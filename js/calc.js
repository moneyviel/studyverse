/* StudyVerse calculator — a "physical" calculator in a slide-up panel, with three modes:
   - Basic: a 12-digit desk calculator like the ones CA students carry — immediate execution (left to right), %, √, ±, 00,
     M+ M− MR MC, GT (grand total), AC / C, constant mode (repeat =), a ÷ = for 1/a, Indian (1,00,000) or international grouping.
   - Scientific: type a whole expression (order of operations, brackets), sin/cos/tan with DEG/RAD and INV, log, ln, 10ˣ, eˣ,
     x², xʸ, √, ∛, 1/x, n!, %, π, e, EXP and Ans. Worked out by a small hand-written parser (no eval).
   - Financial: TVM solver (N, I/Y, PV, PMT, FV with P/Y and BEGIN/END) and quick tools — EMI, simple & compound interest,
     CAGR, NPV & IRR, depreciation (SLM / WDV), GST add/remove, % change, mark-up & margin — each shows its formula.
   - Small 🧮 button (bottom-left) opens/closes it from any screen; the panel floats above the app. The button is OFF by
     default for school students and ON for CA students; "Show calculator button" in Me / CA Profile overrides that on this
     device (localStorage sv_calc_btn = '1' | '0').
   - Paper roll: every calculation (all modes) is printed on a tape kept across screens and visits (localStorage sv_calc);
     tap a result on the roll to reuse it.
   window.Calc = { open, close, toggle, setMode, on, coach, hint, reset, state, math } — on/coach/hint/reset are the hooks
   Calculator Academy (js/calc-acad.js) uses to follow real key presses. */
