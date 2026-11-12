"""Concept cards for Chemistry Unit 1 — Some Basic Concepts in Chemistry (written for StudyVerse)."""
TOPICS = {'mole': 'Mole, atoms & molar mass', 'conc': 'Concentration terms', 'stoich': 'Stoichiometry & limiting reagent', 'formula': 'Percentage composition & formulae'}
CARDS = [
 dict(id='c1', t='The mole — a chemist\'s dozen', e='🥚', lvl='f', topic='mole',
  body=['1 mole = 6.022 × 10^{23} particles (N_{A}). Atoms are far too small to count one by one, so we count them in moles.',
        '<div class="jx-f">n = \\f{mass}{molar mass} = \\f{N}{N_{A}} = \\f{V (gas at STP)}{22.4 L}</div>', 'Molar mass = sum of atomic masses: H_{2}O = 18, CO_{2} = 44, H_{2}SO_{4} = 98, NaCl = 58.5, glucose = 180, sucrose = 342 g mol^{−1}.',
        'Number of ATOMS = moles of molecules × atoms per molecule. 18 g of water has 1 mol molecules but 3 mol atoms.', 'Equal masses of elements → the LIGHTER element has more atoms.'],
  check=dict(q='Atoms in 9 g of water :', o=['0.5 N_{A}', '1.5 N_{A}', '3 N_{A}', '9 N_{A}'], a=1, why='0.5 mol × 3 atoms.')),
 dict(id='c2', t='Stoichiometry and the limiting reagent', e='⚖️', lvl='m', topic='stoich',
  body=['A balanced equation is a recipe in MOLES: 2H_{2} + O_{2} → 2H_{2}O means 2 mol + 1 mol → 2 mol.', 'Always convert grams → moles first, use the mole ratio, then convert back.',
        '<b>Limiting reagent</b>: divide each reactant\'s moles by its coefficient. The SMALLEST value runs out first and decides how much product forms.', 'The other reactant is in excess — the left-over amount is often asked too.',
        'For gases at STP: 1 mol = 22.4 L (some new papers use 22.7 L at 1 bar).'],
  check=dict(q='4 mol H_{2} + 1 mol O_{2} → water. Limiting :', o=['H_{2}', 'O_{2}', 'both', 'neither'], a=1, why='4/2 = 2 vs 1/1 = 1 → O_{2}.')),
 dict(id='c3', t='Concentration terms', e='🧪', lvl='m', topic='conc',
  body=['<div class="jx-f">Molarity M = \\f{mol solute}{L of solution},  Molality m = \\f{mol solute}{kg of solvent}</div>', 'Mass % = \\f{mass solute}{mass solution} × 100; ppm = parts per million by mass; mole fraction x = \\f{n_{i}}{n_{total}}.',
        'From % and density: <div class="jx-f">M = \\f{10 × d × w%}{M_{solute}}</div>', 'From M and density: <div class="jx-f">m = \\f{1000M}{1000d − M × M_{solute}}</div>',
        'Molarity changes with temperature (volume expands); molality, mass % and mole fraction do not.', 'Dilution: M_{1}V_{1} = M_{2}V_{2}. Neutralisation: equivalents of acid = equivalents of base.'],
  check=dict(q='Which changes with temperature?', o=['molality', 'molarity', 'mole fraction', 'mass %'], a=1, why='It uses solution volume.')),
 dict(id='c4', t='From analysis to formula', e='🔬', lvl='m', topic='formula',
  body=['% of an element = \\f{(atoms × atomic mass)}{molar mass} × 100.', 'Combustion analysis: C = \\f{12}{44} × mass of CO_{2};  H = \\f{2}{18} × mass of H_{2}O; O by difference.',
        '<b>Empirical formula</b>: % ÷ atomic mass → divide by the smallest → round (multiply by 2 or 3 if you get .5 or .33).', '<b>Molecular formula</b> = (empirical formula) × n, where n = \\f{molar mass}{empirical formula mass}.'],
  check=dict(q='Empirical formula CH_{2}O, M = 180. Molecular formula :', o=['C_{2}H_{4}O_{2}', 'C_{6}H_{12}O_{6}', 'C_{3}H_{6}O_{3}', 'CH_{2}O'], a=1, why='180/30 = 6.')),
]
FORMULAS = [('Moles', 'n = \\f{m}{M} = \\f{N}{N_{A}} = \\f{V}{22.4 L}'), ('Avogadro', 'N_{A} = 6.022 × 10^{23}'), ('Molarity', 'M = \\f{n}{V (L)}'), ('Molality', 'm = \\f{n}{kg solvent}'),
            ('% → M', 'M = \\f{10dw}{M_{solute}}'), ('M → m', 'm = \\f{1000M}{1000d − MM_{solute}}'), ('Dilution', 'M_{1}V_{1} = M_{2}V_{2}'), ('Mole fraction', 'x_{A} = \\f{n_{A}}{n_{A} + n_{B}}'), ('ppm', '\\f{mass of part}{total mass} × 10^{6}'), ('Carbon %', '\\f{12}{44} × \\f{m_{CO_{2}}}{m} × 100')]
TRAPS = ['Molarity uses volume of SOLUTION, molality uses mass of SOLVENT (not solution).', 'Count atoms, not molecules, when the question says "atoms".', 'Find the limiting reagent before using any product formula.',
         'Partial pressures go by MOLES, not mass %.', 'A hydrate\'s molar mass includes its water (FeSO_{4}·7H_{2}O = 278).', 'Mass of product can never exceed total mass of reactants used.']
STEPS = [dict(k='s1', t='Counting with moles', e='🥚', cards=['c1'], need=['mole'], note='Moles, Avogadro number, molar mass and STP volume'),
         dict(k='s2', t='Reactions', e='⚖️', cards=['c2'], need=['stoich'], note='Mole ratios and the limiting reagent'),
         dict(k='s3', t='Solutions & formulae', e='🧪', cards=['c3', 'c4'], need=['conc', 'formula'], note='Concentration terms, empirical and molecular formulae')]
META = dict(unit='chem-u01', subject='chem', n=1, title='Some Basic Concepts in Chemistry', cls=11, labs=['molemach', 'limit'],
            syllabus="Matter and its nature; Dalton's atomic theory; concept of atom, molecule, element and compound; laws of chemical combination; atomic and molecular masses; mole concept; molar mass; percentage composition; empirical and molecular formulae; chemical equations and stoichiometry; limiting reagent; concentration terms: mass percent, mole fraction, molarity, molality, ppm.")
