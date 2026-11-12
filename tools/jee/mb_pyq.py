"""Real JEE Main questions — Chemistry Unit 1: Some Basic Concepts in Chemistry (mole concept). Our own solutions; chk re-solves each.
Skipped on purpose: 9-Apr-2024 morning Q26 (CuSO4 molality: stated data give 164, official key 81)."""
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
M = dict(H=1, C=12, N=14, O=16, Na=23, Mg=24, Al=27, S=32, Cl=35.5, Ca=40, Fe=56, Zn=65, Ag=108, Cu=63.5, He=4, Ar=40, Ba=137)
def mm(f):   # molar mass from a dict formula
    return sum(M[e] * k for e, k in f.items())
NA = 6.022e23
ST = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
def molal(Mv, d, Ms): return Mv * 1000 / (1000 * d - Mv * Ms)

# ---------- mole, atoms & molar mass ----------
add(('2025', 'Apr', '2025-04-03', 1), 'mole', 'Among 10^{−9} g (each) of the following elements, which one will have the highest number of atoms? Element: Pb, Po, Pr and Pt',
    ['Po', 'Pt', 'Pr', 'Pb'], 3, lambda: pick(['Po', 'Pt', 'Pr', 'Pb'], min({'Po': 209, 'Pt': 195, 'Pr': 141, 'Pb': 207}.items(), key=lambda x: x[1])[0]),
    ['Equal masses: number of atoms ∝ \\f{1}{atomic mass}.', 'Pr (141) is the lightest of Pr 141, Pt 195, Pb 207, Po 209 → most atoms.'], 'mole', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'mole', 'Number of moles and number of molecules in 1.4187 L of SO_{2} at STP respectively are',
    ['0.1266 ; 3.812 × 10^{22}', '0.0633 ; 3.812 × 10^{22}', '0.1266 ; 7.6238 × 10^{22}', '0.0633 ; 7.6238 × 10^{22}'], 2,
    lambda: near([0.1266 + 3.812, 0.0633 + 3.812, 0.1266 + 7.6238, 0.0633 + 7.6238], 1.4187 / 22.4 + 1.4187 / 22.4 * NA / 1e22),
    ['n = \\f{1.4187}{22.4} = 0.0633 mol.', 'Molecules = 0.0633 × 6.022 × 10^{23} = 3.812 × 10^{22}.'], 'mole', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'mole', 'The correct order of total number of atoms present in (A) 2 moles of cyclohexane (B) 684 g of sucrose (C) 90.8 L of dihydrogen at STP is :',
    ['C > A > B', 'C > B > A', 'B > C > A', 'B > A > C'], 4,
    lambda: pick(['C > A > B', 'C > B > A', 'B > C > A', 'B > A > C'], ' > '.join(sorted('ABC', key=lambda k: -{'A': 2 * 18, 'B': 684 / 342 * 45, 'C': 90.8 / 22.7 * 2}[k]))),
    ['A: C_{6}H_{12} has 18 atoms → 2 × 18 = 36 mol of atoms.', 'B: C_{12}H_{22}O_{11} (342 g/mol), 684 g = 2 mol × 45 atoms = 90 mol of atoms.', 'C: 90.8 L ÷ 22.7 L = 4 mol H_{2} → 8 mol of atoms.', 'B > A > C.'], 'mole', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'mole', 'Which of the following contain the same number of atoms? (Given : Molar mass in g mol^{−1} of H, He, O and S are 1, 4, 16 and 32 respectively) A. 2 g of O_{2} gas B. 4 g of SO_{2} gas C. 1400 mL of O_{2} at STP D. 0.05 L of He at STP E. 0.0625 mol of H_{2} gas',
    ['A and B only', 'B and C only', 'C and D only', 'A, C and E only'], 4,
    lambda: (lambda a: pick(['A and B only', 'B and C only', 'C and D only', 'A, C and E only'], {'AB': 'A and B only', 'BC': 'B and C only', 'CD': 'C and D only', 'ACE': 'A, C and E only'}.get(''.join(k for k in 'ABCDE' if abs(a[k] - 0.125) < 1e-9), '?')))(
        dict(A=2 / 32 * 2, B=4 / 64 * 3, C=1.4 / 22.4 * 2, D=0.05 / 22.4, E=0.0625 * 2)),
    ['A: \\f{2}{32} × 2 = 0.125 mol atoms. B: \\f{4}{64} × 3 = 0.1875. C: \\f{1.4}{22.4} × 2 = 0.125.', 'D: \\f{0.05}{22.4} = 0.0022. E: 0.0625 × 2 = 0.125.', 'A, C and E have the same number of atoms.'], 'mole', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'mole', 'Match List-I (mass of substance) with List-II (number of atoms). A. 1.8 mg water B. 9.8 mg sulphuric acid C. 1.8 mg carbon D. 5.85 mg salt (NaCl) — I. 2 × 10^{−4} × N_{A} II. 1.5 × 10^{−4} × N_{A} III. 3 × 10^{−4} × N_{A} IV. 7 × 10^{−4} × N_{A}',
    ['A-IV, B-III, C-I, D-II', 'A-III, B-II, C-IV, D-I', 'A-III, B-IV, C-II, D-I', 'A-III, B-IV, C-I, D-II'], 3,
    lambda: (lambda v: pick(['A-IV, B-III, C-I, D-II', 'A-III, B-II, C-IV, D-I', 'A-III, B-IV, C-II, D-I', 'A-III, B-IV, C-I, D-II'], ', '.join(f'{k}-{ {2: "I", 1.5: "II", 3: "III", 7: "IV"}[round(v[k] * 1e4, 6)] }' for k in 'ABCD')))(
        dict(A=1.8e-3 / 18 * 3, B=9.8e-3 / 98 * 7, C=1.8e-3 / 12, D=5.85e-3 / 58.5 * 2)),
    ['A: 1.8 mg H_{2}O = 10^{−4} mol × 3 atoms = 3 × 10^{−4}N_{A} (III).', 'B: 9.8 mg H_{2}SO_{4} = 10^{−4} mol × 7 = 7 × 10^{−4}N_{A} (IV).', 'C: 1.8 mg C = 1.5 × 10^{−4} mol (II).', 'D: 5.85 mg NaCl = 10^{−4} mol × 2 = 2 × 10^{−4}N_{A} (I).'], 'mole', 2)
