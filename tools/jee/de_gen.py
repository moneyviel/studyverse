"""Practice generators — Mathematics Unit 9: Differential Equations. Every item is built from a known solution and
check() re-solves it independently by a fourth-order Runge–Kutta integration of the stated equation from the stated
condition (or, for order-and-degree items, by reading the equation's structure from its parameters)."""
import math
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
def rk4(f, x0, y0, x1, n=3000):
    h = (x1 - x0) / n; x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y); k2 = f(x + h / 2, y + h * k1 / 2); k3 = f(x + h / 2, y + h * k2 / 2); k4 = f(x + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6; x += h
    return y
def tm(c, var='x', n=1):   # c·var^n as text
    if c == 0: return '0'
    v = '' if n == 0 else var if n == 1 else f'{var}^{{{n}}}'
    s = ('' if abs(c) == 1 and v else str(abs(c))) + v; return ('−' if c < 0 else '') + s
MU = {'pow': 'x^{k}', 'exp': 'e^{kx}', 'sq': '1 + x^{2}'}

def g_lin(rng):
    t = rng.choice(['pow', 'exp', 'sq', 'sec'])
    if t == 'pow':
        k, n, c = rng.randint(1, 4), rng.randint(1, 4), rng.randint(-4, 5); need(c); y0 = rng.randint(-5, 6)
        C = y0 - c; val = c * 2 ** (n + k) + C   # (x^k y)' = c(n+k)x^{n+k-1} with F = c x^{n+k}
        q = c * (n + k)
        return dict(q=f'If x\\f{{dy}}{{dx}} + {k}y = {tm(q, "x", n)}, y(1) = {y0}, then {2 ** k}y(2) = ____.'.replace(' 1y', ' y'), o=None, a=val,
                    sol=[f'Multiply by x^{{{k - 1}}}: (x^{{{k}}}y)\' = {tm(q, "x", n + k - 1)} → x^{{{k}}}y = {tm(c, "x", n + k)} + C.'.replace('x^{1}', 'x'), f'C = {C} from y(1) = {y0}; at x = 2: {2 ** k}y(2) = {val}.'], p=dict(t='l_pow', k=k, n=n, c=c, y0=y0))
    if t == 'exp':
        k, n, c = rng.randint(1, 3), rng.randint(0, 3), rng.randint(-4, 5); need(c); y0 = rng.randint(-5, 6)
        val = c + y0   # (e^{kx}y)' = c(n+1)x^n → e^{kx}y = c x^{n+1} + y0
        return dict(q=f'If \\f{{dy}}{{dx}} + {k}y = {tm(c * (n + 1), "x", n)}e^{{−{k}x}}, y(0) = {y0}, then {"e" if k == 1 else f"e^{{{k}}}"}y(1) = ____.'.replace(' 1y', ' y').replace('{−1x}', '{−x}'), o=None, a=val,
                    sol=[f'Integrating factor e^{{{k}x}}: (e^{{{k}x}}y)\' = {tm(c * (n + 1), "x", n)} → e^{{{k}x}}y = {tm(c, "x", n + 1)} + {y0}.', f'At x = 1: {val}.'], p=dict(t='l_exp', k=k, n=n, c=c, y0=y0))
    if t == 'sq':
        n, c, x1 = rng.randint(1, 3), rng.randint(-3, 4), rng.choice([1, 2, 3]); need(c); y0 = rng.randint(-5, 6)
        val = c * x1 ** (n + 1) + y0
        return dict(q=f'If (1 + x^{{2}})\\f{{dy}}{{dx}} + 2xy = {tm(c * (n + 1), "x", n)}, y(0) = {y0}, then {1 + x1 * x1}y({x1}) = ____.', o=None, a=val,
                    sol=['The left side is ((1 + x^{2})y)\'.', f'(1 + x^{{2}})y = {tm(c, "x", n + 1)} + {y0} → at x = {x1}: {val}.'], p=dict(t='l_sq', n=n, c=c, y0=y0, x1=x1))
    a, y0 = rng.choice([4, 8, -4, 12, -8, 16]), rng.randint(-5, 6)   # (y sec x)' = d(a sin²x) → y = cos x (a sin²x + y0)
    val = F(a * 3, 4) + y0
    return dict(q=f'If \\f{{dy}}{{dx}} + y tan x = {2 * a} sin x cos^{{2}}x, y(0) = {y0}, then 2y(\\f{{π}}{{3}}) = ____.', o=None, a=int(val),
                sol=['Integrating factor sec x: (y sec x)\' = 2a sin x cos x = (a sin^{2}x)\'.', f'y sec x = {a} sin^{{2}}x + {y0} → at \\f{{π}}{{3}}: 2y = {int(val)}.'], p=dict(t='l_sec', a=a, y0=y0))

def g_sep(rng):
    t = rng.choice(['s_gauss', 's_exact', 's_hom', 's_exp', 's_lin', 's_circ', 's_ber'])
    if t == 's_gauss':
        k, x1 = rng.randint(1, 6), rng.choice([1, 2, 3]); a = rng.randint(1, 9); val = F(k * x1 * x1, 2); need(val.denominator == 1)
        return dict(q=f'If \\f{{dy}}{{dx}} = {k if k > 1 else ""}xy and y(0) = {a}, then log_{{e}}(\\f{{y({x1})}}{{{a}}}) = ____.', o=None, a=int(val),
                    sol=['Separate: \\f{dy}{y} = kx dx → log\\f{y}{y(0)} = \\f{kx^{2}}{2}.', f'= {int(val)}.'], p=dict(t=t, k=k, x1=x1, a=a))
    if t == 's_exact':
        b, y0, x1 = rng.randint(1, 4), rng.randint(-5, 6), rng.choice([2, 3, 4]); C = y0 + b
        val = F(C - b * x1 * x1, x1)
        return dict(q=f'The curve through (1, {y0}) satisfies (y + {2 * b}x)dx + x dy = 0. Then {x1}y({x1}) = ____.', o=None, a=int(x1 * val),
                    sol=[f'The left side is d(xy + {b}x^{{2}}) → xy + {b}x^{{2}} = {C}.', f'At x = {x1}: {x1}y = {C} − {b * x1 * x1} = {int(x1 * val)}.'], p=dict(t=t, b=b, y0=y0, x1=x1))
    if t == 's_hom':
        c, n = rng.randint(1, 4), rng.randint(2, 5); val = F(c * (n * n - 1), 2); need(val.denominator == 1)
        return dict(q=f'The solution of x dy − y dx = √{{x^{{2}} + y^{{2}}}} dx, x > 0, with y({c}) = 0 has y({n * c}) = ____.', o=None, a=int(val),
                    sol=['y = vx: \\f{dv}{√{1 + v^{2}}} = \\f{dx}{x} → y + √{x^{2} + y^{2}} = kx^{2}.', f'Through ({c}, 0): k = \\f{{1}}{{{c}}} → y = \\f{{x^{{2}} − {c * c}}}{{{2 * c}}} → y({n * c}) = {int(val)}.'.replace('x^{2} − 1}', 'x^{2} − 1}')], p=dict(t=t, c=c, n=n))
    if t == 's_exp':
        k, m = rng.randint(2, 9), rng.randint(1, 9)
        return dict(q=f'If \\f{{dy}}{{dx}} = e^{{x − y}} and y(0) = log_{{e}}{m}, then e^{{y(log_{{e}}{k})}} = ____.', o=None, a=k + m - 1,
                    sol=['Separate: e^{y}dy = e^{x}dx → e^{y} = e^{x} + C.', f'C = {m} − 1 → e^{{y}} = {k} + {m - 1} = {k + m - 1}.'], p=dict(t=t, k=k, m=m))
    if t == 's_lin':
        a, x1 = rng.randint(-4, 6), rng.randint(1, 5)
        return dict(q=f'If \\f{{dy}}{{dx}} = \\f{{y + 1}}{{x + 1}} and y(0) = {a}, then y({x1}) = ____.', o=None, a=(a + 1) * (x1 + 1) - 1,
                    sol=['Separate: \\f{dy}{y + 1} = \\f{dx}{x + 1} → y + 1 = A(x + 1).', f'A = {a + 1} → y({x1}) = {(a + 1) * (x1 + 1) - 1}.'], p=dict(t=t, a=a, x1=x1))
    if t == 's_circ':
        a, x1 = rng.randint(1, 9), rng.randint(1, 6)
        return dict(q=f'If y\\f{{dy}}{{dx}} = x and y(0) = {a}, then (y({x1}))^{{2}} = ____.', o=None, a=a * a + x1 * x1, sol=['y dy = x dx → y^{2} − x^{2} = C.', f'C = {a * a} → y^{{2}} = {a * a} + {x1 * x1} = {a * a + x1 * x1}.'], p=dict(t=t, a=a, x1=x1))
    k, m = rng.randint(2, 6), rng.randint(1, 4)   # y' = y² e^x, y(0) = −1/m → −1/y = e^x + m − 1
    v = F(-1, k + m - 1); o, an = mcq(rng, fr(v), [fr(-v), fr(F(-1, k + m)), fr(F(-1, k)), fr(F(-1, m))])
    return dict(q=f'If \\f{{dy}}{{dx}} = y^{{2}}e^{{x}} and y(0) = −\\f{{1}}{{{m}}}, then y(log_{{e}}{k}) ='.replace('\\f{1}{1}', '1'), o=o, a=an,
                sol=['Separate: \\f{dy}{y^{2}} = e^{x}dx → −\\f{1}{y} = e^{x} + C.', f'C = {m - 1} → −\\f{{1}}{{y}} = {k + m - 1} → y = {fr(v)}.'], p=dict(t='s_ber', k=k, m=m))

def g_form(rng):
    t = rng.choice(['f_od', 'f_fam', 'f_fam2'])
    if t == 'f_od':
        o2, p2, o1, p1 = rng.randint(2, 4), rng.randint(1, 5), 1, rng.randint(1, 6); ask = rng.choice(['sum', 'prod'])
        order, degree = o2, p2; val = order + degree if ask == 'sum' else order * degree
        d = lambda k: '\\f{dy}{dx}' if k == 1 else f'\\f{{d^{{{k}}}y}}{{dx^{{{k}}}}}'
        return dict(q=f'For the differential equation ({d(o2)})^{{{p2}}} + ({d(o1)})^{{{p1}}} + y = 0, the {"sum" if ask == "sum" else "product"} of its order and degree is ____.'.replace('^{1}', ''), o=None, a=val,
                    sol=['Order = highest derivative present; degree = its power once the equation is a polynomial in the derivatives.', f'Order {order}, degree {degree} → {val}.'], p=dict(t=t, o2=o2, p2=p2, p1=p1, ask=ask))
    if t == 'f_fam':
        k = rng.randint(1, 9)
        return dict(q=f'The differential equation of the family y = Ae^{{{k}x}} + Be^{{−{k}x}} (A, B arbitrary) is y" = cy. Then c = ____.'.replace('{1x}', '{x}').replace('{−1x}', '{−x}'), o=None, a=k * k,
                    sol=['Differentiate twice: y" = k^{2}(Ae^{kx} + Be^{−kx}) = k^{2}y.', f'c = {k * k}.'], p=dict(t=t, k=k))
    k = rng.randint(1, 9)
    return dict(q=f'The differential equation of the family y = A cos {k}x + B sin {k}x is y" + cy = 0. Then c = ____.'.replace(' 1x', ' x'), o=None, a=k * k,
                sol=['Differentiate twice: y" = −k^{2}y.', f'c = {k * k}.'], p=dict(t=t, k=k))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(lin=g_lin, sep=g_sep, form=g_form).items()}
