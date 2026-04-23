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
                  <a class="ac-link" href="{html.escape(v.rel_path)}" data-ac-preview data-ac-title="{html.escape(v.title)}" data-ac-copy="{html.escape(v.copy_id)}">Open →</a>
                </td>
              </tr>
            ''')
            tiles.append(f'''
              <article class="ac-tile" data-search="{search_attr}">
                <a class="ac-tile__thumb" href="{html.escape(v.rel_path)}" data-ac-preview data-ac-title="{html.escape(v.title)}" data-ac-copy="{html.escape(v.copy_id)}" aria-label="Preview {html.escape(v.title)}" style="aspect-ratio: {aspect};">
                  <iframe loading="lazy" src="{html.escape(v.rel_path)}" title="{html.escape(v.title)}" tabindex="-1"></iframe>
                  <span class="ac-tile__hover">Preview →</span>
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
  <link rel="icon" type="image/svg+xml" href="../assets/logos/tracy/tracy-brandmark.svg" />
  <link rel="stylesheet" href="../styles/app-sidebar-mobile-fixes.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles/fonts.css" />
  <link rel="stylesheet" href="../styles/tokens.css" />
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: var(--f-sans); background: var(--p-oatmeal); color: var(--p-ink); -webkit-font-smoothing: antialiased; }}
    a {{ color: inherit; }}

    /* App sidebar (global kit nav) — duplicated inline so the page is portable. */
    :root {{
      --sidebar-width: 240px;
      --sidebar-collapsed-width: 64px;
      --sidebar-ease: cubic-bezier(0.4, 0, 0.2, 1);
    }}
    @media (min-width: 820px) {{
      body.has-sidebar {{ padding-left: var(--sidebar-width); transition: padding-left 220ms var(--sidebar-ease); }}
      body.has-sidebar.sidebar-collapsed {{ padding-left: var(--sidebar-collapsed-width); }}
    }}
    @media (prefers-reduced-motion: reduce) {{ body.has-sidebar {{ transition: none; }} }}
    .app-sidebar {{ position: fixed; top: 0; left: 0; bottom: 0; width: var(--sidebar-width); background: var(--p-oatmeal); border-right: 1px solid var(--border-hairline); display: flex; flex-direction: column; z-index: 60; transition: width 220ms var(--sidebar-ease); font-family: var(--f-sans); overflow: hidden; }}
    body.sidebar-collapsed .app-sidebar {{ width: var(--sidebar-collapsed-width); }}
    @media (prefers-reduced-motion: reduce) {{ .app-sidebar {{ transition: none; }} }}
    .app-sidebar__top {{ padding: 24px; display: flex; flex-direction: column; gap: 6px; border-bottom: 1px solid var(--border-hairline); min-height: 92px; }}
    body.sidebar-collapsed .app-sidebar__top {{ padding: 20px 12px; align-items: center; }}
    .app-sidebar__mark {{ display: block; color: var(--p-charcoal); text-decoration: none; line-height: 0; }}
    .app-sidebar__mark svg {{ display: block; height: 22px; width: auto; fill: currentColor; }}
    body.sidebar-collapsed .app-sidebar__mark svg {{ height: 28px; }}
    .app-sidebar__eyebrow {{ font-family: var(--f-sans); font-size: 10px; font-weight: 500; letter-spacing: 0.28em; text-transform: uppercase; color: var(--p-sage); margin: 0; }}
    body.sidebar-collapsed .app-sidebar__eyebrow {{ display: none; }}
    .app-sidebar__nav {{ list-style: none; padding: 12px 0; margin: 0; display: flex; flex-direction: column; gap: 2px; }}
    .app-sidebar__link {{ position: relative; display: flex; align-items: center; gap: 14px; padding: 16px 24px; font-family: var(--f-sans); font-size: 13px; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--p-charcoal); text-decoration: none; opacity: 0.72; transition: opacity 180ms ease, background-color 180ms ease; white-space: nowrap; border-left: 3px solid transparent; }}
    .app-sidebar__link:hover {{ opacity: 1; background: var(--p-cream); }}
    .app-sidebar__link:focus-visible {{ outline: 2px solid var(--p-aztek); outline-offset: -2px; }}
    .app-sidebar__link.is-active {{ opacity: 1; border-left-color: var(--p-sage); font-weight: 600; }}
    .app-sidebar__icon {{ flex: 0 0 20px; width: 20px; height: 20px; display: inline-flex; align-items: center; justify-content: center; color: currentColor; }}
    .app-sidebar__icon svg {{ width: 20px; height: 20px; display: block; }}
    .app-sidebar__label {{ flex: 1; }}
    body.sidebar-collapsed .app-sidebar__link {{ padding: 16px 0; justify-content: center; gap: 0; }}
    body.sidebar-collapsed .app-sidebar__label {{ display: none; }}
    body.sidebar-collapsed .app-sidebar__link {{ border-left-width: 0; border-right: 3px solid transparent; }}
    body.sidebar-collapsed .app-sidebar__link.is-active {{ border-right-color: var(--p-sage); border-left-color: transparent; }}
    .app-sidebar__bottom {{ margin-top: auto; padding: 16px 24px 20px; border-top: 1px solid var(--border-hairline); display: flex; flex-direction: column; gap: 8px; }}
    body.sidebar-collapsed .app-sidebar__bottom {{ padding: 16px 12px 20px; align-items: center; }}
    .app-sidebar__toggle {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 36px; width: 100%; padding: 0 14px; background: transparent; border: 1px solid var(--p-sage); border-radius: var(--r-pill); color: var(--p-aztek); font-family: var(--f-sans); font-size: 11px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; cursor: pointer; transition: background 180ms ease, color 180ms ease; }}
    .app-sidebar__toggle:hover {{ background: var(--p-sage); color: var(--p-white); }}
    .app-sidebar__toggle:focus-visible {{ outline: 2px solid var(--p-aztek); outline-offset: 2px; }}
    body.sidebar-collapsed .app-sidebar__toggle {{ width: 40px; padding: 0; }}
    body.sidebar-collapsed .app-sidebar__toggle-label {{ display: none; }}
    .app-sidebar__footer {{ font-size: 10px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--ink-mute); margin: 0; text-align: center; opacity: 0.72; }}
    body.sidebar-collapsed .app-sidebar__footer {{ display: none; }}
    .app-sidebar__hamburger {{ position: fixed; top: 16px; left: 16px; width: 48px; height: 48px; border-radius: var(--r-pill); border: 1px solid var(--border-hairline); background: var(--p-oatmeal); color: var(--p-charcoal); display: none; align-items: center; justify-content: center; cursor: pointer; z-index: 70; box-shadow: 0 2px 8px rgba(16,16,16,0.06); }}
    .app-sidebar__hamburger:focus-visible {{ outline: 2px solid var(--p-aztek); outline-offset: 2px; }}
    .app-sidebar__hamburger svg {{ width: 20px; height: 20px; }}
    @media (max-width: 819px) {{
      .app-sidebar {{ width: 100%; max-width: 420px; transform: translateX(-100%); transition: transform 260ms var(--sidebar-ease); border-right: none; box-shadow: 18px 0 40px rgba(16,16,16,0.12); }}
      body.sidebar-mobile-open .app-sidebar {{ transform: translateX(0); }}
      .app-sidebar__hamburger {{ display: inline-flex; }}
      body.has-sidebar {{ padding-left: 0; }}
      body.sidebar-mobile-open {{ overflow: hidden; }}
      .app-sidebar__top {{ padding: 28px 28px 20px; min-height: 0; }}
      .app-sidebar__nav {{ padding: 20px 0; gap: 4px; }}
      .app-sidebar__link {{ font-family: var(--f-serif-display); font-size: clamp(28px, 7vw, 40px); font-weight: 400; letter-spacing: -0.01em; text-transform: none; padding: 10px 28px; opacity: 0.9; border-left: none; color: var(--p-charcoal); }}
      .app-sidebar__link:hover {{ background: transparent; opacity: 1; }}
      .app-sidebar__link.is-active {{ font-weight: 400; color: var(--p-aztek); border-left: none; }}
      .app-sidebar__link.is-active::after {{ content: ""; display: inline-block; width: 8px; height: 8px; margin-left: 12px; background: var(--p-sage); border-radius: 50%; vertical-align: middle; }}
      .app-sidebar__icon {{ display: none; }}
      .app-sidebar__bottom {{ padding: 20px 28px 28px; }}
      .app-sidebar__toggle {{ display: none; }}
      .app-sidebar__footer {{ text-align: left; opacity: 0.72; }}
      .app-sidebar__close {{ position: absolute; top: 14px; right: 14px; width: 44px; height: 44px; border: none; background: transparent; color: var(--p-charcoal); cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }}
      .app-sidebar__close svg {{ width: 20px; height: 20px; }}
      .app-sidebar__backdrop {{ position: fixed; inset: 0; background: rgba(16,16,16,0.32); opacity: 0; pointer-events: none; transition: opacity 260ms ease; z-index: 55; }}
      body.sidebar-mobile-open .app-sidebar__backdrop {{ opacity: 1; pointer-events: auto; }}
    }}
    @media (min-width: 820px) {{ .app-sidebar__close, .app-sidebar__backdrop, .app-sidebar__hamburger {{ display: none !important; }} }}
    @media (prefers-reduced-motion: reduce) {{ .app-sidebar, .app-sidebar__backdrop {{ transition: none; }} }}

    .ac-top {{
      display: flex; justify-content: space-between; align-items: baseline;
      padding: 20px clamp(24px, 5vw, 64px);
      border-bottom: 1px solid rgba(16,16,16,0.08);
      background: var(--p-oatmeal);
      position: fixed; top: 0; left: 0; right: 0; z-index: 20;
      height: 72px;
    }}
    @media (min-width: 820px) {{
      body.has-sidebar .ac-top {{ left: var(--sidebar-width); }}
      body.has-sidebar.sidebar-collapsed .ac-top {{ left: var(--sidebar-collapsed-width); }}
    }}
    @media (max-width: 819px) {{
      .ac-top {{ padding-left: 76px; }}  /* room for hamburger (48px + breathing) */
      .ac-top__title {{ font-size: 22px !important; }}
      .ac-top__nav {{ display: none; }}  /* nav lives in the sidebar on mobile */
    }}
    body.has-sidebar {{ padding-top: 72px; }}
    .ac-top a {{ font-size: 13px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--p-aztek); text-decoration: none; margin-left: 20px; }}
    .ac-top a:hover {{ color: var(--p-copper); }}
    .ac-top__title {{ font-family: var(--f-serif-display); font-size: clamp(24px, 2.4vw, 32px); color: var(--p-aztek); margin: 0; letter-spacing: -0.015em; }}
    .ac-top__title em {{ font-family: var(--f-serif-italic); font-style: italic; color: var(--p-copper); }}
    .ac-top__nav {{ font-size: 12px; }}

    .ac-layout {{ padding: 48px clamp(24px, 5vw, 64px); max-width: 1480px; margin: 0 auto; position: relative; }}
    .ac-main {{ /* main content column */ }}
    @media (min-width: 901px) {{
      .ac-main {{ margin-left: 308px; }}  /* sidebar 260 + gap 48 */
    }}

    /* In-page category sidebar — FIXED on desktop so it stays visible at every
       scroll position regardless of grid/flex quirks. left position is set by
       JS so it aligns with the layout's left padding and adapts when the
       app-sidebar collapses. */
    @media (min-width: 901px) {{
      .ac-sidebar {{
        position: fixed;
        top: 96px;  /* 72 header + 24 breathing room */
        width: 260px;
        max-height: calc(100vh - 116px);
        overflow: hidden;
        z-index: 5;
      }}
    }}
    @media (max-width: 900px) {{
      .ac-sidebar {{ position: static; max-height: none; overflow: visible; margin-bottom: 24px; }}
    }}
    .ac-sidebar__h {{ font-size: 10px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--p-mute); margin: 0 0 8px; font-weight: 500; }}
    .ac-sidebar ul {{ list-style: none; padding: 0; margin: 0 0 14px; }}
    .ac-sidebar li {{ margin: 0; }}
    .ac-sidebar a {{ display: flex; justify-content: space-between; align-items: baseline; padding: 4px 0; font-size: 12px; line-height: 1.35; color: var(--p-aztek); text-decoration: none; border-bottom: 1px solid rgba(16,16,16,0.05); transition: color 180ms ease, border-color 180ms ease; }}
    .ac-sidebar a:hover {{ color: var(--p-copper); border-color: rgba(173,118,91,0.4); }}
    .ac-count {{ font-family: var(--f-serif-display); font-style: italic; color: var(--p-copper); font-size: 11px; }}

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

    /* Preview modal (dialog) */
    dialog.ac-modal {{
      border: none; padding: 0; border-radius: 10px; background: var(--p-white);
      width: min(92vw, 1360px); max-width: 92vw;
      height: min(88vh, 900px); max-height: 88vh;
      overflow: hidden; box-shadow: 0 28px 80px rgba(16,16,16,0.32);
    }}
    dialog.ac-modal::backdrop {{ background: rgba(16,16,16,0.56); backdrop-filter: blur(2px); }}
    .ac-modal__frame {{ display: flex; flex-direction: column; height: 100%; }}
    .ac-modal__head {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px 20px; border-bottom: 1px solid rgba(16,16,16,0.08); flex-shrink: 0; }}
    .ac-modal__title {{ font-family: var(--f-serif-display); font-size: 20px; letter-spacing: -0.01em; color: var(--p-aztek); margin: 0; line-height: 1.2; }}
    .ac-modal__meta {{ display: flex; align-items: center; gap: 12px; }}
    .ac-modal__meta a {{ font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--p-aztek); text-decoration: none; font-weight: 500; }}
    .ac-modal__meta a:hover {{ color: var(--p-copper); }}
    .ac-modal__close {{ background: transparent; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; color: var(--p-aztek); font-size: 24px; line-height: 1; }}
    .ac-modal__close:hover {{ background: var(--p-oatmeal); }}
    .ac-modal__body {{ flex: 1; overflow: hidden; position: relative; background: var(--p-oatmeal); }}
    .ac-modal__body iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; background: var(--p-white); max-width: none; }}
    @media (max-width: 640px) {{ dialog.ac-modal {{ width: 100vw; max-width: 100vw; height: 100vh; max-height: 100vh; border-radius: 0; }} }}

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
<body data-brand="tracy">

  <!-- APP SIDEBAR (shared global kit nav) -->
  <button type="button" class="app-sidebar__hamburger" id="appSidebarHamburger" aria-label="Open navigation" aria-controls="appSidebar" aria-expanded="false">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
  </button>
  <div class="app-sidebar__backdrop" id="appSidebarBackdrop" aria-hidden="true"></div>
  <aside class="app-sidebar" id="appSidebar" role="navigation" aria-label="Brand kit">
    <button type="button" class="app-sidebar__close" id="appSidebarClose" aria-label="Close navigation">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
    </button>
    <div class="app-sidebar__top">
      <a href="../" class="app-sidebar__mark" aria-label="Tracy Harris Co">
        <svg class="app-sidebar__mark-wordmark" viewBox="0 0 951.88 385.78" aria-hidden="true">
          <g>
            <path d="M0,68.37V9.26L55.14,0v68.37h52.49l-1.77,7.5h-50.72v131.45c0,24.7,10.59,37.49,32.64,37.49,12.79,0,22.5-8.82,26.47-15.44l6.62,3.97c-8.82,20.73-35.73,42.79-65.28,42.79-34.85,0-55.58-14.12-55.58-67.49V68.37Z"/>
            <path d="M296.86,72.34c13.67,11.91,15,33.08,3.09,46.32-11.91,13.67-32.2,15.44-46.31,3.53-6.62-6.18-10.15-13.67-10.15-21.61,0-4.85-18.08-.44-34.4,26.03v91.75c0,24.7,2.21,41.9,18.08,46.32v7.5h-91.31v-7.5c17.2-5.29,17.64-23.38,17.64-46.32v-97.92c0-15-3.97-21.61-22.06-30.88v-7.5l77.63-17.64v49.84c23.38-36.61,41.46-43.23,52.05-47.64,9.26-3.97,26.02-2.21,35.73,5.73Z"/>
            <path d="M514.31,241.72l7.5,3.09c-3.53,14.12-23.82,31.32-51.61,31.32,0,0-39.26,0-44.11-35.73-6.62,19.41-32.64,35.73-63.96,35.73,0,0-50.73,0-50.73-44.99,0-48.08,37.05-52.49,114.25-71.9v-27.35c0-45.87-25.58-68.81-56.02-52.93-14.12,7.06-15.88,14.56-12.79,15,6.62.88,12.35,3.97,16.32,9.7,7.94,11.47,4.85,26.91-6.62,34.85-11.47,7.5-26.91,4.85-34.85-6.62-5.29-8.38-5.73-18.97-1.32-26.47,4.41-7.5,10.15-19.41,34.41-32.2,19.85-10.59,42.79-8.82,42.79-8.82,57.78,0,73.66,36.17,73.66,88.22v65.72s-.44,30.88,21.17,30.88c0,0,9.26,0,11.91-7.5ZM425.65,167.18c-43.23,9.7-57.78,30.44-57.78,52.93,0,0,0,29.11,28.67,29.11,15,0,25.14-11.91,29.11-22.5v-59.55Z"/>
            <path d="M712.81,219.23c-6.18,22.5-32.64,56.9-87.78,56.9s-97.04-55.14-97.04-106.75,38.82-104.98,114.24-104.98c31.32,0,50.29,12.79,57.78,19.41,7.5,6.62,11.91,18.97,8.82,29.55-4.41,15.44-20.29,25.58-36.17,21.17-15.88-3.97-25.14-20.29-20.73-35.73,1.77-8.38,7.06-14.12,13.67-17.64,3.97-1.76-5.73-9.26-23.38-9.26-15.88,0-58.67,13.67-58.67,89.54,0,47.64,25.58,68.81,56.02,75.43,22.06,4.85,56.9-7.06,67.05-21.61l6.18,3.97Z"/>
            <path d="M951.88,68.37v7.5c-9.26,0-29.55.88-57.78,68.81l-67.49,177.76c-11.47,30-24.7,42.35-33.08,48.96-7.94,6.62-23.38,9.26-33.97,4.41-15.44-7.06-22.05-25.14-15.44-40.58,7.06-15.44,25.14-22.5,40.58-15.44,7.94,3.53,12.79,10.59,15,18.08,1.77,5.29,12.35,2.21,19.41-16.32l16.76-45.43c-27.35-63.08-83.37-183.06-83.37-183.06-7.06-17.2-21.17-17.2-27.79-17.2v-7.5h104.1v7.5c-22.93,0-11.47,26.91-11.47,26.91l46.76,99.69,23.38-59.55s29.11-67.49-22.05-67.05v-7.5h86.45Z"/>
            <circle cx="913.63" cy="254.68" r="21.87"/>
          </g>
        </svg>
        <svg class="app-sidebar__mark-brandmark" viewBox="0 0 263.98 382.72" aria-hidden="true" style="display:none;">
          <path d="M0,94.76V12.84L76.42,0v94.76h72.75l-2.45,10.39h-70.3v182.19c0,34.24,14.67,51.97,45.24,51.97,17.73,0,31.18-12.23,36.68-21.4l9.17,5.5c-12.23,28.73-49.52,59.3-90.48,59.3-48.3,0-77.03-19.56-77.03-93.54V94.76Z"/>
          <circle cx="233.68" cy="352.41" r="30.31"/>
        </svg>
      </a>
      <p class="app-sidebar__eyebrow">Brand Kit</p>
    </div>
    <ul class="app-sidebar__nav" id="appSidebarNav">
      <li><a class="app-sidebar__link" data-nav="catalog" href="../">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="4" height="4"/><rect x="8" y="2.5" width="4" height="4"/><rect x="13.5" y="2.5" width="4" height="4"/><rect x="2.5" y="8" width="4" height="4"/><rect x="8" y="8" width="4" height="4"/><rect x="13.5" y="8" width="4" height="4"/><rect x="2.5" y="13.5" width="4" height="4"/><rect x="8" y="13.5" width="4" height="4"/><rect x="13.5" y="13.5" width="4" height="4"/></svg></span>
        <span class="app-sidebar__label">Catalog</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="brand" href="../brand/">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7.5"/><path d="M10 2.5v15M2.5 10h15"/></svg></span>
        <span class="app-sidebar__label">Brand at a glance</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="compose" href="../components/compose/">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7.5"/><line x1="10" y1="6.5" x2="10" y2="13.5"/><line x1="6.5" y1="10" x2="13.5" y2="10"/></svg></span>
        <span class="app-sidebar__label">Build a page</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="all-components" href="all-components.html">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="5" x2="16" y2="5"/><line x1="4" y1="10" x2="16" y2="10"/><line x1="4" y1="15" x2="16" y2="15"/><circle cx="2.5" cy="5" r="0.6" fill="currentColor" stroke="none"/><circle cx="2.5" cy="10" r="0.6" fill="currentColor" stroke="none"/><circle cx="2.5" cy="15" r="0.6" fill="currentColor" stroke="none"/></svg></span>
        <span class="app-sidebar__label">All components</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="review" href="../components/review/">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="15" height="15" rx="2"/><polyline points="6.5 10.5 9 13 14 7.5"/></svg></span>
        <span class="app-sidebar__label">Review variants</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="pages" href="../pages/">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2.5" width="11" height="13" rx="1"/><path d="M3.5 5v11a1 1 0 0 0 1 1h10"/></svg></span>
        <span class="app-sidebar__label">Pages</span>
      </a></li>
      <li><a class="app-sidebar__link" data-nav="docs" href="../docs/">
        <span class="app-sidebar__icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3.5h9a2.5 2.5 0 0 1 2.5 2.5v11.5H6.5A2.5 2.5 0 0 1 4 15V3.5z"/><line x1="4" y1="15" x2="15.5" y2="15"/><line x1="7" y1="7" x2="12.5" y2="7"/><line x1="7" y1="10" x2="12.5" y2="10"/></svg></span>
        <span class="app-sidebar__label">Docs</span>
      </a></li>
    </ul>
    <div class="app-sidebar__bottom">
      <button type="button" class="app-sidebar__toggle" id="appSidebarToggle" aria-expanded="true" aria-controls="appSidebar">
        <span class="app-sidebar__toggle-label" id="appSidebarToggleLabel">Collapse</span>
        <span aria-hidden="true" id="appSidebarToggleGlyph">&lsaquo;</span>
      </button>
      <p class="app-sidebar__footer">v1.2 · 2026</p>
    </div>
  </aside>
  <!-- /APP SIDEBAR -->

  <header class="ac-top">
    <h1 class="ac-top__title">All <em>Components</em></h1>
    <nav class="ac-top__nav">
      <a href="../components/compose/">Build a Page</a>
      <a href="../brand/">Brand System</a>
    </nav>
  </header>

  <main class="ac-layout">
    <aside class="ac-sidebar">
      <p class="ac-sidebar__h">Categories</p>
      <ul>{sidebar_html}</ul>
    </aside>

    <div class="ac-main">
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

  <!-- Preview modal -->
  <dialog class="ac-modal" id="ac-preview">
    <div class="ac-modal__frame">
      <header class="ac-modal__head">
        <h2 class="ac-modal__title" id="ac-preview-title">Preview</h2>
        <div class="ac-modal__meta">
          <code class="ac-copy" id="ac-preview-copy" data-copy=""></code>
          <a id="ac-preview-open" href="#" target="_blank" rel="noopener">Open full page ↗</a>
          <button class="ac-modal__close" id="ac-preview-close" type="button" aria-label="Close preview">&times;</button>
        </div>
      </header>
      <div class="ac-modal__body">
        <iframe id="ac-preview-iframe" src="about:blank" title="Variant preview"></iframe>
      </div>
    </div>
  </dialog>

  <script>
    // Position the fixed category sidebar so it aligns with layout left padding.
    // Re-runs on resize and after app-sidebar state changes. Must run AFTER
    // body gets has-sidebar class, otherwise layout.left is wrong on first paint.
    function positionCategorySidebar() {{
      var layout = document.querySelector('.ac-layout');
      var sidebar = document.querySelector('.ac-sidebar');
      if (!layout || !sidebar) return;
      if (window.innerWidth < 901) {{ sidebar.style.left = ''; return; }}
      var rect = layout.getBoundingClientRect();
      var pad = parseFloat(getComputedStyle(layout).paddingLeft) || 0;
      sidebar.style.left = (rect.left + pad) + 'px';
    }}
    window.addEventListener('resize', positionCategorySidebar);

    // App sidebar init
    (function () {{
      var body = document.body;
      body.classList.add('has-sidebar');
      var LS_KEY = 'thc-sidebar-collapsed';
      var initialCollapsed = false;
      try {{ initialCollapsed = localStorage.getItem(LS_KEY) === 'true'; }} catch (e) {{}}
      if (initialCollapsed) body.classList.add('sidebar-collapsed');
      var toggle = document.getElementById('appSidebarToggle');
      var toggleLabel = document.getElementById('appSidebarToggleLabel');
      var toggleGlyph = document.getElementById('appSidebarToggleGlyph');
      var wordmark = document.querySelector('.app-sidebar__mark-wordmark');
      var brandmark = document.querySelector('.app-sidebar__mark-brandmark');
      function syncCollapsedUI() {{
        var collapsed = body.classList.contains('sidebar-collapsed');
        if (toggle) toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        if (toggleLabel) toggleLabel.textContent = collapsed ? '' : 'Collapse';
        if (toggleGlyph) toggleGlyph.textContent = collapsed ? '\u203A' : '\u2039';
        if (wordmark && brandmark) {{
          wordmark.style.display = collapsed ? 'none' : 'block';
          brandmark.style.display = collapsed ? 'block' : 'none';
        }}
      }}
      syncCollapsedUI();
      if (toggle) {{
        toggle.addEventListener('click', function () {{
          body.classList.toggle('sidebar-collapsed');
          var collapsed = body.classList.contains('sidebar-collapsed');
          try {{ localStorage.setItem(LS_KEY, collapsed ? 'true' : 'false'); }} catch (e) {{}}
          syncCollapsedUI();
          // App-sidebar width change shifts the layout, re-position category sidebar after transition
          setTimeout(positionCategorySidebar, 240);
        }});
      }}
      // Re-position category sidebar once the collapsed state is loaded (body padding updates)
      requestAnimationFrame(positionCategorySidebar);
      // Active state: this page is all-components
      var links = document.querySelectorAll('.app-sidebar__link');
      for (var i = 0; i < links.length; i++) {{
        if (links[i].getAttribute('data-nav') === 'all-components') {{
          links[i].classList.add('is-active');
          links[i].setAttribute('aria-current', 'page');
        }}
      }}
      var hamburger = document.getElementById('appSidebarHamburger');
      var closeBtn = document.getElementById('appSidebarClose');
      var backdrop = document.getElementById('appSidebarBackdrop');
      function openMobile() {{ body.classList.add('sidebar-mobile-open'); if (hamburger) hamburger.setAttribute('aria-expanded', 'true'); }}
      function closeMobile() {{ body.classList.remove('sidebar-mobile-open'); if (hamburger) hamburger.setAttribute('aria-expanded', 'false'); }}
      if (hamburger) hamburger.addEventListener('click', openMobile);
      if (closeBtn) closeBtn.addEventListener('click', closeMobile);
      if (backdrop) backdrop.addEventListener('click', closeMobile);
      document.addEventListener('keydown', function (e) {{
        if (e.key === 'Escape' && body.classList.contains('sidebar-mobile-open')) closeMobile();
      }});
    }})();

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

    // Preview modal: intercept any link with data-ac-preview, open in <dialog>
    var modal = document.getElementById('ac-preview');
    var modalTitle = document.getElementById('ac-preview-title');
    var modalCopy = document.getElementById('ac-preview-copy');
    var modalOpen = document.getElementById('ac-preview-open');
    var modalIframe = document.getElementById('ac-preview-iframe');
    var modalClose = document.getElementById('ac-preview-close');
    document.addEventListener('click', function (e) {{
      var link = e.target.closest('[data-ac-preview]');
      if (!link) return;
      e.preventDefault();
      var href = link.getAttribute('href');
      var title = link.getAttribute('data-ac-title') || '';
      var copy = link.getAttribute('data-ac-copy') || '';
      if (modalTitle) modalTitle.textContent = title;
      if (modalCopy) {{ modalCopy.textContent = copy; modalCopy.setAttribute('data-copy', copy); }}
      if (modalOpen) modalOpen.href = href;
      if (modalIframe) modalIframe.src = href;
      if (typeof modal.showModal === 'function') modal.showModal();
      else window.open(href, '_blank', 'noopener');
    }});
    if (modalClose) modalClose.addEventListener('click', function () {{ modal.close(); }});
    modal.addEventListener('close', function () {{ if (modalIframe) modalIframe.src = 'about:blank'; }});
    modal.addEventListener('click', function (e) {{
      // Close on backdrop click, but not when clicking inside the frame
      if (e.target === modal) modal.close();
    }});
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
