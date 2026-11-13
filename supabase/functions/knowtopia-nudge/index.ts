// "knowtopia-nudge": one friendly phone reminder a day for Knowtopia students (web push).
// Called by pg_cron "studyverse-nudge" at 17:31 India time (after school, before night), header x-cron-key = studyverse.job_config.cron_key.
// Who gets one: rpc studyverse.push_due (one phone per student, not reminded today, parent allows it, did not study today;
// students quiet for 7+ days at most once a week). Keys (VAPID) live in studyverse.job_config — no settings needed here.
// Test: POST {"test_user":"<uuid>"} with the same cron key sends one reminder to that student's phones right now.
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const APP = 'https://knowtopia.in/?from=reminder';

const H = () => { const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }; if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`; return h; };
const rpc = async (name: string, body: unknown) => {
  const r = await fetch(`${URL_}/rest/v1/rpc/${name}`, { method: 'POST', headers: H(), body: JSON.stringify(body) });
  const t = await r.text(); if (!r.ok) throw new Error(`${name} ${r.status} ${t.slice(0, 200)}`); return t ? JSON.parse(t) : null;
};

/* ---- web push (RFC 8291 aes128gcm + VAPID), no libraries ---- */
const enc = new TextEncoder();
const b64u = (buf: ArrayBuffer | Uint8Array) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64u = (s: string) => { const p = '='.repeat((4 - (s.length % 4)) % 4); const r = atob((s + p).replace(/-/g, '+').replace(/_/g, '/')); return Uint8Array.from(r, c => c.charCodeAt(0)); };
const concat = (...parts: Uint8Array[]) => { const o = new Uint8Array(parts.reduce((a, p) => a + p.length, 0)); let i = 0; for (const p of parts) { o.set(p, i); i += p.length; } return o; };
async function hkdf(salt: Uint8Array, ikm: Uint8Array, info: Uint8Array, len: number) {
  const key = await crypto.subtle.importKey('raw', ikm, 'HKDF', false, ['deriveBits']);
  return new Uint8Array(await crypto.subtle.deriveBits({ name: 'HKDF', hash: 'SHA-256', salt, info }, key, len * 8));
}
async function vapid(endpoint: string, pub: string, priv: string) {
  const p = unb64u(pub);
  const key = await crypto.subtle.importKey('jwk', { kty: 'EC', crv: 'P-256', d: priv, x: b64u(p.slice(1, 33)), y: b64u(p.slice(33, 65)), ext: true }, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
  const head = b64u(enc.encode(JSON.stringify({ typ: 'JWT', alg: 'ES256' })));
  const body = b64u(enc.encode(JSON.stringify({ aud: new URL(endpoint).origin, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: 'mailto:support@moneyviel.com' })));
  const sig = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, key, enc.encode(`${head}.${body}`));
  return `vapid t=${head}.${body}.${b64u(sig)}, k=${pub}`;
}
async function encrypt(p256dh: string, authSecret: string, payload: string) {
  const ua = unb64u(p256dh), auth = unb64u(authSecret);
  const local = await crypto.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']) as CryptoKeyPair;
  const as = new Uint8Array(await crypto.subtle.exportKey('raw', local.publicKey));
  const uaKey = await crypto.subtle.importKey('raw', ua, { name: 'ECDH', namedCurve: 'P-256' }, false, []);
  const shared = new Uint8Array(await crypto.subtle.deriveBits({ name: 'ECDH', public: uaKey }, local.privateKey, 256));
  const ikm = await hkdf(auth, shared, concat(enc.encode('WebPush: info\0'), ua, as), 32);
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const cek = await hkdf(salt, ikm, enc.encode('Content-Encoding: aes128gcm\0'), 16);
  const nonce = await hkdf(salt, ikm, enc.encode('Content-Encoding: nonce\0'), 12);
  const aes = await crypto.subtle.importKey('raw', cek, 'AES-GCM', false, ['encrypt']);
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce }, aes, concat(enc.encode(payload), new Uint8Array([2]))));
  return concat(salt, new Uint8Array([0, 0, 16, 0]), new Uint8Array([as.length]), as, ct);
}
async function push(sub: any, msg: unknown, cfg: any) {
  const r = await fetch(sub.endpoint, { method: 'POST', body: await encrypt(sub.p256dh, sub.auth, JSON.stringify(msg)),
    headers: { Authorization: await vapid(sub.endpoint, cfg.public, cfg.private), 'Content-Encoding': 'aes128gcm', 'Content-Type': 'application/octet-stream', TTL: '14400', Urgency: 'high' } });
  return r.status;
}

/* ---- the message: streak first, then Mind Gym, then a gentle "your next topic" ---- */
const yesterdayUtc = () => new Date(Date.now() - 864e5).toISOString().slice(0, 10);
function message(r: any) {
  const w = r.ca ? 'unit' : 'topic';
  const first = String(r.name || '').trim().split(/\s+/)[0] || '';
  const alive = r.streak_last === yesterdayUtc() && r.streak_n >= 1;
  const n = r.streak_n, need = r.need;
  if (alive && need === 1) return { title: `🔥 ${n}-day streak + 🧠 1 ${w} to go!`, body: `One ${w} today keeps your streak and unlocks new Mind Gym challenges.` };
  if (alive) return { title: `🔥 Keep your ${n}-day streak going`, body: `One short ${w} today keeps it alive${first ? `, ${first}` : ''}.` };
  if (need === 1) return { title: `🎯 Just 1 ${w} away!`, body: `Finish one more ${w} to unlock new Mind Gym challenges.` };
  if (need === 2) return { title: '🧠 New Mind Gym challenges are close', body: `2 more ${w}s and fresh puzzles open up.` };
  return { title: `📚 Your next ${w} is waiting`, body: `Ten focused minutes today${first ? `, ${first}` : ''}? You've got this.` };
}

