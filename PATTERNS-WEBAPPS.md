# PATTERNS-WEBAPPS

Scope: Web and SaaS deployment plus UI patterns - Netlify deployment, React architecture, PayPal integration, SEO baseline, cache profile, legal modals, full-stack site recipes, visualization, layout components, TradingAgents-specific.

Patterns in this file: 14+ (some have multiple corrections/extensions)

Created: 2 May 2026 as part of memory architecture migration.

Canonical Drive doc: `1da7H-VBDQnX0_ldD6fF6nXjWYnJEhdZfFwKBQ72w6ro`

---

## Pattern 2: Netlify Deployment

Two modes - never confuse them:

### Manual deploy (drag-and-drop)
- `index.html` must be at ZIP/folder root
- `netlify.toml` publish directives are ignored
- Disconnects Git integration - must re-link afterward

### Git-connected deploy
- `netlify.toml` controls publish directory
- Correct structure: `netlify.toml`, `package.json`, `public/`, `netlify/functions/` all at repo root
- No wrapper subfolder containing all files

### Python build transform pipeline (legacy, RegMantle - SUPERSEDED, see Pattern 2 Correction below)
- Single React JSX file transformed for deployment
- ZIP packaging via Python script
- Deploy via Netlify CLI or drag-and-drop from transformed output

### Pattern 2 Correction (10 May 2026) - RegMantle Deployment Modernized

The original Pattern 2 entry for RegMantle described "Python build transform pipeline / single React JSX file transformed for deployment / ZIP packaging via Python script / Deploy via Netlify CLI or drag-and-drop from transformed output." This is **superseded** as of the 10 May 2026 session. Both RegMantle Netlify projects are now Git-connected and auto-deploy on push to main.

Current configuration (verified via Netlify project overview screenshots, 10 May 2026):
- **regmantle.com** - Netlify project name `regmantlelanding` - deploys from `Mikixxl/RegMantle` main. Static landing page, vanilla HTML/CSS/JS, no build step. `netlify.toml` controls publish dir + Pattern 23 cache headers.
- **reg.regmantle.com** - Netlify project name `regmantle` - deploys from `Mikixxl/regmantleapp` main. Single-file React app (`app.jsx` ~2500 lines, ~500 KB). No build step on Netlify side - the index.html loads `app.jsx` via Babel standalone in the browser. `netlify.toml` controls publish dir + Pattern 23 cache headers + SPA redirect.

Deploy flow now: edit locally, commit, push to main, Netlify auto-builds in ~30-60 seconds. No iPad-side action required from Michael. Build status visible in the project Deploys tab on Netlify.

Backup discipline (locked 10 May 2026): before any material change to either repo, create an annotated git tag `backup/<purpose>-<YYYY-MM-DD>` pointing at current HEAD and push it. Restore path is `git reset --hard <tag>` followed by force-push. The two repos are decoupled - tag and restore each independently.

Schema lock for the JURISDICTIONS array in `regmantleapp/app.jsx`: single-line entries, fields `code`, `name`, `region`, `regulator`, `amlLaw`, `guidance` plus optional `documentLanguage` (added Batch 2). Region values: Europe, MENA, Africa, Offshore, Asia. Do NOT use `regulatoryGuidance` or nested arrays - the system prompt builder reads only the flat fields above.

The Python ZIP-transform workflow described in the original Pattern 2 entry is deprecated for RegMantle. Do not revive it.

---

## Pattern 6: PayPal Smart Buttons Integration

Standard serverless architecture:
- `paypal-create.js`: Accept tier parameter, create PayPal order at correct price
- `paypal-capture.js`: Capture payment, issue JWT token with tier-appropriate expiry
- Frontend: JS SDK loaded dynamically from `www.paypal.com` (not sandbox)
- Callbacks: `createOrder` and `onApprove` to serverless functions
- Never include auto-certification fallback on payment failure

---

## Pattern 8: Single-File React App Architecture (IFB style)

Standard stack:
- Single file (e.g., `RegMantle.jsx` ~2400 lines)
- Supabase via lightweight REST fetch (not Supabase JS SDK)
- Anon key hardcoded in client (acceptable for public-facing data)
- PayPal Smart Buttons via dynamic SDK load
- sessionStorage for state persistence across navigation
- Netlify Functions for server-side operations (PayPal, email, DOCX export)

Session/auth pattern:
- Supabase anon key for public reads
- JWT tokens issued by serverless functions after payment
- Token stored in sessionStorage
- Component mount: query Supabase for user state, cache in sessionStorage

---

## Pattern 11: Three.js / Interactive Visualization Deployment

Deployment package:
- `index.html` (self-contained with all JS inline or CDN-loaded)
- `netlify.toml` (security headers)
- All files at ZIP root, no subfolder

CDN: Use `https://cdnjs.cloudflare.com` for Three.js and other libraries.

Three.js version: r128 on Cloudflare CDN. Avoid `CapsuleGeometry` (introduced r142).

OrbitControls: Not available on Cloudflare CDN for r128. Implement manually or skip.

---

## Pattern 16: Website SEO Launch Standards (STANDING RULE)

