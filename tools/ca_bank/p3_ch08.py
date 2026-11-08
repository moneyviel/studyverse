"""Paper 3 Ch 8 — Differential and Integral Calculus: extra MCQ templates (answers computed exactly)."""
from common import *
import math

U = 'fnd-p3-ch08-u01'
C1, C2, C3, C4, C5 = 'The derivative and the first principle', 'Standard derivatives', 'Rules of differentiation', 'Implicit, parametric and logarithmic differentiation', 'Second derivative and the gradient of a curve'
C6, C7, C8, C9, C10 = 'Applications: cost, revenue, profit, break-even and propensities', 'Integration — the reverse of differentiation', 'Methods of integration', 'Definite integrals and their properties', 'From marginal functions back to totals'


def pval(c, x): return sum(F(k) * F(x) ** (len(c) - 1 - i) for i, k in enumerate(c))


def pder(c):
    n = len(c) - 1; return [k * (n - i) for i, k in enumerate(c[:-1])] or [0]


def pint(c):
    n = len(c) - 1; return [F(k, n - i + 1) for i, k in enumerate(c)] + [0]


def rnd_poly(r, deg):
    c = [r.randint(1, 6) * r.choice([1, -1])] + [r.randint(-9, 9) for _ in range(deg)]
    return c


def deriv_at(r):
    c = rnd_poly(r, r.choice([3, 4])); x0 = r.randint(-3, 3)
    v = pval(pder(c), x0)
    return dict(q=f'If y = {poly(c)}, then dy/dx at x = {x0} is:', a=fr(v), w=[fr(pval(c, x0)), fr(pval(pder(pder(c)), x0)), fr(v + c[-2] if c[-2] else v + 1), fr(-v) if v else '1'],
                ex=f'Differentiate term by term with d/dx(xⁿ) = n·xⁿ⁻¹ (the constant vanishes): dy/dx = {poly(pder(c))}. At x = {x0} this is {fr(v)}. Putting x = {x0} into y itself gives {fr(pval(c, x0))}, which is the height of the curve, not its slope.',
                fast='Power rule: bring the power down, reduce it by one, then substitute.', secs=35, d='core', topic=C2, check=frx(v), k='ch08.der', data={'y': poly(c), 'x0': x0})


def product(r):
    a, b, c, d_ = r.randint(1, 6), r.randint(-8, 8), r.randint(1, 5), r.randint(-9, 9); x0 = r.randint(-3, 4)
    u, v = [a, b], [c, 0, d_]
    val = pval(pder(u), x0) * pval(v, x0) + pval(u, x0) * pval(pder(v), x0)
    wrong = pval(pder(u), x0) * pval(pder(v), x0)
    return dict(q=f'If y = ({poly(u)})({poly(v)}), then dy/dx at x = {x0} is:', a=fr(val), w=[fr(wrong), fr(pval(u, x0) * pval(v, x0)), fr(val + pval(u, x0)), fr(-val) if val else '1'],
                ex=f'Product rule: d(uv)/dx = u′v + uv′ with u = {poly(u)} (u′ = {a}) and v = {poly(v)} (v′ = {2 * c}x). At x = {x0}: u = {fr(pval(u, x0))}, v = {fr(pval(v, x0))}, v′ = {2 * c * x0}. So dy/dx = {a} × {fr(pval(v, x0))} + {fr(pval(u, x0))} × {2 * c * x0} = {fr(val)}. Multiplying the two derivatives (u′v′) is wrong.',
                fast='Or expand the product into one polynomial first, then differentiate and substitute.', secs=45, d='moderate', topic=C3, check=frx(val), k='ch08.prod', data={'u': poly(u), 'v': poly(v), 'x0': x0})


def quotient(r):
    a, b, c, d_ = r.randint(1, 7), r.randint(-9, 9), r.randint(1, 5), r.randint(-9, 9); x0 = r.randint(-2, 4)
    if a * d_ - b * c == 0 or c * x0 + d_ == 0: return None
    val = F(a * d_ - b * c, (c * x0 + d_) ** 2)
    return dict(q=f'If y = ({poly([a, b])})/({poly([c, d_])}), then dy/dx at x = {x0} is:', a=fr(val), w=[fr(-val), fr(F(a * d_ - b * c, c * x0 + d_)), fr(F(a, c)), fr(F(b * c - a * d_ + 1, (c * x0 + d_) ** 2)) if F(b * c - a * d_ + 1, (c * x0 + d_) ** 2) != val else fr(val * 2)],
                ex=f'Quotient rule: d(u/v)/dx = (v·u′ − u·v′)/v². Here u′ = {a}, v′ = {c}, so the numerator is ({poly([c, d_])})({a}) − ({poly([a, b])})({c}) = {a * d_ - b * c} (the x-terms cancel). Hence dy/dx = {a * d_ - b * c}/({poly([c, d_])})²; at x = {x0} the denominator is {(c * x0 + d_) ** 2}, giving {fr(val)}. Reversing the order in the numerator flips the sign.',
                fast='For (ax + b)/(cx + d), dy/dx = (ad − bc)/(cx + d)² directly.', secs=40, d='moderate', topic=C3, check=frx(val), k='ch08.quot', data={'u': poly([a, b]), 'v': poly([c, d_]), 'x0': x0})


