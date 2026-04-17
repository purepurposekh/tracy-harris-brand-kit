# Reference Pages Audit — Tonic Site Shop Lead Magnet Set

**Date:** 2026-04-17
**Author:** Kira
**Source:** `leadmagnetfreebiepages.tonicsiteshop.com` (10 pages, fetched live via WebFetch on 2026-04-17)
**Purpose:** Decide what new components we need to complete Tracy Harris Co's page-type library.

All 10 pages accessed live. Section counts below are inferred from rendered content, not raw DOM node counts, so treat the per-page breakdowns as "reading-order experience" audits, not pixel-perfect DOM maps.

---

## 1. Per-page section breakdown

Classifier legend: **E** = already exists, **Q** = queued, **N** = new component we don't have.

### 1.1 long-form-freebie

| # | Section | Class | Maps to / notes |
|---|---|---|---|
| 1 | Hero with primary download CTA | E | `hero/showcase` or `hero/split` |
| 2 | Single-quote social proof strip | E | `testimonials/single-hero` (small variant) |
| 3 | Value-prop list (bulleted feature list) | N | `feature-list` — iconified what's-inside bullets |
| 4 | Secondary testimonial quote | E | `testimonials/single-hero` |
| 5 | "8-page guide" content overview + CTA | N | `freebie-preview` — page-count + what's-inside teaser with a preview graphic |
| 6 | "Why we made this" motivation block | N | `why-block` — narrative problem/purpose explainer |
| 7 | Creator bio | E | `about-bio/split-editorial` |
| 8 | Problem statement paragraph | N | `why-block` (same family, different frame) |
| 9 | Long testimonials (2x full-length) | E | `testimonials/featured-trio` or `editorial-centered` |
| 10 | Stat block ("53%, 70%, 434%, 300%") | N | `stat-strip` — big numbers with caption |
| 11 | Outcome/benefit trio | N | `benefit-trio` — 3 outcome promises |
| 12 | Final CTA section | E | `cta-block/canvas` |
| 13 | Footer | E | `footer/showcase` |

### 1.2 long-form-freebie-2

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Minimal header / logo bar | E | `navigation/martini` (slim) |
| 2 | Hero with email opt-in inline | E | `opt-in/split` or `hero/split` + opt-in |
| 3 | Privacy disclaimer microcopy | N | `form-assurance` — tiny reassurance line |
| 4 | 4-up feature blocks | N | `feature-grid` — quad icon+copy tiles |
| 5 | Transitional CTA row | E | `cta-block/ruled` |
| 6 | Stat callouts (85%, $1M, 6000) | N | `stat-strip` |
| 7 | Long problem narrative | N | `why-block` |
| 8 | Results preview trio | N | `benefit-trio` |
| 9 | Single testimonial | E | `testimonials/single-hero` |
| 10 | 3-up testimonial grid | E | `testimonials/featured-trio` |
| 11 | Repeated testimonial section | — | SKIP (redundant) |
| 12 | Creator bio with transformation arc | E | `about-bio/split-editorial` |
| 13 | Mid-page CTA button | E | `cta-block/accent` |
| 14 | Final CTA | E | `cta-block/canvas` |
| 15 | Footer | E | `footer/showcase` |

### 1.3 interactive-freebie

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Hero "SEO isn't complicated" + CTA | E | `hero/amaretto` |
| 2 | Value-prop paragraph + download button | E | `cta-block/ruled` |
| 3 | "Get the guide" title card + link | E | `cta-block/elevated` |
| 4 | Curriculum preview (3 learning outcomes) | N | `curriculum-preview` — numbered or lettered contents list |
| 5 | Author bio | E | `about-bio/split-editorial` |
| 6 | Pull-quote testimonial (single line, editorial) | E | `testimonials/single-hero` (italic pull-quote variant worth adding) |
| 7 | Numbered benefit summary (3 items) | N | `benefit-trio` (numbered variant) |
| 8 | Inline name + email form | E | `opt-in/card` |
| 9 | Closing testimonial | E | `testimonials/single-hero` |
| 10 | Footer | E | `footer/showcase` |

Note: despite the name "interactive-freebie", this version has no quiz/click-reveal/tabs. The "interactive" hook seems to be the inline form embed, nothing richer.

