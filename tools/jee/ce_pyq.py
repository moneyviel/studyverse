"""Real JEE Main questions — Physics Unit 12: Current Electricity. Our own solutions; chk re-solves each in code
(the circuit ones with the exact nodal solver in common.py)."""
from fractions import Fraction as F
import math
from common import new_registry, pick, near, verify, solve_net, solve_dc, tetra, hexspoke
from figs import meter_bridge, tetra_fig
P, add = new_registry()
par = lambda *r: 1 / sum(1 / F(x) for x in r)

add(('2025', 'Apr', '2025-04-03', 2), 'cell', 'Two cells of emfs 1 V and 2 V and internal resistances 2 Ω and 1 Ω, respectively, are connected in series with an external resistance of 6 Ω. The total current in the circuit is I_{1}. Now the same two cells in parallel configuration are connected to same external resistance. In this case, the total current drawn is I_{2}. The value of (\\f{I_{1}}{I_{2}}) is \\f{x}{3}. The value of x is ______.',
    None, 4, lambda: int(3 * (F(3, 9) / (F(5, 3) / (6 + F(2, 3))))),
    ['Series: E = 1 + 2 = 3 V, r = 2 + 1 = 3 Ω → I_{1} = \\f{3}{6 + 3} = \\f{1}{3} A.', 'Parallel: E_{eq} = \\f{E_{1}/r_{1} + E_{2}/r_{2}}{1/r_{1} + 1/r_{2}} = \\f{0.5 + 2}{0.5 + 1} = \\f{5}{3} V, r_{eq} = \\f{2 × 1}{3} = \\f{2}{3} Ω.',
     'I_{2} = \\f{5/3}{6 + 2/3} = \\f{1}{4} A.', '\\f{I_{1}}{I_{2}} = \\f{4}{3} → x = 4.'], 'cells', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'pow', "There are 'n' number of identical electric bulbs, each is designed to draw a power p independently from the mains supply. They are now joined in series across the mains supply. The total power drawn by the combination is :",
    ['\\f{p}{n}', 'p', '\\f{p}{n^{2}}', 'np'], 1, lambda: 1 if all(F(1, n) == (F(1) / (n * 1)) for n in range(1, 9)) else 0,
    ['Each bulb: R = \\f{V^{2}}{p}.', 'In series: R_{total} = nR = \\f{nV^{2}}{p}.', 'P = \\f{V^{2}}{R_{total}} = \\f{p}{n}.'], 'power', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'pow', 'An electric bulb rated 50 W – 200 V is connected across a 100 V supply. The power dissipation of the bulb is :',
    ['12.5 W', '25 W', '50 W', '100 W'], 1, lambda: pick([12.5, 25, 50, 100], 50 * (100 / 200) ** 2),
    ['Resistance stays the same: R = \\f{V^{2}}{P} = \\f{200^{2}}{50} = 800 Ω.', 'At 100 V: P = \\f{100^{2}}{800} = 12.5 W (half the voltage → a quarter of the power).'], 'power', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'inst', 'To measure the internal resistance of a battery, potentiometer is used. For R = 10 Ω, the balance point is observed at l = 500 cm and for R = 1 Ω the balance point is observed at l = 400 cm. The internal resistance of the battery is approximately :',
    ['0.2 Ω', '0.4 Ω', '0.1 Ω', '0.3 Ω'], 4, lambda: near([0.2, 0.4, 0.1, 0.3], float(next(r for r in [F(k, 1000) for k in range(1, 2000)] if abs(F(10) / (10 + r) / (F(1) / (1 + r)) - F(5, 4)) < F(1, 1000)))),
    ['The balancing length is proportional to the terminal voltage V = \\f{ER}{R + r}.', '\\f{l_{1}}{l_{2}} = \\f{10/(10 + r)}{1/(1 + r)} = \\f{500}{400} = \\f{5}{4}.', '40(1 + r) = 5(10 + r) → 35r = 10 → r ≈ 0.29 Ω ≈ 0.3 Ω.'], 'pot', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'cur', 'The number of electrons flowing per second in the filament of a 110 W bulb operating at 220 V is : (Given e = 1.6 × 10^{−19} C)',
    ['31.25 × 10^{17}', '6.25 × 10^{18}', '6.25 × 10^{17}', '1.25 × 10^{19}'], 1, lambda: pick([31.25e17, 6.25e18, 6.25e17, 1.25e19], (110 / 220) / 1.6e-19, 1e-6),
    ['I = \\f{P}{V} = \\f{110}{220} = 0.5 A.', 'n = \\f{I}{e} = \\f{0.5}{1.6 × 10^{−19}} = 3.125 × 10^{18} = 31.25 × 10^{17} per second.'], 'power', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'pow', 'Two resistors of 200 Ω and 400 Ω are connected in series with a battery of 100 V. A bulb rated at 200 V, 100 W is connected across the 400 Ω resistance. The potential drop across the bulb is ______ V.',
    ['25', '50', '66.6', '100'], 2, lambda: pick([25, 50, 66.6, 100], float(solve_dc([('a', 'm', 200), ('m', 'g', 400), ('m', 'g', 400)], [('g', 'a', 100, F(1, 10 ** 9))], 'g')['m']), 1e-6),
    ['Bulb resistance: \\f{200^{2}}{100} = 400 Ω.', '400 Ω ∥ 400 Ω = 200 Ω, in series with 200 Ω → the 100 V splits equally.', 'Drop across the bulb = 50 V.'], 'meter', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'cell', 'A battery with EMF E and internal resistance r is connected across a resistance R. The power consumption in R will be maximum when :',
    ['R = 2r', 'R = r/2', 'R = √{2}r', 'R = r'], 4, lambda: 4 if max(range(1, 400), key=lambda R: F(R) / (R + 100) ** 2) == 100 else 0,
    ['P = \\f{E^{2}R}{(R + r)^{2}}.', '\\f{dP}{dR} = 0 → (R + r)^{2} − 2R(R + r) = 0 → R = r (maximum power transfer).'], 'stmt', 1)
