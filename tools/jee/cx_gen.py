"""Practice generators — Mathematics Unit 2: Complex Numbers and Quadratic Equations. check() re-solves each item with
complex arithmetic: loci by sampling the curve, roots from the quadratic formula, powers by repeated multiplication,
root counts by scanning for sign changes."""
import cmath, math
from fractions import Fraction as F
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def qroots(a, b, c):
    d = cmath.sqrt(b * b - 4 * a * c); return (-b + d) / (2 * a), (-b - d) / (2 * a)
def grid(lo, hi, n): return [lo + (hi - lo) * i / (n - 1) for i in range(n)]
def circle(c, r, n=7200): return [c + r * cmath.exp(2j * math.pi * k / n) for k in range(n)]
def cstr(z):
    a, b = round(z.real, 6), round(z.imag, 6); a = int(a) if a == int(a) else a; b = int(b) if b == int(b) else b
    if b == 0: return f'{a}'
    if a == 0: return f'{"" if b == 1 else ("−" if b == -1 else str(b).replace("-", "−"))}i'
    return f'{a} {"+" if b > 0 else "−"} {"" if abs(b) == 1 else abs(b)}i'.replace('-', '−')
def cnum(s):
    s = s.replace('−', '-').replace(' ', '')
    if 'i' not in s: return complex(float(s))
    s = s.replace('i', 'j'); s = s.replace('+j', '+1j').replace('-j', '-1j')
    if s.startswith('j'): s = '1' + s
    return complex(s)

def g_cmod(rng):
    t = rng.choice(['m_far', 'm_near', 'm_line', 'm_lat', 'm_arg', 'm_two'])
    if t in ('m_far', 'm_near'):
        c = complex(rng.randint(-4, 4), rng.randint(-4, 4)); r = rng.choice([1, 2, 3, 5]); p = complex(*rng.choice([(3, 4), (6, 8), (-5, 12), (8, 6), (0, 5), (5, 0)])) + c
        d = abs(p - c); need(abs(d - r) > 0.5); val = d + r if t == 'm_far' else abs(d - r); need(abs(val - round(val)) < 1e-9)
        return dict(q=f'z moves on |z − ({cstr(c)})| = {r}. The {"greatest" if t == "m_far" else "least"} value of |z − ({cstr(p)})| is ____.', o=None, a=round(val),
                    sol=['Distance between the centre and the point, then add (or subtract) the radius.', f'd = {nf(d)} → {round(val)}.'], p=dict(t=t, c=[c.real, c.imag], r=r, p=[p.real, p.imag]))
    if t == 'm_line':
        cx, cy, r, k = rng.randint(-3, 3), rng.randint(-3, 3), rng.choice([2, 3, 4, 5]), rng.randint(-3, 5)   # line x + y = k
        A, B, C = 2, -2 * cx - 2 * (k - cy), cx * cx + (k - cy) ** 2 - r * r   # in x: (x − cx)² + (k − x − cy)² = r²
        need(B * B - 4 * A * C > 0); S1, S2 = F(-B, A), F(C, A)   # Σx, Πx
        val = 2 * (S1 * S1 - 2 * S2) - 2 * k * S1 + 2 * k * k   # Σ(x² + (k − x)²)
        need(val.denominator == 1)
        return dict(q=f'S is where |z − ({cstr(complex(cx, cy))})| = {r} meets Re z + Im z = {k}. Then Σ_{{z∈S}}|z|^{{2}} = ____.', o=None, a=int(val),
                    sol=['Put y = k − x into the circle → a quadratic in x; use the sum and product of its roots.', f'Σ(2x^{{2}} − 2kx + k^{{2}}) = {val}.'], p=dict(t=t, cx=cx, cy=cy, r=r, k=k))
    if t == 'm_lat':
        c, r = complex(rng.randint(-2, 2), rng.randint(-2, 2)), rng.choice([1, 2]); cond = rng.choice(['y ≤ x', 'y ≥ 0', 'none'])
        pts = [complex(a, b) for a in range(-6, 7) for b in range(-6, 7) if abs(complex(a, b) - c) <= r + 1e-9 and (cond == 'none' or (cond == 'y ≤ x' and b <= a) or (cond == 'y ≥ 0' and b >= 0))]
        val = sum(round(abs(z) ** 2) for z in pts); extra = {'y ≤ x': ', Im z ≤ Re z', 'y ≥ 0': ', Im z ≥ 0', 'none': ''}[cond]
        return dict(q=f'The sum of |z|^{{2}} over all z = a + ib with a, b integers, |z − ({cstr(c)})| ≤ {r}{extra} is ____.', o=None, a=val,
                    sol=['List the lattice points in the disc that satisfy the condition.', f'{len(pts)} points → Σ|z|^{{2}} = {val}.'], p=dict(t=t, c=[c.real, c.imag], r=r, cond=cond))
    if t == 'm_arg':
        cx, r = rng.choice([(5, 3), (13, 5), (10, 6), (5, 4), (17, 8), (25, 7)]); val = cx * cx - r * r
        return dict(q=f'Among all z with |z − {cx}| ≤ {r}, the one with the largest argument is z_{{0}}. Then |z_{{0}}|^{{2}} = ____.', o=None, a=val,
                    sol=['The largest argument is where the tangent from O touches the circle.', f'Tangent length^{{2}} = {cx}^{{2}} − {r}^{{2}} = {val}.'], p=dict(t=t, cx=cx, r=r))
    c1, c2 = complex(rng.randint(-3, 3), rng.randint(-3, 3)), complex(*rng.choice([(3, 4), (6, 8), (5, 12), (8, 15)])); c2 += c1; r = rng.choice([1, 2, 3, 4]); d = abs(c2 - c1)
    ask = rng.choice(['max', 'min']); val = d + 2 * r if ask == 'max' else max(d - 2 * r, 0); need(d > 2 * r or ask == 'max'); need(abs(val - round(val)) < 1e-9)
    return dict(q=f'z_{{1}} moves on |z − ({cstr(c1)})| = {r} and z_{{2}} on |z − ({cstr(c2)})| = {r}. The {"greatest" if ask == "max" else "least"} value of |z_{{1}} − z_{{2}}| is ____.', o=None, a=round(val),
                sol=['Work along the line of centres.', f'd = {nf(d)} → {round(val)}.'], p=dict(t='m_two', c1=[c1.real, c1.imag], c2=[c2.real, c2.imag], r=r, ask=ask))

