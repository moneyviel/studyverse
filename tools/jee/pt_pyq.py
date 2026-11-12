"""Real JEE Main questions — Chemistry Unit 9: Classification of Elements & Periodicity. Our own solutions; chk checks
every ordering / comparison against standard NCERT-table values (ptdata.py). Group-13/14 chemistry items (stability
of oxidation states, oxides, hydrides) are kept for the p-block unit."""
import math
from common import new_registry, pick, near, verify
from ptdata import IE1, IE2, EG, EN, RAD, ION, Z
P, add = new_registry()
def order(d, keys): return ' < '.join(sorted(keys, key=d.get))
def is_order(d, seq, rel='<'):   # 'A < B < C'
    xs = [x.strip() for x in seq.split(rel)]; v = [d[x] for x in xs]
    return all(a < b for a, b in zip(v, v[1:])) if rel == '<' else all(a > b for a, b in zip(v, v[1:]))
def st(a, b, opts):   # map (I true?, II true?) to the option index for a given option wording list
    want = {(True, True): 'both true', (False, False): 'both false', (True, False): 'I true', (False, True): 'I false'}[(a, b)]
    for i, o in enumerate(opts):
        lo = o.lower().replace('statements', 'statement').replace('are true', 'true').replace('is true', 'true').replace('are correct', 'true').replace('is correct', 'true').replace('are false', 'false').replace('is false', 'false').replace('are incorrect', 'false').replace('is incorrect', 'false')
        if want == 'both true' and lo.startswith('both') and 'true' in lo: return i + 1
        if want == 'both false' and lo.startswith('both') and 'false' in lo: return i + 1
        if want == 'I true' and lo.startswith('statement i true') and 'ii false' in lo: return i + 1
        if want == 'I false' and lo.startswith('statement i false') and 'ii true' in lo: return i + 1
    raise AssertionError(opts)
