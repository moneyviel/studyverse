/* ================= CA Foundation question engine (CAGen) =================
   Unlimited, ever-changing, code-generated practice for CA Foundation (ICAI, May 2027 edition scope).
   Accurate BY CONSTRUCTION: every figure in a question, its four options and its working is computed
   here with exact arithmetic (BigInt fractions; square roots rounded exactly with integer square
   roots), formatted in Indian style (₹1,23,456.50). Wrong options are computed from real student
   mistakes (wrong sign, missed adjustment, wrong formula, wrong period ...) and are always distinct.
   Templates are original; only the scope and conventions follow the ICAI study material.
   Coverage: 106 generators over 62 Foundation units (Paper 1: 46, Paper 3: 43, Paper 4: 17); show-working
   (descriptive) variants with step-mark schemes: p1_brs (BRS), p1_dep_schedule, p1_iod_product (product
   method), p1_gross_profit (Trading Account), p1_appropriation (P&L Appropriation Account).  CAGen.list() for all.
   Independent check: python3 tools/ca_gen_verify.py [N]  (Node harness tools/ca_gen_dump.js makes N items per
   generator; Python re-computes every answer with Fractions, checks options, working, formatting).

   API (window.CAGen)
     CAGen.units()                         -> ['fnd-p1-ch02-u01', ...] unit ids that have generators
     CAGen.has(unitId)                     -> true if at least one generator serves the unit
     CAGen.list(unitId?)                   -> [{id, name, unit[], concept, paper, kinds[]}]
     CAGen.next(unitId, {difficulty, seed, gen, kind})
                                           -> one item (see below) or null.  difficulty: 'easy' |
                                              'moderate' | 'ICAI' (also accepts core/hard).  seed (int)
                                              makes the item reproducible.  gen = force a generator id.
                                              kind: 'mcq' (default) | 'desc' (show-working question).
     CAGen.desc(unitId, opts)              -> same as next(unitId, {...opts, kind:'desc'})
     CAGen.mix(unitIds, n, {difficulty, seed})
                                           -> n fresh MCQs spread over the units (round-robin over
                                              generators, no repeated question text, avoids texts
                                              seen recently by this student)
     CAGen.freshSet(pool, n, history?, {unit, genShare, seed})
                                           -> n MCQs for a test built from the unit's hand-written MCQs
                                              (pool = unit.mcqs; each copy gets shuffled options and
                                              a remapped answer) chosen by spaced repetition (wrong ones
                                              come back sooner, recently seen ones rest), topped up /
                                              varied with generated items (default genShare 0.4 when a
                                              generator exists for the unit).  Items carry .key
                                              ("uid#mid" or "gen:<genId>:<hash>") for record().
     CAGen.record(key, ok)                 -> store the result in the student's history (spacing)
     CAGen.history() / CAGen.resetHistory()
   MCQ item: {kind:'mcq', id, gen, unit, concept, q, options[4], answer (index), explain,
              steps[] (last = "Answer: <exact option text>"), marks (Paper 1/2 = 2, Paper 3/4 = 1),
              difficulty, paper, data{inputs}}
   Descriptive item (kind:'desc', Paper 1): {id, gen, unit, concept, marks, minutes, difficulty, pad,
              q, given[], model[blocks as content/ca README], scheme[{id, pt, m, skill}] (adds up to
              marks), steps[], answer (final figure text), data}
   History: localStorage 'sv_cagen' = {v:1, n:<test number>, s:{key:[box, lastTest, lastDay, wrongs]},
              h:[recent question hashes]}  (compact, pruned to 1500 keys / 400 hashes).
   ========================================================================================= */
