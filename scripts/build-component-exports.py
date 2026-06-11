#!/usr/bin/env python3
"""
Build the component-library export artifacts:

  exports/components-master.md      one file with every component's CSS + HTML,
                                    made to hand to another AI/design system
  exports/brand-kit-components.zip  tokens + fonts + every family CSS + every
                                    variant HTML, structure preserved

Run from repo root: python3 scripts/build-component-exports.py
"""
from __future__ import annotations

import pathlib
import re
import zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / 'components'
EXPORTS = ROOT / 'exports'
EXPORTS.mkdir(exist_ok=True)

CDN = 'https://cdn.jsdelivr.net/gh/purepurposekh/tracy-harris-brand-kit@main'

SKIP_DIRS = {'compose'}  # the page builder, not a visual component

LINK_RE = re.compile(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>')
STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)
BODY_RE = re.compile(r'<body[^>]*>(.*)</body>', re.S)
BODY_TAG_RE = re.compile(r'<body([^>]*)>')


def variant_assets(path: pathlib.Path):
    """Return (linked_css_paths, inline_styles, body_attrs, body_html)."""
    t = path.read_text(encoding='utf-8', errors='ignore')
    css_paths = []
    for href in LINK_RE.findall(t):
        if href.startswith('http') or 'tokens.css' in href or 'fonts.css' in href:
            continue
        resolved = (path.parent / href).resolve()
        if resolved.exists():
            css_paths.append(resolved)
    styles = [s.strip() for s in STYLE_RE.findall(t) if s.strip()]
    m = BODY_RE.search(t)
    body = m.group(1).strip() if m else ''
    m2 = BODY_TAG_RE.search(t)
    attrs = m2.group(1).strip() if m2 else ''
    return css_paths, styles, attrs, body


def build():
    families = sorted(d for d in COMPONENTS.iterdir() if d.is_dir() and d.name not in SKIP_DIRS)
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    md = [
        '# Tracy Harris Co · Brand Kit Component Library (master file)',
        '',
        f'Generated {stamp} from the brand-kit repo. {sum(1 for f in families for _ in (f / "variants").glob("*.html") if (f / "variants").exists())} variants across {len(families)} families.',
        '',
        '## How to use these components',
        '',
        'Every component depends on two shared stylesheets (design tokens + brand fonts). Load them first:',
        '',
        '```html',
        f'<link rel="stylesheet" href="{CDN}/styles/fonts.css">',
        f'<link rel="stylesheet" href="{CDN}/styles/tokens.css">',
        '```',
        '',
        'Then set the brand context on the component\'s wrapper (or the page body): `data-brand="tracy"`, `data-brand="ffb"`, `data-brand="ffm"`, or `data-brand="fresh"`. The semantic CSS variables (surfaces, ink, accents, type) resolve from that attribute.',
        '',
        'Each family below ships its shared CSS once, then every variant\'s HTML. Variants that carry extra inline CSS include it with the variant.',
        '',
        '---',
        '',
    ]

    zip_path = EXPORTS / 'brand-kit-components.zip'
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zf.write(ROOT / 'styles' / 'tokens.css', 'styles/tokens.css')
    zf.write(ROOT / 'styles' / 'fonts.css', 'styles/fonts.css')
    if (ROOT / 'styles' / 'brand-system.css').exists():
        zf.write(ROOT / 'styles' / 'brand-system.css', 'styles/brand-system.css')

    total_variants = 0
    for fam in families:
        vdir = fam / 'variants'
        if not vdir.exists():
            continue
        variants = sorted(vdir.glob('*.html'))
        if not variants:
            continue
        md.append(f'## {fam.name} · {len(variants)} variant{"s" if len(variants) != 1 else ""}')
        md.append('')

        fam_css_seen: list[pathlib.Path] = []
        entries = []
        for v in variants:
            css_paths, styles, attrs, body = variant_assets(v)
            for c in css_paths:
                if c not in fam_css_seen:
                    fam_css_seen.append(c)
            entries.append((v, styles, attrs, body))
            zf.write(v, str(v.relative_to(ROOT)))
            total_variants += 1

        for c in fam_css_seen:
            zf.write(c, str(c.relative_to(ROOT)))
            md.append(f'### Shared CSS · `{c.relative_to(ROOT)}`')
            md.append('')
            md.append('```css')
            md.append(c.read_text(encoding="utf-8", errors="ignore").strip())
            md.append('```')
            md.append('')

        for v, styles, attrs, body in entries:
            md.append(f'### {fam.name}.{v.stem}')
            md.append('')
            if attrs:
                md.append(f'Wrapper context: `<body {attrs}>`')
                md.append('')
            for s in styles:
                if 'margin: 0; font-family: var(--f-sans)' in s and len(s) < 200:
                    continue  # boilerplate body reset, not component CSS
                md.append('```css')
                md.append(s)
                md.append('```')
                md.append('')
            md.append('```html')
            md.append(body)
            md.append('```')
            md.append('')
        md.append('---')
        md.append('')

    readme = (
        '# Tracy Harris Co · Brand Kit Components\n\n'
        f'Exported {stamp}. Structure: styles/ holds the shared design tokens and fonts; '
        'components/<family>/ holds each family\'s shared CSS and its variants/ as standalone HTML.\n\n'
        'To use a variant elsewhere: load styles/fonts.css + styles/tokens.css, include the family CSS, '
        'copy the variant\'s body markup, and keep a data-brand attribute (tracy | ffb | ffm | fresh) on a wrapper.\n'
    )
    zf.writestr('README.md', readme)
    zf.close()

    master = EXPORTS / 'components-master.md'
    master.write_text('\n'.join(md), encoding='utf-8')
    print(f'wrote {master} ({master.stat().st_size/1024:.0f} KB)')
    print(f'wrote {zip_path} ({zip_path.stat().st_size/1024:.0f} KB), {total_variants} variants')


if __name__ == '__main__':
    build()
