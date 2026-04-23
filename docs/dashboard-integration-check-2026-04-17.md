# Dashboard Integration Validation: Kiranism + shadcn + Next 16

**Date:** 2026-04-17
**Target base:** [Kiranism/next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) (Next.js 16.2.1, React 19.2.4, Tailwind v4.2.2, Recharts 2.15.4, TanStack Table 8.21.3, TanStack Query 5.95.2, nuqs 2.8.9, Clerk 6.39.1)
**Verdict:** Go, with two caveats.

---

## TL;DR

Yes. The Kiranism + shadcn + Next 16 stack integrates cleanly with every tool in Tracy Harris Co's existing stack, with two caveats: (1) there is no actively maintained ActiveCampaign Node SDK, so we talk to AC v3 via raw `fetch` from Route Handlers (which is fine, the API is clean REST), and (2) every SDK that uses Node APIs (`stripe`, `@hubspot/api-client`, `googleapis`) must run on the Node runtime, not Edge. Next 16's stable Node middleware runtime and the template's default `runtime = 'nodejs'` handle this by default. Everything else (PostHog HogQL, Fathom, Fireflies, SamCart) is a REST/GraphQL call from a Server Component or Route Handler. No dead-ends.

---

## Per-tool compatibility

| Tool | Grade | Pattern | Auth | Runtime | Notes |
|---|---|---|---|---|---|
| **PostHog Cloud EU (HogQL)** | A | `fetch` → `/api/projects/:id/query/` from Server Component | Bearer personal API key | Node or Edge | Rate limit **120/hr** on free tier, request higher limit for prod ([docs](https://posthog.com/docs/api/queries)) |
| **ActiveCampaign v3** | B | Raw `fetch` from Route Handler | `Api-Token` header | Node or Edge | No maintained Node SDK. API is clean. **5 req/sec** limit ([docs](https://developers.activecampaign.com/reference/rate-limits)) |
| **Stripe** | A | `stripe-node` in Server Action / Route Handler | Secret key | **Node only** (or `createFetchHttpClient()` for Edge) | SDK mature. Template already Node runtime by default ([npm](https://www.npmjs.com/package/stripe)) |
| **HubSpot** | A | `@hubspot/api-client` v13.5.0 | Private App token | **Node only** (CORS blocked, server-only by design) | Built-in rate limiting + retries ([npm](https://www.npmjs.com/package/@hubspot/api-client)) |
| **Gmail / Calendar** | A | `googleapis` Node SDK | OAuth2 | Node only | Token refresh handled by SDK |
| **Slack / Discord** | A | REST via `fetch` or `@slack/web-api` | Bot token | Node preferred | Slack SDK works cleanly |
| **Fathom** | A | `fetch` → `https://api.usefathom.com/v1` | Bearer token | Node or Edge | Good for 2-4wk parallel comparison widget ([docs](https://usefathom.com/api)) |
| **Fireflies** | A | GraphQL POST → `https://api.fireflies.ai/graphql` | Bearer API key | Node or Edge | Same key path as current MCP ([docs](https://docs.fireflies.ai/graphql-api/query/transcript)) |
| **SamCart** | B | REST via `fetch` | API token | Node or Edge | API mature as of Jan 2026 (partial refunds, Stripe plan IDs added) ([docs](https://developer.samcart.com)) |
| **Cloudflare / Vercel** | A | Template deploys to Vercel out of box | n/a | Node | No Edge surprises if we keep Node runtime |
| **Tailwind v4** | A | `@theme` block in CSS | n/a | n/a | Our aztek/sage/oatmeal tokens port via `--color-aztek: #...` in `@theme` ([docs](https://tailwindcss.com/docs/theme)) |

---

## Pattern examples

### PostHog HogQL from a Server Component (correct)

```tsx
// app/admin/recipes/page.tsx
// Server Component. Key stays on server. No "use client".
export default async function RecipesPage() {
  const res = await fetch(
    `${process.env.POSTHOG_HOST}/api/projects/${process.env.POSTHOG_PROJECT_ID}/query/`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${process.env.POSTHOG_PERSONAL_API_KEY}`,
      },
      body: JSON.stringify({
        query: {
          kind: 'HogQLQuery',
          query: `SELECT properties.recipe_id, count() AS views
                  FROM events
                  WHERE event = '$pageview' AND timestamp > now() - INTERVAL 30 DAY
                  GROUP BY properties.recipe_id
                  ORDER BY views DESC LIMIT 20`,
        },
      }),
      next: { revalidate: 300 }, // 5-min ISR cache, keeps us well under 120/hr
    }
  );
  const { results } = await res.json();
  return <RecipeTable rows={results} />;
}
```

**Anti-pattern (do NOT do):** calling PostHog from a `"use client"` component with `NEXT_PUBLIC_POSTHOG_PERSONAL_KEY`. That exposes the key in the JS bundle. Every key with Query Read permission must be server-side only. Use `process.env.POSTHOG_PERSONAL_API_KEY` (no `NEXT_PUBLIC_` prefix) and call from Server Components or Route Handlers.

### ActiveCampaign, list count from a Server Action

```ts
// app/admin/recipes/actions.ts
'use server';
export async function getListActiveCount(listId: string) {
  const r = await fetch(`${process.env.AC_URL}/api/3/lists/${listId}`, {
    headers: { 'Api-Token': process.env.AC_API_TOKEN!, Accept: 'application/json' },
    next: { revalidate: 600 },
  });
  const { list } = await r.json();
  return { active: list.subscriber_count, total: list.membership_count };
}
```

### Stripe, MRR snapshot from Server Component

```ts
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function getMRR() {
  const subs = await stripe.subscriptions.list({ status: 'active', limit: 100 });
  return subs.data.reduce((sum, s) => sum + (s.items.data[0].price.unit_amount ?? 0), 0) / 100;
}
```

### HubSpot, deal pipeline snapshot

```ts
import { Client } from '@hubspot/api-client';
const hubspot = new Client({ accessToken: process.env.HUBSPOT_TOKEN });

export async function getOpenDeals() {
  const res = await hubspot.crm.deals.searchApi.doSearch({
    filterGroups: [{ filters: [{ propertyName: 'dealstage', operator: 'NEQ', value: 'closedlost' }] }],
    limit: 100,
  });
  return res.results;
}
```

---

## Red flags / gotchas

1. **No maintained ActiveCampaign Node SDK.** The official `activecampaign` npm package hasn't shipped in 7+ years. We write a thin wrapper around `fetch` ourselves. That's ~50 lines and actually cleaner than wrangling an abandoned SDK.
2. **`stripe-node` + Edge Runtime = broken.** The SDK uses Node's `events` module ([GH #43809](https://github.com/vercel/next.js/issues/43809)). Fix: keep Stripe routes on `export const runtime = 'nodejs'` (the template's default). Or call `Stripe.createFetchHttpClient()` if we ever need Edge. Non-issue if we don't touch runtime config.
3. **HubSpot SDK is server-only by design.** CORS-blocked. Can't call from `"use client"`. Force it into a Server Action or Route Handler. This is actually a feature.
4. **PostHog rate limit is 120 queries/hour** on the default personal-key tier. Cache aggressively (`next: { revalidate: 300 }` or `'use cache'` with Next 16 Cache Components). For heavy dashboard use, request a custom limit via PostHog support.
5. **Clerk is the template's default auth.** We already use Google OAuth elsewhere. Either swap Clerk for NextAuth/Auth.js, or keep Clerk and use it (cleaner, their free tier covers an internal admin tool).
6. **Next 16 Cache Components are opt-in.** Default is request-time execution, so dashboard pages won't accidentally serve stale data. Add `'use cache'` only where we want static caching.
7. **No Tailwind v4 migration pain.** Our v4 tokens already exist in `tokens/`, they drop straight into a `@theme` block.

---

## Go / no-go

**Go.** Commit to Kiranism + shadcn + Next 16 + Tailwind v4 as the `/admin/recipes` base. The only tool that needs care is ActiveCampaign (no SDK → write a thin `fetch` wrapper). Everything else has a clean, documented Node.js path.

One decision to make before starting: **Clerk vs. swap for Auth.js.** Recommend keeping Clerk for the internal dashboard. It's one less thing to build and the free tier covers us.

---

## What Kira does next (once Karl greenlights)

1. `gh repo clone Kiranism/next-shadcn-dashboard-starter tracy-admin` into the website monorepo.
2. `pnpm install`. Confirm Node 20+.
3. Create `.env.local` with: `POSTHOG_HOST`, `POSTHOG_PROJECT_ID`, `POSTHOG_PERSONAL_API_KEY`, `AC_URL`, `AC_API_TOKEN`, `STRIPE_SECRET_KEY`, `HUBSPOT_TOKEN`, `FATHOM_TOKEN`, `FIREFLIES_API_KEY`, `SAMCART_TOKEN`, plus Clerk keys.
4. Delete the template's demo dashboard pages. Keep the shell (sidebar, header, theme switcher).
5. Port our aztek/sage/oatmeal tokens into `app/globals.css` inside `@theme`.
6. First Route Handler: `app/api/recipes/route.ts`, HogQL query by `recipe_id`. Ship a table view.
7. Then a `@hubspot/api-client` deal-pipeline card, then a Stripe MRR card, then the AC list-health card.
8. Deploy to Vercel (`tracy-admin.vercel.app`), gate behind Clerk org membership.

Estimated total integration time for all 4 priority-1+2 tools into functioning dashboard widgets: **10-14 hours**.

---

## Sources

- [Next.js 16 release notes](https://nextjs.org/blog/next-16)
- [Next.js 16 Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers)
- [Kiranism next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter)
- [PostHog Query API](https://posthog.com/docs/api/query) | [API queries / rate limits](https://posthog.com/docs/api/queries)
- [ActiveCampaign rate limits](https://developers.activecampaign.com/reference/rate-limits) | [API overview](https://developers.activecampaign.com/reference/overview)
- [stripe npm](https://www.npmjs.com/package/stripe) | [Stripe Edge compatibility issue](https://github.com/vercel/next.js/issues/43809)
- [@hubspot/api-client npm](https://www.npmjs.com/package/@hubspot/api-client)
- [Fathom Analytics API](https://usefathom.com/docs/features/api)
- [Fireflies GraphQL API](https://docs.fireflies.ai/graphql-api/query/transcript)
- [SamCart developer docs](https://developer.samcart.com/)
- [Tailwind v4 @theme](https://tailwindcss.com/docs/theme) | [Tailwind v4 release](https://tailwindcss.com/blog/tailwindcss-v4)

---

## Addendum: deploy platform, Netlify + Cloudflare, not Vercel

**Corrected after agent's original pass.** Tracy Harris Co deploys on **Netlify** (primary) and **Cloudflare** (CDN / edge). Not Vercel. The verdict above holds but the deploy path changes materially.

### Netlify as primary deploy target, recommended

**Grade: A.** Netlify ships a first-class Next.js adapter ([docs](https://docs.netlify.com/frameworks/next-js/)) with full SSR, Route Handlers, and Node runtime support. Every SDK in the priority 1+2 list (`stripe`, `@hubspot/api-client`, `posthog-node`, the `fetch` wrapper for AC) runs on **Netlify Functions = Node runtime** by default. Zero special handling needed vs Vercel.

Caveat: Netlify's ISR/On-Demand Revalidation works but uses their Blobs storage; set `revalidate` on fetches and it's transparent.

### Cloudflare Pages, viable for static + edge only

**Grade: C for this dashboard, A for the static brand-kit.** Cloudflare Pages runs Next.js via [OpenNext](https://opennext.js.org/cloudflare) or [@cloudflare/next-on-pages](https://github.com/cloudflare/next-on-pages), but:

- `stripe-node` won't load on Workers (Edge). Workaround: use Stripe's `fetch`-based API directly from a Worker, OR enable [Node compatibility flags](https://developers.cloudflare.com/workers/runtime-apis/nodejs/), works for most cases but adds friction.
- `@hubspot/api-client` has similar Node dependency. Same workaround.
- `posthog-node` works on Cloudflare Workers natively.
- No filesystem, no long-running background jobs (use Durable Objects if needed).

**Use Cloudflare for:**
- The existing brand kit static site (already works, GH Pages + CF CDN)
- Workers for the `/vault/*` redirect, edge rewrites, image transforms
- Tunneling / reverse proxy / DDoS / caching

**Don't use Cloudflare for:**
- The `/admin/recipes` dashboard, deploy that on Netlify where every SDK just works

### Go recipe for `/admin/recipes`

Deploy the Kiranism clone to **Netlify** at `dashboard.tracyharris.com.au` (or a subdomain of it). Cloudflare sits in front as CDN + DNS + WAF as it does today for the rest of the stack. That's the cleanest split: Netlify runs the Node-heavy dashboard, Cloudflare owns the edge.

### `next.config.ts` additions on Netlify

```ts
export default {
  images: { unoptimized: false },
  // Prefer Node runtime for Route Handlers that hit Stripe, HubSpot, AC
  experimental: { serverActions: { bodySizeLimit: '2mb' } },
}
```

Route Handlers that call PostHog / AC / Stripe should explicitly declare `export const runtime = 'nodejs'` at the top, defensive against Next defaulting to Edge in future versions.

### References

- [Netlify Next.js docs](https://docs.netlify.com/frameworks/next-js/)
- [Cloudflare Pages Next.js](https://developers.cloudflare.com/pages/framework-guides/nextjs/)
- [OpenNext for Cloudflare](https://opennext.js.org/cloudflare)
- [Next.js runtime config](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#runtime)
