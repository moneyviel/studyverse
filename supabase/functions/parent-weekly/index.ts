// "parent-weekly": one short weekly email per StudyVerse parent (Brevo, from support@moneyviel.com).
// Runs daily from pg_cron (header x-cron-key = studyverse.job_config.cron_key). Each run emails parents whose last email
// was 7+ days ago (oldest first, max PER_RUN), so sending spreads itself across the week and stays inside Brevo's free 300/day.
// GET ?u=<unsubscribe id> switches the email off (link at the bottom of every email).
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const PER_RUN = Number(Deno.env.get('WEEKLY_PER_RUN') || 250);
const APP = 'https://study.moneyviel.com/';
const FN = `${URL_}/functions/v1/parent-weekly`;

const H = (extra: Record<string, string> = {}) => {
  const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse', ...extra };
  if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`;
  return h;
};
const rpc = async (name: string, body: unknown) => {
  const r = await fetch(`${URL_}/rest/v1/rpc/${name}`, { method: 'POST', headers: H(), body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`${name} ${r.status} ${(await r.text()).slice(0, 200)}`);
  const t = await r.text(); return t ? JSON.parse(t) : null;
};
const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));

/* ---- the same day maths as js/parent.js (keys are India dates 'YYYY-MM-DD') ---- */
const IST = 5.5 * 3600e3, DAY = 864e5;
const key = (t: number) => new Date(t + IST).toISOString().slice(0, 10);
const days = (fromAgo: number, n: number) => { const out: string[] = []; const now = Date.now(); for (let i = fromAgo + n - 1; i >= fromAgo; i--) out.push(key(now - i * DAY)); return out; };
function minutesOn(s: any, d: string) {
  if (!s) return 0;
  if (s.time && s.time[d] != null) return +s.time[d] || 0;
  const a = s.ins?.day?.[d] ? (s.ins.day[d].s || 0) / 60 : 0, b = s.ca?.time?.[d] ? s.ca.time[d] / 60 : 0;
  return Math.max(a, b);
}
function answers(s: any, ds: string[]) {
  const set = new Set(ds); let a = 0, r = 0;
  for (const d of ds) { const i = s?.ins?.day?.[d]; if (i) { a += i.a || 0; r += i.r || 0; } }
  const ml = Array.isArray(s?.ca?.mlog) ? s.ca.mlog : [];
  for (const x of ml) { if (set.has(key(x[0] * 6e4))) { a++; if (x[2]) r++; } }
  return { a, r };
}
const fmtMin = (m: number) => { m = Math.round(m); return m >= 60 ? `${Math.floor(m / 60)} h ${m % 60} min` : `${m} min`; };
const pct = (x: { a: number; r: number }) => x.a ? Math.round(x.r / x.a * 100) : null;

function summary(c: any) {
  const s = c.state || null, name = c.name || s?.profile?.name || 'Your child';
  const W = days(0, 7), P = days(7, 7);
  const mW = W.reduce((t, d) => t + minutesOn(s, d), 0), mP = P.reduce((t, d) => t + minutesOn(s, d), 0);
  const act = W.filter(d => minutesOn(s, d) >= 1).length;
  const aW = answers(s, W), aP = answers(s, P), pW = pct(aW), pP = pct(aP);
  const goal = +(c.controls?.goal || 0), goalDays = goal ? W.filter(d => minutesOn(s, d) >= goal).length : 0;
  let quiet = 0; for (let i = 0; i < 30; i++) { if (minutesOn(s, key(Date.now() - i * DAY)) >= 1) break; quiet++; }
  const lines: string[] = [];
  lines.push(`Studied <b>${fmtMin(mW)}</b> on ${act} of 7 days${mP ? ` (last week ${fmtMin(mP)})` : ''}.`);
  if (aW.a) lines.push(`Answered <b>${aW.a}</b> questions · <b>${pW}%</b> correct${pP != null && aP.a ? ` (last week ${pP}%)` : ''}.`);
  if (goal) lines.push(`Daily goal of ${goal} min met on <b>${goalDays} of 7</b> days.`);
  const alerts: string[] = [];
  if (!s) alerts.push('No progress synced yet — ask them to sign in to StudyVerse on their phone.');
  else if (quiet >= 3) alerts.push(`No study for ${quiet >= 30 ? '30+' : quiet} days.`);
  if (pW != null && pP != null && aP.a >= 10 && pW < pP - 15) alerts.push(`Accuracy dropped ${pP - pW} points — worth a chat.`);
  const text = `${name}: ${fmtMin(mW)} this week, ${act}/7 days${aW.a ? `, ${aW.a} questions, ${pW}% correct` : ''}${alerts.length ? ' — ' + alerts.join(' ') : ''}`;
  return { name, lines, alerts, text, mW };
}

function email(kids: ReturnType<typeof summary>[], unsub: string) {
  const range = `${new Date(Date.now() - 6 * DAY + IST).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' })} – ${new Date(Date.now() + IST).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' })}`;
  const blocks = kids.map(k => `<tr><td style="padding:14px 0;border-top:1px solid #eee">
    <div style="font-size:17px;font-weight:bold;margin:0 0 6px">${esc(k.name)}</div>
    ${k.lines.map(l => `<div style="font-size:15px;line-height:1.5">${l}</div>`).join('')}
    ${k.alerts.map(a => `<div style="font-size:14px;line-height:1.5;color:#9a1b1b;margin-top:4px">⚠️ ${esc(a)}</div>`).join('')}</td></tr>`).join('');
  const off = `${FN}?u=${encodeURIComponent(unsub)}`;
  const html = `<!doctype html><html><body style="margin:0;background:#f4f4f5;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#fff;border-radius:14px;overflow:hidden">
