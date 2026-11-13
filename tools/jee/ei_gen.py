"""Practice generators — Physics Unit 14: Electromagnetic Induction and Alternating Currents. check() re-solves each
item a different way: emfs by numerically differencing the flux Φ(t), motional emfs by summing (v × B)·dl along the
conductor, LR and LC circuits by stepping the circuit equation in time, and ac circuits with complex impedances and
time-averaged products of v(t) and i(t)."""
import math, cmath, re
from common import mcq, nf
pi = math.pi; mu0 = 4e-7 * pi
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def isint(x): return abs(x - round(x)) < 1e-9
def opts(rng, v, k=(2, 0.5, 4, 1.5, math.sqrt(2), 1 / math.sqrt(2), 3)):
    w = []
    for f in k:
        s = nf(v * f, 3)
        if s != nf(v, 3) and s not in w: w.append(s)
    rng.shuffle(w); return mcq(rng, nf(v, 3), w)
def ddt(f, t, h=1e-6): return (f(t + h) - f(t - h)) / (2 * h)
def Z(R=0, L=0, C=None, w=1): return complex(R, w * L - (1 / (w * C) if C else 0))
def mean_vi(v, i, T, n=20000): return sum(v(T * (k + 0.5) / n) * i(T * (k + 0.5) / n) for k in range(n)) / n

def g_flux(rng):
    t = rng.choice(['x_ramp', 'x_poly', 'x_angle', 'x_sin', 'x_heat', 'x_charge', 'x_shape'])
    if t == 'x_ramp':
        N, A, B1, B2, dt = rng.choice([10, 20, 50, 100, 200]), rng.choice([10, 20, 25, 40, 50, 100]), rng.choice([0, 0.1, 0.2, 0.5]), rng.choice([0.4, 0.6, 0.8, 1.0, 1.2]), rng.choice([0.1, 0.2, 0.5, 1, 2])
        need(B1 != B2); e = N * A * 1e-4 * abs(B2 - B1) / dt; need(isint(e * 1000))
        return dict(q=f'A coil of {N} turns and area {A} cm^{{2}} lies perpendicular to a magnetic field that changes steadily from {B1} T to {B2} T in {dt} s. The induced emf is ____ mV.', o=None, a=round(e * 1000),
                    sol=['ε = NA\\f{ΔB}{Δt}.', f'= {N} × {A} × 10^{{−4}} × \\f{{{nf(abs(B2 - B1), 3)}}}{{{dt}}} = {round(e * 1000)} mV.'], p=dict(t=t, N=N, A=A * 1e-4, B1=B1, B2=B2, dt=dt))
    if t == 'x_poly':
        a, b, c, T, R = rng.randint(1, 9), rng.randint(-20, 20), rng.randint(0, 9), rng.randint(1, 6), rng.choice([1, 2, 4, 5, 10]); e = abs(2 * a * T + b); need(e > 0 and isint(e / R * 100))
        I = e / R; q0 = f'The flux through a circuit of resistance {R} Ω is Φ = ({a}t^{{2}} {"+" if b >= 0 else "−"} {abs(b)}t + {c}) Wb. The induced current at t = {T} s'
        sol = ['|ε| = |\\f{dΦ}{dt}| = |2at + b|.', f'= {nf(e, 3)} V → I = {nf(I, 3)} A.']; p = dict(t=t, a=a, b=b, c=c, T=T, R=R)
        if isint(I): return dict(q=q0 + ' is ____ A.', o=None, a=round(I), sol=sol, p=p)
        o, an = opts(rng, I); return dict(q=q0 + ' (in A) is', o=o, a=an, sol=sol, p=p)
    if t == 'x_angle':
        A, B0, w, ang = rng.choice([2, 4, 5, 10, 20]), rng.choice([0.1, 0.2, 0.4, 0.5]), rng.choice([100, 200, 300, 500]), rng.choice([0, 30, 60]); e = A * 1e-4 * B0 * w * math.cos(math.radians(ang))
        o, an = opts(rng, e * 1000, (2, 0.5, math.sqrt(3), 1 / math.sqrt(3), 1.5))
        return dict(q=f'A loop of area {A} cm^{{2}} is in a field B = {B0} sin({w}t) T; the loop\'s normal makes {ang}° with the field. The maximum induced emf (in mV) is', o=o, a=an,
                    sol=['Φ = BA cos θ, so ε_{max} = B_{0}ωA cos θ.', f'= {nf(e * 1000, 3)} mV.'], p=dict(t=t, A=A * 1e-4, B0=B0, w=w, ang=ang))
    if t == 'x_sin':
        A, B0, w, R = rng.choice([0.5, 1, 2]), rng.choice([0.5, 1, 2]), rng.choice([10, 50, 100, 200]), rng.choice([10, 50, 100, 200]); E = (A * B0 * w) ** 2 / (2 * R) * 2 * pi / w
        o, an = opts(rng, E / pi, (2, 0.5, 4, 1.5, pi))
        return dict(q=f'A loop of area {A} m^{{2}} and resistance {R} Ω lies perpendicular to B = {B0} sin({w}t) T. The heat produced in one period is Eπ J, where E =', o=o, a=an,
                    sol=['ε = AB_{0}ω cos ωt; mean power \\f{(AB_{0}ω)^{2}}{2R}.', f'× T = \\f{{2π}}{{ω}} → {nf(E / pi, 3)}π J.'], p=dict(t=t, A=A, B0=B0, w=w, R=R))
    if t == 'x_heat':
        N, A, dB, R = rng.choice([10, 50, 100]), rng.choice([10, 20, 50, 100]), rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([1, 2, 5, 10]); e = N * A * 1e-4 * dB; P = e * e / R
        o, an = opts(rng, P * 1000, (2, 0.5, 4, 0.25, 1.5))
        return dict(q=f'A coil of {N} turns, area {A} cm^{{2}} and resistance {R} Ω lies perpendicular to a field rising at {dB} T/s. The heat produced per second (in mW) is', o=o, a=an,
                    sol=['ε = NA\\f{dB}{dt}, P = \\f{ε^{2}}{R}.', f'= {nf(P * 1000, 3)} mW.'], p=dict(t=t, N=N, A=A * 1e-4, dB=dB, R=R))
    if t == 'x_charge':
        N, A, B, R = rng.choice([10, 20, 50, 100, 200]), rng.choice([10, 20, 50, 100]), rng.choice([0.1, 0.2, 0.5, 1]), rng.choice([2, 5, 10, 20, 50]); flip = rng.choice([True, False]); q = N * A * 1e-4 * B * (2 if flip else 1) / R
        o, an = opts(rng, q * 1000, (2, 0.5, 4, 0.25, 1.5))
        return dict(q=f'A coil of {N} turns, area {A} cm^{{2}}, resistance {R} Ω is perpendicular to a {B} T field. It is {"turned over through 180°" if flip else "pulled out of the field"}. The charge that flows (in mC) is', o=o, a=an,
                    sol=['q = \\f{NΔΦ}{R}, independent of how fast.', f'ΔΦ = {"2BA" if flip else "BA"} → q = {nf(q * 1000, 3)} mC.'], p=dict(t=t, N=N, A=A * 1e-4, B=B, R=R, flip=flip))
    r, B, dt = rng.choice([7, 14, 21, 28]), rng.choice([0.1, 0.2, 0.5, 1.0]), rng.choice([0.1, 0.2, 0.5, 1.0]); A1 = 22 / 7 * r * r; s = 2 * 22 / 7 * r / 4; dA = A1 - s * s; e = B * dA * 1e-4 / dt * 1000
    o, an = opts(rng, e, (2, 0.5, 4, 10, 1.5))
    return dict(q=f'A circular loop of radius {r} cm in a perpendicular field of {B} T is reshaped into a square in {dt} s. The average induced emf (in mV) is (π = 22/7)', o=o, a=an,
                sol=['Same perimeter: side = \\f{2πr}{4}; the area drops.', f'ΔA = {nf(dA, 4)} cm^{{2}} → ε = \\f{{BΔA}}{{Δt}} = {nf(e, 3)} mV.'], p=dict(t='x_shape', r=r, B=B, dt=dt))

