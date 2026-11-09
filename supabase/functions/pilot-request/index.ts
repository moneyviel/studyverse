// "pilot-request": the public "Request a free pilot" form on /pricing/ → email to support@moneyviel.com.
// POST { name, school, city, phone, email, students, website }   (website = honeypot: must be empty; bots fill it)
// No sign-in. Rate limits in SQL (studyverse._pilot_request): 3 per IP per hour (IP stored only as a salted SHA-256), 100 a day.
// Deploy with --no-verify-jwt (anonymous form). Secrets: BREVO_API_KEY, optional PILOT_SALT (+ automatic ones).
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const BREVO = Deno.env.get('BREVO_API_KEY') || '';
const SALT = Deno.env.get('PILOT_SALT') || 'studyverse-pilot';
const OWNER = 'support@moneyviel.com';
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const str = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f<>]/g, ' ').trim().slice(0, n);
const H = () => { const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }; if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`; return h; };
async function sha(t: string) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ ok: false, msg: 'Use POST.' }, 405);
  try {
    const b = await req.json().catch(() => ({}));
    if (str(b.website, 200)) return json({ ok: true });                 // honeypot filled: pretend success, do nothing
    const f = { name: str(b.name, 80), school: str(b.school, 120), city: str(b.city, 60), phone: str(b.phone, 20), email: str(b.email, 120).toLowerCase(), students: Math.floor(Number(b.students) || 0) };
    if (f.name.length < 2 || f.school.length < 2 || f.city.length < 2) return json({ ok: false, msg: 'Please fill in your name, school and city.' });
    if (!/^[+0-9][0-9 -]{7,18}$/.test(f.phone)) return json({ ok: false, msg: 'Please enter a phone number we can call.' });
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email)) return json({ ok: false, msg: 'Please enter a valid email.' });
    if (!(f.students >= 1 && f.students <= 1000000)) return json({ ok: false, msg: 'Please enter the number of students.' });
    const ip = (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || req.headers.get('cf-connecting-ip') || 'unknown';
    const r = await fetch(`${URL_}/rest/v1/rpc/_pilot_request`, { method: 'POST', headers: H(), body: JSON.stringify({ p: f, p_ip: await sha(SALT + ':' + ip) }) });
    const res = r.ok ? await r.json() : null;
    if (!res?.ok) return json({ ok: false, msg: res?.msg || 'Please try again in a few minutes.' }, res?.code === 'limit' ? 429 : 200);
    if (!BREVO) return json({ ok: true, mailed: false });
    const html = `<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;color:#111"><h2 style="color:#5B0F1B">Free pilot request</h2>
<p><b>${esc(f.school)}</b>, ${esc(f.city)}<br>Contact: ${esc(f.name)} · ${esc(f.phone)} · ${esc(f.email)}<br>Students: ${f.students}</p>
<p>Create the institution and grant the 30-day pilot in the app: Me → 🏫 Schools (owner).</p></body></html>`;
    const s = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': BREVO, 'Content-Type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({ sender: { name: 'StudyVerse Schools', email: OWNER }, replyTo: { email: f.email, name: f.name }, to: [{ email: OWNER }],
        subject: `Free pilot request: ${f.school}, ${f.city} (${f.students} students)`, htmlContent: html, tags: ['pilot-request'] }) });
    if (!s.ok) console.log('brevo', s.status, (await s.text()).slice(0, 200));
    return json({ ok: true, mailed: s.ok });
  } catch (e) {
    console.log(String(e)); return json({ ok: false, msg: 'Something went wrong. Please try again.' }, 500);
  }
});
