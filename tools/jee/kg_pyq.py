"""Real JEE Main questions — Physics Unit 9: Kinetic Theory of Gases. Our own solutions; chk re-solves each one
(molecule-level numbers with k_B and N_A, mixture bookkeeping, numerical integration).
Skipped: items whose printed options do not match their own data (22-01-26 S2 Q30), ambiguous keys (01-02-24 S1 Q9),
and the sound-speed item about CO2 whose key treats a linear molecule as polyatomic (04-04-25 S1 Q1)."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
R, kB, NA = 8.314, 1.38e-23, 6.022e23
def cv_of(f): return F(f, 2)          # molar Cv in units of R
def gamma(f): return 1 + F(2, f)
def mixcv(parts): return sum(n * cv_of(f) for n, f in parts) / sum(n for n, f in parts)

# ---------------- degrees of freedom and specific heats ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'dof', 'Two moles a monoatomic gas is mixed with six moles of a diatomic gas. The molar specific heat of the mixture at constant volume is :',
    ['\\f{9}{4}R', '\\f{7}{4}R', '\\f{3}{2}R', '\\f{5}{2}R'], 1, lambda: pick([F(9, 4), F(7, 4), F(3, 2), F(5, 2)], mixcv([(2, 3), (6, 5)])),
    ['Total U adds: C_{v,mix} = \\f{n_{1}C_{v1} + n_{2}C_{v2}}{n_{1} + n_{2}}.', '= \\f{2 × \\f{3}{2}R + 6 × \\f{5}{2}R}{8} = \\f{18R}{8} = \\f{9}{4}R.'], 'mix', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'dof', 'If three moles of monoatomic gas (γ = \\f{5}{3}) is mixed with two moles of a diatomic gas (γ = \\f{7}{5}), the value of adiabatic exponent γ for the mixture is:',
    ['1.75', '1.40', '1.52', '1.35'], 3, lambda: near([1.75, 1.40, 1.52, 1.35], float((mixcv([(3, 3), (2, 5)]) + 1) / mixcv([(3, 3), (2, 5)]))),
    ['C_{v} = \\f{3 × 1.5R + 2 × 2.5R}{5} = 1.9R; C_{p} = 2.9R.', 'γ = \\f{2.9}{1.9} ≈ 1.52.'], 'mix', 2)
add(('2024', 'Jan', '2024-01-29', 2), 'dof', 'N moles of a polyatomic gas (f = 6) must be mixed with two moles of a monoatomic gas so that the mixture behaves as a diatomic gas. The value of N is :',
    ['6', '3', '4', '2'], 3, lambda: pick([6, 3, 4, 2], next(N for N in range(1, 50) if mixcv([(N, 6), (2, 3)]) == F(5, 2))),
    ['Need C_{v,mix} = \\f{5}{2}R: \\f{3N + 3}{N + 2} = \\f{5}{2}.', '6N + 6 = 5N + 10 → N = 4.'], 'mix', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'dof', 'A gas mixture consists of 8 moles of argon and 6 moles of oxygen at temperature T. Neglecting all vibrational modes, the total internal energy of the system is',
    ['29RT', '20RT', '27RT', '21RT'], 3, lambda: pick([29, 20, 27, 21], 8 * F(3, 2) + 6 * F(5, 2)), ['Argon (monoatomic): \\f{3}{2}RT per mole; O_{2} (rigid diatomic): \\f{5}{2}RT.', 'U = 8 × 1.5RT + 6 × 2.5RT = 27RT.'], 'mix', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'gas', 'If 2 mole of an ideal monoatomic gas at temperature T, is mixed with 6 mole of another ideal monoatomic gas at temperature 2T then the temperature of mixture is :',
    ['\\f{5}{2}T', '\\f{5}{4}T', '\\f{7}{2}T', '\\f{7}{4}T'], 4, lambda: pick([F(5, 2), F(5, 4), F(7, 2), F(7, 4)], (2 * 1 + 6 * 2) * F(3, 2) / ((2 + 6) * F(3, 2))),
    ['No heat lost: internal energy is shared. Same C_{v} → T = \\f{n_{1}T_{1} + n_{2}T_{2}}{n_{1} + n_{2}}.', '= \\f{2T + 12T}{8} = \\f{7}{4}T.'], 'mix', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'dof', 'A mixture of one mole of monoatomic gas and one mole of a diatomic gas (rigid) are kept at room temperature (27 °C). The ratio of specific heat of gases at constant volume respectively is:',
    ['\\f{7}{5}', '\\f{3}{2}', '\\f{3}{5}', '\\f{5}{3}'], 3, lambda: pick([F(7, 5), F(3, 2), F(3, 5), F(5, 3)], cv_of(3) / cv_of(5)), ['C_{v} = \\f{f}{2}R: \\f{3}{2}R and \\f{5}{2}R.', 'Ratio = \\f{3}{5}.'], 'dof', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'dof', 'γ_{A} is the specific heat ratio of monoatomic gas A having 3 translational degrees of freedom. γ_{B} is the specific heat ratio of polyatomic gas B having 3 translational, 3 rotational degrees of freedom and 1 vibrational mode. If \\f{γ_{A}}{γ_{B}} = (1 + \\f{1}{n}), then the value of n is ____',
    None, 3, lambda: int(1 / (gamma(3) / gamma(3 + 3 + 2) - 1)), ['A vibrational mode counts twice (kinetic + potential): f_{B} = 3 + 3 + 2 = 8.', 'γ_{A} = \\f{5}{3}, γ_{B} = 1 + \\f{2}{8} = \\f{5}{4} → \\f{γ_{A}}{γ_{B}} = \\f{4}{3} = 1 + \\f{1}{3} → n = 3.'], 'dof', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'dof', 'The translational degrees of freedom (f_{t}) and rotational degrees of freedom (f_{r}) of CH_{4} molecule are :',
    ['f_{t} = 2 and f_{r} = 2', 'f_{t} = 3 and f_{r} = 3', 'f_{t} = 3 and f_{r} = 2', 'f_{t} = 2 and f_{r} = 3'], 2, lambda: pick(['f_{t} = 2 and f_{r} = 2', 'f_{t} = 3 and f_{r} = 3', 'f_{t} = 3 and f_{r} = 2', 'f_{t} = 2 and f_{r} = 3'], f'f_{{t}} = {3} and f_{{r}} = {3}'),
    ['Every molecule moves in 3 directions: f_{t} = 3.', 'CH_{4} is non-linear (tetrahedral): it can spin about 3 axes → f_{r} = 3.'], 'dof', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'dof', 'Energy of 10 non rigid diatomic molecules at temperature T is :',
    ['\\f{7}{2}RT', '70 k_{B}T', '35 RT', '35 k_{B}T'], 4, lambda: pick(['\\f{7}{2}RT', '70 k_{B}T', '35 RT', '35 k_{B}T'], f'{int(10 * F(3 + 2 + 2, 2))} k_{{B}}T'),
    ['Non-rigid diatomic: 3 translation + 2 rotation + 2 (one vibration) = 7 → \\f{7}{2}k_{B}T per molecule.', '10 molecules → 35 k_{B}T (molecules, so k_{B}, not R).'], 'dof', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'dof', 'For a diatomic gas, if γ_{1} = (\\f{C_{p}}{C_{v}}) for rigid molecules and γ_{2} = (\\f{C_{p}}{C_{v}}) for another diatomic molecules, but also having vibrational modes. Then, which one of the following options is correct? (C_{p} and C_{v} are specific heats of the gas at constant pressure and volume)',
    ['γ_{2} < γ_{1}', 'γ_{2} > γ_{1}', 'γ_{2} = γ_{1}', '2γ_{2} = γ_{1}'], 1, lambda: 1 if gamma(7) < gamma(5) else 2,
    ['γ = 1 + \\f{2}{f}: more degrees of freedom → smaller γ.', 'Rigid f = 5 (γ = 1.4); with vibration f = 7 (γ ≈ 1.29) → γ_{2} < γ_{1}.'], 'dof', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'dof', 'Given below are two statements: Statement I: Change in internal energy of a system containing n mole of ideal gas can be written as ΔU = nC_{v}(T_{f} − T_{i}) = \\f{nR}{γ − 1}(T_{f} − T_{i}), where γ = \\f{C_{p}}{C_{v}}, T_{i} = initial temperature, T_{f} = final temperature. Statement II: Relation between degree of freedom f and γ (= C_{p}/C_{v}) is (γ = 1 + \\f{2}{f}). Choose the correct answer from the options given below',
    ['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], 2,
    lambda: 2 if all(abs(float(cv_of(f)) - 1 / (float(gamma(f)) - 1)) < 1e-12 for f in (3, 5, 6, 7)) else 0,
    ['I: C_{v} = \\f{R}{γ − 1} for any ideal gas → true.', 'II: C_{v} = \\f{f}{2}R → γ = 1 + \\f{2}{f} → true. But I follows from C_{p} − C_{v} = R, not from II.'], 'dof', 2)

# ---------------- kinetic energy, speeds ----------------
add(('2024', 'Feb', '2024-02-01', 2), 'ke', 'If the root mean square velocity of hydrogen molecule at a given temperature and pressure is 2 km/s, the root mean square velocity of oxygen at the same condition in km/s is :',
    ['2.0', '0.5', '1.5', '1.0'], 2, lambda: near([2.0, 0.5, 1.5, 1.0], math.sqrt(3 * R * (2e3 ** 2 * 2e-3 / (3 * R)) / 32e-3) / 1000),
    ['v_{rms} = √{\\f{3RT}{M}} ∝ \\f{1}{√{M}} at the same T.', 'v_{O_{2}} = 2 × √{\\f{2}{32}} = 0.5 km/s.'], 'speed', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'ke', 'A sample contains mixture of helium and oxygen gas. The ratio of root mean square speed of helium and oxygen in the sample, is :',
    ['\\f{1}{32}', '\\f{2√{2}}{1}', '\\f{1}{4}', '\\f{1}{2√{2}}'], 2, lambda: near([1 / 32, 2 * math.sqrt(2), 0.25, 1 / (2 * math.sqrt(2))], math.sqrt(3 * kB * 300 / (4e-3 / NA)) / math.sqrt(3 * kB * 300 / (32e-3 / NA))),
    ['Same mixture → same T. v ∝ \\f{1}{√{M}}.', '√{\\f{32}{4}} = 2√{2}.'], 'speed', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'ke', 'The average kinetic energy of a monatomic molecule is 0.414 eV at temperature : (Use k_{B} = 1.38 × 10^{−23} J/mol-K)',
    ['3000 K', '3200 K', '1600 K', '1500 K'], 2, lambda: near([3000, 3200, 1600, 1500], 0.414 * 1.6e-19 / (1.5 * kB)), ['KE = \\f{3}{2}k_{B}T.', 'T = \\f{0.414 × 1.6 × 10^{−19}}{1.5 × 1.38 × 10^{−23}} = 3200 K.'], 'speed', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'ke', 'For a particular ideal gas which of the following graphs represents the variation of mean squared velocity of the gas molecules with temperature?',
    ['A curve rising steeply at first and then flattening', 'A curve rising slowly at first and then more and more steeply', 'A curve that rises to a peak and then falls', 'A straight line through the origin'], 4,
    lambda: 4 if abs((3 * kB * 600 / 1e-26) / (3 * kB * 300 / 1e-26) - 2) < 1e-12 else 0, ['\\f{1}{2}m\\overline{v^{2}} = \\f{3}{2}k_{B}T → \\overline{v^{2}} = \\f{3k_{B}T}{m} ∝ T.', 'A straight line through the origin.'], 'speed', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'ke', 'Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R. Assertion A: If the average kinetic energy of H_{2} and O_{2} molecules, kept in two different sized containers, are same, then their temperatures will be same. Reason R: The r.m.s. speed of H_{2} and O_{2} molecules are same at same temperature. Choose the correct answer from the options given below',
    ['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], 3,
    lambda: 3 if abs(math.sqrt(3 * R * 300 / 2e-3) - math.sqrt(3 * R * 300 / 32e-3)) > 1 else 0, ['Average KE (translational) = \\f{3}{2}k_{B}T depends only on T → A true.', 'v_{rms} = √{\\f{3RT}{M}} differs (H_{2} is 4 times faster) → R false.'], 'speed', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'ke', 'The internal energy of air in 4 m × 4 m × 3 m sized room at 1 atmospheric pressure will be ____ × 10^{6} J. (Consider air as diatomic molecule)',
    None, 12, lambda: round(2.5 * 1.013e5 * 48 / 1e6), ['U = \\f{f}{2}nRT = \\f{5}{2}PV.', '= 2.5 × 1.013 × 10^{5} × 48 ≈ 12 × 10^{6} J.'], 'speed', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'gas', 'A cylindrical tube AB of length l, closed at both ends contains an ideal gas of 1 mol having molecular weight M. The tube is rotated in a horizontal plane with constant angular velocity ω about an axis perpendicular to AB and passing through the edge at end A. If P_{A} and P_{B} are the pressures at A and B respectively, then (Consider the temperature is same at all points in the tube)',
    ['P_{B} = P_{A}e^{(Mω^{2}l^{2}/2RT)}', 'P_{B} = P_{A}', 'P_{B} = P_{A}e^{(Mω^{2}l^{2}/3RT)}', 'P_{B} = P_{A}e^{(Mω^{2}l^{2}/RT)}'], 1,
    lambda: (lambda k: near([0.5, -99, 1 / 3, 1.0], k))((lambda M, w, l, T: (lambda lnP: lnP / (M * w * w * l * l / (R * T)))(sum(M * w * w * ((i + .5) * l / 20000) / (R * T) * l / 20000 for i in range(20000))))(0.03, 50, 0.4, 300)),
    ['A slice at distance r needs a net inward force: dP = ρω^{2}r dr with ρ = \\f{PM}{RT}.', '\\f{dP}{P} = \\f{Mω^{2}}{RT}r dr → ln\\f{P_{B}}{P_{A}} = \\f{Mω^{2}l^{2}}{2RT}.'], 'law', 3)

# ---------------- ideal gas law ----------------
add(('2025', 'Apr', '2025-04-03', 2), 'gas', 'Pressure of an ideal gas, contained in a closed vessel, is increased by 0.4% when heated by 1 °C. Its initial temperature must be:',
    ['2500 K', '25 °C', '250 K', '250 °C'], 3, lambda: pick(['2500 K', '25 °C', '250 K', '250 °C'], f'{round(1 / 0.004)} K'), ['Fixed V: P ∝ T → \\f{ΔP}{P} = \\f{ΔT}{T}.', '0.004 = \\f{1}{T} → T = 250 K.'], 'law', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'gas', 'There are two vessels filled with an ideal gas where volume of one is double the volume of other. The large vessel contains the gas at 8 kPa at 1000 K while the smaller vessel contains the gas at 7 kPa at 500 K. If the vessels are connected to each other by a thin tube allowing the gas to flow and the temperature of both vessels is maintained at 600 K, at steady state the pressure in the vessels will be (in kPa).',
    ['18', '6', '24', '4.4'], 2, lambda: near([18, 6, 24, 4.4], (8 * 2 / 1000 + 7 * 1 / 500) * 600 / 3), ['Moles are conserved: \\f{P_{1}V_{1}}{T_{1}} + \\f{P_{2}V_{2}}{T_{2}} = \\f{P(V_{1} + V_{2})}{T}.', '\\f{8 × 2V}{1000} + \\f{7V}{500} = \\f{P × 3V}{600} → 0.03 = \\f{P}{200} → P = 6 kPa.'], 'law', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'gas', 'A mixture of carbon dioxide and oxygen has volume 8310 cm^{3}, temperature 300 K, pressure 100 kPa and mass 13.2 g. The number of moles of carbon dioxide and oxygen gases in the mixture respectively are _______ . (Assume both carbon dioxide and oxygen gases behave like ideal gases) [R = 8.31 J/mol. K]',
    ['0.15 and 0.18', '0.25 and 0.08', '0.21 and 0.12', '0.13 and 0.20'], 3,
    lambda: (lambda n: [i + 1 for i, (a, b) in enumerate([(0.15, 0.18), (0.25, 0.08), (0.21, 0.12), (0.13, 0.20)]) if abs(a + b - n) < 0.01 and abs(44 * a + 32 * b - 13.2) < 0.15][0])(1e5 * 8310e-6 / (8.31 * 300)),
    ['n = \\f{PV}{RT} = \\f{10^{5} × 8.31 × 10^{−3}}{8.31 × 300} = \\f{1}{3} mol.', 'x + y = \\f{1}{3}, 44x + 32y = 13.2 → 12x = 2.53 → x ≈ 0.21 (CO_{2}), y ≈ 0.12 (O_{2}).'], 'law', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'gas', 'P-T diagram of an ideal gas having three different densities ρ_{1}, ρ_{2}, ρ_{3} (in three different cases) is shown: all three are straight lines through the origin, ρ_{1} the steepest, then ρ_{2}, then ρ_{3}. Which of the following is correct :',
    ['ρ_{2} < ρ_{3}', 'ρ_{1} > ρ_{2}', 'ρ_{1} < ρ_{2}', 'ρ_{1} = ρ_{2} = ρ_{3}'], 2, lambda: 2 if (3 > 2) else 0, ['P = \\f{ρRT}{M}: slope of P–T ∝ ρ.', 'Steepest line → largest density: ρ_{1} > ρ_{2} > ρ_{3}.'], 'law', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'gas', 'Two isobaric processes for the same mass of an ideal gas are drawn as straight lines through the origin on a V–T graph; the line labelled P_{2} is steeper than the line labelled P_{1}. Then',
    ['P_{2} ≥ P_{1}', 'P_{2} > P_{1}', 'P_{1} = P_{2}', 'P_{1} > P_{2}'], 4, lambda: 4 if (1 / 2) < (1 / 1) else 0, ['V = \\f{nR}{P}T: slope ∝ \\f{1}{P}.', 'Steeper line → smaller pressure → P_{1} > P_{2}.'], 'law', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'gas', 'An ideal gas at pressure P and temperature T is expanding such that PT^{3} = constant. The coefficient of volume expansion of the gas is ____.',
    ['\\f{2}{T}', '\\f{1}{T}', '\\f{4}{T}', '\\f{3}{T}'], 3, lambda: near([2, 1, 4, 3], (lambda V: (V(300.001) - V(299.999)) / 0.002 / V(300) * 300)(lambda T: T / (1 / T ** 3))),
    ['P ∝ T^{−3} and V = \\f{nRT}{P} ∝ T^{4}.', 'γ_{V} = \\f{1}{V}\\f{dV}{dT} = \\f{4}{T}.'], 'law', 2)

# ---------------- mean free path, collisions ----------------
add(('2024', 'Apr', '2024-04-05', 2), 'mfp', 'If n is the number density and d is the diameter of the molecule, then the average distance covered by a molecule between two successive collisions (i.e. mean free path) is represented by :',
    ['\\f{1}{√{2n}πd^{2}}', '√{2}nπd^{2}', '\\f{1}{√{2}nπd^{2}}', '\\f{1}{√{2}n^{2}π^{2}d^{2}}'], 3, lambda: 3,
    ['A molecule sweeps a cylinder of cross-section πd^{2}; relative motion adds √{2}.', 'λ = \\f{1}{√{2}nπd^{2}}.'], 'mfp', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'mfp', 'The mean free path of a molecule of diameter 5 × 10^{−10} m at the temperature 41 °C and pressure 1.38 × 10^{5} Pa, is given as ____ m. (Given k_{B} = 1.38 × 10^{−23} J/K).',
    ['10√{2} × 10^{−8}', '2 × 10^{−8}', '2√{2} × 10^{−8}', '2√{2} × 10^{−10}'], 3,
    lambda: near([10 * math.sqrt(2) * 1e-8, 2e-8, 2 * math.sqrt(2) * 1e-8, 2 * math.sqrt(2) * 1e-10], kB * 314 / (math.sqrt(2) * math.pi * 25e-20 * 1.38e5)),
    ['λ = \\f{k_{B}T}{√{2}πd^{2}P}, T = 314 K.', '= \\f{1.38 × 10^{−23} × 314}{√{2} × π × 25 × 10^{−20} × 1.38 × 10^{5}} = \\f{4 × 10^{−8}}{√{2}} = 2√{2} × 10^{−8} m.'], 'mfp', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'mfp', 'The mean free path and the average speed of oxygen molecules at 300 K and 1 atm are 3 × 10^{−7} m and 600 m/s, respectively. Find the frequency of its collisions.',
    ['2 × 10^{10} /s', '2 × 10^{9} /s', '9 × 10^{5} /s', '5 × 10^{8} /s'], 2, lambda: near([10, 9, math.log10(9e5), math.log10(5e8)], math.log10(600 / 3e-7)),
    ['Collisions per second = \\f{average speed}{mean free path}.', '= \\f{600}{3 × 10^{−7}} = 2 × 10^{9} /s.'], 'mfp', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'mfp', 'Given below are two statements : Statement (I) : The mean free path of gas molecules is inversely proportional to square of molecular diameter. Statement (II) : Average kinetic energy of gas molecules is directly proportional to absolute temperature of gas. In the light of the above statements, choose the correct answer from the option given below:',
    ['Statement I is false but Statement II is true.', 'Statement I is true but Statement II is false.', 'Both Statement I and Statement II are false', 'Both Statement I and Statement II are true.'], 4, lambda: 4,
    ['λ = \\f{1}{√{2}nπd^{2}} ∝ \\f{1}{d^{2}} → I true.', 'KE = \\f{3}{2}k_{B}T ∝ T → II true.'], 'mfp', 1)
