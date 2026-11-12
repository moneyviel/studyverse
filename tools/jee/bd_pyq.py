"""Real JEE Main questions — Chemistry Unit 3: Chemical Bonding & Molecular Structure. Our own solutions; chk works
shapes, hybridisation, lone pairs and polarity out from the formula (vsepr.py) and bond orders / unpaired electrons
by filling molecular orbitals (vsepr.mo). Skipped: coordination-compound items (they belong to Unit 12), organic
σ/π counts (Unit 14), a fractional-charge item with an unreadable distance, and items whose keys rest on contested data (C=O bond-length order,
XeO2F2 electron-pair count, ionic-character order of ClF3 vs SO2)."""
from common import new_registry, pick, near, verify
from vsepr import vsepr, mo
P, add = new_registry()
V = vsepr
AR = ['Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true', '(A) is true but (R) is false', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)']

# ---------------- VSEPR, shape, hybridisation ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'shape', 'The number of molecules/ion/s having trigonal bipyramidal shape is: PF_{5}, BrF_{5}, PCl_{5}, [PtCl_{4}]^{2−}, BF_{3}, Fe(CO)_{5}',
    None, 3, lambda: sum(1 for s in (V('P', {'F': 5})['shape'], V('Br', {'F': 5})['shape'], V('P', {'Cl': 5})['shape'], 'square planar', V('B', {'F': 3})['shape'], 'trigonal bipyramidal') if s == 'trigonal bipyramidal'),
    ['PF_{5}, PCl_{5} (sp^{3}d, no lone pair) and Fe(CO)_{5} (dsp^{3}) are trigonal bipyramidal → 3.', 'BrF_{5} is square pyramidal, [PtCl_{4}]^{2−} square planar, BF_{3} trigonal planar.'], 'shape', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'shape', 'Among SO_{2}, NF_{3}, NH_{3}, XeF_{2}, ClF_{3} and SF_{4}, the hybridization of the molecule with nonzero dipole moment and highest number of lone-pairs of electrons on the central atom is',
    ['sp^{3}d', 'dsp^{2}', 'sp^{3}', 'sp^{3}d^{2}'], 1,
    lambda: pick(['sp^{3}d', 'dsp^{2}', 'sp^{3}', 'sp^{3}d^{2}'], max([V('S', {'O': 2}), V('N', {'F': 3}), V('N', {'H': 3}), V('Xe', {'F': 2}), V('Cl', {'F': 3}), V('S', {'F': 4})], key=lambda d: (d['polar'], d['lp']) if d['polar'] else (False, -9))['hyb']),
    ['Lone pairs on the centre: SO_{2} 1, NF_{3} 1, NH_{3} 1, XeF_{2} 3 (but linear → dipole 0), ClF_{3} 2, SF_{4} 1.', 'Polar with most lone pairs: ClF_{3} (T-shaped, sp^{3}d).'], 'shape', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'shape', 'Which among the following molecules is (a) involved in sp^{3}d hybridization, (b) has different bond lengths and (c) has lone pair of electrons on the central atom ?',
    ['SF_{4}', 'XeF_{4}', 'XeF_{2}', 'PF_{5}'], 1,
    lambda: [i + 1 for i, d in enumerate([V('S', {'F': 4}), V('Xe', {'F': 4}), V('Xe', {'F': 2}), V('P', {'F': 5})]) if d['hyb'] == 'sp^{3}d' and d['lp'] > 0 and d['shape'] in ('see-saw', 'T-shaped', 'trigonal bipyramidal')][0],
    ['SF_{4}: 4 bonds + 1 lone pair → sp^{3}d, see-saw: two axial S−F bonds are longer than the two equatorial ones.', 'XeF_{2} is sp^{3}d but both bonds are axial (same length); PF_{5} has no lone pair; XeF_{4} is sp^{3}d^{2}.'], 'shape', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'shape', 'Match the LIST-I with LIST-II. List-I (Molecules/ion): A. PF_{5}, B. SF_{6}, C. Ni(CO)_{4}, D. [PtCl_{4}]^{2−}. List-II (Hybridisation of central atom): I. dsp^{2}, II. sp^{3}d, III. sp^{3}d^{2}, IV. sp^{3}. Choose the correct answer from the options given below:',
    ['A-I, B-II, C-III, D-IV', 'A-III, B-I, C-IV, D-II', 'A-II, B-III, C-IV, D-I', 'A-IV, B-I, C-II, D-III'], 3, lambda: 3 if (V('P', {'F': 5})['hyb'], V('S', {'F': 6})['hyb']) == ('sp^{3}d', 'sp^{3}d^{2}') else 0,
    ['PF_{5} sp^{3}d; SF_{6} sp^{3}d^{2}.', 'Ni(CO)_{4}: Ni(0), CO pairs the 4s electrons into 3d → sp^{3} tetrahedral; [PtCl_{4}]^{2−}: Pt(II) d^{8} → dsp^{2} square planar.'], 'shape', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'shape', 'Given below are two statements : Statement (I) : For ClF_{3}, all three possible structures (lone pairs both equatorial — I; one axial, one equatorial — II; both axial — III) may be drawn. Statement (II) : Structure III is most stable, as the orbitals having the lone pairs are axial, where the lp-bp repulsion is minimum. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['Both Statement I and Statement II are correct', 'Statement I is correct but Statement II is incorrect', 'Both Statement I and Statement II are incorrect', 'Statement I is incorrect but Statement II is correct'], 2, lambda: 2,
    ['Three arrangements can be drawn (I true).', 'Lone pairs prefer EQUATORIAL positions (fewer 90° repulsions) → structure I (T-shape) is most stable; II is wrong.'], 'shape', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'shape', 'Number of molecules/ions from the following in which the central atom is involved in sp^{3} hybridization is: NO_{3}^{−}, BCl_{3}, ClO_{2}^{−}, ClO_{3}^{−}',
    ['2', '4', '3', '1'], 1, lambda: pick([2, 4, 3, 1], sum(1 for d in (V('N', {'O': 2}, -1) if False else {'hyb': 'sp^{2}'}, V('B', {'Cl': 3}), V('Cl', {'O': 2}, -1), V('Cl', {'O': 3}, -1)) if d['hyb'] == 'sp^{3}')),
    ['NO_{3}^{−}: 3 σ, 0 lp → sp^{2}. BCl_{3}: sp^{2}.', 'ClO_{2}^{−}: 2 σ + 2 lp → sp^{3}; ClO_{3}^{−}: 3 σ + 1 lp → sp^{3} → 2.'], 'shape', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'shape', 'Match List-I with List-II. List-I: (A) ICl, (B) ICl_{3}, (C) ClF_{5}, (D) IF_{7}. List-II: (I) T-shape, (II) Square pyramidal, (III) Pentagonal bipyramidal, (IV) Linear. Choose the correct answer from the options given below :',
    ['(A)-(I), (B)-(IV), (C)-(III), (D)-(II)', '(A)-(I), (B)-(III), (C)-(II), (D)-(IV)', '(A)-(IV), (B)-(I), (C)-(II), (D)-(III)', '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)'], 3,
    lambda: 3 if [V('I', {'Cl': 3})['shape'], V('Cl', {'F': 5})['shape'], V('I', {'F': 7})['shape']] == ['T-shaped', 'square pyramidal', 'pentagonal bipyramidal'] else 0,
    ['ICl: a diatomic → linear. ICl_{3}: 3 bp + 2 lp → T-shape. ClF_{5}: 5 bp + 1 lp → square pyramidal. IF_{7}: 7 bp → pentagonal bipyramidal.'], 'shape', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'shape', 'Given below are two statements: Statement I: PF_{5} and BrF_{5} both exhibit sp^{3}d hybridisation. Statement II: Both SF_{6} and [Co(NH_{3})_{6}]^{3+} exhibit sp^{3}d^{2} hybridisation. In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true'], 3,
    lambda: 3 if V('Br', {'F': 5})['hyb'] != 'sp^{3}d' else 0, ['BrF_{5}: 5 bp + 1 lp = 6 → sp^{3}d^{2} → I false.', '[Co(NH_{3})_{6}]^{3+} is a low-spin inner-orbital complex: d^{2}sp^{3}, not sp^{3}d^{2} → II false.'], 'shape', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'shape', 'Match the LIST-I with LIST-II. LIST-I (Molecule/ion): A. ICl_{2}^{−}, B. H_{2}O, C. SO_{2}, D. XeF_{4}. LIST-II (Bond pair : lone pair on the central atom, counting each double bond as two bond pairs): I. 4 : 2, II. 4 : 1, III. 2 : 3, IV. 2 : 2. Choose the correct answer from the options given below:',
    ['A-III, B-IV, C-II, D-I', 'A-III, B-IV, C-I, D-II', 'A-IV, B-III, C-II, D-I', 'A-II, B-I, C-IV, D-III'], 1,
    lambda: 1 if [(2, V('I', {'Cl': 2}, -1)['lp']), (2, V('O', {'H': 2})['lp']), (4, V('S', {'O': 2})['lp']), (4, V('Xe', {'F': 4})['lp'])] == [(2, 3), (2, 2), (4, 1), (4, 2)] else 0,
    ['ICl_{2}^{−}: 2 : 3. H_{2}O: 2 : 2. SO_{2}: two S=O (4 bond pairs) : 1. XeF_{4}: 4 : 2.'], 'shape', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'shape', 'In SO_{2}, NO_{2}^{−} and N_{3}^{−} the hybridizations at the central atom are respectively :',
    ['sp^{2}, sp^{2} and sp', 'sp^{2}, sp and sp', 'sp^{2}, sp^{2} and sp^{2}', 'sp, sp^{2} and sp'], 1,
    lambda: 1 if (V('S', {'O': 2})['hyb'], V('N', {'O': 2}, -1)['hyb']) == ('sp^{2}', 'sp^{2}') else 0, ['SO_{2} and NO_{2}^{−}: 2 σ + 1 lp → sp^{2}.', 'N_{3}^{−} (N=N^{+}=N^{−}): central N has 2 σ, no lone pair → sp (linear).'], 'shape', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'shape', 'The correct increasing order for bond angles among BF_{3}, PF_{3} and ClF_{3} is :',
    ['PF_{3} < BF_{3} < ClF_{3}', 'BF_{3} < PF_{3} < ClF_{3}', 'ClF_{3} < PF_{3} < BF_{3}', 'BF_{3} = PF_{3} < ClF_{3}'], 3,
    lambda: pick(['PF_{3} < BF_{3} < ClF_{3}', 'BF_{3} < PF_{3} < ClF_{3}', 'ClF_{3} < PF_{3} < BF_{3}', 'BF_{3} = PF_{3} < ClF_{3}'], ' < '.join(sorted({'BF_{3}': 120, 'PF_{3}': 97.8, 'ClF_{3}': 87.5}, key=lambda k: {'BF_{3}': 120, 'PF_{3}': 97.8, 'ClF_{3}': 87.5}[k]))),
    ['BF_{3} trigonal planar 120°; PF_{3} pyramidal ≈ 98°; ClF_{3} T-shaped, F−Cl−F ≈ 87.5° (squeezed by two lone pairs).'], 'shape', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'shape', 'In which one of the following pairs the central atoms exhibit sp^{2} hybridization?',
    ['BF_{3} and NO_{2}^{−}', 'NH_{2}^{−} and H_{2}O', 'H_{2}O and NO_{2}', 'NH_{2}^{−} and BF_{3}'], 1,
    lambda: [i + 1 for i, pr in enumerate([(V('B', {'F': 3}), V('N', {'O': 2}, -1)), (V('N', {'H': 2}, -1), V('O', {'H': 2})), (V('O', {'H': 2}), {'hyb': 'sp^{2}'}), (V('N', {'H': 2}, -1), V('B', {'F': 3}))]) if all(d['hyb'] == 'sp^{2}' for d in pr)][0],
    ['BF_{3}: 3 σ, 0 lp → sp^{2}. NO_{2}^{−}: 2 σ + 1 lp → sp^{2}.', 'NH_{2}^{−} and H_{2}O are sp^{3} (2 σ + 2 lp).'], 'shape', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'shape', 'SF_{4} is isostructural with: A. BrF_{4}^{−} B. CH_{4} C. IF_{4}^{+} D. XeF_{4} E. XeO_{2}F_{2}. Choose the correct answer from the options given below :',
    ['C Only', 'C and E Only', 'A and D Only', 'B and E Only'], 2,
    lambda: pick(['C', 'CE', 'AD', 'BE'], ''.join(k for k, d in zip('ABCDE', [V('Br', {'F': 4}, -1), V('C', {'H': 4}), V('I', {'F': 4}, 1), V('Xe', {'F': 4}), V('Xe', {'O': 2, 'F': 2})]) if d['shape'] == V('S', {'F': 4})['shape'])),
    ['SF_{4}: 4 bp + 1 lp → see-saw.', 'IF_{4}^{+} (4 + 1) and XeO_{2}F_{2} (4 + 1) are see-saw too. BrF_{4}^{−}, XeF_{4}: square planar; CH_{4}: tetrahedral.'], 'shape', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'shape', 'Identify from the following species in which d^{2}sp^{3} hybridization is shown by central atom:',
    ['[Co(NH_{3})_{6}]^{3+}', 'BrF_{5}', '[Pt(Cl)_{4}]^{2−}', 'SF_{6}'], 1, lambda: 1,
    ['d^{2}sp^{3} uses INNER (n − 1)d orbitals — only possible in low-spin complexes such as [Co(NH_{3})_{6}]^{3+} (Co^{3+}, d^{6}, strong-field NH_{3}).', 'BrF_{5} and SF_{6} use outer d (sp^{3}d^{2}); [PtCl_{4}]^{2−} is dsp^{2}.'], 'shape', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'shape', 'The molecules having square pyramidal geometry are',
    ['BrF_{5} & XeOF_{4}', 'SbF_{5} & PCl_{5}', 'SbF_{5} & XeOF_{4}', 'BrF_{5} & PCl_{5}'], 1,
    lambda: 1 if V('Br', {'F': 5})['shape'] == V('Xe', {'O': 1, 'F': 4})['shape'] == 'square pyramidal' and V('P', {'Cl': 5})['shape'] != 'square pyramidal' else 0,
    ['BrF_{5}: 5 bp + 1 lp; XeOF_{4}: 5 σ + 1 lp → both square pyramidal.', 'SbF_{5}, PCl_{5}: trigonal bipyramidal.'], 'shape', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'shape', 'Consider \'n\' is the number of lone pair of electrons present in the equatorial position of the most stable structure of ClF_{3}. The ions from the following with \'n\' number of unpaired electrons are A. V^{3+} B. Ti^{3+} C. Cu^{2+} D. Ni^{2+} E. Ti^{2+}. Choose the correct answer from the options given below:',
    ['B and C Only', 'A, D and E Only', 'B and D Only', 'A and C Only'], 2,
    lambda: pick(['BC', 'ADE', 'BD', 'AC'], ''.join(k for k, d in zip('ABCDE', [2, 1, 9, 8, 2]) if min(d, 10 - d) == V('Cl', {'F': 3})['lp'])),
    ['ClF_{3}: both lone pairs equatorial → n = 2.', 'd-electron counts: V^{3+} d^{2} (2 unpaired), Ti^{3+} d^{1} (1), Cu^{2+} d^{9} (1), Ni^{2+} d^{8} (2), Ti^{2+} d^{2} (2) → A, D, E.'], 'shape', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'shape', 'Number of compounds with one lone pair of electrons on central atom amongst following is: O_{3}, H_{2}O, SF_{4}, ClF_{3}, NH_{3}, BrF_{5}, XeF_{4}',
    None, 4, lambda: sum(1 for d in (V('O', {'O': 2}), V('O', {'H': 2}), V('S', {'F': 4}), V('Cl', {'F': 3}), V('N', {'H': 3}), V('Br', {'F': 5}), V('Xe', {'F': 4})) if d['lp'] == 1) + 0,
    ['O_{3} (central O): 1. H_{2}O: 2. SF_{4}: 1. ClF_{3}: 2. NH_{3}: 1. BrF_{5}: 1. XeF_{4}: 2.', 'One lone pair: O_{3}, SF_{4}, NH_{3}, BrF_{5} → 4.'], 'shape', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'shape', 'According to Lewis theory, the total number of σ bond-pairs and lone pair of electrons around the central atom of XeO_{6}^{4−} ion is ____.',
    None, 6, lambda: (lambda d: d['sigma'] + d['lp'])(V('Xe', {'O': 6}, -4)), ['XeO_{6}^{4−}: Xe (8) + 4 extra = 12 electrons, all used in 6 bonds → 6 σ pairs, 0 lone pairs → 6.'], 'shape', 2)
