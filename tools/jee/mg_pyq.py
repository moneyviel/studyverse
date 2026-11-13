"""Real JEE Main questions — Physics Unit 13: Magnetic Effects of Current and Magnetism. Our own solutions; chk
re-solves each one from the raw data in SI units — fields by summing Biot–Savart contributions of each straight
or curved piece (numerically where a piece is curved), forces from qv × B and I L × B, and meter conversions from
the shunt/series resistance condition. Skipped: induction items (filed in Unit 14), a bonus item, and items whose
printed figure we could not read reliably."""
import math
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
mu0 = 4e-7 * math.pi; pi = math.pi; e = 1.6e-19; me = 9.1e-31; mp = 1.67e-27
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)   # relative match
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(sum(x * x for x in a))
def bs_path(pts, I, P0, n=4000):
    """Biot–Savart field at P0 of current I along a polyline/curve given as a list of points (numerical)"""
    B = [0.0, 0.0, 0.0]
    for a, b in zip(pts, pts[1:]):
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            p0 = [a[i] + (b[i] - a[i]) * t0 for i in range(3)]; p1 = [a[i] + (b[i] - a[i]) * t1 for i in range(3)]
            dl = [p1[i] - p0[i] for i in range(3)]; m = [(p0[i] + p1[i]) / 2 for i in range(3)]; r = [P0[i] - m[i] for i in range(3)]; R = nrm(r)
            c = cross(dl, r); B = [B[i] + mu0 * I / (4 * pi) * c[i] / R ** 3 for i in range(3)]
    return B
def arc(R, a0, a1, n=400, c=(0, 0, 0)): return [(c[0] + R * math.cos(a0 + (a1 - a0) * k / n), c[1] + R * math.sin(a0 + (a1 - a0) * k / n), c[2]) for k in range(n + 1)]

# ---------- sheet 1
add(('2024', 'Feb', '2024-02-01', 1), 'galv', 'A galvanometer has a resistance of 50 Ω and it allows maximum current of 5 mA. It can be converted into voltmeter to measure upto 100 V by connecting in series a resistor of resistance', ['5975 Ω', '20050 Ω', '19950 Ω', '19500 Ω'], 3,
    lambda: P4([5975, 20050, 19950, 19500], 100 / 5e-3 - 50), ['Total resistance for full scale: \\f{100}{5 × 10^{−3}} = 20000 Ω.', 'Series resistor = 20000 − 50 = 19950 Ω.'], 'galv', 1)
def _hex():
    s = 4 * pi / 6; I = 4 * pi * math.sqrt(3); Rv = s / (2 * math.sin(pi / 6))   # circumradius
    pts = [(Rv * math.cos(k * pi / 3), Rv * math.sin(k * pi / 3), 0) for k in range(7)]; return round(nrm(bs_path(pts, I, (0, 0, 0), 2000)) / 1e-7, 3)
add(('2024', 'Feb', '2024-02-01', 1), 'field', 'A regular polygon of 6 sides is formed by bending a wire of length 4π meter. If an electric current of 4π√{3} A is flowing through the sides of the polygon, the magnetic field at the centre of the polygon would be x × 10^{−7} T. The value of x is ______.', None, 72,
    lambda: round(_hex()), ['Side = \\f{2π}{3} m; distance of each side from the centre d = \\f{s}{2 tan 30°} = \\f{π}{√{3}} m.', 'Each side: B = \\f{μ_{0}I}{4πd}(sin 30° + sin 30°) = \\f{μ_{0}I}{4πd}.', 'Total 6·10^{−7}·\\f{4π√{3}}{π/√{3}} = 72 × 10^{−7} T.'], 'field', 2)
add(('2024', 'Feb', '2024-02-01', 2), 'galv', 'A moving coil galvanometer has 100 turns and each turn has an area of 2.0 cm^{2}. The magnetic field produced by the magnet is 0.01 T and the deflection in the coil is 0.05 radian when a current of 10 mA is passed through it. The torsional constant of the suspension wire is x × 10^{−5} N m/rad. The value of x is ______.', None, 4,
    lambda: round(100 * 2e-4 * 0.01 * 10e-3 / 0.05 / 1e-5), ['Balance: NIAB = kθ.', 'k = \\f{100 × 10^{−2} × 2 × 10^{−4} × 0.01}{0.05} = 4 × 10^{−5} N m/rad.'], 'galv', 1)

# ---------- sheet 2
def _r10():
    R, x = 4.0, 3.0; B1 = nrm(bs_path(arc(R, 0, 2 * pi, 2000), 1, (0, 0, 0), 4)); B2 = nrm(bs_path(arc(R, 0, 2 * pi, 2000), 1, (0, 0, x), 4)); r = B2 / B1
    return P4([25 / 16, 16 / 25, 4 / 5, 64 / 125], r, 1e-4)
add(('2025', 'Apr', '2025-04-02', 1), 'field', 'Let B_{1} be the magnitude of magnetic field at center of a circular coil of radius R carrying current I. Let B_{2} be the magnitude of magnetic field at an axial distance x from the center. For x : R = 3 : 4, \\f{B_{2}}{B_{1}} is :', ['25 : 16', '16 : 25', '4 : 5', '64 : 125'], 4,
    _r10, ['B_{1} = \\f{μ_{0}I}{2R}, B_{2} = \\f{μ_{0}IR^{2}}{2(R^{2} + x^{2})^{3/2}}.', '\\f{B_{2}}{B_{1}} = \\f{R^{3}}{(R^{2} + x^{2})^{3/2}} = \\f{64}{125}.'], 'field', 1)
def _chi():
    ops = [lambda mu, mr: mr + 1, lambda mu, mr: mr / mu0 + 1, lambda mu, mr: 1 - mr, lambda mu, mr: mr - 1]   # with μ/μ0 = μ_r
    M = mu0 * 1.0003; mr = M / mu0; chi = (M - mu0) / mu0   # χ from B = μ0(H + M), M = χH
    h = [i + 1 for i, f in enumerate(ops) if abs(f(M, mr) - chi) < 1e-12]; assert len(h) == 1; return h[0]
add(('2025', 'Apr', '2025-04-02', 1), 'moment', 'The relationship between the magnetic susceptibility (χ) and the magnetic permeability (μ) is given by : (μ_{0} is the permeability of free space and μ_{r} is relative permeability)', ['χ = μ_{r} + 1', 'χ = \\f{μ_{r}}{μ_{0}} + 1', 'χ = 1 − \\f{μ}{μ_{0}}', 'χ = \\f{μ}{μ_{0}} − 1'], 4,
    _chi, ['B = μ_{0}(H + M) = μ_{0}(1 + χ)H, so μ = μ_{0}(1 + χ).', 'χ = \\f{μ}{μ_{0}} − 1 = μ_{r} − 1.'], 'moment', 1)
def _vs13():
    v1 = 15 * 0.25 * 3.6e-3 / 5; v2 = 21 * 0.50 * 1.8e-3 / 7; return P4([0.5, 1 / 3, 1, 0.25], v1 / v2, 1e-9)
add(('2025', 'Apr', '2025-04-02', 2), 'galv', 'In a moving coil galvanometer, two moving coils M_{1} and M_{2} have the following particulars : R_{1} = 5 Ω, N_{1} = 15, A_{1} = 3.6 × 10^{−3} m^{2}, B_{1} = 0.25 T; R_{2} = 7 Ω, N_{2} = 21, A_{2} = 1.8 × 10^{−3} m^{2}, B_{2} = 0.50 T. Assuming that torsional constant of the springs are same for both coils, what will be the ratio of voltage sensitivity of M_{1} and M_{2} ?', ['1 : 2', '1 : 3', '1 : 1', '1 : 4'], 3,
    _vs13, ['Voltage sensitivity = \\f{NBA}{kR}.', 'M_{1}: \\f{15 × 0.25 × 3.6 × 10^{−3}}{5} = 2.7 × 10^{−3}; M_{2}: \\f{21 × 0.5 × 1.8 × 10^{−3}}{7} = 2.7 × 10^{−3}.', 'Ratio 1 : 1.'], 'galv', 1)
def _db14():
    q, m, B0, v = -1.0, 1.0, 2.0, (3.0, 0.0, 0.0); dt = 1e-4
    for _ in range(20000):   # RK2 on m dv/dt = q v × B
        a = [q / m * c for c in cross(v, (0, B0, 0))]; vm = [v[i] + a[i] * dt / 2 for i in range(3)]; a2 = [q / m * c for c in cross(vm, (0, B0, 0))]; v = tuple(v[i] + a2[i] * dt for i in range(3))
    return 1 if abs(nrm(v) - 3.0) < 1e-6 else 0
add(('2025', 'Apr', '2025-04-02', 2), 'force', 'An electron with mass m with an initial velocity (t = 0) v⃗ = v_{0}î (v_{0} > 0) enters a magnetic field B⃗ = B_{0}ĵ. If the initial de-Broglie wavelength at t = 0 is λ_{0} then its value after time t would be :', ['λ_{0}', '\\f{λ_{0}}{√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}}', '\\f{λ_{0}}{√{1 − \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}}', 'λ_{0}√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}'], 1,
    _db14, ['The magnetic force qv⃗ × B⃗ is always perpendicular to v⃗: it does no work, so speed (and momentum size) stays the same.', 'λ = \\f{h}{p} is unchanged: λ_{0}.'], 'force', 1)
def _u15():
    B, A, l = 0.7, 2e-3, 0.3; mu = 2 * mu0; U = B * B / (2 * mu) * A * l   # energy density B²/2μ
    return P4([B * B * A * l, B * B * A * l / (4 * mu0), B * B * A * l / mu0, B * B * A * l / (2 * mu0)], U, 1e-9)
add(('2025', 'Apr', '2025-04-02', 2), 'moment', 'A solenoid having area A and length l is filled with a material having relative permeability 2. The magnetic energy stored in the solenoid is:', ['B^{2}Al', '\\f{B^{2}Al}{4μ_{0}}', '\\f{B^{2}Al}{μ_{0}}', '\\f{B^{2}Al}{2μ_{0}}'], 2,
    _u15, ['Energy density in a medium = \\f{B^{2}}{2μ} with μ = 2μ_{0}.', 'U = \\f{B^{2}}{4μ_{0}}·Al.'], 'moment', 1)
def _k16():
    I, R1, R2 = 12, 6 * pi, 4 * pi
    outer = arc(R1, 0, pi, 3000); inner = list(reversed(arc(R2, 0, pi, 3000)))   # outer runs D → top → A (anticlockwise); inner runs B → top → C
    pts = outer + [(-R2, 0, 0)] + inner + [(R1, 0, 0)]
    return round(abs(bs_path(pts, I, (0, 0, 0), 1)[2]) / 1e-7, 3)
add(('2025', 'Apr', '2025-04-03', 1), 'field', 'A loop ABCDA, carrying current I = 12 A, is placed in a plane, consists of two semi-circular segments of radius R_{1} = 6π m and R_{2} = 4π m (the outer semicircle D → A and the inner semicircle B → C, joined by straight parts AB and CD along the diameter through the centre O). The magnitude of the resultant magnetic field at center O is k × 10^{−7} T. The value of k is ______. (Given μ_{0} = 4π × 10^{−7} T m A^{−1})', None, 1,
    lambda: round(_k16()), ['The straight parts AB and CD point at O: no field there.', 'The two semicircles are traversed in opposite senses: B = \\f{μ_{0}I}{4}(\\f{1}{R_{2}} − \\f{1}{R_{1}}).', '= 12π × 10^{−7}(\\f{1}{4π} − \\f{1}{6π}) = 1 × 10^{−7} T → k = 1.'], 'field', 2)