def chain(r):
    a, b, n = r.randint(1, 4), r.randint(-5, 6), r.randint(2, 5); x0 = r.choice([-2, -1, 1, 2])
    inner = a * x0 * x0 + b
    val = n * inner ** (n - 1) * 2 * a * x0
    if abs(val) > 10 ** 7: return None
    return dict(q=f'If y = ({poly([a, 0, b])}){sup(n)}, then dy/dx at x = {x0} is:', a=inr(val), w=[inr(n * inner ** (n - 1)), inr(val // (2 * x0) if x0 else val + 1), inr(n * inner ** (n - 1) * 2 * a), inr(inner ** n)],
                ex=f'Chain rule: dy/dx = n(inner)ⁿ⁻¹ × d(inner)/dx = {n}({poly([a, 0, b])}){sup(n - 1)} × {2 * a}x. At x = {x0} the inner function is {inner}, so dy/dx = {n} × {inner}{sup(n - 1)} × {2 * a * x0} = {inr(val)}. Forgetting to multiply by the derivative of the inner function ({2 * a}x) gives {inr(n * inner ** (n - 1))}.',
                fast='Outer derivative × inner derivative, then substitute.', secs=40, d='moderate', topic=C3, check=str(val), k='ch08.chain', data={'a': a, 'b': b, 'n': n, 'x0': x0})


def log_der(r):
    a, b = r.randint(1, 9), r.randint(1, 15); x0 = r.randint(0, 6); k = r.randint(1, 5)
    kind = r.choice(['log', 'exp'])
    if kind == 'log':
        val = F(a, a * x0 + b)
        return dict(q=f'If y = log ({poly([a, b])}) (natural log), then dy/dx at x = {x0} is:', a=fr(val), w=[fr(F(1, a * x0 + b)), fr(F(a * x0 + b, a)), fr(F(a)), fr(F(a, (a * x0 + b) ** 2))],
                    ex=f'd/dx[log u] = (1/u) × du/dx. With u = {poly([a, b])}, du/dx = {a}, so dy/dx = {a}/({poly([a, b])}). At x = {x0}: {a}/{a * x0 + b} = {fr(val)}. Forgetting the factor du/dx = {a} gives 1/{a * x0 + b}.',
                    fast='log of a linear function: derivative = (coefficient of x) ÷ (the linear expression).', secs=25, d='core', topic=C2, check=frx(val), k='ch08.logd', data={'a': a, 'b': b, 'x0': x0})
    val = k * (k * 0 + 1) + 2 * a * 0  # y = x·e^(kx) + a x² at x = 0 -> e^0(1 + 0) = 1 ... use y = e^(kx)(x + a): dy/dx = e^(kx)(k(x + a) + 1); at x = 0 → k a + 1
    val = k * a + 1
    return dict(q=f'If y = e^({k}x) × (x + {a}), then dy/dx at x = 0 is:', a=str(val), w=[str(k * a), str(k + a), str(a + 1), str(k)],
                ex=f'Product rule with d/dx(e^({k}x)) = {k}e^({k}x): dy/dx = {k}e^({k}x)(x + {a}) + e^({k}x) × 1 = e^({k}x)[{k}(x + {a}) + 1]. At x = 0, e⁰ = 1, so dy/dx = {k} × {a} + 1 = {val}. Dropping the second term of the product rule gives {k * a}.',
                fast='At x = 0 every e^(kx) is 1: just evaluate k(x + a) + 1.', secs=35, d='moderate', topic=C3, check=str(val), k='ch08.expd', data={'k': k, 'a': a})


def implicit(r):
    kind = r.choice(['circle', 'hyper'])
    if kind == 'circle':
        trip = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)])
        x0, y0 = r.choice([(trip[0], trip[1]), (trip[1], trip[0]), (-trip[0], trip[1]), (trip[0], -trip[1])]); R2 = trip[2] ** 2
        val = F(-x0, y0)
        return dict(q=f'If x² + y² = {R2}, then dy/dx at the point ({x0}, {y0}) is:', a=fr(val), w=[fr(-val), fr(F(y0, x0)), fr(F(-y0, x0)) if F(-y0, x0) != val else fr(val + 1), fr(F(x0, 2 * y0))],
                    ex=f'Differentiate both sides with respect to x, treating y as a function of x: 2x + 2y·dy/dx = 0, so dy/dx = −x/y. At ({x0}, {y0}): −({x0})/({y0}) = {fr(val)}. Forgetting the dy/dx attached to the y-term is the common implicit-differentiation error.',
                    fast='For x² + y² = r², slope = −x/y at the point.', secs=30, d='moderate', topic=C4, check=frx(val), k='ch08.impl', data={'R2': R2, 'x0': x0, 'y0': y0, 'kind': 'circle'})
    c = r.choice([6, 8, 10, 12, 18, 24, 36]); x0 = r.choice([x for x in range(1, 13) if c % x == 0]); y0 = c // x0
    val = F(-y0, x0)
    return dict(q=f'If xy = {c}, then dy/dx at the point ({x0}, {y0}) is:', a=fr(val), w=[fr(-val), fr(F(-x0, y0)) if F(-x0, y0) != val else fr(val - 1), fr(F(y0, x0 * x0)), fr(F(c))],
                ex=f'Differentiate xy = {c} using the product rule: x·dy/dx + y = 0, so dy/dx = −y/x. At ({x0}, {y0}): −{y0}/{x0} = {fr(val)}. Equivalently y = {c}/x and dy/dx = −{c}/x² = −{c}/{x0 * x0}.',
                fast='xy = c ⇒ dy/dx = −y/x (or −c/x²).', secs=25, d='moderate', topic=C4, check=frx(val), k='ch08.impl', data={'c': c, 'x0': x0, 'y0': y0, 'kind': 'hyper'})


