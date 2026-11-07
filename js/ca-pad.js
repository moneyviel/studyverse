/* ================= CA writing-pad templates (js/ca-pad.js) — loaded after js/ca.js, before js/ca-tools.js =================
   Exam formats a CA Foundation student writes, as editable tables inside the Write tab's answer pad:
   Journal (and Journal Proper) · subsidiary books (Purchases, Sales, both Returns books, Bills Receivable / Payable books)
   · Cash Books (simple, two-column, three-column, analytical Petty Cash) · Ledger (T-account) · Trial Balance · BRS
   · Trading / Profit & Loss / Balance Sheet (horizontal and Schedule III) · Receipts & Payments / Income & Expenditure
   · Statement of Affairs · Partners' Capital A/cs · P&L Appropriation · Revaluation · Realisation · Depreciation schedule
   · Asset A/c · Stores ledger (FIFO / weighted average) · comparison table · blank table.
   Conventions: dates dd-mmm-yy (05-Apr-26; ICAI-style years such as 01-Apr-X1 also accepted) with a date picker;
   separate Dr. / Cr. amount columns; ledger and account names in Title Case (A/c, &, GST, CGST/SGST/IGST, LLP, BRS kept);
   journal credit lines indented "To … A/c"; narration "(Being …)"; Indian digit grouping; auto totals and checks.
   API: CaPad.mount(host, { pad, q, onChange }) -> { value(), isEmpty() } ; CaPad.view(payload) -> static HTML;
        CaPad.suggest(pad, text) -> [template ids] ; CaPad.titleCase / parseDate / parseAmt / inr ; CaPad.TPL.
   Saved payload (attempt.table, and Ca.submission().answer.table for a future AI checker):
     { schema: 'ca-pad/1', sheets: [ { tpl, name, title, data, flat: { kind: 'journal'|'tacc'|'grid', cols:[…], rows:[[…]], account? }, check: { ok, msg } } ] }
   flat + check are what js/ca-check.js marks (rows, figures, and `pad_ok` points use check.ok). */
