"""Practice generators — Physics Unit 13: Magnetic Effects of Current and Magnetism. check() re-solves each item a
different way: fields by numerically integrating Biot–Savart around the actual conductor, forces by summing
I dl × B over the wire or integrating the charge's motion, torques from m × B with explicit vectors, and meter
conversions by solving the current-split condition numerically."""
import math, re
from common import mcq, nf
mu0 = 4e-7 * math.pi; pi = math.pi
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def opts(rng, v, k=(2, 0.5, 4, pi, 1 / pi, 1.5, 3)):
    w = []
    for f in k:
        s = nf(v * f, 3)
        if s != nf(v, 3) and s not in w: w.append(s)
    rng.shuffle(w); return mcq(rng, nf(v, 3), w)
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(sum(x * x for x in a))
def bs(pts, I, P0, n=60):
    B = [0.0, 0.0, 0.0]
    for a, b in zip(pts, pts[1:]):
        for k in range(n):
            p0 = [a[i] + (b[i] - a[i]) * k / n for i in range(3)]; p1 = [a[i] + (b[i] - a[i]) * (k + 1) / n for i in range(3)]
            dl = [p1[i] - p0[i] for i in range(3)]; m = [(p0[i] + p1[i]) / 2 for i in range(3)]; r = [P0[i] - m[i] for i in range(3)]; R = nrm(r); c = cross(dl, r)
            B = [B[i] + mu0 * I / (4 * pi) * c[i] / R ** 3 for i in range(3)]
    return B
def longwire(I, d):   # infinite wire, integrated in the angle variable: B = μ0 I/(4π d) ∫ cos θ dθ over (−π/2, π/2)
    n = 4000; return mu0 * I / (4 * pi * d) * sum(math.cos(-pi / 2 + (k + 0.5) * pi / n) * pi / n for k in range(n))
def ring(R, n=720): return [(R * math.cos(2 * pi * k / n), R * math.sin(2 * pi * k / n), 0) for k in range(n + 1)]

