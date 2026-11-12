"""Real JEE Main questions — Chemistry Unit 4: Chemical Thermodynamics. Our own solutions; chk re-solves the numbers
(first law, Hess cycles, bond-enthalpy and Born–Haber cycles, ΔG = ΔH − TΔS). Skipped: cycles drawn without readable
axes, a heat-transfer item that does not say constant P or V, and a ΔU of vaporisation whose official key (38) we
could not reproduce (we get 37.4)."""
import math
from common import new_registry, pick, near, verify
P, add = new_registry()
R = 8.314

# ---------------- first law, work, heat, ΔH vs ΔU ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'law', 'Choose the correct option for free expansion of an ideal gas under adiabatic condition from the following :',
    ['q = 0, ΔT ≠ 0, w = 0', 'q = 0, ΔT < 0, w ≠ 0', 'q ≠ 0, ΔT = 0, w = 0', 'q = 0, ΔT = 0, w = 0'], 4, lambda: 4,
    ['Adiabatic → q = 0. Free expansion (into vacuum, p_{ext} = 0) → w = 0.', 'So ΔU = 0, and for an ideal gas U depends only on T → ΔT = 0.'], 'law', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'law', 'Arrange the following in order of magnitude of work done by the system/on the system at constant temperature. (a) |w_{reversible}| for expansion in infinite stages. (b) |w_{irreversible}| for expansion in single stage. (c) |w_{reversible}| for compression in infinite stages. (d) |w_{irreversible}| for compression in single stage. Choose the correct answer from the options given below :',
    ['c = a > d > b', 'a > b > c > d', 'a > c > b > d', 'd > c = a > b'], 4,
    lambda: (lambda a, b, c, d: 4 if d > c and abs(c - a) < 1e-9 and a > b else 0)(1 * math.log(2), 1 * (1 - 0.5), 1 * math.log(2), 1 * (2 - 1)),
    ['Take 1 → 2 volume at RT = 1: reversible either way |w| = ln 2 ≈ 0.69 (a = c).', 'Single-stage expansion against the final pressure ½: |w| = 0.5 (b). Single-stage compression against pressure 2: |w| = 1 (d).', 'd > c = a > b.'], 'law', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'law', 'Which of the following properties will change when system containing solution 1 (10 mol of solute x + 10 L of water) will become solution 2 (1 L of solution 1 + 1 mol of solute x + 1 L of water)?',
    ['Gibbs free energy', 'Concentration', 'Molar heat capacity', 'Density'], 1, lambda: 1,
    ['Solution 2 = 1 mol x in 1 L + 1 mol x in 1 L — the same 1 mol per litre composition, so intensive properties (concentration, density, molar heat capacity) stay the same.', 'The amount is different (2 L instead of 10 L), so an EXTENSIVE property like G changes.'], 'law', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'law', 'A sample of n-octane (1.14 g) was completely burnt in excess of oxygen in a bomb calorimeter, whose heat capacity is 5 kJ K^{−1}. As a result of combustion reaction, the temperature of the calorimeter is increased by 5 K. The magnitude of the heat of combustion of octane at constant volume is ____ kJ mol^{−1} (nearest integer).',
    None, 2500, lambda: round(5 * 5 / (1.14 / 114)), ['Heat = CΔT = 5 × 5 = 25 kJ for \\f{1.14}{114} = 0.01 mol.', 'ΔU_{c} = 2500 kJ mol^{−1} (bomb calorimeter = constant volume).'], 'law', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'law', 'One mole of an ideal gas expands isothermally and reversibly from 10 dm^{3} to 20 dm^{3} at 300 K. ΔU, q and work done in the process respectively are (Given: R = 8.3 J K^{−1} mol^{−1}, ln 10 = 2.3, log 2 = 0.30, log 3 = 0.48)',
    ['0, −17.18 kJ, 1.718 J', '0, 21.84 kJ, 21.84 kJ', '0, 21.84 kJ, −1.726 J', '0, 1.718 kJ, −1.718 kJ'], 4,
    lambda: (lambda w: 4 if abs(w + 1.718) < 0.002 else 0)(-1 * 8.3 * 300 * 2.3 * 0.30 / 1000),
    ['Isothermal ideal gas → ΔU = 0.', 'w = −nRT ln\\f{V_{2}}{V_{1}} = −8.3 × 300 × 2.3 × 0.30 = −1718 J; q = −w = +1.718 kJ.'], 'law', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'law', 'Consider the given data : (a) HCl(g) + 10H_{2}O(l) → HCl.10H_{2}O, ΔH = −69.01 kJ mol^{−1} (b) HCl(g) + 40H_{2}O(l) → HCl.40H_{2}O, ΔH = −72.79 kJ mol^{−1}. Choose the correct statement :',
    ['The heat of solution depends on the amount of solvent.', 'The heat of dilution for the HCl (HCl.10H_{2}O to HCl.40H_{2}O) is 3.78 kJ mol^{−1}.', 'Dissolution of gas in water is an endothermic process.', 'The heat of formation of HCl solution is represented by both (a) and (b).'], 1,
    lambda: 1 if abs((-72.79) - (-69.01) + 3.78) < 1e-9 else 0,
    ['(a) and (b) differ only in the amount of water, and their ΔH differ → (1) ✓.', 'Dilution: −72.79 − (−69.01) = −3.78 kJ (heat RELEASED, not +3.78). Both are exothermic.'], 'law', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'law', 'Three moles of an ideal gas are compressed isothermally from 60 L to 20 L using constant pressure of 5 atm. The magnitude of heat exchange Q for the compression is ____ Lit. atm.',
    None, 200, lambda: round(abs(-(-5 * (20 - 60)))), ['w = −p_{ext}ΔV = −5(20 − 60) = +200 L atm (work done ON the gas).', 'Isothermal ideal gas: ΔU = 0 → Q = −w = −200 L atm (heat released); magnitude 200.'], 'law', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'law', 'The heat of combustion of solid benzoic acid at constant volume is −321.30 kJ at 27 °C. The heat of combustion at constant pressure is (−321.30 − xR) kJ, the value of x is',
    None, 150, lambda: round(-(7 - 7.5) * 300), ['C_{6}H_{5}COOH(s) + \\f{15}{2}O_{2} → 7CO_{2} + 3H_{2}O(l): Δn_{g} = 7 − 7.5 = −½.', 'ΔH = ΔU + Δn_{g}RT = −321.30 − ½ × 300R → x = 150.'], 'law', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'law', 'An ideal gas, C̄_{V} = \\f{5}{2}R, is expanded adiabatically against a constant pressure of 1 atm untill it doubles in volume. If the initial temperature and pressure is 298 K and 5 atm, respectively then the final temperature is ____ K (nearest integer).',
    None, 274, lambda: round(298 - 1 * (298 / 5) / 2.5), ['Adiabatic: nC_{V}(T_{2} − T_{1}) = −p_{ext}(V_{2} − V_{1}) with V_{1} = \\f{nRT_{1}}{5}, ΔV = V_{1}.', '\\f{5}{2}(T_{2} − 298) = −\\f{298}{5} → T_{2} = 298 − 23.8 ≈ 274 K.'], 'law', 3)