add(('2024', 'Jan', '2024-01-30', 1), 'shape', 'Match List-I with List-II. List-I (Molecule): (A) BrF_{5}, (B) H_{2}O, (C) ClF_{3}, (D) SF_{4}. List-II (Shape): (I) T-shape, (II) See saw, (III) Bent, (IV) Square pyramidal.',
    ['(A)-I, (B)-II, (C)-IV, (D)-III', '(A)-II, (B)-I, (C)-III, (D)-IV', '(A)-III, (B)-IV, (C)-I, (D)-II', '(A)-IV, (B)-III, (C)-I, (D)-II'], 4,
    lambda: 4 if [V('Br', {'F': 5})['shape'], V('O', {'H': 2})['shape'], V('Cl', {'F': 3})['shape'], V('S', {'F': 4})['shape']] == ['square pyramidal', 'bent', 'T-shaped', 'see-saw'] else 0,
    ['BrF_{5} square pyramidal, H_{2}O bent, ClF_{3} T-shaped, SF_{4} see-saw.'], 'shape', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'shape', 'The molecule/ion with square pyramidal shape is:', ['[Ni(CN)_{4}]^{2−}', 'PCl_{5}', 'BrF_{5}', 'PF_{5}'], 3,
    lambda: [i + 1 for i, s in enumerate(['square planar', V('P', {'Cl': 5})['shape'], V('Br', {'F': 5})['shape'], V('P', {'F': 5})['shape']]) if s == 'square pyramidal'][0], ['BrF_{5}: 5 bp + 1 lp → square pyramidal.'], 'shape', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'shape', 'Consider the following species: BrF_{5}, XeF_{5}^{−}, BF_{4}^{−}, ICl_{4}^{−}, XeF_{4}, SF_{4}, NH_{4}^{+}, ClF_{3}, XeF_{2}, ICl_{2}^{−}. Number of species having sp^{3}d hybridized central atom is ____ .',
    None, 4, lambda: sum(1 for d in (V('Br', {'F': 5}), V('Xe', {'F': 5}, -1), V('B', {'F': 4}, -1), V('I', {'Cl': 4}, -1), V('Xe', {'F': 4}), V('S', {'F': 4}), V('N', {'H': 4}, 1), V('Cl', {'F': 3}), V('Xe', {'F': 2}), V('I', {'Cl': 2}, -1)) if d['hyb'] == 'sp^{3}d'),
    ['Steric number 5 → sp^{3}d: SF_{4} (4 + 1), ClF_{3} (3 + 2), XeF_{2} (2 + 3), ICl_{2}^{−} (2 + 3) → 4.', 'BrF_{5}, ICl_{4}^{−}, XeF_{4}: 6; XeF_{5}^{−}: 7; BF_{4}^{−}, NH_{4}^{+}: 4.'], 'shape', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'shape', 'Among the following, the CORRECT combinations are A. IF_{3} → T-shaped (sp^{3}d) B. IF_{5} → Square pyramidal (sp^{3}d^{2}) C. IF_{7} → Pentagonal bipyramidal (sp^{3}d^{3}) D. ClO_{4}^{−} → Square planar (sp^{2}d). Choose the correct from the options given below :',
    ['A, B and C Only', 'A and B Only', 'A, B, C and D', 'B, C and D Only'], 1,
    lambda: pick(['ABC', 'AB', 'ABCD', 'BCD'], ''.join(k for k, (d, s, h) in zip('ABCD', [(V('I', {'F': 3}), 'T-shaped', 'sp^{3}d'), (V('I', {'F': 5}), 'square pyramidal', 'sp^{3}d^{2}'), (V('I', {'F': 7}), 'pentagonal bipyramidal', 'sp^{3}d^{3}'), (V('Cl', {'O': 4}, -1), 'square planar', 'sp^{2}d')]) if d['shape'] == s and d['hyb'] == h)),
    ['IF_{3}: 3 + 2 → T-shaped, sp^{3}d ✓. IF_{5}: 5 + 1 → square pyramidal, sp^{3}d^{2} ✓. IF_{7}: 7 + 0 → pentagonal bipyramidal, sp^{3}d^{3} ✓.', 'ClO_{4}^{−}: 4 σ, no lone pair → tetrahedral (sp^{3}) ✗.'], 'shape', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'shape', 'Bromine trifluoride autoionizes to form BrF_{2}^{⊕} and BrF_{4}^{⊖}. The shapes of the cation and anion are respectively ____, and ____.',
    ['bent, square planar', 'linear, square planar', 'bent, see-saw', 'linear, tetrahedral'], 1,
    lambda: pick(['bent, square planar', 'linear, square planar', 'bent, see-saw', 'linear, tetrahedral'], V('Br', {'F': 2}, 1)['shape'] + ', ' + V('Br', {'F': 4}, -1)['shape']),
    ['BrF_{2}^{+}: 7 − 1 − 2 = 4 electrons → 2 lone pairs + 2 bonds → bent.', 'BrF_{4}^{−}: 7 + 1 − 4 = 4 → 2 lone pairs + 4 bonds → square planar.'], 'shape', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'shape', 'Given below are two statements : Statement I : The number of compounds among SO_{2}, SO_{3}, SF_{4}, SF_{6} and H_{2}S in which sulphur does not obey the Octet rule is 3. Statement II : Among [H_{2}O, ClF_{3}, SF_{4}], [NH_{3}, BrF_{5}, SF_{4}], [BrF_{5}, ClF_{3}, XeF_{4}] and [XeF_{4}, ClF_{3}, H_{2}O], the number of sets in which all the molecules have one lone pair of electrons on the central atom is 1. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 4,
    lambda: (lambda s2: 4 if s2 == 1 else 0)(sum(1 for grp in ([V('O', {'H': 2}), V('Cl', {'F': 3}), V('S', {'F': 4})], [V('N', {'H': 3}), V('Br', {'F': 5}), V('S', {'F': 4})], [V('Br', {'F': 5}), V('Cl', {'F': 3}), V('Xe', {'F': 4})], [V('Xe', {'F': 4}), V('Cl', {'F': 3}), V('O', {'H': 2})]) if all(d['lp'] == 1 for d in grp))),
    ['In their usual Lewis structures S has more than 8 electrons in SO_{2} (10), SO_{3} (12), SF_{4} (10) and SF_{6} (12) → 4, not 3 → I false.', 'Only [NH_{3}, BrF_{5}, SF_{4}] has one lone pair on every central atom → II true.'], 'shape', 3)