<tr><td style="background:#5B0F1B;color:#fff;padding:18px 24px;font-size:20px;font-weight:bold">StudyVerse<div style="font-size:13px;font-weight:normal;opacity:.85;margin-top:2px">Weekly summary · ${esc(range)}</div></td></tr>
<tr><td style="padding:8px 24px 22px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${blocks}</table>
<p style="margin:18px 0 6px"><a href="${APP}?hub=1" style="display:inline-block;background:#5B0F1B;color:#fff;text-decoration:none;font-weight:bold;font-size:16px;padding:14px 22px;border-radius:10px">Open full report</a></p>
<p style="font-size:13px;color:#666;margin:6px 0 0">Strengths, weak areas, goals and dinner-table questions are in Parent Hub.</p>
</td></tr></table>
<p style="font-size:12px;color:#888;margin:14px 0 0">StudyVerse · Pune, India · <a href="${off}" style="color:#888">Stop weekly emails</a></p>
</td></tr></table></body></html>`;
  const text = `StudyVerse weekly summary (${range})\n\n${kids.map(k => k.text).join('\n')}\n\nFull report: ${APP}?hub=1\nStop weekly emails: ${off}\n`;
  return { html, text };
}

async function send(to: string, subject: string, html: string, text: string) {
  const r = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({ sender: { name: 'StudyVerse', email: 'support@moneyviel.com' }, replyTo: { email: 'support@moneyviel.com' }, to: [{ email: to }], subject, htmlContent: html, textContent: text, tags: ['parent-weekly'] }) });
  if (!r.ok) throw Object.assign(new Error(`brevo ${r.status} ${(await r.text()).slice(0, 200)}`), { status: r.status });
}

const page = (msg: string) => new Response(`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>StudyVerse</title><body style="font-family:Arial,sans-serif;max-width:480px;margin:40px auto;padding:0 16px;text-align:center"><h1 style="color:#5B0F1B">StudyVerse</h1><p style="font-size:17px">${esc(msg)}</p><p><a href="${APP}">Open StudyVerse</a></p></body>`, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });

Deno.serve(async (req) => {
  const u = new URL(req.url);
  if (req.method === 'GET') {
    const id = u.searchParams.get('u') || '';
    if (!/^[0-9a-f-]{36}$/i.test(id)) return page('This link is not valid.');
    try { await rpc('weekly_unsub', { p_unsub: id }); } catch (e) { console.log(String(e)); return page('Something went wrong. Please try again later.'); }
    return page('Done — you will not get weekly emails any more. You can switch them back on in Parent Hub.');
  }
  // cron only
  const k = req.headers.get('x-cron-key') || '';
  const cfg = await fetch(`${URL_}/rest/v1/job_config?select=cron_key&id=eq.1`, { headers: H() }).then(r => r.json()).catch(() => []);
  if (!k || !Array.isArray(cfg) || cfg[0]?.cron_key !== k) return new Response(JSON.stringify({ error: 'forbidden' }), { status: 403 });
  if (!BREVO) return new Response(JSON.stringify({ error: 'BREVO_API_KEY missing' }), { status: 500 });
  const body = await req.json().catch(() => ({}));
  const limit = Math.max(1, Math.min(PER_RUN, Number(body.limit) || PER_RUN));
  const due: any[] = (await rpc('weekly_due', { p_limit: limit })) || [];
  let sent = 0, failed = 0;
  for (const p of due) {
    const kids = (Array.isArray(p.children) ? p.children : []).map(summary);
    if (!kids.length) continue;
    const top = kids[0];
    const subject = kids.length === 1 ? `${top.name}'s week: ${fmtMin(top.mW)} of study` : `Your children's week on StudyVerse`;
    const { html, text } = email(kids, p.unsub);
    try { await send(p.email, subject, html, text); await rpc('weekly_mark', { p_parent: p.parent_id, p_unsub: p.unsub }); sent++; }
    catch (e: any) { failed++; console.log('send failed', String(e)); if (e.status === 429 || e.status === 402) break; }   // daily limit or credits: stop, the rest go tomorrow
  }
  console.log('parent-weekly', { due: due.length, sent, failed });
  return new Response(JSON.stringify({ due: due.length, sent, failed }), { headers: { 'Content-Type': 'application/json' } });
});