(function () {
  'use strict';
  /* ---------- seeded randomness ---------- */
  let rnd = Math.random;
  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = (a, b) => a + Math.floor(rnd() * (b - a + 1));
  const RS = (a, b, s) => s * R(Math.ceil(a / s), Math.floor(b / s));           // random multiple of s in [a, b]
  const pick = a => a[Math.floor(rnd() * a.length)];
  const chance = p => rnd() < p;
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (a, k) => shuffle(a).slice(0, k);
  const distinctNames = (list, k) => sample(list, k);

  /* ---------- exact rational arithmetic (BigInt) ---------- */
  const BI = x => typeof x === 'bigint' ? x : BigInt(x);
  function bg(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) [a, b] = [b, a % b]; return a; }
  class Fx {
    constructor(n, d = 1n) { n = BI(n); d = BI(d); if (d === 0n) throw new Error('div0'); if (d < 0n) { n = -n; d = -d; } const g = bg(n, d) || 1n; this.n = n / g; this.d = d / g; }
    add(o) { o = F(o); return new Fx(this.n * o.d + o.n * this.d, this.d * o.d); }
    sub(o) { o = F(o); return new Fx(this.n * o.d - o.n * this.d, this.d * o.d); }
    mul(o) { o = F(o); return new Fx(this.n * o.n, this.d * o.d); }
    div(o) { o = F(o); return new Fx(this.n * o.d, this.d * o.n); }
    neg() { return new Fx(-this.n, this.d); }
    abs() { return this.n < 0n ? this.neg() : this; }
    cmp(o) { o = F(o); const x = this.n * o.d - o.n * this.d; return x > 0n ? 1 : x < 0n ? -1 : 0; }
    eq(o) { return this.cmp(o) === 0; }
    lt(o) { return this.cmp(o) < 0; }
    gt(o) { return this.cmp(o) > 0; }
    get sign() { return this.n > 0n ? 1 : this.n < 0n ? -1 : 0; }
    get int() { return this.d === 1n; }
    get v() { return Number(this.n) / Number(this.d); }
    pow(k) { let r = F(1); for (let i = 0; i < Math.abs(k); i++) r = r.mul(this); return k < 0 ? F(1).div(r) : r; }
  }
  function F(x, d) {
    if (d !== undefined) return F(x).div(F(d));
    if (x instanceof Fx) return x;
    if (typeof x === 'bigint') return new Fx(x);
    if (typeof x === 'number') { if (Number.isSafeInteger(x)) return new Fx(BigInt(x)); if (!Number.isFinite(x)) throw new Error('bad number'); return F(String(x)); }
    let s = String(x).trim(); if (s.includes('/')) { const [p, q] = s.split('/'); return F(p).div(F(q)); }
    if (/e/i.test(s)) throw new Error('exp notation');
    const neg = s[0] === '-'; if (neg) s = s.slice(1); const [i, f = ''] = s.split('.'); const r = new Fx(BigInt(i + f || '0'), 10n ** BigInt(f.length)); return neg ? r.neg() : r;
  }
  const sum = a => a.reduce((s, x) => s.add(x), F(0));
  function isqrt(n) { n = BI(n); if (n < 0n) throw new Error('neg'); if (n < 2n) return n; let x = BigInt(Math.floor(Math.sqrt(Number(n)))); while (x * x > n) x--; while ((x + 1n) * (x + 1n) <= n) x++; return x; }
  function roundDp(x, dp) { x = F(x); const m = 10n ** BigInt(dp), s = x.n < 0n ? -1n : 1n, a = (x.n < 0n ? -x.n : x.n) * m * 2n, q = (a / x.d + 1n) / 2n; return new Fx(s * q, m); }   // half away from zero
  function sqrtRound(x, dp) { x = F(x); if (x.n < 0n) throw new Error('neg'); const m = 10n ** BigInt(dp), s = isqrt(x.n * 4n * m * m / x.d); return new Fx((s + 1n) / 2n, m); }  // exact rounding of √x
  const isSq = n => { n = BI(n); if (n < 0n) return false; const r = isqrt(n); return r * r === n; };
  const sqrtExact = x => { x = F(x); if (isSq(x.n) && isSq(x.d)) return new Fx(isqrt(x.n), isqrt(x.d)); return null; };
  const gcdN = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
  const fact = n => n <= 1 ? 1n : BI(n) * fact(n - 1);
  const nPr = (n, r) => { let x = 1n; for (let k = 0; k < r; k++) x *= BI(n - k); return x; };
  const nCr = (n, r) => r < 0 || r > n ? 0n : nPr(n, r) / fact(r);
  const badDp = (x, k) => { const d = dpOf(x); return d === null || d > k; };   // true if x needs more than k decimals (or never terminates)
  const dpOf = x => { x = F(x); let k = 0; while (k <= 8 && (10n ** BigInt(k)) % x.d) k++; return k > 8 ? null : k; };

  /* ---------- formatting: Indian commas, real minus sign, ₹ ---------- */
  function ind(n) { n = BI(n instanceof Fx ? (() => { if (!n.int) throw new Error('not int'); return n.n; })() : n); let s = (n < 0n ? -n : n).toString(); if (s.length > 3) s = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + s.slice(-3); return (n < 0n ? '−' : '') + s; }
  function fixed(x, dp) { const r = roundDp(x, dp), m = 10n ** BigInt(dp), a = r.n < 0n ? -r.n : r.n, ip = a / r.d * 1n, num = a * m / r.d; const i = num / m, f = num % m; return (r.n < 0n ? '−' : '') + ind(i) + (dp ? '.' + f.toString().padStart(dp, '0') : ''); }
  function num(x, maxdp = 4) { x = F(x); if (x.int) return ind(x.n); const k = dpOf(x); if (k !== null && k <= maxdp) return fixed(x, k); return (x.n < 0n ? '−' : '') + (x.n < 0n ? -x.n : x.n) + '/' + x.d; }
  function rs(x) { x = F(x); if (x.n < 0n) throw new Error('negative money'); if (x.int) return '₹' + ind(x.n); const k = dpOf(x); if (k === null || k > 2) throw new Error('money needs > 2 dp'); return '₹' + fixed(x, 2); }
  const rsS = x => (F(x).sign < 0 ? '−' : '') + rs(F(x).abs());                // signed money: −₹1,250
  const rsr = x => '₹' + fixed(x, 0).replace(/^−/, '−');                      // money rounded to the rupee (sign kept)
  const rs2 = x => '₹' + fixed(x, 2);                                         // money rounded to 2 dp
  const d2 = x => fixed(x, 2), d4 = x => fixed(x, 4);
  const pct = (x, dp) => (dp === undefined ? num(x) : fixed(x, dp)) + '%';
  const fr = x => { x = F(x); return x.int ? ind(x.n) : (x.n < 0n ? '−' : '') + (x.n < 0n ? -x.n : x.n) + '/' + x.d; };
  function ratio(parts) {                                                       // [Fx...] -> "3 : 2 : 1" (smallest integers)
    parts = parts.map(x => F(x)); let L = 1n; parts.forEach(p => { L = L / bg(L, p.d) * p.d; }); let ints = parts.map(p => p.n * (L / p.d)); let g = 0n; ints.forEach(i => { g = bg(g, i); });
    if (g === 0n) throw new Error('zero ratio'); ints = ints.map(i => i / g); if (ints.some(i => i <= 0n)) throw new Error('ratio sign'); return ints.map(i => i.toString()).join(' : ');
  }
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const FYM = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March'];   // offset 0 = April
  const fyDate = (fy, off, day = 1) => `${day} ${FYM[off]} ${off < 9 ? fy : fy + 1}`;    // 1st of month at offset off in FY starting April fy
  const dstr = dt => `${dt.getUTCDate()} ${MONTHS[dt.getUTCMonth()]} ${dt.getUTCFullYear()}`;
  const SUP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', '-': '⁻', '−': '⁻' };
  const sup = n => String(n).split('').map(c => SUP[c] || c).join('');
  function poly(cs, v = 'x') {                                                   // [a,b,c] -> "2x² − 3x + 1"
    const n = cs.length - 1; let s = '';
    cs.forEach((c, i) => { c = F(c); if (!c.n) return; const e = n - i, a = c.abs(), as = a.int ? (e && a.n === 1n ? '' : ind(a.n)) : `(${fr(a)})`;
      const body = as + (e ? v + (e > 1 ? sup(e) : '') : ''); s += s ? (c.n < 0n ? ' − ' : ' + ') + body : (c.n < 0n ? '−' : '') + body; });
    return s || '0';
  }
  const ap = (x, dp = 2) => (dpOf(x) !== null && dpOf(x) <= dp ? '= ' : '≈ ') + fixed(x, dp);   // '=' if exact, else '≈'
  const pf = x => { const s = fr(x); return s.includes('/') ? `(${s})` : s; };       // fraction in brackets inside an expression
  const ord = n => n + (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');
  const sgn = x => F(x).n < 0n ? '−' : '+';
  const pn = x => { const s = num(x); return s[0] === '−' ? `(${s})` : s; };

  /* ---------- names ---------- */
  const PEOPLE = ['Ramesh', 'Sunita', 'Imran', 'Harpreet', 'Gopal', 'Lata', 'Vikram', 'Ayesha', 'Joseph', 'Kavita', 'Naveen', 'Rekha', 'Suresh', 'Fatima', 'Anil', 'Deepa', 'Mahesh', 'Nisha', 'Rajiv', 'Usha', 'Tenzin', 'Meenakshi', 'Arvind', 'Shabnam'];
  const FIRMS = ['Shree Traders', 'Ganesh Agencies', 'Kaveri Textiles', 'Sai Electricals', 'Narmada Stores', 'Lotus Enterprises', 'Himalaya Distributors', 'Bharat Hardware', 'Coastal Spices', 'Green Valley Foods', 'Sunrise Pharma Distributors', 'Deccan Paper Mart'];
  const COS = ['Vardhan Ltd.', 'Saraswati Tools Ltd.', 'Konark Cements Ltd.', 'Indus Fabrics Ltd.', 'Pragati Motors Ltd.', 'Nilgiri Tea Ltd.', 'Tapti Chemicals Ltd.', 'Aravali Foods Ltd.'];
  const CLUBS = ['Rising Star Sports Club', 'Gyan Deep Library Society', 'Navjeevan Welfare Association', 'Lakeview Recreation Club', 'Sahyog Cultural Society'];
  const LET = ['A', 'B', 'C', 'D', 'P', 'Q', 'R', 'S', 'X', 'Y', 'M', 'N'];

  /* ---------- options: correct + 3 computed mistakes, all distinct ---------- */
  function perturb(c) {
    if (c instanceof Fx) {
      const k = dpOf(c), unit = k === null ? F(1, 100) : F(1, 10 ** Math.min(k, 4));
      const p = pick([F(9, 10), F(11, 10), F(19, 20), F(21, 20), F(4, 5), F(6, 5), F(49, 50), F(51, 50)]);
      let w = c.mul(p); w = k === null || k > 2 ? roundDp(w, 2) : roundDp(w, k); if (w.eq(c)) w = c.add(unit.mul(pick([1, 2, 3, -1, -2])));
      return w;
    }
    return null;
  }
  function build(correct, wrongs, fmt, o = {}) {
    const c = fmt(correct), seen = new Set([c]), out = [], ok = o.ok || (() => true);
    const add = w => { if (out.length >= 3 || w == null) return; let s; try { if (!ok(w)) return; s = fmt(w); } catch (e) { return; } if (s == null || s === '' || seen.has(s)) return; seen.add(s); out.push(s); };
    wrongs.forEach(add);
    for (let k = 0; out.length < 3 && k < 400; k++) add(o.more ? o.more(k) : perturb(correct));
    if (out.length < 3) throw new Error('not enough options');
    const all = shuffle([c, ...out]);
    return { options: all, answer: all.indexOf(c), ans: c };
  }
  const buildS = (correct, wrongs, more) => build(correct, wrongs, s => s, { more });   // string options
  /* safety net: any bare whole number of 4+ digits gets Indian commas (decimals and years after a month name untouched) */
  const fixN = s => String(s).replace(/(^|[\s(=:,×÷+[])-(?=\d)/g, '$1−').replace(/(?<![\d.,⁰¹²³⁴⁵⁶⁷⁸⁹])(?<!(?:January|February|March|April|May|June|July|August|September|October|November|December) )(\d{4,})(?![\d,])(?!-\d\d\b)/g, d => ind(BigInt(d)));
  const QI = (q, b, explain, steps, data, extra) => Object.assign({ kind: 'mcq', q: fixN(q), options: b.options.map(fixN), answer: b.answer, explain: fixN(explain), steps: [...steps, 'Answer: ' + b.ans].map(fixN), data }, extra || {});
  const poss = n => n + (/s$/.test(n) ? '’' : '’s');
  const PSETS = [['A', 'B', 'C', 'D'], ['P', 'Q', 'R', 'S'], ['X', 'Y', 'Z', 'W'], ['K', 'L', 'M', 'N']];
  const PL = (x, word) => `${x} ${word}${x === 1 ? '' : 's'}`;

  /* ---------- registry ---------- */
  const GENS = [];
  const U = s => 'fnd-' + s;
  function def(o) { o.unit = [].concat(o.unit); o.paper = o.unit[0].split('-')[1]; o.kinds = o.kinds || ['mcq']; GENS.push(o); }

  /* =====================================================================================
     PAPER 1 — ACCOUNTING
     ===================================================================================== */
  const DRCR = (dr, cr) => `${dr} Dr. To ${cr}`;
  const PorL = (x, p = 'Profit', l = 'Loss') => { x = F(x); if (x.sign === 0) throw new Error('nil'); return `${x.sign > 0 ? p : l} ${rs(x.abs())}`; };

  /* ---- Trade discount and cash discount ---- */
  def({ id: 'p1_trade_cash', unit: U('p1-ch02-u01'), name: 'Trade and cash discount', concept: 'Trade discount is never recorded; cash discount is',
    make(d) {
      const L = RS(20000, d === 'easy' ? 100000 : 600000, 1000), t = pick([5, 10, 15, 20, 25]), c = pick([1, 2, 3, 4, 5]), sup = pick(FIRMS), who = pick(PEOPLE);
      const td = F(L).mul(t).div(100), net = F(L).sub(td), disc = net.mul(c).div(100), paid = net.sub(disc), ask = pick(['paid', 'purch', 'disc']);
      const q = `${who} bought goods from ${sup} with a list price of ${rs(L)} at ${t}% trade discount and ${c}% cash discount, and paid at once. ` + { paid: 'What amount was paid?', purch: 'At what amount is the Purchases account debited?', disc: 'What amount is credited to Discount Received account?' }[ask];
      const corr = { paid, purch: net, disc }[ask];
      const wr = { paid: [F(L).mul(100 - t - c).div(100), F(L).mul(100 - c).div(100), net, F(L).sub(F(L).mul(c).div(100)).sub(td).add(disc)], purch: [F(L), paid, F(L).mul(100 - t - c).div(100)], disc: [F(L).mul(c).div(100), td, F(L).mul(t + c).div(100)] }[ask];
      const steps = [`Trade discount: ${rs(L)} × ${t}% = ${rs(td)}`, `Invoice value: ${rs(L)} − ${rs(td)} = ${rs(net)}`, `Cash discount: ${rs(net)} × ${c}% = ${rs(disc)}`];
      if (ask !== 'purch') steps.push(`Cash paid: ${rs(net)} − ${rs(disc)} = ${rs(paid)}`);
      steps.push({ paid: 'Purchases is recorded at the invoice value; discount received is credited separately', purch: 'Purchases A/c is debited with the invoice value (after trade discount, before cash discount)', disc: 'Only the cash discount is recorded, as Discount Received (a gain)' }[ask]);
      return QI(q, build(corr, wr, rs), 'Trade discount is deducted on the invoice itself and never enters the books. Cash discount is allowed for prompt payment on the invoice value and is recorded as discount received.', steps, { L, t, c, ask });
    } });

  /* ---- Golden rules: which entry? ---- */
  const TX = [
    ['start', (n, a) => `Started business with cash ${a}`, 'Cash A/c', 'Capital A/c', ['Capital A/c|Cash A/c', 'Cash A/c|Drawings A/c', 'Bank A/c|Capital A/c']],
    ['cashpur', (n, a) => `Bought goods for cash ${a}`, 'Purchases A/c', 'Cash A/c', ['Cash A/c|Purchases A/c', 'Goods A/c|Capital A/c', 'Purchases A/c|Sales A/c']],
    ['credpur', (n, a) => `Bought goods on credit from ${n} for ${a}`, 'Purchases A/c', '@ A/c', ['@ A/c|Purchases A/c', 'Purchases A/c|Cash A/c', '@ A/c|Sales A/c']],
    ['credsale', (n, a) => `Sold goods on credit to ${n} for ${a}`, '@ A/c', 'Sales A/c', ['Sales A/c|@ A/c', 'Cash A/c|Sales A/c', '@ A/c|Purchases A/c']],
    ['rent', (n, a) => `Paid office rent ${a} in cash`, 'Rent A/c', 'Cash A/c', ['Cash A/c|Rent A/c', 'Rent A/c|Capital A/c', 'Landlord A/c|Cash A/c']],
    ['comm', (n, a) => `Received commission ${a} in cash`, 'Cash A/c', 'Commission Received A/c', ['Commission Received A/c|Cash A/c', 'Cash A/c|Capital A/c', 'Cash A/c|Sales A/c']],
    ['furn', (n, a) => `Bought office furniture for ${a} and paid by cheque`, 'Furniture A/c', 'Bank A/c', ['Bank A/c|Furniture A/c', 'Purchases A/c|Bank A/c', 'Furniture A/c|Cash A/c']],
    ['draw', (n, a) => `The proprietor withdrew ${a} in cash for personal use`, 'Drawings A/c', 'Cash A/c', ['Cash A/c|Drawings A/c', 'Capital A/c|Drawings A/c', 'Expenses A/c|Cash A/c']],
    ['goodsdraw', (n, a) => `The proprietor took goods costing ${a} for personal use`, 'Drawings A/c', 'Purchases A/c', ['Drawings A/c|Sales A/c', 'Purchases A/c|Drawings A/c', 'Capital A/c|Cash A/c']],
    ['paycred', (n, a) => `Paid ${a} in cash to ${n}, a supplier, on account`, '@ A/c', 'Cash A/c', ['Cash A/c|@ A/c', 'Purchases A/c|Cash A/c', '@ A/c|Purchases A/c']],
    ['recdebt', (n, a) => `Received ${a} in cash from ${n}, a customer, on account`, 'Cash A/c', '@ A/c', ['@ A/c|Cash A/c', 'Cash A/c|Sales A/c', '@ A/c|Sales A/c']],
    ['deposit', (n, a) => `Deposited ${a} cash into the bank`, 'Bank A/c', 'Cash A/c', ['Cash A/c|Bank A/c', 'Bank A/c|Capital A/c', 'Deposit A/c|Cash A/c']],
    ['samples', (n, a) => `Goods costing ${a} were distributed as free samples`, 'Advertisement A/c', 'Purchases A/c', ['Purchases A/c|Advertisement A/c', 'Advertisement A/c|Sales A/c', 'Drawings A/c|Purchases A/c']],
    ['outsal', (n, a) => `Salary of ${a} for March is due but unpaid at the year end`, 'Salary A/c', 'Outstanding Salary A/c', ['Outstanding Salary A/c|Salary A/c', 'Salary A/c|Cash A/c', 'Salary A/c|Capital A/c']],
    ['dep', (n, a) => `Depreciation of ${a} is charged on machinery`, 'Depreciation A/c', 'Machinery A/c', ['Machinery A/c|Depreciation A/c', 'Depreciation A/c|Cash A/c', 'Profit and Loss A/c|Cash A/c']],
    ['retin', (n, a) => `${n}, a customer, returned goods of ${a}`, 'Sales Returns A/c', '@ A/c', ['@ A/c|Sales Returns A/c', 'Purchases Returns A/c|@ A/c', '@ A/c|Purchases Returns A/c']],
    ['retout', (n, a) => `Goods of ${a} were returned to ${n}, a supplier`, '@ A/c', 'Purchases Returns A/c', ['Purchases Returns A/c|@ A/c', 'Sales Returns A/c|@ A/c', '@ A/c|Sales Returns A/c']],
    ['baddebt', (n, a) => `${n}, a customer who owed ${a}, became insolvent and nothing could be recovered`, 'Bad Debts A/c', '@ A/c', ['@ A/c|Bad Debts A/c', 'Bad Debts A/c|Cash A/c', 'Capital A/c|@ A/c']],
    ['withdraw', (n, a) => `Withdrew ${a} from the bank for office use`, 'Cash A/c', 'Bank A/c', ['Bank A/c|Cash A/c', 'Drawings A/c|Bank A/c', 'Cash A/c|Capital A/c']],
    ['salpaid', (n, a) => `Paid salaries ${a} by cheque`, 'Salaries A/c', 'Bank A/c', ['Bank A/c|Salaries A/c', 'Salaries A/c|Cash A/c', 'Salaries A/c|Capital A/c']]
  ];
  def({ id: 'p1_golden', unit: U('p1-ch02-u01'), name: 'Golden rules — which entry?', concept: 'Golden rules of debit and credit',
    make() {
      const [key, txt, dr0, cr0, alts0] = pick(TX), n = pick(PEOPLE), a = RS(2000, 90000, 500), sub = t => t.replace(/@/g, n), dr = sub(dr0), cr = sub(cr0), alts = alts0.map(sub);
      const q = `Which journal entry records this transaction? “${txt(n, rs(a))}.”`;
      const b = buildS(DRCR(dr, cr), alts.map(s => DRCR(...s.split('|'))));
      const why = (ac, dr) => /^(Cash|Bank|Furniture|Machinery) A\/c$/.test(ac) ? `real account — the asset ${dr ? 'comes in' : 'goes out'}`
        : /^Purchases A\/c$/.test(ac) ? (dr ? 'goods come in' : 'goods go out of the business at cost') : /^Sales A\/c$/.test(ac) ? 'goods go out on sale' : /Sales Returns/.test(ac) ? 'goods come back from the customer' : /Purchases Returns/.test(ac) ? 'goods go back to the supplier'
        : /^Capital A\/c$/.test(ac) ? 'the proprietor is the giver' : /^Drawings A\/c$/.test(ac) ? 'the proprietor is the receiver' : /Outstanding/.test(ac) ? 'representative personal account — salary owed to employees'
        : /Commission Received/.test(ac) ? 'nominal account — an income' : /(Rent|Salary|Salaries|Depreciation|Advertisement|Bad Debts) A\/c/.test(ac) ? 'nominal account — an expense or loss' : `personal account — ${ac.replace(' A/c', '')} is the ${dr ? 'receiver' : 'giver'}`;
      const steps = [`Accounts affected: ${dr} and ${cr}`, `${dr}: ${why(dr, true)} → debit`, `${cr}: ${why(cr, false)} → credit`];
      return QI(q, b, 'Personal: debit the receiver, credit the giver. Real: debit what comes in, credit what goes out. Nominal: debit expenses and losses, credit incomes and gains. Goods taken out at cost reduce Purchases.', steps, { key, n, a });
    } });

  /* ---- Classification of accounts ---- */
  const ACL = [['Ramesh (a customer)', 'Natural personal'], ['Kavita (a supplier)', 'Natural personal'], ['State Bank of India', 'Artificial personal'], ['Konark Cements Ltd. (a supplier)', 'Artificial personal'], ['Lions Club (a member organisation)', 'Artificial personal'],
    ['Outstanding Salary', 'Representative personal'], ['Prepaid Insurance', 'Representative personal'], ['Accrued Interest', 'Representative personal'], ['Rent Received in Advance', 'Representative personal'],
    ['Machinery', 'Real'], ['Cash', 'Real'], ['Goodwill', 'Real'], ['Land and Building', 'Real'], ['Patents', 'Real'], ['Furniture', 'Real'],
    ['Rent Paid', 'Nominal'], ['Salaries', 'Nominal'], ['Commission Received', 'Nominal'], ['Discount Allowed', 'Nominal'], ['Interest Received', 'Nominal'], ['Depreciation', 'Nominal']];
  const ACLS = ['Natural personal', 'Artificial personal', 'Representative personal', 'Real', 'Nominal'];
  def({ id: 'p1_acc_class', unit: U('p1-ch02-u01'), name: 'Classification of accounts', concept: 'Types of accounts',
    make() {
      const [ac, cls] = pick(ACL), q = `Under the traditional classification, the “${ac.replace(/ \(.*\)/, '')}” account${/\(/.test(ac) ? ' ' + ac.match(/\(.*\)/)[0] : ''} is a:`;
      const b = buildS(cls + ' account', ACLS.filter(x => x !== cls).map(x => x + ' account'));
      const why = { 'Natural personal': 'a human being', 'Artificial personal': 'a body created by law or an organisation', 'Representative personal': 'an amount due to or from persons for an expense or income', Real: 'an asset or property', Nominal: 'an expense, loss, income or gain' }[cls];
      return QI(q, b, 'Personal accounts relate to persons (natural, artificial, or representative of persons). Real accounts relate to assets. Nominal accounts relate to expenses, losses, incomes and gains.', [`The account represents ${why}`, `So it is classified as ${cls.toLowerCase()}`], { ac, cls });
    } });

  /* ---- GST on a sale ---- */
  def({ id: 'p1_gst_sale', unit: U('p1-ch02-u01'), name: 'GST on sales and purchases', concept: 'Input and output GST (CGST/SGST/IGST)',
    make(d) {
      const V = RS(10000, d === 'easy' ? 100000 : 400000, 1000), t = pick([0, 0, 5, 10, 20]), g = pick([5, 12, 18]), intra = chance(.5), buy = chance(.35), cust = pick(FIRMS);
      const taxable = F(V).mul(100 - t).div(100), gst = taxable.mul(g).div(100), total = taxable.add(gst);
      const ask = intra ? pick(['total', 'cgst']) : pick(['total', 'igst']);
      const tdTxt = t ? ` at ${t}% trade discount` : '';
      const q = buy ? `Goods with a list price of ${rs(V)} were bought on credit from ${cust}${tdTxt}. ${intra ? `CGST and SGST were charged @ ${g / 2}% each` : `IGST was charged @ ${g}%`}. ` + (ask === 'total' ? `At what amount is ${poss(cust)} account credited?` : `What amount is debited to Input ${ask.toUpperCase()} account?`)
        : `Goods with a list price of ${rs(V)} were sold on credit to ${cust}${tdTxt}, charging ${intra ? `CGST and SGST @ ${g / 2}% each` : `IGST @ ${g}%`}. ` + (ask === 'total' ? `At what amount is ${poss(cust)} account debited?` : `What amount is credited to Output ${ask.toUpperCase()} account?`);
      const corr = ask === 'total' ? total : ask === 'cgst' ? gst.div(2) : gst;
      const wr = ask === 'total' ? [F(V).add(F(V).mul(g).div(100)), taxable.add(gst.div(2)), taxable, F(V).mul(100 - t + g).div(100)] : ask === 'cgst' ? [gst, F(V).mul(g).div(200), F(V).mul(g).div(100)] : [gst.div(2), F(V).mul(g).div(100), total];
      const steps = [];
      if (t) steps.push(`Taxable value: ${rs(V)} − ${t}% trade discount = ${rs(V)} × ${100 - t}% = ${rs(taxable)}`); else steps.push(`Taxable value = ${rs(taxable)}`);
      steps.push(intra ? `CGST = SGST = ${rs(taxable)} × ${g / 2}% = ${rs(gst.div(2))}` : `IGST = ${rs(taxable)} × ${g}% = ${rs(gst)}`);
      if (ask === 'total') steps.push(`${buy ? 'Supplier credited' : 'Customer debited'}: ${rs(taxable)} + ${rs(gst)} = ${rs(total)}`);
      return QI(q, build(corr, wr, rs), 'GST is charged on the value after trade discount. Intra-state supplies attract CGST + SGST (each half of the rate); inter-state supplies attract IGST (the full rate). The party is debited/credited with value plus tax.', steps, { V, t, g, intra, buy, ask });
    } });

  /* ---- GST set-off: net payable in cash ---- */
  function gstSet(CC, SC, IC, OC, OS, OI) {      // all Fx; returns {cash, lines[]}
    const z = F(0), mx = (a, b) => a.gt(b) ? a : b, lines = [];
    const needC = mx(OC.sub(CC), z), needS = mx(OS.sub(SC), z), exC = mx(CC.sub(OC), z), exS = mx(SC.sub(OS), z);
    let cash;
    if (!IC.lt(OI)) {
      const g = IC.sub(OI); lines.push(`IGST credit first against IGST: balance IGST credit = ${rs(IC)} − ${rs(OI)} = ${rs(g)}`);
      lines.push(`CGST still payable after CGST credit = ${rs(needC)}; SGST still payable after SGST credit = ${rs(needS)}`);
      cash = mx(needC.add(needS).sub(g), z);
      lines.push(cash.sign ? `Balance IGST credit used against CGST/SGST: ${rs(needC)} + ${rs(needS)} − ${rs(g)} = ${rs(cash)}` : `Balance IGST credit ${rs(g)} covers the CGST/SGST still payable, so nothing is paid in cash`);
    } else {
      const L = OI.sub(IC); lines.push(`IGST payable after IGST credit: ${rs(OI)} − ${rs(IC)} = ${rs(L)}`);
      lines.push(`Excess CGST credit = ${rs(exC)} and excess SGST credit = ${rs(exS)} can be used against IGST (never CGST for SGST or SGST for CGST)`);
      const li = mx(L.sub(exC).sub(exS), z); cash = li.add(needC).add(needS);
      lines.push(`Cash: IGST ${rs(li)} + CGST ${rs(needC)} + SGST ${rs(needS)} = ${rs(cash)}`);
    }
    return { cash, lines };
  }
  def({ id: 'p1_gst_setoff', unit: U('p1-ch02-u01'), name: 'GST set-off (input tax credit)', concept: 'Utilisation of input tax credit',
    make(d) {
      const g = pick([12, 18]), Pi = RS(10000, 400000, 10000), Pe = RS(10000, 300000, 10000), Si = RS(10000, 600000, 10000), Se = RS(10000, 500000, 10000);
      if (Pi + Pe === 0 || Si + Se === 0) throw new Error('retry');
      const CC = F(Pi).mul(g).div(200), SC = CC, IC = F(Pe).mul(g).div(100), OC = F(Si).mul(g).div(200), OS = OC, OI = F(Se).mul(g).div(100);
      const r = gstSet(CC, SC, IC, OC, OS, OI);
      const q = `During a month a dealer made intra-state purchases of ${rs(Pi)} and inter-state purchases of ${rs(Pe)}, and intra-state sales of ${rs(Si)} and inter-state sales of ${rs(Se)} (all values before GST). GST rate is ${g}% (CGST ${g / 2}% + SGST ${g / 2}% intra-state, IGST ${g}% inter-state). Using the input tax credit as permitted, what GST is payable in cash?`;
      const naive = OC.add(OS).add(OI).sub(CC).sub(SC).sub(IC);
      const wr = [naive.sign >= 0 ? naive : null, OC.add(OS).add(OI), OI.sub(IC).abs(), OC.add(OS).sub(CC).sub(SC).abs(), r.cash.add(IC)];
      const steps = [`Output tax: CGST ${rs(OC)}, SGST ${rs(OS)}, IGST ${rs(OI)}`, `Input credit: CGST ${rs(CC)}, SGST ${rs(SC)}, IGST ${rs(IC)}`, ...r.lines];
      return QI(q, build(r.cash, wr, rs), 'IGST credit is used first against IGST and then against CGST/SGST. CGST credit goes against CGST and then IGST; SGST credit against SGST and then IGST. CGST credit can never pay SGST or vice versa.', steps, { g, Pi, Pe, Si, Se });
    } });

  /* ---- Ledger balance ---- */
  def({ id: 'p1_ledger_bal', unit: U('p1-ch02-u02'), name: 'Balancing a ledger account', concept: 'Balancing personal accounts',
    make(d) {
      const debtor = chance(.5), n = pick(FIRMS), O = RS(5000, 80000, 500), s1 = RS(10000, 120000, 500), s2 = RS(5000, 90000, 500), dsc = RS(100, 2000, 50), rt = RS(500, 8000, 100);
      const r = RS(5000, Math.max(5000, O + s1 - rt - dsc - 1000), 500);
      const bal = O + s1 + s2 - r - dsc - rt; if (bal <= 0) throw new Error('retry');
      const side = debtor ? 'Dr' : 'Cr', oth = debtor ? 'Cr' : 'Dr';
      const q = debtor ? `${n} (a customer) owed ${rs(O)} on 1 April. During April: credit sales to ${n} ${rs(s1)} and ${rs(s2)}; goods returned by ${n} ${rs(rt)}; cash received from ${n} ${rs(r)} and discount allowed ${rs(dsc)}. What is the balance of ${poss(n)} account on 30 April?`
        : `${n} (a supplier) was owed ${rs(O)} on 1 April. During April: credit purchases from ${n} ${rs(s1)} and ${rs(s2)}; goods returned to ${n} ${rs(rt)}; cash paid to ${n} ${rs(r)} and discount received ${rs(dsc)}. What is the balance of ${poss(n)} account on 30 April?`;
      const f = ([v, s]) => `${rs(v)} ${s} balance`;
      const b = build([bal, side], [[bal, oth], [bal + dsc, side], [bal + 2 * rt, side], [bal - O, side], [bal + dsc + rt, side]], f, { ok: x => x[0] > 0 });
      const steps = [`${debtor ? 'Debit' : 'Credit'} side: ${rs(O)} + ${rs(s1)} + ${rs(s2)} = ${rs(O + s1 + s2)}`, `${debtor ? 'Credit' : 'Debit'} side: ${rs(r)} + ${rs(dsc)} + ${rs(rt)} = ${rs(r + dsc + rt)}`, `Balance: ${rs(O + s1 + s2)} − ${rs(r + dsc + rt)} = ${rs(bal)} (${debtor ? 'debit' : 'credit'} side is bigger)`];
      return QI(q, b, `A ${debtor ? 'customer' : 'supplier'}'s account is ${debtor ? 'debited' : 'credited'} with the opening balance and ${debtor ? 'sales' : 'purchases'}, and ${debtor ? 'credited' : 'debited'} with cash, discount and returns. The bigger side gives the balance.`, steps, { debtor, O, s1, s2, r, dsc, rt });
    } });

  /* ---- Trial balance: capital as balancing figure ---- */
  const TBDR = ['Cash in hand', 'Bank balance', 'Trade receivables', 'Opening inventory', 'Purchases', 'Wages', 'Rent', 'Salaries', 'Drawings', 'Furniture', 'Machinery', 'Sales returns', 'Discount allowed', 'Carriage inwards'];
  const TBCR = ['Sales', 'Trade payables', 'Bank loan', 'Commission received', 'Purchases returns', 'Discount received', 'Bills payable'];
  def({ id: 'p1_tb_capital', unit: U('p1-ch02-u03'), name: 'Trial balance — find the missing capital', concept: 'Debit and credit balances',
    make(d) {
      const nd = d === 'easy' ? 6 : 8, nc = d === 'easy' ? 3 : 4;
      const drs = sample(TBDR.filter(x => x !== 'Purchases' && x !== 'Drawings'), nd - 2).concat(['Purchases', 'Drawings']), crs = sample(TBCR.filter(x => x !== 'Sales'), nc - 1).concat(['Sales']);
      const val = a => ({ Purchases: RS(200000, 600000, 1000), Sales: RS(300000, 900000, 1000), Drawings: RS(10000, 60000, 1000), Machinery: RS(100000, 400000, 1000), Furniture: RS(20000, 120000, 1000), 'Opening inventory': RS(30000, 150000, 1000), 'Trade receivables': RS(40000, 200000, 1000), 'Bank loan': RS(50000, 200000, 1000), 'Trade payables': RS(30000, 150000, 1000) }[a] || RS(2000, 60000, 500));
      const items = [...drs.map(a => [a, val(a), 'Dr']), ...crs.map(a => [a, val(a), 'Cr'])];
      const D = items.filter(x => x[2] === 'Dr').reduce((s, x) => s + x[1], 0), C = items.filter(x => x[2] === 'Cr').reduce((s, x) => s + x[1], 0), cap = D - C;
      if (cap < 20000) throw new Error('retry');
      const sh = shuffle(items), dw = items.find(x => x[0] === 'Drawings')[1], sr = items.find(x => x[0] === 'Sales returns'), pr = items.find(x => x[0] === 'Purchases returns');
      const q = `From these balances, find the capital (the balancing figure of the trial balance): ${sh.map(x => `${x[0]} ${rs(x[1])}`).join('; ')}.`;
      const wr = [cap - 2 * dw, sr ? cap - 2 * sr[1] : null, pr ? cap + 2 * pr[1] : null, D, cap + dw];
      const steps = [`Debit balances (assets, expenses, losses, drawings): ${items.filter(x => x[2] === 'Dr').map(x => rs(x[1])).join(' + ')} = ${rs(D)}`, `Credit balances (liabilities, incomes, gains) other than capital: ${items.filter(x => x[2] === 'Cr').map(x => rs(x[1])).join(' + ')} = ${rs(C)}`, `Capital: ${rs(D)} − ${rs(C)} = ${rs(cap)}`];
      return QI(q, build(cap, wr, rs, { ok: x => x > 0 }), 'Assets, expenses, losses, drawings and sales returns have debit balances; liabilities, capital, incomes, gains and purchases returns have credit balances. Capital is the figure that makes both sides equal.', steps, { items });
    } });

  /* ---- Suspense account from errors ---- */
  const ERRS = [
    ['sales_under', x => `The Sales Day Book was undercast by ${rs(x)}`, x => x],
    ['sales_over', x => `The Sales Day Book was overcast by ${rs(x)}`, x => -x],
    ['purch_over', x => `The Purchases Day Book was overcast by ${rs(x)}`, x => x],
    ['purch_under', x => `The Purchases Day Book was undercast by ${rs(x)}`, x => -x],
    ['disc_wrong_side', x => `Discount allowed of ${rs(x)} was posted to the credit side of Discount Account`, x => -2 * x],
    ['receipt_not_posted', x => `Cash of ${rs(x)} received from a customer was not posted to the customer's account`, x => x],
    ['payment_not_posted', x => `Cash of ${rs(x)} paid to a supplier was not posted to the supplier's account`, x => -x],
    ['two_sided', x => `Furniture bought for ${rs(x)} was debited to Purchases Account`, x => 0],
    ['wrong_ac_same_side', x => `Sales returns of ${rs(x)} were debited to Purchases Returns Account`, x => 0],
    ['omitted', x => `A credit purchase of ${rs(x)} was completely omitted from the books`, x => 0]
  ];
  def({ id: 'p1_suspense', unit: U('p1-ch02-u06'), name: 'Suspense account', concept: 'One-sided errors and the suspense account',
    make(d) {
      const k = d === 'easy' ? 3 : 4, errs = sample(ERRS, k).map(e => [e, RS(200, 9000, 50)]);
      const pre = errs.reduce((s, [e, x]) => s + e[2](x), 0);       // (Dr total − Cr total) caused by the errors
      if (pre === 0 || errs.filter(([e]) => e[2](1) !== 0).length < 2) throw new Error('retry');
      const side = pre > 0 ? 'Cr' : 'Dr', amt = Math.abs(pre);
      const q = `The trial balance did not agree and the difference was put to a Suspense Account. Later these errors (the only ones) were found: ${errs.map(([e, x], i) => `(${i + 1}) ${e[1](x)}`).join('; ')}. What balance did the Suspense Account show in the trial balance?`;
      const f = ([v, s]) => `${rs(v)} ${s}`;
      const nod = errs.reduce((s, [e, x]) => s + Math.sign(e[2](1)) * x, 0), absSum = errs.reduce((s, [e, x]) => s + Math.abs(e[2](x)), 0), all = errs.reduce((s, [e, x]) => s + (e[2](1) === 0 ? x : 0), 0);
      const b = build([amt, side], [[amt, side === 'Cr' ? 'Dr' : 'Cr'], [Math.abs(nod), side], [absSum, side], [amt + all, side]], f, { ok: x => x[0] > 0 });
      const steps = errs.map(([e, x], i) => { const v = e[2](x); return `Error ${i + 1}: ${v === 0 ? 'both sides affected equally — no effect on the trial balance' : `debit total ${v > 0 ? 'more' : 'less'} than credit total by ${rs(Math.abs(v))}`}`; });
      steps.push(`Net: debit side ${pre > 0 ? 'exceeds' : 'falls short of'} credit side by ${rs(amt)}, so Suspense shows a ${side === 'Cr' ? 'credit' : 'debit'} balance of ${rs(amt)}`);
      return QI(q, b, 'Only one-sided errors (casting, posting to one account, posting to the wrong side) disturb the trial balance. Errors of principle, omission or posting to the wrong account on the correct side do not. Posting to the wrong side doubles the effect.', steps, { errs: errs.map(([e, x]) => [e[0], x]) });
    } });

  /* ---- Effect of rectification on profit ---- */
  const PERR = [
    ['cap_to_rev', x => `Machinery bought for ${rs(x)} was debited to Purchases Account`, 1],
    ['rev_to_cap', x => `Repairs to machinery of ${rs(x)} were debited to Machinery Account`, -1],
    ['sales_under', x => `The Sales Day Book was undercast by ${rs(x)}`, 1],
    ['purch_under', x => `The Purchases Day Book was undercast by ${rs(x)}`, -1],
    ['out_omitted', x => `Rent outstanding of ${rs(x)} was not recorded`, -1],
    ['comm_personal', x => `Commission received of ${rs(x)} was credited to the payer's personal account`, 1],
    ['draw_as_exp', x => `The proprietor's household rent of ${rs(x)} was debited to Rent Account`, 1],
    ['asset_to_sales', x => `Old furniture sold at its book value of ${rs(x)} was credited to Sales Account`, -1],
    ['stock_under', x => `Closing inventory was undervalued by ${rs(x)}`, 1],
    ['wages_building', x => `Wages of ${rs(x)} paid for constructing the office building were debited to Wages Account`, 1]
  ];
  def({ id: 'p1_rectify_profit', unit: U('p1-ch02-u06'), name: 'Rectification — corrected profit', concept: 'Effect of errors on profit',
    make(d) {
      const P = RS(80000, 500000, 1000), errs = sample(PERR, d === 'easy' ? 2 : 3).map(e => [e, RS(1000, 30000, 500)]);
      const adj = errs.reduce((s, [e, x]) => s + e[2] * x, 0), cp = P + adj; if (cp <= 0) throw new Error('retry');
      const q = `The net profit of a business for the year was ${rs(P)} before these errors were found: ${errs.map(([e, x], i) => `(${i + 1}) ${e[1](x)}`).join('; ')}. Ignore depreciation. What is the corrected net profit?`;
      const rev = P - adj, oneOff = P + adj - 2 * errs[0][0][2] * errs[0][1];
      const steps = errs.map(([e, x], i) => `Error ${i + 1}: profit ${e[2] > 0 ? 'understated' : 'overstated'} → ${e[2] > 0 ? 'add' : 'deduct'} ${rs(x)}`);
      steps.push(`Corrected profit: ${rs(P)} ${errs.map(([e, x]) => `${e[2] > 0 ? '+' : '−'} ${rs(x)}`).join(' ')} = ${rs(cp)}`);
      return QI(q, build(cp, [rev, oneOff, P, P + errs.reduce((s, [e, x]) => s + x, 0)], rs, { ok: x => x > 0 }), 'Capital items charged to revenue understate profit; revenue items capitalised overstate it. Undercast incomes or unrecorded closing inventory understate profit; unrecorded expenses overstate it.', steps, { P, errs: errs.map(([e, x]) => [e[0], x]) });
    } });

  /* ---- Cash book (two-column) ---- */
  def({ id: 'p1_cashbook', unit: U('p1-ch02-u05'), name: 'Cash book balances', concept: 'Contra entries in a two-column cash book',
    make(d) {
      const C0 = RS(5000, 40000, 500), B0 = RS(20000, 200000, 1000), t = { cs: RS(5000, 60000, 500), dep: RS(5000, 40000, 500), chq: RS(5000, 80000, 500), pay: RS(5000, 90000, 500), wd: RS(2000, 30000, 500), cp: RS(2000, 20000, 500), sal: RS(3000, 25000, 500) };
      const cash = C0 + t.cs - t.dep + t.wd - t.cp - t.sal, bank = B0 + t.dep + t.chq - t.pay - t.wd;
      if (cash <= 0 || bank <= 0) throw new Error('retry');
      const ask = pick(['cash', 'bank']);
      const q = `Opening balances: cash ${rs(C0)}, bank ${rs(B0)}. Transactions: cash sales ${rs(t.cs)}; cash deposited into bank ${rs(t.dep)}; cheque received from a customer and deposited the same day ${rs(t.chq)}; paid a supplier by cheque ${rs(t.pay)}; withdrew ${rs(t.wd)} from the bank for office use; cash purchases ${rs(t.cp)}; salaries paid in cash ${rs(t.sal)}. What is the closing ${ask} balance in the two-column cash book?`;
      const corr = ask === 'cash' ? cash : bank;
      const wr = ask === 'cash' ? [cash + 2 * t.dep, cash - 2 * t.wd, C0 + t.cs - t.cp - t.sal, cash + t.chq] : [bank - 2 * t.dep, bank + 2 * t.wd, B0 + t.chq - t.pay, bank - t.chq];
      const steps = ask === 'cash' ? [`Cash receipts: ${rs(C0)} + ${rs(t.cs)} + ${rs(t.wd)} = ${rs(C0 + t.cs + t.wd)}`, `Cash payments: ${rs(t.dep)} + ${rs(t.cp)} + ${rs(t.sal)} = ${rs(t.dep + t.cp + t.sal)}`, `Closing cash: ${rs(C0 + t.cs + t.wd)} − ${rs(t.dep + t.cp + t.sal)} = ${rs(cash)}`]
        : [`Bank receipts: ${rs(B0)} + ${rs(t.dep)} + ${rs(t.chq)} = ${rs(B0 + t.dep + t.chq)}`, `Bank payments: ${rs(t.pay)} + ${rs(t.wd)} = ${rs(t.pay + t.wd)}`, `Closing bank: ${rs(B0 + t.dep + t.chq)} − ${rs(t.pay + t.wd)} = ${rs(bank)}`];
      steps.splice(2, 0, 'Contra entries (C): cash deposited is a cash payment and a bank receipt; cash withdrawn for office is a bank payment and a cash receipt');
      return QI(q, build(corr, wr, rs, { ok: x => x > 0 }), 'In a two-column cash book, a deposit of cash into the bank and a withdrawal for office use are contra entries recorded on both sides. A cheque deposited the same day goes straight to the bank column.', steps, { C0, B0, t, ask });
    } });

  /* ---- Subsidiary books: purchases / sales book total ---- */
  def({ id: 'p1_daybook', unit: U('p1-ch02-u04'), name: 'Purchases / sales book total', concept: 'What goes into the purchases and sales books',
    make(d) {
      const sales = chance(.5), ns = sample(FIRMS, 4), L1 = RS(10000, 90000, 1000), t1 = pick([5, 10, 20]), L2 = RS(5000, 60000, 500), L3 = RS(10000, 80000, 1000), t3 = pick([5, 10, 15]), cash = RS(5000, 40000, 500), asset = RS(10000, 90000, 1000);
      const v1 = F(L1).mul(100 - t1).div(100), v3 = F(L3).mul(100 - t3).div(100), tot = v1.add(L2).add(v3);
      const verb = sales ? 'Sold goods on credit to' : 'Bought goods on credit from', book = sales ? 'Sales Book' : 'Purchases Book';
      const q = `Transactions for May: (1) ${verb} ${ns[0]}, list price ${rs(L1)}, trade discount ${t1}%; (2) ${verb} ${ns[1]} ${rs(L2)}; (3) ${sales ? 'Cash sales' : 'Cash purchases'} ${rs(cash)}; (4) ${sales ? `Sold old office furniture on credit to ${ns[2]}` : `Bought office furniture on credit from ${ns[2]}`} ${rs(asset)}; (5) ${verb} ${ns[3]}, list price ${rs(L3)}, trade discount ${t3}%. What is the total of the ${book} for May?`;
      const wr = [tot.add(cash), tot.add(asset), F(L1 + L2 + L3), tot.add(cash).add(asset)];
      const steps = [`(1) ${rs(L1)} × ${100 - t1}% = ${rs(v1)}`, `(5) ${rs(L3)} × ${100 - t3}% = ${rs(v3)}`, `(3) is a cash transaction (cash book); (4) is not goods traded (journal proper)`, `${book} total: ${rs(v1)} + ${rs(L2)} + ${rs(v3)} = ${rs(tot)}`];
      return QI(q, build(tot, wr, rs), `Only credit ${sales ? 'sales' : 'purchases'} of goods dealt in, at invoice value net of trade discount, go into the ${book}. Cash transactions go to the cash book and credit transactions in assets go to the journal proper.`, steps, { sales, L1, t1, L2, L3, t3, cash, asset });
    } });

  /* ---- Bank reconciliation statement ---- */
  function brsData(d) {
    const fav = chance(.6), B = RS(10000, 250000, 100);
    const pool = ['cni', 'cnc', 'bc', 'int', 'dd', 'dc'], k = d === 'easy' ? 3 : d === 'ICAI' ? 6 : R(4, 5), keys = sample(pool, k);
    const it = {}; keys.forEach(x => { it[x] = { cni: RS(2000, 60000, 50), cnc: RS(2000, 60000, 50), bc: RS(50, 1500, 10), int: RS(100, 5000, 10), dd: RS(500, 15000, 50), dc: RS(1000, 40000, 50) }[x]; });
    return { fav, B, it, dir: chance(.75) ? 'cb2pb' : 'pb2cb' };
  }
  // effect on the PASS BOOK balance (favourable = +) relative to the cash book balance
  const BRS_EFF = { cni: 1, cnc: -1, bc: -1, int: 1, dd: -1, dc: 1 };
  function brsText(k, v, fav) {
    return { cni: `cheques of ${rs(v)} issued to suppliers were not presented for payment`, cnc: `cheques of ${rs(v)} deposited were not yet credited by the bank`, bc: `bank charges of ${rs(v)} were debited in the pass book only`,
      int: fav ? `interest of ${rs(v)} was credited by the bank in the pass book only` : `interest on overdraft of ${rs(v)} was debited in the pass book only`, dd: `an insurance premium of ${rs(v)} paid by the bank under standing instructions was not recorded in the cash book`, dc: `a customer paid ${rs(v)} directly into the bank account, not recorded in the cash book` }[k];
  }
  const brsEff = (k, fav) => k === 'int' && !fav ? -1 : BRS_EFF[k];
  const fo = v => { v = F(v); if (!v.sign) throw new Error('nil'); return `${rs(v.abs())} ${v.sign > 0 ? 'favourable' : 'overdraft'}`; };
  def({ id: 'p1_brs', unit: U('p1-ch03-u01'), name: 'Bank reconciliation — balance as per the other book', concept: 'Reconciling cash book and pass book',
    kinds: ['mcq', 'desc'],
    make(d) {
      const { fav, B, it, dir } = brsData(d), keys = Object.keys(it);
      const start = fav ? B : -B, delta = keys.reduce((s, k) => s + brsEff(k, fav) * it[k], 0) * (dir === 'cb2pb' ? 1 : -1), res = start + delta;
      if (res === 0) throw new Error('nil');
      const from = dir === 'cb2pb' ? 'Cash Book (bank column)' : 'Pass Book', to = dir === 'cb2pb' ? 'Pass Book' : 'Cash Book';
      const q = `On 31 March 2026 the balance as per ${from} was ${rs(B)} ${fav ? 'favourable' : 'overdraft'}. On checking: ${keys.map(k => brsText(k, it[k], fav)).join('; ')}. What is the balance as per ${to}?`;
      const flip = start - delta, raw = (fav ? B : B) + Math.abs(delta) * Math.sign(delta), oneWrong = res - 2 * (dir === 'cb2pb' ? 1 : -1) * brsEff(keys[0], fav) * it[keys[0]];
      const b = build(res, [-res, flip, raw, oneWrong, -flip], fo, { ok: x => x !== 0 });
      const steps = [`Start: ${rs(B)} ${fav ? 'favourable' : 'overdraft'} as per ${from} (treat overdraft as negative)`];
      keys.forEach(k => { const e = brsEff(k, fav) * (dir === 'cb2pb' ? 1 : -1); steps.push(`${{ cni: 'Cheques issued, not presented', cnc: 'Cheques deposited, not credited', bc: 'Bank charges', int: fav ? 'Interest credited' : 'Interest on overdraft', dd: 'Direct payment by bank', dc: 'Direct deposit by customer' }[k]}: ${e > 0 ? 'add' : 'less'} ${rs(it[k])}`); });
      steps.push(`Net: ${fav ? '' : '−'}${ind(B)} ${keys.map(k => { const e = brsEff(k, fav) * (dir === 'cb2pb' ? 1 : -1); return `${e > 0 ? '+' : '−'} ${ind(it[k])}`; }).join(' ')} = ${res < 0 ? '−' : ''}${ind(Math.abs(res))}`);
      return QI(q, b, 'Ask, for each item, whether the bank has recorded it but the cash book has not (or vice versa), and how it changes the balance. A positive answer is a favourable balance; a negative answer is an overdraft.', steps, { fav, B, it, dir });
    },
    desc(d) {
      const { fav, B, it } = brsData(d === 'easy' ? 'moderate' : d), keys = Object.keys(it);
      // ICAI style: start from cash book; for an overdraft start, items increasing the overdraft are ADDED
      const sgnFor = k => fav ? brsEff(k, true) : -brsEff(k, false);
      const adds = keys.filter(k => sgnFor(k) > 0), less = keys.filter(k => sgnFor(k) < 0);
      const res = B + adds.reduce((s, k) => s + it[k], 0) - less.reduce((s, k) => s + it[k], 0);
      if (res === 0) throw new Error('nil');
      const lab = { cni: 'Cheques issued but not presented', cnc: 'Cheques deposited but not credited', bc: 'Bank charges debited by bank', int: fav ? 'Interest credited by bank' : 'Interest on overdraft debited by bank', dd: 'Insurance premium paid by bank (standing instruction)', dc: 'Direct deposit by customer' };
      const endLab = fav ? (res > 0 ? 'Balance as per Pass Book (favourable)' : 'Overdraft as per Pass Book') : (res > 0 ? 'Overdraft as per Pass Book' : 'Balance as per Pass Book (favourable)');
      const rows = [[fav ? 'Balance as per Cash Book (debit)' : 'Overdraft as per Cash Book (credit)', '', ind(B)]];
      if (adds.length) { rows.push(['Add:', '', '']); adds.forEach(k => rows.push([lab[k], ind(it[k]), ''])); rows.push(['', '', ind(adds.reduce((s, k) => s + it[k], 0))]); }
      if (less.length) { rows.push(['Less:', '', '']); less.forEach(k => rows.push([lab[k], ind(it[k]), ''])); rows.push(['', '', '(' + ind(less.reduce((s, k) => s + it[k], 0)) + ')']); }
      rows.push([endLab, '', ind(Math.abs(res))]);
      const scheme = keys.map((k, i) => ({ id: 's' + (i + 1), pt: `${lab[k]} — ${sgnFor(k) > 0 ? 'added' : 'deducted'} correctly (${rs(it[k])})`, m: 1, skill: 'application' }));
      scheme.push({ id: 's' + (keys.length + 1), pt: `Final balance ${rs(Math.abs(res))} with the correct nature (${endLab.toLowerCase()})`, m: 1, skill: 'computation' });
      scheme.push({ id: 's' + (keys.length + 2), pt: 'Proper format: heading with date, starting balance, Add/Less groups', m: 1, skill: 'presentation' });
      const marks = keys.length + 2, fs = FIRMS[R(0, FIRMS.length - 1)];
      const q = `Prepare a Bank Reconciliation Statement of ${fs} as on 31 March 2026. The Cash Book (bank column) showed ${fav ? 'a debit balance' : 'an overdraft (credit balance)'} of ${rs(B)}. ${keys.map(k => brsText(k, it[k], fav)).map(s => s[0].toUpperCase() + s.slice(1)).join('. ')}.`;
      const steps = [`Start with the cash book ${fav ? 'balance' : 'overdraft'} ${rs(B)}`, ...keys.map(k => `${lab[k]}: ${sgnFor(k) > 0 ? 'add' : 'less'} ${rs(it[k])}`), `${ind(B)} ${keys.map(k => `${sgnFor(k) > 0 ? '+' : '−'} ${ind(it[k])}`).join(' ')} = ${res < 0 ? '−' : ''}${ind(Math.abs(res))}`];
      return { kind: 'desc', marks, minutes: Math.round(marks * 1.8), pad: 'table', q: fixN(q), given: [], model: [{ t: 'table', head: ['Particulars', '₹', '₹'], rows, num: [1, 2] }, { t: 'note', text: fav ? 'A negative result would mean the pass book shows an overdraft.' : 'When starting from an overdraft, items that increase the overdraft are added and items that reduce it are deducted.' }],
        scheme, steps: steps.map(fixN), answer: endLab + ' ' + rs(Math.abs(res)), data: { fav, B, it } };
    } });

  /* ---- Inventory: FIFO and weighted average (periodic) ---- */
  function lots(d) {
    const n = d === 'easy' ? 2 : 3, L = [[RS(100, 600, 10), R(20, 60)]]; let p = L[0][1];
    for (let i = 0; i < n; i++) { p += R(-3, 8); if (p < 10) p = 10; L.push([RS(100, 800, 10), p]); }
    return L;   // [units, rate]; first = opening inventory
  }
  def({ id: 'p1_fifo', unit: U('p1-ch04-u01'), name: 'Closing inventory — FIFO', concept: 'FIFO cost formula',
    make(d) {
      const L = lots(d), tot = L.reduce((s, x) => s + x[0], 0), K = RS(50, tot - 50, 10), S = tot - K; if (K <= 0) throw new Error('retry');
      let left = K; const used = []; for (let i = L.length - 1; i >= 0 && left > 0; i--) { const u = Math.min(left, L[i][0]); used.push([u, L[i][1]]); left -= u; }
      const val = used.reduce((s, [u, r]) => s + u * r, 0);
      let l2 = K; const old = []; for (let i = 0; i < L.length && l2 > 0; i++) { const u = Math.min(l2, L[i][0]); old.push([u, L[i][1]]); l2 -= u; }
      const lifo = old.reduce((s, [u, r]) => s + u * r, 0), cost = L.reduce((s, x) => s + x[0] * x[1], 0), avg = F(cost).mul(K).div(tot);
      const q = `Opening inventory ${L[0][0]} units @ ${rs(L[0][1])}. Purchases: ${L.slice(1).map(x => `${x[0]} units @ ${rs(x[1])}`).join(', ')}. ${ind(S)} units were sold during the period. Value the closing inventory using FIFO.`;
      const steps = [`Units available: ${L.map(x => x[0]).join(' + ')} = ${ind(tot)}; closing units = ${ind(tot)} − ${ind(S)} = ${ind(K)}`, 'Under FIFO the earliest units are sold first, so closing units come from the latest purchases', ...used.map(([u, r]) => `${ind(u)} × ${rs(r)} = ${rs(u * r)}`), `Closing inventory: ${used.map(([u, r]) => rs(u * r)).join(' + ')} = ${rs(val)}`];
      return QI(q, build(val, [lifo, roundDp(avg, 0), K * L[L.length - 1][1], K * L[0][1]], rs), 'FIFO assumes the items bought first are sold first, so the closing inventory is valued at the most recent purchase prices.', steps.slice(0, 7), { L, S });
    } });
  def({ id: 'p1_wavg', unit: U('p1-ch04-u01'), name: 'Closing inventory — weighted average', concept: 'Weighted average cost formula',
    make(d) {
      const L = lots(d), rest = L.slice(0, -1).reduce((s, x) => s + x[0], 0), tot = pick([200, 250, 500, 1000, 2000, 2500, 4000, 5000].filter(t => t >= rest + 100)); if (!tot) throw new Error('retry');
      L[L.length - 1][0] = tot - rest; const cost = L.reduce((s, x) => s + x[0] * x[1], 0), avg = F(cost, tot);
      if (badDp(avg, 2)) throw new Error('retry');
      const K = RS(50, tot - 50, 10), S = tot - K, val = avg.mul(K);
      const simple = F(L.reduce((s, x) => s + x[1], 0), L.length).mul(K);
      const q = `Opening inventory ${L[0][0]} units @ ${rs(L[0][1])}. Purchases: ${L.slice(1).map(x => `${x[0]} units @ ${rs(x[1])}`).join(', ')}. ${ind(S)} units were sold. Using the periodic weighted average cost, value the closing inventory.`;
      const steps = [`Total cost: ${L.map(x => `${ind(x[0])} × ${ind(x[1])}`).join(' + ')} = ${rs(cost)}`, `Total units: ${L.map(x => x[0]).join(' + ')} = ${ind(tot)}`, `Weighted average cost: ${ind(cost)} ÷ ${ind(tot)} = ${rs(avg)}`, `Closing units: ${ind(tot)} − ${ind(S)} = ${ind(K)}`, `Closing inventory: ${ind(K)} × ${num(avg)} = ${rs(val)}`];
      return QI(q, build(val, [roundDp(simple, 2), K * L[L.length - 1][1], K * L[0][1], roundDp(avg.mul(S), 2)], rs), 'Weighted average cost = total cost of goods available ÷ total units available. It weights each price by the units bought at that price (not a simple average of prices).', steps, { L, S });
    } });

  def({ id: 'p1_nrv', unit: U('p1-ch04-u01'), name: 'Lower of cost and NRV', concept: 'Net realisable value (item by item)',
    make(d) {
      const names = sample(['Item A', 'Item B', 'Item C', 'Item D'], 3).sort(), rows = names.map(n => { const c = RS(50, 900, 10), sp = c + RS(-200, 300, 10), sc = RS(5, 60, 5), qn = RS(10, 200, 10); return [n, qn, c, sp, sc]; });
      if (rows.some(r => r[3] - r[4] <= 0)) throw new Error('retry');
      const val = rows.reduce((s, [n, qn, c, sp, sc]) => s + qn * Math.min(c, sp - sc), 0), costT = rows.reduce((s, r) => s + r[1] * r[2], 0), nrvT = rows.reduce((s, r) => s + r[1] * (r[3] - r[4]), 0), noSc = rows.reduce((s, r) => s + r[1] * Math.min(r[2], r[3]), 0);
      if (val === costT || val === nrvT) throw new Error('retry');
      const q = `At the year end: ${rows.map(([n, qn, c, sp, sc]) => `${n} — ${qn} units, cost ${rs(c)} each, expected selling price ${rs(sp)} each, selling costs ${rs(sc)} each`).join('; ')}. At what value should inventory be shown (item by item, lower of cost and NRV)?`;
      const steps = rows.map(([n, qn, c, sp, sc]) => `${n}: NRV = ${ind(sp)} − ${ind(sc)} = ${ind(sp - sc)}; lower of ${ind(c)} and ${ind(sp - sc)} = ${ind(Math.min(c, sp - sc))}; ${qn} × ${ind(Math.min(c, sp - sc))} = ${rs(qn * Math.min(c, sp - sc))}`);
      steps.push(`Total: ${rows.map(([n, qn, c, sp, sc]) => rs(qn * Math.min(c, sp - sc))).join(' + ')} = ${rs(val)}`);
      return QI(q, build(val, [costT, nrvT, noSc, Math.min(costT, nrvT)], rs), 'Inventories are valued at the lower of cost and net realisable value, item by item. NRV = estimated selling price − estimated costs to complete and sell.', steps, { rows });
    } });

  def({ id: 'p1_inv_cost', unit: U('p1-ch04-u01'), name: 'Cost of purchase of inventory', concept: 'What is included in cost (AS 2)',
    make(d) {
      const P = RS(50000, 500000, 1000), t = pick([0, 5, 10]), duty = RS(2000, 40000, 500), fr = RS(1000, 15000, 100), g = pick([12, 18]), stor = RS(1000, 10000, 100), sell = RS(1000, 12000, 100);
      const net = F(P).mul(100 - t).div(100), cost = net.add(duty).add(fr), gst = net.mul(g).div(100);
      const q = `Goods were imported at a list price of ${rs(P)}${t ? ` less ${t}% trade discount` : ''}. Import duty ${rs(duty)}; freight inward ${rs(fr)}; GST paid ${rs(gst)} (input tax credit available); storage of the goods after they reached the selling warehouse ${rs(stor)}; selling commission ${rs(sell)}. What is the cost of purchase of the inventory?`;
      const steps = [t ? `Purchase price after trade discount: ${rs(P)} × ${100 - t}% = ${rs(net)}` : `Purchase price = ${rs(net)}`, `Add import duty and freight inward: ${rs(net)} + ${rs(duty)} + ${rs(fr)} = ${rs(cost)}`, 'GST is recoverable (credit available), storage after arrival at the selling point and selling commission are not costs of purchase'];
      return QI(q, build(cost, [cost.add(gst), cost.add(stor), F(P).add(duty).add(fr), cost.add(stor).add(sell)], rs), 'Cost of purchase = purchase price + import duties and non-recoverable taxes + freight inward and other directly attributable costs − trade discounts. Recoverable taxes, later storage and selling costs are excluded.', steps, { P, t, duty, fr, g, stor, sell });
    } });

  /* ---- Depreciation ---- */
  def({ id: 'p1_dep_slm', unit: U('p1-ch05-u01'), name: 'Depreciation — straight line', concept: 'Straight line method and time basis',
    make(d) {
      const n = pick([4, 5, 8, 10]), off = d === 'easy' ? 0 : R(0, 11), mths = 12 - off, C = RS(60000, 900000, 1000), I = pick([0, RS(1000, 20000, 500)]), S = pick([0, RS(5000, 60000, 1000)]);
      const base = C + I - S; if (base <= 0) throw new Error('retry');
      const ann = F(base, n), dep = ann.mul(mths).div(12); if (dpOf(dep) === null || badDp(dep, 2)) throw new Error('retry');
      const fy = R(2023, 2026);
      const q = `A machine was bought on ${fyDate(fy, off)} for ${rs(C)}${I ? `; installation cost ${rs(I)}` : ''}. Estimated useful life ${n} years${S ? `, residual value ${rs(S)}` : ', no residual value'}. Books close on 31 March. Using the straight line method on a time basis, what is the depreciation for the year ending 31 March ${fy + 1}?`;
      const steps = [`Depreciable amount: ${rs(C)}${I ? ` + ${rs(I)}` : ''}${S ? ` − ${rs(S)}` : ''} = ${rs(base)}`, `Annual depreciation: ${ind(base)} ÷ ${n} = ${rs(ann)}`, `Months used in the first year: ${mths}`, `Depreciation: ${num(ann)} × ${mths}/12 = ${rs(dep)}`];
      return QI(q, build(dep, [ann, F(C + I, n).mul(mths).div(12), F(C, n).mul(mths).div(12), F(base, n).mul(mths + 1).div(12)], rs), 'SLM charges an equal amount each year: (cost including installation − residual value) ÷ useful life. In the year of purchase, charge only for the months the asset was available for use.', mths === 12 ? steps.filter((s, i) => i !== 2) : steps, { C, I, S, n, off, fy });
    } });

  def({ id: 'p1_dep_wdv', unit: U('p1-ch05-u01'), name: 'Depreciation — written down value', concept: 'WDV (reducing balance) method',
    make(d) {
      const C = RS(50000, 1000000, 10000), r = pick([10, 15, 20, 25]), k = d === 'easy' ? 2 : R(2, 4), ask = pick(['wdv', 'dep']);
      const w = []; let b = F(C); for (let i = 0; i < k; i++) { const dp = b.mul(r).div(100); w.push([b, dp]); b = b.sub(dp); }
      const corr = ask === 'wdv' ? b : w[k - 1][1]; if (badDp(corr, 2) || dpOf(corr) === null) throw new Error('retry');
      const slm = ask === 'wdv' ? F(C).mul(100 - r * k).div(100) : F(C).mul(r).div(100);
      const q = `An asset costing ${rs(C)} is depreciated at ${r}% p.a. on the written down value. It was bought at the start of Year 1. What is ${ask === 'wdv' ? `its written down value at the end of Year ${k}` : `the depreciation for Year ${k}`}?`;
      const steps = w.map(([b0, dp], i) => `Year ${i + 1}: ${num(b0)} × ${r}% = ${num(dp)}; closing ${num(b0)} − ${num(dp)} = ${num(b0.sub(dp))}`);
      return QI(q, build(corr, ask === 'wdv' ? [slm, b.add(w[k - 1][1]), b.sub(b.mul(r).div(100))] : [slm, k > 1 ? w[k - 2][1] : null, b.mul(r).div(100)], rs, { ok: x => F(x).sign > 0 }), 'Under WDV the rate is applied each year to the opening book value (cost less depreciation to date), so the charge falls every year.', steps, { C, r, k, ask });
    } });

  function depSchedule(C, r, method, off, yrs, saleOff) {   // returns [[year, opening, dep, closing, months]]; method 'slm' on cost / 'wdv'
    const out = []; let b = F(C);
    for (let y = 0; y < yrs; y++) {
      const m = y === 0 ? 12 - off : (saleOff !== undefined && y === yrs - 1 ? saleOff : 12);
      const dep = (method === 'slm' ? F(C) : b).mul(r).div(100).mul(m).div(12); out.push([y, b, dep, b.sub(dep), m]); b = b.sub(dep);
    }
    return out;
  }
  def({ id: 'p1_dep_sale', unit: U('p1-ch05-u01'), name: 'Profit or loss on sale of an asset', concept: 'Book value at the date of sale',
    make(d) {
      const C = RS(100000, 900000, 10000), r = pick([10, 15, 20]), method = pick(['slm', 'wdv']), off = R(0, 8), fy = R(2021, 2023), yrs = R(2, 4), so = R(1, 11);
      const sc = depSchedule(C, r, method, off, yrs, so), bv = sc[yrs - 1][3]; if (dpOf(bv) === null || badDp(bv, 2)) throw new Error('retry');
      const P = RS(Math.max(1000, Math.round(bv.v * .6)), Math.round(bv.v * 1.3), 500), pl = F(P).sub(bv); if (!pl.sign) throw new Error('retry');
      const fullYr = depSchedule(C, r, method, off, yrs, 12)[yrs - 1][3], noDep = yrs > 1 ? depSchedule(C, r, method, off, yrs - 1)[yrs - 2][3] : F(C);
      const q = `A machine costing ${rs(C)} was bought on ${fyDate(fy, off)}. Depreciation is charged at ${r}% p.a. on the ${method === 'slm' ? 'straight line method (on original cost)' : 'written down value method'}, on a time basis; books close on 31 March. The machine was sold on ${fyDate(fy + yrs - 1, so)} for ${rs(P)}. Find the profit or loss on sale.`;
      const steps = sc.map(([y, b0, dp, b1, m]) => `${fy + y}-${String((fy + y + 1) % 100).padStart(2, '0')}: ${num(method === 'slm' ? F(C) : b0)} × ${r}% × ${m}/12 = ${num(dp)}`);
      steps.push(`Book value on sale: ${num(C)} − ${sc.map(x => num(x[2])).join(' − ')} = ${num(bv)}`, `${PorL(pl)}: ${ind(P)} − ${num(bv)} = ${num(pl)}`);
      return QI(q, build(pl, [pl.neg(), F(P).sub(fullYr), F(P).sub(noDep), F(P).sub(C)], v => PorL(v), { ok: v => F(v).sign !== 0 }), 'Charge depreciation up to the date of sale (time basis), find the book value, and compare it with the sale price: sale price above book value is a profit, below is a loss.', steps.length > 7 ? [steps[0], '…', ...steps.slice(-4)] : steps, { C, r, method, off, fy, yrs, so, P });
    } });

  def({ id: 'p1_dep_change', unit: U('p1-ch05-u01'), name: 'Change in depreciation method', concept: 'Change of method is applied prospectively',
    make(d) {
      const C = RS(100000, 1000000, 10000), r = pick([10, 12, 15, 20]), k = R(2, 4), w = pick([15, 20, 25]);
      if (r * k >= 100) throw new Error('retry');
      const bv = F(C).mul(100 - r * k).div(100), dep = bv.mul(w).div(100); if (badDp(dep, 2)) throw new Error('retry');
      const q = `A machine costing ${rs(C)} was depreciated on the straight line method at ${r}% p.a. for ${k} years. From Year ${k + 1} the company changes to the written down value method at ${w}% p.a. The change is treated as a change in accounting estimate and applied prospectively. What is the depreciation for Year ${k + 1}?`;
      const steps = [`Depreciation charged so far: ${ind(C)} × ${r}% × ${k} = ${rs(F(C).mul(r * k).div(100))}`, `Carrying amount at the start of Year ${k + 1}: ${ind(C)} − ${num(F(C).mul(r * k).div(100))} = ${rs(bv)}`, `Year ${k + 1} depreciation: ${num(bv)} × ${w}% = ${rs(dep)}`];
      const retro = F(C).mul(F(100 - w, 100).pow(k)).mul(w).div(100);   // wrongly restating past years on WDV
      return QI(q, build(dep, [F(C).mul(w).div(100), F(C).mul(r).div(100), roundDp(retro, 2), bv.mul(r).div(100)], rs), 'A change in the method of depreciation is a change in accounting estimate: no catch-up for past years; the new method is applied to the carrying amount from the year of change.', steps, { C, r, k, w });
    } });

  def({ id: 'p1_dep_schedule', unit: U('p1-ch05-u01'), name: 'Depreciation schedule (show working)', concept: 'Depreciation over several years', kinds: ['desc'],
    desc(d) {
      for (let tries = 0; tries < 50; tries++) {
        const C = RS(100000, 800000, 10000), r = pick([10, 15, 20]), method = pick(['slm', 'wdv']), off = R(0, 9), fy = R(2023, 2025);
        const sc = depSchedule(C, r, method, off, 3); if (sc.some(x => dpOf(x[2]) === null || badDp(x[2], 2))) continue;
        const yl = y => `${fy + y}-${String((fy + y + 1) % 100).padStart(2, '0')}`;
        const rows = sc.map(([y, b0, dp, b1, m]) => [yl(y), num(b0), `${num(method === 'slm' ? F(C) : b0)} × ${r}% × ${m}/12 = ${num(dp)}`, num(b1)]);
        const scheme = sc.map(([y, b0, dp, b1, m], i) => ({ id: 's' + (i + 1), pt: `${yl(y)} depreciation ${rs(dp)}${i === 0 && m < 12 ? ` (time basis: ${m} months)` : ''}`, m: 1, skill: 'computation' }));
        scheme.push({ id: 's4', pt: `Closing written down value ${rs(sc[2][3])} after three years`, m: 1, skill: 'computation' }, { id: 's5', pt: 'Schedule / Machinery Account neatly presented with years, opening value, depreciation and closing value', m: 1, skill: 'presentation' });
        const q = `A machine was bought on ${fyDate(fy, off)} for ${rs(C)}. Depreciation is charged at ${r}% p.a. on the ${method === 'slm' ? 'straight line method' : 'written down value method'} on a time basis; books close on 31 March each year. Prepare a depreciation schedule for the first three years.`;
        return { kind: 'desc', marks: 5, minutes: 9, pad: 'table', q, given: [], model: [{ t: 'table', head: ['Year', 'Opening value (₹)', 'Depreciation (₹)', 'Closing value (₹)'], rows, num: [1, 3] }],
          scheme, steps: sc.map(([y, b0, dp, b1, m]) => `${yl(y)}: ${num(method === 'slm' ? F(C) : b0)} × ${r}% × ${m}/12 = ${num(dp)}; closing ${num(b0)} − ${num(dp)} = ${num(b1)}`), answer: `Closing value after 3 years ${rs(sc[2][3])}`, data: { C, r, method, off, fy } };
      }
      throw new Error('retry');
    } });

  /* ---- Bills of exchange ---- */
  const addDays = (dt, n) => new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate() + n));
  function addMonths(dt, n) { const y = dt.getUTCFullYear(), m = dt.getUTCMonth() + n, last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate(); return new Date(Date.UTC(y, m, Math.min(dt.getUTCDate(), last))); }
  def({ id: 'p1_bill_due', unit: U('p1-ch06-u01'), name: 'Due date of a bill', concept: 'Days of grace and date of maturity',
    make(d) {
      const y = R(2025, 2027), dt = new Date(Date.UTC(y, R(0, 11), pick([R(1, 28), R(1, 28), 29, 30, 31]))); if (dt.getUTCDate() < 28 && chance(.1)) throw new Error('retry');
      const kind = pick(['months', 'months', 'days', 'sight']), hol = d !== 'easy' && chance(.3);
      let base, q, steps, n, acc;
      if (kind === 'days') { n = pick([30, 45, 60, 90]); base = addDays(dt, n); q = `A bill dated ${dstr(dt)} is payable ${n} days after date.`; steps = [`Exclude the date of drawing: ${dstr(dt)} + ${n} days = ${dstr(base)}`]; }
      else if (kind === 'sight') { n = pick([1, 2, 3]); acc = addDays(dt, R(2, 6)); base = addMonths(acc, n); q = `A bill drawn on ${dstr(dt)} payable ${PL(n, 'month')} after sight was accepted on ${dstr(acc)}.`; steps = [`After sight: count from the date of acceptance: ${dstr(acc)} + ${PL(n, 'month')} = ${dstr(base)}`]; }
      else { n = pick([1, 2, 3, 4, 6]); base = addMonths(dt, n); q = `A bill dated ${dstr(dt)} is payable ${PL(n, 'month')} after date.`; steps = [`${dstr(dt)} + ${PL(n, 'month')} = ${dstr(base)}${base.getUTCDate() !== dt.getUTCDate() ? ' (no corresponding date, so the last day of that month)' : ''}`]; }
      let due = addDays(base, 3); steps.push(`Add 3 days of grace: ${dstr(due)}`);
      if (hol) { q += ` The date of maturity so arrived at is a public holiday.`; const d2 = addDays(due, -1); steps.push('It is a public holiday, so the bill is due on the preceding business day: ' + dstr(d2)); due = d2; }
      q += ' What is the date of maturity?';
      const wr = [base, addDays(due, hol ? 2 : 1), addDays(due, -1), kind === 'sight' ? addDays(addMonths(dt, n), hol ? 2 : 3) : addDays(dt, (kind === 'days' ? n : 30 * n) + 3 - (hol ? 1 : 0)), kind === 'days' ? addDays(due, -1) : null];
      return QI(q, build(due, wr, x => dstr(x)), 'Every bill not payable on demand gets 3 days of grace. For “after date” count from the date of the bill (excluding that day when counting days); for “after sight” count from acceptance. If the maturity date is a public holiday, the bill is due on the preceding business day.', steps, { y: dt.getUTCFullYear(), m: dt.getUTCMonth(), dd: dt.getUTCDate(), kind, n, hol, acc: acc ? [acc.getUTCFullYear(), acc.getUTCMonth(), acc.getUTCDate()] : null });
    } });

  def({ id: 'p1_bill_disc', unit: U('p1-ch06-u01'), name: 'Discounting a bill', concept: 'Discount charged by the bank',
    make(d) {
      const Fv = RS(10000, 300000, 1000), T = pick([3, 4, 6]), k = R(1, T - 1), r = pick([6, 8, 9, 10, 12, 15, 18]), ask = pick(['net', 'disc']);
      const disc = F(Fv).mul(r).div(100).mul(T - k).div(12), net = F(Fv).sub(disc); if (badDp(disc, 2)) throw new Error('retry');
      const q = `A bill for ${rs(Fv)} payable ${T} months after date was discounted with the bank ${PL(k, 'month')} after its date at ${r}% p.a. Calculate discount for the unexpired period in months (ignore days of grace). ${ask === 'net' ? 'How much did the holder receive from the bank?' : 'What is the discount charged by the bank?'}`;
      const full = F(Fv).mul(r).div(100).mul(T).div(12), yr = F(Fv).mul(r).div(100);
      const steps = [`Unexpired period: ${T} − ${k} = ${PL(T - k, 'month')}`, `Discount: ${ind(Fv)} × ${r}% × ${T - k}/12 = ${rs(disc)}`]; if (ask === 'net') steps.push(`Received: ${ind(Fv)} − ${num(disc)} = ${rs(net)}`);
      return QI(q, build(ask === 'net' ? net : disc, ask === 'net' ? [F(Fv).sub(full), F(Fv).sub(yr), F(Fv).sub(F(Fv).mul(r).div(100).mul(k).div(12))] : [full, yr, F(Fv).mul(r).div(100).mul(k).div(12)], rs, { ok: x => F(x).sign > 0 }), 'The bank deducts interest (discount) for the period the bill still has to run; the holder receives the face value less this discount.', steps, { Fv, T, k, r, ask });
    } });

  /* ---- Final accounts ---- */
  def({ id: 'p1_gross_profit', unit: U('p1-ch07-u01'), name: 'Gross profit', concept: 'Trading account', kinds: ['mcq', 'desc'],
    desc(d) {
      for (let t = 0; t < 50; t++) { const x = this.make(d); if (x) { const { OS, P, PR, CI, W, S, SR, CS, CO } = x.data, cogs = OS + P - PR + CI + W - CS, gp = S - SR - cogs;
        const rows = [['To Opening inventory', ind(OS), 'By Sales', ind(S)], ['To Purchases ' + ind(P), '', 'Less: Sales returns', '(' + ind(SR) + ')'], ['Less: Purchases returns (' + ind(PR) + ')', ind(P - PR), '', ind(S - SR)], ['To Carriage inwards', ind(CI), 'By Closing inventory', ind(CS)], ['To Wages', ind(W), '', ''], ['To Gross profit c/d', ind(gp), '', ''], ['Total', ind(OS + P - PR + CI + W + gp), 'Total', ind(S - SR + CS)]];
        const scheme = [{ id: 's1', pt: `Net sales ${rs(S - SR)} (sales less returns)`, m: 1, skill: 'computation' }, { id: 's2', pt: `Net purchases ${rs(P - PR)} with carriage inwards and wages on the debit side`, m: 1, skill: 'classification' }, { id: 's3', pt: `Closing inventory ${rs(CS)} credited; carriage outwards left for the P&L Account`, m: 1, skill: 'classification' }, { id: 's4', pt: `Gross profit ${rs(gp)}; both sides total ${rs(S - SR + CS)}`, m: 1, skill: 'balancing' }, { id: 's5', pt: 'Trading Account heading with period, To/By format', m: 1, skill: 'presentation' }];
        return { kind: 'desc', marks: 5, minutes: 9, pad: 'table', q: x.q.replace(' What is the gross profit?', ' Prepare the Trading Account for the year ended 31 March 2026.'), given: [], model: [{ t: 'table', head: ['Dr. Particulars', '₹', 'Cr. Particulars', '₹'], rows }], scheme, steps: x.steps.slice(0, 3), answer: 'Gross profit ' + rs(gp), data: x.data }; } }
      throw new Error('retry');
    },
    make(d) {
      const OS = RS(20000, 150000, 1000), P = RS(200000, 900000, 1000), PR = RS(2000, 20000, 500), CI = RS(1000, 20000, 500), W = RS(5000, 80000, 1000), S = RS(300000, 1500000, 1000), SR = RS(2000, 30000, 500), CS = RS(20000, 180000, 1000), CO = RS(1000, 20000, 500);
      const cogs = OS + P - PR + CI + W - CS, gp = S - SR - cogs; if (gp <= 0) throw new Error('retry');
      const q = `Opening inventory ${rs(OS)}; purchases ${rs(P)}; purchases returns ${rs(PR)}; carriage inwards ${rs(CI)}; wages ${rs(W)}; sales ${rs(S)}; sales returns ${rs(SR)}; carriage outwards ${rs(CO)}; closing inventory ${rs(CS)}. What is the gross profit?`;
      const steps = [`Net sales: ${ind(S)} − ${ind(SR)} = ${rs(S - SR)}`, `Cost of goods sold: ${ind(OS)} + ${ind(P)} − ${ind(PR)} + ${ind(CI)} + ${ind(W)} − ${ind(CS)} = ${rs(cogs)}`, `Gross profit: ${ind(S - SR)} − ${ind(cogs)} = ${rs(gp)}`, 'Carriage outwards is a selling expense, charged to the Profit and Loss Account'];
      return QI(q, build(gp, [gp - CO, gp + SR + PR, gp + 2 * CS, gp + CI + W, S - P], rs, { ok: x => x > 0 }), 'Gross profit = net sales − cost of goods sold, where cost of goods sold = opening inventory + net purchases + direct expenses (carriage inwards, wages) − closing inventory.', steps, { OS, P, PR, CI, W, S, SR, CS, CO });
    } });

  const NPADJ = [['out', x => `salary outstanding ${rs(x)}`, -1], ['pre', x => `insurance prepaid ${rs(x)}`, 1], ['acc', x => `interest accrued but not received ${rs(x)}`, 1], ['adv', x => `rent received in advance ${rs(x)}`, -1], ['dep', x => `depreciation not yet provided ${rs(x)}`, -1], ['cs_omit', x => `goods of ${rs(x)} taken by the proprietor for personal use not recorded`, 1]];
  def({ id: 'p1_np_adjust', unit: U('p1-ch07-u01'), name: 'Net profit after adjustments', concept: 'Outstanding, prepaid, accrued and advance items',
    make(d) {
      const P = RS(50000, 600000, 1000), adj = sample(NPADJ, d === 'easy' ? 2 : R(3, 4)).map(a => [a, RS(1000, 40000, 500)]), np = P + adj.reduce((s, [a, x]) => s + a[2] * x, 0); if (np <= 0) throw new Error('retry');
      const q = `The net profit of a sole trader before adjustments is ${rs(P)}. Adjust for: ${adj.map(([a, x]) => a[1](x)).join('; ')}. What is the adjusted net profit?`;
      const steps = adj.map(([a, x]) => `${a[1](x)[0].toUpperCase() + a[1](x).slice(1)}: ${a[2] > 0 ? 'add' : 'deduct'} ${rs(x)}`); steps.push(`Adjusted profit: ${ind(P)} ${adj.map(([a, x]) => `${a[2] > 0 ? '+' : '−'} ${ind(x)}`).join(' ')} = ${rs(np)}`);
      const rev = P - adj.reduce((s, [a, x]) => s + a[2] * x, 0);
      return QI(q, build(np, [rev, P + adj.reduce((s, [a, x]) => s + x, 0), P - adj.reduce((s, [a, x]) => s + x, 0), np - 2 * adj[0][0][2] * adj[0][1]], rs, { ok: x => x > 0 }), 'Expenses outstanding and incomes received in advance reduce profit; expenses prepaid and incomes accrued increase it. Goods taken for personal use reduce purchases, so they increase profit.', steps, { P, adj: adj.map(([a, x]) => [a[0], x]) });
    } });

  def({ id: 'p1_bad_debts', unit: U('p1-ch07-u01'), name: 'Bad debts and provision for doubtful debts', concept: 'Provision for doubtful debts',
    make(d) {
      const D = RS(50000, 500000, 1000), b0 = RS(0, 10000, 500), b1 = RS(500, 12000, 500), p0 = RS(1000, 25000, 500), r = pick([2, 3, 4, 5, 10]);
      const np = F(D - b1).mul(r).div(100), ch = np.add(b0 + b1).sub(p0); if (ch.sign <= 0 || badDp(ch, 2)) throw new Error('retry');
      const q = `Trial balance: trade receivables ${rs(D)}, bad debts ${rs(b0)}, provision for doubtful debts ${rs(p0)}. Adjustments: write off further bad debts ${rs(b1)}; maintain a provision for doubtful debts at ${r}% on trade receivables. What net amount is charged to the Profit and Loss Account for bad debts and the provision?`;
      const steps = [`Receivables after further bad debts: ${ind(D)} − ${ind(b1)} = ${rs(D - b1)}`, `New provision: ${ind(D - b1)} × ${r}% = ${rs(np)}`, `Charge: ${ind(b0)} + ${ind(b1)} + ${num(np)} − ${ind(p0)} = ${rs(ch)}`];
      return QI(q, build(ch, [np.add(b1).sub(p0), F(D).mul(r).div(100).add(b0 + b1).sub(p0), np.add(b0 + b1), np.add(b0 + b1).add(p0)], rs, { ok: x => F(x).sign > 0 }), 'Total bad debts (trial balance + further) plus the new provision, minus the old provision, is the net charge. The new provision is calculated after writing off further bad debts.', steps, { D, b0, b1, p0, r });
    } });

  def({ id: 'p1_mfg', unit: U('p1-ch07-u02'), name: 'Cost of goods manufactured', concept: 'Manufacturing account',
    make(d) {
      const RO = RS(20000, 120000, 1000), RP = RS(200000, 900000, 1000), RC = RS(20000, 150000, 1000), CP = RS(2000, 20000, 500), DW = RS(50000, 300000, 1000), FP = RS(10000, 60000, 500), FR = RS(10000, 80000, 500), FD = RS(5000, 50000, 500), WO = RS(10000, 80000, 1000), WC = RS(10000, 80000, 1000), OS = RS(10000, 60000, 500);
      const rmc = RO + RP + CP - RC, cop = rmc + DW + FP + FR + FD + WO - WC; if (rmc <= 0) throw new Error('retry');
      const q = `Raw materials: opening ${rs(RO)}, purchases ${rs(RP)}, carriage on purchases ${rs(CP)}, closing ${rs(RC)}. Direct wages ${rs(DW)}; factory power ${rs(FP)}; factory rent ${rs(FR)}; depreciation of plant ${rs(FD)}; office salaries ${rs(OS)}; work-in-progress: opening ${rs(WO)}, closing ${rs(WC)}. What is the cost of goods manufactured (cost of production)?`;
      const steps = [`Raw materials consumed: ${ind(RO)} + ${ind(RP)} + ${ind(CP)} − ${ind(RC)} = ${rs(rmc)}`, `Prime cost: ${ind(rmc)} + ${ind(DW)} = ${rs(rmc + DW)}`, `Factory overheads: ${ind(FP)} + ${ind(FR)} + ${ind(FD)} = ${rs(FP + FR + FD)}`, `Cost of production: ${ind(rmc + DW)} + ${ind(FP + FR + FD)} + ${ind(WO)} − ${ind(WC)} = ${rs(cop)}`, 'Office salaries go to the Profit and Loss Account'];
      return QI(q, build(cop, [cop + OS, cop - WO + WC, cop + RC - RO, rmc + DW], rs), 'Cost of production = raw materials consumed + direct wages + direct expenses + factory overheads + opening WIP − closing WIP. Office and selling expenses are not part of it.', steps, { RO, RP, RC, CP, DW, FP, FR, FD, WO, WC, OS });
    } });

  /* ---- Not-for-profit organisations ---- */
  def({ id: 'p1_npo_subs', unit: U('p1-ch08-u01'), name: 'Subscriptions — income for the year', concept: 'Subscriptions with arrears and advance',
    make(d) {
      const Rc = RS(100000, 600000, 1000), a1 = RS(2000, 30000, 500), a2 = RS(2000, 30000, 500), o = RS(2000, 30000, 500), a0 = RS(1000, 20000, 500), cl = pick(CLUBS);
      const inc = Rc - a1 - a2 + o + a0;
      const q = `${cl} received subscriptions of ${rs(Rc)} during 2025-26. This includes ${rs(a1)} for 2024-25 and ${rs(a2)} for 2026-27. Subscriptions outstanding for 2025-26 are ${rs(o)}. Subscriptions of ${rs(a0)} for 2025-26 had been received in advance during 2024-25. What is the subscription income for 2025-26?`;
      const steps = [`Received during the year ${rs(Rc)}`, `Less arrears for last year and advance for next year: ${ind(Rc)} − ${ind(a1)} − ${ind(a2)} = ${rs(Rc - a1 - a2)}`, `Add outstanding for this year and last year's advance for this year: ${ind(Rc - a1 - a2)} + ${ind(o)} + ${ind(a0)} = ${rs(inc)}`];
      return QI(q, build(inc, [Rc - a1 - a2 + o - a0, Rc + a1 + a2 - o - a0, Rc - a1 - a2 + o, Rc - a1 + a2 + o + a0], rs, { ok: x => x > 0 }), 'Income & Expenditure shows only the subscription that relates to the current year: remove amounts for other years from receipts, add amounts of this year received earlier or still to be received.', steps, { Rc, a1, a2, o, a0 });
    } });

  def({ id: 'p1_npo_sports', unit: U('p1-ch08-u01'), name: 'Sports material consumed', concept: 'Consumption of stores in an NPO',
    make(d) {
      const so = RS(5000, 60000, 500), sc = RS(5000, 60000, 500), paid = RS(30000, 200000, 1000), co = RS(2000, 25000, 500), cc = RS(2000, 25000, 500);
      const pur = paid - co + cc, cons = so + pur - sc; if (cons <= 0) throw new Error('retry');
      const q = `A sports club paid ${rs(paid)} to suppliers of sports material during the year. Creditors for sports material: opening ${rs(co)}, closing ${rs(cc)}. Stock of sports material: opening ${rs(so)}, closing ${rs(sc)}. What amount of sports material consumed is shown in the Income and Expenditure Account?`;
      const steps = [`Purchases: ${ind(paid)} − ${ind(co)} + ${ind(cc)} = ${rs(pur)}`, `Consumed: ${ind(so)} + ${ind(pur)} − ${ind(sc)} = ${rs(cons)}`];
      return QI(q, build(cons, [so + paid - sc, so + paid + co - cc - sc, pur, sc + pur - so], rs, { ok: x => x > 0 }), 'Find purchases on accrual basis (payments − opening creditors + closing creditors), then consumption = opening stock + purchases − closing stock.', steps, { so, sc, paid, co, cc });
    } });

  /* ---- Incomplete records ---- */
  def({ id: 'p1_capital_compare', unit: U('p1-ch09-u01'), name: 'Profit by capital comparison', concept: 'Statement of affairs method',
    make(d) {
      const A0 = RS(200000, 900000, 1000), L0 = RS(20000, 200000, 1000), A1 = RS(Math.round(A0 * .85), Math.round(A0 * 1.45), 1000), L1 = RS(20000, 250000, 1000), dw = RS(12000, 120000, 1000), add = pick([0, 0, RS(10000, 100000, 1000)]);
      const C0 = A0 - L0, C1 = A1 - L1, pr = C1 - C0 + dw - add; if (C0 <= 0 || C1 <= 0 || pr === 0) throw new Error('retry');
      const q = `A trader keeps incomplete records. On 1 April 2025: assets ${rs(A0)}, liabilities ${rs(L0)}. On 31 March 2026: assets ${rs(A1)}, liabilities ${rs(L1)}. Drawings during the year ${rs(dw)}${add ? `; additional capital introduced ${rs(add)}` : ''}. Find the profit or loss for the year.`;
      const steps = [`Opening capital: ${ind(A0)} − ${ind(L0)} = ${rs(C0)}`, `Closing capital: ${ind(A1)} − ${ind(L1)} = ${rs(C1)}`, `Profit: ${ind(C1)} + ${ind(dw)}${add ? ` − ${ind(add)}` : ''} − ${ind(C0)} = ${pr < 0 ? '−' : ''}${ind(Math.abs(pr))}`];
      return QI(q, build(pr, [C1 - C0 - dw + add, C1 - C0, C1 - C0 + dw + add, -pr], v => PorL(v), { ok: v => v !== 0 }), 'Profit = closing capital − opening capital + drawings − additional capital introduced.', steps, { A0, L0, A1, L1, dw, add });
    } });

  def({ id: 'p1_credit_purchases', unit: U('p1-ch09-u01'), name: 'Missing credit purchases / sales', concept: 'Total creditors and debtors accounts',
    make(d) {
      const sales = chance(.5), O = RS(20000, 200000, 1000), C = RS(20000, 200000, 1000), cash = RS(100000, 900000, 1000), disc = RS(500, 10000, 500), ret = RS(1000, 20000, 500), bd = sales ? RS(0, 8000, 500) : 0;
      const val = C + cash + disc + ret + bd - O; if (val <= 0) throw new Error('retry');
      const q = sales ? `Trade receivables: opening ${rs(O)}, closing ${rs(C)}. Cash received from customers ${rs(cash)}; discount allowed ${rs(disc)}; sales returns ${rs(ret)}${bd ? `; bad debts written off ${rs(bd)}` : ''}. Find the credit sales.` : `Trade payables: opening ${rs(O)}, closing ${rs(C)}. Cash paid to suppliers ${rs(cash)}; discount received ${rs(disc)}; purchases returns ${rs(ret)}. Find the credit purchases.`;
      const steps = [`${sales ? 'Credits to receivables' : 'Debits to payables'}: ${ind(cash)} + ${ind(disc)} + ${ind(ret)}${bd ? ` + ${ind(bd)}` : ''} + closing ${ind(C)} = ${rs(C + cash + disc + ret + bd)}`, `Credit ${sales ? 'sales' : 'purchases'}: ${ind(C + cash + disc + ret + bd)} − ${ind(O)} = ${rs(val)}`];
      return QI(q, build(val, [val + 2 * O - 2 * C, cash + C - O, val - 2 * disc, val - 2 * ret], rs, { ok: x => x > 0 }), `Credit ${sales ? 'sales' : 'purchases'} is the balancing figure of the total ${sales ? 'debtors' : 'creditors'} account: closing balance + cash + discount + returns${sales ? ' + bad debts' : ''} − opening balance.`, steps, { sales, O, C, cash, disc, ret, bd });
    } });

  /* ---- Partnership ---- */
  const RATIOS2 = [[3, 2], [2, 1], [1, 1], [5, 3], [3, 1], [4, 3], [7, 3], [3, 5]], RATIOS3 = [[3, 2, 1], [2, 2, 1], [5, 3, 2], [4, 3, 2], [1, 1, 1], [3, 3, 2], [2, 1, 1]];
  const rStr = a => a.join(' : ');
  def({ id: 'p1_int_capital', unit: U('p1-ch10-u01'), name: 'Interest on capital', concept: 'Interest on capital with changes during the year',
    make(d) {
      const [A, B] = sample(PEOPLE, 2), ca = RS(100000, 1000000, 10000), r = pick([5, 6, 8, 9, 10, 12]), addOff = R(1, 11), x = RS(20000, 300000, 10000), wd = d !== 'easy' && chance(.5), wOff = R(1, 11), y = RS(10000, Math.min(ca / 2, 200000), 10000);
      const i1 = F(ca).mul(r).div(100), i2 = F(x).mul(r).div(100).mul(12 - addOff).div(12), i3 = wd ? F(y).mul(r).div(100).mul(12 - wOff).div(12) : F(0), tot = i1.add(i2).sub(i3);
      if (badDp(tot, 2)) throw new Error('retry');
      const q = `${poss(A)} capital on 1 April 2025 was ${rs(ca)}. ${A} introduced further capital of ${rs(x)} on ${fyDate(2025, addOff)}${wd ? ` and withdrew ${rs(y)} of capital on ${fyDate(2025, wOff)}` : ''}. Interest on capital is allowed at ${r}% p.a. What is ${poss(A)} interest on capital for the year ending 31 March 2026?`;
      const steps = [`On opening capital: ${ind(ca)} × ${r}% = ${rs(i1)}`, `On additional capital (${PL(12 - addOff, 'month')}): ${ind(x)} × ${r}% × ${12 - addOff}/12 = ${rs(i2)}`];
      if (wd) steps.push(`Less on capital withdrawn (${PL(12 - wOff, 'month')}): ${ind(y)} × ${r}% × ${12 - wOff}/12 = ${rs(i3)}`);
      steps.push(`Total: ${num(i1)} + ${num(i2)}${wd ? ` − ${num(i3)}` : ''} = ${rs(tot)}`);
      return QI(q, build(tot, [F(ca + x).mul(r).div(100), i1, i1.add(i2).add(i3), i1.add(F(x).mul(r).div(100).mul(addOff).div(12)).sub(i3)], rs), 'Interest on capital is allowed for the period each amount was actually used in the business: the opening capital for 12 months, later additions or withdrawals for the months that remain.', steps, { ca, r, addOff, x, wd, wOff, y });
    } });

  const IOD = { begm: [F(13, 2), 'at the beginning of every month', '6½'], midm: [F(6), 'in the middle of every month', '6'], endm: [F(11, 2), 'at the end of every month', '5½'], begq: [F(15, 2), 'at the beginning of every quarter', '7½'], endq: [F(9, 2), 'at the end of every quarter', '4½'] };
  def({ id: 'p1_int_drawings', unit: U('p1-ch10-u01'), name: 'Interest on drawings (average period)', concept: 'Average period for equal drawings',
    make(d) {
      const k = pick(Object.keys(IOD)), [m, txt, mt] = IOD[k], qtr = k.endsWith('q'), per = qtr ? RS(5000, 60000, 1000) : RS(1000, 25000, 500), n = qtr ? 4 : 12, D = per * n, r = pick([5, 6, 8, 9, 10, 12, 15]), P = pick(PEOPLE);
      const I = F(D).mul(r).div(100).mul(m).div(12); if (badDp(I, 2)) throw new Error('retry');
      const q = `${P}, a partner, withdrew ${rs(per)} ${txt} during the year ending 31 March 2026. Interest on drawings is charged at ${r}% p.a. What is the interest on drawings?`;
      const mm = String(num(m)).replace('.5', '.5');
      const steps = [`Total drawings: ${rs(per)} × ${n} = ${rs(D)}`, `Average period for drawings ${txt}: ${mt} months`, `Interest: ${ind(D)} × ${r}% × ${num(m)}/12 = ${rs(I)}`];
      const others = Object.values(IOD).map(v => F(D).mul(r).div(100).mul(v[0]).div(12));
      return QI(q, build(I, [...others, F(D).mul(r).div(100)], rs), 'With equal drawings, interest is charged on the total for the average period: 6½ months (beginning of each month), 6 (middle), 5½ (end); 7½ months (beginning of each quarter), 4½ (end of each quarter).', steps, { k, per, r });
    } });

  def({ id: 'p1_iod_product', unit: U('p1-ch10-u01'), name: 'Interest on drawings — product method (show working)', concept: 'Product method for unequal drawings', kinds: ['mcq', 'desc'],
    _data(d) {
      const r = pick([6, 8, 9, 10, 12]), k = d === 'easy' ? 3 : R(4, 5), offs = sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], k).sort((a, b) => a - b), amts = offs.map(() => RS(2000, 50000, 1000));
      const rows = offs.map((o, i) => [o, amts[i], 12 - o, amts[i] * (12 - o)]), prod = rows.reduce((s, x) => s + x[3], 0), I = F(prod).mul(r).div(100).div(12);
      return { r, offs, amts, rows, prod, I };
    },
    make(d) {
      const x = this._data(d), P = pick(PEOPLE); if (badDp(x.I, 2)) throw new Error('retry');
      const tot = x.amts.reduce((s, a) => s + a, 0);
      const q = `${P}, a partner, made these drawings during the year ending 31 March 2026: ${x.offs.map((o, i) => `${fyDate(2025, o)} ${rs(x.amts[i])}`).join('; ')}. Interest on drawings is ${x.r}% p.a. Using the product method, find the interest on drawings.`;
      const steps = [...x.rows.map(([o, a, m, p]) => `${fyDate(2025, o)}: ${ind(a)} × ${m} = ${ind(p)}`), `Sum of products = ${ind(x.prod)}`, `Interest: ${ind(x.prod)} × ${x.r}% × 1/12 = ${rs(x.I)}`];
      return QI(q, build(x.I, [F(tot).mul(x.r).div(100), F(tot).mul(x.r).div(100).div(2), F(x.rows.reduce((s, [o, a]) => s + a * (o + 1), 0)).mul(x.r).div(1200), F(x.prod).mul(x.r).div(100)], rs), 'Product method: multiply each drawing by the months from the date of withdrawal to the year end, add the products and charge interest for one month on the total.', steps.length > 7 ? steps.slice(-4) : steps, { r: x.r, offs: x.offs, amts: x.amts });
    },
    desc(d) {
      const x = this._data(d === 'easy' ? 'moderate' : d), P = pick(PEOPLE); if (badDp(x.I, 2)) throw new Error('retry');
      const rows = x.rows.map(([o, a, m, p]) => [fyDate(2025, o), ind(a), String(m), ind(p)]); rows.push(['Total', ind(x.amts.reduce((s, a) => s + a, 0)), '', ind(x.prod)]);
      const marks = 4, scheme = [{ id: 's1', pt: 'Months correctly counted from each date to 31 March', m: 1, skill: 'computation' }, { id: 's2', pt: `Products and their total ${ind(x.prod)}`, m: 1, skill: 'computation' }, { id: 's3', pt: `Interest ${ind(x.prod)} × ${x.r}% × 1/12 = ${rs(x.I)}`, m: 1, skill: 'computation' }, { id: 's4', pt: 'Table with date, amount, months and product neatly shown', m: 1, skill: 'presentation' }];
      const q = `${P}, a partner, made these drawings during the year ending 31 March 2026: ${x.offs.map((o, i) => `${fyDate(2025, o)} ${rs(x.amts[i])}`).join('; ')}. Interest on drawings is charged at ${x.r}% p.a. Calculate the interest on drawings using the product method.`;
      return { kind: 'desc', marks, minutes: 7, pad: 'table', q, given: [], model: [{ t: 'table', head: ['Date', 'Amount (₹)', 'Months to 31 March', 'Product (₹)'], rows, num: [1, 3] }, { t: 'p', text: `Interest on drawings = ₹${ind(x.prod)} × ${x.r}/100 × 1/12 = ${rs(x.I)}` }],
        scheme, steps: [...x.rows.map(([o, a, m, p]) => `${fyDate(2025, o)}: ${ind(a)} × ${m} = ${ind(p)}`), `Interest: ${ind(x.prod)} × ${x.r}% × 1/12 = ${rs(x.I)}`], answer: rs(x.I), data: { r: x.r, offs: x.offs, amts: x.amts } };
    } });

  def({ id: 'p1_appropriation', unit: U('p1-ch10-u01'), name: 'Profit and loss appropriation', concept: 'Salary and interest before sharing profit', kinds: ['mcq', 'desc'],
    desc(d) {
      for (let t = 0; t < 50; t++) { let x; try { x = this.make(d); } catch (e) { continue; } const { ra, rb, NP, sal, ca, cb, r } = x.data, ia = F(ca).mul(r).div(100), ib = F(cb).mul(r).div(100), rem = F(NP).sub(sal).sub(ia).sub(ib), sa = rem.mul(ra).div(ra + rb), sb = rem.sub(sa);
        if (badDp(sa, 2) || badDp(sb, 2)) continue; const [A, B] = x.q.match(/^(\S+) and (\S+) share/).slice(1);
        const rows = [[`To Salary — ${A}`, num(sal), 'By Net profit b/d', ind(NP)], [`To Interest on capital — ${A}`, num(ia), '', ''], [`To Interest on capital — ${B}`, num(ib), '', ''], [`To Profit transferred — ${A} (${ra}/${ra + rb})`, num(sa), '', ''], [`To Profit transferred — ${B} (${rb}/${ra + rb})`, num(sb), '', ''], ['Total', ind(NP), 'Total', ind(NP)]];
        const scheme = [{ id: 's1', pt: `Salary to ${A} ${rs(sal)}`, m: 1, skill: 'computation' }, { id: 's2', pt: `Interest on capital ${rs(ia)} and ${rs(ib)}`, m: 1, skill: 'computation' }, { id: 's3', pt: `Divisible profit ${rs(rem)}`, m: 1, skill: 'computation' }, { id: 's4', pt: `Shares ${rs(sa)} and ${rs(sb)} in ${ra} : ${rb}`, m: 1, skill: 'application' }, { id: 's5', pt: 'Profit and Loss Appropriation Account in To/By format with totals agreeing', m: 1, skill: 'presentation' }];
        return { kind: 'desc', marks: 5, minutes: 9, pad: 'table', q: x.q.replace(/ (What is|What total amount)[^?]*\?$/, ' Prepare the Profit and Loss Appropriation Account for the year.'), given: [], model: [{ t: 'table', head: ['Dr. Particulars', '₹', 'Cr. Particulars', '₹'], rows }], scheme, steps: x.steps.slice(0, 3), answer: `${A} ${rs(sa)}; ${B} ${rs(sb)}`, data: x.data }; }
      throw new Error('retry');
    },
    make(d) {
      const [A, B] = sample(PEOPLE, 2), [ra, rb] = pick(RATIOS2), NP = RS(200000, 1500000, 1000), sal = RS(5000, 40000, 1000) * 12, ca = RS(200000, 1000000, 10000), cb = RS(200000, 1000000, 10000), r = pick([5, 6, 8, 10]);
      const ia = F(ca).mul(r).div(100), ib = F(cb).mul(r).div(100), rem = F(NP).sub(sal).sub(ia).sub(ib); if (rem.sign <= 0) throw new Error('retry');
      const sa = rem.mul(ra).div(ra + rb); if (badDp(sa, 2)) throw new Error('retry');
      const ask = pick(['share', 'total']), corr = ask === 'share' ? sa : sa.add(sal).add(ia);
      const q = `${A} and ${B} share profits ${ra} : ${rb}. Capitals: ${A} ${rs(ca)}, ${B} ${rs(cb)}. Interest on capital ${r}% p.a.; ${A} gets a salary of ${rs(sal / 12)} per month. Net profit before these items is ${rs(NP)}. ${ask === 'share' ? `What is ${poss(A)} share of the divisible profit?` : `What total amount is credited to ${A} from the appropriation account?`}`;
      const steps = [`Salary to ${A}: ${ind(sal / 12)} × 12 = ${rs(sal)}`, `Interest on capital: ${A} ${ind(ca)} × ${r}% = ${rs(ia)}; ${B} ${ind(cb)} × ${r}% = ${rs(ib)}`, `Divisible profit: ${ind(NP)} − ${ind(sal)} − ${num(ia)} − ${num(ib)} = ${rs(rem)}`, `${poss(A)} share: ${num(rem)} × ${ra}/${ra + rb} = ${rs(sa)}`];
      if (ask === 'total') steps.push(`Total to ${A}: ${num(sa)} + ${ind(sal)} + ${num(ia)} = ${rs(corr)}`);
      const share2 = F(NP).mul(ra).div(ra + rb), noSal = F(NP).sub(ia).sub(ib).mul(ra).div(ra + rb);
      return QI(q, build(corr, ask === 'share' ? [share2, noSal, rem.mul(rb).div(ra + rb), rem.div(2)] : [sa, share2.add(sal).add(ia), corr.add(ib), noSal.add(sal).add(ia)], rs), 'Salary and interest on capital are appropriations made before sharing: deduct them from net profit, then divide the balance in the profit-sharing ratio.', steps, { ra, rb, NP, sal, ca, cb, r, ask });
    } });

  def({ id: 'p1_goodwill', unit: U('p1-ch10-u02'), name: 'Valuation of goodwill', concept: 'Average, super profit and capitalisation methods',
    make(d) {
      const meth = pick(['avg', 'wavg', 'super', 'cap_avg', 'cap_super']), n = meth === 'wavg' ? 3 : R(3, 5), pr = Array.from({ length: n }, () => RS(40000, 300000, 1000));
      if (d !== 'easy' && meth === 'avg' && chance(.4)) pr[R(0, n - 1)] = -RS(10000, 40000, 1000);
      const abn = meth === 'avg' && chance(.4) ? [R(0, n - 1), RS(5000, 30000, 1000)] : null;     // abnormal loss included in that year's profit
      const adj = pr.map((p, i) => abn && abn[0] === i ? p + abn[1] : p);
      const avg = meth === 'wavg' ? F(adj[0] * 1 + adj[1] * 2 + adj[2] * 3, 6) : F(adj.reduce((s, p) => s + p, 0), n);
      const yp = pick([F(2), F(3), F(5, 2), F(4)]), CE = RS(300000, 2000000, 10000), nrr = pick([8, 10, 12, 15, 20]);
      let gw, steps = [], wr = [];
      const yrs = pr.map((p, i) => `Year ${i + 1}: ${p < 0 ? 'loss ' + rs(-p) : rs(p)}`).join('; ');
      let q = `Profits of a firm for the last ${n} years: ${yrs}.${abn ? ` Year ${abn[0] + 1}'s figure is after an abnormal loss of ${rs(abn[1])}.` : ''} `;
      steps.push(abn ? `Add back abnormal loss to Year ${abn[0] + 1}: ${ind(pr[abn[0]])} + ${ind(abn[1])} = ${rs(adj[abn[0]])}` : null);
      steps.push(meth === 'wavg' ? `Weighted average (weights 1, 2, 3): (${ind(adj[0])} × 1 + ${ind(adj[1])} × 2 + ${ind(adj[2])} × 3) ÷ 6 = ${num(avg)}` : `Average profit: (${adj.map(p => pn(p)).join(' + ')}) ÷ ${n} = ${num(avg)}`);
      const plainAvg = F(pr.reduce((s, p) => s + p, 0), n);
      if (meth === 'avg' || meth === 'wavg') { q += `Goodwill is valued at ${num(yp)} years' purchase of the ${meth === 'wavg' ? 'weighted average profit (weights 1, 2 and 3, the latest year getting 3)' : 'average profit'}. Find goodwill.`; gw = avg.mul(yp); steps.push(`Goodwill: ${num(avg)} × ${num(yp)} = ${num(gw)}`); wr = [plainAvg.mul(yp), avg, avg.mul(yp.add(1)), F(adj.reduce((s, p) => s + p, 0), 6).mul(yp)]; }
      else {
        const sp = avg.sub(F(CE).mul(nrr).div(100));
        if (meth === 'super') { q += `Capital employed ${rs(CE)}; normal rate of return ${nrr}%. Goodwill is ${num(yp)} years' purchase of super profit. Find goodwill.`; gw = sp.mul(yp); steps.push(`Normal profit: ${ind(CE)} × ${nrr}% = ${num(F(CE).mul(nrr).div(100))}`, `Super profit: ${num(avg)} − ${num(F(CE).mul(nrr).div(100))} = ${num(sp)}`, `Goodwill: ${num(sp)} × ${num(yp)} = ${num(gw)}`); wr = [avg.mul(yp), sp, sp.mul(100).div(nrr), F(CE).mul(nrr).div(100).mul(yp)]; }
        else if (meth === 'cap_avg') { q += `Net assets (capital employed) ${rs(CE)}; normal rate of return ${nrr}%. Find goodwill by capitalising the average profit.`; const cv = avg.mul(100).div(nrr); gw = cv.sub(CE); steps.push(`Capitalised value: ${num(avg)} × 100/${nrr} = ${num(cv)}`, `Goodwill: ${num(cv)} − ${ind(CE)} = ${num(gw)}`); wr = [cv, sp.mul(100).div(nrr).mul(2), avg.mul(nrr).div(100), cv.add(CE)]; }
        else { q += `Capital employed ${rs(CE)}; normal rate of return ${nrr}%. Find goodwill by capitalising the super profit.`; gw = sp.mul(100).div(nrr); steps.push(`Super profit: ${num(avg)} − ${ind(CE)} × ${nrr}% = ${num(sp)}`, `Goodwill: ${num(sp)} × 100/${nrr} = ${num(gw)}`); wr = [avg.mul(100).div(nrr), sp.mul(3), sp.mul(nrr).div(100), avg.mul(100).div(nrr).sub(CE).add(sp)]; }
      }
      if (gw.sign <= 0 || badDp(gw, 2) || badDp(avg, 4)) throw new Error('retry');
      return QI(q, build(gw, wr, rs, { ok: x => F(x).sign > 0 }), 'Average profit method: goodwill = average (normal) profit × years’ purchase. Super profit = average profit − normal return on capital employed. Capitalisation: average profit × 100/NRR − net assets, or super profit × 100/NRR.', steps.filter(Boolean), { meth, pr, abn, yp: num(yp), CE, nrr });
    } });

  function newRatioAdm(old, s, mode, give) {        // old [ints], s Fx share of new partner; returns [Fx...] new shares incl. new partner
    const tot = old.reduce((a, b) => a + b, 0), sh = old.map(o => F(o, tot));
    if (mode === 'old') return [...sh.map(x => x.mul(F(1).sub(s))), s];
    if (mode === 'equal') return [...sh.map(x => x.sub(s.div(old.length))), s];
    return [...sh.map((x, i) => x.sub(give[i])), s];
  }
  def({ id: 'p1_admission_ratio', unit: U('p1-ch10-u03'), name: 'New and sacrificing ratio on admission', concept: 'Profit-sharing ratios on admission',
    make(d) {
      const two = d === 'easy' || chance(.6), old = two ? pick(RATIOS2) : pick(RATIOS3), names = pick(PSETS).slice(0, old.length + 1), C = names[old.length], s = pick([F(1, 4), F(1, 5), F(1, 3), F(1, 6), F(2, 7), F(1, 8)]);
      const mode = pick(two ? ['old', 'given', 'given'] : ['old', 'given', 'equal']), ask = mode === 'given' && chance(.5) ? 'sac' : 'new';
      let give = null; if (mode === 'given') { const a = pick([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4)]); give = old.length === 2 ? [s.mul(a), s.mul(F(1).sub(a))] : [s.mul(a), s.mul(F(1).sub(a)).div(2), s.mul(F(1).sub(a)).div(2)]; }
      const nr = newRatioAdm(old, s, mode, give); if (nr.some(x => x.sign <= 0)) throw new Error('retry');
      const tot = old.reduce((a, b) => a + b, 0);
      const corr = ask === 'new' ? ratio(nr) : ratio(give);
      const oldN = old.length === 2 ? `${names[0]} and ${names[1]}` : `${names[0]}, ${names[1]} and ${names[2]}`;
      const q = `${oldN} share profits ${rStr(old)}. ${C} is admitted for a ${fr(s)} share` + (mode === 'old' ? ', which the old partners give up in their old ratio.' : mode === 'equal' ? ', which the old partners give up equally.' : `, getting ${give.map((g, i) => `${fr(g)} from ${names[i]}`).join(' and ')}.`) + (ask === 'new' ? ` What is the new profit-sharing ratio (${names.join(' : ')})?` : ` What is the sacrificing ratio (${names.slice(0, old.length).join(' : ')})?`);
      const steps = [`Old shares: ${old.map((o, i) => `${names[i]} ${o}/${tot}`).join(', ')}`];
      if (mode === 'old') steps.push(`Remaining share: 1 − ${fr(s)} = ${fr(F(1).sub(s))}`, ...old.map((o, i) => `${names[i]}: ${o}/${tot} × ${fr(F(1).sub(s))} = ${fr(nr[i])}`));
      else if (mode === 'equal') steps.push(`Each gives up ${fr(s)} ÷ ${old.length} = ${fr(s.div(old.length))}`, ...old.map((o, i) => `${names[i]}: ${o}/${tot} − ${fr(s.div(old.length))} = ${fr(nr[i])}`));
      else steps.push(...old.map((o, i) => `${names[i]}: ${o}/${tot} − ${fr(give[i])} = ${fr(nr[i])}`));
      steps.push(ask === 'new' ? `${C} gets ${fr(s)}, so the new ratio is ${corr}` : `Sacrifices ${give.map((g, i) => `${names[i]} ${fr(g)}`).join(', ')}, so the sacrificing ratio is ${corr}`);
      const wrong = ask === 'new' ? [[...old, 1], old.map(o => F(o, tot)).concat([s]), [...old.map(o => F(o, tot).sub(s.div(old.length))), s], [...old.map(o => F(o, tot).mul(F(1).sub(s))), s], nr.slice(0, -1).reverse().concat([s])] : [old, nr.slice(0, -1), give.slice().reverse(), old.map(() => 1)];
      return QI(q, build(corr, wrong.map(w => { try { return ratio(w); } catch (e) { return null; } }), x => x), 'New share of an old partner = old share − share given up. Sacrificing ratio = old share − new share for each old partner.', steps.slice(0, 7), { old, s: fr(s), mode, give: give && give.map(fr), ask });
    } });

  def({ id: 'p1_gaining_ratio', unit: U('p1-ch10-u04'), name: 'Gaining ratio on retirement', concept: 'Gaining ratio',
    make(d) {
      const old = pick(RATIOS3), [A, B, C] = pick(PSETS), tot = old[0] + old[1] + old[2], given = chance(.6);
      let nA, nB; if (given) { const nr = pick([[1, 1], [3, 2], [2, 1], [5, 3], [3, 1], [2, 3], [4, 3], [5, 2]]); nA = F(nr[0], nr[0] + nr[1]); nB = F(nr[1], nr[0] + nr[1]); } else { nA = F(old[0], old[0] + old[1]); nB = F(old[1], old[0] + old[1]); }
      const gA = nA.sub(F(old[0], tot)), gB = nB.sub(F(old[1], tot)); if (gA.sign <= 0 || gB.sign <= 0) throw new Error('retry');
      const corr = ratio([gA, gB]);
      const q = `${A}, ${B} and ${C} share profits ${rStr(old)}. ${C} retires.${given ? ` ${A} and ${B} will share future profits ${ratio([nA, nB])}.` : ` ${A} and ${B} continue to share in their old ratio.`} What is the gaining ratio of ${A} and ${B}?`;
      const steps = [`New shares: ${A} ${fr(nA)}, ${B} ${fr(nB)}`, `${A}: ${fr(nA)} − ${old[0]}/${tot} = ${fr(gA)}`, `${B}: ${fr(nB)} − ${old[1]}/${tot} = ${fr(gB)}`, `So the gaining ratio is ${corr}`];
      return QI(q, build(corr, [[old[0], old[1]], [nA, nB], [nB, nA], [gB, gA], [1, 1]].map(w => { try { return ratio(w); } catch (e) { return null; } }), x => x), 'Gaining ratio = new share − old share for each continuing partner. If they continue in their old ratio, the gaining ratio equals their old ratio.', steps, { old, given, nA: fr(nA), nB: fr(nB) });
    } });

  def({ id: 'p1_revaluation', unit: U('p1-ch10-u03'), name: 'Revaluation account', concept: 'Revaluation profit or loss',
    make(d) {
      const old = pick(RATIOS2), [A, B] = sample(PEOPLE, 2), bl = RS(200000, 1500000, 10000), bu = pick([10, 15, 20, 25]), mc = RS(100000, 800000, 10000), md = pick([5, 10, 15, 20]), deb = RS(50000, 400000, 1000), pp = pick([2, 5, 10]), ol = RS(2000, 30000, 1000), stk = RS(0, 20000, 1000);
      const items = [['Building appreciated by ' + bu + '%', F(bl).mul(bu).div(100)], ['Machinery depreciated by ' + md + '%', F(mc).mul(md).div(100).neg()], [`Provision for doubtful debts @ ${pp}% on trade receivables`, F(deb).mul(pp).div(100).neg()], ['Outstanding electricity bill not recorded', F(ol).neg()]];
      if (stk) items.push(['Inventory written down', F(stk).neg()]);
      const net = sum(items.map(x => x[1])); if (!net.sign || badDp(net, 2)) throw new Error('retry');
      const ask = pick(['net', 'A']), shA = net.mul(old[0]).div(old[0] + old[1]); if (badDp(shA, 2)) throw new Error('retry');
      const q = `${A} and ${B} share profits ${rStr(old)}. On admitting a partner: building (book value ${rs(bl)}) is appreciated by ${bu}%; machinery (${rs(mc)}) is depreciated by ${md}%; a provision of ${pp}% is created on trade receivables of ${rs(deb)}; an outstanding electricity bill of ${rs(ol)} is to be recorded${stk ? `; inventory is written down by ${rs(stk)}` : ''}. ${ask === 'net' ? 'What is the profit or loss on revaluation?' : `What is ${poss(A)} share of the revaluation profit or loss?`}`;
      const steps = items.map(([t, v]) => `${t}: ${v.sign > 0 ? 'gain' : 'loss'} ${rs(v.abs())}`); steps.push(`Net: ${items.map(([t, v]) => (v.sign > 0 ? '+' : '−') + ' ' + num(v.abs())).join(' ').replace(/^\+ /, '')} = ${num(net)}`);
      if (ask === 'A') steps.push(`${poss(A)} share: ${num(net)} × ${old[0]}/${old[0] + old[1]} = ${num(shA)}`);
      const corr = ask === 'net' ? net : shA, gains = sum(items.filter(x => x[1].sign > 0).map(x => x[1])), losses = sum(items.filter(x => x[1].sign < 0).map(x => x[1]));
      const wr = ask === 'net' ? [net.neg(), gains.add(losses.sub(F(-ol))), gains, net.sub(F(ol).mul(2).neg())] : [shA.neg(), net.mul(old[1]).div(old[0] + old[1]), net, net.div(2)];
      return QI(q, build(corr, wr, v => PorL(v), { ok: v => F(v).sign !== 0 }), 'Increases in assets and decreases in liabilities are gains; decreases in assets, new provisions and unrecorded liabilities are losses. The net result is shared by the old partners in the old ratio.', steps, { old, bl, bu, mc, md, deb, pp, ol, stk, ask });
    } });

  def({ id: 'p1_retire_goodwill', unit: U('p1-ch10-u04'), name: 'Goodwill on retirement', concept: 'Compensating the retiring partner in gaining ratio',
    make(d) {
      const old = pick(RATIOS3), [A, B, C] = pick(PSETS), tot = old[0] + old[1] + old[2], G = RS(60000, 900000, 6000), given = chance(.5);
      let nA, nB; if (given) { const nr = pick([[1, 1], [3, 2], [2, 1], [5, 3], [3, 1], [4, 3], [5, 2]]); nA = F(nr[0], nr[0] + nr[1]); nB = F(nr[1], nr[0] + nr[1]); } else { nA = F(old[0], old[0] + old[1]); nB = F(old[1], old[0] + old[1]); }
      const gA = nA.sub(F(old[0], tot)), gB = nB.sub(F(old[1], tot)); if (gA.sign <= 0 || gB.sign <= 0) throw new Error('retry');
      const cs = F(G).mul(old[2]).div(tot), dA = cs.mul(gA).div(gA.add(gB)); if (badDp(dA, 2) || badDp(cs, 2)) throw new Error('retry');
      const q = `${A}, ${B} and ${C} share profits ${rStr(old)}. ${C} retires; the firm's goodwill is valued at ${rs(G)}.${given ? ` ${A} and ${B} will share profits ${ratio([nA, nB])} in future.` : ` ${A} and ${B} continue in their old ratio.`} No goodwill account is to be raised. By how much is ${poss(A)} capital account debited for ${poss(C)} share of goodwill?`;
      const steps = [`${poss(C)} share of goodwill: ${ind(G)} × ${old[2]}/${tot} = ${rs(cs)}`, `Gaining ratio: ${A} ${fr(nA)} − ${old[0]}/${tot} = ${fr(gA)}; ${B} ${fr(nB)} − ${old[1]}/${tot} = ${fr(gB)} so the gaining ratio is ${ratio([gA, gB])}`, `${poss(A)} debit: ${num(cs)} × ${fr(gA.div(gA.add(gB)))} = ${rs(dA)}`];
      return QI(q, build(dA, [cs.mul(old[0]).div(old[0] + old[1]), cs.mul(nA), F(G).mul(gA), cs.mul(gB).div(gA.add(gB)), cs], rs, { ok: x => F(x).sign > 0 }), 'The retiring partner is credited with his share of goodwill and the continuing partners are debited in their gaining ratio (new share − old share).', steps, { old, G, given, nA: fr(nA), nB: fr(nB) });
    } });

  def({ id: 'p1_death_profit', unit: U('p1-ch10-u05'), name: 'Deceased partner’s share of profit', concept: 'Profit up to the date of death',
    make(d) {
      const old = pick(RATIOS3), [A, B, C] = sample(PEOPLE, 3), tot = old[0] + old[1] + old[2], basis = pick(['last', 'avg']), pr = Array.from({ length: 3 }, () => RS(60000, 600000, 1000)), off = R(1, 11);
      const base = basis === 'last' ? F(pr[2]) : F(pr[0] + pr[1] + pr[2], 3), sh = base.mul(off).div(12).mul(old[2]).div(tot); if (badDp(sh, 2)) throw new Error('retry');
      const q = `${A}, ${B} and ${C} share profits ${rStr(old)}; books close on 31 March. ${C} died on ${fyDate(2025, off) .replace(/^1 /, '1 ')}. ${poss(C)} share of profit up to the date of death is to be based on ${basis === 'last' ? 'the previous year’s profit' : 'the average profit of the last three years'}. Profits: 2022-23 ${rs(pr[0])}, 2023-24 ${rs(pr[1])}, 2024-25 ${rs(pr[2])}. Find ${poss(C)} share of profit.`;
      const steps = [basis === 'last' ? `Base profit (2024-25) = ${rs(base)}` : `Average profit: (${ind(pr[0])} + ${ind(pr[1])} + ${ind(pr[2])}) ÷ 3 = ${num(base)}`, `Period from 1 April 2025 to the date of death: ${off} months`, `Share: ${num(base)} × ${off}/12 × ${old[2]}/${tot} = ${rs(sh)}`];
      return QI(q, build(sh, [base.mul(old[2]).div(tot), base.mul(off + 1).div(12).mul(old[2]).div(tot), (basis === 'last' ? F(pr[0] + pr[1] + pr[2], 3) : F(pr[2])).mul(off).div(12).mul(old[2]).div(tot), base.mul(12 - off).div(12).mul(old[2]).div(tot)], rs, { ok: x => F(x).sign > 0 }), 'The deceased partner gets a share of profit for the part of the year up to death, on the agreed basis (last year’s profit, average profit, or sales), in the profit-sharing ratio.', steps, { old, basis, pr, off });
    } });

  def({ id: 'p1_realisation', unit: U('p1-ch10-u06'), name: 'Realisation profit or loss', concept: 'Realisation account on dissolution',
    make(d) {
      const Bv = RS(200000, 1500000, 10000), Rv = Math.round(Bv * R(70, 115) / 100 / 1000) * 1000, Lb = RS(50000, 500000, 1000), Lp = Lb - RS(0, Math.round(Lb * .1 / 500), 1) * 500, e = RS(2000, 25000, 500);
      const pl = Rv - Bv + Lb - Lp - e; if (pl === 0) throw new Error('retry');
      const q = `On dissolution, assets (other than cash) with a book value of ${rs(Bv)} realised ${rs(Rv)}. Creditors of ${rs(Lb)} were paid ${rs(Lp)} in full settlement. Realisation expenses were ${rs(e)}. What is the profit or loss on realisation?`;
      const steps = [`On assets: ${ind(Rv)} − ${ind(Bv)} = ${Rv - Bv < 0 ? '−' : ''}${ind(Math.abs(Rv - Bv))}`, `Discount on creditors: ${ind(Lb)} − ${ind(Lp)} = ${ind(Lb - Lp)}`, `Net: ${Rv - Bv < 0 ? '−' : ''}${ind(Math.abs(Rv - Bv))} + ${ind(Lb - Lp)} − ${ind(e)} = ${pl < 0 ? '−' : ''}${ind(Math.abs(pl))}`];
      return QI(q, build(pl, [Rv - Bv - e, Rv - Bv + Lb - Lp + e, -pl, Rv - Bv - (Lb - Lp) - e], v => PorL(v), { ok: v => v !== 0 }), 'Realisation profit = amount realised from assets − their book value + discount received from creditors − realisation expenses.', steps, { Bv, Rv, Lb, Lp, e });
    } });

  /* ---- Company accounts ---- */
  def({ id: 'p1_share_calls', unit: U('p1-ch11-u02'), name: 'Share issue — calls and arrears', concept: 'Application, allotment and calls',
    make(d) {
      const co = pick(COS), N = RS(10000, 200000, 1000), p = pick([0, 0, 1, 2, 5]), a = pick([2, 3]), c = pick([2, 3, 4]), b = 10 + p - a - c; if (b <= p) throw new Error('retry');
      const H = RS(100, Math.round(N / 20), 100), ask = pick(['callrec', 'arrears', 'total', 'premium']);
      const vals = { callrec: (N - H) * c, arrears: H * c, total: N * (10 + p) - H * c, premium: N * p }; if (ask === 'premium' && !p) throw new Error('retry');
      const q = `${co} issued ${ind(N)} equity shares of ₹10 each${p ? ` at a premium of ₹${p}` : ''}, payable ₹${a} on application, ₹${b} on allotment${p ? ` (including premium)` : ''} and ₹${c} on first and final call. All shares were subscribed and all money was received except the call on ${ind(H)} shares. ` + { callrec: 'How much was received on the first and final call?', arrears: 'What are the calls in arrears?', total: 'What total amount did the company receive?', premium: 'What amount is credited to Securities Premium?' }[ask];
      const steps = [`Issue price per share: ₹10${p ? ` + ₹${p}` : ''} = ₹${10 + p}; ${a} + ${b} + ${c} = ${a + b + c}`, `Call due: ${ind(N)} × ${c} = ${rs(N * c)}; unpaid on ${ind(H)} shares: ${ind(H)} × ${c} = ${rs(H * c)}`];
      if (ask === 'callrec') steps.push(`Received: ${ind(N * c)} − ${ind(H * c)} = ${rs(vals.callrec)}`); if (ask === 'total') steps.push(`Total: ${ind(N)} × ${10 + p} − ${ind(H * c)} = ${rs(vals.total)}`); if (ask === 'premium') steps.push(`Premium: ${ind(N)} × ${p} = ${rs(vals.premium)}`);
      const wr = { callrec: [N * c, (N - H) * (c + b), N * c + H * c], arrears: [H * (b + c), H * 10, (N - H) * c], total: [N * (10 + p), N * 10 - H * c, N * (10 + p) - H * (b + c)], premium: [(N - H) * p, N * (p + a), H * p] }[ask];
      return QI(q, build(vals[ask], wr, rs, { ok: x => x > 0 }), 'Amounts due on each instalment are credited to Share Capital (premium to Securities Premium when due). Unpaid instalments are calls in arrears, deducted from called-up capital.', steps, { N, p, a, b, c, H, ask });
    } });

  def({ id: 'p1_forfeit', unit: U('p1-ch11-u02'), name: 'Forfeiture and reissue — capital reserve', concept: 'Gain on reissue of forfeited shares',
    make(d) {
      const H = RS(100, 2000, 100), x = pick([3, 4, 5, 6, 7, 8]), K = d === 'easy' ? H : RS(100, H, 100), z = pick([6, 7, 8, 9, 10]); const disc = 10 - z; if (disc > x) throw new Error('retry');
      const cr = K * x - K * disc;
      const q = `${ind(H)} equity shares of ₹10 each, on which ₹${x} per share had been paid, were forfeited. ${K === H ? 'All of these' : ind(K) + ' of these'} shares were reissued as fully paid at ₹${z} per share. What amount is transferred to Capital Reserve?`;
      const steps = [`Amount forfeited (₹${x} per share) on the ${K === H ? '' : 'reissued '}shares: ${ind(K)} × ${x} = ${rs(K * x)}`, `Discount on reissue: ${ind(K)} × (10 − ${z}) = ${rs(K * disc)}`, `Capital reserve: ${ind(K * x)} − ${ind(K * disc)} = ${rs(cr)}`];
      return QI(q, build(cr, [H * x - K * disc, K * x, K * (x + disc), H * x, K * z - K * x], rs, { ok: v => v > 0 }), 'Share Forfeiture account is credited with the amount already paid. On reissue, any discount is met from it; the balance relating to the reissued shares is transferred to Capital Reserve.', steps, { H, x, K, z });
    } });

  def({ id: 'p1_debentures', unit: U('p1-ch11-u03'), name: 'Debentures — interest and loss on issue', concept: 'Issue and interest on debentures',
    make(d) {
      const co = pick(COS), N = RS(1000, 50000, 500), r = pick([8, 9, 10, 11, 12]), ask = pick(['interest', 'loss']);
      if (ask === 'interest') {
        const off = R(0, 9), I = F(N * 100).mul(r).div(100).mul(12 - off).div(12); if (badDp(I, 2)) throw new Error('retry');
        const q = `${co} issued ${ind(N)}, ${r}% debentures of ₹100 each on ${fyDate(2025, off)}. What is the debenture interest for the year ending 31 March 2026?`;
        const steps = [`Face value: ${ind(N)} × 100 = ${rs(N * 100)}`, `Interest for ${PL(12 - off, 'month')}: ${ind(N * 100)} × ${r}% × ${12 - off}/12 = ${rs(I)}`];
        return QI(q, build(I, [F(N * 100).mul(r).div(100), F(N * 100).mul(r).div(100).mul(off).div(12), F(N * 100).mul(r).div(100).mul(13 - off).div(12)], rs, { ok: x => F(x).sign > 0 }), 'Interest is always calculated on the face (nominal) value of debentures, for the period they were outstanding.', steps, { N, r, off, ask });
      }
      const dsc = pick([0, 2, 5, 10]), prem = pick([0, 5, 10]), red = pick([0, 5, 10]); if (!(dsc + red) || (dsc && prem)) throw new Error('retry');
      const iss = prem ? `at a premium of ${prem}%` : dsc ? `at a discount of ${dsc}%` : 'at par', loss = N * (dsc + red);
      const q = `${co} issued ${ind(N)}, ${r}% debentures of ₹100 each ${iss}, redeemable ${red ? `at a premium of ${red}%` : 'at par'}. What amount is debited to Loss on Issue of Debentures?`;
      const steps = [`Discount on issue per debenture: ₹${dsc}; premium payable on redemption: ₹${red}`, `Loss on issue: ${ind(N)} × (${dsc} + ${red}) = ${rs(loss)}`]; if (prem) steps.splice(1, 0, `Premium on issue (₹${prem} each) is credited to Securities Premium, not set off here`);
      return QI(q, build(loss, [N * dsc, N * red, N * (dsc + red + prem), N * Math.abs(red - prem), N * 100], rs, { ok: x => x > 0 }), 'Loss on issue of debentures = discount allowed on issue + premium payable on redemption. Premium received on issue goes to Securities Premium.', steps, { N, r, dsc, prem, red, ask });
    } });

  def({ id: 'p1_bonus_right', unit: U('p1-ch11-u04'), name: 'Bonus and right issue', concept: 'Bonus shares and value of a right',
    make(d) {
      const ask = pick(['bonus', 'right']);
      if (ask === 'bonus') {
        const S = RS(100000, 5000000, 10000), k = pick([2, 4, 5, 10]), fv = 10; if (S % k) throw new Error('retry');
        const B = S / k, cap = B * fv;
        const q = `A company has ${ind(S)} equity shares of ₹10 each, fully paid. It issues bonus shares in the ratio of 1 for every ${k} held, out of its general reserve. What amount of reserve is capitalised?`;
        const steps = [`Bonus shares: ${ind(S)} ÷ ${k} = ${ind(B)}`, `Amount capitalised: ${ind(B)} × 10 = ${rs(cap)}`];
        return QI(q, build(cap, [B, S * fv / (k + 1), S * fv, cap * 2], rs, { ok: x => x > 0 && Number.isInteger(x) }), 'Bonus shares are fully paid shares issued free to existing holders by capitalising reserves: number of bonus shares × face value.', steps, { ask, S, k });
      }
      const MV = RS(50, 600, 5), IP = RS(10, MV - 10, 5), k = pick([1, 2, 3, 4, 5]);
      const ex = F(MV * k + IP, k + 1), vr = F(MV).sub(ex); if (badDp(vr, 2)) throw new Error('retry');
      const q = `A share has a market price of ₹${MV} cum-right. The company offers 1 new share for every ${k} held at ₹${IP} per share. What is the theoretical value of a right?`;
      const steps = [`Ex-right value: (${MV} × ${k} + ${IP}) ÷ ${k + 1} = ${num(ex)}`, `Value of a right: ${MV} − ${num(ex)} = ${num(vr)}`];
      return QI(q, build(vr, [F(MV - IP), F(MV - IP, k), ex, vr.mul(k)], x => rs(x), { ok: x => F(x).sign > 0 }), 'Ex-right value = (market value of existing shares + amount paid for new shares) ÷ total shares after the issue. Value of right = cum-right price − ex-right price.', steps, { ask, MV, IP, k });
    } });

  /* =====================================================================================
     PAPER 3 — QUANTITATIVE APTITUDE
     ===================================================================================== */
  const P3 = s => U('p3-' + s);
  const nf = x => num(x);
  const buildN = (c, w, o) => build(c, w, nf, o);

  def({ id: 'q_ratio', unit: P3('ch01-u01'), name: 'Ratio', concept: 'Dividing in a ratio; compounded and duplicate ratios',
    make(d) {
      const v = pick(['divide', 'chain', 'dup', 'inverse']);
      if (v === 'divide') {
        const r = pick([[2, 3, 5], [3, 4, 5], [1, 2, 3], [4, 5, 6], [2, 5, 7], [3, 5, 8]]), s = r[0] + r[1] + r[2], T = RS(s * 100, s * 20000, s * 100), who = R(0, 2), [A, B, C] = sample(PEOPLE, 3), nm = [A, B, C];
        const sh = F(T).mul(r[who]).div(s);
        return QI(`${rs(T)} is divided among ${A}, ${B} and ${C} in the ratio ${rStr(r)}. What is ${nm[who]}'s share?`, build(sh, [F(T).div(3), F(T).mul(r[(who + 1) % 3]).div(s), F(T).mul(r[who]).div(s - r[who]), F(T).mul(r[who]).div(10)], rs),
          'Share = total × (own part ÷ sum of parts).', [`Sum of parts: ${r.join(' + ')} = ${s}`, `${nm[who]}: ${ind(T)} × ${r[who]}/${s} = ${rs(sh)}`], { v, r, T, who });
      }
      if (v === 'chain') {
        const p = R(1, 9), q = R(1, 9), r2 = R(1, 9), s2 = R(1, 9); if (gcdN(p, q) !== 1 || gcdN(r2, s2) !== 1 || p === q || r2 === s2) throw new Error('retry');
        const corr = ratio([F(p * r2), F(q * r2), F(q * s2)]);
        return QI(`If A : B = ${p} : ${q} and B : C = ${r2} : ${s2}, find A : B : C.`, buildS(corr, [[p, q, s2], [p * s2, q * r2, q * s2], [p, q * r2, s2], [p * r2, q * s2, q * r2]].map(w => { try { return ratio(w.map(x => F(x))); } catch (e) { return null; } })),
          'Make the common term B equal in both ratios, then read off A : B : C.', [`Multiply A : B by ${r2} and B : C by ${q}`, `A : B = ${p * r2} : ${q * r2}; B : C = ${q * r2} : ${q * s2}`, `A : B : C = ${p * r2} : ${q * r2} : ${q * s2}`], { v, p, q, r2, s2 });
      }
      if (v === 'dup') {
        const a = R(2, 9), b = R(2, 9), t = pick(['duplicate', 'triplicate', 'sub-duplicate', 'sub-triplicate']); if (a === b || gcdN(a, b) !== 1) throw new Error('retry');
        const [x, y] = t === 'sub-duplicate' ? [a * a, b * b] : t === 'sub-triplicate' ? [a ** 3, b ** 3] : [a, b];
        const corr = t === 'duplicate' ? `${a * a} : ${b * b}` : t === 'triplicate' ? `${a ** 3} : ${b ** 3}` : `${a} : ${b}`;
        const wr = [`${2 * x} : ${2 * y}`, `${x * x} : ${y * y}`, `${b} : ${a}`, `${a * a} : ${b * b}`, `${a ** 3} : ${b ** 3}`, `${x * 3} : ${y * 3}`];
        return QI(`What is the ${t} ratio of ${x} : ${y}?`, buildS(corr, wr), 'Duplicate ratio squares the terms, triplicate cubes them; sub-duplicate takes square roots, sub-triplicate cube roots.', [`${t[0].toUpperCase() + t.slice(1)} ratio: ${t.startsWith('sub') ? (t === 'sub-duplicate' ? 'square roots' : 'cube roots') : t === 'duplicate' ? 'squares' : 'cubes'} of the terms`, `= ${corr}`], { v, a, b, t });
      }
      const r = pick([[2, 3], [3, 4], [2, 5], [3, 5], [4, 5]]), T = RS(1000, 90000, (r[0] + r[1]) * 10), sh = F(T).mul(r[1]).div(r[0] + r[1]);
      return QI(`Divide ${rs(T)} between P and Q in the inverse ratio of ${r[0]} : ${r[1]}. What does P get?`, build(sh, [F(T).mul(r[0]).div(r[0] + r[1]), F(T).div(2), F(T).mul(r[1]).div(r[0] * r[1])], rs, { ok: x => dpOf(F(x)) <= 2 }), 'Inverse ratio of a : b is 1/a : 1/b = b : a.', [`The inverse ratio of ${r[0]} : ${r[1]} is 1/${r[0]} : 1/${r[1]}, i.e. ${r[1]} : ${r[0]}`, `P: ${ind(T)} × ${r[1]}/${r[0] + r[1]} = ${rs(sh)}`], { v, r, T });
    } });

  def({ id: 'q_proportion', unit: P3('ch01-u01'), name: 'Proportion', concept: 'Fourth, third and mean proportional',
    make(d) {
      const v = pick(['fourth', 'third', 'mean']);
      if (v === 'fourth') { const a = R(2, 12), b = R(2, 20), k = R(2, 9), c = a * k, x = F(b * c, a); return QI(`Find the fourth proportional to ${a}, ${b} and ${c}.`, buildN(x, [F(a * c, b), F(b * b, a), F(a * b, c), x.add(a)]), 'If a : b = c : x then x = bc/a.', [`${a} : ${b} = ${c} : x`, `x = ${b} × ${c} ÷ ${a} = ${nf(x)}`], { v, a, b, c }); }
      if (v === 'third') { const a = R(2, 9), k = R(2, 6), b = a * k, x = F(b * b, a); return QI(`Find the third proportional to ${a} and ${b}.`, buildN(x, [F(a * b), F(b * b), F(a * a, b), F(2 * b - a)]), 'If a : b = b : x then x = b²/a.', [`${a} : ${b} = ${b} : x`, `x = ${b} × ${b} ÷ ${a} = ${nf(x)}`], { v, a, b }); }
      const m = R(2, 15), a = pick([1, 2, 3, 4]) * 1, c = m * m * 4 % a === 0 ? m * m / a : 0; const p = R(1, 6), q = R(2, 9); const A = p * p * R(1, 3), Bq = q * q; const k = R(1, 4), X = k * p * p, Y = k * q * q; const mp = k * p * q; if (p === q) throw new Error('retry');
      return QI(`Find the mean proportional between ${X} and ${Y}.`, buildN(F(mp), [F(X + Y, 2), F(X * Y), F(mp * 2), F(Y - X).abs()]), 'Mean proportional between a and b is √(ab).', [`√(${X} × ${Y}) = √${ind(X * Y)} = ${mp}`], { v, X, Y });
    } });

  def({ id: 'q_indices', unit: P3('ch01-u01'), name: 'Indices', concept: 'Laws of indices',
    make(d) {
      const v = pick(['eval', 'solve']);
      if (v === 'eval') {
        const k = pick([2, 3, 4, 5]), qd = pick([2, 3]), pnum = R(1, 4), j = pick([2, 3, 4]), sd = pick([2, 3]); if (k ** qd > 1000 || j ** sd > 100 || gcdN(pnum, qd) > 1) throw new Error('retry');
        const base1 = k ** qd, base2 = j ** sd, val = F(k ** pnum).div(j);
        const q = `Evaluate: ${base1}^(${pnum}/${qd}) × ${base2}^(−1/${sd})`;
        return QI(q, build(val, [F(k ** pnum).mul(j), F(k ** pnum), F(base1 * pnum, qd).div(j), F(k ** pnum, j * j)], fr), 'aᵐ/ⁿ = (ⁿ√a)ᵐ and a⁻ⁿ = 1/aⁿ.', [`${base1}^(${pnum}/${qd}) = (${k}^${qd})^(${pnum}/${qd}) = ${k}^${pnum} = ${k ** pnum}`, `${base2}^(−1/${sd}) = 1/${j}`, `Product: ${k ** pnum} × 1/${j} = ${nf(val)}`], { v, k, qd, pnum, j, sd });
      }
      const b = pick([2, 3, 5]), a = R(1, 4), c = R(-5, 5), n = R(1, 12), lhs = n - c; if (lhs % a) throw new Error('retry'); const x = lhs / a, N = F(b).pow(n);
      if (N.gt(F(10).pow(8)) || !N.int) throw new Error('retry');
      const q = `If ${b}^(${a === 1 ? '' : a}x ${c < 0 ? '−' : '+'} ${Math.abs(c)}) = ${num(N)}, find x.`;
      return QI(q, buildN(F(x), [F(n, a), F(n + c, a), F(x + 1), F(n)]), 'Write both sides with the same base and equate the powers.', [`${num(N)} = ${b}^${n}`, `${a === 1 ? '' : a}x ${c < 0 ? '−' : '+'} ${Math.abs(c)} = ${n}`, `x = (${n} ${c < 0 ? '+' : '−'} ${Math.abs(c)}) ÷ ${a} = ${x}`], { v, b, a, c, n });
    } });

  def({ id: 'q_logs', unit: P3('ch01-u01'), name: 'Logarithms', concept: 'Laws of logarithms',
    make(d) {
      const v = pick(['base', 'given', 'combine']);
      if (v === 'base') { const k = pick([2, 3, 5]), i = R(1, 3), j = R(1, 6); const a = k ** i, N = k ** j; if (N > 100000) throw new Error('retry'); const val = F(j, i);
        return QI(`Find the value of log ${ind(N)} to the base ${a}.`, buildN(val, [F(i, j), F(j), F(N, a), F(j - i)]), 'logₐ N = x means aˣ = N; write both as powers of the same base.', [`${a} = ${k}${sup(i)}, ${ind(N)} = ${k}${sup(j)}`, `log = ${j}/${i} = ${nf(val)}`], { v, k, i, j }); }
      if (v === 'given') { const a = R(0, 4), b = R(0, 3), c = R(0, 2); if (a + b + c < 2) throw new Error('retry'); const N = 2 ** a * 3 ** b * 5 ** c; const val = F('0.3010').mul(a - c).add(F('0.4771').mul(b)).add(c);
        return QI(`Given log 2 = 0.3010 and log 3 = 0.4771, find log ${ind(N)}.`, build(val, [F('0.3010').mul(a).add(F('0.4771').mul(b)).add(F('0.6990').mul(c)).add('0.0010'), F('0.3010').mul(a + c).add(F('0.4771').mul(b)), F('0.3010').mul(a).mul(F('0.4771').mul(b).add(1)), val.add(1)], x => fixed(x, 4)), 'log(mn) = log m + log n; log 5 = log 10 − log 2 = 1 − 0.3010.', [`${ind(N)} = ${[a ? `2${a > 1 ? sup(a) : ''}` : '', b ? `3${b > 1 ? sup(b) : ''}` : '', c ? `5${c > 1 ? sup(c) : ''}` : ''].filter(Boolean).join(' × ')}`, `log 5 = 1 − 0.3010 = 0.6990`, [a ? `${a} × 0.3010` : '', b ? `${b} × 0.4771` : '', c ? `${c} × 0.6990` : ''].filter(Boolean).join(' + ') + ` = ${fixed(val, 4)}`], { v, a, b, c }); }
      const k = pick([2, 3, 10]), e1 = R(1, 4), e2 = R(1, 4), e3 = R(0, 3), x1 = R(2, 6), x2 = k ** e1 * x1, x3 = k ** e2, prod = e1 + e2;
      return QI(`Simplify (all logarithms to the base ${k}): log ${ind(x2)} + log ${ind(x3)} − log ${x1}`, buildN(F(prod), [F(prod + 1), F(e1), F(x2 + x3 - x1, k), F(prod - 1)]), 'log m + log n − log p = log(mn/p).', [`log m + log n − log p = log (mn/p)`, `${ind(x2)} × ${ind(x3)} ÷ ${x1} = ${ind(x2 * x3 / x1)}`, `${ind(x2 * x3 / x1)} = ${k}${sup(prod)}, so the value is ${prod}`], { v, k, e1, e2, x1 });
    } });

  def({ id: 'q_linear', unit: P3('ch02-u01'), name: 'Linear equations', concept: 'Simple equations and word problems',
    make(d) {
      const v = pick(['solve', 'ages', 'sumdiff']);
      if (v === 'solve') { const x = R(-9, 15), a = R(2, 9), c = R(1, 9), b = R(-20, 20); if (a === c) throw new Error('retry'); const dd = a * x + b - c * x;
        return QI(`Solve: ${poly([a, b])} = ${poly([c, dd])}`, buildN(F(x), [F(dd + b, a - c), F(dd - b, a + c), F(-x), F(x + 1)]), 'Collect x-terms on one side and constants on the other.', [`${a}x − ${c}x = ${pn(dd)} − ${pn(b)}`, `${a - c}x = ${dd - b}`, `x = ${dd - b} ÷ ${a - c} = ${x}`], { v, a, b, c, dd }); }
      if (v === 'ages') { const B = R(5, 30), k = R(2, 4), A = k * B, t = R(2, 15), m = F(A + t, B + t); if (!m.int || m.n < 2n) throw new Error('retry');
        return QI(`A father is ${k} times as old as his son. After ${t} years he will be ${num(m)} times as old as his son. What is the son's present age (years)?`, buildN(F(B), [F(A), F(B + t), F(A + t), F(B - t)], { ok: x => F(x).sign > 0 }), 'Let the son be x; father kx. Form the equation for the future ages.', [`(${k}x + ${t}) = ${num(m)}(x + ${t})`, `${k}x − ${num(m)}x = ${num(m)} × ${t} − ${t}`, `x = ${num(m.mul(t).sub(t))} ÷ ${num(F(k).sub(m))} = ${B}`], { v, B, k, t }); }
      const x = R(5, 99), y = R(1, x - 1), S = x + y, D = x - y;
      return QI(`The sum of two numbers is ${S} and their difference is ${D}. What is the larger number?`, buildN(F(x), [F(y), F(S + D), F(S, 2), F(D)]), 'Larger = (sum + difference)/2.', [`x + y = ${S}, x − y = ${D}`, `2x = ${S} + ${D} = ${S + D}`, `x = ${S + D} ÷ 2 = ${x}`], { v, S, D });
    } });

  def({ id: 'q_simultaneous', unit: P3('ch02-u01'), name: 'Simultaneous equations', concept: 'Two linear equations in two unknowns',
    make(d) {
      const x = R(-8, 12), y = R(-8, 12), a1 = R(1, 7), b1 = R(-6, 7), a2 = R(1, 7), b2 = R(-6, 7); const det = a1 * b2 - a2 * b1; if (!det || !b1 || !b2) throw new Error('retry');
      const c1 = a1 * x + b1 * y, c2 = a2 * x + b2 * y, ask = pick(['x', 'y', 'sum']);
      const lhs = (a, b) => `${a === 1 ? '' : a}x ${b < 0 ? '−' : '+'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}y`;
      const corr = ask === 'x' ? x : ask === 'y' ? y : x + y;
      const steps = [`Determinant: ${a1} × ${pn(b2)} − ${a2} × ${pn(b1)} = ${det}`, `x = (${pn(c1)} × ${pn(b2)} − ${pn(c2)} × ${pn(b1)}) ÷ ${pn(det)} = ${x}`, `y = (${a1} × ${pn(c2)} − ${a2} × ${pn(c1)}) ÷ ${pn(det)} = ${y}`]; if (ask === 'sum') steps.push(`x + y = ${pn(x)} + ${pn(y)} = ${x + y}`);
      return QI(`Solve: ${lhs(a1, b1)} = ${c1} and ${lhs(a2, b2)} = ${c2}. ${ask === 'sum' ? 'Find x + y.' : `Find ${ask}.`}`, buildN(F(corr), ask === 'sum' ? [F(x - y), F(x), F(y), F(x + y + 1)] : [F(ask === 'x' ? y : x), F(-corr), F(corr + 1), F(corr - 2)]), 'Use elimination or Cramer’s rule; check the answer in both equations.', steps, { x, y, a1, b1, a2, b2, ask });
    } });

  def({ id: 'q_quadratic', unit: P3('ch02-u01'), name: 'Quadratic equations', concept: 'Roots, sum and product of roots',
    make(d) {
      const r1 = R(-9, 9), r2 = R(-9, 9), a = d === 'easy' ? 1 : pick([1, 1, 2, 3]); const b = -a * (r1 + r2), c = a * r1 * r2; if (r1 === 0 && r2 === 0) throw new Error('retry');
      const eq = `${poly([a, b, c])} = 0`, v = pick(['roots', 'sum', 'prod', 'sq', 'form']);
      if (v === 'roots') { const fmt = p => `${Math.min(...p)}, ${Math.max(...p)}`.replace(/-/g, '−'); return QI(`Find the roots of ${eq}.`, buildS(fmt([r1, r2]), [fmt([-r1, -r2]), fmt([r1, -r2]), fmt([r1 + 1, r2 + 1]), fmt([-r1, r2])]), 'Factorise (or use x = [−b ± √(b² − 4ac)]/2a).', [`b² − 4ac = ${pn(b)}² − 4 × ${a} × ${pn(c)} = ${b * b - 4 * a * c}`, `x = (${pn(-b)} ± √${b * b - 4 * a * c}) ÷ ${2 * a}`, `x = ${r1} or x = ${r2}`], { v, a, r1, r2 }); }
      if (v === 'sum' || v === 'prod') { const val = v === 'sum' ? F(-b, a) : F(c, a); return QI(`For ${eq}, find the ${v === 'sum' ? 'sum' : 'product'} of the roots.`, buildN(val, v === 'sum' ? [F(b, a), F(c, a), F(-c, a)] : [F(-c, a), F(-b, a), F(b, a)]), 'Sum of roots = −b/a; product = c/a.', [v === 'sum' ? `Sum = −b/a = ${pn(-b)}/${a} = ${nf(val)}` : `Product = c/a = ${pn(c)}/${a} = ${nf(val)}`], { v, a, b, c }); }
      if (v === 'sq') { const s = F(-b, a), p = F(c, a), val = s.mul(s).sub(p.mul(2)); return QI(`If α and β are the roots of ${eq}, find α² + β².`, buildN(val, [s.mul(s), s.mul(s).add(p.mul(2)), p.mul(p), s.mul(s).sub(p)]), 'α² + β² = (α + β)² − 2αβ.', [`α + β = ${nf(s)}, αβ = ${nf(p)}`, `α² + β² = ${pn(s)}² − 2 × ${pn(p)} = ${nf(val)}`], { v, a, b, c }); }
      const E = (p, q) => `x² ${p < 0 ? '+' : '−'} ${Math.abs(p)}x ${q < 0 ? '−' : '+'} ${Math.abs(q)} = 0`.replace(/ [+−] 0x/, '').replace(/ [+−] 0 = 0/, ' = 0');
      return QI(`Which equation has roots ${r1} and ${r2}?`.replace(/-/g, '−'), buildS(E(r1 + r2, r1 * r2), [E(-(r1 + r2), r1 * r2), E(r1 + r2, -r1 * r2), E(r1 * r2, r1 + r2), E(-(r1 + r2), -r1 * r2)]), 'x² − (sum of roots)x + (product of roots) = 0.', [`Sum = ${r1 + r2}, product = ${r1 * r2}`, `x² − (${r1 + r2})x + (${r1 * r2}) = 0`], { v: 'form', r1, r2 });
    } });

  def({ id: 'q_inequality', unit: P3('ch03-u01'), name: 'Linear inequalities and LPP', concept: 'Feasible region and corner points',
    make(d) {
      const a1 = R(1, 6), b1 = R(1, 6), a2 = R(1, 6), b2 = R(1, 6), c1 = a1 * b1 * R(2, 6), c2 = a2 * b2 * R(2, 6); if (a1 * b2 === a2 * b1) throw new Error('retry');
      const feas = (x, y) => x.sign >= 0 && y.sign >= 0 && !F(a1).mul(x).add(F(b1).mul(y)).gt(c1) && !F(a2).mul(x).add(F(b2).mul(y)).gt(c2);
      const sys = `x ≥ 0, y ≥ 0, ${a1 === 1 ? '' : a1}x + ${b1 === 1 ? '' : b1}y ≤ ${c1}, ${a2 === 1 ? '' : a2}x + ${b2 === 1 ? '' : b2}y ≤ ${c2}`;
      if (chance(.5)) {
        const pts = []; for (let k = 0; k < 200 && pts.length < 12; k++) { const p = [R(0, Math.ceil(c1 / a1) + 2), R(0, Math.ceil(c1 / b1) + 2)]; if (!pts.some(q => q[0] === p[0] && q[1] === p[1])) pts.push(p); }
        const good = pts.filter(p => feas(F(p[0]), F(p[1]))), bad = pts.filter(p => !feas(F(p[0]), F(p[1])) && p[0] + p[1] > 0); if (!good.length || bad.length < 3) throw new Error('retry');
        const g = pick(good.filter(p => p[0] + p[1] > 0).length ? good.filter(p => p[0] + p[1] > 0) : good), f = p => `(${p[0]}, ${p[1]})`;
        return QI(`Which point lies in the region ${sys}?`, buildS(f(g), sample(bad, 3).map(f)), 'Substitute the point in every inequality; it must satisfy all of them.', [`${f(g)}: ${a1} × ${g[0]} + ${b1} × ${g[1]} = ${a1 * g[0] + b1 * g[1]} ≤ ${c1}`, `${a2} × ${g[0]} + ${b2} × ${g[1]} = ${a2 * g[0] + b2 * g[1]} ≤ ${c2}`, 'The other points break at least one inequality'], { v: 'point', a1, b1, c1, a2, b2, c2, g });
      }
      const p = R(1, 9), q = R(1, 9), det = a1 * b2 - a2 * b1, ix = F(c1 * b2 - c2 * b1, det), iy = F(a1 * c2 - a2 * c1, det);
      const cand = [[F(0), F(0)], [F(c1, a1), F(0)], [F(c2, a2), F(0)], [F(0), F(c1, b1)], [F(0), F(c2, b2)], [ix, iy]].filter(([x, y]) => feas(x, y));
      const Z = ([x, y]) => F(p).mul(x).add(F(q).mul(y)); let best = cand[0]; cand.forEach(c => { if (Z(c).gt(Z(best))) best = c; });
      const zmax = Z(best); if (dpOf(zmax) === null || badDp(zmax, 2)) throw new Error('retry');
      const all = [[F(c1, a1), F(0)], [F(c2, a2), F(0)], [F(0), F(c1, b1)], [F(0), F(c2, b2)], [ix, iy]].map(Z);
      return QI(`Maximise Z = ${p === 1 ? '' : p}x + ${q === 1 ? '' : q}y subject to ${sys}. The maximum value of Z is:`, buildN(zmax, all.filter(z => !z.eq(zmax))), 'The optimum of a linear objective over a bounded feasible region occurs at a corner point: evaluate Z at each feasible corner.', [`Feasible corners: ${cand.map(([x, y]) => `(${nf(x)}, ${nf(y)})`).join(', ')}`, `Z at corners: ${cand.map(c => nf(Z(c))).join(', ')}`, `Maximum Z = ${nf(zmax)} at (${nf(best[0])}, ${nf(best[1])})`], { v: 'lpp', a1, b1, c1, a2, b2, c2, p, q });
    } });

  /* ---- Mathematics of finance ---- */
  def({ id: 'q_simple_interest', unit: P3('ch04-u01'), name: 'Simple interest', concept: 'SI = PRT/100',
    make(d) {
      const P = RS(1000, 500000, 500), r = pick([4, 5, 6, 7.5, 8, 9, 10, 12, 12.5, 15]), t = pick([1, 2, 3, 4, 5, 2.5, 1.5]), v = pick(['si', 'amt', 'rate', 'time']);
      const SI = F(P).mul(F(r)).mul(F(t)).div(100), A = SI.add(P); if (badDp(SI, 2)) throw new Error('retry');
      if (v === 'si' || v === 'amt') return QI(`Find the ${v === 'si' ? 'simple interest' : 'amount'} on ${rs(P)} at ${num(F(r))}% p.a. for ${num(F(t))} years.`, build(v === 'si' ? SI : A, v === 'si' ? [SI.add(P), F(P).mul(F(r)).div(100), SI.mul(2), F(P).mul(F(r)).div(100).mul(F(t).add(1))] : [SI, A.add(F(P).mul(F(r)).div(100)), F(P).add(F(P).mul(F(r)).div(100))], rs), 'SI = P × R × T / 100; Amount = P + SI.', [`SI = ${ind(P)} × ${num(F(r))} × ${num(F(t))} ÷ 100 = ${rs(SI)}`, ...(v === 'amt' ? [`Amount = ${ind(P)} + ${num(SI)} = ${rs(A)}`] : [])], { v, P, r: String(r), t: String(t) });
      if (v === 'rate') return QI(`A sum of ${rs(P)} amounts to ${rs(A)} in ${num(F(t))} years at simple interest. What is the rate of interest p.a.?`, build(F(r), [F(r).mul(F(t)), SI.mul(100).div(A).div(F(t)), F(r).add(1), SI.mul(100).div(P)], x => pct(x), { ok: x => !badDp(F(x), 2) }), 'R = SI × 100 / (P × T).', [`SI = ${num(A)} − ${ind(P)} = ${num(SI)}`, `R = ${num(SI)} × 100 ÷ (${ind(P)} × ${num(F(t))}) = ${num(F(r))}`], { v, P, r: String(r), t: String(t) });
      return QI(`In how many years will ${rs(P)} earn simple interest of ${rs(SI)} at ${num(F(r))}% p.a.?`, build(F(t), [F(t).add(1), SI.mul(100).div(P), F(t).mul(2), F(r).div(F(t))], x => num(x) + ' years', { ok: x => F(x).sign > 0 }), 'T = SI × 100 / (P × R).', [`T = ${num(SI)} × 100 ÷ (${ind(P)} × ${num(F(r))}) = ${num(F(t))}`], { v, P, r: String(r), t: String(t) });
    } });

  def({ id: 'q_compound_interest', unit: P3('ch04-u01'), name: 'Compound interest', concept: 'Compounding annually, half-yearly, quarterly',
    make(d) {
      const P = RS(1000, 500000, 1000), r = pick([4, 5, 6, 8, 10, 12, 15, 20]), m = d === 'easy' ? 1 : pick([1, 2, 4]), t = pick([1, 2, 3]), v = pick(['ci', 'amt', 'diff']);
      const i = F(r, 100 * m), n = m * t, A = F(P).mul(F(1).add(i).pow(n)), CI = A.sub(P), fq = { 1: 'annually', 2: 'half-yearly', 4: 'quarterly' }[m];
      if (v === 'diff') { const t2 = 2, df = F(P).mul(F(r, 100)).mul(F(r, 100)); return QI(`Find the difference between compound interest (compounded annually) and simple interest on ${rs(P)} for 2 years at ${r}% p.a.`, build(df, [df.mul(2), F(P).mul(r).div(100), df.mul(F(r, 100)).add(df), df.div(2)], rs2), 'For 2 years, CI − SI = P(R/100)².', [`CI − SI = ${ind(P)} × (${r}/100)² = ${num(df)}`], { v, P, r }); }
      const corr = v === 'ci' ? CI : A, si = F(P).mul(r).mul(t).div(100);
      return QI(`Find the ${v === 'ci' ? 'compound interest' : 'amount'} on ${rs(P)} at ${r}% p.a. for ${PL(t, 'year')}, compounded ${fq}. (Round to two decimals.)`, build(roundDp(corr, 2), v === 'ci' ? [si, roundDp(F(P).mul(F(1).add(F(r, 100)).pow(t)).sub(P), 2), roundDp(A, 2), roundDp(CI.mul(F(101, 100)), 2)] : [si.add(P), roundDp(F(P).mul(F(1).add(F(r, 100)).pow(t)), 2), roundDp(CI, 2)], rs2), 'A = P(1 + i)ⁿ where i = rate per period and n = number of periods; CI = A − P.', [`i = ${r}% ÷ ${m} = ${num(i.mul(100))}% per period`, `n = ${t} × ${m} = ${n}`, `A = ${ind(P)} × (${num(F(1).add(i))})${sup(n)} ${ap(A, 2)}`, ...(v === 'ci' ? [`CI = ${fixed(A, 2)} − ${ind(P)} ${ap(CI, 2)}`] : [])], { v, P, r, m, t });
    } });

  def({ id: 'q_effective_rate', unit: P3('ch04-u01'), name: 'Effective rate of interest', concept: 'E = (1 + i)ⁿ − 1',
    make(d) {
      const r = pick([4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 20, 24]), m = pick([2, 4, 12]), fq = { 2: 'half-yearly', 4: 'quarterly', 12: 'monthly' }[m];
      const E = F(1).add(F(r, 100 * m)).pow(m).sub(1).mul(100);
      return QI(`What is the effective annual rate of interest equivalent to a nominal rate of ${r}% p.a. compounded ${fq}? (Correct to two decimals.)`, build(roundDp(E, 2), [F(r), F(r * m), roundDp(F(1).add(F(r, 100 * m)).pow(m - 1).sub(1).mul(100), 2), roundDp(E.add(F(r, m)), 2)], x => fixed(x, 2) + '%'), 'Effective rate E = (1 + r/m)ᵐ − 1, where m is the number of compounding periods a year.', [`i per period = ${r}% ÷ ${m} ${ap(F(r, m), 4)}%`, `E = (1 + ${num(F(r, 100 * m))})${sup(m)} − 1 ≈ ${fixed(E.div(100), 6)}`, `E ≈ ${fixed(E, 2)}%`], { r, m });
    } });

  def({ id: 'q_annuity', unit: P3('ch04-u01'), name: 'Annuity, PV, FV and sinking fund', concept: 'Present and future value of an annuity',
    make(d) {
      const A = RS(1000, 200000, 500), r = pick([4, 5, 6, 8, 10, 12]), n = R(2, d === 'easy' ? 4 : 8), i = F(r, 100), v = pick(['fv', 'pv', 'sink', 'due']), g = F(1).add(i).pow(n);
      const fv = F(A).mul(g.sub(1)).div(i), pv = F(A).mul(F(1).sub(F(1).div(g))).div(i), gx = badDp(g, 6), apg = (x, dp) => gx ? '≈ ' + fixed(x, dp) : ap(x, dp);
      if (v === 'sink') { const T = RS(100000, 5000000, 10000), dep = F(T).mul(i).div(g.sub(1)); return QI(`How much must be deposited at the end of each year at ${r}% p.a. compound interest to accumulate ${rs(T)} in ${n} years (sinking fund)? (Round to the nearest rupee.)`, build(roundDp(dep, 0), [roundDp(F(T, n), 0), roundDp(F(T).mul(i).div(g), 0), roundDp(F(T).div(g), 0), roundDp(F(T).mul(i).div(g.sub(1)).mul(F(1).add(i)), 0)], rsr), 'Sinking fund instalment A = FV × i / [(1 + i)ⁿ − 1].', [`(1 + ${num(i)})${sup(n)} ${ap(g, 6)}`, `A = ${ind(T)} × ${num(i)} ÷ (${fixed(g, 6)} − 1) ${badDp(g, 6) ? '≈ ' + fixed(dep, 2) : ap(dep, 2)}`, `Rounded: ${rsr(dep)}`], { v, T, r, n }); }
      const corr = v === 'fv' ? fv : v === 'pv' ? pv : fv.mul(F(1).add(i));
      const q = v === 'fv' ? `Find the future value of an ordinary annuity of ${rs(A)} a year for ${n} years at ${r}% p.a. compounded annually. (Round to the nearest rupee.)` : v === 'pv' ? `Find the present value of an annuity of ${rs(A)} payable at the end of each year for ${n} years at ${r}% p.a. (Round to the nearest rupee.)` : `Find the future value of an annuity due of ${rs(A)} a year (paid at the beginning of each year) for ${n} years at ${r}% p.a. (Round to the nearest rupee.)`;
      const steps = [`(1 + ${num(i)})${sup(n)} ${ap(g, 6)}`, v === 'pv' ? `PV = ${ind(A)} × (1 − 1/${fixed(g, 6)}) ÷ ${num(i)} ${apg(pv, 2)}` : `FV (ordinary) = ${ind(A)} × (${fixed(g, 6)} − 1) ÷ ${num(i)} ${apg(fv, 2)}`]; if (v === 'due') steps.push(`Annuity due = ${fixed(fv, 2)} × ${num(F(1).add(i))} ${gx || badDp(fv, 2) ? '≈ ' + fixed(corr, 2) : ap(corr, 2)}`); steps.push(`Rounded: ${rsr(corr)}`);
      return QI(q, build(roundDp(corr, 0), [roundDp(F(A * n), 0), roundDp(v === 'pv' ? fv : pv, 0), roundDp(v === 'due' ? fv : corr.mul(F(1).add(i)), 0), roundDp(F(A).mul(g), 0)], rsr), 'FV of an ordinary annuity = A[(1 + i)ⁿ − 1]/i; PV = A[1 − (1 + i)⁻ⁿ]/i; an annuity due is the ordinary value × (1 + i).', steps, { v, A, r, n });
    } });

  def({ id: 'q_perm', unit: P3('ch05-u01'), name: 'Permutations', concept: 'Arrangements with and without repetition',
    make(d) {
      const v = pick(['npr', 'word', 'together', 'circle']);
      if (v === 'npr') { const n = R(4, 10), r = R(2, Math.min(5, n)), val = nPr(n, r); return QI(`In how many ways can ${r} different prizes be given to ${n} students if a student can get at most one prize?`, buildN(F(val), [F(nCr(n, r)), F(BI(n) ** BI(r)), F(nPr(n, r - 1)), F(fact(n))]), 'Order matters (prizes are different): ⁿPᵣ = n!/(n − r)!.', [`ⁿPᵣ = ${n}P${r} = ${Array.from({ length: r }, (_, k) => n - k).join(' × ')} = ${ind(val)}`], { v, n, r }); }
      if (v === 'word') { const w = pick(['ACCOUNT', 'BALANCE', 'LEDGER', 'AUDIT', 'CAPITAL', 'FINANCE', 'MONEY', 'PROFIT', 'ASSETS', 'RUPEE', 'DEBIT', 'CREDIT', 'MARKET', 'BUDGET']), cnt = {}; for (const c of w) cnt[c] = (cnt[c] || 0) + 1;
        let den = 1n; const reps = Object.entries(cnt).filter(([c, k]) => k > 1); reps.forEach(([c, k]) => { den *= fact(k); }); const val = fact(w.length) / den;
        return QI(`How many different arrangements can be made of all the letters of the word ${w}?`, buildN(F(val), [F(fact(w.length)), F(fact(w.length - 1)), F(val * 2n), F(fact(w.length) / 2n)]), 'n!/(p! q! …) where p, q … are the counts of repeated letters.', [`${w.length} letters${reps.length ? `; repeated: ${reps.map(([c, k]) => `${c} × ${k}`).join(', ')}` : ', all different'}`, `${w.length}!${reps.length ? ' ÷ ' + reps.map(([c, k]) => `${k}!`).join(' ÷ ') : ''} = ${ind(fact(w.length))}${reps.length ? ' ÷ ' + ind(den) : ''} = ${ind(val)}`], { v, w }); }
      if (v === 'together') { const n = R(4, 8), k = R(2, Math.min(4, n - 1)), val = fact(n - k + 1) * fact(k); return QI(`In how many ways can ${n} people sit in a row if ${k} particular people must always sit together?`, buildN(F(val), [F(fact(n - k + 1)), F(fact(n) - val), F(fact(n)), F(fact(n - k) * fact(k))]), 'Tie the group into one unit: (n − k + 1)! arrangements × k! inside the group.', [`Units: ${n} − ${k} + 1 = ${n - k + 1}; arrangements ${n - k + 1}! = ${ind(fact(n - k + 1))}`, `Inside the group: ${k}! = ${ind(fact(k))}`, `Total: ${ind(fact(n - k + 1))} × ${ind(fact(k))} = ${ind(val)}`], { v, n, k }); }
      const n = R(4, 9), val = fact(n - 1); return QI(`In how many ways can ${n} persons be seated around a circular table?`, buildN(F(val), [F(fact(n)), F(fact(n - 1) / 2n), F(fact(n - 2)), F(BI(n) * fact(n - 2))]), 'Circular arrangements of n distinct objects = (n − 1)!.', [`(n − 1)! = ${n - 1}! = ${ind(val)}`], { v, n });
    } });

  def({ id: 'q_comb', unit: P3('ch05-u01'), name: 'Combinations', concept: 'Selections and committees',
    make(d) {
      const v = pick(['ncr', 'mixed', 'atleast']);
      if (v === 'ncr') { const n = R(5, 15), r = R(2, Math.min(6, n - 1)), val = nCr(n, r); return QI(`In how many ways can a committee of ${r} be chosen from ${n} persons?`, buildN(F(val), [F(nPr(n, r)), F(nCr(n, r - 1)), F(nCr(n - 1, r)), F(BI(n) * BI(r))]), 'Order does not matter: ⁿCᵣ = n!/[r!(n − r)!].', [`${n}C${r} = ${n}! ÷ (${r}! × ${n - r}!) = ${ind(val)}`], { v, n, r }); }
      const m = R(4, 9), w = R(3, 8), a = R(1, Math.min(4, m)), b = R(1, Math.min(4, w));
      if (v === 'mixed') { const val = nCr(m, a) * nCr(w, b); return QI(`From ${m} men and ${w} women, a committee of ${a} ${a === 1 ? 'man' : 'men'} and ${b} ${b === 1 ? 'woman' : 'women'} is to be formed. In how many ways can this be done?`, buildN(F(val), [F(nCr(m, a) + nCr(w, b)), F(nCr(m + w, a + b)), F(nPr(m, a) * nPr(w, b)), F(nCr(m, b) * nCr(w, a))]), 'Choose the men and the women separately and multiply (fundamental principle).', [`Men: ${m}C${a} = ${ind(nCr(m, a))}`, `Women: ${w}C${b} = ${ind(nCr(w, b))}`, `Total: ${ind(nCr(m, a))} × ${ind(nCr(w, b))} = ${ind(val)}`], { v, m, w, a, b }); }
      const r = R(2, Math.min(5, m + w - 1)); if (r > m) throw new Error('retry'); const tot = nCr(m + w, r), none = nCr(m, r), val = tot - none;
      return QI(`A team of ${r} is chosen from ${m} men and ${w} women. In how many ways can it include at least one woman?`, buildN(F(val), [F(tot), F(nCr(w, 1) * nCr(m + w - 1, r - 1)), F(none), F(nCr(w, r))]), 'At least one = total selections − selections with none.', [`Total: ${m + w}C${r} = ${ind(tot)}`, `No woman: ${m}C${r} = ${ind(none)}`, `At least one woman: ${ind(tot)} − ${ind(none)} = ${ind(val)}`], { v: 'atleast', m, w, r });
    } });

  def({ id: 'q_ap', unit: P3('ch06-u01'), name: 'Arithmetic progression', concept: 'nth term and sum of an AP',
    make(d) {
      const a = R(-20, 50), dd = pick([R(-9, -1), R(1, 12)]), n = R(8, 40), v = pick(['term', 'sum', 'mult']);
      if (v === 'term') { const t = a + (n - 1) * dd; return QI(`Find the ${n}th term of the AP ${a}, ${a + dd}, ${a + 2 * dd}, …`.replace(/-(\d)/g, '−$1'), buildN(F(t), [F(a + n * dd), F(a + (n - 2) * dd), F(n * dd), F(a * n)]), 'tₙ = a + (n − 1)d.', [`a = ${a}, d = ${dd}`, `t${n} = ${pn(a)} + ${n - 1} × ${pn(dd)} = ${t}`], { v, a, dd, n }); }
      if (v === 'sum') { const S = F(n, 2).mul(2 * a + (n - 1) * dd); return QI(`Find the sum of the first ${n} terms of the AP ${a}, ${a + dd}, ${a + 2 * dd}, …`.replace(/-(\d)/g, '−$1'), buildN(S, [F(n, 2).mul(2 * a + n * dd), F(n).mul(a + (n - 1) * dd), F(n, 2).mul(a + (n - 1) * dd), S.add(a)]), 'Sₙ = n/2 [2a + (n − 1)d].', [`Sₙ = ${n}/2 × [2 × ${pn(a)} + ${n - 1} × ${pn(dd)}]`, `= ${nf(F(n, 2))} × ${2 * a + (n - 1) * dd} = ${nf(S)}`], { v, a, dd, n }); }
      const k = R(3, 13), lo = R(1, 100), hi = lo + R(100, 600), f = Math.ceil(lo / k) * k, l = Math.floor(hi / k) * k, cnt = (l - f) / k + 1, S = F(cnt).mul(f + l).div(2);
      return QI(`Find the sum of all multiples of ${k} between ${lo} and ${hi} (inclusive).`, buildN(S, [F(cnt + 1).mul(f + l).div(2), F(cnt).mul(f + l), F(cnt - 1).mul(f + l).div(2), F(cnt)]), 'List the multiples as an AP: first f, last l, number n = (l − f)/k + 1, sum = n(f + l)/2.', [`First = ${f}, last = ${l}`, `n = (${l} − ${f}) ÷ ${k} + 1 = ${cnt}`, `Sum = ${cnt} × (${f} + ${l}) ÷ 2 = ${nf(S)}`], { v, k, lo, hi });
    } });

  def({ id: 'q_gp', unit: P3('ch06-u01'), name: 'Geometric progression', concept: 'nth term and sum of a GP',
    make(d) {
      const a = R(1, 9), r = pick([2, 3, -2, F(1, 2), F(1, 3), 4]), rr = F(r), n = R(4, 8), v = pick(['term', 'sum', 'inf']);
      if (v === 'inf') { const rq = pick([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(-1, 2), F(3, 4)]), S = F(a).div(F(1).sub(rq)); return QI(`Find the sum to infinity of the GP ${a}, ${fr(F(a).mul(rq))}, ${fr(F(a).mul(rq).mul(rq))}, …`, buildN(S, [F(a).div(F(1).add(rq)), F(a).mul(rq).div(F(1).sub(rq)), F(a).div(rq), S.add(1)]), 'S∞ = a/(1 − r) when |r| < 1.', [`a = ${a}, r = ${fr(rq)}`, `S∞ = ${a} ÷ (1 − ${pn(rq)}) = ${nf(S)}`], { v, a, rq: fr(rq) }); }
      const t = F(a).mul(rr.pow(n - 1)), S = rr.eq(1) ? F(a * n) : F(a).mul(F(1).sub(rr.pow(n))).div(F(1).sub(rr));
      if (v === 'term') return QI(`Find the ${n}th term of the GP ${a}, ${fr(F(a).mul(rr))}, ${fr(F(a).mul(rr).mul(rr))}, …`, buildN(t, [F(a).mul(rr.pow(n)), F(a).mul(rr.pow(n - 2)), F(a).mul(rr).mul(n - 1), t.neg()]), 'tₙ = a rⁿ⁻¹.', [`a = ${a}, r = ${fr(rr)}`, `t${n} = ${a} × (${fr(rr)})${sup(n - 1)} = ${nf(t)}`], { v, a, r: fr(rr), n });
      return QI(`Find the sum of the first ${n} terms of the GP ${a}, ${fr(F(a).mul(rr))}, ${fr(F(a).mul(rr).mul(rr))}, …`, buildN(S, [F(a).mul(F(1).sub(rr.pow(n - 1))).div(F(1).sub(rr)), F(a).mul(F(1).sub(rr.pow(n + 1))).div(F(1).sub(rr)), t, S.add(t)]), 'Sₙ = a(rⁿ − 1)/(r − 1) for r ≠ 1.', [`a = ${a}, r = ${fr(rr)}, n = ${n}`, `Sₙ = ${a} × [1 − (${fr(rr)})${sup(n)}] ÷ (1 − ${pn(rr)}) = ${nf(S)}`], { v, a, r: fr(rr), n });
    } });

  def({ id: 'q_sets', unit: P3('ch07-u01'), name: 'Sets', concept: 'n(A ∪ B) = n(A) + n(B) − n(A ∩ B)',
    make(d) {
      const AB = R(5, 60), Ao = R(5, 80), Bo = R(5, 80), N = R(0, 60), U2 = Ao + Bo + AB + N, nA = Ao + AB, nB = Bo + AB, v = pick(['union', 'onlyA', 'neither', 'inter']);
      const subj = pick([['accountancy', 'economics'], ['tea', 'coffee'], ['Hindi newspaper', 'English newspaper'], ['cricket', 'football']]);
      const base = `In a group of ${U2} people, ${nA} like ${subj[0]}, ${nB} like ${subj[1]} and ${AB} like both.`;
      if (v === 'inter') { return QI(`In a group of ${U2} people, ${nA} like ${subj[0]}, ${nB} like ${subj[1]} and ${N} like neither. How many like both?`, buildN(F(AB), [F(nA + nB - U2), F(U2 - N), F(nA + nB), F(AB + N)], { ok: x => F(x).sign >= 0 }), 'n(A ∩ B) = n(A) + n(B) − n(A ∪ B), and n(A ∪ B) = total − neither.', [`n(A ∪ B) = ${U2} − ${N} = ${U2 - N}`, `n(A ∩ B) = ${nA} + ${nB} − ${U2 - N} = ${AB}`], { v, U2, nA, nB, N }); }
      const vals = { union: nA + nB - AB, onlyA: nA - AB, neither: U2 - (nA + nB - AB) }, ask = { union: `How many like at least one of the two?`, onlyA: `How many like only ${subj[0]}?`, neither: `How many like neither?` }[v];
      const wr = { union: [nA + nB, nA + nB - 2 * AB, U2 - AB], onlyA: [nA, nA - 2 * AB, nB - AB], neither: [U2 - nA - nB, U2 - AB, AB] }[v];
      const steps = [`n(A ∪ B) = ${nA} + ${nB} − ${AB} = ${nA + nB - AB}`]; if (v === 'onlyA') steps.splice(0, 1, `Only ${subj[0]} = ${nA} − ${AB} = ${nA - AB}`); if (v === 'neither') steps.push(`Neither = ${U2} − ${nA + nB - AB} = ${vals.neither}`);
      return QI(base + ' ' + ask, buildN(F(vals[v]), wr.map(x => F(x)), { ok: x => F(x).sign >= 0 }), 'Use the Venn diagram: those in both are counted twice in n(A) + n(B).', steps, { v, U2, nA, nB, AB });
    } });

  def({ id: 'q_functions', unit: P3('ch07-u01'), name: 'Functions', concept: 'Composite and inverse functions',
    make(d) {
      const a = R(1, 6) * pick([1, -1]), b = R(-9, 9), c = R(1, 4), e = R(-9, 9), k = R(-4, 5), v = pick(['fog', 'gof', 'inv']);
      const f = x => F(a).mul(x).add(b), g = x => F(c).mul(x).mul(x).add(e);
      if (v === 'inv') { const y = R(-20, 30), val = F(y - b, a); return QI(`If f(x) = ${poly([a, b])}, find f⁻¹(${y}).`.replace(/\((-)(\d)/, '(−$2'), buildN(val, [f(y), F(y + b, a), F(y - b).mul(a), F(a, y - b === 0 ? 1 : y - b)]), 'Solve y = f(x) for x: f⁻¹(y) = (y − b)/a.', [`${y} = ${poly([a, b])}`, `x = (${y} − ${pn(b)}) ÷ ${pn(a)} = ${nf(val)}`], { v, a, b, y }); }
      const val = v === 'fog' ? f(g(k)) : g(f(k));
      return QI(`If f(x) = ${poly([a, b])} and g(x) = ${poly([c, 0, e])}, find ${v === 'fog' ? 'f(g' : 'g(f'}(${k})).`.replace(/\((-)(\d)/, '(−$2'), buildN(val, [v === 'fog' ? g(f(k)) : f(g(k)), f(F(k)).mul(g(F(k))), f(F(k)).add(g(F(k))), val.add(a)]), 'Work from the inside out: evaluate the inner function first.', v === 'fog' ? [`g(${k}) = ${c} × ${pn(k)}² ${sgn(e)} ${Math.abs(e)} = ${nf(g(k))}`, `f(${nf(g(k))}) = ${a} × ${pn(g(k))} ${sgn(b)} ${Math.abs(b)} = ${nf(val)}`] : [`f(${k}) = ${a} × ${pn(k)} ${sgn(b)} ${Math.abs(b)} = ${nf(f(k))}`, `g(${nf(f(k))}) = ${c} × ${pn(f(k))}² ${sgn(e)} ${Math.abs(e)} = ${nf(val)}`], { v, a, b, c, e, k });
    } });

  def({ id: 'q_limits', unit: P3('ch07-u01'), name: 'Limits', concept: 'Standard limits and limits at infinity',
    make(d) {
      const v = pick(['factor', 'power', 'inf']);
      if (v === 'factor') { const a = R(-6, 9), b = R(-6, 9); if (a === b) throw new Error('retry'); const val = F(a - b);   // lim x→a (x−a)(x−b)/(x−a)
        const num2 = poly([1, -(a + b), a * b]); return QI(`Evaluate lim(x→${a}) (${num2}) / (x ${a < 0 ? '+' : '−'} ${Math.abs(a)}).`.replace('→-', '→−'), buildN(val, [F(a + b), F(-b), F(0), F(a * b)]), 'Factorise and cancel the factor that becomes zero, then substitute.', [`${num2} = (x ${a < 0 ? '+' : '−'} ${Math.abs(a)})(x ${b < 0 ? '+' : '−'} ${Math.abs(b)})`, `Limit = ${pn(a)} − ${pn(b)} = ${a - b}`], { v, a, b }); }
      if (v === 'power') { const a = R(1, 5), n = R(2, 6), val = F(n).mul(F(a).pow(n - 1)); return QI(`Evaluate lim(x→${a}) (x${sup(n)} − ${ind(a ** n)}) / (x − ${a}).`, buildN(val, [F(a).pow(n - 1), F(n).mul(F(a).pow(n)), F(n - 1).mul(F(a).pow(n - 1)), F(a ** n)]), 'lim(x→a) (xⁿ − aⁿ)/(x − a) = n aⁿ⁻¹.', [`n aⁿ⁻¹ = ${n} × ${a}${sup(n - 1)} = ${nf(val)}`], { v, a, n }); }
      const p = R(1, 9), q = R(-9, 9), r = R(-9, 9), s = R(1, 9), t = R(-9, 9), u = R(-9, 9), val = F(p, s);
      return QI(`Evaluate lim(x→∞) (${poly([p, q, r])}) / (${poly([s, t, u])}).`, build(val, [F(s, p), F(r, u || 1), F(q, t || 1), F(0)], fr), 'Divide numerator and denominator by the highest power of x; terms with 1/x vanish.', [`Divide by x²: (${p} + ${q}/x + ${r}/x²) ÷ (${s} + ${t}/x + ${u}/x²)`.replace(/\+ -/g, '− '), `As x → ∞ the limit is ${p}/${s} = ${nf(val)}`], { v, p, q, r, s, t, u });
    } });

  def({ id: 'q_calculus', unit: P3('ch08-u01'), name: 'Differentiation and integration', concept: 'Derivatives, marginal cost and definite integrals',
    make(d) {
      const v = pick(['deriv', 'mc', 'integ']), c = [R(-3, 4), R(-9, 9), R(-12, 12), R(-20, 20)]; if (!c[0]) c[0] = 1;
      if (v === 'deriv') { const k = R(-4, 5), val = F(3 * c[0] * k * k + 2 * c[1] * k + c[2]); return QI(`If y = ${poly(c)}, find dy/dx at x = ${k}.`.replace('= -', '= −'), buildN(val, [F(c[0] * k ** 3 + c[1] * k * k + c[2] * k + c[3]), F(3 * c[0] * k * k + c[1] * k + c[2]), F(6 * c[0] * k + 2 * c[1]), F(c[0] * k * k + c[1] * k + c[2])]), 'd/dx (xⁿ) = n xⁿ⁻¹; the derivative of a constant is 0.', [`dy/dx = ${poly([3 * c[0], 2 * c[1], c[2]])}`, `At x = ${k}: ${3 * c[0]} × ${pn(k)}² + ${2 * c[1]} × ${pn(k)} + ${pn(c[2])} = ${nf(val)}`], { v, c, k }); }
      if (v === 'mc') { const a = R(1, 5), b = R(2, 60), FC = RS(100, 5000, 50), qq = R(5, 50), val = F(2 * a * qq + b); return QI(`The total cost function is C = ${a === 1 ? '' : a}q² + ${b}q + ${ind(FC)}. Find the marginal cost when q = ${qq}.`, buildN(val, [F(a * qq * qq + b * qq + FC), F(a * qq + b), F(a * qq * qq + b * qq + FC, qq), F(2 * a * qq + b + FC)]), 'Marginal cost = dC/dq.', [`MC = dC/dq = ${2 * a}q + ${b}`, `At q = ${qq}: ${2 * a} × ${qq} + ${b} = ${nf(val)}`], { v, a, b, FC, qq }); }
      const a = R(0, 3), b = a + R(1, 4), cc = [R(0, 4), R(-6, 6), R(-9, 9)]; if (!cc[0] && !cc[1]) throw new Error('retry');
      const Fn = x => F(cc[0]).mul(F(x).pow(3)).div(3).add(F(cc[1]).mul(F(x).pow(2)).div(2)).add(F(cc[2]).mul(x)), val = Fn(b).sub(Fn(a));
      return QI(`Evaluate ∫ from ${a} to ${b} of (${poly(cc)}) dx.`, buildN(val, [Fn(b), F(cc[0]).mul(b * b - a * a).add(F(cc[1]).mul(b - a)), Fn(b).add(Fn(a)), val.mul(2)]), '∫xⁿ dx = xⁿ⁺¹/(n + 1); evaluate the antiderivative at the upper limit minus at the lower limit.', [`Antiderivative: ${poly([F(cc[0], 3), F(cc[1], 2), cc[2], 0])}`, `At ${b}: ${nf(Fn(b))}; at ${a}: ${nf(Fn(a))}`, `Value: ${nf(Fn(b))} − ${pn(Fn(a))} = ${nf(val)}`], { v, a, b, cc });
    } });

  /* ---- Logical reasoning ---- */
  def({ id: 'q_series', unit: P3('ch09-u01'), name: 'Number series', concept: 'Find the pattern, find the next term',
    make(d) {
      const v = pick(['ap', 'gp', 'sq', 'cube', 'diff2', 'x2p']); let t = [], rule;
      if (v === 'ap') { const a = R(1, 60), dd = R(2, 19); for (let i = 0; i < 6; i++) t.push(a + i * dd); rule = `add ${dd} each time`; }
      if (v === 'gp') { const a = R(1, 7), r = pick([2, 3, 4]); for (let i = 0; i < 6; i++) t.push(a * r ** i); rule = `multiply by ${r} each time`; }
      if (v === 'sq') { const s = R(1, 12), c = R(-3, 5); for (let i = 0; i < 6; i++) t.push((s + i) ** 2 + c); rule = `squares of ${s}, ${s + 1}, ${s + 2}, …${c ? ` ${c < 0 ? 'minus' : 'plus'} ${Math.abs(c)}` : ''}`; }
      if (v === 'cube') { const s = R(1, 6), c = R(-2, 3); for (let i = 0; i < 6; i++) t.push((s + i) ** 3 + c); rule = `cubes of ${s}, ${s + 1}, ${s + 2}, …${c ? ` ${c < 0 ? 'minus' : 'plus'} ${Math.abs(c)}` : ''}`; }
      if (v === 'diff2') { const a = R(1, 30), d0 = R(1, 8), e = R(1, 5); let x = a, dd = d0; for (let i = 0; i < 6; i++) { t.push(x); x += dd; dd += e; } rule = `differences ${d0}, ${d0 + e}, ${d0 + 2 * e}, … increase by ${e}`; }
      if (v === 'x2p') { let x = R(1, 9); const m = pick([2, 3]), c = R(-2, 3); if (!c) throw new Error('retry'); for (let i = 0; i < 6; i++) { t.push(x); x = x * m + c; } rule = `multiply by ${m} then ${c < 0 ? 'subtract' : 'add'} ${Math.abs(c)}`; }
      const shown = t.slice(0, 5), ans = t[5], dlast = t[4] - t[3];
      return QI(`Find the next term: ${shown.map(x => ind(x)).join(', ')}, ?`, buildN(F(ans), [F(t[4] + dlast), F(t[4] * 2), F(ans + 1), F(ans - 2), F(t[4] + (t[4] - t[3]) + (t[3] - t[2]))]), 'Look at the differences first; if they are not constant, try ratios, squares/cubes, or a two-step rule.', [`Pattern: ${rule}`, `Next term = ${ind(ans)}`], { v, t });
    } });

  const shiftW = (w, k) => w.split('').map(c => String.fromCharCode((c.charCodeAt(0) - 65 + k + 2600) % 26 + 65)).join('');
  const mirrorW = w => w.split('').map(c => String.fromCharCode(155 - c.charCodeAt(0))).join('');
  def({ id: 'q_coding', unit: P3('ch09-u01'), name: 'Coding and decoding', concept: 'Letter-shift and mirror codes',
    make(d) {
      const W = ['MONEY', 'TRADE', 'LEDGER', 'AUDIT', 'BANK', 'CASH', 'STOCK', 'PRICE', 'GRAPH', 'VALUE', 'ASSET', 'CLAIM', 'BRIEF', 'DEBIT', 'PROFIT', 'BOND', 'LOAN', 'TAXES'], [w1, w2] = sample(W, 2), v = pick(['shift', 'shift', 'mirror', 'revshift']);
      if (v === 'mirror') { const c1 = mirrorW(w1), c2 = mirrorW(w2); return QI(`In a code, ${w1} is written as ${c1}. How is ${w2} written in that code?`, buildS(c2, [shiftW(w2, 1), c2.split('').reverse().join(''), shiftW(c2, 1), mirrorW(w2.split('').reverse().join(''))]), 'Each letter is replaced by its opposite letter (A↔Z, B↔Y, …): the two positions add up to 27.', [`${w1[0]} (${w1.charCodeAt(0) - 64}) → ${c1[0]} (${27 - (w1.charCodeAt(0) - 64)}): positions add to 27`, `Apply to ${w2}: ${c2}`], { v, w1, w2 }); }
      const k = pick([1, 2, 3, 4, -1, -2, -3]), rev = v === 'revshift', enc = w => rev ? shiftW(w, k).split('').reverse().join('') : shiftW(w, k);
      const c1 = enc(w1), c2 = enc(w2);
      return QI(`In a code, ${w1} is written as ${c1}. How is ${w2} written in that code?`, buildS(c2, [rev ? shiftW(w2, k) : shiftW(w2, k).split('').reverse().join(''), shiftW(w2, k + 1), shiftW(w2, -k), rev ? shiftW(w2, k + 1).split('').reverse().join('') : shiftW(w2, k - 1)]), 'Compare each letter of the word with the code letter: find the shift (and whether the order is reversed).', [`Each letter moves ${Math.abs(k)} place${Math.abs(k) > 1 ? 's' : ''} ${k > 0 ? 'forward' : 'back'}${rev ? ', then the letters are written in reverse order' : ''}`, `${w2} → ${shiftW(w2, k)}${rev ? ` → reversed ${c2}` : ''}`], { v, w1, w2, k });
    } });

  def({ id: 'q_odd', unit: P3('ch09-u01'), name: 'Odd man out (property)', concept: 'Classify numbers by a property',
    make(d) {
      const v = pick(['prime', 'square', 'cube', 'mult']), isP = n => { if (n < 2) return false; for (let k = 2; k * k <= n; k++) if (n % k === 0) return false; return true; };
      let good = [], bad, prop; const k = R(6, 13);
      if (v === 'prime') { while (good.length < 3) { const n = R(11, 97); if (isP(n) && !good.includes(n)) good.push(n); } do { bad = pick([R(3, 32) * 3, R(5, 24) * 7, 91, 87, 51, 57, 119, 133, 161]); } while (isP(bad) || good.includes(bad)); prop = 'a prime number'; }
      if (v === 'square') { while (good.length < 3) { const n = R(4, 30) ** 2; if (!good.includes(n)) good.push(n); } do { bad = R(4, 30) ** 2 + pick([-1, 1, 2, -2, 5]); } while (isSq(bad)); prop = 'a perfect square'; }
      if (v === 'cube') { while (good.length < 3) { const n = R(2, 12) ** 3; if (!good.includes(n)) good.push(n); } do { bad = R(2, 12) ** 3 + pick([-1, 1, 8, -8]); } while (Math.round(Math.cbrt(bad)) ** 3 === bad); prop = 'a perfect cube'; }
      if (v === 'mult') { while (good.length < 3) { const n = k * R(3, 30); if (!good.includes(n)) good.push(n); } do { bad = k * R(3, 30) + R(1, k - 1); } while (bad % k === 0); prop = `a multiple of ${k}`; }
      return QI(`Which of the following is NOT ${prop}?`, buildS(ind(bad), good.map(n => ind(n))), 'Test each number for the property; exactly one fails.', [...good.map(n => `${ind(n)} is ${prop}`), `${ind(bad)} is not`], { v, good, bad, k });
    } });

  const DIRS = ['North', 'East', 'South', 'West'], DV = [[0, 1], [1, 0], [0, -1], [-1, 0]];
  function dirName(dx, dy) { if (!dx && !dy) return 'at the start'; if (!dx) return dy > 0 ? 'North' : 'South'; if (!dy) return dx > 0 ? 'East' : 'West'; return (dy > 0 ? 'North' : 'South') + '-' + (dx > 0 ? 'East' : 'West'); }
  def({ id: 'q_direction', unit: P3('ch10-u01'), name: 'Direction sense', concept: 'Net displacement and direction',
    make(d) {
      const n = d === 'easy' ? 3 : R(3, 5), h0 = R(0, 3), legs = []; let h = h0, x = 0, y = 0; const who = pick(PEOPLE);
      for (let i = 0; i < n; i++) { if (i) h = (h + (chance(.5) ? 1 : 3)) % 4; const k = R(1, 12); legs.push([h, k]); x += DV[h][0] * k; y += DV[h][1] * k; }
      const ask = pick(['dist', 'dir']); const D2 = x * x + y * y; if (!D2) throw new Error('retry'); if (ask === 'dist' && !isSq(D2)) throw new Error('retry');
      const desc = legs.map(([hh, k], i) => i === 0 ? `walks ${k} km ${DIRS[hh]}` : `turns ${(hh - legs[i - 1][0] + 4) % 4 === 1 ? 'right' : 'left'} and walks ${k} km`).join(', then ');
      const q = `${who} ${desc}. ${ask === 'dist' ? `How far is ${who} from the starting point?` : `In which direction is ${who} now from the starting point?`}`;
      const steps = [`East–West: ${legs.filter(l => l[0] % 2).map(([hh, k]) => (hh === 1 ? '+' : '−') + k).join(' ') || '0'} = ${x} km (east positive)`, `North–South: ${legs.filter(l => l[0] % 2 === 0).map(([hh, k]) => (hh === 0 ? '+' : '−') + k).join(' ') || '0'} = ${y} km (north positive)`];
      if (ask === 'dist') { const D = Number(isqrt(D2)); steps.push(`Distance = √(${pn(x)}² + ${pn(y)}²) = √${D2} = ${D} km`); return QI(q, build(D, [Math.abs(x) + Math.abs(y), legs.reduce((s, l) => s + l[1], 0), D + 1, Math.abs(Math.abs(x) - Math.abs(y))], v => `${v} km`, { ok: v => v > 0 }), 'Add the east–west moves and the north–south moves separately, then use Pythagoras for the straight-line distance.', steps, { h0, legs, ask }); }
      const nm = dirName(x, y); steps.push(`${Math.abs(x)} km ${x >= 0 ? 'East' : 'West'} and ${Math.abs(y)} km ${y >= 0 ? 'North' : 'South'} of the start → ${nm}`);
      return QI(q, buildS(nm, [dirName(-x, -y), dirName(y, x) === nm ? dirName(-y, -x) : dirName(y, x), dirName(x, -y), dirName(-x, y), 'North', 'South-East']), 'Track the net east–west and north–south displacement; the direction from the start follows from their signs.', steps.map(s => s.replace(/-(\d)/g, '−$1')), { h0, legs, ask });
    } });

  /* ---- Seating (linear row), solved by brute force ---- */
  const perms = a => a.length <= 1 ? [a] : a.flatMap((x, i) => perms([...a.slice(0, i), ...a.slice(i + 1)]).map(p => [x, ...p]));
  function seatOk(p, c) { const at = n => p.indexOf(n);
    switch (c[0]) { case 'end': return at(c[1]) === 0 || at(c[1]) === p.length - 1; case 'imleft': return at(c[1]) === at(c[2]) - 1; case 'right2': return at(c[1]) === at(c[2]) + 2; case 'between': return Math.abs(at(c[1]) - at(c[2])) === 1 && Math.abs(at(c[1]) - at(c[3])) === 1;
      case 'notadj': return Math.abs(at(c[1]) - at(c[2])) > 1; case 'middle': return at(c[1]) === 2; case 'gap1': return Math.abs(at(c[1]) - at(c[2])) === 2; } return false; }
  function seatTxt(c) { return { end: `${c[1]} sits at one of the ends`, imleft: `${c[1]} sits immediately to the left of ${c[2]}`, right2: `${c[1]} sits second to the right of ${c[2]}`, between: `${c[1]} sits between ${c[2]} and ${c[3]}`, notadj: `${c[1]} does not sit next to ${c[2]}`, middle: `${c[1]} sits exactly in the middle`, gap1: `exactly one person sits between ${c[1]} and ${c[2]}` }[c[0]]; }
  def({ id: 'q_seating', unit: P3('ch11-u01'), name: 'Seating arrangement (row)', concept: 'Linear arrangement from clues',
    make(d) {
      const ppl = sample(['Anu', 'Babu', 'Chitra', 'Dev', 'Esha', 'Farid', 'Gita', 'Hari'], 5), sol = shuffle(ppl), all = perms(ppl), clues = [];
      const mk = () => { const t = pick(['end', 'imleft', 'right2', 'between', 'notadj', 'gap1', 'imleft', 'between']), [a, b, c] = sample(ppl, 3); return [t, a, b, c].slice(0, t === 'between' ? 4 : t === 'end' ? 2 : 3); };
      let cand = all;
      for (let k = 0; k < 80 && cand.length > 1 && clues.length < 7; k++) { const c = mk(); if (!seatOk(sol, c)) continue; const nc = cand.filter(p => seatOk(p, c)); if (nc.length < cand.length) { clues.push(c); cand = nc; } }
      if (cand.length !== 1 || clues.length < 3) throw new Error('retry');
      const ask = pick(['middle', 'left', 'right', 'rightof']), X = pick(sol.slice(0, 4));
      const ans = ask === 'middle' ? sol[2] : ask === 'left' ? sol[0] : ask === 'right' ? sol[4] : sol[sol.indexOf(X) + 1];
      const qq = { middle: 'Who sits in the middle?', left: 'Who sits at the extreme left?', right: 'Who sits at the extreme right?', rightof: `Who sits immediately to the right of ${X}?` }[ask];
      return QI(`Five friends — ${ppl.slice().sort().join(', ').replace(/, ([^,]*)$/, ' and $1')} — sit in a row facing north. ${clues.map(seatTxt).map(s => s[0].toUpperCase() + s.slice(1)).join('. ')}. ${qq}`, buildS(ans, ppl.filter(p => p !== ans && !(ask === 'rightof' && p === X))), 'Place the fixed clues first (ends, middle, “immediately left/right”), then test the remaining possibilities against every clue. Facing north, a person’s right is towards the east end of the row.', [`Only one arrangement satisfies every clue (left to right): ${sol.join(', ')}`, `${qq.replace('?', '')}: ${ans}`], { ppl, clues, ask, X });
    } });

  /* ---- Blood relations from a generated family tree ---- */
  function family() {
    const G = ['M', 'F'], P = {}; let id = 0; const mk = (g, f, m) => { const x = 'p' + (id++); P[x] = { g, f, m, sp: null }; return x; };
    const g1 = mk('M'), g2 = mk('F'); P[g1].sp = g2; P[g2].sp = g1;
    const c1 = mk(pick(G), g1, g2), c2 = mk(pick(G), g1, g2);
    const s1 = mk(P[c1].g === 'M' ? 'F' : 'M'); P[c1].sp = s1; P[s1].sp = c1; const s2 = mk(P[c2].g === 'M' ? 'F' : 'M'); P[c2].sp = s2; P[s2].sp = c2;
    const fa = x => P[x].g === 'M' ? x : P[x].sp, mo = x => P[x].g === 'F' ? x : P[x].sp;
    mk(pick(G), fa(c1), mo(c1)); mk(pick(G), fa(c1), mo(c1)); mk(pick(G), fa(c2), mo(c2));
    return P;
  }
  const famOps = P => {
    const ids = Object.keys(P), par = x => [P[x].f, P[x].m].filter(Boolean), kids = x => ids.filter(y => P[y].f === x || P[y].m === x), sp = x => P[x].sp ? [P[x].sp] : [], sib = x => ids.filter(y => y !== x && P[x].f && P[y].f === P[x].f);
    const fl = (xs, fn) => [...new Set(xs.flatMap(fn))];
    return { ids, par, kids, sp, sib, fl };
  };
  function relWord(P, a, b) {
    const { par, kids, sp, sib, fl } = famOps(P), g = P[a].g, M = g === 'M', has = (arr) => arr.includes(a);
    if (has(sp(b))) return M ? 'husband' : 'wife';
    if (has(par(b))) return M ? 'father' : 'mother';
    if (has(kids(b))) return M ? 'son' : 'daughter';
    if (has(sib(b))) return M ? 'brother' : 'sister';
    if (has(fl(par(b), par))) return M ? 'grandfather' : 'grandmother';
    if (has(fl(kids(b), kids))) return M ? 'grandson' : 'granddaughter';
    if (has(fl(par(b), sib)) || has(fl(fl(par(b), sib), sp))) return M ? 'uncle' : 'aunt';
    if (has(fl(sib(b), kids)) || has(fl(fl(sp(b), sib), kids))) return M ? 'nephew' : 'niece';
    if (has(fl(sp(b), par))) return M ? 'father-in-law' : 'mother-in-law';
    if (has(fl(kids(b), sp))) return M ? 'son-in-law' : 'daughter-in-law';
    if (has(fl(sp(b), sib)) || has(fl(sib(b), sp))) return M ? 'brother-in-law' : 'sister-in-law';
    if (has(fl(fl(par(b), sib), kids))) return 'cousin';
    return null;
  }
  const FLIP = { husband: 'wife', wife: 'husband', father: 'mother', mother: 'father', son: 'daughter', daughter: 'son', brother: 'sister', sister: 'brother', grandfather: 'grandmother', grandmother: 'grandfather', grandson: 'granddaughter', granddaughter: 'grandson', uncle: 'aunt', aunt: 'uncle', nephew: 'niece', niece: 'nephew', 'father-in-law': 'mother-in-law', 'mother-in-law': 'father-in-law', 'son-in-law': 'daughter-in-law', 'daughter-in-law': 'son-in-law', 'brother-in-law': 'sister-in-law', 'sister-in-law': 'brother-in-law', cousin: 'nephew' };
  const NEAR = { husband: ['brother', 'son-in-law'], wife: ['sister', 'daughter-in-law'], father: ['grandfather', 'uncle', 'father-in-law'], mother: ['grandmother', 'aunt', 'mother-in-law'], son: ['grandson', 'nephew', 'brother'], daughter: ['granddaughter', 'niece', 'sister'], brother: ['cousin', 'brother-in-law', 'son'], sister: ['cousin', 'sister-in-law', 'daughter'], grandfather: ['father', 'uncle'], grandmother: ['mother', 'aunt'], grandson: ['son', 'nephew'], granddaughter: ['daughter', 'niece'], uncle: ['father', 'cousin', 'brother-in-law'], aunt: ['mother', 'cousin', 'sister-in-law'], nephew: ['son', 'cousin', 'grandson'], niece: ['daughter', 'cousin', 'granddaughter'], 'father-in-law': ['father', 'uncle'], 'mother-in-law': ['mother', 'aunt'], 'son-in-law': ['son', 'nephew'], 'daughter-in-law': ['daughter', 'niece'], 'brother-in-law': ['brother', 'cousin'], 'sister-in-law': ['sister', 'cousin'], cousin: ['brother', 'sister', 'niece'] };
  def({ id: 'q_blood', unit: P3('ch12-u01'), name: 'Blood relations', concept: 'Relations from a chain of statements',
    make(d) {
      const P = family(), { ids, par, kids, sp, sib } = famOps(P), L = d === 'easy' ? 2 : R(2, 3);
      let path = [pick(ids)];
      for (let i = 0; i < L; i++) { const x = path[path.length - 1], nb = [...par(x), ...kids(x), ...sp(x), ...sib(x)].filter(y => !path.includes(y)); if (!nb.length) throw new Error('retry'); path.push(pick(nb)); }
      const ans = relWord(P, path[0], path[L]); if (!ans || ans === 'cousin' && L < 3) throw new Error('retry');
      const nm = sample(['P', 'Q', 'R', 'S', 'T', 'M', 'K'], L + 1), lab = Object.fromEntries(path.map((x, i) => [x, nm[i]]));
      const stm = path.slice(0, -1).map((x, i) => `${lab[x]} is the ${relWord(P, x, path[i + 1])} of ${lab[path[i + 1]]}`);
      return QI(`${stm.join('. ')}. How is ${nm[0]} related to ${nm[L]}?`, buildS(ans, [FLIP[ans], ...NEAR[ans]]), 'Draw a small family tree: mark gender (male/female), generations (up/down) and marriages, then read the relation of the first person to the last.', [...stm.map(s => s + ' (draw it)'), `So ${nm[0]} is the ${ans} of ${nm[L]}`], { P, path });
    } });

  /* ---- Statistics ---- */
  function classes(d) {
    const k = R(5, 7), h = pick([5, 10, 20]), s = pick([0, 10, 20, 30, 40]) * (h / 10 || 1), f = Array.from({ length: k }, () => R(2, 20));
    return { k, h, s, f, cl: f.map((x, i) => [s + i * h, s + (i + 1) * h]) };
  }
  const clTxt = c => c.cl.map(([a, b], i) => `${a}–${b}: ${c.f[i]}`).join(', ');
  def({ id: 'q_grouped_avg', unit: U('p3-ch14-u01'), name: 'Mean, median and mode (grouped)', concept: 'Averages of a frequency distribution',
    make(d) {
      const c = classes(d), N = c.f.reduce((a, b) => a + b, 0), v = pick(['mean', 'median', 'mode']);
      if (v === 'mean') { const fx = c.f.reduce((s, f, i) => s.add(F(f).mul(F(c.cl[i][0] + c.cl[i][1], 2))), F(0)), m = fx.div(N);
        return QI(`Find the arithmetic mean of the distribution (class: frequency): ${clTxt(c)}. (Correct to two decimals.)`, build(roundDp(m, 2), [roundDp(fx.div(c.k), 2), roundDp(c.f.reduce((s, f, i) => s.add(F(f * c.cl[i][0])), F(0)).div(N), 2), roundDp(c.f.reduce((s, f, i) => s.add(F(f * c.cl[i][1])), F(0)).div(N), 2)], d2), 'Mean = Σfx / N where x is the mid-value of each class.', [`Mid-values: ${c.cl.map(([a, b]) => num(F(a + b, 2))).join(', ')}`, `Σfx = ${num(fx)}; N = ${N}`, `Mean = ${num(fx)} ÷ ${N} ${ap(m, 2)}`], { v, cl: c.cl, f: c.f }); }
      let cum = 0, mi = 0; const cf = c.f.map(x => (cum += x)); while (F(cf[mi]).lt(F(N, 2))) mi++;
      if (v === 'median') { const C = mi ? cf[mi - 1] : 0, L1 = c.cl[mi][0], med = F(L1).add(F(N, 2).sub(C).div(c.f[mi]).mul(c.h));
        return QI(`Find the median of the distribution (class: frequency): ${clTxt(c)}. (Correct to two decimals.)`, build(roundDp(med, 2), [roundDp(F(L1).add(F(N + 1, 2).sub(C).div(c.f[mi]).mul(c.h)), 2), roundDp(F(c.cl[mi][1]).sub(F(N, 2).sub(C).div(c.f[mi]).mul(c.h)), 2), roundDp(F(L1).add(F(N, 2).div(c.f[mi]).mul(c.h)), 2), roundDp(F(L1 + c.cl[mi][1], 2), 2)], d2), 'Median = L₁ + (N/2 − C)/f × h, where L₁ is the lower boundary of the median class, C the cumulative frequency before it, f its frequency and h its width.', [`N/2 = ${num(F(N, 2))}; cumulative frequencies: ${cf.join(', ')}`, `Median class ${c.cl[mi][0]}–${c.cl[mi][1]}: L₁ = ${L1}, C = ${C}, f = ${c.f[mi]}, h = ${c.h}`, `Median = ${L1} + (${num(F(N, 2))} − ${C}) ÷ ${c.f[mi]} × ${c.h} ${ap(med, 2)}`], { v, cl: c.cl, f: c.f }); }
      const mx = Math.max(...c.f), mo = c.f.indexOf(mx); if (c.f.filter(x => x === mx).length > 1 || mo === 0 || mo === c.k - 1) throw new Error('retry');
      const f0 = c.f[mo - 1], f2 = c.f[mo + 1], den = 2 * mx - f0 - f2, L1 = c.cl[mo][0], mode = F(L1).add(F(mx - f0, den).mul(c.h));
      return QI(`Find the mode of the distribution (class: frequency): ${clTxt(c)}. (Correct to two decimals.)`, build(roundDp(mode, 2), [roundDp(F(L1).add(F(mx - f0, mx - f2).mul(c.h)), 2), roundDp(F(L1).add(F(mx - f2, den).mul(c.h)), 2), roundDp(F(L1 + c.cl[mo][1], 2), 2), roundDp(F(L1).add(F(mx - f0, 2 * mx).mul(c.h)), 2)], d2, { ok: x => F(x).sign >= 0 }), 'Mode = L₁ + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h for the modal class (highest frequency).', [`Modal class ${c.cl[mo][0]}–${c.cl[mo][1]}: f₁ = ${mx}, f₀ = ${f0}, f₂ = ${f2}`, `Mode = ${L1} + (${mx} − ${f0}) ÷ (2 × ${mx} − ${f0} − ${f2}) × ${c.h} ${ap(mode, 2)}`], { v, cl: c.cl, f: c.f });
    } });

  def({ id: 'q_raw_avg', unit: U('p3-ch14-u01'), name: 'Averages of raw data', concept: 'Mean, median, mode of ungrouped data',
    make(d) {
      const n = R(7, 11), xs = Array.from({ length: n }, () => R(10, 60)), md = pick(xs); xs.push(md, md); const cnt = {}; xs.forEach(x => cnt[x] = (cnt[x] || 0) + 1);
      const top = Math.max(...Object.values(cnt)); if (Object.values(cnt).filter(c => c === top).length > 1) throw new Error('retry');
      const s = xs.slice().sort((a, b) => a - b), N = s.length, med = N % 2 ? F(s[(N - 1) / 2]) : F(s[N / 2 - 1] + s[N / 2], 2), mean = F(xs.reduce((a, b) => a + b, 0), N), mode = F(+Object.keys(cnt).find(k => cnt[k] === top));
      const v = pick(['mean', 'median', 'mode']), corr = { mean, median: med, mode }[v];
      const f2 = x => badDp(x, 2) ? fixed(x, 2) : num(x); return QI(`For the data ${shuffle(xs).join(', ')}, find the ${v}${v === 'mean' ? ' (correct to two decimals)' : ''}.`, build(v === 'mean' ? roundDp(mean, 2) : corr, [mean, med, mode, F(s[Math.floor(N / 2)]), F(s[N - 1] + s[0], 2)].map(x => v === 'mean' ? roundDp(x, 2) : x), v === 'mean' ? d2 : f2), 'Mean = sum ÷ count; median = middle value of the sorted data (average of the two middle values if the count is even); mode = most frequent value.', v === 'mean' ? [`Sum = ${xs.reduce((a, b) => a + b, 0)}; n = ${N}`, `Mean = ${xs.reduce((a, b) => a + b, 0)} ÷ ${N} ${ap(mean, 2)}`] : v === 'median' ? [`Sorted: ${s.join(', ')}`, `n = ${N}; median = ${N % 2 ? `${(N + 1) / 2}th value` : `average of the ${N / 2}th and ${N / 2 + 1}th values`} = ${nf(med)}`] : [`${nf(mode)} occurs ${top} times, more than any other value`], { v, xs });
    } });

  def({ id: 'q_quartile', unit: U('p3-ch14-u01'), name: 'Quartiles and quartile deviation', concept: 'Partition values of ungrouped data',
    make(d) {
      const n = R(7, 15), xs = [...new Set(Array.from({ length: n + 3 }, () => R(5, 99)))].slice(0, n); if (xs.length < 7) throw new Error('retry');
      const s = xs.slice().sort((a, b) => a - b), N = s.length, at = p => { const pos = F(N + 1).mul(p), i = Number(pos.n / pos.d), fr2 = pos.sub(i); if (i < 1) return F(s[0]); if (i >= N) return F(s[N - 1]); return F(s[i - 1]).add(fr2.mul(s[i] - s[i - 1])); };
      const Q1 = at(F(1, 4)), Q3 = at(F(3, 4)), v = pick(['q1', 'q3', 'qd', 'cqd']), QD = Q3.sub(Q1).div(2), CQ = Q3.sub(Q1).div(Q3.add(Q1)).mul(100);
      const corr = { q1: Q1, q3: Q3, qd: QD, cqd: roundDp(CQ, 2) }[v];
      const lab = { q1: 'first quartile (Q₁)', q3: 'third quartile (Q₃)', qd: 'quartile deviation', cqd: 'coefficient of quartile deviation (in %, correct to two decimals)' }[v];
      return QI(`Find the ${lab} of: ${xs.join(', ')}.`, build(corr, v === 'cqd' ? [roundDp(QD.div(Q3.add(Q1)).mul(100), 2), roundDp(Q3.sub(Q1), 2), roundDp(QD, 2)] : v === 'qd' ? [Q3.sub(Q1), Q3.add(Q1).div(2), Q3.sub(Q1).div(4)] : [at(F(1, 2)), F(s[Math.floor(N * (v === 'q1' ? 1 : 3) / 4)]), v === 'q1' ? Q3 : Q1, F(N + 1, 4)], v === 'cqd' ? d2 : nf), 'For n ungrouped values, Q₁ is the (n + 1)/4-th and Q₃ the 3(n + 1)/4-th value of the sorted data (interpolate between neighbours). QD = (Q₃ − Q₁)/2; coefficient = (Q₃ − Q₁)/(Q₃ + Q₁) × 100.', [`Sorted (n = ${N}): ${s.join(', ')}`, `Q₁ position (${N} + 1)/4 = ${nf(F(N + 1, 4))} → Q₁ = ${nf(Q1)}`, `Q₃ position 3(${N} + 1)/4 = ${nf(F(3 * (N + 1), 4))} → Q₃ = ${nf(Q3)}`, ...(v === 'qd' ? [`QD = (${nf(Q3)} − ${nf(Q1)}) ÷ 2 = ${nf(QD)}`] : v === 'cqd' ? [`Coefficient = (${nf(Q3)} − ${nf(Q1)}) ÷ (${nf(Q3)} + ${nf(Q1)}) × 100 ${ap(CQ, 2)}`] : [])], { v, xs });
    } });

  def({ id: 'q_dispersion', unit: U('p3-ch14-u02'), name: 'Standard deviation, CV, range, MD', concept: 'Measures of dispersion',
    make(d) {
      const n = R(5, 8), xs = Array.from({ length: n }, () => R(2, 40)), v = pick(['sd', 'var', 'cv', 'range', 'md', 'lin']);
      const m = F(xs.reduce((a, b) => a + b, 0), n), vr = xs.reduce((s, x) => s.add(F(x).sub(m).pow(2)), F(0)).div(n);
      if (vr.sign === 0) throw new Error('retry');
      if (v === 'range') { const L = Math.max(...xs), S = Math.min(...xs); if (L + S === 0) throw new Error('retry'); const cr = F(L - S, L + S).mul(100); return QI(`Find the coefficient of range (%) of: ${xs.join(', ')}. (Correct to two decimals.)`, build(roundDp(cr, 2), [F(L - S), roundDp(F(L - S, L).mul(100), 2), roundDp(F(L - S, S || 1).mul(100), 2), roundDp(F(L + S, L - S || 1), 2)], d2), 'Range = L − S; coefficient of range = (L − S)/(L + S) × 100.', [`L = ${L}, S = ${S}`, `(${L} − ${S}) ÷ (${L} + ${S}) × 100 ${ap(cr, 2)}`], { v, xs }); }
      if (v === 'md') { const md = xs.reduce((s, x) => s.add(F(x).sub(m).abs()), F(0)).div(n); return QI(`Find the mean deviation about the mean of: ${xs.join(', ')}. (Correct to two decimals.)`, build(roundDp(md, 2), [roundDp(sqrtRound(vr, 4), 2), roundDp(xs.reduce((s, x) => s.add(F(x).sub(m).abs()), F(0)).div(n - 1), 2), roundDp(md.mul(2), 2), roundDp(m, 2)], d2), 'MD about mean = Σ|x − x̄| / n.', [`Mean = ${xs.reduce((a, b) => a + b, 0)} ÷ ${n} ${ap(m, 4)}`, `Σ|x − x̄| ${ap(md.mul(n), 4)}`, `MD = ${fixed(md.mul(n), 4)} ÷ ${n} ${ap(md, 2)}`], { v, xs }); }
      if (v === 'lin') { const sd = pick([2, 3, 4, 5, 6, 8, 10]), a = R(-5, 5), b = R(-20, 20); if (!a) throw new Error('retry'); return QI(`The standard deviation of x is ${sd}. What is the standard deviation of y = ${poly([a, b])}?`, buildN(F(Math.abs(a) * sd), [F(a * sd), F(Math.abs(a * sd + b)), F(sd), F(a * a * sd)], { ok: x => true }), 'SD is unaffected by a change of origin (adding b) but is multiplied by |a| under a change of scale.', [`Adding ${pn(b)} does not change SD; multiplying by ${pn(a)} multiplies SD by ${Math.abs(a)}`, `SD(y) = ${Math.abs(a)} × ${sd} = ${Math.abs(a) * sd}`], { v, sd, a, b }); }
      const sdv = sqrtRound(vr, 2), steps = [`Mean = ${xs.reduce((a, b) => a + b, 0)} ÷ ${n} ${ap(m, 4)}`, `Variance = Σ(x − x̄)² ÷ n ${ap(vr, 4)}`];
      if (v === 'var') return QI(`Find the variance of: ${xs.join(', ')}. (Correct to two decimals.)`, build(roundDp(vr, 2), [roundDp(vr.mul(n).div(n - 1), 2), sdv, roundDp(vr.mul(n), 2), roundDp(m, 2)], d2), 'Variance = Σ(x − x̄)²/n (ICAI uses n).', steps, { v, xs });
      if (v === 'sd') return QI(`Find the standard deviation of: ${xs.join(', ')}. (Correct to two decimals.)`, build(sdv, [roundDp(vr, 2), sqrtRound(vr.mul(n).div(n - 1), 2), roundDp(xs.reduce((s, x) => s.add(F(x).sub(m).abs()), F(0)).div(n), 2), sqrtRound(vr.div(n), 2)], d2), 'SD = √[Σ(x − x̄)²/n].', [...steps, `SD = √${fixed(vr, 4)} ≈ ${d2(sdv)}`], { v, xs });
      const cv = sqrtRound(vr.mul(10000).div(m.mul(m)), 2);
      return QI(`Find the coefficient of variation (%) of: ${xs.join(', ')}. (Correct to two decimals.)`, build(cv, [roundDp(vr.div(m).mul(100), 2), roundDp(m.div(sqrtRound(vr, 6)).mul(100), 2), sdv, sqrtRound(vr.mul(10000).div(m.mul(m)).mul(n).div(n - 1), 2)], x => d2(x) + '%'), 'CV = SD/mean × 100.', [...steps, `CV = √${fixed(vr, 4)} ÷ ${fixed(m, 4)} × 100 ≈ ${d2(cv)}`], { v, xs });
    } });

  /* ---- Probability ---- */
  const frB = x => fr(F(x));
  def({ id: 'q_prob_dice', unit: U('p3-ch15-u01'), name: 'Probability — dice', concept: 'Equally likely outcomes with two dice',
    make(d) {
      const E = [
        ['sum', () => { const k = R(3, 11); return [`the sum is ${k}`, (a, b) => a + b === k]; }],
        ['sumge', () => { const k = R(4, 11); return [`the sum is at least ${k}`, (a, b) => a + b >= k]; }],
        ['doub', () => ['both dice show the same number', (a, b) => a === b]],
        ['prime', () => ['the sum is a prime number', (a, b) => [2, 3, 5, 7, 11].includes(a + b)]],
        ['prodeven', () => ['the product is even', (a, b) => (a * b) % 2 === 0]],
        ['six', () => ['at least one die shows 6', (a, b) => a === 6 || b === 6]],
        ['diff', () => { const k = R(1, 4); return [`the difference of the numbers is ${k}`, (a, b) => Math.abs(a - b) === k]; }]];
      const [key, gen] = pick(E), [txt, fn] = gen(); let c = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (fn(a, b)) c++;
      const p = F(c, 36);
      return QI(`Two fair dice are thrown. What is the probability that ${txt}?`, build(p, [F(c, 6 * 6 - c || 1), F(Math.max(1, c - 1), 36), F(c + 1, 36), F(36 - c, 36), F(c, 12)], frB, { ok: x => F(x).sign > 0 && !F(x).gt(1) }), 'With two dice there are 6 × 6 = 36 equally likely outcomes; count the favourable ones.', [`Total outcomes = 36`, `Favourable outcomes (${txt}) = ${c}`, `P = ${c}/36 = ${fr(p)}`], { key, txt });
    } });

  const SUITS = ['hearts', 'diamonds', 'clubs', 'spades'], RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'];
  const DECK = SUITS.flatMap(s => RANKS.map(r => ({ s, r, red: s === 'hearts' || s === 'diamonds', face: ['jack', 'queen', 'king'].includes(r) })));
  def({ id: 'q_prob_cards', unit: U('p3-ch15-u01'), name: 'Probability — cards', concept: 'Events from a pack of 52 cards',
    make(d) {
      const one = chance(.6);
      if (one) {
        const r = pick(['king', 'queen', 'ace', 'jack', '7']), s = pick(SUITS), opts = [
          [`a ${r} or a ${s.slice(0, -1)}`, c => c.r === r || c.s === s], ['a face card', c => c.face], ['a red face card', c => c.red && c.face], [`a black ${r}`, c => !c.red && c.r === r], [`neither a ${s.slice(0, -1)} nor a ${r}`, c => c.s !== s && c.r !== r], ['a red card or a face card', c => c.red || c.face]];
        const [txt, fn] = pick(opts), c = DECK.filter(fn).length, p = F(c, 52);
        return QI(`A card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it is ${txt}?`, build(p, [F(c + (/ or /.test(txt) ? 1 : -1), 52), F(c, 13), F(52 - c, 52), F(4, 52).add(F(13, 52))], frB, { ok: x => F(x).sign > 0 && !F(x).gt(1) }), 'P(A or B) = P(A) + P(B) − P(A and B); count cards carefully so that none is counted twice.', [`Favourable cards = ${c}`, `P = ${c}/52 = ${fr(p)}`], { one, txt });
      }
      const opts = [['both are aces', (a, b) => a.r === 'ace' && b.r === 'ace'], ['both are red', (a, b) => a.red && b.red], ['one is a king and the other a queen', (a, b) => (a.r === 'king' && b.r === 'queen') || (a.r === 'queen' && b.r === 'king')], ['both are of the same suit', (a, b) => a.s === b.s], ['both are face cards', (a, b) => a.face && b.face]];
      const [txt, fn] = pick(opts); let c = 0; for (let i = 0; i < 52; i++) for (let j = i + 1; j < 52; j++) if (fn(DECK[i], DECK[j])) c++;
      const p = F(c, 1326);
      return QI(`Two cards are drawn together at random from a pack of 52. What is the probability that ${txt}?`, build(p, [p.mul(2), F(c, 52 * 52), F(c, 2652), F(1).sub(p)], frB, { ok: x => F(x).sign > 0 && F(x).lt(1) }), 'Two cards drawn together: total ways = ⁵²C₂ = 1,326; count the favourable pairs with combinations.', [`Total ways = 52C2 = 1,326`, `Favourable pairs = ${c}`, `P = ${c}/1,326 = ${fr(p)}`], { one, txt });
    } });

  def({ id: 'q_prob_urn', unit: U('p3-ch15-u01'), name: 'Probability — balls from a bag', concept: 'Drawing without replacement',
    make(d) {
      const r = R(2, 8), b = R(2, 8), g = R(0, 6), N = r + b + g, v = pick(['bothr', 'onerb', 'atl']), tot = nCr(N, 2);
      const fav = v === 'bothr' ? nCr(r, 2) : v === 'onerb' ? BI(r * b) : tot - nCr(N - r, 2), p = F(fav, tot);
      const txt = { bothr: 'both are red', onerb: 'one is red and the other blue', atl: 'at least one is red' }[v];
      return QI(`A bag has ${r} red, ${b} blue${g ? ` and ${g} green` : ''} balls. Two balls are drawn at random (without replacement). What is the probability that ${txt}?`, build(p, [F(r * r, N * N), F(r, N).mul(F(r, N)).mul(v === 'onerb' ? 2 : 1), F(fav, N * N), F(1).sub(p), F(r, N)], frB, { ok: x => F(x).sign > 0 && F(x).lt(1) }), 'Count selections with combinations: total = ⁿC₂; “at least one” = 1 − P(none).', [`Total ways = ${N}C2 = ${ind(tot)}`, v === 'bothr' ? `Both red: ${r}C2 = ${ind(fav)}` : v === 'onerb' ? `One red and one blue: ${r} × ${b} = ${ind(fav)}` : `No red: ${N - r}C2 = ${ind(nCr(N - r, 2))}; at least one red = ${ind(tot)} − ${ind(nCr(N - r, 2))} = ${ind(fav)}`, `P = ${ind(fav)}/${ind(tot)} = ${fr(p)}`], { r, b, g, v });
    } });

  def({ id: 'q_prob_rules', unit: U('p3-ch15-u01'), name: 'Addition and conditional probability', concept: 'P(A ∪ B), P(A | B), independence',
    make(d) {
      const D0 = pick([10, 12, 20, 24, 30]), a = R(2, D0 - 2), b = R(2, D0 - 2), ab = R(1, Math.min(a, b) - 1), v = pick(['union', 'cond', 'neither', 'onlyA']); if (a + b - ab > D0) throw new Error('retry');
      const pA = F(a, D0), pB = F(b, D0), pAB = F(ab, D0), corr = { union: pA.add(pB).sub(pAB), cond: pAB.div(pB), neither: F(1).sub(pA.add(pB).sub(pAB)), onlyA: pA.sub(pAB) }[v];
      const ask = { union: 'P(A ∪ B)', cond: 'P(A | B)', neither: 'P(neither A nor B)', onlyA: 'P(A but not B)' }[v];
      return QI(`P(A) = ${fr(pA)}, P(B) = ${fr(pB)} and P(A ∩ B) = ${fr(pAB)}. Find ${ask}.`, build(corr, [pA.add(pB), pAB.div(pA), F(1).sub(pAB), pA.mul(pB), pA.sub(pB).abs(), pA.add(pB).sub(pAB)], frB, { ok: x => F(x).sign > 0 && !F(x).gt(1) }), 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B); P(A | B) = P(A ∩ B)/P(B); P(neither) = 1 − P(A ∪ B).', v === 'cond' ? [`P(A | B) = ${pf(pAB)} ÷ ${pf(pB)} = ${fr(corr)}`] : v === 'onlyA' ? [`P(A ∩ B′) = ${fr(pA)} − ${fr(pAB)} = ${fr(corr)}`] : [`P(A ∪ B) = ${fr(pA)} + ${fr(pB)} − ${fr(pAB)} = ${fr(pA.add(pB).sub(pAB))}`, ...(v === 'neither' ? [`P(neither) = 1 − ${fr(pA.add(pB).sub(pAB))} = ${fr(corr)}`] : [])], { D0, a, b, ab, v });
    } });

  def({ id: 'q_expectation', unit: U('p3-ch15-u01'), name: 'Expected value', concept: 'Mathematical expectation of a random variable',
    make(d) {
      const k = R(3, 4), D0 = pick([10, 12, 20]), xs = [...new Set(Array.from({ length: k + 3 }, () => R(-3, 10)))].slice(0, k).sort((a, b) => a - b); if (xs.length < 3) throw new Error('retry');
      const w = xs.map(() => R(1, 5)), W = w.reduce((s, x) => s + x, 0), ps = w.map(x => F(x, W)), v = pick(['mean', 'var']);
      const E = xs.reduce((s, x, i) => s.add(ps[i].mul(x)), F(0)), E2 = xs.reduce((s, x, i) => s.add(ps[i].mul(x * x)), F(0)), V = E2.sub(E.mul(E));
      const corr = v === 'mean' ? E : V;
      return QI(`A random variable X takes values ${xs.join(', ')} with probabilities ${ps.map(fr).join(', ')} respectively. Find ${v === 'mean' ? 'E(X)' : 'Var(X)'}.`.replace(/(^|[ ,])-(\d)/g, '$1−$2'), build(corr, v === 'mean' ? [F(xs.reduce((a, b) => a + b, 0), xs.length), E2, E.add(1)] : [E2, E.mul(E), V.add(E)], frB), 'E(X) = Σ x·p; Var(X) = E(X²) − [E(X)]².', [`E(X) = Σ x·p = ${fr(E)}`, ...(v === 'var' ? [`E(X²) = Σ x²·p = ${fr(E2)}`, `Var(X) = ${fr(E2)} − (${fr(E)})² = ${fr(V)}`] : [])], { xs, w, v });
    } });

  const PFR = [F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5), F(3, 4), F(2, 5), F(1, 6)];
  def({ id: 'q_binomial', unit: U('p3-ch16-u01'), name: 'Binomial distribution', concept: 'P(X = r) = ⁿCᵣ pʳ qⁿ⁻ʳ; mean np, variance npq',
    make(d) {
      const n = R(3, 8), p = pick(PFR), q = F(1).sub(p), v = pick(['exact', 'atl1', 'params', 'findn']);
      if (v === 'params') { const ask = pick(['mean', 'var']), val = ask === 'mean' ? p.mul(n) : p.mul(q).mul(n); return QI(`For a binomial distribution with n = ${n} and p = ${fr(p)}, find the ${ask === 'mean' ? 'mean' : 'variance'}.`, build(val, [ask === 'mean' ? p.mul(q).mul(n) : p.mul(n), q.mul(n), p.mul(q), val.add(1)], frB), 'Mean = np; variance = npq (q = 1 − p).', [ask === 'mean' ? `Mean = ${n} × ${fr(p)} = ${fr(val)}` : `Variance = ${n} × ${fr(p)} × ${fr(q)} = ${fr(val)}`], { v, n, p: fr(p), ask }); }
      if (v === 'findn') { const N = R(4, 40), mean = p.mul(N), vr = mean.mul(q); return QI(`The mean of a binomial distribution is ${fr(mean)} and its variance is ${fr(vr)}. Find n.`, buildN(F(N), [mean.div(q), F(N + 1), mean.div(vr), vr.div(p)], { ok: x => F(x).sign > 0 }), 'q = variance/mean, p = 1 − q, n = mean/p.', [`q = ${pf(vr)} ÷ ${pf(mean)} = ${fr(q)}`, `p = 1 − ${fr(q)} = ${fr(p)}`, `n = ${pf(mean)} ÷ ${pf(p)} = ${N}`], { v, N, p: fr(p) }); }
      if (v === 'atl1') { const val = F(1).sub(q.pow(n)); if (q.pow(n).d > 10000n) throw new Error('retry'); return QI(`A trial succeeds with probability ${fr(p)}. In ${n} independent trials, what is the probability of at least one success?`, build(val, [q.pow(n), p.mul(n), F(1).sub(p.pow(n)), F(n).mul(p).mul(q.pow(n - 1))], frB, { ok: x => F(x).sign > 0 && F(x).lt(1) }), 'P(at least one) = 1 − P(none) = 1 − qⁿ.', [`P(none) = (${fr(q)})${sup(n)} = ${fr(q.pow(n))}`, `P(at least one) = 1 − ${fr(q.pow(n))} = ${fr(val)}`], { v, n, p: fr(p) }); }
      const r = R(0, n), val = F(nCr(n, r)).mul(p.pow(r)).mul(q.pow(n - r)); if (val.d > 50000n) throw new Error('retry');
      return QI(`X follows a binomial distribution with n = ${n} and p = ${fr(p)}. Find P(X = ${r}).`, build(val, [p.pow(r).mul(q.pow(n - r)), F(nCr(n, r)).mul(p.pow(n - r)).mul(q.pow(r)), F(nPr(n, r)).mul(p.pow(r)).mul(q.pow(n - r)), F(nCr(n, r)).mul(p.pow(r))], frB, { ok: x => F(x).sign > 0 && !F(x).gt(1) }), 'P(X = r) = ⁿCᵣ pʳ qⁿ⁻ʳ.', [`${n}C${r} = ${ind(nCr(n, r))}`, `P = ${ind(nCr(n, r))} × (${fr(p)})${sup(r)} × (${fr(q)})${sup(n - r)} = ${fr(val)}`], { v, n, p: fr(p), r });
    } });

  def({ id: 'q_poisson', unit: U('p3-ch16-u01'), name: 'Poisson distribution', concept: 'P(X = r) = e⁻ᵐ mʳ / r!',
    make(d) {
      const m = pick(['0.2', '0.5', '0.8', '1', '1.2', '1.5', '2', '2.5', '3', '3.5', '4', '5']), e = F(fixed(F(Math.round(Math.exp(-Number(m)) * 10000), 10000), 4).replace('−', '-')), mm = F(m), v = pick(['eq', 'eq', 'le1', 'ge1']);
      const P = r => e.mul(mm.pow(r)).div(F(fact(r)));
      if (v === 'eq') { const r = R(0, 5), val = P(r); return QI(`X follows a Poisson distribution with mean ${m}. Find P(X = ${r}). (Take e^(−${m}) = ${fixed(e, 4)}; answer to four decimals.)`, build(roundDp(val, 4), [roundDp(e.mul(mm.pow(r)), 4), roundDp(P(r + 1), 4), roundDp(F(1).sub(val), 4), roundDp(r ? P(r - 1) : P(2), 4)], d4), 'P(X = r) = e⁻ᵐ mʳ / r!.', [`P(X = ${r}) = ${fixed(e, 4)} × ${m}${sup(r)} ÷ ${r}!`, `= ${fixed(e, 4)} × ${num(mm.pow(r))} ÷ ${ind(fact(r))} ${ap(val, 4)}`], { v, m, r, e: fixed(e, 4) }); }
      const le1 = P(0).add(P(1)), val = v === 'le1' ? le1 : F(1).sub(P(0));
      return QI(`X follows a Poisson distribution with mean ${m}. Find ${v === 'le1' ? 'P(X ≤ 1)' : 'P(X ≥ 1)'}. (Take e^(−${m}) = ${fixed(e, 4)}; answer to four decimals.)`, build(roundDp(val, 4), v === 'le1' ? [roundDp(P(1), 4), roundDp(F(1).sub(le1), 4), roundDp(P(0).add(P(1)).add(P(2)), 4)] : [roundDp(P(0), 4), roundDp(F(1).sub(le1), 4), roundDp(P(1), 4)], d4), v === 'le1' ? 'P(X ≤ 1) = P(0) + P(1).' : 'P(X ≥ 1) = 1 − P(0) = 1 − e⁻ᵐ.', v === 'le1' ? [`P(0) = ${fixed(e, 4)}; P(1) = ${fixed(e, 4)} × ${m} ${ap(P(1), 4)}`, `P(X ≤ 1) = ${fixed(e, 4)} + ${fixed(P(1), 4)} ${ap(val, 4)}`] : [`P(X ≥ 1) = 1 − ${fixed(e, 4)} = ${fixed(val, 4)}`], { v, m, e: fixed(e, 4) });
    } });

  /* ---- Correlation and regression ---- */
  const r2s = x => (F(x).sign < 0 ? '−' : '') + fixed(F(x).abs(), 2);
  function corrR(xs, ys) {
    const n = xs.length, mx = F(xs.reduce((a, b) => a + b, 0), n), my = F(ys.reduce((a, b) => a + b, 0), n);
    let sxy = F(0), sxx = F(0), syy = F(0); xs.forEach((x, i) => { const dx = F(x).sub(mx), dy = F(ys[i]).sub(my); sxy = sxy.add(dx.mul(dy)); sxx = sxx.add(dx.mul(dx)); syy = syy.add(dy.mul(dy)); });
    return { mx, my, sxy, sxx, syy };
  }
  const rRound = (sxy, sxx, syy) => { const r2 = sxy.mul(sxy).div(sxx.mul(syy)), a = sqrtRound(r2, 2); return sxy.sign < 0 ? a.neg() : a; };
  def({ id: 'q_karl_pearson', unit: U('p3-ch17-u01'), name: 'Karl Pearson’s correlation', concept: 'r = cov(x, y)/(σx σy)',
    make(d) {
      if (chance(.35)) { const sx = R(2, 12), sy = R(2, 12), r = pick(['0.4', '0.5', '0.6', '0.75', '0.8', '-0.5', '-0.6', '-0.8', '0.9', '-0.25']), cov = F(r).mul(sx * sy); if (badDp(cov, 2)) throw new Error('retry');
        return QI(`The covariance between x and y is ${num(cov)}, σx = ${sx} and σy = ${sy}. Find the correlation coefficient.`, build(F(r), [cov.div(sx), cov.div(sx + sy), F(r).neg(), cov.div(sx * sx)], x => num(x), { ok: x => !F(x).abs().gt(1) }), 'r = cov(x, y)/(σx σy).', [`r = ${num(cov)} ÷ (${sx} × ${sy}) = ${num(F(r))}`], { v: 'cov', sx, sy, r }); }
      const n = R(5, 6), xs = Array.from({ length: n }, () => R(1, 20)), sgnr = pick([1, -1]), ys = xs.map(x => sgnr * x + R(-6, 6) + 20);
      const c = corrR(xs, ys); if (c.sxx.sign === 0 || c.syy.sign === 0) throw new Error('retry'); const r = rRound(c.sxy, c.sxx, c.syy);
      return QI(`Find Karl Pearson’s coefficient of correlation (correct to two decimals) for: x = ${xs.join(', ')}; y = ${ys.join(', ')}.`, build(r, [r.neg(), rRound(c.sxy, c.sxx, c.sxx), roundDp(c.sxy.div(c.sxx), 2), roundDp(c.sxy.div(c.syy), 2)], r2s, { ok: x => !F(x).abs().gt(1) }), 'r = Σ(x − x̄)(y − ȳ) / √[Σ(x − x̄)² Σ(y − ȳ)²].', [`x̄ = ${nf(c.mx)}, ȳ = ${nf(c.my)}`, `Σdxdy = ${nf(c.sxy)}, Σdx² = ${nf(c.sxx)}, Σdy² = ${nf(c.syy)}`, `r = ${nf(c.sxy)} ÷ √(${nf(c.sxx)} × ${nf(c.syy)}) ≈ ${r2s(r)}`], { v: 'data', xs, ys });
    } });

  def({ id: 'q_rank_corr', unit: U('p3-ch17-u01'), name: 'Spearman’s rank correlation', concept: 'R = 1 − 6Σd²/[n(n² − 1)]',
    make(d) {
      const n = R(5, 9), r1 = shuffle(Array.from({ length: n }, (_, i) => i + 1)), r2 = shuffle(Array.from({ length: n }, (_, i) => i + 1)), d2s = r1.reduce((s, x, i) => s + (x - r2[i]) ** 2, 0), R0 = F(1).sub(F(6 * d2s, n * (n * n - 1)));
      if (chance(.4)) { return QI(`For ${n} pairs of ranks, Σd² = ${d2s}. Find the rank correlation coefficient (correct to two decimals).`, build(roundDp(R0, 2), [roundDp(F(6 * d2s, n * (n * n - 1)), 2), roundDp(F(1).sub(F(6 * d2s, n * n * n)), 2), roundDp(F(1).sub(F(d2s, n * (n * n - 1))), 2), roundDp(F(1).sub(F(6 * d2s, n * (n * n + 1))), 2)], r2s), 'R = 1 − 6Σd²/[n(n² − 1)].', [`R = 1 − 6 × ${d2s} ÷ (${n} × (${n}² − 1))`, `R = 1 − ${6 * d2s} ÷ ${n * (n * n - 1)} ${ap(R0, 2)}`], { v: 'given', n, d2s }); }
      return QI(`Two judges ranked ${n} candidates. Judge 1: ${r1.join(', ')}; Judge 2: ${r2.join(', ')}. Find the rank correlation coefficient (correct to two decimals).`, build(roundDp(R0, 2), [roundDp(F(6 * d2s, n * (n * n - 1)), 2), roundDp(F(1).sub(F(6 * d2s, n * n * n)), 2), roundDp(R0.neg(), 2), roundDp(F(1).sub(F(d2s, n * (n * n - 1))), 2)], r2s), 'R = 1 − 6Σd²/[n(n² − 1)], d = difference of ranks.', [`d: ${r1.map((x, i) => x - r2[i]).join(', ')}`.replace(/-/g, '−'), `Σd² = ${d2s}`, `R = 1 − 6 × ${d2s} ÷ (${n} × (${n}² − 1)) ${ap(R0, 2)}`], { v: 'ranks', r1, r2 });
    } });

  def({ id: 'q_regression', unit: U('p3-ch17-u01'), name: 'Regression lines and estimates', concept: 'byx = r σy/σx; lines pass through the means',
    make(d) {
      const v = pick(['estimate', 'coef', 'lines']);
      if (v === 'lines') {
        const prs = [['0.8', '0.45', '0.6'], ['0.5', '0.5', '0.5'], ['0.4', '0.9', '0.6'], ['1.2', '0.3', '0.6'], ['0.6', '0.6', '0.6'], ['0.25', '1', '0.5'], ['0.9', '0.4', '0.6'], ['0.8', '0.8', '0.8']], [b, dd, r] = pick(prs), mx = R(5, 60), my = R(5, 60), neg = chance(.4);
        const B = F(b).mul(neg ? -1 : 1), Dd = F(dd).mul(neg ? -1 : 1), a = F(my).sub(B.mul(mx)), c = F(mx).sub(Dd.mul(my)), ask = pick(['r', 'mx', 'my']);
        const corr = ask === 'r' ? F(r).mul(neg ? -1 : 1) : ask === 'mx' ? F(mx) : F(my);
        const ln1 = `y = ${num(a)} ${B.sign < 0 ? '−' : '+'} ${num(B.abs())}x`, ln2 = `x = ${num(c)} ${Dd.sign < 0 ? '−' : '+'} ${num(Dd.abs())}y`;
        return QI(`The regression line of y on x is ${ln1} and that of x on y is ${ln2}. Find ${ask === 'r' ? 'the correlation coefficient r' : ask === 'mx' ? 'the mean of x' : 'the mean of y'}.`, build(corr, ask === 'r' ? [corr.neg(), B.mul(Dd), B.add(Dd).div(2), B] : [F(ask === 'mx' ? my : mx), corr.add(1), ask === 'mx' ? c : a], x => num(x), { ok: x => ask !== 'r' || !F(x).abs().gt(1) }), 'Both regression lines pass through (x̄, ȳ); r = ±√(byx × bxy), taking the common sign of the two coefficients.', ask === 'r' ? [`byx = ${num(B)}, bxy = ${num(Dd)}`, `r² = ${num(B)} × ${num(Dd)} = ${num(B.mul(Dd))}`, `r = ${num(corr)} (same sign as the coefficients)`] : [`Solve the two equations together`, `x̄ = ${mx}, ȳ = ${my}`], { v, b, dd, mx, my, neg, ask });
      }
      const sx = R(2, 10), sy = R(2, 15), r = pick(['0.4', '0.5', '0.6', '0.75', '0.8', '-0.5', '-0.6', '-0.4', '0.9']), mx = R(10, 80), my = R(10, 80), byx = F(r).mul(sy).div(sx), bxy = F(r).mul(sx).div(sy);
      if (v === 'coef') { const ask = pick(['byx', 'bxy']), val = ask === 'byx' ? byx : bxy; if (badDp(val, 4)) throw new Error('retry'); return QI(`r = ${r.replace('-', '−')}, σx = ${sx}, σy = ${sy}. Find the regression coefficient ${ask === 'byx' ? 'of y on x (byx)' : 'of x on y (bxy)'}.`, buildN(val, [ask === 'byx' ? bxy : byx, F(r).mul(sx * sy), F(r).mul(sy).div(sx).neg(), F(sy, sx)]), 'byx = r σy/σx; bxy = r σx/σy.', [ask === 'byx' ? `byx = ${num(F(r))} × ${sy} ÷ ${sx} = ${nf(val)}` : `bxy = ${num(F(r))} × ${sx} ÷ ${sy} = ${nf(val)}`], { v, sx, sy, r, ask }); }
      const x0 = mx + R(-10, 10), est = F(my).add(byx.mul(x0 - mx)); if (badDp(est, 2)) throw new Error('retry');
      return QI(`x̄ = ${mx}, ȳ = ${my}, σx = ${sx}, σy = ${sy} and r = ${r.replace('-', '−')}. Estimate y when x = ${x0}.`, buildN(est, [F(my).add(bxy.mul(x0 - mx)), F(my).add(F(r).mul(x0 - mx)), F(mx).add(byx.mul(x0 - my)), est.add(byx)]), 'Regression of y on x: y − ȳ = byx (x − x̄), byx = r σy/σx.', [`byx = ${num(F(r))} × ${sy} ÷ ${sx} = ${nf(byx)}`, `y = ${my} + ${pn(byx)} × (${x0} − ${mx}) = ${nf(est)}`], { v, sx, sy, r, mx, my, x0 });
    } });

  def({ id: 'q_index_numbers', unit: U('p3-ch18-u01'), name: 'Index numbers', concept: 'Laspeyres, Paasche, Fisher and other price indices',
    make(d) {
      const k = R(3, 4), rows = Array.from({ length: k }, (_, i) => ({ n: 'ABCD'[i], p0: R(2, 40), q0: R(2, 30) })); rows.forEach(r => { r.p1 = r.p0 + R(-2, 15); r.q1 = r.q0 + R(-3, 10); }); if (rows.some(r => r.p1 <= 0 || r.q1 <= 0)) throw new Error('retry');
      const S = f => rows.reduce((s, r) => s + f(r), 0), p1q0 = S(r => r.p1 * r.q0), p0q0 = S(r => r.p0 * r.q0), p1q1 = S(r => r.p1 * r.q1), p0q1 = S(r => r.p0 * r.q1);
      const L = F(p1q0, p0q0).mul(100), Pa = F(p1q1, p0q1).mul(100), Fi = sqrtRound(L.mul(Pa), 2), ME = F(p1q0 + p1q1, p0q0 + p0q1).mul(100), SA = F(S(r => r.p1), S(r => r.p0)).mul(100);
      const v = pick(['L', 'P', 'F', 'ME', 'SA']), corr = { L: roundDp(L, 2), P: roundDp(Pa, 2), F: Fi, ME: roundDp(ME, 2), SA: roundDp(SA, 2) }[v];
      const nm = { L: 'Laspeyres’ price index', P: 'Paasche’s price index', F: 'Fisher’s ideal price index', ME: 'Marshall–Edgeworth price index', SA: 'simple aggregative price index' }[v];
      const tbl = rows.map(r => `${r.n}: p₀ ${r.p0}, q₀ ${r.q0}, p₁ ${r.p1}, q₁ ${r.q1}`).join('; ');
      const steps = { L: [`Σp₁q₀ = ${ind(p1q0)}, Σp₀q₀ = ${ind(p0q0)}`, `L = ${ind(p1q0)} ÷ ${ind(p0q0)} × 100 ${ap(L, 2)}`], P: [`Σp₁q₁ = ${ind(p1q1)}, Σp₀q₁ = ${ind(p0q1)}`, `P = ${ind(p1q1)} ÷ ${ind(p0q1)} × 100 ${ap(Pa, 2)}`], F: [`L = ${ind(p1q0)} ÷ ${ind(p0q0)} × 100 ${ap(L, 4)}`, `P = ${ind(p1q1)} ÷ ${ind(p0q1)} × 100 ${ap(Pa, 4)}`, `F = √(${fixed(L, 4)} × ${fixed(Pa, 4)}) ≈ ${d2(Fi)}`], ME: [`Σp₁(q₀ + q₁) = ${ind(p1q0 + p1q1)}, Σp₀(q₀ + q₁) = ${ind(p0q0 + p0q1)}`, `Index = ${ind(p1q0 + p1q1)} ÷ ${ind(p0q0 + p0q1)} × 100 ${ap(ME, 2)}`], SA: [`Σp₁ = ${S(r => r.p1)}, Σp₀ = ${S(r => r.p0)}`, `Index = ${S(r => r.p1)} ÷ ${S(r => r.p0)} × 100 ${ap(SA, 2)}`] }[v];
      return QI(`Commodity data (base year p₀, q₀; current year p₁, q₁) — ${tbl}. Find the ${nm} (correct to two decimals).`, build(corr, [roundDp(L, 2), roundDp(Pa, 2), Fi, roundDp(ME, 2), roundDp(SA, 2), roundDp(F(p0q0, p1q0).mul(100), 2)], d2), 'Laspeyres uses base-year quantities, Paasche current-year quantities; Fisher = √(L × P); Marshall–Edgeworth uses q₀ + q₁.', steps, { v, rows });
    } });

  def({ id: 'q_sampling', unit: U('p3-ch13-u02'), name: 'Sampling — number of samples and standard error', concept: 'Samples with/without replacement; SE = σ/√n',
    make(d) {
      const v = pick(['with', 'without', 'se']);
      if (v === 'se') { const sq = R(2, 12), n = sq * sq, sd = RS(2, 120, 2), se = F(sd, sq); return QI(`A population has standard deviation ${sd}. Find the standard error of the sample mean for a random sample of size ${n} (sampling with replacement).`, buildN(se, [F(sd, n), F(sd * sq), F(sd * sd, n), se.add(1)]), 'SE of mean = σ/√n.', [`SE = ${sd} ÷ √${n} = ${sd} ÷ ${sq} = ${nf(se)}`], { v, sd, n }); }
      const N = R(4, 12), n = R(2, Math.min(4, N - 1)), val = v === 'with' ? BI(N) ** BI(n) : nCr(N, n);
      return QI(`How many different samples of size ${n} can be drawn from a population of ${N} units ${v === 'with' ? 'with replacement (ordered samples)' : 'without replacement (order not considered)'}?`, buildN(F(val), [F(v === 'with' ? nCr(N, n) : BI(N) ** BI(n)), F(nPr(N, n)), F(BI(n) ** BI(N)), F(val + 1n)]), 'With replacement: Nⁿ samples; without replacement: ᴺCₙ samples.', [v === 'with' ? `Nⁿ = ${N}${sup(n)} = ${ind(val)}` : `${N}C${n} = ${ind(val)}`], { v, N, n });
    } });

  def({ id: 'q_class_data', unit: U('p3-ch13-u01'), name: 'Classes, boundaries and class marks', concept: 'Frequency distribution vocabulary',
    make(d) {
      const h = pick([5, 10, 20]), s = pick([0, 10, 20, 30, 40, 50]), k = R(3, 6), lo = s + k * h, hi = lo + h - 1, v = pick(['ub', 'lb', 'mark', 'width']);
      const val = { ub: F(2 * hi + 1, 2), lb: F(2 * lo - 1, 2), mark: F(lo + hi, 2), width: F(h) }[v];
      const lab = { ub: 'upper class boundary', lb: 'lower class boundary', mark: 'class mark (mid-value)', width: 'class width (class length)' }[v];
      return QI(`A frequency distribution has inclusive classes ${s}–${s + h - 1}, ${s + h}–${s + 2 * h - 1}, ${s + 2 * h}–${s + 3 * h - 1}, … What is the ${lab} of the class ${lo}–${hi}?`, buildN(val, [F(hi), F(lo), F(h - 1), F(lo + hi + 1, 2), F(2 * hi + 1, 2), F(2 * lo - 1, 2)]), 'For inclusive classes, boundaries are found by subtracting/adding half the gap (0.5 here) to the class limits; class mark = (lower limit + upper limit)/2; width = difference of successive lower limits.', [{ ub: `Upper boundary = ${hi} + 0.5 = ${nf(val)}`, lb: `Lower boundary = ${lo} − 0.5 = ${nf(val)}`, mark: `Class mark = (${lo} + ${hi}) ÷ 2 = ${nf(val)}`, width: `Width = ${lo + h} − ${lo} = ${h}` }[v]], { v, h, s, k });
    } });

  /* =====================================================================================
     PAPER 4 — BUSINESS ECONOMICS
     ===================================================================================== */
  const P4 = s => U('p4-' + s);
  const e2 = x => fixed(x, 2);
  def({ id: 'e_elasticity', unit: [P4('ch02-u01'), P4('ch02-u03')], name: 'Elasticity (arc and percentage methods)', concept: 'Price, income, cross and supply elasticity',
    make(d) {
      const kind = pick(['price', 'price', 'income', 'cross', 'supply']), meth = pick(['arc', 'pct']);
      let P1 = R(5, 100), P2 = P1 + R(-Math.min(30, P1 - 1), 30), Q1 = R(20, 500), Q2; if (P1 === P2) throw new Error('retry');
      const goods = { price: 'demand', income: 'demand', cross: 'demand', supply: 'supply' }[kind];
      if (kind === 'price') Q2 = Q1 + (P2 > P1 ? -1 : 1) * R(1, Math.min(200, Q1 - 1)); else if (kind === 'supply') Q2 = Q1 + (P2 > P1 ? 1 : -1) * R(1, Math.min(200, Q1 - 1)); else Q2 = Q1 + R(-Math.min(150, Q1 - 1), 200);
      if (Q2 === Q1 || Q2 <= 0) throw new Error('retry');
      const dQ = Q2 - Q1, dP = P2 - P1, e = meth === 'arc' ? F(dQ, Q1 + Q2).div(F(dP, P1 + P2)) : F(dQ, Q1).div(F(dP, P1)), ee = kind === 'price' ? e.abs() : e;
      const xname = { price: 'price', income: 'income', cross: 'price of the related good Y', supply: 'price' }[kind], unitTxt = kind === 'income' ? '₹' : '₹';
      const q = `When the ${xname} ${kind === 'income' ? 'of a consumer ' : ''}changes from ${unitTxt}${ind(P1)} to ${unitTxt}${ind(P2)}, the quantity ${goods === 'supply' ? 'supplied' : 'demanded'}${kind === 'cross' ? ' of good X' : ''} changes from ${Q1} to ${Q2} units. Find the ${{ price: 'price elasticity of demand (absolute value)', income: 'income elasticity of demand', cross: 'cross elasticity of demand', supply: 'price elasticity of supply' }[kind]} using the ${meth === 'arc' ? 'arc (mid-point) method' : 'percentage method on the original values'} (correct to two decimals).`;
      const alt = meth === 'arc' ? F(dQ, Q1).div(F(dP, P1)) : F(dQ, Q1 + Q2).div(F(dP, P1 + P2)), inv = F(dP, P1).div(F(dQ, Q1)), fin = F(dQ, Q2).div(F(dP, P2));
      const f = x => kind === 'price' ? fixed(F(x).abs(), 2) : r2s(x);
      const steps = meth === 'arc' ? [`ΔQ/(Q₁ + Q₂) = ${dQ} ÷ ${Q1 + Q2}`.replace(/-/g, '−'), `ΔP/(P₁ + P₂) = ${dP} ÷ ${P1 + P2}`.replace(/-/g, '−'), `e = (${dQ} ÷ ${Q1 + Q2}) ÷ (${dP} ÷ ${P1 + P2}) ${ap(e, 2)}`.replace(/\((-)/g, '(−')] : [`% change in quantity = ${dQ} ÷ ${Q1} × 100`.replace(/-/g, '−'), `% change in ${xname} = ${dP} ÷ ${P1} × 100`.replace(/-/g, '−'), `e = (${dQ} ÷ ${Q1}) ÷ (${dP} ÷ ${P1}) ${ap(e, 2)}`.replace(/\((-)/g, '(−')];
      if (kind === 'price') steps.push('Price elasticity is quoted without the minus sign');
      if (kind === 'income') steps.push(ee.sign < 0 ? 'Negative: an inferior good' : ee.gt(1) ? 'Greater than 1: a luxury' : 'Between 0 and 1: a necessity');
      if (kind === 'cross') steps.push(ee.sign > 0 ? 'Positive: X and Y are substitutes' : 'Negative: X and Y are complements');
      return QI(q, build(roundDp(ee, 2), [alt, inv, fin, ee.neg(), ee.add(1)].map(x => roundDp(kind === 'price' ? x.abs() : x, 2)), f, { ok: x => kind !== 'price' || F(x).sign >= 0 }), meth === 'arc' ? 'Arc elasticity = [(Q₂ − Q₁)/(Q₂ + Q₁)] ÷ [(P₂ − P₁)/(P₂ + P₁)] — the mid-point formula gives the same answer whichever direction the change is measured.' : 'Percentage method: e = (ΔQ/Q) ÷ (ΔP/P) using the original price and quantity.', steps, { kind, meth, P1, P2, Q1, Q2 });
    } });

  def({ id: 'e_point_elasticity', unit: P4('ch02-u01'), name: 'Point elasticity on a linear demand curve', concept: 'e = (dQ/dP) × P/Q',
    make(d) {
      const b = R(1, 10), P = R(1, 40), a = b * P + R(10, 400), Q = a - b * P, e = F(b * P, Q);
      return QI(`The demand function is Q = ${ind(a)} − ${b === 1 ? '' : b}P. Find the price elasticity of demand (absolute value) at P = ${P} (correct to two decimals).`, build(roundDp(e, 2), [roundDp(F(Q, b * P), 2), roundDp(F(b * Q, P), 2), roundDp(F(b), 2), roundDp(F(P, Q), 2)], e2, { ok: x => F(x).sign > 0 }), 'Point elasticity = |dQ/dP| × P/Q.', [`Q at P = ${P}: ${ind(a)} − ${b} × ${P} = ${ind(Q)}`, `|dQ/dP| = ${b}`, `e = ${b} × ${P} ÷ ${ind(Q)} ${ap(e, 2)}`], { a, b, P });
    } });

  def({ id: 'e_utility', unit: P4('ch02-u02'), name: 'Marginal utility and consumer surplus', concept: 'Diminishing marginal utility; consumer surplus',
    make(d) {
      const k = R(5, 7), mu = []; let m = R(30, 80); for (let i = 0; i < k; i++) { mu.push(m); m -= R(3, 12); } if (mu[k - 1] <= 0) throw new Error('retry');
      const v = pick(['mu', 'cs']);
      if (v === 'mu') { const tu = mu.reduce((a, x) => (a.push((a[a.length - 1] || 0) + x), a), []), i = R(1, k - 1); return QI(`Total utility from successive units: ${tu.map((t, j) => `${j + 1} unit${j ? 's' : ''}: ${t}`).join(', ')} utils. What is the marginal utility of unit ${i + 1}?`, buildN(F(mu[i]), [F(tu[i]), roundDp(F(tu[i], i + 1), 2), F(mu[i - 1]), F(i + 1 < k ? mu[i + 1] : mu[i] - 1)]), 'MUₙ = TUₙ − TUₙ₋₁.', [`MU = ${tu[i]} − ${tu[i - 1]} = ${mu[i]} utils`], { v, mu, i }); }
      const P = R(mu[k - 1], mu[1]); let bought = mu.filter(x => x >= P).length; const cs = mu.slice(0, bought).reduce((s, x) => s + x - P, 0);
      return QI(`A consumer is willing to pay ₹${mu.join(', ₹')} for successive units of a good. The market price is ₹${P}. What is the consumer surplus?`, build(cs, [mu.slice(0, bought).reduce((s, x) => s + x, 0), cs + P, mu.reduce((s, x) => s + x - P, 0), mu[0] - P], x => rs(x), { ok: x => x >= 0 }), 'The consumer buys while willingness to pay ≥ price; surplus = Σ(willingness to pay − price) on units bought.', [`Units bought (worth at least ₹${P}): ${bought}`, `Surplus: ${mu.slice(0, bought).map(x => `(${x} − ${P})`).join(' + ')} = ${cs}`], { v, mu, P });
    } });

  def({ id: 'e_production', unit: P4('ch03-u01'), name: 'Total, average and marginal product', concept: 'TP, AP and MP',
    make(d) {
      const k = 6, mp = []; let x = R(5, 20); for (let i = 0; i < k; i++) { mp.push(x); x += i < 2 ? R(1, 8) : -R(2, 10); } if (mp.some(m => m < -5)) throw new Error('retry');
      const tp = mp.reduce((a, m) => (a.push((a[a.length - 1] || 0) + m), a), []); if (tp.some(t => t <= 0)) throw new Error('retry');
      const L = R(2, k), v = pick(['ap', 'mp']), corr = v === 'ap' ? F(tp[L - 1], L) : F(mp[L - 1]);
      return QI(`Total product with 1 to ${k} workers: ${tp.join(', ')} units. Find the ${v === 'ap' ? 'average' : 'marginal'} product of labour when ${L} workers are employed.`, buildN(v === 'ap' ? roundDp(corr, 2) : corr, [v === 'ap' ? F(mp[L - 1]) : roundDp(F(tp[L - 1], L), 2), F(tp[L - 1]), F(mp[L - 2]), roundDp(F(tp[L - 2], L - 1), 2)]), 'AP = TP/L; MP = TPₙ − TPₙ₋₁.', [v === 'ap' ? `AP = ${tp[L - 1]} ÷ ${L} ${ap(corr, 2)}` : `MP = ${tp[L - 1]} − ${tp[L - 2]} = ${mp[L - 1]}`], { v, tp, L });
    } });

  def({ id: 'e_cost', unit: P4('ch03-u02'), name: 'Cost concepts from a table', concept: 'TFC, TVC, AC, AVC, AFC, MC',
    make(d) {
      const TFC = RS(20, 500, 10), mc = []; let m = R(10, 40); for (let i = 0; i < 6; i++) { mc.push(m); m += i < 1 ? -R(1, 5) : R(2, 12); } if (mc.some(x => x <= 0)) throw new Error('retry');
      const tc = mc.reduce((a, x) => (a.push((a[a.length - 1] || TFC) + x), a), []), q = R(2, 6), v = pick(['ac', 'avc', 'afc', 'mc']);
      const tvc = tc[q - 1] - TFC, val = { ac: F(tc[q - 1], q), avc: F(tvc, q), afc: F(TFC, q), mc: F(mc[q - 1]) }[v];
      const nm = { ac: 'average total cost', avc: 'average variable cost', afc: 'average fixed cost', mc: 'marginal cost' }[v];
      return QI(`Total fixed cost is ₹${ind(TFC)}. Total cost (₹) of producing 1 to 6 units: ${tc.map(ind).join(', ')}. Find the ${nm} of ${q} units.`, build(roundDp(val, 2), [roundDp(F(tc[q - 1], q), 2), roundDp(F(tvc, q), 2), roundDp(F(TFC, q), 2), F(mc[q - 1]), F(tc[q - 1]), roundDp(F(tc[q - 1] - tc[q - 2], q), 2)], x => rs2(x)), 'TVC = TC − TFC; AC = TC/Q; AVC = TVC/Q; AFC = TFC/Q; MC = TCₙ − TCₙ₋₁.', [{ ac: `AC = ${ind(tc[q - 1])} ÷ ${q} ${ap(val, 2)}`, avc: `TVC = ${ind(tc[q - 1])} − ${ind(TFC)} = ${ind(tvc)}; AVC = ${ind(tvc)} ÷ ${q} ${ap(val, 2)}`, afc: `AFC = ${ind(TFC)} ÷ ${q} ${ap(val, 2)}`, mc: `MC = ${ind(tc[q - 1])} − ${ind(tc[q - 2])} = ${mc[q - 1]}` }[v]], { v, TFC, tc, q });
    } });

  def({ id: 'e_revenue', unit: P4('ch04-u01'), name: 'Total, average and marginal revenue', concept: 'TR, AR, MR and MR = AR(1 − 1/e)',
    make(d) {
      if (chance(.4)) { const AR = RS(10, 500, 5), e = pick(['2', '1.5', '4', '5', '1.25', '3', '0.5']), MR = F(AR).mul(F(1).sub(F(1).div(F(e)))); if (badDp(MR, 2)) throw new Error('retry');
        return QI(`Average revenue is ₹${AR} and price elasticity of demand is ${e}. Find marginal revenue.`, build(MR, [F(AR).mul(F(1).add(F(1).div(F(e)))), F(AR).div(F(e)), F(AR).mul(F(e).sub(1)), F(AR).sub(F(e))], rsS, { ok: x => true }), 'MR = AR × (e − 1)/e, i.e. AR(1 − 1/e). MR is negative when demand is inelastic.', [`MR = ${AR} × (1 − 1/${e}) = ${num(MR)}`], { v: 'formula', AR, e }); }
      const p = []; let x = RS(40, 200, 2); for (let i = 0; i < 6; i++) { p.push(x); x -= R(1, 8) * 2; } if (p[5] <= 0) throw new Error('retry');
      const tr = p.map((pp, i) => pp * (i + 1)), q = R(2, 6), v = pick(['tr', 'mr']), val = v === 'tr' ? tr[q - 1] : tr[q - 1] - tr[q - 2];
      return QI(`A firm can sell 1, 2, 3, 4, 5 and 6 units at prices ₹${p.join(', ₹')} per unit respectively. Find the ${v === 'tr' ? 'total revenue' : 'marginal revenue'} from the ${v === 'tr' ? 'sale of ' + q + ' units' : ord(q) + ' unit'}.`, build(F(val), [F(p[q - 1]), F(tr[q - 1]), F(tr[q - 2]), F(p[q - 2] - p[q - 1]), F(val + p[q - 1])], rsS, { ok: x => true }), 'TR = P × Q; AR = TR/Q = P; MR = TRₙ − TRₙ₋₁.', v === 'tr' ? [`TR = ${p[q - 1]} × ${q} = ${tr[q - 1]}`] : [`TR(${q}) = ${p[q - 1]} × ${q} = ${tr[q - 1]}; TR(${q - 1}) = ${p[q - 2]} × ${q - 1} = ${tr[q - 2]}`, `MR = ${tr[q - 1]} − ${tr[q - 2]} = ${val}`], { v, p, q });
    } });

  def({ id: 'e_profit_max', unit: P4('ch04-u03'), name: 'Profit-maximising output (MR = MC)', concept: 'Equilibrium of a firm',
    make(d) {
      const P = RS(20, 200, 2), k = 7, star = R(3, 6), mc = []; for (let i = 0; i < k; i++) mc.push(0);
      mc[star - 1] = P - R(1, 4); for (let i = star; i < k; i++) mc[i] = (i === star ? P : mc[i - 1]) + R(2, 15); for (let i = star - 2; i >= 1; i--) mc[i] = mc[i + 1] - R(2, 12); mc[0] = mc[1] + R(2, 20);
      if (mc.some(x => x <= 0)) throw new Error('retry');
      const room = P * star - mc.slice(0, star).reduce((a, b) => a + b, 0); if (room < 30) throw new Error('retry'); const TFC = RS(10, room - 10, 10), tc = mc.reduce((a, x) => (a.push((a[a.length - 1] ?? TFC) + x), a), []), prof = tc.map((c, i) => P * (i + 1) - c);
      return QI(`In a perfectly competitive market the price is ₹${P}. A firm’s total cost (₹) for 1 to ${k} units is ${tc.map(ind).join(', ')}. At what output does the firm maximise profit?`, build(star, [star - 1, star + 1, prof.indexOf(Math.min(...prof)) + 1, k, 1], x => PL(x, 'unit'), { ok: x => x >= 1 && x <= k }), 'Under perfect competition MR = price. The firm expands output as long as MR ≥ MC; it stops where the next unit’s MC would exceed MR (the MR = MC condition with MC rising).', [`MC: ${mc.map(ind).join(', ')}`, `MR = price = ${P}; MC ≤ ${P} up to unit ${star} and MC of unit ${star + 1} = ${mc[star]} > ${P}`, `Profit at ${star} units = ${P} × ${star} − ${ind(tc[star - 1])} = ${prof[star - 1] < 0 ? '−' : ''}${ind(Math.abs(prof[star - 1]))}`], { P, tc });
    } });

  def({ id: 'e_equilibrium', unit: P4('ch04-u02'), name: 'Market equilibrium', concept: 'Equilibrium price and quantity; effect of a tax',
    make(d) {
      const b = R(1, 10), dd = R(1, 10), Ps = R(5, 60), Qs = R(50, 500), a = Qs + b * Ps, c = Qs - dd * Ps, v = pick(['p', 'q', 'tax']);
      const Dq = `Qd = ${ind(a)} − ${b === 1 ? '' : b}P`, Sq = `Qs = ${c < 0 ? '−' + ind(-c) : ind(c)} + ${dd === 1 ? '' : dd}P`;
      if (v === 'tax') { const t = R(1, 10), np = F(a - c + dd * t, b + dd); if (badDp(np, 2)) throw new Error('retry'); return QI(`${Dq} and ${Sq}. A specific tax of ₹${t} per unit is imposed on sellers. Find the new equilibrium price paid by buyers.`, build(np, [F(Ps + t), F(Ps), np.sub(t), F(a - c - dd * t, b + dd)], rs, { ok: x => F(x).sign > 0 }), 'A specific tax on sellers shifts supply: Qs = c + d(P − t). Equate with demand.', [`Before tax P = ${Ps}`, `${ind(a)} − ${b}P = ${c} + ${dd}(P − ${t})`, `P = (${ind(a)} − ${pn(c)} + ${dd * t}) ÷ ${b + dd} = ${num(np)}`], { v, a, b, c, dd, t }); }
      const corr = v === 'p' ? F(Ps) : F(Qs);
      return QI(`${Dq} and ${Sq}. Find the equilibrium ${v === 'p' ? 'price' : 'quantity'}.`, build(corr, v === 'p' ? [F(a + c, b + dd), F(a - c, b), F(Qs), F(a - c, dd)] : [F(Ps), F(a - b * Ps + 10), F(c + dd * Ps * 2), F(a)], v === 'p' ? rs : nf, { ok: x => F(x).sign > 0 }), 'At equilibrium quantity demanded = quantity supplied.', [`${ind(a)} − ${b}P = ${c} + ${dd}P`, `P = (${ind(a)} − ${pn(c)}) ÷ (${b} + ${dd}) = ${Ps}`, ...(v === 'q' ? [`Q = ${ind(a)} − ${b} × ${Ps} = ${ind(Qs)}`] : [])], { v, a, b, c, dd });
    } });

  const cr = x => '₹' + ind(F(x).abs()) + ' crore';
  const crS = x => (F(x).sign < 0 ? '−' : '') + cr(x);
  def({ id: 'e_national_income', unit: P4('ch05-u01'), name: 'National income aggregates', concept: 'GDP, GNP, NDP, NNP at MP and FC',
    make(d) {
      const v = pick(['agg', 'agg', 'exp', 'inc', 'va']);
      if (v === 'agg') {
        const G = RS(50000, 900000, 100), dep = RS(2000, 60000, 100), nf = RS(-20000, 15000, 100), it = RS(5000, 90000, 100), sb = RS(1000, 30000, 100), nit = it - sb;
        const tg = pick(['GNPMP', 'NDPMP', 'NNPMP', 'GDPFC', 'NNPFC', 'NDPFC']), val = { GNPMP: G + nf, NDPMP: G - dep, NNPMP: G + nf - dep, GDPFC: G - nit, NNPFC: G + nf - dep - nit, NDPFC: G - dep - nit }[tg];
        const nm = { GNPMP: 'GNP at market prices', NDPMP: 'NDP at market prices', NNPMP: 'NNP at market prices', GDPFC: 'GDP at factor cost', NNPFC: 'NNP at factor cost (national income)', NDPFC: 'NDP at factor cost' }[tg];
        const steps = [`Net indirect taxes = ${ind(it)} − ${ind(sb)} = ${ind(nit)}`, { GNPMP: `GNP MP = ${ind(G)} + ${pn(nf)} = ${ind(val)}`, NDPMP: `NDP MP = ${ind(G)} − ${ind(dep)} = ${ind(val)}`, NNPMP: `NNP MP = ${ind(G)} + ${pn(nf)} − ${ind(dep)} = ${ind(val)}`, GDPFC: `GDP FC = ${ind(G)} − ${ind(nit)} = ${ind(val)}`, NNPFC: `NNP FC = ${ind(G)} + ${pn(nf)} − ${ind(dep)} − ${ind(nit)} = ${ind(val)}`, NDPFC: `NDP FC = ${ind(G)} − ${ind(dep)} − ${ind(nit)} = ${ind(val)}` }[tg]];
        return QI(`GDP at market prices ₹${ind(G)} crore; consumption of fixed capital ₹${ind(dep)} crore; net factor income from abroad ${nf < 0 ? '−' : ''}₹${ind(Math.abs(nf))} crore; indirect taxes ₹${ind(it)} crore; subsidies ₹${ind(sb)} crore. Find ${nm}.`, build(val, [G + nf - dep, G - nf - dep - nit, G + nf - dep - it, G + nf - dep + nit, G - dep - nit, G + nf, G - nit + sb * 0 - dep + nf * 0].filter(x => x !== val), crS), 'GNP = GDP + NFIA; Net = Gross − depreciation; FC = MP − net indirect taxes (indirect taxes − subsidies).', steps, { v, G, dep, nf, it, sb, tg });
      }
      if (v === 'exp') { const C = RS(100000, 700000, 100), I = RS(20000, 250000, 100), Gv = RS(20000, 200000, 100), X = RS(10000, 150000, 100), M = RS(10000, 180000, 100), val = C + I + Gv + X - M;
        return QI(`Private final consumption expenditure ₹${ind(C)} crore; gross domestic capital formation ₹${ind(I)} crore; government final consumption expenditure ₹${ind(Gv)} crore; exports ₹${ind(X)} crore; imports ₹${ind(M)} crore. Find GDP at market prices.`, build(val, [C + I + Gv + X + M, C + I + Gv, C + I + Gv + X, C + I + Gv - X + M], crS), 'Expenditure method: GDP MP = C + I + G + (X − M).', [`GDP MP = ${ind(C)} + ${ind(I)} + ${ind(Gv)} + ${ind(X)} − ${ind(M)} = ${ind(val)}`], { v, C, I, Gv, X, M }); }
      if (v === 'inc') { const W = RS(100000, 500000, 100), Rn = RS(5000, 60000, 100), In = RS(5000, 80000, 100), Pr = RS(20000, 200000, 100), Mx = RS(10000, 150000, 100), nf = RS(-15000, 10000, 100), val = W + Rn + In + Pr + Mx + nf;
        return QI(`Compensation of employees ₹${ind(W)} crore; rent ₹${ind(Rn)} crore; interest ₹${ind(In)} crore; profit ₹${ind(Pr)} crore; mixed income of self-employed ₹${ind(Mx)} crore; net factor income from abroad ${nf < 0 ? '−' : ''}₹${ind(Math.abs(nf))} crore. Find national income (NNP at factor cost).`, build(val, [val - nf, val - Mx, val + 2 * Math.abs(nf), W + Rn + In + Pr], crS), 'Income method: NDP FC = compensation of employees + operating surplus (rent, interest, profit) + mixed income; NNP FC = NDP FC + NFIA.', [`NDP FC = ${ind(W)} + ${ind(Rn)} + ${ind(In)} + ${ind(Pr)} + ${ind(Mx)} = ${ind(val - nf)}`, `NNP FC = ${ind(val - nf)} + ${pn(nf)} = ${ind(val)}`], { v, W, Rn, In, Pr, Mx, nf }); }
      const O = RS(50000, 400000, 100), IC = RS(10000, Math.round(O * .6), 100), dep = RS(1000, 20000, 100), nit = RS(1000, 20000, 100), val = O - IC - dep - nit; if (val <= 0) throw new Error('retry');
      return QI(`For a firm: value of output ₹${ind(O)} crore; intermediate consumption ₹${ind(IC)} crore; consumption of fixed capital ₹${ind(dep)} crore; net indirect taxes ₹${ind(nit)} crore. Find net value added at factor cost.`, build(val, [O - IC, O - IC - dep, O - IC - nit, O - dep - nit], crS), 'Value added method: GVA MP = output − intermediate consumption; NVA FC = GVA MP − depreciation − net indirect taxes.', [`GVA MP = ${ind(O)} − ${ind(IC)} = ${ind(O - IC)}`, `NVA FC = ${ind(O - IC)} − ${ind(dep)} − ${ind(nit)} = ${ind(val)}`], { v, O, IC, dep, nit });
    } });

  def({ id: 'e_multiplier', unit: P4('ch05-u02'), name: 'Investment multiplier and equilibrium income', concept: 'k = 1/(1 − MPC) = 1/MPS',
    make(d) {
      const mpc = pick([F(1, 2), F(3, 5), F(2, 3), F(3, 4), F(4, 5), F(5, 6), F(9, 10), F(7, 10)]), k = F(1).div(F(1).sub(mpc)), v = pick(['k', 'dy', 'eq', 'mps']);
      const show = x => dpOf(x) !== null && dpOf(x) <= 2 ? num(x) : fr(x);
      if (v === 'k' || v === 'mps') { const given = v === 'mps' ? `MPS is ${show(F(1).sub(mpc))}` : `MPC is ${show(mpc)}`; const fk = x => badDp(x, 4) ? fixed(x, 2) : num(x); return QI(`If ${given}, what is the investment multiplier? (Correct to two decimals where needed.)`, build(k, [F(1).div(mpc), mpc.mul(10), F(1).sub(mpc), k.add(1)], fk), 'k = 1/(1 − MPC) = 1/MPS.', [`MPS = 1 − MPC = ${show(F(1).sub(mpc))}`, `k = 1 ÷ ${show(F(1).sub(mpc)).includes('/') ? '(' + show(F(1).sub(mpc)) + ')' : show(F(1).sub(mpc))} ${badDp(k, 4) ? '≈ ' + fixed(k, 2) : '= ' + num(k)}`], { v, mpc: fr(mpc) }); }
      if (v === 'dy') { const dI = RS(100, 5000, 50), dy = k.mul(dI); if (!dy.int && badDp(dy, 2)) throw new Error('retry'); return QI(`MPC is ${show(mpc)}. If investment rises by ₹${ind(dI)} crore, by how much does national income rise?`, build(dy, [mpc.mul(dI), F(1).sub(mpc).mul(dI), F(1).div(mpc).mul(dI), dy.add(dI)], x => cr(x)), 'ΔY = k × ΔI with k = 1/(1 − MPC).', [`k = 1 ÷ (1 − ${pf(mpc).includes('/') ? pf(mpc) : show(mpc)}) = ${nf(k)}`, `ΔY = ${nf(k)} × ${ind(dI)} = ${num(dy)}`], { v, mpc: fr(mpc), dI }); }
      const a = RS(50, 2000, 10), I = RS(100, 5000, 10), Y = F(a + I).mul(k); if (badDp(Y, 2)) throw new Error('retry');
      return QI(`The consumption function is C = ${ind(a)} + ${show(mpc).includes('/') ? '(' + show(mpc) + ')' : show(mpc)}Y and autonomous investment is ₹${ind(I)} crore. Find the equilibrium level of income.`, build(Y, [F(a + I), F(a + I).div(mpc), F(a).mul(k).add(I), Y.add(a)], x => cr(x)), 'At equilibrium Y = C + I, so Y = (a + I)/(1 − b).', [`Y = C + I`, `Y = (${ind(a)} + ${ind(I)}) ÷ (1 − ${pf(mpc).includes('/') ? pf(mpc) : show(mpc)}) = ${num(Y)}`], { v, mpc: fr(mpc), a, I });
    } });

  def({ id: 'e_money_multiplier', unit: [P4('ch08-u02'), P4('ch08-u03')], name: 'Money multiplier and credit creation', concept: 'm = 1/r or (1 + c)/(r + c)',
    make(d) {
      const v = pick(['simple', 'cash', 'credit']), r = pick([F(1, 10), F(1, 20), F(1, 5), F(1, 4), F(2, 25), F(1, 8)]), rP = r.mul(100);
      if (v === 'simple') { const m = F(1).div(r); return QI(`If the required reserve ratio is ${num(rP)}% and banks hold no excess reserves (and the public holds no currency), what is the money multiplier?`, buildN(m, [rP, F(1).sub(r).mul(10), m.add(1), F(1).div(r.mul(2))]), 'Money multiplier = 1/reserve ratio.', [`m = 1 ÷ ${num(r)} = ${nf(m)}`], { v, r: fr(r) }); }
      if (v === 'cash') { const c = pick([F(1, 10), F(1, 5), F(1, 4), F(3, 10), F(1, 2)]), m = F(1).add(c).div(r.add(c)), H = RS(1000, 50000, 100), M = m.mul(H); if (badDp(m, 4) || badDp(M, 2)) throw new Error('retry');
        return QI(`High-powered money is ₹${ind(H)} crore, the currency-deposit ratio is ${num(c)} and the reserve-deposit ratio is ${num(r)}. Find the money supply.`, build(M, [F(H).div(r), F(H).div(r.add(c)), F(1).div(r).mul(H).mul(F(1).add(c)), F(H).mul(F(1).add(c))], x => cr(x)), 'm = (1 + c)/(r + c); money supply = m × H.', [`m = (1 + ${num(c)}) ÷ (${num(r)} + ${num(c)}) = ${num(m)}`, `M = ${num(m)} × ${ind(H)} = ${num(M)}`], { v, r: fr(r), c: fr(c), H }); }
      const D0 = RS(1000, 100000, 1000), tot = F(D0).div(r), cred = tot.sub(D0);
      return QI(`A fresh deposit of ₹${ind(D0)} is made in the banking system. The cash reserve ratio is ${num(rP)}% and there are no other leakages. What is the total amount of credit (loans) created by the banks?`, build(cred, [tot, F(D0).mul(r), F(D0).mul(F(1).sub(r)), cred.add(D0).add(D0)], x => rs(x)), 'Total deposits = initial deposit ÷ CRR; credit created = total deposits − initial deposit.', [`Total deposits = ${ind(D0)} ÷ ${num(r)} = ${num(tot)}`, `Credit created = ${num(tot)} − ${ind(D0)} = ${num(cred)}`], { v, r: fr(r), D0 });
    } });

  def({ id: 'e_qtm', unit: P4('ch08-u01'), name: 'Quantity theory of money', concept: 'MV = PT',
    make(d) {
      const v = pick(['p', 'v', 'pct']);
      if (v === 'pct') { const g = pick([5, 8, 10, 12, 15, 20, 25]); return QI(`According to Fisher’s quantity theory (V and T constant), if the money supply rises by ${g}%, the price level:`, buildS(`rises by ${g}%`, [`falls by ${g}%`, `rises by ${g / 2}%`, 'does not change', `rises by ${2 * g}%`]), 'With V and T constant, P changes in the same proportion as M.', [`MV = PT with V, T fixed: P is proportional to M`, `P rises by ${g}%`], { v, g }); }
      const M = RS(1000, 50000, 500), V = R(2, 10), T = RS(1000, 50000, 100), P = F(M * V, T); if (badDp(P, 2)) throw new Error('retry');
      if (v === 'p') return QI(`Money supply is ₹${ind(M)} crore, velocity of circulation ${V} and volume of transactions ${ind(T)} crore units. Find the price level (MV = PT).`, build(P, [F(M, T * V), F(T, M * V), F(M * V), F(M * T, V)], nf, { ok: x => dpOf(F(x)) !== null && dpOf(F(x)) <= 4 }), 'P = MV/T.', [`P = ${ind(M)} × ${V} ÷ ${ind(T)} = ${nf(P)}`], { v, M, V, T });
      return QI(`If MV = PT with M = ₹${ind(M)} crore, P = ${nf(P)} and T = ${ind(T)} crore units, find V.`, buildN(F(V), [F(V + 1), P.mul(T), F(M).div(T), F(V * 2)]), 'V = PT/M.', [`V = ${nf(P)} × ${ind(T)} ÷ ${ind(M)} = ${V}`], { v, M, V, T });
    } });

  def({ id: 'e_budget', unit: [P4('ch07-u03'), P4('ch07-u04')], name: 'Budget deficits', concept: 'Fiscal, revenue and primary deficit',
    make(d) {
      const tax = RS(100000, 900000, 1000), ntax = RS(10000, 150000, 1000), rec = RS(1000, 30000, 1000), dis = RS(0, 60000, 1000), rexp = RS(150000, 1200000, 1000), intr = RS(20000, Math.round(rexp * .4), 1000), cexp = RS(20000, 400000, 1000);
      const RR = tax + ntax, RD = rexp - RR, FD = rexp + cexp - RR - rec - dis, PD = FD - intr; if (RD <= 0 || FD <= 0) throw new Error('retry');
      const v = pick(['FD', 'RD', 'PD']), val = { FD, RD, PD }[v];
      const q = `Government budget (₹ crore): tax revenue ${ind(tax)}; non-tax revenue ${ind(ntax)}; recovery of loans ${ind(rec)}; disinvestment receipts ${ind(dis)}; revenue expenditure ${ind(rexp)} (including interest payments ${ind(intr)}); capital expenditure ${ind(cexp)}. Find the ${{ FD: 'fiscal deficit', RD: 'revenue deficit', PD: 'primary deficit' }[v]}.`;
      const steps = [`Revenue receipts = ${ind(tax)} + ${ind(ntax)} = ${ind(RR)}`, `Fiscal deficit = ${ind(rexp)} + ${ind(cexp)} − ${ind(RR)} − ${ind(rec)} − ${ind(dis)} = ${ind(FD)}`]; if (v === 'RD') steps.splice(1, 1, `Revenue deficit = ${ind(rexp)} − ${ind(RR)} = ${ind(RD)}`); if (v === 'PD') steps.push(`Primary deficit = ${ind(FD)} − ${ind(intr)} = ${ind(PD)}`);
      return QI(q, build(val, [FD, RD, PD, rexp + cexp - RR, FD + intr, RD - intr].filter(x => x !== val), crS), 'Revenue deficit = revenue expenditure − revenue receipts. Fiscal deficit = total expenditure − (revenue receipts + non-debt capital receipts). Primary deficit = fiscal deficit − interest payments.', steps, { tax, ntax, rec, dis, rexp, intr, cexp, v });
    } });

  def({ id: 'e_trade', unit: P4('ch09-u01'), name: 'Terms of trade and comparative advantage', concept: 'Net barter terms of trade; opportunity cost',
    make(d) {
      if (chance(.5)) { const px = R(100, 250), pm = R(100, 250), ToT = F(px, pm).mul(100), v = pick(['nbt', 'itt']); if (v === 'itt') { const qx = R(80, 160), itt = ToT.mul(qx).div(100);
        return QI(`With base year = 100, the export price index is ${px}, the import price index is ${pm} and the export volume index is ${qx}. Find the income terms of trade (correct to two decimals).`, build(roundDp(itt, 2), [roundDp(ToT, 2), roundDp(F(pm, px).mul(qx), 2), roundDp(F(px * qx, 100), 2)], e2), 'Income terms of trade = (Px/Pm) × Qx.', [`(Px/Pm) × Qx = ${px} ÷ ${pm} × ${qx} ${ap(itt, 2)}`], { v, px, pm, qx }); }
        return QI(`With base year = 100, the export price index has risen to ${px} and the import price index to ${pm}. Find the net barter terms of trade (correct to two decimals).`, build(roundDp(ToT, 2), [roundDp(F(pm, px).mul(100), 2), F(px - pm), roundDp(F(px + pm, 2), 2)], e2), 'Net barter terms of trade = (Px/Pm) × 100.', [`ToT = ${px} ÷ ${pm} × 100 ${ap(ToT, 2)}`, ToT.gt(100) ? 'Above 100: terms of trade improved' : ToT.lt(100) ? 'Below 100: terms of trade worsened' : 'Unchanged'], { v, px, pm }); }
      const [A, B] = sample(['India', 'Japan', 'Brazil', 'Kenya', 'Germany', 'Vietnam'], 2), aX = R(2, 12), aY = R(2, 12), bX = R(2, 12), bY = R(2, 12); if (aX * bY === aY * bX) throw new Error('retry');
      const ocA = F(aX, aY), ocB = F(bX, bY), win = ocA.lt(ocB) ? A : B;
      return QI(`Labour hours needed per unit: ${A} — cloth ${aX}, wheat ${aY}; ${B} — cloth ${bX}, wheat ${bY}. Which country has the comparative advantage in cloth?`, buildS(win, [win === A ? B : A, 'Neither — the costs are proportional', 'Both countries equally']), 'Comparative advantage lies with the country whose opportunity cost of the good (in terms of the other good) is lower.', [`Opportunity cost of 1 cloth: ${A} = ${aX}/${aY} = ${fr(ocA)} wheat; ${B} = ${bX}/${bY} = ${fr(ocB)} wheat`, `Lower opportunity cost: ${win}`], { v: 'ca', aX, aY, bX, bY, A, B });
    } });

  def({ id: 'e_tariff', unit: P4('ch09-u02'), name: 'Effects of a tariff', concept: 'Domestic price, imports and tariff revenue',
    make(d) {
      const b = R(2, 10), dd = R(2, 10), Pw = R(5, 30), t = R(1, 8), Pe = Pw + t + R(2, 15), Qe = R(100, 600), a = Qe + b * Pe, c = Qe - dd * Pe; const imp0 = (a - b * Pw) - (c + dd * Pw), P1 = Pw + t, imp1 = (a - b * P1) - (c + dd * P1); if (imp1 <= 0) throw new Error('retry');
      const v = pick(['imp', 'rev']), val = v === 'imp' ? imp1 : t * imp1;
      return QI(`Domestic demand Qd = ${ind(a)} − ${b}P and supply Qs = ${c < 0 ? '−' + ind(-c) : ind(c)} + ${dd}P. The world price is ₹${Pw} (free trade). A specific tariff of ₹${t} per unit is imposed. ${v === 'imp' ? 'Find the quantity imported after the tariff.' : 'Find the tariff revenue.'}`, build(val, v === 'imp' ? [imp0, imp0 - imp1, (a - b * P1), imp1 + 2 * t] : [t * imp0, imp1, t * (imp0 - imp1), P1 * imp1], v === 'imp' ? (x => ind(x) + ' units') : (x => rs(x)), { ok: x => x > 0 }), 'With a tariff the domestic price = world price + tariff; imports = demand − domestic supply at that price; tariff revenue = tariff × imports.', [`Price with tariff = ${Pw} + ${t} = ${P1}`, `Demand = ${ind(a)} − ${b} × ${P1} = ${ind(a - b * P1)}; supply = ${c} + ${dd} × ${P1} = ${ind(c + dd * P1)}`, `Imports = ${ind(a - b * P1)} − ${ind(c + dd * P1)} = ${ind(imp1)}`, ...(v === 'rev' ? [`Revenue = ${t} × ${ind(imp1)} = ${ind(t * imp1)}`] : [])], { a, b, c, dd, Pw, t, v });
    } });

  def({ id: 'e_exchange', unit: P4('ch09-u04'), name: 'Exchange rate changes', concept: 'Appreciation and depreciation',
    make(d) {
      const E1 = RS(6000, 9000, 25), E2 = E1 + RS(-800, 1200, 25); if (E2 === E1) throw new Error('retry'); const e1 = F(E1, 100), e2 = F(E2, 100), v = pick(['usd', 'inr']);
      const usd = e2.sub(e1).div(e1).mul(100), inr = e1.sub(e2).div(e2).mul(100);
      const ch = x => `${F(x).sign > 0 ? 'appreciated' : 'depreciated'} by ${fixed(F(x).abs(), 2)}%`;
      return QI(`The exchange rate moves from ₹${num(e1)} per US dollar to ₹${num(e2)} per US dollar. ${v === 'usd' ? 'Measured in rupees per dollar, the dollar has:' : 'Measured in dollars per rupee, the rupee has:'} (correct to two decimals)`, buildS(ch(v === 'usd' ? usd : inr), [ch(v === 'usd' ? usd.neg() : inr.neg()), ch(v === 'usd' ? inr : usd), ch(v === 'usd' ? inr.neg() : usd.neg()), ch(v === 'usd' ? e2.sub(e1).div(e2).mul(100) : e1.sub(e2).div(e1).mul(100))]), 'A rise in rupees per dollar means the dollar has appreciated and the rupee has depreciated; measure each change against its own starting value.', v === 'usd' ? [`(${num(e2)} − ${num(e1)}) ÷ ${num(e1)} × 100 ${ap(usd, 2)}`] : [`Dollars per rupee: 1/${num(e1)} → 1/${num(e2)}`, `(${num(e1)} − ${num(e2)}) ÷ ${num(e2)} × 100 ${ap(inr, 2)}`], { E1, E2, v });
    } });

  def({ id: 'e_ppc', unit: P4('ch01-u02'), name: 'Opportunity cost on a PPC', concept: 'Marginal opportunity cost',
    make(d) {
      const k = 5, y = [RS(50, 200, 5)]; let lost = R(1, 6); for (let i = 1; i < k; i++) { y.push(y[i - 1] - lost); lost += R(1, 8); } if (y[k - 1] < 0) throw new Error('retry');
      const i = R(1, k - 1), moc = y[i - 1] - y[i];
      return QI(`Production possibilities: guns 0, 1, 2, 3, 4 with butter ${y.join(', ')} respectively. What is the opportunity cost of producing gun number ${i} (in units of butter)?`, buildN(F(moc), [F(y[i]), F(y[0] - y[i]), F(i < k - 1 ? y[i] - y[i + 1] : moc + 1), roundDp(F(y[0] - y[i], i), 2)]), 'Marginal opportunity cost = butter given up for one more gun; it rises along a concave PPC.', [`${y[i - 1]} − ${y[i]} = ${PL(moc, 'unit')} of butter`], { y, i });
    } });

  /* =====================================================================================
     ENGINE: validation, seeded generation, never-repeat history, spaced fresh sets
     ===================================================================================== */
  const DIFF = { easy: 'easy', core: 'easy', moderate: 'moderate', ICAI: 'ICAI', icai: 'ICAI', hard: 'ICAI', challenging: 'ICAI' };
  const normD = d => DIFF[d] || pick(['easy', 'moderate', 'moderate', 'ICAI']);
  const hashStr = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
  const BAD = /undefined|NaN|null|Infinity|\[object/;
  function validMcq(x) {
    return x && x.kind === 'mcq' && typeof x.q === 'string' && x.q.length > 10 && Array.isArray(x.options) && x.options.length === 4 && new Set(x.options).size === 4 && x.options.every(o => typeof o === 'string' && o.length && !BAD.test(o))
      && Number.isInteger(x.answer) && x.answer >= 0 && x.answer < 4 && Array.isArray(x.steps) && x.steps.length >= 2 && x.steps.length <= 10 && x.steps[x.steps.length - 1] === 'Answer: ' + x.options[x.answer]
      && !BAD.test(x.q + x.explain + x.steps.join('|'));
  }
  function validDesc(x) {
    return x && x.kind === 'desc' && x.q && Array.isArray(x.scheme) && x.scheme.length && Math.abs(x.scheme.reduce((s, p) => s + p.m, 0) - x.marks) < 1e-9 && Array.isArray(x.model) && x.model.length && !BAD.test(JSON.stringify(x));
  }
  const jsonSafe = o => JSON.parse(JSON.stringify(o, (k, v) => typeof v === 'bigint' ? v.toString() : v instanceof Fx ? fr(v) : v));
  function makeFrom(G, d, kind, seed) {
    const prev = rnd; let s0 = seed == null ? (Math.random() * 4294967296) >>> 0 : seed >>> 0;
    try {
      for (let k = 0; k < 250; k++) {
        const sd = (s0 + Math.imul(k, 0x9E3779B1)) >>> 0; rnd = mulberry(sd);
        try {
          const dd = normD(d), x = kind === 'desc' ? G.desc.call(G, dd) : G.make.call(G, dd);
          if (kind === 'desc' ? !validDesc(x) : !validMcq(x)) continue;
          const paper = G.paper, marks = kind === 'desc' ? x.marks : (paper === 'p1' || paper === 'p2' ? 2 : 1);
          return Object.assign(x, { id: `${G.id}-${sd.toString(36)}`, gen: G.id, unit: G.unit[0], units: G.unit.slice(), concept: G.concept, paper, marks, difficulty: dd, seed: sd, data: jsonSafe(x.data || {}) });
        } catch (e) { if (typeof globalThis !== "undefined" && globalThis.CAGEN_DEBUG) console.warn(G.id, e.message); }
      }
      return null;
    } finally { rnd = prev; }
  }
  const forUnit = (uid, kind = 'mcq') => GENS.filter(G => G.unit.includes(uid) && G.kinds.includes(kind) && (kind === 'desc' ? G.desc : G.make));
  const has = uid => forUnit(uid).length > 0 || forUnit(uid, 'desc').length > 0;
  const units = () => [...new Set(GENS.flatMap(G => G.unit))].sort();
  const list = uid => GENS.filter(G => !uid || G.unit.includes(uid)).map(G => ({ id: G.id, name: G.name, unit: G.unit.slice(), concept: G.concept, paper: G.paper, kinds: G.kinds.slice() }));

  /* ---------- per-student history (localStorage 'sv_cagen') ---------- */
  const HK = 'sv_cagen', MAXK = 1500, MAXH = 400;
  let HIST = null;
  const today = () => Math.floor(Date.now() / 864e5);
  function hist() {
    if (HIST) return HIST;
    try { HIST = JSON.parse(localStorage.getItem(HK) || 'null'); } catch (e) { HIST = null; }
    if (!HIST || HIST.v !== 1) HIST = { v: 1, n: 0, s: {}, h: [] };
    return HIST;
  }
  function saveHist() {
    const H = hist(), keys = Object.keys(H.s);
    if (keys.length > MAXK) keys.sort((a, b) => H.s[a][1] - H.s[b][1]).slice(0, keys.length - MAXK).forEach(k => delete H.s[k]);
    if (H.h.length > MAXH) H.h = H.h.slice(-MAXH);
    try { localStorage.setItem(HK, JSON.stringify(H)); } catch (e) { /* storage full or blocked: keep in memory */ }
  }
  const GAP_T = [1, 2, 4, 8, 16, 32], GAP_D = [0, 1, 3, 7, 14, 30];
  function record(key, ok) {
    const H = hist(), e = H.s[key] || [0, H.n, today(), 0];
    e[0] = ok ? Math.min(5, e[0] + 1) : 0; e[1] = H.n; e[2] = today(); if (!ok) e[3] = Math.min(99, e[3] + 1);
    H.s[key] = e; saveHist(); return e;
  }
  function priority(key, H) {           // lower = sooner
    const e = H.s[key]; if (!e) return 1 + rnd();                            // never seen: high priority
    const tests = H.n - e[1], days = today() - e[2], box = e[0];
    const due = tests >= GAP_T[box] || (days >= GAP_D[box] && days > 0) || (box === 0 && tests >= 1);
    if (box === 0 && tests >= 1) return 0 + rnd() * .5 - Math.min(e[3], 5) * .05;   // wrong last time: first
    if (due) return 1.5 + box * .3 + rnd();
    return 10 + (GAP_T[box] - tests) + rnd();                                   // resting
  }
  const fp = x => hashStr(x.q + '|' + x.options.slice().sort().join('|'));        // fingerprint: stem + option set
  const seen = x => hist().h.includes(fp(x));
  const markSeen = x => { const H = hist(), f = fp(x); if (!H.h.includes(f)) H.h.push(f); };

  function shuffleOpts(m) {
    const order = shuffle([0, 1, 2, 3].slice(0, m.options.length));
    return Object.assign({}, m, { options: order.map(i => m.options[i]), answer: order.indexOf(m.answer) });
  }

  /* ---------- public API ---------- */
  function next(uid, o = {}) {
    const kind = o.kind || 'mcq', gs = o.gen ? GENS.filter(G => G.id === o.gen) : forUnit(uid, kind); if (!gs.length) return null;
    const prev = rnd; if (o.seed != null) rnd = mulberry(o.seed >>> 0);
    try {
      const order = shuffle(gs);
      for (let t = 0; t < order.length * 3; t++) {
        const G = order[t % order.length], x = makeFrom(G, o.difficulty, kind, o.seed != null ? ((o.seed >>> 0) + t * 7919) >>> 0 : undefined);
        if (!x) continue;
        if (kind === 'mcq' && o.seed == null && t < order.length * 2 && seen(x)) continue;            // never the same question twice (recent memory)
        if (uid && x.units.includes(uid)) x.unit = uid;
        if (kind === 'mcq') { x.key = `gen:${G.id}:${fp(x)}`; if (o.seed == null) { markSeen(x); saveHist(); } }
        return x;
      }
      return null;
    } finally { rnd = prev; }
  }
  function mix(uids, n, o = {}) {
    uids = [].concat(uids).filter(u => forUnit(u).length); if (!uids.length || !n) return [];
    const prev = rnd; if (o.seed != null) rnd = mulberry(o.seed >>> 0);
    try {
      const out = [], texts = new Set(), pairs = shuffle(uids.flatMap(u => forUnit(u).map(G => [u, G])));
      let i = 0, guard = 0;
      while (out.length < n && guard++ < n * 20) {
        const [u, G] = pairs[i++ % pairs.length], x = makeFrom(G, o.difficulty, 'mcq', o.seed != null ? ((o.seed >>> 0) + guard * 104729) >>> 0 : undefined);
        const f = x && fp(x); if (!x || texts.has(f) || (o.seed == null && guard < n * 10 && seen(x))) continue;
        x.unit = u; x.key = `gen:${G.id}:${f}`; texts.add(f); out.push(x);
      }
      if (o.seed == null) { out.forEach(x => markSeen(x)); saveHist(); }
      return out;
    } finally { rnd = prev; }
  }
  function freshSet(pool, n, history, o = {}) {
    pool = (pool || []).filter(m => m && Array.isArray(m.options) && m.options.length >= 2);
    const H = history || hist(), prev = rnd; if (o.seed != null) rnd = mulberry(o.seed >>> 0);
    try {
      const uid = o.unit || (pool[0] && (pool[0].unit || (pool[0].key || '').split('#')[0])) || null;
      const keyOf = m => m.key || (uid ? `${uid}#${m.id}` : `#${m.id || hashStr(m.q)}`);
      const canGen = uid && forUnit(uid).length > 0, share = canGen ? (o.genShare != null ? o.genShare : .4) : 0;
      let nGen = Math.round(n * share); if (pool.length < n - nGen) nGen = canGen ? n - pool.length : nGen;
      const ranked = pool.map(m => [priority(keyOf(m), H), m]).sort((a, b) => a[0] - b[0]);
      const take = ranked.slice(0, Math.max(0, n - nGen)).map(([p, m]) => Object.assign(shuffleOpts(m), { key: keyOf(m), source: 'bank', unit: m.unit || uid }));
      const gens = canGen && nGen > 0 ? mix([uid], nGen, { difficulty: o.difficulty, seed: o.seed }).map(x => Object.assign(x, { source: 'gen' })) : [];
      H.n = (H.n || 0) + 1; if (!history) saveHist();
      // interleave: generated items spread through the set
      const out = take.slice(); gens.forEach((g, i) => out.splice(Math.min(out.length, Math.round((i + 1) * (out.length + gens.length) / (gens.length + 1))), 0, g));
      return out.slice(0, n);
    } finally { rnd = prev; }
  }

  const API = { has, units, list, next, desc: (uid, o = {}) => next(uid, Object.assign({}, o, { kind: 'desc' })), mix, freshSet, record,
    history: () => hist(), resetHistory: () => { HIST = { v: 1, n: 0, s: {}, h: [] }; saveHist(); },
    _gens: GENS, _make: (id, d, kind, seed) => { const G = GENS.find(g => g.id === id); return G ? makeFrom(G, d, kind || 'mcq', seed) : null; },
    _kit: { F, Fx, ind, fixed, num, rs, ratio, roundDp, sqrtRound } };
  if (typeof window !== 'undefined') window.CAGen = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})();
