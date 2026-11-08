// "auth-email": Supabase Auth Send Email Hook for project moneyviel-apps (StudyVerse, Salonzy, Football Club share one auth).
// Every sign-up / password-reset / email-change / magic-link email comes here; we pick the sender + branding per app and
// send it through Brevo (secret BREVO_API_KEY). The request is verified with the hook secret (SEND_EMAIL_HOOK_SECRET).
// If the app's own sender fails (e.g. domain not verified in Brevo) we retry once from support@moneyviel.com.
/* eslint-disable */
import { Webhook } from 'https://esm.sh/standardwebhooks@1.0.0';

const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const HOOK = (Deno.env.get('SEND_EMAIL_HOOK_SECRET') || '').replace('v1,whsec_', '');
const SB = Deno.env.get('SUPABASE_URL')!;

type Brand = { name: string; from: string; color: string; site: string; tag: string };
const BRANDS: Record<string, Brand> = {
  studyverse: { name: 'StudyVerse', from: 'support@moneyviel.com', color: '#5B0F1B', site: 'https://study.moneyviel.com/', tag: 'Learn, play and grow' },
  salonzy: { name: 'Salonzy', from: 'support@salonzy.in', color: '#7C3AED', site: 'https://www.salonzy.in/', tag: 'Your salon, simplified' },
  football: { name: 'Football Club Portal', from: 'support@moneyviel.com', color: '#0F5132', site: 'https://demo.moneyviel.com/', tag: 'Your club, organised' },
  moneyviel: { name: 'MoneyViel', from: 'support@moneyviel.com', color: '#1F2937', site: 'https://moneyviel.com/', tag: '' },
};
function appOf(user: any, redirect: string): string {
  const a = String(user?.user_metadata?.app || user?.raw_user_meta_data?.app || '').toLowerCase();
  if (BRANDS[a]) return a;
  if (/salonzy/i.test(redirect)) return 'salonzy';
  if (/demo\.moneyviel\.com|football/i.test(redirect)) return 'football';
  if (/study\.moneyviel\.com|studyverse/i.test(redirect)) return 'studyverse';
  return 'moneyviel';
}
const esc = (s: string) => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));

const COPY: Record<string, { subject: string; head: string; body: string; btn: string }> = {
  signup: { subject: 'Confirm your {app} account', head: 'Welcome to {app}! 👋', body: 'Tap the button to confirm your email and finish creating your account.', btn: 'Confirm my email' },
  recovery: { subject: 'Reset your {app} password', head: 'Reset your password', body: 'We got a request to reset your password. Tap the button to choose a new one. If you did not ask for this, you can ignore this email.', btn: 'Choose a new password' },
  magiclink: { subject: 'Your {app} sign-in link', head: 'Sign in to {app}', body: 'Tap the button to sign in. The link works once and expires soon.', btn: 'Sign me in' },
  invite: { subject: "You're invited to {app}", head: "You're invited! 🎉", body: 'You have been invited to join {app}. Tap the button to accept and set up your account.', btn: 'Accept invite' },
  email_change: { subject: 'Confirm your new email for {app}', head: 'Confirm your new email', body: 'Tap the button to confirm this email address for your {app} account.', btn: 'Confirm email change' },
  email_change_current: { subject: 'Confirm the email change on your {app} account', head: 'Is this change yours?', body: 'Someone asked to change the email on your {app} account. Tap the button to confirm. If this was not you, please change your password.', btn: 'Confirm change' },
  reauthentication: { subject: 'Your {app} verification code', head: 'Your verification code', body: 'Enter this code in {app} to continue.', btn: '' },
};