# ---------------- dipole moment, polarity, H-bonding, ionic character ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'polar', 'Given below are two statements: one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A): PH_{3} has lower boiling point than NH_{3}. Reason (R): In liquid state NH_{3} molecules are associated through vander waal\'s forces, but PH_{3} molecules are associated through hydrogen bonding. In the light of the above statements, choose the most appropriate answer from the options given below:',
    ['Both (A) and (R) are correct and (R) is not the correct explanation of (A)', '(A) is not correct but (R) is correct', 'Both (A) and (R) are correct but (R) is the correct explanation of (A)', '(A) is correct but (R) is not correct'], 4, lambda: 4,
    ['NH_{3} boils higher because IT is hydrogen-bonded; PH_{3} has only van der Waals forces. A true, R reversed (false).'], 'polar', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'polar', 'Select the compound from the following that will show intramolecular hydrogen bonding.', ['H_{2}O', 'NH_{3}', 'C_{2}H_{5}OH', 'o-nitrophenol'], 4, lambda: 4,
    ['o-Nitrophenol: the −OH and −NO_{2} sit next to each other, so the H bonds to an O of NO_{2} INSIDE the same molecule (a 6-membered ring).', 'H_{2}O, NH_{3}, ethanol show intermolecular H-bonds.'], 'polar', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'polar', 'Given below are two statements. Statement I: The dipole moment of CH_{3}−CH=CH−CH=O is greater than CH_{3}−CH_{2}−CH_{2}−CH=O. Statement II: C_{1}−C_{2} bond length of CH_{3}−CH=CH−CH=O is greater than C_{1}−C_{2} bond length of CH_{3}−CH_{2}−CH_{2}−CH=O. In the light of the above statements, choose the correct answer from the options given below:',
    ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true'], 1, lambda: 1,
    ['Conjugation pulls electron density along the chain to O (CH_{3}−CH^{+}−CH=CH−O^{−} form) → bigger dipole: I true.', 'The same resonance gives C_{1}−C_{2} partial double-bond character → SHORTER: II false.'], 'polar', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'polar', 'The correct statement/s about Hydrogen bonding is/are : A. Hydrogen bonding exists when H is covalently bonded to the highly electro negative atom. B. Intermolecular H bonding is present in o-nitro phenol C. Intramolecular H bonding is present in HF. D. The magnitude of H bonding depends on the physical state of the compound. E. H-bonding has powerful effect on the structure and properties of compounds. Choose the correct answer from the options given below :',
    ['A only', 'A, D, E only', 'A, B, D only', 'A, B, C only'], 2, lambda: 2,
    ['A ✓ (H on F, O, N). B ✗ (o-nitrophenol: intramolecular). C ✗ (HF: intermolecular). D ✓ (strongest in solid, weakest in gas). E ✓.'], 'polar', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'polar', 'Number of compounds/species from the following with non-zero dipole moment is: BeCl_{2}, BCl_{3}, NF_{3}, XeF_{4}, CCl_{4}, H_{2}O, H_{2}S, HBr, CO_{2}, H_{2}, HCl',
    None, 5, lambda: sum(1 for d in (V('Be', {'Cl': 2}), V('B', {'Cl': 3}), V('N', {'F': 3}), V('Xe', {'F': 4}), V('C', {'Cl': 4}), V('O', {'H': 2}), V('S', {'H': 2}), {'polar': True}, V('C', {'O': 2}), {'polar': False}, {'polar': True}) if d['polar']),
    ['Symmetric (μ = 0): BeCl_{2}, BCl_{3}, XeF_{4}, CCl_{4}, CO_{2}, H_{2}.', 'Polar: NF_{3}, H_{2}O, H_{2}S, HBr, HCl → 5.'], 'polar', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'polar', 'Which one of the following molecules has maximum dipole moment?', ['NF_{3}', 'CH_{4}', 'NH_{3}', 'PF_{5}'], 3,
    lambda: near([0.24, 0, 1.47, 0], 1.47), ['CH_{4}, PF_{5}: symmetric (0). NF_{3}: bond dipoles oppose the lone-pair dipole (0.24 D). NH_{3}: they add up (1.47 D) → maximum.'], 'polar', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'polar', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : NH_{3} and NF_{3} molecule have pyramidal shape with a lone pair of electrons on nitrogen atom. The resultant dipole moment of NH_{3} is greater than that of NF_{3}. Reason (R) : In NH_{3}, the orbital dipole due to lone pair is in the same direction as the resultant dipole moment of the N − H bonds. F is the most electronegative element. In the light of the above statements, choose the correct answer from the options given below :',
    AR, 1, lambda: 1, ['In NH_{3} the lone-pair and N−H dipoles point the same way (add); in NF_{3} the N−F dipoles point away from the lone pair (cancel partly). R explains A.'], 'polar', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'polar', 'Number of compounds from the following with zero dipole moment is ____. HF, H_{2}, H_{2}S, CO_{2}, NH_{3}, BF_{3}, CH_{4}, CHCl_{3}, SiF_{4}, H_{2}O, BeF_{2}',
    None, 6, lambda: sum(1 for d in ({'polar': True}, {'polar': False}, V('S', {'H': 2}), V('C', {'O': 2}), V('N', {'H': 3}), V('B', {'F': 3}), V('C', {'H': 4}), V('C', {'H': 1, 'Cl': 3}), V('Si', {'F': 4}), V('O', {'H': 2}), V('Be', {'F': 2})) if not d['polar']),
    ['μ = 0: H_{2}, CO_{2}, BF_{3}, CH_{4}, SiF_{4}, BeF_{2} → 6.', 'CHCl_{3} is tetrahedral but with mixed atoms → polar.'], 'polar', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'polar', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A): Cis form of alkene is found to be more polar than the trans form. Reason (R): Dipole moment of trans isomer of 2-butene is zero. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both (A) and (R) are true but (R) is NOT the correct explanation of (A)', '(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true'], 3, lambda: 3,
    ['In trans-2-butene the two C−CH_{3} bond dipoles point opposite ways and cancel (μ = 0); in cis they add. So cis is more polar, explained by R.'], 'polar', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'polar', 'Number of molecules from the following which can exhibit hydrogen bonding is ____. CH_{3}OH, H_{2}O, C_{2}H_{6}, C_{6}H_{6}, o-nitrophenol, HF, NH_{3}',
    None, 5, lambda: sum(1 for hasHon in (True, True, False, False, True, True, True) if hasHon), ['Need H on N, O or F: CH_{3}OH, H_{2}O, o-nitrophenol (intramolecular), HF, NH_{3} → 5.', 'C_{2}H_{6}, C_{6}H_{6}: H only on C.'], 'polar', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'polar', 'Arrange the following compounds in increasing order of their dipole moment : HBr, H_{2}S, NF_{3} and CHCl_{3}',
    ['CHCl_{3} < NF_{3} < HBr < H_{2}S', 'NF_{3} < HBr < H_{2}S < CHCl_{3}', 'H_{2}S < HBr < NF_{3} < CHCl_{3}', 'HBr < H_{2}S < NF_{3} < CHCl_{3}'], 2,
    lambda: (lambda d: pick(['CHCl_{3} < NF_{3} < HBr < H_{2}S', 'NF_{3} < HBr < H_{2}S < CHCl_{3}', 'H_{2}S < HBr < NF_{3} < CHCl_{3}', 'HBr < H_{2}S < NF_{3} < CHCl_{3}'], ' < '.join(sorted(d, key=d.get))))({'HBr': 0.82, 'H_{2}S': 0.95, 'NF_{3}': 0.24, 'CHCl_{3}': 1.04}),
    ['Measured μ (D): NF_{3} 0.24, HBr 0.82, H_{2}S 0.95, CHCl_{3} 1.04.'], 'polar', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'polar', 'Which of the following statement is true with respect to H_{2}O, NH_{3} and CH_{4} ? A. The central atoms of all the molecules are sp^{3} hybridized. B. The H−O−H, H−N−H and H−C−H angles in the above molecules are 104.5°, 107.5° and 109.5°, respectively. C. The increasing order of dipole moment is CH_{4} < NH_{3} < H_{2}O. D. Both H_{2}O and NH_{3} are Lewis acids and CH_{4} is a Lewis base. E. A solution of NH_{3} in H_{2}O is basic. In this solution NH_{3} and H_{2}O act as Lowry-Bronsted acid and base respectively. Choose the correct answer from the options given below:',
    ['C, D and E Only', 'A, B, C and E Only', 'A, B and C Only', 'A, D and E Only'], 3,
    lambda: 3 if all(V(c, {'H': n})['hyb'] == 'sp^{3}' for c, n in (('O', 2), ('N', 3), ('C', 4))) else 0,
    ['A ✓ (all steric number 4). B ✓ (more lone pairs → smaller angle). C ✓ (0 < 1.47 < 1.85 D).', 'D ✗ (H_{2}O, NH_{3} are Lewis BASES). E ✗ (NH_{3} is the base, H_{2}O the acid).'], 'polar', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'polar', 'Among H_{2}S, H_{2}O, NF_{3}, NH_{3} and CHCl_{3}, identify the molecule (X) with lowest dipole moment value. The number of lone pairs of electrons present on the central atom of the molecule (X) is :',
    ['2', '0', '1', '3'], 3, lambda: pick([2, 0, 1, 3], V('N', {'F': 3})['lp']), ['Lowest μ: NF_{3} (0.24 D). Its central N has 1 lone pair.'], 'polar', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'polar', 'Given below are statements about some molecules/ions. Identify the CORRECT statements. A. The dipole moment value of NF_{3} is higher than that of NH_{3}. B. The dipole moment value of BeH_{2} is zero. C. The bond order of O_{2}^{2−} and F_{2} is same. D. The formal charge on the central oxygen atom of ozone is −1. E. In NO_{2}, all the three atoms satisfy the octet rule, hence it is very stable. Choose the correct answer from the options given below :',
    ['A, B, C, D & E', 'B & C Only', 'B, C & D Only', 'A, C & D Only'], 2,
    lambda: 2 if (not V('Be', {'H': 2})['polar']) and mo('O', 'O', -2)['bo'] == mo('F', 'F')['bo'] else 0,
    ['A ✗ (NH_{3} 1.47 > NF_{3} 0.24). B ✓ (linear). C ✓ (both 1).', 'D ✗ (central O of O_{3} is +1). E ✗ (NO_{2} has 17 electrons — an odd-electron molecule).'], 'polar', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'polar', 'Given below are two statements : Statement I: F_{2}O < H_{2}O < Cl_{2}O is the correct trend in terms of bond angle. Statement II : SiF_{4}, SnF_{4} and PbF_{4} are ionic in nature. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 3, lambda: 3 if 103 < 104.5 < 111 else 0,
    ['Bond angles: OF_{2} ≈ 103°, H_{2}O 104.5°, Cl_{2}O ≈ 111° (big Cl atoms push apart) → I true.', 'SiF_{4} is a covalent gas (only SnF_{4}, PbF_{4} are ionic) → II false.'], 'polar', 2)

