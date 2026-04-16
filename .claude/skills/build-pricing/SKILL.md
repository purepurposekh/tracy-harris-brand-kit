---
name: build-pricing
description: Generates a pricing section. Three variants: side-by-side (two payment options), single card (one centered card), dark (FFM premium). Always verify pricing against current sales page.
---

# build-pricing

Generate a pricing/offer block.

## Questions (only if genuinely unclear)

1. **Variant?** side-by-side (two cards), single (one centered), dark (FFM premium)
2. **Which product?** FFB or FFM
3. **Current pricing verified?** Always check against live sales page before quoting

## Pricing (verify before using)

- FFB: $6,000 AUD PIF | $550/mo x12 | $1,000 x6
- FFM: $31,000 AUD PIF (save $2,000) | $2,750/mo x12 | $1,000 discovery call fee (refundable)

## Generation rules

1. Section: `<section class="pricing" data-brand="{brand}">`
2. Side-by-side: `<div class="pricing__options">` with 2 cards
3. Single: `<div class="pricing__single">` with 1 centered card
4. Dark: add `pricing--dark` class for FFM inverse treatment
5. Featured card gets `pricing__card--featured` + badge
6. Features list: checkmark bullets via CSS ::before
7. CTA: FFB = "Apply Now", FFM = "Book a Discovery Call"

## Rules

- Freedom Filled® always has ® symbol
- FFM is always "Apply" language, never "Buy"
- Never fabricate pricing. Use [CHECK: verify current pricing] if unsure
