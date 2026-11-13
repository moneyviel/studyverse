"""Practice generators — Mathematics Unit 8: Integral Calculus. check() re-solves every item numerically: definite
integrals and areas by the midpoint rule on a fine grid (areas slice by slice from the region's own inequalities),
antiderivatives by differentiating the claimed answer and comparing with the integrand."""
import math
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
def integ(f, a, b, n=60000):
    h = (b - a) / n; return h * sum(f(a + (i + 0.5) * h) for i in range(n))
def d1(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
PI = math.pi
def tofr(s):
    s = s.replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-')
    v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def poly_txt(cs, var='x'):   # cs: highest power first
    n = len(cs) - 1; out = []
    for i, c in enumerate(cs):
        k = n - i
        if c == 0: continue
        mag = abs(c); body = ('' if mag == 1 and k else fr(mag)) + (var if k == 1 else f'{var}^{{{k}}}' if k > 1 else '')
        out.append(('− ' if c < 0 else '+ ') + body)
    s = ' '.join(out) or '0'; return s[2:] if s.startswith('+ ') else '−' + s[2:]

def g_area(rng):
    t = rng.choice(['ar_line', 'ar_line', 'ar_pp', 'ar_sqrt', 'ar_abs', 'ar_parab', 'ar_trig', 'ar_cub', 'ar_cap'])
    if t == 'ar_cub':
        k = rng.randint(1, 9)
        return dict(q=f'If A is the total area enclosed by y = x^{{3}} and y = {k * k}x, then 2A = ____.', o=None, a=k ** 4, sol=[f'They meet at x = 0, ±{k}; the two loops are equal.', f'A = 2∫_{{0}}^{{{k}}}({k * k}x − x^{{3}})dx = \\f{{{k}^{{4}}}}{{2}} → 2A = {k ** 4}.'], p=dict(t=t, k=k))
    if t == 'ar_cap':
        n, a = rng.randint(1, 9), rng.randint(1, 3); val = F(4 * n ** 3, 3 * math.isqrt(a * a))
        return dict(q=f'If A is the area enclosed by y = {poly_txt([a, 0, 0])} and y = {a * n * n}, then 3A = ____.', o=None, a=int(3 * val) if (3 * val).denominator == 1 else None, sol=[f'They meet at x = ±{n}.', f'A = ∫_{{−{n}}}^{{{n}}}({a * n * n} − {a}x^{{2}})dx = \\f{{4·{a}·{n}^{{3}}}}{{3}} → 3A = {4 * a * n ** 3}.'], p=dict(t=t, n=n, a=a)) if False else dict(q=f'If A is the area enclosed by y = {poly_txt([a, 0, 0])} and y = {a * n * n}, then 3A = ____.', o=None, a=4 * a * n ** 3, sol=[f'They meet at x = ±{n}.', f'A = ∫_{{−{n}}}^{{{n}}}({a * n * n} − {a}x^{{2}})dx = \\f{{4·{a}·{n}^{{3}}}}{{3}} → 3A = {4 * a * n ** 3}.'.replace('4·1·', '4·')], p=dict(t=t, n=n, a=a))
    if t == 'ar_line':
        r1, r2 = sorted(rng.sample(range(-6, 9), 2)); a = rng.choice([1, 1, 2, 3]); m, c = a * (r1 + r2), -a * r1 * r2   # a x² = m x + c at r1, r2
        val = F(a * (r2 - r1) ** 3, 6)
        return dict(q=f'If A is the area enclosed by y = {poly_txt([a, 0, 0])} and y = {poly_txt([m, c])}, then 6A = ____.', o=None, a=int(6 * val),
                    sol=[f'They meet at x = {r1} and x = {r2}.', f'A = ∫(line − parabola)dx = \\f{{{a}({r2} − ({r1}))^{{3}}}}{{6}} → 6A = {int(6 * val)}.'.replace('(−', '(−')], p=dict(t=t, a=a, m=m, c=c, r=[r1, r2]))
    if t == 'ar_pp':
        b, c = rng.randint(-10, 10), rng.randint(-10, 10); need(c != b); k = abs(c - b); X = F(c - b, 2)
        val = F(k ** 3, 24) * 2 / 2 * 2 / 2 * 1   # ∫_0^X |2x^2 − (c − b)x| = |c − b|^3/24
        val = abs(F(c - b) ** 3) / 24
        need((24 * val).denominator == 1)
        return dict(q=f'If A is the area enclosed by the parabolas y = {poly_txt([1, b, 0])} and y = {poly_txt([-1, c, 0])}, then 24A = ____.', o=None, a=int(24 * val),
                    sol=[f'They meet where 2x^{{2}} = {c - b}x: x = 0 and {fr(X)}.', f'A = ∫|{c - b}x − 2x^{{2}}|dx = \\f{{|{c - b}|^{{3}}}}{{24}} → 24A = {int(24 * val)}.'], p=dict(t=t, b=b, c=c))
    if t == 'ar_sqrt':
        k, m = rng.randint(1, 5), rng.randint(1, 5); val = F(k ** 4 * m ** 3, 6)
        return dict(q=f'If A is the area enclosed by y = {"" if k == 1 else k}√{{x}} and y = {"x" if m == 1 else f"\\\\f{{x}}{{{m}}}"}, then 6A = ____.', o=None, a=int(6 * val),
                    sol=[f'They meet at x = 0 and x = {(k * m) ** 2}.', f'A = ∫({k}√{{x}} − \\f{{x}}{{{m}}})dx = {fr(val)} → 6A = {int(6 * val)}.'], p=dict(t=t, k=k, m=m))
    if t == 'ar_abs':
        a, k = rng.randint(-3, 3), rng.randint(1, 8); ask = rng.choice(['abs', 'diam'])
        if ask == 'abs':
            return dict(q=f'The area enclosed by y = |x − ({a})| and y = {k} is ____.'.replace('− (-', '+ (').replace('(', '').replace(')', '') if a else f'The area enclosed by y = |x| and y = {k} is ____.', o=None, a=k * k,
                        sol=['A triangle with height k and base 2k.', f'Area = k^{{2}} = {k * k}.'], p=dict(t=t, a=a, k=k, ask=ask))
        return dict(q=f'The area of the region |x| + |y| ≤ {k} is ____.', o=None, a=2 * k * k, sol=['A square with diagonals 2k.', f'Area = \\f{{(2k)^{{2}}}}{{2}} = {2 * k * k}.'], p=dict(t=t, k=k, ask=ask))
    if t == 'ar_parab':
        a, b = rng.choice([1, 4, 9, 16, 25]), rng.choice([1, 4, 9, 16, 25, 36]); val = F(8, 3) * math.isqrt(a) * math.isqrt(b) ** 3
        return dict(q=f'If A is the area enclosed by y^{{2}} = {4 * a}x and the line x = {b}, then 3A = ____.', o=None, a=int(3 * val),
                    sol=['A = 2∫_{0}^{b}2√{a}√{x}dx = \\f{8}{3}√{a}b^{3/2}.', f'3A = {int(3 * val)}.'], p=dict(t=t, a=a, b=b))
    n, ask = rng.randint(1, 6), rng.choice(['sin', 'abs'])
    if ask == 'sin':
        return dict(q=f'The area between y = sin x and the x-axis from x = 0 to x = {n}π is ____.', o=None, a=2 * n, sol=['Each arch of sin x has area 2.', f'{n} arches → {2 * n}.'], p=dict(t=t, n=n, ask=ask))
    return dict(q=f'The area between y = |cos x| and the x-axis from x = 0 to x = {n}π is ____.', o=None, a=2 * n, sol=['Each half-period of |cos x| has area 2.', f'{n} of them → {2 * n}.'], p=dict(t=t, n=n, ask=ask))

def g_def(rng):
    t = rng.choice(['dp_poly', 'dp_king', 'dp_odd', 'dp_wallis', 'dp_exp', 'dp_abs'])
    if t == 'dp_poly':
        cs = [rng.randint(-3, 4) for _ in range(3)]; a, b = sorted(rng.sample(range(-2, 4), 2))
        val = sum(F(c, 3 - i) * (F(b) ** (3 - i) - F(a) ** (3 - i)) for i, c in enumerate(cs)); need(val)
        return dict(q=f'If I = ∫_{{{a}}}^{{{b}}}({poly_txt(cs)})dx, then 6I = ____.', o=None, a=int(6 * val),
                    sol=['Integrate term by term: ∫x^{n} = \\f{x^{n+1}}{n + 1}.', f'I = {fr(val)} → 6I = {int(6 * val)}.'], p=dict(t=t, cs=cs, a=a, b=b))
    if t == 'dp_king':
        a = rng.randint(1, 12); kind = rng.choice(['sqrt', 'pow', 'trig'])
        if kind == 'trig':
            n = rng.randint(1, 9); right = '\\f{π}{4}'; o, an = mcq(rng, right, ['\\f{π}{2}', '1', '\\f{π}{8}', '0'])
            return dict(q=f'∫_{{0}}^{{π/2}}\\f{{sin^{{{n}}}x}}{{sin^{{{n}}}x + cos^{{{n}}}x}}dx =', o=o, a=an, sol=['x → \\f{π}{2} − x swaps sin and cos: 2I = ∫_{0}^{π/2}1 dx.', 'I = \\f{π}{4}.'], p=dict(t=t, kind=kind, n=n))
        n = rng.randint(2, 7); txt = f'\\f{{√{{x}}}}{{√{{x}} + √{{{a} − x}}}}' if kind == 'sqrt' else f'\\f{{x^{{{n}}}}}{{x^{{{n}}} + ({a} − x)^{{{n}}}}}'
        val = F(a, 2); o, an = mcq(rng, fr(val), [fr(a), fr(F(a, 4)), fr(val + 1), fr(F(a, 3))])
        return dict(q=f'∫_{{0}}^{{{a}}}{txt}dx =', o=o, a=an, sol=[f'x → {a} − x gives the partner fraction; adding, 2I = ∫_{{0}}^{{{a}}}1 dx = {a}.', f'I = {fr(val)}.'], p=dict(t=t, kind=kind, a=a, n=n))
    if t == 'dp_odd':
        a, c, k = rng.randint(1, 5), rng.randint(1, 9), rng.choice([3, 5, 7]); val = 2 * a * c
        return dict(q=f'∫_{{−{a}}}^{{{a}}}(x^{{{k}}} cos x + sin^{{{k}}}x + {c})dx = ____.', o=None, a=val, sol=['x^{k}cos x and sin^{k}x are odd (k odd): they integrate to 0 on [−a, a].', f'Only the constant is left: {c} × {2 * a} = {val}.'], p=dict(t=t, a=a, c=c, k=k))
    if t == 'dp_wallis':
        n = rng.randint(2, 8); fn = rng.choice(['sin', 'cos'])
        def W(n): return F(1) if n == 0 else F(1) if n == 1 else F(n - 1, n) * W(n - 2)
        v = W(n); right = fr(v) + ('π/2' if n % 2 == 0 else '')
        right = f'\\f{{{v.numerator}π}}{{{2 * v.denominator}}}' if n % 2 == 0 else fr(v)
        wr = [f'\\f{{{v.numerator}π}}{{{v.denominator}}}', fr(v * 2), f'\\f{{{v.numerator + 1}π}}{{{2 * v.denominator}}}', fr(v + F(1, 2)), f'\\f{{π}}{{{n}}}']
        o, an = mcq(rng, right, wr)
        return dict(q=f'∫_{{0}}^{{π/2}}{fn}^{{{n}}}x dx =', o=o, a=an, sol=['Reduction: I_{n} = \\f{n − 1}{n}I_{n−2}, I_{0} = \\f{π}{2}, I_{1} = 1.', f'= {right}.'], p=dict(t=t, n=n, fn=fn))
    if t == 'dp_exp':
        k, m = rng.randint(2, 9), rng.randint(1, 3); val = F(k ** m - 1, m)
        need(val.denominator == 1)
        return dict(q=f'∫_{{0}}^{{log_{{e}}{k}}} e^{{{m if m > 1 else ""}x}}dx = ____.', o=None, a=int(val), sol=[f'= \\f{{e^{{{m}x}}}}{{{m}}} from 0 to log {k}.', f'\\f{{{k}^{{{m}}} − 1}}{{{m}}} = {int(val)}.'], p=dict(t=t, k=k, m=m))
    a, b, c = rng.randint(-4, 0), rng.randint(1, 6), rng.randint(-3, 5); need(a < c < b)
    val = F((c - a) ** 2 + (b - c) ** 2, 2)
    return dict(q=f'If I = ∫_{{{a}}}^{{{b}}}|x − ({c})|dx, then 2I = ____.'.replace('− (-', '+ (').replace('(', '').replace(')', ''), o=None, a=int(2 * val),
                sol=['Two triangles meeting at x = c.', f'I = \\f{{({c} − ({a}))^{{2}} + ({b} − {c})^{{2}}}}{{2}} → 2I = {int(2 * val)}.'], p=dict(t='dp_abs', a=a, b=b, c=c))

def g_gif(rng):
    t = rng.choice(['gf_floor', 'gf_frac', 'gf_sym', 'gf_lin'])
    if t == 'gf_floor':
        n = rng.randint(2, 25)
        return dict(q=f'∫_{{0}}^{{{n}}}[x]dx = ____ ([·] = greatest integer).', o=None, a=n * (n - 1) // 2, sol=['[x] = k on [k, k + 1): area k each.', f'0 + 1 + … + {n - 1} = {n * (n - 1) // 2}.'], p=dict(t=t, n=n))
    if t == 'gf_frac':
        n = rng.randint(2, 30)
        return dict(q=f'If I = ∫_{{0}}^{{{n}}}{{x}}dx, where {{x}} = x − [x] is the fractional part, then 2I = ____.', o=None, a=n, sol=['On each unit interval {x} goes from 0 to 1: area \\f{1}{2}.', f'I = \\f{{{n}}}{{2}} → 2I = {n}.'], p=dict(t=t, n=n))
    if t == 'gf_sym':
        n = rng.randint(1, 20)
        return dict(q=f'∫_{{−{n}}}^{{{n}}}[x]dx = ____.', o=None, a=-n, sol=['[x] + [−x] = −1 for non-integer x, so the integral over a symmetric range is −\\f{1}{2} × length.', f'= −{n}.'], p=dict(t=t, n=n))
    k, n = rng.randint(2, 7), rng.randint(1, 6)   # ∫_0^n [kx] dx = Σ_{j=0}^{kn−1} j/k
    val = F((k * n) * (k * n - 1), 2 * k)
    return dict(q=f'If I = ∫_{{0}}^{{{n}}}[{k}x]dx, then {2 * k}I = ____.', o=None, a=int(2 * k * val),
                sol=[f'[{k}x] = j on [\\f{{j}}{{{k}}}, \\f{{j + 1}}{{{k}}}): each piece contributes \\f{{j}}{{{k}}}.', f'I = \\f{{1}}{{{k}}}(0 + 1 + … + {k * n - 1}) = {fr(val)} → {int(2 * k * val)}.'], p=dict(t='gf_lin', k=k, n=n))

def g_indef(rng):
    t = rng.choice(['in_pf', 'in_lin'])
    if t == 'in_pf':
        p_, q_ = rng.sample(range(-5, 6), 2); al, be = rng.choice([x for x in range(-6, 7) if x]), rng.choice([x for x in range(-6, 7) if x])
        A, B = al + be, -(al * q_ + be * p_); need(A or B)
        den = poly_txt([1, -(p_ + q_), p_ * q_]); ask = rng.choice(['sum', 'prod', 'diff'])
        val = {'sum': al + be, 'prod': al * be, 'diff': al - be}[ask]
        return dict(q=f'If ∫\\f{{{poly_txt([A, B])}}}{{{den}}}dx = α log_{{e}}|x − ({p_})| + β log_{{e}}|x − ({q_})| + C, then {"α + β" if ask == "sum" else "αβ" if ask == "prod" else "α − β"} = ____.'.replace('− (-', '+ (').replace('(0)', '0'), o=None, a=val,
                    sol=[f'Partial fractions: \\f{{α}}{{x − {p_}}} + \\f{{β}}{{x − {q_}}} with α = {al}, β = {be}.'.replace('− -', '+ '), f'→ {val}.'], p=dict(t=t, pp=p_, qq=q_, A=A, B=B, ask=ask))
    c, d = rng.randint(1, 5), rng.randint(1, 5); lam, mu = rng.choice([F(k, 2) for k in range(-6, 7) if k]), rng.choice([F(k, 2) for k in range(-6, 7) if k])
    a, b = lam * c - mu * d, lam * d + mu * c; need(a.denominator == 1 and b.denominator == 1 and (a or b))
    num = ' '.join(x for x in [(fr(a) + ' sin x') if a else '', (('+ ' if b > 0 else '− ') + fr(abs(b)) + ' cos x') if b else ''] if x).lstrip('+ ')
    return dict(q=f'If ∫\\f{{{num}}}{{{c} sin x + {d} cos x}}dx = λx + μ log_{{e}}|{c} sin x + {d} cos x| + C, then 2(λ + μ) = ____.'.replace(' 1 sin', ' sin').replace(' 1 cos', ' cos').replace('{1 sin', '{sin'), o=None, a=int(2 * (lam + mu)),
                sol=['Write the top as λ·(bottom) + μ·(bottom)\'.', f'λ = {fr(lam)}, μ = {fr(mu)} → {int(2 * (lam + mu))}.'], p=dict(t='in_lin', a=int(a), b=int(b), c=c, d=d))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(area=g_area, defi=g_def, gif=g_gif, indef=g_indef).items()}
GEN['def'] = GEN.pop('defi')
def finish(it): return it
def close(a, b, tol=1e-4): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'ar_line':
        r1, r2 = p['r']; return close(R, 6 * integ(lambda x: max(0.0, p['m'] * x + p['c'] - p['a'] * x * x), r1 - 3, r2 + 3, 120000))
    if t == 'ar_pp':
        lo, hi = sorted([0, (p['c'] - p['b']) / 2]); f = lambda x: abs((-x * x + p['c'] * x) - (x * x + p['b'] * x)); return close(R, 24 * integ(f, lo, hi))
    if t == 'ar_sqrt':
        X = (p['k'] * p['m']) ** 2; return close(R, 6 * integ(lambda x: max(0.0, p['k'] * math.sqrt(x) - x / p['m']), 0, X + 5, 120000))
    if t == 'ar_abs':
        k = p['k']
        if p['ask'] == 'abs': return close(R, integ(lambda x: max(0.0, k - abs(x - p['a'])), p['a'] - k - 1, p['a'] + k + 1))
        return close(R, integ(lambda x: 2 * max(0.0, k - abs(x)), -k - 1, k + 1))
    if t == 'ar_cub': k = p['k']; return close(R, 2 * integ(lambda x: abs(x ** 3 - k * k * x), -k, k))
    if t == 'ar_cap': n, a = p['n'], p['a']; return close(R, 3 * integ(lambda x: max(0.0, a * n * n - a * x * x), -n - 1, n + 1, 120000))
    if t == 'ar_parab': return close(R, 3 * integ(lambda x: 2 * math.sqrt(4 * p['a'] * x), 0, p['b']))
    if t == 'ar_trig': return close(R, integ(lambda x: abs(math.sin(x)) if p['ask'] == 'sin' else abs(math.cos(x)), 0, p['n'] * PI))
    if t == 'dp_poly':
        cs = p['cs']; return close(R, 6 * integ(lambda x: cs[0] * x * x + cs[1] * x + cs[2], p['a'], p['b']))
    if t == 'dp_king':
        if p['kind'] == 'trig': n = p['n']; v = integ(lambda x: math.sin(x) ** n / (math.sin(x) ** n + math.cos(x) ** n), 0, PI / 2); return R == '\\f{π}{4}' and close(v, PI / 4)
        a, n = p['a'], p['n']; f = (lambda x: math.sqrt(x) / (math.sqrt(x) + math.sqrt(a - x))) if p['kind'] == 'sqrt' else (lambda x: x ** n / (x ** n + (a - x) ** n))
        return close(tofr(R), integ(f, 0, a))
    if t == 'dp_odd':
        a, c, k = p['a'], p['c'], p['k']; return close(R, integ(lambda x: x ** k * math.cos(x) + math.sin(x) ** k + c, -a, a))
    if t == 'dp_wallis':
        n = p['n']; v = integ(lambda x: (math.sin(x) if p['fn'] == 'sin' else math.cos(x)) ** n, 0, PI / 2)
        val = float(tofr(R.replace('π', ''))) * (PI if 'π' in R else 1); return close(val, v)
    if t == 'dp_exp': return close(R, integ(lambda x: math.exp(p['m'] * x), 0, math.log(p['k'])))
    if t == 'dp_abs': return close(R, 2 * integ(lambda x: abs(x - p['c']), p['a'], p['b']))
    if t == 'gf_floor': return close(R, integ(math.floor, 0, p['n'], 200000))
    if t == 'gf_frac': return close(R, 2 * integ(lambda x: x - math.floor(x), 0, p['n'], 200000))
    if t == 'gf_sym': return close(R, integ(math.floor, -p['n'], p['n'], 200000))
    if t == 'gf_lin': return close(R, 2 * p['k'] * integ(lambda x: math.floor(p['k'] * x), 0, p['n'], 240000))
    if t == 'in_pf':
        f = lambda x: (p['A'] * x + p['B']) / ((x - p['pp']) * (x - p['qq'])); xs = [x + 0.37 for x in (-7.1, 9.3, 12.2)]
        for al in range(-8, 9):
            for be in range(-8, 9):
                Fn = lambda x: al * math.log(abs(x - p['pp'])) + be * math.log(abs(x - p['qq']))
                if all(abs(d1(Fn, x) - f(x)) < 1e-6 for x in xs): return R == {'sum': al + be, 'prod': al * be, 'diff': al - be}[p['ask']]
        return False
    if t == 'in_lin':
        a, b, c, d = p['a'], p['b'], p['c'], p['d']; f = lambda x: (a * math.sin(x) + b * math.cos(x)) / (c * math.sin(x) + d * math.cos(x))
        for lam in [k / 2 for k in range(-12, 13)]:
            for mu in [k / 2 for k in range(-12, 13)]:
                Fn = lambda x: lam * x + mu * math.log(abs(c * math.sin(x) + d * math.cos(x)))
                if all(abs(d1(Fn, x) - f(x)) < 1e-6 for x in (0.2, 0.7, 1.1)): return R == round(2 * (lam + mu))
        return False
    raise KeyError(t)