def g_field(rng):
    t = rng.choice(['f_wire', 'f_loop', 'f_sol', 'f_axis', 'f_two', 'f_poly', 'f_arc'])
    if t == 'f_wire':
        I, d = rng.choice([2, 4, 5, 8, 10, 15, 20, 25, 30, 40, 50]), rng.choice([1, 2, 4, 5, 10, 20, 25, 50]); B = 2e-7 * I / (d / 100) * 1e6; need(abs(B - round(B)) < 1e-9)
        return dict(q=f'A long straight wire carries {I} A. The magnetic field at {d} cm from it is ____ μT.', o=None, a=round(B), sol=['B = \\f{μ_{0}I}{2πd} = 2 × 10^{−7}\\f{I}{d}.', f'= {round(B)} μT.'], p=dict(t=t, I=I, d=d / 100))
    if t == 'f_loop':
        N, I, R = rng.choice([1, 10, 20, 50, 100]), rng.choice([1, 2, 5, 10]), rng.choice([2, 5, 10, 20]); B = N * mu0 * I / (2 * R / 100)
        o, an = opts(rng, B)
        return dict(q=f'A circular coil of {N} turn{"s" if N > 1 else ""} and radius {R} cm carries {I} A. The magnetic field at its centre (in T) is', o=o, a=an, sol=['B = \\f{Nμ_{0}I}{2R}.', f'= {nf(B, 3)} T.'], p=dict(t=t, N=N, I=I, R=R / 100))
    if t == 'f_sol':
        n, I = rng.choice([200, 500, 1000, 2000, 5000]), rng.choice([1, 2, 3, 5, 10]); B = mu0 * n * I; mr = rng.choice([1, 1, 100, 400])
        o, an = opts(rng, B * mr)
        return dict(q=f'A long solenoid has {n} turns per metre and carries {I} A{"" if mr == 1 else f"; its core has relative permeability {mr}"}. The field inside (in T) is', o=o, a=an, sol=['B = μ_{r}μ_{0}nI.', f'= {nf(B * mr, 3)} T.'], p=dict(t=t, n=n, I=I, mr=mr))
    if t == 'f_axis':
        R, x = rng.choice([(3, 4), (4, 3), (5, 12), (12, 5), (1, 1), (1, math.sqrt(3)), (8, 6), (6, 8)]); B0 = rng.choice([8, 16, 25, 54, 125, 250, 1000]); B = B0 * R ** 3 / (R * R + x * x) ** 1.5
        o, an = opts(rng, B, (2, 0.5, R / math.hypot(R, x), (R / math.hypot(R, x)) ** 2, 1.5))
        xs = 'R√{3}' if abs(x - math.sqrt(3)) < 1e-9 else ('R' if (R, x) == (1, 1) else f'\\f{{{int(x)}}}{{{R}}}R')
        return dict(q=f'The field at the centre of a circular loop of radius R is {B0} μT. The field at a point on its axis at distance {xs} from the centre is (in μT)', o=o, a=an,
                    sol=['B_{axis} = B_{0}\\f{R^{3}}{(R^{2} + x^{2})^{3/2}}.', f'= {nf(B, 3)} μT.'], p=dict(t=t, R=R, x=x, B0=B0))
    if t == 'f_two':
        I1, I2 = rng.choice([1, 2, 3, 4, 5, 6, 8, 10]), rng.choice([1, 2, 3, 4, 5, 6, 8, 10]); d = rng.choice([2, 4, 5, 10]); same = rng.choice([True, False])
        B = 2e-7 * (I1 - I2 if same else I1 + I2) / (d / 200) * 1e6; need(abs(B) > 0 and abs(abs(B) - round(abs(B))) < 1e-9)
        return dict(q=f'Two long parallel wires {d} cm apart carry {I1} A and {I2} A in {"the same direction" if same else "opposite directions"}. The magnitude of the field midway between them is ____ μT.', o=None, a=round(abs(B)),
                    sol=['Between the wires: same directions → fields oppose; opposite directions → fields add.', f'2 × 10^{{−7}} × \\f{{{"|" + str(I1) + " − " + str(I2) + "|" if same else str(I1) + " + " + str(I2)}}}{{{d / 200}}} = {round(abs(B))} μT.'], p=dict(t=t, I1=I1, I2=I2, d=d / 100, same=same))
    if t == 'f_poly':
        n = rng.choice([3, 4, 6]); a = rng.choice([0.1, 0.2, 0.5, 1.0]); I = rng.choice([1, 2, 5, 10]); dd = a / (2 * math.tan(pi / n)); B = n * mu0 * I / (4 * pi * dd) * 2 * math.sin(pi / n)
        o, an = opts(rng, B, (2, 0.5, math.sqrt(2), 1 / math.sqrt(2), 1.5))
        shape = {3: 'an equilateral triangle', 4: 'a square', 6: 'a regular hexagon'}[n]
        return dict(q=f'A current of {I} A flows round {shape} of side {a} m. The field at its centre (in T) is', o=o, a=an,
                    sol=['Each side: \\f{μ_{0}I}{4πd}(sin α + sin α) with d its distance from the centre.', f'Add all {n} sides: {nf(B, 3)} T.'], p=dict(t=t, n=n, a=a, I=I))
    R1, R2 = rng.choice([(1, 2), (2, 3), (1, 3), (2, 5), (3, 4)]); I = rng.choice([2, 4, 6, 12]); same = rng.choice([True, False]); s = R1 * R2   # radii in units of π m
    B = mu0 * I / 4 * (1 / (R1 * pi) + (1 if same else -1) / (R2 * pi)); val = abs(B) / 1e-7; need(abs(val - round(val, 6)) < 1e-9 and val > 0)
    o, an = opts(rng, val, (2, 0.5, 1.5, 3, 4))
    return dict(q=f'A loop is made of two semicircles of radii {R1}π m and {R2}π m with a common centre O, joined by straight pieces along the diameter. The semicircles are traversed in {"the same" if same else "opposite"} rotational sense and the current is {I} A. The field at O is B × 10^{{−7}} T, where B =', o=o, a=an,
                sol=['Straight pieces through O give no field; each semicircle gives \\f{μ_{0}I}{4R}.', f'B = \\f{{μ_{{0}}I}}{{4}}(\\f{{1}}{{R_{{1}}}} {"+" if same else "−"} \\f{{1}}{{R_{{2}}}}) = {nf(val, 3)} × 10^{{−7}} T.'], p=dict(t='f_arc', R1=R1 * pi, R2=R2 * pi, I=I, same=same))

