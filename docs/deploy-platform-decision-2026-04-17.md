# Deploy Platform Decision: Vercel vs Netlify

**Date:** 2026-04-17
**Author:** Kira
**Context:** Karl choosing deploy target for the new `/admin/recipes` dashboard (Next.js 16 + shadcn + Kiranism starter, pulling PostHog HogQL + ActiveCampaign + Stripe + HubSpot). Single internal user = Karl. Cloudflare stays in front as CDN / DNS / WAF. Recipe-built public pages stay on WordPress at tracyharris.co.

---

## TL;DR

**Stay on Netlify. Keep the Free plan. $0/month.**

The existing `dashboard.tracyharris.com.au` is already deployed to Netlify today (confirmed via live headers: `server: Netlify`, `x-nf-request-id`). All integration env vars already live in the Netlify UI. There is no realistic workload Karl can generate as a single internal user that breaks the Free tier, and Netlify Free explicitly permits commercial use. Zero migration. Zero new billing. Zero new accounts.

Vercel Hobby is legally unusable for Tracy Harris Co (non-commercial clause). Vercel Pro at $20/mo buys no real advantage for this workload.

---

## Part 1, The pick: Netlify (unchanged)

1. **It's already there.** Dashboard is on Netlify today. Env vars, build config, DNS, Cloudflare front-proxy, all working. Switching platforms for this workload is pure cost with no upside.
2. **Free tier allows commercial use.** Netlify Free is legal for a business dashboard. Vercel Hobby is not, Vercel's ToS restricts Hobby to "personal or non-commercial use." Any Tracy Harris Co dashboard on Vercel requires Pro at $20/month on day one.
3. **Next 16 is supported.** Netlify's runtime deploys Next.js 16 today via OpenNext ([Netlify changelog, Oct 2025](https://www.netlify.com/changelog/next-js-16-deploy-on-netlify/)). The official Adapter API (shipped in Next 16.2) is being added this year with zero-config rollout to existing projects.
4. **Every SDK in our stack runs on Node by default.** `stripe`, `@hubspot/api-client`, `posthog-node`, the AC fetch wrapper, all Node runtime, all "just works" on Netlify Functions. No edge-runtime gymnastics. Already validated in `dashboard-integration-check-2026-04-17.md`.
5. **Credentials + infra familiarity.** Kira already holds the Netlify API key (`nfp_REDACTED-revoked`). Karl runs ops across Netlify + Cloudflare already. No new surface area.

---

## Part 2, Exact cost at Tracy's real usage

**Realistic workload for `/admin/recipes`:**
- 1 user (Karl)
- ~20 dashboard page loads per day = ~600/month
- Each page load: 3-5 server-side HogQL calls + AC/Stripe/HubSpot calls = ~25 function invocations per page
- Total function invocations: 600 × 25 = **~15,000/month**
- Bandwidth: mostly JSON responses, some chart renders = **~2-5 GB/month** (conservatively 10 GB)
- Build minutes: 1-3 builds/week × ~3 min = **~40 min/month**

### Netlify Free, what Karl actually gets

| Resource | Free tier limit | Karl's use | Headroom |
|---|---|---|---|
| Bandwidth | 100 GB/month | ~10 GB | 10× |
| Function invocations | 125,000/month | ~15,000 | 8× |
| Edge function invocations | 1,000,000/month | near-zero | massive |
| Build minutes | 300/month | ~40 | 7× |
| Storage | 10 GB | <1 GB | 10× |
| Credits | 300/month (soft cap across all above) | well under | safe |
| Team members | 1 | 1 | fits |
| Commercial use | **Allowed** | yes | legal |

