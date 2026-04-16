---
name: build-image-grid
description: Generates a photo gallery section. Two variants: bento (asymmetric grid with mixed sizes) and masonry (natural-height columns).
---

# build-image-grid

Generate a photo gallery block.

## Questions (only if genuinely unclear)

1. **Variant?** bento (asymmetric, mixed sizes, hover overlays) or masonry (equal columns, natural heights)
2. **Which brand?** tracy, ffb, ffm, fresh
3. **Content?** retreat photos, event photos, behind-the-scenes, member moments

Default to bento for about/gallery pages, masonry for lighter inline use.

## Generation rules

1. Section: `<section class="image-grid" data-brand="{brand}">`
2. Bento: `<div class="image-grid__bento">` with cells using size modifiers
3. Cell sizes: `--wide` (span 2 cols), `--tall` (span 2 rows), `--large` (span 2x2)
4. Hover overlay: `<div class="image-grid__cell-overlay">` with label + sub
5. Masonry: `<div class="image-grid__masonry">` with equal-width cells
6. Use real photos from Showit CDN, not placeholders

## Accessibility

- [ ] Every image has descriptive alt text
- [ ] Overlay text is decorative (also visible in alt)
