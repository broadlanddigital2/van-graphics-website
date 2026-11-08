// Van Designer back end for Norwich Vehicle Graphics (shared CRM project).
// Passwordless accounts: sign-up logs the customer straight in and emails a login link
// for returning on another device. Every account is a CRM customer + lead, so the team
// sees who is designing, what van they have and when they ask for a quote.
//
// POST JSON { action, ... }. Authenticated actions send { token } (the session token
// returned by signup/redeem). Tokens are stored as sha256 hashes only.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.57.4";

const BUSINESS_SLUG = "norwich-vehicle-graphics";
const CHANNEL_KEY = "318764b3-e82a-4b82-b832-dda45ab860a3"; // "Norwich Vehicle Graphics Web Forms"
const TEAM_EMAIL = Deno.env.get("NVG_TEAM_EMAIL") || "production@broadlanddigital.co.uk";
const FALLBACK_FROM = "noreply@racecargraphics.uk";
const SESSION_DAYS = 180;
const LINK_HOURS = 48;
const MAX_STATE_BYTES = 1_800_000;
const EVENT_TYPES = new Set(["designs_generated", "layout_viewed", "view_360", "lifestyle_view", "logo_uploaded", "reg_entered", "design_opened"]);

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST,OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const clean = (v: unknown, max = 200) => {
  if (v === null || v === undefined) return null;
  const s = String(v).trim().slice(0, max);
  return s || null;
};
const esc = (v: unknown) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
const isEmail = (v: string | null) => !!v && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

async function sha256(value: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
function newToken() {
  const b = new Uint8Array(32);
  crypto.getRandomValues(b);
  return btoa(String.fromCharCode(...b)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function ukPhone(v: string | null) {
  if (!v) return null;
  let s = v.replace(/[^\d+]/g, "");
  if (s.startsWith("00")) s = "+" + s.slice(2);
  if (s.startsWith("0")) s = "+44" + s.slice(1);
  else if (s.startsWith("44")) s = "+" + s;
  return s || null;
}

const secretKeysRaw = Deno.env.get("SUPABASE_SECRET_KEYS");
const serviceKey = secretKeysRaw ? JSON.parse(secretKeysRaw)["default"] : Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const db = createClient(Deno.env.get("SUPABASE_URL")!, serviceKey!, { auth: { persistSession: false, autoRefreshToken: false } });

let ctxCache: any = null;
async function context() {
  if (ctxCache) return ctxCache;
  const { data: bu } = await db.from("business_units").select("id,name,slug,website_url,outbound_from_email,outbound_from_name,contact_phone,address_text").eq("slug", BUSINESS_SLUG).single();
  const { data: ch } = await db.from("channel_integrations").select("id,workflow_id,default_stage_id").eq("public_key", CHANNEL_KEY).single();
  if (!bu || !ch) throw new Error("Van Designer is not configured");
  ctxCache = { bu, ch };
  return ctxCache;
}

async function sendEmail(to: string, subject: string, html: string, text: string, replyTo?: string) {
  const sg = Deno.env.get("SENDGRID_API_KEY");
  if (!sg) return false;
  const { bu } = await context();
  const r = await fetch("https://api.sendgrid.com/v3/mail/send", {
    method: "POST",
    headers: { Authorization: "Bearer " + sg, "Content-Type": "application/json" },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: bu.outbound_from_email || FALLBACK_FROM, name: bu.outbound_from_name || bu.name },
      ...(replyTo ? { reply_to: { email: replyTo } } : { reply_to: { email: TEAM_EMAIL, name: bu.name } }),
      subject,
      content: [{ type: "text/plain", value: text }, { type: "text/html", value: html }],
    }),
  });
  if (!r.ok) console.error("sendgrid", r.status, await r.text());
  return r.ok;
}

