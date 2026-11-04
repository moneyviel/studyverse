/* StudyVerse Concept Lab: graphplot — plot y = mx + c, two lines (simultaneous equations) or a quadratic.
 *
 * The child moves sliders and the graph, equation, points table and key facts update live.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode      'line' | 'two' | 'quad'   one line; two lines + intersection; y = ax² + bx + c   default 'line'
 *   m, c      number   starting slope and intercept of line 1                                  default 1, 0
 *   m2, c2    number   starting slope and intercept of line 2 (mode 'two')                     default -1, 4
 *   qa,qb,qc  number   starting a, b, c of the quadratic (mode 'quad')                          default 1, 0, -4
 *   mRange    [min,max,step]  slider range for m and m2                                         default [-4,4,0.5]
 *   cRange    [min,max,step]  slider range for c and c2                                         default [-6,6,1]
 *   aRange, bRange, qcRange   [min,max,step] quadratic sliders   default [-2,2,0.5], [-6,6,1], [-8,8,1]
 *   xr, yr    number   axes run from −xr..xr and −yr..yr                                         default 6, 8
 *   tableX    number[] x values in the points table                                             default [-2,-1,0,1,2]
 *   lock      string[] slider keys to hide/fix, e.g. ['m2','c2'] for a given line               default []
 * Challenge (pick one; if none is given a sensible one is made for the mode):
 *   through   [[x,y],…]  make line 1 pass through all these points ('line')
 *   target    {m,c,m2,c2,qa,qb,qc} any subset — the sliders must reach these values
 *   meet      [x,y]      make the two lines cross at this point ('two')
 *   zeros     [r1,r2]    make the parabola cut the x-axis at these x values ('quad')
 *   challenge string     the challenge sentence shown to the child (else generated)
 *   winText   string     optional win message
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const near = (a, b) => Math.abs(a - b) < 1e-6;
  function frac(v) {
    if (!isFinite(v)) return '—';
    if (near(v, Math.round(v))) return String(Math.round(v)).replace('-', '−');
    for (let d = 2; d <= 12; d++) { const n = v * d; if (near(n, Math.round(n))) return (Math.round(n) < 0 ? '−' : '') + Math.abs(Math.round(n)) + '/' + d; }
    return (Math.round(v * 100) / 100).toString().replace('-', '−');
  }
  const num = v => frac(v);
  function coef(k, sym, first) {
    if (near(k, 0)) return '';
    const s = k < 0 ? (first ? '−' : ' − ') : (first ? '' : ' + ');
    const a = Math.abs(k);
    return s + (near(a, 1) && sym ? '' : frac(a)) + sym;
  }
  function lineEq(m, c) {
    let s = coef(m, 'x', true);
    s += s ? coef(c, '', false) : (near(c, 0) ? '0' : coef(c, '', true));
    return 'y = ' + s;
  }
  function quadEq(a, b, c) {
    let s = coef(a, 'x²', true);
    s += coef(b, 'x', !s);
    s += s ? coef(c, '', false) : (near(c, 0) ? '0' : coef(c, '', true));
    return 'y = ' + s;
  }
  const rng = (r, d) => (Array.isArray(r) && r.length === 3 && r.every(n => isFinite(+n)) && +r[0] < +r[1] && +r[2] > 0) ? r.map(Number) : d;

  Labs.register('graphplot', {
    title: 'Graph plotter',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = ['line', 'two', 'quad'].includes(p.mode) ? p.mode : 'line';
      const xr = Math.max(2, Math.min(20, +p.xr || 6)), yr = Math.max(2, Math.min(40, +p.yr || 8));
      const R = {
        m: rng(p.mRange, [-4, 4, 0.5]), c: rng(p.cRange, [-6, 6, 1]),
        qa: rng(p.aRange, [-2, 2, 0.5]), qb: rng(p.bRange, [-6, 6, 1]), qc: rng(p.qcRange, [-8, 8, 1])
      };
      R.m2 = R.m; R.c2 = R.c;
      const lock = Array.isArray(p.lock) ? p.lock : [];
      const tableX = Array.isArray(p.tableX) && p.tableX.length ? p.tableX.slice(0, 7).map(Number) : [-2, -1, 0, 1, 2];
      const clampK = (k, v) => { const [a, b, s] = R[k]; v = isFinite(+v) ? +v : a; v = Math.round((Math.min(b, Math.max(a, v)) - a) / s) * s + a; return +v.toFixed(4); };
      const keys = mode === 'line' ? ['m', 'c'] : mode === 'two' ? ['m', 'c', 'm2', 'c2'] : ['qa', 'qb', 'qc'];
      const start = { m: p.m ?? 1, c: p.c ?? 0, m2: p.m2 ?? -1, c2: p.c2 ?? 4, qa: p.qa ?? 1, qb: p.qb ?? 0, qc: p.qc ?? -4 };
      const v = {}; Object.keys(start).forEach(k => { v[k] = R[k] ? clampK(k, start[k]) : start[k]; });

      // ---- challenge ----
      let ch = null;
      const through = Array.isArray(p.through) ? p.through.filter(q => Array.isArray(q) && q.length === 2) : null;
      const target = p.target && typeof p.target === 'object' ? p.target : null;
      if (mode === 'line' && through && through.length) ch = { kind: 'through', pts: through };
      else if (mode === 'two' && Array.isArray(p.meet)) ch = { kind: 'meet', pt: p.meet.map(Number) };
      else if (mode === 'quad' && Array.isArray(p.zeros) && p.zeros.length) ch = { kind: 'zeros', z: p.zeros.map(Number).sort((a, b) => a - b) };
      else if (target && keys.some(k => k in target)) ch = { kind: 'target', t: target };
      if (!ch) ch = mode === 'line' ? { kind: 'through', pts: [[1, 3], [3, 7]] } : mode === 'two' ? { kind: 'meet', pt: [2, 3] } : { kind: 'zeros', z: [-1, 3] };
      const P = (x, y) => `(${frac(x)}, ${frac(y)})`;
      const chText = p.challenge || (ch.kind === 'through' ? `Make the line pass through ${ch.pts.map(q => P(q[0], q[1])).join(' and ')}.`
        : ch.kind === 'meet' ? `Make the two lines cross at ${P(ch.pt[0], ch.pt[1])}.`
          : ch.kind === 'zeros' ? `Make the curve cut the x-axis at x = ${ch.z.map(frac).join(' and x = ')}.`
            : `Set ${keys.filter(k => k in ch.t).map(k => `${k.replace('q', '')} = ${frac(+ch.t[k])}`).join(', ')}.`);

      const W = 360, H = 236, PAD = 6;
      const sx = (W - 2 * PAD) / (2 * xr), sy = (H - 2 * PAD) / (2 * yr);
      const X = x => PAD + (x + xr) * sx, Y = y => PAD + (yr - y) * sy;
      const COL = ['#8b5cf6', '#ff6b6b'], QC = '#3b82f6';
      const labelOf = { m: 'm', c: 'c', m2: 'm₂', c2: 'c₂', qa: 'a', qb: 'b', qc: 'c' };
      const colOf = { m: COL[0], c: COL[0], m2: COL[1], c2: COL[1], qa: QC, qb: QC, qc: QC };
      const showKeys = keys.filter(k => !lock.includes(k));

      // grid (static)
      const stepT = xr <= 8 ? 1 : xr <= 16 ? 2 : 5, stepY = yr <= 8 ? 1 : yr <= 20 ? 2 : 5;
      let grid = '';
      for (let x = -xr; x <= xr; x++) grid += `<line x1="${X(x)}" y1="${PAD}" x2="${X(x)}" y2="${H - PAD}" stroke="${x % stepT ? '#eef0fb' : '#dfe3f6'}" stroke-width="1"/>`;
      for (let y = -yr; y <= yr; y++) grid += `<line x1="${PAD}" y1="${Y(y)}" x2="${W - PAD}" y2="${Y(y)}" stroke="${y % stepY ? '#eef0fb' : '#dfe3f6'}" stroke-width="1"/>`;
      grid += `<line x1="${PAD}" y1="${Y(0)}" x2="${W - PAD}" y2="${Y(0)}" stroke="#1b1f3a" stroke-width="1.6"/><line x1="${X(0)}" y1="${PAD}" x2="${X(0)}" y2="${H - PAD}" stroke="#1b1f3a" stroke-width="1.6"/>`;
      for (let x = -xr + stepT; x < xr; x += stepT) if (x) grid += `<text x="${X(x)}" y="${Y(0) + 12}" font-size="9" text-anchor="middle" fill="#6b7090" font-weight="700">${String(x).replace('-', '−')}</text>`;
      for (let y = -yr + stepY; y < yr; y += stepY) if (y) grid += `<text x="${X(0) - 4}" y="${Y(y) + 3}" font-size="9" text-anchor="end" fill="#6b7090" font-weight="700">${String(y).replace('-', '−')}</text>`;
      grid += `<text x="${W - PAD - 2}" y="${Y(0) - 4}" font-size="11" text-anchor="end" font-weight="800" fill="#1b1f3a">x</text><text x="${X(0) + 5}" y="${PAD + 10}" font-size="11" font-weight="800" fill="#1b1f3a">y</text>`;

      host.innerHTML = `
<style>
.lb-graphplot-w input[type=range]{-webkit-appearance:none;appearance:none;height:32px;background:transparent;cursor:pointer}.lb-graphplot-w input[type=range]::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-graphplot-w input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:var(--c,#8b5cf6);margin-top:-8px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}.lb-graphplot-w input[type=range]::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-graphplot-w input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:var(--c,#8b5cf6);border:3px solid #fff}
.lb-graphplot-w{font-size:14px;color:#1b1f3a}
.lb-graphplot-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-graphplot-eqs{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:18px;line-height:1.15;min-height:22px}
.lb-graphplot-svg{width:100%;height:auto;display:block;background:#fbfbff;border-radius:16px;border:2px solid #eef0fb;margin-top:3px}
.lb-graphplot-info{font-size:12.5px;font-weight:800;color:#6b7090;text-align:center;min-height:18px;margin-top:3px}
.lb-graphplot-info b{color:#1b1f3a}
.lb-graphplot-sl{display:grid;grid-template-columns:1fr 1fr;gap:2px 12px;margin-top:2px}
.lb-graphplot-sl.three{grid-template-columns:1fr 1fr 1fr;gap:2px 8px}
.lb-graphplot-s{display:flex;align-items:center;gap:6px;min-height:40px}
.lb-graphplot-s{min-width:0}
.lb-graphplot-s b{font-family:'Baloo 2',Nunito,sans-serif;font-size:15px;min-width:54px;white-space:nowrap}
.lb-graphplot-s input{flex:1;min-width:0;height:32px}
.lb-graphplot-sl.three .lb-graphplot-s{flex-direction:column;gap:0;align-items:stretch;min-height:52px;min-width:0}
.lb-graphplot-sl.three .lb-graphplot-s input{width:100%;flex:none}
.lb-graphplot-sl.three .lb-graphplot-s b{text-align:center}
.lb-graphplot-tb{width:100%;table-layout:fixed;border-collapse:separate;border-spacing:2px;margin-top:3px;font-size:12.5px;font-weight:800;text-align:center}
.lb-graphplot-tb td,.lb-graphplot-tb th{background:#f4f5fd;border-radius:7px;padding:2px 0}
.lb-graphplot-tb th{background:#e8e9f8;color:#6b7090;width:34px}
</style>
<div class="lb-graphplot-w">
  <div class="lb-graphplot-ch">🎯 Challenge: ${esc(chText)}</div>
  <div class="lb-graphplot-eqs"></div>
  <svg class="lb-graphplot-svg" viewBox="0 0 ${W} ${H}"><g>${grid}</g><g class="lb-graphplot-tg"></g><g class="lb-graphplot-pl"></g><g class="lb-graphplot-dots"></g></svg>
  <div class="lb-graphplot-info"></div>
  <div class="lb-graphplot-sl ${showKeys.length === 3 ? 'three' : ''}">${showKeys.map(k => `<label class="lb-graphplot-s"><b style="color:${colOf[k]}">${labelOf[k]} = <span data-v="${k}"></span></b><input type="range" data-k="${k}" min="${R[k][0]}" max="${R[k][1]}" step="${R[k][2]}" value="${v[k]}" style="--c:${colOf[k]}"></label>`).join('')}</div>
  <table class="lb-graphplot-tb"></table>
</div>`;
      const $ = s => host.querySelector(s);
      const eqs = $('.lb-graphplot-eqs'), pl = $('.lb-graphplot-pl'), dots = $('.lb-graphplot-dots'), info = $('.lb-graphplot-info'), tb = $('.lb-graphplot-tb'), tg = $('.lb-graphplot-tg');
      let won = false;

      // target markers
      if (ch.kind === 'through') tg.innerHTML = ch.pts.map(q => `<circle cx="${X(q[0])}" cy="${Y(q[1])}" r="9" fill="none" stroke="#ffc93c" stroke-width="3" stroke-dasharray="4 3"/>`).join('');
      if (ch.kind === 'meet') tg.innerHTML = `<circle cx="${X(ch.pt[0])}" cy="${Y(ch.pt[1])}" r="10" fill="none" stroke="#ffc93c" stroke-width="3" stroke-dasharray="4 3"/>`;
      if (ch.kind === 'zeros') tg.innerHTML = ch.z.map(z => `<circle cx="${X(z)}" cy="${Y(0)}" r="9" fill="none" stroke="#ffc93c" stroke-width="3" stroke-dasharray="4 3"/>`).join('');

      const clipLine = (m, c) => {
        // segment of y = mx + c inside the box
        const pts = [];
        const add = (x, y) => { if (x >= -xr - 1e-9 && x <= xr + 1e-9 && y >= -yr - 1e-9 && y <= yr + 1e-9) pts.push([x, y]); };
        add(-xr, m * -xr + c); add(xr, m * xr + c);
        if (!near(m, 0)) { add((yr - c) / m, yr); add((-yr - c) / m, -yr); }
        if (pts.length < 2) return '';
        pts.sort((a, b) => a[0] - b[0]);
        const a = pts[0], b = pts[pts.length - 1];
        return `M${X(a[0]).toFixed(1)} ${Y(a[1]).toFixed(1)} L${X(b[0]).toFixed(1)} ${Y(b[1]).toFixed(1)}`;
      };
      const curve = f => {
        let d = '', pen = false;
        for (let i = 0; i <= 240; i++) {
          const x = -xr + (2 * xr * i) / 240, y = f(x);
          if (y > yr + 2 || y < -yr - 2) { pen = false; continue; }
          d += (pen ? 'L' : 'M') + X(x).toFixed(1) + ' ' + Y(Math.max(-yr - 2, Math.min(yr + 2, y))).toFixed(1);
          pen = true;
        }
        return d;
      };
      const dot = (x, y, col, r = 4.5) => (Math.abs(x) <= xr && Math.abs(y) <= yr) ? `<circle cx="${X(x)}" cy="${Y(y)}" r="${r}" fill="${col}" stroke="#fff" stroke-width="1.5"/>` : '';
      const tag = (x, y, t, col) => {
        if (Math.abs(x) > xr || Math.abs(y) > yr) return '';
        const tx = Math.min(W - 70, Math.max(4, X(x) + 8)), ty = Math.max(16, Math.min(H - 8, Y(y) - 8));
        return `<rect x="${tx - 3}" y="${ty - 12}" width="${t.length * 6.3 + 6}" height="16" rx="6" fill="#fff" opacity=".92"/><text x="${tx}" y="${ty}" font-size="11.5" font-weight="800" fill="${col}">${esc(t)}</text>`;
      };

      function update() {
        let paths = '', dd = '', inf = '', E = [];
        if (mode !== 'quad') {
          paths += `<path d="${clipLine(v.m, v.c)}" stroke="${COL[0]}" stroke-width="3.5" stroke-linecap="round" fill="none"/>`;
          E.push(`<span style="color:${COL[0]}">${esc(lineEq(v.m, v.c))}</span>`);
          dd += dot(0, v.c, COL[0], 5);
        }
        if (mode === 'two') {
          paths += `<path d="${clipLine(v.m2, v.c2)}" stroke="${COL[1]}" stroke-width="3.5" stroke-linecap="round" fill="none"/>`;
          E.push(`<span style="color:${COL[1]}">${esc(lineEq(v.m2, v.c2))}</span>`);
          if (!near(v.m, v.m2)) {
            const ix = (v.c2 - v.c) / (v.m - v.m2), iy = v.m * ix + v.c;
            dd += dot(ix, iy, '#ffc93c', 7) + tag(ix, iy, P(ix, iy), '#1b1f3a');
            inf = `Lines meet at <b>x = ${frac(ix)}, y = ${frac(iy)}</b> — one solution`;
          } else if (near(v.c, v.c2)) inf = `Same line — <b>infinitely many</b> solutions`;
          else inf = `Parallel lines (same slope) — <b>no solution</b>`;
        }
        if (mode === 'line') {
          inf = `Slope <b>m = ${frac(v.m)}</b> (${near(v.m, 0) ? 'flat' : v.m > 0 ? 'goes up ↗' : 'goes down ↘'}) · cuts y-axis at <b>(0, ${frac(v.c)})</b>`;
          if (!near(v.m, 0)) dd += dot(-v.c / v.m, 0, '#2ed3a5', 4.5);
        }
        if (mode === 'quad') {
          const a = v.qa, b = v.qb, c = v.qc;
          E.push(`<span style="color:${QC}">${esc(quadEq(a, b, c))}</span>`);
          if (near(a, 0)) {
            paths += `<path d="${clipLine(b, c)}" stroke="${QC}" stroke-width="3.5" fill="none"/>`;
            inf = `a = 0, so this is a straight line, not a parabola`;
          } else {
            paths += `<path d="${curve(x => a * x * x + b * x + c)}" stroke="${QC}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" fill="none"/>`;
            const D = b * b - 4 * a * c, vx = -b / (2 * a), vy = a * vx * vx + b * vx + c;
            dd += dot(vx, vy, '#8b5cf6', 4.5);
            if (D > 1e-9) {
              const r1 = (-b - Math.sqrt(D)) / (2 * a), r2 = (-b + Math.sqrt(D)) / (2 * a), lo = Math.min(r1, r2), hi = Math.max(r1, r2);
              dd += dot(lo, 0, '#2ed3a5', 6) + dot(hi, 0, '#2ed3a5', 6);
              const show = r => near(r * 1e4, Math.round(r * 1e4)) || frac(r).includes('/') || near(r, Math.round(r)) ? frac(r) : '≈' + r.toFixed(2);
              inf = `D = ${frac(D)} &gt; 0 → two zeros: <b>x = ${show(lo)}, ${show(hi)}</b>`;
            } else if (near(D, 0)) { dd += dot(vx, 0, '#2ed3a5', 6); inf = `D = 0 → one (repeated) zero: <b>x = ${frac(vx)}</b>`; }
            else inf = `D = ${frac(D)} &lt; 0 → <b>no real zeros</b> (doesn't touch x-axis)`;
            inf += ` · vertex (${frac(vx)}, ${frac(vy)})`;
          }
        }
        // table points on graph
        const fs = mode === 'quad' ? [[x => v.qa * x * x + v.qb * x + v.qc, QC, 'y']] : mode === 'two' ? [[x => v.m * x + v.c, COL[0], 'y₁'], [x => v.m2 * x + v.c2, COL[1], 'y₂']] : [[x => v.m * x + v.c, COL[0], 'y']];
        fs.forEach(([f, col]) => tableX.forEach(x => { dd += `<circle cx="${X(x)}" cy="${Y(f(x))}" r="3" fill="${col}" opacity="${Math.abs(f(x)) <= yr ? .85 : 0}"/>`; }));
        pl.innerHTML = paths; dots.innerHTML = dd; info.innerHTML = inf; eqs.innerHTML = E.join('');
        tb.innerHTML = `<tr><th>x</th>${tableX.map(x => `<td>${frac(x)}</td>`).join('')}</tr>` + fs.map(([f, col, n]) => `<tr><th style="color:${col}">${n}</th>${tableX.map(x => `<td style="color:${col}">${frac(f(x))}</td>`).join('')}</tr>`).join('');
        showKeys.forEach(k => { host.querySelector(`[data-v="${k}"]`).textContent = frac(v[k]); });
        check();
      }
      let touched = false;
      function check() {
        if (won || !touched) return;
        let ok = false, msg = '';
        if (ch.kind === 'through') { ok = ch.pts.every(q => near(v.m * q[0] + v.c, q[1])); msg = `${lineEq(v.m, v.c)} passes through ${ch.pts.map(q => P(q[0], q[1])).join(' and ')}. Slope m = ${frac(v.m)}, intercept c = ${frac(v.c)}.`; }
        else if (ch.kind === 'meet') { ok = !near(v.m, v.m2) && near(v.m * ch.pt[0] + v.c, ch.pt[1]) && near(v.m2 * ch.pt[0] + v.c2, ch.pt[1]); msg = `${lineEq(v.m, v.c)} and ${lineEq(v.m2, v.c2)} meet at ${P(ch.pt[0], ch.pt[1])}, so x = ${frac(ch.pt[0])}, y = ${frac(ch.pt[1])} solves both.`; }
        else if (ch.kind === 'zeros') {
          const a = v.qa, b = v.qb, c = v.qc, D = b * b - 4 * a * c;
          if (!near(a, 0) && D >= -1e-9) {
            const s = Math.sqrt(Math.max(0, D)), r = [(-b - s) / (2 * a), (-b + s) / (2 * a)].sort((x, y) => x - y);
            const z = ch.z.length === 1 ? [ch.z[0], ch.z[0]] : ch.z;
            ok = near(r[0], z[0]) && near(r[1], z[1]);
          }
          msg = `${quadEq(a, b, c)} has zeros x = ${ch.z.map(frac).join(' and ')} — the curve cuts the x-axis there.`;
        } else {
          ok = keys.filter(k => k in ch.t).every(k => near(v[k], +ch.t[k]));
          if (mode === 'two' && !near(v.m, v.m2)) { const ix = (v.c2 - v.c) / (v.m - v.m2); msg = `The lines meet at ${P(ix, v.m * ix + v.c)}: x = ${frac(ix)}, y = ${frac(v.m * ix + v.c)}.`; }
          else msg = `${mode === 'quad' ? quadEq(v.qa, v.qb, v.qc) : lineEq(v.m, v.c)} — well done!`;
        }
        if (ok) { won = true; api.sfx('correct'); api.win(p.winText || msg); }
      }
      const onInput = e => { const k = e.target.dataset && e.target.dataset.k; if (!k) return; touched = true; v[k] = clampK(k, e.target.value); update(); };
      host.addEventListener('input', onInput);
      update();
      return () => host.removeEventListener('input', onInput);
    },
    example: { mode: 'line', m: 1, c: 0, m2: -1, c2: 4, qa: 1, qb: 0, qc: -4, xr: 6, yr: 8, tableX: [-2, -1, 0, 1, 2] },
    examples: [
      { mode: 'two', m: 1, c: 0, m2: 0, c2: 2, target: { m: -1, c: 5, m2: 1, c2: -1 }, challenge: 'Solve x + y = 5 and x − y = 1. Draw y = −x + 5 and y = x − 1. Where do they cross?' },
      { mode: 'quad', qa: 1, qb: 0, qc: 0, zeros: [-1, 3], challenge: 'Find a, b, c so the zeros of y = ax² + bx + c are −1 and 3.' },
      { mode: 'line', m: 0, c: 0, xr: 6, yr: 8, through: [[0, 1], [2, 5]], tableX: [0, 1, 2, 3], challenge: 'Draw the line through (0, 1) and (2, 5). What is its slope?' }
    ]
  });
})();
