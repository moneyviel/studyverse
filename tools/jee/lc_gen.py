"""Practice generators — Mathematics Unit 7: Limits, Continuity and Differentiability (with applications of
derivatives). check() re-solves every item numerically: limits by evaluating the expression very close to the
point, continuity and differentiability by comparing one-sided values and slopes on a fine scan, derivatives by
central differences and extrema by scanning a grid."""
import math
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
def lim(f, a, side=0, h=1e-3):
    sides = [side] if side else [1, -1]; vals = [2 * f(a + s * h / 2) - f(a + s * h) for s in sides]; return sum(vals) / len(vals)
def lim_inf(f, n=1e5): return 2 * f(2 * n) - f(n)
def d1(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
def d2(f, x, h=1e-4): return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)
def grid(lo, hi, n): return [lo + (hi - lo) * i / (n - 1) for i in range(n)]
def fopts(rng, v, extra):
    right = fr(v); o, a = mcq(rng, right, [fr(x) for x in extra]); return o, a
def tofr(s):
    s = s.replace('−', '-')
    if s.startswith('-\\f') or s.startswith('\\f'):
        neg = s.startswith('-'); s = s.lstrip('-').replace('\\f{', '').replace('}{', '/').replace('}', ''); return -F(s) if neg else F(s)
    return F(s)

STD = {'sin': ('sin {a}x', lambda a, x: math.sin(a * x), lambda a: F(a)), 'tan': ('tan {a}x', lambda a, x: math.tan(a * x), lambda a: F(a)),
       'exp': ('(e^{{{a}x}} − 1)', lambda a, x: math.expm1(a * x), lambda a: F(a)), 'log': ('log_{{e}}(1 + {a}x)', lambda a, x: math.log1p(a * x), lambda a: F(a)),
       'asin': ('sin^{{−1}} {a}x', lambda a, x: math.asin(a * x), lambda a: F(a)), 'atan': ('tan^{{−1}} {a}x', lambda a, x: math.atan(a * x), lambda a: F(a))}
