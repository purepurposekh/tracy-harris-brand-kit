---
name: build-cta-block
description: Generates a mid-page CTA block. Five variants: canvas (light), elevated (oatmeal), accent (brand color), dark (inverse), ruled (minimal with borders).
---

# build-cta-block

Generate a call-to-action interrupt block.

## Questions (only if genuinely unclear)

1. **Variant?** canvas, elevated, accent, dark, ruled
2. **Which brand?** tracy, ffb, ffm, fresh
3. **CTA?** Default: Tracy = Take the Quiz, FFB = Apply to FFB, FFM = Apply to FFM

## Generation rules

1. Section: `<section class="cta-block cta-block--{variant}" data-brand="{brand}">`
2. Inner: `<div class="cta-block__inner">` centered
3. Elements: eyebrow (optional), title with italic emphasis, body (optional), actions
4. Buttons: `cta-block__btn--primary` (filled) + optional `--secondary` (outlined)
5. Accent/dark variants invert button colors automatically
6. Use `cta-block__script` class for Jhon Halend script accent words