Every new website or webapp - regardless of entity, stack, or deployment method - must ship with the full SEO and PWA baseline below. This is not optional polish, it is the minimum viable launch. Apply on first deploy, not retroactively.

### Required files at deploy root
1. `robots.txt` - with explicit Sitemap reference line
2. `sitemap.xml` - minimum one entry (homepage), `lastmod` = deploy date, priority 1.0, changefreq appropriate to content type
3. `favicon.ico` - multi-size ICO (16/32/48) generated from the entity logo on the site's background color
4. `favicon-16.png` and `favicon-32.png` - for modern browsers
5. `apple-touch-icon.png` - 180x180 for iOS home screen
6. `icon-192.png` and `icon-512.png` - for PWA install and Android home screen
7. `site.webmanifest` - with `name`, `short_name`, `description`, `start_url`, `display=standalone`, `background_color`, `theme_color`, icons array (192 + 512 with `purpose="any maskable"`)

### Required head section tags in index.html
- charset, viewport, title, description (all present by default)
- `meta name="theme-color"` matching site background
- `meta name="robots" content="index, follow"`
- `link rel="canonical"` pointing to apex URL
- Full favicon link chain: ico + 16 + 32 + apple-touch + manifest
- Open Graph block: `og:type`, `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image` (512 or larger), `og:image:width`, `og:image:height`, `og:locale` (plus `og:locale:alternate` for each additional language)
- Twitter Card block: `twitter:card="summary_large_image"`, `twitter:title`, `twitter:description`, `twitter:image`
- JSON-LD schema (`application/ld+json`): `Organization` for corporate sites, `WebApplication` for tools, `FAQPage` if Q&A content exists. Include `name`, `url`, `logo`, `description`, `foundingDate`, `address` (if corporate), `contactPoint` with `availableLanguage` array

### Google Search Console setup
- Register as Domain property (not URL-prefix), verify via DNS TXT record
- For Netlify DNS domains: add TXT via Netlify API (token in KEYS-REPOSITORY)
- Domain property auto-covers www, non-www, http, https, all subdomains - no separate verifications needed
- After verification, submit `sitemap.xml` via GSC Sitemaps section

### Common pitfalls to avoid
- Never point favicon to a JPEG - browsers tolerate it but render poorly and PWA install breaks
- Never use URL-prefix GSC property on Netlify apex if `www → apex` redirects (301) - verification bot does not follow redirects
- Never deploy without `lastmod` updated to current date
- Never skip the manifest even for a single-page marketing site - installability is a mobile SEO signal

### Reference implementations
- `tera-ag.com` - corporate holding, Organization schema, 11 languages (implemented 21.04.2026)
- `timewemeet.com` - consumer tool, WebApplication + FAQPage schema, AdSense (updated 21.04.2026)
- `nuptelle.com` - SaaS product, full SEO baseline
- `regmantle.com` - compliance SaaS, full SEO baseline

### Implementation workflow
1. Fetch site's current state (via GitHub API if Git-linked, via Netlify deploy files API if direct-deploy)
2. Fetch the entity logo from repo or GROUP-LOGOS
3. Generate favicon set with PIL, auto-detect background color from logo corners
4. Build `robots.txt`, `sitemap.xml`, `site.webmanifest` with entity-specific values
5. Expand `index.html` head with canonical, OG, Twitter, JSON-LD, favicon chain
6. Deploy via Git push (auto-deploys) OR Netlify digest deploy API for non-Git sites
7. Verify all endpoints return 200 with expected content
8. Set GSC Domain property TXT record via Netlify DNS API
9. Submit sitemap in GSC after verification succeeds

Added: 21 April 2026 - after SEO rollout to `tera-ag.com` and `timewemeet.com` revealed that sites were being deployed without the full baseline. Pattern makes it non-optional going forward.

### Pattern 16 Correction (2026-04-23): GSC Verification

The original Pattern 16 default of "register as Domain property, verify by DNS TXT" is WRONG for Michael's account. Google binds a persistent HTML verification file to the Gmail account (`mikixxl1@gmail.com`). The same file works across every new site with zero per-site interaction.

The file: `googlefc0fefe84ee29fbd.html`
Content (53 bytes): `google-site-verification: googlefc0fefe84ee29fbd.html`
Canonical copy in Drive: file ID `1ANQrKIMN5xScJ-gUjJefKGTgDeC7FI6e`, parent folder `1lFmy4vdzWMkcBY2_hvGdyaaRxgQwubF2`

NEW WORKFLOW for every new site deploy:
1. Download `googlefc0fefe84ee29fbd.html` from Drive (file ID above) into the repo root. NOT inside `/assets` - Google checks the domain root.
2. Commit and push. Netlify auto-deploys.
3. Verify the file is reachable at `https://<domain>/googlefc0fefe84ee29fbd.html` and returns the 53-byte body.
4. Tell Michael: in GSC, add property → choose URL-prefix option → paste `https://<domain>` → select HTML file method → click Verify.

DNS TXT method on a Domain property remains the fallback for cases where URL-prefix is not desired (e.g., if Michael wants the property to cover every subdomain automatically), but URL-prefix + persistent file is the DEFAULT going forward.

Standard sitemap submission still applies: once verified, submit `/sitemap.xml` from inside GSC under the Sitemaps tab.

