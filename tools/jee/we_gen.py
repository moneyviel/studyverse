"""Practice generators — Physics Unit 4: Work, Energy and Power. check() re-solves each item independently: work by
numerical integration, power from a time-stepped velocity, energy by stepping the motion or writing energy afresh,
collisions from momentum + restitution."""
import math
from common import mcq, nf
G = 10.0
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-9)
def half(x): need(abs(x % 1 - 0.5) > 0.02)
def integ(f, a, b, n=4000):
    h = (b - a) / n; return sum(f(a + (i + 0.5) * h) for i in range(n)) * h
def vec(v): return ' '.join(f'{"+ " if i and c >= 0 else ("− " if c < 0 else "")}{abs(c)}{u}' for i, (c, u) in enumerate(zip(v, ['î', 'ĵ', 'k̂'])))
def poly(c):   # c = [c2, c1, c0] → "3x^{2} + 2x − 5"
    out = []
    for p, k in zip((2, 1, 0), c):
        if k == 0: continue
        s = ('' if abs(k) == 1 and p else str(abs(k))) + {2: 'x^{2}', 1: 'x', 0: ''}[p]
        out.append(('− ' if k < 0 else ('+ ' if out else '')) + s)
    return ' '.join(out)

def g_work(rng):
    t = rng.choice(['w_dot', 'w_var', 'w_fric', 'w_grav', 'w_zero', 'w_spring'])
    if t == 'w_dot':
        F1 = [rng.randint(-4, 6) for _ in range(3)]; F2 = [rng.randint(-4, 6) for _ in range(3)]; d = rng.choice([(3, 4), (3, -4), (4, 3), (-4, 3), (6, 8), (5, 12)]); L = rng.choice([5, 10, 15, 20, 25, 50])
        n = math.hypot(*d); s = [L * x / n for x in d] + [0]; W = sum((a + b) * c for a, b, c in zip(F1, F2, s)); need(abs(W - round(W)) < 1e-9 and W > 0)
        return dict(q=f'Two forces ({vec(F1)}) N and ({vec(F2)}) N act together on a block that moves {L} m along ({vec(list(d))}). The work done is ____ J.', o=None, a=round(W),
                    sol=['Add the forces, write the displacement as length × unit vector, then take the dot product.', f'd⃗ = {L} × \\f{{{vec(list(d))}}}{{{nf(n)}}}; W = F⃗ · d⃗ = {nf(W)} J.'], p=dict(t=t, F1=F1, F2=F2, d=d, L=L))
    if t == 'w_var':
        c = [rng.randint(1, 4), rng.randint(-3, 4), rng.randint(-6, 6)]; a = rng.randint(0, 2); b = a + rng.randint(1, 3); W = c[0] * (b ** 3 - a ** 3) / 3 + c[1] * (b * b - a * a) / 2 + c[2] * (b - a)
        need(abs(W - round(W)) < 1e-9 and W > 0)
        return dict(q=f'A force F = ({poly(c)}) N moves a body from x = {a} m to x = {b} m. The work done is ____ J.', o=None, a=round(W), sol=['W = ∫F dx — integrate term by term.', f'= [{nf(c[0] / 3)}x^{{3}} + {nf(c[1] / 2)}x^{{2}} + {c[2]}x] from {a} to {b} = {nf(W)} J.'], p=dict(t=t, c=c, a=a, b=b))
    if t == 'w_fric':
        m, mu, d = rng.choice([2, 5, 10, 20, 50, 100]), rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5]), rng.choice([2, 5, 8, 10, 20]); th = rng.choice([0, 0, 30, 60]); W = mu * m * G * math.cos(math.radians(th)) * d
        need(abs(W - round(W)) < 1e-6)
        where = 'a horizontal floor' if th == 0 else f'a {th}° incline (moving up the slope)'
        return dict(q=f'A {m} kg block slides {d} m on {where} with μ = {mu}. The work done against friction is ____ J (g = 10).', o=None, a=round(W),
                    sol=['Friction = μN, with N = mg cosθ.', f'W = {mu} × {m} × 10 × {nf(math.cos(math.radians(th)), 3)} × {d} = {nf(W)} J.'], p=dict(t=t, m=m, mu=mu, d=d, th=th))
    if t == 'w_grav':
        m, h, th = rng.choice([2, 5, 10, 20, 40, 50]), rng.choice([2, 5, 10, 15, 20]), rng.choice([30, 37, 45, 53, 60]); W = m * G * h
        right = f'{nf(W)} J'; o, a = mcq(rng, right, [f'{nf(W * x)} J' for x in (2, 0.5, 1 / math.sin(math.radians(th)), math.sin(math.radians(th)))])
        return dict(q=f'A {m} kg box is pushed slowly up a smooth {th}° ramp until it is {h} m higher. The work done against gravity is :', o=o, a=a, sol=['Gravity is conservative: work = mgh, whatever the path.', f'= {m} × 10 × {h} = {nf(W)} J.'], p=dict(t=t, m=m, h=h))
    if t == 'w_zero':
        F = [rng.randint(1, 5), None, rng.randint(-3, 3)]; d = [rng.randint(-3, 3), rng.choice([-3, -2, -1, 1, 2, 3]), rng.randint(-3, 3)]; b = -(F[0] * d[0] + F[2] * d[2]) / d[1]
        need(abs(b * 2 - round(b * 2)) < 1e-9 and abs(b) <= 8)
        right = nf(b); o, a = mcq(rng, right, [nf(x) for x in (-b, b + 1, b - 1, 2 * b + 1, b + 0.5)])
        return dict(q=f'A force F⃗ = {F[0]}î + bĵ {"+" if F[2] >= 0 else "−"} {abs(F[2])}k̂ moves a particle through ({vec(d)}). If the work done is zero, b =', o=o, a=a,
                    sol=['Zero work → F⃗ · d⃗ = 0.', f'{F[0]}({d[0]}) + b({d[1]}) + {F[2]}({d[2]}) = 0 → b = {nf(b)}.'], p=dict(t=t, F=F, d=d))
    k, x1, x2 = rng.choice([100, 200, 400, 500, 800, 1000]), rng.choice([0, 1, 2, 3]), rng.choice([2, 4, 5, 6, 8, 10]); need(x2 > x1); W = 0.5 * k * ((x2 / 100) ** 2 - (x1 / 100) ** 2)
    return dict(q=f'A spring (k = {k} N/m) is stretched from {x1} cm to {x2} cm. The work done is ____ × 10^{{−2}} J (nearest integer).', o=None, a=round(W * 100),
                sol=['W = ½k(x_{2}^{2} − x_{1}^{2}).', f'= ½ × {k} × ({nf(x2 / 100)}^{{2}} − {nf(x1 / 100)}^{{2}}) = {nf(W, 4)} J.'], p=dict(t=t, k=k, x1=x1, x2=x2)) if abs(W * 100 % 1 - 0.5) > 0.02 else g_work(rng)