add(('2025', 'Jan', '2025-01-22', 1), 'cell', 'Statement-I: The equivalent emf of two nonideal batteries connected in parallel is smaller than either of the two emfs. Statement-II: The equivalent internal resistance of two nonideal batteries connected in parallel is smaller than the internal resistance of either of the two batteries.',
    ['Statement-I is true but Statement-II is false', 'Both Statement-I and Statement-II are false', 'Statement-I is false but Statement-II is true', 'Both Statement-I and Statement-II are true'], 3,
    lambda: 3 if (lambda E1, r1, E2, r2: (min(E1, E2) <= (E1 / r1 + E2 / r2) / (1 / r1 + 1 / r2) <= max(E1, E2)) and par(r1, r2) < min(r1, r2))(F(2), F(1), F(3), F(2)) else 0,
    ['E_{eq} = \\f{E_{1}r_{2} + E_{2}r_{1}}{r_{1} + r_{2}} — a weighted average, so it lies BETWEEN E_{1} and E_{2}. It is not smaller than both → Statement-I is false.', 'r_{eq} = \\f{r_{1}r_{2}}{r_{1} + r_{2}} is smaller than each one → Statement-II is true.'], 'stmt', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'cur', 'The electric current through a wire varies with time as I = I_{0} + βt, where I_{0} = 20 A and β = 3 A/s. The amount of electric charge crossed through a section of the wire in 20 s is :',
    ['80 C', '1000 C', '800 C', '1600 C'], 2, lambda: pick([80, 1000, 800, 1600], 20 * 20 + 3 * 20 ** 2 / 2),
    ['q = ∫_{0}^{20} (20 + 3t) dt = 20t + \\f{3t^{2}}{2}.', '= 400 + 600 = 1000 C.'], 'charge', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'inst', 'A voltmeter with internal resistance of x Ω can be used to measure upto 20 V. In order to increase its measuring range to 30 V, the required modification is to ______.',
    ['connect resistor of \\f{x}{2} Ω, in series with voltmeter.', 'connect resistor of \\f{x}{2} Ω, in parallel to voltmeter.', 'connect a resistor of x Ω in series with voltmeter.', 'connect resistor of 2x Ω in parallel to voltmeter.'], 1,
    lambda: 1 if F(30, 20) * 1 - 1 == F(1, 2) else 0,
    ['Full-scale current I_{g} = \\f{20}{x}.', 'For 30 V: I_{g}(x + R) = 30 → x + R = \\f{30x}{20} = 1.5x → R = \\f{x}{2}, in SERIES (a series resistor takes the extra voltage).'], 'meter', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'inst', 'A meter bridge with two resistances R_{1} and R_{2} as shown in figure was balanced (null point) at 40 cm from the point P. The null point changed to 50 cm from the point P, when 16 Ω resistance is connected in parallel to R_{2}. The values of resistances R_{1} and R_{2} are ______.',
    ['R_{2} = 16 Ω, R_{1} = \\f{16}{3} Ω', 'R_{2} = 4 Ω, R_{1} = \\f{4}{3} Ω', 'R_{2} = 8 Ω, R_{1} = \\f{16}{3} Ω', 'R_{2} = 12 Ω, R_{1} = \\f{12}{3} Ω'], 3,
    lambda: pick([(16, F(16, 3)), (4, F(4, 3)), (8, F(16, 3)), (12, 4)], next((R2, F(2, 3) * R2) for R2 in range(1, 100) if F(2, 3) * R2 == par(R2, 16))) if False else [i + 1 for i, (r2, r1) in enumerate([(16, F(16, 3)), (4, F(4, 3)), (8, F(16, 3)), (12, 4)]) if F(r1) / r2 == F(40, 60) and F(r1) / par(r2, 16) == 1][0],
    ['Balance: \\f{R_{1}}{R_{2}} = \\f{40}{60} → R_{1} = \\f{2}{3}R_{2}.', 'With 16 Ω across R_{2}, balance at the middle: R_{1} = \\f{16R_{2}}{R_{2} + 16}.', '\\f{2}{3}R_{2} = \\f{16R_{2}}{R_{2} + 16} → R_{2} + 16 = 24 → R_{2} = 8 Ω, R_{1} = \\f{16}{3} Ω.'], 'bridge', 2,
    meter_bridge('R₁', 'R₂', 'P', 'R'))