---

## Pattern 18 (webapps variant): Systematic QA-Sweep Methodology (STANDING TEMPLATE)

*Note: this is a webapps-specific variant. The canonical Pattern 18 is the Strategic Report DOCX Standard in `documents.md`.*

Effective bug-hunting on a mature webapp follows a categorical approach. Instead of clicking through each tab manually, scan for known anti-patterns at scale across the codebase. The categories that consistently produce real bugs:

1. **Render functions without try-catch wrap.** Single uncaught exception in render leaves the user with a blank tab and no recovery. Detect with: grep for `async function render` patterns then count `console.error` markers.
2. **`JSON.parse(event.body)` without try-catch in Netlify functions.** Malformed JSON returns 500 instead of 400, breaks API consumers.
3. **Hardcoded English UI strings inside render functions.** Massive i18n leak surface that monolingual users notice immediately.
4. **`innerHTML` concatenation with user-input fields without `escapeHTML` wrapping.** XSS risk where bad vendor name or guest note executes script.
5. **Async window handlers without disabled-button pattern.** Double-submit risk on slow networks.
6. **`console.log` calls left in production `index.html`.** PII leak risk if any log dumps wedding/user data.
7. **Admin endpoints without proper Supabase JWT validation** (shared-secret auth or no auth at all).
8. **Missing CORS headers on 4xx/5xx error responses** (browser-facing functions only - webhooks excluded).

The methodology: run each detection as a one-liner script, compile findings into a priority list (HIGH = security/PII, MED = resilience/i18n, LOW = UX polish), then file each as a separate Reminder. Don't try to fix all at once - the discipline is in the detection sweep, the fix sweep is a separate session per category.

---

## Pattern 20: Self-Contained E2E Test Runner (Zero-Dep Node.js)

For Netlify-deployed function E2E tests, prefer a self-contained Node script over npm-based test frameworks. The benefits: no `package.json` bloat, no `npm install` in CI, runnable from any sandbox or workstation with just Node 18+. The pattern:

- Single file in `tests/email-functions.test.js` (or similar).
- BASE_URL via env var defaults to production URL.
- Uses built-in `fetch` and `fs.writeFileSync`.
- Per-endpoint test routine: OPTIONS preflight, wrong-method 405, empty body, invalid JSON, missing required fields.
- Categorize endpoints: POST endpoints, GET endpoints, webhook endpoints. Each category gets its own test routine.
- Output: console summary AND markdown report at `tests/EMAIL_E2E_REPORT.md` so results diff across runs.
- Exit code 0/1 for CI pipelines.

The big benefit beyond catching new regressions is that the FIRST RUN of these tests catches existing latent bugs - the QA5 sweep of Nuptelle caught 3 bugs (vendor-inquiry, inbox-reply, rsvp-submit returning 500 instead of 400 on malformed JSON) immediately on first execution. The fix is mechanical (wrap `JSON.parse` in try-catch) so test infra and bug fixes go in the same commit. Re-run after fix deploys to confirm 100 percent pass rate.

Run command: `BASE_URL=https://example.com node tests/email-functions.test.js`. For local development, point BASE_URL at `netlify dev` localhost. The same script serves both purposes.

---

## Pattern 23: Netlify Boost Cache Profile (STANDING RULE)

Added 1 May 2026. Applies to every Netlify site, retroactively or going forward. Origin: IFBH GmbH and IFB-Holdings handover docs.

The goal: changes deploy fast and become visible to returning visitors quickly, without giving up the bandwidth savings of intermediary CDN caches. Cache invalidation is handled at the file-name level, not via Cache-Control alone.

### Required netlify.toml header block

```toml
[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=(), payment=()"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=3600, must-revalidate"
    X-Content-Type-Options = "nosniff"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=3600, must-revalidate"
    X-Content-Type-Options = "nosniff"

[[headers]]
  for = "/*.png"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/*.jpg"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/*.svg"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/*.ico"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/site.webmanifest"
  [headers.values]
    Cache-Control = "public, max-age=86400"
```

### Filename versioning is non-negotiable

CSS, JS, and config files carry an explicit version suffix in the filename: `styles-v3.css`, `script-v3.js`, `config-v3.js`. Query-string versioning (`styles.css?v=3`) is forbidden because it does not invalidate every CDN tier reliably and breaks on some service-worker setups.

Cache-bust mechanism: any CSS or JS edit MUST bump the filename suffix and update every HTML reference in the SAME commit. Never one without the other. Never edit `styles-v3.css` contents and leave the filename at v3. The version number monotonically increases per file.

### Reference implementations applying this exact spec
- `sad.ifcifb.com` (commit `590e21a`, 1 May 2026)
- `ifbh.org` (since 21 April 2026)
- `ifb-h.com` (since 27 April 2026)

### Common pitfalls
- Editing a file without bumping its version - returning visitors keep seeing old assets for up to 3600s.
- Bumping the filename without updating `index.html` references - 404s on the deployed site.
- Mixing query-string and filename versioning in the same site - causes cache divergence between visitor segments.
- Forgetting HSTS - browsers cache the HTTP-to-HTTPS preference long-term, so adding HSTS retroactively is fine but earlier is better.