add(('2025', 'Apr', '2025-04-07', 1), 'law', 'Total enthalpy change for freezing of 1 mol of water at 10 °C to ice at −10 °C is (Given: Δ_{fus}H = x kJ/mol, C_{p}[H_{2}O(l)] = y J mol^{−1} K^{−1}, C_{p}[H_{2}O(s)] = z J mol^{−1} K^{−1})',
    ['x − 10y − 10z', '−10(100x + y + z)', '10(100x + y + z)', '−x − 10y − 10z'], 2,
    lambda: (lambda x, y, z: near([x * 1000 - 10 * y - 10 * z, -10 * (100 * x + y + z), 10 * (100 * x + y + z), -x - 10 * y - 10 * z], -10 * y - 1000 * x - 10 * z))(6.0, 75.3, 36.8),
    ['Cool water 10 → 0 °C: −10y J; freeze: −x kJ = −1000x J; cool ice 0 → −10 °C: −10z J.', 'Total = −10(100x + y + z) J.'], 'law', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'law', 'Standard enthalpy of vapourisation for CCl_{4} is 30.5 kJ mol^{−1}. Heat required for vapourisation of 284 g of CCl_{4} at constant temperature is ____ kJ. (Given molar mass in g mol^{−1}; C = 12, Cl = 35.5)',
    None, 56, lambda: round(284 / (12 + 4 * 35.5) * 30.5), ['M(CCl_{4}) = 154 → 284 g = 1.844 mol.', 'q = 1.844 × 30.5 ≈ 56 kJ.'], 'law', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'law', 'Given below are two statements: Statement I : For an ideal gas, heat capacity at constant volume is always greater than the heat capacity at constant pressure. Statement II : In a constant volume process, no work is produced and all the heat withdrawn goes into the chaotic motion and is reflected by a temperature increase of the ideal gas. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 4, lambda: 4,
    ['C_{p} − C_{V} = R > 0: at constant pressure part of the heat is spent as expansion work → I false.', 'At constant volume w = 0, so q = ΔU, raising T → II true.'], 'law', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'law', 'If 5 moles of an ideal gas expands from 10 L to a volume of 100 L at 300 K under isothermal and reversible condition then work, w, is −x J. The value of x is ____ . (Given R = 8.314 J K^{−1} mol^{−1})',
    None, 28721, lambda: round(5 * R * 300 * 2.303 * math.log10(100 / 10)), ['w = −2.303nRT log\\f{V_{2}}{V_{1}} = −2.303 × 5 × 8.314 × 300 × log 10 ≈ −28 721 J.'], 'law', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'law', 'Arrange the following isothermal processes in order of the magnitude of the work (p−V) involved between states 1 and 2. A. Expansion in single stage w_{A} B. Expansion in multi stages w_{B} C. Compression in single stage w_{C} D. Compression in multi stages w_{D}. Choose the correct option.',
    ['|w_{B}| > |w_{A}| > |w_{C}| > |w_{D}|', '|w_{C}| > |w_{D}| > |w_{A}| > |w_{B}|', '|w_{C}| > |w_{D}| > |w_{B}| > |w_{A}|', '|w_{B}| > |w_{A}| > |w_{D}| > |w_{C}|'], 3,
    lambda: (lambda w: pick(['|w_{B}| > |w_{A}| > |w_{C}| > |w_{D}|', '|w_{C}| > |w_{D}| > |w_{A}| > |w_{B}|', '|w_{C}| > |w_{D}| > |w_{B}| > |w_{A}|', '|w_{B}| > |w_{A}| > |w_{D}| > |w_{C}|'], ' > '.join(f'|w_{{{k}}}|' for k in sorted(w, key=lambda k: -w[k]))))(
        {'A': 0.5 * 1, 'B': (2 / 3) * 0.5 + 0.5 * 0.5, 'C': 1 * 1, 'D': (1 / 1.5) * 0.5 + 1 * 0.5}),   # V 1 → 2 (or back), nRT = 1, two equal steps
    ['Expansion (1 → 2 V): the more stages, the closer to reversible → MORE work out: |w_{B}| > |w_{A}|.', 'Compression: the more stages, the LESS work needed: |w_{C}| > |w_{D}|; and any compression needs more than the matching expansion gives.', '|w_{C}| > |w_{D}| > |w_{B}| > |w_{A}|.'], 'law', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'law', 'Match List-I with List-II. Given V_{1} and V_{2} are initial and final volumes respectively. List-I (Isothermal process): A. Reversible expansion B. Free expansion C. Irreversible Compression D. Cyclic reversible. List-II (Expression): I. q = 0 II. q = nRT ln\\f{V_{2}}{V_{1}} III. w = −p_{ext}(V_{1} − V_{2}) IV. \\f{q_{rev}}{T} = 0. Choose the correct answer from the options given below :',
    ['A-II, B-III, C-I, D-IV', 'A-II, B-I, C-IV, D-III', 'A-II, B-I, C-III, D-IV', 'A-I, B-II, C-III, D-IV'], 3, lambda: 3,
    ['Reversible isothermal expansion: q = −w = nRT ln\\f{V_{2}}{V_{1}} (II). Free expansion: w = 0, ΔU = 0 → q = 0 (I).', 'Irreversible compression: w = −p_{ext}(V_{2} − V_{1}) = p_{ext}(V_{1} − V_{2}); List-II writes it the other way round — still the one irreversible-work entry (III). Cyclic reversible: ΔS = Σ\\f{q_{rev}}{T} = 0 (IV).'], 'law', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'law', '20.0 dm^{3} of an ideal gas \'X\' at 600 K and 0.5 MPa undergoes isothermal reversible expansion until pressure of the gas is 0.2 MPa. Which of the following option is correct? (Given: log 2 = 0.3010 and log 5 = 0.6989)',
    ['w = −9.1 kJ, ΔU = 0, ΔH = 0, q = 9.1 kJ', 'w = 9.1 J, ΔU = 9.1 J, ΔH = 0; q = 0', 'w = +4.1 kJ, ΔU = 0, ΔH = 0; q = −4.1 kJ', 'w = −3.9 kJ, ΔU = 0, ΔH = 0; q = 3.9 kJ'], 1,
    lambda: near([-9.1, 9.1, 4.1, -3.9], -0.5e6 * 0.020 * math.log(0.5 / 0.2) / 1000),
    ['w = −nRT ln\\f{p_{1}}{p_{2}} = −p_{1}V_{1} ln 2.5 = −(0.5 × 10^{6})(0.020)(0.916) ≈ −9.16 kJ.', 'Isothermal ideal gas: ΔU = ΔH = 0, q = −w ≈ +9.1 kJ.'], 'law', 2)