add(('2024', 'Jan', '2024-01-31', 1), 'mole', 'Number of moles of methane required to produce 22 g CO_{2}(g) after combustion is x × 10^{−2} moles. The value of x is ______.', None, 50, lambda: round(22 / 44 * 100),
    ['CH_{4} + 2O_{2} → CO_{2} + 2H_{2}O: 1 mol CH_{4} gives 1 mol CO_{2}.', '22 g CO_{2} = 0.5 mol → 0.5 mol CH_{4} = 50 × 10^{−2}.'], 'stoich', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'mole', 'The number of moles of methane required to produce 11 g CO_{2}(g) after complete combustion is: (Given molar mass of methane in g mol^{−1}: 16)',
    ['0.75', '0.25', '0.35', '0.5'], 2, lambda: pick([0.75, 0.25, 0.35, 0.5], 11 / 44), ['One CH_{4} gives one CO_{2}.', '11 g CO_{2} = \\f{11}{44} = 0.25 mol → 0.25 mol CH_{4}.'], 'stoich', 1)

# ---------- concentration terms ----------
add(('2024', 'Apr', '2024-04-04', 1), 'conc', 'The Molarity (M) of an aqueous solution containing 5.85 g of NaCl in 500 mL water is : (Given : Molar Mass Na: 23 and Cl: 35.5 g mol^{−1})',
    ['20', '0.2', '2', '4'], 2, lambda: pick([20, 0.2, 2, 4], round(5.85 / 58.5 / 0.5, 6)), ['n = \\f{5.85}{58.5} = 0.1 mol.', 'M = \\f{0.1}{0.5 L} = 0.2 M (taking the solution volume as 500 mL).'], 'conc', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'conc', 'Molality (m) of 3M aqueous solution of NaCl is: (Given : Density of solution = 1.25 g mL^{−1}, Molar mass in g mol^{−1}: Na − 23, Cl − 35.5)',
    ['2.90 m', '2.79 m', '1.90 m', '3.85 m'], 2, lambda: near([2.90, 2.79, 1.90, 3.85], molal(3, 1.25, 58.5)),
    ['Take 1 L: mass = 1250 g; NaCl = 3 × 58.5 = 175.5 g.', 'Water = 1074.5 g → m = \\f{3}{1.0745} = 2.79 m.'], 'conc', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'conc', 'Density of 3 M NaCl solution is 1.25 g/mL. The molality of the solution is :',
    ['1.79 m', '3 m', '2.79 m', '2 m'], 3, lambda: near([1.79, 3, 2.79, 2], molal(3, 1.25, 58.5)),
    ['1 L of solution = 1250 g, of which NaCl = 175.5 g.', 'Water = 1074.5 g → \\f{3}{1.0745} = 2.79 m.'], 'conc', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'conc', "The density of 'x' M solution ('x' molar) of NaOH is 1.12 g mL^{−1}, while in molality, the concentration of the solution is 3 m (3 molal). Then x is (Given : Molar mass of NaOH is 40 g/mol)",
    ['3.5', '3.0', '3.8', '2.8'], 2, lambda: near([3.5, 3.0, 3.8, 2.8], 3 * 1120 / (1000 + 3 * 40)),
    ['m = \\f{1000M}{1000d − M × M_{solute}} → 3 = \\f{1000x}{1120 − 40x}.', '3360 − 120x = 1000x → x = 3.0.'], 'conc', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'conc', 'Molality of an aqueous solution of urea is 4.44 m. Mole fraction of urea in solution is x × 10^{−3}. Value of x is ______ (integer answer)',
    None, 74, lambda: round(4.44 / (4.44 + 1000 / 18) * 1000), ['4.44 mol urea per 1000 g water = 55.56 mol water.', 'x = \\f{4.44}{4.44 + 55.56} = 0.074 = 74 × 10^{−3}.'], 'conc', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'conc', 'A solution is prepared by adding 1 mole ethyl alcohol in 9 mole water. The mass percent of solute in the solution is ______ (Integer Answer) (Given : Molar mass in g mol^{−1} Ethyl alcohol : 46, water : 18)',
    None, 22, lambda: round(46 / (46 + 9 * 18) * 100), ['Mass of solute = 46 g; water = 9 × 18 = 162 g.', 'Mass % = \\f{46}{208} × 100 = 22.1 ≈ 22.'], 'conc', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'conc', 'The molarity of a 70% (mass/mass) aqueous solution of a monobasic acid (X) is ______ × 10^{−1} M (Nearest integer) [Given: Density of aqueous solution of (X) is 1.25 g mL^{−1}; Molar mass of the acid is 70 g mol^{−1}]',
    None, 125, lambda: round(1250 * 0.7 / 70 * 10), ['1 L = 1250 g of solution → acid = 875 g = \\f{875}{70} = 12.5 mol.', 'M = 12.5 = 125 × 10^{−1}.'], 'conc', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'conc', 'Concentrated nitric acid is labelled as 75% by mass. The volume in mL of the solution which contains 30 g of nitric acid is (Given : Density of nitric acid solution is 1.25 g/mL)',
    ['45', '40', '55', '32'], 4, lambda: pick([45, 40, 55, 32], round(30 / 0.75 / 1.25, 6)), ['Mass of solution = \\f{30}{0.75} = 40 g.', 'Volume = \\f{40}{1.25} = 32 mL.'], 'conc', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'conc', 'A solution of H_{2}SO_{4} is 31.4% H_{2}SO_{4} by mass and has a density of 1.25 g/mL. The molarity of the H_{2}SO_{4} solution is ______ M (nearest integer) [Given molar mass of H_{2}SO_{4} = 98 g mol^{−1}]',
    None, 4, lambda: round(1250 * 0.314 / 98), ['M = \\f{10 × d × %}{M_{solute}} = \\f{10 × 1.25 × 31.4}{98} = 4.0 M.'], 'conc', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'conc', 'Molality of 0.8 M H_{2}SO_{4} solution (density 1.06 g cm^{−3}) is ______ × 10^{−3} m.', None, 815, lambda: round(molal(0.8, 1.06, 98) * 1000),
    ['1 L = 1060 g; H_{2}SO_{4} = 0.8 × 98 = 78.4 g.', 'Water = 981.6 g → m = \\f{0.8}{0.9816} = 0.815 = 815 × 10^{−3} m.'], 'conc', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'conc', 'The molarity of 1 L orthophosphoric acid (H_{3}PO_{4}) having 70% purity by weight (specific gravity 1.54 g cm^{−3}) is ______ M. (Molar mass of H_{3}PO_{4} = 98 g mol^{−1})',
    None, 11, lambda: round(1540 * 0.7 / 98), ['Mass of 1 L = 1540 g; H_{3}PO_{4} = 0.7 × 1540 = 1078 g.', 'M = \\f{1078}{98} = 11 M.'], 'conc', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'conc', 'The mass of sodium acetate (CH_{3}COONa) required to prepare 250 mL of 0.35 M aqueous solution is ______ g. (Molar mass of CH_{3}COONa is 82.02 g mol^{−1}) (nearest integer)',
    None, 7, lambda: round(0.25 * 0.35 * 82.02), ['n = 0.35 × 0.25 = 0.0875 mol.', 'Mass = 0.0875 × 82.02 = 7.18 ≈ 7 g.'], 'conc', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'conc', 'At T(K), 100 g of 98% H_{2}SO_{4} (w/w) aqueous solution is mixed with 100 g of 49% H_{2}SO_{4} (w/w) aqueous solution. What is the mole fraction of H_{2}SO_{4} in the resultant solution? (Given : Atomic mass H = 1 u; S = 32 u; O = 16 u)',
    ['0.663', '0.9', '0.337', '0.1'], 3, lambda: near([0.663, 0.9, 0.337, 0.1], (147 / 98) / (147 / 98 + 53 / 18)),
    ['H_{2}SO_{4} = 98 + 49 = 147 g = 1.5 mol; water = 2 + 51 = 53 g = 2.944 mol.', 'x = \\f{1.5}{4.444} = 0.337.'], 'conc', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'conc', 'What is the mole fraction of water in 10% by weight (w/w) of aqueous urea solution? [Given: Molar mass of H, O, C and N are 1, 16, 12 and 14 g mol^{−1} respectively.]',
    ['0.825', '0.032', '0.867', '0.967'], 4, lambda: near([0.825, 0.032, 0.867, 0.967], 5 / (5 + 10 / 60)), ['100 g: urea 10 g = 0.167 mol; water 90 g = 5 mol.', 'x_{water} = \\f{5}{5.167} = 0.967.'], 'conc', 1)