Application to existing sites: if an active Netlify site does not yet have the Boost profile, audit and bring it onto spec on the next material change. Do not retrofit purely for retrofit's sake on production sites that are stable.

---

## Pattern 26 (webapps): Featured-Card Square-Cover Layout

*Note: webapps-specific. The strategic-side Pattern 26 (Fact-Check Living Persons) is in `strategic.md`.*

Added: 1 May 2026

When working with AI-generated covers (square 1024x1024 default for dall-e-3 / gpt-image-2), use 1:1 layout in featured cards instead of 16:10 horizontal hero crop.

### CSS pattern (locked in styles-v7+ on sad-platform)
- Card grid: `align-items: start` (NOT default stretch)
- Cover: `aspect-ratio: 1/1; align-self: start` (so it does not stretch to text-panel height)
- Cover img: `object-fit: cover; object-position: center center` (explicit)
- Right-edge gradient on cover `::after` for visual separation from text
- Body panel: explicit gradient background + `position: relative; z-index: 2` (prevents bleed)
- Desktop columns: `1fr 1fr` at 920px+ (equal split, was `1.1fr/1fr` which over-wide image)

### Why this matters

The previous 16:10 layout (styles-v4 and earlier) cropped 20% off every AI-generated square cover. The 1:1 layout uses the full image and reads as paired panels (text left / image right) rather than text-over-image. Generals demo on 1 May 2026 confirmed this layout reads as institutional-grade.

Brief-card layout: stays 16:10 (1792x1024 covers) - works for stock photos and wider compositions.

---

## Pattern 27 (webapps): Military-Insignia Category Badges

*Note: webapps-specific. The strategic-side Pattern 27 (Dual-Measurement Reframe) is in `strategic.md`.*

Added: 1 May 2026

For category/coverage cards on SAD-style platforms, use embossed gold-on-navy military insignia badges. Reads as institutional/heraldic to military audience.

### DALL-E 3 prompt template

> "Ornate military insignia badge, circular heraldic emblem with a thick gold metallic border ring and an inner dark navy blue field. Embossed three-dimensional gold metalwork with realistic depth, shadow, and metallic shine. Centered single emblematic motif: [TOPIC SYMBOL]. Style of formal NATO unit patches and US Army staff insignia. Photorealistic rendering of metal and enamel. Plain matte black background. No text, no letters, no numbers, no flags."

Generate at 1024x1024 `quality=hd`, then post-process:
1. Remove black background via PIL flood-fill from corners (scipy.ndimage.label)
2. Set alpha=0 on outer-dark connected components
3. Resize to 320x320 PNG (retina-ready for 120px display)
4. Upload to Supabase `site-assets/`

### Display in cards
- Card padding-top increased to accommodate badge (24px+)
- Badge img: `width:120px; height:120px; object-fit:contain`
- NO drop-shadow on transparent versions (creates ugly halo on edges)
- Hover: `transform: scale(1.05)`
- Layout: badge top-left, title + subtags bottom (`justify-content: space-between`)

---

## Pattern 28 (webapps): Impressum / Imprint Modal Pattern

*Note: webapps-specific. The strategic-side Pattern 28 (Wealth Preservation as Hardening-Axis) is in `strategic.md`.*

Added 22 April 2026. Applies to any multi-language IFB group webapp that needs §5 TMG (for German entities) or statutory corporate disclosure (for US entities).

### Legal baseline

For a German GmbH (§5 TMG): Firma, Sitz, Registergericht, HRB, USt-IdNr., W-IdNr., LEI, Geschäftsführer, Aufsichtsratsvorsitzender (if applicable), Verantwortlich für den Inhalt (§18 Abs. 2 MStV), Email, Telefon. Footer link "Impressum" must be reachable from every page.

For a US LLC: Legal name, Legal form, Principal office, State of formation, Document number, EIN, LEI (if applicable), Responsible for content, Email. Footer link "Legal Notice" required.

### 14-language label keys (reusable)

Authored 22 April 2026 as Claude Opus 4.7 in formal legal register. Keys: `legal_nav`, `imprint_heading`, `imprint_intro_gmbh`, `imprint_intro_llc`, `imprint_company`, `imprint_form`, `imprint_address`, `imprint_state`, `imprint_docnum`, `imprint_court`, `imprint_hrb`, `imprint_vat`, `imprint_widnr`, `imprint_lei`, `imprint_ein`, `imprint_md`, `imprint_chairman`, `imprint_responsible`, `imprint_email`, `imprint_phone`.

Sample renderings (footer link / section heading):
- `en` Legal Notice
- `de` Impressum
- `fr` Mentions légales
- `es` Aviso legal
- `it` Note legali
- `pt` Aviso legal
- `ru` Правовая информация
- `zh` 法律声明
- `zh-Hant` 法律聲明
- `ja` 法的情報
- `ko` 법적 고지
- `hi` कानूनी सूचना
- `ar` الإشعار القانوني
- `he` מידע משפטי

### Deployment workflow (atomic Git Data API)

