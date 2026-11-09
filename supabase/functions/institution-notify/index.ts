// "institution-notify": an institution admin pressed "Request invoice" → email the owner (support@moneyviel.com) the order,
// and send the admin a copy. POST { order_id } with the admin's token. Checked in SQL (studyverse._inst_order_mail: only
// someone who manages the institution; at most once per 10 minutes per order). Secrets: BREVO_API_KEY (+ automatic ones).
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const OWNER = 'support@moneyviel.com';
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const inr = (n: unknown) => '₹' + Number(n || 0).toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
const H = () => { const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }; if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`; return h; };

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const ur = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: req.headers.get('Authorization') || '' } });
    const user = ur.ok ? await ur.json() : null;
    if (!user?.id) return json({ ok: false, msg: 'Please sign in again.' }, 401);
    const b = await req.json().catch(() => ({}));
    const id = String(b.order_id || '');
    if (!/^[0-9a-f-]{36}$/i.test(id)) return json({ ok: false, msg: 'Order not found.' }, 400);
    const r = await fetch(`${URL_}/rest/v1/rpc/_inst_order_mail`, { method: 'POST', headers: H(), body: JSON.stringify({ p_order: id, p_caller: user.id }) });
    const res = r.ok ? await r.json() : null;
    if (!res?.ok) return json({ ok: false, msg: res?.msg || 'Could not send the request.' });
    if (!BREVO) return json({ ok: true, mailed: false, msg: 'Your order is saved. Email is not set up yet — please write to support@moneyviel.com.' });
    const o = res.order, by = res.buyer || o.buyer || {};
    const rows = (o.lines || []).map((l: any) => `<tr><td style="padding:4px 8px">${esc(l.label)}</td><td style="padding:4px 8px;text-align:right">${l.students}</td><td style="padding:4px 8px;text-align:right">${inr(l.rate)} × 10</td><td style="padding:4px 8px;text-align:right">${inr(l.amount)}</td></tr>`).join('');
    const html = `<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;color:#111">
<h2 style="color:#5B0F1B">Invoice request · ${esc(o.invoice_no || '')}</h2>
<p><b>${esc(by.name)}</b>${by.city ? ', ' + esc(by.city) : ''}${by.state ? ' (' + esc(by.state) + ')' : ''}<br>GSTIN: ${esc(by.gstin || '—')}<br>
Contact: ${esc(by.contact_name || '')} · ${esc(by.contact_email || '')} · ${esc(by.contact_phone || '')}<br>Requested by: ${esc(res.by)}</p>
<table style="border-collapse:collapse;border:1px solid #ddd"><thead><tr><th style="padding:4px 8px;text-align:left">Group</th><th style="padding:4px 8px">Students</th><th style="padding:4px 8px">Rate / month</th><th style="padding:4px 8px">Amount</th></tr></thead><tbody>${rows}</tbody></table>
<p>Subtotal ${inr(o.subtotal)} · Discount ${o.discount_pct}% (−${inr(o.discount_amt)}) · Taxable ${inr(o.taxable)}<br>${esc(o.gst?.note || '')} ${o.gst?.amount ? inr(o.gst.amount) : ''}<br>
<b>Total ${inr(o.total)}</b> · Academic year ${esc(o.academic_year)} (seats till 31 March)</p>
<p>Mark it paid in the app: Me → 🏫 Schools (owner) → Orders.</p></body></html>`;
    const s = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({ sender: { name: 'Knowtopia Schools', email: OWNER }, replyTo: { email: res.by || OWNER }, to: [{ email: OWNER }], cc: res.by ? [{ email: res.by }] : undefined,
        subject: `Invoice request ${o.invoice_no || ''}: ${by.name || 'institution'} — ${o.students} students, ${inr(o.total)}`, htmlContent: html, tags: ['inst-invoice'] }) });
    if (!s.ok) { console.log('brevo', s.status, (await s.text()).slice(0, 200)); return json({ ok: true, mailed: false, msg: 'Your order is saved, but the email could not be sent. Please write to support@moneyviel.com.' }); }
    return json({ ok: true, mailed: true });
  } catch (e) {
    console.log(String(e)); return json({ ok: false, msg: 'Something went wrong. Please try again.' }, 500);
  }
});
