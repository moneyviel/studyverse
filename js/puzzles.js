/* ================= StudyVerse Puzzles: chapter-aware crosswords, Sudoku, Kakuro + warm-ups (js/puzzles.js) =================
   "360-degree" learning: the chapter you study turns into puzzles.
     📝 Chapter Crossword — 8–15 of the chapter's key terms; clues come from the lesson itself (match pairs, fill-ins,
        definitions, quiz stems; CA: quick-reference cards, MCQ stems, concept definitions, 📚 key rules/formulas).
     🔢 Sudoku 4×4 (Class 1–3) · 6×6 (Class 4–6) · 9×9 (Class 7+ and CA), easy/medium/hard, unique solution.
     🧠 Concept Sudoku — 4×4 / 6×6 with chapter terms as the symbols, plus a legend that teaches them.
     ➕ Kakuro 5×5 – 8×8, unique solution; maths / accounts / QA chapters get a ledger "story".
     🔎 Word search and 🔤 Anagram warm-ups from the chapter's terms.
     📅 Daily Puzzle — one puzzle a day from your current chapter (crossword → sudoku → kakuro, rotating), its own
        🔥 streak, stars through addXP(), badges (🧩 Puzzle Master …) and best times.
   Engine: js/puzzles-core.js (deterministic per seed = date + chapter), run in js/puzzles-worker.js when possible.
   Stars: hints are paid from the puzzle's prize first, then from your stars. Puzzles never use button.opt (plans.js
   counts those for the free daily limit), so they are free for everyone.
   Entry points: 🧩 tile on school World + Practice, a 🧩 button on every chapter and on the quest-complete card,
   CA home + Practice hub + every unit. State: ST.pz (synced with the rest of ST). */
