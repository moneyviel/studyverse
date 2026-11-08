// StudyVerse "read my handwriting": turns photos of a written answer into text, so the app's own checker can mark it.
// Deployed as "studyverse-read" in project moneyviel-apps. Uses Google Gemini (free tier) — secret GEMINI_API_KEY
// (optional GEMINI_MODEL; falls back through current free Flash models). It only transcribes; marking is done by the app (js/ca-check.js).
// POST { images: [base64 JPEG, ...] (max 4 pages), question: "..." } → { text } | { error }
// Daily limit per student: READ_PAGES_PER_DAY pages (studyverse.take_read_quota).
/* eslint-disable */
const URL_ = Deno.env.get('SUPABASE_URL')!;
const SRK = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const GKEY = Deno.env.get('GEMINI_API_KEY') || '';
// [model, seconds to wait]: the best reader first; the fast "lite" model steps in when it is busy or slow
const MODELS: [string, number][] = [...(Deno.env.get('GEMINI_MODEL') ? [[Deno.env.get('GEMINI_MODEL')!, 30] as [string, number]] : []), ['gemini-flash-latest', 20], ['gemini-flash-lite-latest', 25], ['gemini-3.8-flash', 20]];
const LIMIT = Number(Deno.env.get('READ_PAGES_PER_DAY') || 20);
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } });

async function who(req: Request) {
  const r = await fetch(`${URL_}/auth/v1/user`, { headers: { apikey: req.headers.get('apikey') || SRK, Authorization: req.headers.get('Authorization') || '' } });
  if (!r.ok) return null; const u = await r.json(); return u && u.id ? u : null;
}
async function quota(user: string, pages: number) {
  const h: Record<string, string> = { apikey: SRK, 'Content-Type': 'application/json', 'Accept-Profile': 'studyverse', 'Content-Profile': 'studyverse' };
  if (SRK.startsWith('eyJ')) h.Authorization = `Bearer ${SRK}`;
  const r = await fetch(`${URL_}/rest/v1/rpc/take_read_quota`, { method: 'POST', headers: h, body: JSON.stringify({ p_user: user, p_pages: pages, p_limit: LIMIT }) });
  return r.ok && (await r.json()) === true;
}

const PROMPT = (q: string) => `You are reading a student's handwritten exam answer from photos (Indian CA Foundation exam).
Question (for context only): ${q.slice(0, 1500)}

Transcribe exactly what the student wrote, page by page, in reading order.
- Copy words, numbers, amounts, dates, section numbers and symbols (Dr, Cr, ₹, %, →) exactly as written. Do NOT correct spelling, grammar, facts or calculations, and do NOT add anything that is not written.
- Keep the student's line breaks and numbering. For a table, write one row per line with " | " between columns.
- Ignore struck-out text. If a word cannot be read, write [?].
- Output only the transcription, no comments.`;

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const user = await who(req);
    if (!user) return json({ error: 'Please sign in again.' }, 401);
    if (!GKEY) return json({ error: 'Handwriting reading is not set up yet' });
    const b = await req.json().catch(() => ({}));
    const imgs: string[] = Array.isArray(b.images) ? b.images.filter((x: unknown) => typeof x === 'string' && x.length < 3_000_000).slice(0, 4) : [];
    if (!imgs.length) return json({ error: 'No photo received.' });
    if (!(await quota(user.id, imgs.length))) return json({ error: `Daily limit reached (${LIMIT} pages a day). Type your key points, or try again tomorrow.` });
    const body = { contents: [{ role: 'user', parts: [{ text: PROMPT(String(b.question || '')) }, ...imgs.map(d => ({ inline_data: { mime_type: 'image/jpeg', data: d } }))] }],
      generationConfig: { temperature: 0, maxOutputTokens: 4096 } };
    let r: Response | null = null, j: any = {};
    const call = async (m: string, secs: number, gc: Record<string, unknown>) => {
      const t0 = Date.now();
      try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, { method: 'POST', signal: AbortSignal.timeout(secs * 1000),
          headers: { 'Content-Type': 'application/json', 'x-goog-api-key': GKEY }, body: JSON.stringify({ ...body, generationConfig: gc }) });
        const jj = await res.json().catch(() => ({}));
        console.log('gemini', m, res.status, Date.now() - t0, 'ms', String(jj?.error?.message || '').slice(0, 120));
        return { res, jj };
      } catch (e) { console.log('gemini', m, 'timeout/err', Date.now() - t0, String(e).slice(0, 80)); return null; }
    };
    for (const [m, secs] of MODELS) {   // try the next model if Google retires one, does not offer it on this key, or it is too slow
      let out = await call(m, secs, { ...body.generationConfig, thinkingConfig: { thinkingLevel: 'low' } });
      if (out && out.res.status === 400 && /thinking/i.test(String(out.jj?.error?.message || ''))) out = await call(m, secs, body.generationConfig);
      if (!out) continue;
      r = out.res; j = out.jj;
      const msg = String(j?.error?.message || '');
      if (r.ok || !([404, 429, 500, 503].includes(r.status) || /no longer available|not found|not supported|limit: 0/i.test(msg))) break;
    }
    if (!r) return json({ error: 'The reading service is slow right now. Please try again in a minute.' });
    if (!r.ok) return json({ error: [429, 503].includes(r.status) ? 'The free reading service is busy. Please try again in a minute.' : 'Could not read the photo. Please try again.', detail: String(j?.error?.message || r.status).slice(0, 200) });
    const text = (j?.candidates?.[0]?.content?.parts || []).map((p: { text?: string }) => p.text || '').join('').trim();
    if (!text) return json({ error: 'No writing could be read from the photo. Try a clearer photo in good light.' });
    return json({ text: text.slice(0, 20000) });
  } catch (e) {
    return json({ error: 'Something went wrong. Please try again.', detail: String((e as Error).message || e).slice(0, 200) }, 500);
  }
});
