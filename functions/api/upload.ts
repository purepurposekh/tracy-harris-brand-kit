interface Env {
  R2_BUCKET: R2Bucket;
  WEBHOOK_TAG_URL: string;
  WEBHOOK_AUTH_TOKEN: string;
}

const ALLOWED_MIME = new Set([
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/heic',
  'image/heif',
]);

const MAX_BYTES = 30 * 1024 * 1024;

function err(status: number, message: string) {
  return new Response(JSON.stringify({ ok: false, error: message }), {
    status,
    headers: { 'content-type': 'application/json', 'access-control-allow-origin': '*' },
  });
}

function ok(body: Record<string, unknown>) {
  return new Response(JSON.stringify({ ok: true, ...body }), {
    headers: { 'content-type': 'application/json', 'access-control-allow-origin': '*' },
  });
}

function slug(): string {
  const bytes = new Uint8Array(4);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}

function extFor(mime: string): string {
  if (mime === 'image/jpeg') return 'jpg';
  if (mime === 'image/png') return 'png';
  if (mime === 'image/webp') return 'webp';
  if (mime === 'image/heic') return 'heic';
  if (mime === 'image/heif') return 'heif';
  return 'jpg';
}

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, {
    status: 204,
    headers: {
      'access-control-allow-origin': '*',
      'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'authorization, content-type',
    },
  });

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const auth = request.headers.get('authorization') || '';
  const expected = `Bearer ${env.WEBHOOK_AUTH_TOKEN}`;
  if (!env.WEBHOOK_AUTH_TOKEN || auth !== expected) {
    return err(401, 'Unauthorized');
  }

  let form: FormData;
  try {
    form = await request.formData();
  } catch (e) {
    return err(400, 'Could not parse multipart body');
  }
  const file = form.get('image');
  if (!(file instanceof File)) {
    return err(400, 'image field is required');
  }
  if (file.size > MAX_BYTES) {
    return err(413, `File exceeds ${MAX_BYTES} bytes`);
  }
  const mime = file.type || 'image/jpeg';
  if (!ALLOWED_MIME.has(mime)) {
    return err(415, `Unsupported content type: ${mime}`);
  }

  const id = slug();
  const ext = extFor(mime);
  const r2Filename = `${id}.${ext}`;
  const photoKey = `photos/${r2Filename}`;

  try {
    await env.R2_BUCKET.put(photoKey, file.stream(), {
      httpMetadata: { contentType: mime },
    });
  } catch (e) {
    return err(500, `R2 write failed: ${(e as Error).message}`);
  }

  let tagged: Record<string, unknown>;
  try {
    const tagRes = await fetch(env.WEBHOOK_TAG_URL, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${env.WEBHOOK_AUTH_TOKEN}`,
      },
      body: JSON.stringify({ slug: id, r2_filename: r2Filename, content_type: mime }),
    });
    if (!tagRes.ok) {
      return err(502, `Tagger returned ${tagRes.status}`);
    }
    tagged = await tagRes.json();
  } catch (e) {
    return err(502, `Tagger fetch failed: ${(e as Error).message}`);
  }

  const photoUrl = `https://assets.tracyharris.com.au/photos/${r2Filename}`;
  tagged._source_path = `r2:tracy-brand-assets/photos/${r2Filename}`;
  tagged.photo_url = photoUrl;
  tagged.filename = r2Filename;

  try {
    await env.R2_BUCKET.put(`manifest/${id}.json`, JSON.stringify(tagged, null, 2), {
      httpMetadata: { contentType: 'application/json' },
    });
  } catch (e) {
    return err(500, `Manifest write failed: ${(e as Error).message}`);
  }

  try {
    const idxObj = await env.R2_BUCKET.get('index.json');
    let idx: { schema_version: string; generated_at: string; count: number; public_base: string; fields: string[]; items: unknown[] };
    if (idxObj) {
      idx = await idxObj.json();
    } else {
      idx = {
        schema_version: '1.0',
        generated_at: new Date().toISOString(),
        count: 0,
        public_base: 'https://assets.tracyharris.com.au',
        fields: [],
        items: [],
      };
    }
    idx.items.push(tagged);
    idx.count = idx.items.length;
    idx.generated_at = new Date().toISOString();
    await env.R2_BUCKET.put('index.json', JSON.stringify(idx, null, 2), {
      httpMetadata: { contentType: 'application/json' },
    });
  } catch (e) {
    return err(500, `Index update failed: ${(e as Error).message}`);
  }

  return ok({ slug: id, photo_url: photoUrl, tags: tagged });
};