**Cost: $0.00/month. Hard-capped, the site pauses rather than bills.**
Sources: [Netlify Free plan](https://www.netlify.com/blog/introducing-netlify-free-plan/), [Credit-based pricing docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/).

### Netlify Pro (if Karl ever upgraded)
- $20/month, 3,000 credits, unlimited team members.
- Overages: ~$0.13/GB bandwidth, ~$0.10/production deploy.
- Only relevant when Karl adds more team members or hits credit caps. Not today.

### Vercel Hobby, cannot use
- $0/month technically, but **non-commercial personal use only** ([Vercel ToS](https://vercel.com/legal/terms), [Hobby plan docs](https://vercel.com/docs/plans/hobby), [Fair Use](https://vercel.com/docs/limits/fair-use-guidelines)).
- A Tracy Harris Co business dashboard is commercial. Using Hobby here = ToS violation. Policy, not technical.
- **Effective cost to use legally: $20/month Pro minimum.**

### Vercel Pro, what it would cost
- **$20/user/month** base.
- Includes 1 TB bandwidth, 1M function invocations, pay-as-you-go build minutes.
- For Karl's workload: no overages, so flat **$20/month**.
- Net difference vs. Netlify Free: **+$240/year for no additional capability.**

---

## Part 3, Platform × Next 16 / shadcn / Kiranism fit

**Honest assessment: Vercel ships Next.js features first. For this use case, it doesn't matter.**

| Next 16 feature | Vercel | Netlify | Matters to `/admin/recipes`? |
|---|---|---|---|
| App Router / Server Components | Day 0 | Day 0 (via OpenNext) | Yes, both fine |
| Route Handlers (our PostHog/AC/Stripe calls) | Day 0 | Day 0 | Yes, both fine |
| Partial Prerendering (PPR) | Day 0 | Delayed weeks-months | No, admin dashboard, not public content |
| Turbopack builds | Day 0 | Day 0 | No, builds locally identical |
| `after()` / background callbacks | Day 0 | Day 0 | No, not used in Kiranism template |
| Next 16 Adapter API (official) | Day 0 | H2 2026 rollout | No, OpenNext already handles it |
| shadcn/ui + Tailwind v4 | Works | Works | Build-time only, platform-agnostic |
| Recharts / TanStack Query | Works | Works | Pure client/server React, no platform bind |

**Verdict:** Vercel's first-mover advantage on new Next features is real but aimed at production public sites that care about PPR, streaming, edge cache. Karl's dashboard is a logged-in admin tool with 1 user. The Kiranism template doesn't use PPR or experimental features. Every piece of the Kiranism stack runs identically on both.

Source: [Next.js adapter API announcement](https://www.netlify.com/blog/the-next-js-adapter-api-just-shipped-here-s-what-comes-next/), [OpenNext for Netlify](https://github.com/opennextjs/opennextjs-netlify).

---

## Part 4, Cloudflare integration

Both platforms sit cleanly behind Cloudflare. No platform-specific gotchas for this setup.

**Current working setup (Netlify + Cloudflare):**
- Cloudflare DNS: CNAME `dashboard.tracyharris.com.au` → Netlify.
- SSL: Cloudflare terminates at the edge, Netlify also has its own cert. "Full (strict)" mode works.
- Caching: dashboard is auth-gated, so Cloudflare page rules set `Cache-Level: Bypass` on `/admin/*` routes. Static assets (`/_next/static/*`) cache at the edge.

**If we switched to Vercel:**
- Vercel's auto-HTTPS conflicts with Cloudflare proxy orange-cloud by default. You either grey-cloud the record (losing WAF + CDN benefits) or configure Vercel's CNAME + set Cloudflare to Full strict. Well-documented but one more config step.
- Vercel's `x-vercel-cache` headers interact with Cloudflare cache rules differently. Usually fine. Occasionally surprising.

**Neither is a blocker. Netlify's current setup is zero-friction.**

---

## Part 5, Migration risk

**If we picked Netlify and later wanted Vercel:** ~1 day effort.
- Re-create env vars in Vercel UI (can export from Netlify).
- Update Cloudflare DNS CNAME.
- Rebuild, Next.js code is platform-agnostic via the Adapter API.
- Clerk sessions: keyed by Clerk, not by platform, so sessions persist.
- Database connections: env-var-driven, portable.
- **Nothing is locked in.** Both platforms read the same `next.config.ts` and `package.json`.

**If we picked Vercel and later wanted Netlify:** Same ~1 day.

The Next.js Adapter API (stable in 16.2) explicitly exists to make this portable. Neither vendor can lock us in at this layer.

**The only real lock-in risk is Vercel-specific primitives if we started using them:** Edge Config, Vercel KV, Vercel Postgres, `@vercel/analytics`, Vercel Blob. Don't use any of these and migration stays cheap. The Kiranism starter uses none of them.

---

## Part 6, The recommendation

**Stay on Netlify Free indefinitely.**

Deploy the `/admin/recipes` dashboard to the existing Netlify project at `dashboard.tracyharris.com.au`. No new accounts, no new billing, no new DNS records, no migration. Env vars are already there.

**Cost: $0/month, indefinitely, at Karl's realistic usage.**

### The "reconsider if" triggers

Flip to Netlify Pro ($20/mo) only when one of these hits:
- **Team grows.** Second person (Lisa, VA, Tracy) needs dashboard access with their own account.
- **Usage explodes.** Workshop-day bursts push function invocations past ~100k/mo or bandwidth past 70 GB/mo. Unlikely for an internal tool.
- **Build minutes tight.** If we push to dashboard >10×/day during active dev sprints, we might brush the 300 min/mo cap. Easy to monitor.

Don't flip to Vercel unless:
- **PPR becomes critical for a public site** (not the admin dashboard, the public tracyharris.co rebuild on Next instead of WordPress, if that ever happens). At that point, evaluate fresh on the public workload.

---

## Appendix: What I verified live

- `curl -I https://dashboard.tracyharris.com.au/` → `server: Netlify`, `x-nf-request-id: 01KPCTE6RS5YJBWE6B3R2ANTGD`, confirmed current host.
- Memory (`project_dashboard_status.md`): "Key Env Vars (all in Netlify UI)", already configured.
- `dashboard-integration-check-2026-04-17.md` line 164 addendum: Netlify is already the verified target for this workload.
- Vercel ToS: [vercel.com/legal/terms](https://vercel.com/legal/terms), [Hobby plan](https://vercel.com/docs/plans/hobby), [Fair Use Guidelines](https://vercel.com/docs/limits/fair-use-guidelines).
- Netlify Free plan: [Netlify Free announcement](https://www.netlify.com/blog/introducing-netlify-free-plan/), [credit docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/).
- Next 16 on Netlify: [Netlify changelog](https://www.netlify.com/changelog/next-js-16-deploy-on-netlify/).
