// Van Designer photo-real renders (OpenAI image API, CRM secret OPENAI_API_KEY).
// generate: { token, design_id, scene, image }  image = PNG data URL of the customer's van design on a
//           transparent background. Returns a photo-real scene as base64; the browser adds the watermark.
// save:     { token, design_id, scene, image }  image = final JPEG data URL; stored in the public
//           van-designer-renders bucket and listed on the design (renders) and the lead (lead event).
// status:   { token } -> { available, remaining }
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.57.4";

const DAILY_LIMIT = Number(Deno.env.get("NVG_RENDERS_PER_DAY") || 5);
const IMAGE_MODELS = ["gpt-image-2", "gpt-image-1.5", "gpt-image-1"];
const BUCKET = "van-designer-renders";
const SCENES: Record<string, string> = {
  motorway: "driving on a UK dual carriageway in daylight, gentle motion blur on the road and background, other traffic far behind",
  city: "parked on a historic English city street with independent shopfronts and brick buildings, late afternoon light",
  site: "parked on a residential building site beside a new brick house with scaffolding, ladders and materials nearby",
  driveway: "parked on a block-paved driveway outside a red-brick and flint East Anglian house, warm evening light",
  country: "on a quiet Norfolk country lane between hedgerows and open fields under a big sky",
  coast: "parked in a seafront car park with the sea, sand dunes and a wide sky behind",
  night: "parked on a wet city street at night, street lights and reflections on the road, headlights on",
  studio: "on a clean light grey studio floor with soft even lighting and a seamless backdrop",
};

const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "content-type", "Access-Control-Allow-Methods": "POST,OPTIONS" };
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...CORS, "Content-Type": "application/json" } });
const raw = Deno.env.get("SUPABASE_SECRET_KEYS");
const db = createClient(Deno.env.get("SUPABASE_URL")!, raw ? JSON.parse(raw).default : Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false, autoRefreshToken: false } });