### 1.4 medium-freebie-colorful

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Hero "Tired of this frustrating outcome?" + download CTA | E | `hero/showcase` |
| 2 | Guide overview with rotating SVG icon | N | `freebie-preview` (animated icon variant worth adding) |
| 3 | Curriculum list ("What you'll learn") | N | `curriculum-preview` |
| 4 | Explanation / pain-point paragraph | N | `why-block` |
| 5 | Bio "New here? I'm Cassandra" | E | `about-bio/centered-circle` |
| 6 | 2 brief testimonials | E | `testimonials/featured-trio` (2-up mode) |
| 7 | Testimonial label row | — | Inline ornamentation, not a component |
| 8 | "Ready to get started?" CTA | E | `cta-block/accent` |
| 9 | Footer quote | E | `testimonials/single-hero` |
| 10 | Footer | E | `footer/showcase` |

### 1.5 medium-freebie-neutral

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Neutral hero with inline opt-in form | E | `opt-in/split` |
| 2 | Single testimonial | E | `testimonials/single-hero` |
| 3 | Contents preview + "Yep I want this" CTA | N | `curriculum-preview` + inline CTA |
| 4 | Bio "Kara Langely" | E | `about-bio/split-editorial` |
| 5 | Testimonial + "as seen in" press strip | N | `press-strip` — logo row for publications |
| 6 | Centered CTA with opt-in | E | `opt-in/card` |
| 7 | Footer | E | `footer/showcase` |

### 1.6 simple-freebie

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Title/header | E | `navigation/martini` slim |
| 2 | Hero "Get the free download" CTA | E | `hero/amaretto` |
| 3 | Value prop paragraph | E | `cta-block/ruled` |
| 4 | Creator intro "hey, I'm Grace" | E | `about-bio/centered-circle` |
| 5 | Button-based CTA | E | `cta-block/accent` |
| 6 | Footer | E | `footer/showcase` |

Lightest page. Nothing new.

### 1.7 download-page-1 (TY / confirmation)

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | "You're in" confirmation hero + download button | Q | `hero/variants/results.html` (queued) |
| 2 | "Here's what's next" 3-step list | N | `next-steps` — numbered onboarding list (check email, subscribe, follow on IG) |
| 3 | Soft upsell mention w/ link to paid offer | N | `soft-upsell` — inline teaser card linking to OTO |
| 4 | Closing welcome message | E | `cta-block/ruled` |
| 5 | Footer | E | `footer/showcase` |

### 1.8 download-page-2 (TY variant with more structure)

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Header / title | E | `navigation/martini` |
| 2 | Primary download CTA section | Q | `hero/variants/results.html` |
| 3 | Confirmation + "check spam folder" callout | N | `spam-callout` — warm warning card |
| 4 | Numbered next-steps (01, 02) | N | `next-steps` (numbered variant) |
| 5 | "Wanna dive deeper?" section 03 — upsell | N | `soft-upsell` |
| 6 | "Check your inbox" final CTA | E | `cta-block/canvas` |
| 7 | Footer | E | `footer/showcase` |

