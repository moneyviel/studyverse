"""Practice generators — Mathematics Unit 5: Binomial Theorem. check() re-solves every item by expanding the power term by
term with exact fractions, by computing remainders with Python's modular power, and by evaluating coefficient sums
directly from the coefficients."""
import math, itertools
from fractions import Fraction as F
from common import mcq, fr
C = math.comb
def need(x):
    if not x: raise AssertionError('retry')
def expand(terms, n):
    out = {F(0): F(1)}
    for _ in range(n):
        nxt = {}
        for e1, c1 in out.items():
            for c2, e2 in terms: nxt[e1 + F(e2)] = nxt.get(e1 + F(e2), 0) + c1 * F(c2)
        out = nxt
    return out
def mul(A, B):
    out = {}
    for e1, c1 in A.items():
        for e2, c2 in B.items(): out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
    return out
def xp(c, e, first=False):   # coefficient·x^e as text
    cs = fr(c); e = F(e)
    base = '' if e == 0 else 'x' if e == 1 else f'x^{{{fr(e)}}}'
    if e < 0: base = f'\\f{{1}}{{x{"" if e == -1 else "^{" + fr(-e) + "}"}}}'
    if base and abs(c) == 1: cs = '' if c > 0 else '−'
    elif base and F(c).denominator != 1: cs = fr(c)
    return cs + base
def bracket(a, p, b, q):
    t2 = xp(abs(b), q); return f'({xp(a, p)} {"+" if b > 0 else "−"} {t2})'