def g_force(rng):
    t = rng.choice(['v_wire', 'v_qvb', 'v_rad', 'v_per', 'v_cross', 'v_par', 'v_pitch'])
    if t == 'v_wire':
        B, I, L = rng.choice([0.1, 0.2, 0.25, 0.5, 0.8]), rng.choice([2, 4, 5, 8, 10]), rng.choice([5, 10, 20, 25, 50]); ang = rng.choice([90, 30, 60, 90]); F = B * I * L / 100 * math.sin(math.radians(ang)) * 1000
        o, an = opts(rng, F, (2, 0.5, math.sqrt(3), 1 / math.sqrt(3), 1.5))
        return dict(q=f'A {L} cm wire carrying {I} A lies at {ang}° to a uniform field of {B} T. The force on it (in mN) is', o=o, a=an, sol=['F = BIL sin θ.', f'= {nf(F, 3)} mN.'], p=dict(t=t, B=B, I=I, L=L / 100, ang=ang))
    if t == 'v_qvb':
        v, B = rng.choice([(1, 2, 3), (2, -1, 1), (3, 0, 4), (1, 1, 0), (2, 3, -1)]), rng.choice([(0, 0, 1), (1, 2, 0), (2, 3, -5), (0, 1, 1), (1, -1, 2)]); q = rng.choice([1, 2, 5]); F = cross(v, B); s = sum(x * x for x in F) * q * q; need(s)
        return dict(q=f'A {q} μC charge moves with v⃗ = ({v[0]}, {v[1]}, {v[2]}) m/s in B⃗ = ({B[0]}, {B[1]}, {B[2]}) T. If the force has magnitude √{{α}} × 10^{{−6}} N, α = ____.', o=None, a=s,
                    sol=['F⃗ = qv⃗ × B⃗.', f'v⃗ × B⃗ = ({F[0]}, {F[1]}, {F[2]}) → α = {s}.'], p=dict(t=t, v=v, B=B, q=q))
    if t == 'v_rad':
        part = rng.choice(['proton', 'electron', 'alpha particle']); m, q = {'proton': (1.67e-27, 1.6e-19), 'electron': (9.1e-31, 1.6e-19), 'alpha particle': (6.68e-27, 3.2e-19)}[part]
        v, B = rng.choice([1e5, 2e5, 5e5, 1e6, 3e6]), rng.choice([0.01, 0.05, 0.1, 0.5, 1.0]); r = m * v / (q * B)
        o, an = opts(rng, r)
        return dict(q=f'A {part} moves at {nf(v, 2)} m/s perpendicular to a {B} T field. The radius of its path (in m) is', o=o, a=an, sol=['r = \\f{mv}{qB}.', f'= {nf(r, 3)} m.'], p=dict(t=t, m=m, q=q, v=v, B=B))
    if t == 'v_per':
        m, q, B = rng.choice([1, 2, 4, 5, 10]) * 1e-6, rng.choice([1, 2, 5]) * pi * 1e-6, rng.choice([0.1, 0.2, 0.5, 1.0]); T = 2 * pi * m / (q * B)
        o, an = opts(rng, T)
        return dict(q=f'A particle of mass {nf(m * 1e6, 3)} mg and charge {nf(q * 1e6 / pi, 3)}π μC moves in a {B} T field. Its period of revolution (in s) is', o=o, a=an, sol=['T = \\f{2πm}{qB}, independent of speed.', f'= {nf(T, 3)} s.'], p=dict(t=t, m=m, q=q, B=B))
    if t == 'v_cross':
        v, B = rng.choice([1, 2, 3, 4, 5]) * 1e5, rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]); E = v * B; val = E / 1e3; need(abs(val - round(val)) < 1e-9)
        return dict(q=f'A charge moves undeflected at {nf(v, 2)} m/s through crossed fields with B = {B} T. The electric field is ____ kN/C.', o=None, a=round(val), sol=['Balance: qE = qvB → E = vB.', f'= {round(val)} × 10^{{3}} N/C.'], p=dict(t=t, v=v, B=B))
    if t == 'v_par':
        I1, I2, d = rng.choice([2, 5, 10, 20]), rng.choice([2, 5, 10, 20]), rng.choice([1, 2, 5, 10]); f = 2e-7 * I1 * I2 / (d / 100) * 1e6; need(abs(f - round(f)) < 1e-9)
        return dict(q=f'Two long parallel wires {d} cm apart carry {I1} A and {I2} A. The force per metre between them is ____ μN/m.', o=None, a=round(f), sol=['\\f{F}{L} = \\f{μ_{0}I_{1}I_{2}}{2πd}.', f'= {round(f)} μN/m.'], p=dict(t=t, I1=I1, I2=I2, d=d / 100))
    m, q, B = rng.choice([1, 2, 5]) * 1e-6, rng.choice([1, 2, 5]) * pi * 1e-6, rng.choice([0.1, 0.2, 0.5]); vpar = rng.choice([1, 2, 4, 5]) * 1e-2; n = rng.randint(1, 6); T = 2 * pi * m / (q * B); dist = n * T * vpar
    need(abs(dist * 100 - round(dist * 100)) < 1e-9)
    return dict(q=f'A particle (mass {nf(m * 1e6, 2)} mg, charge {nf(q * 1e6 / pi, 2)}π μC) moves in a uniform field B = {B} T with velocity component {nf(vpar * 100, 2)} cm/s along B (and some perpendicular component). How far (in cm) along B does it go in {n} revolution{"s" if n > 1 else ""}?', o=None, a=round(dist * 100),
                sol=['Pitch = v_{∥}T with T = \\f{2πm}{qB}.', f'T = {nf(T, 3)} s → {n} × T × v_{{∥}} = {round(dist * 100)} cm.'], p=dict(t='v_pitch', m=m, q=q, B=B, vpar=vpar, n=n))

