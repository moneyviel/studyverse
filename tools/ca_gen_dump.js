// Test harness for js/ca-gen.js (CA Foundation question engine).
// usage: node tools/ca_gen_dump.js N [out.jsonl] [genId]
//   writes N seeded items per generator and per kind (mcq / desc), difficulties rotating easy/moderate/ICAI,
//   one JSON object per line (stdout if no file). Used by tools/ca_gen_verify.py.
const path = require('path'), fs = require('fs');
const G = require(path.join(__dirname, '..', 'js', 'ca-gen.js'));
const N = +process.argv[2] || 10, out = process.argv[3], only = process.argv[4];
const fd = out ? fs.openSync(out, 'w') : null, t0 = Date.now(); let miss = 0, n = 0;
const h = s => { let x = 2166136261; for (const c of s) { x ^= c.charCodeAt(0); x = Math.imul(x, 16777619); } return x >>> 0; };
for (const g of G._gens) {
  if (only && g.id !== only) continue;
  for (const kind of g.kinds) {
    for (let i = 0; i < N; i++) {
      const seed = (h(g.id + kind) + Math.imul(i, 1000003)) >>> 0;
      const x = G._make(g.id, ['easy', 'moderate', 'ICAI'][i % 3], kind, seed);
      if (!x) { miss++; continue; }
      const line = JSON.stringify(x) + '\n'; n++;
      if (fd) fs.writeSync(fd, line); else process.stdout.write(line);
    }
  }
}
if (fd) fs.closeSync(fd);
console.error(JSON.stringify({ generators: G._gens.length, items: n, failed: miss, ms: Date.now() - t0 }));