def g_term(rng):
    t = rng.choice(['t_const', 't_coef', 't_prod', 't_mid', 't_ratio'])
    if t == 't_const':
        p, q = rng.choice([(1, 1), (1, 2), (2, 1), (2, 3), (3, 1), (1, 3), (3, 2), (2, 2)]); n = rng.randint(3, 12); need(n * p % (p + q) == 0)
        a, b = rng.choice([1, 2, 3]), rng.choice([1, -1, 2, -2, 3, -3, F(1, 2), F(-1, 3)]); val = expand([(a, p), (b, -q)], n)[F(0)]
        need(val.denominator == 1 and abs(val) < 10 ** 7)
        return dict(q=f'The term independent of x in the expansion of {bracket(a, p, b, -q)}^{{{n}}} is ____.', o=None, a=int(val),
                    sol=[f'T_{{r+1}} has x^{{{p}({n} − r) − {q}r}}: set the power to 0 → r = {n * p // (p + q)}.', f'Value = {int(val)}.'], p=dict(t=t, a=a, p=p, b=[b.numerator, b.denominator] if isinstance(b, F) else [b, 1], q=q, n=n))
    if t == 't_coef':
        p, q = rng.choice([(1, 1), (2, 1), (1, 2), (2, 3), (3, 1)]); n = rng.randint(4, 10); a, b = rng.choice([1, 2, 3]), rng.choice([1, -1, 2, -2, 3])
        E = expand([(a, p), (b, -q)], n); k = rng.choice([e for e in E if e != 0 and E[e] != 0]); val = E[k]; need(val.denominator == 1 and abs(val) < 10 ** 8)
        return dict(q=f'The coefficient of {xp(1, k)} in the expansion of {bracket(a, p, b, -q)}^{{{n}}} is ____.', o=None, a=int(val),
                    sol=[f'Power of x in T_{{r+1}}: {p}({n} − r) − {q}r. Set it equal to {fr(k)} and solve for r.', f'Coefficient = {int(val)}.'], p=dict(t=t, a=a, p=p, b=[b, 1], q=q, n=n, k=[k.numerator, k.denominator]))
    if t == 't_prod':
        c0, c1, c2 = rng.randint(1, 4), rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([0, 1, -1, 2]); d, n, k = rng.choice([-2, -1, 1, 2, 3]), rng.randint(5, 12), rng.randint(2, 4)
        val = mul({F(0): c0, F(1): c1, F(2): c2}, expand([(1, 0), (d, 1)], n)).get(F(k), 0); need(val and abs(val) < 10 ** 9)
        poly = ' '.join(x for x in [str(c0), ('+ ' if c1 > 0 else '− ') + xp(abs(c1), 1), ('+ ' if c2 > 0 else '− ') + xp(abs(c2), 2) if c2 else ''] if x)
        return dict(q=f'The coefficient of x^{{{k}}} in ({poly})(1 {"+" if d > 0 else "−"} {xp(abs(d), 1)})^{{{n}}} is ____.', o=None, a=int(val),
                    sol=['Multiply each term of the first bracket by the matching term of the binomial: c_{0}·[x^{k}] + c_{1}·[x^{k−1}] + c_{2}·[x^{k−2}].', f'= {int(val)}.'], p=dict(t=t, c=[c0, c1, c2], d=d, n=n, k=k))
    if t == 't_mid':
        m, a = rng.randint(2, 6), rng.choice([1, 2, 3, -1, -2]); n = 2 * m; val = expand([(1, 1), (a, -1)], n)[F(0)]
        return dict(q=f'The middle term of the expansion of {bracket(1, 1, a, -1)}^{{{n}}} is ____.', o=None, a=int(val),
                    sol=[f'{n + 1} terms → the middle one is T_{{{m + 1}}} = C({n}, {m})(x)^{{{m}}}({fr(a)}/x)^{{{m}}}.', f'= {int(val)}.'], p=dict(t=t, a=a, n=n))
    n, r = rng.randint(6, 20), rng.randint(1, 6); need(r + 2 <= n)
    a, b, c = C(n, r), C(n, r + 1), C(n, r + 2); g = math.gcd(math.gcd(a, b), c)
    return dict(q=f'Three consecutive coefficients in the expansion of (1 + x)^{{n}} are in the ratio {a // g} : {b // g} : {c // g}. Then n = ____.', o=None, a=n,
                sol=['C(n, r + 1)/C(n, r) = \\f{n − r}{r + 1}: two such ratios give two equations in n and r.', f'n = {n} (r = {r}).'], p=dict(t='t_ratio', rt=[a // g, b // g, c // g]))

def g_coef(rng):
    t = rng.choice(['c_ap', 'c_sum', 'c_sq', 'c_big', 'c_alt'])
    if t == 'c_ap':
        r = rng.randint(2, 8); ns = [n for n in range(r + 1, 80) if 2 * C(n, r) == C(n, r - 1) + C(n, r + 1)]; need(ns); ask = rng.choice(['max', 'sum'])
        val = max(ns) if ask == 'max' else sum(ns)
        return dict(q=f'The coefficients of x^{{{r - 1}}}, x^{{{r}}} and x^{{{r + 1}}} in (1 + x)^{{n}} are in A.P. The {"largest possible n" if ask == "max" else "sum of all possible values of n"} is ____.', o=None, a=val,
                    sol=['2C(n, r) = C(n, r − 1) + C(n, r + 1) → n^{2} − (4r + 1)n + 4r^{2} − 2 = 0.', f'n ∈ {{{", ".join(map(str, ns))}}} → {val}.'], p=dict(t=t, r=r, ask=ask))
    if t == 'c_sum':
        n = rng.randint(4, 14); kind = rng.choice(['r', 'r2', 'inv', 'odd', 'rr1'])
        val = {'r': sum(r * C(n, r) for r in range(n + 1)), 'r2': sum(r * r * C(n, r) for r in range(n + 1)), 'inv': sum(F(C(n, r), r + 1) for r in range(n + 1)),
               'odd': sum(C(n, r) for r in range(1, n + 1, 2)), 'rr1': sum(r * (r - 1) * C(n, r) for r in range(n + 1))}[kind]
        txt = {'r': 'Σ_{r=0}^{n} r·C(n, r)', 'r2': 'Σ_{r=0}^{n} r^{2}·C(n, r)', 'inv': 'Σ_{r=0}^{n} \\f{C(n, r)}{r + 1}', 'odd': 'C(n, 1) + C(n, 3) + C(n, 5) + …', 'rr1': 'Σ_{r=0}^{n} r(r − 1)·C(n, r)'}[kind]
        rule = {'r': 'n·2^{n−1}', 'r2': 'n(n + 1)2^{n−2}', 'inv': '\\f{2^{n+1} − 1}{n + 1}', 'odd': '2^{n−1}', 'rr1': 'n(n − 1)2^{n−2}'}[kind]
        if kind == 'inv':
            right = fr(val); o, a = mcq(rng, right, [fr(val + 1), fr(val * 2), fr(F(2 ** n, n + 1)), fr(F(2 ** (n + 1), n + 1))])
            return dict(q=f'For n = {n}, {txt} =', o=o, a=a, sol=[f'Use {rule}.', f'= {right}.'], p=dict(t=t, n=n, kind=kind))
        return dict(q=f'For n = {n}, the value of {txt} is ____.', o=None, a=int(val), sol=[f'Use {rule}.', f'= {int(val)}.'], p=dict(t=t, n=n, kind=kind))
    if t == 'c_sq':
        n = rng.randint(3, 12); k = rng.randint(0, 3); val = sum(C(n, r) * C(n, r + k) for r in range(n + 1))
        return dict(q=f'The value of Σ_{{r=0}}^{{{n - k}}} C({n}, r)·C({n}, r + {k}) is ____.'.replace(' + 0)', ')'), o=None, a=val,
                    sol=['C(n, r)C(n, r + k) = C(n, r)C(n, n − r − k): compare coefficients of x^{n−k} in (1 + x)^{n}(1 + x)^{n}.', f'= C({2 * n}, {n - k}) = {val}.'], p=dict(t=t, n=n, k=k))
    if t == 'c_big':
        a, b, n = rng.randint(1, 3), rng.randint(1, 3), rng.randint(4, 10); need(a != b or a == 1)
        co = [C(n, r) * a ** (n - r) * b ** r for r in range(n + 1)]; val = max(co)
        return dict(q=f'The greatest coefficient in the expansion of ({a} + {b}x)^{{{n}}} is ____.'.replace('(1 + 1x)', '(1 + x)').replace(' 1x)', ' x)'), o=None, a=val,
                    sol=['Compare consecutive coefficients: T_{r+1}/T_{r} = \\f{n − r + 1}{r} · \\f{b}{a}; it is the largest where this ratio drops below 1.', f'Greatest = {val}.'], p=dict(t=t, a=a, b=b, n=n))
    n = rng.randint(4, 12); k = rng.randint(1, n - 1); val = sum((-1) ** r * C(n, r) for r in range(k + 1))
    return dict(q=f'The value of C({n}, 0) − C({n}, 1) + C({n}, 2) − … + (−1)^{{{k}}}C({n}, {k}) is ____.', o=None, a=val,
                sol=['Partial alternating sums telescope: Σ_{r=0}^{k}(−1)^{r}C(n, r) = (−1)^{k}C(n − 1, k).', f'= {val}.'], p=dict(t='c_alt', n=n, k=k))

def g_rat(rng):
    t = rng.choice(['r_cnt', 'r_sum', 'r_sum', 'r_irr'])
    if t == 'r_cnt':
        a, p, b, q = rng.choice([2, 3, 5, 7]), rng.choice([2, 3, 4, 5, 6, 8]), rng.choice([3, 5, 7, 11]), rng.choice([2, 3, 4, 5, 6]); need(a != b)
        n = rng.choice(range(10, 400)); val = sum(1 for r in range(n + 1) if (n - r) % p == 0 and r % q == 0); need(val)
        return dict(q=f'The number of rational terms in the expansion of ({a}^{{1/{p}}} + {b}^{{1/{q}}})^{{{n}}} is ____.', o=None, a=val,
                    sol=[f'T_{{r+1}} = C({n}, r){a}^{{({n} − r)/{p}}}{b}^{{r/{q}}}: need {p} | ({n} − r) and {q} | r.', f'Count such r from 0 to {n} → {val}.'], p=dict(t=t, a=a, pp=p, b=b, q=q, n=n))
    if t == 'r_sum':
        b, a, n = rng.randint(1, 4), rng.choice([2, 3, 5, 6, 7]), rng.randint(3, 9); val = sum(C(n, r) * b ** (n - r) * a ** (r // 2) for r in range(0, n + 1, 2)); need(val < 10 ** 8)
        return dict(q=f'The sum of all rational terms in the expansion of ({b} + √{{{a}}})^{{{n}}} is ____.', o=None, a=val,
                    sol=['Keep the terms with an even power of the root.', f'= \\f{{({b} + √{{{a}}})^{{{n}}} + ({b} − √{{{a}}})^{{{n}}}}}{{2}} = {val}.'], p=dict(t=t, a=a, b=b, n=n))
    a, p, b, q = rng.choice([2, 3, 5]), rng.choice([2, 3, 4, 5]), rng.choice([3, 5, 7]), rng.choice([2, 3, 4]); need(a != b); n = rng.randint(6, 40)
    rat = sum(1 for r in range(n + 1) if (n - r) % p == 0 and r % q == 0); val = n + 1 - rat
    return dict(q=f'The number of irrational terms in the expansion of ({a}^{{1/{p}}} + {b}^{{1/{q}}})^{{{n}}} is ____.', o=None, a=val,
                sol=[f'{n + 1} terms in all; count the rational ones ({p} | ({n} − r), {q} | r) and subtract.', f'{n + 1} − {rat} = {val}.'], p=dict(t='r_irr', a=a, pp=p, b=b, q=q, n=n))

def g_rem(rng):
    t = rng.choice(['m_pow', 'm_pow', 'm_last', 'm_near'])
    if t == 'm_pow':
        m = rng.choice([5, 7, 9, 11, 13, 17, 19, 21, 23, 25, 31]); a = rng.randint(2, 600); need(a % m); n = rng.randint(20, 3000); val = pow(a, n, m)
        return dict(q=f'The remainder when {a}^{{{n}}} is divided by {m} is ____.', o=None, a=val,
                    sol=[f'Reduce the base: {a} ≡ {a % m} (mod {m}); find a small power that is ±1, then split the exponent.', f'Remainder {val}.'], p=dict(t=t, a=a, n=n, m=m))
    if t == 'm_last':
        a, n = rng.choice([3, 7, 9, 11, 13, 17, 19, 21, 23, 29, 31, 101]), rng.randint(10, 999); val = pow(a, n, 100)
        return dict(q=f'The last two digits of {a}^{{{n}}} form the number ____.', o=None, a=val,
                    sol=['Work mod 100: write the base as (multiple of 10 ± small) or find the cycle of its powers.', f'{a}^{{{n}}} ≡ {val} (mod 100).'], p=dict(t=t, a=a, n=n))
    m = rng.choice([7, 8, 9, 13, 16, 17, 25, 49, 64]); k = rng.randint(1, 4); s = rng.choice([1, -1]); a = k * m + s; n = rng.randint(5, 200); c = rng.randint(0, m - 1)
    val = (pow(a, n, m) + c) % m
    return dict(q=f'The remainder when {a}^{{{n}}} + {c} is divided by {m} is ____.'.replace(' + 0 is', ' is'), o=None, a=val,
                sol=[f'{a} = {k * m} {"+" if s > 0 else "−"} 1, so {a}^{{{n}}} ≡ ({"1" if s > 0 else "−1"})^{{{n}}} (mod {m}).', f'Remainder {val}.'], p=dict(t='m_near', a=a, n=n, m=m, c=c))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(term=g_term, coef=g_coef, rat=g_rat, rem=g_rem).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 't_const': return R == expand([(p['a'], p['p']), (F(*p['b']), -p['q'])], p['n'])[F(0)]
    if t == 't_coef': return R == expand([(p['a'], p['p']), (F(*p['b']), -p['q'])], p['n'])[F(*p['k'])]
    if t == 't_prod':
        c0, c1, c2 = p['c']; poly = [c0, c1, c2]; tot = 0
        for j in range(3):
            if p['k'] - j >= 0: tot += poly[j] * C(p['n'], p['k'] - j) * p['d'] ** (p['k'] - j)
        return R == tot
    if t == 't_mid':
        E = sorted(expand([(1, 1), (p['a'], -1)], p['n']).items()); return R == E[len(E) // 2][1]
    if t == 't_ratio':
        a, b, c = p['rt']; return R == next(n for n in range(2, 200) for r in range(n - 1) if C(n, r) * b == C(n, r + 1) * a and C(n, r + 1) * c == C(n, r + 2) * b)
    if t == 'c_ap':
        ns = []
        for n in range(p['r'] + 1, 120):
            co = [C(n, k) for k in range(n + 1)]
            if 2 * co[p['r']] == co[p['r'] - 1] + co[p['r'] + 1]: ns.append(n)
        return R == (max(ns) if p['ask'] == 'max' else sum(ns))
    if t == 'c_sum':
        n = p['n']; co = expand([(1, 0), (1, 1)], n); cs = [co[F(r)] for r in range(n + 1)]
        v = {'r': sum(r * c for r, c in enumerate(cs)), 'r2': sum(r * r * c for r, c in enumerate(cs)), 'inv': sum(c / (r + 1) for r, c in enumerate(cs)), 'odd': sum(c for r, c in enumerate(cs) if r % 2), 'rr1': sum(r * (r - 1) * c for r, c in enumerate(cs))}[p['kind']]
        return (F(R.replace('\\f{', '').replace('}{', '/').replace('}', '').replace('−', '-')) if isinstance(R, str) else R) == v
    if t == 'c_sq':
        n, k = p['n'], p['k']; co = [C(n, r) for r in range(n + 1)] + [0] * 5; return R == sum(co[r] * co[r + k] for r in range(n + 1))
    if t == 'c_big': return R == max(expand([(p['a'], 0), (p['b'], 1)], p['n']).values())
    if t == 'c_alt': return R == sum((-1) ** r * C(p['n'], r) for r in range(p['k'] + 1))
    if t in ('r_cnt', 'r_irr'):
        rat = 0
        for r in range(p['n'] + 1):
            e1, e2 = F(p['n'] - r, p['pp']), F(r, p['q'])
            rat += e1.denominator == 1 and e2.denominator == 1
        return R == (rat if t == 'r_cnt' else p['n'] + 1 - rat)
    if t == 'r_sum':
        n, a, b = p['n'], p['a'], p['b']; x, y = 1, 0   # (b + √a)^n = x + y√a
        for _ in range(n): x, y = b * x + a * y, x + b * y
        return R == x
    if t == 'm_pow': return R == pow(p['a'], p['n'], p['m'])
    if t == 'm_last': return R == p['a'] ** p['n'] % 100
    if t == 'm_near': return R == (p['a'] ** p['n'] + p['c']) % p['m']
    raise KeyError(t)