def parametric(r):
    a = r.randint(1, 6); t = r.choice([-3, -2, -1, 1, 2, 3, 4, F(1, 2)])
    val = 1 / F(t)
    ts = fr(t)
    return dict(q=f'If x = {a}t² and y = {2 * a}t, then dy/dx at t = {ts} is:', a=fr(val), w=[fr(F(t)), fr(2 * F(t)), fr(-val), fr(F(1, 2) / F(t))],
                ex=f'For parametric equations, dy/dx = (dy/dt)/(dx/dt). Here dy/dt = {2 * a} and dx/dt = {2 * a}t, so dy/dx = {2 * a}/({2 * a}t) = 1/t. At t = {ts}: {fr(val)}. Dividing the other way round gives t. This curve is the parabola y² = {4 * a}x written in parametric form.',
                fast='dy/dx = (dy/dt) ÷ (dx/dt) = 1/t for this standard parabola.', secs=25, d='moderate', topic=C4, check=frx(val), k='ch08.param', data={'a': a, 't': ts})


def second(r):
    c = rnd_poly(r, r.choice([3, 4])); x0 = r.randint(-3, 3)
    v = pval(pder(pder(c)), x0)
    return dict(q=f'If y = {poly(c)}, then d²y/dx² at x = {x0} is:', a=fr(v), w=[fr(pval(pder(c), x0)), fr(pval(pder(pder(pder(c))), x0)) if len(c) > 3 else fr(v + 2), fr(v + 2 * c[-3] if len(c) > 2 else v + 1), fr(-v) if v else '2'],
                ex=f'Differentiate twice. dy/dx = {poly(pder(c))}; d²y/dx² = {poly(pder(pder(c)))}. At x = {x0}: {fr(v)}. The second derivative measures how the slope changes; a positive value means the curve is bending upwards (a possible minimum).',
                fast='Differentiate twice term by term; linear and constant terms vanish in d²y/dx².', secs=35, d='core', topic=C5, check=frx(v), k='ch08.second', data={'y': poly(c), 'x0': x0})