def g_power(rng):
    t = rng.choice(['p_tforce', 'p_tval', 'p_const', 'p_lift', 'p_avg'])
    if t in ('p_tforce', 'p_tval'):
        m = rng.choice([1, 2, 3, 4]); a, b = rng.randint(1, 6), rng.randint(1, 6); ex = rng.choice([(1, 2), (1, 1), (0, 1), (2, 1)])   # F = a t^{p} î + b t^{q} ĵ
        p, q = ex; cx = a * a / (m * (p + 1)); cy = b * b / (m * (q + 1))   # P = cx t^{2p+1} + cy t^{2q+1}
        tp = lambda e: '' if e == 0 else ('t' if e == 1 else f't^{{{e}}}')
        Ftxt = f'({a}{tp(p)}î + {b}{tp(q)}ĵ) N'
        if t == 'p_tval':
            T = rng.choice([1, 2, 3]); Pv = cx * T ** (2 * p + 1) + cy * T ** (2 * q + 1); need(abs(Pv - round(Pv)) < 1e-9)
            return dict(q=f'A {m} kg body starts from rest under F⃗ = {Ftxt}. The power delivered at t = {T} s is ____ W.', o=None, a=round(Pv),
                        sol=['Integrate a = F/m to get v⃗ (from rest), then P = F⃗ · v⃗.', f'P = {nf(Pv)} W.'], p=dict(t=t, m=m, a=a, b=b, ex=ex, T=T))
        def term(c, e):
            return f'{nf(c)}{tp(e)}'
        need(2 * p + 1 != 2 * q + 1); need(abs(cx * 6 - round(cx * 6)) < 1e-9 and abs(cy * 6 - round(cy * 6)) < 1e-9)
        right = f'({term(cx, 2 * p + 1)} + {term(cy, 2 * q + 1)}) W'
        wr = [f'({term(cx * k1, 2 * p + 1)} + {term(cy * k2, 2 * q + 1)}) W' for k1, k2 in ((p + 1, q + 1), (m, m), (2, 1), (1, 2))] + [f'({term(cx, 2 * p + 2)} + {term(cy, 2 * q + 2)}) W']
        o, ans = mcq(rng, right, wr)
        return dict(q=f'A {m} kg body starts from rest under F⃗ = {Ftxt}. The power developed by the force at time t is :', o=o, a=ans,
                    sol=['From rest: v⃗ = ∫\\f{F⃗}{m}dt.', f'P = F⃗ · v⃗ = {right[:-2]}.'], p=dict(t=t, m=m, a=a, b=b, ex=ex))
    if t == 'p_const':
        n = rng.choice(['x', 'v']); right = {'x': 't^{3/2}', 'v': 't^{1/2}'}[n]; o, a = mcq(rng, right, ['t', 't^{2}', 't^{2/3}', 't^{3/2}', 't^{1/2}', 't^{1/3}'])
        return dict(q=f'A body starts from rest and is driven by a constant-power engine. Its {"displacement" if n == "x" else "speed"} after time t is proportional to :', o=o, a=a,
                    sol=['Pt = ½mv^{2} → v ∝ t^{1/2}.', 'x = ∫v dt ∝ t^{3/2}.'], p=dict(t=t, n=n))
    if t == 'p_lift':
        m, h, T = rng.choice([50, 100, 200, 500, 1000]), rng.choice([5, 10, 15, 20, 30]), rng.choice([5, 10, 20, 25, 50]); Pw = m * G * h / T
        need(abs(Pw - round(Pw)) < 1e-9)
        return dict(q=f'A motor lifts {m} kg through {h} m at steady speed in {T} s. Its power output is ____ W (g = 10).', o=None, a=round(Pw), sol=['P = \\f{mgh}{t} (steady speed: no KE change).', f'= \\f{{{m} × 10 × {h}}}{{{T}}} = {nf(Pw)} W.'], p=dict(t=t, m=m, h=h, T=T))
    m, F, T = rng.choice([1, 2, 4, 5, 10]), rng.choice([2, 4, 5, 6, 10, 20]), rng.choice([2, 3, 4, 5, 6])   # constant force from rest: avg P : instantaneous P = 1 : 2
    Pavg = F * F * T / (2 * m); need(abs(Pavg - round(Pavg)) < 1e-9)
    return dict(q=f'A constant {F} N force acts on a {m} kg body initially at rest. The average power over the first {T} s is ____ W.', o=None, a=round(Pavg),
                sol=['W = ½mv^{2} with v = \\f{F}{m}t → P_{avg} = \\f{W}{t} = \\f{F^{2}t}{2m}.', f'= \\f{{{F}^{{2}} × {T}}}{{2 × {m}}} = {nf(Pavg)} W.'], p=dict(t='p_avg', m=m, F=F, T=T))

