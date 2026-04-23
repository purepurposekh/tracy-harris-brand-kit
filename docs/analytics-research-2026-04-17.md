# Analytics Stack Research, Tracy Harris Co
*Conducted 2026-04-17 for Karl Harris. Triple-checking the PostHog recommendation.*

## TL;DR

**Yes, PostHog is the right pick, but use PostHog Cloud, not self-hosted.** Everything Tracy Harris Co needs (MIT-licensed data layer, full HogQL/SQL API, arbitrary event properties like `recipe_id`, funnels, session replay, Next.js/Vercel SDK, Cloudflare-friendly reverse proxy) ships in the free tier. At our traffic volume we'll almost certainly stay free forever.

Self-hosting PostHog would be a strategic mistake at our scale. PostHog only recommends self-hosting up to ~300k events/month, they sunset Helm support, and it needs Postgres + Redis + ClickHouse + Kafka running. Cloud is cheaper, more reliable, and the data is just as exportable. **Ownership isn't about hosting; it's about the API surface**, and PostHog's API gives raw SQL over ClickHouse via HogQL.

The only candidate that gave a real moment of hesitation: **Rybbit** (AGPL, active, feature parity self-hosted vs cloud). If we're philosophically committed to running our own infra, Rybbit is the pick. For everything else, PostHog wins.

## Scored comparison matrix

Grades: A = best-in-class, B = solid, C = workable with compromise, D = avoid.

| Dimension | PostHog | Plausible CE | Umami | Matomo | Rybbit | OpenPanel | Snowplow + CH |
|---|---|---|---|---|---|---|---|
| Data ownership | A (both) | A (self) | A (self) | A (self) | A (both) | A (both) | A (self) |
| SQL / API access | **A** (HogQL via API) | C (Stats API only, 2-prop limit) | B (REST + Postgres) | B (SQL on MySQL) | B | B | **A** (raw warehouse) |
| Custom dashboard | A (embed, API, JSON insights) | C (dashboard is the product) | B | B | B | B | A (BYO) |
| `recipe_id` props | A (unlimited, queryable) | C (2 props max) | B | A | A | A | A |
| Session replay | A (5k free/mo) | None | None | Paid plugin | A (OSS) | A | No (BYO) |
| Funnels/cohorts | A | C (paywalled in CE) | C (recent, basic) | B | A | A | BYO |
| Self-host ops burden | D (PG+Redis+CH+Kafka) | B | A | C | B | B | D |
| Scaling 100k → 10M/mo | A (cloud); struggles >300k self-host | B | B | B | B | B | A |
| Licence risk | B (MIT core + EE dir, stable since 2020) | C (AGPL + paywalled features) | B (MIT) | B (GPLv3) | B (AGPL) | B (AGPL) | B |
| JS snippet size | C (~45-70KB) | **A** (<1KB) | A (~2KB) | C (~22KB) | A | B | varies |
| Privacy / GDPR | B (cookieless mode available) | A (cookieless default) | A | B | A | A | BYO |
| Community momentum | A (29k+ stars) | A (22k+) | A (24k+) | B | B (8k+, growing) | C | B |
| Vercel/Next/CF fit | A (official integration) | B | B | C | B | B | C |

## Why PostHog wins

**1. We need SQL, not dashboards.** Reason for doing this is building a custom dashboard keyed on `recipe_id`. PostHog's HogQL exposes `POST /api/projects/:id/query` accepting ClickHouse SQL over raw events. No other candidate exposes raw analytics-grade SQL through a clean API. Plausible's Stats API limits custom-property dimensions to `url` and `path`, disqualifying for recipe attribution.

**2. Recipe-level attribution is literally what it does.**
```
posthog.capture('$pageview', { recipe_id: 'rcp_abc' })
```
Then HogQL:
```sql
SELECT properties.recipe_id, count() AS views,
       countIf(event='apply_click') AS applies
FROM events
WHERE timestamp > now() - interval 30 day
GROUP BY properties.recipe_id
```
That's the whole system.

