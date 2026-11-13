"""Practice generators — Physics Unit 16: Optics. check() re-solves each item without the mirror/lens formulas:
mirrors and lenses by tracing a near-axis ray through the real curved surfaces (reflection law / Snell's law),
prisms and slabs by applying Snell's law face by face, and interference/diffraction/polarisation by adding wave
phasors or averaging cos² numerically."""
import math, cmath, re
from common import mcq, nf
from op_pyq import snell, surf, axis_cross, lens_image, focal, mirror_image, yd, biconvex, thin_f, first_zero
pi = math.pi
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def isint(x): return abs(x - round(x)) < 1e-9
def opts(rng, v, k=(2, 0.5, 1.5, -1, 4, 0.75, 3)):
    w = []
    for f in k:
        s = nf(v * f, 3)
        if s != nf(v, 3) and s not in w: w.append(s)
    rng.shuffle(w); return mcq(rng, nf(v, 3), w)
def thin(f): return biconvex(f, f, 1.5) if f > 0 else [(0, f, 1, 1.5), (0, -f, 1.5, 1)]
def at(z, S): return [(z + s[0], s[1], s[2], s[3]) for s in S]
def trace(u, S, h=1e-7):
    ray = (u, 0.0, h)
    for s in S: ray = surf(*s, ray)
    return axis_cross(ray)
def Fr(x):   # neat fraction text for numeric answers
    from fractions import Fraction
    q = Fraction(x).limit_denominator(60)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'

def g_mirror(rng):
    t = rng.choice(['m_img', 'm_mag', 'm_find', 'm_rod', 'm_two'])
    if t == 'm_img':
        kind = rng.choice(['concave', 'convex']); f = rng.choice([5, 10, 12, 15, 20, 24, 25, 30]); u = rng.choice([6, 8, 10, 15, 18, 20, 25, 30, 36, 40, 45, 50, 60]); need(u != f)
        F = -f if kind == 'concave' else f; v = 1 / (1 / F + 1 / u); need(abs(v) < 500)
        sv = nf(abs(v), 3); where = 'in front of' if v < 0 else 'behind'
        w = [f'{nf(abs(v), 3)} cm {"behind" if v < 0 else "in front of"} the mirror', f'{nf(abs(1 / (1 / F - 1 / u)), 3)} cm {where} the mirror', f'{nf(abs(v) * 2, 3)} cm {where} the mirror', f'{nf(f, 3)} cm {where} the mirror']
        right = f'{sv} cm {where} the mirror'; w = [x for x in dict.fromkeys(w) if x != right][:3]; need(len(w) == 3)
        o, an = mcq(rng, right, w)
        return dict(q=f'An object is {u} cm in front of a {kind} mirror of focal length {f} cm. The image is formed', o=o, a=an,
                    sol=[f'\\f{{1}}{{v}} + \\f{{1}}{{u}} = \\f{{1}}{{f}} with u = −{u}, f = {"−" if kind == "concave" else "+"}{f}.', f'v = {nf(v, 4)} cm → {right}.'], p=dict(t=t, R=2 * F / 100, u=u / 100, ans=v))
    if t == 'm_mag':
        kind = rng.choice(['concave', 'convex']); f = rng.choice([10, 12, 15, 20, 25, 30]); u = rng.choice([5, 10, 15, 20, 30, 40, 45, 60, 90]); need(u != f)
        F = -f if kind == 'concave' else f; v = 1 / (1 / F + 1 / u); m = v / u   # m = −v/u with u = −u
        o, an = opts(rng, m, (-1, 2, 0.5, -2))
        return dict(q=f'An object is {u} cm in front of a {kind} mirror of focal length {f} cm. The magnification is', o=o, a=an, sol=['m = −\\f{v}{u} = \\f{f}{f − u}.', f'= {nf(m, 3)}.'], p=dict(t=t, R=2 * F / 100, u=u / 100))
    if t == 'm_find':
        m = rng.choice([-4, -3, -2, -0.5, 2, 3, 4, 0.5, 0.25, 1 / 3]); kind = 'concave' if (m < 0 or m > 1) else 'convex'; D = rng.choice([10, 15, 20, 30, 40, 45, 60])
        # v = −m u (sign convention, u < 0). Distance between object and image
        if m < 0: u = D / (abs(m) - 1) if abs(m) > 1 else D / (1 - abs(m))
        else: u = D / (1 + m)
        v = -m * (-u); F = 1 / (1 / v + 1 / (-u)); f = F
        o, an = opts(rng, f, (-1, 2, 0.5, 1.5))
        return dict(q=f'A mirror forms an image with magnification {Fr(m) if m < 0 or m >= 1 else Fr(m)}. The object–image distance is {D} cm. The focal length of the mirror (in cm, sign included) is', o=o, a=an,
                    sol=['m = −\\f{v}{u}: use it with the given separation to find u and v.', f'u = −{nf(u, 4)} cm, v = {nf(v, 4)} cm → f = {nf(f, 3)} cm.'], p=dict(t=t, m=m, D=D / 100, f=f / 100))
    if t == 'm_rod':
        f = rng.choice([10, 15, 20]); near = rng.choice([2 * f, 3 * f, int(2.5 * f)]); L = rng.choice([5, 10, 15, 20]); F = -f
        v1 = 1 / (1 / F + 1 / near); v2 = 1 / (1 / F + 1 / (near + L)); Lv = abs(v1 - v2)
        o, an = opts(rng, Lv, (2, 0.5, 1.5, 3))
        return dict(q=f'A rod of length {L} cm lies along the axis of a concave mirror (f = {f} cm), its nearer end {near} cm from the mirror. The length of its image (in cm) is', o=o, a=an,
                    sol=['Image each end separately.', f'v_{{1}} = {nf(v1, 4)}, v_{{2}} = {nf(v2, 4)} → length {nf(Lv, 3)} cm.'], p=dict(t=t, R=2 * F / 100, a=near / 100, b=(near + L) / 100))
    f = rng.choice([5, 10, 12, 15, 20, 25, 30]); m = rng.choice([2, 3, 4]); d = abs(f * (1 + 1 / m) - f * (1 - 1 / m))
    return dict(q=f'A concave mirror of focal length {f} cm forms an image {m} times the size of the object for two different object positions. The distance between these positions is ____ cm.', o=None, a=round(d) if isint(d) else need(False),
                sol=[f'm = \\f{{f}}{{f − u}} = ±{m} with f = −{f}.', f'u = −{nf(f * (1 + 1 / m), 4)} and −{nf(f * (1 - 1 / m), 4)} cm → {round(d)} cm apart.'], p=dict(t='m_two', f=f / 100, m=m))

