/* ================= Endless practice: never-ending, code-generated questions =================
   Every number in a question, in its four options and in its worked steps is COMPUTED here by code
   (exact integer / fraction arithmetic), never typed by hand. Wrong options are computed from real
   mistakes (forgetting to carry, wrong operation, off by one, ...), always distinct from the answer.
   Generators are matched to a topic by subject + grade + keywords in the topic title.
     Gen.has(topicId, title, grade, subject)  -> true if some generator fits
     Gen.next(topicId, title, grade, subject) -> { q, options[4], answer, explain, steps[2-6], meta }
     Gen.open(host, topic, { onExit })        -> one-question-at-a-time endless practice UI       */
(function () {
  'use strict';
  /* ---------- exact maths kit ---------- */
  const R = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; }
  const lcm = (a, b) => a / gcd(a, b) * b;
  class Fr {
    constructor(p, q = 1) {
      if (!Number.isSafeInteger(p) || !Number.isSafeInteger(q) || q === 0) throw new Error('bad fraction');
      if (q < 0) { p = -p; q = -q; } const g = gcd(p, q) || 1; this.p = p / g; this.q = q / g;
    }
    add(o) { o = F(o); return new Fr(this.p * o.q + o.p * this.q, this.q * o.q); }
    sub(o) { o = F(o); return new Fr(this.p * o.q - o.p * this.q, this.q * o.q); }
    mul(o) { o = F(o); return new Fr(this.p * o.p, this.q * o.q); }
    div(o) { o = F(o); return new Fr(this.p * o.q, this.q * o.p); }
    eq(o) { o = F(o); return this.p === o.p && this.q === o.q; }
    get int() { return this.q === 1; }
    get v() { return this.p / this.q; }
  }
  function D(s) { s = String(s); const neg = s[0] === '-'; if (neg) s = s.slice(1); const [i, f = ''] = s.split('.'); const x = new Fr(+(i + f), 10 ** f.length); return neg ? new Fr(-x.p, x.q) : x; }
  const F = (p, q = 1) => p instanceof Fr ? p : typeof p === 'string' ? D(p) : Number.isInteger(p) ? new Fr(p, q) : D(String(p));
  const digits = n => String(n).split('').reverse().map(Number);
  const isPrime = n => { if (n < 2) return false; for (let k = 2; k * k <= n; k++) if (n % k === 0) return false; return true; };
  const pfList = n => { const f = []; for (let k = 2; k * k <= n; k++) while (n % k === 0) { f.push(k); n /= k; } if (n > 1) f.push(n); return f; };
  const fact = n => n <= 1 ? 1 : n * fact(n - 1);
  const nPr = (n, r) => { let x = 1; for (let k = 0; k < r; k++) x *= n - k; return x; };
  const nCr = (n, r) => nPr(n, r) / fact(r);

  /* ---------- formatting (Indian commas, real minus sign, exact decimals) ---------- */
  function ind(n) {
    if (!Number.isSafeInteger(n)) throw new Error('unsafe integer');
    let s = String(Math.abs(n));
    if (s.length > 3) s = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + s.slice(-3);
    return (n < 0 ? '−' : '') + s;
  }
  function dec(x, maxdp = 4) {           // exact decimal string, or null if it needs more than maxdp places
    x = F(x); let k = 0; while (k <= maxdp && (10 ** k) % x.q) k++; if (k > maxdp) return null;
    const n = x.p * (10 ** k / x.q), a = Math.abs(n), ip = Math.floor(a / 10 ** k), fp = a % 10 ** k;
    return (n < 0 ? '−' : '') + ind(ip) + (k ? '.' + String(fp).padStart(k, '0') : '');
  }
  const fs = x => { x = F(x); return x.q === 1 ? ind(x.p) : (x.p < 0 ? '−' : '') + Math.abs(x.p) + '/' + x.q; };
  const nm = x => dec(x) ?? fs(x);
  const pn = x => { const s = nm(x); return s[0] === '−' ? `(${s})` : s; };          // negatives in brackets inside sums
  const rs = x => '₹' + nm(x);
  const SUP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', '-': '⁻' };
  const sup = n => String(n).split('').map(c => SUP[c]).join('');
  const pfStr = n => pfList(n).join(' × ');
  const pfPow = n => { const f = pfList(n), m = new Map(); f.forEach(p => m.set(p, (m.get(p) || 0) + 1)); return [...m].map(([p, e]) => e > 1 ? p + sup(e) : '' + p).join(' × '); };
  const Cap = s => s[0].toUpperCase() + s.slice(1);
  const PL = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'lakhs', 'ten lakhs'];
  const NAMES = ['Riya', 'Aarav', 'Meera', 'Kabir', 'Diya', 'Arjun', 'Ananya', 'Ishaan', 'Priya', 'Rohan', 'Sana', 'Vihaan', 'Zoya', 'Neha', 'Dev', 'Tara', 'Kunal', 'Pooja', 'Farhan', 'Simran'];
  const ITEMS = ['mangoes', 'marbles', 'pencils', 'laddoos', 'stickers', 'bangles', 'kites', 'balloons', 'shells', 'beads', 'flowers', 'crayons'];
  const EMO = { mangoes: '🥭', marbles: '🔵', pencils: '✏️', laddoos: '🟡', stickers: '⭐', bangles: '⭕', kites: '🪁', balloons: '🎈', shells: '🐚', beads: '🟣', flowers: '🌼', crayons: '🖍️' };
  const two = () => { const a = pick(NAMES); let b = pick(NAMES); while (b === a) b = pick(NAMES); return [a, b]; };
  function poly(cs, v = 'x') {        // [a, b, c] -> "2x² − 3x + 1"
    const n = cs.length - 1; let s = '';
    cs.forEach((c, i) => { if (!c) return; const e = n - i, a = Math.abs(c);
      const body = (e && a === 1 ? '' : ind(a)) + (e ? v + (e > 1 ? sup(e) : '') : '');
      s += s ? (c < 0 ? ' − ' : ' + ') + body : (c < 0 ? '−' : '') + body; });
    return s || '0';
  }

  function polyF(cs, v = 'x') {       // fraction coefficients -> "(1/3)x³ − (3/2)x² + 4x"
    const n = cs.length - 1; let s = '';
    cs.forEach((c, i) => { c = F(c); if (!c.p) return; const e = n - i, a = c.p < 0 ? c.mul(-1) : c, as = a.int ? (e && a.p === 1 ? '' : ind(a.p)) : `(${fs(a)})`;
      const body = as + (e ? v + (e > 1 ? sup(e) : '') : '');
      s += s ? (c.p < 0 ? ' − ' : ' + ') + body : (c.p < 0 ? '−' : '') + body; });
    return s || '0';
  }

  /* ---------- options: correct + 3 computed mistakes, all distinct ---------- */
  function moreNum(c) {
    if (c instanceof Fr) return c.int ? new Fr(c.p + pick([-3, -2, -1, 1, 2, 3]) * Math.max(1, Math.round(Math.abs(c.p) * .08))) : c.add(new Fr(pick([-2, -1, 1, 2]), c.q));
    if (typeof c === 'number') { const sp = Math.max(3, Math.round(Math.abs(c) * .12)); return c + R(1, sp) * pick([-1, 1]); }
    return null;
  }
  function build(correct, wrongs, fmt, o = {}) {
    const c = fmt(correct), seen = new Set([c]), out = [], ok = o.ok || (() => true);
    const add = w => { if (out.length >= 3 || w == null) return; let s; try { if (typeof w === 'number' && !Number.isFinite(w)) return; if (!ok(w)) return; s = fmt(w); } catch (e) { return; }
      if (s == null || seen.has(s)) return; seen.add(s); out.push(s); };
    wrongs.forEach(add);
    for (let k = 0; out.length < 3 && k < 400; k++) add(o.more ? o.more(k) : moreNum(correct));
    if (out.length < 3) throw new Error('not enough options');
    const all = shuffle([c, ...out]);
    return { options: all, answer: all.indexOf(c), ans: c };
  }
  /* every bare whole number of 4+ digits gets Indian commas (decimal parts are never touched) */
  const fixN = s => String(s).replace(/(?<![\d.⁰¹²³⁴⁵⁶⁷⁸⁹]|\d,)(\d{4,})(?!\d|,\d)/g, d => ind(+d));
  const Q = (q, b, explain, steps, meta, extra) => Object.assign({ q: fixN(q), options: b.options.map(fixN), answer: b.answer, explain: fixN(explain), steps: [...steps, 'Answer: ' + b.ans].map(fixN), meta }, extra || {});
  const pos = v => F(v).p > 0;
  const nonneg = v => F(v).p >= 0;
  const titleNums = t => (t.match(/\d+/g) || []).map(Number);

  /* ---------- column methods (steps + the classic mistakes) ---------- */
  function colAdd(a, b) {
    const big = Math.max(a, b), small = Math.min(a, b), A = digits(big), B = digits(small), n = A.length, steps = [];
    let c = 0, noCarry = 0;
    for (let i = 0; i < n; i++) {
      const x = A[i], hasY = i < B.length, y = hasY ? B[i] : 0, t = x + y + c, parts = [x, ...(hasY ? [y] : []), ...(c ? [c] : [])];
      steps.push(`${Cap(PL[i])}: ` + (parts.length === 1 ? `bring down ${x}` : `${parts.join(' + ')} = ${t}` + (t >= 10 && i < n - 1 ? `, write ${t % 10}, carry ${Math.floor(t / 10)}` : '')));
      noCarry += (i < n - 1 ? (x + y) % 10 : x + y) * 10 ** i;
      c = i < n - 1 ? Math.floor(t / 10) : 0;
    }
    return { steps, noCarry };
  }
  function colSub(a, b) {
    const A = digits(a), B = digits(b), steps = []; let br = 0, noBorrow = 0, noReduce = 0;
    for (let i = 0; i < A.length; i++) {
      const x = A[i], hasY = i < B.length, y = hasY ? B[i] : 0, top = x - br, need = top < y, d = (need ? top + 10 : top) - y;
      const tt = br ? `${x} − 1` : `${x}`;
      steps.push(`${Cap(PL[i])}: ` + (need ? `borrow 1 from the next place, ${tt} + 10${hasY ? ` − ${y}` : ''} = ${d}` : !hasY && !br ? `bring down ${x}` : `${tt}${hasY ? ` − ${y}` : ''} = ${d}`));
      noBorrow += Math.abs(x - y) * 10 ** i; noReduce += (x < y ? x + 10 - y : x - y) * 10 ** i;
      br = need ? 1 : 0;
    }
    return { steps, noBorrow, noReduce };
  }
  function longDiv(n, d) {
    const ds = String(n).split('').map(Number), steps = []; let cur = 0, started = false;
    for (const x of ds) {
      cur = cur * 10 + x; const q = Math.floor(cur / d);
      if (!started && !q) continue; started = true;
      steps.push(q ? `${cur} ÷ ${d} → ${q}: ${d} × ${q} = ${d * q}, ${cur} − ${d * q} = ${cur - d * q}` : `${cur} is less than ${d}, so write 0 in the quotient`);
      cur -= d * q;
    }
    return steps;
  }

  /* =====================================================================================
     GENERATORS. Each: id, name, subj (subjects), g [min grade, max grade], re (title must match),
     not (title must not match), make(ctx) -> question. ctx = { g, title, subj }.
     ===================================================================================== */
  const GENS = [];
  const def = o => GENS.push(o);
  const MONEYX = /money|rupee|₹|coin|note|bill|shop|paying|balance|price|cost/i;

  /* ---- 1. Addition within 20 / 2-digit (Grades 1–2) ---- */
  def({ id: 'add_small', name: 'Addition', subj: ['maths'], g: [1, 2], re: /\badd|addition|sum puzzle|putting together|going past 100/i, not: /money|rupee|coin|equal groups|magic|chart|length|repeated|days/i,
    make({ g, title }) {
      let a, b; const past = g === 2 && /past 100/i.test(title);
      if (g === 1) { a = R(2, 15); b = R(1, 20 - a); } else if (past) { a = R(45, 95); b = R(Math.max(10, 101 - a), 99); } else { a = R(11, 78); b = R(10, 99 - a - 1 < 10 ? 10 : 99 - a); if (a + b > 99) b = 99 - a; }
      if (b < 1) b = 1;
      const s = a + b, [n1, n2] = two(), it = pick(ITEMS), story = Math.random() < .5;
      const q = story ? `${n1} has ${a} ${it}. ${n2} gives ${n1} ${b} more. How many ${it} does ${n1} have now?` : `What is ${a} + ${b}?`;
      let steps;
      if (g === 1) {
        if (a < 10 && s > 10) steps = [`Make a ten first: ${a} + ${10 - a} = 10`, `Split ${b}: ${b} = ${10 - a} + ${b - (10 - a)}`, `10 + ${b - (10 - a)} = ${s}`];
        else steps = [`Start at ${a} and count on ${b}: ${Array.from({ length: b }, (_, k) => a + k + 1).join(', ')}`, `${a} + ${b} = ${s}`];
      } else steps = colAdd(a, b).steps;
      const ca = g === 1 ? null : colAdd(a, b).noCarry;
      const bb = build(s, [ca, s + 1, s - 1, Math.abs(a - b), s + 10, s - 10], ind, { ok: v => v > 0 });
      return Q(q, bb, g === 1 ? `Adding means putting together. ${a} and ${b} more make ${s}.` : `Add the ones first, then the tens. Remember to carry when the ones add up to 10 or more.`, steps,
        { a, b }, g === 1 && s <= 20 ? { visual: { kind: 'numberline', from: 0, to: 20, marks: [a, s], jumps: [[a, s]] } } : null);
    } });

  /* ---- 2. Subtraction within 20 / 2-digit (Grades 1–2) ---- */
  def({ id: 'sub_small', name: 'Subtraction', subj: ['maths'], g: [1, 2], re: /subtract|take away|taking away|hop back|getting down|how much is left|how many more|hidden dots|add or take away|add or subtract/i, not: MONEYX,
    make({ g }) {
      let a, b; if (g === 1) { a = R(5, 20); b = R(1, a - 1); } else { a = R(30, 99); b = R(11, a - 5); }
      const d = a - b, [n1] = two(), it = pick(ITEMS), story = Math.random() < .5;
      const q = story ? `${n1} had ${a} ${it} and gave away ${b}. How many ${it} are left?` : `What is ${a} − ${b}?`;
      let steps, cs = null;
      if (g === 1) steps = a > 10 && b > a - 10 && a - 10 < b ? [`Take away ${a - 10} to reach 10: ${a} − ${a - 10} = 10`, `Take away the rest: ${b} − ${a - 10} = ${b - (a - 10)}`, `10 − ${b - (a - 10)} = ${d}`] : [`Start at ${a} and count back ${b}`, `${a} − ${b} = ${d}`];
      else { cs = colSub(a, b); steps = cs.steps; }
      const bb = build(d, [cs && cs.noBorrow, cs && cs.noReduce, d + 1, d - 1, a + b, d + 10], ind, { ok: v => v >= 0 });
      return Q(q, bb, `Taking away ${b} from ${a} leaves ${d}. Check: ${d} + ${b} = ${a}.`, steps, { a, b },
        g === 1 ? { visual: { kind: 'numberline', from: 0, to: 20, marks: [d, a], jumps: [[a, d]] } } : null);
    } });

  /* ---- 3. Column addition with carrying (Grades 3–5) ---- */
  def({ id: 'add_col', name: 'Column addition', subj: ['maths'], g: [3, 5], re: /\badd(ing|ition)?\b|big sums|partners/i,
    not: /money|rupee|length|distance|litre|magic|chart|equal groups|reverse|odd|fraction|decimal|integer|weight|bill|consecutive|sums equal|closest/i,
    make({ g }) {
      const lo = [0, 0, 0, 100, 1000, 10000][g], hi = [0, 0, 0, 999, 9999, 99999][g];
      const a = R(lo, Math.floor(hi * .7)), b = R(lo, hi - a);
      const s = a + b, ca = colAdd(a, b), [n1] = two(), story = Math.random() < .4;
      const q = story ? `A school library had ${ind(a)} books. It got ${ind(b)} new books. How many books does it have now?` : `Add: ${ind(a)} + ${ind(b)}`;
      const bb = build(s, [ca.noCarry, s + 10, s - 10, s + 100, s + 1, s - 1], ind, { ok: v => v > 0 });
      return Q(q, bb, `Line up the places and add from the ones. When a column makes 10 or more, write the ones digit and carry 1 to the next place.`, ca.steps, { a, b });
    } });

  /* ---- 4. Column subtraction with borrowing (Grades 3–5) ---- */
  def({ id: 'sub_col', name: 'Column subtraction', subj: ['maths'], g: [3, 5], re: /subtract|taking away|take away|how much is left|add or subtract|add and subtract|partners|difference/i, not: /money|rupee|balance|bill|length|distance|fraction|decimal|integer|weight|odd|change|division/i,
    make({ g }) {
      const lo = [0, 0, 0, 200, 2000, 20000][g], hi = [0, 0, 0, 999, 9999, 99999][g];
      const a = R(lo, hi), b = R(Math.floor(lo / 2), a - 1);
      const d = a - b, cs = colSub(a, b), story = Math.random() < .4;
      const q = story ? `A train had ${ind(a)} passengers. At a big station ${ind(b)} got down. How many passengers are still on the train?` : `Subtract: ${ind(a)} − ${ind(b)}`;
      const bb = build(d, [cs.noBorrow, cs.noReduce, d + 10, d - 10, a + b, d + 100], ind, { ok: v => v >= 0 });
      return Q(q, bb, `Subtract from the ones. If the top digit is smaller, borrow 1 from the next place (it becomes 10 more here). Check: ${ind(d)} + ${ind(b)} = ${ind(a)}.`, cs.steps, { a, b });
    } });

  /* ---- 5. Multiplication facts and tables (Grades 1–3) ---- */
  def({ id: 'times_basic', name: 'Multiplication facts', subj: ['maths'], g: [1, 3], re: /equal groups|repeated addition|how many times|\btables?\b|multipl|arrays|wings, legs|frog jumps|turn it around|adding equal groups/i, not: /money|shar|divide|chart|patterns|fruit|survey|colour day|vegetables/i,
    make({ g, title }) {
      let a, b, steps; const it = pick(ITEMS);
      if (g === 1) { b = R(2, 5); a = R(2, 5); }
      else { const tn = titleNums(title).filter(x => x >= 2 && x <= 10); a = tn.length ? pick(tn) : pick(g === 2 ? [2, 3, 4, 5, 10] : [2, 3, 4, 5, 6, 7, 8, 9, 10]); b = R(2, 10); }
      const p = a * b, story = g === 1 || Math.random() < .4;
      const q = story ? `There are ${b} plates with ${a} ${it} on each plate. How many ${it} are there in all?` : `What is ${b} × ${a}?`;
      steps = [`${b} groups of ${a}`, `${Array(b).fill(a).join(' + ')} = ${p}`, `So ${b} × ${a} = ${p}`];
      const bb = build(p, [a + b, p + a, p - a, p + b, p - b], ind, { ok: v => v > 0 });
      return Q(q, bb, `${b} groups of ${a} is ${a} added ${b} times, which is ${b} × ${a} = ${p}.`, steps, { a, b }, p <= 40 ? { visual: { kind: 'count', emoji: EMO[it], n: p, groups: b } } : null);
    } });

  /* ---- 6. Multiplying bigger numbers (Grades 4–7) ---- */
  def({ id: 'mult_big', name: 'Long multiplication', subj: ['maths'], g: [4, 7], re: /\bmultiplying\b|\bmultiplication\b|\d-digit ×|× \d-digit|times-1\d|tables from 11/i, not: /fraction|decimal|integer|matri|complex|chart|patterns|estimat|identit|shortcuts? with|puzzle|check|order, zero|by 10s|lengths|tokens|equal groups|nearest/i,
    make({ g }) {
      const t = g === 4 ? pick(['2x1', '3x1', '2x2']) : pick(['3x1', '4x1', '2x2', '3x2']);
      const nd = s => +s, [da, db] = t.split('x').map(nd);
      const a = R(10 ** (da - 1) + 1, 10 ** da - 1), m = db === 1 ? R(3, 9) : R(12, 99), p = a * m;
      let steps, wr = [];
      if (db === 1) {
        const parts = digits(a).map((x, i) => x * 10 ** i).filter(Boolean).reverse();
        steps = [...parts.map(x => `${ind(x)} × ${m} = ${ind(x * m)}`), `${parts.map(x => ind(x * m)).join(' + ')} = ${ind(p)}`];
        if (steps.length < 2) steps.unshift(`Multiply each place by ${m}`);
        wr.push(digits(a).reduce((s, x, i) => s + ((x * m) % 10) * 10 ** i, 0));
      } else {
        const m1 = m % 10, m10 = m - m1;
        steps = m1 ? [`${ind(a)} × ${m1} = ${ind(a * m1)}`, `${ind(a)} × ${m10} = ${ind(a * m10)}`, `${ind(a * m1)} + ${ind(a * m10)} = ${ind(p)}`] : [`${ind(a)} × ${m10 / 10} = ${ind(a * m10 / 10)}`, `${ind(a * m10 / 10)} × 10 = ${ind(p)}`];
        wr.push(a * m1 + a * (m10 / 10));     // forgot the zero in the tens row
      }
      const story = Math.random() < .4;
      const q = story ? `One box holds ${ind(a)} pencils. How many pencils are there in ${m} such boxes?` : `Find ${ind(a)} × ${m}.`;
      const bb = build(p, [...wr, p + a, p - a, a * (m + 10), a + m], ind, { ok: v => v > 0 });
      return Q(q, bb, `Break the multiplication into parts by place value, multiply each part, then add the parts.`, steps, { a, m });
    } });

  /* ---- 7. Division, sharing and long division (Grades 2–6) ---- */
  def({ id: 'division', name: 'Division', subj: ['maths'], g: [2, 6], re: /divi(de|ding|sion)|sharing equally|sharing sweets|equal sharing|how many groups|sharing with pictures|grouping into equal rows/i, not: /fraction|decimal|integer|polynomial|algorithm|divisib|money|length|patterns|clever|missing|true or false|10 and 100|10s/i,
    make({ g }) {
      let d, q, r = 0;
      if (g <= 3) { d = R(2, g === 2 ? 5 : 10); q = R(2, 10); }
      else if (g === 4) { d = R(3, 9); q = R(12, 99); r = Math.random() < .5 ? R(1, d - 1) : 0; }
      else { const two_ = Math.random() < .4; d = two_ ? R(11, 25) : R(3, 9); q = two_ ? R(12, 99) : R(102, 999); r = Math.random() < .5 ? R(1, d - 1) : 0; }
      const n = d * q + r, it = pick(ITEMS), [n1] = two();
      const fmt = v => v[1] ? `${ind(v[0])} remainder ${v[1]}` : ind(v[0]);
      const q_ = g <= 3 ? `${n} ${it} are shared equally among ${d} children. How many does each child get?` : r ? `Divide ${ind(n)} by ${d}. Give the quotient and the remainder.` : `Find ${ind(n)} ÷ ${d}.`;
      const steps = g <= 3 ? [`Share ${n} into ${d} equal groups`, `${d} × ${q} = ${n}`, `So ${n} ÷ ${d} = ${q}`] : [...longDiv(n, d).slice(0, 4), `Check: ${d} × ${ind(q)}${r ? ` + ${r}` : ''} = ${ind(n)}`];
      const nz = +String(q).replace(/0/g, '');
      const bb = build([q, r], [[q + 1, r], [q - 1, r], [nz, r], r ? [q, 0] : null, [q, r + 1 < d ? r + 1 : r - 1], [q * 10, r], [n - d, 0]], fmt, { ok: v => v[0] > 0 && v[1] >= 0 && v[1] < d, more: () => [q + R(-5, 5), R(0, d - 1) * (r ? 1 : 0)] });
      return Q(q_, bb, `Division is sharing into equal groups. ${ind(n)} ÷ ${d} gives ${ind(q)}${r ? ` with ${r} left over` : ''}, because ${d} × ${ind(q)}${r ? ` + ${r}` : ''} = ${ind(n)}.`, steps, { n, d },
        g <= 3 && n <= 40 ? { visual: { kind: 'count', emoji: EMO[it], n, groups: d } } : null);
    } });

  /* ---- 8. Money: totals, change, bills (Grades 1–5) ---- */
  const SHOP = ['a pencil', 'an eraser', 'a notebook', 'a kite', 'a ball', 'a toy car', 'a box of crayons', 'a bottle of water', 'a packet of biscuits', 'a storybook'];
  def({ id: 'money', name: 'Money: totals and change', subj: ['maths'], g: [1, 5], re: /money|coins and notes|change|bill|shop|paying|balance|deposit|cost of things/i, not: /paise|barter|piggy|fewest|closer look|making an amount|counting money|patterns|saving|using a balance|pan balance/i,
    make({ g }) {
      const cap = [0, 20, 100, 500, 2000, 2000][g], notes = [0, [10, 20], [50, 100], [100, 200, 500], [500, 2000], [500, 2000]][g];
      const t = g >= 2 ? pick(['total', 'change', 'qty']) : pick(['total', 'change']);
      const [n1] = two(); const [i1, i2] = shuffle(SHOP);
      let q, ans, steps, wr, exp;
      if (t === 'qty') {
        const k = R(2, g === 2 ? 5 : 9), p = R(2, Math.floor(cap / k / (g === 2 ? 1 : 2))); ans = k * p;
        q = `One ${i1.replace(/^an? /, '')} costs ₹${ind(p)}. What do ${k} of them cost?`;
        steps = [`Cost of ${k} = ${k} × cost of one`, `${k} × ₹${ind(p)} = ₹${ind(ans)}`]; wr = [k + p, ans + p, ans - p, p * (k + 1)];
        exp = `Multiply the price of one by the number bought.`;
      } else {
        const a = R(2, Math.floor(cap * .45)), b = R(2, Math.floor(cap * .45)), s = a + b;
        if (t === 'total') {
          ans = s; q = `${n1} buys ${i1} for ₹${ind(a)} and ${i2} for ₹${ind(b)}. How much does ${n1} spend in all?`;
          steps = g >= 3 ? [`Add the two prices`, `₹${ind(a)} + ₹${ind(b)} = ₹${ind(s)}`] : [`Add the prices: ₹${a} + ₹${b} = ₹${s}`, `Total spent is ₹${s}`];
          wr = [colAdd(a, b).noCarry, s + 10, s - 10, Math.abs(a - b), s + 1]; exp = `To find how much is spent, add the prices.`;
        } else {
          const note = notes.find(x => x > s) || notes[notes.length - 1]; if (note <= s) throw new Error('retry');
          ans = note - s; q = `${n1} buys ${i1} for ₹${ind(a)} and ${i2} for ₹${ind(b)}, and pays with a ₹${ind(note)} note. How much change does ${n1} get back?`;
          steps = [`Total cost: ₹${ind(a)} + ₹${ind(b)} = ₹${ind(s)}`, `Change: ₹${ind(note)} − ₹${ind(s)} = ₹${ind(ans)}`];
          wr = [s, note - a, note - b, ans + 10, ans - 10, colSub(note, s).noBorrow]; exp = `Change = money given − total cost.`;
        }
      }
      const bb = build(ans, wr, rs, { ok: v => v > 0 });
      return Q(q, bb, exp, steps, { t });
    } });

  /* ---- 9. Place value and expanded form (Grades 1–5) ---- */
  def({ id: 'place_value', name: 'Place value', subj: ['maths'], g: [1, 5], re: /place value|tens and ones|a ten and some ones|hundreds, tens|expanded form|packing sweets in 100s|slips of 100|place-value|arrow cards|tens, ones/i, not: /decimal|international|fewest clicks|adding|subtract|game/i,
    make({ g }) {
      const nd = [0, 2, 2, 3, 4, 6][g];
      let ds; do { ds = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9]).slice(0, nd); } while (!ds[0]);
      if (g >= 3 && nd >= 3 && Math.random() < .3) ds[R(1, nd - 1)] = 0;
      const N = +ds.join(''), D = digits(N);
      const t = g <= 2 ? pick(['make', 'pv']) : pick(['pv', 'pv', 'exp']);
      if (t === 'make') {
        const tn = D[1], on = D[0];
        const bb = build(N, [on * 10 + tn, tn + on, tn * 100 + on, tn * 10], ind, { ok: v => v > 0 && v !== N });
        return Q(`${tn} tens and ${on} ones make which number?`, bb, `${tn} tens is ${tn * 10}. ${tn * 10} and ${on} more is ${N}.`, [`${tn} tens = ${tn} × 10 = ${tn * 10}`, `${tn * 10} + ${on} = ${N}`], { t, N });
      }
      if (t === 'pv') {
        const idx = shuffle(D.map((x, i) => i).filter(i => D[i])).find(i => i > 0 || g <= 2) ?? 0, d = D[idx], val = d * 10 ** idx;
        const other = D.findIndex((x, i) => i !== idx && x);
        const bb = build(val, [d, d * 10 ** (idx + 1), idx ? d * 10 ** (idx - 1) : null, other >= 0 ? D[other] * 10 ** other : null, d * 10 ** (idx + 2)], ind, { ok: v => v > 0 });
        return Q(`What is the place value of the digit ${d} in ${ind(N)}?`, bb, `The place value of a digit is the digit times the value of its place. The face value is just ${d}.`,
          [`In ${ind(N)}, the digit ${d} is in the ${PL[idx]} place`, `Value: ${d} × ${ind(10 ** idx)} = ${ind(val)}`], { t, N, d, idx });
      }
      const terms = D.map((x, i) => x * 10 ** i).filter(Boolean).reverse();
      const fmtT = a => a.map(ind).join(' + ');
      const nz = D.map((x, i) => [x, i]).filter(x => x[0]).reverse();
      const sw = nz.length >= 2 ? (() => { const c = nz.map(x => x[0] * 10 ** x[1]); const [i, j] = [nz.length - 1, nz.length - 2]; c[i] = nz[i][0] * 10 ** nz[j][1]; c[j] = nz[j][0] * 10 ** nz[i][1]; return c; })() : null;
      const bigger = nz.map(x => x[0] * 10 ** (x[1] + (x[1] === nz[0][1] ? 1 : 0)));
      const bb = build(terms, [nz.map(x => x[0]), sw, bigger, nz.map(x => x[0] * 10 ** Math.max(0, x[1] - 1))], fmtT, { ok: a => a.reduce((s, x) => s + x, 0) !== N });
      return Q(`Which is the expanded form of ${ind(N)}?`, bb, `Expanded form writes each digit as its place value and adds them.`,
        [nz.map(x => `${x[0]} ${PL[x[1]]}`).join(', '), `Check: ${fmtT(terms)} = ${ind(N)}`], { t, N });
    } });

  /* ---- 10. Comparing and ordering numbers (Grades 1–5) ---- */
  def({ id: 'compare_num', name: 'Comparing numbers', subj: ['maths'], g: [1, 5], re: /compar|biggest|smallest|greatest|largest|in order|ordering|which number is more|more and less/i,
    not: /fraction|decimal|length|weight|capacit|angle|shape|expression|group|estimat|graph|distance|height|quantit|real life|without moving|routine|data|sizes|calendar|day|names|animal|tall|first|before|tables|items|1\/2/i,
    make({ g }) {
      const [lo, hi] = [[0, 0], [1, 20], [10, 99], [100, 999], [1000, 9999], [10000, 999999]][g];
      let nums;
      do { const base = R(lo, hi), ds = String(base).split(''); const set = new Set([base]);
        for (let k = 0; set.size < 4 && k < 50; k++) { const v = Math.random() < .6 && ds.length > 1 ? +shuffle(ds).join('') : base + R(-15, 15) * (g >= 4 ? 10 ** (g - 3) : 1); if (v >= lo && v <= hi) set.add(v); }
        nums = [...set]; } while (nums.length < 4);
      const big = Math.random() < .5, ans = big ? Math.max(...nums) : Math.min(...nums), srt = nums.slice().sort((a, b) => a - b);
      const opts = shuffle(nums), bb = { options: opts.map(ind), answer: opts.indexOf(ans), ans: ind(ans) };
      return Q(`Which number is the ${big ? 'greatest' : 'smallest'}?`, bb, `Compare the number of digits first. If they are the same, compare digit by digit from the left.`,
        [`Compare from the biggest place on the left`, `In order from smallest to greatest: ${srt.map(ind).join(' < ')}`, `The ${big ? 'greatest is the last' : 'smallest is the first'} one: ${ind(ans)}`], { big, nums });
    } });

  /* ---- 11. Skip counting / number patterns (Grades 1–5) ---- */
  def({ id: 'skip_count', name: 'Skip counting', subj: ['maths'], g: [1, 5], re: /skip count|counting in tens|count(ing)? backward|skip jumps|skip counting in big steps|^number patterns$|number patterns and the number line/i, not: /100 chart|growing/i,
    make({ g, title }) {
      const fromT = (title.match(/(\d+)s\b/g) || []).map(x => parseInt(x, 10));
      let st = /tens/i.test(title) ? 10 : fromT.length ? pick(fromT) : pick([[1, 2, 5, 10], [2, 3, 5, 10], [2, 3, 4, 5, 10, 25, 50, 100], [3, 4, 5, 6, 25, 50, 100], [5, 10, 25, 50, 100, 1000]][g - 1]);
      const back = /backward/i.test(title) || (g >= 2 && Math.random() < .3);
      const cap = [0, 100, 200, 1000, 5000, 100000][g];
      const len = 4; let a = R(back ? st * (len + 1) : 0, Math.max(st * (len + 2), cap - st * (len + 1))); if (Math.random() < .5) a -= a % st;
      if (!back && a + st * len > cap) a = cap - st * len - st; if (a < 0) a = 0;
      const sq = Array.from({ length: len }, (_, k) => back ? a - k * st : a + k * st);
      if (sq.some(x => x < 0)) throw new Error('retry');
      const last = sq[len - 1], nx = back ? last - st : last + st;
      const bb = build(nx, [back ? last + st : last - st, nx + 1, nx - 1, back ? last - 1 : last + 1, back ? nx - st : nx + st], ind, { ok: v => v >= 0 });
      return Q(`What comes next? ${sq.map(ind).join(', ')}, ___`, bb, `The numbers go ${back ? 'down' : 'up'} by ${st} each time.`,
        [back ? `Each number is ${st} less: ${ind(sq[0])} − ${ind(sq[1])} = ${st}` : `Each number is ${st} more: ${ind(sq[1])} − ${ind(sq[0])} = ${st}`, back ? `${ind(last)} − ${st} = ${ind(nx)}` : `${ind(last)} + ${st} = ${ind(nx)}`], { sq, nx });
    } });

  /* ---- 12. Even and odd (Grades 2–5) ---- */
  def({ id: 'even_odd', name: 'Even and odd', subj: ['maths'], g: [2, 5], re: /\beven\b|\bodd\b/i, not: /odd one out|odd-one|window|sums|puzzle|neighbours|making/i,
    make({ g }) {
      const hi = [0, 0, 99, 999, 9999, 99999][g], wantEven = Math.random() < .5, isE = n => n % 2 === 0;
      const set = new Set(); set.add((x => isE(x) === wantEven ? x : x + 1)(R(10, hi - 1)));
      while (set.size < 4) { const v = R(10, hi); if (isE(v) !== wantEven) set.add(v); }
      const nums = shuffle([...set]), ans = nums.find(x => isE(x) === wantEven);
      const bb = { options: nums.map(ind), answer: nums.indexOf(ans), ans: ind(ans) };
      return Q(`Which of these numbers is ${wantEven ? 'even' : 'odd'}?`, bb, `Only the ones digit decides: 0, 2, 4, 6, 8 means even; 1, 3, 5, 7, 9 means odd.`,
        [`Look at the ones digit of each number`, `${ind(ans)} ends in ${ans % 10}, so it is ${wantEven ? 'even' : 'odd'}`, `The others end in ${nums.filter(x => x !== ans).map(x => x % 10).join(', ')}, so they are ${wantEven ? 'odd' : 'even'}`], { want: wantEven ? 'even' : 'odd' });
    } });

  /* ---- 13. Rounding (Grades 4–6) ---- */
  def({ id: 'rounding', name: 'Rounding', subj: ['maths'], g: [4, 6], re: /\brounding\b|round to|round off/i, not: /round and|round things/i,
    make({ g, title }) {
      const opts = []; if (/\bten\b/i.test(title)) opts.push(10); if (/hundred/i.test(title)) opts.push(100); if (/thousand/i.test(title)) opts.push(1000); if (!opts.length) opts.push(10, 100, 1000);
      const p = pick(opts); let N; do { N = R(p * 2, g === 4 ? 9999 : 99999); } while (N % p === 0);
      const dn = N - N % p, up = dn + p, rd = Math.floor((N % p) / (p / 10)), r = rd >= 5 ? up : dn, pname = { 10: 'tens', 100: 'hundreds', 1000: 'thousands' }[p], rname = { 10: 'ones', 100: 'tens', 1000: 'hundreds' }[p];
      const bb = build(r, [rd >= 5 ? dn : up, N - N % (p * 10) + (N % (p * 10) >= p * 5 ? p * 10 : 0), N - N % (p / 10 || 1), r + p], ind, { ok: v => v > 0 && v !== N });
      return Q(`Round ${ind(N)} to the nearest ${p === 10 ? 'ten' : p === 100 ? 'hundred' : 'thousand'}.`, bb, `Rule: look at the digit just to the right of the ${pname} place. If it is 5 or more, round up; if it is less than 5, round down.`,
        [`The digit in the ${rname} place is ${rd}`, rd >= 5 ? `${rd} is 5 or more, so round up to ${ind(up)}` : `${rd} is less than 5, so round down to ${ind(dn)}`], { N, p });
    } });

  /* ---- 14. Fraction of a quantity (Grades 3–6) ---- */
  def({ id: 'frac_of', name: 'Fraction of a number', subj: ['maths'], g: [3, 6], re: /\bhalf\b|halves|quarter|of a (group|collection)|fractions? of|three quarters/i, not: /metre|litre|kilogram|folding|shapes|equal or not|more than half|circle|fractions of a whole|past|quarter to|mirror/i,
    make({ g }) {
      let a, b; if (g === 3) [a, b] = pick([[1, 2], [1, 4], [3, 4], [1, 2]]); else { b = R(2, 10); a = R(1, b - 1); while (gcd(a, b) > 1) a = R(1, b - 1); }
      const k = R(2, g === 3 ? 10 : 12), n = b * k, ans = a * k, it = pick(ITEMS), word = { '1/2': 'half', '1/4': 'one quarter', '3/4': 'three quarters' }[`${a}/${b}`];
      const q = `${word && g === 3 ? `What is ${word} of ${n} ${it}?` : `What is ${a}/${b} of ${n}?`}`;
      const steps = [`Split ${n} into ${b} equal parts: ${n} ÷ ${b} = ${k}`, ...(a > 1 ? [`Take ${a} parts: ${a} × ${k} = ${ans}`] : [`One part is ${k}`])];
      const bb = build(ans, [k, n - ans, ans + k, n * a, Math.floor(n / a) === n / a ? n / a : null], ind, { ok: v => v > 0 && v !== n });
      return Q(q, bb, `To find ${a}/${b} of a number, divide it into ${b} equal parts and take ${a} of them.`, steps, { a, b, n }, n <= 40 ? { visual: { kind: 'count', emoji: EMO[it], n, groups: b } } : null);
    } });

  /* ---- 15. Equivalent fractions and simplest form (Grades 4–7) ---- */
  def({ id: 'frac_simplify', name: 'Equivalent fractions', subj: ['maths'], g: [4, 7], re: /equivalent fraction|simplest form|same fraction, different|fraction wall|checking equal fractions|cancelling/i,
    make({ g }) {
      let p, q; do { q = R(3, 12); p = R(1, q - 1); } while (gcd(p, q) !== 1);
      const k = R(2, 9), a = p * k, b = q * k;
      if (g <= 4 || Math.random() < .4) {
        const m = R(2, 6), b2 = q * m, ans = p * m;
        const bb = build(ans, [p + (b2 - q), b2 / q, p * b2, ans + 1, ans - 1], ind, { ok: v => v > 0 });
        return Q(`Fill in the missing number: ${p}/${q} = ___/${b2}`, bb, `Multiply the top and the bottom by the same number to get an equivalent fraction.`,
          [`${q} × ${m} = ${b2}, so multiply the bottom by ${m}`, `Multiply the top by ${m} too: ${p} × ${m} = ${ans}`], { t: 'missing', p, q, b2 }, q <= 12 ? { visual: { kind: 'fraction', num: p, den: q } } : null);
      }
      const facs = []; for (let f = 2; f < k; f++) if (k % f === 0) facs.push(f);
      const f0 = facs.length ? pick(facs) : null, partial = f0 ? `${a / f0}/${b / f0}` : null;
      const bb = build(`${p}/${q}`, [partial, `${p}/${b}`, `${p}/${b - a + p}`, `${q}/${p}`, `${a}/${b}`], s => s);
      return Q(`Write ${a}/${b} in its simplest form.`, bb, `Divide the top and the bottom by their HCF. A fraction is in simplest form when 1 is the only common factor.`,
        [`HCF of ${a} and ${b} is ${k}`, `${a} ÷ ${k} = ${p}, ${b} ÷ ${k} = ${q}`], { t: 'simplest', a, b }, q <= 12 ? { visual: { kind: 'fraction', num: p, den: q } } : null);
    } });

  /* ---- 16. Comparing fractions (Grades 4–6) ---- */
  def({ id: 'frac_compare', name: 'Comparing fractions', subj: ['maths'], g: [4, 6], re: /comparing fractions|comparing: same top|same bottom|comparing unit fractions|< and >|comparing with 1/i,
    make() {
      const D_ = pick([[2, 3, 4, 6, 12], [2, 4, 8], [2, 4, 5, 10, 20], [3, 6, 9, 18], [2, 3, 6]]);
      const set = new Map(); let guard = 0;
      while (set.size < 4 && guard++ < 200) { const d = pick(D_), n = R(1, d - 1); const f = new Fr(n, d); set.set(f.p + '/' + f.q, f); }
      if (set.size < 4) throw new Error('retry');
      const fr = shuffle([...set.values()]), big = Math.random() < .5, L = fr.reduce((s, f) => lcm(s, f.q), 1);
      const ans = fr.reduce((m, f) => (big ? f.v > m.v : f.v < m.v) ? f : m);
      const opts = fr.map(fs), bb = { options: opts, answer: opts.indexOf(fs(ans)), ans: fs(ans) };
      return Q(`Which fraction is the ${big ? 'greatest' : 'smallest'}?`, bb, `Give all the fractions the same denominator, then compare the numerators.`,
        [`Common denominator: LCM of ${fr.map(f => f.q).join(', ')} is ${L}`, fr.map(f => `${fs(f)} = ${f.p * L / f.q}/${L}`).join(', '), `The ${big ? 'largest' : 'smallest'} numerator is ${ans.p * L / ans.q}`], { big });
    } });

  /* ---- 17. Adding and subtracting fractions (Grades 5–7) ---- */
  def({ id: 'frac_addsub', name: 'Adding and subtracting fractions', subj: ['maths'], g: [5, 7], re: /adding and subtracting fractions|models for adding|adding fractions|add(ing)? .*fraction/i,
    make() {
      const nf = () => { let q = R(2, 12), p = R(1, q - 1); while (gcd(p, q) > 1) p = R(1, q - 1); return [p, q]; };
      let [a, b] = nf(), [c, d] = nf(); const sub = Math.random() < .45;
      if (sub && a / b < c / d) [a, b, c, d] = [c, d, a, b];
      if (sub && a * d === c * b) throw new Error('retry');
      const L = lcm(b, d), A = a * L / b, C = c * L / d, top = sub ? A - C : A + C, res = new Fr(top, L), op = sub ? '−' : '+';
      const steps = b === d ? [`Same denominator, so ${sub ? 'subtract' : 'add'} the numerators: ${a} ${op} ${c} = ${top}`, `${top}/${L}${res.q !== L ? ` = ${fs(res)}` : ' is already in simplest form'}`]
        : [`LCM of ${b} and ${d} is ${L}`, `${a}/${b} = ${A}/${L}, ${c}/${d} = ${C}/${L}`, `${A}/${L} ${op} ${C}/${L} = ${top}/${L}`, ...(res.q !== L ? [`Simplify: ${top}/${L} = ${fs(res)}`] : [])];
      const wr = [new Fr(sub ? Math.abs(a - c) || 1 : a + c, sub ? Math.abs(b - d) || 1 : b + d), new Fr(sub ? Math.abs(a - c) || 1 : a + c, L), new Fr(sub ? A + C : Math.abs(A - C) || 1, L), new Fr(a * c, b * d)];
      const bb = build(res, wr, fs, { ok: v => v.p > 0 && !v.eq(res) });
      return Q(`Work out ${a}/${b} ${op} ${c}/${d}. Give the answer in simplest form.`, bb, `Fractions can be ${sub ? 'subtracted' : 'added'} only when the denominators are the same. Never ${sub ? 'subtract' : 'add'} the denominators.`, steps, { a, b, c, d, sub });
    } });

  /* ---- 18. Multiplying and dividing fractions (Grades 7–8) ---- */
  def({ id: 'frac_muldiv', name: 'Multiplying and dividing fractions', subj: ['maths'], g: [7, 8], re: /multiplying fractions|dividing fractions|fraction multiplication|fraction problems in daily life|division as the inverse/i,
    make({ title }) {
      const nf = () => { let q = R(2, 10), p = R(1, 9); while (gcd(p, q) > 1 || p === q) p = R(1, 9); return [p, q]; };
      const [a, b] = nf(), [c, d] = nf(), div = /divid|inverse/i.test(title) ? true : /multipl/i.test(title) ? false : Math.random() < .5;
      const res = div ? new Fr(a * d, b * c) : new Fr(a * c, b * d);
      const steps = div ? [`Dividing by ${c}/${d} is multiplying by ${d}/${c}`, `${a}/${b} × ${d}/${c} = ${a * d}/${b * c}`, ...(res.q !== b * c ? [`Simplify: ${a * d}/${b * c} = ${fs(res)}`] : [])]
        : [`Multiply the tops: ${a} × ${c} = ${a * c}`, `Multiply the bottoms: ${b} × ${d} = ${b * d}`, ...(res.q !== b * d ? [`Simplify: ${a * c}/${b * d} = ${fs(res)}`] : [])];
      const wr = div ? [new Fr(a * c, b * d), new Fr(b * c, a * d), new Fr(a + d, b + c)] : [new Fr(a * d, b * c), new Fr(a + c, b + d), new Fr(a * c, b + d)];
      const bb = build(res, wr, fs, { ok: v => v.p > 0 && !v.eq(res) });
      return Q(`Work out ${a}/${b} ${div ? '÷' : '×'} ${c}/${d}. Give the answer in simplest form.`, bb, div ? `To divide by a fraction, multiply by its reciprocal (flip the second fraction).` : `Multiply numerator by numerator and denominator by denominator, then simplify.`, steps, { a, b, c, d, div });
    } });

  /* ---- 19. Adding and subtracting decimals (Grades 5–8) ---- */
  def({ id: 'dec_addsub', name: 'Adding and subtracting decimals', subj: ['maths'], g: [5, 8], re: /adding.*decimal|subtracting decimal|adding, subtracting and ordering tenths|adding and subtracting decimals|decimals with care/i,
    make() {
      const da = R(1, 2), db = R(1, 2), dp = Math.max(da, db), S = 10 ** dp;
      const ia = R(10 ** da + 1, 60 * 10 ** da), ib = R(10 ** db + 1, 40 * 10 ** db), A = new Fr(ia, 10 ** da), B = new Fr(ib, 10 ** db);
      let sub = Math.random() < .45, X = A, Y = B; if (sub && A.v < B.v) [X, Y] = [B, A]; if (sub && X.eq(Y)) throw new Error('retry');
      const res = sub ? X.sub(Y) : X.add(Y), pad = f => { const s = dec(f); const [i, fr = ''] = s.split('.'); return i + '.' + fr.padEnd(dp, '0'); }, op = sub ? '−' : '+';
      const iX = X.mul(S).p, iY = Y.mul(S).p, unit = pick(['kg', 'km', 'L', 'm']);
      const raw = s => +dec(s).replace(/[.,]/g, ''), wrongAlign = new Fr(sub ? Math.abs(raw(X) - raw(Y)) : raw(X) + raw(Y), S);
      const fmt = v => `${dec(v)} ${unit}`;
      const bb = build(res, [wrongAlign, res.mul(10), res.div(10), res.add(new Fr(1, 10)), res.sub(new Fr(1, 10)), res.add(1)], fmt, { ok: v => v.p > 0 });
      const [n1] = two();
      const q = sub ? `${n1} had ${dec(X)} ${unit} and used ${dec(Y)} ${unit}. How much is left?` : `${n1} has ${dec(X)} ${unit} and gets ${dec(Y)} ${unit} more. How much is that in all?`;
      return Q(q, bb, `Line up the decimal points (add zeros so both have ${dp} decimal place${dp > 1 ? 's' : ''}), then ${sub ? 'subtract' : 'add'} like whole numbers.`,
        [`Write both with ${dp} decimal place${dp > 1 ? 's' : ''}: ${pad(X)} and ${pad(Y)}`, `Work with whole ${dp > 1 ? 'hundredths' : 'tenths'}: ${ind(iX)} ${op} ${ind(iY)} = ${ind(res.mul(S).p)}`, `Put the point back ${dp} place${dp > 1 ? 's' : ''} from the right: ${dec(res)}`], { x: dec(X), y: dec(Y), sub, unit });
    } });

  /* ---- 20. Multiplying and dividing decimals (Grades 6–8) ---- */
  def({ id: 'dec_muldiv', name: 'Multiplying and dividing decimals', subj: ['maths'], g: [6, 8], re: /multiplying decimals|decimal products|dividing decimals|dividing by a decimal|tenths times tenths/i,
    make({ title }) {
      const t = /dividing by a decimal/i.test(title) ? 'divdec' : /dividing/i.test(title) ? 'divwhole' : /multipl|products|times/i.test(title) ? 'mul' : pick(['mul', 'divwhole', 'divdec']);
      if (t === 'mul') {
        const da = R(1, 2), db = R(0, 1), ia = R(11, 99), ib = R(2, db ? 99 : 9); if (ia % 10 === 0 || (db && ib % 10 === 0)) throw new Error('retry');
        const A = new Fr(ia, 10 ** da), B = new Fr(ib, 10 ** db), res = A.mul(B), dp = da + db;
        const bb = build(res, [res.mul(10), res.div(10), A.add(B), res.mul(100)], v => dec(v, 6), { ok: v => v.p > 0 });
        return Q(`Work out ${dec(A)} × ${dec(B)}.`, bb, `Multiply as whole numbers, then count the decimal places in both numbers and put that many in the answer.`,
          [`Ignore the points: ${ia} × ${ib} = ${ind(ia * ib)}`, `Decimal places: ${da} + ${db} = ${dp}`, `Put ${dp} decimal place${dp > 1 ? 's' : ''} in ${ind(ia * ib)}: ${dec(res, 6)}`], { t, a: dec(A), b: dec(B) });
      }
      if (t === 'divwhole') {
        const n = R(2, 9), qd = R(11, 999), dp = R(1, 2), Qv = new Fr(qd, 10 ** dp), A = Qv.mul(n);
        if (qd % 10 === 0) throw new Error('retry');
        const bb = build(Qv, [Qv.mul(10), Qv.div(10), A.sub(n), Qv.add(1)], v => dec(v, 6), { ok: v => v.p > 0 });
        return Q(`Work out ${dec(A)} ÷ ${n}.`, bb, `Divide as if there were no point, then keep the same number of decimal places as in ${dec(A)}.`,
          [`Ignore the point: ${ind(A.mul(10 ** dp).p)} ÷ ${n} = ${ind(qd)}`, `Put the point back ${dp} place${dp > 1 ? 's' : ''} from the right: ${dec(Qv)}`, `Check: ${dec(Qv)} × ${n} = ${dec(A)}`], { t, a: dec(A), b: n });
      }
      const bi = R(2, 9), B = new Fr(bi, 10), qv = R(2, 40), A = B.mul(qv);
      const bb = build(qv, [qv / 10, qv * 10, A.mul(B), qv + 1], v => nm(v), { ok: v => F(v).p > 0 });
      return Q(`Work out ${dec(A)} ÷ ${dec(B)}.`, bb, `Multiply both numbers by 10 so that you divide by a whole number. The answer does not change.`,
        [`Multiply both by 10: ${dec(A)} ÷ ${dec(B)} = ${dec(A.mul(10))} ÷ ${bi}`, `${dec(A.mul(10))} ÷ ${bi} = ${qv}`], { t, a: dec(A), b: dec(B) });
    } });

  /* ---- 21. HCF and LCM (Grades 4–10) ---- */
  def({ id: 'hcf_lcm', name: 'HCF and LCM', subj: ['maths'], g: [4, 10], re: /\bhcf\b|\blcm\b|common factors|common multiples|common landing|where jumpers meet|who lands first|meeting times/i, not: /patterns|ladder|mystery|puzzle|1-to-10|irrational|formulas/i,
    make({ g, title }) {
      const wantH = /hcf|common factors/i.test(title), wantL = /lcm|common multiples|landing|jumpers|lands|meeting/i.test(title);
      let t = wantH && !wantL ? 'hcf' : wantL && !wantH ? 'lcm' : pick(['hcf', 'lcm']);
      if (g === 10 && Math.random() < .35) t = 'prod';
      const small = g <= 5;
      let h, m, n; do { h = small ? R(1, 4) : R(2, 15); m = R(2, small ? 6 : 9); n = R(2, small ? 6 : 9); } while (gcd(m, n) !== 1 || m === n || h * m * n > (small ? 60 : 400) || (t === 'hcf' && h === 1));
      const a = h * m, b = h * n, L = h * m * n;
      if (t === 'prod') {
        const bb = build(b, [L / h, a, h * L, L - a], ind, { ok: v => v > 0 });
        return Q(`The HCF of two numbers is ${h} and their LCM is ${ind(L)}. One number is ${a}. Find the other number.`, bb, `For two numbers, HCF × LCM = product of the two numbers.`,
          [`HCF × LCM = ${h} × ${ind(L)} = ${ind(h * L)}`, `Other number = ${ind(h * L)} ÷ ${a} = ${b}`], { t, h, L, a });
      }
      const story = Math.random() < .4, isH = t === 'hcf', ans = isH ? h : L;
      const q = story ? (isH ? `Two ribbons are ${a} cm and ${b} cm long. They must be cut into pieces of the same length with nothing left over. What is the longest possible piece?` : `One bell rings every ${a} minutes and another every ${b} minutes. They ring together now. After how many minutes will they ring together again?`)
        : `Find the ${isH ? 'HCF' : 'LCM'} of ${a} and ${b}.`;
      const unit = story ? (isH ? ' cm' : ' minutes') : '';
      let steps;
      if (small && !isH) { const ma = Array.from({ length: Math.min(L / a, 8) }, (_, k) => a * (k + 1)), mb = Array.from({ length: Math.min(L / b, 8) }, (_, k) => b * (k + 1)); steps = [`Multiples of ${a}: ${ma.join(', ')}`, `Multiples of ${b}: ${mb.join(', ')}`, `The first common multiple is ${L}`]; }
      else steps = [(isPrime(a) ? `${a} is a prime number` : `${a} = ${pfStr(a)}`), (isPrime(b) ? `${b} is a prime number` : `${b} = ${pfStr(b)}`), isH ? (isPrime(h) ? `Common prime factor: ${h}, so HCF = ${h}` : `Common prime factors: ${pfStr(h)} = ${h}`) : `LCM = ${pfStr(L)} = ${ind(L)}`];
      const bb = build(ans, [isH ? L : h, a * b, Math.min(a, b), isH ? h * 2 : L * 2, Math.abs(a - b)], v => ind(v) + unit, { ok: v => v > 0 && v !== ans });
      return Q(q, bb, isH ? `The HCF is the biggest number that divides both ${a} and ${b} exactly.` : `The LCM is the smallest number that both ${a} and ${b} divide into exactly.`, steps, { t, a, b });
    } });

  /* ---- 22. Primes, factors and prime factorisation (Grades 5–10) ---- */
  def({ id: 'primes', name: 'Primes and factors', subj: ['maths'], g: [5, 10], re: /prime|factors?\b|factor pairs|fundamental theorem/i, not: /common|remainder|scale|riddle|puzzle|twin|odd|identit|algebra|polynomial|splitting|tiles|zeros|gcd|mystery|perfect squares|making formulas|jackpot|testing|multiplier|true or false/i,
    make({ g, title }) {
      const t = /factoris|fundamental/i.test(title) ? 'pf' : /prime/i.test(title) ? pick(['which', 'pf']) : pick(['count', 'count', 'which']);
      if (t === 'which') {
        const ps = []; for (let k = 11; k < 200; k++) if (isPrime(k)) ps.push(k);
        const cs = []; for (let k = 21; k < 200; k += 2) if (!isPrime(k) && k % 5) cs.push(k);
        const p = pick(ps), list = shuffle([p, ...shuffle(cs).slice(0, 3)]);
        const show = list.filter(x => x !== p).map(x => { const f = pfList(x); return `${x} = ${f[0]} × ${x / f[0]}`; }).join(', ');
        const bb = { options: list.map(ind), answer: list.indexOf(p), ans: ind(p) };
        return Q(`Which of these is a prime number?`, bb, `A prime number has exactly two factors: 1 and itself.`, [`Look for a factor of each number: ${show}`, `${p} has no factor other than 1 and ${p}`], { t, list });
      }
      if (t === 'count') {
        const N = pick([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 44, 45, 48, 50, 54, 56, 60, 63, 64, 66, 70, 72, 75, 80, 84, 90, 96, 98, 100]);
        const fs_ = []; for (let k = 1; k <= N; k++) if (N % k === 0) fs_.push(k); const pairs = fs_.filter(k => k * k <= N).map(k => `${k} × ${N / k}`);
        const c = fs_.length, bb = build(c, [c - 1, c + 1, pairs.length, c - 2, c + 2], ind, { ok: v => v > 0 });
        return Q(`How many factors does ${N} have?`, bb, `Find factor pairs that multiply to ${N}. Every number in a pair is a factor.`,
          [`Factor pairs of ${N}: ${pairs.join(', ')}`, `Factors: ${fs_.join(', ')}`, `Count them: ${c} factors`], { t, N });
      }
      let N; do { N = [2, 2, 2, 3, 3, 5, 7, 11, 13].sort(() => Math.random() - .5).slice(0, R(3, 5)).reduce((s, x) => s * x, 1); } while (N > (g <= 6 ? 500 : 3000) || N < 24);
      const f = pfList(N), useP = g >= 7, show = useP ? pfPow : pfStr;
      const chunks = []; let cur = N; const ps = [...new Set(f)];
      ps.forEach(p => { const part = []; while (cur % p === 0) { part.push(`${ind(cur)} ÷ ${p} = ${ind(cur / p)}`); cur /= p; } chunks.push(part.join(', ')); });
      while (chunks.length > 4) { const x = chunks.pop(); chunks[chunks.length - 1] += ', ' + x; }
      const join = a => a.join(' × ');
      const comp = f.length >= 2 ? (() => { const x = f.slice(); const y = x.splice(0, 2); return join([y[0] * y[1], ...x].sort((p, q) => p - q)); })() : null;
      const drop = join(f.slice(1)), extra = join([...f, 2].sort((p, q) => p - q)), swap = join(f.map((x, i) => i === f.length - 1 ? (x === 2 ? 3 : 2) : x).sort((p, q) => p - q));
      const pw = x => useP ? pfPow(x.split(' × ').reduce((s, y) => s * +y, 1)) : x;
      const fmtF = s => s;
      const cands = [comp, pw(drop), pw(extra), pw(swap)].filter(Boolean);
      const bb = build(show(N), cands.map(c => c), fmtF);
      return Q(`Which is the prime factorisation of ${ind(N)}?`, bb, `Keep dividing by the smallest prime that works until you reach 1. Every factor in the answer must be prime.`, chunks, { t, N });
    } });

  /* ---- 23. Divisibility rules (Grades 4–8) ---- */
  def({ id: 'divisibility', name: 'Divisibility rules', subj: ['maths'], g: [4, 8], re: /divisib/i, not: /proposition|why/i,
    make({ title }) {
      let ks = titleNums(title).filter(x => [2, 3, 4, 5, 6, 8, 9, 10, 11].includes(x)); if (!ks.length) ks = [2, 3, 4, 5, 6, 8, 9, 10, 11];
      const k = pick(ks), lo = 1000, hi = 99999;
      let c; do { c = R(lo, hi); c -= c % k; } while (c < lo);
      const set = new Set([c]); while (set.size < 4) { const v = c + R(1, 40) * pick([-1, 1]); if (v % k && v > 0) set.add(v); }
      const list = shuffle([...set]), D_ = digits(c), ds = D_.slice().reverse();
      const rule = { 2: 'the last digit is even', 5: 'the last digit is 0 or 5', 10: 'the last digit is 0', 3: 'the digit sum is a multiple of 3', 9: 'the digit sum is a multiple of 9', 4: 'the number formed by the last two digits is divisible by 4', 8: 'the number formed by the last three digits is divisible by 8', 6: 'it is divisible by both 2 and 3', 11: 'the alternating digit sum (from the right) is a multiple of 11' }[k];
      let chk;
      if ([2, 5, 10].includes(k)) chk = `${ind(c)} ends in ${c % 10}`;
      else if (k === 3 || k === 9 || k === 6) { const s = ds.reduce((a, b) => a + b, 0); chk = `Digit sum of ${ind(c)}: ${ds.join(' + ')} = ${s}${k === 6 ? `, and ${ind(c)} ends in ${c % 10} (even)` : ''}`; }
      else if (k === 4) chk = `Last two digits: ${c % 100} ÷ 4 = ${(c % 100) / 4}`;
      else if (k === 8) chk = `Last three digits: ${c % 1000} ÷ 8 = ${(c % 1000) / 8}`;
      else { const alt = D_.reduce((s, x, i) => s + (i % 2 ? -x : x), 0); chk = `${D_.map((x, i) => (i ? (i % 2 ? ' − ' : ' + ') : '') + x).join('')} = ${ind(alt)}`; }
      const bb = { options: list.map(ind), answer: list.indexOf(c), ans: ind(c) };
      return Q(`Which of these numbers is divisible by ${k}?`, bb, `A number is divisible by ${k} when ${rule}.`, [`Rule for ${k}: ${rule}`, chk, `So ${ind(c)} is divisible by ${k}; the others are not`], { k, list });
    } });

  /* ---- 24. Adding and subtracting integers (Grades 6–8) ---- */
  def({ id: 'int_addsub', name: 'Adding and subtracting integers', subj: ['maths'], g: [6, 8], re: /adding and subtracting integers|integer recap|integers on a number line|lift buttons|positive and negative tokens|mine levels|integers: fortunes/i,
    make({ g }) {
      const M = g === 6 ? 30 : 100; let a = R(-M, M), b = R(-M, M); if (!a || !b) throw new Error('retry');
      const sub = Math.random() < .45, r = sub ? a - b : a + b, story = Math.random() < .3 && !sub;
      const q = story ? `At night the temperature in Leh was ${ind(a)} °C. By noon it changed by ${b > 0 ? '+' : ''}${ind(b)} °C. What was the noon temperature?` : `Work out ${pn(a)} ${sub ? '−' : '+'} ${pn(b)}.`;
      const steps = [];
      const ea = sub ? -b : b;
      if (sub) steps.push(`Subtracting ${pn(b)} is the same as adding ${pn(-b)}`);
      if ((a < 0) !== (ea < 0)) steps.push(`Signs differ, so subtract the sizes: ${Math.max(Math.abs(a), Math.abs(ea))} − ${Math.min(Math.abs(a), Math.abs(ea))} = ${Math.abs(r)}`, `Keep the sign of the number with the bigger size`);
      else steps.push(`Same signs, so add the sizes: ${Math.abs(a)} + ${Math.abs(ea)} = ${Math.abs(a) + Math.abs(ea)}`, `Keep the common sign`);
      steps.push(`${pn(a)} + ${pn(ea)} = ${ind(r)}`);
      const fmt = v => ind(v) + (story ? ' °C' : '');
      const bb = build(r, [-r, sub ? a + b : a - b, Math.abs(a) + Math.abs(b), -(Math.abs(a) + Math.abs(b)), r + 1, r - 1], fmt);
      return Q(q, bb, `On a number line, adding a positive number moves right and adding a negative number moves left. Subtracting a number means adding its opposite.`, steps.slice(0, 5), { a, b, sub });
    } });

  /* ---- 25. Multiplying and dividing integers (Grade 7–8) ---- */
  def({ id: 'int_muldiv', name: 'Multiplying and dividing integers', subj: ['maths'], g: [7, 8], re: /multiplying integers|dividing integers|brahmagupta's rules|tokens, inverses and multiplying|properties of integers/i,
    make({ title }) {
      const div = /dividing/i.test(title) ? true : /multiplying/i.test(title) ? false : Math.random() < .5;
      let a = R(2, 15) * pick([-1, 1]), b = R(2, 15) * pick([-1, 1]); const p = a * b;
      const [x, y, r] = div ? [p, a, b] : [a, b, p];
      const neg = (x < 0) !== (y < 0), sz = Math.abs(r);
      const bb = build(r, [-r, div ? x * y : x + y, x - y, r + (div ? 1 : y)], ind);
      return Q(`Work out ${pn(x)} ${div ? '÷' : '×'} ${pn(y)}.`, bb, `Same signs give a positive answer; different signs give a negative answer.`,
        [`Signs: ${x < 0 ? 'negative' : 'positive'} ${div ? '÷' : '×'} ${y < 0 ? 'negative' : 'positive'} gives ${neg ? 'negative' : 'positive'}`, `Sizes: ${Math.abs(x)} ${div ? '÷' : '×'} ${Math.abs(y)} = ${sz}`, `${pn(x)} ${div ? '÷' : '×'} ${pn(y)} = ${ind(r)}`], { x, y, div });
    } });

  /* ---- 26. Exponents and laws of exponents (Grades 7–9) ---- */
  def({ id: 'exponents', name: 'Exponents', subj: ['maths'], g: [7, 9], re: /exponent|power play|exponential form|powers in stories/i, not: /scientific/i,
    make({ title }) {
      const t = /negative|zero/i.test(title) ? pick(['neg', 'laws']) : /laws|dividing/i.test(title) ? pick(['laws', 'pow']) : pick(['val', 'laws', 'pow', 'neg']);
      const a = pick([2, 3, 5, 7, 10]);
      if (t === 'val') {
        const b = pick([2, 3, 4, 5]), n = b === 2 ? R(3, 10) : b === 3 ? R(2, 6) : R(2, 4), v = b ** n;
        const bb = build(v, [b * n, n ** b, v * b, v / b, b + n], ind, { ok: x => Number.isInteger(x) && x > 0 && x !== v });
        return Q(`What is the value of ${b}${sup(n)}?`, bb, `${b}${sup(n)} means ${b} multiplied by itself ${n} times, not ${b} × ${n}.`, [`${b}${sup(n)} = ${Array(n).fill(b).join(' × ')} = ${ind(v)}`], { t, b, n });
      }
      if (t === 'neg') {
        const n = a === 10 ? R(1, 4) : R(1, 3), v = new Fr(1, a ** n);
        const bb = build(v, [new Fr(-(a ** n)), new Fr(-a * n), new Fr(1, a * n), new Fr(a ** n)], fs, { ok: x => !x.eq(v) });
        return Q(`What is the value of ${a}${sup(-n)}?`, bb, `A negative exponent means the reciprocal: a⁻ⁿ = 1/aⁿ.`, [`${a}${sup(-n)} = 1/${a}${sup(n)}`, `${a}${sup(n)} = ${ind(a ** n)}`], { t, a, n: -n });
      }
      const m = R(2, 9), n = R(2, 9);
      if (t === 'pow') {
        const k = m * n, bb = build(k, [m + n, k + m, k - 1, Math.abs(m - n)], e => a + sup(e), { ok: e => e > 0 && e !== k });
        return Q(`Simplify (${a}${sup(m)})${sup(n)}.`, bb, `A power of a power: multiply the exponents.`, [`(aᵐ)ⁿ = a to the power m × n`, `Exponent: ${m} × ${n} = ${k}`], { t, a, m, n });
      }
      const p = R(1, m + n - 1), k = m + n - p;
      const bb = build(k, [m + n + p, m * n - p, m - n + p, k + 1, k - 1], e => a + sup(e), { ok: e => e !== k });
      return Q(`Simplify ${a}${sup(m)} × ${a}${sup(n)} ÷ ${a}${sup(p)}.`, bb, `With the same base: add the exponents when multiplying and subtract them when dividing.`,
        [`Multiplying: add the exponents: ${m} + ${n} = ${m + n}`, `Dividing: subtract: ${m + n} − ${p} = ${k}`], { t, a, m, n, p });
    } });

  /* ---- 27. Squares, square roots, cubes, cube roots (Grades 7–9) ---- */
  def({ id: 'squares', name: 'Squares and roots', subj: ['maths'], g: [7, 9], re: /square numbers|square roots?|cubes, cube roots|cubes of negatives|perfect cube|quick cube roots|squares: table/i,
    make({ title }) {
      const cube = /cube/i.test(title) && (!/square/i.test(title) || Math.random() < .5), root = /root/i.test(title) ? Math.random() < .7 : Math.random() < .4;
      if (!cube && !root) { const n = R(11, 45), v = n * n; const bb = build(v, [2 * n, v + n, (n + 1) ** 2, (n - 1) ** 2, v + 10], ind);
        return Q(`What is ${n}²?`, bb, `${n}² means ${n} × ${n}.`, [`${n}² = ${n} × ${n} = ${ind(v)}`, `Check the last digit: ${n % 10} × ${n % 10} = ${(n % 10) ** 2}, so it ends in ${v % 10}`], { t: 'sq', n }); }
      if (!cube) { const n = pick([12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 28, 30, 32, 35, 36, 40, 42, 44, 45, 48]), v = n * n;
        const bb = build(n, [v / 2, n + 1, n - 1, n * 2, Math.round(v / 10)], ind, { ok: x => Number.isInteger(x) && x > 0 && x !== n });
        return Q(`Find √${ind(v)}.`, bb, `Group the prime factors in pairs; one factor from each pair gives the square root.`, [`${ind(v)} = ${pfList(v).length > 6 ? pfPow(v) : pfStr(v)}`, `One from each pair: ${pfStr(n)} = ${n}`, `Check: ${n} × ${n} = ${ind(v)}`], { t: 'sqrt', v }); }
      if (!root) { const n = R(2, 15) * (/negative/i.test(title) && Math.random() < .5 ? -1 : 1), v = n ** 3;
        const bb = build(v, [3 * n, n * n, -v, (n + 1) ** 3, v + n], ind, { ok: x => x !== v });
        return Q(`What is ${pn(n)}³?`, bb, `${pn(n)}³ = ${pn(n)} × ${pn(n)} × ${pn(n)}. A negative number cubed stays negative.`, [`${pn(n)}³ = ${pn(n)} × ${pn(n)} × ${pn(n)} = ${ind(v)}`], { t: 'cube', n }); }
      const n = R(2, 20), v = n ** 3;
      const bb = build(n, [Math.round(v / 3), n + 1, n - 1, n * n], ind, { ok: x => x > 0 && x !== n });
      return Q(`Find the cube root of ${ind(v)}.`, bb, `Group the prime factors in threes; one from each group gives the cube root.`, [`${ind(v)} = ${pfList(v).length > 6 ? pfPow(v) : pfStr(v)}`, `Check: ${n} × ${n} × ${n} = ${ind(v)}`], { t: 'cbrt', v });
    } });

  /* ---- 28. Scientific notation (Grades 8–11, maths/physics/chemistry) ---- */
  def({ id: 'sci_notation', name: 'Scientific notation', subj: ['maths', 'physics', 'chemistry'], g: [8, 11], re: /scientific notation/i,
    make() {
      const sig = R(2, 4); let m; do { m = R(10 ** (sig - 1), 10 ** sig - 1); } while (m % 10 === 0);
      const small = Math.random() < .4, e = small ? -R(2, 6) : R(4, 9);
      const M = new Fr(m, 10 ** (sig - 1)), val = e >= 0 ? M.mul(10 ** e) : M.div(10 ** -e);
      const fmtS = ([mm, ee]) => `${dec(mm)} × 10${sup(ee)}`;
      const plain = dec(val, 12);
      const bb = build([M, e], [[M, e + 1], [M, e - 1], [M.mul(10), e - 1], [M, -e]], fmtS);
      return Q(`Write ${plain} in scientific notation.`, bb, `Scientific notation is a × 10ⁿ with 1 ≤ a < 10. Count how many places the decimal point moves.`,
        [`Put the decimal point after the first non-zero digit: ${dec(M)}`, `The point moves ${Math.abs(e)} places to the ${e > 0 ? 'left' : 'right'}, so the power is ${ind(e)}`, `Check: ${dec(M)} × 10${sup(e)} = ${plain}`], { m: dec(M), e });
    } });

  /* ---- 29. Order of operations / brackets (Grades 6–8) ---- */
  def({ id: 'bodmas', name: 'Order of operations', subj: ['maths'], g: [6, 8], re: /order of operations|brackets|writing and evaluating expressions|arithmetic expressions/i, not: /removing|tinkering|hitting|puzzle/i,
    make() {
      const t = R(1, 5); let e, steps, ltr, v;
      const a = R(2, 20), b = R(2, 12), c = R(2, 9), d = R(2, 9);
      if (t === 1) { e = `${a} + ${b} × ${c}`; v = a + b * c; steps = [`Multiply first: ${b} × ${c} = ${b * c}`, `Then add: ${a} + ${b * c} = ${v}`]; ltr = (a + b) * c; }
      else if (t === 2) { e = `(${a} + ${b}) × ${c}`; v = (a + b) * c; steps = [`Brackets first: ${a} + ${b} = ${a + b}`, `Then multiply: ${a + b} × ${c} = ${v}`]; ltr = a + b * c; }
      else if (t === 3) { const x = c * d + R(1, 30); e = `${x} − ${c} × ${d} + ${b}`; v = x - c * d + b; steps = [`Multiply first: ${c} × ${d} = ${c * d}`, `Then left to right: ${x} − ${c * d} = ${x - c * d}, ${x - c * d} + ${b} = ${v}`]; ltr = (x - c) * d + b; }
      else if (t === 4) { const y = c * d; e = `${a} + ${y} ÷ ${c} × ${b}`; v = a + d * b; steps = [`÷ and × from left to right: ${y} ÷ ${c} = ${d}, ${d} × ${b} = ${d * b}`, `Then add: ${a} + ${d * b} = ${v}`]; ltr = (a + y) / c * b; }
      else { const s = c * R(2, 6) - b; if (s <= 0) throw new Error('retry'); e = `${a} × (${s} + ${b}) ÷ ${c}`; v = a * (s + b) / c; steps = [`Brackets first: ${s} + ${b} = ${s + b}`, `Then left to right: ${a} × ${s + b} = ${a * (s + b)}, ${a * (s + b)} ÷ ${c} = ${v}`]; ltr = a * s + b / c; }
      if (!Number.isInteger(v) || v < 0) throw new Error('retry');
      const bb = build(v, [ltr, v + c, v - c, v * 2], ind, { ok: x => Number.isInteger(x) && x >= 0 });
      return Q(`Find the value of ${e}.`, bb, `Order: brackets first, then × and ÷ from left to right, then + and − from left to right.`, steps, { e });
    } });

  /* ---- 30. Linear equations in one variable (Grades 6–9) ---- */
  def({ id: 'linear_eq', name: 'Linear equations', subj: ['maths'], g: [6, 9], re: /equation|zeros? of a linear|balance puzzles|guess-and-check|finding the unknown/i,
    not: /two variables|pair|quadratic|chemical|differential|kinematic|motion|gas|continuity|lens|mirror|nernst|equation of|wave|maxwell|schr|identit|homogeneous|lines?\b|graph|no solutions|history|machines|mistake|squares|polynomials/i,
    make({ g, title }) {
      const negOK = g >= 8 || /negative/i.test(title);
      const t = /word problem/i.test(title) ? 'word' : /both sides/i.test(title) ? 'both' : /zeros? of a linear/i.test(title) ? 'zero' : pick(g >= 8 ? ['one', 'both', 'word'] : ['one', 'one', 'word']);
      const fx = v => `x = ${fs(v)}`;
      if (t === 'zero') {
        let a = R(2, 9) * pick([-1, 1]), b = R(1, 15) * pick([-1, 1]); const z = new Fr(-b, a);
        const bb = build(z, [new Fr(b, a), new Fr(-a, b), new Fr(a, b), z.add(1)], fx, { ok: v => !v.eq(z) });
        return Q(`Find the zero of the polynomial p(x) = ${poly([a, b])}.`, bb, `A zero of p(x) is the value of x that makes p(x) = 0.`,
          [`Set p(x) = 0: ${poly([a, b])} = 0`, `${poly([a, 0])} = ${ind(-b)}`, `x = ${ind(-b)} ÷ ${pn(a)} = ${fs(z)}`], { t, a, b });
      }
      let x = negOK ? R(-9, 15) : R(1, 15); if (!x) x = 4;
      const a = R(2, 9);
      if (t === 'both') {
        let c = R(1, 9); while (c === a) c = R(1, 9); const b = R(-20, 20) || 5, d = (a - c) * x + b;
        const bb = build(F(x), [F(-x), new Fr(d + b, a - c), new Fr(d - b, a + c), F(x + 1)], fx, { ok: v => !v.eq(F(x)) });
        const k = a - c;
        return Q(`Solve: ${poly([a, b])} = ${poly([c, d])}`, bb, `Bring the x-terms to one side and the numbers to the other, doing the same thing to both sides.`,
          [`Subtract ${poly([c, 0])} from both sides: ${poly([k, b])} = ${ind(d)}`, `${b < 0 ? 'Add' : 'Subtract'} ${Math.abs(b)} ${b < 0 ? 'to' : 'from'} both sides: ${poly([k, 0])} = ${ind(d)} ${b < 0 ? '+' : '−'} ${Math.abs(b)} = ${ind(d - b)}`, `Divide by ${pn(k)}: x = ${ind(d - b)} ÷ ${pn(k)} = ${ind(x)}`, `Check: ${a} × ${pn(x)} + ${pn(b)} = ${ind(a * x + b)} and ${c} × ${pn(x)} + ${pn(d)} = ${ind(c * x + d)}`], { t, a, b, c, d });
      }
      const b = t === 'word' ? R(2, 30) : (R(1, 25) * (negOK && Math.random() < .4 ? -1 : 1)), c = a * x + b;
      if (t === 'word') {
        if (x <= 0) x = R(2, 15);
        const c2 = a * x + b;
        const bb = build(x, [(c2 + b) / a, c2 - b, c2 / a - b, x + 1, (c2 - b) * a], ind, { ok: v => Number.isInteger(v) && v > 0 && v !== x });
        return Q(`${pick(NAMES)} thinks of a number, multiplies it by ${a} and then adds ${b}. The result is ${c2}. What is the number?`, bb, `Write it as an equation and undo each step in reverse order.`,
          [`Equation: ${a}x + ${b} = ${c2}`, `Subtract ${b}: ${c2} − ${b} = ${c2 - b}`, `Divide by ${a}: ${c2 - b} ÷ ${a} = ${x}`, `Check: ${a} × ${x} + ${b} = ${c2}`], { t, a, b, c: c2 });
      }
      const bb = build(F(x), [new Fr(c + b, a), F(c - b), new Fr(c, a).sub(b), F(-x), F(x + 1)], fx, { ok: v => !v.eq(F(x)) && (v.int || g >= 8) });
      return Q(`Solve: ${poly([a, b])} = ${ind(c)}`, bb, `Do the same thing to both sides to keep the balance: first undo the ${b < 0 ? 'subtraction' : 'addition'}, then the multiplication.`,
        [`${b < 0 ? 'Add' : 'Subtract'} ${Math.abs(b)} ${b < 0 ? 'to' : 'from'} both sides: ${a}x = ${ind(c)} ${b < 0 ? '+' : '−'} ${Math.abs(b)} = ${ind(c - b)}`, `Divide both sides by ${a}: x = ${ind(c - b)} ÷ ${a} = ${ind(x)}`, `Check: ${a} × ${pn(x)} ${b < 0 ? '−' : '+'} ${Math.abs(b)} = ${ind(c)}`], { t: 'one', a, b, c });
    } });

  /* ---- 31. Ratio and proportion (Grades 6–8) ---- */
  def({ id: 'ratio', name: 'Ratio and proportion', subj: ['maths'], g: [6, 8], re: /\bratios?\b|^proportion$|sharing profits|mixtures and the rule|sharing in a ratio/i, not: /trig|area ratios|cylinder|mole|more than two|triangles|pie|inverse|test/i,
    make() {
      const t = pick(['simp', 'share', 'share', 'missing']);
      let p, q; do { p = R(1, 9); q = R(1, 9); } while (gcd(p, q) !== 1 || p === q);
      if (t === 'simp') {
        const k = pick([4, 6, 8, 9, 10, 12, 15, 16, 18]), a = p * k, b = q * k;
        const facs = []; for (let f = 2; f < k; f++) if (k % f === 0) facs.push(f); const f0 = facs.length ? pick(facs) : null;
        const bb = build(`${p} : ${q}`, [f0 ? `${a / f0} : ${b / f0}` : null, `${q} : ${p}`, `${a - (a - p)} : ${b - (a - p)}`, `${p + 1} : ${q + 1}`], s => s, { ok: s => !/(^|\s)-|: 0$|^0 :/.test(s) });
        return Q(`Write the ratio ${a} : ${b} in its simplest form.`, bb, `Divide both terms by their HCF.`, [`HCF of ${a} and ${b} is ${k}`, `${a} ÷ ${k} = ${p}, ${b} ÷ ${k} = ${q}`], { t, a, b });
      }
      if (t === 'share') {
        const u = R(5, 200) * pick([1, 10]), N = (p + q) * u, [n1, n2] = two(), first = Math.random() < .5, ans = (first ? p : q) * u;
        const bb = build(ans, [(first ? q : p) * u, N / 2, u, Math.round(N / (first ? p : q)) === N / (first ? p : q) ? N / (first ? p : q) : null, ans + u], rs, { ok: v => v > 0 && v !== ans });
        return Q(`${n1} and ${n2} share ₹${ind(N)} in the ratio ${p} : ${q}. How much does ${first ? n1 : n2} get?`, bb, `Add the ratio parts to find the total number of parts, find one part, then multiply.`,
          [`Total parts: ${p} + ${q} = ${p + q}`, `One part: ${ind(N)} ÷ ${p + q} = ${ind(u)}`, `${first ? n1 : n2}'s share: ${first ? p : q} × ${ind(u)} = ${ind(ans)}`], { t, N, p, q, first });
      }
      const a = p * R(1, 4), b = q * R(1, 4), m = R(2, 6), c = a * m, ans = b * m;
      const bb = build(ans, [b + (c - a), c * a / b, ans + b, b * c], ind, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
      return Q(`Find the missing number: ${a} : ${b} = ${c} : ___`, bb, `In equal ratios, both terms are multiplied by the same number.`, [`${c} ÷ ${a} = ${m}, so the first term was multiplied by ${m}`, `${b} × ${m} = ${ans}`], { t, a, b, c });
    } });

  /* ---- 32. Unitary method, direct and inverse proportion (Grades 5–8) ---- */
  def({ id: 'unitary', name: 'Unitary method', subj: ['maths'], g: [5, 8], re: /unitary|direct proportion|inverse proportion|working together|rule of three|scaling and the unitary/i,
    make({ g, title }) {
      const inv = /inverse|working together/i.test(title) ? true : g >= 8 && Math.random() < .3;
      if (inv) {
        let w1, d1, w2, d2; do { w1 = R(2, 12); d1 = R(2, 30); w2 = R(2, 15); d2 = w1 * d1 / w2; } while (!Number.isInteger(d2) || w1 === w2);
        const bb = build(d2, [d1 * w2 / w1, d1 + w1 - w2, d1, d2 + 1], v => `${nm(v)} days`, { ok: v => F(v).p > 0 && !(F(v).eq(F(d2))) });
        return Q(`${w1} workers can paint a school wall in ${d1} days. How many days will ${w2} workers take, working at the same rate?`, bb, `More workers take fewer days: this is inverse proportion, so workers × days stays the same.`,
          [`Total work: ${w1} × ${d1} = ${w1 * d1} worker-days`, `Days for ${w2} workers: ${w1 * d1} ÷ ${w2} = ${d2}`], { t: 'inv', w1, d1, w2 });
      }
      const n = R(2, 12), u = R(3, g <= 5 ? 60 : 250), m = R(2, 20); if (m === n) throw new Error('retry');
      const C = n * u, ans = m * u, it = pick(['pens', 'notebooks', 'kg of rice', 'metres of cloth', 'mangoes']);
      const bb = build(ans, [C + (m - n), C * n / m, u, ans + u], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
      return Q(`${n} ${it} cost ₹${ind(C)}. What do ${m} ${it} cost?`, bb, `Find the cost of one first (divide), then of many (multiply).`,
        [`Cost of 1: ${ind(C)} ÷ ${n} = ${ind(u)}`, `Cost of ${m}: ${m} × ${ind(u)} = ${ind(ans)}`], { t: 'dir', n, C, m });
    } });

  /* ---- 33. Percentages (Grades 6–9) ---- */
  def({ id: 'percent', name: 'Percentages', subj: ['maths'], g: [6, 9], re: /percent/i, not: /chart|cylinder|mass percent|compare and check|reading/i,
    make() {
      const t = pick(['of', 'what', 'change']);
      if (t === 'of') {
        const x = pick([5, 10, 12, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80]), base = 100 / gcd(x, 100), N = base * R(2, Math.max(2, Math.floor(5000 / base / 4))), ans = N * x / 100;
        const bb = build(ans, [N * x / 10, N - ans, x, ans * 10, N / x], ind, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
        return Q(`What is ${x}% of ${ind(N)}?`, bb, `Per cent means "out of 100", so ${x}% = ${x}/100.`, [`${x}% = ${x}/100`, `${ind(N)} × ${x}/100 = ${ind(ans)}`], { t, x, N });
      }
      if (t === 'what') {
        const b = pick([20, 25, 40, 50, 80, 120, 200, 250, 400, 500]), x = pick([5, 10, 15, 20, 25, 30, 40, 60, 75]), a = b * x / 100;
        if (!Number.isInteger(a)) throw new Error('retry');
        const bb = build(x, [a, 100 - x, b / a * 10, x * 2], v => `${nm(v)}%`, { ok: v => F(v).p > 0 && !F(v).eq(F(x)) });
        return Q(`${pick(NAMES)} scored ${a} marks out of ${b}. What percentage is that?`, bb, `Percentage = (part ÷ whole) × 100.`, [`${a}/${b} × 100 = ${x}`, `So it is ${x}%`], { t, a, b });
      }
      const x = pick([5, 10, 20, 25, 40, 50]), up = Math.random() < .5, base = 100 / gcd(x, 100), N = base * R(4, 200), ch = N * x / 100, ans = up ? N + ch : N - ch;
      const bb = build(ans, [up ? N - ch : N + ch, ch, N + x, up ? N * (1 + x / 10) : N - x], ind, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
      return Q(`A price of ₹${ind(N)} is ${up ? 'increased' : 'decreased'} by ${x}%. What is the new price (in ₹)?`, bb, `Find ${x}% of the old value, then ${up ? 'add it' : 'take it away'}.`,
        [`${x}% of ${ind(N)}: ${ind(N)} × ${x}/100 = ${ind(ch)}`, `New price: ${ind(N)} ${up ? '+' : '−'} ${ind(ch)} = ${ind(ans)}`], { t, x, N, up });
    } });

  /* ---- 34. Profit, loss, discount, GST (Grades 7–9) ---- */
  def({ id: 'profit_loss', name: 'Profit, loss and discount', subj: ['maths'], g: [7, 9], re: /profit|loss|discount|gst/i, not: /sharing|weights/i,
    make({ title }) {
      const t = /gst/i.test(title) && Math.random() < .5 ? 'gst' : pick(['sp', 'pct', 'disc']);
      if (t === 'gst') {
        const g_ = pick([5, 12, 18, 28]), base = 100 / gcd(g_, 100), P = base * R(2, 200), tax = P * g_ / 100, ans = P + tax;
        const bb = build(ans, [P - tax, tax, P + g_, P * (100 + g_) / 1000], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
        return Q(`A school bag costs ₹${ind(P)} before GST. GST is ${g_}%. What is the price including GST?`, bb, `Price with GST = price + GST on the price.`, [`GST: ${ind(P)} × ${g_}/100 = ${ind(tax)}`, `Total: ${ind(P)} + ${ind(tax)} = ${ind(ans)}`], { t, g: g_, P });
      }
      if (t === 'disc') {
        const r = pick([5, 10, 15, 20, 25, 30, 40, 50]), base = 100 / gcd(r, 100), M = base * R(2, 400), off = M * r / 100, ans = M - off;
        const bb = build(ans, [M + off, off, M - r, M * (100 - r) / 1000], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
        return Q(`A cycle is marked ₹${ind(M)}. The shop gives ${r}% discount. What is the selling price?`, bb, `Discount is always worked out on the marked price.`, [`Discount: ${ind(M)} × ${r}/100 = ${ind(off)}`, `Selling price: ${ind(M)} − ${ind(off)} = ${ind(ans)}`], { t, r, M });
      }
      const r = pick([5, 8, 10, 12, 15, 20, 25, 30]), gain = Math.random() < .55, base = 100 / gcd(r, 100), CP = base * R(2, 500), ch = CP * r / 100, SP = gain ? CP + ch : CP - ch;
      if (t === 'sp') {
        const bb = build(SP, [gain ? CP - ch : CP + ch, ch, CP + r, SP + ch], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== SP });
        return Q(`A shopkeeper buys a fan for ₹${ind(CP)} and sells it at a ${r}% ${gain ? 'profit' : 'loss'}. What is the selling price?`, bb, `${gain ? 'Profit' : 'Loss'} % is worked out on the cost price.`,
          [`${gain ? 'Profit' : 'Loss'}: ${ind(CP)} × ${r}/100 = ${ind(ch)}`, `SP: ${ind(CP)} ${gain ? '+' : '−'} ${ind(ch)} = ${ind(SP)}`], { t, r, CP, gain });
      }
      const fmt = ([v, gn]) => `${nm(v)}% ${gn ? 'profit' : 'loss'}`;
      const onSP = new Fr(ch * 100, SP);
      const bb = build([F(r), gain], [[F(r), !gain], [onSP, gain], [F(ch), gain], [F(r * 2), gain]], fmt, { ok: ([v]) => dec(v, 2) !== null && v.p > 0 });
      return Q(`A phone bought for ₹${ind(CP)} is sold for ₹${ind(SP)}. Find the profit or loss per cent.`, bb, `Profit or loss % = (profit or loss ÷ cost price) × 100.`,
        [`${gain ? 'SP > CP, so profit' : 'SP < CP, so loss'}: ${ind(Math.max(SP, CP))} − ${ind(Math.min(SP, CP))} = ${ind(ch)}`, `${ind(ch)}/${ind(CP)} × 100 = ${r}`], { t, CP, SP });
    } });

  /* ---- 35. Simple interest (Grades 7–8) ---- */
  def({ id: 'simple_int', name: 'Simple interest', subj: ['maths'], g: [7, 8], re: /interest/i,
    make() {
      const t = pick(['si', 'amt', 'time']);
      let P, Rr, T; do { P = R(2, 100) * 500; Rr = R(4, 15); T = R(2, 6); } while ((P * Rr * T) % 100);
      const SI = P * Rr * T / 100;
      if (t === 'time') {
        const bb = build(T, [T + 1, T - 1, SI / Rr / 100 | 0 || null, Rr], v => `${v} years`, { ok: v => v > 0 && v !== T });
        return Q(`₹${ind(P)} earns ₹${ind(SI)} simple interest at ${Rr}% per year. For how many years was it invested?`, bb, `From SI = P × R × T ÷ 100, we get T = SI × 100 ÷ (P × R).`,
          [`P × R = ${ind(P)} × ${Rr} = ${ind(P * Rr)}`, `T = ${ind(SI)} × 100 ÷ ${ind(P * Rr)} = ${T}`], { t, P, R: Rr, SI });
      }
      const amt = t === 'amt', ans = amt ? P + SI : SI;
      const bb = build(ans, [amt ? SI : P + SI, P * Rr / 100 + (amt ? P : 0), amt ? P + SI * 2 : SI * 2, P * Rr * (T + 1) / 100 + (amt ? P : 0)], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
      return Q(`Find the ${amt ? 'amount' : 'simple interest'} on ₹${ind(P)} at ${Rr}% per year for ${T} years.`, bb, `Simple interest = P × R × T ÷ 100. Amount = principal + interest.`,
        [`SI = ${ind(P)} × ${Rr} × ${T} ÷ 100 = ${ind(SI)}`, ...(amt ? [`Amount = ${ind(P)} + ${ind(SI)} = ${ind(P + SI)}`] : [])], { t, P, R: Rr, T });
    } });

  /* ---- 36. Compound interest and depreciation (Grade 8) ---- */
  def({ id: 'compound_int', name: 'Compound interest', subj: ['maths'], g: [8, 8], re: /interest|growth and depreciation|depreciation/i,
    make() {
      const dep = Math.random() < .25, r = pick([5, 10, 20, 4, 8, 15]), n = R(2, 3), f = dep ? 100 - r : 100 + r, unit = (100 / gcd(f, 100)) ** n;
      const P = unit * R(1, Math.max(1, Math.floor(200000 / unit))); if (P < 1000) throw new Error('retry');
      const A = [P]; for (let k = 1; k <= n; k++) A.push(A[k - 1] * f / 100);
      if (A.some(x => !Number.isInteger(x))) throw new Error('retry');
      const steps = A.slice(1).map((x, k) => `Year ${k + 1}: ${ind(A[k])} × ${f}/100 = ${ind(x)}`);
      if (dep) {
        const ans = A[n], bb = build(ans, [P - P * r * n / 100, A[n - 1], P - ans, ans + P * r / 100], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
        return Q(`A scooter worth ₹${ind(P)} loses ${r}% of its value every year. What is it worth after ${n} years?`, bb, `Each year the value is ${f}% of the value at the start of that year.`, steps, { t: 'dep', P, r, n });
      }
      const askCI = Math.random() < .5, CI = A[n] - P, ans = askCI ? CI : A[n], SI = P * r * n / 100;
      const bb = build(ans, [askCI ? SI : P + SI, askCI ? A[n] : CI, askCI ? A[n - 1] - P : A[n - 1], ans + P * r / 100], rs, { ok: v => Number.isInteger(v) && v > 0 && v !== ans });
      return Q(`Find the ${askCI ? 'compound interest' : 'amount'} on ₹${ind(P)} at ${r}% per year, compounded yearly, for ${n} years.`, bb, `With compound interest, each year's interest is added on before the next year's interest is worked out.`,
        [...steps, ...(askCI ? [`CI = ${ind(A[n])} − ${ind(P)} = ${ind(CI)}`] : [])], { t: askCI ? 'ci' : 'amt', P, r, n });
    } });

  /* ---- 37. Perimeter and area of rectangles and squares (Grades 4–8) ---- */
  def({ id: 'rect', name: 'Perimeter and area (rectangles, squares)', subj: ['maths'], g: [4, 8], re: /perimeter|area of rectangles|area and perimeter|area vs perimeter|same area/i,
    not: /circle|triangle|trapez|rhomb|sector|segment|surface|heron|π|mystery|composite|puzzle|estimat|tracks|grid|patch|stories|calendar/i,
    make({ g, title }) {
      const hasA = /area/i.test(title) || g >= 5, hasP = /perimeter/i.test(title);
      const kinds = [...(hasP ? ['pr', 'ps'] : []), ...(hasA ? ['ar', 'as'] : []), ...(g >= 6 && hasA ? ['side'] : [])];
      const t = pick(kinds.length ? kinds : ['pr']), u = pick(['cm', 'm']);
      const l = R(4, g === 4 ? 30 : 60), b = R(2, l - 1), s = R(3, 40);
      if (t === 'pr') { const P = 2 * (l + b); const bb = build(P, [l * b, l + b, 2 * l + b, 4 * l], v => `${ind(v)} ${u}`, { ok: v => v > 0 && v !== P });
        return Q(`A rectangular garden is ${l} ${u} long and ${b} ${u} wide. What is its perimeter?`, bb, `Perimeter is the distance all the way round: 2 × (length + breadth).`, [`Perimeter = 2 × (length + breadth)`, `2 × (${l} + ${b}) = 2 × ${l + b} = ${P}`], { t, l, b }); }
      if (t === 'ps') { const P = 4 * s; const bb = build(P, [s * s, 2 * s, s + 4, 3 * s], v => `${ind(v)} ${u}`, { ok: v => v > 0 && v !== P });
        return Q(`A square tile has side ${s} ${u}. What is its perimeter?`, bb, `A square has 4 equal sides, so perimeter = 4 × side.`, [`Perimeter = 4 × side`, `4 × ${s} = ${P}`], { t, s }); }
      if (t === 'ar') { const A = l * b; const bb = build(A, [2 * (l + b), l + b, A * 2, l * l], v => `${ind(v)} ${u}²`, { ok: v => v > 0 && v !== A });
        return Q(`A rectangular room is ${l} ${u} long and ${b} ${u} wide. What is its area?`, bb, `Area of a rectangle = length × breadth, in square units.`, [`Area = length × breadth`, `${l} × ${b} = ${ind(A)}`], { t, l, b }); }
      if (t === 'as') { const A = s * s; const bb = build(A, [4 * s, 2 * s, A + s, (s + 1) ** 2], v => `${ind(v)} ${u}²`, { ok: v => v > 0 && v !== A });
        return Q(`A square board has side ${s} ${u}. What is its area?`, bb, `Area of a square = side × side.`, [`Area = side × side`, `${s} × ${s} = ${ind(A)}`], { t, s }); }
      const A = l * b; const bb = build(b, [A - l, l, A / 2 / l === b ? null : Math.round(A / l / 2), b + 1, 2 * b], v => `${ind(v)} ${u}`, { ok: v => Number.isInteger(v) && v > 0 && v !== b });
      return Q(`A rectangle has area ${ind(A)} ${u}² and length ${l} ${u}. What is its breadth?`, bb, `Breadth = area ÷ length.`, [`Area = length × breadth, so breadth = area ÷ length`, `${ind(A)} ÷ ${l} = ${b}`], { t, A, l });
    } });

  /* ---- 38. Area of a triangle (Grades 6–10) ---- */
  def({ id: 'tri_area', name: 'Area of a triangle', subj: ['maths'], g: [6, 10], re: /area of a triangle|area of triangles|triangles inside rectangles|equal-area triangles/i,
    make({ g }) {
      let b = R(4, 40), h = R(3, 30); if ((b * h) % 2) b++; const A = b * h / 2, u = pick(['cm', 'm']);
      if (g >= 8 && Math.random() < .3) { const bb = build(h, [2 * A * b === 0 ? null : A / b, A - b, h * 2, h + 1], v => `${nm(v)} ${u}`, { ok: v => F(v).p > 0 && !F(v).eq(F(h)) });
        return Q(`A triangle has area ${nm(A)} ${u}² and base ${b} ${u}. Find its height.`, bb, `Area = 1/2 × base × height, so height = 2 × area ÷ base.`, [`2 × ${nm(A)} = ${b * h}`, `Height = ${b * h} ÷ ${b} = ${h}`], { t: 'h', A, b }); }
      const bb = build(A, [b * h, b + h, A / 2, (b + h) / 2], v => `${nm(v)} ${u}²`, { ok: v => F(v).p > 0 && !F(v).eq(F(A)) });
      return Q(`A triangle has base ${b} ${u} and height ${h} ${u}. What is its area?`, bb, `A triangle is half of a rectangle with the same base and height.`, [`Area = 1/2 × base × height`, `1/2 × ${b} × ${h} = ${nm(A)}`], { t: 'a', b, h });
    } });

  /* ---- 39. Heron's formula (Grade 9) ---- */
  const HERON = []; for (let a = 3; a <= 30; a++) for (let b = a; b <= 30; b++) for (let c = b; c < a + b && c <= 30; c++) { if ((a + b + c) % 2) continue; const s = (a + b + c) / 2, P = s * (s - a) * (s - b) * (s - c), r = Math.round(Math.sqrt(P)); if (P > 0 && r * r === P) HERON.push([a, b, c]); }
  def({ id: 'heron', name: "Heron's formula", subj: ['maths'], g: [9, 10], re: /heron/i,
    make() {
      const [a, b, c] = shuffle(pick(HERON)), s = (a + b + c) / 2, P = s * (s - a) * (s - b) * (s - c), A = Math.round(Math.sqrt(P));
      const bb = build(A, [P, A * 2, A + s, a * b / 2], v => `${ind(v)} cm²`, { ok: v => Number.isInteger(v) && v > 0 && v !== A });
      return Q(`A triangle has sides ${a} cm, ${b} cm and ${c} cm. Find its area using Heron's formula.`, bb, `Heron's formula: area = √(s(s − a)(s − b)(s − c)), where s is half the perimeter.`,
        [`s = (${a} + ${b} + ${c}) ÷ 2 = ${s}`, `s − a = ${s - a}, s − b = ${s - b}, s − c = ${s - c}`, `${s} × ${s - a} × ${s - b} × ${s - c} = ${ind(P)}`, `${A} × ${A} = ${ind(P)}, so the area is √${ind(P)} = ${A} cm²`], { a, b, c });
    } });

  /* ---- 40. Area of trapezium and rhombus (Grades 8–9) ---- */
  def({ id: 'trap', name: 'Area of trapezium and rhombus', subj: ['maths'], g: [8, 9], re: /area of a trapezium|area of rhombus|rhombuses|area of triangles and quadrilaterals/i,
    make({ title }) {
      const rh = /rhomb/i.test(title) ? true : /trapez/i.test(title) ? false : Math.random() < .5, u = pick(['cm', 'm']);
      if (rh) { let d1 = R(4, 30), d2 = R(4, 30); if ((d1 * d2) % 2) d1++; const A = d1 * d2 / 2;
        const bb = build(A, [d1 * d2, d1 + d2, A / 2, 2 * (d1 + d2)], v => `${nm(v)} ${u}²`, { ok: v => F(v).p > 0 && !F(v).eq(F(A)) });
        return Q(`The diagonals of a rhombus are ${d1} ${u} and ${d2} ${u}. Find its area.`, bb, `Area of a rhombus = 1/2 × product of its diagonals.`, [`Area = 1/2 × d₁ × d₂`, `1/2 × ${d1} × ${d2} = ${nm(A)}`], { t: 'rh', d1, d2 }); }
      let a = R(5, 30), b = R(3, 25), h = R(3, 20); if (a === b) a++; if (((a + b) * h) % 2) h++; const A = (a + b) * h / 2;
      const bb = build(A, [(a + b) * h, a * b * h / 2, A + h, (Math.abs(a - b)) * h / 2], v => `${nm(v)} ${u}²`, { ok: v => F(v).p > 0 && !F(v).eq(F(A)) });
      return Q(`A trapezium has parallel sides ${a} ${u} and ${b} ${u}, and the distance between them is ${h} ${u}. Find its area.`, bb, `Area of a trapezium = 1/2 × (sum of parallel sides) × height.`,
        [`Sum of parallel sides: ${a} + ${b} = ${a + b}`, `1/2 × ${a + b} × ${h} = ${nm(A)}`], { t: 'tr', a, b, h });
    } });

  /* ---- 41. Circles: circumference, area, arc, sector (Grades 9–10) ---- */
  def({ id: 'circle', name: 'Circles: circumference and area', subj: ['maths'], g: [9, 10], re: /circumference|mystery ratio|area of a sector|arc length|why πr²|perimeter and the mystery/i, not: /recap|segment/i,
    make({ title }) {
      const t = /sector/i.test(title) ? 'sector' : /arc/i.test(title) ? pick(['arc', 'sector']) : pick(['circ', 'area', 'circ', 'area']);
      const r = pick([7, 14, 21, 28, 35, 3.5, 10.5]), Rr = F(r), PI = new Fr(22, 7), u = 'cm';
      if (t === 'circ' || t === 'area') {
        const v = t === 'circ' ? PI.mul(2).mul(Rr) : PI.mul(Rr).mul(Rr), unit = t === 'circ' ? u : u + '²';
        const other = t === 'circ' ? PI.mul(Rr).mul(Rr) : PI.mul(2).mul(Rr);
        const bb = build(v, [other, t === 'circ' ? PI.mul(Rr) : PI.mul(2).mul(Rr).mul(Rr), v.mul(2), t === 'circ' ? Rr.mul(2) : PI.mul(Rr)], x => (dec(x, 2) ?? 'x') + ' ' + unit, { ok: x => dec(x, 2) !== null && !F(x).eq(v) });
        return Q(`Find the ${t === 'circ' ? 'circumference' : 'area'} of a circle of radius ${dec(Rr)} ${u}. (Take π = 22/7.)`, bb, t === 'circ' ? `Circumference = 2πr.` : `Area = πr².`,
          [t === 'circ' ? `C = 2 × π × r` : `A = π × r × r`, t === 'circ' ? `2 × 22/7 × ${dec(Rr)} = ${dec(v, 2)}` : `22/7 × ${dec(Rr)} × ${dec(Rr)} = ${dec(v, 2)}`], { t, r: dec(Rr) });
      }
      const th = pick([30, 45, 60, 72, 90, 120, 135, 150, 180, 210, 240, 270]), fr = new Fr(th, 360);
      const v = t === 'arc' ? fr.mul(PI).mul(2).mul(Rr) : fr.mul(PI).mul(Rr).mul(Rr); if (dec(v, 2) === null) throw new Error('retry');
      const unit = t === 'arc' ? u : u + '²';
      const bb = build(v, [t === 'arc' ? fr.mul(PI).mul(Rr).mul(Rr) : fr.mul(PI).mul(2).mul(Rr), t === 'arc' ? fr.mul(PI).mul(Rr) : fr.mul(PI).mul(Rr).mul(Rr).mul(2), new Fr(th, 180).mul(PI).mul(Rr).mul(t === 'arc' ? 2 : Rr), v.mul(2)], x => (dec(x, 2) ?? 'x') + ' ' + unit, { ok: x => dec(x, 2) !== null && !F(x).eq(v) });
      return Q(`A circle has radius ${dec(Rr)} cm. Find the ${t === 'arc' ? 'length of the arc' : 'area of the sector'} with angle ${th}° at the centre. (Take π = 22/7.)`, bb,
        t === 'arc' ? `Arc length = (θ/360) × 2πr.` : `Sector area = (θ/360) × πr².`,
        [`Fraction of the circle: ${th}/360 = ${fs(fr)}`, t === 'arc' ? `${fs(fr)} × 2 × 22/7 × ${dec(Rr)} = ${dec(v, 2)}` : `${fs(fr)} × 22/7 × ${dec(Rr)} × ${dec(Rr)} = ${dec(v, 2)}`], { t, r: dec(Rr), th });
    } });

  /* ---- 42. Volume and surface area of solids (Grades 8–10) ---- */
  def({ id: 'solids', name: 'Volume and surface area', subj: ['maths'], g: [8, 10], re: /volume of|surface area of|surface area and volume|cuboids in layers|surface versus space/i, not: /combined|conversion|converting/i,
    make({ title }) {
      let pool = []; if (/cuboid|cube/i.test(title)) pool.push('cuboidV', 'cubeV', 'cuboidS', 'cubeS'); if (/cylinder/i.test(title)) pool.push(/volume/i.test(title) ? 'cylV' : 'cylS', 'cylV'); if (/cone/i.test(title)) pool.push(/surface/i.test(title) ? 'coneS' : 'coneV'); if (/sphere/i.test(title)) pool.push(/surface/i.test(title) ? 'sphS' : 'sphV');
      if (!pool.length) pool = ['cuboidV', 'cubeV', 'cylV', 'coneV', 'sphV', 'cuboidS', 'cylS', 'sphS'];
      const t = pick(pool), PI = new Fr(22, 7);
      let q, v, st, wr, exp, unit = 'cm³';
      if (t === 'cuboidV' || t === 'cuboidS') { const l = R(3, 25), b = R(2, 20), h = R(2, 15);
        if (t === 'cuboidV') { v = F(l * b * h); q = `Find the volume of a cuboid ${l} cm long, ${b} cm wide and ${h} cm high.`; st = [`V = l × b × h`, `${l} × ${b} × ${h} = ${ind(l * b * h)}`]; wr = [2 * (l * b + b * h + h * l), l + b + h, l * b, l * b * h * 2]; exp = `Volume of a cuboid = length × breadth × height.`; }
        else { unit = 'cm²'; v = F(2 * (l * b + b * h + h * l)); q = `Find the total surface area of a cuboid ${l} cm × ${b} cm × ${h} cm.`; st = [`TSA = 2(lb + bh + hl)`, `${l} × ${b} + ${b} × ${h} + ${h} × ${l} = ${l * b + b * h + h * l}`, `2 × ${l * b + b * h + h * l} = ${ind(v.p)}`]; wr = [l * b * h, l * b + b * h + h * l, 2 * (l + b + h), 4 * (l * b + b * h + h * l)]; exp = `A cuboid has 6 faces in 3 equal pairs.`; } }
      else if (t === 'cubeV' || t === 'cubeS') { const a = R(2, 25);
        if (t === 'cubeV') { v = F(a ** 3); q = `Find the volume of a cube of edge ${a} cm.`; st = [`V = a × a × a`, `${a} × ${a} × ${a} = ${ind(a ** 3)}`]; wr = [6 * a * a, a * a, 3 * a, a ** 3 * 2]; exp = `Volume of a cube = edge³.`; }
        else { unit = 'cm²'; v = F(6 * a * a); q = `Find the total surface area of a cube of edge ${a} cm.`; st = [`TSA = 6 × a × a`, `6 × ${a} × ${a} = ${ind(6 * a * a)}`]; wr = [a ** 3, 4 * a * a, a * a, 12 * a]; exp = `A cube has 6 equal square faces.`; } }
      else {
        const r = F(pick(t.startsWith('sph') ? [7, 14, 21, 3.5, 10.5] : [7, 14, 21, 3.5, 10.5])), h = F(t === 'coneV' ? pick([6, 9, 12, 15, 24, 30]) : pick([5, 10, 12, 15, 20, 7]));
        const rS = dec(r), hS = dec(h);
        if (t === 'cylV') { v = PI.mul(r).mul(r).mul(h); q = `Find the volume of a cylinder with radius ${rS} cm and height ${hS} cm. (Take π = 22/7.)`; st = [`V = πr²h`, `22/7 × ${rS} × ${rS} × ${hS} = ${dec(v, 2)}`]; wr = [PI.mul(2).mul(r).mul(h), PI.mul(r).mul(h), PI.mul(r).mul(r).mul(h).div(3), v.mul(2)]; exp = `Volume of a cylinder = area of the circular base × height.`; }
        else if (t === 'cylS') { unit = 'cm²'; v = PI.mul(2).mul(r).mul(h); q = `Find the curved surface area of a cylinder with radius ${rS} cm and height ${hS} cm. (Take π = 22/7.)`; st = [`CSA = 2πrh`, `2 × 22/7 × ${rS} × ${hS} = ${dec(v, 2)}`]; wr = [PI.mul(r).mul(r).mul(h), PI.mul(r).mul(h), PI.mul(2).mul(r).mul(h.add(r)), v.mul(2)]; exp = `Unrolled, the curved surface is a rectangle: circumference × height.`; }
        else if (t === 'coneV') { v = PI.mul(r).mul(r).mul(h).div(3); q = `Find the volume of a cone with radius ${rS} cm and height ${hS} cm. (Take π = 22/7.)`; st = [`V = 1/3 × πr²h`, `1/3 × 22/7 × ${rS} × ${rS} × ${hS} = ${dec(v, 2)}`]; wr = [PI.mul(r).mul(r).mul(h), PI.mul(r).mul(h).div(3), v.mul(2), PI.mul(r).mul(r).mul(h).div(2)]; exp = `A cone holds one third of a cylinder with the same base and height.`; }
        else if (t === 'coneS') { const tri = pick([[3, 4, 5], [5, 12, 13], [6, 8, 10], [7, 24, 25]]), k = 7; const rr = F(tri[0] * k), hh = tri[1] * k, l = tri[2] * k; unit = 'cm²'; v = PI.mul(rr).mul(l);
          q = `A cone has radius ${dec(rr)} cm and height ${hh} cm. Find its curved surface area. (Take π = 22/7.)`; st = [`Slant height: ${dec(rr)}² + ${hh}² = ${tri[0] ** 2 * 49 + tri[1] ** 2 * 49} = ${l}²`, `CSA = πrl`, `22/7 × ${dec(rr)} × ${l} = ${dec(v, 2)}`]; wr = [PI.mul(rr).mul(hh), PI.mul(rr).mul(rr.add(l)), PI.mul(2).mul(rr).mul(l), v.div(2)]; exp = `CSA of a cone = πrl, where l is the slant height.`; }
        else if (t === 'sphV') { v = PI.mul(4).mul(r).mul(r).mul(r).div(3); q = `Find the volume of a sphere of radius ${rS} cm. (Take π = 22/7.)`; st = [`V = 4/3 × πr³`, `4/3 × 22/7 × ${rS} × ${rS} × ${rS} = ${dec(v, 2) ?? 'x'}`]; wr = [PI.mul(4).mul(r).mul(r), PI.mul(r).mul(r).mul(r), v.mul(2), PI.mul(2).mul(r).mul(r).mul(r).div(3)]; exp = `Volume of a sphere = 4/3 πr³.`; }
        else { unit = 'cm²'; v = PI.mul(4).mul(r).mul(r); q = `Find the surface area of a sphere of radius ${rS} cm. (Take π = 22/7.)`; st = [`SA = 4πr²`, `4 × 22/7 × ${rS} × ${rS} = ${dec(v, 2)}`]; wr = [PI.mul(r).mul(r), PI.mul(2).mul(r).mul(r), PI.mul(4).mul(r).mul(r).mul(r).div(3), PI.mul(3).mul(r).mul(r)]; exp = `Surface area of a sphere = 4πr², four times the area of its biggest circle.`; }
      }
      if (dec(v, 2) === null) throw new Error('retry');
      const bb = build(v, wr, x => (dec(x, 2) ?? 'x') + ' ' + unit, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(v) });
      return Q(q, bb, exp, st, { t, q });
    } });

  /* ---- 43. Mean, median, mode, range (Grades 6–11) ---- */
  def({ id: 'mmm', name: 'Mean, median, mode and range', subj: ['maths'], g: [6, 11], re: /\bmean\b|\bmedian\b|\bmode\b|averages? of ungrouped|\brange\b/i,
    not: /grouped data|frequency|deviation|variance|balance point|tinkering|story of the mean|step-deviation|cumulative|empirical|weights|average of averages|impossible|mixtures|fair shares|combined|domain|codomain|mean value|a\.m\.|means$|arithmetic and geometric|grouped|making sense/i,
    make({ title }) {
      const ks = []; if (/mean|average/i.test(title)) ks.push('mean'); if (/median/i.test(title)) ks.push('median'); if (/\bmode\b/i.test(title)) ks.push('mode'); if (/range/i.test(title)) ks.push('range');
      const t = pick(ks.length ? ks : ['mean', 'median', 'mode', 'range']), n = R(5, 8);
      let xs; const ctx = pick([['runs scored by a batter in', 'matches', ''], ['marks scored in', 'tests', ''], ['heights of plants (in cm) after', 'weeks', '']]);
      if (t === 'mode') { const m = R(10, 60); xs = [m, m, m]; while (xs.length < n) { const v = R(10, 60); if (xs.filter(x => x === v).length < 2 && v !== m) xs.push(v); } xs = shuffle(xs); }
      else { xs = Array.from({ length: n }, () => R(5, 95)); if (t === 'mean') { const s = xs.reduce((a, b) => a + b, 0), r = s % n; xs[n - 1] -= r; if (xs[n - 1] < 1) xs[n - 1] += n; } }
      const srt = xs.slice().sort((a, b) => a - b), sum = xs.reduce((a, b) => a + b, 0);
      const med = n % 2 ? F(srt[(n - 1) / 2]) : new Fr(srt[n / 2 - 1] + srt[n / 2], 2), mid = n % 2 ? F(xs[(n - 1) / 2]) : new Fr(xs[n / 2 - 1] + xs[n / 2], 2);
      const q = `The ${ctx[0]} ${n} ${ctx[1]} are: ${xs.join(', ')}. Find the ${t}.`;
      let ans, steps, wr, exp;
      if (t === 'mean') { ans = new Fr(sum, n); steps = [`Sum: ${xs.join(' + ')} = ${sum}`, `Mean = ${sum} ÷ ${n} = ${nm(ans)}`]; wr = [new Fr(sum, n - 1), med, F(sum), ans.add(1), mid]; exp = `Mean = sum of all values ÷ number of values.`; }
      else if (t === 'median') { ans = med; steps = [`Put in order: ${srt.join(', ')}`, n % 2 ? `${n} values, so the middle one is value number ${(n + 1) / 2}: ${srt[(n - 1) / 2]}` : `${n} values, so take the mean of values ${n / 2} and ${n / 2 + 1}: (${srt[n / 2 - 1]} + ${srt[n / 2]}) ÷ 2 = ${nm(med)}`]; wr = [mid, new Fr(sum, n), F(srt[n - 1] - srt[0]), F(srt[Math.floor(n / 2) + 1])]; exp = `The median is the middle value after putting the data in order.`; }
      else if (t === 'mode') { const m = xs.find(x => xs.filter(y => y === x).length === 3); ans = F(m); steps = [`${m} appears 3 times; every other value appears fewer times`, `The value that appears most often is ${m}`]; wr = [med, F(srt[n - 1]), F(Math.round(sum / n)), F(srt[0])]; exp = `The mode is the value that occurs most often.`; }
      else { ans = F(srt[n - 1] - srt[0]); steps = [`Highest: ${srt[n - 1]}, lowest: ${srt[0]}`, `Range = ${srt[n - 1]} − ${srt[0]} = ${srt[n - 1] - srt[0]}`]; wr = [F(srt[n - 1]), F(srt[n - 1] + srt[0]), F(srt[n - 1] - srt[1]), med]; exp = `Range = highest value − lowest value.`; }
      const bb = build(ans, wr, nm, { ok: v => F(v).p > 0 && dec(v, 2) !== null && !F(v).eq(ans) });
      return Q(q, bb, exp, steps, { t, xs });
    } });

  /* ---- 44. Quadratic equations with integer roots (Grades 9–10) ---- */
  def({ id: 'quadratic', name: 'Quadratic equations', subj: ['maths'], g: [9, 10], re: /quadratic|splitting the middle|solving by factorisation|finding zeros by splitting|zeros and coefficients|roots, zeros/i, not: /nature|real life|recap|complex/i,
    make({ g }) {
      const a = g >= 10 ? pick([1, 1, 1, 2, 3]) : 1; let r, s; do { r = R(-9, 9); s = R(-9, 9); } while (!r || !s || r === s || r === -s);
      const b = -a * (r + s), c = a * r * s, m = -a * r, n = -a * s, sorted = [r, s].sort((x, y) => x - y);
      const fmt = ([x, y]) => { const [p, q] = [x, y].sort((u, v) => u - v); return `x = ${ind(p)} or x = ${ind(q)}`; };
      const fac = (k) => `(${poly([1, -k])})`;
      const bb = build(sorted, [[-r, -s], [r, -s], [-r, s], [c, 1].map(x => x / a)], fmt, { ok: ([x, y]) => x !== y && Number.isInteger(x) && Number.isInteger(y) });
      return Q(`Solve by factorisation: ${poly([a, b, c])} = 0`, bb, `Split the middle term using two numbers whose product is a × c and whose sum is b. Then each bracket can be zero.`,
        [`a × c = ${a} × ${pn(c)} = ${ind(a * c)}`, `Two numbers: ${pn(m)} and ${pn(n)}; ${pn(m)} × ${pn(n)} = ${ind(m * n)}, ${pn(m)} + ${pn(n)} = ${ind(b)}`, `Factorise: ${a > 1 ? a + ' × ' : ''}${fac(r)}${fac(s)} = 0`, `Set each bracket to zero: ${fac(r)} = 0 or ${fac(s)} = 0`], { a, b, c });
    } });

  /* ---- 45. Nature of roots (Grade 10) ---- */
  def({ id: 'nature_roots', name: 'Nature of roots', subj: ['maths'], g: [10, 11], re: /nature of roots|nature first/i,
    make() {
      const a = R(1, 5), b = R(-12, 12), c = R(-10, 10) || 3, Dd = b * b - 4 * a * c, nat = d => d > 0 ? 'two distinct real roots' : d === 0 ? 'two equal real roots' : 'no real roots';
      const fmt = ([d, k]) => `D = ${ind(d)}, ${k}`;
      const bb = build([Dd, nat(Dd)], [[b * b + 4 * a * c, nat(b * b + 4 * a * c)], [Dd, nat(Dd === 0 ? 1 : -Dd)], [Dd, Dd === 0 ? 'no real roots' : 'two equal real roots'], [b - 4 * a * c, nat(b - 4 * a * c)], [-Dd, nat(-Dd)]], fmt);
      return Q(`For ${poly([a, b, c])} = 0, find the discriminant D and the nature of the roots.`, bb, `D = b² − 4ac. If D > 0 there are two distinct real roots, if D = 0 two equal real roots, and if D < 0 no real roots.`,
        [`a = ${a}, b = ${ind(b)}, c = ${ind(c)}`, `D = ${pn(b)}² − 4 × ${a} × ${pn(c)} = ${b * b} − ${pn(4 * a * c)} = ${ind(Dd)}`, `D ${Dd > 0 ? '>' : Dd === 0 ? '=' : '<'} 0, so there are ${nat(Dd)}`], { a, b, c });
    } });

  /* ---- 46. Arithmetic progressions (Grades 9–11) ---- */
  def({ id: 'ap', name: 'Arithmetic progressions', subj: ['maths'], g: [9, 11], re: /arithmetic progression|\bAPs?\b|nth term|sum of n terms|1 \+ 2 \+ 3|gauss|is it a term/i, not: /G\.P|geometric|challenge/i,
    make({ title }) {
      const t = /sum|gauss|1 \+ 2/i.test(title) ? pick(['sum', 'sum', 'nat']) : pick(['nth', 'nth', 'sum', 'which']);
      const a = R(-10, 30), d = pick([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 9, 11]), n = R(8, 40), seq = [a, a + d, a + 2 * d, a + 3 * d].map(ind).join(', ');
      if (t === 'nat') { const N = R(10, 150), S = N * (N + 1) / 2; const bb = build(S, [N * N / 2 | 0, N * (N - 1) / 2, S + N, N * (N + 1)], ind, { ok: v => Number.isInteger(v) && v > 0 && v !== S });
        return Q(`Find 1 + 2 + 3 + ... + ${N}.`, bb, `Pair the first and last terms (Gauss's trick): the sum of 1 to n is n(n + 1)/2.`, [`n(n + 1)/2 with n = ${N}`, `${N} × ${N + 1} ÷ 2 = ${ind(S)}`], { t, N }); }
      if (t === 'nth') { const T = a + (n - 1) * d; const bb = build(T, [a + n * d, n * d, a + (n - 2) * d, T + d * 2], ind, { ok: v => v !== T });
        return Q(`Find term number ${n} of the AP ${seq}, ...`, bb, `The nth term of an AP is a + (n − 1)d.`, [`a = ${ind(a)}, d = ${ind(a + d)} − ${pn(a)} = ${ind(d)}`, `Term ${n} = ${pn(a)} + (${n} − 1) × ${pn(d)} = ${pn(a)} + ${n - 1} × ${pn(d)} = ${ind(T)}`], { t, a, d, n }); }
      if (t === 'which') { const T = a + (n - 1) * d; const bb = build(n, [n - 1, n + 1, Math.abs(Math.round((T - a) / d)) + 2, Math.abs(Math.floor(T / d)) || n + 2], ind, { ok: v => v > 0 && v !== n });
        return Q(`Which term of the AP ${seq}, ... is ${ind(T)}?`, bb, `Solve a + (n − 1)d = ${ind(T)} for n.`, [`a = ${ind(a)}, d = ${ind(d)}`, `n − 1 = (${ind(T)} − ${pn(a)}) ÷ ${pn(d)} = ${n - 1}`, `n = ${n - 1} + 1 = ${n}`], { t, a, d, T }); }
      const S = n * (2 * a + (n - 1) * d) / 2; if (!Number.isInteger(S)) throw new Error('retry');
      const bb = build(S, [n * (2 * a + n * d) / 2, n * (a + (n - 1) * d), S + a, (n - 1) * (2 * a + (n - 2) * d) / 2], ind, { ok: v => Number.isInteger(v) && v !== S });
      return Q(`Find the sum of the first ${n} terms of the AP ${seq}, ...`, bb, `Sum of n terms: Sₙ = n/2 × [2a + (n − 1)d].`, [`a = ${ind(a)}, d = ${ind(d)}, n = ${n}`, `2 × ${pn(a)} + (${n} − 1) × ${pn(d)} = ${ind(2 * a + (n - 1) * d)}`, `${n}/2 × ${pn(2 * a + (n - 1) * d)} = ${ind(S)}`], { t, a, d, n });
    } });

  /* ---- 47. Geometric progressions (Grades 9–11) ---- */
  def({ id: 'gp', name: 'Geometric progressions', subj: ['maths'], g: [9, 11], re: /geometric progressions?|G\.P\.|\bGPs?\b/i, not: /graphs|real life|proofs/i,
    make() {
      const a = R(1, 6), r = pick([2, 3, -2, 4, -3, 5]), n = R(4, 8), seq = [a, a * r, a * r * r, a * r ** 3].map(ind).join(', ');
      if (Math.random() < .55) { const T = a * r ** (n - 1); const bb = build(T, [a * r ** n, a * r * (n - 1), T / r * (r + 1) | 0, -T], ind, { ok: v => Number.isInteger(v) && v !== T });
        return Q(`Find term number ${n} of the GP ${seq}, ...`, bb, `The nth term of a GP is a × rⁿ⁻¹.`, [`a = ${a}, r = ${ind(a * r)} ÷ ${a} = ${ind(r)}`, `Term ${n} = ${a} × ${pn(r)}${sup(n - 1)} = ${a} × ${ind(r ** (n - 1))} = ${ind(T)}`], { t: 'nth', a, r, n }); }
      const S = a * (r ** n - 1) / (r - 1);
      const bb = build(S, [a * (r ** (n + 1) - 1) / (r - 1), a * r ** (n - 1), a * (r ** n - 1), S + a], ind, { ok: v => Number.isInteger(v) && v !== S });
      return Q(`Find the sum of the first ${n} terms of the GP ${seq}, ...`, bb, `Sum of n terms of a GP: Sₙ = a(rⁿ − 1)/(r − 1), for r ≠ 1.`, [`a = ${a}, r = ${ind(r)}, n = ${n}`, `${pn(r)}${sup(n)} = ${ind(r ** n)}`, `${a} × (${ind(r ** n)} − 1) ÷ (${pn(r)} − 1) = ${ind(S)}`], { t: 'sum', a, r, n });
    } });

  /* ---- 48. Trigonometric ratios (Grades 9–11) ---- */
  const TV = { sin: { 0: '0', 30: '1/2', 45: '1/√2', 60: '√3/2', 90: '1' }, cos: { 0: '1', 30: '√3/2', 45: '1/√2', 60: '1/2', 90: '0' }, tan: { 0: '0', 30: '1/√3', 45: '1', 60: '√3', 90: 'not defined' },
    cosec: { 0: 'not defined', 30: '2', 45: '√2', 60: '2/√3', 90: '1' }, sec: { 0: '1', 30: '2/√3', 45: '√2', 60: '2', 90: 'not defined' }, cot: { 0: 'not defined', 30: '√3', 45: '1', 60: '1/√3', 90: '0' } };
  const RECIP = { sin: 'cosec', cos: 'sec', tan: 'cot', cosec: 'sin', sec: 'cos', cot: 'tan' };
  const RATIO = { sin: ['opposite', 'hypotenuse'], cos: ['adjacent', 'hypotenuse'], tan: ['opposite', 'adjacent'], cosec: ['hypotenuse', 'opposite'], sec: ['hypotenuse', 'adjacent'], cot: ['adjacent', 'opposite'] };
  def({ id: 'trig', name: 'Trigonometric ratios', subj: ['maths'], g: [9, 11], re: /trigonometric ratios|ratios of standard angles|where the values of 30|all six ratios|first ideas of trigonometry|evaluating expressions/i, not: /identit|algebra|letter/i,
    make({ g }) {
      const t = pick(g === 9 ? ['val', 'tri'] : ['val', 'val', 'tri', 'ang']);
      if (t === 'val') {
        const f = pick(Object.keys(TV)), th = pick([0, 30, 45, 60, 90]), ans = TV[f][th];
        const all = ['0', '1/2', '1/√2', '√3/2', '1', '1/√3', '√3', '2', '√2', '2/√3', 'not defined'];
        const comp = { sin: 'cos', cos: 'sin', tan: 'cot', cot: 'tan', sec: 'cosec', cosec: 'sec' }[f];
        const bb = build(ans, [TV[comp][th], TV[RECIP[f]][th], TV[f][{ 0: 90, 30: 60, 45: 30, 60: 30, 90: 0 }[th]], ...shuffle(all)], s => s);
        return Q(`What is the value of ${f} ${th}°?`, bb, `Learn the table for 0°, 30°, 45°, 60°, 90°. ${f} = ${RATIO[f][0]}/${RATIO[f][1]}.`,
          [`${f} θ = ${RATIO[f][0]} ÷ ${RATIO[f][1]}`, f === 'sin' || f === 'cos' ? `From the standard table, ${f} ${th}° = ${ans}` : `${f} ${th}° comes from sin ${th}° = ${TV.sin[th]} and cos ${th}° = ${TV.cos[th]}`], { t, f, th });
      }
      if (t === 'ang') {
        const f = pick(['sin', 'cos', 'tan']), th = pick([30, 45, 60]), val = TV[f][th];
        const bb = build(th, [90 - th === th ? 30 : 90 - th, 0, 90, th === 45 ? 60 : 45], v => `${v}°`, { ok: v => v !== th });
        return Q(`If ${f} θ = ${val} and θ is acute, what is θ?`, bb, `Match the value with the standard table.`, [`From the table, ${f} ${th}° = ${val}`, `So θ = ${th}°`], { t, f, val });
      }
      const [o, a_, h] = pick([[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [4, 3, 5], [12, 5, 13], [15, 8, 17]]);
      const given = pick(['sin', 'cos', 'tan']), want = pick(['sin', 'cos', 'tan', 'sec', 'cosec', 'cot'].filter(x => x !== given));
      const side = { opposite: o, adjacent: a_, hypotenuse: h }, ratio = f => new Fr(side[RATIO[f][0]], side[RATIO[f][1]]);
      const known = RATIO[given], missing = ['opposite', 'adjacent', 'hypotenuse'].find(x => !known.includes(x));
      const ans = ratio(want);
      const bb = build(ans, [ratio(RECIP[want]), ratio(given), ratio({ sin: 'cos', cos: 'sin', tan: 'cot', cot: 'tan', sec: 'cosec', cosec: 'sec' }[want]), new Fr(o + a_, h)], fs, { ok: v => !v.eq(ans) });
      const st2 = missing === 'hypotenuse' ? `hypotenuse² = ${o}² + ${a_}² = ${o * o + a_ * a_} = ${h}²` : `${missing}² = ${h}² − ${side[known[0] === 'hypotenuse' ? known[1] : known[0]]}² = ${h * h - side[known[0] === 'hypotenuse' ? known[1] : known[0]] ** 2} = ${side[missing]}²`;
      return Q(`If ${given} θ = ${fs(ratio(given))} and θ is acute, find ${want} θ.`, bb, `Draw a right triangle, label two sides from the given ratio and find the third side by Pythagoras.`,
        [`Take ${known[0]} = ${side[known[0]]} and ${known[1]} = ${side[known[1]]}`, st2, `${want} θ = ${RATIO[want][0]} ÷ ${RATIO[want][1]} = ${side[RATIO[want][0]]}/${side[RATIO[want][1]]}`], { t, given, gv: fs(ratio(given)), want });
    } });

  /* ---- 49. Heights and distances (Grade 10) ---- */
  def({ id: 'heights', name: 'Heights and distances', subj: ['maths'], g: [10, 10], re: /angles? of elevation|finding heights|finding distances|poles across|balloons/i,
    make() {
      const th = pick([30, 45, 60]), d = 3 * R(2, 20), findH = Math.random() < .6;
      const fmtS = ([k, s]) => (s ? (k === 1 ? '' : ind(k)) + '√3' : ind(k)) + ' m';
      let ans, wr, st;
      if (findH) { ans = th === 45 ? [d, 0] : th === 60 ? [d, 1] : [d / 3, 1]; wr = [th === 60 ? [d / 3, 1] : [d, 1], [d, 0], [2 * d, 0], th === 45 ? [d, 1] : [2 * d, 1]];
        st = [`tan ${th}° = height ÷ distance`, `tan ${th}° = ${TV.tan[th]}`, `height = ${d} × tan ${th}° = ${fmtS(ans)}`]; }
      else { ans = th === 45 ? [d, 0] : th === 30 ? [d, 1] : [d / 3, 1]; wr = [th === 30 ? [d / 3, 1] : [d, 1], [d, 0], [2 * d, 0], th === 45 ? [d / 3, 1] : [2 * d, 1]];
        st = [`tan ${th}° = height ÷ distance, so distance = height ÷ tan ${th}°`, `tan ${th}° = ${TV.tan[th]}`, `distance = ${d} ÷ ${TV.tan[th]} = ${fmtS(ans)}`]; }
      const bb = build(ans, wr, fmtS, { ok: ([k]) => Number.isInteger(k) && k > 0 });
      return Q(findH ? `From a point ${d} m away from the foot of a tower, the angle of elevation of its top is ${th}°. How tall is the tower?` : `A tower is ${d} m tall. The angle of elevation of its top from a point on the ground is ${th}°. How far is the point from the foot of the tower?`,
        bb, `In the right triangle, tan(angle) = opposite ÷ adjacent = height ÷ distance.`, st, { findH, th, d });
    } });

  /* ---- 50. Distance formula (Grades 9–11) ---- */
  def({ id: 'distance', name: 'Distance formula', subj: ['maths'], g: [9, 11], re: /distance formula|quadrants and distances|distance between two points|using distances/i, not: /from a line/i,
    make({ g, title }) {
      const three = /space/i.test(title);
      const tr = three ? pick([[1, 2, 2, 3], [2, 3, 6, 7], [1, 4, 8, 9], [4, 4, 7, 9], [2, 6, 9, 11], [6, 6, 7, 11], [2, 10, 11, 15]]) : pick([[3, 4, 5], [5, 12, 13], [6, 8, 10], [8, 15, 17], [7, 24, 25], [9, 12, 15], [12, 16, 20]]);
      const dim = three ? 3 : 2, P = Array.from({ length: dim }, () => R(-8, 8)), dlt = shuffle(tr.slice(0, dim)).map(x => x * pick([-1, 1])), Q_ = P.map((x, i) => x + dlt[i]), dist = tr[dim];
      const pt = a => `(${a.map(ind).join(', ')})`, sq = dlt.reduce((s, x) => s + x * x, 0), nmz = three ? ['x', 'y', 'z'] : ['x', 'y'];
      const bb = build(dist, [dlt.reduce((s, x) => s + Math.abs(x), 0), sq, Q_.reduce((s, x, i) => s + Math.abs(x + P[i]), 0) || dist + 2, dist + 1], v => `${ind(v)} units`, { ok: v => v > 0 && v !== dist });
      return Q(`Find the distance between the points ${pt(P)} and ${pt(Q_)}.`, bb, `Distance = √[(x₂ − x₁)² + (y₂ − y₁)²${three ? ' + (z₂ − z₁)²' : ''}].`,
        [nmz.map((n_, i) => `${n_}: ${pn(Q_[i])} − ${pn(P[i])} = ${ind(dlt[i])}`).join(', '), `${dlt.map(x => pn(x) + '²').join(' + ')} = ${dlt.map(x => x * x).join(' + ')} = ${sq}`, `${dist} × ${dist} = ${sq}, so the distance is √${sq} = ${dist}`], { P, Q: Q_ });
    } });

  /* ---- 51. Section formula and mid-point (Grades 9–12) ---- */
  def({ id: 'section', name: 'Section formula', subj: ['maths'], g: [9, 12], re: /section formula|midpoints? and points|mid-point$|points of trisection|section formula and mid-point/i,
    make({ title }) {
      const mid = /mid/i.test(title) && Math.random() < .5; const m = mid ? 1 : R(1, 4), n = mid ? 1 : R(1, 4); if (!mid && m === n) throw new Error('retry');
      const Pt = [R(-8, 8), R(-8, 8)], k = [R(-3, 3) || 1, R(-3, 3) || 2], A = Pt.map((x, i) => x - m * k[i]), B = Pt.map((x, i) => x + n * k[i]);
      const pt = a => `(${a.map(ind).join(', ')})`, fmt = a => pt(a), swap = A.map((x, i) => (n * B[i] + m * x)), mm = m + n;
      const cand = [swap.every(x => x % mm === 0) ? swap.map(x => x / mm) : null, A.map((x, i) => (x + B[i]) % 2 === 0 ? (x + B[i]) / 2 : null).includes(null) ? null : A.map((x, i) => (x + B[i]) / 2), A.map((x, i) => B[i] - x), Pt.map(x => -x), [Pt[1], Pt[0]]];
      const bb = build(Pt, cand, fmt, { ok: a => a.every(Number.isInteger) });
      return Q(mid ? `Find the mid-point of the line segment joining ${pt(A)} and ${pt(B)}.` : `Find the point that divides the segment joining A${pt(A)} and B${pt(B)} internally in the ratio ${m} : ${n}.`, bb,
        `Section formula: ((m x₂ + n x₁)/(m + n), (m y₂ + n y₁)/(m + n)). The mid-point is the case m = n = 1.`,
        [`x: (${m} × ${pn(B[0])} + ${n} × ${pn(A[0])}) ÷ ${mm} = ${ind(m * B[0] + n * A[0])} ÷ ${mm} = ${ind(Pt[0])}`, `y: (${m} × ${pn(B[1])} + ${n} × ${pn(A[1])}) ÷ ${mm} = ${ind(m * B[1] + n * A[1])} ÷ ${mm} = ${ind(Pt[1])}`], { A, B, m, n });
    } });

  /* ---- 52. Speed, distance and time (maths 5–8, science 6–10, physics 11) ---- */
  def({ id: 'speed', name: 'Speed, distance and time', subj: ['maths', 'science', 'physics'], g: [5, 11], re: /\bspeed\b|rates and speed|distance and displacement/i, not: /round|angular|escape|orbital|wave|sound|rms|terminal|banked|optimum|velocity–time|safe speed|instantaneous|light/i,
    make({ g }) {
      const t = pick(g >= 9 ? ['s', 'd', 't', 'conv', 'avg'] : ['s', 'd', 't', 's', 'conv']);
      if (t === 'conv') { const toMs = Math.random() < .5; const v = toMs ? 18 * R(1, 8) : 5 * R(1, 8), ans = toMs ? v * 5 / 18 : v * 18 / 5;
        const bb = build(ans, [toMs ? v * 18 / 5 : v * 5 / 18, v / 60 * 1000 | 0, ans * 10, ans + 5], x => `${nm(x)} ${toMs ? 'm/s' : 'km/h'}`, { ok: x => F(x).p > 0 && !F(x).eq(F(ans)) && dec(x, 2) !== null });
        return Q(`Convert ${v} ${toMs ? 'km/h to m/s' : 'm/s to km/h'}.`, bb, `1 km/h = 1000 m ÷ 3600 s = 5/18 m/s.`, [toMs ? `Multiply by 5/18` : `Multiply by 18/5`, `${v} × ${toMs ? '5/18' : '18/5'} = ${nm(ans)}`], { t, v, toMs }); }
      if (t === 'avg') { const s1 = pick([30, 40, 60]), t1 = R(1, 3), s2 = pick([20, 50, 80]), t2 = R(1, 3), D1 = s1 * t1, D2 = s2 * t2, av = new Fr(D1 + D2, t1 + t2); if (dec(av, 2) === null) throw new Error('retry');
        const bb = build(av, [new Fr(s1 + s2, 2), F(D1 + D2), new Fr(D1 + D2, 2), av.add(5)], x => `${dec(x, 2) ?? 'x'} km/h`, { ok: x => dec(x, 2) !== null && !F(x).eq(av) });
        return Q(`A bus travels at ${s1} km/h for ${t1} h and then at ${s2} km/h for ${t2} h. What is its average speed?`, bb, `Average speed = total distance ÷ total time (not the average of the two speeds).`,
          [`Distances: ${s1} × ${t1} = ${D1} km, ${s2} × ${t2} = ${D2} km`, `Total: ${D1} + ${D2} = ${D1 + D2} km in ${t1} + ${t2} = ${t1 + t2} h`, `${D1 + D2} ÷ ${t1 + t2} = ${dec(av, 2)}`], { t, s1, t1, s2, t2 }); }
      const sp = R(3, 90), tm = pick([1, 2, 3, 4, 5, 6, 1.5, 2.5, 0.5]), T = F(tm), Dv = T.mul(sp), m = Math.random() < .5;
      const u = m ? ['m', 's', 'm/s'] : ['km', 'h', 'km/h'];
      if (t === 's') { const bb = build(F(sp), [Dv.mul(T), Dv.add(T), F(sp).mul(2), F(sp + 1)], x => `${nm(x)} ${u[2]}`, { ok: x => F(x).p > 0 && dec(x, 2) !== null && !F(x).eq(F(sp)) });
        return Q(`A cyclist covers ${nm(Dv)} ${u[0]} in ${nm(T)} ${u[1]}. What is the speed?`, bb, `Speed = distance ÷ time.`, [`Speed = distance ÷ time`, `${nm(Dv)} ÷ ${nm(T)} = ${sp}`], { t, D: nm(Dv), T: nm(T) }); }
      if (t === 'd') { const bb = build(Dv, [F(sp).div(T), F(sp).add(T), Dv.mul(2), Dv.add(sp)], x => `${nm(x)} ${u[0]}`, { ok: x => F(x).p > 0 && dec(x, 2) !== null && !F(x).eq(Dv) });
        return Q(`A train moves at ${sp} ${u[2]} for ${nm(T)} ${u[1]}. How far does it go?`, bb, `Distance = speed × time.`, [`Distance = speed × time`, `${sp} × ${nm(T)} = ${nm(Dv)}`], { t, s: sp, T: nm(T) }); }
      const bb = build(T, [Dv.mul(sp), F(sp).div(Dv), T.add(1), T.mul(2)], x => `${nm(x)} ${u[1]}`, { ok: x => F(x).p > 0 && dec(x, 2) !== null && !F(x).eq(T) });
      return Q(`How long does it take to cover ${nm(Dv)} ${u[0]} at ${sp} ${u[2]}?`, bb, `Time = distance ÷ speed.`, [`Time = distance ÷ speed`, `${nm(Dv)} ÷ ${sp} = ${nm(T)}`], { t, D: nm(Dv), s: sp });
    } });

  /* ---- 53. Unit conversion: length, mass, capacity, area (Grades 3–8) ---- */
  def({ id: 'units', name: 'Converting units', subj: ['maths'], g: [3, 8], re: /convert|converting|metre and centimetre|metres and centimetres|millimetres|changing mm|grams and kilograms|millilitres and litres|milligrams|quintals|kilogram, half|half litre|the litre|^the metre$|weight in grams|half metre/i, not: /temperature|radian/i,
    make({ g, title }) {
      const T = [];
      if (/length|metre|centimetre|mm|millimetre|km|distance/i.test(title)) T.push(['m', 'cm', 100], ['km', 'm', 1000], ['cm', 'mm', 10]);
      if (/gram|weight|kilogram|quintal|tonne/i.test(title)) T.push(['kg', 'g', 1000], ...(/milligram/i.test(title) ? [['g', 'mg', 1000]] : []), ...(/quintal|tonne/i.test(title) ? [['quintal', 'kg', 100], ['tonne', 'kg', 1000]] : []));
      if (/litre|capacity/i.test(title)) T.push(['L', 'mL', 1000]);
      if (/area/i.test(title) && g >= 7) T.push(['m²', 'cm²', 10000]);
      if (!T.length) T.push(['m', 'cm', 100], ['kg', 'g', 1000], ['L', 'mL', 1000], ['km', 'm', 1000]);
      let [B, S, k] = pick(T); if (g === 3 && k === 1000 && B === 'km') [B, S, k] = ['m', 'cm', 100];
      const mode = g === 3 ? pick(['mix', 'half']) : pick(['mix', 'toSmall', 'toBig']);
      if (mode === 'half' && S !== 'mm') { const fr = pick([[1, 2], [1, 4], [3, 4]]), v = k * fr[0] / fr[1]; if (!Number.isInteger(v)) throw new Error('retry');
        const nmF = { '1/2': 'half', '1/4': 'a quarter', '3/4': 'three quarters' }[fr.join('/')];
        const bb = build(v, [k / 10 * fr[0] / fr[1] | 0 || 25, v * 2, k - v, v + 50].filter(x => x !== v), x => `${ind(x)} ${S}`, { ok: x => Number.isInteger(x) && x > 0 });
        return Q(`How many ${S} make ${nmF} of a ${{ m: 'metre', kg: 'kilogram', L: 'litre', km: 'kilometre', cm: 'centimetre', g: 'gram' }[B] || B}?`, bb, `1 ${B} = ${ind(k)} ${S}.`, [`1 ${B} = ${ind(k)} ${S}`, `${fr[0]}/${fr[1]} of ${ind(k)} = ${ind(k)} ÷ ${fr[1]}${fr[0] > 1 ? ` × ${fr[0]}` : ''} = ${ind(v)}`], { mode, B, S, k, f: fr }); }
      if (mode === 'mix') { const big = R(1, 20), small = R(1, k - 1), v = big * k + small, sm = String(small);
        const bb = build(v, [+(String(big) + sm), big * k + small * 10, big * 10 + small, big + small], x => `${ind(x)} ${S}`, { ok: x => x > 0 && x !== v });
        return Q(`${big} ${B} ${small} ${S} = how many ${S}?`, bb, `1 ${B} = ${ind(k)} ${S}. Change the ${B} to ${S}, then add the ${S}.`, [`${big} ${B} = ${big} × ${ind(k)} = ${ind(big * k)} ${S}`, `${ind(big * k)} + ${small} = ${ind(v)}`], { mode, B, S, k, big, small }); }
      const n = mode === 'toSmall' ? F(pick(['1.5', '2.25', '0.75', '3.5', '0.5', '4.2', '12', '7', '0.25', '6.8'])) : null;
      if (mode === 'toSmall') { const v = n.mul(k); if (!v.int) throw new Error('retry');
        const bb = build(v, [n.mul(k / 10), n.mul(k * 10), n.add(k), v.add(k)], x => `${nm(x)} ${S}`, { ok: x => F(x).p > 0 && dec(x, 4) !== null && !F(x).eq(v) });
        return Q(`Convert ${nm(n)} ${B} to ${S}.`, bb, `To change ${B} to ${S}, multiply by ${ind(k)} (1 ${B} = ${ind(k)} ${S}).`, [`1 ${B} = ${ind(k)} ${S}`, `${nm(n)} × ${ind(k)} = ${nm(v)}`], { mode, B, S, k, n: nm(n) }); }
      const s = F(R(1, 9) * pick([k / 10, k / 4, k / 2, k * 3 / 4, k * 1.5, k / 20].filter(Number.isInteger)) + (Math.random() < .5 ? 0 : R(1, 9) * k / (k >= 1000 ? 100 : 10))), v = s.div(k);
      if (dec(v, 4) === null) throw new Error('retry');
      const bb = build(v, [s.div(k / 10), s.div(k * 10), s.mul(k), v.add(1)], x => `${dec(x, 6) ?? 'x'} ${B}`, { ok: x => F(x).p > 0 && dec(x, 6) !== null && !F(x).eq(v) });
      return Q(`Convert ${nm(s)} ${S} to ${B}.`, bb, `To change ${S} to ${B}, divide by ${ind(k)} (1 ${B} = ${ind(k)} ${S}).`, [`1 ${B} = ${ind(k)} ${S}`, `${nm(s)} ÷ ${ind(k)} = ${nm(v)}`], { mode: 'toBig', B, S, k, s: nm(s) });
    } });

  /* ---- 54. Time and durations (Grades 2–5) ---- */
  const clk = m => { m = ((m % 1440) + 1440) % 1440; const h = Math.floor(m / 60), mi = m % 60, ap = h < 12 ? 'am' : 'pm', hh = h % 12 || 12; return `${hh}:${String(mi).padStart(2, '0')} ${ap}`; };
  const dur = m => { const h = Math.floor(m / 60), mi = m % 60; return [h ? `${h} h` : '', mi ? `${mi} min` : ''].filter(Boolean).join(' ') || '0 min'; };
  def({ id: 'time', name: 'Time and durations', subj: ['maths'], g: [2, 5], re: /how long|duration|hours to minutes|seconds, minutes|start times|how many hours in a day|minutes, hours/i, not: /trip\?$/i,
    make({ g, title }) {
      const t = /hours to minutes|seconds, minutes|minutes, hours|hours in a day/i.test(title) ? 'conv' : /start times|backwards/i.test(title) ? 'start' : g <= 3 ? pick(['conv', 'between']) : pick(['between', 'end', 'start', 'conv']);
      if (t === 'conv') { const h = R(1, g <= 3 ? 4 : 9), m = pick([0, 5, 10, 15, 20, 30, 40, 45]), v = h * 60 + m;
        const bb = build(v, [h * 100 + m, h + m, h * 60, v + 60, h * 10 + m].filter(x => x !== v), x => `${ind(x)} min`, { ok: x => x > 0 });
        return Q(`How many minutes are there in ${dur(v)}?`, bb, `1 hour = 60 minutes.`, [`${h} h = ${h} × 60 = ${h * 60} min`, ...(m ? [`${h * 60} + ${m} = ${v}`] : [`So ${dur(v)} = ${v} min`])], { t, h, m }); }
      const s = R(6 * 12, 17 * 12) * 5, d = R(3, g <= 3 ? 24 : 54) * 5, e = s + d;
      const stepsBetween = () => { const nh = Math.ceil(s / 60) * 60, a = nh - s, b = Math.floor((e - nh) / 60), c = e - nh - b * 60; if (nh > e) return [`From ${clk(s)} to ${clk(e)} is ${d} min`]; return [`From ${clk(s)} to ${clk(nh)} is ${a} min`, ...(b ? [`From ${clk(nh)} to ${clk(nh + b * 60)} is ${b} h`] : []), ...(c ? [`From ${clk(nh + b * 60)} to ${clk(e)} is ${c} min`] : []), `Total: ${dur(d)}`]; };
      if (t === 'between') { const bb = build(d, [d + 40, d - 40, d + 60, d + 10, Math.abs(Math.floor(e / 60) - Math.floor(s / 60)) * 100 + Math.abs(e % 60 - s % 60)], dur, { ok: x => x > 0 && x < 600 });
        return Q(`A school trip starts at ${clk(s)} and ends at ${clk(e)}. How long is the trip?`, bb, `Count on: first to the next full hour, then whole hours, then the extra minutes.`, stepsBetween().slice(0, 5), { t, s, e }); }
      if (t === 'end') { const bb = build(e, [e + 40, e - 40, s - d, e + 60], clk, { ok: x => x !== e });
        return Q(`A cricket match starts at ${clk(s)} and lasts ${dur(d)}. When does it end?`, bb, `Add the hours, then the minutes. 60 minutes make 1 hour.`, [`Start: ${clk(s)}`, `Add ${dur(d)}`, `End: ${clk(e)}`], { t, s, d }); }
      const bb = build(s, [s + 40, s - 40, e + d, s + 60], clk, { ok: x => x !== s });
      return Q(`A film ends at ${clk(e)}. It lasted ${dur(d)}. When did it start?`, bb, `Work backwards: subtract the duration from the end time.`, [`End: ${clk(e)}`, `Go back ${dur(d)}`, `Start: ${clk(s)}`], { t, e, d });
    } });

  /* ---- 55. Pythagoras theorem (Grades 7–9) ---- */
  def({ id: 'pythag', name: 'Pythagoras theorem', subj: ['maths'], g: [7, 9], re: /pythag|right triangles and the theorem|baudhayana|primitive triples/i, not: /history|fermat|proof ideas/i,
    make({ title }) {
      const base = pick([[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41]]), k = base[0] === 3 ? R(1, 6) : R(1, 2), [a, b, c] = base.map(x => x * k);
      if (/triple/i.test(title) && Math.random() < .6) {
        const good = [a, b, c], bad = () => { const x = [a, b, c].slice(); x[R(0, 2)] += pick([-1, 1, 2]); return x; };
        const bb = build(good, [bad(), bad(), bad(), [a, b, c + 1], [a + 1, b + 1, c + 1]], x => `(${x.join(', ')})`, { ok: x => x[0] * x[0] + x[1] * x[1] !== x[2] * x[2] && x[0] < x[2] && x[1] < x[2] });
        return Q(`Which of these is a Pythagorean triple?`, bb, `(a, b, c) is a Pythagorean triple when a² + b² = c².`, [`${a}² + ${b}² = ${a * a} + ${b * b} = ${a * a + b * b}`, `${c}² = ${c * c}, so the two sides match`], { t: 'triple' });
      }
      const hyp = Math.random() < .55, u = pick(['cm', 'm']);
      if (hyp) { const bb = build(c, [a + b, a * a + b * b, c + 1, Math.abs(b - a) + c / 2 | 0], v => `${ind(v)} ${u}`, { ok: v => v > 0 && v !== c });
        return Q(`A right triangle has legs ${a} ${u} and ${b} ${u}. How long is the hypotenuse?`, bb, `In a right triangle, hypotenuse² = leg² + leg².`, [`${a}² + ${b}² = ${a * a} + ${b * b} = ${ind(a * a + b * b)}`, `${c} × ${c} = ${ind(c * c)}, so the hypotenuse is ${c}`], { t: 'h', a, b }); }
      const bb = build(b, [c - a, c + a, c * c - a * a, b + 1], v => `${ind(v)} ${u}`, { ok: v => v > 0 && v !== b });
      return Q(`A ladder ${c} ${u} long leans against a wall. Its foot is ${a} ${u} from the wall. How high up the wall does it reach?`, bb, `The ladder is the hypotenuse, so height² = ladder² − base².`, [`${c}² − ${a}² = ${c * c} − ${a * a} = ${ind(c * c - a * a)}`, `${b} × ${b} = ${ind(b * b)}, so the height is ${b}`], { t: 'l', a, c });
    } });

  /* ---- 56. Angles: triangles, straight lines, parallel lines (Grades 6–9) ---- */
  def({ id: 'angles', name: 'Finding unknown angles', subj: ['maths'], g: [6, 9], re: /angle sum|why 180|angles on a straight line|intersecting lines and their angles|transversals and angles|unknown angles with parallel|angles of isosceles/i,
    make({ title }) {
      const t = /diagonals/i.test(title) ? 'quad' : /isosceles/i.test(title) ? 'iso' : /straight|intersecting/i.test(title) ? pick(['line', 'vert']) : /parallel|transversal/i.test(title) ? pick(['corr', 'coint']) : 'tri';
      const deg = v => `${v}°`;
      if (t === 'tri') { const a = R(20, 100), b = R(15, 160 - a - 5), c = 180 - a - b;
        const bb = build(c, [360 - a - b, 180 - a, 90 - Math.min(a, b) > 0 ? 180 - a - b + 10 : c + 20, a + b], deg, { ok: v => v > 0 && v < 360 && v !== c });
        return Q(`Two angles of a triangle are ${a}° and ${b}°. Find the third angle.`, bb, `The three angles of a triangle add up to 180°.`, [`${a}° + ${b}° = ${a + b}°`, `180° − ${a + b}° = ${c}°`], { t, a, b }); }
      if (t === 'quad') { const a = R(50, 120), b = R(50, 120), c = R(50, 120), d = 360 - a - b - c; if (d <= 10 || d >= 200) throw new Error('retry');
        const bb = build(d, [180 - a - b - c + 360 > 0 ? 540 - a - b - c : d + 30, 360 - a - b, d + 10, 180 - c], deg, { ok: v => v > 0 && v !== d });
        return Q(`Three angles of a quadrilateral are ${a}°, ${b}° and ${c}°. Find the fourth angle.`, bb, `The angles of a quadrilateral add up to 360° (two triangles).`, [`${a}° + ${b}° + ${c}° = ${a + b + c}°`, `360° − ${a + b + c}° = ${d}°`], { t, a, b, c }); }
      if (t === 'iso') { const ap = 2 * R(10, 80), base = (180 - ap) / 2;
        const bb = build(base, [180 - ap, ap, 90 - ap / 2 + 10, (180 - ap) / 3 | 0], deg, { ok: v => v > 0 && v !== base });
        return Q(`In an isosceles triangle the angle between the two equal sides is ${ap}°. Find each of the other two angles.`, bb, `The two base angles of an isosceles triangle are equal and all three add up to 180°.`, [`180° − ${ap}° = ${180 - ap}°`, `${180 - ap}° ÷ 2 = ${base}°`], { t, ap }); }
      const a = R(25, 155); if (a === 90) throw new Error('retry');
      if (t === 'line') { const bb = build(180 - a, [a, 360 - a, 90 - a > 0 ? 90 - a : 270 - a, 180 - a + 10], deg, { ok: v => v > 0 && v !== 180 - a });
        return Q(`Two angles form a linear pair (they sit on a straight line). One is ${a}°. Find the other.`, bb, `Angles on a straight line add up to 180°.`, [`Angles on a straight line add to 180°`, `180° − ${a}° = ${180 - a}°`], { t, a }); }
      if (t === 'vert') { const bb = build(a, [180 - a, 360 - a, 90 + a > 180 ? a - 10 : 90 + a], deg, { ok: v => v > 0 && v !== a });
        return Q(`Two straight lines cross. One of the angles formed is ${a}°. What is the angle vertically opposite to it?`, bb, `Vertically opposite angles are equal.`, [`Vertically opposite angles are equal`, `So the angle is ${a}°, and its neighbours are 180° − ${a}° = ${180 - a}°`], { t, a }); }
      if (t === 'corr') { const bb = build(a, [180 - a, 90 - a > 0 ? 90 - a : a - 15, 360 - a], deg, { ok: v => v > 0 && v !== a });
        return Q(`A transversal cuts two parallel lines. One angle is ${a}°. What is its corresponding angle?`, bb, `When lines are parallel, corresponding angles are equal.`, [`Corresponding angles are equal for parallel lines`, `So it is ${a}° (its neighbour would be 180° − ${a}° = ${180 - a}°)`], { t, a }); }
      const bb = build(180 - a, [a, 360 - a, 90 + (a > 90 ? -a + 90 + 20 : a), 180 - a + 10], deg, { ok: v => v > 0 && v < 360 && v !== 180 - a });
      return Q(`A transversal cuts two parallel lines. One interior angle is ${a}°. Find the co-interior angle on the same side of the transversal.`, bb, `Co-interior angles between parallel lines add up to 180°.`, [`Co-interior angles add to 180°`, `180° − ${a}° = ${180 - a}°`], { t, a });
    } });

  /* ---- 57. Probability (Grades 9–11) ---- */
  const DECK = []; ['hearts', 'diamonds', 'clubs', 'spades'].forEach(s => ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'].forEach(r => DECK.push({ s, r, red: s === 'hearts' || s === 'diamonds' })));
  const CARD_EV = { 'a king': c => c.r === 'K', 'a red card': c => c.red, 'a face card (J, Q or K)': c => 'JQK'.includes(c.r) && c.r.length === 1, 'a heart': c => c.s === 'hearts', 'the ace of spades': c => c.r === 'A' && c.s === 'spades', 'a black face card': c => !c.red && ['J', 'Q', 'K'].includes(c.r), 'a red king': c => c.red && c.r === 'K', 'a card that is not an ace': c => c.r !== 'A' };
  const DIE_EV = { 'an even number': x => x % 2 === 0, 'a prime number': x => [2, 3, 5].includes(x), 'a number greater than 4': x => x > 4, 'a multiple of 3': x => x % 3 === 0, 'a number less than 3': x => x < 3, 'a number greater than 6': x => x > 6, 'a number less than 7': x => x < 7 };
  def({ id: 'probability', name: 'Probability', subj: ['maths'], g: [9, 11], re: /theoretical probability|coins and dice|cards, balls|probability with counting|equally likely outcomes|probability scale|experimental probability|^probability$/i, not: /conditional|bayes|independent|multiplication theorem|fallacy/i,
    make() {
      const t = pick(['bag', 'die', 'cards', 'coins', 'exp']); let f, n, q, fav;
      if (t === 'bag') { const cols = shuffle(['red', 'blue', 'green', 'yellow']).slice(0, 3), ns = cols.map(() => R(1, 12)), k = R(0, 2); f = ns[k]; n = ns.reduce((a, b) => a + b, 0);
        q = `A bag has ${cols.map((c, i) => `${ns[i]} ${c}`).join(', ')} balls. One ball is picked at random. What is the probability that it is ${cols[k]}?`; fav = `${f} ${cols[k]} balls`; }
      else if (t === 'die') { const ev = pick(Object.keys(DIE_EV)); f = [1, 2, 3, 4, 5, 6].filter(DIE_EV[ev]).length; n = 6; q = `A fair die is thrown once. What is the probability of getting ${ev}?`; fav = f ? `${[1, 2, 3, 4, 5, 6].filter(DIE_EV[ev]).join(', ')}, which is ${f} outcome${f > 1 ? 's' : ''}` : 'none'; }
      else if (t === 'cards') { const ev = pick(Object.keys(CARD_EV)); f = DECK.filter(CARD_EV[ev]).length; n = 52; q = `One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it is ${ev}?`; fav = `${f} such cards`; }
      else if (t === 'coins') { const ev = pick(['exactly one head', 'at least one head', 'two heads', 'no head']); const out = ['HH', 'HT', 'TH', 'TT'], c = s => (s.match(/H/g) || []).length;
        const pr = { 'exactly one head': s => c(s) === 1, 'at least one head': s => c(s) >= 1, 'two heads': s => c(s) === 2, 'no head': s => c(s) === 0 }[ev]; f = out.filter(pr).length; n = 4; q = `Two coins are tossed together. What is the probability of getting ${ev}?`; fav = out.filter(pr).join(', '); }
      else { n = pick([20, 25, 40, 50, 60, 80, 100]); f = R(3, n - 3); q = `A coin is tossed ${n} times and shows heads ${f} times. What is the experimental probability of getting a head?`; fav = `${f} heads`; }
      const p = new Fr(f, n);
      const bb = build(p, [f < n && f ? new Fr(n - f, n) : new Fr(1, n), f && f < n ? new Fr(f, n - f) : new Fr(2, n), new Fr(1, Math.max(2, f)), p.int ? new Fr(1, 2) : new Fr(p.p, p.q + 1)], fs, { ok: v => v.p >= 0 && v.v <= 1 && !v.eq(p) });
      return Q(q, bb, `Probability = number of favourable outcomes ÷ total number of outcomes.`, [`Total outcomes: ${n}`, `Favourable: ${fav}`, f && n / gcd(f, n) !== n ? `P = ${f}/${n} = ${fs(p)}` : `P = ${f}/${n}`], { t, q });
    } });

  /* ---- 58. Permutations and combinations (Grade 11) ---- */
  const WORDS = ['MANGO', 'TIGER', 'PLANE', 'CHAIR', 'BLACK', 'INDIA', 'APPLE', 'BANANA', 'LETTER', 'COFFEE', 'MUMBAI', 'KERALA', 'DELHI', 'PUNE'];
  def({ id: 'permcomb', name: 'Permutations and combinations', subj: ['maths'], g: [11, 11], re: /permutation|combination|factorial|fundamental principle of counting|counting with and without|committees|select then arrange|arrangements with alike/i, not: /dictionary/i,
    make({ title }) {
      const t = /alike/i.test(title) ? 'word' : /combination|committee/i.test(title) ? pick(['ncr', 'comm']) : /permutation|factorial/i.test(title) ? pick(['npr', 'word', 'fact']) : pick(['npr', 'ncr', 'word', 'comm', 'mul']);
      if (t === 'mul') { const s = R(2, 6), p = R(2, 6), sh = R(2, 5), v = s * p * sh; const bb = build(v, [s + p + sh, s * p + sh, v * 2, s * p], ind, { ok: x => x > 0 && x !== v });
        return Q(`A student has ${s} shirts, ${p} pairs of trousers and ${sh} pairs of shoes. How many different outfits can be made?`, bb, `Fundamental principle of counting: multiply the number of choices at each step.`, [`Choices: ${s}, ${p} and ${sh}`, `${s} × ${p} × ${sh} = ${v}`], { t, s, p, sh }); }
      if (t === 'fact') { const n = R(4, 9), v = fact(n); const bb = build(v, [fact(n - 1), n * (n + 1) / 2, v * (n + 1), n * n], ind, { ok: x => x > 0 && x !== v });
        return Q(`What is ${n}! ?`, bb, `n! = n × (n − 1) × ... × 2 × 1.`, [`${n}! = ${Array.from({ length: n }, (_, k) => n - k).join(' × ')} = ${ind(v)}`], { t, n }); }
      if (t === 'npr' || t === 'ncr') { const n = R(5, 12), r = R(2, Math.min(5, n - 1)), p = nPr(n, r), c = nCr(n, r), isP = t === 'npr', v = isP ? p : c;
        const bb = build(v, [isP ? c : p, isP ? n ** r : nCr(n, r - 1) === c ? nCr(n, r + 1) : nCr(n, r - 1), isP ? nPr(n, r - 1) : c * 2, n * r], ind, { ok: x => x > 0 && x !== v });
        return Q(isP ? `In how many ways can ${r} students be chosen from ${n} to be captain, vice-captain${r > 2 ? ' and other posts (all different)' : ''}? Find P(${n}, ${r}).` : `In how many ways can ${r} students be chosen from ${n} for a team (order does not matter)? Find C(${n}, ${r}).`, bb,
          isP ? `P(n, r) = n!/(n − r)! — order matters.` : `C(n, r) = n!/(r!(n − r)!) — order does not matter.`,
          isP ? [`P(${n}, ${r}) = ${Array.from({ length: r }, (_, k) => n - k).join(' × ')}`, `${Array.from({ length: r }, (_, k) => n - k).join(' × ')} = ${ind(p)}`] : [`P(${n}, ${r}) = ${Array.from({ length: r }, (_, k) => n - k).join(' × ')} = ${ind(p)}`, `Divide by ${r}! = ${fact(r)} because order does not matter: ${ind(p)} ÷ ${fact(r)} = ${ind(c)}`], { t, n, r }); }
      if (t === 'comm') { const m = R(4, 8), w = R(3, 7), a = R(1, Math.min(3, m)), b = R(1, Math.min(3, w)), v = nCr(m, a) * nCr(w, b);
        const bb = build(v, [nCr(m, a) + nCr(w, b), nCr(m + w, a + b), nPr(m, a) * nPr(w, b), v * 2], ind, { ok: x => x > 0 && x !== v });
        return Q(`A committee of ${a} boy${a > 1 ? 's' : ''} and ${b} girl${b > 1 ? 's' : ''} is to be chosen from ${m} boys and ${w} girls. In how many ways can this be done?`, bb, `Choose the boys and the girls separately, then multiply.`, [`Boys: C(${m}, ${a}) = ${nCr(m, a)}`, `Girls: C(${w}, ${b}) = ${nCr(w, b)}`, `${nCr(m, a)} × ${nCr(w, b)} = ${ind(v)}`], { t, m, w, a, b }); }
      const word = pick(WORDS), L = word.length, cnt = {}; word.split('').forEach(c => cnt[c] = (cnt[c] || 0) + 1);
      const reps = Object.entries(cnt).filter(([, k]) => k > 1), den = reps.reduce((s, [, k]) => s * fact(k), 1), v = fact(L) / den;
      const bb = build(v, [fact(L), v * 2 === fact(L) ? fact(L) / 3 | 0 : v * 2, fact(L - 1), L * L], ind, { ok: x => x > 0 && x !== v });
      return Q(`How many different arrangements can be made with all the letters of the word ${word}?`, bb, reps.length ? `When letters repeat, divide by the factorial of each repeat count.` : `All ${L} letters are different, so the number of arrangements is ${L}!.`,
        reps.length ? [`${L} letters: ${L}! = ${ind(fact(L))}`, `Repeats: ${reps.map(([c, k]) => `${c} appears ${k} times`).join(', ')}`, `${ind(fact(L))} ÷ ${reps.map(([, k]) => k + '!').join(' × ')} = ${ind(fact(L))} ÷ ${den} = ${ind(v)}`] : [`${L} different letters`, `${L}! = ${Array.from({ length: L }, (_, k) => L - k).join(' × ')} = ${ind(v)}`], { t: 'word', word });
    } });

  /* ---- 59. Complex numbers (Grade 11) ---- */
  const cx = (a, b) => b === 0 ? ind(a) : a === 0 ? (b === 1 ? 'i' : b === -1 ? '−i' : ind(b) + 'i') : `${ind(a)} ${b < 0 ? '−' : '+'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}i`;
  def({ id: 'complex', name: 'Complex numbers', subj: ['maths'], g: [11, 11], re: /complex numbers|powers of i|imaginary unit|modulus and conjugate|multiplying complex|adding and subtracting complex|argand/i, not: /reciprocal and division/i,
    make({ title }) {
      const t = /powers of i/i.test(title) ? 'pow' : /modulus/i.test(title) ? 'mod' : /multiplying/i.test(title) ? 'mul' : /adding/i.test(title) ? 'add' : pick(['add', 'mul', 'pow', 'mod']);
      const fc = ([a, b]) => cx(a, b);
      if (t === 'pow') { const n = R(5, 103), r = n % 4, v = [[1, 0], [0, 1], [-1, 0], [0, -1]][r];
        const bb = build(v, [[1, 0], [0, 1], [-1, 0], [0, -1]], fc);
        return Q(`Find the value of i${sup(n)}.`, bb, `Powers of i repeat every 4: i, −1, −i, 1.`, [`${n} = 4 × ${Math.floor(n / 4)} + ${r}, so the remainder is ${r}`, `So i${sup(n)} = i${sup(r)} = ${fc(v)}`], { t, n }); }
      if (t === 'mod') { const [p, q] = pick([[3, 4], [5, 12], [8, 15], [6, 8], [7, 24], [9, 12]]).map(x => x * pick([-1, 1])); const m = Math.round(Math.hypot(p, q));
        const bb = build(m, [Math.abs(p) + Math.abs(q), p * p + q * q, m + 1, Math.abs(p - q)], ind, { ok: x => x > 0 && x !== m });
        return Q(`Find the modulus of z = ${cx(p, q)}.`, bb, `|a + bi| = √(a² + b²).`, [`${pn(p)}² + ${pn(q)}² = ${p * p} + ${q * q} = ${p * p + q * q}`, `${m} × ${m} = ${m * m}, so |z| = ${m}`], { t, p, q }); }
      const a = R(-9, 9), b = R(-9, 9) || 2, c = R(-9, 9), d = R(-9, 9) || 3;
      if (t === 'add') { const sub = Math.random() < .5, v = sub ? [a - c, b - d] : [a + c, b + d];
        const bb = build(v, [sub ? [a + c, b + d] : [a - c, b - d], [v[0], -v[1]], [v[1], v[0]], [v[0] + v[1], 0]], fc, { ok: x => !(x[0] === v[0] && x[1] === v[1]) });
        return Q(`Simplify (${cx(a, b)}) ${sub ? '−' : '+'} (${cx(c, d)}).`, bb, `${sub ? 'Subtract' : 'Add'} the real parts and the imaginary parts separately.`, [`Real: ${pn(a)} ${sub ? '−' : '+'} ${pn(c)} = ${ind(v[0])}`, `Imaginary: ${pn(b)} ${sub ? '−' : '+'} ${pn(d)} = ${ind(v[1])}`], { t, a, b, c, d, sub }); }
      const re_ = a * c - b * d, im = a * d + b * c;
      const bb = build([re_, im], [[a * c + b * d, im], [a * c, b * d], [re_, a * d - b * c], [-re_, im]], fc, { ok: x => !(x[0] === re_ && x[1] === im) });
      return Q(`Multiply: (${cx(a, b)})(${cx(c, d)})`, bb, `Expand like brackets and use i² = −1.`, [`Real part: ${pn(a)} × ${pn(c)} − ${pn(b)} × ${pn(d)} = ${ind(re_)}`, `Imaginary part: ${pn(a)} × ${pn(d)} + ${pn(b)} × ${pn(c)} = ${ind(im)}`, `This uses i × i = −1, which turns the b × d part into a real number`], { t: 'mul', a, b, c, d });
    } });

  /* ---- 60. Determinants and matrices (Grade 12) ---- */
  def({ id: 'matrix', name: 'Matrices and determinants', subj: ['maths'], g: [12, 12], re: /evaluating determinants|matrix multiplication|addition and scalar multiplication|minors and cofactors/i,
    make({ title }) {
      const t = /multiplication/i.test(title) ? 'mul' : /addition/i.test(title) ? 'lin' : /minors/i.test(title) ? 'cof' : pick(['d2', 'd3']);
      const M = (r, c) => Array.from({ length: r }, () => Array.from({ length: c }, () => R(-5, 9)));
      const show = m => '[ ' + m.map(r => r.map(ind).join('  ')).join(' ; ') + ' ]';
      if (t === 'd2') { const [[a, b], [c, d]] = M(2, 2), v = a * d - b * c;
        const bb = build(v, [a * d + b * c, a * b - c * d, -v, a * c - b * d], ind, { ok: x => x !== v });
        return Q(`Find the determinant of ${show([[a, b], [c, d]])}.`, bb, `For [a b ; c d], the determinant is ad − bc.`, [`ad − bc = ${pn(a)} × ${pn(d)} − ${pn(b)} × ${pn(c)} = ${ind(a * d)} − ${pn(b * c)} = ${ind(v)}`], { t, m: [[a, b], [c, d]] }); }
      if (t === 'd3' || t === 'cof') { const m = M(3, 3), [[a, b, c], [d, e, f], [g, h, k]] = m;
        const c1 = e * k - f * h, c2 = d * k - f * g, c3 = d * h - e * g, v = a * c1 - b * c2 + c * c3;
        if (t === 'cof') { const A12 = -(d * k - f * g); const bb = build(A12, [-A12, d * k + f * g, e * k - f * h, A12 + 1], ind, { ok: x => x !== A12 });
          return Q(`For A = ${show(m)}, find the cofactor A₁₂ (row 1, column 2).`, bb, `Cofactor Aᵢⱼ = (−1)^(i+j) × minor Mᵢⱼ.`, [`Delete row 1 and column 2: minor M₁₂ = ${pn(d)} × ${pn(k)} − ${pn(f)} × ${pn(g)} = ${ind(d * k - f * g)}`, `Sign for (1, 2) is −, so A₁₂ = ${ind(A12)}`], { t, m }); }
        const bb = build(v, [a * c1 + b * c2 + c * c3, -v, a * c1 - b * c2 - c * c3, v + a], ind, { ok: x => x !== v });
        return Q(`Find the determinant of ${show(m)}.`, bb, `Expand along the first row with signs + − +.`, [`${pn(a)} × (${pn(e)} × ${pn(k)} − ${pn(f)} × ${pn(h)}) = ${pn(a)} × ${pn(c1)} = ${ind(a * c1)}`, `${pn(b)} × (${pn(d)} × ${pn(k)} − ${pn(f)} × ${pn(g)}) = ${pn(b)} × ${pn(c2)} = ${ind(b * c2)}`, `${pn(c)} × (${pn(d)} × ${pn(h)} − ${pn(e)} × ${pn(g)}) = ${pn(c)} × ${pn(c3)} = ${ind(c * c3)}`, `${ind(a * c1)} − ${pn(b * c2)} + ${pn(c * c3)} = ${ind(v)}`], { t, m }); }
      const A = M(2, 2), B = M(2, 2), i = R(0, 1), j = R(0, 1);
      if (t === 'lin') { const p = R(2, 3), q = R(2, 3) * pick([1, -1]), v = p * A[i][j] + q * B[i][j];
        const bb = build(v, [A[i][j] + B[i][j], p * A[i][j] - q * B[i][j], p * A[j][i] + q * B[j][i] === v ? v + 1 : p * A[j][i] + q * B[j][i], v + p], ind, { ok: x => x !== v });
        return Q(`A = ${show(A)}, B = ${show(B)}. Find the entry in row ${i + 1}, column ${j + 1} of ${p}A ${q < 0 ? '−' : '+'} ${Math.abs(q)}B.`, bb, `Scalar multiplication multiplies every entry; addition adds matching entries.`, [`Entry (${i + 1}, ${j + 1}): A has ${ind(A[i][j])}, B has ${ind(B[i][j])}`, `${p} × ${pn(A[i][j])} + ${pn(q)} × ${pn(B[i][j])} = ${ind(v)}`], { t, A, B, i, j, p, q }); }
      const v = A[i][0] * B[0][j] + A[i][1] * B[1][j];
      const bb = build(v, [A[i][0] * B[j][0] + A[i][1] * B[j][1], A[i][j] * B[i][j], A[0][i] * B[0][j] + A[1][i] * B[1][j], v + 1], ind, { ok: x => x !== v });
      return Q(`A = ${show(A)}, B = ${show(B)}. Find the entry in row ${i + 1}, column ${j + 1} of AB.`, bb, `Entry (i, j) of AB = row i of A times column j of B, multiplied pair by pair and added.`,
        [`Row ${i + 1} of A: ${A[i].map(ind).join(', ')}; column ${j + 1} of B: ${ind(B[0][j])}, ${ind(B[1][j])}`, `${pn(A[i][0])} × ${pn(B[0][j])} + ${pn(A[i][1])} × ${pn(B[1][j])} = ${ind(v)}`], { t, A, B, i, j });
    } });

  /* ---- 61. Derivatives and definite integrals of polynomials (Grades 11–12) ---- */
  def({ id: 'calculus', name: 'Derivatives and integrals of polynomials', subj: ['maths'], g: [11, 12], re: /rules of differentiation and polynomials|second order derivatives|definite integrals and the fundamental theorem|anti-derivatives and standard integrals/i,
    make({ title }) {
      const t = /integral/i.test(title) ? 'int' : /second/i.test(title) ? 'd2' : 'd1';
      if (t === 'int') { const a = R(-3, 4) || 1, b = R(-6, 6), c = R(-6, 6), p = R(-2, 1), q = p + R(1, 3);
        const Fx = x => new Fr(a * x ** 3, 3).add(new Fr(b * x * x, 2)).add(c * x), v = Fx(q).sub(Fx(p));
        const wrongF = x => F(a * x ** 3 + b * x * x + c * x);
        const bb = build(v, [wrongF(q).sub(wrongF(p)), v.mul(-1), Fx(q), new Fr(2 * a * q + b).sub(2 * a * p + b)], fs, { ok: x => !x.eq(v) });
        return Q(`Evaluate the integral of (${poly([a, b, c])}) dx from x = ${ind(p)} to x = ${ind(q)}.`, bb, `Find an antiderivative F(x), then work out F(upper) − F(lower).`,
          [`F(x) = ${polyF([new Fr(a, 3), new Fr(b, 2), F(c), F(0)])}`, `F(${ind(q)}) = ${fs(Fx(q))}, F(${ind(p)}) = ${fs(Fx(p))}`, `${pn(Fx(q))} − ${pn(Fx(p))} = ${fs(v)}`], { t, a, b, c, p, q }); }
      const a = R(-4, 5) || 2, b = R(-6, 6), c = R(-9, 9), d = R(-9, 9), k = R(-3, 4);
      if (t === 'd2') { const v = 6 * a * k + 2 * b; const bb = build(v, [3 * a * k * k + 2 * b * k + c, 6 * a + 2 * b, 3 * a * k + b, v + 2], ind, { ok: x => x !== v });
        return Q(`If f(x) = ${poly([a, b, c, d])}, find f″(${ind(k)}).`, bb, `Differentiate twice: the power rule d/dx(xⁿ) = n xⁿ⁻¹.`, [`f′(x) = ${poly([3 * a, 2 * b, c])}`, `f″(x) = ${poly([6 * a, 2 * b])}`, `f″(${ind(k)}) = ${pn(6 * a)} × ${pn(k)} + ${pn(2 * b)} = ${ind(v)}`], { t, a, b, c, d, k }); }
      const v = 3 * a * k * k + 2 * b * k + c;
      const bb = build(v, [a * k ** 3 + b * k * k + c * k + d, 3 * a * k + 2 * b + c, a * k * k + b * k + c, 6 * a * k + 2 * b], ind, { ok: x => x !== v });
      return Q(`If f(x) = ${poly([a, b, c, d])}, find f′(${ind(k)}).`, bb, `Power rule: d/dx(xⁿ) = n xⁿ⁻¹; the derivative of a constant is 0.`, [`f′(x) = ${poly([3 * a, 2 * b, c])}`, `f′(${ind(k)}) = ${pn(3 * a)} × ${pn(k)}² + ${pn(2 * b)} × ${pn(k)} + ${pn(c)} = ${ind(v)}`], { t, a, b, c, d, k });
    } });

  /* ---- 62. Degrees and radians (Grade 11) ---- */
  def({ id: 'radians', name: 'Degrees and radians', subj: ['maths'], g: [11, 11], re: /degrees and radians|degrees and radians; arc/i,
    make() {
      const dg = pick([15, 30, 36, 40, 45, 60, 72, 75, 90, 105, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330, 360, 18, 20]), f = new Fr(dg, 180);
      const fp = x => { x = F(x); return (x.p === 1 ? '' : x.p) + 'π' + (x.q === 1 ? '' : '/' + x.q); };
      if (Math.random() < .5) { const bb = build(f, [new Fr(dg, 360), new Fr(180, dg), new Fr(dg, 90), f.mul(2)], fp, { ok: x => x.p > 0 && !x.eq(f) });
        return Q(`Convert ${dg}° to radians.`, bb, `180° = π radians, so multiply degrees by π/180.`, [`${dg}/180 = ${fs(f)}`, `So ${dg}° = ${fp(f)} radians`], { t: 'toRad', dg }); }
      const bb = build(dg, [f.p * 180 / (f.q * 2), dg * 2, Math.round(f.v * 57), 180 - dg].filter(x => x !== dg && Number.isInteger(x)), v => `${v}°`, { ok: v => v > 0 && v !== dg });
      return Q(`Convert ${fp(f)} radians to degrees.`, bb, `π radians = 180°, so replace π with 180°.`, [`${fp(f)} = ${fs(f)} × 180°`, `${fs(f)} × 180 = ${dg}`], { t: 'toDeg', p: f.p, q: f.q });
    } });

  /* ---- 63. Binomial theorem coefficients (Grade 11) ---- */
  def({ id: 'binomial', name: 'Binomial theorem', subj: ['maths'], g: [11, 11], re: /binomial theorem|pascal|full expansions/i, not: /surd|divisibility/i,
    make() {
      const n = R(4, 9), a = R(1, 4) * pick([1, -1]), k = R(1, n - 1), coeff = nCr(n, k) * a ** (n - k);
      const bb = build(coeff, [nCr(n, k), nCr(n, k) * a ** k, nCr(n, k - 1) * a ** (n - k + 1), -coeff], ind, { ok: x => x !== coeff });
      return Q(`Find the coefficient of x${sup(k)} in the expansion of (x ${a < 0 ? '−' : '+'} ${Math.abs(a)})${sup(n)}.`, bb, `The general term of (x + a)ⁿ is C(n, r) xⁿ⁻ʳ aʳ.`,
        [`x${sup(k)} needs n − r = ${k}, so r = ${n} − ${k} = ${n - k}`, `C(${n}, ${n - k}) = ${nCr(n, n - k)}`, `${nCr(n, k)} × ${pn(a)}${sup(n - k)} = ${nCr(n, k)} × ${pn(a ** (n - k))} = ${ind(coeff)}`], { n, a, k });
    } });

  /* ---- 64. Slope of a line (Grades 9–11) ---- */
  def({ id: 'slope', name: 'Slope of a line', subj: ['maths'], g: [9, 11], re: /slope/i, not: /curves|intercept and intercept|families|how steep and which way|form y/i,
    make() {
      const x1 = R(-8, 8), y1 = R(-8, 8); let x2 = R(-8, 8); if (x2 === x1) x2 = x1 + R(1, 5); const y2 = R(-8, 8), m = new Fr(y2 - y1, x2 - x1);
      const bb = build(m, [new Fr(x2 - x1, (y2 - y1) || 7), m.mul(-1), new Fr(y2 + y1, (x2 + x1) || 9), m.add(1)], fs, { ok: v => !v.eq(m) });
      return Q(`Find the slope of the line through (${ind(x1)}, ${ind(y1)}) and (${ind(x2)}, ${ind(y2)}).`, bb, `Slope = rise ÷ run = (y₂ − y₁)/(x₂ − x₁).`, [`Rise: ${pn(y2)} − ${pn(y1)} = ${ind(y2 - y1)}`, `Run: ${pn(x2)} − ${pn(x1)} = ${ind(x2 - x1)}`, `Slope = ${ind(y2 - y1)} ÷ ${pn(x2 - x1)} = ${fs(m)}`], { x1, y1, x2, y2 });
    } });

  /* ================= Physics and chemistry ================= */
  /* ---- 65. Kinematics: equations of motion (science 9, physics 11) ---- */
  def({ id: 'kinematics', name: 'Equations of motion', subj: ['science', 'physics'], g: [9, 11], re: /equations and graphs of motion|kinematic|free fall|stopping distance|speed, velocity and acceleration|acceleration: meaning/i, not: /rotation|flywheel/i,
    make() {
      const t = pick(['v', 'a', 's', 's2', 'fall']);
      if (t === 'fall') { const tt = R(1, 6), h = 5 * tt * tt, v = 10 * tt; const ask = Math.random() < .5;
        const ans = ask ? h : v, bb = build(ans, ask ? [10 * tt * tt, 10 * tt, 5 * tt] : [5 * tt * tt, 5 * tt, 20 * tt], x => `${ind(x)} ${ask ? 'm' : 'm/s'}`, { ok: x => x > 0 && x !== ans });
        return Q(`A stone is dropped from rest from a tall cliff. ${ask ? 'How far does it fall' : 'How fast is it moving'} after ${tt} s? (Take g = 10 m/s² and ignore air resistance.)`, bb, `Dropped from rest: u = 0, a = g. Use ${ask ? 's = ut + ½at²' : 'v = u + at'}.`,
          ask ? [`s = ½ × g × t²`, `1/2 × 10 × ${tt}² = ${h}`] : [`v = u + gt`, `0 + 10 × ${tt} = ${v}`], { t, tt, ask }); }
      const u = R(0, 20), a = R(1, 6), tt = R(2, 10), v = u + a * tt, s = u * tt + a * tt * tt / 2;
      if (t === 'v') { const bb = build(v, [u + a, a * tt, u * tt + a, v + a], x => `${ind(x)} m/s`, { ok: x => x > 0 && x !== v });
        return Q(`A car starts at ${u} m/s and speeds up at ${a} m/s² for ${tt} s. What is its final velocity?`, bb, `First equation of motion: v = u + at.`, [`v = u + at`, `${u} + ${a} × ${tt} = ${v}`], { t, u, a, tt }); }
      if (t === 'a') { const bb = build(a, [v / tt === a ? (v + u) / tt : v / tt, v - u, (v - u) * tt, a + 1], x => `${nm(x)} m/s²`, { ok: x => F(x).p > 0 && dec(x, 2) !== null && !F(x).eq(F(a)) });
        return Q(`A scooter speeds up from ${u} m/s to ${v} m/s in ${tt} s. What is its acceleration?`, bb, `Acceleration = change in velocity ÷ time.`, [`a = (v − u) ÷ t`, `(${v} − ${u}) ÷ ${tt} = ${a}`], { t, u, v, tt }); }
      if (t === 's') { if (!Number.isInteger(s)) throw new Error('retry');
        const bb = build(s, [u * tt + a * tt * tt, u * tt, v * tt, s + u], x => `${ind(x)} m`, { ok: x => x > 0 && x !== s });
        return Q(`A cyclist moving at ${u} m/s accelerates at ${a} m/s² for ${tt} s. How far does the cyclist travel in this time?`, bb, `Second equation of motion: s = ut + ½at².`, [`s = ut + ½at²`, `${u} × ${tt} + 1/2 × ${a} × ${tt}² = ${u * tt} + ${a * tt * tt / 2} = ${s}`], { t, u, a, tt }); }
      if ((v * v - u * u) % (2 * a)) throw new Error('retry');
      const bb = build(s, [(v * v - u * u) / a, (v - u) * (v - u) / (2 * a), v * v / (2 * a) === s ? s + v : v * v / (2 * a), s + a], x => `${nm(x)} m`, { ok: x => F(x).p > 0 && dec(x, 2) !== null && !F(x).eq(F(s)) });
      return Q(`A train's speed rises from ${u} m/s to ${v} m/s with a steady acceleration of ${a} m/s². What distance does it cover meanwhile?`, bb, `Third equation of motion: v² = u² + 2as, so s = (v² − u²) ÷ 2a.`, [`v² − u² = ${v}² − ${u}² = ${v * v} − ${u * u} = ${v * v - u * u}`, `s = ${v * v - u * u} ÷ (2 × ${a}) = ${nm(s)}`], { t, u, v, a });
    } });

  /* ---- 66. Ohm's law (science 10, physics 12) ---- */
  def({ id: 'ohm', name: "Ohm's law", subj: ['science', 'physics'], g: [10, 12], re: /ohm's law/i,
    make() {
      const Rv = pick([2, 4, 5, 6, 8, 10, 12, 15, 20, 24, 25, 30, 40, 50, 100]), I = F(pick(['0.1', '0.2', '0.25', '0.5', '1', '1.5', '2', '3', '4'])), V = I.mul(Rv), t = pick(['V', 'I', 'R']);
      if (dec(V, 2) === null) throw new Error('retry');
      if (t === 'V') { const bb = build(V, [F(Rv).div(I), I.div(Rv), V.mul(2), V.add(Rv)], x => `${dec(x, 3) ?? 'x'} V`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(V) });
        return Q(`A current of ${dec(I)} A flows through a ${Rv} Ω resistor. What is the potential difference across it?`, bb, `Ohm's law: V = I × R.`, [`V = I × R`, `${dec(I)} × ${Rv} = ${dec(V)}`], { t, I: dec(I), R: Rv }); }
      if (t === 'I') { const bb = build(I, [V.mul(Rv), F(Rv).div(V), I.mul(10), I.add(1)], x => `${dec(x, 3) ?? 'x'} A`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(I) });
        return Q(`A ${dec(V)} V battery is connected across a ${Rv} Ω resistor. What current flows?`, bb, `From Ohm's law, I = V ÷ R.`, [`I = V ÷ R`, `${dec(V)} ÷ ${Rv} = ${dec(I)}`], { t, V: dec(V), R: Rv }); }
      const bb = build(F(Rv), [V.mul(I), I.div(V), F(Rv).mul(2), F(Rv + 5)], x => `${dec(x, 3) ?? 'x'} Ω`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(F(Rv)) });
      return Q(`A bulb draws ${dec(I)} A from a ${dec(V)} V supply. What is its resistance?`, bb, `From Ohm's law, R = V ÷ I.`, [`R = V ÷ I`, `${dec(V)} ÷ ${dec(I)} = ${Rv}`], { t, V: dec(V), I: dec(I) });
    } });

  /* ---- 67. Resistors (and capacitors) in series and parallel (science 10, physics 12) ---- */
  def({ id: 'resistors', name: 'Series and parallel combinations', subj: ['science', 'physics'], g: [10, 12], re: /resistors in series|series and parallel|combining capacitors/i, not: /cells/i,
    make({ title }) {
      const cap = /capacitor/i.test(title), u = cap ? 'μF' : 'Ω', sets = [[2, 2], [3, 6], [4, 4], [4, 12], [6, 12], [10, 15], [20, 30], [6, 3, 2], [12, 6, 4], [10, 10, 5], [12, 4], [8, 8], [5, 20], [30, 60]];
      const vals = shuffle(pick(sets)), ser = Math.random() < .5, sum = vals.reduce((s, x) => s + x, 0), rec = vals.reduce((s, x) => s.add(new Fr(1, x)), F(0)), par = F(1).div(rec);
      const isSum = cap ? !ser : ser, ans = isSum ? F(sum) : par, word = ser ? 'series' : 'parallel';
      const bb = build(ans, [isSum ? par : F(sum), rec, F(sum).div(vals.length), ans.mul(2)], x => `${nm(x)} ${u}`, { ok: x => F(x).p > 0 && dec(x, 3) !== null && !F(x).eq(ans) });
      const steps = isSum ? [`In ${word}, ${cap ? 'capacitances' : 'resistances'} add`, `${vals.join(' + ')} = ${sum}`] : [`In ${word}, the reciprocals add: ${vals.map(x => `1/${x}`).join(' + ')} = ${fs(rec)}`, `Take the reciprocal: 1 ÷ (${fs(rec)}) = ${nm(par)}`];
      return Q(`Find the equivalent ${cap ? 'capacitance' : 'resistance'} of ${vals.map(x => x + ' ' + u).join(', ').replace(/, ([^,]*)$/, ' and $1')} connected in ${word}.`, bb,
        cap ? `Capacitors: in parallel C = C₁ + C₂ + ...; in series 1/C = 1/C₁ + 1/C₂ + ...` : `Resistors: in series R = R₁ + R₂ + ...; in parallel 1/R = 1/R₁ + 1/R₂ + ...`, steps, { cap, vals, ser });
    } });

  /* ---- 68. Electric power and energy (science 10, physics 12) ---- */
  def({ id: 'elec_power', name: 'Electric power and energy', subj: ['science', 'physics'], g: [10, 12], re: /electric power|electrical energy and power|heating effect of current/i,
    make() {
      const t = pick(['P', 'I', 'R', 'kwh']);
      if (t === 'kwh') { const P = pick([100, 200, 500, 750, 1000, 1500, 2000]), h = R(1, 6), d = pick([10, 15, 30]), rate = R(4, 9), kwh = new Fr(P * h * d, 1000), cost = kwh.mul(rate);
        if (dec(cost, 2) === null) throw new Error('retry');
        const bb = build(cost, [F(P * h * d * rate), kwh, cost.mul(10), new Fr(P * h * rate, 1000)], x => '₹' + (dec(x, 2) ?? 'x'), { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(cost) });
        return Q(`A ${P} W heater runs ${h} hours a day for ${d} days. Electricity costs ₹${rate} per unit (1 unit = 1 kWh). What is the cost?`, bb, `Energy in kWh = power in kW × hours. 1 kW = 1000 W.`, [`Energy: ${P} × ${h} × ${d} ÷ 1000 = ${nm(kwh)} kWh`, `Cost: ${nm(kwh)} × ${rate} = ${dec(cost, 2)}`], { t, P, h, d, rate }); }
      const V = pick([6, 12, 24, 110, 220, 240]), I = F(pick(['0.5', '1', '2', '2.5', '4', '5', '0.25'])), P = I.mul(V);
      if (t === 'P') { const bb = build(P, [F(V).div(I), I.div(V), P.mul(2), F(V).add(I)], x => `${nm(x)} W`, { ok: x => F(x).p > 0 && dec(x, 3) !== null && !F(x).eq(P) });
        return Q(`An appliance on ${V} V draws ${dec(I)} A. What is its power?`, bb, `Electric power P = V × I.`, [`P = V × I`, `${V} × ${dec(I)} = ${nm(P)}`], { t, V, I: dec(I) }); }
      if (t === 'I') { const bb = build(I, [P.mul(V), F(V).div(P), I.mul(2), I.add(1)], x => `${nm(x)} A`, { ok: x => F(x).p > 0 && dec(x, 3) !== null && !F(x).eq(I) });
        return Q(`A ${nm(P)} W lamp works on ${V} V. What current does it draw?`, bb, `From P = V × I, I = P ÷ V.`, [`I = P ÷ V`, `${nm(P)} ÷ ${V} = ${nm(I)}`], { t, P: nm(P), V }); }
      const Pw = pick([40, 60, 100, 200, 500, 1000]), Vv = pick([100, 200, 220, 240]), Rr = new Fr(Vv * Vv, Pw); if (dec(Rr, 2) === null) throw new Error('retry');
      const bb = build(Rr, [new Fr(Pw, Vv), new Fr(Vv, Pw), new Fr(Pw * Pw, Vv), Rr.mul(2)], x => `${dec(x, 2) ?? 'x'} Ω`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(Rr) });
      return Q(`A bulb is rated ${Pw} W, ${Vv} V. What is its resistance when glowing normally?`, bb, `P = V²/R, so R = V² ÷ P.`, [`V² = ${Vv} × ${Vv} = ${ind(Vv * Vv)}`, `R = ${ind(Vv * Vv)} ÷ ${Pw} = ${dec(Rr, 2)}`], { t, P: Pw, V: Vv });
    } });

  /* ---- 69. Work and power (science 9, physics 11) ---- */
  def({ id: 'work_power', name: 'Work and power', subj: ['science', 'physics'], g: [9, 11], re: /work and power|work done by a constant force|^power$/i, not: /rotation/i,
    make({ g }) {
      const t = pick(['W', 'P', 'W', 'P2']);
      if (t === 'W') { const F_ = R(2, 50) * 5, s = R(2, 30), ang = g >= 11 ? pick([0, 60, 90, 180]) : 0, cs = { 0: 1, 60: new Fr(1, 2), 90: 0, 180: -1 }[ang], Wv = F(F_ * s).mul(cs);
        const bb = build(Wv, [F(F_ * s), F(F_ + s), new Fr(F_, s), Wv.mul(-1).eq(Wv) ? F(F_ * s * 2) : Wv.mul(-1)], x => `${nm(x)} J`, { ok: x => dec(x, 2) !== null && !F(x).eq(Wv) });
        return Q(`A force of ${F_} N moves a box ${s} m${ang ? `, and the force acts at ${ang}° to the direction of motion` : ' in the direction of the force'}. How much work is done?`, bb, `Work = force × displacement${ang ? ' × cos θ' : ''}.`,
          [ang ? `W = F × s × cos θ, and cos ${ang}° = ${fs(F(cs))}` : `W = F × s`, `${F_} × ${s}${ang ? ` × ${pn(F(cs))}` : ''} = ${nm(Wv)}`], { t, F: F_, s, ang }); }
      if (t === 'P') { const Pw = R(2, 60) * 10, tt = R(2, 20), Wv = Pw * tt;
        const bb = build(Pw, [Wv * tt, tt, Wv / 10, Pw + tt], x => `${ind(x)} W`, { ok: x => Number.isInteger(x) && x > 0 && x !== Pw });
        return Q(`A motor does ${ind(Wv)} J of work in ${tt} s. What is its power?`, bb, `Power = work done ÷ time taken. 1 W = 1 J/s.`, [`P = W ÷ t`, `${ind(Wv)} ÷ ${tt} = ${Pw}`], { t, W: Wv, tt }); }
      const m = R(2, 60), h = R(2, 20), tt = R(2, 10), Wv = m * 10 * h, Pw = new Fr(Wv, tt); if (dec(Pw, 2) === null) throw new Error('retry');
      const bb = build(Pw, [F(Wv), new Fr(m * h, tt), Pw.mul(10), new Fr(Wv * tt, 1)], x => `${dec(x, 2) ?? 'x'} W`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(Pw) });
      return Q(`A girl of mass ${m} kg climbs stairs ${h} m high in ${tt} s. What power does she use? (Take g = 10 m/s².)`, bb, `Work against gravity = mgh; power = work ÷ time.`, [`Work = m × g × h = ${m} × 10 × ${h} = ${ind(Wv)}`, `Power = ${ind(Wv)} ÷ ${tt} = ${dec(Pw, 2)}`], { t, m, h, tt });
    } });

  /* ---- 70. Kinetic and potential energy (science 9, physics 11) ---- */
  def({ id: 'energy', name: 'Kinetic and potential energy', subj: ['science', 'physics'], g: [9, 11], re: /kinetic and potential energy|kinetic energy and the work|conservation of mechanical energy/i,
    make() {
      const t = pick(['ke', 'pe', 'v']);
      if (t === 'ke') { const m = R(1, 40), v = R(2, 20), K = new Fr(m * v * v, 2);
        const bb = build(K, [F(m * v * v), new Fr(m * v, 2), F(m * v), K.mul(2).add(m)], x => `${nm(x)} J`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(K) });
        return Q(`An object of mass ${m} kg moves at ${v} m/s. What is its kinetic energy?`, bb, `Kinetic energy = ½ m v².`, [`KE = 1/2 × m × v²`, `1/2 × ${m} × ${v}² = 1/2 × ${m} × ${v * v} = ${nm(K)}`], { t, m, v }); }
      if (t === 'pe') { const m = R(1, 50), h = R(2, 40), P = m * 10 * h;
        const bb = build(P, [m * h, m * 10 + h, P / 2, P * 10], x => `${ind(x)} J`, { ok: x => Number.isInteger(x) && x > 0 && x !== P });
        return Q(`A ${m} kg box is lifted to a shelf ${h} m high. What is its gain in potential energy? (Take g = 10 m/s².)`, bb, `Potential energy = m g h.`, [`PE = m × g × h`, `${m} × 10 × ${h} = ${ind(P)}`], { t, m, h }); }
      const v = pick([10, 20, 30, 40]), h = v * v / 20;
      const bb = build(v, [2 * 10 * h, 10 * h / v === v ? v / 2 : 10 * h / v, v / 2, v * 2], x => `${ind(x)} m/s`, { ok: x => Number.isInteger(x) && x > 0 && x !== v });
      return Q(`A ball is dropped from a height of ${h} m. Ignoring air resistance, how fast is it moving just before it hits the ground? (Take g = 10 m/s².)`, bb, `All the potential energy becomes kinetic energy: mgh = ½mv², so v = √(2gh).`, [`2 × g × h = 2 × 10 × ${h} = ${20 * h}`, `${v} × ${v} = ${v * v}, so v = ${v}`], { t, h });
    } });

  /* ---- 71. Force, momentum, impulse (science 9, physics 11) ---- */
  def({ id: 'force', name: 'Force and momentum', subj: ['science', 'physics'], g: [9, 11], re: /newton's laws of motion|newton's second law|inertia and momentum|first law in action, and momentum|second law in action|rockets, recoil/i,
    make() {
      const t = pick(['F', 'a', 'p', 'imp', 'recoil']);
      if (t === 'recoil') { const m = F(pick(['0.01', '0.02', '0.05', '0.1'])), v = R(10, 60) * 10, M = R(2, 10), V = m.mul(v).div(M); if (dec(V, 3) === null) throw new Error('retry');
        const bb = build(V, [m.mul(v), F(M).mul(v).mul(m).mul(M), V.mul(10), m.mul(v).div(M + 1)], x => `${dec(x, 3) ?? 'x'} m/s`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(V) });
        return Q(`A ${M} kg gun fires a ${dec(m)} kg bullet at ${v} m/s. What is the recoil speed of the gun?`, bb, `Momentum is conserved: before firing it is 0, so the gun's momentum equals the bullet's momentum.`, [`Bullet momentum: ${dec(m)} × ${v} = ${nm(m.mul(v))}`, `Gun speed: ${nm(m.mul(v))} ÷ ${M} = ${dec(V, 3)}`], { t, m: dec(m), v, M }); }
      const m = R(2, 60), a = R(1, 12);
      if (t === 'F') { const bb = build(m * a, [m + a, new Fr(m, a), m * a * 10, m * 10], x => `${nm(x)} N`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(F(m * a)) });
        return Q(`What force gives a ${m} kg object an acceleration of ${a} m/s²?`, bb, `Newton's second law: F = m × a.`, [`F = m × a`, `${m} × ${a} = ${m * a}`], { t, m, a }); }
      if (t === 'a') { const Fv = m * a; const bb = build(a, [Fv * m, m / a === a ? a + 1 : new Fr(m, a), Fv - m, a * 2], x => `${nm(x)} m/s²`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(F(a)) });
        return Q(`A force of ${Fv} N acts on a ${m} kg trolley. What is its acceleration?`, bb, `From F = ma, a = F ÷ m.`, [`a = F ÷ m`, `${Fv} ÷ ${m} = ${a}`], { t, F: Fv, m }); }
      if (t === 'p') { const v = R(2, 30), p = m * v; const bb = build(p, [m + v, new Fr(m * v * v, 2), new Fr(m, v), p * 2], x => `${nm(x)} kg m/s`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(F(p)) });
        return Q(`What is the momentum of a ${m} kg body moving at ${v} m/s?`, bb, `Momentum p = m × v.`, [`p = m × v`, `${m} × ${v} = ${p}`], { t, m, v }); }
      const u = R(0, 10), v = u + R(2, 20), tt = pick([1, 2, 4, 5, 10]), Fv = new Fr(m * (v - u), tt); if (dec(Fv, 2) === null) throw new Error('retry');
      const bb = build(Fv, [new Fr(m * v, tt), F(m * (v - u)), new Fr(m * (v + u), tt), Fv.mul(tt * 2)], x => `${dec(x, 2) ?? 'x'} N`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(Fv) });
      return Q(`A ${m} kg cart speeds up from ${u} m/s to ${v} m/s in ${tt} s. What steady force acted on it?`, bb, `Force = rate of change of momentum = m(v − u) ÷ t.`, [`Change in momentum: ${m} × (${v} − ${u}) = ${m * (v - u)}`, `F = ${m * (v - u)} ÷ ${tt} = ${dec(Fv, 2)}`], { t, m, u, v, tt });
    } });

  /* ---- 72. Density and pressure (science 8–10, physics 11, chemistry 11) ---- */
  def({ id: 'density', name: 'Density and pressure', subj: ['science', 'physics', 'chemistry'], g: [8, 11], re: /density|pressure and air pressure|pressure at depth|fluids, pressure/i, not: /nuclear|current density|vapour|osmotic|partial|charge/i,
    make({ title }) {
      const t = /density/i.test(title) && !/pressure/i.test(title) ? pick(['rho', 'mass']) : /depth/i.test(title) ? 'depth' : /density/i.test(title) ? pick(['rho', 'mass', 'P']) : pick(['P', 'P', 'rho']);
      if (t === 'rho' || t === 'mass') { const rho = F(pick(['0.8', '1', '1.2', '2.5', '2.7', '7.8', '8.9', '11.3', '13.6', '0.9', '19.3'])), V = R(2, 50), m = rho.mul(V);
        if (t === 'rho') { const bb = build(rho, [F(V).div(m), m.mul(V), rho.mul(10), rho.add(1)], x => `${dec(x, 3) ?? 'x'} g/cm³`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(rho) });
          return Q(`A metal block has mass ${nm(m)} g and volume ${V} cm³. What is its density?`, bb, `Density = mass ÷ volume.`, [`ρ = m ÷ V`, `${nm(m)} ÷ ${V} = ${nm(rho)}`], { t, m: nm(m), V }); }
        const bb = build(m, [rho.div(V), F(V).div(rho), m.mul(10), m.add(V)], x => `${dec(x, 3) ?? 'x'} g`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(m) });
        return Q(`A liquid has density ${nm(rho)} g/cm³. What is the mass of ${V} cm³ of it?`, bb, `Mass = density × volume.`, [`m = ρ × V`, `${nm(rho)} × ${V} = ${nm(m)}`], { t, rho: nm(rho), V }); }
      if (t === 'depth') { const h = R(1, 50), P = 1000 * 10 * h;
        const bb = build(P, [10 * h, 1000 * h, P * 10, P / 2], x => `${ind(x)} Pa`, { ok: x => Number.isInteger(x) && x > 0 && x !== P });
        return Q(`What is the pressure due to water at a depth of ${h} m? (Density of water = 1000 kg/m³, g = 10 m/s².)`, bb, `Pressure due to a liquid column = h × ρ × g.`, [`P = h × ρ × g`, `${h} × 1000 × 10 = ${ind(P)}`], { t, h }); }
      const A = F(pick(['0.5', '0.25', '2', '4', '0.1', '0.02', '1.5'])), P = R(2, 50) * 100, Fv = A.mul(P);
      const bb = build(P, [Fv.mul(A), A.div(Fv), F(P * 10), F(P + 100)], x => `${nm(x)} Pa`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(F(P)) });
      return Q(`A force of ${nm(Fv)} N acts on an area of ${nm(A)} m². What is the pressure?`, bb, `Pressure = force ÷ area. 1 Pa = 1 N/m².`, [`P = F ÷ A`, `${nm(Fv)} ÷ ${nm(A)} = ${ind(P)}`], { t, F: nm(Fv), A: nm(A) });
    } });

  /* ---- 73. Waves and sound: v = fλ, echoes (science 9, physics 11) ---- */
  def({ id: 'waves', name: 'Wave speed and echoes', subj: ['science', 'physics'], g: [9, 11], re: /sound waves, frequency|wave speed|frequency and amplitude|echo|waves on strings/i,
    make({ title }) {
      const t = /echo/i.test(title) ? 'echo' : pick(['v', 'lam', 'f', 'echo', 'T']);
      if (t === 'echo') { const v = pick([330, 340, 1500]), tt = F(pick(['1', '2', '3', '4', '0.5', '1.5', '2.5'])), d = tt.mul(v).div(2);
        const bb = build(d, [tt.mul(v), d.div(2), F(v).div(tt), d.add(v)], x => `${nm(x)} m`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(d) });
        return Q(`${v === 1500 ? 'A ship sends a SONAR pulse; the echo from the sea bed' : 'A boy shouts near a cliff; the echo'} comes back after ${nm(tt)} s. Speed of sound ${v === 1500 ? 'in water' : 'in air'} is ${v} m/s. How far away is the ${v === 1500 ? 'sea bed' : 'cliff'}?`, bb, `The sound goes there and back, so distance = speed × time ÷ 2.`, [`Total path: ${v} × ${nm(tt)} = ${nm(tt.mul(v))}`, `One way: ${nm(tt.mul(v))} ÷ 2 = ${nm(d)}`], { t, v, tt: nm(tt) }); }
      const f = pick([50, 100, 170, 200, 250, 340, 400, 500, 680, 1000]), lam = F(pick(['0.5', '1', '2', '0.25', '1.5', '0.68', '0.34', '3', '4'])), v = lam.mul(f);
      if (t === 'v') { const bb = build(v, [F(f).div(lam), lam.div(f), v.mul(10), F(f).add(lam)], x => `${nm(x)} m/s`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(v) });
        return Q(`A wave has frequency ${f} Hz and wavelength ${nm(lam)} m. What is its speed?`, bb, `Wave speed = frequency × wavelength.`, [`v = f × λ`, `${f} × ${nm(lam)} = ${nm(v)}`], { t, f, lam: nm(lam) }); }
      if (t === 'lam') { const bb = build(lam, [v.mul(f), F(f).div(v), lam.mul(10), lam.add(1)], x => `${dec(x, 4) ?? 'x'} m`, { ok: x => dec(x, 4) !== null && F(x).p > 0 && !F(x).eq(lam) });
        return Q(`Sound of frequency ${f} Hz travels at ${nm(v)} m/s. What is its wavelength?`, bb, `λ = v ÷ f.`, [`λ = v ÷ f`, `${nm(v)} ÷ ${f} = ${nm(lam)}`], { t, f, v: nm(v) }); }
      if (t === 'f') { const bb = build(F(f), [v.mul(lam), lam.div(v), F(f * 2), F(f).add(10)], x => `${nm(x)} Hz`, { ok: x => dec(x, 4) !== null && F(x).p > 0 && !F(x).eq(F(f)) });
        return Q(`A wave travels at ${nm(v)} m/s with wavelength ${nm(lam)} m. What is its frequency?`, bb, `f = v ÷ λ.`, [`f = v ÷ λ`, `${nm(v)} ÷ ${nm(lam)} = ${ind(f)}`], { t, v: nm(v), lam: nm(lam) }); }
      const T = new Fr(1, f); if (dec(T, 4) === null) throw new Error('retry');
      const bb = build(T, [F(f), new Fr(10, f), new Fr(1, f * 10), new Fr(2, f)], x => `${dec(x, 5) ?? 'x'} s`, { ok: x => dec(x, 5) !== null && !F(x).eq(T) });
      return Q(`A tuning fork vibrates at ${f} Hz. What is its time period?`, bb, `Time period T = 1 ÷ frequency.`, [`T = 1 ÷ f`, `1 ÷ ${f} = ${dec(T, 4)}`], { t, f });
    } });

  /* ---- 74. Mass and weight (science 8–9, physics 11) ---- */
  def({ id: 'weight', name: 'Mass and weight', subj: ['science', 'physics'], g: [8, 11], re: /mass and weight|gravity, mass and weight|gravitation, mass and weight/i,
    make() {
      const moon = Math.random() < .35;
      if (moon) { const W = 6 * R(5, 200), Wm = W / 6; const bb = build(Wm, [W * 6, W - 6, W, W / 2], x => `${ind(x)} N`, { ok: x => Number.isInteger(x) && x > 0 && x !== Wm });
        return Q(`An astronaut weighs ${ind(W)} N on Earth. What does the astronaut weigh on the Moon, where gravity is 1/6 of Earth's?`, bb, `Mass stays the same; weight depends on gravity. On the Moon, weight = Earth weight ÷ 6.`, [`Weight on Moon = weight on Earth × 1/6`, `${ind(W)} ÷ 6 = ${ind(Wm)}`], { moon, W }); }
      const m = R(2, 120), g = pick(['10', '9.8']), W = F(g).mul(m);
      const bb = build(W, [F(m), F(m).div(F(g)), W.mul(10), W.add(m)], x => `${dec(x, 3) ?? 'x'} N`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(W) });
      return Q(`What is the weight of a ${m} kg object on Earth? (Take g = ${g} m/s².)`, bb, `Weight is a force: W = m × g. Mass is in kg, weight is in newtons.`, [`W = m × g`, `${m} × ${g} = ${nm(W)}`], { moon, m, g });
    } });

  /* ---- 75. Temperature scales (science 6–8, physics/chemistry 11, maths 8) ---- */
  def({ id: 'temperature', name: 'Temperature conversion', subj: ['science', 'physics', 'chemistry', 'maths'], g: [6, 11], re: /celsius|temperature scales|thermometers and temperature|temperature and real-life conversions|^thermometers$/i,
    make({ g }) {
      const t = pick(['CK', 'KC', 'CF', 'FC']), exactK = g >= 9, add = exactK ? F('273.15') : F(273), rule = exactK ? 'K = °C + 273.15' : 'K = °C + 273 (the school rule, rounded)';
      if (t === 'CK' || t === 'KC') { const C = R(-50, 120), K = F(C).add(add);
        if (t === 'CK') { const bb = build(K, [F(C).sub(add), F(C).add(exactK ? 273 : 373), K.add(1), F(C)], x => `${nm(x)} K`, { ok: x => !F(x).eq(K) });
          return Q(`Convert ${ind(C)} °C to kelvin.`, bb, `Using ${rule}.`, [`Rule: ${rule}`, `${pn(C)} + ${nm(add)} = ${nm(K)}`], { t, C, exactK }); }
        const bb = build(F(C), [K.add(add), F(C + (exactK ? 1 : 100)), K, F(-C)], x => `${nm(x)} °C`, { ok: x => !F(x).eq(F(C)) });
        return Q(`Convert ${nm(K)} K to degrees Celsius.`, bb, `Using ${rule}, so °C = K − ${nm(add)}.`, [`Rule: °C = K − ${nm(add)}`, `${nm(K)} − ${nm(add)} = ${ind(C)}`], { t, K: nm(K), exactK }); }
      const C = 5 * R(-8, 24), Fh = C * 9 / 5 + 32;
      if (t === 'CF') { const bb = build(Fh, [C * 9 / 5, (C + 32) * 9 / 5, C * 5 / 9 + 32 | 0, Fh + 32], x => `${nm(x)} °F`, { ok: x => dec(x, 2) !== null && !F(x).eq(F(Fh)) });
        return Q(`Convert ${ind(C)} °C to degrees Fahrenheit.`, bb, `°F = °C × 9/5 + 32.`, [`${pn(C)} × 9/5 = ${ind(C * 9 / 5)}`, `${pn(C * 9 / 5)} + 32 = ${ind(Fh)}`], { t, C }); }
      const bb = build(C, [Fh - 32, (Fh - 32) * 9 / 5, Fh * 5 / 9 | 0, C + 32], x => `${nm(x)} °C`, { ok: x => dec(x, 2) !== null && !F(x).eq(F(C)) });
      return Q(`Convert ${ind(Fh)} °F to degrees Celsius.`, bb, `°C = (°F − 32) × 5/9.`, [`${pn(Fh)} − 32 = ${ind(Fh - 32)}`, `${pn(Fh - 32)} × 5/9 = ${ind(C)}`], { t, F: Fh });
    } });

  /* ---- 76. Lenses and mirrors (science 10, physics 12) ---- */
  def({ id: 'optics', name: 'Lens and mirror formula', subj: ['science', 'physics'], g: [10, 12], re: /lens formula|mirror formula|power of a lens|thin lens formula|mirror equation/i,
    make({ title }) {
      const mir = /mirror/i.test(title) && (!/lens/i.test(title) || Math.random() < .5);
      if (!mir && Math.random() < .4) { const f = pick([10, 20, 25, 40, 50, 100, -10, -20, -25, -40, -50]), Pw = new Fr(100, f);
        const bb = build(Pw, [new Fr(f, 100), Pw.mul(-1), F(f), new Fr(1, f)], x => `${dec(x, 3) ?? 'x'} D`, { ok: x => dec(x, 3) !== null && !F(x).eq(Pw) });
        return Q(`A ${f > 0 ? 'convex' : 'concave'} lens has focal length ${ind(f)} cm. What is its power?`, bb, `Power P = 1/f with f in metres, so P = 100 ÷ f(cm). Convex lenses have positive power, concave lenses negative.`, [`f = ${ind(f)} cm = ${nm(new Fr(f, 100))} m`, `P = 100 ÷ ${pn(f)} = ${nm(Pw)}`], { t: 'pow', f }); }
      let u, f, v, guard = 0;
      do { u = -5 * R(2, 20); f = mir ? -pick([5, 10, 12, 15, 20, 25, 30]) : pick([5, 10, 12, 15, 20, 25, 30]); v = mir ? F(1).div(new Fr(1, f).sub(new Fr(1, u))) : F(1).div(new Fr(1, f).add(new Fr(1, u))); }
      while ((Math.abs(u) === Math.abs(f) || !v.int || Math.abs(v.p) > 300) && guard++ < 200);
      if (!v.int) throw new Error('retry');
      const wrongV = mir ? F(1).div(new Fr(1, f).add(new Fr(1, u))) : (new Fr(1, f).sub(new Fr(1, u)).p ? F(1).div(new Fr(1, f).sub(new Fr(1, u))) : null);
      const bb = build(v, [v.mul(-1), wrongV, F(u + f), F(u).mul(-1)], x => `v = ${dec(x, 2) ?? 'x'} cm`, { ok: x => x && dec(x, 2) !== null && !F(x).eq(v) });
      const sumTxt = mir ? `1/v = 1/${pn(f)} − 1/${pn(u)}` : `1/v = 1/${f} + 1/${pn(u)}`;
      return Q(`An object is placed ${Math.abs(u)} cm in front of a ${mir ? 'concave mirror' : 'convex lens'} of focal length ${Math.abs(f)} cm. Find the image distance v (use the New Cartesian sign convention).`, bb,
        mir ? `Mirror formula: 1/v + 1/u = 1/f. For a concave mirror f is negative; the object distance u is negative.` : `Lens formula: 1/v − 1/u = 1/f. For a convex lens f is positive; the object distance u is negative.`,
        [`u = ${ind(u)} cm, f = ${ind(f)} cm`, `${sumTxt}`, `1/${pn(f)} ${mir ? '−' : '+'} 1/${pn(u)} = ${fs(F(1).div(v))}`, `v = ${ind(v.p)} cm`], { mir, u, f });
    } });

  /* ---- 77. Moles and molar mass (science 9, chemistry 11) ---- */
  const AM = { H: 1, C: 12, N: 14, O: 16, Na: 23, Mg: 24, Al: 27, S: 32, Cl: '35.5', K: 39, Ca: 40 };
  const CMP = [['H₂O', { H: 2, O: 1 }], ['CO₂', { C: 1, O: 2 }], ['NH₃', { N: 1, H: 3 }], ['CH₄', { C: 1, H: 4 }], ['NaCl', { Na: 1, Cl: 1 }], ['CaCO₃', { Ca: 1, C: 1, O: 3 }], ['H₂SO₄', { H: 2, S: 1, O: 4 }], ['HCl', { H: 1, Cl: 1 }], ['MgO', { Mg: 1, O: 1 }], ['C₆H₁₂O₆', { C: 6, H: 12, O: 6 }], ['NaOH', { Na: 1, O: 1, H: 1 }], ['HNO₃', { H: 1, N: 1, O: 3 }], ['KCl', { K: 1, Cl: 1 }], ['C₂H₅OH', { C: 2, H: 6, O: 1 }], ['Al₂O₃', { Al: 2, O: 3 }], ['MgCl₂', { Mg: 1, Cl: 2 }], ['CaO', { Ca: 1, O: 1 }], ['SO₂', { S: 1, O: 2 }], ['O₂', { O: 2 }], ['N₂', { N: 2 }], ['Na₂CO₃', { Na: 2, C: 1, O: 3 }], ['KOH', { K: 1, O: 1, H: 1 }], ['CaCl₂', { Ca: 1, Cl: 2 }]];
  const molar = c => Object.entries(c).reduce((s, [e, k]) => s.add(F(AM[e]).mul(k)), F(0));
  def({ id: 'moles', name: 'Moles and molar mass', subj: ['science', 'chemistry'], g: [9, 11], re: /\bmole\b|molar mass|molecular mass|formula mass|mole concept/i, not: /mole fraction|molar conductivity/i,
    make({ title }) {
      const t = /molecular mass|formula mass/i.test(title) && !/mole\b/i.test(title) ? 'M' : pick(['M', 'n', 'mass', 'N']);
      const [fm, comp] = pick(CMP), M = molar(comp), parts = Object.entries(comp).map(([e, k]) => k > 1 ? `${k} × ${nm(F(AM[e]))}` : nm(F(AM[e])));
      const amTxt = Object.keys(comp).map(e => `${e} = ${nm(F(AM[e]))}`).join(', ');
      if (t === 'M') { const wrong1 = Object.entries(comp).reduce((s, [e]) => s.add(F(AM[e])), F(0)), wrong2 = Object.entries(comp).reduce((s, [e, k]) => s.add(F(AM[e]).add(k)), F(0));
        const bb = build(M, [wrong1, wrong2, M.mul(2), M.add(16)], x => `${nm(x)} g/mol`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(M) });
        return Q(`Find the molar mass of ${fm}. (Atomic masses: ${amTxt}.)`, bb, `Add the atomic masses of all the atoms in one formula unit.`, [`Atoms in ${fm}: ${Object.entries(comp).map(([e, k]) => `${k} ${e}`).join(', ')}`, `${parts.join(' + ')} = ${nm(M)}`], { t, fm }); }
      const n = F(pick(['0.1', '0.2', '0.25', '0.5', '2', '3', '1.5', '5', '4'])), m = n.mul(M);
      if (dec(m, 2) === null) throw new Error('retry');
      if (t === 'n') { const bb = build(n, [m.mul(M), M.div(m), n.mul(10), n.add(1)], x => `${dec(x, 4) ?? 'x'} mol`, { ok: x => dec(x, 4) !== null && F(x).p > 0 && !F(x).eq(n) });
        return Q(`How many moles are there in ${nm(m)} g of ${fm}? (Atomic masses: ${amTxt}.)`, bb, `Number of moles = mass ÷ molar mass.`, [`Molar mass of ${fm}: ${parts.join(' + ')} = ${nm(M)}`, `n = ${nm(m)} ÷ ${nm(M)} = ${nm(n)}`], { t, fm, m: nm(m) }); }
      if (t === 'mass') { const bb = build(m, [M.div(n), n.add(M), m.mul(10), M], x => `${dec(x, 3) ?? 'x'} g`, { ok: x => dec(x, 3) !== null && F(x).p > 0 && !F(x).eq(m) });
        return Q(`What is the mass of ${nm(n)} mol of ${fm}? (Atomic masses: ${amTxt}.)`, bb, `Mass = number of moles × molar mass.`, [`Molar mass of ${fm}: ${parts.join(' + ')} = ${nm(M)}`, `m = ${nm(n)} × ${nm(M)} = ${nm(m)}`], { t, fm, n: nm(n) }); }
      const NA = F('6.022'), prod = n.mul(NA); let mant = prod, e = 23; while (mant.v >= 10) { mant = mant.div(10); e++; } while (mant.v < 1) { mant = mant.mul(10); e--; }
      const fmtS = ([mm, ee]) => `${dec(mm, 6)} × 10${sup(ee)}`;
      const bb = build([mant, e], [[mant, e + 1], [mant, e - 1], [NA, 23], [NA.div(n).v < 10 && NA.div(n).v >= 1 ? NA.div(n) : NA, NA.div(n).v < 10 && NA.div(n).v >= 1 ? 23 : 22]], fmtS, { ok: ([mm]) => dec(mm, 6) !== null });
      return Q(`How many molecules are there in ${nm(n)} mol of ${fm}? (Avogadro's number = 6.022 × 10²³ per mol.)`, bb, `Number of particles = moles × Avogadro's number.`, [`N = ${nm(n)} × 6.022 × 10²³`, `${nm(n)} × 6.022 × 10²³ = ${fmtS([mant, e])}`], { t, fm, n: nm(n) });
    } });

  /* ---- 78. Molarity and mass per cent (chemistry 11–12) ---- */
  const SOL = [['NaOH', 40], ['NaCl', '58.5'], ['glucose (C₆H₁₂O₆)', 180], ['KOH', 56], ['HCl', '36.5'], ['urea (CH₄N₂O)', 60]];
  def({ id: 'molarity', name: 'Molarity and mass per cent', subj: ['chemistry'], g: [11, 12], re: /molarity|concentration: mass percent|types of solutions and percentage/i,
    make({ title }) {
      if (/percent|percentage/i.test(title) && Math.random() < .5) { let a, b; do { a = R(2, 60); b = R(20, 400); } while ((a * 100) % (a + b)); const p = a * 100 / (a + b);
        const bb = build(p, [new Fr(a * 100, b), a, new Fr(b * 100, a + b), p + 5], x => `${dec(x, 2) ?? 'x'}%`, { ok: x => dec(x, 2) !== null && F(x).p > 0 && !F(x).eq(F(p)) });
        return Q(`${a} g of sugar is dissolved in ${b} g of water. What is the mass per cent of sugar in the solution?`, bb, `Mass % = mass of solute ÷ mass of solution × 100. The solution includes the water.`, [`Mass of solution: ${a} + ${b} = ${a + b} g`, `${a}/${a + b} × 100 = ${nm(p)}`], { t: 'pct', a, b }); }
      const [nmS, Mm] = pick(SOL), M = F(Mm), n = F(pick(['0.05', '0.1', '0.2', '0.25', '0.5', '1', '0.02'])), V = pick([100, 200, 250, 500, 1000]), mass = n.mul(M), Mol = n.mul(1000).div(V);
      if (dec(mass, 3) === null || dec(Mol, 4) === null) throw new Error('retry');
      const bb = build(Mol, [n.div(V), n, Mol.mul(10), mass.div(V)], x => `${dec(x, 5) ?? 'x'} M`, { ok: x => dec(x, 5) !== null && F(x).p > 0 && !F(x).eq(Mol) });
      return Q(`${nm(mass)} g of ${nmS} (molar mass ${nm(M)} g/mol) is dissolved to make ${V} mL of solution. What is the molarity?`, bb, `Molarity = moles of solute ÷ volume of solution in litres.`,
        [`Moles: ${nm(mass)} ÷ ${nm(M)} = ${nm(n)}`, `Volume: ${V} mL = ${nm(new Fr(V, 1000))} L`, `M = ${nm(n)} ÷ ${nm(new Fr(V, 1000))} = ${nm(Mol)}`], { t: 'M', mass: nm(mass), M: nm(M), V });
    } });

  /* =====================================================================================
     Matching and API
     ===================================================================================== */
  const parseId = id => { const m = /^g(\d+)-([a-z]+)-/.exec(id || ''); return m ? { g: +m[1], sid: m[2] } : {}; };
  function matching(topicId, title, grade, subject) {
    const p = parseId(topicId); grade = +(grade || p.g); subject = subject || p.sid; title = String(title || '');
    return GENS.filter(G => G.subj.includes(subject) && grade >= G.g[0] && grade <= G.g[1] && G.re.test(title) && !(G.not && G.not.test(title)));
  }
  function valid(x) {
    return x && typeof x.q === 'string' && Array.isArray(x.options) && x.options.length === 4 && new Set(x.options).size === 4 && x.options.every(o => typeof o === 'string' && o.length && !/undefined|NaN|null|Infinity/.test(o))
      && x.answer >= 0 && x.answer < 4 && Array.isArray(x.steps) && x.steps.length >= 2 && x.steps.length <= 6 && x.steps[x.steps.length - 1] === 'Answer: ' + x.options[x.answer]
      && !/undefined|NaN|Infinity/.test(x.q + x.explain + x.steps.join('|'));
  }
  function makeFrom(G, ctx) {
    for (let k = 0; k < 60; k++) { try { const x = G.make(ctx); if (valid(x)) { x.gen = G.id; return x; } } catch (e) { /* retry with new numbers */ } }
    return null;
  }
  function next(topicId, title, grade, subject, opts) {
    const p = parseId(topicId), gs = matching(topicId, title, grade, subject); if (!gs.length) return null;
    const ctx = { g: +(grade || p.g), title: String(title || ''), subj: subject || p.sid };
    const order = opts && opts.gen ? gs.filter(G => G.id === opts.gen) : shuffle(gs);
    for (const G of order) { const x = makeFrom(G, ctx); if (x) return x; }
    return null;
  }
  const has = (topicId, title, grade, subject) => matching(topicId, title, grade, subject).length > 0;

  /* =====================================================================================
     UI: one question at a time, endless, with look-back and a summary
     ===================================================================================== */
  const H = s => (typeof esc === 'function' ? esc(s) : String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])));
  const SPK = (t, o) => `<button class="spk"${o ? ' data-opts="1"' : ''} data-say="${H(t)}" aria-label="Read aloud">🔊</button>`;
  const S = k => { try { if (typeof sfx === 'function') sfx(k); } catch (e) {} };
  const XP = n => { try { if (typeof addXP === 'function') addXP(n); } catch (e) {} };
  function open(host, topic, opt = {}) {
    const p = parseId(topic.id), grade = (typeof ST !== 'undefined' && ST.profile && ST.profile.grade) || p.g, subj = p.sid || (typeof NAV !== 'undefined' && NAV.subject);
    if (!has(topic.id, topic.title, grade, subj)) { host.innerHTML = '<div class="card"><p class="sub">Endless practice is not available for this topic yet.</p></div>'; return false; }
    const st = { n: 0, right: 0, xp: 0, hist: [], cur: null };
    const stopTalk = () => { try { ReadAlong.stop(); } catch (e) {} };
    const head = (label, j) => `<div class="tst-top"><span class="tag">${label}</span>${j > 0 ? `<button class="tst-ic" id="gvPrevTop" aria-label="See the previous question">◀</button>` : ''}<button class="tst-ic" id="gvEnd" aria-label="End practice">End</button></div>`;
    const counter = () => `♾️ Question ${st.n} · ✔ ${st.right}`;
    const explainBox = (x, ok) => `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : `🤔 Not quite — it's <b>${H(x.options[x.answer])}</b>`}</div>
        ${x.visual && window.Visual ? `<div class="vis">${Visual.render(x.visual)}</div>` : `<div class="bigans popin">${H(x.options[x.answer])}</div>`}
        <div class="why">${H(x.explain)} ${SPK(x.explain)}</div>
        ${x.steps.map((s, j) => `<div class="exstep popin" style="animation-delay:${(.3 + j * .35).toFixed(2)}s">${j + 1}. ${H(s)}</div>`).join('')}</div>`;
    const wireTop = j => { const e = host.querySelector('#gvEnd'); if (e) e.onclick = summary; const pv = host.querySelector('#gvPrevTop'); if (pv) pv.onclick = () => review(j - 1); };
    function ask() {
      stopTalk();
      const x = next(topic.id, topic.title, grade, subj); if (!x) { summary(); return; }
      st.n++; st.cur = { x, k: null, order: shuffle([0, 1, 2, 3]) };
      st.hist.push(st.cur); if (st.hist.length > 40) st.hist.shift();
      draw();
    }
    function draw() {
      const c = st.cur, x = c.x, idx = st.hist.length - 1;
      host.innerHTML = `<div class="card gen-card">${head(counter(), idx)}<div class="progress"><i style="width:${Math.min(100, (st.n % 10 || 10) * 10)}%"></i></div>
        <h2 class="qtext">${H(x.q)} ${SPK(x.q, 1)}</h2><div id="qo">${c.order.map(k => `<button class="opt" data-k="${k}">${H(x.options[k])}</button>`).join('')}</div><div id="qx"></div></div>
        <button class="back" id="gvBack" style="background:rgba(255,255,255,.18)">← Back to lesson</button>`;
      wireTop(idx); host.querySelector('#gvBack').onclick = exit;
      host.querySelectorAll('#qo .opt').forEach(b => b.onclick = () => choose(+b.dataset.k, b));
      if (c.k !== null) showResult();
    }
    function choose(k, btn) {
      const c = st.cur; if (c.k !== null) return; c.k = k; c.ok = k === c.x.answer;
      if (c.ok) { st.right++; st.xp += 2; S('correct'); XP(2); } else { S('wrong'); }
      showResult(true);
    }
    function showResult(fresh) {
      const c = st.cur, x = c.x, idx = st.hist.length - 1;
      host.querySelectorAll('#qo .opt').forEach(o => { o.disabled = true; const kk = +o.dataset.k; if (kk === x.answer) o.classList.add('right'); else if (kk === c.k) o.classList.add('wrong'); });
      const tag = host.querySelector('.tst-top .tag'); if (tag) tag.textContent = counter();
      host.querySelector('#qx').innerHTML = explainBox(x, c.ok) + `<div class="xrow">${idx > 0 ? '<button class="btn ghost" id="gvPrev">◀ Previous</button>' : ''}<button class="btn mint" id="nx">Next ▶</button></div>`;
      const pv = host.querySelector('#gvPrev'); if (pv) pv.onclick = () => review(idx - 1);
      host.querySelector('#nx').onclick = ask;
      if (fresh) setTimeout(() => { const bx = host.querySelector('#qx'); if (bx && bx.scrollIntoView) bx.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 120);
    }
    function review(j) {
      if (j < 0) return; stopTalk();
      const h = st.hist[j], x = h.x, back = st.hist.length - 1, num = st.n - back + j;
      host.innerHTML = `<div class="card gen-card">${head(`Question ${num} · review`, j)}
        <h2 class="qtext">${H(x.q)} ${SPK(x.q, 1)}</h2><div>${h.order.map(k => `<button class="opt ${k === x.answer ? 'right' : k === h.k ? 'wrong' : ''}" disabled>${H(x.options[k])}</button>`).join('')}</div>
        ${h.k === null ? '<p class="sub">Not answered yet.</p>' : explainBox(x, h.ok)}
        <div class="tst-nav"><button class="btn ghost" id="gvPrev" ${j ? '' : 'disabled'}>◀ Previous</button><button class="btn" id="gvBackQ">Back to question ${st.n} ▶</button></div></div>`;
      wireTop(j);
      host.querySelector('#gvPrev').onclick = () => review(j - 1);
      host.querySelector('#gvBackQ').onclick = draw;
    }
    function summary() {
      stopTalk();
      const done = st.hist.filter(h => h.k !== null).length + Math.max(0, st.n - st.hist.length), pct = done ? Math.round(st.right / done * 100) : 0;
      host.innerHTML = `<div class="card done-card"><div class="gbig">♾️</div><h2>Practice summary</h2>
        <p class="sub">${H(topic.title)}</p><p class="sub">You answered <b>${done}</b> question${done === 1 ? '' : 's'} · ✔ <b>${st.right}</b> correct${done ? ` (${pct}%)` : ''} · +${st.xp} ⭐</p>
        <p class="sub">${pct >= 90 && done >= 5 ? 'Superb! You have really got this. 🌟' : done ? 'Every question makes your brain stronger. Keep going! 💪' : 'Try a few questions. They never run out!'}</p>
        <button class="btn" id="gvMore">Keep practising ▶</button><div style="height:8px"></div><button class="btn ghost" id="gvExit">Back to lesson</button></div>`;
      host.querySelector('#gvMore').onclick = () => (st.cur && st.cur.k === null ? draw() : ask());
      host.querySelector('#gvExit').onclick = exit;
      if (window.scrollTo) window.scrollTo(0, 0);
    }
    function exit() { stopTalk(); if (opt.onExit) opt.onExit(); }
    ask();
    if (window.scrollTo) window.scrollTo(0, 0);
    return true;
  }

  window.Gen = { has, next, open, list: () => GENS.map(G => ({ id: G.id, name: G.name, subj: G.subj, g: G.g })), _matching: (id, t, g, s) => matching(id, t, g, s).map(G => G.id), _gens: GENS };
})();