# ---------- sheet 3
add(('2025', 'Apr', '2025-04-03', 1), 'force', 'A 4.0 cm long straight wire carrying a current of 8 A is placed perpendicular to a uniform magnetic field of strength 0.15 T. The magnetic force on the wire is ______ mN.', None, 48,
    lambda: round(nrm(cross((0.04 * 8, 0, 0), (0, 0.15, 0))) * 1e3, 6), ['F = BIL sin 90° = 0.15 × 8 × 0.04 = 0.048 N = 48 mN.'], 'force', 1)
def _u18():
    mB = 80 * math.sqrt(3) / math.sin(pi / 3); return P4([-60, -40 * math.sqrt(3), 80, -80], -mB * math.cos(pi / 3), 1e-9)
add(('2025', 'Apr', '2025-04-03', 2), 'moment', 'A magnetic dipole experiences a torque of 80√{3} N m when placed in uniform magnetic field in such a way that dipole moment makes angle of 60° with magnetic field. The potential energy of the dipole is :', ['−60 J', '−40√{3} J', '80 J', '−80 J'], 4,
    _u18, ['τ = mB sin 60° = 80√{3} → mB = 160.', 'U = −mB cos 60° = −80 J.'], 'moment', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'moment', 'The magnetic moment of a bar magnet is 0.5 A m^{2}. It is suspended in a uniform magnetic field of 8 × 10^{−2} T. The work done in rotating it from its most stable to most unstable position is :', ['16 × 10^{−2} J', '8 × 10^{−2} J', '4 × 10^{−2} J', 'Zero'], 2,
    lambda: P4([16e-2, 8e-2, 4e-2, 0], (-0.5 * 0.08 * math.cos(pi)) - (-0.5 * 0.08 * math.cos(0)), 1e-9), ['U = −mB cos θ: from θ = 0 (−mB) to θ = 180° (+mB).', 'W = 2mB = 2 × 0.5 × 0.08 = 8 × 10^{−2} J.'], 'moment', 1)

# ---------- sheet 4
def wire(I, x0, P0):   # infinite straight wire along z at x = x0 (sum of a long finite segment)
    return seg_fine((x0, 0, -1e4), (x0, 0, 1e4), I, P0)
def _x24():
    r = 1.0; BA = nrm([a + b for a, b in zip(wire(1, 0, (-r, 0, 0)), wire(2, 2 * r, (-r, 0, 0)))]); BC = nrm([a + b for a, b in zip(wire(1, 0, (3 * r, 0, 0)), wire(2, 2 * r, (3 * r, 0, 0)))])
    return round(7 * BA / BC, 3)
add(('2024', 'Apr', '2024-04-04', 2), 'field', 'Two parallel long current carrying wires separated by a distance 2r carry currents I and 2I in the same direction. A is at distance r outside the first wire (on the far side from the second) and C is at distance r outside the second wire. The ratio of magnetic field at A to the magnetic field produced at C is \\f{x}{7}. The value of x is ______.', None, 5,
    lambda: round(_x24()), ['Outside both wires the two fields add (same current direction, same side).', 'B_{A} = \\f{μ_{0}}{2π}(\\f{I}{r} + \\f{2I}{3r}) = \\f{5}{3}\\f{μ_{0}I}{2πr}; B_{C} = \\f{μ_{0}}{2π}(\\f{I}{3r} + \\f{2I}{r}) = \\f{7}{3}\\f{μ_{0}I}{2πr}.', 'Ratio \\f{5}{7} → x = 5.'], 'field', 2)
def _s25():
    v = (0, 0, 2e6); B = (0, 0, 0.01); F = cross(v, B); return 2 if nrm(F) == 0 else 0
add(('2024', 'Apr', '2024-04-04', 1), 'force', 'An electron is projected with uniform velocity along the axis inside a current carrying long solenoid. Then :', ['the electron will be accelerated along the axis.', 'the electron will continue to move with uniform velocity along the axis of the solenoid.', 'the electron path will be circular about the axis.', 'the electron will experience a force at 45° to the axis and execute a helical path.'], 2,
    _s25, ['Inside the solenoid B⃗ is along the axis, parallel to v⃗.', 'F⃗ = qv⃗ × B⃗ = 0: uniform velocity.'], 'force', 1)
def _f27():
    I, a, x1, y1 = 0.5, 0.5, 2.0, 2.0; Bz = lambda x: 0.2 * (1 + 2 * x); Fx = Fy = 0.0; n = 2000
    sides = [((x1, y1), (x1 + a, y1)), ((x1 + a, y1), (x1 + a, y1 + a)), ((x1 + a, y1 + a), (x1, y1 + a)), ((x1, y1 + a), (x1, y1))]
    for (ax, ay), (bx, by) in sides:
        for k in range(n):
            mx, my = ax + (bx - ax) * (k + 0.5) / n, ay + (by - ay) * (k + 0.5) / n; dl = ((bx - ax) / n, (by - ay) / n, 0); f = cross(dl, (0, 0, Bz(mx))); Fx += I * f[0]; Fy += I * f[1]
    return round(math.hypot(Fx, Fy) * 1e3, 6)
add(('2024', 'Apr', '2024-04-04', 1), 'force', 'The magnetic field existing in a region is given by B⃗ = 0.2(1 + 2x)k̂ T. A square loop of edge 50 cm carrying 0.5 A current is placed in x − y plane with its edges parallel to the x − y axes, its lower-left corner at (2 m, 2 m). The magnitude of the net magnetic force experienced by the loop is ______ mN.', None, 50,
    lambda: round(_f27()), ['Forces on the top and bottom edges cancel (same field profile, opposite currents).', 'Left edge at x = 2: B = 1.0 T; right edge at x = 2.5: B = 1.2 T. Net F = IL(ΔB) = 0.5 × 0.5 × 0.2 = 0.05 N.', '50 mN.'], 'force', 2)
def _x28():
    Ig = 10 / (100 + 400); S = Ig * 100 / (10 - Ig); return P4([2, 800, 20, 200], S / 1e-2, 0.01)
add(('2024', 'Apr', '2024-04-05', 2), 'galv', 'A galvanometer of resistance 100 Ω when connected in series with 400 Ω measures a voltage of upto 10 V. The value of resistance required to convert the galvanometer into ammeter to read upto 10 A is x × 10^{−2} Ω. The value of x is :', ['2', '800', '20', '200'], 3,
    _x28, ['Full-scale current I_{g} = \\f{10}{500} = 0.02 A.', 'Shunt S = \\f{I_{g}G}{I − I_{g}} = \\f{0.02 × 100}{9.98} ≈ 0.2 Ω = 20 × 10^{−2} Ω.'], 'galv', 1)
def _f29():
    q, v, E, B = 2.0, (1.0, 2.0, 0.5), (0.3, -1.0, 2.0), (0.7, 0.1, -0.4); F2 = [q * c for c in cross(v, B)]   # Lorentz force on a test case
    ops2 = [None, None, [q * c for c in cross(v, B)], [q * c for c in cross(B, v)]]
    return 3 if all(abs(a - b) < 1e-12 for a, b in zip(ops2[2], F2)) and any(abs(a - b) > 1e-6 for a, b in zip(ops2[3], F2)) else 0
add(('2024', 'Apr', '2024-04-05', 2), 'force', 'The electrostatic force (F⃗_{1}) and magnetic force (F⃗_{2}) acting on a charge q moving with velocity v can be written :', ['F⃗_{1} = qV⃗·E⃗, F⃗_{2} = q(B⃗·V⃗)', 'F⃗_{1} = qB⃗, F⃗_{2} = q(B⃗ × V⃗)', 'F⃗_{1} = qE⃗, F⃗_{2} = q(V⃗ × B⃗)', 'F⃗_{1} = qE⃗, F⃗_{2} = q(B⃗ × V⃗)'], 3,
    _f29, ['Electric force qE⃗ (a vector, not a dot product).', 'Magnetic force q(v⃗ × B⃗) — order matters: B⃗ × v⃗ has the opposite sign.'], 'force', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'field', 'A solenoid of length 0.5 m has a radius of 1 cm and is made up of m number of turns. It carries a current of 5 A. If the magnitude of the magnetic field inside the solenoid is 6.28 × 10^{−3} T, then the value of m is ______.', None, 500,
    lambda: round(6.28e-3 * 0.5 / (mu0 * 5)), ['B = μ_{0}\\f{m}{L}I → m = \\f{BL}{μ_{0}I} = \\f{6.28 × 10^{−3} × 0.5}{4π × 10^{−7} × 5} = 500.'], 'field', 1)

# ---------- sheet 5
def _cx31():
    # Ampère: enclosed current for a loop of radius r in each region (inner radius a, outer shell b..c), currents +I and −I
    a, b, c, I = 1.0, 2.0, 2.5, 3.0
    enc = lambda r: I * min(r, a) ** 2 / a ** 2 - (I * (min(max(r, b), c) ** 2 - b * b) / (c * c - b * b) if r > b else 0)
    regions = {1: 2.2, 2: 1.5, 3: 4.0, 4: 0.5}; zero = [k for k, r in regions.items() if abs(enc(r)) < 1e-12]; assert len(zero) == 1; return zero[0]
add(('2024', 'Apr', '2024-04-05', 1), 'field', 'In a co-axial straight cable, the central conductor and the outer conductor carry equal currents in opposite directions. The magnetic field is zero.', ['inside the outer conductor', 'in between the two conductors', 'outside the cable', 'inside the inner conductor'], 3,
    _cx31, ['Ampère: B·2πr = μ_{0}I_{enclosed}.', 'Outside the cable the enclosed current is I − I = 0, so B = 0.'], 'field', 1)
def _b32():
    L = 1 * 10e-6 / 2e-6; B = 0.5 * 10 / (2 * L); return round(B / 1e-1, 6)
add(('2024', 'Apr', '2024-04-05', 1), 'force', 'A 2 A current carrying straight metal wire of resistance 1 Ω, resistivity 2 × 10^{−6} Ω m, area of cross-section 10 mm^{2} and mass 500 g is suspended horizontally in mid air by applying a uniform magnetic field B⃗. The magnitude of B is ______ × 10^{−1} T (given, g = 10 m/s^{2})', None, 5,
    _b32, ['Length from R = \\f{ρL}{A}: L = \\f{1 × 10 × 10^{−6}}{2 × 10^{−6}} = 5 m.', 'BIL = mg → B = \\f{0.5 × 10}{2 × 5} = 0.5 T = 5 × 10^{−1} T.'], 'force', 1)
def _k33():
    pts = [(2, 1.0), (4, 1.5), (6, 2.0)]   # (R, 1/θ) read from the graph
    slope = (pts[2][1] - pts[0][1]) / (pts[2][0] - pts[0][0]); E = 2; k = slope * E   # I = E/(R + G) = kθ ⇒ 1/θ = (k/E)(R + G)
    return round(k / 1e-1, 6)