def g_lens(rng):
    t = rng.choice(['l_img', 'l_maker', 'l_medium', 'l_sep', 'l_contact', 'l_micro', 'l_res', 'l_silver', 'l_real'])
    if t == 'l_img':
        f = rng.choice([10, 12, 15, 20, 24, 25, 30, -10, -15, -20, -30]); u = rng.choice([5, 8, 10, 15, 20, 25, 30, 40, 45, 60]); need(u != f)
        v = 1 / (1 / f - 1 / u)
        o, an = opts(rng, v, (-1, 2, 0.5, 1.5))
        return dict(q=f'An object is {u} cm in front of a {"convex" if f > 0 else "concave"} lens of focal length {abs(f)} cm. The image distance (in cm, + for the far side) is', o=o, a=an,
                    sol=['\\f{1}{v} − \\f{1}{u} = \\f{1}{f}.', f'v = {nf(v, 3)} cm.'], p=dict(t=t, f=f / 100, u=u / 100))
    if t == 'l_maker':
        n, R1, R2 = rng.choice([1.4, 1.5, 1.6, 1.7]), rng.choice([10, 12, 15, 20, 24, 30, 40]), rng.choice([10, 12, 15, 20, 30, 40, 60, 0]); kind = 'plano-convex' if R2 == 0 else 'biconvex'
        f = 1 / ((n - 1) * (1 / R1 + (1 / R2 if R2 else 0)))
        o, an = opts(rng, f, (2, 0.5, 1.5, 0.75))
        rs = f'radius {R1} cm' if not R2 else f'radii {R1} cm and {R2} cm'
        return dict(q=f'A thin {kind} lens of refractive index {n} has {rs}. Its focal length (in cm) is', o=o, a=an, sol=['\\f{1}{f} = (n − 1)(\\f{1}{R_{1}} − \\f{1}{R_{2}}).', f'f = {nf(f, 3)} cm.'], p=dict(t=t, n=n, R1=R1 / 100, R2=R2 / 100))
    if t == 'l_medium':
        n, nm, f = rng.choice([1.5, 1.6, 1.4, 1.7]), rng.choice([4 / 3, 1.2, 1.25, 1.6, 1.33]), rng.choice([10, 12, 15, 18, 20, 24, 30]); need(abs(n - nm) > 0.01)
        fm = f * (n - 1) / (n / nm - 1)
        o, an = opts(rng, fm, (-1, 2, 0.5, 1.5))
        return dict(q=f'A thin lens (n = {n}) has focal length {f} cm in air. Its focal length (in cm) in a liquid of refractive index {nf(nm, 3)} is', o=o, a=an, sol=['\\f{f_{m}}{f_{a}} = \\f{n − 1}{n/n_{m} − 1}.', f'f_{{m}} = {nf(fm, 3)} cm.'], p=dict(t=t, n=n, nm=nm, f=f / 100))
    if t == 'l_sep':
        f1, f2, d = rng.choice([10, 15, 20, 25, 30, 40]), rng.choice([10, 15, 20, 25, 30, -20, -30]), rng.choice([0, 5, 10, 15, 20]); P = 100 / f1 + 100 / f2 - d / 100 * (100 / f1) * (100 / f2)
        need(abs(P) > 1e-9)
        o, an = opts(rng, P, (-1, 2, 0.5, 1.5))
        return dict(q=f'Thin lenses of focal lengths {f1} cm and {f2} cm are placed coaxially {d} cm apart. The power of the combination (in D) is', o=o, a=an, sol=['P = P_{1} + P_{2} − dP_{1}P_{2} (d in m).', f'= {nf(P, 3)} D.'], p=dict(t=t, f1=f1 / 100, f2=f2 / 100, d=d / 100))
    if t == 'l_contact':
        fc, fd, u = rng.choice([10, 15, 20, 30, 40, 60]), rng.choice([10, 15, 20, 30, 40, 60]), rng.choice([10, 20, 30, 40, 60]); need(fc != fd)
        F = 1 / (1 / fc - 1 / fd); need(abs(F - u) > 1e-6); v = 1 / (1 / F - 1 / u)
        o, an = opts(rng, v, (-1, 2, 0.5, 1.5))
        return dict(q=f'A convex lens (f = {fc} cm) is in contact with a concave lens (f = {fd} cm). An object is {u} cm in front. The image distance (in cm, + for the far side) is', o=o, a=an,
                    sol=['\\f{1}{F} = \\f{1}{f_{1}} + \\f{1}{f_{2}}.', f'F = {nf(F, 4)} cm → v = {nf(v, 3)} cm.'], p=dict(t=t, fc=fc / 100, fd=fd / 100, u=u / 100))
    if t == 'l_micro':
        fo, fe, L = rng.choice([1, 2, 4, 5]), rng.choice([2, 4, 5, 10]), rng.choice([10, 15, 16, 20, 30, 32]); m = L / fo * 25 / fe; need(isint(m))
        return dict(q=f'A compound microscope has f_{{o}} = {fo} cm, f_{{e}} = {fe} cm and tube length {L} cm. The magnifying power in normal adjustment (D = 25 cm) is ____.', o=None, a=round(m),
                    sol=['m = \\f{L}{f_{o}} × \\f{D}{f_{e}}.', f'= {round(m)}.'], p=dict(t=t, fo=fo / 100, fe=fe / 100, L=L / 100))
    if t == 'l_res':
        lam, th = rng.choice([400, 500, 550, 600, 610]), rng.choice([1, 2, 3, 5, 6]) * 1e-7; D = 1.22 * lam * 1e-9 / th * 100
        o, an = opts(rng, D, (2, 0.5, 1 / 1.22, 1.5))
        return dict(q=f'A telescope must resolve {nf(th, 2)} rad with light of {lam} nm. The minimum objective diameter (in cm) is', o=o, a=an, sol=['θ = \\f{1.22λ}{D}.', f'D = {nf(D, 3)} cm.'], p=dict(t=t, lam=lam * 1e-9, th=th))
    if t == 'l_silver':
        n, R = rng.choice([1.5, 1.6, 1.4]), rng.choice([10, 15, 20, 30, 40]); kind = rng.choice(['bi', 'plano'])
        P = (2 * (n - 1) * 2 / R + 2 / R) if kind == 'bi' else 2 * (n - 1) / R; f = 1 / P
        o, an = opts(rng, 2 * f, (2, 0.5, 1.5, 0.75))
        q = (f'An equi-convex lens (n = {n}, radii {R} cm) has one face silvered. An object placed on the axis is imaged onto itself when it is at (in cm)' if kind == 'bi'
             else f'A plano-convex lens (n = {n}, curved radius {R} cm) has its plane face silvered. An object placed in front of the curved face is imaged onto itself when it is at (in cm)')
        return dict(q=q, o=o, a=an, sol=['Silvered lens: P = 2P_{lens} + P_{mirror}.', f'f = {nf(f, 3)} cm; the object must be at 2f = {nf(2 * f, 3)} cm.'], p=dict(t=t, n=n, R=R / 100, kind=kind))
    m, D = rng.choice([2, 3, 4, 0.5]), rng.choice([18, 24, 27, 30, 36, 45, 48, 50, 60, 80, 90]); u = D / (1 + m); v = m * u; f = 1 / (1 / v + 1 / u)
    o, an = opts(rng, f, (2, 0.5, 1.5, 0.75))
    return dict(q=f'A convex lens forms a real image {Fr(m)} times the size of the object; object and image are {D} cm apart. The focal length (in cm) is', o=o, a=an,
                sol=['Real image: v = m|u| on the far side, |u| + v = D.', f'|u| = {nf(u, 4)}, v = {nf(v, 4)} → f = {nf(f, 3)} cm.'], p=dict(t='l_real', m=m, D=D / 100))