# ---------------- Hess's law, formation, combustion ----------------
add(('2024', 'Apr', '2024-04-05', 2), 'hess', 'Combustion of 1 mole of benzene is expressed as C_{6}H_{6}(l) + \\f{15}{2}O_{2}(g) → 6CO_{2}(g) + 3H_{2}O(l). The standard enthalpy of combustion of 2 mol of benzene is −\'x\' kJ. x = ____. (1) Standard enthalpy of formation of 1 mol of C_{6}H_{6}(l), for the reaction 6C(graphite) + 3H_{2}(g) → C_{6}H_{6}(l) is 48.5 kJ mol^{−1}. (2) Standard enthalpy of formation of 1 mol of CO_{2}(g) is −393.5 kJ mol^{−1}. (3) Standard enthalpy of formation of 1 mol of H_{2}O(l) is −286 kJ mol^{−1}.',
    None, 6535, lambda: round(-2 * (6 * -393.5 + 3 * -286 - 48.5)), ['Δ_{c}H = 6(−393.5) + 3(−286) − 48.5 = −3267.5 kJ per mol.', 'For 2 mol: −6535 kJ → x = 6535.'], 'hess', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'hess', 'The hydration energies of K^{+} and Cl^{−} are −x and −y kJ/mol respectively. If lattice energy of KCl is −z kJ/mol, then the heat of solution of KCl is :',
    ['z − (x + y)', 'x + y + z', '−z − (x + y)', '+x − y − z'], 1, lambda: (lambda x, y, z: near([z - (x + y), x + y + z, -z - (x + y), x - y - z], z + (-x - y)))(322.0, 363.0, 701.0),
    ['Dissolving = break the lattice (+z, the reverse of forming it) + hydrate the ions (−x − y).', 'Δ_{sol}H = z − (x + y).'], 'hess', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'hess', 'The heat of solution of anhydrous CuSO_{4} and CuSO_{4}·5H_{2}O are −70 kJ mol^{−1} and +12 kJ mol^{−1} respectively. The heat of hydration of CuSO_{4} to CuSO_{4}·5H_{2}O is −x kJ. The value of x is ____.',
    None, 82, lambda: round(-(-70 - 12)), ['CuSO_{4} → solution (−70) = CuSO_{4} → CuSO_{4}·5H_{2}O (ΔH_{hyd}) + CuSO_{4}·5H_{2}O → solution (+12).', 'ΔH_{hyd} = −70 − 12 = −82 kJ → x = 82.'], 'hess', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'hess', 'Consider the following data. (i) 2Al(s) + 6HCl(aq) → Al_{2}Cl_{6}(aq) + 3H_{2}(g) + 1200 kJ/mol (ii) H_{2}(g) + Cl_{2}(g) → 2HCl(g) + 164 kJ/mol (iii) HCl(g) + aq → HCl(aq) + 83 kJ/mol (iv) Al_{2}Cl_{6}(s) + aq → Al_{2}Cl_{6}(aq) + 663 kJ/mol. The enthalpy of formation of anhydrous solid Al_{2}Cl_{6} is :',
    ['−648 kJ mol^{−1}', '−1350 kJ mol^{−1}', '−2002 kJ mol^{−1}', '−1527 kJ mol^{−1}'], 4, lambda: pick([-648, -1350, -2002, -1527], -1200 + 3 * -164 + 6 * -83 - (-663)),
    ['Target: 2Al + 3Cl_{2} → Al_{2}Cl_{6}(s) = (i) + 3(ii) + 6(iii) − (iv).', 'ΔH = −1200 − 492 − 498 + 663 = −1527 kJ mol^{−1}.'], 'hess', 3)
