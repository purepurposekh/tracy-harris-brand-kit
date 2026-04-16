---
name: build-testimonials
description: Generates a testimonials section. Three variants: masonry wall (homepage), featured trio (product pages before pricing), single hero quote (between sections).
---

# build-testimonials

Generate a social-proof block.

## Questions (only if genuinely unclear)

1. **Variant?** wall (homepage dense), featured (3-up before pricing), single (big quote between sections)
2. **Which brand?** tracy, ffb, ffm, fresh
3. **Any real quotes to use?** If not, use `[MEMBER NAME]` placeholders with plausible role descriptors

Default to the brand's masonry wall if unspecified.

## Placeholder rule

Never fabricate named people or specific revenue figures. Use `[MEMBER NAME]` as the name and generic roles like "Online course creator", "Service business owner", "SaaS founder". Real data replaces placeholders later.

## Voice rules for quotes

- Short, specific, emotional
- Can use italic emphasis on one key word via `<em>`
- No em dashes
- Max 3 sentences for wall cards, 2-4 for featured/single

## Generation rules

1. Section: `<section class="testimonials" data-brand="{brand}">`
2. Header: eyebrow + title (with italic emphasis) + optional sub
3. Wall: `<div class="testimonials__wall">` with figures; varies with screen (3→2→1 columns)
4. Featured: `<div class="testimonials__featured">` — 3 cards, middle card gets `data-featured="true"` for accent-color treatment
5. Single: `<div class="testimonials__single">` — portrait left, big quote right
6. Each testimonial: `<figure class="testimonial">`, with `<blockquote class="testimonial__quote">`, `<figcaption class="testimonial__attribution">`
7. Tag pill showing program: `<span class="testimonial__tag">FFB</span>` etc.

## Accessibility

- [ ] Each quote in `<figure>` with `<blockquote>` and `<figcaption>`
- [ ] Avatar has `alt` describing the person
- [ ] Quote text meets 4.5:1 contrast against its card background
