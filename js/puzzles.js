/* ================= Knowtopia Puzzles: chapter puzzles, Sudoku, Kakuro + a daily puzzle (js/puzzles.js) =================
   PUBLIC API (window.Puzzles) — used by the 🎮 Play hub (js/playhub.js) and the live 🧩 Puzzle Race (js/live.js):
     Puzzles.kinds() → [{ id, e, n, d, chapter }]   ids: 'sdk' Sudoku · 'kak' Kakuro · 'xw' Crossword · 'ws' Word search ·
                       'an' Anagram · 'csdk' Concept sudoku ('ana' is accepted everywhere as another name for 'an').
                       chapter: true = built from one chapter's own words (the student picks subject → chapter).
     Puzzles.hub({ from })        the Puzzles screen (daily puzzle, quick play for every kind, badges). from: 'practice' |
                                  'play' | 'world' | 'ca' | 'ca-practice' — where its Back button goes ('play' → PlayHub.open()).
     Puzzles.quick(kind, { from }) picker for that kind (chapter kinds: subject → chapter, default = the chapter the student
                                  is on; difficulty; Sudoku also size), then plays it. Back returns to `from`.
     Puzzles.daily()              plays today's daily puzzle.
     Puzzles.pick(kind) → Promise<spec | null>   the same picker in a bottom sheet, WITHOUT playing (null = cancelled).
                                  spec is plain JSON and self-contained, e.g.
                                  { v: 1, t: 'ws', sc: { k: 's', g: 7, sid: 'hindi', ci: 2 } | { k: 'c', ch: 'fnd-p2-ch02' } | { k: 'q' },
                                    seed: 'race|…', diff: 'easy'|'medium'|'hard'|'expert', n?: 4|6|9, ph: '<puzzle hash>',
                                    label: 'Word search · <chapter> · Medium', kindName, chapterTitle, subjectName }
                                  Any phone (any class, school or CA) rebuilds the exact same puzzle from it.
     Puzzles.race(hostEl, spec, { onSolved({ ms, hints, mistakes }), onQuit(), onProgress({ done, total }), onError?(msg) })
                                  → { stop(), ready: Promise<{ ok, same }> }   renders that exact puzzle inside hostEl (no
                                  screen / nav change). onProgress = cells right / words found so far; onSolved fires once.
                                  No daily streak, badges, best times or saves — only the puzzle's small star prize.
                                  ready.same is false if this phone built a different puzzle (different content version).
     Puzzles.describe(spec) → { ch, d }   a lobby label for a spec.
     Puzzles.build(spec) → Promise<{ p, extra } | null>  (tests / tools)
   WHAT EACH PUZZLE IS MADE OF
     📝 Crossword · 🔎 Word search · 🔤 Anagram · 🧠 Concept sudoku: the chosen chapter's OWN key words (match pairs,
        fill-ins, definitions, quiz answers; CA: quick-reference cards, MCQ stems, key rules). English crosswords may
        borrow a few words from the neighbouring chapters (marked ↗) when the chapter alone is too small.
        Hindi / Sanskrit (any Indic script): words in that script, one AKSHARA per cell / tile (क्ष, स्व, विः stay whole;
        see PuzzleCore.aksharas), clues in the chapter's language, an akshara keyboard for the crossword. If a chapter has
        too few words for a kind, that kind is hidden for the chapter with a kind note — never swapped for another puzzle.
     🔢 Sudoku 4×4 / 6×6 / 9×9 and ➕ Kakuro: general brain games (never offered as a "chapter puzzle"), except Kakuro on a
        maths / accounts / economics chapter, which gets a ledger story.
     📅 Daily Puzzle — one a day from your current chapter (crossword → sudoku → kakuro, rotating), its own 🔥 streak,
        stars through addXP(), badges (🧩 Puzzle Master …) and best times.
   Engine: js/puzzles-core.js (deterministic per seed), run in js/puzzles-worker.js when possible.
   Stars: hints are paid from the puzzle's prize first, then from your stars. Puzzles never use button.opt (plans.js
   counts those for the free daily limit), so they are free for everyone.
   Entry points: the 🎮 Play hub (Practice tab), a 🧩 button on every chapter, unit and quest-complete card. State: ST.pz. */
