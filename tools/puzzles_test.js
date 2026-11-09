/* Puzzle engine test harness (node tools/puzzles_test.js [count-scale]).
   - 500 random Sudokus (4×4 / 6×6 / 9×9 × easy / medium / hard): valid solution, clues match, exactly one solution
     (independent solver count), easy/medium solvable by singles, deterministic per seed.
   - 500 random Kakuros (easy … expert): runs ≥ 2, no repeats, sums right, givens match, exactly one solution.
   - 200 crosswords from random school + CA chapters (with nearby-chapter fill, as the app does): grid legality
     (every across/down run is an entry, nothing isolated, connected, numbering), 8–15 entries, answers A–Z 3–12,
     enumeration adds up, clue does not contain its answer, no clue gives away another answer, deterministic.
   - word searches: each word found exactly once.
   - every Hindi / Sanskrit chapter (Indic scripts): aksharas are whole (no cell starts with a matra / halant / nukta;
     Intl.Segmenter and the no-Segmenter fallback agree), crossword / word search / anagram / concept sudoku for every
     difficulty: valid, deterministic, every answer is a word of THIS chapter, tiles are the answer's aksharas.
   - many real chapters of every grade and subject + CA: chapter puzzles use only the chapter's own words (crossword
     words marked ↗ come from the neighbouring chapters of the same subject).
   - server answer key: solutionOf(spec, content-from-disk) === the answer read back from the built grid the way the
     UI reads it, for every kind (school, Hindi, CA); contentPathOf lists the files; the core loads without window.
   Prints timings (generation must stay well under 300 ms on a phone; the app also runs it in a Web Worker). */
'use strict';
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const P = require(path.join(ROOT, 'js/puzzles-core.js'));
const K = require(path.join(ROOT, 'js/ca-keys-data.js'));
const scale = +process.argv[2] || 1;
const r = P.rng('harness');
let fails = 0; const fail = (what, why) => { fails++; if (fails < 40) console.log('FAIL', what, why); };
const time = f => { const t = process.hrtime.bigint(); const v = f(); return [v, Number(process.hrtime.bigint() - t) / 1e6]; };
const stats = (name, ms) => { ms.sort((a, b) => a - b); console.log(`${name}: n=${ms.length} median ${ms[ms.length >> 1].toFixed(1)} ms · p95 ${ms[Math.floor(ms.length * .95)].toFixed(1)} ms · max ${ms[ms.length - 1].toFixed(1)} ms`); };

