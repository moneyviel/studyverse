// "institution-bulk": Knowtopia for Schools — accounts in bulk and staff invites. Called with the signed-in admin's token.
// POST { action: 'bulk', institution_id, rows: [{ name, class: '1'..'12'|'CA', section, roll, email?, parent_email? }] }
//   → rows WITH a student email: an account is made (or found) and added to the class; a NEW account gets an email with a
//     link to set a password (Auth admin generate_link type=recovery, sent by Brevo). An existing account gets a short notice.
//   → rows WITHOUT an email: a single-use roll-number code (studyverse._inst_bulk_prepare); the admin prints the code sheet,
//     students sign up on their phone and enter the code → linked to the class automatically.
//   → parent_email: saved; the parent gets an email to make a Parent account; on sign-in they are linked (Parent Hub).
// POST { action: 'staff', institution_id, email, role: 'admin'|'teacher', name?, class_ids?: [] }
//   → owner (first admin) or institution admin invites staff the same way.
// All permission checks happen in SQL (functions take the caller's id). Rate limits: 10 uploads/hour, 250 emails/day per
// institution (SQL), 500 rows and 100 emails per upload (here). The service role key never leaves this function.
// Secrets: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (automatic), BREVO_API_KEY.
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const APP = 'https://knowtopia.in/';
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const H = (schema = true) => {
  const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json' };
  if (schema) { h['Accept-Profile'] = 'studyverse'; h['Content-Profile'] = 'studyverse'; }
  if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`;
  return h;
};
async function rpc(fn: string, args: unknown) {
  const r = await fetch(`${URL_}/rest/v1/rpc/${fn}`, { method: 'POST', headers: H(), body: JSON.stringify(args) });
  const t = await r.text(); if (!r.ok) throw new Error(`${fn}: ${r.status} ${t.slice(0, 200)}`); return t ? JSON.parse(t) : null;
}
async function who(req: Request) {
  const r = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: req.headers.get('Authorization') || '' } });
  if (!r.ok) return null; const u = await r.json(); return u && u.id ? u : null;
}
// make the account (email already confirmed: the school vouches for it) or find the existing one
async function ensureUser(email: string, meta: Record<string, unknown>): Promise<{ id: string; created: boolean } | null> {
  const r = await fetch(`${URL_}/auth/v1/admin/users`, { method: 'POST', headers: H(false), body: JSON.stringify({ email, email_confirm: true, user_metadata: meta }) });
  if (r.ok) { const j = await r.json(); return j && j.id ? { id: j.id, created: true } : null; }
  const t = await r.text();
  if (!/already|exists|registered/i.test(t)) { console.log('create user', r.status, t.slice(0, 200)); return null; }
  const g = await fetch(`${URL_}/auth/v1/admin/generate_link`, { method: 'POST', headers: H(false), body: JSON.stringify({ type: 'magiclink', email }) });   // no email is sent: only to learn the id
  if (!g.ok) return null; const j = await g.json(); const id = j.id || j.user?.id; return id ? { id, created: false } : null;
}
async function passwordLink(email: string) {
  const g = await fetch(`${URL_}/auth/v1/admin/generate_link`, { method: 'POST', headers: H(false), body: JSON.stringify({ type: 'recovery', email, redirect_to: APP }) });
  if (!g.ok) return null; const j = await g.json(); return j.action_link || j.properties?.action_link || null;
}
const shell = (title: string, body: string) => `<!doctype html><html><body style="margin:0;background:#f4f4f5;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#fff;border-radius:14px;overflow:hidden">
<tr><td style="background:#5B0F1B;color:#fff;padding:18px 24px;font-size:20px;font-weight:bold">Knowtopia<div style="font-size:13px;font-weight:normal;opacity:.85;margin-top:2px">for Schools &amp; Coaching</div></td></tr>
<tr><td style="padding:24px"><h1 style="font-size:21px;margin:0 0 12px">${title}</h1>${body}</td></tr></table>
<p style="font-size:12px;color:#888;margin:14px 0 0">Knowtopia · MoneyViel, Pune, India · knowtopia.in</p></td></tr></table></body></html>`;
const btn = (href: string, t: string) => `<p style="margin:0 0 20px"><a href="${esc(href)}" style="display:inline-block;background:#5B0F1B;color:#fff;text-decoration:none;font-weight:bold;font-size:16px;padding:14px 22px;border-radius:10px">${t}</a></p>`;
const P = (t: string) => `<p style="font-size:16px;line-height:1.5;margin:0 0 16px">${t}</p>`;
async function send(to: string, subject: string, html: string, text: string, tag: string) {
  const s = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({ sender: { name: 'Knowtopia', email: 'support@moneyviel.com' }, replyTo: { email: 'support@moneyviel.com' }, to: [{ email: to }], subject, htmlContent: html, textContent: text, tags: [tag] }) });
  if (!s.ok) console.log('brevo', s.status, (await s.text()).slice(0, 200));
  return s.ok;
}
async function inviteMail(email: string, created: boolean, school: string, what: string, name: string) {
  const hi = name ? `Hi ${esc(name)},` : 'Hello,';
  if (created) {
    const link = await passwordLink(email); if (!link) return false;
    return send(email, `${school}: your Knowtopia account is ready`,
      shell(`${hi} welcome to Knowtopia 🎉`, P(`<b>${esc(school)}</b> has made a Knowtopia account for you (${esc(what)}).`) + P('Tap the button on your phone to choose your password. Then you can learn, practise and play.') + btn(link, 'Set my password') +
        `<p style="font-size:13px;color:#666;margin:0">The link works once. If it has expired, open knowtopia.in, tap Sign in → Forgot password, and use this email (${esc(email)}).</p>`),
      `${name ? 'Hi ' + name + ',' : 'Hello,'} ${school} made a Knowtopia account for you (${what}). Set your password: ${link}`, 'inst-invite');
  }
  return send(email, `${school} added you on Knowtopia`,
    shell(`${hi} you have been added 🏫`, P(`<b>${esc(school)}</b> added your Knowtopia account (${esc(email)}) as ${esc(what)}.`) + P('Just sign in as usual on knowtopia.in.') + btn(APP, 'Open Knowtopia')),
    `${school} added your Knowtopia account (${email}) as ${what}. Sign in as usual: ${APP}`, 'inst-added');
}
async function parentMail(email: string, child: string, school: string) {
  const link = `${APP}?pinvite=1&email=${encodeURIComponent(email)}`;
  return send(email, `${school}: follow ${child}'s learning on Knowtopia`,
    shell('See how your child is learning 👨‍👩‍👧', P(`<b>${esc(school)}</b> uses Knowtopia. You can follow <b>${esc(child)}</b>'s study time, strong and weak topics and homework in <b>Parent Hub</b> — free.`) +
      P(`Tap the button and create a <b>Parent</b> account with <b>this email (${esc(email)})</b>. Already have one? Just sign in — ${esc(child)} appears by itself.`) + btn(link, 'Open Parent Hub') +
      '<p style="font-size:13px;color:#666;margin:0">Not expecting this? You can ignore this email.</p>'),
    `${school} uses Knowtopia. Create a Parent account with this email (${email}) to follow ${child}'s learning: ${link}`, 'inst-parent');
}
const str = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f<>]/g, ' ').trim().slice(0, n);

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ ok: false, msg: 'Use POST.' }, 405);
  try {
    const user = await who(req);
    if (!user) return json({ ok: false, msg: 'Please sign in again.' }, 401);
    const b = await req.json().catch(() => ({}));
    const inst = String(b.institution_id || '');
    if (!UUID_RE.test(inst)) return json({ ok: false, msg: 'Choose the institution.' }, 400);

    if (b.action === 'bulk') {
      if (!Array.isArray(b.rows) || !b.rows.length) return json({ ok: false, msg: 'No rows found.' });
      if (b.rows.length > 500) return json({ ok: false, msg: 'Up to 500 students per upload. Please split the list.' });
      const rows = b.rows.map((r: any) => ({ name: str(r?.name, 60), class: str(r?.class, 20), section: str(r?.section, 40), roll: str(r?.roll, 20),
        email: str(r?.email, 120).toLowerCase(), parent_email: str(r?.parent_email, 120).toLowerCase() }));
      const nEmail = rows.filter((r: any) => r.email).length;
      if (nEmail > 100) return json({ ok: false, msg: `Up to 100 student emails per upload (this list has ${nEmail}). Upload the rest separately.` });
      if (!BREVO && rows.some((r: any) => r.email || r.parent_email)) return json({ ok: false, msg: 'Email is not set up yet. Upload without emails to get roll-number codes.' });
      const prep = await rpc('_inst_bulk_prepare', { p_caller: user.id, p_inst: inst, p_rows: rows });
      if (!prep?.ok) return json({ ok: false, msg: prep?.msg || 'Could not read the list.' });
      const school = String(prep.institution || 'Your school');
      const added: any[] = [], failed: any[] = [...(prep.errors || [])], parents: string[] = [];
      const queue = [...(prep.invites || [])];
      const work = async () => {
        for (let it = queue.shift(); it; it = queue.shift()) {
          try {
            const u = await ensureUser(it.email, { sv_role: 'student', name: it.name });
            if (!u) { failed.push({ row: it.row, msg: 'Could not make the account for ' + it.email }); continue; }
            const res = await rpc('_inst_add_member', { p_inst: inst, p_user: u.id, p_role: 'student', p_class: it.class_id, p_roll: it.roll, p_name: it.name });
            if (!res?.ok) { failed.push({ row: it.row, msg: res?.msg || 'Could not add to the class.' }); continue; }
            const mailed = await inviteMail(it.email, u.created, school, `student, ${it.class_name}`, it.name);
            added.push({ row: it.row, email: it.email, name: it.name, class_name: it.class_name, created: u.created, mailed });
            if (it.parent_email) parents.push(JSON.stringify([it.parent_email, it.name]));
          } catch (e) { failed.push({ row: it.row, msg: 'Something went wrong for ' + it.email }); console.log(String(e)); }
        }
      };
      await Promise.all([work(), work(), work(), work()]);
      for (const c of prep.codes || []) if (c.parent_email) parents.push(JSON.stringify([c.parent_email, c.name]));
      let parentMails = 0;
      for (const p of [...new Set(parents)]) { const [e, n] = JSON.parse(p); if (BREVO && await parentMail(e, n, school)) parentMails++; }
      return json({ ok: true, institution: school, classes_created: prep.classes_created, codes: prep.codes, added, failed, parent_emails: parentMails });
    }

    if (b.action === 'staff') {
      const email = str(b.email, 120).toLowerCase(), role = String(b.role || ''), name = str(b.name, 60);
      if (!EMAIL_RE.test(email)) return json({ ok: false, msg: 'Please enter a valid email.' });
      if (!BREVO) return json({ ok: false, msg: 'Email is not set up yet.' });
      const chk = await rpc('_inst_staff_ok', { p_caller: user.id, p_inst: inst, p_role: role });
      if (!chk?.ok) return json({ ok: false, msg: chk?.msg || 'Not allowed.' });
      const u = await ensureUser(email, { name });
      if (!u) return json({ ok: false, msg: 'Could not make the account. Please try again.' });
      const classes = (Array.isArray(b.class_ids) ? b.class_ids : []).map(String).filter((x: string) => UUID_RE.test(x)).slice(0, 40);
      let res = await rpc('_inst_add_member', { p_inst: inst, p_user: u.id, p_role: role, p_class: role === 'teacher' && classes[0] ? classes[0] : null, p_roll: null, p_name: name || null });
      if (!res?.ok) return json({ ok: false, msg: res?.msg || 'Could not add.' });
      for (const c of role === 'teacher' ? classes.slice(1) : []) await rpc('_inst_add_member', { p_inst: inst, p_user: u.id, p_role: 'teacher', p_class: c, p_roll: null, p_name: null });
      const mailed = await inviteMail(email, u.created, String(chk.institution || 'Your school'), role === 'admin' ? 'an admin' : 'a teacher', name);
      return json({ ok: true, created: u.created, mailed });
    }
    return json({ ok: false, msg: 'Unknown request' }, 400);
  } catch (e) {
    console.log(String(e)); return json({ ok: false, msg: 'Something went wrong. Please try again.' }, 500);
  }
});