add(('2026', 'Apr', '2026-04-08', 2), 'conc', "Given : Molar mass of C, H, O, Cl are 12, 1, 16 and 35.5 g mol^{−1}. Statement I: In 30% (w/w) solution of methanol in CCl_{4} (at T K), the mole fraction of CCl_{4} is equal to 0.33. Statement II: Mixture of methanol and CCl_{4} shows positive deviation from Raoult's law.",
    ST, 1, lambda: 1 if abs((70 / 154) / (70 / 154 + 30 / 32) - 0.33) < 0.005 else 0,
    ['I: 30 g CH_{3}OH = 0.9375 mol; 70 g CCl_{4} = 0.4545 mol → x = \\f{0.4545}{1.392} = 0.327 ≈ 0.33. TRUE.', 'II: methanol molecules lose some hydrogen bonding when mixed with CCl_{4} → positive deviation. TRUE.'], 'conc', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'conc', 'Fortification of food with iron is done using FeSO_{4}·7H_{2}O. The mass in grams of the FeSO_{4}·7H_{2}O required to achieve 12 ppm of iron in 150 kg of wheat is ______ (Nearest integer) [Given: Molar mass of Fe, S and O respectively are 56, 32 and 16 g mol^{−1}]',
    None, 9, lambda: round(12e-6 * 150000 / 56 * (56 + 32 + 64 + 7 * 18)),
    ['Fe needed = 12 × 10^{−6} × 150000 g = 1.8 g.', 'FeSO_{4}·7H_{2}O = 278 g/mol carries 56 g Fe → \\f{1.8 × 278}{56} = 8.94 ≈ 9 g.'], 'conc', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'conc', 'Sea water, which can be considered as a 6 molar (6 M) solution of NaCl, has a density of 2 g mL^{−1}. The concentration of dissolved oxygen (O_{2}) in sea water is 5.8 ppm. Then the concentration of dissolved oxygen (O_{2}) in sea water, is x × 10^{−4} m. (nearest integer)',
    None, 2, lambda: round(5.8e-6 * 2000 / 32 / ((2000 - 6 * 58.5) / 1000) * 1e4),
    ['Take 1 L = 2000 g; NaCl = 351 g → water = 1649 g.', 'O_{2} = 5.8 × 10^{−6} × 2000 = 0.0116 g = 3.63 × 10^{−4} mol.', 'Molality = \\f{3.63 × 10^{−4}}{1.649} = 2.2 × 10^{−4} m → x = 2.'], 'conc', 3)
