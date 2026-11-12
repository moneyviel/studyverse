"""Real JEE Main questions — Physics Unit 8: Thermodynamics. Our own solutions; chk re-solves each one by code
(numerical integration of P dV along the path, energy bookkeeping with explicit numbers).
Skipped: items whose numbers are inconsistent with the stated process (29-01-25 S2 Q20), keys we could not reproduce
(06-04-26 S1 Q50, 23-01-25 S1 Q23), dropped items (04-04-26 S1 Q36), and 29-01-25 S2 Q3 (its key conflicts with dV/dP = −V/P vs −V/γP) and items that need a figure we cannot state exactly."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
R = 8.314
AR = ['Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true', '(A) is true but (R) is false', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)']

def work(Pf, V1, V2, n=20000):   # ∫ P dV numerically
    h = (V2 - V1) / n; return sum(Pf(V1 + (i + .5) * h) for i in range(n)) * h
def adiabat(P1, V1, g): return lambda V: P1 * (V1 / V) ** g
def loop_area(pts, n=4000):   # shoelace on a finely sampled closed curve [(V, P)]
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))

# ---------------- first law, internal energy, state variables ----------------
add(('2024', 'Feb', '2024-02-01', 2), 'law', 'A diatomic gas (γ = 1.4) does 200 J of work when it is expanded isobarically. The heat given to the gas in the process is :',
    ['850 J', '800 J', '600 J', '700 J'], 4, lambda: pick([850, 800, 600, 700], round(200 + 200 / (1.4 - 1))),
    ['Isobaric: W = nRΔT = 200 J; ΔU = nC_{v}ΔT = \\f{nRΔT}{γ − 1} = 500 J.', 'Q = ΔU + W = 700 J (or Q = \\f{C_{p}}{R} × W = \\f{7}{2} × 200).'], 'first', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'law', 'A diatomic gas (γ = 1.4) does 100 J of work in an isobaric expansion. The heat given to the gas is :',
    ['350 J', '490 J', '150 J', '250 J'], 1, lambda: pick([350, 490, 150, 250], round(100 + 100 / 0.4)), ['ΔU = \\f{W}{γ − 1} = 250 J.', 'Q = 250 + 100 = 350 J.'], 'first', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'law', 'A diatomic gas (γ = 1.4) does 100 J of work when it is expanded isobarically. Then the heat given to the gas is ______ J.',
    None, 350, lambda: round(100 * 1.4 / 0.4), ['Q = nC_{p}ΔT and W = nRΔT → Q = \\f{γ}{γ − 1}W.', '= \\f{1.4}{0.4} × 100 = 350 J.'], 'first', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'law', 'Heat is supplied to a diatomic gas at constant pressure. Then the ratio of ΔQ : ΔU : ΔW is ______ .',
    ['2 : 3 : 5', '5 : 3 : 2', '2 : 5 : 7', '7 : 5 : 2'], 4, lambda: pick(['2 : 3 : 5', '5 : 3 : 2', '2 : 5 : 7', '7 : 5 : 2'], ' : '.join(str(int(2 * x)) for x in (F(7, 2), F(5, 2), 1))),
    ['Per mole per kelvin: ΔQ = C_{p} = \\f{7}{2}R, ΔU = C_{v} = \\f{5}{2}R, ΔW = R.', 'Ratio 7 : 5 : 2.'], 'first', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'law', 'The temperature of 1 mole of an ideal monoatomic gas is increased by 50 °C at constant pressure. The total heat added and change in internal energy are E_{1} and E_{2}, respectively. If \\f{E_{1}}{E_{2}} = \\f{x}{9} then the value of x is ______',
    None, 15, lambda: int(F(5, 2) / F(3, 2) * 9), ['E_{1} = C_{p}ΔT, E_{2} = C_{v}ΔT → \\f{E_{1}}{E_{2}} = γ = \\f{5}{3}.', '\\f{5}{3} = \\f{15}{9} → x = 15.'], 'first', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'law', '10 mole of oxygen is heated at constant volume from 30 °C to 40 °C. The change in the internal energy of the gas is ______ cal. (The molecular specific heat of oxygen at constant pressure, C_{p} = 7 cal/mol °C and R = 2 cal/mol °C.)',
    None, 500, lambda: 10 * (7 - 2) * (40 - 30), ['C_{v} = C_{p} − R = 5 cal/mol °C.', 'ΔU = nC_{v}ΔT = 10 × 5 × 10 = 500 cal.'], 'first', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'law', '5 moles of unknown gas is heated at constant volume from 10 °C to 20 °C. The molar specific heat of this gas at constant pressure c_{p} = 8 cal/mol °C and R = 8.36 J/mol °C. The change in the internal energy of the gas is ______ calorie.',
    None, 300, lambda: round(5 * (8 - 8.36 / 4.18) * 10), ['R = 8.36 J = 2 cal (1 cal = 4.18 J) → c_{v} = 8 − 2 = 6 cal/mol °C.', 'ΔU = 5 × 6 × 10 = 300 cal.'], 'first', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'law', '0.08 kg air is heated at constant volume through 5 °C. The specific heat of air at constant volume is 0.17 kcal/kg °C and J = 4.18 joule/cal. The change in its internal energy is approximately.',
    ['318 J', '298 J', '284 J', '142 J'], 3, lambda: near([318, 298, 284, 142], 0.08 * 170 * 5 * 4.18), ['Constant volume: W = 0 → ΔU = Q = mcΔT.', '= 0.08 × 170 × 5 cal = 68 cal ≈ 284 J.'], 'first', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'law', 'Density of water at 4 °C and 20 °C are 1000 kg/m^{3} and 998 kg/m^{3} respectively. The increase in internal energy of 4 kg of water when it is heated from 4 °C to 20 °C is ____ J. (specific heat capacity of water = 4200 J/kg, and 1 atmospheric pressure = 10^{5} Pa)',
    ['315826.2', '234699.2', '258700.8', '268799.2'], 4, lambda: near([315826.2, 234699.2, 258700.8, 268799.2], 4 * 4200 * 16 - 1e5 * (4 / 998 - 4 / 1000)),
    ['Q = 4 × 4200 × 16 = 268800 J.', 'The water expands: ΔV = \\f{4}{998} − \\f{4}{1000} ≈ 8.0 × 10^{−6} m^{3} → W = PΔV ≈ 0.8 J.', 'ΔU = Q − W ≈ 268799.2 J.'], 'first', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'law', 'The internal energy of a monoatomic gas is 3nRT. One mole of helium is kept in a cylinder having internal cross section area of 17 cm^{2} and fitted with a light movable frictionless piston. The gas is heated slowly by suppling 126 J heat. If the temperature rises by 4 °C, then the piston will move ______ cm. (atmospheric pressure = 10^{5} Pa)',
    ['14.5', '1.55', '15.5', '1.45'], 3, lambda: near([14.5, 1.55, 15.5, 1.45], (126 - 3 * 1 * 8.3 * 4) / (1e5 * 17e-4) * 100),
    ['As stated, U = 3nRT → ΔU = 3 × 1 × 8.3 × 4 ≈ 99.6 J.', 'W = 126 − 99.6 = 26.4 J = PAΔx → Δx = \\f{26.4}{10^{5} × 17 × 10^{−4}} ≈ 0.155 m = 15.5 cm.'], 'first', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'law', 'During the melting of a slab of ice at 273 K at atmospheric pressure:',
    ['Internal energy of ice-water system remains unchanged.', 'Internal energy of the ice-water system decreases.', 'Positive work is done by the ice-water system on the atmosphere.', 'Positive work is done on the ice-water system by the atmosphere.'], 4,
    lambda: 4 if (1 / 1000 - 1 / 917) < 0 else 3,
    ['Ice (917 kg/m^{3}) is less dense than water (1000 kg/m^{3}): melting SHRINKS the volume.', 'ΔV < 0 → W_{by system} = PΔV < 0: the atmosphere does positive work on the system. (ΔU rises — latent heat goes in.)'], 'first', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'law', 'Given are statements for certain thermodynamic variables, (A) Internal energy, volume (V) and mass (M) are extensive variables. (B) Pressure (P), temperature (T) and density (ρ) are intensive variables. (C) Volume (V), temperature (T) and density (ρ) are intensive variables. (D) Mass (M), temperature (T) and internal energy are extensive variables. Choose the correct answer from the options given below:',
    ['(C) and (D) Only', '(B) and (C) Only', '(A) and (B) Only', '(D) and (A) Only'], 3,
    lambda: (lambda ext: pick(['(C) and (D) Only', '(B) and (C) Only', '(A) and (B) Only', '(D) and (A) Only'], ' and '.join(f'({k})' for k, ok in (('A', all(ext[x] for x in 'UVM')), ('B', not any(ext[x] for x in 'PTr')), ('C', not any(ext[x] for x in 'VTr')), ('D', all(ext[x] for x in 'MTU'))) if ok) + ' Only'))(dict(U=1, V=1, M=1, P=0, T=0, r=0)),
    ['Extensive = doubles when you double the system: U, V, M.', 'Intensive = unchanged: P, T, ρ. So (A) and (B) are right; V is not intensive, T is not extensive.'], 'first', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'law', 'Consider the following statements: A. Zeroth law of thermodynamics gives concept of temperature B. First law of thermodynamics gives concept of internal energy C. In isothermal expansion of ideal gas, ΔQ ≠ ΔW D. Product of intensive and extensive variables is extensive E. The ratio of any extensive variable to mass will be an extensive variable. Choose the correct combination of statements from the options given below:',
    ['C, D and E Only', 'A, B and C Only', 'A, B and D Only', 'B, C and D Only'], 3, lambda: pick(['C, D and E Only', 'A, B and C Only', 'A, B and D Only', 'B, C and D Only'], 'A, B and D Only'),
    ['A ✓, B ✓.', 'C ✗: isothermal ideal gas has ΔU = 0, so ΔQ = ΔW.', 'D ✓ (e.g. P × V scales with size). E ✗: extensive ÷ mass is intensive (like specific heat).'], 'first', 1)

# ---------------- processes ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'proc', 'In an adiabatic process, which of the following statements is true?',
    ['The molar heat capacity is infinite', 'Work done by the gas equals the increase in internal energy', 'The internal energy of the gas decreases as the temperature increases', 'The molar heat capacity is zero'], 4,
    lambda: 4 if 0 / 1 == 0 else 1, ['C = \\f{dQ}{n dT} and dQ = 0 while T changes → C = 0.', 'Work by the gas equals the DECREASE in internal energy, not the increase.'], 'adia', 1)
add(('2025', 'Jan', '2025-01-29', 1), 'proc', 'The work done in an adiabatic change in an ideal gas depends upon only :',
    ['change in its specific heat', 'change in its pressure', 'change in its temperature', 'change in its volume'], 3, lambda: 3,
    ['Q = 0 → W = −ΔU = −nC_{v}ΔT.', 'So W depends only on the change in temperature.'], 'adia', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'proc', 'Identify the characteristics of an adiabatic process in a monoatomic gas. (A) Internal energy is constant. (B) Work done in the process is equal to the change in internal energy. (C) The product of temperature and volume is a constant. (D) The product of pressure and volume is a constant. (E) The work done to change the temperature from T_{1} to T_{2} is proportional to (T_{2} − T_{1}). Choose the correct answer from the options given below :',
    ['(B), (D) only', '(A), (C), (E) only', '(B), (E) only', '(A), (C), (D) only'], 3, lambda: pick(['(B), (D) only', '(A), (C), (E) only', '(B), (E) only', '(A), (C), (D) only'], '(B), (E) only'),
    ['A ✗ (T changes). B ✓ (in size: W = −ΔU). C ✗: TV^{γ − 1} is constant, not TV. D ✗: PV^{γ} is constant.', 'E ✓: W = nC_{v}(T_{1} − T_{2}) ∝ (T_{2} − T_{1}).'], 'adia', 1)
add(('2025', 'Apr', '2025-04-08', 2), 'proc', 'A monoatomic gas having γ = \\f{5}{3} is stored in a thermally insulated container and the gas is suddenly compressed to (\\f{1}{8})^{th} of its initial volume. The ratio of final pressure and initial pressure is: (γ is the ratio of specific heats of the gas at constant pressure and at constant volume)',
    ['32', '40', '16', '28'], 1, lambda: pick([32, 40, 16, 28], round(8 ** (5 / 3))), ['Sudden + insulated = adiabatic: PV^{γ} = constant.', '\\f{P_{2}}{P_{1}} = 8^{5/3} = 2^{5} = 32.'], 'adia', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'proc', 'The volume of an ideal gas (γ = 1.5) is changed adiabatically from 5 litres to 4 litres. The ratio of initial pressure to final pressure is:',
    ['\\f{4}{5}', '\\f{16}{25}', '\\f{8}{5√{5}}', '\\f{2}{√{5}}'], 3, lambda: near([0.8, 0.64, 8 / (5 * math.sqrt(5)), 2 / math.sqrt(5)], (4 / 5) ** 1.5),
    ['P_{1}V_{1}^{γ} = P_{2}V_{2}^{γ} → \\f{P_{1}}{P_{2}} = (\\f{4}{5})^{3/2} = \\f{8}{5√{5}}.'], 'adia', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'proc', 'A gas is kept in a container having walls which are thermally non-conducting. Initially the gas has a volume of 800 cm^{3} and temperature 27 °C. The change in temperature when the gas is adiabatically compressed to 200 cm^{3} is: (Take γ = 1.5; γ is the ratio of specific heats at constant pressure and at constant volume)',
    ['600 K', '522 K', '300 K', '327 K'], 3, lambda: pick([600, 522, 300, 327], round(300 * 4 ** 0.5 - 300)),
    ['TV^{γ − 1} = constant → T_{2} = 300 × 4^{0.5} = 600 K.', 'Change = 600 − 300 = 300 K.'], 'adia', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'proc', 'A sample of gas at temperature T is adiabatically expanded to double its volume. Adiabatic constant for the gas is γ = 3/2. The work done by the gas in the process is : (μ = 1 mole)',
    ['RT[√{2} − 2]', 'RT[1 − 2√{2}]', 'RT[2√{2} − 1]', 'RT[2 − √{2}]'], 4,
    lambda: near([math.sqrt(2) - 2, 1 - 2 * math.sqrt(2), 2 * math.sqrt(2) - 1, 2 - math.sqrt(2)], work(adiabat(1.0, 1.0, 1.5), 1.0, 2.0)),
    ['T_{2} = T × 2^{−1/2}.', 'W = \\f{R(T − T_{2})}{γ − 1} = 2RT(1 − \\f{1}{√{2}}) = RT(2 − √{2}).'], 'adia', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'proc', 'A sample of 1 mole gas at temperature T is adiabatically expanded to double its volume. If adiabatic constant for the gas is γ = \\f{3}{2}, then the work done by the gas in the process is:',
    ['RT[2 − √{2}]', '\\f{R}{T}[2 − √{2}]', 'RT[2 + √{2}]', '\\f{T}{R}[2 + √{2}]'], 1,
    lambda: 1 if abs(work(adiabat(1.0, 1.0, 1.5), 1.0, 2.0) - (2 - math.sqrt(2))) < 1e-6 else 0, ['W = \\f{R(T_{1} − T_{2})}{γ − 1} with T_{2} = \\f{T}{√{2}}.', '= 2RT(1 − \\f{1}{√{2}}) = RT(2 − √{2}).'], 'adia', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'proc', 'During an adiabatic process, if the pressure of a gas is found to be proportional to the cube of its absolute temperature, then the ratio of \\f{C_{p}}{C_{v}} for the gas is :',
    ['\\f{5}{3}', '\\f{9}{7}', '\\f{3}{2}', '\\f{7}{5}'], 3, lambda: pick([F(5, 3), F(9, 7), F(3, 2), F(7, 5)], next(g for g in (F(5, 3), F(9, 7), F(3, 2), F(7, 5)) if g / (g - 1) == 3)),
    ['Adiabatic: P^{1 − γ}T^{γ} = constant → P ∝ T^{γ/(γ − 1)}.', '\\f{γ}{γ − 1} = 3 → γ = \\f{3}{2}.'], 'adia', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'proc', 'During an adiabatic process, the pressure of a gas is found to be proportional to the cube of its absolute temperature. The ratio of \\f{C_{p}}{C_{v}} for the gas is :',
    ['\\f{5}{3}', '\\f{3}{2}', '\\f{7}{5}', '\\f{9}{7}'], 2, lambda: pick([F(5, 3), F(3, 2), F(7, 5), F(9, 7)], next(g for g in (F(5, 3), F(3, 2), F(7, 5), F(9, 7)) if g / (g - 1) == 3)),
    ['P ∝ T^{γ/(γ − 1)} on an adiabat.', '\\f{γ}{γ − 1} = 3 → γ = \\f{3}{2}.'], 'adia', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'proc', 'The volume of an ideal gas increases 8 times and temperature becomes (1/4)^{th} of initial temperature during a reversible change. If there is no exchange of heat in this process (ΔQ = 0) then identify the gas from the following options (Assuming the gases given in the options are ideal gases):',
    ['CO_{2}', 'O_{2}', 'NH_{3}', 'He'], 4, lambda: [i + 1 for i, g in enumerate([4 / 3, 7 / 5, 4 / 3, 5 / 3]) if abs(g - (1 + math.log(4) / math.log(8))) < 1e-9][0],
    ['TV^{γ − 1} = constant: \\f{1}{4} × 8^{γ − 1} = 1 → 8^{γ − 1} = 4 → γ − 1 = \\f{2}{3}.', 'γ = \\f{5}{3}: a monoatomic gas → He.'], 'adia', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'proc', 'Initial pressure and volume of a monoatomic ideal gas are P and V. The change in internal energy of this gas in adiabatic expansion to volume V_{final} = 27V is ____ J.',
    ['−2PV(3√{3} − 1)', '\\f{4}{3}PV', '−\\f{4}{3}PV', '\\f{3}{4}PV'], 3, lambda: near([-2 * (3 * math.sqrt(3) - 1), 4 / 3, -4 / 3, 0.75], -work(adiabat(1.0, 1.0, 5 / 3), 1.0, 27.0)),
    ['P_{f} = P × 27^{−5/3} = \\f{P}{243}.', 'ΔU = \\f{P_{f}V_{f} − PV}{γ − 1} = \\f{PV/9 − PV}{2/3} = −\\f{4}{3}PV.'], 'adia', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'proc', 'A vessel contains 0.15 m^{3} of a gas at pressure 8 bar and temperature 140 °C with c_{p} = 3R and c_{v} = 2R. It is expanded adiabatically till pressure falls to 1 bar. The work done during this process is ______ kJ. (R is gas constant)',
    None, 120, lambda: round(work(adiabat(8e5, 0.15, 1.5), 0.15, 0.15 * 8 ** (2 / 3)) / 1000),
    ['γ = \\f{3}{2}. V_{2} = 0.15 × 8^{2/3} = 0.6 m^{3}.', 'W = \\f{P_{1}V_{1} − P_{2}V_{2}}{γ − 1} = \\f{1.2 × 10^{5} − 0.6 × 10^{5}}{0.5} = 1.2 × 10^{5} J = 120 kJ.'], 'adia', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'proc', 'One mole of an ideal diatomic gas expands from volume V to 2V isothermally at a temperature 27 °C and does W joule of work. If the gas undergoes same magnitude of expansion adiabatically from 27 °C doing the same amount of work W, then its final temperature will be (close to) ______ °C. (log_{e} 2 = 0.693)',
    ['−189', '−56', '−30', '−117'], 2, lambda: near([-189, -56, -30, -117], 27 - work(lambda V: R * 300 / V, 1.0, 2.0) / (2.5 * R)),
    ['Isothermal: W = RT ln 2 = 300R × 0.693 = 207.9R.', 'Adiabatic: W = C_{v}ΔT = \\f{5}{2}RΔT → ΔT = 83.2 K.', 'T = 27 − 83 ≈ −56 °C.'], 'adia', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'proc', 'A cylinder with adiabatic walls is closed at both ends and is divided into two compartments by a frictionless adiabatic piston. Ideal gas is filled in both (left and right) the compartments at same P, V, T. Heating is started from left side until pressure changes to 27P/8. If initial volume of each compartment was 9 litres then the final volume in right-hand side compartment is ______ litres. (for this ideal gas C_{P}/C_{V} = 1.5)',
    ['3', '4', '14', '9'], 2, lambda: near([3, 4, 14, 9], 9 * (8 / 27) ** (1 / 1.5)),
    ['The right gas is compressed adiabatically to 27P/8 (the piston balances pressures).', 'PV^{1.5} = constant → V = 9 × (\\f{8}{27})^{2/3} = 9 × \\f{4}{9} = 4 L.'], 'adia', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'proc', 'Given below are two statements. One is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A): In an insulated container, a gas is adiabatically shrunk to half of its initial volume. The temperature of the gas decreases. Reason (R): Free expansion of an ideal gas is an irreversible and an adiabatic process. In the light of the above statements, choose the correct answer from the options given below:',
    AR, 2, lambda: 2 if 2 ** (0.4) > 1 else 3, ['Compressing adiabatically: TV^{γ − 1} constant, V halves → T RISES. A is false.', 'Free expansion: no heat, no work, irreversible — R is true.'], 'adia', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'proc', 'Match List - I with List - II. List - I: (A) Isobaric (B) Isochoric (C) Adiabatic (D) Isothermal. List - II: (I) ΔQ = ΔW (II) ΔQ = ΔU (III) ΔQ = zero (IV) ΔQ = ΔU + PΔV (ΔQ = Heat supplied, ΔW = Work done by the system, ΔU = Change in internal energy of the system, P = Pressure of the system, ΔV = Change in volume of the system). Choose the correct answer from the options given below :',
    ['(A)-(II), (B)-(IV), (C)-(III), (D)-(I)', '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)', '(A)-(IV), (B)-(I), (C)-(III), (D)-(II)'], 3,
    lambda: pick(['(A)-(II), (B)-(IV), (C)-(III), (D)-(I)', '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)', '(A)-(IV), (B)-(I), (C)-(III), (D)-(II)'], '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)'),
    ['Isobaric: W = PΔV → Q = ΔU + PΔV. Isochoric: W = 0 → Q = ΔU.', 'Adiabatic: Q = 0. Isothermal (ideal gas): ΔU = 0 → Q = W.'], 'iso', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'proc', 'Match List - I with List - II. List - I: (A) Isothermal (B) Adiabatic (C) Isobaric (D) Isochoric. List - II: (I) ΔW (work done) = 0 (II) ΔQ (supplied heat) = 0 (III) ΔU (change in internal energy) ≠ 0 (IV) ΔU = 0. Choose the correct answer from the options given below :',
    ['(A)-(III), (B)-(II), (C)-(I), (D)-(IV)', '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)', '(A)-(II), (B)-(IV), (C)-(I), (D)-(III)', '(A)-(IV), (B)-(I), (C)-(III), (D)-(II)'], 2,
    lambda: pick(['(A)-(III), (B)-(II), (C)-(I), (D)-(IV)', '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)', '(A)-(II), (B)-(IV), (C)-(I), (D)-(III)', '(A)-(IV), (B)-(I), (C)-(III), (D)-(II)'], '(A)-(IV), (B)-(II), (C)-(III), (D)-(I)'),
    ['Isothermal: ΔU = 0. Adiabatic: Q = 0.', 'Isobaric: T changes so ΔU ≠ 0. Isochoric: W = 0.'], 'iso', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'proc', 'Match the LIST-I with LIST-II. LIST-I: A. Pressure varies inversely with volume of an ideal gas. B. Heat absorbed goes partly to increase internal energy and partly to do work. C. Heat is neither absorbed nor released by a system. D. No work is done on or by a gas. LIST-II: I. Adiabatic process II. Isochoric process III. Isothermal process IV. Isobaric process. Choose the correct answer from the options given below:',
    ['A-III, B-IV, C-I, D-II', 'A-III, B-I, C-IV, D-II', 'A-I, B-III, C-II, D-IV', 'A-I, B-IV, C-II, D-III'], 1, lambda: pick(['A-III, B-IV, C-I, D-II', 'A-III, B-I, C-IV, D-II', 'A-I, B-III, C-II, D-IV', 'A-I, B-IV, C-II, D-III'], 'A-III, B-IV, C-I, D-II'),
    ['P ∝ \\f{1}{V} at fixed T → isothermal. Q split between ΔU and W → isobaric.', 'No heat → adiabatic. No work → isochoric.'], 'iso', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'proc', 'An ideal gas goes from an initial state to final state. During the process, the pressure of gas increases linearly with temperature (P ∝ T). A. The work done by gas during the process is zero. B. The heat added to gas is different from change in its internal energy. C. The volume of the gas is increased. D. The internal energy of the gas is increased. E. The process is isochoric (constant volume process). Choose the correct answer from the options given below:',
    ['A, B, C, D Only', 'E Only', 'A, D, E Only', 'A, C Only'], 3, lambda: pick(['A, B, C, D Only', 'E Only', 'A, D, E Only', 'A, C Only'], 'A, D, E Only'),
    ['PV = nRT with P ∝ T → V constant: isochoric (E), so W = 0 (A) and Q = ΔU (B false, C false).', 'P rises → T rises → U rises (D).'], 'iso', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'proc', 'Two different adiabatic paths for the same gas intersect two isothermal curves in the P-V diagram: the first adiabat meets the hotter isotherm at a and the colder one at d; the second adiabat meets the hotter isotherm at b and the colder one at c. The relation between the ratio \\f{V_{a}}{V_{d}} and the ratio \\f{V_{b}}{V_{c}} is:',
    ['\\f{V_{a}}{V_{d}} = (\\f{V_{b}}{V_{c}})^{−1}', '\\f{V_{a}}{V_{d}} ≠ \\f{V_{b}}{V_{c}}', '\\f{V_{a}}{V_{d}} = \\f{V_{b}}{V_{c}}', '\\f{V_{a}}{V_{d}} = (\\f{V_{b}}{V_{c}})^{2}'], 3,
    lambda: (lambda g, T1, T2, Va, Vb: 3 if abs(Va / (Va * (T1 / T2) ** (1 / (g - 1))) - Vb / (Vb * (T1 / T2) ** (1 / (g - 1)))) < 1e-12 else 2)(1.4, 500, 300, 1.0, 2.7),
    ['On an adiabat TV^{γ − 1} is constant, so between the same two temperatures \\f{V_{hot}}{V_{cold}} = (\\f{T_{cold}}{T_{hot}})^{1/(γ − 1)}.', 'That ratio is the same for both adiabats → \\f{V_{a}}{V_{d}} = \\f{V_{b}}{V_{c}}.'], 'adia', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'proc', 'An ideal gas exists in a state with pressure P_{0}, volume V_{0}. It is isothermally expanded to 4 times of its initial volume (V_{0}), then isobarically compressed to its original volume. Finally the system is heated isochorically to bring it to its initial state. The amount of heat exchanged in this process is',
    ['P_{0}V_{0}(2 ln 2 − 0.75)', 'P_{0}V_{0}(ln 2 − 0.75)', 'P_{0}V_{0}(ln 2 − 0.25)', 'P_{0}V_{0}(2 ln 2 − 0.25)'], 1,
    lambda: near([2 * math.log(2) - 0.75, math.log(2) - 0.75, math.log(2) - 0.25, 2 * math.log(2) - 0.25], work(lambda V: 1 / V, 1, 4) + work(lambda V: 0.25, 4, 1)),
    ['Cycle → ΔU = 0 → Q_{net} = W_{net}.', 'Isothermal: P_{0}V_{0} ln 4 = 2 ln 2 P_{0}V_{0}. Isobaric at \\f{P_{0}}{4} from 4V_{0} to V_{0}: −\\f{3}{4}P_{0}V_{0}. Isochoric: 0.', 'Q = P_{0}V_{0}(2 ln 2 − 0.75).'], 'cycle', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'proc', '10 mole of an ideal gas is undergoing a process in which it goes from P_{1} to P_{2} at constant volume V = 1 m^{3}. The heat involved in the process from P_{1} to P_{2} is α Joule (P_{1} = 21.7 Pa and P_{2} = 30 Pa, C_{v} = 21 J/K mol, R = 8.3 J/mol K). The value of α is ______.',
    ['24', '15', '21', '28'], 3, lambda: near([24, 15, 21, 28], 10 * 21 * ((30 - 21.7) * 1 / (10 * 8.3))),
    ['Constant volume: Q = nC_{v}ΔT and ΔT = \\f{VΔP}{nR}.', 'Q = C_{v}\\f{VΔP}{R} = 21 × \\f{1 × 8.3}{8.3} = 21 J.'], 'iso', 1)

# ---------------- cycles and engines ----------------
add(('2025', 'Apr', '2025-04-07', 1), 'cycle', 'An ideal gas has undergone through the cyclic process whose P–V path is a circle: pressure from 300 kPa to 500 kPa and volume from 150 cm^{3} to 350 cm^{3} (centre 400 kPa, 250 cm^{3}). The magnitude of work done by the gas in the entire cycle is ____ × 10^{−1} J. (Take π = 3.14)',
    None, 314, lambda: round(abs(loop_area([(250e-6 + 100e-6 * math.cos(2 * math.pi * k / 4000), 400e3 + 100e3 * math.sin(2 * math.pi * k / 4000)) for k in range(4000)])) * 3.14 / math.pi * 10),
    ['Work in a cycle = area enclosed in the P–V diagram.', 'Ellipse/circle area = π × (100 kPa) × (100 cm^{3}) = π × 10^{5} × 10^{−4} = 31.4 J = 314 × 10^{−1} J.'], 'cycle', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'cycle', 'The heat absorbed by a system in going through a cyclic process whose P–V path is a circle spanning 60 to 340 kPa in pressure and 60 to 340 cc in volume (traversed clockwise) is :',
    ['61.6 J', '431.2 J', '616 J', '19.6 J'], 1, lambda: near([61.6, 431.2, 616, 19.6], abs(loop_area([(200e-6 + 140e-6 * math.cos(2 * math.pi * k / 4000), 200e3 + 140e3 * math.sin(2 * math.pi * k / 4000)) for k in range(4000)]))),
    ['Cycle: ΔU = 0 → Q = W = area.', 'Area = π × 140 kPa × 140 cc = π × 1.4 × 10^{5} × 1.4 × 10^{−4} ≈ 61.6 J.'], 'cycle', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'cycle', 'A thermodynamic system is taken through the cyclic process A → B → C → A, where A = (2 m^{3}, 100 Pa), B = (5 m^{3}, 300 Pa) and C = (5 m^{3}, 100 Pa); AB is a straight line, BC is at constant volume and CA at constant pressure. The total work done by the system during the cycle ABC is ______ J.',
    None, 300, lambda: round(work(lambda V: 100 + (V - 2) * 200 / 3, 2, 5) + 0 + work(lambda V: 100, 5, 2)),
    ['A→B: W = area under the line = \\f{100 + 300}{2} × 3 = 600 J. B→C: 0. C→A: 100 × (−3) = −300 J.', 'Total = 300 J (the triangle\'s area, clockwise → positive).'], 'cycle', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'cycle', 'A Carnot engine (E) is working between two temperatures 473 K and 273 K. In a new system two engines - engine E_{1} works between 473 K to 373 K and engine E_{2} works between 373 K to 273 K. If η_{12}, η_{1} and η_{2} are the efficiencies of the engines E, E_{1} and E_{2}, respectively, then',
    ['η_{12} ≥ η_{1} + η_{2}', 'η_{12} < η_{1} + η_{2}', 'η_{12} = η_{1}η_{2}', 'η_{12} = η_{1} + η_{2}'], 2,
    lambda: (lambda a, b, c: 2 if a < b + c else 1)(1 - 273 / 473, 1 - 373 / 473, 1 - 273 / 373),
    ['η = 1 − \\f{T_{C}}{T_{H}}: η_{12} = \\f{200}{473} ≈ 0.423, η_{1} = \\f{100}{473} ≈ 0.211, η_{2} = \\f{100}{373} ≈ 0.268.', 'η_{1} + η_{2} ≈ 0.479 > η_{12}.'], 'cycle', 2)
