/* Knowtopia Concept Lab: taccount — an accounting workbench (CBSE Class 11 Accountancy, NCERT format).
 *
 * MODES
 *   journal       Read a transaction, tap an account chip, then tap the Debit or Credit box to place it,
 *                 type the amount, Check. Feedback explains the rule (modern / accounting-equation rules or
 *                 the golden rules: personal / real / nominal). Compound entries are supported.
 *   ledger        Post each journal entry into T-accounts: choose the account tab, tap its Dr or Cr side
 *                 ("To … A/c" / "By … A/c" are written for you). Then close every account: type the balance,
 *                 choose the side and how it is closed (Balance c/d → b/d, or transfer to Trading A/c,
 *                 Profit and Loss A/c, Capital A/c for Drawings).
 *   trialbalance  Tap the Dr or Cr column for every ledger balance; totals update live and must agree.
 *   bankrec       Prepare a Bank Reconciliation Statement: start from the cash book (or pass book) balance,
 *                 mark every difference Add or Less until your BRS gives the other book's balance.
 *
 * PARAMS (all optional — every one has a built-in default)
 *   mode          string   'journal' | 'ledger' | 'trialbalance' | 'bankrec'                   'journal'
 *   title         string   Heading shown above the work area                                    (by mode)
 *   challenge     string   Challenge sentence                                                   (by mode)
 *   firm          string   Name of the business                                                 'Ravi Traders'
 *   rules         string   'modern' | 'golden' explanation style shown first (toggle in UI)     'modern'
 *   transactions  array    [{date, text, dr, cr, amt, narration}]  dr/cr = account name, or for a
 *                          compound entry an array of {a, amt}. Used by journal & ledger, and by
 *                          trialbalance when `balances` is not given (balances are worked out).   6 April entries
 *   accounts      array    Extra account names offered as (distractor) chips in journal mode     []
 *   types         object   {accountName: 'asset'|'liability'|'capital'|'drawings'|'expense'|'revenue'}
 *                          to classify accounts the built-in dictionary does not know.          {}
 *   closeDate     string   Date written on Balance c/d rows (ledger)                             'Mar 31'
 *   openDate      string   Date written on Balance b/d rows (ledger)                             'Apr 1'
 *   balances      array    trialbalance: [{a, amt, side?}] (side 'dr'|'cr' — else from the account
 *                          type), or an object {name: amount}                                     12 balances
 *   tbDate        string   Date in the trial balance heading                                     '31st March, 2026'
 *   start         string   bankrec: 'cashbook' | 'passbook' — which balance the BRS starts from    'cashbook'
 *   balance       number   bankrec: starting balance (₹)                                         45000
 *   overdraft     boolean  bankrec: the starting balance is an overdraft                         false
 *   items         array    bankrec: [{type, amt, text?}] or [{text, amt, pb: +1|-1}]. pb = +1 if the
 *                          item makes the PASS BOOK (favourable) balance higher than the cash book.
 *                          types: issued_not_presented, deposited_not_credited, bank_charges,
 *                          interest_credited, direct_deposit, direct_payment, dishonoured,
 *                          collected_by_bank, interest_debited                                    6 items
 *   brsDate       string   bankrec: date of the statement                                        '31st March, 2026'
 *
 * Amounts are shown in the Indian system (₹1,00,000).
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
  const same = (a, b) => Math.abs(a - b) < 0.005;
  const norm = a => String(a == null ? '' : a).trim().replace(/\s*(a\/c|account)\.?$/i, '').trim();
  const key = a => norm(a).toLowerCase();
  const TR = 'trading', PL = 'pl', CAP = 'capital';
  /* [type, golden class, where a nominal account is closed] */
  const DICT = {
    cash: ['asset', 'real'], bank: ['asset', 'personal'], capital: ['capital', 'personal'], drawings: ['drawings', 'personal', CAP],
    purchases: ['expense', 'real', TR], purchase: ['expense', 'real', TR], sales: ['revenue', 'real', TR], sale: ['revenue', 'real', TR],
    'purchases return': ['revenue', 'real', TR], 'purchase return': ['revenue', 'real', TR], 'purchases returns': ['revenue', 'real', TR], 'returns outward': ['revenue', 'real', TR],
    'sales return': ['expense', 'real', TR], 'sales returns': ['expense', 'real', TR], 'returns inward': ['expense', 'real', TR],
    'opening stock': ['expense', 'real', TR], wages: ['expense', 'nominal', TR], 'carriage inwards': ['expense', 'nominal', TR], 'freight inwards': ['expense', 'nominal', TR],
    furniture: ['asset', 'real'], machinery: ['asset', 'real'], 'plant and machinery': ['asset', 'real'], building: ['asset', 'real'], buildings: ['asset', 'real'], land: ['asset', 'real'],
    computer: ['asset', 'real'], computers: ['asset', 'real'], 'motor vehicle': ['asset', 'real'], vehicle: ['asset', 'real'], 'office equipment': ['asset', 'real'], equipment: ['asset', 'real'],
    stock: ['asset', 'real'], 'closing stock': ['asset', 'real'], inventory: ['asset', 'real'], investments: ['asset', 'real'], 'bills receivable': ['asset', 'real'], goodwill: ['asset', 'real'],
    rent: ['expense', 'nominal', PL], salaries: ['expense', 'nominal', PL], salary: ['expense', 'nominal', PL], electricity: ['expense', 'nominal', PL], advertisement: ['expense', 'nominal', PL],
    insurance: ['expense', 'nominal', PL], 'interest paid': ['expense', 'nominal', PL], 'discount allowed': ['expense', 'nominal', PL], 'bad debts': ['expense', 'nominal', PL],
    depreciation: ['expense', 'nominal', PL], 'commission paid': ['expense', 'nominal', PL], stationery: ['expense', 'nominal', PL], repairs: ['expense', 'nominal', PL],
    'telephone charges': ['expense', 'nominal', PL], 'carriage outwards': ['expense', 'nominal', PL], 'general expenses': ['expense', 'nominal', PL], 'loss by fire': ['expense', 'nominal', PL], charity: ['expense', 'nominal', PL],
    'bank charges': ['expense', 'nominal', PL], 'commission received': ['revenue', 'nominal', PL], commission: ['revenue', 'nominal', PL], 'interest received': ['revenue', 'nominal', PL],
    'rent received': ['revenue', 'nominal', PL], 'discount received': ['revenue', 'nominal', PL], 'dividend received': ['revenue', 'nominal', PL], 'bad debts recovered': ['revenue', 'nominal', PL],
    loan: ['liability', 'personal'], 'bank loan': ['liability', 'personal'], 'bank overdraft': ['liability', 'personal'], creditors: ['liability', 'personal'], 'sundry creditors': ['liability', 'personal'],
    'trade payables': ['liability', 'personal'], 'bills payable': ['liability', 'personal'], debtors: ['asset', 'personal'], 'sundry debtors': ['asset', 'personal'], 'trade receivables': ['asset', 'personal'],
    'gst payable': ['liability', 'personal'], 'outstanding salaries': ['liability', 'personal'], 'outstanding rent': ['liability', 'personal'], 'outstanding wages': ['liability', 'personal'],
    'prepaid insurance': ['asset', 'personal'], 'prepaid rent': ['asset', 'personal'], 'accrued interest': ['asset', 'personal']
  };
  const GOLD = { asset: 'real', liability: 'personal', capital: 'personal', drawings: 'personal', expense: 'nominal', revenue: 'nominal' };
  const DRSIDE = { asset: 1, expense: 1, drawings: 1 };
  function infoOf(name, types, hint) {
    const n = norm(name), k = n.toLowerCase();
    let d = DICT[k];
    if (!d) {
      const has = w => k.includes(w);
      if (has('loan') || has('overdraft') || has('outstanding') || has('payable') || has('creditor')) d = ['liability', 'personal'];
      else if (has('prepaid') || has('accrued') || has('receivable') || has('debtor')) d = ['asset', 'personal'];
      else if (has('received') || has('income') || has('earned') || has('recovered')) d = ['revenue', 'nominal', PL];
      else if (has('expense') || has('paid') || has('loss') || has('charges')) d = ['expense', 'nominal', PL];
      else if (/machin|furnitur|building|equipment|vehicle|computer|land|stock|investment|plant/.test(k)) d = ['asset', 'real'];
      else d = hint === 'cr' ? ['liability', 'personal'] : ['asset', 'personal']; /* a person or firm: creditor or debtor */
    }
    const ov = types && (types[n] || types[name]);
    if (ov) {
      const t = typeof ov === 'string' ? ov : ov.type;
      if (GOLD[t]) d = [t, (ov && ov.golden) || (t === d[0] ? d[1] : GOLD[t]), t === 'drawings' ? CAP : (t === 'expense' || t === 'revenue') ? (d[2] || PL) : undefined];
    }
    return { type: d[0], gold: d[1], close: d[2] || null };
  }
  const MOD = {
    asset: ['Asset increases → Debit', 'Asset decreases → Credit'], liability: ['Liability decreases → Debit', 'Liability increases → Credit'],
    capital: ['Capital decreases → Debit', 'Capital increases → Credit'], drawings: ['Drawings increase → Debit', 'Drawings decrease → Credit'],
    expense: ['Expense / loss increases → Debit', 'Expense decreases → Credit'], revenue: ['Income decreases → Debit', 'Income / gain increases → Credit']
  };
  const GLD = {
    personal: ['Personal a/c: debit the receiver', 'Personal a/c: credit the giver'], real: ['Real a/c: debit what comes in', 'Real a/c: credit what goes out'],
    nominal: ['Nominal a/c: debit all expenses and losses', 'Nominal a/c: credit all incomes and gains']
  };
  const why = (inf, side, rules) => rules === 'golden' ? GLD[inf.gold][side === 'dr' ? 0 : 1] : MOD[inf.type][side === 'dr' ? 0 : 1];
  function linesOf(x, side, amt) {
    if (x == null) return [];
    return (Array.isArray(x) ? x : [x]).map(it => typeof it === 'string' ? { a: norm(it), side, amt: +amt } : it && typeof it === 'object' ? { a: norm(it.a || it.account || it.name), side, amt: +(it.amt != null ? it.amt : amt) } : null)
      .filter(l => l && l.a && l.amt > 0);
  }
  function normTxns(list) {
    return (Array.isArray(list) ? list : []).map(t => t && typeof t === 'object' ? ({ date: t.date || '', text: t.text || '', narration: t.narration || '', lines: [...linesOf(t.dr, 'dr', t.amt), ...linesOf(t.cr, 'cr', t.amt)] }) : null)
      .filter(t => t && t.lines.some(l => l.side === 'dr') && t.lines.some(l => l.side === 'cr'));
  }
  const DEF_TXNS = [
    { date: 'Apr 1', text: 'Ravi started business with cash ₹1,00,000', dr: 'Cash', cr: 'Capital', amt: 100000, narration: '(Being business started with cash)' },
    { date: 'Apr 3', text: 'Deposited ₹40,000 cash into the bank', dr: 'Bank', cr: 'Cash', amt: 40000, narration: '(Being cash deposited into bank)' },
    { date: 'Apr 5', text: 'Bought goods from Mohan on credit ₹30,000', dr: 'Purchases', cr: 'Mohan', amt: 30000, narration: '(Being goods purchased on credit)' },
    { date: 'Apr 10', text: 'Sold goods for ₹25,000 — ₹15,000 in cash, the rest on credit to Sita', dr: [{ a: 'Cash', amt: 15000 }, { a: 'Sita', amt: 10000 }], cr: 'Sales', amt: 25000, narration: '(Being goods sold partly for cash and partly on credit)' },
    { date: 'Apr 20', text: 'Paid ₹20,000 to Mohan by cheque', dr: 'Mohan', cr: 'Bank', amt: 20000, narration: '(Being amount paid to Mohan by cheque)' },
    { date: 'Apr 30', text: 'Paid rent ₹5,000 in cash', dr: 'Rent', cr: 'Cash', amt: 5000, narration: '(Being rent paid)' }
  ];
  const DEF_LEDGER = [DEF_TXNS[0], DEF_TXNS[1], DEF_TXNS[2], DEF_TXNS[4], DEF_TXNS[5]];
  const DEF_TB = [
    { a: 'Capital', amt: 200000 }, { a: 'Drawings', amt: 20000 }, { a: 'Cash', amt: 30000 }, { a: 'Bank', amt: 50000 }, { a: 'Machinery', amt: 80000 }, { a: 'Furniture', amt: 30000 },
    { a: 'Purchases', amt: 120000 }, { a: 'Sales', amt: 180000 }, { a: 'Debtors', amt: 40000 }, { a: 'Creditors', amt: 30000 }, { a: 'Salaries', amt: 25000 }, { a: 'Rent', amt: 15000 }
  ];
  const BRS = {
    issued_not_presented: [1, 'Cheques issued but not yet presented for payment', 'The cash book already reduced the balance, but the bank has not paid them yet.'],
    deposited_not_credited: [-1, 'Cheques deposited but not yet credited by the bank', 'The cash book already added them, but the bank has not collected them yet.'],
    bank_charges: [-1, 'Bank charges debited in the pass book only', 'The bank reduced the balance; the cash book does not show it yet.'],
    interest_debited: [-1, 'Interest on overdraft debited by the bank only', 'The bank reduced the balance; the cash book does not show it yet.'],
    interest_credited: [1, 'Interest credited by the bank, not in the cash book', 'The bank added it; the cash book does not show it yet.'],
    direct_deposit: [1, 'A customer paid directly into our bank account', 'Only the pass book shows this receipt.'],
    collected_by_bank: [1, 'Dividend collected by the bank directly', 'Only the pass book shows this receipt.'],
    direct_payment: [-1, 'Insurance premium paid by the bank on standing instructions', 'Only the pass book shows this payment.'],
    dishonoured: [-1, 'A cheque deposited earlier was dishonoured', 'The bank cancelled the credit; the cash book still counts it.']
  };
  const DEF_ITEMS = [
    { type: 'issued_not_presented', amt: 12000 }, { type: 'deposited_not_credited', amt: 8000 }, { type: 'bank_charges', amt: 500 },
    { type: 'interest_credited', amt: 1200 }, { type: 'direct_deposit', amt: 5000 }, { type: 'direct_payment', amt: 2000 }
  ];
  /* tiny seeded shuffle so chip order is stable but not revealing */
  function shuffle(arr, seed) { const a = arr.slice(); let s = seed * 9301 + 49297; for (let i = a.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor(s / 233280 * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  const CSS = `
.lb-taccount-w{font-size:13px;color:#1b1f3a;user-select:none;-webkit-user-select:none;line-height:1.3}
.lb-taccount-w button{font-family:inherit;cursor:pointer;border:none}
.lb-taccount-ch{font-weight:800;font-size:13.5px;line-height:1.3;margin-bottom:6px}
.lb-taccount-bar{display:flex;align-items:center;gap:6px;margin-bottom:6px;font-size:12px}
.lb-taccount-bar b{flex:1;font-size:13px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-taccount-pg{background:#f1ecff;color:#7044e0;border-radius:99px;padding:3px 9px;font-weight:800;white-space:nowrap}
.lb-taccount-seg{display:inline-flex;background:#eef0fb;border-radius:99px;padding:2px}
.lb-taccount-seg button{background:none;border-radius:99px;padding:5px 9px;font-weight:800;font-size:11.5px;color:#6b7090;min-height:28px}
.lb-taccount-seg button.on{background:#fff;color:#7044e0;box-shadow:0 1px 3px #0002}
.lb-taccount-txn{background:#fff8e1;border-radius:12px;padding:7px 10px;font-weight:700;font-size:13.5px;margin-bottom:6px}
.lb-taccount-txn i{font-style:normal;color:#b57f00;font-weight:800;margin-right:6px}
.lb-taccount-zone{border:2px dashed #c9d6f5;border-radius:12px;padding:4px 6px;margin-bottom:5px;min-height:44px;background:#f5f8ff;transition:background .15s,border-color .15s}
.lb-taccount-zone.cr{border-color:#f7c6c6;background:#fff6f6}
.lb-taccount-zone.arm{border-style:solid;border-color:#8b5cf6;background:#f3efff}
.lb-taccount-zh{font-size:10.5px;font-weight:800;color:#6b7090;text-transform:uppercase;letter-spacing:.04em}
.lb-taccount-ln{display:flex;align-items:center;gap:5px;margin:3px 0;border-radius:9px;padding:2px 3px}
.lb-taccount-ln .an{flex:1;font-weight:800;font-size:13px;min-width:0}
.lb-taccount-ln .an small{color:#6b7090;font-weight:700}
.lb-taccount-ln input{width:96px;height:34px;border:2px solid #dfe3f5;border-radius:9px;padding:0 6px;font:inherit;font-weight:800;text-align:right;font-size:13px;user-select:text;-webkit-user-select:text}
.lb-taccount-ln .x{width:32px;height:34px;border-radius:9px;background:#eef0fb;color:#6b7090;font-weight:900;font-size:15px}
.lb-taccount-ln.ok{background:#e3fbf3}.lb-taccount-ln.bad{background:#ffe9e9}
.lb-taccount-tot{display:flex;justify-content:space-between;font-weight:800;font-size:12px;color:#6b7090;margin:2px 2px 5px}
.lb-taccount-tot .agr{color:#0f9a72}.lb-taccount-tot .dif{color:#e04848}
.lb-taccount-chips{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:6px}
.lb-taccount-chip{background:#fff;border:2px solid #e3e6f6 !important;border-radius:99px;padding:6px 11px;font-weight:800;font-size:12.5px;min-height:38px;color:#1b1f3a;transition:transform .12s}
.lb-taccount-chip.sel{background:#8b5cf6;color:#fff;border-color:#8b5cf6 !important;transform:translateY(-2px);box-shadow:0 3px 8px #8b5cf655}
.lb-taccount-btns{display:flex;gap:6px}
.lb-taccount-btn{flex:1;min-height:40px;border-radius:12px;background:#8b5cf6;color:#fff;font-weight:800;font-size:14px}
.lb-taccount-btn.alt{background:#eef0fb;color:#1b1f3a}.lb-taccount-btn.go{background:#2ed3a5;color:#063b2c}
.lb-taccount-btn[disabled]{opacity:.45}
.lb-taccount-msg{margin-top:6px;font-weight:700;font-size:12.5px;line-height:1.35;min-height:18px}
.lb-taccount-msg.ok{color:#0f7a5c}.lb-taccount-msg.bad{color:#d03c3c}
.lb-taccount-msg em{font-style:normal;color:#6b7090;display:block;font-weight:700}
.lb-taccount-tabs{display:flex;gap:5px;overflow-x:auto;padding-bottom:3px;margin-bottom:5px;scrollbar-width:none}
.lb-taccount-tabs::-webkit-scrollbar{display:none}
.lb-taccount-tabs button{flex:none;background:#eef0fb;border-radius:10px;padding:6px 10px;font-weight:800;font-size:12px;min-height:36px;color:#1b1f3a}
.lb-taccount-tabs button.on{background:#1b1f3a;color:#fff}
.lb-taccount-tabs button.dn{box-shadow:inset 0 0 0 2px #2ed3a5}
.lb-taccount-je{background:#f7f8ff;border-radius:12px;padding:5px 9px;margin-bottom:6px;font-size:12.5px}
.lb-taccount-je .r{display:flex;gap:6px;align-items:center;font-weight:700;min-height:20px}
.lb-taccount-je .r span{flex:1}.lb-taccount-je .r b{min-width:62px;text-align:right}
.lb-taccount-je .r.dn{color:#0f9a72}.lb-taccount-je .r.dn span:after{content:' ✓'}
.lb-taccount-je .d{font-size:10.5px;color:#6b7090;font-weight:800}
.lb-taccount-t{border:2px solid #1b1f3a;border-radius:10px;overflow:hidden;background:#fff}
.lb-taccount-th{display:flex;justify-content:space-between;align-items:center;background:#1b1f3a;color:#fff;padding:4px 8px;font-size:11px;font-weight:800}
.lb-taccount-th b{font-size:13px}
.lb-taccount-tb{display:grid;grid-template-columns:1fr 1fr}
.lb-taccount-sd{min-height:96px;padding:2px 3px 4px;position:relative;touch-action:manipulation}
.lb-taccount-sd.dr{border-right:2px solid #1b1f3a}
.lb-taccount-sd.tap{cursor:pointer}.lb-taccount-sd.tap:active{background:#f3efff}
.lb-taccount-sd .hd,.lb-taccount-sd .rw{display:grid;grid-template-columns:31px 1fr 52px;gap:2px;font-size:10.5px;align-items:center;min-height:17px}
.lb-taccount-sd .hd{color:#6b7090;font-weight:800;border-bottom:1px solid #e3e6f6;font-size:9.5px}
.lb-taccount-sd .rw span{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-taccount-sd .rw b{text-align:right}
.lb-taccount-sd .rw i{font-style:normal;color:#6b7090;font-size:9px;white-space:nowrap;overflow:hidden}
.lb-taccount-sd .rw.tl b{border-top:1.5px solid #1b1f3a;border-bottom:3px double #1b1f3a}
.lb-taccount-sd .rw.cl span,.lb-taccount-sd .rw.cl b{color:#7044e0}
.lb-taccount-sd .rw.new{animation:lbtaPop .45s ease}
.lb-taccount-sd .ghost{position:absolute;left:0;right:0;bottom:4px;text-align:center;font-size:10.5px;font-weight:800;color:#a8aed0}
@keyframes lbtaPop{0%{background:#fff1b8}100%{background:transparent}}
.lb-taccount-cl{background:#f7f8ff;border-radius:12px;padding:6px 8px;margin-top:6px}
.lb-taccount-cl .rowx{display:flex;gap:5px;align-items:center;flex-wrap:wrap;margin-bottom:4px;font-weight:800;font-size:12px}
.lb-taccount-cl input{width:104px;height:36px;border:2px solid #dfe3f5;border-radius:9px;padding:0 6px;font:inherit;font-weight:800;text-align:right;user-select:text;-webkit-user-select:text}
.lb-taccount-pill{background:#fff;border:2px solid #e3e6f6 !important;border-radius:99px;padding:5px 9px;font-weight:800;font-size:11.5px;min-height:34px;color:#1b1f3a}
.lb-taccount-pill.on{background:#1b1f3a;color:#fff;border-color:#1b1f3a !important}
.lb-taccount-tbl{border:2px solid #e3e6f6;border-radius:12px;overflow:hidden}
.lb-taccount-tbh,.lb-taccount-tbr,.lb-taccount-tbt{display:grid;grid-template-columns:1fr 84px 84px;align-items:center}
.lb-taccount-tbh{background:#1b1f3a;color:#fff;font-weight:800;font-size:11px;padding:4px 6px}
.lb-taccount-tbh span:not(:first-child){text-align:center}
.lb-taccount-sc{max-height:236px;overflow-y:auto}
.lb-taccount-tbr{border-top:1px solid #eef0fb;padding:2px 4px;min-height:42px}
.lb-taccount-tbr .nm{font-weight:800;font-size:12.5px;padding-left:2px}
.lb-taccount-tbr .nm small{display:block;color:#6b7090;font-size:11px;font-weight:700}
.lb-taccount-tbr button{height:36px;margin:0 3px;border-radius:9px;background:#f5f6fc;color:#8a90b4;border:1.5px dashed #d5d9ee !important;font-weight:800;font-size:12px}
.lb-taccount-tbr button.on{background:#eaf2ff;color:#2f6fd6}.lb-taccount-tbr button.on.c{background:#fff0f0;color:#e04848}
.lb-taccount-tbr.bad{background:#fff3f3}.lb-taccount-tbr.ok{background:#f0fdf8}
.lb-taccount-tbt{border-top:2px solid #1b1f3a;padding:5px 4px;font-weight:900;font-size:12.5px}
.lb-taccount-tbt span:not(:first-child){text-align:center}
.lb-taccount-tbt.agr span:not(:first-child){color:#0f9a72}.lb-taccount-tbt.dif span:not(:first-child){color:#e04848}
.lb-taccount-bk{display:flex;gap:6px;margin-bottom:6px}
.lb-taccount-bk div{flex:1;border-radius:12px;padding:5px 8px;font-weight:800;font-size:15px;line-height:1.15}
.lb-taccount-bk small{display:block;font-size:10.5px;color:#6b7090}
.lb-taccount-bk .cb{background:#eaf2ff;color:#2f6fd6}.lb-taccount-bk .pb{background:#fff6dc;color:#a77400}
.lb-taccount-it{display:flex;align-items:center;gap:5px;border-top:1px solid #eef0fb;padding:4px 2px}
.lb-taccount-it .tx{flex:1;font-size:12px;font-weight:700;line-height:1.25}
.lb-taccount-it .tx b{display:block;font-size:12.5px}
.lb-taccount-it button{width:50px;height:38px;border-radius:9px;background:#f5f6fc;color:#6b7090;border:1.5px solid #e3e6f6 !important;font-weight:800;font-size:12px}
.lb-taccount-it button.on.a{background:#2ed3a5;color:#063b2c}.lb-taccount-it button.on.l{background:#ff6b6b;color:#fff}
.lb-taccount-it.bad{background:#fff3f3}.lb-taccount-it.ok{background:#f0fdf8}
.lb-taccount-sum{background:#f7f8ff;border-radius:12px;padding:5px 9px;margin-top:6px;font-size:12px;font-weight:700}
.lb-taccount-sum div{display:flex;justify-content:space-between}
.lb-taccount-sum .fin{border-top:1.5px solid #1b1f3a;margin-top:2px;padding-top:2px;font-weight:900;font-size:13px}
`;

  Labs.register('taccount', {
    title: 'Accounting workbench',
    subjects: ['accountancy', 'commerce'],
    render(host, p, api) {
      p = p && typeof p === 'object' ? p : {};
      const mode = ['journal', 'ledger', 'trialbalance', 'bankrec'].includes(p.mode) ? p.mode : 'journal';
      const firm = p.firm || 'Ravi Traders';
      const types = p.types && typeof p.types === 'object' ? p.types : {};
      let rules = p.rules === 'golden' ? 'golden' : 'modern';
      let txns = normTxns(p.transactions);
      if (!txns.length) txns = normTxns(mode === 'ledger' ? DEF_LEDGER : DEF_TXNS);
      const firstSide = {};
      txns.forEach(t => t.lines.forEach(l => { if (!firstSide[key(l.a)]) firstSide[key(l.a)] = l.side; }));
      const inf = a => infoOf(a, types, firstSide[key(a)]);
      const AC = a => `${esc(a)} A/c`;
      const timers = [];
      host.innerHTML = `<div class="lb-taccount-w"><style>${CSS}</style><div class="lb-taccount-ch"></div><div class="lb-taccount-body"></div></div>`;
      const W = host.firstElementChild, body = W.querySelector('.lb-taccount-body');
      const setCh = t => { W.querySelector('.lb-taccount-ch').textContent = '🎯 Challenge: ' + t; };
      let won = false;
      const win = m => { if (won) return; won = true; api.sfx && api.sfx('correct'); api.win(m); };

      /* ───────────────────────── JOURNAL ───────────────────────── */
      function journal() {
        setCh(p.challenge || `Journalise all ${txns.length} transactions of ${firm} — debits must equal credits`);
        const pool = []; const addP = a => { a = norm(a); if (a && !pool.some(x => key(x) === key(a))) pool.push(a); };
        txns.forEach(t => t.lines.forEach(l => addP(l.a))); (Array.isArray(p.accounts) ? p.accounts : []).forEach(addP);
        ['Cash', 'Bank', 'Capital', 'Purchases', 'Sales', 'Drawings', 'Furniture', 'Salaries', 'Creditors'].forEach(addP);
        let ti = 0, placed = [], sel = null, solved = false, marks = null;
        function chips(t) {
          const need = [...new Set(t.lines.map(l => norm(l.a)))];
          const others = shuffle(pool.filter(a => !need.some(n => key(n) === key(a))), ti + 3).slice(0, Math.max(3, 8 - need.length));
          return shuffle([...need, ...others], ti + 11);
        }
        let chipList = chips(txns[0]);
        function totals() { let d = 0, c = 0; placed.forEach(l => { const v = num(l.amt); if (v > 0) { if (l.side === 'dr') d += v; else c += v; } }); return [d, c]; }
        function drawTot() { const [d, c] = totals(); const el = body.querySelector('.lb-taccount-tot'); if (el) el.innerHTML = `<span>Dr total ₹${inr(d)}</span><span class="${d && same(d, c) ? 'agr' : d || c ? 'dif' : ''}">${d && same(d, c) ? '= ' : d || c ? '≠ ' : ''}Cr total ₹${inr(c)}</span>`; }
        function lineHTML(l, i) {
          const m = marks ? marks[i] : '';
          return `<div class="lb-taccount-ln ${m}" data-i="${i}"><span class="an">${l.side === 'cr' ? '<small>To </small>' : ''}${AC(l.a)}${l.side === 'dr' ? ' <small>…Dr</small>' : ''}</span>` +
            `<input inputmode="numeric" aria-label="amount" placeholder="₹" value="${esc(l.amt)}" ${solved ? 'disabled' : ''}>${solved ? '' : '<button class="x" aria-label="remove">×</button>'}</div>`;
        }
        function draw(msg, cls) {
          const t = txns[ti];
          body.innerHTML = `<div class="lb-taccount-bar"><b>Journal of ${esc(firm)}</b><span class="lb-taccount-pg">Entry ${ti + 1}/${txns.length}</span>
<span class="lb-taccount-seg"><button data-r="modern" class="${rules === 'modern' ? 'on' : ''}">Modern</button><button data-r="golden" class="${rules === 'golden' ? 'on' : ''}">Golden</button></span></div>
<div class="lb-taccount-txn"><i>${esc(t.date)}</i>${esc(t.text)}</div>
${['dr', 'cr'].map(s => `<div class="lb-taccount-zone ${s}${sel && !solved ? ' arm' : ''}" data-side="${s}"><div class="lb-taccount-zh">${s === 'dr' ? 'Debit (Dr) — account' : 'Credit (Cr) — To account'}${sel && !solved ? ' · tap to place ' + esc(sel) : ''}</div>${placed.map((l, i) => l.side === s ? lineHTML(l, i) : '').join('')}</div>`).join('')}
<div class="lb-taccount-tot"></div>
${solved ? '' : `<div class="lb-taccount-chips">${chipList.map(a => `<button class="lb-taccount-chip${sel === a ? ' sel' : ''}" data-a="${esc(a)}">${esc(a)}</button>`).join('')}</div>`}
<div class="lb-taccount-btns">${solved ? (ti < txns.length - 1 ? '<button class="lb-taccount-btn go nx">Next entry ▶</button>' : '<button class="lb-taccount-btn alt rs">↺ Start again</button>') : '<button class="lb-taccount-btn alt clr">Clear</button><button class="lb-taccount-btn chk">Check ✓</button>'}</div>
<div class="lb-taccount-msg ${cls || ''}">${msg || (placed.length ? '' : 'Tap an account, then tap the Debit or Credit box.')}</div>`;
          drawTot();
        }
        function solvedMsg() { const t = txns[ti]; return `✔ Correct! ${t.narration ? `<em>${esc(t.narration)}</em>` : ''}<em>${t.lines.map(l => `${esc(l.a)} A/c: ${esc(why(inf(l.a), l.side, rules))}`).join('<br>')}</em>`; }
        function check() {
          const t = txns[ti], exp = {}, got = {};
          t.lines.forEach(l => { const k = key(l.a) + '|' + l.side; exp[k] = (exp[k] || 0) + l.amt; });
          placed.forEach(l => { const k = key(l.a) + '|' + l.side; got[k] = (got[k] || 0) + (num(l.amt) || 0); });
          const [d, c] = totals();
          marks = placed.map(l => { const k = key(l.a) + '|' + l.side; return exp[k] != null && same(exp[k], got[k]) ? 'ok' : 'bad'; });
          let m = '';
          if (!placed.some(l => l.side === 'dr') || !placed.some(l => l.side === 'cr')) { marks = null; m = 'Every entry needs at least one debit and one credit.'; }
          else if (placed.some(l => !(num(l.amt) > 0))) { marks = null; m = 'Type an amount for every account.'; }
          else {
            const wrongSide = placed.find(l => exp[key(l.a) + '|' + l.side] == null && exp[key(l.a) + '|' + (l.side === 'dr' ? 'cr' : 'dr')] != null);
            const notIn = placed.find(l => exp[key(l.a) + '|dr'] == null && exp[key(l.a) + '|cr'] == null);
            const missing = t.lines.filter(l => !placed.some(x => key(x.a) === key(l.a))).length;
            const wrongAmt = placed.find(l => exp[key(l.a) + '|' + l.side] != null && !same(exp[key(l.a) + '|' + l.side], got[key(l.a) + '|' + l.side]));
            if (notIn) m = `${notIn.a} A/c is not affected by this transaction.`;
            else if (wrongSide) { const s = wrongSide.side === 'dr' ? 'cr' : 'dr'; m = `${wrongSide.a} A/c is on the wrong side. <em>${esc(why(inf(wrongSide.a), s, rules))}</em>`; }
            else if (missing) m = `${missing === 1 ? 'One more account is' : missing + ' more accounts are'} affected — read the transaction again.`;
            else if (!same(d, c)) m = `Dr total (₹${inr(d)}) ≠ Cr total (₹${inr(c)}). Every debit needs an equal credit.`;
            else if (wrongAmt) m = `Check the amount for ${wrongAmt.a} A/c.`;
          }
          if (m) { api.sfx && api.sfx('wrong'); draw(m, 'bad'); return; }
          solved = true; marks = placed.map(() => 'ok'); api.sfx && api.sfx('correct');
          draw(solvedMsg(), 'ok');
          if (ti === txns.length - 1) win(`All ${txns.length} entries are correct — total debits always equal total credits!`);
        }
        body.addEventListener('click', e => {
          const b = e.target.closest('button');
          if (b && b.dataset.r) { rules = b.dataset.r; draw(solved ? solvedMsg() : '', solved ? 'ok' : ''); return; }
          if (b && b.dataset.a != null) { sel = sel === b.dataset.a ? null : b.dataset.a; api.sfx && api.sfx('tap'); draw(); return; }
          if (b && b.classList.contains('x')) { const i = +b.closest('.lb-taccount-ln').dataset.i; placed.splice(i, 1); marks = null; draw(); return; }
          if (b && b.classList.contains('chk')) { check(); return; }
          if (b && b.classList.contains('clr')) { placed = []; marks = null; sel = null; draw(); return; }
          if (b && b.classList.contains('nx')) { ti++; placed = []; marks = null; sel = null; solved = false; chipList = chips(txns[ti]); draw(); return; }
          if (b && b.classList.contains('rs')) { ti = 0; placed = []; marks = null; sel = null; solved = false; chipList = chips(txns[0]); draw(); return; }
          const z = e.target.closest('.lb-taccount-zone');
          if (z && !solved && !e.target.closest('input')) {
            if (!sel) { draw('First tap an account chip below, then tap this box.'); return; }
            const side = z.dataset.side;
            if (!placed.some(l => key(l.a) === key(sel) && l.side === side)) {
              const [d, c] = totals(), gap = side === 'dr' ? c - d : d - c;
              placed.push({ a: sel, side, amt: gap > 0 ? String(gap) : '' }); marks = null; api.sfx && api.sfx('tap');
            }
            sel = null; draw();
            const ins = body.querySelectorAll('.lb-taccount-ln input'); const last = [...ins].find(x => !x.value); if (last && !('ontouchstart' in window)) last.focus();
          }
        });
        body.addEventListener('input', e => { const ln = e.target.closest('.lb-taccount-ln'); if (!ln) return; placed[+ln.dataset.i].amt = e.target.value; if (marks) { marks = null; ln.classList.remove('ok', 'bad'); } drawTot(); });
        draw();
      }

      /* ───────────────────────── LEDGER ───────────────────────── */
      function ledger() {
        const closeD = p.closeDate || 'Mar 31', openD = p.openDate || 'Apr 1';
        setCh(p.challenge || `Post every entry to the ledger, then balance or close each account`);
        const accs = [], A = {};
        const acc = a => { const k = key(a); if (!A[k]) { A[k] = { name: norm(a), dr: [], cr: [], close: null }; accs.push(A[k]); } return A[k]; };
        txns.forEach(t => {
          const drs = t.lines.filter(l => l.side === 'dr'), crs = t.lines.filter(l => l.side === 'cr'); t.posts = [];
          if (drs.length === 1) crs.forEach(c => { t.posts.push({ acc: drs[0].a, side: 'dr', part: c.a, amt: c.amt }); t.posts.push({ acc: c.a, side: 'cr', part: drs[0].a, amt: c.amt }); });
          else if (crs.length === 1) drs.forEach(d => { t.posts.push({ acc: d.a, side: 'dr', part: crs[0].a, amt: d.amt }); t.posts.push({ acc: crs[0].a, side: 'cr', part: d.a, amt: d.amt }); });
          else t.lines.forEach(l => t.posts.push({ acc: l.a, side: l.side, part: 'Sundries', amt: l.amt }));
          t.posts.forEach(q => acc(q.acc));
        });
        let ei = 0, tab = accs[0], phase = 'post', fresh = null, cl = { side: null, type: null, amt: '' };
        const tot = a => [a.dr.reduce((s, r) => s + r.amt, 0), a.cr.reduce((s, r) => s + r.amt, 0)];
        const closeTypes = a => { const i = inf(a.name); return i.type === 'drawings' ? ['cd', CAP, PL] : ['cd', TR, PL]; };
        const TN = { cd: 'Balance c/d', [TR]: 'Trading A/c', [PL]: 'P&L A/c', [CAP]: 'Capital A/c' };
        const PART = { cd: 'Balance c/d', [TR]: 'Trading A/c', [PL]: 'Profit and Loss A/c', [CAP]: 'Capital A/c' };
        function rowsHTML(a, side) {
          const rows = a[side].map(r => ({ ...r, pre: side === 'dr' ? 'To' : 'By' }));
          return rows;
        }
        function tHTML(a) {
          const L = rowsHTML(a, 'dr'), R = rowsHTML(a, 'cr');
          const c = a.close;
          if (c && c.amt > 0) (c.side === 'dr' ? L : R).push({ date: closeD, part: PART[c.type], pre: c.side === 'dr' ? 'To' : 'By', amt: c.amt, cls: 'cl', raw: true });
          const n = Math.max(L.length, R.length);
          const pad = arr => { while (arr.length < n) arr.push(null); };
          pad(L); pad(R);
          if (c) { const [d, cr] = tot(a); const tt = Math.max(d + (c.side === 'dr' ? c.amt : 0), cr + (c.side === 'cr' ? c.amt : 0)); L.push({ tl: 1, amt: tt }); R.push({ tl: 1, amt: tt });
            if (c.type === 'cd' && c.amt > 0) { const bd = { date: openD, part: 'Balance b/d', pre: c.side === 'dr' ? 'By' : 'To', amt: c.amt, cls: 'cl', raw: true }; if (c.side === 'dr') { R.push(bd); L.push(null); } else { L.push(bd); R.push(null); } } }
          const rw = r => !r ? '<div class="rw"></div>' : r.tl ? `<div class="rw tl"><i></i><span></span><b>${inr(r.amt)}</b></div>` :
            `<div class="rw ${r.cls || ''}${r === fresh ? ' new' : ''}"><i>${esc(r.date)}</i><span>${r.pre} ${r.raw ? esc(r.part) : AC(r.part)}</span><b>${inr(r.amt)}</b></div>`;
          const hd = '<div class="hd"><span>Date</span><span>Particulars</span><span style="text-align:right">₹</span></div>';
          const tapping = phase === 'post';
          return `<div class="lb-taccount-t"><div class="lb-taccount-th"><span>Dr.</span><b>${esc(a.name)} Account</b><span>Cr.</span></div><div class="lb-taccount-tb">` +
            `<div class="lb-taccount-sd dr${tapping ? ' tap' : ''}" data-side="dr">${hd}${L.map(rw).join('')}${tapping ? '<div class="ghost">tap to post on Dr side</div>' : ''}</div>` +
            `<div class="lb-taccount-sd cr${tapping ? ' tap' : ''}" data-side="cr">${hd}${R.map(rw).join('')}${tapping ? '<div class="ghost">tap to post on Cr side</div>' : ''}</div></div></div>`;
        }
        function jeHTML() {
          if (phase !== 'post') return '';
          const t = txns[ei];
          const doneLine = l => t.posts.filter(q => key(q.acc) === key(l.a) && q.side === l.side).every(q => q.done);
          return `<div class="lb-taccount-je"><div class="d">Journal entry ${ei + 1}/${txns.length} · ${esc(t.date)} — ${esc(t.text)}</div>` +
            t.lines.map(l => `<div class="r ${doneLine(l) ? 'dn' : ''}"><span>${l.side === 'cr' ? '&nbsp;&nbsp;&nbsp;To ' : ''}${AC(l.a)}${l.side === 'dr' ? ' …Dr' : ''}</span><b>${l.side === 'dr' ? inr(l.amt) : ''}</b><b>${l.side === 'cr' ? inr(l.amt) : ''}</b></div>`).join('') + '</div>';
        }
        function clHTML() {
          if (phase !== 'close' || tab.close) return '';
          return `<div class="lb-taccount-cl"><div class="rowx">Close ${esc(tab.name)} A/c: ₹<input inputmode="numeric" placeholder="balance" value="${esc(cl.amt)}"><span style="flex:1"></span>
<button class="lb-taccount-pill ${cl.side === 'dr' ? 'on' : ''}" data-cs="dr">on Dr side</button><button class="lb-taccount-pill ${cl.side === 'cr' ? 'on' : ''}" data-cs="cr">on Cr side</button></div>
<div class="rowx">${closeTypes(tab).map(k => `<button class="lb-taccount-pill ${cl.type === k ? 'on' : ''}" data-ct="${k}">${TN[k]}</button>`).join('')}<button class="lb-taccount-btn" data-close style="flex:1;min-width:70px;min-height:36px">Close ✓</button></div></div>`;
        }
        function draw(msg, cls) {
          body.innerHTML = `${jeHTML()}<div class="lb-taccount-tabs">${accs.map(a => `<button data-tab="${esc(a.name)}" class="${a === tab ? 'on' : ''} ${a.close ? 'dn' : ''}">${esc(a.name)}${a.close ? ' ✓' : ''}</button>`).join('')}</div>
${tHTML(tab)}${clHTML()}<div class="lb-taccount-msg ${cls || ''}">${msg || (phase === 'post' ? 'Pick the account tab, then tap the side to post on.' : phase === 'close' ? 'All posted! Now balance or close every account.' : '')}</div>`;
          fresh = null;
        }
        function tapSide(side) {
          const t = txns[ei];
          const q = t.posts.find(q => !q.done && key(q.acc) === key(tab.name) && q.side === side);
          if (!q) {
            const other = t.posts.find(q => !q.done && key(q.acc) === key(tab.name));
            if (other) { api.sfx && api.sfx('wrong'); draw(`${esc(tab.name)} A/c was ${other.side === 'dr' ? 'DEBITED' : 'CREDITED'} in the journal, so post it on the ${other.side === 'dr' ? 'Dr (left)' : 'Cr (right)'} side.`, 'bad'); return; }
            const any = t.posts.find(q => !q.done);
            api.sfx && api.sfx('hmm');
            draw(t.posts.some(q => key(q.acc) === key(tab.name)) ? `${esc(tab.name)} A/c is done for this entry. Now post ${any ? AC(any.acc) : 'the other account'}.` : `${esc(tab.name)} A/c is not in this entry — pick another tab.`, 'bad'); return;
          }
          q.done = true; const r = { date: t.date, part: q.part, amt: q.amt }; tab[side].push(r); fresh = r; api.sfx && api.sfx('coin');
          const msg = `Posted: ${side === 'dr' ? 'To' : 'By'} ${esc(q.part)} A/c ₹${inr(q.amt)} on the ${side === 'dr' ? 'debit' : 'credit'} side of ${esc(tab.name)} A/c.`;
          if (t.posts.every(q => q.done)) {
            if (ei < txns.length - 1) { ei++; draw(msg + ' Entry complete ✓ — next one!', 'ok'); }
            else { phase = 'close'; cl = { side: null, type: null, amt: '' }; draw('✔ All entries posted! Now close each account: type its balance, pick the side and how it is closed.', 'ok'); }
          } else draw(msg, 'ok');
        }
        function closeIt() {
          const [d, c] = tot(tab), bal = d - c, i = inf(tab.name), v = num(cl.amt);
          const want = i.type === 'drawings' ? CAP : i.close ? i.close : 'cd';
          if (!(v >= 0)) { draw('Type the balance amount first.', 'bad'); return; }
          if (same(bal, 0)) { if (!same(v, 0)) { draw(`Both sides already total ₹${inr(d)} — the balance is 0.`, 'bad'); return; } tab.close = { side: 'dr', type: 'cd', amt: 0 }; }
          else {
            const side = bal > 0 ? 'cr' : 'dr';
            if (!same(v, Math.abs(bal))) { api.sfx && api.sfx('wrong'); draw(`Not quite: balance = bigger side total − smaller side total (Dr ₹${inr(d)}, Cr ₹${inr(c)}).`, 'bad'); return; }
            if (!cl.side) { draw('Choose the side the balancing figure goes on.', 'bad'); return; }
            if (cl.side !== side) { api.sfx && api.sfx('wrong'); draw(`Write the balancing figure on the SMALLER side (${side === 'dr' ? 'Dr' : 'Cr'}), so both sides total the same.`, 'bad'); return; }
            if (!cl.type) { draw('Choose how the account is closed.', 'bad'); return; }
            if (cl.type !== want) {
              api.sfx && api.sfx('wrong');
              draw(want === 'cd' ? `${esc(tab.name)} A/c is a ${i.type === 'capital' ? 'capital' : i.type} (real / personal) account — its balance is carried down (c/d) to the next period.` :
                want === CAP ? 'Drawings are closed by transfer to the Capital A/c.' :
                  `${esc(tab.name)} A/c is a${i.type === 'expense' ? 'n expense' : ' revenue'} account — it is not carried down but closed by transfer to the ${want === TR ? 'Trading A/c' : 'Profit and Loss A/c'}.`, 'bad'); return;
            }
            tab.close = { side, type: want, amt: Math.abs(bal) };
          }
          api.sfx && api.sfx('correct');
          const left = accs.filter(a => !a.close);
          const done = tab;
          if (!left.length) { draw('✔ Every account is balanced or closed — the ledger is ready for the trial balance!', 'ok'); win(`Ledger complete: ${txns.length} entries posted and ${accs.length} accounts balanced/closed.`); return; }
          cl = { side: null, type: null, amt: '' };
          const m = done.close.amt === 0 ? `${esc(done.name)} A/c has no balance.` : done.close.type === 'cd' ? `${esc(done.name)} A/c: Balance c/d ₹${inr(done.close.amt)}, brought down as Balance b/d.` : `${esc(done.name)} A/c closed by transfer to ${PART[done.close.type]}.`;
          draw('✔ ' + m + ` ${left.length} to go.`, 'ok');
        }
        body.addEventListener('click', e => {
          const b = e.target.closest('button');
          if (b && b.dataset.tab != null) { tab = accs.find(a => a.name === b.dataset.tab) || tab; cl = { side: null, type: null, amt: '' }; draw(); return; }
          if (b && b.dataset.cs) { cl.side = b.dataset.cs; draw(); return; }
          if (b && b.dataset.ct) { cl.type = b.dataset.ct; draw(); return; }
          if (b && b.hasAttribute('data-close')) { closeIt(); return; }
          const sd = e.target.closest('.lb-taccount-sd');
          if (sd && phase === 'post') tapSide(sd.dataset.side);
        });
        body.addEventListener('input', e => { if (e.target.closest('.lb-taccount-cl')) cl.amt = e.target.value; });
        draw();
      }

      /* ───────────────────────── TRIAL BALANCE ───────────────────────── */
      function trial() {
        let rows = [];
        if (Array.isArray(p.balances) && p.balances.length) rows = p.balances.map(b => b && ({ a: norm(b.a || b.account || b.name), amt: +b.amt, side: b.side === 'dr' || b.side === 'cr' ? b.side : null }));
        else if (p.balances && typeof p.balances === 'object') rows = Object.entries(p.balances).map(([a, v]) => ({ a: norm(a), amt: +v, side: null }));
        rows = rows.filter(r => r && r.a && r.amt > 0);
        if (!rows.length && Array.isArray(p.transactions) && txns.length) {
          const m = {}, order = [];
          txns.forEach(t => t.lines.forEach(l => { const k = key(l.a); if (m[k] == null) { m[k] = { a: l.a, v: 0 }; order.push(k); } m[k].v += l.side === 'dr' ? l.amt : -l.amt; }));
          rows = order.map(k => m[k]).filter(x => !same(x.v, 0)).map(x => ({ a: x.a, amt: Math.abs(x.v), side: x.v > 0 ? 'dr' : 'cr' }));
        }
        if (!rows.length) rows = DEF_TB.map(r => ({ ...r, side: null }));
        rows.forEach(r => { if (!r.side) r.side = DRSIDE[inf(r.a).type] ? 'dr' : 'cr'; r.pick = null; r.mark = ''; });
        const tD = rows.reduce((s, r) => s + (r.side === 'dr' ? r.amt : 0), 0), tC = rows.reduce((s, r) => s + (r.side === 'cr' ? r.amt : 0), 0);
        if (!same(tD, tC)) console.warn('taccount: trial balance params do not agree', tD, tC);
        setCh(p.challenge || `Put every balance in the Dr or Cr column — the totals must agree`);
        function draw(msg, cls) {
          const d = rows.reduce((s, r) => s + (r.pick === 'dr' ? r.amt : 0), 0), c = rows.reduce((s, r) => s + (r.pick === 'cr' ? r.amt : 0), 0), all = rows.every(r => r.pick);
          body.innerHTML = `<div class="lb-taccount-bar"><b>Trial Balance of ${esc(firm)} as at ${esc(p.tbDate || '31st March, 2026')}</b></div>
<div class="lb-taccount-tbl"><div class="lb-taccount-tbh"><span>Account</span><span>Dr (₹)</span><span>Cr (₹)</span></div><div class="lb-taccount-sc">
${rows.map((r, i) => `<div class="lb-taccount-tbr ${r.mark}" data-i="${i}"><div class="nm">${AC(r.a)}<small>₹${inr(r.amt)}</small></div><button data-s="dr" class="${r.pick === 'dr' ? 'on' : ''}">${r.pick === 'dr' ? inr(r.amt) : 'Dr'}</button><button data-s="cr" class="c ${r.pick === 'cr' ? 'on' : ''}">${r.pick === 'cr' ? inr(r.amt) : 'Cr'}</button></div>`).join('')}
</div><div class="lb-taccount-tbt ${all ? (same(d, c) ? 'agr' : 'dif') : ''}"><span>Total</span><span>${inr(d)}</span><span>${inr(c)}</span></div></div>
<div class="lb-taccount-btns" style="margin-top:6px"><button class="lb-taccount-btn alt rs">Reset</button><button class="lb-taccount-btn chk">Check ✓</button></div>
<div class="lb-taccount-msg ${cls || ''}">${msg || (all ? (same(d, c) ? 'Totals agree — press Check.' : `Totals differ by ₹${inr(Math.abs(d - c))}.`) : `${rows.filter(r => !r.pick).length} balances still to place.`)}</div>`;
        }
        body.addEventListener('click', e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.s) { const sc = body.querySelector('.lb-taccount-sc').scrollTop; const r = rows[+b.closest('.lb-taccount-tbr').dataset.i]; r.pick = r.pick === b.dataset.s ? null : b.dataset.s; r.mark = ''; api.sfx && api.sfx('tap'); draw(); body.querySelector('.lb-taccount-sc').scrollTop = sc; return; }
          if (b.classList.contains('rs')) { rows.forEach(r => { r.pick = null; r.mark = ''; }); draw(); return; }
          if (b.classList.contains('chk')) {
            if (rows.some(r => !r.pick)) { draw('Place every balance first.', 'bad'); return; }
            rows.forEach(r => r.mark = r.pick === r.side ? 'ok' : 'bad');
            const bad = rows.filter(r => r.mark === 'bad');
            if (!bad.length) { draw(`✔ Correct! Both columns total ₹${inr(tD)}. Assets, expenses and drawings have debit balances; capital, liabilities and incomes have credit balances.`, 'ok'); win(`Trial balance agrees: Dr ₹${inr(tD)} = Cr ₹${inr(tC)}`); return; }
            const r = bad[0], ty = inf(r.a).type, d = rows.reduce((s, x) => s + (x.pick === 'dr' ? x.amt : 0), 0), c = rows.reduce((s, x) => s + (x.pick === 'cr' ? x.amt : 0), 0);
            api.sfx && api.sfx('wrong');
            draw(`${bad.length} in the wrong column${same(d, c) ? ' (the totals agree, but errors can cancel out!)' : ''}. Hint: ${esc(r.a)} A/c — ${{ asset: 'an asset', expense: 'an expense / loss', drawings: 'drawings', liability: 'a liability', capital: 'capital', revenue: 'an income / gain' }[ty]} usually has a ${r.side === 'dr' ? 'debit' : 'credit'} balance.`, 'bad');
          }
        });
        draw();
      }

      /* ───────────────────────── BANK RECONCILIATION ───────────────────────── */
      function bankrec() {
        const start = p.start === 'passbook' ? 'passbook' : 'cashbook', od = !!p.overdraft;
        const bal = +p.balance > 0 ? +p.balance : 45000;
        let items = (Array.isArray(p.items) && p.items.length ? p.items : DEF_ITEMS).map(it => {
          if (!it || typeof it !== 'object') return null;
          const d = BRS[it.type]; const pb = it.pb === 1 || it.pb === -1 ? it.pb : d ? d[0] : 0;
          return pb && +it.amt > 0 ? { text: it.text || (d ? d[1] : ''), why: it.why || (d ? d[2] : ''), amt: +it.amt, pb, pick: null, mark: '' } : null;
        }).filter(Boolean);
        if (!items.length) items = DEF_ITEMS.map(it => ({ text: BRS[it.type][1], why: BRS[it.type][2], amt: it.amt, pb: BRS[it.type][0], pick: null, mark: '' }));
        const dir = start === 'cashbook' ? 1 : -1, sg = od ? -1 : 1;
        items.forEach(it => it.need = dir * it.pb * sg > 0 ? 'add' : 'less');
        const Fstart = od ? -bal : bal, Fother = Fstart + dir * items.reduce((s, it) => s + it.pb * it.amt, 0);
        const CB = start === 'cashbook' ? 'Cash Book' : 'Pass Book', OB = start === 'cashbook' ? 'Pass Book' : 'Cash Book';
        const sideTxt = (book, F) => book === 'Cash Book' ? (F >= 0 ? 'Dr' : 'Cr, overdraft') : (F >= 0 ? 'Cr' : 'Dr, overdraft');
        setCh(p.challenge || `Mark each item Add or Less so your BRS gives the ${OB} balance`);
        function draw(msg, cls) {
          const add = items.reduce((s, it) => s + (it.pick === 'add' ? it.amt : 0), 0), less = items.reduce((s, it) => s + (it.pick === 'less' ? it.amt : 0), 0);
          const all = items.every(it => it.pick), R = bal + add - less; /* in the units of the starting figure */
          const RF = od ? -R : R;
          const sc = body.querySelector('.lb-taccount-sc'); const st = sc ? sc.scrollTop : 0;
          body.innerHTML = `<div class="lb-taccount-bar"><b>BRS of ${esc(firm)} as at ${esc(p.brsDate || '31st March, 2026')}</b></div>
<div class="lb-taccount-bk"><div class="cb">₹${inr(bal)}<small>${od ? 'Overdraft' : 'Balance'} as per ${CB} (${sideTxt(CB, Fstart)})</small></div><div class="pb">₹${inr(Math.abs(Fother))}<small>${OB} shows (${sideTxt(OB, Fother)})</small></div></div>
<div class="lb-taccount-sc" style="max-height:164px">${items.map((it, i) => `<div class="lb-taccount-it ${it.mark}" data-i="${i}"><div class="tx">${esc(it.text)}<b>₹${inr(it.amt)}</b></div><button data-p="add" class="a ${it.pick === 'add' ? 'on' : ''}">Add</button><button data-p="less" class="l ${it.pick === 'less' ? 'on' : ''}">Less</button></div>`).join('')}</div>
<div class="lb-taccount-sum"><div><span>${od ? 'Overdraft' : 'Balance'} as per ${CB}</span><b>${inr(bal)}</b></div><div><span>Add: items marked Add</span><b>${inr(add)}</b></div><div><span>Less: items marked Less</span><b>(${inr(less)})</b></div>
<div class="fin"><span>${all ? `${(od ? R >= 0 : R < 0) ? 'Overdraft' : 'Balance'} as per ${OB}` : `${OB} balance (finish all items)`}</span><b>${all ? inr(Math.abs(R)) : '?'}</b></div></div>
<div class="lb-taccount-btns" style="margin-top:6px"><button class="lb-taccount-btn alt rs">Reset</button><button class="lb-taccount-btn chk">Check ✓</button></div>
<div class="lb-taccount-msg ${cls || ''}">${msg || (all ? (same(RF, Fother) ? 'Your BRS matches the ' + OB + '! Press Check.' : `Your BRS gives ₹${inr(Math.abs(R))}, but the ${OB} shows ₹${inr(Math.abs(Fother))}.`) : 'Ask: does this item make the ' + OB + ' balance higher or lower?')}</div>`;
          const sc2 = body.querySelector('.lb-taccount-sc'); if (sc2) sc2.scrollTop = st;
        }
        body.addEventListener('click', e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.p) { const it = items[+b.closest('.lb-taccount-it').dataset.i]; it.pick = it.pick === b.dataset.p ? null : b.dataset.p; it.mark = ''; api.sfx && api.sfx('tap'); draw(); return; }
          if (b.classList.contains('rs')) { items.forEach(it => { it.pick = null; it.mark = ''; }); draw(); return; }
          if (b.classList.contains('chk')) {
            if (items.some(it => !it.pick)) { draw('Mark every item Add or Less first.', 'bad'); return; }
            items.forEach(it => it.mark = it.pick === it.need ? 'ok' : 'bad');
            const bad = items.filter(it => it.mark === 'bad');
            if (!bad.length) { draw(`✔ Reconciled! ${od ? 'Overdraft' : 'Balance'} as per ${CB} ₹${inr(bal)} → ${Fother >= 0 ? 'balance' : 'overdraft'} as per ${OB} ₹${inr(Math.abs(Fother))}.`, 'ok'); win(`BRS done: the ${OB} ${Fother >= 0 ? 'balance' : 'overdraft'} is ₹${inr(Math.abs(Fother))}`); return; }
            const it = bad[0]; api.sfx && api.sfx('wrong');
            draw(`${bad.length} item${bad.length > 1 ? 's' : ''} wrong. “${esc(it.text)}”: ${esc(it.why)} So the ${OB} ${od ? 'overdraft' : 'balance'} is ${it.need === 'add' ? 'HIGHER' : 'LOWER'} → ${it.need === 'add' ? 'Add' : 'Less'}.`, 'bad');
          }
        });
        draw();
      }

      ({ journal, ledger, trialbalance: trial, bankrec })[mode]();
      return () => { timers.forEach(clearTimeout); host.innerHTML = ''; };
    },
    example: {
      mode: 'journal', firm: 'Ravi Traders', rules: 'modern',
      challenge: 'Journalise the April transactions of Ravi Traders (one is a compound entry!)',
      transactions: [
        { date: 'Apr 1', text: 'Ravi started business with cash ₹1,00,000', dr: 'Cash', cr: 'Capital', amt: 100000, narration: '(Being business started with cash)' },
        { date: 'Apr 3', text: 'Deposited ₹40,000 cash into the bank', dr: 'Bank', cr: 'Cash', amt: 40000, narration: '(Being cash deposited into bank)' },
        { date: 'Apr 5', text: 'Bought goods from Mohan on credit ₹30,000', dr: 'Purchases', cr: 'Mohan', amt: 30000, narration: '(Being goods purchased on credit)' },
        { date: 'Apr 10', text: 'Sold goods for ₹25,000 — ₹15,000 in cash, the rest on credit to Sita', dr: [{ a: 'Cash', amt: 15000 }, { a: 'Sita', amt: 10000 }], cr: 'Sales', amt: 25000, narration: '(Being goods sold partly for cash and partly on credit)' },
        { date: 'Apr 25', text: 'Ravi withdrew ₹3,000 cash for personal use', dr: 'Drawings', cr: 'Cash', amt: 3000, narration: '(Being cash withdrawn for personal use)' }
      ],
      accounts: ['Furniture', 'Salaries', 'Creditors']
    },
    examples: [
      { mode: 'ledger', firm: 'Meera Stores', challenge: 'Post these entries to the ledger and balance every account on 31st March',
        transactions: [
          { date: 'Mar 1', text: 'Started business with cash', dr: 'Cash', cr: 'Capital', amt: 80000 },
          { date: 'Mar 4', text: 'Bought furniture for cash', dr: 'Furniture', cr: 'Cash', amt: 15000 },
          { date: 'Mar 9', text: 'Purchased goods for cash', dr: 'Purchases', cr: 'Cash', amt: 25000 },
          { date: 'Mar 20', text: 'Sold goods to Arjun on credit', dr: 'Arjun', cr: 'Sales', amt: 32000 },
          { date: 'Mar 28', text: 'Received cash from Arjun', dr: 'Cash', cr: 'Arjun', amt: 20000 }
        ], closeDate: 'Mar 31', openDate: 'Apr 1' },
      { mode: 'trialbalance', firm: 'Kapoor & Sons', tbDate: '31st March, 2026', challenge: 'Prepare the trial balance — then see that the totals agree',
        balances: [{ a: 'Capital', amt: 250000 }, { a: 'Drawings', amt: 18000 }, { a: 'Building', amt: 150000 }, { a: 'Cash', amt: 12000 }, { a: 'Purchases', amt: 95000 }, { a: 'Sales', amt: 140000 },
          { a: 'Wages', amt: 14000 }, { a: 'Debtors', amt: 36000 }, { a: 'Creditors', amt: 22000 }, { a: 'Bank Loan', amt: 40000 }, { a: 'Interest Received', amt: 3000 }, { a: 'Machinery', amt: 130000 }] },
      { mode: 'bankrec', firm: 'Sharma Electricals', start: 'cashbook', balance: 28400, overdraft: false, brsDate: '31st March, 2026',
        challenge: 'Prepare the BRS starting from the Cash Book balance of ₹28,400',
        items: [{ type: 'issued_not_presented', amt: 9600 }, { type: 'deposited_not_credited', amt: 6500 }, { type: 'bank_charges', amt: 350 }, { type: 'dishonoured', amt: 2000 }, { type: 'collected_by_bank', amt: 4200 }] }
    ]
  });
})();
