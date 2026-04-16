---
name: build-podcast-card
description: Generates a podcast section. Two variants: featured (large card with art, details, listen-on links) and compact (small inline card for homepage).
---

# build-podcast-card

Generate a podcast block.

## Generation rules

1. Section: `<section class="podcast-card" data-brand="{brand}">`
2. Featured: `<div class="podcast-card__featured">` art left, details right
3. Compact: `<div class="podcast-card__compact">` small inline row
4. Play button: circle icon + "Listen now" text
5. Platforms: Apple Podcasts, Spotify, YouTube, RSS pills
6. Episode title/desc: use [EPISODE TITLE] placeholder unless real data provided

## Rules

- Podcast is still branded "Mums With Hustle Podcast" (rebrand pending)
- 500+ episodes, ~4,100 downloads/month
- Never reference @mumswithhustle Instagram handle