async function sha256(v: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(v));
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function session(token: unknown) {
  const t = String(token || "").slice(0, 200);
  if (!t) return null;
  const { data } = await db.from("van_designer_sessions").select("customer_id,lead_id,expires_at,revoked_at").eq("token_hash", await sha256(t)).eq("kind", "session").maybeSingle();
  if (!data || data.revoked_at || new Date(data.expires_at) < new Date()) return null;
  return data;
}
function dataUrlBytes(u: unknown, max: number) {
  const m = /^data:(image\/(png|jpeg|webp));base64,([A-Za-z0-9+/=]+)$/.exec(String(u || ""));
  if (!m) return null;
  const bin = atob(m[3]);
  if (bin.length > max) return null;
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return { type: m[1], bytes };
}
async function usedToday(leadId: string | null) {
  if (!leadId) return 0;
  const { count } = await db.from("lead_events").select("id", { count: "exact", head: true })
    .eq("lead_id", leadId).eq("event_type", "designer_render_generated").gte("created_at", new Date(Date.now() - 864e5).toISOString());
  return count || 0;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST required" }, 405);
  let body: any;
  try { body = await req.json(); } catch { return json({ error: "Invalid JSON" }, 400); }
  try {
    const s = await session(body.token);
    if (!s) return json({ error: "Signed out" }, 401);
    const key = Deno.env.get("OPENAI_API_KEY");
    if (body.action === "status") {
      return json({ ok: true, available: !!key, remaining: Math.max(0, DAILY_LIMIT - await usedToday(s.lead_id)), scenes: Object.keys(SCENES) });
    }
    const { data: design } = await db.from("van_designer_designs").select("id,vehicle,state,renders").eq("id", String(body.design_id || "")).eq("customer_id", s.customer_id).maybeSingle();
    if (!design) return json({ error: "Save your design first." }, 404);
    const scene = SCENES[body.scene] ? body.scene : "motorway";

    if (body.action === "generate") {
      if (!key) return json({ error: "Photo-real renders aren't switched on yet." }, 503);
      const used = await usedToday(s.lead_id);
      if (used >= DAILY_LIMIT) return json({ error: `You've used today's ${DAILY_LIMIT} renders. Try again tomorrow, or request a quote and we'll render it for you.`, remaining: 0 }, 429);
      const img = dataUrlBytes(body.image, 6 * 1024 * 1024);
      if (!img || img.type !== "image/png") return json({ error: "Invalid design image" }, 400);
      const v = design.vehicle || {};
      const st = design.state || {};
      const wording = [st.company, st.tagline, st.phone, st.web].filter(Boolean).map((x: string) => `"${String(x).slice(0, 80)}"`).join(", ");
      const prompt = [
        `Photorealistic commercial photograph of a ${v.colour || "white"} ${v.make || ""} ${v.model || "panel van"} ${v.lwb ? "long wheelbase" : ""} panel van, right-hand drive UK registration, ${SCENES[scene]}.`,
        `The van must carry exactly the vinyl ${st.mode === "wrap" ? "printed wrap" : "graphics"} shown in the reference image: the same layout, colours, shapes, logo and lettering in the same positions.`,
        wording ? `The lettering on the van reads exactly: ${wording}. Spell every word and number exactly as written.` : "",
        "Show the van side-on, slightly angled towards the camera, filling about two thirds of the frame, sharp and in focus, with realistic reflections, shadows and panel gaps.",
        "Blank number plate. No other text, no watermark, no people in the foreground, no real company logos.",
      ].filter(Boolean).join(" ");
      let b64 = "", last = "Render failed";
      for (const model of IMAGE_MODELS) {
        const fd = new FormData();
        fd.append("model", model); fd.append("prompt", prompt); fd.append("size", "1536x1024"); fd.append("n", "1");
        fd.append("quality", "high"); fd.append("input_fidelity", "high");
        fd.append("image[]", new File([img.bytes], "van-design.png", { type: "image/png" }));
        const r = await fetch("https://api.openai.com/v1/images/edits", { method: "POST", headers: { Authorization: "Bearer " + key }, body: fd });
        const j = await r.json().catch(() => ({}));
        if (!r.ok) {
          last = j?.error?.message || "OpenAI error " + r.status;
          console.error(model, last);
          if (/credit|quota|billing/i.test(last)) return json({ error: "Photo-real renders are temporarily unavailable. Please try again later, or request a quote and we'll render it for you." }, 503);
          if (r.status === 404 || /model|input_fidelity|quality|parameter/i.test(last)) continue;
          return json({ error: "The render service is busy. Please try again in a minute." }, 502);
        }
        b64 = j.data?.[0]?.b64_json || "";
        if (b64) break;
      }
      if (!b64) return json({ error: "The render service is busy. Please try again in a minute." }, 502);
      await db.from("lead_events").insert({ lead_id: s.lead_id, event_type: "designer_render_generated", payload: { design_id: design.id, scene } });
      return json({ ok: true, image: "data:image/png;base64," + b64, remaining: Math.max(0, DAILY_LIMIT - used - 1) });
    }

    if (body.action === "save") {
      const img = dataUrlBytes(body.image, 8 * 1024 * 1024);
      if (!img) return json({ error: "Invalid image" }, 400);
      const ext = img.type === "image/png" ? "png" : img.type === "image/webp" ? "webp" : "jpg";
      const path = `${design.id}/${Date.now()}-${scene}.${ext}`;
      const { error } = await db.storage.from(BUCKET).upload(path, img.bytes, { contentType: img.type, upsert: false });
      if (error) return json({ error: "Couldn't save the render." }, 500);
      const url = db.storage.from(BUCKET).getPublicUrl(path).data.publicUrl;
      const renders = [{ url, scene, created_at: new Date().toISOString() }, ...(design.renders || [])].slice(0, 30);
      await db.from("van_designer_designs").update({ renders, updated_at: new Date().toISOString() }).eq("id", design.id);
      if (s.lead_id) await db.from("lead_events").insert({ lead_id: s.lead_id, event_type: "designer_render_saved", payload: { design_id: design.id, scene, url } });
      return json({ ok: true, url, renders });
    }

    if (body.action === "list") return json({ ok: true, renders: design.renders || [] });
    return json({ error: "Unknown action" }, 400);
  } catch (e) {
    console.error(e);
    return json({ error: "Something went wrong. Please try again." }, 500);
  }
});
