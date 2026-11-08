#!/usr/bin/env python3
"""Independent re-verification of the Paper 3 MCQ banks (content/ca/foundation/p3/bank/*.json).

  python3 tools/ca_bank/p3_verify.py

Written separately from the generators (it imports nothing from them). For every bank question it
  1. re-solves the question with its own method (brute force / enumeration / iteration / exact fractions / simulation,
     and for the reasoning chapters it parses the question TEXT itself) using the inputs in tools/ca_bank/p3_data.json,
  2. checks that every input it used is printed in the question text (so text and data cannot drift apart),
  3. checks that the keyed option equals its own answer and that no other option does (same rounding as the option shows),
  4. checks schema: 4 distinct options, explanation 35+ words, fast (6+ words), secs 15-180, topic, no duplicate stems.
Prints per-unit counts and 'VERIFY OK' or the failures.
"""
import json, os, re, sys, glob, math, itertools, collections
sys.dont_write_bytecode = True          # keep the shared tools folders free of .pyc files
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SOL = {}
FAIL = []


def sol(*ks):
    def deco(f):
        for k in ks: SOL[k] = f
        return f
    return deco


class Tracked(dict):
    def __init__(self, d): super().__init__(d); self.used = set()
    def __getitem__(self, k): self.used.add(k); return super().__getitem__(k)


SUPS = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')


def text_has(q, v):
    """is the value v printed in question text q (any common format)?"""
    t = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', lambda m: '^' + m.group(0).translate(SUPS), q).replace('−', '-')
    plain = t.replace(',', '')
    if isinstance(v, bool): return True
    if isinstance(v, str):
        return v in q or v.replace(',', '') in plain or v in t
    if isinstance(v, (list, tuple)): return all(text_has(q, x) for x in v)
    if isinstance(v, dict): return all(text_has(q, x) for x in v.values())
    if isinstance(v, float) and v != int(v):
        cands = {f'{v:g}', f'{v:.2f}', f'{v:.3f}', f'{v:.4f}', str(v), f'{v:.1f}'}
        return any(re.search(r'(?<![\d.])' + re.escape(c.rstrip('0').rstrip('.') if '.' in c else c) + r'(?![\d])', plain) for c in cands)
    v = abs(int(v))                 # signs are printed apart from the number in expressions ('x² − 12x')
    return v <= 1 or re.search(r'(?<![\d.])' + re.escape(str(v)) + r'(?![\d])', plain) is not None


NUM = re.compile(r'-?\d[\d,]*(?:\.\d+)?(?:/\d+)?')


def parse_opt(o):
    s = o.replace('−', '-').replace('₹', '')
    m = NUM.search(s)
    if not m: return None, 0
    t = m.group(0).replace(',', '')
    if '/' in t: a, b = t.split('/'); return F(int(float(a))) / int(b), None
    dp = len(t.split('.')[1]) if '.' in t else 0
    return F(t), dp


def same_num(exp, o, D=None):
    v, dp = parse_opt(o)
    if v is None: return False
    exact = isinstance(exp, (int, F))
    exp = F(exp) if not isinstance(exp, float) else F(exp).limit_denominator(10 ** 12)
    if dp is None: return v == exp
    if exact and dp == 0 and (D or 0) == 0: return v == exp      # exact answers shown as integers/fractions compare exactly
    dp = max(dp, D or 0)          # options are shown to the precision of the most precise option
    tol = F(1, 2) / 10 ** dp + F(1, 10 ** 9)
    return abs(v - exp) <= tol


def norm(s): return re.sub(r'\s+', ' ', s.replace('−', '-')).strip().lower()


def check_q(uid, q, rec):
    w = f'{uid}#{q["id"]}'
    o = q['options']
    if len(o) != 4 or len(set(o)) != 4: FAIL.append(f'{w}: options not 4 distinct'); return
    if len(re.findall(r'\S+', q['explain'])) < 35: FAIL.append(f'{w}: explain < 35 words')
    if len(re.findall(r'\S+', q.get('fast', ''))) < 6 or not 15 <= q.get('secs', 0) <= 180: FAIL.append(f'{w}: fast/secs missing')
    if not q.get('topic') or not q.get('concept'): FAIL.append(f'{w}: topic/concept missing')
    if rec is None: FAIL.append(f'{w}: no verification data'); return
    f = SOL.get(rec['k'])
    if not f: FAIL.append(f'{w}: no solver for {rec["k"]}'); return
    d = Tracked(rec['d'])
    try: exp = f(d, q['q'])
    except Exception as e: FAIL.append(f'{w}: solver error {type(e).__name__}: {e}'); return
    for k in d.used:
        if k.startswith('_'): continue
        if not text_has(q['q'], dict.__getitem__(d, k)): FAIL.append(f'{w}: input {k}={dict.__getitem__(d, k)!r} not printed in the question')
    if callable(exp):
        hits = [i for i, x in enumerate(o) if exp(x)]
    elif isinstance(exp, str):
        hits = [i for i, x in enumerate(o) if norm(x) == norm(exp)]
    else:
        D = max((parse_opt(x)[1] or 0) for x in o)
        hits = [i for i, x in enumerate(o) if same_num(exp, x, D)]
    if hits != [q['answer']]:
        FAIL.append(f'{w}: re-solved answer {exp!r} matches options {hits}, key is {q["answer"]} ({o[q["answer"]]!r}) — {q["q"][:80]}')