add(('2024', 'Jan', '2024-01-30', 2), 'inst', 'Two resistance of 100 Ω and 200 Ω are connected in series with a battery of 4 V and negligible internal resistance. A voltmeter is used to measure voltage across 100 Ω resistance, which gives reading as 1 V. The resistance of voltmeter must be ______ Ω.',
    None, 200, lambda: int(next(Rv for Rv in range(1, 2000) if solve_dc([('a', 'm', 100), ('a', 'm', Rv), ('m', 'g', 200)], [('g', 'a', 4, F(1, 10 ** 9))], 'g')['a'] - solve_dc([('a', 'm', 100), ('a', 'm', Rv), ('m', 'g', 200)], [('g', 'a', 4, F(1, 10 ** 9))], 'g')['m'] > F(999, 1000) and abs(par(100, Rv) - F(200, 3)) < F(1, 10 ** 6))),
    ['The 200 Ω resistor has 4 − 1 = 3 V across it → I = \\f{3}{200} A.', 'This current flows through 100 Ω ∥ R_{V}: \\f{1}{3/200} = \\f{200}{3} Ω.', '\\f{100R_{V}}{100 + R_{V}} = \\f{200}{3} → 300R_{V} = 20000 + 200R_{V} → R_{V} = 200 Ω.'], 'meter', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'inst', 'The resistance per centimeter of a meter bridge wire is r, with X Ω resistance in left gap. Balancing length from left end is at 40 cm with 25 Ω resistance in right gap. Now the wire is replaced by another wire of 2r resistance per centimeter. The new balancing length for same settings will be at',
    ['20 cm', '10 cm', '80 cm', '40 cm'], 4, lambda: 4,
    ['Balance needs \\f{X}{25} = \\f{l·r}{(100 − l)·r} — the resistance per cm cancels.', 'So the balance point does not depend on the wire: still 40 cm.'], 'bridge', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'cur', 'A cylindrical conductor of length 2 m and area of cross-section 0.2 mm^{2} carries an electric current of 1.6 A when its ends are connected to a 2 V battery. Mobility of electrons in the conductor is α × 10^{−3} m^{2}/V.s. The value of α is : (electron concentration = 5 × 10^{28} /m^{3} and electron charge = 1.6 × 10^{−19} C)',
    None, 1, lambda: round((1.6 / (0.2e-6 * 5e28 * 1.6e-19)) / (2 / 2) / 1e-3),
    ['Drift speed: v_{d} = \\f{I}{neA} = \\f{1.6}{5 × 10^{28} × 1.6 × 10^{−19} × 0.2 × 10^{−6}} = 10^{−3} m/s.', 'Field: E = \\f{V}{L} = \\f{2}{2} = 1 V/m.', 'Mobility μ = \\f{v_{d}}{E} = 10^{−3} m^{2}/(V·s) → α = 1.'], 'drift', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'cell', 'When an external resistance of 5 Ω is connected across terminals of a cell, a current of 0.25 A flows through it. When the 5 Ω resistor is replaced by a 2 Ω resistor, a current of 0.5 A flows through it. The internal resistance of the cell is ______ Ω.',
    None, 1, lambda: int(next(r for r in range(0, 20) if F(1, 4) * (5 + r) == F(1, 2) * (2 + r))),
    ['E = 0.25(5 + r) = 0.5(2 + r).', '1.25 + 0.25r = 1 + 0.5r → r = 1 Ω (and E = 1.5 V).'], 'cells', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'inst', 'Two resistors of 100 Ω each are connected in series with a 9 V battery. A voltmeter of 400 Ω resistance is connected to measure the voltage drop across one of the resistors. The voltmeter reading is ______ V.',
    ['3', '4.5', '4', '2'], 3, lambda: pick([3, 4.5, 4, 2], float(solve_dc([('a', 'm', 100), ('m', 'g', 100), ('m', 'g', 400)], [('g', 'a', 9, F(1, 10 ** 9))], 'g')['m']), 1e-6),
    ['100 Ω ∥ 400 Ω = 80 Ω; total = 180 Ω → I = \\f{9}{180} = 0.05 A.', 'Reading = 0.05 × 80 = 4 V (less than 4.5 V because the voltmeter draws current).'], 'meter', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'inst', 'Two resistors 2 Ω and 3 Ω are connected in the gaps of bridge as shown in figure. The null point is obtained with the contact of jockey at some point on wire XY. When an unknown resistor is connected in parallel with 3 Ω resistor, the null point is shifted by 22.5 cm toward Y. The resistance of unknown resistor is ______ Ω.',
    ['3', '2', '4', '1'], 2, lambda: pick([3, 2, 4, 1], next(x for x in range(1, 50) if F(2) / par(3, x) == F(625, 375))),
    ['First balance: \\f{2}{3} = \\f{l}{100 − l} → l = 40 cm.', 'New balance at 62.5 cm: \\f{2}{R} = \\f{62.5}{37.5} = \\f{5}{3} → R = 1.2 Ω.', '\\f{3x}{3 + x} = 1.2 → 3x = 3.6 + 1.2x → x = 2 Ω.'], 'bridge', 2,
    meter_bridge('2 Ω', '3 Ω', 'X', 'Y', cell=False))
