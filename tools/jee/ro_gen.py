"""Practice generators — Physics Unit 5: Rotational Motion. check() re-solves each item independently: moments of
inertia by summing point masses or integrating, rotations by stepping in time, rolling from the force + torque
equations solved as a linear system, spin-ups from angular-momentum conservation."""
import math
from common import mcq, nf
G = 10.0
def need(x):
    if not x: raise AssertionError('retry')
def half(x): need(abs(x % 1 - 0.5) > 0.02)
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-9)
K2 = {'ring': 1.0, 'disc': 0.5, 'solid cylinder': 0.5, 'hollow cylinder': 1.0, 'solid sphere': 0.4, 'hollow sphere': 2 / 3}
FR = {1.0: '1', 0.5: '\\f{1}{2}', 0.4: '\\f{2}{5}', 2 / 3: '\\f{2}{3}'}
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def vec(v): return ' '.join(f'{"+ " if i and c >= 0 else ("− " if c < 0 else "")}{abs(c)}{u}' for i, (c, u) in enumerate(zip(v, ['î', 'ĵ', 'k̂'])))

def g_com(rng):
    t = rng.choice(['m_pts', 'm_shift', 'm_hole', 'm_lrod'])
    if t == 'm_pts':
        n = 3; P = [(rng.randint(0, 6), rng.randint(0, 6)) for _ in range(n)]; ms = [rng.randint(1, 5) for _ in range(n)]; need(len(set(P)) == n)
        cx = sum(m * x for m, (x, _) in zip(ms, P)) / sum(ms); cy = sum(m * y for m, (_, y) in zip(ms, P)) / sum(ms); need(abs(cx * 10 - round(cx * 10)) < 1e-9 and abs(cy * 10 - round(cy * 10)) < 1e-9)
        right = f'({nf(cx)}, {nf(cy)})'; o, a = mcq(rng, right, [f'({nf(x)}, {nf(y)})' for x, y in ((cy, cx), (sum(x for x, _ in P) / n, sum(y for _, y in P) / n), (cx + 1, cy), (cx, cy - 1))])
        return dict(q=f'Masses {ms[0]} kg, {ms[1]} kg and {ms[2]} kg sit at ({P[0][0]}, {P[0][1]}), ({P[1][0]}, {P[1][1]}) and ({P[2][0]}, {P[2][1]}) m. The centre of mass is at (m) :', o=o, a=a,
                    sol=['x̄ = \\f{Σmx}{Σm}, ȳ = \\f{Σmy}{Σm}.', f'= {right}.'], p=dict(t=t, P=P, ms=ms))
    if t == 'm_shift':
        m1, m2, d = rng.randint(1, 9), rng.randint(1, 9), rng.choice([1, 2, 3, 4, 5, 6]); d2 = m1 * d / m2; need(m1 != m2); need(abs(d2 * 10 - round(d2 * 10)) < 1e-9)
        return dict(q=f'Particles of {m1} kg and {m2} kg lie on a line. The {m1} kg one moves {d} cm towards the centre of mass. How far (× 10^{{−1}} cm) must the {m2} kg one move towards it to keep the centre of mass fixed?', o=None, a=round(d2 * 10),
                    sol=['m_{1}d_{1} = m_{2}d_{2}.', f'd_{{2}} = \\f{{{m1} × {d}}}{{{m2}}} = {nf(d2)} cm.'], p=dict(t=t, m1=m1, m2=m2, d=d))
    if t == 'm_hole':
        R, r = rng.choice([(20, 5), (30, 10), (12, 4), (40, 10), (16, 4), (18, 6), (24, 6)]); c = R - r; x = r * r * c / (R * R - r * r); half(x * 100)
        return dict(q=f'A circular hole of radius {r} cm is cut from a uniform disc of radius {R} cm so that the hole touches the rim. The centre of mass shifts by ____ × 10^{{−2}} cm (nearest integer).', o=None, a=round(x * 100),
                    sol=[f'Hole centre at {c} cm; mass ∝ area.', f'x = \\f{{{r}^{{2}} × {c}}}{{{R}^{{2}} − {r}^{{2}}}} ≈ {nf(x, 4)} cm (away from the hole).'], p=dict(t=t, R=R, r=r))
    a, b = rng.randint(1, 5), rng.randint(1, 5); L = rng.choice([2, 5, 10, 20])   # bent rod: aL along y, bL along x
    cx, cy = b * b * L / (2 * (a + b)), a * a * L / (2 * (a + b)); need(abs(cx * 10 - round(cx * 10)) < 1e-9 and abs(cy * 10 - round(cy * 10)) < 1e-9)
    right = f'{nf(cx)}î + {nf(cy)}ĵ'; o, an = mcq(rng, right, [f'{nf(y)}î + {nf(x)}ĵ' for x, y in ((cx, cy), (cx * 2, cy), (b * L / 2, a * L / 2), (cx, cy * 2))])
    return dict(q=f'A uniform rod of length {(a + b) * L} cm is bent at a right angle: {a * L} cm along +y and {b * L} cm along +x, corner at the origin. The centre of mass (cm) is :', o=o, a=an,
                sol=['Treat each straight part as a point mass at its middle (mass ∝ length).', f'x̄ = \\f{{{b * L} × {nf(b * L / 2)}}}{{{(a + b) * L}}}, ȳ = \\f{{{a * L} × {nf(a * L / 2)}}}{{{(a + b) * L}}} → {right}.'], p=dict(t='m_lrod', a=a, b=b, L=L))

