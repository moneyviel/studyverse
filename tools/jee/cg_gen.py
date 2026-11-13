"""Practice generators — Mathematics Unit 10: Coordinate Geometry. check() re-solves every item numerically from the
figure itself — intersections by solving the equations, focal distances by measuring to the foci, tangency by a
discriminant, extreme values by scanning — never from the formula used to build the item."""
import math, itertools
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
PYT = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15), (12, 16, 20), (20, 21, 29)]
def dist(p, q): return math.hypot(p[0] - q[0], p[1] - q[1])
def inter(l1, l2):
    (a1, b1, c1), (a2, b2, c2) = l1, l2; D = a1 * b2 - a2 * b1; return ((c1 * b2 - c2 * b1) / D, (a1 * c2 - a2 * c1) / D)
def ortho(A, B, C):
    return inter((C[0] - B[0], C[1] - B[1], (C[0] - B[0]) * A[0] + (C[1] - B[1]) * A[1]), (C[0] - A[0], C[1] - A[1], (C[0] - A[0]) * B[0] + (C[1] - A[1]) * B[1]))
def area(*V): return abs(sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))) / 2
def qr(a, b, c):
    d = b * b - 4 * a * c; return sorted([(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)]) if d >= -1e-12 else []
def lt(a, b, c):   # a x + b y = c as text
    s = []
    for co, v in ((a, 'x'), (b, 'y')):
        if co: s.append(('− ' if co < 0 else '+ ') + ('' if abs(co) == 1 else str(abs(co))) + v)
    t = ' '.join(s); t = t[2:] if t.startswith('+ ') else '−' + t[2:]; return f'{t} = {str(c).replace("-", "−")}'
def tofr(s):
    s = s.replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-'); v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def sgn(v): return f'+ {v}' if v >= 0 else f'− {-v}'

