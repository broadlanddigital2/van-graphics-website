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
