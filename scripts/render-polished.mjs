#!/usr/bin/env node
// Quick render verifier for polished variants.
// Renders each HTML file at desktop + mobile, saves PNGs, reports file size.
// Usage: node scripts/render-polished.mjs <file1> <file2> ...

import { chromium } from '/home/claude-bot/.hermes/hermes-agent/node_modules/playwright-core/index.mjs';
import path from 'node:path';
import fs from 'node:fs';

const files = process.argv.slice(2);
if (!files.length) {
  console.error('No files given');
  process.exit(1);
}

const outDir = '/tmp/render-polished';
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({
  executablePath: '/home/claude-bot/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

for (const file of files) {
  const abs = path.resolve(file);
  const url = 'file://' + abs;
  const basename = path.basename(abs, '.html');

  for (const [label, viewport] of [
    ['desktop', { width: 1440, height: 900 }],
    ['mobile',  { width: 390,  height: 844 }],
  ]) {
    const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 15000 });
      await page.waitForTimeout(400);
      const outPath = `${outDir}/${basename}-${label}.png`;
      await page.screenshot({ path: outPath, fullPage: false });
      const size = fs.statSync(outPath).size;
      const ok = size > 20_000 ? 'OK' : (size < 5_000 ? 'BROKEN' : 'thin');
      console.log(`${ok}  ${label.padEnd(7)}  ${size.toString().padStart(8)} bytes  ${basename}`);
    } catch (err) {
      console.log(`ERR  ${label.padEnd(7)}  ${basename}: ${err.message}`);
    } finally {
      await ctx.close();
    }
  }
}

await browser.close();
