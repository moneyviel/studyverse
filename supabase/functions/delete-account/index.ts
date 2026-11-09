// StudyVerse "Delete my account" (Google Play: in-app account deletion). Deployed as "delete-account" in project
// moneyviel-apps (keep "Verify JWT" ON). Called from the app: Me / CA Profile → Your account → Delete my account
// (and Parent Hub → Your account) after a two-step confirmation where the person types DELETE.
// POST { confirm: "DELETE" } with the user's access token → { ok: true } | { error }
//   1. The token is checked with Supabase Auth (/auth/v1/user) — only the signed-in person can delete their own account.
//   2. rpc studyverse._pr_delete_user_data(p_user) (service role only, supabase/migrations/20261113_play_ready.sql) cleans
//      the rows that are not removed by a foreign-key cascade: unlinks parents/children, removes room answers and email
//      invites addressed to this email, and KEEPS payment rows for tax records with user_id set to NULL.
//      Owner (admin) accounts are refused.
//   3. The auth user is deleted with the Admin API; every other studyverse row cascades (progress, profile, squad,
//      friends, cheers, parent links and controls, consents, course access, school membership, game rooms…).
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });
const srv = (extra: Record<string, string> = {}) => {
  const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', ...extra };
  if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`;
  return h;
};

async function who(req: Request) {
  const auth = req.headers.get('Authorization') || '';
  if (!/^Bearer\s+\S+/.test(auth)) return null;
  const r = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: auth } });
  if (!r.ok) return null; const u = await r.json(); return u && u.id ? u : null;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Use POST.' }, 405);
  try {
    const user = await who(req);
    if (!user) return json({ error: 'Please sign in again.' }, 401);
    const b = await req.json().catch(() => ({}));
    if (String(b?.confirm || '') !== 'DELETE') return json({ error: 'Please type DELETE to confirm.' }, 400);

    // 1. clean-up that a cascade does not do (and the owner guard)
    const p = await fetch(`${URL_}/rest/v1/rpc/_pr_delete_user_data`, { method: 'POST', headers: srv({ 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }), body: JSON.stringify({ p_user: user.id }) });
    const pj = await p.json().catch(() => null);
    if (!p.ok || !pj) { console.log('delete-account prepare failed', p.status, JSON.stringify(pj).slice(0, 200)); return json({ error: 'Could not delete your account right now. Please try again, or write to support@moneyviel.com.' }, 500); }
    if (pj.ok === false) return json({ error: pj.msg || 'This account cannot be deleted from the app.' }, 400);

    // 2. wipe every StudyVerse row of this person (the project is SHARED with other MoneyViel apps — see
    //    supabase/migrations/20261113b_delete_scope.sql), then close the login ONLY if no other app uses it.
    const rpc = (fn: string) => fetch(`${URL_}/rest/v1/rpc/${fn}`, { method: 'POST', headers: srv({ 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' }), body: JSON.stringify({ p_user: user.id }) });
    const w = await rpc('_pr_wipe_studyverse'); const wj = await w.json().catch(() => null);
    if (!w.ok || !wj || wj.ok === false) { console.log('delete-account wipe failed', w.status, JSON.stringify(wj).slice(0, 200)); return json({ error: 'Could not delete your account right now. Please try again, or write to support@moneyviel.com.' }, 500); }
    const e = await rpc('_pr_user_elsewhere'); const shared = e.ok ? (await e.json().catch(() => true)) === true : true;   // unsure → keep the login
    if (shared) {
      console.log('delete-account studyverse data deleted; login kept (used by another MoneyViel app)', user.id);
      return json({ ok: true, shared: true, payments_kept: pj.payments_kept || 0 });
    }
    const d = await fetch(`${URL_}/auth/v1/admin/users/${encodeURIComponent(user.id)}`, { method: 'DELETE', headers: srv() });
    if (!d.ok) {
      const t = await d.text().catch(() => '');
      console.log('delete-account auth delete failed', d.status, t.slice(0, 200));
      return json({ error: 'Your data was cleaned up but the account could not be closed. Please write to support@moneyviel.com from this email and we will finish it within 7 days.' }, 500);
    }
    console.log('delete-account done', user.id, 'payments kept', pj.payments_kept || 0);
    return json({ ok: true, payments_kept: pj.payments_kept || 0 });
  } catch (e) {
    return json({ error: 'Something went wrong. Please try again.', detail: String((e as Error).message || e).slice(0, 200) }, 500);
  }
});