Six `proxy_execute` calls per repo:
1. `GET /repos/{repo}/git/ref/heads/main` - capture parent SHA
2. `GET /repos/{repo}/git/commits/{parent_sha}` - capture base tree SHA
3. `POST /repos/{repo}/git/blobs` (once per file) - base64 content + encoding
4. `POST /repos/{repo}/git/trees` - base_tree + tree items with blob SHAs
5. `POST /repos/{repo}/git/commits` - message + tree SHA + parents
6. `PATCH /repos/{repo}/git/refs/heads/main` - sha + force=false

Result: single commit containing all modified files, clean history, no force-push risk.

### Modal variant (22 April 2026)

Superseded the original inline section approach. An imprint as a visible section was too long on mobile once sitting above all other site sections. Switch to footer links that open glass-morphic modals.

Footer pattern: Three button elements, not anchors, with `data-open-modal` attributes pointing to `imprint`, `privacy`, `cookies`. Translated per language via new i18n keys `legal_imprint`, `legal_privacy`, `legal_cookies`. Keys authored in 14 languages, formal legal register.

Modal structure: Each modal contains DE and EN bodies (hidden by class). JavaScript in `applyTranslations()` flips which body has the `is-visible` class based on current lang (`bodyLang = lang === 'de' ? 'de' : 'en'`). For the 12 non-DE languages, EN fallback applies - acceptable because legal texts do not need 14 versions for a static info site.

Modal UX: Backdrop click closes, Escape key closes, body scroll locks while open, panel focus goes to close button on open for keyboard accessibility. Glass-morphic: `rgba(255,255,255,0.97)` + `backdrop-filter blur(14px)`, rise+fade animation on open.

Content (GmbH example):
- Impressum: 12 statutory rows per §5 TMG
- Datenschutzerklärung: 10 sections covering data controller, technical processing, no cookies, hosting provider (Netlify Inc., 44 Montgomery St Suite 300, San Francisco CA 94104), recipients, retention, GDPR rights, update clause
- Cookies: 4 paragraphs confirming zero cookie use, no consent required under §25 TDDDG

### AG (Aktiengesellschaft) refinement (Nurdug build, 22 April 2026)

For AG entities, the Impressum modal requires different statutory labels than GmbH:
- Use `Vorstand` instead of `Geschäftsführer`. If Aufsichtsrat exists in the entity, add `Aufsichtsratsvorsitzender`; otherwise omit the field rather than leaving it blank.
- Add a `Rechtsform` row at the top explicitly stating "Aktiengesellschaft nach deutschem Recht"
- Include Fax if the entity still uses one (Nurdug does: `+49 30 50508719`)
- DUNS number and EBID belong in Impressum even though §5 TMG doesn't require them. They signal completeness and help DDGS/trade partners verify.

Reference commit: `Mikixxl/nurdug` commit `aefa7e27` (22 April 2026).

For real estate holdings specifically: use `RealEstateAgent` JSON-LD schema, not `FinancialService`. Pull `knowsLanguage` from the switcher's active language set.

---

## Pattern 29: IFB Group Website Build Recipe

Established 22 April 2026 after successful Nurdug AG build (`Mikixxl/nurdug`). This recipe consolidates Patterns 16 (SEO+PWA), 18 (Legal Modals), and the translation authoring methodology into a single repeatable sequence. Following these steps in order produces a multi-language IFB-group website with German legal compliance, full SEO, and glassmorphism aesthetic in roughly 90 minutes of build time.

### When to use

Any new corporate website for an IFB-group entity, or similar static informational sites with 10+ languages, German legal requirements, and glassmorphism brand aesthetic. Do NOT use for webapps with backends - this recipe is for static single-page sites.

### Prerequisites
1. Entity registration data ready: legal form (GmbH/AG/LLC), HRB number, tax IDs, officers (Vorstand for AG, Geschäftsführer for GmbH, Managing Member for LLC)
2. Hero image (landscape, at least 1200px wide)
3. Logo (square, at least 512x512, ideally transparent PNG)
4. Brand content in source language (usually DE)
5. GitHub PAT: in 08-Keys / KEYS-REPOSITORY (standing default for `Mikixxl/*` repos)
6. Reference commit: `Mikixxl/IFBH de1e7b79` (or whichever commit reflects the current Pattern 18 modal variant)

### Step 1: Image processing (bash sandbox, 3 min)

Images live in `/mnt/user-data/uploads` which only bash can reach. Use PIL with content-bounds detection to split combined logos (swirl + text) into swirl-only variants for favicons.

Generate exactly 10 assets per site: `hero.jpg` (1920x1080), `hero-mobile.jpg` (960x540), `og-image.jpg` (1200x630), `logo.png` (512x512 with text), `apple-touch-icon.png` (180x180 on white bg), `favicon-16.png`, `favicon-32.png`, `favicon.ico` (multi-size), `icon-192.png`, `icon-512.png`. All written to `/home/claude/out/`.

Key PIL technique: detect text boundary in combined logo by finding a horizontal row with < 10 non-white pixels, use that y-coordinate to split swirl (for favicons) from full mark (for main logo). This produces clean square favicons even from non-square source logos.

### Step 2: Fetch IFBH template (workbench, 1 min)