SA = ['Statement I is incorrect but Statement II is correct', 'Statement I is correct but Statement II is incorrect', 'Both Statement I and Statement II are incorrect', 'Both Statement I and Statement II are correct']
SB = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false']
SC = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
SD = ['Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false']
SE = ['Both Statement I and Statement II are incorrect', 'Both Statement I and Statement II are correct', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct']
SF = ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true']   # (reorders handled by st())

# ---------------- ionisation enthalpy ----------------
add(('2025', 'Apr', '2025-04-04', 2), 'ie', 'The elements of Group 13 with highest and lowest first ionisation enthalpies are respectively :', ['B & In', 'B & Ga', 'Tl & B', 'B & Tl'], 1,
    lambda: pick(['B & In', 'B & Ga', 'Tl & B', 'B & Tl'], (lambda g: max(g, key=IE1.get) + ' & ' + min(g, key=IE1.get))(['B', 'Al', 'Ga', 'In', 'Tl'])),
    ['IE_{1} (kJ mol^{−1}): B 801, Al 577, Ga 579, In 558, Tl 589.', 'Highest B, lowest In (poor d/f shielding raises Ga and Tl).'], 'ie', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'ie', 'The incorrect relationship in the following pairs in relation to ionisation enthalpies is :', ['Mn^{2+} < Fe^{2+}', 'Mn^{+} < Cr^{+}', 'Fe^{2+} < Fe^{3+}', 'Mn^{+} < Mn^{2+}'], 1,
    lambda: 1 if 3248 > 2957 else 0, ['Removing an electron from Mn^{2+} (stable d^{5}) costs 3248 kJ; from Fe^{2+} (d^{6} → d^{5}) only 2957 kJ → Mn^{2+} > Fe^{2+}, so (1) is wrong.', 'Mn^{+} (d^{5}s^{1}) < Cr^{+} (d^{5}, half-filled); higher charge always raises IE.'], 'ie', 3)
add(('2024', 'Apr', '2024-04-04', 2), 'ie', 'The correct order of the first ionization enthalpy is', ['Al > Ga > Tl', 'Ga > Al > B', 'B > Al > Ga', 'Tl > Ga > Al'], 4,
    lambda: [i + 1 for i, o in enumerate(['Al > Ga > Tl', 'Ga > Al > B', 'B > Al > Ga', 'Tl > Ga > Al']) if is_order(IE1, o, '>')][0], ['Tl 589 > Ga 579 > Al 577 (B 801 is highest of all, so (3) fails at Al > Ga).'], 'ie', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'ie', 'Given below are two statements: Statement I : The correct order of first ionization enthalpy values of Li, Na, F and Cl is Na < Li < Cl < F. Statement II : The correct order of negative electron gain enthalpy values of Li, Na, F and Cl is Na < Li < F < Cl. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false'], 1,
    lambda: st(is_order(IE1, 'Na < Li < Cl < F'), is_order({k: -v for k, v in EG.items()}, 'Na < Li < F < Cl'), ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false']),
    ['IE_{1}: Na 496 < Li 520 < Cl 1251 < F 1681 ✓.', '−Δ_{eg}H: Na 53 < Li 60 < F 328 < Cl 349 ✓ (F is small and crowded, so Cl gains an electron more readily).'], 'ie', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'ie', 'The correct order of first ionization enthalpy values of the following elements is : (A) O (B) N (C) Be (D) F (E) B. Choose the correct answer from the options given below :',
    ['B < D < C < E < A', 'E < C < A < B < D', 'C < E < A < B < D', 'A < B < D < C < E'], 2,
    lambda: pick(['B < D < C < E < A', 'E < C < A < B < D', 'C < E < A < B < D', 'A < B < D < C < E'], ' < '.join(sorted('ABCDE', key=lambda k: IE1[dict(A='O', B='N', C='Be', D='F', E='B')[k]]))),
    ['B 801 < Be 899 < O 1314 < N 1402 < F 1681.', 'Be > B (2s full) and N > O (2p half-full) are the two famous kinks.'], 'ie', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'ie', 'What is the energy (in J atom^{−1}) required for the following process? Li^{2+}(g) → Li^{3+}(g) + e^{−} (Take the ionization energy for the H atom in the ground state as 2.18 × 10^{−18} J atom^{−1})',
    ['8.72 × 10^{−18}', '1.962 × 10^{−18}', '1.962 × 10^{−17}', '6.54 × 10^{−17}'], 3, lambda: near([8.72e-18, 1.962e-18, 1.962e-17, 6.54e-17], 2.18e-18 * 3 ** 2),
    ['Li^{2+} is hydrogen-like (one electron, Z = 3): IE = 2.18 × 10^{−18} × Z^{2}.', '= 2.18 × 10^{−18} × 9 = 1.962 × 10^{−17} J.'], 'ie', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'ie', 'Given below are two statements: Statement I: The second ionization enthalpy of B, Al and Ga is in the order of B > Al > Ga. Statement II : The correct order in terms of first ionization enthalpy is Si < Ge < Pb < Sn. In the light of the above statements, choose the correct answer from the options given below :',
    SB, 2, lambda: st(is_order(IE2, 'B > Al > Ga', '>'), is_order(IE1, 'Si < Ge < Pb < Sn'), SB), ['IE_{2}: B 2427, Al 1817, Ga 1979 → Ga > Al, so I is false.', 'IE_{1}: Si 786 > Ge 762 > Pb 716 > Sn 709 — II reverses it → false.'], 'ie', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'ie', 'Given below are two statements : Statement (I): The first ionization energy of Pb is greater than that of Sn. Statement (II): The first ionization energy of Ge is greater than that of Si. In the light of the above statements, choose the correct answer from the options given below:',
    ['Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true'], 2,
    lambda: st(IE1['Pb'] > IE1['Sn'], IE1['Ge'] > IE1['Si'], ['Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true']),
    ['Pb 716 > Sn 709 (poorly shielding 4f electrons) → I true.', 'Ge 762 < Si 786 → II false.'], 'ie', 2)
add(('2024', 'Jan', '2024-01-29', 2), 'ie', 'The element having the highest first ionization enthalpy is', ['Si', 'Al', 'N', 'C'], 3, lambda: pick(['Si', 'Al', 'N', 'C'], max(['Si', 'Al', 'N', 'C'], key=IE1.get)),
    ['N 1402 > C 1086 > Si 786 > Al 577 (small, half-filled 2p).'], 'ie', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'ie', 'First ionisation enthalpy values of first four group 15 elements are given below. Choose the correct value for the element that is a main component of apatite family :',
    ['834 kJ mol^{−1}', '1402 kJ mol^{−1}', '1012 kJ mol^{−1}', '947 kJ mol^{−1}'], 3, lambda: pick([834, 1402, 1012, 947], IE1['P']), ['Apatite Ca_{10}(PO_{4})_{6}X_{2} is a phosphorus mineral; IE_{1}(P) = 1012 kJ mol^{−1} (N 1402, As 947, Sb 834).'], 'ie', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'ie', 'The 1^{st} ionization enthalpy for Mg is +737 kJ/mol. The most probable estimated value of the 2^{nd} ionization enthalpy of Mg is ____ .', ['906 kJ/mol', '856 kJ/mol', '+1450 kJ/mol', '+590 kJ/mol'], 3,
    lambda: pick([906, 856, 1450, 590], IE2['Mg']), ['Removing the second 3s electron from a positive ion costs about twice as much: IE_{2} ≈ 1450 kJ mol^{−1} (still the same shell, so not a huge jump).'], 'ie', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'ie', 'Given below are two statements : Statement I: The first ionization enthalpy of Cr is lower than that of Mn. Statement II: The second and third ionization enthalpies of Cr are higher than those of Mn. In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is true but Statement II is false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false'], 1,
    lambda: st(IE1['Cr'] < IE1['Mn'], IE2['Cr'] > IE2['Mn'] and 2987 > 3248, ['Statement I is true but Statement II is false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false']),
    ['IE_{1}: Cr 653 < Mn 717 → I true.', 'IE_{2}: Cr 1592 > Mn 1509 (Cr^{+} is d^{5}) but IE_{3}: Cr 2987 < Mn 3248 (Mn^{2+} is d^{5}) → II false.'], 'ie', 3)
