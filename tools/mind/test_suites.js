// Self-test for js/suites-gen.js
const S = require('../../js/suites-gen.js');
let bad = 0, n = 0; const fail = (m, p) => { bad++; if (bad < 12) console.log('FAIL', m, JSON.stringify(p).slice(0, 220)); };
const G = ['fair', 'peace', 'imsg', 'team', 'include', 'yet', 'control', 'plan', 'rocket', 'cope', 'uses', 'link', 'scamper', 'curious', 'riddle'];
for (const b of ['j', 'm', 's', 'p']) for (let l = 1; l <= 5; l++) for (let t = 0; t < 120; t++) for (const g of G) {
  const p = S.make(g, b, l); n++;
  if (p.g === 'fair' && (p.names.length * p.each + p.left !== p.total || p.left >= p.names.length)) fail(g, p);
  if (p.g === 'peace' || p.g === 'plan') { if (p.tiles.slice().sort().join() !== p.steps.slice().sort().join() || new Set(p.steps).size !== p.steps.length) fail(g, p); }
  if (p.g === 'imsg') p.slots.forEach(s => { if (s.opts.filter(o => o.ok).length !== 1) fail(g, p); });
  if (p.g === 'team') { if (new Set(p.people.map(x => x.skill)).size !== p.people.length || p.tasks.some(t => p.people.filter(x => x.skill === t.skill).length !== 1)) fail(g, p); }
  if (p.g === 'include') { if (p.a < 0 || p.opts.length !== 4) fail(g, p); }
  if (p.g === 'bins') { if (!p.items.some(i => i.bin === 0) || !p.items.some(i => i.bin === 1)) fail(g, p); }
  if (p.g === 'multi') { if (p.items.filter(i => i.ok).length !== p.need) fail(g, p); }
  if (p.g === 'link') { const tl = p.tiles.slice(); for (const c of p.answer) { const k = tl.indexOf(c); if (k < 0) fail(g, p); else tl.splice(k, 1); } }
  if (p.g === 'pick') { if (p.a < 0 || new Set(p.opts.map(o => o.t)).size !== p.opts.length) fail(g, p); }
  if (p.g === 'rocket') { // a landing shot must exist: search angles/powers on the app's slider steps
    let ok = false; for (let a = 15; a <= 75 && !ok; a += 5) for (let v = 10; v <= 40 && !ok; v++) { const f = S.flight(a, v, p.wind).land; if (Math.abs(f - p.tx) <= p.tw / 2) ok = true; } if (!ok) fail('rocket unreachable', p); }
}
// the include puzzle must have exactly one activity that works for everyone (re-check from the data)
for (let t = 0; t < 2000; t++) { const p = S.make('include', 's', 3); const fits = p.opts.map(o => S.ACTS.find(a => a.t === o.t)).map(a => p.friends.every(f => { const nd = S.NEEDS.find(x => f.endsWith(x[0])); return !a.a.includes(nd[1]); })); if (fits.filter(Boolean).length !== 1 || !fits[p.a]) fail('include unique', p); n++; }
console.log('puzzles checked:', n, 'failures:', bad); process.exit(bad ? 1 : 0);
