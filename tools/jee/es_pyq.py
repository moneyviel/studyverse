"""Real JEE Main questions — Physics Unit 11: Electrostatics. Our own solutions; chk re-solves each one
(numerically from the charges, exact circuit solver, or vector sums) so the NTA key is confirmed by code.
Figures are described in words. Skipped: dimension-only items (Unit 1), displacement-current / AC items (Units 14–15),
items whose meaning sits only in a figure we cannot state exactly, NTA bonus items, and items where our working
disagrees with the key (24-01-25 S1 Q5, 22-01-25 S1 Q1, 28-01-26 S2 Q27, 29-01-25 S1 Q15)."""
import math, random
from fractions import Fraction as F
from common import new_registry, pick, near, verify, solve_dc
P, add = new_registry()
k = 9e9; e0 = 8.85e-12
AR4 = ['Both (A) and (R) are correct but (R) is not the correct explanation of (A)', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)', '(A) is correct but (R) is not correct', '(A) is not correct but (R) is correct']

def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
def pt_field(qs, p):   # qs: [(q, x, y, z)], k = 1
    E = [0.0, 0.0, 0.0]
    for q, *r in qs:
        d = [p[i] - r[i] for i in range(3)]; s = math.sqrt(sum(x * x for x in d))
        for i in range(3): E[i] += q * d[i] / s ** 3
    return E
def pt_pot(qs, p): return sum(q / math.dist(r, p) for q, *r in qs)
def mag(v): return math.sqrt(sum(x * x for x in v))
def dip(a=1e-4, p=1.0): return [(p / (2 * a), a, 0, 0), (-p / (2 * a), -a, 0, 0)]   # dipole along +x, moment p
def arc_field(t0, t1, n=4000):
    ex = ey = 0.0
    for i in range(n):
        t = t0 + (t1 - t0) * (i + .5) / n; ex -= math.cos(t); ey -= math.sin(t)
    return math.hypot(ex, ey) * (t1 - t0) / n

def swing(dt=1e-5):   # string angle θ from +x; qE/m = 1, l = 1 → θ'' = −sin θ; integrate until the particle reaches the x-axis
    th, w = math.pi / 3, 0.0
    while th > 0: w -= math.sin(th) * dt; th += w * dt
    return abs(w)

# ---------------- Coulomb's law, superposition ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'charge', 'A point charge +q is placed at the origin. A second point charge +9q is placed at (d, 0, 0) in Cartesian coordinate system. The point in between them where the electric field vanishes is :',
    ['(d/4, 0, 0)', '(d/3, 0, 0)', '(4d/3, 0, 0)', '(3d/4, 0, 0)'], 1, lambda: near([0.25, 1 / 3, 4 / 3, 0.75], bisect(lambda x: 1 / x ** 2 - 9 / (1 - x) ** 2, 1e-6, 1 - 1e-6)),
    ['Between two like charges the fields point opposite ways, so they can cancel there.', '\\f{q}{x^{2}} = \\f{9q}{(d − x)^{2}} → d − x = 3x → x = \\f{d}{4}.'], 'coul', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'charge', 'Two identical conducting spheres P and S with charge Q on each, repel each other with a force 16 N. A third identical uncharged conducting sphere R is successively brought in contact with the two spheres. The new force of repulsion between P and S is :',
    ['4 N', '6 N', '1 N', '12 N'], 2, lambda: (lambda p, s: pick([4, 6, 1, 12], 16 * p * s))(F(1, 2), (1 + F(1, 2)) / 2),
    ['Identical spheres share charge equally on contact.', 'R touches P: P → \\f{Q}{2}, R → \\f{Q}{2}. R touches S: (Q + \\f{Q}{2}) ÷ 2 = \\f{3Q}{4} each.', 'F′ = 16 × \\f{1}{2} × \\f{3}{4} = 6 N.'], 'coul', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'field', 'Suppose a uniformly charged wall provides a uniform electric field of 2 × 10^{4} N/C normally. A charged particle of mass 2 g being suspended through a silk thread of length 20 cm and remain stayed at a distance of 10 cm from the wall. Then the charge on the particle will be \\f{1}{√{x}} μC where x = ______ [use g = 10 m/s^{2}]',
    None, 3, lambda: round((1 / (0.002 * 10 * math.tan(math.asin(0.1 / 0.2)) / 2e4 * 1e6)) ** 2),
    ['The thread makes angle θ with the wall: sin θ = \\f{10}{20} → θ = 30°.', 'Balance: qE = mg tan θ → q = \\f{0.002 × 10 × (1/√{3})}{2 × 10^{4}} = \\f{1}{√{3}} × 10^{−6} C.', 'So x = 3.'], 'coul', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'charge', 'Six point charges are kept 60° apart from each other on the circumference of a circle of radius R, at angles 30°, 90°, 150°, 210°, 270° and 330° from the +x axis. The charge at 150° is −Q and all the others are +Q. The net electric field at the center of the circle is ______. (ε_{0} is permittivity of free space)',
    ['−\\f{5Q}{8πε_{0}R^{2}}(î + √{3}ĵ)', '−\\f{Q}{4πε_{0}R^{2}}(√{3}î − ĵ)', '−(\\f{5Q}{8πε_{0}R^{2}})(î − 3ĵ)', '\\f{Q}{4πε_{0}R^{2}}(√{3}î − ĵ)'], 2,
    lambda: (lambda E: [i + 1 for i, c in enumerate([(-5 / 2, -5 * math.sqrt(3) / 2), (-math.sqrt(3), 1), (-5 / 2, 15 / 2), (math.sqrt(3), -1)]) if abs(c[0] - E[0]) + abs(c[1] - E[1]) < 1e-9][0])(
        pt_field([((-1 if a == 150 else 1), math.cos(math.radians(a)), math.sin(math.radians(a)), 0) for a in (30, 90, 150, 210, 270, 330)], (0, 0, 0))),
    ['Six equal +Q would cancel. Turning the one at 150° into −Q is the same as adding −2Q there.', 'A −2Q charge pulls the field toward it: magnitude \\f{2Q}{4πε_{0}R^{2}} along (cos 150°, sin 150°) = (−\\f{√{3}}{2}, \\f{1}{2}).', 'E = \\f{Q}{4πε_{0}R^{2}}(−√{3}î + ĵ) = −\\f{Q}{4πε_{0}R^{2}}(√{3}î − ĵ).'], 'coul', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'field', 'A metallic ring is uniformly charged. AC and BD are two mutually perpendicular diameters (A at the top, B on the right, C at the bottom, D on the left; O is the centre). Electric field due to arc AB at O is E in magnitude. What would be the magnitude of electric field at O due to arc ABC ?',
    ['2E', 'Zero', 'E/2', '√{2}E'], 4, lambda: near([2, 0, 0.5, math.sqrt(2)], arc_field(0, math.pi) / arc_field(0, math.pi / 2)),
    ['Arc ABC = arc AB + arc BC, two equal quarter arcs.', 'Each gives E at O, pointing along its own middle (45° lines), so the two fields are at 90° to each other.', 'Resultant = √{E^{2} + E^{2}} = √{2}E.'], 'coul', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'field', 'Consider a circular loop that is uniformly charged and has a radius a√{2}. Find the position along the positive z-axis of the cartesian coordinate system where the electric field is maximum if the ring was assumed to be placed in xy plane at the origin :',
    ['a/√{2}', 'a', '0', 'a/2'], 2, lambda: near([1 / math.sqrt(2), 1, 0, 0.5], max((i / 10000 for i in range(1, 40000)), key=lambda z: z / (z * z + 2) ** 1.5)),
    ['On the axis: E = \\f{kQz}{(z^{2} + R^{2})^{3/2}}; it is largest at z = \\f{R}{√{2}}.', 'R = a√{2} → z = a.'], 'coul', 2)