Deno.serve(async (req) => {
  try {
    const cfg = await rpc('push_cfg', { p_key: req.headers.get('x-cron-key') || '' });
    if (!cfg || !cfg.private) return new Response(JSON.stringify({ error: 'forbidden' }), { status: 403 });
    const body = await req.json().catch(() => ({}));
    let list: any[];
    if (body.test_user && /^[0-9a-f-]{36}$/i.test(body.test_user)) {
      const subs = await fetch(`${URL_}/rest/v1/push_subs?select=endpoint,p256dh,auth,user_id,need&user_id=eq.${body.test_user}`, { headers: H() }).then(r => r.json());
      list = (Array.isArray(subs) ? subs : []).map((s: any) => ({ ...s, name: '', ca: false, streak_n: 0, streak_last: '', test: true }));
    } else list = (await rpc('push_due', { p_limit: 5000 })) || [];
    let sent = 0, failed = 0, gone = 0;
    for (let i = 0; i < list.length; i += 20) {
      await Promise.all(list.slice(i, i + 20).map(async (r) => {
        const m = r.test ? { title: '🔔 Knowtopia reminders are on', body: 'This is a test. You will get at most one reminder a day, never at night or in school hours.' } : message(r);
        let st = 0; try { st = await push(r, { ...m, link: APP, tag: r.test ? `knowtopia-test-${Date.now()}` : 'knowtopia-daily' }, cfg); } catch (e) { console.log('push error', String(e)); }
        const ok = st >= 200 && st < 300, isGone = st === 404 || st === 410;
        if (ok) sent++; else if (isGone) gone++; else failed++;
        if (!r.test || isGone) await rpc('push_result', { p_endpoint: r.endpoint, p_user: r.user_id, p_ok: ok, p_gone: isGone }).catch(e => console.log(String(e)));
      }));
    }
    console.log('knowtopia-nudge', { due: list.length, sent, failed, gone });
    return new Response(JSON.stringify({ due: list.length, sent, failed, gone }), { headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    console.log('knowtopia-nudge failed', String(e));
    return new Response(JSON.stringify({ error: String(e) }), { status: 500 });
  }
});