def g_line(rng):
    t = rng.choice(['l_par', 'l_pt', 'l_ortho', 'l_inc', 'l_refl', 'l_minarea'])
    if t == 'l_par':
        a, b, r = rng.choice(PYT); k = rng.randint(1, 6); c1 = rng.randint(-20, 20); c2 = c1 + k * r * rng.choice([1, -1])
        return dict(q=f'The distance between the parallel lines {lt(a, b, c1)} and {lt(a, b, c2)} is ____.', o=None, a=k,
                    sol=['Distance = \\f{|c_{1} − c_{2}|}{√{a^{2} + b^{2}}}.', f'\\f{{{abs(c1 - c2)}}}{{{r}}} = {k}.'], p=dict(t=t, a=a, b=b, c1=c1, c2=c2))
    if t == 'l_pt':
        a, b, r = rng.choice(PYT); px, py = rng.randint(-6, 6), rng.randint(-6, 6); d = rng.randint(1, 8); c = a * px + b * py + rng.choice([1, -1]) * d * r
        return dict(q=f'The distance of the point ({px}, {py}) from the line {lt(a, b, c)} is ____.', o=None, a=d,
                    sol=['\\f{|ax_{1} + by_{1} − c|}{√{a^{2} + b^{2}}}.', f'\\f{{{abs(a * px + b * py - c)}}}{{{r}}} = {d}.'], p=dict(t=t, a=a, b=b, c=c, P=[px, py]))
    if t == 'l_ortho':
        V = [(rng.randint(-6, 8), rng.randint(-6, 8)) for _ in range(3)]; need(area(*V) > 2)
        A, B, C = [tuple(map(F, v)) for v in V]
        l1 = (C[0] - B[0], C[1] - B[1], (C[0] - B[0]) * A[0] + (C[1] - B[1]) * A[1]); l2 = (C[0] - A[0], C[1] - A[1], (C[0] - A[0]) * B[0] + (C[1] - A[1]) * B[1])
        D = l1[0] * l2[1] - l2[0] * l1[1]; H = ((l1[2] * l2[1] - l2[2] * l1[1]) / D, (l1[0] * l2[2] - l2[0] * l1[2]) / D); v = H[0] + H[1]; need(v.denominator == 1 and abs(v) < 60)
        return dict(q=f'If (h, k) is the orthocentre of the triangle with vertices ({V[0][0]}, {V[0][1]}), ({V[1][0]}, {V[1][1]}) and ({V[2][0]}, {V[2][1]}), then h + k = ____.', o=None, a=int(v),
                    sol=['Intersect two altitudes: through each vertex, perpendicular to the opposite side.', f'H = ({fr(H[0])}, {fr(H[1])}) → h + k = {int(v)}.'], p=dict(t=t, V=V))
    if t == 'l_inc':
        a, b, c = rng.choice(PYT); k = rng.randint(1, 2); sx, sy = rng.randint(-5, 5), rng.randint(-5, 5); a, b, c = a * k, b * k, c * k
        r = (a + b - c) // 2; I = (sx + r, sy + r)
        return dict(q=f'The incentre of the triangle with vertices ({sx}, {sy}), ({sx + a}, {sy}) and ({sx}, {sy + b}) is (h, k). Then h + k = ____.', o=None, a=I[0] + I[1],
                    sol=[f'Right angle at ({sx}, {sy}); inradius r = \\f{{a + b − c}}{{2}} = {r}.', f'Incentre ({I[0]}, {I[1]}) → {I[0] + I[1]}.'], p=dict(t=t, V=[(sx, sy), (sx + a, sy), (sx, sy + b)]))
    if t == 'l_refl':
        a, b = rng.choice([(1, 1), (1, 2), (2, 1), (1, -1), (3, 1), (1, 3), (2, -1), (1, -2)]); Pp = (rng.randint(-6, 6), rng.randint(-6, 6)); tt = rng.choice([-2, -1, 1, 2])
        Q = (Pp[0] - 2 * tt * a, Pp[1] - 2 * tt * b); c = a * (Pp[0] + Q[0]) // 2 + b * (Pp[1] + Q[1]) // 2; need(a * (Pp[0] + Q[0]) % 2 == 0 or True)
        M = (F(Pp[0] + Q[0], 2), F(Pp[1] + Q[1], 2)); c = a * M[0] + b * M[1]; need(c.denominator == 1)
        return dict(q=f'If (α, β) is the image of the point ({Pp[0]}, {Pp[1]}) in the line {lt(a, b, int(c))}, then α + β = ____.', o=None, a=Q[0] + Q[1],
                    sol=['Image = P − \\f{2(ax_{1} + by_{1} − c)}{a^{2} + b^{2}}(a, b).', f'Image ({Q[0]}, {Q[1]}) → {Q[0] + Q[1]}.'], p=dict(t=t, a=a, b=b, c=int(c), P=list(Pp)))
    px, py = rng.randint(1, 9), rng.randint(1, 9)
    return dict(q=f'A line through ({px}, {py}) cuts the positive x- and y-axes at A and B. The least possible area of triangle OAB is ____.', o=None, a=2 * px * py,
                sol=['With intercepts a, b: \\f{p}{a} + \\f{q}{b} = 1 and ab is least when \\f{p}{a} = \\f{q}{b} = \\f{1}{2}.', f'a = {2 * px}, b = {2 * py} → area {2 * px * py}.'], p=dict(t='l_minarea', px=px, py=py))