add(('2025', 'Jan', '2025-01-22', 2), 'hess', 'Consider the following cases of standard enthalpy of reaction (ΔH°_{r} in kJ mol^{−1}): C_{2}H_{6}(g) + \\f{7}{2}O_{2}(g) → 2CO_{2}(g) + 3H_{2}O(l), ΔH°_{1} = −1550; C(graphite) + O_{2}(g) → CO_{2}(g), ΔH°_{2} = −393.5; H_{2}(g) + \\f{1}{2}O_{2}(g) → H_{2}O(l), ΔH°_{3} = −286. The magnitude of ΔH°_{f}(C_{2}H_{6}, g) is ____ kJ mol^{−1} (Nearest integer).',
    None, 95, lambda: round(abs(2 * -393.5 + 3 * -286 + 1550)), ['ΔH_{f} = 2ΔH_{2} + 3ΔH_{3} − ΔH_{1} = −787 − 858 + 1550 = −95 kJ mol^{−1} → 95.'], 'hess', 1)
add(('2025', 'Jan', '2025-01-24', 2), 'hess', 'S(g) + \\f{3}{2}O_{2}(g) → SO_{3}(g) + 2x kcal; SO_{2}(g) + \\f{1}{2}O_{2}(g) → SO_{3}(g) + y kcal. The heat of formation of SO_{2}(g) is given by :',
    ['2x + y kcal', 'y − 2x kcal', '\\f{2x}{y} kcal', 'x + y kcal'], 2, lambda: (lambda x, y: near([2 * x + y, y - 2 * x, 2 * x / y, x + y], -2 * x - (-y)))(47.0, 23.0),
    ['"+ heat" on the right means ΔH is negative: ΔH_{1} = −2x, ΔH_{2} = −y.', 'S + O_{2} → SO_{2} = (1) − (2): ΔH = −2x + y = y − 2x kcal.'], 'hess', 2)