def g_calg(rng):
    t = rng.choice(['a_pow', 'a_pow', 'a_sum', 'a_sum', 'a_omega', 'a_prod', 'a_count', 'a_quot', 'a_quot', 'a_quot'])
    if t == 'a_pow':
        k, n, m = rng.choice([1, 2, 3, 4, 5]), rng.randint(5, 250), rng.choice([2, 4, 8]); w = cmath.exp(1j * math.pi * k / 6) ** n; sh = rng.choice([1j, -1j, 1, -1])
        val = (w - sh) ** m; need(abs(val.imag) < 1e-6 and abs(val.real - round(val.real)) < 1e-6)
        right = str(round(val.real)); o, a = mcq(rng, right, [str(x) for x in (-round(val.real), round(val.real) * 2, 0, 1, -1, 2 ** m) if str(x) != right])
        return dict(q=f'z = cos\\f{{{k}π}}{{6}} + i sin\\f{{{k}π}}{{6}}. Then (z^{{{n}}} − ({cstr(complex(sh))}))^{{{m}}} =', o=o, a=a,
                    sol=[f'z^{{{n}}} = e^{{i{n * k}π/6}} — reduce the angle mod 2π.', f'Result = {right}.'], p=dict(t=t, k=k, n=n, m=m, sh=[complex(sh).real, complex(sh).imag]))
    if t == 'a_sum':
        b, c, w = complex(rng.randint(-4, 4), rng.randint(-2, 2)), complex(rng.randint(-8, 16), 0), complex(0, rng.choice([1, 2, 3]))
        rs = qroots(1, b, c); val = sum(abs(z + w) ** 2 for z in rs); need(abs(val - round(val)) < 1e-6)
        return dict(q=f'S = {{z : z^{{2}} + ({cstr(b)})z + {cstr(c)} = 0}}. Then Σ_{{z∈S}}|z + {cstr(w)}|^{{2}} = ____.', o=None, a=round(val),
                    sol=['Solve the quadratic, then add the two squared moduli.', f'= {round(val)}.'], p=dict(t=t, b=[b.real, b.imag], c=c.real, w=w.imag))
    if t == 'a_omega':
        tgt = rng.choice([8, 14, 20, 26, 32, 38]); ns = [n for n in range(1, 60) if sum((2 if k % 3 == 0 else -1) ** 2 for k in range(1, n + 1)) == tgt]; need(ns)
        return dict(q=f'ω is a non-real cube root of 1. If Σ_{{k=1}}^{{n}}(ω^{{k}} + ω^{{−k}})^{{2}} = {tgt}, then n = ____.', o=None, a=ns[0],
                    sol=['ω^{k} + ω^{−k} = 2 if 3 | k, else −1 → squares 1, 1, 4, 1, 1, 4, …', f'n = {ns[0]}.'], p=dict(t=t, tgt=tgt))
    if t == 'a_prod':
        n = rng.randint(2, 7); val = round(abs(math.prod(complex(1, k) for k in range(1, n + 1))) ** 2)
        return dict(q=f'z = (1 + i)(1 + 2i)…(1 + ni). If |z|^{{2}} = {val}, then n = ____.', o=None, a=n, sol=['|z|^{2} = Π(1 + k^{2}).', f'2 × 5 × 10 × … → n = {n}.'], p=dict(t=t, val=val))
    if t == 'a_count':
        m, c = rng.choice([1, 2, 3]), rng.choice(['1', '√{2}', '√{3}', '0']); cv = {'1': 1, '√{2}': math.sqrt(2), '√{3}': math.sqrt(3), '0': 0}[c]
        cnt = 8 * m if cv > 0 else 4 * m
        return dict(q=f'The number of complex z with |z| = 1 and |\\f{{z^{{{m}}}}}{{z̄^{{{m}}}}} + \\f{{z̄^{{{m}}}}}{{z^{{{m}}}}}| = {c} is ____.', o=None, a=cnt,
                    sol=[f'z = e^{{iθ}}: the expression is 2cos{2 * m}θ.', f'Solve |2cos{2 * m}θ| = {c} on [0, 2π) → {cnt} solutions.'], p=dict(t=t, m=m, c=c))
    a, b = complex(rng.randint(-3, 3), rng.randint(-3, 3)), complex(rng.randint(1, 4), rng.randint(-3, 3)); c = complex(rng.randint(-3, 3), rng.randint(-3, 3))   # (z² + c)/(z − a) = b
    rs = qroots(1, -b, c + a * b); val = sum(z * z for z in rs); need(val.real == int(val.real) and val.imag == int(val.imag))
    right = cstr(val); o, an = mcq(rng, right, [cstr(x) for x in (val.conjugate(), -val, -val.conjugate(), val + 1)])
    return dict(q=f'\\f{{z^{{2}} + ({cstr(c)})}}{{z − ({cstr(a)})}} = {cstr(b)}. The sum of all possible values of z^{{2}} is', o=o, a=an,
                sol=['Clear the fraction: z^{2} − bz + (c + ab) = 0.', f'Σz^{{2}} = b^{{2}} − 2(c + ab) = {right}.'], p=dict(t='a_quot', a=[a.real, a.imag], b=[b.real, b.imag], c=[c.real, c.imag]))