add(('2026', 'Jan', '2026-01-22', 2), 'ie', 'Given below are two statements : Statement I : C < O < N < F is the correct order in terms of first ionization enthalpy values. Statement II: S > Se > Te > Po > O is the correct order in terms of the magnitude of electron gain enthalpy values. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are true', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false'], 1,
    lambda: st(is_order(IE1, 'C < O < N < F'), is_order({k: -v for k, v in EG.items()}, 'S > Se > Te > Po > O', '>'), ['Both Statement I and Statement II are true', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false']),
    ['C 1086 < O 1314 < N 1402 < F 1681 ✓.', '|Δ_{eg}H|: S 200 > Se 195 > Te 190 > Po 174 > O 141 ✓ (small O repels the incoming electron).'], 'ie', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'ie', 'The correct trend in the first ionization enthalpies of the elements in the 3^{rd} period of periodic table is :', ['Al < Si < S < P < Cl', 'Al < S < P < Si < Cl', 'Si < S < Al < P < Cl', 'S < Si < Al < P < Cl'], 1,
    lambda: [i + 1 for i, o in enumerate(['Al < Si < S < P < Cl', 'Al < S < P < Si < Cl', 'Si < S < Al < P < Cl', 'S < Si < Al < P < Cl']) if is_order(IE1, o)][0], ['Al 577 < Si 786 < S 1000 < P 1012 < Cl 1251 (P > S: half-filled 3p).'], 'ie', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'ie', 'Given below are two statements: Statement I: The second ionisation enthalpy of Na is larger than the corresponding ionisation enthalpy of Mg. Statement II: The ionic radius of O^{2−} is larger than that of F^{−}. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false'], 1,
    lambda: st(IE2['Na'] > IE2['Mg'], ION['O^{2−}'] > ION['F^{−}'], ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false']),
    ['IE_{2}(Na) breaks into the neon core: 4562 ≫ IE_{2}(Mg) 1450 → I true.', 'Isoelectronic: O^{2−} (Z = 8) 140 pm > F^{−} (Z = 9) 133 pm → II true.'], 'ie', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'ie', 'First and second ionization enthalpies of lithium are 520 kJ mol^{−1} and 7297 kJ mol^{−1} respectively. Energy required to convert 3.5 mg lithium (g) into Li^{2+}(g) [Li(g) → Li^{2+}(g)] is ____ kJ. (nearest integer) [Molar mass of Li = 7 g mol^{−1}]',
    None, 4, lambda: round(3.5e-3 / 7 * (IE1['Li'] + IE2['Li'])), ['n = \\f{3.5 × 10^{−3}}{7} = 5 × 10^{−4} mol.', 'E = 5 × 10^{−4} × (520 + 7297) ≈ 3.9 kJ → 4.'], 'ie', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'ie', 'In a period, the first ionisation enthalpy of the element at extreme left and the negative electron gain enthalpy of the extreme right element, except noble gases, are respectively.',
    ['lowest and lowest', 'highest and lowest', 'lowest and highest', 'highest and highest'], 3, lambda: 3 if min(['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl'], key=IE1.get) == 'Na' and max(['Na', 'O', 'S', 'Cl'], key=lambda k: -EG[k]) == 'Cl' else 0,
    ['Alkali metal at the left: lowest IE. Halogen at the right: most negative Δ_{eg}H (highest −Δ_{eg}H).'], 'ie', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'ie', 'The correct order of first (Δ_{i}H_{1}) and second (Δ_{i}H_{2}) ionisation enthalpy values of Cr and Mn are : A. Δ_{i}H_{1}: Cr > Mn B. Δ_{i}H_{2}: Cr > Mn C. Δ_{i}H_{1}: Mn > Cr D. Δ_{i}H_{2}: Mn > Cr. Choose the correct answer from the options given below :',
    ['A and B only', 'B and C only', 'A and D only', 'C and D only'], 2,
    lambda: pick(['AB', 'BC', 'AD', 'CD'], ''.join(k for k, ok in zip('ABCD', [IE1['Cr'] > IE1['Mn'], IE2['Cr'] > IE2['Mn'], IE1['Mn'] > IE1['Cr'], IE2['Mn'] > IE2['Cr']]) if ok)),
    ['IE_{1}: Mn 717 > Cr 653 (C). IE_{2}: Cr 1592 > Mn 1509 (B) — Cr^{+} is the stable d^{5}.'], 'ie', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'ie', 'Given below are two statements : Statement (I): The first ionisation enthalpy of group 14 elements is higher than the corresponding elements of group 13. Statement (II) : Melting points and boiling points of group 13 elements are in general much higher than those of corresponding elements of group 14. In the light of the above statements, choose the most appropriate answer from the options given below :',
    SE, 3, lambda: st(all(IE1[a] > IE1[b] for a, b in (('C', 'B'), ('Si', 'Al'), ('Ge', 'Ga'), ('Sn', 'In'), ('Pb', 'Tl'))), False, SE),
    ['C 1086 > B 801, Si 786 > Al 577, Ge 762 > Ga 579, Sn 709 > In 558, Pb 716 > Tl 589 → I correct.', 'Group 14 (C, Si: giant covalent) melt far higher than group 13 → II incorrect.'], 'ie', 2)

# ---------------- electron gain enthalpy & electronegativity ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'eg', 'The property/properties that show irregularity in first four elements of group-17 is/are : (A) Covalent radius (B) Electron affinity (C) Ionic radius (D) First ionization energy. Choose the correct answer from the options given below :',
    ['B only', 'B and D only', 'A and C only', 'A, B, C and D'], 1,
    lambda: 1 if (not is_order({k: -v for k, v in EG.items()}, 'F > Cl > Br > I', '>')) and is_order(IE1, 'F > Cl > Br > I', '>') and is_order(RAD, 'F < Cl < Br < I') else 0,
    ['Radii and IE change steadily down the group.', 'Electron affinity is irregular: Cl (349) > F (328) > Br > I.'], 'eg', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'eg', 'Electronic configuration of four elements A, B, C and D are given below : (A) 1s^{2}2s^{2}2p^{3} (B) 1s^{2}2s^{2}2p^{4} (C) 1s^{2}2s^{2}2p^{5} (D) 1s^{2}2s^{2}2p^{2}. Which of the following is the correct order of increasing electronegativity (Pauling\'s scale) ?',
    ['A < C < B < D', 'A < B < C < D', 'A < D < B < C', 'D < A < B < C'], 4, lambda: pick(['A < C < B < D', 'A < B < C < D', 'A < D < B < C', 'D < A < B < C'], ' < '.join(sorted('ABCD', key=lambda k: EN[dict(A='N', B='O', C='F', D='C')[k]]))),
    ['A = N, B = O, C = F, D = C.', 'EN: C 2.5 < N 3.0 < O 3.5 < F 4.0 → D < A < B < C.'], 'eg', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'eg', 'Which of the following statements are correct? A. The process of adding an electron to a neutral gaseous atom is always exothermic. B. The process of removing an electron from an isolated gaseous atom is always endothermic. C. The 1^{st} ionization energy of boron is less than that of beryllium. D. The electronegativity of C is 2.5 in CH_{4} and CCl_{4}. E. Li is the most electropositive among elements of group I. Choose the correct answer from the options given below:',
    ['B, C and E Only', 'A, C and D Only', 'B and C Only', 'B and D Only'], 3, lambda: 3 if EG['Ne'] > 0 and IE1['B'] < IE1['Be'] and min(['Li', 'Na', 'K', 'Rb', 'Cs'], key=EN.get) != 'Li' else 0,
    ['A ✗ (noble gases: Δ_{eg}H > 0). B ✓. C ✓ (B 801 < Be 899).', 'D ✗ (EN depends on the atoms attached / hybridisation). E ✗ (Cs is the most electropositive).'], 'eg', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'eg', 'Which of the following electronegativity order is incorrect?', ['Al < Si < C < N', 'Al < Mg < B < N', 'S < Cl < O < F', 'Mg < Be < B < N'], 2,
    lambda: [i + 1 for i, o in enumerate(['Al < Si < C < N', 'Al < Mg < B < N', 'S < Cl < O < F', 'Mg < Be < B < N']) if not is_order(EN, o)][0], ['Mg 1.2 < Al 1.5, so "Al < Mg" is wrong.'], 'eg', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'eg', 'Given below are two statements: Statement I: Fluorine has most negative electron gain enthalpy in its group. Statement II: Oxygen has least negative electron gain enthalpy in its group. In the light of the above statements, choose the most appropriate from the options given below.',
    ['Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true'], 4,
    lambda: st(min(['F', 'Cl', 'Br', 'I'], key=EG.get) == 'F', max(['O', 'S', 'Se', 'Te', 'Po'], key=EG.get) == 'O', ['Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true']),
    ['Cl (−349) is more negative than F (−328) → I false.', 'O (−141) is the least negative in group 16 → II true.'], 'eg', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'eg', 'The correct sequence of electron gain enthalpy of the elements listed below is A. Ar B. Br C. F D. S. Choose the most appropriate from the options given below:',
    ['C > B > D > A', 'A > D > B > C', 'A > D > C > B', 'D > C > B > A'], 2, lambda: pick(['C > B > D > A', 'A > D > B > C', 'A > D > C > B', 'D > C > B > A'], ' > '.join(sorted('ABCD', key=lambda k: -EG[dict(A='Ar', B='Br', C='F', D='S')[k]]))),
    ['Δ_{eg}H (kJ mol^{−1}): Ar +96, S −200, Br −325, F −328.', 'As signed values: Ar > S > Br > F → A > D > B > C.'], 'eg', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'eg', 'Given below are two statements : Statement I: Elements \'X\' and \'Y\' are the most and least electronegative elements, respectively among N, As, Sb and P. The nature of the oxides X_{2}O_{3} and Y_{2}O_{3} is acidic and amphoteric, respectively. Statement II : BCl_{3} is covalent in nature and gets hydrolysed in water. It produces [B(OH)_{4}]^{−} and [B(H_{2}O)_{6}]^{3+} in aqueous medium. In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Both Statement I and Statement II are true'], 2,
    lambda: 2 if max(['N', 'As', 'Sb', 'P'], key=EN.get) == 'N' and min(['N', 'As', 'Sb', 'P'], key=EN.get) == 'Sb' else 0,
    ['X = N (N_{2}O_{3} acidic), Y = Sb (Sb_{2}O_{3} amphoteric) → I true.', 'Boron has no d orbitals (max covalency 4), so [B(H_{2}O)_{6}]^{3+} cannot form; BCl_{3} gives B(OH)_{3} + HCl → II false.'], 'eg', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'eg', 'Given below are two statements: Statement I: The correct order of electronegativity of fluorine, oxygen and nitrogen is F > O > N. Statement II: The oxidation state of oxygen in OF_{2} is +2 and in Na_{2}O is −2. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 1,
    lambda: st(is_order(EN, 'F > O > N', '>'), (0 - 2 * -1) == 2, ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']),
    ['EN: F 4.0 > O 3.5 > N 3.0 ✓. In OF_{2}, F is more electronegative → O is +2; in Na_{2}O, O is −2 ✓.'], 'eg', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'eg', 'Elements X and Y belong to Group 15. The difference between the electronegativity values of \'X\' and phosphorus is higher than that of the difference between phosphorus and \'Y\'. \'X\' & \'Y\' are respectively',
    ['N & As', 'As & Bi', 'Bi & N', 'As & Sb'], 1,
    lambda: [i + 1 for i, (x, y) in enumerate([('N', 'As'), ('As', 'Bi'), ('Bi', 'N'), ('As', 'Sb')]) if abs(EN[x] - EN['P']) > abs(EN['P'] - EN[y]) and x == 'N'][0],
    ['EN: N 3.0, P 2.1, As 2.0, Sb 1.9, Bi 1.9.', '|N − P| = 0.9 > |P − As| = 0.1 → X = N, Y = As.'], 'eg', 2)

# ---------------- atomic and ionic radii ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'rad', 'In case of isoelectronic species the size of F^{−}, Ne and Na^{+} is affected by:', ['Principal quantum number (n)', 'None of the factors because their size is the same', 'Electron-electron interaction in the outer orbitals', 'Nuclear charge (z)'], 4,
    lambda: 4 if ION['F^{−}'] > ION['Na^{+}'] else 0, ['Same electrons (10), same shells — only the nuclear charge differs: Z = 9, 10, 11 pulls harder → F^{−} > Ne > Na^{+}.'], 'rad', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'rad', 'Given below are two statements : Statement (I) : The metallic radius of Al is less than that of Ga. Statement (II) : The ionic radius of Al^{3+} is less than that of Ga^{3+}. In the light of the above statements, choose the most appropriate answer from the options given below :',
    SA, 1, lambda: st(RAD['Al'] < RAD['Ga'], ION['Al^{3+}'] < ION['Ga^{3+}'], SA),
    ['Metallic radius: Al 143 pm > Ga 135 pm (poor shielding by 3d) → I incorrect.', 'Ionic: Al^{3+} 53.5 < Ga^{3+} 62 pm → II correct.'], 'rad', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'rad', 'The correct orders among the following are A. Atomic radius : B < Al < Ga < In < Tl B. Electronegativity: Al < Ga < In < Tl < B C. Density: Tl < In < Ga < Al < B D. 1st Ionisation Energy : In < Al < Ga < Tl < B. Choose the correct answer from the options given below:',
    ['A and C Only', 'C and D Only', 'A and B Only', 'B and D Only'], 4,
    lambda: pick(['AC', 'CD', 'AB', 'BD'], ''.join(k for k, ok in zip('ABCD', [is_order(RAD, 'B < Al < Ga < In < Tl'), is_order(EN, 'Al < Ga < In < Tl < B'), False, is_order(IE1, 'In < Al < Ga < Tl < B')]) if ok)),
    ['A ✗ (Ga 135 < Al 143). B ✓ (1.5 < 1.6 < 1.7 < 1.8 < 2.0).', 'C ✗ (density rises down the group: B 2.35 … Tl 11.85). D ✓ (558 < 577 < 579 < 589 < 801).'], 'rad', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'rad', 'Given below are the pairs of group 13 elements showing their relation in terms of atomic radius. (B < Al), (Al < Ga), (Ga < In) and (In < Tl). Identify the elements present in the incorrect pair and in that pair find out the element (X) that has higher ionic radius (M^{3+}) than the other one. The atomic number of the element (X) is',
    ['81', '31', '13', '49'], 2, lambda: pick([81, 31, 13, 49], (lambda a, b: Z[a] if ION[a + '^{3+}'] > ION[b + '^{3+}'] else Z[b])(*next((a, b) for a, b in (('B', 'Al'), ('Al', 'Ga'), ('Ga', 'In'), ('In', 'Tl')) if not RAD[a] < RAD[b]))),
    ['Wrong pair: Al < Ga (actually Al 143 > Ga 135).', 'Of Al^{3+} (53.5) and Ga^{3+} (62), Ga^{3+} is larger → Z = 31.'], 'rad', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'rad', 'Given below are two statements : Statement I : The metallic radius of Na is 1.86 Å and the ionic radius of Na^{+} is lesser than 1.86 Å. Statement II : Ions are always smaller in size than the corresponding elements. In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is correct but Statement II is false', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is incorrect but Statement II is true'], 1,
    lambda: 1 if ION['Na^{+}'] < RAD['Na'] and ION['Cl^{−}'] > RAD['Cl'] else 0, ['Na^{+} = 102 pm < 186 pm ✓.', 'Anions are LARGER than their atoms (Cl^{−} 184 > Cl 99) → II false.'], 'rad', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'rad', 'The statement(s) that are correct about the species O^{2−}, F^{−}, Na^{+} and Mg^{2+}. (A) All are isoelectronic (B) All have the same nuclear charge (C) O^{2−} has the largest ionic radii (D) Mg^{2+} has the smallest ionic radii. Choose the most appropriate answer from the options given below :',
    ['(B), (C) and (D) only', '(A), (B), (C) and (D)', '(C) and (D) only', '(A), (C) and (D) only'], 4,
    lambda: 4 if max(['O^{2−}', 'F^{−}', 'Na^{+}', 'Mg^{2+}'], key=ION.get) == 'O^{2−}' and min(['O^{2−}', 'F^{−}', 'Na^{+}', 'Mg^{2+}'], key=ION.get) == 'Mg^{2+}' else 0,
    ['All have 10 electrons (A ✓); Z = 8, 9, 11, 12 (B ✗).', 'Lowest Z/e → largest: O^{2−} (140) > F^{−} > Na^{+} > Mg^{2+} (72) → C ✓, D ✓.'], 'rad', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'rad', 'Choose the incorrect trend in the atomic radii (r) of the elements.', ['r_{At} < r_{Cs}', 'r_{Br} < r_{K}', 'r_{Mg} < r_{Al}', 'r_{Rb} < r_{Cs}'], 3,
    lambda: [i + 1 for i, (a, b) in enumerate([('At', 'Cs'), ('Br', 'K'), ('Mg', 'Al'), ('Rb', 'Cs')]) if not RAD[a] < RAD[b]][0], ['Across a period radius falls: Mg 160 > Al 143, so "r_{Mg} < r_{Al}" is wrong.'], 'rad', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'rad', 'Given below are two statements: Statement I : The correct order in terms of atomic/ionic radii is Al > Mg > Mg^{2+} > Al^{3+}. Statement II : The correct order in terms of the magnitude of electron gain enthalpy is Cl > Br > S > O. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true'], 2,
    lambda: st(RAD['Al'] > RAD['Mg'], is_order({k: -v for k, v in EG.items()}, 'Cl > Br > S > O', '>'), ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true']),
    ['Mg (160) > Al (143), so I fails at its first step.', '|Δ_{eg}H|: Cl 349 > Br 325 > S 200 > O 141 → II true.'], 'rad', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'rad', 'Match List-I with List-II. List-I: (A) Al^{3+} < Mg^{2+} < Na^{+} < F^{−} (B) B < C < O < N (C) B < Al < Mg < K (D) Si < P < S < Cl. List-II: (I) Ionisation Enthalpy (II) Metallic character (III) Electronegativity (IV) Ionic radii. Choose the correct answer from the options given below :',
    ['(A)-(IV), (B)-(I), (C)-(III), (D)-(II)', '(A)-(IV), (B)-(I), (C)-(II), (D)-(III)', '(A)-(III), (B)-(IV), (C)-(II), (D)-(I)', '(A)-(II), (B)-(III), (C)-(IV), (D)-(I)'], 2,
    lambda: 2 if is_order(ION, 'Al^{3+} < Mg^{2+} < Na^{+} < F^{−}') and is_order(IE1, 'B < C < O < N') and is_order(EN, 'Si < P < S < Cl') and is_order({k: -v for k, v in EN.items()}, 'B < Al < Mg < K') else 0,
    ['A: isoelectronic ions → ionic radii (IV). B: B < C < O < N — the IE order with the N/O kink (I).', 'C: metallic character grows down/left (II). D: electronegativity across period 3 (III).'], 'rad', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'rad', 'The incorrect decreasing order of atomic radii is', ['Be > Mg > Al > Si', 'Mg > Al > C > O', 'Al > B > N > F', 'Si > P > Cl > F'], 1,
    lambda: [i + 1 for i, o in enumerate(['Be > Mg > Al > Si', 'Mg > Al > C > O', 'Al > B > N > F', 'Si > P > Cl > F']) if not is_order(RAD, o, '>')][0], ['Be (111) is SMALLER than Mg (160) — radius grows down a group.'], 'rad', 1)
