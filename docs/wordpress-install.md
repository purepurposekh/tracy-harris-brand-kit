# Installing PostHog on tracyharris.co (WordPress)

**Project**: Tracy Harris Co
**Region**: PostHog Cloud EU
**Project API Key**: `phc_yvn2WdBhF8fZYpQExJbXpJg7Y6ivVbpy7uect6zgWgK8`
**Project ID**: 160809

## The single snippet

Paste this into your WordPress site header. Two ways:

### Option A — "Insert Headers and Footers" plugin (easiest, 2 minutes)

1. WP admin → Plugins → Add New → search "Insert Headers and Footers" (by WPBeginner) → Install & Activate
2. Settings → Insert Headers and Footers
3. Paste into the "Scripts in Header" box:

```html
<script src="https://purepurposekh.github.io/tracy-harris-brand-kit/assets/js/thc-analytics.js"></script>
```

4. Save. Done. PostHog now tracks every page on tracyharris.co.

### Option B — direct edit of theme `header.php` (if you want zero external dependency)

If the theme is editable and you can FTP in, paste this block just before the closing `</head>` tag in `header.php`:

```html
<script src="https://purepurposekh.github.io/tracy-harris-brand-kit/assets/js/thc-analytics.js"></script>
```

Same result as Option A, one fewer plugin on the stack.

## What this gives you automatically

Every page on tracyharris.co will auto-capture:

- `$pageview` — when a page loads
- `$pageleave` — with accurate time-on-page
- `$autocapture` — every click + form submit, tagged with the element info

## Recipe attribution

Pages built from a `/compose/` recipe carry `<body data-recipe-id="rcp_...">`. The analytics script reads that on load and registers `recipe_id` as a session super-property. Every subsequent event on that page is auto-tagged with the recipe_id — no extra work.

## Tracking specific CTAs

Add `data-track` attributes to your buttons/links and they track automatically:

```html
<!-- Apply for FFB button -->
<a href="/ffb/apply" data-track="apply" data-product="ffb">Apply for FFB</a>

<!-- Workshop registration -->
<a href="/workshop/register" data-track="workshop" data-product="million-dollar-message">Reserve my seat</a>

<!-- Any custom event -->
<a href="/something" data-track="custom" data-event="podcast_play">Listen now</a>
```

Or call the JS helpers directly from form handlers:

```html
<form id="optin-quiz" onsubmit="window.thc.trackAndIdentifyFromForm('optin-quiz', 'email')">
  <input name="email" type="email" required>
  <button type="submit">Get my result</button>
</form>
```

## Verify it's working

1. Load tracyharris.co in your browser
2. Open DevTools Network tab → filter for "posthog"
3. You should see `/decide/?...` and `/e/` requests firing
4. In PostHog dashboard: **Activity → Live Events** — your pageview should appear in real-time

## Masking form inputs (privacy)

The script already masks ALL form inputs in session recordings by default (`maskAllInputs: true`). So session replay won't leak email addresses, passwords, or any form data. If a specific element should be FULLY hidden in recordings, add:

```html
<div data-ph-no-capture>Sensitive content here</div>
```

## Later

- When we want to track the dashboard (`dashboard.tracyharris.com.au`) we'll run the PostHog Next.js wizard in that repo
- When we want to build a custom `/admin/recipes` view that pulls HogQL aggregates, we'll add it to that dashboard app
- Fathom keeps running in parallel for 2-4 weeks for sanity-checking numbers
