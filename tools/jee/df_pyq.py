"""Real JEE Main questions — Chemistry Unit 11: d- and f-Block Elements. Our own solutions; chk recomputes every
number from data — d-electron counts and unpaired electrons from the ion's charge (dblock.py), spin-only moments
μ = √(n(n + 2)), ionisation/atomisation/E° comparisons from NCERT tables, and redox titrations by balancing
electrons. Statement items are checked against a fact table. Complex-ion questions are filed in Unit 12, and
organic/analysis items that only mention KMnO₄ or K₂Cr₂O₇ in their units."""
import math
from common import new_registry, pick, verify
from chemkit import stmt, ar, pickset
from dblock import ATOM, E2, E32, IE1, IE2, IE3, d_count, unpaired, mu
P, add = new_registry()
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)
def n_of(ion):   # 'Fe3+' → unpaired electrons (high spin, free ion)
    m = ion.rstrip('+').rstrip('0123456789'); q = int(ion[len(m):-1] or 1); return unpaired(d_count(m, q))
def mu_of(ion): return mu(n_of(ion))
LAN = {'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'}
def f_ion(m, q):   # 4f electrons of a lanthanoid ion: neutral 4f^n 5d^0 6s2 (La, Ce, Gd, Lu also have 5d1)
    nf = {'La': 0, 'Ce': 1, 'Pr': 3, 'Nd': 4, 'Pm': 5, 'Sm': 6, 'Eu': 7, 'Gd': 7, 'Tb': 9, 'Dy': 10, 'Ho': 11, 'Er': 12, 'Tm': 13, 'Yb': 14, 'Lu': 14}[m]
    d5 = 1 if m in ('La', 'Ce', 'Gd', 'Lu') else 0; e = nf + d5 + 2 - q   # electrons left beyond [Xe]
    return min(e, 14) if e >= 0 else 0
def f_unp(k): return k if k <= 7 else 14 - k