add(('2024', 'Apr', '2024-04-05', 1), 'galv', 'In the experiment to determine the galvanometer resistance by half-deflection method, the plot of \\f{1}{θ} vs the resistance (R) of the resistance box is a straight line through (2 Ω, 1), (4 Ω, 1.5) and (6 Ω, 2) (1/θ in div^{−1}). The figure of merit of the galvanometer is ______ × 10^{−1} A/division. [The source has emf 2 V]', None, 5,
    _k33, ['I = \\f{E}{R + G} = kθ → \\f{1}{θ} = \\f{k}{E}(R + G), a straight line of slope \\f{k}{E}.', 'Slope = \\f{2 − 1}{6 − 2} = \\f{1}{4} → k = \\f{E}{4} = 0.5 A/div = 5 × 10^{−1}.'], 'galv', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'moment', 'A coil having 100 turns, area of 5 × 10^{−3} m^{2}, carrying current of 1 mA is placed in uniform magnetic field of 0.20 T such a way that plane of coil is perpendicular to the magnetic field. The work done in turning the coil through 90° is ______ μJ.', None, 100,
    lambda: round(((-100 * 1e-3 * 5e-3 * 0.2 * math.cos(pi / 2)) - (-100 * 1e-3 * 5e-3 * 0.2 * math.cos(0))) * 1e6, 6), ['Plane ⟂ B means m⃗ ∥ B⃗ (θ = 0). Turning to 90°: W = mB(cos 0 − cos 90°) = mB.', 'm = NIA = 100 × 10^{−3} × 5 × 10^{−3} = 5 × 10^{−4}; W = 5 × 10^{−4} × 0.2 = 10^{−4} J = 100 μJ.'], 'moment', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'field', 'An element Δl = Δx î is placed at the origin and carries a large current I = 10 A. The magnetic field on the y-axis at a distance of 0.5 m from the element Δx of 1 cm length is :', ['4 × 10^{−8} T', '8 × 10^{−8} T', '12 × 10^{−8} T', '10 × 10^{−8} T'], 1,
    lambda: P4([4e-8, 8e-8, 12e-8, 10e-8], nrm(bs_path([(-0.005, 0, 0), (0.005, 0, 0)], 10, (0, 0.5, 0), 200)), 1e-3),
    ['Biot–Savart: dB = \\f{μ_{0}}{4π}\\f{I dl sin 90°}{r^{2}}.', '10^{−7} × \\f{10 × 0.01}{0.25} = 4 × 10^{−8} T.'], 'field', 1)

# ---------- sheet 6
add(('2024', 'Apr', '2024-04-06', 1), 'moment', 'A circular coil having 200 turns, 2.5 × 10^{−4} m^{2} area and carrying 100 μA current is placed in a uniform magnetic field of 1 T. Initially the magnetic dipole moment (M⃗) was directed along B⃗. Amount of work, required to rotate the coil through 90° from its initial orientation such that M⃗ becomes perpendicular to B⃗, is ______ μJ.', None, 5,
    lambda: round((200 * 100e-6 * 2.5e-4 * 1) * (math.cos(0) - math.cos(pi / 2)) * 1e6, 6), ['M = NIA = 200 × 10^{−4} × 2.5 × 10^{−4} = 5 × 10^{−6} A m^{2}.', 'W = MB(1 − cos 90°) = 5 × 10^{−6} J = 5 μJ.'], 'moment', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'moment', 'The percentage increase in magnetic field (B) when space within a current carrying solenoid is filled with magnesium (magnetic susceptibility χ_{Mg} = 1.2 × 10^{−5}) is :', ['\\f{5}{6} × 10^{−4} %', '\\f{6}{5} × 10^{−3} %', '\\f{5}{3} × 10^{−5} %', '\\f{5}{6} × 10^{−5} %'], 2,
    lambda: P4([5 / 6 * 1e-4, 6 / 5 * 1e-3, 5 / 3 * 1e-5, 5 / 6 * 1e-5], ((1 + 1.2e-5) - 1) * 100), ['B = μ_{0}(1 + χ)nI, so B rises by a fraction χ.', '1.2 × 10^{−5} × 100% = 1.2 × 10^{−3} % = \\f{6}{5} × 10^{−3} %.'], 'moment', 1)
def _r39():
    m, q, B = 1.0, 1.0, 1.0; r = lambda E: math.sqrt(2 * m * E) / (q * B); Es = [0.5, 1, 2, 3, 4]
    inc = all(r(a) < r(b) for a, b in zip(Es, Es[1:])); conc = all(r(b) - r(a) > r(c) - r(b) for a, b, c in zip(Es[1:], Es[2:], Es[3:]) if b - a == c - b)
    return 3 if inc and conc else 0
add(('2025', 'Apr', '2025-04-07', 1), 'force', 'A particle of charge q, mass m and kinetic energy E enters in magnetic field perpendicular to its velocity and undergoes a circular arc of radius (r). Which of the following curves represents the variation of r with E ?', ['r falling as E grows (hyperbola-like)', 'r rising faster and faster with E', 'r rising but bending over (like √E)', 'r rising in a straight line with E'], 3,
    _r39, ['r = \\f{mv}{qB} = \\f{√{2mE}}{qB} ∝ √{E}.', 'A √{E} curve rises and bends over (concave down).'], 'force', 1)
def _d40():
    m, q, v, B1, B2 = 1.0, 1.0, 1.0, 1.0, 3.0; d = 2 * m * v / (q * B2) - 2 * m * v / (q * B1)   # half circle in each region, opposite drift
    ops = [m * v / (q * B1) * (1 - B2 / B1), m * v / (q * B1) * (1 - B1 / B2), m * v / (q * B1) * (1 - B2 / B1) * 2, m * v / (q * B1) * (1 - B1 / B2) * 2]
    return P4(ops, abs(d), 1e-9)
add(('2025', 'Apr', '2025-04-07', 1), 'force', 'Uniform magnetic fields of different strengths (B_{1} and B_{2}), both normal to the plane of the paper exist on either side of an interface. A charged particle of mass m and charge q, at the interface at an instant, moves into the region 2 with velocity v and returns to the interface. It continues to move into region 1 and finally reaches the interface. What is the displacement of the particle during this movement along the interface? (Consider the velocity of the particle to be normal to the magnetic field and B_{2} > B_{1})', ['\\f{mv}{qB_{1}}(1 − \\f{B_{2}}{B_{1}})', '\\f{mv}{qB_{1}}(1 − \\f{B_{1}}{B_{2}})', '\\f{mv}{qB_{1}}(1 − \\f{B_{2}}{B_{1}}) × 2', '\\f{mv}{qB_{1}}(1 − \\f{B_{1}}{B_{2}}) × 2'], 4,
    _d40, ['Each region gives a semicircle; its chord along the interface is the diameter \\f{2mv}{qB}.', 'The two semicircles move the particle in opposite senses along the interface: |\\f{2mv}{qB_{1}} − \\f{2mv}{qB_{2}}| = \\f{mv}{qB_{1}}(1 − \\f{B_{1}}{B_{2}}) × 2.'], 'force', 2)
def _sq42():
    a, I = 1.0, 3.0; A, B, C, D = (-a / math.sqrt(2), 0, 0), (0, a / math.sqrt(2), 0), (a / math.sqrt(2), 0, 0), (0, -a / math.sqrt(2), 0)
    i1, i2 = I * 2 / 3, I / 3   # parallel paths: r and 2r
    Bv = [x + y for x, y in zip(bs_path([A, B, C], i1, (0, 0, 0), 3000), bs_path([A, D, C], i2, (0, 0, 0), 3000))]
    return P4([math.sqrt(2) * mu0 * I / (3 * pi * a), mu0 * I / (2 * pi * a), 2 * mu0 * I / (3 * pi * a), 3 * pi * mu0 * I / (math.sqrt(2) * a)], nrm(Bv))
add(('2025', 'Apr', '2025-04-08', 2), 'field', 'A current carrying square loop ABCD of edge length a lies in a plane; current I enters at A and leaves at C. If the resistance of the ABC part is r and that of ADC part is 2r, then the magnitude of the resultant magnetic field at centre of the square loop is', ['\\f{√{2}μ_{0}I}{3πa}', '\\f{μ_{0}I}{2πa}', '\\f{2μ_{0}I}{3πa}', '\\f{3πμ_{0}I}{√{2}a}'], 1,
    _sq42, ['Current splits inversely to resistance: \\f{2I}{3} through ABC, \\f{I}{3} through ADC; their fields at the centre are opposite.', 'One side at distance \\f{a}{2}: B = \\f{μ_{0}i}{4π(a/2)}·2 sin 45° = \\f{√{2}μ_{0}i}{2πa}; two sides: \\f{√{2}μ_{0}i}{πa}.', 'Net: \\f{√{2}μ_{0}}{πa}(\\f{2I}{3} − \\f{I}{3}) = \\f{√{2}μ_{0}I}{3πa}.'], 'field', 2)

# ---------- sheet 7
def _w43():
    a, I = 1.0, 1.0; enc = lambda r: I * min(r, a) ** 2 / a ** 2; B = lambda r: mu0 * enc(r) / (2 * pi * r); return P4([0.25, 4, 1, 0.75], B(a / 2) / B(2 * a), 1e-9)
add(('2024', 'Apr', '2024-04-08', 2), 'field', 'A long straight wire of radius a carries a steady current I. The current is uniformly distributed across its cross section. The ratio of the magnetic field at \\f{a}{2} and 2a from axis of the wire is :', ['1 : 4', '4 : 1', '1 : 1', '3 : 4'], 3,
    _w43, ['Inside: B = \\f{μ_{0}Ir}{2πa^{2}} → at \\f{a}{2}: \\f{μ_{0}I}{4πa}. Outside: B = \\f{μ_{0}I}{2πr} → at 2a: \\f{μ_{0}I}{4πa}.', 'Ratio 1 : 1.'], 'field', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'moment', 'The coercivity of a magnet is 5 × 10^{3} A/m. The amount of current required to be passed in a solenoid of length 30 cm and the number of turns 150, so that the magnet gets demagnetised when inside the solenoid is ______ A.', None, 10,
    lambda: round(5e3 * 0.30 / 150, 6), ['The solenoid must supply H = coercivity: H = nI = \\f{N}{L}I.', 'I = \\f{5 × 10^{3} × 0.30}{150} = 10 A.'], 'moment', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'force', 'An electron with kinetic energy 5 eV enters a region of uniform magnetic field of 3 μT perpendicular to its direction. An electric field E is applied perpendicular to the direction of velocity and magnetic field. The value of E, so that electron moves along the same path, is ______ N C^{−1}. (Given, mass of electron = 9 × 10^{−31} kg, electric charge = 1.6 × 10^{−19} C)', None, 4,
    lambda: round(math.sqrt(2 * 5 * 1.6e-19 / 9e-31) * 3e-6, 6), ['Undeflected: qE = qvB → E = vB.', 'v = √{\\f{2 × 5 × 1.6 × 10^{−19}}{9 × 10^{−31}}} = \\f{4}{3} × 10^{6} m/s.', 'E = \\f{4}{3} × 10^{6} × 3 × 10^{−6} = 4 N/C.'], 'force', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'force', 'A proton and a deutron (q = +e, m = 2.0 u) having same kinetic energies enter a region of uniform magnetic field B⃗, moving perpendicular to B⃗. The ratio of the radius r_{d} of deutron path to the radius r_{p} of the proton path is :', ['1 : 1', '1 : √{2}', '√{2} : 1', '1 : 2'], 3,
    lambda: P4([1, 1 / math.sqrt(2), math.sqrt(2), 0.5], math.sqrt(2 * 2.0 * 1.0) / math.sqrt(2 * 1.0 * 1.0)),
    ['r = \\f{√{2mK}}{qB}: same q and K, so r ∝ √{m}.', '\\f{r_{d}}{r_{p}} = √{2} : 1.'], 'force', 1)
def _m51():
    m, pi_ = 44.0, 22 / 7; L = 1.0; pole = m / L; d = 2 * L / pi_   # semicircle: poles end up a diameter apart
    return round(pole * d, 6)
