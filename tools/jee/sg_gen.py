"""Practice generators — Mathematics Unit 11: Three Dimensional Geometry. Each item is built from integer data with
the answer planted by construction; check() re-solves it a different way — shortest distances by numerically
minimising the gap between two moving points, images by the mid-point/perpendicular test, meeting points by
searching for where two lines come together, and distances along a direction by walking until the line is hit."""
import math, itertools
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
QD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17), (8, 9, 12, 17)]
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def addv(a, b, k=1): return tuple(x + k * y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(dot(a, a))
def red(v):
    g = math.gcd(*[abs(x) for x in v]); need(g); v = tuple(x // g for x in v)
    return tuple(-x for x in v) if (v[0] < 0 or (v[0] == 0 and (v[1] < 0 or (v[1] == 0 and v[2] < 0)))) else v
def rv(rng, lo=-4, hi=4): return tuple(rng.randint(lo, hi) for _ in range(3))
def signed(rng, v): o = list(v[:3]); rng.shuffle(o); return tuple(x * rng.choice([1, -1]) for x in o)
def num(v):
    v = F(v); return fr(v)
def part(var, a):   # x − a
    a = F(a)
    if a == 0: return var
    return f'{var} − {fr(a)}' if a > 0 else f'{var} + {fr(-a)}'
def ln(A, d):   # symmetric form
    return ' = '.join(f'\\f{{{part(v, a)}}}{{{num(c)}}}' for v, a, c in zip('xyz', A, d))
def pt(A): return '(' + ', '.join(num(a) for a in A) + ')'
def vec(d):
    s = ''
    for c, u in zip(d, ('î', 'ĵ', 'k̂')):
        if c == 0: continue
        t = ('' if abs(c) == 1 else str(abs(c))) + u
        s += (' − ' if c < 0 else (' + ' if s else '')) + t if s else ('−' if c < 0 else '') + t
    return s
def frs(x):
    x = F(x).limit_denominator(10 ** 6); return fr(x)

# ---------------- shortest distance
def g_sd(rng):
    t = rng.choice(['sd_skew', 'sd_par', 'sd_lam', 'sd_meet', 'sd_sq'])
    if t in ('sd_skew', 'sd_lam', 'sd_sq'):
        q = rng.choice(QD); n = signed(rng, q); N = q[3]
        d1 = red(cross(n, rv(rng))); d2 = red(cross(n, rv(rng))); need(nrm(cross(d1, d2)) > 0 and max(map(abs, d1 + d2)) <= 12)
        A1 = rv(rng, -6, 6); j = rng.choice([1, 2, 3, -1, -2]); w = addv(addv(tuple(j * x for x in n), d1, rng.randint(-1, 1)), d2, rng.randint(-1, 1)); A2 = addv(A1, w)
        need(max(map(abs, A2)) <= 15); n0 = red(cross(d1, d2)); D = F(abs(dot(w, n0)), 1) / F(math.isqrt(dot(n0, n0)) if math.isqrt(dot(n0, n0)) ** 2 == dot(n0, n0) else 0 or 1)
        need(math.isqrt(dot(n0, n0)) ** 2 == dot(n0, n0)); D = F(abs(dot(w, n0)), math.isqrt(dot(n0, n0))); need(D.denominator == 1 and D > 0)
        if t == 'sd_skew':
            return dict(q=f'The shortest distance between the lines {ln(A1, d1)} and {ln(A2, d2)} is ____.', o=None, a=int(D),
                        sol=[f'n = d_{{1}} × d_{{2}} ∥ {pt(n0)}, |n| = {math.isqrt(dot(n0, n0))}.', f'(A_{{2}} − A_{{1}})·n = {dot(w, n0)} → distance = {int(D)}.'], p=dict(t=t, A1=A1, d1=d1, A2=A2, d2=d2))
        if t == 'sd_sq':
            return dict(q=f'If d is the shortest distance between the lines r⃗ = ({vec(A1) or "0"}) + λ({vec(d1)}) and r⃗ = ({vec(A2) or "0"}) + μ({vec(d2)}), then d^{{2}} = ____.', o=None, a=int(D * D),
                        sol=[f'Normal n = d_{{1}} × d_{{2}} ∥ {pt(n0)}, |n| = {math.isqrt(dot(n0, n0))}.', f'd = \\f{{|(A_{{2}} − A_{{1}})·n|}}{{|n|}} = {int(D)} → d^{{2}} = {int(D * D)}.'], p=dict(t=t, A1=A1, d1=d1, A2=A2, d2=d2))
        # λ in the x-coordinate of A1: |c − λ n_x| = D|n| has two roots
        need(n0[0] != 0); s = F(2 * dot(sub(A2, (0, A1[1], A1[2])), n0), n0[0]); need(s.denominator == 1)
        return dict(q=f'The shortest distance between the lines \\f{{x − λ}}{{{d1[0]}}} = \\f{{{part("y", A1[1])}}}{{{d1[1]}}} = \\f{{{part("z", A1[2])}}}{{{d1[2]}}} and {ln(A2, d2)} is {int(D)}. The sum of all possible values of λ is ____.', o=None, a=int(s),
                    sol=[f'n ∥ {pt(n0)}, |n| = {math.isqrt(dot(n0, n0))}. (A_{{2}} − A_{{1}})·n is linear in λ with λ-coefficient −{n0[0]}.'.replace('−-', ''), f'|… | = {int(D)}·{math.isqrt(dot(n0, n0))} gives two values whose sum is {int(s)}.'], p=dict(t=t, A1=(None, A1[1], A1[2]), d1=d1, A2=A2, d2=d2, D=int(D)))
    if t == 'sd_par':
        q = rng.choice(QD); d = red(signed(rng, q)); A1 = rv(rng, -5, 5); w = rv(rng, -4, 4); A2 = addv(A1, w); k = rng.choice([1, 2, -1, 3])
        c = cross(w, d); need(dot(c, c)); v = F(dot(c, c), q[3] ** 2); d2 = tuple(k * x for x in d)
        o, an = mcq(rng, fr(v), [fr(v + 1), fr(F(dot(w, w))), fr(v * 2), fr(F(dot(c, c), q[3]))])
        return dict(q=f'The square of the distance between the parallel lines {ln(A1, d)} and {ln(A2, d2)} is', o=o, a=an,
                    sol=['For parallel lines: distance = \\f{|(A_{2} − A_{1}) × d|}{|d|}.', f'(A_{{2}} − A_{{1}}) × d = {pt(c)}, |d| = {q[3]} → distance^{{2}} = {fr(v)}.'], p=dict(t=t, A1=A1, d1=d, A2=A2, d2=d2))
    X = rv(rng, -5, 5); d1, d2 = red(rv(rng, -3, 3)), red(rv(rng, -3, 3)); need(nrm(cross(d1, d2)) > 0)
    A1, A2 = addv(X, d1, rng.randint(-2, 2)), addv(X, d2, rng.randint(1, 3)); K = rng.randint(-3, 3); A2k = (A2[0], A2[1], A2[2])
    return dict(q=f'The lines {ln(A1, d1)} and {ln(A2, d2)} intersect at the point (α, β, γ). Then α + β + γ = ____.', o=None, a=sum(X),
                sol=['Write both in parameter form and equate x and y to find the parameters; z must then agree.', f'They meet at {pt(X)} → {sum(X)}.'], p=dict(t='sd_meet', A1=A1, d1=d1, A2=A2, d2=d2))

# ---------------- images and feet
def g_img(rng):
    t = rng.choice(['i_img', 'i_foot', 'i_dist', 'i_area', 'i_proj'])
    d = red(rv(rng, -4, 4)); need(dot(d, d) > 1); Fo = rv(rng, -5, 5); v = red(cross(d, rv(rng, -3, 3))); k = rng.choice([1, 2, -1]); v = tuple(k * x for x in v)
    need(dot(v, v) and max(map(abs, v)) <= 10); Pp = addv(Fo, v); A = addv(Fo, d, rng.choice([-2, -1, 1, 2])); I = sub(Fo, v)
    if t == 'i_img':
        return dict(q=f'If (α, β, γ) is the image of the point {pt(Pp)} in the line {ln(A, d)}, then α + β + γ = ____.', o=None, a=sum(I),
                    sol=['Find the foot F (parameter t = \\f{(P − A)·d}{|d|^{2}}), then image = 2F − P.', f'F = {pt(Fo)}, image = {pt(I)} → {sum(I)}.'], p=dict(t=t, P=Pp, A=A, d=d))
    if t == 'i_foot':
        cc = rng.choice([(1, 1, 1), (1, 2, 3), (2, -1, 1), (1, -1, 2)])
        return dict(q=f'If (a, b, c) is the foot of the perpendicular from {pt(Pp)} to the line {ln(A, d)}, then {cc[0] if cc[0] != 1 else ""}a {"+ " + ("" if cc[1] == 1 else str(cc[1])) if cc[1] > 0 else "− " + ("" if cc[1] == -1 else str(-cc[1]))}b {"+ " + ("" if cc[2] == 1 else str(cc[2])) if cc[2] > 0 else "− " + ("" if cc[2] == -1 else str(-cc[2]))}c = ____.', o=None, a=dot(cc, Fo),
                    sol=['Foot: A + td with t = \\f{(P − A)·d}{|d|^{2}}.', f'Foot {pt(Fo)} → {dot(cc, Fo)}.'], p=dict(t=t, P=Pp, A=A, d=d, cc=cc))
    if t == 'i_dist':
        return dict(q=f'The square of the perpendicular distance of the point {pt(Pp)} from the line {ln(A, d)} is ____.', o=None, a=dot(v, v),
                    sol=['Find the foot F, then distance = PF.', f'F = {pt(Fo)} → PF^{{2}} = {dot(v, v)}.'], p=dict(t=t, P=Pp, A=A, d=d))
    if t == 'i_area':
        m = rng.choice([1, 2, -1, -2, 3]); R = addv(Fo, d, m); a2 = dot(v, v) * m * m * dot(d, d)   # (½·2|v|·|m d|)²
        return dict(q=f'Q is the image of P{pt(Pp)} in the line {ln(A, d)} and R{pt(R)} lies on the line. The square of the area of triangle PQR is ____.', o=None, a=a2,
                    sol=['PQ is perpendicular to the line and bisected by it at the foot F; R is on the line, so the height from R is RF.', f'F = {pt(Fo)}: area = \\f{{1}}{{2}}·PQ·RF → area^{{2}} = |PF|^{{2}}·|RF|^{{2}} = {dot(v, v)}·{m * m * dot(d, d)} = {a2}.'], p=dict(t=t, P=Pp, A=A, d=d, R=R))
    u = rng.choice([(1, 2, 2, 3), (2, 3, 6, 7), (2, 1, 2, 3), (6, 2, 3, 7), (4, 4, 7, 9), (1, 4, 8, 9)]); w = u[:3]; val = F(dot(Fo, w), u[3]); need(val != 0)
    o, an = mcq(rng, fr(abs(val)), [fr(abs(val) + 1), fr(abs(F(dot(Pp, w), u[3]))), fr(abs(val) * 2), fr(abs(F(dot(I, w), u[3])))])
    return dict(q=f'If the foot of the perpendicular from {pt(Pp)} to the line {ln(A, d)} is (α, β, γ), the length of the projection of αî + βĵ + γk̂ on {vec(w)} is', o=o, a=an,
                sol=[f'Foot = {pt(Fo)}.', f'Projection = \\f{{|F·w|}}{{|w|}} = \\f{{{abs(dot(Fo, w))}}}{{{u[3]}}}.'], p=dict(t='i_proj', P=Pp, A=A, d=d, w=w))

# ---------------- other line problems
def g_line3(rng):
    t = rng.choice(['l_along', 'l_perp', 'l_tri', 'l_eq', 'l_cos', 'l_div', 'l_twopt'])
    if t == 'l_along':
        X = rv(rng, -5, 5); d = red(rv(rng, -3, 3)); q = rng.choice(QD); u = signed(rng, q); need(nrm(cross(d, u)) > 0); k = rng.choice([1, 2, -1, -2]); Pp = addv(X, u, k); A = addv(X, d, rng.randint(-2, 2))
        return dict(q=f'The distance of the point {pt(Pp)} from the line {ln(A, d)}, measured along a line with direction ratios {u[0]}, {u[1]}, {u[2]}, is ____.', o=None, a=abs(k) * q[3],
                    sol=[f'Move from the point: {pt(Pp)} + s{pt(u)}, and find s for which this lies on the line.', f's = {-k} gives {pt(X)}; distance = |s|·{q[3]} = {abs(k) * q[3]}.'], p=dict(t=t, P=Pp, A=A, d=d, u=u))
    if t == 'l_perp':
        d1, d2 = red(rv(rng, -3, 3)), red(rv(rng, -3, 3)); dd = red(cross(d1, d2)); need(dd[0] != 0 and dot(dd, dd) and max(map(abs, dd)) <= 9); Pp = rv(rng, -6, 6); need(Pp[0] != 0)
        s = F(-Pp[0], dd[0]); Q = tuple(F(p) + s * c for p, c in zip(Pp, dd)); v = s * s * dot(dd, dd)
        o, an = mcq(rng, fr(v), [fr(v + 1), fr(v * 2), fr(s * s), fr(v + F(1, 2))])
        return dict(q=f'A line through {pt(Pp)} is perpendicular to both {ln((0, 0, 0), d1)} and {ln((1, 1, 1), d2)}. It meets the yz-plane at Q. If P is {pt(Pp)}, then PQ^{{2}} =', o=o, a=an,
                    sol=[f'Direction = d_{{1}} × d_{{2}} ∥ {pt(dd)}.', f'x = 0 at parameter {fr(s)} → Q = {pt(Q)}; PQ^{{2}} = {fr(v)}.'], p=dict(t=t, P=Pp, d1=d1, d2=d2))
    if t == 'l_tri':
        q = rng.choice(QD); d = signed(rng, q[:3] + (0,))[:3] if False else red(rv(rng, -3, 3)); need(dot(d, d)); Fo = rv(rng, -4, 4); v = red(cross(d, rv(rng, -3, 3))); need(dot(v, v)); B = addv(Fo, v)
        L = rng.randint(2, 10); a2 = F(L * L * dot(v, v), 4); A = addv(Fo, d, rng.randint(-2, 2))
        return dict(q=f'Vertices A and C of triangle ABC lie on the line {ln(A, d)}, AC = {L} and B = {pt(B)}. If the area of the triangle is Δ, then Δ^{{2}} = ____.' if a2.denominator == 1 else 'x', o=None, a=int(a2) if a2.denominator == 1 else need(False),
                    sol=['Height = distance of B from the line.', f'Foot {pt(Fo)} → height^{{2}} = {dot(v, v)}; Δ^{{2}} = \\f{{1}}{{4}}·{L * L}·{dot(v, v)} = {int(a2)}.'], p=dict(t=t, B=B, A=A, d=d, L=L))
    if t == 'l_eq':
        A = rv(rng, -5, 5); r0 = rng.randint(-5, 8); Pp0 = (A[0] + rng.randint(-3, 3), None, A[2] + rng.randint(-3, 3)); a, c = Pp0[0] - A[0], Pp0[2] - A[2]
        D2 = F(2 * (a * a + c * c) - 2 * a * c, 3)   # with y = A_y the distance² to direction (1,1,1)
        # distance² as a function of y: |v|² − (v·(1,1,1))²/3 with v = (a, y − A_y, c) → roots sum: 2A_y + (a + c)
        h = rng.randint(1, 4); val = D2 + F(2 * h * h, 3) if False else None
        m = rng.randint(1, 4); y1 = A[1] + F(a + c, 2) + m; y2 = A[1] + F(a + c, 2) - m; need(F(a + c, 2).denominator == 1)
        dist2 = lambda y: F(a * a + (y - A[1]) ** 2 + c * c) - F((a + (y - A[1]) + c) ** 2, 3)
        need(dist2(y1) == dist2(y2)); ds = dist2(y1)
        return dict(q=f'A line through {pt(A)} makes equal angles with the coordinate axes (direction 1, 1, 1). If the square of the distance of ({Pp0[0]}, r, {Pp0[2]}) from it is {fr(ds)}, then the sum of all possible values of r is ____.', o=None, a=int(y1 + y2),
                    sol=['v = point − A; distance^{2} = |v|^{2} − \\f{(v·(1, 1, 1))^{2}}{3}, a quadratic in r.', f'Its two roots are symmetric about {fr(A[1] + F(a + c, 2))} → sum {int(y1 + y2)}.'], p=dict(t=t, A=A, x=Pp0[0], z=Pp0[2], D=float(ds)))
    if t == 'l_cos':
        q1, q2 = rng.sample(QD, 2); u1, u2 = signed(rng, q1), signed(rng, q2); c = F(abs(dot(u1, u2)), q1[3] * q2[3]); need(c != 0 and c != 1)
        o, an = mcq(rng, fr(c), [fr(1 - c), fr(c / 2), fr(c + F(1, q1[3] * q2[3])), fr(F(abs(dot(u1, u2)), q1[3] * q2[3] + 1))])
        return dict(q=f'The cosine of the acute angle between the lines \\f{{x}}{{{u1[0]}}} = \\f{{y}}{{{u1[1]}}} = \\f{{z}}{{{u1[2]}}} and \\f{{x − 1}}{{{u2[0]}}} = \\f{{y + 2}}{{{u2[1]}}} = \\f{{z − 3}}{{{u2[2]}}} is', o=o, a=an,
                    sol=['cos θ = \\f{|d_{1}·d_{2}|}{|d_{1}||d_{2}|}.', f'= \\f{{{abs(dot(u1, u2))}}}{{{q1[3]}·{q2[3]}}} = {fr(c)}.'], p=dict(t=t, u1=u1, u2=u2))
    if t == 'l_div':
        Pp = rv(rng, -5, 5); q = rng.choice(QD); u = signed(rng, q); m = rng.randint(1, 4); Q = addv(Pp, u, m); k = rng.randint(1, m * q[3] - 1) if m * q[3] > 1 else 1
        X = tuple(F(p) + F(k, q[3]) * c for p, c in zip(Pp, u)); s = sum(X)
        return dict(q=f'R is the point on the segment joining P{pt(Pp)} and Q{pt(Q)} at a distance {k} from P. If R = (α, β, γ), then {q[3]}(α + β + γ) = ____.', o=None, a=int(q[3] * s),
                    sol=[f'PQ = {m * q[3]}; unit vector along PQ is \\f{{1}}{{{q[3]}}}{pt(u)}.', f'R = P + \\f{{{k}}}{{{q[3]}}}{pt(u)} → {q[3]}(α + β + γ) = {int(q[3] * s)}.'], p=dict(t=t, P=Pp, Q=Q, k=k, m=q[3]))
    Pp = rv(rng, -5, 5); Q = addv(Pp, red(rv(rng, -3, 3))); need(Q != Pp); d = sub(Q, Pp); M = rng.choice([2, 3, 4, -1, -2]); Rr = addv(Pp, d, M)
    wr = [addv(Rr, e) for e in ((1, 0, 0), (0, 1, -1), (-1, 1, 0), (0, 0, 2), (1, 1, 0), (0, -1, 2))]; wr = [x for x in wr if nrm(cross(sub(x, Pp), d)) > 1e-9]
    o, an = mcq(rng, pt(Rr), [pt(x) for x in wr])
    return dict(q=f'Which of the following points lies on the line through {pt(Pp)} and {pt(Q)}?', o=o, a=an,
                sol=[f'Direction {pt(d)}; points are {pt(Pp)} + t{pt(d)}.', f't = {M} gives {pt(Rr)}.'], p=dict(t='l_twopt', P=Pp, Q=Q))

def robust(gf):
    def w(rng):
        for _ in range(800):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(sd=g_sd, img=g_img, line3=g_line3).items()}
import re
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent checks
def tofr(s):
    s = s.replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-')
    v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def close(a, b, tol=1e-6): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))