Clone the reference state from `Mikixxl/IFBH` main. Eight text files needed: `index.html`, `script-v6.js`, `styles-v3.css`, `netlify.toml`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `README.md`. Save to `/tmp/ifbh-ref/`.

The IFBH commit `de1e7b79` already carries Pattern 18 (modal legal system) inline - no need to re-author modal CSS/JS.

### Step 3: Author translations directly (workbench, 20 min)

CRITICAL: Do NOT use workbench `invoke_llm` for translations. It routes to Groq Compound which degrades quality below Claude Opus. Author each language block as a Python dict literal directly.

Content structure: 54 keys per language covering meta, nav, hero, firm, focus, approach (with 5 principle cards), distinction, self, closing, contact, footer, and 3 legal labels. Write DE first from source document, then EN as source of truth for all non-DE translations, then the 12 remaining languages.

Save as `/tmp/site_i18n.json`. Verify all 14 languages have identical key sets before proceeding.

Authoring register: formal business, elevated, Douglas Murray-influenced. Preserve the source text's positioning (for Nurdug: "Substanz statt Spekulation", "La substance plutôt que la spéculation", "The substance over speculation", etc.). Avoid LLM filler vocabulary (delve/leverage/robust etc.).

### Step 4: Build CSS (workbench, 5 min)

Clone IFBH `styles-v3.css` verbatim. Replace only the `:root` custom properties block with the new entity's palette. Keep all structural rules (layout, glassmorphism, responsive media queries) unchanged.