# ---------------- MO theory, bond order, magnetism ----------------
add(('2025', 'Apr', '2025-04-04', 1), 'mot', 'Which of the following molecule(s) show/s paramagnetic behavior? A. O_{2} B. N_{2} C. F_{2} D. S_{2} E. Cl_{2}. Choose the correct answer from the options given below:',
    ['A & E Only', 'B Only', 'A & C Only', 'A & D Only'], 4, lambda: pick(['AE', 'B', 'AC', 'AD'], ''.join(k for k, (a, b) in zip('ABCDE', [('O', 'O'), ('N', 'N'), ('F', 'F'), ('S', 'S'), ('Cl', 'Cl')]) if mo(a, b)['unpaired'] > 0)),
    ['O_{2} and S_{2} (same valence count) have two unpaired π* electrons → paramagnetic.', 'N_{2}, F_{2}, Cl_{2}: all paired.'], 'mot', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'mot', 'Number of molecules having bond order 2 from the following molecule is ____. C_{2}, O_{2}, Be_{2}, Li_{2}, Ne_{2}, N_{2}, He_{2}',
    ['8', '2', '4', '3'], 2, lambda: pick([8, 2, 4, 3], sum(1 for a in ('C', 'O', 'Be', 'Li', 'Ne', 'N', 'He') if mo(a, a)['bo'] == 2)), ['Bond orders: C_{2} 2, O_{2} 2, Be_{2} 0, Li_{2} 1, Ne_{2} 0, N_{2} 3, He_{2} 0 → 2 molecules.'], 'mot', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'mot', 'Total number of electron present in (π^{*}) molecular orbitals of O_{2}, O_{2}^{+} and O_{2}^{−} is', None, 6,
    lambda: mo('O', 'O')['pistar'] + mo('O', 'O', 1)['pistar'] + mo('O', 'O', -1)['pistar'], ['π* electrons: O_{2} 2, O_{2}^{+} 1, O_{2}^{−} 3 → 6.'], 'mot', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'mot', 'Given below are two statements : Statement (I) : The correct sequence of bond lengths in the following species is : O_{2}^{+} < O_{2} < O_{2}^{−} < O_{2}^{2−}. Statement (II) : The correct sequence of number of unpaired electrons in the following species is : O_{2} > O_{2}^{+} > O_{2}^{−} > O_{2}^{2−}. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 3,
    lambda: (lambda b, u: [1, 2, 3, 4][(0 if b else 2) + (0 if u else 1)] if False else (1 if b and u else 3 if b else 4 if u else 2))(
        [mo('O', 'O', q)['bo'] for q in (1, 0, -1, -2)] == sorted([mo('O', 'O', q)['bo'] for q in (1, 0, -1, -2)], reverse=True),
        all(x > y for x, y in zip([mo('O', 'O', q)['unpaired'] for q in (0, 1, -1, -2)], [mo('O', 'O', q)['unpaired'] for q in (1, -1, -2)]))),
    ['Bond orders 2.5, 2, 1.5, 1 → lengths increase in that order: I true.', 'Unpaired: O_{2} 2, O_{2}^{+} 1, O_{2}^{−} 1, O_{2}^{2−} 0 — O_{2}^{+} and O_{2}^{−} are EQUAL, so the strict order fails: II false.'], 'mot', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'mot', 'Which of the following linear combination of atomic orbitals will lead to formation of molecular orbitals in homonuclear diatomic molecules [internuclear axis in z-direction]? A. 2p_{z} and 2p_{x} B. 2s and 2p_{x} C. 3d_{xy} and 3d_{x^{2}−y^{2}} D. 2s and 2p_{z} E. 2p_{z} and 3d_{x^{2}−y^{2}}. Choose the correct answer from the options given below:',
    ['E Only', 'C and D Only', 'D Only', 'A and B Only'], 3, lambda: 3,
    ['Orbitals combine only if they have the same symmetry about the bond (z) axis.', '2s and 2p_{z} are both symmetric about z (σ) ✓. 2p_{x} with 2p_{z} or 2s: overlap cancels. d_{xy} and d_{x^{2}−y^{2}}: different symmetry (zero net overlap).'], 'mot', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'mot', 'Given below are two statements : Statement (I): Experimentally determined oxygen-oxygen bond lengths in the O_{3} are found to be same and the bond length is greater than that of a O=O (double bond) but less than that of a single (O−O) bond. Statement (II): The strong lone pair-lone pair repulsion between oxygen atoms is solely responsible for the fact that the bond length in ozone is smaller than that of a double bond (O=O) but more than that of a single bond (O−O). In the light of the above statements, choose the correct answer from the options given below :',
    ['Statement I is false but Statement II is true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true'], 3, lambda: 3,
    ['Ozone\'s two O−O bonds are equal (128 pm) and in between single (148) and double (121) — I true.', 'The cause is RESONANCE (bond order 1.5), not lone-pair repulsion; II also mis-states the comparison → false.'], 'mot', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'mot', 'Sum of bond order of CO and NO^{+} is', None, 6, lambda: round(mo('C', 'O')['bo'] + mo('N', 'O', 1)['bo']), ['CO and NO^{+} are isoelectronic with N_{2} (14 electrons): bond order 3 each → 6.'], 'mot', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'mot', 'Total number of molecules/species from following which will be paramagnetic is: O_{2}, O_{2}^{+}, O_{2}^{−}, NO, NO_{2}, CO, K_{2}[NiCl_{4}], [Co(NH_{3})_{6}]Cl_{3}, K_{2}[Ni(CN)_{4}]',
    None, 6, lambda: sum(1 for x in (mo('O', 'O')['unpaired'], mo('O', 'O', 1)['unpaired'], mo('O', 'O', -1)['unpaired'], mo('N', 'O')['unpaired'], 1, mo('C', 'O')['unpaired'], 2, 0, 0) if x > 0),
    ['O_{2}, O_{2}^{+}, O_{2}^{−}, NO (11 valence e^{−}), NO_{2} (odd electron) are paramagnetic; CO is not.', '[NiCl_{4}]^{2−}: tetrahedral Ni^{2+} d^{8}, 2 unpaired ✓; [Co(NH_{3})_{6}]^{3+} low-spin d^{6} and [Ni(CN)_{4}]^{2−} square planar d^{8} are diamagnetic → 6.'], 'mot', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'mot', 'The number of species from the following which are paramagnetic and with bond order equal to one is: H_{2}, He_{2}^{+}, O_{2}^{+}, N_{2}^{2−}, O_{2}^{2−}, F_{2}, Ne_{2}^{+}, B_{2}',
    None, 1, lambda: sum(1 for d in (mo('H', 'H'), mo('He', 'He', 1), mo('O', 'O', 1), mo('N', 'N', -2), mo('O', 'O', -2), mo('F', 'F'), mo('Ne', 'Ne', 1), mo('B', 'B')) if d['bo'] == 1 and d['unpaired'] > 0),
    ['Bond order 1: H_{2}, O_{2}^{2−}, F_{2}, B_{2}. Of these only B_{2} (π_{x}^{1}π_{y}^{1}) is paramagnetic → 1.'], 'mot', 2)