add(('2025', 'Jan', '2025-01-28', 2), 'hess', 'Consider the following data : Heat of formation of CO_{2}(g) = −393.5 kJ mol^{−1}, Heat of formation of H_{2}O(l) = −286.0 kJ mol^{−1}, Heat of combustion of benzene = −3267.0 kJ mol^{−1}. The heat of formation of benzene is ____ kJ mol^{−1}. (Nearest integer)',
    None, 48, lambda: round(6 * -393.5 + 3 * -286.0 + 3267.0), ['Δ_{f}H = 6(−393.5) + 3(−286) − (−3267) = −2361 − 858 + 3267 = 48 kJ mol^{−1}.'], 'hess', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'hess', 'Two reactions are given below: 2Fe(s) + \\f{3}{2}O_{2}(g) → Fe_{2}O_{3}(s), ΔH° = −822 kJ/mol; C(s) + \\f{1}{2}O_{2}(g) → CO(g), ΔH° = −110 kJ/mol. Then enthalpy change for following reaction 3C(s) + Fe_{2}O_{3}(s) → 2Fe(s) + 3CO(g) is ____.',
    None, 492, lambda: round(3 * -110 - (-822)), ['Target = 3 × (2) − (1): ΔH = 3(−110) + 822 = +492 kJ.'], 'hess', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'hess', 'If 3.365 g of ethanol (l) is burnt completely in a bomb calorimeter at 298.15 K, the heat produced is 99.472 kJ. The |ΔH°_{f}| of ethanol at 298.15 K is ____ × 10^{2} kJ mol^{−1}. (Nearest integer) Given: Standard enthalpy for combustion of graphite = −393.5 kJ mol^{−1}; Standard enthalpy of formation of water (l) = −285.8 kJ mol^{−1}; Molar mass in g mol^{−1} of C, H, O are 12, 1 and 16 respectively',
    None, 3, lambda: (lambda dU: round(abs(2 * -393.5 + 3 * -285.8 - (dU + (2 - 3) * R * 298.15 / 1000)) / 100))(-99.472 / (3.365 / 46)),
    ['n = \\f{3.365}{46} = 0.0732 mol → Δ_{c}U = −1360 kJ mol^{−1}.', 'C_{2}H_{5}OH(l) + 3O_{2} → 2CO_{2} + 3H_{2}O(l): Δn_{g} = −1 → Δ_{c}H = −1360 − 2.5 = −1362 kJ.', 'Δ_{f}H = 2(−393.5) + 3(−285.8) + 1362 ≈ −282 kJ → 2.82 × 10^{2} → 3.'], 'hess', 3)