### 1.9 upsell-page (OTO)

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Exit-intent / header offer + price tag | Q | `hero/variants/oto.html` (queued) |
| 2 | Problem recognition hook | N | `why-block` |
| 3 | 4-up qualification checklist w/ icons | N | `feature-grid` (same as 1.2 — 4-up tiles) |
| 4 | Countdown timer ("hurry! offer ends in") | — | **SKIP** (breaks Tracy's no-fake-scarcity rule) |
| 5 | 4 testimonial cards | E | `testimonials/wall` or `featured-trio` |
| 6 | "Why people love us" descriptive block | E | `cta-block/elevated` |
| 7 | Final "I need this!" CTA | E | `cta-block/canvas` |

Also implied on OTO but not always rendered: offer-stack, guarantee — both already queued.

### 1.10 bonus-screamers

| # | Section | Class | Notes |
|---|---|---|---|
| 1 | Title | E | `navigation/martini` |
| 2 | "Steal my free X" offer block | N | `bonus-screamer` — a loud single-offer callout with heading + body + button, designed to break up long pages |
| 3 | "Screamer message here" separator block | N | `bonus-screamer` (rule/separator variant) |
| 4 | "Get my free SEO guide" bold CTA | E | `cta-block/accent` |
| 5 | Repeating decorative copy with bullet separators | — | Styling, not a component |

Karl's question: "what is bonus-screamers?" — it's a page of reusable, attention-grabbing offer-interrupter blocks you drop between long-form sections. Not a standalone page type for us, but the *block* itself (loud mid-page interrupter callout) is genuinely useful.

---

## 2. New components to build (ranked)

Ranked by unlock value (how many page types it serves), then complexity ascending.

| # | Component | Purpose | Seen on | Serves page types | Complexity | Why it matters |
|---|---|---|---|---|---|---|
| 1 | `why-block` | Narrative problem/purpose explainer with lead-in heading and body paragraph | long-1, long-2, colorful, upsell | sales-home, long-landing, short-landing, oto | S | Every long-form page needs a "why this exists" beat. Currently we have hero and CTA, nothing in between for narrative. |
| 2 | `benefit-trio` | 3 outcome promises with icon or number + short copy | long-1, long-2, interactive | sales-home, long-landing, oto | S | High-traffic layout pattern. Used on 3 of 10 pages. Feeds sales-page skill output directly. |
| 3 | `curriculum-preview` | "What you'll learn" / contents list for a freebie or course | interactive, colorful, neutral | long-landing, short-landing, sales-home | S | Essential for FRESH Quiz, FFB resource vault pages, workshop registrations. 3 of 10 pages. |
| 4 | `next-steps` | Numbered onboarding list (1, 2, 3 steps) with icons and copy | download-1, download-2 | results-ty, oto | S | Completes the TY/download page so it's not just "here's your file" but "here's how to actually use what you got". |
| 5 | `feature-grid` | 4-up icon+copy tiles (quad layout, not trio) | long-2, upsell | sales-home, long-landing, oto | S | Distinct from our existing bento — this is symmetrical quad, not asymmetric. Clean for feature/qualification checklists. |
| 6 | `stat-strip` | Big-number statistics row with captions (e.g. "85% • $1M • 6000") | long-1, long-2 | long-landing, sales-home | S | Tracy has legit numbers she can use (500+ episodes, 4,100 downloads/mo, 7+ years FFM). Currently no component for this. |
| 7 | `soft-upsell` | Inline teaser card linking post-opt-in traffic to a paid offer | download-1, download-2 | results-ty | S | The money-making moment on TY pages. Without this, TY pages are dead-ends. |
| 8 | `freebie-preview` | Page-count + what's-inside teaser with a preview graphic (mocked-up PDF/workbook image) | long-1, colorful | long-landing, short-landing | M | Visual proof the freebie is real. Lifts opt-in conversion. The colorful version had a rotating SVG — worth adding as an animated variant. |
| 9 | `feature-list` | Iconified vertical what's-inside bullets (not a grid, a list) | long-1 | long-landing, oto | S | Variant of feature-grid; listy rather than grid. May end up as a variant of `feature-grid` rather than its own family. |
| 10 | `press-strip` | Logo row for "as seen in" publications | neutral | sales-home, long-landing | S | Only useful once Tracy has press logos confirmed — currently low-priority. Build the shell, leave the logos TBD. |
| 11 | `spam-callout` | "Check your spam folder" warm warning card | download-2 | results-ty | XS | Tiny utility block. 30-minute build. |
| 12 | `form-assurance` | Tiny privacy reassurance line under form fields | long-2 | any page with a form | XS | Probably should just be a utility class on `opt-in`, not a new component. Noted for completeness. |
| 13 | `bonus-screamer` | Loud mid-page offer interrupter (heading + body + button, high-contrast) | bonus-screamers | long-landing, oto | S | Mid-scroll attention-grabber for dense pages. Useful but not critical — essentially a dialled-up variant of `cta-block`. |

---

## 3. Variations worth adding to existing components

These aren't new components, they're new treatments of families we already have.

| Existing family | New variant | Source page | Treatment |
|---|---|---|---|
| `testimonials` | `pull-quote` | interactive | Single italic pull-quote, editorial serif, centred, no avatar. Distinct from `single-hero` which has more chrome. |
| `testimonials` | `duo` | colorful | 2-up testimonials (we currently have trio and wall, nothing in between). |
| `about-bio` | `narrative-long` | long-1, long-2 | Bio with a multi-paragraph transformation arc, not just a tight 3-sentence intro. |
| `cta-block` | `rule-separator` | bonus-screamers | Copy block with ornamental rule separators (• • •) between lines — rhythm/pacing utility. |
| `hero` | `opt-in-inline` | long-2, neutral | Hero where the email form is embedded in the hero itself, not a separate section below. We have this behaviour in `opt-in/split` but not as a `hero` variant. |
| `cta-block` | `download-hero` | download-1, download-2 | TY-page-specific: giant centred "GET YOUR DOWNLOAD" button with success-state framing. Could live under the queued `hero/results` instead. |

---

## 4. What we can skip

| Section type | Why skip |
|---|---|
| Countdown timer on upsell-page | Violates Tracy's no-fake-scarcity rule. Only build if Tracy has a real deadline event, and even then use a dated headline, not a ticking clock. |
| "Screamer message here" decorative ornament repeats on bonus-screamers | Pure filler. The useful pattern is the single `bonus-screamer` block, not the repeated ornament. |
| "As seen in" press strip | Build the shell, skip populating until Tracy has confirmed press logos. Not a launch blocker. |
| Duplicated testimonial sections on long-2 | Pure duplication, not a new pattern. Page composer can just reuse the same component twice if needed. |
| Hipster / lorem-ipsum filler copy across all pages ("master cleanse af shoreditch vinyl jawn") | Ignore entirely — this is Tonic's template placeholder, not a component. |

---

## 5. Suggested build order

### Phase 1 — Unblock queued page types (results-ty + OTO)
1. `hero/variants/results.html` — confirmation / TY / quiz-result hero
2. `hero/variants/oto.html` — one-time-offer hero
3. `offer-stack` — what's-included bullet list for OTO
4. `guarantee` — risk-reversal block for OTO
5. `next-steps` — numbered onboarding list (completes results-ty)
6. `soft-upsell` — inline paid-offer teaser on TY pages

**Estimate:** ~2 dev days. Phase 1 ships results-ty and OTO page types end-to-end.

### Phase 2 — Highest-leverage new components (serve the most page types)
7. `why-block` — narrative problem/purpose explainer
8. `benefit-trio` — 3 outcome promises
9. `curriculum-preview` — what's-inside contents list
10. `feature-grid` — 4-up icon+copy tiles
11. `stat-strip` — big-number row

**Estimate:** ~2 dev days. Phase 2 ships long-landing and sales-home page types to full fidelity.

### Phase 3 — Variations of existing components
12. `testimonials/pull-quote` + `testimonials/duo`
13. `about-bio/narrative-long`
14. `hero/opt-in-inline`
15. `cta-block/rule-separator`

**Estimate:** ~1 dev day. Phase 3 is polish — same components, more treatments for design variety.

### Phase 4 — Nice-to-haves
16. `freebie-preview` (with animated-icon variant)
17. `feature-list` (could ship as a `feature-grid` variant instead)
18. `press-strip` (shell only)
19. `spam-callout`
20. `form-assurance` (likely just a utility class)
21. `bonus-screamer`

**Estimate:** ~1.5 dev days. Phase 4 closes the long tail.

**Total to full parity with Tonic's lead-magnet set:** ~6.5 dev days across 4 phases, with Phase 1 alone unblocking the two page types we can't currently ship.

---

## Assumptions + caveats

- Section breakdowns come from WebFetch's AI read of rendered HTML, not a DOM-level audit. Treat them as experience-level, not pixel-perfect.
- Tonic templates lean heavily on filler copy and stock placeholder graphics. The value here is the **section grammar**, not the copy.
- `opt-in` currently has one variant (`showcase`) on disk, though the brand kit inventory lists `split`, `banner`, `card`, `accent-dark`. Those may exist in the composer/examples rather than as standalone variant files — worth verifying before calling any of them "done".
- `cta-block` has similar drift — inventory lists 5 variants, on-disk has `showcase` only. Either the variants live elsewhere or the inventory doc is ahead of implementation. Flag for Karl.