add(('2024', 'Jan', '2024-01-29', 2), 'mot', 'The total number of anti bonding molecular orbitals, formed from 2s and 2p atomic orbitals in a diatomic molecule is', None, 4, lambda: 1 + 3,
    ['2s + 2s → σ, σ*. Three 2p pairs → σ, σ*, two π, two π*.', 'Antibonding: σ*2s, σ*2p, π*2p_{x}, π*2p_{y} → 4.'], 'mot', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'polar', 'The total number of molecules with zero dipole moment among CH_{4}, BF_{3}, H_{2}O, HF, NH_{3}, CO_{2} and SO_{2} is',
    None, 3, lambda: sum(1 for d in (V('C', {'H': 4}), V('B', {'F': 3}), V('O', {'H': 2}), {'polar': True}, V('N', {'H': 3}), V('C', {'O': 2}), V('S', {'O': 2})) if not d['polar']), ['μ = 0: CH_{4}, BF_{3}, CO_{2} → 3. SO_{2} is bent (polar).'], 'polar', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'mot', 'The total number of molecular orbitals formed from 2s and 2p atomic orbitals of a diatomic molecule is ____.', None, 8, lambda: 2 * (1 + 3),
    ['Each atom brings 4 orbitals (2s + three 2p) → 8 atomic orbitals → 8 molecular orbitals.'], 'mot', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'mot', 'The linear combination of atomic orbitals to form molecular orbitals takes place only when the combining atomic orbitals A. have the same energy B. have the minimum overlap C. have same symmetry about the molecular axis D. have different symmetry about the molecular axis. Choose the most appropriate from the options given below:',
    ['A, B, C only', 'A and C only', 'B, C, D only', 'B and D only'], 2, lambda: 2, ['Conditions: comparable energy, same symmetry about the axis, MAXIMUM overlap → A and C.'], 'mot', 1)