add(('2024', 'Apr', '2024-04-09', 2), 'moment', 'A straight magnetic strip has a magnetic moment of 44 A m^{2}. If the strip is bent in a semicircular shape, its magnetic moment will be ______ A m^{2}. (Given π = \\f{22}{7})', None, 28,
    lambda: round(_m51()), ['Pole strength unchanged; the poles are now a diameter apart: πr = L → 2r = \\f{2L}{π}.', 'm′ = m·\\f{2}{π} = 44 × \\f{2 × 7}{22} = 28 A m^{2}.'], 'moment', 1)

# ---------- sheet 8
def _f54():
    I, a, B0 = 2.0, 2.0, 5.0; Bz = lambda x: B0 * (1 + 4 * x); Fx = 0.0; n = 2000
    for side, x0 in ((+1, 0.0), (-1, a)):   # vertical sides: left (current up) and right (current down); horizontal sides cancel
        for k in range(n):
            dl = (0, side * a / n, 0); f = cross(dl, (0, 0, Bz(x0 if side == 1 else a))); Fx += I * f[0]
    return round(abs(Fx), 6)
add(('2024', 'Apr', '2024-04-09', 1), 'force', 'A square loop of edge length 2 m carrying current of 2 A is placed with its edges parallel to the x − y axis. A magnetic field is passing through the x − y plane and expressed as B⃗ = B_{0}(1 + 4x)k̂, where B_{0} = 5 T. The net magnetic force experienced by the loop is ______ N.', None, 160,
    lambda: round(_f54()), ['Top and bottom edges see the same x-profile with opposite currents: they cancel.', 'The two vertical edges are 2 m apart in x: ΔB = 5 × 4 × 2 = 40 T. F = IL·ΔB = 2 × 2 × 40 = 160 N.'], 'force', 2)
def _b56():
    r, I = 1.0, 1.0; L = 2000.0
    B1 = bs_path([(-L, r, 0), (0, r, 0)], I, (0, 0, 0), 20000)   # top straight wire into the arc
    arc1 = arc(r, pi / 2, -pi / 2, 4000); B1 = [a + b for a, b in zip(B1, bs_path(arc1, I, (0, 0, 0), 1))]
    B1 = [a + b for a, b in zip(B1, bs_path([(0, -r, 0), (-L, -r, 0)], I, (0, 0, 0), 20000))]
    B2 = bs_path([(-L, r, 0), (0, r, 0)], I, (0, 0, 0), 20000); B2 = [a + b for a, b in zip(B2, bs_path(arc1, I, (0, 0, 0), 1))]
    B2 = [a + b for a, b in zip(B2, bs_path([(0, -r, 0), (0, -L, 0)], I, (0, 0, 0), 20000))]   # leaves straight down along the line through Q
    return P4([(2 + pi) / (1 + pi), (1 + pi) / (1 - pi), (2 + pi) / (1 - pi), (1 + pi) / (2 - pi)], nrm(B1) / nrm(B2), 1e-3)
add(('2026', 'Apr', '2026-04-02', 1), 'field', 'Two identical long current carrying wires are bent into the shapes shown: (I) two long parallel straight parts joined by a semicircular arc of radius r with centre P (a hairpin); (II) one long straight part joined to a semicircular arc of radius r with centre Q, the current then leaving along a long straight wire perpendicular to the first, along the line through Q. If the magnitude of magnetic fields at the centres P and Q of the semicircular arc are B_{1} and B_{2} respectively, then the ratio \\f{B_{1}}{B_{2}} is ______.', ['\\f{2 + π}{1 + π}', '\\f{1 + π}{1 − π}', '\\f{2 + π}{1 − π}', '\\f{1 + π}{2 − π}'], 1,
    _b56, ['Semicircle: \\f{μ_{0}I}{4r}; a semi-infinite wire ending opposite the centre at distance r: \\f{μ_{0}I}{4πr}; a wire whose line passes through the centre: 0.', 'B_{1} = \\f{μ_{0}I}{4πr}(2 + π), B_{2} = \\f{μ_{0}I}{4πr}(1 + π).', 'Ratio \\f{2 + π}{1 + π}.'], 'field', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'force', '1 μC charge moving with velocity v⃗ = (î − 2ĵ + 3k̂) m/s in the region of magnetic field B⃗ = (2î + 3ĵ − 5k̂) T. The magnitude of force acting on it is √{α} × 10^{−6} N. The value of α is ______.', None, 171,
    lambda: round(sum(c * c for c in cross((1, -2, 3), (2, 3, -5)))), ['F⃗ = qv⃗ × B⃗; v⃗ × B⃗ = (1, 11, 7).', '|F| = 10^{−6}√{1 + 121 + 49} = √{171} × 10^{−6} N.'], 'force', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'force', 'A current carrying solenoid is placed vertically and a particle of mass m with charge Q is released from rest. The particle moves along the axis of solenoid. If g is acceleration due to gravity then the acceleration (a) of the charged particle will satisfy :', ['a = g', 'a > g', 'a = 0', '0 < a < g'], 1,
    lambda: 1 if nrm(cross((0, 0, -3.0), (0, 0, 0.02))) == 0 else 0, ['Along the axis B⃗ is vertical and v⃗ is vertical: qv⃗ × B⃗ = 0.', 'Only gravity acts: a = g.'], 'force', 1)
def _c63():
    a = 1.0; B = lambda r: mu0 * min(r, a) ** 2 / a ** 2 / (2 * pi * r) if r else 0.0; rs = [k * a / 100 for k in range(0, 101)]; vals = [B(r) for r in rs]
    D = vals.index(min(vals)) == 0; Bmax_axis = vals.index(max(vals)) == 0; Cmin_surface = vals.index(min(vals)) == 100; E = max(vals) - min(vals) < 1e-15
    return 2 if D and not Bmax_axis and not Cmin_surface and not E else 0
add(('2026', 'Jan', '2026-01-28', 2), 'field', 'A long cylindrical conductor with large cross section carries an electric current distributed uniformly over its cross-section. Magnetic field due to this current is : A. maximum at either ends of the conductor and minimum at the midpoint B. maximum at the axis of the conductor C. minimum at the surface of the conductor D. minimum at the axis of the conductor E. same at all points in the cross-section of the conductor', ['A, D Only', 'D Only', 'B, C Only', 'E Only'], 2,
    _c63, ['Inside: B = \\f{μ_{0}Ir}{2πa^{2}} — zero on the axis, largest at the surface.', 'For a long conductor nothing changes along its length. Only D is right.'], 'field', 1)

# ---------- sheet 9
def _bohr66():
    B = lambda n: (lambda r, v: mu0 * (1.6e-19 * v / (2 * pi * r)) / (2 * r))(0.529e-10 * n * n, 2.19e6 / n); return round(B(2) / B(4), 6)
add(('2026', 'Apr', '2026-04-02', 2), 'field', 'Using Bohr\'s model, calculate the ratio of the magnetic fields generated due to the motion of the electrons in the 2^{nd} and 4^{th} orbits of hydrogen atom ______.', None, 32,
    lambda: round(_bohr66()), ['At the nucleus B = \\f{μ_{0}I}{2r} with I = \\f{ev}{2πr}, so B ∝ \\f{v}{r^{2}}.', 'Bohr: v ∝ \\f{1}{n}, r ∝ n^{2} → B ∝ \\f{1}{n^{5}}.', '\\f{B_{2}}{B_{4}} = 2^{5} = 32.'], 'field', 2)
def _o68():
    r, I, L = 1.0, 1.0, 3000.0   # axes: y to the right, z up, x out of the page; wire along y at z = −r, loop (clockwise seen from +x) through the touch point
    Bw = bs_path([(0, -L, -r), (0, L, -r)], I, (0, 0, 0), 30000)
    loop = [(0, -r * math.sin(t), -r * math.cos(t)) for t in [2 * pi * k / 6000 for k in range(6001)]]   # starts at the bottom, goes up the left side
    Bl = bs_path(loop, I, (0, 0, 0), 1); Bx = Bw[0] + Bl[0]; k = mu0 * I / (2 * pi * r)
    return P4([k * (pi + 1), -k * (pi - 1), k * (pi - 1), -k * (pi + 1)], Bx, 1e-3)
add(('2026', 'Jan', '2026-01-21', 2), 'field', 'An infinitely long straight wire carrying current I is bent in a planar shape: it runs along the y-axis (A → B), goes once round a circle of radius r with centre O above it (B → C → D, up the left side and over the top), then continues straight (D → E). x̂ points out of the plane, ŷ to the right, ẑ up. The magnetic field at the centre O of the circular loop is :', ['\\f{μ_{0}I}{2πr}(π + 1)î', '−\\f{μ_{0}I}{2πr}(π − 1)î', '\\f{μ_{0}I}{2πr}(π − 1)î', '−\\f{μ_{0}I}{2πr}(π + 1)î'], 2,
    _o68, ['Straight wire (current +ŷ, below O): \\f{μ_{0}I}{2πr} along +î.', 'Circle traversed clockwise as seen from +x: \\f{μ_{0}I}{2r} along −î.', 'Net: −\\f{μ_{0}I}{2πr}(π − 1)î.'], 'field', 3)
def _d69():
    # dimensions as (M, L, T, A) exponents: B = [M T^-2 A^-1], μ0 = [M L T^-2 A^-2]
    B, mu = (1, 0, -2, -1), (1, 1, -2, -2); d = tuple(a - b for a, b in zip(B, mu))
    ops = [(0, 1, -2, -1), (1, 2, -2, -1), (0, -1, 0, 1), (1, 0, -2, -1)]; return ops.index(d) + 1
add(('2025', 'Jan', '2025-01-22', 1), 'moment', 'If B is magnetic field and μ_{0} is permeability of free space, then the dimensions of (B/μ_{0}) is', ['L T^{−2} A^{−1}', 'M L^{2} T^{−2} A^{−1}', 'L^{−1} A', 'M T^{−2} A^{−1}'], 3,
    _d69, ['\\f{B}{μ_{0}} = H, measured in A/m.', '[L^{−1} A].'], 'moment', 1)
def _r70():
    h, e_, B, m = 6.63e-34, 1.6e-19, 0.3, 9.1e-31; n = 2
    lo, hi = 1e-12, 1.0   # bisection on r for: (eBr)·r = nh/2π  (mv = eBr from the circular motion)
    for _ in range(200):
        mid = (lo + hi) / 2
        if e_ * B * mid * mid < n * h / (2 * pi): lo = mid
        else: hi = mid
    rr = lo
    return P4([math.sqrt(4 * h / (pi * e_ * B)), math.sqrt(h / (2 * pi * e_ * B)), math.sqrt(2 * h / (pi * e_ * B)), math.sqrt(h / (pi * e_ * B))], rr, 1e-6)
add(('2025', 'Jan', '2025-01-22', 2), 'force', 'An electron projected perpendicular to a uniform magnetic field B moves in a circle. If Bohr\'s quantization is applicable, then the radius of the electronic orbit in the first excited state is :', ['√{\\f{4h}{πeB}}', '√{\\f{h}{2πeB}}', '√{\\f{2h}{πeB}}', '√{\\f{h}{πeB}}'], 4,
    _r70, ['Circular motion: mv = eBr. Bohr: mvr = \\f{nh}{2π}.', 'eBr^{2} = \\f{nh}{2π} → r = √{\\f{nh}{2πeB}}; first excited state n = 2: √{\\f{h}{πeB}}.'], 'force', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'force', 'A proton is moving undeflected in a region of crossed electric and magnetic fields at a constant speed of 2 × 10^{5} m s^{−1}. When the electric field is switched off, the proton moves along a circular path of radius 2 cm. The magnitude of electric field is x × 10^{4} N/C. The value of x is ______. Take the mass of the proton = 1.6 × 10^{−27} kg.', None, 2,
    lambda: round((2e5 * (1.6e-27 * 2e5 / (1.6e-19 * 0.02))) / 1e4, 6), ['Circle: B = \\f{mv}{qr} = \\f{1.6 × 10^{−27} × 2 × 10^{5}}{1.6 × 10^{−19} × 0.02} = 0.1 T.', 'Undeflected: E = vB = 2 × 10^{4} N/C → x = 2.'], 'force', 1)

