#!/usr/bin/env python3
"""
Generate pages/all-components.html by walking components/*/variants/*.html.

Each variant's name is derived from its filename (sans .html). The display
title is read from the <title> tag. Category names are the component
directory names.

Run from the brand-kit repo root:
    python3 scripts/generate-all-components.py
"""
from __future__ import annotations

import html
import pathlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPONENTS_DIR = ROOT / 'components'
OUT = ROOT / 'pages' / 'all-components.html'

# Pretty category titles + one-line description each
CATEGORY_META = {
    'about-bio':          ('About / Bio',            'Personal intro, founder story, bio blocks.'),
    'benefit-trio':        ('Benefit Trio',           'Three-feature rows with icon/number + short body.'),
    'card-flip':           ('Card Flip',              'Front/back cards that flip on hover or tap.'),
    'compose':             ('Compose',                'Page builder, not a visual component.'),
    'content-section':    ('Content Section',        'Generic long-form copy blocks with editorial rhythm.'),
    'cta-block':           ('CTA Block',              'Stand-alone calls to action and mid-page conversion moments.'),
    'curriculum-preview':  ('Curriculum Preview',     'Module/lesson breakdowns for courses, programs, workshops.'),
    'event-widget':        ('Event Widget',           'Live/upcoming event cards and registration blocks.'),
    'expandable-cta':      ('Expandable CTA',         'Collapsed CTA that expands to reveal detail or form.'),
    'faq':                 ('FAQ',                    'Question/answer lists with accordion or inline patterns.'),
    'feature-grid':        ('Feature Grid',           'Multi-item feature matrices, for programs or inclusions.'),
    'footer':              ('Footer',                 'Site footers across all sub-brands.'),
    'freebies':            ('Freebies',               'Lead-magnet offer blocks and download cards.'),
    'guarantee':           ('Guarantee',              'Trust-building, risk-reversal blocks.'),
    'hero':                ('Hero',                   'Top-of-page hero blocks. The most used component.'),
    'image-grid':          ('Image Grid',             'Masonry / gallery / editorial image layouts.'),
    'navigation':          ('Navigation',             'Header menus, sub-nav, in-page jump links.'),
    'next-steps':          ('Next Steps',             'Post-conversion guidance, thank-you page structures.'),
    'offer-stack':         ('Offer Stack',            'Value stack / inclusions stacked with dollar framing.'),
    'opt-in':              ('Opt-in',                 'Email capture forms and lead-gen sign-up blocks.'),
    'podcast-card':        ('Podcast Card',           'Podcast episode cards and lineup blocks.'),
    'post-grid':           ('Post Grid',              'Blog post feeds, journal / article list layouts.'),
    'pricing':             ('Pricing',                'Pricing tables and payment option blocks.'),
    'product-callout':    ('Product Callout',        'Inline callouts pointing to FFB or FFM.'),
    'programs-grid':       ('Programs Grid',          'Cards for multiple programs, tiers, or offerings.'),
    'review':              ('Review / Audit',         'Audit pages for testing components, not for production use.'),
    'soft-upsell':         ('Soft Upsell',            'Gentle upsell blocks that feel like value, not push.'),
    'testimonials':        ('Testimonials',           'Member story cards and quote blocks.'),
    'why-block':           ('Why Block',              'The "why it works" explainer blocks.'),
}

# Components that are operational (not visual components) to exclude from the visual index
OPERATIONAL = {'compose', 'review'}


@dataclass
class Variant:
    slug: str              # filename without .html
    title: str             # human-readable from <title>
    rel_path: str          # relative path to the HTML file
    size_kb: float

    @property
    def copy_id(self) -> str:
        # The canonical name Karl can copy + paste to ask for this variant.
        return f"{self.category_slug}.{self.slug}"

    category_slug: str = ''


