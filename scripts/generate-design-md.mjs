#!/usr/bin/env node
// Generate Google DESIGN.md files from our primitives + brand tokens.
// One file per brand → exports/design-md/<brand>.md
// The brand-kit is source of truth. These are one-way exports.

import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const PRIMITIVES = JSON.parse(readFileSync(join(ROOT, 'tokens/primitives.json'), 'utf8'));
const BRAND_DIR = join(ROOT, 'tokens/brands');
const OUT_DIR = join(ROOT, 'exports/design-md');
mkdirSync(OUT_DIR, { recursive: true });

function getByPath(obj, path) {
  return path.split('.').reduce((a, k) => (a == null ? a : a[k]), obj);
}

function resolveRef(value) {
  if (typeof value !== 'string') return value;
  const m = value.match(/^\{([^}]+)\}$/);
  if (!m) return value;
  const resolved = getByPath(PRIMITIVES, m[1]);
  return resolved == null ? value : resolveRef(resolved);
}

function flattenColors(brandColor) {
  const out = {};
  const walk = (node, prefix = []) => {
    for (const [k, v] of Object.entries(node)) {
      if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
        walk(v, [...prefix, k]);
      } else {
        const resolved = resolveRef(v);
        if (typeof resolved === 'string' && resolved.startsWith('#')) {
          out[[...prefix, k].join('-')] = resolved;
        } else if (typeof resolved === 'string' && resolved.startsWith('rgba')) {
          // skip rgba for now, design.md wants hex
        }
      }
    }
  };
  walk(brandColor);
  return out;
}

function buildTypography(brandType) {
  const out = {};
  for (const [name, def] of Object.entries(brandType)) {
    out[name] = {
      fontFamily: resolveRef(def.family) || 'inherit',
      fontWeight: resolveRef(def.weight) || 400,
      lineHeight: resolveRef(def.leading) || 1.5,
    };
  }
  return out;
}

function formatYaml(obj, indent = 0) {
  const pad = '  '.repeat(indent);
  const lines = [];
  for (const [k, v] of Object.entries(obj)) {
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      lines.push(`${pad}${k}:`);
      lines.push(formatYaml(v, indent + 1));
    } else if (typeof v === 'string') {
      lines.push(`${pad}${k}: "${v}"`);
    } else {
      lines.push(`${pad}${k}: ${v}`);
    }
  }
  return lines.join('\n');
}

function generate(brandSlug) {
  const brand = JSON.parse(readFileSync(join(BRAND_DIR, `${brandSlug}.json`), 'utf8'));
  const meta = brand._meta;
  const colors = flattenColors(brand.color);
  const typography = buildTypography(brand.type);
  const spacing = Object.fromEntries(
    Object.entries(PRIMITIVES.space).map(([k, v]) => [`s${k}`, v])
  );
  const rounded = Object.fromEntries(
    Object.entries(PRIMITIVES.radius).map(([k, v]) => [k, v === '0' ? '0px' : v])
  );
  // Alias the brand's accent.primary as literal "primary" so the linter + Stitch find it.
  if (colors['accent-primary']) {
    colors.primary = colors['accent-primary'];
  }
  if (colors['ink-inverse']) {
    colors['on-primary'] = colors['ink-inverse'];
  }

  const yaml = [
    'version: "alpha"',
    `name: "${meta.name}"`,
    `description: "${meta.description.replace(/"/g, '\\"')}"`,
    'colors:',
    formatYaml(colors, 1),
    'typography:',
    formatYaml(typography, 1),
    'spacing:',
    formatYaml(spacing, 1),
    'rounded:',
    formatYaml(rounded, 1),
  ].join('\n');

  const prose = [
    '## Overview',
    '',
    meta.description,
    '',
    meta.tagline ? `**Tagline:** ${meta.tagline}` : '',
    '',
    '## Colors',
    '',
    Object.entries(colors)
      .map(([k, v]) => `- **${k}** (\`${v}\`)`)
      .join('\n'),
    '',
    '## Typography',
    '',
    'Families and weights resolve from primitives. See tokens/primitives.json for canonical values.',
    '',
    '## Voice',
    '',
    brand.voice ? `**Tone:** ${brand.voice.tone}` : '',
    brand.voice && brand.voice.exampleCopy ? `\n**Example:** ${brand.voice.exampleCopy}` : '',
    '',
    '## Source of Truth',
    '',
    'This file is generated from `tokens/primitives.json` + `tokens/brands/' + brandSlug + '.json`. Do not hand-edit. Run `npm run design-md` to regenerate.',
  ]
    .filter(Boolean)
    .join('\n');

  return `---\n${yaml}\n---\n\n${prose}\n`;
}

const brands = readdirSync(BRAND_DIR)
  .filter((f) => f.endsWith('.json'))
  .map((f) => f.replace('.json', ''));

for (const b of brands) {
  const out = generate(b);
  const path = join(OUT_DIR, `${b}.md`);
  writeFileSync(path, out, 'utf8');
  console.log(`Generated ${path} (${out.length} bytes)`);
}

console.log(`\nDone. ${brands.length} DESIGN.md files written to ${OUT_DIR}`);