def g_lim(rng):
    t = rng.choice(['l_ratio', 'l_cos', 'l_pow', 'l_inf', 'l_coef', 'l_sqrt'])
    if t == 'l_ratio':
        k1, k2 = rng.sample(sorted(STD), 2); a, b = rng.randint(1, 9), rng.randint(1, 9); v = F(a, b)
        o, an = fopts(rng, v, [F(b, a), v * 2, v + 1, F(a * b), -v])
        return dict(q=f'\\lim_{{x→0}} \\f{{{STD[k1][0].format(a=a)}}}{{{STD[k2][0].format(a=b)}}} =', o=o, a=an,
                    sol=['Each of sin kx, tan kx, e^{kx} − 1, log(1 + kx), sin^{−1}kx, tan^{−1}kx behaves like kx near 0.', f'Ratio → \\f{{{a}}}{{{b}}} = {fr(v)}.'], p=dict(t=t, k1=k1, k2=k2, a=a, b=b))
    if t == 'l_cos':
        a, b = rng.randint(1, 8), rng.randint(1, 8); kind = rng.choice(['x2', 'cos'])
        v = F(a * a, 2) if kind == 'x2' else F(a * a, b * b)
        o, an = fopts(rng, v, [v * 2, F(a, b), v + 1, F(a * a, 4), F(b * b, a * a)])
        q = f'\\lim_{{x→0}} \\f{{1 − cos {a}x}}{{x^{{2}}}} =' if kind == 'x2' else f'\\lim_{{x→0}} \\f{{1 − cos {a}x}}{{1 − cos {b}x}} ='
        return dict(q=q, o=o, a=an, sol=['1 − cos kx = 2 sin^{2}\\f{kx}{2} ≈ \\f{k^{2}x^{2}}{2}.', f'→ {fr(v)}.'], p=dict(t=t, a=a, b=b, kind=kind))
    if t == 'l_pow':
        a, n = rng.randint(1, 5), rng.randint(2, 7); m = rng.randint(1, 5); need(m != n)
        v = F(n, m) * F(a) ** (n - m)
        o, an = fopts(rng, v, [F(m, n) * F(a) ** (n - m), F(n) * a ** (n - 1), v + 1, v * a])
        return dict(q=f'\\lim_{{x→{a}}} \\f{{x^{{{n}}} − {a ** n}}}{{x^{{{m}}} − {a ** m}}} =', o=o, a=an,
                    sol=['\\f{x^{n} − a^{n}}{x − a} → na^{n−1}; divide top and bottom by x − a.', f'\\f{{{n}·{a}^{{{n - 1}}}}}{{{m}·{a}^{{{m - 1}}}}} = {fr(v)}.'], p=dict(t=t, a=a, n=n, m=m))
    if t == 'l_inf':
        a, b = rng.randint(1, 6), rng.randint(1, 6); kind = rng.choice(['e', 'rat'])
        if kind == 'e':
            return dict(q=f'If \\lim_{{x→∞}}(1 + \\f{{{a}}}{{x}})^{{{b}x}} = e^{{k}}, then k = ____.', o=None, a=a * b,
                        sol=['(1 + \\f{a}{x})^{bx} → e^{ab}.', f'k = {a * b}.'], p=dict(t=t, a=a, b=b, kind=kind))
        c, d = rng.randint(1, 9), rng.randint(1, 9); v = F(a, c)
        o, an = fopts(rng, v, [F(c, a), F(b, d), v + 1, F(0)])
        return dict(q=f'\\lim_{{x→∞}} \\f{{{a}x^{{2}} + {b}x + 1}}{{{c}x^{{2}} − {d}x + 5}} =', o=o, a=an, sol=['Divide top and bottom by x^{2}.', f'→ \\f{{{a}}}{{{c}}} = {fr(v)}.'], p=dict(t=t, a=a, b=b, c=c, d=d, kind=kind))
    if t == 'l_coef':
        pp, qq = rng.sample(range(1, 6), 2); A = -F(pp * pp, qq * qq); B = 1 + A; v = A + B
        o, an = fopts(rng, v, [A - B, -v, v + 1, A, B])
        return dict(q=f'If \\lim_{{x→0}} \\f{{cos {pp}x + a cos {qq}x − b}}{{x^{{4}}}} is finite, then a + b =', o=o, a=an,
                    sol=['Constant term 1 + a − b = 0 and x^{2} term −\\f{p^{2}}{2} − \\f{aq^{2}}{2} = 0.', f'a = {fr(A)}, b = {fr(B)} → a + b = {fr(v)}.'], p=dict(t=t, pp=pp, qq=qq))
    a = rng.randint(-3, 12); c = rng.choice([k * k for k in range(1, 6)]) - a; need(a + c > 0); v = F(1, 2 * math.isqrt(a + c))
    o, an = fopts(rng, v, [F(1, math.isqrt(a + c)), v * 2 + 1, F(math.isqrt(a + c), 2), F(1, a + c)])
    return dict(q=f'\\lim_{{x→{a}}} \\f{{√{{x + {c}}} − {math.isqrt(a + c)}}}{{x − ({a})}} ='.replace('+ -', '− ').replace('(-', '(−'), o=o, a=an,
                sol=['Multiply by the conjugate: \\f{1}{√{x + c} + √{a + c}}.', f'→ {fr(v)}.'], p=dict(t='l_sqrt', a=a, c=c))