def g_quad(rng):
    t = rng.choice(['q_pow', 'q_new', 'q_rec', 'q_ratio', 'q_eq', 'q_sym'])
    s, p = rng.randint(-5, 5), rng.choice([x for x in range(-6, 7) if x])
    if t == 'q_pow':
        n = rng.choice([3, 4, 5, 6]); a, b = qroots(1, -s, p); val = (a ** n + b ** n).real; need(abs(val) < 1e6)
        return dict(q=f'α, β are the roots of x^{{2}} {"−" if s >= 0 else "+"} {abs(s)}x {"+" if p > 0 else "−"} {abs(p)} = 0. Then α^{{{n}}} + β^{{{n}}} = ____.', o=None, a=round(val),
                    sol=['Use P_{k} = sP_{k−1} − pP_{k−2} with P_{0} = 2, P_{1} = s.', f'= {round(val)}.'], p=dict(t=t, s=s, pp=p, n=n))
    if t == 'q_new':
        k = rng.choice([2, 3]); a, b = qroots(1, -s, p); S, Pr = (a ** k + b ** k).real, (a ** k * b ** k).real
        right = f'x^{{2}} − {round(S)}x + {round(Pr)} = 0'.replace('− -', '+ ').replace('+ -', '− '); wr = [f'x^{{2}} − {round(x)}x + {round(y)} = 0'.replace('− -', '+ ').replace('+ -', '− ') for x, y in ((-S, Pr), (S, -Pr), (S + 1, Pr), (S, Pr + 1))]
        o, an = mcq(rng, right, wr)
        return dict(q=f'α, β are the roots of x^{{2}} {"−" if s >= 0 else "+"} {abs(s)}x {"+" if p > 0 else "−"} {abs(p)} = 0. The equation with roots α^{{{k}}} and β^{{{k}}} is', o=o, a=an,
                    sol=['New sum α^{k} + β^{k}, new product (αβ)^{k}.', f'→ {right}.'], p=dict(t=t, s=s, pp=p, k=k))
    if t == 'q_rec':
        n = rng.choice([6, 8, 10, 12]); a, b = qroots(1, -s, p); Pn = lambda m: (a ** m + b ** m).real; need(abs(Pn(n - 2)) > 1e-9)
        val = (Pn(n) - s * Pn(n - 1)) / Pn(n - 2)
        return dict(q=f'α, β are the roots of x^{{2}} {"−" if s >= 0 else "+"} {abs(s)}x {"+" if p > 0 else "−"} {abs(p)} = 0 and P_{{n}} = α^{{n}} + β^{{n}}. Then \\f{{P_{{{n}}} − {s}P_{{{n - 1}}}}}{{P_{{{n - 2}}}}} = ____.'.replace('− -', '+ '), o=None, a=round(val),
                    sol=['α^{2} = sα − p (same for β) → P_{n} = sP_{n−1} − pP_{n−2}.', f'Ratio = −p = {round(val)}.'], p=dict(t=t, s=s, pp=p, n=n))
    if t == 'q_ratio':
        r, k = rng.choice([1, 2, 3, -1, -2]), rng.choice([2, 3])   # roots r and k·r of x² − (1+k)r x + k r² → a·(x² …)
        A = rng.choice([1, 2, 3]); B = -A * (1 + k) * r; C = A * k * r * r; val = k * B * B / (A * C) if C else 0   # (1 + k)² / k = B²/(AC)
        need(C != 0); frac = F(B * B, A * C)
        right = str(F((1 + k) ** 2, k)); o, an = mcq(rng, right, [str(x) for x in (F(k * k, 1 + k), F(1 + k, k), F((1 + k) ** 2, k * k), F(k, 1))])
        return dict(q=f'One root of ax^{{2}} + bx + c = 0 is {k} times the other. Then \\f{{b^{{2}}}}{{ac}} =', o=o, a=an,
                    sol=['Roots r, kr: sum (1 + k)r = −\\f{b}{a}, product kr^{2} = \\f{c}{a}.', f'\\f{{b^{{2}}}}{{ac}} = \\f{{(1 + k)^{{2}}}}{{k}} = {right}.'], p=dict(t=t, k=k, A=A, r=r))
    if t == 'q_eq':
        a_, c_ = rng.choice([(3, 12), (6, 9), (4, 12), (9, 6), (2, 8), (8, 2), (5, 20)]); S = a_ + c_; b_ = F(2 * a_ * c_, S)   # a(b − c)x² + b(c − a)x + c(a − b) with equal roots
        val = a_ * a_ + c_ * c_
        return dict(q=f'a(b − c)x^{{2}} + b(c − a)x + c(a − b) = 0 has equal roots, a + c = {S} and b = {b_}. Then a^{{2}} + c^{{2}} = ____.', o=None, a=val,
                    sol=['x = 1 is a root (coefficients add to 0); equal roots → product 1 → b = \\f{2ac}{a + c}.', f'ac = \\f{{b(a + c)}}{{2}} = {a_ * c_} → a^{{2}} + c^{{2}} = {S}^{{2}} − 2 × {a_ * c_} = {val}.'], p=dict(t=t, S=S, b=[b_.numerator, b_.denominator], ac=a_ * c_))
    A = rng.choice([1, 2]); k = rng.randint(1, 4); a, b = qroots(A, k, -1)   # A x² + k x − 1, ask α⁴ + β⁴ form
    val = (a ** 4 + b ** 4).real; fr = F(val).limit_denominator(64); need(abs(float(fr) - val) < 1e-9)
    right = str(fr); o, an = mcq(rng, right, [str(x) for x in (fr + 1, fr - F(1, 2), fr * 2, -fr)])
    return dict(q=f'α, β are the roots of {A if A > 1 else ""}x^{{2}} + {k}x − 1 = 0. Then α^{{4}} + β^{{4}} =', o=o, a=an,
                sol=['α^{2} + β^{2} = s^{2} − 2p, then α^{4} + β^{4} = (α^{2} + β^{2})^{2} − 2p^{2}.', f'= {right}.'], p=dict(t='q_sym', A=A, k=k))