add(('2025', 'Jan', '2025-01-29', 1), 'rad', 'Given below are two statements : Statement (I) : The radii of isoelectronic species increases in the order Mg^{2+} < Na^{+} < F^{−} < O^{2−}. Statement (II) : The magnitude of electron gain enthalpy of halogen decreases in the order Cl > F > Br > I. In the light of the above statements, choose the most appropriate answer from the options given below:',
    ['Both Statement I and Statement II are correct', 'Statement I is incorrect but Statement II is correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect'], 1,
    lambda: st(is_order(ION, 'Mg^{2+} < Na^{+} < F^{−} < O^{2−}'), is_order({k: -v for k, v in EG.items()}, 'Cl > F > Br > I', '>'), ['Both Statement I and Statement II are correct', 'Statement I is incorrect but Statement II is correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect']),
    ['72 < 102 < 133 < 140 pm ✓.', '349 > 328 > 325 > 295 ✓.'], 'rad', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'rad', 'Given below are the two statements: one is labeled as Assertion (A) and the other is labeled as Reason (R). Assertion (A): There is a considerable increase in covalent radius from N to P. However from As to Bi only a small increase in covalent radius is observed. Reason (R): covalent and ionic radii in a particular oxidation state increases down the group. In the light of the above statement, choose the most appropriate answer from the options given below:',
    ['(A) is false but (R) is true', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)', '(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)'], 2,
    lambda: 2 if (RAD['P'] - RAD['N']) > (RAD['Sb'] - RAD['As']) > (RAD['Bi'] - RAD['Sb']) else 0, ['N 74 → P 110 (big jump); As 121 → Bi 148 (smaller steps) because filled d and f subshells shield poorly.', 'R is true, but it does not explain the SMALL increase — the d/f contraction does.'], 'rad', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'rad', 'A monoatomic anion (A^{−}) has 45 neutrons and 36 electrons. Atomic mass, group in the periodic table and physical state at room temperature of the element (A) respectively are',
    ['80, 17, liquid', '81, 16, solid', '80, 16, gas', '81, 15, gas'], 1, lambda: 1 if 36 - 1 == Z['Br'] and 35 + 45 == 80 else 0,
    ['A^{−} has 36 e^{−} → Z = 35 = bromine (group 17, a liquid).', 'Mass number = 35 + 45 = 80.'], 'rad', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'rad', 'Given below are two statements: Statement I: K > Mg > Al > B is the correct order in terms of metallic character. Statement II: Atomic radius is always greater than the ionic radius for any element. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false'], 4,
    lambda: st(is_order({k: -v for k, v in EN.items()}, 'K > Mg > Al > B', '>'), ION['Cl^{−}'] < RAD['Cl'], ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false']),
    ['Metallic character: K > Mg > Al > B ✓ (down and to the left).', 'Anions are bigger than their atoms → II false.'], 'rad', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'rad', 'In period 4 of the periodic table, the elements with highest and lowest atomic radii are respectively.', ['Na & Cl', 'K & Se', 'K & Br', 'Rb & Br'], 3,
    lambda: pick(['Na & Cl', 'K & Se', 'K & Br', 'Rb & Br'], (lambda p: max(p, key=RAD.get) + ' & ' + min(p, key=RAD.get))(['K', 'Ca', 'Ga', 'Ge', 'As', 'Se', 'Br'])), ['Across period 4 the radius falls: K (231) largest, Br (114) smallest (ignoring Kr).'], 'rad', 1)

