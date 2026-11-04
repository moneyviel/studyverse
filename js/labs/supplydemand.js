/* StudyVerse Concept Lab: supplydemand — a market with straight-line demand and supply curves.
   Quantity demanded  Qd = a − b·P      Quantity supplied  Qs = c + d·P   (negative values shown as 0)
   Equilibrium        P* = (a − c) / (b + d),  Q* = a − b·P*

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title       string  Heading text.                                         'Market for onions'
   good        string  Name of the item.                                     'onions'
   emoji       string  Item emoji.                                           '🧅'
   unit        string  Quantity unit label.                                  'kg'
   currency    string  Money symbol.                                         '₹'
   demand      object  {a, b}: Qd = a − b·P.                                 {a:100, b:1}
   supply      object  {c, d}: Qs = c + d·P.                                 {c:-20, d:2}
   price       object  Slider {min, max, step, start}.                       {min:10,max:80,step:5,start:15}
   task        string  'equilibrium' | 'shortage' | 'surplus' | 'shift'.     'equilibrium'
                       shortage/surplus: set a price that makes a gap of at least `target` units.
                       shift: move a curve (income / cost) and then find the NEW equilibrium.
   target      number  Gap size for shortage/surplus tasks.                  20
   shift       boolean Show the shift sliders (always on for task 'shift').  false
   incomeStep  number  Units the demand curve moves right per income step.   15
   costStep    number  Units the supply curve moves LEFT per cost step.      15
   start       object  Starting shift steps {income, cost} (−2…2).          {income:0, cost:0}
   labels      object  {income, cost} slider names (any language).           {income:"Buyers' income", cost:'Cost of making'}
   tol         number  Price tolerance for equilibrium.                      price.step / 2
   challenge   string  Challenge text (else generated).

   What the child does: drags the price (slider or the dashed price line on the graph) and sees how
   much buyers want vs sellers offer, the shortage/surplus gap and which way the price will be pushed;
   in shift mode they change income / cost and watch the curve move and the equilibrium change.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const r1 = v => Math.round(v * 10) / 10;
  Labs.register('supplydemand', {
    title: 'Supply and demand', subjects: ['economics', 'social', 'maths'],
    render(host, p, api) {
      const ex = this.example || {};
      const D = Object.assign({}, ex.demand, p.demand), S = Object.assign({}, ex.supply, p.supply), PR = Object.assign({}, ex.price, p.price);
      const cur = p.currency || '₹', unit = p.unit || 'units', good = p.good || 'goods', emoji = p.emoji || '🛒';
      const task = ['equilibrium', 'shortage', 'surplus', 'shift'].includes(p.task) ? p.task : 'equilibrium';
      const showShift = task === 'shift' || !!p.shift;
      const iStep = isFinite(+p.incomeStep) ? +p.incomeStep : 15, cStep = isFinite(+p.costStep) ? +p.costStep : 15;
      const lab = Object.assign({ income: "Buyers' income", cost: 'Cost of making' }, p.labels || {});
      const st = Object.assign({ income: 0, cost: 0 }, p.start || {});
      const pmin = +PR.min, pmax = +PR.max, pstep = +PR.step > 0 ? +PR.step : 1;
      const tol = +p.tol > 0 ? +p.tol : pstep / 2 + 1e-9, target = +p.target > 0 ? +p.target : 20;
      let P = Math.min(pmax, Math.max(pmin, isFinite(+PR.start) ? +PR.start : pmin)), inc = +st.income || 0, cost = +st.cost || 0, won = false, dragging = false, touched = false;
      const A = () => +D.a + inc * iStep, C = () => +S.c - cost * cStep;
      const Qd = pr => Math.max(0, A() - D.b * pr), Qs = pr => Math.max(0, C() + S.d * pr);
      const eqP = () => (A() - C()) / (+D.b + +S.d), eqQ = () => A() - D.b * eqP();
      /* x-axis max: biggest quantity reached anywhere in the allowed shifts */
      const sh = showShift ? 2 : 0, qmaxRaw = Math.max(10, 1.2 * Math.max(+D.a + sh * Math.abs(iStep) - D.b * pmin, Math.min(+S.c + sh * Math.abs(cStep) + S.d * pmax, +D.a + sh * Math.abs(iStep))));
      const qStep = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 5000].find(s => qmaxRaw / s <= 7) || 10000, QM = Math.ceil(qmaxRaw / qStep) * qStep;
      const chText = p.challenge || ({ equilibrium: `Find the price where buyers want exactly what sellers offer (equilibrium)`, shortage: `Set a price that causes a shortage of at least ${target} ${unit}`, surplus: `Set a price that causes a surplus of at least ${target} ${unit}`, shift: `Change income or cost, then find the NEW equilibrium price` })[task];
      const VW = 340, VH = showShift ? 200 : 220, L = 40, Rr = 12, T = 22, B = 32, GW = VW - L - Rr, GH = VH - T - B;
      const X = q => L + q / QM * GW, Y = pr => T + (pmax - pr) / (pmax - pmin) * GH;

      host.innerHTML = `<div class="lb-supplydemand-w"><style>
.lb-supplydemand-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-supplydemand-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-supplydemand-g{background:#f7f8ff;border-radius:16px;padding:2px}
.lb-supplydemand-g svg{display:block;width:100%;height:auto;touch-action:none}
.lb-supplydemand-ax{font-size:10px;font-weight:700;fill:#6b7090}
.lb-supplydemand-at{font-size:10.5px;font-weight:800;fill:#1b1f3a}
.lb-supplydemand-row{display:flex;align-items:center;gap:8px;margin-top:6px;font-weight:800;font-size:13px}
.lb-supplydemand-row input{flex:1;height:32px;accent-color:#8b5cf6}
.lb-supplydemand-row .v{min-width:58px;text-align:right;font-size:16px;color:#8b5cf6}
.lb-supplydemand-row .n{min-width:104px;font-size:12.5px}
.lb-supplydemand-row .s{min-width:30px;text-align:right;color:#6b7090;font-size:12px}
.lb-supplydemand-cards{display:flex;gap:6px;margin-top:6px}
.lb-supplydemand-cards div{flex:1;border-radius:12px;padding:5px 4px;text-align:center;font-weight:800;font-size:16px;line-height:1.1;background:#f6f7ff}
.lb-supplydemand-cards small{display:block;font-size:10.5px;color:#6b7090;font-weight:700;margin-top:2px}
.lb-supplydemand-cards .d{background:#eaf2ff;color:#2f6fd6}.lb-supplydemand-cards .s{background:#fff0f0;color:#e04848}
.lb-supplydemand-cards .gap.sh{background:#fff6dc;color:#b57f00}.lb-supplydemand-cards .gap.su{background:#f1ecff;color:#7044e0}.lb-supplydemand-cards .gap.eq{background:#e3fbf3;color:#0f7a5c}
.lb-supplydemand-msg{margin-top:6px;font-weight:800;font-size:13px;line-height:1.3;min-height:34px}
</style>
<div class="lb-supplydemand-ch">🎯 Challenge: ${esc(chText)}</div>
<div class="lb-supplydemand-g"><svg viewBox="0 0 ${VW} ${VH}"></svg></div>
<div class="lb-supplydemand-row">${esc(emoji)} Price <input class="pr" type="range" min="${pmin}" max="${pmax}" step="${pstep}" value="${P}"><span class="v"></span></div>
<div class="lb-supplydemand-cards"><div class="d"></div><div class="s"></div><div class="gap"></div></div>
${showShift ? `<div class="lb-supplydemand-row"><span class="n">💰 ${esc(lab.income)}</span><input class="inc" type="range" min="-2" max="2" step="1" value="${inc}"><span class="s si"></span></div>
<div class="lb-supplydemand-row"><span class="n">🏭 ${esc(lab.cost)}</span><input class="cost" type="range" min="-2" max="2" step="1" value="${cost}"><span class="s sc"></span></div>` : ''}
<div class="lb-supplydemand-msg"></div></div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), prIn = $('.pr'), msg = $('.lb-supplydemand-msg');
      const startShift = { inc, cost };
      function line(f, pts) { return pts.map((pr, i) => `${i ? 'L' : 'M'}${X(f(pr)).toFixed(1)} ${Y(pr).toFixed(1)}`).join(''); }
      function curvePts(f) { const out = []; for (let i = 0; i <= 60; i++) out.push(pmin + (pmax - pmin) * i / 60); return out.filter(pr => f(pr) <= QM); }
      function draw() {
        const qd = Qd(P), qs = Qs(P), y = Y(P), pe = eqP(), qe = eqQ();
        let s = '';
        for (let q = 0; q <= QM; q += qStep) s += `<line x1="${X(q)}" x2="${X(q)}" y1="${T}" y2="${T + GH}" stroke="#e3e6f7"/><text class="lb-supplydemand-ax" x="${X(q)}" y="${T + GH + 12}" text-anchor="middle">${q}</text>`;
        const ps = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000].find(k => (pmax - pmin) / k <= 6) || 1000;
        for (let pr = Math.ceil(pmin / ps) * ps; pr <= pmax; pr += ps) s += `<line x1="${L}" x2="${L + GW}" y1="${Y(pr)}" y2="${Y(pr)}" stroke="#e3e6f7"/><text class="lb-supplydemand-ax" x="${L - 4}" y="${Y(pr) + 3}" text-anchor="end">${esc(cur)}${pr}</text>`;
        s += `<line x1="${L}" x2="${L}" y1="${T}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${L}" x2="${L + GW}" y1="${T + GH}" y2="${T + GH}" stroke="#1b1f3a" stroke-width="1.5"/>`;
        s += `<text class="lb-supplydemand-at" x="${L + GW}" y="${VH - 3}" text-anchor="end">Quantity (${esc(unit)}) →</text><text class="lb-supplydemand-at" x="4" y="11">Price (${esc(cur)}) ↑</text>`;
        /* ghost of the original curves when shifted */
        if (inc !== 0) s += `<path d="${line(pr => Math.max(0, +D.a - D.b * pr), curvePts(pr => Math.max(0, +D.a - D.b * pr)))}" fill="none" stroke="#3b82f6" stroke-width="2" opacity=".25" stroke-dasharray="4 4"/>`;
        if (cost !== 0) s += `<path d="${line(pr => Math.max(0, +S.c + S.d * pr), curvePts(pr => Math.max(0, +S.c + S.d * pr)))}" fill="none" stroke="#ff6b6b" stroke-width="2" opacity=".25" stroke-dasharray="4 4"/>`;
        /* gap band */
        if (Math.abs(qd - qs) > 1e-9) { const a = X(Math.min(qd, qs)), b = X(Math.max(qd, qs)); s += `<rect x="${a}" y="${y - 7}" width="${b - a}" height="14" rx="7" fill="${qd > qs ? '#ffc93c' : '#c4b5fd'}" opacity=".55"/><text class="lb-supplydemand-at" x="${(a + b) / 2}" y="${y > T + 24 ? y - 11 : y + 20}" text-anchor="middle">${qd > qs ? 'Shortage' : 'Surplus'} ${r1(Math.abs(qd - qs))}</text>`; }
        const dP = curvePts(Qd), sP = curvePts(Qs);
        s += `<path d="${line(Qd, dP)}" fill="none" stroke="#3b82f6" stroke-width="3.2" stroke-linecap="round"/><path d="${line(Qs, sP)}" fill="none" stroke="#ff6b6b" stroke-width="3.2" stroke-linecap="round"/>`;
        const dl = dP[dP.length - 1] != null ? dP[dP.length - 1] : pmax, sl = sP[sP.length - 1] != null ? sP[sP.length - 1] : pmax;
        s += `<text class="lb-supplydemand-at" fill="#2f6fd6" style="fill:#2f6fd6" x="${X(Qd(pmax - (pmax - pmin) * .04)) + 5}" y="${Y(pmax) + 12}">D</text>`;
        s += `<text class="lb-supplydemand-at" style="fill:#e04848" x="${Math.min(L + GW - 8, X(Qs(sl)) + 5)}" y="${Y(sl) + 12}">S</text>`;
        if (won && pe >= pmin && pe <= pmax) s += `<g><line x1="${L}" x2="${X(qe)}" y1="${Y(pe)}" y2="${Y(pe)}" stroke="#2ed3a5" stroke-dasharray="3 3"/><line x1="${X(qe)}" x2="${X(qe)}" y1="${Y(pe)}" y2="${T + GH}" stroke="#2ed3a5" stroke-dasharray="3 3"/><text x="${X(qe)}" y="${Y(pe) + 5}" font-size="14" text-anchor="middle">⭐</text></g>`;
        /* price line (draggable) */
        s += `<line x1="${L}" x2="${L + GW}" y1="${y}" y2="${y}" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 4"/><rect class="hit" x="${L}" y="${y - 16}" width="${GW}" height="32" fill="transparent" style="cursor:ns-resize"/>`;
        s += `<g transform="translate(${L + GW - 2},${y})"><rect x="-44" y="-11" width="44" height="22" rx="11" fill="#8b5cf6"/><text x="-22" y="4" text-anchor="middle" font-size="11" font-weight="800" fill="#fff">${esc(cur)}${r1(P)}</text></g>`;
        s += `<circle cx="${X(qd)}" cy="${y}" r="5.5" fill="#3b82f6" stroke="#fff" stroke-width="2"/><circle cx="${X(qs)}" cy="${y}" r="5.5" fill="#ff6b6b" stroke="#fff" stroke-width="2"/>`;
        svg.innerHTML = s;
        $('.lb-supplydemand-row .v').textContent = cur + r1(P);
        $('.lb-supplydemand-cards .d').innerHTML = `${r1(qd)}<small>buyers want (${esc(unit)})</small>`;
        $('.lb-supplydemand-cards .s').innerHTML = `${r1(qs)}<small>sellers offer (${esc(unit)})</small>`;
        const g = $('.lb-supplydemand-cards .gap'), gap = qd - qs, eqNow = Math.abs(P - pe) <= tol;
        g.className = 'gap ' + (eqNow ? 'eq' : gap > 0 ? 'sh' : 'su');
        g.innerHTML = eqNow ? `0 ⚖️<small>equilibrium!</small>` : `${r1(Math.abs(gap))}<small>${gap > 0 ? 'shortage' : 'surplus'}</small>`;
        if (showShift) { const f = v => v > 0 ? '+' + v : '' + v; $('.si').textContent = f(inc); $('.sc').textContent = f(cost); }
        if (dragging) return;
        let m = eqNow ? `⚖️ At ${cur}${r1(P)} buyers want ${r1(qd)} ${unit} and sellers offer ${r1(qs)} — the market clears.`
          : gap > 0 ? `🔥 Shortage: buyers want ${r1(gap)} ${unit} more than sellers offer, so the price tends to RISE ⬆️`
            : `📦 Surplus: ${r1(-gap)} ${unit} left unsold, so the price tends to FALL ⬇️`;
        if (!won && touched) {
          let ok = false;
          if (task === 'equilibrium') ok = eqNow;
          else if (task === 'shortage') ok = gap >= target - 1e-9;
          else if (task === 'surplus') ok = -gap >= target - 1e-9;
          else ok = (inc !== startShift.inc || cost !== startShift.cost || inc !== 0 || cost !== 0) && eqNow;
          if (task === 'shift' && eqNow && inc === 0 && cost === 0) m += ' Now move a curve with income or cost!';
          if (ok) {
            won = true; api.sfx('correct');
            const msgs = { equilibrium: `Equilibrium! At ${cur}${r1(pe)} both buyers and sellers want ${r1(eqQ())} ${unit}.`, shortage: `Shortage of ${r1(gap)} ${unit} at ${cur}${r1(P)} — prices that are too low cause shortages!`, surplus: `Surplus of ${r1(-gap)} ${unit} at ${cur}${r1(P)} — prices that are too high leave goods unsold!`, shift: `New equilibrium: ${cur}${r1(pe)} and ${r1(eqQ())} ${unit}. Shifting a curve moves the equilibrium!` };
            api.win(msgs[task]); draw(); return;
          }
        }
        msg.textContent = m;
      }
      function setP(v) { P = Math.min(pmax, Math.max(pmin, Math.round((v - pmin) / pstep) * pstep + pmin)); prIn.value = P; touched = true; draw(); }
      prIn.addEventListener('input', () => { touched = true; setP(+prIn.value); });
      const toPrice = ev => { const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY; const q = pt.matrixTransform(svg.getScreenCTM().inverse()); return pmax - (q.y - T) / GH * (pmax - pmin); };
      const onDown = ev => { if (!ev.target.classList || !ev.target.classList.contains('hit')) { const pr = toPrice(ev); if (Math.abs(Y(pr) - Y(P)) > 40) return; } dragging = true; svg.setPointerCapture && svg.setPointerCapture(ev.pointerId); setP(toPrice(ev)); };
      const onMove = ev => { if (dragging) setP(toPrice(ev)); };
      const onUp = () => { if (!dragging) return; dragging = false; draw(); };
      svg.addEventListener('pointerdown', onDown); svg.addEventListener('pointermove', onMove); svg.addEventListener('pointerup', onUp); svg.addEventListener('pointercancel', onUp);
      if (showShift) {
        $('.inc').addEventListener('input', e => { inc = +e.target.value; touched = true; api.sfx('tap'); draw(); });
        $('.cost').addEventListener('input', e => { cost = +e.target.value; touched = true; api.sfx('tap'); draw(); });
      }
      draw();
      return () => { svg.removeEventListener('pointerdown', onDown); };
    },
    example: {
      title: 'Market for onions', good: 'onions', emoji: '🧅', unit: 'kg', currency: '₹',
      demand: { a: 100, b: 1 }, supply: { c: -20, d: 2 }, price: { min: 10, max: 80, step: 5, start: 15 },
      task: 'equilibrium', challenge: 'Slide the price of onions until buyers want exactly what sellers offer'
    },
    examples: [
      { title: 'Lemonade stall (Class 4-5)', good: 'glasses of lemonade', emoji: '🍋', unit: 'glasses', currency: '₹',
        demand: { a: 70, b: 2 }, supply: { c: -10, d: 2 }, price: { min: 5, max: 30, step: 1, start: 28 }, task: 'shortage', target: 20,
        challenge: 'Set a price so low that 20 or more glasses are missing (a shortage)' },
      { title: 'Mangoes after a storm (Class 11-12)', good: 'mangoes', emoji: '🥭', unit: 'kg', currency: '₹',
        demand: { a: 100, b: 1 }, supply: { c: -20, d: 2 }, price: { min: 10, max: 80, step: 5, start: 40 }, task: 'shift', shift: true,
        start: { income: 0, cost: 1 }, incomeStep: 15, costStep: 15, labels: { income: "Buyers' income", cost: 'Cost (storm)' },
        challenge: 'A storm raised costs, so supply moved left. Find the NEW equilibrium price' }
    ]
  });
})();
