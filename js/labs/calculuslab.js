/* StudyVerse Concept Lab: calculuslab — limits, derivatives, integrals and maxima/minima on a live graph.
 * (Grades 11–12, NCERT notation; log x means the natural logarithm.)
 *
 * The child drags a point on the curve (or the limits a, b of an integral) and taps / slides controls;
 * slopes, tables, Riemann sums and exact values update instantly.
 *
 * mode 'tangent' : drag point P(a, f(a)); the tangent line and f′(a) are shown, plus the secant PQ with
 *                  Q at a + h. Slide h (or tap "h → 0") to watch the secant slope approach f′(a).
 *                  Tangent equation y = mx + c is shown.
 * mode 'area'    : drag the limits a and b; n Riemann rectangles (left / right / mid / trapezium) are
 *                  drawn; tap "n → ∞" to watch Sₙ converge to the definite integral (exact value shown,
 *                  as a fraction / multiple of π when it is one, and F(b) − F(a) if F is given).
 * mode 'limit'   : tap "from left" / "from right" (or drag) to bring x towards a; a table of x and f(x)
 *                  fills on each side; then pick the value of the limit (or "does not exist").
 * mode 'maxmin'  : drag the point along the curve; f(x), f′(x), f″(x) are shown; the point "clicks" onto
 *                  critical points (f′ = 0); find the local / absolute maximum or minimum.
 *
 * Expressions: a tiny safe parser (no eval). Allowed: numbers, x, pi (π), e, + − * / ^, brackets,
 * implicit multiplication (2x, 3(x+1), x sin x), functions sin cos tan sec cosec/csc cot asin acos atan
 * exp log/ln sqrt abs, and sin^2(x) style powers. Write sin(2x) with brackets.
 *
 * PARAMS (all optional)
 *   mode       'tangent' | 'area' | 'limit' | 'maxmin'                               default 'tangent'
 *   fn         string   f(x)                      default per mode: 'x^3 - 3x' | 'x^2' | '(x^2 - 4)/(x - 2)' |
 *                                                                   'x^3 - 6x^2 + 9x + 1'
 *   fnLeft, fnRight  string  (limit) piecewise f: fnLeft for x < a, fnRight for x ≥ a      default none
 *   valueAt    number   (limit) f(a) defined separately (removable discontinuity)          default none
 *   xRange     [min,max] x-axis window                     default per mode ([-2.5,2.5] | [-1,3] | [-1,5] | [-0.5,4.5])
 *   yRange     [min,max] y-axis window                     default auto from the curve
 *   fname      string   name of the function, e.g. 'V' or 'P'                          default 'f'
 *   xLabel, yLabel string axis captions (may be Hindi)                                default '' (none)
 *   a          number   tangent: start point / area: lower limit / limit: the point a    default per mode
 *   b          number   area: upper limit                                                default per mode
 *   h          number   tangent: starting h of the secant                                default ¼ of the x-window
 *   secant     boolean  tangent: show the secant and h controls                          default true
 *   n          number   area: starting number of strips (1–200)                          default 4
 *   method     'left' | 'right' | 'mid' | 'trap'   area: starting rule                    default 'left'
 *   F          string   area: an antiderivative, shown as F(b) − F(a) (ignored if wrong)  default none
 *   step       number   snap step for dragging a, b (area)                               default auto (nice ≈ window/50)
 *   interval   [a,b]    maxmin: closed interval for absolute max/min                     default xRange
 * Challenge (one target; if none is given a sensible one is generated for the mode):
 *   target     tangent: {slope:m}  — put P where f′(a) = m
 *              area:    {area:v} — drag the limits so ∫ₐᵇ f dx = v;  {error:e} — get |Sₙ − ∫| < e
 *              limit:   {} — find the limit (always: explore both sides, then choose the value)
 *              maxmin:  {find:'max'|'min'|'absmax'|'absmin'}
 *   challenge  string   challenge sentence (may be Hindi); else generated
 *   winText    string   optional win message
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const minus = s => String(s).replace(/-/g, '−');
  function fmt(v, dp = 4) {
    if (v === Infinity) return '∞'; if (v === -Infinity) return '−∞';
    if (!isFinite(v)) return 'undefined';
    if (Math.abs(v) >= 1e6 || (Math.abs(v) < 1e-4 && v !== 0 && dp > 4)) return minus(v.toExponential(2));
    let s = (+v.toFixed(dp)).toString(); if (s === '-0') s = '0';
    return minus(s);
  }
  // recognise simple exact values: integers, fractions, rational multiples of π
  function exactStr(v) {
    if (!isFinite(v)) return null;
    const tol = n => 1e-7 * Math.max(1, Math.abs(n));
    for (let d = 1; d <= 24; d++) { const n = v * d; if (Math.abs(n - Math.round(n)) < tol(n)) { const N = Math.round(n); if (N === 0) return '0'; return minus(d === 1 ? String(N) : N + '/' + d); } }
    const w = v / Math.PI;
    for (let d = 1; d <= 12; d++) { const n = w * d; if (Math.abs(n - Math.round(n)) < tol(n) && Math.round(n) !== 0) { const N = Math.round(n); const top = (N === 1 ? '' : N === -1 ? '-' : N) + 'π'; return minus(d === 1 ? top : top + '/' + d); } }
    return null;
  }
  const show = v => { const e = exactStr(v); return e && e.length <= 7 && e !== fmt(v) ? `${e} ≈ ${fmt(v)}` : fmt(v); };

  // ---------------- tiny safe expression parser ----------------
  const FNS = ['cosec', 'asin', 'acos', 'atan', 'sqrt', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'exp', 'log', 'abs', 'ln'];
  const NAMES = FNS.concat(['pi', 'x', 'e']).sort((a, b) => b.length - a.length);
  const ALIAS = { ln: 'log', cosec: 'csc' };
  function tokenize(src) {
    const s = String(src).replace(/\s+/g, ' ').replace(/[−–]/g, '-').replace(/[×·]/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi')
      .replace(/²/g, '^2').replace(/³/g, '^3').replace(/√/g, 'sqrt').toLowerCase();
    const out = []; let i = 0;
    while (i < s.length) {
      const c = s[i];
      if (c === ' ') { i++; continue; }
      if (/[0-9.]/.test(c)) {
        const m = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/.exec(s.slice(i));
        if (!m) throw new Error('bad number');
        out.push({ k: 'n', v: parseFloat(m[0]) }); i += m[0].length; continue;
      }
      if (/[a-z]/.test(c)) {
        const rest = s.slice(i); const hit = NAMES.find(n => rest.startsWith(n));
        if (!hit) throw new Error('unknown name at ' + rest.slice(0, 6));
        out.push(FNS.includes(hit) ? { k: 'f', v: ALIAS[hit] || hit } : { k: 'id', v: hit }); i += hit.length; continue;
      }
      if ('+-*/^()'.includes(c)) { out.push({ k: c }); i++; continue; }
      throw new Error('bad character ' + c);
    }
    return out;
  }
  const N = v => ({ t: 'n', v });
  function parse(src) {
    const T = tokenize(src); let i = 0;
    const pk = () => T[i], nx = () => T[i++];
    const want = k => { const t = nx(); if (!t || t.k !== k) throw new Error('expected ' + k); };
    function expr() { let a = term(); while (pk() && (pk().k === '+' || pk().k === '-')) { const op = nx().k; a = { t: op, a, b: term() }; } return a; }
    function term() {
      let a = unary();
      for (;;) {
        const t = pk(); if (!t) break;
        if (t.k === '*' || t.k === '/') { nx(); a = { t: t.k, a, b: unary() }; }
        else if (t.k === 'n' || t.k === 'id' || t.k === 'f' || t.k === '(') a = { t: '*', a, b: power() };
        else break;
      }
      return a;
    }
    function unary() { const t = pk(); if (t && t.k === '-') { nx(); return { t: 'neg', a: unary() }; } if (t && t.k === '+') { nx(); return unary(); } return power(); }
    function power() { const b = primary(); if (pk() && pk().k === '^') { nx(); return { t: '^', a: b, b: unary() }; } return b; }
    function primary() {
      const t = nx(); if (!t) throw new Error('unexpected end');
      if (t.k === 'n') return N(t.v);
      if (t.k === 'id') return t.v === 'x' ? { t: 'x' } : N(t.v === 'pi' ? Math.PI : Math.E);
      if (t.k === '(') { const e = expr(); want(')'); return e; }
      if (t.k === 'f') {
        let pw = null;
        if (pk() && pk().k === '^') { nx(); pw = primary(); }
        let arg;
        if (pk() && pk().k === '(') { nx(); arg = expr(); want(')'); }
        else { arg = power(); while (pk() && (pk().k === 'n' || pk().k === 'id')) arg = { t: '*', a: arg, b: power() }; }
        const node = { t: 'f', f: t.v, a: arg };
        return pw ? { t: '^', a: node, b: pw } : node;
      }
      throw new Error('unexpected ' + t.k);
    }
    const tree = expr(); if (i < T.length) throw new Error('unexpected ' + T[i].k);
    return tree;
  }
  function rpow(a, b) {
    if (a < 0 && !Number.isInteger(b)) {
      for (let q = 3; q <= 9; q += 2) { const p = b * q; if (Math.abs(p - Math.round(p)) < 1e-9) { const r = Math.pow(-a, b); return Math.round(p) % 2 ? -r : r; } }
      return NaN;
    }
    return Math.pow(a, b);
  }
  const FEV = { sin: Math.sin, cos: Math.cos, tan: Math.tan, sec: v => 1 / Math.cos(v), csc: v => 1 / Math.sin(v), cot: v => Math.cos(v) / Math.sin(v), asin: Math.asin, acos: Math.acos, atan: Math.atan, exp: Math.exp, log: v => v > 0 ? Math.log(v) : NaN, sqrt: v => v >= 0 ? Math.sqrt(v) : NaN, abs: Math.abs };
  function ev(n, x) {
    switch (n.t) {
      case 'n': return n.v; case 'x': return x;
      case '+': return ev(n.a, x) + ev(n.b, x); case '-': return ev(n.a, x) - ev(n.b, x);
      case '*': return ev(n.a, x) * ev(n.b, x); case '/': return ev(n.a, x) / ev(n.b, x);
      case '^': return rpow(ev(n.a, x), ev(n.b, x)); case 'neg': return -ev(n.a, x);
      case 'f': return FEV[n.f](ev(n.a, x));
    }
    return NaN;
  }
  const hasX = n => n.t === 'x' || (n.a && hasX(n.a)) || (n.b && hasX(n.b));
  const isN = (n, v) => n.t === 'n' && (v === undefined || n.v === v);
  const add = (a, b) => isN(a, 0) ? b : isN(b, 0) ? a : isN(a) && isN(b) ? N(a.v + b.v) : { t: '+', a, b };
  const neg = a => isN(a) ? N(-a.v) : a.t === 'neg' ? a.a : { t: 'neg', a };
  const sub = (a, b) => isN(b, 0) ? a : isN(a, 0) ? neg(b) : isN(a) && isN(b) ? N(a.v - b.v) : { t: '-', a, b };
  const mul = (a, b) => isN(a, 0) || isN(b, 0) ? N(0) : isN(a, 1) ? b : isN(b, 1) ? a : isN(a) && isN(b) ? N(a.v * b.v) : { t: '*', a, b };
  const div = (a, b) => isN(a, 0) ? N(0) : isN(b, 1) ? a : { t: '/', a, b };
  const pow = (a, b) => isN(b, 0) ? N(1) : isN(b, 1) ? a : { t: '^', a, b };
  const F = (f, a) => ({ t: 'f', f, a });
  function d(n) {
    switch (n.t) {
      case 'n': return N(0); case 'x': return N(1);
      case '+': return add(d(n.a), d(n.b)); case '-': return sub(d(n.a), d(n.b)); case 'neg': return neg(d(n.a));
      case '*': return add(mul(d(n.a), n.b), mul(n.a, d(n.b)));
      case '/': return div(sub(mul(d(n.a), n.b), mul(n.a, d(n.b))), pow(n.b, N(2)));
      case '^':
        if (!hasX(n.b)) return mul(mul(n.b, pow(n.a, sub(n.b, N(1)))), d(n.a));
        if (!hasX(n.a)) return mul(mul(n, F('log', n.a)), d(n.b));
        return mul(n, add(mul(d(n.b), F('log', n.a)), div(mul(n.b, d(n.a)), n.a)));
      case 'f': {
        const g = n.a, dg = d(g);
        if (isN(dg, 0)) return N(0);
        switch (n.f) {
          case 'sin': return mul(F('cos', g), dg);
          case 'cos': return neg(mul(F('sin', g), dg));
          case 'tan': return div(dg, pow(F('cos', g), N(2)));
          case 'sec': return mul(mul(F('sec', g), F('tan', g)), dg);
          case 'csc': return neg(mul(mul(F('csc', g), F('cot', g)), dg));
          case 'cot': return neg(div(dg, pow(F('sin', g), N(2))));
          case 'exp': return mul(F('exp', g), dg);
          case 'log': return div(dg, g);
          case 'sqrt': return div(dg, mul(N(2), F('sqrt', g)));
          case 'abs': return mul(div(g, F('abs', g)), dg);
          case 'asin': return div(dg, F('sqrt', sub(N(1), pow(g, N(2)))));
          case 'acos': return neg(div(dg, F('sqrt', sub(N(1), pow(g, N(2))))));
          case 'atan': return div(dg, add(N(1), pow(g, N(2))));
        }
      }
    }
    return N(NaN);
  }
  function compile(src) { const t = parse(src); const t1 = d(t), t2 = d(t1); return { f: x => ev(t, x), d1: x => ev(t1, x), d2: x => ev(t2, x) }; }
  function tryCompile(src) { try { const c = compile(src); return c; } catch (e) { return null; } }
  // pretty-print an expression string for display
  function pretty(s) {
    return minus(String(s).replace(/\s*\*\s*/g, '·').replace(/\bsqrt\b/g, '√').replace(/\bpi\b/g, 'π').replace(/\^\(?2\)?(?![\d.])/g, '²').replace(/\^\(?3\)?(?![\d.])/g, '³')
      .replace(/\s*([+\-/])\s*/g, ' $1 ').replace(/\(\s*-\s*/g, '(-').replace(/^\s*-\s*/, '-').replace(/\s+/g, ' ').trim());
  }
  // adaptive Simpson integration
  function integrate(f, a, b) {
    if (a === b) return 0;
    const simp = (a, b, fa, fm, fb) => (b - a) / 6 * (fa + 4 * fm + fb);
    function rec(a, b, fa, fm, fb, whole, eps, depth) {
      const m = (a + b) / 2, lm = (a + m) / 2, rm = (m + b) / 2, flm = f(lm), frm = f(rm);
      const left = simp(a, m, fa, flm, fm), right = simp(m, b, fm, frm, fb);
      if (depth <= 0 || Math.abs(left + right - whole) <= 15 * eps) return left + right + (left + right - whole) / 15;
      return rec(a, m, fa, flm, fm, left, eps / 2, depth - 1) + rec(m, b, fm, frm, fb, right, eps / 2, depth - 1);
    }
    const fa = f(a), fb = f(b), fm = f((a + b) / 2);
    return rec(a, b, fa, fm, fb, simp(a, b, fa, fm, fb), 1e-11, 40);
  }
  function niceStep(span, target) { const raw = span / target, p10 = Math.pow(10, Math.floor(Math.log10(raw))); const m = raw / p10; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p10; }
  const snapTo = (v, s) => Math.round(v / s) * s;
  const clean = v => +v.toFixed(10);
  function newton(g, x, lo, hi) { // root of g near x (numerical derivative)
    for (let k = 0; k < 40; k++) {
      const gx = g(x), h = 1e-6 * Math.max(1, Math.abs(x)), dg = (g(x + h) - g(x - h)) / (2 * h);
      if (!isFinite(gx) || !isFinite(dg) || dg === 0) return null;
      const nx = x - gx / dg; if (nx < lo - 1e-9 || nx > hi + 1e-9) return null;
      if (Math.abs(nx - x) < 1e-12) return nx; x = nx;
    }
    return Math.abs(g(x)) < 1e-8 ? x : null;
  }
  function roots(g, lo, hi, steps = 600) { // all sign-change roots of g on [lo,hi]
    const out = []; let px = lo, pg = g(lo);
    for (let i = 1; i <= steps; i++) {
      const x = lo + (hi - lo) * i / steps, gx = g(x);
      if (isFinite(pg) && isFinite(gx)) {
        if (pg === 0) out.push(px);
        else if (pg * gx < 0 && Math.abs(pg - gx) < 1e6) { let a = px, b = x, ga = pg; for (let k = 0; k < 60; k++) { const m = (a + b) / 2, gm = g(m); if (ga * gm <= 0) b = m; else { a = m; ga = gm; } } out.push((a + b) / 2); }
      }
      px = x; pg = gx;
    }
    if (pg === 0) out.push(hi);
    return out.filter((r, i) => i === 0 || Math.abs(r - out[i - 1]) > 1e-7);
  }

  const DEF = {
    tangent: { fn: 'x^3 - 3x', xRange: [-2.5, 2.5], a: 0.5 },
    area: { fn: 'x^2', xRange: [-1, 3], a: 0, b: 2 },
    limit: { fn: '(x^2 - 4)/(x - 2)', xRange: [-1, 5], a: 2 },
    maxmin: { fn: 'x^3 - 6x^2 + 9x + 1', xRange: [-0.5, 4.5] }
  };

  Labs.register('calculuslab', {
    title: 'Calculus lab',
    subjects: ['maths'],
    _expr: { parse, compile, exactStr, integrate, pretty, roots },
    render(host, p, api) {
      const mode = ['tangent', 'area', 'limit', 'maxmin'].includes(p.mode) ? p.mode : 'tangent';
      const D = DEF[mode];
      const ownFn = typeof p.fn === 'string' && tryCompile(p.fn);
      let fnStr = ownFn ? p.fn : D.fn;
      let pieces = null;
      if (mode === 'limit' && typeof p.fnLeft === 'string' && typeof p.fnRight === 'string') {
        const L = tryCompile(p.fnLeft), R = tryCompile(p.fnRight); if (L && R) pieces = { L, R };
      }
      const own = !!ownFn || !!pieces; // the topic supplied its own function → do not reuse default numbers
      let xr = Array.isArray(p.xRange) && p.xRange.length === 2 && +p.xRange[0] < +p.xRange[1] ? p.xRange.map(Number) : (own ? [-5, 5] : D.xRange);
      const [X0, X1] = xr, SPAN = X1 - X0;
      const fname = esc(p.fname || 'f'), xl = p.xLabel ? esc(p.xLabel) : '', yl = p.yLabel ? esc(p.yLabel) : '';
      const C = pieces ? null : compile(fnStr);
      const lim0 = isFinite(+p.a) ? +p.a : (own ? (X0 + X1) / 2 : D.a);
      const f = pieces ? (x => x < lim0 ? pieces.L.f(x) : pieces.R.f(x)) : C.f;
      const f1 = pieces ? (x => x < lim0 ? pieces.L.d1(x) : pieces.R.d1(x)) : C.d1;
      const f2 = pieces ? (x => x < lim0 ? pieces.L.d2(x) : pieces.R.d2(x)) : C.d2;
      const fnShow = pieces ? '' : pretty(fnStr);
      let won = false, touched = false, raf = 0;
      const timers = [];
      const W = 360, H = mode === 'limit' ? 196 : mode === 'area' ? 206 : 214;
      const PL = 6, PR = W - 6, PT = 6, PB = H - 6;
      // y-range
      let yr;
      if (Array.isArray(p.yRange) && p.yRange.length === 2 && +p.yRange[0] < +p.yRange[1]) yr = p.yRange.map(Number);
      else {
        const vals = []; for (let i = 0; i <= 300; i++) { const v = f(X0 + SPAN * i / 300); if (isFinite(v)) vals.push(v); }
        if (mode === 'limit' && isFinite(+p.valueAt)) for (let i = 0; i < 12; i++) vals.push(+p.valueAt);
        vals.sort((a, b) => a - b);
        let lo = vals.length ? vals[Math.floor(vals.length * 0.02)] : -1, hi = vals.length ? vals[Math.ceil(vals.length * 0.98) - 1] : 1;
        if (mode === 'area' || mode === 'limit' || lo > 0 && lo < (hi - lo) * 0.6) lo = Math.min(lo, 0);
        if (hi < 0 && -hi < (hi - lo) * 0.6) hi = Math.max(hi, 0);
        if (hi - lo < 1e-6) { lo -= 1; hi += 1; }
        const pad = (hi - lo) * 0.12; yr = [lo - pad, hi + pad];
      }
      const [Y0, Y1] = yr;
      const X = x => PL + (x - X0) / SPAN * (PR - PL), Y = y => PB - (y - Y0) / (Y1 - Y0) * (PB - PT);
      const iX = px => X0 + (px - PL) / (PR - PL) * SPAN;
      const uid = 'lbcl' + Math.random().toString(36).slice(2, 8);

      const css = `
.lb-calculuslab-w{font-size:13.5px;color:#1b1f3a}
.lb-calculuslab-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.3}
.lb-calculuslab-fx{font-weight:800;font-size:13px;color:#5b33c9;margin:-1px 0 4px}
.lb-calculuslab-svg{width:100%;height:auto;display:block;background:#fbfbff;border:1.5px solid #e6e8f7;border-radius:16px;touch-action:none;user-select:none;-webkit-user-select:none;box-sizing:border-box}
.lb-calculuslab-chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.lb-calculuslab-chip{flex:1 1 auto;border-radius:10px;padding:3px 7px;font-weight:800;font-size:12.5px;text-align:center;background:#f1f2fb;white-space:nowrap}
.lb-calculuslab-chip b{font-size:14px}
.lb-calculuslab-row{display:flex;gap:5px;margin-top:5px;align-items:center}
.lb-calculuslab-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 6px}
.lb-calculuslab-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-calculuslab-b.go{background:#2ed3a5;color:#08372a;box-shadow:0 3px 0 #1ea383}
.lb-calculuslab-b:active{transform:translateY(2px)}
.lb-calculuslab-b:disabled{opacity:.45}
.lb-calculuslab-sl{display:flex;align-items:center;gap:7px;margin-top:3px;font-weight:800;font-size:13px}
.lb-calculuslab-sl span{min-width:58px}
.lb-calculuslab-sl input{flex:1;min-width:0;-webkit-appearance:none;appearance:none;height:34px;background:transparent;cursor:pointer}
.lb-calculuslab-sl input::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-calculuslab-sl input::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#8b5cf6;margin-top:-9px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.lb-calculuslab-sl input::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-calculuslab-sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#8b5cf6;border:3px solid #fff}
.lb-calculuslab-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px;text-align:center;line-height:1.3}
.lb-calculuslab-tabs{display:flex;gap:6px;margin-top:5px}
.lb-calculuslab-tab{flex:1;background:#f6f4ff;border-radius:12px;padding:3px 6px;font-size:12px;font-weight:700;font-variant-numeric:tabular-nums}
.lb-calculuslab-tab table{width:100%;border-collapse:collapse}
.lb-calculuslab-tab th{font-size:11.5px;color:#6b7090;text-align:left;font-weight:800}
.lb-calculuslab-tab td{padding:1px 0;white-space:nowrap}
.lb-calculuslab-tab td+td,.lb-calculuslab-tab th+th{text-align:right}`;

      // ---------- static graph: grid, axes, curve ----------
      function gridSvg() {
        let g = '';
        const sx = niceStep(SPAN, 8), sy = niceStep(Y1 - Y0, 6);
        const ax = Math.min(PB, Math.max(PT, Y(0))), ay = Math.min(PR, Math.max(PL, X(0)));
        for (let v = Math.ceil(X0 / sx) * sx; v <= X1 + 1e-9; v += sx) { const px = X(v); g += `<line x1="${px}" y1="${PT}" x2="${px}" y2="${PB}" stroke="#eceefa"/>`; if (Math.abs(v) > 1e-9 && px > PL + 10 && px < PR - (xl ? 34 : 14)) g += `<text x="${px}" y="${ax > PB - 14 ? ax - 4 : ax + 12}" font-size="9.5" font-weight="700" fill="#8a8fae" text-anchor="middle">${fmt(clean(v), 3)}</text>`; }
        for (let v = Math.ceil(Y0 / sy) * sy; v <= Y1 + 1e-9; v += sy) { const py = Y(v); g += `<line x1="${PL}" y1="${py}" x2="${PR}" y2="${py}" stroke="#eceefa"/>`; if (Math.abs(v) > 1e-9 && py > PT + 18 && py < PB - 4) g += `<text x="${ay < PL + 24 ? ay + 4 : ay - 4}" y="${py + 3.5}" font-size="9.5" font-weight="700" fill="#8a8fae" text-anchor="${ay < PL + 24 ? 'start' : 'end'}">${fmt(clean(v), 3)}</text>`; }
        g += `<line x1="${PL}" y1="${ax}" x2="${PR}" y2="${ax}" stroke="#1b1f3a" stroke-width="1.3"/><line x1="${ay}" y1="${PT}" x2="${ay}" y2="${PB}" stroke="#1b1f3a" stroke-width="1.3"/>`;
        g += `<text x="${PR - 3}" y="${ax - 5}" font-size="11" font-weight="800" fill="#1b1f3a" text-anchor="end">${xl || 'x'}</text>`;
        g += `<text x="${ay + 5}" y="${PT + 11}" font-size="11" font-weight="800" fill="#1b1f3a">${yl || 'y'}</text>`;
        return g;
      }
      function pathOf(fun, lo, hi, n = 360) {
        let d = '', pen = false, py = 0;
        for (let i = 0; i <= n; i++) {
          const x = lo + (hi - lo) * i / n, y = fun(x);
          if (!isFinite(y)) { pen = false; continue; }
          const sy = Y(y), cy = Math.max(PT - 400, Math.min(PB + 400, sy));
          if (pen && Math.abs(sy - py) > (PB - PT) * 2.5) pen = false; // asymptote
          d += (pen ? 'L' : 'M') + X(x).toFixed(1) + ' ' + cy.toFixed(1); pen = true; py = sy;
        }
        return d;
      }
      function curveSvg() {
        if (pieces) {
          const eps = SPAN * 1e-6;
          return `<path d="${pathOf(pieces.L.f, X0, lim0 - eps, 200)}" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/><path d="${pathOf(pieces.R.f, lim0, X1, 200)}" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>`;
        }
        return `<path d="${pathOf(f, X0, X1)}" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>`;
      }
      function shell(controls, extraTop = '') {
        host.innerHTML = `<style>${css}</style><div class="lb-calculuslab-w">
<div class="lb-calculuslab-ch">🎯 Challenge: <span class="lb-calculuslab-cht"></span></div>
${fnShow ? `<div class="lb-calculuslab-fx">${fname}(x) = ${esc(fnShow)}</div>` : extraTop}
<svg class="lb-calculuslab-svg" viewBox="0 0 ${W} ${H}"><defs><clipPath id="${uid}"><rect x="${PL}" y="${PT}" width="${PR - PL}" height="${PB - PT}"/></clipPath></defs>
<g>${gridSvg()}</g><g class="lb-calculuslab-under" clip-path="url(#${uid})"></g><g clip-path="url(#${uid})">${curveSvg()}</g><g class="lb-calculuslab-dyn" clip-path="url(#${uid})"></g><g class="lb-calculuslab-top"></g></svg>
${controls}<div class="lb-calculuslab-msg"></div></div>`;
      }
      const $ = s => host.querySelector(s);
      const setCh = t => { $('.lb-calculuslab-cht').textContent = t; };
      const msg = t => { $('.lb-calculuslab-msg').innerHTML = t; };
      function win(text) { if (won) return; won = true; api.sfx('correct'); api.win(p.winText && !customRound ? p.winText : text); }
      let customRound = false; // true after "New challenge" (the topic's own text no longer applies)
      function pointerX(e, svg) { const r = svg.getBoundingClientRect(); return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height }; }
      const listeners = [];
      const on = (el, ev, fn) => { el.addEventListener(ev, fn); listeners.push([el, ev, fn]); };
      function dragOn(svg, start, moveFn, end) {
        let dragging = false;
        on(svg, 'pointerdown', e => { dragging = start(pointerX(e, svg)) !== false; if (dragging) { svg.setPointerCapture && svg.setPointerCapture(e.pointerId); moveFn(pointerX(e, svg)); e.preventDefault(); } });
        on(svg, 'pointermove', e => { if (dragging) moveFn(pointerX(e, svg)); });
        const up = () => { if (dragging) { dragging = false; end && end(); } };
        on(svg, 'pointerup', up); on(svg, 'pointercancel', up);
      }
      const cleanup = () => { cancelAnimationFrame(raf); timers.forEach(clearInterval); listeners.forEach(([el, ev, fn]) => el.removeEventListener(ev, fn)); };
      const dot = (x, y, col, r = 7, extra = '') => `<circle cx="${X(x)}" cy="${Y(y)}" r="${r}" fill="${col}" stroke="#fff" stroke-width="2.5" ${extra}/>`;
      const halo = (x, y, col) => `<circle cx="${X(x)}" cy="${Y(y)}" r="19" fill="${col}" fill-opacity=".15"/>`;
      const lineThrough = (x, y, m, col, w = 2.5, dash = '') => `<line x1="${X(X0)}" y1="${Y(y + m * (X0 - x))}" x2="${X(X1)}" y2="${Y(y + m * (X1 - x))}" stroke="${col}" stroke-width="${w}" ${dash ? `stroke-dasharray="${dash}"` : ''} stroke-linecap="round"/>`;
      const label = (px, py, t, col, anchor = 'start', size = 11.5) => `<text x="${px}" y="${py}" font-size="${size}" font-weight="900" fill="${col}" text-anchor="${anchor}" paint-order="stroke" stroke="#fbfbff" stroke-width="3.5">${t}</text>`;

      if (mode === 'tangent') return tangent();
      if (mode === 'area') return area();
      if (mode === 'limit') return limit();
      return maxmin();

      // ================= tangent =================
      function tangent() {
        const showSec = p.secant !== false;
        let a = Math.max(X0, Math.min(X1, isFinite(+p.a) ? +p.a : (own ? X0 + SPAN * 0.3 : D.a)));
        const hMax = clean(niceStep(SPAN, 4));
        let h = isFinite(+p.h) && +p.h > 0 ? Math.min(hMax * 2, +p.h) : hMax;
        const hMin = 0.001;
        const toSl = hv => Math.round(1000 * Math.log(hMax * 2 / hv) / Math.log(hMax * 2 / hMin));
        const fromSl = s => { const v = hMax * 2 * Math.pow(hMin / (hMax * 2), s / 1000); return +v.toPrecision(2); };
        let target = p.target && isFinite(+p.target.slope) ? +p.target.slope : null;
        let chText = p.challenge || '';
        const okPoint = x => isFinite(f(x)) && isFinite(f1(x));
        function genTarget(rand) {
          const cands = [];
          for (let i = 1; i < 20; i++) { const x = X0 + SPAN * (0.1 + 0.8 * i / 20); if (!okPoint(x)) continue; const m = f1(x); const mr = Math.abs(m) >= 3 ? Math.round(m) : Math.round(m * 2) / 2; if (Math.abs(mr) > 1e-9 && roots(t => f1(t) - mr, X0 + SPAN * 0.04, X1 - SPAN * 0.04).length && Math.abs(x - a) > SPAN * 0.15) cands.push(mr); }
          if (!cands.length) return 1;
          return rand ? cands[Math.floor(Math.random() * cands.length)] : cands[Math.floor(cands.length * 0.8)];
        }
        if (target == null) target = genTarget(false);
        const genText = () => `Drag P to a point where the tangent has slope ${fmt(target)} (${fname}′(a) = ${fmt(target)}).`;
        if (!chText) chText = genText();
        shell(`<div class="lb-calculuslab-chips">
<div class="lb-calculuslab-chip" style="background:#f3edff;color:#5b33c9">a = <b data-o="a"></b></div>
<div class="lb-calculuslab-chip" style="background:#fff5d6;color:#9a6a00">${fname}(a) = <b data-o="fa"></b></div>
${showSec ? `<div class="lb-calculuslab-chip" style="background:#e0ecff;color:#2f6fd6">secant slope <b data-o="sec"></b></div>` : ''}
<div class="lb-calculuslab-chip" style="background:#d9f7ee;color:#0f7a5c">${fname}′(a) = <b data-o="d"></b></div></div>
${showSec ? `<div class="lb-calculuslab-sl"><span>h = <b data-o="h"></b></span><input type="range" min="0" max="1000" step="1" value="${toSl(h)}"><button class="lb-calculuslab-b go" data-act="lim" style="flex:0 0 auto;min-width:74px">h → 0 ▶</button></div>` : ''}
<div class="lb-calculuslab-row"><div class="lb-calculuslab-chip" style="background:#f6f4ff;flex:3" data-o="eq"></div><button class="lb-calculuslab-b" data-act="new" style="flex:1.2">New challenge</button></div>`);
        setCh(chText);
        const svg = $('.lb-calculuslab-svg'), dyn = $('.lb-calculuslab-dyn'), top = $('.lb-calculuslab-top'), sl = host.querySelector('input[type=range]');
        function draw() {
          const fa = f(a), m = f1(a);
          let g = '';
          if (showSec) {
            const b = a + h, fb = f(b);
            if (isFinite(fb)) {
              const ms = (fb - fa) / h;
              g += lineThrough(a, fa, ms, '#3b82f6', 2, '6 5');
              g += `<line x1="${X(a)}" y1="${Y(fa)}" x2="${X(b)}" y2="${Y(fa)}" stroke="#ffc93c" stroke-width="2.5"/><line x1="${X(b)}" y1="${Y(fa)}" x2="${X(b)}" y2="${Y(fb)}" stroke="#ff6b6b" stroke-width="2.5"/>`;
              if (Math.abs(X(b) - X(a)) > 22) g += label((X(a) + X(b)) / 2, Y(fa) + (fb > fa ? 13 : -6), 'h', '#b8860b', 'middle');
              g += dot(b, fb, '#3b82f6', 6) + label(X(b) + 8, Y(fb) + (fb > fa ? -6 : 14), 'Q', '#2f6fd6');
              host.querySelector('[data-o="sec"]').textContent = fmt(ms);
            } else host.querySelector('[data-o="sec"]').textContent = '—';
            host.querySelector('[data-o="h"]').textContent = fmt(h, 4);
          }
          if (isFinite(fa) && isFinite(m)) g += lineThrough(a, fa, m, '#2ed3a5', 3);
          dyn.innerHTML = g;
          top.innerHTML = isFinite(fa) ? halo(a, fa, '#8b5cf6') + dot(a, fa, '#8b5cf6', 9) + label(Math.min(PR - 12, X(a) + 12), Math.max(PT + 12, Y(fa) - 10), 'P', '#5b33c9') : '';
          host.querySelector('[data-o="a"]').textContent = fmt(a, 3);
          host.querySelector('[data-o="fa"]').textContent = fmt(fa, 3);
          host.querySelector('[data-o="d"]').textContent = isFinite(m) ? fmt(m, 3) : 'undefined';
          const c = fa - m * a;
          host.querySelector('[data-o="eq"]').innerHTML = isFinite(m) ? `Tangent: <b>y = ${Math.abs(m) < 5e-4 ? fmt(c, 3) : (fmt(m, 3) === '1' ? '' : fmt(m, 3) === '−1' ? '−' : fmt(m, 3)) + 'x ' + (c < 0 ? '− ' : '+ ') + fmt(Math.abs(c), 3)}</b>` : 'No tangent slope here';
          if (touched && !won && isFinite(m) && Math.abs(m - target) < 5e-4) {
            msg(`✔ At a = ${fmt(a, 3)}, ${fname}′(a) = ${fmt(m, 3)}`);
            win(`Slope ${fname}′(${fmt(a, 3)}) = ${fmt(target)} — the tangent there is y = ${fmt(m, 3)}x ${c < 0 ? '−' : '+'} ${fmt(Math.abs(c), 3)}`);
          }
        }
        dragOn(svg, () => { touched = true; }, pt => {
          let x = Math.max(X0, Math.min(X1, iX(pt.x)));
          const r = newton(t => f1(t) - target, x, X0, X1);
          if (r != null && Math.abs(r - x) < SPAN * 0.025) x = clean(r);
          else x = clean(snapTo(x, niceStep(SPAN, 200)));
          if (okPoint(x)) { a = x; draw(); }
        });
        if (sl) on(sl, 'input', () => { h = fromSl(+sl.value); draw(); });
        on(host, 'click', e => {
          const b = e.target.closest('[data-act]'); if (!b) return;
          if (b.dataset.act === 'lim') {
            cancelAnimationFrame(raf); let s = toSl(h) >= 990 ? 0 : toSl(h);
            const step = () => { s = Math.min(1000, s + 12); h = fromSl(s); sl.value = s; draw(); if (s < 1000) raf = requestAnimationFrame(step); else msg(`As h → 0, secant slope → ${fname}′(a) = ${fmt(f1(a), 3)}`); };
            raf = requestAnimationFrame(step); api.sfx('tap');
          } else if (b.dataset.act === 'new') {
            customRound = true; won = false; api.resetWin(); const old = target; let k = 0; do { target = genTarget(true); } while (target === old && k++ < 8);
            setCh(genText()); msg(''); api.sfx('tap'); draw();
          }
        });
        draw();
        msg('Drag P along the curve');
        return cleanup;
      }

      // ================= area =================
      function area() {
        const step = isFinite(+p.step) && +p.step > 0 ? +p.step : clean(niceStep(SPAN, 50));
        let a = isFinite(+p.a) ? +p.a : (own ? X0 + SPAN * 0.25 : D.a), b = isFinite(+p.b) ? +p.b : (own ? X1 - SPAN * 0.25 : D.b);
        a = Math.max(X0, Math.min(X1, a)); b = Math.max(X0, Math.min(X1, b)); if (b < a) [a, b] = [b, a];
        let n = Math.max(1, Math.min(200, Math.round(+p.n || 4)));
        let method = ['left', 'right', 'mid', 'trap'].includes(p.method) ? p.method : 'left';
        const Fc = typeof p.F === 'string' ? tryCompile(p.F) : null;
        let tg = p.target && typeof p.target === 'object' ? p.target : {};
        let mode2 = isFinite(+tg.area) ? 'area' : isFinite(+tg.error) && +tg.error > 0 ? 'error' : null;
        let tArea = +tg.area, tErr = +tg.error;
        if (!mode2) { mode2 = 'error'; tErr = 0.01; }
        const genText = () => mode2 === 'area' ? `Drag the limits so that ∫ₐᵇ ${fname}(x) dx = ${fmt(tArea)}.` : `Get the sum Sₙ within ${fmt(tErr)} of the exact area. Try the different rules!`;
        const nToSl = v => Math.round(Math.log(v) / Math.log(200) * 1000), slToN = s => Math.max(1, Math.round(Math.pow(200, s / 1000)));
        shell(`<div class="lb-calculuslab-chips">
<div class="lb-calculuslab-chip" style="background:#d9f7ee;color:#0f7a5c">S<sub>n</sub> = <b data-o="s"></b></div>
<div class="lb-calculuslab-chip" style="background:#f3edff;color:#5b33c9" data-o="ex"></div>
<div class="lb-calculuslab-chip" style="background:#ffe9e9;color:#d64545">error <b data-o="err"></b></div></div>
<div class="lb-calculuslab-sl"><span>n = <b data-o="n"></b></span><input type="range" min="0" max="1000" step="1" value="${nToSl(n)}"><button class="lb-calculuslab-b go" data-act="inf" style="flex:0 0 auto;min-width:72px">n → ∞ ▶</button></div>
<div class="lb-calculuslab-row">${[['left', 'Left'], ['right', 'Right'], ['mid', 'Mid'], ['trap', 'Trap']].map(([k, t]) => `<button class="lb-calculuslab-b" data-m="${k}">${t}</button>`).join('')}</div>`);
        setCh(p.challenge || genText());
        const svg = $('.lb-calculuslab-svg'), under = $('.lb-calculuslab-under'), top = $('.lb-calculuslab-top'), sl = host.querySelector('input[type=range]');
        function sum() {
          const dx = (b - a) / n; let s = 0;
          for (let i = 0; i < n; i++) {
            const xl = a + i * dx, xr = xl + dx;
            s += method === 'left' ? f(xl) : method === 'right' ? f(xr) : method === 'mid' ? f(xl + dx / 2) : (f(xl) + f(xr)) / 2;
          }
          return s * dx;
        }
        function draw() {
          const dx = (b - a) / n, y0 = Y(0); let g = '';
          for (let i = 0; i < n; i++) {
            const xl = a + i * dx, xr = xl + dx, sw = n > 60 ? 0 : 1;
            if (method === 'trap') {
              const yl = f(xl), yr2 = f(xr); if (!isFinite(yl) || !isFinite(yr2)) continue;
              const col = yl + yr2 >= 0 ? '#2ed3a5' : '#ff6b6b';
              g += `<path d="M${X(xl)} ${y0}L${X(xl)} ${Y(yl)}L${X(xr)} ${Y(yr2)}L${X(xr)} ${y0}Z" fill="${col}" fill-opacity=".38" stroke="${col}" stroke-width="${sw}"/>`;
            } else {
              const xs = method === 'left' ? xl : method === 'right' ? xr : xl + dx / 2, h = f(xs); if (!isFinite(h)) continue;
              const col = h >= 0 ? '#2ed3a5' : '#ff6b6b';
              g += `<rect x="${X(xl)}" y="${Math.min(y0, Y(h))}" width="${Math.max(0.3, X(xr) - X(xl))}" height="${Math.abs(Y(h) - y0)}" fill="${col}" fill-opacity=".38" stroke="${col}" stroke-width="${sw}"/>`;
              if (n <= 16) g += `<circle cx="${X(xs)}" cy="${Y(h)}" r="2.6" fill="#1b1f3a"/>`;
            }
          }
          under.innerHTML = g;
          const ya = Math.min(PB - 1, Math.max(PT + 1, y0));
          const handle = (x, t) => `<line x1="${X(x)}" y1="${PT}" x2="${X(x)}" y2="${PB}" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="${X(x)}" cy="${ya}" r="17" fill="#8b5cf6" fill-opacity=".16"/><circle cx="${X(x)}" cy="${ya}" r="10" fill="#8b5cf6" stroke="#fff" stroke-width="2.5"/><text x="${X(x)}" y="${ya + 4}" font-size="11" font-weight="900" fill="#fff" text-anchor="middle">${t}</text>`;
          top.innerHTML = handle(a, 'a') + handle(b, 'b') + label(Math.max(X(a), PL + 2), PT + 12, `a = ${fmt(a, 3)}`, '#5b33c9', X(a) > PR - 50 ? 'end' : 'start', 10.5) + label(Math.min(X(b), PR - 2), PT + 26, `b = ${fmt(b, 3)}`, '#5b33c9', X(b) > PR - 50 ? 'end' : 'start', 10.5);
          const S = sum(), I = integrate(f, a, b);
          host.querySelector('[data-o="s"]').textContent = fmt(S);
          host.querySelector('[data-o="n"]').textContent = n;
          let exTxt = `∫ = <b>${esc(show(I))}</b>`;
          if (Fc) { const v = Fc.f(b) - Fc.f(a); if (isFinite(v) && Math.abs(v - I) < 1e-6 * Math.max(1, Math.abs(I))) exTxt = `F(b) − F(a) = <b>${esc(show(I))}</b>`; }
          host.querySelector('[data-o="ex"]').innerHTML = exTxt;
          host.querySelector('[data-o="err"]').textContent = isFinite(S - I) ? fmt(Math.abs(S - I)) : '—';
          host.querySelectorAll('[data-m]').forEach(el => el.classList.toggle('on', el.dataset.m === method));
          if (!touched || won) return;
          if (mode2 === 'area' && Math.abs(I - tArea) < 1e-6 * Math.max(1, Math.abs(tArea))) { msg(`✔ ∫ from ${fmt(a, 3)} to ${fmt(b, 3)} = ${show(I)}`); win(`∫ from ${fmt(a, 3)} to ${fmt(b, 3)} of ${fname}(x) dx = ${show(I)}`); }
          else if (mode2 === 'area' && Math.abs(I - tArea) < 0.02 * Math.max(1, Math.abs(tArea))) msg('So close — nudge a limit by one step');
          else if (mode2 === 'error' && Math.abs(S - I) < tErr) { msg(`✔ ${({ left: 'Left', right: 'Right', mid: 'Midpoint', trap: 'Trapezium' })[method]} rule, n = ${n}: error ${fmt(Math.abs(S - I))}`); win(`With n = ${n} strips, Sₙ = ${fmt(S)} ≈ ∫ = ${show(I)} (error ${fmt(Math.abs(S - I))})`); }
        }
        // pick a target area reachable by dragging b (for "New challenge")
        function genArea() {
          for (let k = 0; k < 30; k++) {
            const bb = clean(snapTo(a + (X1 - a) * (0.3 + 0.7 * Math.random()), step));
            if (bb <= a || Math.abs(bb - b) < step * 3) continue;
            const I = integrate(f, a, bb); if (isFinite(I) && exactStr(I) && !exactStr(I).includes('π') && exactStr(I).length <= 5) return I;
          }
          return null;
        }
        let which = null;
        dragOn(svg, pt => { touched = true; const x = iX(pt.x); which = Math.abs(x - a) <= Math.abs(x - b) ? 'a' : 'b'; if (Math.abs(x - a) === Math.abs(x - b)) which = x > a ? 'b' : 'a'; }, pt => {
          const x = clean(Math.max(X0, Math.min(X1, snapTo(iX(pt.x), step))));
          if (which === 'a') a = Math.min(x, b); else b = Math.max(x, a);
          draw();
        });
        on(sl, 'input', () => { touched = true; n = slToN(+sl.value); draw(); });
        on(host, 'click', e => {
          const m = e.target.closest('[data-m]'); if (m) { touched = true; method = m.dataset.m; api.sfx('tap'); draw(); return; }
          const btn = e.target.closest('[data-act]'); if (!btn) return;
          if (btn.dataset.act === 'inf') {
            touched = true; clearInterval(timers[0]); n = 1; draw(); api.sfx('tap');
            timers[0] = setInterval(() => { n = Math.min(200, n < 8 ? n + 1 : Math.round(n * 1.45)); sl.value = nToSl(n); draw(); if (n >= 200) { clearInterval(timers[0]); msg(`As n → ∞, Sₙ → ∫ₐᵇ ${fname}(x) dx = ${show(integrate(f, a, b))}`); } }, 380);
          }
        });
        draw();
        msg(mode2 === 'area' ? 'Drag a or b along the x-axis' : 'Slide n, or tap "n → ∞"');
        // optional: new challenge button only meaningful for area targets
        if (mode2 === 'area') {
          const row = host.querySelector('.lb-calculuslab-row');
          row.insertAdjacentHTML('beforeend', '<button class="lb-calculuslab-b" data-act2="new" style="flex:1.6">New</button>');
          on(row, 'click', e => { if (!e.target.closest('[data-act2]')) return; const v = genArea(); if (v == null) return; customRound = true; tArea = v; won = false; api.resetWin(); setCh(genText()); msg('Drag a or b along the x-axis'); api.sfx('tap'); draw(); });
        }
        return cleanup;
      }

      // ================= limit =================
      function limit() {
        const A = lim0;
        const sideVal = s => { // numeric one-sided limit
          const v1 = f(A + s * 1e-4), v2 = f(A + s * 1e-5);
          if (!isFinite(v1) && !isFinite(v2)) return NaN;
          if (Math.abs(v2) > 1e4 && Math.abs(v2) > 4 * Math.abs(v1)) return v2 > 0 ? Infinity : -Infinity;
          const r = (10 * v2 - v1) / 9; // Richardson extrapolation (error ∝ h)
          const e = exactStr(+r.toFixed(6)); return e != null ? +(+r.toFixed(6)).toFixed(6) : +r.toFixed(4);
        };
        const LHL = sideVal(-1), RHL = sideVal(1);
        const exists = isFinite(LHL) && isFinite(RHL) && Math.abs(LHL - RHL) < 1e-3;
        const LIM = exists ? (LHL + RHL) / 2 : null;
        const fA = isFinite(+p.valueAt) ? +p.valueAt : f(A);
        const valTxt = v => v === Infinity ? '∞' : v === -Infinity ? '−∞' : (exactStr(v) || fmt(v));
        const h0 = SPAN / 2 >= 1 ? 1 : clean(niceStep(SPAN, 3));
        const sides = { L: [], R: [] }, hs = { L: h0 * 10, R: h0 * 10 };
        let px = A - h0; // probe point
        let chText = p.challenge || `Approach x = ${fmt(A)} from both sides. What is lim ${fname}(x) as x → ${fmt(A)}?`;
        const exTop = pieces ? `<div class="lb-calculuslab-fx">${fname}(x) = ${esc(pretty(p.fnLeft))} (x &lt; ${fmt(A)}), &nbsp;${esc(pretty(p.fnRight))} (x ≥ ${fmt(A)})</div>` : '';
        shell(`<div class="lb-calculuslab-row"><button class="lb-calculuslab-b" data-s="L">◀ x → ${fmt(A)}⁻</button><button class="lb-calculuslab-b" data-s="R">x → ${fmt(A)}⁺ ▶</button></div>
<div class="lb-calculuslab-tabs"><div class="lb-calculuslab-tab"><table><tr><th>x (left)</th><th>${fname}(x)</th></tr><tbody data-t="L"></tbody></table></div><div class="lb-calculuslab-tab"><table><tr><th>x (right)</th><th>${fname}(x)</th></tr><tbody data-t="R"></tbody></table></div></div>
<div class="lb-calculuslab-row" data-o="opts" style="display:none"></div>`, exTop);
        setCh(chText);
        const svg = $('.lb-calculuslab-svg'), dyn = $('.lb-calculuslab-dyn'), top = $('.lb-calculuslab-top');
        const rowTxt = x => { const v = f(x); return `<tr><td>${fmt(x, 6)}</td><td>${isFinite(v) ? fmt(v, 6) : '—'}</td></tr>`; };
        function draw() {
          let g = `<line x1="${X(A)}" y1="${PT}" x2="${X(A)}" y2="${PB}" stroke="#ffc93c" stroke-width="2" stroke-dasharray="5 5"/>`;
          if (exists) g += `<line x1="${PL}" y1="${Y(LIM)}" x2="${PR}" y2="${Y(LIM)}" stroke="#ffc93c" stroke-width="1.2" stroke-dasharray="3 5" opacity="${sides.L.length && sides.R.length ? 1 : 0}"/>`;
          dyn.innerHTML = g;
          let t = '';
          // holes and filled dots at x = a
          const hole = (y, col) => isFinite(y) ? `<circle cx="${X(A)}" cy="${Y(y)}" r="5.5" fill="#fbfbff" stroke="${col}" stroke-width="2.5"/>` : '';
          if (pieces) {
            const yl = pieces.L.f(A), yrr = pieces.R.f(A);
            t += hole(yl, '#8b5cf6');
            if (isFinite(+p.valueAt) && Math.abs(+p.valueAt - yrr) > 1e-9) t += hole(yrr, '#8b5cf6');
          } else if (exists && (!isFinite(f(A)) || isFinite(+p.valueAt))) t += hole(LIM, '#8b5cf6');
          if (isFinite(fA) && (pieces || isFinite(+p.valueAt))) t += `<circle cx="${X(A)}" cy="${Y(fA)}" r="5.5" fill="#8b5cf6" stroke="#fff" stroke-width="2"/>`;
          const py = f(px);
          if (isFinite(py)) {
            t += `<line x1="${X(px)}" y1="${Y(py)}" x2="${X(px)}" y2="${Y(0)}" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="3 3"/>`;
            t += halo(px, py, '#3b82f6') + dot(px, py, '#3b82f6', 8);
            const right = X(px) < PR - 120;
            t += label(X(px) + (right ? 12 : -12), Math.max(PT + 12, Y(py) - 12), `(${fmt(px, 4)}, ${fmt(py, 4)})`, '#2f6fd6', right ? 'start' : 'end', 10.5);
          }
          top.innerHTML = t;
          ['L', 'R'].forEach(s => { host.querySelector(`[data-t="${s}"]`).innerHTML = sides[s].slice(-4).map(rowTxt).join('') || `<tr><td colspan="2" style="color:#8a8fae">tap ${s === 'L' ? '◀' : '▶'}</td></tr>`; });
        }
        function maybeOptions() {
          const opts = host.querySelector('[data-o="opts"]');
          if (opts.style.display !== 'none') return;
          if (!(hs.L <= 0.0011 && hs.R <= 0.0011)) return;
          let right = exists ? valTxt(LIM) : 'Does not exist';
          const cand = new Set([right]);
          const add2 = v => { if (cand.size < 4 && v != null) cand.add(typeof v === 'string' ? v : valTxt(v)); };
          if (!exists) { if (isFinite(LHL)) add2(LHL); if (isFinite(RHL)) add2(RHL); }
          else add2('Does not exist');
          if (isFinite(fA)) add2(fA);
          [LIM != null ? LIM + 1 : 0, 0, 1, LIM != null ? -LIM : 2, LIM != null ? LIM / 2 : -1, 2].forEach(v => isFinite(v) && add2(v));
          const list = [...cand].sort(() => Math.random() - 0.5);
          opts.innerHTML = list.map(v => `<button class="lb-calculuslab-b" data-ans="${esc(v)}" style="font-size:${v.length > 8 ? 11.5 : 14}px">${esc(v)}</button>`).join('');
          opts.style.display = 'flex';
          msg('Now choose the value of the limit:');
          opts.dataset.right = right;
        }
        dragOn(svg, () => { touched = true; }, pt => {
          let x = clean(snapTo(Math.max(X0, Math.min(X1, iX(pt.x))), niceStep(SPAN, 300)));
          if (Math.abs(x - A) < 1e-9) x = A + (pt.x < X(A) ? -1 : 1) * niceStep(SPAN, 300);
          px = x; draw();
        });
        on(host, 'click', e => {
          const s = e.target.closest('[data-s]');
          if (s) {
            touched = true; const k = s.dataset.s; if (hs[k] <= 0.0011) { msg('That side is already very close — try the other side'); return; }
            hs[k] = clean(hs[k] / 10); if (hs[k] > h0) hs[k] = h0;
            px = clean(A + (k === 'L' ? -1 : 1) * hs[k]); sides[k].push(px); api.sfx('tap'); draw();
            msg(`x = ${fmt(px, 6)} → ${fname}(x) = ${fmt(f(px), 6)}`);
            maybeOptions(); return;
          }
          const o = e.target.closest('[data-ans]');
          if (o && !won) {
            const right = host.querySelector('[data-o="opts"]').dataset.right;
            if (o.dataset.ans === right) {
              o.classList.add('go');
              const why = exists ? `LHL = RHL = ${valTxt(LIM)}` : `LHL = ${valTxt(LHL)} but RHL = ${valTxt(RHL)}`;
              msg('✔ ' + why);
              win(exists ? `lim ${fname}(x) as x → ${fmt(A)} = ${valTxt(LIM)} (${why}${isFinite(fA) && Math.abs(fA - LIM) > 1e-9 ? `; note ${fname}(${fmt(A)}) = ${valTxt(fA)}` : !isFinite(f(A)) && !pieces ? `; ${fname}(${fmt(A)}) itself is undefined` : ''})` : `The limit does not exist: ${why}`);
            } else { api.sfx('wrong'); o.disabled = true; msg('Not quite — compare the last values in both tables'); }
          }
        });
        draw();
        msg('Tap ◀ and ▶ to move x closer to ' + fmt(A));
        return cleanup;
      }

      // ================= maxmin =================
      function maxmin() {
        const iv = Array.isArray(p.interval) && p.interval.length === 2 && +p.interval[0] < +p.interval[1] ? [Math.max(X0, +p.interval[0]), Math.min(X1, +p.interval[1])] : [X0, X1];
        const crit = roots(f1, iv[0], iv[1]).filter(x => isFinite(f(x))).map(x => {
          const s = f2(x); const k = s < -1e-9 ? 'max' : s > 1e-9 ? 'min' : (() => { const e = SPAN * 1e-3; const l = f1(x - e), r = f1(x + e); return l > 0 && r < 0 ? 'max' : l < 0 && r > 0 ? 'min' : 'infl'; })();
          return { x: Math.abs(x - Math.round(x * 1e6) / 1e6) < 1e-9 ? Math.round(x * 1e6) / 1e6 : x, k };
        });
        const cands = crit.concat([{ x: iv[0], k: 'end' }, { x: iv[1], k: 'end' }]).filter(c => isFinite(f(c.x)));
        let find = p.target && ['max', 'min', 'absmax', 'absmin'].includes(p.target.find) ? p.target.find : null;
        if (!find) find = crit.some(c => c.k === 'max') ? 'max' : crit.some(c => c.k === 'min') ? 'min' : 'absmax';
        function goalOf(fd) {
          if (fd === 'max' || fd === 'min') { const l = crit.filter(c => c.k === fd); if (!l.length) return null; return l.reduce((a, c) => (fd === 'max' ? f(c.x) > f(a.x) : f(c.x) < f(a.x)) ? c : a); }
          return cands.reduce((a, c) => (fd === 'absmax' ? f(c.x) > f(a.x) : f(c.x) < f(a.x)) ? c : a);
        }
        let goal = goalOf(find); if (!goal) { find = 'absmax'; goal = goalOf(find); }
        const word = { max: 'local maximum', min: 'local minimum', absmax: 'absolute maximum', absmin: 'absolute minimum' };
        const genText = () => `Drag the point to the ${word[find]} of ${fname}(x)${find.startsWith('abs') ? ` on [${fmt(iv[0])}, ${fmt(iv[1])}]` : ''}.`;
        let x = isFinite(+p.a) ? Math.max(iv[0], Math.min(iv[1], +p.a)) : clean(iv[0] + (iv[1] - iv[0]) * 0.08);
        let showSign = false;
        const seen = new Set();
        shell(`<div class="lb-calculuslab-chips">
<div class="lb-calculuslab-chip" style="background:#f3edff;color:#5b33c9">x = <b data-o="x"></b></div>
<div class="lb-calculuslab-chip" style="background:#fff5d6;color:#9a6a00">${fname}(x) = <b data-o="f"></b></div>
<div class="lb-calculuslab-chip" data-o="d1c">${fname}′ = <b data-o="d1"></b></div>
<div class="lb-calculuslab-chip" style="background:#e0ecff;color:#2f6fd6">${fname}″ = <b data-o="d2"></b></div></div>
<div class="lb-calculuslab-row"><button class="lb-calculuslab-b" data-act="sign">${fname}′ sign chart</button><button class="lb-calculuslab-b" data-act="new">New challenge</button></div>`);
        setCh(p.challenge || genText());
        const svg = $('.lb-calculuslab-svg'), dyn = $('.lb-calculuslab-dyn'), top = $('.lb-calculuslab-top'), under = $('.lb-calculuslab-under');
        function draw() {
          // sign chart strip
          let u = '';
          if (showSign) {
            const n = 120;
            for (let i = 0; i < n; i++) { const xa = iv[0] + (iv[1] - iv[0]) * i / n, xb = iv[0] + (iv[1] - iv[0]) * (i + 1) / n, s = f1((xa + xb) / 2); if (!isFinite(s)) continue; u += `<rect x="${X(xa)}" y="${PB - 9}" width="${X(xb) - X(xa) + 0.5}" height="9" fill="${s > 0 ? '#2ed3a5' : '#ff6b6b'}" opacity=".8"/>`; }
            u += label(PL + 3, PB - 12, `${fname}′ > 0 ↑   ${fname}′ < 0 ↓`, '#6b7090', 'start', 9.5);
          }
          if (iv[0] > X0 || iv[1] < X1) u += `<rect x="${PL}" y="${PT}" width="${X(iv[0]) - PL}" height="${PB - PT}" fill="#1b1f3a" opacity=".05"/><rect x="${X(iv[1])}" y="${PT}" width="${PR - X(iv[1])}" height="${PB - PT}" fill="#1b1f3a" opacity=".05"/>`;
          under.innerHTML = u;
          const y = f(x), m = f1(x), s2 = f2(x);
          let g = '';
          const len = SPAN * 0.14 / Math.sqrt(1 + Math.pow(m * SPAN / (Y1 - Y0) * (PB - PT) / (PR - PL), 2));
          if (isFinite(m)) g += `<line x1="${X(x - len)}" y1="${Y(y - m * len)}" x2="${X(x + len)}" y2="${Y(y + m * len)}" stroke="${Math.abs(m) < 1e-9 ? '#ffc93c' : m > 0 ? '#2ed3a5' : '#ff6b6b'}" stroke-width="4" stroke-linecap="round"/>`;
          dyn.innerHTML = g;
          let t = '';
          crit.forEach(c => { if (!seen.has(c.x)) return; const cy = f(c.x); t += `<circle cx="${X(c.x)}" cy="${Y(cy)}" r="4.5" fill="#ffc93c" stroke="#1b1f3a" stroke-width="1.5"/>` + label(X(c.x), Y(cy) + (c.k === 'min' ? 18 : -10), c.k === 'max' ? 'max' : c.k === 'min' ? 'min' : 'inflection', '#9a6a00', 'middle', 10); });
          t += halo(x, y, '#8b5cf6') + dot(x, y, '#8b5cf6', 9);
          top.innerHTML = t;
          host.querySelector('[data-o="x"]').textContent = fmt(x, 3);
          host.querySelector('[data-o="f"]').textContent = fmt(y, 3);
          host.querySelector('[data-o="d1"]').textContent = fmt(Math.abs(m) < 1e-9 ? 0 : m, 3);
          host.querySelector('[data-o="d2"]').textContent = fmt(Math.abs(s2) < 1e-9 ? 0 : s2, 3);
          const dc = host.querySelector('[data-o="d1c"]');
          dc.style.background = Math.abs(m) < 1e-9 ? '#fff0c2' : m > 0 ? '#d9f7ee' : '#ffe9e9'; dc.style.color = Math.abs(m) < 1e-9 ? '#9a6a00' : m > 0 ? '#0f7a5c' : '#d64545';
          const c = crit.find(c => c.x === x);
          if (c) msg(`${fname}′(${fmt(x, 3)}) = 0 → ${c.k === 'max' ? `${fname}″ < 0: local maximum` : c.k === 'min' ? `${fname}″ > 0: local minimum` : 'neither (point of inflection)'}, ${fname} = ${fmt(y, 3)}`);
          else if (x === iv[0] || x === iv[1]) msg(`End point of [${fmt(iv[0])}, ${fmt(iv[1])}]: ${fname} = ${fmt(y, 3)}`);
          else msg(m > 0 ? `${fname}′ > 0: ${fname} is increasing here` : m < 0 ? `${fname}′ < 0: ${fname} is decreasing here` : '');
          if (touched && !won && Math.abs(x - goal.x) < 1e-12) {
            win(`${word[find][0].toUpperCase() + word[find].slice(1)} at x = ${exactStr(x) || fmt(x, 3)}: ${fname}(${exactStr(x) || fmt(x, 3)}) = ${exactStr(y) || fmt(y, 3)}${goal.k !== 'end' ? ` (${fname}′ = 0, ${fname}″ ${f2(x) < 0 ? '< 0' : '> 0'})` : ' (an end point)'}`);
          }
        }
        dragOn(svg, () => { touched = true; }, pt => {
          let nx = Math.max(iv[0], Math.min(iv[1], iX(pt.x)));
          const near = cands.filter(c => Math.abs(c.x - nx) < SPAN * 0.03).sort((a, b) => Math.abs(a.x - nx) - Math.abs(b.x - nx))[0];
          if (near) { nx = near.x; if (near.k !== 'end') { if (!seen.has(near.x)) api.sfx('tap'); seen.add(near.x); } }
          else nx = clean(snapTo(nx, niceStep(SPAN, 200)));
          if (isFinite(f(nx))) { x = nx; draw(); }
        });
        on(host, 'click', e => {
          const b = e.target.closest('[data-act]'); if (!b) return;
          if (b.dataset.act === 'sign') { showSign = !showSign; b.classList.toggle('on', showSign); api.sfx('tap'); draw(); }
          else {
            const opts = ['max', 'min', 'absmax', 'absmin'].filter(k => k !== find && goalOf(k));
            if (!opts.length) return;
            find = opts[Math.floor(Math.random() * opts.length)]; goal = goalOf(find); customRound = true; won = false; api.resetWin(); setCh(genText()); api.sfx('tap'); draw();
          }
        });
        draw();
        if (!host.querySelector('.lb-calculuslab-msg').textContent) msg('Drag the point along the curve');
        return cleanup;
      }
    },
    example: { mode: 'tangent', fn: 'x^3 - 3x', xRange: [-2.5, 2.5], a: 0.5, target: { slope: 9 }, challenge: 'Find a point where the tangent to y = x³ − 3x has slope 9.' },
    examples: [
      { mode: 'area', fn: 'x^2', xRange: [-0.5, 3.5], a: 0, b: 1, n: 6, F: 'x^3/3', target: { area: 9 }, challenge: 'Drag b so that ∫₀ᵇ x² dx = 9. (Use F(x) = x³/3.)' },
      { mode: 'limit', fn: 'sin(x)/x', xRange: [-7, 7], a: 0, challenge: 'x → 0 पर sin x / x की सीमा (limit) ज्ञात कीजिए।' },
      { mode: 'maxmin', fn: 'x(12 - 2x)^2', fname: 'V', xRange: [0, 6], interval: [0, 6], target: { find: 'absmax' }, xLabel: 'x (cm)', yLabel: 'V (cm³)', challenge: 'A box is made from a 12 cm square sheet by cutting squares of side x. Find x for the largest volume V.' }
    ]
  });
})();