# ---------------- Electric dipole ----------------
add(('2024', 'Apr', '2024-04-05', 2), 'field', 'The electric field at an axial point p, at distance r from the centre O of a short electric dipole, is E. The electric field at a point R on the equatorial line, at distance 2r from O, will be \\f{E}{x}. The value of x :',
    None, 16, lambda: round(mag(pt_field(dip(), (1, 0, 0))) / mag(pt_field(dip(), (0, 2, 0)))),
    ['Short dipole: axial E = \\f{2kp}{r^{3}}, equatorial E = \\f{kp}{r^{3}}.', 'At 2r on the equator: \\f{kp}{8r^{3}} = \\f{1}{16} × \\f{2kp}{r^{3}} → x = 16.'], 'dip', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'field', 'For a short dipole placed at origin O, the dipole moment P is along x-axis. If the electric potential and electric field at A, a point on the x-axis at distance r from O, are V_{0} and E_{0}, respectively, then the correct combination of the electric potential and electric field, respectively, at point B on the y-axis at distance 2r from O is given by',
    ['V_{0} and \\f{E_{0}}{4}', 'zero and \\f{E_{0}}{8}', '\\f{V_{0}}{2} and \\f{E_{0}}{16}', 'zero and \\f{E_{0}}{16}'], 4,
    lambda: (lambda V, r: [0, 0, 0, 4][0] if V > 1e-6 else (2 if abs(r - 8) < .01 else 4 if abs(r - 16) < .01 else 0))(abs(pt_pot(dip(), (0, 2, 0))), mag(pt_field(dip(), (1, 0, 0))) / mag(pt_field(dip(), (0, 2, 0)))),
    ['B is on the equatorial line: the two charges are equally far → V = 0.', 'Equatorial field at 2r: \\f{kp}{(2r)^{3}} = \\f{kp}{8r^{3}}; axial E_{0} = \\f{2kp}{r^{3}} → E_{B} = \\f{E_{0}}{16}.'], 'dip', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'field', 'Two short electric dipoles A and B, with dipole moments p_{1} and p_{2}, are placed at the same point O with their axes mutually perpendicular: A lies along the line Ox (its + end pointing away from x) and B is perpendicular to Ox. The resultant electric field at a point x is making an angle of 60° with the line joining points O and x. The ratio of the dipole moments p_{2}/p_{1} is ______ .',
    ['\\f{√{3}}{2}', '2√{3}', '\\f{1}{√{3}}', '√{3}'], 2,
    lambda: near([math.sqrt(3) / 2, 2 * math.sqrt(3), 1 / math.sqrt(3), math.sqrt(3)], bisect(lambda r: (lambda E: math.degrees(math.atan2(abs(E[1]), abs(E[0]))) - 60)([a + b for a, b in zip(pt_field(dip(), (1, 0, 0)), pt_field([(q, y, x, z) for q, x, y, z in dip(p=r)], (1, 0, 0)))]), 0.1, 20)),
    ['At x: A gives an axial field \\f{2kp_{1}}{r^{3}} along Ox; B gives an equatorial field \\f{kp_{2}}{r^{3}} perpendicular to Ox.', 'tan 60° = \\f{kp_{2}/r^{3}}{2kp_{1}/r^{3}} = \\f{p_{2}}{2p_{1}} → \\f{p_{2}}{p_{1}} = 2√{3}.'], 'dip', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'field', 'Two small spherical balls of mass 10 g each with charges −2 μC and 2 μC, are attached to two ends of very light rigid rod of length 20 cm. The arrangement is now placed near an infinite nonconducting charge sheet with uniform charge density of 100 μC/m^{2} such that length of rod makes an angle of 30° with electric field generated by charge sheet. Net torque acting on the rod is: (Take ε_{0} : 8.85 × 10^{−12} C^{2} N^{−1} m^{−2})',
    ['11.2 Nm', '112 Nm', '1.12 Nm', '2.24 Nm'], 3, lambda: near([11.2, 112, 1.12, 2.24], 2e-6 * (1e-4 / (2 * e0)) * 0.2 * math.sin(math.radians(30))),
    ['Sheet field: E = \\f{σ}{2ε_{0}} = \\f{10^{−4}}{2 × 8.85 × 10^{−12}} ≈ 5.65 × 10^{6} N/C (uniform).', 'p = 2 × 10^{−6} × 0.2 = 4 × 10^{−7} C m.', 'τ = pE sin 30° ≈ 4 × 10^{−7} × 5.65 × 10^{6} × 0.5 ≈ 1.12 N m.'], 'dip', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'field', 'A dipole with two electric charges of 2 μC magnitude each, with separation distance 0.5 μm, is placed between the plates of a capacitor such that its axis is parallel to an electric field established between the plates when a potential difference of 5 V is applied. Separation between the plates is 0.5 mm. If the dipole is rotated by 30° from the axis, it tends to realign in the direction due to a torque. The value of torque is :',
    ['2.5 × 10^{−9} N m', '5 × 10^{−9} N m', '2.5 × 10^{−12} N m', '5 × 10^{−3} N m'], 2, lambda: near([2.5e-9, 5e-9, 2.5e-12, 5e-3], 2e-6 * 0.5e-6 * (5 / 0.5e-3) * 0.5),
    ['p = 2 × 10^{−6} × 0.5 × 10^{−6} = 10^{−12} C m; E = \\f{5}{0.5 × 10^{−3}} = 10^{4} V/m.', 'τ = pE sin 30° = 10^{−12} × 10^{4} × \\f{1}{2} = 5 × 10^{−9} N m.'], 'dip', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'field', 'Two point charges −4 μC and 4 μC, constituting an electric dipole, are placed at (−9, 0, 0) cm and (9, 0, 0) cm in a uniform electric field of strength 10^{4} N C^{−1}. The work done on the dipole in rotating it from the equilibrium through 180° is :',
    ['18.4 mJ', '16.4 mJ', '12.4 mJ', '14.4 mJ'], 4, lambda: near([18.4, 16.4, 12.4, 14.4], 1000 * ((lambda U: U(math.pi) - U(0))(lambda t: -4e-6 * 0.18 * 1e4 * math.cos(t)))),
    ['p = 4 × 10^{−6} × 0.18 = 7.2 × 10^{−7} C m.', 'W = U(180°) − U(0°) = pE − (−pE) = 2pE = 2 × 7.2 × 10^{−7} × 10^{4} = 14.4 mJ.'], 'dip', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'field', 'An electric dipole of dipole moment 6 × 10^{−6} C m is placed in uniform electric field of magnitude 10^{6} V/m. Initially, the dipole moment is parallel to electric field. The work that needs to be done on the dipole to make its dipole moment opposite to the field, will be ______ J.',
    None, 12, lambda: round(-6e-6 * 1e6 * math.cos(math.pi) + 6e-6 * 1e6 * math.cos(0)),
    ['U = −pE cos θ.', 'W = U(180°) − U(0°) = 2pE = 2 × 6 × 10^{−6} × 10^{6} = 12 J.'], 'dip', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'field', 'Two charges of −4 μC and +4 μC are placed at the points A(1, 0, 4) m and B(2, −1, 5) m located in an electric field \\vec{E} = 0.20 î V/cm. The magnitude of the torque acting on the dipole is 8√{α} × 10^{−5} N m, where α = ______',
    None, 2, lambda: (lambda d, E: round((mag([4e-6 * (d[1] * E[2] - d[2] * E[1]), 4e-6 * (d[2] * E[0] - d[0] * E[2]), 4e-6 * (d[0] * E[1] - d[1] * E[0])]) / 8e-5) ** 2))((1, -1, 1), (20, 0, 0)),
    ['\\vec{p} = q × (B − A) = 4 × 10^{−6}(î − ĵ + k̂) C m; E = 0.20 V/cm = 20 V/m along î.', '\\vec{τ} = \\vec{p} × \\vec{E} = 8 × 10^{−5}(ĵ + k̂) → |τ| = 8√{2} × 10^{−5} N m → α = 2.'], 'dip', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'field', 'An electric dipole is placed at a distance of 2 cm from an infinite plane sheet having positive charge density σ_{0}, with its −q end nearer the sheet and its axis perpendicular to the sheet. Choose the correct option from the following.',
    ['Potential energy and torque both are maximum.', 'Torque on dipole is zero and net force is directed away from the sheet.', 'Torque on dipole is zero and net force acts towards the sheet.', 'Potential energy of dipole is minimum and torque is zero.'], 4,
    lambda: 4 if (lambda E_on_minus, E_on_plus: abs(E_on_minus - E_on_plus) < 1e-12)(1 / 2, 1 / 2) else 0,
    ['The sheet\'s field is uniform (σ/2ε_{0}) and points away from it — from −q toward +q, i.e. along \\vec{p}.', 'Uniform field → forces on ±q cancel: no net force.', '\\vec{p} ∥ \\vec{E} → τ = 0 and U = −pE is the minimum (stable).'], 'dip', 2)