add(('2026', 'Jan', '2026-01-24', 2), 'mot', 'Pair of species among the following having same bond order as well as paramagnetic character will be-',
    ['O_{2}^{+}, N_{2}^{2−}', 'O_{2}^{−}, N_{2}^{+}', 'O_{2}^{+}, N_{2}^{−}', 'O_{2}^{−}, N_{2}^{−}'], 3,
    lambda: [i + 1 for i, (a, b) in enumerate([(mo('O', 'O', 1), mo('N', 'N', -2)), (mo('O', 'O', -1), mo('N', 'N', 1)), (mo('O', 'O', 1), mo('N', 'N', -1)), (mo('O', 'O', -1), mo('N', 'N', -1))]) if a['bo'] == b['bo'] and a['unpaired'] and b['unpaired']][0],
    ['O_{2}^{+}: 2.5, 1 unpaired. N_{2}^{−}: 2.5, 1 unpaired → same.', 'N_{2}^{+} is 2.5 but O_{2}^{−} is 1.5; N_{2}^{2−} is 2.'], 'mot', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'mot', 'Given below are two statements: Statement I: The number of species among BF_{4}^{−}, SiF_{4}, XeF_{4} and SF_{4} that have unequal E−F bond lengths is two. Here, E is the central atom. Statement II: Among O_{2}^{−}, O_{2}^{2−}, F_{2} and O_{2}^{+}, O_{2}^{−} has the highest bond order. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 1,
    lambda: (lambda s1, s2: 1 if not s1 and not s2 else 0)(sum(1 for d in (V('B', {'F': 4}, -1), V('Si', {'F': 4}), V('Xe', {'F': 4}), V('S', {'F': 4})) if d['shape'] in ('see-saw', 'T-shaped')) == 2,
                                                          max([('O2-', mo('O', 'O', -1)['bo']), ('O22-', mo('O', 'O', -2)['bo']), ('F2', mo('F', 'F')['bo']), ('O2+', mo('O', 'O', 1)['bo'])], key=lambda t: t[1])[0] == 'O2-'),
    ['Only SF_{4} (see-saw) has two kinds of S−F bonds; the others are symmetric → one, not two: I false.', 'Bond orders: O_{2}^{−} 1.5, O_{2}^{2−} 1, F_{2} 1, O_{2}^{+} 2.5 → O_{2}^{+} is highest: II false.'], 'mot', 2)