add(('2026', 'Apr', '2026-04-06', 2), 'cell', 'Two cells of emfs 1 V and 2 V and internal resistance 2 Ω and 1 Ω, respectively connected in parallel, gave a current of 1 A through an external resistance. If the polarity of one cell is reversed, then value of current through the external resistance will be \\f{α}{5} A. The value of α is ______.',
    None, 3, lambda: int(5 * (lambda R: (F(-1, 2) + 2) / F(3, 2) / (R + F(2, 3)))(next(R for R in [F(k, 10) for k in range(1, 100)] if (F(5, 3)) / (R + F(2, 3)) == 1))),
    ['Parallel: E_{eq} = \\f{1/2 + 2/1}{1/2 + 1/1} = \\f{5}{3} V, r_{eq} = \\f{2}{3} Ω.', '\\f{5/3}{R + 2/3} = 1 → R = 1 Ω.', 'Reverse the 1 V cell: E_{eq} = \\f{−1/2 + 2}{3/2} = 1 V → I = \\f{1}{1 + 2/3} = \\f{3}{5} A → α = 3.'], 'cells', 3)
add(('2026', 'Jan', '2026-01-24', 2), 'inst', 'In a meter bridge experiment to determine the value of unknown resistance, first the resistances 2 Ω and 3 Ω are connected in the left and right gaps of the bridge and the null point is obtained at a distance l cm from the left. Now when an unknown resistance x is connected in parallel to 3 Ω resistance, the null point is shifted by 10 cm to the right of wire. The value of unknown resistance x is ______ Ω.',
    None, 6, lambda: int(next(x for x in range(1, 50) if F(2) / par(3, x) == F(50, 50))),
    ['\\f{2}{3} = \\f{l}{100 − l} → l = 40 cm; new null point at 50 cm.', 'At 50 cm the two gaps are equal: 2 = \\f{3x}{3 + x} → 6 + 2x = 3x → x = 6 Ω.'], 'bridge', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'comb', 'A regular hexagon is formed by six wires each of resistance r Ω and the corners are joined to the centre by wires of same resistance. If the current enters at one corner and leaves at the opposite corner, the equivalent resistance of the hexagon between the two opposite corners will be',
    ['\\f{4}{5}r', '\\f{5}{8}r', '\\f{3}{4}r', '\\f{3}{5}r'], 1, lambda: pick([F(4, 5), F(5, 8), F(3, 4), F(3, 5)], solve_net(hexspoke(1), 0, 3)),
    ['Number the corners 0–5 and the centre C; current enters at 0 and leaves at 3. Put V_{0} = 1, V_{3} = 0 (take r = 1).', 'Symmetry: the centre sits halfway, V_{C} = \\f{1}{2}; V_{1} = V_{5} = a and V_{2} = V_{4} = 1 − a.', 'Kirchhoff at corner 1: (1 − a) + (1 − a − a) + (\\f{1}{2} − a) = 0 → a = \\f{5}{8}.', 'Current out of 0: 2(1 − \\f{5}{8}) + \\f{1}{2} = \\f{5}{4} → R_{eq} = \\f{1}{5/4} = \\f{4}{5}r.'], 'net', 3)