Palette selection from logo: sample 3-5 dominant colors, pick deepest navy for `--bg-deep` (slightly warmer than IFBH's `#06091c` if the brand is warmer), mid-brand blue for `--blue`, accent color (copper for Nurdug vs gold for IFBH) for `--gold` and `--gold-deep` variables (names kept for compatibility). Update leading comment.

### Step 5: Compose index.html (workbench, 10 min)

Build fresh, do not try to string-manipulate the IFBH index. Structure:
- `<head>` with full Pattern 16 SEO+PWA baseline (canonical, OG, Twitter, JSON-LD, favicon chain, fonts, CSS link)
- Inline `<script>` for i18n + modal handlers
- Body sections per the entity's content

### Pattern 19 Correction (22 April 2026): GSC verification file

Missed in the initial Nurdug build, added in commit `fe3d6637`. Future sites must include this from Commit 1.

Michael uses one standard Google Search Console verification file across all IFB-group sites:
- Filename: `googlefc0fefe84ee29fbd.html`
- Content: `google-site-verification: googlefc0fefe84ee29fbd.html`
- Location: repository root (served at `/googlefc0fefe84ee29fbd.html`)

The same file is committed to `Mikixxl/IFBH`, `Mikixxl/ifb-holdings`, and `Mikixxl/nurdug`. Any new IFB-group site must carry it too. When Michael adds the new domain as a GSC property, the verification passes via file-upload method automatically.

Add this to Step 7 (Configure) of Pattern 19. Text files checklist for every new site:
1. `netlify.toml`
2. `robots.txt`
3. `sitemap.xml`
4. `site.webmanifest`
5. `README.md`
6. `googlefc0fefe84ee29fbd.html` (GSC verification, always the same content)

If a future IFB-group rotation requires a new GSC token, update this pattern with the new filename + content pair.

---

## Pattern 31 (webapps): TradingAgents Model Whitelist Silent Hang

*Note: webapps-specific. The infra-side Pattern 31 (Rube to Composio Migration) is in `infra.md`.*

Problem it solves: TradingAgents backend run starts, prints initial logs, then goes completely silent. No error, no timeout, no progress. Looks like a tool/network hang but is actually a model-name validation failure that's incorrectly classified as a warning.

Trigger condition: `DEEP_THINK_MODEL` or `QUICK_THINK_MODEL` env var set to a Claude model not in `tradingagents/llm_clients/model_catalog.py` whitelist. Example: setting `claude-opus-4-7` when the catalog only knows up to `claude-opus-4-6`.

Symptom signature:
- Backend logs show: `RuntimeWarning: Model 'X' is not in the known model list for provider 'anthropic'. Continuing anyway.`
- After this line: ZERO further log output from the analysis run
- Only Fly health-check GETs continue showing in logs
- Run hangs indefinitely (>15 minutes), no error, no completion
- The "Continuing anyway" message is misleading - the actual API call retries forever inside `langchain-anthropic`

Solution:
- Pin model env vars to entries in `model_catalog.py` whitelist
- Current safe whitelist (3 May 2026): `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-opus-4-5`, `claude-sonnet-4-5`, `claude-haiku-4-5`
- To use a newer Claude model: BOTH (1) extend `model_catalog.py` allowlist AND (2) upgrade `langchain-anthropic` in `requirements.txt`
- Set fly.toml: `DEEP_THINK_MODEL = 'claude-opus-4-6'` / `QUICK_THINK_MODEL = 'claude-sonnet-4-6'` as proven baseline

Detection sweep: grep "is not in the known model list" in Fly logs immediately after any deploy that changes model env vars.

First seen: 3 May 2026 during TradingAgents NVDA + AAPL test runs. Set `DEEP_THINK_MODEL=claude-opus-4-7` (the model running this Claude session at the time), runs hung 13+ minutes silently. Fixed in commit `ade2606` by reverting to `claude-opus-4-6`.

---

## Pattern 32: LangGraph Parallel Agents Break Anthropic tool_use Invariant

Problem it solves: Naive attempt to parallelize multiple LangGraph agents via fan-out/fan-in fails with cryptic Anthropic API error after a few seconds, even though each agent writes to a different state field.

Trigger condition: Multiple agents running in parallel that all (a) inherit from `MessagesState` (or equivalent shared messages array) AND (b) make tool calls. Anthropic API requires every `tool_use` block in the messages array to be IMMEDIATELY followed by its corresponding `tool_result` block. When agents run in parallel and append messages concurrently, their tool_use/tool_result pairs interleave and break the invariant.

Symptom signature:
- Run fails 30 seconds to 2 minutes after start (much faster than a normal hang)
- Error in Supabase `analyses.error`: `BadRequestError: Error code: 400 - tool_use ids were found without tool_result blocks immediately after: toolu_X, toolu_Y, toolu_Z, toolu_W`
- Error usually attributed to one specific agent ("During task with name 'News Analyst'") but the cause is contamination from OTHER agents' interleaved tool_use blocks

Solution options (ordered by complexity):
- **(Easy)** Revert to sequential analyst chain. Accept ~12-min runs. Done in commit `bffdeaa`.
- **(Medium)** Use LangGraph `Send` API to spawn each agent as an independent worker with isolated `MessagesState` substate. Parent graph merges only the report fields back. ~150-200 line refactor in `graph/setup.py` plus analyst function adjustments to use private message lists.
- **(Hard)** Replace shared `MessagesState` with custom reducer that segregates messages by `agent_name` and only flattens for downstream synthesis nodes.

Speed alternatives that DO work without parallelization:
- **Anthropic Prompt Caching** (`cache_control` on system prompts in `langchain-anthropic ChatAnthropic` config) - 50-70% latency cut on repeat agent loops, ZERO quality impact
- Reduce `MAX_DEBATE_ROUNDS` env var (1 instead of 2)
- Drop one of the 3 risk debators (Aggressive/Conservative/Neutral) - one is enough

First seen: 3 May 2026 commit `a538b26` attempted naive fan-out parallelization of 4 analysts in TradingAgents. TSLA test run failed in 2:25 with "tool_use ids without tool_result" error. Reverted in commit `bffdeaa`. Send-API rewrite deferred as separate roadmap item.

---

## Pattern 33 (webapps): CORS DELETE Preflight Requires Explicit allow_methods

*Note: webapps-specific. The infra-side Pattern 33 (GitHub-Relay for Binary Drive Upload) is in `infra.md`.*

Problem it solves: Browser DELETE call to FastAPI backend fails with "Load failed" / "Failed to fetch" - looks like the backend is down or unreachable, but the backend is fine and never even sees the request.

Trigger condition: FastAPI `CORSMiddleware` configured with `allow_methods=["GET", "POST"]` (the typical default copy-pasted from tutorials). Any browser-issued DELETE, PUT, or PATCH triggers a CORS preflight (OPTIONS) request that the middleware rejects, so the actual DELETE never reaches the route handler.

Symptom signature:
- Browser console: `Failed to fetch` or `Load failed` or `TypeError: Failed to fetch`
- Frontend status pill shows backend ONLINE (because GET /health works)
- Backend Fly logs show NO entry for the DELETE attempt at all (the request is killed in the browser before it even leaves)
- Only OPTIONS request might appear and immediately get rejected with no `Access-Control-Allow-Methods` header for DELETE

Solution:
- FastAPI `CORSMiddleware`: explicitly list every method the frontend uses
- Minimum for a CRUD-capable browser frontend: `allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"]`
- OR use `allow_methods=["*"]` (acceptable for trusted same-tenant frontend, NOT for public APIs)
- Do NOT forget OPTIONS - browsers send it as preflight for any non-simple request

Cross-check during deploy:
- Test the new HTTP method from the browser console with `fetch()` before assuming the backend code is wrong
- If "Load failed" within milliseconds (no network round-trip latency), it's almost always CORS, not backend

First seen: 3 May 2026 during TradingAgents trash-button feature. Added `DELETE /analyses/{id}` backend endpoint (commit `fe105f3`) but `allow_methods` was still `["GET", "POST"]`. Browser blocked the call entirely. Fixed in commit `09610ca` by adding `DELETE + OPTIONS` to `allow_methods`.

---

## Pattern 34: Single-Repo Multi-Site Netlify Monorepo (Mikixxl/IFBYCB convention)

Added 11 May 2026. Discovered during the Claude Code OS dashboard deploy session.

The repo `Mikixxl/IFBYCB` hosts 11+ small Netlify sites in a single GitHub repo. Each site has its OWN dedicated long-lived branch named `claude/<descriptive>-<suffix>`, deployed as that site's production branch. Examples (as of 11 May 2026):

| Site | Domain | Branch |
|---|---|---|
| bondcalc | bondcalc.ifcifb.com | claude/bond-calculator-webapp-NurmW |
| sternwarte | sternwarte.ifcifb.com | claude/planetary-positions-webapp-5RNrs |
| gpi-tracker | gpi.ifcifb.com | claude/swift-transfer-tracker-Nq9K5 |
| bondsifb | bondyields.ifcifb.com | claude/dynamic-bonds-market-site-XZ4Ta |
| meetingscript | meetscript.ifcifb.com | claude/meeting-recorder-app-ny5CX |
| unidades1 | units.ifcifb.com | claude/unit-converter-app-EHhCt |
| photocon | photoconv.ifcifb.com | claude/photo-format-converter-V4VYv |
| pepupload | pepupload.ifcifb.com | claude/client-upload-portal-ne3qQ |
| ifbupload | upload.ifcifb.com | claude/client-upload-portal-ne3qQ |
| ifcteams | ifcteams.ifcifb.com | claude/project-management-webapp-eW1yw |
| claudeos | claudeos.ifcifb.com | claude/build-claude-os-dashboard-fV05f |

Per-branch isolation is enforced via the `build_settings.allowed_branches` array on each Netlify site, set to exactly that one branch. Webhook deploys on any other branch are ignored.

**CRITICAL CONSEQUENCE: `main` is NOT a production branch for anything in this repo.** Merging a PR into `main` does NOT deploy any site, and `main` drifts out-of-sync with every site. Treat `main` as a template/reset branch only. Do not PR feature work back into it.

### Adding a new site to this repo (procedure verified 11 May 2026)

1. Pick a feature branch name `claude/<feature>-<suffix>`. Push initial content. publish=`.`, no build step.
2. Fetch an existing site via Netlify API to copy `build_settings` verbatim (bondcalc is a clean reference, site_id `aa3f9b66-c06a-4352-bc43-95d9fe4ebcce`). Fields to mirror:
   ```
   provider: github
   repo_path: Mikixxl/IFBYCB
   installation_id: 56164198            (the existing Netlify-GitHub App install)
   repo_branch: <new branch>
   allowed_branches: [<new branch>]     ← non-negotiable, this is what isolates the sites
   dir: "."
   cmd: "echo 'no build step'"
   ```
3. POST `https://api.netlify.com/api/v1/<account_slug>/sites` with name, custom_domain, processing_settings, and the repo block above. account_slug for this account: `mikixxl`. account_id: `6713fa5c840ac7fb17a7678b`.
4. Trigger initial build with `POST /api/v1/sites/<id>/builds`. The webhook sometimes fires automatically on link, sometimes not - safer to trigger explicitly.
5. Custom domain DNS resolves automatically because `*.ifcifb.com` is on Netlify DNS.

### Two specific gotchas that bit during the first claudeos deploy

**A) `main` has a malformed netlify.toml.** The boost cache profile (Pattern 23) was concatenated onto the redirect block with no separating newline, producing `status = 200[build]` on one line. Every branch that inherited from `main` carries this typo; first deploy of any new site fails at the parsing stage with: "Unexpected character, expected only whitespace or comments till end of line at row 7, col 15". Fix before deploying: ensure `status = 200` ends the redirect block on its own line, followed by a blank line before the next `[[headers]]` table.