# ---------------- Flux and Gauss's law ----------------
add(('2024', 'Feb', '2024-02-01', 2), 'gauss', 'C_{1} and C_{2} are two hollow concentric cubes. The inner cube C_{1} encloses a charge 2Q; a charge 3Q lies between C_{1} and C_{2} (inside C_{2} but outside C_{1}). The ratio of electric flux passing through C_{1} and C_{2} is :',
    ['2 : 5', '5 : 2', '2 : 3', '3 : 2'], 1, lambda: pick(['2 : 5', '5 : 2', '2 : 3', '3 : 2'], (lambda r: f'{r.numerator} : {r.denominator}')(F(2, 2 + 3))),
    ['Gauss: flux = \\f{charge enclosed}{ε_{0}} — shape and size do not matter.', 'C_{1} encloses 2Q; C_{2} encloses 2Q + 3Q = 5Q → 2 : 5.'], 'gauss', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'gauss', 'Five charges +q, +5q, −2q, +3q and −4q are situated such that +q, +5q and −2q lie inside a closed surface S while +3q and −4q lie outside it. The electric flux due to this configuration through the surface S is :',
    ['\\f{5q}{ε_{0}}', '\\f{4q}{ε_{0}}', '\\f{3q}{ε_{0}}', '\\f{q}{ε_{0}}'], 2, lambda: pick([5, 4, 3, 1], 1 + 5 - 2),
    ['Only charges inside S count.', 'q + 5q − 2q = 4q → flux = \\f{4q}{ε_{0}}.'], 'gauss', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'gauss', 'Two charges of 5Q and −2Q are situated at the points (3a, 0) and (−5a, 0) respectively. The electric flux through a sphere of radius 4a having center at origin is :',
    ['\\f{2Q}{ε_{0}}', '\\f{5Q}{ε_{0}}', '\\f{7Q}{ε_{0}}', '\\f{3Q}{ε_{0}}'], 2, lambda: pick([2, 5, 7, 3], sum(q for q, x in ((5, 3), (-2, -5)) if abs(x) < 4)),
    ['5Q is 3a from the centre — inside. −2Q is 5a away — outside.', 'Flux = \\f{5Q}{ε_{0}}.'], 'gauss', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'gauss', 'Two point charges 8 μC and −2 μC are located at x = 2 cm and x = 4 cm, respectively on the x-axis. The ratio of electric flux due to these charges through two spheres of radii 3 cm and 5 cm with their centers at the origin is ______.',
    ['4 : 1', '3 : 4', '4 : 3', '4 : 5'], 3, lambda: pick(['4 : 1', '3 : 4', '4 : 3', '4 : 5'], (lambda r: f'{r.numerator} : {r.denominator}')(F(sum(q for q, x in ((8, 2), (-2, 4)) if x < 3), sum(q for q, x in ((8, 2), (-2, 4)) if x < 5)))),
    ['Radius 3 cm encloses only 8 μC; radius 5 cm encloses 8 − 2 = 6 μC.', 'Ratio 8 : 6 = 4 : 3.'], 'gauss', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'gauss', 'A charge q is placed at the center of one of the surface of a cube. The flux linked with the cube is :-',
    ['\\f{q}{4ε_{0}}', '\\f{q}{2ε_{0}}', '\\f{q}{8ε_{0}}', 'Zero'], 2,
    lambda: (lambda N: near([0.25, 0.5, 0.125, 0], (sum(2 / ((x * x + y * y + 4) ** 1.5) for x in [(-1 + (i + .5) * 2 / N) for i in range(N)] for y in [(-1 + (j + .5) * 2 / N) for j in range(N)]) * (2 / N) ** 2
        + 4 * sum(1 / ((1 + y * y + z * z) ** 1.5) for y in [(-1 + (i + .5) * 2 / N) for i in range(N)] for z in [((j + .5) * 2 / N) for j in range(N)]) * (2 / N) ** 2) / (4 * math.pi)))(120),
    ['Put a second, identical cube on the other side of that face: together they enclose q with full symmetry.', 'So one cube gets half the flux: \\f{q}{2ε_{0}}.'], 'gauss', 1)
add(('2025', 'Jan', '2025-01-22', 1), 'gauss', 'A line charge of length \\f{a}{2} is kept at the center of an edge BC of a cube ABCDEFGH having edge length a (the line charge lies along the edge). If the density of line charge is λ C per unit length, then the total electric flux through all the faces of the cube will be ____. (Take, ε_{0} as the free space permittivity)',
    ['\\f{λa}{4ε_{0}}', '\\f{λa}{16ε_{0}}', '\\f{λa}{2ε_{0}}', '\\f{λa}{8ε_{0}}'], 4, lambda: pick([F(1, 4), F(1, 16), F(1, 2), F(1, 8)], F(1, 4) * F(1, 2)),
    ['Charge on the line = \\f{λa}{2}.', 'A charge on an edge is shared by 4 cubes meeting at that edge → this cube gets ¼.', 'Flux = \\f{1}{4} × \\f{λa}{2ε_{0}} = \\f{λa}{8ε_{0}}.'], 'gauss', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'gauss', 'An infinitely long wire has uniform linear charge density λ = 2 nC/m. The net flux through a Gaussian cube of side length √{3} cm, if the wire passes through any two corners of the cube, that are maximally displaced from each other, would be x N m^{2} C^{−1}, where x is : [Neglect any edge effects and use \\f{1}{4πε_{0}} = 9 × 10^{9} SI units]',
    ['0.72π', '1.44π', '6.48π', '2.16π'], 4, lambda: near([0.72, 1.44, 6.48, 2.16], 2e-9 * (math.sqrt(3) * math.sqrt(3) * 1e-2) * 4 * 9e9),
    ['The wire runs along a body diagonal: length inside = √{3} × √{3} cm = 3 cm.', 'q = 2 × 10^{−9} × 0.03 = 6 × 10^{−11} C.', 'Φ = \\f{q}{ε_{0}} = 6 × 10^{−11} × 4π × 9 × 10^{9} = 2.16π.'], 'gauss', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'gauss', 'A point charge causes an electric flux of −2 × 10^{4} N m^{2} C^{−1} to pass through a spherical Gaussian surface of 8.0 cm radius, centred on the charge. The value of the point charge is : (Given ε_{0} = 8.85 × 10^{−12} C^{2} N^{−1} m^{−2})',
    ['−17.7 × 10^{−8} C', '15.7 × 10^{−8} C', '−15.7 × 10^{−8} C', '17.7 × 10^{−8} C'], 1, lambda: near([-17.7, 15.7, -15.7, 17.7], -2e4 * e0 * 1e8),
    ['q = ε_{0}Φ — the radius does not matter.', '= 8.85 × 10^{−12} × (−2 × 10^{4}) = −17.7 × 10^{−8} C.'], 'gauss', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'gauss', 'The electric field in a region is given by \\vec{E} = (2î + 4ĵ + 6k̂) × 10^{3} N/C. The flux of the field through a rectangular surface parallel to x-z plane is 6.0 N m^{2} C^{−1}. The area of the surface is ______ cm^{2}.',
    None, 15, lambda: round(6.0 / 4e3 * 1e4), ['A surface parallel to the x-z plane has its normal along ĵ, so only E_{y} = 4 × 10^{3} counts.', 'A = \\f{6}{4 × 10^{3}} = 1.5 × 10^{−3} m^{2} = 15 cm^{2}.'], 'gauss', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'gauss', 'An electric field, \\vec{E} = \\f{2î + 6ĵ + 8k̂}{√{6}} passes through the surface of 4 m^{2} area having unit vector n̂ = (\\f{2î + ĵ + k̂}{√{6}}). The electric flux for that surface is ______ V m.',
    None, 12, lambda: round(sum(a * b for a, b in zip((2, 6, 8), (2, 1, 1))) / 6 * 4), ['Φ = \\vec{E}·n̂ A.', '\\vec{E}·n̂ = \\f{4 + 6 + 8}{6} = 3 → Φ = 3 × 4 = 12 V m.'], 'gauss', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'gauss', 'An electric field is given by (6î + 5ĵ + 3k̂) N/C. The electric flux through a surface area 30î m^{2} lying in YZ-plane (in SI unit) is :',
    ['90', '150', '180', '60'], 3, lambda: pick([90, 150, 180, 60], 6 * 30), ['Area vector 30î → only E_{x} = 6 counts.', 'Φ = 6 × 30 = 180 N m^{2}/C.'], 'gauss', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'gauss', 'An electric field \\vec{E} = (2x î) N C^{−1} exists in space. A cube of side 2 m is placed with its edges parallel to the axes and its two faces perpendicular to x at x = 2 m and x = 4 m. The electric flux through the cube is ______ N m^{2}/C.',
    None, 16, lambda: (lambda faces, div: round(faces) if abs(faces - div) < 1e-3 else -1)((2 * 4) * 4 - (2 * 2) * 4, sum((2 * (x + 1e-6) - 2 * x) / 1e-6 * (2 / 1000) * 4 for x in [2 + (i + .5) * 2 / 1000 for i in range(1000)])),
    ['Field only along x: flux only through the two x-faces (area 4 m^{2}).', 'Φ = E(4) × 4 − E(2) × 4 = 8 × 4 − 4 × 4 = 16 N m^{2}/C.', 'Check by Gauss: charge density ∝ \\f{dE}{dx} = 2 is uniform; 2 × volume 8 = 16 ✓.'], 'gauss', 2)