**3. Vercel/Next.js/Cloudflare fit is first-class.** Official Vercel Marketplace integration auto-configures env vars; Next.js App Router docs cover reverse-proxy via `next.config.js` rewrites (important so ad-blockers don't nuke events).

**4. Cost curve.** Free up to 1M events/mo. tracyharris.co (20-60k monthly visitors × 2-4 events) sits inside the free tier comfortably. Even at 10× that, we'd pay ~$50/mo with a hard spend cap.

**Where PostHog loses:** JS bundle weight. Mitigations: slim bundle, lazy-load extensions, or `posthog-js-lite` for capture-only.

## Self-hosted vs cloud, cloud wins

With PostHog Cloud we already own the data. API identical. Can export events, stream to S3, query via HogQL. Data lives on their ClickHouse instead of ours, but the access surface doesn't change.

What we'd lose by self-hosting:
- $40-80/mo VPS (Hetzner CCX23 or equivalent)
- 2-5 hours/month babysitting ClickHouse compaction, Kafka lag, Postgres disk
- PostHog's own recommendation: self-host only up to ~300k events/mo
- Helm chart support sunsetted; Docker Compose "hobby" deploy is the only blessed path
- No vendor support

Only do this with regulatory/sovereignty requirements. Tracy Harris Co doesn't have them.

## "Build your own" (Snowplow / ClickHouse / Grafana), no

10-20× the engineering cost of PostHog and buys nothing we'll actually use. Snowplow was designed for 100M+ events/day with custom entity validation. We're tracking pageviews, clicks, opt-ins, and recipe attribution. Revisit only if we cross 50M events/mo or outgrow the product analytics shape entirely.

## Red flags / gotchas

- **PostHog sunset Helm chart self-hosting** (late 2024 / early 2025). Docker Compose "hobby" deploy is the only supported self-host path, explicitly a hobby tier.
- **PostHog bundle size ~45-70 KB** gzip core. Lazy-load everything.
- **Plausible CE is deliberately crippled.** Funnels and ecommerce stay behind paid Cloud even on CE.
- **Umami funnels are recent and basic.**
- **Matomo plugin tax.** Session recordings, heatmaps, A/B tests all paid add-ons. PHP. Opex pain.
- **Rybbit is young.** 8k stars, fast-moving, no enterprise scar tissue yet. Good for philosophical AGPL self-host, but more career risk than PostHog.
- **Session replay is a PII minefield.** Mask all form inputs, especially Apply/Opt-in. PostHog has `data-ph-no-capture`.

No licence drift drama found on PostHog as of April 2026. Core still MIT, `ee/` directory under Enterprise License (unchanged since 2020).

## Implementation sketch

1. **PostHog Cloud** (EU region for GDPR, since Tracy has UK/EU audience). Sign up, get `NEXT_PUBLIC_POSTHOG_KEY` and `NEXT_PUBLIC_POSTHOG_HOST`.
2. **Next.js integration**: install `posthog-js` + `posthog-node`. PostHogProvider in `app/providers.tsx`. Reverse proxy rewrites in `next.config.js` so tracking goes through `tracyharris.co/ingest/*` (dodges ad-blockers).
3. **Recipe attribution**: read `data-recipe-id` off `<body>` in app layout, call `posthog.register({ recipe_id })` once per session. Every subsequent event auto-tags.
4. **Custom events**: `posthog.capture('apply_click', { product: 'ffb' })`, `posthog.capture('optin_submit', { form: 'quiz' })`, etc.
5. **Custom dashboard**: Next.js route (e.g. `/admin/recipes`) hits `/api/projects/:id/query` with HogQL, renders with our own charts. Cache in Cloudflare KV or Vercel's data cache, 5-min TTL.
6. **Cost**: $0/mo until ~1M events. Realistic scenario at Tracy's traffic: $0/mo indefinitely. Hard cap set at $20.
7. **Migration from Fathom**: run both in parallel 2-4 weeks, compare numbers, kill Fathom.

## Watch list, reconsider if…

- PostHog relicenses core away from MIT (BSL, Elastic License). What Mongo, Redis, Elastic did. Check the LICENSE file quarterly.
- PostHog free tier drops below 500k events/mo or adds seat fees.
- We cross 5M events/mo. Redo the cloud vs self-host math at that point.
- HogQL API gets flaky. Mitigation: mirror events to our own ClickHouse via PostHog's batch export.
- Rybbit hits 20k stars + ships v1.0. Feature gap might close; AGPL clean self-host becomes realistic.

## Sources

- [PostHog self-host docs](https://posthog.com/docs/self-host)
- [PostHog pricing](https://posthog.com/pricing)
- [HogQL introduction](https://posthog.com/blog/introducing-hogql)
- [PostHog SQL docs](https://posthog.com/docs/sql)
- [PostHog Next.js docs](https://posthog.com/docs/libraries/next-js)
- [Vercel PostHog integration](https://vercel.com/kb/guide/posthog-nextjs-vercel-feature-flags-analytics)
- [PostHog LICENSE](https://github.com/PostHog/posthog/blob/master/LICENSE)
- [Plausible CE intro](https://plausible.io/blog/community-edition)
- [Plausible Stats API + custom props](https://plausible.io/docs/custom-props/introduction)
- [Umami docs](https://docs.umami.is/docs)
- [Rybbit GitHub](https://github.com/rybbit-io/rybbit)
- [OpenPanel open-source comparison](https://openpanel.dev/articles/open-source-web-analytics)
- [Self-hosted analytics: Umami vs Plausible vs Rybbit (Haloy)](https://haloy.dev/blog/self-hosted-analytics-compared)
- [Best self-hosted analytics 2026 (OpenPanel)](https://openpanel.dev/articles/self-hosted-web-analytics)
- [posthog-js bundlephobia](https://bundlephobia.com/package/posthog-js)
- [Snowplow FAQ](https://snowplow.io/snowplow-frequently-asked-questions)

---

**Bottom line**: ship PostHog Cloud this week. Reverse-proxy through our domain, tag events with `recipe_id`, build the dashboard against HogQL.
