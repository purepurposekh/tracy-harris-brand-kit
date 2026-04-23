#!/usr/bin/env node
// Renders WebP thumbnails for every component variant under
// components/<category>/variants/<slug>.html. These thumbnails power the
// mobile fallback on components/compose/ where iframes are disabled to
// avoid iOS Safari white-screen crashes.
//
// Approach:
//   1. Spin up a tiny Node static server from the brand-kit root so variants
//      resolve their ../../../styles/*.css paths naturally.
//   2. Launch chromium via playwright-core (reuses the cached browser).
//   3. For each variant, navigate, wait for network idle + 500ms for fonts,
//      capture a full 1440x900 PNG, then resize to 720x450 WebP via sharp.
//   4. Write to assets/thumbnails/<category>/<slug>.webp.
//
// Usage:
//   node scripts/render-thumbnails.mjs           // render all variants
//   node scripts/render-thumbnails.mjs hero      // render only one category

import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

// Reuse the playwright-core + cached chromium already on this machine rather
// than re-installing inside the brand-kit repo. Keeps node_modules thin.
const PLAYWRIGHT_CORE = '/home/claude-bot/.hermes/hermes-agent/node_modules/playwright-core/index.mjs';
const CHROMIUM_BIN = '/home/claude-bot/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome';

const { chromium } = await import(PLAYWRIGHT_CORE);
const sharp = (await import('sharp')).default;

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COMPONENTS_DIR = path.join(ROOT, 'components');
const OUT_DIR = path.join(ROOT, 'assets', 'thumbnails');

const TARGET_W = 720;
const TARGET_H = 450;
const VIEWPORT_W = 1440;
const VIEWPORT_H = 900;

// --- Walk variants ------------------------------------------------------

const filterCategory = process.argv[2] || null;

function walkVariants() {
  const items = [];
  const categories = fs.readdirSync(COMPONENTS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name)
    .filter(name => name !== 'compose'); // compose page itself, not a component
  for (const cat of categories) {
    if (filterCategory && cat !== filterCategory) continue;
    const variantsDir = path.join(COMPONENTS_DIR, cat, 'variants');
    if (!fs.existsSync(variantsDir)) continue;
    const files = fs.readdirSync(variantsDir).filter(f => f.endsWith('.html'));
    for (const f of files) {
      const slug = f.replace(/\.html$/, '');
      items.push({
        category: cat,
        slug,
        urlPath: `/components/${cat}/variants/${f}`,
        absPath: path.join(variantsDir, f),
      });
    }
  }
  return items;
}

// --- Static server ------------------------------------------------------

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.mjs':  'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
  '.ttf':  'font/ttf',
  '.otf':  'font/otf',
  '.ico':  'image/x-icon',
};

function startServer(port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      try {
        const urlPath = decodeURIComponent(req.url.split('?')[0]);
        let filePath = path.join(ROOT, urlPath);
        // Normalize + protect against traversal.
        filePath = path.normalize(filePath);
        if (!filePath.startsWith(ROOT)) {
          res.writeHead(403); res.end('forbidden'); return;
        }
        if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
          filePath = path.join(filePath, 'index.html');
        }
        if (!fs.existsSync(filePath)) {
          res.writeHead(404); res.end('not found'); return;
        }
        const ext = path.extname(filePath).toLowerCase();
        res.writeHead(200, {
          'Content-Type': MIME[ext] || 'application/octet-stream',
          'Cache-Control': 'no-store',
        });
        fs.createReadStream(filePath).pipe(res);
      } catch (err) {
        res.writeHead(500); res.end(String(err && err.message || err));
      }
    });
    server.listen(port, '127.0.0.1', () => resolve(server));
    server.on('error', reject);
  });
}

// --- Main ---------------------------------------------------------------

const PORT = 8787;
const server = await startServer(PORT);
console.log(`static server: http://127.0.0.1:${PORT}`);

const variants = walkVariants();
console.log(`variants found: ${variants.length}${filterCategory ? ` (filter: ${filterCategory})` : ''}`);

await fsp.mkdir(OUT_DIR, { recursive: true });

const browser = await chromium.launch({
  executablePath: CHROMIUM_BIN,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

const context = await browser.newContext({
  viewport: { width: VIEWPORT_W, height: VIEWPORT_H },
  deviceScaleFactor: 1,
  // Reduce motion so canvas animations / polished variants settle quickly.
  reducedMotion: 'reduce',
});

const startedAt = Date.now();
const failures = [];
let done = 0;
let totalBytes = 0;

for (const v of variants) {
  const outCatDir = path.join(OUT_DIR, v.category);
  await fsp.mkdir(outCatDir, { recursive: true });
  const outPath = path.join(outCatDir, `${v.slug}.webp`);
  const url = `http://127.0.0.1:${PORT}${v.urlPath}`;
  const page = await context.newPage();
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
    // Let webfonts + polish animations settle.
    await page.waitForTimeout(600);
    const png = await page.screenshot({ type: 'png', fullPage: false });
    const webp = await sharp(png)
      .resize(TARGET_W, TARGET_H, { fit: 'cover', position: 'top' })
      .webp({ quality: 78, effort: 4 })
      .toBuffer();
    await fsp.writeFile(outPath, webp);
    totalBytes += webp.length;
    done += 1;
    console.log(`ok   [${done}/${variants.length}] ${v.category}/${v.slug}  ${(webp.length / 1024).toFixed(1)} KB`);
  } catch (err) {
    failures.push({ ...v, error: err.message });
    console.log(`FAIL [${done + failures.length}/${variants.length}] ${v.category}/${v.slug}: ${err.message}`);
  } finally {
    await page.close();
  }
}

await context.close();
await browser.close();
server.close();

const elapsed = ((Date.now() - startedAt) / 1000).toFixed(1);
console.log('');
console.log(`rendered: ${done}/${variants.length}`);
console.log(`failures: ${failures.length}`);
console.log(`total size: ${(totalBytes / 1024 / 1024).toFixed(2)} MB`);
console.log(`elapsed: ${elapsed}s`);
if (failures.length) {
  console.log('');
  console.log('failed variants:');
  for (const f of failures) {
    console.log(`  - ${f.category}/${f.slug}: ${f.error}`);
  }
  process.exit(1);
}
