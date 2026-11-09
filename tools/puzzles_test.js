/* Puzzle engine test harness (node tools/puzzles_test.js [count-scale]).
   - 500 random Sudokus (4×4 / 6×6 / 9×9 × easy / medium / hard): valid solution, clues match, exactly one solution
     (independent solver count), easy/medium solvable by singles, deterministic per seed.
   - 500 random Kakuros (easy … expert): runs ≥ 2, no repeats, sums right, givens match, exactly one solution.
   - 200 crosswords from random school + CA chapters (with nearby-chapter fill, as the app does): grid legality
     (every across/down run is an entry, nothing isolated, connected, numbering), 8–15 entries, answers A–Z 3–12,
     enumeration adds up, clue does not contain its answer, no clue gives away another answer, deterministic.
   - word searches: each word found exactly once.
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
console.log(fails ? `${fails} FAILURES` : 'ALL PASSED');
process.exit(fails ? 1 : 0);