(function () {
  'use strict';
  const D = document, PC = () => window.PuzzleCore;
  const $1 = (s, r) => (r || D).querySelector(s), $$ = (s, r) => [...(r || D).querySelectorAll(s)];
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const T = m => { try { toast(m); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const grade = () => { const s = STx(); return isCA() ? 13 : (+(s && s.profile && s.profile.grade) || 6); };
  const X = () => (window.Ca && Ca._) || null;
  const pad2 = n => String(n).padStart(2, '0');
  const localISO = (d = new Date()) => `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;
  const dayNum = (d = new Date()) => Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 864e5);
  const yISO = () => localISO(new Date(Date.now() - 864e5));
  const fmtT = s => `${Math.floor(s / 60)}:${pad2(s % 60)}`;
  const announce = m => { const a = $1('#s-puz .pz-live'); if (a && m) { a.textContent = ''; setTimeout(() => { a.textContent = m; }, 30); } try { if (window.A11Y && A11Y.cue) A11Y.cue(m); } catch (e) {} };

  /* ---------- saved state ---------- */
  function Z() {
    const s = STx(); s.pz = s.pz || {}; const z = s.pz;
    z.solved = z.solved || {}; z.best = z.best || {}; z.badges = z.badges || {}; z.daily = z.daily || { last: '', n: 0, best: 0, hist: {} };
    z.daily.hist = z.daily.hist || {}; z.saves = z.saves || {}; z.done = z.done || {}; z.ctr = z.ctr || {}; z.pref = z.pref || {}; z.flags = z.flags || {};
    z.total = z.total || 0; z.nohint = z.nohint || 0;
    return z;
  }
  let saveT = 0; const saveSoon = () => { clearTimeout(saveT); saveT = setTimeout(() => { try { save(); } catch (e) {} }, 1200); };
  const dailyLive = () => { const d = Z().daily; return d.last === localISO() || d.last === yISO() ? d.n : 0; };

  /* ---------- generation (Web Worker with a main-thread fallback; same result either way) ---------- */
  /* same ?v= as this script (index.html), so the worker and the service-worker cache stay in step */
  const VQ = (() => { try { const sc = D.currentScript || [...D.scripts].find(x => /js\/puzzles\.js/.test(x.src)); const m = sc && /\?v=[\w.]+/.exec(sc.src); return m ? m[0] : ''; } catch (e) { return ''; } })();
  let W = null, wid = 0; const pend = {};
  function worker() {
    if (W === false) return null; if (W) return W;
    try {
      W = new Worker('js/puzzles-worker.js' + VQ);
      W.onmessage = e => { const p = pend[e.data.id]; if (!p) return; delete pend[e.data.id]; clearTimeout(p.t); if (e.data.err) p.local(); else p.res(e.data.res); };
      W.onerror = ev => { try { ev.preventDefault(); } catch (x) {} W = false; Object.keys(pend).forEach(k => { const p = pend[k]; delete pend[k]; clearTimeout(p.t); p.local(); }); };
    } catch (e) { W = false; }
    return W || null;
  }
  function gen(fn, args) {
    return new Promise((res, rej) => {
      const local = () => { try { res(PC()[fn].apply(null, args)); } catch (e) { rej(e); } };
      const w = worker(); if (!w) return local();
      const id = ++wid; pend[id] = { res, local, t: setTimeout(() => { if (pend[id]) { delete pend[id]; local(); } }, 5000) };
      try { w.postMessage({ id, fn, args }); } catch (e) { delete pend[id]; local(); }
    });
  }

  /* ================= scope: which chapter ================= */
  // school {k:'s', g, sid, ci} · CA {k:'c', ch:'fnd-p2-ch02'} · free play {k:'q'}
  const scopeKey = sc => !sc || sc.k === 'q' ? 'free' : sc.k === 'c' ? sc.ch : `g${sc.g}-${sc.sid}-c${sc.ci}`;
  const NUMERIC = /^(maths|accountancy|economics)$/;
  async function caChapter(ch) {
    const x = X(); if (!x) return null;
    const lvl = x.levelOf(ch); let st; try { st = await x.structure(lvl); } catch (e) { return null; }
    for (const p of st.papers) { const i = p.chapters.findIndex(c => c.id === ch); if (i >= 0) return { st, p, c: p.chapters[i], i }; }
    return null;
  }
  async function info(sc) {
    if (!sc || sc.k === 'q') return { title: 'Free play', sub: 'Any time, any level', emoji: '🧩', numeric: true, key: 'free' };
    if (sc.k === 's') {
      const d = await subjectData(sc.g, sc.sid), c = d && d.chapters[sc.ci]; if (!c) return null;
      const meta = (((typeof CUR !== 'undefined' && CUR && CUR.grades && CUR.grades[sc.g]) || {}).subjects || []).find(s => s.id === sc.sid) || {};
      const st = (window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[sc.sid]) || { e: '📘' };
      return { title: c.title, sub: `${meta.name || sc.sid} · Class ${sc.g} · Chapter ${c.n}`, emoji: c.emoji || st.e, numeric: NUMERIC.test(sc.sid), key: scopeKey(sc), sname: meta.name || sc.sid };
    }
    const f = await caChapter(sc.ch); if (!f) return null;
    return { title: f.c.title, sub: `CA ${{ fnd: 'Foundation', int: 'Intermediate', fin: 'Final' }[sc.ch.split('-')[0]] || ''} · Paper ${String(f.p.key).replace('p', '')} ${f.p.name} · Ch ${f.c.n}`, emoji: '📘', numeric: /-p[13]-/.test(sc.ch), key: sc.ch, pname: f.p.name };
  }
  const TERMS = {};
  async function caUnits(c) {
    const x = X(), out = [];
    for (const u of c.units) { if (u.status !== 'built') continue; try { const d = await x.unitData(u.id); if (d) out.push(d); } catch (e) {} }
    return out;
  }
  const keyItems = c => ((window.CaKeysData && CaKeysData.ITEMS) || []).filter(it => c.units.some(u => u.id === it.u));
  async function terms(sc) {
    const k = scopeKey(sc); if (TERMS[k]) return TERMS[k];
    let own = [], near = [], groups = [];
    try {
      if (sc.k === 's') {
        const d = await subjectData(sc.g, sc.sid); const c = d && d.chapters[sc.ci];
        if (c) {
          own = PC().termsSchool(c);
          const order = []; for (let j = 1; j < d.chapters.length && order.length < 6; j++) [sc.ci - j, sc.ci + j].forEach(x => { if (x >= 0 && x < d.chapters.length && order.length < 6) order.push(x); });
          if (own.length < 20) order.forEach(x => near.push(...PC().termsSchool(d.chapters[x])));
          (c.topics || []).forEach(t => (t.games || []).forEach(gm => { if (gm && gm.type === 'match') groups.push({ title: gm.title || t.title, items: (gm.pairs || []).filter(p => Array.isArray(p) && /^[A-Za-z][A-Za-z '\-]*$/.test(String(p[0]).trim())).map(p => ({ label: String(p[0]).trim(), info: String(p[1]) })) }); }));
        }
      } else if (sc.k === 'c') {
        const f = await caChapter(sc.ch);
        if (f) {
          const units = await caUnits(f.c); own = PC().termsCA(units, keyItems(f.c));
          units.forEach(u => groups.push({ title: u.title, items: (u.quickref || []).filter(q => /^[A-Za-z][A-Za-z '\-]*$/.test(String(q.k || '').trim())).map(q => ({ label: String(q.k).trim(), info: String(q.v || '') })) }));
          if (own.length < 20) {
            const chs = f.p.chapters, order = []; for (let j = 1; j < chs.length && order.length < 5; j++) [f.i - j, f.i + j].forEach(x => { if (x >= 0 && x < chs.length && order.length < 5) order.push(x); });
            for (const x of order) near.push(...PC().termsCA(await caUnits(chs[x]), keyItems(chs[x])));
          }
        }
      }
    } catch (e) { console.warn('puzzle terms', e); }
    return (TERMS[k] = { own, near, groups });
  }
  /* one coherent set (a single match game: "4 market forms", "6 diseases") beats a mixed bag */
  const conceptFor = (t, g, k) => (g > 3 && PC().conceptSet(t.groups, 6, k, true)) || PC().conceptSet(t.groups, 4, k, true) || PC().conceptSet(t.groups, g <= 3 ? 4 : 6, k);
  const canXW = t => t && (t.own.length + t.near.length >= 8) && t.own.length >= 3;

  /* the student's current chapter: last topic studied (school) / last unit opened (CA) */
  async function curChapter() {
    if (isCA()) {
      const x = X(); if (!x) return { k: 'q' };
      const c = x.C(); let st; try { st = await x.structure(c.level || 'foundation'); } catch (e) { return { k: 'q' }; }
      let f = c.last && x.findUnit(st, c.last); if (!f) f = x.nextUnit(st);
      return f ? { k: 'c', ch: f.c.id } : { k: 'q' };
    }
    const g = +ST.profile.grade; let best = null;
    Object.entries(ST.topics || {}).forEach(([tid, v]) => { const m = /^g(\d+)-([a-z]+)-(\d+)-\d+$/.exec(tid); if (!m || +m[1] !== g) return; if (!best || String(v.last || '') > String(best.last || '')) best = { sid: m[2], cn: +m[3], last: v.last }; });
    if (best) { const d = await subjectData(g, best.sid); if (d) { const ci = d.chapters.findIndex(c => +c.n === best.cn); if (ci >= 0) return { k: 's', g, sid: best.sid, ci }; } }
    const subs = curSubjects(g).filter(s => !/hindi|sanskrit/.test(s.id)).concat(curSubjects(g).filter(s => /hindi|sanskrit/.test(s.id)));
    for (const s of subs) { const d = await subjectData(g, s.id); if (!d || !d.chapters.length) continue; let ci = d.chapters.findIndex(c => !c.topics.every(t => ST.topics[t.id])); if (ci < 0) ci = 0; return { k: 's', g, sid: s.id, ci }; }
    return { k: 'q' };
  }

  /* ---------- defaults by class ---------- */
  const defN = () => { const g = grade(); return g <= 3 ? 4 : g <= 6 ? 6 : 9; };
  const defKak = () => { const g = grade(); return g <= 5 ? 'easy' : g <= 8 ? 'medium' : 'hard'; };
  const pref = () => { const p = Z().pref; return { n: p.n || defN(), diff: p.diff || 'easy', kak: p.kak || defKak() }; };
  const TYPES = {
    xw: { e: '📝', n: 'Chapter Crossword', d: 'Key terms from this chapter, clues from the lesson.' },
    sdk: { e: '🔢', n: 'Sudoku', d: 'Every row, column and box holds each number once.' },
    csdk: { e: '🧠', n: 'Concept Sudoku', d: 'Sudoku with this chapter\'s terms as the symbols.' },
    kak: { e: '➕', n: 'Kakuro', d: 'Fill the cells so each run adds up to its clue.' },
    ws: { e: '🔎', n: 'Word search', d: 'Warm-up: find the chapter\'s key words.' },
    an: { e: '🔤', n: 'Anagram', d: 'Warm-up: unscramble five key terms.' } };
  const DIFFS = [['easy', 'Easy'], ['medium', 'Medium'], ['hard', 'Hard']];
  const KDIFFS = [['easy', 'Easy 5×5'], ['medium', 'Medium 6×6'], ['hard', 'Hard 7×7'], ['expert', 'Expert 8×8']];

  /* ================= screen ================= */
  function screen() {
    let s = D.getElementById('s-puz');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-puz'; D.querySelector('main').appendChild(s); }
    style(); return s;
  }
  let CTX = null;
  function stopPlay() { if (CTX) { CTX.stop(); CTX = null; } PLAY = null; }
  function makeCtx(host) {
    const c = { dead: false, ivs: [] };
    c.alive = () => { if (c.dead) return false; if (!host.isConnected || !D.getElementById('s-puz').classList.contains('active')) { c.stop(); return false; } return true; };
    c.iv = (f, ms) => { const id = setInterval(() => { if (c.alive()) f(); }, ms); c.ivs.push(id); return id; };
    c.stop = () => { c.dead = true; c.ivs.forEach(clearInterval); c.ivs = []; };
    return c;
  }
  function openScr(navKey, play) {
    stopPlay(); const s = screen(); show('puz', navKey || (isCA() ? 'practice' : 'practice'));
    const nav = D.querySelector('nav'); if (nav) nav.style.display = play ? 'none' : '';
    return s;
  }
  const navKeyOf = from => (from === 'world' || from === 'ca' ? 'world' : 'practice');

  /* ================= HUB ================= */
  let HUBFROM = 'practice';
  async function hub(o) {
    o = o || {}; if (o.from) HUBFROM = o.from;
    const el = openScr(navKeyOf(HUBFROM)); const z = Z();
    el.innerHTML = `<div class="pz-root pz-hub"><p class="pz-live sr-only" aria-live="polite"></p><button class="back" id="pzBack">← ${HUBFROM === 'world' || HUBFROM === 'ca' ? 'Home' : 'Practice'}</button>
      <div class="hello" role="heading" aria-level="1"><span aria-hidden="true">🧩</span> Puzzles <small>Crosswords, Sudoku and Kakuro from your chapters · free</small></div>
      <div id="pzDaily" class="card pz-daily"><p class="sub">Finding today's puzzle…</p></div>
      <div class="card"><h3>Quick play</h3><p class="sub">Number puzzles at your level. Pick a size and difficulty.</p>
        <div class="pz-games">${btn('sdk', null, 'qsdk')}${btn('kak', null, 'qkak')}</div>
        ${prefChips()}</div>
      <div class="card"><h3>Puzzle a chapter</h3><p class="sub">Every chapter makes its own crossword, warm-ups and concept sudoku.</p><div id="pzChs"><p class="sub">Loading chapters…</p></div></div>
      <div class="card"><h3>🏅 Puzzle badges</h3>${badgeGrid()}<div class="pz-stats"><span>🧩 <b>${z.total}</b> solved</span><span>📅 best daily streak <b>${z.daily.best || 0}</b></span></div>${bestList()}</div></div>`;
    $1('#pzBack').onclick = () => back(HUBFROM);
    wirePref(el);
    el.querySelector('[data-q="qsdk"]').onclick = () => { S('open'); play({ t: 'sdk', sc: { k: 'q' }, seed: nextSeed('free', 'sdk'), n: pref().n, diff: pref().diff }); };
    el.querySelector('[data-q="qkak"]').onclick = () => { S('open'); play({ t: 'kak', sc: { k: 'q' }, seed: nextSeed('free', 'kak'), diff: pref().kak }); };
    dailyCard($1('#pzDaily'));
    chapterList($1('#pzChs'));
  }
  function back(from) {
    try {
      if (from && typeof from === 'object') { if (from.t === 'chapter') return chapterScreen(from.sid, from.ci); if (from.t === 'unit' && window.Ca) return Ca.unit(from.uid); if (from.t === 'topic') return chapterScreen(from.sid, from.ci); }
      if (from === 'world' || from === 'ca') return worldScreen();
      return practiceScreen();
    } catch (e) { worldScreen(); }
  }
  function btn(t, extra, q) { const m = TYPES[t]; return `<button class="pz-game pz-g-${t}" data-q="${q || t}"><span class="pz-ge" aria-hidden="true">${m.e}</span><b>${m.n}</b><small>${extra ? E(extra) : m.d}</small></button>`; }
  function prefChips() {
    const p = pref();
    const row = (k, list, cur, lab) => `<div class="pz-chips" role="radiogroup" aria-label="${lab}">${list.map(([v, n]) => `<button type="button" role="radio" aria-checked="${String(v) === String(cur)}" class="pz-chip${String(v) === String(cur) ? ' on' : ''}" data-pk="${k}" data-pv="${v}">${n}</button>`).join('')}</div>`;
    return `<div class="pz-prefs"><small>Sudoku size</small>${row('n', [[4, '4×4'], [6, '6×6'], [9, '9×9']], p.n, 'Sudoku size')}<small>Sudoku difficulty</small>${row('diff', DIFFS, p.diff, 'Sudoku difficulty')}<small>Kakuro</small>${row('kak', KDIFFS, p.kak, 'Kakuro difficulty')}</div>`;
  }
  function wirePref(el) {
    el.querySelectorAll('.pz-chip').forEach(b => b.onclick = () => {
      const z = Z(); z.pref[b.dataset.pk] = b.dataset.pk === 'n' ? +b.dataset.pv : b.dataset.pv; saveSoon(); S('tap');
      el.querySelectorAll(`.pz-chip[data-pk="${b.dataset.pk}"]`).forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-checked', String(on)); });
    });
  }
  const nextSeed = (k, t) => { const z = Z(), key = k + '|' + t; z.ctr[key] = (z.ctr[key] || 0) + 1; saveSoon(); return `${key}|${z.ctr[key]}`; };

  async function dailySpec() {
    const sc = await curChapter(), iso = localISO(), dn = dayNum();
    let t = ['xw', 'sdk', 'kak'][dn % 3];
    if (t === 'xw' && !canXW(await terms(sc))) t = 'sdk';
    const p = pref();
    return { t, sc, seed: `daily|${iso}|${scopeKey(sc)}`, n: p.n, diff: t === 'sdk' ? (dn % 2 ? 'medium' : 'easy') : p.diff, kdiff: p.kak, daily: iso };
  }
  async function dailyCard(box) {
    if (!box) return;
    let sp, inf; try { sp = await dailySpec(); inf = await info(sp.sc); } catch (e) { box.innerHTML = '<p class="sub">Daily puzzle is not ready right now.</p>'; return; }
    if (!box.isConnected) return;
    const z = Z(), done = z.daily.hist[sp.daily], m = TYPES[sp.t], n = dailyLive();
    box.innerHTML = `<div class="pz-dh"><span class="pz-de" aria-hidden="true">📅</span><div><span class="tag">Daily Puzzle · ${E(new Date().toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' }))}</span>
      <h2>${m.e} ${m.n}</h2><p class="sub">From ${E(inf ? inf.title : 'your chapter')}${inf && inf.sub ? ' · ' + E(inf.sub) : ''}</p></div></div>
      <div class="pz-streak"><span>🔥 Daily streak <b>${n}</b></span><span>Best <b>${z.daily.best || 0}</b></span>${done ? '<span class="pz-ok">✓ Solved today</span>' : '<span>+10 ⭐ bonus</span>'}</div>
      <button class="btn ${done ? 'ghost' : 'mint'}" id="pzDailyGo">${done ? 'Play it again' : 'Play today\'s puzzle ▶'}</button>`;
    $1('#pzDailyGo', box).onclick = () => { S('open'); play(Object.assign({}, sp, sp.t === 'kak' ? { diff: sp.kdiff } : {})); };
  }
  async function chapterList(box) {
    if (!box) return;
    if (isCA()) {
      const x = X(); let st = null; try { st = await x.structure(x.C().level || 'foundation'); } catch (e) {}
      if (!st) { box.innerHTML = '<p class="sub">Could not load your papers.</p>'; return; }
      box.innerHTML = st.papers.map(p => `<details class="pz-subj"><summary><b>Paper ${String(p.key).replace('p', '')}: ${E(p.name)}</b><small>${p.chapters.length} chapters</small></summary><div class="pz-chl">${p.chapters.map(c => `<button class="pz-chb" data-ch="${E(c.id)}"><span>${c.n}</span>${E(c.title)}</button>`).join('')}</div></details>`).join('');
      box.querySelectorAll('[data-ch]').forEach(b => b.onclick = () => { S('open'); chapter({ k: 'c', ch: b.dataset.ch }, { t: 'hub' }); });
      return;
    }
    const g = +ST.profile.grade, subs = curSubjects(g);
    box.innerHTML = subs.map(s => `<details class="pz-subj" data-sid="${E(s.id)}"><summary><b>${E((Worlds.SUBJECT_STYLE[s.id] || { e: '📘' }).e)} ${E(s.name)}</b><small>${/hindi|sanskrit/.test(s.id) ? 'number puzzles' : 'tap to see chapters'}</small></summary><div class="pz-chl"><p class="sub">Loading…</p></div></details>`).join('') || '<p class="sub">No subjects yet.</p>';
    box.querySelectorAll('details.pz-subj').forEach(dt => dt.addEventListener('toggle', async () => {
      if (!dt.open || dt.dataset.ok) return; dt.dataset.ok = 1;
      const d = await subjectData(g, dt.dataset.sid), l = $1('.pz-chl', dt);
      if (!d) { l.innerHTML = '<p class="sub">Coming soon.</p>'; return; }
      l.innerHTML = d.chapters.map((c, i) => `<button class="pz-chb" data-ci="${i}"><span>${E(c.n)}</span>${E(c.title)}</button>`).join('');
      l.querySelectorAll('[data-ci]').forEach(b => b.onclick = () => { S('open'); chapter({ k: 's', g, sid: dt.dataset.sid, ci: +b.dataset.ci }, { t: 'hub' }); });
    }));
  }

  /* ================= CHAPTER: its puzzles ================= */
  async function chapter(sc, from) {
    const el = openScr(sc.k === 'c' ? 'world' : 'world');
    el.innerHTML = `<div class="pz-root pz-chap"><p class="sub pz-load">Building this chapter's puzzles…</p></div>`;
    const [inf, t] = await Promise.all([info(sc), terms(sc)]);
    if (!el.isConnected || !D.getElementById('s-puz').classList.contains('active')) return;
    if (!inf) { el.innerHTML = '<div class="card"><p class="sub">This chapter is not available.</p></div>'; return; }
    const g = grade(), cs = conceptFor(t, g, scopeKey(sc));
    const xw = canXW(t), words = t.own.length, p = pref();
    const backLabel = from && from.t === 'hub' ? 'Puzzles' : from && from.t === 'unit' ? 'Unit' : 'Chapter';
    el.innerHTML = `<div class="pz-root pz-chap"><p class="pz-live sr-only" aria-live="polite"></p><button class="back" id="pzBack">← ${backLabel}</button>
      <div class="card pz-chead"><div class="pz-ce" aria-hidden="true">${E(inf.emoji)}</div><div><span class="tag">🧩 Puzzle this chapter</span><h2>${E(inf.title)}</h2><p class="sub">${E(inf.sub)}</p></div></div>
      <div class="pz-games">
        ${xw ? btn('xw', `${Math.min(15, words + t.near.length)} key terms${words < 8 ? ' (with nearby chapters)' : ''}`) : ''}
        ${words >= 4 ? btn('ws') : ''}${words >= 5 ? btn('an') : ''}
        ${cs ? btn('csdk', `${cs.items.length} symbols: ${cs.items.map(i => i.label).slice(0, 3).join(', ')}…`) : ''}
        ${btn('sdk', `${p.n}×${p.n} · ${p.diff}`)}${btn('kak', inf.numeric ? 'With a ledger story · ' + p.kak : p.kak)}
      </div>
      ${!xw ? `<p class="note">${words ? 'Not enough key terms here yet for a crossword.' : 'Word puzzles need English key terms — this chapter gets number puzzles.'}</p>` : ''}
      <div class="card">${prefChips()}</div>
      <button class="btn ghost" id="pzHub">🧩 All puzzles & daily puzzle</button></div>`;
    $1('#pzBack').onclick = () => (from && from.t === 'hub' ? hub() : back(from));
    $1('#pzHub').onclick = () => hub({});
    wirePref(el);
    const k = scopeKey(sc);
    el.querySelectorAll('.pz-game').forEach(b => b.onclick = () => {
      S('open'); const ty = b.dataset.q, pp = pref();
      const sp = { t: ty, sc, seed: nextSeed(k, ty), from };
      if (ty === 'sdk') Object.assign(sp, { n: pp.n, diff: pp.diff });
      if (ty === 'csdk') Object.assign(sp, { n: cs.items.length, diff: pp.diff === 'hard' ? 'medium' : pp.diff });
      if (ty === 'kak') Object.assign(sp, { diff: pp.kak });
      play(sp);
    });
  }

  /* ================= PLAY ================= */
  let PLAY = null;          // the running puzzle (for keys + Listen mode)
  const pid = sp => [sp.t, sp.seed, sp.n || '', sp.diff || ''].join('|');
  async function play(sp) {
    const el = openScr(sp.daily ? 'practice' : 'practice', true);
    el.innerHTML = `<div class="pz-root"><div class="card pz-genc"><div class="pz-spin" aria-hidden="true">🧩</div><b>Making your puzzle…</b><p class="sub">Checking it has exactly one answer.</p></div></div>`;
    let p = null, extra = {};
    try {
      if (sp.t === 'xw') { const t = await terms(sp.sc); p = canXW(t) ? await gen('chapterCrossword', [t.own, t.near, sp.seed]) : null; if (!p) { T('Not enough key terms for a crossword — here is a sudoku instead'); sp = Object.assign({}, sp, { t: 'sdk', n: pref().n, diff: pref().diff }); } }
      if (sp.t === 'csdk') { const t = await terms(sp.sc); extra.set = conceptFor(t, grade(), scopeKey(sp.sc)); if (extra.set) sp = Object.assign({}, sp, { n: extra.set.items.length }); if (!extra.set) sp = Object.assign({}, sp, { t: 'sdk', n: pref().n }); }
      if (sp.t === 'sdk' || sp.t === 'csdk') p = await gen('sudoku', [sp.n || pref().n, sp.diff || 'easy', sp.seed]);
      if (sp.t === 'kak') { p = await gen('kakuro', [0, sp.diff || 'easy', sp.seed]); extra.info = await info(sp.sc); }
      if (sp.t === 'ws' || sp.t === 'an') {
        const t = await terms(sp.sc), g = grade(), n = g <= 3 ? 8 : g <= 6 ? 10 : 12;
        const words = PC().shuffle(t.own.filter(x => x.a.length >= 3 && x.a.length <= n), PC().rng(sp.seed)).slice(0, sp.t === 'ws' ? 8 : 5);
        if (sp.t === 'ws') { p = await gen('wordsearch', [words.map(w => w.a), n, g <= 3 ? 2 : g <= 6 ? 3 : 8, sp.seed]); if (p) p.clues = Object.fromEntries(words.map(w => [w.a, w])); }
        else p = words.length >= 3 ? { type: 'anagram', words: words.map(w => ({ a: w.a, clue: w.clue, enum: w.enum, ctx: w.ctx || '', s: PC().scramble(w.a, sp.seed) })) } : null;
      }
    } catch (e) { console.error(e); p = null; }
    if (!el.isConnected || !D.getElementById('s-puz').classList.contains('active')) return;
    if (!p) { el.innerHTML = `<div class="pz-root"><button class="back" id="pzBack">← Back</button><div class="card"><p class="sub">This puzzle could not be made. Please try another one.</p></div></div>`; $1('#pzBack').onclick = () => hub(); return; }
    const id = pid(sp), saved = Z().saves[id];
    CTX = makeCtx(el);
    const st = { sp, p, id, t0: Date.now(), secs: saved ? saved.t || 0 : 0, hints: 0, spent: 0, pool: prize(sp, p), done: false, extra };
    if (saved && saved.pool != null) { st.pool = saved.pool; st.hints = saved.hints || 0; }
    PLAY = st;
    ({ xw: playXW, sdk: playSDK, csdk: playSDK, kak: playKAK, ws: playWS, an: playAN })[sp.t](el, st, saved);
    if (st.sp.t !== 'an') startClock(st);
    try { if (window.A11Y && A11Y.readScreen) setTimeout(() => A11Y.readScreen(), 300); } catch (e) {}
  }
  function prize(sp, p) {
    if (sp.t === 'xw') return 10 + p.entries.length;
    if (sp.t === 'sdk' || sp.t === 'csdk') return ({ 4: { easy: 6, medium: 8, hard: 10 }, 6: { easy: 10, medium: 12, hard: 15 }, 9: { easy: 15, medium: 20, hard: 25 } }[p.n] || {})[p.diff] || 10;
    if (sp.t === 'kak') return { easy: 12, medium: 16, hard: 20, expert: 25 }[p.diff] || 12;
    return sp.t === 'ws' ? 8 : 6;
  }
  function header(st, title, sub) {
    const back = st.sp.from && st.sp.from.t !== 'hub' ? 'Puzzles' : 'Puzzles';
    return `<p class="pz-live sr-only" aria-live="polite"></p><div class="pz-bar"><button class="pz-x" id="pzQuit" aria-label="Leave puzzle (progress is saved)">← ${back}</button><b class="pz-title">${title}</b><span class="pz-time" role="timer" aria-label="Time">${fmtT(st.secs)}</span><span class="pz-prize" title="Stars for solving">⭐ <b>${st.pool}</b></span></div>${sub ? `<p class="pz-sub">${sub}</p>` : ''}`;
  }
  function wireQuit(el, st) {
    $1('#pzQuit', el).onclick = () => { persist(st, true); S('tap'); const sp = st.sp; stopPlay(); if (sp.sc && sp.sc.k !== 'q' && !sp.daily) chapter(sp.sc, sp.from || { t: 'hub' }); else hub(); };
  }
  function startClock(st) {
    let last = Date.now();
    CTX.iv(() => { const n = Date.now(); if (!D.hidden && !st.done) { st.secs += Math.round((n - last) / 1000); } last = n; const t = $1('#s-puz .pz-time'); if (t) t.textContent = fmtT(st.secs); }, 1000);
  }
  function setPool(st) { const b = $1('#s-puz .pz-prize b'); if (b) b.textContent = st.pool; }
  /* hints: paid from this puzzle's prize first, then from your stars */
  function charge(st, cost, what) {
    if (st.pool >= cost) { st.pool -= cost; }
    else {
      const need = cost - st.pool;
      if ((ST.xp || 0) < need) { T(`You need ${need} more ⭐ for this hint`); S('hmm'); return false; }
      st.pool = 0; addXP(-need); st.spent += need;
    }
    st.hints++; setPool(st); persist(st); announce(`${what}. Hint used: ${cost} star${cost > 1 ? 's' : ''}.`);
    return true;
  }
  function persist(st, now) {
    if (st.done || !st.getState) return;
    const z = Z(); z.saves[st.id] = Object.assign(st.getState(), { t: st.secs, pool: st.pool, hints: st.hints, at: Date.now() });
    const ks = Object.keys(z.saves).sort((a, b) => z.saves[b].at - z.saves[a].at); ks.slice(8).forEach(k => delete z.saves[k]);
    if (now) { try { save(); } catch (e) {} } else saveSoon();
  }

  /* ---------- 📝 CROSSWORD ---------- */
  function playXW(el, st, saved) {
    const p = st.p, w = p.w, h = p.h, N = w * h, sol = p.grid.join(''), u = new Array(N).fill(''), rev = new Set(), wrong = new Set();
    const at = {}; p.entries.forEach((e, k) => { for (let j = 0; j < e.len; j++) { const i = (e.r + (e.dir === 'D' ? j : 0)) * w + e.c + (e.dir === 'A' ? j : 0); (at[i] = at[i] || {})[e.dir] = k; } });
    if (saved && saved.u) saved.u.forEach((c, i) => { if (sol[i] !== '#' && /^[A-Z]$/.test(c)) u[i] = c; });
    if (saved && saved.rev) saved.rev.forEach(i => rev.add(i));
    st.getState = () => ({ u: u.slice(), rev: [...rev] });
    let cur = p.entries[0].r * w + p.entries[0].c, dir = p.entries[0].dir;
    const near = p.entries.some(e => e.near);
    const nums = {}; p.entries.forEach(e => { nums[e.r * w + e.c] = e.n; });
    const cellsOf = k => { const e = p.entries[k], l = []; for (let j = 0; j < e.len; j++) l.push((e.r + (e.dir === 'D' ? j : 0)) * w + e.c + (e.dir === 'A' ? j : 0)); return l; };
    const entryAt = (i, d) => (at[i] ? (at[i][d] != null ? at[i][d] : at[i][d === 'A' ? 'D' : 'A']) : null);
    const dirName = d => (d === 'A' ? 'Across' : 'Down');
    const clueHTML = e => `${e.ctx ? `<span class="pz-ctx">${E(e.ctx)} ·</span> ` : ''}${E(e.clue)} <span class="pz-enum">${E(e.enum)}</span>${e.near ? ' <span class="pz-near" title="From a nearby chapter">↗</span>' : ''}`;
    el.innerHTML = `<div class="pz-root pz-xw" data-pz="xw">${header(st, '📝 Chapter Crossword', `${p.entries.length} words${near ? ' · ↗ = from a nearby chapter' : ''}`)}
      <div class="pz-cluebar" id="pzClue" aria-live="polite"></div>
      <div class="pz-gridwrap"><div class="pz-xgrid" id="pzGrid" role="grid" aria-label="Crossword, ${w} columns by ${h} rows. Type letters; arrow keys move; Enter goes to the next clue; Space turns between across and down." style="--w:${w};--h:${h}">
        ${Array.from({ length: h }, (_, y) => `<div role="row" class="pz-row">${Array.from({ length: w }, (_, x) => { const i = y * w + x; return sol[i] === '#' ? `<div role="gridcell" class="pz-c blk" aria-hidden="true"></div>` : `<div role="gridcell" class="pz-c" data-i="${i}" tabindex="-1">${nums[i] ? `<span class="pz-n" aria-hidden="true">${nums[i]}</span>` : ''}<span class="pz-l" aria-hidden="true"></span></div>`; }).join('')}</div>`).join('')}
      </div></div>
      <div class="pz-tools"><button class="pz-tb" id="pzRev">💡 Reveal letter <small>2⭐</small></button><button class="pz-tb" id="pzChk">✔ Check word <small>1⭐</small></button><button class="pz-tb" id="pzDir" aria-label="Switch between across and down">⇄</button></div>
      ${kbHTML()}
      <div class="card pz-clues"><h3>Across</h3><ol>${p.entries.filter(e => e.dir === 'A').map(e => `<li><button class="pz-cl" data-k="${p.entries.indexOf(e)}"><b>${e.n}</b> ${clueHTML(e)}</button></li>`).join('')}</ol>
        <h3>Down</h3><ol>${p.entries.filter(e => e.dir === 'D').map(e => `<li><button class="pz-cl" data-k="${p.entries.indexOf(e)}"><b>${e.n}</b> ${clueHTML(e)}</button></li>`).join('')}</ol></div></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el), cellEl = i => grid.querySelector(`[data-i="${i}"]`);
    const paint = (speak) => {
      const k = entryAt(cur, dir); if (k == null) return; dir = p.entries[k].dir; const cs = new Set(cellsOf(k)), e = p.entries[k];
      $$('.pz-c[data-i]', grid).forEach(c => {
        const i = +c.dataset.i, L = u[i]; c.querySelector('.pz-l').textContent = L;
        c.classList.toggle('word', cs.has(i)); c.classList.toggle('cur', i === cur); c.classList.toggle('rev', rev.has(i)); c.classList.toggle('bad', wrong.has(i));
        c.tabIndex = i === cur ? 0 : -1;
        const parts = []; if (at[i].A != null) parts.push(`${p.entries[at[i].A].n} across`); if (at[i].D != null) parts.push(`${p.entries[at[i].D].n} down`);
        c.setAttribute('aria-label', `${parts.join(', ')}. Row ${Math.floor(i / w) + 1}, column ${i % w + 1}: ${L || 'empty'}${rev.has(i) ? ', revealed' : ''}${wrong.has(i) ? ', wrong' : ''}`);
        c.setAttribute('aria-selected', String(i === cur));
      });
      $1('#pzClue', el).innerHTML = `<b>${e.n} ${dirName(e.dir)}</b> ${clueHTML(e)}`;
      $$('.pz-cl', el).forEach(b => b.classList.toggle('on', +b.dataset.k === k));
      if (speak) announce(`${e.n} ${dirName(e.dir)}, ${e.len} letters. ${e.ctx ? e.ctx + '. ' : ''}${e.clue}. ${cellsOf(k).map(i => u[i] || 'blank').join(', ')}`);
    };
    const focusCur = () => { const c = cellEl(cur); if (c && el.contains(D.activeElement) && D.activeElement !== c && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const done = () => { for (let i = 0; i < N; i++) if (sol[i] !== '#' && u[i] !== sol[i]) return false; return true; };
    const filled = () => { for (let i = 0; i < N; i++) if (sol[i] !== '#' && !u[i]) return false; return true; };
    const after = () => { persist(st); if (done()) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (filled()) { T('All filled — but some letters are not right yet'); S('hmm'); } };
    const moveIn = (step) => { const k = entryAt(cur, dir), cs = cellsOf(k), j = cs.indexOf(cur) + step; if (j >= 0 && j < cs.length) cur = cs[j]; };
    const typeL = L => { if (st.done) return; if (!rev.has(cur)) { u[cur] = L; wrong.delete(cur); } S('tap'); moveIn(1); paint(); focusCur(); after(); };
    const backsp = () => { if (st.done) return; if (u[cur] && !rev.has(cur)) { u[cur] = ''; wrong.delete(cur); } else { moveIn(-1); if (!rev.has(cur)) { u[cur] = ''; wrong.delete(cur); } } paint(); focusCur(); persist(st); };
    const gotoEntry = (k, speak) => { const e = p.entries[k], cs = cellsOf(k); dir = e.dir; cur = cs.find(i => !u[i]) ?? cs[0]; paint(speak !== false); focusCur(); };
    const nextEntry = s => { const k = entryAt(cur, dir); gotoEntry((k + s + p.entries.length) % p.entries.length); };
    const arrow = (dy, dx) => { let y = Math.floor(cur / w), x = cur % w; for (;;) { y += dy; x += dx; if (y < 0 || x < 0 || y >= h || x >= w) return; const i = y * w + x; if (sol[i] !== '#') { cur = i; const nd = dx ? 'A' : 'D'; if (at[i][nd] != null) dir = nd; paint(true); focusCur(); return; } } };
    const toggle = () => { const o = dir === 'A' ? 'D' : 'A'; if (at[cur][o] != null) { dir = o; paint(true); } };
    grid.addEventListener('click', e => { const c = e.target.closest('.pz-c[data-i]'); if (!c) return; const i = +c.dataset.i; if (i === cur) toggle(); else { cur = i; if (at[i][dir] == null) dir = dir === 'A' ? 'D' : 'A'; paint(true); } c.focus({ preventScroll: true }); });
    $$('.pz-cl', el).forEach(b => b.onclick = () => { gotoEntry(+b.dataset.k); grid.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
    $1('#pzDir', el).onclick = toggle;
    $1('#pzRev', el).onclick = () => { if (st.done) return; if (u[cur] === sol[cur]) { const k = entryAt(cur, dir), nx = cellsOf(k).find(i => u[i] !== sol[i]); if (nx == null) { T('This word is already right'); return; } cur = nx; } if (!charge(st, 2, `Revealed ${sol[cur]}`)) return; u[cur] = sol[cur]; rev.add(cur); wrong.delete(cur); S('coin'); paint(); after(); };
    $1('#pzChk', el).onclick = () => { if (st.done) return; const cs = cellsOf(entryAt(cur, dir)); if (cs.every(i => !u[i])) { T('Type some letters first'); return; } if (!charge(st, 1, 'Checked this word')) return; let bad = 0; cs.forEach(i => { if (u[i] && u[i] !== sol[i]) { wrong.add(i); bad++; } }); S(bad ? 'wrong' : 'correct'); T(bad ? `${bad} letter${bad > 1 ? 's' : ''} to fix (marked red)` : 'Every letter so far is right ✓'); paint(); };
    wireKB(el, k => (k === '⌫' ? backsp() : k === '⇥' ? nextEntry(1) : typeL(k)));
    st.key = e => {
      if (/^[a-zA-Z]$/.test(e.key)) { typeL(e.key.toUpperCase()); return true; }
      if (e.key === 'Backspace' || e.key === 'Delete') { backsp(); return true; }
      if (e.key === 'ArrowRight') { arrow(0, 1); return true; } if (e.key === 'ArrowLeft') { arrow(0, -1); return true; }
      if (e.key === 'ArrowDown') { arrow(1, 0); return true; } if (e.key === 'ArrowUp') { arrow(-1, 0); return true; }
      if (e.key === 'Enter') { nextEntry(e.shiftKey ? -1 : 1); return true; }
      if (e.key === ' ') { toggle(); return true; }
      return false;
    };
    st.speech = () => { const k = entryAt(cur, dir), e = p.entries[k]; return `Chapter crossword, ${p.entries.length} words. ${e.n} ${dirName(e.dir)}, ${e.len} letters. ${e.ctx ? e.ctx + '. ' : ''}${e.clue}. So far: ${cellsOf(k).map(i => u[i] || 'blank').join(', ')}. Type the letters. Enter goes to the next clue, Space switches across and down.`; };
    paint();
  }
  function kbHTML() {
    const rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];
    return `<div class="pz-kb" role="group" aria-label="Letter keyboard">${rows.map((r, j) => `<div class="pz-kr">${j === 2 ? '<button class="pz-k wide" data-key="⇥" aria-label="Next clue">Next ⇥</button>' : ''}${r.split('').map(c => `<button class="pz-k" data-key="${c}">${c}</button>`).join('')}${j === 2 ? '<button class="pz-k wide" data-key="⌫" aria-label="Delete">⌫</button>' : ''}</div>`).join('')}</div>`;
  }
  function wireKB(el, fn) { $$('.pz-k', el).forEach(b => b.addEventListener('click', e => { e.preventDefault(); fn(b.dataset.key); })); }

  /* ---------- 🔢 SUDOKU (classic + concept) ---------- */
  function playSDK(el, st, saved) {
    const p = st.p, n = p.n, N = n * n, [bh, bw] = p.box, set = st.extra.set, u = p.puzzle.slice(), pm = new Array(N).fill(0), undo = [];
    const given = p.puzzle.map(v => !!v), shown = new Set();
    if (saved && saved.u) saved.u.forEach((v, i) => { if (!given[i] && v >= 0 && v <= n) u[i] = v; });
    if (saved && saved.pm) saved.pm.forEach((v, i) => { pm[i] = v | 0; });
    if (saved && saved.shown) saved.shown.forEach(i => shown.add(i));
    st.getState = () => ({ u: u.slice(), pm: pm.slice(), shown: [...shown] });
    let cur = u.findIndex(v => !v); if (cur < 0) cur = 0; let pencil = false;
    const sym = v => (set ? set.items[v - 1].sym : String(v)), lab = v => (set ? set.items[v - 1].label : String(v));
    const title = set ? '🧠 Concept Sudoku' : '🔢 Sudoku';
    el.innerHTML = `<div class="pz-root pz-sdk${set ? ' pz-csdk' : ''}" data-pz="${set ? 'csdk' : 'sdk'}">${header(st, title, `${n}×${n} · ${p.diff}${set ? ' · each symbol once in every row, column and box' : ''}`)}
      ${set ? `<div class="card pz-legend"><h3>${set.title ? E(set.title) : 'Legend'}</h3><ul>${set.items.map(it => `<li><span class="pz-sym" aria-hidden="true">${it.sym}</span><b>${E(it.label)}</b>${it.info ? `<small>${E(it.info)}</small>` : ''}</li>`).join('')}</ul></div>` : ''}
      <div class="pz-gridwrap"><div class="pz-sgrid n${n}" id="pzGrid" role="grid" aria-label="Sudoku, ${n} by ${n}. Arrow keys move; type ${set ? '1 to ' + n + ' for the symbols' : 'a number 1 to ' + n}; P switches pencil marks." style="--n:${n}">
        ${Array.from({ length: n }, (_, y) => `<div role="row" class="pz-row">${Array.from({ length: n }, (_, x) => { const i = y * n + x; return `<div role="gridcell" class="pz-s${given[i] ? ' giv' : ''}${(x + 1) % bw === 0 && x < n - 1 ? ' br' : ''}${(y + 1) % bh === 0 && y < n - 1 ? ' bb' : ''}" data-i="${i}" tabindex="-1"></div>`; }).join('')}</div>`).join('')}
      </div></div>
      <div class="pz-pad n${n}" role="group" aria-label="${set ? 'Symbols' : 'Numbers'}">${Array.from({ length: n }, (_, k) => `<button class="pz-num" data-v="${k + 1}" aria-label="${E(lab(k + 1))}"><span>${sym(k + 1)}</span>${set ? `<small>${E(lab(k + 1))}</small>` : ''}</button>`).join('')}</div>
      <div class="pz-tools"><button class="pz-tb" id="pzPen" aria-pressed="false">✏️ Pencil</button><button class="pz-tb" id="pzErase">⌫ Erase</button><button class="pz-tb" id="pzUndo">↶ Undo</button><button class="pz-tb" id="pzHint">💡 Reveal <small>2⭐</small></button></div></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el);
    const conflicts = () => {
      const bad = new Set(), U = [];
      for (let r = 0; r < n; r++) U.push(Array.from({ length: n }, (_, c) => r * n + c));
      for (let c = 0; c < n; c++) U.push(Array.from({ length: n }, (_, r) => r * n + c));
      for (let b = 0; b < n; b++) { const br = Math.floor(b / (n / bw)) * bh, bc = (b % (n / bw)) * bw, l = []; for (let r = 0; r < bh; r++) for (let c = 0; c < bw; c++) l.push((br + r) * n + bc + c); U.push(l); }
      U.forEach(l => { const m = {}; l.forEach(i => { if (u[i]) (m[u[i]] = m[u[i]] || []).push(i); }); Object.values(m).forEach(a => { if (a.length > 1) a.forEach(i => bad.add(i)); }); });
      return bad;
    };
    const paint = () => {
      const bad = conflicts(), cv = u[cur];
      $$('.pz-s', grid).forEach(c => {
        const i = +c.dataset.i, v = u[i], r = Math.floor(i / n), col = i % n;
        c.innerHTML = v ? `<span class="pz-v">${sym(v)}</span>${set ? `<small class="pz-vl">${E(lab(v).slice(0, 5))}</small>` : ''}` : pm[i] ? `<span class="pz-pm">${Array.from({ length: n }, (_, k) => (pm[i] >> k) & 1 ? `<i>${sym(k + 1)}</i>` : '<i></i>').join('')}</span>` : '';
        c.classList.toggle('cur', i === cur); c.classList.toggle('bad', bad.has(i)); c.classList.toggle('rev', shown.has(i));
        c.classList.toggle('peer', i !== cur && (r === Math.floor(cur / n) || col === cur % n)); c.classList.toggle('same', !!cv && v === cv && i !== cur);
        c.tabIndex = i === cur ? 0 : -1;
        c.setAttribute('aria-label', `Row ${r + 1}, column ${col + 1}: ${v ? lab(v) : 'empty'}${given[i] ? ', given' : ''}${bad.has(i) ? ', clashes' : ''}${!v && pm[i] ? ', pencil ' + Array.from({ length: n }, (_, k) => (pm[i] >> k) & 1 ? lab(k + 1) : '').filter(Boolean).join(' ') : ''}`);
        c.setAttribute('aria-selected', String(i === cur));
      });
      $1('#pzPen', el).classList.toggle('on', pencil); $1('#pzPen', el).setAttribute('aria-pressed', String(pencil));
    };
    const focusCur = () => { const c = grid.querySelector(`[data-i="${cur}"]`); if (c && D.activeElement && D.activeElement.closest && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const check = () => { persist(st); if (u.every(v => v) && !conflicts().size) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (u.every(v => v)) { T('Every cell is filled, but some clash (red)'); S('hmm'); } };
    const setV = v => {
      if (st.done || given[cur] || shown.has(cur)) { if (given[cur]) { T('That one is given'); S('hmm'); } return; }
      undo.push([cur, u[cur], pm[cur]]); if (undo.length > 300) undo.shift();
      if (pencil && v) { pm[cur] ^= 1 << (v - 1); u[cur] = 0; S('tap'); paint(); persist(st); return; }
      u[cur] = u[cur] === v ? 0 : v; pm[cur] = 0;
      if (v && u[cur]) { const r = Math.floor(cur / n), c = cur % n; for (let k = 0; k < n; k++) { [r * n + k, k * n + c].forEach(j => { pm[j] &= ~(1 << (v - 1)); }); } }
      S(conflicts().has(cur) ? 'wrong' : 'tap'); paint(); announce(`${u[cur] ? lab(u[cur]) : 'cleared'}${conflicts().has(cur) ? ', clashes' : ''}`); check();
    };
    grid.addEventListener('click', e => { const c = e.target.closest('.pz-s'); if (!c) return; cur = +c.dataset.i; paint(); c.focus({ preventScroll: true }); });
    $$('.pz-num', el).forEach(b => b.onclick = () => setV(+b.dataset.v));
    $1('#pzPen', el).onclick = () => { pencil = !pencil; S('tap'); paint(); announce(pencil ? 'Pencil marks on' : 'Pencil marks off'); };
    $1('#pzErase', el).onclick = () => { if (given[cur] || shown.has(cur)) return; undo.push([cur, u[cur], pm[cur]]); u[cur] = 0; pm[cur] = 0; paint(); persist(st); };
    $1('#pzUndo', el).onclick = () => { const x = undo.pop(); if (!x) { T('Nothing to undo'); return; } [cur, u[x[0]], pm[x[0]]] = [x[0], x[1], x[2]]; paint(); persist(st); };
    $1('#pzHint', el).onclick = () => { if (st.done) return; let i = cur; if (given[i] || u[i] === p.solution[i]) i = u.findIndex((v, j) => v !== p.solution[j]); if (i < 0) return; if (!charge(st, 2, `Revealed ${lab(p.solution[i])}`)) return; cur = i; u[i] = p.solution[i]; pm[i] = 0; shown.add(i); S('coin'); paint(); check(); };
    const mv = (dy, dx) => { const r = (Math.floor(cur / n) + dy + n) % n, c = (cur % n + dx + n) % n; cur = r * n + c; paint(); focusCur(); announce(`Row ${r + 1}, column ${c + 1}: ${u[cur] ? lab(u[cur]) : 'empty'}`); };
    st.key = e => {
      if (/^[1-9]$/.test(e.key) && +e.key <= n) { setV(+e.key); return true; }
      if (/^(Backspace|Delete|0)$/.test(e.key)) { $1('#pzErase', el).click(); return true; }
      if (e.key === 'ArrowRight') { mv(0, 1); return true; } if (e.key === 'ArrowLeft') { mv(0, -1); return true; } if (e.key === 'ArrowDown') { mv(1, 0); return true; } if (e.key === 'ArrowUp') { mv(-1, 0); return true; }
      if (e.key === 'p' || e.key === 'P') { $1('#pzPen', el).click(); return true; }
      if ((e.key === 'z' || e.key === 'u') && !e.shiftKey) { $1('#pzUndo', el).click(); return true; }
      return false;
    };
    st.speech = () => { const r = Math.floor(cur / n), c = cur % n, left = u.filter(v => !v).length; return `${set ? 'Concept sudoku' : 'Sudoku'}, ${n} by ${n}, ${p.diff}. ${set ? 'Symbols: ' + set.items.map((it, k) => `${k + 1} is ${it.label}`).join(', ') + '. ' : ''}${left} empty cells. Row ${r + 1}, column ${c + 1}: ${u[cur] ? lab(u[cur]) : 'empty'}. Type 1 to ${n}. Arrow keys move. P switches pencil marks.`; };
    paint();
  }

  /* ---------- ➕ KAKURO ---------- */
  function storyOf(inf, p) {
    if (!inf || !inf.numeric) return '';
    const k = String(inf.key || '');
    if (/-p1-|accountancy/.test(k)) return '🧾 <b>Ledger story:</b> each across clue is one day\'s cash-book total and each down clue is one account\'s total for the week (₹ thousands). Every entry is ₹1–9 thousand and never repeats inside one total.';
    if (/-p3-/.test(k)) return '📊 <b>Data story:</b> each clue is a total of observations — like a frequency table, a row or column must add up exactly. Values are 1–9 and never repeat inside one total.';
    if (/economics/.test(k)) return '💹 <b>Market story:</b> each across clue is a day\'s units sold and each down clue is one stall\'s total. Every number is 1–9 and never repeats inside one total.';
    return '🧮 <b>Number story:</b> each across clue is a row total and each down clue is a column total, like checking sums in your maths book. Use 1–9, no repeats inside one total.';
  }
  function playKAK(el, st, saved) {
    const p = st.p, H = p.h, Wd = p.w, N = H * Wd, given = p.given || new Array(N).fill(0), u = new Array(N).fill(0), pm = new Array(N).fill(0), undo = [], shown = new Set();
    for (let i = 0; i < N; i++) if (given[i]) u[i] = given[i];
    if (saved && saved.u) saved.u.forEach((v, i) => { if (p.cells[i] && !given[i] && v >= 0 && v <= 9) u[i] = v; });
    if (saved && saved.pm) saved.pm.forEach((v, i) => { pm[i] = v | 0; });
    if (saved && saved.shown) saved.shown.forEach(i => shown.add(i));
    st.getState = () => ({ u: u.slice(), pm: pm.slice(), shown: [...shown] });
    const clueA = {}, clueD = {}, runOf = {}; p.runs.forEach((r, k) => { (r.dir === 'A' ? clueA : clueD)[r.clue] = r.sum; r.cells.forEach(i => { (runOf[i] = runOf[i] || {})[r.dir] = k; }); });
    let cur = p.cells.findIndex((v, i) => v && !given[i]); let pencil = false;
    const story = storyOf(st.extra.info, p);
    el.innerHTML = `<div class="pz-root pz-kak" data-pz="kak">${header(st, '➕ Kakuro', `${H}×${Wd} · ${p.diff} · each run adds up to its clue, digits 1–9 never repeat in a run`)}
      ${story ? `<div class="card pz-story">${story}</div>` : ''}
      <div class="pz-gridwrap"><div class="pz-kgrid" id="pzGrid" role="grid" aria-label="Kakuro, ${Wd} by ${H}. Arrow keys move; type 1 to 9; P switches pencil marks." style="--w:${Wd}">
        ${Array.from({ length: H }, (_, y) => `<div role="row" class="pz-row">${Array.from({ length: Wd }, (_, x) => { const i = y * Wd + x; if (p.cells[i]) return `<div role="gridcell" class="pz-k1${given[i] ? ' giv' : ''}" data-i="${i}" tabindex="-1"></div>`; const a = clueA[i], d = clueD[i]; return `<div role="gridcell" class="pz-kc${a || d ? ' clue' : ''}" data-c="${i}" aria-label="${a || d ? `Clue${a ? ': across ' + a : ''}${d ? (a ? ',' : ':') + ' down ' + d : ''}` : 'Blocked'}">${d ? `<span class="kd">${d}</span>` : ''}${a ? `<span class="ka">${a}</span>` : ''}</div>`; }).join('')}</div>`).join('')}
      </div></div>
      <div class="pz-pad n9" role="group" aria-label="Numbers">${Array.from({ length: 9 }, (_, k) => `<button class="pz-num" data-v="${k + 1}"><span>${k + 1}</span></button>`).join('')}</div>
      <div class="pz-tools"><button class="pz-tb" id="pzPen" aria-pressed="false">✏️ Pencil</button><button class="pz-tb" id="pzErase">⌫ Erase</button><button class="pz-tb" id="pzUndo">↶ Undo</button><button class="pz-tb" id="pzHint">💡 Reveal <small>2⭐</small></button></div>
      <p class="note">Tip: a run of 2 adding to 3 can only be 1 + 2; a run of 2 adding to 17 can only be 8 + 9.</p></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el);
    const errors = () => {
      const bad = new Set(), badClue = new Set();
      p.runs.forEach(r => {
        const vs = r.cells.map(i => u[i]), f = vs.filter(Boolean), sum = f.reduce((a, b) => a + b, 0), m = {};
        r.cells.forEach(i => { if (u[i]) (m[u[i]] = m[u[i]] || []).push(i); }); Object.values(m).forEach(a => { if (a.length > 1) a.forEach(i => bad.add(i)); });
        const empty = vs.length - f.length;
        if ((empty === 0 && sum !== r.sum) || (empty > 0 && sum + empty > r.sum)) { badClue.add(r.clue + r.dir); r.cells.forEach(i => { if (u[i]) bad.add(i); }); }
      });
      return { bad, badClue };
    };
    const paint = () => {
      const { bad, badClue } = errors();
      $$('.pz-k1', grid).forEach(c => {
        const i = +c.dataset.i, v = u[i], r = Math.floor(i / Wd), col = i % Wd, ro = runOf[i] || {};
        c.innerHTML = v ? `<span class="pz-v">${v}</span>` : pm[i] ? `<span class="pz-pm k">${Array.from({ length: 9 }, (_, k) => (pm[i] >> k) & 1 ? `<i>${k + 1}</i>` : '<i></i>').join('')}</span>` : '';
        c.classList.toggle('cur', i === cur); c.classList.toggle('bad', bad.has(i)); c.classList.toggle('rev', shown.has(i));
        const inRun = (ro.A != null && runOf[cur] && runOf[cur].A === ro.A) || (ro.D != null && runOf[cur] && runOf[cur].D === ro.D);
        c.classList.toggle('peer', i !== cur && !!inRun); c.tabIndex = i === cur ? 0 : -1;
        const ra = ro.A != null ? p.runs[ro.A] : null, rd = ro.D != null ? p.runs[ro.D] : null;
        c.setAttribute('aria-label', `Row ${r + 1}, column ${col + 1}: ${v || 'empty'}${given[i] ? ', given' : ''}. Across total ${ra ? ra.sum + ' in ' + ra.cells.length + ' cells' : '-'}, down total ${rd ? rd.sum + ' in ' + rd.cells.length + ' cells' : '-'}${bad.has(i) ? '. Problem in this run' : ''}`);
        c.setAttribute('aria-selected', String(i === cur));
      });
      $$('.pz-kc.clue', grid).forEach(c => { const i = +c.dataset.c; c.classList.toggle('badA', badClue.has(i + 'A')); c.classList.toggle('badD', badClue.has(i + 'D')); });
      $1('#pzPen', el).classList.toggle('on', pencil); $1('#pzPen', el).setAttribute('aria-pressed', String(pencil));
    };
    const focusCur = () => { const c = grid.querySelector(`[data-i="${cur}"]`); if (c && D.activeElement && D.activeElement.closest && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const check = () => { persist(st); const full = p.cells.every((v, i) => !v || u[i]); if (full && !errors().bad.size) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (full) { T('All filled — check the red runs'); S('hmm'); } };
    const setV = v => {
      if (st.done || cur < 0) return; if (given[cur] || shown.has(cur)) { T('That one is given'); S('hmm'); return; }
      undo.push([cur, u[cur], pm[cur]]);
      if (pencil && v) { pm[cur] ^= 1 << (v - 1); u[cur] = 0; S('tap'); paint(); persist(st); return; }
      u[cur] = u[cur] === v ? 0 : v; pm[cur] = 0; S(errors().bad.has(cur) ? 'wrong' : 'tap'); paint(); announce(`${u[cur] || 'cleared'}${errors().bad.has(cur) ? ', problem in this run' : ''}`); check();
    };
    grid.addEventListener('click', e => { const c = e.target.closest('.pz-k1'); if (!c) return; cur = +c.dataset.i; paint(); c.focus({ preventScroll: true }); });
    $$('.pz-num', el).forEach(b => b.onclick = () => setV(+b.dataset.v));
    $1('#pzPen', el).onclick = () => { pencil = !pencil; S('tap'); paint(); };
    $1('#pzErase', el).onclick = () => { if (given[cur] || shown.has(cur)) return; undo.push([cur, u[cur], pm[cur]]); u[cur] = 0; pm[cur] = 0; paint(); persist(st); };
    $1('#pzUndo', el).onclick = () => { const x = undo.pop(); if (!x) { T('Nothing to undo'); return; } cur = x[0]; u[x[0]] = x[1]; pm[x[0]] = x[2]; paint(); persist(st); };
    $1('#pzHint', el).onclick = () => { if (st.done) return; let i = cur; if (given[i] || u[i] === p.solution[i]) i = p.cells.findIndex((v, j) => v && u[j] !== p.solution[j]); if (i < 0) return; if (!charge(st, 2, `Revealed ${p.solution[i]}`)) return; cur = i; u[i] = p.solution[i]; pm[i] = 0; shown.add(i); S('coin'); paint(); check(); };
    const mv = (dy, dx) => { let y = Math.floor(cur / Wd), x = cur % Wd; for (let k = 0; k < N; k++) { y += dy; x += dx; if (x >= Wd) { x = 0; y++; } if (x < 0) { x = Wd - 1; y--; } if (y >= H) y = 0; if (y < 0) y = H - 1; const i = y * Wd + x; if (p.cells[i]) { cur = i; break; } } paint(); focusCur(); };
    st.key = e => {
      if (/^[1-9]$/.test(e.key)) { setV(+e.key); return true; }
      if (/^(Backspace|Delete|0)$/.test(e.key)) { $1('#pzErase', el).click(); return true; }
      if (e.key === 'ArrowRight') { mv(0, 1); return true; } if (e.key === 'ArrowLeft') { mv(0, -1); return true; } if (e.key === 'ArrowDown') { mv(1, 0); return true; } if (e.key === 'ArrowUp') { mv(-1, 0); return true; }
      if (e.key === 'p' || e.key === 'P') { $1('#pzPen', el).click(); return true; }
      if (e.key === 'z' || e.key === 'u') { $1('#pzUndo', el).click(); return true; }
      return false;
    };
    st.speech = () => { const ro = runOf[cur] || {}, ra = ro.A != null ? p.runs[ro.A] : null, rd = ro.D != null ? p.runs[ro.D] : null; return `Kakuro, ${p.diff}. ${story ? story.replace(/<[^>]+>/g, '') + ' ' : ''}Row ${Math.floor(cur / Wd) + 1}, column ${cur % Wd + 1}: ${u[cur] || 'empty'}. Across: ${ra ? ra.cells.length + ' cells adding to ' + ra.sum + ', now ' + ra.cells.map(i => u[i] || 'blank').join(', ') : 'none'}. Down: ${rd ? rd.cells.length + ' cells adding to ' + rd.sum + ', now ' + rd.cells.map(i => u[i] || 'blank').join(', ') : 'none'}. Type 1 to 9. Arrow keys move.`; };
    paint();
  }

  /* ---------- 🔎 WORD SEARCH ---------- */
  function playWS(el, st, saved) {
    const p = st.p, n = p.n, found = new Set(saved && saved.found || []); let a = null, hover = null;
    st.getState = () => ({ found: [...found] });
    const line = (s, e) => { const y0 = Math.floor(s / n), x0 = s % n, y1 = Math.floor(e / n), x1 = e % n, dy = Math.sign(y1 - y0), dx = Math.sign(x1 - x0), L = Math.max(Math.abs(y1 - y0), Math.abs(x1 - x0));
      if (!(y0 === y1 || x0 === x1 || Math.abs(y1 - y0) === Math.abs(x1 - x0))) return null; return Array.from({ length: L + 1 }, (_, k) => (y0 + dy * k) * n + x0 + dx * k); };
    const cellsOfW = w => Array.from({ length: w.a.length }, (_, k) => (w.r + w.dr * k) * n + w.c + w.dc * k);
    el.innerHTML = `<div class="pz-root pz-ws" data-pz="ws">${header(st, '🔎 Word search', `Find ${p.words.length} key words. Tap the first letter, then the last (or drag).`)}
      <div class="pz-gridwrap"><div class="pz-wgrid" id="pzGrid" role="grid" aria-label="Word search, ${n} by ${n} letters" style="--n:${n}">${p.grid.map((row, y) => `<div role="row" class="pz-row">${row.split('').map((c, x) => `<div role="gridcell" class="pz-w" data-i="${y * n + x}" tabindex="${y + x ? -1 : 0}" aria-label="${c}, row ${y + 1}, column ${x + 1}">${c}</div>`).join('')}</div>`).join('')}</div></div>
      <div class="card pz-wl"><h3>Words <small id="pzWc"></small></h3><ul>${p.words.map(w => { const c = p.clues && p.clues[w.a]; return `<li data-w="${w.a}"><b>${w.a}</b>${c ? `<small>${E(c.clue)}</small>` : ''}</li>`; }).join('')}</ul></div></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el);
    const paint = () => {
      const on = new Set(); p.words.forEach(w => { if (found.has(w.a)) cellsOfW(w).forEach(i => on.add(i)); });
      const sel = a != null ? (hover != null ? line(a, hover) || [a] : [a]) : [];
      $$('.pz-w', grid).forEach(c => { const i = +c.dataset.i; c.classList.toggle('got', on.has(i)); c.classList.toggle('sel', sel.includes(i)); });
      $$('.pz-wl li', el).forEach(li => li.classList.toggle('got', found.has(li.dataset.w)));
      $1('#pzWc', el).textContent = `${found.size} of ${p.words.length}`;
    };
    const tryLine = (s, e) => {
      const l = line(s, e); if (!l || l.length < 3) return false;
      const str = l.map(i => p.grid[Math.floor(i / n)][i % n]).join(''), rv = str.split('').reverse().join('');
      const w = p.words.find(w => !found.has(w.a) && (w.a === str || w.a === rv) && (cellsOfW(w).join() === l.join() || cellsOfW(w).reverse().join() === l.join()));
      if (!w) return false;
      found.add(w.a); S('coin'); announce(`Found ${w.a}. ${found.size} of ${p.words.length}.`); persist(st);
      if (found.size === p.words.length) { st.done = true; setTimeout(() => finish(st), 500); }
      return true;
    };
    let down = null, moved = false;
    grid.addEventListener('pointerdown', e => { const c = e.target.closest('.pz-w'); if (!c) return; e.preventDefault(); down = +c.dataset.i; moved = false; if (a == null) { a = down; hover = null; } else hover = down; paint(); try { grid.releasePointerCapture(e.pointerId); } catch (x) {} });
    grid.addEventListener('pointermove', e => { if (down == null) return; const c = D.elementFromPoint(e.clientX, e.clientY); const cc = c && c.closest && c.closest('.pz-w'); if (!cc) return; const i = +cc.dataset.i; if (i !== down) moved = true; if (moved) { if (a == null) a = down; hover = i; paint(); } });
    const up = () => {
      if (down == null) return; const d0 = down; down = null;
      if (moved && a != null && hover != null) { const ok = tryLine(a, hover); if (!ok) S('hmm'); a = null; hover = null; paint(); return; }
      if (a != null && d0 !== a) { const ok = tryLine(a, d0); if (!ok) { S('hmm'); T('Not a word — tap its first letter, then its last'); } a = null; hover = null; }
      paint();
    };
    grid.addEventListener('pointerup', up); grid.addEventListener('pointercancel', () => { down = null; });
    grid.addEventListener('keydown', e => { const c = e.target.closest('.pz-w'); if (!c) return; let i = +c.dataset.i; const m = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: n, ArrowUp: -n }[e.key];
      if (m) { i = Math.max(0, Math.min(n * n - 1, i + m)); const t = grid.querySelector(`[data-i="${i}"]`); t.focus(); c.tabIndex = -1; t.tabIndex = 0; if (a != null) { hover = i; paint(); } e.preventDefault(); }
      else if (e.key === 'Enter' || e.key === ' ') { if (a == null) { a = i; announce(`Start at ${p.grid[Math.floor(i / n)][i % n]}. Move to the last letter and press Enter.`); } else { if (!tryLine(a, i)) announce('Not a word.'); a = null; hover = null; } paint(); e.preventDefault(); } });
    st.speech = () => `Word search, ${n} by ${n}. Find: ${p.words.filter(w => !found.has(w.a)).map(w => w.a).join(', ')}. Found ${found.size} of ${p.words.length}. Use the arrow keys and Enter on the first and last letter.`;
    paint();
  }

  /* ---------- 🔤 ANAGRAM ---------- */
  function playAN(el, st, saved) {
    const p = st.p; let k = saved && saved.k || 0, got = saved && saved.got || 0, skipped = saved && saved.skipped || 0, pick = [];
    st.getState = () => ({ k, got, skipped });
    const draw = () => {
      if (k >= p.words.length) { st.done = true; st.pool = Math.max(0, st.pool - skipped * 2); return finish(st, { line: `${got} of ${p.words.length} unscrambled` }); }
      const w = p.words[k]; pick = [];
      el.innerHTML = `<div class="pz-root pz-an" data-pz="an">${header(st, '🔤 Anagram', `Word ${k + 1} of ${p.words.length}`)}
        <div class="card pz-anc"><p class="pz-ctx">${w.ctx ? E(w.ctx) : 'Clue'}</p><h2 class="pz-anq">${E(w.clue)} <span class="pz-enum">${E(w.enum)}</span></h2>
          <div class="pz-slots" aria-live="polite">${w.a.split('').map((_, j) => `<span class="pz-slot" data-j="${j}"></span>`).join('')}</div>
          <div class="pz-tiles">${w.s.split('').map((c, j) => `<button class="pz-lt" data-j="${j}" aria-label="${c}">${c}</button>`).join('')}</div>
          <div class="pz-tools"><button class="pz-tb" id="pzAnBack">⌫ Undo letter</button><button class="pz-tb" id="pzAnSkip">⏭ Show answer <small>−2⭐</small></button></div></div></div>`;
      wireQuit(el, st);
      const slots = $$('.pz-slot', el), tiles = $$('.pz-lt', el);
      const paint = () => { slots.forEach((s, j) => { s.textContent = pick[j] != null ? w.s[pick[j]] : ''; }); tiles.forEach(t => { t.disabled = pick.includes(+t.dataset.j); }); };
      const chk = () => {
        if (pick.length < w.a.length) return;
        const ans = pick.map(j => w.s[j]).join('');
        if (ans === w.a) { got++; S('correct'); slots.forEach(s => s.classList.add('ok')); announce(`Correct: ${w.a}`); k++; persist(st); setTimeout(draw, 800); }
        else { S('wrong'); $1('.pz-slots', el).classList.add('shake'); announce('Not quite. Try again.'); setTimeout(() => { pick = []; paint(); const s = $1('.pz-slots', el); if (s) s.classList.remove('shake'); }, 600); }
      };
      tiles.forEach(t => t.onclick = () => { if (pick.includes(+t.dataset.j) || pick.length >= w.a.length) return; pick.push(+t.dataset.j); S('tap'); paint(); chk(); });
      $1('#pzAnBack', el).onclick = () => { pick.pop(); paint(); };
      $1('#pzAnSkip', el).onclick = () => { skipped++; slots.forEach((s, j) => { s.textContent = w.a[j]; s.classList.add('rev'); }); announce(`The answer is ${w.a}`); S('hmm'); k++; persist(st); setTimeout(draw, 1400); };
      st.key = e => { if (/^[a-zA-Z]$/.test(e.key)) { const L = e.key.toUpperCase(), t = tiles.find(t => !t.disabled && t.textContent === L); if (t) t.click(); return true; } if (e.key === 'Backspace') { $1('#pzAnBack', el).click(); return true; } return false; };
      st.speech = () => `Anagram ${k + 1} of ${p.words.length}. Clue: ${w.clue}. ${w.a.length} letters. Letters: ${w.s.split('').join(', ')}. Type the letters in order.`;
      paint();
    };
    draw();
  }

  /* ================= results, stars, badges, daily streak ================= */
  const BADGES = [
    ['pzFirst', '🧩', 'First puzzle', z => z.total >= 1],
    ['pzMaster', '🧩', 'Puzzle Master: 25 solved', z => z.total >= 25],
    ['pzDaily3', '📅', 'Daily streak: 3 days', z => (z.daily.best || 0) >= 3],
    ['pzDaily7', '🗓️', 'Daily streak: 7 days', z => (z.daily.best || 0) >= 7],
    ['pzXw5', '📝', 'Crossword Ace: 5 crosswords', z => (z.solved.xw || 0) >= 5],
    ['pzSdkHard', '🔢', 'Sudoku Sensei: hard 9×9', z => !!z.flags.sdkHard9],
    ['pzKak3', '➕', 'Kakuro Whiz: 3 kakuros', z => (z.solved.kak || 0) >= 3],
    ['pzNoHint', '🎯', 'Sharp Mind: 10 without hints', z => (z.nohint || 0) >= 10],
    ['pzSpeed', '⚡', 'Speed Solver: 9×9 under 10 min', z => !!z.flags.fast9],
    ['pzAll', '🌈', 'All-rounder: every puzzle type', z => ['xw', 'sdk', 'csdk', 'kak', 'ws', 'an'].every(k => z.solved[k])]];
  const badgeGrid = () => { const z = Z(); return `<div class="bgrid pz-bgrid">${BADGES.map(([id, e, n]) => `<div class="bdg ${z.badges[id] ? 'on' : ''}"><b aria-hidden="true">${e}</b><span>${E(n)}</span><span class="sr-only">${z.badges[id] ? 'earned' : 'not yet'}</span></div>`).join('')}</div>`; };
  const bestKey = (sp, p) => sp.t === 'sdk' || sp.t === 'csdk' ? `${sp.t}${p.n}-${p.diff}` : sp.t === 'kak' ? `kak-${p.diff}` : sp.t;
  const BEST_N = { xw: '📝 Crossword', sdk4: '🔢 Sudoku 4×4', sdk6: '🔢 Sudoku 6×6', sdk9: '🔢 Sudoku 9×9', csdk4: '🧠 Concept 4×4', csdk6: '🧠 Concept 6×6', kak: '➕ Kakuro', ws: '🔎 Word search', an: '🔤 Anagram' };
  function bestList() {
    const b = Z().best, ks = Object.keys(b).sort(); if (!ks.length) return '<p class="sub">Best times appear here once you solve a puzzle.</p>';
    return `<h3 style="margin-top:10px">⏱ Best times</h3><div class="pz-best">${ks.map(k => { const m = /^([a-z]+?)(\d*)-?([a-z]*)$/.exec(k) || []; return `<span>${E(BEST_N[(m[1] || k) + (m[2] || '')] || BEST_N[m[1]] || k)}${m[3] ? ' · ' + E(m[3]) : ''} <b>${fmtT(b[k])}</b></span>`; }).join('')}</div>`;
  }
  function finish(st, o) {
    if (st.finished) return; st.finished = true; o = o || {};
    const z = Z(), sp = st.sp, p = st.p, first = !z.done[st.id];
    delete z.saves[st.id];
    let stars = first ? Math.max(0, st.pool) : 0, dailyMsg = '';
    const lines = [];
    if (first) {
      z.done[st.id] = localISO(); const dk = Object.keys(z.done); if (dk.length > 300) dk.slice(0, dk.length - 300).forEach(k => delete z.done[k]);
      z.total++; z.solved[sp.t] = (z.solved[sp.t] || 0) + 1; if (!st.hints) z.nohint++;
      if ((sp.t === 'sdk') && p.n === 9 && p.diff === 'hard') z.flags.sdkHard9 = 1;
      if ((sp.t === 'sdk') && p.n === 9 && st.secs < 600) z.flags.fast9 = 1;
    }
    const bk = bestKey(sp, p), isBest = sp.t !== 'an' && (!z.best[bk] || st.secs < z.best[bk]);
    if (isBest && sp.t !== 'an') z.best[bk] = st.secs;
    if (sp.daily && sp.daily === localISO() && !z.daily.hist[sp.daily]) {
      const d = z.daily; d.n = d.last === yISO() ? d.n + 1 : 1; d.last = sp.daily; d.best = Math.max(d.best || 0, d.n); d.hist[sp.daily] = sp.t;
      const hk = Object.keys(d.hist).sort(); if (hk.length > 60) hk.slice(0, hk.length - 60).forEach(k => delete d.hist[k]);
      const bonus = 10 + Math.min(d.n, 7); stars += bonus; dailyMsg = `📅 Daily puzzle done · 🔥 ${d.n}-day puzzle streak · +${bonus} ⭐ bonus`;
      try { bumpStreak(); } catch (e) {}
    }
    const fresh = [];
    BADGES.forEach(([id, e, n, ok]) => { if (!z.badges[id] && ok(z)) { z.badges[id] = localISO(); fresh.push(`${e} ${n}`); } });
    try { save(); } catch (e) {}
    if (stars > 0) addXP(stars, 'Puzzle solved!'); else { try { hud(); } catch (e) {} }
    if (fresh.length) setTimeout(() => { S('unlock'); T(`🏅 New badge: ${fresh[0]}`); }, 1500);
    if (st.hints) lines.push(`💡 ${st.hints} hint${st.hints > 1 ? 's' : ''} used${st.spent ? ` (${st.spent} ⭐ from your stars)` : ''}`);
    if (o.line) lines.push(o.line);
    stopPlay();
    const el = screen(); const nav = D.querySelector('nav'); if (nav) nav.style.display = '';
    const m = TYPES[sp.t];
    el.innerHTML = `<div class="pz-root pz-res" data-pz="res"><div class="card done-card pz-rescard"><div class="confetti">${Array.from({ length: 14 }, (_, j) => `<span style="left:${(j * 7.3 + 3) % 100}%;animation-delay:${(j % 5) * .15}s">${['🎉', '⭐', '✨', '🧩'][j % 4]}</span>`).join('')}</div>
      <div class="pz-rese" aria-hidden="true">${m.e}</div><h2>Solved!</h2><p class="pz-resn">${m.n}${p.n ? ` ${p.n}×${p.n}` : ''}${p.diff ? ' · ' + E(p.diff) : ''}</p>
      ${sp.t !== 'an' ? `<div class="pz-rest"><span>⏱ <b>${fmtT(st.secs)}</b></span>${isBest ? '<span class="pz-best1">🏆 Best time!</span>' : `<span>Best ${fmtT(z.best[bk])}</span>`}</div>` : ''}
      <div class="arc-xp">${first ? `+${stars} ⭐` : 'Already solved — stars were given the first time'}</div>
      ${dailyMsg ? `<p class="sub">${E(dailyMsg)}</p>` : ''}${lines.map(l => `<p class="sub">${E(l)}</p>`).join('')}
      ${fresh.length ? `<p class="pz-newb">🏅 ${fresh.map(E).join(' · ')}</p>` : ''}
      ${sp.t === 'xw' ? `<details class="pz-recap"><summary>📖 Review the words</summary><ul>${p.entries.map(e => `<li><b>${E(e.disp || e.a)}</b> — ${E(e.clue)}</li>`).join('')}</ul></details>` : ''}
      <button class="btn mint" id="pzAgain">🧩 New ${E(m.n.toLowerCase())}</button><div style="height:8px"></div>
      <button class="btn ghost" id="pzHome">${sp.sc && sp.sc.k !== 'q' && !sp.daily ? 'Back to this chapter\'s puzzles' : 'Back to puzzles'}</button></div></div>`;
    S('unlock');
    $1('#pzAgain').onclick = () => { S('tap'); const k = scopeKey(sp.sc); play(Object.assign({}, sp, { seed: nextSeed(k, sp.t), daily: null })); };
    $1('#pzHome').onclick = () => { S('tap'); if (sp.sc && sp.sc.k !== 'q' && !sp.daily) chapter(sp.sc, sp.from || { t: 'hub' }); else hub(); };
    announce(`Solved! ${sp.t !== 'an' ? 'Time ' + fmtT(st.secs) + '. ' : ''}${first ? stars + ' stars.' : ''} ${dailyMsg}`);
  }

  /* ================= keys (physical keyboard) ================= */
  D.addEventListener('keydown', e => {
    if (!PLAY || !PLAY.key || PLAY.done || e.ctrlKey || e.metaKey || e.altKey) return;
    const s = D.getElementById('s-puz'); if (!s || !s.classList.contains('active')) return;
    const a = D.activeElement; if (a && (/^(input|textarea|select)$/i.test(a.tagName) || a.isContentEditable)) return;
    if (D.querySelector('.sheet.show, .asksheet.show')) return;
    if (a && a.tagName === 'BUTTON' && (e.key === 'Enter' || e.key === ' ') && !a.closest('#pzGrid')) return;   // let buttons work
    if (e.key === 'Tab') return;                                                  // Tab always moves focus (never trapped in the grid)
    if (PLAY.key(e)) { e.preventDefault(); e.stopPropagation(); }
  }, true);

  /* ================= Listen mode / screen readers ================= */
  function speech(r) {
    if (PLAY && PLAY.speech && $1('[data-pz]', r) && !$1('.pz-res', r)) { try { return PLAY.speech(); } catch (e) { return ''; } }
    const res = $1('.pz-res', r); if (res) return `${res.querySelector('h2').textContent}. ${[...res.querySelectorAll('.pz-resn,.pz-rest,.arc-xp,.sub')].map(x => x.textContent).join('. ')}. Buttons: new puzzle, or back.`;
    const h = $1('.hello,h2', r), games = $$('.pz-game', r).map(b => `${b.querySelector('b').textContent}: ${b.querySelector('small').textContent}`);
    const dl = $1('#pzDaily h2', r);
    return `${h ? h.textContent : 'Puzzles'}. ${dl ? 'Daily puzzle: ' + dl.textContent + '. ' : ''}${games.length ? 'Puzzles: ' + games.join('. ') + '.' : ''} Use Tab to move between buttons.`;
  }

  /* ================= entry points ================= */
  function tileHTML(dark) {
    const n = dailyLive(), done = Z().daily.hist[localISO()];
    return `<button type="button" class="card pz-tile${dark ? ' dark' : ''}" data-pztile="1"><span class="pz-tile-e" aria-hidden="true">🧩</span><span class="pz-tile-t"><b>Puzzles</b><small>${done ? '✓ Daily puzzle solved' : 'Daily puzzle ready'} · crosswords, sudoku, kakuro${n ? ` · 🔥 ${n}` : ''}</small></span><span class="pz-tile-go" aria-hidden="true">›</span></button>`;
  }
  function place() {
    { const ps = D.getElementById('s-puz'); D.documentElement.classList.toggle('pz-playing', !!(ps && ps.classList.contains('active') && ps.querySelector('[data-pz]:not([data-pz="res"])'))); }   // floating Ask / calculator buttons would cover the grid or keyboard
    const s0 = STx(); if (!s0 || !s0.profile) return;
    try { if (window.Cloud && Cloud.isParent && Cloud.isParent()) return; } catch (e) {}
    const put = (host, ref, where, html, sel, fn) => { if (!host || !ref || host.querySelector(sel)) return; ref.insertAdjacentHTML(where, html); const b = host.querySelector(sel); if (b) b.onclick = () => { S('open'); fn(); }; };
    const act = id => { const e = D.getElementById(id); return e && e.classList.contains('active') ? e : null; };
    let w;
    if ((w = act('s-world')) && !isCA()) { const map = D.getElementById('map'); if (map) put(w, map, 'beforebegin', tileHTML(), '[data-pztile]', () => hub({ from: 'world' })); }
    if ((w = act('s-practice')) && !isCA()) { const ref = w.querySelector(':scope > [data-lvtile]') || w.querySelector(':scope > .goalcard'); if (ref) put(w, ref, 'afterend', tileHTML(), '[data-pztile]', () => hub({ from: 'practice' })); }
    if ((w = act('s-chapter')) && !isCA()) {
      const nv = (() => { try { return NAV; } catch (e) { return {}; } })();
      const row = w.querySelector('.ch-btns'), sid = nv.subject, ci = nv.chapter;
      if (sid != null && ci != null) { if (row) put(w, row, 'beforeend', '<button id="chPuz" data-pzch="1">🧩 Puzzles</button>', '[data-pzch]', () => chapter({ k: 's', g: +ST.profile.grade, sid, ci }, { t: 'chapter', sid, ci })); }
    }
    if ((w = act('s-topic')) && !isCA()) {
      const dc = w.querySelector('.done-card #dBack'), run = (() => { try { return RUN; } catch (e) { return null; } })();
      if (dc && run) put(w, dc, 'beforebegin', '<button class="btn ghost" data-pzdone="1">🧩 Puzzle this chapter</button><div style="height:8px"></div>', '[data-pzdone]', () => chapter({ k: 's', g: +ST.profile.grade, sid: run.sid, ci: run.ci }, { t: 'chapter', sid: run.sid, ci: run.ci }));
    }
    if ((w = act('s-ca')) && isCA()) {
      const mot = w.querySelector(':scope > .ca-mot');
      if (mot && w.querySelector('.ca-journey')) { const ref = w.querySelector(':scope > [data-lvtile]') || mot; put(w, ref, 'afterend', tileHTML(true), '[data-pztile]', () => hub({ from: 'ca' })); }
      const hubs = w.querySelector(':scope > .ca-hubs');
      if (hubs) put(w, hubs, 'beforeend', `<button class="card ca-hub" data-pzhub="1"><b class="ca-hube" aria-hidden="true">🧩</b><span><b>Puzzles</b><small>Daily puzzle, chapter crosswords, Sudoku, Kakuro</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`, '[data-pzhub]', () => hub({ from: 'ca-practice' }));
      const ua = w.querySelector('.ca-uhead .ca-uacts');
      if (ua) { const x = X(), uid = x && x.C().last; if (uid) put(w, ua, 'beforeend', '<button class="ca-link" data-pzunit="1">🧩 Puzzles</button>', '[data-pzunit]', () => chapter({ k: 'c', ch: uid.replace(/-u\d+$/, '') }, { t: 'unit', uid })); }
    }
  }

  /* ================= styles ================= */
  function style() {
    if (D.getElementById('pzCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="pzCss">
.pz-tile{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;font:inherit;color:var(--ink);padding:12px 14px}
.pz-tile.dark{background:#1d2128;color:#fff}.pz-tile-e{font-size:30px}.pz-tile-t{flex:1;display:flex;flex-direction:column}.pz-tile-t b{font-family:'Baloo 2';font-size:18px}.pz-tile-t small{opacity:.8;font-size:12.5px}.pz-tile-go{font-size:26px;opacity:.5}
.pz-root .hello small{display:block}
.pz-games{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0 12px}
.pz-game{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;border:0;border-radius:18px;padding:12px;background:var(--card);color:var(--ink);box-shadow:0 6px 18px rgba(0,0,0,.16);cursor:pointer;font:inherit;min-height:104px}
.pz-game b{font-family:'Baloo 2';font-size:16px;line-height:1.1}.pz-game small{font-size:12px;color:var(--muted);line-height:1.3}.pz-ge{font-size:26px}
.pz-g-xw{background:#fff7e0}.pz-g-sdk{background:#e9f0ff}.pz-g-csdk{background:#f3e9ff}.pz-g-kak{background:#e6fbf3}.pz-g-ws{background:#fff0ee}.pz-g-an{background:#eef7ff}
.card .pz-games .pz-game{box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.pz-prefs small{display:block;font-weight:800;font-size:12px;color:var(--muted);margin-top:6px}
.pz-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}.pz-chip{border:0;border-radius:999px;padding:7px 11px;background:#eef0fb;color:var(--ink);font:700 13px Nunito,sans-serif;cursor:pointer;min-height:34px}.pz-chip.on{background:var(--violet);color:#fff}
.pz-daily .pz-dh{display:flex;gap:10px;align-items:flex-start}.pz-de{font-size:34px}.pz-streak{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 10px;font-size:13px;font-weight:700}.pz-ok{color:#0a7d55}
.pz-subj{border-top:1px solid rgba(0,0,0,.07);padding:8px 0}.pz-subj summary{cursor:pointer;display:flex;flex-direction:column;list-style:none}.pz-subj summary::-webkit-details-marker{display:none}.pz-subj summary small{color:var(--muted);font-size:12px}
.pz-chl{display:flex;flex-direction:column;gap:6px;margin-top:8px}.pz-chb{display:flex;gap:8px;align-items:center;text-align:left;border:0;border-radius:12px;padding:9px 10px;background:#f4f5fb;color:var(--ink);font:600 14px Nunito,sans-serif;cursor:pointer}.pz-chb span{min-width:24px;height:24px;border-radius:8px;background:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:12px}
.pz-stats{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;margin-top:8px}.pz-best{display:flex;flex-wrap:wrap;gap:6px}.pz-best span{background:#f4f5fb;border-radius:10px;padding:5px 8px;font-size:12.5px}
.pz-chead{display:flex;gap:12px;align-items:center}.pz-ce{font-size:38px}
.pz-genc{text-align:center;padding:30px 16px}.pz-spin{font-size:40px;animation:pzSpin 1.2s linear infinite;display:inline-block}@keyframes pzSpin{to{transform:rotate(360deg)}}
.pz-bar{display:flex;align-items:center;gap:8px;color:#fff;margin:2px 0 4px}.pz-x{border:0;background:rgba(255,255,255,.14);color:#fff;border-radius:999px;padding:8px 12px;font:700 13px Nunito,sans-serif;cursor:pointer;min-height:36px}
.pz-title{flex:1;font-family:'Baloo 2';font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pz-time,.pz-prize{background:rgba(255,255,255,.14);border-radius:999px;padding:5px 9px;font-weight:800;font-size:13px;font-variant-numeric:tabular-nums}
.pz-sub{color:#fff;opacity:.85;font-size:12.5px;margin:0 2px 6px}
.pz-gridwrap{background:var(--card);border-radius:16px;padding:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);margin-bottom:8px;overflow-x:auto}
.pz-row{display:flex}
.pz-xgrid{display:flex;flex-direction:column;width:min(100%, calc(var(--w) * 34px));margin:0 auto}
.pz-xgrid .pz-c{flex:1 1 0;aspect-ratio:1;position:relative;border:1px solid #2b2f48;margin:0 -1px -1px 0;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;font:800 clamp(13px,4.2vw,19px) 'Baloo 2',sans-serif;color:#1b1f3a;text-transform:uppercase;outline:none;min-width:0}
.pz-xgrid .pz-c.blk{background:transparent;border-color:transparent;cursor:default}
.pz-xgrid .pz-n{position:absolute;top:0;left:2px;font:700 9px Nunito,sans-serif;color:#555}
.pz-xgrid .pz-c.word{background:#fff3c4}.pz-xgrid .pz-c.cur{background:#ffc93c}.pz-xgrid .pz-c.rev .pz-l{color:#7646ea}.pz-xgrid .pz-c.bad .pz-l{color:#d62828;text-decoration:line-through}
.pz-c:focus-visible,.pz-s:focus-visible,.pz-k1:focus-visible,.pz-w:focus-visible{box-shadow:inset 0 0 0 3px #2563eb}
.pz-cluebar{background:#fff;border-radius:14px;padding:9px 12px;margin-bottom:8px;font-size:14.5px;line-height:1.35;min-height:44px;box-shadow:0 4px 14px rgba(0,0,0,.14)}
.pz-ctx{color:var(--muted);font-size:12.5px}.pz-enum{color:var(--muted);font-weight:800;white-space:nowrap}.pz-near{color:#7646ea;font-weight:800}
.pz-tools{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 8px}.pz-tb{flex:1 1 auto;border:0;border-radius:12px;padding:9px 10px;background:#eef0fb;color:var(--ink);font:700 13px Nunito,sans-serif;cursor:pointer;min-height:40px}.pz-tb small{opacity:.7}.pz-tb.on{background:var(--violet);color:#fff}
.pz-kb{display:flex;flex-direction:column;gap:5px;margin-bottom:10px;user-select:none}.pz-kr{display:flex;gap:4px;justify-content:center}
.pz-k{flex:1 1 0;max-width:40px;min-height:44px;border:0;border-radius:9px;background:#fff;color:#1b1f3a;font:800 16px 'Baloo 2',sans-serif;box-shadow:0 2px 0 #c9cde4;cursor:pointer;padding:0}.pz-k.wide{max-width:64px;flex:1.6 1 0;font-size:13px;background:#dfe3f6}.pz-k:active{transform:translateY(2px);box-shadow:none}
.pz-clues ol{list-style:none;margin:0 0 8px;padding:0}.pz-cl{width:100%;text-align:left;border:0;background:none;padding:7px 6px;border-radius:10px;font:500 14px/1.35 Nunito,sans-serif;color:var(--ink);cursor:pointer}.pz-cl b{display:inline-block;min-width:22px}.pz-cl.on{background:#fff3c4}
.pz-sgrid{display:flex;flex-direction:column;width:min(100%, calc(var(--n) * 46px));margin:0 auto;border:3px solid #1b1f3a;border-radius:6px;overflow:hidden}
.pz-s{flex:1 1 0;aspect-ratio:1;border-right:1px solid #b8bdd6;border-bottom:1px solid #b8bdd6;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;outline:none;min-width:0;position:relative}
.pz-s.br{border-right:3px solid #1b1f3a}.pz-s.bb{border-bottom:3px solid #1b1f3a}.pz-sgrid .pz-row:last-child .pz-s{border-bottom:0}.pz-sgrid .pz-s:last-child{border-right:0}
.pz-s .pz-v,.pz-k1 .pz-v{font:800 clamp(16px,5.5vw,24px) 'Baloo 2',sans-serif;color:#2563eb;line-height:1}.pz-s.giv .pz-v,.pz-k1.giv .pz-v{color:#1b1f3a}.pz-s.rev .pz-v,.pz-k1.rev .pz-v{color:#7646ea}
.pz-sgrid.n4 .pz-v{font-size:clamp(22px,8vw,32px)}.pz-csdk .pz-v{font-size:clamp(16px,6vw,26px)}.pz-vl{font-size:8.5px;color:#555;line-height:1;margin-top:1px;max-width:100%;overflow:hidden;white-space:nowrap}
.pz-s.peer,.pz-k1.peer{background:#f0f3ff}.pz-s.same{background:#e1e8ff}.pz-s.cur,.pz-k1.cur{background:#ffe08a}.pz-s.bad .pz-v,.pz-k1.bad .pz-v{color:#d62828}.pz-s.bad,.pz-k1.bad{box-shadow:inset 0 0 0 2px #ff6b6b}
.pz-pm{display:grid;grid-template-columns:repeat(3,1fr);width:100%;height:100%;padding:1px}.pz-sgrid.n4 .pz-pm{grid-template-columns:repeat(2,1fr)}.pz-pm i{font:700 9px Nunito,sans-serif;color:#667;display:flex;align-items:center;justify-content:center;font-style:normal}
.pz-pad{display:grid;gap:6px;margin:6px 0}.pz-pad.n4{grid-template-columns:repeat(4,1fr)}.pz-pad.n6{grid-template-columns:repeat(6,1fr)}.pz-pad.n9{grid-template-columns:repeat(9,1fr)}
.pz-num{border:0;border-radius:12px;background:#fff;color:#1b1f3a;font:800 20px 'Baloo 2',sans-serif;min-height:48px;box-shadow:0 3px 0 #c9cde4;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2px;min-width:0}.pz-num small{font:700 9.5px Nunito,sans-serif;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pz-legend ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px}.pz-legend li{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}.pz-legend small{flex-basis:100%;color:var(--muted);font-size:12px;padding-left:30px}.pz-sym{font-size:20px;width:22px}
.pz-kgrid{display:flex;flex-direction:column;width:min(100%, calc(var(--w) * 48px));margin:0 auto;border:2px solid #1b1f3a}
.pz-k1,.pz-kc{flex:1 1 0;aspect-ratio:1;min-width:0;border-right:1px solid #1b1f3a;border-bottom:1px solid #1b1f3a;position:relative}
.pz-k1{background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;outline:none}
.pz-kc{background:#2b2f48}.pz-kc.clue{background:linear-gradient(to top right,#3b4060 calc(50% - 1px),#9aa0c0 50%,#3b4060 calc(50% + 1px))}
.pz-kc .ka,.pz-kc .kd{position:absolute;color:#fff;font:800 clamp(10px,3vw,13px) Nunito,sans-serif}.pz-kc .ka{top:3px;right:4px}.pz-kc .kd{bottom:3px;left:4px}.pz-kc.badA .ka,.pz-kc.badD .kd{color:#ff8f8f}
.pz-pm.k{grid-template-columns:repeat(3,1fr)}
.pz-story{font-size:13.5px;line-height:1.4}
.pz-wgrid{display:flex;flex-direction:column;width:min(100%, calc(var(--n) * 38px));margin:0 auto;touch-action:none;user-select:none}
.pz-w{flex:1 1 0;aspect-ratio:1;display:flex;align-items:center;justify-content:center;font:800 clamp(13px,4.5vw,19px) 'Baloo 2',sans-serif;color:#1b1f3a;border-radius:8px;cursor:pointer;min-width:0;outline:none}.pz-w.got{background:#bdf3dd}.pz-w.sel{background:#ffc93c}
.pz-wl ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:5px}.pz-wl li{display:flex;flex-direction:column}.pz-wl li small{color:var(--muted);font-size:12px}.pz-wl li.got b{text-decoration:line-through;color:#0a7d55}
.pz-anq{font-size:19px;margin:4px 0 12px}.pz-slots{display:flex;gap:5px;justify-content:center;flex-wrap:wrap;margin-bottom:14px}.pz-slot{width:34px;height:40px;border-bottom:3px solid #1b1f3a;display:flex;align-items:center;justify-content:center;font:800 22px 'Baloo 2',sans-serif}.pz-slot.ok{color:#0a7d55}.pz-slot.rev{color:#7646ea}
.pz-tiles{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:10px}.pz-lt{width:42px;height:46px;border:0;border-radius:10px;background:#ffc93c;color:#1b1f3a;font:800 22px 'Baloo 2',sans-serif;box-shadow:0 3px 0 #d39b00;cursor:pointer}.pz-lt:disabled{opacity:.25}
.pz-slots.shake{animation:pzShake .4s}@keyframes pzShake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.pz-rese{font-size:46px}.pz-resn{color:var(--muted);font-weight:700;margin-bottom:6px}.pz-rest{display:flex;justify-content:center;gap:14px;font-size:16px;margin:6px 0}.pz-best1{color:#b7791f;font-weight:800}.pz-newb{font-weight:800;margin:6px 0}
.pz-recap{text-align:left;margin:8px 0 12px}.pz-recap ul{padding-left:18px;font-size:13.5px;line-height:1.45}
.pz-rescard{text-align:center}
html[data-age=pro] .pz-g-xw,html[data-age=pro] .pz-g-sdk,html[data-age=pro] .pz-g-csdk,html[data-age=pro] .pz-g-kak,html[data-age=pro] .pz-g-ws,html[data-age=pro] .pz-g-an{background:#fff}
html[data-age=pro] .pz-xgrid .pz-c.cur,html[data-age=pro] .pz-s.cur,html[data-age=pro] .pz-k1.cur{background:#cfe0ff}html[data-age=pro] .pz-xgrid .pz-c.word{background:#eef3fb}html[data-age=pro] .pz-chip.on{background:#1f5fd1}
@media (prefers-reduced-motion: reduce){.pz-spin{animation:none}}
html.pz-playing #askFab,html.pz-playing #calcFab{display:none!important}
html.sv-hc .pz-c,html.sv-hc .pz-s,html.sv-hc .pz-k1{border-color:#000}html.sv-hc .pz-xgrid .pz-c.cur,html.sv-hc .pz-s.cur,html.sv-hc .pz-k1.cur{background:#ff0;outline:3px solid #000}
</style>`);
  }

  /* ================= boot ================= */
  function boot() {
    style();
    let t = 0;
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) {} }); }).observe(D.querySelector('main') || D.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    place();
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', boot) : boot();
  if (window.Nav) { hub = Nav.route('puz.hub', hub); chapter = Nav.route('puz.chapter', chapter); play = Nav.route('puz.play', play); }
  window.Puzzles = { hub: o => hub(o || {}), chapter: (sc, from) => chapter(sc, from), play: sp => play(sp), daily: async () => play(await dailySpec()), speech, terms, curChapter, dailySpec, _Z: Z, _state: () => PLAY };
})();