def g_moment(rng):
    t = rng.choice(['m_tor', 'm_work', 'm_pe', 'm_nia', 'm_dip', 'm_H', 'm_chi'])
    if t == 'm_tor':
        N, I, R, B = rng.choice([10, 50, 100, 125, 200]), rng.choice([1, 2, 5]), rng.choice([1, 2, 5]), rng.choice([0.1, 0.2, 0.4, 0.5]); ang = rng.choice([30, 60, 90]); tau = N * I * pi * (R / 100) ** 2 * B * math.sin(math.radians(ang))
        o, an = opts(rng, tau, (2, 0.5, math.sqrt(3), 1 / math.sqrt(3), 1.5))
        return dict(q=f'A circular coil of {N} turns, radius {R} cm carries {I} A in a {B} T field; its axis makes {ang}° with the field. The torque on it (in N m) is', o=o, a=an, sol=['τ = NIAB sin θ (θ between the axis/moment and B).', f'= {nf(tau, 3)} N m.'], p=dict(t=t, N=N, I=I, R=R / 100, B=B, ang=ang))
    if t == 'm_work':
        m, B = rng.choice([0.2, 0.5, 1.0, 2.0, 4.0]), rng.choice([0.02, 0.04, 0.05, 0.08, 0.1]); a1, a2 = rng.choice([(0, 180), (0, 90), (0, 60), (60, 180), (90, 180)]); W = m * B * (math.cos(math.radians(a1)) - math.cos(math.radians(a2)))
        o, an = opts(rng, W, (2, 0.5, 1.5, 3))
        return dict(q=f'A magnet of moment {m} A m^{{2}} in a {B} T field is turned from θ = {a1}° to θ = {a2}°. The work done (in J) is', o=o, a=an, sol=['W = mB(cos θ_{1} − cos θ_{2}).', f'= {nf(W, 3)} J.'], p=dict(t=t, m=m, B=B, a1=a1, a2=a2))
    if t == 'm_pe':
        tau, ang = rng.choice([4, 8, 10, 16, 20, 40]), rng.choice([30, 60]); mB = tau / math.sin(math.radians(ang)); U = -mB * math.cos(math.radians(ang))
        o, an = opts(rng, U, (-1, 2, 0.5, math.sqrt(3), 1 / math.sqrt(3)))
        return dict(q=f'A magnetic dipole feels a torque of {tau} N m when its moment makes {ang}° with a uniform field. Its potential energy (in J) is', o=o, a=an, sol=['τ = mB sin θ gives mB; U = −mB cos θ.', f'U = {nf(U, 3)} J.'], p=dict(t=t, tau=tau, ang=ang))
    if t == 'm_nia':
        N, I, a, b = rng.choice([1, 10, 20, 50]), rng.choice([1, 2, 5]), rng.choice([2, 5, 10, 20]), rng.choice([2, 5, 10]); m = N * I * a * b / 1e4
        o, an = opts(rng, m)
        return dict(q=f'A rectangular coil of {N} turns, {a} cm × {b} cm, carries {I} A. Its magnetic moment (in A m^{{2}}) is', o=o, a=an, sol=['m = NIA.', f'= {nf(m, 3)} A m^{{2}}.'], p=dict(t=t, N=N, I=I, A=a * b / 1e4))
    if t == 'm_dip':
        m, d = rng.choice([1, 2, 5, 10]), rng.choice([5, 10, 20]); where = rng.choice(['axial', 'equatorial']); B = 1e-7 * m * (2 if where == 'axial' else 1) / (d / 100) ** 3
        o, an = opts(rng, B, (2, 0.5, 4, 0.25))
        return dict(q=f'A short magnet of moment {m} A m^{{2}}. The field at {d} cm from it on its {where} line (in T) is', o=o, a=an, sol=['Axial: \\f{μ_{0}}{4π}\\f{2m}{d^{3}}; equatorial: \\f{μ_{0}}{4π}\\f{m}{d^{3}}.', f'= {nf(B, 3)} T.'], p=dict(t=t, m=m, d=d / 100, where=where))
    if t == 'm_H':
        B, mr = rng.choice([0.5, 1.0, 1.5, 2.0]), rng.choice([100, 200, 400, 500, 1000]); H = B / (mr * mu0)
        o, an = opts(rng, H)
        return dict(q=f'Inside a solenoid with a core of relative permeability {mr}, B = {B} T. The magnetic intensity H (in A/m) is', o=o, a=an, sol=['H = \\f{B}{μ_{r}μ_{0}}.', f'= {nf(H, 3)} A/m.'], p=dict(t=t, B=B, mr=mr))
    chi = rng.choice([1.2e-5, 2.3e-5, -1.6e-5, 8e-6, 3e-4]); pct = chi * 100
    o, an = opts(rng, pct, (2, 0.5, 10, 0.1, -1))
    return dict(q=f'A solenoid\'s core space is filled with a material of susceptibility {nf(chi, 2)}. The percentage change in B is', o=o, a=an, sol=['B ∝ μ_{r} = 1 + χ.', f'Change = χ × 100% = {nf(pct, 3)} %.'], p=dict(t='m_chi', chi=chi))