def finish(it): return it
def close(a, b, tol=1e-5): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))
def tofr(s):
    s = s.replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-'); v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'l_pow':
        k, n, c = p['k'], p['n'], p['c']; return close(R, 2 ** k * rk4(lambda x, y: (c * (n + k) * x ** n - k * y) / x, 1, p['y0'], 2))
    if t == 'l_exp':
        k, n, c = p['k'], p['n'], p['c']; return close(R, math.exp(k) * rk4(lambda x, y: c * (n + 1) * x ** n * math.exp(-k * x) - k * y, 0, p['y0'], 1))
    if t == 'l_sq':
        n, c, x1 = p['n'], p['c'], p['x1']; return close(R, (1 + x1 * x1) * rk4(lambda x, y: (c * (n + 1) * x ** n - 2 * x * y) / (1 + x * x), 0, p['y0'], x1))
    if t == 'l_sec': a = p['a']; return close(R, 2 * rk4(lambda x, y: 2 * a * math.sin(x) * math.cos(x) ** 2 - y * math.tan(x), 0, p['y0'], math.pi / 3))
    if t == 's_gauss': return close(R, math.log(rk4(lambda x, y: p['k'] * x * y, 0, p['a'], p['x1']) / p['a']))
    if t == 's_exact': b, x1 = p['b'], p['x1']; return close(R, x1 * rk4(lambda x, y: -(y + 2 * b * x) / x, 1, p['y0'], x1))
    if t == 's_hom':
        c, n = p['c'], p['n']; x0 = c * 1.1; y0 = (x0 * x0 - c * c) / (2 * c)   # start just off the singular point, on the branch through (c, 0)
        y_chk = rk4(lambda x, y: (y + math.sqrt(x * x + y * y)) / x, c, 0, x0, 2000)
        return abs(y_chk - y0) < 1e-6 and close(R, rk4(lambda x, y: (y + math.sqrt(x * x + y * y)) / x, c, 0, n * c))
    if t == 's_exp': return close(R, math.exp(rk4(lambda x, y: math.exp(x - y), 0, math.log(p['m']), math.log(p['k']))))
    if t == 's_lin': return close(R, rk4(lambda x, y: (y + 1) / (x + 1), 0, p['a'], p['x1']))
    if t == 's_circ': return close(R, rk4(lambda x, y: x / y, 0, p['a'], p['x1']) ** 2)
    if t == 's_ber': return close(tofr(R), rk4(lambda x, y: y * y * math.exp(x), 0, -1 / p['m'], math.log(p['k'])))
    if t == 'f_od':
        order, degree = p['o2'], p['p2']; return R == (order + degree if p['ask'] == 'sum' else order * degree) and p['o2'] > 1
    if t == 'f_fam':
        k = p['k']; y = lambda x: 1.3 * math.exp(k * x) - 0.4 * math.exp(-k * x); h = 1e-4; x = 0.2
        return close(R, (y(x + h) - 2 * y(x) + y(x - h)) / h ** 2 / y(x), 1e-4)
    if t == 'f_fam2':
        k = p['k']; y = lambda x: 1.3 * math.cos(k * x) + 0.7 * math.sin(k * x); h = 1e-4; x = 0.11
        return close(R, -(y(x + h) - 2 * y(x) + y(x - h)) / h ** 2 / y(x), 1e-3)
    raise KeyError(t)