function shell(bu: any, title: string, body: string) {
  return `<!doctype html><html><body style="margin:0;background:#eef1f7;font-family:Arial,Helvetica,sans-serif;color:#141f38">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef1f7"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#fff">
<tr><td style="background:#111b31;padding:22px 28px;border-bottom:4px solid #ffac62;color:#fff;font:800 18px Arial,sans-serif;letter-spacing:.06em">NORWICH <span style="font-weight:400;font-size:12px;letter-spacing:.14em">VEHICLE GRAPHICS</span></td></tr>
<tr><td style="padding:30px 28px;font-size:15px;line-height:1.6"><h1 style="font-size:22px;margin:0 0 12px">${esc(title)}</h1>${body}</td></tr>
<tr><td style="background:#111b31;color:#cfd9f5;padding:20px 28px;font-size:12px;line-height:1.6">${esc(bu.name)} · ${esc(bu.contact_phone || "")}<br>${esc(bu.address_text || "")}</td></tr>
</table></td></tr></table></body></html>`;
}
const button = (href: string, label: string) =>
  `<p style="margin:22px 0"><a href="${esc(href)}" style="display:inline-block;background:#ffac62;color:#111b31;padding:14px 22px;text-decoration:none;font-weight:bold">${esc(label)}</a></p>`;

async function siteUrl() {
  const { bu } = await context();
  return String(bu.website_url || "").replace(/\/+$/, "");
}

async function issueToken(customerId: string, leadId: string | null, kind: "session" | "link", ua: string | null) {
  const { bu } = await context();
  const token = newToken();
  const ms = kind === "session" ? SESSION_DAYS * 864e5 : LINK_HOURS * 36e5;
  await db.from("van_designer_sessions").insert({
    business_unit_id: bu.id, customer_id: customerId, lead_id: leadId, token_hash: await sha256(token), kind,
    expires_at: new Date(Date.now() + ms).toISOString(), user_agent: ua?.slice(0, 300) || null,
  });
  return token;
}

async function sendLoginLink(customer: any, leadId: string | null, ua: string | null, welcome: boolean) {
  const { bu } = await context();
  const link = await issueToken(customer.id, leadId, "link", ua);
  const url = `${await siteUrl()}/design-your-van/?login=${encodeURIComponent(link)}#designer`;
  const first = customer.first_name || "there";
  const title = welcome ? "Your Van Designer account is ready" : "Your Van Designer login link";
  const intro = welcome
    ? `<p>Hi ${esc(first)}, thanks for signing up. You're already logged in on the device you used.</p><p>To pick up your designs on another phone or computer, use this button. It works once and lasts ${LINK_HOURS} hours, and you can request a new one any time from the designer.</p>`
    : `<p>Hi ${esc(first)}, here's your login link for the Van Designer. It works once and lasts ${LINK_HOURS} hours.</p>`;
  const html = shell(bu, title, intro + button(url, "Open my designs") + `<p style="font-size:13px;color:#485774">If you didn't ask for this, you can ignore this email.</p>`);
  const text = `${title}\n\nHi ${first},\n\nOpen your designs: ${url}\n\nThe link works once and lasts ${LINK_HOURS} hours.\n\n${bu.name} · ${bu.contact_phone || ""}`;
  return await sendEmail(customer.email, title, html, text);
}

async function sessionFrom(token: unknown) {
  const t = clean(token, 200);
  if (!t) return null;
  const { data } = await db.from("van_designer_sessions").select("id,customer_id,lead_id,expires_at,revoked_at,kind,last_seen_at")
    .eq("token_hash", await sha256(t)).eq("kind", "session").maybeSingle();
  if (!data || data.revoked_at || new Date(data.expires_at) < new Date()) return null;
  if (!data.last_seen_at || Date.now() - new Date(data.last_seen_at).getTime() > 36e5) {
    await db.from("van_designer_sessions").update({ last_seen_at: new Date().toISOString() }).eq("id", data.id);
  }
  return data;
}

async function profile(customerId: string) {
  const { data: c } = await db.from("customers").select("id,first_name,last_name,email,phone,mobile,company_id,companies(name)").eq("id", customerId).single();
  const { bu } = await context();
  const { data: consent } = await db.from("customer_marketing_consents").select("consented").eq("business_unit_id", bu.id).eq("customer_id", customerId).eq("channel", "email").maybeSingle();
  return {
    name: [c?.first_name, c?.last_name].filter((x) => x && x !== "-").join(" "),
    email: c?.email, phone: c?.mobile || c?.phone || "", company: (c as any)?.companies?.name || "", consent: !!consent?.consented,
  };
}

