// Serves the static site from dist/. Server-side jobs: search-engine control (preview hosts (workers.dev) are marked
// noindex; the live domain(s) in LIVE_HOSTS are indexable), and AI visibility stats for the CRM on the live domain
// (ai-visibility.js: AI crawler visits and people sent by ChatGPT, Claude, Perplexity… → Marketing → SEO tracking →
// AI assistants).
import { trackAi } from "./ai-visibility.js";
const LIVE_HOSTS: string[] = ["getitwrapt.co.uk"];
const CANONICAL_HOST = "getitwrapt.co.uk";
// The CRM SEO site's feed key (seo_sites.feed_key; the same key as the seo-feed in build.py).
const SEO_FEED_KEY = "21aed0c2-5381-44a9-8e6b-42f99b684c59";
type Ctx = { waitUntil(p: Promise<unknown>): void };

type Env = { ASSETS: { fetch: typeof fetch } };

let REDIRECTS: Record<string, string> | null = null;
async function redirects(env: Env, url: URL): Promise<Record<string, string>> {
  if (REDIRECTS) return REDIRECTS;
  try {
    const r = await env.ASSETS.fetch(new Request(new URL("/redirects.json", url.origin).toString()));
    REDIRECTS = r.ok ? await r.json() : {};
  } catch { REDIRECTS = {}; }
  return REDIRECTS!;
}

export default {
  async fetch(request: Request, env: Env, ctx: Ctx): Promise<Response> {
    const url = new URL(request.url);
    if (url.hostname === "www." + CANONICAL_HOST) {
      url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }
    let response = await env.ASSETS.fetch(request);
    if (response.status === 404) {
      // Old addresses (before the keyword URLs) redirect permanently to their new pages.
      const map = await redirects(env, url);
      const path = url.pathname.endsWith("/") ? url.pathname : url.pathname + "/";
      const to = map[url.pathname] || map[path];
      if (to) return Response.redirect(new URL(to + url.search + url.hash, url.origin).toString(), 301);
    }
    if (LIVE_HOSTS.includes(url.hostname)) {
      // Pages only (not images, styles or scripts under /assets/).
      if (!url.pathname.startsWith("/assets/")) trackAi(request, response, ctx, { feedKey: SEO_FEED_KEY });
      return response;
    }
    const out = new Response(response.body, response);
    out.headers.set("X-Robots-Tag", "noindex, nofollow");
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain; charset=utf-8", "X-Robots-Tag": "noindex" } });
    }
    return out;
  },
};
