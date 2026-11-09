/* ================= StudyVerse Puzzles — engine (js/puzzles-core.js) =================
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
  function clueOK(ans, clue, o) {
    o = o || {};
    if (!clue || clue.length < 6 || clue.length > 150) return false;
    if (!/[a-z]/i.test(clue) || /[ऀ-ॿ]/.test(clue)) return false;
    if (BAD_CLUE.test(clue) || BAD_CAPS.test(clue)) return false;
    const blanks = (clue.match(/___/g) || []).length;
    if (blanks > (o.blank ? 1 : 0)) return false;
    if (o.blank && blanks !== 1) return false;
    if (leaks(ans, clue)) return false;
    if (clue.split(/\s+/).length < 2) return false;
    if (/^(which|choose|pick|select|identify|tick|circle|underline|fill|complete|rewrite|correct)\b/i.test(clue)) return false;
    if ((clue.match(/\(/g) || []).length !== (clue.match(/\)/g) || []).length) return false;
    return true;
  }
  const PRI = { def: 6, match: 5, quickref: 5, key: 5, fill: 4, speed: 3, mcq: 3, quiz: 3, point: 2 };
  function cand(raw, clue, src, extra) {
    const ans = normAnswer(raw); if (!ans) return null;
    const c = cleanClue(clue);
    if (!clueOK(ans, c, { blank: src === 'fill' || (extra && extra.blank) })) return null;
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
  function termsSchool(ch) {
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
  function termsCA(units, keyItems) {
    const out = [], push = x => { if (x) out.push(x); };
    const sentences = t => String(t || '').split(/(?<=[a-z0-9)\]][.!?])\s+(?=[A-Z])/);
    (units || []).forEach(u => {
      if (!u) return; const uid = u.id;
      const text = JSON.stringify([u.concepts || [], (u.mcqs || []).map(q => [q.q, q.explain]), u.revision || {}]).toLowerCase();
      const known = k => text.includes(k.toLowerCase());
      (u.quickref || []).forEach(q => {
        if (!q) return; const k = String(q.k || ''), v = String(q.v || '');
        const nk = normAnswer(k);
        if (nk && !VAGUE.test(k) && !/\bvs\b|\d/i.test(k) && known(k) && !listy(v) && !/:/.test(v) && v.split(/\s+/).length >= 2) push(cand(k, v, 'quickref', { uid }));
        const d = defSplit(v); if (d) push(cand(d[0], d[1] + (/^section|^sec\.|^rule/i.test(k) ? ` (${k})` : ''), 'quickref', { uid }));
      });
      const mcq = q => { if (q && Array.isArray(q.options) && DEF_Q.test(q.q || '')) push(cand(q.options[q.answer], q.q, 'mcq', { uid, blank: /___/.test(q.q) })); };
      (u.mcqs || []).forEach(mcq);
      (u.cases || []).forEach(c => (c && c.mcqs || []).forEach(mcq));
      (u.concepts || []).forEach(c => (c && Array.isArray(c.body) ? c.body : []).forEach(b => sentences(b).forEach(sn => { const d = isSplit(sn) || meansSplit(sn); if (d) push(cand(d[0], d[1], 'def', { uid })); })));
      /* revision lines are condensed notes ("Recession: increase G") — not reliable definitions, so they are not used */
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
        if (it.f && String(it.f).length <= 90) push(cand(t, 'Formula: ' + it.f, 'key', { kid: it.id }));
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
    return [...by.values()].sort((a, b) => b.pri - a.pri || a.a.localeCompare(b.a));
  }

  /* ======================================================================================
     CROSSWORD — greedy placement with many seeded attempts, scored for size, density, squareness, symmetry
     ====================================================================================== */
  function crossword(cands, seed, opts) {
    opts = opts || {};
    const MAXD0 = opts.maxDim || 13, MIN = opts.min || 8, MAX = opts.max || 15, ATT = opts.attempts || 36;
    const r = rng('xw|' + seed);
    const pool0 = (cands || []).filter(c => /^[A-Z]{3,12}$/.test(c.a) && c.a.length <= MAXD0);
    if (pool0.length < MIN) return null;
    // every answer must not contain another answer of the set (would make two answers for one entry ambiguous) — keep the longer
    /* a fixed number of attempts (never a time limit) so the same seed gives the same grid on every phone */
    const S = 2 * MAXD0 + 2, DIMS = [11, 12, 13, 10, 12, 13].map(d => Math.min(d, MAXD0));
    let best = null, bestScore = -1e9;
    for (let attempt = 0; attempt < ATT; attempt++) {
      const MAXD = Math.max(DIMS[attempt % DIMS.length], pool0.reduce((m, c) => Math.max(m, c.a.length), 0));
      const pick = shuffle(pool0, r).slice(0, Math.min(pool0.length, 26)).sort((a, b) => (b.a.length + r() * 3) - (a.a.length + r() * 3));
      const L = new Array(S * S).fill(''), D = new Uint8Array(S * S), placed = [];
      let minR = S, maxR = -1, minC = S, maxC = -1;
      const put = (w, r0, c0, dir) => {
        const dr = dir === 'D' ? 1 : 0, dc = dir === 'A' ? 1 : 0;
        for (let k = 0; k < w.a.length; k++) { const y = r0 + k * dr, x = c0 + k * dc, i = y * S + x; L[i] = w.a[k]; D[i] |= dir === 'A' ? 1 : 2; minR = Math.min(minR, y); maxR = Math.max(maxR, y); minC = Math.min(minC, x); maxC = Math.max(maxC, x); }
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
      const first = pick[0], c0 = Math.floor(S / 2) - Math.floor(first.a.length / 2), r0 = Math.floor(S / 2);
      put(first, r0, c0, r() < .5 ? 'A' : 'D');
      const rest = pick.slice(1), used = new Set([first.a]);
      while (placed.length < MAX) {
        let bp = null, bs = -1e9;
        for (const w of rest) {
          if (used.has(w.a)) continue;
          if ([...used].some(u => u.includes(w.a) || w.a.includes(u))) continue;
          if (placed.some(q => xleak(wordsOf(w), q.w.clue) || xleak(wordsOf(q.w), w.clue))) continue;   // no clue may give away another answer
          for (const p of placed) {
            const pd = p.dir === 'A' ? [0, 1] : [1, 0], nd = p.dir === 'A' ? 'D' : 'A';
            for (let i = 0; i < p.w.a.length; i++) {
              const y = p.r + i * pd[0], x = p.c + i * pd[1], ch = p.w.a[i];
              for (let k = 0; k < w.a.length; k++) {
                if (w.a[k] !== ch) continue;
                const rr = nd === 'D' ? y - k : y, cc = nd === 'A' ? x - k : x;
                const cr = fit(w.a, rr, cc, nd); if (cr < 0) continue;
                const er = nd === 'D' ? rr + w.a.length - 1 : rr, ec = nd === 'A' ? cc + w.a.length - 1 : cc;
                const area = (Math.max(maxR, er) - Math.min(minR, rr) + 1) * (Math.max(maxC, ec) - Math.min(minC, cc) + 1);
                const sc = cr * 16 - area * 0.45 + w.a.length * 0.8 + r() * 5;
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
  const wordsOf = c => c._w || (c._w = { a: c.a, words: String(c.disp || c.a).toUpperCase().split(/[ \-]+/).map(x => x.replace(/[^A-Z]/g, '')).filter(Boolean) });
  function chapterCrossword(own, near, seed) {
    own = (own || []).slice(); const have = new Set(own.map(t => t.a));
    const extra = (near || []).filter(t => !have.has(t.a) && (have.add(t.a) || true)).map(t => Object.assign({}, t, { near: true }));
    const r = rng('xwp|' + seed), ex = shuffle(extra, r);
    for (const k of [Math.max(0, 14 - own.length), Math.max(0, 20 - own.length), 34]) {
      const pool = own.concat(ex.slice(0, k));
      if (pool.length < 8) continue;
      const x = crossword(pool, seed + '|' + k);
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
    b.placed.forEach(p => { for (let k = 0; k < p.w.a.length; k++) grid[p.r + (p.dir === 'D' ? k : 0)][p.c + (p.dir === 'A' ? k : 0)] = p.w.a[k]; });
    const starts = {}; let n = 0;
    const isL = (y, x) => y >= 0 && x >= 0 && y < h && x < w && grid[y][x] !== '#';
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!isL(y, x)) continue;
      const a = !isL(y, x - 1) && isL(y, x + 1), d = !isL(y - 1, x) && isL(y + 1, x);
      if (a || d) starts[y * w + x] = ++n;
    }
    const entries = b.placed.map(p => ({ n: starts[p.r * w + p.c], dir: p.dir, r: p.r, c: p.c, len: p.w.a.length, a: p.w.a, clue: p.w.clue, enum: p.w.enum, disp: p.w.disp, ctx: p.w.ctx || '', src: p.w.src, near: !!p.w.near }))
      .sort((x, y) => (x.dir === y.dir ? x.n - y.n : x.dir === 'A' ? -1 : 1));
    return { type: 'crossword', seed: String(seed), w, h, grid: grid.map(r => r.join('')), entries };
  }
  function validCrossword(p) {
    if (!p || !p.entries) return 'missing';
    const { w, h, grid } = p;
    if (grid.length !== h || grid.some(r => r.length !== w)) return 'grid size';
    if (p.entries.length < 8 || p.entries.length > 15) return 'entry count ' + p.entries.length;
    const isL = (y, x) => y >= 0 && x >= 0 && y < h && x < w && grid[y][x] !== '#';
    const runs = new Set();
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!isL(y, x)) continue;
      if (!isL(y, x - 1) && isL(y, x + 1)) { let k = x, s = ''; while (isL(y, k)) s += grid[y][k++]; runs.add(`A${y},${x}:${s}`); }
      if (!isL(y - 1, x) && isL(y + 1, x)) { let k = y, s = ''; while (isL(k, x)) s += grid[k++][x]; runs.add(`D${y},${x}:${s}`); }
      if (!isL(y, x - 1) && !isL(y, x + 1) && !isL(y - 1, x) && !isL(y + 1, x)) return 'isolated letter';
    }
    const ents = new Set(p.entries.map(e => `${e.dir}${e.r},${e.c}:${e.a}`));
    if (ents.size !== p.entries.length) return 'duplicate entry';
    for (const k of runs) if (!ents.has(k)) return 'unintended word ' + k;
    for (const k of ents) if (!runs.has(k)) return 'entry not on grid ' + k;
    const seenA = new Set();
    for (const e of p.entries) {
      if (!/^[A-Z]{3,12}$/.test(e.a)) return 'bad answer ' + e.a;
      if (seenA.has(e.a)) return 'repeated answer ' + e.a; seenA.add(e.a);
      const lens = e.enum.replace(/[()]/g, '').split(/[,-]/).map(Number);
      if (lens.reduce((a, b) => a + b, 0) !== e.a.length) return 'enumeration ' + e.a + ' ' + e.enum;
      if (!e.clue || leaks({ a: e.a, words: (e.disp || e.a).toUpperCase().split(/[ \-]+/).map(x => x.replace(/[^A-Z]/g, '')) }, e.clue)) return 'clue leaks ' + e.a;
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
  function wordsearch(words, n, ndirs, seed) {
    const r = rng('ws|' + seed), dirs = DIRS8.slice(0, ndirs || 2);
    const list = [...new Set(words.filter(w => /^[A-Z]{3,}$/.test(w) && w.length <= n))].sort((a, b) => b.length - a.length).slice(0, 10);
    for (let attempt = 0; attempt < 60; attempt++) {
      const g = new Array(n * n).fill(''), placed = [];
      for (const w of list) {
        let ok = false;
        for (let t = 0; t < 150 && !ok; t++) {
          const [dr, dc] = dirs[ri(r, dirs.length)], y0 = ri(r, n), x0 = ri(r, n), ey = y0 + dr * (w.length - 1), ex = x0 + dc * (w.length - 1);
          if (ey < 0 || ex < 0 || ey >= n || ex >= n) continue;
          let fits = true; for (let k = 0; k < w.length; k++) { const c = g[(y0 + dr * k) * n + x0 + dc * k]; if (c && c !== w[k]) { fits = false; break; } }
          if (!fits) continue;
          for (let k = 0; k < w.length; k++) g[(y0 + dr * k) * n + x0 + dc * k] = w[k];
          placed.push({ a: w, r: y0, c: x0, dr, dc }); ok = true;
        }
      }
      if (placed.length < Math.min(list.length, 6)) continue;
      const AL = 'ABCDEFGHIJKLMNOPRSTUVWY';
      for (let i = 0; i < g.length; i++) if (!g[i]) g[i] = AL[ri(r, AL.length)];
      const res = { type: 'wordsearch', n, seed: String(seed), grid: range(n).map(y => g.slice(y * n, y * n + n).join('')), words: placed };
      if (!validWordsearch(res)) return res;
    }
    return null;
  }
  function wsCount(p, w) {
    const n = p.n, G = p.grid; let c = 0;
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) for (const [dr, dc] of DIRS8) {
      let k = 0; while (k < w.length) { const yy = y + dr * k, xx = x + dc * k; if (yy < 0 || xx < 0 || yy >= n || xx >= n || G[yy][xx] !== w[k]) break; k++; }
      if (k === w.length) c++;
    }
    return w.split('').reverse().join('') === w ? c / 2 : c;
  }
  function validWordsearch(p) {
    for (const w of p.words) { const c = wsCount(p, w.a); if (c !== 1) return `${w.a} found ${c} times`; }
    return '';
  }
  function scramble(word, seed) {
    const r = rng('an|' + seed + '|' + word);
    if (new Set(word).size < 2) return word;
    for (let t = 0; t < 20; t++) { const s = shuffle(word.split(''), r).join(''); if (s !== word) return s; }
    return word.split('').reverse().join('');
  }

  const API = { hash, rng, shuffle, sudoku, sdkCount, sdkLogic, validSudoku, BOX, kakuro, kakCount, kakRuns, validKakuro, COMBOS,
    normAnswer, leaks, cleanClue, clueOK, termsSchool, termsCA, rank, crossword, chapterCrossword, conceptSet, SHAPES, validCrossword, wordsearch, validWordsearch, scramble, defSplit, isSplit };
  root.PuzzleCore = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : (typeof self !== 'undefined' ? self : globalThis));
