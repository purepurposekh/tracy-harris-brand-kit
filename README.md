# tracy-harris-brand-kit

Brand system for Tracy Harris Co, FFB, FFM, and FRESH.

## Preview

Open `components/hero/variants/showcase.html` in a browser. Four brands, one component, side-by-side.

## Structure

- `tokens/`, design tokens (primitives + per-brand semantic mappings)
- `styles/tokens.css`, CSS custom properties with `[data-brand]` scoping
- `components/`, one folder per component (hero, cta, footer, etc.)
- `.claude/skills/`, invocable skills for generating branded sections
- `assets/`, logos, fonts (add as delivered)

## Using it

### From Claude Code (Karl)
Invoke `/build-hero-section` in any session. The skill asks which brand, layout, copy, and CTA, then generates a brand-compliant HTML block.

### From Cowork (designer / Tracy)
Open this folder in Cowork. Ask: "build an FFM hero with title 'Apply for the 2026 cohort'". Skill loads and walks through the questions.

### From Claude.ai web
Zip `.claude/skills/build-hero-section/`, upload via Settings > Features > Skills. Works the same as CLI but outputs HTML in chat.

## Adding a component

See `AGENTS.md` for the pattern.

## The four brands

| Brand | Canvas | Primary | Voice |
|---|---|---|---|
| Tracy Harris Co | white | dark green (AZTEK) | editorial, grounded |
| FFB | oatmeal | dark teal + sage | mentorship, warm |
| FFM | oatmeal / charcoal | gold gradient | premium, application-based |
| FRESH | oatmeal | navy + 5 pillars | framework-led, human |

## Source of truth

- Brand guidelines PDF (archived): see commit history
- Live FFM page: https://freedom.tracyharris.co/ffm-2026
- Live FFB components: referenced from tracy-harris-co repo
