// "parent-invite": a Knowtopia parent invites a child by email. Saves the invite (studyverse.add_invite) and emails the
// child a link to create / sign in to their account; when that email signs in, the app calls claim_invites() and the
// child is linked to the parent. POST { email, name } with the parent's sign-in token → { ok, msg? }.
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const APP = 'https://knowtopia.in/';
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const H = () => { const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }; if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`; return h; };

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const ur = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: req.headers.get('Authorization') || '' } });
    const user = ur.ok ? await ur.json() : null;
    if (!user?.id) return json({ ok: false, msg: 'Please sign in again.' }, 401);
    if (!BREVO) return json({ ok: false, msg: 'Email is not set up yet.' });
    const b = await req.json().catch(() => ({}));
    const email = String(b.email || '').trim().toLowerCase(), name = String(b.name || '').trim().slice(0, 40);
    const r = await fetch(`${URL_}/rest/v1/rpc/add_invite`, { method: 'POST', headers: H(), body: JSON.stringify({ p_parent: user.id, p_email: email, p_name: name }) });
    const res = r.ok ? await r.json() : null;
    if (!res?.ok) return json({ ok: false, msg: res?.msg || 'Could not create the invite. Please try again.' });
    const link = `${APP}?invite=1&email=${encodeURIComponent(email)}`;
    const who = esc(user.email), hi = name ? `Hi ${esc(name)},` : 'Hi,';
    const html = `<!doctype html><html><body style="margin:0;background:#f4f4f5;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#fff;border-radius:14px;overflow:hidden">
<tr><td style="background:#5B0F1B;color:#fff;padding:18px 24px;font-size:20px;font-weight:bold">Knowtopia<div style="font-size:13px;font-weight:normal;opacity:.85;margin-top:2px">Learn, play and grow</div></td></tr>
<tr><td style="padding:24px"><h1 style="font-size:21px;margin:0 0 12px">${hi} you're invited! 🎉</h1>
<p style="font-size:16px;line-height:1.5;margin:0 0 16px">Your parent (<b>${who}</b>) wants to cheer on your learning with Knowtopia — fun lessons, games and practice for school and CA.</p>
<p style="font-size:16px;line-height:1.5;margin:0 0 20px">Tap the button on <b>your</b> phone and create your account with <b>this email (${esc(email)})</b>. You'll be linked to your parent automatically.</p>
<p style="margin:0 0 20px"><a href="${link}" style="display:inline-block;background:#5B0F1B;color:#fff;text-decoration:none;font-weight:bold;font-size:16px;padding:14px 22px;border-radius:10px">Start Knowtopia</a></p>
<p style="font-size:13px;color:#666;margin:0">Already have an account with this email? Just sign in — the link happens by itself. Not expecting this? You can ignore this email.</p>
</td></tr></table><p style="font-size:12px;color:#888;margin:14px 0 0">Knowtopia · Pune, India · knowtopia.in</p></td></tr></table></body></html>`;
    const text = `${name ? 'Hi ' + name + ',' : 'Hi,'} your parent (${user.email}) invited you to Knowtopia.\nCreate your account with this email (${email}) on your phone: ${link}\nAlready have an account? Just sign in.`;
    const s = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({ sender: { name: 'Knowtopia', email: 'support@moneyviel.com' }, replyTo: { email: 'support@moneyviel.com' }, to: [{ email }], subject: `${name || 'You'}: your parent invited you to Knowtopia`, htmlContent: html, textContent: text, tags: ['parent-invite'] }) });
    if (!s.ok) { console.log('brevo', s.status, (await s.text()).slice(0, 200)); return json({ ok: false, msg: 'Invite saved, but the email could not be sent. Please try again in a minute.' }); }
    return json({ ok: true, exists: !!res.exists });
  } catch (e) {
    console.log(String(e)); return json({ ok: false, msg: 'Something went wrong. Please try again.' }, 500);
  }
});