def g_circle(rng):
    t = rng.choice(['c_chord', 'c_tlen', 'c_common', 'c_touch', 'c_three', 'c_square'])
    if t == 'c_chord':
        d, s, r = rng.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (0, 5, 5), (8, 15, 17)]); h, k = rng.randint(-4, 4), rng.randint(-4, 4)
        a, b, n = rng.choice(PYT); c = a * h + b * k + rng.choice([1, -1]) * d * n
        return dict(q=f'The line {lt(a, b, c)} cuts the circle (x {sgn(-h)})^{{2}} + (y {sgn(-k)})^{{2}} = {r * r} in a chord of length ____.'.replace('+ 0)', ')').replace('− 0)', ')'), o=None, a=2 * s,
                    sol=[f'Distance of the centre from the line: {d}.', f'Chord = 2√{{r^{{2}} − d^{{2}}}} = 2√{{{r * r} − {d * d}}} = {2 * s}.'], p=dict(t=t, h=h, k=k, r=r, a=a, b=b, c=c))
    if t == 'c_tlen':
        g, f_, c = rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-10, 4); need(g * g + f_ * f_ - c > 0); px, py = rng.randint(-8, 8), rng.randint(-8, 8)
        S = px * px + py * py + 2 * g * px + 2 * f_ * py + c; need(S > 0)
        return dict(q=f'The square of the length of the tangent from ({px}, {py}) to the circle x^{{2}} + y^{{2}} {sgn(2 * g)}x {sgn(2 * f_)}y {sgn(c)} = 0 is ____.'.replace('+ 0x ', '').replace('+ 0y ', '').replace(' + 0 = 0', ' = 0'), o=None, a=S,
                    sol=['Tangent length^{2} = S(P): substitute the point into the circle\'s equation.', f'= {S}.'], p=dict(t=t, g=g, f=f_, c=c, P=[px, py]))
    if t == 'c_common':
        r1 = rng.randint(3, 9); d = rng.randint(2, 12); r2 = rng.randint(2, 10); need(abs(r1 - r2) < d < r1 + r2)
        x = F(d * d + r1 * r1 - r2 * r2, 2 * d); L2 = 4 * (r1 * r1 - x * x); need(L2 > 0)
        o, an = mcq(rng, fr(L2), [fr(L2 + 4), fr(L2 / 2), fr(4 * r1 * r1), fr(L2 * 2)])
        return dict(q=f'The circles x^{{2}} + y^{{2}} = {r1 * r1} and (x − {d})^{{2}} + y^{{2}} = {r2 * r2} meet at P and Q. Then PQ^{{2}} =', o=o, a=an,
                    sol=['Common chord: subtract the equations → x = \\f{d^{2} + r_{1}^{2} − r_{2}^{2}}{2d}.', f'x = {fr(x)}, PQ^{{2}} = 4(r_{{1}}^{{2}} − x^{{2}}) = {fr(L2)}.'], p=dict(t=t, r1=r1, r2=r2, d=d))
    if t == 'c_touch':
        a, b, n = rng.choice(PYT); h, k = rng.randint(-3, 3), rng.randint(-3, 3); r1 = rng.randint(1, n - 1); ext = rng.choice([True, False])
        r2 = n - r1 if ext else n + r1
        return dict(q=f'The circle with centre ({h + a}, {k + b}) touches the circle (x {sgn(-h)})^{{2}} + (y {sgn(-k)})^{{2}} = {r1 * r1} {"externally" if ext else "internally (the given circle lies inside it)"}. Its radius is ____.'.replace('+ 0)', ')').replace('− 0)', ')'), o=None, a=r2,
                    sol=[f'Distance between centres = {n}.', f'{"r_{1} + r_{2}" if ext else "r_{2} − r_{1}"} = {n} → r_{{2}} = {r2}.'], p=dict(t=t, C1=[h, k], r1=r1, C2=[h + a, k + b], ext=ext))
    if t == 'c_three':
        h, k = rng.randint(-4, 4), rng.randint(-4, 4); a, b, r = rng.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (0, 5, 5)])
        pts = list({(h + sa * x, k + sb * y) for x, y in ((a, b), (b, a), (r, 0), (0, r)) for sa in (1, -1) for sb in (1, -1)}); rng.shuffle(pts); P3 = pts[:3]
        need(area(*P3) > 1)
        return dict(q=f'The circle through ({P3[0][0]}, {P3[0][1]}), ({P3[1][0]}, {P3[1][1]}) and ({P3[2][0]}, {P3[2][1]}) has radius r. Then r^{{2}} = ____.', o=None, a=r * r,
                    sol=['The centre is where the perpendicular bisectors of two chords meet.', f'Centre ({h}, {k}) → r^{{2}} = {r * r}.'], p=dict(t=t, P=P3))
    h, k, r = rng.randint(-5, 6), rng.randint(-5, 6), rng.randint(1, 6)
    return dict(q=f'A square is inscribed in the circle (x {sgn(-h)})^{{2}} + (y {sgn(-k)})^{{2}} = {r * r}. If (x_{{i}}, y_{{i}}) are its vertices, Σ(x_{{i}}^{{2}} + y_{{i}}^{{2}}) = ____.'.replace('+ 0)', ')').replace('− 0)', ')'), o=None, a=4 * (h * h + k * k + r * r),
                sol=['Vertices are c + u, c + v, c − u, c − v with |u| = |v| = r: the cross terms cancel.', f'4(|c|^{{2}} + r^{{2}}) = {4 * (h * h + k * k + r * r)}.'], p=dict(t='c_square', h=h, k=k, r=r))

