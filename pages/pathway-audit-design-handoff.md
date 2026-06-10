# The Freedom Filled® Pathway Audit · Result Page Design Handoff

> For Karl to take into Claude Design (or any design tool). 2026-06-10.
> Working prototype: https://362c2084.tracy-harris-brand-kit.pages.dev/pages/pathway-audit.html
> Sample results: add `?demo=ffb`, `?demo=workshop`, `?demo=fresh`, `?demo=nurture`
> Real data payloads for each sample: `pathway-audit-sample-payloads.json` (same folder)

---

## 1. Governing rules (design must respect these, everything else is open)

1. **No numeric score anywhere on the customer surface.** No 68/100, no percentages, no "score". Visuals MAY encode the internal 0-100 area values (bar length, dial position, fill level) as long as no number is printed next to them. The data payload includes `internalScore` per area for exactly this.
2. **Never render nine problem cards.** One expanded primary focus, two compact secondaries, strengths named as strengths. The full 9-area view lives behind a "See your full snapshot" drawer.
3. **Max one expanded problem at a time.** The page kills overwhelm, it never stacks red flags. If 6+ areas need attention, the copy says that's normal for her season and the plan is still one step.
4. **"Leak" language only inside the diagnosis card.** Never in headlines, buttons, chips, or labels.
5. **FFB is applied for, never bought.** No checkout energy, no countdown timers, no scarcity.
6. **No archetypes, no persona names.** The season name is the identity hook.
7. **No fabricated testimonials, names, stats.** If a proof slot is designed in, label it [INSERT CLIENT STORY/RESULT].
8. **No em dashes in any copy.**

---

## 2. Page anatomy, in order

Each section below lists: its job, where the content comes from (fixed copy vs computed), and the data available if you want to design a visual for it.

### 2.1 Hero · "Your next best step"
- **Job:** land the one-step answer before anything else.
- **Content:** `heroHeadline` ("Leah, your next best step is to tighten your message."), season name as a script accent under it, then 2-4 sentences of season copy (fixed per band, already written and voice-approved).
- **Data:** `firstName`, `primaryFocus`, `season`.
- **Visual opportunity:** the season could carry a quiet motif (a horizon line, a sun position, a phase mark). Keep it abstract; the season is context, not a grade.

### 2.2 Pathway snapshot (the health check)
- **Job:** Karl's "business health check" moment. She sees what's strong, what's steady, what needs attention, without judgment.
- **Content:** primary focus expanded (state chip + meaning line), two secondaries compact, strengths sentence naming her Strong areas.
- **Data per area (all 9):** `name`, `domain` (BUILD/SELL/LEAD), `state` (strong / steady / attention), `internalScore` (0-100, for visual encoding only).
- **Visual opportunity, the big one:** per-area health indicator. Options that fit the rules: fill bars without numbers, a three-position marker (strong/steady/attention), an arc or dial per domain, a "pathway elevation" line across the 9 areas. State colour mapping in section 4.

### 2.3 Why we're starting here (diagnosis card)
- **Job:** Tracy reading her map back to her, in Tracy's voice. The only place "leak" may appear.
- **Content:** fixed per band with computed substitutions (strength names, primary focus lowercase). Already written.
- **Data:** `season.key`, `strengths`, `primaryFocus`, `needsAttentionCount`.
- **Visual:** keep this typographic. It's a voice moment, not a chart moment.

### 2.4 Your first business fix
- **Job:** one prescribed move for the primary area. Concrete, doable this week.
- **Content:** one fixed prescription per area (9 total, written). Messaging fixes reference Million Dollar Message™, never StoryBrand.
- **Data:** `primaryFocus.code` picks the prescription.
- **Visual opportunity:** card treatment that feels like a handwritten note or a single index card. One card, never a list.

### 2.5 The woman carrying it (F.R.E.S.H support signal)
- **Job:** the human layer. Renders quiet (one line), elevated (named gently), or leading (when depletion routes her FRESH-first).
- **Data:** `fresh.level` (quiet / elevated / first), `fresh.supportLabel` (one of 5 public labels), `fresh.depletionFlags` (0-6, internal).
- **Visual opportunity:** F.R.E.S.H as a foundation line or watermark, never a sixth chart. It's an undercurrent by locked decision, not a parallel dimension.

### 2.6 The Pathway map
- **Job:** show the whole Freedom Filled® Pathway as a clear system, with her pins on it. This is the "there IS a system" moment that earns FFB.
- **Data:** all 9 areas with domain + state, `primaryFocus` (her "start here" pin), `secondaryFocus` (her "then" pins), `fresh.level` for the foundation line.
- **Visual opportunity, the second big one:** this is the take-home asset (it also gets emailed as her personalised Pathway Map). BUILD then SELL then LEAD as territories in order, 3 areas each, her pins placed, F.R.E.S.H drawn underneath as the foundation, not as a fourth pillar. Design this as something she'd print.

