"""Real JEE Main questions — Physics Unit 6: Gravitation. Our own solutions; chk re-solves each.
Skipped: dimension-only questions (they belong to Unit 1), 22-1-25 S1 Q18 (cavity position only in the figure),
23-1-25 S1 Q25 (dropped by NTA — bonus)."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
G = 6.67e-11
AR = ['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is true but R is false', 'A is false but R is true']
ST = ['Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true']

# ---------- Newton's law, superposition, field ----------
add(('2024', 'Feb', '2024-02-01', 2), 'law', 'A light planet is revolving around a massive star in a circular orbit of radius R with a period of revolution T. If the force of attraction between planet and star is proportional to R^{−3/2} then choose the correct option :',
    ['T^{2} ∝ R^{5/2}', 'T^{2} ∝ R^{7/2}', 'T^{2} ∝ R^{3/2}', 'T^{2} ∝ R^{3}'], 1, lambda: pick(['T^{2} ∝ R^{5/2}', 'T^{2} ∝ R^{7/2}', 'T^{2} ∝ R^{3/2}', 'T^{2} ∝ R^{3}'], f'T^{{2}} ∝ R^{{{F(1) + F(3, 2)}}}'.replace('5/2}', '5/2}')),
    ['Gravity supplies the centripetal force: mω^{2}R ∝ R^{−3/2} → ω^{2} ∝ R^{−5/2}.', 'T = \\f{2π}{ω} → T^{2} ∝ R^{5/2}.'], 'law', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'law', 'A 90 kg body placed at 2R distance from surface of earth experiences gravitational pull of : (R = Radius of earth, g = 10 m s^{−2})',
    ['300 N', '225 N', '120 N', '100 N'], 4, lambda: pick([300, 225, 120, 100], 90 * 10 / 9), ['Distance from the centre = R + 2R = 3R → force falls by 3^{2} = 9.', 'F = \\f{90 × 10}{9} = 100 N.'], 'law', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'law', 'A metal wire of uniform mass density having length L and mass M is bent to form a semicircular arc and a particle of mass m is placed at the centre of the arc. The gravitational force on the particle by the wire is :',
    ['\\f{GMmπ}{2L^{2}}', '0', '\\f{GmMπ^{2}}{L^{2}}', '\\f{2GmMπ}{L^{2}}'], 4,
    lambda: (lambda r, lam: near([math.pi / 2, 0, math.pi ** 2, 2 * math.pi], sum(lam * (r * math.pi / 2000) / r ** 2 * math.sin((k + 0.5) * math.pi / 2000) for k in range(2000))))(1 / math.pi, 1.0),
    ['Radius r = \\f{L}{π}, mass per length λ = \\f{M}{L}.', 'For a semicircle the sideways parts cancel; the field at the centre is \\f{2Gλ}{r}.', 'F = m × \\f{2G(M/L)}{L/π} = \\f{2GMmπ}{L^{2}}.'], 'law', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'law', 'In hydrogen like system the ratio of coulombian force and gravitational force between an electron and a proton is in the order of:',
    ['10^{39}', '10^{19}', '10^{29}', '10^{36}'], 1, lambda: pick([39, 19, 29, 36], round(math.log10(9e9 * (1.6e-19) ** 2 / (G * 9.1e-31 * 1.67e-27)))),
    ['Both forces ∝ \\f{1}{r^{2}}, so r cancels.', '\\f{ke^{2}}{Gm_{e}m_{p}} = \\f{9 × 10^{9} × (1.6 × 10^{−19})^{2}}{6.67 × 10^{−11} × 9.1 × 10^{−31} × 1.67 × 10^{−27}} ≈ 2.3 × 10^{39}.'], 'law', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'law', 'Three identical spheres of mass m, are placed at the vertices of an equilateral triangle of length a. When released, they interact only through gravitational force and collide after a time T = 4 seconds. If the sides of the triangle are increased to length 2a and also the masses of the spheres are made 2m, then they will collide after ______ seconds.',
    None, 8, lambda: round(4 * math.sqrt(2 ** 3 / 2)),
    ['Only G, m and a can set the time: by dimensions t ∝ √{\\f{a^{3}}{Gm}}.', 'a × 2 and m × 2 → t × √{\\f{8}{2}} = 2 → 8 s.'], 'law', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'law', 'Net gravitational force at the center of a square is found to be F_{1} when four particles having mass M, 2M, 3M and 4M are placed at the four corners of the square (M bottom-left, 2M bottom-right, 3M top-right, 4M top-left) and it is F_{2} when the positions of 3M and 4M are interchanged. The ratio \\f{F_{1}}{F_{2}} is \\f{α}{√{5}}. The value of α is ______.',
    ['2', '3', '1', '2√{5}'], 1, lambda: pick([2, 3, 1, 2 * math.sqrt(5)], round(math.hypot(3 - 1, 4 - 2) / math.hypot(4 - 1, 3 - 2) * math.sqrt(5), 9)),
    ['Each mass pulls the centre-particle along its diagonal with force ∝ its mass (same distance).', 'F_{1}: diagonals M↔3M and 2M↔4M → net 2M and 2M at right angles → 2√{2}M.', 'F_{2}: M↔4M → 3M, 2M↔3M → M → √{10}M. Ratio = \\f{2√{2}}{√{10}} = \\f{2}{√{5}} → α = 2.'], 'law', 2)
add(('2024', 'Jan', '2024-01-31', 1), 'law', 'Four identical particles of mass m are kept at the four corners of a square. If the gravitational force exerted on one of the masses by the other masses is (\\f{2√{2} + 1}{32})\\f{Gm^{2}}{L^{2}}, the length of the sides of the square is',
    ['L/2', '4 L', '3 L', '2 L'], 2, lambda: pick([0.5, 4, 3, 2], round(math.sqrt((math.sqrt(2) + 0.5) / ((2 * math.sqrt(2) + 1) / 32)), 9)),
    ['On one corner (side a): two neighbours give \\f{Gm^{2}}{a^{2}} each at 90° → √{2}\\f{Gm^{2}}{a^{2}}; the far corner adds \\f{Gm^{2}}{2a^{2}} along the same diagonal.', 'Total = \\f{2√{2} + 1}{2}\\f{Gm^{2}}{a^{2}} = \\f{2√{2} + 1}{32}\\f{Gm^{2}}{L^{2}} → a^{2} = 16L^{2} → a = 4L.'], 'law', 2)

# ---------- g: height, depth, shape of earth ----------
add(('2024', 'Feb', '2024-02-01', 1), 'g', "If R is the radius of the earth and the acceleration due to gravity on the surface of earth is g = π^{2} m/s^{2}, then the length of the second's pendulum at a height h = 2R from the surface of earth will be,:",
    ['\\f{2}{9} m', '\\f{1}{9} m', '\\f{4}{9} m', '\\f{8}{9} m'], 2, lambda: pick([F(2, 9), F(1, 9), F(4, 9), F(8, 9)], F(1, 9) * 4 / 4),
    ["A second's pendulum has T = 2 s → L = \\f{gT^{2}}{4π^{2}}.", 'At h = 2R, r = 3R → g′ = \\f{g}{9} = \\f{π^{2}}{9}.', 'L = \\f{(π^{2}/9) × 4}{4π^{2}} = \\f{1}{9} m.'], 'gvar', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'g', 'A simple pendulum doing small oscillations at a place R height above earth surface has time period of T_{1} = 4 s. T_{2} would be its time period if it is brought to a point which is at a height 2R from earth surface. Choose the correct relation [R = radius of Earth]:',
    ['T_{1} = T_{2}', '2T_{1} = 3T_{2}', '3T_{1} = 2T_{2}', '2T_{1} = T_{2}'], 3, lambda: pick(['1', '2/3', '3/2', '2'], str(F(3, 2))),
    ['T ∝ \\f{1}{√{g}} and g ∝ \\f{1}{r^{2}} → T ∝ r.', 'r goes from 2R to 3R → T_{2} = \\f{3}{2}T_{1} → 3T_{1} = 2T_{2}.'], 'gvar', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'g', 'If the radius of earth is reduced to three-fourth of its present value without change in its mass then value of duration of the day of earth will be ______ hours 30 minutes.',
    None, 13, lambda: int(24 * F(9, 16)),
    ['No outside torque → angular momentum Iω is constant; I = \\f{2}{5}MR^{2}.', 'T ∝ R^{2} → T = 24 × \\f{9}{16} = 13.5 h = 13 hours 30 minutes.'], 'gvar', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'g', "Acceleration due to gravity on the surface of earth is 'g'. If the diameter of earth is reduced to one third of its original value and mass remains unchanged, then the acceleration due to gravity on the surface of the earth is ______ g.",
    None, 9, lambda: 3 ** 2, ['g = \\f{GM}{R^{2}}: R becomes R/3.', 'g′ = 9g.'], 'gvar', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'g', 'The acceleration due to gravity on the surface of earth is g. If the diameter of earth reduces to half of its original value and mass remains constant, then acceleration due to gravity on the surface of earth would be :',
    ['g/4', '2 g', 'g/2', '4 g'], 4, lambda: pick([0.25, 2, 0.5, 4], 2 ** 2), ['g ∝ \\f{1}{R^{2}} → halving R makes g four times.'], 'gvar', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'g', 'The gravitational potential at a point above the surface of earth is −5.12 × 10^{7} J/kg and the acceleration due to gravity at that point is 6.4 m/s^{2}. Assume that the mean radius of earth to be 6400 km. The height of this point above the earth\'s surface is :',
    ['1600 km', '540 km', '1200 km', '1000 km'], 1, lambda: pick([1600, 540, 1200, 1000], round(5.12e7 / 6.4 / 1000 - 6400)),
    ['V = −\\f{GM}{r}, g = \\f{GM}{r^{2}} → r = \\f{|V|}{g} = \\f{5.12 × 10^{7}}{6.4} = 8 × 10^{6} m.', 'h = 8000 − 6400 = 1600 km.'], 'gvar', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'g', "A simple pendulum is placed at a place where its distance from the earth's surface is equal to the radius of the earth. If the length of the string is 4 m, then the time period of small oscillations will be ______ s. [take g = π^{2} m s^{−2}]",
    None, 8, lambda: round(2 * math.pi * math.sqrt(4 / (math.pi ** 2 / 4))), ['At h = R, g′ = \\f{g}{4} = \\f{π^{2}}{4}.', 'T = 2π√{\\f{4}{π^{2}/4}} = 2π × \\f{4}{π} = 8 s.'], 'gvar', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'g', "The height in terms of radius of the earth (R), at which the acceleration due to gravity becomes \\f{g}{9}, where g is acceleration due to gravity on earth's surface, is",
    ['√{3}R', '2√{2}R', '2R', '\\f{4}{9}R'], 3, lambda: pick(['√{3}R', '2√{2}R', '2R', '\\f{4}{9}R'], f'{math.isqrt(9) - 1}R'), ['g′ = g(\\f{R}{R + h})^{2} = \\f{g}{9} → R + h = 3R → h = 2R.'], 'gvar', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'g', "When one moves from a point 16 km below the earth's surface to a point 16 km above the earth's surface. The change in g is approximately α%. The value of α is ______. (Take radius of the earth = 6400 km)",
    ['0.12', '0.25', '0.50', '0.75'], 2, lambda: near([0.12, 0.25, 0.50, 0.75], 100 * ((1 - 16 / 6400) - (1 - 2 * 16 / 6400))),
    ['Below: g(1 − \\f{d}{R}) = g(1 − 0.0025). Above (h ≪ R): g(1 − \\f{2h}{R}) = g(1 − 0.005).', 'Change = 0.0025g = 0.25% of g.'], 'gvar', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'g', 'Assertion (A): A simple pendulum is taken to a planet of mass and radius, 4 times and 2 times, respectively, than the Earth. The time period of the pendulum remains same on earth and the planet. Reason (R): The mass of the pendulum remains unchanged at Earth and the other planet. In the light of the above statements, choose the correct answer from the options given below :',
    ['(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)', '(A) is false but (R) is true'], 3, lambda: 3 if F(4, 2 ** 2) == 1 else 0,
    ['g on the planet = \\f{G(4M)}{(2R)^{2}} = g → same period: A is true.', 'R is true, but T = 2π√{L/g} does not depend on the bob\'s mass — R does not explain A.'], 'gvar', 1)

# ---------- energy and escape ----------
add(('2025', 'Apr', '2025-04-04', 1), 'pot', 'Assertion A: The kinetic energy needed to project a body of mass m from earth surface to infinity is \\f{1}{2}mgR, where R is the radius of earth. Reason R: The maximum potential energy of a body is zero when it is projected to infinity from earth surface.',
    ['A is false but R is true', 'Both A and R are true but R is NOT the correct explanation of A', 'A is true but R is false', 'Both A and R are true and R is the correct explanation of A'], 1, lambda: 1 if F(1) != F(1, 2) else 0,
    ['Energy needed = 0 − (−\\f{GMm}{R}) = \\f{GMm}{R} = mgR, not ½mgR: A is false.', 'Potential energy −\\f{GMm}{r} rises to its maximum 0 at infinity: R is true.'], 'escape', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'pot', "An object is kept at rest at a distance of 3R above the earth's surface where R is earth's radius. The minimum speed with which it must be projected so that it does not return to earth is: (Assume M = mass of earth, G = Universal gravitational constant)",
    ['√{\\f{GM}{R}}', '√{\\f{3GM}{R}}', '√{\\f{GM}{2R}}', '√{\\f{2GM}{R}}'], 3, lambda: near([1, 3 ** 0.5, 0.5 ** 0.5, 2 ** 0.5], math.sqrt(2 / 4)),
    ['From r = R + 3R = 4R: ½mv^{2} = \\f{GMm}{4R}.', 'v = √{\\f{GM}{2R}}.'], 'escape', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'pot', "To project a body of mass m from earth's surface to infinity, the required kinetic energy is (assume, the radius of earth is R_{E}, g = acceleration due to gravity on the surface of earth) :",
    ['2mgR_{E}', 'mgR_{E}', '\\f{1}{2}mgR_{E}', '4mgR_{E}'], 2, lambda: 2, ['KE needed = \\f{GMm}{R_{E}} = mgR_{E} (since GM = gR_{E}^{2}).'], 'escape', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'pot', 'If a body of mass 1 kg falls on the earth from infinity, it attains velocity (v) and kinetic energy (k) on reaching the surface of earth. The values of v and k respectively are ______. (Take radius of earth to be 6400 km and g = 9.8 m/s^{2})',
    ['11.2 km/s; 6.27 × 10^{7} J', '11.2 km/s; 12.54 × 10^{7} J', '8.8 km/s; 6.27 × 10^{7} J', '8.8 km/s; 12.54 × 10^{7} J'], 1, lambda: near([11.2 + 6.27, 11.2 + 12.54, 8.8 + 6.27, 8.8 + 12.54], math.sqrt(2 * 9.8 * 6.4e6) / 1000 + 9.8 * 6.4e6 / 1e7),
    ['Falling from infinity: ½mv^{2} = mgR → v = √{2gR} = √{2 × 9.8 × 6.4 × 10^{6}} = 11.2 km/s.', 'k = mgR = 9.8 × 6.4 × 10^{6} = 6.27 × 10^{7} J.'], 'escape', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'pot', 'A body of mass m is taken from the surface of earth to a height equal to twice the radius of earth (R_{e}). The increase in potential energy will be ______. (g is acceleration due to gravity at the surface of earth)',
    ['\\f{1}{2}mgR_{e}', '\\f{3}{4}mgR_{e}', '\\f{1}{4}mgR_{e}', '\\f{2}{3}mgR_{e}'], 4, lambda: pick([F(1, 2), F(3, 4), F(1, 4), F(2, 3)], 1 - F(1, 3)),
    ['ΔU = GMm(\\f{1}{R} − \\f{1}{3R}) = \\f{2}{3}\\f{GMm}{R} = \\f{2}{3}mgR_{e}.'], 'escape', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'pot', 'Earth has mass 8 times and radius 2 times that of a planet. If the escape velocity from the earth is 11.2 km/s, the escape velocity in km/s from the planet will be :',
    ['8.4', '5.6', '11.2', '2.8'], 2, lambda: pick([8.4, 5.6, 11.2, 2.8], round(11.2 / math.sqrt(8 / 2), 9)), ['v_{e} = √{\\f{2GM}{R}} ∝ √{\\f{M}{R}}.', 'Earth/planet = √{8/2} = 2 → planet: 5.6 km/s.'], 'escape', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'pot', 'The escape velocity from a spherical planet A is 10 km/s. The escape velocity from another planet B whose density and radius are 10% of those of planet A, is ______ m/s.',
    ['1000', '200√{5}', '100√{10}', '1000√{2}'], 3, lambda: near([1000, 200 * 5 ** 0.5, 100 * 10 ** 0.5, 1000 * 2 ** 0.5], 10000 * 0.1 * math.sqrt(0.1)),
    ['M = \\f{4}{3}πR^{3}ρ → v_{e} = √{\\f{2GM}{R}} ∝ R√{ρ}.', 'v_{B} = 10000 × 0.1 × √{0.1} = 316 m/s = 100√{10} m/s.'], 'escape', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'pot', 'Escape velocity of a body from earth is 11.2 km/s. If the radius of a planet be one-third the radius of earth and mass be one-sixth that of earth, the escape velocity from the plate is:',
    ['11.2 km/s', '8.4 km/s', '4.2 km/s', '7.9 km/s'], 4, lambda: near([11.2, 8.4, 4.2, 7.9], 11.2 * math.sqrt((1 / 6) / (1 / 3))), ['v_{e} ∝ √{\\f{M}{R}} = √{\\f{1/6}{1/3}} = \\f{1}{√{2}}.', '11.2/√{2} ≈ 7.9 km/s.'], 'escape', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'pot', 'The mass of the moon is 1/144 times the mass of a planet and its diameter 1/16 times the diameter of a planet. If the escape velocity on the planet is v, the escape velocity on the moon will be:',
    ['\\f{v}{3}', '\\f{v}{4}', '\\f{v}{12}', '\\f{v}{6}'], 1, lambda: pick([F(1, 3), F(1, 4), F(1, 12), F(1, 6)], F(math.isqrt(16 * 1), math.isqrt(144 * 1))), ['v_{e} ∝ √{\\f{M}{R}} = √{\\f{1/144}{1/16}} = √{\\f{1}{9}} = \\f{1}{3}.'], 'escape', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'pot', 'Three masses 200 kg, 300 kg and 400 kg are placed at the vertices of an equilateral triangle with sides 20 m. They are rearranged on the vertices of a bigger triangle of side 25 m and with the same centre. The work done in this process ______ J. (Gravitational constant G = 6.7 × 10^{−11} N m^{2}/kg^{2})',
    ['9.86 × 10^{−6}', '2.85 × 10^{−7}', '1.74 × 10^{−7}', '4.77 × 10^{−7}'], 3, lambda: near([9.86e-6, 2.85e-7, 1.74e-7, 4.77e-7], 6.7e-11 * (200 * 300 + 300 * 400 + 200 * 400) * (1 / 20 - 1 / 25)),
    ['W = ΔU = Gm_{i}m_{j} sum × (\\f{1}{20} − \\f{1}{25}).', 'Σm_{i}m_{j} = 60000 + 120000 + 80000 = 2.6 × 10^{5}; W = 6.7 × 10^{−11} × 2.6 × 10^{5} × 0.01 = 1.74 × 10^{−7} J.'], 'escape', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'pot', 'Consider two identical metallic spheres of radius R each having charge Q and mass m. Their centers have an initial separation of 4R. Both the spheres are given an initial speed of u towards each other. The minimum value of u, so that they can just touch each other is : (Take k = \\f{1}{4πε_{0}} and assume kQ^{2} > Gm^{2} where G is the Gravitational constant)',
    ['√{\\f{kQ^{2}}{4mR}(1 − \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{4mR}(1 + \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{2mR}(1 − \\f{Gm^{2}}{kQ^{2}})}', '√{\\f{kQ^{2}}{2mR}(1 − \\f{Gm^{2}}{2kQ^{2}})}'], 1,
    lambda: (lambda k, Gm2, m, R: near([math.sqrt(k / (4 * m * R) * (1 - Gm2 / k)), math.sqrt(k / (4 * m * R) * (1 + Gm2 / k)), math.sqrt(k / (2 * m * R) * (1 - Gm2 / k)), math.sqrt(k / (2 * m * R) * (1 - Gm2 / (2 * k)))], math.sqrt((k - Gm2) * (1 / (2 * R) - 1 / (4 * R)) / m)))(5.0, 2.0, 1.0, 1.0),
    ['Net repulsion energy U(r) = \\f{kQ^{2} − Gm^{2}}{r}; touching means r goes from 4R to 2R.', '2 × ½mu^{2} = (kQ^{2} − Gm^{2})(\\f{1}{2R} − \\f{1}{4R}) → u = √{\\f{kQ^{2}}{4mR}(1 − \\f{Gm^{2}}{kQ^{2}})}.'], 'escape', 3)

# ---------- satellites & Kepler ----------
add(('2025', 'Apr', '2025-04-02', 2), 'orbit', "A satellite of mass 1000 kg is launched to revolve around the earth in an orbit at a height of 270 km from the earth's surface. Kinetic energy of the satellite in this orbit is ______ × 10^{10} J. (Mass of earth = 6 × 10^{24} kg, Radius of earth = 6.4 × 10^{6} m, Gravitational constant = 6.67 × 10^{−11} N m^{2} kg^{−2})",
    None, 3, lambda: round(G * 6e24 * 1000 / (2 * (6.4e6 + 2.7e5)) / 1e10), ['r = 6.4 × 10^{6} + 0.27 × 10^{6} = 6.67 × 10^{6} m.', 'KE = \\f{GMm}{2r} = \\f{6.67 × 10^{−11} × 6 × 10^{24} × 1000}{2 × 6.67 × 10^{6}} = 3 × 10^{10} J.'], 'orbit', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'orbit', "Correct formula for height of a satellite from earth's surface is:",
    ['(\\f{T^{2}R^{2}g}{4π})^{1/2} − R', '(\\f{T^{2}R^{2}g}{4π^{2}})^{1/3} − R', '(\\f{T^{2}R^{2}}{4π^{2}g})^{1/3} − R', '(\\f{T^{2}R^{2}}{4π^{2}})^{−1/3} + R'], 2, lambda: 2,
    ['T^{2} = \\f{4π^{2}r^{3}}{GM} with GM = gR^{2} → r^{3} = \\f{T^{2}gR^{2}}{4π^{2}}.', 'h = r − R = (\\f{T^{2}R^{2}g}{4π^{2}})^{1/3} − R.'], 'orbit', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'orbit', 'A satellite revolving around a planet in stationary orbit has time period 6 hours. The mass of planet is one-fourth the mass of earth. The radius orbit of planet is : (Given = Radius of geo-stationary orbit for earth is 4.2 × 10^{4} km)',
    ['1.4 × 10^{4} km', '8.4 × 10^{4} km', '1.68 × 10^{5} km', '1.05 × 10^{4} km'], 4, lambda: near([1.4e4, 8.4e4, 1.68e5, 1.05e4], 4.2e4 * ((1 / 4) * (6 / 24) ** 2) ** (1 / 3)),
    ['r^{3} ∝ MT^{2}.', 'r^{3} = (4.2 × 10^{4})^{3} × \\f{1}{4} × (\\f{6}{24})^{2} = \\f{(4.2 × 10^{4})^{3}}{64} → r = 1.05 × 10^{4} km.'], 'orbit', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'orbit', 'Match List-I with List-II (a = radius of planet orbit, r = radius of planet, M mass of Sun, m = mass of planet): (A) Kinetic energy of planet (B) Gravitation potential energy of Sun-planet system (C) Total mechanical energy of planet (D) Escape energy at the surface of planet for unit mass object — (I) −\\f{GMm}{a} (II) \\f{GMm}{2a} (III) \\f{Gm}{r} (IV) −\\f{GMm}{2a}',
    ['(A)-II, (B)-I, (C)-IV, (D)-III', '(A)-III, (B)-IV, (C)-I, (D)-II', '(A)-I, (B)-IV, (C)-II, (D)-III', '(A)-I, (B)-II, (C)-III, (D)-IV'], 1, lambda: 1,
    ['KE = \\f{GMm}{2a} (II); PE = −\\f{GMm}{a} (I); total = −\\f{GMm}{2a} (IV).', 'Escape energy per unit mass from the planet\'s surface = \\f{Gm}{r} (III).'], 'orbit', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'orbit', 'Assertion (A): The radius vector from the Sun to a planet sweeps out equal areas in equal intervals of time and thus areal velocity of planet is constant. Reason (R): For a central force field the angular momentum is a constant.',
    ['(A) is not correct but (R) is correct', '(A) is correct but (R) is not correct', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)', 'Both (A) and (R) are correct but (R) is not the correct explanation of (A)'], 3, lambda: 3,
    ['Areal velocity = \\f{L}{2m}. A central force has no torque about the Sun → L constant → equal areas in equal times.', 'Both true and R explains A.'], 'orbit', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'orbit', 'Two satellite A and B go round a planet in circular orbits having radii 4R and R respectively. If the speed of A is 3v, the speed of B will be :',
    ['\\f{4}{3}v', '3v', '6v', '12v'], 3, lambda: pick([F(4, 3), 3, 6, 12], 3 * math.isqrt(4)), ['v = √{\\f{GM}{r}} ∝ \\f{1}{√{r}}.', 'v_{B} = 3v × √{\\f{4R}{R}} = 6v.'], 'orbit', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'orbit', 'Two planets A and B having masses m_{1} and m_{2} move around the sun in circular orbits of r_{1} and r_{2} radii respectively. If angular momentum of A is L and that of B is 3L, the ratio of time period (\\f{T_{A}}{T_{B}}) is:',
    ['(\\f{r_{2}}{r_{1}})^{3/2}', '(\\f{r_{1}}{r_{2}})^{3}', '\\f{1}{27}(\\f{m_{2}}{m_{1}})^{3}', '27(\\f{m_{1}}{m_{2}})^{3}'], 3,
    lambda: (lambda m1, m2: (lambda r1, r2: near([(r2 / r1) ** 1.5, (r1 / r2) ** 3, (m2 / m1) ** 3 / 27, 27 * (m1 / m2) ** 3], (r1 / r2) ** 1.5))(1.0, (3 * m1 / m2) ** 2))(2.0, 5.0),
    ['L = m√{GMr} → \\f{L_{A}}{L_{B}} = \\f{m_{1}√{r_{1}}}{m_{2}√{r_{2}}} = \\f{1}{3} → √{\\f{r_{1}}{r_{2}}} = \\f{m_{2}}{3m_{1}}.', 'T ∝ r^{3/2} → \\f{T_{A}}{T_{B}} = (\\f{m_{2}}{3m_{1}})^{3} = \\f{1}{27}(\\f{m_{2}}{m_{1}})^{3}.'], 'orbit', 3)
add(('2024', 'Apr', '2024-04-09', 2), 'orbit', 'A satellite of 10^{3} kg mass is revolving in circular orbit of radius 2R. If \\f{10^{4}R}{6} J energy is supplied to the satellite, it would revolve in a new circular orbit of radius : (use g = 10 m/s^{2}, R = radius of earth)',
    ['2.5 R', '3 R', '4R', '6R'], 4, lambda: pick([F(5, 2), 3, 4, 6], 1 / (F(1, 2) - 2 * F(1, 6))),
    ['E = −\\f{GMm}{2r} = −\\f{gR^{2}m}{2r}; gRm = 10^{4}R (taking R in the same units).', 'E_{1} = −\\f{10^{4}R}{4}; E_{2} = E_{1} + \\f{10^{4}R}{6} = −\\f{10^{4}R}{12}.', '−\\f{10^{4}R^{2}}{2r} = −\\f{10^{4}R}{12} → r = 6R.'], 'orbit', 3)
add(('2026', 'Apr', '2026-04-02', 1), 'orbit', 'A planet (P_{1}) is moving around the star of mass 2M in the orbit of radius R. Another planet (P_{2}) is moving around another star of mass 4M in a orbit of radius 2R. Ratio of time periods of revolution of P_{2} and P_{1} is ______.',
    ['\\f{1}{2}', '2', '4', '\\f{1}{4}'], 2, lambda: pick([F(1, 2), 2, 4, F(1, 4)], math.isqrt(int(F(8, 4) / F(1, 2)))), ['T^{2} ∝ \\f{r^{3}}{M}: P_{1}: \\f{R^{3}}{2M}; P_{2}: \\f{8R^{3}}{4M} = \\f{2R^{3}}{M}.', 'T_{2}^{2}/T_{1}^{2} = 4 → ratio 2.'], 'orbit', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'orbit', 'Initially a satellite of 100 kg is in a circular orbit of radius 1.5R_{E}. This satellite can be moved to a circular orbit of radius 3R_{E} by supplying α × 10^{6} J of energy. The value of α is ______. (Take Radius of Earth R_{E} = 6 × 10^{6} m and g = 10 m/s^{2})',
    ['150', '500', '100', '1000'], 4, lambda: pick([150, 500, 100, 1000], round(10 * 6e6 ** 2 * 100 / 2 * (1 / (1.5 * 6e6) - 1 / (3 * 6e6)) / 1e6)),
    ['ΔE = \\f{GMm}{2}(\\f{1}{r_{1}} − \\f{1}{r_{2}}) with GM = gR_{E}^{2}.', '= \\f{gR_{E}m}{2}(\\f{2}{3} − \\f{1}{3}) = \\f{10 × 6 × 10^{6} × 100}{6} = 10^{9} J = 1000 × 10^{6} J.'], 'orbit', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'orbit', 'If a satellite orbiting the Earth is 9 times closer to the Earth than the Moon, what is the time period of rotation of the satellite? Given rotational time period of Moon = 27 days and gravitational attraction between the satellite and the moon is neglected.',
    ['81 days', '27 days', '1 day', '3 days'], 3, lambda: pick([81, 27, 1, 3], round(27 * (1 / 9) ** 1.5)), ['Kepler: T ∝ r^{3/2}.', 'T = 27 × (\\f{1}{9})^{3/2} = \\f{27}{27} = 1 day.'], 'orbit', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'orbit', 'A satellite of mass \\f{M}{2} is revolving around earth in a circular orbit at a height of \\f{R}{3} from earth surface. The angular momentum of the satellite is M√{\\f{GMR}{x}}. The value of x is ______, where M and R are the mass and radius of earth, respectively.',
    None, 3, lambda: int(1 / (F(1, 4) * F(4, 3))), ['r = R + \\f{R}{3} = \\f{4R}{3}; L = m√{GMr} = \\f{M}{2}√{\\f{4GMR}{3}}.', '= M√{\\f{GMR}{3}} → x = 3.'], 'orbit', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'orbit', "A satellite is launched into a circular orbit of radius 'R' around the earth. A second satellite is launched into an orbit of radius 1.03 R. The time period of revolution of the second satellite is larger than the first one approximately by",
    ['3%', '4.5%', '2.5%', '9%'], 2, lambda: near([3, 4.5, 2.5, 9], 100 * (1.03 ** 1.5 - 1)), ['T ∝ r^{3/2} → \\f{ΔT}{T} ≈ \\f{3}{2} × 3% = 4.5%.'], 'orbit', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'orbit', 'A planet takes 200 days to complete one revolution around the Sun. If the distance of the planet from Sun is reduced to one fourth of the original distance, how many days will it take to complete one revolution?',
    ['25', '50', '100', '20'], 1, lambda: pick([25, 50, 100, 20], round(200 * 0.25 ** 1.5)), ['T ∝ r^{3/2}: (\\f{1}{4})^{3/2} = \\f{1}{8}.', '200/8 = 25 days.'], 'orbit', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'orbit', 'Two planets, A and B are orbiting a common star in circular orbits of radii R_{A} and R_{B}, respectively, with R_{B} = 2R_{A}. The planet B is 4√{2} times more massive than planet A. The ratio (\\f{L_{B}}{L_{A}}) of angular momentum (L_{B}) of planet B to that of planet A (L_{A}) is closest to integer ______.',
    None, 8, lambda: round(4 * math.sqrt(2) * math.sqrt(2)), ['L = m√{GMr} → \\f{L_{B}}{L_{A}} = 4√{2} × √{2} = 8.'], 'orbit', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'orbit', 'Statement I: A satellite is moving around earth in the orbit very close to the earth surface. The time period of revolution of satellite depends upon the density of earth. Statement II: The time period of revolution of the satellite is T = 2π√{\\f{R_{e}}{g}} (for satellite very close to the earth surface), where R_{e} radius of earth and g acceleration due to gravity.',
    ['Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true'], 3, lambda: 3,
    ['Near the surface: T = 2π√{\\f{R^{3}}{GM}} = 2π√{\\f{R}{g}} (II true).', 'With M = \\f{4}{3}πR^{3}ρ: T = √{\\f{3π}{Gρ}} — depends only on density (I true).'], 'orbit', 2)

if __name__ == '__main__': print(verify(P), 'real questions verified')
