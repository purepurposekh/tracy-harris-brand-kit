---
name: build-hero-section
description: Generates a branded hero section for Tracy Harris Co, FFB, FFM, or FRESH. Always asks which brand + layout + CTA + copy before generating. Uses the tracy-harris-brand-kit token system — never hard-codes colors or fonts.
---

# build-hero-section

Generate a brand-compliant hero section as the first block of a landing page.

## When this skill runs

The user asks for "a hero", "the first section", "the above-the-fold", or "the top of a landing page" for any of the four brands.

## Required questions to ask the user

Before generating, ask in one short message:

1. **Which brand?** — Tracy Harris Co (parent), FFB, FFM, or FRESH
2. **Which layout?** — splitRight (image right), splitLeft (image left), textOnly (no image), or stacked (image on top)
3. **Title copy?** — 4-8 words, the single biggest line on the page. Italic emphasis on a phrase using `<em>`.
4. **Supporting copy?** — one sentence, 15-30 words. Who it's for + what they get.
5. **Primary CTA?** — button label + href. (If unsure, see brand defaults below.)
6. **Secondary CTA?** — optional. Label + href or skip.
7. **Image?** — path to file or Unsplash URL. Skip for textOnly.
8. **Eyebrow?** — optional short label above the title. Usually the product name.

If the user only gives partial info, generate with sensible brand defaults and list what you assumed.

## Brand defaults (if user doesn't specify)

### Tracy Harris Co
- Layout: textOnly
- Eyebrow: "Tracy Harris Co"
- CTA: "Explore the programs"
- Tone: editorial, grounded

### FFB (Freedom Filled® Business)
- Layout: splitRight
- Eyebrow: "Freedom Filled® Business"
- CTA: "Apply for FFB"
- Tone: warm, mentorship-led

### FFM (Freedom Filled® Mastermind)
- Layout: splitLeft
- Eyebrow: "Freedom Filled® Mastermind"
- CTA: "Apply for the Mastermind"  (NEVER "Buy" or "Enrol")
- Tone: intimate, premium

### FRESH (FRESH Framework™)
- Layout: splitRight
- Eyebrow: "The FRESH Framework™"
- CTA: "Take the Quiz"
- Include the 5-pillar dots after the actions block
- Tone: grounded, multi-dimensional

## Generation rules

1. **Never hard-code colors or fonts.** Always use semantic CSS custom properties (`var(--accent)`, `var(--ink-heading)`, etc.) defined in `styles/tokens.css`.
2. **Set the brand on the section element,** not the body: `<section class="hero hero--{layout}" data-brand="{brand}">`.
3. **Title is always `<h1>`** and always uses `.hero__title` class.
4. **Italic emphasis** uses `<em>` inside the title, which the CSS styles with the italic serif.
5. **CTA language** follows brand rules. For FFM, refuse to use "Buy", "Enrol now", or "Add to cart" — offer the user the correct application-based alternative.
6. **Em dashes are banned** in all generated copy. Use commas or full stops.
7. **Alt text is required** on images. If the user doesn't provide, write a descriptive alt based on the image context.
8. **® symbol** must appear on Freedom Filled — never "Freedom Filled" without the ® in product names.

## Output format

Return a single HTML `<section>` block, ready to paste into a page. Include:
- The section HTML
- A note listing which tokens it uses (`--accent`, `--surface-canvas`, etc.)
- A note on any brand defaults applied because the user didn't specify

Do NOT generate a full `<html>` document — heroes are page fragments, not pages.

If the user wants a standalone preview page, wrap the section in a minimal HTML doc that links `../../../styles/tokens.css` and `../hero.css`. Use `showcase.html` as the reference template.

## Accessibility checks before returning

- [ ] Title is an `<h1>`, not a `<div>` or `<h2>`
- [ ] Image has `alt` text (or is decorative with `alt=""`)
- [ ] CTA contrast: for FFM gold gradient, verify text colour is `--accent-on` (oatmeal)
- [ ] No em dashes in any user-facing copy
- [ ] `data-brand` attribute is set

## Related files

- `components/hero/spec.json` — machine-readable spec (slots, variants, validation rules)
- `components/hero/README.md` — intent-first human docs
- `components/hero/hero.css` — stylesheet (reference only, don't duplicate styles inline)
- `components/hero/variants/showcase.html` — four-brand showcase for reference
- `tokens/brands/{brand}.json` — the token map for the chosen brand
- `styles/tokens.css` — CSS custom properties layer