function html(b: Brand, c: typeof COPY[string], link: string, code: string) {
  const f = (s: string) => esc(s.replace(/\{app\}/g, b.name));
  return `<!doctype html><html><body style="margin:0;background:#f4f4f5;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#fff;border-radius:14px;overflow:hidden">
<tr><td style="background:${b.color};color:#fff;padding:18px 24px;font-size:20px;font-weight:bold">${esc(b.name)}${b.tag ? `<div style="font-size:13px;font-weight:normal;opacity:.85;margin-top:2px">${esc(b.tag)}</div>` : ''}</td></tr>
<tr><td style="padding:24px">
<h1 style="font-size:21px;margin:0 0 12px">${f(c.head)}</h1>
<p style="font-size:16px;line-height:1.5;margin:0 0 20px">${f(c.body)}</p>
${link ? `<p style="margin:0 0 20px"><a href="${esc(link)}" style="display:inline-block;background:${b.color};color:#fff;text-decoration:none;font-weight:bold;font-size:16px;padding:14px 22px;border-radius:10px">${f(c.btn)}</a></p>
<p style="font-size:13px;color:#555;line-height:1.5;margin:0 0 12px">Button not working? Copy this link into your browser:<br><a href="${esc(link)}" style="color:${b.color};word-break:break-all">${esc(link)}</a></p>` : ''}
${code ? `<p style="font-size:14px;color:#333;margin:0 0 6px">${link ? 'Or enter this code:' : ''}</p><p style="font-size:28px;letter-spacing:6px;font-weight:bold;margin:0 0 16px">${esc(code)}</p>` : ''}
<p style="font-size:13px;color:#777;margin:16px 0 0">Need help? Reply to this email or write to ${esc(b.from)}.</p>
</td></tr></table>
<p style="font-size:12px;color:#888;margin:14px 0 0">${esc(b.name)} · Pune, India · <a href="${esc(b.site)}" style="color:#888">${esc(b.site.replace(/^https:\/\//, '').replace(/\/$/, ''))}</a></p>
</td></tr></table></body></html>`;
}

async function brevo(b: Brand, to: string, subject: string, body: string, text: string) {
  const r = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({ sender: { name: b.name, email: b.from }, replyTo: { email: b.from, name: b.name }, to: [{ email: to }], subject, htmlContent: body, textContent: text, tags: ['auth'] }) });
  if (!r.ok) throw new Error(`brevo ${r.status} ${(await r.text()).slice(0, 200)}`);
}

async function sendOne(app: string, to: string, type: string, link: string, code: string) {
  const c = COPY[type] || COPY.magiclink, b = BRANDS[app];
  const subject = c.subject.replace(/\{app\}/g, b.name);
  const text = `${c.head.replace(/\{app\}/g, b.name)}\n\n${c.body.replace(/\{app\}/g, b.name)}\n\n${link ? link + '\n' : ''}${code ? 'Code: ' + code + '\n' : ''}`;
  try { await brevo(b, to, subject, html(b, c, link, code), text); }
  catch (e) {
    console.log('send failed for', app, String(e));
    if (b.from === BRANDS.moneyviel.from) throw e;
    const fb = { ...b, from: BRANDS.moneyviel.from };   // keep the app's look, send from the always-verified address
    await brevo(fb, to, subject, html(fb, c, link, code), text);
  }
}

const out = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'Content-Type': 'application/json' } });

Deno.serve(async (req) => {
  if (req.method !== 'POST') return out({ error: 'POST only' }, 405);
  const raw = await req.text();
  let data: any;
  try { data = new Webhook(HOOK).verify(raw, Object.fromEntries(req.headers)); }
  catch (e) { console.log('bad signature', String(e)); return out({ error: { http_code: 401, message: 'invalid signature' } }, 401); }
  try {
    if (!BREVO) throw new Error('BREVO_API_KEY missing');
    const { user, email_data: d } = data;
    const type = String(d.email_action_type || '');
    const redirect = String(d.redirect_to || d.site_url || '');
    const app = appOf(user, redirect);
    const link = (hash: string, t: string) => hash ? `${SB}/auth/v1/verify?token=${encodeURIComponent(hash)}&type=${encodeURIComponent(t)}&redirect_to=${encodeURIComponent(redirect)}` : '';
    if (type === 'email_change') {
      // secure email change (Supabase pairing): token_hash_new/token_new → current address, token_hash/token → new address
      if (d.token_hash_new && user.email) await sendOne(app, user.email, 'email_change_current', link(d.token_hash_new, 'email_change'), d.token_new || '');
      const to = user.new_email || user.email;
      if (d.token_hash && to) await sendOne(app, to, 'email_change', link(d.token_hash, 'email_change'), d.token || '');
    } else if (type === 'reauthentication') {
      await sendOne(app, user.email, type, '', d.token || '');
    } else {
      await sendOne(app, user.email, type, link(d.token_hash, type === 'signup' ? 'signup' : type), '');
    }
    console.log('sent', type, app);
    return out({});
  } catch (e) {
    console.log('error', String(e));
    return out({ error: { http_code: 500, message: 'Could not send the email. Please try again in a minute.' } }, 500);
  }
});