def g_moi(rng):
    t = rng.choice(['i_body', 'i_par', 'i_sq', 'i_scale', 'i_gyr', 'i_cut', 'i_dumb'])
    if t == 'i_body':
        body, axn, axis = rng.choice([('ring', 'tangent in its plane', 1.5), ('ring', 'tangent ⊥ its plane', 2.0), ('ring', 'diameter', 0.5), ('disc', 'diameter', 0.25), ('disc', 'tangent in its plane', 1.25), ('disc', 'tangent ⊥ its plane', 1.5),
                                 ('solid sphere', 'tangent', 1.4), ('hollow sphere', 'tangent', 5 / 3), ('rod (length 2R)', 'end, ⊥ rod', 4 / 3)])
        m, R = rng.choice([1, 2, 3, 4, 5]), rng.choice([0.1, 0.2, 0.5, 1, 2]); I = axis * m * R * R; need(abs(I * 1000 - round(I * 1000)) < 1e-6); half(I * 100)
        return dict(q=f'A {body} of mass {m} kg and radius {R} m: moment of inertia about a {axn} is ____ × 10^{{−2}} kg m^{{2}} (nearest integer).', o=None, a=round(I * 100),
                    sol=['Use the standard result plus the parallel/perpendicular axis theorems.', f'I = {nf(axis, 4)} MR^{{2}} = {nf(I, 4)} kg m^{{2}}.'], p=dict(t=t, body=body, axn=axn, axis=axis, m=m, R=R))
    if t == 'i_par':
        body = rng.choice(['solid sphere', 'disc', 'ring', 'hollow sphere']); m, R, d = rng.choice([1, 2, 5, 10]), rng.choice([0.1, 0.2, 0.3, 0.5]), rng.choice([0.2, 0.3, 0.4, 0.5, 1])
        k = {'solid sphere': 0.4, 'hollow sphere': 2 / 3, 'disc': 0.5, 'ring': 1.0}[body]; I = m * (k * R * R + d * d); half(I * 1000)
        return dict(q=f'A {body} (mass {m} kg, radius {R} m) turns about an axis parallel to its central {"⊥ axis" if body in ("disc", "ring") else "diameter"}, {d} m from its centre. I = ____ × 10^{{−3}} kg m^{{2}} (nearest integer).', o=None, a=round(I * 1000),
                    sol=['Parallel axis: I = I_{cm} + md^{2}.', f'= {m}({FR[k]} × {R}^{{2}} + {d}^{{2}}) ≈ {nf(I, 4)} kg m^{{2}}.'], p=dict(t=t, body=body, m=m, R=R, d=d))
    if t == 'i_sq':
        m, a = rng.choice([1, 2, 3, 0.5]), rng.choice([1, 2, 3, 4]); where = rng.choice(['vertex', 'centre', 'side']); pts = [(0, 0), (a, 0), (0, a), (a, a)]
        o_ = {'vertex': (0, 0), 'centre': (a / 2, a / 2), 'side': (a / 2, 0)}[where]; I = sum(m * ((x - o_[0]) ** 2 + (y - o_[1]) ** 2) for x, y in pts); half(I * 10)
        return dict(q=f'Four {m} kg particles sit at the corners of a square of side {a} m. I about an axis ⊥ to the square through {"one corner" if where == "vertex" else ("its centre" if where == "centre" else "the midpoint of one side")} is ____ × 10^{{−1}} kg m^{{2}}.', o=None, a=round(I * 10),
                    sol=['Add md^{2} for each particle.', f'I = {nf(I)} kg m^{{2}}.'], p=dict(t=t, m=m, a=a, where=where))
    if t == 'i_scale':
        kind = rng.choice(['disc_same_t', 'cyl', 'sphere']); s = rng.choice([2, 3, 4]); f = rng.choice([1, 2])
        ratio = {'disc_same_t': s ** 4, 'cyl': s ** 4 * f, 'sphere': s ** 5}[kind]
        txt = {'disc_same_t': f'Two discs cut from the same sheet have radii R and {s}R.', 'cyl': f'From a solid cylinder (radius R, length L) a co-axial cylinder of radius R/{s} and length L/{f} is carved.', 'sphere': f'Two solid spheres of the same material have radii R and {s}R.'}[kind]
        return dict(q=f'{txt} The ratio of their moments of inertia about their own symmetry axes (bigger : smaller) is ____.', o=None, a=ratio,
                    sol=['Same density: M ∝ volume, I ∝ M × R^{2}.', f'Ratio = {ratio}.'], p=dict(t=t, kind=kind, s=s, f=f))
    if t == 'i_gyr':
        R, d = rng.choice([2, 3, 4, 5, 6, 10]), rng.choice([3, 4, 5, 6, 8, 10, 15]); body = rng.choice(['solid sphere', 'disc (axis ⊥ plane)', 'ring (axis ⊥ plane)']); k = {'solid sphere': 0.4, 'disc (axis ⊥ plane)': 0.5, 'ring (axis ⊥ plane)': 1.0}[body]
        n = k * R * R + d * d; need(abs(n - round(n)) < 1e-9)
        return dict(q=f'A {body} of radius {R} cm rotates about a parallel axis {d} cm from its centre. Its radius of gyration is √{{n}} cm; n = ____.', o=None, a=round(n), sol=['k^{2} = k_{cm}^{2} + d^{2}.', f'= {FR[k]} × {R}^{{2}} + {d}^{{2}} = {nf(n)}.'], p=dict(t=t, R=R, d=d, k=k))
    if t == 'i_cut':
        q = rng.choice([2, 3, 4]); hole_c = 1 - 1 / q   # hole radius R/q touching the rim
        I = 0.5 - (1 / q ** 2) * (0.5 / q ** 2 + hole_c ** 2); fr_ = I
        right = nf(fr_, 4); o, a = mcq(rng, f'{right} MR^{{2}}', [f'{nf(x, 4)} MR^{{2}}' for x in (0.5 - 0.5 / q ** 4, 0.5 - hole_c ** 2 / q ** 2, 0.5 - 1 / q ** 2 * 0.5, fr_ + 0.05)])
        return dict(q=f'A disc (mass M before cutting, radius R) has a hole of radius R/{q} cut so that the hole touches the rim. I of the remaining part about the central axis ⊥ to the disc is :', o=o, a=a,
                    sol=[f'Removed mass \\f{{M}}{{{q * q}}}, centre {nf(hole_c, 3)}R away: I_{{hole}} = \\f{{M}}{{{q * q}}}(\\f{{R^{{2}}}}{{{2 * q * q}}} + ({nf(hole_c, 3)}R)^{{2}}).', f'I = \\f{{MR^{{2}}}}{{2}} − I_{{hole}} ≈ {right} MR^{{2}}.'], p=dict(t=t, q=q))
    m1, m2, d = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 6]), rng.choice([0.3, 0.5, 0.6, 1, 1.2]); I = m1 * m2 / (m1 + m2) * d * d; half(I * 1000)
    return dict(q=f'Point masses {m1} kg and {m2} kg are joined by a light {d} m rod. I about an axis through the centre of mass ⊥ to the rod is ____ × 10^{{−3}} kg m^{{2}} (nearest integer).', o=None, a=round(I * 1000),
                sol=['I = μd^{2} with μ = \\f{m_{1}m_{2}}{m_{1} + m_{2}}.', f'= {nf(m1 * m2 / (m1 + m2), 4)} × {d}^{{2}} ≈ {nf(I, 4)} kg m^{{2}}.'], p=dict(t='i_dumb', m1=m1, m2=m2, d=d))

