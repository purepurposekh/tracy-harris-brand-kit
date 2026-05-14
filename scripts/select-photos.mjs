#!/usr/bin/env node
/**
 * Slot-aware photo selector for Tracy Harris brand library.
 *
 * Replaces score-first selection (which systematically excluded documentary /
 * teaching / credibility shots) with weighted-per-slot scoring across 6 axes,
 * plus hard filters and series diversity.
 *
 * Usage as a library:
 *   import { selectPhotos } from './select-photos.mjs';
 *   const { candidates, chosen } = await selectPhotos({
 *     slot: 'teaching credibility',
 *     count: 1,
 *     tracyPresent: true,
 *     excludeShootIds: ['th-pb-2024-outfit8'],
 *   });
 *
 * Usage as a CLI:
 *   node scripts/select-photos.mjs --slot "teaching credibility" --count 1 --tracy-present
 *   node scripts/select-photos.mjs --slot "hero portrait" --count 3
 *
 * Output: ranked candidates with score + reasons + per-dimension breakdown.
 */

const INDEX_URL = 'https://assets.tracyharris.com.au/index.json';

// Slot weights over score_dimensions (brand_fit / proof_value / authenticity /
// production_quality / crop_flexibility / emotional_fit). Locked per spec.
export const SLOT_WEIGHTS = {
  'hero portrait': {
    brand_fit: 0.5,
    crop_flexibility: 0.2,
    emotional_fit: 0.15,
    production_quality: 0.1,
    proof_value: 0.05,
    authenticity: 0,
  },
  'teaching credibility': {
    proof_value: 0.45,
    authenticity: 0.2,
    emotional_fit: 0.15,
    brand_fit: 0.1,
    crop_flexibility: 0.1,
    production_quality: 0,
  },
  'lifestyle authenticity': {
    authenticity: 0.45,
    emotional_fit: 0.2,
    brand_fit: 0.15,
    crop_flexibility: 0.15,
    production_quality: 0.05,
    proof_value: 0,
  },
  'about Tracy': {
    emotional_fit: 0.3,
    brand_fit: 0.25,
    authenticity: 0.2,
    crop_flexibility: 0.15,
    proof_value: 0.1,
    production_quality: 0,
  },
  'social proof event': {
    proof_value: 0.5,
    authenticity: 0.2,
    emotional_fit: 0.15,
    brand_fit: 0.1,
    crop_flexibility: 0.05,
    production_quality: 0,
  },
  'retreat-freedom': {
    emotional_fit: 0.35,
    authenticity: 0.25,
    brand_fit: 0.2,
    crop_flexibility: 0.15,
    proof_value: 0.05,
    production_quality: 0,
  },
};

const DIMENSIONS = [
  'brand_fit',
  'proof_value',
  'authenticity',
  'production_quality',
  'crop_flexibility',
  'emotional_fit',
];

const FALLBACK_WEIGHTS = Object.fromEntries(DIMENSIONS.map(d => [d, 1 / DIMENSIONS.length]));

// Intent-tag hints per slot. Used as a soft hard-filter: if the photo has at
// least one of these intent_tags, it's eligible. Empty list = no intent_tag gate.
const SLOT_INTENT_TAGS = {
  'hero portrait': ['hero', 'editorial', 'premium', 'authority'],
  'teaching credibility': ['teaching', 'speaking', 'authority', 'proof'],
  'lifestyle authenticity': ['lifestyle', 'candid', 'warmth', 'intimate'],
  'about Tracy': ['warmth', 'intimate', 'authority', 'editorial'],
  'social proof event': ['speaking', 'audience', 'proof', 'authority'],
  'retreat-freedom': ['retreat', 'lifestyle', 'premium', 'warmth'],
};

let _indexCache = null;

export async function loadIndex(url = INDEX_URL) {
  if (_indexCache) return _indexCache;
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`Fetch ${url} returned ${res.status}`);
  _indexCache = await res.json();
  return _indexCache;
}

// Fallback scoring: when an item has no score_dimensions yet (legacy v1 items),
// fan the single on_brand_score across all 6 dimensions. Lets the selector
// keep working through the migration window without forcing a re-tag.
function dimensions(item) {
  if (item.score_dimensions && typeof item.score_dimensions === 'object') {
    return Object.fromEntries(
      DIMENSIONS.map(d => [d, Number(item.score_dimensions[d]) || 0])
    );
  }
  const fallback = Number(item.on_brand_score) || 0;
  return Object.fromEntries(DIMENSIONS.map(d => [d, fallback]));
}

function weightedScore(item, weights) {
  const dims = dimensions(item);
  return DIMENSIONS.reduce((sum, d) => sum + dims[d] * (weights[d] || 0), 0);
}

