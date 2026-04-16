---
name: build-card-flip
description: Generates a 3D card-flip programs grid. Front shows summary, back shows details + CTA. Three cards in a row (FRESH → FFB → FFM).
---

# build-card-flip

Generate a flip-card programs section.

## Generation rules

1. Section: `<section class="card-flip-section" data-brand="{brand}">`
2. Grid: `<div class="card-flip-grid">` with 3 `<div class="card-flip">` cards
3. Each card: `card-flip__front` (summary) + `card-flip__back` (details + CTA)
4. Order: FRESH → FFB → FFM (ascending price)
5. Back color: program-specific via `data-program="fresh|ffb|ffm"`
6. Include card-flip.js for click/keyboard toggle
7. Cards are `tabindex="0"` with `role="button"` for keyboard access

## Accessibility

- [ ] Cards focusable with keyboard
- [ ] aria-label describes the card
- [ ] CTA links on back face are tabbable independently