def read_title(path: pathlib.Path) -> str:
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            head = f.read(2048)
        m = re.search(r'<title>(.+?)</title>', head, flags=re.IGNORECASE | re.DOTALL)
        if not m:
            return path.stem.replace('-', ' ').title()
        return re.sub(r'\s+', ' ', m.group(1)).strip()
    except OSError:
        return path.stem


def walk_components() -> list[tuple[str, list[Variant]]]:
    out: list[tuple[str, list[Variant]]] = []
    for comp_dir in sorted(COMPONENTS_DIR.iterdir()):
        if not comp_dir.is_dir():
            continue
        slug = comp_dir.name
        if slug in OPERATIONAL:
            continue
        variants_dir = comp_dir / 'variants'
        if not variants_dir.is_dir():
            continue
        variants: list[Variant] = []
        for v in sorted(variants_dir.glob('*.html')):
            size = v.stat().st_size / 1024
            variants.append(Variant(
                slug=v.stem,
                title=read_title(v),
                rel_path=f'../components/{slug}/variants/{v.name}',
                size_kb=size,
                category_slug=slug,
            ))
        if variants:
            out.append((slug, variants))
    return out


def render(sections: list[tuple[str, list[Variant]]]) -> str:
    total_variants = sum(len(v) for _, v in sections)
    total_categories = len(sections)
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Sidebar nav
    sidebar_items = []
    for slug, variants in sections:
        cat_title, _ = CATEGORY_META.get(slug, (slug.replace('-', ' ').title(), ''))
        sidebar_items.append(
            f'<li><a href="#cat-{slug}"><span>{html.escape(cat_title)}</span>'
            f'<span class="ac-count">{len(variants)}</span></a></li>'
        )
    sidebar_html = '\n'.join(sidebar_items)

    # Per-category aspect overrides so iframes scale to the component's natural shape.
    # Same heuristics the compose page uses.
    aspect_by_category = {
        'navigation':  '1440 / 160',
        'footer':      '1440 / 560',
        'opt-in':      '16 / 7',
        'guarantee':   '16 / 6',
        'next-steps':  '16 / 7',
        'soft-upsell': '16 / 7',
        'cta-block':   '16 / 7',
        'podcast-card':'16 / 9',
        'testimonials':'16 / 10',
    }

    # Sections (both list rows + tile cards, toggle between on client)
    section_blocks = []
    for slug, variants in sections:
        cat_title, cat_desc = CATEGORY_META.get(slug, (slug.replace('-', ' ').title(), ''))
        aspect = aspect_by_category.get(slug, '16 / 10')

        rows = []
        tiles = []
        for v in variants:
            search_attr = html.escape(v.copy_id + ' ' + v.title)
            rows.append(f'''
              <tr data-search="{search_attr}">
                <td class="ac-cell ac-cell--id">
                  <code class="ac-copy" data-copy="{html.escape(v.copy_id)}">{html.escape(v.copy_id)}</code>
                </td>
                <td class="ac-cell ac-cell--title">{html.escape(v.title)}</td>
                <td class="ac-cell ac-cell--size">{v.size_kb:.1f} KB</td>
                <td class="ac-cell ac-cell--actions">
                  <a class="ac-link" href="{html.escape(v.rel_path)}" target="_blank" rel="noopener">Open →</a>
                </td>
              </tr>
            ''')
            tiles.append(f'''
              <article class="ac-tile" data-search="{search_attr}">
                <a class="ac-tile__thumb" href="{html.escape(v.rel_path)}" target="_blank" rel="noopener" aria-label="Open {html.escape(v.title)}" style="aspect-ratio: {aspect};">
                  <iframe loading="lazy" src="{html.escape(v.rel_path)}" title="{html.escape(v.title)}" tabindex="-1"></iframe>
                  <span class="ac-tile__hover">Open →</span>
                </a>
                <div class="ac-tile__meta">
                  <code class="ac-copy ac-copy--tile" data-copy="{html.escape(v.copy_id)}">{html.escape(v.copy_id)}</code>
                  <p class="ac-tile__title">{html.escape(v.title)}</p>
                </div>
              </article>
            ''')

        section_blocks.append(f'''
          <section class="ac-section" id="cat-{html.escape(slug)}" data-category-slug="{html.escape(slug)}">
            <header class="ac-section__head">
              <h2 class="ac-section__title">{html.escape(cat_title)}</h2>
              <span class="ac-section__count">{len(variants)} variant{"s" if len(variants) != 1 else ""}</span>
            </header>
            {f'<p class="ac-section__desc">{html.escape(cat_desc)}</p>' if cat_desc else ''}
            <div class="ac-view ac-view--list">
              <table class="ac-table">
                <thead>
                  <tr>
                    <th>Copy name</th>
                    <th>Title</th>
                    <th>Size</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>{"".join(rows)}</tbody>
              </table>
            </div>
            <div class="ac-view ac-view--tile">
              <div class="ac-tiles">{"".join(tiles)}</div>
            </div>
          </section>
        ''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>All Components · Tracy Harris Co Brand Kit</title>
  <meta name="description" content="Index of every component in the brand kit. Copy a component name, share it with Kira." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles/fonts.css" />
  <link rel="stylesheet" href="../styles/tokens.css" />
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: var(--f-sans); background: var(--p-oatmeal); color: var(--p-ink); -webkit-font-smoothing: antialiased; }}
    a {{ color: inherit; }}

    .ac-top {{
      display: flex; justify-content: space-between; align-items: baseline;
      padding: 28px clamp(24px, 5vw, 64px);
      border-bottom: 1px solid rgba(16,16,16,0.08);
      background: var(--p-oatmeal);
      position: sticky; top: 0; z-index: 10;
    }}
    .ac-top a {{ font-size: 13px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--p-aztek); text-decoration: none; margin-left: 20px; }}
    .ac-top a:hover {{ color: var(--p-copper); }}
    .ac-top__title {{ font-family: var(--f-serif-display); font-size: clamp(24px, 2.4vw, 32px); color: var(--p-aztek); margin: 0; letter-spacing: -0.015em; }}
    .ac-top__title em {{ font-family: var(--f-serif-italic); font-style: italic; color: var(--p-copper); }}
    .ac-top__nav {{ font-size: 12px; }}

    .ac-layout {{ display: grid; grid-template-columns: 280px 1fr; gap: 48px; padding: 48px clamp(24px, 5vw, 64px); max-width: 1480px; margin: 0 auto; }}
    @media (max-width: 900px) {{ .ac-layout {{ grid-template-columns: 1fr; gap: 24px; }} }}

    .ac-sidebar {{ position: sticky; top: 120px; align-self: start; }}
    .ac-sidebar__h {{ font-size: 11px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--p-mute); margin: 0 0 18px; font-weight: 500; }}
    .ac-sidebar ul {{ list-style: none; padding: 0; margin: 0 0 28px; }}
    .ac-sidebar li {{ margin: 0; }}
    .ac-sidebar a {{ display: flex; justify-content: space-between; align-items: baseline; padding: 8px 0; font-size: 14px; color: var(--p-aztek); text-decoration: none; border-bottom: 1px solid rgba(16,16,16,0.06); transition: color 180ms ease, border-color 180ms ease; }}
    .ac-sidebar a:hover {{ color: var(--p-copper); border-color: rgba(173,118,91,0.4); }}
    .ac-count {{ font-family: var(--f-serif-display); font-style: italic; color: var(--p-copper); font-size: 13px; }}

    .ac-intro {{ margin-bottom: 40px; max-width: 720px; }}
    .ac-intro p {{ font-size: 15px; line-height: 1.72; color: var(--p-ink); margin: 0 0 14px; }}
    .ac-intro__stats {{ display: flex; gap: 40px; padding-top: 16px; border-top: 1px solid rgba(16,16,16,0.12); margin-top: 16px; flex-wrap: wrap; }}
    .ac-stat__num {{ font-family: var(--f-serif-display); font-size: 28px; color: var(--p-aztek); line-height: 1; margin-bottom: 4px; }}
    .ac-stat__label {{ font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--p-mute); }}

    .ac-search {{ margin-bottom: 32px; }}
    .ac-search input {{ width: 100%; max-width: 480px; padding: 14px 18px; font-family: var(--f-sans); font-size: 15px; border: 1px solid rgba(16,16,16,0.2); border-radius: 4px; background: var(--p-white); color: var(--p-aztek); }}
    .ac-search input:focus {{ outline: none; border-color: var(--p-copper); }}

    .ac-section {{ background: var(--p-white); border: 1px solid rgba(16,16,16,0.08); border-radius: 6px; padding: 28px 32px; margin-bottom: 24px; }}
    .ac-section__head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 16px; margin-bottom: 6px; }}
    .ac-section__title {{ font-family: var(--f-serif-display); font-weight: 400; font-size: 28px; letter-spacing: -0.01em; color: var(--p-aztek); margin: 0; }}
    .ac-section__count {{ font-family: var(--f-serif-italic); font-style: italic; color: var(--p-copper); font-size: 14px; }}
    .ac-section__desc {{ font-size: 14px; color: var(--p-mute); margin: 0 0 16px; max-width: 70ch; }}

    .ac-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .ac-table th {{ text-align: left; font-weight: 500; font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--p-mute); padding: 10px 12px 10px 0; border-bottom: 1px solid rgba(16,16,16,0.12); }}
    .ac-cell {{ padding: 12px 12px 12px 0; border-bottom: 1px solid rgba(16,16,16,0.06); vertical-align: top; }}
    .ac-cell--id {{ width: 32%; }}
    .ac-cell--title {{ width: 42%; color: var(--p-ink); }}
    .ac-cell--size {{ width: 10%; color: var(--p-mute); font-variant-numeric: tabular-nums; }}
    .ac-cell--actions {{ width: 16%; text-align: right; }}

    code.ac-copy {{
      font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 12px;
      background: var(--p-oatmeal); padding: 4px 8px; border-radius: 3px;
      color: var(--p-aztek); cursor: pointer;
      border: 1px solid rgba(16,16,16,0.08);
      transition: background 180ms ease, border-color 180ms ease;
      user-select: all;
      display: inline-block;
    }}
    code.ac-copy:hover {{ background: var(--p-cream); border-color: var(--p-copper); }}
    code.ac-copy.is-copied {{ background: var(--p-sage); color: var(--p-white); border-color: var(--p-sage); }}

    a.ac-link {{ font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--p-aztek); text-decoration: none; font-weight: 500; }}
    a.ac-link:hover {{ color: var(--p-copper); }}

    .ac-foot {{ text-align: center; padding: 32px 0; font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--p-mute); }}

    .ac-section[hidden] {{ display: none; }}

    /* View toggle */
    .ac-toggle {{ display: inline-flex; align-items: center; gap: 0; border: 1px solid rgba(16,16,16,0.14); border-radius: 999px; padding: 3px; background: var(--p-white); }}
    .ac-toggle button {{ border: none; background: transparent; padding: 8px 16px; font-family: var(--f-sans); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 500; color: var(--p-mute); cursor: pointer; border-radius: 999px; transition: background 180ms ease, color 180ms ease; }}
    .ac-toggle button.is-active {{ background: var(--p-aztek); color: var(--p-oatmeal); }}
    .ac-toolbar {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}

    /* Views */
    .ac-view {{ display: none; }}
    body[data-view="list"] .ac-view--list {{ display: block; }}
    body[data-view="tile"] .ac-view--tile {{ display: block; }}

    /* Tile grid (compose-style) */
    .ac-tiles {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; margin-top: 4px; }}
    .ac-tile {{ position: relative; border: 1px solid rgba(16,16,16,0.10); border-radius: 8px; background: var(--p-white); overflow: hidden; display: flex; flex-direction: column; transition: border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease; }}
    .ac-tile:hover {{ border-color: var(--p-copper); transform: translateY(-2px); box-shadow: 0 10px 28px rgba(16,16,16,0.08); }}
    .ac-tile[hidden] {{ display: none; }}
    .ac-tile__thumb {{ position: relative; display: block; width: 100%; background: var(--p-oatmeal); overflow: hidden; border-bottom: 1px solid rgba(16,16,16,0.08); text-decoration: none; }}
    .ac-tile__thumb iframe {{ position: absolute; top: 0; left: 0; width: 1440px; height: 900px; max-width: none; border: 0; pointer-events: none; transform: scale(var(--ac-scale, 0.24)); transform-origin: top left; }}
    .ac-tile__hover {{ position: absolute; inset: auto 0 0 0; padding: 10px 14px; background: linear-gradient(to top, rgba(16,16,16,0.72), rgba(16,16,16,0)); color: var(--p-oatmeal); font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 500; opacity: 0; transition: opacity 180ms ease; }}
    .ac-tile__thumb:hover .ac-tile__hover {{ opacity: 1; }}
    .ac-tile__meta {{ padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 8px; }}
    .ac-tile__title {{ font-size: 12px; color: var(--p-mute); margin: 0; line-height: 1.4; }}
    code.ac-copy--tile {{ font-size: 11px; align-self: start; }}
  </style>
</head>
<body>
  <header class="ac-top">
    <h1 class="ac-top__title">All <em>Components</em></h1>
    <nav class="ac-top__nav">
      <a href="../">← Home</a>
      <a href="../components/compose/">Build a Page</a>
      <a href="../brand/">Brand System</a>
    </nav>
  </header>

  <main class="ac-layout">
    <aside class="ac-sidebar">
      <p class="ac-sidebar__h">Categories</p>
      <ul>{sidebar_html}</ul>
      <p class="ac-sidebar__h">How to use</p>
      <p style="font-size: 13px; line-height: 1.65; color: var(--p-ink); margin: 0;">
        Click any <code style="font-size: 11px; background: var(--p-oatmeal); padding: 2px 6px; border-radius: 3px;">name.variant</code> to copy it. Say to Kira "I want hero.classic-ffb-split-right-polished" and she'll know exactly which variant.
      </p>
    </aside>

    <div>
      <div class="ac-intro">
        <p>Every visual component in the brand kit, in one place. Naming convention: <code style="font-size: 12px; background: var(--p-white); padding: 3px 7px; border-radius: 3px; border: 1px solid rgba(16,16,16,0.08);">category.variant-slug</code>. Click a name to copy it, click Open to preview the live variant.</p>
        <p>Updated whenever the <code style="font-size: 12px;">components/</code> tree changes. Run <code style="font-size: 12px;">python3 scripts/generate-all-components.py</code> after adding a new variant to refresh this page.</p>
        <div class="ac-intro__stats">
          <div>
            <div class="ac-stat__num">{total_categories}</div>
            <div class="ac-stat__label">Categories</div>
          </div>
          <div>
            <div class="ac-stat__num">{total_variants}</div>
            <div class="ac-stat__label">Variants</div>
          </div>
          <div>
            <div class="ac-stat__num">{now}</div>
            <div class="ac-stat__label">Last regen</div>
          </div>
        </div>
      </div>

      <div class="ac-toolbar">
        <div class="ac-search" style="flex: 1; min-width: 280px; margin-bottom: 0;">
          <input id="ac-search-input" type="search" placeholder="Search components (e.g. hero, card-flip, ffm dark)" autocomplete="off" />
        </div>
        <div class="ac-toggle" role="group" aria-label="View mode">
          <button type="button" data-view="list" class="is-active">List</button>
          <button type="button" data-view="tile">Tile</button>
        </div>
      </div>

      {"".join(section_blocks)}

      <p class="ac-foot">Tracy Harris Co Brand Kit · generated {now}</p>
    </div>
  </main>

  <script>
    // Click-to-copy on .ac-copy nodes
    document.querySelectorAll('code.ac-copy').forEach(function (el) {{
      el.addEventListener('click', function () {{
        var text = el.getAttribute('data-copy') || el.textContent;
        if (!text) return;
        navigator.clipboard.writeText(text).then(function () {{
          el.classList.add('is-copied');
          setTimeout(function () {{ el.classList.remove('is-copied'); }}, 1400);
        }}).catch(function () {{
          // fallback: select the text
          var range = document.createRange();
          range.selectNode(el);
          window.getSelection().removeAllRanges();
          window.getSelection().addRange(range);
        }});
      }});
    }});

    // Filter rows AND tiles together
    var input = document.getElementById('ac-search-input');
    if (input) {{
      input.addEventListener('input', function () {{
        var q = input.value.trim().toLowerCase();
        document.querySelectorAll('.ac-section').forEach(function (section) {{
          var anyVisible = false;
          // Rows (list view)
          section.querySelectorAll('tbody tr').forEach(function (row) {{
            var hay = (row.getAttribute('data-search') || '').toLowerCase();
            var match = !q || hay.indexOf(q) !== -1;
            row.hidden = !match;
            if (match) anyVisible = true;
          }});
          // Tiles (tile view)
          section.querySelectorAll('.ac-tile').forEach(function (tile) {{
            var hay = (tile.getAttribute('data-search') || '').toLowerCase();
            var match = !q || hay.indexOf(q) !== -1;
            tile.hidden = !match;
          }});
          section.hidden = !anyVisible;
        }});
      }});
    }}

    // View toggle (list vs tile)
    var STORAGE_KEY = 'ac-view-mode';
    var initial = localStorage.getItem(STORAGE_KEY) || 'list';
    document.body.setAttribute('data-view', initial);
    document.querySelectorAll('.ac-toggle button').forEach(function (btn) {{
      if (btn.getAttribute('data-view') === initial) btn.classList.add('is-active');
      else btn.classList.remove('is-active');
      btn.addEventListener('click', function () {{
        var mode = btn.getAttribute('data-view');
        document.body.setAttribute('data-view', mode);
        localStorage.setItem(STORAGE_KEY, mode);
        document.querySelectorAll('.ac-toggle button').forEach(function (b) {{
          b.classList.toggle('is-active', b === btn);
        }});
        if (mode === 'tile') scaleTiles();
      }});
    }});

    // Tile iframe scaling, same pattern as compose page.
    // Iframe renders at 1440x900 desktop viewport, CSS transform-scale shrinks
    // to fit the tile. ResizeObserver updates --ac-scale per tile on resize.
    function scaleTiles() {{
      document.querySelectorAll('.ac-tile__thumb').forEach(function (thumb) {{
        var w = thumb.clientWidth;
        if (!w) return;
        var scale = w / 1440;
        thumb.style.setProperty('--ac-scale', scale.toString());
      }});
    }}
    if ('ResizeObserver' in window) {{
      var ro = new ResizeObserver(scaleTiles);
      document.querySelectorAll('.ac-tile__thumb').forEach(function (t) {{ ro.observe(t); }});
    }} else {{
      window.addEventListener('resize', scaleTiles);
    }}
    if (initial === 'tile') scaleTiles();
  </script>
</body>
</html>
'''


def main() -> int:
    sections = walk_components()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(sections), encoding='utf-8')
    total_variants = sum(len(v) for _, v in sections)
    print(f'Wrote {OUT.relative_to(ROOT)} with {len(sections)} categories, {total_variants} variants.')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