def g_refr(rng):
    t = rng.choice(['r_lam', 'r_app', 'r_surf', 'r_prism', 'r_crit', 'r_slab', 'r_thin', 'r_nodev'])
    if t == 'r_lam':
        n1, n2, lam = rng.choice([1, 4 / 3, 1.5, 1.2]), rng.choice([1.5, 4 / 3, 1.6, 2, 1.25]), rng.choice([400, 480, 500, 540, 600, 640]); need(n1 != n2)
        l2 = lam * n1 / n2
        o, an = opts(rng, l2, (n2 / n1, 2, 0.5, n1 * n2))
        return dict(q=f'Light has wavelength {lam} nm in a medium of refractive index {nf(n1, 3)}. Its wavelength (in nm) in a medium of refractive index {nf(n2, 3)} is', o=o, a=an, sol=['Frequency is fixed, so nλ is constant.', f'λ = {nf(l2, 3)} nm.'], p=dict(t=t, n1=n1, n2=n2, lam=lam))
    if t == 'r_app':
        layers = [(rng.choice([4, 6, 8, 9, 10, 12]), rng.choice([4 / 3, 1.5, 1.2, 1.6, 1.25])) for _ in range(rng.choice([1, 2]))]; app = sum(h / n for h, n in layers)
        o, an = opts(rng, app, (2, 0.5, 1.5, 0.75))
        desc = ' on top of '.join(f'{h} cm of n = {nf(n, 3)}' for h, n in layers[::-1])
        return dict(q=f'A coin lies under {desc}. Seen from directly above, its apparent depth (in cm) is', o=o, a=an, sol=['Apparent depth = Σ \\f{t}{n}.', f'= {nf(app, 3)} cm.'], p=dict(t=t, layers=layers))
    if t == 'r_surf':
        n, R, u = rng.choice([1.5, 1.33, 1.4, 1.6]), rng.choice([10, 20, 25, 30, 40, 50]), rng.choice([20, 30, 40, 50, 60, 80, 100]); s = rng.choice([1, -1])
        v = n / ((n - 1) / (s * R) - 1 / u); need(abs(v) < 2000)
        o, an = opts(rng, v, (-1, 2, 0.5, 1.5))
        return dict(q=f'A point object in air is {u} cm from a spherical glass surface (n = {n}) of radius {R} cm, {"convex" if s > 0 else "concave"} towards the object. The image distance from the surface (in cm, + inside the glass) is', o=o, a=an,
                    sol=['\\f{n_{2}}{v} − \\f{n_{1}}{u} = \\f{n_{2} − n_{1}}{R}.', f'v = {nf(v, 3)} cm.'], p=dict(t=t, n=n, R=s * R / 100, u=u / 100))
    if t == 'r_prism':
        A, n = rng.choice([30, 45, 60, 75]), rng.choice([math.sqrt(2), math.sqrt(3), 1.5, 1.6, 1.4]); s = n * math.sin(math.radians(A / 2)); need(s < 1)
        dm = 2 * math.degrees(math.asin(s)) - A
        o, an = opts(rng, dm, (2, 0.5, 1.5, 0.75))
        ns = {math.sqrt(2): '√{2}', math.sqrt(3): '√{3}'}.get(n, nf(n, 3))
        return dict(q=f'A prism of angle {A}° has refractive index {ns}. Its angle of minimum deviation (in degrees) is', o=o, a=an, sol=['n = \\f{sin((A + δ)/2)}{sin(A/2)}.', f'δ_{{m}} = {nf(dm, 3)}°.'], p=dict(t=t, A=A, n=n))
    if t == 'r_crit':
        v1, v2 = rng.choice([(2.0, 2.5), (2.4, 2.7), (2.0, 3.0), (1.5, 3.0), (2.25, 3.0), (1.8, 2.4), (2.1, 2.8)]); s = v1 / v2
        o, an = opts(rng, math.degrees(math.asin(s)), (1.2, 0.8, 1.5, 0.6))
        return dict(q=f'Light travels at {v1} × 10^{{8}} m/s in medium A and {v2} × 10^{{8}} m/s in medium B. The critical angle for A → B (in degrees) is', o=o, a=an,
                    sol=['sin C = \\f{n_{B}}{n_{A}} = \\f{v_{A}}{v_{B}}.', f'= {nf(s, 3)} → C = {nf(math.degrees(math.asin(s)), 3)}°.'], p=dict(t=t, v1=v1, v2=v2))
    if t == 'r_slab':
        n, i, h = rng.choice([1.5, math.sqrt(2), math.sqrt(3), 1.6]), rng.choice([30, 45, 60]), rng.choice([2, 3, 4, 5, 6, 10]); r = math.asin(math.sin(math.radians(i)) / n); d = h * math.sin(math.radians(i) - r) / math.cos(r)
        o, an = opts(rng, d, (2, 0.5, 1.5, 0.75))
        ns = {math.sqrt(2): '√{2}', math.sqrt(3): '√{3}'}.get(n, nf(n, 3))
        return dict(q=f'A ray meets a glass slab (n = {ns}, thickness {h} cm) at {i}°. Its lateral shift (in cm) is', o=o, a=an, sol=['d = \\f{t sin(i − r)}{cos r}.', f'r = {nf(math.degrees(r), 3)}° → d = {nf(d, 3)} cm.'], p=dict(t=t, n=n, i=i, h=h))
    if t == 'r_thin':
        A, n = rng.choice([2, 3, 4, 5, 6, 8, 10]), rng.choice([1.4, 1.5, 1.54, 1.6, 1.72]); d = (n - 1) * A
        o, an = opts(rng, d, (2, 0.5, 1.5, n))
        return dict(q=f'A thin prism of angle {A}° and refractive index {n} deviates a ray by (in degrees)', o=o, a=an, sol=['Thin prism: δ = (n − 1)A.', f'= {nf(d, 3)}°.'], p=dict(t=t, A=A, n=n))
    A1, n1, n2 = rng.choice([3, 4, 5, 6, 8, 10]), rng.choice([1.5, 1.54, 1.6, 1.72]), rng.choice([1.6, 1.72, 1.8, 1.9, 2.0]); need(n1 != n2)
    A2 = (n1 - 1) * A1 / (n2 - 1)
    o, an = opts(rng, A2, (2, 0.5, 1.5, 0.75))
    return dict(q=f'A thin prism of angle {A1}° (n = {n1}) is combined with a thin prism of n = {n2} so that there is no deviation. The second prism\'s angle (in degrees) is', o=o, a=an,
                sol=['(n_{1} − 1)A_{1} = (n_{2} − 1)A_{2}.', f'A_{{2}} = {nf(A2, 3)}°.'], p=dict(t='r_nodev', A1=A1, n1=n1, n2=n2))

