// Self-test for js/heartplay-gen.js — thousands of puzzles, each checked for exactly one best answer.
const H = require('../../js/heartplay-gen.js');
let bad = 0, n = 0; const fail = (m, p) => { bad++; if (bad < 10) console.log('FAIL', m, JSON.stringify(p).slice(0, 240)); };
for (const b of ['j', 'm', 's', 'p']) for (let l = 1; l <= 5; l++) for (let t = 0; t < 300; t++) {
  const f = H.make('faces', b, l); n++;
  if (f.opts.filter(o => o.k === f.answer).length !== 1 || new Set(f.opts.map(o => o.k)).size !== 4) fail('faces', f);
  if (f.mode === 'sit' && f.opts.some(o => o.k !== f.answer && !H.FAR[f.answer].includes(o.k))) fail('faces far', f);
  const th = H.make('thermo', b, l); n++; if (th.tiles.length !== 3 || th.tiles.map(x => x.w).sort().join() !== th.answer.slice().sort().join()) fail('thermo', th);
  const s = H.make('shoes', b, l); n++;
  const tpl = H.SHOES.find(x => x.r.length === s.roles.length && x.r.every((r, i) => s.roles[i].ok.join() === r[1].join()));
  s.stickers.forEach(st => { if (s.roles.filter(r => r.ok.includes(st.k)).length > 1) fail('shoes sticker fits two', s); });
  s.roles.forEach((r, i) => { if (!r.ok.includes(s.answer[i])) fail('shoes answer', s); if (s.stickers.filter(x => r.ok.includes(x.k)).length !== 1) fail('shoes one per role', s); });
  const c = H.make('chat', b, l); n++; if (c.t1.filter(x => x.s === 3).length !== 1 || c.t2.filter(x => x.s === 3).length !== 1) fail('chat', c);
  const p = H.make('paths', b, l); n++; p.steps.forEach(st => { if (st.opts.filter(o => o.best).length !== 1 || st.opts.length !== 3) fail('paths', p); });
  const br = H.make('breathe', b, l); n++; if (!(br.inh > 0 && br.exh > 0 && br.cycles >= 3)) fail('breathe', br);
}
Object.keys(H.SIT).forEach(k => { if (!H.FAR[k] || H.FAR[k].includes(k)) fail('FAR ' + k); });
console.log('puzzles checked:', n, 'failures:', bad); process.exit(bad ? 1 : 0);
