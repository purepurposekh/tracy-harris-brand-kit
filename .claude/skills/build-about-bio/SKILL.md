---
name: build-about-bio
description: Generates a Tracy bio section. Two variants: split (portrait left, editorial bio right with signature and facts) and centered (circle portrait, stacked text).
---

# build-about-bio

Generate a bio/about block.

## Generation rules

1. Section: `<section class="about-bio" data-brand="{brand}">`
2. Split: `<div class="about-bio__split">` portrait left, content right
3. Centered: `<div class="about-bio__centered">` stacked with circle portrait
4. Signature: `<p class="about-bio__signature">Tracy</p>` in Jhon Halend script
5. Facts strip: episodes, years, cohort size
6. Use real Tracy photos from Showit CDN
7. Bio copy must follow Tracy's voice (first person, breathing rhythm)

## Rules

- Tracy writes as "I", never third person
- Never fabricate facts or figures
- Include Jhon Halend signature
- CTA links to /about for homepage placement