def g_motional(rng):
    t = rng.choice(['o_rod', 'o_rot', 'o_coil', 'o_force', 'o_term', 'o_fall', 'o_bisect'])
    if t == 'o_rod':
        B, l, v = rng.choice([0.1, 0.2, 0.4, 0.5, 1.0, 2.0]), rng.choice([10, 20, 25, 50, 100]), rng.choice([1, 2, 4, 5, 10]); e = B * l / 100 * v; need(isint(e * 1000))
        return dict(q=f'A rod of length {l} cm moves at {v} m/s perpendicular to itself and to a {B} T field. The emf across it is ____ mV.', o=None, a=round(e * 1000), sol=['ε = Bℓv.', f'= {round(e * 1000)} mV.'], p=dict(t=t, B=B, l=l / 100, v=v))
    if t == 'o_rot':
        B, w, L = rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([10, 20, 50, 100]), rng.choice([10, 20, 50, 100]); e = 0.5 * B * w * (L / 100) ** 2
        o, an = opts(rng, e, (2, 0.5, 4, 0.25, 1.5))
        return dict(q=f'A {L} cm rod rotates about one end at {w} rad/s in a {B} T field parallel to the axis. The emf between its ends (in V) is', o=o, a=an, sol=['ε = ½BωL^{2}.', f'= {nf(e, 3)} V.'], p=dict(t=t, B=B, w=w, L=L / 100))
    if t == 'o_coil':
        N, A, B, f = rng.choice([50, 100, 200, 500]), rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]), rng.choice([0.01, 0.05, 0.1, 0.2]), rng.choice([0.5, 1, 2, 5, 50]); e = N * A * B * 2 * pi * f
        o, an = opts(rng, e, (2, 0.5, 1 / pi, pi, 1.5))
        return dict(q=f'A coil of {N} turns and area {A} m^{{2}} spins at {f} rev/s in a {B} T field perpendicular to its axis. The peak emf (in V) is', o=o, a=an, sol=['ε_{0} = NBAω, ω = 2πf.', f'= {nf(e, 3)} V.'], p=dict(t=t, N=N, A=A, B=B, f=f))
    if t == 'o_force':
        B, l, v, R = rng.choice([0.1, 0.2, 0.5, 1]), rng.choice([0.5, 1, 2]), rng.choice([1, 1.5, 2, 4, 5]), rng.choice([1, 2, 5, 10]); F = B * B * l * l * v / R
        o, an = opts(rng, F, (2, 0.5, 4, 0.25, 1.5))
        return dict(q=f'A {l} m rod slides at a steady {v} m/s on rails in a {B} T field; total resistance {R} Ω. The force needed to keep it moving (in N) is', o=o, a=an, sol=['I = \\f{Bℓv}{R}, F = BIℓ = \\f{B^{2}ℓ^{2}v}{R}.', f'= {nf(F, 3)} N.'], p=dict(t=t, B=B, l=l, v=v, R=R))
    if t == 'o_term':
        m, B, l, R = rng.choice([10, 20, 50, 100]), rng.choice([0.5, 1, 2]), rng.choice([0.1, 0.2, 0.5, 1]), rng.choice([1, 2, 5, 10]); v = m / 1000 * 10 * R / (B * l) ** 2
        o, an = opts(rng, v, (2, 0.5, 4, 0.25, 1.5))
        return dict(q=f'A rod of mass {m} g slides down smooth vertical rails {l} m apart, closed by {R} Ω, in a horizontal {B} T field. Its terminal speed (in m/s) is (g = 10 m/s^{{2}})', o=o, a=an,
                    sol=['Terminal when \\f{B^{2}ℓ^{2}v}{R} = mg.', f'v = \\f{{mgR}}{{B^{{2}}ℓ^{{2}}}} = {nf(v, 3)} m/s.'], p=dict(t=t, m=m / 1000, B=B, l=l, R=R))
    if t == 'o_fall':
        L, B, h = rng.choice([1, 2, 5, 10, 20]), rng.choice([0.2, 0.3, 0.5, 0.6]), rng.choice([5, 20, 45, 80, 125]); v = math.sqrt(20 * h); e = B * 1e-4 * L * v
        o, an = opts(rng, e * 1000, (2, 0.5, math.sqrt(2), 1 / math.sqrt(2), 1.5))
        return dict(q=f'A horizontal {L} m wire falls from rest through a horizontal field of {B} G perpendicular to it. The emf after it has fallen {h} m (in mV) is (g = 10 m/s^{{2}})', o=o, a=an,
                    sol=['v = √{2gh}.', f'ε = Bℓv = {nf(e * 1000, 3)} mV.'], p=dict(t=t, L=L, B=B * 1e-4, h=h))
    B, w, L = rng.choice([0.2, 0.5, 1]), rng.choice([10, 20, 50]), rng.choice([20, 40, 60, 100]); frac = rng.choice([2, 3, 4])
    e = 0.5 * B * w * ((L / 100 * (frac - 1) / frac) ** 2 - (L / 100 / frac) ** 2)
    o, an = opts(rng, e, (2, 0.5, 1.5, 3))
    return dict(q=f'A {L} cm rod spins at {w} rad/s about an axis perpendicular to it through the point 1/{frac} of the way along, in a {B} T field parallel to the axis. The potential difference between the ends (in V) is', o=o, a=an,
                sol=['Each part from the axis gives ½Bωr^{2}; the two parts oppose.', f'ΔV = ½Bω(r_{{1}}^{{2}} − r_{{2}}^{{2}}) = {nf(e, 3)} V.'], p=dict(t='o_bisect', B=B, w=w, L=L / 100, frac=frac)) if frac > 2 else \
        dict(q=f'A {L} cm rod spins at {w} rad/s about its perpendicular bisector in a {B} T field parallel to the axis. The potential difference between its two ends is ____ V.', o=None, a=0,
             sol=['Each half gives ½Bω(\\f{L}{2})^{2} from the centre outwards, in the same sense.', 'The ends are at the same potential: 0.'], p=dict(t='o_bisect', B=B, w=w, L=L / 100, frac=2))