def marginal_cost(r):
    a, b, c, d_ = r.choice([F(1, 3), F(1, 2), 1, 2]), r.randint(1, 12), r.randint(5, 60), r.randint(100, 5000); x0 = r.randint(5, 40)
    C = [a, -b, c, d_]; mc = pval(pder(C), x0)
    if mc <= 0: return None
    return dict(q=f'The total cost function is C(x) = {poly(C)}. The marginal cost when x = {x0} units is:', a=rs(mc), w=[rs(pval(C, x0)), rs(pval(C, x0) / x0), rs(pval(C, x0) - pval(C, x0 - 1)), rs(mc + d_ / x0)],
                ex=f'Marginal cost is the derivative of total cost: MC = dC/dx = {poly(pder(C))}. At x = {x0}: MC = ₹{num(mc)}. The fixed cost {inr(d_)} does not affect MC. Total cost ₹{num(pval(C, x0))} and average cost ₹{num(pval(C, x0) / x0)} are different ideas.',
                fast='Differentiate C(x), drop the constant, substitute x.', secs=35, d='core', topic=C6, check=frx(mc), k='ch08.mc', data={'C': poly(C), 'x0': x0})


def profit_max(r):
    p, q_ = r.randint(40, 400), r.choice([1, 2, 3, 4, 5, F(1, 2)]); rr_, s = r.randint(5, 39), r.randint(100, 3000)
    if rr_ >= p: return None
    x = F(p - rr_) / (2 * q_)
    if x.denominator != 1: return None
    prof = p * x - q_ * x * x - rr_ * x - s
    return dict(q=f'Revenue R(x) = {poly([-q_, p, 0])} and cost C(x) = {poly([rr_, s])}. The output that maximises profit is:', a=f'{fr(x)} units',
                w=[f'{fr(F(p) / (2 * q_))} units', f'{fr(F(p - rr_) / q_)} units', f'{fr(F(p) / q_)} units', f'{fr(x + 5)} units'],
                ex=f'Profit P(x) = R − C = {poly([-q_, p - rr_, -s])}. Set dP/dx = 0: {fr(p - rr_)} − {fr(2 * q_)}x = 0, so x = {fr(x)}. d²P/dx² = −{fr(2 * q_)} < 0 confirms a maximum (profit ₹{num(prof)}). Maximising revenue alone gives {fr(F(p) / (2 * q_))} units, ignoring cost.',
                fast='Maximum profit where MR = MC: p − 2qx = r.', secs=45, d='moderate', topic=C6, check=frx(x), k='ch08.pmax', data={'R': poly([-q_, p, 0]), 'C': poly([rr_, s])})


