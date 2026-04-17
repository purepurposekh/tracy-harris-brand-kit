# Tracy Harris Co — Brand Kit Backlog

*Living doc. Updated when items land or new ones surface. Ranked by unlock value, not effort.*

Last updated: 2026-04-17

---

## In flight

*(nothing currently — next build ready to start when Karl greenlights)*

---

## Phase 2 — high-leverage new components (NEXT UP)

Needed to bring **Long landing** and **Blog** page types to full fidelity (they render sparse today).

- [ ] **`why-block`** — narrative problem/purpose explainer. Serves sales-home, long-landing, short-landing, OTO (4 page types)
- [ ] **`benefit-trio`** — 3 outcome promises with icons. Serves sales-home, long-landing, OTO
- [ ] **`curriculum-preview`** — what's-inside contents list. Serves long-landing, short-landing, sales-home
- [ ] **`feature-grid`** — long-landing fills out properly (audit flag)
- [ ] **`post-grid`** — blog post card grid for `/blog` index
- [ ] **`content-section`** — blog article body section (typographic-only hero + long-form prose)
- [ ] **`hero/textonly`** — dedicated text-only hero variant (currently aliased to hero.showcase)

---

## Phase 3 — site-rebuild unlocks

Pre-requisites for shipping the new tracyharris.co homepage + FFB sales page + podcast rebuild.

- [ ] **Announcement bar** — thin top strip for launches ("Applications open for the May cohort · Apply →")
- [ ] **Process / how-it-works** — numbered-step section for sales pages
- [ ] **Results strip / proof bar** — "500+ episodes · 4.1k monthly downloads · 7+ years running" metric band OR logo strip if we have placements
- [ ] **Before/after transformation block** — paired "where you are now · where you'll be" columns
- [ ] **Workshop / event landing hero** — single-date registration, different from main hero
- [ ] **Application form section** — FFB/FFM application inline, multi-step with save state
- [ ] **Blog post card grid** — for `/blog` index
- [ ] **Podcast episode archive** — for `/podcast`, searchable/filterable 500+ episode list
- [ ] **Curriculum accordion** — FFB/FFM deep-dive module breakdown, expandable
- [ ] **Contact / booking block** — Calendly-embed-ready or clean email-forward form

---

## Phase 4 — variations of existing components

From the audit, flagged as variants worth adding to existing families:

- [ ] Testimonials — scroll-cycling carousel with big portraits
- [ ] Hero — editorial with diagonal cream stripe overlay
- [ ] (Others; see `docs/ref-pages-audit-2026-04-17.md`)

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

- [ ] **/review/ approval walkthrough** — stamp each of 44 (soon 54) variants as approved / revise / rejected. Click Export to lock state in

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