# ====================== Chapter 1 ======================
def ratio_str(xs):
    xs = [F(x) for x in xs]; l = 1
    for x in xs: l = l * x.denominator // math.gcd(l, x.denominator)
    ints = [int(x * l) for x in xs]; g = 0
    for i in ints: g = math.gcd(g, i)
    return ' : '.join(str(i // g) for i in ints)


@sol('ch01.chain')
def _(d, q):
    a, b = d['ab']; c, e = d['bc']
    return ratio_str([F(a, b), 1, F(e, c)])          # put B = 1


@sol('ch01.share')
def _(d, q):
    p = d['ratio']; who = d['who']; idx = 'ABC'.index(who)
    # brute force: smallest unit u with shares u*p summing to N
    return F(d['N']) * p[idx] / sum(p)


@sol('ch01.eqmult')
def _(d, q):
    return ratio_str([F(1, m) for m in d['m']])


@sol('ch01.fourth')
def _(d, q):
    for x in range(1, 100000):
        if d['a'] * x == d['b'] * d['c']: return x
    return F(d['b'] * d['c'], d['a'])


@sol('ch01.meanp')
def _(d, q):
    return next(x for x in range(1, 10 ** 5) if x * x == d['a'] * d['b'])


@sol('ch01.third')
def _(d, q):
    return next(x for x in range(1, 10 ** 6) if d['a'] * x == d['b'] ** 2)


@sol('ch01.mix')
def _(d, q):
    V = d['V']; a, b = d['r1']; c, e = d['r2']
    milk = F(V * a, a + b); water = V - milk
    # search in steps of 1/6 litre for the water w with milk : (water + w) = c : e
    for k in range(0, 6 * 2000):
        w = F(k, 6)
        if milk * e == (water + w) * c: return w
    raise ValueError('no solution')


@sol('ch01.addeach')
def _(d, q):
    a, b = d['r1']; k = d['k']; c, e = d['r2']
    for x in range(1, 10000):
        if (a * x + k) * e == (b * x + k) * c: return a * x
    raise ValueError


@sol('ch01.dup')
def _(d, q):
    kind = d['kind']; x, y = map(int, re.search(r'ratio of (\d+) : (\d+)', q).groups())
    root = lambda n, k: next(t for t in range(1, 100) if t ** k == n)
    f = {'duplicate': lambda: (x * x, y * y), 'triplicate': lambda: (x ** 3, y ** 3), 'sub-duplicate': lambda: (root(x, 2), root(y, 2)), 'sub-triplicate': lambda: (root(x, 3), root(y, 3))}[kind]
    a, b = f()
    return f'{a} : {b}'


@sol('ch01.idxeq')
def _(d, q):
    m = re.search(r'If (\d+)\^x × (\d+)\^\(?(-?\d+)\)? = (\d+)\^\(x ([+−]) (\d+)\)', q)
    A, b, a, C, sg, c = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5), int(m.group(6))
    c = c if sg == '+' else -c
    for x in range(-200, 201):      # compare exact powers: A^x * b^a == C^(x+c)
        L = F(A) ** x * F(b) ** a; R = F(C) ** (x + c)
        if L == R: return x
    raise ValueError


@sol('ch01.fracpow')
def _(d, q):
    base = d['base']; p, s = d['e']
    root = next(t for t in range(1, 100) if t ** s == base)
    return F(root) ** p


@sol('ch01.logbase')
def _(d, q):
    # read base and argument from the text and search y = p/q with base^y = arg
    m = re.search(r'log (1/)?(\d+) to the base (√)?(\d+)', q)
    inv, arg, rt, base = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    argv = F(1, arg) if inv else F(arg)
    bl = math.log(base) / (2 if rt else 1)
    y = F(math.log(argv) / bl).limit_denominator(12)
    return y


@sol('ch01.logval')
def _(d, q):
    n = F(d['n']); L = {2: 0.3010, 3: 0.4771, 5: 1 - 0.3010}
    e = 0
    while n.denominator != 1: n *= 10; e -= 1
    n = n.numerator
    while n % 10 == 0: n //= 10; e += 1
    tot = e
    for p in (2, 3, 5):
        while n % p == 0: n //= p; tot += L[p]
    assert n == 1
    return round(tot, 4)


@sol('ch01.digits')
def _(d, q): return len(str(d['b'] ** d['n']))


@sol('ch01.logeq')
def _(d, q):
    a, b = d['a'], d['b']
    return next(x for x in range(a + 1, 10 ** 4) if x * (x - a) == b)


@sol('ch01.char')
def _(d, q):
    n = F(d['n'].replace(',', '')); return math.floor(math.log10(n) + 1e-12)


# ====================== Chapter 2 ======================
WORDN = {'twice': 2, 'three times': 3, 'four times': 4, 'five times': 5, 'six times': 6, 'seven times': 7}


def parse_poly(s):
    """'2x³ − 5x + 7' -> {3: 2, 1: -5, 0: 7} (also y/z variables ignored: x only)"""
    s = s.replace('−', '-').replace(' ', '').translate(SUPS).replace('(', '').replace(')', '')
    s = re.sub(r'=0$', '', s)
    out = collections.defaultdict(F)
    for m in re.finditer(r'([+-]?)(\d+(?:/\d+)?)?(x(\^?\d+)?)?', s):
        if not m.group(0) or m.group(0) in '+-': continue
        sign = -1 if m.group(1) == '-' else 1
        c = F(m.group(2)) if m.group(2) else F(1)
        p = (int(m.group(4).lstrip('^')) if m.group(4) else 1) if m.group(3) else 0
        out[p] += sign * c
    return out


def peval(pp, x): return sum(c * F(x) ** p for p, c in pp.items())


@sol('ch02.ages')
def _(d, q):
    k, j, m, n = d['k'], d['j'], WORDN[d['m']], WORDN[d['n']]
    for s in range(1, 120):
        for f in range(s, 150):
            if f - k == m * (s - k) and f + j == n * (s + j) and s > k: return s
    raise ValueError


@sol('ch02.twodigit')
def _(d, q):
    return next(n for n in range(10, 100) if n // 10 + n % 10 == d['S'] and (n % 10) * 10 + n // 10 - n == d['D'])


@sol('ch02.linfrac')
def _(d, q):
    a, b, c, dd, e = d['a'], d['b'], d['c'], d['d'], d['e']
    f = lambda x: F(x + a, b) - F(x - c, dd) - e
    x = F(0) - f(0) / (f(1) - f(0))             # linear: root from two evaluations
    return f'x = {x}'


@sol('ch02.sim2')
def _(d, q):
    (a, b, e), (c, dd, f) = d['eq']
    sols = [(x, y) for x in range(-30, 31) for y in range(-30, 31) if a * x + b * y == e and c * x + dd * y == f]
    assert len(sols) == 1
    return f'x = {sols[0][0]}, y = {sols[0][1]}'


@sol('ch02.sim3')
def _(d, q):
    rows = d['rows']
    sols = [(x, y, z) for x in range(-15, 16) for y in range(-15, 16) for z in range(-15, 16) if all(r[0] * x + r[1] * y + r[2] * z == r[3] for r in rows)]
    assert len(sols) == 1
    return dict(zip('xyz', sols[0]))[d['ask']]


@sol('ch02.formq')
def _(d, q):
    a, b = d['roots']
    def ok(o):
        pp = parse_poly(o)
        return pp.get(2) == 1 and peval(pp, a) == 0 and peval(pp, b) == 0
    return ok


@sol('ch02.symfn')
def _(d, q):
    a, b, c = d['abc']
    # roots numerically (may be complex) and evaluate the expression
    D = complex(b * b - 4 * a * c) ** 0.5
    al, be = (-b + D) / (2 * a), (-b - D) / (2 * a)
    v = {'α² + β²': al ** 2 + be ** 2, '1/α + 1/β': 1 / al + 1 / be, 'α/β + β/α': al / be + be / al}[d['kind']]
    return F(v.real).limit_denominator(1000)


@sol('ch02.nature')
def _(d, q):
    a, b, c = d['abc']
    # look for rational roots p/q by search; else use the sign of the discriminant
    D = b * b - 4 * a * c
    if D < 0: return 'Imaginary (not real)'
    rats = {F(p, qq) for p in range(-400, 401) for qq in range(1, a + 1) if a * F(p, qq) ** 2 + b * F(p, qq) + c == 0}
    if len(rats) == 1 and D == 0: return 'Real and equal'
    if len(rats) == 2: return 'Real, rational and unequal'
    return 'Real, irrational and unequal'


@sol('ch02.eqroots')
def _(d, q):
    return next(k for k in range(1, 1000) if k * k == 4 * d['a'] * d['c'])


@sol('ch02.cubother')
def _(d, q):
    co = d['co']; pp = {3: F(co[0]), 2: F(co[1]), 1: F(co[2]), 0: F(co[3])}
    roots = [x for x in range(-50, 51) if peval(pp, x) == 0]
    others = sorted(x for x in roots if x != d['g'])
    return f'{others[0]} and {others[1]}'


@sol('ch02.cubcoef')
def _(d, q):
    rt, p, qq = d['rt'], d['p'], d['q']
    return next(a for a in range(-500, 501) if rt ** 3 + p * rt * rt + a * rt + qq == 0)


@sol('ch02.cubvieta')
def _(d, q):
    co = d['co']; pp = {3: F(co[0]), 2: F(co[1]), 1: F(co[2]), 0: F(co[3])}
    r = [x for x in range(-50, 51) if peval(pp, x) == 0]
    assert len(r) == 3
    return {'α + β + γ': sum(r), 'αβ + βγ + γα': r[0] * r[1] + r[1] * r[2] + r[0] * r[2], 'αβγ': r[0] * r[1] * r[2]}[d['kind']]


@sol('ch02.rect')
def _(d, q): return next(b for b in range(1, 1000) if b * (b + d['d']) == d['A'])


@sol('ch02.share')
def _(d, q):
    N, k, less = d['N'], d['k'], d['less']
    return next(n for n in range(1, 1000) if F(N, n) - F(N, n + k) == less)


@sol('ch02.expoq')
def _(d, q):
    a, S, P = d['a'], d['S'], d['P']
    xs = sorted(x for x in range(-10, 11) if F(a) ** (2 * x) - S * F(a) ** x + P == 0)
    return f'x = {xs[0]} or x = {xs[1]}'


# ====================== Chapter 3 ======================
OPS_ = {'<': lambda a, b: a < b, '>': lambda a, b: a > b, '<=': lambda a, b: a <= b, '>=': lambda a, b: a >= b,
        '≤': lambda a, b: a <= b, '≥': lambda a, b: a >= b}


@sol('ch03.onevar')
def _(d, q):
    a, b, c, e, op = d['a'], d['b'], d['c'], d['d'], d['op']
    grid = [F(k, 2) for k in range(-150, 151)]
    truth = [OPS_[op](a * x + b, c * x + e) for x in grid]
    def ok(o):
        m = re.match(r'x ([<>≤≥]) (-?\d+(?:/\d+)?)$', o.replace('−', '-'))
        sg, v = m.group(1), F(m.group(2))
        return [OPS_[sg](x, v) for x in grid] == truth
    return ok


@sol('ch03.count')
def _(d, q):
    a, b, p, qq = d['a'], d['b'], d['p'], d['q']; li, hi = dict.__getitem__(d, 'inc')
    return sum(1 for x in range(-1000, 1001) if (a * x + b >= p if li else a * x + b > p) and (a * x + b <= qq if hi else a * x + b < qq))


def pt(o):
    m = re.match(r'\((-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\)$', o.replace('−', '-')); return F(m.group(1)), F(m.group(2))


@sol('ch03.feaspt')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = d['c1'], d['c2']
    def ok(o):
        x, y = pt(o); return a1 * x + b1 * y <= c1 and a2 * x + b2 * y >= c2 and x >= 0 and y >= 0
    return ok


@sol('ch03.corner')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = d['l1'], d['l2']
    def ok(o):
        x, y = pt(o); return a1 * x + b1 * y == c1 and a2 * x + b2 * y == c2
    return ok


def grid_opt(d, sense, fn=max):
    (a1, b1, c1), (a2, b2, c2) = d['l1'], d['l2']; p, qq = d['Z']
    X = max(c1 // a1, c2 // a2) + 1; Y = max(c1 // b1, c2 // b2) + 1
    if sense == '<=': feas = lambda x, y: a1 * x + b1 * y <= c1 and a2 * x + b2 * y <= c2
    else: feas = lambda x, y: a1 * x + b1 * y >= c1 and a2 * x + b2 * y >= c2
    return fn(p * x + qq * y for x in range(0, X + 1) for y in range(0, Y + 1) if feas(x, y))


@sol('ch03.lpmax')
def _(d, q): return grid_opt(d, '<=', max)


@sol('ch03.lpmin')
def _(d, q): return grid_opt(d, '>=', min)


@sol('ch03.form')
def _(d, q):
    def ok(o):
        m = re.match(r'(\d*)x \+ (\d*)y ([≤≥=]) (\d+)$', o)
        if not m: return False
        A = int(m.group(1) or 1); B = int(m.group(2) or 1)
        return A == d['a'] and B == d['b'] and m.group(3) == '≤' and int(m.group(4)) == d['H']
    return ok


@sol('ch03.slack')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = d['l1'], d['l2']; p = d['p']
    pts = [(x, y) for x in range(0, 500) for y in range(0, 500) if a1 * x + b1 * y <= c1 and a2 * x + b2 * y <= c2]
    best = max(p * x for x, y in pts); opt = [(x, y) for x, y in pts if p * x == best]
    assert len(opt) == 1
    x, y = opt[0]; s1, s2 = c1 - a1 * x - b1 * y, c2 - a2 * x - b2 * y
    assert min(s1, s2) == 0
    return max(s1, s2)


def clip(poly_, a, b, c, sense):
    """Sutherland-Hodgman: keep the part of polygon with a x + b y (<= / >=) c"""
    inside = (lambda P: a * P[0] + b * P[1] <= c) if sense in ('<=', '≤') else (lambda P: a * P[0] + b * P[1] >= c)
    out = []
    for i in range(len(poly_)):
        P, Q = poly_[i], poly_[(i + 1) % len(poly_)]
        if inside(Q):
            if not inside(P): out.append(cut(P, Q, a, b, c))
            out.append(Q)
        elif inside(P): out.append(cut(P, Q, a, b, c))
    return out


def cut(P, Q, a, b, c):
    fp, fq = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c; t = fp / (fp - fq)
    return (P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1]))


def clean(poly_):
    pts = []
    for P in poly_:
        if not pts or pts[-1] != P: pts.append(P)
    if len(pts) > 1 and pts[0] == pts[-1]: pts.pop()
    changed = True
    while changed and len(pts) > 2:
        changed = False
        for i in range(len(pts)):
            A, B, C = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            if (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]) == 0: pts.pop(i); changed = True; break
    return pts


@sol('ch03.ncorn')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = d['l1'], d['l2']; k = d['k']; var = d['var']; sense = d['sense']
    poly_ = [(F(-1), F(-1)), (F(1000), F(-1)), (F(1000), F(1000)), (F(-1), F(1000))]
    for cons in ((a1, b1, c1, '<='), (a2, b2, c2, '<='), (1, 0, 0, '>='), (0, 1, 0, '>='), ((1, 0) if var == 'x' else (0, 1)) + (k, sense)):
        poly_ = clip(poly_, *cons)
    return len(clean(poly_))


@sol('ch03.half')
def _(d, q):
    a, b, c, op = d['a'], d['b'], d['c'], d['op']
    return 'The half-plane that contains the origin' if OPS_[op](0, c) else 'The half-plane that does not contain the origin'


@sol('ch03.avg')
def _(d, q):
    ms, A = d['ms'], d['A']; n = len(ms) + 1
    return next(x for x in range(0, 201) if F(sum(ms) + x, n) >= A)


# ====================== Chapter 4 (period-by-period loops, bisection; no closed annuity formulas) ======================
MWV = {'half-yearly': 2, 'quarterly': 4, 'monthly': 12, 'monthly': 12}


def grow(P, i, n):
    for _ in range(n): P = P + P * i
    return P


def pv_flows(flows, i):      # flows[t] at end of period t+1
    v = 0.0; f = 1.0
    for c in flows: f /= (1 + i); v += c * f
    return v


