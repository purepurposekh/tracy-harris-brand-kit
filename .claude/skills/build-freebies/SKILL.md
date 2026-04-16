---
name: build-freebies
description: Generates a freebies/resources section with zigzag alternating image-text cards. For free downloads, worksheets, mini-courses.
---

# build-freebies

Generate a free resources section.

## Questions (only if genuinely unclear)

1. **Which brand?** tracy, ffb, ffm, fresh
2. **How many resources?** Default: 3
3. **Any real resources to feature?** If not, use plausible placeholders

## Generation rules

1. Section: `<section class="freebies" data-brand="{brand}">`
2. Header: eyebrow + large serif title (can be just "Freebies")
3. Grid: `<div class="freebies__grid">` with `<article class="freebies__item">` cards
4. Each card: image left, content right (alternates via CSS nth-child)
5. Content: tag pill + serif title + description + download link
6. Tags: "Free worksheet", "Free download", "Free mini-course", etc.
7. Images: use real Tracy photos from Showit CDN

## Accessibility

- [ ] Each card is an `<article>` with heading hierarchy
- [ ] Images have descriptive alt text
- [ ] Links are descriptive ("Download free" not just "click here")
