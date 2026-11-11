// Self-test for js/mindplay-gen.js: makes thousands of puzzles and re-checks each one in a different way.
const G = require('../../js/mindplay-gen.js');
let bad = 0, n = 0; const fail = (m, p) => { bad++; if (bad < 10) console.log('FAIL', m, JSON.stringify(p).slice(0, 300)); };
// 1. cube chirality: cross net, centre = front, cell above = top, cell right of centre = right
{ const net = [[1, 1], [0, 1], [1, 0], [1, 2], [1, 3], [2, 1]], fm = G.fold(net), lab = {}; Object.entries(fm).forEach(([i, f]) => lab[f] = i);
  const v = G.views(lab); if (!v.has('1|0|3')) fail('cube: top/front/right should be valid'); if (v.has('1|0|2')) fail('cube: mirror order must be invalid');
  // opposite pairs of the cross net: centre–far right, above–below, left–right
  const opp = { T: 'B', B: 'T', N: 'S', S: 'N', E: 'W', W: 'E' }, cellOf = {}; Object.entries(fm).forEach(([i, f]) => cellOf[f] = +i);
  const pairs = new Set(Object.entries(fm).map(([i, f]) => [Math.min(+i, cellOf[opp[f]]), Math.max(+i, cellOf[opp[f]])].join('-')));
  ['0-4', '1-5', '2-3'].forEach(p => { if (!pairs.has(p)) fail('cube opposite ' + p); }); }
for (const b of ['j', 'm', 's']) for (let lvl = 1; lvl <= 5; lvl++) for (let t = 0; t < 120; t++) {
  for (const g of ['memory', 'twins', 'scale', 'pyramid', 'wheel', 'cube', 'jumble', 'magic']) {
    if (g === 'cube' && b === 'j') continue;
    const p = G.make(g, b, lvl); n++;
    if (g === 'memory') { const a = {}; p.pairs.forEach(x => a[x.s] = x.n); if (!p.check(a) || new Set(p.pairs.map(x => x.n)).size !== p.pairs.length) fail(g, p); }
    if (g === 'twins') { if (p.mode === 'digit') { if (p.shown.includes(p.answer) || !p.keys.includes(p.answer) || p.shown.length !== p.keys.length - 1) fail(g, p); }
      else { const c = p.shown.filter(x => x === p.answer).length, others = new Set(p.shown.filter(x => x !== p.answer)); if (c !== 2 || others.size !== p.shown.length - 2) fail(g, p); } }
    if (g === 'scale') { // independent brute force over weights 1..20
      const vals = new Set(), k = p.items.length, rec = (i, W) => { if (i === k) { W['🍒'] = 1; const v = s => Object.entries(s).reduce((t, [x, c]) => t + W[x] * c, 0);
        if (p.clueSides.every(([L, R]) => v(L) === v(R))) vals.add(v(p.left)); return; } for (let x = 1; x <= 20; x++) rec(i + 1, Object.assign({}, W, { [p.items[i]]: x })); };
      rec(0, {}); if (vals.size !== 1 || !vals.has(p.answer)) fail(g + ' ' + [...vals], p); }
    if (g === 'pyramid') { const r = p.rows; for (let a = 1; a < r.length; a++) r[a].forEach((v, c) => { if (v !== r[a - 1][c] + r[a - 1][c + 1]) fail(g, p); });
      const ans = {}; p.hidden.forEach(([a, c]) => ans[a + ',' + c] = r[a][c]); if (!p.check(ans)) fail(g, p); }
    if (g === 'wheel') { const f = G.wheelFits(p.seg, p.miss); if (f.size !== 1 || !f.has(p.answer)) fail(g, p); }
    if (g === 'cube') { const lab = {}; Object.entries(p.fold).forEach(([i, f]) => lab[f] = i); const v = G.views(lab);
      p.opts.forEach((o, i) => { if (v.has(o.join('|')) !== (i === p.a)) fail(g, p); }); }
    if (g === 'jumble') { if (G.sortL(p.tiles.join('')) !== G.sortL(p.word)) fail(g, p); }
    if (g === 'magic') { const fits = G.MAGIC.filter(m => m.every((x, i) => p.hide.includes(i) || x + (p.total - 15) / 3 === p.sq[i])); if (fits.length !== 1) fail(g, p);
      const s = p.sq; [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]].forEach(l => { if (l.reduce((t, i) => t + s[i], 0) !== p.total) fail('magic line', p); }); }
  }
}
// jumble lists: no two words in one category share the same letters
Object.values(G.WORDS).forEach(c => Object.values(c).forEach(L => { if (Array.isArray(L)) { const k = L.map(G.sortL); if (new Set(k).size !== k.length) fail('jumble list', L); } }));
console.log('puzzles checked:', n, 'failures:', bad); process.exit(bad ? 1 : 0);
