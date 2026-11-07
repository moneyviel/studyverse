/* ================= Dashboard engine (SVDash) — premium analytics view, plain SVG =================
   One generic renderer used by the school dashboard (js/insights.js builds the data from its model)
   and by any other module (CA) through Insights.dashboardFor(host, {mode:'ca', data}) or SVDash.render.
   The data shape is documented at the top of js/insights.js. Everything here is computed from that
   shape: KPIs with sparklines and change vs the previous period, strength gauge, predicted readiness,
   accuracy trend, correct/wrong/skipped columns, breakdown bars, radar, mastery donut, activity
   heatmap, streak calendar, time-of-day pattern, confidence matrix, self-check skills, test scores,
   a sortable/filterable table and a question list. Every mark is a button: tapping drills the scope
   (level 1 → 2 → 3 → questions) or narrows the period/filter. Each chart has a one-line summary and a
   table version. Results are cached per data object and filter set. No libraries, no network. */
(function () {
  'use strict';
  const DAY = 864e5;
  const H = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const dkey = t => new Date(t).toISOString().slice(0, 10);          // same day key as the app's today()
  const dnum = d => Date.parse(d + 'T00:00:00Z');
  const addD = (d, n) => dkey(dnum(d) + n * DAY);
  const tdy = () => dkey(Date.now());
  const fmtD = d => new Date(dnum(d)).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });
  const fmtN = n => (n == null ? '–' : Math.round(n).toLocaleString('en-IN'));
  const fmtDur = s => { if (s == null) return '–'; const m = Math.round(s / 60); return m < 60 ? `${m}m` : `${Math.floor(m / 60)}h ${m % 60}m`; };
  const fmtDurL = s => { if (s == null) return 'not tracked'; const m = Math.round(s / 60); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h ${m % 60} min`; };
  const pct = v => v == null ? '–' : Math.round(v) + '%';
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const rmOn = () => document.documentElement.classList.contains('sv-rm');
  const C = { ink: '#15161C', gold: '#C9A76A', goldD: '#8A6A2E', crim: '#B71C2C', ok: '#2E8B57', warn: '#C98A0B', vw: '#7A0F1A', neu: '#6B6F7B', teal: '#2A7F8F' };
  const BANDS = [[0, 'Very weak', C.vw, 'vw'], [40, 'Weak', C.crim, 'w'], [60, 'Strong', C.gold, 's'], [80, 'Very strong', C.ok, 'vs']];
  const band = v => v == null ? null : BANDS.filter(b => v >= b[0]).pop();
  const MASTERY = [['mastered', 'Mastered', '80+ strength'], ['strong', 'Strong', '60–79'], ['learning', 'Learning', '40–59'], ['weak', 'Weak', 'under 40'], ['new', 'Not started', 'no answers yet']];
  const CELLS = { solid: ['Sure', 'Right', 'Solid'], fair: ['Think so', 'Right', 'Fairly solid'], luck: ['Guessing', 'Right', 'Lucky'], mis: ['Sure', 'Wrong', 'Misconception'], gap: ['Not sure', 'Wrong', 'Gap'] };
  const TOD = [[5, 8, 'Early morning', '5–8 am', 'Dawn', 'Dawn', '5–8a'], [8, 12, 'Morning', '8 am–12', 'Morning', 'Morn', '8–12'], [12, 16, 'Afternoon', '12–4 pm', 'Afternoon', 'Aftn', '12–4p'],
    [16, 20, 'Evening', '4–8 pm', 'Evening', 'Eve', '4–8p'], [20, 24, 'Night', '8 pm–12', 'Night', 'Night', '8–12p'], [0, 5, 'Late night', '12–5 am', 'Late', 'Late', '12–5a']];
  const todOf = h => TOD.findIndex(b => h >= b[0] && h < b[1]);

  /* ---------------- index (once per data object) ---------------- */
  const IDX = new WeakMap();
  function index(data) {
    let X = IDX.get(data); if (X) return X;
    const nodes = {}, leaves = [];
    const walk = (list, path, depth) => (list || []).forEach(n => {
      const p = path.concat(n.id); nodes[n.id] = { n, p, depth, kids: (n.children || []).map(c => c.id) };
      if (n.children && n.children.length && depth < 3) walk(n.children, p, depth + 1); else leaves.push(n.id);
    });
    walk(data.tree, [], 1);
    const ev = (data.events || []).filter(e => e && e.t).slice().sort((a, b) => a.t - b.t).map(e => {
      const dt = new Date(e.t); return { e, d: dkey(e.t), h: dt.getHours(), p: e.path || [], ok: e.ok == null ? null : e.ok ? 1 : 0, w: e.kind === 'write' };
    });
    const all = {}, qs = {};
    const A = id => all[id] || (all[id] = { n: 0, ok: 0, w: 0, wSum: 0, last: '' });
    ev.forEach(x => {
      ['*'].concat(x.p).forEach(id => { const a = A(id); if (x.w) { if (x.e.max) { a.w++; a.wSum += x.e.score / x.e.max; } } else if (x.ok != null) { a.n++; a.ok += x.ok; } if (x.d > a.last) a.last = x.d; });
      if (x.e.qid && !x.w) { const q = qs[x.e.qid] || (qs[x.e.qid] = { qid: x.e.qid, p: x.p, n: 0, ok: 0, skip: 0, last: '' }); if (x.ok == null) q.skip++; else { q.n++; q.ok += x.ok; } if (x.d > q.last) q.last = x.d; }
    });
    const tests = (data.tests || []).filter(t => t && t.pct != null).map(t => ({ ...t, d: t.d || dkey(t.t || Date.now()) })).sort((a, b) => a.d < b.d ? -1 : a.d > b.d ? 1 : 0);
    const dayKeys = Object.keys(data.days || {}).sort();
    const first = [ev.length ? ev[0].d : null, dayKeys[0] || null, tests.length ? tests[0].d : null].filter(Boolean).sort()[0] || tdy();
    X = { nodes, leaves, ev, all, qs, tests, first, cache: new Map(), str: {} };
    IDX.set(data, X); return X;
  }
  const inScope = (p, sc) => sc.every((id, i) => p[i] === id);
  const compat = (tp, sc) => !tp || tp.every((id, i) => i >= sc.length || sc[i] === id);   /* a test on a paper counts for its chapters too */

  /* strength 0–100 (all time): node.score if the data gives one, otherwise smoothed accuracy blended with self-check marks */
  function strength(data, X, id) {
    if (id in X.str) return X.str[id];
    let v = null;
    if (id === '*') {
      if (data.overall && data.overall.score != null) v = data.overall.score;
      else { let w = 0, s = 0; (data.tree || []).forEach(n => { const x = strength(data, X, n.id); if (x != null) { const k = Math.sqrt(Math.max(1, (X.all[n.id] || {}).n || 1)); w += k; s += k * x; } }); v = w ? s / w : null; }
    } else {
      const nd = X.nodes[id];
      if (nd && nd.n.score != null && nd.n.enough !== false) v = nd.n.score;
      else if (!(nd && nd.n.enough === false)) {
        const a = X.all[id];
        if (a && a.n + a.w >= 3) { const acc = (a.ok + 1) / (a.n + 2), wr = a.w ? a.wSum / a.w : null; v = 100 * (a.n ? (wr == null ? acc : .7 * acc + .3 * wr) : wr); }
      }
    }
    return (X.str[id] = v);
  }
  const nodeName = (X, id) => id === '*' ? 'All' : ((X.nodes[id] || {}).n || {}).name || id;
  const mastery = (data, X, id) => { const a = X.all[id]; if (!a || !(a.n + a.w)) return 'new'; const s = strength(data, X, id); if (s == null) return 'learning'; return s >= 80 && a.n + a.w >= 4 ? 'mastered' : s >= 60 ? 'strong' : s >= 40 ? 'learning' : 'weak'; };

  /* ---------------- period + slices (cached) ---------------- */
  function period(X, f) {
    const to = f.period === 'custom' && f.to ? f.to : tdy();
    let from;
    if (f.period === 'custom') from = f.from || addD(to, -29);
    else if (f.period === 'all') from = X.first < to ? X.first : addD(to, -6);
    else from = addD(to, -(+f.period - 1));
    if (from > to) from = to;
    const len = Math.round((dnum(to) - dnum(from)) / DAY) + 1;
    const prev = f.period === 'all' ? null : { from: addD(from, -len), to: addD(from, -1) };
    const label = f.period === 'all' ? 'all time' : f.period === 'custom' ? (from === to ? fmtD(from) : `${fmtD(from)} – ${fmtD(to)}`) : `last ${f.period} days`;
    return { from, to, len, prev, label };
  }
  function slice(data, X, sc, from, to, flt) {
    const key = [sc.join('/'), from, to, flt ? JSON.stringify(flt) : ''].join('|');
    if (X.cache.has(key)) return X.cache.get(key);
    const S = { n: 0, ok: 0, wrong: 0, skip: 0, w: 0, wSum: 0, kids: {}, days: {}, tod: TOD.map(() => ({ n: 0, ok: 0 })), cells: { solid: 0, fair: 0, luck: 0, mis: 0, gap: 0 }, rated: 0, qs: {}, skills: {}, secsEv: 0, hasSecs: false };
    const depth = sc.length;
    X.ev.forEach(x => {
      if (x.d < from || x.d > to || !inScope(x.p, sc)) return;
      const cell = x.e.conf && x.ok != null ? (x.ok ? (x.e.conf === 1 ? 'solid' : x.e.conf === 2 ? 'fair' : 'luck') : (x.e.conf === 1 ? 'mis' : 'gap')) : null;
      if (flt && flt.cell && cell !== flt.cell) return;
      if (flt && flt.tod != null && todOf(x.h) !== flt.tod) return;
      if (x.e.secs) { S.secsEv += x.e.secs; S.hasSecs = true; }
      const kid = x.p[depth], K = kid ? (S.kids[kid] || (S.kids[kid] = { n: 0, ok: 0, w: 0, wSum: 0, secs: 0, last: '' })) : null;
      if (K && x.e.secs) K.secs += x.e.secs; if (K && x.d > K.last) K.last = x.d;
      if (x.w) {
        if (x.e.max) { const r = x.e.score / x.e.max; S.w++; S.wSum += r; if (K) { K.w++; K.wSum += r; }
          (x.e.skills || []).forEach(sk => { const s = S.skills[sk] || (S.skills[sk] = { n: 0, sum: 0 }); s.n++; s.sum += r; }); }
        return;
      }
      const D = S.days[x.d] || (S.days[x.d] = { n: 0, ok: 0, wrong: 0, skip: 0 });
      if (x.ok == null) { S.skip++; D.skip++; } else {
        S.n++; S.ok += x.ok; S.wrong += 1 - x.ok; D.n++; D.ok += x.ok; D.wrong += 1 - x.ok;
        if (K) { K.n++; K.ok += x.ok; }
        const t = S.tod[todOf(x.h)]; t.n++; t.ok += x.ok;
      }
      if (cell) { S.cells[cell]++; S.rated++; }
      if (x.e.qid) { const q = S.qs[x.e.qid] || (S.qs[x.e.qid] = { qid: x.e.qid, p: x.p, n: 0, ok: 0, skip: 0, last: '' }); if (x.ok == null) q.skip++; else { q.n++; q.ok += x.ok; } if (x.d > q.last) q.last = x.d; }
    });
    /* time: data.days (level 0: secs, level 1: by[id]) when given, otherwise seconds carried on events */
    S.secsDay = {}; S.xpDay = {}; let secs = null, xp = null, kidsByDays = false;
    Object.entries(data.days || {}).forEach(([d, v]) => {
      if (d < from || d > to || !v) return;
      const s = depth === 0 ? v.secs : depth === 1 && v.by ? v.by[sc[0]] : null;
      if (s != null) { S.secsDay[d] = s; secs = (secs || 0) + s; }
      if (depth === 0 && v.xp != null) { S.xpDay[d] = v.xp; xp = (xp || 0) + v.xp; }
      if (depth === 0 && v.by) { if (!kidsByDays) { kidsByDays = true; Object.values(S.kids).forEach(k => { k.secs = 0; }); }
        Object.entries(v.by).forEach(([id, x]) => { const K = S.kids[id] || (S.kids[id] = { n: 0, ok: 0, w: 0, wSum: 0, secs: 0, last: '' }); K.secs += x || 0; }); }
    });
    if (secs == null && S.hasSecs) { secs = S.secsEv; X.ev.forEach(x => { if (x.e.secs && x.d >= from && x.d <= to && inScope(x.p, sc)) S.secsDay[x.d] = (S.secsDay[x.d] || 0) + x.e.secs; }); }
    S.secs = secs; S.xp = xp;
    S.acc = S.n ? S.ok / S.n * 100 : null;
    S.self = S.w ? S.wSum / S.w * 100 : null;
    S.active = new Set([...Object.keys(S.days), ...Object.keys(S.secsDay).filter(d => S.secsDay[d] > 0)]);
    S.tests = X.tests.filter(t => t.d >= from && t.d <= to && compat(t.path, sc));
    S.testAvg = S.tests.length ? S.tests.reduce((a, t) => a + t.pct, 0) / S.tests.length : null;
    X.cache.set(key, S); return S;
  }
  function buckets(P) {
    const step = P.len <= 31 ? 1 : P.len <= 126 ? 7 : 30, out = [];
    for (let end = P.to; end >= P.from; end = addD(end, -step)) { const st = addD(end, -(step - 1)); out.unshift({ from: st < P.from ? P.from : st, to: end, step }); }
    return out;
  }
  function fill(bks, S) {
    return bks.map(b => { const o = { ...b, n: 0, ok: 0, wrong: 0, skip: 0, secs: 0, xp: 0, act: 0 };
      for (let d = b.from; d <= b.to; d = addD(d, 1)) { const x = S.days[d]; if (x) { o.n += x.n; o.ok += x.ok; o.wrong += x.wrong; o.skip += x.skip; } o.secs += S.secsDay[d] || 0; o.xp += S.xpDay[d] || 0; if (S.active.has(d)) o.act++; }
      o.acc = o.n ? o.ok / o.n * 100 : null; return o; });
  }
  const bLabel = b => b.from === b.to ? fmtD(b.from) : `${fmtD(b.from)} – ${fmtD(b.to)}`;
  function streaks(data, X) {
    const act = new Set(X.ev.map(x => x.d)); Object.entries(data.days || {}).forEach(([d, v]) => { if (v && (v.secs > 0 || v.xp > 0 || v.a > 0)) act.add(d); });
    const sorted = [...act].sort(); let best = 0, run = 0, prev = null;
    sorted.forEach(d => { run = prev && addD(prev, 1) === d ? run + 1 : 1; best = Math.max(best, run); prev = d; });
    let cur = 0, d = act.has(tdy()) ? tdy() : addD(tdy(), -1); while (act.has(d)) { cur++; d = addD(d, -1); }
    const s = data.streak || {};
    return { act, cur: s.n != null ? s.n : cur, best: Math.max(best, s.best || 0, s.n || 0) };
  }

  /* ---------------- tiny SVG pieces ---------------- */
  const attrs = o => Object.entries(o || {}).map(([k, v]) => `data-${k}="${H(v)}"`).join(' ');
  const hit = (go, label, inner, cls = '') => `<g class="dk-hit ${cls}" tabindex="0" role="button" ${attrs(go)} aria-label="${H(label)}" data-tip="${H(label)}">${inner}</g>`;
  function spark(vals, w, h, cls) {
    const pts = vals.map((v, i) => v == null ? null : [vals.length > 1 ? i / (vals.length - 1) * (w - 4) + 2 : w / 2, h - 3 - (h - 6) * v]).filter(Boolean);
    if (!pts.length) return `<svg class="dk-spark" viewBox="0 0 ${w} ${h}" aria-hidden="true"><line x1="2" x2="${w - 2}" y1="${h - 3}" y2="${h - 3}" class="dk-spk-base"/></svg>`;
    const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
    const last = pts[pts.length - 1];
    return `<svg class="dk-spark ${cls || ''}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true"><path d="${d} L${last[0].toFixed(1)},${h} L${pts[0][0].toFixed(1)},${h} Z" class="dk-spk-area"/><path d="${d}" class="dk-spk-line dk-draw" pathLength="1"/><circle cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="2.6" class="dk-spk-dot"/></svg>`;
  }
  const norm = vals => { const mx = Math.max(0, ...vals.filter(v => v != null)); return vals.map(v => v == null ? null : mx ? v / mx : 0); };
  function arcP(cx, cy, r, v0, v1) { const p = v => { const a = Math.PI * (1 - v / 100); return [cx + r * Math.cos(a), cy - r * Math.sin(a)]; }; const [x0, y0] = p(v0), [x1, y1] = p(v1); return `M${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 0 1 ${x1.toFixed(1)},${y1.toFixed(1)}`; }
  function gauge(v) {
    const b = band(v);
    const segs = BANDS.map((x, i) => `<path d="${arcP(100, 100, 80, x[0] + (i ? 1 : 0), (BANDS[i + 1] || [100])[0] - (i < 3 ? 1 : 0))}" class="dk-gseg dk-g-${x[3]}" stroke-width="16" fill="none"/>`).join('');
    const ndl = v == null ? '' : `<g class="dk-needle" style="--r:${(clamp(v, 0, 100) * 1.8 - 90).toFixed(1)}deg"><path d="M100,32 L104.5,100 L95.5,100 Z" class="dk-ndl"/></g><circle cx="100" cy="100" r="8" class="dk-hub"/>`;
    const ticks = [0, 40, 60, 80, 100].map(t => { const a = Math.PI * (1 - t / 100); return `<text x="${(100 + 99 * Math.cos(a)).toFixed(1)}" y="${(100 - 99 * Math.sin(a) + (t === 0 || t === 100 ? 12 : 0)).toFixed(1)}" text-anchor="${t < 50 ? 'end' : t > 50 ? 'start' : 'middle'}" class="dk-ax">${t}</text>`; }).join('');
    return `<svg class="dk-gauge" viewBox="-16 -10 232 124" role="img" aria-label="${v == null ? 'Strength: not enough data yet' : `Strength ${Math.round(v)} out of 100, ${b[1]}`}">${segs}${ticks}${ndl}</svg>`;
  }
  function ring(v, size, label) {
    const r = size / 2 - 7, c = 2 * Math.PI * r, f = v == null ? 0 : clamp(v, 0, 100) / 100;
    return `<svg class="dk-ring" viewBox="0 0 ${size} ${size}" role="img" aria-label="${H(label)}"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="dk-ring-bg"/><circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="dk-ring-fg" stroke-dasharray="${(c * f).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 ${size / 2} ${size / 2})" style="--c:${c.toFixed(1)}"/></svg>`;
  }

  /* ---------------- charts (w = inner card width in CSS px, so SVG text is 1:1 with page text) ---------------- */
  function trendChart(bks, pbks, w, compare) {
    const Hh = 190, L = 36, R = 10, T = 14, B = 26, pw = w - L - R, ph = Hh - T - B;
    const X0 = i => L + (bks.length > 1 ? i / (bks.length - 1) : .5) * pw, Y = v => T + ph * (1 - v / 100);
    const pts = bks.map((b, i) => b.acc == null ? null : { b, i, x: X0(i), y: Y(b.acc) }).filter(Boolean);
    const grid = [0, 25, 50, 75, 100].map(v => `<line x1="${L}" x2="${w - R}" y1="${Y(v)}" y2="${Y(v)}" class="dk-gline${v === 0 ? ' base' : ''}"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end" class="dk-ax">${v}%</text>`).join('');
    const nl = Math.max(2, Math.min(5, Math.floor(pw / 70)));
    const idxs = [...new Set(Array.from({ length: nl }, (_, k) => Math.round(k * (bks.length - 1) / (nl - 1))))];
    const xl = idxs.map(i => `<text x="${X0(i)}" y="${Hh - 6}" text-anchor="${i === 0 ? 'start' : i === bks.length - 1 ? 'end' : 'middle'}" class="dk-ax">${fmtD(bks[i].from)}</text>`).join('');
    const line = pts.length > 1 ? pts.map((p, i) => (i ? 'L' : 'M') + p.x.toFixed(1) + ',' + p.y.toFixed(1)).join(' ') : '';
    const area = line ? `<path d="${line} L${pts[pts.length - 1].x.toFixed(1)},${Y(0)} L${pts[0].x.toFixed(1)},${Y(0)} Z" class="dk-area"/>` : '';
    let prev = '';
    if (compare && pbks) { const pp = pbks.map((b, i) => b.acc == null ? null : [X0(i), Y(b.acc)]).filter(Boolean); if (pp.length > 1) prev = `<path d="${pp.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ')}" class="dk-prevline"/>`; }
    const dots = pts.map(p => hit({ act: 'range', from: p.b.from, to: p.b.to }, `${bLabel(p.b)}: ${Math.round(p.b.acc)}% correct of ${p.b.n} answers. Tap to focus on this ${p.b.step === 1 ? 'day' : 'period'}`,
      `<rect x="${(p.x - Math.max(8, pw / bks.length / 2)).toFixed(1)}" y="${T}" width="${Math.max(16, pw / bks.length).toFixed(1)}" height="${ph}" class="dk-hitr"/><circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${pts.length > 40 ? 3 : 4.5}" class="dk-dot"/>`)).join('');
    const lastP = pts[pts.length - 1];
    const endLbl = lastP ? `<text x="${Math.min(lastP.x, w - R - 2).toFixed(1)}" y="${(lastP.y - 10).toFixed(1)}" text-anchor="end" class="dk-vlab">${Math.round(lastP.b.acc)}%</text>` : '';
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Accuracy over time">${grid}${xl}${area}${prev}${line ? `<path d="${line}" class="dk-line dk-draw" pathLength="1"/>` : ''}${dots}${endLbl}</svg>`;
  }
  function stackChart(bks, w) {
    const Hh = 170, L = 30, R = 6, T = 10, B = 24, pw = w - L - R, ph = Hh - T - B, mx = Math.max(1, ...bks.map(b => b.n + b.skip));
    const nice = mx <= 5 ? 5 : mx <= 10 ? 10 : Math.ceil(mx / 10) * 10, Y = v => T + ph * (1 - v / nice);
    const slot = pw / bks.length, bw = Math.min(24, Math.max(3, slot - 3));
    const grid = [0, nice / 2, nice].map(v => `<line x1="${L}" x2="${w - R}" y1="${Y(v)}" y2="${Y(v)}" class="dk-gline${v === 0 ? ' base' : ''}"/><text x="${L - 5}" y="${Y(v) + 4}" text-anchor="end" class="dk-ax">${fmtN(v)}</text>`).join('');
    const cols = bks.map((b, i) => {
      if (!(b.n + b.skip)) return '';
      const x = L + i * slot + (slot - bw) / 2; let y = Y(0), out = '';
      [['ok', b.ok, 'dk-s-ok'], ['wrong', b.wrong, 'dk-s-bad'], ['skip', b.skip, 'dk-s-skip']].forEach(([, v, cls], k, arr) => {
        if (!v) return; const hgt = ph * v / nice, top = y - hgt, isTop = !arr.slice(k + 1).some(z => z[1]);
        out += isTop ? `<path d="${roundTop(x, top, bw, hgt - (y === Y(0) ? 0 : 2))}" class="${cls}"/>` : `<rect x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(0, hgt - (y === Y(0) ? 0 : 2)).toFixed(1)}" class="${cls}"/>`;
        y = top;
      });
      return hit({ act: 'range', from: b.from, to: b.to }, `${bLabel(b)}: ${b.ok} correct, ${b.wrong} wrong${b.skip ? `, ${b.skip} skipped` : ''}. Tap to focus`, `<rect x="${(L + i * slot).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${ph}" class="dk-hitr"/><g class="dk-grow">${out}</g>`);
    }).join('');
    const nl = Math.max(2, Math.min(5, Math.floor(pw / 70))), idxs = [...new Set(Array.from({ length: nl }, (_, k) => Math.round(k * (bks.length - 1) / (nl - 1))))];
    const xl = idxs.map(i => `<text x="${(L + i * slot + slot / 2).toFixed(1)}" y="${Hh - 6}" text-anchor="${i === 0 ? 'start' : i === bks.length - 1 ? 'end' : 'middle'}" class="dk-ax">${fmtD(bks[i].from)}</text>`).join('');
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Correct, wrong and skipped answers">${grid}${cols}${xl}</svg>`;
  }
  function roundTop(x, y, w, h) { const r = Math.min(4, w / 2, Math.max(0, h)); if (h <= 0) return ''; return `M${x.toFixed(1)},${(y + h).toFixed(1)} V${(y + r).toFixed(1)} Q${x.toFixed(1)},${y.toFixed(1)} ${(x + r).toFixed(1)},${y.toFixed(1)} H${(x + w - r).toFixed(1)} Q${(x + w).toFixed(1)},${y.toFixed(1)} ${(x + w).toFixed(1)},${(y + r).toFixed(1)} V${(y + h).toFixed(1)} Z`; }
  function hbars(rows, w, max, compare) {
    /* rows: {label, v, pv, txt, go, cls} — label above, bar below, value at the tip */
    const rh = compare ? 50 : 44, Hh = rows.length * rh + 4, bw = w - 64;
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Breakdown">${rows.map((r, i) => { const y = i * rh + 2, len = Math.max(r.v ? 4 : 0, bw * clamp((r.v || 0) / max, 0, 1));
      const pl = r.pv == null ? '' : `<rect x="0" y="${y + 36}" width="${Math.max(2, bw * clamp(r.pv / max, 0, 1)).toFixed(1)}" height="5" rx="2.5" class="dk-prevbar"/>`;
      const mxc = Math.max(10, Math.floor(w / 8.2));
      return hit(r.go, `${r.label}: ${r.txt}${r.pv != null ? `, previous period ${Math.round(r.pv)}%` : ''}. ${r.go.act === 'drill' ? 'Tap to open' : ''}`,
        `<rect x="0" y="${y}" width="${w}" height="${rh - 2}" class="dk-hitr"/><text x="0" y="${y + 13}" class="dk-bl">${H(r.label.length > mxc ? r.label.slice(0, mxc - 1) + '…' : r.label)}</text>
        <rect x="0" y="${y + 20}" width="${bw}" height="12" rx="4" class="dk-track"/><rect x="0" y="${y + 20}" width="${len.toFixed(1)}" height="12" rx="4" class="dk-bar dk-growx ${r.cls || ''}"/>${pl}
        <text x="${w}" y="${y + 31}" text-anchor="end" class="dk-bv">${H(r.short || r.txt)}</text>`); }).join('')}</svg>`;
  }
  function radar(items, w) {
    const n = items.length, R = clamp(Math.min(w / 2 - 70, 105), 52, 105), cx = w / 2, cy = R + 30, Hh = 2 * R + 64;
    const pt = (i, r) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; };
    const poly = (f, cls) => `<polygon points="${items.map((x, i) => pt(i, R * f(x) / 100).map(z => z.toFixed(1)).join(',')).join(' ')}" class="${cls}"/>`;
    const rings = [25, 50, 75, 100].map(v => poly(() => v, 'dk-rring')).join('');
    const spokes = items.map((x, i) => { const [x1, y1] = pt(i, R); return `<line x1="${cx}" y1="${cy}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}" class="dk-gline"/>`; }).join('');
    const mx = Math.max(6, Math.floor((w / 2 - R - 14) / 7.4));
    const labels = items.map((x, i) => { const [lx, ly] = pt(i, R + 14), [px, py] = pt(i, R * (x.v || 0) / 100), anc = Math.abs(lx - cx) < 6 ? 'middle' : lx > cx ? 'start' : 'end';
      const lab = x.label.length > mx ? x.label.slice(0, mx - 1) + '…' : x.label, dy = Math.abs(lx - cx) < 6 ? (ly < cy ? -6 : 12) : 4;
      return hit(x.go, `${x.label}: strength ${x.v == null ? 'not enough data' : Math.round(x.v)}. Tap to open`, `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="14" class="dk-hitc"/><circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="4.5" class="dk-dot"/>
        <text x="${lx.toFixed(1)}" y="${(ly + dy).toFixed(1)}" text-anchor="${anc}" class="dk-bl sm">${H(lab)} <tspan class="dk-bv2">${x.v == null ? '–' : Math.round(x.v)}</tspan></text>`); }).join('');
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Strength radar">${rings}${spokes}<g class="dk-pop">${poly(x => x.v || 0, 'dk-rpoly')}</g>${labels}</svg>`;
  }
  function donut(cnt, total, w) {
    const size = Math.min(170, w * .48), r = size / 2 - 14, c = 2 * Math.PI * r; let acc = 0;
    const segs = MASTERY.map(([k, name]) => { const v = cnt[k] || 0; if (!v) return ''; const len = c * v / total, gap = Math.min(2, len / 3), off = acc; acc += len;
      return hit({ act: 'cat', cat: k }, `${name}: ${v} of ${total}. Tap to filter the table`, `<circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="dk-dseg dk-m-${k}" stroke-dasharray="${Math.max(0, len - gap).toFixed(2)} ${c.toFixed(2)}" stroke-dashoffset="${(-off).toFixed(2)}" transform="rotate(-90 ${size / 2} ${size / 2})"/>`); }).join('');
    const m = cnt.mastered || 0;
    return `<svg viewBox="0 0 ${size} ${size}" class="dk-donut" role="group" aria-label="Mastery">${segs}<text x="${size / 2}" y="${size / 2 + 2}" text-anchor="middle" class="dk-dnum">${total ? Math.round(m / total * 100) : 0}%</text><text x="${size / 2}" y="${size / 2 + 20}" text-anchor="middle" class="dk-ax">mastered</text></svg>`;
  }
  function heat(S, P, w, data, X, sc) {
    const td = P.to, cs0 = 15, gap = 3, L = 24, T = 16;
    const maxWeeks = Math.max(5, Math.floor((w - L) / (cs0 + gap)));
    const weeks = clamp(Math.max(Math.ceil((P.len + 6) / 7), Math.floor((w - L) / (22 + gap))), 5, Math.max(5, Math.min(53, maxWeeks)));
    const cs = clamp(Math.floor((w - L) / weeks) - gap, 11, 22);
    const endDow = new Date(dnum(td)).getUTCDay(), start = addD(td, -(weeks * 7 - 1) + (6 - endDow));
    const S2 = slice(data, X, sc, start, td);
    const val = d => (S2.days[d] ? S2.days[d].n + S2.days[d].skip : 0) + Math.round((S2.secsDay[d] || 0) / 120);
    const lvl = v => v <= 0 ? 0 : v < 6 ? 1 : v < 14 ? 2 : v < 28 ? 3 : 4;
    let cells = '';
    for (let wk = 0; wk < weeks; wk++) for (let dw = 0; dw < 7; dw++) {
      const d = addD(start, wk * 7 + dw); if (d > td) continue;
      const v = val(d), inR = d >= P.from, x = L + wk * (cs + gap), y = T + dw * (cs + gap), dd = S2.days[d] || { n: 0, ok: 0 };
      const desc = `${fmtD(d)}: ${dd.n} answers${dd.n ? `, ${Math.round(dd.ok / dd.n * 100)}% correct` : ''}${S2.secsDay[d] ? `, ${fmtDurL(S2.secsDay[d])}` : ''}`;
      const rect = `<rect x="${x}" y="${y}" width="${cs}" height="${cs}" rx="3" class="dk-hm l${lvl(v)}${inR ? '' : ' out'}${d === tdy() ? ' td' : ''}"/>`;
      cells += v > 0 ? hit({ act: 'range', from: d, to: d }, desc + '. Tap to focus on this day', rect) : rect;
    }
    const dl = ['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((x, i) => i % 2 ? `<text x="${L - 7}" y="${T + i * (cs + gap) + cs * .75}" text-anchor="end" class="dk-ax">${x}</text>` : '').join('');
    let ml = '', lastM = -99; for (let wk = 0; wk < weeks; wk++) { const d = addD(start, wk * 7); if ((wk === 0 || d.slice(8) <= '07') && wk - lastM >= 3) { lastM = wk; ml += `<text x="${L + wk * (cs + gap)}" y="11" class="dk-ax">${new Date(dnum(d)).toLocaleDateString('en-IN', { month: 'short', timeZone: 'UTC' })}</text>`; } }
    const Wd = L + weeks * (cs + gap), Hd = T + 7 * (cs + gap);
    return `<svg viewBox="0 0 ${Wd} ${Hd}" class="dk-svg dk-hmsvg" style="max-width:${Wd}px" role="group" aria-label="Activity calendar">${ml}${dl}${cells}</svg>
      <div class="dk-hmkey" aria-hidden="true">Less ${[0, 1, 2, 3, 4].map(l => `<i class="dk-hm l${l}"></i>`).join('')} More</div>`;
  }
  function streakCal(stk, P, w) {
    const end = P.to, y = +end.slice(0, 4), mo = +end.slice(5, 7) - 1, first = new Date(Date.UTC(y, mo, 1)), dim = new Date(Date.UTC(y, mo + 1, 0)).getUTCDate(), off = first.getUTCDay();
    const cs = clamp(Math.floor((w - 6 * 4) / 7), 22, 44), g = 4, Wd = 7 * cs + 6 * g, rows = Math.ceil((off + dim) / 7), Hd = 18 + rows * (cs + g);
    /* the run that makes up the current streak */
    const run = new Set(); let d = stk.act.has(tdy()) ? tdy() : addD(tdy(), -1); while (stk.act.has(d)) { run.add(d); d = addD(d, -1); }
    let out = ['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((x, i) => `<text x="${i * (cs + g) + cs / 2}" y="12" text-anchor="middle" class="dk-ax">${x}</text>`).join('');
    for (let i = 1; i <= dim; i++) {
      const k = off + i - 1, cx = (k % 7) * (cs + g), cy = 18 + Math.floor(k / 7) * (cs + g), dk = `${y}-${String(mo + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
      const a = stk.act.has(dk), r = run.has(dk), fut = dk > tdy();
      const cell = `<rect x="${cx}" y="${cy}" width="${cs}" height="${cs}" rx="${cs / 2}" class="dk-sc${a ? ' on' : ''}${r ? ' run' : ''}${fut ? ' fut' : ''}${dk === tdy() ? ' td' : ''}"/><text x="${cx + cs / 2}" y="${cy + cs / 2 + 4}" text-anchor="middle" class="dk-scn${a ? ' on' : ''}">${i}</text>`;
      out += a ? hit({ act: 'range', from: dk, to: dk }, `${fmtD(dk)}: active${r ? ', part of your current streak' : ''}. Tap to focus`, cell) : cell;
    }
    return `<svg viewBox="0 0 ${Wd} ${Hd}" class="dk-svg" style="max-width:${Math.max(Wd, 280)}px" role="group" aria-label="Streak calendar for ${first.toLocaleDateString('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' })}">${out}</svg>`;
  }
  function todChart(S, w, best) {
    const Hh = 160, T = 22, B = 34, ph = Hh - T - B, slot = w / TOD.length, bw = Math.min(28, slot - 10), mx = Math.max(1, ...S.tod.map(t => t.n));
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Study pattern by time of day"><line x1="0" x2="${w}" y1="${T + ph}" y2="${T + ph}" class="dk-gline base"/>${S.tod.map((t, i) => {
      const hgt = ph * t.n / mx, x = i * slot + (slot - bw) / 2, acc = t.n ? Math.round(t.ok / t.n * 100) : null;
      return hit({ act: 'tod', tod: i }, `${TOD[i][2]} (${TOD[i][3]}): ${t.n} answers${acc != null ? `, ${acc}% correct` : ''}. Tap to see these questions`,
        `<rect x="${(i * slot).toFixed(1)}" y="0" width="${slot.toFixed(1)}" height="${Hh}" class="dk-hitr"/>${t.n ? `<path d="${roundTop(x, T + ph - hgt, bw, hgt)}" class="dk-col dk-grow ${i === best ? 'best' : ''}"/>` : ''}
        ${acc != null ? `<text x="${(x + bw / 2).toFixed(1)}" y="${(T + ph - hgt - 5).toFixed(1)}" text-anchor="middle" class="dk-bv sm">${acc}%</text>` : ''}
        <text x="${(i * slot + slot / 2).toFixed(1)}" y="${Hh - 18}" text-anchor="middle" class="dk-ax">${slot >= 66 ? TOD[i][4] : TOD[i][5]}</text><text x="${(i * slot + slot / 2).toFixed(1)}" y="${Hh - 5}" text-anchor="middle" class="dk-ax sm">${slot >= 66 ? TOD[i][3] : TOD[i][6]}</text>`); }).join('')}</svg>`;
  }
  function matrix(cnt) {
    const cell = k => `<button class="dk-mx dk-c-${k}" data-act="cell" data-cell="${k}" ${cnt[k] ? '' : 'disabled'} aria-label="${CELLS[k][1]} and ${CELLS[k][0]}: ${cnt[k]} answers, ${CELLS[k][2]}"><b>${cnt[k]}</b><span>${CELLS[k][2].replace('Misconception', 'Mis&shy;conception')}</span></button>`;
    return `<div class="dk-mxg"><span></span><span class="dk-mxh">Sure</span><span class="dk-mxh">Think so</span><span class="dk-mxh">Guessing</span>
      <span class="dk-mxr">Right</span>${cell('solid')}${cell('fair')}${cell('luck')}<span class="dk-mxr">Wrong</span>${cell('mis')}<button class="dk-mx dk-c-gap" style="grid-column:span 2" data-act="cell" data-cell="gap" ${cnt.gap ? '' : 'disabled'} aria-label="Wrong and not sure: ${cnt.gap} answers, Gap"><b>${cnt.gap}</b><span>Gap</span></button></div>`;
  }
  function testChart(tests, w) {
    const Hh = 160, L = 34, R = 12, T = 14, B = 24, pw = w - L - R, ph = Hh - T - B, n = tests.length;
    const X0 = i => L + (n > 1 ? i / (n - 1) : .5) * pw, Y = v => T + ph * (1 - v / 100), avg = tests.reduce((a, t) => a + t.pct, 0) / n;
    const grid = [0, 50, 100].map(v => `<line x1="${L}" x2="${w - R}" y1="${Y(v)}" y2="${Y(v)}" class="dk-gline${v === 0 ? ' base' : ''}"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end" class="dk-ax">${v}%</text>`).join('');
    const line = n > 1 ? `<path d="${tests.map((t, i) => (i ? 'L' : 'M') + X0(i).toFixed(1) + ',' + Y(t.pct).toFixed(1)).join(' ')}" class="dk-line alt dk-draw" pathLength="1"/>` : '';
    const dots = tests.map((t, i) => hit(t.path ? { act: 'drill', path: t.path.join('>') } : { act: 'none' }, `${t.name}, ${fmtD(t.d)}: ${Math.round(t.pct)}%`, `<circle cx="${X0(i).toFixed(1)}" cy="${Y(t.pct).toFixed(1)}" r="14" class="dk-hitc"/><circle cx="${X0(i).toFixed(1)}" cy="${Y(t.pct).toFixed(1)}" r="4.5" class="dk-dot alt"/>`)).join('');
    return `<svg viewBox="0 0 ${w} ${Hh}" class="dk-svg" role="group" aria-label="Test scores">${grid}<line x1="${L}" x2="${w - R}" y1="${Y(avg)}" y2="${Y(avg)}" class="dk-avg"/><text x="${w - R}" y="${Y(avg) - 5}" text-anchor="end" class="dk-ax">avg ${Math.round(avg)}%</text>${line}${dots}
      <text x="${L}" y="${Hh - 6}" class="dk-ax">${fmtD(tests[0].d)}</text>${n > 1 ? `<text x="${w - R}" y="${Hh - 6}" text-anchor="end" class="dk-ax">${fmtD(tests[n - 1].d)}</text>` : ''}</svg>`;
  }

  /* ---------------- HTML pieces ---------------- */
  const tbl = (cap, heads, rows) => `<table class="dk-tbl"><caption class="sr-only">${H(cap)}</caption><thead><tr>${heads.map(h => `<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.length ? rows.join('') : `<tr><td colspan="${heads.length}">No data yet</td></tr>`}</tbody></table>`;
  function card(st, id, title, eyebrow, summary, body, table, opts = {}) {
    const tv = st.f.view[id] === 'table';
    return `<section class="dk-card ${opts.span ? 'span' + opts.span : ''} ${opts.cls || ''}" id="dk-${id}" aria-labelledby="dkh-${id}" style="--i:${st.ci++}">
      <div class="dk-ctop"><div><small class="dk-eye">${eyebrow}</small><h3 id="dkh-${id}">${title}</h3></div>${table ? `<button class="dk-tgl" data-act="view" data-id="${id}" aria-pressed="${tv}" data-fk="view-${id}">${tv ? 'Chart' : 'Table'}</button>` : ''}</div>
      ${opts.pre || ''}${summary ? `<p class="dk-sum">${summary}</p>` : ''}<div class="dk-body" ${tv ? 'hidden' : ''}>${body}</div>${table ? `<div class="${tv ? 'dk-tblw' : 'sr-only'}">${table}</div>` : ''}</section>`;
  }
  function delta(cur, prev, kind, P) {
    if (!P.prev) return '<span class="dk-d na">all time</span>';
    if (cur == null || prev == null) return `<span class="dk-d na">${prev == null && cur != null ? 'new' : '–'}</span>`;
    let v, txt;
    if (kind === 'pts') { v = Math.round(cur - prev); txt = `${Math.abs(v)} pt${Math.abs(v) === 1 ? '' : 's'}`; } else { if (!prev) return cur ? '<span class="dk-d up">▲ new</span>' : '<span class="dk-d eq">= 0</span>'; v = Math.round((cur - prev) / prev * 100); txt = `${Math.abs(v)}%`; }
    const cls = v > 0 ? 'up' : v < 0 ? 'dn' : 'eq';
    return `<span class="dk-d ${cls}"><span aria-hidden="true">${v > 0 ? '▲' : v < 0 ? '▼' : '='}</span> ${v ? txt : 'same'}<span class="sr-only"> ${v > 0 ? 'up' : v < 0 ? 'down' : ''} vs previous ${P.len} days</span></span>`;
  }
  function deltaAbs(cur, prev, unit, P) {
    if (!P.prev || prev == null) return '<span class="dk-d na">all time</span>';
    const v = cur - prev, cls = v > 0 ? 'up' : v < 0 ? 'dn' : 'eq';
    return `<span class="dk-d ${cls}"><span aria-hidden="true">${v > 0 ? '▲' : v < 0 ? '▼' : '='}</span> ${v ? Math.abs(v) + ' ' + (Math.abs(v) === 1 ? unit.split(' ')[1].replace(/s$/, '') : unit.split(' ')[1]) : 'same'}<span class="sr-only"> ${unit} ${v > 0 ? 'more' : v < 0 ? 'fewer' : ''} than the previous ${P.len} days</span></span>`;
  }
  function kpi(id, label, val, fmtv, sub, d, sparkVals, act) {
    return `<button class="dk-kpi" data-act="kpi" data-k="${id}" data-fk="kpi-${id}" ${act ? '' : ''}><span class="dk-kl">${label}</span><b class="dk-kv" data-v="${val ?? ''}" data-fmt="${fmtv}">${val == null ? '–' : fmtv === 'pct' ? Math.round(val) + '%' : fmtv === 'dur' ? fmtDur(val) : fmtN(val)}</b>
      <span class="dk-krow">${d}<small>${sub}</small></span>${sparkVals ? spark(sparkVals, 120, 30) : ''}</button>`;
  }

  /* ---------------- main view ---------------- */
  function view(host, st) {
    const { data } = st.opts, X = index(data), f = st.f, sc = f.scope, depth = sc.length, lv = data.levels || ['Subject', 'Chapter', 'Topic'];
    const P = period(X, f), flt = f.cell || f.tod != null ? { cell: f.cell, tod: f.tod } : null;
    const S = slice(data, X, sc, P.from, P.to, flt), PS = P.prev ? slice(data, X, sc, P.prev.from, P.prev.to, flt) : null;
    const bks = fill(buckets(P), S), pbks = P.prev ? fill(buckets({ ...P.prev, len: P.len }), PS) : null;
    const W = st.W, cols = st.cols, cw = n => Math.floor((W - 14 * (cols - 1)) / cols * Math.min(n, cols) + 14 * (Math.min(n, cols) - 1) - 32);
    const scopeId = depth ? sc[depth - 1] : '*', scopeName = nodeName(X, scopeId), kids = depth < 3 ? (depth ? X.nodes[scopeId].kids : (data.tree || []).map(n => n.id)) : [];
    const leafIds = depth >= 3 || !kids.length ? [scopeId] : X.leaves.filter(id => inScope(X.nodes[id].p, sc));
    const kidLevel = lv[depth] || 'Item';
    st.ci = 0;
    /* ----- header + filters ----- */
    const crumbs = [`<button class="dk-crumb" data-act="scope" data-depth="0" data-fk="crumb-0" ${depth ? '' : 'aria-current="page"'}>${H(data.rootName || 'Everything')}</button>`]
      .concat(sc.map((id, i) => `<span aria-hidden="true">›</span><button class="dk-crumb" data-act="scope" data-depth="${i + 1}" data-fk="crumb-${i + 1}" ${i === depth - 1 ? 'aria-current="page"' : ''}>${H(nodeName(X, id))}</button>`)).join('');
    const per = [['7', '7D'], ['30', '30D'], ['90', '90D'], ['all', 'All'], ['custom', 'Custom']];
    const sel1 = `<label class="dk-sel"><span>${H(lv[0])}</span><select data-act="sel" data-depth="1" data-fk="sel-1"><option value="">All ${H(lv[0].toLowerCase())}s</option>${(data.tree || []).map(n => `<option value="${H(n.id)}" ${sc[0] === n.id ? 'selected' : ''}>${H(n.name)}</option>`).join('')}</select></label>`;
    const sel2 = depth >= 1 && X.nodes[sc[0]].kids.length ? `<label class="dk-sel"><span>${H(lv[1])}</span><select data-act="sel" data-depth="2" data-fk="sel-2"><option value="">All ${H(lv[1].toLowerCase())}s</option>${X.nodes[sc[0]].kids.map(id => `<option value="${H(id)}" ${sc[1] === id ? 'selected' : ''}>${H(nodeName(X, id))}</option>`).join('')}</select></label>` : '';
    const chips = [];
    if (f.cell) chips.push(`<button class="dk-chip" data-act="clr" data-k="cell" data-fk="clr-cell">${CELLS[f.cell][2]} answers <span aria-hidden="true">✕</span><span class="sr-only">remove filter</span></button>`);
    if (f.tod != null) chips.push(`<button class="dk-chip" data-act="clr" data-k="tod" data-fk="clr-tod">${TOD[f.tod][2]} only <span aria-hidden="true">✕</span><span class="sr-only">remove filter</span></button>`);
    if (f.cat) chips.push(`<button class="dk-chip" data-act="clr" data-k="cat" data-fk="clr-cat">${MASTERY.find(m => m[0] === f.cat)[1]} only <span aria-hidden="true">✕</span><span class="sr-only">remove filter</span></button>`);
    if (f.back) chips.push(`<button class="dk-chip" data-act="clr" data-k="back" data-fk="clr-back">Focused on ${H(P.label)} · back to ${H(f.back.period === 'all' ? 'all time' : f.back.period === 'custom' ? 'custom' : f.back.period + ' days')} <span aria-hidden="true">✕</span></button>`);
    const head = `<div class="dk-hero">
      <div class="dk-htop"><div><small class="dk-eye gold">${H(data.subtitle || 'Your progress, live')}</small><h2 class="dk-title"><span aria-hidden="true">📊</span> ${H(data.title || 'Dashboard')}</h2></div>
        <button class="dk-cmp" data-act="compare" aria-pressed="${!!f.compare}" data-fk="compare" ${P.prev ? '' : 'disabled'}><span class="dk-sw" aria-hidden="true"><i></i></span>Compare</button></div>
      ${depth ? `<div class="dk-crumbs" role="navigation" aria-label="Dashboard level">${crumbs}</div>` : '<div class="dk-gap"></div>'}
      <div class="dk-filters"><div class="dk-seg" role="group" aria-label="Period">${per.map(([k, n]) => `<button data-act="period" data-p="${k}" aria-pressed="${f.period === k}" data-fk="p-${k}">${n}</button>`).join('')}</div>
        <div class="dk-sels">${sel1}${sel2}</div></div>
      ${f.period === 'custom' ? `<div class="dk-custom"><label>From <input type="date" data-act="date" data-k="from" value="${P.from}" max="${tdy()}" data-fk="from"></label><label>To <input type="date" data-act="date" data-k="to" value="${P.to}" max="${tdy()}" data-fk="to"></label></div>` : ''}
      ${chips.length ? `<div class="dk-chips">${chips.join('')}</div>` : ''}
      <p class="dk-plabel">${H(scopeName === 'All' ? (data.rootName || 'Everything') : scopeName)} · ${H(P.label)}${P.prev ? ` <span>vs ${fmtD(P.prev.from)} – ${fmtD(P.prev.to)}</span>` : ''}</p>`;
    /* ----- KPIs ----- */
    const stk = streaks(data, X);
    const mastN = leafIds.filter(id => mastery(data, X, id) === 'mastered').length;
    const accV = bks.map(b => b.acc == null ? null : b.acc / 100), sixth = S.self != null || (PS && PS.self != null) ? 'self' : (S.tests.length || (PS && PS.tests.length)) ? 'tests' : S.xp != null ? 'xp' : null;
    const k6 = sixth === 'self' ? kpi('self', 'Answer checks', S.self, 'pct', `${S.w} written`, delta(S.self, PS && PS.self, 'pts', P), null)
      : sixth === 'tests' ? kpi('tests', 'Test average', S.testAvg, 'pct', `${S.tests.length} test${S.tests.length === 1 ? '' : 's'}`, delta(S.testAvg, PS && PS.testAvg, 'pts', P), null)
      : sixth === 'xp' ? kpi('xp', 'XP earned', S.xp, 'n', P.label, delta(S.xp, PS && PS.xp, 'pct', P), norm(bks.map(b => b.xp))) : '';
    const nK = k6 ? 6 : 5, perRow = cols === 1 ? 2 : cols === 2 ? 3 : nK;
    const kpis = `<div class="dk-kpis" style="grid-template-columns:repeat(${perRow},minmax(0,1fr))">${kpi('acc', 'Accuracy', S.acc, 'pct', `${fmtN(S.n)} answered`, delta(S.acc, PS && PS.acc, 'pts', P), accV)}
      ${kpi('ans', 'Questions', S.n + S.skip, 'n', S.skip ? `${S.skip} skipped` : P.label, delta(S.n + S.skip, PS && PS.n + PS.skip, 'pct', P), norm(bks.map(b => b.n + b.skip)))}
      ${kpi('time', 'Study time', S.secs, 'dur', S.secs == null ? 'not tracked here' : `${S.active.size} active day${S.active.size === 1 ? '' : 's'}`, S.secs == null ? '' : delta(S.secs, PS && PS.secs, 'pct', P), S.secs == null ? null : norm(bks.map(b => b.secs)))}
      ${kpi('streak', 'Day streak', stk.cur, 'n', `best ${stk.best}`, deltaAbs(S.active.size, PS && PS.active.size, 'active days', P), norm(bks.map(b => b.act)))}
      <button class="dk-kpi" data-act="kpi" data-k="mast" data-fk="kpi-mast"><span class="dk-kl">Mastered</span><b class="dk-kv" data-v="${mastN}" data-fmt="n">${mastN}</b><span class="dk-krow"><small>of ${leafIds.length} ${H((depth >= 3 ? lv[2] : lv[2] || 'topic').toLowerCase())}${leafIds.length === 1 ? '' : 's'}</small></span><span class="dk-kbar" aria-hidden="true"><i style="width:${leafIds.length ? Math.round(mastN / leafIds.length * 100) : 0}%"></i></span></button>
      ${k6}</div></div>`;

    /* ----- standing: gauge + readiness ----- */
    const sv = strength(data, X, scopeId), b = band(sv);
    const recent = slice(data, X, sc, addD(tdy(), -13), tdy());
    const touched = leafIds.filter(id => X.all[id] && (X.all[id].n + X.all[id].w)).length, cov = leafIds.length ? touched / leafIds.length : 0;
    const recentAcc = recent.n ? (recent.ok + 2) / (recent.n + 4) * 100 : sv;
    const scTests = X.tests.filter(t => compat(t.path, sc)).slice(-3);
    let ready = null; const parts = [];
    if (sv != null) {
      ready = .55 * sv + .25 * (recentAcc ?? sv) + 20 * cov; parts.push(['Strength', sv], ['Last 14 days accuracy', recentAcc], ['Coverage', cov * 100]);
      if (scTests.length) { const ta = scTests.reduce((a, t) => a + t.pct, 0) / scTests.length; ready = .6 * ready + .4 * ta; parts.push([`Last ${scTests.length} test${scTests.length > 1 ? 's' : ''}`, ta]); }
    }
    const rTxt = ready == null ? 'Not enough data yet' : ready >= 75 ? 'On track' : ready >= 55 ? 'Getting there' : 'Needs work';
    const nt = data.nextTest && data.nextTest.date ? (() => { const n = Math.round((dnum(data.nextTest.date) - dnum(tdy())) / DAY); return n >= 0 ? `${H(data.nextTest.name || 'Next test')} · in ${n} day${n === 1 ? '' : 's'}` : ''; })() : '';
    const standing = card(st, 'stand', 'Strength & readiness', H(scopeName === 'All' ? 'Overall' : scopeName),
      '', `<div class="dk-stand"><div class="dk-gw">${gauge(sv)}<div class="dk-gl ${b ? 'dk-t-' + b[3] : ''}">${sv == null ? '<span>Not enough data yet</span>' : `<b class="dk-kv" data-v="${sv}" data-fmt="n">${Math.round(sv)}</b><span>${b[1]}</span>`}</div></div>
        <button class="dk-ready" data-act="how" data-fk="how" aria-label="Predicted readiness ${ready == null ? 'not available yet' : Math.round(ready) + ' percent, ' + rTxt}. How is this estimated?"><span class="dk-rw">${ring(ready, 104, '')}<b>${ready == null ? '–' : Math.round(ready) + '%'}</b></span>
          <span class="dk-rt"><small class="dk-eye">Predicted readiness</small><b>${rTxt}</b><small>${nt || `for a test on ${H(scopeName === 'All' ? 'what you have studied' : scopeName)}`}</small><u>How is this estimated?</u></span></button></div>
        ${st.how ? `<div class="dk-how" id="dkHow"><p>An estimate, not a promise. It mixes your strength (55%), your accuracy in the last 14 days (25%) and how much of this you have practised (20%)${scTests.length ? '; then your last tests count for 40%' : ''}.</p>${parts.map(([n, v]) => `<div class="dk-mini"><span>${H(n)}</span><i><i style="width:${Math.round(clamp(v ?? 0, 0, 100))}%"></i></i><b>${pct(v)}</b></div>`).join('')}
          <p>Strength bands: under 40 very weak · 40–59 weak · 60–79 strong · 80+ very strong.</p></div>` : ''}`, null, { span: 1, cls: 'dk-standc' });
    /* ----- trend ----- */
    const withD = bks.filter(b => b.acc != null);
    const half = Math.floor(withD.length / 2), accOf = xs => { const n = xs.reduce((a, b) => a + b.n, 0); return n ? Math.round(xs.reduce((a, b) => a + b.ok, 0) / n * 100) : null; };
    const tSum = !withD.length ? `No answers in ${P.label}.` : withD.length < 2 ? `${Math.round(withD[0].acc)}% correct on ${bLabel(withD[0])}.` : (() => { const a = accOf(withD.slice(0, half)), z = accOf(withD.slice(half)); return `${Math.round(S.acc)}% correct in ${P.label}. Earlier ${a}%, more recently ${z}% — ${z > a ? `up ${z - a} point${z - a === 1 ? '' : 's'}` : z < a ? `down ${a - z} point${a - z === 1 ? '' : 's'}` : 'steady'}.${f.compare && PS && PS.acc != null ? ` Previous period: ${Math.round(PS.acc)}%.` : ''} Tap a point to focus on it.`; })();
    const legendT = f.compare && P.prev ? `<div class="dk-legend"><span><i class="dkl-line"></i>This period</span><span><i class="dkl-prev"></i>Previous period</span></div>` : '';
    const trend = card(st, 'trend', 'Accuracy trend', 'Over time', tSum, withD.length ? legendT + trendChart(bks, pbks, cw(2), f.compare) : emptyMini('No answers in this period'),
      tbl('Accuracy over time', ['Period', 'Answers', 'Correct'], withD.map(b => `<tr><td><button class="dk-tl" data-act="range" data-from="${b.from}" data-to="${b.to}">${H(bLabel(b))}</button></td><td>${b.n}</td><td>${Math.round(b.acc)}%</td></tr>`)), { span: 2 });
    /* ----- stacked ----- */
    const anyQ = bks.some(b => b.n + b.skip);
    const stack = card(st, 'stack', 'Correct, wrong & skipped', 'Every answer', anyQ ? `${S.ok} correct, ${S.wrong} wrong${S.skip ? `, ${S.skip} skipped` : ''} in ${P.label}.` : '',
      anyQ ? `<div class="dk-legend"><span><i class="dkl-ok"></i>Correct ${S.ok}</span><span><i class="dkl-bad"></i>Wrong ${S.wrong}</span>${S.skip ? `<span><i class="dkl-skip"></i>Skipped ${S.skip}</span>` : ''}</div>${stackChart(bks, cw(2))}` : emptyMini('Nothing answered in this period'),
      tbl('Correct, wrong and skipped', ['Period', 'Correct', 'Wrong', 'Skipped'], bks.filter(b => b.n + b.skip).map(b => `<tr><td>${H(bLabel(b))}</td><td>${b.ok}</td><td>${b.wrong}</td><td>${b.skip}</td></tr>`)), { span: 2 });
    /* ----- breakdown bars (children) ----- */
    const met = f.metric || 'acc';
    const krows = kids.map(id => { const k = S.kids[id] || {}, pk = PS && PS.kids[id] || {}; const a = k.n ? k.ok / k.n * 100 : null, pa = pk.n ? pk.ok / pk.n * 100 : null;
      return { id, name: nodeName(X, id), n: k.n || 0, acc: a, pacc: pa, secs: k.secs || 0, psecs: pk.secs || 0, str: strength(data, X, id), last: (X.all[id] || {}).last || '', mast: mastery(data, X, id), self: k.w ? k.wSum / k.w * 100 : null }; });
    const metSw = `<div class="dk-seg sm" role="group" aria-label="Measure">${[['acc', 'Accuracy'], ['str', 'Strength'], ['n', 'Answers'], ['secs', 'Time']].map(([k, n]) => `<button data-act="metric" data-m="${k}" aria-pressed="${met === k}" data-fk="m-${k}">${n}</button>`).join('')}</div>`;
    const mv = r => met === 'acc' ? r.acc : met === 'str' ? r.str : met === 'n' ? r.n : r.secs;
    const shown = krows.filter(r => met === 'acc' || met === 'str' ? mv(r) != null : mv(r) > 0).sort((a, b) => mv(b) - mv(a));
    const mtxt = r => met === 'acc' ? `${Math.round(r.acc)}% of ${r.n}` : met === 'str' ? `${Math.round(r.str)} · ${band(r.str)[1]}` : met === 'n' ? `${r.n} answers` : fmtDurL(r.secs);
    const mshort = r => met === 'acc' ? `${Math.round(r.acc)}%` : met === 'str' ? `${Math.round(r.str)}` : met === 'n' ? fmtN(r.n) : fmtDur(r.secs);
    const bmax = met === 'acc' || met === 'str' ? 100 : Math.max(1, ...shown.map(mv), ...(f.compare ? shown.map(r => met === 'n' ? 0 : r.psecs) : []));
    const drillGo = id => ({ act: 'drill', path: X.nodes[id].p.join('>') });
    const bars = kids.length ? card(st, 'bars', `By ${kidLevel.toLowerCase()}`, H(scopeName === 'All' ? 'Breakdown' : scopeName),
      shown.length ? `${met === 'acc' ? 'Highest accuracy' : met === 'str' ? 'Strongest' : met === 'n' ? 'Most answers' : 'Most time'}: ${H(shown[0].name)} (${mtxt(shown[0])})${shown.length > 1 ? `; lowest: ${H(shown[shown.length - 1].name)} (${mtxt(shown[shown.length - 1])})` : ''}. Tap a bar to open it.` : `No data for ${P.label}.`,
      shown.length ? (f.compare && met === 'acc' ? `<div class="dk-legend"><span><i class="dkl-line"></i>This period</span><span><i class="dkl-prev"></i>Previous</span></div>` : '') + hbars(shown.slice(0, 14).map(r => ({ label: r.name, v: mv(r), pv: f.compare && met === 'acc' ? r.pacc : null, txt: mtxt(r), short: mshort(r), go: drillGo(r.id), cls: met === 'str' ? 'dk-b-' + band(r.str)[3] : '' })), cw(1), bmax, f.compare && met === 'acc') : emptyMini('Nothing yet'),
      tbl(`By ${kidLevel}`, [kidLevel, 'Answers', 'Accuracy', 'Strength', 'Time'], krows.map(r => `<tr><td><button class="dk-tl" data-act="drill" data-path="${H(X.nodes[r.id].p.join('>'))}">${H(r.name)}</button></td><td>${r.n}</td><td>${pct(r.acc)}</td><td>${r.str == null ? '–' : Math.round(r.str)}</td><td>${fmtDurL(r.secs)}</td></tr>`)), { pre: metSw }) : '';
    /* ----- radar ----- */
    const rItems = krows.filter(r => r.str != null).map(r => ({ label: r.name, v: r.str, go: drillGo(r.id) }));
    const rad = kids.length ? card(st, 'radar', `Strength by ${kidLevel.toLowerCase()}`, 'Balance', rItems.length ? `Strongest: ${H(rItems.slice().sort((a, b) => b.v - a.v)[0].label)} (${Math.round(Math.max(...rItems.map(x => x.v)))}); weakest: ${H(rItems.slice().sort((a, b) => a.v - b.v)[0].label)} (${Math.round(Math.min(...rItems.map(x => x.v)))}).${rItems.length < kids.length ? ` ${kids.length - rItems.length} without enough data yet.` : ''}` : 'Not enough data yet.',
      rItems.length >= 3 ? radar(rItems.slice(0, 10), cw(1)) : rItems.length ? hbars(rItems.map(x => ({ label: x.label, v: x.v, txt: `${Math.round(x.v)} · ${band(x.v)[1]}`, short: String(Math.round(x.v)), go: x.go, cls: 'dk-b-' + band(x.v)[3] })), cw(1), 100) : emptyMini('Answer a few questions in each ' + kidLevel.toLowerCase()),
      tbl('Strength', [kidLevel, 'Strength', 'Band'], krows.map(r => `<tr><td>${H(r.name)}</td><td>${r.str == null ? '–' : Math.round(r.str)}</td><td>${r.str == null ? 'Not enough data' : band(r.str)[1]}</td></tr>`))) : '';
    /* ----- mastery donut ----- */
    const mc = {}; leafIds.forEach(id => { const m = mastery(data, X, id); mc[m] = (mc[m] || 0) + 1; });
    const leafName = (lv[2] || 'topic').toLowerCase();
    const dn = depth < 3 && leafIds.length > 1 ? card(st, 'mast', `${lv[2] || 'Topic'} mastery`, 'Where you stand', `${mc.mastered || 0} of ${leafIds.length} ${leafName}s mastered${mc.weak ? `, ${mc.weak} weak` : ''}${mc.new ? `, ${mc.new} not started` : ''}. Tap a slice to filter the table.`,
      `<div class="dk-dwrap">${donut(mc, leafIds.length, cw(1))}<div class="dk-dleg">${MASTERY.map(([k, n, d]) => `<button data-act="cat" data-cat="${k}" aria-pressed="${f.cat === k}" data-fk="cat-${k}" ${mc[k] ? '' : 'disabled'}><i class="dk-m-${k}"></i><span>${n}<small>${d}</small></span><b>${mc[k] || 0}</b></button>`).join('')}</div></div>`,
      tbl('Mastery', ['Level', leafName + 's'], MASTERY.map(([k, n]) => `<tr><td>${n}</td><td>${mc[k] || 0}</td></tr>`))) : '';
    /* ----- heatmap + streak ----- */
    const hm = card(st, 'heat', 'Activity calendar', 'Consistency', S.active.size ? `Active on ${S.active.size} of ${P.len} days in ${P.label}. Darker squares mean more practice. Tap a day to focus on it.` : `No activity in ${P.label}.`,
      heat(S, P, cw(2), data, X, sc), tbl('Active days', ['Day', 'Answers', 'Correct', 'Time'], [...S.active].sort().reverse().slice(0, 60).map(d => { const x = S.days[d] || { n: 0, ok: 0 }; return `<tr><td>${fmtD(d)}</td><td>${x.n}</td><td>${x.n ? Math.round(x.ok / x.n * 100) + '%' : '–'}</td><td>${fmtDurL(S.secsDay[d] || 0)}</td></tr>`; })), { span: 2 });
    const stc = card(st, 'streak', `${stk.cur} day streak`, new Date(dnum(P.to)).toLocaleDateString('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' }),
      `${stk.cur ? `You have studied ${stk.cur} day${stk.cur > 1 ? 's' : ''} in a row.` : 'Study today to start a streak.'} Best ever: ${stk.best} day${stk.best === 1 ? '' : 's'}.`,
      `<div class="dk-legend"><span><i class="dkl-on"></i>Active</span><span><i class="dkl-run"></i>Current streak</span></div>${streakCal(stk, P, cw(1))}`, null);
    /* ----- time of day ----- */
    const todBest = (() => { let bi = -1, ba = -1; S.tod.forEach((t, i) => { if (t.n >= 5 && t.ok / t.n > ba) { ba = t.ok / t.n; bi = i; } }); return bi; })();
    const todMost = S.tod.reduce((bi, t, i, a) => t.n > a[bi].n ? i : bi, 0);
    const tod = card(st, 'tod', 'When you study', 'Time of day', S.n ? `Most answers: ${TOD[todMost][2].toLowerCase()} (${S.tod[todMost].n}).${todBest >= 0 ? ` Best accuracy: ${TOD[todBest][2].toLowerCase()} (${Math.round(S.tod[todBest].ok / S.tod[todBest].n * 100)}%) — highlighted.` : ''}` : `No answers in ${P.label}.`,
      S.n ? todChart(S, cw(1), todBest) : emptyMini('No answers yet'), tbl('Time of day', ['Time', 'Answers', 'Correct'], S.tod.map((t, i) => `<tr><td>${TOD[i][2]} (${TOD[i][3]})</td><td>${t.n}</td><td>${t.n ? Math.round(t.ok / t.n * 100) + '%' : '–'}</td></tr>`)));
    /* ----- confidence ----- */
    const conf = card(st, 'conf', 'Confidence vs correct', 'Honesty check', S.rated ? `${S.rated} answers rated. ${S.cells.mis ? `${S.cells.mis} sure-but-wrong (misconceptions) — fix these first.` : 'No sure-but-wrong answers.'}${S.cells.luck ? ` ${S.cells.luck} lucky guesses.` : ''} Tap a box to see those questions.` : 'Rate how sure you are in tests — this grid shows what you really know.',
      matrix(S.cells), tbl('Confidence vs correct', ['Result', 'Count'], Object.keys(CELLS).map(k => `<tr><td>${CELLS[k][1]} + ${CELLS[k][0]} (${CELLS[k][2]})</td><td>${S.cells[k]}</td></tr>`)));
    /* ----- skills (self-check) ----- */
    const sk = Object.entries(S.skills).map(([k, v]) => ({ k, name: (data.skills || {})[k] || k, v: v.sum / v.n * 100, n: v.n })).sort((a, b) => a.v - b.v);
    const skills = sk.length ? card(st, 'skills', 'Written answers by skill', 'Checked answer marks', `Weakest skill: ${H(sk[0].name)} (${Math.round(sk[0].v)}%).${sk.length > 1 ? ` Strongest: ${H(sk[sk.length - 1].name)} (${Math.round(sk[sk.length - 1].v)}%).` : ''}`,
      hbars(sk.map(s => ({ label: s.name, v: s.v, txt: `${Math.round(s.v)}% · ${s.n} answer${s.n > 1 ? 's' : ''}`, short: `${Math.round(s.v)}%`, go: { act: 'none' }, cls: 'dk-b-' + band(s.v)[3] })), cw(1), 100),
      tbl('Skills', ['Skill', 'Average mark', 'Answers'], sk.map(s => `<tr><td>${H(s.name)}</td><td>${Math.round(s.v)}%</td><td>${s.n}</td></tr>`))) : '';
    /* ----- tests ----- */
    const tlist = S.tests;
    const tests = tlist.length ? card(st, 'tests', data.testLabel || 'Test scores', `${tlist.length} in ${H(P.label)}`, `Average ${Math.round(S.testAvg)}%${PS && PS.testAvg != null ? ` (previous period ${Math.round(PS.testAvg)}%)` : ''}. Latest: ${H(tlist[tlist.length - 1].name)} — ${Math.round(tlist[tlist.length - 1].pct)}%.`,
      testChart(tlist, cw(1)), tbl('Tests', ['Test', 'Date', 'Score'], tlist.slice().reverse().map(t => `<tr><td>${H(t.name)}</td><td>${fmtD(t.d)}</td><td>${Math.round(t.pct)}%</td></tr>`))) : '';
    /* ----- table of children (sortable, filterable, inline mini bars) ----- */
    let table = '';
    if (kids.length) {
      const q = (f.q || '').toLowerCase();
      let rows = krows.filter(r => (!q || r.name.toLowerCase().includes(q)) && (!f.cat || (depth === 2 ? r.mast === f.cat : leafIds.some(id => X.nodes[id].p.includes(r.id) && mastery(data, X, id) === f.cat))));
      const keyF = { name: r => r.name.toLowerCase(), str: r => r.str ?? -1, acc: r => r.acc ?? -1, n: r => r.n, d: r => r.acc != null && r.pacc != null ? r.acc - r.pacc : -999, last: r => r.last };
      const sk2 = f.sort || 'str', dir = f.dir || 1, isNA = r => (sk2 === 'str' && r.str == null) || (sk2 === 'acc' && r.acc == null) || (sk2 === 'd' && (r.acc == null || r.pacc == null));
      rows.sort((a, b) => { if (isNA(a) !== isNA(b)) return isNA(a) ? 1 : -1; const x = keyF[sk2](a), y = keyF[sk2](b); return (x < y ? -1 : x > y ? 1 : 0) * dir; });
      const th = (k, n) => `<th scope="col" aria-sort="${sk2 === k ? (dir > 0 ? 'ascending' : 'descending') : 'none'}"><button class="dk-sort" data-act="sort" data-k="${k}" data-fk="sort-${k}">${n}<span aria-hidden="true">${sk2 === k ? (dir > 0 ? ' ▲' : ' ▼') : ''}</span></button></th>`;
      const mb = (v, cls) => v == null ? '<span class="dk-na">–</span>' : `<span class="dk-mb"><i class="${cls}" style="width:${Math.round(clamp(v, 0, 100))}%"></i></span><b>${Math.round(v)}</b>`;
      table = `<section class="dk-card span3" id="dk-table" aria-labelledby="dkh-table" style="--i:${st.ci++}"><div class="dk-ctop"><div><small class="dk-eye">${H(scopeName === 'All' ? 'Details' : scopeName)}</small><h3 id="dkh-table">${H(kidLevel)}s</h3></div></div>
        <div class="dk-tf"><label class="dk-search"><span class="sr-only">Filter ${H(kidLevel.toLowerCase())}s by name</span><input type="search" data-act="q" data-fk="q" placeholder="Filter ${H(kidLevel.toLowerCase())}s…" value="${H(f.q || '')}"></label>${f.cat ? `<button class="dk-chip" data-act="clr" data-k="cat">${MASTERY.find(m => m[0] === f.cat)[1]} ✕</button>` : ''}</div>
        <p class="dk-sum" aria-live="polite">${rows.length} of ${krows.length} shown${sk2 === 'str' && dir > 0 ? ', weakest first' : ''}. Tap a heading to sort, a name to open.</p>
        <div class="dk-tscroll"><table class="dk-tbl dk-main"><caption class="sr-only">${H(kidLevel)}s with strength, accuracy in ${H(P.label)}, answers, change and last practised</caption>
        <thead><tr>${th('name', H(kidLevel))}${th('str', 'Strength')}${th('acc', 'Accuracy')}${th('n', 'Answers')}${th('d', 'Change')}${th('last', 'Last')}</tr></thead><tbody>
        ${rows.length ? rows.map(r => { const dv = r.acc != null && r.pacc != null ? Math.round(r.acc - r.pacc) : null; return `<tr><td><button class="dk-tl" data-act="drill" data-path="${H(X.nodes[r.id].p.join('>'))}">${H(r.name)}</button></td><td class="dk-mbc">${mb(r.str, r.str == null ? '' : 'dk-b-' + band(r.str)[3])}</td><td class="dk-mbc">${mb(r.acc, 'dk-acc')}</td><td>${r.n}</td><td>${dv == null ? '–' : `<span class="dk-d ${dv > 0 ? 'up' : dv < 0 ? 'dn' : 'eq'} lt"><span aria-hidden="true">${dv > 0 ? '▲' : dv < 0 ? '▼' : '='}</span> ${Math.abs(dv)}<span class="sr-only"> points ${dv > 0 ? 'up' : dv < 0 ? 'down' : ''}</span></span>`}</td><td>${r.last ? fmtD(r.last) : '–'}</td></tr>`; }).join('') : `<tr><td colspan="6">No ${H(kidLevel.toLowerCase())}s match.</td></tr>`}</tbody></table></div></section>`;
    }
    /* ----- questions (leaf scope, or a confidence / time-of-day filter) ----- */
    let qcard = '';
    if (depth >= 3 || !kids.length || f.cell || f.tod != null) {
      const leafNode = X.nodes[scopeId];
      const qmap = Object.values(S.qs).sort((a, b) => (a.ok / (a.n || 1)) - (b.ok / (b.n || 1)) || b.n - a.n);
      const qInfo = q => { const ln = X.nodes[q.p[q.p.length - 1]]; return ((ln && ln.n.questions) || {})[q.qid] || null; };
      qcard = `<section class="dk-card span3" id="dk-qs" aria-labelledby="dkh-qs" style="--i:${st.ci++}"><div class="dk-ctop"><div><small class="dk-eye">${H(f.cell ? CELLS[f.cell][2] : f.tod != null ? TOD[f.tod][2] : scopeName)} · ${H(P.label)}</small><h3 id="dkh-qs">Questions</h3></div>
        ${depth >= 3 && st.opts.onLeaf ? `<button class="dk-tgl" data-act="leaf" data-fk="leaf">${H(st.opts.leafLabel || 'Open lesson & practice')} ›</button>` : ''}</div>
        <p class="dk-sum">${qmap.length ? `${qmap.length} question${qmap.length > 1 ? 's' : ''} answered, the ones you got wrong most first. Tap one to see the answer.` : `No questions answered here in ${H(P.label)}.`}${leafNode && leafNode.n.note ? ' ' + H(leafNode.n.note) : ''}</p>
        ${qmap.slice(0, f.qn || 15).map((q, i) => { const info = qInfo(q), acc = q.n ? Math.round(q.ok / q.n * 100) : null;
          return `<details class="dk-q"><summary><span class="dk-qn">${i + 1}</span><span class="dk-qb"><b>${H(info ? info.q : 'Question ' + q.qid)}</b><small>${q.n} attempt${q.n === 1 ? '' : 's'} · ${q.ok} right${q.skip ? ` · ${q.skip} skipped` : ''}${q.last ? ` · last ${fmtD(q.last)}` : ''}${depth < 3 ? ` · ${H(nodeName(X, q.p[q.p.length - 1]))}` : ''}</small></span><span class="dk-qp ${acc == null ? '' : acc >= 80 ? 'g' : acc >= 50 ? 'm' : 'b'}">${acc == null ? '–' : acc + '%'}</span></summary>
            <div class="dk-qa">${info ? `${info.a != null ? `<p><b>Correct answer:</b> ${H(info.a)}</p>` : ''}${info.explain ? `<p>${H(info.explain)}</p>` : ''}` : '<p>Details for this question are not available here.</p>'}</div></details>`; }).join('')}
        ${qmap.length > (f.qn || 15) ? `<button class="dk-more" data-act="qmore" data-fk="qmore">Show ${Math.min(15, qmap.length - (f.qn || 15))} more</button>` : ''}</section>`;
    }
    const order = depth >= 3 ? [standing, trend, stack, hm, stc, tod, conf, skills, tests] : [standing, trend, bars, dn, stack, rad, hm, stc, tod, conf, skills, tests];
    st.say = `${scopeName === 'All' ? '' : scopeName + ', '}${P.label}: ${S.acc == null ? 'no answers' : Math.round(S.acc) + '% accuracy'}, ${S.n + S.skip} questions.`;
    return `${head}${kpis}<div class="dk-grid" data-cols="${cols}">${qcard && (f.cell || f.tod != null) ? qcard : ''}${order.join('')}${table}${qcard && !(f.cell || f.tod != null) ? qcard : ''}</div>`;
  }
  const emptyMini = t => `<div class="dk-emini"><span aria-hidden="true">◌</span>${H(t)}</div>`;

  /* ---------------- empty state ---------------- */
  function emptyView(host, st, n, need) {
    const sample = sampleData(st.opts.mode === 'ca' ? 'ca' : 'school');
    const pv = { opts: { data: sample, mode: st.opts.mode }, f: defaults(), W: st.W, cols: st.cols, ci: 0, preview: true };
    return `<div class="dk-empty"><div class="dk-preview" aria-hidden="true" inert>${view(host, pv)}</div>
      <div class="dk-onb" role="region" aria-labelledby="dkOnbT"><div class="dk-onbin">
        <div class="dk-onbicon" aria-hidden="true">${ring(n / need * 100, 96, '')}<b>${n}/${need}</b></div>
        <small class="dk-eye gold">${H(st.opts.data.subtitle || 'Your dashboard')}</small>
        <h2 id="dkOnbT">Answer ${need} questions to light up your dashboard</h2>
        <p>${n ? `${n} done, ${need - n} to go.` : 'It takes about five minutes.'} Then you will see your accuracy trend, strength gauge, streak calendar, weak spots and a readiness estimate for your next test — all tappable.</p>
        <ul class="dk-onbl"><li><span aria-hidden="true">📈</span> Accuracy trend & change vs last week</li><li><span aria-hidden="true">🧭</span> Strength by ${H(((st.opts.data.levels || ['Subject'])[0]).toLowerCase())}, chapter and topic</li><li><span aria-hidden="true">🔥</span> Streak calendar & study times</li></ul>
        ${st.opts.onStart ? `<button class="dk-cta" data-act="start" data-fk="start">${H(st.opts.startLabel || 'Start answering')} <span aria-hidden="true">›</span></button>` : ''}
        <small class="dk-note">Preview with sample data</small></div></div></div>`;
  }

  /* ---------------- sample data (preview + demos) ---------------- */
  function sampleData(kind) {
    let seed = kind === 'ca' ? 11 : 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const names = kind === 'ca' ? ['Accounting', 'Business Laws', 'Quantitative Aptitude', 'Business Economics'] : ['Maths', 'Science', 'English', 'Social Science', 'Hindi'];
    const skill = ['concept', 'application', 'computation', 'presentation'];
    const tree = names.map((nm, i) => ({ id: 's' + i, name: nm, children: [0, 1, 2].map(c => ({ id: `s${i}c${c}`, name: `Chapter ${c + 1}`, children: [0, 1, 2].map(u => ({ id: `s${i}c${c}u${u}`, name: `${kind === 'ca' ? 'Unit' : 'Topic'} ${u + 1}` })) })) }));
    const events = [], days = {}, tests = [], now = Date.now(), base = [.82, .64, .74, .55, .7];
    for (let b = 60; b >= 0; b--) {
      if (rnd() < .3) continue;
      const d = dkey(now - b * DAY), hr = [7, 17, 19, 20, 21][Math.floor(rnd() * 5)]; let secs = 0;
      for (let k = 0; k < 2; k++) { const s = Math.floor(rnd() * names.length), c = Math.floor(rnd() * 3), u = Math.floor(rnd() * 3), n = 4 + Math.floor(rnd() * 8);
        for (let q = 0; q < n; q++) { const r = rnd(); events.push({ t: dnum(d) + (hr + k) * 36e5 + q * 6e4, path: ['s' + s, `s${s}c${c}`, `s${s}c${c}u${u}`], qid: `s${s}c${c}u${u}#${q % 5}`, ok: r < .04 ? null : r < base[s] + (60 - b) / 600 ? 1 : 0, conf: rnd() < .4 ? 1 + Math.floor(rnd() * 3) : 0 }); }
        if (kind === 'ca' && rnd() < .5) events.push({ t: dnum(d) + hr * 36e5, path: ['s' + s, `s${s}c${c}`, `s${s}c${c}u${u}`], kind: 'write', score: 2 + Math.floor(rnd() * 4), max: 5, skills: [skill[Math.floor(rnd() * 4)]] });
        secs += n * 40; }
      days[d] = { secs, xp: Math.round(secs / 20) };
    }
    [45, 30, 16, 5].forEach((b, i) => tests.push({ t: now - b * DAY, d: dkey(now - b * DAY), name: kind === 'ca' ? `Mock test ${i + 1}` : `Chapter test ${i + 1}`, pct: [54, 61, 68, 74][i], path: ['s' + (i % names.length)] }));
    return { title: 'Dashboard', subtitle: kind === 'ca' ? 'CA Foundation' : 'Sample', levels: kind === 'ca' ? ['Paper', 'Chapter', 'Unit'] : ['Subject', 'Chapter', 'Topic'], tree, events, days, tests,
      skills: { concept: 'Concept clarity', application: 'Applying concepts', computation: 'Computation', presentation: 'Presentation & format' } };
  }

  /* ---------------- state, render, events ---------------- */
  function defaults() { return { period: '30', scope: [], compare: false, view: {}, metric: 'acc', sort: 'str', dir: 1, q: '', cat: null, cell: null, tod: null, back: null, qn: 15 }; }
  function measure(host) {
    const w = host.clientWidth || 360, cols = w >= 860 ? 3 : w >= 560 ? 2 : 1;
    return { W: w, cols };
  }
  function render(host, opts) {
    if (!host) return;
    const prev = host._dsh;
    const st = prev && prev.opts.data === opts.data ? Object.assign(prev, { opts }) : { opts, f: Object.assign(defaults(), (prev && prev.f) || {}, opts.filters || {}), how: false, kv: {} };
    if (prev && prev.opts.data !== opts.data && prev.f) st.f.scope = prev.f.scope.filter(id => index(opts.data).nodes[id]);
    host._dsh = st; paint(host, true);
    if (!host._dshWired) wire(host);
    return { refresh: () => paint(host), state: st };
  }
  function paint(host, first) {
    const st = host._dsh; if (!st) return;
    Object.assign(st, measure(host));
    const X = index(st.opts.data), need = st.opts.data.minEvents ?? 8;
    const answered = Math.max(X.ev.length, st.opts.data.answered || 0);
    const fk = document.activeElement && host.contains(document.activeElement) ? document.activeElement.getAttribute('data-fk') : null;
    let html;
    try { html = answered < need ? emptyView(host, st, answered, need) : view(host, st); }
    catch (e) { console.error(e); html = '<div class="dk-card"><p class="dk-sum">Something went wrong showing the dashboard.</p></div>'; }
    host.innerHTML = `<div class="dsh${st.opts.mode === 'ca' ? ' dsh-ca' : ''}" role="region" aria-label="${H(st.opts.data.title || 'Dashboard')}">${html}<div class="dk-tip" role="tooltip" hidden></div></div>`;
    host._dshW = st.W;
    countUp(host, st);
    if (fk) { const el = host.querySelector(`[data-fk="${CSS.escape(fk)}"]`); if (el) el.focus({ preventScroll: true }); }
    if (!first && st.say) { try { if (window.A11Y && A11Y.announce) A11Y.announce(st.say); } catch (e) {} }
  }
  function countUp(host, st) {
    const els = host.querySelectorAll('.dsh > .dk-kpis .dk-kv[data-v], .dk-gl .dk-kv[data-v]');
    if (rmOn() || !window.requestAnimationFrame) { els.forEach(e => { st.kv[e.closest('[data-fk]') ? e.closest('[data-fk]').dataset.fk : 'g'] = +e.dataset.v; }); return; }
    els.forEach(e => {
      const key = e.closest('[data-fk]') ? e.closest('[data-fk]').dataset.fk : 'g', to = e.dataset.v === '' ? null : +e.dataset.v, from = st.kv[key] ?? 0, fm = e.dataset.fmt;
      st.kv[key] = to; if (to == null || from === to) return;
      const t0 = performance.now(), dur = 650, out = v => fm === 'pct' ? Math.round(v) + '%' : fm === 'dur' ? fmtDur(v) : fmtN(v);
      const step = now => { const k = Math.min(1, (now - t0) / dur), e2 = 1 - Math.pow(1 - k, 3); if (!e.isConnected) return; e.textContent = out(from + (to - from) * e2); if (k < 1) requestAnimationFrame(step); };
      e.textContent = out(from); requestAnimationFrame(step);
    });
  }
  function wire(host) {
    host._dshWired = true;
    const set = (fn, scroll) => { const st = host._dsh; fn(st.f, st); const y = window.scrollY; paint(host); if (scroll !== false) window.scrollTo(0, y); };
    const scrollToCard = id => { const c = host.querySelector('#dk-' + id); if (!c) return; c.scrollIntoView({ behavior: rmOn() ? 'auto' : 'smooth', block: 'start' }); c.classList.add('dk-flash'); setTimeout(() => c.classList.remove('dk-flash'), 1200); };
    const act = el => {
      const d = el.dataset, st = host._dsh; if (!st) return;
      try { if (typeof sfx === 'function') sfx('tap'); } catch (e) {}
      switch (d.act) {
        case 'period': return set(f => { f.period = d.p; f.back = null; if (d.p === 'custom' && !f.from) { f.to = tdy(); f.from = addD(tdy(), -13); } });
        case 'compare': return set(f => { f.compare = !f.compare; });
        case 'scope': return set(f => { f.scope = f.scope.slice(0, +d.depth); f.cat = null; f.q = ''; f.qn = 15; });
        case 'drill': if (!d.path) return; return set(f => { f.scope = d.path.split('>'); f.cat = null; f.q = ''; f.qn = 15; }), window.scrollTo({ top: host.getBoundingClientRect().top + window.scrollY - 10, behavior: rmOn() ? 'auto' : 'smooth' });
        case 'range': return set(f => { if (!f.back) f.back = { period: f.period, from: f.from, to: f.to }; f.period = 'custom'; f.from = d.from; f.to = d.to; });
        case 'clr': return set(f => { if (d.k === 'back' && f.back) { f.period = f.back.period; f.from = f.back.from; f.to = f.back.to; f.back = null; } else f[d.k] = null; });
        case 'cell': return set(f => { f.cell = f.cell === d.cell ? null : d.cell; }), setTimeout(() => scrollToCard('qs'), 30);
        case 'tod': return set(f => { f.tod = f.tod === +d.tod ? null : +d.tod; }), setTimeout(() => scrollToCard('qs'), 30);
        case 'cat': return set(f => { f.cat = f.cat === d.cat ? null : d.cat; }), setTimeout(() => scrollToCard('table'), 30);
        case 'metric': return set(f => { f.metric = d.m; });
        case 'view': return set(f => { f.view[d.id] = f.view[d.id] === 'table' ? 'chart' : 'table'; });
        case 'sort': return set(f => { if (f.sort === d.k) f.dir *= -1; else { f.sort = d.k; f.dir = d.k === 'name' || d.k === 'str' || d.k === 'acc' ? 1 : -1; } });
        case 'qmore': return set(f => { f.qn = (f.qn || 15) + 15; });
        case 'how': return set((f, s) => { s.how = !s.how; });
        case 'kpi': { const t = { acc: 'trend', ans: 'stack', time: 'heat', streak: 'streak', mast: 'mast', self: 'skills', tests: 'tests', xp: 'heat' }[d.k]; return scrollToCard(t === 'mast' && !host.querySelector('#dk-mast') ? 'table' : t); }
        case 'start': return st.opts.onStart && st.opts.onStart();
        case 'leaf': return st.opts.onLeaf && st.opts.onLeaf(st.f.scope.slice());
      }
    };
    host.addEventListener('click', e => { const el = e.target.closest('[data-act]'); if (!el || !host.contains(el) || el.disabled || ['sel', 'date', 'q', 'none'].includes(el.dataset.act)) return; act(el); });
    host.addEventListener('keydown', e => { const el = e.target.closest('g[data-act]'); if (el && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); act(el); } });
    host.addEventListener('change', e => { const el = e.target; const d = el.dataset;
      if (d.act === 'sel') set(f => { const dep = +d.depth; f.scope = f.scope.slice(0, dep - 1); if (el.value) f.scope.push(el.value); f.cat = null; f.q = ''; });
      if (d.act === 'date') set(f => { f[d.k] = el.value || null; if (f.from && f.to && f.from > f.to) { const t = f.from; f.from = f.to; f.to = t; } }); });
    let qT; host.addEventListener('input', e => { const el = e.target; if (el.dataset.act !== 'q') return; clearTimeout(qT); qT = setTimeout(() => { const pos = el.selectionStart; set(f => { f.q = el.value; }); const n = host.querySelector('[data-fk="q"]'); if (n) { n.focus(); try { n.setSelectionRange(pos, pos); } catch (x) {} } }, 220); });
    /* tooltip */
    const tipShow = (el, x, y) => { const tip = host.querySelector('.dk-tip'), root = host.querySelector('.dsh'); if (!tip || !root) return; tip.textContent = el.dataset.tip; tip.hidden = false;
      const rb = root.getBoundingClientRect(), z = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--z')) || 1, sx = rb.width / root.offsetWidth || 1;
      let lx = (x - rb.left) / sx, ly = (y - rb.top) / sx; const tw = tip.offsetWidth; lx = clamp(lx - tw / 2, 4, root.offsetWidth - tw - 4); tip.style.left = lx + 'px'; tip.style.top = (ly - tip.offsetHeight - 12) + 'px'; void z; };
    const tipHide = () => { const tip = host.querySelector('.dk-tip'); if (tip) tip.hidden = true; };
    host.addEventListener('pointerover', e => { const el = e.target.closest('[data-tip]'); if (el && e.pointerType === 'mouse') { const r = el.getBoundingClientRect(); tipShow(el, r.left + r.width / 2, r.top); } });
    host.addEventListener('pointerout', e => { if (e.target.closest('[data-tip]')) tipHide(); });
    host.addEventListener('focusin', e => { const el = e.target.closest('[data-tip]'); if (el) { const r = el.getBoundingClientRect(); tipShow(el, r.left + r.width / 2, r.top); } else tipHide(); });
    host.addEventListener('focusout', tipHide);
    /* re-layout when the width changes (rotation, text size) */
    let rT; const ro = () => { clearTimeout(rT); rT = setTimeout(() => { if (host.isConnected && host._dsh && host.clientWidth && Math.abs(host.clientWidth - (host._dshW || 0)) > 8) paint(host); }, 150); };
    if (window.ResizeObserver) new ResizeObserver(ro).observe(host); else window.addEventListener('resize', ro);
  }

  /* ---------------- compact tile (home + Me) ---------------- */
  function tile(data, opts = {}) {
    const X = index(data), need = data.minEvents ?? 8, n = Math.max(X.ev.length, data.answered || 0);
    const lbl = H(opts.label || 'Dashboard');
    if (n < need) return `<button class="dk-tile empty" id="${opts.id || ''}" data-dk-open="1" aria-label="${lbl}. Answer ${need} questions to light up your dashboard. ${n} of ${need} done. Open">
      <span class="dk-tl1"><small class="dk-eye gold">Your progress</small><b><span aria-hidden="true">📊</span> ${lbl}</b><span class="dk-tsub">Answer ${need} questions to light it up</span>
      <span class="dk-tprog" aria-hidden="true"><i style="width:${Math.round(n / need * 100)}%"></i></span><span class="dk-tsub sm">${n} of ${need} done</span></span>
      <span class="dk-tghost" aria-hidden="true">${spark([.2, .35, .3, .5, .45, .62, .58, .75], 120, 44)}</span><span class="dk-tgo" aria-hidden="true">›</span></button>`;
    const P = period(X, { period: '7' }), S = slice(data, X, [], P.from, P.to), PS = slice(data, X, [], P.prev.from, P.prev.to);
    const sv = strength(data, X, '*'), b = band(sv), stk = streaks(data, X), bks = fill(buckets({ ...P, len: 14, from: addD(P.to, -13) }), slice(data, X, [], addD(P.to, -13), P.to));
    return `<button class="dk-tile" id="${opts.id || ''}" data-dk-open="1" aria-label="${lbl}: strength ${sv == null ? 'not enough data' : Math.round(sv) + ', ' + b[1]}; accuracy this week ${pct(S.acc)}; ${stk.cur} day streak. Open dashboard">
      <span class="dk-tl1"><small class="dk-eye gold">Your progress, live</small><b><span aria-hidden="true">📊</span> ${lbl}</b>
        <span class="dk-tstats"><span><b>${sv == null ? '–' : Math.round(sv)}</b><small>Strength${b ? ' · ' + b[1] : ''}</small></span><span><b>${pct(S.acc)}</b><small>7-day accuracy ${S.acc != null && PS.acc != null ? (S.acc >= PS.acc ? '▲' : '▼') + Math.abs(Math.round(S.acc - PS.acc)) : ''}</small></span><span><b>${stk.cur}</b><small>Day streak</small></span></span></span>
      <span class="dk-tspark" aria-hidden="true">${spark(norm(bks.map(x => x.n)), 120, 44)}<small>Last 14 days</small></span><span class="dk-tgo" aria-hidden="true">›</span></button>`;
  }

  window.SVDash = { render, tile, sampleData, index, _strength: (d, id) => strength(d, index(d), id || '*') };
})();