def g_parab(rng):
    t = rng.choice(['p_focal', 'p_flen', 'p_tan', 'p_mid', 'p_dist'])
    a = rng.randint(1, 6)
    if t == 'p_focal':
        tt = rng.choice([F(1), F(2), F(1, 2), F(3), F(1, 3), F(-2), F(-1, 2), F(4)]); x1, y1 = a * tt * tt, 2 * a * tt; t2 = -1 / tt; x2, y2 = a * t2 * t2, 2 * a * t2
        need(x2.denominator == 1 and y2.denominator == 1)
        return dict(q=f'One end of a focal chord of y^{{2}} = {4 * a}x is ({fr(x1)}, {fr(y1)}). If the other end is (α, β), then α + β = ____.', o=None, a=int(x2 + y2),
                    sol=['Ends of a focal chord have parameters t and −\\f{1}{t}.', f'Other end ({fr(x2)}, {fr(y2)}) → {int(x2 + y2)}.'], p=dict(t=t, a=a, P=[float(x1), float(y1)]))
    if t == 'p_flen':
        tt = rng.choice([1, 2, 3, F(1, 2)]); L = a * (tt + 1 / F(tt)) ** 2; need(L.denominator == 1)
        return dict(q=f'The length of the focal chord of y^{{2}} = {4 * a}x through the point ({fr(a * F(tt) ** 2)}, {fr(2 * a * F(tt))}) is ____.', o=None, a=int(L),
                    sol=['Focal chord with ends t, −\\f{1}{t}: length a(t + \\f{1}{t})^{2}.', f'= {int(L)}.'], p=dict(t=t, a=a, tt=float(tt)))
    if t == 'p_tan':
        m = rng.choice([1, 2, -1, -2, F(1, 2), F(-1, 2)]); X, Y = a / F(m) ** 2, 2 * a / F(m); need(X.denominator == 1 and Y.denominator == 1)
        return dict(q=f'The tangent of slope {fr(m)} to y^{{2}} = {4 * a}x touches it at (α, β). Then α + β = ____.', o=None, a=int(X + Y),
                    sol=['y = mx + \\f{a}{m} touches at (\\f{a}{m^{2}}, \\f{2a}{m}).', f'({fr(X)}, {fr(Y)}) → {int(X + Y)}.'], p=dict(t=t, a=a, m=float(m)))
    if t == 'p_mid':
        h, k = rng.randint(1, 8), rng.choice([1, 2, 3, 4, -1, -2, -3]); need(k * k < 4 * a * h)
        slope = F(2 * a, k); c = k - slope * h   # chord: y − k = (2a/k)(x − h)
        return dict(q=f'The chord of y^{{2}} = {4 * a}x with mid-point ({h}, {k}) meets the y-axis at (0, c). Then c =', o=(lambda o: o)(mcq(rng, fr(c), [fr(-c), fr(c + 1), fr(slope), fr(c * 2)])[0]), a=None,
                    sol=['T = S_{1}: ky − 2a(x + h) = k^{2} − 4ah, i.e. slope \\f{2a}{k} through the mid-point.', f'c = k − \\f{{2a}}{{k}}h = {fr(c)}.'], p=dict(t=t, a=a, h=h, k=k))
    m = rng.choice([1, 2, -1, F(1, 2), -2]); X, Y = a / F(m) ** 2, 2 * a / F(m); need(X.denominator == 1 and Y.denominator == 1)
    cx, cy = int(X) + rng.choice([-3, 0, 3, 4, -4]), int(Y) + rng.choice([-4, 0, 4, 3]); d2 = (cx - X) ** 2 + (cy - Y) ** 2; need(d2)
    return dict(q=f'A line of slope {fr(m)} touches y^{{2}} = {4 * a}x at P. If Q = ({cx}, {cy}), then PQ^{{2}} = ____.', o=None, a=int(d2),
                sol=['Contact point of the tangent of slope m: (\\f{a}{m^{2}}, \\f{2a}{m}).', f'P = ({fr(X)}, {fr(Y)}) → PQ^{{2}} = {int(d2)}.'], p=dict(t='p_dist', a=a, m=float(m), Q=[cx, cy]))