/* ---------- Sudoku ---------- */
{
  const ms = [], N = 500 * scale;
  for (let i = 0; i < N; i++) {
    const n = [4, 6, 9][i % 3], d = ['easy', 'medium', 'hard'][Math.floor(i / 3) % 3], seed = 'h' + i + '-' + Math.floor(r() * 1e9);
    const [p, t] = time(() => P.sudoku(n, d, seed)); ms.push(t);
    const v = P.validSudoku(p); if (v) fail(`sudoku ${n} ${d} ${seed}`, v);
    if (d !== 'hard' && !P.sdkLogic(p.puzzle, n, d === 'medium')) fail(`sudoku ${n} ${d} ${seed}`, 'not solvable by singles');
    if (i % 25 === 0 && JSON.stringify(P.sudoku(n, d, seed)) !== JSON.stringify(p)) fail('sudoku determinism', seed);
  }
  stats('sudoku', ms);
}
/* ---------- Kakuro ---------- */
{
  const ms = [], N = 500 * scale; let giv = 0;
  for (let i = 0; i < N; i++) {
    const d = ['easy', 'medium', 'hard', 'expert'][i % 4], seed = 'k' + i + '-' + Math.floor(r() * 1e9);
    const [p, t] = time(() => P.kakuro(0, d, seed)); ms.push(t);
    if (!p) { fail(`kakuro ${d} ${seed}`, 'null'); continue; }
    giv += p.givens;
    const v = P.validKakuro(p); if (v) fail(`kakuro ${d} ${seed}`, v);
    if (i % 25 === 0 && JSON.stringify(P.kakuro(0, d, seed)) !== JSON.stringify(p)) fail('kakuro determinism', seed);
  }
  stats('kakuro', ms); console.log(`kakuro: average givens ${(giv / N).toFixed(1)}`);
}
/* ---------- Crosswords from real chapters ---------- */
function schoolChapters() {
  const out = [];
  for (let g = 1; g <= 12; g++) {
    const dir = path.join(ROOT, 'content', 'g' + g); if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f)));
      d.chapters.forEach((c, ci) => out.push({ key: `g${g}/${f.replace('.json', '')}/c${ci}`, own: () => P.termsSchool(c), near: () => { const l = []; for (let j = 1; j <= 3; j++) [ci - j, ci + j].forEach(x => { if (d.chapters[x]) l.push(...P.termsSchool(d.chapters[x])); }); return l; } }));
    }
  }
  return out;
}
function caChapters() {
  const st = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/ca/foundation/structure.json'))), out = [];
  const unitsOf = c => c.units.filter(u => u.status === 'built').map(u => { const d = JSON.parse(fs.readFileSync(path.join(ROOT, u.file))); const bf = path.join(ROOT, `content/ca/foundation/${u.id.split('-')[1]}/bank/${u.id}.json`); if (fs.existsSync(bf)) d.mcqs = (d.mcqs || []).concat(JSON.parse(fs.readFileSync(bf)).mcq || []); return d; });
  const terms = c => P.termsCA(unitsOf(c), K.ITEMS.filter(it => c.units.some(u => u.id === it.u)));
  st.papers.forEach(p => p.chapters.forEach((c, i) => out.push({ key: c.id, own: () => terms(c), near: () => { const l = []; for (let j = 1; j <= 3; j++) [i - j, i + j].forEach(x => { if (p.chapters[x]) l.push(...terms(p.chapters[x])); }); return l; } })));
  return out;
}
{
  const chs = schoolChapters(), cas = caChapters(), ms = [], N = 200 * scale; let made = 0, notMade = 0, skipped = 0, words = 0, nearW = 0; const sizes = {};
  const cache = new Map(), get = ch => { if (!cache.has(ch.key)) cache.set(ch.key, { own: ch.own(), near: ch.near() }); return cache.get(ch.key); };
  for (let i = 0; made < N && i < N * 4; i++) {
    const ch = i % 4 === 3 ? cas[Math.floor(r() * cas.length)] : chs[Math.floor(r() * chs.length)], t = get(ch);
    if (t.own.length < 3 || t.own.length + t.near.length < 8) { skipped++; continue; }
    const seed = `xw|${ch.key}|${i}`;
    const [x, ms1] = time(() => P.chapterCrossword(t.own, t.near, seed)); ms.push(ms1);
    if (!x) { notMade++; console.log(`note: no crossword for ${ch.key} (own ${t.own.length}, near ${t.near.length}) — the app offers a sudoku instead`); continue; }
    made++; words += x.entries.length; nearW += x.entries.filter(e => e.near).length; sizes[`${x.w}x${x.h}`] = (sizes[`${x.w}x${x.h}`] || 0) + 1;
    const v = P.validCrossword(x); if (v) fail(`crossword ${ch.key}`, v);
    x.entries.forEach(e => {
      if (!/^\(\d+([,-]\d+)*\)$/.test(e.enum)) fail(`crossword ${ch.key}`, 'enum ' + e.enum);
      x.entries.forEach(o => { if (o !== e) { const C = ' ' + o.clue.toUpperCase().replace(/[^A-Z]+/g, ' ') + ' '; if (C.includes(' ' + e.a + ' ')) fail(`crossword ${ch.key}`, `${o.a}'s clue gives away ${e.a}`); } });
    });
    if (i % 20 === 0 && JSON.stringify(P.chapterCrossword(t.own, t.near, seed)) !== JSON.stringify(x)) fail('crossword determinism', seed);
    if (i % 10 === 0) { const ws = P.wordsearch(t.own.map(w => w.a).slice(0, 8), 12, 8, seed); if (ws) { const wv = P.validWordsearch(ws); if (wv) fail('wordsearch ' + ch.key, wv); } }
  }
  stats('crossword', ms);
  console.log(`crossword: ${made} made, ${notMade} could not be laid out, ${skipped} chapters skipped (no English key terms, e.g. Hindi/Sanskrit), avg ${(words / made).toFixed(1)} words (${(nearW / made).toFixed(1)} from nearby chapters); sizes ${JSON.stringify(sizes)}`);
  // coverage: how many chapters can have a crossword at all
  let ok = 0; chs.concat(cas).forEach(ch => { const t = get(ch); if (t.own.length >= 3 && t.own.length + t.near.length >= 8) ok++; });
  console.log(`coverage: ${ok} of ${chs.length + cas.length} chapters have enough terms for a crossword`);
}
/* ---------- Indic scripts: every Hindi / Sanskrit chapter ---------- */
const MARK0 = /^[\p{M}‌‍]/u;
const readJ = f => JSON.parse(fs.readFileSync(path.join(ROOT, f)));
const flat = x => JSON.stringify(x).normalize('NFC');
function uiAnswer(t, p) {   // read the answer back from the grid exactly the way js/puzzles.js does when a student fills it in
  if (t === 'sdk' || t === 'csdk') return p.solution.join('');
  if (t === 'kak') return p.cells.map((c, i) => (c ? String(p.solution[i]) : '.')).join('');
  if (t === 'xw') { const sol = [].concat(...p.grid.map(r => (Array.isArray(r) ? r : r.split('')))); return p.entries.map(e => Array.from({ length: e.len }, (_, j) => sol[(e.r + (e.dir === 'D' ? j : 0)) * p.w + e.c + (e.dir === 'A' ? j : 0)]).join('')); }
  if (t === 'ws') { const G = p.grid.map(r => (Array.isArray(r) ? r : r.split(''))); return p.words.map(w => Array.from({ length: w.u.length }, (_, k) => G[w.r + w.dr * k][w.c + w.dc * k]).join('')).sort(); }
  if (t === 'an') return p.words.map(w => w.u.join(''));
}
{
  let chs = 0, terms = 0, made = {}, hidden = {}, cells = 0;
  const t0 = Date.now();
  for (let g = 1; g <= 12; g++) for (const sid of ['hindi', 'sanskrit']) {
    const f = `content/g${g}/${sid}.json`; if (!fs.existsSync(path.join(ROOT, f))) continue;
    const d = readJ(f);
    d.chapters.forEach((c, ci) => {
      chs++;
      const T = P.termsFromSchool(d, ci), key = `g${g}/${sid}/c${ci}`, text = flat(c);
      if (T.near.length) fail(key, 'Indic chapter borrowed terms from other chapters');
      T.own.forEach(t => {
        terms++;
        if (!t.u) return fail(key, 'Latin term in an Indic chapter ' + t.a);
        if (t.u.join('') !== t.a || P.aksharas(t.a).join('|') !== t.u.join('|') || P.aksharas(t.a, true).join('|') !== t.u.join('|')) fail(key, 'akshara split differs ' + t.a);
        t.u.forEach(x => { cells++; if (MARK0.test(x) || !P.goodCell(x)) fail(key, `cell starts with a mark: ${t.a} → ${t.u.join('|')}`); });
        if (!text.includes(t.a)) fail(key, 'answer not in the chapter ' + t.a);
        if (t.clue && P.leaksIndic(t, t.clue)) fail(key, 'clue gives the answer away ' + t.a);
      });
      for (const k of ['xw', 'ws', 'an', 'csdk']) for (const diff of ['easy', 'medium', 'hard']) {
        const spec = { t: k, sc: { k: 's', g, sid, ci }, seed: `ind|${key}|${diff}`, diff, n: k === 'csdk' ? 6 : undefined };
        const r = P.puzzleFor(spec, T);
        if (!r) { hidden[k] = (hidden[k] || 0) + 1; continue; }
        made[k] = (made[k] || 0) + 1;
        if (diff === 'medium' && JSON.stringify(P.puzzleFor(spec, P.termsFromSchool(readJ(f), ci))) !== JSON.stringify(r)) fail(key, k + ' not deterministic');
        const p = r.p;
        if (k === 'xw') { const v = P.validCrossword(p); if (v) fail(key + ' xw', v); p.grid.forEach(row => row.forEach(x => { if (x !== '#' && MARK0.test(x)) fail(key, 'xw cell ' + x); })); p.entries.forEach(e => { if (!text.includes(e.a)) fail(key, 'xw answer not in chapter ' + e.a); if (e.near) fail(key, 'xw near word'); }); }
        if (k === 'ws') { const v = P.validWordsearch(p); if (v) fail(key + ' ws', v); p.words.forEach(w => { if (!text.includes(w.a)) fail(key, 'ws word not in chapter ' + w.a); }); p.grid.forEach(row => row.forEach(x => { if (MARK0.test(x) || !P.goodCell(x)) fail(key, 'ws cell ' + x); if (!T.own.some(t => t.u.includes(x))) fail(key, 'ws filler not from this chapter ' + x); })); }
        if (k === 'an') p.words.forEach(w => { if (!text.includes(w.a)) fail(key, 'anagram word not in chapter ' + w.a); if (w.t.slice().sort().join('|') !== w.u.slice().sort().join('|') || w.t.join('|') === w.u.join('|')) fail(key, 'anagram tiles ' + w.a); if (!w.clue) fail(key, 'anagram without clue'); });
        if (k === 'csdk') { const v = P.validSudoku(p); if (v) fail(key + ' csdk', v); r.extra.set.items.forEach(it => { if (!text.includes(it.label)) fail(key, 'concept label not in chapter ' + it.label); }); }
        const sol = P.solutionOf(spec, d), ui = uiAnswer(k, p);
        if (JSON.stringify(sol) !== JSON.stringify(ui)) fail(key, `${k} solutionOf differs from the UI answer`);
      }
    });
  }
  console.log(`indic: ${chs} Hindi/Sanskrit chapters, ${terms} terms, ${cells} akshara cells all whole; made ${JSON.stringify(made)}; hidden (too few words) ${JSON.stringify(hidden)} · ${Date.now() - t0} ms`);
  if (P.aksharas('क्षत्रिय').join('|') !== 'क्ष|त्रि|य' || P.aksharas('रविः मातरम्', true).join('|') !== 'र|विः| |मा|त|र|म्' || P.aksharas('क़लम').length !== 3) fail('aksharas', P.aksharas('क्षत्रिय').join('|'));
}
/* ---------- chapter puzzles use the chapter's own words (every grade and subject, CA) ---------- */
{
  let n = 0, near = 0; const kinds = { xw: 0, ws: 0, an: 0, csdk: 0 };
  const lat = s => String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/[^A-Z]/g, '');
  for (let g = 1; g <= 12; g++) {
    const dir = path.join(ROOT, 'content', 'g' + g);
    for (const f of fs.readdirSync(dir)) {
      if (/hindi|sanskrit/.test(f)) continue;
      const d = JSON.parse(fs.readFileSync(path.join(dir, f))), sid = f.replace('.json', '');
      d.chapters.forEach((c, ci) => {
        if ((ci + g) % 3) return;      // a third of all chapters
        const T = P.termsFromSchool(d, ci), own = lat(JSON.stringify(c)), key = `g${g}/${sid}/c${ci}`;
        const order = []; for (let j = 1; j < d.chapters.length && order.length < 6; j++) [ci - j, ci + j].forEach(x => { if (x >= 0 && x < d.chapters.length && order.length < 6) order.push(x); });
        const nb = lat(JSON.stringify(order.map(x => d.chapters[x])));   // the same 6 nearest chapters the app uses
        for (const k of Object.keys(kinds)) {
          const spec = { t: k, sc: { k: 's', g, sid, ci }, seed: 'own|' + key, diff: 'medium', n: 6 }, r = P.puzzleFor(spec, T); if (!r) continue;
          kinds[k]++; n++;
          const words = k === 'xw' ? r.p.entries : k === 'csdk' ? r.extra.set.items.map(i => ({ a: lat(i.label) })) : r.p.words;
          words.forEach(w => { if (w.near) { near++; if (!nb.includes(lat(w.a))) fail(key, `↗ word not from a neighbouring chapter: ${w.a}`); } else if (!own.includes(lat(w.a))) fail(key, `${k} word not from this chapter: ${w.a}`); });
          if (k === 'ws') { const v = P.validWordsearch(r.p); if (v) fail(key, v); }
          if (k === 'xw') { const v = P.validCrossword(r.p); if (v) fail(key, v); }
          if (JSON.stringify(P.solutionOf(spec, d)) !== JSON.stringify(uiAnswer(k, r.p))) fail(key, k + ' solutionOf differs');
        }
      });
    }
  }
  console.log(`school (English + other subjects): ${n} chapter puzzles ${JSON.stringify(kinds)}, every word from its chapter (${near} crossword words ↗ from neighbouring chapters)`);
}
/* ---------- CA: contentPathOf + solutionOf from disk ---------- */
{
  const st = readJ('content/ca/foundation/structure.json'); let n = 0;
  const loadCA = spec => {
    const paths = P.contentPathOf(spec, st), content = { structure: st, units: {}, banks: {}, keyItems: K.ITEMS };
    if (spec.t !== 'kak' && (paths[0] !== 'content/ca/foundation/structure.json' || !paths.includes('js/ca-keys-data.js'))) fail('contentPathOf', paths.slice(0, 3));
    paths.slice(2).forEach(pth => { const full = path.join(ROOT, pth); if (!fs.existsSync(full)) return; const j = JSON.parse(fs.readFileSync(full)); if (/\/bank\//.test(pth)) content.banks[j.unit] = j; else { const uid = (st.papers.flatMap(p => p.chapters.flatMap(c => c.units)).find(u => u.file === pth) || {}).id; content.units[uid] = j; } });
    return content;
  };
  st.papers.forEach(p => p.chapters.forEach((c, i) => {
    if (i % 2) return;
    for (const k of ['xw', 'ws', 'an', 'csdk', 'kak']) {
      const spec = { t: k, sc: { k: 'c', ch: c.id }, seed: 'ca|' + c.id, diff: 'medium', n: 6 }, content = loadCA(spec);
      const r = P.puzzleFor(spec, k === 'kak' ? null : P.termsFor(spec, content)); if (!r) continue; n++;
      if (JSON.stringify(P.solutionOf(spec, content)) !== JSON.stringify(uiAnswer(k, r.p))) fail(c.id, k + ' CA solutionOf differs');
    }
  }));
  for (const [spec, want] of [[{ t: 'sdk', sc: { k: 'q' }, seed: 'a', diff: 'easy', n: 4 }, P.sudoku(4, 'easy', 'a').solution.join('')], [{ t: 'kak', sc: { k: 'q' }, seed: 'b', diff: 'hard' }, null]]) {
    const s1 = P.solutionOf(spec, null); if (!s1 || (want && s1 !== want)) fail('solutionOf numbers', spec.t);
    if (P.contentPathOf(spec).length) fail('contentPathOf numbers', spec.t);
  }
  if (P.contentPathOf({ t: 'ana', sc: { k: 's', g: 7, sid: 'hindi', ci: 2 } })[0] !== 'content/g7/hindi.json') fail('contentPathOf school', '');
  /* the core must load with no window / module (Deno Edge Function) */
  const vm = require('vm'), sb = { console }; sb.globalThis = sb; vm.createContext(sb);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'js/puzzles-core.js'), 'utf8'), sb);
  if (!sb.PuzzleCore || sb.PuzzleCore.solutionOf({ t: 'sdk', seed: 'z', diff: 'medium', n: 6 }, null) !== P.solutionOf({ t: 'sdk', seed: 'z', diff: 'medium', n: 6 }, null)) fail('core without window', 'did not load');
  console.log(`CA: ${n} puzzles — solutionOf from disk content matches; core loads without window`);
}

console.log(fails ? `${fails} FAILURES` : 'ALL PASSED');
process.exit(fails ? 1 : 0);