def gap_min(A1, d1, A2, d2):   # minimise |A1 + s d1 − A2 − t d2| by coordinate descent (it is a convex quadratic)
    s = t = 0.0; a, b = dot(d1, d1), dot(d2, d2); prev = None
    for _ in range(3000):
        r = sub(addv(A1, d1, s), addv(A2, d2, t)); s -= dot(r, d1) / a
        r = sub(addv(A1, d1, s), addv(A2, d2, t)); t += dot(r, d2) / b
        g = nrm(sub(addv(A1, d1, s), addv(A2, d2, t)))
        if prev is not None and abs(prev - g) < 1e-15: break
        prev = g
    return g
def on_line(X, A, d): return nrm(cross(sub(X, A), d)) < 1e-7 * max(1, nrm(sub(X, A)))
def walk(Pt, u, A, d):   # step along u until the line is hit: minimise distance of Pt + s u to the line over s
    lo, hi = -50.0, 50.0
    f = lambda s: nrm(cross(sub(addv(Pt, u, s), A), d))
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) < f(m2): hi = m2
        else: lo = m1
    s = (lo + hi) / 2; assert f(s) < 1e-6; return s
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('sd_skew', 'sd_sq'):
        g = gap_min(p['A1'], p['d1'], p['A2'], p['d2']); return close(R, g if t == 'sd_skew' else g * g)
    if t == 'sd_lam':
        A1 = p['A1']; f = lambda l: gap_min((l, A1[1], A1[2]), p['d1'], p['A2'], p['d2']) - p['D']
        xs = [x + 0.0137 for x in range(-400, 401)]; rts = []
        for a, b in zip(xs, xs[1:]):
            if f(a) * f(b) < 0:
                for _ in range(60):
                    m = (a + b) / 2
                    if f(a) * f(m) <= 0: b = m
                    else: a = m
                rts.append((a + b) / 2)
            elif f(a) == 0: rts.append(a)
        return len(rts) == 2 and close(R, sum(rts), 1e-5)
    if t == 'sd_par': return close(tofr(R), gap_min(p['A1'], p['d1'], p['A2'], p['d2']) ** 2)
    if t == 'sd_meet':
        assert gap_min(p['A1'], p['d1'], p['A2'], p['d2']) < 1e-7
        s = walk(p['A1'], p['d1'], p['A2'], p['d2']); X = addv(p['A1'], p['d1'], s); return close(R, sum(X))
    if t in ('i_img', 'i_foot', 'i_dist', 'i_area', 'i_proj'):
        Pt, A, d = p['P'], p['A'], p['d']
        # foot = the point of the line nearest P (scan + refine), image = the point whose mid-point with P is on the line and PQ ⟂ d
        lo, hi = -200.0, 200.0; g = lambda u: dot(sub(addv(A, d, u), Pt), d)   # PF ⟂ d, found by bisection
        for _ in range(200):
            m = (lo + hi) / 2
            if g(lo) * g(m) <= 0: hi = m
            else: lo = m
        Fo = addv(A, d, (lo + hi) / 2); I = tuple(2 * a - b for a, b in zip(Fo, Pt))
        assert on_line(tuple((a + b) / 2 for a, b in zip(I, Pt)), A, d) and abs(dot(sub(I, Pt), d)) < 1e-6
        if t == 'i_img': return close(R, sum(I))
        if t == 'i_foot': return close(R, dot(p['cc'], Fo))
        if t == 'i_dist': return close(R, nrm(sub(Pt, Fo)) ** 2)
        if t == 'i_area': return close(R, (nrm(cross(sub(I, Pt), sub(p['R'], Pt))) / 2) ** 2)
        return close(tofr(R), abs(dot(Fo, p['w'])) / nrm(p['w']))
    if t == 'l_along':
        s = walk(p['P'], p['u'], p['A'], p['d']); return close(R, abs(s) * nrm(p['u']))
    if t == 'l_perp':
        dd = cross(p['d1'], p['d2']); assert abs(dot(dd, p['d1'])) < 1e-9 and abs(dot(dd, p['d2'])) < 1e-9
        lo, hi = -100.0, 100.0   # bisection for x = 0
        g = lambda s: p['P'][0] + s * dd[0]
        for _ in range(200):
            m = (lo + hi) / 2
            if g(lo) * g(m) <= 0: hi = m
            else: lo = m
        Q = addv(p['P'], dd, (lo + hi) / 2); return close(tofr(R), nrm(sub(Q, p['P'])) ** 2)
    if t == 'l_tri':
        A, d, B = p['A'], p['d'], p['B']; C1 = A; C2 = addv(A, d, p['L'] / nrm(d)); return close(R, (nrm(cross(sub(C1, B), sub(C2, B))) / 2) ** 2)
    if t == 'l_eq':
        A = p['A']; dist2 = lambda y: nrm(cross(sub((p['x'], y, p['z']), A), (1, 1, 1))) ** 2 / 3 - p['D']
        xs = [x / 8 + 0.0137 for x in range(-800, 801)]
        rr = []
        for a, b in zip(xs, xs[1:]):
            if dist2(a) * dist2(b) < 0:
                for _ in range(60):
                    m = (a + b) / 2
                    if dist2(a) * dist2(m) <= 0: b = m
                    else: a = m
                rr.append((a + b) / 2)
        return len(rr) == 2 and close(R, sum(rr), 1e-5)
    if t == 'l_cos':
        u1, u2 = p['u1'], p['u2']; ang = math.acos(dot(u1, u2) / (nrm(u1) * nrm(u2))); return close(tofr(R), abs(math.cos(min(ang, math.pi - ang))))
    if t == 'l_div':
        Pt, Q = p['P'], p['Q']; u = sub(Q, Pt); X = addv(Pt, u, p['k'] / nrm(u)); assert abs(nrm(sub(X, Pt)) - p['k']) < 1e-9; return close(R, p['m'] * sum(X))
    if t == 'l_twopt':
        X = tuple(float(tofr(x)) for x in R.strip('()').split(', ')); hits = [o for o in it['o'] if on_line(tuple(float(tofr(x)) for x in o.strip('()').split(', ')), p['P'], sub(p['Q'], p['P']))]
        return len(hits) == 1 and on_line(X, p['P'], sub(p['Q'], p['P']))
    raise KeyError(t)