add(('2025', 'Apr', '2025-04-07', 1), 'conc', 'At the sea level, the dry air mass percentage composition is given as nitrogen gas: 70.0, oxygen gas: 27.0 and argon gas: 3.0. If total pressure is 1.15 atm, then calculate the ratio of following respectively: (i) partial pressure of nitrogen gas to partial pressure of oxygen gas (ii) partial pressure of oxygen gas to partial pressure of argon gas (Given: Molar mass of N, O and Ar are 14, 16 and 40 g mol^{−1} respectively.)',
    ['2.96, 11.2', '2.59, 11.85', '4.26, 19.3', '5.46, 17.8'], 1, lambda: near([2.96 + 11.2, 2.59 + 11.85, 4.26 + 19.3, 5.46 + 17.8], (70 / 28) / (27 / 32) + (27 / 32) / (3 / 40)),
    ['Partial pressures are in the ratio of MOLES (total pressure is not needed).', 'N_{2}: 70/28 = 2.5; O_{2}: 27/32 = 0.844; Ar: 3/40 = 0.075.', 'Ratios: 2.5/0.844 = 2.96 and 0.844/0.075 = 11.25.'], 'conc', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'conc', 'The quantity which changes with temperature is :', ['Molarity', 'Mass percentage', 'Molality', 'Mole fraction'], 1, lambda: 1,
    ['Molarity uses VOLUME of solution, and volume expands with temperature.', 'Mass %, molality and mole fraction use only masses/moles → temperature-independent.'], 'conc', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'conc', '10 mL of 2 M NaOH solution is added to 20 mL of 1 M HCl solution kept in a beaker. Now, 10 mL of this mixture is poured into a volumetric flask of 100 mL containing 2 moles of HCl and made the volume upto the mark with distilled water. The solution in this flask is :',
    ['Neutral solution', '10 M HCl solution', '20 M HCl solution', '0.2 M NaCl solution'], 3, lambda: pick(['Neutral solution', '10 M HCl solution', '20 M HCl solution', '0.2 M NaCl solution'], f'{round(2 / 0.1)} M HCl solution'),
    ['20 mmol NaOH + 20 mmol HCl → exactly neutral NaCl; the 10 mL portion adds no acid.', 'Flask: 2 mol HCl in 100 mL → \\f{2}{0.1} = 20 M HCl.'], 'conc', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'conc', 'x mg of pure HCl was used to make an aqueous solution. 25.0 mL of 0.1 M Ba(OH)_{2} solution is used when the HCl solution was titrated against it. The numerical value of x is ______ × 10^{−1}. (Nearest integer) Given : Molar mass of HCl and Ba(OH)_{2} are 36.5 and 171.0 g mol^{−1} respectively.',
    None, 1825, lambda: round(25 * 0.1 * 2 * 36.5 * 10), ['Ba(OH)_{2} = 2.5 mmol → OH^{−} = 5 mmol → HCl = 5 mmol.', 'Mass = 5 × 36.5 = 182.5 mg = 1825 × 10^{−1} mg.'], 'conc', 1)