def g_ke(rng):
    t = rng.choice(['k_pk', 'k_bullet', 'k_top', 'k_xt', 'k_ball', 'k_samep', 'k_vx'])
    if t == 'k_pk':
        n = rng.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 1.44, 1.21, 2.25]); r = math.sqrt(n); inc = 100 * (r - 1)
        o, a = mcq(rng, f'{nf(inc)}%', [f'{nf(x)}%' for x in (100 * (n - 1), 100 * r, inc / 10, 100 * (r - 1) / 2 if r > 1 else 1)])
        return dict(q=f'The kinetic energy of a body becomes {nf(n)} times its original value. The percentage increase in its momentum is :', o=o, a=a, sol=['p = √{2mK} → p scales as √{K}.', f'√{{{nf(n)}}} = {nf(r)} → increase {nf(inc)}%.'], p=dict(t=t, n=n))
    if t == 'k_bullet':
        u, v = rng.choice([100, 200, 250, 300, 400, 500]), None; v = u * rng.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]); L = 100 * (1 - (v / u) ** 2); half(L)
        return dict(q=f'A bullet enters a plank at {u} m/s and leaves at {nf(v)} m/s. The percentage loss of its kinetic energy is ____ (nearest integer).', o=None, a=round(L), sol=['Loss fraction = 1 − (\\f{v}{u})^{2}.', f'= 1 − ({nf(v / u)})^{{2}} → {nf(L)}%.'], p=dict(t=t, u=u, v=v))
    if t == 'k_top':
        m, u, th = rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([10, 20, 30, 40]), rng.choice([30, 37, 45, 53, 60]); s = {37: 0.6, 53: 0.8}.get(th, math.sin(math.radians(th)))
        d = 0.5 * m * (u * s) ** 2; need(abs(d * 10 - round(d * 10)) < 1e-6); half(d)
        return dict(q=f'A {int(m * 1000)} g ball is projected at {u} m/s, {th}° above the horizontal{" (sin 37° = 0.6)" if th in (37, 53) else ""}. The decrease in its kinetic energy from launch to the highest point is ____ J (nearest integer).', o=None, a=round(d),
                    sol=['At the top only u cosθ remains → loss = ½m(u sinθ)^{2}.', f'= ½ × {m} × ({nf(u * s)})^{{2}} = {nf(d)} J.'], p=dict(t=t, m=m, u=u, s=s))
    if t == 'k_xt':
        m, al, be = rng.choice([1, 2, 3, 4, 5]), rng.choice([0.5, 1, 1.5, 2, 3]), rng.choice([0, 1, 2, 3]); t1 = rng.choice([0, 1, 2, 3]); t2 = t1 + rng.choice([1, 2])
        v = lambda s: 2 * al * s + be; W = 0.5 * m * (v(t2) ** 2 - v(t1) ** 2); half(W)
        return dict(q=f'A {m} kg body moves along x with x(t) = {nf(al)}t^{{2}} + {be}t + 1 (m). The work done on it from t = {t1} s to t = {t2} s is ____ J (nearest integer).', o=None, a=round(W),
                    sol=['v = \\f{dx}{dt}; work–energy theorem W = ΔK.', f'v: {nf(v(t1))} → {nf(v(t2))} m/s → W = {nf(W)} J.'], p=dict(t=t, m=m, al=al, be=be, t1=t1, t2=t2))
    if t == 'k_ball':
        f = rng.choice([0.25, 0.4, 0.5, 0.6, 0.64, 0.75, 0.8, 0.81, 0.9]); L = 100 * (1 - f); half(L)
        return dict(q=f'A ball dropped from height h rebounds to {nf(f)}h. The percentage of its energy lost in the bounce is ____ (nearest integer).', o=None, a=round(L), sol=['Energy ∝ height reached.', f'Loss = 1 − {nf(f)} = {nf(L)}%.'], p=dict(t=t, f=f))
    if t == 'k_samep':
        ms = rng.sample([1, 2, 3, 4, 5, 6, 8], 4); mx = rng.choice(['maximum', 'minimum']); labels = 'ABCD'
        best = (min if mx == 'maximum' else max)(range(4), key=lambda i: ms[i]); o = list(labels); a = best
        return dict(q=f'Particles A, B, C, D of masses {", ".join(f"{x}m" for x in ms)} have the same momentum. Which has the {mx} kinetic energy?', o=o, a=a,
                    sol=['K = \\f{p^{2}}{2m}: at equal p, lighter → more K.', f'{labels[best]}.'], p=dict(t=t, ms=ms, mx=mx))
    m, k, X = rng.choice([0.5, 1, 2, 4]), rng.choice([1, 2, 3]), rng.choice([1, 2, 3, 4, 5]); n = rng.choice([1, 2]); W = 0.5 * m * (k * X ** n) ** 2; half(W)
    return dict(q=f'A {m} kg body starts at x = 0 and its velocity varies as v = {k}x{"^{2}" if n == 2 else ""} m/s. The work done by the net force up to x = {X} m is ____ J (nearest integer).', o=None, a=round(W),
                sol=['Work–energy theorem: W = ½mv^{2} − 0.', f'v = {nf(k * X ** n)} m/s → W = {nf(W)} J.'], p=dict(t=t, m=m, k=k, X=X, n=n))