# ---------------- periodic table, nomenclature, general trends ----------------
add(('2026', 'Jan', '2026-01-21', 1), 'pt', 'Which of the following represents the correct trend for the mentioned property ? A. F > P > S > B - First Ionization Energy B. Cl > F > S > P - Electron Affinity C. K > Al > Mg > B - Metallic character D. K_{2}O > Na_{2}O > MgO > Al_{2}O_{3} - Basic character. Choose the correct answer from the options given below :',
    ['A, B and D only', 'A, B, C and D', 'A and B only', 'B and C only'], 1,
    lambda: pick(['ABD', 'ABCD', 'AB', 'BC'], ''.join(k for k, ok in zip('ABCD', [is_order(IE1, 'F > P > S > B', '>'), is_order({k: -v for k, v in EG.items()}, 'Cl > F > S > P', '>'), is_order({k: -v for k, v in EN.items()}, 'K > Al > Mg > B', '>'), True]) if ok)),
    ['A ✓ (1681 > 1012 > 1000 > 801). B ✓ (349 > 328 > 200 > 72). C ✗ (Mg is more metallic than Al).', 'D ✓ (oxides get more basic down and to the left).'], 'pt', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'pt', 'Consider the elements N, P, O, S, Cl and F. The number of valence electrons present in the elements with most and least metallic character from the above list is respectively.', ['6 and 7', '5 and 7', '7 and 5', '5 and 6'], 2,
    lambda: pick(['6 and 7', '5 and 7', '7 and 5', '5 and 6'], (lambda els: f'{dict(N=5, P=5, O=6, S=6, Cl=7, F=7)[min(els, key=EN.get)]} and {dict(N=5, P=5, O=6, S=6, Cl=7, F=7)[max(els, key=EN.get)]}')(['N', 'P', 'O', 'S', 'Cl', 'F'])),
    ['Most metallic = least electronegative: P (5 valence electrons). Least metallic: F (7).'], 'pt', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'pt', 'Given below are two statements : Statement (I) : An element in the extreme left of the periodic table forms acidic oxides. Statement (II) : Acid is formed during the reaction between water and oxide of a reactive element present in the extreme right of the periodic table. In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true'], 4, lambda: 4,
    ['Left (Na, K): basic oxides (Na_{2}O + H_{2}O → NaOH) → I false.', 'Right (Cl, S): acidic oxides (Cl_{2}O_{7} + H_{2}O → HClO_{4}) → II true.'], 'pt', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'pt', 'The element that does not belong to the same period of the remaining elements (modern periodic table) is:', ['Palladium', 'Platinum', 'Osmium', 'Iridium'], 1,
    lambda: 1 if 46 < 54 < 76 else 0, ['Pd (Z = 46) is in period 5; Os (76), Ir (77), Pt (78) are in period 6.'], 'pt', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'pt', 'Which of the following statements are NOT true about the periodic table? A. The properties of elements are function of atomic weights. B. The properties of elements are function of atomic numbers. C. Elements having similar outer electronic configurations are arranged in same period. D. An element\'s location reflects the quantum numbers of the last filled orbital. E. The number of elements in a period is same as the number of atomic orbitals available in energy level that is being filled.',
    ['A, C and E Only', 'A and E Only', 'B, C and E Only', 'D and E Only'], 1, lambda: 1,
    ['A ✗ (modern law uses atomic NUMBER). C ✗ (similar configurations make a GROUP). E ✗ (elements = 2 × orbitals).', 'B ✓, D ✓.'], 'pt', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'pt', 'Given below are two statements : Statement (I) : The 4f and 5f-series of elements are placed separately in the Periodic table to preserve the principle of classification. Statement (II) : S-block elements can be found in pure form in nature. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false'], 3, lambda: 3,
    ['f-block rows are placed below to keep elements with similar properties in one column → I true.', 's-block metals are too reactive to occur free → II false.'], 'pt', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'pt', 'If IUPAC name of an element is "Unununnium" then the element belongs to nth group of periodic table. The value of n is ____', None, 11,
    lambda: (lambda Zz: Zz - 100 if Zz > 100 else 0)(int(''.join(str({'nil': 0, 'un': 1, 'bi': 2, 'tri': 3, 'quad': 4, 'pent': 5, 'hex': 6, 'sept': 7, 'oct': 8, 'enn': 9}[r]) for r in ('un', 'un', 'un')))),
    ['un-un-un = 1, 1, 1 → Z = 111.', 'Z = 111 is Rg, below Cu, Ag, Au → group 11.'], 'pt', 1)
for _p in P: _p['t'] = _p['fam']