(function () {
  'use strict';
  const D = document;
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const p2 = n => String(n).padStart(2, '0');
  const e_ = s => (typeof esc === 'function' ? esc(s) : String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])));

  /* ---------- dates: dd-mmm-yy ---------- */
  const monIdx = s => { s = String(s).slice(0, 3).toLowerCase(); const i = MON.findIndex(m => m.toLowerCase() === s); return i < 0 ? 0 : i + 1; };
  function parseDate(s) {
    s = String(s || '').trim(); if (!s) return { ok: true, v: '' };
    let d, m, y = null, yx = null, r;
    const yr = t => { if (/^[Xx]\d$/.test(t)) yx = 'X' + t[1]; else y = t.length === 2 ? 2000 + +t : +t; };
    if ((r = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s))) { y = +r[1]; m = +r[2]; d = +r[3]; }
    else if ((r = /^(\d{1,2})(?:st|nd|rd|th)?[\s\-\/.]+([A-Za-z]{3,9}\.?|\d{1,2})[\s\-\/.,]+(\d{4}|\d{2}|[Xx]\d)$/.exec(s))) { d = +r[1]; m = /^\d/.test(r[2]) ? +r[2] : monIdx(r[2]); yr(r[3]); }
    else if ((r = /^([A-Za-z]{3,9})\.?[\s\-\/.]+(\d{1,2})(?:st|nd|rd|th)?,?[\s\-\/.]+(\d{4}|\d{2}|[Xx]\d)$/.exec(s))) { m = monIdx(r[1]); d = +r[2]; yr(r[3]); }
    else return { ok: false };
    if (!m || m < 1 || m > 12 || !d) return { ok: false };
    const dim = yx ? [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1] : new Date(y, m, 0).getDate();
    if (d > dim || (!yx && (y < 1900 || y > 2199))) return { ok: false };
    return { ok: true, v: `${p2(d)}-${MON[m - 1]}-${yx || p2(y % 100)}`, iso: yx ? '' : `${y}-${p2(m)}-${p2(d)}` };
  }
  const isoToD = iso => { const r = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || ''); return r ? `${r[3]}-${MON[+r[2] - 1]}-${r[1].slice(2)}` : ''; };

  /* ---------- amounts: Indian grouping, (1,000) = negative ---------- */
  function parseAmt(s) {
    let t = String(s ?? '').trim(); if (!t) return null;
    let neg = false;
    if (/^\(.*\)$/.test(t)) { neg = true; t = t.slice(1, -1); }
    t = t.replace(/[₹,\s]/g, '').replace(/^Rs\.?/i, '').replace(/(Dr|Cr)\.?$/i, '');
    if (/^[-−]/.test(t)) { neg = !neg; t = t.slice(1); }
    if (!/^(\d+\.?\d*|\.\d+)$/.test(t)) return NaN;
    const v = parseFloat(t); return neg ? -v : v;
  }
  const r2 = v => Math.round(v * 100) / 100;
  function inr(v) {
    if (v == null || v === '' || isNaN(v)) return '';
    v = r2(v); const frac = Math.round(Math.abs(v) * 100) % 100 !== 0;
    const s = Math.abs(v).toLocaleString('en-IN', { minimumFractionDigits: frac ? 2 : 0, maximumFractionDigits: 2 });
    return v < 0 ? `(${s})` : s;
  }
  const inr0 = v => (v ? inr(v) : '');
  const num = s => { const v = parseAmt(s); return v == null || isNaN(v) ? 0 : v; };
  const has = s => { const v = parseAmt(s); return v != null && !isNaN(v); };

  /* ---------- Title Case for ledger / account names ---------- */
  const KEEP = { 'a/c': 'A/c', 'a/cs': 'A/cs', '&': '&', gst: 'GST', cgst: 'CGST', sgst: 'SGST', igst: 'IGST', utgst: 'UTGST', 'cgst/sgst': 'CGST/SGST', 'cgst/sgst/igst': 'CGST/SGST/IGST',
    llp: 'LLP', brs: 'BRS', itc: 'ITC', tds: 'TDS', tcs: 'TCS', npo: 'NPO', vat: 'VAT', 'c/d': 'c/d', 'b/d': 'b/d', 'c/f': 'c/f', 'b/f': 'b/f', 'dr.': 'Dr.', 'cr.': 'Cr.', dr: 'Dr.', cr: 'Cr.',
    'm/s': 'M/s', 'm/s.': 'M/s.', 'ltd.': 'Ltd.', ltd: 'Ltd', 'pvt.': 'Pvt.', 'co.': 'Co.', 'p&l': 'P&L', 'b/r': 'B/R', 'b/p': 'B/P', 'r&p': 'R&P', 'i&e': 'I&E', ppe: 'PPE', huf: 'HUF', nrv: 'NRV', fifo: 'FIFO', 'w/o': 'w/o' };
  /* ICAI writes "Profit and Loss A/c", "Provision for Doubtful Debts A/c": these joining words stay lower case unless first.
     To capitalise literally every word, empty this set. */
  const SMALL = new Set(['and', 'of', 'for', 'to', 'on', 'in', 'the', 'by', 'at', 'as', 'from', 'over', 'with', 'a', 'an', 'or']);
  function tcWord(w, first) {
    const lo = w.toLowerCase(); if (KEEP[lo]) return KEEP[lo];
    const m = /^([("'“‘\[]*)(.*?)([)"'”’\],:;]*)$/.exec(w);
    if (m && m[2] && (m[1] || m[3])) { const k = m[2].toLowerCase(); if (KEEP[k]) return m[1] + KEEP[k] + m[3]; }
    if (!first && SMALL.has(lo)) return lo;
    if (/[A-Z]/.test(w) && w === w.toUpperCase() && w.replace(/[^A-Z]/g, '').length >= 2) return w;   // acronym typed in capitals
    return w.split(/([\-\/])/).map((part, pi) => { const k = part.toLowerCase(); if (KEEP[k]) return KEEP[k]; if (pi > 0 && SMALL.has(k)) return k; const i = part.search(/[A-Za-z]/); return i < 0 ? part : part.slice(0, i) + part[i].toUpperCase() + part.slice(i + 1); }).join('');
  }
  const titleCase = s => String(s || '').replace(/\s+/g, ' ').trim().split(' ').filter(Boolean).map((w, i) => tcWord(w, i === 0)).join(' ');
  const stripPre = s => String(s || '').replace(/^\s*(to|by)\s+/i, '');
  const withAc = s => (s && !/\bA\/cs?\.?$/i.test(s) && !/^(Sundries|Balance [bc]\/[df])$/i.test(s) ? s + ' A/c' : s);
  function narr(s) {
    s = String(s || '').trim(); if (!s) return '';
    if (/^\(.*\)$/.test(s)) return s;
    s = s.replace(/^\(|\)$/g, '').trim(); if (!/^being\b/i.test(s)) s = 'Being ' + s.charAt(0).toLowerCase() + s.slice(1);
    return `(${s.charAt(0).toUpperCase() + s.slice(1)})`;
  }

  /* ---------- column helpers ---------- */
  const C_ = (h, t, o) => Object.assign({ h, t }, o || {});
  const DT = (h = 'Date') => C_(h, 'date');
  const PA = (h = 'Particulars') => C_(h, 'acct');
  const TX = h => C_(h, 'text');
  const LF = (h = 'L.F.') => C_(h, 'lf');
  const AM = (h, o) => C_(h, 'amt', o);
  const QT = h => C_(h, 'qty', { tot: false });
  const RT = (h = 'Rate (₹)') => C_(h, 'amt', { tot: false, rate: true });
  const DET = AM('Details (₹)', { tot: false, bal: false });
  const sumRow = (nums, a, b) => { let s = 0; for (let i = a; i <= b; i++) s += nums[i] || 0; return s; };
  const off = (a, b) => Math.abs(a - b) >= 0.005;

  /* ---------- the templates ---------- */
  const G = { orig: 'Books of original entry', cash: 'Cash books', led: 'Ledger and trial balance', brs: 'Bank reconciliation', fin: 'Final accounts', npo: 'Not-for-profit organisations',
    inc: 'Incomplete records', part: 'Partnership', dep: 'Depreciation', inv: 'Inventory', oth: 'Other' };
  const TPL = [
    { id: 'journal', g: G.orig, name: 'Journal', kind: 'journal', hint: 'Debit lines first with “Dr.”, then credit lines indented “To … A/c”, then the narration (Being …). Each entry must balance.' },
    { id: 'jproper', g: G.orig, name: 'Journal Proper', kind: 'journal', hint: 'For entries no other book records: opening, closing, adjusting, rectification and transfer entries, credit purchase of assets, dishonour of bills.' },
    { id: 'purch', g: G.orig, name: 'Purchases Book', kind: 'grid', cols: [DT(), TX('Invoice No.'), PA('Particulars (Name of Supplier)'), LF(), DET, AM('Amount (₹)')], foot: 'Total — debited to Purchases A/c', hint: 'Only credit purchases of goods dealt in. Show trade discount in Details; it is never recorded separately.' },
    { id: 'purchgst', g: G.orig, name: 'Purchases Book (with GST)', kind: 'grid', cols: [DT(), PA(), TX('Invoice No.'), LF(), AM('Purchase Value (₹)'), AM('Freight (₹)'), AM('Input CGST (₹)'), AM('Input SGST (₹)'), AM('Input IGST (₹)'), AM('Total (₹)')], foot: 'Total',
      rowCheck: n => n[9] != null && off(sumRow(n, 4, 8), n[9]) ? 'Total is not the sum of value, freight and GST' : '', hint: 'Intra-state supply: CGST + SGST. Inter-state: IGST.' },
    { id: 'sales', g: G.orig, name: 'Sales Book', kind: 'grid', cols: [DT(), TX('Invoice No.'), PA('Particulars (Name of Customer)'), LF(), DET, AM('Amount (₹)')], foot: 'Total — credited to Sales A/c', hint: 'Only credit sales of goods dealt in. Cash sales go to the Cash Book; sale of an old asset is journalised.' },
    { id: 'salesgst', g: G.orig, name: 'Sales Book (with GST)', kind: 'grid', cols: [DT(), PA(), TX('Invoice No.'), LF(), AM('Sale Value (₹)'), AM('Freight (₹)'), AM('Output CGST (₹)'), AM('Output SGST (₹)'), AM('Output IGST (₹)'), AM('Total (₹)')], foot: 'Total',
      rowCheck: n => n[9] != null && off(sumRow(n, 4, 8), n[9]) ? 'Total is not the sum of value, freight and GST' : '', hint: 'Intra-state supply: CGST + SGST. Inter-state: IGST.' },
    { id: 'pret', g: G.orig, name: 'Purchases Returns (Returns Outward) Book', kind: 'grid', cols: [DT(), TX('Debit Note No.'), PA('Name of Supplier'), LF(), AM('Amount (₹)')], foot: 'Total — credited to Purchases Returns A/c', hint: 'A debit note is issued to the supplier for goods returned.' },
    { id: 'sret', g: G.orig, name: 'Sales Returns (Returns Inward) Book', kind: 'grid', cols: [DT(), TX('Credit Note No.'), PA('Name of Customer'), LF(), AM('Amount (₹)')], foot: 'Total — debited to Sales Returns A/c', hint: 'A credit note is issued to the customer for goods returned.' },
    { id: 'brb', g: G.orig, name: 'Bills Receivable Book', kind: 'grid', cols: [DT('Date of Receipt'), TX('Voucher No.'), PA('Party from whom Received'), PA('Acceptor'), DT('Date of Bill'), DT('Due Date'), TX('Place of Payment'), AM('Amount (₹)'), LF(), TX('Mode of Disposal')], foot: 'Total — debited to Bills Receivable A/c',
      rowCheck: (n, r) => { const a = parseDate(r[4]), b = parseDate(r[5]); return a.iso && b.iso && b.iso < a.iso ? 'Due date is before the date of the bill' : ''; }, hint: 'Due date = date of bill + term + 3 days of grace.' },
    { id: 'bpb', g: G.orig, name: 'Bills Payable Book', kind: 'grid', cols: [DT('Date of Acceptance'), PA('Drawer'), PA('Payee'), DT('Date of Bill'), DT('Due Date'), TX('Place of Payment'), AM('Amount (₹)'), LF(), TX('Mode of Disposal')], foot: 'Total — credited to Bills Payable A/c',
      rowCheck: (n, r) => { const a = parseDate(r[3]), b = parseDate(r[4]); return a.iso && b.iso && b.iso < a.iso ? 'Due date is before the date of the bill' : ''; }, hint: 'Due date = date of bill + term + 3 days of grace.' },

    { id: 'cb1', g: G.cash, name: 'Simple Cash Book', kind: 'tacc', cols: [DT(), PA(), LF(), AM('Amount (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, ac: 'Cash Book', hint: 'Receipts on the debit side, payments on the credit side. Cash can never show a credit balance.' },
    { id: 'cb2', g: G.cash, name: 'Two-column Cash Book (Cash and Bank)', kind: 'tacc', cols: [DT(), PA(), LF(), AM('Cash (₹)'), AM('Bank (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, ac: 'Cash Book', hint: 'Write “C” in the L.F. column for contra entries (cash deposited into or withdrawn from the bank).' },
    { id: 'cb3', g: G.cash, name: 'Three-column Cash Book (Discount, Cash, Bank)', kind: 'tacc', cols: [DT(), PA(), LF(), AM('Discount (₹)', { bal: false }), AM('Cash (₹)'), AM('Bank (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, ac: 'Cash Book',
      hint: 'Discount columns are only totalled, never balanced: Dr total = discount allowed, Cr total = discount received. “C” in L.F. marks a contra entry.' },
    { id: 'petty', g: G.cash, name: 'Petty Cash Book (analytical, imprest)', kind: 'grid', cols: [AM('Receipts (₹)'), DT(), TX('V. No.'), PA(), AM('Total (₹)'), AM('Conveyance (₹)', { edit: 1 }), AM('Cartage (₹)', { edit: 1 }), AM('Stationery (₹)', { edit: 1 }), AM('Postage (₹)', { edit: 1 }), AM('Sundries (₹)', { edit: 1 })], foot: 'Total', addCol: 'amt',
      rowCheck: n => { const a = n.slice(5); return n[4] != null && a.some(x => x != null) && off(a.reduce((s, x) => s + (x || 0), 0), n[4]) ? 'Total is not the sum of the analysis columns' : ''; },
      check: (S, T) => { const rec = T[0] || 0, pay = T[4] || 0; return rec || pay ? { ok: true, msg: `Receipts ₹${inr(rec)} − payments ₹${inr(pay)} = balance c/d ₹${inr(rec - pay)}. Under the imprest system the reimbursement equals the payments of the period.` } : null; },
      hint: 'Rename the analysis columns to match the question (tap a heading). Each row’s Total must equal its analysis columns.' },

    { id: 'ledger', g: G.led, name: 'Ledger account (T-account)', kind: 'tacc', cols: [DT(), PA(), LF('J.F.'), AM('Amount (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, acIn: 1, multi: 1, hint: 'Debit side “To …”, credit side “By …” — name the other account of the entry. Balance with “Balance c/d”; bring it down as “Balance b/d”.' },
    { id: 'tb', g: G.led, name: 'Trial Balance', kind: 'grid', cols: [PA(), LF(), AM('Dr. Amount (₹)'), AM('Cr. Amount (₹)')], foot: 'Total',
      check: (S, T) => (T[2] || T[3] ? (off(T[2], T[3]) ? { ok: false, msg: `Dr. ₹${inr(T[2])} and Cr. ₹${inr(T[3])} differ by ₹${inr(Math.abs(T[2] - T[3]))} — the trial balance does not agree.` } : { ok: true, msg: `Dr. = Cr. = ₹${inr(T[2])} — the trial balance agrees.` }) : null),
      title: 'Trial Balance of … as at …', hint: 'Assets, expenses, losses and drawings have debit balances; capital, liabilities, incomes and gains have credit balances.' },

    { id: 'brs', g: G.brs, name: 'Bank Reconciliation Statement', kind: 'brs', title: 'Bank Reconciliation Statement as at …', hint: '“Add” items raise the balance you started from (or the overdraft, when you start from an overdraft); “Less” items reduce it.' },

    { id: 'trading', g: G.fin, name: 'Trading Account', kind: 'tacc', cols: [PA(), DET, AM('Amount (₹)')], bal: { l: 'Gross Profit c/d', r: 'Gross Loss c/d' }, title: 'Trading Account for the year ended …', hint: 'Gross profit is carried down to the Profit and Loss Account.' },
    { id: 'pl', g: G.fin, name: 'Profit and Loss Account', kind: 'tacc', cols: [PA(), DET, AM('Amount (₹)')], bal: { l: 'Net Profit transferred to Capital A/c', r: 'Net Loss transferred to Capital A/c' }, title: 'Profit and Loss Account for the year ended …', hint: 'Start with Gross Profit b/d (credit side) or Gross Loss b/d (debit side).' },
    { id: 'bsh', g: G.fin, name: 'Balance Sheet (horizontal)', kind: 'tacc', sides: ['Liabilities', 'Assets'], cols: [PA(), DET, AM('Amount (₹)')], pre: null, title: 'Balance Sheet as at …', hint: 'Liabilities and capital on the left, assets on the right. Both totals must agree.' },
    { id: 'bss3', g: G.fin, name: 'Balance Sheet — Schedule III (company)', kind: 'grid', fixed: 's3', cols: [C_('Particulars', 'label'), TX('Note No.'), AM('Figures as at the end of the current reporting period (₹)'), AM('Figures as at the end of the previous reporting period (₹)')], title: '… Ltd — Balance Sheet as at …',
      hint: 'Schedule III, Division I. Give the detail of share capital, reserves and other items in the Notes to Accounts.' },

    { id: 'rp', g: G.npo, name: 'Receipts and Payments Account', kind: 'tacc', sides: ['Receipts', 'Payments'], cols: [PA(), DET, AM('Amount (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d' }, title: 'Receipts and Payments Account for the year ended …', hint: 'A summary of the cash book: capital and revenue items, of any year, actually received or paid. Opens with the opening cash and bank balance.' },
    { id: 'ie', g: G.npo, name: 'Income and Expenditure Account', kind: 'tacc', sides: ['Expenditure', 'Income'], cols: [PA(), DET, AM('Amount (₹)')], bal: { l: 'Surplus — Excess of Income over Expenditure', r: 'Deficit — Excess of Expenditure over Income' }, title: 'Income and Expenditure Account for the year ended …', hint: 'Revenue items of this year only (accrual basis), like a Profit and Loss Account.' },

    { id: 'soa', g: G.inc, name: 'Statement of Affairs', kind: 'tacc', sides: ['Liabilities', 'Assets'], cols: [PA(), DET, AM('Amount (₹)')], pre: null, bal: { l: 'Capital (balancing figure)', r: 'Deficiency (balancing figure)' }, title: 'Statement of Affairs as at …', hint: 'Capital is the balancing figure: assets − outside liabilities.' },

    { id: 'capital', g: G.part, name: 'Partners’ Capital A/cs (columnar)', kind: 'tacc', partners: 1, cols: [DT(), PA()], heads: ['A', 'B'], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, variant: ['Partners’ Capital A/cs (fluctuating capital)', 'Partners’ Capital A/cs (fixed capital)', 'Partners’ Current A/cs (fixed capital method)'],
      hint: 'Fluctuating method: interest, salary, share of profit and drawings all go to the Capital A/c. Fixed method: those go to the Current A/c; the Capital A/c changes only for capital introduced or withdrawn.' },
    { id: 'appr', g: G.part, name: 'Profit and Loss Appropriation A/c', kind: 'tacc', cols: [PA(), DET, AM('Amount (₹)')], bal: { l: 'Profit transferred to Partners’ Capital A/cs', r: 'Loss transferred to Partners’ Capital A/cs' }, title: 'Profit and Loss Appropriation Account for the year ended …', hint: 'Credit: net profit, interest on drawings. Debit: interest on capital, salary, commission, then the divisible profit in the profit-sharing ratio.' },
    { id: 'reval', g: G.part, name: 'Revaluation A/c', kind: 'tacc', cols: [PA(), AM('Amount (₹)')], bal: { l: 'Profit on Revaluation transferred to Partners’ Capital A/cs', r: 'Loss on Revaluation transferred to Partners’ Capital A/cs' }, ac: 'Revaluation A/c', hint: 'Decrease in assets and increase in liabilities on the debit side; increase in assets and decrease in liabilities on the credit side. Share the result in the old ratio.' },
    { id: 'realis', g: G.part, name: 'Realisation A/c', kind: 'tacc', cols: [PA(), AM('Amount (₹)')], bal: { l: 'Profit on Realisation transferred to Partners’ Capital A/cs', r: 'Loss on Realisation transferred to Partners’ Capital A/cs' }, ac: 'Realisation A/c', hint: 'Debit: assets (except cash, bank and fictitious assets) at book value, liabilities paid, expenses. Credit: liabilities (except partners’ items) at book value, assets realised.' },

    { id: 'depsched', g: G.dep, name: 'Depreciation schedule', kind: 'grid', cols: [TX('Year'), AM('Opening Book Value (₹)', { tot: false }), AM('Additions (₹)'), AM('Depreciation (₹)'), AM('Closing Book Value (₹)', { tot: false })], foot: 'Total',
      rowCheck: n => n[1] != null && n[3] != null && n[4] != null && off(n[1] + (n[2] || 0) - n[3], n[4]) ? 'Opening + additions − depreciation ≠ closing' : '',
      check: S => { const rows = S.data.rows.filter(r => r.c.some(x => String(x || '').trim())); for (let i = 1; i < rows.length; i++) { const a = parseAmt(rows[i - 1].c[4]), b = parseAmt(rows[i].c[1]); if (a != null && b != null && !isNaN(a) && !isNaN(b) && off(a, b)) return { ok: false, msg: `Year ${i + 1}: the opening book value should equal last year’s closing book value (₹${inr(a)}).` }; } return null; },
      hint: 'Straight line: the same amount each year. Written down value: the rate on the opening book value. Time basis for part of a year.' },
    { id: 'asset', g: G.dep, name: 'Asset A/c / Provision for Depreciation A/c', kind: 'tacc', cols: [DT(), PA(), LF('J.F.'), AM('Amount (₹)')], bal: { l: 'Balance c/d', r: 'Balance c/d', bd: 1 }, acIn: 1, acDefault: 'Machinery A/c', multi: 1, hint: 'Without a provision: depreciation is credited to the Asset A/c. With a provision: the Asset A/c stays at cost and depreciation is credited to the Provision for Depreciation A/c.' },

    { id: 'stores', g: G.inv, name: 'Stores ledger (FIFO / weighted average)', kind: 'grid', groups: [['', 1], ['Receipts', 3], ['Issues', 3], ['Balance', 3]], cols: [DT(), QT('Qty'), RT(), AM('Amount (₹)'), QT('Qty'), RT(), AM('Amount (₹)'), QT('Qty'), RT(), AM('Amount (₹)', { tot: false })], foot: 'Total',
      variant: ['Stores Ledger — FIFO', 'Stores Ledger — Weighted average'],
      rowCheck: n => { for (const [q, r, a] of [[1, 2, 3], [4, 5, 6], [7, 8, 9]]) if (n[q] != null && n[r] != null && n[a] != null && off(n[q] * n[r], n[a])) return 'Quantity × rate ≠ amount'; return ''; },
      check: (S, T) => { const rq = S.data.rows.reduce((a, r) => a + num(r.c[1]), 0), iq = S.data.rows.reduce((a, r) => a + num(r.c[4]), 0); return rq || iq ? { ok: true, msg: `Received ${inr(rq)} units (₹${inr(T[3] || 0)}) · issued ${inr(iq)} units (₹${inr(T[6] || 0)}). FIFO: issue from the oldest lot first, a separate line for each lot. Weighted average: a new average rate after every receipt.` } : null; },
      hint: 'Enter the opening balance in the Balance columns of the first row.' },

    { id: 'compare', g: G.oth, name: 'Comparison table (distinguish between)', kind: 'grid', cols: [TX('Basis of Distinction'), C_('…', 'text', { edit: 1 }), C_('…', 'text', { edit: 1 })], addCol: 'text', foot: false, rows: 4, hint: 'Rename the two headings (tap them), one basis per row — the same basis for both sides.' },
    { id: 'blank', g: G.oth, name: 'Blank table', kind: 'grid', cols: [C_('Particulars', 'acct', { edit: 1 }), AM('Details (₹)', { tot: false, edit: 1 }), AM('Amount (₹)', { edit: 1 })], addCol: 'amt', foot: 'Total', hint: 'Tap a heading to rename it; add columns as needed.' }
  ];
  const byId = id => TPL.find(t => t.id === id);

  /* Schedule III (Division I) balance sheet lines, as in the ICAI study material */
  const S3 = (() => {
    const L = []; const h = (label, lvl = 0) => L.push({ k: 'h', label, lvl }); const i = (label, sec, lvl = 1) => L.push({ k: 'in', label, sec, lvl }); const t = (label, sec) => L.push({ k: 'tot', label, sec });
    h('I. EQUITY AND LIABILITIES'); h('(1) Shareholders’ Funds', 1); i('(a) Share Capital', 'I', 2); i('(b) Reserves and Surplus', 'I', 2); i('(c) Money Received against Share Warrants', 'I', 2);
    i('(2) Share Application Money Pending Allotment', 'I', 1);
    h('(3) Non-current Liabilities', 1); i('(a) Long-term Borrowings', 'I', 2); i('(b) Deferred Tax Liabilities (Net)', 'I', 2); i('(c) Other Long-term Liabilities', 'I', 2); i('(d) Long-term Provisions', 'I', 2);
    h('(4) Current Liabilities', 1); i('(a) Short-term Borrowings', 'I', 2); h('(b) Trade Payables', 2); i('(A) Total outstanding dues of micro enterprises and small enterprises', 'I', 3); i('(B) Total outstanding dues of creditors other than micro enterprises and small enterprises', 'I', 3);
    i('(c) Other Current Liabilities', 'I', 2); i('(d) Short-term Provisions', 'I', 2); t('Total', 'I');
    h('II. ASSETS'); h('(1) Non-current Assets', 1); h('(a) Property, Plant and Equipment and Intangible Assets', 2); i('(i) Property, Plant and Equipment', 'II', 3); i('(ii) Intangible Assets', 'II', 3); i('(iii) Capital Work-in-progress', 'II', 3); i('(iv) Intangible Assets under Development', 'II', 3);
    i('(b) Non-current Investments', 'II', 2); i('(c) Deferred Tax Assets (Net)', 'II', 2); i('(d) Long-term Loans and Advances', 'II', 2); i('(e) Other Non-current Assets', 'II', 2);
    h('(2) Current Assets', 1); i('(a) Current Investments', 'II', 2); i('(b) Inventories', 'II', 2); i('(c) Trade Receivables', 'II', 2); i('(d) Cash and Cash Equivalents', 'II', 2); i('(e) Short-term Loans and Advances', 'II', 2); i('(f) Other Current Assets', 'II', 2); t('Total', 'II');
    return L;
  })();

  /* ---------- which template fits a question ---------- */
  const RULES = [
    [/distinguish|differentiate|difference between|differences between/i, 'compare'],
    [/bank reconciliation|\bBRS\b/i, 'brs'], [/petty cash/i, 'petty'], [/three[- ]column cash|cash book with (cash discount|discount)|discount,? cash and bank/i, 'cb3'],
    [/two[- ]column cash|double[- ]column cash|cash book with cash and bank/i, 'cb2'], [/(simple|single[- ]column) cash book/i, 'cb1'],
    [/purchases? returns? book|returns? outwards? book/i, 'pret'], [/sales returns? book|returns? inwards? book/i, 'sret'],
    [/purchases? (book|day book)/i, 'purch'], [/sales (book|day book)/i, 'sales'], [/subsidiary books?|appropriate books? of original entry/i, 'purch'],
    [/bills? receivable book/i, 'brb'], [/bills? payable book/i, 'bpb'],
    [/receipts? (and|&) payments? (account|a\/c)/i, 'rp'], [/income (and|&) expenditure (account|a\/c)/i, 'ie'], [/statement of affairs/i, 'soa'],
    [/appropriation/i, 'appr'], [/revaluation (account|a\/c)/i, 'reval'], [/reali[sz]ation (account|a\/c)/i, 'realis'],
    [/(capital|current) (accounts|a\/cs)|partners['’]? capital/i, 'capital'],
    [/schedule iii|division i\b/i, 'bss3'], [/trading (account|a\/c)|trading and profit/i, 'trading'], [/profit (and|&) loss (account|a\/c)(?!\s*appropriation)/i, 'pl'],
    [/balance sheet/i, 'bsh'], [/trial balance/i, 'tb'], [/depreciation schedule|schedule of depreciation|book value (at|for) (the end of )?each year/i, 'depsched'],
    [/(machinery|machine|asset|furniture|plant|vehicle|building|provision for depreciation) (account|a\/c)/i, 'asset'],
    [/fifo|weighted average|stores ledger|stock ledger|inventory (ledger|record)/i, 'stores'], [/cash book/i, 'cb1'],
    [/\bledger\b|post (them|it|these|the entries) (in)?to/i, 'ledger'], [/journal/i, 'journal']
  ];
  const TACC = new Set(TPL.filter(t => t.kind === 'tacc').map(t => t.id));
  function suggest(pad, text) {
    text = String(text || '');
    const hits = []; RULES.forEach(([re, id]) => { const m = re.exec(text); if (m && !hits.some(h => h.id === id)) hits.push({ id, at: m.index }); });
    if (hits.some(h => h.id === 'appr')) { const i = hits.findIndex(h => h.id === 'pl'); if (i >= 0 && !/profit (and|&) loss (account|a\/c)(?!\s*appropriation)[\s\S]*profit (and|&) loss/i.test(text)) hits.splice(i, 1); }
    if (/gst|cgst|sgst|igst/i.test(text)) hits.forEach(h => { if (h.id === 'purch') h.id = 'purchgst'; if (h.id === 'sales') h.id = 'salesgst'; });
    if (hits.some(h => h.id === 'purch' || h.id === 'purchgst') && /\bsold\b|sales/i.test(text) && !hits.some(h => /^sales/.test(h.id)) && /subsidiary|books of original/i.test(text)) hits.push({ id: /gst/i.test(text) ? 'salesgst' : 'sales', at: 9e9 });
    hits.sort((a, b) => a.at - b.at);
    const drop = id => { const i = hits.findIndex(h => h.id === id); if (i >= 0) hits.splice(i, 1); };
    if (hits.some(h => h.id === 'cb2' || h.id === 'cb3' || h.id === 'petty')) drop('cb1');
    if (hits.some(h => h.id === 'stores')) drop('ledger');
    if (/from the (following |given |above )?trial balance/i.test(text) && hits.some(h => ['trading', 'pl', 'bsh', 'bss3', 'rp', 'ie'].includes(h.id))) drop('tb');
    let ids = hits.map(h => h.id);
    if (pad === 'journal') ids = ['journal'].concat(ids.filter(i => i === 'ledger' || i === 'tb'));
    else if (pad === 'ledger') { ids = ids.filter(i => TACC.has(i)).concat(ids.filter(i => i === 'brs' || i === 'tb' || i === 'journal')); if (!ids.length) ids = ['ledger']; }
    else if (pad === 'tb') ids = ['tb'].concat(ids.filter(i => i !== 'tb' && i !== 'journal'));
    else if (pad === 'table' && !ids.length) ids = ['blank'];
    else if (pad === 'legal') ids = [];
    return [...new Set(ids)].slice(0, 4);
  }

  /* ---------- data ---------- */
  const blankRow = n => ({ c: Array(n).fill('') });
  function init(t) {
    if (t.kind === 'journal') return { title: t.title || '', entries: [newEntry()] };
    if (t.kind === 'brs') return { title: t.title || '', start: 'cb', od: false, amt: '', add: [{ p: '', v: '' }], less: [{ p: '', v: '' }], given: '' };
    if (t.kind === 'tacc') {
      const cols = t.partners ? t.cols.concat((t.heads || ['A', 'B']).map(h => AM(h, { edit: 1, partner: 1 }))) : t.cols.map(c => ({ ...c }));
      return { title: t.title || '', ac: t.acDefault || '', variant: 0, cols, rows: Array.from({ length: 4 }, () => ({ l: blankRow(cols.length), r: blankRow(cols.length) })) };
    }
    const cols = t.cols.map(c => ({ ...c }));
    if (t.fixed === 's3') return { title: t.title || '', cols, rows: S3.map(x => ({ ...x, c: Array(cols.length).fill('') })) };
    return { title: t.title || '', variant: 0, cols, rows: Array.from({ length: t.rows || 3 }, () => blankRow(cols.length)) };
  }
  function newEntry() { return { date: '', lines: [{ s: 'dr', ac: '', lf: '', amt: '' }, { s: 'cr', ac: '', lf: '', amt: '' }], narr: '' }; }

  /* ---------- cell HTML ---------- */
  let UID = 0;
  function cell(S, col, val, path, label, extra = '') {
    const id = `cp${S.uid}-${path.replace(/[^\w]/g, '_')}`;
    S.meta[path] = col.t;
    const base = `class="ca-pc ca-pc-${col.t}${extra}" id="${id}" data-p="${path}" aria-label="${e_(label)}" value="${e_(val)}" autocomplete="off" spellcheck="false"`;
    if (col.t === 'date') return `<span class="ca-pd-date"><input ${base} placeholder="dd-mmm-yy" maxlength="11" inputmode="text"><button type="button" class="ca-pd-cal" data-cal="${path}" aria-label="Choose a date: ${e_(label)}">📅</button><input type="date" class="ca-pd-native" data-nat="${path}" tabindex="-1" aria-hidden="true"></span>`;
    if (col.t === 'amt' || col.t === 'qty') return `<input ${base} inputmode="decimal">`;
    if (col.t === 'lf') return `<input ${base} maxlength="6">`;
    return `<input ${base}>`;
  }
  const tdN = (inner, cls = '') => `<td class="${cls}">${inner}</td>`;

  /* ---------- renderers ---------- */
  function headHTML(S) {
    const t = S.t, d = S.data;
    const opts = Object.values(G).map(g => `<optgroup label="${e_(g)}">${TPL.filter(x => x.g === g).map(x => `<option value="${x.id}" ${x.id === t.id ? 'selected' : ''}>${e_(x.name)}${S.pad.sug.includes(x.id) ? ' ★' : ''}</option>`).join('')}</optgroup>`).join('');
    return `<div class="ca-pd-top"><label class="ca-pd-lab" for="cpSel${S.uid}">Format</label><select class="ca-in ca-pd-sel" id="cpSel${S.uid}" data-act="tpl">${opts}</select>
      ${S.pad.sheets.length > 1 ? `<button type="button" class="ca-link ca-pd-rm" data-act="rmsheet" aria-label="Remove this table">Remove table</button>` : ''}</div>
      ${t.variant ? `<label class="ca-pd-lab" for="cpVar${S.uid}">Type</label><select class="ca-in ca-pd-sel" id="cpVar${S.uid}" data-act="variant">${t.variant.map((v, i) => `<option value="${i}" ${+d.variant === i ? 'selected' : ''}>${e_(v)}</option>`).join('')}</select>` : ''}
      <label class="ca-pd-lab" for="cpTitle${S.uid}">Heading</label><input class="ca-in ca-pd-title" id="cpTitle${S.uid}" data-act="title" value="${e_(d.title)}" placeholder="${e_(t.title || (t.variant ? t.variant[+d.variant || 0] : t.name) + ' — e.g. In the books of …')}" autocomplete="off">
      <p class="ca-pd-hint">${e_(t.hint || '')}</p>`;
  }

  function gridHTML(S) {
    const t = S.t, d = S.data, cols = d.cols, fixed = !!t.fixed;
    const groups = t.groups ? `<tr>${t.groups.map(([g, n]) => `<th scope="colgroup" colspan="${n}" class="ca-pd-grp">${e_(g)}</th>`).join('')}${fixed ? '' : '<th></th>'}</tr>` : '';
    const ths = cols.map((c, ci) => `<th scope="col" class="${c.t === 'amt' || c.t === 'qty' ? 'n' : ''} ca-pd-c-${c.t}">${c.edit ? `<input class="ca-pc ca-pc-head" data-p="h${ci}" aria-label="Column ${ci + 1} heading" value="${e_(c.h)}">` : e_(c.h)}${c.edit && t.addCol && ci >= t.cols.length ? ` <button type="button" class="ca-x" data-act="rmcol" data-c="${ci}" aria-label="Remove column ${ci + 1}">✕</button>` : ''}</th>`).join('');
    let body = '';
    d.rows.forEach((r, ri) => {
      if (r.k === 'h') { body += `<tr class="ca-pd-h ca-pd-l${r.lvl}"><th scope="row" colspan="${cols.length}">${e_(r.label)}</th></tr>`; return; }
      if (r.k === 'tot') { body += `<tr class="ca-tot"><th scope="row">${e_(r.label)}</th>${cols.slice(1).map((c, ci) => `<td class="n" data-calc="t${r.sec}-${ci + 1}">${c.t === 'amt' ? '' : ''}</td>`).join('')}</tr>`; return; }
      const lab = r.label ? r.label.replace(/^\([a-z]+\)\s*/i, '') : `Row ${ri + 1}`;
      body += `<tr data-r="${ri}" class="${r.k === 'in' ? `ca-pd-l${r.lvl}` : ''}">${cols.map((c, ci) => c.t === 'label' ? `<th scope="row" class="ca-pd-lbl">${e_(r.label)}</th>` : tdN(cell(S, c, r.c[ci], `r${ri}.${ci}`, `${lab}, ${c.h}`), c.t === 'amt' || c.t === 'qty' ? 'n' : '')).join('')}${fixed ? '' : `<td class="ca-pd-ops"><button type="button" class="ca-x" data-act="rmrow" data-r="${ri}" aria-label="Remove row ${ri + 1}">✕</button></td>`}</tr>`;
    });
    const foot = !fixed && t.foot !== false ? `<tfoot><tr>${cols.map((c, ci) => { const tot = (c.t === 'amt') && c.tot !== false; const lab = ci === cols.findIndex(x => x.t !== 'amt' && x.t !== 'qty'); return `<td class="${tot ? 'n' : ''}" ${tot ? `data-calc="T${ci}"` : ''}>${lab ? e_(t.foot) : ''}</td>`; }).join('')}<td></td></tr></tfoot>` : '';
    return `<div class="ca-scroll ca-pd-sc" role="region" tabindex="0" aria-label="${e_(t.name)} — scroll sideways for more columns"><table class="ca-t ca-pd-t ca-pd-grid ${fixed ? 'ca-pd-s3' : ''}"><thead>${groups}<tr>${ths}${fixed ? '' : '<th class="ca-pd-ops"><span class="sr-only">Remove</span></th>'}</tr></thead><tbody>${body}</tbody>${foot}</table></div>
      ${fixed ? '' : `<div class="ca-btns ca-pd-btns"><button type="button" class="btn ghost" data-act="addrow">+ Add row</button>${t.addCol ? '<button type="button" class="btn ghost" data-act="addcol">+ Add column</button>' : ''}</div>`}`;
  }

  function journalHTML(S) {
    const d = S.data; let rows = '';
    d.entries.forEach((en, ei) => {
      const lines = en.lines.map((l, li) => {
        const who = `Entry ${ei + 1}, ${l.s === 'dr' ? 'debit' : 'credit'} line`;
        const part = l.s === 'dr' ? `<span class="ca-pd-acw">${cell(S, { t: 'acctj' }, l.ac, `e${ei}.${li}.ac`, `${who}: account debited`)}<span class="ca-pd-suf" aria-hidden="true">Dr.</span></span>`
          : `<span class="ca-pd-acw ca-pd-to"><span class="ca-pd-pre" aria-hidden="true">To</span>${cell(S, { t: 'acctj' }, l.ac, `e${ei}.${li}.ac`, `${who}: account credited`)}</span>`;
        return `<tr class="ca-pd-${l.s}">${tdN(li === 0 ? cell(S, { t: 'date' }, en.date, `e${ei}.date`, `Entry ${ei + 1}: date`) : '')}${tdN(part, 'ca-pd-part')}${tdN(cell(S, { t: 'lf' }, l.lf, `e${ei}.${li}.lf`, `${who}: L.F.`))}
          ${tdN(l.s === 'dr' ? cell(S, { t: 'amt' }, l.amt, `e${ei}.${li}.amt`, `${who}: Dr. amount`) : '', 'n')}${tdN(l.s === 'cr' ? cell(S, { t: 'amt' }, l.amt, `e${ei}.${li}.amt`, `${who}: Cr. amount`) : '', 'n')}
          <td class="ca-pd-ops"><button type="button" class="ca-x" data-act="rmline" data-e="${ei}" data-l="${li}" aria-label="Remove ${who} ${li + 1}">✕</button></td></tr>`;
      }).join('');
      rows += `<tbody class="ca-pd-je" data-e="${ei}">${lines}<tr class="ca-pd-narr"><td></td><td colspan="4">${cell(S, { t: 'narr' }, en.narr, `e${ei}.narr`, `Entry ${ei + 1}: narration`)}</td><td></td></tr>
        <tr class="ca-pd-act"><td colspan="6"><div class="ca-pd-actin"><button type="button" class="ca-link" data-act="adddr" data-e="${ei}">+ Dr. line</button><button type="button" class="ca-link" data-act="addcr" data-e="${ei}">+ Cr. line</button><span class="ca-pd-est" data-calc="e${ei}"></span><button type="button" class="ca-link ca-pd-rme" data-act="rmentry" data-e="${ei}" aria-label="Remove entry ${ei + 1}">Remove entry</button></div></td></tr></tbody>`;
    });
    return `<div class="ca-scroll ca-pd-sc" role="region" tabindex="0" aria-label="Journal — scroll sideways for more columns"><table class="ca-t ca-pd-t ca-pd-j"><thead><tr><th scope="col" class="ca-pd-c-date">Date</th><th scope="col" class="ca-pd-c-part">Particulars</th><th scope="col" class="ca-pd-c-lf">L.F.</th><th scope="col" class="n ca-pd-c-amt">Dr. Amount (₹)</th><th scope="col" class="n ca-pd-c-amt">Cr. Amount (₹)</th><th class="ca-pd-ops"><span class="sr-only">Remove</span></th></tr></thead>
      ${rows}<tfoot><tr><td></td><td>Total</td><td></td><td class="n" data-calc="dr"></td><td class="n" data-calc="cr"></td><td></td></tr></tfoot></table></div>
      <div class="ca-btns ca-pd-btns"><button type="button" class="btn ghost" data-act="addentry">+ New entry</button></div>`;
  }

  function taccHTML(S) {
    const t = S.t, d = S.data, cols = d.cols, n = cols.length, sides = t.sides || ['Dr.', 'Cr.'], pre = t.pre === null ? null : ['To', 'By'];
    const hcell = (c, ci, side) => `<th scope="col" class="${c.t === 'amt' ? 'n' : ''} ca-pd-c-${c.t}${side === 'r' && ci === 0 ? ' ca-pd-mid' : ''}">${c.edit && side === 'l' ? `<input class="ca-pc ca-pc-head" data-p="h${ci}" aria-label="Column heading: ${e_(c.h)}" value="${e_(c.h)}">` : `<span ${c.edit ? `data-calc="hh${ci}"` : ''}>${e_(c.t === 'acct' && t.sides ? sides[side === 'l' ? 0 : 1] : c.h)}</span>`}${c.partner && side === 'l' && cols.filter(x => x.partner).length > 2 ? ` <button type="button" class="ca-x" data-act="rmcol" data-c="${ci}" aria-label="Remove partner column ${e_(c.h)}">✕</button>` : ''}</th>`;
    const sideCells = (row, side, ri) => cols.map((c, ci) => {
      const lab = `Row ${ri + 1}, ${side === 'l' ? sides[0] : sides[1]} side, ${c.t === 'acct' ? 'particulars' : c.h}`;
      let inner = cell(S, c, row.c[ci], `r${ri}.${side}.${ci}`, lab);
      if (c.t === 'acct' && pre) inner = `<span class="ca-pd-acw"><span class="ca-pd-pre" aria-hidden="true">${pre[side === 'l' ? 0 : 1]}</span>${inner}</span>`;
      return tdN(inner, `${c.t === 'amt' ? 'n' : ''}${side === 'r' && ci === 0 ? ' ca-pd-mid' : ''}${c.t === 'acct' ? ' ca-pd-part' : ''}`);
    }).join('');
    const body = d.rows.map((row, ri) => `<tr data-r="${ri}" class="${row.auto ? 'ca-bal' : ''}">${sideCells(row.l, 'l', ri)}${sideCells(row.r, 'r', ri)}<td class="ca-pd-ops"><button type="button" class="ca-x" data-act="rmrow" data-r="${ri}" aria-label="Remove row ${ri + 1}">✕</button></td></tr>`).join('');
    const foot = side => cols.map((c, ci) => `<td class="${c.t === 'amt' ? 'n' : ''}${side === 'r' && ci === 0 ? ' ca-pd-mid' : ''}" ${c.t === 'amt' ? `data-calc="${side}${ci}"` : ''}>${c.t === 'acct' ? 'Total' : ''}</td>`).join('');
    const acHead = t.acIn ? `<div class="ca-pd-ach"><span>${e_(sides[0])}</span><input class="ca-in ca-pc ca-pc-acname" data-p="ac" value="${e_(d.ac)}" placeholder="Account name, e.g. ${e_(t.acDefault || 'Cash A/c')}" aria-label="Name of the account"><span>${e_(sides[1])}</span></div>`
      : `<div class="ca-pd-ach"><span>${e_(t.sides ? '' : sides[0])}</span><b data-calc="achead">${e_(d.title || (t.variant ? t.variant[+d.variant || 0] : t.ac || t.name))}</b><span>${e_(t.sides ? '' : sides[1])}</span></div>`;
    return `${acHead}<p class="ca-pd-swipe" aria-hidden="true">⇆ Swipe the table sideways for the ${e_(sides[1])} side</p><div class="ca-scroll ca-pd-sc" role="region" tabindex="0" aria-label="${e_(t.name)} — both sides; scroll sideways for the right-hand side"><table class="ca-t ca-pd-t ca-pd-ta"><thead><tr><th scope="colgroup" colspan="${n}" class="ca-pd-side">${e_(sides[0])}</th><th scope="colgroup" colspan="${n}" class="ca-pd-side ca-pd-mid">${e_(sides[1])}</th><th></th></tr>
      <tr>${cols.map((c, ci) => hcell(c, ci, 'l')).join('')}${cols.map((c, ci) => hcell(c, ci, 'r')).join('')}<th class="ca-pd-ops"><span class="sr-only">Remove</span></th></tr></thead><tbody>${body}</tbody>
      <tfoot><tr>${foot('l')}${foot('r')}<td></td></tr></tfoot></table></div><p class="ca-pd-bd" data-calc="bd"></p>
      <div class="ca-btns ca-pd-btns"><button type="button" class="btn ghost" data-act="addrow">+ Add row</button>${t.bal ? `<button type="button" class="btn ghost" data-act="balance">⚖ Balance it</button>` : ''}${t.partners ? '<button type="button" class="btn ghost" data-act="addpartner">+ Partner</button>' : ''}${t.multi ? '<button type="button" class="btn ghost" data-act="dupsheet">+ Another account</button>' : ''}</div>`;
  }

  function brsLabels(d) {
    const other = d.start === 'cb' ? 'pb' : 'cb';
    const L = (k, od) => k === 'cb' ? (od ? 'Overdraft as per Cash Book (Cr.)' : 'Balance as per Cash Book (Dr.)') : (od ? 'Overdraft as per Pass Book (Dr.)' : 'Balance as per Pass Book (Cr.)');
    return { start: L(d.start, d.od), res: v => L(other, d.od ? v >= 0 : v < 0), other: other === 'pb' ? 'Pass Book' : 'Cash Book' };
  }
  function brsHTML(S) {
    const d = S.data, L = brsLabels(d);
    const items = (k, nm) => d[k].map((it, i) => `<tr>${tdN(cell(S, { t: 'text' }, it.p, `${k}${i}.p`, `${nm} item ${i + 1}: particulars`), 'ca-pd-brsp')}${tdN(cell(S, { t: 'amt' }, it.v, `${k}${i}.v`, `${nm} item ${i + 1}: amount`), 'n')}<td class="n"></td><td class="ca-pd-ops"><button type="button" class="ca-x" data-act="rmbrs" data-k="${k}" data-i="${i}" aria-label="Remove ${nm} item ${i + 1}">✕</button></td></tr>`).join('');
    return `<div class="ca-pd-brso"><label class="ca-pd-lab" for="cpBs${S.uid}">Start from</label><select class="ca-in ca-pd-sel" id="cpBs${S.uid}" data-act="brsstart"><option value="cb" ${d.start === 'cb' ? 'selected' : ''}>Balance as per Cash Book</option><option value="pb" ${d.start === 'pb' ? 'selected' : ''}>Balance as per Pass Book</option></select>
      <label class="ca-pd-chk"><input type="checkbox" data-act="brsod" ${d.od ? 'checked' : ''}> The starting balance is an overdraft</label></div>
      <div class="ca-scroll ca-pd-sc" role="region" tabindex="0" aria-label="Bank Reconciliation Statement"><table class="ca-t ca-pd-t ca-pd-brs"><thead><tr><th scope="col">Particulars</th><th scope="col" class="n">Details (₹)</th><th scope="col" class="n">Amount (₹)</th><th class="ca-pd-ops"><span class="sr-only">Remove</span></th></tr></thead><tbody>
        <tr><th scope="row" class="ca-pd-lbl">${e_(L.start)}</th><td></td>${tdN(cell(S, { t: 'amt' }, d.amt, 'amt', L.start), 'n')}<td></td></tr>
        <tr class="ca-pd-h"><th scope="row" colspan="4">Add:</th></tr>${items('add', 'Add')}<tr><td><button type="button" class="ca-link" data-act="addbrs" data-k="add">+ Add item</button></td><td class="ca-pd-sublbl">Total additions</td><td class="n" data-calc="addT"></td><td></td></tr>
        <tr class="ca-pd-h"><th scope="row" colspan="4">Less:</th></tr>${items('less', 'Less')}<tr><td><button type="button" class="ca-link" data-act="addbrs" data-k="less">+ Add item</button></td><td class="ca-pd-sublbl">Total deductions</td><td class="n" data-calc="lessT"></td><td></td></tr>
      </tbody><tfoot><tr><td data-calc="resL"></td><td></td><td class="n" data-calc="res"></td><td></td></tr></tfoot></table></div>
      <label class="ca-pd-lab" for="cp${S.uid}-given">Balance as per ${e_(L.other)} given in the question (optional — to check your statement)</label>${cell(S, { t: 'amt' }, d.given, 'given', `Balance as per ${L.other} given in the question`, ' ca-in ca-pd-given')}`;
  }

  /* ---------- state access by path ---------- */
  function getSet(S, path) {
    const d = S.data; let m;
    if (path === 'ac') return [() => d.ac, v => { d.ac = v; }];
    if ((m = /^h(\d+)$/.exec(path))) return [() => d.cols[+m[1]].h, v => { d.cols[+m[1]].h = v; }];
    if (S.t.kind === 'grid' && (m = /^r(\d+)\.(\d+)$/.exec(path))) return [() => d.rows[+m[1]].c[+m[2]], v => { d.rows[+m[1]].c[+m[2]] = v; }];
    if (S.t.kind === 'tacc' && (m = /^r(\d+)\.([lr])\.(\d+)$/.exec(path))) return [() => d.rows[+m[1]][m[2]].c[+m[3]], v => { d.rows[+m[1]][m[2]].c[+m[3]] = v; }];
    if (S.t.kind === 'journal') {
      if ((m = /^e(\d+)\.date$/.exec(path))) return [() => d.entries[+m[1]].date, v => { d.entries[+m[1]].date = v; }];
      if ((m = /^e(\d+)\.narr$/.exec(path))) return [() => d.entries[+m[1]].narr, v => { d.entries[+m[1]].narr = v; }];
      if ((m = /^e(\d+)\.(\d+)\.(\w+)$/.exec(path))) return [() => d.entries[+m[1]].lines[+m[2]][m[3]], v => { d.entries[+m[1]].lines[+m[2]][m[3]] = v; }];
    }
    if (S.t.kind === 'brs') {
      if (path === 'amt' || path === 'given') return [() => d[path], v => { d[path] = v; }];
      if ((m = /^(add|less)(\d+)\.(p|v)$/.exec(path))) return [() => d[m[1]][+m[2]][m[3]], v => { d[m[1]][+m[2]][m[3]] = v; }];
    }
    return [() => '', () => {}];
  }

  /* ---------- totals and checks ---------- */
  function compute(S) {
    const t = S.t, d = S.data, calc = {}, bad = {}; let check = null;
    if (t.kind === 'journal') {
      let DR = 0, CR = 0, unb = [];
      d.entries.forEach((en, ei) => {
        let dr = 0, cr = 0; en.lines.forEach(l => { if (l.s === 'dr') dr += num(l.amt); else cr += num(l.amt); });
        DR += dr; CR += cr;
        calc['e' + ei] = dr || cr ? (off(dr, cr) ? `✗ Dr. ₹${inr(dr)} ≠ Cr. ₹${inr(cr)}` : `✓ Dr. = Cr. ₹${inr(dr)}`) : '';
        bad['e' + ei] = (dr || cr) && off(dr, cr); if (bad['e' + ei]) unb.push(ei + 1);
      });
      calc.dr = inr0(DR); calc.cr = inr0(CR);
      if (DR || CR) check = unb.length ? { ok: false, msg: `Entr${unb.length > 1 ? 'ies' : 'y'} ${unb.join(', ')} ${unb.length > 1 ? 'do' : 'does'} not balance — every entry needs Dr. = Cr.` } : { ok: true, msg: `Every entry balances · total Dr. = Cr. = ₹${inr(DR)}` };
    } else if (t.kind === 'grid') {
      const cols = d.cols, T = cols.map(() => 0), msgs = [];
      d.rows.forEach((r, ri) => {
        if (r.k && r.k !== 'in') return;
        const nums = r.c.map((v, ci) => (cols[ci].t === 'amt' || cols[ci].t === 'qty') && has(v) ? parseAmt(v) : null);
        nums.forEach((v, ci) => { if (v != null) T[ci] += v; });
        const m = t.rowCheck ? t.rowCheck(nums, r.c) : ''; if (m) { bad['r' + ri] = m; msgs.push(`Row ${ri + 1}: ${m}`); }
      });
      cols.forEach((c, ci) => { if (c.t === 'amt' && c.tot !== false) calc['T' + ci] = inr0(T[ci]); });
      if (t.fixed === 's3') {
        const sec = { I: cols.map(() => 0), II: cols.map(() => 0) };
        d.rows.forEach(r => { if (r.k === 'in') r.c.forEach((v, ci) => { if (cols[ci].t === 'amt') sec[r.sec][ci] += num(v); }); });
        cols.forEach((c, ci) => { if (ci) { calc[`tI-${ci}`] = c.t === 'amt' ? inr0(sec.I[ci]) : ''; calc[`tII-${ci}`] = c.t === 'amt' ? inr0(sec.II[ci]) : ''; } });
        const diffs = [2, 3].filter(ci => (sec.I[ci] || sec.II[ci]) && off(sec.I[ci], sec.II[ci]));
        if (sec.I[2] || sec.II[2] || sec.I[3] || sec.II[3]) check = diffs.length ? { ok: false, msg: `Equity and liabilities ₹${inr(sec.I[diffs[0]])} ≠ assets ₹${inr(sec.II[diffs[0]])} (${diffs[0] === 2 ? 'current' : 'previous'} period).` } : { ok: true, msg: `Total equity and liabilities = total assets = ₹${inr(sec.I[2] || sec.I[3])}` };
      }
      const own = t.check ? t.check(S, T) : null;
      if (msgs.length) check = { ok: false, msg: msgs.slice(0, 3).join(' · ') + (msgs.length > 3 ? ` · +${msgs.length - 3} more` : '') };
      else if (own) check = own;
      else if (!check && T.some(Boolean)) check = { ok: true, msg: 'Totals updated.' };
    } else if (t.kind === 'tacc') {
      const cols = d.cols, L = cols.map(() => 0), R = cols.map(() => 0);
      d.rows.forEach(row => cols.forEach((c, ci) => { if (c.t === 'amt') { L[ci] += num(row.l.c[ci]); R[ci] += num(row.r.c[ci]); } }));
      cols.forEach((c, ci) => { if (c.t === 'amt') { calc['l' + ci] = c.tot === false ? '' : inr0(L[ci]); calc['r' + ci] = c.tot === false ? '' : inr0(R[ci]); } if (c.edit) calc['hh' + ci] = c.h; });
      const balCols = cols.map((c, ci) => (c.t === 'amt' && c.bal !== false && c.tot !== false ? ci : -1)).filter(i => i >= 0);
      const sides = t.sides || ['Dr.', 'Cr.'];
      const any = balCols.some(ci => L[ci] || R[ci]);
      const diff = balCols.filter(ci => off(L[ci], R[ci]));
      const nm = ci => (balCols.length > 1 ? `${cols[ci].h.replace(/\s*\(₹\)/, '')}: ` : '');
      if (any) check = diff.length ? { ok: false, msg: `${sides[0]} and ${sides[1]} totals differ — ${diff.map(ci => `${nm(ci)}₹${inr(L[ci])} vs ₹${inr(R[ci])}`).join(' · ')}.${t.bal ? ' Tap “Balance it” or check your entries.' : ''}` }
        : { ok: true, msg: `${sides[0]} total = ${sides[1]} total ${balCols.map(ci => `${nm(ci)}₹${inr(L[ci])}`).join(' · ')} ✓${cols.some(c => c.bal === false && c.tot !== false) ? ' (discount columns are only totalled)' : ''}` };
      /* balance brought down */
      if (t.bal && t.bal.bd) {
        const bd = []; d.rows.forEach(row => ['l', 'r'].forEach(side => { const p = String(row[side].c[cols.findIndex(c => c.t === 'acct')] || ''); if (/c\/d/i.test(p)) cols.forEach((c, ci) => { if (c.t === 'amt' && has(row[side].c[ci]) && num(row[side].c[ci])) bd.push(`${side === 'r' ? 'To' : 'By'} Balance b/d${balCols.length > 1 ? ` (${c.h.replace(/\s*\(₹\)/, '')})` : ''} ₹${inr(num(row[side].c[ci]))} — ${side === 'r' ? 'debit' : 'credit'} balance`); }); }));
        calc.bd = bd.length ? 'Next period: ' + bd.join(' · ') : '';
      } else calc.bd = '';
      calc.achead = d.title || (t.variant ? t.variant[+d.variant || 0] : t.ac || t.name);
    } else if (t.kind === 'brs') {
      const a = d.add.reduce((s, x) => s + num(x.v), 0), l = d.less.reduce((s, x) => s + num(x.v), 0), st = num(d.amt), res = st + a - l, Ls = brsLabels(d);
      calc.addT = inr0(a); calc.lessT = inr0(l); calc.res = inr(Math.abs(res)); calc.resL = Ls.res(res);
      if (has(d.amt)) {
        if (has(d.given)) check = off(Math.abs(res), num(d.given)) ? { ok: false, msg: `Your statement gives ₹${inr(Math.abs(res))}; the question says ₹${inr(num(d.given))} — difference ₹${inr(Math.abs(Math.abs(res) - num(d.given)))}. Check each Add / Less item.` } : { ok: true, msg: `Reconciled ✓ ${Ls.res(res)} ₹${inr(Math.abs(res))} agrees with the question.` };
        else check = { ok: true, msg: `${Ls.res(res)}: ₹${inr(Math.abs(res))}. Enter the balance given in the question below to check that it reconciles.` };
      }
    }
    return { calc, bad, check };
  }

  /* ---------- flatten for the saved attempt / AI checker ---------- */
  function flat(S) {
    const t = S.t, d = S.data;
    if (t.kind === 'journal') {
      const rows = []; d.entries.forEach(en => { en.lines.forEach((l, i) => { if (!l.ac && !l.amt) return; rows.push([i === 0 ? en.date : '', l.s === 'dr' ? `${l.ac} Dr.` : `    To ${l.ac}`, l.lf, l.s === 'dr' ? l.amt : '', l.s === 'cr' ? l.amt : '']); }); if (en.narr) rows.push(['', en.narr, '', '', '']); });
      return { kind: 'journal', cols: ['Date', 'Particulars', 'L.F.', 'Dr. Amount (₹)', 'Cr. Amount (₹)'], rows };
    }
    if (t.kind === 'grid') return { kind: 'grid', cols: d.cols.map(c => c.h), rows: d.rows.filter(r => r.k === 'h' || r.c.some(x => String(x || '').trim())).map(r => (r.k === 'h' ? [r.label].concat(Array(d.cols.length - 1).fill('')) : r.c.map((v, ci) => (d.cols[ci].t === 'label' ? r.label : v)))) };
    if (t.kind === 'tacc') {
      const pi = d.cols.findIndex(c => c.t === 'acct'), pre = t.pre === null ? ['', ''] : ['To ', 'By '], sides = t.sides || ['Dr.', 'Cr.'];
      const side = (r, k) => r.c.map((v, ci) => (ci === pi && v ? pre[k] + v : v));
      return { kind: 'tacc', cols: d.cols.map(c => `${sides[0]} ${c.h}`).concat(d.cols.map(c => `${sides[1]} ${c.h}`)), rows: d.rows.filter(r => r.l.c.concat(r.r.c).some(x => String(x || '').trim())).map(r => side(r.l, 0).concat(side(r.r, 1))), account: d.ac || '' };
    }
    if (t.kind === 'brs') {
      const L = brsLabels(d), c = compute(S).calc, rows = [[L.start, '', d.amt], ['Add:', '', '']].concat(d.add.filter(x => x.p || x.v).map(x => [x.p, x.v, '']), [['', '', c.addT]], [['Less:', '', '']], d.less.filter(x => x.p || x.v).map(x => [x.p, x.v, '']), [['', '', c.lessT], [c.resL, '', c.res]]);
      return { kind: 'grid', cols: ['Particulars', 'Details (₹)', 'Amount (₹)'], rows };
    }
    return { cols: [], rows: [] };
  }
  const ne = x => String(x == null ? '' : x).trim() !== '';
  function filled(S) {
    const d = S.data, k = S.t.kind;
    if (k === 'journal') return d.entries.some(en => ne(en.date) || ne(en.narr) || en.lines.some(l => ne(l.ac) || ne(l.amt)));
    if (k === 'grid') return d.rows.some(r => (!r.k || r.k === 'in') && r.c.some(ne));
    if (k === 'tacc') return d.rows.some(r => r.l.c.concat(r.r.c).some(ne));
    if (k === 'brs') return ne(d.amt) || d.add.concat(d.less).some(x => ne(x.p) || ne(x.v));
    return false;
  }

  /* ---------- the pad ---------- */
  function mount(host, opts = {}) {
    const sug = suggest(opts.pad, opts.q);
    const pad = { host, sheets: [], sug, onChange: opts.onChange || (() => {}) };
    const mk = id => { const t = byId(id) || byId('blank'); const S = { uid: ++UID, t, data: init(t), store: {}, meta: {}, pad }; return S; };
    pad.sheets.push(mk(sug[0] || opts.fallback || 'blank'));
    const errMsg = { date: 'Write the date as dd-mmm-yy, for example 05-Apr-26.', amt: 'Amounts: digits only, for example 1,25,000 or 450.50.', qty: 'Quantity: digits only.' };

    let drawing = false;   // the focused cell is removed while redrawing: its focusout must not write into the new data
    function draw(focusPath, sheetIdx) {
      drawing = true;
      const more = sug.filter(id => !pad.sheets.some(S => S.t.id === id));
      host.innerHTML = `${sug.length ? `<p class="ca-pd-sug"><b>Suggested format${sug.length > 1 ? 's' : ''}:</b> ${sug.map(id => `<span class="ca-pd-sugc">${e_(byId(id).name)}</span>`).join(' ')}</p>` : '<p class="ca-pd-sug">Choose the exam format that fits your answer.</p>'}
        ${pad.sheets.map((S, si) => `<section class="ca-pd-sheet" data-s="${si}" aria-label="Table ${si + 1}: ${e_(S.t.name)}">${headHTML(S)}${(S.meta = {}, '')}${S.t.kind === 'journal' ? journalHTML(S) : S.t.kind === 'grid' ? gridHTML(S) : S.t.kind === 'tacc' ? taccHTML(S) : brsHTML(S)}
          <p class="ca-pd-chk0" data-check role="status" aria-live="polite"></p><p class="ca-pd-err" data-err role="alert"></p></section>`).join('')}
        <div class="ca-btns ca-pd-more">${more.map(id => `<button type="button" class="btn ghost" data-act="addsheet" data-tpl="${id}">+ ${e_(byId(id).name)}</button>`).join('')}<button type="button" class="btn ghost" data-act="addsheet">+ Another table</button></div>
        <p class="ca-note ca-pd-keys">Keyboard: Enter moves to the next cell (and adds a row at the end), Shift+Enter goes back. Dates dd-mmm-yy · amounts in Indian format · account names are put in Title Case when you leave the cell.</p>`;
      drawing = false;
      pad.sheets.forEach((S, si) => refresh(si));
      if (focusPath != null) { const el = host.querySelector(`.ca-pd-sheet[data-s="${sheetIdx}"] [data-p="${focusPath}"]`); if (el) { el.focus({ preventScroll: false }); try { el.setSelectionRange(el.value.length, el.value.length); } catch (e) {} } }
    }
    function refresh(si) {
      const S = pad.sheets[si], sec = host.querySelector(`.ca-pd-sheet[data-s="${si}"]`); if (!sec) return;
      const { calc, bad, check } = compute(S);
      sec.querySelectorAll('[data-calc]').forEach(el => { const k = el.dataset.calc; if (k in calc) el.textContent = calc[k]; });
      sec.querySelectorAll('tbody.ca-pd-je').forEach(tb => tb.classList.toggle('ca-pd-bad', !!bad['e' + tb.dataset.e]));
      sec.querySelectorAll('tr[data-r]').forEach(tr => { const m = bad['r' + tr.dataset.r]; tr.classList.toggle('ca-pd-bad', !!m); if (m) tr.title = m; else tr.removeAttribute('title'); });
      const ce = sec.querySelector('[data-check]'); const txt = check ? check.msg : 'Totals and checks appear here as you fill the table.';
      if (ce.textContent !== txt) ce.textContent = txt; ce.className = `ca-pd-chk0 ${check ? (check.ok ? 'ok' : 'no') : ''}`;
    }
    const sheetOf = el => { const s = el.closest('.ca-pd-sheet'); return s ? +s.dataset.s : -1; };
    function normalise(S, el) {
      const p = el.dataset.p; if (!p) return;
      const ty = S.meta[p] || (el.classList.contains('ca-pc-head') ? 'head' : el.classList.contains('ca-pc-acname') ? 'acname' : 'text');
      const [get, set] = getSet(S, p); let v = el.value, msg = '';
      if (ty === 'date') { const r = parseDate(v); if (r.ok) v = r.v; else msg = errMsg.date; }
      else if (ty === 'amt' || ty === 'qty') { const a = parseAmt(v); if (a == null) v = ''; else if (isNaN(a)) msg = errMsg[ty]; else v = ty === 'qty' ? String(r2(a)) : inr(a); }
      else if (ty === 'acct') v = titleCase(stripPre(v));
      else if (ty === 'acctj') v = withAc(titleCase(stripPre(v)));
      else if (ty === 'acname') v = withAc(titleCase(v));
      else if (ty === 'narr') v = narr(v);
      el.value = v; set(v); el.setAttribute('aria-invalid', msg ? 'true' : 'false'); el.classList.toggle('ca-pc-bad', !!msg);
      const er = host.querySelector(`.ca-pd-sheet[data-s="${sheetOf(el)}"] [data-err]`);
      if (er) { if (msg) er.textContent = `${el.getAttribute('aria-label') || 'Cell'}: ${msg}`; else if (!er.closest('.ca-pd-sheet').querySelector('.ca-pc-bad')) er.textContent = ''; }
      if (ty === 'head' && S.t.kind === 'tacc') refresh(sheetOf(el));
    }

    host.addEventListener('input', e => {
      const el = e.target, si = sheetOf(el); if (si < 0) return; const S = pad.sheets[si];
      if (el.dataset.act === 'title') { S.data.title = el.value; refresh(si); pad.onChange(); return; }
      if (!el.dataset.p) return;
      getSet(S, el.dataset.p)[1](el.value); clearTimeout(refresh['t' + si]); refresh['t' + si] = setTimeout(() => refresh(si), 250); pad.onChange();
    });
    host.addEventListener('focusout', e => { const el = e.target; if (drawing || !el.isConnected || !el.classList || !el.classList.contains('ca-pc')) return; const si = sheetOf(el); if (si < 0) return; normalise(pad.sheets[si], el); refresh(si); });
    host.addEventListener('change', e => {
      const el = e.target, si = sheetOf(el); if (si < 0) return; const S = pad.sheets[si];
      if (el.dataset.nat) { const v = isoToD(el.value); const inp = el.parentElement.querySelector('.ca-pc'); if (v && inp) { inp.value = v; getSet(S, inp.dataset.p)[1](v); inp.setAttribute('aria-invalid', 'false'); inp.classList.remove('ca-pc-bad'); refresh(si); pad.onChange(); inp.focus(); } return; }
      const act = el.dataset.act;
      if (act === 'tpl') { S.store[S.t.id] = S.data; S.t = byId(el.value); S.data = S.store[S.t.id] || init(S.t); draw(); const f = host.querySelector(`#cpSel${S.uid}`); if (f) f.focus(); pad.onChange(); }
      else if (act === 'variant') { S.data.variant = +el.value; refresh(si); pad.onChange(); }
      else if (act === 'brsstart') { S.data.start = el.value; draw(); const f = host.querySelector(`#cpBs${S.uid}`); if (f) f.focus(); }
      else if (act === 'brsod') { S.data.od = el.checked; draw(); }
    });
    host.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b || !host.contains(b)) return;
      if (b.dataset.cal) { const nat = b.parentElement.querySelector('.ca-pd-native'), inp = b.parentElement.querySelector('.ca-pc'); const r = parseDate(inp.value); nat.value = r.ok && r.iso ? r.iso : ''; try { if (nat.showPicker) nat.showPicker(); else { nat.focus(); nat.click(); } } catch (x) { nat.focus(); nat.click(); } return; }
      const act = b.dataset.act; if (!act) return;
      const si = sheetOf(b); const S = pad.sheets[si];
      if (act === 'addsheet') { pad.sheets.push(mk(b.dataset.tpl || 'blank')); draw(); const s = host.querySelector(`.ca-pd-sheet[data-s="${pad.sheets.length - 1}"] select`); if (s) { s.focus(); s.scrollIntoView({ block: 'nearest' }); } pad.onChange(); return; }
      if (!S) return;
      const d = S.data, n = d.cols ? d.cols.length : 0; let fp = null;
      if (act === 'rmsheet') { pad.sheets.splice(si, 1); draw(); pad.onChange(); return; }
      if (act === 'dupsheet') { const N = mk(S.t.id); pad.sheets.splice(si + 1, 0, N); draw(); const a = host.querySelector(`.ca-pd-sheet[data-s="${si + 1}"] .ca-pc-acname`); if (a) a.focus(); return; }
      if (S.t.kind === 'journal') {
        const ei = +b.dataset.e;
        if (act === 'addentry') { d.entries.push(newEntry()); fp = `e${d.entries.length - 1}.date`; }
        else if (act === 'rmentry') { d.entries.splice(ei, 1); if (!d.entries.length) d.entries.push(newEntry()); }
        else if (act === 'adddr') { const ls = d.entries[ei].lines; let at = ls.map(l => l.s).lastIndexOf('dr') + 1; ls.splice(at, 0, { s: 'dr', ac: '', lf: '', amt: '' }); fp = `e${ei}.${at}.ac`; }
        else if (act === 'addcr') { const ls = d.entries[ei].lines; ls.push({ s: 'cr', ac: '', lf: '', amt: '' }); fp = `e${ei}.${ls.length - 1}.ac`; }
        else if (act === 'rmline') { const ls = d.entries[ei].lines; ls.splice(+b.dataset.l, 1); if (!ls.length) ls.push({ s: 'dr', ac: '', lf: '', amt: '' }); }
      } else if (S.t.kind === 'brs') {
        if (act === 'addbrs') { d[b.dataset.k].push({ p: '', v: '' }); fp = `${b.dataset.k}${d[b.dataset.k].length - 1}.p`; }
        else if (act === 'rmbrs') { d[b.dataset.k].splice(+b.dataset.i, 1); if (!d[b.dataset.k].length) d[b.dataset.k].push({ p: '', v: '' }); }
      } else {
        const firstIn = ri => { const ci = d.cols.findIndex(c => c.t !== 'label'); return S.t.kind === 'tacc' ? `r${ri}.l.${ci}` : `r${ri}.${ci}`; };
        if (act === 'addrow') { d.rows.push(S.t.kind === 'tacc' ? { l: blankRow(n), r: blankRow(n) } : blankRow(n)); fp = firstIn(d.rows.length - 1); }
        else if (act === 'rmrow') { d.rows.splice(+b.dataset.r, 1); if (!d.rows.length) d.rows.push(S.t.kind === 'tacc' ? { l: blankRow(n), r: blankRow(n) } : blankRow(n)); }
        else if (act === 'addcol' || act === 'addpartner') {
          const c = act === 'addpartner' ? AM(String.fromCharCode(65 + d.cols.filter(x => x.partner).length), { edit: 1, partner: 1 }) : C_(S.t.addCol === 'amt' ? 'New column (₹)' : 'New column', S.t.addCol, { edit: 1 });
          d.cols.push(c); d.rows.forEach(r => { if (S.t.kind === 'tacc') { r.l.c.push(''); r.r.c.push(''); } else if (r.c) r.c.push(''); }); fp = `h${d.cols.length - 1}`;
        } else if (act === 'rmcol') { const ci = +b.dataset.c; d.cols.splice(ci, 1); d.rows.forEach(r => { if (S.t.kind === 'tacc') { r.l.c.splice(ci, 1); r.r.c.splice(ci, 1); } else if (r.c) r.c.splice(ci, 1); }); }
        else if (act === 'balance') { if (balance(S) && typeof toast === 'function') toast('Balancing figure added'); }
      }
      draw(fp, si); pad.onChange();
    });
    host.addEventListener('keydown', e => {
      const el = e.target; if (e.key !== 'Enter' || !el.classList || !el.classList.contains('ca-pc')) return;
      e.preventDefault(); normalise(pad.sheets[sheetOf(el)], el);
      const sec = el.closest('.ca-pd-sheet'), all = [...sec.querySelectorAll('input.ca-pc')], i = all.indexOf(el);
      const nx = all[i + (e.shiftKey ? -1 : 1)];
      if (nx) { nx.focus(); try { nx.select(); } catch (x) {} return; }
      if (!e.shiftKey) { const add = sec.querySelector('[data-act="addrow"], [data-act="addentry"]'); if (add) add.click(); }
    });
    function balance(S) {
      const d = S.data, cols = d.cols, pi = cols.findIndex(c => c.t === 'acct');
      d.rows = d.rows.filter(r => !r.auto);
      const L = cols.map(() => 0), R = cols.map(() => 0);
      d.rows.forEach(row => cols.forEach((c, ci) => { if (c.t === 'amt') { L[ci] += num(row.l.c[ci]); R[ci] += num(row.r.c[ci]); } }));
      const row = { l: blankRow(cols.length), r: blankRow(cols.length), auto: true }; let any = false;
      cols.forEach((c, ci) => { if (c.t !== 'amt' || c.bal === false || c.tot === false) return; const df = r2(L[ci] - R[ci]); if (!df) return; any = true; const side = df > 0 ? 'r' : 'l'; row[side].c[ci] = inr(Math.abs(df)); row[side].c[pi] = side === 'l' ? S.t.bal.l : S.t.bal.r; });
      if (!any) { if (typeof toast === 'function') toast('Both sides already agree'); return false; }
      const empty = d.rows.findIndex(r => !r.l.c.concat(r.r.c).some(x => String(x || '').trim()));
      if (empty >= 0) d.rows.splice(empty, 0, row); else d.rows.push(row);
      d.rows = d.rows.filter((r, i) => r.auto || r.l.c.concat(r.r.c).some(x => String(x || '').trim()) || i < 2);
      return true;
    }
    draw();
    return {
      sheets: pad.sheets,
      isEmpty: () => !pad.sheets.some(filled),
      value: () => ({ schema: 'ca-pad/1', sheets: pad.sheets.filter(filled).map(S => ({ tpl: S.t.id, name: S.t.name, title: S.data.title || '', data: JSON.parse(JSON.stringify(S.data)), flat: flat(S), check: compute(S).check })) })
    };
  }

  /* static view of a saved payload (attempt history) — also renders the old { cols, rows } shape */
  function view(p) {
    if (!p) return '';
    const sheets = p.sheets || (p.cols ? [{ name: 'Table', flat: { cols: p.cols, rows: p.rows } }] : []);
    return sheets.map(s => `<div class="ca-pd-view"><b>${e_(s.title || s.name)}</b>${s.flat.account ? ` <span class="ca-note">${e_(s.flat.account)}</span>` : ''}<div class="ca-scroll" role="region" tabindex="0" aria-label="${e_(s.name)}"><table class="ca-t"><thead><tr>${s.flat.cols.map(c => `<th scope="col">${e_(c)}</th>`).join('')}</tr></thead><tbody>${s.flat.rows.map(r => `<tr>${r.map(x => `<td${/^[\d,().]+$/.test(String(x || '')) ? ' class="n"' : ''}>${e_(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>${s.check ? `<p class="ca-pd-chk0 ${s.check.ok ? 'ok' : 'no'}">${e_(s.check.msg)}</p>` : ''}</div>`).join('');
  }

  window.CaPad = { mount, view, suggest, titleCase, parseDate, parseAmt, inr, narr, TPL, byId, _compute: compute, _init: init };
})();
