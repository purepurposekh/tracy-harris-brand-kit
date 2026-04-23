# Dashboard Templates Research, April 2026

> For: `/admin/recipes` build on `dashboard.tracyharris.com.au`
> Goal: Pick a pre-built template we clone, reskin to Tracy's brand, and drop PostHog HogQL charts into.

---

## TL;DR

**Pick: [`Kiranism/next-shadcn-dashboard-starter`](https://github.com/Kiranism/next-shadcn-dashboard-starter)** (Next.js 16 + shadcn/ui + Tailwind v4 + Recharts, MIT, ~6.3k stars, actively maintained). It ships the exact stack we already run (Next.js App Router on Vercel, Tailwind, shadcn) with parallel-route dashboards, Recharts cards, data tables with React Query prefetch, a proper sidebar layout, and six pre-wired themes. It beats the rest because theming is one `globals.css` edit (shadcn CSS variables via tweakcn), and because PostHog publishes [an official shadcn + Recharts example](https://github.com/PostHog/posthog-shadcn-charts-example) that drops straight in as the `/admin/recipes` query layer.

---

## Shortlist

| Template | Stack | Density | Install | Brand-fit | Chart lib | License | Momentum |
|---|---|---|---|---|---|---|---|
| **Kiranism next-shadcn-dashboard-starter** | Next 16 + shadcn + TW v4 | A, sidebar, tables, charts, kanban, forms, auth | A, `git clone` + `pnpm i` | A, shadcn CSS vars, tweakcn, 6 themes | A, shadcn Chart wraps Recharts | A, MIT | A, 6.3k stars, Next 16 ready [ref](https://github.com/Kiranism/next-shadcn-dashboard-starter) |
| **shadcn/ui Blocks (dashboard-01 + sidebar-07)** | Next + shadcn + TW v4 | B, fewer pages, just blocks | A+, `npx shadcn add dashboard-01` | A, canonical shadcn theming | A, shadcn Chart / Recharts | A, MIT | A, official Vercel, 112k stars [ref](https://ui.shadcn.com/blocks) |
| **TailAdmin Free Next.js** | Next 16 + TW v4 (no shadcn) | A+, 500+ elements, 7 dashboards | B, clone repo | B, Tailwind tokens scattered; pro fonts baked in | C, ApexCharts (heavier, imperative) | B, MIT free, pro $59–$299 | B, 2.3k stars, pro-product feel [ref](https://github.com/TailAdmin/free-nextjs-admin-dashboard) |
| **Tremor (Vercel-owned, copy-paste)** | React + TW + Recharts | C, charts-only, no shell | B, copy components | A, Tailwind classes | A, Recharts, 35+ chart primitives | A, Apache 2.0 | B, 3.4k stars on new repo, mostly merged into Vercel/v0 [ref](https://vercel.com/blog/vercel-acquires-tremor) |
| **Tabler** | Bootstrap 5.3 | A, huge component set | A, static HTML | D, Bootstrap, not Tailwind; font overrides fight theme | C, ApexCharts via community | A, MIT | A, 41k stars, v1.4 July 2025 [ref](https://tabler.io) |
| **Ant Design Pro** | React + Ant + UmiJS | A+, enterprise grade | C, opinionated scaffolding | D, Ant visual language very corporate, hard to soften | B, @ant-design/charts | A, MIT | B, 36k stars, Alibaba [ref](https://pro.ant.design) |
| **Mantis (MUI)** | React + MUI | A, polished | B, MUI ecosystem | D, MUI theming is powerful but heavy; fighting Material for editorial feel | B, Recharts/ApexCharts | B, MIT free, commercial pro | B, CodedThemes, updated Feb 2026 [ref](https://mui.com/store/items/mantis-react-admin-dashboard-template/) |

---

## Deeper look at top 3

### 1. Kiranism next-shadcn-dashboard-starter (THE PICK)

**Install:**
```bash
git clone https://github.com/Kiranism/next-shadcn-dashboard-starter.git admin-recipes
cd admin-recipes && pnpm install
cp env.example.txt .env.local   # Clerk keys optional, can be ripped out
pnpm dev
```

**Ships:** Next.js 16 App Router, Tailwind v4, shadcn/ui (vendored), Recharts via shadcn Chart primitive, TanStack Query (server prefetch + client cache), Zustand, Zod, Clerk (removable), parallel routes with `loading.tsx` per section, Sentry, feature-based folder structure, data tables with search/filter/pagination, kanban, forms, 6 themes with switcher, command palette, breadcrumbs, notifications. Source: [README](https://github.com/Kiranism/next-shadcn-dashboard-starter/blob/main/README.md).

**Tracy brand adaptation:** Because shadcn themes are plain CSS custom properties, the reskin is one file. Use [tweakcn](https://tweakcn.com) to generate OKLCh tokens for `--background` (cream #FAF6EE), `--primary` (aztek #1e3735), `--accent` (sage #6e8e77), `--ring` (gold #c9a46c), paste into `src/app/globals.css`. Swap fonts in the root layout: `Editors Note` for `--font-serif` (display), `Poppins` for `--font-sans` (body), `Jhon Halend` as a utility class for accents. Time: **half a day** to reskin the whole shell.

**PostHog HogQL wiring:** Drop PostHog's [official shadcn charts example](https://github.com/PostHog/posthog-shadcn-charts-example) into `/admin/recipes/page.tsx` as a server component. Use [PostHog's Query API](https://posthog.com/tutorials/recharts):
```ts
// app/admin/recipes/_lib/hogql.ts, runs server-side, key stays secret
export async function hogql(query: string) {
  const r = await fetch(`https://eu.posthog.com/api/projects/${process.env.POSTHOG_PROJECT_ID}/query/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.POSTHOG_PERSONAL_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ query: { kind: "HogQLQuery", query } }),
    next: { revalidate: 300 },
  });
  return r.json();
}
```
Then feed results into shadcn's `<ChartContainer>` + Recharts `<AreaChart>`. TanStack Query already wired for client-side refresh.

**Estimate to ship `/admin/recipes` v1:** **10–14 hours.** 2h clone + strip Clerk/Kanban/Chat. 4h brand reskin. 3h wire one HogQL query for page-recipe conversion. 3h build the recipe table + conversion card grid. 2h polish/deploy.

### 2. shadcn/ui Blocks (dashboard-01 + sidebar-07)

**Install:** `npx shadcn add dashboard-01 sidebar-07 login-04` directly into the existing `dashboard.tracyharris.com.au` repo. No new repo, just new routes.

**Ships:** Sidebar shell with collapsible nav, area chart card, stat cards, data table, site header, breadcrumbs, user menu. That's it, you're meant to compose from [the block library](https://ui.shadcn.com/blocks).

**Tracy brand adaptation:** Same theming mechanism as above. Upside: no wholesale starter to strip, so less waste. Downside: no kanban/auth/notifications pre-built, but we don't need them for recipes anyway.

**PostHog wiring:** Identical pattern to option 1. Use same `hogql()` helper.

**Estimate:** **8–12 hours** if we stay in the existing dashboard repo. Simplest of all paths because no cloning.

**Why this is 2nd not 1st:** Karl asked for "multiple templates with lots of components we can sub in easily." Raw blocks give less upfront than Kiranism's starter. But if simplicity wins, this is the cleaner choice.

### 3. TailAdmin Free Next.js

**Install:** `git clone https://github.com/TailAdmin/free-nextjs-admin-dashboard.git`

**Ships:** 200+ UI components, 7 dashboard layouts (Analytics, Ecommerce, Marketing, CRM, SaaS, Stocks, Logistics), ApexCharts, Flatpickr, calendar, data tables, auth flows, forms, profiles, [source](https://github.com/TailAdmin/free-nextjs-admin-dashboard).

**Tracy brand adaptation:** Harder. Tailwind is raw (no shadcn CSS-variable system), which means colour tokens are scattered across component files rather than centralised. ApexCharts also has its own theme object you have to mirror. Plan ~2 days for a brand-faithful reskin.

**PostHog wiring:** Same `hogql()` server helper works, but you'll swap the chart JSX to ApexCharts' imperative config pattern. Less pleasant for Server Components.

**Estimate:** **20–28 hours.** More components out of the box but more reskinning friction.

---

## Red flags

- **Tremor standalone is not a dashboard template**, it's just chart primitives. The [Vercel acquisition](https://vercel.com/blog/vercel-acquires-tremor) merged the team into Vercel Design Engineering; public Tremor repo commits slowed (last stable v3.18.7 Jan 2025). Use Tremor blocks as *inspiration*, not infrastructure. Recharts + shadcn Chart gives you 90% of Tremor now anyway.
- **Tabler is Bootstrap.** Means fighting Bootstrap's default typography, spacing, and jQuery patterns to get editorial/quiet. Wrong tool for Tracy's brand. Skip.
- **Ant Design Pro is enterprise banking aesthetic.** You cannot soften it into "cream editorial" in a day. It's a fantastic template for the wrong brand.
- **Mantis / Material Dashboard**, MUI's emotional baseline is "Google product." Theming is possible but heavy; density defaults feel corporate. Wrong fit.
- **Shipfast / Makerkit / Supastarter**, these are SaaS starter kits (auth + billing + onboarding), not dashboard templates. Their admin views are thin. Overkill for an internal analytics dashboard, and `dashboard.tracyharris.com.au` already exists. Skip.
- **shadcn/ui's "you own the code" trap**, [well-documented](https://leonardomontini.dev/shadcn-ui-use-with-caution/). When a component has a bug, no npm update fixes it. Mitigation: we only copy blocks we actually use, and we pin the shadcn CLI version.
- **PostHog tutorial example** uses a client-side fetch with the API key exposed, [they warn against this](https://posthog.com/tutorials/recharts). Always call the Query API from a Next.js Route Handler or Server Component. Never ship the personal API key to the browser.

---

## Recommendation + implementation sketch

**Clone Kiranism's starter as a new app in the existing `dashboard.tracyharris.com.au` monorepo** (or as `/admin/recipes` inside it if you want a single-app setup).

**First 3 tasks after clone:**
1. **Strip the noise.** Delete `/kanban`, `/chat`, `/products`, `/profile`, Clerk integration (replace with existing dashboard auth), and sample data files. Keep: sidebar, overview layout, parallel routes, data tables, Chart primitive.
2. **Reskin to Tracy.** Paste brand tokens into `src/app/globals.css` (cream/aztek/sage/gold via tweakcn). Swap sans to Poppins, serif to Editors Note, add Jhon Halend utility class. Update sidebar copy + logo.
3. **Wire the first HogQL query.** Create `app/admin/recipes/_lib/hogql.ts` with the server helper above. First query: `SELECT properties.$pathname, count() AS views, countIf(event = 'quiz_start') AS starts FROM events WHERE timestamp > now() - INTERVAL 30 DAY GROUP BY properties.$pathname ORDER BY views DESC`. Render as a shadcn `<DataTable>` + conversion-rate column + `<AreaChart>` overview card.

**Components to wire first for PostHog recipe dashboard:**
- `<StatCard>` row, total page views, total quiz starts, overall conversion rate, trend arrow
- `<ChartContainer>` with `<AreaChart>`, 30-day conversion trend
- `<DataTable>`, per-page recipe breakdown with sort/filter/pagination (TanStack Table already in starter)
- `<Sheet>` drawer, click-through to per-page detail view with a second HogQL query

---

## "Reconsider if..."

- **If Karl wants zero setup and is happy composing as we go** → drop Kiranism, go shadcn Blocks direct (option 2). Saves the cloning/stripping step.
- **If we need 7+ distinct admin views (finance, scenarios, recipes, members, podcast, launches, retreats) fast** → TailAdmin's 7 pre-built dashboards become worth the reskin cost.
- **If PostHog releases a first-party Next.js dashboard SDK** (the `@posthog/next` package is pre-release as of April 2026 [ref](https://posthog.com/docs/libraries/next-js)) → re-evaluate. Might make custom HogQL dashboards unnecessary.
- **If charts get exotic** (sankey, network graph, heatmap) → Recharts/shadcn Chart runs out of range. Swap to [Visx](https://airbnb.io/visx/) or D3 inside the same shell.
- **If we want Tremor's specific chart style back** → copy individual Tremor blocks from [tremor.so](https://tremor.so) into the Kiranism shell. They coexist cleanly since both use Tailwind + Recharts.

---

## Sources

- [Kiranism next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter), the pick
- [shadcn/ui Blocks](https://ui.shadcn.com/blocks), official block library, dashboard-01, sidebar-07
- [PostHog shadcn charts example](https://github.com/PostHog/posthog-shadcn-charts-example), PostHog's own integration reference
- [PostHog Recharts tutorial](https://posthog.com/tutorials/recharts), Query API + HogQLQuery payload pattern
- [Vercel acquires Tremor](https://vercel.com/blog/vercel-acquires-tremor), context on Tremor's future
- [tweakcn theme generator](https://tweakcn.com), OKLCh shadcn theme builder
- [TailAdmin Next.js](https://github.com/TailAdmin/free-nextjs-admin-dashboard), runner-up
- [Tabler](https://tabler.io), rejected, Bootstrap
- [Ant Design Pro](https://pro.ant.design), rejected, enterprise aesthetic
- [shadcn/ui caveats](https://leonardomontini.dev/shadcn-ui-use-with-caution/), the copy-paste trap
- [AdminLTE 2026 roundup: 7 Next.js 16 shadcn admin dashboards](https://adminlte.io/blog/nextjs-admin-dashboards-shadcn/)
- [thefrontkit 2026 comparison: 10 shadcn dashboard templates](https://thefrontkit.com/blogs/best-shadcn-dashboard-templates-2026)
