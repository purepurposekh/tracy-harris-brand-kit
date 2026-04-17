# Dashboard Moodboard, 2026-04-17

> Visual reference set for the Tracy Harris Co internal dashboard rebuild. Curated against Karl's brief: clean, professional, whitespace-heavy, bento. Not playtoy. Not corporate-bank.

**Brief from Karl:**
> "Looks too much like a play toy, kid-like. Not serious. Like things to be clean and professional but I do like white space and the bento look."

**Current dashboard:** `dashboard.tracyharris.com.au`. Next.js 16, shadcn, Tailwind v4, Recharts. Brand palette (aztek green, sage, gold, oatmeal). Editors Note serif + Poppins.

---

## The 5 picks (ranked best fit first)

### 1. Linear, Dashboards + the 2026 UI refresh

- **Live:** [linear.app](https://linear.app/), [Dashboards best practices](https://linear.app/now/dashboards-best-practices), [UI refresh changelog (2026-03-12)](https://linear.app/changelog/2026-03-12-ui-refresh), [Behind the design refresh](https://linear.app/now/behind-the-latest-design-refresh)
- **Distinctive feel:** Calm, monochrome with a single restrained accent. Warmer grays in 2026 (less saturated, less "tech-bro"). Custom Inter Display sets the tone. Bento dashboard cards are large, rounded, asymmetric, surrounded by air.
- **Screenshot:** [Linear Dashboards hero on linear.app/now](https://linear.app/now/dashboards-best-practices). Scroll to "Dashboard examples".
- **Why it fits Karl's brief:** Hits every bullet. Generous whitespace, bento cards of varied size, restrained palette (grayscale plus one accent), confident sans typography. Reads grown-up. Their changelog itself uses bento (big tile = big release, small tile = bug fix), which is how a Tracy Harris Co dashboard should treat KPIs. Revenue gets a big tile. Mailing list churn gets a small one.
- **Tracy adaptation:** Swap Linear's cool gray for our **oatmeal canvas (#F4EFE8)**. Cards in soft cream (#FAF7F1) with a 1px hairline border in sage. Aztek green as the single accent (active states, primary numbers). Editors Note for the big metric numbers (e.g. "$48,200 MRR" set in serif at 56 to 72px), Poppins for everything else. No drop shadows, borders only.
- **Complexity:** **S.** This is essentially shadcn cards with bigger spacing, larger numbers, fewer colours. Mostly tokens and layout work, not a rewrite.

### 2. Vercel, Dashboard redesign (Feb 2026 rollout)

- **Live:** [vercel.com/dashboard](https://vercel.com/dashboard), [Dashboard redesign blog](https://vercel.com/blog/dashboard-redesign), [Rollout changelog](https://vercel.com/changelog/dashboard-navigation-redesign-rollout), [The New Side of Vercel](https://vercel.com/try/new-dashboard)
- **Distinctive feel:** Pure white plus pure black, monochrome precision, geometric sans (Geist). Sidebar is the workhorse. Cards are flat with hairline borders, no shadows. Project as a filter, not a modal. Mobile has a floating bottom bar.
- **Screenshot:** [Dashboard redesign blog hero](https://vercel.com/blog/dashboard-redesign) (image embedded at top of post)
- **Why it fits:** This is the platonic ideal of "clean and serious." Karl will recognise the restraint instantly. The mobile floating-action-bar pattern alone is worth stealing.
- **Tracy adaptation:** Replace the cold black with our **deep aztek green (#1F3A2E)** for primary text. Pure white surfaces become **cream (#FAF7F1)**. Geist becomes Poppins (already very close in character). Add Editors Note italic for section headers ("*Revenue this month*") to soften the sharpness. That is the move that makes it feel like Tracy's brand and not a developer tool.
- **Complexity:** **M.** Sidebar redesign is real work. Mobile floating bar is a new pattern.

### 3. Stripe, Dashboard

- **Live:** [dashboard.stripe.com](https://dashboard.stripe.com) (auth-walled), [Stripe Apps style docs](https://docs.stripe.com/stripe-apps/style), [SaaSFrame Stripe dashboard reference](https://www.saasframe.io/examples/stripe-payments-dashboard), [Dribbble: Stripe dashboard shots](https://dribbble.com/search/stripe-dashboard)
- **Distinctive feel:** Editorial typography (Sohne / Stripe Sans), restrained gradient accents, big numbers up top, dense but never cramped. Tables done right. Tabs and filters are quiet, not shouty.
- **Screenshot:** [Stripe payments dashboard reference, SaaSFrame](https://www.saasframe.io/examples/stripe-payments-dashboard). Public, post-auth screenshot.
- **Why it fits:** This is the gold standard for "polished without being corporate." Looks expensive without trying. Tracy is a premium brand, her dashboard should feel like she could charge $31K for a mastermind without flinching.
- **Tracy adaptation:** Keep Stripe's "big number, small label, tiny delta indicator" pattern verbatim. Use **gold (#C99B5C)** for the delta-up arrows. Lean into our serif for hero numbers. Keep tables but use 14px Poppins, generous row padding (16 to 20px), no zebra striping, just hairlines.
- **Complexity:** **M.** Number presentation is easy. Getting the table aesthetic right takes a couple of passes.

### 4. Plausible Analytics, Dashboard

- **Live:** [plausible.io](https://plausible.io/), [Live demo dashboard](https://plausible.io/plausible.io), [Guided tour](https://plausible.io/docs/guided-tour)
- **Distinctive feel:** Single page, no sub-menus, no tabs. Sparse and confident. One chart, then a row of dimension cards. Inter throughout, almost no colour. Open-source so the whole thing is inspectable.
- **Screenshot:** [Live demo (plausible.io/plausible.io)](https://plausible.io/plausible.io). Interactive, current.
- **Why it fits:** This is the answer to "what does it look like when you remove every non-essential element from an analytics dashboard?" Pure whitespace philosophy. Deeply un-toylike.
- **Tracy adaptation:** Plausible is almost too sparse for Tracy's brand, needs warming up. Keep the single-page-no-submenus structure. Replace Plausible's blue with sage. Add an editorial header band ("*Tracy Harris Co* · Performance · April 2026") in Editors Note italic to give it personality. Don't ape the chart-then-cards layout exactly, go bento on the cards.
- **Complexity:** **S.** Mostly subtractive. Delete things from the current dashboard until it looks like this.

### 5. Cal.com, Dashboard + design system

- **Live:** [cal.com](https://cal.com/), [Public design system](https://design.cal.com/), [Dashboard (auth)](https://app.cal.com/event-types)
- **Distinctive feel:** Lighter, friendlier than Linear or Vercel but still grown-up. Open-source. Strong empty states. Their event-types dashboard is genuinely bento (each event type is a card, varied sizes, varied content). Inter plus a touch of warmth.
- **Screenshot:** [design.cal.com components page](https://design.cal.com/) shows live cards.
- **Why it fits:** Closest to Tracy's brand temperature of all five. Warm, human, but not cute. Empty states have personality, that's a Tracy move.
- **Tracy adaptation:** Cal.com's structure is basically already there in our shadcn setup. The win is in their empty states and onboarding cards. Write those in Tracy's voice ("*Nothing in the pipeline yet, lovely. Add your first launch event below.*"). Borrow their card sizing logic.
- **Complexity:** **S to M.** Borrow patterns, not the full system.

---

## What to avoid (3 explicit "not this")

### Avoid 1: Neumorphism dashboards (the puffy soft-shadow look)

- **Reference:** [Neumorphism Dashboard, Marcus on Medium](https://medium.com/@studie-gelatine0z/neumorphism-dashboard-design-21e0aecc5356), [BigHuman 2026 guide](https://www.bighuman.com/blog/neumorphism)
- **Why avoid:** Soft puffy shadows plus low contrast equals the literal definition of "playtoy, kid-like." Accessibility nightmare. This is exactly what Karl is calling out.

### Avoid 2: Bloomberg / corporate-bank density (Datadog-heavy)

- **Reference:** [Datadog dashboard examples](https://www.datadoghq.com/dashboards/). 14 charts on screen, 12 colours, dense tables, tiny type. Bloomberg Terminal energy.
- **Why avoid:** Karl already said no. Tracy's dashboard tracks ~20 numbers that matter, not 200. Density signals "engineer built this for myself," not "founder runs this business."

### Avoid 3: Bright-gradient SaaS template look (TailAdmin / Material defaults)

- **Reference:** [TailAdmin SaaS templates](https://tailadmin.com/blog/saas-dashboard-templates). Purple-to-pink hero gradients, rainbow Recharts defaults, "Welcome back, John 👋" greeting cards.
- **Why avoid:** Reads as "I downloaded a template." Generic SaaS aesthetic is a tier below Tracy's brand. The 2024 startup look, not the 2026 mature-business look.

---

## Recommendation: go Linear

**The pick: Linear's 2026 dashboard refresh.** It is the cleanest 1:1 match for Karl's brief on every axis (whitespace, bento, restrained palette, grown-up typography), and it is the lowest-effort to reach from where the dashboard sits today. It is shadcn cards, more air, fewer colours, bigger numbers.

**How we get there from current state:**

1. **Spacing.** Bump card padding from 16px to 28 to 32px. Bump grid gap from 16px to 24px. Almost nothing else changes structurally and the dashboard immediately feels twice as expensive.
2. **Typography.** Hero metric numbers move to **Editors Note serif at 56 to 72px**. Section headers in Editors Note italic at 22px. Body stays Poppins. Drop the small-caps eyebrows on cards, too busy.
3. **Colour.** Cut to oatmeal canvas plus cream cards plus aztek green for primary text plus gold for positive deltas. Sage for borders. That is it. Recharts gets one colour per chart, not five.
4. **Bento.** Make the grid asymmetric. One hero card spans 2/3 width (revenue this month, big serif number). Three smaller equal cards underneath (mailing list, podcast downloads, FFM applications). Don't force everything into a 4-up grid.
5. **Chrome.** Remove drop shadows entirely. Replace with 1px hairline borders in sage at 30% opacity. No rounded-2xl, go to rounded-3xl on cards (24px) for the editorial feel.
6. **Charts.** Recharts defaults out. Single-colour line charts, no gridlines, axis labels in 11px Poppins uppercase letterspaced. Tooltips in serif italic.

That is a 1 to 2 day refresh, not a rebuild. Ship it, look at it, then decide if Vercel-style monochrome austerity is the next move or if it's already there.

---

## Sources

- [Linear UI refresh changelog 2026-03-12](https://linear.app/changelog/2026-03-12-ui-refresh)
- [Linear Dashboards best practices](https://linear.app/now/dashboards-best-practices)
- [Linear: Behind the latest design refresh](https://linear.app/now/behind-the-latest-design-refresh)
- [Vercel dashboard redesign blog](https://vercel.com/blog/dashboard-redesign)
- [Vercel dashboard rollout changelog](https://vercel.com/changelog/dashboard-navigation-redesign-rollout)
- [Stripe Apps style guide](https://docs.stripe.com/stripe-apps/style)
- [SaaSFrame: Stripe payments dashboard](https://www.saasframe.io/examples/stripe-payments-dashboard)
- [Plausible live demo dashboard](https://plausible.io/plausible.io)
- [Cal.com design system](https://design.cal.com/)
- [Tailscale admin console (Mobbin)](https://mobbin.com/explore/screens/bedfacb1-958b-40df-999d-308e76d8401f)
- [Bento grid 2026 trend report (SaaSFrame)](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide)
- [Dashboard design dos and donts 2026 (think.design)](https://think.design/blog/dashboard-design-in-2026-dos-and-donts/)
- [Neumorphism 2026 guide (BigHuman)](https://www.bighuman.com/blog/neumorphism)
