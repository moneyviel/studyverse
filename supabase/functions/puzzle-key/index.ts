// "puzzle-key": starts a Puzzle Race with an answer key computed ON THE SERVER (never by a player's phone).
// POST { code } with the HOST's sign-in token → { ok, msg?, code? } (the result of studyverse.puzzle_start).
//   1. who is calling (auth/v1/user) → studyverse.puzzle_prepare(code, user)   [service role: host? lobby? ready? puzzle?]
//   2. rebuild the puzzle from the stored spec with js/puzzles-core.js → PuzzleCore.solutionOf(spec, content), where
//      content = the app's content JSON listed by PuzzleCore.contentPathOf(spec) (fetched from https://study.moneyviel.com/,
//      content/*.json only — see logic.mjs)
//   3. studyverse.puzzle_set_key(code, user, spec hash, answer)                 [service role → room_keys, unreadable]
//   4. studyverse.puzzle_start(code) AS THE HOST (same start rules as every game)
// DEPLOY: the engine is BUNDLED, not fetched (no remote code runs next to the service-role key). Copy it in first:
//     cp js/puzzles-core.js js/ca-keys-data.js supabase/functions/puzzle-key/ && supabase functions deploy puzzle-key
// Re-deploy every time js/puzzles-core.js or js/ca-keys-data.js changes (same release as the app), or keys may not
// match what the phones build — every check would then say "not solved". (If PuzzleCore ever exports VERSION, specs
// with another "v" are refused with a clear message instead.)
/* eslint-disable */
// ENGINE (pinned): js/puzzles-core.js + js/ca-keys-data.js are loaded from GitHub at ONE fixed commit and run only if
// their SHA-256 matches the hashes below (content-addressed: nobody can swap the code). Update PIN in the same release
// whenever either file changes (tools: sha256sum js/puzzles-core.js js/ca-keys-data.js).
const PIN = { commit: '__COMMIT__', files: { 'js/puzzles-core.js': '__H1__', 'js/ca-keys-data.js': '__H2__' } as Record<string, string> };
let ENGINE: Promise<void> | null = null;
const hex = (b: ArrayBuffer) => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
function loadEngine() {
  if (!ENGINE) ENGINE = (async () => {
    for (const [path, want] of Object.entries(PIN.files)) {
      const r = await fetch(`https://raw.githubusercontent.com/moneyviel/studyverse/${PIN.commit}/${path}`, { signal: AbortSignal.timeout(10000) });
      if (!r.ok) throw new Error('engine fetch ' + r.status);
      const t = await r.text();
      if (hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t))) !== want) throw new Error('engine hash mismatch: ' + path);
      (0, eval)(t);                                // indirect eval → global scope: sets globalThis.PuzzleCore / CaKeysData
    }
  })().catch(e => { ENGINE = null; throw e; });
  return ENGINE;
}
import { computeAnswer, KeyError, SITE } from './logic.mjs';

const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const SVC = () => { const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }; if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`; return h; };
const rpc = async (fn: string, body: unknown, headers: Record<string, string>) => {
  const r = await fetch(`${URL_}/rest/v1/rpc/${fn}`, { method: 'POST', headers, body: JSON.stringify(body) });
  const t = await r.text(); let j: any = null; try { j = t ? JSON.parse(t) : null; } catch (_) { /* ignore */ }
  if (!r.ok) { console.log(fn, r.status, t.slice(0, 200)); return null; }
  return Array.isArray(j) ? j[0] : j;
};
// content JSON from the app's own site; small in-memory cache for warm instances
const cache = new Map<string, { at: number; v: unknown }>();
async function getJSON(path: string) {
  const c = cache.get(path); if (c && Date.now() - c.at < 10 * 60e3) return c.v;
  const r = await fetch(SITE + path, { signal: AbortSignal.timeout(8000) });
  if (!r.ok) throw new KeyError('content', 'The chapter for this puzzle could not be loaded.');
  const t = await r.text(); if (t.length > 5e6) throw new KeyError('content', 'The chapter for this puzzle is too big.');
  const v = JSON.parse(t); if (cache.size > 200) cache.clear(); cache.set(path, { at: Date.now(), v }); return v;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const auth = req.headers.get('Authorization') || '', apikey = req.headers.get('apikey') || SRK;
    const ur = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey, Authorization: auth } });
    const user = ur.ok ? await ur.json() : null;
    if (!user?.id) return json({ ok: false, msg: 'Please sign in again.' }, 401);
    const b = await req.json().catch(() => ({}));
    const code = String(b.code || '').trim().toUpperCase();
    if (!/^[A-Z]{6}$/.test(code)) return json({ ok: false, msg: 'Room not found.' });
    const prep = await rpc('puzzle_prepare', { p_code: code, p_user: user.id }, SVC());
    if (!prep?.ok) return json(prep || { ok: false, msg: 'Could not reach the server. Please try again.' });
    let answer: unknown;
    try { await loadEngine(); answer = await computeAnswer((globalThis as any).PuzzleCore, prep.spec, getJSON, (globalThis as any).CaKeysData?.ITEMS || []); }
    catch (e) { console.log('key', prep.kind, String(e)); return json({ ok: false, code: (e as any).code || 'engine', msg: e instanceof KeyError ? e.message : 'This puzzle could not be prepared. Please pick another one.' }); }
    const set = await rpc('puzzle_set_key', { p_code: code, p_user: user.id, p_hash: prep.h, p_answer: answer }, SVC());
    if (!set?.ok) return json(set || { ok: false, msg: 'Could not save the puzzle. Please try again.' });
    const st = await rpc('puzzle_start', { p_code: code }, { apikey, Authorization: auth, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' });
    return json(st || { ok: false, msg: 'Could not start the race. Please try again.' });
  } catch (e) {
    console.log(String(e)); return json({ ok: false, msg: 'Something went wrong. Please try again.' }, 500);
  }
});