add(('2025', 'Apr', '2025-04-02', 1), 'gauss', 'Consider two infinitely large plane parallel conducting plates separated by d. The plates are uniformly charged with a surface charge density +σ and −2σ. The force experienced by a point charge +q placed at the mid point between two plates will be :',
    ['\\f{3σq}{4ε_{0}}', '\\f{3σq}{2ε_{0}}', '\\f{σq}{4ε_{0}}', '\\f{σq}{2ε_{0}}'], 2, lambda: near([0.75, 1.5, 0.25, 0.5], abs(1 / 2 * 1 + (-2) / 2 * (-1))),
    ['Each sheet gives \\f{σ}{2ε_{0}}, pointing away from + and toward −.', 'Between them: away from +σ (→) and toward −2σ (→): \\f{σ}{2ε_{0}} + \\f{2σ}{2ε_{0}} = \\f{3σ}{2ε_{0}}.', 'F = \\f{3σq}{2ε_{0}}.'], 'gauss', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'gauss', 'Three infinitely long charged thin sheets are placed parallel to the y-z plane: −σ at x = −a, −2σ at x = a and σ at x = 3a. The magnitude of electric field at the point P, which lies between x = a and x = 3a, is \\f{xσ}{ε_{0}}. The value of x is (all quantities are measured in SI units).',
    None, 2, lambda: round(abs(sum(s / 2 * (1 if 2 > xs else -1) for s, xs in ((-1, -1), (-2, 1), (1, 3))))),
    ['Each sheet: \\f{σ}{2ε_{0}}, away from + and toward −.', 'At P all three fields point along −x: \\f{σ}{2ε_{0}} + \\f{2σ}{2ε_{0}} + \\f{σ}{2ε_{0}} = \\f{2σ}{ε_{0}} → x = 2.'], 'gauss', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'gauss', 'An infinite plane sheet of charge having uniform surface charge density +σ_{s} C/m^{2} is placed on x-y plane. Another infinitely long line charge having uniform linear charge density +λ_{e} C/m is placed at z = 4 m plane and parallel to y-axis. If the magnitude values |σ_{s}| = 2|λ_{e}| then at point (0, 0, 2), the ratio of magnitudes of electric field values due to sheet charge to that of line charge is π√{n} : 1. The value of n is',
    None, 16, lambda: round(((2 / 2) / (1 / (2 * math.pi * 2)) / math.pi) ** 2),
    ['Sheet: \\f{σ}{2ε_{0}}. Line (distance 2 m): \\f{λ}{2πε_{0} × 2} = \\f{λ}{4πε_{0}}.', 'Ratio = \\f{σ/2}{λ/4π} = 2π × \\f{σ}{λ} = 4π = π√{16} → n = 16.'], 'gauss', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'gauss', 'Match List - I with List - II. List - I: (A) Electric field inside (distance r > 0 from center) of a uniformly charged spherical shell with surface charge density σ, and radius R. (B) Electric field at distance r > 0 from a uniformly charged infinite plane sheet with surface charge density σ. (C) Electric field outside (distance r > 0 from center) of a uniformly charged spherical shell with surface charge density σ, and radius R. (D) Electric field between 2 oppositely charged infinite plane parallel sheets with uniform surface charge density σ. List - II: (I) σ/ε_{0} (II) σ/2ε_{0} (III) 0 (IV) \\f{σ}{ε_{0}r^{2}}',
    ['(A)−(IV), (B)−(I), (C)−(III), (D)−(II)', '(A)−(IV), (B)−(II), (C)−(III), (D)−(I)', '(A)−(III), (B)−(II), (C)−(IV), (D)−(I)', '(A)−(II), (B)−(I), (C)−(IV), (D)−(III)'], 3,
    lambda: pick(['(A)−(IV), (B)−(I), (C)−(III), (D)−(II)', '(A)−(IV), (B)−(II), (C)−(III), (D)−(I)', '(A)−(III), (B)−(II), (C)−(IV), (D)−(I)', '(A)−(II), (B)−(I), (C)−(IV), (D)−(III)'], '(A)−(III), (B)−(II), (C)−(IV), (D)−(I)'),
    ['Inside a shell: 0. Sheet: \\f{σ}{2ε_{0}}. Between opposite sheets: \\f{σ}{ε_{0}}.', 'Outside the shell: \\f{σ4πR^{2}}{4πε_{0}r^{2}} = \\f{σR^{2}}{ε_{0}r^{2}} — the list writes it as \\f{σ}{ε_{0}r^{2}} (R = 1 unit) → (IV).'], 'gauss', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'gauss', 'An electron is moving under the influence of the electric field of a uniformly charged infinite plane sheet S having surface charge density +σ. The electron at t = 0 is at a distance of 1 m from S and has a speed of 1 m/s. The maximum value of σ if the electron strikes S at t = 1 s is α[\\f{mε_{0}}{e}] \\f{C}{m^{2}}, the value of α is',
    None, 8, lambda: round(bisect(lambda al: (1 + 1 * 1 - 0.5 * (al / 2) * 1) , 0.1, 100)),
    ['Acceleration toward S: a = \\f{eσ}{2ε_{0}m} (constant).', 'Largest σ ↔ the electron first moves away at 1 m/s: 0 = 1 + 1 × 1 − \\f{a}{2} × 1^{2} → a = 4.', '\\f{eσ}{2ε_{0}m} = 4 → σ = 8\\f{mε_{0}}{e} → α = 8.'], 'gauss', 3)

