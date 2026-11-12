"""Concept cards for Chemistry Unit 5 — Solutions (written for StudyVerse)."""
TOPICS = {'conc': 'Concentration terms', 'vp': "Vapour pressure & Raoult's law", 'colli': 'Colligative properties', 'vant': "Abnormal molar mass & van 't Hoff factor"}
CARDS = [
 dict(id='c1', t='Ways to express concentration', e='⚖️', lvl='f', topic='conc',
  body=['<div class="jx-f">M = \\f{mol solute}{L solution},  m = \\f{mol solute}{kg solvent},  x = \\f{n_{i}}{Σn},  ppm = \\f{g solute}{10^{6} g solution}</div>',
        'Molarity changes with temperature (volume expands); molality, mole fraction and mass % do not.', 'M ↔ m: take 1 L of solution, mass = 1000 × density, subtract the solute mass to get the solvent mass.',
        'Mixing solutions of the same solute: total moles ÷ total volume.'],
  check=dict(q='Which changes with temperature?', o=['Molality', 'Molarity', 'Mole fraction', 'Mass %'], a=1, why='It depends on volume.')),
 dict(id='c2', t="Raoult's law and ideal solutions", e='💨', lvl='m', topic='vp',
  body=['<div class="jx-f">p = x_{A}p_{A}^{0} + x_{B}p_{B}^{0},  y_{A} = \\f{x_{A}p_{A}^{0}}{p}</div>', 'The vapour is richer in the MORE volatile component.',
        'Positive deviation (ethanol + water): weaker A–B attraction, higher VP, ΔH_{mix} > 0, minimum-boiling azeotrope.', 'Negative deviation (chloroform + acetone): stronger attraction, lower VP, ΔH_{mix} < 0, maximum-boiling azeotrope.'],
  check=dict(q='Negative deviation gives :', o=['higher VP, lower bp', 'lower VP, higher bp', 'higher VP, higher bp', 'no change'], a=1, why='Stronger attraction holds molecules back.')),
 dict(id='c3', t='Colligative properties', e='🧊', lvl='m', topic='colli',
  body=['<div class="jx-f">\\f{Δp}{p^{0}} = x_{solute},  ΔT_{b} = iK_{b}m,  ΔT_{f} = iK_{f}m,  π = iCRT</div>', 'They depend only on the NUMBER of solute particles, not their kind. Water: K_{b} = 0.52, K_{f} = 1.86 K kg mol^{−1}.',
        'Molar mass from data: M = \\f{K × w}{ΔT × W(kg)}. Osmotic pressure is the most sensitive (good for proteins).', 'Reverse osmosis: press the more concentrated side above π through a semipermeable membrane.'],
  check=dict(q='0.1 m glucose vs 0.1 m NaCl — which freezes lower?', o=['glucose', 'NaCl', 'same', 'cannot say'], a=1, why='NaCl gives 2 particles.')),
 dict(id='c4', t="van 't Hoff factor", e='🔢', lvl='h', topic='vant',
  body=['<div class="jx-f">i = \\f{observed colligative effect}{expected for no change} = 1 + (n − 1)α (dissociation) = 1 − (1 − \\f{1}{n})α (association)</div>',
        'NaCl: i ≤ 2, CaCl_{2}: i ≤ 3, Al_{2}(SO_{4})_{3}: i ≤ 5. Acetic acid dimerises in benzene (i < 1).', 'Weak acid from ΔT_{f}: i = 1 + α → K_{a} = \\f{cα^{2}}{1 − α}.'],
  check=dict(q='i for 50 % dissociated AB₂ :', o=['1.5', '2', '2.5', '3'], a=1, why='1 + 2 × 0.5.')),
]
FORMULAS = [('Molality', 'm = \\f{n_{solute}}{kg solvent}'), ('Raoult', 'p = Σx_{i}p_{i}^{0}'), ('RLVP', '\\f{Δp}{p^{0}} = x_{solute}'), ('Boiling', 'ΔT_{b} = iK_{b}m'), ('Freezing', 'ΔT_{f} = iK_{f}m'),
            ('Osmotic', 'π = iCRT'), ("van 't Hoff", 'i = 1 + (n − 1)α'), ('Molar mass', 'M = \\f{Kw}{ΔT W}')]
TRAPS = ['Molality uses kg of SOLVENT, not of solution.', 'Count particles: CaCl₂ gives 3, Al₂(SO₄)₃ gives 5.', 'Vapour is richer in the more volatile liquid.', 'Molarity falls on heating (water expands, except below 4 °C).',
         'Osmosis: solvent moves from dilute to concentrated side.']
STEPS = [dict(k='s1', t='Concentration', e='⚖️', cards=['c1'], need=['conc'], note='M, m, x, mass %, ppm'),
         dict(k='s2', t='Vapour pressure', e='💨', cards=['c2'], need=['vp'], note="Raoult's law and deviations"),
         dict(k='s3', t='Colligative', e='🧊', cards=['c3', 'c4'], need=['colli', 'vant'], note="ΔT_b, ΔT_f, π and van 't Hoff factor")]
META = dict(unit='chem-u05', subject='chem', n=5, title='Solutions', cls=12, labs=['mixer'],
            syllabus="Different methods for expressing the concentration of solution — molality, molarity, mole fraction, percentage (by volume and mass both), the vapour pressure of solutions and Raoult's Law — Ideal and non-ideal solutions, vapour pressure-composition plots for ideal and non-ideal solutions; Colligative properties of dilute solutions — a relative lowering of vapour pressure, depression of freezing point, the elevation of boiling point and osmotic pressure; Determination of molecular mass using colligative properties; Abnormal value of molar mass, van't Hoff factor and its significance.")