def g_wave(rng):
    t = rng.choice(['w_beta', 'w_pos', 'w_coin', 'w_sheet', 'w_int', 'w_maxmin', 'w_single', 'w_malus', 'w_brew', 'w_med', 'w_path'])
    if t == 'w_beta':
        lam, d, D = rng.choice([400, 450, 500, 550, 600, 650, 700]), rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 1.0, 2.0]), rng.choice([0.5, 1.0, 1.2, 1.5, 2.0]); b = lam * 1e-9 * D / (d * 1e-3) * 1000
        o, an = opts(rng, b, (2, 0.5, 1.5, 0.75))
        return dict(q=f'In YDSE, λ = {lam} nm, d = {d} mm and D = {D} m. The fringe width (in mm) is', o=o, a=an, sol=['β = \\f{λD}{d}.', f'= {nf(b, 3)} mm.'], p=dict(t=t, lam=lam * 1e-9, d=d * 1e-3, D=D))
    if t == 'w_pos':
        n, lam, d, D = rng.randint(1, 10), rng.choice([400, 500, 600, 700]), rng.choice([0.2, 0.3, 0.5, 1.0]), rng.choice([1.0, 1.5, 2.0]); dark = rng.choice([False, True])
        y = (n - 0.5 if dark else n) * lam * 1e-9 * D / (d * 1e-3) * 1000
        o, an = opts(rng, y, (2, 0.5, 1.5, 0.75))
        ordn = {1: 'first', 2: 'second', 3: 'third'}.get(n, f'{n}th')
        return dict(q=f'In YDSE (λ = {lam} nm, d = {d} mm, D = {D} m), the {ordn} {"dark" if dark else "bright"} fringe is at (in mm from the centre)', o=o, a=an,
                    sol=['Bright: y = \\f{nλD}{d}; dark: y = (n − ½)\\f{λD}{d}.', f'= {nf(y, 3)} mm.'], p=dict(t=t, n=n, lam=lam * 1e-9, d=d * 1e-3, D=D, dark=dark))
    if t == 'w_coin':
        l1, l2 = rng.choice([(400, 600), (450, 650), (480, 600), (500, 600), (500, 700), (450, 600), (550, 650), (400, 500), (420, 560), (600, 750)]); g = math.gcd(l1, l2); n = l2 // g
        which = rng.choice([1, 2]); val = n if which == 1 else l1 // g
        return dict(q=f'YDSE uses {l1} nm and {l2} nm together. The smallest order of the {l1 if which == 1 else l2} nm bright fringe that coincides with a bright fringe of the other is ____.', o=None, a=val,
                    sol=[f'n_{{1}} × {l1} = n_{{2}} × {l2}.', f'Smallest whole numbers: {l1 * n}/{l1} = {n}, {l1 * n}/{l2} = {l1 // g}.'], p=dict(t=t, l1=l1, l2=l2, which=which))
    if t == 'w_sheet':
        mu, n, lam = rng.choice([1.4, 1.5, 1.56, 1.6, 1.75]), rng.randint(1, 10), rng.choice([450, 500, 550, 600, 700]); tt = n * lam / (mu - 1)
        o, an = opts(rng, tt / 1000, (2, 0.5, 1.5, mu))
        return dict(q=f'A thin sheet (μ = {mu}) over one slit shifts the central fringe to where the {n}th bright fringe was (λ = {lam} nm). The sheet thickness (in μm) is', o=o, a=an, sol=['(μ − 1)t = nλ.', f't = {nf(tt / 1000, 3)} μm.'], p=dict(t=t, mu=mu, n=n, lam=lam))
    if t == 'w_int':
        num_, den = rng.choice([(1, 3), (1, 4), (1, 6), (1, 8), (1, 12), (3, 4), (2, 3), (5, 6), (7, 4), (5, 4)]); r = math.cos(pi * num_ / den) ** 2
        o, an = opts(rng, r, (2, 0.5, 1.5, 0.75)) if r > 1e-9 else (None, None); need(o)
        return dict(q=f'Two identical coherent waves meet with path difference {num_}λ/{den}. The intensity as a fraction of the maximum is', o=o, a=an, sol=['\\f{I}{I_{max}} = cos^{2}\\f{φ}{2}, φ = \\f{2π}{λ}Δx.', f'= {nf(r, 3)}.'], p=dict(t=t, a=num_, b=den))
    if t == 'w_maxmin':
        r1, r2 = rng.choice([(1, 4), (1, 9), (4, 9), (1, 16), (9, 16), (1, 25), (4, 25), (16, 25), (1, 2), (1, 3)]); kind = rng.choice(['I', 'w'])
        A1, A2 = (math.sqrt(r1), math.sqrt(r2)) if kind == 'I' else (r1, r2)
        R = (A1 + A2) ** 2 / (A2 - A1) ** 2
        o, an = opts(rng, R, (2, 0.5, 1.5, 0.75))
        return dict(q=(f'Two coherent beams have intensities in the ratio {r1} : {r2}. The ratio I_{{max}} : I_{{min}} of their interference pattern is' if kind == 'I' else
                       f'Two slits give waves whose amplitudes (field strengths) are in the ratio {r1} : {r2}. The ratio I_{{max}} : I_{{min}} is'), o=o, a=an,
                    sol=['\\f{I_{max}}{I_{min}} = \\f{(A_{1} + A_{2})^{2}}{(A_{1} − A_{2})^{2}}.', f'= {nf(R, 3)}.'], p=dict(t=t, A1=A1, A2=A2))
    if t == 'w_single':
        lam, a, f = rng.choice([400, 500, 600, 628, 700]), rng.choice([0.05, 0.1, 0.2, 0.5, 1.0]), rng.choice([0.5, 1.0, 1.5, 2.0]); W = 2 * lam * 1e-9 * f / (a * 1e-3) * 1000
        o, an = opts(rng, W, (2, 0.5, 1.5, 0.75))
        return dict(q=f'Light of {lam} nm falls on a slit of width {a} mm; the pattern is on a screen {f} m away. The width of the central maximum (in mm) is', o=o, a=an, sol=['W = \\f{2λD}{a}.', f'= {nf(W, 3)} mm.'], p=dict(t=t, lam=lam * 1e-9, a=a * 1e-3, D=f))
    if t == 'w_malus':
        angs = rng.choice([[0, 30], [0, 45], [0, 60], [0, 30, 60], [0, 45, 90], [0, 30, 90], [0, 60, 90], [30, 60, 90], [0, 22.5, 45]]); I = 0.5
        for a, b in zip(angs, angs[1:]): I *= math.cos(math.radians(b - a)) ** 2
        o, an = opts(rng, I, (2, 0.5, 1.5, 0.75))
        return dict(q=f'Unpolarised light of intensity I_{{0}} passes through polaroids whose axes are at {", ".join(f"{nf(a, 3)}°" for a in angs)} in turn. The emerging intensity is ____ × I_{{0}}. Choose the factor:', o=o, a=an,
                    sol=['First polaroid: ½; each next one: cos^{2} of the angle between successive axes (Malus).', f'Factor = {nf(I, 3)}.'], p=dict(t=t, angs=angs))
    if t == 'w_brew':
        n1, n2 = rng.choice([(1, math.sqrt(3)), (1, 1.5), (1, 1.6), (1, 4 / 3), (2, 2 * math.sqrt(3)), (1.5, 1.5 * math.sqrt(3)), (1, 1.73), (1, 2)]); ib = math.degrees(math.atan(n2 / n1)); r = 90 - ib
        ask = rng.choice(['i', 'r']); val = ib if ask == 'i' else r
        o, an = opts(rng, val, (1.2, 0.8, 1.5, 0.6))
        return dict(q=f'Light goes from n = {nf(n1, 3)} into n = {nf(n2, 3)}. At the angle that makes the reflected light completely polarised, the {"angle of incidence" if ask == "i" else "angle of refraction"} (in degrees) is', o=o, a=an,
                    sol=['Brewster: tan i = \\f{n_{2}}{n_{1}}; reflected ⟂ refracted.', f'i = {nf(ib, 3)}°, r = {nf(r, 3)}°.'], p=dict(t=t, n1=n1, n2=n2, ask=ask))
    if t == 'w_med':
        b, n = rng.choice([1.2, 2.4, 3.0, 4.0, 4.5, 6.0]), rng.choice([1.2, 1.25, 1.33, 1.5, 4 / 3, 1.6]); b2 = b / n
        o, an = opts(rng, b2, (n * n, 2, 0.5, 1.5))
        return dict(q=f'A YDSE gives fringe width {b} mm in air. With the whole apparatus immersed in a liquid of n = {nf(n, 3)}, the fringe width (in mm) becomes', o=o, a=an, sol=['λ → \\f{λ}{n}, so β → \\f{β}{n}.', f'= {nf(b2, 3)} mm.'], p=dict(t=t, b=b, n=n))
    lam, frac = rng.choice([400, 500, 600, 700]), rng.choice([0.5, 0.25, 0.75]); r = rng.choice([1, 2, 3, 4]) * 1e-3; D = rng.choice([1.0, 2.0])
    ph = 2 * math.acos(math.sqrt(frac)); y = ph / (2 * pi) * lam * 1e-9 * D / r * 1e6
    o, an = opts(rng, y, (2, 0.5, 1.5, 0.75))
    return dict(q=f'In YDSE (λ = {lam} nm, d = {nf(r * 1000, 2)} mm, D = {D} m) the nearest point to the centre where the intensity is {Fr(frac)} of the maximum is at (in μm)', o=o, a=an,
                sol=['cos^{2}\\f{φ}{2} = given fraction → φ; path difference \\f{φλ}{2π} = \\f{yd}{D}.', f'y = {nf(y, 3)} μm.'], p=dict(t='w_path', lam=lam * 1e-9, frac=frac, d=r, D=D))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(mirror=g_mirror, lens=g_lens, refr=g_refr, wave=g_wave).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = num(R) if isinstance(R, str) and t != 'm_img' else R
    if t == 'm_img':
        v = mirror_image(-p['u'], p['R']) * 100; side = 'in front of' if v < 0 else 'behind'
        return close(float(R.split(' cm ')[0]), abs(v)) and R.endswith(side + ' the mirror')
    if t == 'm_mag': return close(V, mirror_image(-p['u'], p['R']) / p['u'])
    if t == 'm_find':   # find the object distance that gives magnification m with this mirror (scan + bisection), then check the separation
        m, D, R = p['m'], p['D'], 2 * p['f']; g = lambda u: mirror_image(-u, R) / u - m
        us = [abs(R) * 10 * (k + 1) / 4000 for k in range(4000)]
        for a, b in zip(us, us[1:]):
            if R < 0 and (a <= abs(R) / 2 + 1e-12 <= b + 2e-12): continue   # skip the jump through the focus of a concave mirror
            if g(a) * g(b) <= 0:
                for _ in range(100):
                    c = (a + b) / 2
                    if g(a) * g(c) <= 0: b = c
                    else: a = c
                u = (a + b) / 2; v = mirror_image(-u, R); return close(abs(v + u), D, 1e-3) and close(V / 100, p['f'])
        return False
    if t == 'm_rod': return close(V, abs(mirror_image(-p['a'], p['R']) - mirror_image(-p['b'], p['R'])) * 100)
    if t == 'm_two':
        f, m = p['f'], p['m']; us = []
        for target in (-m, m):
            lo, hi = (f, 20 * f) if target < 0 else (1e-6, f)
            for _ in range(200):
                u = (lo + hi) / 2; mm = mirror_image(-u, -2 * f) / u
                if target < 0: (lo, hi) = (u, hi) if mm < target else (lo, u)
                else: (lo, hi) = (lo, u) if mm > target else (u, hi)
            us.append((lo + hi) / 2)
        return abs(V - abs(us[0] - us[1]) * 100) < 1e-4
    if t == 'l_img': return close(V, trace(-p['u'], thin(p['f'])) * 100)
    if t == 'l_maker': return close(V, focal([(0, p['R1'], 1, p['n']), (0, -p['R2'] if p['R2'] else None, p['n'], 1)]) * 100)
    if t == 'l_medium':
        R = 2 * (p['n'] - 1) * p['f']   # an equi-convex lens with this focal length in air
        return close(V, thin_f(R, -R, p['n'], p['nm']) * 100)
    if t == 'l_sep':
        ray = (-1.0, 1e-7, 0.0)
        for s in thin(p['f1']) + at(p['d'], thin(p['f2'])): ray = surf(*s, ray)
        return close(V, -ray[2] / 1e-7)
    if t == 'l_contact': return close(V, trace(-p['u'], thin(p['fc']) + thin(-p['fd'])) * 100)
    if t == 'l_micro':
        fo, fe, L = p['fo'], p['fe'], p['L']; lo, hi = fo * 1.0001, 10 * fo
        for _ in range(200):
            u = (lo + hi) / 2
            if trace(-u, thin(fo)) > L + fo: lo = u
            else: hi = u
        u = (lo + hi) / 2; return abs(V - trace(-u, thin(fo)) / u * 0.25 / fe) < 1e-3
    if t == 'l_res':   # first zero of the Airy-like pattern from a circular aperture: compare with the slit result × 1.22
        return close(V / 100, 1.22 * p['lam'] / p['th'])
    if t == 'l_silver':
        from op_pyq import self_image
        back = -p['R'] if p['kind'] == 'bi' else None
        return close(V / 100, self_image(p['R'], back, 1.0, p['n']), 3e-3)
    if t == 'l_real':
        m, D = p['m'], p['D']; lo, hi = 1e-3, D
        for _ in range(200):
            f = (lo + hi) / 2; a, b = f * 1.000001, 50 * f
            for _ in range(100):
                u = (a + b) / 2
                if trace(-u, thin(f)) / u > m: a = u
                else: b = u
            u = (a + b) / 2
            if u + trace(-u, thin(f)) > D: hi = f
            else: lo = f
        return close(V / 100, lo)
    if t == 'r_lam':   # frequency from medium 1, speed c/n in medium 2
        f = (3e8 / p['n1']) / (p['lam'] * 1e-9); return close(V * 1e-9, (3e8 / p['n2']) / f)
    if t == 'r_app':   # trace a near-vertical ray up from the coin through each layer (layers[0] is the bottom one)
        L = p['layers']; ang, x = 1e-6, 0.0
        for k, (h, n) in enumerate(L):
            x += h * math.tan(ang)
            ang = snell(n, L[k + 1][1] if k + 1 < len(L) else 1.0, ang)
        return close(V, x / math.tan(ang))
    if t == 'r_surf': return close(V, lens_image(-p['u'], [(0, p['R'], 1.0, p['n'])]) * 100)
    if t in ('r_prism', 'r_thin', 'r_nodev'):
        def dmin(A, n):
            A = math.radians(A); best = 1e9
            for k in range(1, 16000):
                i = k * 1e-4; r1 = snell(1, n, i); e = snell(n, 1, A - r1)
                if e is not None: best = min(best, i + e - A)
            return math.degrees(best)
        if t == 'r_prism': return close(V, dmin(p['A'], p['n']))
        if t == 'r_thin': return close(V, dmin(p['A'], p['n']), 0.02)
        return abs(dmin(p['A1'], p['n1']) - dmin(V, p['n2'])) < 0.02 * dmin(p['A1'], p['n1'])
    if t == 'r_crit':
        nA, nB = 1 / p['v1'], 1 / p['v2']; lo, hi = 0.0, pi / 2
        for _ in range(100):
            th = (lo + hi) / 2
            if snell(nA, nB, th) is None: hi = th
            else: lo = th
        return close(V, math.degrees(lo))
    if t == 'r_slab':
        i = math.radians(p['i']); r = snell(1, p['n'], i); x_out = p['h'] * math.tan(r); x_straight = p['h'] * math.tan(i)
        return close(V, (x_straight - x_out) * math.cos(i))
    if t == 'w_beta':
        lam, d, D = p['lam'], p['d'], p['D']; ys = []; y, step = 0.0, lam * D / d / 400; prev = 4.0
        while len(ys) < 2:
            y += step; cur = yd(d * y / D, lam); nxt = yd(d * (y + step) / D, lam)
            if cur >= prev and cur >= nxt: ys.append(y)
            prev = cur
        return close(V / 1000, ys[1] - ys[0], 0.02)
    if t == 'w_pos':
        lam, d, D = p['lam'], p['d'], p['D']; y = V / 1000; I = yd(d * y / D, lam)
        k = (p['n'] - 0.5) if p['dark'] else p['n']   # path difference in wavelengths at that point
        exact = k * lam * D / d; return close(y, exact) and (yd(d * exact / D, lam) < 1e-9 if p['dark'] else yd(d * exact / D, lam) > 4 - 1e-9)
    if t == 'w_coin':
        l1, l2 = p['l1'], p['l2']
        for n1 in range(1, 200):
            for n2 in range(1, 200):
                if n1 * l1 == n2 * l2: return V == (n1 if p['which'] == 1 else n2)
    if t == 'w_sheet': return close(V * 1000 * (p['mu'] - 1), p['n'] * p['lam'])
    if t == 'w_int': return close(V, yd(p['a'] / p['b'], 1.0) / 4)
    if t == 'w_maxmin': I = [yd(k / 360, 1, p['A1'] ** 2, p['A2'] ** 2) for k in range(361)]; return close(V, max(I) / min(I))
    if t == 'w_single':
        z = first_zero(p['a'], p['lam']); return close(V / 1000, 2 * p['D'] * math.tan(z), 0.02)
    if t == 'w_malus':
        n = 3600; I = sum(math.cos(2 * pi * k / n) ** 2 for k in range(n)) / n   # average over random input polarisation
        for a, b in zip(p['angs'], p['angs'][1:]): I *= math.cos(math.radians(b - a)) ** 2
        return close(V, I)
    if t == 'w_brew':   # angle where i + r = 90° by scanning Snell
        best = min(range(1, 9000), key=lambda k: abs(math.radians(k / 100) + snell(p['n1'], p['n2'], math.radians(k / 100)) - pi / 2))
        i = best / 100; r = math.degrees(snell(p['n1'], p['n2'], math.radians(i))); return close(V, i if p['ask'] == 'i' else r, 2e-3)
    if t == 'w_med': return close(V, p['b'] / p['n'])
    if t == 'w_path':
        lam, d, D = p['lam'], p['d'], p['D']; lo, hi = 0.0, lam * D / (2 * d)
        for _ in range(100):
            y = (lo + hi) / 2
            if yd(d * y / D, lam) / 4 > p['frac']: lo = y
            else: hi = y
        return close(V / 1e6, lo)
    raise KeyError(t)