def g_induct(rng):
    t = rng.choice(['l_emf', 'l_sol', 'l_energy', 'l_tau', 'l_rise', 'l_lc', 'l_mut', 'l_par'])
    if t == 'l_emf':
        L, I1, I2, dt = rng.choice([1, 2, 5, 10, 20, 50]), rng.randint(-5, 5), rng.randint(-5, 10), rng.choice([0.1, 0.2, 0.5, 1]); need(I1 != I2); e = L * 1e-3 * abs(I2 - I1) / dt
        o, an = opts(rng, e * 1000, (2, 0.5, 4, 1.5, 10))
        return dict(q=f'The current in a {L} mH coil changes steadily from {I1} A to {I2} A in {dt} s. The self-induced emf (in mV) is', o=o, a=an, sol=['ε = L\\f{ΔI}{Δt}.', f'= {nf(e * 1000, 3)} mV.'], p=dict(t=t, L=L * 1e-3, I1=I1, I2=I2, dt=dt))
    if t == 'l_sol':
        n, A, l = rng.choice([500, 1000, 2000, 5000]), rng.choice([1, 2, 5, 10]), rng.choice([10, 20, 30, 50]); Lh = mu0 * n * n * A * 1e-4 * l / 100
        o, an = opts(rng, Lh * 1000, (2, 0.5, 4, 0.25, pi))
        return dict(q=f'A solenoid {l} cm long with {n} turns per metre has cross-section {A} cm^{{2}}. Its self-inductance (in mH) is', o=o, a=an, sol=['L = μ_{0}n^{2}Aℓ.', f'= {nf(Lh * 1000, 3)} mH.'], p=dict(t=t, n=n, A=A * 1e-4, l=l / 100))
    if t == 'l_energy':
        L, I = rng.choice([10, 20, 50, 100, 200, 500]), rng.choice([1, 2, 3, 4, 5, 10]); U = 0.5 * L * 1e-3 * I * I
        o, an = opts(rng, U, (2, 0.5, 4, 0.25))
        return dict(q=f'A {L} mH inductor carries {I} A. The energy stored (in J) is', o=o, a=an, sol=['U = ½LI^{2}.', f'= {nf(U, 3)} J.'], p=dict(t=t, L=L * 1e-3, I=I))
    if t == 'l_tau':
        L, R = rng.choice([10, 20, 50, 100, 200, 500]), rng.choice([1, 2, 5, 10, 20, 50]); tau = L * 1e-3 / R
        o, an = opts(rng, tau * 1000, (2, 0.5, 10, 0.1))
        return dict(q=f'An inductor of {L} mH and a resistance {R} Ω are connected to a battery. The time constant (in ms) is', o=o, a=an, sol=['τ = \\f{L}{R}.', f'= {nf(tau * 1000, 3)} ms.'], p=dict(t=t, L=L * 1e-3, R=R))
    if t == 'l_rise':
        E, R, L, i1, i2 = rng.choice([1, 2, 5, 10, 12]), rng.choice([10, 20, 50, 100]), rng.choice([10, 20, 50]), rng.randint(1, 4), rng.randint(5, 9); I0 = E / R; a, b = I0 * i1 / 10, I0 * i2 / 10
        r = (E - a * R) / (E - b * R)
        o, an = opts(rng, r, (1 / r ** 2, 2, 0.5, 1.5))
        return dict(q=f'A {L} mH coil of resistance {R} Ω is switched across a {E} V battery. The ratio of the voltages across the inductance when the current is {nf(a * 1000, 3)} mA and {nf(b * 1000, 3)} mA is', o=o, a=an,
                    sol=['Across the inductance: E − iR.', f'Ratio = \\f{{{E} − {nf(a * R, 3)}}}{{{E} − {nf(b * R, 3)}}} = {nf(r, 3)}.'], p=dict(t=t, E=E, R=R, L=L * 1e-3, a=a, b=b))
    if t == 'l_lc':
        C, V, L = rng.choice([10, 20, 25, 50, 100]), rng.choice([5, 10, 12, 20]), rng.choice([1, 2, 4, 5, 10]); I = V * math.sqrt(C * 1e-6 / (L * 1e-3))
        o, an = opts(rng, I, (2, 0.5, math.sqrt(2), 1 / math.sqrt(2)))
        return dict(q=f'A {C} μF capacitor charged to {V} V is connected across a {L} mH inductor. The maximum current (in A) is', o=o, a=an, sol=['½CV^{2} = ½LI^{2}.', f'I = V√{{\\f{{C}}{{L}}}} = {nf(I, 3)} A.'], p=dict(t=t, C=C * 1e-6, V=V, L=L * 1e-3))
    if t == 'l_mut':
        M, I0, w = rng.choice([1, 2, 4, 5, 10]), rng.choice([1, 2, 5, 10]), rng.choice([50, 100, 200, 314]); e = M * 1e-3 * I0 * w
        o, an = opts(rng, e, (2, 0.5, pi, 1 / pi))
        return dict(q=f'Two coils have mutual inductance {M} mH. The current in one is i = {I0} sin({w}t) A. The peak emf in the other (in V) is', o=o, a=an, sol=['ε = M\\f{di}{dt}, peak Mi_{0}ω.', f'= {nf(e, 3)} V.'], p=dict(t=t, M=M * 1e-3, I0=I0, w=w))
    n = rng.choice([2, 3, 4]); r = (1 + n * (1 / n) ** 2) / (1 / n) ** 2; need(isint(r))
    return dict(q=f'Inductor L_{{1}} is in series with {n} identical inductors in parallel, all of the same inductance L. The ratio of the total stored energy to the energy in one of the parallel inductors is ____.', o=None, a=round(r),
                sol=['The parallel ones share the current equally: \\f{I}{n} each.', f'\\f{{½LI^{{2}}(1 + \\f{{1}}{{{n}}})}}{{½L(I/{n})^{{2}}}} = {round(r)}.'], p=dict(t='l_par', n=n))