async function listDesigns(customerId: string) {
  const { bu } = await context();
  const { data } = await db.from("van_designer_designs").select("id,name,vehicle,status,preview_svg,updated_at,quote_requested_at")
    .eq("business_unit_id", bu.id).eq("customer_id", customerId).neq("status", "archived").order("updated_at", { ascending: false }).limit(50);
  return data || [];
}

async function event(leadId: string | null, type: string, payload: unknown) {
  if (!leadId) return;
  const { ch } = await context();
  await db.from("lead_events").insert({ lead_id: leadId, channel_integration_id: ch.id, event_type: "designer_" + type, payload });
}

async function findOrCreateCustomer(email: string, first: string, last: string, phone: string | null, companyName: string | null) {
  let companyId: string | null = null;
  if (companyName) {
    const { data: m } = await db.from("companies").select("id").ilike("name", companyName).limit(1);
    if (m?.[0]) companyId = m[0].id;
    else {
      const { data: created } = await db.from("companies").insert({ name: companyName }).select("id").single();
      companyId = created?.id || null;
    }
  }
  const { data: found } = await db.from("customers").select("*").eq("email", email).limit(1);
  let customer = found?.[0] || null;
  if (customer) {
    const patch: Record<string, unknown> = {};
    if (!customer.mobile && !customer.phone && phone) patch.mobile = phone;
    if (!customer.company_id && companyId) patch.company_id = companyId;
    if (Object.keys(patch).length) await db.from("customers").update(patch).eq("id", customer.id);
  } else {
    const { data: created, error } = await db.from("customers").insert({
      first_name: first, last_name: last || "-", email, mobile: phone, company_id: companyId, country: "United Kingdom", source: "van_designer",
    }).select("*").single();
    if (error) throw new Error(error.message);
    customer = created;
  }
  return { customer, companyId: companyId || customer.company_id || null };
}

async function designerLead(customer: any, companyId: string | null, body: any) {
  const { bu, ch } = await context();
  const { data: existing } = await db.from("leads").select("id").eq("business_unit_id", bu.id).eq("customer_id", customer.id)
    .is("deleted_at", null).eq("raw_payload->>source", "van_designer").eq("raw_payload->>kind", "signup")
    .order("created_at", { ascending: false }).limit(1);
  if (existing?.[0]) return { id: existing[0].id, created: false };
  const src = body.source || {};
  const { data: lead, error } = await db.from("leads").insert({
    business_unit_id: bu.id, channel_integration_id: ch.id, workflow_id: ch.workflow_id, stage_id: ch.default_stage_id,
    customer_id: customer.id, company_id: companyId, first_name: customer.first_name, last_name: customer.last_name,
    email: customer.email, mobile: customer.mobile, phone: customer.phone,
    subject: `Van Designer sign-up – ${[customer.first_name, customer.last_name].filter((x: string) => x && x !== "-").join(" ")}`,
    message: "Signed up to use the Van Designer." + (body.consent ? " Marketing consent: yes." : " Marketing consent: no."),
    source_url: clean(src.landing || body.page, 500), utm_source: clean(src.utm_source), utm_medium: clean(src.utm_medium),
    utm_campaign: clean(src.utm_campaign), gclid: clean(src.gclid, 300),
    raw_payload: { source: "van_designer", kind: "signup", referrer: clean(src.ref, 500), page: clean(body.page, 500) },
  }).select("id").single();
  if (error) throw new Error(error.message);
  await db.from("lead_events").insert({ lead_id: lead.id, channel_integration_id: ch.id, event_type: "received", payload: { source: "van_designer" } });
  return { id: lead.id, created: true };
}