add(('2026', 'Apr', '2026-04-08', 2), 'hess', 'Consider the reaction 2H_{2}S(g) + 3O_{2}(g) → 2H_{2}O(l) + 2SO_{2}(g). The magnitude of enthalpy change for the reaction in kJ mol^{−1} is ____. (Nearest integer) Given: Δ_{f}H°(H_{2}S) = −20.1 kJ mol^{−1}, Δ_{f}H°(H_{2}O) = −286.0 kJ mol^{−1}, Δ_{f}H°(SO_{2}) = −297.0 kJ mol^{−1}',
    None, 1126, lambda: round(abs(2 * -286.0 + 2 * -297.0 - 2 * -20.1)), ['ΔH = ΣΔ_{f}H(products) − ΣΔ_{f}H(reactants) = −572 − 594 + 40.2 = −1125.8 → 1126.'], 'hess', 1)

# ---------------- bond enthalpy, Born–Haber ----------------
add(('2024', 'Apr', '2024-04-04', 1), 'bond', 'The magnitude of enthalpy of formation of ethane (C_{2}H_{6}) from ethylene by addition of hydrogen where the bond energies of C−H, C−C, C=C, H−H are 414 kJ, 347 kJ, 615 kJ and 435 kJ respectively is ____ kJ.',
    None, 125, lambda: round(abs((615 + 435) - (347 + 2 * 414))), ['Break C=C + H−H = 615 + 435 = 1050; form C−C + 2 C−H = 347 + 828 = 1175.', 'ΔH = 1050 − 1175 = −125 kJ → 125.'], 'bond', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'bond', 'Consider the following data: Δ_{f}H°(methane, g) = −X kJ mol^{−1}; Enthalpy of sublimation of graphite = Y kJ mol^{−1}; Dissociation enthalpy of H_{2} = Z kJ mol^{−1}. The bond enthalpy of C−H bond is given by :',
    ['\\f{X + Y + 2Z}{4}', '\\f{X + Y + 4Z}{2}', 'X + Y + Z', '\\f{−X + Y + Z}{4}'], 1, lambda: (lambda X, Y, Z: near([(X + Y + 2 * Z) / 4, (X + Y + 4 * Z) / 2, X + Y + Z, (-X + Y + Z) / 4], (Y + 2 * Z - (-X)) / 4))(75.0, 717.0, 436.0),
    ['C(s) + 2H_{2} → CH_{4}: −X = Y + 2Z − 4ε_{C−H}.', 'ε_{C−H} = \\f{X + Y + 2Z}{4}.'], 'bond', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'bond', 'The bond dissociation enthalpy of X_{2} ΔH°_{bond} calculated from the given data is ____ kJ mol^{−1}. (Nearest integer) M^{+}X^{−}(s) → M^{+}(g) + X^{−}(g), ΔH°_{lattice} = 800 kJ mol^{−1}; M(s) → M(g), ΔH°_{sub} = 100 kJ mol^{−1}; M(g) → M^{+}(g) + e^{−}(g), ΔH°_{i} = 500 kJ mol^{−1}; X(g) + e^{−}(g) → X^{−}(g), ΔH°_{eg} = −300 kJ mol^{−1}; M(s) + \\f{1}{2}X_{2}(g) → M^{+}X^{−}(s), ΔH°_{f} = −400 kJ mol^{−1} [Given : M^{+}X^{−} is a pure ionic compound and X forms a diatomic molecule X_{2} in gaseous state]',
    None, 200, lambda: round(2 * (-400 - 100 - 500 + 300 + 800)), ['Born–Haber: ΔH_{f} = sub + IE + ½D + EG − lattice.', '−400 = 100 + 500 + ½D − 300 − 800 → ½D = 100 → D = 200 kJ mol^{−1}.'], 'bond', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'bond', 'The formation enthalpies, ΔH°_{f} for H(g) and O(g) are 220.0 and 250.0 kJ mol^{−1}, respectively, at 298.15 K, and ΔH°_{f} for H_{2}O(g) is −242.0 kJ mol^{−1} at the same temperature. The average bond enthalpy of the O−H bond in water at 298.15 K is ____ kJ mol^{−1} (nearest integer).',
    None, 466, lambda: round((2 * 220.0 + 250.0 - (-242.0)) / 2), ['H_{2}O(g) → 2H(g) + O(g): ΔH = 2(220) + 250 + 242 = 932 kJ.', 'Two O−H bonds → 466 kJ mol^{−1}.'], 'bond', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'bond', 'If the enthalpy of sublimation of Li is 155 kJ mol^{−1}, enthalpy of dissociation of F_{2} is 150 kJ mol^{−1}, ionization enthalpy of Li is 520 kJ mol^{−1}, electron gain enthalpy of F is −313 kJ mol^{−1}, standard enthalpy of formation of LiF is −594 kJ mol^{−1}. The magnitude of lattice enthalpy of LiF is ____ kJ mol^{−1}. (Nearest Integer)',
    None, 1031, lambda: round(155 + 150 / 2 + 520 - 313 - (-594)), ['Lattice (LiF → ions) = sub + ½D + IE + EG − ΔH_{f}.', '= 155 + 75 + 520 − 313 + 594 = 1031 kJ mol^{−1}.'], 'bond', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'bond', 'The heat of atomisation of methane and ethane are \'x\' kJ mol^{−1} and \'y\' kJ mol^{−1} respectively. The longest wavelength (λ) of light capable of breaking the C−C bond can be expressed in SI unit as:',
    ['\\f{hc}{1000}(\\f{y − 6x}{4})^{−1}', '\\f{N_{A}hc}{250(4y − 6x)}', '\\f{N_{A}hc}{250(y − 6x)}', 'N_{A}hc(y − \\f{6x}{4})^{−1}'], 2,
    lambda: (lambda x, y, NA, hc: near([hc / 1000 / ((y - 6 * x) / 4), NA * hc / (250 * (4 * y - 6 * x)), NA * hc / (250 * (y - 6 * x)), NA * hc / (y - 6 * x / 4)], NA * hc / ((y - 6 * x / 4) * 1000)))(1660.0, 2826.0, 6.022e23, 1.986e-25),
    ['C−H = \\f{x}{4}; ethane: C−C + 6\\f{x}{4} = y → C−C = y − \\f{3x}{2} kJ mol^{−1}.', 'Per bond: E = \\f{1000(y − 1.5x)}{N_{A}} J = \\f{hc}{λ} → λ = \\f{N_{A}hc}{1000(y − 1.5x)} = \\f{N_{A}hc}{250(4y − 6x)}.'], 'bond', 3)