# ---------------- Potential and energy ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'pot', 'The electrostatic potential on the surface of uniformly charged spherical shell of radius R = 10 cm is 120 V. The potential at the centre of shell, at a distance r = 5 cm from centre, and at a distance r = 15 cm from the centre of the shell respectively, are:',
    ['40 V, 40 V, 80 V', '0 V, 0 V, 80 V', '0 V, 120 V, 40 V', '120 V, 120 V, 80 V'], 4,
    lambda: pick(['40 V, 40 V, 80 V', '0 V, 0 V, 80 V', '0 V, 120 V, 40 V', '120 V, 120 V, 80 V'], ', '.join(f'{round(120 * 10 / max(r, 10))} V' for r in (0.001, 5, 15))),
    ['Inside a shell the field is 0, so V is the same as on the surface: 120 V at 0 and 5 cm.', 'Outside V ∝ \\f{1}{r}: 120 × \\f{10}{15} = 80 V.'], 'pot', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'pot', 'Two charges q_{1} (at A) and q_{2} (at B) are separated by a distance of 30 cm. A third charge q_{3}, initially at C, 40 cm from A on the line through A perpendicular to AB, is moved along the circular path of radius 40 cm centred at A from C to D, where D lies on line AB beyond B (AD = 40 cm). If the difference in potential energy due to movement of q_{3} from C to D is given by \\f{q_{3}K}{4πε_{0}}, the value of K is:',
    ['8q_{1}', '6q_{2}', '6q_{1}', '8q_{2}'], 4,
    lambda: (lambda A, B, C, D: pick(['8q_{1}', '6q_{2}', '6q_{1}', '8q_{2}'], (f'{round(1 / math.dist(D, B) - 1 / math.dist(C, B))}q_{{2}}' if abs(1 / math.dist(D, A) - 1 / math.dist(C, A)) < 1e-12 else '?')))((0, 0), (0.3, 0), (0, 0.4), (0.4, 0)),
    ['q_{3} stays 40 cm from q_{1}, so that part of U does not change.', 'From q_{2}: BC = √{30^{2} + 40^{2}} = 50 cm, BD = 10 cm.', 'ΔU = \\f{q_{3}q_{2}}{4πε_{0}}(\\f{1}{0.1} − \\f{1}{0.5}) = \\f{q_{3} × 8q_{2}}{4πε_{0}} → K = 8q_{2}.'], 'pot', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'pot', 'A point charge of 10^{−8} C is placed at origin. The work done in moving a point charge 2 μC from point A(4, 4, 2) m to B(2, 2, 1) m is ______ J. (\\f{1}{4πε_{0}} = 9 × 10^{9} in SI units)',
    ['45 × 10^{−6}', '0', '30 × 10^{−6}', '15 × 10^{−6}'], 3, lambda: near([45, 0, 30, 15], 2e-6 * k * 1e-8 * (1 / math.dist((2, 2, 1), (0, 0, 0)) - 1 / math.dist((4, 4, 2), (0, 0, 0))) * 1e6),
    ['OA = √{16 + 16 + 4} = 6 m, OB = 3 m.', 'V_{A} = \\f{9 × 10^{9} × 10^{−8}}{6} = 15 V, V_{B} = 30 V.', 'W = q(V_{B} − V_{A}) = 2 × 10^{−6} × 15 = 30 × 10^{−6} J.'], 'pot', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'pot', 'Two charges 7 μC and −4 μC are placed at (−7 cm, 0, 0) and (7 cm, 0, 0) respectively. Given, ε_{0} = 8.85 × 10^{−12} C^{2} N^{−1} m^{−2}, the electrostatic potential energy of the charge configuration is :',
    ['−2.0 J', '−1.2 J', '−1.8 J', '−1.5 J'], 3, lambda: near([-2, -1.2, -1.8, -1.5], 7e-6 * -4e-6 / (4 * math.pi * e0 * 0.14)),
    ['U = \\f{q_{1}q_{2}}{4πε_{0}r} with r = 14 cm.', '= \\f{9 × 10^{9} × 7 × 10^{−6} × (−4 × 10^{−6})}{0.14} ≈ −1.8 J.'], 'pot', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'pot', 'The electric potential at the surface of an atomic nucleus (Z = 50) of radius 9 × 10^{−13} cm is ______ × 10^{6} V.',
    None, 8, lambda: round(k * 50 * 1.6e-19 / 9e-15 / 1e6), ['V = \\f{kZe}{R}, R = 9 × 10^{−15} m.', '= \\f{9 × 10^{9} × 50 × 1.6 × 10^{−19}}{9 × 10^{−15}} = 8 × 10^{6} V.'], 'pot', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'pot', 'Electric field in a region is given by \\vec{E} = Axî + Byĵ, where A = 10 V/m^{2} and B = 5 V/m^{2}. If the electric potential at a point (10, 20) is 500 V, then the electric potential at origin is ______ V.',
    ['1000', '500', '2000', '0'], 3, lambda: near([1000, 500, 2000, 0], 500 + sum((10 * (10 * t) * 10 + 5 * (20 * t) * 20) / 4000 for t in [(i + .5) / 4000 for i in range(4000)])),
    ['V(0) − V(P) = ∫_{0}^{P} \\vec{E}·d\\vec{r} = \\f{A x^{2}}{2} + \\f{B y^{2}}{2}.', '= 5 × 100 + 2.5 × 400 = 1500 → V(0) = 500 + 1500 = 2000 V.'], 'pot', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'pot', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : Work done by electric field on moving a positive charge on an equipotential surface is always zero. Reason (R) : Electric lines of forces are always perpendicular to equipotential surfaces. In the light of the above statements, choose the most appropriate answer from the options given below',
    ['Both (A) and (R) are correct but (R) is not the correct explanation of (A)', '(A) is correct but (R) is not correct', '(A) is not correct but (R) is correct', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)'], 4,
    lambda: 4 if (True, True, True) == (True, True, True) else 0,
    ['W = q(V_{1} − V_{2}) = 0 on an equipotential — A is true.', 'Field lines meet equipotentials at 90°, so the force has no component along the motion — R is true and explains A.'], 'pot', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'pot', 'Three infinitely long wires with linear charge density λ are placed along the x-axis, y-axis and z-axis respectively. Which of the following denotes an equipotential surface?',
    ['xy + yz + zx = constant', 'xyz = constant', '(x^{2} + y^{2})(y^{2} + z^{2})(z^{2} + x^{2}) = constant', '(x + y)(y + z)(z + x) = constant'], 3,
    lambda: (lambda pts: [i + 1 for i, f in enumerate([lambda x, y, z: x * y + y * z + z * x, lambda x, y, z: x * y * z, lambda x, y, z: (x * x + y * y) * (y * y + z * z) * (z * z + x * x), lambda x, y, z: (x + y) * (y + z) * (z + x)])
        if all(abs((-0.5 * sum(math.log(a * a + b * b) for a, b in ((p[1], p[2]), (p[0], p[2]), (p[0], p[1])))) + 0.5 * math.log(abs(f(*p)))) < 1e-9 for p in pts)][0])([tuple(random.Random(s).uniform(0.2, 3) for _ in range(3)) for s in range(20)]),
    ['A line charge gives V = −\\f{λ}{2πε_{0}} ln ρ (ρ = distance from the line).', 'Distances from the x, y, z axes: √{y^{2} + z^{2}}, √{x^{2} + z^{2}}, √{x^{2} + y^{2}}.', 'V = −\\f{λ}{4πε_{0}} ln[(x^{2} + y^{2})(y^{2} + z^{2})(z^{2} + x^{2})] → constant V ↔ that product is constant.'], 'pot', 3)
add(('2026', 'Jan', '2026-01-21', 2), 'pot', 'Consider two identical metallic spheres of radius R each having charge Q and mass m. Their centers have an initial separation of 4R. Both the spheres are given an initial speed of u towards each other. The minimum value of u, so that they can just touch each other is : (Take k = \\f{1}{4πε_{0}} and assume kQ^{2} > Gm^{2} where G is the Gravitational constant)',
    ['√{\\f{kQ^{2}}{4mR}(1 − \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{4mR}(1 + \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{2mR}(1 − \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{2mR}(1 − \\f{Gm^{2}}{2kQ^{2}})}'], 1,
    lambda: (lambda kk, Q, G_, m, R: (lambda u: near([math.sqrt(kk * Q * Q / (4 * m * R) * (1 - G_ * m * m / (kk * Q * Q))), math.sqrt(kk * Q * Q / (4 * m * R) * (1 + G_ * m * m / (kk * Q * Q))), math.sqrt(kk * Q * Q / (2 * m * R) * (1 - G_ * m * m / (kk * Q * Q))), math.sqrt(kk * Q * Q / (2 * m * R) * (1 - G_ * m * m / (2 * kk * Q * Q)))], u))(
        bisect(lambda u: m * u * u - ((kk * Q * Q - G_ * m * m) * (1 / (2 * R) - 1 / (4 * R))), 1e-6, 10)))(1.0, 1.0, 0.3, 1.0, 1.0),
    ['Energy: 2 × ½mu^{2} + \\f{kQ^{2} − Gm^{2}}{4R} = \\f{kQ^{2} − Gm^{2}}{2R} (touching: centres 2R apart, speeds just zero).', 'mu^{2} = \\f{kQ^{2} − Gm^{2}}{4R} → u = √{\\f{kQ^{2}}{4mR}(1 − \\f{Gm^{2}}{kQ^{2}})}.'], 'pot', 3)
