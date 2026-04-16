---
name: build-opt-in
description: Generates an email opt-in section. Three variants: split (portrait + form), banner (centered minimal), card (compact accent mid-page).
---

# build-opt-in

Generate an email capture block.

## Questions (only if genuinely unclear)

1. **Variant?** split (big title + portrait circle), banner (centered, minimal), card (compact accent mid-page)
2. **Which brand?** tracy, ffb, ffm, fresh
3. **CTA?** Default: Tracy = Take the Quiz, FFB = Apply, FFM = Apply, FRESH = Take the Quiz

Default to split variant for homepage, banner for product pages, card for mid-page interrupts.

## Generation rules

1. Section: `<section class="opt-in" data-brand="{brand}">`
2. Background modifiers: `opt-in--canvas`, `opt-in--elevated`, `opt-in--accent`
3. Split: `<div class="opt-in__split">` with content left, portrait right
4. Banner: `<div class="opt-in__banner">` centered
5. Card: `<div class="opt-in__card">` with accent background
6. Form: `<form class="opt-in__form">` with inputs + submit button
7. Fine print: privacy note in `<p class="opt-in__fine">`

## Tracy defaults

- Tracy homepage: quiz CTA, not newsletter (no newsletter exists)
- Portrait: use real Tracy photos from Showit CDN
- Never fabricate email addresses or subscriber counts