function intentMatch(item, slotTags) {
  if (!slotTags || slotTags.length === 0) return true;
  const tags = (item.intent_tags || []).map(t => String(t).toLowerCase());
  return slotTags.some(t => tags.includes(t.toLowerCase()));
}

function primaryUseMatch(item, slot) {
  // Slot names align with the primary_use enum on purpose. If primary_use
  // matches, that's a strong positive signal (use as a bonus, not a hard gate,
  // since secondary_uses might also justify inclusion).
  const pu = String(item.primary_use || '').toLowerCase();
  if (pu === slot.toLowerCase()) return 'primary';
  const sec = (item.secondary_uses || []).map(s => String(s).toLowerCase());
  if (sec.includes(slot.toLowerCase())) return 'secondary';
  return null;
}

function reasons(item, slot, weights, slotIntentTags) {
  const dims = dimensions(item);
  const out = [];
  const matched = primaryUseMatch(item, slot);
  if (matched === 'primary') out.push(`primary_use matches "${slot}"`);
  else if (matched === 'secondary') out.push(`listed as a secondary_use for "${slot}"`);
  const intents = (item.intent_tags || []).filter(t =>
    slotIntentTags.map(x => x.toLowerCase()).includes(String(t).toLowerCase())
  );
  if (intents.length) out.push(`intent_tags hit: ${intents.join(', ')}`);
  // Highlight strongest dimensions weighted into this slot.
  const sorted = Object.entries(weights)
    .filter(([, w]) => w > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);
  for (const [d, w] of sorted) {
    out.push(`${d}=${dims[d].toFixed(2)} (weight ${w})`);
  }
  if (!item.score_dimensions) {
    out.push('legacy v1 record, score_dimensions inferred from on_brand_score');
  }
  return out;
}

/**
 * @param {object} opts
 * @param {string} opts.slot - one of SLOT_WEIGHTS keys (or a primary_use enum value)
 * @param {number} [opts.count=1]
 * @param {boolean} [opts.tracyPresent] - filter by tracy_present (undefined = no filter)
 * @param {number} [opts.peopleCount] - exact people_count match
 * @param {string} [opts.candidOrPosed] - 'candid' | 'posed'
 * @param {string[]} [opts.excludeShootIds] - shoot_ids already used on the page (enforce diversity)
 * @param {string[]} [opts.excludeFilenames] - filenames already chosen
 * @param {string[]} [opts.locationTypes] - whitelist of location_type values
 * @param {boolean} [opts.allowSeriesRepeat=false] - if true, allow more than one from same shoot_id
 * @param {string} [opts.indexUrl]
 */
export async function selectPhotos(opts) {
  const {
    slot,
    count = 1,
    tracyPresent,
    peopleCount,
    candidOrPosed,
    excludeShootIds = [],
    excludeFilenames = [],
    locationTypes,
    allowSeriesRepeat = false,
    indexUrl,
  } = opts;
  if (!slot) throw new Error('slot is required');

  const index = await loadIndex(indexUrl);
  const items = index.items || [];
  const weights = SLOT_WEIGHTS[slot] || FALLBACK_WEIGHTS;
  const slotIntentTags = SLOT_INTENT_TAGS[slot] || [];

  // Hard filters.
  const filtered = items.filter(item => {
    if (excludeFilenames.includes(item.filename)) return false;
    if (typeof tracyPresent === 'boolean' && Boolean(item.tracy_present) !== tracyPresent) return false;
    if (typeof peopleCount === 'number' && Number(item.people_count) !== peopleCount) return false;
    if (candidOrPosed && String(item.candid_or_posed || '').toLowerCase() !== candidOrPosed.toLowerCase()) return false;
    if (locationTypes && locationTypes.length) {
      const lt = String(item.location_type || '').toLowerCase();
      if (!locationTypes.map(x => x.toLowerCase()).includes(lt)) return false;
    }
    // Intent-tag gate. Skipped for legacy v1 records that have no intent_tags
    // at all. Those get evaluated on weighted score only, and the selector
    // notes that in the reasons list.
    if ((item.intent_tags || []).length > 0 && !intentMatch(item, slotIntentTags)) return false;
    return true;
  });

  // Score each candidate, with a small bonus for matching primary_use.
  const scored = filtered.map(item => {
    let score = weightedScore(item, weights);
    const puMatch = primaryUseMatch(item, slot);
    if (puMatch === 'primary') score += 0.15;
    else if (puMatch === 'secondary') score += 0.05;
    return {
      filename: item.filename,
      photo_url: item.photo_url,
      shoot_id: item.shoot_id || null,
      score: Number(score.toFixed(4)),
      reasons: reasons(item, slot, weights, slotIntentTags),
      scores_breakdown: dimensions(item),
      primary_use: item.primary_use || null,
      intent_tags: item.intent_tags || [],
      _item: item,
    };
  });

  scored.sort((a, b) => b.score - a.score);

  // Series diversity. Don't return more than one photo from the same shoot_id
  // unless the caller explicitly opted in or the photo has no shoot_id yet
  // (legacy items, fall back to filename diversity).
  const seenShoots = new Set(excludeShootIds.map(s => String(s).toLowerCase()));
  const chosen = [];
  for (const cand of scored) {
    const sid = cand.shoot_id ? String(cand.shoot_id).toLowerCase() : null;
    if (!allowSeriesRepeat && sid && seenShoots.has(sid)) continue;
    if (sid) seenShoots.add(sid);
    chosen.push(cand);
    if (chosen.length >= count) break;
  }

  return {
    slot,
    count_requested: count,
    candidates: scored.slice(0, Math.max(count * 5, 10)).map(c => {
      const { _item, ...rest } = c;
      return rest;
    }),
    chosen: chosen.map(c => {
      const { _item, ...rest } = c;
      return rest;
    }),
    chosen_filename: chosen[0]?.filename || null,
    weights,
    filtered_count: filtered.length,
    total_items: items.length,
    schema_version: index.schema_version || 'unknown',
  };
}