# ---------- sheet 10
def seg_fine(a, b, I, P0):   # long straight run, split geometrically away from the point nearest P0
    d = [b[i] - a[i] for i in range(3)]; L = nrm(d); u = [x / L for x in d]
    t0 = min(max(sum((P0[i] - a[i]) * u[i] for i in range(3)), 0.0), L)
    ts = {0.0, L, t0}
    for side in (1, -1):
        h = 1e-4
        while True:
            t = t0 + side * h
            if t <= 0 or t >= L: break
            ts.add(t); h *= 1.05
    ts = sorted(ts); pts = [tuple(a[i] + u[i] * t for i in range(3)) for t in ts]; return bs_path(pts, I, P0, 4)
def _x73():
    L = 2000.0; P0 = (0.10, 0, 0)
    B = [a + b for a, b in zip(seg_fine((0, -L, 0), (0, L, 0), 5, P0), seg_fine((0.06, L, 0), (0.06, -L, 0), 4, P0))]
    return round(nrm(B) / 1e-5, 2)
add(('2025', 'Jan', '2025-01-22', 2), 'field', 'Two long parallel wires X and Y, separated by a distance of 6 cm, carry currents of 5 A and 4 A, respectively, in opposite directions. Magnitude of the resultant magnetic field at point P at a distance of 4 cm from wire Y (on the side away from X) is x × 10^{−5} T. The value of x is ______. Take permeability of free space as μ_{0} = 4π × 10^{−7} SI units.', None, 1,
    lambda: round(_x73()), ['P is 10 cm from X and 4 cm from Y; opposite currents give opposite fields there.', 'B_{X} = \\f{2 × 10^{−7} × 5}{0.10} = 1 × 10^{−5} T; B_{Y} = \\f{2 × 10^{−7} × 4}{0.04} = 2 × 10^{−5} T.', 'Net 1 × 10^{−5} T → x = 1.'], 'field', 1)
def _g75():
    dimsk = tuple(a - b for a, b in zip((1, 2, -2, 0), (0, 0, 0, 0)))   # torque / angle(dimensionless) = [M L² T⁻²]
    A = dimsk == (1, 2, -2, 0)
    NBA, k, rho = 1.0, 1.0, 1.0; cs = lambda N: N * NBA / k; vs = lambda N: N * NBA / (k * rho * N)   # resistance grows with N
    B = True   # e.g. more turns raise current sensitivity but leave voltage sensitivity unchanged
    C = abs(vs(2) - 2 * vs(1)) < 1e-12; E = cs(2) < cs(1); D = False   # an ammeter needs a SMALL shunt
    chosen = {k_ for k_, v in dict(A=A, B=B and abs(vs(2) - vs(1)) < 1e-12, C=C, D=D, E=E).items() if v}
    opts = [{'A', 'B', 'E'}, {'A', 'B'}, {'B', 'D', 'E'}, {'A', 'D'}]; return opts.index(chosen) + 1
add(('2025', 'Jan', '2025-01-23', 1), 'galv', 'Consider a moving coil galvanometer (MCG): A. The torsional constant in moving coil galvanometer has dimensions [ML^{2}T^{−2}] B. Increasing the current sensitivity may not necessarily increase the voltage sensitivity. C. If we increase number of turns (N) to its double (2N), then the voltage sensitivity doubles. D. MCG can be converted into an ammeter by introducing a shunt resistance of large value in parallel with galvanometer. E. Current sensitivity of MCG depends inversely on number of turns of coil. Choose the correct answer from the options given below :', ['A, B, E Only', 'A, B Only', 'B, D, E Only', 'A, D Only'], 2,
    _g75, ['A: k = \\f{torque}{angle} → [ML^{2}T^{−2}] ✓.', 'Current sensitivity \\f{NBA}{k} ∝ N (E false); voltage sensitivity \\f{NBA}{kR}: doubling N also doubles R, so it is unchanged (C false, B true).', 'An ammeter needs a small shunt (D false). Answer: A, B only.'], 'galv', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'galv', 'A galvanometer having a coil of resistance 30 Ω need 20 mA of current for full-scale deflection. If a maximum current of 3 A is to be measured using this galvanometer, the resistance of the shunt to be added to the galvanometer should be \\f{30}{X} Ω, where X is', ['447', '596', '298', '149'], 4,
    lambda: P4([447, 596, 298, 149], 30 / (0.02 * 30 / (3 - 0.02)), 1e-9), ['S = \\f{I_{g}G}{I − I_{g}} = \\f{0.02 × 30}{2.98} = \\f{30}{149} Ω.'], 'galv', 1)
def _m78():
    dims = {'mu0': (1, 1, -2, -2), 'B': (1, 0, -2, -1), 'm': (0, 2, 0, 1), 'k': (1, 2, -2, 0)}
    L2 = {'I': (1, 2, -2, 0), 'II': (1, 0, -2, -1), 'III': (1, 1, -2, -2), 'IV': (0, 2, 0, 1)}; inv = {v: k for k, v in L2.items()}
    m = (inv[dims['mu0']], inv[dims['B']], inv[dims['m']], inv[dims['k']]); opts = [('IV', 'III', 'I', 'II'), ('I', 'IV', 'II', 'III'), ('III', 'II', 'IV', 'I'), ('II', 'I', 'III', 'IV')]; return opts.index(m) + 1
add(('2025', 'Jan', '2025-01-23', 2), 'moment', 'Match List - I with List - II. List - I: (A) Permeability of free space (B) Magnetic field (C) Magnetic moment (D) Torsional constant. List - II: (I) [ML^{2}T^{−2}] (II) [MT^{−2}A^{−1}] (III) [MLT^{−2}A^{−2}] (IV) [L^{2}A]', ['(A)-(IV), (B)-(III), (C)-(I), (D)-(II)', '(A)-(I), (B)-(IV), (C)-(II), (D)-(III)', '(A)-(III), (B)-(II), (C)-(IV), (D)-(I)', '(A)-(II), (B)-(I), (C)-(III), (D)-(IV)'], 3,
    _m78, ['μ_{0} from F = \\f{μ_{0}I^{2}L}{2πd}: [MLT^{−2}A^{−2}]. B from F = ILB: [MT^{−2}A^{−1}].', 'm = IA: [L^{2}A]. Torsional constant = torque/angle: [ML^{2}T^{−2}].'], 'moment', 1)
def _p79():
    a = 1 / math.sqrt(2); pts = [(-a / 2, -a / 2, 0), (a / 2, -a / 2, 0), (a / 2, a / 2, 0), (-a / 2, a / 2, 0), (-a / 2, -a / 2, 0)]; return round(nrm(bs_path(pts, 5, (0, 0, 0), 4000)) / 1e-6, 3)
add(('2025', 'Jan', '2025-01-24', 1), 'field', 'A current of 5 A exists in a square loop of side \\f{1}{√{2}} m. Then the magnitude of the magnetic field B at the centre of the square loop will be p × 10^{−6} T, where value of p is ______. [Take μ_{0} = 4π × 10^{−7} T m A^{−1}]', None, 8,
    lambda: round(_p79()), ['Each side at distance \\f{a}{2}: B = \\f{μ_{0}I}{4π(a/2)}·2 sin 45°.', 'Four sides: 4 × 10^{−7} × \\f{5}{1/(2√{2})} × √{2} = 8 × 10^{−6} T.'], 'field', 1)