def g_cons(rng):
    t = rng.choice(['c_kpe', 'c_cut', 'c_hang', 'c_loop', 'c_drop', 'c_spring', 'c_elong'])
    if t == 'c_kpe':
        n, S = rng.choice([1, 2, 3, 4, 5, 7, 9]), rng.choice([20, 40, 60, 80, 100]); h = S / (n + 1); v = math.sqrt(2 * G * (S - h)); half(v * 10)
        return dict(q=f'A stone is dropped from {S} m. At the height where its KE is {n} times its PE (ground = 0), its speed is ____ × 10^{{−1}} m/s (nearest integer; g = 10).', o=None, a=round(v * 10),
                    sol=[f'K = {n}U and K + U = mgS → h = \\f{{S}}{{{n + 1}}} = {nf(h)} m.', f'v = √{{2g(S − h)}} ≈ {nf(v, 4)} m/s.'], p=dict(t=t, n=n, S=S))
    if t == 'c_cut':
        k, r = rng.choice([10, 12, 15, 20, 24, 30, 60]), rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (1, 5), (2, 5)]); sm = rng.choice([True, False]); part = r[0] if sm else r[1]; kk = k * (r[0] + r[1]) / part
        need(abs(kk - round(kk)) < 1e-9)
        return dict(q=f'A spring of constant {k} N/m is cut into two pieces with lengths in the ratio {r[0]} : {r[1]}. The constant of the {"smaller" if sm else "longer"} piece is ____ N/m.', o=None, a=round(kk),
                    sol=['k × length = constant.', f'k\' = {k} × \\f{{{r[0] + r[1]}}}{{{part}}} = {nf(kk)} N/m.'], p=dict(t=t, k=k, r=r, sm=sm))
    if t == 'c_hang':
        mA, mB = rng.choice([(100, 200), (100, 300), (200, 100), (50, 100), (200, 300)]); kr = rng.choice([(1, 2), (2, 1), (3, 4), (4, 3), (1, 1), (2, 3)])   # kA : kB
        ratio = (mB / mA) ** 2 * kr[0] / kr[1]; need(abs(ratio * 4 - round(ratio * 4)) < 1e-9)
        right = f'{nf(ratio)}E'; o, a = mcq(rng, right, [f'{nf(x)}E' for x in ((mB / mA) * kr[0] / kr[1], (mB / mA) ** 2 * kr[1] / kr[0], (mB / mA) ** 2, ratio * 2, ratio / 2)])
        return dict(q=f'Masses {mA} g and {mB} g hang in equilibrium from springs A and B with k_{{A}} : k_{{B}} = {kr[0]} : {kr[1]}. If spring A stores energy E, spring B stores :', o=o, a=a,
                    sol=['Stretch = \\f{mg}{k} → U = \\f{(mg)^{2}}{2k}.', f'\\f{{U_{{B}}}}{{U_{{A}}}} = ({nf(mB / mA)})^{{2}} × \\f{{{kr[0]}}}{{{kr[1]}}} = {nf(ratio)}.'], p=dict(t=t, mA=mA, mB=mB, kr=kr))
    if t == 'c_loop':
        n = rng.choice([0, 1, 2, 3, 4, 5]); h = 2 + (n + 1) / 2   # N_top = n mg → v^2 = (n+1) gR
        return dict(q=f'A body slides down a smooth track into a vertical loop of radius R. At the top of the loop it presses on the track with {"zero force" if n == 0 else f"{n} times its weight"}. It was released from h = αR; α × 10 = ____.', o=None, a=round(h * 10),
                    sol=[f'Top: N + mg = \\f{{mv^{{2}}}}{{R}} → v^{{2}} = {n + 1}gR.', f'mgh = 2mgR + ½mv^{{2}} → h = {nf(h)}R.'], p=dict(t=t, n=n))
    if t == 'c_drop':
        R, ang = rng.choice([1, 2, 2.5, 4, 5, 10]), rng.choice([0, 30, 45, 60, 90, 120]); drop = R + R * math.cos(math.radians(ang)); v = math.sqrt(2 * G * drop); half(v * 10)
        return dict(q=f'A bead starts from rest on a smooth vertical ring of radius {R} m at a point whose radius makes {ang}° with the upward vertical. Its speed at the lowest point is ____ × 10^{{−1}} m/s (nearest integer; g = 10).', o=None, a=round(v * 10),
                    sol=['Drop = R + R cosθ (θ from the upward vertical).', f'= {nf(drop)} m → v = √{{2g × {nf(drop)}}} ≈ {nf(v, 4)} m/s.'], p=dict(t=t, R=R, ang=ang))
    if t == 'c_spring':
        m, k, A = rng.choice([0.5, 1, 2, 4]), rng.choice([50, 100, 200, 400, 800]), rng.choice([0.1, 0.2, 0.25, 0.5]); x = A * rng.choice([0, 0.5, 0.6, 0.8]); v = math.sqrt(k / m * (A * A - x * x)); half(v * 10)
        return dict(q=f'A {m} kg block on a smooth table is attached to a spring (k = {k} N/m), pushed {int(A * 100)} cm from natural length and released. Its speed when it is {nf(x * 100)} cm from natural length is ____ × 10^{{−1}} m/s (nearest integer).', o=None, a=round(v * 10),
                    sol=['½kA^{2} = ½kx^{2} + ½mv^{2}.', f'v = √{{\\f{{k}}{{m}}(A^{{2}} − x^{{2}})}} ≈ {nf(v, 4)} m/s.'], p=dict(t=t, m=m, k=k, A=A, x=x))
    T1, T2 = rng.sample([2, 3, 4, 5, 6, 7, 8, 10], 2); a, b = rng.choice([(5, 2), (2, 1), (3, 2), (4, 3), (3, 1), (5, 3)]); T = a * T1 - b * T2; need(T > 0)
    return dict(q=f'A spring stretches x_{{1}} under {T1} N and x_{{2}} under {T2} N. For a stretch of ({a}x_{{1}} − {b}x_{{2}}) the tension is ____ N.', o=None, a=T,
                sol=['x = \\f{T}{k} (Hooke).', f'{a}x_{{1}} − {b}x_{{2}} = \\f{{{a} × {T1} − {b} × {T2}}}{{k}} → T = {T} N.'], p=dict(t='c_elong', T1=T1, T2=T2, a=a, b=b))