# ---------------- entropy, Gibbs energy, spontaneity ----------------
add(('2025', 'Apr', '2025-04-04', 1), 'spont', 'Let us consider a reversible reaction at temperature, T. In this reaction, both ΔH and ΔS were observed to have positive values. If the equilibrium temperature is Te, then the reaction becomes spontaneous at:',
    ['T > Te', 'Te = 5T', 'Te > T', 'T = Te'], 1, lambda: 1, ['ΔG = ΔH − TΔS = 0 at Te = \\f{ΔH}{ΔS}; with both positive, ΔG < 0 when T > Te.'], 'spont', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'spont', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A): Enthalpy of neutralisation of strong monobasic acid with strong monoacidic base is always −57 kJ mol^{−1}. Reason (R): Enthalpy of neutralisation is the amount of heat liberated when one mole of H^{+} ions furnished by acid combine with one mole of ^{−}OH ions furnished by base to form one mole of water. In the light of the above statements, choose the correct answer from the options given below.',
    ['(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)'], 2, lambda: 2,
    ['Strong acid + strong base are fully ionised, so the only reaction is H^{+} + OH^{−} → H_{2}O, about −57 kJ every time — R explains A.'], 'law', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'spont', 'For the reaction at 298 K, 2A + B → C. ΔH = 400 kJ mol^{−1} and ΔS = 0.2 kJ mol^{−1} K^{−1}. The reaction will become spontaneous above ____ K.',
    None, 2000, lambda: round(400 / 0.2), ['ΔG < 0 when T > \\f{ΔH}{ΔS} = \\f{400}{0.2} = 2000 K.'], 'spont', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'spont', 'When ΔH_{vap} = 30 kJ/mol and ΔS_{vap} = 75 J mol^{−1} K^{−1}, then the temperature of vapour, at one atmosphere is ____ K.',
    None, 400, lambda: round(30000 / 75), ['At the boiling point ΔG = 0: T = \\f{30 000}{75} = 400 K.'], 'spont', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'spont', 'Ice at −5 °C is heated to become vapor with temperature of 110 °C at atmospheric pressure. The entropy change associated with this process can be obtained from',
    ['∫_{268K}^{383K} C_{p}dT + \\f{ΔH_{melting}}{273} + \\f{ΔH_{boiling}}{373}', '∫_{268K}^{273K} \\f{C_{p,m}}{T}dT + \\f{ΔH_{m,fusion}}{T_{f}} + \\f{ΔH_{m,vaporisation}}{T_{b}} + ∫_{273K}^{373K} \\f{C_{p,m}dT}{T} + ∫_{373K}^{383K} \\f{C_{p,m}dT}{T}',
     '∫_{268K}^{383K} C_{p}dT + \\f{q_{rev}}{T}', '∫_{268K}^{273K} C_{p,m}dT + \\f{ΔH_{m,fusion}}{T_{f}} + \\f{ΔH_{m,vaporisation}}{T_{b}} + ∫_{273K}^{373K} C_{p,m}dT + ∫_{373K}^{383K} C_{p,m}dT'], 2, lambda: 2,
    ['Heating: ΔS = ∫\\f{C_{p}}{T}dT for each phase (ice, water, steam). Phase change: ΔS = \\f{ΔH}{T} at that temperature.', 'Only (2) divides every heating step by T; (1) and (4) give enthalpy, not entropy.'], 'spont', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'spont', 'The standard enthalpy and standard entropy of decomposition of N_{2}O_{4} to NO_{2} are 55.0 kJ mol^{−1} and 175.0 J/K/mol respectively. The standard free energy change for this reaction at 25 °C in J mol^{−1} is ____. (Nearest integer)',
    None, 2850, lambda: round(55000 - 298 * 175.0), ['ΔG° = ΔH° − TΔS° = 55 000 − 298 × 175 = 2850 J mol^{−1}.'], 'spont', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'spont', 'The effect of temperature on spontaneity of reactions are represented as : (A) ΔH +, ΔS −, any T, Non spontaneous; (B) ΔH +, ΔS +, low T, spontaneous; (C) ΔH −, ΔS −, low T, Non spontaneous; (D) ΔH −, ΔS +, any T, spontaneous. The incorrect combinations are:',
    ['(A) and (D) only', '(A) and (C) only', '(B) and (D) only', '(B) and (C) only'], 4,
    lambda: (lambda claims: pick(['AD', 'AC', 'BD', 'BC'], ''.join(k for k, (h, sS, Ts, sp) in claims.items() if any(((h * 50 - T * sS * 0.1) < 0) != sp for T in Ts))))(
        dict(A=(1, -1, (100, 1000), False), B=(1, 1, (100,), True), C=(-1, -1, (100,), False), D=(-1, 1, (100, 1000), True))),   # ΔH ±50 kJ, ΔS ±0.1 kJ/K
    ['ΔG = ΔH − TΔS.', '(B) +, +: spontaneous only at HIGH T ✗. (C) −, −: spontaneous at LOW T ✗. (A) and (D) are right.'], 'spont', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'spont', 'Let us consider an endothermic reaction which is non-spontaneous at the freezing point of water. However, the reaction is spontaneous at boiling point of water. Choose the correct option.',
    ['Both ΔH and ΔS are (−ve)', 'ΔH is (−ve) but ΔS is (+ve)', 'Both ΔH and ΔS are (+ve)', 'ΔH is (+ve) but ΔS is (−ve)'], 3, lambda: 3,
    ['Endothermic → ΔH > 0. Spontaneous only at higher T means −TΔS must win as T rises → ΔS > 0.'], 'spont', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'spont', 'Standard entropies of X_{2}, Y_{2} and XY_{5} are 70, 50 and 110 J K^{−1} mol^{−1} respectively. The temperature in Kelvin at which the reaction \\f{1}{2}X_{2} + \\f{5}{2}Y_{2} ⇌ XY_{5}, ΔH° = −35 kJ mol^{−1} will be at equilibrium is ____ (Nearest integer)',
    None, 700, lambda: round(-35000 / (110 - 35 - 125)), ['ΔS° = 110 − ½(70) − \\f{5}{2}(50) = −50 J K^{−1}.', 'T = \\f{ΔH°}{ΔS°} = \\f{−35 000}{−50} = 700 K.'], 'spont', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'spont', 'Which of the following is not correct ?',
    ['ΔG is negative for a spontaneous reaction', 'ΔG is positive for a spontaneous reaction', 'ΔG is zero for a reversible reaction', 'ΔG is positive for a non-spontaneous reaction'], 2, lambda: 2, ['Spontaneous ⇔ ΔG < 0; equilibrium (reversible) ⇔ ΔG = 0.'], 'spont', 1)
for _p in P: _p['t'] = _p['fam']
