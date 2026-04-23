# Brand Rules · Tracy Harris Co

Absolute rules every agent, team member, and contractor must follow. Non-negotiable.

Updated: 2026-04-21

---

## Source of Truth

1. **`tracy-harris-brand-kit/` is the design system source of truth.**
   - Tokens: `tokens/primitives.json` + `styles/tokens.css`
   - Fonts: `styles/fonts.css`
   - Components: `components/*/variants/`
2. **Production reference:** `tracy-harris-co/website/ffb-components.html`. When kit and production disagree, production wins, patch the kit.
3. **Archived (do NOT build against):** `tracy-harris-co/website/_archive/DESIGN*.md`, `tracy-harris-co/design/_archive/brand-system.md`, `opencore-vault/Clients/Tracy-Harris-Co/Brand.md` (legacy).

---

## Typography

4. **Serif display:** `Editors Note Regular` / `Editors Note Light Italic`. Loaded via Showit CDN in `fonts.css`. Use for H1 / H2 / hero display / pull quotes / section cards.
5. **Sans body:** `Poppins` (16px default). Use for all body copy, CTAs, navigation, labels. Never use a serif for long-form body.
6. **Script accent:** `Chic Societe Script` (Jhon Halend as fallback). Use ONLY for handwritten personal moments, tagline accents, signature phrases. Never body copy.
    - **Minimum size 40px.** Script fonts have low ink density per glyph. At anything under 40px, readability collapses. On desktop hero pages with display type above 60px, use `clamp(44px, 3.4vw, 56px)`. On section eyebrows above 28-32px h2s, use `clamp(32px, 2.4vw, 40px)`.
    - **Never pair with a sans-serif eyebrow in the same block.** Pick one. Stacking a sans-serif all-caps label under a script creates two eyebrows fighting for attention. If the sans label is load-bearing (it usually is, it communicates the offer), drop the script or move it elsewhere on the page.
    - **Weight + colour matter more than size.** The script at `var(--p-copper)` on `var(--p-oatmeal)` reads warmly at 44px. The same at `var(--p-mute)` disappears. Favour high-contrast colour placements.
    - **Use the `.tk-script-accent` class** (in `styles/tokens.css`) instead of inlining. The class enforces the minimum.
    - **When in doubt, skip it.** Script is an accent, not a requirement. If a page has 3+ hierarchy markers already, the script is noise.
7. **Label sans:** `Public Sans` (Poppins fallback). Use for eyebrows, small caps labels where Poppins reads too warm.

---

## Palette (primitives)

8. **Brand aztek:** `#1e3735` (brandmark colour).
9. **FFB dark:** `#243531` (canvas for FFB dark sections).
10. **Sage:** `#6e8e77` (kit accent).
11. **Sage alt:** `#788E75` (production FFB accent).
12. **Warm accents:** `coral #EF673E`, `copper #AD765B`, `dusty-rose #CC9989`.
13. **Cream:** `#ece7de`. **Oatmeal:** `#f6f4f1`.
14. **FFM gold:** `dark #7b623c`, `mid #c9a46c`.
15. **FRESH pillars:** `navy #20314c`, `orange #ca6b4d`, `yellow #ddab7d`, `peach #cc9989`.

---

## Voice Rules (applies to all copy, all channels)

16. **NEVER use em dashes (—).** Use commas, full stops, or rewrite. Hard rule.
17. **Freedom Filled® is a registered trademark.** Always include ® the first time it appears on a page, ideally every time.
18. **The Social Method® Society.** Full name with ®. Never "Social Method Society" or "Smart Marketing School".
19. **Never use "girlfriend".** Legacy Mums With Hustle vocab. Use "lovely" or nothing.
20. **Audience framing:** women building coaching, creative, or digital service businesses. Include **creatives** alongside coaches, experts, course creators. Not just "coaches and course creators".
21. **No Australian slang.** No "balmy", no "ripper", no "mate". Australian English spelling yes, slang no.
22. **No recycled scene openers.** "Sitting with a friend in Bali, drink in hand" pattern is BANNED. Every email gets a fresh entry beat, not a recycled scene.
23. **No corporate jargon.** No leverage, synergize, optimize your ROI, value proposition, stakeholders.
24. **No fake scarcity.** "Only 2 spots left" only if genuinely true.
25. **No AI slop.** Use real source HTML, real assets, real client stories. Placeholders labelled `[INSERT CLIENT STORY]` when you don't have real material, never invented.
26. **Tracy writes as "I".** Never "Tracy Harris believes". Always "I believe".

---

## Breathing Rhythm

27. **One sentence per line.** Tracy's most distinctive structural habit. If the draft looks like dense paragraphs, it's wrong.
28. **Bold for emphasis within flow.** ALL CAPS sparingly (1-3 times per piece max).
29. **Story first.** Lead with a relatable moment or client story. Never open with the offer.

---

## Products (canonical)

30. **Current products, ONLY:**
    - FFB (Freedom Filled® Business Mentorship) · $6K AUD
    - FFM (Freedom Filled® Mastermind) · $31K AUD
31. **Stale or discontinued, do NOT promote:**
    - SMS (The Social Method® Society) · being sunset, kept as FFM bonus
    - Inner Circle Mastermind · discontinued
    - Reels for Business Course · discontinued
    - Instagram Bio Checklist · discontinued
    - **Real estate business · does NOT exist.** Tracy never had one. If you see it in copy, strip it. Likely voice-transcription error for "Reels for Business".

---

## Handles + Naming

32. **Instagram:** `@tracyharrisco`. Never `@mumswithhustle` (old brand, do not reference).
33. **Podcast:** still "Mums With Hustle Podcast" until rebrand ships. Reference sparingly.
34. **Always refer to Tracy as "Tracy"** in company voice. Never "Tracy Harris" in third person when writing as the brand.

---

## Faith

35. **Christianity is the philosophical undercurrent, not the headline.** Show through language (steward, calling, gifts, purpose, by the grace of God), never declarations or preaching. More explicit in seasonal content (Christmas, Easter) and origin stories. Never weaponise faith for sales.

---

## Build Reports

36. **Always include a live preview URL** in every build report. A clickable URL, not just a repo link.
37. **Don't ask permission mid-build.** Default to placeholders + brand defaults, ship, iterate on Karl's reaction. Only ask for architectural or destructive decisions.

---

## Discord + Team Communication

38. **Discord tables:** use code blocks, not markdown tables. Markdown tables don't render in Discord.
39. **Discord replies:** always go through `mcp__plugin_discord_discord__reply`. Plain text output doesn't cross to Discord.
40. **Keep replies conversational.** Not doc-style. Lead with short answer. Don't mix code blocks + tables + nested bullets in one message.

---

## Legacy Files to Ignore

41. **Archived specs** (historical context only, never build against):
    - `tracy-harris-co/website/_archive/DESIGN.md` (v0)
    - `tracy-harris-co/website/_archive/DESIGN.v1.md`
    - `tracy-harris-co/website/_archive/DESIGN.v3.md`
    - `tracy-harris-co/website/_archive/DESIGN.v4.md` (Tony-Robbins-inspired, team moved on)
    - `tracy-harris-co/design/_archive/brand-system.md` (competing palette, superseded)

---

If a rule conflicts with something you see in a historical file, **this document wins**.