add(('2025', 'Jan', '2025-01-24', 2), 'force', 'Given below are two statements. Assertion (A): A electron in a certain region of uniform magnetic field is moving with constant velocity in a straight line path. Reason (R): The magnetic field in that region is along the direction of velocity of the electron. In the light of the above statements, choose the correct answer from the options given below:', ['(A) is true but (R) is false', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true'], 3,
    lambda: 3 if nrm(cross((2.0, 0, 0), (0.5, 0, 0))) == 0 else 0, ['With v⃗ ∥ B⃗ the force qv⃗ × B⃗ is zero, so the electron keeps a constant velocity.', 'R gives exactly that reason: both true, R explains A.'], 'force', 1)

# ---------- sheet 11
def _g81():
    a = 1.0; B = lambda r: mu0 * min(r, a) ** 2 / a ** 2 / (2 * pi * r) if r else 0.0
    lin_inside = all(abs(B(r) / r - B(a) / a) < 1e-12 for r in (0.2, 0.5, 0.9)); inv_out = all(abs(B(r) * r - B(2 * a) * 2 * a) < 1e-12 for r in (1.5, 3, 5))
    return 4 if lin_inside and inv_out and B(0) == 0 else 0
add(('2025', 'Jan', '2025-01-24', 2), 'field', 'A long straight wire of a circular cross-section with radius a carries a steady current I. The current I is uniformly distributed across this cross-section. The plot of magnitude of magnetic field B with distance r from the centre of the wire is given by', ['zero inside, then falling as 1/r outside', 'constant inside, then falling as 1/r outside', 'falling exponentially from the centre', 'rising linearly from 0 to r = a, then falling as 1/r'], 4,
    _g81, ['Inside (Ampère with enclosed current Ir^{2}/a^{2}): B = \\f{μ_{0}Ir}{2πa^{2}} — a straight line from zero.', 'Outside: B = \\f{μ_{0}I}{2πr}, peak at r = a.'], 'field', 1)
def _p83():
    q, v = 1.0, (2.0, 0, 0); cases = {'A': ((0, 0, 0), (0, 0, 0)), 'B': ((0, 0, 0), (0.3, 0, 0)), 'C': ((0, 1.0, 0), (0, 0, 0)), 'D': ((0, 1.0, 0), (0, 0, 0.5))}   # D: crossed, E = vB
    ok = {k for k, (E, B) in cases.items() if nrm([q * (E[i] + cross(v, B)[i]) for i in range(3)]) < 1e-12}
    return [{'A', 'B', 'C'}, {'A', 'C', 'D'}, {'A', 'B', 'D'}, {'B', 'C', 'D'}].index(ok) + 1
add(('2024', 'Jan', '2024-01-27', 1), 'force', 'A proton moving with a constant velocity passes through a region of space without any change in its velocity. If E⃗ and B⃗ represent the electric and magnetic fields respectively, then the region of space may have : (A) E = 0, B = 0 (B) E = 0, B ≠ 0 (C) E ≠ 0, B = 0 (D) E ≠ 0, B ≠ 0', ['(A), (B) and (C) only', '(A), (C) and (D) only', '(A), (B) and (D) only', '(B), (C) and (D) only'], 3,
    _p83, ['No net force needed: no fields (A); B ∥ v⃗ (B); or crossed fields with qE⃗ = −qv⃗ × B⃗ (D).', 'E ≠ 0 alone always pushes the proton (C impossible).'], 'force', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'field', 'Two long, straight wires carry equal currents (10 A) in opposite directions. The separation between the wires is 5.0 cm. The magnitude of the magnetic field at a point P midway between the wires is ______ μT. (Given : μ_{0} = 4π × 10^{−7} T m A^{−1})', None, 160,
    lambda: round(nrm([a + b for a, b in zip(seg_fine((0, -2000, 0), (0, 2000, 0), 10, (0.025, 0, 0)), seg_fine((0.05, 2000, 0), (0.05, -2000, 0), 10, (0.025, 0, 0)))]) * 1e6),
    ['Between wires with opposite currents the fields add.', 'B = 2 × \\f{2 × 10^{−7} × 10}{0.025} = 1.6 × 10^{−4} T = 160 μT.'], 'field', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'galv', 'A current of 200 μA deflects the coil of a moving coil galvanometer through 60°. The current to cause deflection through \\f{π}{10} radian is :', ['30 μA', '120 μA', '60 μA', '180 μA'], 3,
    lambda: P4([30, 120, 60, 180], 200 * (pi / 10) / (pi / 3), 1e-9), ['I ∝ θ.', 'I = 200 × \\f{π/10}{π/3} = 60 μA.'], 'galv', 1)
def _a87():
    I, R1, R2 = 4, 2 * pi, 4 * pi
    pts = arc(R2, 0, pi, 4000) + [(-R1, 0, 0)] + arc(R1, pi, 2 * pi, 4000) + [(R2, 0, 0)]   # upper big semicircle, lower small one, same sense
    return round(nrm(bs_path(pts, I, (0, 0, 0), 1)) / 1e-7, 3)
add(('2024', 'Jan', '2024-01-27', 2), 'field', 'The magnetic field at the centre of a wire loop formed by two semicircular wires of radii R_{1} = 2π m and R_{2} = 4π m carrying current I = 4 A (the larger semicircle on one side of the common diameter, the smaller on the other, joined by straight pieces along the diameter) is α × 10^{−7} T. The value of α is ______. (Centre O is common for all segments)', None, 3,
    lambda: round(_a87()), ['Both semicircles are traversed in the same rotational sense; the straight pieces point at O.', 'B = \\f{μ_{0}I}{4}(\\f{1}{R_{1}} + \\f{1}{R_{2}}) = 4π × 10^{−7}(\\f{1}{2π} + \\f{1}{4π}) = 3 × 10^{−7} T.'], 'field', 2)

# ---------- sheet 12
def _x88():
    m, q, k, v0, a = 1.0, 1.0, 1.0, 0.5, 1.0   # k = μ0 I / 2π, B = k / r (azimuthal); current along +z
    def acc(r, vr, vz):   # q v × B with B along φ̂: (v_r r̂ + v_z ẑ) × (B φ̂) = v_r B ẑ − v_z B r̂
        B = k / r; return (-q * vz * B / m, q * vr * B / m)
    r, vr, vz, dt, rmin = a, 0.0, v0, 1e-4, a
    for _ in range(400000):
        k1 = acc(r, vr, vz); r2, vr2, vz2 = r + vr * dt / 2, vr + k1[0] * dt / 2, vz + k1[1] * dt / 2; k2 = acc(r2, vr2, vz2)
        r, vr, vz = r + vr2 * dt, vr + k2[0] * dt, vz + k2[1] * dt; rmin = min(rmin, r)
        if vr > 0 and r > rmin + 1e-6: break
    mu0I = 2 * pi * k
    ops = [a * (1 - m * v0 / (2 * q * mu0I)), a / 2, a * math.exp(-4 * pi * m * v0 / (q * mu0I)), a * (1 - m * v0 / (q * mu0I))]
    return P4(ops, rmin, 1e-3)
add(('2025', 'Jan', '2025-01-28', 1), 'force', 'Consider a long thin conducting wire carrying a uniform current I. A particle having mass M and charge q is released at a distance a from the wire with a speed v_{0} along the direction of current in the wire. The particle gets attracted to the wire due to magnetic force. The particle turns round when it is at distance x from the wire. The value of x is [μ_{0} is vacuum permeability]', ['a[1 − \\f{mv_{0}}{2qμ_{0}I}]', '\\f{a}{2}', 'a e^{−\\f{4πmv_{0}}{qμ_{0}I}}', 'a[1 − \\f{mv_{0}}{qμ_{0}I}]'], 3,
    _x88, ['Speed stays v_{0}. Along the wire: m\\f{dv_{z}}{dt} = qv_{r}B = \\f{qμ_{0}I}{2πr}\\f{dr}{dt} → m dv_{z} = \\f{qμ_{0}I}{2π}\\f{dr}{r}.', 'At the turning point v_{r} = 0 and v_{z} = −v_{0}: −2mv_{0} = \\f{qμ_{0}I}{2π}ln\\f{x}{a}.', 'x = a e^{−4πmv_{0}/(qμ_{0}I)}.'], 'force', 3)
def _b90():
    a, I, L = 1.0, 1.0, 3000.0
    pts = [(L, 0, 0), (a, 0, 0)] + arc(a, 0, 1.5 * pi, 6000)[1:] + [(L, -a, 0)]   # in along the line through O, 3/4 circle, out along y = −a
    B = [x + y for x, y in zip(seg_fine((L, 0, 0), (a, 0, 0), I, (0, 0, 0)), bs_path(arc(a, 0, 1.5 * pi, 6000), I, (0, 0, 0), 1))]
    B = [x + y for x, y in zip(B, seg_fine((0, -a, 0), (L, -a, 0), I, (0, 0, 0)))]
    k = mu0 * I / (4 * pi * a); return P4([k * (1.5 * pi + 2), k * (1.5 * pi + 1), k * (pi / 2 + 1), 2 * k * (pi / 2 + 2)], nrm(B), 2e-3)
add(('2025', 'Jan', '2025-01-28', 2), 'field', 'An infinite wire has a circular bend of radius a, and carrying a current I: it comes in along a straight line through the centre O, goes round three-quarters of a circle of radius a about O, and leaves along a straight line at distance a from O, starting from the point of the circle nearest that line. The magnitude of magnetic field at the origin O of the arc is given by :', ['\\f{μ_{0}I}{4πa}[\\f{3π}{2} + 2]', '\\f{μ_{0}I}{4πa}[\\f{3π}{2} + 1]', '\\f{μ_{0}I}{4πa}[\\f{π}{2} + 1]', '\\f{μ_{0}I}{2πa}[\\f{π}{2} + 2]'], 2,
    _b90, ['The incoming wire points at O: no field.', 'Three-quarter arc: \\f{3}{4}·\\f{μ_{0}I}{2a} = \\f{μ_{0}I}{4πa}·\\f{3π}{2}; semi-infinite wire ending opposite O at distance a: \\f{μ_{0}I}{4πa}, same direction.', 'Total \\f{μ_{0}I}{4πa}[\\f{3π}{2} + 1].'], 'field', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'galv', 'A galvanometer having coil resistance 10 Ω shows a full scale deflection for a current of 3 mA. For it to measure a current of 8 A, the value of the shunt should be:', ['3 × 10^{−3} Ω', '4.85 × 10^{−3} Ω', '3.75 × 10^{−3} Ω', '2.75 × 10^{−3} Ω'], 3,
    lambda: P4([3e-3, 4.85e-3, 3.75e-3, 2.75e-3], 3e-3 * 10 / (8 - 3e-3)), ['S = \\f{I_{g}G}{I − I_{g}} = \\f{0.003 × 10}{7.997} ≈ 3.75 × 10^{−3} Ω.'], 'galv', 1)
def _g95():
    S = 24.0; frac = 5 / 25; lo, hi = 0.1, 1e4
    for _ in range(200):   # bisection on G for: share of current through G = S/(S + G) = frac
        G = (lo + hi) / 2
        if S / (S + G) > frac: lo = G
        else: hi = G
    return P4([12, 96, 48, 100], lo, 1e-6)
add(('2024', 'Jan', '2024-01-29', 1), 'galv', 'The deflection in moving coil galvanometer falls from 25 divisions to 5 division when a shunt of 24 Ω is applied. The resistance of galvanometer coil will be :', ['12 Ω', '96 Ω', '48 Ω', '100 Ω'], 2,
    _g95, ['The galvanometer now carries \\f{5}{25} = \\f{1}{5} of the current: \\f{S}{S + G} = \\f{1}{5}.', '24 × 5 = 24 + G → G = 96 Ω.'], 'galv', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'moment', 'The magnetic potential due to a magnetic dipole at a point on its axis situated at a distance of 20 cm from its center is 1.5 × 10^{−5} T m. The magnetic moment of the dipole is ______ A m^{2}. (Given : \\f{μ_{0}}{4π} = 10^{−7} T m A^{−1})', None, 6,
    lambda: round(1.5e-5 * 0.2 ** 2 / 1e-7, 6), ['Axial magnetic potential V = \\f{μ_{0}}{4π}\\f{m}{r^{2}}.', 'm = \\f{1.5 × 10^{−5} × 0.04}{10^{−7}} = 6 A m^{2}.'], 'moment', 1)

# ---------- sheet 13
def _m98():
    q, V, B = 1.0, 3.0, 2.0; R = lambda m: math.sqrt(2 * m * q * V) / (q * B); mX, mY = 2.7, 0.9; R1, R2 = R(mX), R(mY)
    return P4([(R2 / R1) ** 2, (R1 / R2) ** 2, R1 / R2, R2 / R1], mX / mY, 1e-9)
add(('2024', 'Jan', '2024-01-29', 2), 'force', 'Two particles X and Y having equal charges are being accelerated through the same potential difference. Thereafter they enter normally in a region of uniform magnetic field and describes circular paths of radii R_{1} and R_{2} respectively. The mass ratio of X and Y is :', ['(\\f{R_{2}}{R_{1}})^{2}', '(\\f{R_{1}}{R_{2}})^{2}', '\\f{R_{1}}{R_{2}}', '\\f{R_{2}}{R_{1}}'], 2,
    _m98, ['K = qV for both; r = \\f{√{2mqV}}{qB} ∝ √{m}.', '\\f{m_{X}}{m_{Y}} = (\\f{R_{1}}{R_{2}})^{2}.'], 'force', 1)
def _h102():
    a = 1.0; B = lambda r: min(r, a) ** 2 / a ** 2 / r; Bmax = B(a)
    inside = [r for r in [k * a / 10000 for k in range(1, 10000)] if abs(B(r) - Bmax / 2) < 1e-4]; outside = [r for r in [a + k * a / 10000 for k in range(1, 30000)] if abs(B(r) - Bmax / 2) < 1e-4]
    ri, ro = sum(inside) / len(inside), sum(outside) / len(outside)
    ops = [(0.5, 2), (0.25, 1.5), (0.25, 2), (0.5, 3)]; return [i + 1 for i, (x, y) in enumerate(ops) if abs(x - ri) < 1e-3 and abs(y - ro) < 1e-3][0]
add(('2025', 'Jan', '2025-01-29', 1), 'field', 'Consider a long straight wire of a circular cross-section (radius a) carrying a steady current I. The current is uniformly distributed across this cross-section. The distances from the centre of the wire\'s cross-section at which the magnetic field [inside the wire, outside the wire] is half of the maximum possible magnetic field, any where due to the wire, will be', ['[a/2, 2a]', '[a/4, 3a/2]', '[a/4, 2a]', '[a/2, 3a]'], 1,
    _h102, ['Maximum at the surface: \\f{μ_{0}I}{2πa}.', 'Inside B ∝ r → half at \\f{a}{2}; outside B ∝ \\f{1}{r} → half at 2a.'], 'field', 1)
def _u103():
    units = {'induction': 'gauss', 'intensity': 'A/m', 'flux': 'weber', 'moment': 'A m²'}   # B in gauss/tesla, H in A/m, Φ in Wb, m in A m²
    L2 = {'I': 'A m²', 'II': 'weber', 'III': 'gauss', 'IV': 'A/m'}; inv = {v: k for k, v in L2.items()}
    m = tuple(inv[units[k]] for k in ('induction', 'intensity', 'flux', 'moment'))
    return [('III', 'IV', 'II', 'I'), ('III', 'IV', 'I', 'II'), ('I', 'II', 'III', 'IV'), ('III', 'II', 'I', 'IV')].index(m) + 1
add(('2025', 'Jan', '2025-01-29', 2), 'moment', 'Match List - I with List - II. List – I: (A) Magnetic induction (B) Magnetic intensity (C) Magnetic flux (D) Magnetic moment. List - II: (I) Ampere meter^{2} (II) Weber (III) Gauss (IV) Ampere meter^{−1}', ['(A)-(III), (B)-(IV), (C)-(II), (D)-(I)', '(A)-(III), (B)-(IV), (C)-(I), (D)-(II)', '(A)-(I), (B)-(II), (C)-(III), (D)-(IV)', '(A)-(III), (B)-(II), (C)-(I), (D)-(IV)'], 1,
    _u103, ['Induction B: tesla or gauss. Intensity H: A/m.', 'Flux: weber. Magnetic moment: A m^{2}.'], 'moment', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'field', 'The magnetic field inside a 200 turns solenoid of radius 10 cm is 2.9 × 10^{−4} Tesla. If the solenoid carries a current of 0.29 A, then the length of the solenoid is ______ π cm.', None, 8,
    lambda: round(mu0 * 200 * 0.29 / 2.9e-4 * 100 / pi, 6), ['B = μ_{0}\\f{N}{L}I → L = \\f{4π × 10^{−7} × 200 × 0.29}{2.9 × 10^{−4}} = 0.08π m = 8π cm.'], 'field', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'force', 'The horizontal component of earth\'s magnetic field at a place is 3.5 × 10^{−5} T. A very long straight conductor carrying current of √{2} A in the direction from South east to North West is placed. The force per unit length experienced by the conductor is ______ × 10^{−6} N/m.', None, 35,
    lambda: round(nrm(cross((-math.sqrt(2) / math.sqrt(2), math.sqrt(2) / math.sqrt(2), 0), (0, 3.5e-5, 0))) / 1e-6, 6),
    ['The field points north; SE → NW is 45° from it.', 'F/L = IB sin 45° = √{2} × 3.5 × 10^{−5} × \\f{1}{√{2}} = 35 × 10^{−6} N/m.'], 'force', 1)
def _x109():
    mu = lambda n: (1.6e-19 * (2.19e6 / n) / (2 * pi * 0.529e-10 * n * n)) * pi * (0.529e-10 * n * n) ** 2   # I·A with Bohr v and r
    return P4([2, 1, 3, 1e-9], math.log(mu(4) / mu(2)) / math.log(2), 1e-6)
add(('2024', 'Jan', '2024-01-30', 2), 'moment', 'An electron revolving in n^{th} Bohr orbit has magnetic moment μ_{n}. If μ_{n} ∝ n^{x}, the value of x is:', ['2', '1', '3', '0'], 2,
    _x109, ['μ = IA = \\f{ev}{2πr}·πr^{2} = \\f{evr}{2}.', 'v ∝ \\f{1}{n}, r ∝ n^{2} → μ ∝ n: x = 1.'], 'moment', 1)

# ---------- sheet 14
def _x110():
    a = 1.0; pts = [(-a / 2, -a / 2, 0), (a / 2, -a / 2, 0), (a / 2, a / 2, 0), (-a / 2, a / 2, 0), (-a / 2, -a / 2, 0)]; return round(nrm(bs_path(pts, 5, (0, 0, 0), 4000)) / (math.sqrt(2) * 1e-7), 3)
add(('2024', 'Jan', '2024-01-30', 2), 'field', 'The current of 5 A flows in a square loop of sides 1 m is placed in air. The magnetic field at the centre of the loop is X√{2} × 10^{−7} T. The value of X is ______.', None, 40,
    lambda: round(_x110()), ['Each side at 0.5 m: B = \\f{μ_{0}I}{4π(0.5)}·2 sin 45° = 10^{−7} × 10 × √{2}.', 'Four sides: 40√{2} × 10^{−7} T → X = 40.'], 'field', 1)
def _t115():
    m = 5 * 0.20 * 0.10; mv = (-m, 0, 0); tau = cross(mv, (0, 2e-3, 0)); mag = nrm(tau)
    dirs = {1: (0, 0, 1), 2: (0, 0, -1), 3: (1, 0, 0), 4: (0, 1, 0)}; h = [k for k, d in dirs.items() if abs(sum(t * x for t, x in zip(tau, d)) - mag) < 1e-15 and abs(mag - 2e-4) < 1e-12]; return h[0]
add(('2024', 'Jan', '2024-01-31', 2), 'moment', 'A uniform magnetic field of 2 × 10^{−3} T acts along positive Y-direction. A rectangular loop of sides 20 cm and 10 cm with current of 5 A is in Y − Z plane. The current is in anticlockwise sense with reference to negative X axis. Magnitude and direction of the torque is :', ['2 × 10^{−4} N m along positive Z-direction', '2 × 10^{−4} N m along negative Z-direction', '2 × 10^{−4} N m along positive X-direction', '2 × 10^{−4} N m along positive Y-direction'], 2,
    _t115, ['Anticlockwise seen looking along −X means m⃗ points along −x̂; m = IA = 5 × 0.02 = 0.1 A m^{2}.', 'τ⃗ = m⃗ × B⃗ = (−0.1x̂) × (2 × 10^{−3}ŷ) = −2 × 10^{−4} ẑ N m.'], 'moment', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'moment', 'A solenoid has a core made of material with relative permeability 400. The magnetic field produced in the interior of solenoid is 1.0 T. The magnetic intensity in SI units is α × 10^{5}. The value of α is ______. (Free space permeability μ_{0} = 4π × 10^{−7} SI units.)', ['\\f{25}{π}', '\\f{1}{16π}', '\\f{1}{π}', '\\f{1}{4π}'], 2,
    lambda: P4([25 / pi, 1 / (16 * pi), 1 / pi, 1 / (4 * pi)], 1.0 / (400 * mu0) / 1e5, 1e-9), ['H = \\f{B}{μ_{r}μ_{0}} = \\f{1}{400 × 4π × 10^{−7}} = \\f{10^{5}}{16π} A/m.'], 'moment', 1)
def _b120():
    m, d = 3 * math.sqrt(5), 0.05; k = 1e-7
    def dip(mvec, pos, P0):   # point dipole field
        r = [P0[i] - pos[i] for i in range(3)]; R = nrm(r); u = [x / R for x in r]; md = sum(a * b for a, b in zip(mvec, u))
        return [k * (3 * md * u[i] - mvec[i]) / R ** 3 for i in range(3)]
    B = [a + b for a, b in zip(dip((m, 0, 0), (0, 0, 0), (d, 0, 0)), dip((0, -m, 0), (2 * d, 0, 0), (d, 0, 0)))]
    return round(nrm(B) / 1e-3, 4)
add(('2026', 'Apr', '2026-04-04', 2), 'moment', 'Two identical small bar magnets each of dipole moment 3√{5} J/T are placed at a center to center separation of 10 cm, with their axes perpendicular to each other: P, midway between them, lies on the axis of the first and on the equatorial line of the second. The value of magnetic field at the point P midway between the magnets is α × 10^{−3} T. The value of α is ______. (μ_{0} = 4π × 10^{−7} T m/A)', None, 12,
    lambda: round(_b120()), ['Axial point of the first: B_{1} = \\f{μ_{0}}{4π}\\f{2m}{d^{3}}; equatorial point of the second: B_{2} = \\f{μ_{0}}{4π}\\f{m}{d^{3}}, at right angles.', '\\f{μ_{0}}{4π}\\f{m}{d^{3}} = 10^{−7} × \\f{3√{5}}{1.25 × 10^{−4}} = 2.4√{5} × 10^{−3}.', 'B = √{5} × 2.4√{5} × 10^{−3} = 12 × 10^{−3} T.'], 'moment', 2)

# ---------- sheet 15
add(('2026', 'Apr', '2026-04-04', 2), 'moment', 'A circular coil of radius 2 cm and 125 turns carries a current of 1 A. The coil is placed in a uniform magnetic field of magnitude 0.4 T. The axis of the coil makes an angle of 30° with the direction of the magnetic field. The torque acting on the coil is α × 10^{−4} N m. The value of α is ______. (π = 3.14)', None, 314,
    lambda: round(nrm(cross((125 * 1 * 3.14 * 0.02 ** 2, 0, 0), (0.4 * math.cos(pi / 6), 0.4 * math.sin(pi / 6), 0))) / 1e-4, 4),
    ['τ = NIAB sin 30° = 125 × 1 × 3.14 × 4 × 10^{−4} × 0.4 × 0.5.', '= 0.0314 N m = 314 × 10^{−4} N m.'], 'moment', 1)
def _x124():
    lo, hi = -100.0, 100.0   # magnetic acceleration is ⟂ B: find x with a·B = 0
    f = lambda x: 4 * 3 + (-x / 2) * 2
    for _ in range(200):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0: hi = m
        else: lo = m
    return round(lo, 6)
add(('2026', 'Apr', '2026-04-05', 1), 'force', 'The charged particle moving in a uniform magnetic field of (3î + 2ĵ) T has an acceleration (4î − \\f{x}{2}ĵ) m/s^{2}. The value of x is ______.', None, 12,
    lambda: round(_x124()), ['The magnetic force (and acceleration) is perpendicular to B⃗: a⃗·B⃗ = 0.', '12 − x = 0 → x = 12.'], 'force', 1)
def _k128():
    q, E0, lam, L, m, B0, v0 = 1.0, 2.0, 0.7, 1.5, 1.0, 0.8, 1.0
    x, y, vx, vy, dt = 0.0, 0.0, v0 / math.sqrt(2), v0 / math.sqrt(2), 1e-5; K0 = 0.5 * m * (vx * vx + vy * vy)
    def a(x, vx, vy): return ((q * E0 * math.exp(-lam * x) + q * vy * B0) / m, (-q * vx * B0) / m)
    while x < L:
        ax, ay = a(x, vx, vy); xm, vxm, vym = x + vx * dt / 2, vx + ax * dt / 2, vy + ay * dt / 2; ax2, ay2 = a(xm, vxm, vym)
        x, y, vx, vy = x + vxm * dt, y + vym * dt, vx + ax2 * dt, vy + ay2 * dt
        assert vx > 0
    dK = 0.5 * m * (vx * vx + vy * vy) - K0
    ops = [q * E0 / lam * (1 - math.exp(-lam * L)), v0 * q * B0 / (2 * lam) * (2 - math.exp(-2 * lam * L)), q * E0 / lam * (1 + math.exp(-lam * L)), q * (E0 + v0 * B0) / lam * (1 - math.exp(-lam * L / 2))]
    return P4(ops, dK, 2e-3)
add(('2026', 'Apr', '2026-04-05', 2), 'force', 'A particle of charge q and mass m is projected from origin with an initial velocity v⃗ = (\\f{v_{0}}{√{2}}x̂ + \\f{v_{0}}{√{2}}ŷ). There exists a uniform magnetic field B⃗ = B_{0}ẑ and a space varying electric field E⃗ = E_{0}e^{−λx}x̂ within the region 0 ≤ x ≤ L. After travelling a distance such that x-coordinate has changed from x = 0 to x = L, the change in the kinetic energy is ______.', ['\\f{qE_{0}}{λ}[1 − e^{−λL}]', '(\\f{v_{0}qB_{0}}{2λ})[2 − e^{−2λL}]', '\\f{qE_{0}}{λ}[1 + e^{−λL}]', 'q(\\f{E_{0} + v_{0}B_{0}}{λ})[1 − e^{−λL/2}]'], 1,
    _k128, ['The magnetic force does no work; only the electric field does.', 'ΔK = ∫_{0}^{L} qE_{0}e^{−λx}dx = \\f{qE_{0}}{λ}(1 − e^{−λL}).'], 'force', 2)
def _a130():
    a = 4 * math.sqrt(3) * 1e-2; Rv = a / math.sqrt(3); pts = [(Rv * math.cos(pi / 2 + k * 2 * pi / 3), Rv * math.sin(pi / 2 + k * 2 * pi / 3), 0) for k in range(4)]
    return P4([2 * math.sqrt(3), math.sqrt(3), 3 * math.sqrt(3), math.sqrt(3) / 2], nrm(bs_path(pts, 2, (0, 0, 0), 4000)) / 1e-5, 1e-3)
add(('2026', 'Jan', '2026-01-23', 2), 'field', 'The current passing through a conducting loop in the form of equilateral triangle of side 4√{3} cm is 2 A. The magnetic field at its centroid is α × 10^{−5} T. The value of α is ______. (Given : μ_{0} = 4π × 10^{−7} SI units)', ['2√{3}', '√{3}', '3√{3}', '\\f{√{3}}{2}'], 3,
    _a130, ['Distance of each side from the centroid: \\f{a}{2√{3}} = 2 cm.', 'Each side: \\f{μ_{0}I}{4πd}(sin 60° + sin 60°) = 10^{−7} × \\f{2}{0.02} × √{3} = √{3} × 10^{−5} T.', 'Three sides: 3√{3} × 10^{−5} T.'], 'field', 1)

# ---------- sheet 16
add(('2026', 'Jan', '2026-01-24', 1), 'moment', 'A short bar magnet placed with its axis at 30° with an external field of 800 Gauss, experiences a torque of 0.016 N m. The work done in moving it from most stable to most unstable position is α × 10^{−3} J. The value of α is ______.', None, 64,
    lambda: round(2 * (0.016 / math.sin(pi / 6)) / 1e-3, 6), ['τ = mB sin 30° = 0.016 → mB = 0.032 J.', 'W = U(180°) − U(0°) = 2mB = 0.064 J → α = 64.'], 'moment', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'field', 'A current of 30 A each flows in opposite directions in two conducting wires, placed parallel to each other at a distance of 8 cm. The magnetic field at the mid point between the two wires is ______ μT. (\\f{μ_{0}}{4π} = 10^{−7} N/A^{2})', ['30', '300', '150', '0.0'], 2,
    lambda: P4([30, 300, 150, 1e-9], nrm([a + b for a, b in zip(seg_fine((0, -2000, 0), (0, 2000, 0), 30, (0.04, 0, 0)), seg_fine((0.08, 2000, 0), (0.08, -2000, 0), 30, (0.04, 0, 0)))]) * 1e6, 1e-3),
    ['Opposite currents: the fields add between the wires.', 'B = 2 × \\f{2 × 10^{−7} × 30}{0.04} = 3 × 10^{−4} T = 300 μT.'], 'field', 1)
def _g137():
    for k in range(1, 100000):
        G = k / 1000; Ig = 10 / (G + 470)
        if abs(Ig * G - (0.5 - Ig) * 2) < 1e-6: return round(G, 3)
add(('2026', 'Apr', '2026-04-06', 2), 'galv', 'A moving coil of galvanometer when shunted with 2 Ω resistance gives a full scale deflection for a current of 500 mA. When a resistance of 470 Ω is connected in series it gives a full scale deflection for 10 V potential applied on it. The value of resistance of galvanometer coil is ______ Ω.', None, 50,
    lambda: round(_g137()), ['Shunt: I_{g}G = (0.5 − I_{g}) × 2. Series: I_{g}(G + 470) = 10.', 'Subtract: 470I_{g} + 2I_{g} = 9 → I_{g} = \\f{9}{468} A; then G = 50 Ω.'], 'galv', 2)
def _o138():
    r, I = 1.0, 1.0
    P_loop = [(-r, r * math.cos(t), -r * math.sin(t)) for t in [2 * pi * k / 4000 for k in range(4001)]]   # clockwise seen from O (looking along −x)
    Q_loop = [(r, r * math.cos(t), r * math.sin(t)) for t in [2 * pi * k / 4000 for k in range(4001)]]    # clockwise seen from O (looking along +x)
    B = [a + b for a, b in zip(bs_path(P_loop, I, (0, 0, 0), 1), bs_path(Q_loop, 4 * I, (0, 0, 0), 1))]
    k = mu0 * I / (4 * math.sqrt(2) * r); vals = [-3 * k, -k, k, 3 * k]   # +x is towards Q
    return P4(vals, B[0], 1e-3)
add(('2026', 'Jan', '2026-01-24', 2), 'field', 'Two identical circular loops P and Q each of radius r are lying in parallel planes such that they have common axis, each at distance r from O on either side. The current through P and Q are I and 4I respectively in clockwise direction as seen from O. The net magnetic field at O is:', ['\\f{3μ_{0}I}{4√{2}r} towards P', '\\f{μ_{0}I}{4√{2}r} towards P', '\\f{μ_{0}I}{4√{2}r} towards Q', '\\f{3μ_{0}I}{4√{2}r} towards Q'], 4,
    _o138, ['On the axis at distance r: B = \\f{μ_{0}Ir^{2}}{2(2r^{2})^{3/2}} = \\f{μ_{0}I}{4√{2}r}.', 'Clockwise as seen from O: each loop\'s field at O points away from O, towards that loop.', 'Net (4 − 1)\\f{μ_{0}I}{4√{2}r} = \\f{3μ_{0}I}{4√{2}r} towards Q.'], 'field', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'galv', 'A moving coil galvanometer of resistance 100 Ω shows a full scale deflection for a current of 1 mA. The value of resistance required to convert this galvanometer into an ammeter, showing full scale deflection for a current of 5 mA, is ______ Ω', ['25', '10', '0.5', '2.5'], 1,
    lambda: P4([25, 10, 0.5, 2.5], 1e-3 * 100 / (5e-3 - 1e-3), 1e-9), ['S = \\f{I_{g}G}{I − I_{g}} = \\f{1 × 100}{4} = 25 Ω.'], 'galv', 1)
def _d140():
    # (M, L, T, A): H = A/m, ε = M⁻¹L⁻³T⁴A², E = M L T⁻³ A⁻¹, x = L, t = T. Solve by brute force over small integers
    H = (0, -1, 0, 1); eps = (-1, -3, 4, 2); E = (1, 1, -3, -1)
    sols = [(p, q, r, s) for p in range(-3, 4) for q in range(-3, 4) for r in range(-3, 4) for s in range(-3, 4)
            if all(p * (i == 1) + q * eps[i] + r * E[i] - s * (i == 2) == H[i] for i in range(4))]
    assert len(sols) == 1; return [(1, 1, 1, 1), (-1, 1, 2, 1), (1, -1, -2, 1), (-1, -2, -2, 1)].index(sols[0]) + 1
add(('2026', 'Apr', '2026-04-08', 2), 'moment', 'Consider the equation H = \\f{x^{p}ε^{q}E^{r}}{t^{s}} where H = magnetic field (intensity); E = electric field, ε = permittivity, x = distance, t = time. The values of p, q, r and s respectively are:', ['1, 1, 1, 1', '−1, 1, 2, 1', '1, −1, −2, 1', '−1, −2, −2, 1'], 1,
    _d140, ['[H] = A L^{−1}; [ε] = M^{−1}L^{−3}T^{4}A^{2}; [E] = MLT^{−3}A^{−1}.', 'Match M: r = q; A: 2q − r = 1 → q = r = 1; L: p − 3 + 1 = −1 → p = 1; T: 4 − 3 − s = 0 → s = 1.'], 'moment', 2)

# ---------- sheet 17
def _t141():
    I, R = 100 * math.sqrt(2), 0.02; n = (1 / math.sqrt(2), 0, 1 / math.sqrt(2)); m = [I * 3.14 * R * R * c for c in n]; B = [4e-3 * c for c in (3, 0, 2)]; t = cross(m, B)
    ops = [(0, 0, 16e-5), (0, 0, 5024e-7), (5024e-7, 0, 0), (0, 5024e-7, 0)]; h = [i + 1 for i, o in enumerate(ops) if nrm([a - b for a, b in zip(o, t)]) < 1e-9]; assert len(h) == 1; return h[0]
add(('2026', 'Apr', '2026-04-08', 2), 'moment', 'A current carrying circular loop of radius 2 cm with unit normal n̂ = \\f{k̂ + î}{√{2}} is placed in a magnetic field, B⃗ = B_{0}(3î + 2k̂). If B_{0} = 4 × 10^{−3} T and current I = 100√{2} A, the torque experienced by the loop is ______ Wb A. (π = 3.14)', ['16 × 10^{−5} k̂', '5024 × 10^{−7} k̂', '5024 × 10^{−7} î', '5024 × 10^{−7} ĵ'], 4,
    _t141, ['m⃗ = IAn̂ = 100√{2} × 3.14 × 4 × 10^{−4} × \\f{(1, 0, 1)}{√{2}} = 0.1256(1, 0, 1).', 'τ⃗ = m⃗ × B⃗ = 0.1256 × 4 × 10^{−3} × ((1, 0, 1) × (3, 0, 2)) = 5.024 × 10^{−4}(0, 1, 0).', '5024 × 10^{−7} ĵ.'], 'moment', 2)
def _p143():
    m, q, B = 5e-6, 5 * pi * 1e-6, 0.1; v = (3e-2, 0, 2e-2); dt = 1e-3; pos = [0.0, 0.0, 0.0]; vel = list(v); T = 2 * pi * m / (q * B); n = int(round(5 * T / dt))
    for _ in range(n):   # RK2 for 5 periods
        a = [q / m * c for c in cross(vel, (0, 0, B))]; vm = [vel[i] + a[i] * dt / 2 for i in range(3)]; a2 = [q / m * c for c in cross(vm, (0, 0, B))]
        pos = [pos[i] + vm[i] * dt for i in range(3)]; vel = [vel[i] + a2[i] * dt for i in range(3)]
    return round(pos[2], 4)
add(('2026', 'Apr', '2026-04-08', 2), 'force', 'A 5 mg particle carrying a charge of 5π × 10^{−6} C is moving with velocity of (3î + 2k̂) × 10^{−2} m/s in a region having magnetic field B⃗ = 0.1k̂ Wb/m^{2}. It moves a distance of α meter along k̂ when it completes 5 revolutions. The value of α is ______.', None, 2,
    lambda: round(_p143()), ['Helix: period T = \\f{2πm}{qB} = \\f{2π × 5 × 10^{−6}}{5π × 10^{−6} × 0.1} = 20 s.', 'Along k̂ the speed stays 2 × 10^{−2} m/s: 5 × 20 × 0.02 = 2 m.'], 'force', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'field', 'The magnetic field at the centre of a current carrying circular loop of radius R is 16 μT. The magnetic field at a distance x = √{3}R on its axis from the centre is ______ μT.', ['2√{2}', '4', '2', '8'], 3,
    lambda: P4([2 * math.sqrt(2), 4, 2, 8], 16 * nrm(bs_path(arc(1.0, 0, 2 * pi, 4000), 1, (0, 0, math.sqrt(3)), 1)) / nrm(bs_path(arc(1.0, 0, 2 * pi, 4000), 1, (0, 0, 0), 1)), 1e-4),
    ['Axial field ratio \\f{R^{3}}{(R^{2} + x^{2})^{3/2}} = \\f{R^{3}}{8R^{3}} = \\f{1}{8}.', '16 × \\f{1}{8} = 2 μT.'], 'field', 1)
for _p in P: _p['t'] = _p['fam']
