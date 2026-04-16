---
name: build-footer
description: Generates a branded footer for Tracy Harris Co, FFB, FFM, or FRESH. Asks which brand, which variant (full / columns / minimal), signature copy, and link columns. Uses the tracy-harris-brand-kit token system.
---

# build-footer

Generate a brand-compliant footer as the last block on a page.

## When this skill runs

User asks for "a footer", "bottom of the page", or "closing section" for any of the four brands.

## Questions to ask

1. **Which brand?** tracy, ffb, ffm, fresh
2. **Which variant?** full (signature + newsletter + columns), columns (no newsletter), or minimal (logo + legal only)
3. **Signature copy?** The big serif statement. Use brand default if unsure.
4. **Newsletter?** Only if variant is "full". Heading + form action URL.
5. **Columns?** 2-4 columns, each with a title + array of links. Use brand defaults if unsure.
6. **Social?** Instagram only for Tracy brand. Confirm if the brand has others.
7. **Legal links?** Usually privacy + terms. Add press/cookie if brand has them.

## Brand defaults

### Tracy Harris Co
- Signature: "Peace, Profit and Presence."
- Variant: full (no newsletter — Tracy doesn't currently send one)
- CTA slot: "Take the Quiz" → /quiz (primary lead magnet, entry to FRESH)
- Heading: "Not sure where to start? Take the quiz."
- Columns: Programs, Resources, Connect

### FFB
- Signature: "Build a business that lets you live."
- Variant: columns (no newsletter, the program has its own opt-in)
- Columns: The program, About, Connect

### FFM
- Signature: "Intentionally small. Quietly expensive."
- Variant: full, often .footer--dark for premium charcoal feel
- Columns: The mastermind, Tracy, Connect
- Newsletter heading: "Get the Mastermind dossier."

### FRESH
- Signature: "Start with you."
- Variant: columns
- Columns: The framework, Connect

## Generation rules

1. Wrap in `<footer class="footer" data-brand="{brand}" role="contentinfo">`
2. Add `.footer--dark` class when brand is ffm and user wants the dark variant
3. Column titles are `<h2 class="footer__col-title">`
4. Use italic emphasis on key word of the signature via `<em>`
5. Never hard-code colors. Only semantic tokens.
6. Copyright line format: `© {year} Tracy Harris Co · {optional}` — current year hard-coded is fine
7. Include the ® symbol on "Freedom Filled®" everywhere it appears
8. No em dashes in copy

## Output format

Return a single `<footer>` block ready to paste. Include:
- The footer HTML
- Note on brand defaults applied
- Reminder to include `/styles/tokens.css` and `/components/footer/footer.css` on the page

## Accessibility checks

- [ ] `role="contentinfo"` on the footer element
- [ ] Column titles as `<h2>` (proper heading hierarchy)
- [ ] Every link has visible text
- [ ] Social links have `aria-label`
- [ ] No em dashes in any copy

## Related files

- `components/footer/spec.json` — machine-readable spec
- `components/footer/README.md` — intent + brand guidance
- `components/footer/footer.css` — stylesheet
- `components/footer/variants/showcase.html` — four-brand showcase