(function () {
  const D = document, KEY = 'sv_calc', BTN_KEY = 'sv_calc_btn', MAXD = 12;
  let S = { cur: '0', acc: null, op: null, fresh: true, mem: 0, gt: 0, tape: [], grp: 'in', open: false, lastOp: null, lastVal: null, err: false, mode: 'basic', sx: null, fin: null };
  try { Object.assign(S, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
  S.open = false;
  if (!['basic', 'sci', 'fin'].includes(S.mode)) S.mode = 'basic';
  S.sx = Object.assign({ toks: [], ans: 0, angle: 'deg', inv: false, out: null, done: false, err: '' }, S.sx || {});
  S.fin = Object.assign({ tool: 'tvm', v: {}, bgn: false, cf: ['', '', '', ''] }, S.fin || {});
  if (!Array.isArray(S.fin.cf) || S.fin.cf.length < 2) S.fin.cf = ['', '', '', ''];
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify({ ...S, tape: S.tape.slice(-200) })); } catch (e) {} };

  /* ---------- hooks: every key press / mode change / financial answer is announced to listeners ---------- */
  const subs = new Set();
  const emit = ev => { subs.forEach(f => { try { f(ev); } catch (e) { console.error(e); } }); };

  // ---- number helpers (round to 15 significant digits to avoid 0.1 + 0.2 = 0.30000000000000004) ----
  const clean = x => { if (!isFinite(x)) return NaN; const r = +x.toPrecision(15); return Object.is(r, -0) ? 0 : r; };
  // fit to a 12-digit display like a Casio desk calculator: drop (truncate) decimals that do not fit
  function fit(x) { const neg = x < 0, a = Math.abs(x); const intD = Math.floor(a).toString().length; if (intD > MAXD) return NaN;
    const dec = Math.max(0, MAXD - intD), f = Math.pow(10, dec); let t = Math.floor(+(a * f).toPrecision(15)) / f; t = +t.toFixed(dec); return neg ? -t : t; }
  const group = (i, g = S.grp) => g === 'in' ? (() => { const last3 = i.slice(-3), rest = i.slice(0, -3); return (rest ? rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' : '') + last3; })() : i.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  function fmt(x, g = S.grp) {
    if (typeof x === 'string') x = +x;
    if (!isFinite(x)) return 'Error';
    x = fit(clean(x)); if (!isFinite(x)) return 'Error';
    let s = x.toFixed(Math.max(0, MAXD - Math.floor(Math.abs(x)).toString().length)).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
    const neg = s[0] === '-'; if (neg) s = s.slice(1);
    let [i, d] = s.split('.');
    i = group(i, g);
    return (neg ? '−' : '') + i + (d != null ? '.' + d : '');
  }
  const fmtEntry = s => { // keep what the student is typing (e.g. trailing "." or "0.50")
    const neg = s[0] === '-'; let t = neg ? s.slice(1) : s; let [i, d] = t.split('.');
    i = fmt(+i || 0).replace('−', ''); return (neg ? '−' : '') + i + (t.includes('.') ? '.' + (d || '') : '');
  };
  /* money / financial answers: 2 decimals, grouped */
  function fmt2(x, dp = 2) { if (!isFinite(x)) return '—'; const neg = x < 0; let [i, d] = Math.abs(x).toFixed(dp).split('.'); return (neg ? '−' : '') + group(i) + (d ? '.' + d : ''); }
  const SYM = { '+': '+', '-': '−', '*': '×', '/': '÷' };
  const apply = (a, op, b) => op === '+' ? a + b : op === '-' ? a - b : op === '*' ? a * b : op === '/' ? (b === 0 ? NaN : a / b) : b;

  function print(line, cls, v) { const l = { t: line, c: cls || '' }; if (v != null && isFinite(v)) l.v = v; S.tape.push(l); if (S.tape.length > 200) S.tape.splice(0, S.tape.length - 200); }
  function setErr() { S.err = true; S.cur = 'Error'; S.acc = null; S.op = null; S.fresh = true; print('Error', 'err'); }

  /* ================= BASIC (desk calculator) ================= */
  function digit(k) {
    if (S.err) return;
    if (S.fresh) { S.cur = '0'; S.fresh = false; }
    const digits = S.cur.replace(/[-.]/g, '').length;
    if (k === '.') { if (!S.cur.includes('.')) S.cur += '.'; return; }
    if (digits + k.length > MAXD) return;
    S.cur = S.cur === '0' ? (k === '00' ? '0' : k) : S.cur === '-0' ? '-' + k : S.cur + k;
  }
  const val = () => +S.cur;
  function operator(op) {
    if (S.err) return;
    if (S.op && !S.fresh) {            // chain: 12 + 5 +  → running total 17 shown
      const b = val(); print(`${fmt(b)} ${SYM[op]}`);
      const r = clean(apply(S.acc, S.op, b)); if (isNaN(r)) return setErr();
      S.acc = r; S.cur = String(r);
    } else if (S.op && S.fresh) {      // operator changed before the next number
      const l = S.tape[S.tape.length - 1]; if (l) l.t = l.t.replace(/[+−×÷]$/, SYM[op]);
    } else { S.acc = val(); print(`${fmt(S.acc)} ${SYM[op]}`); }
    S.op = op; S.fresh = true;
  }
  function equals() {
    if (S.err) return;
    let a, op, b;
    if (S.op && S.fresh && S.op === '/') {   // a ÷ =  →  1/a (reciprocal), as on Casio desk calculators; further = keeps dividing by a
      a = 1; op = '/'; b = S.acc; S.lastOp = '/'; S.lastVal = b; print('=');
    } else if (S.op) { a = S.acc; op = S.op; b = val(); S.lastOp = op; S.lastVal = b; print(S.fresh ? '=' : `${fmt(b)} =`); }
    else if (S.lastOp) { a = val(); op = S.lastOp; b = S.lastVal; print(`${fmt(a)} ${SYM[op]} ${fmt(b)} =`); } // repeat last operation, like a desk calculator
    else return;
    const r = clean(apply(a, op, b)); if (isNaN(r)) return setErr();
    print(fmt(r), 'res', r); S.gt = clean(S.gt + r); S.cur = String(r); S.acc = null; S.op = null; S.fresh = true;
  }
  function percent() { // desk-calculator %: a×b% = a·b/100 ; a+b% = a + a·b/100 ; a−b% = a − a·b/100 ; a÷b% = a/b·100
    if (S.err) return;
    const b = val();
    if (!S.op) { const r = clean(b / 100); print(`${fmt(b)} % = ${fmt(r)}`); S.cur = String(r); S.fresh = true; return; }
    const a = S.acc, op = S.op; let r;
    if (op === '*') r = a * b / 100; else if (op === '+') r = a + a * b / 100; else if (op === '-') r = a - a * b / 100; else r = b === 0 ? NaN : a / b * 100;
    r = clean(r); print(`${fmt(b)} % =`); if (isNaN(r)) return setErr();
    print(fmt(r), 'res', r); S.gt = clean(S.gt + r); S.cur = String(r); S.acc = null; S.op = null; S.fresh = true;
  }
  function sqrt() { if (S.err) return; const x = val(); if (x < 0) return setErr(); const r = clean(Math.sqrt(x)); print(`√${fmt(x)} = ${fmt(r)}`); S.cur = String(r); S.fresh = true; }
  function neg() { if (S.err) return; if (S.cur === '0') return; S.cur = S.cur[0] === '-' ? S.cur.slice(1) : '-' + S.cur; }
  function back() { if (S.err || S.fresh) return; S.cur = S.cur.length > 1 && S.cur !== '-0' ? S.cur.slice(0, -1) : '0'; if (S.cur === '-') S.cur = '0'; }
  function clearEntry() { S.err = false; S.cur = '0'; S.fresh = false; }
  function allClear() { S.err = false; S.cur = '0'; S.acc = null; S.op = null; S.fresh = true; S.lastOp = null; print('— AC —', 'sep'); }
  function mem(k) {
    if (S.err && k !== 'MC') return;
    if (k === 'M+') { if (S.op && !S.fresh) equals(); S.mem = clean(S.mem + val()); print(`M+ ${fmt(val())}`, 'mem'); S.fresh = true; }
    if (k === 'M-') { if (S.op && !S.fresh) equals(); S.mem = clean(S.mem - val()); print(`M− ${fmt(val())}`, 'mem'); S.fresh = true; }
    if (k === 'MR') { S.cur = String(S.mem); S.fresh = true; S.err = false; }
    if (k === 'MC') { S.mem = 0; print('MC', 'mem'); }
    if (k === 'GT') { S.cur = String(S.gt); S.fresh = true; print(`GT = ${fmt(S.gt)}`, 'res', S.gt); S.gt = 0; }
  }
  function press(k) {
    if (/^(\d|00|\.)$/.test(k)) digit(k);
    else if ('+-*/'.includes(k) && k.length === 1) operator(k);
    else if (k === '=') equals(); else if (k === '%') percent(); else if (k === 'sqrt') sqrt(); else if (k === 'neg') neg();
    else if (k === 'back') back(); else if (k === 'C') clearEntry(); else if (k === 'AC') allClear(); else mem(k);
    save(); paint(k);
    emit({ type: 'key', mode: 'basic', k, value: S.err ? NaN : +S.cur, mem: S.mem, gt: S.gt, done: !S.err && ['=', '%', 'GT', 'sqrt'].includes(k) });
  }

  /* ================= SCIENTIFIC (expression entry + safe parser) ================= */
  const SCI_TOK = { '+': ['+', '+'], '-': ['−', '-'], '*': ['×', '*'], '/': ['÷', '/'], '(': ['(', '('], ')': [')', ')'],
    pi: ['π', 'pi'], e: ['e', 'e'], ans: ['Ans', 'ans'], exp: ['E', 'E'], neg: ['−', 'neg'],
    sq: ['²', 'sq'], pow: ['^', '^'], recip: ['⁻¹', 'recip'], fact: ['!', '!'], pct: ['%', '%'], sqrt: ['√(', 'sqrt'], cbrt: ['∛(', 'cbrt'] };
  const FN = { sin: ['sin(', 'sin'], cos: ['cos(', 'cos'], tan: ['tan(', 'tan'], log: ['log(', 'log'], ln: ['ln(', 'ln'] };
  const FN_INV = { sin: ['sin⁻¹(', 'asin'], cos: ['cos⁻¹(', 'acos'], tan: ['tan⁻¹(', 'atan'], log: ['10^(', 'tenx'], ln: ['e^(', 'exp'] };
  const CONT = ['+', '-', '*', '/', 'sq', 'pow', 'recip', 'fact', 'pct'];   // after an answer these continue from Ans
  const exprText = (toks = S.sx.toks) => toks.map(t => t.d).join('');

  function lex(toks, ans) {
    const out = []; let num = '';
    const flush = () => { if (!num) return; if (!/^(\d+\.?\d*|\.\d+)(E-?\d+)?$/.test(num)) throw new Error('Syntax'); out.push({ t: 'num', v: parseFloat(num) }); num = ''; };
    for (const tk of toks) {
      const v = tk.v;
      if (/^[\d.]$/.test(v)) { num += v; continue; }
      if (v === 'E') { if (!num) num = '1'; num += 'E'; continue; }               // EXP: 6.02 EXP 23 = 6.02 × 10²³
      if ((v === '-' || v === 'neg') && num.endsWith('E')) { num += '-'; continue; }
      flush();
      if (v.length === 1 && '+-*/^'.includes(v)) out.push({ t: 'op', v });
      else if (v === 'neg') out.push({ t: 'neg' });
      else if (v === '(' || v === ')') out.push({ t: v });
      else if (v === 'pi' || v === 'e' || v === 'ans') out.push({ t: 'num', v: v === 'pi' ? Math.PI : v === 'e' ? Math.E : +ans || 0 });
      else if (['!', '%', 'sq', 'recip'].includes(v)) out.push({ t: 'post', v });
      else out.push({ t: 'fn', v });
    }
    flush(); return out;
  }
  /* expr := term {(+|−) term} · term := unary {(×|÷) unary | implicit ×} · unary := (−|+) unary | power
     power := postfix [^ unary] (right to left) · postfix := primary {! % ² ⁻¹} · primary := number | fn( expr ) | ( expr )
     A missing ")" at the end is closed for you, as on school scientific calculators. */
  function evalToks(toks, angle, ans) {
    const L = lex(toks, ans); let i = 0;
    const peek = () => L[i], next = () => L[i++];
    const fail = k => { throw new Error(k); };
    const M = x => (typeof x === 'number' && isFinite(x) ? x : fail('Math'));
    const toRad = x => angle === 'deg' ? x * Math.PI / 180 : x, fromRad = x => angle === 'deg' ? x * 180 / Math.PI : x;
    function trig(f, x) {
      if (angle === 'deg') { const m = ((x % 360) + 360) % 360;
        if (f === 'sin' && m % 180 === 0) return 0; if (f === 'cos' && (m - 90) % 180 === 0) return 0;
        if (f === 'tan') { if (m % 180 === 0) return 0; if ((m - 90) % 180 === 0) fail('Math'); } }
      const r = Math[f](toRad(x)); return Math.abs(r) < 1e-15 ? 0 : r;
    }
    function call(f, x) {
      switch (f) {
        case 'sin': case 'cos': case 'tan': return trig(f, x);
        case 'asin': case 'acos': return x < -1 || x > 1 ? fail('Math') : fromRad(Math[f](x));
        case 'atan': return fromRad(Math.atan(x));
        case 'log': return x <= 0 ? fail('Math') : Math.log10(x);
        case 'ln': return x <= 0 ? fail('Math') : Math.log(x);
        case 'tenx': return Math.pow(10, x);
        case 'exp': return Math.exp(x);
        case 'sqrt': return x < 0 ? fail('Math') : Math.sqrt(x);
        case 'cbrt': return Math.cbrt(x);
      }
      return fail('Syntax');
    }
    function fact(x) { if (x < 0 || x > 170 || Math.abs(x - Math.round(x)) > 1e-9) fail('Math'); let r = 1; for (let k = 2; k <= Math.round(x); k++) r *= k; return r; }
    function primary() {
      const t = next(); if (!t) fail('Syntax');
      if (t.t === 'num') return t.v;
      if (t.t === '(' || t.t === 'fn') { const v = expr(); if (peek() && peek().t === ')') next(); return t.t === 'fn' ? M(call(t.v, v)) : v; }
      return fail('Syntax');
    }
    function postfix() {
      let v = primary();
      while (peek() && peek().t === 'post') { const p = next().v; v = p === '!' ? fact(v) : p === '%' ? v / 100 : p === 'sq' ? v * v : (v === 0 ? fail('Math') : 1 / v); }
      return v;
    }
    function power() { const b = postfix(); if (peek() && peek().t === 'op' && peek().v === '^') { next(); return M(Math.pow(b, unary())); } return b; }
    function unary() { const t = peek(); if (t && (t.t === 'neg' || (t.t === 'op' && (t.v === '-' || t.v === '+')))) { next(); const v = unary(); return t.v === '+' ? v : -v; } return power(); }
    const starts = t => t && (t.t === 'num' || t.t === 'fn' || t.t === '(' || t.t === 'neg');
    function term() {
      let v = unary();
      for (;;) { const t = peek();
        if (t && t.t === 'op' && (t.v === '*' || t.v === '/')) { next(); const r = unary(); if (t.v === '/' && r === 0) fail('Math'); v = t.v === '*' ? v * r : v / r; }
        else if (starts(t)) v *= unary();           // 2π, 3(4+1), 2sin(30)
        else return v; }
    }
    function expr() { let v = term(); for (;;) { const t = peek(); if (t && t.t === 'op' && (t.v === '+' || t.v === '-')) { next(); const r = term(); v = t.v === '+' ? v + r : v - r; } else return v; } }
    if (!L.length) fail('Syntax');
    const r = expr(); if (i < L.length) fail('Syntax');
    return M(clean(M(r)));
  }
  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  function sciFmt(x) {
    if (!isFinite(x)) return 'Math ERROR';
    if (x === 0) return '0';
    const a = Math.abs(x);
    if (a >= 1e12 || a < 1e-9) { const [m, e] = x.toExponential(9).split('e'); return m.replace(/\.?0+$/, '').replace('-', '−') + '×10' + String(+e).split('').map(c => SUP[c]).join(''); }
    const r = +x.toPrecision(10); let s = String(r); if (/e/.test(s)) s = r.toFixed(12).replace(/\.?0+$/, '');
    const neg = s[0] === '-'; if (neg) s = s.slice(1); const [i, d] = s.split('.');
    return (neg ? '−' : '') + group(i) + (d ? '.' + d : '');
  }
  function sciEquals() {
    const X = S.sx; if (X.done || !X.toks.length) return;
    const txt = exprText();
    try { const r = evalToks(X.toks, X.angle, X.ans); X.out = r; X.ans = r; X.done = true; X.err = ''; print(`${txt} =`); print(sciFmt(r), 'res', r); }
    catch (e) { X.err = e.message === 'Math' ? 'Math ERROR' : 'Syntax ERROR'; X.out = null; print(`${txt} → ${X.err}`, 'err'); }
  }
  function sciPress(k) {
    const X = S.sx;
    if (k === 'AC') { X.toks = []; X.done = false; X.err = ''; X.out = null; }
    else if (k === 'back') { if (X.done || X.err) { X.done = false; X.err = ''; } else X.toks.pop(); }
    else if (k === 'angle') X.angle = X.angle === 'deg' ? 'rad' : 'deg';
    else if (k === 'inv') X.inv = !X.inv;
    else if (k === '=') sciEquals();
    else {
      let tok;
      if (/^\d$/.test(k) || k === '.') tok = { d: k, v: k };
      else if (FN[k]) { const f = X.inv ? FN_INV[k] : FN[k]; tok = { d: f[0], v: f[1] }; X.inv = false; }
      else if (SCI_TOK[k]) tok = { d: SCI_TOK[k][0], v: SCI_TOK[k][1] };
      else return;
      if (X.done || X.err) { X.toks = CONT.includes(k) && X.done ? [{ d: 'Ans', v: 'ans' }] : []; X.done = false; X.err = ''; }
      if (X.toks.length < 120) X.toks.push(tok);
    }
    save(); paint();
    emit({ type: 'key', mode: 'sci', k, value: X.done ? X.out : NaN, done: k === '=' && X.done, expr: exprText(), angle: X.angle, inv: X.inv });
  }
  /* for tests and Calculator Academy: run a list of scientific keys, e.g. ['sin','3','0',')'] */
  function sciRun(keys, angle = 'deg') {
    const toks = []; let inv = false;
    keys.forEach(k => { if (k === 'inv') { inv = !inv; return; } if (/^\d$/.test(k) || k === '.') toks.push({ d: k, v: k }); else if (FN[k]) { toks.push({ d: '', v: (inv ? FN_INV : FN)[k][1] }); inv = false; } else if (SCI_TOK[k]) toks.push({ d: '', v: SCI_TOK[k][1] }); });
    return evalToks(toks, angle, 0);
  }

  /* ================= FINANCIAL ================= */
  /* rate root finder: scan for sign changes, then bisection; picks the root nearest 10% when there are several */
  function root(f, lo, hi) {
    let best = NaN, bd = Infinity, px = null, pf = null;
    const take = r => { const d = Math.abs(r - 0.1); if (d < bd) { bd = d; best = r; } };
    for (let x = lo; x <= hi; x += x < 1 ? 0.0025 : 0.05) {
      const fx = f(x); if (!isFinite(fx)) { px = null; continue; }
      if (fx === 0) take(x);
      else if (px !== null && (pf < 0) !== (fx < 0)) { let a = px, b = x, fa = pf; for (let it = 0; it < 200; it++) { const m = (a + b) / 2, fm = f(m); if ((fa < 0) === (fm < 0)) { a = m; fa = fm; } else b = m; } take((a + b) / 2); }
      px = x; pf = fx;
    }
    return best;
  }
  const FINM = {
    /* PV(1+i)^N + PMT(1+i·t)((1+i)^N − 1)/i + FV = 0 ; i = I/Y ÷ P/Y ÷ 100 ; t = 1 (BEGIN) or 0 (END) */
    tvm(solve, o) {
      const py = o.PY || 1, t = o.bgn ? 1 : 0, i = o.IY / 100 / py, z = Math.abs(i) < 1e-12;
      const g = n => Math.pow(1 + i, n);
      if (solve === 'FV') return z ? -(o.PV + o.PMT * o.N) : -(o.PV * g(o.N) + o.PMT * (1 + i * t) * (g(o.N) - 1) / i);
      if (solve === 'PV') return z ? -(o.FV + o.PMT * o.N) : -(o.FV + o.PMT * (1 + i * t) * (g(o.N) - 1) / i) / g(o.N);
      if (solve === 'PMT') { if (!o.N) return NaN; return z ? -(o.PV + o.FV) / o.N : -(o.PV * g(o.N) + o.FV) * i / ((1 + i * t) * (g(o.N) - 1)); }
      if (solve === 'N') { if (z) return o.PMT ? -(o.PV + o.FV) / o.PMT : NaN; const k = o.PMT * (1 + i * t); return Math.log((k - o.FV * i) / (k + o.PV * i)) / Math.log(1 + i); }
      if (solve === 'IY') {
        const f = x => { if (Math.abs(x) < 1e-12) return o.PV + o.PMT * o.N + o.FV; const G = Math.pow(1 + x, o.N); return o.PV * G + o.PMT * (1 + x * t) * (G - 1) / x + o.FV; };
        const r = root(f, -0.99, 10); return isFinite(r) ? r * py * 100 : NaN;
      }
      return NaN;
    },
    emi(P, rate, n) { const r = rate / 1200; if (!(n > 0)) return NaN; if (!r) return P / n; const g = Math.pow(1 + r, n); return P * r * g / (g - 1); },
    npv(rate, cfs) { const r = rate / 100; return cfs.reduce((s, c, t) => s + c / Math.pow(1 + r, t), 0); },
    irr(cfs) { if (!cfs.some(c => c < 0) || !cfs.some(c => c > 0)) return NaN; const r = root(x => cfs.reduce((s, c, t) => s + c / Math.pow(1 + x, t), 0), -0.99, 10); return isFinite(r) ? r * 100 : NaN; },
    cagr(a, b, y) { return a > 0 && b > 0 && y > 0 ? (Math.pow(b / a, 1 / y) - 1) * 100 : NaN; },
    si(P, R, T) { return P * R * T / 100; },
    ci(P, R, T, m) { m = m || 1; return P * Math.pow(1 + R / (100 * m), m * T) - P; },
    slm(c, s, n) { return n > 0 ? (c - s) / n : NaN; },
    wdvRate(c, s, n) { return c > 0 && s > 0 && n > 0 && s < c ? (1 - Math.pow(s / c, 1 / n)) * 100 : NaN; },
    gstAdd(a, r) { return a * r / 100; },
    gstIn(a, r) { return a - a * 100 / (100 + r); },
    pct(o, n) { return o ? (n - o) / Math.abs(o) * 100 : NaN; },
  };
  const TOOLS = [
    { id: 'tvm', name: 'TVM', title: 'Time value of money (TVM)', fields: [['N', 'N · number of periods'], ['IY', 'I/Y · interest % a year'], ['PV', 'PV · present value'], ['PMT', 'PMT · payment each period'], ['FV', 'FV · future value'], ['PY', 'P/Y · payments a year', '1']],
      acts: [['N', 'Find N'], ['IY', 'Find I/Y'], ['PV', 'Find PV'], ['PMT', 'Find PMT'], ['FV', 'Find FV']], note: 'Signs: money you pay out is minus (−), money you get is plus (+).' },
    { id: 'emi', name: 'EMI', title: 'Loan EMI', fields: [['P', 'Loan amount (₹)'], ['R', 'Interest rate (% a year)'], ['N', 'Tenure (months)']], acts: [['EMI', 'Find EMI']] },
    { id: 'int', name: 'Interest', title: 'Simple & compound interest', fields: [['P', 'Principal (₹)'], ['R', 'Rate (% a year)'], ['T', 'Time (years)'], ['M', 'Compounding times a year (CI)', '1']], acts: [['SI', 'Simple interest'], ['CI', 'Compound interest']] },
    { id: 'cagr', name: 'CAGR', title: 'CAGR — yearly growth rate', fields: [['A', 'Starting value'], ['B', 'Ending value'], ['Y', 'Number of years']], acts: [['CAGR', 'Find CAGR']] },
    { id: 'npv', name: 'NPV · IRR', title: 'NPV & IRR from cash flows', fields: [['R', 'Discount rate % (for NPV)']], cf: true, acts: [['NPV', 'Find NPV'], ['IRR', 'Find IRR']] },
    { id: 'dep', name: 'Depreciation', title: 'Depreciation (SLM / WDV)', fields: [['C', 'Cost of the asset (₹)'], ['S', 'Residual (scrap) value (₹)'], ['N', 'Useful life (years)'], ['R', 'WDV rate % (empty = work it out)']], acts: [['SLM', 'Straight line (SLM)'], ['WDV', 'Written down (WDV)']] },
    { id: 'gst', name: 'GST', title: 'GST — add or remove', fields: [['A', 'Amount (₹)'], ['R', 'GST rate %', '18']], chips: [5, 12, 18, 28], acts: [['ADD', 'Add GST'], ['REM', 'Remove GST']] },
    { id: 'pct', name: '% change', title: 'Percentage change', fields: [['O', 'Old value'], ['N', 'New value']], acts: [['PCT', 'Find % change']] },
    { id: 'mark', name: 'Mark-up · margin', title: 'Mark-up & margin', fields: [['C', 'Cost price (₹)'], ['S', 'Selling price (₹)'], ['P', 'Percent (to find a price)']], acts: [['MM', 'Mark-up & margin'], ['SPU', 'Price for mark-up %'], ['SPM', 'Price for margin %']] },
  ];
  const toolOf = id => TOOLS.find(t => t.id === id) || TOOLS[0];
  const num = s => { if (s == null) return NaN; const t = String(s).replace(/[,\s₹%]/g, '').replace(/[−–]/g, '-'); return t === '' || t === '-' ? NaN : +t; };
  const fv = (tool, k) => { const T = toolOf(tool), f = T.fields.find(x => x[0] === k), v = (S.fin.v[tool] || {})[k]; return v != null && v !== '' ? v : (f && f[2]) || ''; };
  function finCompute(tool, act) {
    const T = toolOf(tool), g = k => num(fv(tool, k)), need = (ks, names) => { const miss = ks.filter(k => !isFinite(g(k))); if (miss.length) throw new Error(`Please fill in ${miss.map(k => names[k] || k).join(', ')}.`); };
    const NM = Object.fromEntries(T.fields.map(f => [f[0], f[1].split(' · ')[0].split(' (')[0]]));
    let value, label, formula, lines = [], table = null, unit = '₹', fill = null, tape;
    const pc = x => fmt2(x) + '%';
    if (tool === 'tvm') {
      const all = ['N', 'IY', 'PV', 'PMT', 'FV']; need(all.filter(k => k !== act), NM);
      const o = { N: g('N'), IY: g('IY'), PV: g('PV'), PMT: g('PMT'), FV: g('FV'), PY: isFinite(g('PY')) && g('PY') > 0 ? g('PY') : 1, bgn: S.fin.bgn };
      value = FINM.tvm(act, o); label = { N: 'N', IY: 'I/Y', PV: 'PV', PMT: 'PMT', FV: 'FV' }[act]; unit = act === 'N' ? '' : act === 'IY' ? '%' : '₹';
      if (!isFinite(value)) throw new Error('No answer with these numbers. Check the signs: money you pay out is minus (−), money you get is plus (+).');
      formula = 'PV(1+i)ᴺ + PMT(1+i·t)((1+i)ᴺ − 1)/i + FV = 0, where i = I/Y ÷ P/Y ÷ 100 and t = 1 in BEGIN, 0 in END';
      lines.push(`${S.fin.bgn ? 'BEGIN' : 'END'} mode · P/Y ${o.PY}`);
      fill = [act, +value.toFixed(act === 'IY' ? 4 : 2)];
      tape = `TVM ${label} (${S.fin.bgn ? 'BGN' : 'END'})`;
    } else if (tool === 'emi') {
      need(['P', 'R', 'N'], NM); const P = g('P'), R = g('R'), N = g('N'); value = FINM.emi(P, R, N); label = 'EMI';
      if (!isFinite(value)) throw new Error('Tenure must be more than 0 months.');
      lines.push(`Total paid: ₹${fmt2(value * N)}`, `Total interest: ₹${fmt2(value * N - P)}`);
      formula = 'EMI = P × r × (1+r)ⁿ ÷ ((1+r)ⁿ − 1), where r = yearly rate ÷ 12 ÷ 100 and n = months'; tape = `EMI ${fmt2(P, 0)} @ ${R}% × ${N} m`;
    } else if (tool === 'int') {
      need(['P', 'R', 'T'], NM); const P = g('P'), R = g('R'), Tt = g('T'), m = isFinite(g('M')) && g('M') > 0 ? g('M') : 1;
      if (act === 'SI') { value = FINM.si(P, R, Tt); label = 'Simple interest'; formula = 'SI = P × R × T ÷ 100'; }
      else { value = FINM.ci(P, R, Tt, m); label = 'Compound interest'; formula = 'CI = P × (1 + R ÷ (100 × m))^(m × T) − P, where m = times compounded a year'; lines.push(`Compounded ${m} time${m === 1 ? '' : 's'} a year`); }
      lines.unshift(`Amount (P + interest): ₹${fmt2(P + value)}`); tape = `${act} ${fmt2(P, 0)} @ ${R}% × ${Tt} y`;
    } else if (tool === 'cagr') {
      need(['A', 'B', 'Y'], NM); value = FINM.cagr(g('A'), g('B'), g('Y')); label = 'CAGR'; unit = '%';
      if (!isFinite(value)) throw new Error('Values and years must be more than 0.');
      formula = 'CAGR = (Ending ÷ Starting)^(1 ÷ years) − 1'; tape = `CAGR ${fmt2(g('A'), 0)} → ${fmt2(g('B'), 0)} in ${g('Y')} y`;
    } else if (tool === 'npv') {
      const cfs = S.fin.cf.map(num); const last = cfs.map(isFinite).lastIndexOf(true);
      if (last < 1) throw new Error('Type at least CF0 (today) and CF1.');
      const list = cfs.slice(0, last + 1).map(c => (isFinite(c) ? c : 0));
      if (act === 'NPV') { need(['R'], NM); value = FINM.npv(g('R'), list); label = 'NPV'; formula = 'NPV = CF0 + CF1 ÷ (1+r) + CF2 ÷ (1+r)² + …'; tape = `NPV @ ${g('R')}% [${list.join(', ')}]`; }
      else { value = FINM.irr(list); label = 'IRR'; unit = '%'; if (!isFinite(value)) throw new Error('IRR needs at least one minus (money out) and one plus (money in) cash flow.'); formula = 'IRR is the rate at which NPV = 0 (found by trying rates, like the exam trial-and-error method)'; tape = `IRR [${list.join(', ')}]`; }
    } else if (tool === 'dep') {
      need(['C', 'S', 'N'], NM); const c = g('C'), s = g('S'), n = Math.round(g('N'));
      if (!(n > 0) || c <= 0) throw new Error('Cost and life must be more than 0.');
      let rate = act === 'WDV' ? (isFinite(g('R')) ? g('R') : FINM.wdvRate(c, s, n)) : null;
      if (act === 'WDV' && !isFinite(rate)) throw new Error('Type a WDV rate, or a residual value more than 0 and less than the cost.');
      const rows = []; let open = c;
      for (let y = 1; y <= Math.min(n, 10); y++) { const d = act === 'SLM' ? FINM.slm(c, s, n) : open * rate / 100; rows.push([y, open, d, open - d]); open -= d; }
      value = rows[0][2]; label = act === 'SLM' ? 'Depreciation a year' : 'Year 1 depreciation';
      formula = act === 'SLM' ? 'Depreciation each year = (Cost − Residual value) ÷ Life' : 'Depreciation = Opening value × Rate; Rate = 1 − (Residual ÷ Cost)^(1 ÷ Life)';
      if (act === 'WDV') lines.push(`Rate used: ${fmt2(rate)}% a year`);
      table = rows; tape = `${act} cost ${fmt2(c, 0)} life ${n} y`;
    } else if (tool === 'gst') {
      need(['A', 'R'], NM); const a = g('A'), r = g('R');
      if (act === 'ADD') { const t = FINM.gstAdd(a, r); value = a + t; label = 'Total with GST'; lines.push(`GST (${r}%): ₹${fmt2(t)} = CGST ₹${fmt2(t / 2)} + SGST ₹${fmt2(t / 2)}`); formula = 'GST = Amount × Rate ÷ 100; Total = Amount + GST'; }
      else { const t = FINM.gstIn(a, r); value = a - t; label = 'Price before GST'; lines.push(`GST inside the price: ₹${fmt2(t)} = CGST ₹${fmt2(t / 2)} + SGST ₹${fmt2(t / 2)}`); formula = 'Price before GST = Amount × 100 ÷ (100 + Rate)'; }
      tape = `GST ${act === 'ADD' ? '+' : '−'}${r}% on ${fmt2(a)}`;
    } else if (tool === 'pct') {
      need(['O', 'N'], NM); value = FINM.pct(g('O'), g('N')); label = '% change'; unit = '%';
      if (!isFinite(value)) throw new Error('The old value cannot be 0.');
      lines.push(value >= 0 ? 'It went up.' : 'It went down.'); formula = '% change = (New − Old) ÷ Old × 100'; tape = `% change ${fmt2(g('O'))} → ${fmt2(g('N'))}`;
    } else {
      const c = g('C');
      if (act === 'MM') { need(['C', 'S'], NM); const s = g('S'), p = s - c; if (!c || !s) throw new Error('Cost and selling price cannot be 0.'); value = p / c * 100; label = 'Mark-up'; unit = '%'; lines.push(`Margin: ${pc(p / s * 100)} of the selling price`, `Profit: ₹${fmt2(p)}`); formula = 'Mark-up % = Profit ÷ Cost × 100 · Margin % = Profit ÷ Selling price × 100'; tape = `Mark-up C ${fmt2(c)} S ${fmt2(s)}`; }
      else { need(['C', 'P'], NM); const p = g('P'); if (act === 'SPM' && p >= 100) throw new Error('Margin must be less than 100%.');
        value = act === 'SPU' ? c * (1 + p / 100) : c / (1 - p / 100); label = 'Selling price'; lines.push(`Profit: ₹${fmt2(value - c)}`);
        formula = act === 'SPU' ? 'Selling price = Cost × (1 + Mark-up % ÷ 100)' : 'Selling price = Cost ÷ (1 − Margin % ÷ 100)'; tape = `Price C ${fmt2(c)} ${act === 'SPU' ? 'mark-up' : 'margin'} ${p}%`; fill = ['S', +value.toFixed(2)]; }
    }
    return { value, label, unit, formula, lines, table, fill, tape };
  }

  /* ================= UI ================= */
  const KEYS = [
    ['MC', 'MC', 'kf'], ['MR', 'MR', 'kf'], ['M-', 'M−', 'kf'], ['M+', 'M+', 'kf'], ['GT', 'GT', 'kf'],
    ['sqrt', '√', 'kf'], ['%', '%', 'kf'], ['neg', '±', 'kf'], ['back', '⌫', 'kf'], ['AC', 'AC', 'kc'],
    ['7', '7'], ['8', '8'], ['9', '9'], ['/', '÷', 'ko'], ['C', 'C', 'kc'],
    ['4', '4'], ['5', '5'], ['6', '6'], ['*', '×', 'ko'], ['-', '−', 'ko'],
    ['1', '1'], ['2', '2'], ['3', '3'], ['+', '+', 'ko kt'], ['=', '=', 'ke kt'],
    ['0', '0'], ['00', '00'], ['.', '.']];
  const LABEL = { MC: 'Memory clear', MR: 'Memory recall', 'M-': 'Memory minus', 'M+': 'Memory plus', GT: 'Grand total', sqrt: 'Square root', '%': 'Percent', neg: 'Change sign', back: 'Delete last digit', AC: 'All clear', C: 'Clear entry', '/': 'Divide', '*': 'Multiply', '-': 'Minus', '+': 'Plus', '=': 'Equals', '.': 'Decimal point' };
  const SKEYS = [
    ['angle', 'DEG', 'kf'], ['inv', 'INV', 'kf'], ['(', '(', 'kf'], [')', ')', 'kf'], ['AC', 'AC', 'kc'],
    ['sin', 'sin', 'kf'], ['cos', 'cos', 'kf'], ['tan', 'tan', 'kf'], ['pi', 'π', 'kf'], ['back', '⌫', 'kf'],
    ['log', 'log', 'kf'], ['ln', 'ln', 'kf'], ['e', 'e', 'kf'], ['ans', 'Ans', 'kf'], ['exp', 'EXP', 'kf'],
    ['sq', 'x²', 'kf'], ['pow', 'xʸ', 'kf'], ['sqrt', '√', 'kf'], ['cbrt', '∛', 'kf'], ['recip', '1/x', 'kf'],
    ['7', '7'], ['8', '8'], ['9', '9'], ['/', '÷', 'ko'], ['fact', 'n!', 'kf'],
    ['4', '4'], ['5', '5'], ['6', '6'], ['*', '×', 'ko'], ['pct', '%', 'kf'],
    ['1', '1'], ['2', '2'], ['3', '3'], ['-', '−', 'ko'], ['=', '=', 'ke kt'],
    ['0', '0'], ['.', '.'], ['neg', '(−)', 'kf'], ['+', '+', 'ko']];
  const SLABEL = { angle: 'Angle unit: degrees or radians', inv: 'Inverse (second function)', '(': 'Open bracket', ')': 'Close bracket', AC: 'All clear', sin: 'Sine', cos: 'Cosine', tan: 'Tangent', pi: 'Pi', back: 'Delete last', log: 'Log base 10', ln: 'Natural log', e: 'e (2.718…)', ans: 'Last answer', exp: 'Times ten to the power (EXP)',
    sq: 'Square', pow: 'Power', sqrt: 'Square root', cbrt: 'Cube root', recip: 'Reciprocal, 1 over x', '/': 'Divide', fact: 'Factorial', '*': 'Multiply', pct: 'Percent', '-': 'Minus', '=': 'Equals', '.': 'Decimal point', neg: 'Negative sign', '+': 'Plus' };
  const MODES = [['basic', 'Basic'], ['sci', 'Scientific'], ['fin', 'Financial']];
  let fab, panel, hl = [];
  function build() {
    const st = D.createElement('style'); st.textContent = CSS; D.head.appendChild(st);
    fab = D.createElement('button'); fab.id = 'calcFab'; fab.type = 'button'; fab.setAttribute('aria-label', 'Calculator'); fab.setAttribute('aria-expanded', 'false');
    fab.innerHTML = '<span aria-hidden="true">🧮</span>'; fab.onclick = toggle; fab.hidden = true; D.body.appendChild(fab);
    panel = D.createElement('section'); panel.id = 'calcPanel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Calculator'); panel.hidden = true;
    panel.innerHTML = `<div class="cx-body">
      <div class="cx-top"><span class="cx-brand">StudyVerse <b>CX-12</b></span>
        <button type="button" class="cx-mini" id="cxLearn" aria-label="Learn to use this calculator: Calculator Academy">🎓 Learn</button>
        <button type="button" class="cx-mini" id="cxTapeBtn" aria-pressed="false">🧾 Roll</button>
        <button type="button" class="cx-mini" id="cxGrp" data-hl="grp" title="Number grouping" aria-label="Number grouping">1,00,000</button>
        <button type="button" class="cx-close" id="cxClose" aria-label="Close calculator">✕</button></div>
      <div class="cx-modes" role="group" aria-label="Calculator type">${MODES.map(([m, n]) => `<button type="button" class="cx-mode" data-mode="${m}" aria-pressed="false">${n}</button>`).join('')}</div>
      <div class="cx-coach" id="cxCoach" role="status" aria-live="polite" hidden></div>
      <div class="cx-tape" id="cxTape" hidden aria-label="Paper roll — tap a result to use it"></div>
      <div id="cxBasic">
        <div class="cx-lcd"><div class="cx-ind"><span id="cxM">M</span><span id="cxOp"></span><span id="cxGT">GT</span><span id="cxE">E</span></div>
          <output class="cx-num" id="cxNum" aria-live="polite">0</output></div>
        <div class="cx-keys">${KEYS.map(([k, t, c]) => `<button type="button" class="cx-k ${c || 'kn'}" data-k="${k}" aria-label="${LABEL[k] || t}">${t}</button>`).join('')}</div></div>
      <div id="cxSci" hidden>
        <div class="cx-lcd cx-slcd"><div class="cx-ind"><span id="cxAng" class="on">DEG</span><span id="cxInv">INV</span><span id="cxSE">E</span></div>
          <div class="cx-expr" id="cxExpr" aria-label="Expression"></div><output class="cx-num cx-snum" id="cxSNum" aria-live="polite">0</output></div>
        <div class="cx-keys cx-skeys">${SKEYS.map(([k, t, c]) => `<button type="button" class="cx-k ${c || 'kn'}" data-k="${k}" aria-label="${SLABEL[k] || t}"${k === 'inv' ? ' aria-pressed="false"' : ''}>${t}</button>`).join('')}</div></div>
      <div id="cxFin" class="cx-fin" hidden></div></div>`;
    D.body.appendChild(panel);
    panel.querySelectorAll('#cxBasic .cx-k').forEach(b => b.addEventListener('click', () => { press(b.dataset.k); buzz(); }));
    panel.querySelectorAll('#cxSci .cx-k').forEach(b => b.addEventListener('click', () => { sciPress(b.dataset.k); buzz(); }));
    panel.querySelectorAll('.cx-mode').forEach(b => b.onclick = () => setMode(b.dataset.mode));
    panel.querySelector('#cxClose').onclick = close;
    panel.querySelector('#cxLearn').onclick = () => { if (window.CalcAcademy) { close(); CalcAcademy.open(); } };
    panel.querySelector('#cxGrp').onclick = () => { S.grp = S.grp === 'in' ? 'intl' : 'in'; save(); paint(); if (S.mode === 'fin') renderFin(); emit({ type: 'key', mode: S.mode, k: 'grp', grp: S.grp, value: S.mode === 'basic' ? +S.cur : NaN }); };
    panel.querySelector('#cxTapeBtn').onclick = () => { const t = panel.querySelector('#cxTape'); t.hidden = !t.hidden; panel.querySelector('#cxTapeBtn').setAttribute('aria-pressed', String(!t.hidden)); paint(); };
    panel.querySelector('#cxTape').addEventListener('click', e => {
      const b = e.target.closest('[data-v]');
      if (b) { const v = b.dataset.v;
        if (S.mode === 'sci') { const X = S.sx; if (X.done || X.err) { X.toks = []; X.done = false; X.err = ''; } String(+v).replace(/e\+?/, 'E').split('').forEach(ch => X.toks.push(ch === 'E' ? { d: 'E', v: 'E' } : ch === '-' ? { d: '−', v: 'neg' } : { d: ch, v: ch })); }
        else if (S.mode === 'fin') { const inp = lastInput && panel.contains(lastInput) ? lastInput : null; if (inp) { inp.value = String(+(+v).toFixed(6)); inp.dispatchEvent(new Event('input', { bubbles: true })); } else try { toast('Tap a box first, then the number on the roll'); } catch (x) {} }
        else { S.cur = v; S.fresh = true; S.err = false; }
        save(); paint(); }
      if (e.target.id === 'cxTapeClr') { S.tape = []; save(); paint(); }
    });
    D.addEventListener('keydown', e => {
      if (panel.hidden || e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === 'Escape') { close(); e.stopPropagation(); return; }
      const a = D.activeElement; if (a && /^(input|textarea|select)$/i.test(a.tagName)) return;
      if (S.mode === 'fin') return;
      if (S.mode === 'sci') {
        const m = { Enter: '=', '=': '=', Backspace: 'back', Delete: 'AC', '^': 'pow', '!': 'fact', '%': 'pct', x: '*', X: '*' }[e.key];
        const k = m || (/^[0-9.+\-*/()]$/.test(e.key) ? e.key : null);
        if (k) { sciPress(k); e.preventDefault(); e.stopPropagation(); }
        return;
      }
      const m = { Enter: '=', '=': '=', Backspace: 'back', Delete: 'C', '%': '%', x: '*', X: '*' }[e.key];
      const k = m || (/^[0-9.+\-*/]$/.test(e.key) ? e.key : null);
      if (k) { press(k); e.preventDefault(); e.stopPropagation(); }
    }, true);
  }
  const buzz = () => { if (navigator.vibrate) try { navigator.vibrate(8); } catch (e) {} };
  let lastInput = null;

  function renderFin() {
    const box = panel.querySelector('#cxFin'), T = toolOf(S.fin.tool), vals = S.fin.v[T.id] = S.fin.v[T.id] || {};
    const fid = k => `cxF_${T.id}_${k}`;
    box.innerHTML = `<div class="cx-tools" role="group" aria-label="Financial tools">${TOOLS.map(t => `<button type="button" class="cx-tool" data-tool="${t.id}" aria-pressed="${t.id === T.id}">${t.name}</button>`).join('')}</div>
      <h3 class="cx-ft">${T.title}</h3>${T.note ? `<p class="cx-note">${T.note}</p>` : ''}
      <div class="cx-fgrid">${T.fields.map(([k, l, d]) => `<label class="cx-fl" for="${fid(k)}"><span>${l}</span><input id="${fid(k)}" data-f="${k}" inputmode="decimal" autocomplete="off" placeholder="${d || ''}" value="${String(vals[k] == null ? '' : vals[k]).replace(/"/g, '&quot;')}"></label>`).join('')}</div>
      ${T.chips ? `<div class="cx-chips" role="group" aria-label="Common GST rates">${T.chips.map(c => `<button type="button" class="cx-chip" data-chip="${c}">${c}%</button>`).join('')}</div>` : ''}
      ${T.id === 'tvm' ? `<div class="cx-seg" role="group" aria-label="When payments happen"><button type="button" data-bgn="0" aria-pressed="${!S.fin.bgn}">END (end of period)</button><button type="button" data-bgn="1" aria-pressed="${!!S.fin.bgn}">BEGIN (start)</button></div>` : ''}
      ${T.cf ? `<div class="cx-cfs" role="group" aria-label="Cash flows">${S.fin.cf.map((c, j) => `<label class="cx-fl cx-cf" for="cxCF${j}"><span>CF${j}${j === 0 ? ' · today (money out is −)' : ` · year ${j}`}</span><input id="cxCF${j}" data-cf="${j}" inputmode="decimal" autocomplete="off" value="${String(c).replace(/"/g, '&quot;')}"></label>`).join('')}
        <div class="cx-cfb"><button type="button" class="cx-mini cx-mini2" id="cxCfAdd">+ Add year</button><button type="button" class="cx-mini cx-mini2" id="cxCfDel" ${S.fin.cf.length <= 2 ? 'disabled' : ''}>− Remove last</button></div></div>` : ''}
      <div class="cx-acts">${T.acts.map(([a, l]) => `<button type="button" class="cx-act" data-act="${a}">${l}</button>`).join('')}</div>
      <div class="cx-fout" id="cxFout" role="status" aria-live="polite"></div>`;
    box.querySelectorAll('.cx-tool').forEach(b => b.onclick = () => { S.fin.tool = b.dataset.tool; save(); renderFin(); emit({ type: 'tool', mode: 'fin', tool: S.fin.tool }); const f = box.querySelector('input'); if (f) f.focus(); });
    box.querySelectorAll('input[data-f]').forEach(inp => { inp.onfocus = () => { lastInput = inp; }; inp.oninput = () => { vals[inp.dataset.f] = inp.value; save(); }; });
    box.querySelectorAll('input[data-cf]').forEach(inp => { inp.onfocus = () => { lastInput = inp; }; inp.oninput = () => { S.fin.cf[+inp.dataset.cf] = inp.value; save(); }; });
    box.querySelectorAll('[data-chip]').forEach(b => b.onclick = () => { vals.R = b.dataset.chip; save(); const r = box.querySelector('input[data-f="R"]'); if (r) r.value = b.dataset.chip; });
    box.querySelectorAll('[data-bgn]').forEach(b => b.onclick = () => { S.fin.bgn = b.dataset.bgn === '1'; save(); box.querySelectorAll('[data-bgn]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); emit({ type: 'key', mode: 'fin', k: S.fin.bgn ? 'BGN' : 'END' }); });
    const add = box.querySelector('#cxCfAdd'); if (add) add.onclick = () => { if (S.fin.cf.length < 16) S.fin.cf.push(''); save(); renderFin(); const l = box.querySelector(`#cxCF${S.fin.cf.length - 1}`); if (l) l.focus(); };
    const del = box.querySelector('#cxCfDel'); if (del) del.onclick = () => { if (S.fin.cf.length > 2) S.fin.cf.pop(); save(); renderFin(); };
    box.querySelectorAll('.cx-act').forEach(b => b.onclick = () => finRun(T.id, b.dataset.act));
    applyHint();
  }
  function finRun(tool, act) {
    const out = panel && panel.querySelector('#cxFout');
    let r;
    try { r = finCompute(tool, act); }
    catch (e) { if (out) out.innerHTML = `<p class="cx-err">${e.message}</p>`; emit({ type: 'fin', mode: 'fin', tool, solve: act, value: NaN, error: e.message }); return null; }
    const shown = r.unit === '%' ? fmt2(r.value) + '%' : r.unit === '₹' ? '₹' + fmt2(r.value) : fmt2(r.value);
    if (r.fill) { const [k, v] = r.fill; const vals = S.fin.v[tool] = S.fin.v[tool] || {}; vals[k] = String(v); const inp = panel && panel.querySelector(`#cxFin input[data-f="${k}"]`); if (inp) inp.value = String(v); }
    print(r.tape); print(`= ${shown}`, 'res', +r.value.toFixed(6)); save();
    if (out) out.innerHTML = `<div class="cx-ans"><span>${r.label}</span><b>${shown}</b></div>${r.lines.map(l => `<p class="cx-line">${l}</p>`).join('')}
      ${r.table ? `<div class="cx-tblw" tabindex="0" role="region" aria-label="Depreciation schedule"><table class="cx-tbl"><thead><tr><th scope="col">Year</th><th scope="col">Opening</th><th scope="col">Dep.</th><th scope="col">Closing</th></tr></thead><tbody>${r.table.map(w => `<tr><td>${w[0]}</td><td>${fmt2(w[1])}</td><td>${fmt2(w[2])}</td><td>${fmt2(w[3])}</td></tr>`).join('')}</tbody></table></div>` : ''}
      <p class="cx-formula"><span aria-hidden="true">📐</span> ${r.formula}</p><p class="cx-copied">Copied to the roll 🧾</p>`;
    paint();
    emit({ type: 'fin', mode: 'fin', tool, solve: act, value: r.value });
    return r;
  }

  function applyHint() { if (!panel) return; panel.querySelectorAll('.cx-hl').forEach(x => x.classList.remove('cx-hl'));
    if (!hl.length) return;
    panel.querySelectorAll('[data-k],[data-mode],[data-tool],[data-act],[data-hl],[data-bgn]').forEach(el => {
      const box = el.closest('#cxBasic,#cxSci'); if (box && box.id !== (S.mode === 'sci' ? 'cxSci' : 'cxBasic')) return;
      const keys = [el.dataset.k, el.dataset.mode && 'mode:' + el.dataset.mode, el.dataset.tool && 'tool:' + el.dataset.tool, el.dataset.act && 'act:' + el.dataset.act, el.dataset.hl, el.dataset.bgn && (el.dataset.bgn === '1' ? 'BGN' : 'END')];
      if (keys.some(k => k && hl.includes(k))) el.classList.add('cx-hl'); }); }
  function paint(k) {
    if (!panel) return;
    panel.querySelectorAll('.cx-mode').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === S.mode)));
    panel.querySelector('#cxBasic').hidden = S.mode !== 'basic'; panel.querySelector('#cxSci').hidden = S.mode !== 'sci';
    const fin = panel.querySelector('#cxFin'); fin.hidden = S.mode !== 'fin'; if (S.mode === 'fin' && !fin.firstElementChild) renderFin();
    panel.querySelector('#cxGrp').textContent = S.grp === 'in' ? '1,00,000' : '100,000';
    if (S.mode === 'basic') {
      const shown = S.err ? 'Error' : S.fresh ? fmt(S.cur) : fmtEntry(S.cur);
      const n = panel.querySelector('#cxNum'); n.textContent = shown; n.classList.toggle('long', shown.length > 14);
      panel.querySelector('#cxM').classList.toggle('on', S.mem !== 0);
      panel.querySelector('#cxGT').classList.toggle('on', S.gt !== 0);
      panel.querySelector('#cxE').classList.toggle('on', !!S.err);
      panel.querySelector('#cxOp').textContent = S.op ? SYM[S.op] : '';
    } else if (S.mode === 'sci') {
      const X = S.sx, ex = panel.querySelector('#cxExpr'), n = panel.querySelector('#cxSNum');
      ex.textContent = exprText() || ' '; ex.scrollLeft = ex.scrollWidth;
      const shown = X.err || (X.done ? sciFmt(X.out) : X.toks.length ? '' : '0');
      n.textContent = shown; n.classList.toggle('long', shown.length > 14);
      const ang = panel.querySelector('#cxAng'); ang.textContent = X.angle === 'deg' ? 'DEG' : 'RAD'; ang.classList.add('on');
      panel.querySelector('#cxInv').classList.toggle('on', !!X.inv); panel.querySelector('#cxSE').classList.toggle('on', !!X.err);
      const ak = panel.querySelector('#cxSci [data-k="angle"]'); ak.textContent = X.angle === 'deg' ? 'DEG' : 'RAD'; ak.setAttribute('aria-label', `Angle unit: ${X.angle === 'deg' ? 'degrees' : 'radians'}. Tap to switch`);
      const ik = panel.querySelector('#cxSci [data-k="inv"]'); ik.setAttribute('aria-pressed', String(!!X.inv));
      ['sin', 'cos', 'tan'].forEach(f => { const b = panel.querySelector(`#cxSci [data-k="${f}"]`); b.innerHTML = X.inv ? `${f}<sup>−1</sup>` : f; b.setAttribute('aria-label', X.inv ? `Inverse ${SLABEL[f].toLowerCase()}` : SLABEL[f]); });
      const lg = panel.querySelector('#cxSci [data-k="log"]'), ln = panel.querySelector('#cxSci [data-k="ln"]');
      lg.innerHTML = X.inv ? '10<sup>x</sup>' : 'log'; lg.setAttribute('aria-label', X.inv ? '10 to the power x' : SLABEL.log);
      ln.innerHTML = X.inv ? 'e<sup>x</sup>' : 'ln'; ln.setAttribute('aria-label', X.inv ? 'e to the power x' : SLABEL.ln);
    }
    const t = panel.querySelector('#cxTape');
    if (!t.hidden) {
      t.innerHTML = (S.tape.length ? S.tape.map(l => l.c === 'res' ? `<button type="button" class="cx-tl res" data-v="${l.v != null ? l.v : l.t.replace(/[^\d.−-]/g, '').replace('−', '-')}">${l.t}</button>` : `<div class="cx-tl ${l.c}">${l.t}</div>`).join('') : '<div class="cx-tl sep">Your calculations will print here</div>')
        + (S.tape.length ? '<button type="button" class="cx-mini" id="cxTapeClr">Clear roll</button>' : '');
      t.scrollTop = t.scrollHeight;
    }
    applyHint();
  }
  function setMode(m) {
    if (!['basic', 'sci', 'fin'].includes(m)) return;
    const was = S.mode; S.mode = m; save();
    if (panel) { if (m === 'fin') renderFin(); paint(); }
    if (was !== m) emit({ type: 'mode', mode: m });
  }
  function open(o) {
    if (!panel) build();
    if (o && o.mode) setMode(o.mode);
    panel.hidden = false; S.open = true; fab.setAttribute('aria-expanded', 'true'); fab.classList.add('on'); paint();
    D.body.classList.add('cx-open');
    setTimeout(() => { const b = panel.querySelector(S.mode === 'sci' ? '#cxSci [data-k="="]' : '#cxBasic [data-k="="]'); if (b && D.activeElement === fab && S.mode !== 'fin') b.focus(); }, 30);
  }
  function close() { if (!panel) return; panel.hidden = true; S.open = false; fab.setAttribute('aria-expanded', 'false'); fab.classList.remove('on'); D.body.classList.remove('cx-open'); emit({ type: 'close' }); }
  function toggle() { panel && !panel.hidden ? close() : open(); }

  /* ---------- who sees the 🧮 button: OFF for school students, ON for CA — the Me / Profile switch overrides ---------- */
  function profile() { try { if (typeof ST !== 'undefined' && ST) return ST.profile; } catch (e) {} try { return JSON.parse(localStorage.getItem('sv_state') || '{}').profile; } catch (e) { return null; } }
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  function pref() { try { const v = localStorage.getItem(BTN_KEY); return v === '1' ? true : v === '0' ? false : null; } catch (e) { return null; } }
  function visible() { const p = profile(); if (!p || isParent()) return false; const v = pref(); return v == null ? p.course === 'ca' : v; }
  function sync() { if (!fab) return; const v = visible(); fab.hidden = !v; if (!profile() || isParent()) close(); }
  function setPref(on) { try { localStorage.setItem(BTN_KEY, on ? '1' : '0'); } catch (e) {} sync(); paintSet(); }

  /* the switch card on school Me and CA Profile (added above the sound / erase card) */
  function setCard() {
    const p = profile(); if (!p || isParent()) return;
    const ca = p.course === 'ca', host = D.getElementById(ca ? 's-ca' : 's-me'); if (!host) return;
    const anchorBtn = host.querySelector(ca ? '#caReset' : '#meReset'); if (!anchorBtn) return;
    const old = D.getElementById('cxSet'); if (old && host.contains(old)) return;
    if (old) old.remove();
    const anchor = anchorBtn.closest('.card'); if (!anchor) return;
    anchor.insertAdjacentHTML('beforebegin', `<div class="card cx-set" id="cxSet">${ca ? '<h2 class="ca-h2s">Calculator</h2>' : '<h3><span aria-hidden="true">🧮</span> Calculator</h3>'}
      <div class="srow"><span id="cxSetL">Show calculator button</span><button type="button" class="tgl" role="switch" id="cxSetT" aria-labelledby="cxSetL" aria-describedby="cxSetD"></button></div>
      <p class="sub" id="cxSetD"></p><button class="btn ghost" type="button" id="cxSetO">🧮 Open calculator</button></div>`);
    D.getElementById('cxSetT').onclick = () => { setPref(!visible()); try { sfx('tap'); } catch (e) {} };
    D.getElementById('cxSetO').onclick = () => open();
    paintSet();
  }
  function paintSet() {
    const t = D.getElementById('cxSetT'); if (!t) return; const on = visible();
    t.classList.toggle('on', on); t.setAttribute('aria-checked', String(on));
    const d = D.getElementById('cxSetD'); if (d) d.textContent = on ? 'The 🧮 button stays at the bottom-left of every screen. It has Basic, Scientific and Financial modes.' : 'The 🧮 button is hidden. You can still open the calculator here or from Calculator Academy.';
  }

  /* ---------- hooks for Calculator Academy ---------- */
  function coach(html) { if (!panel) build(); const c = panel.querySelector('#cxCoach'); c.classList.remove('cx-bad', 'cx-good'); if (!html) { c.hidden = true; c.innerHTML = ''; return c; } c.innerHTML = html; c.hidden = false; return c; }
  function hint(list) { hl = Array.isArray(list) ? list.slice() : []; applyHint(); }
  function reset() { S.cur = '0'; S.acc = null; S.op = null; S.fresh = true; S.mem = 0; S.gt = 0; S.lastOp = null; S.lastVal = null; S.err = false;
    Object.assign(S.sx, { toks: [], done: false, err: '', out: null, inv: false }); print('— new mission —', 'sep'); save(); paint(); }

  const CSS = `
#calcFab{position:fixed;left:12px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:960;width:44px;height:44px;border-radius:12px;border:1.5px solid #C9A76A;
 background:#15161C;color:#fff;font-size:22px;line-height:1;box-shadow:0 4px 14px rgba(0,0,0,.35);opacity:.8;cursor:pointer;display:flex;align-items:center;justify-content:center}
#calcFab:hover,#calcFab:focus-visible,#calcFab.on{opacity:1}#calcFab.on{background:#C9A76A}
#calcFab[hidden]{display:none}
#calcPanel{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom));z-index:970;width:min(360px,calc(100vw - 16px));
 font-family:Inter,system-ui,sans-serif;filter:drop-shadow(0 12px 28px rgba(0,0,0,.45));animation:cxIn .18s ease-out}
@keyframes cxIn{from{transform:translate(-50%,16px);opacity:0}to{transform:translate(-50%,0);opacity:1}}
@media (prefers-reduced-motion:reduce){#calcPanel{animation:none}}
.cx-body{background:linear-gradient(180deg,#2a2c35,#1b1c23);border-radius:18px;padding:8px 10px 12px;border:1px solid #3a3c47;box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
 max-height:calc(100vh - 92px - env(safe-area-inset-bottom));max-height:calc(100dvh - 92px - env(safe-area-inset-bottom));overflow-y:auto;overscroll-behavior:contain}
.cx-top{display:flex;align-items:center;gap:6px;margin:0 2px 6px}
.cx-brand{flex:1;min-width:0;color:#b9bcc8;font-size:11px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cx-brand b{color:#C9A76A}
.cx-mini{position:relative;background:#34363f;color:#e8e3d6;border:1px solid #4a4c57;border-radius:8px;font:600 11px Inter,system-ui,sans-serif;padding:6px 8px;min-height:32px;cursor:pointer;white-space:nowrap}
.cx-mini::after,.cx-close::after{content:'';position:absolute;left:50%;top:50%;width:max(100%,44px);height:max(100%,44px);transform:translate(-50%,-50%)}
.cx-mini[aria-pressed=true]{background:#C9A76A;color:#15161C}.cx-mini:disabled{opacity:.45;cursor:default}
.cx-close{position:relative;background:none;border:0;color:#e8e3d6;font-size:18px;width:36px;height:36px;cursor:pointer}
.cx-modes{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:0 2px 8px}
.cx-mode{min-height:44px;border-radius:10px;border:1px solid #4a4c57;background:#34363f;color:#e8e3d6;font:700 13px Inter,system-ui,sans-serif;cursor:pointer;padding:0 4px}
.cx-mode[aria-pressed=true]{background:#C9A76A;color:#15161C;border-color:#C9A76A}
.cx-coach{background:#fff7d6;color:#15161C;border:2px solid #ffd54a;border-radius:12px;padding:8px 10px;margin:0 2px 8px;font:600 13.5px/1.35 Nunito,Inter,system-ui,sans-serif}
.cx-coach b{font-weight:800}.cx-coach .cxc-top{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:#6b5a1e;font-weight:800;margin-bottom:2px}
.cx-coach .cxc-msg{margin-top:4px;font-weight:800;color:#5b4a00}.cx-coach.cx-bad .cxc-msg{color:#8a1c14}
.cxc-hint{position:relative;margin-top:6px;min-height:36px;padding:4px 12px;border-radius:999px;border:1.5px solid #e0b400;background:#fff;color:#15161C;font:700 13px Nunito,Inter,system-ui,sans-serif;cursor:pointer}
.cxc-hint::after{content:'';position:absolute;left:50%;top:50%;width:max(100%,44px);height:max(100%,44px);transform:translate(-50%,-50%)}
.cxc-hint:focus-visible{outline:3px solid #C9A76A;outline-offset:2px}
.cx-coach.cx-bad{border-color:#e57373;background:#fff1f0}.cx-coach.cx-good{border-color:#2E8B57;background:#eefaf2}
.cx-lcd{background:linear-gradient(180deg,#c9d3b6,#b7c3a1);border-radius:10px;padding:6px 10px 8px;box-shadow:inset 0 2px 6px rgba(0,0,0,.35);border:2px solid #0f1014}
.cx-ind{display:flex;gap:10px;height:14px;font:700 10px Inter,system-ui,sans-serif;color:rgba(30,36,22,.18)}.cx-ind .on{color:#1e2416}#cxOp{color:#1e2416;margin-left:auto;min-width:10px}
.cx-num{display:block;text-align:right;font:500 34px/1.15 "Courier New",ui-monospace,monospace;color:#1e2416;letter-spacing:.02em;white-space:nowrap;overflow:hidden;font-variant-numeric:tabular-nums}
.cx-num.long{font-size:24px;line-height:1.6}
.cx-expr{min-height:20px;text-align:right;font:600 15px/20px "Courier New",ui-monospace,monospace;color:#1e2416;white-space:nowrap;overflow-x:auto;scrollbar-width:none}
.cx-expr::-webkit-scrollbar{display:none}
.cx-snum{font-size:30px;min-height:35px}
.cx-keys{display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:44px;gap:7px;margin-top:10px}
.cx-skeys{gap:6px}
.cx-k{border:0;border-radius:10px;font:600 18px Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.18);transition:transform .05s,box-shadow .05s;touch-action:manipulation}
.cx-k:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(0,0,0,.45)}
.cx-k.kn{background:#f2efe7;color:#15161C}.cx-k.kf{background:#4a4d59;color:#f2efe7;font-size:14px}.cx-k.ko{background:#C9A76A;color:#15161C;font-size:22px}
.cx-k.kc{background:#B71C2C;color:#fff;font-size:15px}.cx-k.ke{background:#2E8B57;color:#fff;font-size:24px}
.cx-k[aria-pressed=true]{background:#C9A76A;color:#15161C}.cx-k sup{font-size:9px}
.cx-k.kt{grid-row:span 2}
.cx-keys .cx-k[data-k="0"]{grid-column:1}
.cx-k:focus-visible,.cx-mini:focus-visible,.cx-close:focus-visible,.cx-mode:focus-visible,.cx-tool:focus-visible,.cx-act:focus-visible,.cx-chip:focus-visible,.cx-seg button:focus-visible{outline:3px solid #C9A76A;outline-offset:2px}
.cx-hl{outline:3px solid #ffd54a!important;outline-offset:2px;animation:cxPulse 1s ease-in-out infinite}
@keyframes cxPulse{50%{outline-color:#ff8f00;box-shadow:0 0 0 6px rgba(255,213,74,.35)}}
@media (prefers-reduced-motion:reduce){.cx-hl{animation:none}}
.cx-tape{background:#fffdf6;border-radius:8px;max-height:140px;overflow:auto;margin:0 2px 8px;padding:6px 10px;font:14px "Courier New",ui-monospace,monospace;color:#2b2b2b;
 background-image:repeating-linear-gradient(#fffdf6 0 21px,#efe9d8 21px 22px);box-shadow:inset 0 -6px 8px -6px rgba(0,0,0,.2)}
.cx-tl{text-align:right;line-height:22px;white-space:nowrap}.cx-tl.res{display:block;width:100%;background:none;border:0;font:700 14px "Courier New",monospace;color:#5B0F1B;text-align:right;cursor:pointer;line-height:22px;border-bottom:1px dashed #C9A76A}
.cx-tl.sep{color:#999;text-align:center}.cx-tl.mem{color:#2A7F8F}.cx-tl.err{color:#B71C2C}
.cx-tape .cx-mini{display:block;margin:6px 0 2px auto;background:#efe9d8;color:#5B0F1B;border-color:#d9cfb5}
.cx-fin{background:#f7f3ea;border-radius:12px;padding:8px 10px 10px;color:#15161C;font:14px Nunito,Inter,system-ui,sans-serif}
.cx-tools{display:flex;gap:6px;overflow-x:auto;padding:2px 2px 6px;scrollbar-width:thin}
.cx-tool{flex:none;min-height:44px;padding:0 12px;border-radius:999px;border:1.5px solid #d9cfb5;background:#fff;color:#15161C;font:700 13px Inter,system-ui,sans-serif;cursor:pointer}
.cx-tool[aria-pressed=true]{background:#15161C;color:#F4EAD8;border-color:#15161C}
.cx-ft{margin:6px 0 2px;font:800 15px Inter,system-ui,sans-serif}.cx-note{margin:0 0 4px;font-size:12.5px;color:#5B0F1B}
.cx-fgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 8px}
.cx-fl{display:flex;flex-direction:column;justify-content:flex-end;gap:3px;margin:5px 0;font:600 12px/1.25 Inter,system-ui,sans-serif;color:#3b3d46}
.cx-fl input{min-height:44px;width:100%;box-sizing:border-box;border:1.5px solid #d9cfb5;border-radius:10px;padding:0 10px;font:600 16px Inter,system-ui,sans-serif;background:#fff;color:#15161C}
.cx-fl input:focus{outline:3px solid #C9A76A;outline-offset:1px;border-color:#8A6A2E}
.cx-cfs{display:grid;grid-template-columns:1fr 1fr;gap:0 8px}.cx-cfb{grid-column:1/-1;display:flex;gap:8px;margin:2px 0 4px}
.cx-mini2{background:#fff;color:#15161C;border-color:#d9cfb5;min-height:40px;font-size:12.5px}
.cx-chips{display:flex;gap:6px;margin:2px 0 4px}.cx-chip{flex:1;min-height:44px;border-radius:10px;border:1.5px solid #d9cfb5;background:#fff;font:700 14px Inter,system-ui,sans-serif;cursor:pointer;color:#15161C}
.cx-seg{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:4px 0}.cx-seg button{min-height:44px;border-radius:10px;border:1.5px solid #d9cfb5;background:#fff;font:700 12.5px Inter,system-ui,sans-serif;color:#15161C;cursor:pointer}
.cx-seg button[aria-pressed=true]{background:#15161C;color:#F4EAD8;border-color:#15161C}
.cx-acts{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.cx-act{flex:1 1 30%;min-height:44px;border:0;border-radius:10px;background:#2E8B57;color:#fff;font:700 13px Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 0 rgba(0,0,0,.25);padding:4px 6px}
.cx-ans{display:flex;justify-content:space-between;align-items:baseline;gap:8px;background:linear-gradient(180deg,#c9d3b6,#b7c3a1);border:2px solid #0f1014;border-radius:10px;padding:8px 10px;margin-top:10px;color:#1e2416}
.cx-ans span{font:700 12.5px Inter,system-ui,sans-serif}.cx-ans b{font:700 22px "Courier New",ui-monospace,monospace;word-break:break-all;text-align:right}
.cx-line{margin:5px 0 0;font:600 13px Inter,system-ui,sans-serif}.cx-formula{margin:6px 0 0;font:600 12.5px/1.35 Inter,system-ui,sans-serif;color:#5B0F1B}
.cx-copied{margin:4px 0 0;font:600 11.5px Inter,system-ui,sans-serif;color:#6b6f7a}.cx-err{color:#B71C2C;font:700 13px Inter,system-ui,sans-serif;margin:8px 0 0}
.cx-tblw{overflow-x:auto;margin-top:6px}.cx-tbl{width:100%;border-collapse:collapse;font:600 12px Inter,system-ui,sans-serif}.cx-tbl th,.cx-tbl td{padding:4px 5px;text-align:right;border-bottom:1px solid #e2d6bd}.cx-tbl th:first-child,.cx-tbl td:first-child{text-align:left}
.cx-set .srow{border-bottom:0;padding-top:4px}
@media (forced-colors:active){.cx-k,.cx-lcd,.cx-body,.cx-mode,.cx-tool,.cx-act{border:1px solid CanvasText}.cx-hl{outline:3px solid Highlight!important}}`;

  function init() {
    build(); paint(); sync(); setInterval(sync, 1500); D.addEventListener('visibilitychange', sync);
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; setCard(); }); }).observe(D.body, { childList: true, subtree: true });
    setCard();
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', init) : init();
  window.Calc = { open, close, toggle, setMode, isOpen: () => !!(panel && !panel.hidden), visible, setPref,
    on: f => { subs.add(f); return () => subs.delete(f); }, coach, hint, reset, finRun,
    state: () => ({ mode: S.mode, value: S.mode === 'sci' ? S.sx.out : (S.err ? NaN : +S.cur), mem: S.mem, gt: S.gt, angle: S.sx.angle, tool: S.fin.tool, bgn: S.fin.bgn, expr: exprText(), done: S.sx.done }),
    math: { sci: sciRun, sciFmt, fmt, fmt2, ...FINM },
    _press: press, _sciPress: sciPress, _state: () => S, _fmt: fmt };
})();
