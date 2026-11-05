/* StudyVerse Concept Lab: circularflow — circular flow of income, the investment multiplier and
 * national-income aggregates (CBSE Class 12 Macroeconomics, NCERT notation).
 *
 * MODES
 *   flow        Animated money flows between households, firms, government, the financial sector and the
 *               rest of the world. Tap a flow (or its chip) and move the slider: saving S, taxes T, imports M
 *               are leakages (shares of income); investment I, government purchases G, exports X are
 *               injections (₹). Income Y rises while injections > leakages and settles where
 *               S + T + M = I + G + X, i.e. Y = (I + G + X) ÷ (s + t + m).
 *   multiplier  MPC slider and ΔI slider. Bars show each round of spending (ΔI, MPC·ΔI, MPC²·ΔI …);
 *               k = 1 ÷ (1 − MPC) = 1 ÷ MPS and ΔY = k × ΔI.
 *   national    Start from GDPMP (or from C + I + G + (X − M), or from NDPFC by the income method) and
 *               step across the aggregates: ± depreciation (gross ↔ net), ± NFIA (domestic ↔ national),
 *               ± net indirect taxes (market price ↔ factor cost). The child types each new value.
 *
 * PARAMS (all optional — every one has a built-in default)
 *   mode        string  'flow' | 'multiplier' | 'national'                                     'flow'
 *   challenge   string  Challenge sentence                                                    (by mode)
 *   unit        string  Money unit label                                                      '₹ crore'
 *   labels      object  Names {households, firms, government, financial, foreign} (any language) English
 * flow:
 *   sectors     array   extra sectors shown: any of 'financial','government','foreign'       all three
 *   start       object  {I, G, X} injections (unit) and {s, t, m} leakage shares of income   {I:100,G:60,X:40,s:0.1,t:0.1,m:0.05}
 *   targetY     number  income the economy must settle at                                    1000
 *   tol         number  relative tolerance for targetY                                       0.005
 * multiplier:
 *   mpc         number  starting MPC (0–0.95)                                                0.5
 *   dI          number  starting change in investment                                        100
 *   lock        string  'dI' | 'mpc' | '' — which slider is fixed                             'dI'
 *   mpcRange    object  {min, max, step}                                                     {min:0.1,max:0.95,step:0.05}
 *   dIRange     object  {min, max, step}                                                     {min:10,max:500,step:10}
 *   target      object  {dY} or {k} the child must reach                                      {dY:400}
 * national:
 *   gdpmp       number  GDP at market price (used when no expenditure/income data)           12000
 *   expenditure object  {C, I, G, X, M}: GDPMP = C + I + G + (X − M) is the first step         none
 *   income      object  {compensation, operatingSurplus, mixedIncome}: start at NDPFC          none
 *   dep         number  depreciation (consumption of fixed capital)                          1200
 *   nfia        number  net factor income from abroad (may be negative)                       −300
 *   indirectTaxes, subsidies  numbers; NIT = indirect taxes − subsidies                       1100, 200
 *   nit         number  net indirect taxes (used if indirectTaxes not given)
 *   target      string  aggregate to reach, e.g. 'NNPfc' (national income), 'GNPmp', 'NDPfc'  'NNPfc'
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function inr(n, dp) {
    if (!isFinite(n)) return '—';
    const neg = n < 0; const f = Math.pow(10, dp == null ? 2 : dp); n = Math.abs(Math.round(n * f) / f);
    let [i, d] = n.toFixed(dp == null ? 2 : dp).split('.'); let l3 = i.slice(-3), rest = i.slice(0, -3);
    if (rest) l3 = ',' + l3; rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    d = d ? d.replace(/0+$/, '') : '';
    return (neg ? '−' : '') + rest + l3 + (d ? '.' + d : '');
  }
  const num = s => { const t = String(s == null ? '' : s).replace(/[−–]/g, '-').replace(/[^\d.\-]/g, ''); if (!t || t === '-') return NaN; const v = parseFloat(t); return isFinite(v) ? v : NaN; };
  const fin = (v, d) => isFinite(+v) && v !== null && v !== '' ? +v : d;
  const r2 = v => Math.round(v * 100) / 100;
  const CSS = `
.lb-circularflow-w{font-size:13px;color:#1b1f3a;user-select:none;-webkit-user-select:none;line-height:1.3}
.lb-circularflow-w button{font-family:inherit;cursor:pointer;border:none}
.lb-circularflow-ch{font-weight:800;font-size:13.5px;line-height:1.3;margin-bottom:6px}
.lb-circularflow-svg{background:#f7f8ff;border-radius:16px}
.lb-circularflow-svg svg{display:block;width:100%;height:auto}
.lb-circularflow-svg .hit{cursor:pointer}
.lb-circularflow-chips{display:flex;gap:4px;margin-top:6px}
.lb-circularflow-chips button{flex:1;min-height:38px;border-radius:10px;font-weight:900;font-size:13px;background:#eef0fb;color:#1b1f3a;line-height:1}
.lb-circularflow-chips button small{display:block;font-size:9px;font-weight:800;opacity:.8;margin-top:2px}
.lb-circularflow-chips button.lk{background:#fff0f0;color:#d03c3c}.lb-circularflow-chips button.ij{background:#e3fbf3;color:#0f7a5c}
.lb-circularflow-chips button.on{outline:3px solid #8b5cf6;outline-offset:-3px}
.lb-circularflow-sl{display:flex;align-items:center;gap:8px;margin-top:5px;font-weight:800;font-size:12.5px}
.lb-circularflow-sl input{flex:1;height:30px;accent-color:#8b5cf6;min-width:0}
.lb-circularflow-sl b{min-width:66px;text-align:right;color:#7044e0;font-size:14px}
.lb-circularflow-sl span{min-width:92px;line-height:1.1}
.lb-circularflow-kp{display:flex;gap:5px;margin-top:6px}
.lb-circularflow-kp div{flex:1;border-radius:11px;padding:4px 3px;text-align:center;font-weight:900;font-size:14px;line-height:1.15;background:#f6f7ff}
.lb-circularflow-kp small{display:block;font-size:9.5px;color:#6b7090;font-weight:800}
.lb-circularflow-kp .w{background:#fff0f0;color:#d03c3c}.lb-circularflow-kp .j{background:#e3fbf3;color:#0f7a5c}.lb-circularflow-kp .y{background:#f1ecff;color:#7044e0}
.lb-circularflow-msg{margin-top:5px;font-weight:700;font-size:12.5px;line-height:1.35;min-height:17px}
.lb-circularflow-msg.ok{color:#0f7a5c}.lb-circularflow-msg.bad{color:#d03c3c}
.lb-circularflow-f{background:#fff8e1;border-radius:12px;padding:6px 9px;font-weight:800;font-size:13px;margin-top:6px;line-height:1.5}
.lb-circularflow-f b{color:#7044e0;font-size:15px}
.lb-circularflow-btn{min-height:40px;border-radius:12px;background:#8b5cf6;color:#fff;font-weight:800;font-size:14px;padding:0 14px}
.lb-circularflow-btn.alt{background:#eef0fb;color:#1b1f3a}
.lb-circularflow-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.lb-circularflow-grid div{border-radius:10px;background:#f6f7ff;text-align:center;padding:4px 2px;font-weight:900;font-size:13px;line-height:1.15;min-height:36px;border:2px solid transparent}
.lb-circularflow-grid div small{display:block;font-size:10.5px;color:#6b7090;font-weight:800}
.lb-circularflow-grid div.vis{background:#eef6ff}
.lb-circularflow-grid div.cur{border-color:#8b5cf6;background:#f3efff;box-shadow:0 2px 8px #8b5cf640}
.lb-circularflow-grid div.tgt{border-style:dashed;border-color:#ff6b6b}
.lb-circularflow-grid div.cur.tgt{border-style:solid;border-color:#2ed3a5;background:#e3fbf3}
.lb-circularflow-ops{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:6px}
.lb-circularflow-ops button{min-height:38px;border-radius:10px;font-weight:800;font-size:12px;background:#eef0fb;color:#1b1f3a;line-height:1.1}
.lb-circularflow-ops button small{display:block;font-size:10px;color:#6b7090}
.lb-circularflow-pend{display:flex;align-items:center;gap:6px;background:#fff8e1;border-radius:12px;padding:5px 8px;margin-top:6px;font-weight:800;font-size:12.5px;flex-wrap:wrap}
.lb-circularflow-pend input{width:96px;height:36px;border:2px solid #e6dcae;border-radius:9px;padding:0 6px;font:inherit;font-weight:900;text-align:right;user-select:text;-webkit-user-select:text}
.lb-circularflow-der{background:#f7f8ff;border-radius:12px;padding:4px 8px;margin-top:6px;font-size:12px;font-weight:700;max-height:86px;overflow-y:auto}
.lb-circularflow-der div{display:flex;justify-content:space-between;gap:6px;border-bottom:1px dashed #e3e6f6;padding:1px 0}
.lb-circularflow-data{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}
.lb-circularflow-data span{background:#f6f7ff;border-radius:99px;padding:3px 8px;font-size:11.5px;font-weight:800}
`;

  Labs.register('circularflow', {
    title: 'Circular flow & national income',
    subjects: ['economics'],
    render(host, p, api) {
      p = p && typeof p === 'object' ? p : {};
      const mode = ['flow', 'multiplier', 'national'].includes(p.mode) ? p.mode : 'flow';
      const unit = p.unit || '₹ crore';
      const LB = Object.assign({ households: 'Households', firms: 'Firms', government: 'Government', financial: 'Financial sector', foreign: 'Rest of the world' }, p.labels && typeof p.labels === 'object' ? p.labels : {});
      let won = false, raf = 0; const timers = [];
      const win = m => { if (won) return; won = true; api.sfx && api.sfx('correct'); api.win(m); };
      host.innerHTML = `<div class="lb-circularflow-w"><style>${CSS}</style><div class="lb-circularflow-ch"></div><div class="lb-circularflow-body"></div></div>`;
      const W = host.firstElementChild, body = W.querySelector('.lb-circularflow-body');
      const setCh = t => { W.querySelector('.lb-circularflow-ch').textContent = '🎯 Challenge: ' + t; };

      /* ───────────── FLOW ───────────── */
      function flow() {
        const secs = Array.isArray(p.sectors) ? p.sectors : ['financial', 'government', 'foreign'];
        const has = { financial: secs.includes('financial'), government: secs.includes('government'), foreign: secs.includes('foreign') };
        const st = Object.assign({ I: 100, G: 60, X: 40, s: 0.1, t: 0.1, m: 0.05 }, p.start && typeof p.start === 'object' ? p.start : {});
        const v = { I: has.financial ? fin(st.I, 100) : 0, G: has.government ? fin(st.G, 60) : 0, X: has.foreign ? fin(st.X, 40) : 0, s: has.financial ? fin(st.s, 0.1) : 0, t: has.government ? fin(st.t, 0.1) : 0, m: has.foreign ? fin(st.m, 0.05) : 0 };
        if (!has.financial && !has.government && !has.foreign) { has.financial = true; v.I = 100; v.s = 0.1; }
        const L = () => v.s + v.t + v.m, J = () => v.I + v.G + v.X, Ystar = () => L() > 0 ? J() / L() : Infinity;
        const tgt = fin(p.targetY, isFinite(J() / L()) ? Math.round(J() / L() / 10) * 10 + 200 : 1000), tol = fin(p.tol, 0.005);
        let Y = isFinite(Ystar()) ? Ystar() : 500, touched = false, sel = has.financial ? 'I' : has.government ? 'G' : 'X', info = '';
        setCh(p.challenge || `Change the leakages and injections so that income settles at ${inr(tgt, 0)} (${unit})`);
        const FL = {
          S: ['s', 'Saving', 'lk', 'financial', 'A leakage: income households do not spend; it goes to banks / financial markets.'],
          T: ['t', 'Taxes', 'lk', 'government', 'A leakage: income paid to the government instead of spent on goods.'],
          M: ['m', 'Imports', 'lk', 'foreign', 'A leakage: spending that goes to producers abroad.'],
          I: ['I', 'Investment', 'ij', 'financial', 'An injection: firms borrow savings to buy capital goods.'],
          G: ['G', 'Govt. purchases', 'ij', 'government', 'An injection: government spending on goods and services from firms.'],
          X: ['X', 'Exports', 'ij', 'foreign', 'An injection: foreigners buy our goods.']
        };
        const avail = Object.keys(FL).filter(k => has[FL[k][3]]);
        const P = {
          Y: 'M262,104 Q180,68 98,104', C: 'M98,148 Q180,186 262,148',
          T: 'M40,94 Q40,28 138,28', G: 'M222,28 Q320,28 320,94', S: 'M100,126 L138,126', I: 'M222,126 L260,126',
          M: 'M40,156 Q40,222 138,222', X: 'M222,222 Q320,222 320,156'
        };
        const box = (x, y, w, h, fill, label, emoji) => `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${fill}"/><text x="${x + w / 2}" y="${y + h / 2 - 3}" text-anchor="middle" font-size="15">${emoji}</text><text x="${x + w / 2}" y="${y + h / 2 + 12}" text-anchor="middle" font-size="10" font-weight="800" fill="#1b1f3a">${esc(label)}</text></g>`;
        const flowsOn = ['Y', 'C', ...(has.financial ? ['S', 'I'] : []), ...(has.government ? ['T', 'G'] : []), ...(has.foreign ? ['M', 'X'] : [])];
        const col = k => k === 'Y' || k === 'C' ? '#3b82f6' : FL[k][2] === 'lk' ? '#ff6b6b' : '#2ed3a5';
        const svgPaths = flowsOn.map(k => `<path id="cf-${k}" d="${P[k]}" fill="none" stroke="${col(k)}" stroke-linecap="round" marker-end="url(#cfa-${k})" opacity=".85"/><path class="hit" data-f="${k}" d="${P[k]}" fill="none" stroke="transparent" stroke-width="22"/>`).join('');
        const uid = 'cf' + Math.random().toString(36).slice(2, 7);
        body.innerHTML = `<div class="lb-circularflow-svg"><svg viewBox="0 0 360 250">
<defs>${flowsOn.map(k => `<marker id="cfa-${k}-${uid}" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0L10,5L0,10z" fill="${col(k)}"/></marker>`).join('')}</defs>
${svgPaths.replace(/url\(#cfa-(\w)\)/g, `url(#cfa-$1-${uid})`).replace(/id="cf-/g, `id="${uid}-`)}
<g class="dots"></g>
${box(8, 94, 92, 62, '#ffe7c2', LB.households, '🏠')}${box(260, 94, 92, 62, '#dbeafe', LB.firms, '🏭')}
${has.government ? box(138, 8, 84, 40, '#ede9fe', LB.government, '🏛️') : ''}${has.financial ? box(138, 106, 84, 40, '#dcfce7', LB.financial, '🏦') : ''}${has.foreign ? box(138, 202, 84, 40, '#fee2e2', LB.foreign, '🌍') : ''}
<g class="lbl" font-size="9.5" font-weight="900"></g></svg></div>
<div class="lb-circularflow-chips">${avail.map(k => `<button data-f="${k}" class="${FL[k][2]}">${k}<small>${FL[k][2] === 'lk' ? 'leakage' : 'injection'}</small></button>`).join('')}</div>
<div class="lb-circularflow-sl"><span class="nm"></span><input type="range"><b></b></div>
<div class="lb-circularflow-kp"><div class="w"></div><div class="j"></div><div class="y"></div></div>
<div class="lb-circularflow-msg"></div>`;
        const svg = body.querySelector('svg'), dotsG = svg.querySelector('.dots'), lblG = svg.querySelector('.lbl'), rng = body.querySelector('input'), msg = body.querySelector('.lb-circularflow-msg');
        const paths = {}; flowsOn.forEach(k => { paths[k] = svg.getElementById ? svg.getElementById(`${uid}-${k}`) : svg.querySelector(`#${uid}-${k}`); });
        const lens = {}; flowsOn.forEach(k => { try { lens[k] = paths[k].getTotalLength(); } catch (e) { lens[k] = 100; } });
        const amt = k => k === 'Y' ? Y : k === 'C' ? Y * (1 - L()) : k === 'S' ? v.s * Y : k === 'T' ? v.t * Y : k === 'M' ? v.m * Y : v[k];
        const LPOS = { Y: [180, 80, 'middle'], C: [180, 178, 'middle'], T: [46, 40, 'start'], G: [314, 40, 'end'], S: [119, 119, 'middle'], I: [241, 119, 'middle'], M: [46, 218, 'start'], X: [314, 218, 'end'] };
        function selUI() {
          body.querySelectorAll('.lb-circularflow-chips button').forEach(b => b.classList.toggle('on', b.dataset.f === sel));
          const f = FL[sel], rate = f[2] === 'lk';
          rng.min = 0; rng.max = rate ? 0.4 : 400; rng.step = rate ? 0.05 : 10; rng.value = v[f[0]];
          body.querySelector('.lb-circularflow-sl .nm').textContent = rate ? `${f[1]} share of Y (${f[0]})` : `${f[1]} (${sel})`;
        }
        function labels() {
          lblG.innerHTML = flowsOn.map(k => { const [x, y, a] = LPOS[k]; return `<text x="${x}" y="${y}" text-anchor="${a}" fill="${col(k) === '#2ed3a5' ? '#0f9a72' : col(k) === '#ff6b6b' ? '#e04848' : '#2f6fd6'}" stroke="#f7f8ff" stroke-width="3" paint-order="stroke">${k} ${inr(amt(k), 0)}</text>`; }).join('');
          flowsOn.forEach(k => { const a = amt(k); paths[k].setAttribute('stroke-width', Math.max(1.5, Math.min(9, 1.5 + a / Math.max(Y, 1) * 9 * (k === 'Y' || k === 'C' ? .8 : 2.2)))); });
        }
        function stats() {
          const w = L() * Y, j = J(), ys = Ystar();
          const f = FL[sel]; body.querySelector('.lb-circularflow-sl b').textContent = f[2] === 'lk' ? v[f[0]].toFixed(2) : inr(v[f[0]], 0);
          const [a, b, c] = body.querySelectorAll('.lb-circularflow-kp div');
          a.innerHTML = `${inr(w, 0)}<small>leakages S+T+M</small>`; b.innerHTML = `${inr(j, 0)}<small>injections I+G+X</small>`; c.innerHTML = `${inr(Y, 0)}<small>income Y (${esc(unit)})</small>`;
          const gap = j - w, steady = Math.abs(gap) <= Math.max(0.5, Y * 0.002);
          let m = info ? info + ' ' : '';
          if (!isFinite(ys)) m += 'With no leakages at all, income would grow without limit!';
          else if (steady) m += `⚖️ Injections = leakages, so income is steady at ${inr(Y, 0)}.`;
          else m += gap > 0 ? `📈 Injections > leakages → income is RISING (towards ${inr(ys, 0)}).` : `📉 Leakages > injections → income is FALLING (towards ${inr(ys, 0)}).`;
          msg.textContent = m; msg.className = 'lb-circularflow-msg' + (steady && Math.abs(Y - tgt) <= tgt * tol ? ' ok' : '');
          if (touched && steady && isFinite(ys) && Math.abs(ys - tgt) <= tgt * tol && Math.abs(Y - tgt) <= tgt * tol)
            win(`Income settled at ${inr(ys, 0)}: leakages ${inr(L() * ys, 0)} = injections ${inr(j, 0)}  (Y = ${inr(j, 0)} ÷ ${r2(L())})`);
        }
        let phase = 0, last = 0, acc = 0;
        function tick(ts) {
          const dt = last ? Math.min(0.05, (ts - last) / 1000) : 0; last = ts; phase += dt;
          const ys = Ystar();
          if (isFinite(ys)) { const k = 1 / 1.4; Y += (ys - Y) * (1 - Math.exp(-k * dt)); if (Math.abs(ys - Y) < 0.05) Y = ys; } else Y = Math.min(Y * (1 + dt * 0.3) + 1, 1e6);
          let s = '';
          flowsOn.forEach(k => {
            const a = amt(k); if (a <= 0.01) return; const n = Math.max(1, Math.min(7, Math.round(a / Math.max(Y, 1) * (k === 'Y' || k === 'C' ? 6 : 12)))), len = lens[k];
            for (let i = 0; i < n; i++) { const f = ((phase * 0.25 + i / n) % 1); const pt = paths[k].getPointAtLength(f * len); s += `<circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="3" fill="${col(k)}" stroke="#fff" stroke-width="1"/>`; }
          });
          dotsG.innerHTML = s;
          acc += dt; if (acc > 0.1) { acc = 0; labels(); stats(); }
          raf = requestAnimationFrame(tick);
        }
        const onClick = e => { const t = e.target.closest('[data-f]'); if (!t) return; const k = t.dataset.f; if (FL[k]) { sel = k; info = `${k}: ${FL[k][4]}`; selUI(); } else info = k === 'Y' ? 'Y: factor payments — wages, rent, interest and profit paid by firms to households.' : 'C: consumption spending by households on goods made by firms.'; api.sfx && api.sfx('tap'); stats(); };
        body.addEventListener('click', onClick);
        rng.addEventListener('input', () => { const f = FL[sel]; v[f[0]] = +rng.value; touched = true; info = ''; stats(); labels(); });
        selUI(); labels(); stats();
        raf = requestAnimationFrame(tick);
      }

      /* ───────────── MULTIPLIER ───────────── */
      function multiplier() {
        const mr = Object.assign({ min: 0.1, max: 0.95, step: 0.05 }, p.mpcRange || {}), ir = Object.assign({ min: 10, max: 500, step: 10 }, p.dIRange || {});
        let mpc = Math.min(Math.max(fin(p.mpc, 0.5), mr.min), Math.min(0.99, mr.max)), dI = Math.min(Math.max(fin(p.dI, 100), ir.min), ir.max);
        const lock = p.lock === 'mpc' || p.lock === '' || p.lock === 'none' ? p.lock : 'dI';
        const tg = p.target && typeof p.target === 'object' ? p.target : { dY: 400 };
        const k = () => 1 / (1 - mpc), dY = () => k() * dI;
        let touched = false, shown = 10, playing = false;
        const tText = tg.k != null ? `make the multiplier k = ${tg.k}` : `make income rise by ΔY = ${inr(fin(tg.dY, 400))} (${unit})`;
        setCh(p.challenge || `${lock === 'dI' ? `Investment rises by ${inr(dI)} (${unit}). Set the MPC to ` : lock === 'mpc' ? `MPC is ${mpc}. Choose ΔI to ` : 'Use the sliders to '}${tText}`);
        body.innerHTML = `<div class="lb-circularflow-svg"><svg viewBox="0 0 360 170"></svg></div>
${lock !== 'mpc' ? `<div class="lb-circularflow-sl"><span>MPC (ΔC/ΔY)</span><input class="mp" type="range" min="${mr.min}" max="${mr.max}" step="${mr.step}" value="${mpc}"><b class="mpv"></b></div>` : ''}
${lock !== 'dI' ? `<div class="lb-circularflow-sl"><span>ΔI (${esc(unit)})</span><input class="di" type="range" min="${ir.min}" max="${ir.max}" step="${ir.step}" value="${dI}"><b class="div"></b></div>` : ''}
<div class="lb-circularflow-f"></div>
<div style="display:flex;gap:6px;margin-top:6px"><button class="lb-circularflow-btn pl" style="flex:1">▶ Play spending rounds</button></div>
<div class="lb-circularflow-msg"></div>`;
        const svg = body.querySelector('svg'), f = body.querySelector('.lb-circularflow-f'), msg = body.querySelector('.lb-circularflow-msg');
        function draw() {
          const N = 10, x0 = 34, bw = 28, H = 120, top = 18;
          const total = dY(), scaleTop = Math.max(total, dI) * 1.05;
          let s = `<text x="6" y="12" font-size="10" font-weight="800" fill="#6b7090">ΔY per round (bars) and running total (line), ${esc(unit)}</text>`;
          s += `<line x1="${x0 - 4}" y1="${top + H}" x2="352" y2="${top + H}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          const y = v => top + H - v / scaleTop * H;
          s += `<line x1="${x0 - 4}" x2="352" y1="${y(total)}" y2="${y(total)}" stroke="#8b5cf6" stroke-dasharray="5 4"/><text x="350" y="${y(total) - 3}" text-anchor="end" font-size="10" font-weight="900" fill="#7044e0">ΔY = ${inr(total)}</text>`;
          let cum = 0, pts = [];
          for (let i = 0; i < N; i++) {
            const r = dI * Math.pow(mpc, i); cum += r; const x = x0 + i * 31.5;
            if (i < shown) { s += `<rect x="${x}" y="${y(r)}" width="${bw}" height="${top + H - y(r)}" rx="4" fill="${i ? '#ffc93c' : '#2ed3a5'}"/>`; pts.push(`${x + bw / 2},${y(cum)}`); }
            s += `<text x="${x + bw / 2}" y="${top + H + 12}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#6b7090">${i + 1}</text>`;
          }
          if (pts.length) s += `<polyline points="${pts.join(' ')}" fill="none" stroke="#3b82f6" stroke-width="2.5"/>` + pts.map(q => `<circle cx="${q.split(',')[0]}" cy="${q.split(',')[1]}" r="2.8" fill="#3b82f6"/>`).join('');
          s += `<text x="${x0 - 6}" y="${top + H + 24}" font-size="9.5" font-weight="800" fill="#6b7090">round →</text>`;
          svg.innerHTML = s;
          const after = dI * (1 - Math.pow(mpc, shown)) / (1 - mpc);
          f.innerHTML = `k = 1 ÷ (1 − MPC) = 1 ÷ ${r2(1 - mpc)} = <b>${r2(k())}</b> &nbsp;·&nbsp; ΔY = k × ΔI = ${r2(k())} × ${inr(dI)} = <b>${inr(total)}</b><br><small style="color:#6b7090">After ${shown} rounds: ${inr(after)} (${(after / total * 100).toFixed(1)}% of ΔY). MPS = ${r2(1 - mpc)}</small>`;
          const mv = body.querySelector('.mpv'), dv = body.querySelector('.div'); if (mv) mv.textContent = mpc.toFixed(2); if (dv) dv.textContent = inr(dI);
          const hit = tg.k != null ? Math.abs(k() - fin(tg.k, 0)) < 1e-6 : Math.abs(total - fin(tg.dY, 400)) < 1e-6 * Math.max(1, total);
          msg.className = 'lb-circularflow-msg' + (hit ? ' ok' : '');
          msg.textContent = hit ? `🎯 k = ${r2(k())}: each ₹1 of new investment raises income by ₹${r2(k())}.` : `Higher MPC → people re-spend more of each round → bigger multiplier.`;
          if (hit && touched) win(`MPC ${mpc.toFixed(2)} → k = 1/(1 − ${mpc.toFixed(2)}) = ${r2(k())}; ΔY = ${r2(k())} × ${inr(dI)} = ${inr(total)}`);
        }
        function play() {
          if (playing) return; playing = true; shown = 0; draw();
          const step = () => { shown++; api.sfx && api.sfx('coin'); draw(); if (shown < 10) timers.push(setTimeout(step, 350)); else playing = false; };
          timers.push(setTimeout(step, 250));
        }
        body.addEventListener('input', e => {
          if (e.target.classList.contains('mp')) mpc = Math.round(+e.target.value * 1000) / 1000;
          if (e.target.classList.contains('di')) dI = +e.target.value;
          touched = true; draw();
        });
        body.querySelector('.pl').addEventListener('click', play);
        draw();
      }

      /* ───────────── NATIONAL INCOME ───────────── */
      function national() {
        const dep = fin(p.dep, 1200), nfia = fin(p.nfia, -300);
        const nit = p.indirectTaxes != null ? fin(p.indirectTaxes, 0) - fin(p.subsidies, 0) : p.nit != null ? fin(p.nit, 900) : 1100 - 200;
        const it = p.indirectTaxes != null ? fin(p.indirectTaxes, 0) : p.nit != null ? null : 1100, sub = p.indirectTaxes != null ? fin(p.subsidies, 0) : p.nit != null ? null : 200;
        const ex = p.expenditure && typeof p.expenditure === 'object' ? p.expenditure : null, inc = !ex && p.income && typeof p.income === 'object' ? p.income : null;
        let gdpmp;
        if (ex) gdpmp = fin(ex.C, 0) + fin(ex.I, 0) + fin(ex.G, 0) + fin(ex.X, 0) - fin(ex.M, 0);
        else if (inc) gdpmp = fin(inc.compensation, 0) + fin(inc.operatingSurplus, 0) + fin(inc.mixedIncome, 0) + dep + nit;
        else gdpmp = fin(p.gdpmp, 12000);
        const NAME = a => `${a.g ? 'G' : 'N'}${a.n ? 'N' : 'D'}P<sub>${a.mp ? 'MP' : 'FC'}</sub>`;
        const TXT = a => `${a.g ? 'G' : 'N'}${a.n ? 'N' : 'D'}P${a.mp ? 'mp' : 'fc'}`;
        const value = a => gdpmp - (a.g ? 0 : dep) + (a.n ? nfia : 0) - (a.mp ? 0 : nit);
        const parse = s => { const m = /^([GN])([ND])P\s*(mp|fc)$/i.exec(String(s || '').trim()); return m ? { g: m[1].toUpperCase() === 'G', n: m[2].toUpperCase() === 'N', mp: m[3].toLowerCase() === 'mp' } : null; };
        const T = parse(p.target) || { g: false, n: true, mp: false };
        const startA = inc ? { g: false, n: false, mp: false } : { g: true, n: false, mp: true };
        let cur = null, pending = null, steps = [], visited = {};
        const kA = a => TXT(a);
        if (ex) pending = { to: startA, short: 'C + I + G + (X − M)', label: `C + I + G + (X − M) = ${inr(fin(ex.C, 0))} + ${inr(fin(ex.I, 0))} + ${inr(fin(ex.G, 0))} + (${inr(fin(ex.X, 0))} − ${inr(fin(ex.M, 0))})` };
        else if (inc) pending = { to: startA, short: 'Compensation + Op. surplus + Mixed income', label: `Compensation + Operating surplus + Mixed income = ${inr(fin(inc.compensation, 0))} + ${inr(fin(inc.operatingSurplus, 0))} + ${inr(fin(inc.mixedIncome, 0))}` };
        else { cur = startA; visited[kA(cur)] = 1; steps.push([`${NAME(cur)} (given)`, value(cur)]); }
        setCh(p.challenge || `Starting from ${ex ? 'the expenditure data' : inc ? 'the income data' : 'GDP at market price'}, work out ${TXT(T) === 'NNPfc' ? 'national income (NNPFC)' : TXT(T)}`);
        const OPS = [['dep', -1, '− Depreciation', 'gross → net'], ['nfia', 1, '+ NFIA', 'domestic → national'], ['nit', -1, '− NIT', 'MP → FC'], ['dep', 1, '+ Depreciation', 'net → gross'], ['nfia', -1, '− NFIA', 'national → domestic'], ['nit', 1, '+ NIT', 'FC → MP']];
        const ORDER = [{ g: true, n: false }, { g: true, n: true }, { g: false, n: false }, { g: false, n: true }];
        function draw(m, cls) {
          const cell = a => { const k = kA(a), isC = cur && kA(cur) === k, isT = kA(T) === k; return `<div class="${visited[k] ? 'vis' : ''} ${isC ? 'cur' : ''} ${isT ? 'tgt' : ''}">${NAME(a)}<small>${visited[k] ? inr(value(a)) : isT ? '🎯 ?' : '?'}</small></div>`; };
          body.innerHTML = `<div class="lb-circularflow-data">${ex ? '' : inc ? '' : `<span>GDP<sub>MP</sub> ${inr(gdpmp)}</span>`}<span>Depreciation ${inr(dep)}</span><span>NFIA ${inr(nfia)}</span><span>NIT ${it != null ? `= ${inr(it)} − ${inr(sub)} = ` : ''}${inr(nit)}</span><span style="background:none;color:#6b7090">${esc(unit)}</span></div>
<div class="lb-circularflow-grid">${[true, false].map(mp => ORDER.map(o => cell({ g: o.g, n: o.n, mp })).join('')).join('')}</div>
${pending ? `<div class="lb-circularflow-pend"><span style="flex:1;min-width:150px">${NAME(pending.to)} = ${pending.label} =</span><input inputmode="decimal" placeholder="?"><button class="lb-circularflow-btn ok2">✓</button></div>` : ''}
<div class="lb-circularflow-ops">${OPS.map((o, i) => `<button data-o="${i}" ${pending || !cur ? 'disabled style="opacity:.45"' : ''}>${o[2]}<small>${o[3]}</small></button>`).join('')}</div>
<div class="lb-circularflow-der" ${steps.length ? '' : 'hidden'}>${steps.map(s => `<div><span>${s[0]}</span><b>${inr(s[1])}</b></div>`).join('')}</div>
<div class="lb-circularflow-msg ${cls || ''}">${m || (pending ? 'Type the value and press ✓.' : 'Tap an operation to move to the next aggregate.')}</div>`;
          const inp = body.querySelector('.lb-circularflow-pend input'); if (inp && !('ontouchstart' in window)) inp.focus({ preventScroll: true });
          const der = body.querySelector('.lb-circularflow-der'); der.scrollTop = der.scrollHeight;
        }
        function op(i) {
          const [what, sgn, label] = OPS[i], a = Object.assign({}, cur);
          const bad = what === 'dep' ? (sgn < 0 ? !a.g : a.g) : what === 'nfia' ? (sgn > 0 ? a.n : !a.n) : (sgn < 0 ? !a.mp : a.mp);
          if (bad) { api.sfx && api.sfx('hmm'); draw(what === 'dep' ? (sgn < 0 ? 'Already NET — depreciation is already subtracted. Net = Gross − Depreciation.' : 'Already GROSS — it includes depreciation.') : what === 'nfia' ? (sgn > 0 ? 'Already NATIONAL — NFIA is already added. National = Domestic + NFIA.' : 'Already DOMESTIC.') : (sgn < 0 ? 'Already at FACTOR COST. FC = MP − Net indirect taxes.' : 'Already at MARKET PRICE.'), 'bad'); return; }
          const to = Object.assign({}, a); if (what === 'dep') to.g = sgn > 0; if (what === 'nfia') to.n = sgn > 0; if (what === 'nit') to.mp = sgn > 0;
          const amt = what === 'dep' ? dep : what === 'nfia' ? nfia : nit;
          pending = { to, label: `${NAME(a)} ${inr(value(a))} ${sgn > 0 ? '+' : '−'} ${label.replace(/^[+−] /, '')} ${amt < 0 ? `(${inr(amt)})` : inr(amt)}` };
          api.sfx && api.sfx('tap'); draw();
        }
        function submit() {
          const inp = body.querySelector('.lb-circularflow-pend input'), v = num(inp && inp.value), want = value(pending.to);
          if (!isFinite(v)) { draw('Type a number first.', 'bad'); return; }
          if (Math.abs(v - want) > 0.5) { api.sfx && api.sfx('wrong'); draw(`Not quite — check the arithmetic${nfia < 0 && /NFIA/.test(pending.label) ? ' (NFIA is negative here!)' : ''}.`, 'bad'); return; }
          cur = pending.to; visited[kA(cur)] = 1; steps.push([`${NAME(cur)} = ${pending.short || pending.label}`, want]); pending = null; api.sfx && api.sfx('coin');
          if (kA(cur) === kA(T)) { draw(`✔ ${NAME(T)} = ${inr(want)} (${esc(unit)})${kA(T) === 'NNPfc' ? ' — this is National Income.' : ''}`, 'ok'); win(`${TXT(T)} = ${inr(want)} (${unit}) — derived step by step`); return; }
          draw(`✔ ${NAME(cur)} = ${inr(want)}. Keep going to ${NAME(T)}.`, 'ok');
        }
        body.addEventListener('click', e => { const b = e.target.closest('button'); if (!b || b.disabled) return; if (b.dataset.o != null) op(+b.dataset.o); else if (b.classList.contains('ok2')) submit(); });
        body.addEventListener('keydown', e => { if (e.key === 'Enter' && pending) submit(); });
        draw();
      }
      ({ flow, multiplier, national })[mode]();
      return () => { cancelAnimationFrame(raf); timers.forEach(clearTimeout); host.innerHTML = ''; };
    },
    example: {
      mode: 'flow', unit: '₹ crore', sectors: ['financial', 'government', 'foreign'],
      start: { I: 100, G: 60, X: 40, s: 0.1, t: 0.1, m: 0.05 }, targetY: 1000,
      challenge: 'Income is ₹800 crore. Change leakages or injections so it settles at ₹1,000 crore'
    },
    examples: [
      { mode: 'multiplier', unit: '₹ crore', mpc: 0.5, dI: 100, lock: 'dI', target: { dY: 400 },
        challenge: 'Investment rises by ₹100 crore. Find the MPC that raises income by ₹400 crore' },
      { mode: 'national', unit: '₹ crore', gdpmp: 12000, dep: 1200, nfia: -300, indirectTaxes: 1100, subsidies: 200, target: 'NNPfc',
        challenge: 'From GDP at market price, calculate National Income (NNPFC)' },
      { mode: 'national', unit: '₹ crore', expenditure: { C: 4000, I: 1200, G: 900, X: 500, M: 600 }, dep: 300, nfia: 50, nit: 400, target: 'NNPfc',
        challenge: 'Expenditure method: find GDPMP, then National Income (NNPFC)' }
    ]
  });
})();