def g_torq(rng):
    t = rng.choice(['t_cross', 't_wheel', 't_fall', 't_theta', 't_stop', 't_atw', 't_spin'])
    if t == 't_cross':
        r = [rng.randint(-3, 3) for _ in range(3)]; F = [rng.randint(-3, 3) for _ in range(3)]; tau = list(cross(r, F)); need(any(tau))
        right = vec(tau); o, a = mcq(rng, right, [vec([-x for x in tau]), vec(list(cross(F, r)) if list(cross(F, r)) != [-x for x in tau] else [x + 1 for x in tau]), vec([tau[0], -tau[1], tau[2]]), vec([x + 1 for x in tau]), vec([tau[2], tau[1], tau[0]])])
        return dict(q=f'A force ({vec(F)}) N acts at the point r⃗ = ({vec(r)}) m. Its torque about the origin is (N m) :', o=o, a=a, sol=['τ⃗ = r⃗ × F⃗ (order matters).', f'= {right}.'], p=dict(t=t, r=r, F=F))
    if t == 't_wheel':
        F, R, I, T = rng.choice([5, 10, 20, 40]), rng.choice([0.1, 0.2, 0.25, 0.5]), rng.choice([0.1, 0.2, 0.4, 0.5, 1, 2]), rng.choice([2, 4, 5, 10]); w = F * R / I * T; need(abs(w - round(w)) < 1e-9)
        return dict(q=f'A string wound on a wheel (I = {I} kg m^{{2}}, radius {R} m, frictionless axle, at rest) is pulled with {F} N. The angular speed after {T} s is ____ rad/s.', o=None, a=round(w),
                    sol=['α = \\f{FR}{I}; ω = αt.', f'α = {nf(F * R / I)} rad/s^{{2}} → ω = {nf(w)} rad/s.'], p=dict(t=t, F=F, R=R, I=I, T=T))
    if t == 't_fall':
        m, M, body, h = rng.choice([1, 2, 3, 4]), rng.choice([2, 4, 6, 8, 10]), rng.choice(['disc', 'ring']), rng.choice([1, 2, 3, 4, 5]); k = K2[body]; v2 = 2 * m * G * h / (m + k * M); v = math.sqrt(v2); half(v * 10)
        return dict(q=f'A {m} kg block hangs from a string wound on a {body}-shaped pulley of mass {M} kg (fixed axle). Released from rest, its speed after falling {h} m is ____ × 10^{{−1}} m/s (nearest integer; g = 10).', o=None, a=round(v * 10),
                    sol=[f'mgh = ½(m + {FR[k]}M)v^{{2}}.', f'v = √{{\\f{{2 × {m} × 10 × {h}}}{{{nf(m + k * M)}}}}} ≈ {nf(v, 4)} m/s.'], p=dict(t=t, m=m, M=M, k=k, h=h))
    if t == 't_theta':
        a, b, T = rng.randint(1, 6), rng.randint(-8, 8), rng.randint(1, 4); k = rng.choice([0.5, 1]); w = 2 * a * T + b; P = k * 2 * a * w; need(w != 0)
        right = f'{nf(P)}MR^{{2}}'; o, an = mcq(rng, right, [f'{nf(x)}MR^{{2}}' for x in (P * 2 if k == 0.5 else P / 2, 2 * a * k * (a * T * T + b * T), k * a * w, P + 2 * a * k * 2)])
        return dict(q=f'A {"disc" if k == 0.5 else "ring"} (mass M, radius R) turns about its central axis with θ(t) = {a}t^{{2}} {"+" if b >= 0 else "−"} {abs(b)}t. The power delivered by the torque at t = {T} s is :', o=o, a=an,
                    sol=['α = θ″, ω = θ′ → P = Iαω.', f'α = {2 * a}, ω = {w} → P = {FR[k]} × {2 * a} × {w} MR^{{2}} = {right}.'], p=dict(t=t, a=a, b=b, T=T, k=k))
    if t == 't_stop':
        rpm, T = rng.choice([300, 600, 900, 1200, 1800]), rng.choice([5, 10, 15, 20, 30]); n = rpm / 60 * T / 2; need(abs(n - round(n)) < 1e-9)
        return dict(q=f'A wheel spinning at {rpm} rpm is brought to rest uniformly in {T} s. It turns ____ revolutions while stopping.', o=None, a=round(n), sol=['Uniform deceleration: average speed = half the initial.', f'n = \\f{{{rpm}}}{{60}} × \\f{{{T}}}{{2}} = {nf(n)}.'], p=dict(t=t, rpm=rpm, T=T))
    if t == 't_atw':
        m1, m2, Mp = rng.choice([1, 2, 3, 4]), rng.choice([2, 3, 5, 6, 8]), rng.choice([2, 4, 6, 10, 20]); need(m2 > m1); a = (m2 - m1) * G / (m1 + m2 + Mp / 2); half(a * 100)
        return dict(q=f'Masses {m1} kg and {m2} kg hang over a disc pulley of mass {Mp} kg (string does not slip). The acceleration is ____ × 10^{{−2}} m/s^{{2}} (nearest integer; g = 10).', o=None, a=round(a * 100),
                    sol=['Pulley adds \\f{I}{R^{2}} = \\f{M}{2} to the inertia.', f'a = \\f{{({m2} − {m1})g}}{{{m1} + {m2} + {nf(Mp / 2)}}} ≈ {nf(a, 4)} m/s^{{2}}.'], p=dict(t=t, m1=m1, m2=m2, Mp=Mp))
    th, n = rng.choice([2, 3, 4, 5]), rng.choice([2, 3, 4])   # θ in first t s vs next t s ... generalised to the n-th interval
    r = (n * n - (n - 1) ** 2)
    return dict(q=f'A wheel starts from rest with constant angular acceleration and turns {th} rad in the first second. In the {n}{"nd" if n == 2 else ("rd" if n == 3 else "th")} second it turns ____ rad.', o=None, a=th * r,
                sol=['θ ∝ t^{2} → the n-th second covers (2n − 1) times the first.', f'= {th} × {r} = {th * r} rad.'], p=dict(t='t_spin', th=th, n=n))