add(('2025', 'Jan', '2025-01-28', 1), 'pot', 'A particle of mass m and charge q is fastened to one end A of a massless string of length l, whose other end is fixed at point O. The whole system is placed on a frictionless horizontal plane and is initially at rest with OA making 60° with the x-axis. If a uniform electric field E is switched on along the +x direction, then the speed of the particle when it crosses the x-axis is',
    ['√{\\f{qEl}{2m}}', '√{\\f{qEl}{m}}', '√{\\f{2qEl}{m}}', '√{\\f{qEl}{4m}}'], 2,
    lambda: near([0.5 ** .5, 1, 2 ** .5, 0.5], swing()),
    ['The force qE along x does work as A swings down to the x-axis.', 'x-displacement = l − l cos 60° = \\f{l}{2} → ½mv^{2} = qE\\f{l}{2}.', 'v = √{\\f{qEl}{m}}.'], 'pot', 2)

# ---------------- Conductors ----------------
add(('2024', 'Apr', '2024-04-08', 1), 'pot', 'Two charged conducting spheres of radii a and b are connected to each other by a conducting wire. The ratio of charges of the two spheres respectively is:',
    ['√{ab}', 'ab', '\\f{a}{b}', '\\f{b}{a}'], 3, lambda: pick([math.sqrt(10), 10, 0.4, 2.5], (lambda a, b: a / b)(2, 5)),
    ['Joined spheres reach the same potential: \\f{kq_{1}}{a} = \\f{kq_{2}}{b}.', '\\f{q_{1}}{q_{2}} = \\f{a}{b}.'], 'cond', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'pot', 'Two charged conducting spheres S_{1} and S_{2} of radii 8 cm and 18 cm are connected to each other by a wire. After equilibrium is established, the ratio of electric fields on S_{1} and S_{2} spheres are E_{S1} and E_{S2} respectively. The value of \\f{E_{S1}}{E_{S2}} is ______ .',
    ['\\f{3}{2}', '\\f{2}{3}', '\\f{4}{9}', '\\f{9}{4}'], 4, lambda: pick([F(3, 2), F(2, 3), F(4, 9), F(9, 4)], (lambda r1, r2: (F(r1) / r1 ** 2) / (F(r2) / r2 ** 2))(8, 18)),
    ['Same potential → q ∝ r. Surface field E = \\f{kq}{r^{2}} ∝ \\f{1}{r}.', '\\f{E_{1}}{E_{2}} = \\f{18}{8} = \\f{9}{4}.'], 'cond', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'pot', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : The outer body of an air craft is made of metal which protects persons sitting inside from lightning-strikes. Reason (R): The electric field inside the cavity enclosed by a conductor is zero. In the light of the above statements, choose the most appropriate answer from the options given below :',
    AR4, 2, lambda: 2, ['A metal shell is an electrostatic shield: charge stays on the outer surface.', 'With no charge in the cavity, E inside = 0 — that is exactly why passengers are safe. Both true, R explains A.'], 'cond', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'pot', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : Net dipole moment of a polar linear isotropic dielectric substance is not zero even in the absence of an external electric field. Reason (R): In absence of an external electric field, the different permanent dipoles of a polar dielectric substance are oriented in random directions. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['(A) is correct but (R) is not correct', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)', 'Both (A) and (R) are correct but (R) is not the correct explanation of (A)', '(A) is not correct but (R) is correct'], 4,
    lambda: (lambda A, R: 4 if (not A and R) else 1)(abs(sum(math.cos(random.Random(s).uniform(0, 2 * math.pi)) for s in range(200000))) / 200000 > 0.05, True),
    ['Without a field, thermal motion points the molecular dipoles every which way: they add to (nearly) zero. A is false.', 'R correctly describes the random orientation. → (A) wrong, (R) right.'], 'cond', 1)

