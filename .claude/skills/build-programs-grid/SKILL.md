---
name: build-programs-grid
description: Generates a programs-grid section showing 2-4 program cards (FFB / FFM / FRESH). Used as the homepage offer anchor and as a cross-link block on product pages.
---

# build-programs-grid

Generate the horizontal card grid that summarises Tracy's programs.

## When this skill runs

User asks for "programs section", "pathway section", "programs grid", or "the three programs on the homepage".

## Questions to ask

1. **Which brand page?** Tracy (parent, shows 3-up), or a product page (shows 2-up of sister programs)
2. **Header copy?** Eyebrow, title (italic emphasis on a word), subline. Use brand default if unsure.
3. **Which programs to feature?** Default order on Tracy homepage: **FRESH → FFB → FFM** (ascending pricing ladder: free → $6K → $31K). For product pages, show the other two in the same ladder order.
4. **Custom facts per card?** Default facts are Duration + Format + Investment. User can override.

## Card defaults

### FFB (accent: sage)
- Title: Freedom Filled® _Business_
- Tagline: The flagship mentorship.
- Desc: A 12-month mentorship for women ready to move beyond content and into the full architecture of a profitable, scalable online business. Strategy meets identity.
- Facts: Duration 12 months, Format Mentorship, Investment From $6,000 AUD
- CTA: Explore FFB → /ffb

### FFM (accent: gold)
- Title: Freedom Filled® _Mastermind_
- Tagline: The intimate room.
- Desc: Tracy's most intimate and premium offering. Application-based, intentionally small, for women ready to lead at a higher level. Includes Bali retreats.
- Facts: Cohort 20 women max, Format Application-based, Investment From $31,000 AUD
- CTA: Apply for FFM → /ffm

### FRESH (accent: green)
- Title: The FRESH _Framework™_
- Tagline: The foundation.
- Desc: Tracy's personal operating system. Fitness and Nutrition, Relationships, Environment, Self, Hustle. The foundation beneath every program.
- Facts: Format Self-led + quiz, Entry point FRESH Quiz, Investment Free
- CTA: Take the Quiz → /quiz

## Generation rules

1. Section element: `<section class="programs" data-brand="{brand}">`.
2. Grid class: `programs__grid` for 3-up, add `programs__grid--two` or `programs__grid--four` to switch count.
3. Each card: `<article class="program-card" data-accent="{sage|gold|green|navy|orange}">`.
4. Title uses italic emphasis on the differentiator word via `<em>`.
5. Always include the ® on "Freedom Filled®" and ™ on "FRESH Framework™".
6. Facts use `<dl>` with `<dt>` for label and `<dd>` for value.
7. CTA link text must include the program name (accessibility).
8. No em dashes in copy.

## Output format

Return the full `<section>` block ready to paste. Include:
- Note on brand defaults applied
- Reminder to link `/styles/tokens.css` and `/components/programs-grid/programs-grid.css`

## Accessibility

- [ ] Section has `<h2>` as title
- [ ] Cards are `<article>` with internal `<h3>`
- [ ] CTA text is descriptive ("Explore FFB" not "Learn more")
- [ ] Accent colours only as 3px top border, never as background behind text