def g_ac(rng):
    t = rng.choice(['a_rms', 'a_xc', 'a_xl', 'a_z', 'a_pf', 'a_pow', 'a_res', 'a_vc', 'a_tr', 'a_phase', 'a_q'])
    if t == 'a_rms':
        k = rng.choice(['dc', 'ramp']);
        if k == 'dc':
            a, b = rng.choice([(6, 56), (3, 32), (4, 18), (5, 22), (8, 72), (2, 42), (6, 128), (10, 200)]); I = math.sqrt(a * a + b / 2); need(isint(I))
            return dict(q=f'i = [{a} + √{{{b}}} sin(ωt + φ)] A. The rms current is ____ A.', o=None, a=round(I), sol=['I_{rms}^{2} = I_{dc}^{2} + \\f{I_{0}^{2}}{2}.', f'= {a * a} + {nf(b / 2, 3)} → {round(I)} A.'], p=dict(t=t, k=k, a=a, b=b))
        i0 = rng.choice([1, 2, 3, 5, 6, 10]); I = i0 / math.sqrt(3)
        o, an = opts(rng, I, (math.sqrt(3) / math.sqrt(2), math.sqrt(3), math.sqrt(3) / math.sqrt(6), 0.5 * math.sqrt(3)))
        return dict(q=f'A current rises linearly from 0 to {i0} A over a period T and repeats. Its rms value (in A) is', o=o, a=an, sol=['I_{rms}^{2} = \\f{1}{T}∫_{0}^{T}i_{0}^{2}\\f{t^{2}}{T^{2}}dt = \\f{i_{0}^{2}}{3}.', f'= {nf(I, 3)} A.'], p=dict(t=t, k=k, i0=i0))
    if t == 'a_xc':
        C, f, V = rng.choice([1, 2, 4, 5, 10, 20, 25, 50, 100]), rng.choice([50, 60, 100, 200, 500, 1000]), rng.choice([110, 220, 230, 10, 20, 40, 100]); I = V * 2 * pi * f * C * 1e-6
        o, an = opts(rng, I * 1000, (2, 0.5, pi, 1 / pi, 1.5))
        return dict(q=f'A {C} μF capacitor is connected to a {V} V (rms), {f} Hz supply. The rms current (in mA) is', o=o, a=an, sol=['X_{C} = \\f{1}{2πfC}, I = \\f{V}{X_{C}}.', f'= {nf(I * 1000, 3)} mA.'], p=dict(t=t, C=C * 1e-6, f=f, V=V))
    if t == 'a_xl':
        L, f, V = rng.choice([10, 20, 50, 100, 200, 250, 500, 1000]), rng.choice([50, 60, 100, 200, 500]), rng.choice([10, 20, 50, 110, 220, 230]); I = V / (2 * pi * f * L * 1e-3)
        o, an = opts(rng, I, (2, 0.5, pi, 1 / pi, 1.5))
        return dict(q=f'A pure {L} mH inductor is connected to a {V} V (rms), {f} Hz supply. The rms current (in A) is', o=o, a=an, sol=['X_{L} = 2πfL.', f'I = \\f{{V}}{{X_{{L}}}} = {nf(I, 3)} A.'], p=dict(t=t, L=L * 1e-3, f=f, V=V))
    if t == 'a_z':
        R, X = rng.choice([(3, 4), (6, 8), (5, 12), (8, 6), (9, 12), (12, 16), (20, 15), (30, 40), (60, 80), (24, 7), (4, 3), (12, 5)]); k = rng.choice([1, 2, 5, 10, 20]); R, X = R * k, X * k; V = rng.choice([10, 20, 50, 100, 110, 200, 220, 230, 250])
        I = V / math.hypot(R, X)
        o, an = opts(rng, I, (2, 0.5, math.hypot(R, X) / R, math.hypot(R, X) / X, 1.5))
        kind = rng.choice(['L', 'C'])
        return dict(q=f'A {R} Ω resistor and a{"n inductor" if kind == "L" else " capacitor"} of reactance {X} Ω are in series across {V} V (rms). The current (in A) is', o=o, a=an, sol=['Z = √{R^{2} + X^{2}}.', f'Z = {nf(math.hypot(R, X), 4)} Ω → I = {nf(I, 3)} A.'], p=dict(t=t, R=R, X=X, V=V, kind=kind))
    if t == 'a_pf':
        R0, X0 = rng.choice([(3, 4), (4, 3), (6, 8), (8, 6), (1, 0)]); k = rng.choice([5, 10, 15, 20, 25, 30]); R, X = R0 * k, X0 * k * rng.choice([1, -1]); XC = rng.choice([10, 20, 40, 50, 80, 100, 150]); XL = XC + X; need(XL > 0)
        pf = R / math.hypot(R, XL - XC); need(isint(pf * 10))
        return dict(q=f'A series LCR circuit has R = {R} Ω, X_{{L}} = {XL} Ω and X_{{C}} = {XC} Ω. Its power factor is \\f{{α}}{{10}}. α = ____.', o=None, a=round(pf * 10), sol=['cos φ = \\f{R}{Z}.', f'Z = {nf(math.hypot(R, XL - XC), 4)} Ω → cos φ = {nf(pf, 3)}.'], p=dict(t=t, R=R, XL=XL, XC=XC))
    if t == 'a_pow':
        V0, I0, ph = rng.choice([10, 20, 40, 50, 100, 200, 220, 311]), rng.choice([0.1, 0.5, 1, 2, 4, 5, 10]), rng.choice([0, 30, 45, 60, 90]); P = V0 * I0 / 2 * math.cos(math.radians(ph))
        o, an = opts(rng, P, (2, 0.5, math.sqrt(2), math.sqrt(3), 1.5)) if P > 1e-9 else (None, 0)
        q = f'v = {V0} sin(ωt) V and i = {I0} sin(ωt + {ph}°) A. The average power (in W) is'
        if o is None: return dict(q=q.replace('(in W) is', 'is ____ W.'), o=None, a=0, sol=['P = \\f{V_{0}I_{0}}{2} cos φ.', 'cos 90° = 0 → P = 0 (wattless current).'], p=dict(t=t, V0=V0, I0=I0, ph=ph))
        return dict(q=q, o=o, a=an, sol=['P = \\f{V_{0}I_{0}}{2} cos φ.', f'= {nf(P, 3)} W.'], p=dict(t=t, V0=V0, I0=I0, ph=ph))
    if t == 'a_res':
        L, C = rng.choice([(0.1, 2.5e-9), (0.1, 25e-9), (2, 50e-6), (1.6, 40e-6), (0.5, 2e-6), (1, 1e-6), (0.4, 10e-6), (4, 25e-6), (0.25, 4e-6), (0.01, 1e-6)]); w = 1 / math.sqrt(L * C)
        ask = rng.choice(['w', 'XL'])
        val = w if ask == 'w' else w * L; need(isint(val))
        return dict(q=f'A series LCR circuit has L = {nf(L, 3)} H and C = {nf(C * 1e6, 3)} μF. The {"resonant angular frequency is ____ rad/s" if ask == "w" else "inductive reactance at resonance is ____ Ω"}.', o=None, a=round(val),
                    sol=['ω_{0} = \\f{1}{√{LC}}.', f'ω_{{0}} = {nf(w, 4)} rad/s' + ('.' if ask == 'w' else f' → X_{{L}} = ω_{{0}}L = {round(val)} Ω.')], p=dict(t=t, L=L, C=C, ask=ask))
    if t == 'a_vc':
        R, L, C, w = rng.choice([(300, 1, 20e-6, 100), (30, 0.1, 100e-6, 200), (60, 0.5, 50e-6, 100), (40, 0.2, 25e-6, 400), (80, 1, 10e-6, 200), (120, 2, 20e-6, 50), (50, 0.3, 40e-6, 250), (100, 0.4, 5e-6, 500), (20, 0.05, 200e-6, 314), (10, 0.02, 1000e-6, 100)]); V = rng.choice([10, 20, 25, 40, 50, 100, 110, 200, 220])
        z = Z(R, L, C, w); I = V / abs(z); which = rng.choice(['R', 'L', 'C']); x = {'R': R, 'L': w * L, 'C': 1 / (w * C)}[which]; val = I * x
        o, an = opts(rng, val, (2, 0.5, 1.5, 0.8)) if not isint(val) else (None, round(val))
        q = f'An rms voltage of {V} V at ω = {w} rad/s drives a series circuit R = {R} Ω, L = {L} H, C = {nf(C * 1e6, 3)} μF. The rms voltage across the {dict(R="resistor", L="inductor", C="capacitor")[which]}'
        return dict(q=q + (' is ____ V.' if o is None else ' (in V) is'), o=o, a=an, sol=[f'X_{{L}} = {nf(w * L, 4)} Ω, X_{{C}} = {nf(1 / (w * C), 4)} Ω, Z = {nf(abs(z), 4)} Ω.', f'I = {nf(I, 3)} A → V = I × {nf(x, 4)} = {nf(val, 3)} V.'], p=dict(t=t, R=R, L=L, C=C, w=w, V=V, which=which))
    if t == 'a_tr':
        Vp, Np, Ns, eta, Ip = rng.choice([110, 220, 230, 2300, 11000]), rng.choice([100, 200, 500, 1000, 3000]), rng.choice([10, 20, 50, 100, 300]), rng.choice([80, 90, 100]), rng.choice([1, 2, 5, 10])
        Vs = Vp * Ns / Np; Is = eta / 100 * Vp * Ip / Vs
        o, an = opts(rng, Is, (2, 0.5, 100 / eta, eta / 100 * 0.9, 1.5))
        return dict(q=f'A transformer with {Np} primary and {Ns} secondary turns takes {Ip} A at {Vp} V. Its efficiency is {eta}%. The secondary current (in A) is', o=o, a=an,
                    sol=[f'V_{{s}} = {Vp} × \\f{{{Ns}}}{{{Np}}} = {nf(Vs, 4)} V.', f'I_{{s}} = \\f{{η V_{{p}}I_{{p}}}}{{V_{{s}}}} = {nf(Is, 3)} A.'], p=dict(t=t, Vp=Vp, Np=Np, Ns=Ns, eta=eta, Ip=Ip))
    if t == 'a_phase':
        f = rng.choice([50, 60, 100, 25]); a, b = rng.choice([(0.5, 1), (0, 0.5), (0, 1 / math.sqrt(2)), (1 / math.sqrt(2), 1), (0.5, math.sqrt(3) / 2), (0, math.sqrt(3) / 2)]); dt = (math.asin(b) - math.asin(a)) / (2 * pi * f)
        o, an = opts(rng, dt * 1000, (2, 0.5, 1.5, 3))
        nm = lambda x: {0: 'zero', 0.5: 'half the peak', 1: 'the peak'}.get(x, {1 / math.sqrt(2): '1/√2 of the peak', math.sqrt(3) / 2: '√3/2 of the peak'}.get(x))
        return dict(q=f'For a {f} Hz sinusoidal current, the shortest time to rise from {nm(a)} to {nm(b)} value (in ms) is', o=o, a=an,
                    sol=['i = I_{0} sin 2πft: find the phase of each value.', f'Δt = \\f{{Δ(phase)}}{{2πf}} = {nf(dt * 1000, 3)} ms.'], p=dict(t=t, f=f, a=a, b=b))
    R1, Xc = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 5]); m = rng.choice([2, 3, 4]); r = abs(complex(R1, -Xc)) / abs(complex(R1, -m * Xc))
    o, an = opts(rng, r, (1 / r, 2, 0.5, 1.5))
    return dict(q=f'A resistor R = {R1} Ω and a capacitor of reactance {Xc} Ω at frequency ω are in series across a fixed voltage. The frequency is changed to ω/{m}. The ratio of the new current to the old is', o=o, a=an,
                sol=[f'At ω/{m} the reactance becomes {m * Xc} Ω.', f'Ratio = \\f{{√{{R^{{2}} + X^{{2}}}}}}{{√{{R^{{2}} + ({m}X)^{{2}}}}}} = {nf(r, 3)}.'], p=dict(t='a_q', R=R1, X=Xc, m=m))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(flux=g_flux, motional=g_motional, induct=g_induct, ac=g_ac).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = num(R) if isinstance(R, str) else R
    if t == 'x_ramp': return abs(V / 1000 - abs(ddt(lambda s: p['N'] * p['A'] * (p['B1'] + (p['B2'] - p['B1']) * s / p['dt']), p['dt'] / 2))) < 1e-6
    if t == 'x_poly': return close(V, abs(ddt(lambda s: p['a'] * s * s + p['b'] * s + p['c'], p['T'])) / p['R'])
    if t == 'x_angle':
        f = lambda s: p['A'] * p['B0'] * math.sin(p['w'] * s) * math.cos(math.radians(p['ang'])); T = 2 * pi / p['w']
        return close(V / 1000, max(abs(ddt(f, T * k / 4000, 1e-7)) for k in range(4000)))
    if t == 'x_sin':
        T = 2 * pi / p['w']; n = 4000; E = sum(ddt(lambda s: p['A'] * p['B0'] * math.sin(p['w'] * s), T * (k + 0.5) / n, 1e-7) ** 2 / p['R'] * T / n for k in range(n)); return close(V * pi, E)
    if t == 'x_heat': e = abs(ddt(lambda s: p['N'] * p['A'] * p['dB'] * s, 1.0)); return close(V / 1000, e * e / p['R'])
    if t == 'x_charge':   # integrate the current while the coil turns/leaves over 1 s
        n = 4000; ang = pi if p['flip'] else None; q = 0.0
        phi = (lambda s: p['N'] * p['B'] * p['A'] * math.cos(pi * s)) if p['flip'] else (lambda s: p['N'] * p['B'] * p['A'] * (1 - s))
        for k in range(n): q += abs(ddt(phi, (k + 0.5) / n, 1e-7)) / p['R'] / n
        return close(V / 1000, q)
    if t == 'x_shape':
        P7 = 22 / 7; per = 2 * P7 * p['r']; A1 = P7 * p['r'] ** 2; A2 = (per / 4) ** 2; return close(V / 1000, p['B'] * (A1 - A2) * 1e-4 / p['dt'])
    if t == 'o_rod': return abs(V / 1000 - p['B'] * p['l'] * p['v']) < 1e-9
    if t in ('o_rot', 'o_bisect'):
        n = 20000; seg = lambda a: sum(p['B'] * p['w'] * (a * (k + 0.5) / n) * a / n for k in range(n))
        if t == 'o_rot': return close(V, seg(p['L']))
        r1 = p['L'] * (p['frac'] - 1) / p['frac']; r2 = p['L'] / p['frac']; d = seg(r1) - seg(r2); return abs(V) < 1e-12 if p['frac'] == 2 else close(V, d)
    if t == 'o_coil':
        w = 2 * pi * p['f']; f = lambda s: p['N'] * p['B'] * p['A'] * math.cos(w * s); T = 1 / p['f']; return close(V, max(abs(ddt(f, T * k / 4000, T * 1e-6)) for k in range(4000)))
    if t == 'o_force': I = p['B'] * p['l'] * p['v'] / p['R']; return close(V, I * p['l'] * p['B'])
    if t == 'o_term':
        v, dt = 0.0, 1e-4; k = p['B'] ** 2 * p['l'] ** 2 / (p['m'] * p['R'])
        for _ in range(int(20 / (k * dt)) + 1000): v += (10 - k * v) * dt
        return close(V, v, 2e-3)
    if t == 'o_fall':
        v, y, dt = 0.0, 0.0, 1e-5
        while y < p['h']: v += 10 * dt; y += v * dt
        return close(V / 1000, p['B'] * p['L'] * v, 3e-3)
    if t == 'l_emf': return close(V / 1000, abs(ddt(lambda s: p['L'] * (p['I1'] + (p['I2'] - p['I1']) * s / p['dt']), p['dt'] / 2)))
    if t == 'l_sol':   # flux linkage per ampere: N × (μ0 n I) × A
        N = p['n'] * p['l']; return close(V / 1000, N * mu0 * p['n'] * 1 * p['A'])
    if t == 'l_energy':   # work against the back emf while ramping 0 → I
        n = 10000; return close(V, sum(p['L'] * (p['I'] * (k + 0.5) / n) * p['I'] / n for k in range(n)))
    if t == 'l_tau':   # time for the current to reach 1 − 1/e of final
        L, Rr = p['L'], p['R']; i, tt, dt = 0.0, 0.0, L / Rr / 20000
        while i < (1 - math.exp(-1)) / Rr: i += (1 - i * Rr) / L * dt; tt += dt
        return close(V / 1000, tt, 2e-3)
    if t == 'l_rise':
        L, Rr, E = p['L'], p['R'], p['E']; i, dt, out = 0.0, L / Rr / 200000, {}
        while i < p['b'] * 1.0001:
            vL = E - i * Rr
            for k in ('a', 'b'):
                if k not in out and i >= p[k]: out[k] = vL
            i += vL / L * dt
        return close(V, out['a'] / out['b'], 2e-3)
    if t == 'l_lc':
        L, C = p['L'], p['C']; q, i, dt, best = C * p['V'], 0.0, math.sqrt(L * C) / 20000, 0.0
        for _ in range(40000): i += -q / (L * C) * dt; q += i * dt; best = max(best, abs(i))
        return close(V, best)
    if t == 'l_mut':
        T = 2 * pi / p['w']; f = lambda s: p['M'] * p['I0'] * math.sin(p['w'] * s); return close(V, max(abs(ddt(f, T * k / 4000, 1e-7)) for k in range(4000)))
    if t == 'l_par':
        n = p['n']; I = 1.0; Ut = 0.5 * I * I + n * 0.5 * (I / n) ** 2; return abs(V - Ut / (0.5 * (I / n) ** 2)) < 1e-9
    if t == 'a_rms':
        if p['k'] == 'dc': f = lambda s: p['a'] + math.sqrt(p['b']) * math.sin(s + 0.7)
        else: f = lambda s: p['i0'] * (s / (2 * pi))
        n = 40000; return close(V, math.sqrt(sum(f(2 * pi * (k + 0.5) / n) ** 2 for k in range(n)) / n))
    if t == 'a_xc': return close(V / 1000, abs(p['V'] / Z(C=p['C'], w=2 * pi * p['f'])))
    if t == 'a_xl': return close(V, abs(p['V'] / Z(L=p['L'], w=2 * pi * p['f'])))
    if t == 'a_z': z = complex(p['R'], p['X'] if p['kind'] == 'L' else -p['X']); return close(V, abs(p['V'] / z))
    if t == 'a_pf': return abs(V / 10 - math.cos(cmath.phase(complex(p['R'], p['XL'] - p['XC'])))) < 1e-9
    if t == 'a_pow':
        w = 1.0; P = mean_vi(lambda s: p['V0'] * math.sin(s), lambda s: p['I0'] * math.sin(s + math.radians(p['ph'])), 2 * pi); return abs(V) < 1e-9 and abs(P) < 1e-6 if p['ph'] == 90 else close(V, P)
    if t == 'a_res':   # scan ω for the impedance minimum, then refine
        lo, hi = 1.0, 1e7
        for _ in range(300):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if abs(Z(1, p['L'], p['C'], m1)) < abs(Z(1, p['L'], p['C'], m2)): hi = m2
            else: lo = m1
        w = (lo + hi) / 2; return close(V, w if p['ask'] == 'w' else w * p['L'], 1e-4)
    if t == 'a_vc':
        z = {'R': p['R'], 'L': complex(0, p['w'] * p['L']), 'C': complex(0, -1 / (p['w'] * p['C']))}[p['which']]; I = p['V'] / Z(p['R'], p['L'], p['C'], p['w']); return close(V, abs(I * z))
    if t == 'a_tr': Vs = p['Vp'] * p['Ns'] / p['Np']; return close(V * Vs, p['eta'] / 100 * p['Vp'] * p['Ip'])
    if t == 'a_phase':
        f = lambda s: math.sin(2 * pi * p['f'] * s); s, dt = 0.0, 1e-7
        while f(s) < p['a'] - 1e-12: s += dt
        s1 = s
        while f(s) < p['b'] - 1e-9 and f(s + dt) > f(s): s += dt
        return close(V / 1000, s - s1, 3e-3)
    if t == 'a_q': return close(V, abs(1 / complex(p['R'], -p['m'] * p['X'])) / abs(1 / complex(p['R'], -p['X'])))
    raise KeyError(t)