**B) If `netlify.toml` contains `functions = "netlify/functions"`, Netlify auto-bundles every `.js` file in that directory.** The legacy `market.js` requires `node-fetch` and `cheerio` but the local `package.json` is empty (1 byte) - the bundle resolution fails with exit code 2 at the "building site" stage. The error message does not mention deps; it just says "Build script returned non-zero exit code: 2", which is misleading because the `build_settings.cmd` is the no-op echo. For branches that do NOT use those functions, drop the `functions` config from `netlify.toml` AND delete the `netlify/functions` directory on that branch. Per-branch isolation makes this safe; other sites that use the functions on their own branches are unaffected.

### API egress note

`api.netlify.com` is NOT in the Anthropic sandbox outbound allowlist. Call it from the Rube workbench (`RUBE_REMOTE_BASH_TOOL`) which has broader egress. Direct curl from a Claude Code sandbox session will fail silently or with DNS errors. **Note: Rube EOL 15 May 2026.** Post-EOL, the Netlify API must be reached via a GitHub Actions workflow or other CI runner with unrestricted egress, OR via the GitHub-relay pattern (`infra.md` Pattern 33).

### Operational discipline reminder

When a found-credential token is used for the first time in a session:
1. Verify scope and revocation date before any write call.
2. Read-only calls first (`GET /sites`, `GET /sites/<id>`) - confirms the token works AND surfaces the existing landscape so the write call doesn't create duplicates or clobber a sibling.
3. Confirm with user before the first POST/PATCH/DELETE.
4. Never write the token to any commit, function env, or CLAUDE.md - reference its location in 2nd Brain instead.

### Reference commit chain (claudeos, 11 May 2026)
- `a27aab1` feat: replace yield-curve frontend with Claude Code OS dashboard
- `9ae8d12` fix: repair malformed netlify.toml so build can parse it
- `886f078` chore: drop unused yield-curve netlify functions on this branch

The third commit took the deploy from error → ready in about 30s.

Final URL: https://claudeos.ifcifb.com
Admin: https://app.netlify.com/projects/claudeos