# ---------------- Capacitors ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'cap', 'Two identical capacitors have same capacitance C. One of them is charged to the potential V and other to the potential 2V. The negative ends of both are connected together. When the positive ends are also joined together, the decrease in energy of the combined system is :',
    ['\\f{1}{4}CV^{2}', '2CV^{2}', '\\f{1}{2}CV^{2}', '\\f{3}{4}CV^{2}'], 1, lambda: pick([F(1, 4), 2, F(1, 2), F(3, 4)], F(1, 2) * (1 + 4) - F(1, 2) * 2 * F(3, 2) ** 2),
    ['Charges C·V and C·2V share: common V = \\f{3CV}{2C} = \\f{3V}{2}.', 'Before: ½CV^{2} + ½C(2V)^{2} = \\f{5}{2}CV^{2}. After: ½(2C)(\\f{3V}{2})^{2} = \\f{9}{4}CV^{2}.', 'Loss = \\f{1}{4}CV^{2}.'], 'cap', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'cap', 'Using a battery, a 100 pF capacitor is charged to 60 V and then the battery is removed. After that, a second uncharged capacitor is connected to the first capacitor in parallel. If the final voltage across the second capacitor is 20 V , its capacitance is: (in pF )',
    ['600', '200', '100', '400'], 2, lambda: pick([600, 200, 100, 400], F(100 * 60, 20) - 100), ['Charge is conserved: 100 × 60 = 6000 pC.', 'Total C = \\f{6000}{20} = 300 pF → second = 200 pF.'], 'cap', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'cap', 'A capacitor, C_{1} = 6 μF is charged to a potential difference of V_{0} = 5 V using a 5 V battery. The battery is removed and another (uncharged) capacitor, C_{2} = 12 μF is connected across C_{1} through a switch S. When the switch S is closed, the charge flows between the capacitors for some time until equilibrium condition is reached. What are the charges (q_{1} and q_{2}) on the capacitors C_{1} and C_{2} when equilibrium condition is reached.',
    ['q_{1} = 10 μC, q_{2} = 20 μC', 'q_{1} = 30 μC, q_{2} = 15 μC', 'q_{1} = 20 μC, q_{2} = 10 μC', 'q_{1} = 15 μC, q_{2} = 30 μC'], 1,
    lambda: (lambda V: pick(['q_{1} = 10 μC, q_{2} = 20 μC', 'q_{1} = 30 μC, q_{2} = 15 μC', 'q_{1} = 20 μC, q_{2} = 10 μC', 'q_{1} = 15 μC, q_{2} = 30 μC'], f'q_{{1}} = {6 * V} μC, q_{{2}} = {12 * V} μC'))(F(30, 18)),
    ['Q = 6 × 5 = 30 μC is shared at a common voltage: V = \\f{30}{6 + 12} = \\f{5}{3} V.', 'q_{1} = 6 × \\f{5}{3} = 10 μC, q_{2} = 12 × \\f{5}{3} = 20 μC.'], 'cap', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'cap', 'Three capacitors of capacitances 25 μF, 30 μF and 45 μF are connected in parallel to a supply of 100 V. Energy stored in the above combination is E. When these capacitors are connected in series to the same supply, the stored energy is \\f{9}{x}E. The value of x is ______.',
    None, 86, lambda: int(9 * F(25 + 30 + 45) / (1 / (F(1, 25) + F(1, 30) + F(1, 45)))),
    ['Same V → energy ∝ C.', 'Parallel: 100 μF. Series: \\f{1}{C} = \\f{1}{25} + \\f{1}{30} + \\f{1}{45} = \\f{43}{450} → C = \\f{450}{43} μF.', 'Ratio = \\f{450/43}{100} = \\f{9}{86} → x = 86.'], 'cap', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'cap', 'Three parallel plate capacitors C_{1}, C_{2} and C_{3} each of capacitance 5 μF are connected so that C_{1} and C_{2} are in series between points A and B, and C_{3} is connected directly between A and B. The effective capacitance between points A and B, when the space between the parallel plates of C_{1} capacitor is filled with a dielectric medium having dielectric constant of 4, is :',
    ['9 μF', '7.5 μF', '30 μF', '22.5 μF'], 1, lambda: pick([9, F(15, 2), 30, F(45, 2)], 1 / (F(1, 20) + F(1, 5)) + 5), ['C_{1} → 4 × 5 = 20 μF.', 'C_{1}, C_{2} in series: \\f{20 × 5}{25} = 4 μF; plus C_{3}: 4 + 5 = 9 μF.'], 'cap', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'cap', 'A capacitor is made of a flat plate of area A and a second plate having a stair-like structure of three steps. The area of each stair is \\f{A}{3} and the steps are at distances d, 2d and 3d from the flat plate. The capacitance of the arrangement is:',
    ['\\f{11ε_{0}A}{18d}', '\\f{13ε_{0}A}{17d}', '\\f{11ε_{0}A}{20d}', '\\f{18ε_{0}A}{11d}'], 1, lambda: pick([F(11, 18), F(13, 17), F(11, 20), F(18, 11)], sum(F(1, 3) / n for n in (1, 2, 3))),
    ['Three capacitors side by side (parallel), each of area \\f{A}{3}.', 'C = \\f{ε_{0}A}{3}(\\f{1}{d} + \\f{1}{2d} + \\f{1}{3d}) = \\f{ε_{0}A}{3d} × \\f{11}{6} = \\f{11ε_{0}A}{18d}.'], 'cap', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'cap', 'Consider a parallel plate capacitor of area A (of each plate) and separation d between the plates. If E is the electric field and ε_{0} is the permittivity of free space between the plates, then potential energy stored in the capacitor is',
    ['\\f{1}{4}ε_{0}E^{2}Ad', '\\f{3}{4}ε_{0}E^{2}Ad', 'ε_{0}E^{2}Ad', '\\f{1}{2}ε_{0}E^{2}Ad'], 4, lambda: pick([F(1, 4), F(3, 4), 1, F(1, 2)], F(1, 2) * 1 * 1),
    ['U = ½CV^{2} with C = \\f{ε_{0}A}{d} and V = Ed.', 'U = ½ × \\f{ε_{0}A}{d} × E^{2}d^{2} = ½ε_{0}E^{2}Ad (energy density × volume).'], 'cap', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'cap', 'A parallel plate capacitor of capacitance 1 μF is charged to a potential difference of 20 V. The distance between plates is 1 μm. The energy density between plates of capacitor is.',
    ['2 × 10^{−4} J/m^{3}', '2 × 10^{2} J/m^{3}', '1.8 × 10^{3} J/m^{3}', '1.8 × 10^{5} J/m^{3}'], 3, lambda: near([math.log10(2e-4), 2.30103, math.log10(1.8e3), math.log10(1.8e5)], math.log10(0.5 * e0 * (20 / 1e-6) ** 2)),
    ['E = \\f{V}{d} = \\f{20}{10^{−6}} = 2 × 10^{7} V/m.', 'u = ½ε_{0}E^{2} = ½ × 8.85 × 10^{−12} × 4 × 10^{14} ≈ 1.8 × 10^{3} J/m^{3}.'], 'cap', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'cap', 'Identify the correct statements : A. Effective capacitance of a series combination of capacitors is always smaller than the smallest capacitance of the capacitor in the combination. B. When a dielectric medium is placed between the charged plates of a capacitor, displacement of charges cannot occur due to insulation property of dielectric. C. Increasing of area of capacitor plate or decreasing of thickness of dielectric is an alternate method to increase the capacitance. D. For a point charge, concentric spherical shells centered at the location of the charge are equipotential surfaces. Choose the correct answer from the options given below :',
    ['A, C and D Only', 'B and D Only', 'C and D Only', 'A, B and C Only'], 1, lambda: pick(['A, C and D Only', 'B and D Only', 'C and D Only', 'A, B and C Only'], 'A, C and D Only' if (1 / (1 / 2 + 1 / 3 + 1 / 7) < 2) else ''),
    ['A ✓: \\f{1}{C} = Σ\\f{1}{C_{i}} > \\f{1}{C_{min}}.', 'B ✗: a dielectric polarises — its bound charges do shift slightly.', 'C ✓: C = \\f{Kε_{0}A}{d}. D ✓: V = \\f{kq}{r} is the same on each sphere.'], 'cap', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'cap', 'An uncharged air capacitor (plates A and B), a resistor R, a key and a 5 V battery are connected in series. Identify the valid statements relevant to this circuit at the instant when the key is closed. A. There will be no current through resistor R. B. There will be maximum current in the connecting wires. C. Potential difference between the capacitor plates A and B is minimum. D. Charge on the capacitor plates is minimum. Choose the correct answer from the options given below:',
    ['C, D Only', 'B, C, D Only', 'A, B, D Only', 'A, C Only'], 2, lambda: pick(['C, D Only', 'B, C, D Only', 'A, B, D Only', 'A, C Only'], ', '.join(x for x, ok in (('A', 5 / 1 * math.exp(0) == 0), ('B', True), ('C', 5 * (1 - math.exp(0)) == 0), ('D', 1 - math.exp(0) == 0)) if ok) + ' Only'),
    ['At t = 0 the capacitor has no charge (q = 0) and so no voltage — it acts like a plain wire.', 'Then I = \\f{5}{R}, the largest it will ever be. So B, C, D are true and A is false.'], 'cap', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'cap', 'Two capacitors C_{1} and C_{2} are connected in parallel to a battery. Their charge–time graphs while charging show that C_{1} levels off at a smaller final charge than C_{2}. The energy stored with them are U_{1} and U_{2}, respectively. Which of the given statements is true?',
    ['C_{2} > C_{1}, U_{2} > U_{1}', 'C_{1} > C_{2}, U_{1} < U_{2}', 'C_{2} > C_{1}, U_{2} < U_{1}', 'C_{1} > C_{2}, U_{1} > U_{2}'], 1,
    lambda: (lambda q1, q2, V: pick(['C_{2} > C_{1}, U_{2} > U_{1}', 'C_{1} > C_{2}, U_{1} < U_{2}', 'C_{2} > C_{1}, U_{2} < U_{1}', 'C_{1} > C_{2}, U_{1} > U_{2}'], ('C_{2} > C_{1}' if q2 / V > q1 / V else 'C_{1} > C_{2}') + ', ' + ('U_{2} > U_{1}' if q2 * V > q1 * V else 'U_{2} < U_{1}')))(3, 5, 2),
    ['In parallel both get the same V. Final charge Q = CV → larger Q means larger C: C_{2} > C_{1}.', 'U = ½QV → U_{2} > U_{1}.'], 'cap', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'cap', 'A parallel plate air capacitor is connected to a battery. The plates are pulled apart at uniform speed v. If x is the separation between the plates at any instant, then the time rate of change of electrostatic energy of the capacitor is proportional to x^{α}, where α is ______.',
    ['−2', '1', '−1', '2'], 1, lambda: pick([-2, 1, -1, 2], round(math.log(((1 / 2.0 - 1 / 2.001) / 0.001) / ((1 / 4.0 - 1 / 4.001) / 0.001)) / math.log(2 / 4))),
    ['V fixed: U = ½CV^{2} = \\f{ε_{0}AV^{2}}{2x}.', '\\f{dU}{dt} = −\\f{ε_{0}AV^{2}}{2x^{2}} × \\f{dx}{dt} = −\\f{ε_{0}AV^{2}v}{2x^{2}} ∝ x^{−2}.'], 'cap', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'cap', 'At steady state the charge on the capacitor, as shown in the circuit below, is ___ μC. Circuit: a 10 Ω and a 15 Ω resistor are in series across a 5 V battery, and an 8 μF capacitor is connected across the 10 Ω resistor.',
    None, 16, lambda: round(8 * abs((lambda V: V['a'] - V['m'])(solve_dc([('a', 'm', 10), ('m', 'g', 15)], [('g', 'a', 5, F(1, 10 ** 9))], 'g')))),
    ['At steady state no current enters the capacitor; I = \\f{5}{25} = 0.2 A.', 'V across 10 Ω = 2 V → Q = 8 × 2 = 16 μC.'], 'cap', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'cap', 'The charge accumulated on the capacitor connected in the following circuit is ______ μC (Given C = 150 μF). Circuit: a 10 V battery is connected between junctions P (+) and Q (−). Between P and Q there are two branches: R_{1} = 1 Ω from P to A then R_{2} = 2 Ω from A to Q; and R_{3} = 6 Ω from P to B then R_{4} = 4 Ω from B to Q. The capacitor C is connected between A and B.',
    None, 400, lambda: round(150 * abs((lambda V: V['A'] - V['B'])(solve_dc([('P', 'A', 1), ('A', 'Q', 2), ('P', 'B', 6), ('B', 'Q', 4)], [('Q', 'P', 10, F(1, 10 ** 9))], 'Q')))),
    ['Steady state: no current through C. Left branch: V_{A} = 10 × \\f{2}{3} = \\f{20}{3} V (above Q).', 'Right branch: V_{B} = 10 × \\f{4}{10} = 4 V.', 'Q = 150 × (\\f{20}{3} − 4) = 150 × \\f{8}{3} = 400 μC.'], 'cap', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'cap', 'A wire of resistance 16 Ω is bent to form a square loop. A 9 V battery with internal resistance 1 Ω is connected across one of its sides. If a 4 μF capacitor is connected across one of its diagonals, the energy stored by the capacitor will be \\f{x}{2} μJ, where x = ______.',
    None, 81, lambda: int(2 * F(1, 2) * 4 * (lambda V: (V['a'] - V['c']) ** 2)(solve_dc([('a', 'b', 4), ('b', 'c', 4), ('c', 'd', 4), ('d', 'a', 4)], [('b', 'a', 9, 1)], 'b'))),
    ['Each side 4 Ω. The battery\'s side (4 Ω) is in parallel with the other three (12 Ω): 3 Ω, plus 1 Ω inside → I = \\f{9}{4} A, terminal V = \\f{27}{4} V.', 'Along the 12 Ω path each side drops \\f{27}{4} × \\f{4}{12} = \\f{9}{4} V; a diagonal spans two sides: \\f{9}{2} V.', 'U = ½ × 4 × (\\f{9}{2})^{2} = \\f{81}{2} μJ → x = 81.'], 'cap', 3)