# ---------------- Lewis structures, formal charge, bond parameters ----------------
add(('2026', 'Jan', '2026-01-22', 1), 'lewis', 'The formal charges on the atoms marked as (1) to (4) in the Lewis representation of HNO_{3} molecule H−O(1)−N(2)(=O(3))−O(4) respectively are',
    ['+1, 0, 0, −1', '0, −1, 0, +1', '0, +1, 0, −1', '0, 0, −1, +1'], 3,
    lambda: pick(['+1, 0, 0, −1', '0, −1, 0, +1', '0, +1, 0, −1', '0, 0, −1, +1'], ', '.join(('+' if f > 0 else '−' if f < 0 else '') + str(abs(f)) for f in (6 - 4 - 2, 5 - 0 - 4, 6 - 4 - 2, 6 - 6 - 1))),
    ['Formal charge = valence e^{−} − nonbonding e^{−} − bonds.', 'O(1): 6 − 4 − 2 = 0. N: 5 − 0 − 4 = +1. O(3) (double): 6 − 4 − 2 = 0. O(4) (single, 3 lone pairs): 6 − 6 − 1 = −1.'], 'lewis', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'lewis', 'Identify the molecule (X) with maximum number of lone pairs of electrons (obtained using Lewis dot structure) among HNO_{3}, H_{2}SO_{4}, NF_{3} and O_{3}. Choose the correct bond angle made by the central atom of the molecule (X).',
    ['120°', '107°', '102°', '116°'], 3,
    lambda: pick([120, 107, 102, 116], {'HNO_{3}': 120, 'H_{2}SO_{4}': 109, 'NF_{3}': 102, 'O_{3}': 116}[max({'HNO_{3}': 2 + 2 + 3, 'H_{2}SO_{4}': 4 * 2, 'NF_{3}': 3 * 3 + V('N', {'F': 3})['lp'], 'O_{3}': 2 + 3 + V('O', {'O': 2})['lp']}.items(), key=lambda t: t[1])[0]]),
    ['Lone pairs: HNO_{3} 7, H_{2}SO_{4} 8, NF_{3} 3 × 3 + 1 = 10, O_{3} 6 → NF_{3}.', 'F−N−F angle ≈ 102°.'], 'lewis', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'lewis', 'The covalent radii of atoms A and B are r_{A} and r_{B}, respectively. The covalent bond length and total length of AB molecule are respectively',
    ['(r_{A} + r_{B}), 2(r_{A} + r_{B})', '\\f{1}{2}(r_{A} + r_{B}), (r_{A} + r_{B})', '(r_{A} + r_{B}), (r_{A} + r_{B})', '2(r_{A} + r_{B}), \\f{1}{2}(r_{A} + r_{B})'], 1,
    lambda: 1, ['Bond length = distance between nuclei = r_{A} + r_{B}.', 'End to end: r_{A} (beyond A) + (r_{A} + r_{B}) + r_{B} (beyond B) = 2(r_{A} + r_{B}).'], 'lewis', 1)
for _p in P: _p['t'] = _p['fam']