# ---------- stoichiometry & limiting reagent ----------
add(('2025', 'Apr', '2025-04-02', 1), 'stoich', 'CaCO_{3}(s) + 2HCl(aq) → CaCl_{2}(aq) + CO_{2}(g) + H_{2}O(l). Consider the above reaction, what mass of CaCl_{2} will be formed if 250 mL of 0.76 M HCl reacts with 1000 g of CaCO_{3}? (Given : Molar mass of Ca, C, O, H and Cl are 40, 12, 16, 1 and 35.5 g mol^{−1}, respectively)',
    ['10.545 g', '3.908 g', '5.272 g', '2.636 g'], 1, lambda: near([10.545, 3.908, 5.272, 2.636], min(0.25 * 0.76 / 2, 1000 / 100) * 111),
    ['HCl = 0.19 mol (limiting; 10 mol CaCO_{3} is a huge excess).', 'CaCl_{2} = 0.095 mol × 111 = 10.545 g.'], 'stoich', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'stoich', 'Mass of magnesium required to produce 220 mL of hydrogen gas at STP on reaction with excess of dil. HCl is (Given: Molar mass of Mg is 24 g mol^{−1})',
    ['2.444 g', '0.24 mg', '236 mg', '235.7 g'], 3, lambda: near([2444, 0.24, 236, 235700], 0.220 / 22.4 * 24 * 1000), ['Mg + 2HCl → MgCl_{2} + H_{2}.', 'H_{2} = \\f{220}{22400} = 9.82 × 10^{−3} mol → Mg = 0.236 g = 236 mg.'], 'stoich', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'stoich', 'Combustion of glucose (C_{6}H_{12}O_{6}) produces CO_{2} and water. The amount of oxygen (in g) required for the complete combustion of 900 g of glucose is: [Molar mass of glucose in g mol^{−1} = 180]',
    ['480', '960', '800', '32'], 2, lambda: pick([480, 960, 800, 32], 900 / 180 * 6 * 32), ['C_{6}H_{12}O_{6} + 6O_{2} → 6CO_{2} + 6H_{2}O.', '900 g = 5 mol → 30 mol O_{2} = 960 g.'], 'stoich', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'stoich', 'Butane reacts with oxygen: C_{4}H_{10}(g) + \\f{13}{2}O_{2}(g) → 4CO_{2}(g) + 5H_{2}O(l). If 174.0 kg of butane is mixed with 320.0 kg of O_{2}, the volume of water formed in liters is ______. (Nearest integer) [Given : (a) Molar mass of C, H, O are 12, 1, 16 g mol^{−1} respectively, (b) Density of water = 1 g mL^{−1}]',
    None, 138, lambda: round(min(174000 / 58 * 5, 320000 / 32 * 5 / 6.5) * 18 / 1000),
    ['Butane = 3000 mol (needs 19500 mol O_{2}); O_{2} = 10000 mol → O_{2} is limiting.', 'Water = 10000 × \\f{5}{6.5} = 7692 mol × 18 = 138.5 kg ≈ 138 L.'], 'stoich', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'stoich', 'The mass of iron converted into Fe_{3}O_{4} by the action of 18 g of steam is : (Given : Molar mass of H, O and Fe are 1, 16 and 56 g mol^{−1} respectively) Assume iron is present in excess :',
    ['2.1 g', '4.2 g', '21 g', '42 g'], 4, lambda: pick([2.1, 4.2, 21, 42], 18 / 18 * 3 / 4 * 56), ['3Fe + 4H_{2}O → Fe_{3}O_{4} + 4H_{2}.', '1 mol steam reacts with \\f{3}{4} mol Fe = 42 g.'], 'stoich', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'stoich', '14.0 g of calcium metal is allowed to react with excess HCl at 1.0 atm pressure and 273 K. Which of the following statements is incorrect? [Given : Molar mass in g mol^{−1} of Ca − 40, Cl − 35.5, H − 1]',
    ['0.35 mol of H_{2} gas is evolved.', '7.84 L of H_{2} gas is evolved.', '33.3 g of CaCl_{2} is produced.', 'The limiting reagent is calcium metal.'], 3,
    lambda: [i + 1 for i, ok in enumerate([abs(14 / 40 - 0.35) < 1e-9, abs(14 / 40 * 22.4 - 7.84) < 1e-9, abs(14 / 40 * 111 - 33.3) < 0.05, True]) if not ok][0],
    ['Ca + 2HCl → CaCl_{2} + H_{2}; Ca = 0.35 mol (limiting, HCl in excess).', 'H_{2} = 0.35 mol = 7.84 L at 273 K, 1 atm.', 'CaCl_{2} = 0.35 × 111 = 38.85 g, NOT 33.3 g → statement 3 is incorrect.'], 'stoich', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'stoich', 'For the given reaction CaCO_{3} + 2HCl → CaCl_{2} + H_{2}O + CO_{2}: if 90 g CaCO_{3} is added to 300 mL of HCl which contains 38.55% HCl by mass and has density 1.13 g mL^{−1}, then which of the following option is correct? (Given molar mass of H, Cl, Ca and O are 1, 35.5, 40 and 16 g mol^{−1} respectively.)',
    ['60.32 g of HCl remains unreacted', '64.97 g of HCl remains unreacted', '32.85 g of CaCO_{3} remains unreacted', '97.30 g of HCl reacted'], 2,
    lambda: near([60.32, 64.97, -1, -1], 300 * 1.13 * 0.3855 - 90 / 100 * 2 * 36.5),
    ['HCl present = 300 × 1.13 × 0.3855 = 130.7 g (3.58 mol).', '90 g CaCO_{3} = 0.9 mol uses 1.8 mol HCl = 65.7 g → CaCO_{3} is limiting.', 'HCl left = 130.7 − 65.7 = 64.97 g.'], 'stoich', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'stoich', 'When 81.0 g of aluminium is allowed to react with 128.0 g of oxygen gas, the mass of aluminium oxide produced in grams is ______ (Nearest integer) Given : Molar mass of Al is 27.0 g mol^{−1}; Molar mass of O is 16.0 g mol^{−1}',
    None, 153, lambda: round(min(81 / 27 / 2, 128 / 32 / 1.5) * 102), ['4Al + 3O_{2} → 2Al_{2}O_{3}. Al = 3 mol (needs 2.25 mol O_{2}); O_{2} = 4 mol → Al limiting.', 'Al_{2}O_{3} = 1.5 mol × 102 = 153 g.'], 'stoich', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'stoich', "Consider the following reaction occurring in the blast furnace: Fe_{3}O_{4}(s) + 4CO(g) → 3Fe(l) + 4CO_{2}(g). 'x' kg of iron is produced when 2.32 × 10^{3} kg Fe_{3}O_{4} and 2.8 × 10^{2} kg CO are brought together in the furnace. The value of 'x' is ______. (nearest integer) {Given: molar mass of Fe_{3}O_{4} = 232, CO = 28, Fe = 56 g mol^{−1}}",
    None, 420, lambda: round(min(2320 / 232 * 3, 280 / 28 * 3 / 4) * 56),
    ['Fe_{3}O_{4} = 10 kmol (needs 40 kmol CO); CO = 10 kmol → CO is limiting.', 'Fe = 10 × \\f{3}{4} = 7.5 kmol × 56 = 420 kg.'], 'stoich', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'stoich', "A + 2B → AB_{2}. 36.0 g of 'A' (Molar mass: 60 g mol^{−1}) and 56.0 g of 'B' (Molar mass: 80 g mol^{−1}) are allowed to react. Which of the following statements are correct? A. 'A' is the limiting reagent. B. 77.0 g of AB_{2} is formed. C. Molar mass of AB_{2} is 140 g mol^{−1}. D. 15.0 g of A is left unreacted after the completion of reaction.",
    ['A and B Only', 'A and C Only', 'B and D Only', 'C and D Only'], 3,
    lambda: pick(['A and B Only', 'A and C Only', 'B and D Only', 'C and D Only'], ' and '.join(k for k, v in dict(A=0.6 < 0.7 / 2, B=abs(0.7 / 2 * 220 - 77) < 1e-9, C=60 + 160 == 140, D=abs((0.6 - 0.35) * 60 - 15) < 1e-9).items() if v) + ' Only'),
    ['A = 0.6 mol, B = 0.7 mol. B is limiting (0.6 mol A would need 1.2 mol B) → A false.', 'AB_{2} = 0.35 mol × 220 = 77.0 g → B true; molar mass is 220, not 140 → C false.', 'A left = 0.25 mol = 15.0 g → D true.'], 'stoich', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'stoich', 'How many grams of residue is obtained by heating 2.76 g of silver carbonate? (Given : Molar mass of C, O and Ag are 12, 16 and 108 g mol^{−1} respectively)',
    ['1.08 g', '2.16 g', '3.24 g', '4.32 g'], 2, lambda: pick([1.08, 2.16, 3.24, 4.32], round(2.76 / 276 * 2 * 108, 6)), ['Ag_{2}CO_{3} → 2Ag + CO_{2} + ½O_{2} (strong heating leaves silver metal).', '2.76 g = 0.01 mol → 0.02 mol Ag = 2.16 g.'], 'stoich', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'stoich', 'What volume of hydrogen gas at STP would be liberated by action of 50 mL of H_{2}SO_{4} of 50% purity (density = 1.3 g mL^{−1}) on 20 g of zinc? Given : Molar mass of H, O, S, Zn are 1, 16, 32, 65 g mol^{−1} respectively.',
    ['5.824 L', '7.428 L', '6.892 L', '8.375 L'], 3, lambda: near([5.824, 7.428, 6.892, 8.375], min(50 * 1.3 * 0.5 / 98, 20 / 65) * 22.4),
    ['H_{2}SO_{4} = 50 × 1.3 × 0.5 = 32.5 g = 0.332 mol; Zn = \\f{20}{65} = 0.308 mol → Zn limiting.', 'H_{2} = 0.308 × 22.4 = 6.892 L.'], 'stoich', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'stoich', 'In the reaction, 2Al(s) + 6HCl(aq) → 2Al^{3+}(aq) + 6Cl^{−}(aq) + 3H_{2}(g)',
    ['11.2 L H_{2}(g) at STP is produced for every mole of HCl consumed.', '67.2 L H_{2}(g) at STP is produced for every mole of Al that reacts.', '12 L HCl(aq) is consumed for every 6 L H_{2}(g) produced.', '33.6 L H_{2}(g) is produced regardless of temperature and pressure for every mole of Al that reacts.'], 1,
    lambda: 1 if abs(3 / 6 * 22.4 - 11.2) < 1e-9 and abs(3 / 2 * 22.4 - 67.2) > 1 else 0,
    ['Per mole HCl: ½ mol H_{2} = 11.2 L at STP ✓.', 'Per mole Al: 1.5 mol H_{2} = 33.6 L at STP (not 67.2 L), and gas volume always depends on T and P.', 'HCl(aq) is a solution — its volume is not fixed by gas laws.'], 'stoich', 1)