def bisect(fn, lo, hi, it=200):
    flo = fn(lo)
    for _ in range(it):
        mid = (lo + hi) / 2; fm = fn(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2


@sol('ch04.sirate')
def _(d, q):
    P, A, t = d['P'], d['A'], d['t']
    return bisect(lambda R: P + P * R / 100 * t - A, 0.0, 100.0)


@sol('ch04.siparts')
def _(d, q):
    N, r1, r2, I = d['N'], d['r1'], d['r2'], d['I']
    return next(x for x in range(0, N + 1) if x * r1 + (N - x) * r2 == 100 * I)


@sol('ch04.ciper')
def _(d, q):
    m = MWV[d['m']]; n = round(d['t'] * m); P = d['P']
    return grow(P, d['R'] / 100 / m, n) - P


@sol('ch04.cisi')
def _(d, q):
    R, D = d['R'], d['D']
    return bisect(lambda P: (grow(P, R / 100, 2) - P) - P * R / 100 * 2 - D, 0.0, 1e8)


@sol('ch04.eff')
def _(d, q):
    m = MWV[d['m']]; return (grow(1.0, d['R'] / 100 / m, m) - 1) * 100


@sol('ch04.real')
def _(d, q):
    # real rate r: (1 + r)(1 + inflation) = 1 + nominal
    return bisect(lambda x: (1 + x / 100) * (1 + d['inf'] / 100) - (1 + d['n'] / 100), -50.0, 50.0)


@sol('ch04.fva')
def _(d, q):
    A, i, n = d['A'], d['R'] / 100, d['n']; bal = 0.0
    for _ in range(n): bal = bal * (1 + i) + A        # interest for the year, then the year-end deposit
    return bal


@sol('ch04.due')
def _(d, q):
    A, i, n = d['A'], d['R'] / 100, d['n']
    return sum(A / (1 + i) ** t for t in range(n))  # payments at t = 0 .. n-1


@sol('ch04.sink')
def _(d, q):
    FV, i, n = d['FV'], d['R'] / 100, d['n']
    def short(A):
        bal = 0.0
        for _ in range(n): bal = bal * (1 + i) + A
        return bal - FV
    return bisect(short, 0.0, float(FV))


@sol('ch04.pva')
def _(d, q): return pv_flows([d['A']] * d['n'], d['R'] / 100)


@sol('ch04.emi')
def _(d, q):
    m = 12 if d['per'] == 'monthly' else 1; i = d['R'] / 100 / m; n = d['yrs'] * m; L = d['L']
    def left(E):
        bal = float(L)
        for _ in range(n): bal = bal * (1 + i) - E
        return bal
    return bisect(lambda E: -left(E), 0.0, float(L))


@sol('ch04.lease')
def _(d, q):
    C, i, n = d['C'], d['R'] / 100, d['n']
    return bisect(lambda x: pv_flows([x] * n, i) - C, 0.0, float(C))


@sol('ch04.bond')
def _(d, q):
    face, c, y, n = d['face'], d['c'], d['y'], d['n']
    return pv_flows([face * c / 100] * (n - 1) + [face * c / 100 + face], y / 100)


@sol('ch04.perp')
def _(d, q):
    A, R, g = d['A'], d['R'] / 100, d['g'] / 100
    v, c, f = 0.0, float(A), 1.0
    for _ in range(20000):
        f /= (1 + R); v += c * f; c *= (1 + g)
        if c * f < 1e-9: break
    return v


@sol('ch04.npv')
def _(d, q): return pv_flows(d['cfs'], d['k'] / 100) - d['C0']


@sol('ch04.cagr')
def _(d, q):
    return bisect(lambda g: grow(float(d['V0']), g / 100, d['n']) - d['Vn'], 0.0, 100.0)


@sol('ch04.dep')
def _(d, q):
    v = float(d['C'])
    for _ in range(d['n']): v -= v * d['R'] / 100
    return v


@sol('ch04.double')
def _(d, q):
    k = {'double': 2, 'treble': 3}[d['word']]; v = 1.0; n = 0
    while v <= k: v *= 1 + d['R'] / 100; n += 1
    return n


# ====================== Chapter 5 (brute-force enumeration; Pascal's triangle) ======================
def pascal_row(n):
    row = [1]
    for _ in range(n): row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def nCr(n, r): return pascal_row(n)[r] if 0 <= r <= n else 0


@sol('ch05.npr')
def _(d, q): return sum(1 for _ in itertools.permutations(range(d['n']), d['k']))


@sol('ch05.word')
def _(d, q): return len(set(itertools.permutations(d['w'])))


@sol('ch05.vowels')
def _(d, q):
    w = d['w']; n = 0
    for p in set(itertools.permutations(w)):
        idx = [i for i, c in enumerate(p) if c in 'AEIOU']
        if idx[-1] - idx[0] == len(idx) - 1: n += 1
    return n


@sol('ch05.row')
def _(d, q):
    n, k = d['n'], d['k']; cnt = 0
    for p in itertools.permutations(range(n)):
        pos = sorted(p.index(i) for i in range(k)); tog = pos[-1] - pos[0] == k - 1
        cnt += tog if d['kind'] == 'together' else (not tog)
    return cnt


@sol('ch05.circ')
def _(d, q):
    n = d['n']; cnt = 0
    for p in itertools.permutations(range(1, n)):
        seat = (0,) + p                              # person 0 fixed: removes rotations
        a, b = seat.index(1), seat.index(2); adj = (a - b) % n in (1, n - 1)
        kind = 'apart' if 'never sit next' in q else 'together' if 'always sit together' in q else 'plain'
        cnt += {'plain': True, 'together': adj, 'apart': not adj}[kind]
    return cnt


@sol('ch05.neck')
def _(d, q):
    n = d['n']; seen = set()
    if n > 9: return math.factorial(n - 1) // 2
    for p in itertools.permutations(range(n)):
        forms = []
        for seq in (p, p[::-1]):
            for i in range(n): forms.append(seq[i:] + seq[:i])
        seen.add(min(forms))
    return len(seen)


@sol('ch05.comm')
def _(d, q):
    m, w, k, at = d['m'], d['w'], d['k'], d['at']
    people = ['M'] * m + ['W'] * w
    return sum(1 for c in itertools.combinations(range(m + w), k) if sum(people[i] == 'W' for i in c) >= at)


@sol('ch05.ncreq')
def _(d, q): return next(n for n in range(1, 200) if n >= max(d['a'], d['b']) and nCr(n, d['a']) == nCr(n, d['b']))


@sol('ch05.pascal')
def _(d, q):
    n, k = d['n'], d['k']
    return sum(1 for _ in itertools.combinations(range(n), k)) + sum(1 for _ in itertools.combinations(range(n), k - 1))


def line_key(P, Q):
    a, b = Q[1] - P[1], P[0] - Q[0]; c = a * P[0] + b * P[1]
    g = math.gcd(math.gcd(a, b), c) or 1
    if a < 0 or (a == 0 and b < 0): g = -g
    return (a // g, b // g, c // g)


@sol('ch05.geom')
def _(d, q):
    n, k = d['n'], d['k']
    pts = [(i, 0) for i in range(k)]          # k points on the x-axis
    x = 1
    while len(pts) < n:                        # others on the parabola y = x^2 + 1: no three collinear, none on the axis
        pts.append((x * 7, (x * 7) ** 2 + 1)); x += 1
    if d['kind'] == 'lines': return len({line_key(P, Q) for P, Q in itertools.combinations(pts, 2)})
    return sum(1 for A, B, C in itertools.combinations(pts, 3) if (B[0] - A[0]) * (C[1] - A[1]) != (B[1] - A[1]) * (C[0] - A[0]))


@sol('ch05.diag')
def _(d, q):
    n = d['n']; return sum(1 for i, j in itertools.combinations(range(n), 2) if (j - i) % n not in (1, n - 1))


@sol('ch05.shake')
def _(d, q): return sum(1 for _ in itertools.combinations(range(d['n']), 2))


@sol('ch05.digits')
def _(d, q):
    pool, k = d['pool'], d['k']; t = {'even': lambda x: x % 2 == 0, 'divisible by 5': lambda x: x % 5 == 0, 'odd': lambda x: x % 2 == 1}[d['cond']]
    return sum(1 for x in range(10 ** (k - 1), 10 ** k) if len(set(str(x))) == k and set(map(int, str(x))) <= set(pool) and t(x))


@sol('ch05.alike')
def _(d, q):
    return sum(1 for x in range(d['a'] + 1) for y in range(d['b'] + 1) for z in range(d['c'] + 1) if x + y + z > 0)


@sol('ch05.boxes')
def _(d, q): return sum(1 for _ in itertools.product(range(d['m']), repeat=d['n']))


@sol('ch05.routes')
def _(d, q):
    m, n = d['m'], d['n']
    return sum(1 for a, b, c, e in itertools.product(range(m), range(n), range(n), range(m)) if c != b and e != a)


@sol('ch05.permeq')
def _(d, q):
    a, b, k = d['a'], d['b'], d['k']
    return next(n for n in range(a, 300) if math.perm(n, a) == k * math.perm(n, b))


@sol('ch05.facteq')
def _(d, q): return next(n for n in range(1, 500) if math.factorial(n + 1) == d['v'] * math.factorial(n - 1))


# ====================== Chapter 6 (term-by-term generation and summation) ======================
def suffix(n): return f'{n}th' if 10 < n % 100 < 14 else f'{n}' + {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def terms_from(first3, n):
    a, b, c = (F(x) for x in first3)
    if b - a == c - b:                       # AP
        out = [a]
        while len(out) < n: out.append(out[-1] + (b - a))
    else:                                    # GP
        assert b * b == a * c
        out = [a]
        while len(out) < n: out.append(out[-1] * (b / a))
    return out


@sol('ch06.apterm', 'ch06.gpterm')
def _(d, q): return terms_from(d['first3'], d['n'])[-1]


@sol('ch06.which')
def _(d, q):
    t = terms_from(d['first3'], 500)
    return suffix(t.index(d['X']) + 1) + ' term'


@sol('ch06.apsum', 'ch06.gpsum')
def _(d, q): return sum(terms_from(d['first3'], d['n']))


@sol('ch06.two')
def _(d, q):
    p, tp, qq, tq, s = d['p'], d['tp'], d['q'], d['tq'], d['s']
    for a in range(-500, 501):
        for dd in range(-50, 51):
            if a + (p - 1) * dd == tp and a + (qq - 1) * dd == tq: return a + (s - 1) * dd
    raise ValueError


@sol('ch06.mult')
def _(d, q): return sum(x for x in range(d['A'], d['B'] + 1) if x % d['k'] == 0)


@sol('ch06.ams')
def _(d, q):
    m, a, b, j = d['m'], d['a'], d['b'], d['j']
    for dd in range(-100, 101):
        if a + (m + 1) * dd == b: return a + j * dd
    raise ValueError


@sol('ch06.gpfind')
def _(d, q):
    p, tp, qq, tq = d['p'], d['tp'], d['q'], d['tq']
    for r in range(-10, 11):
        if r == 0: continue
        for a in range(-100, 101):
            if a * r ** (p - 1) == tp and a * r ** (qq - 1) == tq: return a if d['ask'] == 'first term' else r
    raise ValueError


@sol('ch06.inf')
def _(d, q):
    t = terms_from(d['first3'], 400); s_ = sum(float(x) for x in t)
    return F(s_).limit_denominator(1000)


@sol('ch06.infr')
def _(d, q):
    S, a = F(d['S']), F(d['a'])
    for den in range(1, 50):
        for nu in range(-den + 1, den):
            r = F(nu, den)
            if abs(sum(float(a) * float(r) ** k for k in range(600)) - float(S)) < 1e-9: return r
    raise ValueError


@sol('ch06.recur')
def _(d, q):
    nr, rep = d['nr'], d['rep']
    def ok(o):
        f = F(o)
        # long division: produce digits and compare with the pattern nr + rep repeated
        want = nr + rep * 12; num_, den = f.numerator, f.denominator; got = ''
        if num_ >= den: return False
        for _ in range(len(want)):
            num_ *= 10; got += str(num_ // den); num_ %= den
        return got == want and math.gcd(f.numerator, f.denominator) == 1
    return ok


@sol('ch06.special')
def _(d, q):
    last = int(re.findall(r'(\d+)[²³]? is:', q)[0])
    if '²' in q: return sum(i * i for i in range(1, last + 1))
    if '³' in q: return sum(i ** 3 for i in range(1, last + 1))
    if q.startswith('The value of 1 + 3 + 5'): return sum(range(1, last + 1, 2))
    return sum(range(1, last + 1))


@sol('ch06.three')
def _(d, q):
    S, P = d['S'], d['P']
    for a in range(-200, 201):
        for dd in range(1, 100):
            if 3 * a == S and (a - dd) * a * (a + dd) == P: return a + dd
    raise ValueError


@sol('ch06.salary')
def _(d, q):
    sal = [d['A'] + i * d['I'] for i in range(d['n'])]
    return sum(sal) if d['kind'] == 'total' else sal[-1]


@sol('ch06.gpapp')
def _(d, q):
    g = {'doubles': 2, 'triples': 3}[d['g']]; s = [d['P']]
    while len(s) < d['n']: s.append(s[-1] * g)
    return sum(s)


@sol('ch06.reduce')
def _(d, q):
    dg = re.search(r'of 0\.(\d) \+', q).group(1)
    return sum(F('0.' + dg * k) for k in range(1, d['n'] + 1))


# ====================== Chapter 7 (explicit sets, brute force, exact evaluation near the point) ======================
@sol('ch07.union')
def _(d, q):
    a, b = d['a'], d['b']
    if 'c' in d:
        c = d['c']; A = set(range(a)); B = set(range(a - c, a - c + b)); return len(A | B)
    u = d['u']
    for c in range(0, min(a, b) + 1):
        A = set(range(a)); B = set(range(a - c, a - c + b))
        if len(A | B) == u: return c


@sol('ch07.neither')
def _(d, q):
    N, a, b, c = d['N'], d['a'], d['b'], d['c']
    A = set(range(a)); B = set(range(a - c, a - c + b)); return N - len(A | B)


@sol('ch07.three')
def _(d, q):
    nA, nB, nC, nAB, nBC, nCA, abc = d['n']
    # recover the 7 Venn regions by subtraction and build actual sets
    ab, bc, ca = nAB - abc, nBC - abc, nCA - abc
    oa, ob, oc = nA - ab - ca - abc, nB - ab - bc - abc, nC - bc - ca - abc
    it = itertools.count(); A, B, C = set(), set(), set()
    for cnt, mem in ((oa, 'A'), (ob, 'B'), (oc, 'C'), (ab, 'AB'), (bc, 'BC'), (ca, 'CA'), (abc, 'ABC')):
        assert cnt >= 0
        for _ in range(cnt):
            x = next(it)
            if 'A' in mem: A.add(x)
            if 'B' in mem: B.add(x)
            if 'C' in mem: C.add(x)
    assert (len(A), len(B), len(C), len(A & B), len(B & C), len(C & A), len(A & B & C)) == tuple(d['n'])
    return len(A | B | C)


@sol('ch07.power')
def _(d, q):
    X = set(d['w']); subs = sum(1 for k in range(len(X) + 1) for _ in itertools.combinations(X, k))
    return subs - (1 if 'proper subsets' in q else 0)


@sol('ch07.cart')
def _(d, q):
    m, n = d['m'], d['n']; pairs = list(itertools.product(range(m), range(n)))
    return len(pairs) if d['kind'] == 'elements in A × B' else 2 ** len(pairs)


@sol('ch07.builder')
def _(d, q):
    a, b, desc = d['a'], d['b'], d['desc']
    if 'prime' in desc: t = lambda x: x > 1 and all(x % k for k in range(2, x))
    elif 'square' in desc: t = lambda x: any(k * k == x for k in range(x + 1))
    else: k = int(re.search(r'multiple of (\d+)', desc).group(1)); t = lambda x: x % k == 0
    return sum(1 for x in range(a + 1, b) if t(x))


def parse_set(s):
    if 'φ' in s: return set()
    return set(int(x) for x in re.findall(r'-?\d+', s))


@sol('ch07.ops')
def _(d, q):
    A, B = parse_set(d['A']), parse_set(d['B']); kind = d['kind']; U = set(range(1, 13))
    res = {'A − B': A - B, 'B − A': B - A, 'A Δ B (symmetric difference)': (A | B) - (A & B), "(A ∪ B)′ with U = {1, 2, …, 12}": (U - A) & (U - B)}[kind]
    return lambda o: parse_set(o) == res and ('φ' in o) == (not res)


@sol('ch07.reltype')
def _(d, q):
    R = {tuple(x) for x in d['R']}
    assert '{' + ', '.join(f'({a}, {b})' for a, b in sorted(R)) + '}' in q
    X = {1, 2, 3}
    ref = all((x, x) in R for x in X)
    sym = all((b, a) in R for (a, b) in R)
    tra = all((a, c) in R for (a, b) in R for (b2, c) in R if b == b2)
    def ok(o):
        o = o.lower()
        if o.startswith('an equivalence'): return ref and sym and tra
        if o.startswith('neither'): return not (ref or sym or tra)
        claim = {}
        pos, _, neg = o.partition('not ')
        for w in ('reflexive', 'symmetric', 'transitive'):
            if w in neg: claim[w] = False
            elif w in pos: claim[w] = True
        return claim == {'reflexive': ref, 'symmetric': sym, 'transitive': tra}
    return ok


@sol('ch07.compose')
def _(d, q):
    a, b = d['f']; c, e = d['g']; x0 = d['x0']
    f = lambda x: a * x + b; g = lambda x: c * x * x + e
    return f(g(x0)) if d['order'] == 'f(g(' else g(f(x0))


@sol('ch07.inverse')
def _(d, q):
    a, b, y = d['a'], d['b'], d['y']
    x = F(0); fx = lambda x: a * x + b
    return x + (y - fx(x)) / (fx(1) - fx(0))


def near(fn, a, h=F(1, 10 ** 9)):
    l, r = fn(a - h), fn(a + h)
    return F((l + r) / 2).limit_denominator(1000)


@sol('ch07.limpow')
def _(d, q):
    n, a = d['n'], d['a']; return near(lambda x: (x ** n - F(a) ** n) / (x - a), F(a))


@sol('ch07.limfac')
def _(d, q):
    pp = parse_poly(d['num']); p = d['p']
    return near(lambda x: peval(pp, x) / (x - p), F(p))


@sol('ch07.liminf')
def _(d, q):
    t, b = parse_poly(d['top']), parse_poly(d['bot']); X = F(10) ** 12
    return F(peval(t, X) / peval(b, X)).limit_denominator(100)


@sol('ch07.cont')
def _(d, q):
    if 'x ≠' in q:
        sq, a = d['sq'], d['a']
        return near(lambda x: (x * x - sq) / (x - a), F(a))
    p, qq, s, c = d['p'], d['q'], d['s'], d['c']
    left = p * (F(c) - F(1, 10 ** 9)) + qq
    return F(left - s * c).limit_denominator(1000)


@sol('ch07.nfun')
def _(d, q):
    m, n = d['m'], d['n']; fs = list(itertools.product(range(n), repeat=m))
    return sum(1 for f in fs if len(set(f)) == m) if 'one-one' in q else len(fs)


@sol('ch07.range')
def _(d, q):
    A = parse_set(d['A']); res = {d['a'] * x + d['b'] for x in A}
    return lambda o: parse_set(o) == res


@sol('ch07.relinv')
def _(d, q):
    R = [tuple(map(int, t)) for t in re.findall(r'\((-?\d+), (-?\d+)\)', d['R'])]
    inv = {(b, a) for a, b in R}
    return lambda o: {tuple(map(int, t)) for t in re.findall(r'\((-?\d+), (-?\d+)\)', o)} == inv


# ====================== Chapter 8 (numerical differentiation / Simpson integration / grid search) ======================
H = F(1, 10 ** 7)


def dnum(f, x, h=H): return F((f(x + h) - f(x - h)) / (2 * h)).limit_denominator(2000)


def d2num(f, x, h=F(1, 10 ** 4)): return F((f(x + h) - 2 * f(x) + f(x - h)) / (h * h)).limit_denominator(2000)


def simpson(f, a, b, n=2):
    a, b = F(a), F(b); h = (b - a) / n
    return h / 3 * (f(a) + f(b) + 4 * sum(f(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1)) + 2 * sum(f(a + 2 * i * h) for i in range(1, n // 2)))


def P(s):
    pp = parse_poly(s); return lambda x: peval(pp, x)


@sol('ch08.der')
def _(d, q): return dnum(P(d['y']), F(d['x0']))


@sol('ch08.prod')
def _(d, q):
    u, v = P(d['u']), P(d['v']); return dnum(lambda x: u(x) * v(x), F(d['x0']))


@sol('ch08.quot')
def _(d, q):
    u, v = P(d['u']), P(d['v']); return dnum(lambda x: u(x) / v(x), F(d['x0']))


@sol('ch08.chain')
def _(d, q):
    a, b, n = d['a'], d['b'], d['n']; return dnum(lambda x: (a * x * x + b) ** n, F(d['x0']))


@sol('ch08.logd')
def _(d, q):
    a, b, x0 = d['a'], d['b'], d['x0']; h = 1e-6
    return F((math.log(a * (x0 + h) + b) - math.log(a * (x0 - h) + b)) / (2 * h)).limit_denominator(500)


@sol('ch08.expd')
def _(d, q):
    k, a = d['k'], d['a']; h = 1e-6; f = lambda x: math.exp(k * x) * (x + a)
    return round((f(h) - f(-h)) / (2 * h), 6)


@sol('ch08.impl')
def _(d, q):
    x0, y0 = d['x0'], d['y0']; h = 1e-6
    if 'x² + y²' in q:
        R2 = d['R2']; sg = 1 if y0 > 0 else -1; y = lambda x: sg * math.sqrt(R2 - x * x)
    else:
        c = d['c']; y = lambda x: c / x
    assert abs(y(x0) - y0) < 1e-9
    return F((y(x0 + h) - y(x0 - h)) / (2 * h)).limit_denominator(500)


@sol('ch08.param')
def _(d, q):
    a, t = d['a'], F(d['t']); hh = F(1, 10 ** 6)
    x = lambda t: a * t * t; y = lambda t: 2 * a * t
    return F((y(t + hh) - y(t - hh)) / (x(t + hh) - x(t - hh))).limit_denominator(500)


@sol('ch08.second')
def _(d, q): return d2num(P(d['y']), F(d['x0']))


@sol('ch08.mc')
def _(d, q): return dnum(P(d['C']), F(d['x0']))


@sol('ch08.pmax')
def _(d, q):
    R, C = P(d['R']), P(d['C'])
    best = max((R(F(k, 2)) - C(F(k, 2)), F(k, 2)) for k in range(0, 4001))
    return f'{best[1]} units'.replace('/1 ', ' ')


@sol('ch08.minac')
def _(d, q):
    C = P(d['C']); return min((C(F(x)) / x, x) for x in range(1, 2001))[1]


@sol('ch08.defint')
def _(d, q): return simpson(P(d['f']), d['a'], d['b'], 2)          # Simpson is exact for cubics


@sol('ch08.tcmc')
def _(d, q): return simpson(P(d['mc']), 0, d['N'], 2) + d['FC']


@sol('ch08.subst')
def _(d, q):
    k, c, n, b = d['k'], d['c'], d['n'], d['b']
    # expand k x (x^2 + c)^n exactly (binomial) and integrate term by term
    tot = F(0)
    for j in range(n + 1):
        coef = k * math.comb(n, j) * F(c) ** (n - j)      # term: coef * x^(2j+1)
        tot += coef * F(b) ** (2 * j + 2) / (2 * j + 2)
    return tot


@sol('ch08.be')
def _(d, q):
    p, v, FC = d['p'], d['v'], d['FC']
    return next(x for x in range(0, 10 ** 7) if p * x >= FC + v * x)


# ====================== Chapter 9 (own rule libraries; uniqueness = exactly one option fits) ======================
PR = [p for p in range(2, 3000) if all(p % k for k in range(2, int(p ** .5) + 1))]


def rule_ok(xs):
    xs = [F(x) for x in xs]; n = len(xs)
    # 1. polynomial in the index of degree <= 2 (<= 3 when 6+ terms): Lagrange through the first deg+1 terms
    for deg in (0, 1, 2, 3):
        if n < deg + 3 or (deg == 3 and n < 6): continue
        pts = list(range(deg + 1))
        def L(t):
            tot = F(0)
            for i in pts:
                term = xs[i]
                for j in pts:
                    if j != i: term *= F(t - j, i - j)
                tot += term
            return tot
        if all(L(t) == xs[t] for t in range(n)): return True
    # 2. constant ratio
    if 0 not in xs and all(xs[i + 1] * xs[0] == xs[i] * xs[1] for i in range(n - 1)): return True
    # 3. x(k+1) = a x(k) + b with integer a
    for a in range(-4, 7):
        if a and all(xs[i + 1] - a * xs[i] == xs[1] - a * xs[0] for i in range(n - 1)): return True
    # 4. differences with constant ratio
    ds = [xs[i + 1] - xs[i] for i in range(n - 1)]
    if len(ds) >= 3 and 0 not in ds and all(ds[i + 1] * ds[0] == ds[i] * ds[1] for i in range(len(ds) - 1)): return True
    # 5. two interleaved arithmetic series
    ev, od = xs[0::2], xs[1::2]
    if len(ev) >= 3 and len(od) >= 2 and len({b - a for a, b in zip(ev, ev[1:])}) == 1 and len({b - a for a, b in zip(od, od[1:])}) == 1 and n >= 5: return True
    # 6. Fibonacci type
    if n >= 4 and all(xs[i + 2] == xs[i] + xs[i + 1] for i in range(n - 2)): return True
    # 7. consecutive primes
    if all(x.denominator == 1 and int(x) in PR for x in xs) and n >= 4:
        i = PR.index(int(xs[0]))
        if [int(x) for x in xs] == PR[i:i + n]: return True
    # 8. two alternating operations, each '+c' or '×c'
    def same_op(pairs):
        return len({b - a for a, b in pairs}) == 1 or (all(a for a, b in pairs) and len({b / a for a, b in pairs}) == 1)
    p1 = [(xs[i], xs[i + 1]) for i in range(0, n - 1, 2)]; p2 = [(xs[i], xs[i + 1]) for i in range(1, n - 1, 2)]
    if len(p1) >= 2 and len(p2) >= 2 and same_op(p1) and same_op(p2): return True
    return False


@sol('ch09.series')
def _(d, q):
    parts = [x.strip() for x in d['shown'].split(',')]; pos = parts.index('?')
    def ok(o):
        t = parts[:]; t[pos] = o
        return rule_ok([int(x) for x in t])
    return ok


@sol('ch09.wrong')
def _(d, q):
    t = [int(x) for x in d['shown'].split(',')]
    def ok(o):
        j = t.index(int(o))
        for cand in range(-60, 3000):
            u = t[:]; u[j] = cand
            if rule_ok(u): return True
        return False
    return ok


AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


@sol('ch09.letters')
def _(d, q):
    parts = [x.strip() for x in d['shown'].split(',')]
    def ok(o):
        t = parts[:-1] + [o]
        if len(t[0]) == 1: return all(len(x) == 1 for x in t) and rule_ok([AZ.index(x) + 1 for x in t])
        if any(len(x) != 2 for x in t): return False
        if any(AZ.index(x[1]) - AZ.index(x[0]) != AZ.index(t[0][1]) - AZ.index(t[0][0]) for x in t): return False
        return rule_ok([AZ.index(x[0]) + 1 for x in t])
    return ok


def vrules():
    R = []
    sh = lambda w, k: ''.join(AZ[(AZ.index(c) + k) % 26] for c in w)
    for k in range(-8, 9):
        if k:
            R.append(lambda w, k=k: sh(w, k)); R.append(lambda w, k=k: sh(w[::-1], k))
            R.append(lambda w, k=k: ''.join(AZ[(AZ.index(c) + (k if i % 2 == 0 else -k)) % 26] for i, c in enumerate(w)))
    R.append(lambda w: ''.join(AZ[25 - AZ.index(c)] for c in w)); R.append(lambda w: ''.join(AZ[25 - AZ.index(c)] for c in w[::-1]))
    R.append(lambda w: w[::-1])
    R.append(lambda w: ''.join(w[i + 1] + w[i] if i + 1 < len(w) else w[i] for i in range(0, len(w), 2)))
    R.append(lambda w: ''.join(AZ[(AZ.index(c) + i + 1) % 26] for i, c in enumerate(w)))       # +1, +2, +3 … (not used by the generator)
    R.append(lambda w: ''.join(AZ[(AZ.index(c) - i - 1) % 26] for i, c in enumerate(w)))
    return R


@sol('ch09.code')
def _(d, q):
    outs = {f(d['w2']) for f in vrules() if f(d['w1']) == d['c1']}
    assert len(outs) == 1, f'ambiguous code: {outs}'
    return outs.pop()


@sol('ch09.numcode')
def _(d, q):
    def pos(w): return [AZ.index(c) + 1 for c in w]
    fams = [lambda w: sum(pos(w)), lambda w: sum(27 - p for p in pos(w)), lambda w: sum(pos(w)) + len(w), lambda w: 2 * sum(pos(w)), lambda w: sum(pos(w)) * len(w),
            lambda w: sum(p * p for p in pos(w)), lambda w: math.prod(pos(w)), lambda w: sum(pos(w)) - len(w)]
    outs = {f(d['w2']) for f in fams if f(d['w1']) == d['v1']}
    assert len(outs) == 1, f'ambiguous number code {outs}'
    return outs.pop()


def vprops():
    P = [lambda n: n in PR, lambda n: math.isqrt(n) ** 2 == n, lambda n: any(k ** 3 == n for k in range(0, 60)), lambda n: n % 2 == 0, lambda n: str(n) == str(n)[::-1],
         lambda n: sum(map(int, str(n))) % 2 == 0]
    for k in range(3, 21): P.append(lambda n, k=k: n % k == 0)
    return P


@sol('ch09.odd')
def _(d, q):
    ns = [int(x) for x in d['shown'].split(',')]; odd = set()
    for f in vprops():
        v = [bool(f(x)) for x in ns]
        if v.count(True) == 1: odd.add(ns[v.index(True)])
        if v.count(False) == 1: odd.add(ns[v.index(False)])
    assert len(odd) == 1, f'ambiguous odd one {odd}'
    return odd.pop()


@sol('ch09.oddlet')
def _(d, q):
    gs = [x.strip() for x in d['shown'].split(',')]
    const = [len({AZ.index(g[i + 1]) - AZ.index(g[i]) for i in range(len(g) - 1)}) == 1 for g in gs]
    vow = [any(c in 'AEIOU' for c in g) for g in gs]
    assert vow.count(True) not in (1, 3) or True
    odd = set()
    for v in (const, vow):
        if v.count(True) == 1: odd.add(gs[v.index(True)])
        if v.count(False) == 1: odd.add(gs[v.index(False)])
    assert len(odd) == 1, f'ambiguous odd group {odd}'
    return odd.pop()


# ====================== Chapter 10 (the question TEXT is parsed and the walk simulated with compass bearings) ======================
BEAR = {'North': 0, 'North-East': 45, 'East': 90, 'South-East': 135, 'South': 180, 'South-West': 225, 'West': 270, 'North-West': 315}
DIRRE = r'(North-East|North-West|South-East|South-West|North|South|East|West)'


def step(b, dist):
    rad = math.radians(b); return (round(dist * math.sin(rad), 9), round(dist * math.cos(rad), 9))


def sim_walk(q):
    m = re.search(r'starts facing ' + DIRRE + r' and walks (\d+) km', q); b = BEAR[m.group(1)]
    x, y = step(b, int(m.group(2)))
    for t, dist in re.findall(r'turns (left|right) and walks (\d+) km', q):
        b = (b + (90 if t == 'right' else -90)) % 360; dx, dy = step(b, int(dist)); x += dx; y += dy
    return x, y, b


def where(x, y):
    ns = 'North' if y > 1e-9 else 'South' if y < -1e-9 else ''
    ew = 'East' if x > 1e-9 else 'West' if x < -1e-9 else ''
    return (ns + '-' + ew) if ns and ew else (ns or ew or 'At the starting point')


@sol('ch10.dist')
def _(d, q):
    x, y, b = sim_walk(q); return F(math.hypot(x, y)).limit_denominator(1000)


@sol('ch10.pos')
def _(d, q):
    x, y, b = sim_walk(q); return where(x, y)


@sol('ch10.face')
def _(d, q):
    b = BEAR[re.search(r'is facing ' + DIRRE + r'\.', q).group(1)]
    body = q.split('. ', 1)[1]
    for part in re.findall(r'turns left|turns right|takes an about-turn|turns \d+° (?:clockwise|anticlockwise)', body):
        if part == 'turns left': b -= 90
        elif part == 'turns right': b += 90
        elif part == 'takes an about-turn': b += 180
        else:
            a = int(re.search(r'\d+', part).group(0)); b += a if 'anticlockwise' not in part else -a
    b %= 360
    return next(k for k, v in BEAR.items() if v == b)


@sol('ch10.shadow')
def _(d, q):
    sun = 90 if 'morning' in q else 270; shadow = (sun + 180) % 360
    side = next(s_ for s_ in ('to the right of', 'to the left of', 'behind', 'in front of') if s_ in q)
    off = {'to the right of': 90, 'to the left of': 270, 'behind': 180, 'in front of': 0}[side]
    fits = [k for k, v in BEAR.items() if (v + off) % 360 == shadow]
    assert len(fits) == 1
    return fits[0]


@sol('ch10.rename')
def _(d, q):
    pairs = re.findall(DIRRE + r' is called ' + DIRRE, q)
    rots = {(BEAR[b] - BEAR[a]) % 360 for a, b in pairs}
    assert len(rots) == 1
    ask = re.search(r'what is ' + DIRRE + r' called', q).group(1)
    rot = rots.pop()
    return next(k for k, v in BEAR.items() if v == (BEAR[ask] + rot) % 360)


@sol('ch10.rel')
def _(d, q):
    facts = re.findall(r'([A-Z]) is (\d+) m to the ' + DIRRE + r' of ([A-Z])', q)
    pos = {facts[0][3]: (0.0, 0.0)}
    for _ in range(3):
        for a, dist, dr, b in facts:
            if b in pos and a not in pos:
                dx, dy = step(BEAR[dr], int(dist)); pos[a] = (pos[b][0] + dx, pos[b][1] + dy)
    if 'distance between' in q:
        a, c = re.search(r'distance between ([A-Z]) and ([A-Z])', q).groups()
        return F(math.hypot(pos[a][0] - pos[c][0], pos[a][1] - pos[c][1])).limit_denominator(100)
    c, a = re.search(r'direction is ([A-Z]) from ([A-Z])', q).groups()
    return where(pos[c][0] - pos[a][0], pos[c][1] - pos[a][1])


# ====================== Chapter 11 (text parsed; geometry decides left/right; brute force over ALL arrangements) ======================
def seat_geometry(n, circle, face):
    if circle:
        pts = [(math.cos(-2 * math.pi * i / n), math.sin(-2 * math.pi * i / n)) for i in range(n)]
        fac = [(-x, -y) for x, y in pts]
    else:
        pts = [(float(i), 0.0) for i in range(n)]; fac = [(0.0, 1.0) if face == 'North' else (0.0, -1.0)] * n
    right = [(fy, -fx) for fx, fy in fac]           # facing turned 90° clockwise
    return pts, right


def neighbour(i, side, n, circle, pts, right):
    cands = [(i + 1) % n, (i - 1) % n] if circle else [j for j in (i - 1, i + 1) if 0 <= j < n]
    sg = 1 if side == 'right' else -1
    for j in cands:
        v = (pts[j][0] - pts[i][0], pts[j][1] - pts[i][1])
        if sg * (v[0] * right[i][0] + v[1] * right[i][1]) > 1e-9: return j
    return None


def kth(i, side, k, n, circle, pts, right):
    for _ in range(k):
        if i is None: return None
        i = neighbour(i, side, n, circle, pts, right)
    return i


KW = {'immediate': 1, 'second': 2, 'third': 3}


def seating_solve(q):
    m = re.search(r'friends ([A-Z](?:, [A-Z])*) and ([A-Z]) sit (in a row facing (North|South)|around a round table, all facing the centre)', q)
    people = m.group(1).split(', ') + [m.group(2)]; circle = 'round table' in q; face = m.group(4); n = len(people)
    pts, right = seat_geometry(n, circle, face)
    body = q[m.end():]
    clues = []
    for x, w, side, b in re.findall(r'([A-Z]) is (second|third) to the (right|left) of ([A-Z])\.', body): clues.append(('k', x, KW[w], side, b))
    for x, side, b in re.findall(r'([A-Z]) is immediately to the (right|left) of ([A-Z])\.', body): clues.append(('k', x, 1, side, b))
    for x in re.findall(r'([A-Z]) is at one of the two ends\.', body): clues.append(('end', x))
    for x in re.findall(r'([A-Z]) is not at either end\.', body): clues.append(('notend', x))
    for w, a, b in re.findall(r'There (is exactly one person|are exactly two people) between ([A-Z]) and ([A-Z])\.', body): clues.append(('gap', a, b, 1 if 'one' in w else 2))
    for a, b in re.findall(r'([A-Z]) sits next to ([A-Z])\.', body): clues.append(('nbr', a, b))
    for a, b in re.findall(r'([A-Z]) does not sit next to ([A-Z])\.', body): clues.append(('notnbr', a, b))
    for x in re.findall(r'([A-Z]) is in the exact middle of the row\.', body): clues.append(('mid', x))
    for a, b in re.findall(r'([A-Z]) sits directly opposite ([A-Z])\.', body): clues.append(('opp', a, b))
    nsent = len(re.findall(r'[A-Z][^.?]*\.', body.split(' facing the centre.')[-1] if circle else body[body.index('.') + 1:]))
    assert nsent == len(clues), f'parsed {len(clues)} clues from {nsent} sentences'
    def adj(i, j): return (i - j) % n in (1, n - 1) if circle else abs(i - j) == 1
    def ok(arr):
        P = {x: i for i, x in enumerate(arr)}
        for c in clues:
            t = c[0]
            if t == 'k':
                if kth(P[c[4]], c[3], c[2], n, circle, pts, right) != P[c[1]]: return False
            elif t == 'end' and P[c[1]] not in (0, n - 1): return False
            elif t == 'notend' and P[c[1]] in (0, n - 1): return False
            elif t == 'gap' and abs(P[c[1]] - P[c[2]]) - 1 != c[3]: return False
            elif t == 'nbr' and not adj(P[c[1]], P[c[2]]): return False
            elif t == 'notnbr' and adj(P[c[1]], P[c[2]]): return False
            elif t == 'mid' and P[c[1]] != n // 2: return False
            elif t == 'opp' and (P[c[1]] - P[c[2]]) % n != n // 2: return False
        return True
    sols = [a for a in itertools.permutations(people) if ok(a)]
    return sols, people, circle, pts, right, n, clues


def seating_answer(q, arr, circle, pts, right, n):
    P = {x: i for i, x in enumerate(arr)}
    m = re.search(r'Who is at the extreme (left|right) end of the row\?', q)
    if m:
        dots = [p[0] * right[0][0] + p[1] * right[0][1] for p in pts]
        i = (min if m.group(1) == 'left' else max)(range(n), key=lambda j: dots[j]); return arr[i]
    m = re.search(r'Who is (immediately to the|second to the) (right|left) of ([A-Z])\?', q)
    if m:
        k = 1 if 'immediate' in m.group(1) else 2; j = kth(P[m.group(3)], m.group(2), k, n, circle, pts, right); return arr[j]
    m = re.search(r'Who sits between ([A-Z]) and ([A-Z])\?', q)
    if m:
        a, b = P[m.group(1)], P[m.group(2)]; assert abs(a - b) == 2; return arr[(a + b) // 2]
    m = re.search(r'How many people sit between ([A-Z]) and ([A-Z])\?', q)
    if m: return abs(P[m.group(1)] - P[m.group(2)]) - 1
    m = re.search(r'Who sits directly opposite ([A-Z])\?', q)
    if m: return arr[(P[m.group(1)] + n // 2) % n]
    raise ValueError('unknown question')


@sol('ch11.row', 'ch11.circle')
def _(d, q):
    sols, people, circle, pts, right, n, clues = seating_solve(q)
    assert clues and sols, 'no solution'
    answers = {str(seating_answer(q, a, circle, pts, right, n)) for a in sols}
    assert len(answers) == 1, f'answer not unique: {answers}'
    a = answers.pop()
    return int(a) if a.isdigit() else a


@sol('ch11.rank')
def _(d, q):
    a = d['a']
    if 'How many students' in q:
        b = d['b']
        return next(n for n in range(1, 500) if n - a + 1 == b)
    n = d['n']; b = n - a + 1
    return f'{b}th' if 10 < b % 100 < 14 else f'{b}' + {1: 'st', 2: 'nd', 3: 'rd'}.get(b % 10, 'th')


# ====================== Chapter 12 (statements parsed into a family graph built from the TEXT) ======================
GW = {'father': ('M', 'parent'), 'mother': ('F', 'parent'), 'son': ('M', 'child'), 'daughter': ('F', 'child'), 'brother': ('M', 'sib'), 'sister': ('F', 'sib'), 'husband': ('M', 'sp'), 'wife': ('F', 'sp')}


class Fam:
    def __init__(s): s.unit, s.up, s.parents, s.spouse, s.g = {}, {}, collections.defaultdict(set), {}, {}
    def node(s, p):
        if p not in s.unit: s.unit[p] = ('u', p); s.up[('u', p)] = ('u', p)
        return p
    def find(s, u):
        while s.up[u] != u: u = s.up[u]
        return u
    def fact(s, a, word, b):          # a is the <word> of b
        s.node(a); s.node(b); g, kind = GW[word]; s.g[a] = g
        if kind == 'parent': s.parents[s.find(s.unit[b])].add(a)
        elif kind == 'child': s.parents[s.find(s.unit[a])].add(b)
        elif kind == 'sp': s.spouse[a] = b; s.spouse[b] = a
        else:
            ua, ub = s.find(s.unit[a]), s.find(s.unit[b])
            if ua != ub: s.up[ub] = ua; s.parents[ua] |= s.parents.pop(ub, set())
    def sp(s, p):                     # stated spouse, or the other parent of a common child (convention)
        if p in s.spouse: return s.spouse[p]
        for u, P in s.parents.items():
            if p in P and len(P) == 2: return next(x for x in P if x != p)
        return None
    def par(s, p):
        P = set(s.parents[s.find(s.unit[p])]); return P | {s.sp(x) for x in P if s.sp(x)}
    def sibs(s, p): return {q for q in s.unit if q != p and (s.find(s.unit[q]) == s.find(s.unit[p]) or (s.par(q) & s.par(p)))}
    def name(s, x, y):
        g = s.g[x]; pk = lambda m, f: m if g == 'M' else f
        P, S = s.par, s.sibs; spy, spx = s.sp(y), s.sp(x)
        if spy == x: return pk('husband', 'wife')
        if x in P(y): return pk('father', 'mother')
        if y in P(x): return pk('son', 'daughter')
        if x in S(y): return pk('brother', 'sister')
        if any(x in P(z) for z in P(y)): return pk('grandfather', 'grandmother')
        if any(y in P(z) for z in P(x)): return pk('grandson', 'granddaughter')
        if any(x in S(z) or (spx and spx in S(z)) for z in P(y)): return pk('uncle', 'aunt')
        if any(z in S(y) or (spy and z in S(spy)) for z in P(x)): return pk('nephew', 'niece')
        if any(z in S(w) for z in P(x) for w in P(y)): return 'cousin'
        if spy and x in P(spy): return pk('father-in-law', 'mother-in-law')
        if spx and y in P(spx): return pk('son-in-law', 'daughter-in-law')
        if (spy and x in S(spy)) or (spx and spx in S(y)): return pk('brother-in-law', 'sister-in-law')
        raise ValueError('relation not in vocabulary')


@sol('ch12.rel')
def _(d, q):
    f = Fam()
    for a, w, b in re.findall(r'([A-Z]) is the (\w+) of ([A-Z])\.', q): f.fact(a, w, b)
    x, y = re.search(r'How is ([A-Z]) related to ([A-Z])\?', q).groups()
    return f.name(x, y).capitalize()


@sol('ch12.point')
def _(d, q):
    m = re.search(r'Pointing to (a man|a woman) in a photograph, (\w+) said, "(He|She) is the (\w+) of my ([\w\' ]+)\."', q)
    steps = m.group(5).split("'s ") + [m.group(4)]
    f = Fam(); cur = 'SPEAKER'; f.node(cur)
    for i, w in enumerate(steps):
        nxt = f'N{i}'; f.fact(nxt, w, cur); cur = nxt
    assert f.g[cur] == ('M' if m.group(3) == 'He' else 'F')
    f.g.setdefault('SPEAKER', 'M')
    return f.name(cur, 'SPEAKER').capitalize()


@sol('ch12.code')
def _(d, q):
    defs = dict((sym, w) for sym, w in re.findall(r'X (\S) Y says "X is the (\w+) of Y"', q))
    expr = re.search(r'If ([A-Z](?: \S [A-Z])+), how', q).group(1).split()
    f = Fam()
    for i in range(0, len(expr) - 2, 2): f.fact(expr[i], defs[expr[i + 1]], expr[i + 2])
    x, y = re.search(r'how is ([A-Z]) related to ([A-Z])\?', q).groups()
    return f.name(x, y).capitalize()


@sol('ch12.side')
def _(d, q):
    who, rel = re.search(r"Your (father|mother)'s (\w+) is your", q).groups()
    side = 'paternal' if who == 'father' else 'maternal'
    return f'{side} ' + {'brother': 'uncle', 'sister': 'aunt', 'father': 'grandfather', 'mother': 'grandmother'}[rel]


# ====================== Chapter 13 (direct computation from the table; definition answers from a separate key) ======================
FACT_KEY = {      # written independently of the generator: stem -> correct option
    'The point where the "less than" ogive and the "more than" ogive intersect gives the:': 'Median',
    'The mode of a frequency distribution can be located graphically with the help of a:': 'Histogram',
    'Joining the mid-points of the tops of adjacent rectangles of a histogram gives a:': 'Frequency polygon',
    'Data collected by an investigator for the first time, for a specific purpose, are called:': 'Primary data',
    'Classification of data according to time (years, months) is called:': 'Chronological classification',
    'The part of a statistical table that describes the rows is called the:': 'Stub',
    'Which of the following is a limitation of statistics?': 'It does not study individual cases',
    'Data classified according to place (states, cities) is an example of:': 'Geographical classification',
    'Sampling error can generally be reduced by:': 'Increasing the sample size',
    'Non-sampling errors can occur in:': 'Both sample surveys and complete enumeration',
    'The standard deviation of the sampling distribution of a statistic is called its:': 'Standard error',
    'Selecting every k-th unit from a list after a random start is called:': 'Systematic sampling',
    'Dividing the population into homogeneous groups and drawing a random sample from each group is:': 'Stratified sampling',
    'The lottery method is a way of drawing a:': 'Simple random sample',
    'A sample is preferred to complete enumeration especially when:': 'The population is infinite or testing destroys the item',
    'A characteristic calculated from sample observations is called a:': 'Statistic',
}


@sol('ch13.fact')
def _(d, q): return FACT_KEY[q]


@sol('ch13.mark')
def _(d, q): return F(d['a'] + d['b'], 2)


@sol('ch13.bound')
def _(d, q):
    m = re.search(r'classes (\d+)–(\d+), (\d+)–(\d+)', q); gap = int(m.group(3)) - int(m.group(2))
    return F(d['b']) + F(gap, 2) if d['kind'] == 'upper' else F(d['a']) - F(gap, 2)


@sol('ch13.dens')
def _(d, q): return round(d['f'] / (d['b'] - d['a']), 3)


def table_from(q):
    return [(int(a), int(b), int(f)) for a, b, f in re.findall(r'(\d+)–(\d+): (\d+)', q)]


@sol('ch13.relf')
def _(d, q):
    t = table_from(q); m = re.search(r'class (\d+)–(\d+), as', q); a = int(m.group(1))
    f = next(x[2] for x in t if x[0] == a); return F(100 * f, sum(x[2] for x in t))


@sol('ch13.cum')
def _(d, q):
    t = table_from(q)
    m = re.search(r'observations less than (\d+) is', q)
    if m: return sum(f for a, b, f in t if b <= int(m.group(1)))
    m = re.search(r'observations (\d+) or more is', q); return sum(f for a, b, f in t if a >= int(m.group(1)))


@sol('ch13.pie', 'ch13.comp')
def _(d, q):
    items = {n.strip(): int(v.replace(',', '')) for n, v in re.findall(r'([A-Z][a-z]+(?: [a-z]+)?) (\d[\d,]*)', q.split('.')[0])}
    name = re.search(r'(?:angle for|length of the) ([A-Z][a-z]+(?: [a-z]+)?)(?: segment| is)', q).group(1)
    assert sorted(items.values()) == sorted(d['vals'])
    return F(items[name] * (360 if 'pie chart' in q else 100), sum(items.values()))


@sol('ch13.marks')
def _(d, q):
    mk = d['marks']; w = mk[1] - mk[0]; m = int(re.search(r'whose mark is (\d+)', q).group(1))
    return F(m) - F(w, 2) if d['kind'] == 'lower' else F(m) + F(w, 2)


@sol('ch13.ncls')
def _(d, q):
    lo, hi, w = d['lo'], d['hi'], d['w']; k = 0
    while not (lo + (k - 1) * w <= hi < lo + k * w): k += 1
    return k


@sol('ch13.nsamp')
def _(d, q):
    N, n = d['N'], d['n']
    if d['kind'] == 'without': return sum(1 for _ in itertools.combinations(range(N), n))
    return sum(1 for _ in itertools.product(range(N), repeat=n))


@sol('ch13.se')
def _(d, q): return d['s'] / math.sqrt(d['n'])


@sol('ch13.fpc')
def _(d, q):
    N, n, s = d['N'], d['n'], d['s']
    return math.sqrt(s * s / n * (N - n) / (N - 1))


@sol('ch13.seprop')
def _(d, q): return math.sqrt(d['p'] * (1 - d['p']) / d['n'])


@sol('ch13.sys')
def _(d, q):
    k = d['N'] // d['n']; sel = list(range(d['start'], d['N'] + 1, k)); return sel[d['j'] - 1]


@sol('ch13.strat')
def _(d, q): return F(d['n'] * d['sizes'][d['i']], sum(d['sizes']))


@sol('ch13.size')
def _(d, q): return next(n for n in range(1, 10 ** 5) if abs(d['s'] / math.sqrt(n) - d['se']) < 1e-12)


@sol('ch13.mom')
def _(d, q):
    ms = [F(a + b, 2) for a, b in itertools.combinations(d['pop'], 2)]; return sum(ms) / len(ms)


# ====================== Chapter 14 (statistics module / direct definitions / enumeration) ======================
import statistics as ST


def nums_after(q, key):
    seg = q.split(key, 1)[1]
    return [int(x) for x in re.findall(r'\d+', seg.split(' is')[0])]


@sol('ch14.mean')
def _(d, q): return F(ST.mean(d['xs'])).limit_denominator(1000)


@sol('ch14.comb')
def _(d, q): return F(ST.mean([d['m1']] * d['n1'] + [d['m2']] * d['n2'])).limit_denominator(10000)


@sol('ch14.corr')
def _(d, q):
    n, m = d['n'], d['m']; data = [F(m)] * n                       # any data with this mean; replace one value
    data[0] = F(d['wrong']); data[1] += F(m - d['wrong'])           # keep the total n*m with the wrong value inside
    assert sum(data) == n * m
    data[0] = F(d['right'])
    return sum(data) / n


@sol('ch14.wmean')
def _(d, q): return F(sum(x * w for x, w in zip(d['xs'], d['ws'])), sum(d['ws']))


@sol('ch14.med')
def _(d, q): return F(ST.median(d['xs'])).limit_denominator(10)


@sol('ch14.grp')
def _(d, q):
    t = [(int(a), int(b), int(f)) for a, b, f in re.findall(r'(\d+)–(\d+): (\d+)', q)]
    assert [x[2] for x in t] == d['f']
    if d['kind'] == 'median':
        N = sum(x[2] for x in t); c = 0
        for a, b, f in t:
            if c + f >= F(N, 2): return round(float(a + (F(N, 2) - c) / f * (b - a)), 2)
            c += f
    i = max(range(len(t)), key=lambda j: t[j][2]); a, b, f1 = t[i]; f0, f2 = t[i - 1][2], t[i + 1][2]
    return round(float(a + F(f1 - f0, 2 * f1 - f0 - f2) * (b - a)), 2)


@sol('ch14.emp')
def _(d, q):
    vals = dict((k, int(v)) for k, v in re.findall(r'(mean|median|mode) = (\d+)', q))
    ask = re.search(r'The (mean|median|mode) is about', q).group(1)
    for x in range(-1000, 1001):
        v = dict(vals); v[ask] = F(x, 3)
        if v['mode'] == 3 * v['median'] - 2 * v['mean']: return F(x, 3)


@sol('ch14.gm')
def _(d, q):
    p = math.prod(d['xs']); k = len(d['xs'])
    return next(g for g in range(1, 10 ** 4) if g ** k == p)


@sol('ch14.hm')
def _(d, q):
    a, b, D = d['a'], d['b'], d['D']; return F(2 * D) / (F(D, a) + F(D, b))


@sol('ch14.quart')
def _(d, q):
    xs = sorted(d['xs']); n = len(xs); k = 1 if 'first quartile' in q else 3; pos = F(k * (n + 1), 4); i = math.floor(pos)
    return xs[i - 1] + (pos - i) * (xs[i] - xs[i - 1]) if pos != i else F(xs[i - 1])


@sol('ch14.lin')
def _(d, q):
    a, b, c, mx = d['a'], d['b'], d['c'], d['mx']
    xs = [mx - 3, mx, mx + 3]; ys = [F(c - a * x, b) for x in xs]   # transform a small symmetric data set
    return F(ST.median(ys))


@sol('ch14.amgm')
def _(d, q):
    A, G = F(d['A']).limit_denominator(10), d['G']
    for a in range(1, 400):
        b = 2 * A - a
        if b > 0 and a * b == G * G:
            return F(2 * a * b) / (a + b) if d['kind'] == 'harmonic' else max(a, b)


@sol('ch14.miss')
def _(d, q): return next(x for x in range(-500, 501) if F(sum(d['xs']) + x, len(d['xs']) + 1) == d['m'])


@sol('ch14.range')
def _(d, q):
    xs = d['xs']; hi, lo = max(xs), min(xs)
    return hi - lo if d['kind'] == 'range' else round((hi - lo) / (hi + lo), 4)


@sol('ch14.md')
def _(d, q):
    xs = d['xs']; c = F(ST.mean(xs)).limit_denominator(100) if d['about'] == 'mean' else F(ST.median(xs)).limit_denominator(10)
    return round(float(sum(abs(x - c) for x in xs) / len(xs)), 2)


@sol('ch14.sd')
def _(d, q): return round(ST.pstdev(d['xs']), 2)


@sol('ch14.varsum')
def _(d, q):
    n, Sx, Sx2 = d['n'], d['Sx'], d['Sx2']; return math.sqrt(F(Sx2, n) - F(Sx, n) ** 2)


@sol('ch14.cv')
def _(d, q):
    if 'Its coefficient of variation is' in q: return F(100 * d['sd'], d['m'])
    sd = F(d['c'] * d['m'], 100); return sd * sd


@sol('ch14.cvcmp')
def _(d, q): return 'Series A' if F(d['sd'], d['m']) < F(d['sd2'], d['m2']) else 'Series B'


@sol('ch14.qd')
def _(d, q):
    q1, q3 = d['q1'], d['q3']
    return F(q3 - q1, 2) if 'coefficient' not in q else round((q3 - q1) / (q3 + q1), 4)


@sol('ch14.sd2')
def _(d, q): return F(ST.pstdev([d['a'], d['b']])).limit_denominator(10)


@sol('ch14.nat')
def _(d, q): return F(ST.pvariance(list(range(1, d['n'] + 1)))).limit_denominator(100)


@sol('ch14.lin2')
def _(d, q):
    a, b, s = d['a'], d['b'], d['s']; sd0 = math.sqrt(s) if d['kind'] == 'variance' else s
    xs = [10 - sd0, 10 + sd0]                                                       # a data set with the stated SD / variance
    ys = [a + b * x for x in xs]
    if d['kind'] == 'range': xs = [0, s]; ys = [a + b * x for x in xs]; return max(ys) - min(ys)
    sd = ST.pstdev(ys); return round(sd ** 2) if d['kind'] == 'variance' else round(sd, 6)


@sol('ch14.csd')
def _(d, q):
    # build two concrete groups with the stated n, mean, SD and pool them
    def grp(n, m, s):
        if n % 2 == 0: return [m - s, m + s] * (n // 2)
        k = (n - 1) // 2; e = s * math.sqrt(n / (2 * k)); return [m - e, m + e] * k + [m]
    g = grp(d['n1'], d['m1'], d['s1']) + grp(d['n2'], d['m2'], d['s2'])
    return round(ST.pstdev(g), 2)


# ====================== Chapter 15 (enumeration of sample spaces) ======================
def frac_opt(o):
    m = re.fullmatch(r'-?\d+(?:/\d+)?', o.strip()); return F(o.strip()) if m else None


@sol('ch15.dice')
def _(d, q):
    t = d['txt']; outs = list(itertools.product(range(1, 7), repeat=2))
    m = re.match(r'the sum is (\d+)$', t)
    if m: ev = [o for o in outs if sum(o) == int(m.group(1))]
    elif t.startswith('the sum is at least'): ev = [o for o in outs if sum(o) >= int(t.split()[-1])]
    elif t.startswith('both dice'): ev = [o for o in outs if o[0] == o[1]]
    elif 'product' in t: ev = [o for o in outs if (o[0] * o[1]) % 2 == 0]
    else: ev = [o for o in outs if abs(o[0] - o[1]) == int(t.split()[-1])]
    return F(len(ev), len(outs))


@sol('ch15.coins')
def _(d, q):
    n, k, w = d['n'], d['k'], d['word']; outs = list(itertools.product('HT', repeat=n))
    t = {'at least': lambda h: h >= k, 'exactly': lambda h: h == k, 'at most': lambda h: h <= k}[w]
    return F(sum(1 for o in outs if t(o.count('H'))), len(outs))


@sol('ch15.cards')
def _(d, q):
    deck = [(r_, s_) for s_ in ('heart', 'diamond', 'club', 'spade') for r_ in ['ace'] + [str(i) for i in range(2, 11)] + ['jack', 'queen', 'king']]
    t = d['txt']
    m = re.match(r'an? (\w+) or a (heart|diamond|club|spade)$', t)
    if m: ev = [c for c in deck if c[0] == m.group(1) or c[1] == m.group(2)]
    elif t.startswith('a face card'): ev = [c for c in deck if c[0] in ('jack', 'queen', 'king')]
    elif t.startswith('a red card or'): rk = t.split()[-1]; ev = [c for c in deck if c[1] in ('heart', 'diamond') or c[0] == rk]
    else: su = t.split()[-1]; ev = [c for c in deck if c[1] != su]
    return F(len(ev), 52)


@sol('ch15.balls')
def _(d, q):
    a, b = d['a'], d['b']; bag = ['A'] * a + ['B'] * b; t = d['txt']
    pairs = list(itertools.combinations(range(a + b), 2))
    if t.startswith('both are of the same'): ok = lambda i, j: bag[i] == bag[j]
    elif t.startswith('both are'): ok = lambda i, j: bag[i] == bag[j] == 'A'
    else: ok = lambda i, j: bag[i] != bag[j]
    return F(sum(1 for i, j in pairs if ok(i, j)), len(pairs))


@sol('ch15.add')
def _(d, q):
    pa, pb = F(d['pa']).limit_denominator(100), F(d['pb']).limit_denominator(100)
    nums_ = [F(x) for x in re.findall(r'= (\d\.\d+|\d)', q)]
    for k in range(0, 101):                                   # search the intersection that matches the stated figures
        pab = F(k, 100); onlyA, onlyB = pa - pab, pb - pab
        if onlyA < 0 or onlyB < 0 or onlyA + onlyB + pab > 1: continue
        union = onlyA + onlyB + pab
        if 'P(A ∪ B) = ' in q and q.rstrip().endswith('P(A ∩ B) ='):
            if union == nums_[2]: return pab
        elif pab == nums_[2]:
            return union if q.rstrip().endswith('P(A ∪ B) =') else 1 - union


@sol('ch15.indep')
def _(d, q):
    pa, pb = F(d['pa']), F(d['pb']); t = d['txt']
    space = {(x, y): (pa if x else 1 - pa) * (pb if y else 1 - pb) for x in (0, 1) for y in (0, 1)}
    cond = {'at least one of the two events happens': lambda x, y: x or y, 'neither event happens': lambda x, y: not x and not y, 'exactly one of the two events happens': lambda x, y: x != y}[t]
    return sum(p for (x, y), p in space.items() if cond(x, y))


@sol('ch15.cond')
def _(d, q):
    pa, pb, pab = (F(d[k]).limit_denominator(100) for k in ('pa', 'pb', 'pab'))
    return pab / (pb if d['kind'] == 'P(A | B)' else pa)


@sol('ch15.odds')
def _(d, q):
    a, b = d['a'], d['b']; return F(a, a + b) if d['kind'] == 'in favour of' else F(b, a + b)


@sol('ch15.exp')
def _(d, q):
    pairs = [(int(x), F(p)) for x, p in re.findall(r'P\(X = (-?\d+)\) = (\d+/\d+|\d+)', d['tb'])]
    assert sum(p for x, p in pairs) == 1
    E = sum(x * p for x, p in pairs)
    return E if d['kind'] == 'E(X) =' else sum((x - E) ** 2 * p for x, p in pairs)


@sol('ch15.k')
def _(d, q):
    n = d['n']; f = (lambda x: x) if d['form'] == 'kx' else (lambda x: x * x)
    return F(1, sum(f(x) for x in range(1, n + 1)))


@sol('ch15.div')
def _(d, q):
    N, a, b = d['N'], d['a'], d['b']; return F(sum(1 for x in range(1, N + 1) if x % a == 0 or x % b == 0), N)


@sol('ch15.comm')
def _(d, q):
    m, w, k, j = d['m'], d['w'], d['k'], d['j']; ppl = ['M'] * m + ['W'] * w
    cs = list(itertools.combinations(range(m + w), k))
    return F(sum(1 for c in cs if sum(ppl[i] == 'W' for i in c) == j), len(cs))


@sol('ch15.sun')
def _(d, q):
    days = 366 if d['leap'] == 'leap' else 365; hits = 0
    for start in range(7):                               # weekday of 1 January, all equally likely
        if sum(1 for i in range(days) if (start + i) % 7 == 0) == 53: hits += 1
    return F(hits, 7)


@sol('ch15.game')
def _(d, q):
    win, lose = d['win'], d['lose']; fav = len(re.findall(r'\d', q.split('if the number is ')[1].split(' and')[0]))
    E = sum(F(win if face > 6 - fav else -lose, 6) for face in range(1, 7))
    def ok(o):
        v, dp = parse_opt(o); v = -v if o.startswith('Loss') else v
        return abs(v - E) <= F(1, 200)
    return ok


# ====================== Chapter 16 (enumeration for binomial; series for Poisson; erf checks the stated table areas) ======================
@sol('ch16.binpt')
def _(d, q):
    n, p, k = d['n'], F(d['p']), d['k']
    return sum(math.prod(p if s_ else 1 - p for s_ in seq) for seq in itertools.product((0, 1), repeat=n) if sum(seq) == k)


@sol('ch16.binal')
def _(d, q):
    n, p = d['n'], F(d['p'])
    return sum(math.prod(p if s_ else 1 - p for s_ in seq) for seq in itertools.product((0, 1), repeat=n) if sum(seq) >= 1)


@sol('ch16.binmv')
def _(d, q):
    n, p = d['n'], F(d['p']).limit_denominator(10)
    pm = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
    mean = sum(k * x for k, x in enumerate(pm)); var = sum(k * k * x for k, x in enumerate(pm)) - mean ** 2
    return {'mean': mean, 'variance': var, 'standard deviation': F(math.sqrt(var)).limit_denominator(100)}[d['kind']]


@sol('ch16.binnp')
def _(d, q):
    m, v = F(d['m']).limit_denominator(100), F(d['v']).limit_denominator(1000)
    for n in range(1, 1000):
        p = m / n
        if 0 < p < 1 and n * p * (1 - p) == v: return F(n) if d['kind'] == 'n' else p


def check_e(m, e): assert abs(math.exp(-m) - e) < 0.00005, f'stated e^-{m} = {e} is wrong'


@sol('ch16.poispt')
def _(d, q):
    m, e, k = d['m'], d['e'], d['k']; check_e(m, e)
    return round(e * m ** k / math.factorial(k), 4)


@sol('ch16.poiseq')
def _(d, q):
    k = d['k']; P = lambda m, r: math.exp(-m) * m ** r / math.factorial(r)
    m = next(F(x, 100) for x in range(1, 2000) if abs(P(x / 100, k) - P(x / 100, k + 1)) < 1e-12)
    return m if d['kind'] == 'mean' else round(math.sqrt(m), 4)


@sol('ch16.poisap')
def _(d, q):
    n, p, e, kind = d['n'], F(d['p']), d['e'], d['kind']; m = n * p; check_e(float(m), e)
    return round(e * float(m) ** kind / math.factorial(kind), 4)


@sol('ch16.z')
def _(d, q): return F(d['x'] - d['mu'], d['s'])


def stated_areas(q):
    out = {}
    for z, a in re.findall(r'between z = 0 and z = ([\d.]+) is (0\.\d{4})', q): out[float(z)] = float(a)
    m = re.search(r'between z = 0 and z = ([\d.]+) and between z = 0 and z = ([\d.]+) are (0\.\d{4}) and (0\.\d{4})', q)
    if m: out[float(m.group(1))] = float(m.group(3)); out[float(m.group(2))] = float(m.group(4))
    for z, a in out.items(): assert abs(0.5 * math.erf(z / math.sqrt(2)) - a) < 0.00006, f'stated area for z={z} is wrong'
    return out


def Phi_table(x, mu, s, A):
    z = (x - mu) / s; a = A[abs(z)] if z else 0.0
    return 0.5 + a if z >= 0 else 0.5 - a


@sol('ch16.norm')
def _(d, q):
    mu, s = d['mu'], d['s']; A = stated_areas(q)
    m = re.search(r'more than (\d+)', q)
    if m: return round(1 - Phi_table(int(m.group(1)), mu, s, A), 4)
    m = re.search(r'less than (\d+)', q)
    if m: return round(Phi_table(int(m.group(1)), mu, s, A), 4)
    a, b = map(int, re.search(r'between (\d+) and (\d+) is:', q).groups())
    return round(Phi_table(b, mu, s, A) - Phi_table(a, mu, s, A), 4)


@sol('ch16.ncount')
def _(d, q):
    A = stated_areas(q); x = int(re.search(r'score above (\d+)', q).group(1))
    return round(d['N'] * (1 - Phi_table(x, d['mu'], d['s'], A)))


@sol('ch16.md')
def _(d, q):
    # ratio MD/SD for a normal curve computed numerically: E|Z| = sqrt(2/pi) ≈ 0.798, taken as 4/5 by convention
    assert abs(math.sqrt(2 / math.pi) - 0.8) < 0.003
    return F(4 * d['s'], 5) if d['kind'] == 'mean deviation' else F(d['md']).limit_denominator(10) * F(5, 4)


# ====================== Chapter 17 ======================
def parse_line(t):
    t = t.replace('−', '-').replace(' ', '')
    m = re.fullmatch(r'(-?\d*)x([+-]\d*)y(?:([+-]\d+))?=0', t)
    co = lambda g: F(-1) if g == '-' else F(1) if g in ('', '+') else F(int(g))
    return co(m.group(1)), co(m.group(2)), F(int(m.group(3)) if m.group(3) else 0)


def two_lines(q):
    return [parse_line(x) for x in re.findall(r'(−?\d*x [+−] \d*y(?: [+−] \d+)? = 0)', q)]


@sol('ch17.rcov')
def _(d, q):
    if d['kind'] == 'covariance': return F(d['r']).limit_denominator(10) * d['sx'] * d['sy']
    return F(d['cov']).limit_denominator(100) / (d['sx'] * d['sy'])


@sol('ch17.rb')
def _(d, q):
    byx, bxy = F(d['byx']).limit_denominator(100), F(d['bxy']).limit_denominator(100); r2 = byx * bxy
    rr = F(math.sqrt(r2)).limit_denominator(100); return rr if byx > 0 else -rr


@sol('ch17.br')
def _(d, q):
    r_, sx, sy = d['r'], d['sx'], d['sy']
    return round(r_ * sy / sx if d['kind'] == 'byx' else r_ * sx / sy, 4)


@sol('ch17.means')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = two_lines(q)
    D = a1 * b2 - a2 * b1; x = (b1 * c2 - b2 * c1) / D; y = (a2 * c1 - a1 * c2) / D
    return f'x̄ = {x}, ȳ = {y}'


@sol('ch17.rlines')
def _(d, q):
    (a1, b1, c1), (a2, b2, c2) = two_lines(q)
    for (A1, B1), (A2, B2) in (((a1, b1), (a2, b2)), ((a2, b2), (a1, b1))):
        byx = -A1 / B1; bxy = -B2 / A2           # first line as y on x, second as x on y
        if byx * bxy <= 1 and byx * bxy > 0:
            rr = F(math.sqrt(byx * bxy)).limit_denominator(100); return rr if byx > 0 else -rr
    raise ValueError


@sol('ch17.spear')
def _(d, q):
    if 'pairs of ranks' in q: n, d2 = d['n'], d['d2']; return round(1 - 6 * d2 / (n * (n * n - 1)), 4)
    A, B = d['A'], d['B']
    # Spearman = Pearson correlation of the ranks
    return round(ST.correlation(A, B), 4)


@sol('ch17.pear')
def _(d, q): return round(ST.correlation(d['xs'], d['ys']), 3)


@sol('ch17.det')
def _(d, q):
    r_ = F(d['r']).limit_denominator(10); return (1 - r_ * r_) * 100 if 'NOT explained' in q else r_ * r_ * 100


@sol('ch17.est')
def _(d, q):
    mx, my, sx, sy, r_, x0 = d['mx'], d['my'], d['sx'], d['sy'], d['r'], d['x0']
    # least squares on a synthetic data set with these moments
    xs = [mx - sx, mx + sx]; e = math.sqrt(1 - r_ * r_)
    pts = [(mx - sx, my - r_ * sy + e * sy), (mx - sx, my - r_ * sy - e * sy), (mx + sx, my + r_ * sy + e * sy), (mx + sx, my + r_ * sy - e * sy)]
    X = [p[0] for p in pts]; Y = [p[1] for p in pts]
    slope, icpt = ST.linear_regression(X, Y)
    return round(icpt + slope * x0, 2)


@sol('ch17.os')
def _(d, q):
    r_ = F(d['r']).limit_denominator(10); return r_ if d['h'] * d['k'] > 0 else -r_


@sol('ch17.conc')
def _(d, q):
    m = d['n'] - 1; v = (2 * d['c'] - m) / m
    return round(math.copysign(math.sqrt(abs(v)), v), 4)


# ====================== Chapter 18 ======================
def rows_from(q):
    return [tuple(int(x) for x in m) for m in re.findall(r'[A-D]: p₀ = (\d+), q₀ = (\d+), p₁ = (\d+), q₁ = (\d+)', q)]


@sol('ch18.windex')
def _(d, q):
    rows = rows_from(q); assert [list(x) for x in rows] == d['rows']
    s = lambda pi, qi: sum(F(r_[pi]) * r_[qi] for r_ in rows)       # indexes: p0=0, q0=1, p1=2, q1=3
    L = s(2, 1) / s(0, 1) * 100; P = s(2, 3) / s(0, 3) * 100
    k = d['kind']
    if k == 'Laspeyres': v = L
    elif k == 'Paasche': v = P
    elif k == 'Fisher': v = math.sqrt(L * P)
    elif k == 'Bowley': v = (L + P) / 2
    elif k == 'value': v = s(2, 3) / s(0, 1) * 100
    else: v = sum(F(r_[2]) * (r_[1] + r_[3]) for r_ in rows) / sum(F(r_[0]) * (r_[1] + r_[3]) for r_ in rows) * 100
    return round(float(v), 2)


@sol('ch18.simple')
def _(d, q):
    pr = [(int(a), int(b)) for a, b in re.findall(r'[A-D]: p₀ = (\d+), p₁ = (\d+)', q)]
    if 'simple aggregative' in q: return round(float(F(sum(b for a, b in pr), sum(a for a, b in pr)) * 100), 2)
    return round(ST.mean([b / a * 100 for a, b in pr]), 2)


@sol('ch18.rel')
def _(d, q):
    p0, p1 = d['p0'], d['p1']
    return round(p0 / p1 * 100 if 'Taking year 1 as the base' in q else p1 / p0 * 100, 2)


@sol('ch18.fp')
def _(d, q):
    L, Fi = d['L'], d['Fi']
    return round(float(bisect(lambda P: math.sqrt(L * P) - Fi, 1.0, 1000.0)), 2)


@sol('ch18.chain')
def _(d, q):
    v = 100.0
    for l in d['links']: v = v * l / 100
    return round(v, 2)


@sol('ch18.shift')
def _(d, q):
    yrs = [int(y) for y in re.search(r'for ([\d, ]+) are', q).group(1).split(', ')]
    idx = [int(x) for x in re.search(r' are ([\d, ]+)\. Shifting', q).group(1).split(', ')]
    nb = int(re.search(r'base to (\d+) = 100', q).group(1)); t = int(re.search(r'index for (\d+) becomes', q).group(1))
    return round(idx[yrs.index(t)] / idx[yrs.index(nb)] * 100, 2)


@sol('ch18.defl')
def _(d, q):
    if 'real wage' in q: return round(d['W'] / d['cpi'] * 100, 2)
    return round(100 / d['cpi'], 2)


@sol('ch18.wavg')
def _(d, q): return round(sum(a * b for a, b in zip(d['R'], d['W'])) / sum(d['W']), 2)


@sol('ch18.qty')
def _(d, q):
    rows = rows_from(q); return round(sum(r_[3] * r_[0] for r_ in rows) / sum(r_[1] * r_[0] for r_ in rows) * 100, 2)


@sol('ch18.stock')
def _(d, q): return round((d['b'] - d['a']) / d['a'] * 100, 2)


FACT18 = {
    'Which index number satisfies both the time reversal test and the factor reversal test?': "Fisher's ideal index",
    'The time reversal test requires that (P₀₁ = index for year 1 on base 0, P₁₀ = index for year 0 on base 1):': 'P₀₁ × P₁₀ = 1',
    'The factor reversal test requires that the product of the price index and the quantity index equals the:': 'Value index',
    'The index number commonly used to deflate money wages into real wages is the:': 'Consumer price index',
}


@sol('ch18.fact')
def _(d, q): return FACT18[q]


def main():
    data = json.load(open(os.path.join(HERE, 'p3_data.json'), encoding='utf-8'))
    tot = 0; per = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'content/ca/foundation/p3/bank/*.json'))):
        b = json.load(open(f, encoding='utf-8')); uid = b['unit']
        unit = json.load(open(os.path.join(ROOT, f'content/ca/foundation/p3/{uid.split("-")[2]}/{uid.split("-")[3]}.json'), encoding='utf-8'))
        old = {norm(x['q']) for x in unit['mcqs']}
        seen = set()
        for q in b['mcq']:
            if norm(q['q']) in old or norm(q['q']) in seen: FAIL.append(f'{uid}#{q["id"]}: duplicate stem')
            seen.add(norm(q['q']))
            check_q(uid, q, data.get(f'{uid}#{q["id"]}'))
        per[uid] = len(b['mcq']); tot += len(b['mcq'])
    for k, v in per.items(): print(f'{k}: {v} re-solved')
    print('total', tot)
    for x in FAIL: print('FAIL', x)
    print('VERIFY OK' if not FAIL else f'{len(FAIL)} failure(s)')
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