### 2.7 Route bridge (the CTA block)
- **Job:** one primary CTA matched to her route. Copy is written for all four routes.
- **Data:** `route` picks the variant:
  - `ffb` → Apply for Freedom Filled® Business
  - `workshop` → Save your seat for the next workshop
  - `fresh` → Start the F.R.E.S.H. Reset (no FFB mention on this page)
  - `nurture` → Start with Tracy's free teaching (nothing priced on this page)
- **Conditional:** `mdmFit: true` on the `ffb` route adds a compact Million Dollar Message™ Workshop secondary card. On `workshop` route it reframes the CTA toward the MDM Workshop. Never on `fresh` or `nurture`.
- **Visual:** the bridge swaps, the pathway visual stays constant. Design one frame with four content states.

### 2.8 Drawer + footer
- "See your full snapshot" drawer: all 9 areas with states. Same no-number rule.
- Restart link, take-home Map delivery line ("Your Pathway Map is on its way to your inbox").

---

## 3. The data contract (what the engine hands the page)

```
{
  firstName:        string | ""           // personalisation, may be empty
  heroHeadline:     string                // computed, ready to render
  season:           { key, name }         // foundation | momentum | refinement | leadership
  route:            "ffb" | "workshop" | "fresh" | "nurture"
  primaryFocus:     { code, name, domain, state }
  secondaryFocus:   [ two of the same shape ]
  areas:            [ 9 x { code, name, domain, state, internalScore } ]
                    // state: strong | steady | attention
                    // internalScore: 0-100, VISUAL ENCODING ONLY, never printed
  strengths:        [ area names with state = strong ]
  needsAttentionCount: number             // 6+ triggers the "normal for your season" line
  fresh:            { level, dominantLetter, supportLabel, depletionFlags }
                    // level: quiet | elevated | first
  mdmFit:           boolean               // MDM Workshop secondary trigger
  internalReadiness: number               // 0-100, internal + analytics only, NEVER on the page
  firedTags:        [ ... ]               // email personalisation, not for the page
  acTags:           [ ... ]               // ActiveCampaign writes, not for the page
}
```

Four real payloads (one per route, straight from the engine) are in `pathway-audit-sample-payloads.json`. Paste one into Claude Design as the working data.

---

## 4. FFM brand quick sheet (so the tool starts in our world)

- Canvas: oatmeal `#f6f4f1` · Elevated: white `#ffffff` · Inverse sections: charcoal `#101010`
- Ink: heading `#101010`, body `#313131`, mute `#727272`
- Accent: gold dark `#7b623c`, gold mid `#c9a46c`, hero gradient 135deg dark→mid
- State colours used in the prototype: attention = gold-dark tint, steady = neutral grey tint, strong = sage `#6e8e77` tint. Open to better, keep attention warm (never red alarm) and strong calm (never traffic-light green).
- Display type: Editors Note (serif), regular weight. Body: Poppins. Labels: Public Sans, uppercase, wide tracking.
- Script accent: Chic Societe Script, 28px minimum, gold. Used for the season name.
- Buttons: pill, gold gradient, charcoal text. Application language on FFB.
- Mood: luxury editorial, quietly expensive, intimate. Not cottagecore, not corporate dashboard.

---

## 5. Functional requirements beyond design (the non-design answer)

What the production page needs that no mockup will show:

1. **Server-side submission endpoint.** Answers + free-texts + result posted on completion (before the result renders, so abandons after the transition still capture).
2. **AC sync.** Tags + custom fields per the scoring matrix scheme (`quiz_audit_*`). Route, band, primary focus, FRESH signal, fired objection tags.
3. **Email capture position.** The audit is post-class, so she's usually already known. Production needs the known-contact path (prefill from link token) and the unknown path (capture before results).
4. **Personalised Pathway Map email.** The take-home asset, generated per result. The map design from 2.6 should work in email/PDF form, not just on-page.
5. **Internal readiness number to the warehouse** (thc.db) for analytics and route calibration. Not to AC, not to the page.
6. **Free-text storage** for VOC mining and pre-application context. No AI analysis layer in v1.
7. **Route URLs.** FFB application page, workshop registration (with MDM-scheduled variant), F.R.E.S.H. Reset, free teaching path. All currently placeholders.
8. **Result permalink.** She'll want to revisit; the emailed map should link back to her result.
9. **FRESH-first calibration hook.** The 4-depletion-flag override needs watching against real completions so it doesn't fire too often. Log enough to tune it.

---

## 6. What design should NOT add

- A numeric score, grade, ranking, or percentile anywhere.
- A ninth-area red wall, alarm icons, warning triangles.
- Archetype/persona names.
- Countdown timers, scarcity banners, "only X spots".
- Testimonial slots with invented names or numbers.
- A F.R.E.S.H chart competing with the business snapshot.
