/* StudyVerse Concept Lab: statlab — statistics workbench (CBSE Class 11 Economics "Statistics for
 * Economics", Class 11 Maths sets & statistics, Class 12 probability).
 *
 * MODES
 *   central      Drag the dots of a dot plot: n, mean, median, mode, Q1, Q3 and a box plot update live.
 *                With `freq` (grouped data) it becomes a histogram: drag bar tops to change frequencies;
 *                mean (direct method), median = L + ((N/2 − c.f.)/f)·h and mode = L + (f1 − f0)/(2f1 − f0 − f2)·h
 *                are worked out with the numbers shown.
 *   correlation  Drag points on a scatter plot; Karl Pearson's r and Spearman's rank correlation
 *                (with the NCERT tie correction) are computed exactly.
 *   normal       Normal curve with μ and σ sliders; drag the two handles to shade an area;
 *                P = Φ(z₂) − Φ(z₁) with z = (x − μ)/σ.
 *   venn         2 or 3 sets in a universal set. Tap regions to shade A∪B, A∩B′, (A∪B)′ … then Check.
 *                n(region) values are shown; n(A∪B) = n(A) + n(B) − n(A∩B) is worked out.
 *
 * PARAMS (all optional — every one has a built-in default)
 *   mode       string  'central' | 'correlation' | 'normal' | 'venn'                             'central'
 *   challenge  string  Challenge sentence                                                         (generated)
 *   label      string  Variable name / axis label (any language)                                 'Marks'
 * central (ungrouped):
 *   data       array   numbers                                                                    [4,6,6,7,9,10,12]
 *   range      array   [min, max] of the axis                                                     [0, 20]
 *   step       number  snapping step                                                              1
 *   targets    object  any of {mean, median, mode, q1, q3, n} the data must reach                 {mean: 9}
 * central (grouped):
 *   freq       array   class frequencies (turns on histogram)                                     —
 *   classStart number  lower limit of the first class                                            0
 *   width      number  class width h                                                              10
 *   maxF       number  largest frequency on the axis                                              20
 *   targets    object  {mean|median|mode: value, tol} or {modalClass: index (0-based)}             {mode: 34, tol: 0.5}
 * correlation:
 *   points     array   [[x, y], …]                                                                8 points
 *   xRange, yRange     [min, max]                                                                 [0,10], [0,10]
 *   xLabel, yLabel     axis names                                                                 'X', 'Y'
 *   targets    object  {pearson: [min, max]} and/or {spearman: [min, max]}                        {pearson: [0.9, 1]}
 * normal:
 *   mu, sigma  numbers  starting mean and standard deviation                                      50, 10
 *   muRange, sigmaRange  [min, max] for the sliders (omit to lock)                                 locked
 *   a, b       numbers  starting handle positions (x units)                                       45, 55
 *   step       number  handle snapping step (x units)                                             0.5
 *   tail       string  'between' | 'left' (X < b) | 'right' (X > a)                               'between'
 *   targets    object  {area, tol}                                                                {area: 0.95, tol: 0.005}
 * venn:
 *   sets       number | object   2 or 3, or {A:[elements], B:[…], C:[…]} (counts worked out)      2
 *   universe   array   elements of U (with object `sets`)                                         —
 *   counts     object  region counts by letters: {A:12, B:9, AB:5, '':4} ('' = outside all)      2-set default
 *   names      array   display names of the sets, e.g. ['Cricket','Football'] or Hindi           ['A','B','C']
 *   tasks      array   set expressions to shade, using A B C U ∪ ∩ ′ − ( )                        ['A∪B', 'A∩B′', '(A∪B)′']
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fin = (v, d) => v !== null && v !== '' && isFinite(+v) ? +v : d;
  const rd = (v, k = 2) => { if (!isFinite(v)) return '—'; const f = Math.pow(10, k); const r = Math.round(v * f) / f; return String(Object.is(r, -0) ? 0 : r).replace('-', '−'); };
  const CSS = `
.lb-statlab-w{font-size:13px;color:#1b1f3a;user-select:none;-webkit-user-select:none;line-height:1.3}
.lb-statlab-w button{font-family:inherit;cursor:pointer;border:none}
.lb-statlab-ch{font-weight:800;font-size:13.5px;line-height:1.3;margin-bottom:6px}
.lb-statlab-g{background:#f7f8ff;border-radius:16px}
.lb-statlab-g svg{display:block;width:100%;height:auto;touch-action:none}
.lb-statlab-ax{font-size:10px;font-weight:700;fill:#6b7090}
.lb-statlab-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:6px}
.lb-statlab-cards div{border-radius:10px;padding:4px 2px;text-align:center;font-weight:900;font-size:14px;line-height:1.15;background:#f6f7ff}
.lb-statlab-cards small{display:block;font-size:9.5px;color:#6b7090;font-weight:800}
.lb-statlab-cards .mn{background:#f1ecff;color:#7044e0}.lb-statlab-cards .md{background:#e3fbf3;color:#0f7a5c}.lb-statlab-cards .mo{background:#fff6dc;color:#a77400}.lb-statlab-cards .hit{box-shadow:inset 0 0 0 2px #2ed3a5}
.lb-statlab-f{background:#fff8e1;border-radius:12px;padding:5px 9px;font-weight:700;font-size:12px;margin-top:6px;line-height:1.45}
.lb-statlab-f b{color:#7044e0}
.lb-statlab-row{display:flex;gap:6px;margin-top:6px;align-items:center}
.lb-statlab-btn{min-height:40px;border-radius:12px;background:#8b5cf6;color:#fff;font-weight:800;font-size:13.5px;padding:0 12px}
.lb-statlab-btn.alt{background:#eef0fb;color:#1b1f3a}
.lb-statlab-sl{display:flex;align-items:center;gap:8px;margin-top:4px;font-weight:800;font-size:12.5px}
.lb-statlab-sl input{flex:1;height:30px;accent-color:#8b5cf6;min-width:0}
.lb-statlab-sl b{min-width:44px;text-align:right;color:#7044e0;font-size:14px}
.lb-statlab-msg{margin-top:5px;font-weight:700;font-size:12.5px;line-height:1.35;min-height:17px}
.lb-statlab-msg.ok{color:#0f7a5c}.lb-statlab-msg.bad{color:#d03c3c}
.lb-statlab-task{display:flex;align-items:center;gap:6px;margin-bottom:5px}
.lb-statlab-task .ex{flex:1;font-weight:900;font-size:18px;color:#7044e0}
.lb-statlab-task .pg{background:#f1ecff;color:#7044e0;border-radius:99px;padding:3px 9px;font-weight:800;font-size:12px}
.lb-statlab-g .rg{cursor:pointer;transition:fill .15s}
`;
  /* ---------- shared maths ---------- */
  function quant(sorted, q) { const n = sorted.length; if (!n) return NaN; const pos = (n + 1) * q; if (pos <= 1) return sorted[0]; if (pos >= n) return sorted[n - 1]; const lo = Math.floor(pos); return sorted[lo - 1] + (pos - lo) * (sorted[lo] - sorted[lo - 1]); }
  function modes(arr) { const c = new Map(); arr.forEach(v => c.set(v, (c.get(v) || 0) + 1)); let mx = 0; c.forEach(n => mx = Math.max(mx, n)); if (mx <= 1) return []; return [...c.entries()].filter(e => e[1] === mx).map(e => e[0]).sort((a, b) => a - b); }
  function ranks(a) { const idx = a.map((v, i) => [v, i]).sort((x, y) => x[0] - y[0]); const r = new Array(a.length); const ties = []; let i = 0; while (i < idx.length) { let j = i; while (j + 1 < idx.length && idx[j + 1][0] === idx[i][0]) j++; const avg = (i + j + 2) / 2; for (let k = i; k <= j; k++) r[idx[k][1]] = avg; if (j > i) ties.push(j - i + 1); i = j + 1; } return { r, ties }; }
  function erf(x) { const s = x < 0 ? -1 : 1; x = Math.abs(x); const t = 1 / (1 + 0.3275911 * x); const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
  const Phi = z => 0.5 * (1 + erf(z / Math.SQRT2));
  function svgPt(svg, ev) { const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY; const m = svg.getScreenCTM(); return m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 }; }
  function niceStep(span, max) { return [0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000].find(s => span / s <= max) || 1000; }

  Labs.register('statlab', {
    title: 'Statistics lab',
    subjects: ['maths', 'economics'],
    render(host, p, api) {
      p = p && typeof p === 'object' ? p : {};
      const mode = ['central', 'correlation', 'normal', 'venn'].includes(p.mode) ? p.mode : 'central';
      const cleanups = []; let won = false;
      const win = m => { if (won) return; won = true; api.sfx && api.sfx('correct'); api.win(m); };
      host.innerHTML = `<div class="lb-statlab-w"><style>${CSS}</style><div class="lb-statlab-ch"></div><div class="lb-statlab-body"></div></div>`;
      const W = host.firstElementChild, body = W.querySelector('.lb-statlab-body');
      const setCh = t => { W.querySelector('.lb-statlab-ch').textContent = '🎯 Challenge: ' + t; };
      const label = p.label || 'Marks';
      function dragOn(svg, down, move, up) {
        let active = false;
        const d = e => { const r = down(svgPt(svg, e), e); if (r) { active = true; try { svg.setPointerCapture(e.pointerId); } catch (x) { } e.preventDefault(); } };
        const m = e => { if (active) move(svgPt(svg, e), e); };
        const u = () => { if (active) { active = false; up && up(); } };
        svg.addEventListener('pointerdown', d); svg.addEventListener('pointermove', m); svg.addEventListener('pointerup', u); svg.addEventListener('pointercancel', u);
      }

      /* ───────────── CENTRAL (ungrouped) ───────────── */
      function central() {
        const rg = Array.isArray(p.range) && p.range.length === 2 && +p.range[1] > +p.range[0] ? [+p.range[0], +p.range[1]] : [0, 20];
        const step = fin(p.step, 1) > 0 ? fin(p.step, 1) : 1;
        const snap = v => Math.min(rg[1], Math.max(rg[0], Math.round((v - rg[0]) / step) * step + rg[0]));
        let data = (Array.isArray(p.data) ? p.data : [4, 6, 6, 7, 9, 10, 12]).map(Number).filter(isFinite).map(snap).slice(0, 30);
        if (!data.length) data = [4, 6, 6, 7, 9, 10, 12];
        const tg = p.targets && typeof p.targets === 'object' ? p.targets : (p.data ? {} : { mean: 9 });
        const keys = ['mean', 'median', 'mode', 'q1', 'q3', 'n'].filter(k => tg[k] != null && isFinite(+tg[k]));
        const NM = { mean: 'mean', median: 'median', mode: 'mode', q1: 'Q1', q3: 'Q3', n: 'n' };
        setCh(p.challenge || (keys.length ? `Drag the dots so that ${keys.map(k => `the ${NM[k]} is ${tg[k]}`).join(' and ')}` : 'Drag the dots and watch the mean, median and mode change'));
        const VW = 360, VH = 178, L = 16, R = 16, AX = 118, GW = VW - L - R;
        const X = v => L + (v - rg[0]) / (rg[1] - rg[0]) * GW, V = x => rg[0] + (x - L) / GW * (rg[1] - rg[0]);
        body.innerHTML = `<div class="lb-statlab-g"><svg viewBox="0 0 ${VW} ${VH}"></svg></div><div class="lb-statlab-cards"></div>
<div class="lb-statlab-row"><button class="lb-statlab-btn alt ad" style="flex:1">＋ Add dot</button><button class="lb-statlab-btn alt rm" style="flex:1">－ Remove dot</button></div><div class="lb-statlab-msg"></div>`;
        const svg = body.querySelector('svg'), cards = body.querySelector('.lb-statlab-cards'), msg = body.querySelector('.lb-statlab-msg');
        let drag = -1, selI = data.length - 1, touched = false;
        const stats = () => { const s = data.slice().sort((a, b) => a - b), n = s.length; return { n, s, mean: s.reduce((a, b) => a + b, 0) / n, median: quant(s, 0.5), q1: quant(s, 0.25), q3: quant(s, 0.75), modes: modes(s) }; };
        function draw() {
          const st = stats(), ts = niceStep(rg[1] - rg[0], 10);
          let s = '';
          for (let v = Math.ceil(rg[0] / ts) * ts; v <= rg[1] + 1e-9; v += ts) s += `<line x1="${X(v)}" x2="${X(v)}" y1="${AX}" y2="${AX + 5}" stroke="#1b1f3a"/><text class="lb-statlab-ax" x="${X(v)}" y="${AX + 16}" text-anchor="middle">${rd(v)}</text>`;
          s += `<line x1="${L}" x2="${L + GW}" y1="${AX}" y2="${AX}" stroke="#1b1f3a" stroke-width="1.5"/><text class="lb-statlab-ax" x="${VW - 4}" y="${AX + 28}" text-anchor="end">${esc(label)} →</text>`;
          /* box plot strip */
          const by = AX + 36; s += `<line x1="${X(st.s[0])}" x2="${X(st.s[st.n - 1])}" y1="${by + 7}" y2="${by + 7}" stroke="#6b7090" stroke-width="1.5"/><rect x="${X(st.q1)}" y="${by}" width="${Math.max(1, X(st.q3) - X(st.q1))}" height="14" rx="3" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/><line x1="${X(st.median)}" x2="${X(st.median)}" y1="${by}" y2="${by + 14}" stroke="#0f9a72" stroke-width="3"/>`;
          s += `<text class="lb-statlab-ax" x="${X(st.q1)}" y="${by - 2}" text-anchor="middle">Q1</text><text class="lb-statlab-ax" x="${X(st.q3)}" y="${by - 2}" text-anchor="middle">Q3</text>`;
          /* dots */
          const cnt = {}; const order = data.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
          const dr = Math.min(8, GW / ((rg[1] - rg[0]) / step + 1) / 2 - 0.5);
          order.forEach(([v, i]) => { const k = cnt[v] = (cnt[v] || 0) + 1; const cy = AX - dr - 1 - (k - 1) * (dr * 2 + 1); data[i]._y = cy; s += `<circle cx="${X(v)}" cy="${Math.max(dr + 1, cy)}" r="${dr}" fill="${i === drag ? '#ff6b6b' : i === selI ? '#3b82f6' : '#8b5cf6'}" stroke="#fff" stroke-width="1.5"/>`; });
          s += `<path d="M${X(st.mean)} ${AX + 2} l-6 10 h12z" fill="#7044e0"/><text x="${X(st.mean)}" y="${AX + 2}" font-size="9" font-weight="900" fill="#7044e0" text-anchor="middle" dy="-${0}"></text>`;
          s += `<text x="8" y="13" font-size="10" font-weight="800" fill="#6b7090">▲ mean · ┃ median · box = Q1 to Q3 · drag a dot</text>`;
          svg.innerHTML = s;
          const hit = k => keys.includes(k) && ok(k, st);
          cards.innerHTML = `<div class="mn ${hit('mean') ? 'hit' : ''}">${rd(st.mean)}<small>mean x̄</small></div><div class="md ${hit('median') ? 'hit' : ''}">${rd(st.median)}<small>median</small></div><div class="mo ${hit('mode') ? 'hit' : ''}">${st.modes.length ? st.modes.map(m => rd(m)).join(', ') : '—'}<small>mode${st.modes.length > 1 ? 's' : ''}</small></div><div class="${hit('n') ? 'hit' : ''}">${st.n}<small>n · Q1 ${rd(st.q1)} · Q3 ${rd(st.q3)}</small></div>`;
          if (drag < 0) {
            msg.className = 'lb-statlab-msg';
            msg.textContent = `x̄ = Σx ÷ n = ${rd(st.s.reduce((a, b) => a + b, 0))} ÷ ${st.n} = ${rd(st.mean)}. Median = size of (n+1)/2 = ${rd((st.n + 1) / 2, 1)}th item = ${rd(st.median)}.`;
            if (touched && keys.length && keys.every(k => ok(k, st))) win(`${keys.map(k => `${NM[k]} = ${k === 'mode' ? rd(st.modes[0]) : k === 'n' ? st.n : rd(st[k])}`).join(', ')} with data ${st.s.map(v => rd(v)).join(', ')}`);
          }
        }
        function ok(k, st) { const t = +tg[k]; if (k === 'mode') return st.modes.length === 1 && Math.abs(st.modes[0] - t) < 1e-9; if (k === 'n') return st.n === t; return Math.abs(st[k] - t) < (fin(tg.tol, 1e-9) || 1e-9); }
        dragOn(svg, pt => { let best = -1, bd = 1e9; data.forEach((v, i) => { const d = Math.hypot(X(v) - pt.x, (data[i]._y || AX) - pt.y); if (d < bd) { bd = d; best = i; } }); if (best < 0 || bd > 24) return false; drag = best; selI = best; draw(); return true; },
          pt => { const nv = snap(V(pt.x)); if (nv !== data[drag]) { data[drag] = nv; touched = true; api.sfx && api.sfx('tap'); } draw(); }, () => { drag = -1; draw(); });
        body.querySelector('.ad').addEventListener('click', () => { if (data.length >= 30) return; data.push(snap(stats().median)); selI = data.length - 1; touched = true; draw(); });
        body.querySelector('.rm').addEventListener('click', () => { if (data.length <= 2) return; data.splice(selI >= 0 && selI < data.length ? selI : data.length - 1, 1); selI = data.length - 1; touched = true; draw(); });
        draw();
      }

      /* ───────────── CENTRAL (grouped histogram) ───────────── */
      function grouped() {
        let f = p.freq.map(v => Math.max(0, Math.round(fin(v, 0)))).slice(0, 10);
        const c0 = fin(p.classStart, 0), h = fin(p.width, 10) > 0 ? fin(p.width, 10) : 10, maxF = Math.max(fin(p.maxF, 0), ...f.map(v => v + 4), 10);
        const k = f.length, lo = i => c0 + i * h, mid = i => c0 + i * h + h / 2;
        const tg = p.targets && typeof p.targets === 'object' ? p.targets : {};
        const tk = ['mean', 'median', 'mode'].filter(x => tg[x] != null && isFinite(+tg[x])), tol = fin(tg.tol, 0.5);
        const mc = tg.modalClass != null && isFinite(+tg.modalClass) ? +tg.modalClass : null;
        setCh(p.challenge || (tk.length ? `Drag the bars so that the ${tk.map(x => `${x} is ${tg[x]} (±${tol})`).join(' and ')}` : mc != null ? `Make ${lo(mc)}–${lo(mc + 1)} the modal class` : 'Drag the bars and watch the mean, median and mode move'));
        const VW = 360, VH = 190, L = 30, R = 10, T = 16, B = 30, GW = VW - L - R, GH = VH - T - B;
        const X = v => L + (v - c0) / (k * h) * GW, Y = n => T + GH - n / maxF * GH;
        body.innerHTML = `<div class="lb-statlab-g"><svg viewBox="0 0 ${VW} ${VH}"></svg></div><div class="lb-statlab-cards"></div><div class="lb-statlab-f"></div><div class="lb-statlab-msg"></div>`;
        const svg = body.querySelector('svg'), cards = body.querySelector('.lb-statlab-cards'), fx = body.querySelector('.lb-statlab-f'), msg = body.querySelector('.lb-statlab-msg');
        let drag = -1, touched = false;
        function S() {
          const N = f.reduce((a, b) => a + b, 0); if (!N) return { N };
          const mean = f.reduce((a, v, i) => a + v * mid(i), 0) / N;
          let cf = 0, mi = 0; for (let i = 0; i < k; i++) { if (cf + f[i] >= N / 2) { mi = i; break; } cf += f[i]; }
          const median = lo(mi) + (N / 2 - cf) / f[mi] * h;
          const mx = Math.max(...f), mcs = f.map((v, i) => v === mx ? i : -1).filter(i => i >= 0), mo = mcs[0];
          const f0 = mo > 0 ? f[mo - 1] : 0, f2 = mo < k - 1 ? f[mo + 1] : 0, den = 2 * f[mo] - f0 - f2;
          const mode = den ? lo(mo) + (f[mo] - f0) / den * h : NaN;
          return { N, mean, mi, cf, median, mo, mcs, f0, f2, mode };
        }
        function draw() {
          const st = S(); let s = '';
          const ys = niceStep(maxF, 5); for (let n = 0; n <= maxF; n += ys) s += `<line x1="${L}" x2="${L + GW}" y1="${Y(n)}" y2="${Y(n)}" stroke="#e3e6f7"/><text class="lb-statlab-ax" x="${L - 4}" y="${Y(n) + 3}" text-anchor="end">${n}</text>`;
          f.forEach((v, i) => { const x = X(lo(i)), w = X(lo(i + 1)) - x; const isM = st.N && st.mcs.includes(i); s += `<rect x="${x + 0.5}" y="${Y(v)}" width="${w - 1}" height="${T + GH - Y(v)}" fill="${i === drag ? '#ff6b6b' : isM ? '#ffc93c' : '#8b5cf6'}" opacity="${isM || i === drag ? 1 : .8}"/><rect x="${x + 4}" y="${Y(v) - 5}" width="${w - 8}" height="7" rx="3.5" fill="#1b1f3a" opacity=".55"/><text x="${x + w / 2}" y="${T + GH - Y(v) > 22 ? Y(v) + 16 : Y(v) - 8}" text-anchor="middle" font-size="10.5" font-weight="900" fill="${T + GH - Y(v) > 22 ? '#fff' : '#1b1f3a'}">${v}</text>`; });
          for (let i = 0; i <= k; i++) s += `<text class="lb-statlab-ax" x="${X(lo(i))}" y="${T + GH + 12}" text-anchor="middle">${rd(lo(i))}</text>`;
          s += `<line x1="${L}" x2="${L + GW}" y1="${T + GH}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/><text class="lb-statlab-ax" x="${VW - 4}" y="${VH - 4}" text-anchor="end">${esc(label)} (class intervals) →</text><text class="lb-statlab-ax" x="4" y="10">f ↑</text>`;
          if (st.N) {
            const mk = (v, c, t, y) => isFinite(v) ? `<line x1="${X(v)}" x2="${X(v)}" y1="${T}" y2="${T + GH}" stroke="${c}" stroke-width="2" stroke-dasharray="4 3"/><text x="${X(v)}" y="${y}" text-anchor="middle" font-size="9.5" font-weight="900" fill="${c}" stroke="#f7f8ff" stroke-width="3" paint-order="stroke">${t}</text>` : '';
            s += mk(st.mean, '#7044e0', 'x̄', T + 8) + mk(st.median, '#0f9a72', 'Me', T + 18) + mk(st.mode, '#c2410c', 'Mo', T + 28);
          }
          svg.innerHTML = s;
          if (!st.N) { cards.innerHTML = ''; fx.textContent = 'Every frequency is 0 — drag a bar up.'; return; }
          const hit = x => tk.includes(x) && Math.abs(st[x] - tg[x]) <= tol;
          cards.innerHTML = `<div class="mn ${hit('mean') ? 'hit' : ''}">${rd(st.mean)}<small>mean</small></div><div class="md ${hit('median') ? 'hit' : ''}">${rd(st.median)}<small>median</small></div><div class="mo ${hit('mode') ? 'hit' : ''}">${rd(st.mode)}<small>mode</small></div><div>${st.N}<small>N = Σf</small></div>`;
          fx.innerHTML = `Mean = Σfm ÷ N = ${rd(f.reduce((a, v, i) => a + v * mid(i), 0))} ÷ ${st.N} = <b>${rd(st.mean)}</b><br>Median = L + ((N/2 − c.f.) ÷ f) × h = ${rd(lo(st.mi))} + ((${rd(st.N / 2)} − ${st.cf}) ÷ ${f[st.mi]}) × ${h} = <b>${rd(st.median)}</b><br>Mode = L + (f₁ − f₀) ÷ (2f₁ − f₀ − f₂) × h = ${rd(lo(st.mo))} + (${f[st.mo]} − ${st.f0}) ÷ (${2 * f[st.mo]} − ${st.f0} − ${st.f2}) × ${h} = <b>${rd(st.mode)}</b>${st.mcs.length > 1 ? ' (more than one modal class!)' : ''}`;
          if (drag < 0 && touched) {
            const good = (tk.length || mc != null) && tk.every(hit) && (mc == null || (st.mcs.length === 1 && st.mcs[0] === mc));
            msg.className = 'lb-statlab-msg' + (good ? ' ok' : ''); msg.textContent = good ? '🎯 Target reached!' : 'Taller bars pull the mean towards them; the mode sits in the tallest class.';
            if (good) win(`${tk.map(x => `${x} = ${rd(st[x])}`).join(', ')}${mc != null ? `${tk.length ? ', ' : ''}modal class ${lo(mc)}–${lo(mc + 1)}` : ''} with frequencies ${f.join(', ')}`);
          } else if (!touched) msg.textContent = 'Drag the top of a bar up or down to change its frequency.';
        }
        dragOn(svg, pt => { for (let i = 0; i < k; i++) if (pt.x >= X(lo(i)) && pt.x < X(lo(i + 1))) { drag = i; return true; } return false; },
          pt => { const n = Math.max(0, Math.min(maxF, Math.round((T + GH - pt.y) / GH * maxF))); if (n !== f[drag]) { f[drag] = n; touched = true; api.sfx && api.sfx('tap'); } draw(); }, () => { drag = -1; draw(); });
        draw();
      }

      /* ───────────── CORRELATION ───────────── */
      function correlation() {
        const xr = Array.isArray(p.xRange) && +p.xRange[1] > +p.xRange[0] ? p.xRange.map(Number) : [0, 10], yr = Array.isArray(p.yRange) && +p.yRange[1] > +p.yRange[0] ? p.yRange.map(Number) : [0, 10];
        const step = fin(p.step, 1) > 0 ? fin(p.step, 1) : 1;
        const sx = v => Math.min(xr[1], Math.max(xr[0], Math.round((v - xr[0]) / step) * step + xr[0])), sy = v => Math.min(yr[1], Math.max(yr[0], Math.round((v - yr[0]) / step) * step + yr[0]));
        let pts = (Array.isArray(p.points) ? p.points : [[1, 3], [2, 6], [3, 2], [4, 7], [5, 4], [6, 8], [7, 3], [8, 6]]).filter(q => Array.isArray(q) && isFinite(+q[0]) && isFinite(+q[1])).map(q => [sx(+q[0]), sy(+q[1])]).slice(0, 15);
        if (pts.length < 3) pts = [[1, 3], [2, 6], [3, 2], [4, 7], [5, 4], [6, 8], [7, 3], [8, 6]];
        const tg = p.targets && typeof p.targets === 'object' ? p.targets : { pearson: [0.9, 1] };
        const rngOf = v => Array.isArray(v) && v.length === 2 ? [+v[0], +v[1]] : null, tP = rngOf(tg.pearson), tS = rngOf(tg.spearman);
        const desc = (nm, r) => r[1] >= 1 && r[0] > 0 ? `${nm} ≥ ${r[0]}` : r[0] <= -1 && r[1] < 0 ? `${nm} ≤ ${r[1]}` : `${r[0]} ≤ ${nm} ≤ ${r[1]}`;
        setCh(p.challenge || `Drag the points to make ${[tP && desc('r', tP), tS && desc('rₛ', tS)].filter(Boolean).join(' and ') || 'a strong correlation'}`);
        const xl = p.xLabel || 'X', yl = p.yLabel || 'Y';
        const VW = 360, VH = 184, L = 30, R = 10, T = 10, B = 26, GW = VW - L - R, GH = VH - T - B;
        const X = v => L + (v - xr[0]) / (xr[1] - xr[0]) * GW, Y = v => T + GH - (v - yr[0]) / (yr[1] - yr[0]) * GH;
        body.innerHTML = `<div class="lb-statlab-g"><svg viewBox="0 0 ${VW} ${VH}"></svg></div><div class="lb-statlab-cards" style="grid-template-columns:1fr 1fr"></div><div class="lb-statlab-f"></div>
<div class="lb-statlab-row"><button class="lb-statlab-btn alt ad" style="flex:1">＋ Add point</button><button class="lb-statlab-btn alt rm" style="flex:1">－ Remove point</button></div><div class="lb-statlab-msg"></div>`;
        const svg = body.querySelector('svg'), cards = body.querySelector('.lb-statlab-cards'), fx = body.querySelector('.lb-statlab-f'), msg = body.querySelector('.lb-statlab-msg');
        let drag = -1, sel = pts.length - 1, touched = false;
        function S() {
          const n = pts.length, mx = pts.reduce((a, q) => a + q[0], 0) / n, my = pts.reduce((a, q) => a + q[1], 0) / n;
          let sxy = 0, sxx = 0, syy = 0; pts.forEach(q => { const dx = q[0] - mx, dy = q[1] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy; });
          const r = sxx && syy ? sxy / Math.sqrt(sxx * syy) : NaN;
          const RX = ranks(pts.map(q => q[0])), RY = ranks(pts.map(q => q[1]));
          const D2 = RX.r.reduce((a, v, i) => a + (v - RY.r[i]) ** 2, 0), cf = [...RX.ties, ...RY.ties].reduce((a, m) => a + (m ** 3 - m) / 12, 0);
          const rs = 1 - 6 * (D2 + cf) / (n ** 3 - n);
          return { n, mx, my, sxy, sxx, syy, r, D2, cf, rs, constant: !sxx || !syy };
        }
        const word = r => !isFinite(r) ? 'undefined' : Math.abs(r) === 1 ? `perfect ${r > 0 ? 'positive' : 'negative'}` : Math.abs(r) < 0.05 ? 'no (≈ zero)' : `${Math.abs(r) >= 0.75 ? 'high' : Math.abs(r) >= 0.4 ? 'moderate' : 'low'} ${r > 0 ? 'positive' : 'negative'}`;
        function draw() {
          const st = S(); let s = '';
          const xs = niceStep(xr[1] - xr[0], 10), ys = niceStep(yr[1] - yr[0], 6);
          for (let v = Math.ceil(xr[0] / xs) * xs; v <= xr[1] + 1e-9; v += xs) s += `<line x1="${X(v)}" x2="${X(v)}" y1="${T}" y2="${T + GH}" stroke="#e3e6f7"/><text class="lb-statlab-ax" x="${X(v)}" y="${T + GH + 12}" text-anchor="middle">${rd(v)}</text>`;
          for (let v = Math.ceil(yr[0] / ys) * ys; v <= yr[1] + 1e-9; v += ys) s += `<line x1="${L}" x2="${L + GW}" y1="${Y(v)}" y2="${Y(v)}" stroke="#e3e6f7"/><text class="lb-statlab-ax" x="${L - 4}" y="${Y(v) + 3}" text-anchor="end">${rd(v)}</text>`;
          s += `<line x1="${L}" x2="${L}" y1="${T}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${L}" x2="${L + GW}" y1="${T + GH}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          s += `<text class="lb-statlab-ax" x="${VW - 4}" y="${VH - 3}" text-anchor="end">${esc(xl)} →</text><text class="lb-statlab-ax" x="${L + 4}" y="${T + 9}">↑ ${esc(yl)}</text>`;
          s += `<line x1="${X(st.mx)}" x2="${X(st.mx)}" y1="${T}" y2="${T + GH}" stroke="#ffc93c" stroke-dasharray="4 3"/><line x1="${L}" x2="${L + GW}" y1="${Y(st.my)}" y2="${Y(st.my)}" stroke="#ffc93c" stroke-dasharray="4 3"/>`;
          pts.forEach((q, i) => { const dx = q[0] - st.mx, dy = q[1] - st.my, c = dx * dy > 0 ? '#2ed3a5' : dx * dy < 0 ? '#ff6b6b' : '#6b7090'; s += `<circle cx="${X(q[0])}" cy="${Y(q[1])}" r="${i === drag ? 10 : 8}" fill="${c}" stroke="${i === sel ? '#1b1f3a' : '#fff'}" stroke-width="2"/>`; });
          svg.innerHTML = s;
          const inR = (v, r) => r && isFinite(v) && v >= r[0] - 1e-9 && v <= r[1] + 1e-9;
          cards.innerHTML = `<div class="mn ${inR(st.r, tP) ? 'hit' : ''}">r = ${rd(st.r, 4)}<small>Karl Pearson · ${word(st.r)}</small></div><div class="md ${inR(st.rs, tS) ? 'hit' : ''}">rₛ = ${rd(st.rs, 4)}<small>Spearman rank · ${word(st.rs)}</small></div>`;
          fx.innerHTML = `r = Σdxdy ÷ √(Σdx² · Σdy²) = ${rd(st.sxy)} ÷ √(${rd(st.sxx)} × ${rd(st.syy)}) = <b>${rd(st.r, 4)}</b><br>rₛ = 1 − 6(ΣD²${st.cf ? ' + Σ(m³−m)/12' : ''}) ÷ (n³ − n) = 1 − 6(${rd(st.D2)}${st.cf ? ' + ' + rd(st.cf) : ''}) ÷ ${st.n ** 3 - st.n} = <b>${rd(st.rs, 4)}</b>`;
          if (drag < 0) {
            const good = (tP || tS) && (!tP || inR(st.r, tP)) && (!tS || inR(st.rs, tS));
            msg.className = 'lb-statlab-msg' + (good ? ' ok' : '');
            msg.textContent = st.constant ? 'All X (or all Y) values are equal — r cannot be computed.' : good ? '🎯 Target reached!' : 'Green points (dx·dy > 0) push r up; red points (dx·dy < 0) pull it down.';
            if (good && touched) win(`r = ${rd(st.r, 4)} and rₛ = ${rd(st.rs, 4)} with ${st.n} points`);
          }
        }
        dragOn(svg, pt => { let b = -1, bd = 1e9; pts.forEach((q, i) => { const d = Math.hypot(X(q[0]) - pt.x, Y(q[1]) - pt.y); if (d < bd) { bd = d; b = i; } }); if (bd > 26) return false; drag = sel = b; draw(); return true; },
          pt => { const nx = sx(xr[0] + (pt.x - L) / GW * (xr[1] - xr[0])), ny = sy(yr[0] + (T + GH - pt.y) / GH * (yr[1] - yr[0])); if (nx !== pts[drag][0] || ny !== pts[drag][1]) { pts[drag] = [nx, ny]; touched = true; } draw(); }, () => { drag = -1; draw(); });
        body.querySelector('.ad').addEventListener('click', () => { if (pts.length >= 15) return; pts.push([sx((xr[0] + xr[1]) / 2), sy((yr[0] + yr[1]) / 2)]); sel = pts.length - 1; touched = true; draw(); });
        body.querySelector('.rm').addEventListener('click', () => { if (pts.length <= 3) return; pts.splice(sel >= 0 && sel < pts.length ? sel : pts.length - 1, 1); sel = pts.length - 1; touched = true; draw(); });
        draw();
      }

      /* ───────────── NORMAL ───────────── */
      function normal() {
        let mu = fin(p.mu, 50), sg = Math.max(1e-6, fin(p.sigma, 10));
        const muR = Array.isArray(p.muRange) && p.muRange.length === 2 ? p.muRange.map(Number) : null, sgR = Array.isArray(p.sigmaRange) && p.sigmaRange.length === 2 ? p.sigmaRange.map(Number) : null;
        const sgMax = sgR ? Math.max(sgR[1], sg) : sg;
        const lo = (muR ? Math.min(muR[0], mu) : mu) - 3.3 * sgMax, hi = (muR ? Math.max(muR[1], mu) : mu) + 3.3 * sgMax;
        const step = fin(p.step, 0.5) > 0 ? fin(p.step, 0.5) : 0.5, snap = v => Math.min(hi, Math.max(lo, Math.round(v / step) * step));
        let a = snap(fin(p.a, mu - sg / 2)), b = snap(fin(p.b, mu + sg / 2));
        const tail = ['left', 'right'].includes(p.tail) ? p.tail : 'between';
        const tg = p.targets && typeof p.targets === 'object' ? p.targets : { area: 0.95, tol: 0.005 };
        const tA = tg.area != null && isFinite(+tg.area) ? +tg.area : null, tol = fin(tg.tol, 0.005);
        const sym = (tail === 'left' ? 'P(X < b)' : tail === 'right' ? 'P(X > a)' : 'P(a < X < b)');
        setCh(p.challenge || (tA != null ? `Drag the handle${tail === 'between' ? 's' : ''} so the shaded area ${sym} = ${tA} (±${tol})` : 'Drag the handles and watch the shaded probability'));
        const VW = 360, VH = 190, L = 10, R = 10, T = 16, B = 32, GW = VW - L - R, GH = VH - T - B;
        const X = v => L + (v - lo) / (hi - lo) * GW, V = x => lo + (x - L) / GW * (hi - lo);
        body.innerHTML = `<div class="lb-statlab-g"><svg viewBox="0 0 ${VW} ${VH}"></svg></div>
${muR ? `<div class="lb-statlab-sl"><span>Mean μ</span><input class="mu" type="range" min="${muR[0]}" max="${muR[1]}" step="${step}" value="${mu}"><b class="muv"></b></div>` : ''}
${sgR ? `<div class="lb-statlab-sl"><span>SD σ</span><input class="sg" type="range" min="${sgR[0]}" max="${sgR[1]}" step="${step}" value="${sg}"><b class="sgv"></b></div>` : ''}
<div class="lb-statlab-cards" style="grid-template-columns:1.3fr 1fr 1fr"></div><div class="lb-statlab-f"></div><div class="lb-statlab-msg"></div>`;
        const svg = body.querySelector('svg'), cards = body.querySelector('.lb-statlab-cards'), fx = body.querySelector('.lb-statlab-f'), msg = body.querySelector('.lb-statlab-msg');
        let drag = null, touched = false;
        const pdf = x => Math.exp(-0.5 * ((x - mu) / sg) ** 2) / (sg * Math.sqrt(2 * Math.PI));
        function draw() {
          const peak = 1 / (Math.min(sg, sgR ? sgR[0] : sg) * Math.sqrt(2 * Math.PI)), Y = d => T + GH - d / peak * GH * 0.95;
          const za = (a - mu) / sg, zb = (b - mu) / sg;
          const area = tail === 'left' ? Phi(zb) : tail === 'right' ? 1 - Phi(za) : Phi(zb) - Phi(za);
          const x1 = tail === 'left' ? lo : a, x2 = tail === 'right' ? hi : b;
          let s = '', d = '', sh = '';
          for (let i = 0; i <= 160; i++) { const x = lo + (hi - lo) * i / 160; d += `${i ? 'L' : 'M'}${X(x).toFixed(1)} ${Y(pdf(x)).toFixed(1)}`; }
          if (x2 > x1) { sh = `M${X(x1)} ${T + GH}`; for (let i = 0; i <= 80; i++) { const x = x1 + (x2 - x1) * i / 80; sh += `L${X(x).toFixed(1)} ${Y(pdf(x)).toFixed(1)}`; } sh += `L${X(x2)} ${T + GH}Z`; }
          s += `<path d="${sh}" fill="#8b5cf6" opacity=".35"/><path d="${d}" fill="none" stroke="#7044e0" stroke-width="2.5"/>`;
          s += `<line x1="${L}" x2="${L + GW}" y1="${T + GH}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          if (X(mu + sg) - X(mu) >= 26) { for (let k = -3; k <= 3; k++) { const x = mu + k * sg; if (x < lo || x > hi) continue; s += `<line x1="${X(x)}" x2="${X(x)}" y1="${T + GH}" y2="${T + GH + 4}" stroke="#1b1f3a"/><text class="lb-statlab-ax" x="${X(x)}" y="${T + GH + 14}" text-anchor="middle">${rd(x)}</text><text class="lb-statlab-ax" x="${X(x)}" y="${T + GH + 25}" text-anchor="middle" style="fill:#a8aed0">${k ? (k > 0 ? '+' : '−') + Math.abs(k) + 'σ' : 'μ'}</text>`; } }
          else { const ts = niceStep(hi - lo, 9); for (let x = Math.ceil(lo / ts) * ts; x <= hi + 1e-9; x += ts) s += `<line x1="${X(x)}" x2="${X(x)}" y1="${T + GH}" y2="${T + GH + 4}" stroke="#1b1f3a"/><text class="lb-statlab-ax" x="${X(x)}" y="${T + GH + 14}" text-anchor="middle">${rd(x)}</text>`; s += `<path d="M${X(mu)} ${T + GH + 17} l-5 8 h10z" fill="#7044e0"/><text class="lb-statlab-ax" x="${X(mu) + 8}" y="${T + GH + 25}" style="fill:#7044e0">μ</text>`; }
          const hd = (v, nm, c) => `<g><line x1="${X(v)}" x2="${X(v)}" y1="${T + 12}" y2="${T + GH}" stroke="${c}" stroke-width="2.5"/><rect x="${X(v) - 25}" y="${T - 4}" width="50" height="18" rx="9" fill="${c}" stroke="#fff" stroke-width="1.5"/><text x="${X(v)}" y="${T + 9}" text-anchor="middle" font-size="10" font-weight="900" fill="#fff">${nm} = ${rd(v)}</text></g>`;
          if (tail !== 'left') s += hd(a, 'a', '#ff6b6b'); if (tail !== 'right') s += hd(b, 'b', '#3b82f6');
          s += `<text x="${X((x1 + x2) / 2)}" y="${T + GH - 8}" text-anchor="middle" font-size="12" font-weight="900" fill="#1b1f3a" stroke="#f7f8ff" stroke-width="3" paint-order="stroke">${(area * 100).toFixed(2)}%</text>`;
          svg.innerHTML = s;
          const ok = tA != null && Math.abs(area - tA) <= tol;
          cards.innerHTML = `<div class="mn ${ok ? 'hit' : ''}">${area.toFixed(4)}<small>${sym}</small></div>${tail !== 'left' ? `<div>${rd(za)}<small>z₁ = (a − μ)/σ</small></div>` : ''}${tail !== 'right' ? `<div>${rd(zb)}<small>z₂ = (b − μ)/σ</small></div>` : ''}`;
          fx.innerHTML = tail === 'left' ? `P(X < ${rd(b)}) = Φ(${rd(zb)}) = <b>${area.toFixed(4)}</b>` : tail === 'right' ? `P(X > ${rd(a)}) = 1 − Φ(${rd(za)}) = <b>${area.toFixed(4)}</b>` : `P(${rd(a)} < X < ${rd(b)}) = Φ(${rd(zb)}) − Φ(${rd(za)}) = ${Phi(zb).toFixed(4)} − ${Phi(za).toFixed(4)} = <b>${area.toFixed(4)}</b>`;
          const mv = body.querySelector('.muv'), sv = body.querySelector('.sgv'); if (mv) mv.textContent = rd(mu); if (sv) sv.textContent = rd(sg);
          if (!drag) {
            msg.className = 'lb-statlab-msg' + (ok ? ' ok' : '');
            msg.textContent = ok ? '🎯 Target area reached!' : `μ = ${rd(mu)}, σ = ${rd(sg)}. About 68.27% lies within μ ± σ, 95.45% within μ ± 2σ, 99.73% within μ ± 3σ.`;
            if (ok && touched) win(`${sym.replace('a', rd(a)).replace('b', rd(b))} = ${area.toFixed(4)} (z from ${tail === 'left' ? '−∞' : rd(za)} to ${tail === 'right' ? '∞' : rd(zb)})`);
          }
        }
        dragOn(svg, pt => { const da = tail !== 'left' ? Math.abs(X(a) - pt.x) : 1e9, db = tail !== 'right' ? Math.abs(X(b) - pt.x) : 1e9; if (Math.min(da, db) > 34) return false; drag = da <= db ? 'a' : 'b'; return true; },
          pt => { const v = snap(V(pt.x)); if (drag === 'a') { const nv = tail === 'between' ? Math.min(v, b) : v; if (nv !== a) { a = nv; touched = true; } } else { const nv = tail === 'between' ? Math.max(v, a) : v; if (nv !== b) { b = nv; touched = true; } } draw(); }, () => { drag = null; draw(); });
        body.addEventListener('input', e => { if (e.target.classList.contains('mu')) mu = +e.target.value; if (e.target.classList.contains('sg')) sg = Math.max(1e-6, +e.target.value); touched = true; draw(); });
        draw();
      }

      /* ───────────── VENN ───────────── */
      function venn() {
        let K = 2, counts = {}, elems = null;
        const LET = ['A', 'B', 'C'];
        const codeOf = keyStr => { let c = 0; String(keyStr).toUpperCase().split('').forEach(ch => { const i = LET.indexOf(ch); if (i >= 0) c |= 1 << i; }); return c; };
        if (p.sets && typeof p.sets === 'object' && !Array.isArray(p.sets)) {
          const S = LET.map(l => Array.isArray(p.sets[l]) ? p.sets[l].map(String) : null); K = S[2] ? 3 : 2;
          const all = new Set([...(Array.isArray(p.universe) ? p.universe.map(String) : []), ...S.slice(0, K).flat()]);
          elems = {}; all.forEach(e => { let c = 0; for (let i = 0; i < K; i++) if (S[i].includes(e)) c |= 1 << i; (elems[c] = elems[c] || []).push(e); });
          for (let c = 0; c < 1 << K; c++) counts[c] = (elems[c] || []).length;
        } else {
          K = +p.sets === 3 || (p.counts && Object.keys(p.counts).some(k => /c/i.test(k))) ? 3 : 2;
          const src = p.counts && typeof p.counts === 'object' ? p.counts : (K === 3 ? { A: 10, B: 8, C: 6, AB: 4, AC: 3, BC: 2, ABC: 1, '': 6 } : { A: 12, B: 9, AB: 5, '': 4 });
          for (let c = 0; c < 1 << K; c++) counts[c] = 0;
          Object.entries(src).forEach(([k, v]) => { const c = k === 'U' || k === 'none' || k === 'outside' ? 0 : codeOf(k); if (c < 1 << K) counts[c] = Math.max(0, Math.round(fin(v, 0))); });
        }
        const names = LET.slice(0, K).map((l, i) => Array.isArray(p.names) && p.names[i] != null ? String(p.names[i]) : l);
        const ALL = (1 << (1 << K)) - 1, setMask = i => { let m = 0; for (let c = 0; c < 1 << K; c++) if (c & (1 << i)) m |= 1 << c; return m; };
        /* tiny parser for set expressions */
        function parse(str) {
          const s = String(str).replace(/\s+/g, ''); let i = 0;
          const peek = () => s[i];
          const atom = () => {
            const ch = s[i];
            if (ch === '(') { i++; const v = expr(); if (s[i] !== ')') throw Error('bracket'); i++; return v; }
            if (ch === 'U' || ch === 'ξ') { i++; return ALL; }
            if (ch === 'φ' || ch === '∅' || ch === 'Φ') { i++; return 0; }
            for (let k = 0; k < K; k++) { const nm = names[k]; if (nm.length > 1 && s.startsWith(nm.replace(/\s+/g, ''), i)) { i += nm.replace(/\s+/g, '').length; return setMask(k); } }
            const k = LET.indexOf(ch); if (k >= 0 && k < K) { i++; return setMask(k); }
            throw Error('bad token ' + ch);
          };
          const post = () => { let v = atom(); while ("′'ᶜ’".includes(peek() || '#')) { i++; v = ALL & ~v; } return v; };
          const inter = () => { let v = post(); while (peek() === '∩' || peek() === '^') { i++; v &= post(); } return v; };
          const expr = () => { let v = inter(); for (;;) { const c = peek(); if (c === '∪' || c === '+') { i++; v |= inter(); } else if (c === '−' || c === '-' || c === '\\') { i++; v &= ~inter(); } else if (c === 'Δ') { i++; v ^= inter(); } else break; } return v & ALL; };
          const v = expr(); if (i !== s.length) throw Error('extra'); return v;
        }
        let tasks = (Array.isArray(p.tasks) && p.tasks.length ? p.tasks : (K === 3 ? ['A∩B∩C', 'A∪B∪C', 'A∩(B∪C)', '(A∪B)′∩C'] : ['A∪B', 'A∩B′', '(A∪B)′'])).map(t => { try { return { ex: String(t), m: parse(t) }; } catch (e) { return null; } }).filter(Boolean);
        if (!tasks.length) tasks = [{ ex: 'A∪B', m: setMask(0) | setMask(1) }];
        const show = ex => { let s = ex; LET.slice(0, K).forEach((l, i) => { if (names[i] !== l) s = s.split(l).join(names[i]); }); return s; };
        setCh(p.challenge || `Shade each set by tapping regions: ${tasks.map(t => show(t.ex)).join(', ')}`);
        const VW = 360, VH = K === 3 ? 228 : 214;
        const C = K === 3 ? [[145, 88, 66], [215, 88, 66], [180, 148, 66]] : [[140, 110, 82], [220, 110, 82]];
        const POS = K === 3 ? { 1: [108, 70], 2: [252, 70], 4: [180, 186], 3: [180, 62], 5: [138, 134], 6: [222, 134], 7: [180, 108], 0: [28, 214] } : { 1: [98, 112], 2: [262, 112], 3: [180, 112], 0: [26, 200] };
        const NPOS = K === 3 ? [[78, 24, 'end'], [282, 24, 'start'], [258, 214, 'start']] : [[86, 30, 'end'], [274, 30, 'start']];
        const COLS = ['#ff6b6b', '#3b82f6', '#2ed3a5'];
        const uid = 'vn' + Math.random().toString(36).slice(2, 7);
        let defs = C.map((c, i) => `<clipPath id="${uid}c${i}"><circle cx="${c[0]}" cy="${c[1]}" r="${c[2]}"/></clipPath>`).join('');
        let regs = '';
        for (let c = 0; c < 1 << K; c++) {
          defs += `<mask id="${uid}m${c}"><rect x="0" y="0" width="${VW}" height="${VH}" fill="#fff"/>${C.map((q, i) => c & (1 << i) ? '' : `<circle cx="${q[0]}" cy="${q[1]}" r="${q[2]}" fill="#000"/>`).join('')}</mask>`;
          let inner = `<rect class="rg" data-c="${c}" x="6" y="6" width="${VW - 12}" height="${VH - 12}" rx="10" fill="transparent" mask="url(#${uid}m${c})"/>`;
          C.forEach((q, i) => { if (c & (1 << i)) inner = `<g clip-path="url(#${uid}c${i})">${inner}</g>`; });
          regs += inner;
        }
        const lbl = c => { const e = elems && elems[c] && elems[c].length && elems[c].join(', ').length <= 14 ? elems[c].join(', ') : null; return e || String(counts[c]); };
        body.innerHTML = `<div class="lb-statlab-task"><span class="pg"></span><span class="ex"></span></div>
<div class="lb-statlab-g"><svg viewBox="0 0 ${VW} ${VH}" style="touch-action:manipulation"><defs>${defs}</defs>
<rect x="6" y="6" width="${VW - 12}" height="${VH - 12}" rx="10" fill="#fff" stroke="#1b1f3a" stroke-width="1.5"/>${regs}
${C.map((q, i) => `<circle cx="${q[0]}" cy="${q[1]}" r="${q[2]}" fill="${COLS[i]}" fill-opacity=".07" stroke="${COLS[i]}" stroke-width="2.5" pointer-events="none"/>`).join('')}
${Object.entries(POS).map(([c, xy]) => `<text x="${xy[0]}" y="${xy[1] + 5}" text-anchor="middle" font-size="${elems ? 11 : 15}" font-weight="900" fill="#1b1f3a" pointer-events="none">${esc(lbl(+c))}</text>`).join('')}
${names.map((n, i) => `<text x="${NPOS[i][0]}" y="${NPOS[i][1]}" text-anchor="${NPOS[i][2]}" font-size="14" font-weight="900" fill="${COLS[i]}" pointer-events="none">${esc(n)}</text>`).join('')}
<text x="16" y="24" font-size="13" font-weight="900" fill="#6b7090" pointer-events="none">U</text></svg></div>
<div class="lb-statlab-f"></div>
<div class="lb-statlab-row"><button class="lb-statlab-btn alt cl" style="flex:1">Clear</button><button class="lb-statlab-btn ck" style="flex:2">Check ✓</button></div><div class="lb-statlab-msg"></div>`;
        const svg = body.querySelector('svg'), fx = body.querySelector('.lb-statlab-f'), msg = body.querySelector('.lb-statlab-msg');
        let ti = 0, shade = 0, solved = false;
        const n = m => { let s = 0; for (let c = 0; c < 1 << K; c++) if (m & (1 << c)) s += counts[c]; return s; };
        const nS = i => n(setMask(i));
        function formula(m) {
          for (let i = 0; i < K; i++) for (let j = i + 1; j < K; j++) if (m === (setMask(i) | setMask(j))) { const a = names[i], b = names[j]; return `n(${a}∪${b}) = n(${a}) + n(${b}) − n(${a}∩${b}) = ${nS(i)} + ${nS(j)} − ${n(setMask(i) & setMask(j))} = <b>${n(m)}</b>`; }
          if (K === 3 && m === (setMask(0) | setMask(1) | setMask(2))) { const [a, b, c] = names, A = setMask(0), B = setMask(1), Cc = setMask(2); return `n(${a}∪${b}∪${c}) = ${nS(0)} + ${nS(1)} + ${nS(2)} − ${n(A & B)} − ${n(B & Cc)} − ${n(A & Cc)} + ${n(A & B & Cc)} = <b>${n(m)}</b>`; }
          for (let i = 0; i < K; i++) if (m === (ALL & ~setMask(i))) return `n(${names[i]}′) = n(U) − n(${names[i]}) = ${n(ALL)} − ${nS(i)} = <b>${n(m)}</b>`;
          return `n(${esc(show(tasks[ti].ex))}) = <b>${n(m)}</b>`;
        }
        function draw(m, cls) {
          body.querySelector('.pg').textContent = `${Math.min(ti + 1, tasks.length)}/${tasks.length}`;
          body.querySelector('.ex').textContent = `Shade ${show(tasks[Math.min(ti, tasks.length - 1)].ex)}`;
          svg.querySelectorAll('.rg').forEach(r => { const c = +r.dataset.c; r.setAttribute('fill', shade & (1 << c) ? (solved ? '#2ed3a5' : '#8b5cf6') : 'transparent'); r.setAttribute('fill-opacity', '.55'); });
          fx.innerHTML = solved ? formula(tasks[ti].m) : `Shaded so far: n = <b>${n(shade)}</b> &nbsp;·&nbsp; n(U) = ${n(ALL)}, ${names.map((nm, i) => `n(${esc(nm)}) = ${nS(i)}`).join(', ')}`;
          body.querySelector('.ck').textContent = solved ? (ti < tasks.length - 1 ? 'Next ▶' : '✓ Done') : 'Check ✓';
          msg.className = 'lb-statlab-msg ' + (cls || ''); msg.innerHTML = m || (solved ? '' : 'Tap regions to shade or unshade them.');
        }
        svg.addEventListener('click', e => {
          if (solved) return;
          const pt = svgPt(svg, e); if (pt.x < 6 || pt.y < 6 || pt.x > VW - 6 || pt.y > VH - 6) return;
          let c = 0; C.forEach((q, i) => { if (Math.hypot(pt.x - q[0], pt.y - q[1]) <= q[2]) c |= 1 << i; });
          shade ^= 1 << c; api.sfx && api.sfx('tap'); draw();
        });
        body.querySelector('.cl').addEventListener('click', () => { if (solved) return; shade = 0; draw(); });
        body.querySelector('.ck').addEventListener('click', () => {
          if (solved) { if (ti < tasks.length - 1) { ti++; shade = 0; solved = false; draw(); } return; }
          const t = tasks[ti];
          if (shade === t.m) { solved = true; api.sfx && api.sfx('correct'); draw(`✔ Correct! ${ti < tasks.length - 1 ? 'Tap Next for the next one.' : ''}`, 'ok'); if (ti === tasks.length - 1) win(`All ${tasks.length} regions shaded correctly! Last: n(${show(t.ex)}) = ${n(t.m)}`); return; }
          const extra = shade & ~t.m, miss = t.m & ~shade, cnt = x => { let k = 0; for (let c = 0; c < 1 << K; c++) if (x & (1 << c)) k++; return k; };
          api.sfx && api.sfx('wrong');
          draw(`Not yet: ${cnt(extra) ? `${cnt(extra)} region${cnt(extra) > 1 ? 's' : ''} should NOT be shaded` : ''}${cnt(extra) && cnt(miss) ? ' and ' : ''}${cnt(miss) ? `${cnt(miss)} region${cnt(miss) > 1 ? 's are' : ' is'} missing` : ''}. Hint: ∪ = in either, ∩ = in both, ′ = outside.`, 'bad');
        });
        draw();
      }

      if (mode === 'central') (Array.isArray(p.freq) && p.freq.length >= 2 ? grouped : central)();
      else ({ correlation, normal, venn })[mode]();
      return () => { cleanups.forEach(f => f()); host.innerHTML = ''; };
    },
    example: {
      mode: 'central', label: 'Marks (out of 20)', data: [4, 6, 6, 7, 9, 10, 12], range: [0, 20], step: 1,
      targets: { mean: 10, median: 9 }, challenge: 'Drag the dots so that the mean becomes 10 but the median stays 9'
    },
    examples: [
      { mode: 'central', label: 'Daily wages (₹)', freq: [5, 8, 12, 15, 6, 4], classStart: 100, width: 20, maxF: 20,
        targets: { mode: 170, tol: 0.5 }, challenge: 'Grouped data: drag the bars so the mode is exactly 170 (±0.5)' },
      { mode: 'correlation', xLabel: 'Hours studied', yLabel: 'Marks', xRange: [0, 10], yRange: [0, 10],
        points: [[1, 3], [2, 6], [3, 2], [4, 7], [5, 4], [6, 8], [7, 3], [8, 6]], targets: { pearson: [0.9, 1] },
        challenge: 'Drag the points to make Karl Pearson’s r at least 0.9' },
      { mode: 'venn', sets: 2, names: ['क्रिकेट', 'फ़ुटबॉल'], counts: { A: 12, B: 9, AB: 5, '': 4 }, tasks: ['A∪B', 'A∩B′', '(A∪B)′'],
        challenge: 'Shade the regions — क्रिकेट (A) and फ़ुटबॉल (B)' }
    ]
  });
})();