def g_coll(rng):
    t = rng.choice(['x_inel', 'x_elas', 'x_gun', 'x_rest', 'x_heat', 'x_pend'])
    if t == 'x_inel':
        m1, m2, u1, u2 = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 6]), rng.choice([2, 4, 5, 6, 8, 10]), rng.choice([0, 0, -2, -4, 2]); v = (m1 * u1 + m2 * u2) / (m1 + m2)
        L = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2 - 0.5 * (m1 + m2) * v ** 2; half(L)
        return dict(q=f'A {m1} kg ball moving at {u1} m/s collides with a {m2} kg ball moving at {u2} m/s (same line) and they stick. The kinetic energy lost is ____ J (nearest integer).', o=None, a=round(L),
                    sol=['Momentum: v = \\f{m_{1}u_{1} + m_{2}u_{2}}{m_{1} + m_{2}}.', f'v = {nf(v)} m/s → loss = {nf(L)} J.'], p=dict(t=t, m1=m1, m2=m2, u1=u1, u2=u2))
    if t == 'x_elas':
        m1, m2, u = rng.choice([1, 2, 3, 4, 6]), rng.choice([1, 2, 3, 4, 6]), rng.choice([3, 6, 9, 12]); need(m1 != m2); who = rng.choice([1, 2])
        v1 = (m1 - m2) / (m1 + m2) * u; v2 = 2 * m1 / (m1 + m2) * u; val = v1 if who == 1 else v2
        right = f'{nf(val, 3)} m/s'; o, a = mcq(rng, right, [f'{nf(x, 3)} m/s' for x in (-val, u, (v2 if who == 1 else v1), val / 2, val * 2) if abs(x) > 1e-9])
        return dict(q=f'A {m1} kg ball moving at {u} m/s hits a {m2} kg ball at rest head-on, perfectly elastically. The velocity of the {"first" if who == 1 else "second"} ball after impact is (direction of the original motion is +) :', o=o, a=a,
                    sol=['v_{1} = \\f{m_{1} − m_{2}}{m_{1} + m_{2}}u, v_{2} = \\f{2m_{1}}{m_{1} + m_{2}}u.', f'→ {nf(val, 3)} m/s.'], p=dict(t=t, m1=m1, m2=m2, u=u, who=who))
    if t == 'x_gun':
        M, m = rng.choice([2, 4, 5, 10, 20, 50]), rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]); r = m / M
        right = nf(r, 3); o, a = mcq(rng, right, [nf(x, 3) for x in (M / m, m / (m + M), M / (m + M), math.sqrt(r))])
        return dict(q=f'A {M} kg gun fires a {int(m * 1000)} g bullet. Right after firing, (KE of gun) : (KE of bullet) =', o=o, a=a, sol=['Equal and opposite momenta; K = \\f{p^{2}}{2m}.', f'\\f{{K_{{gun}}}}{{K_{{bullet}}}} = \\f{{m}}{{M}} = {nf(r, 3)}.'], p=dict(t=t, M=M, m=m))
    if t == 'x_rest':
        e, h = rng.choice([0.2, 0.4, 0.5, 0.6, 0.8, 0.9]), rng.choice([1, 2, 5, 10, 20]); h1 = e * e * h; need(abs(h1 * 100 - round(h1 * 100)) < 1e-6); half(h1 * 100)
        return dict(q=f'A ball dropped from {h} m hits the floor (coefficient of restitution {e}). It rises to ____ cm (nearest integer).', o=None, a=round(h1 * 100), sol=['Rebound speed = e × impact speed → h\' = e^{2}h.', f'= {e}^{{2}} × {h} = {nf(h1)} m.'], p=dict(t=t, e=e, h=h))
    if t == 'x_heat':
        m1, m2, u1, u2 = rng.choice([5, 10, 15, 20]), rng.choice([5, 10, 25, 30]), rng.choice([5, 10, 20]), rng.choice([10, 20, 30]); c = rng.choice([100, 200, 400, 500])
        v = (m1 * u1 - m2 * u2) / (m1 + m2); L = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2 - 0.5 * (m1 + m2) * v ** 2; dT = L / ((m1 + m2) * c); half(dT * 100)
        return dict(q=f'Balls of {m1} kg and {m2} kg moving towards each other at {u1} m/s and {u2} m/s stick together. If all the lost KE heats them (specific heat {c} J/kg °C), the temperature rise is ____ × 10^{{−2}} °C (nearest integer).', o=None, a=round(dT * 100),
                    sol=['Common velocity from momentum; heat = KE lost.', f'v = {nf(v)} m/s, loss = {nf(L)} J → ΔT = \\f{{{nf(L)}}}{{{m1 + m2} × {c}}} ≈ {nf(dT, 3)} °C.'], p=dict(t=t, m1=m1, m2=m2, u1=u1, u2=u2, c=c))
    L, ang, r = rng.choice([0.5, 1, 1.6, 2, 2.5]), rng.choice([60, 90, 120, 180]), rng.choice([1, 2, 3, 0.5])   # pendulum mass m hits block m/r? use mass ratio r = m2/m1
    v0 = math.sqrt(2 * G * L * (1 - math.cos(math.radians(ang)))) if ang <= 90 else None; need(v0 is not None and r != 1)
    v1 = (1 - r) / (1 + r) * v0; half(abs(v1) * 100)
    return dict(q=f'A pendulum bob (length {L} m) is released with the string at {ang}° to the vertical and hits, at the lowest point, a block of {nf(r)} times its mass at rest, elastically. The bob\'s speed just after is ____ × 10^{{−2}} m/s (nearest integer; g = 10).', o=None, a=round(abs(v1) * 100),
                sol=['v_{0} = √{2gL(1 − cosθ)}.', f'Elastic: v_{{1}} = \\f{{1 − {nf(r)}}}{{1 + {nf(r)}}}v_{{0}} → |v_{{1}}| ≈ {nf(abs(v1), 4)} m/s.'], p=dict(t='x_pend', L=L, ang=ang, r=r))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(work=g_work, power=g_power, ke=g_ke, cons=g_cons, coll=g_coll).items()}
