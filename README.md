# Norwich Vehicle Graphics

## Hosting (same set-up as rcg-website)

| Piece | What it is |
| --- | --- |
| `dist/` | **The live website**, committed. Cloudflare serves it. |
| `build.py` + `*_content.py`, `*_pages.py`, `designer_page.py` | The Python generator that writes `dist/` (pages, sitemap, robots, llms.txt). |
| `worker/index.ts` | Tiny Worker in front of `dist/`: marks preview hosts (workers.dev) noindex. Add the live domain to `LIVE_HOSTS` at launch. |
| `wrangler.jsonc` | Worker `van-graphics-website`, serves `dist/`. |
| `.github/workflows/publish-from-crm.yml` | Hourly (and on demand / `crm-publish` dispatch): runs `build.py`, which reads the CRM feed, and commits `dist/` if anything changed. |

**Deploying:** Cloudflare **Workers Builds** is connected to this repo: every push to `main` deploys. Build command: *(none)*. Deploy command: `npx wrangler deploy`.

**Editing:** change the Python content files, run `python3 build.py`, commit and push.


Static marketing site. Run `python3 build.py` from the repository root to regenerate pages, sitemap and robots.txt in `dist/`. The shared core service template is in `core_pages.py` and the copy and route data are in `core_content.py`.

The private site uses Norwich Vehicle Graphics as a working name. The core enquiry form prepares an email draft and links to the existing Broadland Digital web enquiry form. Gallery and featured design imagery is illustrative.

## Van Designer

A free online design tool at `/design-your-van/`, with an advert block on the homepage (directly under the hero ribbon) and a "Design your van" link in the header and footer.

- `designer_page.py` – homepage promo block, page content and FAQs.
- `dist/assets/designer.js` – the tool (sign-up gate, van picker, graphics/wrap layouts, logo colour extraction, 360° WebGL viewer, lifestyle scenes, quote request). No external libraries.
- `dist/assets/designer.css` – styles, all scoped under `.nvg`.

**Lead capture.** Visitors sign up with name and email before designing; their session and designs are kept in their browser. Sign-ups and quote requests are posted to the CRM (see below). If the CRM can't be reached, quote requests open an email draft to the production inbox. `dataLayer` events are pushed for `designer_signup`, `designer_design` and `designer_quote` for GA4 / Google Ads.

Run `python3 build.py` after any change to `designer_page.py` or `build.py`. The two asset files are edited directly.

## CRM (managed site)

The site is managed in the Race Car Graphics CRM (Supabase project `dipjypzrfigkzuarlsov`) as its own business unit, **Norwich Vehicle Graphics** (slug `norwich-vehicle-graphics`).

| In the CRM | What it does |
| --- | --- |
| Business unit + "Incoming Leads" workflow | Incoming → Quoted → On Proof → Jobs → Completed |
| Channel "Norwich Vehicle Graphics Web Forms" (`enquiry_form`) | Receives the enquiry forms and Van Designer sign-ups/quotes; emails production@broadlanddigital.co.uk |
| SEO site "Norwich Vehicle Graphics" (static) | All 50 site pages imported for Search Console, audits and page fixes; brand profile for AI-written content |
| SEO feed | Pages written and published in the CRM are added to the site on the next `python3 build.py` |

Config lives in the `CRM` dict at the top of `build.py`. The build fetches the feed (15 s timeout) and keeps the last good copy in `crm_feed_cache.json`, so builds without internet keep working. If the build machine can reach the CRM, schedule `python3 build.py` (for example hourly, as Race Car Graphics does) and redeploy `dist/` so CRM-published pages go live automatically.

When the live domain is chosen, update `ORIGIN` in `build.py` and the business unit, channel and SEO site addresses in the CRM, then connect Search Console (`gsc_property`).

## Van Designer accounts

The designer at `/design-your-van/` sits behind a free, passwordless account.

- **Back end:** `supabase/functions/van-designer` (deployed to the shared CRM project), with tables `van_designer_sessions` and `van_designer_designs`.
- **Sign-up** creates (or matches) the CRM customer, a "Van Designer sign-up" lead with UTM/gclid, the marketing consent row when ticked, and logs the visitor straight in. A welcome email carries a one-time login link (48 hours) for other devices; "Email me a login link" on the gate sends a new one.
- **Designs** autosave to the account and appear under *My designs* (open, delete, start new). Activity (designs generated, 360°, lifestyle, logo upload, reg entered) is logged as lead events.
- **Quote request** creates a separate "Van Designer quote" lead carrying the sign-up's ad tracking, emails the team (`NVG_TEAM_EMAIL` secret, default production@broadlanddigital.co.uk) and confirms to the customer.
- **Reg lookup** uses the DVLA Vehicle Enquiry Service once a `DVLA_VES_API_KEY` secret is added; until then customers pick make and model.
- **Emails** send through the CRM's SendGrid account from the business unit's `outbound_from_email` (currently falls back to noreply@racecargraphics.uk). Login links use the business unit's `website_url`, so update it at launch.

## Launch checklist (search engines and AI assistants)

Until launch the site is only on the workers.dev preview, which tells every crawler to stay away (the Worker serves
`Disallow: /` and `X-Robots-Tag: noindex`). That's deliberate, so the preview never competes with the real site.
At launch:

1. **Domain**: attach it to the Worker in Cloudflare, add it to `routes` in `wrangler.jsonc` and to `LIVE_HOSTS` in
   `worker/index.ts`.
2. **Site address**: build with `SITE_ORIGIN=https://<domain> python3 build.py` (or change the fallback `ORIGIN` in
   `build.py`) so the sitemap, canonical links, `llms.txt` and structured data use the real domain. Commit `dist/`.
3. **Cloudflare AI settings** (zone → AI Crawl Control / Security → Bots): leave **Block AI bots** OFF and
   **Manage your robots.txt** OFF. Otherwise Cloudflare puts its own blocklist in front of `robots.txt` and returns
   403 to ChatGPT, Claude and Perplexity (this is what happened on lemancave.co.uk).
4. **CRM**: set the SEO site's domain (Marketing → SEO, `seo_sites.domain`) and the business's `website_url`; re-run
   the AI crawler check (Marketing → SEO tracking → AI answers) and confirm every crawler shows OK.
5. **Listings**: put the real domain on the Google Business Profile, then use "Sync with Google" in Bing Places.
6. **Search Console and Bing Webmaster Tools**: verify the domain and submit `/sitemap.xml`.