# ---------------- Dielectrics ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'cap', 'A parallel plate capacitor is filled equally (half) with two dielectrics of dielectric constants ε_{1} and ε_{2}. The distance between the plates is d and area of each plate is A. First configuration: the dielectrics are two layers, each of thickness d/2 covering the whole plate area. Second configuration: they sit side by side, each filling half the plate area across the full gap d. If capacitance in first configuration and second configuration are C_{1} and C_{2} respectively, then \\f{C_{1}}{C_{2}} is',
    ['\\f{ε_{1}ε_{2}^{2}}{(ε_{1} + ε_{2})^{2}}', '\\f{ε_{1}ε_{2}}{ε_{1} + ε_{2}}', '\\f{4ε_{1}ε_{2}}{(ε_{1} + ε_{2})^{2}}', '\\f{ε_{0}(ε_{1} + ε_{2})}{2}'], 3,
    lambda: (lambda a, b: near([a * b * b / (a + b) ** 2, a * b / (a + b), 4 * a * b / (a + b) ** 2, (a + b) / 2], (1 / (0.5 / a + 0.5 / b)) / (0.5 * a + 0.5 * b)))(2.0, 5.0),
    ['Layers = series: C_{1} = \\f{2ε_{0}A}{d} × \\f{ε_{1}ε_{2}}{ε_{1} + ε_{2}}.', 'Side by side = parallel: C_{2} = \\f{ε_{0}A}{2d}(ε_{1} + ε_{2}).', '\\f{C_{1}}{C_{2}} = \\f{4ε_{1}ε_{2}}{(ε_{1} + ε_{2})^{2}}.'], 'diel', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'cap', 'Space between the plates of a parallel plate capacitor of plate area 4 cm^{2} and separation of (d) 1.77 mm, is filled with uniform dielectric materials with dielectric constants 3 and 5 as two layers, each of thickness d/2 covering the whole plate area. Another capacitor of capacitance 7.5 pF is connected in parallel with it. The effective capacitance of this combination is ______ pF. (Given ε_{0} = 8.85 × 10^{−12} F/m)',
    None, 15, lambda: round(e0 * 4e-4 / (0.885e-3 / 3 + 0.885e-3 / 5) * 1e12 + 7.5),
    ['ε_{0}A/d = \\f{8.85 × 10^{−12} × 4 × 10^{−4}}{1.77 × 10^{−3}} = 2 pF.', 'Two layers in series: C = \\f{2 × 2 × 3 × 5}{3 + 5} = 7.5 pF.', 'With 7.5 pF in parallel: 15 pF.'], 'diel', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'cap', 'A parallel plate capacitor of capacitance 12.5 pF is charged by a battery connected between its plates to potential difference of 12.0 V. The battery is now disconnected and a dielectric slab (ε_{r} = 6) is inserted between the plates. The change in its potential energy after inserting the dielectric slab is ______ × 10^{−12} J.',
    None, 750, lambda: round((lambda Q: Q * Q / (2 * 12.5) - Q * Q / (2 * 75))(12.5 * 12)),
    ['Battery off → Q stays 150 pC. U = \\f{Q^{2}}{2C}.', 'Before: ½ × 12.5 × 144 = 900 pJ. After (C × 6): 150 pJ.', 'Change = 750 × 10^{−12} J (a decrease).'], 'diel', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'cap', 'A parallel plate capacitor has charge 5 × 10^{−6} C. A dielectric slab is inserted between the plates and almost fills the space between the plates. If the induced charge on one face of the slab is 4 × 10^{−6} C then the dielectric constant of the slab is ____ .',
    None, 5, lambda: round(bisect(lambda K: 5 * (1 - 1 / K) - 4, 1.0001, 100)), ['Induced charge Q_{i} = Q(1 − \\f{1}{K}).', '4 = 5(1 − \\f{1}{K}) → K = 5.'], 'diel', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'cap', 'A capacitor has air as dielectric medium and two conducting plates of area 12 cm^{2} and they are 0.6 cm apart. When a slab of dielectric having area 12 cm^{2} and 0.6 cm thickness is inserted between the plates, one of the conducting plates has to be moved by 0.2 cm to keep the capacitance same as in previous case. The dielectric constant of the slab is : (Given ε_{0} = 8.834 × 10^{−12} F/m)',
    ['1.50', '1.33', '0.66', '1'], 1, lambda: near([1.5, 1.33, 0.66, 1], bisect(lambda K: 1 / (0.002 + 0.006 / K) - 1 / 0.006, 1.0001, 50)),
    ['The plate moves out to 0.8 cm. Same C: 0.6 = (0.8 − 0.6) + \\f{0.6}{K}.', '\\f{0.6}{K} = 0.4 → K = 1.5.'], 'diel', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'cap', 'A parallel plate air capacitor has a capacitance C. When it is half filled with a dielectric constant K = 5 (a slab of thickness d/2 covering the whole plate area), the percentage increase in the capacitance is ______ .',
    ['33.34', '66.67', '200', '400'], 2, lambda: near([33.34, 66.67, 200, 400], 100 * (1 / (0.5 + 0.5 / 5) - 1)),
    ['C′ = \\f{ε_{0}A}{d/2 + d/(2 × 5)} = \\f{ε_{0}A}{0.6d} = \\f{5}{3}C.', 'Increase = 66.67 %.'], 'diel', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'cap', 'A parallel plate capacitor has capacitance C, when there is vacuum within the parallel plates. A sheet having thickness (\\f{1}{3})^{rd} of the separation between the plates and relative permittivity K is introduced between the plates. The new capacitance of the system is :',
    ['\\f{3KC}{2K + 1}', '\\f{CK}{2 + K}', '\\f{3CK^{2}}{(2K + 1)^{2}}', '\\f{4KC}{3K − 1}'], 1, lambda: (lambda K: near([3 * K / (2 * K + 1), K / (2 + K), 3 * K * K / (2 * K + 1) ** 2, 4 * K / (3 * K - 1)], 1 / (2 / 3 + 1 / (3 * K))))(4.0),
    ['C′ = \\f{ε_{0}A}{d − t + t/K} with t = \\f{d}{3}.', '= \\f{ε_{0}A}{d(\\f{2}{3} + \\f{1}{3K})} = \\f{3KC}{2K + 1}.'], 'diel', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'cap', 'A parallel-plate capacitor of capacitance 40 μF is connected to a 100 V power supply. Now the intermediate space between the plates is filled with a dielectric material of dielectric constant K = 2. Due to the introduction of dielectric material, the extra charge and the change in the electrostatic energy in the capacitor, respectively, are',
    ['8 mC and 2.0 J', '4 mC and 0.2 J', '2 mC and 0.4 J', '2 mC and 0.2 J'], 2,
    lambda: pick(['8 mC and 2.0 J', '4 mC and 0.2 J', '2 mC and 0.4 J', '2 mC and 0.2 J'], f'{round((80 - 40) * 100 / 1000)} mC and {round(0.5 * (80 - 40) * 1e-6 * 100 ** 2, 1)} J'),
    ['Battery stays on → V = 100 V fixed; C → 80 μF.', 'ΔQ = 40 μF × 100 V = 4 mC.', 'ΔU = ½(80 − 40) × 10^{−6} × 100^{2} = 0.2 J.'], 'diel', 1)
