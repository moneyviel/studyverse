#!/usr/bin/env node
/* Key sections & rules — link report.
   For every item in js/ca-keys-data.js: how many CA Foundation MCQs link to it (same matcher as the app, js/ca-keys.js),
   why (tag / sec = section cited with its Act / kw = keyword in scope) and 3 sample questions, so false links can be spotted.
   usage: node tools/ca_keys_report.js [--paper p2] [--zero] [--item ICA-s10] [--samples 3] [--json out.json] */
'use strict';
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const { DATA, KM } = require(path.join(ROOT, 'js/ca-keys.js'));
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const has = k => process.argv.includes(k);
const N = +(arg('--samples') || 3), onlyP = arg('--paper'), onlyItem = arg('--item');

const st = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/ca/foundation/structure.json'), 'utf8'));
const pool = [];
for (const p of st.papers) for (const c of p.chapters) for (const u of c.units) {
  const seen = new Set();
  if (u.status === 'built' && u.file && fs.existsSync(path.join(ROOT, u.file))) {
    const d = JSON.parse(fs.readFileSync(path.join(ROOT, u.file), 'utf8'));
    (d.mcqs || []).forEach(q => { seen.add(q.id); pool.push({ uid: u.id, key: `${u.id}#${q.id}`, q }); });
    (d.cases || []).forEach(cs => (cs.mcqs || []).forEach(q => { seen.add(q.id); pool.push({ uid: u.id, key: `${u.id}#${q.id}`, q }); }));
  }
  const bf = path.join(ROOT, `content/ca/foundation/${p.key}/bank/${u.id}.json`);
  if (fs.existsSync(bf)) { const b = JSON.parse(fs.readFileSync(bf, 'utf8')); if (b.unit === u.id) (b.mcq || []).forEach(q => { if (!seen.has(q.id)) pool.push({ uid: u.id, key: `${u.id}#${q.id}`, q }); }); }
}
const ix = KM.index(pool);
const paperOf = it => KM.groups[it.g].p;
const rows = [], tot = {};
for (const it of DATA.ITEMS) {
  const p = paperOf(it), m = ix[it.id] || [], own = (it.mcqs || []).length;
  const by = { tag: 0, sec: 0, kw: 0 }; m.forEach(e => { by[e.why]++; });
  const t = tot[p] = tot[p] || { items: 0, linked: 0, links: 0, own: 0, ownItems: 0, zero: 0 };
  t.items++; t.links += m.length; t.own += own; if (own) t.ownItems++; if (m.length) t.linked++; if (!m.length && !own) t.zero++;
  rows.push({ id: it.id, p, label: KM.label(it), t: it.t, n: m.length, own, by, samples: m.slice(0, N).map(e => ({ key: e.key, why: e.why, q: String(e.q.q).slice(0, 110) })) });
}
const show = rows.filter(r => (!onlyP || r.p === 'fnd-' + onlyP) && (!onlyItem || r.id === onlyItem) && (!has('--zero') || r.n === 0));
for (const r of show) {
  console.log(`${r.id.padEnd(16)} ${String(r.n).padStart(4)} linked${r.own ? ` + ${r.own} own` : ''}  [sec ${r.by.sec} · kw ${r.by.kw} · tag ${r.by.tag}]  ${r.label} — ${r.t}`);
  r.samples.forEach(s => console.log(`      ${s.why.padEnd(3)} ${s.key.padEnd(34)} ${s.q}`));
}
console.log('\nTotals (MCQ pool: ' + pool.length + ')');
let all = { items: 0, linked: 0, links: 0, own: 0, ownItems: 0, zero: 0 };
for (const p of Object.keys(tot).sort()) { const t = tot[p]; console.log(`  ${p}: ${t.items} items · ${t.linked} with bank links · ${t.links} links · ${t.ownItems} items with ${t.own} own MCQs · ${t.zero} with no questions`); Object.keys(all).forEach(k => { all[k] += t[k]; }); }
console.log(`  all: ${all.items} items · ${all.linked} with bank links · ${all.links} links · ${all.own} own MCQs · ${all.zero} with no questions`);
const distinct = new Set(); Object.values(ix).forEach(l => l.forEach(e => distinct.add(e.key)));
console.log(`  distinct MCQs linked to at least one item: ${distinct.size} of ${pool.length}`);
if (arg('--json')) fs.writeFileSync(arg('--json'), JSON.stringify({ totals: tot, rows }, null, 1));
if (all.zero) process.exitCode = 1;
