// Serves the static site from dist/. The only server-side job is search-engine control:
// preview hosts (workers.dev) are marked noindex; the live domain(s) in LIVE_HOSTS are indexable.
const LIVE_HOSTS: string[] = []; // e.g. ["norwichvehiclegraphics.co.uk"] once the domain is live

type Env = { ASSETS: { fetch: typeof fetch } };

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const response = await env.ASSETS.fetch(request);
    if (LIVE_HOSTS.includes(url.hostname)) return response;
    const out = new Response(response.body, response);
    out.headers.set("X-Robots-Tag", "noindex, nofollow");
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain; charset=utf-8", "X-Robots-Tag": "noindex" } });
    }
    return out;
  },
};
