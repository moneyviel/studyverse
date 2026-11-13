"""Practice generators — Mathematics Unit 12: Vector Algebra. Items are built from integer vectors with the answer
planted by construction; check() re-solves each a different way — angles by the cosine rule on the triangle the
vectors make, projections by minimising |a − t b|, unknown vectors by Gaussian elimination on the stated
conditions, areas by Heron's formula and volumes by expanding the determinant."""
import math, re
from fractions import Fraction as F
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
QD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15)]
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def addv(a, b, k=1): return tuple(x + k * y for x, y in zip(a, b))
def sc(k, a): return tuple(k * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(dot(a, a))
def rv(rng, lo=-4, hi=4): return tuple(rng.randint(lo, hi) for _ in range(3))
def signed(rng, q): o = list(q[:3]); rng.shuffle(o); return tuple(x * rng.choice([1, -1]) for x in o)
def vec(d):
    s = ''
    for c, u in zip(d, ('î', 'ĵ', 'k̂')):
        c = F(c)
        if c == 0: continue
        t = ('' if abs(c) == 1 else fr(abs(c))) + u
        s += (' − ' if c < 0 else ' + ') + t if s else ('−' if c < 0 else '') + t
    return s or '0⃗'
def lc(m, n):   # m a + n b as text
    t = ('−' if m < 0 else '') + ('' if abs(m) == 1 else str(abs(m))) + 'a⃗'
    return t + (' + ' if n > 0 else ' − ') + ('' if abs(n) == 1 else str(abs(n))) + 'b⃗'
def pt(A): return '(' + ', '.join(fr(F(a)) for a in A) + ')'

def g_dot(rng):
    t = rng.choice(['d_cos', 'd_proj', 'd_perp', 'd_mag', 'd_comp', 'd_lam', 'd_bis'])
    if t == 'd_cos':
        q1, q2 = rng.sample(QD, 2); a, b = signed(rng, q1), signed(rng, q2); c = F(dot(a, b), q1[3] * q2[3]); need(c != 0 and abs(c) != 1)
        o, an = mcq(rng, fr(c), [fr(-c), fr(c + F(1, q1[3] * q2[3])), fr(c / 2), fr(F(dot(a, b), q1[3] * q2[3] + 1))])
        return dict(q=f'If θ is the angle between a⃗ = {vec(a)} and b⃗ = {vec(b)}, then cos θ =', o=o, a=an, sol=['cos θ = \\f{a⃗·b⃗}{|a⃗||b⃗|}.', f'a⃗·b⃗ = {dot(a, b)}, |a⃗| = {q1[3]}, |b⃗| = {q2[3]} → {fr(c)}.'], p=dict(t=t, a=a, b=b))
    if t == 'd_proj':
        q = rng.choice(QD); b = signed(rng, q); a = rv(rng, -6, 6); v = F(dot(a, b), q[3]); need(v != 0)
        o, an = mcq(rng, fr(v), [fr(-v), fr(F(dot(a, b), q[3] ** 2)), fr(v + 1), fr(F(dot(a, b) + 1, q[3]))])
        return dict(q=f'The projection (scalar component) of a⃗ = {vec(a)} on b⃗ = {vec(b)} is', o=o, a=an, sol=['Projection = \\f{a⃗·b⃗}{|b⃗|}.', f'a⃗·b⃗ = {dot(a, b)}, |b⃗| = {q[3]} → {fr(v)}.'], p=dict(t=t, a=a, b=b))
    if t == 'd_perp':
        a = rv(rng); need(a[2] != 0 and a[1] != 0); bx = rng.randint(-4, 4); lam = rng.randint(-6, 6)
        c = -(a[0] * bx + a[2] * lam); need(c % a[1] == 0); b = (bx, c // a[1], lam); need(dot(a, b) == 0 and max(map(abs, b)) <= 12 and (b[0] or b[1]))
        return dict(q=f'If the vectors {vec(a)} and {vec((b[0], b[1], 0))} + λk̂ are perpendicular, then λ = ____.', o=None, a=lam,
                    sol=['Perpendicular ⇔ dot product 0.', f'{a[0] * b[0] + a[1] * b[1]} {"+" if a[2] > 0 else "−"} {abs(a[2]) if abs(a[2]) != 1 else ""}λ = 0 → λ = {lam}.'], p=dict(t=t, a=a, b2=(b[0], b[1])))
    if t == 'd_mag':
        p_, q_ = rng.randint(1, 6), rng.randint(1, 6); ang = rng.choice([60, 120, 90, 180, 0]); cs = {60: F(1, 2), 120: F(-1, 2), 90: F(0), 180: F(-1), 0: F(1)}[ang]
        m, n = rng.choice([(1, 1), (2, 1), (1, -1), (3, 2), (2, -3), (1, 2)]); v = m * m * p_ * p_ + n * n * q_ * q_ + 2 * m * n * p_ * q_ * cs; need(v.denominator == 1)
        return dict(q=f'|a⃗| = {p_}, |b⃗| = {q_} and the angle between them is {ang}°. Then |{"" if m == 1 else m}a⃗ {"+" if n > 0 else "−"} {"" if abs(n) == 1 else abs(n)}b⃗|^{{2}} = ____.', o=None, a=int(v),
                    sol=['|ma⃗ + nb⃗|^{2} = m^{2}|a⃗|^{2} + n^{2}|b⃗|^{2} + 2mn a⃗·b⃗.', f'a⃗·b⃗ = {fr(p_ * q_ * cs)} → {int(v)}.'], p=dict(t=t, P=p_, Q=q_, ang=ang, m=m, n=n))
    if t == 'd_comp':
        b = rv(rng, -3, 3); need(dot(b, b)); a = rv(rng, -6, 6); k = F(dot(a, b), dot(b, b)); perp = tuple(F(x) - k * y for x, y in zip(a, b)); v = dot(perp, perp)
        o, an = mcq(rng, fr(v), [fr(v + 1), fr(F(dot(a, a))), fr(k * k * dot(b, b)), fr(v * 2 if v else 1)])
        return dict(q=f'If a⃗ = {vec(a)} is written as a part along b⃗ = {vec(b)} plus a part perpendicular to b⃗, the square of the length of the perpendicular part is', o=o, a=an,
                    sol=['Along part = \\f{a⃗·b⃗}{|b⃗|^{2}}b⃗; perpendicular part = a⃗ − that.', f'|perp|^{{2}} = |a⃗|^{{2}} − \\f{{(a⃗·b⃗)^{{2}}}}{{|b⃗|^{{2}}}} = {dot(a, a)} − \\f{{{dot(a, b) ** 2}}}{{{dot(b, b)}}} = {fr(v)}.'], p=dict(t=t, a=a, b=b))
    if t == 'd_lam':
        a, b = rv(rng, -3, 3), rv(rng, -3, 3); need(dot(a, a) and dot(b, b))
        # (a + λb)·(a − b) = 0 → λ = (a·b − |a|²) / (|b|² − a·b) … ask when it is an integer
        need(dot(a, b) != dot(b, b))
        lam = F(dot(a, b) - dot(a, a), dot(a, b) - dot(b, b)); need(lam.denominator == 1)
        return dict(q=f'If a⃗ = {vec(a)}, b⃗ = {vec(b)} and a⃗ + λb⃗ is perpendicular to a⃗ − b⃗, then λ = ____.', o=None, a=int(lam),
                    sol=['(a⃗ + λb⃗)·(a⃗ − b⃗) = |a⃗|^{2} − a⃗·b⃗ + λ(a⃗·b⃗ − |b⃗|^{2}) = 0.', f'{dot(a, a)} − {dot(a, b)} + λ({dot(a, b)} − {dot(b, b)}) = 0 → λ = {int(lam)}.'.replace('− -', '+ ')], p=dict(t=t, a=a, b=b))
    q1, q2 = rng.sample(QD, 2); a, b = signed(rng, q1), signed(rng, q2); u = addv(sc(q2[3], a), sc(q1[3], b)); need(nrm(cross(a, b)) > 0)
    g = math.gcd(*[abs(x) for x in u]); need(g); u = tuple(x // g for x in u)
    wr = [addv(a, b), sub(sc(q2[3], a), sc(q1[3], b)), cross(a, b), addv(u, (1, 0, 0))]; wr = [w for w in wr if nrm(cross(w, u)) > 1e-9]
    o, an = mcq(rng, pt(u), [pt(w) for w in wr])
    return dict(q=f'A vector along the bisector of the angle between a⃗ = {vec(a)} and b⃗ = {vec(b)} is parallel to', o=o, a=an,
                sol=['The internal bisector is along â + b̂ (sum of unit vectors).', f'\\f{{a⃗}}{{{q1[3]}}} + \\f{{b⃗}}{{{q2[3]}}} ∥ {pt(u)}.'], p=dict(t='d_bis', a=a, b=b))

def g_cross(rng):
    t = rng.choice(['x_tri', 'x_par', 'x_solve', 'x_box', 'x_bac', 'x_lag', 'x_diag', 'x_ac'])
    if t == 'x_tri':
        A, B, C = rv(rng), rv(rng), rv(rng); n = cross(sub(B, A), sub(C, A)); v = F(dot(n, n), 4); need(v)
        o, an = mcq(rng, fr(v), [fr(v * 4), fr(v * 2), fr(v + 1), fr(F(dot(n, n), 2) + 1)])
        return dict(q=f'The square of the area of the triangle with vertices A{pt(A)}, B{pt(B)} and C{pt(C)} is', o=o, a=an,
                    sol=['Area = \\f{1}{2}|AB⃗ × AC⃗|.', f'AB⃗ × AC⃗ = {pt(n)} → area^{{2}} = \\f{{{dot(n, n)}}}{{4}} = {fr(v)}.'], p=dict(t=t, V=(A, B, C)))
    if t == 'x_par':
        a, b = rv(rng, -3, 3), rv(rng, -3, 3); n = cross(a, b); need(dot(n, n)); m1, n1, m2, n2 = [rng.choice([1, 2, 3, -1, -2]) for _ in range(4)]; k = m1 * n2 - n1 * m2; need(k)
        v = k * k * dot(n, n)
        return dict(q=f'If a⃗ = {vec(a)} and b⃗ = {vec(b)}, the square of the area of the parallelogram with adjacent sides {lc(m1, n1)} and {lc(m2, n2)} is ____.', o=None, a=v,
                    sol=[f'(m_{{1}}a⃗ + n_{{1}}b⃗) × (m_{{2}}a⃗ + n_{{2}}b⃗) = (m_{{1}}n_{{2}} − n_{{1}}m_{{2}})(a⃗ × b⃗) = {k}(a⃗ × b⃗).', f'a⃗ × b⃗ = {pt(n)} → area^{{2}} = {k * k}·{dot(n, n)} = {v}.'], p=dict(t=t, a=a, b=b, s=(m1, n1, m2, n2)))
    if t == 'x_solve':
        a, b = rv(rng, -3, 3), rv(rng, -3, 3); p_, q_ = rng.choice([(2, 3), (1, 2), (3, 1), (1, -2), (2, -1)]); u = addv(sc(p_, a), sc(q_, b)); need(dot(u, u) and nrm(cross(a, b)))
        w = rv(rng, -3, 3); need(dot(w, u)); tt = rng.choice([1, 2, -1, -2, 3]); K = tt * dot(w, u); c = sc(tt, u); z = rv(rng, -2, 2); need(dot(z, z))
        return dict(q=f'a⃗ = {vec(a)}, b⃗ = {vec(b)} and c⃗ satisfies {p_}(a⃗ × c⃗) {"+" if q_ > 0 else "−"} {abs(q_)}(b⃗ × c⃗) = 0⃗ and c⃗·({vec(w)}) = {K}. Then c⃗·({vec(z)}) = ____.'.replace('1(', '('), o=None, a=dot(c, z),
                    sol=[f'({p_}a⃗ + {q_}b⃗) × c⃗ = 0 → c⃗ = t{pt(u)}.'.replace('+ -', '− '), f'The dot condition gives t = {tt}: c⃗ = {pt(c)} → {dot(c, z)}.'], p=dict(t=t, a=a, b=b, pq=(p_, q_), w=w, K=K, z=z))
    if t == 'x_box':
        a, b, c = rv(rng, -3, 3), rv(rng, -3, 3), rv(rng, -3, 3); V = dot(a, cross(b, c)); need(V)
        o, an = mcq(rng, str(abs(V)), [str(abs(V) + 1), str(2 * abs(V)), str(abs(V) - 1) if abs(V) > 1 else '13', str(abs(dot(a, b)) + 20)])
        return dict(q=f'The volume of the parallelepiped with coterminous edges {vec(a)}, {vec(b)} and {vec(c)} is', o=o, a=an,
                    sol=['Volume = |[a⃗ b⃗ c⃗]| = |a⃗·(b⃗ × c⃗)|.', f'b⃗ × c⃗ = {pt(cross(b, c))} → |{V}| = {abs(V)}.'.replace('|-', '|−')], p=dict(t=t, a=a, b=b, c=c))
    if t == 'x_bac':
        a, b, c = rv(rng, -3, 3), rv(rng, -3, 3), rv(rng, -3, 3); r = sub(sc(dot(a, c), b), sc(dot(a, b), c)); need(sum(r) != 0 or True)
        return dict(q=f'If a⃗ = {vec(a)}, b⃗ = {vec(b)}, c⃗ = {vec(c)} and a⃗ × (b⃗ × c⃗) = xî + yĵ + zk̂, then x + y + z = ____.', o=None, a=sum(r),
                    sol=['a⃗ × (b⃗ × c⃗) = (a⃗·c⃗)b⃗ − (a⃗·b⃗)c⃗.', f'a⃗·c⃗ = {dot(a, c)}, a⃗·b⃗ = {dot(a, b)} → {pt(r)} → {sum(r)}.'], p=dict(t=t, a=a, b=b, c=c))
    if t == 'x_lag':
        p_, q_ = rng.randint(1, 8), rng.randint(1, 8); d = rng.randint(-p_ * q_ + 1, p_ * q_ - 1); v = p_ * p_ * q_ * q_ - d * d
        return dict(q=f'If |a⃗| = {p_}, |b⃗| = {q_} and a⃗·b⃗ = {d}, then |a⃗ × b⃗|^{{2}} = ____.', o=None, a=v,
                    sol=['|a⃗ × b⃗|^{2} + (a⃗·b⃗)^{2} = |a⃗|^{2}|b⃗|^{2}.', f'{p_ * p_ * q_ * q_} − {d * d} = {v}.'], p=dict(t=t, P=p_, Q=q_, d=d))
    if t == 'x_diag':
        d1, d2 = rv(rng, -4, 4), rv(rng, -4, 4); n = cross(d1, d2); v = F(dot(n, n), 4); need(v)
        o, an = mcq(rng, fr(v), [fr(v * 4), fr(v * 2), fr(v / 4), fr(v + 1)])
        return dict(q=f'The diagonals of a parallelogram are {vec(d1)} and {vec(d2)}. The square of its area is', o=o, a=an,
                    sol=['Area from diagonals = \\f{1}{2}|d⃗_{1} × d⃗_{2}|.', f'd⃗_{{1}} × d⃗_{{2}} = {pt(n)} → area^{{2}} = \\f{{{dot(n, n)}}}{{4}} = {fr(v)}.'], p=dict(t=t, d1=d1, d2=d2))
    a = rv(rng, -3, 3); need(dot(a, a)); c0 = rv(rng, -3, 3); b = cross(a, c0); need(dot(b, b)); K = dot(a, c0); z = rv(rng, -2, 2); need(dot(z, z))
    return dict(q=f'a⃗ = {vec(a)} and c⃗ satisfies a⃗ × c⃗ = {vec(b)} and a⃗·c⃗ = {K}. Then c⃗·({vec(z)}) = ____.', o=None, a=dot(c0, z),
                sol=['All c⃗ with a⃗ × c⃗ = b⃗ are c⃗_{0} + ta⃗; the dot condition fixes t.', f'c⃗ = {pt(c0)} → {dot(c0, z)}.'], p=dict(t='x_ac', a=a, b=b, K=K, z=z))

def robust(gf):
    def w(rng):
        for _ in range(800):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(dot=g_dot, cross=g_cross).items()}
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
def gsolve(rows, rhs):
    n = len(rows[0]); A = [[sum(r[i] * r[j] for r in rows) for j in range(n)] + [sum(r[i] * b for r, b in zip(rows, rhs))] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c: f = A[r][c] / A[c][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return tuple(A[i][n] / A[i][i] for i in range(n))
def heron(A, B, C):
    a, b, c = math.dist(B, C), math.dist(A, C), math.dist(A, B); s = (a + b + c) / 2; return math.sqrt(max(0, s * (s - a) * (s - b) * (s - c)))
def det3(m): return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'd_cos':   # cosine rule on the triangle with sides a, b, a − b
        a, b = p['a'], p['b']; A, B, C = nrm(a), nrm(b), nrm(sub(a, b)); return close(tofr(R), (A * A + B * B - C * C) / (2 * A * B))
    if t == 'd_proj':   # signed length of the shadow: minimise |a − s b̂| over s
        a, b = p['a'], p['b']; u = sc(1 / nrm(b), b); lo, hi = -100.0, 100.0
        for _ in range(300):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if nrm(sub(a, sc(m1, u))) < nrm(sub(a, sc(m2, u))): hi = m2
            else: lo = m1
        return close(tofr(R), (lo + hi) / 2, 1e-6)
    if t == 'd_perp':
        a, (bx, by) = p['a'], p['b2']; lo, hi = -100.0, 100.0; g = lambda l: dot(a, (bx, by, l))
        for _ in range(200):
            m = (lo + hi) / 2
            if g(lo) * g(m) <= 0: hi = m
            else: lo = m
        return close(R, (lo + hi) / 2)
    if t == 'd_mag':
        th = math.radians(p['ang']); a = (p['P'], 0, 0); b = (p['Q'] * math.cos(th), p['Q'] * math.sin(th), 0); v = addv(sc(p['m'], a), sc(p['n'], b)); return close(R, dot(v, v))
    if t == 'd_comp':
        a, b = p['a'], p['b']   # ternary search for the nearest multiple of b
        L, H = -30.0, 30.0
        for _ in range(300):
            m1, m2 = L + (H - L) / 3, H - (H - L) / 3
            if nrm(sub(a, sc(m1, b))) < nrm(sub(a, sc(m2, b))): H = m2
            else: L = m1
        return close(tofr(R), nrm(sub(a, sc((L + H) / 2, b))) ** 2, 1e-6)
    if t == 'd_lam':
        a, b = p['a'], p['b']; lo, hi = -500.0, 500.0; g = lambda l: dot(addv(a, sc(l, b)), sub(a, b))
        for _ in range(200):
            m = (lo + hi) / 2
            if g(lo) * g(m) <= 0: hi = m
            else: lo = m
        return close(R, (lo + hi) / 2)
    if t == 'd_bis':
        a, b = p['a'], p['b']; v = tuple(float(tofr(x)) for x in R.strip('()').split(', '))
        ang = lambda x, y: math.acos(max(-1, min(1, dot(x, y) / (nrm(x) * nrm(y))))); return abs(ang(v, a) - ang(v, b)) < 1e-9 and abs(ang(v, a) + ang(v, b) - ang(a, b)) < 1e-9
    if t == 'x_tri': return close(tofr(R), heron(*p['V']) ** 2, 1e-6)
    if t == 'x_par':
        a, b = p['a'], p['b']; m1, n1, m2, n2 = p['s']; u, v = addv(sc(m1, a), sc(n1, b)), addv(sc(m2, a), sc(n2, b)); return close(R, (2 * heron((0, 0, 0), u, v)) ** 2, 1e-6)
    if t == 'x_diag':
        d1, d2 = p['d1'], p['d2']; u, v = sc(0.5, addv(d1, d2)), sc(0.5, sub(d1, d2)); return close(tofr(R), (2 * heron((0, 0, 0), u, v)) ** 2, 1e-6)
    if t in ('x_solve', 'x_ac'):
        if t == 'x_solve':
            a, b = p['a'], p['b']; P_, Q_ = p['pq']; u = addv(sc(P_, a), sc(Q_, b))
            rows = [(0, u[2], -u[1]), (-u[2], 0, u[0]), (u[1], -u[0], 0), p['w']]; rhs = [0, 0, 0, p['K']]   # c × u = 0 and c·w = K
        else:
            a = p['a']; rows = [(0, -a[2], a[1]), (a[2], 0, -a[0]), (-a[1], a[0], 0), a]; rhs = list(p['b']) + [p['K']]
        c = gsolve(rows, rhs); return close(R, dot(c, p['z']))
    if t == 'x_box': return close(int(R), abs(det3([p['a'], p['b'], p['c']])))
    if t == 'x_bac': a, b, c = p['a'], p['b'], p['c']; return close(R, sum(cross(a, cross(b, c))))
    if t == 'x_lag':
        th = math.acos(p['d'] / (p['P'] * p['Q'])); return close(R, (p['P'] * p['Q'] * math.sin(th)) ** 2)
    raise KeyError(t)
