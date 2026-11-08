// StudyVerse payments (Razorpay). Deployed as "studyverse-pay" in project moneyviel-apps.
// POST { action: 'order', plan, code?, for_child?, grade? }  (school plans unlock ONE class: grade, else the student's saved class)
// POST { action: 'order', plan, code?, for_child? }  (for_child: a parent pays for a linked child; the child gets the plan)
// POST { action: 'order', plan, code? }  → creates a Razorpay order (price and discount decided here, never by the app)
// POST { action: 'verify', order_id, payment_id, signature } → checks the signature and the payment with Razorpay,
//      then unlocks the course (studyverse.grant_paid).
// Secrets (Edge Functions → Secrets): RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET. Without them it answers "Payments not set up yet".
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const KEY_ID = Deno.env.get('RAZORPAY_KEY_ID') || '';
const KEY_SECRET = Deno.env.get('RAZORPAY_KEY_SECRET') || '';
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });

const svc = (extra: Record<string, string> = {}) => {
  const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse', ...extra };
  if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`;
  return h;
};
async function rpc(fn: string, args: unknown) {
  const r = await fetch(`${URL_}/rest/v1/rpc/${fn}`, { method: 'POST', headers: svc(), body: JSON.stringify(args) });
  const t = await r.text(); if (!r.ok) throw new Error(`${fn}: ${t.slice(0, 200)}`); return t ? JSON.parse(t) : null;
}
async function insertPayment(row: unknown) {
  const r = await fetch(`${URL_}/rest/v1/payments`, { method: 'POST', headers: svc({ Prefer: 'return=minimal' }), body: JSON.stringify(row) });
  if (!r.ok) throw new Error('payments: ' + (await r.text()).slice(0, 200));
}
async function findPayment(order: string) {
  const r = await fetch(`${URL_}/rest/v1/payments?order_id=eq.${encodeURIComponent(order)}&select=*`, { headers: svc() });
  const a = await r.json(); return Array.isArray(a) ? a[0] : null;
}
async function who(req: Request) {
  const auth = req.headers.get('Authorization') || '';
  const r = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: auth } });
  if (!r.ok) return null; const u = await r.json(); return u && u.id ? u : null;
}
const rzpAuth = () => 'Basic ' + btoa(`${KEY_ID}:${KEY_SECRET}`);
async function hmac(msg: string) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(KEY_SECRET), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const s = new Uint8Array(await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(msg)));
  return [...s].map(b => b.toString(16).padStart(2, '0')).join('');
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const user = await who(req);
    if (!user) return json({ error: 'Please sign in again.' }, 401);
    const b = await req.json().catch(() => ({}));

    if (b.action === 'order') {
      let target = user.id;
      if (b.for_child) {                               // parent paying for a linked child
        const lr = await fetch(`${URL_}/rest/v1/parent_links?parent_id=eq.${user.id}&child_id=eq.${encodeURIComponent(String(b.for_child))}&select=child_id`, { headers: svc() });
        const la = await lr.json().catch(() => []);
        if (!Array.isArray(la) || !la.length) return json({ error: 'This child is not linked to your account.' });
        target = String(b.for_child);
      }
      // school plans are for ONE class: the class sent by the page, else the student's own class from their saved progress
      let course: string | null = null;
      const plr = await fetch(`${URL_}/rest/v1/plans?id=eq.${encodeURIComponent(String(b.plan || ''))}&select=course`, { headers: svc() });
      const pla = await plr.json().catch(() => []);
      if (Array.isArray(pla) && pla[0] && pla[0].course === 'school') {
        let g = Number(b.grade);
        if (!(g >= 1 && g <= 12)) {
          const pr = await fetch(`${URL_}/rest/v1/progress?user_id=eq.${target}&select=state`, { headers: svc() });
          const pa = await pr.json().catch(() => []);
          g = Number(pa?.[0]?.state?.st?.profile?.grade);
        }
        if (!(Number.isInteger(g) && g >= 1 && g <= 12)) return json({ error: 'Please choose the class first.' });
        course = 'school-g' + g;
      }
      const p = await rpc('price_for', { p_user: target, p_plan: String(b.plan || ''), p_code: b.code || null });
      if (!p || !p.ok) return json({ error: (p && p.msg) || 'This plan is not available.' });
      if (p.amount_paise === 0) {                      // 100% discount: no payment needed
        const order = 'free-' + crypto.randomUUID();
        await insertPayment({ user_id: target, payer_id: user.id, course, plan_id: b.plan, amount_paise: 0, discount_code: p.code, percent: p.percent, order_id: order });
        const g = await rpc('grant_paid', { p_order: order, p_payment: 'free' });
        return json({ paid: true, label: g.label, until: g.until, course: g.course });
      }
      if (!KEY_ID || !KEY_SECRET) return json({ error: 'Payments not set up yet' });
      const r = await fetch('https://api.razorpay.com/v1/orders', { method: 'POST', headers: { Authorization: rzpAuth(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: p.amount_paise, currency: 'INR', receipt: `sv-${Date.now()}`, notes: { user: target, payer: user.id, plan: b.plan, course: course || '', code: p.code || '' } }) });
      const o = await r.json();
      if (!r.ok || !o.id) return json({ error: 'Could not start the payment. Please try again.' });
      await insertPayment({ user_id: target, payer_id: user.id, course, plan_id: b.plan, amount_paise: p.amount_paise, discount_code: p.code, percent: p.percent, order_id: o.id });
      return json({ order_id: o.id, amount: p.amount_paise, key_id: KEY_ID, label: course ? `${p.label} · Class ${course.slice(8)}` : p.label });
    }

    if (b.action === 'verify') {
      if (!KEY_SECRET) return json({ error: 'Payments not set up yet' });
      const pay = await findPayment(String(b.order_id || ''));
      if (!pay || (pay.user_id !== user.id && pay.payer_id !== user.id)) return json({ error: 'Order not found.' });
      if ((await hmac(`${b.order_id}|${b.payment_id}`)) !== b.signature) return json({ error: 'Payment could not be verified.' });
      const r = await fetch(`https://api.razorpay.com/v1/payments/${encodeURIComponent(b.payment_id)}`, { headers: { Authorization: rzpAuth() } });
      const p = await r.json();
      if (!r.ok || p.order_id !== b.order_id || Number(p.amount) !== Number(pay.amount_paise) || !['captured', 'authorized'].includes(p.status))
        return json({ error: 'Payment is not complete yet.' });
      const g = await rpc('grant_paid', { p_order: b.order_id, p_payment: b.payment_id });
      return json({ ok: true, label: g.label, until: g.until, course: g.course });
    }
    return json({ error: 'Unknown request' }, 400);
  } catch (e) {
    return json({ error: 'Something went wrong. Please try again.', detail: String((e as Error).message || e).slice(0, 200) }, 500);
  }
});
