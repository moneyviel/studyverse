/* ================= Brain games: puzzle makers (js/mindplay-gen.js) =================
   Every puzzle is created fresh by these functions (nothing is stored or copied), and each maker
   checks its own puzzle before returning it:
     memory  – symbols with secret numbers to remember            (answer = the code itself)
     twins   – find the missing digit / the letter that appears twice (checked by counting)
     scale   – balance scales with hidden weights                   (brute force: every weight set that fits the clues gives the same answer)
     pyramid – number pyramid, each brick = sum of the two below     (filled only by forced steps, so the answer is unique)
     wheel   – number wheel with one missing segment                 (every rule in a library that fits must agree)
     cube    – which cube can this net fold into?                    (net is folded by rolling a cube; all 24 turns checked)
     jumble  – unscramble the word, with a picture/category clue     (no other word in the same list uses the same letters)
     magic   – magic square with blanks                              (brute force: exactly one way to finish)
   Levels 1–5 make each game harder. Bands: j = Grades 1–3, m = 4–8, s = 9–12 and CA.
   Works in the browser (window.MindPlayGen) and in Node for the self-tests (tools/mind/test_play.js). */
(function (root) {
  'use strict';
  const ri = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (a, n) => shuffle(a).slice(0, n);
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

  /* ---------- memory code ---------- */
  const MEM_J = ['🐶', '🐱', '🐸', '🐵', '🦁', '🐼', '🐷', '🐔', '🐙', '🦋', '🐢', '🐘'];
  const MEM_M = ['🍎', '🚀', '⚽', '🎸', '🌵', '🔑', '🎈', '🧲', '🍩', '🪁', '🌙', '🔔'];
  const MEM_S = ['★', '◆', '▲', '●', '■', '✚', '♣', '♠', '☾', '⚑', '✿', '⬢', '♥', '✦'];
  function memory(b, lvl) {
    const n = { j: [3, 4, 4, 5, 5], m: [5, 6, 6, 7, 8], s: [6, 7, 8, 9, 10] }[b][lvl - 1];
    const syms = sample(b === 'j' ? MEM_J : b === 'm' ? MEM_M : MEM_S, n);
    const nums = sample(Array.from({ length: n }, (_, i) => i + 1), n);
    const pairs = syms.map((s, i) => ({ s, n: nums[i] }));
    return { g: 'memory', pairs, ask: shuffle(pairs), study: { j: 14, m: 16, s: 18 }[b] + n, check: ans => pairs.every(p => ans[p.s] === p.n) };
  }

  /* ---------- perception: missing digit / twin letter ---------- */
  const LET = 'ABCDEFGHIJKLMNOPRSTUVWY'.split('');
  function twins(b, lvl) {
    if (Math.random() < .5 || b === 'j') {
      const top = b === 'j' ? (lvl < 3 ? 5 : 9) : 9;                                   // digits 1–top (j small) or 0–9
      const lo = b === 'j' ? 1 : 0, all = Array.from({ length: top - lo + 1 }, (_, i) => i + lo);
      const miss = pick(all), shown = shuffle(all.filter(x => x !== miss));
      if (shown.includes(miss) || shown.length !== all.length - 1) throw new Error('twins digit');
      return { g: 'twins', mode: 'digit', shown, keys: all, answer: miss, time: { j: 20, m: 12, s: 9 }[b] + (5 - lvl), q: `Which number from ${lo} to ${top} is missing?` };
    }
    const n = { m: [6, 7, 8, 9, 10], s: [8, 9, 10, 11, 12] }[b][lvl - 1];
    const set = sample(LET, n), dup = pick(set), shown = shuffle(set.concat(dup));
    const counts = {}; shown.forEach(x => counts[x] = (counts[x] || 0) + 1);
    if (Object.values(counts).filter(c => c > 1).length !== 1 || counts[dup] !== 2) throw new Error('twins letter');
    return { g: 'twins', mode: 'letter', shown, keys: set.slice().sort(), answer: dup, time: { m: 14, s: 10 }[b] + (5 - lvl), q: 'Which letter appears twice?' };
  }

  /* ---------- balance scales ---------- */
  const FRUIT = ['🍎', '🍌', '🍇', '🍍', '🥭', '🍉'];
  const fmtSide = side => Object.entries(side).filter(([, c]) => c).map(([k, c]) => Array(c).fill(k).join('')).join('');
  function scale(b, lvl) {
    const k = b === 'j' ? 1 : b === 'm' ? (lvl < 3 ? 2 : 3) : (lvl < 2 ? 2 : 3);
    const items = sample(FRUIT, k), unit = '🍒';
    for (let tries = 0; tries < 400; tries++) {
      const w = {}; items.forEach(x => w[x] = ri(2, b === 'j' ? 4 + lvl : 6 + lvl)); w[unit] = 1;
      const val = side => Object.entries(side).reduce((s, [x, c]) => s + w[x] * c, 0);
      const clues = [];
      // chain clues: item0 = cherries, item i = combination of earlier items (+ cherries)
      items.forEach((x, i) => {
        if (i === 0) { clues.push([{ [x]: 1 }, { [unit]: w[x] }]); return; }
        const prev = items[i - 1];
        if (b === 's' && Math.random() < .5) {          // two-item clue: x + prev = cherries
          clues.push([{ [x]: 1, [prev]: 1 }, { [unit]: w[x] + w[prev] }]);
        } else if (w[x] > w[prev]) clues.push([{ [x]: 1 }, { [prev]: 1, [unit]: w[x] - w[prev] }]);
        else if (w[x] === w[prev]) clues.push([{ [x]: 1 }, { [prev]: 1 }]);
        else clues.push([{ [x]: 1, [unit]: w[prev] - w[x] }, { [prev]: 1 }]);
      });
      // the question: some items on the left, how many cherries on the right?
      const left = {}; items.forEach(x => { left[x] = ri(b === 'j' ? 1 : 0, b === 'j' ? 3 : 2); });
      if (!Object.values(left).some(c => c)) left[items[k - 1]] = 1;
      if (b !== 'j' && Object.keys(left).filter(x => left[x]).length === 1 && left[items[0]]) continue;   // too easy
      const ans = val(left);
      if (ans > 30 || ans < 2) continue;
      clues.forEach(([L, Rr]) => { if (val(L) !== val(Rr)) throw new Error('scale clue'); });
      // brute force: every weight set (1..15) that fits all clues must give the same answer
      const vals = new Set(); const rng = Array.from({ length: 15 }, (_, i) => i + 1);
      const rec = (i, cur) => {
        if (vals.size > 1) return;
        if (i === k) { const W = Object.assign({ [unit]: 1 }, cur); const v2 = s => Object.entries(s).reduce((t, [x, c]) => t + W[x] * c, 0);
          if (clues.every(([L, Rr]) => v2(L) === v2(Rr))) vals.add(v2(left)); return; }
        rng.forEach(v => rec(i + 1, Object.assign({}, cur, { [items[i]]: v })));
      };
      rec(0, {});
      if (vals.size !== 1 || !vals.has(ans)) continue;
      return { g: 'scale', items, unit, w, clues: clues.map(([L, Rr]) => [fmtSide(L), fmtSide(Rr)]), clueSides: clues, left, leftTxt: fmtSide(left), answer: ans, max: Math.max(ans + 6, 12) };
    }
    return scale(b, lvl);
  }

  /* ---------- number pyramid ---------- */
  function pyramid(b, lvl) {
    const n = b === 'j' ? 3 : b === 'm' ? (lvl < 3 ? 3 : 4) : (lvl < 3 ? 4 : 5);
    const hide = { j: [2, 2, 3, 3, 3], m: [3, 3, 4, 5, 6], s: [5, 6, 7, 8, 9] }[b][lvl - 1];
    for (let tries = 0; tries < 400; tries++) {
      const rows = [Array.from({ length: n }, () => ri(1, b === 'j' ? 5 : b === 'm' ? 9 + lvl : 12 + 2 * lvl))];
      while (rows[0].length > 1 && rows.length < n) { const p = rows[rows.length - 1]; rows.push(p.slice(1).map((x, i) => p[i] + x)); }
      const cells = []; rows.forEach((r, ri_) => r.forEach((v, ci) => cells.push([ri_, ci])));
      const hidden = new Set(sample(cells, hide).map(c => c.join()));
      // solve by forced steps only
      const known = rows.map((r, a) => r.map((v, c) => hidden.has(a + ',' + c) ? null : v));
      let changed = true;
      while (changed) {
        changed = false;
        for (let a = 1; a < n; a++) for (let c = 0; c < rows[a].length; c++) {
          const P = known[a][c], L = known[a - 1][c], Rr = known[a - 1][c + 1];
          if (P == null && L != null && Rr != null) { known[a][c] = L + Rr; changed = true; }
          else if (P != null && L == null && Rr != null) { known[a - 1][c] = P - Rr; changed = true; }
          else if (P != null && L != null && Rr == null) { known[a - 1][c + 1] = P - L; changed = true; }
        }
      }
      if (known.some((r, a) => r.some((v, c) => v !== rows[a][c]))) continue;
      if (rows[n - 1][0] > (b === 'j' ? 20 : 200)) continue;
      return { g: 'pyramid', rows, hidden: [...hidden].map(x => x.split(',').map(Number)), check: ans => [...hidden].every(k => ans[k] === rows[+k.split(',')[0]][+k.split(',')[1]]) };
    }
    return pyramid(b, lvl);
  }

  /* ---------- number wheel (8 segments, one missing) ---------- */
  const WRULES = {
    oppSum: (s, i, T) => T - s[(i + 4) % 8], oppProd: (s, i, T) => T / s[(i + 4) % 8], oppDiff: (s, i, T) => [s[(i + 4) % 8] + T, s[(i + 4) % 8] - T],
    step: (s, i, T) => s[(i + 7) % 8] + T, double: (s, i) => [s[(i + 4) % 8] * 2, s[(i + 4) % 8] / 2]
  };
  function wheelFits(seg, miss) {        // every simple rule that fits all the other segments → its predicted value(s)
    const out = new Set();
    const others = [0, 1, 2, 3, 4, 5, 6, 7].filter(i => i !== miss);
    const pairs = [0, 1, 2, 3].filter(i => i !== miss % 4);
    const sums = pairs.map(i => seg[i] + seg[i + 4]); if (new Set(sums).size === 1) out.add(sums[0] - seg[(miss + 4) % 8]);
    const prods = pairs.map(i => seg[i] * seg[i + 4]); if (new Set(prods).size === 1) { const v = prods[0] / seg[(miss + 4) % 8]; if (Number.isInteger(v)) out.add(v); }
    const diffs = pairs.map(i => Math.abs(seg[i] - seg[i + 4])); if (new Set(diffs).size === 1) { [seg[(miss + 4) % 8] + diffs[0], seg[(miss + 4) % 8] - diffs[0]].forEach(v => v > 0 && out.add(v)); }
    const ratio = pairs.map(i => seg[i] === 2 * seg[i + 4] ? 'a' : seg[i + 4] === 2 * seg[i] ? 'b' : 'x');
    if (ratio.every(r => r === 'a')) out.add(miss < 4 ? seg[miss + 4] * 2 : seg[miss - 4] / 2);
    if (ratio.every(r => r === 'b')) out.add(miss < 4 ? seg[miss + 4] / 2 : seg[miss - 4] * 2);
    // clockwise step (same jump all the way round, excluding the gap)
    for (let start = 0; start < 8; start++) {
      const seq = Array.from({ length: 8 }, (_, k) => (start + k) % 8);
      const vals = seq.map(i => i === miss ? null : seg[i]);
      const known = vals.map((v, k) => [k, v]).filter(x => x[1] != null);
      const d = (known[1][1] - known[0][1]) / (known[1][0] - known[0][0]);
      if (Number.isInteger(d) && known.every(([k, v]) => v === known[0][1] + d * (k - known[0][0]))) out.add(known[0][1] + d * (seq.indexOf(miss) - known[0][0]));
    }
    return out;
  }
  function wheel(b, lvl) {
    for (let tries = 0; tries < 400; tries++) {
      const kind = b === 'j' ? 'step' : pick(b === 'm' ? ['oppSum', 'step', 'oppDiff', 'double'] : ['oppSum', 'oppProd', 'oppDiff', 'double', 'step']);
      let seg;
      if (kind === 'step') { const d = b === 'j' ? ri(1, 3) : ri(2, 4 + lvl), a = ri(1, 10); seg = Array.from({ length: 8 }, (_, k) => a + d * k); }
      else if (kind === 'oppSum') { const T = ri(15, 20 + 6 * lvl); const a = sample(Array.from({ length: T - 2 }, (_, i) => i + 1), 4); seg = a.concat(a.map(x => T - x)); }
      else if (kind === 'oppProd') { const T = pick([24, 36, 48, 60, 72]); const dv = Array.from({ length: T }, (_, i) => i + 1).filter(x => T % x === 0 && x > 1 && x < T); if (dv.length < 4) continue; const a = sample(dv, 4); seg = a.concat(a.map(x => T / x)); }
      else if (kind === 'oppDiff') { const T = ri(3, 6 + lvl); const a = sample(Array.from({ length: 20 }, (_, i) => i + 1), 4); seg = a.concat(a.map(x => x + T)); }
      else { const a = sample(Array.from({ length: 12 }, (_, i) => i + 2), 4); seg = a.concat(a.map(x => x * 2)); seg = seg.slice(4).concat(seg.slice(0, 4)); }
      if (new Set(seg).size < 8 && kind !== 'oppSum') continue;
      // turn the wheel randomly so the pattern can start anywhere
      const sh = ri(0, 7); seg = seg.slice(sh).concat(seg.slice(0, sh));
      const miss = ri(0, 7), ans = seg[miss];
      const fits = wheelFits(seg, miss);
      if (fits.size !== 1 || !fits.has(ans)) continue;
      const why = { step: 'Going clockwise, every number goes up by the same amount.', oppSum: 'Numbers opposite each other always add up to the same total.', oppProd: 'Numbers opposite each other always multiply to the same total.',
        oppDiff: 'Numbers opposite each other always differ by the same amount.', double: 'Each number is double the number opposite it.' }[kind];
      return { g: 'wheel', seg, miss, answer: ans, kind, why };
    }
    return wheel(b, lvl);
  }

  /* ---------- cube folding ---------- */
  const NETS = [   // [row, col] cells, first is where folding starts
    [[1, 1], [0, 1], [1, 0], [1, 2], [1, 3], [2, 1]], [[1, 1], [0, 0], [1, 0], [1, 2], [1, 3], [2, 1]], [[1, 1], [0, 1], [1, 0], [1, 2], [1, 3], [2, 3]],
    [[1, 1], [0, 0], [1, 0], [1, 2], [2, 2], [2, 3]], [[1, 2], [0, 0], [0, 1], [0, 2], [1, 3], [1, 4]].map(([r, c]) => [r, c]), [[1, 1], [0, 2], [1, 0], [1, 2], [1, 3], [2, 0]]];
  /* fold a net by rolling a cube over it (net seen from outside: mirror the columns so the printed side faces out) */
  function fold(cells) {
    const key = c => c.join(), at = {}; cells.forEach((c, i) => at[key(c)] = i);
    const face = {}; const start = cells[0];
    const go = (cell, die) => {
      const i = at[key(cell)]; if (face[i] != null) return; face[i] = die.bottom;
      [[-1, 0, 'n'], [1, 0, 's'], [0, -1, 'w'], [0, 1, 'e']].forEach(([dr, dc, d]) => {
        const nx = [cell[0] + dr, cell[1] + dc]; if (at[key(nx)] == null) return;
        const D = Object.assign({}, die);
        // printed side faces out = look from below → east/west swap
        const dd = d === 'e' ? 'w' : d === 'w' ? 'e' : d;
        if (dd === 'n') { D.bottom = die.n; D.n = die.top; D.top = die.s; D.s = die.bottom; }
        if (dd === 's') { D.bottom = die.s; D.s = die.top; D.top = die.n; D.n = die.bottom; }
        if (dd === 'e') { D.bottom = die.e; D.e = die.top; D.top = die.w; D.w = die.bottom; }
        if (dd === 'w') { D.bottom = die.w; D.w = die.top; D.top = die.e; D.e = die.bottom; }
        go(nx, D);
      });
    };
    go(start, { bottom: 'B', top: 'T', n: 'N', s: 'S', e: 'E', w: 'W' });
    return face;    // net cell index → cube face
  }
  /* all (top, front, right) views of a cube whose faces carry labels; cube faces: T,B(bottom),N(back),S(front),E(right),W(left) */
  function views(lab) {
    const F = ['T', 'B', 'N', 'S', 'E', 'W'], out = new Set();
    const rx = d => ({ T: d.S, S: d.B, B: d.N, N: d.T, E: d.E, W: d.W }), rz = d => ({ T: d.T, B: d.B, S: d.E, E: d.N, N: d.W, W: d.S });
    const seen = new Set(), st = [Object.fromEntries(F.map(f => [f, f]))];
    while (st.length) { const d = st.pop(), k = F.map(f => d[f]).join(); if (seen.has(k)) continue; seen.add(k); out.add([lab[d.T], lab[d.S], lab[d.E]].join('|')); st.push(rx(d), rz(d)); }
    if (seen.size !== 24) throw new Error('cube turns');
    return out;
  }
  const CUBE_SYM = [['#ff5a5f', '★'], ['#2b8cff', '●'], ['#ffc43d', '▲'], ['#21b573', '■'], ['#9b5cff', '♥'], ['#ff8a1f', '✚'], ['#00b8c7', '◆']];
  function cube(b, lvl) {
    for (let tries = 0; tries < 300; tries++) {
      const net = pick(lvl < 3 ? NETS.slice(0, 2) : NETS);
      const fm = fold(net); if (new Set(Object.values(fm)).size !== 6) continue;
      const syms = sample(CUBE_SYM, 6);
      const lab = {}; Object.entries(fm).forEach(([i, f]) => { lab[f] = i; });   // cube face → net cell index
      const ok = views(lab);
      const all = [];   // every ordered triple of different cells
      for (let a = 0; a < 6; a++) for (let c = 0; c < 6; c++) for (let d = 0; d < 6; d++) if (a !== c && c !== d && a !== d) all.push([a, c, d].join('|'));
      const good = [...ok], bad = all.filter(x => !ok.has(x));
      const ans = pick(good);
      // tricky wrong ones: same three faces in mirror order, then ones using opposite faces
      const [a1, c1, d1] = ans.split('|');
      const mirror = [a1, d1, c1].join('|'), wrong = [];
      if (!ok.has(mirror)) wrong.push(mirror);
      shuffle(bad).forEach(x => { if (wrong.length < 3 && !wrong.includes(x)) wrong.push(x); });
      if (wrong.length < 3 || wrong.some(w => ok.has(w))) continue;
      const opts = shuffle([ans].concat(wrong)).map(x => x.split('|').map(Number));
      return { g: 'cube', net, syms, opts, a: opts.findIndex(o => o.join('|') === ans), fold: fm };
    }
    return cube(b, lvl);
  }

  /* ---------- word jumble ---------- */
  const WORDS = {
    j: { '🐱': 'CAT', '🐶': 'DOG', '🐮': 'COW', '🐷': 'PIG', '🦉': 'OWL', '🐝': 'BEE', '🐜': 'ANT', '🦊': 'FOX', '🚌': 'BUS', '☀️': 'SUN', '🥚': 'EGG', '🐔': 'HEN', '🧢': 'CAP', '🖊️': 'PEN', '🐟': 'FISH', '🐸': 'FROG', '🦁': 'LION', '🐻': 'BEAR', '🦆': 'DUCK', '🍰': 'CAKE', '🌳': 'TREE', '⭐': 'STAR', '🐐': 'GOAT', '🚂': 'TRAIN', '🍎': 'APPLE', '🐯': 'TIGER', '🐴': 'HORSE', '🌙': 'MOON', '🥭': 'MANGO', '🪁': 'KITE', '🌧️': 'RAIN', '🍋': 'LEMON' },
    m: { 'A fruit': ['BANANA', 'ORANGE', 'CHERRY', 'PAPAYA', 'GRAPES', 'GUAVA', 'LITCHI', 'COCONUT'], 'An animal': ['RABBIT', 'MONKEY', 'DONKEY', 'GIRAFFE', 'TURTLE', 'SQUIRREL', 'ELEPHANT', 'LEOPARD'],
         'A planet': ['MERCURY', 'JUPITER', 'SATURN', 'NEPTUNE', 'URANUS'], 'A musical instrument': ['GUITAR', 'VIOLIN', 'TABLA', 'SITAR', 'TRUMPET', 'PIANO'],
         'A sport': ['CRICKET', 'HOCKEY', 'KABADDI', 'TENNIS', 'BOXING', 'CHESS'], 'A colour': ['PURPLE', 'YELLOW', 'MAROON', 'VIOLET', 'INDIGO', 'SILVER'] },
    s: { 'A country': ['PORTUGAL', 'ARGENTINA', 'INDONESIA', 'AUSTRALIA', 'MALAYSIA', 'SINGAPORE', 'BANGLADESH', 'SWITZERLAND'], 'A science word': ['MOLECULE', 'ELECTRON', 'GRAVITY', 'OXYGEN', 'NITROGEN', 'ENZYME', 'NUCLEUS', 'FRICTION'],
         'A job': ['ENGINEER', 'ARCHITECT', 'SCIENTIST', 'JOURNALIST', 'ACCOUNTANT', 'PHARMACIST', 'MECHANIC', 'ELECTRICIAN'], 'A money word': ['INTEREST', 'DIVIDEND', 'INFLATION', 'BUDGET', 'SAVINGS', 'INVOICE', 'TURNOVER', 'LIABILITY'],
         'A shape': ['TRIANGLE', 'PENTAGON', 'HEXAGON', 'CYLINDER', 'RECTANGLE', 'PYRAMID', 'TRAPEZIUM', 'PARALLELOGRAM'] }
  };
  const sortL = w => w.split('').sort().join('');
  function jumble(b, lvl) {
    let word, clue, emoji = '';
    if (b === 'j') { const ok = Object.entries(WORDS.j).filter(([, w]) => w.length <= (lvl < 3 ? 3 : lvl < 5 ? 4 : 5)); [emoji, word] = pick(ok); clue = 'Spell the picture'; }
    else { const cats = WORDS[b]; clue = pick(Object.keys(cats)); const L = cats[clue].filter(w => b === 'm' ? w.length <= 4 + lvl : w.length >= 6 + Math.floor(lvl / 2)); word = pick(L.length ? L : cats[clue]);
      if (cats[clue].filter(w => sortL(w) === sortL(word)).length !== 1) throw new Error('jumble twin'); }
    let tiles; do { tiles = shuffle(word.split('')); } while (tiles.join('') === word && word.length > 2);
    return { g: 'jumble', word, clue, emoji, tiles };
  }

  /* ---------- magic square ---------- */
  const MAGIC = (() => { const out = []; const P = a => a.length <= 1 ? [a] : a.flatMap((x, i) => P(a.slice(0, i).concat(a.slice(i + 1))).map(p => [x].concat(p)));
    P([1, 2, 3, 4, 5, 6, 7, 8, 9]).forEach(p => { const s = 15; if (p[0] + p[1] + p[2] === s && p[3] + p[4] + p[5] === s && p[0] + p[3] + p[6] === s && p[1] + p[4] + p[7] === s && p[0] + p[4] + p[8] === s && p[2] + p[4] + p[6] === s) out.push(p); }); return out; })();
  function magic(b, lvl) {
    const base = pick(MAGIC), k = b === 's' ? ri(0, 5 + lvl) : b === 'm' ? ri(0, 2 + lvl) : 0, sq = base.map(x => x + k);
    const blanks = { j: [2, 2, 3, 3, 3], m: [3, 4, 4, 5, 5], s: [4, 5, 5, 6, 6] }[b][lvl - 1];
    for (let tries = 0; tries < 200; tries++) {
      const hide = sample([0, 1, 2, 3, 4, 5, 6, 7, 8], blanks);
      const fits = MAGIC.map(p => p.map(x => x + k)).filter(p => p.every((v, i) => hide.includes(i) || v === sq[i]));
      if (fits.length !== 1) continue;
      return { g: 'magic', sq, hide, total: 15 + 3 * k, keys: Array.from({ length: 9 }, (_, i) => i + 1 + k) };
    }
    return magic(b, lvl);
  }

  const MAKERS = { memory, twins, scale, pyramid, wheel, cube, jumble, magic };
  const API = { MAKERS, make: (g, b, lvl) => MAKERS[g](b, clamp(lvl, 1, 5)), views, fold, NETS, WORDS, wheelFits, MAGIC, sortL };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.MindPlayGen = API;
})(typeof window !== 'undefined' ? window : this);
