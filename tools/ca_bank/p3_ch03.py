"""Paper 3 Ch 3 — Linear Inequalities: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch03-u01'
T1, T2, T3 = 'Inequalities and their rules; one-variable solution space', 'Graphing a linear inequality in two variables', 'Developing inequalities from a descriptive problem'
T4, T5, T6 = 'Common region (feasible region) and corner points', 'Optimal solution — corner point method and matrix method', 'Summary of the graphical method and unused resources'
SG = {'<': '<', '>': '>', '<=': '≤', '>=': '≥'}
FLIP = {'<': '>', '>': '<', '<=': '>=', '>=': '<='}


def lin(a, b, var=('x', 'y')):
    s = poly([a, 0], var[0]) if a else ''
    if b: s = (s + ' ' + signed(b, var[1])) if s else poly([b, 0], var[1])
    return s


def one_var(r):
    a, c = r.sample(range(-7, 8), 2); x0 = F(r.randint(-12, 12), r.choice([1, 1, 2]))
    if a == c or 0 in (a, c): return None
    b = r.randint(-20, 20); d_ = (a - c) * x0 + b
    if d_.denominator != 1: return None
    op = r.choice(['<', '>', '<=', '>='])
    # a x + b op c x + d  ->  (a-c) x op d - b  -> x op' (d-b)/(a-c)
    k = a - c; res = op if k > 0 else FLIP[op]
    ans = f'x {SG[res]} {fr(x0)}'
    w = [f'x {SG[FLIP[res]]} {fr(x0)}', f'x {SG[res]} {fr(-x0)}' if x0 else f'x {SG[res]} 1', f'x {SG[FLIP[res]]} {fr(-x0)}' if x0 else f'x {SG[FLIP[res]]} 1', f'x {SG[res]} {fr(x0 + 1)}']
    return dict(q=f'Solve: {poly([a, b])} {SG[op]} {poly([c, int(d_)])}', a=ans, w=w,
                ex=f'Collect x on the left: ({a} − ({c}))x {SG[op]} {int(d_)} − ({b}), i.e. {k}x {SG[op]} {int(d_) - b}. Dividing by {k}{" (a negative number) reverses the inequality sign" if k < 0 else " keeps the sign because it is positive"}: {ans}. Forgetting to reverse the sign when dividing by a negative number is the classic error.',
                fast=f'Test x = {fr(x0 + (1 if res in (">", ">=") else -1))} (a point on the claimed side) in the original inequality; it must be true.', secs=35, d='core', topic=T1,
                k='ch03.onevar', data={'a': a, 'b': b, 'c': c, 'd': int(d_), 'op': SG[op]})


def count_int(r):
    a = r.choice([2, 3, 4, 5]); b = r.randint(-9, 9); p = r.randint(-15, 10); q_ = p + r.randint(8, 40)
    lo_inc, hi_inc = r.choice([(True, False), (False, True), (True, True), (False, False)])
    xs = [x for x in range(-100, 101) if (a * x + b >= p if lo_inc else a * x + b > p) and (a * x + b <= q_ if hi_inc else a * x + b < q_)]
    n = len(xs)
    if n < 3: return None
    return dict(q=f'How many integers x satisfy {p} {"≤" if lo_inc else "<"} {poly([a, b])} {"≤" if hi_inc else "<"} {q_}?', a=str(n), w=[str(n + 1), str(n - 1), str(n + 2), str(q_ - p)],
                ex=f'Subtract {b} and divide every part by {a}: {fr(F(p - b, a))} {"≤" if lo_inc else "<"} x {"≤" if hi_inc else "<"} {fr(F(q_ - b, a))}. The integers in this range are {xs[0]} to {xs[-1]}, which is {n} integers. Check the end points carefully — a strict sign excludes an end point that is itself an integer.',
                fast=f'Integers from {xs[0]} to {xs[-1]}: count = {xs[-1]} − ({xs[0]}) + 1 = {n}.', secs=40, d='core', topic=T1, check=str(n),
                k='ch03.count', data={'a': a, 'b': b, 'p': p, 'q': q_, 'inc': [lo_inc, hi_inc]})


def feasible_pt(r):
    a1, b1, a2, b2 = (r.randint(1, 6) for _ in range(4))
    c1, c2 = r.randint(12, 40), r.randint(6, 30)
    # region: a1x+b1y <= c1, a2x+b2y >= c2, x,y >= 0
    ok = lambda x, y: a1 * x + b1 * y <= c1 and a2 * x + b2 * y >= c2 and x >= 0 and y >= 0
    pts = [(x, y) for x in range(0, 13) for y in range(0, 13)]
    good = [p for p in pts if ok(*p)]; bad = [p for p in pts if not ok(*p) and (a1 * p[0] + b1 * p[1] <= c1 + 6)]
    if not good or len(bad) < 3: return None
    g = r.choice(good); bs = r.sample(bad, 3)
    P = lambda p: f'({p[0]}, {p[1]})'
    return dict(q=f'Which point lies in the region {lin(a1, b1)} ≤ {c1}, {lin(a2, b2)} ≥ {c2}, x ≥ 0, y ≥ 0?', a=P(g), w=[P(b) for b in bs],
                ex=f'A point lies in the common region only if it satisfies every inequality. Substitute each option: {P(g)} gives {a1*g[0]+b1*g[1]} ≤ {c1} and {a2*g[0]+b2*g[1]} ≥ {c2}, so it is inside. Each other option breaks at least one of the two conditions, so it lies outside the feasible region.',
                fast='Check the first inequality for all four points, then only the survivors against the second.', secs=45, d='core', topic=T4,
                k='ch03.feaspt', data={'c1': [a1, b1, c1], 'c2': [a2, b2, c2]})


def corner(r):
    vx, vy = r.randint(1, 12), r.randint(1, 12)
    a1, b1, a2, b2 = (r.randint(1, 6) for _ in range(4))
    if a1 * b2 == a2 * b1: return None
    c1, c2 = a1 * vx + b1 * vy, a2 * vx + b2 * vy
    P = lambda x, y: f'({fr(x)}, {fr(y)})'
    return dict(q=f'The lines {lin(a1, b1)} = {c1} and {lin(a2, b2)} = {c2} meet at the corner point:', a=P(vx, vy),
                w=[P(vy, vx) if vx != vy else P(vx + 1, vy), P(F(c1, a1), 0), P(0, F(c2, b2)), P(vx + 1, vy - 1)],
                ex=f'A corner point of the feasible region where two boundary lines cross is found by solving them as simultaneous equations. Eliminating one variable gives x = {vx} and y = {vy}. Check: {a1}({vx}) + {b1}({vy}) = {c1} and {a2}({vx}) + {b2}({vy}) = {c2}. The intercepts on the axes are different corner points.',
                fast='Put each option into both equations; Cramer\'s rule: x = (c₁b₂ − c₂b₁)/(a₁b₂ − a₂b₁).', secs=40, d='core', topic=T4,
                k='ch03.corner', data={'l1': [a1, b1, c1], 'l2': [a2, b2, c2]})


def lp_setup(r):
    """two <= constraints through an interior integer vertex with integer intercepts"""
    vx, vy = r.randint(1, 15), r.randint(1, 15)
    a1, b1, a2, b2 = (r.randint(1, 5) for _ in range(4))
    c1, c2 = a1 * vx + b1 * vy, a2 * vx + b2 * vy
    if any(c % k for c, k in ((c1, a1), (c1, b1), (c2, a2), (c2, b2))): return None
    X1, Y1, X2, Y2 = c1 // a1, c1 // b1, c2 // a2, c2 // b2
    if not ((X1 > X2 and Y1 < Y2) or (X1 < X2 and Y1 > Y2)): return None
    return vx, vy, (a1, b1, c1), (a2, b2, c2), (X1, Y1, X2, Y2)


def lp_max(r):
    s = lp_setup(r)
    if not s: return None
    vx, vy, l1, l2, (X1, Y1, X2, Y2) = s
    p, q_ = r.randint(1, 9), r.randint(1, 9)
    V = [(0, 0), (min(X1, X2), 0), (vx, vy), (0, min(Y1, Y2))]
    Z = [p * x + q_ * y for x, y in V]; best = max(Z)
    if Z.count(best) > 1: return None
    i = Z.index(best); bv = V[i]
    return dict(q=f'Maximise Z = {lin(p, q_)} subject to {lin(l1[0], l1[1])} ≤ {l1[2]}, {lin(l2[0], l2[1])} ≤ {l2[2]}, x ≥ 0, y ≥ 0. The maximum value of Z is:',
                a=num(best), w=[num(z) for z in Z if z != best and z != 0] + [num(p * max(X1, X2) + q_ * 0), num(p * vx * 2), num(best + p)],
                ex=f'The feasible region has corner points (0, 0), ({min(X1, X2)}, 0), ({vx}, {vy}) and (0, {min(Y1, Y2)}). Evaluate Z at each: {", ".join(num(z) for z in Z)}. The largest is {num(best)} at ({bv[0]}, {bv[1]}). Using the larger intercept ({max(X1, X2)}, 0) is a trap — that point violates the other constraint.',
                fast='Corner-point method: find the 3 non-zero corners (two intercepts that satisfy both constraints, and the intersection) and compare Z.', secs=90, d='hard', topic=T5,
                check=str(best), k='ch03.lpmax', data={'Z': [p, q_], 'l1': list(l1), 'l2': list(l2)})


def lp_min(r):
    s = lp_setup(r)
    if not s: return None
    vx, vy, l1, l2, (X1, Y1, X2, Y2) = s
    p, q_ = r.randint(1, 9), r.randint(1, 9)
    V = [(max(X1, X2), 0), (vx, vy), (0, max(Y1, Y2))]
    Z = [p * x + q_ * y for x, y in V]; best = min(Z)
    if Z.count(best) > 1: return None
    bv = V[Z.index(best)]
    return dict(q=f'Minimise Z = {lin(p, q_)} subject to {lin(l1[0], l1[1])} ≥ {l1[2]}, {lin(l2[0], l2[1])} ≥ {l2[2]}, x ≥ 0, y ≥ 0. The minimum value of Z is:',
                a=num(best), w=[num(z) for z in Z if z != best] + [num(p * min(X1, X2)), num(q_ * min(Y1, Y2)), num(0)],
                ex=f'With "≥" constraints the feasible region is unbounded, away from the origin. Its corner points are ({max(X1, X2)}, 0), ({vx}, {vy}) and (0, {max(Y1, Y2)}). Z there = {", ".join(num(z) for z in Z)}; the minimum is {num(best)} at ({bv[0]}, {bv[1]}). Zero is not possible because (0, 0) is outside the region.',
                fast='Evaluate Z only at the three corners: the larger x-intercept, the larger y-intercept and the intersection point.', secs=90, d='hard', topic=T5,
                check=str(best), k='ch03.lpmin', data={'Z': [p, q_], 'l1': list(l1), 'l2': list(l2)})


ITEMS = [('chair', 'chairs', 'table', 'tables'), ('shirt', 'shirts', 'pair of trousers', 'pairs of trousers'), ('toy of type A', 'toys of type A', 'toy of type B', 'toys of type B'),
         ('bag', 'bags', 'belt', 'belts'), ('cake', 'cakes', 'pastry', 'pastries'), ('lamp', 'lamps', 'fan', 'fans')]


def formulate(r):
    As, Ap, Bs, Bp = r.choice(ITEMS); a, b = r.sample(range(1, 9), 2); H = r.randint(40, 300)
    res, one, many = r.choice([('machine time', 'hour', 'hours'), ('labour', 'hour', 'hours'), ('raw material', 'kg', 'kg')])
    u = lambda n: one if n == 1 else many
    ans = f'{lin(a, b)} ≤ {H}'
    return dict(q=f'A unit makes x {Ap} and y {Bp}. Each {As} needs {a} {u(a)} of {res} and each {Bs} needs {b} {u(b)}; only {H} {many} of {res} are available. The constraint is:',
                a=ans, w=[f'{lin(a, b)} ≥ {H}', f'{lin(b, a)} ≤ {H}', f'{lin(1, 1)} ≤ {H}', f'{lin(a, b)} = {H}'],
                ex=f'Total {res} used = {a} per unit × x + {b} per unit × y = {lin(a, b)}. Usage cannot exceed what is available, so {ans}. Use "≤" for a limited resource and "≥" for a minimum requirement. Swapping the coefficients attaches each requirement to the wrong product.',
                fast='Coefficient of x goes with the product called x; "only/at most/available" means ≤.', secs=30, d='core', topic=T3, k='ch03.form', data={'a': a, 'b': b, 'H': H})


def slack(r):
    s = lp_setup(r)
    if not s: return None
    vx, vy, l1, l2, (X1, Y1, X2, Y2) = s
    # maximise Z = px with x only: optimum at the smaller x-intercept; slack on the other constraint
    p = r.randint(2, 9)
    if X1 < X2: bx, lt, lo = X1, l1, l2
    else: bx, lt, lo = X2, l2, l1
    unused = lo[2] - lo[0] * bx
    if unused <= 0: return None
    return dict(q=f'A firm maximises Z = {p}x subject to {lin(l1[0], l1[1])} ≤ {l1[2]} (resource P), {lin(l2[0], l2[1])} ≤ {l2[2]} (resource Q), x ≥ 0, y ≥ 0. At the optimum, how many units of the resource that is not fully used remain unused?',
                a=num(unused), w=[num(lo[2]), num(lt[2] - lt[0] * bx + lo[0]), num(abs(lo[2] - lo[0] * max(X1, X2))) if lo[2] != lo[0] * max(X1, X2) else num(unused + 1), num(unused * 2)],
                ex=f'Z depends only on x, so the optimum is the largest x allowed: x = {bx}, y = 0 (the binding constraint gives x ≤ {bx}). The other resource uses {lo[0]} × {bx} = {lo[0]*bx} of its {lo[2]} units, so {unused} units remain unused (its slack). The binding resource has zero slack.',
                fast=f'Optimum at the smaller x-intercept ({bx}, 0); unused = capacity − usage = {lo[2]} − {lo[0]*bx}.', secs=75, d='hard', topic=T6,
                check=str(unused), k='ch03.slack', data={'p': p, 'l1': list(l1), 'l2': list(l2)})


def vertices(cons):
    """cons: list of (a, b, c, sense) meaning a x + b y (<= or >=) c; returns the corner points of the region"""
    pts = set()
    for i in range(len(cons)):
        for j in range(i + 1, len(cons)):
            a1, b1, c1, _ = cons[i]; a2, b2, c2, _ = cons[j]; D = a1 * b2 - a2 * b1
            if D == 0: continue
            x, y = F(c1 * b2 - c2 * b1, D), F(a1 * c2 - a2 * c1, D)
            if all((a * x + b * y <= c) if s == '<=' else (a * x + b * y >= c) for a, b, c, s in cons): pts.add((x, y))
    return pts


def ncorners(r):
    s = lp_setup(r)
    if not s: return None
    vx, vy, l1, l2, (X1, Y1, X2, Y2) = s
    var = r.choice(['x', 'y']); sense = r.choice(['<=', '>=']); k = r.randint(1, max(2, (min(X1, X2) if var == 'x' else min(Y1, Y2)) - 1))
    cons = [(l1[0], l1[1], l1[2], '<='), (l2[0], l2[1], l2[2], '<='), (1, 0, 0, '>='), (0, 1, 0, '>='), ((1, 0) if var == 'x' else (0, 1)) + (k, sense)]
    V = vertices(cons); n = len(V)
    if n < 3: return None
    vs = ', '.join(f'({fr(x)}, {fr(y)})' for x, y in sorted(V))
    return dict(q=f'How many corner points does the feasible region of {lin(l1[0], l1[1])} ≤ {l1[2]}, {lin(l2[0], l2[1])} ≤ {l2[2]}, {var} {SG[sense]} {k}, x ≥ 0, y ≥ 0 have?', a=str(n), w=[str(n - 1), str(n + 1), str(n + 2), str(n - 2)],
                ex=f'Draw the two lines using their intercepts, the line {var} = {k}, and keep the side allowed by each sign. The common region is a polygon with corners {vs}. So it has {n} corner points. Points where lines cross outside the region are not corner points.',
                fast='Sketch with intercepts only; test each crossing point in all constraints and count the survivors.', secs=75, d='hard', topic=T4, check=str(n),
                k='ch03.ncorn', data={'l1': list(l1), 'l2': list(l2), 'var': var, 'k': k, 'sense': SG[sense]})


def halfplane(r):
    a, b = r.randint(1, 9), r.randint(1, 9); c = r.choice([-1, 1]) * r.randint(2, 40); op = r.choice(['<=', '>='])
    orig = (0 <= c) if op == '<=' else (0 >= c)
    A = ['The half-plane that contains the origin', 'The half-plane that does not contain the origin', 'Only the points on the line', 'The whole plane']
    ans = A[0] if orig else A[1]
    return dict(q=f'The solution region of {lin(a, b)} {SG[op]} {c} is:', a=ans, w=[x for x in A if x != ans],
                ex=f'Draw the line {lin(a, b)} = {c}; it divides the plane into two half-planes. Test the origin: 0 {SG[op]} {c} is {"true" if orig else "false"}, so the solution region is the side {"containing" if orig else "not containing"} the origin, together with the line itself (because the sign includes equality).',
                fast='Origin test: put x = 0, y = 0 — true means shade the origin side.', secs=20, d='core', topic=T2, k='ch03.half', data={'a': a, 'b': b, 'c': c, 'op': SG[op]})


def avg_marks(r):
    n = r.choice([3, 4, 5]); A = r.randint(55, 85); ms = [r.randint(40, 98) for _ in range(n - 1)]
    need = n * A - sum(ms)
    if not 30 <= need <= 100: return None
    return dict(q=f'A student scored {", ".join(map(str, ms))} in the first {n - 1} tests. What is the minimum score in test {n} for an average of at least {A}?', a=str(need),
                w=[str(A), str(need - 1), str(need + 1), str(round(sum(ms) / (n - 1)))],
                ex=f'Let the score be x. Average ≥ {A} means ({" + ".join(map(str, ms))} + x)/{n} ≥ {A}, i.e. {sum(ms)} + x ≥ {n*A}, so x ≥ {need}. The minimum score is {need}. Writing x ≥ {A} ignores how the earlier scores pull the average up or down.',
                fast=f'Total needed = {n} × {A} = {n*A}; subtract the marks already earned ({sum(ms)}).', secs=30, d='core', topic=T3, check=str(need),
                k='ch03.avg', data={'ms': ms, 'A': A})


BANKS = {U: [(one_var, 3), (count_int, 3), (feasible_pt, 3), (corner, 2), (lp_max, 3), (lp_min, 3), (formulate, 3), (slack, 2), (ncorners, 2), (halfplane, 2), (avg_marks, 2)]}