def g_qloc(rng):
    t = rng.choice(['l_abs', 'l_red', 'l_sign'])
    if t == 'l_abs':
        a, b, c, d = rng.choice([1, 2, 3]), rng.choice([1, 2, 3, 4]), rng.choice([0, 1, 2, 3]), rng.choice([-5, -1, 1, 2, 5])
        f = lambda x: x * abs(x - a) + b * abs(x - c) + d; xs = grid(-60, 60, 240001); cnt = sum(1 for u, v in zip(xs, xs[1:]) if f(u) * f(v) < 0); need(all(abs(f(x)) > 1e-6 for x in xs[::400]))
        return dict(q=f'The number of real roots of x|x − {a}| + {b}|x − {c}| {"+" if d > 0 else "−"} {abs(d)} = 0 is ____.'.replace('|x − 0|', '|x|'), o=None, a=cnt,
                    sol=['Split at the corner points and solve the quadratic on each piece, keeping roots inside it.', f'Total {cnt}.'], p=dict(t=t, a=a, b=b, c=c, d=d))
    if t == 'l_red':
        s = rng.choice([5, 7, 9, 11]); r1, r2 = rng.sample([x for x in range(-2, 12)], 2); need(r1 + r2 == s or True)
        # (x² − s x + k)² − (x² − s x + m) = n with a nice factorisation: u = x² − s x + k → u² − u − (m − k) − n = 0
        k = rng.randint(1, 12); u1, u2 = rng.sample(range(-6, 8), 2); need(u1 + u2 == 1)   # u² − u − u1u2·(−1)…: roots u1, u2 with sum 1
        m_n = -u1 * u2   # u² − u + u1u2 = 0 ⇒ (m − k) + n = −u1u2
        m = k + rng.randint(1, 9); n = m_n - (m - k)
        rat = [x for x in range(-60, 61) if (x * x - s * x + k) ** 2 - (x * x - s * x + m) == n]; need(rat); val = math.prod(rat)
        return dict(q=f'The product of all rational roots of (x^{{2}} − {s}x + {k})^{{2}} − (x^{{2}} − {s}x + {m}) = {n} is ____.'.replace('= -', '= −'), o=None, a=val,
                    sol=[f'Put u = x^{{2}} − {s}x + {k}: u^{{2}} − u − {m - k} = {n} → u = {u1} or {u2}.', f'Keep the equations with rational roots → product {val}.'], p=dict(t=t, s=s, k=k, m=m, n=n))
    kind = rng.choice(['positive', 'negative']); c1, c2 = rng.choice([(2, 9), (2, 5), (3, 7), (1, 4)])   # x² − (p + c1)x + (c1 p + c2): roots sign interval
    ok = lambda p: all(abs(r.imag) < 1e-12 and (r.real > 0 if kind == 'positive' else r.real < 0) for r in qroots(1, -(p + c1), c1 * p + c2))
    ps = [p for p in grid(-30, 30, 120001) if ok(p)]; need(ps); lo, hi = min(ps), max(ps); need(hi < 29)
    val = round(lo + hi, 2); need(abs(val * 4 - round(val * 4)) < 1e-6)
    return dict(q=f'All p for which both roots of x^{{2}} − (p + {c1})x + ({c1}p + {c2}) = 0 are {kind} reals form an interval with end points a < b. a + b ≈ ____ (nearest integer).', o=None, a=round(val),
                sol=['Need discriminant ≥ 0 and the right signs for the sum and the product.', f'a + b ≈ {nf(val, 4)}.'], p=dict(t='l_sign', kind=kind, c1=c1, c2=c2)) if abs(val - round(val)) > 0.03 and abs(val % 1 - 0.5) > 0.03 or abs(val - round(val)) < 1e-6 else g_qloc(rng)

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, RecursionError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(cmod=g_cmod, calg=g_calg, quad=g_quad, qloc=g_qloc).items()}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('m_far', 'm_near'):
        c, pt = complex(*p['c']), complex(*p['p']); v = [abs(z - pt) for z in circle(c, p['r'])]; return abs(Rv - (max(v) if t == 'm_far' else min(v))) < 1e-3
    if t == 'm_line':
        c = complex(p['cx'], p['cy']); xs = grid(-20.0000371, 20.0000213, 400001); f = lambda x: abs(complex(x, p['k'] - x) - c) - p['r']
        roots = [(u + v) / 2 for u, v in zip(xs, xs[1:]) if f(u) * f(v) < 0]; return abs(Rv - sum(abs(complex(x, p['k'] - x)) ** 2 for x in roots)) < 0.01
    if t == 'm_lat':
        c = complex(*p['c']); tot = 0
        for a in range(-8, 9):
            for b in range(-8, 9):
                z = complex(a, b)
                if abs(z - c) <= p['r'] + 1e-9 and {'none': True, 'y ≤ x': b <= a, 'y ≥ 0': b >= 0}[p['cond']]: tot += a * a + b * b
        return Rv == tot
    if t == 'm_arg':
        z = max(circle(p['cx'], p['r'], 360000), key=cmath.phase); return abs(Rv - abs(z) ** 2) < 0.01
    if t == 'm_two':
        A = circle(complex(*p['c1']), p['r'], 720); B = circle(complex(*p['c2']), p['r'], 720)
        d = abs(complex(*p['c1']) - complex(*p['c2'])); far = max(abs(a - complex(*p['c2'])) for a in A) + p['r']; near_ = max(min(abs(a - complex(*p['c2'])) for a in A) - p['r'], 0)
        return abs(Rv - (far if p['ask'] == 'max' else near_)) < 0.01
    if t == 'a_pow':
        z = 1
        for _ in range(p['n']): z *= cmath.exp(1j * math.pi * p['k'] / 6)
        v = (z - complex(*p['sh'])) ** p['m']; return abs(float(Rv) - v.real) < 1e-6 and abs(v.imag) < 1e-6
    if t == 'a_sum':
        b = complex(*p['b']); rs = qroots(1, b, p['c']); return all(abs(z * z + b * z + p['c']) < 1e-9 for z in rs) and Rv == round(sum(abs(z + 1j * p['w']) ** 2 for z in rs))
    if t == 'a_omega':
        w = cmath.exp(2j * math.pi / 3); tot = 0
        for n in range(1, 80):
            tot += (w ** n + w ** -n) ** 2
            if abs(tot - p['tgt']) < 1e-9: return Rv == n
        return False
    if t == 'a_prod':
        z = 1
        for n in range(1, 30):
            z *= complex(1, n)
            if round(abs(z) ** 2) == p['val']: return Rv == n
        return False
    if t == 'a_count':
        cv = {'1': 1, '√{2}': math.sqrt(2), '√{3}': math.sqrt(3), '0': 0}[p['c']]; m = p['m']; N = 72000; th0 = 0.0000123
        def e(th): z = cmath.exp(1j * th); return (z ** m / z.conjugate() ** m + z.conjugate() ** m / z ** m).real   # real, signed
        g = [e(th0 + 2 * math.pi * i / N) for i in range(N + 1)]
        h = [x * x - cv * cv for x in g] if cv > 0 else g
        return Rv == sum(1 for u, v in zip(h, h[1:]) if u * v < 0)
    if t == 'a_quot':
        a, b, c = complex(*p['a']), complex(*p['b']), complex(*p['c']); rs = qroots(1, -b, c + a * b)
        ok = all(abs((z * z + c) / (z - a) - b) < 1e-9 for z in rs if abs(z - a) > 1e-9); return ok and abs(cnum(Rv) - sum(z * z for z in rs if abs(z - a) > 1e-9)) < 1e-9
    if t == 'q_pow':
        a, b = qroots(1, -p['s'], p['pp']); return Rv == round((a ** p['n'] + b ** p['n']).real)
    if t == 'q_new':
        a, b = qroots(1, -p['s'], p['pp']); k = p['k']; x1, x2 = a ** k, b ** k
        st = Rv.replace(' = 0', '').replace('x^{2}', '').replace('−', '-').replace(' ', ''); coef = st.split('x'); B = -float(coef[0]) if coef[0] not in ('', '+', '-') else 0; C = float(coef[1])
        return abs((x1 + x2).real - B) < 1e-6 and abs((x1 * x2).real - C) < 1e-6
    if t == 'q_rec':
        a, b = qroots(1, -p['s'], p['pp']); P_ = lambda m: (a ** m + b ** m).real; n = p['n']; return abs(Rv - (P_(n) - p['s'] * P_(n - 1)) / P_(n - 2)) < 1e-6
    if t == 'q_ratio':
        k, A, r = p['k'], p['A'], p['r']; B = -A * (1 + k) * r; C = A * k * r * r; rs = qroots(A, B, C)
        ok = abs(rs[0] / rs[1] - k) < 1e-9 or abs(rs[1] / rs[0] - k) < 1e-9; return ok and F(Rv) == F(B * B, A * C)
    if t == 'q_eq':
        b = F(*p['b']); S = p['S']; a = next(x for x in [F(i, 2) for i in range(1, 2 * S)] if abs(x * (S - x) - p['ac']) < 1e-12)   # a, c from sum and product
        c = S - a; A2, B2, C2 = a * (b - c), b * (c - a), c * (a - b); return B2 * B2 - 4 * A2 * C2 == 0 and Rv == a * a + c * c
    if t == 'q_sym':
        a, b = qroots(p['A'], p['k'], -1); return abs(float(F(Rv)) - (a ** 4 + b ** 4).real) < 1e-9
    if t == 'l_abs':
        f = lambda x: x * abs(x - p['a']) + p['b'] * abs(x - p['c']) + p['d']; xs = grid(-80, 80, 320001); return Rv == sum(1 for u, v in zip(xs, xs[1:]) if f(u) * f(v) < 0)
    if t == 'l_red':
        rs = [x for x in range(-100, 101) if (x * x - p['s'] * x + p['k']) ** 2 - (x * x - p['s'] * x + p['m']) == p['n']]; return Rv == math.prod(rs)
    if t == 'l_sign':
        ok = lambda q: all(abs(r.imag) < 1e-12 and (r.real > 0 if p['kind'] == 'positive' else r.real < 0) for r in qroots(1, -(q + p['c1']), p['c1'] * q + p['c2']))
        ps = [q for q in grid(-30, 30, 240001) if ok(q)]; return Rv == round(min(ps) + max(ps))
    raise KeyError(t)