def g_ellhyp(rng):
    t = rng.choice(['e_lr', 'e_focal', 'e_tan', 'h_lr', 'h_tan', 'e_mid', 'h_focal', 'e_sum', 'e_ecc', 'h_ecc', 'e_dir', 'e_quad', 'h_foc'])
    if t in ('e_ecc', 'h_ecc', 'e_dir', 'e_quad', 'h_foc'):
        b, c, a = rng.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25), (20, 21, 29), (21, 20, 29)]); k = rng.randint(1, 3)
        if t == 'e_ecc':
            v = F(c * c, a * a); a, b = a * k, b * k
            o, an = mcq(rng, fr(v), [fr(F(b * b, a * a)), fr(1 - v + F(1, 10)), fr(F(c, a // k)), fr(F(a * a, b * b))])
            return dict(q=f'If e is the eccentricity of \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1, then e^{{2}} =', o=o, a=an, sol=['e^{2} = 1 − \\f{b^{2}}{a^{2}}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b))
        if t == 'h_ecc':
            A, B = b * k, c * k; v = F(a * a, b * b)
            o, an = mcq(rng, fr(v), [fr(F(c * c, b * b)), fr(F(a, b)), fr(v + 1), fr(F(b * b, a * a))])
            return dict(q=f'If e is the eccentricity of \\f{{x^{{2}}}}{{{A * A}}} − \\f{{y^{{2}}}}{{{B * B}}} = 1, then e^{{2}} =', o=o, a=an, sol=['e^{2} = 1 + \\f{b^{2}}{a^{2}}.', f'= {fr(v)}.'], p=dict(t=t, a=A, b=B))
        a, b, c = a * k, b * k, c * k
        if t == 'e_dir':
            v = F(2 * a * a, c); o, an = mcq(rng, fr(v), [fr(F(2 * c * c, a)), fr(F(a * a, c)), fr(2 * c), fr(F(2 * b * b, a))])
            return dict(q=f'The distance between the directrices of \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1 is', o=o, a=an, sol=['Directrices x = ±\\f{a}{e} = ±\\f{a^{2}}{ae}.', f'Distance \\f{{2a^{{2}}}}{{ae}} = {fr(v)}.'], p=dict(t=t, a=a, b=b))
        if t == 'e_quad':
            v = F(2 * c * 2 * b * b, a); o, an = mcq(rng, fr(v), [fr(v / 2), fr(F(4 * c * b, 1)), fr(F(2 * c * b * b, a)), fr(v + 2)])
            return dict(q=f'The area of the quadrilateral whose vertices are the ends of the two latera recta of \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1 is', o=o, a=an, sol=['A rectangle of width 2ae and height \\f{2b^{2}}{a}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b))
        A, B = b, c   # hyperbola x²/A² − y²/B² = 1 with focal distance 2a
        return dict(q=f'The distance between the foci of \\f{{x^{{2}}}}{{{A * A}}} − \\f{{y^{{2}}}}{{{B * B}}} = 1 is ____.', o=None, a=2 * a, sol=['Foci (±ae, 0) with a^{2}e^{2} = a^{2} + b^{2}.', f'2√{{{A * A} + {B * B}}} = {2 * a}.'], p=dict(t=t, a=A, b=B))
    if t in ('e_lr', 'e_focal', 'e_tan', 'e_mid', 'e_sum'):
        b, c, a = rng.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25)]); k = rng.choice([1, 1, 2, 3]); a, b, c = a * k, b * k, c * k
        if t == 'e_lr':
            v = F(2 * b * b, a); o, an = mcq(rng, fr(v), [fr(F(2 * a * a, b)), fr(F(b * b, a)), fr(v + 1), fr(F(2 * c * c, a))])
            return dict(q=f'The length of the latus rectum of \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1 is', o=o, a=an, sol=['\\f{2b^{2}}{a}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b))
        if t == 'e_focal':
            x0 = rng.choice([0, F(a, 2), F(a, 5), F(3 * a, 5), F(4 * a, 5), a]); v = a * a - F(c * c, a * a) * x0 * x0; need(v.denominator == 1)
            y0sq = b * b * (1 - x0 * x0 / (a * a))
            return dict(q=f'P is a point on \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1 with x-coordinate {fr(x0)}. The product of its focal distances is ____.', o=None, a=int(v),
                        sol=['Focal distances a ± ex: product a^{2} − e^{2}x^{2}.', f'{a * a} − \\f{{{c * c}}}{{{a * a}}}·{fr(x0 * x0)} = {int(v)}.'], p=dict(t=t, a=a, b=b, x0=float(x0)))
        if t == 'e_sum':
            return dict(q=f'For any point on \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1, the sum of its distances from the foci is ____.', o=None, a=2 * a, sol=['Sum of focal distances = 2a (major axis).', f'= {2 * a}.'], p=dict(t=t, a=a, b=b))
        if t == 'e_tan':
            m = rng.randint(-4, 4); v = a * a * m * m + b * b
            return dict(q=f'The line y = {m if m not in (1, -1) else ("" if m == 1 else "−")}x + c touches \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1. Then c^{{2}} = ____.'.replace('y = 0x + c', 'y = c').replace('= −x', '= −x').replace('y = -', 'y = −'), o=None, a=v,
                        sol=['Tangency: c^{2} = a^{2}m^{2} + b^{2}.', f'= {v}.'], p=dict(t=t, a=a, b=b, m=m))
        h0, k0 = rng.randint(1, max(1, a // 2)), rng.randint(1, max(1, b // 2))
        sl = -F(b * b * h0, a * a * k0); c0 = k0 - sl * h0
        o, an = mcq(rng, fr(sl), [fr(-sl), fr(1 / sl), fr(-1 / sl), fr(sl * 2)])
        return dict(q=f'The slope of the chord of \\f{{x^{{2}}}}{{{a * a}}} + \\f{{y^{{2}}}}{{{b * b}}} = 1 whose mid-point is ({h0}, {k0}) is', o=o, a=an,
                    sol=['T = S_{1}: \\f{hx}{a^{2}} + \\f{ky}{b^{2}} = \\f{h^{2}}{a^{2}} + \\f{k^{2}}{b^{2}} → slope −\\f{b^{2}h}{a^{2}k}.', f'= {fr(sl)}.'], p=dict(t='e_mid', a=a, b=b, h=h0, k=k0))
    a, b, c = rng.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17), (20, 21, 29), (21, 20, 29), (7, 24, 25), (24, 7, 25), (9, 12, 15), (12, 9, 15)])
    if t == 'h_lr':
        v = F(2 * b * b, a); o, an = mcq(rng, fr(v), [fr(F(2 * a * a, b)), fr(F(b * b, a)), fr(v + 1), fr(F(2 * c * c, a))])
        return dict(q=f'The length of the latus rectum of \\f{{x^{{2}}}}{{{a * a}}} − \\f{{y^{{2}}}}{{{b * b}}} = 1 is', o=o, a=an, sol=['\\f{2b^{2}}{a}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b))
    if t == 'h_tan':
        m = rng.randint(1, 5) * rng.choice([1, -1]); v = a * a * m * m - b * b; need(v > 0)
        return dict(q=f'The line y = {m if m not in (1, -1) else ("" if m == 1 else "−")}x + c touches \\f{{x^{{2}}}}{{{a * a}}} − \\f{{y^{{2}}}}{{{b * b}}} = 1. Then c^{{2}} = ____.'.replace('y = -', 'y = −'), o=None, a=v,
                    sol=['Tangency: c^{2} = a^{2}m^{2} − b^{2}.', f'= {v}.'], p=dict(t=t, a=a, b=b, m=m))
    x0 = rng.choice([a, 2 * a, F(5 * a, 4), F(13 * a, 12), 3 * a]); v = F(c * c, a * a) * x0 * x0 - a * a; need(v.denominator == 1)
    return dict(q=f'P is a point on \\f{{x^{{2}}}}{{{a * a}}} − \\f{{y^{{2}}}}{{{b * b}}} = 1 with x-coordinate {fr(x0)}. The product of its focal distances is ____.', o=None, a=int(v),
                sol=['Focal distances ex ± a: product e^{2}x^{2} − a^{2}.', f'= {int(v)}.'], p=dict(t='h_focal', a=a, b=b, x0=float(x0)))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try:
                it = gf(rng)
                if it.get('o') and it['a'] is None: it['a'] = it['o'].index(fr(_mid_c(it['p'])))
                return it
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
def _mid_c(p): return p['k'] - F(2 * p['a'], p['k']) * p['h']
GEN = {k: robust(v) for k, v in dict(line=g_line, circle=g_circle, parab=g_parab, ellhyp=g_ellhyp).items()}
def finish(it): return it
def close(a, b, tol=1e-6): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = tofr(R) if isinstance(R, str) else R
    if t == 'l_par':   # pick a point on line 1, measure to line 2
        a, b = p['a'], p['b']; pt = (p['c1'] / a, 0) if a else (0, p['c1'] / b); return close(V, abs(a * pt[0] + b * pt[1] - p['c2']) / math.hypot(a, b))
    if t == 'l_pt':
        a, b, c = p['a'], p['b'], p['c']; foot_t = (a * p['P'][0] + b * p['P'][1] - c) / (a * a + b * b); return close(V, math.hypot(a * foot_t, b * foot_t))
    if t == 'l_ortho':
        H = ortho(*[tuple(map(float, v)) for v in p['V']]); A, B, C = p['V']
        ok = abs((H[0] - A[0]) * (C[0] - B[0]) + (H[1] - A[1]) * (C[1] - B[1])) < 1e-6 and abs((H[0] - B[0]) * (C[0] - A[0]) + (H[1] - B[1]) * (C[1] - A[1])) < 1e-6
        return ok and close(V, H[0] + H[1])
    if t == 'l_inc':
        A, B, C = p['V']; a, b, c = dist(B, C), dist(A, C), dist(A, B); I = ((a * A[0] + b * B[0] + c * C[0]) / (a + b + c), (a * A[1] + b * B[1] + c * C[1]) / (a + b + c)); return close(V, I[0] + I[1])
    if t == 'l_refl':
        a, b, c = p['a'], p['b'], p['c']; P0 = p['P']; best = None
        for x in range(-40, 41):
            for y in range(-40, 41):
                M = ((x + P0[0]) / 2, (y + P0[1]) / 2)
                if abs(a * M[0] + b * M[1] - c) < 1e-9 and abs((x - P0[0]) * b - (y - P0[1]) * a) < 1e-9 and (x, y) != tuple(P0): best = (x, y)
        return best is not None and V == best[0] + best[1]
    if t == 'l_minarea':
        px, py = p['px'], p['py']; return close(V, min((px + py / m) * (py + px * m) / 2 for m in [k / 2000 for k in range(1, 40000)]), 1e-4)
    if t == 'c_chord':
        h, k, r, a, b, c = p['h'], p['k'], p['r'], p['a'], p['b'], p['c']
        if b: xs = qr(1 + (a / b) ** 2, -2 * h - 2 * (a / b) * (c / b - k), h * h + (c / b - k) ** 2 - r * r); pts = [(x, (c - a * x) / b) for x in xs]
        else: ys = qr(1, -2 * k, k * k + (c / a - h) ** 2 - r * r); pts = [(c / a, y) for y in ys]
        return len(pts) == 2 and close(V, dist(*pts))
    if t == 'c_tlen':
        g, f_, c = p['g'], p['f'], p['c']; C = (-g, -f_); r2 = g * g + f_ * f_ - c; return close(V, dist(p['P'], C) ** 2 - r2)
    if t == 'c_common':
        r1, r2, d = p['r1'], p['r2'], p['d']; pts = [(r1 * math.cos(th), r1 * math.sin(th)) for th in [k * 2 * math.pi / 200000 for k in range(200000)]]
        on = [q for q in pts if abs(math.hypot(q[0] - d, q[1]) - r2) < 2e-3]; ys = [q[1] for q in on]; return close(V, (max(ys) - min(ys)) ** 2, 1e-2)
    if t == 'c_touch':
        D = dist(p['C1'], p['C2']); r2 = R
        return (abs(D - (p['r1'] + r2)) < 1e-9) if p['ext'] else (abs(D - (r2 - p['r1'])) < 1e-9)
    if t == 'c_three':
        A, B, C = [tuple(map(float, q)) for q in p['P']]
        O = inter((B[0] - A[0], B[1] - A[1], (B[0] ** 2 - A[0] ** 2 + B[1] ** 2 - A[1] ** 2) / 2), (C[0] - A[0], C[1] - A[1], (C[0] ** 2 - A[0] ** 2 + C[1] ** 2 - A[1] ** 2) / 2)); return close(V, dist(O, A) ** 2)
    if t == 'c_square':
        h, k, r = p['h'], p['k'], p['r']; th = 0.37; return close(V, sum((h + r * math.cos(th + j * math.pi / 2)) ** 2 + (k + r * math.sin(th + j * math.pi / 2)) ** 2 for j in range(4)))
    if t == 'p_focal':
        a = p['a']; P0 = p['P']; S = (a, 0)
        if abs(P0[0] - a) < 1e-12: return close(V, a - P0[1])
        m = P0[1] / (P0[0] - a); ys = qr(1, -4 * a / m, -4 * a * a); other = [y for y in ys if abs(y - P0[1]) > 1e-6][0]; return close(V, other * other / (4 * a) + other)
    if t == 'p_flen':
        a, tt = p['a'], p['tt']; P0 = (a * tt * tt, 2 * a * tt)
        if abs(P0[0] - a) < 1e-12: return close(V, 4 * a)
        m = P0[1] / (P0[0] - a); ys = qr(1, -4 * a / m, -4 * a * a); pts = [(y * y / (4 * a), y) for y in ys]; return close(V, dist(*pts))
    if t == 'p_tan':
        a, m = p['a'], p['m']; c = a / m; xs = qr(m * m, 2 * m * c - 4 * a, c * c); x = sum(xs) / 2; return close(V, x + m * x + c)
    if t == 'p_mid':
        a, h, k = p['a'], p['h'], p['k']; c = float(V); s = (k - c) / h   # the line through (h, k) and (0, c)
        ys = qr(s, -4 * a, 4 * a * c); xs = [(y - c) / s for y in ys]
        return len(ys) == 2 and abs(sum(ys) / 2 - k) < 1e-9 and abs(sum(xs) / 2 - h) < 1e-9
    if t == 'p_dist':
        a, m = p['a'], p['m']; c = a / m; xs = qr(m * m, 2 * m * c - 4 * a, c * c); x = sum(xs) / 2; return close(V, dist((x, m * x + c), p['Q']) ** 2)
    if t in ('e_lr', 'h_lr'):
        a, b = p['a'], p['b']; c = math.sqrt(a * a - b * b) if t == 'e_lr' else math.sqrt(a * a + b * b)
        yy = b * math.sqrt(max(1 - c * c / (a * a), 0)) if t == 'e_lr' else b * math.sqrt(c * c / (a * a) - 1); return close(V, 2 * yy)
    if t in ('e_focal', 'h_focal'):
        a, b, x0 = p['a'], p['b'], p['x0']; c = math.sqrt(a * a - b * b) if t == 'e_focal' else math.sqrt(a * a + b * b)
        y0 = b * math.sqrt(max(1 - x0 * x0 / (a * a), 0)) if t == 'e_focal' else b * math.sqrt(x0 * x0 / (a * a) - 1); return close(V, dist((x0, y0), (c, 0)) * dist((x0, y0), (-c, 0)))
    if t == 'e_sum':
        a, b = p['a'], p['b']; c = math.sqrt(a * a - b * b); P0 = (a * math.cos(0.7), b * math.sin(0.7)); return close(V, dist(P0, (c, 0)) + dist(P0, (-c, 0)))
    if t in ('e_tan', 'h_tan'):
        a, b, m = p['a'], p['b'], p['m']; s = 1 if t == 'e_tan' else -1; c2 = V   # discriminant of x²/a² ± (mx + c)²/b² = 1 must vanish
        A_ = 1 / a ** 2 + s * m * m / b ** 2; c = math.sqrt(c2); B_ = s * 2 * m * c / b ** 2; C_ = s * c * c / b ** 2 - 1; return abs(B_ * B_ - 4 * A_ * C_) < 1e-9 * max(1, abs(B_ * B_))
    if t == 'e_mid':
        a, b, h, k = p['a'], p['b'], p['h'], p['k']; m = float(V); c = k - m * h
        xs = qr(1 / a ** 2 + m * m / b ** 2, 2 * m * c / b ** 2, c * c / b ** 2 - 1); return len(xs) == 2 and abs(sum(xs) / 2 - h) < 1e-9
    if t in ('e_ecc', 'h_ecc'):
        a, b = p['a'], p['b']; c = math.sqrt(a * a - b * b) if t == 'e_ecc' else math.sqrt(a * a + b * b)
        P0 = (a * math.cos(1.1), b * math.sin(1.1)) if t == 'e_ecc' else (a / math.cos(1.1), b * math.tan(1.1))
        dd = a * a / c; return close(math.sqrt(float(V)), dist(P0, (c, 0)) / abs(P0[0] - dd))   # focus–directrix ratio
    if t == 'e_dir':
        a, b = p['a'], p['b']; c = math.sqrt(a * a - b * b); P0 = (a * math.cos(0.9), b * math.sin(0.9))
        # directrix x = d is where PS/PM is constant: find d from two points
        P1 = (a * math.cos(2.0), b * math.sin(2.0)); r0, r1 = dist(P0, (c, 0)), dist(P1, (c, 0)); d = (r1 * P0[0] - r0 * P1[0]) / (r1 - r0); return close(V, 2 * d)
    if t == 'e_quad':
        a, b = p['a'], p['b']; c = math.sqrt(a * a - b * b); y = b * math.sqrt(1 - c * c / (a * a)); return close(V, area((c, y), (c, -y), (-c, -y), (-c, y)))
    if t == 'h_foc':
        a, b = p['a'], p['b']; P0 = (a / math.cos(0.8), b * math.tan(0.8))
        lo, hi = a + 1e-9, 1e4
        for _ in range(200):
            m = (lo + hi) / 2
            if abs(dist(P0, (m, 0)) - dist(P0, (-m, 0))) < 2 * a: lo = m
            else: hi = m
        return close(V, 2 * lo, 1e-6)
    raise KeyError(t)