function summary(vehicle: any, state: any) {
  const v = vehicle || {}, s = state || {};
  return [
    `Vehicle: ${v.make || "-"} ${v.model || ""} ${v.lwb ? "LWB" : "SWB"}${v.reg ? ` (${v.reg})` : ""}`,
    `Body colour: ${v.colour || "-"}`,
    `Style: ${s.mode === "wrap" ? "Full wrap" : "Graphics"}${s.layoutName ? ` · layout ${s.layoutName}` : ""}`,
    `Company on van: ${s.company || "-"}`, `Tagline: ${s.tagline || "-"}`, `Phone on van: ${s.phone || "-"}`,
    `Website: ${s.web || "-"}`, `Services: ${(s.services || []).join(", ") || "-"}`, `Logo uploaded: ${s.logo ? "yes" : "no"}`,
    `Brand colours: ${s.P || "-"} / ${s.S || "-"}`,
  ].join("\n");
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST required" }, 405);
  let body: any;
  try { body = await req.json(); } catch { return json({ error: "Invalid JSON" }, 400); }
  const ua = req.headers.get("user-agent");
  try {
    const { bu, ch } = await context();
    switch (body.action) {
      case "signup": {
        const name = clean(body.name, 120), email = clean(body.email, 160)?.toLowerCase() || null;
        if (!name) return json({ error: "Please enter your name." }, 400);
        if (!isEmail(email)) return json({ error: "Please enter a valid email address." }, 400);
        const parts = name.split(/\s+/);
        const first = parts.shift()!, last = parts.join(" ");
        const phone = ukPhone(clean(body.phone, 40));
        const { customer, companyId } = await findOrCreateCustomer(email!, first, last, phone, clean(body.company, 160));
        const lead = await designerLead(customer, companyId, body);
        if (body.consent === true) {
          await db.from("customer_marketing_consents").upsert({
            business_unit_id: bu.id, customer_id: customer.id, channel: "email", consented: true, source: "van_designer",
            captured_at: new Date().toISOString(), withdrawn_at: null, metadata: { page: clean(body.page, 500) },
          }, { onConflict: "business_unit_id,customer_id,channel" });
        }
        await event(lead.id, lead.created ? "signup" : "signup_returning", { consent: !!body.consent, source: body.source || null });
        const token = await issueToken(customer.id, lead.id, "session", ua);
        const emailed = await sendLoginLink(customer, lead.id, ua, true).catch(() => false);
        return json({ ok: true, token, returning: !lead.created, emailed, user: await profile(customer.id), designs: await listDesigns(customer.id) }, 201);
      }
      case "request_link": {
        const email = clean(body.email, 160)?.toLowerCase() || null;
        if (!isEmail(email)) return json({ error: "Please enter a valid email address." }, 400);
        const { data: c } = await db.from("customers").select("id,first_name,email").eq("email", email).limit(1);
        const customer = c?.[0];
        if (customer) {
          const { data: lead } = await db.from("leads").select("id").eq("business_unit_id", bu.id).eq("customer_id", customer.id)
            .eq("raw_payload->>source", "van_designer").is("deleted_at", null).limit(1);
          if (lead?.[0]) {
            const since = new Date(Date.now() - 36e5).toISOString();
            const { count } = await db.from("van_designer_sessions").select("id", { count: "exact", head: true })
              .eq("customer_id", customer.id).eq("kind", "link").gte("created_at", since);
            if ((count || 0) < 5) await sendLoginLink(customer, lead[0].id, ua, false);
          }
        }
        // Same answer whether or not the address has an account.
        return json({ ok: true });
      }
      case "redeem": {
        const t = clean(body.link, 200);
        if (!t) return json({ error: "Missing link" }, 400);
        const { data: link } = await db.from("van_designer_sessions").select("*").eq("token_hash", await sha256(t)).eq("kind", "link").maybeSingle();
        if (!link || link.used_at || link.revoked_at || new Date(link.expires_at) < new Date()) {
          return json({ error: "This login link has expired or been used. Request a new one below." }, 401);
        }
        await db.from("van_designer_sessions").update({ used_at: new Date().toISOString() }).eq("id", link.id);
        const token = await issueToken(link.customer_id, link.lead_id, "session", ua);
        await event(link.lead_id, "login", { via: "email_link" });
        return json({ ok: true, token, user: await profile(link.customer_id), designs: await listDesigns(link.customer_id) });
      }
      case "me": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        return json({ ok: true, user: await profile(s.customer_id), designs: await listDesigns(s.customer_id) });
      }
      case "save_design": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        const d = body.design || {};
        const state = d.state || {};
        if (JSON.stringify(state).length > MAX_STATE_BYTES) state.logo = null;
        const row = {
          name: clean(d.name, 120), vehicle: d.vehicle || {}, state,
          preview_svg: typeof d.preview_svg === "string" && d.preview_svg.length < 400_000 ? d.preview_svg : null,
          updated_at: new Date().toISOString(),
        };
        if (d.id) {
          const { data, error } = await db.from("van_designer_designs").update(row).eq("id", d.id).eq("customer_id", s.customer_id).select("id").maybeSingle();
          if (error || !data) return json({ error: "Design not found" }, 404);
          return json({ ok: true, id: data.id });
        }
        const { data, error } = await db.from("van_designer_designs").insert({ ...row, business_unit_id: bu.id, customer_id: s.customer_id, lead_id: s.lead_id }).select("id").single();
        if (error) return json({ error: error.message }, 500);
        await event(s.lead_id, "design_saved", { design_id: data.id, vehicle: row.vehicle, style: state.mode || null });
        return json({ ok: true, id: data.id, created: true });
      }
      case "get_design": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        const { data } = await db.from("van_designer_designs").select("id,name,vehicle,state,status,updated_at").eq("id", clean(body.id, 60)).eq("customer_id", s.customer_id).maybeSingle();
        if (!data) return json({ error: "Design not found" }, 404);
        return json({ ok: true, design: data });
      }
      case "delete_design": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        await db.from("van_designer_designs").update({ status: "archived", updated_at: new Date().toISOString() }).eq("id", clean(body.id, 60)).eq("customer_id", s.customer_id);
        return json({ ok: true, designs: await listDesigns(s.customer_id) });
      }
      case "event": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        const type = clean(body.type, 40);
        if (!type || !EVENT_TYPES.has(type)) return json({ error: "Unknown event" }, 400);
        await event(s.lead_id, type, body.data || null);
        return json({ ok: true });
      }
      case "quote": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        const { data: design } = await db.from("van_designer_designs").select("*").eq("id", clean(body.design_id, 60)).eq("customer_id", s.customer_id).maybeSingle();
        if (!design) return json({ error: "Save your design first." }, 404);
        const user = await profile(s.customer_id);
        const phone = ukPhone(clean(body.phone, 40));
        if (phone) {
          const { data: c } = await db.from("customers").select("mobile,phone").eq("id", s.customer_id).single();
          if (!c?.mobile && !c?.phone) await db.from("customers").update({ mobile: phone }).eq("id", s.customer_id);
        }
        const notes = clean(body.notes, 1200), pref = clean(body.pref, 30) || "Phone";
        const v = design.vehicle || {};
        const message = summary(v, design.state) + `\n\nContact preference: ${pref}` + (phone ? `\nPhone: ${phone}` : "") + (notes ? `\nNotes: ${notes}` : "") + `\n\nDesign ID: ${design.id}`;
        const [first, ...rest] = (user.name || "").split(" ");
        const { data: c2 } = await db.from("customers").select("company_id,mobile,phone").eq("id", s.customer_id).single();
        const { data: origin } = s.lead_id ? await db.from("leads").select("utm_source,utm_medium,utm_campaign,gclid").eq("id", s.lead_id).maybeSingle() : { data: null };
        const { data: qlead, error } = await db.from("leads").insert({
          business_unit_id: bu.id, channel_integration_id: ch.id, workflow_id: ch.workflow_id, stage_id: ch.default_stage_id,
          customer_id: s.customer_id, company_id: c2?.company_id || null, first_name: first || null, last_name: rest.join(" ") || null,
          email: user.email, mobile: phone || c2?.mobile || null, phone: c2?.phone || null,
          subject: `Van Designer quote – ${v.make || ""} ${v.model || ""} (${user.name})`.replace(/\s+/g, " "),
          message, source_url: clean(body.page, 500),
          utm_source: origin?.utm_source || null, utm_medium: origin?.utm_medium || null, utm_campaign: origin?.utm_campaign || null, gclid: origin?.gclid || null,
          raw_payload: { source: "van_designer", kind: "quote", design_id: design.id, signup_lead_id: s.lead_id, vehicle: v, style: design.state?.mode || null },
        }).select("id").single();
        if (error) return json({ error: error.message }, 500);
        await db.from("lead_events").insert({ lead_id: qlead.id, channel_integration_id: ch.id, event_type: "received", payload: { source: "van_designer", design_id: design.id } });
        await event(s.lead_id, "quote_requested", { design_id: design.id, quote_lead_id: qlead.id });
        await db.from("van_designer_designs").update({ status: "quote_requested", quote_requested_at: new Date().toISOString(), quote_lead_id: qlead.id }).eq("id", design.id);
        // Alert the team (hot lead) and confirm to the customer.
        const site = await siteUrl();
        const preview = design.preview_svg ? `<p><b>Design preview</b> is attached to the lead in the CRM (design ${esc(design.id)}).</p>` : "";
        await sendEmail(TEAM_EMAIL, `Hot lead: Van Designer quote – ${v.make || ""} ${v.model || ""}`,
          shell(bu, "New Van Designer quote request", `<p><b>${esc(user.name)}</b> · ${esc(user.email)} · ${esc(phone || user.phone || "no phone")}${user.company ? " · " + esc(user.company) : ""}</p><pre style="white-space:pre-wrap;font:14px/1.5 Arial,sans-serif;background:#f4f6ff;padding:14px">${esc(message)}</pre>${preview}`),
          `New Van Designer quote request\n\n${user.name} · ${user.email} · ${phone || user.phone || ""}\n\n${message}`, user.email).catch(() => false);
        await sendEmail(user.email, "We've got your van design", shell(bu, "Thanks, we've got your design",
          `<p>Hi ${esc(first || "there")}, your design for the ${esc(v.make || "")} ${esc(v.model || "")} is with our Norwich team. We'll be in touch by ${esc(pref.toLowerCase())} with a quote.</p><p>Before anything is printed we check your exact vehicle and send you a proof to approve.</p>${button(site + "/design-your-van/#designer", "View my designs")}`),
          `Thanks, we've got your design for the ${v.make || ""} ${v.model || ""}. We'll be in touch by ${pref.toLowerCase()} with a quote.\n\n${site}/design-your-van/`).catch(() => false);
        return json({ ok: true, designs: await listDesigns(s.customer_id) });
      }
      case "reg": {
        const s = await sessionFrom(body.token);
        if (!s) return json({ error: "Signed out" }, 401);
        const reg = String(body.reg || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 8);
        if (!/^[A-Z0-9]{2,8}$/.test(reg)) return json({ error: "Invalid registration" }, 400);
        await event(s.lead_id, "reg_entered", { reg });
        const { data: cached } = await db.from("vehicle_reg_lookups").select("vehicle,found,fetched_at").eq("registration", reg).maybeSingle();
        if (cached && Date.now() - new Date(cached.fetched_at).getTime() < 30 * 864e5) return json({ ok: true, available: true, found: cached.found, vehicle: cached.vehicle ? { make: cached.vehicle.make, colour: cached.vehicle.colour, yearOfManufacture: cached.vehicle.yearOfManufacture, fuelType: cached.vehicle.fuelType } : null });
        const key = Deno.env.get("DVLA_VES_API_KEY");
        if (!key) return json({ ok: true, available: false });
        const r = await fetch("https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles", {
          method: "POST", headers: { "x-api-key": key, "Content-Type": "application/json" }, body: JSON.stringify({ registrationNumber: reg }),
        });
        const found = r.ok;
        const vehicle = found ? await r.json() : null;
        await db.from("vehicle_reg_lookups").upsert({ registration: reg, vehicle, found, fetched_at: new Date().toISOString() });
        return json({ ok: true, available: true, found, vehicle: vehicle ? { make: vehicle.make, colour: vehicle.colour, yearOfManufacture: vehicle.yearOfManufacture, fuelType: vehicle.fuelType } : null });
      }
      case "logout": {
        const t = clean(body.token, 200);
        if (t) await db.from("van_designer_sessions").update({ revoked_at: new Date().toISOString() }).eq("token_hash", await sha256(t));
        return json({ ok: true });
      }
      default:
        return json({ error: "Unknown action" }, 400);
    }
  } catch (e) {
    console.error(e);
    return json({ error: "Something went wrong. Please try again." }, 500);
  }
});
