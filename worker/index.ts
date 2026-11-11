// Serves the static site from dist/. The only server-side job is search-engine control:
// preview hosts (workers.dev) are marked noindex; the live domain(s) in LIVE_HOSTS are indexable.
const LIVE_HOSTS: string[] = []; // e.g. ["norwichvehiclegraphics.co.uk"] once the domain is live

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
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    let response = await env.ASSETS.fetch(request);
    if (response.status === 404) {
      // Old addresses (before the keyword URLs) redirect permanently to their new pages.
      const map = await redirects(env, url);
      const path = url.pathname.endsWith("/") ? url.pathname : url.pathname + "/";
      if (map[path]) return Response.redirect(new URL(map[path] + url.search + url.hash, url.origin).toString(), 301);
    }
    if (LIVE_HOSTS.includes(url.hostname)) return response;
    const out = new Response(response.body, response);
    out.headers.set("X-Robots-Tag", "noindex, nofollow");
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain; charset=utf-8", "X-Robots-Tag": "noindex" } });
    }
    return out;
  },
};