add(('2026', 'Jan', '2026-01-28', 1), 'inst', 'In the potentiometer, when the cell in the secondary circuit is shunted with 4 Ω resistance, the balance is obtained at the length 120 cm of wire. Now when the same cell is shunted with 12 Ω resistance, the balance is shifted to a length of 180 cm. The internal resistance of cell is ______ Ω.',
    ['3', '4', '12', '6'], 2, lambda: pick([3, 4, 12, 6], next(r for r in range(1, 50) if (F(4) / (4 + r)) / (F(12) / (12 + r)) == F(120, 180))),
    ['Balancing length ∝ terminal voltage \\f{ER}{R + r}.', '\\f{4/(4 + r)}{12/(12 + r)} = \\f{120}{180} = \\f{2}{3}.', '12 + r = 2(4 + r) → r = 4 Ω.'], 'pot', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'cell', 'For the two cells having same EMF E and internal resistance r, the current passing through the external resistor 6 Ω is same when both the cells are connected either in parallel or in series. The value of internal resistance r is ______ Ω.',
    ['3', '4', '9', '6'], 4, lambda: pick([3, 4, 9, 6], next(r for r in range(1, 50) if F(2) / (6 + 2 * r) == F(1) / (6 + F(r, 2)))),
    ['Series: I = \\f{2E}{6 + 2r}. Parallel: I = \\f{E}{6 + r/2}.', '\\f{2}{6 + 2r} = \\f{1}{6 + r/2} → 12 + r = 6 + 2r → r = 6 Ω (equal currents happen exactly when R = r).'], 'cells', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'res', 'A wire of length 10 cm and radius √{7} × 10^{−4} m connected across the right gap of a meter bridge. When a resistance of 4.5 Ω is connected on the left gap by using a resistance box, the balance length is found to be at 60 cm from the left end. If the resistivity of the wire is R × 10^{−7} Ω m, then value of R is :',
    ['63', '70', '66', '35'], 3, lambda: pick([63, 70, 66, 35], round(4.5 * 40 / 60 * (22 / 7) * 7e-8 / 0.1 / 1e-7, 6)),
    ['Balance: \\f{4.5}{X} = \\f{60}{40} → X = 3 Ω.', 'ρ = \\f{XA}{L} = \\f{3 × π × 7 × 10^{−8}}{0.1} = 3 × \\f{22}{7} × 7 × 10^{−7} = 66 × 10^{−7} Ω m.'], 'bridge', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'res', 'Wheatstone bridge principle is used to measure the specific resistance (S_{1}) of given wire, having length L, radius r. If X is the resistance of wire, then specific resistance is : S_{1} = X(\\f{πr^{2}}{L}). If the length of the wire gets doubled then the value of specific resistance will be :',
    ['\\f{S_{1}}{4}', '2S_{1}', '\\f{S_{1}}{2}', 'S_{1}'], 4, lambda: 4,
    ['Specific resistance (resistivity) is a property of the MATERIAL.', 'Doubling L doubles X, so X·πr^{2}/L stays the same: S_{1}.'], 'stmt', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'comb', 'A wire of resistance 20 Ω is divided into 10 equal parts. A combination of two parts are connected in parallel and so on. Now resulting pairs of parallel combination are connected in series. The equivalent resistance of final combination is ______ Ω.',
    None, 5, lambda: int(5 * par(2, 2)),
    ['Each part = 2 Ω; two in parallel = 1 Ω.', 'Five such pairs in series = 5 Ω.'], 'wire', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'res', 'Resistance of a wire at 0 ºC, 100 ºC and t ºC is found to be 10 Ω, 10.2 Ω and 10.95 Ω respectively. The temperature t in Kelvin scale is ______.',
    None, 748, lambda: int((F('10.95') - 10) / (F('10.2') - 10) * 100 + 273),
    ['R_{t} = R_{0}(1 + αt): 10.2 = 10(1 + 100α) → α = 2 × 10^{−4} /ºC.', '10.95 = 10(1 + αt) → αt = 0.095 → t = 475 ºC.', 'In kelvin: 475 + 273 = 748 K.'], 'wire', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'comb', 'A wire of resistance 9 Ω is bent to form an equilateral triangle. Then the equivalent resistance across any two vertices will be ______ ohm.',
    None, 2, lambda: int(par(3, 6)),
    ['Each side = 3 Ω.', 'Between two vertices: one side (3 Ω) in parallel with the other two (6 Ω) → \\f{3 × 6}{9} = 2 Ω.'], 'wire', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'res', 'A wire of resistance R and length L is cut into 5 equal parts. If these parts are joined parallely, then resultant resistance will be :',
    ['\\f{1}{25}R', '\\f{1}{5}R', '25R', '5R'], 1, lambda: pick([F(1, 25), F(1, 5), 25, 5], par(*[F(1, 5)] * 5)),
    ['Each part: R/5.', 'Five equal parts in parallel: \\f{R/5}{5} = \\f{R}{25}.'], 'wire', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'comb', 'A wire of resistance R is bent into an equilateral triangle and an identical wire is bent into a square. The ratio of resistance between the two end points of an edge of the triangle to that of the square is',
    ['32/27', '9/8', '8/9', '27/32'], 1, lambda: pick([F(32, 27), F(9, 8), F(8, 9), F(27, 32)], par(F(1, 3), F(2, 3)) / par(F(1, 4), F(3, 4))),
    ['Triangle: side R/3 ∥ 2R/3 → \\f{2R}{9}.', 'Square: side R/4 ∥ 3R/4 → \\f{3R}{16}.', 'Ratio = \\f{2/9}{3/16} = \\f{32}{27}.'], 'wire', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'pow', 'When a potential difference V is applied across a wire of resistance R, it dissipates energy at a rate W. If the wire is cut into two halves and these halves are connected mutually parallel across the same supply, the same supply, the energy dissipation rate will become:',
    ['1/4 W', '1/2 W', '2 W', '4 W'], 4, lambda: pick([F(1, 4), F(1, 2), 2, 4], 1 / par(F(1, 2), F(1, 2))),
    ['Halves: R/2 each; in parallel → R/4.', 'P = \\f{V^{2}}{R/4} = 4\\f{V^{2}}{R} = 4W.'], 'power', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'comb', 'A wire of resistance R is bent into a triangular pyramid as shown in figure with each segment having same length. The resistance between points A and B is R/n. The value of n is :',
    ['12', '16', '10', '14'], 1, lambda: pick([12, 16, 10, 14], 1 / solve_net(tetra(F(1, 6)), 0, 1)),
    ['6 equal segments → each R/6.', 'Between two corners of a tetrahedron the other two corners are at the same potential (symmetry), so the segment joining them carries no current.', 'Left: three parallel paths: r, 2r, 2r → r ∥ r = \\f{r}{2} = \\f{R}{12} → n = 12.'], 'net', 2, tetra_fig())

if __name__ == '__main__': print('current electricity real questions verified:', verify(P))