def g_cont(rng):
    t = rng.choice(['c_piece', 'c_floor', 'c_corner', 'c_param'])
    if t == 'c_piece':
        k = rng.randint(1, 8); kind = rng.choice(['cos', 'sin', 'exp'])
        v = {'cos': F(k * k, 2), 'sin': F(k), 'exp': F(k)}[kind]
        txt = {'cos': f'\\f{{1 − cos {k}x}}{{x^{{2}}}}', 'sin': f'\\f{{sin {k}x}}{{x}}', 'exp': f'\\f{{e^{{{k}x}} − 1}}{{x}}'}[kind]
        o, an = fopts(rng, v, [v * 2, v + 1, F(k, 2), F(1), F(k * k)])
        return dict(q=f'f(x) = {txt} for x ≠ 0 is continuous at x = 0. Then f(0) =', o=o, a=an, sol=['f(0) must equal the limit at 0.', f'→ {fr(v)}.'], p=dict(t=t, k=k, kind=kind))
    if t == 'c_floor':
        k, n = rng.choice([1, 2, 3, 4]), rng.randint(2, 4); kind = rng.choice(['sq', 'lin'])
        if kind == 'sq': pts = [math.sqrt(k * j) for j in range(1, n * n // k + 1) if 0 < math.sqrt(k * j) < n]
        else: pts = [j / k for j in range(1, n * k) if 0 < j / k < n]
        val = len(pts)
        expr = (f'x^{{2}}' if k == 1 else f'\\f{{x^{{2}}}}{{{k}}}') if kind == 'sq' else (f'{k}x' if k > 1 else 'x')
        return dict(q=f'The number of points in the open interval (0, {n}) where f(x) = [{expr}] ([·] = greatest integer) is discontinuous is ____.', o=None, a=val,
                    sol=['[g(x)] jumps exactly where g(x) passes an integer.', f'{val} points.'], p=dict(t=t, k=k, n=n, kind=kind))
    if t == 'c_corner':
        cs = sorted(rng.sample(range(-5, 6), rng.randint(2, 4))); kind = rng.choice(['abs', 'sq'])
        if kind == 'abs':
            val = len(cs); txt = ' + '.join(f'|x − ({c})|'.replace('− (-', '+ (').replace('(', '').replace(')', '') if c else '|x|' for c in cs)
            return dict(q=f'The number of points where f(x) = {txt} is not differentiable is ____.', o=None, a=val, sol=['Each |x − c| adds a corner at x = c.', f'{val} points.'], p=dict(t=t, cs=cs, kind=kind))
        c = rng.randint(1, 9); val = 2
        return dict(q=f'The number of points where f(x) = |x^{{2}} − {c}| is not differentiable is ____.', o=None, a=val, sol=[f'Corners where x^{{2}} = {c}: x = ±√{{{c}}}.', '2 points.'], p=dict(t=t, c=c, kind=kind))
    a, b = rng.randint(1, 6), rng.randint(1, 6); kind = rng.choice(['lin', 'quad'])
    v = F(a * 1 + b, 1) if kind == 'lin' else F(a * 4 + b - 2, 1)
    q = (f'f(x) = kx + {b} for x ≤ 1 and f(x) = {a + b}x^{{2}} − ... ' if False else
         (f'f(x) = {a}x + {b} for x ≤ 1 and f(x) = kx^{{2}} for x > 1 is continuous at x = 1. Then k = ____.' if kind == 'lin' else f'f(x) = {a}x^{{2}} + {b} for x ≤ 2 and f(x) = kx + 2 for x > 2 is continuous at x = 2. Then 2k = ____.'))
    val = a + b if kind == 'lin' else 4 * a + b - 2
    return dict(q=q, o=None, a=val, sol=['Match the two one-sided values at the joining point.', f'→ {val}.'], p=dict(t='c_param', a=a, b=b, kind=kind))

def g_deriv(rng):
    t = rng.choice(['d_prod', 'd_chain', 'd_quot', 'd_ode'])
    if t == 'd_prod':
        a, b, c = rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-2, 3); val = (2 * c) * (c ** 3 + b) + (c * c + a) * 3 * c * c
        return dict(q=f'If f(x) = (x^{{2}} + {a})(x^{{3}} + {b}), then f\'({c}) = ____.'.replace('+ -', '− '), o=None, a=val, sol=['Product rule: f\' = 2x(x^{3} + b) + 3x^{2}(x^{2} + a).', f'f\'({c}) = {val}.'], p=dict(t=t, a=a, b=b, c=c))
    if t == 'd_chain':
        a, b, n, x0 = rng.randint(1, 4), rng.randint(-3, 3), rng.randint(2, 5), rng.randint(-1, 2); val = n * a * (a * x0 + b) ** (n - 1)
        return dict(q=f'If y = ({a}x + {b})^{{{n}}}, then \\f{{dy}}{{dx}} at x = {x0} is ____.'.replace('+ -', '− '), o=None, a=val, sol=['Chain rule: n·a·(ax + b)^{n−1}.', f'= {val}.'], p=dict(t=t, a=a, b=b, n=n, x0=x0))
    if t == 'd_quot':
        a, b, c, d = rng.randint(1, 5), rng.randint(-4, 4), rng.randint(1, 4), rng.randint(1, 5); x0 = rng.randint(0, 3); need(c * x0 + d != 0 and a * d - b * c != 0)
        v = F(a * d - b * c, (c * x0 + d) ** 2); o, an = fopts(rng, v, [-v, F(a, c), v * 2, F(a * d + b * c, (c * x0 + d) ** 2)])
        return dict(q=f'If f(x) = \\f{{{a}x + {b}}}{{{c}x + {d}}}, then f\'({x0}) ='.replace('+ -', '− '), o=o, a=an, sol=['f\' = \\f{ad − bc}{(cx + d)^{2}}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b, c=c, d=d, x0=x0))
    pp, qq = rng.sample(range(-4, 5), 2); A, B = -(pp + qq), pp * qq
    return dict(q=f'y = c_{{1}}e^{{{pp}x}} + c_{{2}}e^{{{qq}x}} satisfies y" + ay\' + by = 0 for all constants c_{{1}}, c_{{2}}. Then a + 2b = ____.', o=None, a=A + 2 * B,
                sol=[f'{pp} and {qq} are the roots of m^{{2}} + am + b = 0.', f'a = {A}, b = {B} → {A + 2 * B}.'], p=dict(t='d_ode', pp=pp, qq=qq))

def g_app(rng):
    t = rng.choice(['a_cubic', 'a_trig', 'a_rect', 'a_mono', 'a_box'])
    if t == 'a_cubic':
        p_, q_ = sorted(rng.sample(range(-4, 6), 2)); c = rng.randint(-5, 5); f = lambda x: 2 * x ** 3 - 3 * (p_ + q_) * x * x + 6 * p_ * q_ * x + c
        ask = rng.choice(['diff', 'sum', 'max']); val = {'diff': f(p_) - f(q_), 'sum': p_ + q_, 'max': f(p_)}[ask]
        txt = {'diff': 'the local maximum value minus the local minimum value', 'sum': 'the sum of the points of local maximum and local minimum', 'max': 'the local maximum value'}[ask]
        return dict(q=f'For f(x) = 2x^{{3}} − {3 * (p_ + q_)}x^{{2}} + {6 * p_ * q_}x + {c}, {txt} is ____.'.replace('+ -', '− ').replace('− -', '+ '), o=None, a=val,
                    sol=[f'f\'(x) = 6(x − {p_})(x − {q_}): maximum at the smaller root, minimum at the larger.'.replace('− -', '+ '), f'→ {val}.'], p=dict(t=t, p=p_, q=q_, c=c, ask=ask))
    if t == 'a_trig':
        a, b = rng.choice([(3, 4), (5, 12), (8, 15), (6, 8), (7, 24), (9, 12), (12, 5), (4, 3)]); c = rng.randint(-5, 9); ask = rng.choice(['max', 'min', 'sum'])
        r = math.isqrt(a * a + b * b); val = {'max': r + c, 'min': c - r, 'sum': 2 * c}[ask]
        return dict(q=f'For f(x) = {a} sin x + {b} cos x + {c}, the {"maximum value" if ask == "max" else "minimum value" if ask == "min" else "sum of the maximum and minimum values"} is ____.'.replace('+ -', '− '), o=None, a=val,
                    sol=[f'a sin x + b cos x ranges over [−√{{a^{{2}} + b^{{2}}}}, √{{a^{{2}} + b^{{2}}}}] = [−{r}, {r}].', f'→ {val}.'], p=dict(t=t, a=a, b=b, c=c, ask=ask))
    if t == 'a_rect':
        m = rng.randint(1, 5); k = 3 * m * m
        return dict(q=f'A rectangle has its base on the x-axis and its upper corners on y = {k} − x^{{2}}. Its maximum area is ____.', o=None, a=4 * m ** 3,
                    sol=[f'Area A(x) = 2x({k} − x^{{2}}); A\'(x) = 0 at x = √{{{k}/3}} = {m}.', f'A = 2·{m}·{2 * m * m} = {4 * m ** 3}.'], p=dict(t=t, k=k))
    if t == 'a_mono':
        k = rng.randint(1, 7); kind = rng.choice(['dec', 'inc'])
        val = 2 * k - 1 if kind == 'dec' else None
        if kind == 'inc':
            n = rng.randint(k + 1, k + 8); val = 2 * (n - k)
            return dict(q=f'The number of integers x in [−{n}, {n}] at which f(x) = x^{{3}} − {3 * k * k}x is strictly increasing (f\'(x) > 0) is ____.', o=None, a=val,
                        sol=[f'f\'(x) = 3(x^{{2}} − {k * k}) > 0 for |x| > {k}.', f'Integers {k + 1}…{n} and their negatives → {val}.'], p=dict(t=t, k=k, kind=kind, n=n))
        return dict(q=f'The number of integers in the interval where f(x) = x^{{3}} − {3 * k * k}x is decreasing is ____.', o=None, a=val,
                    sol=[f'f\'(x) = 3(x^{{2}} − {k * k}) < 0 on (−{k}, {k}).', f'{val} integers.'], p=dict(t=t, k=k, kind=kind))
    m = rng.randint(1, 6); s = 6 * m
    return dict(q=f'Equal squares are cut from the corners of a {s} cm × {s} cm sheet and the sides folded up into an open box. The largest possible volume (cm^{{3}}) is ____.', o=None, a=16 * m ** 3,
                sol=[f'V(x) = x({s} − 2x)^{{2}}; V\'(x) = 0 at x = \\f{{{s}}}{{6}} = {m}.', f'V = {m} × {4 * m}^{{2}} = {16 * m ** 3}.'], p=dict(t='a_box', s=s))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(lim=g_lim, cont=g_cont, deriv=g_deriv, app=g_app).items()}
def finish(it): return it
def close(a, b, tol=1e-4): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = tofr(R) if isinstance(R, str) else R
    if t == 'l_ratio': return close(V, lim(lambda x: STD[p['k1']][1](p['a'], x) / STD[p['k2']][1](p['b'], x), 0, h=1e-3))
    if t == 'l_cos': return close(V, lim((lambda x: (1 - math.cos(p['a'] * x)) / x ** 2) if p['kind'] == 'x2' else (lambda x: (1 - math.cos(p['a'] * x)) / (1 - math.cos(p['b'] * x))), 0, h=1e-3))
    if t == 'l_pow': a = p['a']; return close(V, lim(lambda x: (x ** p['n'] - a ** p['n']) / (x ** p['m'] - a ** p['m']), a, h=1e-4))
    if t == 'l_inf':
        if p['kind'] == 'e': return close(V, lim_inf(lambda x: p['b'] * x * math.log1p(p['a'] / x)))
        return close(V, lim_inf(lambda x: (p['a'] * x * x + p['b'] * x + 1) / (p['c'] * x * x - p['d'] * x + 5)))
    if t == 'l_coef':
        ok = []
        for m in range(1, 26):
            for n in range(1, 26):
                a = -F(n, m); b = 1 + a; f = lambda x: (math.cos(p['pp'] * x) + float(a) * math.cos(p['qq'] * x) - float(b)) / x ** 4
                if abs(f(0.002)) < 200: ok.append(a + b)
        return len(set(ok)) == 1 and V == ok[0]
    if t == 'l_sqrt': return close(V, lim(lambda x: (math.sqrt(x + p['c']) - math.sqrt(p['a'] + p['c'])) / (x - p['a']), p['a'], h=1e-4))
    if t == 'c_piece':
        f = {'cos': lambda x: (1 - math.cos(p['k'] * x)) / x ** 2, 'sin': lambda x: math.sin(p['k'] * x) / x, 'exp': lambda x: math.expm1(p['k'] * x) / x}[p['kind']]
        return close(V, lim(f, 0, h=1e-3))
    if t == 'c_floor':
        k, n = p['k'], p['n']; f = (lambda x: math.floor(x * x / k + 1e-12)) if p['kind'] == 'sq' else (lambda x: math.floor(k * x + 1e-12))
        xs = grid(1e-9, n - 1e-9, 200001); return V == sum(1 for a, b in zip(xs, xs[1:]) if f(a) != f(b))
    if t == 'c_corner':
        f = (lambda x: sum(abs(x - c) for c in p['cs'])) if p['kind'] == 'abs' else (lambda x: abs(x * x - p['c']))
        xs = grid(-12.000037, 12.000041, 240001); sl = [(f(b) - f(a)) / (b - a) for a, b in zip(xs, xs[1:])]
        jj = [i for i, (u, v) in enumerate(zip(sl, sl[1:])) if abs(u - v) > 0.5]; return V == sum(1 for k, i in enumerate(jj) if k == 0 or i - jj[k - 1] > 1)
    if t == 'c_param':
        a, b = p['a'], p['b']
        if p['kind'] == 'lin': return abs((a + b) - V * 1) < 1e-12 and abs(lim(lambda x: a * x + b, 1, -1) - lim(lambda x: V * x * x, 1, 1)) < 1e-4
        k = F(V, 2); return abs(lim(lambda x: a * x * x + b, 2, -1) - lim(lambda x: float(k) * x + 2, 2, 1)) < 1e-4
    if t == 'd_prod': return close(V, d1(lambda x: (x * x + p['a']) * (x ** 3 + p['b']), p['c']))
    if t == 'd_chain': return close(V, d1(lambda x: (p['a'] * x + p['b']) ** p['n'], p['x0']))
    if t == 'd_quot': return close(V, d1(lambda x: (p['a'] * x + p['b']) / (p['c'] * x + p['d']), p['x0']))
    if t == 'd_ode':
        y = lambda x: 2 * math.exp(p['pp'] * x) - 3 * math.exp(p['qq'] * x); z = lambda x: math.exp(p['pp'] * x) + math.exp(p['qq'] * x)
        for a in range(-20, 21):
            for b in range(-20, 21):
                if all(abs(d2(g, 0.1) + a * d1(g, 0.1) + b * g(0.1)) < 1e-3 * max(1, abs(d2(g, 0.1))) for g in (y, z)): return V == a + 2 * b
        return False
    if t == 'a_cubic':
        f = lambda x: 2 * x ** 3 - 3 * (p['p'] + p['q']) * x * x + 6 * p['p'] * p['q'] * x + p['c']; xs = [k / 1000 for k in range(-10000, 10001)]
        mx = next(x for a, x, b in zip(xs, xs[1:], xs[2:]) if f(x) >= f(a) and f(x) >= f(b)); mn = next(x for a, x, b in zip(xs, xs[1:], xs[2:]) if f(x) <= f(a) and f(x) <= f(b))
        return close(V, {'diff': f(mx) - f(mn), 'sum': mx + mn, 'max': f(mx)}[p['ask']])
    if t == 'a_trig':
        v = [p['a'] * math.sin(x) + p['b'] * math.cos(x) + p['c'] for x in grid(0, 2 * math.pi, 200001)]
        return close(V, {'max': max(v), 'min': min(v), 'sum': max(v) + min(v)}[p['ask']], 1e-6)
    if t == 'a_rect': return close(V, max(2 * x * (p['k'] - x * x) for x in grid(0, math.sqrt(p['k']), 200001)), 1e-6)
    if t == 'a_mono':
        k = p['k']; f = lambda x: x ** 3 - 3 * k * k * x
        if p['kind'] == 'dec': return V == sum(1 for x in range(-50, 51) if d1(f, x) < -1e-3)
        return V == sum(1 for x in range(-p['n'], p['n'] + 1) if d1(f, x) > 1e-3)
    if t == 'a_box': s = p['s']; return close(V, max(x * (s - 2 * x) ** 2 for x in grid(0, s / 2, 300001)), 1e-6)
    raise KeyError(t)