def finish(it): return it
def vstep(F, m, T, dt=1e-3):
    v = [0.0, 0.0]; t = 0.0
    while t < T - 1e-12:
        f = F(t + dt / 2); v = [vi + fi / m * dt for vi, fi in zip(v, f)]; t += dt
    return v
def coll(m1, u1, m2, u2, e):
    v1 = (m1 * u1 + m2 * u2 - m2 * e * (u1 - u2)) / (m1 + m2); return v1, v1 + e * (u1 - u2)
def parse_poly(s):   # "(2t^{3} + 3t^{5}) W" → {3: 2, 5: 3}
    out = {}
    for c, e in re.findall(r'([\d.]+)t(?:\^\{(\d+)\})?', s): out[int(e or 1)] = float(c)
    return out
import re
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'w_dot':
        n = math.hypot(*p['d']); s = [p['L'] * x / n for x in p['d']] + [0]; return Rv == round(sum((a + b) * c for a, b, c in zip(p['F1'], p['F2'], s)))
    if t == 'w_var': c = p['c']; return Rv == round(integ(lambda x: c[0] * x * x + c[1] * x + c[2], p['a'], p['b']))
    if t == 'w_fric': return Rv == round(p['mu'] * p['m'] * G * math.cos(math.radians(p['th'])) * p['d'])
    if t == 'w_grav': return close(num(Rv), p['m'] * G * p['h'], 1e-3)
    if t == 'w_zero': F, d = p['F'], p['d']; b = num(Rv); return abs(F[0] * d[0] + b * d[1] + F[2] * d[2]) < 1e-6
    if t == 'w_spring': return Rv == round(integ(lambda x: p['k'] * x, p['x1'] / 100, p['x2'] / 100) * 100)
    if t in ('p_tforce', 'p_tval'):
        q_, r_ = p['ex']; F = lambda s: (p['a'] * s ** q_, p['b'] * s ** r_)
        if t == 'p_tval':
            v = vstep(F, p['m'], p['T']); f = F(p['T']); return Rv == round(f[0] * v[0] + f[1] * v[1])
        poly_ = parse_poly(Rv)
        for T in (0.7, 1.3):
            v = vstep(F, p['m'], T); f = F(T); P_ = f[0] * v[0] + f[1] * v[1]
            if not close(sum(c * T ** e for e, c in poly_.items()), P_, 2e-3): return False
        return True
    if t == 'p_const':
        dt = 1e-3; xs = {}
        for T in (1.0, 4.0):   # P = 1, m = 2: v = √t ; x = ∫v
            x = sum(math.sqrt((k + 0.5) * dt) * dt for k in range(int(T / dt))); xs[T] = x if p['n'] == 'x' else math.sqrt(T)
        e = math.log(xs[4.0] / xs[1.0]) / math.log(4); want = {'t': 1, 't^{2}': 2, 't^{2/3}': 2 / 3, 't^{3/2}': 1.5, 't^{1/2}': 0.5, 't^{1/3}': 1 / 3}[Rv]; return abs(e - want) < 0.01
    if t == 'p_lift': return Rv == round(p['m'] * G * p['h'] / p['T'])
    if t == 'p_avg':
        v = p['F'] / p['m'] * p['T']; return Rv == round(0.5 * p['m'] * v * v / p['T'])
    if t == 'k_pk': n = p['n']; return close(num(Rv.rstrip('%')), 100 * (math.sqrt(2 * n) / math.sqrt(2) - 1), 1e-3)
    if t == 'k_bullet': return Rv == round(100 * (p['u'] ** 2 - p['v'] ** 2) / p['u'] ** 2)
    if t == 'k_top': return Rv == round(0.5 * p['m'] * p['u'] ** 2 - 0.5 * p['m'] * p['u'] ** 2 * (1 - p['s'] ** 2))
    if t == 'k_xt':
        x = lambda s: p['al'] * s * s + p['be'] * s + 1; v = lambda s: (x(s + 1e-5) - x(s - 1e-5)) / 2e-5; return Rv == round(0.5 * p['m'] * (v(p['t2']) ** 2 - v(p['t1']) ** 2))
    if t == 'k_ball': return Rv == round(100 * (1 - p['f']))
    if t == 'k_samep':
        Ks = [1 / (2 * m) for m in p['ms']]; i = 'ABCD'.index(Rv); return Ks[i] == (max(Ks) if p['mx'] == 'maximum' else min(Ks))
    if t == 'k_vx':
        v = lambda x: p['k'] * x ** p['n']; return Rv == round(integ(lambda x: p['m'] * v(x) * (v(x + 1e-6) - v(x - 1e-6)) / 2e-6, 0, p['X']))
    if t == 'c_kpe':
        h = p['S']; v = 0.0; dt = 1e-4   # fall until K = n U
        while 0.5 * v * v < p['n'] * G * h: h -= v * dt + 0.5 * G * dt * dt; v += G * dt
        return abs(Rv - v * 10) < 0.6
    if t == 'c_cut': r = p['r']; part = r[0] if p['sm'] else r[1]; return Rv == round(p['k'] / (part / (r[0] + r[1])))
    if t == 'c_hang':
        kA = 1.0 * p['kr'][0]; kB = 1.0 * p['kr'][1]; UA = (p['mA'] * G) ** 2 / (2 * kA); UB = (p['mB'] * G) ** 2 / (2 * kB); return close(num(Rv.rstrip('E')), UB / UA, 1e-3)
    if t == 'c_loop':
        v2 = (p['n'] + 1) * G * 1.0; h = (2 * G * 1.0 + 0.5 * v2) / G; return Rv == round(h * 10)
    if t == 'c_drop':
        y0 = p['R'] * math.cos(math.radians(p['ang'])); return Rv == round(math.sqrt(2 * G * (y0 + p['R'])) * 10)
    if t == 'c_spring':
        x = -p['A']; v = 0.0; dt = 1e-5   # step the oscillator until |x| first reaches the asked value
        target = p['x']
        while x < -target - 1e-12: a = -p['k'] / p['m'] * x; v += a * dt; x += v * dt
        return abs(Rv - v * 10) < 0.6
    if t == 'c_elong': k = 7.0; return Rv == round(k * (p['a'] * p['T1'] / k - p['b'] * p['T2'] / k))
    if t == 'x_inel':
        v1, v2 = coll(p['m1'], p['u1'], p['m2'], p['u2'], 0); return Rv == round(0.5 * p['m1'] * p['u1'] ** 2 + 0.5 * p['m2'] * p['u2'] ** 2 - 0.5 * p['m1'] * v1 ** 2 - 0.5 * p['m2'] * v2 ** 2)
    if t == 'x_elas':
        v1, v2 = coll(p['m1'], p['u'], p['m2'], 0, 1); return close(num(Rv), v1 if p['who'] == 1 else v2, 3e-3)
    if t == 'x_gun':
        v = 7.0; V = p['m'] * v / p['M']; return close(num(Rv), (0.5 * p['M'] * V * V) / (0.5 * p['m'] * v * v), 3e-3)
    if t == 'x_rest':
        u = math.sqrt(2 * G * p['h']); return Rv == round((p['e'] * u) ** 2 / (2 * G) * 100)
    if t == 'x_heat':
        v1, v2 = coll(p['m1'], p['u1'], p['m2'], -p['u2'], 0); L = 0.5 * p['m1'] * p['u1'] ** 2 + 0.5 * p['m2'] * p['u2'] ** 2 - 0.5 * (p['m1'] + p['m2']) * v1 ** 2; return Rv == round(L / ((p['m1'] + p['m2']) * p['c']) * 100)
    if t == 'x_pend':
        u = math.sqrt(2 * G * p['L'] * (1 - math.cos(math.radians(p['ang'])))); v1, _ = coll(1, u, p['r'], 0, 1); return Rv == round(abs(v1) * 100)
    raise KeyError(t)