def g_angmom(rng):
    t = rng.choice(['l_add', 'l_loss', 'l_line', 'l_shrink', 'l_dumb'])
    if t in ('l_add', 'l_loss'):
        I1, I2, w1 = rng.choice([1, 2, 4, 5, 10]), rng.choice([1, 2, 3, 4, 5]), rng.choice([4, 6, 10, 12, 20]); w2 = rng.choice([0, 0, 2, 4, -2]); w = (I1 * w1 + I2 * w2) / (I1 + I2)
        if t == 'l_add':
            half(w * 100)
            return dict(q=f'A disc (I = {I1} kg m^{{2}}, {w1} rad/s) is joined co-axially with another (I = {I2} kg m^{{2}}, {w2} rad/s). The common angular speed is ____ × 10^{{−2}} rad/s (nearest integer).', o=None, a=round(abs(w) * 100),
                        sol=['No outside torque: I_{1}ω_{1} + I_{2}ω_{2} = (I_{1} + I_{2})ω.', f'ω = {nf(w, 4)} rad/s.'], p=dict(t=t, I1=I1, I2=I2, w1=w1, w2=w2))
        L = 0.5 * I1 * w1 ** 2 + 0.5 * I2 * w2 ** 2 - 0.5 * (I1 + I2) * w * w; half(L)
        return dict(q=f'Two discs, I_{{1}} = {I1} kg m^{{2}} at {w1} rad/s and I_{{2}} = {I2} kg m^{{2}} at {w2} rad/s (same sense), are pressed together face to face. The kinetic energy lost is ____ J (nearest integer).', o=None, a=round(L),
                    sol=['Common ω from angular momentum; loss = KE before − KE after.', f'ω = {nf(w, 4)} rad/s → loss ≈ {nf(L, 4)} J.'], p=dict(t=t, I1=I1, I2=I2, w1=w1, w2=w2))
    if t == 'l_line':
        m, c, s = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 5, 6]), rng.choice([1, 2, 3])   # line y = x + c, speed s√2
        L = m * c * s   # v = (s, s); r0 = (0, c)
        return dict(q=f'A {m} kg particle moves with speed {s}√{{2}} m/s along the line y = x + {c} (in the xy-plane). Its angular momentum about the origin is ____ kg m^{{2}}/s.', o=None, a=L,
                    sol=['L = mvd with d = the perpendicular distance of the line from O = \\f{c}{√{2}}.', f'L = {m} × {s}√{{2}} × \\f{{{c}}}{{√{{2}}}} = {L}.'], p=dict(t=t, m=m, c=c, s=s))
    if t == 'l_shrink':
        body = rng.choice(['solid sphere', 'disc']); f = rng.choice([2, 3]); keep = rng.choice(['density', 'mass'])
        ratio = {('solid sphere', 'density'): f ** 5, ('solid sphere', 'mass'): f ** 2, ('disc', 'density'): f ** 4, ('disc', 'mass'): f ** 2}[(body, keep)]
        return dict(q=f'A spinning {body} (no outside torque) shrinks to 1/{f} of its radius keeping its {"density (it loses mass)" if keep == "density" else "mass"}{" and thickness" if body == "disc" and keep == "density" else ""}. Its angular speed becomes ____ times.', o=None, a=ratio,
                    sol=['Iω = constant.', f'I falls by a factor {ratio} → ω rises {ratio} times.'], p=dict(t=t, body=body, f=f, keep=keep))
    m1, m2 = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (2, 5)]); I = m1 * m2 / (m1 + m2)   # in units of m d²
    right = f'\\f{{{nf(1 / I, 3)}L}}{{md^{{2}}}}'; o, a = mcq(rng, right, [f'\\f{{{nf(x, 3)}L}}{{md^{{2}}}}' for x in (1 / (m1 + m2), I, 1 / (m1 * m1 + m2 * m2), 2 / I)])
    return dict(q=f'Balls of {m1}m and {m2}m are fixed to the ends of a light rod of length d. If its angular momentum about an axis through the CM ⊥ to the rod is L, the angular speed is :', o=o, a=a,
                sol=['I = \\f{m_{1}m_{2}}{m_{1} + m_{2}}d^{2}.', f'= {nf(I, 4)}md^{{2}} → ω = \\f{{L}}{{I}}.'], p=dict(t='l_dumb', m1=m1, m2=m2))

