/* StudyVerse Concept Lab: budget — plan a monthly budget (needs / wants / savings pie) and
   watch money grow with simple vs compound interest.

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title      string   Heading text.                                          'Family budget'
   mode       string   Starting mode: 'budget' | 'interest'.                  'budget'
   modes      string[] Tabs to show (one entry = no tabs).                    [mode]
   currency   string   Money symbol.                                          '₹'
   income     number   Monthly income / pocket money to share out.           30000
   incomeRange object  {min, max, step} → income becomes a slider; omit to keep it fixed.
   step       number   Slider step for items.                                 500
   items      object[] {name, emoji?, kind:'need'|'want'|'save', amount, min?}. min = cannot go lower
                       (e.g. rent). Default: Needs / Wants / Savings.
   goal       object   budget win rule — all given parts must be true:
                       {save: min % saved, needsMax: max % on needs, wantsMax: max % on wants,
                        plan: true → every rupee planned (nothing left)}.   {save:20, plan:true}
   principal  object   interest: {min, max, step, value} (₹).                {1000…100000, 10000}
   rate       object   interest: {min, max, step, value} (% per year).       {1…20, 8}
   years      object   interest: {min, max, step, value}.                    {1…20, 3}
   igoal      object   interest win rule: {kind:'ci'|'si', times: n} → amount ≥ n × principal,
                       or {kind, amount: X} → amount ≥ X, or {kind, interest: X} → interest = X exactly.
                       Default {kind:'ci', times:2}.
   challenge  string   Challenge text for the starting mode (else generated).

   What the child does: budget = move sliders to share the income between needs, wants and savings,
   seeing the pie, % and a live checklist; interest = slide principal, rate and years and compare
   Simple Interest (P×R×T/100) with Compound Interest (P(1+R/100)^T − P) on a growth chart.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const KC = { need: ['#3b82f6', '#60a5fa', '#1d4ed8', '#93c5fd'], want: ['#ff9f43', '#ff6b6b', '#ffc93c', '#f472b6'], save: ['#2ed3a5', '#14b8a6', '#86efac'] };
  const KN = { need: 'Needs', want: 'Wants', save: 'Savings' };
  const MODES = { budget: '🥧 Budget', interest: '📈 Interest' };
  Labs.register('budget', {
    title: 'Budget & interest', subjects: ['maths', 'economics', 'social', 'life skills'],
    render(host, p, api) {
      const ex = this.example || {};
      const cur = p.currency || '₹';
      const money = v => cur + Math.round(v).toLocaleString('en-IN');
      const money2 = v => cur + (Math.round(v * 100) / 100).toLocaleString('en-IN', { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 });
      const modes = (Array.isArray(p.modes) && p.modes.length ? p.modes : [p.mode || 'budget']).filter(m => MODES[m]);
      if (!modes.length) modes.push('budget');
      let mode = modes.includes(p.mode) ? p.mode : modes[0];
      const step = +p.step > 0 ? +p.step : 500;
      let income = +p.income > 0 ? +p.income : 30000;
      const IR = p.incomeRange && +p.incomeRange.max > 0 ? { min: +p.incomeRange.min || 0, max: +p.incomeRange.max, step: +p.incomeRange.step || step } : null;
      const items = (Array.isArray(p.items) && p.items.length ? p.items : ex.items).map((it, i) => ({ name: it.name || 'Item', emoji: it.emoji || '', kind: KC[it.kind] ? it.kind : 'need', amount: Math.max(0, +it.amount || 0), min: Math.max(0, +it.min || 0) }));
      const kindCount = {}; items.forEach(it => { const k = kindCount[it.kind] || 0; it.col = KC[it.kind][k % KC[it.kind].length]; kindCount[it.kind] = k + 1; });
      const start = items.map(it => it.amount);
      const goal = p.goal && typeof p.goal === 'object' ? p.goal : { save: 20, plan: true };
      const rng = (o, d) => { o = Object.assign({}, d, o || {}); o.value = Math.min(+o.max, Math.max(+o.min, +o.value)); return o; };
      const PR = rng(p.principal, { min: 1000, max: 100000, step: 1000, value: 10000 }), RR = rng(p.rate, { min: 1, max: 20, step: 0.5, value: 8 }), YR = rng(p.years, { min: 1, max: 20, step: 1, value: 3 });
      const ig = Object.assign({ kind: 'ci' }, p.igoal && typeof p.igoal === 'object' ? p.igoal : { times: 2 });
      let P0 = +PR.value, R = +RR.value, T = +YR.value, won = false, touched = false;

      host.innerHTML = `<div class="lb-budget-w"><style>
.lb-budget-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-budget-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-budget-tabs{display:flex;gap:6px;margin-bottom:6px}
.lb-budget-tabs button{flex:1;min-height:40px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:13px;cursor:pointer}
.lb-budget-tabs button.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-budget-inc{display:flex;align-items:center;gap:8px;background:#f6f7ff;border-radius:12px;padding:6px 10px;font-weight:800;font-size:13px}
.lb-budget-inc b{font-size:16px;color:#8b5cf6;margin-left:auto}
.lb-budget-inc input{flex:1}
.lb-budget-top{display:flex;gap:10px;align-items:center;margin-top:6px}
.lb-budget-top svg{width:112px;height:112px;flex:none}
.lb-budget-chk{flex:1;font-size:12.5px;font-weight:800;line-height:1.25}
.lb-budget-chk div{display:flex;gap:6px;align-items:flex-start;margin:3px 0}
.lb-budget-chk .ok{color:#0f7a5c}.lb-budget-chk .no{color:#c94f4f}
.lb-budget-pct{display:flex;gap:4px;margin-bottom:4px}
.lb-budget-pct span{flex:1;border-radius:8px;padding:3px 2px;text-align:center;font-size:11px;line-height:1.2;font-weight:800;color:#fff}
.lb-budget-it{display:flex;align-items:center;gap:6px;margin-top:0;font-weight:800;font-size:12.5px}
.lb-budget-it .n{width:98px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-budget-it .sw{width:10px;height:10px;border-radius:3px;flex:none}
.lb-budget-it input{flex:1;height:28px;min-width:0}
.lb-budget-it .v{width:64px;text-align:right}
.lb-budget-w input[type=range]{accent-color:#8b5cf6}
.lb-budget-msg{flex:1;margin-top:6px;font-weight:800;font-size:13px;line-height:1.3;min-height:20px}
.lb-budget-row{display:flex;align-items:center;gap:6px;margin-top:3px;font-weight:800;font-size:12.5px}
.lb-budget-row .n{width:84px}.lb-budget-row input{flex:1;height:30px;min-width:0}.lb-budget-row .v{width:72px;text-align:right;color:#8b5cf6;font-size:14px}
.lb-budget-cards{display:flex;gap:6px;margin-top:6px}
.lb-budget-cards div{flex:1;border-radius:12px;padding:5px 6px;font-weight:800;font-size:14px;line-height:1.15}
.lb-budget-cards small{display:block;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:700;opacity:.8}
.lb-budget-cards .si{background:#eaf2ff;color:#2f6fd6}.lb-budget-cards .ci{background:#e3fbf3;color:#0f7a5c}
.lb-budget-chart{background:#f7f8ff;border-radius:14px;margin-top:6px}
.lb-budget-chart svg{display:block;width:100%;height:auto}
.lb-budget-btn{min-height:40px;border:none;border-radius:12px;padding:0 12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;cursor:pointer;box-shadow:0 3px 0 #d3d7ef}
</style>
<div class="lb-budget-ch"></div>
${modes.length > 1 ? `<div class="lb-budget-tabs">${modes.map(m => `<button data-m="${m}">${MODES[m]}</button>`).join('')}</div>` : ''}
<div class="lb-budget-body"></div><div style="display:flex;align-items:center;gap:8px"><div class="lb-budget-msg"></div><button class="lb-budget-btn rs">⟲ Reset</button></div></div>`;
      const $ = s => host.querySelector(s), body = $('.lb-budget-body'), msg = $('.lb-budget-msg');
      function chText() {
        if (p.challenge && mode === (modes.includes(p.mode) ? p.mode : modes[0])) return p.challenge;
        if (mode === 'budget') { const parts = []; if (goal.save != null) parts.push(`save at least ${goal.save}%`); if (goal.needsMax != null) parts.push(`keep needs ≤ ${goal.needsMax}%`); if (goal.wantsMax != null) parts.push(`keep wants ≤ ${goal.wantsMax}%`); if (goal.plan) parts.push('plan every rupee'); return 'Make a budget that will ' + (parts.join(', ') || 'balance'); }
        const k = ig.kind === 'si' ? 'simple' : 'compound';
        if (ig.interest != null) return `Find a rate and time that give exactly ${money(ig.interest)} ${k} interest`;
        if (ig.amount != null) return `Grow your money to ${money(ig.amount)} or more with ${k} interest`;
        return `Find how many years it takes to make your money ${ig.times || 2}× bigger with ${k} interest`;
      }
      /* ---------------- budget ---------------- */
      function sums() { const s = { need: 0, want: 0, save: 0 }; items.forEach(it => s[it.kind] += it.amount); s.total = s.need + s.want + s.save; s.left = income - s.total; return s; }
      function arc(cx, cy, r, a0, a1) { if (a1 - a0 >= Math.PI * 2 - 1e-6) return `M${cx - r} ${cy}A${r} ${r} 0 1 1 ${cx + r} ${cy}A${r} ${r} 0 1 1 ${cx - r} ${cy}Z`; const p0 = [cx + r * Math.sin(a0), cy - r * Math.cos(a0)], p1 = [cx + r * Math.sin(a1), cy - r * Math.cos(a1)]; return `M${cx} ${cy}L${p0[0]} ${p0[1]}A${r} ${r} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${p1[0]} ${p1[1]}Z`; }
      function buildBudget() {
        body.innerHTML = `<div class="lb-budget-inc">💼 Income / month ${IR ? `<input class="inc" type="range" min="${IR.min}" max="${IR.max}" step="${IR.step}" value="${income}">` : ''}<b class="iv"></b></div>
<div class="lb-budget-top"><svg viewBox="0 0 128 128"></svg><div class="lb-budget-chk"></div></div>
${items.map((it, i) => `<div class="lb-budget-it"><span class="sw" style="background:${it.col}"></span><span class="n">${esc((it.emoji ? it.emoji + ' ' : '') + it.name)}</span><input data-i="${i}" type="range" min="0" max="${income}" step="${step}" value="${it.amount}"><span class="v"></span></div>`).join('')}`;
        body.querySelectorAll('.lb-budget-it input').forEach(inp => inp.addEventListener('input', () => {
          const it = items[+inp.dataset.i], others = sums().total - it.amount;
          it.amount = Math.max(it.min, Math.min(+inp.value, income - others)); if (+inp.value !== it.amount) inp.value = it.amount;
          touched = true; updBudget();
        }));
        const ii = body.querySelector('.inc'); if (ii) ii.addEventListener('input', () => {
          income = +ii.value; let s = sums();
          /* if income shrinks below the plan, trim wants, then savings, then needs (never below min) */
          for (const k of ['want', 'save', 'need']) for (const it of items.slice().reverse()) { if (s.left >= 0) break; if (it.kind !== k) continue; const cut = Math.min(-s.left, it.amount - it.min); it.amount -= cut; s = sums(); }
          body.querySelectorAll('.lb-budget-it input').forEach(inp => { inp.max = income; inp.value = items[+inp.dataset.i].amount; });
          touched = true; updBudget();
        });
                updBudget();
      }
      function updBudget() {
        const s = sums(), pc = v => income > 0 ? v / income * 100 : 0, f1 = v => (Math.round(v * 10) / 10) + '%';
        $('.iv').textContent = money(income);
        let a = 0, svg = '';
        items.forEach(it => { if (it.amount <= 0 || income <= 0) return; const da = it.amount / income * Math.PI * 2; svg += `<path d="${arc(64, 64, 60, a, a + da)}" fill="${it.col}" stroke="#fff" stroke-width="1.5"/>`; a += da; });
        if (s.left > 0 && income > 0) svg += `<path d="${arc(64, 64, 60, a, Math.PI * 2)}" fill="#e7e9f5" stroke="#fff" stroke-width="1.5"/>`;
        svg += `<circle cx="64" cy="64" r="30" fill="#fff"/><text x="64" y="61" text-anchor="middle" font-size="10" font-weight="800" fill="#6b7090">${s.left > 0 ? 'left' : s.left < 0 ? 'overspent' : 'all planned'}</text><text x="64" y="76" text-anchor="middle" font-size="${s.left === 0 ? 16 : 13}" font-weight="800" fill="${s.left > 0 ? '#1b1f3a' : s.left < 0 ? '#d63c4a' : '#0f7a5c'}">${s.left > 0 ? money(s.left) : s.left < 0 ? money(-s.left) : '✓'}</text>`;
        body.querySelector('.lb-budget-top svg').innerHTML = svg;
        const checks = [];
        if (goal.save != null) checks.push([pc(s.save) >= +goal.save - 1e-9, `Savings ${f1(pc(s.save))} (need ≥ ${goal.save}%)`]);
        if (goal.needsMax != null) checks.push([pc(s.need) <= +goal.needsMax + 1e-9, `Needs ${f1(pc(s.need))} (≤ ${goal.needsMax}%)`]);
        if (goal.wantsMax != null) checks.push([pc(s.want) <= +goal.wantsMax + 1e-9, `Wants ${f1(pc(s.want))} (≤ ${goal.wantsMax}%)`]);
        if (goal.plan) checks.push([s.left === 0, s.left === 0 ? 'Every rupee planned' : `${money(s.left)} not planned yet`]);
        const kinds = ['need', 'want', 'save'].filter(k => items.some(it => it.kind === k));
        body.querySelector('.lb-budget-chk').innerHTML = `<div class="lb-budget-pct">${kinds.map(k => `<span style="background:${KC[k][0]}">${KN[k]} ${Math.round(pc(s[k]))}%</span>`).join('')}</div>` + checks.map(([ok, t]) => `<div class="${ok ? 'ok' : 'no'}">${ok ? '✅' : '⬜'} <span>${esc(t)}</span></div>`).join('');
        body.querySelectorAll('.lb-budget-it').forEach((row, i) => { row.querySelector('.v').textContent = money(items[i].amount); });
        const allOk = checks.length && checks.every(c => c[0]);
        if (allOk && touched && !won) { won = true; api.sfx('correct'); api.win(`Great budget! You save ${f1(pc(s.save))} — ${money(s.save)} a month, ${money(s.save * 12)} a year.`); }
        msg.textContent = allOk ? `🎉 Saving ${money(s.save)} a month = ${money(s.save * 12)} in a year!` : s.left < 0 ? 'You are spending more than you earn!' : 'Move the sliders to share out the money.';
      }
      /* ---------------- interest ---------------- */
      function buildInterest() {
        const row = (k, label, o, unit) => `<div class="lb-budget-row"><span class="n">${label}</span><input data-k="${k}" type="range" min="${o.min}" max="${o.max}" step="${o.step}" value="${o.value}"><span class="v" data-v="${k}"></span></div>`;
        body.innerHTML = row('P', '💰 Principal', Object.assign({}, PR, { value: P0 })) + row('R', '📊 Rate', Object.assign({}, RR, { value: R })) + row('T', '⏳ Years', Object.assign({}, YR, { value: T })) +
          `<div class="lb-budget-cards"><div class="si"></div><div class="ci"></div></div><div class="lb-budget-chart"><svg viewBox="0 0 340 128"></svg></div>`;
        body.querySelectorAll('.lb-budget-row input').forEach(inp => inp.addEventListener('input', () => { const v = +inp.value; if (inp.dataset.k === 'P') P0 = v; else if (inp.dataset.k === 'R') R = v; else T = v; touched = true; updInterest(); }));
        updInterest();
      }
      function updInterest() {
        const si = P0 * R * T / 100, ciA = P0 * Math.pow(1 + R / 100, T), ci = ciA - P0;
        body.querySelector('[data-v=P]').textContent = money(P0); body.querySelector('[data-v=R]').textContent = R + '% /yr'; body.querySelector('[data-v=T]').textContent = T + (T === 1 ? ' yr' : ' yrs');
        body.querySelector('.lb-budget-cards .si').innerHTML = `<small>Simple: ${money(P0)}×${R}×${T}÷100</small>+${money2(si)} → <br>${money2(P0 + si)}`;
        body.querySelector('.lb-budget-cards .ci').innerHTML = `<small>Compound: ${money(P0)}×(1+${R}/100)<sup>${T}</sup></small>+${money2(ci)} → <br>${money2(ciA)}`;
        /* chart: interest earned by the end of each year, SI vs CI */
        const n = T, W = 340, H = 128, L = 46, B = 20, Tp = 16, GW = W - L - 8, GH = H - B - Tp, bw = Math.min(14, GW / n / 2.6);
        const gl = ig.interest != null ? +ig.interest : ig.amount != null ? +ig.amount - P0 : P0 * ((+ig.times || 2) - 1);
        const max = Math.max(ci, gl > 0 ? gl : 0, 1) * 1.12;
        const Y = v => Tp + GH - v / max * GH;
        const kf = v => v >= 100000 ? (v / 100000).toLocaleString('en-IN') + 'L' : v >= 1000 ? (v / 1000).toLocaleString('en-IN') + 'k' : String(Math.round(v));
        let s = '';
        const mag = Math.pow(10, Math.floor(Math.log10(max / 4))), st = [1, 2, 5, 10].map(k => k * mag).find(v => max / v <= 5);
        for (let v = 0; v <= max; v += st) s += `<line x1="${L}" x2="${W - 8}" y1="${Y(v)}" y2="${Y(v)}" stroke="#e3e6f7"/><text x="${L - 4}" y="${Y(v) + 3}" text-anchor="end" font-size="9" font-weight="700" fill="#6b7090">${esc(cur)}${kf(v)}</text>`;
        if (gl > 0) s += `<line x1="${L}" x2="${W - 8}" y1="${Y(gl)}" y2="${Y(gl)}" stroke="#ffb020" stroke-width="1.5" stroke-dasharray="4 3"/><rect x="${L + 2}" y="${Y(gl) - 12}" width="${money(gl).length * 5.2 + 30}" height="11" rx="4" fill="#fff8e1"/><text x="${L + 5}" y="${Y(gl) - 3.5}" font-size="9" font-weight="800" fill="#c98a00">goal ${esc(money(gl))}</text>`;
        for (let y = 1; y <= n; y++) {
          const cx = L + (y - .5) * GW / n, a1 = P0 * R * y / 100, a2 = P0 * Math.pow(1 + R / 100, y) - P0;
          s += `<rect x="${cx - bw - 1}" y="${Y(a1)}" width="${bw}" height="${Y(0) - Y(a1)}" rx="2" fill="#3b82f6"/><rect x="${cx + 1}" y="${Y(a2)}" width="${bw}" height="${Y(0) - Y(a2)}" rx="2" fill="#2ed3a5"/>`;
          if (n <= 12 || y % Math.ceil(n / 10) === 0) s += `<text x="${cx}" y="${H - 6}" text-anchor="middle" font-size="9" font-weight="700" fill="#6b7090">yr ${y}</text>`;
        }
        s += `<rect x="${L}" y="2" width="9" height="9" rx="2" fill="#3b82f6"/><text x="${L + 12}" y="10" font-size="9.5" font-weight="800" fill="#1b1f3a">Simple</text><rect x="${L + 56}" y="2" width="9" height="9" rx="2" fill="#2ed3a5"/><text x="${L + 68}" y="10" font-size="9.5" font-weight="800" fill="#1b1f3a">Compound</text><text x="${W - 8}" y="10" text-anchor="end" font-size="9" font-weight="700" fill="#6b7090">interest earned so far</text>`;
        body.querySelector('.lb-budget-chart svg').innerHTML = s;
        const amt = ig.kind === 'si' ? P0 + si : ciA, intr = ig.kind === 'si' ? si : ci;
        let ok = false;
        if (ig.interest != null) ok = Math.abs(intr - +ig.interest) < 0.005;
        else if (ig.amount != null) ok = amt >= +ig.amount - 1e-6;
        else ok = amt >= P0 * (+ig.times || 2) - 1e-6;
        const diff = ci - si;
        msg.textContent = diff > 0.004 ? `Compound earns ${money2(diff)} more — interest also earns interest!` : 'In year 1, simple and compound interest are the same.';
        if (ok && touched && !won) { won = true; api.sfx('correct'); api.win(ig.interest != null ? `${ig.kind === 'si' ? 'Simple' : 'Compound'} interest = ${money2(intr)} at ${R}% for ${T} years!` : `${money(P0)} grows to ${money2(amt)} in ${T} years at ${R}% (${ig.kind === 'si' ? 'simple' : 'compound'} interest)!`); }
      }
      function setMode(m) {
        mode = m; won = false; touched = false; api.resetWin && api.resetWin();
        host.querySelectorAll('.lb-budget-tabs button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
        $('.lb-budget-ch').textContent = '🎯 Challenge: ' + chText();
        (m === 'budget' ? buildBudget : buildInterest)();
      }
      host.querySelectorAll('.lb-budget-tabs button').forEach(b => b.addEventListener('click', () => { api.sfx('tap'); setMode(b.dataset.m); }));
      $('.rs').addEventListener('click', () => { api.sfx('tap'); items.forEach((it, i) => it.amount = start[i]); income = +p.income > 0 ? +p.income : 30000; P0 = +PR.value; R = +RR.value; T = +YR.value; (mode === 'budget' ? buildBudget : buildInterest)(); });
      setMode(mode);
      return () => {};
    },
    example: {
      title: 'Family budget', mode: 'budget', modes: ['budget', 'interest'], currency: '₹', income: 30000, step: 500,
      challenge: 'Plan the family\'s ₹30,000: save at least 20% and plan every rupee',
      items: [{ name: 'Rent & bills', emoji: '🏠', kind: 'need', amount: 10000, min: 9000 }, { name: 'Food', emoji: '🍚', kind: 'need', amount: 7000, min: 5000 },
        { name: 'School', emoji: '🎒', kind: 'need', amount: 3000, min: 2000 }, { name: 'Fun & treats', emoji: '🍦', kind: 'want', amount: 6000 },
        { name: 'Savings', emoji: '🐷', kind: 'save', amount: 2000 }],
      goal: { save: 20, plan: true },
      principal: { min: 1000, max: 50000, step: 1000, value: 10000 }, rate: { min: 1, max: 15, step: 0.5, value: 10 }, years: { min: 1, max: 15, step: 1, value: 2 },
      igoal: { kind: 'ci', times: 2 }
    },
    examples: [
      { title: 'Pocket money (Class 3-5)', mode: 'budget', modes: ['budget'], income: 500, step: 10,
        challenge: 'Share your ₹500 pocket money: save at least 20% and use it all',
        items: [{ name: 'Snacks', emoji: '🍪', kind: 'want', amount: 200 }, { name: 'Stationery', emoji: '✏️', kind: 'need', amount: 150 },
          { name: 'Toys', emoji: '🧸', kind: 'want', amount: 100 }, { name: 'Piggy bank', emoji: '🐷', kind: 'save', amount: 0 }],
        goal: { save: 20, plan: true } },
      { title: 'Simple vs compound interest (Class 7-8)', mode: 'interest', modes: ['interest', 'budget'],
        challenge: 'Find the rate and time that give exactly ₹1,200 simple interest on ₹5,000',
        principal: { min: 1000, max: 20000, step: 1000, value: 5000 }, rate: { min: 1, max: 12, step: 1, value: 5 }, years: { min: 1, max: 10, step: 1, value: 2 },
        igoal: { kind: 'si', interest: 1200 } }
    ]
  });
})();