def min_ac(r):
    a = r.choice([1, 2, 3, 4, 5]); x = r.randint(2, 30); c = a * x * x; b = r.randint(5, 80)
    acmin = 2 * a * x + b
    return dict(q=f'Total cost C(x) = {poly([a, b, c])}. Average cost is minimum when output x =', a=str(x), w=[str(x * x), str(2 * x), str(c // b) if c // b not in (x, 2 * x, x * x) else str(x + 1), str(math.isqrt(c))],
                ex=f'Average cost AC = C/x = {a if a > 1 else ""}x + {b} + {inr(c)}/x. dAC/dx = {a} − {inr(c)}/x² = 0 gives x² = {inr(c // a)}, x = {x}. The second derivative 2 × {inr(c)}/x³ is positive, so it is a minimum (AC = ₹{acmin}). Minimising total cost instead would give x = 0.',
                fast=f'Min AC at x = √(fixed cost ÷ coefficient of x²) = √({inr(c)}/{a}).', secs=45, d='moderate', topic=C6, check=str(x), k='ch08.minac', data={'C': poly([a, b, c])})


def def_int(r):
    c = rnd_poly(r, r.choice([2, 3])); a = r.randint(-2, 2); b = a + r.randint(1, 3)
    I = pint(c); v = pval(I, b) - pval(I, a)
    return dict(q=f'∫ from {a} to {b} of ({poly(c)}) dx =', a=fr(v), w=[fr(pval(I, b) + pval(I, a)), fr(pval(pder(c), b) - pval(pder(c), a)), fr(pval(c, b) - pval(c, a)), fr(pval(I, b))],
                ex=f'Integrate term by term with ∫xⁿ dx = xⁿ⁺¹/(n + 1): the antiderivative is {poly(I)}. Evaluate at the upper limit minus the lower limit: [{fr(pval(I, b))}] − [{fr(pval(I, a))}] = {fr(v)}. Adding the two values, or differentiating instead of integrating, are the usual slips.',
                fast='Antiderivative at the top limit minus at the bottom limit; when the lower limit is 0 only the top limit matters.', secs=50, d='moderate', topic=C9, check=frx(v), k='ch08.defint', data={'f': poly(c), 'a': a, 'b': b})


def total_from_mc(r):
    a, b, c = r.randint(10, 200), r.randint(1, 20), r.choice([0, F(3, 1), F(3, 2), 6]); FC = r.randint(500, 20000); N = r.randint(5, 40)
    mc = [c, b, a] if c else [b, a]
    TC = pint(mc); v = pval(TC, N) + FC
    return dict(q=f'Marginal cost is MC = {poly(mc)} and fixed cost is ₹{inr(FC)}. The total cost of producing {N} units is:', a=rs(v), w=[rs(pval(TC, N)), rs(pval(mc, N) * N + FC), rs(pval(mc, N) + FC), rs(v + FC)],
                ex=f'Total cost is the integral of MC plus the fixed cost (the constant of integration): C(x) = {poly(TC)} + {inr(FC)}. At x = {N}: C = ₹{num(pval(TC, N))} + ₹{inr(FC)} = ₹{num(v)}. Leaving out the fixed cost gives only the variable cost.',
                fast=f'Integrate MC, put x = {N}, then add the fixed cost.', secs=50, d='moderate', topic=C10, check=frx(v), k='ch08.tcmc', data={'mc': poly(mc), 'FC': FC, 'N': N})


def substitution(r):
    c, n = r.randint(1, 5), r.randint(2, 4); b = r.choice([1, 2]); k = r.choice([2, 4, 6])
    # ∫_0^b k x (x² + c)^n dx = (k/2) [(x²+c)^(n+1)/(n+1)]_0^b
    v = F(k, 2) * (F(b * b + c) ** (n + 1) - F(c) ** (n + 1)) / (n + 1)
    return dict(q=f'∫ from 0 to {b} of {k}x(x² + {c}){sup(n)} dx =', a=fr(v), w=[fr(v * 2), fr(F(k, 2) * (F(b * b + c) ** (n + 1)) / (n + 1)), fr(F(k) * (F(b * b + c) ** n - F(c) ** n) / n), fr(v / (n + 1))],
                ex=f'Substitute t = x² + {c}, so dt = 2x dx and {k}x dx = {fr(F(k, 2))} dt. The limits become t = {c} to t = {b * b + c}. Integral = {fr(F(k, 2))} × [t{sup(n + 1)}/{n + 1}] from {c} to {b * b + c} = {fr(F(k, 2))} × ({(b * b + c) ** (n + 1)} − {c ** (n + 1)})/{n + 1} = {fr(v)}. Forgetting to change the lower limit gives a larger value.',
                fast='Spot f′(x)·[f(x)]ⁿ: the integral is [f(x)]ⁿ⁺¹/(n + 1), scaled by the constant.', secs=60, d='hard', topic=C8, check=frx(v), k='ch08.subst', data={'k': k, 'c': c, 'n': n, 'b': b})


def break_even(r):
    p, v = r.randint(50, 900), r.randint(10, 600); FC = r.randint(10000, 500000)
    if v >= p: return None
    x = F(FC, p - v)
    if x.denominator != 1: return None
    return dict(q=f'A product sells at ₹{inr(p)} per unit, the variable cost is ₹{inr(v)} per unit and fixed costs are ₹{inr(FC)}. The break-even output is:', a=f'{inr(int(x))} units',
                w=[f'{inr(FC // p)} units' if FC // p != x else f'{inr(int(x) + 1)} units', f'{inr(FC // v)} units' if FC // v != x else f'{inr(int(x) + 2)} units', f'{inr(int(x) * 2)} units', f'{inr(FC // (p + v))} units'],
                ex=f'At break-even, revenue = total cost: {inr(p)}x = {inr(FC)} + {inr(v)}x. So ({inr(p)} − {inr(v)})x = {inr(FC)} and x = {inr(FC)}/{inr(p - v)} = {inr(int(x))} units. Each unit contributes ₹{inr(p - v)} towards fixed costs; dividing by the price ignores variable cost.',
                fast='Break-even units = fixed cost ÷ contribution per unit (price − variable cost).', secs=30, d='core', topic=C6, check=str(int(x)), k='ch08.be', data={'p': p, 'v': v, 'FC': FC})


BANKS = {U: [(deriv_at, 2), (product, 2), (quotient, 2), (chain, 2), (log_der, 3), (implicit, 2), (parametric, 2), (second, 2), (marginal_cost, 2), (profit_max, 2),
             (min_ac, 2), (def_int, 3), (total_from_mc, 2), (substitution, 2), (break_even, 2)]}