# ---------- percentage composition & formula ----------
add(('2025', 'Apr', '2025-04-02', 1), 'formula', 'On complete combustion 1.0 g of an organic compound (X) gave 1.46 g of CO_{2} and 0.567 g of H_{2}O. The empirical formula mass of compound (X) is ______ (Given molar mass in g mol^{−1} C:12, H:1, O:16)',
    ['45', '15', '30', '60'], 3, lambda: (lambda c, h: pick([45, 15, 30, 60], 12 + 2 + 16 if abs(h / c - 2) < 0.15 and abs((1 - 12 * c - h) / 16 / c - 1) < 0.05 else 0))(1.46 / 44, 0.567 / 18 * 2),
    ['C = \\f{1.46}{44} = 0.0332 mol (0.398 g); H = \\f{0.567 × 2}{18} = 0.063 mol (0.063 g).', 'O = 1 − 0.398 − 0.063 = 0.539 g = 0.0337 mol.', 'C : H : O ≈ 1 : 2 : 1 → CH_{2}O, empirical formula mass 30.'], 'formula', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'formula', 'An organic compound weighing 500 mg, produced 220 mg of CO_{2}, on complete combustion. The percentage composition of carbon in the compound is ______ %. (nearest integer) (Given molar mass in g mol^{−1} of C:12, O:16)',
    None, 12, lambda: round(220 * 12 / 44 / 500 * 100), ['C = 220 × \\f{12}{44} = 60 mg.', '% C = \\f{60}{500} × 100 = 12%.'], 'formula', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'formula', 'The ratio of mass percentage (w/w) of C : H in a hydrocarbon is 12 : 1. It has two carbon atoms. The weight (in g) of CO_{2}(g) formed when 3.38 g of this hydrocarbon is completely burnt in oxygen is : (Given : Molar mass in g mol^{−1} C:12, H:1, O:16)',
    ['5.68', '11.44', '22.74', '17.05'], 2, lambda: near([5.68, 11.44, 22.74, 17.05], 3.38 / 26 * 2 * 44), ['12 : 1 by mass → C : H = 1 : 1 by moles → C_{2}H_{2} (26 g/mol).', '3.38 g = 0.13 mol → 0.26 mol CO_{2} = 11.44 g.'], 'formula', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'formula', 'Complete combustion of X g of an organic compound gave 0.25 g of CO_{2} and 0.12 g of H_{2}O. If the % of carbon is 25% and of hydrogen is 4.89%, then X = ______ × 10^{−3} g. (Nearest integer) (Molar mass of C, H and O are 12, 1 and 16 g mol^{−1} respectively.)',
    ['273', '27', '2730', '227'], 1, lambda: pick([273, 27, 2730, 227], round(0.25 * 12 / 44 / 0.25 * 1000)), ['C = 0.25 × \\f{12}{44} = 0.0682 g, which is 25% of X.', 'X = \\f{0.0682}{0.25} = 0.273 g = 273 × 10^{−3} g (H gives the same: 0.01333/0.0489).'], 'formula', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'formula', '0.01 mole of an organic compound (X) containing 10% hydrogen, on complete combustion produced 0.9 g H_{2}O. Molar mass of (X) is ______ g mol^{−1}.', None, 100, lambda: round(0.9 / 18 * 2 / 0.01 / 0.10),
    ['H_{2}O = 0.05 mol → H = 0.1 mol = 0.1 g, from 0.01 mol X → 10 g H per mole.', '10 g is 10% of the molar mass → M = 100 g mol^{−1}.'], 'formula', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'formula', 'The elemental composition of a compound is 54.2% C, 9.2% H and 36.6% O. If the molar mass of the compound is 132 g mol^{−1}, the molecular formula of the compound is : [Given : The relative atomic mass of C : H : O = 12 : 1 : 16]',
    ['C_{4}H_{8}O_{2}', 'C_{6}H_{12}O_{6}', 'C_{4}H_{9}O_{3}', 'C_{6}H_{12}O_{3}'], 4,
    lambda: pick(['C_{4}H_{8}O_{2}', 'C_{6}H_{12}O_{6}', 'C_{4}H_{9}O_{3}', 'C_{6}H_{12}O_{3}'], (lambda r: f'C_{{{2 * r}}}H_{{{4 * r}}}O_{{{r}}}')(round(132 / 44))),
    ['Moles: C 54.2/12 = 4.52, H 9.2, O 36.6/16 = 2.29 → 2 : 4 : 1 → C_{2}H_{4}O (44).', '\\f{132}{44} = 3 → C_{6}H_{12}O_{3}.'], 'formula', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'formula', 'An oxide of iron contains 69.9% iron, its empirical formula, is: (Given : Molar mass of Fe and O are 56 and 16 g mol^{−1} respectively.)',
    ['FeO', 'Fe_{2}O_{3}', 'Fe_{3}O_{4}', 'FeO_{3}'], 2, lambda: pick(['FeO', 'Fe_{2}O_{3}', 'Fe_{3}O_{4}', 'FeO_{3}'], min([('FeO', 1), ('Fe_{2}O_{3}', 1.5), ('Fe_{3}O_{4}', 4 / 3), ('FeO_{3}', 3)], key=lambda x: abs(x[1] - (30.1 / 16) / (69.9 / 56)))[0]),
    ['Fe : O = \\f{69.9}{56} : \\f{30.1}{16} = 1.248 : 1.881 = 1 : 1.5.', '→ Fe_{2}O_{3}.'], 'formula', 1)

if __name__ == '__main__': print(verify(P), 'real questions verified')