def g_roll(rng):
    t = rng.choice(['r_acc', 'r_ke', 'r_frac', 'r_h', 'r_top', 'r_rim', 'r_slip'])
    body = rng.choice(list(K2)); k = K2[body]
    if t == 'r_acc':
        th = rng.choice([30, 37, 45, 53, 60]); s = {37: 0.6, 53: 0.8}.get(th, math.sin(math.radians(th))); a = G * s / (1 + k); half(a * 100)
        return dict(q=f'A {body} rolls without slipping down a {th}° incline{" (sin 37° = 0.6)" if th in (37, 53) else ""}. Its acceleration is ____ × 10^{{−2}} m/s^{{2}} (nearest integer; g = 10).', o=None, a=round(a * 100),
                    sol=['a = \\f{g sinθ}{1 + k^{2}/R^{2}}.', f'= \\f{{10 × {nf(s, 3)}}}{{1 + {FR[k]}}} ≈ {nf(a, 4)} m/s^{{2}}.'], p=dict(t=t, k=k, s=s))
    if t == 'r_ke':
        m, v = rng.choice([1, 2, 4, 5, 10, 20, 50]), rng.choice([0.2, 0.4, 0.5, 1, 2, 3]); K = 0.5 * m * v * v * (1 + k); half(K * 100)
        return dict(q=f'A {body} of mass {m} kg rolls with its centre moving at {v} m/s. The work needed to stop it is ____ × 10^{{−2}} J (nearest integer).', o=None, a=round(K * 100),
                    sol=['K = ½mv^{2}(1 + \\f{k^{2}}{R^{2}}).', f'= ½ × {m} × {v}^{{2}} × {nf(1 + k, 4)} ≈ {nf(K, 4)} J.'], p=dict(t=t, k=k, m=m, v=v))
    if t == 'r_frac':
        ask = rng.choice(['rot/total', 'trans/rot', 'trans/total']); val = {'rot/total': k / (1 + k), 'trans/rot': 1 / k, 'trans/total': 1 / (1 + k)}[ask]
        right = nf(val, 3); o, a = mcq(rng, right, [nf(x, 3) for x in (k, 1 + k, k / (1 + k), 1 / k, 1 / (1 + k), 0.5)])
        return dict(q=f'For a {body} rolling without slipping, the ratio of {"rotational KE to total KE" if ask == "rot/total" else ("translational KE to rotational KE" if ask == "trans/rot" else "translational KE to total KE")} is :', o=o, a=a,
                    sol=[f'K_{{trans}} = ½mv^{{2}}, K_{{rot}} = {FR[k]} × ½mv^{{2}}.', f'Ratio ≈ {right}.'], p=dict(t=t, k=k, ask=ask))
    if t == 'r_h':
        v = rng.choice([2, 3, 4, 5, 6]); rough = rng.choice([True, True, False]); h = v * v / (2 * G) * ((1 + k) if rough else 1); half(h * 100)
        return dict(q=f'A {body} rolls at {v} m/s and then runs up a {"rough (it keeps rolling)" if rough else "perfectly smooth"} incline. The greatest height reached is ____ × 10^{{−2}} m (nearest integer; g = 10).', o=None, a=round(h * 100),
                    sol=['Rough: all KE → mgh. Smooth: no friction torque, spin stays — only ½mv^{2} → mgh.', f'h ≈ {nf(h, 4)} m.'], p=dict(t=t, k=k, v=v, rough=rough))
    if t == 'r_top':
        M1, M2 = rng.choice([1, 2, 3, 5]), rng.choice([1, 2, 3, 5]); b2 = rng.choice([x for x in K2 if x != body]); k2 = K2[b2]
        a1, a2 = 2 / (M1 * (1 + k)), 2 / (M2 * (1 + k2)); r = a1 / a2
        right = nf(r, 3); o, a = mcq(rng, right, [nf(x, 3) for x in (1 / r, (1 + k2) / (1 + k), M2 / M1, r * 2)])
        return dict(q=f'Equal forces are applied horizontally at the TOP of a {body} (mass {M1}m) and a {b2} (mass {M2}m) of equal radius; both roll without slipping. a_{{1}} : a_{{2}} ≈', o=o, a=a,
                    sol=['F + f = Ma and (F − f)R = Ia/R → a = \\f{2F}{M + I/R^{2}}.', f'Ratio ≈ {right}.'], p=dict(t=t, k=k, k2=k2, M1=M1, M2=M2))
    if t == 'r_rim':
        v = rng.choice([2, 4, 5, 6, 8, 10]); where = rng.choice(['top', 'side', 'bottom'])
        val = {'top': 2 * v, 'side': v * math.sqrt(2), 'bottom': 0}[where]
        right = {'top': f'{2 * v} m/s', 'side': f'{v}√{{2}} m/s', 'bottom': '0 m/s'}[where]; o, a = mcq(rng, right, [f'{2 * v} m/s', f'{v}√{{2}} m/s', '0 m/s', f'{v} m/s', f'{2 * v}√{{2}} m/s'])
        return dict(q=f'A wheel rolls with its centre moving at {v} m/s. The speed of the rim point {"at the top" if where == "top" else ("level with the centre" if where == "side" else "touching the ground")} is :', o=o, a=a,
                    sol=['Each rim point = v (forward) + v (along the rim).', f'→ {right}.'], p=dict(t=t, v=v, where=where))
    v0, mu, f = rng.choice([7, 14, 21, 28, 49]), rng.choice([0.1, 0.2, 0.25, 0.5]), rng.choice([0, 0.25, 0.5])   # cylinder/ball sliding, initial spin f·v0/R
    kk = rng.choice([0.5, 0.4]); T = v0 * (1 - f) / (mu * 9.8 * (1 + 1 / kk)); half(T * 10)
    return dict(q=f'A {"solid cylinder" if kk == 0.5 else "solid sphere"} is launched on a rough floor (μ = {mu}) with speed {v0} m/s and spin {"zero" if f == 0 else f"{nf(f)}v_{{0}}/R (rolling sense)"}. It starts pure rolling after ____ × 10^{{−1}} s (nearest integer; g = 9.8).', o=None, a=round(T * 10),
                sol=['Friction slows the centre: v = v_{0} − μgt. Its torque spins it up: ωR = ω_{0}R + \\f{μgR^{2}}{k^{2}}t.', f'Set v = ωR → t = \\f{{v_{{0}}(1 − {nf(f)})}}{{μg(1 + R^{{2}}/k^{{2}})}} ≈ {nf(T, 4)} s.'], p=dict(t='r_slip', v0=v0, mu=mu, f=f, kk=kk))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(com=g_com, moi=g_moi, torq=g_torq, angmom=g_angmom, roll=g_roll).items()}
