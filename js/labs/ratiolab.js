/* StudyVerse Concept Lab: ratiolab — accounting ratios from a simplified Balance Sheet (Schedule III) and
 * Statement of Profit and Loss (CBSE Class 12 Accountancy, NCERT "Accounting Ratios").
 *
 * MODES
 *   compute  The child picks a ratio, reads the statements and types the two figures of the NCERT formula
 *            (e.g. Current assets and Current liabilities). The lab divides them live; Check marks each
 *            figure right/wrong with a hint ("Quick assets = Current assets − Inventories − Prepaid expenses").
 *   target   Sliders change balance-sheet items; every ratio updates live. Reach the target ratio
 *            (e.g. make the current ratio 2 : 1). The balance sheet stays balanced through a balancing item.
 *
 * PARAMS (all optional — every one has a built-in default)
 *   mode       string  'compute' | 'target'                                                      'compute'
 *   company    string  Company name                                                              'Shree Ganesh Ltd.'
 *   challenge  string  Challenge sentence                                                        (by mode)
 *   bs         object  Balance sheet (₹). Keys: shareCapital, reserves, ltBorrowings, ltProvisions,
 *                      tradePayables, stBorrowings, otherCL, stProvisions, ppe, intangibles,
 *                      ncInvestments, currentInvestments, inventories, tradeReceivables, cash, prepaid.
 *                      If `bs` is given, keys left out are 0.                                   a ₹8,00,000 balance sheet
 *   pl         object  Statement of P&L (₹). Keys: revenue (revenue from operations), cogs (cost of revenue
 *                      from operations), opex (other operating expenses), interest (finance costs on
 *                      long-term debt), tax, openingInventory, openingReceivables, openingPayables,
 *                      creditRevenue, creditPurchases. Missing opening figures = closing figures;
 *                      creditRevenue defaults to revenue; creditPurchases to cogs + closing − opening inventory.
 *   ratios     array   compute mode: ratio keys to do, in order. Keys: current, quick, debtEquity,
 *                      totalAssetsToDebt, proprietary, interestCoverage, inventoryTurnover,
 *                      receivablesTurnover, payablesTurnover, wcTurnover, grossProfit, operating,
 *                      netProfit, roi                                                          ['current','quick','debtEquity','grossProfit']
 *   target     object  target mode: {ratio, value, tol}  (value in the ratio's own unit: 2 = 2 : 1, 25 = 25%) {ratio:'current', value:2, tol:0.005}
 *   sliders    array   target mode: item keys that get a slider (max 4)                          ['inventories','tradeReceivables','cash','tradePayables']
 *   step       number  slider step (₹)                                                           1% of total assets, rounded
 *   balancer   string  item that absorbs slider changes so Assets = Equity + Liabilities         'ltBorrowings'
 *   show       array   target mode: other ratio keys shown live under the target                ['quick','debtEquity','wcTurnover']
 *   tol        number  compute mode: ₹ tolerance when checking typed figures                    0.5
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function inr(n) {
    if (!isFinite(n)) return '—';
    const neg = n < 0; n = Math.abs(Math.round(n * 100) / 100);
    let [i, d] = n.toFixed(2).split('.'); let l3 = i.slice(-3), rest = i.slice(0, -3);
    if (rest) l3 = ',' + l3; rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    return (neg ? '−' : '') + rest + l3 + (d !== '00' ? '.' + d : '');
  }
  const num = s => { const t = String(s == null ? '' : s).replace(/[^\d.]/g, ''); if (!t) return NaN; const v = parseFloat(t); return isFinite(v) ? v : NaN; };
  const BSK = {
    shareCapital: ['Share capital', 'el', 'Shareholders’ funds'], reserves: ['Reserves and surplus', 'el', 'Shareholders’ funds'],
    ltBorrowings: ['Long-term borrowings', 'el', 'Non-current liabilities'], ltProvisions: ['Long-term provisions', 'el', 'Non-current liabilities'],
    tradePayables: ['Trade payables', 'el', 'Current liabilities'], stBorrowings: ['Short-term borrowings', 'el', 'Current liabilities'],
    otherCL: ['Other current liabilities', 'el', 'Current liabilities'], stProvisions: ['Short-term provisions', 'el', 'Current liabilities'],
    ppe: ['Property, plant & equip.', 'a', 'Non-current assets'], intangibles: ['Intangible assets', 'a', 'Non-current assets'], ncInvestments: ['Non-current investments', 'a', 'Non-current assets'],
    currentInvestments: ['Current investments', 'a', 'Current assets'], inventories: ['Inventories', 'a', 'Current assets'], tradeReceivables: ['Trade receivables', 'a', 'Current assets'],
    cash: ['Cash & cash equivalents', 'a', 'Current assets'], prepaid: ['Prepaid expenses', 'a', 'Current assets']
  };
  const SHORT = { shareCapital: 'Share capital', reserves: 'Reserves & surplus', ltBorrowings: 'LT borrowings', ltProvisions: 'LT provisions', tradePayables: 'Trade payables',
    stBorrowings: 'ST borrowings', otherCL: 'Other curr. liab.', stProvisions: 'ST provisions', ppe: 'PPE', intangibles: 'Intangibles', ncInvestments: 'NC investments',
    currentInvestments: 'Current invest.', inventories: 'Inventories', tradeReceivables: 'Trade receivables', cash: 'Cash & equiv.', prepaid: 'Prepaid exp.' };
  const PLK = {
    revenue: 'Revenue from ops', cogs: 'Cost of rev. from ops', opex: 'Operating expenses', interest: 'Finance costs', tax: 'Tax',
    openingInventory: 'Opening inventory', openingReceivables: 'Opening receivables', openingPayables: 'Opening payables', creditRevenue: 'Credit revenue', creditPurchases: 'Credit purchases'
  };
  const DEF_BS = { shareCapital: 300000, reserves: 100000, ltBorrowings: 200000, tradePayables: 120000, stBorrowings: 40000, otherCL: 20000, stProvisions: 20000,
    ppe: 440000, ncInvestments: 60000, currentInvestments: 20000, inventories: 120000, tradeReceivables: 100000, cash: 50000, prepaid: 10000 };
  const DEF_PL = { revenue: 1200000, cogs: 840000, opex: 180000, interest: 20000, tax: 40000, openingInventory: 100000 };
  function derive(b, l) {
    const v = k => +b[k] || 0, w = k => +l[k] || 0;
    const CA = v('currentInvestments') + v('inventories') + v('tradeReceivables') + v('cash') + v('prepaid');
    const CL = v('tradePayables') + v('stBorrowings') + v('otherCL') + v('stProvisions');
    const SHF = v('shareCapital') + v('reserves'), DEBT = v('ltBorrowings') + v('ltProvisions');
    const TA = v('ppe') + v('intangibles') + v('ncInvestments') + CA, TEL = SHF + DEBT + CL;
    const rev = w('revenue'), cogs = w('cogs'), GP = rev - cogs, PBIT = GP - w('opex'), PAT = PBIT - w('interest') - w('tax');
    const oi = l.openingInventory != null ? w('openingInventory') : v('inventories'), avgInv = (oi + v('inventories')) / 2;
    const orc = l.openingReceivables != null ? w('openingReceivables') : v('tradeReceivables'), avgRec = (orc + v('tradeReceivables')) / 2;
    const opy = l.openingPayables != null ? w('openingPayables') : v('tradePayables'), avgPay = (opy + v('tradePayables')) / 2;
    const credRev = l.creditRevenue != null ? w('creditRevenue') : rev, credPur = l.creditPurchases != null ? w('creditPurchases') : cogs + v('inventories') - oi;
    return { CA, CL, QA: CA - v('inventories') - v('prepaid'), SHF, DEBT, TA, TEL, GP, PBIT, PAT, rev, cogs, opex: w('opex'), interest: w('interest'), avgInv, avgRec, avgPay, credRev, credPur, WC: CA - CL, CE: SHF + DEBT, OC: cogs + w('opex') };
  }
  /* [name, numerator label, numerator key, denominator label, denominator key, format, hint numerator, hint denominator] */
  const R = {
    current: ['Current ratio', 'Current assets', 'CA', 'Current liabilities', 'CL', 'ratio', 'Current investments + Inventories + Trade receivables + Cash & cash eq. + Prepaid exp.', 'Trade payables + Short-term borrowings + Other current liabilities + Short-term provisions'],
    quick: ['Quick (liquid) ratio', 'Quick assets', 'QA', 'Current liabilities', 'CL', 'ratio', 'Quick assets = Current assets − Inventories − Prepaid expenses', 'All current liabilities'],
    debtEquity: ['Debt–equity ratio', 'Long-term debts', 'DEBT', 'Shareholders’ funds', 'SHF', 'ratio', 'Long-term borrowings + Long-term provisions', 'Share capital + Reserves and surplus'],
    totalAssetsToDebt: ['Total assets to debt ratio', 'Total assets', 'TA', 'Long-term debts', 'DEBT', 'ratio', 'All non-current + current assets', 'Long-term borrowings + Long-term provisions'],
    proprietary: ['Proprietary ratio', 'Shareholders’ funds', 'SHF', 'Total assets', 'TA', 'ratio', 'Share capital + Reserves and surplus', 'All non-current + current assets'],
    interestCoverage: ['Interest coverage ratio', 'Net profit before interest & tax', 'PBIT', 'Interest on long-term debt', 'interest', 'times', 'Revenue − Cost of revenue − Operating expenses', 'Finance costs'],
    inventoryTurnover: ['Inventory turnover ratio', 'Cost of revenue from operations', 'cogs', 'Average inventory', 'avgInv', 'times', 'From the Statement of P&L', '(Opening inventory + Closing inventory) ÷ 2'],
    receivablesTurnover: ['Trade receivables turnover', 'Net credit revenue from operations', 'credRev', 'Average trade receivables', 'avgRec', 'times', 'Credit revenue from operations', '(Opening + Closing trade receivables) ÷ 2'],
    payablesTurnover: ['Trade payables turnover', 'Net credit purchases', 'credPur', 'Average trade payables', 'avgPay', 'times', 'Purchases = Cost of revenue + Closing inventory − Opening inventory', '(Opening + Closing trade payables) ÷ 2'],
    wcTurnover: ['Working capital turnover', 'Revenue from operations', 'rev', 'Working capital', 'WC', 'times', 'From the Statement of P&L', 'Current assets − Current liabilities'],
    grossProfit: ['Gross profit ratio', 'Gross profit', 'GP', 'Net revenue from operations', 'rev', 'pct', 'Revenue from operations − Cost of revenue from operations', 'Revenue from operations'],
    operating: ['Operating ratio', 'Cost of revenue + Operating exp.', 'OC', 'Net revenue from operations', 'rev', 'pct', 'Cost of revenue from operations + Other operating expenses', 'Revenue from operations'],
    netProfit: ['Net profit ratio', 'Net profit (after tax)', 'PAT', 'Net revenue from operations', 'rev', 'pct', 'Revenue − Cost of revenue − Op. expenses − Finance costs − Tax', 'Revenue from operations'],
    roi: ['Return on investment (ROI)', 'Profit before interest & tax', 'PBIT', 'Capital employed', 'CE', 'pct', 'Revenue − Cost of revenue − Operating expenses', 'Shareholders’ funds + Non-current liabilities']
  };
  const val = (k, d) => { const r = R[k]; const a = d[r[2]], b = d[r[4]]; return b ? a / b * (r[5] === 'pct' ? 100 : 1) : NaN; };
  const fmtR = (k, v) => !isFinite(v) ? '—' : R[k][5] === 'ratio' ? `${v.toFixed(2)} : 1` : R[k][5] === 'times' ? `${v.toFixed(2)} times` : `${v.toFixed(2)}%`;

  const CSS = `
.lb-ratiolab-w{font-size:13px;color:#1b1f3a;user-select:none;-webkit-user-select:none;line-height:1.3}
.lb-ratiolab-w button{font-family:inherit;cursor:pointer;border:none}
.lb-ratiolab-ch{font-weight:800;font-size:13.5px;line-height:1.3;margin-bottom:6px}
.lb-ratiolab-st{background:#f7f8ff;border-radius:12px;padding:5px 7px;max-height:142px;overflow-y:auto;font-size:11px}
.lb-ratiolab-st h4{margin:0 0 2px;font-size:11px;color:#7044e0;font-weight:900;display:flex;justify-content:space-between}
.lb-ratiolab-cols{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.lb-ratiolab-st .g{color:#6b7090;font-weight:800;font-size:9.5px;text-transform:uppercase;letter-spacing:.03em;margin-top:2px}
.lb-ratiolab-st .i{display:flex;justify-content:space-between;gap:4px;font-weight:700;line-height:1.35}
.lb-ratiolab-st .i span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-ratiolab-w.tg .lb-ratiolab-st{max-height:92px}
.lb-ratiolab-st .i b{white-space:nowrap}
.lb-ratiolab-st .i.chg b{color:#7044e0}.lb-ratiolab-st .i.bal b{color:#b57f00}
.lb-ratiolab-st .tot{display:flex;justify-content:space-between;border-top:1.5px solid #1b1f3a;font-weight:900;margin-top:2px}
.lb-ratiolab-pl{display:grid;grid-template-columns:1fr 1fr;column-gap:8px;margin-top:4px;border-top:1px dashed #d5d9ee;padding-top:3px}
.lb-ratiolab-tabs{display:flex;gap:5px;overflow-x:auto;margin:7px 0 5px;padding-bottom:2px;scrollbar-width:none}
.lb-ratiolab-tabs::-webkit-scrollbar{display:none}
.lb-ratiolab-tabs button{flex:none;background:#eef0fb;border-radius:99px;padding:6px 11px;font-weight:800;font-size:12px;min-height:34px;color:#1b1f3a}
.lb-ratiolab-tabs button.on{background:#8b5cf6;color:#fff}.lb-ratiolab-tabs button.dn:not(.on){background:#e3fbf3;color:#0f7a5c}
.lb-ratiolab-f{background:#fff8e1;border-radius:12px;padding:6px 9px}
.lb-ratiolab-f .nm{font-weight:900;font-size:13px}
.lb-ratiolab-frac{display:grid;grid-template-columns:1fr 112px;gap:4px 8px;align-items:center;margin-top:4px}
.lb-ratiolab-frac label{font-weight:800;font-size:12px;line-height:1.2}
.lb-ratiolab-frac input{height:36px;border:2px solid #e6dcae;border-radius:9px;padding:0 7px;font:inherit;font-weight:800;text-align:right;font-size:13.5px;width:100%;box-sizing:border-box;background:#fff;user-select:text;-webkit-user-select:text}
.lb-ratiolab-frac input.ok{border-color:#2ed3a5;background:#effdf8}.lb-ratiolab-frac input.bad{border-color:#ff6b6b;background:#fff3f3}
.lb-ratiolab-frac .bar{grid-column:1/3;border-top:2px solid #1b1f3a;height:0}
.lb-ratiolab-res{display:flex;align-items:center;gap:6px;margin-top:6px}
.lb-ratiolab-res .v{flex:1;font-weight:900;font-size:17px;color:#7044e0}
.lb-ratiolab-btn{min-height:40px;border-radius:12px;background:#8b5cf6;color:#fff;font-weight:800;font-size:14px;padding:0 14px}
.lb-ratiolab-btn.alt{background:#eef0fb;color:#1b1f3a}
.lb-ratiolab-msg{margin-top:5px;font-weight:700;font-size:12.5px;line-height:1.35;min-height:17px}
.lb-ratiolab-msg.ok{color:#0f7a5c}.lb-ratiolab-msg.bad{color:#d03c3c}
.lb-ratiolab-big{margin:6px 0 2px}
.lb-ratiolab-big .v{font-size:21px;font-weight:900;color:#7044e0;line-height:1.1}
.lb-ratiolab-big .v small{display:block;font-size:10.5px;color:#6b7090;font-weight:800}
.lb-ratiolab-gauge{height:12px;margin:5px 4px 0;border-radius:99px;background:#eef0fb;position:relative}
.lb-ratiolab-gauge .fl{position:absolute;left:0;top:0;bottom:0;border-radius:99px;background:linear-gradient(90deg,#ff6b6b,#ffc93c);transition:width .15s}
.lb-ratiolab-gauge .tg{position:absolute;top:-4px;bottom:-4px;width:3px;margin-left:-1.5px;background:#1b1f3a;border-radius:2px}
.lb-ratiolab-gauge .tl{position:absolute;top:16px;font-size:9.5px;font-weight:800;color:#1b1f3a;transform:translateX(-50%);white-space:nowrap}
.lb-ratiolab-gauge.hit .fl{background:#2ed3a5}
.lb-ratiolab-sl{display:flex;align-items:center;gap:6px;margin-top:1px;font-weight:800;font-size:12px}
.lb-ratiolab-sl span.n{width:104px;line-height:1.1}
.lb-ratiolab-sl input{flex:1;height:30px;accent-color:#8b5cf6;min-width:0}
.lb-ratiolab-sl b{width:70px;text-align:right;color:#7044e0}
.lb-ratiolab-mini{display:flex;gap:5px;margin-top:6px}
.lb-ratiolab-mini div{flex:1;background:#f6f7ff;border-radius:10px;padding:4px;text-align:center;font-weight:900;font-size:13px;line-height:1.15}
.lb-ratiolab-mini small{display:block;font-size:9.5px;color:#6b7090;font-weight:800}
`;

  Labs.register('ratiolab', {
    title: 'Ratio lab',
    subjects: ['accountancy', 'commerce'],
    render(host, p, api) {
      p = p && typeof p === 'object' ? p : {};
      const mode = p.mode === 'target' ? 'target' : 'compute';
      const company = p.company || 'Shree Ganesh Ltd.';
      const bs0 = {}; Object.keys(BSK).forEach(k => bs0[k] = p.bs && typeof p.bs === 'object' ? Math.max(0, +p.bs[k] || 0) : (DEF_BS[k] || 0));
      const pl = {}; const srcPL = p.pl && typeof p.pl === 'object' ? p.pl : DEF_PL;
      Object.keys(PLK).forEach(k => { if (srcPL[k] != null && isFinite(+srcPL[k])) pl[k] = +srcPL[k]; });
      const bs = Object.assign({}, bs0);
      const tolR = isFinite(+p.tol) && +p.tol >= 0 ? +p.tol : 0.5;
      let won = false;
      const win = m => { if (won) return; won = true; api.sfx && api.sfx('correct'); api.win(m); };
      host.innerHTML = `<div class="lb-ratiolab-w"><style>${CSS}</style><div class="lb-ratiolab-ch"></div><div class="lb-ratiolab-st"></div><div class="lb-ratiolab-body"></div></div>`;
      const W = host.firstElementChild; if (mode === 'target') W.classList.add('tg'); const st = W.querySelector('.lb-ratiolab-st'), body = W.querySelector('.lb-ratiolab-body');
      const setCh = t => { W.querySelector('.lb-ratiolab-ch').textContent = '🎯 Challenge: ' + t; };
      let balKey = null, changed = {};
      function drawStatements() {
        const d = derive(bs, pl), groups = side => {
          let out = '', last = '';
          Object.keys(BSK).filter(k => BSK[k][1] === side && (bs[k] || changed[k] || k === balKey)).forEach(k => {
            if (BSK[k][2] !== last) { last = BSK[k][2]; out += `<div class="g">${last}</div>`; }
            out += `<div class="i ${changed[k] ? 'chg' : ''} ${k === balKey ? 'bal' : ''}"><span>${SHORT[k]}${k === balKey ? ' ⚖️' : ''}</span><b>${inr(bs[k])}</b></div>`;
          });
          return out;
        };
        const plRows = ['revenue', 'cogs', 'opex', 'interest', 'tax', 'openingInventory', 'openingReceivables', 'openingPayables', 'creditRevenue', 'creditPurchases'].filter(k => pl[k] != null)
          .map(k => `<div class="i"><span>${PLK[k]}</span><b>${inr(pl[k])}</b></div>`).join('');
        st.innerHTML = `<h4><span>Balance Sheet of ${esc(company)}</span><span>${balKey ? '⚖️ = balancing item · ' : ''}₹</span></h4><div class="lb-ratiolab-cols"><div>${groups('el')}<div class="tot"><span>Total</span><span>${inr(d.TEL)}</span></div></div><div>${groups('a')}<div class="tot"><span>Total</span><span>${inr(d.TA)}</span></div></div></div>
<h4 style="margin-top:5px"><span>Statement of Profit and Loss</span><span>₹</span></h4><div class="lb-ratiolab-pl">${plRows}</div>`;
      }

      /* ───────── compute ───────── */
      function compute() {
        let list = (Array.isArray(p.ratios) ? p.ratios : []).filter(k => R[k]);
        if (!list.length) list = ['current', 'quick', 'debtEquity', 'grossProfit'];
        list = [...new Set(list)].slice(0, 8);
        setCh(p.challenge || `Work out the ${list.map(k => R[k][0].replace(/ ratio| \(.*\)/g, '')).join(', ')} ratio${list.length > 1 ? 's' : ''} of ${company}`);
        const state = {}; list.forEach(k => state[k] = { n: '', d: '', done: false, mn: '', md: '' });
        let cur = list[0], hint = false;
        drawStatements();
        function res() { const s = state[cur], a = num(s.n), b = num(s.d); return a >= 0 && b > 0 ? a / b * (R[cur][5] === 'pct' ? 100 : 1) : NaN; }
        function draw(msg, cls) {
          const r = R[cur], s = state[cur], d = derive(bs, pl);
          body.innerHTML = `<div class="lb-ratiolab-tabs">${list.map(k => `<button data-k="${k}" class="${k === cur ? 'on' : ''} ${state[k].done ? 'dn' : ''}">${state[k].done ? '✓ ' : ''}${R[k][0].replace(/ ratio$/, '').replace(/ \(.*\)/, '')}</button>`).join('')}</div>
<div class="lb-ratiolab-f"><div class="nm">${r[0]} = ${r[1]} ÷ ${r[3]}${r[5] === 'pct' ? ' × 100' : ''}</div>
<div class="lb-ratiolab-frac"><label>${r[1]}${hint ? `<br><small style="color:#6b7090">${r[6]}</small>` : ''}</label><input class="n ${s.mn}" inputmode="decimal" placeholder="₹" value="${esc(s.n)}" ${s.done ? 'disabled' : ''}>
<div class="bar"></div><label>${r[3]}${hint ? `<br><small style="color:#6b7090">${r[7]}</small>` : ''}</label><input class="d ${s.md}" inputmode="decimal" placeholder="₹" value="${esc(s.d)}" ${s.done ? 'disabled' : ''}></div></div>
<div class="lb-ratiolab-res"><span class="v">= ${fmtR(cur, res())}</span>${s.done ? '' : `<button class="lb-ratiolab-btn alt hn">💡</button><button class="lb-ratiolab-btn ck">Check ✓</button>`}</div>
<div class="lb-ratiolab-msg ${cls || ''}">${msg || (s.done ? `✔ ${r[0]} = ${fmtR(cur, val(cur, d))}` : 'Type both figures from the statements (₹).')}</div>`;
        }
        function liveRes() { const v = body.querySelector('.lb-ratiolab-res .v'); if (v) v.textContent = '= ' + fmtR(cur, res()); }
        function check() {
          const r = R[cur], s = state[cur], d = derive(bs, pl), a = num(s.n), b = num(s.d);
          if (!(a >= 0) || !(b > 0)) { draw('Type both figures first.', 'bad'); return; }
          const okA = Math.abs(a - d[r[2]]) <= tolR, okB = Math.abs(b - d[r[4]]) <= tolR;
          s.mn = okA ? 'ok' : 'bad'; s.md = okB ? 'ok' : 'bad';
          if (okA && okB) {
            s.done = true; api.sfx && api.sfx('correct'); hint = false;
            const left = list.filter(k => !state[k].done);
            draw(`✔ ${r[0]} = ₹${inr(d[r[2]])} ÷ ₹${inr(d[r[4]])}${r[5] === 'pct' ? ' × 100' : ''} = ${fmtR(cur, val(cur, d))}${left.length ? ` — ${left.length} to go` : ''}`, 'ok');
            if (!left.length) win(`All ${list.length} ratios correct! e.g. ${R[list[0]][0]} = ${fmtR(list[0], val(list[0], d))}`);
            return;
          }
          api.sfx && api.sfx('wrong');
          draw(`${!okA ? r[1] : r[3]} is not right. Hint: ${(!okA ? r[6] : r[7]).replace(/\.$/, '')}.`, 'bad');
        }
        body.addEventListener('click', e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.k) { cur = b.dataset.k; hint = false; draw(); return; }
          if (b.classList.contains('hn')) { hint = !hint; draw(); return; }
          if (b.classList.contains('ck')) check();
        });
        body.addEventListener('input', e => { const s = state[cur]; if (e.target.classList.contains('n')) { s.n = e.target.value; s.mn = ''; e.target.classList.remove('ok', 'bad'); } if (e.target.classList.contains('d')) { s.d = e.target.value; s.md = ''; e.target.classList.remove('ok', 'bad'); } liveRes(); });
        body.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
        draw();
      }

      /* ───────── target ───────── */
      function target() {
        const tg = Object.assign({ ratio: 'current', value: 2, tol: 0.005 }, p.target && typeof p.target === 'object' ? p.target : {});
        if (!R[tg.ratio]) tg.ratio = 'current';
        tg.value = isFinite(+tg.value) ? +tg.value : 2; tg.tol = isFinite(+tg.tol) && +tg.tol > 0 ? +tg.tol : 0.005;
        let sl = (Array.isArray(p.sliders) ? p.sliders : ['inventories', 'tradeReceivables', 'cash', 'tradePayables']).filter(k => BSK[k]).slice(0, 4);
        if (!sl.length) sl = ['inventories', 'tradeReceivables', 'cash', 'tradePayables'];
        balKey = BSK[p.balancer] ? p.balancer : 'ltBorrowings';
        const altBal = balKey === 'cash' ? 'reserves' : 'cash';
        const d0 = derive(bs0, pl);
        const nice = x => { const e = Math.pow(10, Math.floor(Math.log10(x))); return [1, 2, 5, 10].map(m => m * e).find(m => m >= x) || e * 10; };
        const step = +p.step > 0 ? +p.step : nice(Math.max(1, d0.TA / 100) / 2);
        const maxOf = k => Math.max(step * 10, Math.ceil(bs0[k] * 2 / step) * step);
        const show = (Array.isArray(p.show) ? p.show : ['quick', 'debtEquity', 'wcTurnover']).filter(k => R[k] && k !== tg.ratio).slice(0, 3);
        const unitTxt = R[tg.ratio][5] === 'ratio' ? `${tg.value} : 1` : R[tg.ratio][5] === 'pct' ? `${tg.value}%` : `${tg.value} times`;
        setCh(p.challenge || `Use the sliders to make the ${R[tg.ratio][0].toLowerCase()} exactly ${unitTxt}`);
        let touched = false;
        const gmax = Math.max(tg.value * 1.6, val(tg.ratio, d0) * 1.3, 0.1);
        body.innerHTML = `<div class="lb-ratiolab-big"><div class="v"></div><div class="lb-ratiolab-gauge"><div class="fl"></div><div class="tg" style="left:${tg.value / gmax * 100}%"></div><div class="tl" style="left:${tg.value / gmax * 100}%">🎯 ${unitTxt}</div></div></div>
<div style="height:12px"></div>${sl.map(k => `<div class="lb-ratiolab-sl"><span class="n">${SHORT[k]}</span><input type="range" data-k="${k}" min="0" max="${maxOf(k)}" step="${step}" value="${bs0[k]}"><b data-v="${k}"></b></div>`).join('')}
<div class="lb-ratiolab-mini">${show.map(k => `<div data-m="${k}"></div>`).join('')}</div>
<div class="lb-ratiolab-msg"></div>`;
        function upd() {
          const d = derive(bs, pl), v = val(tg.ratio, d), hit = isFinite(v) && Math.abs(v - tg.value) <= tg.tol + 1e-12;
          drawStatements();
          body.querySelector('.lb-ratiolab-big .v').innerHTML = `${fmtR(tg.ratio, v)}<small>${R[tg.ratio][0]} = ${R[tg.ratio][1]} ₹${inr(d[R[tg.ratio][2]])} ÷ ${R[tg.ratio][3]} ₹${inr(d[R[tg.ratio][4]])}</small>`;
          const g = body.querySelector('.lb-ratiolab-gauge'); g.classList.toggle('hit', hit); g.querySelector('.fl').style.width = Math.min(100, Math.max(0, (isFinite(v) ? v : 0) / gmax * 100)) + '%';
          sl.forEach(k => { body.querySelector(`[data-v="${k}"]`).textContent = '₹' + inr(bs[k]); });
          show.forEach(k => { body.querySelector(`[data-m="${k}"]`).innerHTML = `${fmtR(k, val(k, d))}<small>${R[k][0].replace(/ ratio$/, '')}</small>`; });
          const r = R[tg.ratio], m = body.querySelector('.lb-ratiolab-msg');
          m.className = 'lb-ratiolab-msg' + (hit ? ' ok' : '');
          m.textContent = `${hit ? '🎯 On target!' : isFinite(v) ? (v < tg.value ? `Too low — raise the ${r[1].toLowerCase()} or cut the ${r[3].toLowerCase()}.` : `Too high — lower the ${r[1].toLowerCase()} or raise the ${r[3].toLowerCase()}.`) : ''}`;
          if (hit && touched) win(`${r[0]} = ₹${inr(d[r[2]])} ÷ ₹${inr(d[r[4]])} = ${fmtR(tg.ratio, v)}`);
        }
        body.addEventListener('input', e => {
          const k = e.target.dataset.k; if (!k) return;
          const nv = +e.target.value, delta = nv - bs[k], side = BSK[k][1];
          const bk = k === balKey ? altBal : balKey;
          /* keep Assets = Equity + Liabilities: the balancer moves with the change if it is on the other side, against it if on the same side */
          const sgn = BSK[bk][1] === side ? -1 : 1;
          let dd = sgn > 0 ? Math.max(delta, -bs[bk]) : Math.min(delta, bs[bk]); /* never push the balancing item below 0 */
          if (dd !== delta) { dd = Math.trunc(dd / step) * step; e.target.value = bs[k] + dd; }
          bs[k] += dd; const nb = bs[bk] + sgn * dd;
          bs[bk] = Math.max(0, nb); changed[k] = 1; touched = true; upd();
        });
        upd();
      }
      (mode === 'target' ? target : compute)();
      return () => { host.innerHTML = ''; };
    },
    example: {
      mode: 'compute', company: 'Shree Ganesh Ltd.',
      challenge: 'Find the current, quick, debt–equity, inventory turnover and gross profit ratios',
      bs: { shareCapital: 300000, reserves: 100000, ltBorrowings: 200000, tradePayables: 120000, stBorrowings: 40000, otherCL: 20000, stProvisions: 20000,
        ppe: 440000, ncInvestments: 60000, currentInvestments: 20000, inventories: 120000, tradeReceivables: 100000, cash: 50000, prepaid: 10000 },
      pl: { revenue: 1200000, cogs: 840000, opex: 180000, interest: 20000, tax: 40000, openingInventory: 100000 },
      ratios: ['current', 'quick', 'debtEquity', 'inventoryTurnover', 'grossProfit']
    },
    examples: [
      { mode: 'target', company: 'Shree Ganesh Ltd.', challenge: 'The bank wants a current ratio of 2 : 1 — move the sliders to get it',
        bs: { shareCapital: 300000, reserves: 100000, ltBorrowings: 200000, tradePayables: 120000, stBorrowings: 40000, otherCL: 20000, stProvisions: 20000,
          ppe: 440000, ncInvestments: 60000, currentInvestments: 20000, inventories: 120000, tradeReceivables: 100000, cash: 50000, prepaid: 10000 },
        pl: { revenue: 1200000, cogs: 840000, opex: 180000, interest: 20000, tax: 40000, openingInventory: 100000 },
        target: { ratio: 'current', value: 2, tol: 0.005 }, sliders: ['inventories', 'cash', 'tradePayables', 'stBorrowings'], balancer: 'ltBorrowings', show: ['quick', 'debtEquity', 'roi'] },
      { mode: 'compute', company: 'Vikas Ltd.', challenge: 'Profitability check: find the net profit ratio, operating ratio and return on investment',
        bs: { shareCapital: 500000, reserves: 150000, ltBorrowings: 250000, tradePayables: 90000, otherCL: 10000, ppe: 700000, inventories: 120000, tradeReceivables: 120000, cash: 60000 },
        pl: { revenue: 1500000, cogs: 1000000, opex: 230000, interest: 25000, tax: 61250 },
        ratios: ['netProfit', 'operating', 'roi'] }
    ]
  });
})();