(function () {
  'use strict';
  const D = document, PC = () => window.PuzzleCore;
  const $1 = (s, r) => (r || D).querySelector(s), $$ = (s, r) => [...(r || D).querySelectorAll(s)];
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const T = m => { try { toast(m); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const isJEE = () => { try { return !isCA() && !!(window.Jee && Jee.active && Jee.active()); } catch (e) { return false; } };
  const grade = () => { const s = STx(); return isCA() ? 13 : isJEE() ? 12 : (+(s && s.profile && s.profile.grade) || 6); };
  const X = () => (window.Ca && Ca._) || null;
  const pad2 = n => String(n).padStart(2, '0');
  const localISO = (d = new Date()) => `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;
  const dayNum = (d = new Date()) => Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 864e5);
  const yISO = () => localISO(new Date(Date.now() - 864e5));
  const fmtT = s => `${Math.floor(s / 60)}:${pad2(s % 60)}`;
  const kid = k => (k === 'ana' ? 'an' : k);
  const liveEl = () => { const r = PLAY && PLAY.root && PLAY.root.isConnected ? PLAY.root : D.getElementById('s-puz'); return r ? (r.querySelector('.pz-live') || $1('.pz-live', D.getElementById('s-puz') || D)) : null; };
  const announce = m => { const a = liveEl(); if (a && m) { a.textContent = ''; setTimeout(() => { a.textContent = m; }, 30); } try { if (window.A11Y && A11Y.cue) A11Y.cue(m); } catch (e) {} };

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
  /* scopes: { k:'q' } free play · { k:'s', g, sid, ci } one school chapter · { k:'c', ch } one CA chapter ·
     { k:'m', ca, g | lvl, sel: [tokens], label } any mix of subjects / papers, chapters and topics (js/scope.js tokens) */
  const scopeKey = sc => !sc || sc.k === 'q' ? 'free' : sc.k === 'c' ? sc.ch : sc.k === 'j' ? 'jee:' + sc.u : sc.k === 'm' ? `m:${sc.ca ? sc.lvl : 'g' + sc.g}:${(sc.sel || []).slice().sort().join(',')}` : `g${sc.g}-${sc.sid}-c${sc.ci}`;
  const cleanSc = sc => (!sc || sc.k === 'q' ? { k: 'q' } : sc.k === 'c' ? { k: 'c', ch: String(sc.ch) } : sc.k === 'j' ? { k: 'j', u: String(sc.u) }
    : sc.k === 'm' ? Object.assign({ k: 'm', ca: !!sc.ca, sel: (sc.sel || []).map(String).slice(0, 80), label: String(sc.label || '').slice(0, 120) }, sc.ca ? { lvl: String(sc.lvl || 'foundation') } : { g: +sc.g })
    : { k: 's', g: +sc.g, sid: String(sc.sid), ci: +sc.ci });
  const mOpt = sc => ({ ca: !!sc.ca, grade: sc.g, level: sc.lvl });
  const MRES = {};
  const mResolve = async sc => { const k = scopeKey(sc); if (!MRES[k]) MRES[k] = window.ScopePick ? ScopePick.resolve(sc.sel, mOpt(sc)).catch(() => []) : Promise.resolve([]); return MRES[k]; };
  const NUMERIC = /^(maths|accountancy|economics)$/;
  async function caChapter(ch) {
    const x = X(); if (!x) return null;
    const lvl = x.levelOf(ch); let st; try { st = await x.structure(lvl); } catch (e) { return null; }
    for (const p of st.papers) { const i = p.chapters.findIndex(c => c.id === ch); if (i >= 0) return { st, p, c: p.chapters[i], i }; }
    return null;
  }
  const subjMeta = (g, sid) => (((typeof CUR !== 'undefined' && CUR && CUR.grades && CUR.grades[g]) || {}).subjects || []).find(s => s.id === sid) || {};
  async function info(sc) {
    if (sc && sc.k === 'm') {
      const parts = await mResolve(sc); if (!parts.length) return null;
      let script = 'latn', numeric = false, lang = 'en';
      if (!sc.ca) { const c0 = parts[0].c; script = PC().chapterScript(c0) || 'latn'; numeric = parts.some(x => NUMERIC.test(x.sid)); if (script !== 'latn') lang = PC().langOf(script, parts[0].sid); }
      else numeric = parts.some(x => /-p[13]-/.test(x.ch));
      const subj = new Set(parts.map(x => (sc.ca ? x.p && x.p.name : x.sid)));
      return { title: sc.label || 'Your mix', sub: `${parts.length} chapter${parts.length > 1 ? 's' : ''}${subj.size > 1 ? ` · ${subj.size} ${sc.ca ? 'papers' : 'subjects'}` : ''}`, emoji: '🎯', numeric, key: scopeKey(sc), sname: sc.label || '', script, lang };
    }
    if (!sc || sc.k === 'q') return { title: 'Free play', sub: 'Any time, any level', emoji: '🧩', numeric: true, key: 'free', lang: 'en', script: 'latn' };
    if (sc.k === 'j') { if (!window.Jee) return null; const x = Jee.unitInfo(sc.u); return { title: x.title, sub: x.sub, emoji: x.emoji, numeric: false, key: scopeKey(sc), sname: x.sname, script: 'latn', lang: 'en' }; }
    if (sc.k === 's') {
      const d = await subjectData(sc.g, sc.sid), c = d && d.chapters[sc.ci]; if (!c) return null;
      const meta = subjMeta(sc.g, sc.sid), script = PC().chapterScript(c) || 'latn';
      const st = (window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[sc.sid]) || { e: '📘' };
      return { title: c.title, sub: `${meta.name || sc.sid} · Class ${sc.g} · Chapter ${c.n}`, emoji: c.emoji || st.e, numeric: NUMERIC.test(sc.sid), key: scopeKey(sc), sname: meta.name || sc.sid,
        script, lang: script === 'latn' ? 'en' : PC().langOf(script, sc.sid) };
    }
    const f = await caChapter(sc.ch); if (!f) return null;
    return { title: f.c.title, sub: `CA ${{ fnd: 'Foundation', int: 'Intermediate', fin: 'Final' }[sc.ch.split('-')[0]] || ''} · Paper ${String(f.p.key).replace('p', '')} ${f.p.name} · Ch ${f.c.n}`, emoji: '📘', numeric: /-p[13]-/.test(sc.ch), key: sc.ch, pname: f.p.name, sname: `Paper ${String(f.p.key).replace('p', '')}: ${f.p.name}`, lang: 'en', script: 'latn' };
  }
  const TERMS = {};
  /* the chapter's terms: own (this chapter), near (neighbouring chapters, Latin crosswords only), groups (concept
     sudoku) — built by PuzzleCore.termsFromSchool / termsFromCA from the raw content, exactly as a server would */
  async function terms(sc) {
    const k = scopeKey(sc); if (TERMS[k]) return TERMS[k];
    let t = { own: [], near: [], groups: [] };
    try {
      if (sc.k === 's') { const d = await subjectData(sc.g, sc.sid); if (d) t = PC().termsFromSchool(d, sc.ci); }
      else if (sc.k === 'j') { const d = window.Jee && await Jee.data(sc.u); if (d) t = PC().termsFromJee(d); }
      else if (sc.k === 'm') t = await mixTerms(sc);
      else if (sc.k === 'c') {
        const x = X(), f = await caChapter(sc.ch);
        if (f) {
          const units = {}, load = async cis => { for (const ci of cis) for (const u of f.p.chapters[ci].units) { if (u.status !== 'built' || units[u.id]) continue; try { const d = await x.unitData(u.id); if (d) units[u.id] = d; } catch (e) {} } };
          const make = () => PC().termsFromCA({ structure: f.st, units, keyItems: (window.CaKeysData && CaKeysData.ITEMS) || [] }, sc.ch);
          await load([f.i]); t = make();

        }
      }
    } catch (e) { console.warn('puzzle terms', e); }
    return (TERMS[k] = t);
  }
  /* a mix: the words of every chosen chapter (only the chosen topics / units), one script only (the first chapter's) */
  async function mixTerms(sc) {
    const parts = await mResolve(sc), out = { own: [], near: [], groups: [], ca: !!sc.ca }, seen = new Set();
    const put = list => list.forEach(t => { if (!seen.has(t.a)) { seen.add(t.a); out.own.push(t); } });
    if (!sc.ca) {
      let script = null;
      for (const x of parts) {
        const d = await subjectData(sc.g, x.sid); if (!d) continue;
        const scr = PC().chapterScript(d.chapters[x.ci]) || 'latn'; if (script == null) script = scr; if (scr !== script) continue;
        const t = PC().termsFromSchool(d, x.ci);
        put(t.own.filter(w => !x.topics || (w.tid && x.topics.has(w.tid))));
        if (!x.topics) out.groups.push(...(t.groups || []));
      }
    } else {
      const xx = X(); if (!xx) return out;
      const items = (window.CaKeysData && CaKeysData.ITEMS) || [];
      for (const x of parts) {
        const f = await caChapter(x.ch); if (!f) continue;
        const units = {};
        for (const u of f.c.units) { if (u.status !== 'built' || (x.units && !x.units.has(u.id))) continue; try { const d = await xx.unitData(u.id); if (d) units[u.id] = d; } catch (e) {} }
        const t = PC().termsFromCA({ structure: f.st, units, keyItems: items.filter(it => units[it.u]) }, x.ch);
        put(t.own); out.groups.push(...(t.groups || []));
      }
    }
    PC().rank && (out.own = PC().rank(out.own));
    return out;
  }
  const caNear = f => { const chs = f.p.chapters, order = []; for (let j = 1; j < chs.length && order.length < 20; j++) [f.i - j, f.i + j].forEach(x => { if (x >= 0 && x < chs.length && order.length < 20) order.push(x); }); return order; };

  /* the student's current chapter: last topic studied (school) / last unit opened (CA) */
  async function curChapter() {
    if (isJEE()) { const u = Jee.lastUnit(); return u ? { k: 'j', u } : { k: 'q' }; }
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
  /* the chapter last studied in one subject (school), for the picker's default */
  function lastInSubject(g, sid, d) {
    let best = null;
    Object.entries(ST.topics || {}).forEach(([tid, v]) => { const m = /^g(\d+)-([a-z]+)-(\d+)-\d+$/.exec(tid); if (!m || +m[1] !== g || m[2] !== sid) return; if (!best || String(v.last || '') > String(best.last || '')) best = { cn: +m[3], last: v.last }; });
    const ci = best ? d.chapters.findIndex(c => +c.n === best.cn) : -1;
    return ci >= 0 ? ci : Math.max(0, d.chapters.findIndex(c => !c.topics.every(t => ST.topics[t.id])));
  }

  /* ---------- kinds, defaults ---------- */
  const KINDS = [
    { id: 'sdk', e: '🔢', n: 'Sudoku', d: 'Every row, column and box holds each number once.', chapter: false },
    { id: 'kak', e: '➕', n: 'Kakuro', d: 'Number crossword: fill the cells so each run adds up.', chapter: false },
    { id: 'xw', e: '📝', n: 'Crossword', d: 'A chapter\'s key words, clues from the lesson.', chapter: true },
    { id: 'ws', e: '🔎', n: 'Word search', d: 'Find a chapter\'s key words in the grid.', chapter: true },
    { id: 'an', e: '🔤', n: 'Anagram', d: 'Unscramble a chapter\'s key words.', chapter: true },
    { id: 'csdk', e: '🧠', n: 'Concept sudoku', d: 'Sudoku with a chapter\'s words as the symbols.', chapter: true }];
  const KM = Object.fromEntries(KINDS.map(k => [k.id, k]));
  const TYPES = Object.assign({}, KM, { xw: Object.assign({}, KM.xw, { n: 'Chapter Crossword' }) });
  const CHAP = new Set(KINDS.filter(k => k.chapter).map(k => k.id));
  const defN = () => { const g = grade(); return g <= 3 ? 4 : g <= 6 ? 6 : 9; };
  const defKak = () => { const g = grade(); return g <= 5 ? 'easy' : g <= 8 ? 'medium' : 'hard'; };
  const defC = () => { const g = grade(); return g <= 4 ? 'easy' : g <= 8 ? 'medium' : 'hard'; };
  const pref = () => { const p = Z().pref; return { n: p.n || defN(), diff: p.diff || 'easy', kak: p.kak || defKak(), cdiff: p.cdiff || defC() }; };
  const DIFFS = [['easy', 'Easy'], ['medium', 'Medium'], ['hard', 'Hard']];
  const KDIFFS = [['easy', 'Easy 5×5'], ['medium', 'Medium 6×6'], ['hard', 'Hard 7×7'], ['expert', 'Expert 8×8']];
  const DN = { easy: 'Easy', medium: 'Medium', hard: 'Hard', expert: 'Expert' };
  /* kind notes: shown instead of a puzzle that this chapter cannot make (never swapped for an unrelated puzzle) */
  const NOPE = {
    xw: 'This chapter\'s key words don\'t cross each other well enough for a crossword yet.',
    ws: 'This chapter does not have enough key words for a word search yet.',
    an: 'This chapter does not have enough key words with clues for an anagram yet.',
    csdk: 'This chapter does not have a set of words for a concept sudoku yet.' };

  /* ================= build: spec → puzzle (deterministic, same on every phone) ================= */
  const BUILT = new Map();
  const phash = p => { try { return PC().hash(JSON.stringify(p)).toString(36); } catch (e) { return ''; } };
  function safe(t, p) {
    try {
      if (t === 'xw') return !PC().validCrossword(p);
      if (t === 'ws') return !PC().validWordsearch(p);
      if (t === 'an') return p.words.length >= 3 && p.words.every(w => w.u.join('') === w.a && w.t.slice().sort().join('|') === w.u.slice().sort().join('|') && w.u.every(PC().goodCell));
      if (t === 'sdk' || t === 'csdk') return !!(p && p.solution && p.puzzle.every((v, i) => !v || v === p.solution[i]));
      return !!p;
    } catch (e) { return false; }
  }
  async function build(spec) {
    if (!spec) return null;
    const sp = { t: kid(spec.t), sc: cleanSc(spec.sc), seed: String(spec.seed || 'x'), diff: spec.diff || 'easy', n: spec.n ? +spec.n : undefined };
    if (!KM[sp.t]) return null;
    const key = JSON.stringify([sp.t, sp.sc, sp.seed, sp.diff, sp.n || 0]);
    if (BUILT.has(key)) return BUILT.get(key);
    let res = null;
    try {
      const inf = await info(sp.sc); if (!inf) return null;
      let t = null;
      if (CHAP.has(sp.t)) { if (sp.sc.k === 'q') return null; const tt = await terms(sp.sc); t = { own: tt.own, near: tt.near, groups: tt.groups, ca: !!tt.ca }; }
      const r = await gen('puzzleFor', [sp, t]);
      if (r && r.p && safe(sp.t, r.p)) res = { p: r.p, extra: Object.assign({}, r.extra || {}, { info: inf, lang: inf.lang || 'en' }) };
    } catch (e) { console.warn('puzzle build', e); res = null; }
    BUILT.set(key, res); if (BUILT.size > 12) BUILT.delete(BUILT.keys().next().value);
    return res;
  }
  const readyText = (t, b) => {
    const p = b.p;
    const mix = b.extra && b.extra.info && String(b.extra.info.key || '').startsWith('m:');
    if (t === 'xw') { const nn = p.entries.filter(e => e.near).length; return `✓ ${p.entries.length - nn} words from ${mix ? 'your choice' : 'this chapter'}${nn ? ` + ${nn} ↗ from nearby chapters` : ''}${p.giv ? ' · first letters given' : ''}`; }
    if (t === 'ws') return `✓ ${p.words.length} words to find in a ${p.n}×${p.n} grid`;
    if (t === 'an') return `✓ ${p.words.length} words to unscramble`;
    if (t === 'csdk') return `✓ ${p.n}×${p.n} with ${b.extra.set.items.length} chapter words`;
    if (t === 'sdk') return `✓ ${p.n}×${p.n} · ${DN[p.diff] || p.diff}`;
    return `✓ ${p.w}×${p.h} · ${DN[p.diff] || p.diff}`;
  };
  function describe(spec) {
    if (!spec) return { ch: '', d: '' };
    const k = KM[kid(spec.t)] || {};
    const sz = kid(spec.t) === 'sdk' && spec.n ? `${spec.n}×${spec.n} · ` : '';
    return { ch: [spec.subjectName, spec.chapterTitle].filter(Boolean).join(' · ') || (k.chapter ? '' : 'Brain game'), d: `${k.e || '🧩'} ${k.n || 'Puzzle'} · ${sz}${DN[spec.diff] || spec.diff || ''}` };
  }

  /* ================= screen ================= */
  function screen() {
    let s = D.getElementById('s-puz');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-puz'; D.querySelector('main').appendChild(s); }
    style(); return s;
  }
  let CTX = null;
  function stopPlay() { if (CTX) { CTX.stop(); CTX = null; } if (PLAY && !PLAY.race) PLAY = null; }
  function makeCtx(host, race) {
    const c = { dead: false, ivs: [] };
    c.alive = () => { if (c.dead) return false; const s = D.getElementById('s-puz'); if (!host.isConnected || (!race && !(s && s.classList.contains('active')))) { c.stop(); return false; } return true; };
    c.iv = (f, ms) => { const id = setInterval(() => { if (c.alive()) f(); }, ms); c.ivs.push(id); return id; };
    c.stop = () => { c.dead = true; c.ivs.forEach(clearInterval); c.ivs = []; };
    return c;
  }
  function openScr(navKey, play) {
    stopPlay(); const s = screen(); show('puz', navKey || 'practice');
    const nav = D.querySelector('nav'); if (nav) nav.style.display = play ? 'none' : '';
    return s;
  }
  const navKeyOf = from => (from === 'world' || from === 'ca' ? 'world' : 'practice');
  const backLabel = from => (from === 'hub' ? 'Puzzles' : from === 'play' ? 'Play' : from === 'world' || from === 'ca' ? 'Home' : 'Practice');
  const scrAlive = el => el.isConnected && D.getElementById('s-puz').classList.contains('active');

  /* ---------- 💾 puzzles the student saved to finish later ---------- */
  const agoT = t => { const m = Math.round((Date.now() - t) / 6e4); return m < 1 ? 'just now' : m < 60 ? m + ' min ago' : m < 1440 ? Math.round(m / 60) + ' h ago' : Math.round(m / 1440) + ' days ago'; };
  function savedCard(box, only) {
    if (!box) return;
    const z = Z(), list = Object.entries(z.saves).filter(([, v]) => v && v.kept && v.sp && KM[v.sp.t] && (!only || scopeKey(v.sp.sc || { k: 'q' }) === only)).sort((a, b) => b[1].at - a[1].at);
    if (!list.length) { box.innerHTML = ''; return; }
    box.innerHTML = `<div class="card pz-saved"><h3>💾 Saved puzzles — finish them</h3>${list.map(([id, v]) => { const m = TYPES[v.sp.t] || KM[v.sp.t];
      return `<div class="pz-svrow"><button class="pz-svgo" data-id="${E(id)}"><span aria-hidden="true">${m.e}</span><span><b>${E(m.n)}</b><small>${E([v.title, DN[v.sp.diff] || v.sp.diff, agoT(v.at)].filter(Boolean).join(' · '))}</small></span><span class="pz-svp">▶ Continue</span></button><button class="pz-svx" data-x="${E(id)}" aria-label="Delete this saved ${E(m.n)}">🗑</button></div>`; }).join('')}</div>`;
    $$('.pz-svgo', box).forEach(b => b.onclick = () => { const v = Z().saves[b.dataset.id]; if (!v) return; S('open'); play(Object.assign({}, v.sp)); });
    $$('.pz-svx', box).forEach(b => b.onclick = () => { const z2 = Z(); delete z2.saves[b.dataset.x]; try { save(); } catch (e) {} T('Deleted'); savedCard(box, only); });
  }

  /* ================= HUB ================= */
  let HUBFROM = 'practice';
  async function hub(o) {
    o = o || {}; if (o.from) HUBFROM = o.from;
    const el = openScr(navKeyOf(HUBFROM)); const z = Z();
    el.innerHTML = `<div class="pz-root pz-hub"><p class="pz-live sr-only" aria-live="polite"></p><button class="back" id="pzBack">← ${backLabel(HUBFROM)}</button>
      <div class="hello" role="heading" aria-level="1"><span aria-hidden="true">🧩</span> Puzzles <small>Brain games and puzzles made from your chapters · free</small></div>
      <div id="pzSaved"></div><div id="pzDaily" class="card pz-daily"><p class="sub">Finding today's puzzle…</p></div>
      <div class="card"><h3>Quick play</h3><p class="sub">Tap a puzzle. Word puzzles let you pick the chapter.</p>
        <div class="pz-games">${KINDS.map(k => btn(k.id, k.chapter ? '📚 ' + k.d : k.d)).join('')}</div></div>
      <div class="card"><h3>🏅 Puzzle badges</h3>${badgeGrid()}<div class="pz-stats"><span>🧩 <b>${z.total}</b> solved</span><span>📅 best daily streak <b>${z.daily.best || 0}</b></span></div>${bestList()}</div></div>`;
    $1('#pzBack').onclick = () => back(HUBFROM);
    el.querySelectorAll('.pz-game').forEach(b => b.onclick = () => { S('open'); quick(b.dataset.q, { from: 'hub' }); });
    dailyCard($1('#pzDaily')); savedCard($1('#pzSaved'));
  }
  function back(from) {
    try {
      if (from && typeof from === 'object') { if (from.t === 'chapter') return chapterScreen(from.sid, from.ci); if (from.t === 'unit' && window.Ca) return Ca.unit(from.uid); if (from.t === 'topic') return chapterScreen(from.sid, from.ci); }
      if (from === 'hub') return hub();
      if (from === 'play') return window.PlayHub && PlayHub.open ? PlayHub.open() : practiceScreen();
      if (from === 'world' || from === 'ca') return worldScreen();
      if (from === 'ca-practice' && isCA() && window.CaTools && CaTools.practiceHub) return CaTools.practiceHub();
      return practiceScreen();
    } catch (e) { worldScreen(); }
  }
  function btn(t, extra, q) { const m = TYPES[t]; return `<button class="pz-game pz-g-${t}" data-q="${q || t}"><span class="pz-ge" aria-hidden="true">${m.e}</span><b>${m.n}</b><small>${extra ? E(extra) : E(m.d)}</small></button>`; }
  const chipRow = (k, list, cur, lab) => `<div class="pz-chips" role="radiogroup" aria-label="${lab}">${list.map(([v, n]) => `<button type="button" role="radio" aria-checked="${String(v) === String(cur)}" class="pz-chip${String(v) === String(cur) ? ' on' : ''}" data-pk="${k}" data-pv="${v}">${n}</button>`).join('')}</div>`;
  function wireChips(el, fn) {
    el.querySelectorAll('.pz-chip').forEach(b => b.onclick = () => {
      S('tap'); el.querySelectorAll(`.pz-chip[data-pk="${b.dataset.pk}"]`).forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-checked', String(on)); });
      fn(b.dataset.pk, b.dataset.pk === 'n' ? +b.dataset.pv : b.dataset.pv);
    });
  }
  const peekSeed = (k, t) => { const z = Z(), key = k + '|' + t; return `${key}|${(z.ctr[key] || 0) + 1}`; };
  const nextSeed = (k, t) => { const z = Z(), key = k + '|' + t; z.ctr[key] = (z.ctr[key] || 0) + 1; saveSoon(); return `${key}|${z.ctr[key]}`; };

  async function dailySpec() {
    const sc = await curChapter(), iso = localISO(), dn = dayNum(), p = pref(), seed = `daily|${iso}|${scopeKey(sc)}`;
    let t = ['xw', 'sdk', 'kak'][dn % 3];
    if (t === 'xw') { t = null; for (const k of ['xw', 'ws']) { if (sc.k !== 'q' && await build({ t: k, sc, seed, diff: p.cdiff })) { t = k; break; } } if (!t) t = 'sdk'; }
    return { t, sc, seed, n: p.n, diff: t === 'sdk' ? (dn % 2 ? 'medium' : 'easy') : t === 'kak' ? p.kak : p.cdiff, daily: iso };
  }
  async function dailyCard(box) {
    if (!box) return;
    let sp, inf; try { sp = await dailySpec(); inf = await info(sp.sc); } catch (e) { box.innerHTML = '<p class="sub">Daily puzzle is not ready right now.</p>'; return; }
    if (!box.isConnected) return;
    const z = Z(), done = z.daily.hist[sp.daily], m = TYPES[sp.t], n = dailyLive(), chap = CHAP.has(sp.t);
    box.innerHTML = `<div class="pz-dh"><span class="pz-de" aria-hidden="true">📅</span><div><span class="tag">Daily Puzzle · ${E(new Date().toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' }))}</span>
      <h2>${m.e} ${m.n}</h2><p class="sub">${chap ? `From <span${inf && inf.lang !== 'en' ? ` lang="${inf.lang}"` : ''}>${E(inf ? inf.title : 'your chapter')}</span>${inf && inf.sub ? ' · ' + E(inf.sub) : ''}` : 'Today\'s brain game at your level'}</p></div></div>
      <div class="pz-streak"><span>🔥 Daily streak <b>${n}</b></span><span>Best <b>${z.daily.best || 0}</b></span>${done ? '<span class="pz-ok">✓ Solved today</span>' : '<span>+10 ⭐ bonus</span>'}</div>
      <button class="btn ${done ? 'ghost' : 'mint'}" id="pzDailyGo">${done ? 'Play it again' : 'Play today\'s puzzle ▶'}</button>`;
    $1('#pzDailyGo', box).onclick = () => { S('open'); play(sp); };
  }

  /* ================= PICKER: subject → chapter, difficulty (quick play and race lobby) ================= */
  async function quick(kind, o) {
    o = o || {}; kind = kid(kind); if (!KM[kind]) kind = 'sdk';
    const from = o.from || 'hub';
    const el = openScr(navKeyOf(from === 'hub' ? HUBFROM : from));
    el.innerHTML = `<div class="pz-root pz-pick"><p class="pz-live sr-only" aria-live="polite"></p><button class="back" id="pzBack">← ${backLabel(from)}</button><div id="pzPk"></div></div>`;
    $1('#pzBack', el).onclick = () => back(from);
    picker($1('#pzPk', el), kind, { mode: 'play', sc: o.sc, diff: o.diff, n: o.n, from,
      onKind: k => quick(k, { from, sc: o.sc }),
      onGo: spec => play(Object.assign({}, spec, { seed: nextSeed(scopeKey(spec.sc), spec.t), from: { t: 'quick', from } })) });
  }
  function pick(kind) {
    return new Promise(res => {
      screen(); kind = kid(kind); if (!KM[kind]) kind = 'sdk';
      const sh = D.createElement('div'); sh.className = 'sheet show pz-sheet'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-label', 'Choose a puzzle');
      sh.innerHTML = '<div class="sheet-in pz-sheet-in"><div class="sheet-grab" aria-hidden="true"></div><div class="pz-root pz-pick"><p class="pz-live sr-only" aria-live="polite"></p><div class="pz-pkb"></div></div></div>';
      D.body.appendChild(sh);
      let done = false;
      const esc = e => { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); end(null); } };
      const end = v => { if (done) return; done = true; D.removeEventListener('keydown', esc, true); sh.classList.remove('show'); sh.remove(); res(v); };
      D.addEventListener('keydown', esc, true);
      sh.addEventListener('click', e => { if (e.target === sh) end(null); });
      const open = k => picker($1('.pz-pkb', sh), k, { mode: 'pick', onKind: open, onGo: spec => end(spec), onCancel: () => end(null) });
      open(kind);
      setTimeout(() => { const f = $1('h2', sh); if (f) { f.tabIndex = -1; try { f.focus(); } catch (e) {} } }, 60);
    });
  }
  async function picker(box, kind, o) {
    const m = KM[kind], chap = m.chapter, p = pref(), g = grade(), ca = isCA(), jee = isJEE();
    const S0 = { diff: o.diff || (kind === 'kak' ? p.kak : kind === 'sdk' ? p.diff : p.cdiff), n: o.n || (kind === 'sdk' ? p.n : kind === 'csdk' ? (g <= 3 ? 4 : 6) : undefined), sc: o.sc ? cleanSc(o.sc) : null, tok: 0, ready: null };
    if (kind === 'csdk' && S0.diff === 'hard') S0.diff = 'medium';
    if (kind !== 'kak' && S0.diff === 'expert') S0.diff = 'hard';
    const diffs = kind === 'kak' ? KDIFFS : kind === 'csdk' ? DIFFS.slice(0, 2) : DIFFS;
    box.innerHTML = `<div class="card pz-phead"><span class="pz-pe" aria-hidden="true">${m.e}</span><div><h2>${E(m.n)}</h2><p class="sub">${E(m.d)}</p></div></div>
      ${chap ? `<div class="card"><h3>📚 Pick a chapter</h3><div class="pz-subs" role="radiogroup" aria-label="${ca ? 'Paper' : 'Subject'}" id="pzSubs"><p class="sub">Loading…</p></div>
        <div class="pz-chlist" role="radiogroup" aria-label="Chapter" id="pzChl"></div></div>` : ''}
      <div class="card"><h3>💪 How hard?</h3>${kind === 'sdk' ? '<small class="pz-lab">Size</small>' + chipRow('n', [[4, '4×4'], [6, '6×6'], [9, '9×9']], S0.n, 'Sudoku size') + '<small class="pz-lab">Difficulty</small>' : ''}${chipRow('diff', diffs, S0.diff, 'Difficulty')}</div>
      <p class="pz-status" id="pzStat" role="status" aria-live="polite"></p><div id="pzAlt" class="pz-alt"></div>
      <button class="btn mint pz-go" id="pzGo" disabled>${o.mode === 'pick' ? 'Choose this puzzle ✓' : 'Play ▶'}</button>
      ${o.mode === 'pick' ? '<div style="height:8px"></div><button class="btn ghost" id="pzCancel" data-close="1">Cancel</button>' : ''}`;
    const stat = $1('#pzStat', box), go = $1('#pzGo', box), alt = $1('#pzAlt', box);
    const mkSpec = () => {
      const sc = chap ? S0.sc : { k: 'q' };
      const sp = { v: 1, t: kind, sc: cleanSc(sc), seed: o.mode === 'pick' ? S0.raceSeed : peekSeed(scopeKey(sc), kind), diff: S0.diff };
      if (S0.n) sp.n = S0.n;
      return sp;
    };
    S0.raceSeed = `race|${Date.now().toString(36)}|${Math.random().toString(36).slice(2, 8)}`;
    const check = async () => {
      const tok = ++S0.tok; go.disabled = true; S0.ready = null; alt.innerHTML = '';
      if (chap && !S0.sc) { stat.textContent = 'Pick a chapter above.'; return; }
      stat.textContent = 'Getting it ready…';
      const sp = mkSpec(), b = await build(sp);
      if (tok !== S0.tok || !box.isConnected) return;
      if (b) { S0.ready = { sp, b }; stat.textContent = readyText(kind, b); go.disabled = false; return; }
      stat.textContent = '🙂 ' + (chap ? (S0.sc && S0.sc.k === 'm' ? 'Your mix does not have enough key words for this puzzle yet — add more chapters with 🎯 Change, or try:' : NOPE[kind] + ' Tap 🎯 Change to add more chapters, or try:') : 'This puzzle could not be made. Please try again.');
      if (!chap) return;
      const others = [];
      for (const k of ['ws', 'an', 'xw', 'csdk']) { if (k === kind) continue; if (await build(Object.assign(mkSpec(), { t: k, n: k === 'csdk' ? (g <= 3 ? 4 : 6) : undefined, diff: k === 'csdk' && S0.diff === 'hard' ? 'medium' : S0.diff }))) others.push(k); }
      if (tok !== S0.tok || !box.isConnected) return;
      alt.innerHTML = others.length ? others.map(k => `<button class="pz-chip pz-altb" data-k="${k}">${KM[k].e} ${E(KM[k].n)}</button>`).join('') : '<p class="sub">This chapter has no word puzzles yet — please pick another chapter.</p>';
      $$('[data-k]', alt).forEach(b2 => b2.onclick = () => { S('tap'); o.onKind(b2.dataset.k, S0.sc); });
    };
    wireChips(box, (k, v) => { S0[k] = v; check(); });
    if (o.mode === 'pick') $1('#pzCancel', box).onclick = () => o.onCancel && o.onCancel();
    go.onclick = () => {
      if (!S0.ready) return; S('open');
      const z = Z(); if (kind === 'kak') z.pref.kak = S0.diff; else if (kind === 'sdk') { z.pref.diff = S0.diff; z.pref.n = S0.n; } else z.pref.cdiff = S0.diff; saveSoon();
      const sp = S0.ready.sp;
      if (o.mode === 'pick') {
        const inf = S0.ready.b.extra.info || {};
        const spec = JSON.parse(JSON.stringify(Object.assign({}, sp, { ph: phash(S0.ready.b.p), kindName: m.n, chapterTitle: chap ? inf.title || '' : '', subjectName: chap ? inf.sname || '' : '', size: S0.n ? `${S0.n}×${S0.n}` : undefined })));
        spec.label = [m.n, spec.chapterTitle, DN[spec.diff]].filter(Boolean).join(' · ');
        o.onGo(spec);
      } else o.onGo(sp);
    };
    if (!chap) { check(); return; }
    /* 🎯 solo play: any mix of subjects / papers, chapters and topics (js/scope.js); races keep one chapter (below) */
    if (o.mode !== 'pick' && window.ScopePick && !jee) {
      const card = $1('#pzSubs', box).closest('.card');
      const opt = ca ? { ca: true, level: (X() && X().C && X().C().level) || 'foundation' } : { ca: false, grade: g };
      const cur0 = await curChapter(); if (!box.isConnected) return;
      if (!S0.sc && cur0.k !== 'q') S0.sc = cur0;
      const tokensOf = async sc => {
        if (!sc) return [];
        if (sc.k === 'm') return sc.sel.slice();
        if (sc.k === 'c') return [sc.ch];
        if (sc.k === 's') { const d = await subjectData(sc.g, sc.sid), c = d && d.chapters[sc.ci]; const t0 = c && c.topics && c.topics[0]; return t0 && /-\d+$/.test(t0.id) ? [t0.id.replace(/-\d+$/, '')] : [`g${sc.g}-${sc.sid}`]; }
        return [];
      };
      const toSc = async (v, lb) => {
        const parts = await ScopePick.resolve(v, opt);
        if (parts.length === 1 && !parts[0].topics && !parts[0].units) return ca ? { k: 'c', ch: parts[0].ch } : { k: 's', g, sid: parts[0].sid, ci: parts[0].ci };
        return cleanSc({ k: 'm', ca, g, lvl: opt.level, sel: v, label: lb });
      };
      const draw = async () => {
        let label = 'Pick what to play', hint = ca ? 'Papers, chapters or units — any mix' : 'Subjects, chapters or topics — any mix';
        if (S0.sc) { const inf = await info(S0.sc); if (inf) { label = inf.title; hint = inf.sub + ' · tap Change to mix more'; } }
        if (!box.isConnected) return;
        card.innerHTML = `<h3>📚 Play from</h3>${ScopePick.pickHTML(label, hint, 'pzScope')}`;
        $1('#pzScope', card).onclick = async () => { S('tap'); ScopePick.open(Object.assign({}, opt, { value: await tokensOf(S0.sc), title: `${m.e} What should the ${m.n.toLowerCase()} use?`, cta: 'Use these ✓',
          onDone: async (v, lb) => { S0.sc = await toSc(v, lb); await draw(); check(); } })); };
      };
      await draw(); check(); return;
    }
    /* subjects (school) or papers (CA), then that subject's chapters */
    const subsEl = $1('#pzSubs', box), chl = $1('#pzChl', box);
    const cur = await curChapter(); if (!box.isConnected) return;
    if (!S0.sc && cur.k !== 'q') S0.sc = cur;
    let subs = [];
    if (jee) subs = Jee.puzzleSubjects();
    else if (ca) {
      const x = X(); let st = null; try { st = await x.structure(x.C().level || 'foundation'); } catch (e) {}
      subs = st ? st.papers.map(pp => ({ id: pp.key, name: `P${String(pp.key).replace('p', '')} ${pp.name}`, e: '📘', chs: pp.chapters.map((c, i) => ({ n: c.n, title: c.title, sc: { k: 'c', ch: c.id } })) })) : [];
    } else {
      subs = curSubjects(g).map(s0 => ({ id: s0.id, name: s0.name, e: ((window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[s0.id]) || { e: '📘' }).e }));
    }
    if (!subs.length) { subsEl.innerHTML = '<p class="sub">No subjects yet.</p>'; stat.textContent = ''; return; }
    const subOf = sc => (!sc ? null : sc.k === 'c' ? (subs.find(s0 => s0.chs.some(c => c.sc.ch === sc.ch)) || {}).id : sc.k === 'j' ? (subs.find(s0 => s0.chs.some(c => c.sc.u === sc.u)) || {}).id : sc.sid);
    let curSub = subOf(S0.sc) || subs[0].id;
    subsEl.innerHTML = subs.map(s0 => `<button type="button" role="radio" class="pz-sbj" data-sid="${E(s0.id)}" aria-checked="false"><span aria-hidden="true">${E(s0.e)}</span> ${E(s0.name)}</button>`).join('');
    const showSub = async (sid, keep) => {
      curSub = sid;
      $$('.pz-sbj', subsEl).forEach(b2 => { const on = b2.dataset.sid === sid; b2.classList.toggle('on', on); b2.setAttribute('aria-checked', String(on)); });
      let chs = [];
      if (ca || jee) chs = (subs.find(s0 => s0.id === sid) || {}).chs || [];
      else { chl.innerHTML = '<p class="sub">Loading…</p>'; const d = await subjectData(g, sid); if (curSub !== sid || !box.isConnected) return; chs = d ? d.chapters.map((c, i) => ({ n: c.n, title: c.title, sc: { k: 's', g, sid, ci: i }, lang: PC().chapterScript(c) !== 'latn' ? PC().langOf(PC().chapterScript(c), sid) : '' })) : []; if (!keep && d) S0.sc = chs[lastInSubject(g, sid, d)] ? chs[lastInSubject(g, sid, d)].sc : null; }
      if (ca && !keep) S0.sc = chs.length ? (chs.find(c => cur.k === 'c' && c.sc.ch === cur.ch) || chs[0]).sc : null;
      if (jee && !keep) S0.sc = chs.length ? (chs.find(c => cur.k === 'j' && c.sc.u === cur.u) || chs[0]).sc : null;
      if (!chs.length) { chl.innerHTML = '<p class="sub">Coming soon.</p>'; S0.sc = null; check(); return; }
      const isCur = c => cur.k !== 'q' && scopeKey(c.sc) === scopeKey(cur);
      chl.innerHTML = chs.map((c, i) => `<button type="button" role="radio" class="pz-chb" data-i="${i}" aria-checked="false"><span class="pz-chn">${E(c.n)}</span><span class="pz-cht"${c.lang ? ` lang="${c.lang}"` : ''}>${E(c.title)}</span>${isCur(c) ? '<small class="pz-here">📍 your chapter</small>' : ''}</button>`).join('');
      const mark = () => $$('.pz-chb', chl).forEach(b2 => { const on = S0.sc && scopeKey(chs[+b2.dataset.i].sc) === scopeKey(S0.sc); b2.classList.toggle('on', !!on); b2.setAttribute('aria-checked', String(!!on)); });
      $$('.pz-chb', chl).forEach(b2 => b2.onclick = () => { S('tap'); S0.sc = chs[+b2.dataset.i].sc; mark(); check(); });
      mark(); const on = $1('.pz-chb.on', chl); if (on) { try { chl.scrollTop = Math.max(0, on.offsetTop - chl.offsetTop - 8); } catch (e) {} }
      check();
    };
    $$('.pz-sbj', subsEl).forEach(b2 => b2.onclick = () => { S('tap'); showSub(b2.dataset.sid, false); });
    showSub(curSub, !!S0.sc && subOf(S0.sc) === curSub);
  }

  /* ================= CHAPTER: its puzzles (from a chapter / unit / quest-complete card) ================= */
  async function chapter(sc, from) {
    const el = openScr('world');
    el.innerHTML = `<div class="pz-root pz-chap"><p class="sub pz-load">Building this chapter's puzzles…</p></div>`;
    const inf = await info(sc);
    if (!scrAlive(el)) return;
    if (!inf) { el.innerHTML = '<div class="card"><p class="sub">This chapter is not available.</p></div>'; return; }
    const p = pref(), g = grade(), lang = inf.lang && inf.lang !== 'en' ? ` lang="${inf.lang}"` : '';
    const backLbl = from && from.t === 'hub' ? 'Puzzles' : from && from.t === 'unit' ? 'Unit' : 'Chapter';
    el.innerHTML = `<div class="pz-root pz-chap"><p class="pz-live sr-only" aria-live="polite"></p><button class="back" id="pzBack">← ${backLbl}</button>
      <div class="card pz-chead"><div class="pz-ce" aria-hidden="true">${E(inf.emoji)}</div><div><span class="tag">🧩 Puzzle this chapter</span><h2${lang}>${E(inf.title)}</h2><p class="sub">${E(inf.sub)}</p></div></div><div id="pzSaved"></div>
      <div class="card"><h3>💪 How hard?</h3>${chipRow('cdiff', DIFFS, p.cdiff, 'Difficulty')}</div>
      <div class="pz-games" id="pzCg"><p class="sub pz-load">Checking which puzzles this chapter can make…</p></div><div id="pzCn"></div>
      <button class="btn ghost" id="pzHub">🧩 All puzzles & daily puzzle</button></div>`;
    $1('#pzBack').onclick = () => (from && from.t === 'hub' ? hub() : back(from));
    $1('#pzHub').onclick = () => hub({});
    const k = scopeKey(sc); savedCard($1('#pzSaved', el), k);
    const fill = async () => {
      const diff = pref().cdiff, tok = (fill.tok = (fill.tok || 0) + 1), got = [], miss = [];
      const list = ['xw', 'ws', 'an', 'csdk'].concat(inf.numeric ? ['kak'] : []);
      for (const t of list) {
        const sp = { t, sc, seed: peekSeed(k, t), diff: t === 'kak' ? pref().kak : t === 'csdk' && diff === 'hard' ? 'medium' : diff, n: t === 'csdk' ? (g <= 3 ? 4 : 6) : undefined };
        const b = await build(sp); if (fill.tok !== tok || !scrAlive(el)) return;
        (b ? got : miss).push([t, b]);
      }
      const cg = $1('#pzCg', el), cn = $1('#pzCn', el); if (!cg) return;
      cg.innerHTML = got.map(([t, b]) => btn(t, t === 'kak' ? 'With a ledger story · ' + (DN[b.p.diff] || '') : readyText(t, b).replace(/^✓ /, ''))).join('') || '';
      cn.innerHTML = miss.filter(([t]) => t !== 'kak').length ? `<p class="note">🙂 ${got.length ? 'Not here yet: ' + miss.filter(([t]) => t !== 'kak').map(([t]) => KM[t].n).join(', ') + ' — this chapter does not have enough key words for ' + (miss.length > 1 ? 'them' : 'it') + ' yet.' : 'This chapter does not have enough key words for word puzzles yet. Try a brain game from the Puzzles screen.'}</p>` : '';
      $$('.pz-game', cg).forEach(b2 => b2.onclick = () => {
        S('open'); const t = b2.dataset.q, d2 = pref().cdiff;
        play({ t, sc, seed: nextSeed(k, t), diff: t === 'kak' ? pref().kak : t === 'csdk' && d2 === 'hard' ? 'medium' : d2, n: t === 'csdk' ? (g <= 3 ? 4 : 6) : undefined, from: { t: 'chap', from } });
      });
    };
    wireChips(el, (key, v) => { Z().pref.cdiff = v; saveSoon(); fill(); });
    fill();
  }

  /* ================= PLAY ================= */
  let PLAY = null;          // the running puzzle (for keys + Listen mode)
  const pid = sp => [sp.t, sp.seed, sp.n || '', sp.diff || ''].join('|');
  function goBack(sp) {
    const f = sp && sp.from;
    if (f && f.t === 'quick') return quick(sp.t, { from: f.from, sc: CHAP.has(sp.t) ? sp.sc : undefined, diff: sp.diff, n: sp.t === 'sdk' ? sp.n : undefined });
    if (f && f.t === 'chap' && sp.sc && sp.sc.k !== 'q') return chapter(sp.sc, f.from);
    return hub();
  }
  async function play(sp) {
    sp = Object.assign({}, sp, { t: kid(sp.t) });
    const el = openScr('practice', true);
    el.innerHTML = `<div class="pz-root"><div class="card pz-genc"><div class="pz-spin" aria-hidden="true">🧩</div><b>Making your puzzle…</b><p class="sub">Checking it has exactly one answer.</p></div></div>`;
    const b = await build(sp);
    if (!scrAlive(el)) return;
    if (!b) {
      el.innerHTML = `<div class="pz-root"><button class="back" id="pzBack">← Back</button><div class="card"><p class="sub">🙂 ${E(CHAP.has(sp.t) ? NOPE[sp.t] : 'This puzzle could not be made.')} Please try another one.</p></div></div>`;
      const nav = D.querySelector('nav'); if (nav) nav.style.display = '';
      $1('#pzBack').onclick = () => goBack(sp); return;
    }
    start(el, sp, b, null);
    try { if (window.A11Y && A11Y.readScreen) setTimeout(() => A11Y.readScreen(), 300); } catch (e) {}
  }
  /* render a built puzzle into el: the full screen (race = null) or a race host (race = callbacks) */
  function start(el, sp, b, race) {
    const p = b.p, id = pid(sp), sig = sp.t === 'xw' ? p.entries.map(e => e.a).join(',') : '';
    let saved = race ? null : Z().saves[id];
    if (saved && sig && saved.sig !== sig) saved = null;          // the puzzle changed since it was saved (new app version): start fresh
    const ctx = makeCtx(el, !!race); if (!race) CTX = ctx;
    const st = { sp, p, id, t0: Date.now(), secs: saved ? saved.t || 0 : 0, hints: 0, spent: 0, mistakes: 0, pool: prize(sp, p), done: false, extra: b.extra || {}, ctx, race, root: el,
      lang: (b.extra && b.extra.lang) || 'en', indic: !!(p.script && p.script !== 'latn') };
    st.L = st.indic ? ` lang="${st.lang}"` : '';
    if (saved && saved.pool != null) { st.pool = saved.pool; st.hints = saved.hints || 0; }
    if (saved && saved.kept) st.kept = true;
    st.prog = (done, total) => { if (!race || !race.onProgress || st.lastProg === done + '/' + total) return; st.lastProg = done + '/' + total; try { race.onProgress({ done, total }); } catch (e) {} };
    PLAY = st;
    ({ xw: playXW, sdk: playSDK, csdk: playSDK, kak: playKAK, ws: playWS, an: playAN })[sp.t](el, st, saved);
    if (st.sp.t !== 'an') startClock(st);
    if (!race && window.LeaveGuard) LeaveGuard.arm({ name: 'this ' + (TYPES[sp.t] || KM[sp.t] || { n: 'puzzle' }).n.toLowerCase(), root: el.querySelector('.pz-root') || el,
      save: () => { st.kept = true; persist(st, true); }, saveNote: 'Find it in 🎮 Play → Your saved games',
      discard: () => { const z = Z(); delete z.saves[st.id]; try { save(); } catch (e) {} },
      leave: () => { const sp2 = st.sp; stopPlay(); goBack(sp2); } });
    return st;
  }
  function prize(sp, p) {
    if (sp.t === 'xw') return 10 + p.entries.length;
    if (sp.t === 'sdk' || sp.t === 'csdk') return ({ 4: { easy: 6, medium: 8, hard: 10 }, 6: { easy: 10, medium: 12, hard: 15 }, 9: { easy: 15, medium: 20, hard: 25 } }[p.n] || {})[p.diff] || 10;
    if (sp.t === 'kak') return { easy: 12, medium: 16, hard: 20, expert: 25 }[p.diff] || 12;
    return sp.t === 'ws' ? 8 : 6;
  }
  /* ---------- "How to play": 3–4 short steps per puzzle; open the first time a student plays that kind ---------- */
  const HOW = {
    xw: ind => [
      `Tap a clue (or a box) to choose a word. The number in brackets is how many ${ind ? 'boxes' : 'letters'} it has — (5,4) means two words of 5 and 4.`,
      `Words before a dot are the topic, e.g. <i>Feeling and what to do · Talk to someone you trust</i> → the answer fits that topic.`,
      ind ? 'Tap a box, then tap the akshara below to fill it.' : 'Type the answer. Across words go left → right, Down words go top → bottom.',
      'A finished word gets a thin <b style="color:#1f9d55">green</b> border when it is right and a <b style="color:#e03131">red</b> one when it is wrong, and shows the chapter and topic it is from — tap it to read.',
      'Stuck? <b>🪄 Hint</b> gives up to 5 clues per word (1⭐ each — fewer stars at the end). <b>✔ Check word</b> marks wrong boxes; <b>💡 Reveal</b> fills one box. ↗ = word from a nearby chapter.'],
    ws: ind => [
      'Read the word list below the grid — every word is hidden in the grid.',
      `Words run in a straight line: across, down or diagonally${ind ? '' : ', sometimes backwards'}.`,
      `Tap the first ${ind ? 'box' : 'letter'} of a word, then the last ${ind ? 'box' : 'letter'}. A found word turns coloured and is ticked in the list.`],
    an: ind => [
      `The ${ind ? 'tiles' : 'letters'} of one key word are mixed up. Read the clue to know what the word is.`,
      `Tap the ${ind ? 'tiles' : 'letters'} in the right order to spell it. <b>⌫ Undo</b> takes back the last one.`,
      'Finish every word to solve the puzzle. Showing an answer costs stars.'],
    sdk: () => [
      'Fill every empty box with a number.',
      'Each row, each column and each bold box must have every number exactly once — no repeats.',
      'Look for a row, column or box with only one number missing and start there. <b>✏️ Pencil</b> lets you note possible numbers.'],
    csdk: () => [
      'Same rules as Sudoku, but with symbols — each symbol stands for one word from your chapter (see the key).',
      'Each row, each column and each bold box must have every symbol exactly once.',
      'Tap a box, then tap a symbol to place it. Start where only one symbol is missing.'],
    kak: () => [
      'A crossword with numbers. In a dark box, the number at the <b>top-right</b> is the total of the white boxes to its right; the number at the <b>bottom-left</b> is the total of the white boxes below it.',
      'Use only the digits 1 to 9, and never repeat a digit inside one total.',
      'Example: a total of 3 in two boxes can only be 1 + 2. Start with such small or large totals.']
  };
  function howHTML(st) {
    const k = st && st.sp && (st.sp.t === 'ana' ? 'an' : st.sp.t), f = HOW[k]; if (!f) return '';
    let seen = {}; try { seen = JSON.parse(localStorage.getItem('sv_pz_how') || '{}'); } catch (e) {}
    const first = !seen[k]; if (first) { seen[k] = 1; try { localStorage.setItem('sv_pz_how', JSON.stringify(seen)); } catch (e) {} }
    return `<details class="pz-how"${first ? ' open' : ''}><summary>❓ How to play</summary><ol>${f(!!st.indic).map(x => `<li>${x}</li>`).join('')}</ol></details>`;
  }
  function header(st, title, sub) {
    const q = st.race ? '<button class="pz-x" id="pzQuit" aria-label="Leave the race">✕ Quit</button>' : '<button class="pz-x" id="pzQuit" aria-label="Leave puzzle — save it or leave">← Back</button>';
    return `<p class="pz-live sr-only" aria-live="polite"></p><div class="pz-bar">${q}<b class="pz-title">${title}</b><span class="pz-time" role="timer" aria-label="Time">${fmtT(st.secs)}</span><span class="pz-prize" title="Stars for solving">⭐ <b>${st.pool}</b></span></div>${howHTML(st)}${sub ? `<p class="pz-sub">${sub}</p>` : ''}`;
  }
  function wireQuit(el, st) {
    $1('#pzQuit', el).onclick = () => {
      S('tap');
      if (st.race) { try { st.race.onQuit && st.race.onQuit(); } catch (e) {} return; }
      if (window.LeaveGuard && LeaveGuard.armed) { LeaveGuard.ask(); return; }
      persist(st, true); const sp = st.sp; stopPlay(); goBack(sp);
    };
  }
  function startClock(st) {
    let last = Date.now();
    st.ctx.iv(() => { const n = Date.now(); if (!D.hidden && !st.done) { st.secs += Math.round((n - last) / 1000); } last = n; const t = $1('.pz-time', st.root); if (t) t.textContent = fmtT(st.secs); }, 1000);
  }
  function setPool(st) { const b = $1('.pz-prize b', st.root); if (b) b.textContent = st.pool; }
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
    if (st.done || !st.getState || st.race) return;
    const z = Z(), inf = (st.extra && st.extra.info) || {};
    const spec = JSON.parse(JSON.stringify({ t: st.sp.t, sc: st.sp.sc, seed: st.sp.seed, diff: st.sp.diff, n: st.sp.n, daily: st.sp.daily, from: st.sp.from }));
    z.saves[st.id] = Object.assign(st.getState(), { sig: st.sp.t === 'xw' ? st.p.entries.map(e => e.a).join(',') : '', t: st.secs, pool: st.pool, hints: st.hints, at: Date.now(), sp: spec, title: inf.title || '', sub: inf.sname || '', kept: !!st.kept });
    const ks = Object.keys(z.saves).sort((a, b) => z.saves[b].at - z.saves[a].at);
    ks.filter(k => !z.saves[k].kept).slice(8).forEach(k => delete z.saves[k]); ks.filter(k => z.saves[k] && z.saves[k].kept).slice(12).forEach(k => delete z.saves[k]);
    if (now) { try { save(); } catch (e) {} } else saveSoon();
  }
  const cellsU = g => [].concat(...g.map(r => (Array.isArray(r) ? r : r.split(''))));

  /* ---------- 📝 CROSSWORD (Latin letters or Indic aksharas, one per cell) ---------- */
  function playXW(el, st, saved) {
    const p = st.p, w = p.w, h = p.h, N = w * h, sol = cellsU(p.grid), u = new Array(N).fill(''), rev = new Set(), wrong = new Set(), giv = new Set(p.giv || []);
    const indic = st.indic, tray = indic ? [...new Set(sol.filter(c => c !== '#'))].sort() : null, unit = indic ? 'box' : 'letter';
    const okCell = c => typeof c === 'string' && (indic ? tray.includes(c) : /^[A-Z]$/.test(c));
    const at = {}; p.entries.forEach((e, k) => { for (let j = 0; j < e.len; j++) { const i = (e.r + (e.dir === 'D' ? j : 0)) * w + e.c + (e.dir === 'A' ? j : 0); (at[i] = at[i] || {})[e.dir] = k; } });
    giv.forEach(i => { u[i] = sol[i]; });
    if (saved && saved.u) saved.u.forEach((c, i) => { if (sol[i] !== '#' && !giv.has(i) && okCell(c)) u[i] = c; });
    if (saved && saved.rev) saved.rev.forEach(i => rev.add(i));
    const HU = Object.assign({}, (saved && saved.hu) || {}), HC = {}, SRC = {}, HMAX = 5;   // hints used per word · hint lists · word sources
    st.getState = () => ({ u: u.slice(), rev: [...rev], hu: Object.assign({}, HU) });
    st.answer = () => p.entries.map((e, k) => cellsOf(k).map(i => u[i]).join(''));
    const lock = i => rev.has(i) || giv.has(i);
    let cur = p.entries[0].r * w + p.entries[0].c, dir = p.entries[0].dir;
    const near = p.entries.some(e => e.near);
    const nums = {}; p.entries.forEach(e => { nums[e.r * w + e.c] = e.n; });
    const cellsOf = k => { const e = p.entries[k], l = []; for (let j = 0; j < e.len; j++) l.push((e.r + (e.dir === 'D' ? j : 0)) * w + e.c + (e.dir === 'A' ? j : 0)); return l; };
    const entryAt = (i, d) => (at[i] ? (at[i][d] != null ? at[i][d] : at[i][d === 'A' ? 'D' : 'A']) : null);
    const dirName = d => (d === 'A' ? 'Across' : 'Down');
    const clueHTML = e => `${e.ctx ? `<span class="pz-ctx"${st.L}>${E(e.ctx)} ·</span> ` : ''}<span${st.L}>${E(e.clue)}</span> <span class="pz-enum">${E(e.enum)}</span>${e.near ? ' <span class="pz-near" title="From a nearby chapter">↗</span>' : ''}`;
    el.innerHTML = `<div class="pz-root pz-xw${indic ? ' pz-indic' : ''}" data-pz="xw">${header(st, '📝 Chapter Crossword', `${p.entries.length} words${indic ? ' · one akshara in each box' : ''}${p.giv ? ' · first letters given' : ''}${near ? ' · ↗ = from a nearby chapter' : ''}`)}
      <div class="pz-cluebar" id="pzClue" aria-live="polite"></div><div class="pz-whelp" id="pzHelp"></div>
      <div class="pz-gridwrap"><div class="pz-xgrid" id="pzGrid" role="grid"${st.L} aria-label="Crossword, ${w} columns by ${h} rows. ${indic ? 'Tap a box, then an akshara below' : 'Type letters'}; arrow keys move; Enter goes to the next clue; Space turns between across and down." style="--w:${w};--h:${h}">
        ${Array.from({ length: h }, (_, y) => `<div role="row" class="pz-row">${Array.from({ length: w }, (_, x) => { const i = y * w + x; return sol[i] === '#' ? `<div role="gridcell" class="pz-c blk" aria-hidden="true"></div>` : `<div role="gridcell" class="pz-c${giv.has(i) ? ' giv' : ''}" data-i="${i}" tabindex="-1">${nums[i] ? `<span class="pz-n" aria-hidden="true">${nums[i]}</span>` : ''}<span class="pz-l" aria-hidden="true"></span></div>`; }).join('')}</div>`).join('')}
      </div></div>
      <div class="pz-tools"><button class="pz-tb" id="pzHint">🪄 Hint <span class="pz-hn"></span> <small>1⭐</small></button><button class="pz-tb" id="pzRev">💡 Reveal ${unit} <small>2⭐</small></button><button class="pz-tb" id="pzChk">✔ Check word <small>1⭐</small></button><button class="pz-tb" id="pzDir" aria-label="Switch between across and down">⇄</button></div>
      ${indic ? trayHTML(tray, st.lang) : kbHTML()}
      <div class="card pz-clues"><h3>Across</h3><ol>${p.entries.filter(e => e.dir === 'A').map(e => `<li><button class="pz-cl" data-k="${p.entries.indexOf(e)}"><b>${e.n}</b> ${clueHTML(e)}</button><button class="pz-srcb" data-sk="${p.entries.indexOf(e)}" hidden></button></li>`).join('')}</ol>
        <h3>Down</h3><ol>${p.entries.filter(e => e.dir === 'D').map(e => `<li><button class="pz-cl" data-k="${p.entries.indexOf(e)}"><b>${e.n}</b> ${clueHTML(e)}</button><button class="pz-srcb" data-sk="${p.entries.indexOf(e)}" hidden></button></li>`).join('')}</ol></div></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el), cellEl = i => grid.querySelector(`[data-i="${i}"]`);
    const total = sol.filter(c => c !== '#').length;
    /* a finished word gets a thin border: green when right, red when wrong; and shows where it comes from */
    const state = k => { const cs = cellsOf(k); if (cs.some(i => !u[i])) return ''; return cs.every(i => u[i] === sol[i]) ? 'ok' : 'bad'; };
    const wb = {};
    const words = () => {
      p.entries.forEach((e, k) => {
        const s2 = state(k); let b = wb[k];
        if (!s2) { if (b) b.hidden = true; } else {
          if (!b) { b = wb[k] = D.createElement('div'); b.className = 'pz-wb'; b.setAttribute('aria-hidden', 'true'); grid.appendChild(b); }
          const cs = cellsOf(k), a = cellEl(cs[0]), z = cellEl(cs[cs.length - 1]);
          if (a && z) { b.style.left = a.offsetLeft + 'px'; b.style.top = a.offsetTop + 'px'; b.style.width = (z.offsetLeft + z.offsetWidth - a.offsetLeft) + 'px'; b.style.height = (z.offsetTop + z.offsetHeight - a.offsetTop) + 'px'; }
          b.className = 'pz-wb ' + s2 + (e.dir === 'D' ? ' d' : ' a'); b.hidden = false;
        }
        const sb = $1(`.pz-srcb[data-sk="${k}"]`, el); if (!sb) return;
        if (!s2 || !window.PzWords) { sb.hidden = true; return; }
        const show = r => { if (!r || !r.path.length) { sb.hidden = true; return; } sb.innerHTML = `${s2 === 'ok' ? '✅' : '❌'} 📍 ${r.path.map(E).join(' › ')}`; sb.className = 'pz-srcb ' + s2; sb.hidden = false; };
        if (SRC[k] && SRC[k].then) return; if (SRC[k]) show(SRC[k]); else SRC[k] = PzWords.source(st.sp, e).then(r => { SRC[k] = r; if (st.ctx.alive()) paint(); }).catch(() => { SRC[k] = { path: [], open() {} }; });
      });
    };
    const help = k => {
      const hb = $1('#pzHelp', el); if (!hb) return;
      const n = HU[k] || 0, list = HC[k] && !HC[k].then ? HC[k] : null, s2 = state(k), r = SRC[k] && !SRC[k].then ? SRC[k] : null;
      const hn = $1('#pzHint .pz-hn', el); if (hn) hn.textContent = `${n}/${list ? Math.min(HMAX, list.length) : HMAX}`;
      const hs = list ? list.slice(0, n) : [];
      hb.innerHTML = (hs.length ? `<ol class="pz-hlist" aria-label="Hints for this word">${hs.map(h => `<li><span aria-hidden="true">${h.ic}</span> <b>${E(h.label)}:</b> <span${st.L}>${E(h.text)}</span></li>`).join('')}</ol>` : '')
        + (s2 && r && r.path.length ? `<button class="pz-srcb ${s2}" id="pzSrcCur">${s2 === 'ok' ? '✅ Right!' : '❌ Not right yet.'} 📍 From: ${r.path.map(E).join(' › ')} <u>Read</u></button>` : '');
      const sc = $1('#pzSrcCur', hb); if (sc) sc.onclick = () => { S('tap'); r.open(); };
    };
    const paint = (speak) => {
      const k = entryAt(cur, dir); if (k == null) return; dir = p.entries[k].dir; const cs = new Set(cellsOf(k)), e = p.entries[k];
      $$('.pz-c[data-i]', grid).forEach(c => {
        const i = +c.dataset.i, L = u[i]; c.querySelector('.pz-l').textContent = L;
        c.classList.toggle('word', cs.has(i)); c.classList.toggle('cur', i === cur); c.classList.toggle('rev', rev.has(i)); c.classList.toggle('bad', wrong.has(i));
        c.tabIndex = i === cur ? 0 : -1;
        const parts = []; if (at[i].A != null) parts.push(`${p.entries[at[i].A].n} across`); if (at[i].D != null) parts.push(`${p.entries[at[i].D].n} down`);
        c.setAttribute('aria-label', `${parts.join(', ')}. Row ${Math.floor(i / w) + 1}, column ${i % w + 1}: ${L || 'empty'}${giv.has(i) ? ', given' : ''}${rev.has(i) ? ', revealed' : ''}${wrong.has(i) ? ', wrong' : ''}`);
        c.setAttribute('aria-selected', String(i === cur));
      });
      $1('#pzClue', el).innerHTML = `<b>${e.n} ${dirName(e.dir)}</b> ${clueHTML(e)}`;
      $$('.pz-cl', el).forEach(b => b.classList.toggle('on', +b.dataset.k === k));
      words(); help(k);
      if (speak) announce(`${e.n} ${dirName(e.dir)}, ${e.len} ${unit}es. ${e.ctx ? e.ctx + '. ' : ''}${e.clue}. ${cellsOf(k).map(i => u[i] || 'blank').join(', ')}`.replace(/letteres/, 'letters'));
      let ok = 0; for (let i = 0; i < N; i++) if (sol[i] !== '#' && u[i] === sol[i]) ok++; st.prog(ok, total);
    };
    const focusCur = () => { const c = cellEl(cur); if (c && el.contains(D.activeElement) && D.activeElement !== c && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const done = () => { for (let i = 0; i < N; i++) if (sol[i] !== '#' && u[i] !== sol[i]) return false; return true; };
    const filled = () => { for (let i = 0; i < N; i++) if (sol[i] !== '#' && !u[i]) return false; return true; };
    const after = () => { persist(st); if (done()) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (filled()) { T('All filled, but some boxes are wrong. Tap ✔ Check word on each word to find them.'); S('hmm'); } };
    const moveIn = (step) => { const k = entryAt(cur, dir), cs = cellsOf(k); let j = cs.indexOf(cur) + step; while (j >= 0 && j < cs.length && giv.has(cs[j]) && step > 0) j += step; if (j >= 0 && j < cs.length) cur = cs[j]; };
    const typeL = L => { if (st.done) return; if (!lock(cur)) { if (L !== sol[cur]) st.mistakes++; u[cur] = L; wrong.delete(cur); } S('tap'); moveIn(1); paint(); focusCur(); after(); };
    const backsp = () => { if (st.done) return; if (u[cur] && !lock(cur)) { u[cur] = ''; wrong.delete(cur); } else { moveIn(-1); if (!lock(cur)) { u[cur] = ''; wrong.delete(cur); } } paint(); focusCur(); persist(st); };
    const gotoEntry = (k, speak) => { const e = p.entries[k], cs = cellsOf(k); dir = e.dir; cur = cs.find(i => !u[i]) ?? cs[0]; paint(speak !== false); focusCur(); };
    const nextEntry = s => { const k = entryAt(cur, dir); gotoEntry((k + s + p.entries.length) % p.entries.length); };
    const arrow = (dy, dx) => { let y = Math.floor(cur / w), x = cur % w; for (;;) { y += dy; x += dx; if (y < 0 || x < 0 || y >= h || x >= w) return; const i = y * w + x; if (sol[i] !== '#') { cur = i; const nd = dx ? 'A' : 'D'; if (at[i][nd] != null) dir = nd; paint(true); focusCur(); return; } } };
    const toggle = () => { const o = dir === 'A' ? 'D' : 'A'; if (at[cur][o] != null) { dir = o; paint(true); } };
    grid.addEventListener('click', e => { const c = e.target.closest('.pz-c[data-i]'); if (!c) return; const i = +c.dataset.i; if (i === cur) toggle(); else { cur = i; if (at[i][dir] == null) dir = dir === 'A' ? 'D' : 'A'; paint(true); } c.focus({ preventScroll: true }); });
    $$('.pz-cl', el).forEach(b => b.onclick = () => { gotoEntry(+b.dataset.k); grid.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
    $1('#pzDir', el).onclick = toggle;
    $1('#pzRev', el).onclick = () => { if (st.done) return; if (u[cur] === sol[cur]) { const k = entryAt(cur, dir), nx = cellsOf(k).find(i => u[i] !== sol[i]); if (nx == null) { T('This word is already right'); return; } cur = nx; } if (!charge(st, 2, `Revealed ${sol[cur]}`)) return; u[cur] = sol[cur]; rev.add(cur); wrong.delete(cur); S('coin'); paint(); after(); };
    $1('#pzChk', el).onclick = () => { if (st.done) return; const cs = cellsOf(entryAt(cur, dir)); if (cs.every(i => !u[i] || giv.has(i))) { T('Fill some boxes first'); return; } if (!charge(st, 1, 'Checked this word')) return; let bad = 0; cs.forEach(i => { if (u[i] && u[i] !== sol[i]) { wrong.add(i); bad++; } }); S(bad ? 'wrong' : 'correct'); T(bad ? `${bad} box${bad > 1 ? 'es' : ''} to fix (marked red)` : 'Every box so far is right ✓'); paint(); };
    $1('#pzHint', el).onclick = async () => {
      if (st.done || !window.PzWords) return;
      const k = entryAt(cur, dir), e = p.entries[k];
      if (!HC[k]) HC[k] = PzWords.hints(st.sp, e, p.entries.map(x => x.a)).then(l => (HC[k] = l || [])).catch(() => (HC[k] = []));
      const list = HC[k].then ? await HC[k] : HC[k];
      if (!st.ctx.alive() || st.done) return;
      const n = HU[k] || 0, max = Math.min(HMAX, list.length);
      if (n >= max) { T(n ? `All ${max} hints for this word are shown below` : 'No hints for this word'); S('hmm'); return; }
      if (!charge(st, 1, `Hint ${n + 1}: ${list[n].label}. ${list[n].text}`)) return;
      HU[k] = n + 1; persist(st); S('coin'); paint();
    };
    $$('.pz-srcb[data-sk]', el).forEach(b => b.onclick = () => { const r = SRC[+b.dataset.sk]; if (r && r.open) { S('tap'); r.open(); } });
    try { new ResizeObserver(() => { if (st.ctx.alive()) words(); }).observe(grid); } catch (e) {}
    wireKB(el, k => (k === '⌫' ? backsp() : k === '⇥' ? nextEntry(1) : typeL(k)));
    st.key = e => {
      if (!indic && /^[a-zA-Z]$/.test(e.key)) { typeL(e.key.toUpperCase()); return true; }
      if (e.key === 'Backspace' || e.key === 'Delete') { backsp(); return true; }
      if (e.key === 'ArrowRight') { arrow(0, 1); return true; } if (e.key === 'ArrowLeft') { arrow(0, -1); return true; }
      if (e.key === 'ArrowDown') { arrow(1, 0); return true; } if (e.key === 'ArrowUp') { arrow(-1, 0); return true; }
      if (e.key === 'Enter') { nextEntry(e.shiftKey ? -1 : 1); return true; }
      if (e.key === ' ') { toggle(); return true; }
      return false;
    };
    st.speech = () => { const k = entryAt(cur, dir), e = p.entries[k]; return `Chapter crossword, ${p.entries.length} words. ${e.n} ${dirName(e.dir)}, ${e.len} ${indic ? 'boxes' : 'letters'}. ${e.ctx ? e.ctx + '. ' : ''}${e.clue}. So far: ${cellsOf(k).map(i => u[i] || 'blank').join(', ')}. ${indic ? 'Tap an akshara button to fill the box.' : 'Type the letters.'} Enter goes to the next clue, Space switches across and down.`; };
    paint();
  }
  function kbHTML() {
    const rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];
    return `<div class="pz-kb" role="group" aria-label="Letter keyboard">${rows.map((r, j) => `<div class="pz-kr">${j === 2 ? '<button class="pz-k wide" data-key="⇥" aria-label="Next clue">Next ⇥</button>' : ''}${r.split('').map(c => `<button class="pz-k" data-key="${c}">${c}</button>`).join('')}${j === 2 ? '<button class="pz-k wide" data-key="⌫" aria-label="Delete">⌫</button>' : ''}</div>`).join('')}</div>`;
  }
  /* Indic crossword keyboard: every akshara of this puzzle, as whole buttons */
  function trayHTML(tray, lang) {
    return `<div class="pz-kb pz-tray" role="group" aria-label="Akshara keyboard" lang="${lang}"><div class="pz-trayk">${tray.map(c => `<button class="pz-k pz-ak" data-key="${E(c)}">${E(c)}</button>`).join('')}</div>
      <div class="pz-kr"><button class="pz-k wide" data-key="⇥" aria-label="Next clue" lang="en">Next ⇥</button><button class="pz-k wide" data-key="⌫" aria-label="Delete" lang="en">⌫</button></div></div>`;
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
    st.answer = () => u.join('');
    let cur = u.findIndex(v => !v); if (cur < 0) cur = 0; let pencil = false;
    const LS = set && /[ऀ-෿]/.test(set.items.map(i => i.label).join('')) ? ` lang="${st.lang}"` : '';
    const sym = v => (set ? set.items[v - 1].sym : String(v)), lab = v => (set ? set.items[v - 1].label : String(v));
    const title = set ? '🧠 Concept Sudoku' : '🔢 Sudoku', todo = given.filter(x => !x).length;
    el.innerHTML = `<div class="pz-root pz-sdk${set ? ' pz-csdk' : ''}" data-pz="${set ? 'csdk' : 'sdk'}">${header(st, title, `${n}×${n} · ${p.diff}${set ? ' · each symbol once in every row, column and box' : ''}`)}
      ${set ? `<div class="card pz-legend"><h3${LS}>${set.title ? E(set.title) : 'Legend'}</h3><ul${LS}>${set.items.map(it => `<li><span class="pz-sym" aria-hidden="true">${it.sym}</span><b>${E(it.label)}</b>${it.info ? `<small>${E(it.info)}</small>` : ''}</li>`).join('')}</ul></div>` : ''}
      <div class="pz-gridwrap"><div class="pz-sgrid n${n}" id="pzGrid" role="grid"${LS} aria-label="Sudoku, ${n} by ${n}. Arrow keys move; type ${set ? '1 to ' + n + ' for the symbols' : 'a number 1 to ' + n}; P switches pencil marks." style="--n:${n}">
        ${Array.from({ length: n }, (_, y) => `<div role="row" class="pz-row">${Array.from({ length: n }, (_, x) => { const i = y * n + x; return `<div role="gridcell" class="pz-s${given[i] ? ' giv' : ''}${(x + 1) % bw === 0 && x < n - 1 ? ' br' : ''}${(y + 1) % bh === 0 && y < n - 1 ? ' bb' : ''}" data-i="${i}" tabindex="-1"></div>`; }).join('')}</div>`).join('')}
      </div></div>
      <div class="pz-pad n${n}" role="group" aria-label="${set ? 'Symbols' : 'Numbers'}"${LS}>${Array.from({ length: n }, (_, k) => `<button class="pz-num" data-v="${k + 1}" aria-label="${E(lab(k + 1))}"><span>${sym(k + 1)}</span>${set ? `<small>${E(lab(k + 1))}</small>` : ''}</button>`).join('')}</div>
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
        c.innerHTML = v ? `<span class="pz-v">${sym(v)}</span>${set ? `<small class="pz-vl">${E(PC().clip(lab(v), 3))}</small>` : ''}` : pm[i] ? `<span class="pz-pm">${Array.from({ length: n }, (_, k) => (pm[i] >> k) & 1 ? `<i>${sym(k + 1)}</i>` : '<i></i>').join('')}</span>` : '';
        c.classList.toggle('cur', i === cur); c.classList.toggle('bad', bad.has(i)); c.classList.toggle('rev', shown.has(i));
        c.classList.toggle('peer', i !== cur && (r === Math.floor(cur / n) || col === cur % n)); c.classList.toggle('same', !!cv && v === cv && i !== cur);
        c.tabIndex = i === cur ? 0 : -1;
        c.setAttribute('aria-label', `Row ${r + 1}, column ${col + 1}: ${v ? lab(v) : 'empty'}${given[i] ? ', given' : ''}${bad.has(i) ? ', clashes' : ''}${!v && pm[i] ? ', pencil ' + Array.from({ length: n }, (_, k) => (pm[i] >> k) & 1 ? lab(k + 1) : '').filter(Boolean).join(' ') : ''}`);
        c.setAttribute('aria-selected', String(i === cur));
      });
      $1('#pzPen', el).classList.toggle('on', pencil); $1('#pzPen', el).setAttribute('aria-pressed', String(pencil));
      let ok = 0; for (let i = 0; i < N; i++) if (!given[i] && u[i] === p.solution[i]) ok++; st.prog(ok, todo);
    };
    const focusCur = () => { const c = grid.querySelector(`[data-i="${cur}"]`); if (c && D.activeElement && D.activeElement.closest && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const check = () => { persist(st); if (u.every(v => v) && !conflicts().size) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (u.every(v => v)) { T('Every cell is filled, but some clash (red)'); S('hmm'); } };
    const setV = v => {
      if (st.done || given[cur] || shown.has(cur)) { if (given[cur]) { T('That one is given'); S('hmm'); } return; }
      undo.push([cur, u[cur], pm[cur]]); if (undo.length > 300) undo.shift();
      if (pencil && v) { pm[cur] ^= 1 << (v - 1); u[cur] = 0; S('tap'); paint(); persist(st); return; }
      u[cur] = u[cur] === v ? 0 : v; pm[cur] = 0;
      if (u[cur] && u[cur] !== p.solution[cur]) st.mistakes++;
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
    st.speech = () => { const r = Math.floor(cur / n), c = cur % n, left = u.filter(v => !v).length; return `${set ? 'Concept sudoku' : 'Sudoku'}, ${n} by ${n}, ${p.diff}. ${set ? 'Symbols: ' + set.items.map((it, k) => `${k + 1} is ${it.label}`).join('. ') + '. ' : ''}${left} empty cells. Row ${r + 1}, column ${c + 1}: ${u[cur] ? lab(u[cur]) : 'empty'}. Type 1 to ${n}. Arrow keys move. P switches pencil marks.`; };
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
    st.answer = () => p.cells.map((c, i) => (c ? String(u[i]) : '.')).join('');
    const clueA = {}, clueD = {}, runOf = {}; p.runs.forEach((r, k) => { (r.dir === 'A' ? clueA : clueD)[r.clue] = r.sum; r.cells.forEach(i => { (runOf[i] = runOf[i] || {})[r.dir] = k; }); });
    let cur = p.cells.findIndex((v, i) => v && !given[i]); let pencil = false;
    const story = storyOf(st.extra.info, p), todo = p.cells.filter((v, i) => v && !given[i]).length;
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
      let ok = 0; for (let i = 0; i < N; i++) if (p.cells[i] && !given[i] && u[i] === p.solution[i]) ok++; st.prog(ok, todo);
    };
    const focusCur = () => { const c = grid.querySelector(`[data-i="${cur}"]`); if (c && D.activeElement && D.activeElement.closest && D.activeElement.closest('#pzGrid')) c.focus({ preventScroll: true }); };
    const check = () => { persist(st); const full = p.cells.every((v, i) => !v || u[i]); if (full && !errors().bad.size) { st.done = true; paint(); setTimeout(() => finish(st), 450); } else if (full) { T('All filled — check the red runs'); S('hmm'); } };
    const setV = v => {
      if (st.done || cur < 0) return; if (given[cur] || shown.has(cur)) { T('That one is given'); S('hmm'); return; }
      undo.push([cur, u[cur], pm[cur]]);
      if (pencil && v) { pm[cur] ^= 1 << (v - 1); u[cur] = 0; S('tap'); paint(); persist(st); return; }
      u[cur] = u[cur] === v ? 0 : v; pm[cur] = 0; if (u[cur] && u[cur] !== p.solution[cur]) st.mistakes++;
      S(errors().bad.has(cur) ? 'wrong' : 'tap'); paint(); announce(`${u[cur] || 'cleared'}${errors().bad.has(cur) ? ', problem in this run' : ''}`); check();
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

  /* ---------- 🔎 WORD SEARCH (cells are letters or aksharas) ---------- */
  function playWS(el, st, saved) {
    const p = st.p, n = p.n, G = p.grid.map(r => (Array.isArray(r) ? r : r.split(''))), found = new Set(saved && saved.found || []); let a = null, hover = null;
    const cellAt = i => G[Math.floor(i / n)][i % n], U = w => w.u || w.a.split('');
    st.getState = () => ({ found: [...found] });
    st.answer = () => [...found].sort();
    const line = (s, e) => { const y0 = Math.floor(s / n), x0 = s % n, y1 = Math.floor(e / n), x1 = e % n, dy = Math.sign(y1 - y0), dx = Math.sign(x1 - x0), L = Math.max(Math.abs(y1 - y0), Math.abs(x1 - x0));
      if (!(y0 === y1 || x0 === x1 || Math.abs(y1 - y0) === Math.abs(x1 - x0))) return null; return Array.from({ length: L + 1 }, (_, k) => (y0 + dy * k) * n + x0 + dx * k); };
    const cellsOfW = w => Array.from({ length: U(w).length }, (_, k) => (w.r + w.dr * k) * n + w.c + w.dc * k);
    el.innerHTML = `<div class="pz-root pz-ws${st.indic ? ' pz-indic' : ''}" data-pz="ws">${header(st, '🔎 Word search', `Find ${p.words.length} key words. Tap the first ${st.indic ? 'box' : 'letter'}, then the last (or drag).`)}
      <div class="pz-gridwrap"><div class="pz-wgrid" id="pzGrid" role="grid"${st.L} aria-label="Word search, ${n} by ${n}" style="--n:${n}">${G.map((row, y) => `<div role="row" class="pz-row">${row.map((c, x) => `<div role="gridcell" class="pz-w" data-i="${y * n + x}" tabindex="${y + x ? -1 : 0}" aria-label="${E(c)}, row ${y + 1}, column ${x + 1}">${E(c)}</div>`).join('')}</div>`).join('')}</div></div>
      <div class="card pz-wl"><h3>Words <small id="pzWc"></small></h3><ul${st.L}>${p.words.map(w => { const c = p.clues && p.clues[w.a]; return `<li data-w="${E(w.a)}"><b>${E(w.a)}</b>${c && c.clue ? `<small>${E(c.clue)}</small>` : ''}</li>`; }).join('')}</ul></div></div>`;
    wireQuit(el, st);
    const grid = $1('#pzGrid', el);
    const paint = () => {
      const on = new Set(); p.words.forEach(w => { if (found.has(w.a)) cellsOfW(w).forEach(i => on.add(i)); });
      const sel = a != null ? (hover != null ? line(a, hover) || [a] : [a]) : [];
      $$('.pz-w', grid).forEach(c => { const i = +c.dataset.i; c.classList.toggle('got', on.has(i)); c.classList.toggle('sel', sel.includes(i)); });
      $$('.pz-wl li', el).forEach(li => li.classList.toggle('got', found.has(li.dataset.w)));
      $1('#pzWc', el).textContent = `${found.size} of ${p.words.length}`;
      st.prog(found.size, p.words.length);
    };
    const tryLine = (s, e) => {
      const l = line(s, e); if (!l || l.length < 2) return false;
      const key = l.join();
      const w = p.words.find(w => !found.has(w.a) && (cellsOfW(w).join() === key || cellsOfW(w).reverse().join() === key));
      if (!w) { st.mistakes++; return false; }
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
      if (a != null && d0 !== a) { const ok = tryLine(a, d0); if (!ok) { S('hmm'); T(`Not a word — tap its first ${st.indic ? 'box' : 'letter'}, then its last`); } a = null; hover = null; }
      paint();
    };
    grid.addEventListener('pointerup', up); grid.addEventListener('pointercancel', () => { down = null; });
    grid.addEventListener('keydown', e => { const c = e.target.closest('.pz-w'); if (!c) return; let i = +c.dataset.i; const m = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: n, ArrowUp: -n }[e.key];
      if (m) { i = Math.max(0, Math.min(n * n - 1, i + m)); const t = grid.querySelector(`[data-i="${i}"]`); t.focus(); c.tabIndex = -1; t.tabIndex = 0; if (a != null) { hover = i; paint(); } e.preventDefault(); }
      else if (e.key === 'Enter' || e.key === ' ') { if (a == null) { a = i; announce(`Start at ${cellAt(i)}. Move to the last ${st.indic ? 'box' : 'letter'} and press Enter.`); } else { if (!tryLine(a, i)) announce('Not a word.'); a = null; hover = null; } paint(); e.preventDefault(); } });
    st.speech = () => `Word search, ${n} by ${n}. Find: ${p.words.filter(w => !found.has(w.a)).map(w => w.a).join(', ')}. Found ${found.size} of ${p.words.length}. Use the arrow keys and Enter on the first and last ${st.indic ? 'box' : 'letter'}.`;
    paint();
  }

  /* ---------- 🔤 ANAGRAM (tiles are letters or aksharas) ---------- */
  function playAN(el, st, saved) {
    const p = st.p; let k = saved && saved.k || 0, got = saved && saved.got || 0, skipped = saved && saved.skipped || 0, pick = [];
    const answers = (saved && saved.ans) || [], shown = (saved && saved.shown) || [];
    st.getState = () => ({ k, got, skipped, ans: answers.slice(), shown: shown.slice() });
    /* numbered strip: tap any finished word to look at it again (answer + clue); nothing moves on by itself */
    const strip = cur => `<div class="pz-strip" role="group" aria-label="Words">${p.words.map((_, i) => `<button class="pz-sd${i === cur ? ' cur' : i < k ? (shown.includes(i) ? ' sh' : ' ok') : ''}" data-v="${i}" ${i > k || (i === k && cur !== k) ? '' : ''}${i > k ? 'disabled' : ''} aria-label="Word ${i + 1}">${i < k ? (shown.includes(i) ? '💡' : '✓') : i + 1}</button>`).join('')}</div>`;
    const wireStrip = () => $$('.pz-sd', el).forEach(b => b.onclick = () => { const v = +b.dataset.v; S('tap'); if (v < k) review(v); else if (v === k) draw(); });
    function review(i) {
      const w = p.words[i], ans = w.u || w.a.split(''), was = shown.includes(i);
      el.innerHTML = `<div class="pz-root pz-an${st.indic ? ' pz-indic' : ''}" data-pz="an">${header(st, '🔤 Anagram', `Word ${i + 1} of ${p.words.length}`)}${strip(i)}
        <div class="card pz-anc pz-rev"><p class="pz-ctx"${st.L}>${w.ctx ? E(w.ctx) : 'Clue'}</p><h2 class="pz-anq"${st.L}>${E(w.clue)} <span class="pz-enum">${E(w.enum)}</span></h2>
          <div class="pz-slots"${st.L}>${ans.map(c => `<span class="pz-slot ${was ? 'rev' : 'ok'}">${E(c)}</span>`).join('')}</div>
          <p class="pz-revt">${was ? `💡 The answer is <b>${E(w.a)}</b>. Say it aloud and spell it once — it will stick!` : `✅ You unscrambled <b>${E(w.a)}</b>!`}</p>
          <div class="pz-nav">${i > 0 ? '<button class="btn ghost" id="pzPrev">◀ Previous</button>' : '<span></span>'}<button class="btn" id="pzNext">${i + 1 < k ? 'Next ▶' : k >= p.words.length ? 'See my result ▶' : 'Next word ▶'}</button></div></div></div>`;
      wireQuit(el, st); wireStrip();
      const pv = $1('#pzPrev', el); if (pv) pv.onclick = () => { S('tap'); review(i - 1); };
      $1('#pzNext', el).onclick = () => { S('tap'); if (i + 1 < k) review(i + 1); else draw(); };
      st.key = e => { if (e.key === 'ArrowLeft' && i > 0) { review(i - 1); return true; } if (e.key === 'ArrowRight' || e.key === 'Enter') { $1('#pzNext', el).click(); return true; } return false; };
      st.speech = () => was ? `Word ${i + 1}. Clue: ${w.clue}. The answer is ${w.a}.` : `Word ${i + 1}. You unscrambled ${w.a}.`;
    }
    st.answer = () => answers.slice();
    const draw = () => {
      st.prog(k, p.words.length);
      if (k >= p.words.length) { st.done = true; st.pool = Math.max(0, st.pool - skipped * 2); return finish(st, { line: `${got} of ${p.words.length} unscrambled` }); }
      const w = p.words[k], tiles0 = w.t || w.s.split(''), ans = w.u || w.a.split(''); pick = [];
      el.innerHTML = `<div class="pz-root pz-an${st.indic ? ' pz-indic' : ''}" data-pz="an">${header(st, '🔤 Anagram', `Word ${k + 1} of ${p.words.length}`)}${st.race ? '' : strip(k)}
        <div class="card pz-anc"><p class="pz-ctx"${st.L}>${w.ctx ? E(w.ctx) : 'Clue'}</p><h2 class="pz-anq"${st.L}>${E(w.clue)} <span class="pz-enum">${E(w.enum)}</span></h2>
          <div class="pz-slots" aria-live="polite"${st.L}>${ans.map((_, j) => `<span class="pz-slot" data-j="${j}"></span>`).join('')}</div>
          <div class="pz-tiles"${st.L}>${tiles0.map((c, j) => `<button class="pz-lt" data-j="${j}" aria-label="${E(c)}">${E(c)}</button>`).join('')}</div>
          <div class="pz-tools"><button class="pz-tb" id="pzAnBack">⌫ Undo ${st.indic ? 'tile' : 'letter'}</button>${st.race ? '<button class="pz-tb" id="pzAnHint">💡 Next tile <small>2⭐</small></button>' : '<button class="pz-tb" id="pzAnSkip">⏭ Show answer <small>−2⭐</small></button>'}${!st.race && k > 0 ? '<button class="pz-tb" id="pzAnPrev">◀ Previous word</button>' : ''}</div></div></div>`;
      wireQuit(el, st); if (!st.race) { wireStrip(); const pw = $1('#pzAnPrev', el); if (pw) pw.onclick = () => { S('tap'); review(k - 1); }; }
      const slots = $$('.pz-slot', el), tiles = $$('.pz-lt', el);
      const paint = () => { slots.forEach((s, j) => { s.textContent = pick[j] != null ? tiles0[pick[j]] : ''; }); tiles.forEach(t => { t.disabled = pick.includes(+t.dataset.j); }); };
      const chk = () => {
        if (pick.length < ans.length) return;
        const got1 = pick.map(j => tiles0[j]).join('');
        if (got1 === w.a) { answers[k] = got1; got++; S('correct'); slots.forEach(s => s.classList.add('ok')); announce(`Correct: ${w.a}`); k++; persist(st); if (st.race) setTimeout(draw, 800); else setTimeout(() => review(k - 1), 500); }
        else { st.mistakes++; S('wrong'); $1('.pz-slots', el).classList.add('shake'); announce('Not quite. Try again.'); setTimeout(() => { pick = []; paint(); const s = $1('.pz-slots', el); if (s) s.classList.remove('shake'); }, 600); }
      };
      tiles.forEach(t => t.onclick = () => { if (pick.includes(+t.dataset.j) || pick.length >= ans.length) return; pick.push(+t.dataset.j); S('tap'); paint(); chk(); });
      $1('#pzAnBack', el).onclick = () => { pick.pop(); paint(); };
      /* race: no skipping (a race is only won by really solving) — a hint puts the next right tile in place instead */
      if (st.race) $1('#pzAnHint', el).onclick = () => {
        let ok = 0; while (ok < pick.length && tiles0[pick[ok]] === ans[ok]) ok++;
        const keep = pick.slice(0, ok), j = tiles0.findIndex((c, x) => c === ans[ok] && !keep.includes(x)); if (j < 0) return;
        if (!charge(st, 2, `Next is ${ans[ok]}`)) return; pick = keep.concat(j); S('coin'); paint(); chk();
      };
      else $1('#pzAnSkip', el).onclick = () => { skipped++; st.hints++; shown.push(k); announce(`The answer is ${w.a}`); S('hmm'); k++; persist(st); review(k - 1); };
      st.key = e => { if (!st.indic && /^[a-zA-Z]$/.test(e.key)) { const L = e.key.toUpperCase(), t = tiles.find(t => !t.disabled && t.textContent === L); if (t) t.click(); return true; } if (e.key === 'Backspace') { $1('#pzAnBack', el).click(); return true; } return false; };
      st.speech = () => `Anagram ${k + 1} of ${p.words.length}. Clue: ${w.clue}. ${ans.length} ${st.indic ? 'tiles' : 'letters'}. ${st.indic ? 'Tiles' : 'Letters'}: ${tiles0.join(', ')}. ${st.indic ? 'Tap the tiles in order.' : 'Type the letters in order.'}`;
      paint();
    };
    draw();
  }

  /* ================= RACE: one exact puzzle inside someone else's screen ================= */
  function race(hostEl, spec, cbs) {
    cbs = cbs || {}; style();
    const box = D.createElement('div'); box.className = 'pz-race';
    if (hostEl) { hostEl.innerHTML = ''; hostEl.appendChild(box); }
    box.innerHTML = '<div class="pz-root"><div class="card pz-genc"><div class="pz-spin" aria-hidden="true">🧩</div><b>Making the puzzle…</b></div></div>';
    let stopped = false, st = null;
    const api = {
      stop() { stopped = true; if (st) { st.done = true; st.ctx.stop(); if (PLAY === st) PLAY = null; } },
      ready: null };
    api.ready = (async () => {
      const sp = Object.assign({}, spec || {}, { t: kid(spec && spec.t), from: null, daily: null });
      let b = null; try { b = await build(sp); } catch (e) { b = null; }
      if (stopped || !box.isConnected) return { ok: false, same: false };
      if (!b) {
        box.innerHTML = '<div class="pz-root"><div class="card"><p class="sub">🙂 This puzzle could not be made on this phone. Please reload the app and try again.</p></div></div>';
        try { cbs.onError && cbs.onError('build'); } catch (e) {}
        return { ok: false, same: false };
      }
      st = start(box, sp, b, cbs);
      const same = !spec.ph || spec.ph === phash(b.p);
      if (!same) console.warn('Puzzles.race: this phone built a different puzzle from the spec (content version differs)');
      return { ok: true, same };
    })();
    return api;
  }
  function raceDone(st) {
    if (st.finished) return; st.finished = true; st.done = true;
    const ms = Date.now() - st.t0; st.ctx.stop(); if (PLAY === st) PLAY = null;
    const stars = Math.max(0, st.pool);
    if (stars) { try { addXP(stars, 'Puzzle solved!'); } catch (e) {} }
    S('unlock');
    const r = st.root.querySelector('.pz-root');
    if (r) r.insertAdjacentHTML('afterbegin', `<div class="card pz-racedone" role="status"><b>🎉 Solved in ${fmtT(Math.round(ms / 1000))}!</b>${stars ? ` <span>+${stars} ⭐</span>` : ''}</div>`);
    announce(`Solved in ${fmtT(Math.round(ms / 1000))}!`);
    let answer = null; try { answer = st.answer ? st.answer() : null; } catch (e) {}
    try { st.race.onSolved && st.race.onSolved({ ms, hints: st.hints, mistakes: st.mistakes, answer }); } catch (e) { console.warn(e); }
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
    if (st.race) return raceDone(st);
    if (st.finished) return; st.finished = true; o = o || {};
    try { if (window.LeaveGuard) LeaveGuard.disarm(); } catch (e) {}
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
    const m = TYPES[sp.t], L = st.L;
    const recap = sp.t === 'xw' ? p.entries.map(e => [e.disp || e.a, e.clue]) : sp.t === 'an' ? p.words.map(w => [w.a, w.clue]) : sp.t === 'ws' ? p.words.map(w => [w.a, (p.clues && p.clues[w.a] && p.clues[w.a].clue) || '']) : null;
    el.innerHTML = `<div class="pz-root pz-res" data-pz="res"><p class="pz-live sr-only" aria-live="polite"></p><div class="card done-card pz-rescard"><div class="confetti">${Array.from({ length: 14 }, (_, j) => `<span style="left:${(j * 7.3 + 3) % 100}%;animation-delay:${(j % 5) * .15}s">${['🎉', '⭐', '✨', '🧩'][j % 4]}</span>`).join('')}</div>
      <div class="pz-rese" aria-hidden="true">${m.e}</div><h2>Solved!</h2><p class="pz-resn">${m.n}${p.n && sp.t !== 'ws' ? ` ${p.n}×${p.n}` : ''}${p.diff ? ' · ' + E(p.diff) : ''}</p>
      ${sp.t !== 'an' ? `<div class="pz-rest"><span>⏱ <b>${fmtT(st.secs)}</b></span>${isBest ? '<span class="pz-best1">🏆 Best time!</span>' : `<span>Best ${fmtT(z.best[bk])}</span>`}</div>` : ''}
      <div class="arc-xp">${first ? `+${stars} ⭐` : 'Already solved — stars were given the first time'}</div>
      ${dailyMsg ? `<p class="sub">${E(dailyMsg)}</p>` : ''}${lines.map(l => `<p class="sub">${E(l)}</p>`).join('')}
      ${fresh.length ? `<p class="pz-newb">🏅 ${fresh.map(E).join(' · ')}</p>` : ''}
      ${recap ? `<details class="pz-recap"><summary>📖 Review the words</summary><ul${L}>${recap.map(([a, c]) => `<li><b>${E(a)}</b>${c ? ' — ' + E(c) : ''}</li>`).join('')}</ul></details>` : ''}
      <button class="btn mint" id="pzAgain">🧩 New ${E(m.n.toLowerCase())}</button><div style="height:8px"></div>
      <button class="btn ghost" id="pzHome">${sp.from && sp.from.t === 'chap' ? 'Back to this chapter\'s puzzles' : sp.from && sp.from.t === 'quick' ? 'Pick another' : 'Back to puzzles'}</button></div></div>`;
    S('unlock');
    $1('#pzAgain').onclick = () => { S('tap'); play(Object.assign({}, sp, { seed: nextSeed(scopeKey(sp.sc), sp.t), daily: null })); };
    $1('#pzHome').onclick = () => { S('tap'); goBack(sp); };
    announce(`Solved! ${sp.t !== 'an' ? 'Time ' + fmtT(st.secs) + '. ' : ''}${first ? stars + ' stars.' : ''} ${dailyMsg}`);
  }

  /* ================= keys (physical keyboard) ================= */
  D.addEventListener('keydown', e => {
    if (!PLAY || !PLAY.key || PLAY.done || e.ctrlKey || e.metaKey || e.altKey) return;
    if (PLAY.race) { if (!PLAY.root.isConnected) return; }
    else { const s = D.getElementById('s-puz'); if (!s || !s.classList.contains('active')) return; }
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
    const pk = $1('.pz-pick', r);
    if (pk) { const h2 = $1('h2', pk), ch = $1('.pz-chb.on .pz-cht', pk), stt = $1('#pzStat', pk); return `${h2 ? h2.textContent : 'Puzzle'}. ${ch ? 'Chapter: ' + ch.textContent + '. ' : ''}${stt ? stt.textContent + '. ' : ''}Pick a ${$1('#pzChl', pk) ? 'subject, chapter and ' : ''}difficulty, then press Play.`; }
    const h = $1('.hello,h2', r), games = $$('.pz-game', r).map(b => `${b.querySelector('b').textContent}: ${b.querySelector('small').textContent}`);
    const dl = $1('#pzDaily h2', r);
    return `${h ? h.textContent : 'Puzzles'}. ${dl ? 'Daily puzzle: ' + dl.textContent + '. ' : ''}${games.length ? 'Puzzles: ' + games.join('. ') + '.' : ''} Use Tab to move between buttons.`;
  }

  /* ================= entry points (the Puzzles tiles now live in the 🎮 Play hub, js/playhub.js) ================= */
  function place() {
    { const ps = D.getElementById('s-puz'); D.documentElement.classList.toggle('pz-playing', !!(ps && ps.classList.contains('active') && ps.querySelector('[data-pz]:not([data-pz="res"])'))); }   // floating Ask / calculator buttons would cover the grid or keyboard
    const s0 = STx(); if (!s0 || !s0.profile) return;
    try { if (window.Cloud && Cloud.isParent && Cloud.isParent()) return; } catch (e) {}
    const put = (host, ref, where, html, sel, fn) => { if (!host || !ref || host.querySelector(sel)) return; ref.insertAdjacentHTML(where, html); const b = host.querySelector(sel); if (b) b.onclick = () => { S('open'); fn(); }; };
    const act = id => { const e = D.getElementById(id); return e && e.classList.contains('active') ? e : null; };
    let w;
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
.pz-chl{display:flex;flex-direction:column;gap:6px;margin-top:8px}.pz-chb{display:flex;gap:8px;align-items:center;text-align:left;border:0;border-radius:12px;padding:9px 10px;background:#f4f5fb;color:var(--ink);font:600 14px Nunito,sans-serif;cursor:pointer}.pz-chb .pz-chn,.pz-chb > span:first-child{min-width:24px;height:24px;border-radius:8px;background:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:12px}
.pz-stats{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;margin-top:8px}.pz-best{display:flex;flex-wrap:wrap;gap:6px}.pz-best span{background:#f4f5fb;border-radius:10px;padding:5px 8px;font-size:12.5px}
.pz-chead{display:flex;gap:12px;align-items:center}.pz-ce{font-size:38px}
.pz-genc{text-align:center;padding:30px 16px}.pz-spin{font-size:40px;animation:pzSpin 1.2s linear infinite;display:inline-block}@keyframes pzSpin{to{transform:rotate(360deg)}}
.pz-bar{display:flex;align-items:center;gap:8px;color:#fff;margin:2px 0 4px}.pz-x{border:0;background:rgba(255,255,255,.14);color:#fff;border-radius:999px;padding:8px 12px;font:700 13px Nunito,sans-serif;cursor:pointer;min-height:36px}
.pz-title{flex:1;font-family:'Baloo 2';font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pz-time,.pz-prize{background:rgba(255,255,255,.14);border-radius:999px;padding:5px 9px;font-weight:800;font-size:13px;font-variant-numeric:tabular-nums}
.pz-sub{color:#fff;opacity:.85;font-size:12.5px;margin:0 2px 6px}
.pz-how{background:#fff;color:#1b1f3a;border-radius:14px;padding:8px 12px;margin:2px 0 8px;font-size:14px;line-height:1.45}.pz-how summary{cursor:pointer;font-weight:800;list-style:none}.pz-how summary::-webkit-details-marker{display:none}.pz-how summary::after{content:' ▾';opacity:.6}.pz-how:not([open]) summary::after{content:' ▸'}.pz-how ol{margin:6px 0 2px;padding-left:20px}.pz-how li{margin:4px 0}
.pz-gridwrap{background:var(--card);border-radius:16px;padding:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);margin-bottom:8px;overflow-x:auto}
.pz-row{display:flex}
.pz-xgrid{display:flex;flex-direction:column;width:min(100%, calc(var(--w) * 34px));margin:0 auto}
.pz-xgrid .pz-c{flex:1 1 0;aspect-ratio:1;position:relative;border:1px solid #2b2f48;margin:0 -1px -1px 0;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;font:800 clamp(13px,4.2vw,19px) 'Baloo 2',sans-serif;color:#1b1f3a;text-transform:uppercase;outline:none;min-width:0}
.pz-xgrid .pz-c.blk{background:transparent;border-color:transparent;cursor:default}
.pz-xgrid .pz-n{position:absolute;top:0;left:2px;font:700 9px Nunito,sans-serif;color:#555}
.pz-xgrid .pz-c.word{background:#fff3c4}.pz-xgrid .pz-c.cur{background:#ffc93c}.pz-xgrid .pz-c.rev .pz-l{color:#7646ea}.pz-xgrid .pz-c.bad .pz-l{color:#d62828;text-decoration:line-through}
.pz-xgrid{position:relative}.pz-wb{position:absolute;pointer-events:none;border-radius:3px;z-index:2;box-sizing:border-box}
.pz-wb.ok{box-shadow:inset 0 0 0 1.5px #1f9d55}.pz-wb.bad{box-shadow:inset 0 0 0 1.5px #e03131}
.pz-whelp:empty{display:none}.pz-whelp{margin:-2px 0 8px}
.pz-hlist{margin:0 0 6px;padding:8px 10px 8px 28px;background:#f4efff;border-radius:12px;font-size:13.5px;line-height:1.4;color:#1d1f3a}.pz-hlist li{margin:3px 0}
.pz-srcb{display:block;width:100%;text-align:left;border:0;border-radius:10px;padding:6px 10px;margin:4px 0 0;font:700 12.5px/1.35 Nunito,sans-serif;cursor:pointer;background:#eaf8ef;color:#156b3b}
.pz-srcb.bad{background:#fdecec;color:#a61e22}.pz-srcb[hidden]{display:none}.pz-srcb u{white-space:nowrap}
.pz-saved .pz-svrow{display:flex;gap:6px;align-items:stretch;margin-top:8px}.pz-svgo{flex:1;display:flex;gap:10px;align-items:center;text-align:left;border:0;border-radius:14px;padding:10px 12px;background:#fff7e0;cursor:pointer;color:var(--ink);font:inherit}
.pz-svgo>span:first-child{font-size:24px}.pz-svgo b{display:block}.pz-svgo small{display:block;color:var(--muted);font-size:12px}.pz-svp{margin-left:auto;font-weight:800;color:#7646ea;white-space:nowrap}
.pz-svx{border:0;border-radius:14px;background:#f3f3f8;padding:0 12px;cursor:pointer;font-size:16px}
.pz-c:focus-visible,.pz-s:focus-visible,.pz-k1:focus-visible,.pz-w:focus-visible{box-shadow:inset 0 0 0 3px #2563eb}
.pz-cluebar{background:#fff;border-radius:14px;padding:9px 12px;margin-bottom:8px;font-size:14.5px;line-height:1.35;min-height:44px;box-shadow:0 4px 14px rgba(0,0,0,.14)}
.pz-ctx{color:var(--muted);font-size:12.5px}.pz-enum{color:var(--muted);font-weight:800;white-space:nowrap}.pz-near{color:#7646ea;font-weight:800}
.pz-strip{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:6px 0 8px}.pz-sd{min-width:34px;height:34px;border:0;border-radius:50%;background:#eef0fb;color:var(--ink);font:800 13px Nunito,sans-serif;cursor:pointer}.pz-sd.ok{background:#d6f5e6;color:#137a4b}.pz-sd.sh{background:#fff1c2}.pz-sd.cur{background:var(--violet);color:#fff;box-shadow:0 0 0 3px rgba(108,92,231,.25)}.pz-sd:disabled{opacity:.45;cursor:default}.pz-nav{display:flex;gap:8px;justify-content:space-between;margin-top:10px}.pz-nav .btn{flex:1}.pz-revt{text-align:center;font-size:16px;margin:8px 0}.pz-tools{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 8px}.pz-tb{flex:1 1 auto;border:0;border-radius:12px;padding:9px 10px;background:#eef0fb;color:var(--ink);font:700 13px Nunito,sans-serif;cursor:pointer;min-height:40px}.pz-tb small{opacity:.7}.pz-tb.on{background:var(--violet);color:#fff}
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
.pz-phead{display:flex;gap:12px;align-items:center}.pz-pe{font-size:40px}.pz-phead h2{margin:0}
.pz-lab{display:block;font-weight:800;font-size:12px;color:var(--muted);margin-top:6px}
.pz-subs{display:flex;gap:8px;overflow-x:auto;padding:2px 2px 8px;scrollbar-width:thin}
.pz-sbj{flex:0 0 auto;border:0;border-radius:999px;padding:10px 14px;min-height:44px;background:#eef0fb;color:var(--ink);font:800 14px Nunito,sans-serif;cursor:pointer;white-space:nowrap}.pz-sbj.on{background:var(--violet);color:#fff}
.pz-chlist{display:flex;flex-direction:column;gap:6px;max-height:300px;overflow-y:auto;padding:2px}
.pz-chlist .pz-chb{min-height:48px;flex-wrap:wrap}.pz-chb .pz-cht{display:block;background:none;height:auto;text-align:left;font-weight:700}.pz-chb.on{background:var(--violet);color:#fff}.pz-chb.on .pz-chn{color:var(--ink)}.pz-cht{flex:1;min-width:0}
.pz-here{flex-basis:100%;padding-left:32px;font-size:11.5px;font-weight:800;opacity:.85}
.pz-chip{min-height:44px;padding:9px 14px;font-size:14px}
.pz-status{background:#fff;border-radius:14px;padding:10px 12px;margin:0 0 8px;font-weight:700;font-size:14px;color:#1b1f3a;min-height:20px}
.pz-alt{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}.pz-altb{background:#fff3c4}
.pz-go{font-size:18px;min-height:54px}.pz-go:disabled{opacity:.5}
.pz-sheet-in{max-height:92vh;overflow-y:auto;background:#eef0fb}.pz-sheet .pz-root .card{margin-bottom:10px}.pz-sheet .pz-status{box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.pz-race{background:linear-gradient(160deg,#2b2f6b,#1b1f3a);border-radius:18px;padding:10px;color:#fff}.pz-race .pz-root{color:var(--ink)}.pz-race .pz-bar,.pz-race .pz-sub{color:#fff}
.pz-racedone{display:flex;gap:10px;align-items:center;justify-content:center;font-size:17px;background:#d9fbe9}
.pz-indic .pz-c,.pz-indic .pz-w{font-family:'Baloo 2','Noto Sans Devanagari','Nirmala UI',sans-serif;text-transform:none}
.pz-indic .pz-xgrid .pz-c{font-size:clamp(11px,3.6vw,17px)}.pz-indic .pz-w{font-size:clamp(13px,4.4vw,19px)}
.pz-xgrid .pz-c.giv .pz-l{color:#0a7d55}
.pz-trayk{display:flex;flex-wrap:wrap;gap:5px;justify-content:center}.pz-ak{flex:0 0 auto;min-width:44px;max-width:none;padding:0 8px;font-family:'Baloo 2','Noto Sans Devanagari','Nirmala UI',sans-serif;font-size:18px}
.pz-indic .pz-lt{width:auto;min-width:46px;padding:0 8px;font-family:'Baloo 2','Noto Sans Devanagari','Nirmala UI',sans-serif}.pz-indic .pz-slot{width:auto;min-width:40px;padding:0 4px}
html[data-age=pro] .pz-sbj.on,html[data-age=pro] .pz-chb.on{background:#1f5fd1}
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
  if (window.Nav) { hub = Nav.route('puz.hub', hub); chapter = Nav.route('puz.chapter', chapter); play = Nav.route('puz.play', play); quick = Nav.route('puz.quick', quick); }
  window.Puzzles = {
    kinds: () => KINDS.map(k => Object.assign({}, k)),
    hub: o => hub(o || {}), quick: (kind, o) => quick(kid(kind), o || {}), pick: kind => pick(kid(kind)), race, describe,
    chapter: (sc, from) => chapter(sc, from), play: sp => play(sp), daily: async () => play(await dailySpec()), build,
    saved: () => Object.entries(Z().saves).filter(([, v]) => v && v.kept && v.sp && KM[v.sp.t]).sort((a, b) => b[1].at - a[1].at).map(([id, v]) => ({ id, e: (TYPES[v.sp.t] || KM[v.sp.t]).e, n: (TYPES[v.sp.t] || KM[v.sp.t]).n, label: [v.title, DN[v.sp.diff] || v.sp.diff].filter(Boolean).join(' · '), at: v.at, kind: 'puzzle' })),
    resumeSaved: id => { const v = Z().saves[id]; if (v && v.sp) play(Object.assign({}, v.sp)); },
    dropSaved: id => { const z = Z(); delete z.saves[id]; try { save(); } catch (e) {} },
    speech, terms, _terms: terms, curChapter, dailySpec, _Z: Z, _state: () => PLAY };
})();