# ---------------- magnetic moments and configurations ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'mag', 'The metal ions that have the calculated spin-only magnetic moment value of 4.9 B.M. are : A. Cr^{2+} B. Fe^{2+} C. Fe^{3+} D. Co^{2+} E. Mn^{3+}',
    ['B and E Only', 'A, C and E Only', 'A, B and E Only', 'A, D and E Only'], 3, lambda: pickset(['B and E Only', 'A, C and E Only', 'A, B and E Only', 'A, D and E Only'], {k: abs(mu_of(i) - 4.9) < 0.02 for k, i in zip('ABCDE', ['Cr2+', 'Fe2+', 'Fe3+', 'Co2+', 'Mn3+'])}),
    ['4.9 BM ↔ 4 unpaired electrons (√24).', 'Cr^{2+} d^{4}, Fe^{2+} d^{6}, Mn^{3+} d^{4} have 4; Fe^{3+} d^{5} has 5, Co^{2+} d^{7} has 3.'], 'mag', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'mag', 'Among Sc, Mn, Co and Cu, identify the element with highest enthalpy of atomisation. The spin only magnetic moment value of that element in its +2 oxidation state is ______ BM (in nearest integer).', None, 4,
    lambda: round(mu_of(max(['Sc', 'Mn', 'Co', 'Cu'], key=ATOM.get) + '2+')), ['Atomisation (kJ/mol): Sc 326, Mn 281, Co 425, Cu 339 → Co.', 'Co^{2+} is d^{7}: 3 unpaired → √15 = 3.87 ≈ 4 BM.'], 'mag', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'mag', 'Pair of transition metal ions having the same number of unpaired electrons is', ['Ti^{2+}, Co^{2+}', 'V^{2+}, Co^{2+}', 'Fe^{3+}, Cr^{2+}', 'Ti^{3+}, Mn^{2+}'], 2,
    lambda: pick([n_of('Ti2+') == n_of('Co2+'), n_of('V2+') == n_of('Co2+'), n_of('Fe3+') == n_of('Cr2+'), n_of('Ti3+') == n_of('Mn2+')], True), ['V^{2+} (d^{3}) and Co^{2+} (d^{7}) both have 3 unpaired electrons.', 'Ti^{2+} 2, Fe^{3+} 5, Cr^{2+} 4, Ti^{3+} 1, Mn^{2+} 5.'], 'mag', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'mag', 'A first row transition metal in its +2 oxidation state has a spin-only magnetic moment value of 3.86 BM. The atomic number of the metal is', ['25', '26', '22', '23'], 4,
    lambda: pick([25, 26, 22, 23], [{'Mn': 25, 'Fe': 26, 'Ti': 22, 'V': 23}[m] for m in ('Mn', 'Fe', 'Ti', 'V') if abs(mu_of(m + '2+') - 3.86) < 0.02][0]), ['3.86 BM ↔ 3 unpaired → d^{3} as M^{2+}.', 'd^{3} M^{2+} is V (Z = 23).'], 'mag', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'mag', 'A first row transition metal with highest enthalpy of atomisation, upon reaction with oxygen at high temperature forms oxides of formula M_{2}O_{n} (where n = 3, 4, 5). The \'spin-only\' magnetic moment value of the amphoteric oxide from the above oxides is ______ BM (near integer).', None, 0,
    lambda: round(mu(unpaired(d_count(max(ATOM, key=ATOM.get), 5)))), ['Highest atomisation: V (515 kJ/mol). Oxides V_{2}O_{3} (basic), V_{2}O_{4}, V_{2}O_{5} (amphoteric).', 'V^{5+} is d^{0} → 0 BM.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'mag', 'The number of complexes from the following with no electrons in the t_{2} orbital is: TiCl_{4}, [MnO_{4}]^{−}, [FeO_{4}]^{2−}, [FeCl_{4}]^{−}, [CoCl_{4}]^{2−}', ['3', '1', '4', '2'], 1,
    lambda: pick([3, 1, 4, 2], sum(1 for d in (d_count('Ti', 4), d_count('Mn', 7), d_count('Fe', 6), d_count('Fe', 3), d_count('Co', 2)) if d - min(d, 4) == 0)),
    ['All are tetrahedral: the lower e set (2 orbitals, up to 4 electrons) fills before t_{2}.', 'TiCl_{4} d^{0}, MnO_{4}^{−} d^{0}, FeO_{4}^{2−} d^{2} (e^{2}) → no t_{2} electrons; FeCl_{4}^{−} d^{5} and CoCl_{4}^{2−} d^{7} have some → 3.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'mag', 'The fusion of chromite ore with sodium carbonate in the presence of air leads to the formation of products A and B along with the evolution of CO_{2}. The sum of spin-only magnetic moment values of A and B is ______ B.M. (Nearest integer)', None, 6,
    lambda: round(mu(unpaired(d_count('Cr', 6))) + mu(unpaired(d_count('Fe', 3)))), ['4FeCr_{2}O_{4} + 8Na_{2}CO_{3} + 7O_{2} → 8Na_{2}CrO_{4} + 2Fe_{2}O_{3} + 8CO_{2}.', 'CrO_{4}^{2−}: Cr^{6+} d^{0} → 0; Fe_{2}O_{3}: Fe^{3+} d^{5} → 5.92. Sum ≈ 6.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'mag', 'The spin only magnetic moment value of the ion among Ti^{2+}, V^{2+}, Co^{3+} and Cr^{2+}, that acts as strong oxidising agent in aqueous solution is ______ BM (Near integer).', None, 5,
    lambda: round(mu_of(max([('Co', 'Co3+')], key=lambda x: E32[x[0]])[1])), ['Co^{3+}/Co^{2+} E° = +1.97 V: Co^{3+} is the strong oxidant (the others are reductants).', 'Co^{3+} d^{6} (aqueous, high spin): 4 unpaired → 4.90 ≈ 5 BM.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'mag', 'Among VO_{2}^{+}, MnO_{4}^{−} and Cr_{2}O_{7}^{2−}, the spin-only magnetic moment value of the species with least oxidising ability is ______ BM (Nearest integer).', None, 0,
    lambda: round(mu(unpaired(d_count('V', 5)))), ['Oxidising power: MnO_{4}^{−} (1.51 V) > Cr_{2}O_{7}^{2−} (1.33 V) > VO_{2}^{+} (1.0 V).', 'VO_{2}^{+}: V^{5+} d^{0} → 0 BM.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'mag', 'The difference in the \'spin-only\' magnetic moment values of KMnO_{4} and the manganese product formed during titration of KMnO_{4} against oxalic acid in acidic medium is ______ BM. (nearest integer)', None, 6,
    lambda: round(abs(mu(unpaired(d_count('Mn', 2))) - mu(unpaired(d_count('Mn', 7))))), ['In acid, MnO_{4}^{−} (Mn^{7+}, d^{0}, 0 BM) → Mn^{2+} (d^{5}, 5.92 BM).', 'Difference ≈ 6.'], 'mag', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'mag', 'Among CrO, Cr_{2}O_{3} and CrO_{3}, the sum of spin-only magnetic moment values of basic and amphoteric oxides is ______ × 10^{−2} BM (nearest integer). (Given atomic number of Cr is 24)', None, 877,
    lambda: round((mu(unpaired(d_count('Cr', 2))) + mu(unpaired(d_count('Cr', 3)))) * 100), ['CrO (basic): Cr^{2+} d^{4} → 4.90; Cr_{2}O_{3} (amphoteric): Cr^{3+} d^{3} → 3.87.', 'Sum = 8.77 BM = 877 × 10^{−2}.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-08', 1), 'mag', 'The \'spin only\' magnetic moment value of MO_{4}^{2−} is ______ BM. (Where M is a metal having least metallic radii among Sc, Ti, V, Cr, Mn and Zn).', None, 0,
    lambda: round(mu(unpaired(d_count(min({'Sc': 164, 'Ti': 147, 'V': 135, 'Cr': 129, 'Mn': 137, 'Zn': 137}, key={'Sc': 164, 'Ti': 147, 'V': 135, 'Cr': 129, 'Mn': 137, 'Zn': 137}.get), 6)))),
    ['Metallic radii (pm): Sc 164, Ti 147, V 135, Cr 129, Mn 137, Zn 137 → Cr is smallest.', 'CrO_{4}^{2−}: Cr^{6+} d^{0} → 0 BM.'], 'mag', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'mag', 'A transition metal \'M\' among Sc, Ti, V, Cr, Mn and Fe has the highest second ionisation enthalpy. The spin only magnetic moment value of M^{+} ion is ______ BM (Near integer)', None, 6,
    lambda: round(mu(unpaired(d_count(max(['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe'], key=IE2.get), 1)))), ['IE_{2} is highest for Cr (1592 kJ/mol): Cr^{+} is 3d^{5}, so removing a second electron breaks a half-filled set.', 'Cr^{+} 3d^{5}: 5 unpaired → 5.92 ≈ 6 BM.'], 'mag', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'mag', 'Identify the metal ions among Co^{2+}, Ni^{2+}, Fe^{2+}, V^{3+} and Ti^{2+} having a spin-only magnetic moment value more than 3.0 BM. The sum of unpaired electrons present in the high spin octahedral complexes formed by those metal ions is ______', None, 7,
    lambda: sum(n_of(i) for i in ['Co2+', 'Ni2+', 'Fe2+', 'V3+', 'Ti2+'] if mu_of(i) > 3.0), ['μ > 3 BM needs ≥ 3 unpaired: Co^{2+} (d^{7}, 3) and Fe^{2+} (d^{6}, 4); Ni^{2+}, V^{3+}, Ti^{2+} have 2.', 'Sum = 3 + 4 = 7.'], 'mag', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'mag', 'Match List-I (transition metal ion) with List-II (spin only magnetic moment, B.M.): (A) Ti^{3+} (B) V^{2+} (C) Ni^{2+} (D) Sc^{3+}; (I) 3.87 (II) 0.00 (III) 1.73 (IV) 2.84',
    ['(A)-(IV), (B)-(II), (C)-(II), (D)-(I)', '(A)-(II), (B)-(IV), (C)-(I), (D)-(III)', '(A)-(III), (B)-(I), (C)-(II), (D)-(IV)', '(A)-(III), (B)-(I), (C)-(IV), (D)-(II)'], 4,
    lambda: pick(['IV II II I', 'II IV I III', 'III I II IV', 'III I IV II'], ' '.join({3.87: 'I', 0.0: 'II', 1.73: 'III', 2.83: 'IV'}[round(mu_of(i), 2)] for i in ['Ti3+', 'V2+', 'Ni2+', 'Sc3+'])),
    ['Ti^{3+} d^{1} → 1.73; V^{2+} d^{3} → 3.87; Ni^{2+} d^{8} → 2.83; Sc^{3+} d^{0} → 0.'], 'mag', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'mag', 'Which of the following electronic configuration would be associated with the highest magnetic moment?', ['[Ar]3d^{7}', '[Ar]3d^{8}', '[Ar]3d^{3}', '[Ar]3d^{6}'], 4,
    lambda: pick([unpaired(7), unpaired(8), unpaired(3), unpaired(6)], max(unpaired(d) for d in (7, 8, 3, 6))), ['Unpaired: d^{7} 3, d^{8} 2, d^{3} 3, d^{6} 4.', 'd^{6} has the most → highest moment.'], 'mag', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'mag', 'The spin only magnetic moment (μ) value (B.M.) of the compound with strongest oxidising power among Mn_{2}O_{3}, TiO and VO is ______ B.M. (Nearest integer).', None, 5,
    lambda: round(mu(unpaired(d_count('Mn', 3)))), ['Mn^{3+} (E° Mn^{3+}/Mn^{2+} = +1.57 V) is a strong oxidant; Ti^{2+} and V^{2+} are reductants.', 'Mn^{3+} d^{4}: 4 unpaired → 4.90 ≈ 5 BM.'], 'mag', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'mag', 'Match List-I (complex ion) with List-II (calculated spin only magnetic moment, BM): A. [Cr(H_{2}O)_{6}]^{2+} B. [Co(H_{2}O)_{6}]^{2+} C. [Cu(H_{2}O)_{6}]^{2+} D. [Mn(H_{2}O)_{6}]^{2+}; I. 3.87 II. 5.92 III. 4.90 IV. 1.73',
    ['A-I, B-III, C-IV, D-II', 'A-II, B-I, C-III, D-IV', 'A-IV, B-II, C-I, D-III', 'A-III, B-I, C-IV, D-II'], 4,
    lambda: pick(['I III IV II', 'II I III IV', 'IV II I III', 'III I IV II'], ' '.join({3.87: 'I', 5.92: 'II', 4.9: 'III', 1.73: 'IV'}[round(mu_of(i), 2)] for i in ['Cr2+', 'Co2+', 'Cu2+', 'Mn2+'])),
    ['Water is a weak-field ligand: high spin.', 'Cr^{2+} d^{4} 4.90; Co^{2+} d^{7} 3.87; Cu^{2+} d^{9} 1.73; Mn^{2+} d^{5} 5.92.'], 'mag', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'mag', 'Statement I: Presence of large number of unpaired electrons in transition metal atoms results in higher enthalpies of their atomisation. Statement II: d_{xy} = d_{xz} = d_{yz} < d_{x^{2}−y^{2}} = d_{z^{2}} and d_{x^{2}−y^{2}} = d_{z^{2}} < d_{xy} = d_{xz} = d_{yz} are the d-orbital splittings in [Fe(H_{2}O)_{6}]^{3+} and [Ni(Cl)_{4}]^{2−} complex ions respectively.',
    ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct'], 1,
    lambda: stmt(ATOM['V'] > ATOM['Zn'] and ATOM['Cr'] > ATOM['Cu'], True, ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct']),
    ['More unpaired d electrons → stronger metallic bonding → higher atomisation (V 515 vs Zn 126 kJ/mol): I correct.', 'Octahedral: t_{2g} below e_{g}; tetrahedral [NiCl_{4}]^{2−}: e below t_{2}: II correct.'], 'mag', 2)

# ---------------- general trends and properties ----------------
SAa = ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true']
add(('2024', 'Feb', '2024-02-01', 2), 'trend', 'The transition metal having highest 3^{rd} ionisation enthalpy is :', ['Cr', 'Mn', 'V', 'Fe'], 2, lambda: pick(['Cr', 'Mn', 'V', 'Fe'], max(['Cr', 'Mn', 'V', 'Fe'], key=IE3.get)),
    ['IE_{3} (kJ/mol): V 2833, Cr 2990, Mn 3260, Fe 2962.', 'Mn^{2+} is d^{5}: taking the third electron breaks a half-filled set → Mn highest.'], 'trend', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'trend', 'Statement (I) : Both metal and non-metal exist in p and d-block elements. Statement (II) : Non-metals have higher ionisation enthalpy and higher electronegativity than the metals.',
    ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are true'], 2,
    lambda: stmt(False, True, SAa), ['The d-block contains only metals (non-metals are only in s/p blocks): I false.', 'Non-metals hold electrons more tightly — higher IE and EN: II true.'], 'trend', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'trend', 'The first transition series metal \'M\' has the highest enthalpy of atomisation in its series. One of its aquated ion (M^{n+}) exists in green colour. The nature of the oxide formed by the above M^{n+} ion is:', ['amphoteric', 'neutral', 'basic', 'acidic'], 3,
    lambda: pick(['amphoteric', 'neutral', 'basic', 'acidic'], {2: 'basic', 3: 'basic', 4: 'amphoteric', 5: 'amphoteric'}[{'V': 3}[max(ATOM, key=ATOM.get)]]),
    ['Highest atomisation: V. [V(H_{2}O)_{6}]^{3+} is green.', 'V_{2}O_{3} (V^{3+}, low oxidation state) is basic.'], 'trend', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'trend', 'Statement I : The higher oxidation states are more stable down the group among transition elements unlike p-block elements. Statement II : Copper can not liberate hydrogen from weak acids.',
    ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false'], 3,
    lambda: stmt(True, E2['Cu'] > 0, ['Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false']),
    ['Mo(VI), W(VI) are more stable than Cr(VI) — the reverse of the p-block inert-pair trend: I true.', 'E°(Cu^{2+}/Cu) = +0.34 V > 0: Cu cannot displace H_{2} from acids: II true.'], 'trend', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'trend', 'The electronic configuration of Cu(II) is 3d^{9} whereas that of Cu(I) is 3d^{10}. Which of the following is correct?',
    ['Cu(II) is less stable', 'Stability of Cu(I) and Cu(II) depends on nature of copper salts', 'Cu(II) is more stable', 'Cu(I) and Cu(II) are equally stable'], 3, lambda: 3 if -2100 < -1500 else 0,
    ['In water Cu^{+} disproportionates: 2Cu^{+} → Cu^{2+} + Cu.', 'The much larger hydration enthalpy of Cu^{2+} (≈ −2100 kJ/mol vs −580) more than repays the second IE: Cu(II) is more stable.'], 'trend', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'trend', 'Yellow compound of lead chromate gets dissolved on treatment with hot NaOH solution. The product of lead formed is a :',
    ['Tetraanionic complex with coordination number six', 'Neutral complex with coordination number four', 'Dianionic complex with coordination number six', 'Dianionic complex with coordination number four'], 4,
    lambda: pick([(-4, 6), (0, 4), (-2, 6), (-2, 4)], (2 - 4 * 1, 4)), ['PbCrO_{4} + 4OH^{−} → [Pb(OH)_{4}]^{2−} + CrO_{4}^{2−}.', 'Pb^{2+} + 4OH^{−}: charge 2 − 4 = −2, coordination number 4.'], 'trend', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'trend', 'The correct IUPAC name of K_{2}MnO_{4} is', ['Potassium tetraoxopermanganate (VI)', 'Potassium tetraoxidomanganate (VI)', 'Dipotassium tetraoxidomanganate (VII)', 'Potassium tetraoxidomanganese (VI)'], 2,
    lambda: pick(['oxo', 'oxido VI', 'oxido VII', 'manganese'], 'oxido ' + {6: 'VI', 7: 'VII'}[8 - 2]), ['Mn: 2(+1) + x + 4(−2) = 0 → x = +6.', 'Anionic complex: "-ate" ending on manganese; O^{2−} ligand is "oxido" → potassium tetraoxidomanganate(VI).'], 'trend', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'trend', 'Which of the following is NOT a physical or chemical characteristics of interstitial compounds?',
    ['They have high melting points, higher than those of pure metals.', 'They are very soft and ionic in nature.', 'They retain metallic conductivity.', 'They are chemically inert and usually non-stoichiometric.'], 2, lambda: 2,
    ['Interstitial compounds (TiC, Mn_{4}N, Fe_{3}H …) have small atoms in the metal lattice.', 'They are very HARD, high-melting, metallic conductors, inert and non-stoichiometric — not soft or ionic.'], 'trend', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'trend', 'The correct statements among the following are. A. Basic vanadium oxide is used in the manufacture of H_{2}SO_{4}. B. The spin-only magnetic moment value of the transition metal halide employed in Ziegler-Natta polymerization is 2.84 BM. C. The p-block metal compound employed in Ziegler-Natta polymerization has the metal in +3 oxidation state. D. The number of electrons present in the outer most \'d\' orbital of metal halide employed in Wacker process is 8.',
    ['A and B only', 'A, C and D only', 'C and D Only', 'B, C and D only'], 3,
    lambda: pickset(['A and B only', 'A, C and D only', 'C and D Only', 'B, C and D only'], dict(A=False, B=abs(mu(unpaired(d_count('Ti', 4))) - 2.84) < 0.05, C=True, D=(10 - 2) == 8)),
    ['A ✗: V_{2}O_{5} (contact process) is amphoteric, not basic. B ✗: TiCl_{4} is Ti^{4+} d^{0} → 0 BM.', 'C ✓: Al(C_{2}H_{5})_{3}, Al is +3. D ✓: PdCl_{2}, Pd^{2+} is 4d^{8}.'], 'trend', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'trend', 'Statement I: First row transition metals which act as catalyst utilise their 3d electrons only for formation of bonds between reactant molecules and atoms on the surface of catalyst. Statement II: There is increase in the concentration of reactants on the surface of catalyst which strengthens the bonds in reacting molecules.',
    ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct'], 2,
    lambda: stmt(False, False, ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct']),
    ['Surface bonding uses 3d AND 4s electrons: I incorrect.', 'Adsorption raises surface concentration but WEAKENS bonds in the reactants (lowering E_{a}): II incorrect.'], 'trend', 1)

# ---------------- KMnO4, K2Cr2O7 and redox ----------------
E = {'MnO4-/Mn2+': 1.51, 'Cr2O7/Cr3+': 1.33, 'Fe3+/Fe2+': 0.77, 'I2/I-': 0.54, 'S/S2-': 0.14, 'Sn4+/Sn2+': 0.15, 'SO4/SO2': 0.17, 'NO3-/NO2-': 0.94, 'IO3-/I-': 1.09, 'SO4/S2O3': 0.08}
def oxidises(ox, red): return E[ox] > E[red]   # can ox (as written) oxidise the reduced form of red?
add(('2025', 'Apr', '2025-04-03', 2), 'oxo', 'Compounds that should not be used as primary standards in titrimetric analysis are : A. Na_{2}Cr_{2}O_{7} B. Oxalic acid C. NaOH D. FeSO_{4}·6H_{2}O E. Sodium tetraborate',
    ['B and D Only', 'C, D and E Only', 'A, C and D Only', 'D and E Only'], 3, lambda: pickset(['B and D Only', 'C, D and E Only', 'A, C and D Only', 'D and E Only'], dict(A=True, B=False, C=True, D=True, E=False)),
    ['A primary standard must be pure, stable in air, non-hygroscopic.', 'Na_{2}Cr_{2}O_{7} and NaOH absorb moisture (NaOH also CO_{2}); FeSO_{4} is oxidised by air → A, C, D. Oxalic acid and borax are standards.'], 'oxo', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'oxo', 'Only 2 mL of KMnO_{4} solution of unknown molarity is required to reach the end point of a titration of 20 mL of oxalic acid (2M) in acidic medium. The molarity of KMnO_{4} solution should be ______ M.', None, 8,
    lambda: round(0.020 * 2 * 2 / 5 / 0.002), ['2MnO_{4}^{−} + 5C_{2}O_{4}^{2−} + 16H^{+} → 2Mn^{2+} + 10CO_{2} + 8H_{2}O.', 'Oxalic acid 0.04 mol → MnO_{4}^{−} 0.016 mol in 2 mL → 8 M.'], 'oxo', 1)
SAb = ['Both Statement I and Statement II is true', 'Both Statement I and Statement II is false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
add(('2024', 'Apr', '2024-04-08', 2), 'oxo', 'Statement (I) : Fusion of MnO_{2} with KOH and an oxidising agent gives dark green K_{2}MnO_{4}. Statement (II) : Manganate ion on electrolytic oxidation in alkaline medium gives permanganate ion.',
    SAb, 1, lambda: stmt(True, True, SAb), ['2MnO_{2} + 4KOH + O_{2} → 2K_{2}MnO_{4} (green) + 2H_{2}O: I true.', 'MnO_{4}^{2−} → MnO_{4}^{−} + e^{−} at the anode (alkaline): II true.'], 'oxo', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'oxo', 'Identify the incorrect statements regarding primary standard of titrimetric analysis (A) It should be purely available in dry form. (B) It should not undergo chemical change in air. (C) It should be hygroscopic and should react with another chemical instantaneously and stoichiometrically. (D) It should be readily soluble in water. (E) KMnO_{4} & NaOH can be used as primary standard.',
    ['(C) and (D) only', '(B) and (E) only', '(A) and (B) only', '(C) and (E) only'], 4, lambda: pickset(['(C) and (D) only', '(B) and (E) only', '(A) and (B) only', '(C) and (E) only'], dict(A=False, B=False, C=True, D=False, E=True)),
    ['A primary standard must NOT be hygroscopic: C is wrong.', 'KMnO_{4} (decomposes, has MnO_{2}) and NaOH (absorbs H_{2}O, CO_{2}) are secondary standards: E is wrong.'], 'oxo', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'oxo', 'Which of the following sets includes all the species that will change the orange colour of K_{2}Cr_{2}O_{7} in acidic medium?',
    ['Fe^{2+}, Sn^{2+}, I^{−}, S^{2−}', 'S^{2−}, Fe^{3+}, I^{−}, C_{2}O_{4}^{2−}', 'Fe^{2+}, NO_{2}^{−}, SO_{2}, Sn^{4+}', 'Fe^{3+}, SO_{4}^{2−}, S^{2−}, Sn^{4+}'], 1,
    lambda: pick([all(x for x in s) for s in [[oxidises('Cr2O7/Cr3+', r) for r in ('Fe3+/Fe2+', 'Sn4+/Sn2+', 'I2/I-', 'S/S2-')], [True, False, True, True], [True, True, True, False], [False, False, True, False]]], True),
    ['Only reducing agents turn Cr_{2}O_{7}^{2−} (orange) into Cr^{3+} (green).', 'Fe^{2+}, Sn^{2+}, I^{−}, S^{2−} are all reducing; Fe^{3+}, Sn^{4+}, SO_{4}^{2−} are already fully oxidised.'], 'oxo', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'oxo', 'Consider the following statements about manganate and permanganate ions. A. The geometry of both manganate and permanganate ions is tetrahedral. B. The oxidation states of Mn in manganate and permanganate are +7 and +6, respectively. C. Oxidation of Mn(II) salt by peroxodisulphate gives manganate ion as the final product. D. Manganate ion is paramagnetic and permanganate ions is diamagnetic. E. Acidified permanganate ion reduces oxalate, nitrite and iodide ions.',
    ['A, C and D Only', 'A and D Only', 'A, B and C Only', 'A, D and E Only'], 2, lambda: pickset(['A, C and D Only', 'A and D Only', 'A, B and C Only', 'A, D and E Only'], dict(A=True, B=False, C=False, D=unpaired(d_count('Mn', 6)) > 0 and unpaired(d_count('Mn', 7)) == 0, E=False)),
    ['A ✓ (both tetrahedral). B ✗ (manganate +6, permanganate +7). C ✗ (S_{2}O_{8}^{2−} gives permanganate).', 'D ✓ (MnO_{4}^{2−} d^{1}, MnO_{4}^{−} d^{0}). E ✗: permanganate OXIDISES them.'], 'oxo', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'oxo', 'On heating a mixture of common salt and K_{2}Cr_{2}O_{7} in equal amount along with concentrated H_{2}SO_{4} in a test tube, a gas is evolved. Formula of the gas evolved and oxidation state of the central metal atom in the gas respectively are:',
    ['CrO_{2}Cl_{2} and +5', 'CrO_{2}Cl_{2} and +6', 'Cr_{2}O_{2}Cl_{2} and +6', 'Cr_{2}O_{2}Cl_{2} and +3'], 2, lambda: pick([('CrO2Cl2', 5), ('CrO2Cl2', 6), ('Cr2O2Cl2', 6), ('Cr2O2Cl2', 3)], ('CrO2Cl2', 0 + 2 * 2 + 2 * 1)),
    ['Chromyl chloride test: K_{2}Cr_{2}O_{7} + 4NaCl + 6H_{2}SO_{4} → 2CrO_{2}Cl_{2}↑ (red vapour) + …', 'In CrO_{2}Cl_{2}: x − 4 − 2 = 0 → +6.'], 'oxo', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'oxo', 'Consider the following reactions: K_{2}Cr_{2}O_{7} —(KOH, −H_{2}O)→ [A] —(H_{2}SO_{4}, −H_{2}O)→ [B] + K_{2}SO_{4}. The products [A] and [B], respectively are :',
    ['K_{2}Cr(OH)_{6} and Cr_{2}O_{3}', 'K_{2}CrO_{4} and CrO', 'K_{2}CrO_{4} and Cr_{2}O_{3}', 'K_{2}CrO_{4} and K_{2}Cr_{2}O_{7}'], 4, lambda: 4,
    ['In alkali dichromate becomes chromate: Cr_{2}O_{7}^{2−} + 2OH^{−} → 2CrO_{4}^{2−} + H_{2}O.', 'Acid reverses it: 2CrO_{4}^{2−} + 2H^{+} → Cr_{2}O_{7}^{2−} + H_{2}O (Cr stays +6, no redox).'], 'oxo', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'oxo', 'Preparation of potassium permanganate from MnO_{2} involves two step process in which the 1st step is a reaction with KOH and KNO_{3} to produce', ['K_{2}MnO_{4}', 'K_{3}MnO_{4}', 'K_{4}[Mn(OH)_{6}]', 'KMnO_{4}'], 1, lambda: 1,
    ['Fusing MnO_{2} with KOH and an oxidant (KNO_{3}) gives green potassium manganate K_{2}MnO_{4} (Mn +6).', 'Step 2 (oxidation/disproportionation) gives KMnO_{4}.'], 'oxo', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'oxo', 'Which of the following oxidation reactions are carried out by both K_{2}Cr_{2}O_{7} and KMnO_{4} in acidic medium? A. I^{−} → I_{2} B. S^{2−} → S C. Fe^{2+} → Fe^{3+} D. I^{−} → IO_{3}^{−} E. S_{2}O_{3}^{2−} → SO_{4}^{2−}',
    ['B, C and D Only', 'A, D and E Only', 'C, D and E Only', 'A, B and C Only'], 4, lambda: pickset(['B, C and D Only', 'A, D and E Only', 'C, D and E Only', 'A, B and C Only'], dict(A=True, B=True, C=True, D=False, E=False)),
    ['In acid both oxidise I^{−} to I_{2}, S^{2−} to S and Fe^{2+} to Fe^{3+}.', 'I^{−} → IO_{3}^{−} is done by KMnO_{4} in neutral/alkaline medium, and S_{2}O_{3}^{2−} → SO_{4}^{2−} by KMnO_{4} in neutral medium — not by dichromate.'], 'oxo', 2)
def _mno4_moles():
    e = {'FeC2O4': 1 + 2, 'Fe2(C2O4)3': 0 + 3 * 2, 'FeSO4': 1, 'Fe2(SO4)3': 0}   # electrons released per mole when fully oxidised
    return sum(e.values()) / 5
add(('2026', 'Apr', '2026-04-04', 1), 'oxo', 'In order to oxidise a mixture of 1 mole each of FeC_{2}O_{4}, Fe_{2}(C_{2}O_{4})_{3}, FeSO_{4} and Fe_{2}(SO_{4})_{3} in acidic medium, the number of moles of KMnO_{4} required is', ['3', '2', '5', '7'], 2,
    lambda: pick([3, 2, 5, 7], _mno4_moles()), ['Electrons given up: FeC_{2}O_{4} 1 + 2 = 3; Fe_{2}(C_{2}O_{4})_{3} 3 × 2 = 6; FeSO_{4} 1; Fe_{2}(SO_{4})_{3} 0 → 10.', 'Each MnO_{4}^{−} takes 5 → 2 mol.'], 'oxo', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'oxo', 'Correct statements from the following are A. Potassium dichromate is an oxidising agent and it oxidises FeSO_{4} to Fe_{2}(SO_{4})_{3} in acidic medium. B. Sodium dichromate can be used as primary standard in volumetric estimation. C. CrO_{4}^{2−} and Cr_{2}O_{7}^{2−} are interconvertible in aqueous solution by varying the pH of the solution. D. Cr−O−Cr bond angle in Cr_{2}O_{7}^{2−} is 126°.',
    ['A, B and C Only', 'A, C and D Only', 'A and C Only', 'B and D Only'], 2, lambda: pickset(['A, B and C Only', 'A, C and D Only', 'A and C Only', 'B and D Only'], dict(A=oxidises('Cr2O7/Cr3+', 'Fe3+/Fe2+'), B=False, C=True, D=True)),
    ['A ✓; B ✗ (Na_{2}Cr_{2}O_{7} is hygroscopic — K_{2}Cr_{2}O_{7} is the standard).', 'C ✓ (pH-controlled equilibrium); D ✓ (Cr−O−Cr ≈ 126°).'], 'oxo', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'oxo', 'Identify correct statements from below: A. The chromate ion is square planar. B. Dichromates are generally prepared from chromates. C. The green manganate ion is diamagnetic. D. Dark green coloured K_{2}MnO_{4} disproportionates in a neutral or acidic medium to give permanganate. E. With increasing oxidation number of transition metal, ionic character of the oxides decreases.',
    ['B, C, D only', 'A, D, E only', 'A, B, C only', 'B, D, E only'], 4, lambda: pickset(['B, C, D only', 'A, D, E only', 'A, B, C only', 'B, D, E only'], dict(A=False, B=True, C=unpaired(d_count('Mn', 6)) == 0, D=True, E=True)),
    ['A ✗ (CrO_{4}^{2−} is tetrahedral); B ✓; C ✗ (MnO_{4}^{2−} is d^{1}, paramagnetic).', 'D ✓ (3MnO_{4}^{2−} + 4H^{+} → 2MnO_{4}^{−} + MnO_{2} + 2H_{2}O); E ✓ (higher oxidation state → more covalent, acidic oxides).'], 'oxo', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'oxo', 'Statement I: Sodium dichromate and potassium dichromate are classified as primary standards in titrimetric analysis. Statement II: Phenolphthalein is a weak base, therefore it dissociates in acidic medium.',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 2,
    lambda: stmt(False, False, ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']),
    ['Na_{2}Cr_{2}O_{7} is hygroscopic, so not a primary standard: I false.', 'Phenolphthalein is a weak ACID that ionises (turns pink) in basic medium: II false.'], 'oxo', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'oxo', 'A paper dipped in a dil. H_{2}SO_{4} solution of \'X\' upon treatment with SO_{2} gas turns into green. The compound \'X\' is :', ['KI-starch', 'KMnO_{4}', 'Pb(CH_{3}COO)_{2}', 'K_{2}Cr_{2}O_{7}'], 4,
    lambda: 4 if oxidises('Cr2O7/Cr3+', 'SO4/SO2') else 0, ['SO_{2} reduces acidified dichromate: orange Cr_{2}O_{7}^{2−} → green Cr^{3+}.', '(KMnO_{4} would be decolourised, not turned green.)'], 'oxo', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'oxo', 'The oxidation state of chromium in the final product formed in the reaction between KI and acidified K_{2}Cr_{2}O_{7} solution is:', ['+4', '+3', '+2', '+6'], 2,
    lambda: pick([4, 3, 2, 6], 6 - 6 // 2), ['Cr_{2}O_{7}^{2−} + 14H^{+} + 6I^{−} → 2Cr^{3+} + 3I_{2} + 7H_{2}O.', 'Each Cr gains 3 electrons: +6 → +3.'], 'oxo', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'oxo', 'X and Y are the number of electrons involved, respectively during the oxidation of I^{−} to I_{2} and S^{2−} to S by acidified K_{2}Cr_{2}O_{7} (per mole of dichromate). The value of X + Y is ______ .', None, 12,
    lambda: 6 + 6, ['Each Cr_{2}O_{7}^{2−} accepts 6 electrons (2 Cr: +6 → +3).', '6I^{−} → 3I_{2} and 3S^{2−} → 3S each release 6 electrons → X + Y = 12.'], 'oxo', 2)
def _iod(V_mn, M_mn, V_ki, M_ki, M_th=None, V_th=None):
    e = min(V_mn * M_mn * 3, V_ki * M_ki)   # basic medium: MnO4- + 3e- → MnO2; iodide gives one electron each
    I2 = e / 2; th = 2 * I2
    return th / V_th if M_th is None else th / M_th
add(('2026', 'Apr', '2026-04-06', 2), 'oxo', '500 mL of 0.2 M MnO_{4}^{−} solution in basic medium when mixed with 500 mL of 1.5 M KI solution, oxidises iodide ions to liberate molecular iodine. This liberated iodine is then titrated with a standard x M thiosulphate solution in presence of starch till the end point. If 300 mL of thiosulphate was consumed, then the value of x is ______.', None, 1,
    lambda: round(_iod(0.5, 0.2, 0.5, 1.5, V_th=0.3), 6), ['Basic medium: MnO_{4}^{−} + 3e^{−} → MnO_{2}: 0.1 mol takes 0.3 mol e^{−} from I^{−} (0.75 mol, in excess) → 0.15 mol I_{2}.', 'I_{2} + 2S_{2}O_{3}^{2−}: 0.3 mol thiosulphate in 0.3 L → 1 M.'], 'oxo', 3)
add(('2026', 'Jan', '2026-01-28', 1), 'oxo', '500 mL of 1.2 M KI solution is mixed with 500 mL of 0.2 M KMnO_{4} solution in basic medium. The liberated iodine was titrated with standard 0.1 M Na_{2}S_{2}O_{3} solution in the presence of starch indicator till the blue color disappeared. The volume (in L) of Na_{2}S_{2}O_{3} consumed is ______ . (Nearest integer)', None, 3,
    lambda: round(_iod(0.5, 0.2, 0.5, 1.2, M_th=0.1)), ['0.1 mol MnO_{4}^{−} (→ MnO_{2}) takes 0.3 mol e^{−}; KI (0.6 mol) is in excess → 0.15 mol I_{2}.', 'Thiosulphate needed 0.3 mol ÷ 0.1 M = 3 L.'], 'oxo', 3)

# ---------------- lanthanoids and actinoids ----------------
add(('2024', 'Apr', '2024-04-06', 1), 'lanth', 'The number of element from the following that do not belong to lanthanoids is : Eu, Cm, Er, Tb, Yb and Lu', ['3', '4', '1', '5'], 3,
    lambda: pick([3, 4, 1, 5], sum(1 for x in ['Eu', 'Cm', 'Er', 'Tb', 'Yb', 'Lu'] if x not in LAN)), ['Eu, Er, Tb, Yb, Lu are lanthanoids (Z 57–71).', 'Cm (curium, Z = 96) is an actinoid → 1.'], 'lanth', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'lanth', 'Number of colourless lanthanoid ions among the following is ______. Eu^{3+}, Lu^{3+}, Nd^{3+}, La^{3+}, Sm^{3+}', None, 2,
    lambda: sum(1 for m in ['Eu', 'Lu', 'Nd', 'La', 'Sm'] if f_ion(m, 3) in (0, 14)), ['f–f transitions need a partly filled 4f set.', 'La^{3+} (4f^{0}) and Lu^{3+} (4f^{14}) are colourless → 2.'], 'lanth', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'lanth', 'Number of paramagnetic ions among the following d- and f-block metal ions is ______. Mn^{2+}, Cu^{2+}, Zn^{2+}, Yb^{2+}, Sc^{3+}, La^{3+}, Gd^{3+}, Lu^{3+}, Ti^{4+}, Ce^{4+}', None, 3,
    lambda: sum(1 for x in ['Mn2+', 'Cu2+', 'Zn2+', 'Sc3+', 'Ti4+'] if n_of(x)) + sum(1 for m, q in [('Yb', 2), ('La', 3), ('Gd', 3), ('Lu', 3), ('Ce', 4)] if f_unp(f_ion(m, q))),
    ['d-block: Mn^{2+} (d^{5}) and Cu^{2+} (d^{9}) are paramagnetic; Zn^{2+}, Sc^{3+}, Ti^{4+} are d^{10}/d^{0}.', 'f-block: Gd^{3+} (4f^{7}) only; Yb^{2+} and Lu^{3+} are 4f^{14}, La^{3+} and Ce^{4+} 4f^{0} → total 3.'], 'lanth', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'lanth', 'Statement (I) : In the Lanthanoids, the formation of Ce^{+4} is favoured by its noble gas configuration. Statement (II) : Ce^{+4} is a strong oxidant reverting to the common +3 state.',
    ['Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false'], 2,
    lambda: stmt(f_ion('Ce', 4) == 0, True, ['Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false']),
    ['Ce^{4+} is [Xe]4f^{0}: noble-gas configuration favours it: I true.', 'E°(Ce^{4+}/Ce^{3+}) = +1.74 V: a strong oxidant returning to +3: II true.'], 'lanth', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'lanth', 'The correct statements among the following, A. Mo(VI) and W(VI) are less stable than Cr(VI). B. Ce^{4+} and Tb^{4+} are oxidant while Eu^{2+} and Yb^{2+} are reductant. C. Cm and Am have seven unpaired electrons. D. Actinoid contraction is greater from element to element than lanthanoid contraction.',
    ['A and B Only', 'C and D Only', 'B and D Only', 'A and C Only'], 3, lambda: pickset(['A and B Only', 'C and D Only', 'B and D Only', 'A and C Only'], dict(A=False, B=True, C=False, D=True)),
    ['A ✗: heavier members are MORE stable in high oxidation states.', 'B ✓ (they head for +3). C ✗: Am 5f^{7}7s^{2} has 7 but Cm 5f^{7}6d^{1}7s^{2} has 8. D ✓ (poor 5f shielding).'], 'lanth', 2)
add(('2024', 'Jan', '2024-01-30', 1), 'lanth', 'Diamagnetic Lanthanoid ions are:', ['Nd^{3+} and Eu^{3+}', 'La^{3+} and Ce^{4+}', 'Nd^{3+} and Ce^{4+}', 'Lu^{3+} and Eu^{3+}'], 2,
    lambda: pick([all(f_unp(f_ion(m, q)) == 0 for m, q in s) for s in [[('Nd', 3), ('Eu', 3)], [('La', 3), ('Ce', 4)], [('Nd', 3), ('Ce', 4)], [('Lu', 3), ('Eu', 3)]]], True),
    ['La^{3+} and Ce^{4+} are both 4f^{0}: no unpaired electrons.', 'Nd^{3+} 4f^{3}, Eu^{3+} 4f^{6} are paramagnetic.'], 'lanth', 1)
def _pairs():
    col = lambda m, q: 0 < d_count(m, q) < 10
    I = sum(1 for (a, b) in [(('Ti', 4), ('V', 2)), (('V', 2), ('Mn', 2)), (('Mn', 2), ('Fe', 3)), (('V', 2), ('Cr', 2))] if col(*a) and col(*b))
    act = {'Ac': 0, 'Lr': 14}   # 5f electrons in Ac3+, Lr3+
    II = sum([f_unp(f_ion('La', 3)) == 0 and f_unp(f_ion('Yb', 2)) == 0, f_unp(f_ion('Lu', 3)) == 0 and f_unp(f_ion('Ce', 4)) == 0, f_unp(act['Ac']) == 0 and f_unp(act['Lr']) == 0])
    return I == 3, II == 3
add(('2026', 'Apr', '2026-04-08', 2), 'lanth', 'Statement I : The number of pairs among [Ti^{4+}, V^{2+}], [V^{2+}, Mn^{2+}], [Mn^{2+}, Fe^{3+}] and [V^{2+}, Cr^{2+}] in which both ions are coloured is 3. Statement II : The number of pairs among [La^{3+}, Yb^{2+}], [Lu^{3+}, Ce^{4+}] and [Ac^{3+}, Lr^{3+}] ions in which both are diamagnetic is 3.',
    ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct'], 1,
    lambda: stmt(*_pairs(), ['Both Statement I and Statement II are correct', 'Both Statement I and Statement II are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct']),
    ['Ti^{4+} (d^{0}) is colourless; V^{2+}, Mn^{2+}, Fe^{3+}, Cr^{2+} are coloured → 3 pairs: I correct.', 'La^{3+}/Yb^{2+}, Lu^{3+}/Ce^{4+}, Ac^{3+}/Lr^{3+} are all f^{0} or f^{14} → 3 pairs: II correct.'], 'lanth', 2)
for _p in P: _p['t'] = _p['fam']