def g_galv(rng):
    t = rng.choice(['g_shunt', 'g_series', 'g_k', 'g_vs', 'g_ratio'])
    if t == 'g_shunt':
        G, Ig, I = rng.choice([10, 20, 30, 50, 100]), rng.choice([1, 2, 5, 10, 20]) * 1e-3, rng.choice([1, 2, 3, 5, 10]); S = Ig * G / (I - Ig)
        o, an = opts(rng, S, (2, 0.5, 10, 0.1))
        return dict(q=f'A galvanometer of {G} Ω gives full deflection at {nf(Ig * 1e3, 3)} mA. The shunt needed to read up to {I} A (in Ω) is', o=o, a=an, sol=['S = \\f{I_{g}G}{I − I_{g}}.', f'= {nf(S, 3)} Ω.'], p=dict(t=t, G=G, Ig=Ig, I=I))
    if t == 'g_series':
        G, Ig, V = rng.choice([10, 20, 50, 100]), rng.choice([1, 2, 5, 10]) * 1e-3, rng.choice([1, 5, 10, 20, 50, 100]); R = V / Ig - G; need(R > 0)
        return dict(q=f'A galvanometer of {G} Ω gives full deflection at {nf(Ig * 1e3, 3)} mA. The series resistance to read up to {V} V is ____ Ω.', o=None, a=round(R), sol=['R = \\f{V}{I_{g}} − G.', f'= {round(R)} Ω.'], p=dict(t=t, G=G, Ig=Ig, V=V))
    if t == 'g_k':
        N, A, B, I, th = rng.choice([50, 100, 200]), rng.choice([1, 2, 4, 5]), rng.choice([0.01, 0.02, 0.05, 0.1]), rng.choice([1, 2, 5, 10]), rng.choice([0.05, 0.1, 0.2, 0.5]); k = N * A * 1e-4 * B * I * 1e-3 / th
        o, an = opts(rng, k)
        return dict(q=f'A galvanometer coil has {N} turns of area {A} cm^{{2}} in a {B} T radial field. A current of {I} mA turns it through {th} rad. The torsional constant (in N m/rad) is', o=o, a=an, sol=['NIAB = kθ.', f'k = {nf(k, 3)} N m/rad.'], p=dict(t=t, N=N, A=A * 1e-4, B=B, I=I * 1e-3, th=th))
    if t == 'g_vs':
        N1, N2 = rng.choice([10, 15, 20, 30]), rng.choice([10, 21, 25, 40]); A1, A2 = rng.choice([1.8, 3.6, 2.0, 4.0]), rng.choice([1.8, 3.6, 2.0, 4.0]); B1, B2 = rng.choice([0.25, 0.5]), rng.choice([0.25, 0.5]); R1, R2 = rng.choice([5, 7, 10]), rng.choice([5, 7, 10])
        which = rng.choice(['current', 'voltage']); r = (N1 * A1 * B1 / (N2 * A2 * B2)) * ((R2 / R1) if which == 'voltage' else 1)
        o, an = opts(rng, r, (2, 0.5, R1 / R2, R2 / R1, 1.5))
        return dict(q=f'Coils M_{{1}} (N = {N1}, A = {A1} × 10^{{−3}} m^{{2}}, B = {B1} T, R = {R1} Ω) and M_{{2}} (N = {N2}, A = {A2} × 10^{{−3}} m^{{2}}, B = {B2} T, R = {R2} Ω) have equal torsional constants. The ratio of their {which} sensitivities (M_{{1}} : M_{{2}}) is', o=o, a=an,
                    sol=['Current sensitivity \\f{NBA}{k}; voltage sensitivity \\f{NBA}{kR}.', f'Ratio = {nf(r, 3)}.'], p=dict(t=t, s=(N1, A1, B1, R1, N2, A2, B2, R2), which=which))
    S, a, b = rng.choice([2, 4, 6, 8, 12, 24]), rng.choice([20, 25, 30, 40, 50]), rng.choice([5, 10]); need(a > b); G = S * (a / b - 1)
    return dict(q=f'A galvanometer\'s deflection falls from {a} to {b} divisions when a {S} Ω shunt is connected. Its resistance is ____ Ω.', o=None, a=round(G) if abs(G - round(G)) < 1e-9 else need(False),
                sol=['The galvanometer now carries the fraction \\f{S}{S + G} of the current.', f'\\f{{{S}}}{{{S} + G}} = \\f{{{b}}}{{{a}}} → G = {round(G)} Ω.'], p=dict(t='g_ratio', S=S, a=a, b=b))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(field=g_field, force=g_force, moment=g_moment, galv=g_galv).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = num(R) if isinstance(R, str) else R
    if t == 'f_wire': return close(V, longwire(p['I'], p['d']) * 1e6, 1e-3)
    if t == 'f_loop': return close(V, p['N'] * nrm(bs(ring(p['R']), p['I'], (0, 0, 0), 2)))
    if t == 'f_sol':   # Ampère: B L = μ0 μr (n L) I for a rectangular loop of length L inside
        Lr = 0.37; return close(V, mu0 * p['mr'] * (p['n'] * Lr) * p['I'] / Lr)
    if t == 'f_axis':
        B0 = nrm(bs(ring(p['R']), 1, (0, 0, 0), 2)); Bx = nrm(bs(ring(p['R']), 1, (0, 0, p['x']), 2)); return close(V, p['B0'] * Bx / B0)
    if t == 'f_two':
        d = p['d']; B1 = longwire(p['I1'], d / 2); B2 = longwire(p['I2'], d / 2); return close(V, abs(B1 - B2 if p['same'] else B1 + B2) * 1e6, 1e-3)
    if t == 'f_poly':
        n, a = p['n'], p['a']; Rv = a / (2 * math.sin(pi / n)); pts = [(Rv * math.cos(2 * pi * k / n), Rv * math.sin(2 * pi * k / n), 0) for k in range(n + 1)]; return close(V, nrm(bs(pts, p['I'], (0, 0, 0), 400)))
    if t == 'f_arc':
        R1, R2, I = p['R1'], p['R2'], p['I']; s1 = [(R1 * math.cos(pi * k / 400), R1 * math.sin(pi * k / 400), 0) for k in range(401)]
        s2 = [(R2 * math.cos(pi + pi * k / 400), R2 * math.sin(pi + pi * k / 400), 0) for k in range(401)] if p['same'] else [(R2 * math.cos(-pi * k / 400), R2 * math.sin(-pi * k / 400), 0) for k in range(401)]
        B = [a + b for a, b in zip(bs(s1, I, (0, 0, 0), 2), bs(s2, I, (0, 0, 0), 2))]; return close(V * 1e-7, nrm(B))
    if t == 'v_wire':
        th = math.radians(p['ang']); dl = (math.cos(th), math.sin(th), 0); F = cross([p['I'] * p['L'] * c for c in dl], (p['B'], 0, 0)); return close(V, nrm(F) * 1000)
    if t == 'v_qvb': F = cross(p['v'], p['B']); return V == sum(x * x for x in F) * p['q'] ** 2
    if t in ('v_rad', 'v_per', 'v_pitch'):
        m, q, B = p['m'], p['q'], p['B']; v = (p.get('v', 1.0), 0.0, p.get('vpar', 0.0)); x, y, z = 0.0, 0.0, 0.0; vx, vy, vz = v
        Tg = 2 * pi * m / (q * B); n = 4000; dt = Tg / n; xs = []
        for _ in range(n * (p['n'] if t == 'v_pitch' else 1)):
            ax, ay = q / m * vy * B, -q / m * vx * B; vxm, vym = vx + ax * dt / 2, vy + ay * dt / 2; ax2, ay2 = q / m * vym * B, -q / m * vxm * B
            x, y, z = x + vxm * dt, y + vym * dt, z + vz * dt; vx, vy = vx + ax2 * dt, vy + ay2 * dt; xs.append((x, y))
        if t == 'v_rad': d = max(math.hypot(a, b) for a, b in xs); return close(V, d / 2)
        if t == 'v_per': return close(V, Tg) and math.hypot(x, y) < 1e-3 * max(1e-30, max(math.hypot(a, b) for a, b in xs))
        return close(V / 100, z, 1e-6)
    if t == 'v_cross':
        v, B = p['v'], p['B']; E = V * 1e3; F = [0, E, 0]; mag = cross((v, 0, 0), (0, 0, B)); return abs(F[1] + mag[1]) < 1e-9 * E
    if t == 'v_par':   # force on wire 2 from the field of wire 1, by I L × B
        B1 = longwire(p['I1'], p['d']); return close(V, p['I2'] * B1 * 1e6, 1e-3)
    if t == 'm_tor':
        th = math.radians(p['ang']); m = p['N'] * p['I'] * pi * p['R'] ** 2; return close(V, nrm(cross((m, 0, 0), (p['B'] * math.cos(th), p['B'] * math.sin(th), 0))))
    if t == 'm_work':   # integrate the torque against the angle
        m, B = p['m'], p['B']; a1, a2 = math.radians(p['a1']), math.radians(p['a2']); n = 20000
        W = sum(m * B * math.sin(a1 + (a2 - a1) * (k + 0.5) / n) * (a2 - a1) / n for k in range(n)); return close(V, W)
    if t == 'm_pe':
        th = math.radians(p['ang']); mB = p['tau'] / math.sin(th)   # U(θ) = U(0) + ∫ τ dθ with U(0) = −mB
        return close(V, -mB + sum(mB * math.sin(th * (k + 0.5) / 4000) * th / 4000 for k in range(4000)))
    if t == 'm_nia': return close(V, p['N'] * p['I'] * p['A'])
    if t == 'm_dip':   # field of a tiny current loop of that moment, by Biot–Savart
        a = 1e-3 * p['d']; I = p['m'] / (pi * a * a); P0 = (0, 0, p['d']) if p['where'] == 'axial' else (p['d'], 0, 0)
        return close(V, nrm(bs(ring(a, 720), I, P0, 1)), 5e-3)
    if t == 'm_H': return close(V, p['B'] / (p['mr'] * mu0))
    if t == 'm_chi': return close(V, ((1 + p['chi']) - 1) / 1 * 100)
    if t == 'g_shunt':   # bisection on S for: current through G at full scale
        lo, hi = 1e-9, 1e4; f = lambda S: p['I'] * S / (S + p['G']) - p['Ig']
        for _ in range(200):
            m = (lo + hi) / 2
            if f(m) > 0: hi = m
            else: lo = m
        return close(V, lo)
    if t == 'g_series': return abs(p['Ig'] * (p['G'] + V) - p['V']) < 1e-9
    if t == 'g_k': return close(V, p['N'] * p['A'] * p['B'] * p['I'] / p['th'])
    if t == 'g_vs':
        N1, A1, B1, R1, N2, A2, B2, R2 = p['s']; c1, c2 = N1 * A1 * B1, N2 * A2 * B2; r = c1 / c2 if p['which'] == 'current' else (c1 / R1) / (c2 / R2); return close(V, r)
    if t == 'g_ratio': return abs(p['S'] / (p['S'] + V) - p['b'] / p['a']) < 1e-12
    raise KeyError(t)
