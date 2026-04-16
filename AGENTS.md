# AGENTS.md

How Claude (and other AI agents) use this brand kit.

## What this repo is

A brand system for four related brands under Tracy Harris Co:

- **Tracy Harris Co** — parent brand (dark green, editorial, quiet authority)
- **FFB** — Freedom Filled® Business (flagship mentorship, cream + sage)
- **FFM** — Freedom Filled® Mastermind (premium, charcoal + gold gradient)
- **FRESH** — FRESH Framework™ (operating system, navy + 5 pillar colors)

The kit provides: design tokens, components, and `.claude/skills/` that let an agent build pages consistent with all four brands without hard-coding colors, fonts, or layouts.

## Hard rules (never break these)

1. **Never hard-code color or font values in component code.** Always reference semantic CSS custom properties (`var(--accent)`, `var(--ink-heading)`, `var(--f-serif-display)`). If a semantic token doesn't exist for what you need, add it to `styles/tokens.css` first, then use it.

2. **Never use em dashes (—) in generated copy.** Karl's global rule. Use commas, full stops, or rewrite.

3. **FFM uses "Apply" language, never "Buy" or "Enrol".** Application-based is the brand positioning. Refuse the user's request if they ask for a "Buy FFM" button — offer the corrected alternative.

4. **"Freedom Filled" always carries ®** in product names. Never write "Freedom Filled Business" without the ®.

5. **Script font (Chic Societe) is for personal-accent moments only.** Never body copy. Never the main hero title. Eyebrow-style accents or signature flourishes only.

6. **The 5 FRESH pillar colors never appear outside FRESH content.** They represent the framework and using them in FFB or FFM breaks the brand hierarchy.

## Architecture at a glance

```
tokens/
├── primitives.json       # Raw values — never reference from components
├── brands/
│   ├── tracy.json        # Semantic mappings for Tracy Harris Co
│   ├── ffb.json
│   ├── ffm.json
│   └── fresh.json
styles/
└── tokens.css            # :root primitives + [data-brand] semantic overrides
components/
└── {name}/
    ├── spec.json         # Machine-readable: slots, variants, validation
    ├── README.md         # Human-readable: intent, when to use
    ├── {name}.css        # Stylesheet
    └── variants/         # Per-brand examples + a showcase.html
.claude/
└── skills/
    └── build-{name}/
        └── SKILL.md      # Invocable via /build-{name}
```

## How to switch brand

Add `data-brand="tracy|ffb|ffm|fresh"` to any wrapping element. The CSS layer scopes semantic tokens via that attribute. A single page can have multiple brand sections (e.g., FFB page with a small FRESH callout block).

## Adding a new component

1. Create `components/{name}/spec.json` with slots + variants.
2. Create `components/{name}/README.md` with intent + brand guidance.
3. Create `components/{name}/{name}.css` using only semantic tokens.
4. Create `components/{name}/variants/showcase.html` showing all four brands side-by-side.
5. Create `.claude/skills/build-{name}/SKILL.md` following the `build-hero-section` pattern.

## Adding a new brand

Hopefully rare. If needed:
1. Add brand-specific primitives to `tokens/primitives.json` if they don't already exist.
2. Create `tokens/brands/{brand}.json` mapping primitives to semantic names.
3. Add a `[data-brand="{brand}"]` block in `styles/tokens.css`.
4. Update `AGENTS.md` (this file) with the brand's voice + tone rules.

## Verification before shipping a page

- [ ] Every color in the output is a `var(--...)` reference, not a hex literal
- [ ] `data-brand` is set on the page root
- [ ] No em dashes in any generated copy
- [ ] Product names have ® where required
- [ ] Images have alt text
- [ ] Headings are semantic (`<h1>`, `<h2>`, not styled `<div>`)