// ---------- CLI ----------

function parseArgs(argv) {
  const out = { slot: null, count: 1 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slot') out.slot = argv[++i];
    else if (a === '--count') out.count = parseInt(argv[++i], 10) || 1;
    else if (a === '--tracy-present') out.tracyPresent = true;
    else if (a === '--no-tracy') out.tracyPresent = false;
    else if (a === '--people') out.peopleCount = parseInt(argv[++i], 10);
    else if (a === '--candid') out.candidOrPosed = 'candid';
    else if (a === '--posed') out.candidOrPosed = 'posed';
    else if (a === '--exclude-shoot') out.excludeShootIds = (out.excludeShootIds || []).concat(argv[++i]);
    else if (a === '--exclude-file') out.excludeFilenames = (out.excludeFilenames || []).concat(argv[++i]);
    else if (a === '--location') out.locationTypes = (out.locationTypes || []).concat(argv[++i]);
    else if (a === '--allow-series-repeat') out.allowSeriesRepeat = true;
    else if (a === '--index-url') out.indexUrl = argv[++i];
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function printHelp() {
  console.log(`Usage: node scripts/select-photos.mjs --slot "<slot>" [options]

Slots:
  ${Object.keys(SLOT_WEIGHTS).map(s => `"${s}"`).join('\n  ')}

Options:
  --count N                   How many to return (default 1)
  --tracy-present             Only photos with tracy_present=true
  --no-tracy                  Only photos with tracy_present=false
  --people N                  Filter by exact people_count
  --candid | --posed          Filter by candid_or_posed
  --exclude-shoot SLUG        Exclude this shoot_id (repeatable)
  --exclude-file NAME         Exclude this filename (repeatable)
  --location TYPE             Whitelist location_type (repeatable)
  --allow-series-repeat       Permit multiple photos from same shoot_id
  --index-url URL             Override default index URL
  --json                      Emit raw JSON only (machine-readable)

Examples:
  node scripts/select-photos.mjs --slot "teaching credibility" --count 1 --tracy-present
  node scripts/select-photos.mjs --slot "hero portrait" --count 3 --json
`);
}

async function cli() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.slot) {
    printHelp();
    process.exit(args.help ? 0 : 1);
  }
  const result = await selectPhotos(args);

  if (args.json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`Slot: ${result.slot}`);
  console.log(`Schema: ${result.schema_version}  |  Total items: ${result.total_items}  |  After filters: ${result.filtered_count}`);
  console.log(`Weights: ${JSON.stringify(result.weights)}`);
  console.log('');
  console.log(`Chosen (${result.chosen.length} of ${result.count_requested} requested):`);
  result.chosen.forEach((c, i) => {
    console.log(`  ${i + 1}. ${c.filename}  score=${c.score}  primary_use=${c.primary_use || '-'}  shoot_id=${c.shoot_id || '-'}`);
    console.log(`     ${c.photo_url}`);
    c.reasons.forEach(r => console.log(`     - ${r}`));
  });
  console.log('');
  console.log(`Other candidates considered (top ${result.candidates.length}):`);
  result.candidates.forEach((c, i) => {
    console.log(`  ${i + 1}. ${c.filename}  score=${c.score}  primary_use=${c.primary_use || '-'}  shoot_id=${c.shoot_id || '-'}`);
  });
}

// Run CLI when invoked directly.
if (import.meta.url === `file://${process.argv[1]}`) {
  cli().catch(err => {
    console.error('select-photos failed:', err.message);
    process.exit(1);
  });
}