def finish(it): return it
def lin2(a, b, c, d, e, f): D = a * d - b * c; return (e * d - b * f) / D, (a * f - e * c) / D
def ring_pts(R, n=720): return [(R * math.cos(2 * math.pi * (i + 0.5) / n), R * math.sin(2 * math.pi * (i + 0.5) / n)) for i in range(n)]
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'm_pts':
        M = sum(p['ms']); want = (sum(m * x for m, (x, _) in zip(p['ms'], p['P'])) / M, sum(m * y for m, (_, y) in zip(p['ms'], p['P'])) / M)
        x, y = [num(s) for s in Rv.strip('()').split(', ')]; return abs(x - want[0]) < 1e-6 and abs(y - want[1]) < 1e-6
    if t == 'm_shift':
        x1, x2 = 0.0, 10.0; c = (p['m1'] * x1 + p['m2'] * x2) / (p['m1'] + p['m2']); d = Rv / 10
        return abs((p['m1'] * (x1 + p['d']) + p['m2'] * (x2 - d)) / (p['m1'] + p['m2']) - c) < 0.006
    if t == 'm_hole':
        R, r = p['R'], p['r']; n = 400; h = 2 * R / n; A = Sx = 0.0
        for i in range(n):
            for j in range(n):
                x, y = -R + (i + 0.5) * h, -R + (j + 0.5) * h
                if x * x + y * y <= R * R and (x - (R - r)) ** 2 + y * y > r * r: A += 1; Sx += x
        return abs(Rv - abs(Sx / A) * 100) <= 1.5
    if t == 'm_lrod':
        a, b, L = p['a'], p['b'], p['L']; n = 2000; pts = [(0, (i + 0.5) * a * L / n) for i in range(n)] * a + [((i + 0.5) * b * L / n, 0) for i in range(n)] * b   # equal density: weight each part by its length
        cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts); xs, ys = Rv.replace('ĵ', '').split('î + '); return close(num(xs), cx, 1e-3) and close(num(ys), cy, 1e-3)
    if t == 'i_body':   # central values, then perpendicular / parallel axis theorems applied afresh
        b, ax, m, R = p['body'], p['axn'], p['m'], p['R']
        if b.startswith('rod'): I = m * (2 * R) ** 2 / 12 + m * R * R
        elif 'sphere' in b: I = (0.4 if b == 'solid sphere' else 2 / 3) * m * R * R + m * R * R
        else:
            perp = (1.0 if b == 'ring' else 0.5) * m * R * R; diam = perp / 2
            I = {'diameter': diam, 'tangent in its plane': diam + m * R * R, 'tangent ⊥ its plane': perp + m * R * R}[ax]
        return Rv == round(I * 100)
    if t == 'i_par':
        k = {'solid sphere': 0.4, 'hollow sphere': 2 / 3, 'disc': 0.5, 'ring': 1.0}[p['body']]; return Rv == round((k * p['m'] * p['R'] ** 2 + p['m'] * p['d'] ** 2) * 1000)
    if t == 'i_sq':
        a = p['a']; o_ = {'vertex': (0, 0), 'centre': (a / 2, a / 2), 'side': (a / 2, 0)}[p['where']]; return Rv == round(sum(p['m'] * math.dist(q, o_) ** 2 for q in [(0, 0), (a, 0), (0, a), (a, a)]) * 10)
    if t == 'i_scale':
        s, f = p['s'], p['f']; I = lambda R, Lth, kind: (R ** 2 * Lth) * R * R if kind != 'sphere' else R ** 3 * R * R
        if p['kind'] == 'disc_same_t': return Rv == round(I(s, 1, 'd') / I(1, 1, 'd'))
        if p['kind'] == 'cyl': return Rv == round(I(1, 1, 'c') / I(1 / s, 1 / f, 'c'))
        return Rv == round(I(s, 1, 'sphere') / I(1, 1, 'sphere'))
    if t == 'i_gyr': return Rv == round(p['k'] * p['R'] ** 2 + p['d'] ** 2)
    if t == 'i_cut':
        q = p['q']; n = 500; h = 2 / n; A = S = 0.0; rr = 1 / q; c = 1 - rr
        for i in range(n):
            for j in range(n):
                x, y = -1 + (i + 0.5) * h, -1 + (j + 0.5) * h
                if x * x + y * y <= 1: A += 1
                if x * x + y * y <= 1 and (x - c) ** 2 + y * y > rr * rr: S += x * x + y * y
        M_full = A; return close(num(Rv), S / M_full, 0.01)
    if t == 'i_dumb':
        m1, m2, d = p['m1'], p['m2'], p['d']; c = m2 * d / (m1 + m2); return Rv == round((m1 * c * c + m2 * (d - c) ** 2) * 1000)
    if t == 't_cross':
        s = Rv.replace('− ', '-').replace('+ ', '').replace('î', ' ').replace('ĵ', ' ').replace('k̂', ' ').split(); return [int(x) for x in s] == list(cross(p['r'], p['F']))
    if t == 't_wheel':
        w = 0.0; dt = 1e-3
        for _ in range(int(round(p['T'] / dt))): w += p['F'] * p['R'] / p['I'] * dt
        return Rv == round(w)
    if t == 't_fall':
        a, T = lin2(p['m'], 1, p['k'] * p['M'], -1, p['m'] * G, 0); return Rv == round(math.sqrt(2 * a * p['h']) * 10)   # mg − T = ma ; T = kMa
    if t == 't_theta':
        th = lambda s: p['a'] * s * s + p['b'] * s; T = p['T']; e = 1e-3; w = (th(T + e) - th(T - e)) / (2 * e); al = (th(T + e) - 2 * th(T) + th(T - e)) / e ** 2
        return close(num(Rv.replace('MR^{2}', '')), p['k'] * al * w, 1e-4)
    if t == 't_stop':
        w0 = p['rpm'] / 60; dt = 1e-3; ang = 0.0; tt = 0.0
        while tt < p['T'] - 1e-12: ang += (w0 - w0 / p['T'] * (tt + dt / 2)) * dt; tt += dt
        return Rv == round(ang)
    if t == 't_atw':
        a, _ = lin2(p['m2'] + p['m1'], 0, 0, 1, (p['m2'] - p['m1']) * G - p['Mp'] / 2 * 0, 0)
        a = (p['m2'] - p['m1']) * G / (p['m1'] + p['m2'] + 0.5 * p['Mp']); T1 = p['m1'] * (G + a); T2 = p['m2'] * (G - a)
        return abs((T2 - T1) - 0.5 * p['Mp'] * a) < 1e-9 and Rv == round(a * 100)   # torque balance on the disc checks the formula
    if t == 't_spin':
        al = 2 * p['th']; n = p['n']; return Rv == round(0.5 * al * (n * n - (n - 1) ** 2))
    if t == 'l_add':
        w = (p['I1'] * p['w1'] + p['I2'] * p['w2']) / (p['I1'] + p['I2']); return Rv == round(abs(w) * 100)
    if t == 'l_loss':
        w = (p['I1'] * p['w1'] + p['I2'] * p['w2']) / (p['I1'] + p['I2']); return Rv == round(0.5 * p['I1'] * p['w1'] ** 2 + 0.5 * p['I2'] * p['w2'] ** 2 - 0.5 * (p['I1'] + p['I2']) * w * w)
    if t == 'l_line':
        x0, y0 = 1.7, 1.7 + p['c']; v = (p['s'], p['s']); return Rv == round(abs(p['m'] * (x0 * v[1] - y0 * v[0])))
    if t == 'l_shrink':
        f = p['f']; M = (1 / f) ** (3 if p['body'] == 'solid sphere' else 2) if p['keep'] == 'density' else 1; return Rv == round(1 / (M * (1 / f) ** 2))
    if t == 'l_dumb':
        m1, m2 = p['m1'], p['m2']; c = m2 / (m1 + m2); I = m1 * c * c + m2 * (1 - c) ** 2; return close(float(Rv.split('{')[1].split('L')[0]), 1 / I, 3e-3)
    if t == 'r_acc':
        a, f = lin2(1, 1, p['k'], -1, G * p['s'], 0); return Rv == round(a * 100)   # a + f/m = g sinθ ; f·R = I a/R → f/m = k a
    if t == 'r_ke':
        v = p['v']; return Rv == round((0.5 * p['m'] * v * v + 0.5 * p['k'] * p['m'] * v * v) * 100)
    if t == 'r_frac':
        Kt, Kr = 1.0, p['k']; return close(num(Rv), {'rot/total': Kr / (Kt + Kr), 'trans/rot': Kt / Kr, 'trans/total': Kt / (Kt + Kr)}[p['ask']], 3e-3)
    if t == 'r_h':
        v = p['v']; E = 0.5 * v * v * (1 + p['k']) if p['rough'] else 0.5 * v * v; return Rv == round(E / G * 100)
    if t == 'r_top':
        acc = lambda M, k: lin2(M, -1, k * M, 1, 1.0, 1.0)[0]   # Ma − f = F ; kMa + f = F
        return close(num(Rv), acc(p['M1'], p['k']) / acc(p['M2'], p['k2']), 3e-3)
    if t == 'r_rim':
        v = p['v']; w = v / 1.0; pt = {'top': (0, 1), 'side': (1, 0), 'bottom': (0, -1)}[p['where']]; vel = (v + w * pt[1], -w * pt[0]); want = math.hypot(*vel)
        got = 0.0 if Rv.startswith('0 ') else (float(Rv.split('√')[0]) * math.sqrt(2) if '√' in Rv else num(Rv)); return abs(got - want) < 1e-9
    if t == 'r_slip':
        v, w, R, dt, tt = p['v0'], p['f'] * p['v0'] / 1.0, 1.0, 1e-4, 0.0
        while v > w * R + 1e-9: v -= p['mu'] * 9.8 * dt; w += p['mu'] * 9.8 * R / (p['kk'] * R * R) * dt; tt += dt
        return abs(Rv - tt * 10) <= 0.6
    raise KeyError(t)
