"""Practice generators — Physics Unit 11: Electrostatics. Each item carries its parameters in p; check() re-solves it a
different way: point-charge field/potential sums, numerical integration (arcs, rings, cube solid angles, line integrals,
motion), bisection, the exact circuit solver, or energy bookkeeping with explicit SI numbers."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr, solve_dc
K9, E0 = 9e9, 8.85e-12
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')

def U(v, unit, s=3): return f'{nf(v, s)} {unit}'.strip()
def dists(v, fs, unit='', s=3): return [U(v * f, unit, s) for f in fs]
def need(c):
    if not c: raise AssertionError('retry')
def whole(x):
    need(abs(x - round(x)) < 1e-9 and 0 < abs(round(x)) < 100000); return int(round(x))

# ---------- independent tools ----------
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def efield(qs, p):
    E = [0.0, 0.0, 0.0]
    for q, *r in qs:
        d = [p[i] - r[i] for i in range(3)]; s = math.sqrt(sum(x * x for x in d)) ** 3
        for i in range(3): E[i] += K9 * q * d[i] / s
    return E
def epot(qs, p): return sum(K9 * q / math.dist(r, p) for q, *r in qs)
def mag(v): return math.sqrt(sum(x * x for x in v))
def bis(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
def cube_frac(pt, n=48):
    """fraction of a point charge's flux through the unit cube [0,1]^3 (charge at pt on/inside the cube), by
    integrating E·dA over the six faces numerically."""
    tot = 0.0; h = 1 / n; g = [(i + .5) * h for i in range(n)]
    for ax in range(3):
        for side in (0, 1):
            if abs(pt[ax] - side) < 1e-12: continue
            sg = 1 if side == 1 else -1
            for u in g:
                for v in g:
                    r = [0, 0, 0]; o = [a for a in range(3) if a != ax]; r[ax] = side; r[o[0]] = u; r[o[1]] = v
                    d = [r[i] - pt[i] for i in range(3)]; s = math.sqrt(sum(x * x for x in d)) ** 3
                    tot += sg * d[ax] / s * h * h
    return tot / (4 * math.pi)

# =============================== Coulomb / superposition ===============================
def g_coul(rng):
    t = rng.choice(['force', 'null', 'nullout', 'share', 'hang', 'poly', 'arc', 'ring'])
    if t == 'force':
        q1, q2 = rng.choice([1, 2, 3, 4, 5, 6, 8, 10]), rng.choice([1, 2, 3, 4, 5, 6, 8, 10]); r = rng.choice([3, 5, 6, 10, 12, 15, 20, 30, 50])
        Fv = K9 * q1 * q2 * 1e-12 / (r / 100) ** 2
        q = f'Two point charges {q1} μC and {q2} μC are {r} cm apart in air. The force between them is :'
        o, a = mcq(rng, U(Fv, 'N'), dists(Fv, (100 / r, 2, 0.5, r / 100, 10), 'N'))
        return dict(q=q, o=o, a=a, sol=['F = \\f{kq_{1}q_{2}}{r^{2}}.', f'= \\f{{9 × 10^{{9}} × {q1} × 10^{{−6}} × {q2} × 10^{{−6}}}}{{({nf(r / 100)})^{{2}}}} ≈ {U(Fv, "N")}.'], p=dict(t=t, q1=q1, q2=q2, r=r))
    if t in ('null', 'nullout'):
        n = rng.choice([2, 3, 4, 5, 6]); d = rng.choice([6, 9, 12, 15, 18, 20, 24, 30, 36, 40, 60])
        if t == 'null':
            x = F(d, 1 + n); q = f'Charges +q and +{n * n}q are fixed {d} cm apart. The electric field is zero at a point between them, ______ cm from +q.'
            sol = ['Like charges: the null point is between them, nearer the smaller one.', f'\\f{{q}}{{x^{{2}}}} = \\f{{{n * n}q}}{{({d} − x)^{{2}}}} → {d} − x = {n}x → x = {fr(x)} cm.']
        else:
            x = F(d, n - 1); q = f'Charges +q and −{n * n}q are fixed {d} cm apart. The electric field is zero at a point on the line, outside them on the side of +q, ______ cm from +q.'
            sol = ['Unlike charges: the null point is outside, beyond the smaller charge.', f'\\f{{q}}{{x^{{2}}}} = \\f{{{n * n}q}}{{(x + {d})^{{2}}}} → x + {d} = {n}x → x = {fr(x)} cm.']
        if x.denominator == 1: return dict(q=q, o=None, a=int(x), sol=sol, p=dict(t=t, n=n, d=d))
        o, a = mcq(rng, nf(float(x), 3), [nf(float(x) * f, 3) for f in (n, 1 / n, 2, 0.5, (n + 1) / n)])
        return dict(q=q.replace('______ cm', 'at a distance (cm)'), o=o, a=a, sol=sol, p=dict(t=t, n=n, d=d))
    if t == 'share':
        a0, b0 = rng.choice([(1, 1), (2, 1), (3, 1), (1, 3), (2, 2), (4, 2), (3, 5), (5, 1)]); F0 = rng.choice([8, 12, 16, 24, 32, 40, 48, 64, 80, 96])
        pa = F(a0, 2); pb = (b0 + pa) / 2; Fn = F0 * pa * pb / (a0 * b0)
        need(Fn.denominator == 1)
        q = f'Identical small conducting spheres P and S carry charges {a0}Q and {b0}Q and repel with force {F0} N. A third identical uncharged sphere R touches P, then S, and is removed. The new force between P and S is ______ N.'
        return dict(q=q, o=None, a=int(Fn), sol=['Identical spheres share charge equally.', f'P: {a0}Q → {fr(pa)}Q. R leaves with {fr(pa)}Q; S: ({b0} + {fr(pa)})Q ÷ 2 = {fr(pb)}Q.', f'F ∝ product: {F0} × \\f{{{fr(pa)} × {fr(pb)}}}{{{a0 * b0}}} = {Fn} N.'], p=dict(t=t, a0=a0, b0=b0, F0=F0))
    if t == 'hang':
        m = rng.choice([1, 2, 3, 4, 5, 10]); th = rng.choice([30, 45, 60]); E = rng.choice([1, 2, 5, 10]) * 10 ** rng.choice([3, 4, 5])
        qv = m * 1e-3 * 10 * math.tan(math.radians(th)) / E
        q = f'A small ball of mass {m} g hangs from a silk thread in a uniform horizontal field of {nf(E)} N/C. In equilibrium the thread makes {th}° with the vertical (g = 10 m s^{{−2}}). The charge on the ball is :'
        o, a = mcq(rng, U(qv, 'C'), dists(qv, (1 / math.tan(math.radians(th)) ** 2 if th != 45 else 2, 0.5, 10, math.cos(math.radians(th)), 3), 'C'))
        return dict(q=q, o=o, a=a, sol=['Three forces balance: tan θ = \\f{qE}{mg}.', f'q = \\f{{{m} × 10^{{−3}} × 10 × tan {th}°}}{{{nf(E)}}} ≈ {U(qv, "C")}.'], p=dict(t=t, m=m, th=th, E=E))
    if t == 'poly':
        n = rng.choice([3, 4, 5, 6, 8]); mode = rng.choice(['remove', 'flip', 'double'])
        f = {'remove': 1, 'flip': 2, 'double': 1}[mode]
        what = {'remove': 'one charge is removed', 'flip': 'one charge is replaced by −Q', 'double': 'one charge is replaced by 2Q'}[mode]
        q = f'Equal charges Q sit at the corners of a regular {n}-sided polygon whose corners are a distance R from its centre. If {what}, the field at the centre is ______ × \\f{{Q}}{{4πε_{{0}}R^{{2}}}}.'
        return dict(q=q, o=None, a=f, sol=['With all equal charges the field at the centre is zero by symmetry.', f'The change acts like adding a single charge of {"−Q" if mode == "remove" else "−2Q" if mode == "flip" else "+Q"} at that corner → {f} × \\f{{Q}}{{4πε_{{0}}R^{{2}}}}.'], p=dict(t=t, n=n, mode=mode))
    if t == 'arc':
        a1, a2 = rng.choice([(90, 180), (90, 270), (180, 90), (60, 180), (120, 60), (60, 300), (180, 270), (60, 120), (270, 90), (120, 240)])
        r = math.sin(math.radians(a2) / 2) / math.sin(math.radians(a1) / 2)
        q = f'A uniformly charged ring (same charge per length everywhere). The field at the centre due to an arc subtending {a1}° is E. The field at the centre due to an arc of the same ring subtending {a2}° is :'
        o, a = mcq(rng, f'{nf(r, 3)}E', [f'{nf(x, 3)}E' for x in (a2 / a1, math.sqrt(a2 / a1), r * 2 if r else 1.5, 1.0 if abs(r - 1) > .01 else 0.5, (a2 / a1) ** 2)])
        return dict(q=q, o=o, a=a, sol=['An arc of angle α gives E ∝ 2 sin(α/2), along its bisector.', f'Ratio = \\f{{sin {a2 // 2}°}}{{sin {a1 // 2}°}} ≈ {nf(r, 3)}.'], p=dict(t=t, a1=a1, a2=a2))
    R = rng.choice([1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 20]); mode = rng.choice(['max', 'ratio'])
    if mode == 'max':
        q = f'A ring of radius {R}√{{2}} cm lies in the xy-plane with centre at the origin and carries uniform charge. The field on the z-axis is largest at z = ______ cm.'
        return dict(q=q, o=None, a=R, sol=['E_{axis} ∝ \\f{z}{(z^{2} + a^{2})^{3/2}}; maximum at z = \\f{a}{√{2}}.', f'= \\f{{{R}√{{2}}}}{{√{{2}}}} = {R} cm.'], p=dict(t='rmax', R=R))
    z = rng.choice([F(3, 4), F(4, 3), 1, F(1, 2), 2]); v = z / (1 + z * z) ** F(3, 2) if False else float(z) / (1 + float(z) ** 2) ** 1.5
    q = f'A ring of radius a carries charge Q. On its axis at distance {fr(z)}a from the centre the field is ______ × \\f{{kQ}}{{a^{{2}}}}.'
    o, a = mcq(rng, nf(v, 3), [nf(v * f, 3) for f in (2, 0.5, 1 + float(z), 1 / (1 + float(z) ** 2) ** -0.5, 3)])
    return dict(q=q, o=o, a=a, sol=['E = \\f{kQz}{(z^{2} + a^{2})^{3/2}}.', f'z = {fr(z)}a → {nf(v, 3)} \\f{{kQ}}{{a^{{2}}}}.'], p=dict(t='rz', z=float(z)))

# =============================== dipoles ===============================
def g_dip(rng):
    t = rng.choice(['axeq', 'torque', 'work', 'perp', 'sheet', 'vec'])
    if t == 'axeq':
        m = rng.choice([F(1, 2), 1, 2, 3, 4, 5, F(1, 4), F(3, 2)]); where = rng.choice(['ae', 'ea', 'aa'])
        if where == 'ae': v = 2 * m ** 3; txt = f'at an axial point distance r is E. At a point on the equatorial line at distance {fr(m)}r it is \\f{{E}}{{x}}'
        elif where == 'ea': v = F(m) ** 3 / 2; txt = f'at an equatorial point distance r is E. At a point on the axis at distance {fr(m)}r it is \\f{{E}}{{x}}'
        else: v = F(m) ** 3; txt = f'at an axial point distance r is E. At another axial point at distance {fr(m)}r it is \\f{{E}}{{x}}'
        need(v.denominator == 1 and v != 1); v = int(v)
        q = f'The field of a short electric dipole {txt}. The value of x is ______.'
        return dict(q=q, o=None, a=v, sol=['Short dipole: E_{axial} = \\f{2kp}{r^{3}}, E_{equatorial} = \\f{kp}{r^{3}}.', f'x = {v}.'], p=dict(t=t, m=str(m), w=where))
    if t == 'torque':
        qq = rng.choice([1, 2, 3, 4, 5]); d = rng.choice([1, 2, 5, 10]); E = rng.choice([1, 2, 5]) * 10 ** rng.choice([3, 4, 5]); th = rng.choice([30, 45, 60, 90])
        tau = qq * 1e-6 * d * 1e-2 * E * math.sin(math.radians(th))
        q = f'An electric dipole of charges ±{qq} μC separated by {d} cm is placed in a uniform field of {nf(E)} N/C with its axis at {th}° to the field. The torque on it is :'
        o, a = mcq(rng, U(tau, 'N m'), dists(tau, (2, 0.5, 10, 0.1, 1 / math.sin(math.radians(th)) if th != 90 else 3), 'N m'))
        return dict(q=q, o=o, a=a, sol=[f'p = {qq} × 10^{{−6}} × {nf(d / 100)} = {nf(qq * d * 1e-8)} C m.', f'τ = pE sin {th}° ≈ {U(tau, "N m")}.'], p=dict(t=t, qq=qq, d=d, E=E, th=th))
    if t == 'work':
        pv = rng.choice([1, 2, 3, 4, 5, 6, 8]) * 10 ** rng.choice([-6, -7, -8]); E = rng.choice([1, 2, 5]) * 10 ** rng.choice([3, 4, 5, 6]); t1, t2 = rng.choice([(0, 180), (0, 90), (0, 60), (60, 180), (90, 180), (0, 120), (30, 90), (60, 120)])
        W = pv * E * (math.cos(math.radians(t1)) - math.cos(math.radians(t2)))
        q = f'A dipole of moment {nf(pv)} C m is in a uniform field of {nf(E)} N/C. Work needed to turn it from {t1}° to {t2}° with the field is :'
        o, a = mcq(rng, U(W, 'J'), dists(W, (2, 0.5, 1.5, 3, 0.25), 'J'))
        return dict(q=q, o=o, a=a, sol=['W = U_{2} − U_{1} with U = −pE cos θ → W = pE(cos θ_{1} − cos θ_{2}).', f'≈ {U(W, "J")}.'], p=dict(t=t, pv=pv, E=E, t1=t1, t2=t2))
    if t == 'perp':
        ang = rng.choice([30, 45, 60]); where = rng.choice(['axA', 'eqA'])
        r = 2 * math.tan(math.radians(ang)) if where == 'axA' else 1 / (2 * math.tan(math.radians(ang)))
        lab = 'the axis of A' if where == 'axA' else 'the equatorial line of A (and the axis of B)'
        q = f'Two short dipoles A (moment p_{{1}}) and B (moment p_{{2}}) sit at the same point O with axes perpendicular. At a point x on {lab}, the resultant field makes {ang}° with Ox. p_{{2}}/p_{{1}} is :'
        o, a = mcq(rng, nf(r, 3), [nf(r * f, 3) for f in (0.25, 4, 0.5, 2, 3)])
        return dict(q=q, o=o, a=a, sol=['On a dipole\'s axis E = \\f{2kp}{r^{3}}; on its equator E = \\f{kp}{r^{3}}; the two fields are perpendicular.', f'tan {ang}° = (field across Ox)/(field along Ox) → \\f{{p_{{2}}}}{{p_{{1}}}} ≈ {nf(r, 3)}.'], p=dict(t=t, ang=ang, w=where))
    if t == 'sheet':
        qq = rng.choice([1, 2, 3, 4, 5]); L = rng.choice([5, 10, 20, 25]); sg = rng.choice([10, 20, 50, 100]); th = rng.choice([30, 60, 90])
        tau = qq * 1e-6 * L * 1e-2 * sg * 1e-6 / (2 * E0) * math.sin(math.radians(th))
        q = f'Charges ±{qq} μC are fixed to the ends of a light rod {L} cm long, placed near an infinite sheet of charge density {sg} μC/m^{{2}} with the rod at {th}° to the sheet\'s field (ε_{{0}} = 8.85 × 10^{{−12}}). The torque on the rod is :'
        o, a = mcq(rng, U(tau, 'N m'), dists(tau, (2, 0.5, 10, 4, 0.1), 'N m'))
        return dict(q=q, o=o, a=a, sol=['A sheet gives a uniform field \\f{σ}{2ε_{0}}.', f'τ = pE sin θ = {qq} × 10^{{−6}} × {nf(L / 100)} × \\f{{{sg} × 10^{{−6}}}}{{2ε_{{0}}}} × sin {th}° ≈ {U(tau, "N m")}.'], p=dict(t=t, qq=qq, L=L, sg=sg, th=th))
    d = rng.choice([(1, -1, 1), (1, 1, 0), (2, 1, 2), (1, 2, 2), (0, 1, 1), (1, 0, 1)]); qq = rng.choice([1, 2, 4, 5]); Ex = rng.choice([10, 20, 50, 100])
    tq = [0, qq * 1e-6 * d[2] * Ex, -qq * 1e-6 * d[1] * Ex]; v = mag(tq)
    q = f'Charges −{qq} μC at the origin and +{qq} μC at ({d[0]}, {d[1]}, {d[2]}) m form a dipole in a field \\vec{{E}} = {Ex} î V/m. The magnitude of the torque is :'
    o, a = mcq(rng, U(v, 'N m'), dists(v, (2, 0.5, math.sqrt(2) if abs(v - v * math.sqrt(2)) else 3, 1.5, 3), 'N m'))
    return dict(q=q, o=o, a=a, sol=[f'\\vec{{p}} = {qq} × 10^{{−6}}({d[0]}î + {d[1]}ĵ + {d[2]}k̂) C m.', f'|\\vec{{p}} × \\vec{{E}}| = {qq} × 10^{{−6}} × {Ex} × √{{{d[1] ** 2 + d[2] ** 2}}} ≈ {U(v, "N m")}.'], p=dict(t=t, d=d, qq=qq, Ex=Ex))

# =============================== flux / Gauss ===============================
def g_gauss(rng):
    t = rng.choice(['encl', 'cube', 'flat', 'sheets', 'xfield', 'diag', 'qphi', 'linesheet', 'sphere2'])
    if t == 'encl':
        ins = [rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7]) for _ in range(rng.choice([2, 3, 4]))]; outs = [rng.choice([-4, -3, -2, 2, 3, 5]) for _ in range(rng.choice([1, 2]))]
        s = sum(ins); need(s != 0 and s != sum(ins + outs))
        lab = lambda xs: ', '.join(f'{x:+d}q'.replace('+1q', '+q').replace('-1q', '−q').replace('-', '−') for x in xs)
        q = f'Charges {lab(ins)} are inside a closed surface S and {lab(outs)} outside it. The flux through S is :'
        o, a = mcq(rng, f'{s}q/ε_{{0}}'.replace('-', '−'), [f'{x}q/ε_{{0}}'.replace('-', '−') for x in (sum(ins + outs), -s, sum(map(abs, ins)), s + 1, 2 * s)])
        return dict(q=q, o=o, a=a, sol=['Gauss: Φ = \\f{q_{inside}}{ε_{0}}; outside charges add nothing.', f'Inside total = {s}q.'.replace('-', '−')], p=dict(t=t, ins=ins))
    if t == 'cube':
        where = rng.choice(['centre', 'face', 'edge', 'corner']); qn = rng.choice([1, 2, 3, 4, 6, 8, 12, 16, 24])
        f = dict(centre=1, face=F(1, 2), edge=F(1, 4), corner=F(1, 8))[where]
        txt = dict(centre='at the centre of', face='at the centre of one face of', edge='at the midpoint of one edge of', corner='at one corner of')[where]
        v = qn * f
        q = f'A point charge {qn}q is placed {txt} a cube. The flux through the cube is k\\f{{q}}{{ε_{{0}}}}. k = ______'
        if F(v).denominator == 1: return dict(q=q, o=None, a=int(v), sol=['Imagine the identical cubes that would surround the charge symmetrically.', f'{dict(centre="1", face="2", edge="4", corner="8")[where]} cubes share it → {qn} × {fr(f)} = {fr(v)}.'], p=dict(t=t, w=where, qn=qn))
        o, a = mcq(rng, fr(v), [fr(x) for x in (qn, qn * F(1, 2), qn * F(1, 4), qn * F(1, 8), qn * F(1, 6), 0)])
        return dict(q=q.replace('______', '?'), o=o, a=a, sol=['Imagine the identical cubes that would surround the charge symmetrically.', f'{dict(centre="1", face="2", edge="4", corner="8")[where]} cubes share it → {fr(v)}.'], p=dict(t=t, w=where, qn=qn))
    if t == 'flat':
        E = [rng.choice([1, 2, 3, 4, 5, 6, 8]) for _ in range(3)]; ax = rng.choice([0, 1, 2]); A = rng.choice([2, 3, 4, 5, 10, 20, 30])
        v = E[ax] * A; pl = ['YZ', 'XZ', 'XY'][ax]
        q = f'A field \\vec{{E}} = ({E[0]}î + {E[1]}ĵ + {E[2]}k̂) N/C passes through a flat area of {A} m^{{2}} lying in the {pl}-plane. The magnitude of the flux is ______ N m^{{2}}/C.'
        return dict(q=q, o=None, a=v, sol=[f'A surface in the {pl}-plane has its normal along {"îĵk̂"[ax]}.', f'Φ = {E[ax]} × {A} = {v}.'], p=dict(t=t, E=E, ax=ax, A=A))
    if t == 'sheets':
        n = rng.choice([2, 3]); xs = list(range(n)); ss = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in xs]; reg = rng.choice(range(n + 1))
        Ev = sum(F(s, 2) * (1 if reg > i else -1) for i, s in enumerate(ss))
        need(Ev != 0)
        names = ', '.join(f'{s}σ'.replace('-', '−').replace('1σ', 'σ') for s in ss)
        rtxt = 'to the left of all of them' if reg == 0 else 'to the right of all of them' if reg == n else f'between sheet {reg} and sheet {reg + 1}'
        q = f'Parallel infinite sheets, left to right, carry charge densities {names}. The field magnitude at a point {rtxt} is k\\f{{σ}}{{ε_{{0}}}}. k = ______'
        av = abs(Ev)
        if av.denominator == 1: return dict(q=q, o=None, a=int(av), sol=['Each sheet gives \\f{σ}{2ε_{0}}, away from + and toward −; add with signs.', f'|E| = {fr(av)} \\f{{σ}}{{ε_{{0}}}}.'], p=dict(t=t, ss=ss, reg=reg))
        o, a = mcq(rng, fr(av), [fr(x) for x in (av * 2, av + 1, abs(av - F(1, 2)) or F(5, 2), av / 2, av + F(1, 2))])
        return dict(q=q.replace('______', '?'), o=o, a=a, sol=['Each sheet gives \\f{σ}{2ε_{0}}, away from + and toward −; add with signs.', f'|E| = {fr(av)} \\f{{σ}}{{ε_{{0}}}}.'], p=dict(t=t, ss=ss, reg=reg))
    if t == 'xfield':
        c = rng.choice([1, 2, 3, 4, 5]); x0 = rng.choice([0, 1, 2, 3, 4]); s = rng.choice([1, 2, 3])
        v = c * s * s * s
        q = f'A field \\vec{{E}} = {c}x î N/C (x in m) exists in space. A cube of side {s} m has its faces perpendicular to x at x = {x0} m and x = {x0 + s} m. The flux through the cube is ______ N m^{{2}}/C.'
        return dict(q=q, o=None, a=v, sol=['Only the two x-faces matter.', f'Φ = {c}({x0 + s} − {x0}) × {s * s} = {v}.'], p=dict(t=t, c=c, x0=x0, s=s))
    if t == 'diag':
        lam = rng.choice([1, 2, 3, 4, 5, 6, 8]); sd = rng.choice([1, 2, 3, 4, 5, 6]); how = rng.choice(['body', 'edge'])
        L = 3 * sd if how == 'body' else sd
        side = f'{sd}√{{3}} cm' if how == 'body' else f'{sd} cm'
        phi = lam * 1e-9 * L * 1e-2 * 4 * math.pi * K9
        what = 'two opposite corners (a body diagonal)' if how == 'body' else 'the centre of the cube, parallel to an edge'
        q = f'An infinitely long wire with λ = {lam} nC/m passes through a cube of side {side} along {what}. The net flux through the cube is :'
        o, a = mcq(rng, U(phi, 'N m^{2}/C'), dists(phi, (2, 0.5, math.sqrt(3), 1 / 3, 3), 'N m^{2}/C'))
        return dict(q=q, o=o, a=a, sol=['Only the length of wire inside counts: Φ = \\f{λL}{ε_{0}}.', f'L = {L} cm → Φ = λL × 4π × 9 × 10^{{9}} ≈ {U(phi, "N m^{2}/C")}.'], p=dict(t=t, lam=lam, L=L))
    if t == 'qphi':
        ph = rng.choice([1, 2, 3, 4, 5, 6, 9]) * 10 ** rng.choice([3, 4, 5]) * rng.choice([1, -1]); r = rng.choice([2, 5, 8, 10, 20])
        qv = ph * E0
        q = f'A point charge sends a flux of {nf(ph)} N m^{{2}} C^{{−1}} through a sphere of radius {r} cm centred on it (ε_{{0}} = 8.85 × 10^{{−12}}). The charge is :'.replace('-', '−')
        o, a = mcq(rng, U(qv, 'C'), [U(x, 'C') for x in (-qv, qv * 4 * math.pi, qv * (r / 100) ** 2 * 100, qv * 10)])
        return dict(q=q, o=o, a=a, sol=['q = ε_{0}Φ — the radius does not matter.', f'= 8.85 × 10^{{−12}} × {nf(ph)} ≈ {U(qv, "C")}.'.replace('-', '−')], p=dict(t=t, ph=ph))
    if t == 'linesheet':
        r = rng.choice([1, 2, 3, 4, 5]); m = rng.choice([1, 2, 3, 4])   # σ = m λ, line at distance r
        val = (2 * math.pi * m * r) ** 2 / math.pi ** 2 / 4
        need(abs(val - round(val)) < 1e-9)
        q = f'A sheet of charge density σ lies in the xy-plane and a line charge λ, parallel to the y-axis, passes {r} m from the point P above the sheet. If |σ| = {m}|λ| (SI), the ratio of the sheet\'s field to the line\'s field at P is π√{{n}} : 1. n = ______'
        return dict(q=q, o=None, a=round(val), sol=['Sheet: \\f{σ}{2ε_{0}}; line: \\f{λ}{2πε_{0}r}.', f'Ratio = \\f{{πrσ}}{{λ}} = {m * r}π → n = {round(val)}.'], p=dict(t=t, r=r, m=m))
    a_ = rng.choice([1, 2, 3, 4]); q1, x1, q2, x2 = rng.choice([1, 2, 3, 4, 5, 6, 8]), rng.choice([1, 2]), rng.choice([-1, -2, -3, -4, 2, 3]), rng.choice([3, 4, 5])
    R1, R2 = rng.choice([(F(5, 2), 6), (F(3, 2), 6), (F(5, 2), F(11, 2)), (3, 6)])
    need(x1 < R1 < x2 < R2)
    s1, s2 = q1, q1 + q2; need(s2 != 0 and s1 != s2)
    rt = F(s1, s2)
    q = f'Charges {q1} μC at x = {x1} cm and {q2} μC at x = {x2} cm lie on the x-axis. The ratio of flux through spheres of radii {fr(R1)} cm and {fr(R2)} cm centred at the origin is :'.replace('-', '−')
    need(rt > 0); o, a = mcq(rng, f'{rt.numerator} : {rt.denominator}', [f'{x.numerator} : {x.denominator}' for x in (F(s2, s1), F(abs(q2), q1), F(q1, abs(q1) + abs(q2)), F(q1 + 1, s2 + 1), F(q1, q1 + abs(q2) + 1)) if x > 0])
    return dict(q=q, o=o, a=a, sol=['Each sphere counts only the charge inside it.', f'Small: {q1} μC; large: {s2} μC → ratio {q1} : {s2}.'.replace('-', '−')], p=dict(t='sphere2', q1=q1, x1=x1, q2=q2, x2=x2, R1=float(R1), R2=float(R2)))

# =============================== potential & energy ===============================
QUAD = [((1, 2, 2), 3), ((2, 3, 6), 7), ((2, 4, 4), 6), ((1, 4, 8), 9), ((4, 4, 7), 9), ((2, 6, 9), 11), ((6, 6, 7), 11), ((3, 4, 12), 13), ((2, 10, 11), 15), ((4, 8, 8), 12), ((2, 2, 1), 3), ((3, 6, 6), 9)]
def g_pot(rng):
    t = rng.choice(['shell', 'move', 'pair', 'nuc', 'grad', 'swing', 'tri', 'approach'])
    if t == 'shell':
        R = rng.choice([5, 10, 20, 25, 30]); V0 = rng.choice([60, 90, 120, 150, 180, 240, 300]); r = rng.choice([F(1, 2), F(3, 2), 2, 3, F(5, 4), 4, F(6, 5)]) * R
        v = V0 if r <= R else V0 * F(R) / r
        q = f'A uniformly charged spherical shell of radius {R} cm has potential {V0} V on its surface. The potential at {fr(r)} cm from its centre is ______ V.'
        if F(v).denominator == 1: return dict(q=q, o=None, a=int(v), sol=['Inside: same as the surface. Outside: V ∝ \\f{1}{r}.', f'V = {fr(v)} V.'], p=dict(t=t, R=R, V0=V0, r=float(r)))
        o, a = mcq(rng, nf(float(v), 3) + ' V', [nf(float(x), 3) + ' V' for x in (V0, v * 2, V0 * (F(R) / r) ** 2, 0, v / 2)])
        return dict(q=q.replace('______ V', ''), o=o, a=a, sol=['Outside: V ∝ \\f{1}{r}.', f'V = {V0} × \\f{{{R}}}{{{fr(r)}}} ≈ {nf(float(v), 3)} V.'], p=dict(t=t, R=R, V0=V0, r=float(r)))
    if t == 'move':
        (A, ra), (B, rb) = rng.sample(QUAD, 2); Q = rng.choice([1, 2, 3, 4, 5]) * 1e-8; qq = rng.choice([1, 2, 3, 4, 5])
        W = qq * 1e-6 * K9 * Q * (1 / rb - 1 / ra)
        q = f'A charge {nf(Q)} C sits at the origin. Work done in moving {qq} μC from A{A} m to B{B} m (k = 9 × 10^{{9}}) is :'
        o, a = mcq(rng, U(W, 'J'), [U(x, 'J') for x in (-W, W * 2, qq * 1e-6 * K9 * Q * (1 / rb ** 2 - 1 / ra ** 2), W * 3, qq * 1e-6 * K9 * Q / rb)])
        return dict(q=q.replace('-', '−'), o=o, a=a, sol=[f'OA = {ra} m, OB = {rb} m.', f'W = q(V_{{B}} − V_{{A}}) = {qq} × 10^{{−6}} × 9 × 10^{{9}} × {nf(Q)} × (\\f{{1}}{{{rb}}} − \\f{{1}}{{{ra}}}) ≈ {U(W, "J")}.'.replace('-', '−')], p=dict(t=t, A=A, B=B, Q=Q, qq=qq))
    if t == 'pair':
        q1, q2 = rng.choice([1, 2, 3, 4, 5, 6, 7, 8]), rng.choice([-1, -2, -3, -4, -5, 2, 3, 4]); r = rng.choice([2, 3, 5, 6, 10, 12, 14, 20, 30])
        Uv = K9 * q1 * q2 * 1e-12 / (r / 100)
        q = f'Point charges {q1} μC and {q2} μC are {r} cm apart. The electrostatic potential energy of the pair is :'.replace('-', '−')
        o, a = mcq(rng, U(Uv, 'J'), [U(x, 'J') for x in (-Uv, Uv * 100 / r, Uv * 2, Uv / 2, Uv * 10)])
        return dict(q=q, o=o, a=a, sol=['U = \\f{kq_{1}q_{2}}{r} (the sign matters).', f'≈ {U(Uv, "J")}.'.replace('-', '−')], p=dict(t=t, q1=q1, q2=q2, r=r))
    if t == 'nuc':
        Z = rng.choice([10, 20, 25, 40, 50, 75, 80, 90, 100]); R = rng.choice([3, 4, 5, 6, 8, 9, 10, 12, 15])
        v = K9 * Z * 1.6e-19 / (R * 1e-15) / 1e6
        need(abs(v - round(v)) < 1e-6)
        q = f'The potential at the surface of a nucleus (Z = {Z}) of radius {R} × 10^{{−15}} m is ______ × 10^{{6}} V. (e = 1.6 × 10^{{−19}} C)'
        return dict(q=q, o=None, a=round(v), sol=['V = \\f{kZe}{R}.', f'= \\f{{9 × 10^{{9}} × {Z} × 1.6 × 10^{{−19}}}}{{{R} × 10^{{−15}}}} = {round(v)} × 10^{{6}} V.'], p=dict(t=t, Z=Z, R=R))
    if t == 'grad':
        A, B = rng.choice([2, 4, 6, 10, 20]), rng.choice([2, 4, 5, 10]); x, y = rng.choice([1, 2, 3, 4, 5, 10]), rng.choice([1, 2, 4, 5, 10, 20]); V1 = rng.choice([0, 100, 200, 500, 1000])
        v = V1 + A * x * x / 2 + B * y * y / 2
        q = f'\\vec{{E}} = {A}x î + {B}y ĵ (V/m, x and y in m). If the potential at ({x}, {y}) is {V1} V, the potential at the origin is ______ V.'
        return dict(q=q, o=None, a=whole(v), sol=['V(0) − V(P) = ∫_{0}^{P} \\vec{E}·d\\vec{r}.', f'= \\f{{{A}·{x}^{{2}}}}{{2}} + \\f{{{B}·{y}^{{2}}}}{{2}} = {whole(v) - V1} → V(0) = {whole(v)} V.'], p=dict(t=t, A=A, B=B, x=x, y=y, V1=V1))
    if t == 'swing':
        th = rng.choice([30, 45, 60, 90, 120, 180 - 30]); f = 2 * (1 - math.cos(math.radians(th)))
        q = f'A particle (mass m, charge q) on a string of length l, other end fixed at O, rests on a smooth horizontal table with the string at {th}° to the +x axis. A uniform field E along +x is switched on. When the string lies along the +x axis, the speed is √{{x\\f{{qEl}}{{m}}}}, where x is :'
        o, a = mcq(rng, nf(f, 3), [nf(f * k, 3) for k in (0.5, 2, 0.25, 1.5)] + ['1' if abs(f - 1) > .01 else '3'])
        return dict(q=q, o=o, a=a, sol=['Work by qE = qE × (x-displacement).', f'x-displacement = l(1 − cos {th}°) → v^{{2}} = {nf(f, 3)}\\f{{qEl}}{{m}}.'], p=dict(t=t, th=th))
    if t == 'tri':
        qs = [rng.choice([1, 2, -1, -2, 3]) for _ in range(3)]; a_ = rng.choice([10, 20, 30, 50, 100])
        Uv = K9 * 1e-12 * (qs[0] * qs[1] + qs[1] * qs[2] + qs[0] * qs[2]) / (a_ / 100)
        need(abs(Uv) > 1e-9)
        q = f'Charges {qs[0]} μC, {qs[1]} μC and {qs[2]} μC sit at the corners of an equilateral triangle of side {a_} cm. Their total potential energy is :'.replace('-', '−')
        o, a = mcq(rng, U(Uv, 'J'), [U(x, 'J') for x in (-Uv, Uv * 3, Uv / 2, Uv * 2, K9 * 1e-12 * sum(qs) ** 2 / (a_ / 100) + 1e-12)])
        return dict(q=q, o=o, a=a, sol=['U = k Σ_{pairs} \\f{q_{i}q_{j}}{a}.', f'≈ {U(Uv, "J")}.'.replace('-', '−')], p=dict(t=t, qs=qs, a=a_))
    Q = rng.choice([1, 2, 5, 10]); qq = rng.choice([1, 2, 5]); m = rng.choice([1, 2, 5, 10]); v = rng.choice([1, 2, 3, 5, 10])
    d = K9 * Q * 1e-6 * qq * 1e-6 / (0.5 * m * 1e-3 * v * v)
    q = f'A particle of mass {m} g and charge {qq} μC is fired with speed {v} m/s straight at a fixed charge {Q} μC from very far away. Its distance of closest approach is :'
    o, a = mcq(rng, U(d, 'm'), dists(d, (2, 0.5, 4, 0.25, 10), 'm'))
    return dict(q=q, o=o, a=a, sol=['All KE becomes PE: ½mv^{2} = \\f{kQq}{r}.', f'r = \\f{{2kQq}}{{mv^{{2}}}} ≈ {U(d, "m")}.'], p=dict(t='appr', Q=Q, qq=qq, m=m, v=v))

# =============================== conductors ===============================
def g_cond(rng):
    t = rng.choice(['ratio', 'common', 'cavity', 'shellE'])
    if t in ('ratio', 'common'):
        r1, r2 = rng.sample([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20], 2)
        if t == 'ratio':
            what = rng.choice(['charge', 'field', 'surface charge density', 'potential'])
            v = {'charge': F(r1, r2), 'field': F(r2, r1), 'surface charge density': F(r2, r1), 'potential': F(1)}[what]
            q = f'Conducting spheres of radii {r1} cm and {r2} cm are charged and joined by a thin wire. The ratio (first : second) of their {what} is :'
            o, a = mcq(rng, fr(v), [fr(x) for x in (F(r1, r2), F(r2, r1), F(r1 * r1, r2 * r2), F(r2 * r2, r1 * r1), F(1))])
            return dict(q=q, o=o, a=a, sol=['Joined → same potential: \\f{kq_{1}}{r_{1}} = \\f{kq_{2}}{r_{2}} → q ∝ r.', 'Surface field and σ ∝ \\f{q}{r^{2}} ∝ \\f{1}{r}.', f'Ratio = {fr(v)}.'], p=dict(t=t, r1=r1, r2=r2, w=what))
        Q1, Q2 = rng.choice([10, 20, 30, 40, 60]), rng.choice([0, 10, 20, -10, 30])
        q1 = F(Q1 + Q2) * r1 / (r1 + r2); need(q1.denominator == 1 and q1 != 0)
        q = f'Spheres of radii {r1} cm (charge {Q1} μC) and {r2} cm (charge {Q2} μC) are joined by a thin wire. The charge on the {r1} cm sphere becomes ______ μC.'.replace('-', '−')
        return dict(q=q, o=None, a=int(q1), sol=['Total charge is shared in proportion to radius.', f'q_{{1}} = {Q1 + Q2} × \\f{{{r1}}}{{{r1 + r2}}} = {q1} μC.'], p=dict(t=t, r1=r1, r2=r2, Q1=Q1, Q2=Q2))
    if t == 'cavity':
        qi, qs = rng.choice([1, 2, 3, 4, 5]), rng.choice([0, 1, 2, -1, 3, 4]); what = rng.choice(['inner', 'outer'])
        v = -qi if what == 'inner' else qi + qs
        q = f'A charge {qi} μC sits inside the cavity of a conducting shell that carries a net charge {qs} μC. The charge on the {what} surface of the shell is ______ μC.'.replace('-', '−')
        need(v != 0)
        sol = ['Inside the metal E = 0, so a Gaussian surface in the metal encloses zero charge.', f'Inner surface: −{qi} μC; outer: {qs} + {qi} = {qi + qs} μC.'.replace('+ -', '− ').replace('-', '−')]
        if v > 0: return dict(q=q, o=None, a=v, sol=sol, p=dict(t=t, qi=qi, qs=qs, w=what))
        o, a = mcq(rng, str(v).replace('-', '−'), [str(x).replace('-', '−') for x in (-v, qs, 0, qi + qs, -(qi + qs), v - 1)])
        return dict(q=q.replace('______ μC', '(in μC) :'), o=o, a=a, sol=sol, p=dict(t=t, qi=qi, qs=qs, w=what))
    Q = rng.choice([1, 2, 3, 4, 5, 6, 8, 9]); R = rng.choice([5, 10, 15, 20, 30]); r = rng.choice([F(1, 2), F(1, 5), 2, 3, F(3, 2)]) * R
    E = 0 if r < R else K9 * Q * 1e-9 / float(r / 100) ** 2
    q = f'A conducting sphere of radius {R} cm carries {Q} nC. The field at {fr(r)} cm from its centre is :'
    o, a = mcq(rng, U(E, 'N/C') if E else '0', [U(x, 'N/C') for x in (K9 * Q * 1e-9 / (R / 100) ** 2, K9 * Q * 1e-9 / float(r / 100), K9 * Q * 1e-9 / float(r / 100) ** 2 * 2, K9 * Q * 1e-9 / float(r / 100) ** 2 / 2) if x != E] + (['0'] if E else []))
    return dict(q=q, o=o, a=a, sol=['Inside a conductor E = 0; outside it acts like a point charge.', f'E = {U(E, "N/C") if E else "0"}.'], p=dict(t=t, Q=Q, R=R, r=float(r)))

# =============================== capacitors ===============================
def g_cap(rng):
    t = rng.choice(['join', 'share2', 'combo', 'stair', 'udens', 'circ', 'bridge', 'pull', 'ratioE'])
    if t == 'join':
        C1, C2 = rng.choice([1, 2, 3, 4, 5, 6, 10]), rng.choice([1, 2, 3, 4, 6, 8, 12]); V1, V2 = rng.choice([10, 20, 30, 50, 60, 100]), rng.choice([0, 10, 20, 40, 60, 100]); opp = rng.choice([False, True])
        need(V1 != V2 or opp)
        Vc = F(C1 * V1 + (-1 if opp else 1) * C2 * V2, C1 + C2); loss = F(C1 * C2, 2 * (C1 + C2)) * (V1 + (1 if opp else -1) * V2) ** 2
        need(loss.denominator == 1)
        q = f'A {C1} μF capacitor charged to {V1} V is joined to a {C2} μF capacitor charged to {V2} V ({"positive plate to negative plate" if opp else "like plates together"}). The energy lost is ______ μJ.'
        return dict(q=q, o=None, a=int(loss), sol=['Loss = \\f{C_{1}C_{2}}{2(C_{1} + C_{2})}(ΔV)^{2}' + (' with ΔV = V_{1} + V_{2} for opposite plates.' if opp else '.'), f'= \\f{{{C1} × {C2}}}{{2 × {C1 + C2}}} × {V1 + (1 if opp else -1) * V2}^{{2}} = {loss} μJ.'], p=dict(t=t, C1=C1, C2=C2, V1=V1, V2=V2, opp=opp))
    if t == 'share2':
        C1 = rng.choice([50, 100, 200, 300, 400]); V0 = rng.choice([30, 40, 60, 90, 100, 120]); Vf = rng.choice([10, 15, 20, 30, 40, 60])
        need(Vf < V0); C2 = F(C1 * V0, Vf) - C1; need(C2.denominator == 1)
        q = f'A {C1} pF capacitor is charged to {V0} V and the battery removed. An uncharged capacitor is then connected across it and the common voltage becomes {Vf} V. Its capacitance is ______ pF.'
        return dict(q=q, o=None, a=int(C2), sol=['Charge is conserved: C_{1}V_{0} = (C_{1} + C_{2})V.', f'C_{{2}} = \\f{{{C1} × {V0}}}{{{Vf}}} − {C1} = {C2} pF.'], p=dict(t=t, C1=C1, V0=V0, Vf=Vf))
    if t == 'combo':
        cs = [rng.choice([2, 3, 4, 5, 6, 10, 12, 15, 20, 30]) for _ in range(3)]; kind = rng.choice(['s+p', 'p+s', 'Er'])
        if kind == 's+p':
            v = F(cs[0] * cs[1], cs[0] + cs[1]) + cs[2]; txt = f'{cs[0]} μF and {cs[1]} μF are in series, and this pair is in parallel with {cs[2]} μF'
        elif kind == 'p+s':
            v = F((cs[0] + cs[1]) * cs[2], cs[0] + cs[1] + cs[2]); txt = f'{cs[0]} μF and {cs[1]} μF are in parallel, and this pair is in series with {cs[2]} μF'
        else:
            v = sum(cs) / (1 / sum(F(1, c) for c in cs)); txt = None
        if txt:
            q = f'{txt}. The equivalent capacitance is ______ μF.'
            need(v.denominator == 1)
            return dict(q=q, o=None, a=int(v), sol=['Series: \\f{1}{C} adds. Parallel: C adds.', f'C = {v} μF.'], p=dict(t=t, cs=cs, k=kind))
        need(v.denominator == 1 and v > 1)
        q = f'Capacitors {cs[0]} μF, {cs[1]} μF and {cs[2]} μF store energy E in parallel across a supply. In series across the same supply they store \\f{{E}}{{x}}. x = ______'
        return dict(q=q, o=None, a=int(v), sol=['Same V → U ∝ C.', f'x = \\f{{C_{{par}}}}{{C_{{ser}}}} = {v}.'], p=dict(t=t, cs=cs, k=kind))
    if t == 'stair':
        n = rng.choice([2, 3, 4]); s0 = rng.choice([1, 2, 3]); v = sum(F(1, n * i) for i in range(s0, s0 + n))
        q = f'One plate of a capacitor is flat (area A); the other is a staircase of {n} equal steps, each of area \\f{{A}}{{{n}}}, at gaps {s0}d, {s0 + 1}d, … {s0 + n - 1}d. The capacitance is :'
        o, a = mcq(rng, f'{fr(v)}\\f{{ε_{{0}}A}}{{d}}', [f'{fr(x)}\\f{{ε_{{0}}A}}{{d}}' for x in (1 / sum(F(i) for i in range(1, n + 1)) * n, F(1, n), v * 2, 1 / (n * sum(F(1, i) for i in range(1, n + 1))), F(2, n + 1))])
        return dict(q=q, o=o, a=a, sol=['The steps are capacitors side by side → parallel.', f'C = \\f{{ε_{{0}}A}}{{{n}d}}(\\f{{1}}{{{s0}}} + … + \\f{{1}}{{{s0 + n - 1}}}) = {fr(v)}\\f{{ε_{{0}}A}}{{d}}.'], p=dict(t=t, n=n, s0=s0))
    if t == 'udens':
        V = rng.choice([5, 10, 20, 50, 100, 200]); d = rng.choice([1, 2, 5, 10, 100, 1000])
        u = 0.5 * E0 * (V / (d * 1e-6)) ** 2
        q = f'A parallel-plate capacitor with plates {d} μm apart is charged to {V} V (ε_{{0}} = 8.85 × 10^{{−12}}). The energy density between the plates is :'
        o, a = mcq(rng, U(u, 'J/m^{3}'), dists(u, (2, 0.5, 1e-3, 100, 1e-2), 'J/m^{3}'))
        return dict(q=q, o=o, a=a, sol=['E = \\f{V}{d}; u = ½ε_{0}E^{2}.', f'≈ {U(u, "J/m^{3}")}.'], p=dict(t=t, V=V, d=d))
    if t == 'circ':
        Ev = rng.choice([5, 6, 9, 10, 12, 15, 20, 24]); R1, R2 = rng.choice([1, 2, 3, 4, 5, 6, 10, 15]), rng.choice([1, 2, 3, 4, 5, 6, 10, 15, 20]); C = rng.choice([2, 4, 5, 6, 8, 10])
        Q = F(C * Ev * R1, R1 + R2); need(Q.denominator == 1)
        q = f'Resistors {R1} Ω and {R2} Ω are in series across a {Ev} V battery; a {C} μF capacitor is connected across the {R1} Ω resistor. At steady state its charge is ______ μC.'
        return dict(q=q, o=None, a=int(Q), sol=['No steady current enters the capacitor: I = \\f{E}{R_{1} + R_{2}}.', f'Q = C × IR_{{1}} = {C} × \\f{{{Ev} × {R1}}}{{{R1 + R2}}} = {Q} μC.'], p=dict(t=t, Ev=Ev, R1=R1, R2=R2, C=C))
    if t == 'bridge':
        Ev = rng.choice([6, 10, 12, 15, 20, 24, 30]); Rs = [rng.choice([1, 2, 3, 4, 5, 6, 8]) for _ in range(4)]; C = rng.choice([2, 5, 10, 15, 30, 50, 150])
        dV = F(Ev * Rs[1], Rs[0] + Rs[1]) - F(Ev * Rs[3], Rs[2] + Rs[3]); Q = abs(C * dV); need(Q.denominator == 1 and Q != 0)
        q = f'A {Ev} V battery is connected between P (+) and N (−). Branch 1: {Rs[0]} Ω from P to A, {Rs[1]} Ω from A to N. Branch 2: {Rs[2]} Ω from P to B, {Rs[3]} Ω from B to N. A {C} μF capacitor joins A and B. Its steady charge is ______ μC.'
        return dict(q=q, o=None, a=int(Q), sol=['Each branch is a potential divider (no current through C).', f'V_{{A}} = {fr(F(Ev * Rs[1], Rs[0] + Rs[1]))} V, V_{{B}} = {fr(F(Ev * Rs[3], Rs[2] + Rs[3]))} V above N → Q = {C} × |V_{{A}} − V_{{B}}| = {Q} μC.'], p=dict(t=t, Ev=Ev, Rs=Rs, C=C))
    if t == 'pull':
        bat = rng.choice([True, False]); qty = rng.choice(['energy U', 'charge Q', 'field E between plates', 'force between plates', 'potential difference V'])
        al = {(True, 'energy U'): -1, (True, 'charge Q'): -1, (True, 'field E between plates'): -1, (True, 'force between plates'): -2, (True, 'potential difference V'): 0,
              (False, 'energy U'): 1, (False, 'charge Q'): 0, (False, 'field E between plates'): 0, (False, 'force between plates'): 0, (False, 'potential difference V'): 1}[(bat, qty)]
        q = f'The plates of an air capacitor are slowly pulled apart {"while it stays connected to a battery" if bat else "after it has been charged and disconnected"}. As a function of the separation x, the {qty} varies as x^{{α}}. α = '
        o, a = mcq(rng, str(al).replace('-', '−'), [str(x).replace('-', '−') for x in (-2, -1, 0, 1, 2)])
        return dict(q=q, o=o, a=a, sol=['C = \\f{ε_{0}A}{x}. ' + ('Battery on → V fixed, Q = CV ∝ \\f{1}{x}, E = \\f{V}{x}, U = ½CV^{2}, F = \\f{Q^{2}}{2ε_{0}A}.' if bat else 'Isolated → Q fixed; E = \\f{Q}{ε_{0}A} fixed, V = \\f{Q}{C} ∝ x, U = \\f{Q^{2}}{2C} ∝ x, F = \\f{Q^{2}}{2ε_{0}A} fixed.'), f'α = {al}.'.replace('-', '−')], p=dict(t=t, bat=bat, qty=qty))
    C = rng.choice([1, 2, 4, 5, 10, 20, 40]); V = rng.choice([10, 20, 50, 100, 200])
    Uv = F(1, 2) * C * V * V
    q = f'A {C} μF capacitor is charged to {V} V. The energy stored is :'
    o, a = mcq(rng, U(float(Uv) * 1e-6, 'J'), [U(float(x) * 1e-6, 'J') for x in (Uv * 2, Uv / 2, F(C * V), Uv * 4)])
    return dict(q=q, o=o, a=a, sol=['U = ½CV^{2}.', f'= ½ × {C} × 10^{{−6}} × {V}^{{2}} = {U(float(Uv) * 1e-6, "J")}.'], p=dict(t='energy', C=C, V=V))

# =============================== dielectrics ===============================
def g_diel(rng):
    t = rng.choice(['slab', 'layers', 'induced', 'battery', 'shift', 'pct', 'Kfind'])
    if t in ('slab', 'pct'):
        f = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(1, 5)]); Kd = rng.choice([2, 3, 4, 5, 6, 8, 10])
        v = 1 / (1 - f + f / Kd)
        if t == 'pct':
            pc = (v - 1) * 100; need(F(pc).denominator == 1)
            q = f'A slab of dielectric constant {Kd} and thickness {fr(f)} of the gap, covering the full plate area, is put in a parallel-plate air capacitor. The capacitance rises by ______ %.'
            return dict(q=q, o=None, a=int(pc), sol=['C′ = \\f{ε_{0}A}{d − t + t/K}.', f'\\f{{C′}}{{C}} = {fr(v)} → +{int(pc)} %.'], p=dict(t='slab', f=str(f), K=Kd))
        q = f'A slab of dielectric constant {Kd} with thickness {fr(f)} of the gap (full plate area) is inserted in a capacitor of capacitance C. The new capacitance is :'
        o, a = mcq(rng, f'{fr(v)}C', [f'{fr(x)}C' for x in (Kd * f + 1 - f, F(Kd), 1 + f, v * 2, Kd * f)])
        return dict(q=q, o=o, a=a, sol=['C′ = \\f{ε_{0}A}{d − t + t/K}.', f'= \\f{{C}}{{1 − {fr(f)} + {fr(f)}/{Kd}}} = {fr(v)}C.'], p=dict(t='slab', f=str(f), K=Kd))
    if t == 'layers':
        K1, K2 = rng.sample([2, 3, 4, 5, 6, 8], 2); C0 = rng.choice([1, 2, 3, 4, 5, 6, 10]); how = rng.choice(['series', 'side'])
        v = F(2 * K1 * K2, K1 + K2) * C0 if how == 'series' else F(K1 + K2, 2) * C0
        need(v.denominator == 1)
        txt = 'as two layers, each half the gap thick over the full area' if how == 'series' else 'side by side, each over half the plate area through the full gap'
        q = f'An air capacitor of {C0} pF is filled with dielectrics K = {K1} and K = {K2} {txt}. The new capacitance is ______ pF.'
        return dict(q=q, o=None, a=int(v), sol=[('Layers act in series: C = \\f{2K_{1}K_{2}}{K_{1} + K_{2}}C_{0}.' if how == 'series' else 'Side by side act in parallel: C = \\f{K_{1} + K_{2}}{2}C_{0}.'), f'= {v} pF.'], p=dict(t=t, K1=K1, K2=K2, C0=C0, how=how))
    if t == 'induced':
        Kd = rng.choice([2, 3, 4, 5, 6, 8, 10]); Q = rng.choice([2, 4, 5, 6, 8, 10, 12, 20, 30, 40]); qi = F(Q) * (1 - F(1, Kd)); need(qi.denominator == 1)
        q = f'A capacitor holds {Q} μC. A slab of dielectric constant {Kd} fills the gap. The induced charge on each face of the slab is ______ μC.'
        return dict(q=q, o=None, a=int(qi), sol=['Q_{induced} = Q(1 − \\f{1}{K}).', f'= {Q}(1 − \\f{{1}}{{{Kd}}}) = {qi} μC.'], p=dict(t=t, K=Kd, Q=Q))
    if t == 'Kfind':
        Kd = rng.choice([2, 3, 4, 5, 6, 8, 10]); Q = rng.choice([2, 4, 5, 6, 8, 10, 12, 20, 30, 40]); qi = F(Q) * (1 - F(1, Kd)); need(qi.denominator == 1)
        q = f'A capacitor holds {Q} μC. A slab filling the gap shows an induced charge of {qi} μC on one face. Its dielectric constant is ______.'
        return dict(q=q, o=None, a=Kd, sol=['Q_{induced} = Q(1 − \\f{1}{K}).', f'1 − \\f{{1}}{{K}} = \\f{{{qi}}}{{{Q}}} → K = {Kd}.'], p=dict(t=t, K=Kd, Q=Q))
    if t == 'battery':
        C = rng.choice([1, 2, 5, 10, 20, 40, 50]); V = rng.choice([10, 20, 50, 100, 200]); Kd = rng.choice([2, 3, 4, 5]); on = rng.choice([True, False])
        if on: dQ = (Kd - 1) * C * V; dU = F(1, 2) * (Kd - 1) * C * V * V; txt = 'stays connected to the battery'
        else: dQ = 0; dU = F(1, 2) * C * V * V * (1 - F(1, Kd)); txt = 'is first disconnected from the battery'
        right = f'ΔQ = {nf(dQ)} μC, |ΔU| = {nf(float(dU))} μJ'
        q = f'A {C} μF capacitor is charged to {V} V. It {txt}, and a dielectric K = {Kd} then fills the gap. The change in charge and the size of the change in energy are :'
        wrong = [f'ΔQ = {nf(x)} μC, |ΔU| = {nf(float(y))} μJ' for x, y in (((Kd - 1) * C * V, dU * 2), (0, F(1, 2) * (Kd - 1) * C * V * V), ((Kd - 1) * C * V, F(1, 2) * C * V * V * (1 - F(1, Kd))), (Kd * C * V, dU), (0, dU * 2))]
        o, a = mcq(rng, right, wrong)
        return dict(q=q, o=o, a=a, sol=[('V fixed: C → KC, Q and U = ½CV^{2} both grow K times.' if on else 'Q fixed: U = \\f{Q^{2}}{2C} falls to \\f{1}{K} of its value.'), right + '.'], p=dict(t=t, C=C, V=V, K=Kd, on=on))
    d = rng.choice([4, 5, 6, 8, 10]); tt = rng.choice([1, 2, 3, 4, 5, 6]); Kd = rng.choice([2, 3, 4, 5, 6])
    need(tt <= d); s = tt * (1 - F(1, Kd))
    q = f'Plates {d} mm apart; a slab {tt} mm thick of K = {Kd} is put between them. By how much must one plate be moved away so the capacitance returns to its old value?'
    o, a = mcq(rng, f'{nf(float(s), 3)} mm', [f'{nf(float(x), 3)} mm' for x in (F(tt, Kd), tt * Kd, F(tt), s * 2, tt * (Kd - 1))])
    return dict(q=q, o=o, a=a, sol=['The slab acts like air of thickness \\f{t}{K}: it "removes" t(1 − \\f{1}{K}) of gap.', f'Move = {tt}(1 − \\f{{1}}{{{Kd}}}) = {nf(float(s), 3)} mm.'], p=dict(t='shift', d=d, tt=tt, K=Kd))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, IndexError, StopIteration): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(coul=g_coul, dip=g_dip, gauss=g_gauss, pot=g_pot, cond=g_cond, cap=g_cap, diel=g_diel).items()}
def finish(it): return it

# =============================== independent checks ===============================
def ans(it): return it['o'][it['a']] if it.get('o') else it['a']
def unf(s):
    s = s.replace('−', '-').strip()
    neg = s.startswith('-'); s = s.lstrip('-')
    if s.startswith('\\f{'): a, b = s[3:-1].split('}{'); v = F(int(a), int(b))
    else: v = F(s)
    return -v if neg else v
def capnet(edges, a, b):   # equivalent capacitance by the resistor solver: capacitor C ↔ conductance C
    from common import solve_net
    return 1 / solve_net([(u, v, 1 / F(c)) for u, v, c in edges], a, b)
def check(it):
    p = it['p']; t = p['t']; Rv = ans(it)
    if t == 'force': return close(num(Rv), mag(efield([(p['q1'] * 1e-6, 0, 0, 0)], (p['r'] / 100, 0, 0))) * p['q2'] * 1e-6)
    if t in ('null', 'nullout'):
        d = p['d'] / 100; qs = [(1e-9, 0, 0, 0), ((1 if t == 'null' else -1) * p['n'] ** 2 * 1e-9, d, 0, 0)]
        x = bis(lambda x: efield(qs, (x, 0, 0))[0], 1e-6, d - 1e-6) if t == 'null' else -bis(lambda x: efield(qs, (-x, 0, 0))[0], 1e-6, 10 * d)
        return close(float(Rv) if not it.get('o') else num(Rv), abs(x) * 100, 0.006)
    if t == 'share':
        P_, S_, R_ = p['a0'], p['b0'], 0; P_ = R_ = (P_ + R_) / 2; S_ = R_ = (S_ + R_) / 2; return abs(Rv - p['F0'] * P_ * S_ / (p['a0'] * p['b0'])) < 1e-9
    if t == 'hang':
        qv = num(Rv); fx, fy = qv * p['E'], p['m'] * 1e-3 * 10; return abs(math.degrees(math.atan2(fx, fy)) - p['th']) < 0.3
    if t == 'poly':
        n = p['n']; qs = [((0 if (i == 0 and p['mode'] == 'remove') else -1 if (i == 0 and p['mode'] == 'flip') else 2 if i == 0 and p['mode'] == 'double' else 1), math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), 0) for i in range(n)]
        return abs(mag(efield(qs, (0, 0, 0))) / K9 - Rv) < 1e-9
    if t == 'arc':
        def af(al, N=6000):
            ex = ey = 0.0
            for i in range(N): th = math.radians(al) * (i + .5) / N; ex += math.cos(th); ey += math.sin(th)
            return math.hypot(ex, ey) * math.radians(al) / N
        return close(float(Rv[:-1]) if Rv != '0E' else 0, af(p['a2']) / af(p['a1']))
    if t == 'rmax':
        N = 600; R = p['R'] * math.sqrt(2); qs = [(1 / N, R * math.cos(2 * math.pi * i / N), R * math.sin(2 * math.pi * i / N), 0) for i in range(N)]
        f = lambda z: efield(qs, (0, 0, z))[2]
        lo, hi = 0.01, 5 * R
        for _ in range(80):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if f(m1) < f(m2): lo = m1
            else: hi = m2
        return abs(lo - Rv) < 0.01 * Rv
    if t == 'rz':
        N = 2000; qs = [(1 / N / K9, math.cos(2 * math.pi * i / N), math.sin(2 * math.pi * i / N), 0) for i in range(N)]; return close(num(Rv), efield(qs, (0, 0, p['z']))[2])
    if t == 'axeq':
        def dp(): a = 1e-5; return [(1 / (2 * a), a, 0, 0), (-1 / (2 * a), -a, 0, 0)]
        m = float(F(p['m'])); w = p['w']
        e1 = mag(efield(dp(), (1, 0, 0) if w in ('ae', 'aa') else (0, 1, 0))); e2 = mag(efield(dp(), (m, 0, 0) if w in ('ea', 'aa') else (0, m, 0)))
        return close(Rv, e1 / e2, 0.002)
    if t == 'torque':
        d = p['d'] / 100; th = math.radians(p['th']); r = (d / 2 * math.cos(th), d / 2 * math.sin(th)); Fx = p['qq'] * 1e-6 * p['E']
        tau = (r[0] * 0 - r[1] * Fx) + ((-r[0]) * 0 - (-r[1]) * (-Fx)); return close(num(Rv), abs(tau))
    if t == 'work':
        N = 4000; a1, a2 = math.radians(p['t1']), math.radians(p['t2']); W = sum(p['pv'] * p['E'] * math.sin(a1 + (a2 - a1) * (i + .5) / N) * (a2 - a1) / N for i in range(N)); return close(num(Rv), W)
    if t == 'perp':
        def dp(px, py): a = 1e-5; return [(1 / (2 * a), a * px, a * py, 0), (-1 / (2 * a), -a * px, -a * py, 0)]
        r = num(Rv); pt = (1, 0, 0) if p['w'] == 'axA' else (0, 1, 0)
        E = [x + y for x, y in zip(efield(dp(1, 0), pt), [r * z for z in efield(dp(0, 1), pt)])]
        along = abs(E[0]) if p['w'] == 'axA' else abs(E[1]); across = abs(E[1]) if p['w'] == 'axA' else abs(E[0])
        return abs(math.degrees(math.atan2(across, along)) - p['ang']) < 0.3
    if t == 'sheet':
        E = p['sg'] * 1e-6 / (2 * E0); return close(num(Rv), p['qq'] * 1e-6 * p['L'] / 100 * E * abs(math.sin(math.radians(p['th']))))
    if t == 'vec':
        d, E = p['d'], (p['Ex'], 0, 0); pv = [p['qq'] * 1e-6 * x for x in d]
        cr = [pv[1] * E[2] - pv[2] * E[1], pv[2] * E[0] - pv[0] * E[2], pv[0] * E[1] - pv[1] * E[0]]; return close(num(Rv), mag(cr))
    if t == 'encl': return unf(Rv.split('q')[0] or '1') == sum(p['ins'])
    if t == 'cube':
        pt = dict(centre=(.5, .5, .5), face=(.5, .5, 0), edge=(.5, 0, 0), corner=(0, 0, 0))[p['w']]
        fr_ = cube_frac(pt, 36); v = p['qn'] * fr_; got = float(Rv) if not it.get('o') else float(unf(Rv))
        return abs(got - v) < 0.02 * p['qn']
    if t == 'flat':
        n = [0, 0, 0]; n[p['ax']] = p['A']; return Rv == abs(sum(a * b for a, b in zip(p['E'], n)))
    if t == 'sheets':
        x = (p['reg'] - 0.5); E = sum(s / 2 * (1 if x > i else -1) for i, s in enumerate(p['ss'])); got = float(Rv) if not it.get('o') else float(unf(Rv)); return abs(got - abs(E)) < 1e-9
    if t == 'xfield':
        N = 200; h = p['s'] / N; div = sum((p['c'] * (x + 1e-6) - p['c'] * x) / 1e-6 * h * p['s'] ** 2 for x in [p['x0'] + (i + .5) * h for i in range(N)]); return abs(Rv - div) < 1e-3
    if t == 'diag': return close(num(Rv), p['lam'] * 1e-9 * p['L'] * 1e-2 / (1 / (4 * math.pi * K9)))
    if t == 'qphi': return close(num(Rv), p['ph'] * E0)
    if t == 'linesheet':
        lam = 1.0; sg = p['m'] * lam; es = sg / 2; el = lam / (2 * math.pi * p['r']); return abs((es / el / math.pi) ** 2 - Rv) < 1e-6
    if t == 'sphere2':
        ins = lambda R: sum(q for q, x in ((p['q1'], p['x1']), (p['q2'], p['x2'])) if x < R)
        a, b = Rv.split(' : '); return F(int(a), int(b)) == F(ins(p['R1']), ins(p['R2']))
    if t == 'shell':
        R = p['R'] / 100; N = 3000; Q = p['V0'] * R / K9
        # shell as many rings (numerical potential at distance r on the axis)
        r = p['r'] / 100; V = 0.0
        for i in range(N):
            th = math.pi * (i + .5) / N; dq = Q * 0.5 * math.sin(th) * math.pi / N
            V += K9 * dq / math.hypot(R * math.sin(th), r - R * math.cos(th))
        got = Rv if not it.get('o') else num(Rv); return close(got, V, 0.003)
    if t == 'move':
        qs = [(p['Q'], 0, 0, 0)]; W = p['qq'] * 1e-6 * (epot(qs, p['B']) - epot(qs, p['A'])); return close(num(Rv), W)
    if t == 'pair': return close(num(Rv), p['q1'] * 1e-6 * epot([(p['q2'] * 1e-6, 0, 0, 0)], (p['r'] / 100, 0, 0)))
    if t == 'nuc': return close(Rv, epot([(p['Z'] * 1.6e-19, 0, 0, 0)], (p['R'] * 1e-15, 0, 0)) / 1e6, 1e-6)
    if t == 'grad':   # integrate along x first then y (different path)
        N = 2000; I = sum(p['A'] * (p['x'] * (i + .5) / N) * p['x'] / N for i in range(N)) + sum(p['B'] * (p['y'] * (i + .5) / N) * p['y'] / N for i in range(N))
        return abs(Rv - (p['V1'] + I)) < 1e-3
    if t == 'swing':
        th, w, dt = math.radians(p['th']), 0.0, 2e-5
        while th > 0: w -= math.sin(th) * dt; th += w * dt
        return close(num(Rv), w * w, 0.01)
    if t == 'tri':
        a = p['a'] / 100; pts = [(0, 0, 0), (a, 0, 0), (a / 2, a * math.sqrt(3) / 2, 0)]; qs = [x * 1e-6 for x in p['qs']]
        Uv = sum(qs[i] * epot([(qs[j], *pts[j])], pts[i]) for i in range(3) for j in range(i + 1, 3)); return close(num(Rv), Uv)
    if t == 'appr':   # march the particle in, find the turning point
        m, q, Q = p['m'] * 1e-3, p['qq'] * 1e-6, p['Q'] * 1e-6; KE = 0.5 * m * p['v'] ** 2
        r = bis(lambda r: KE - K9 * Q * q / r, 1e-9, 1e9); return close(num(Rv), r)
    if t == 'ratio':
        r1, r2 = p['r1'], p['r2']; q1 = bis(lambda q: K9 * q / r1 - K9 * (1 - q) / r2, 0, 1); q2 = 1 - q1
        v = {'charge': q1 / q2, 'field': (q1 / r1 ** 2) / (q2 / r2 ** 2), 'surface charge density': (q1 / r1 ** 2) / (q2 / r2 ** 2), 'potential': (q1 / r1) / (q2 / r2)}[p['w']]
        return close(float(unf(Rv)), v, 1e-6)
    if t == 'common':
        T = p['Q1'] + p['Q2']; q1 = bis(lambda q: q / p['r1'] - (T - q) / p['r2'], -1000, 1000); return abs(Rv - q1) < 1e-6
    if t == 'cavity':
        inner, outer = -p['qi'], p['qs'] + p['qi']; v = inner if p['w'] == 'inner' else outer
        return (Rv == v) if not it.get('o') else unf(Rv) == v
    if t == 'shellE':
        r, R = p['r'] / 100, p['R'] / 100; E = 0 if r < R else mag(efield([(p['Q'] * 1e-9, 0, 0, 0)], (r, 0, 0)))
        return (Rv == '0') if E == 0 else close(num(Rv), E)
    if t == 'join':
        C1, C2 = p['C1'], p['C2']; q1, q2 = C1 * p['V1'], C2 * p['V2'] * (-1 if p['opp'] else 1)
        Ui = q1 * q1 / (2 * C1) + q2 * q2 / (2 * C2); V = (q1 + q2) / (C1 + C2); Uf = 0.5 * (C1 + C2) * V * V; return abs(Rv - (Ui - Uf)) < 1e-6
    if t == 'share2': return abs(p['C1'] * p['V0'] - (p['C1'] + Rv) * p['Vf']) < 1e-9
    if t == 'combo':
        cs = p['cs']
        if p['k'] == 's+p': v = capnet([('a', 'm', cs[0]), ('m', 'b', cs[1]), ('a', 'b', cs[2])], 'a', 'b')
        elif p['k'] == 'p+s': v = capnet([('a', 'm', cs[0]), ('a', 'm', cs[1]), ('m', 'b', cs[2])], 'a', 'b')
        else: v = capnet([('a', 'b', c) for c in cs], 'a', 'b') / capnet([('a', 'm', cs[0]), ('m', 'n', cs[1]), ('n', 'b', cs[2])], 'a', 'b')
        return Rv == v
    if t == 'stair':
        n = p['n']; v = capnet([('a', 'b', F(1, n * i)) for i in range(p['s0'], p['s0'] + n)], 'a', 'b'); return unf(Rv.split('\\f{ε')[0]) == v
    if t == 'udens':
        C_per = E0 / (p['d'] * 1e-6); Uv = 0.5 * C_per * p['V'] ** 2; return close(num(Rv), Uv / (p['d'] * 1e-6))
    if t == 'circ':
        V = solve_dc([('a', 'm', p['R1']), ('m', 'g', p['R2'])], [('g', 'a', p['Ev'], F(1, 10 ** 12))], 'g'); return abs(Rv - p['C'] * float(V['a'] - V['m'])) < 1e-6
    if t == 'bridge':
        Rs = p['Rs']; V = solve_dc([('P', 'A', Rs[0]), ('A', 'N', Rs[1]), ('P', 'B', Rs[2]), ('B', 'N', Rs[3])], [('N', 'P', p['Ev'], F(1, 10 ** 12))], 'N')
        return abs(Rv - p['C'] * abs(float(V['A'] - V['B']))) < 1e-6
    if t == 'pull':
        def val(x):
            C = 1 / x
            if p['bat']: V = 1.0; Q = C * V
            else: Q = 1.0; V = Q / C
            return {'energy U': 0.5 * Q * V, 'charge Q': Q, 'field E between plates': V / x, 'force between plates': Q * Q / 2, 'potential difference V': V}[p['qty']]
        al = math.log(val(2.0) / val(1.0)) / math.log(2); return abs(al - float(Rv.replace('−', '-'))) < 1e-9
    if t == 'energy': return close(num(Rv), 0.5 * p['C'] * 1e-6 * p['V'] ** 2)
    if t == 'slab':
        f, Kd = float(F(p['f'])), p['K']; v = capnet([('a', 'm', F(1) / F(1 - F(p['f']))), ('m', 'b', F(Kd) / F(p['f']))], 'a', 'b')
        if it.get('o'): return unf(Rv[:-1]) == v
        return abs(Rv - (v - 1) * 100) < 1e-9
    if t == 'layers':
        K1, K2, C0 = p['K1'], p['K2'], p['C0']
        v = capnet([('a', 'm', 2 * K1 * C0), ('m', 'b', 2 * K2 * C0)], 'a', 'b') if p['how'] == 'series' else capnet([('a', 'b', F(K1 * C0, 2)), ('a', 'b', F(K2 * C0, 2))], 'a', 'b')
        return Rv == v
    if t in ('induced', 'Kfind'):   # induced = free − (field inside × ε0A) = Q − Q/K; for Kfind re-solve K by bisection
        Q, Kd = p['Q'], p['K']; qi = Q - Q / Kd
        if t == 'induced': return abs(Rv - qi) < 1e-9
        return abs(bis(lambda K: Q - Q / K - qi, 1.0001, 1000) - Rv) < 1e-6
    if t == 'battery':
        C, V, Kd = p['C'], p['V'], p['K']
        if p['on']: Q1, Q2 = C * V, Kd * C * V; U1, U2 = 0.5 * C * V * V, 0.5 * Kd * C * V * V
        else: Q1 = Q2 = C * V; U1, U2 = Q1 * Q1 / (2 * C), Q1 * Q1 / (2 * Kd * C)
        return Rv == f'ΔQ = {nf(Q2 - Q1)} μC, |ΔU| = {nf(abs(U2 - U1))} μJ'
    if t == 'shift':
        d, tt, Kd = p['d'], p['tt'], p['K']; x = bis(lambda x: 1 / ((d + x - tt) + tt / Kd) - 1 / d, 0, 20); return close(num(Rv), x, 0.006)
    raise KeyError(t)
