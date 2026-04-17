# Tracy Harris Co — Brand Kit Backlog

*Living doc. Updated when items land or new ones surface. Ranked by unlock value, not effort.*

Last updated: 2026-04-17

---

## In flight

*(nothing currently — Phase 2 shipped, Phase 3 ready to start on greenlight)*

---

## Phase 3 — site-rebuild unlocks (NEXT UP)

Pre-requisites for shipping the new tracyharris.co homepage + FFB sales page + podcast rebuild. Phase 2 closed Long landing and Blog to full fidelity — Phase 3 unlocks the remaining launch-critical pieces.

- [ ] **Announcement bar** — thin top strip for launches ("Applications open for the May cohort · Apply →")
- [ ] **Process / how-it-works** — numbered-step section for sales pages
- [ ] **Results strip / proof bar** — "500+ episodes · 4.1k monthly downloads · 7+ years running" metric band OR logo strip if we have placements (also closes the deferred `stat-strip` flag from the ref-pages audit)
- [ ] **Before/after transformation block** — paired "where you are now · where you'll be" columns
- [ ] **Workshop / event landing hero** — single-date registration, different from main hero
- [ ] **Application form section** — FFB/FFM application inline, multi-step with save state
- [ ] **Podcast episode archive** — for `/podcast`, searchable/filterable 500+ episode list
- [ ] **Contact / booking block** — Calendly-embed-ready or clean email-forward form

---

## Phase 4 — variations of existing components

From the audit, flagged as variants worth adding to existing families:

- [ ] **`testimonials/pull-quote`** — single italic pull-quote, editorial serif, centred, no avatar
- [ ] **`testimonials/duo`** — 2-up testimonials (gap between our trio and wall)
- [ ] **`about-bio/narrative-long`** — bio with multi-paragraph transformation arc
- [ ] **`hero/opt-in-inline`** — hero with email form embedded directly (not separate opt-in section below)
- [ ] **`cta-block/rule-separator`** — ornamental rule separators (• • •) for rhythm
- [ ] **`cta-block/bonus-screamer`** — dialled-up mid-page offer interrupter (absorb the deferred `bonus-screamer` family)
- [ ] **`feature-grid/list`** — 1-column iconified list variant (absorb the deferred `feature-list` family)
- [ ] Testimonials — scroll-cycling carousel with big portraits
- [ ] Hero — editorial with diagonal cream stripe overlay
- [ ] **`freebie-preview`** — page-count + what's-inside teaser with mocked PDF/workbook graphic (blocked on visual asset)
- [ ] **`press-strip`** — "as seen in" logo row (blocked on confirmed press logos)

---

## Infrastructure queue

- [ ] **Split multi-variant showcases** into separate files — testimonials, opt-in, cta-block, pricing, about-bio, podcast-card, image-grid, faq. Each variant gets its own URL for clean /compose/ thumbnail previews
- [ ] **Slack bot routing** — inbound Slack → VPS so one Kira across Discord + Slack with unified memory. ~2hr build
- [ ] **`/admin/recipes` HogQL dashboard** — custom recipe-conversion dashboard inside `dashboard.tracyharris.com.au`. Blocked on PostHog WP snippet being installed first
- [ ] **Fathom → PostHog migration** — run in parallel 2-4 weeks, validate numbers, kill Fathom
- [ ] **`site_version` tagging** — when tracyharris.co v2 launches, update `thc-analytics.js` to set `site_version: 'v2'` so data segments cleanly
- [ ] **Self-hosted analytics** — deferred. PostHog Cloud chosen instead. Revisit only if PostHog relicenses core or free tier degrades (see `project_analytics_system_todo.md` in Kira memory)

---

## Blocked — waiting on Karl

- [ ] **/review/ approval walkthrough** — stamp each of 54 (soon 64) variants as approved / revise / rejected. Click Export to lock state in

---

## Done 2026-04-16 → 04-17

- [x] Martini direction hero + footer + nav overlay
- [x] Amaretto wordmark hero
- [x] Split dual (dark + light) hero with Tracy at 75% viewport
- [x] Tony editorial stage hero (reworked in Tracy voice)
- [x] Product callout: 4 variants (bento-ffb, bento-elite, editorial, clearer) with obvious video section
- [x] Event widget with modal + compact mobile redesign + workshop title overlaid on Tracy
- [x] `/compose/` page composer + recipe JSON + sticky chip strip + preview button
- [x] `/review/` approval page with localStorage + export
- [x] Anchor IDs added across multi-variant showcase files
- [x] PostHog Cloud analytics layer (`thc-analytics.js`) with recipe_id auto-attribution
- [x] WP install guide
- [x] Deep research report on self-hosted analytics (PostHog Cloud chosen)
- [x] 10-ref-pages audit report
- [x] First real recipe → page loop closed: FFB Strategy Archetype preview at `/pages/ffb-strategy-archetype.html`
- [x] **Phase 1 (6 new components shipped)**: `hero/results`, `hero/oto`, `offer-stack`, `guarantee`, `next-steps`, `soft-upsell` — unlocks TY/Results and OTO page types end-to-end
- [x] **/compose/ page-type filter** (Sales · Short · Long · TY · Blog · OTO · Show all)
- [x] **/compose/ reads /review/approvals.json** — rejected variants hidden, approved variants tagged with sage pill
- [x] **PostHog Cloud EU installed on tracyharris.co** — script live, pageviews confirmed in Live Events, recipe_id auto-attribution wired
- [x] **Phase 2 (7 new components shipped): `why-block`, `benefit-trio`, `curriculum-preview`, `feature-grid`, `post-grid`, `content-section`, `hero/textonly`** — Long landing and Blog page types now render to full fidelity. `/compose/` filter map updated to expose them across Sales, Short, Long, OTO, Blog page types. `/review/` now covers 64 variants across 28 families.
- [x] **Re-audit of 10 ref pages (post-Phase 1)** — appended to `docs/ref-pages-audit-2026-04-17.md`. No missed sections load-bearing enough to block Phase 2.
