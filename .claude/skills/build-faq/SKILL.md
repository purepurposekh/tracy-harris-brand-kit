---
name: build-faq
description: Generates an FAQ section. Two variants: tabbed (categories + accordion for multi-topic pages) and simple (single accordion for product pages).
---

# build-faq

Generate an FAQ block.

## Questions (only if genuinely unclear)

1. **Variant?** tabbed (categories like General / FFB / FFM / Billing) or simple (single list, no tabs)
2. **Which brand?** tracy, ffb, ffm, fresh
3. **Any real Q&A to use?** If not, use plausible product-specific questions

Default to simple variant on product pages, tabbed on the main site.

## Generation rules

1. Section: `<section class="faq" data-brand="{brand}">`
2. Add `faq--simple` class for single-list variant
3. Add `faq--elevated` for oatmeal background
4. Each question: `<div class="faq__item" data-open="false">` with `<button class="faq__question">` and `<div class="faq__answer">`
5. Tabs: `<button class="faq__tab" data-tab="{id}">` with matching `<div class="faq__panel" data-tab="{id}">`
6. Include faq.js script at the bottom

## Accessibility

- [ ] Questions use `<button>` with `aria-expanded`
- [ ] Tab buttons use `role="tab"` with `aria-selected`
- [ ] Panels use `role="tabpanel"`
- [ ] Keyboard: Enter/Space toggles items
