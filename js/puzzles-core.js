/* ================= Knowtopia Puzzles — engine (js/puzzles-core.js) =================
   Pure functions, no DOM: used by js/puzzles.js (UI), js/puzzles-worker.js (Web Worker) and the Node test
   harness tools/puzzles_test.js. Every generator is deterministic for a given seed (date + chapter).
     sudoku(n, diff, seed)      n = 4 | 6 | 9 · diff = easy | medium | hard · unique solution (checked by a solver)
     kakuro(size, diff, seed)   size 5–8 (including the clue row and column) · unique solution (checked)
     crossword(cands, seed, o)  8–15 chapter terms on a compact, legal grid (no unintended words)
     wordsearch(words, n, dirs, seed) · scramble(word, seed)
     termsSchool(chapter) / termsCA(units, keyItems) — curated term → clue extraction with checks:
       answer A–Z only (spaces squashed, enumeration like (5,4)), 3–12 letters, answer not inside its clue.
   Validators (validSudoku, validKakuro, validCrossword) are used by the tests and by the UI as a safety net. */
(function (root) {
  'use strict';
  const now = () => (typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now());

  /* ---------------- seeded random ---------------- */
  function hash(s) { let a = 2166136261; for (const ch of String(s)) a = Math.imul(a ^ ch.charCodeAt(0), 16777619) >>> 0; return a; }
  function rng(seed) {
    let a = hash(seed);
    return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  const ri = (r, n) => Math.floor(r() * n);
  function shuffle(a, r) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = ri(r, i + 1); const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  const range = n => Array.from({ length: n }, (_, i) => i);
  const pop = m => { let c = 0; while (m) { m &= m - 1; c++; } return c; };
  const lowBitVal = m => 31 - Math.clz32(m & -m);   // index of the lowest set bit

  /* ======================================================================================
     SCRIPTS — Latin answers use one letter per cell; Indic (Brahmic) answers use one AKSHARA per cell:
     a consonant cluster with its matras, nukta, anusvara/chandrabindu/visarga and halant-joined conjuncts
     (क्ष, स्व, त्र, विः, म्). Intl.Segmenter('grapheme') is used when present and then normalised: a piece that
     starts with a mark joins the previous one, and a piece that ends with a virama joins the next letter. Old and
     new ICU versions (with or without Unicode 15.1 conjunct rules) and the no-Segmenter fallback therefore give
     the SAME cells on every phone, which the race mode (same puzzle on every device) depends on.
     ====================================================================================== */
  const INDIC_RE = /[ऀ-෿]/, LATIN_RE = /[A-Za-z]/;
  const MARK_RE = /^[\p{M}‌‍]/u, VIRAMA_END = /[्্੍્୍్್്][‌‍]?$/u, LETTER0 = /^\p{L}/u;
  const SCRIPTS = [['deva', 0x0900, 0x097F, 'hi'], ['beng', 0x0980, 0x09FF, 'bn'], ['guru', 0x0A00, 0x0A7F, 'pa'], ['gujr', 0x0A80, 0x0AFF, 'gu'], ['orya', 0x0B00, 0x0B7F, 'or'],
    ['taml', 0x0B80, 0x0BFF, 'ta'], ['telu', 0x0C00, 0x0C7F, 'te'], ['knda', 0x0C80, 0x0CFF, 'kn'], ['mlym', 0x0D00, 0x0D7F, 'ml']];
  const scriptOfChar = cp => { for (const x of SCRIPTS) if (cp >= x[1] && cp <= x[2]) return x[0]; return null; };
  /* the main script of a text: 'latn', an Indic script id ('deva' …) or '' */
  function scriptOf(text) {
    const n = {}; let lat = 0;
    for (const ch of String(text || '')) { const cp = ch.codePointAt(0); if (cp < 128) { if (/[A-Za-z]/.test(ch)) lat++; continue; } const sc = scriptOfChar(cp); if (sc) n[sc] = (n[sc] || 0) + 1; }
    let best = '', bn = 0; for (const k in n) if (n[k] > bn) { bn = n[k]; best = k; }
    return bn > lat ? best : lat ? 'latn' : '';
  }
  const langOf = (script, sid) => (script === 'deva' ? (/sanskrit/.test(sid || '') ? 'sa' : /marathi/.test(sid || '') ? 'mr' : 'hi') : ((SCRIPTS.find(x => x[0] === script) || [])[3] || 'en'));
  let SEG = null; try { if (typeof Intl !== 'undefined' && Intl.Segmenter) SEG = new Intl.Segmenter(undefined, { granularity: 'grapheme' }); } catch (e) { SEG = null; }
  function aksharas(text, noSeg) {
    const s = String(text == null ? '' : text).normalize('NFC');
    const raw = SEG && !noSeg ? Array.from(SEG.segment(s), x => x.segment) : Array.from(s);
    const out = [];
    for (const g of raw) {
      const prev = out[out.length - 1];
      if (prev != null && (MARK_RE.test(g) || (VIRAMA_END.test(prev) && LETTER0.test(g) && scriptOfChar(g.codePointAt(0)) === scriptOfChar(prev.codePointAt(0)) && scriptOfChar(g.codePointAt(0)) !== 'taml'))) out[out.length - 1] = prev + g;
      else out.push(g);
    }
    return out;
  }
  /* a cell is a proper akshara: starts with a letter (never a matra / halant / nukta) and is one script */
  const goodCell = c => typeof c === 'string' && c.length > 0 && LETTER0.test(c) && !MARK_RE.test(c);
  const clip = (s, n) => { const a = aksharas(s); return a.length <= n ? String(s) : a.slice(0, n).join('') + '…'; };
  const unitsOf = t => (t && t.u) || String(t && t.a != null ? t.a : t).split('');

  /* ======================================================================================
     SUDOKU — n×n with boxes 2×2 (n=4), 2×3 (n=6), 3×3 (n=9). Digits 1..n, 0 = empty.
     ====================================================================================== */
  const BOX = { 4: [2, 2], 6: [2, 3], 9: [3, 3] };
  const SU = {};
  function sdkUnits(n) {
    if (SU[n]) return SU[n];
    const [bh, bw] = BOX[n], N = n * n, R = new Int8Array(N), C = new Int8Array(N), B = new Int8Array(N), units = [];
    for (let k = 0; k < 3 * n; k++) units.push([]);
    for (let i = 0; i < N; i++) {
      const r = Math.floor(i / n), c = i % n, b = Math.floor(r / bh) * (n / bw) + Math.floor(c / bw);
      R[i] = r; C[i] = c; B[i] = b; units[r].push(i); units[n + c].push(i); units[2 * n + b].push(i);
    }
    return (SU[n] = { n, N, bh, bw, R, C, B, units, full: (1 << n) - 1 });
  }
  /* count solutions (stops at limit) — bitmask DFS with "fewest candidates first" */
  function sdkCount(grid, n, limit) {
    limit = limit || 2;
    const U = sdkUnits(n), g = Array.from(grid), rm = new Int32Array(n), cm = new Int32Array(n), bm = new Int32Array(n), empt = [];
    for (let i = 0; i < U.N; i++) {
      const v = g[i]; if (!v) { empt.push(i); continue; }
      if (v < 1 || v > n) return { count: 0, sol: null };
      const bit = 1 << (v - 1);
      if ((rm[U.R[i]] | cm[U.C[i]] | bm[U.B[i]]) & bit) return { count: 0, sol: null };
      rm[U.R[i]] |= bit; cm[U.C[i]] |= bit; bm[U.B[i]] |= bit;
    }
    let count = 0, sol = null;
    (function dfs() {
      let best = -1, bestM = 0, bestN = 99;
      for (let k = 0; k < empt.length; k++) {
        const i = empt[k]; if (g[i]) continue;
        const m = U.full & ~(rm[U.R[i]] | cm[U.C[i]] | bm[U.B[i]]), c = pop(m);
        if (c < bestN) { bestN = c; best = i; bestM = m; if (c <= 1) break; }
      }
      if (best < 0) { count++; if (!sol) sol = g.slice(); return; }
      if (!bestN) return;
      let m = bestM;
      while (m && count < limit) {
        const bit = m & -m; m ^= bit;
        g[best] = lowBitVal(bit) + 1; rm[U.R[best]] |= bit; cm[U.C[best]] |= bit; bm[U.B[best]] |= bit;
        dfs();
        g[best] = 0; rm[U.R[best]] &= ~bit; cm[U.C[best]] &= ~bit; bm[U.B[best]] &= ~bit;
      }
    })();
    return { count, sol };
  }
  /* human-style solving: naked singles (+ hidden singles). Returns true when it reaches the full solution. */
  function sdkLogic(grid, n, hidden) {
    const U = sdkUnits(n), g = Array.from(grid), rm = new Int32Array(n), cm = new Int32Array(n), bm = new Int32Array(n);
    let left = 0;
    const put = (i, v) => { const bit = 1 << (v - 1); g[i] = v; rm[U.R[i]] |= bit; cm[U.C[i]] |= bit; bm[U.B[i]] |= bit; left--; };
    for (let i = 0; i < U.N; i++) { if (g[i]) { const bit = 1 << (g[i] - 1); rm[U.R[i]] |= bit; cm[U.C[i]] |= bit; bm[U.B[i]] |= bit; } else left++; }
    const cand = i => U.full & ~(rm[U.R[i]] | cm[U.C[i]] | bm[U.B[i]]);
    for (let guard = 0; left > 0 && guard < 400; guard++) {
      let prog = false;
      for (let i = 0; i < U.N; i++) { if (g[i]) continue; const m = cand(i); if (!m) return false; if (!(m & (m - 1))) { put(i, lowBitVal(m) + 1); prog = true; } }
      if (!prog && hidden) {
        for (const u of U.units) {
          for (let d = 0; d < n && !prog; d++) {
            const bit = 1 << d; let at = -1, k = 0;
            for (const i of u) { if (g[i]) { if (g[i] === d + 1) { k = -1; break; } continue; } if (cand(i) & bit) { at = i; k++; } }
            if (k === 1) { put(at, d + 1); prog = true; }
          }
          if (prog) break;
        }
      }
      if (!prog) return false;
    }
    return left === 0;
  }
  function sdkSolved(n, r) {
    const [bh, bw] = BOX[n];
    const rows = shuffle(range(n / bh), r).flatMap(b => shuffle(range(bh), r).map(x => b * bh + x));
    const cols = shuffle(range(n / bw), r).flatMap(s => shuffle(range(bw), r).map(x => s * bw + x));
    const nums = shuffle(range(n).map(x => x + 1), r), tr = bh === bw && r() < .5, g = new Array(n * n);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const a = rows[i], b = cols[j];
      g[(tr ? j : i) * n + (tr ? i : j)] = nums[(bw * (a % bh) + Math.floor(a / bh) + b) % n];
    }
    return g;
  }
  const SDK_TARGET = { 4: { easy: 9, medium: 7, hard: 5 }, 6: { easy: 20, medium: 16, hard: 12 }, 9: { easy: 38, medium: 31, hard: 25 } };
  function sudoku(n, diff, seed) {
    n = BOX[n] ? +n : 9; diff = SDK_TARGET[n][diff] ? diff : 'easy';
    const r = rng(`sdk|${n}|${diff}|${seed}`), sol = sdkSolved(n, r), puz = sol.slice(), N = n * n, target = SDK_TARGET[n][diff];
    const ok = diff === 'easy' ? p => sdkLogic(p, n, false) : diff === 'medium' ? p => sdkLogic(p, n, true) : p => sdkCount(p, n, 2).count === 1;
    let clues = N;
    const cells = shuffle(range(N).filter(i => i <= N - 1 - i), r);   // 180° symmetric pairs
    for (const i of cells) {
      if (clues <= target) break;
      const j = N - 1 - i, a = puz[i], b = puz[j], k = i === j ? 1 : 2;
      puz[i] = 0; puz[j] = 0;
      if (ok(puz)) clues -= k; else { puz[i] = a; puz[j] = b; }
    }
    if (diff === 'hard') {         // second pass: single cells (asymmetric) to get closer to the target
      for (const i of shuffle(range(N), r)) { if (clues <= target) break; if (!puz[i]) continue; const a = puz[i]; puz[i] = 0; if (ok(puz)) clues--; else puz[i] = a; }
    }
    return { type: 'sudoku', n, box: BOX[n], diff, seed: String(seed), puzzle: puz, solution: sol, clues };
  }
  function validSudoku(p) {
    const n = p.n, U = sdkUnits(n), s = p.solution;
    if (!s || s.length !== n * n) return 'bad size';
    for (const u of U.units) { const seen = new Set(u.map(i => s[i])); if (seen.size !== n || [...seen].some(v => v < 1 || v > n)) return 'solution breaks a unit'; }
    for (let i = 0; i < n * n; i++) if (p.puzzle[i] && p.puzzle[i] !== s[i]) return 'clue differs from solution';
    const c = sdkCount(p.puzzle, n, 2);
    if (c.count !== 1) return 'solutions: ' + c.count;
    return '';
  }

  /* ======================================================================================
     KAKURO — grid H×W including the top clue row and left clue column. Cells: 0 block, 1 white.
     Runs of whites (across / down) have length ≥ 2, digits 1–9 never repeat in a run.
     ====================================================================================== */
  const COMBOS = (() => {            // COMBOS[len][sum] = [bitmask of digits (bit d = digit d)]
    const t = []; for (let L = 0; L <= 9; L++) { t.push([]); for (let s = 0; s <= 45; s++) t[L].push([]); }
    for (let m = 0; m < 1024; m += 2) { let s = 0, L = 0; for (let d = 1; d <= 9; d++) if (m & (1 << d)) { s += d; L++; } t[L][s].push(m); }
    return t;
  })();
  function kakRuns(H, W, g) {
    const runs = [], cellRuns = {};                 // cellRuns[i] = [across run index, down run index]
    const at = (r, c) => g[r * W + c];
    for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
      if (at(r, c)) continue;
      if (c + 1 < W && at(r, c + 1)) { const cells = []; let k = c + 1; while (k < W && at(r, k)) { cells.push(r * W + k); k++; } runs.push({ dir: 'A', clue: r * W + c, cells }); }
      if (r + 1 < H && at(r + 1, c)) { const cells = []; let k = r + 1; while (k < H && at(k, c)) { cells.push(k * W + c); k++; } runs.push({ dir: 'D', clue: r * W + c, cells }); }
    }
    runs.forEach((ru, ix) => ru.cells.forEach(i => { (cellRuns[i] = cellRuns[i] || [-1, -1])[ru.dir === 'A' ? 0 : 1] = ix; }));
    return { runs, cellRuns };
  }
  function kakPattern(H, W, r) {
    const N = H * W;
    for (let attempt = 0; attempt < 400; attempt++) {
      const g = new Array(N).fill(0);
      for (let i = 1; i < H; i++) for (let j = 1; j < W; j++) g[i * W + j] = 1;
      const inner = (H - 1) * (W - 1), nb = Math.round(inner * (0.16 + r() * 0.16));
      const blk = (i, j) => { g[i * W + j] = 0; g[(H - i) * W + (W - j)] = 0; };   // 180° symmetric inside the clue frame
      for (let k = 0; k < nb / 2; k++) blk(1 + ri(r, H - 1), 1 + ri(r, W - 1));
      for (let pass = 0; pass < 20; pass++) {     // no white cell may sit in a run of length 1
        let changed = false;
        for (let i = 1; i < H; i++) for (let j = 1; j < W; j++) {
          if (!g[i * W + j]) continue;
          const h = (g[i * W + j - 1] ? 1 : 0) + (j + 1 < W && g[i * W + j + 1] ? 1 : 0), v = (g[(i - 1) * W + j] ? 1 : 0) + (i + 1 < H && g[(i + 1) * W + j] ? 1 : 0);
          if (!h || !v) { blk(i, j); changed = true; }
        }
        if (!changed) break;
      }
      const whites = g.reduce((a, x) => a + x, 0);
      if (whites < inner * 0.55) continue;
      // longest run must stay ≤ 9 (always true here) and whites connected
      const start = g.indexOf(1), seen = new Set([start]), st = [start];
      while (st.length) { const i = st.pop(), rr = Math.floor(i / W), cc = i % W; [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([a, b]) => { const y = rr + a, x = cc + b; if (y < 0 || x < 0 || y >= H || x >= W) return; const k = y * W + x; if (g[k] && !seen.has(k)) { seen.add(k); st.push(k); } }); }
      if (seen.size !== whites) continue;
      return g;
    }
    return null;
  }
  /* a random filling, biased to small and large digits (sums with few combinations keep the answer unique) */
  function kakFill(H, W, g, R, r) {
    const { runs, cellRuns } = R, used = new Int32Array(runs.length), val = new Array(H * W).fill(0);
    const order = []; for (let i = 0; i < H * W; i++) if (g[i]) order.push(i);
    const pref = [1, 9, 2, 8, 3, 7, 4, 6, 5];
    let steps = 0;
    const rec = k => {
      if (k === order.length) return true;
      if (++steps > 20000) return false;
      const i = order[k], [a, d] = cellRuns[i], ban = used[a] | used[d];
      const ds = pref.slice(); for (let x = 0; x < ds.length - 1; x++) if (r() < .45) { const t = ds[x]; ds[x] = ds[x + 1]; ds[x + 1] = t; }
      for (const v of (r() < .2 ? shuffle(ds, r) : ds)) {
        const bit = 1 << v; if (ban & bit) continue;
        used[a] |= bit; used[d] |= bit; val[i] = v;
        if (rec(k + 1)) return true;
        used[a] &= ~bit; used[d] &= ~bit; val[i] = 0;
      }
      return false;
    };
    return rec(0) ? val : null;
  }
  function kakCount(H, W, g, R, sums, limit, given, cap) {
    const { runs, cellRuns } = R, cells = [], used = new Int32Array(runs.length), val = new Array(H * W).fill(0);
    for (let i = 0; i < H * W; i++) if (g[i]) cells.push(i);
    const combos = runs.map((ru, ix) => COMBOS[ru.cells.length][sums[ix]] || []);
    if (combos.some(c => !c.length)) return { count: 0, sol: null };
    const allow = ix => { const U = used[ix]; let m = 0; for (const c of combos[ix]) if ((c & U) === U) m |= c; return m & ~U; };
    let count = 0, sol = null, nodes = 0; const sols = [], CAP = cap || 12000;
    if (given) for (const i of cells) if (given[i]) { const v = given[i], [a, d] = cellRuns[i], bit = 1 << v; if ((used[a] | used[d]) & bit) return { count: 0, sol: null }; used[a] |= bit; used[d] |= bit; val[i] = v; }
    (function dfs() {
      if (++nodes > CAP) { count = Math.max(count, limit); return; }   // too much work: treat as "not unique"
      let best = -1, bestM = 0, bestN = 99;
      for (const i of cells) {
        if (val[i]) continue;
        const [a, d] = cellRuns[i], m = allow(a) & allow(d), c = pop(m);
        if (c < bestN) { bestN = c; best = i; bestM = m; if (c <= 1) break; }
      }
      if (best < 0) { count++; const v = val.slice(); if (!sol) sol = v; sols.push(v); return; }
      if (!bestN) return;
      let m = bestM; const [a, d] = cellRuns[best];
      while (m && count < limit) {
        const bit = m & -m; m ^= bit;
        used[a] |= bit; used[d] |= bit; val[best] = lowBitVal(bit);
        dfs();
        used[a] &= ~bit; used[d] &= ~bit; val[best] = 0;
      }
    })();
    return { count, sol, sols, capped: nodes > CAP };
  }
  /* Size follows the difficulty (5×5 easy … 8×8 hard, clue row/column included). The fill is random; when the sums
     alone allow more than one answer, a few cells are given (pre-filled) until exactly one answer is left —
     at most 25% / 15% / 10% / 12% of the white cells for easy / medium / hard / expert (8×8), otherwise a new grid is tried. */
  const KAK_DIFF = { easy: 5, medium: 6, hard: 7, expert: 8 }, KAK_GIV = { easy: .25, medium: .15, hard: .10, expert: .12 };
  function kakuro(size, diff, seed) {
    diff = KAK_DIFF[diff] ? diff : 'easy';
    size = Math.max(5, Math.min(8, +size || KAK_DIFF[diff]));
    const r = rng(`kak|${size}|${diff}|${seed}`), H = size, W = size, t0 = now();
    for (let tries = 0; tries < 400; tries++) {
      const g = kakPattern(H, W, r); if (!g) continue;
      const R = kakRuns(H, W, g);
      if (R.runs.some(ru => ru.cells.length > 9 || ru.cells.length < 2)) continue;
      const whites = g.reduce((a, x) => a + x, 0), maxG = Math.floor(whites * KAK_GIV[diff]);
      for (let f = 0; f < 3; f++) {
        const val = kakFill(H, W, g, R, r); if (!val) break;
        const sums = R.runs.map(ru => ru.cells.reduce((a, i) => a + val[i], 0)), given = new Array(H * W).fill(0);
        let ng = 0, done = false;
        for (let k = 0; k <= maxG; k++) {
          const c = kakCount(H, W, g, R, sums, 2, given);
          if (c.count === 1 && !c.capped) { done = true; break; }
          if (k === maxG) break;
          const alt = c.capped ? null : c.sols.find(sl => sl.some((v, i) => v !== val[i])); if (!alt && !c.capped) break;
          const diffCells = []; for (let i = 0; i < H * W; i++) if (g[i] && !given[i] && (!alt || alt[i] !== val[i])) diffCells.push(i);   // search too big: give any cell
          const pick = diffCells[ri(r, diffCells.length)]; given[pick] = val[pick]; ng++;
        }
        if (done) {
          return { type: 'kakuro', h: H, w: W, diff, seed: String(seed), cells: g, solution: val, given, givens: ng,
            runs: R.runs.map((ru, ix) => ({ dir: ru.dir, clue: ru.clue, cells: ru.cells, sum: sums[ix] })), tries: tries + 1 };
        }
      }
    }
    return null;
  }
  function validKakuro(p) {
    if (!p) return 'missing';
    const { h: H, w: W, cells: g, solution: s } = p;
    for (let i = 0; i < W; i++) if (g[i]) return 'top row must be clues';
    for (let i = 0; i < H; i++) if (g[i * W]) return 'left column must be clues';
    const R = kakRuns(H, W, g);
    for (let i = 0; i < H * W; i++) if (g[i]) { const cr = R.cellRuns[i]; if (!cr || cr[0] < 0 || cr[1] < 0) return 'white cell outside a run'; if (!(s[i] >= 1 && s[i] <= 9)) return 'bad digit'; }
    if (R.runs.length !== p.runs.length) return 'run count differs';
    for (let k = 0; k < R.runs.length; k++) {
      const ru = R.runs[k], pr = p.runs[k]; if (ru.cells.length < 2) return 'short run';
      if (ru.cells.join() !== pr.cells.join()) return 'run cells differ';
      const ds = ru.cells.map(i => s[i]); if (new Set(ds).size !== ds.length) return 'repeat in a run';
      if (ds.reduce((a, b) => a + b, 0) !== pr.sum) return 'sum mismatch';
    }
    if (p.given) for (let i = 0; i < H * W; i++) if (p.given[i] && (!g[i] || p.given[i] !== s[i])) return 'given differs from solution';
    const c = kakCount(H, W, g, R, p.runs.map(x => x.sum), 2, p.given, 1e9);
    if (c.count !== 1) return 'solutions: ' + c.count;
    return '';
  }

  /* ======================================================================================
     TERMS → CLUES (curated extraction with checks)
     ====================================================================================== */
  const STOP_ANS = new Set(['YES', 'NO', 'TRUE', 'FALSE', 'NONE', 'BOTH', 'ALL', 'ANY', 'THE', 'AND', 'NOT', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'TEN', 'ABOVE', 'BELOW', 'OTHER', 'OTHERS', 'SOME', 'MANY', 'MORE', 'LESS', 'SAME', 'EQUAL', 'INCREASE', 'DECREASE', 'INCREASES', 'DECREASES', 'RISES', 'FALLS', 'ZERO', 'UNITY', 'INFINITE', 'NIL', 'HIGH', 'LOW', 'HIGHER', 'LOWER', 'BIG', 'SMALL', 'LARGE', 'ALWAYS', 'NEVER', 'SOMETIMES', 'CORRECT', 'INCORRECT', 'VALID', 'INVALID']);
  const FUNC = new Set(['TO', 'OF', 'THE', 'A', 'AN', 'NOT', 'IN', 'ON', 'AT', 'IS', 'ARE', 'WAS', 'BE', 'BY', 'FOR', 'AND', 'OR', 'IT', 'AS', 'SO', 'IF']);
  const BAD_CLUE = /\b(which of (the|these)|which one|following|of the above|all of these|none of these|odd one|true or false|true|false|correct (statement|option|answer)|incorrect|match the|statements?|options?|given (below|above)|figure|diagram|table below|shown|picture|passage|extract|paragraph|this (chapter|lesson|poem|story)|in the (poem|story)|above|below)\b/i, BAD_CAPS = /\b(NOT|EXCEPT|INCORRECT)\b/;
  const DEF_Q = /(\b(is|are|was|were) (called|known as|termed|referred to as|named)\b|\bthe (term|name|word) (for|given to|used for)\b|\bwhat (do|does) (we|you) call\b|\bis called\b|\bis the name\b|___|\b(is|are|was|were) (a|an|the)\s*:?\s*$|\b(is|are)\s*:\s*$|\bis termed:?\s*$|\brefers? to:?\s*$|\bknown as:?\s*$|\bcalled:?\s*$|\bmeans:?\s*$)/i;
  const cap1 = s => s.charAt(0).toUpperCase() + s.slice(1);
  const sq = s => String(s).replace(/\s+/g, ' ').trim();
  /* raw answer text → { a: 'LETTERS', disp, enum: '(5,4)' } or null */
  function normAnswer(raw) {
    let t = sq(String(raw == null ? '' : raw).normalize('NFKD').replace(/[̀-ͯ]/g, '')).replace(/[.!?;:,]+$/, '').replace(/^(a|an|the)\s+/i, '');
    if (!t || !/^[A-Za-z][A-Za-z '\-]*[A-Za-z]$/.test(t)) return null;
    const words = t.split(/[ \-]+/).map(w => w.replace(/'/g, '')).filter(Boolean);
    if (!words.length || words.length > 3) return null;
    if (words.length > 1 && words.some(w => w.length < 2 || FUNC.has(w.toUpperCase()))) return null;
    const a = words.join('').toUpperCase();
    if (!/^[A-Z]{3,12}$/.test(a) || STOP_ANS.has(a)) return null;
    if (/^[A-Z]{2,}$/.test(t) && a.length > 5) return null;           // long all-caps strings are usually headings
    const seps = t.match(/[ \-]+/g) || [];
    let en = String(words[0].length); words.slice(1).forEach((w, i) => { en += (/-/.test(seps[i]) ? '-' : ',') + w.length; });
    return { a, disp: t, enum: `(${en})`, words: words.map(w => w.toUpperCase()) };
  }
  /* the answer, or a word built on it, must not appear in the clue */
  function leaks(ans, clue) {
    const C = ' ' + String(clue).toUpperCase().replace(/[^A-Z]+/g, ' ') + ' ', flat = C.replace(/ /g, '');
    if (flat.includes(ans.a)) return true;
    for (const w of ans.words) {
      if (w.length < 3) continue;
      const stem = w.length <= 4 ? w : w.slice(0, Math.max(4, w.length - 3));
      if (C.includes(' ' + stem)) return true;
    }
    return false;
  }
  function cleanClue(raw) {
    let t = sq(String(raw == null ? '' : raw).replace(/\s*\[\d+\]/g, '')).replace(/\s*[:\-–—]+\s*$/, '').replace(/_{2,}/g, '___');
    if (!t) return '';
    t = cap1(t);
    return t;
  }
  /* a clue must read as a plain sentence: no formulas, symbols, shorthand notes (';' '|' '·' '→'), long number runs,
     or "— names, names" example lists. Students must be able to work out the answer from the clue alone. */
  const NOTE = /\s:\s|^case\s*:|\(e\.g|[;|·+→←↔↑↓≈≠≤≥√Σ∑∫∂ⁿ⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉^×÷=<>∝%₹$€£]|\s\/\s|\w\/\w|\u2212|\b[A-Za-z]\s*[\/*+]\s*[A-Za-z]\b|\d+\s*[%:\/]\s*\d+|\(\s*\d|\bsec(tion)?s?\.?\s*\d/i;
  const FRAG = /^(it|this|these|those|they|that|always|never|lower|higher|both|either|same|see|also|only|usually|often|a vital|an important|a key|a major|a basic|an essential|the same|as above|as before|likewise|similarly|name the|add|write|count|multiply|express|put|take|use|find|check|look|draw|read|note|remember|letter positions|drawer writes)\b/i;
  /* a bare list ("Prudence, substance over form, materiality") or a clue that is mostly brackets is not a definition */
  const LISTY = c => { const parts = c.split(/,|\bor\b|\band\b/).map(x => x.trim()).filter(Boolean); const br = (c.match(/\([^)]*\)/g) || []).join('').length; return (parts.length >= 3 && parts.every(x => x.split(/\s+/).length <= 3)) || br > c.length * 0.3; };
  const plainClue = c => !NOTE.test(c) && !FRAG.test(c) && !LISTY(c) && !/—[^—]*,[^—]*,/.test(c) && (c.match(/\d/g) || []).length <= 4 && (c.replace(/[^A-Za-z]/g, '').length / Math.max(1, c.replace(/\s/g, '').length)) > 0.8;
  function clueOK(ans, clue, o) {
    o = o || {};
    if (!plainClue(clue)) return false;
    if (!clue || clue.length < 6 || clue.length > 150) return false;
    if (!/[a-z]/i.test(clue) || /[ऀ-ॿ]/.test(clue)) return false;
    if (BAD_CLUE.test(clue) || BAD_CAPS.test(clue)) return false;
    const blanks = (clue.match(/___/g) || []).length;
    if (blanks > (o.blank ? 1 : 0)) return false;
    if (o.blank && blanks !== 1) return false;
    if (leaks(ans, clue)) return false;
    if (clue.split(/\s+/).length < (o.minWords || 2)) return false;
    if (/^(which|choose|pick|select|identify|tick|circle|underline|fill|complete|rewrite|correct)\b/i.test(clue)) return false;
    if ((clue.match(/\(/g) || []).length !== (clue.match(/\)/g) || []).length) return false;
    return true;
  }
  const NOT_A_THING = /(ED|ING)$|^(VERTICAL|HORIZONTAL|STATEMENT|BALANCE|BASIS|MIXED|FAVOURABLE|UNFAVOURABLE|HALF|QUARTER|DOUBLE|TWICE|FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|ZERO|UNITY|INFINITE|POSITIVE|NEGATIVE|CONSTANT|INDEPENDENT|DEPENDENT|ELASTIC|INELASTIC|PERFECTLY|RELATIVELY|UNITARY|VOID|VOIDABLE|VALID|ILLEGAL|LEGAL|NORMAL|INFERIOR|SUPERIOR|EQUAL|UNEQUAL|SAME|DIFFERENT|DIRECT|INDIRECT|REAL|NOMINAL)$/;
  const GRAMMAR = new Set(['WERE', 'WAS', 'HAVE', 'HAS', 'HAD', 'WILL', 'SHALL', 'WOULD', 'COULD', 'SHOULD', 'MIGHT', 'MUST', 'CAN', 'MAY', 'DOES', 'DID', 'BEEN', 'BEING', 'THEIR', 'THERE', 'THEY', 'THEM', 'THEN', 'THAN', 'THAT', 'THIS', 'THESE', 'THOSE', 'WHICH', 'WHO', 'WHOM', 'WHOSE', 'WHAT', 'WHEN', 'WHERE', 'WHY', 'HOW', 'HER', 'HIS', 'HIM', 'SHE', 'OUR', 'YOUR', 'ITS', 'YOU', 'WITH', 'FROM', 'INTO', 'ONTO', 'UPON', 'OVER', 'UNDER', 'SINCE', 'UNTIL', 'WHILE', 'BUT', 'YET', 'VERY', 'TOO', 'ALSO', 'JUST', 'EVEN', 'MUCH', 'MOST', 'FEW', 'EACH', 'EVERY']);
  const PRI = { def: 6, match: 5, quickref: 5, key: 5, fill: 4, speed: 3, mcq: 3, quiz: 3, point: 2 };
  function cand(raw, clue, src, extra) {
    const ans = normAnswer(raw); if (!ans) return null;
    if (GRAMMAR.has(ans.a)) return null;
    if ((src === 'mcq' || src === 'fill' || src === 'quiz' || src === 'speed') && (NOT_A_THING.test(ans.a) || (ans.words.length > 1 && /^(LESS|MORE|HIGHER|LOWER|GREATER|SMALLER|LARGER|BIGGER|NO|NOT|ONE|TWO|THREE|FOUR|HALF|VERY)$/.test(ans.words[0])) || String(clue).length > 118 || (/\b(the two|the three|the given|the above|this|these|requested by)\b/i.test(String(clue)) || /\b[A-Z]'s\b|\b[A-Z]\b(?! ?[A-Z])/.test(String(clue).replace(/^(A|I)\b/, ''))))) return null;
    const c = cleanClue(clue);
    if (!clueOK(ans, c, { blank: src === 'fill' || (extra && extra.blank), minWords: src === 'quickref' || src === 'def' ? 5 : 2 })) return null;
    return Object.assign({ a: ans.a, disp: ans.disp, enum: ans.enum, clue: c, src, pri: PRI[src] || 1 }, extra || {});
  }
  /* "Term = definition", "Term: definition", "Term — definition", "Term means definition".
     Only plain-language definitions: no second ':' or '=', no figures or symbols, not a long list, and the term is
     not a pointer word ("These", "Types", "Features" …) that only makes sense inside the lesson. */
  const SYM = /[0-9\u00BC-\u00BE\u2150-\u215F×÷+=%₹$²³√π<>→↔∝≈≠≤≥]/;
  const VAGUE = /^(this|these|those|that|it|they|such|both|each|some|many|all|most|other|first|second|third|last|main|key|type|types|kind|kinds|example|examples|feature|features|use|uses|part|parts|step|steps|stage|stages|rule|rules|note|tip|trap|remember|answer|result|formula|method|ways?|links?|relations?|connections?|importance|scope|need|aims?|goals?|roles?|meaning|definition|nature|characteristics|merits|demerits|advantages|disadvantages|limitations|causes|effects|reasons|factors|functions|objectives|principles|elements|components|summary|difference|similarity|typical|next|net|nothing|everything|phases|theories|exam|time|symbols|lags|means|format|order|list|layout|check|shortcut|trick|treatment|entry|entries|journal|position|case|cases|test|tests|why|how|when|where|who|what)\b/i;
  const VERBY = /^(raises|reduces|helps|does|shows|gives|makes|increases|decreases|lowers|has|have|is|are|was|can|may|must|will|no|not|only|also|always|never|used|use|see|go|get|both|either|neither)\b/i;
  const listy = s => (s.match(/,/g) || []).length >= 3 || (s.match(/;/g) || []).length >= 3;
  function defSplit(s) {
    const m = /^\s*([A-Za-z][A-Za-z '\-]{1,40}?)\s*(?:=|:|—|–| means | refers to )\s*(.{8,})$/.exec(String(s || ''));
    if (!m) return null;
    const left = m[1].trim(), right = m[2].trim();
    if (/[:=·]/.test(right) || SYM.test(right) || listy(right) || VAGUE.test(left) || VERBY.test(right)) return null;
    if (right.split(/\s+/).length < 3 || /^[(]/.test(right)) return null;
    return [left, right.replace(/\.$/, '')];
  }
  /* "(A|An|The) Term is/are a ... " → [Term, "A ..."] (only clear definitions: article + ≥ 5 words) */
  function isSplit(s) {
    const m = /^\s*(?:(?:a|an|the)\s+)?([A-Za-z][A-Za-z\-]+(?:\s[A-Za-z][A-Za-z\-]+)?)\s+(?:is|are)\s+((?:a|an|the)\s+.+?)\s*\.?\s*$/i.exec(String(s || ''));
    if (!m || VAGUE.test(m[1])) return null;
    const right = m[2].replace(/[.;]\s.*$/, '');
    if (right.split(/\s+/).length < 5 || /[:·]/.test(right) || SYM.test(right) || listy(right) || /^(a|an|the)\s+(very|bit|lot|kind of|type of|part of|few|same|good|great|big|small|main)\b/i.test(right)) return null;
    return [m[1], cap1(right)];
  }
  /* a chapter's script, from its title and lesson text */
  const chapterScript = ch => scriptOf([ch && ch.title, ...((ch && ch.topics) || []).slice(0, 3).map(t => [t.title, ((t.learn && t.learn.points) || []).join(' ')].join(' '))].join(' '));
  function termsSchool(ch) {
    const scr = chapterScript(ch); if (scr && scr !== 'latn') return termsIndic(ch, scr);
    const out = [];
    const push = x => { if (x) out.push(x); };
    (ch.topics || []).forEach(t => {
      const tid = t.id;
      (t.games || []).forEach(gm => {
        if (!gm) return;
        if (gm.type === 'match') (gm.pairs || []).forEach(p => {
          if (!Array.isArray(p) || p.length < 2) return; const L = String(p[0]), R = String(p[1]);
          const nl = normAnswer(L), nr = normAnswer(R), wl = L.split(/\s+/).length, wr = R.split(/\s+/).length;
          if (nl && wr >= 3 && wr > wl) push(cand(L, R, 'match', { ctx: gm.title || '', tid }));
          else if (nr && wl >= 3 && wl > wr) push(cand(R, L, 'match', { ctx: gm.title || '', tid }));
        });
        else if (gm.type === 'fill') (gm.items || []).forEach(it => { if (it && typeof it.text === 'string') push(cand(it.answer, it.text, 'fill', { tid })); });
        else if (gm.type === 'speed') (gm.items || []).forEach(it => { if (it && typeof it.q === 'string' && !/\d/.test(it.q) && it.q.split(/\s+/).length >= 3) push(cand(it.a, it.q, 'speed', { ctx: gm.title || '', tid })); });
      });
      (t.quiz || []).forEach(q => {
        if (!q || !Array.isArray(q.options) || !DEF_Q.test(q.q || '')) return;
        push(cand(q.options[q.answer], q.q, 'quiz', { tid, blank: /___/.test(q.q) }));
      });
      const rv = t.revise || {};
      (rv.remember || []).forEach(s => { const d = defSplit(s); if (d) push(cand(d[0], d[1], 'def', { tid })); });
      ((t.learn && t.learn.points) || []).forEach(s => { const d = isSplit(s); if (d) push(cand(d[0], d[1], 'point', { tid })); });
    });
    return rank(out);
  }
  /* ---------- Indic-script chapters (Hindi, Sanskrit, …): answers are ONE word of the chapter's own script ---------- */
  const STOP_IN = new Set(['सही', 'गलत', 'ग़लत', 'हाँ', 'हां', 'नहीं', 'दोनों', 'सभी', 'कोई', 'सत्य', 'असत्य', 'आम्', 'न', 'उपर्युक्त', 'कुछ', 'एक', 'दो', 'तीन', 'चार', 'पाँच']);
  /* raw → { a, u: [aksharas], disp, enum: '(n)', words: [a], script } or null. Single word, 2–8 aksharas, all of one Indic script. */
  function normAnswerIndic(raw, script) {
    let t = sq(String(raw == null ? '' : raw).normalize('NFC')).replace(/^[\s'"‘’“”(\[]+|[\s'"‘’“”)\].,!?;:।॥\-–—]+$/g, '');
    if (!t || /[\s\-–—/,.;:'"‘’“”()\[\]0-9०-९।॥?!=+]/.test(t)) return null;
    const sc = scriptOf(t); if (!sc || sc === 'latn' || (script && sc !== script)) return null;
    for (const ch of t) { const cp = ch.codePointAt(0); if (cp === 0x200C || cp === 0x200D) continue; if (scriptOfChar(cp) !== sc) return null; }
    if (STOP_IN.has(t)) return null;
    const u = aksharas(t);
    if (u.length < 2 || u.length > 8 || !u.every(goodCell)) return null;
    return { a: u.join(''), u, disp: t, enum: `(${u.length})`, words: [u.join('')], script: sc };
  }
  /* the answer (or its stem: all but the last akshara, for 3+ aksharas) must not appear in the clue */
  function leaksIndic(ans, clue) {
    const C = String(clue || '').normalize('NFC').replace(/[‌‍]/g, '');
    if (C.includes(ans.a)) return true;
    if (ans.u && ans.u.length >= 3 && C.includes(ans.u.slice(0, -1).join(''))) return true;
    return false;
  }
  /* questions that only make sense with their options, a passage or a picture, or that ask for the odd one out */
  const BAD_IN = /(इनमें से|निम्न|उपर्युक्त|विकल्प|गद्यांश|अनुच्छेद|पढ़ो|पढ़कर|चित्र|सही या गलत|नहीं है|नहीं था|नहीं होता|नहीं होती|असत्य|गलत है|ग़लत है|कौन-सा कथन|कौन सा कथन|उदाहरण दो|लिखो|अधोलिखित|अधः|बताओ कि)/;
  function clueOKIndic(ans, clue, o) {
    o = o || {};
    if (!clue || clue.length < 2 || clue.length > 150) return false;
    if (BAD_IN.test(clue) || LATIN_RE.test(clue.replace(/\b[A-Z]{1,3}\b/g, ''))) return false;
    const blanks = (clue.match(/___/g) || []).length;
    if (o.blank ? blanks !== 1 : blanks) return false;
    if ((clue.match(/\(/g) || []).length !== (clue.match(/\)/g) || []).length) return false;
    return !leaksIndic(ans, clue);
  }
  function candIndic(raw, clue, src, script, extra) {
    const ans = normAnswerIndic(raw, script); if (!ans) return null;
    const c = clue == null ? '' : sq(String(clue).normalize('NFC')).replace(/_{2,}/g, '___').replace(/\s*[:\-–—]+\s*$/, '');
    if (src !== 'sort' && !clueOKIndic(ans, c, { blank: src === 'fill' })) return null;
    if (src === 'sort' && c) return null;
    return Object.assign({ a: ans.a, u: ans.u, disp: ans.disp, enum: ans.enum, clue: c, src, pri: (PRI[src] || 1), script: ans.script }, extra || {});
  }
  function termsIndic(ch, script) {
    const out = [], push = x => { if (x) out.push(x); };
    const one = s => normAnswerIndic(s, script);
    (ch.topics || []).forEach(t => {
      const tid = t.id;
      (t.games || []).forEach(gm => {
        if (!gm) return; const ctx = sq(gm.title || '');
        if (gm.type === 'match') (gm.pairs || []).forEach(p => {
          if (!Array.isArray(p) || p.length < 2) return; const L = String(p[0]), R = String(p[1]);
          if (one(L)) push(candIndic(L, R, 'match', script, { ctx, tid }));
          if (one(R)) push(candIndic(R, L, 'match', script, { ctx, tid, pri: one(L) ? 2 : PRI.match }));   // both one word (synonyms, antonyms, singular/plural): either side can be the answer
        });
        else if (gm.type === 'fill') (gm.items || []).forEach(it => { if (it && typeof it.text === 'string') push(candIndic(it.answer, it.text, 'fill', script, { tid })); });
        else if (gm.type === 'speed') (gm.items || []).forEach(it => { if (it && typeof it.q === 'string') { push(candIndic(it.a, it.q, 'speed', script, { ctx, tid })); if (one(it.q) && /विलोम|पर्याय|समानार्थ/.test(ctx)) push(candIndic(it.q, it.a, 'speed', script, { ctx, tid, pri: 2 })); } });   // antonyms / synonyms work both ways
        else if (gm.type === 'sort') (gm.items || []).forEach(it => { if (Array.isArray(it)) push(candIndic(it[0], null, 'sort', script, { tid })); });   // word-search words only (no clue)
      });
      (t.quiz || []).forEach(q => {
        if (!q || !Array.isArray(q.options) || typeof q.q !== 'string' || !/[?？]\s*$|___/.test(q.q)) return;
        push(candIndic(q.options[q.answer], q.q, /___/.test(q.q) ? 'fill' : 'quiz', script, { tid }));
      });
      const rv = t.revise || {};
      (rv.remember || []).forEach(line => String(line || '').split(/;|।/).forEach(part => {
        const m = /^\s*([^=]+?)\s*=\s*([^=]{2,60})$/.exec(part); if (!m) return;
        const left = m[1].replace(/\s*\([^)]*\)\s*/g, ' ').trim(), right = m[2].trim();
        if (one(left) && !/[:=]/.test(right)) push(candIndic(left, right, 'def', script, { tid }));
      }));
    });
    return rank(out);
  }
  function termsCA(units, keyItems) {
    const out = [], push = x => { if (x) out.push(x); };
    const sentences = t => String(t || '').replace(/([a-z0-9)\]][.!?])\s+(?=[A-Z])/g, '$1\u0000').split('\u0000');   // no look-behind: older Safari cannot parse it
    (units || []).forEach(u => {
      if (!u) return; const uid = u.id;
      const text = JSON.stringify([u.concepts || [], (u.mcqs || []).map(q => [q.q, q.explain]), u.revision || {}]).toLowerCase();
      const known = k => text.includes(k.toLowerCase());
      /* the unit's own vocabulary: MCQ options, quick-reference keys and concept titles — a lesson sentence "X: …" or "X is …"
         is only used when X is one of these real terms (not a heading such as "Exception" or "Disadvantage") */
      const vocab = new Set(); const addV = x => { const k = String(x || '').toLowerCase().replace(/\s*\(.*$/, '').replace(/[^a-z\- ']/g, '').trim(); if (k) { vocab.add(k); vocab.add(k.replace(/s$/, '')); } };
      (u.mcqs || []).forEach(q => (q && q.options || []).forEach(addV)); (u.quickref || []).forEach(q => addV(q && q.k));
      (u.concepts || []).forEach(c => String(c && c.title || '').split(/,|;|\band\b|\bvs\.?\b|\bversus\b|[—–:]/).forEach(addV));
      const isTerm = t => { const k = String(t).toLowerCase().trim(); return k.split(/\s+/).length > 1 ? vocab.has(k) || vocab.has(k.replace(/s$/, '')) : (vocab.has(k) || vocab.has(k.replace(/s$/, ''))) && k.length >= 5; };
      (u.quickref || []).forEach(q => {
        if (!q) return; const k = String(q.k || ''), v = String(q.v || '');
        const nk = normAnswer(k);
        if (nk && !VAGUE.test(k) && !/\bvs\b|\d/i.test(k) && known(k) && !listy(v) && !/:/.test(v) && v.split(/\s+/).length >= 2) push(cand(k, v, 'quickref', { uid }));
        const d = defSplit(v); if (d) push(cand(d[0], d[1] + (/^section|^sec\.|^rule/i.test(k) ? ` (${k})` : ''), 'quickref', { uid }));
      });
      const mcq = q => { if (q && Array.isArray(q.options) && DEF_Q.test(q.q || '')) push(cand(q.options[q.answer], q.q, 'mcq', { uid, blank: /___/.test(q.q) })); };
      (u.mcqs || []).forEach(mcq);
      (u.cases || []).forEach(c => (c && c.mcqs || []).forEach(mcq));
      /* lesson sentences: "Term is a …", "Term means …" and "Term: plain definition." (the part before a dash or a semicolon) */
      const trim = d => { d = String(d).replace(/\.$/, '').split(/\s+[—–]\s+|;\s/)[0]; if (d.length > 110) { const cut = d.slice(0, 110), k = cut.lastIndexOf(','); d = k > 40 ? cut.slice(0, k) : ''; } return d && d.split(/\s+/).length >= 4 ? cap1(d) : ''; };
      (u.concepts || []).forEach(c => (c && Array.isArray(c.body) ? c.body : []).forEach(b => sentences(b).forEach(sn => {
        const d = isSplit(sn) || meansSplit(sn) || defSplit(sn.split(/\s+[—–]\s+/)[0]); if (d && isTerm(d[0])) { const cl = trim(d[1]); if (cl) push(cand(d[0], cl, 'def', { uid })); } })));
      /* a concept's own title + the opening definition of its body: "Contingent liability" ← "A contingent liability is (a) a
         possible obligation, arising out of past events, …" → "A possible obligation, arising out of past events" */
      (u.concepts || []).forEach(c => {
        if (!c || !c.title || !Array.isArray(c.body) || !c.body.length) return;
        const t = String(c.title).replace(/\s*\(.*$/, '').trim(); if (VAGUE.test(t) || /\b(vs|versus|and|or|of|in|on|for)\b/i.test(t)) return;
        const first = sentences(c.body[0])[0] || '', esc = t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const m = new RegExp('^\\s*(?:(?:a|an|the)\\s+)?' + esc + 's?\\s+(?:is|are|means|refers to|is defined as)\\s+(?:\\([a-z]\\)\\s*)?(.+)$', 'i').exec(first);
        if (!m) return;
        let d = m[1].replace(/\.$/, '').split(/\s+[—–]\s+|;\s|\s\((?:e\.g|i\.e|for example)/i)[0];
        if (d.length > 110) { const cut = d.slice(0, 110), k = cut.lastIndexOf(','); d = k > 40 ? cut.slice(0, k) : ''; }
        if (d && d.split(/\s+/).length >= 4) push(cand(t, cap1(d), 'def', { uid }));
      });
      /* revision summary lines "Term: definition. More notes." — only for real unit terms, first clause only; a word of the
         answer that the definition repeats ("Contingent asset: possible asset …") is hidden as "…" so it gives nothing away */
      ((u.revision && u.revision.summary) || []).forEach(line => {
        const m = /^\s*([A-Za-z][A-Za-z '\-]{2,40}?)\s*:\s*(.+)$/.exec(String(line || '')); if (!m || !isTerm(m[1]) || VAGUE.test(m[1])) return;
        const ans = normAnswer(m[1]); if (!ans) return;
        let d = trim(sentences(m[2])[0] || ''); if (!d) return;
        ans.words.filter(w => w.length >= 4).forEach(w => { d = d.replace(new RegExp('\\b' + w.slice(0, Math.max(4, w.length - 2)) + '[a-z]*\\b', 'gi'), '…'); });
        if ((d.match(/…/g) || []).length <= 1 && d.replace(/…/g, '').split(/\s+/).filter(Boolean).length >= 4) push(cand(m[1], cap1(d), 'def', { uid }));
      });
      /* viva key points are short marking notes in context, not stand-alone definitions — not used */
    });
    (keyItems || []).forEach(it => {
      if (!it || !it.t) return;
      const first = sentences(it.r)[0] || '';
      const t = String(it.t).replace(/\s*[—–(:].*$/, '').trim();
      const d = isSplit(first) || meansSplit(first);
      if (d && normAnswer(d[0])) push(cand(d[0], d[1], 'key', { kid: it.id }));
      else if (normAnswer(t)) {
        const m = new RegExp('^\\s*(?:(?:a|an|the)\\s+)?' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s+(?:is|are|means)\\s+(.+)$', 'i').exec(first);
        if (m) push(cand(t, cap1(m[1].replace(/\.$/, '')), 'key', { kid: it.id }));
      }
    });
    return rank(out);
  }
  /* "A 'term' means …" / "Term means …" (law and economics definitions) */
  function meansSplit(s) {
    const m = /^\s*(?:(?:a|an|the)\s+)?["'‘“]?([A-Za-z][A-Za-z\-]+(?:\s[A-Za-z][A-Za-z\-]+){0,2})["'’”]?\s+(?:means|refers to|is defined as)\s+(.{12,})$/i.exec(String(s || ''));
    if (!m || VAGUE.test(m[1])) return null;
    const right = m[2].replace(/\.$/, '');
    if (right.split(/\s+/).length < 4 || listy(right)) return null;
    return [m[1], cap1(right)];
  }
  /* one clue per answer (best source first); drop answers that hide inside another answer's clue of the same set later */
  function rank(list) {
    const by = new Map();
    list.forEach(x => { const o = by.get(x.a); if (!o || x.pri > o.pri || (x.pri === o.pri && x.clue.length < o.clue.length)) by.set(x.a, x); });
    return [...by.values()].sort((a, b) => b.pri - a.pri || (a.a < b.a ? -1 : a.a > b.a ? 1 : 0));
  }

  /* ======================================================================================
     CROSSWORD — greedy placement with many seeded attempts, scored for size, density, squareness, symmetry
     ====================================================================================== */
  function crossword(cands, seed, opts) {
    opts = opts || {};
    const MAXD0 = opts.maxDim || 13, MIN = opts.min || 8, MAX = opts.max || 15, ATT = opts.attempts || 36;
    const r = rng('xw|' + seed);
    /* every candidate as cells: letters (Latin) or aksharas (Indic); U[k] is compared as a whole string */
    const pool0 = (cands || []).filter(c => c && c.clue && (c.u ? c.u.length >= 2 && c.u.length <= 12 && c.u.every(goodCell) : /^[A-Z]{3,12}$/.test(c.a)) && unitsOf(c).length <= MAXD0)
      .map(c => Object.assign({}, c, { U: unitsOf(c) }));
    if (pool0.length < MIN) return null;
    // every answer must not contain another answer of the set (would make two answers for one entry ambiguous) — keep the longer
    /* a fixed number of attempts (never a time limit) so the same seed gives the same grid on every phone */
    const S = 2 * MAXD0 + 2, DIMS = [11, 12, 13, 10, 12, 13].map(d => Math.min(d, MAXD0));
    let best = null, bestScore = -1e9;
    for (let attempt = 0; attempt < ATT; attempt++) {
      const MAXD = Math.max(DIMS[attempt % DIMS.length], pool0.reduce((m, c) => Math.max(m, c.U.length), 0));
      /* decorate–sort–undecorate: the random numbers are drawn ONCE per word, in order (a comparator that draws random
         numbers gives different results in Chrome / Safari / Deno, whose sort algorithms call it differently) */
      const pick = shuffle(pool0, r).slice(0, Math.min(pool0.length, 26)).map((c, i) => [c, c.U.length + r() * 3, i]).sort((a, b) => b[1] - a[1] || a[2] - b[2]).map(x => x[0]);
      const L = new Array(S * S).fill(''), D = new Uint8Array(S * S), placed = [];
      let minR = S, maxR = -1, minC = S, maxC = -1;
      const put = (w, r0, c0, dir) => {
        const dr = dir === 'D' ? 1 : 0, dc = dir === 'A' ? 1 : 0;
        for (let k = 0; k < w.U.length; k++) { const y = r0 + k * dr, x = c0 + k * dc, i = y * S + x; L[i] = w.U[k]; D[i] |= dir === 'A' ? 1 : 2; minR = Math.min(minR, y); maxR = Math.max(maxR, y); minC = Math.min(minC, x); maxC = Math.max(maxC, x); }
        placed.push({ w, r: r0, c: c0, dir });
      };
      const fit = (word, r0, c0, dir) => {
        const dr = dir === 'D' ? 1 : 0, dc = dir === 'A' ? 1 : 0, bit = dir === 'A' ? 1 : 2, n = word.length;
        const er = r0 + (n - 1) * dr, ec = c0 + (n - 1) * dc;
        if (r0 < 1 || c0 < 1 || er >= S - 1 || ec >= S - 1) return -1;
        const nMinR = Math.min(minR, r0), nMaxR = Math.max(maxR, er), nMinC = Math.min(minC, c0), nMaxC = Math.max(maxC, ec);
        if (nMaxR - nMinR + 1 > MAXD || nMaxC - nMinC + 1 > MAXD) return -1;
        if (L[(r0 - dr) * S + (c0 - dc)] || L[(er + dr) * S + (ec + dc)]) return -1;
        let cross = 0;
        for (let k = 0; k < n; k++) {
          const y = r0 + k * dr, x = c0 + k * dc, i = y * S + x, ch = L[i];
          if (ch) { if (ch !== word[k] || (D[i] & bit)) return -1; cross++; }
          else if (L[(y + dc) * S + (x + dr)] || L[(y - dc) * S + (x - dr)]) return -1;
        }
        if (!cross || cross === n) return -1;
        return cross;
      };
      const first = pick[0], c0 = Math.floor(S / 2) - Math.floor(first.U.length / 2), r0 = Math.floor(S / 2);
      put(first, r0, c0, r() < .5 ? 'A' : 'D');
      const rest = pick.slice(1), used = new Set([first.a]);
      while (placed.length < MAX) {
        let bp = null, bs = -1e9;
        for (const w of rest) {
          if (used.has(w.a)) continue;
          if ([...used].some(u => u.includes(w.a) || w.a.includes(u))) continue;
          if (placed.some(q => xleakAny(w, q.w.clue) || xleakAny(q.w, w.clue))) continue;   // no clue may give away another answer
          for (const p of placed) {
            const pd = p.dir === 'A' ? [0, 1] : [1, 0], nd = p.dir === 'A' ? 'D' : 'A';
            for (let i = 0; i < p.w.U.length; i++) {
              const y = p.r + i * pd[0], x = p.c + i * pd[1], ch = p.w.U[i];
              for (let k = 0; k < w.U.length; k++) {
                if (w.U[k] !== ch) continue;
                const rr = nd === 'D' ? y - k : y, cc = nd === 'A' ? x - k : x;
                const cr = fit(w.U, rr, cc, nd); if (cr < 0) continue;
                const er = nd === 'D' ? rr + w.U.length - 1 : rr, ec = nd === 'A' ? cc + w.U.length - 1 : cc;
                const area = (Math.max(maxR, er) - Math.min(minR, rr) + 1) * (Math.max(maxC, ec) - Math.min(minC, cc) + 1);
                const sc = cr * 16 - area * 0.45 + w.U.length * 0.8 + r() * 5;
                if (sc > bs) { bs = sc; bp = [w, rr, cc, nd]; }
              }
            }
          }
        }
        if (!bp) break;
        put(bp[0], bp[1], bp[2], bp[3]); used.add(bp[0].a);
      }
      if (placed.length < MIN) continue;
      const h = maxR - minR + 1, w = maxC - minC + 1;
      let letters = 0, cross = 0, sym = 0;
      for (let y = minR; y <= maxR; y++) for (let x = minC; x <= maxC; x++) { const i = y * S + x; if (L[i]) { letters++; if (D[i] === 3) cross++; const my = maxR - (y - minR), mx = maxC - (x - minC); if (L[my * S + mx]) sym++; } }
      const score = Math.min(placed.length, 13) * 9 + cross * 6 + (letters / (w * h)) * 70 + (Math.min(w, h) / Math.max(w, h)) * 18 + (sym / letters) * 12 - Math.max(0, Math.max(w, h) - 11) * 4;
      if (score > bestScore) {
        bestScore = score;
        best = { placed: placed.map(p => ({ w: p.w, r: p.r - minR, c: p.c - minC, dir: p.dir })), w, h };
      }
    }
    if (!best) return null;
    return buildXW(best, seed);
  }
  /* the chapter's own terms first; terms from nearby chapters (marked near: true) only fill the gap */
  function xleak(ans, clue) {
    const C = ' ' + String(clue).toUpperCase().replace(/[^A-Z]+/g, ' ') + ' ';
    return ans.words.some(w => w.length >= 3 && (w.length <= 4 ? C.includes(' ' + w + ' ') : C.includes(' ' + w.slice(0, Math.max(4, w.length - 3)))));
  }
  const WO = typeof WeakMap !== 'undefined' ? new WeakMap() : null;   // cache outside the objects, so puzzles stay plain JSON
  const wordsOf = c => { let v = WO && WO.get(c); if (!v) { v = { a: c.a, words: String(c.disp || c.a).toUpperCase().split(/[ \-]+/).map(x => x.replace(/[^A-Z]/g, '')).filter(Boolean) }; if (WO) WO.set(c, v); } return v; };
  /* does this clue give away answer c? (Latin: word stems; Indic: the answer or its stem as a substring) */
  const xleakAny = (c, clue) => (c.u ? leaksIndic({ a: c.a, u: c.u }, clue) : xleak(wordsOf(c), clue));
  function chapterCrossword(own, near, seed, o) {
    o = o || {};
    own = (own || []).slice(); const have = new Set(own.map(t => t.a));
    const extra = (near || []).filter(t => !have.has(t.a) && (have.add(t.a) || true)).map(t => Object.assign({}, t, { near: true }));
    const r = rng('xwp|' + seed), ex = shuffle(extra, r);
    const MIN = o.min || 8;
    for (const k of [Math.max(0, 14 - own.length), Math.max(0, 20 - own.length), 34]) {
      const pool = own.concat(ex.slice(0, k));
      if (pool.length < MIN) continue;
      const x = crossword(pool, seed + '|' + k, { min: MIN, max: o.max || 15, attempts: o.attempts });
      if (x) return x;
    }
    return null;
  }
  /* Concept Sudoku legend: n short chapter terms (one coherent set when possible) */
  const SHAPES = ['🔴', '🟦', '🔺', '⭐', '🌙', '💎'];
  function conceptSet(groups, n, seed, strict) {
    const r = rng('cs|' + seed + '|' + n), ok = t => t && t.label && t.label.length <= 22;
    const coh = shuffle((groups || []).map(g => ({ title: g.title || '', items: (g.items || []).filter(ok) })).filter(g => g.items.length >= n), r);
    let pick = null, title = '';
    if (coh.length) { pick = shuffle(coh[0].items, r).slice(0, n); title = coh[0].title; }
    else if (strict) return null;
    else {
      const all = [], seen = new Set(); (groups || []).forEach(g => (g.items || []).filter(ok).forEach(t => { const k = t.label.toLowerCase(); if (!seen.has(k)) { seen.add(k); all.push(t); } }));
      if (all.length < n) return null; pick = shuffle(all, r).slice(0, n);
    }
    const labels = new Set(pick.map(t => t.label.toLowerCase())); if (labels.size < n) return null;
    return { title, items: pick.map((t, i) => ({ sym: SHAPES[i], label: t.label, info: t.info || '' })) };
  }
  function buildXW(b, seed) {
    const { w, h } = b, grid = Array.from({ length: h }, () => new Array(w).fill('#'));
    b.placed.forEach(p => { for (let k = 0; k < p.w.U.length; k++) grid[p.r + (p.dir === 'D' ? k : 0)][p.c + (p.dir === 'A' ? k : 0)] = p.w.U[k]; });
    const starts = {}; let n = 0;
    const isL = (y, x) => y >= 0 && x >= 0 && y < h && x < w && grid[y][x] !== '#';
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!isL(y, x)) continue;
      const a = !isL(y, x - 1) && isL(y, x + 1), d = !isL(y - 1, x) && isL(y + 1, x);
      if (a || d) starts[y * w + x] = ++n;
    }
    const indic = b.placed.some(p => p.w.u);
    const entries = b.placed.map(p => Object.assign({ n: starts[p.r * w + p.c], dir: p.dir, r: p.r, c: p.c, len: p.w.U.length, a: p.w.a, clue: p.w.clue, enum: p.w.enum, disp: p.w.disp, ctx: p.w.ctx || '', src: p.w.src, near: !!p.w.near }, p.w.u ? { u: p.w.u.slice() } : {}))
      .sort((x, y) => (x.dir === y.dir ? x.n - y.n : x.dir === 'A' ? -1 : 1));
    /* grid: rows of cells ('#' = block). Latin rows stay strings (one letter per cell); Indic rows are arrays of aksharas */
    return { type: 'crossword', seed: String(seed), script: indic ? (b.placed.find(p => p.w.script) || { w: {} }).w.script || 'deva' : 'latn', w, h, grid: indic ? grid : grid.map(r => r.join('')), entries };
  }
  function validCrossword(p) {
    if (!p || !p.entries) return 'missing';
    const { w, h, grid } = p;
    if (grid.length !== h || grid.some(r => r.length !== w)) return 'grid size';
    const indic = p.script && p.script !== 'latn';
    if (p.entries.length < (indic ? 4 : 8) || p.entries.length > 15) return 'entry count ' + p.entries.length;
    if (indic) for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (grid[y][x] !== '#' && !goodCell(grid[y][x])) return 'cell is not a whole akshara: ' + grid[y][x];
    const isL = (y, x) => y >= 0 && x >= 0 && y < h && x < w && grid[y][x] !== '#';
    const runs = new Set();
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!isL(y, x)) continue;
      if (!isL(y, x - 1) && isL(y, x + 1)) { let k = x, s = []; while (isL(y, k)) s.push(grid[y][k++]); runs.add(`A${y},${x}:${s.join('|')}`); }
      if (!isL(y - 1, x) && isL(y + 1, x)) { let k = y, s = []; while (isL(k, x)) s.push(grid[k++][x]); runs.add(`D${y},${x}:${s.join('|')}`); }
      if (!isL(y, x - 1) && !isL(y, x + 1) && !isL(y - 1, x) && !isL(y + 1, x)) return 'isolated letter';
    }
    const ents = new Set(p.entries.map(e => `${e.dir}${e.r},${e.c}:${unitsOf(e).join('|')}`));
    if (ents.size !== p.entries.length) return 'duplicate entry';
    for (const k of runs) if (!ents.has(k)) return 'unintended word ' + k;
    for (const k of ents) if (!runs.has(k)) return 'entry not on grid ' + k;
    const seenA = new Set();
    for (const e of p.entries) {
      if (indic ? !(e.u && e.u.length >= 2 && e.u.length <= 12 && e.u.join('') === e.a && e.u.every(goodCell) && aksharas(e.a).join('|') === e.u.join('|')) : !/^[A-Z]{3,12}$/.test(e.a)) return 'bad answer ' + e.a;
      if (seenA.has(e.a)) return 'repeated answer ' + e.a; seenA.add(e.a);
      const lens = e.enum.replace(/[()]/g, '').split(/[,-]/).map(Number);
      if (lens.reduce((a, b) => a + b, 0) !== unitsOf(e).length || e.len !== unitsOf(e).length) return 'enumeration ' + e.a + ' ' + e.enum;
      if (!e.clue || (indic ? leaksIndic(e, e.clue) : leaks({ a: e.a, words: (e.disp || e.a).toUpperCase().split(/[ \-]+/).map(x => x.replace(/[^A-Z]/g, '')) }, e.clue))) return 'clue leaks ' + e.a;
      for (const o of p.entries) if (o !== e && xleakAny(o, e.clue)) return `clue of ${e.a} gives away ${o.a}`;
      if (!(e.n >= 1)) return 'numbering ' + e.a;
    }
    // connected
    const cells = []; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (isL(y, x)) cells.push([y, x]);
    const seen = new Set([cells[0].join()]), st = [cells[0]];
    while (st.length) { const [y, x] = st.pop(); [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([a, b]) => { const k = (y + a) + ',' + (x + b); if (isL(y + a, x + b) && !seen.has(k)) { seen.add(k); st.push([y + a, x + b]); } }); }
    if (seen.size !== cells.length) return 'not connected';
    // numbering in reading order
    let n = 0; const want = {};
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (isL(y, x) && ((!isL(y, x - 1) && isL(y, x + 1)) || (!isL(y - 1, x) && isL(y + 1, x)))) want[y + ',' + x] = ++n;
    for (const e of p.entries) if (want[e.r + ',' + e.c] !== e.n) return 'numbering ' + e.a;
    return '';
  }

  /* ======================================================================================
     WORD SEARCH + ANAGRAM warm-ups
     ====================================================================================== */
  const DIRS8 = [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1]];
  /* words: Latin strings ('PHOTOSYNTHESIS') or arrays of aksharas (['सं','वा','द']). n×n grid, the first ndirs
     directions of DIRS8 (2 = across + down … 8 = every way incl. backwards). fill: the cells used to fill the gaps
     (Latin: common letters; Indic: the words' own aksharas). Every word appears EXACTLY once (checked). */
  function wordsearch(words, n, ndirs, seed, fill) {
    const r = rng('ws|' + seed), dirs = DIRS8.slice(0, ndirs || 2), seen = new Set();
    let list = [];
    for (const w0 of words || []) {
      const u = Array.isArray(w0) ? w0.slice() : String(w0).split(''), a = u.join('');
      if (seen.has(a) || u.length > n || (Array.isArray(w0) ? u.length < 2 || !u.every(goodCell) : !/^[A-Z]{3,}$/.test(a))) continue;
      seen.add(a); list.push({ a, u });
    }
    /* a word hidden inside another word (or inside it backwards) would be found twice: keep the longer one */
    const has = (big, small) => { for (let i = 0; i + small.length <= big.length; i++) if (small.every((c, k) => big[i + k] === c)) return true; return false; };
    list = list.filter(w => !list.some(o => o !== w && o.u.length >= w.u.length && o.a !== w.a && (has(o.u, w.u) || has(o.u, w.u.slice().reverse()))));
    list = list.sort((a, b) => b.u.length - a.u.length || (a.a < b.a ? -1 : a.a > b.a ? 1 : 0)).slice(0, 10);
    const AL = 'ABCDEFGHIJKLMNOPRSTUVWY'.split(''), pool = fill && fill.length ? fill.filter(goodCell) : list.some(w => w.a !== w.u.join('') || w.u.some(c => c.length > 1 || !/[A-Z]/.test(c))) ? [...new Set(list.flatMap(w => w.u))].sort() : AL;
    for (let attempt = 0; attempt < 80; attempt++) {
      const g = new Array(n * n).fill(''), placed = [], mine = new Uint8Array(n * n);
      for (const w of list) {
        let ok = false;
        for (let t = 0; t < 150 && !ok; t++) {
          const [dr, dc] = dirs[ri(r, dirs.length)], y0 = ri(r, n), x0 = ri(r, n), ey = y0 + dr * (w.u.length - 1), ex = x0 + dc * (w.u.length - 1);
          if (ey < 0 || ex < 0 || ey >= n || ex >= n) continue;
          let fits = true; for (let k = 0; k < w.u.length; k++) { const c = g[(y0 + dr * k) * n + x0 + dc * k]; if (c && c !== w.u[k]) { fits = false; break; } }
          if (!fits) continue;
          for (let k = 0; k < w.u.length; k++) { const i = (y0 + dr * k) * n + x0 + dc * k; g[i] = w.u[k]; mine[i] = 1; }
          placed.push({ a: w.a, u: w.u, r: y0, c: x0, dr, dc }); ok = true;
        }
      }
      if (placed.length < Math.min(list.length, 6)) continue;
      for (let i = 0; i < g.length; i++) if (!g[i]) g[i] = pool[ri(r, pool.length)];
      /* repair: a filler cell that spells a word a second time is re-rolled */
      let good = false;
      for (let fix = 0; fix < 200; fix++) {
        const extra = wsExtra(g, n, placed);
        if (!extra) { good = true; break; }
        const free = extra.filter(i => !mine[i]); if (!free.length) break;
        const i = free[ri(r, free.length)]; g[i] = pool[ri(r, pool.length)];
      }
      if (!good) continue;
      const res = { type: 'wordsearch', n, seed: String(seed), script: list.some(w => w.u.some(c => c.length > 1 || !/^[A-Z]$/.test(c))) ? 'indic' : 'latn', grid: range(n).map(y => g.slice(y * n, y * n + n)), words: placed };
      if (!validWordsearch(res)) return res;
    }
    return null;
  }
  /* every place a run of cells spells w.u (any of the 8 directions) */
  function wsFind(g, n, u) {
    const at = (y, x) => (Array.isArray(g[0]) ? g[y][x] : g[y * n + x]), out = [];
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) for (const [dr, dc] of DIRS8) {
      let k = 0; const cells = [];
      while (k < u.length) { const yy = y + dr * k, xx = x + dc * k; if (yy < 0 || xx < 0 || yy >= n || xx >= n || at(yy, xx) !== u[k]) break; cells.push(yy * n + xx); k++; }
      if (k === u.length) out.push(cells);
    }
    return out;
  }
  /* the cells of the first occurrence that is not the placed word (null = every word appears once) */
  function wsExtra(g, n, placed) {
    for (const w of placed) {
      const mineCells = Array.from({ length: w.u.length }, (_, k) => (w.r + w.dr * k) * n + w.c + w.dc * k), key = mineCells.join(), rkey = mineCells.slice().reverse().join();
      for (const occ of wsFind(g, n, w.u)) { const k = occ.join(); if (k !== key && !(k === rkey && w.u.join('|') === w.u.slice().reverse().join('|'))) return occ; }
    }
    return null;
  }
  function wsCount(p, w) {
    const u = Array.isArray(w) ? w : (p.words.find(x => x.a === w) || {}).u || String(w).split('');
    const c = wsFind(p.grid, p.n, u).length;
    return u.join('|') === u.slice().reverse().join('|') ? c / 2 : c;
  }
  function validWordsearch(p) {
    for (const w of p.words) {
      const u = w.u || w.a.split(''); if (u.join('') !== w.a) return `${w.a} cells differ`;
      if (!u.every(goodCell)) return `${w.a} has a broken cell`;
      for (let k = 0; k < u.length; k++) { const y = w.r + w.dr * k, x = w.c + w.dc * k; if (p.grid[y][x] !== u[k]) return `${w.a} not at its place`; }
      const c = wsCount(p, u); if (c !== 1) return `${w.a} found ${c} times`;
    }
    for (const row of p.grid) for (const c of row) if (!goodCell(c)) return 'broken cell ' + c;
    return '';
  }
  function scramble(word, seed) {
    const r = rng('an|' + seed + '|' + word);
    if (new Set(word).size < 2) return word;
    for (let t = 0; t < 20; t++) { const s = shuffle(word.split(''), r).join(''); if (s !== word) return s; }
    return word.split('').reverse().join('');
  }
  /* anagram tiles: the answer's cells (letters or aksharas) in a new order (never the answer itself) */
  function scrambleU(u, seed) {
    const r = rng('an|' + seed + '|' + u.join('')), key = u.join('|');
    if (new Set(u).size < 2) return u.slice();
    for (let t = 0; t < 30; t++) { const s = shuffle(u, r); if (s.join('|') !== key) return s; }
    return u.slice().reverse();
  }

  /* ======================================================================================
     CHAPTER PUZZLES from a spec — pure and deterministic: the same spec + the same chapter content gives the same
     puzzle on every device (the UI, the Web Worker, the race mode and the Node tests all call this).
       spec: { t: 'xw'|'ws'|'an'|'csdk'|'sdk'|'kak', seed, diff, n? }   t = { own, near, groups } from termsFor…()
     Only the chapter's own terms are used, except Latin crosswords, which may borrow a few terms from the
     neighbouring chapters of the same subject (marked ↗) when the chapter alone is too small.
     ====================================================================================== */
  const isIndicT = t => !!(t && t.own && t.own.some(x => x.u));
  const XW_MAX = { easy: 10, medium: 12, hard: 15, expert: 15 };
  const WS_DIFF = { latn: { easy: [8, 2, 6], medium: [10, 4, 8], hard: [12, 8, 10] }, indic: { easy: [6, 2, 5], medium: [7, 3, 6], hard: [8, 3, 8] } };   // [grid n, directions, words]
  const AN_DIFF = { latn: { easy: [4, 3, 7], medium: [5, 4, 9], hard: [6, 5, 12] }, indic: { easy: [4, 2, 3], medium: [5, 3, 4], hard: [6, 3, 6] } };   // [words, min, max length]
  const D3 = d => (d === 'medium' || d === 'hard' ? d : d === 'expert' ? 'hard' : 'easy');
  const clued = t => (t.own || []).filter(x => x.clue);
  const XW_MIN_OWN = { latn: 5, indic: 6 };
  /* which chapter puzzles this chapter can make, and why not */
  function chapterKinds(t) {
    const ind = isIndicT(t), sc = ind ? 'indic' : 'latn', own = clued(t || { own: [] });
    const wsW = (t && t.own || []).filter(x => unitsOf(x).length >= (ind ? 2 : 3) && unitsOf(x).length <= WS_DIFF[sc].hard[0]);
    const anW = own.filter(x => unitsOf(x).length >= (ind ? 2 : 3) && unitsOf(x).length <= 12 && new Set(unitsOf(x)).size >= 2);
    return {
      /* CA chapters have few stand-alone definitions: their crossword may be filled with the same paper's words (shown ↗) */
      xw: { ok: (own.length >= XW_MIN_OWN[sc] || (!ind && own.length >= (t && t.ca ? 0 : 3) && own.length + (t.near || []).filter(x => x.clue).length >= 12)) && (ind || own.length + (t.near || []).filter(x => x.clue).length >= 8), n: own.length },
      ws: { ok: wsW.length >= 4, n: wsW.length },
      an: { ok: anW.length >= 3, n: anW.length },
      csdk: { ok: !!(conceptSet(t && t.groups, 4, 'x', true) || conceptSet(t && t.groups, 4, 'x')), n: 0 } };
  }
  function puzzleFor(spec, t) {
    spec = spec || {}; t = t || { own: [], near: [], groups: [] };
    const seed = String(spec.seed || 'x'), diff = D3(spec.diff), ind = isIndicT(t), sc = ind ? 'indic' : 'latn', kinds = chapterKinds(t);
    if (spec.t === 'sdk') return { p: sudoku(spec.n || 9, spec.diff || 'easy', seed) };
    if (spec.t === 'kak') return { p: kakuro(0, spec.diff || 'easy', seed) };
    if (spec.t === 'xw') {
      if (!kinds.xw.ok) return null;
      const own = clued(t), near = ind ? [] : (t.near || []).filter(x => x.clue);
      const p = chapterCrossword(own, near, seed, { min: ind ? 4 : 8, max: XW_MAX[diff] });
      if (!p) return null;
      if (diff === 'easy') p.giv = [...new Set(p.entries.map(e => e.r * p.w + e.c))].sort((a, b) => a - b);   // easy: first letter of every word is given
      p.diff = diff; return { p };
    }
    if (spec.t === 'ws') {
      if (!kinds.ws.ok) return null;
      const [n, dirs, cnt] = WS_DIFF[sc][diff];
      const pool = (t.own || []).filter(x => unitsOf(x).length >= (ind ? 2 : 3) && unitsOf(x).length <= n);
      const words = shuffle(pool, rng('wsw|' + seed)).slice(0, cnt);
      if (words.length < 4) return null;
      const fill = ind ? [...new Set((t.own || []).flatMap(unitsOf))].sort() : null;
      const p = wordsearch(words.map(w => (ind ? unitsOf(w) : w.a)), n, dirs, seed, fill);
      if (!p) return null;
      p.diff = diff; p.clues = {}; words.forEach(w => { p.clues[w.a] = { clue: w.clue || '', ctx: w.ctx || '', enum: w.enum }; });
      return { p };
    }
    if (spec.t === 'an') {
      if (!kinds.an.ok) return null;
      const [cnt, lo, hi] = AN_DIFF[sc][diff], all = clued(t).filter(x => new Set(unitsOf(x)).size >= 2 && unitsOf(x).length >= (ind ? 2 : 3) && unitsOf(x).length <= 12);
      const r = rng('anw|' + seed), fit = shuffle(all.filter(x => unitsOf(x).length >= lo && unitsOf(x).length <= hi), r);
      const rest = shuffle(all.filter(x => !fit.includes(x)), r).map((x, i) => [x, Math.abs(unitsOf(x).length - lo), i]).sort((a, b) => a[1] - b[1] || a[2] - b[2]).map(x => x[0]);   // total order: same on every engine
      const words = [];
      for (const w of fit.concat(rest)) { if (words.length >= cnt) break; if (!words.some(o => xleakAny(o, w.clue) || xleakAny(w, o.clue))) words.push(w); }   // no clue may give away another word of the set
      if (words.length < 3) return null;
      return { p: { type: 'anagram', diff, seed, script: ind ? 'indic' : 'latn', words: words.map(w => { const u = unitsOf(w); return { a: w.a, u: u.slice(), clue: w.clue, enum: w.enum, ctx: w.ctx || '', t: scrambleU(u, seed) }; }) } };
    }
    if (spec.t === 'csdk') {
      let n = spec.n === 6 ? 6 : 4, set = null;
      for (const m of n === 6 ? [6, 4] : [4]) { set = conceptSet(t.groups, m, seed, true) || conceptSet(t.groups, m, seed); if (set) { n = m; break; } }
      if (!set) return null;
      const p = sudoku(n, diff, seed); return { p, extra: { set } };
    }
    return null;
  }
  /* concept-sudoku groups: one per match game (school) — labels in the chapter's script */
  function groupsSchool(ch) {
    const scr = chapterScript(ch), ind = scr && scr !== 'latn', out = [];
    (ch.topics || []).forEach(t => (t.games || []).forEach(gm => {
      if (!gm || gm.type !== 'match') return;
      const items = (gm.pairs || []).filter(p => Array.isArray(p) && p.length >= 2).map(p => {
        const L = String(p[0]).trim();
        if (ind) { const a = normAnswerIndic(L, scr); return a ? { label: a.disp, info: String(p[1]) } : null; }
        return /^[A-Za-z][A-Za-z '\-]*$/.test(L) ? { label: L, info: String(p[1]) } : null;
      });
      const ok = items.filter(Boolean); if (ok.length) out.push({ title: gm.title || t.title, items: ok });
    }));
    return out;
  }

  /* ======================================================================================
     TERMS FROM RAW CONTENT (pure) — the app (js/puzzles.js) and a server (Edge Function) build the same terms.
       school: content = the subject file content/g{g}/{sid}.json (parsed)          → termsFromSchool(subject, ci)
       CA:     content = { structure, units: { uid: unit json }, banks?: { uid: bank json }, keyItems? }
               (keyItems = CaKeysData.ITEMS from js/ca-keys-data.js; read from globalThis.CaKeysData when missing)
     ====================================================================================== */
  function termsFromSchool(subject, ci) {
    const chs = (subject && subject.chapters) || [], c = chs[ci];
    if (!c) return { own: [], near: [], groups: [] };
    const own = termsSchool(c), groups = groupsSchool(c), near = [];
    if ((chapterScript(c) || 'latn') === 'latn' && own.length < 20) {
      const order = []; for (let j = 1; j < chs.length && order.length < 6; j++) [ci - j, ci + j].forEach(x => { if (x >= 0 && x < chs.length && order.length < 6) order.push(x); });
      order.forEach(x => near.push(...termsSchool(chs[x]).filter(t => !t.u)));
    }
    return { own, near, groups };
  }
  /* the unit as the app reads it: its file plus the extra MCQ bank (js/ca.js mergeBank) */
  function caUnitMerged(d, bank, uid) {
    if (!d) return null;
    const extra = bank && bank.unit === uid && Array.isArray(bank.mcq) ? bank.mcq : [];
    if (!extra.length) return d;
    const have = new Set((d.mcqs || []).map(q => q.id));
    return Object.assign({}, d, { mcqs: (d.mcqs || []).concat(extra.filter(q => !have.has(q.id)).map(q => Object.assign({}, q, { bank: true }))) });
  }
  function caFind(structure, ch) {
    for (const p of (structure && structure.papers) || []) { const i = p.chapters.findIndex(c => c.id === ch); if (i >= 0) return { p, c: p.chapters[i], i }; }
    return null;
  }
  const caNearOrder = (f) => { const chs = f.p.chapters, order = []; for (let j = 1; j < chs.length && order.length < 20; j++) [f.i - j, f.i + j].forEach(x => { if (x >= 0 && x < chs.length && order.length < 20) order.push(x); }); return order; };
  function termsFromCA(content, ch) {
    content = content || {};
    const f = caFind(content.structure, ch); if (!f) return { own: [], near: [], groups: [] };
    const G = typeof globalThis !== 'undefined' ? globalThis : {};
    const items = content.keyItems || (G.CaKeysData && G.CaKeysData.ITEMS) || [];
    const cUnits = c => c.units.filter(u => u.status === 'built').map(u => { const d = content.units && content.units[u.id]; return d ? caUnitMerged(d, content.banks && content.banks[u.id], u.id) : null; }).filter(Boolean);
    const keys = c => items.filter(it => c.units.some(u => u.id === it.u));
    const units = cUnits(f.c), own = termsCA(units, keys(f.c)), groups = [], near = [];
    units.forEach(u => groups.push({ title: u.title, items: (u.quickref || []).filter(q => /^[A-Za-z][A-Za-z '\-]*$/.test(String(q.k || '').trim())).map(q => ({ label: String(q.k).trim(), info: String(q.v || '') })) }));
    if (own.length < 20) for (const x of caNearOrder(f)) near.push(...termsCA(cUnits(f.p.chapters[x]), keys(f.p.chapters[x])));   // nearest chapters first
    return { own, near, groups, ca: true };
  }
  const caLevel = ch => ({ fnd: 'foundation', int: 'inter', fin: 'final' })[String(ch).split('-')[0]] || 'foundation';
  /* the content files a spec needs (relative to the app root). CA: call once without the structure, then again with
     it to get the unit + bank files (bank files are optional: a missing one means "no extra MCQs"). */
  function contentPathOf(spec, structure) {
    const t = spec && spec.t === 'ana' ? 'an' : spec && spec.t, sc = (spec && spec.sc) || { k: 'q' };
    if (t === 'sdk' || t === 'kak' || sc.k === 'q') return [];
    if (sc.k === 's') return [`content/g${+sc.g}/${sc.sid}.json`];
    const lvl = caLevel(sc.ch), out = [`content/ca/${lvl}/structure.json`, 'js/ca-keys-data.js'];
    const f = structure && caFind(structure, sc.ch); if (!f) return out;
    [f.i].concat(caNearOrder(f)).forEach(x => f.p.chapters[x].units.filter(u => u.status === 'built').forEach(u => {
      out.push(u.file); const m = /^[a-z]+-(p\d+)-/.exec(u.id); if (m) out.push(`content/ca/${lvl}/${m[1]}/bank/${u.id}.json`);
    }));
    return out;
  }
  function termsFor(spec, content) {
    const sc = (spec && spec.sc) || { k: 'q' };
    if (sc.k === 's') return termsFromSchool(content && content.chapters ? content : content && content.subject, +sc.ci);
    if (sc.k === 'c') return termsFromCA(content, sc.ch);
    return null;
  }
  /* the canonical answer of a built puzzle — the same form Puzzles.race() reports in onSolved({ answer }):
       sdk / csdk: every cell's digit (concept sudoku: the symbol's number 1–n), row by row, one string
       kak: row by row, '.' for clue/blocked cells, digits for white cells        xw: the answers in entry order
       ws: the words, sorted (plain code-unit order)                              an: the answers in puzzle order */
  function answerOf(kind, p) {
    const t = kind === 'ana' ? 'an' : kind;
    if (!p) return null;
    if (t === 'sdk' || t === 'csdk') return p.solution.join('');
    if (t === 'kak') return p.cells.map((c, i) => (c ? String(p.solution[i]) : '.')).join('');
    if (t === 'xw') return p.entries.map(e => e.a);
    if (t === 'ws') return p.words.map(w => w.a).sort();
    if (t === 'an') return p.words.map(w => w.a);
    return null;
  }
  /* server-side answer key: the exact puzzle `spec` builds (content = what contentPathOf(spec) lists, parsed; null
     for number puzzles) → its canonical answer, or null when the spec cannot make a puzzle */
  function solutionOf(spec, content) {
    if (!spec) return null;
    const sp = Object.assign({}, spec, { t: spec.t === 'ana' ? 'an' : spec.t, seed: String(spec.seed || 'x'), diff: spec.diff || 'easy' });
    const t = sp.t === 'sdk' || sp.t === 'kak' ? null : termsFor(sp, content);
    const r = puzzleFor(sp, t);
    return r && r.p ? answerOf(sp.t, r.p) : null;
  }

  const API = { hash, rng, shuffle, sudoku, sdkCount, sdkLogic, validSudoku, BOX, kakuro, kakCount, kakRuns, validKakuro, COMBOS,
    scriptOf, langOf, aksharas, goodCell, clip, unitsOf, normAnswerIndic, leaksIndic, termsIndic, chapterScript,
    normAnswer, leaks, cleanClue, clueOK, termsSchool, termsCA, rank, crossword, chapterCrossword, conceptSet, SHAPES, validCrossword, wordsearch, validWordsearch, wsCount, scramble, scrambleU, defSplit, isSplit, puzzleFor, chapterKinds, groupsSchool, XW_MAX, WS_DIFF, AN_DIFF,
    termsFromSchool, termsFromCA, caUnitMerged, termsFor, contentPathOf, answerOf, solutionOf };
  root.PuzzleCore = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : (typeof self !== 'undefined' ? self : globalThis));
