"""Concept cards for Physics Unit 19 — Electronic Devices (written for StudyVerse)."""
TOPICS = {'semi': 'Semiconductors, bands & doping', 'diode': 'p-n junction, rectifiers & Zener', 'gate': 'Logic gates'}
CARDS = [
 dict(id='c1', t='Bands & carriers', e='🧱', lvl='f', topic='semi',
  body=['<div class="jx-f">E_{g}: conductor ≈ 0, semiconductor ≈ 1 eV, insulator > 3 eV;  n_{e}n_{h} = n_{i}^{2};  σ = e(n_{e}μ_{e} + n_{h}μ_{h})</div>', 'Pentavalent dopant (P, As) → n-type, electrons majority; trivalent (B, Al, In) → p-type, holes majority. The crystal stays neutral.',
        'Semiconductors have a NEGATIVE temperature coefficient of resistance: hotter → more carriers → lower resistance.', 'Light of λ < \\f{hc}{E_{g}} (hc = 1242 eV nm) creates electron–hole pairs.'],
  check=dict(q='In n-type silicon, the minority carriers are', o=['holes', 'electrons', 'donor ions', 'none'], a=0, why='Donors add electrons; holes are fewer.')),
 dict(id='c2', t='The p-n junction', e='🔀', lvl='m', topic='diode',
  body=['<div class="jx-f">Forward: anode (p) higher than cathode (n);  N_{A}x_{p} = N_{D}x_{n}</div>', 'Diffusion builds a depletion layer and barrier (~0.7 V Si, ~0.3 V Ge). Forward bias shrinks it; reverse bias widens it.',
        'Reverse current is tiny (minority carriers) and nearly constant until breakdown. The lightly doped side has the wider depletion region.'],
  check=dict(q='Which is forward biased?', o=['p at −10 V, n at −15 V', 'p at −10 V, n at 0 V', 'p at 2 V, n at 4 V', 'p at 0 V, n at 5 V'], a=0, why='Anode higher than cathode.')),
 dict(id='c3', t='Rectifiers & special diodes', e='⚡', lvl='m', topic='diode',
  body=['Half-wave: output frequency = f; full-wave/bridge: 2f. A capacitor filter smooths the ripple.', 'Zener: operated in reverse breakdown, holds V_{Z}: I_{S} = \\f{V_{in} − V_{Z}}{R_{S}}, I_{Z} = I_{S} − I_{L}; max current \\f{P_{max}}{V_{Z}}.',
        'Photodiode: reverse biased, current ∝ light. Solar cell: no bias, large area. LED: forward biased, heavily doped, colour from E_{g}.'],
  check=dict(q='A Zener regulator: 12 V in, 200 Ω, V_Z = 6 V, load 1 kΩ. I_Z =', o=['24 mA', '30 mA', '6 mA', '18 mA'], a=0, why='30 − 6 = 24 mA.')),
 dict(id='c4', t='Logic gates', e='🔢', lvl='f', topic='gate',
  body=['AND: 1 only if all 1. OR: 1 if any 1. NOT inverts. NAND = NOT AND, NOR = NOT OR (both universal). XOR: 1 when inputs differ; XNOR: when equal.',
        'De Morgan: \\overline{A·B} = Ā + B̄, \\overline{A + B} = Ā·B̄. NAND or NOR with tied inputs is a NOT gate.', 'Absorption: A(A + B) = A, A + AB = A. Work any circuit row by row.'],
  check=dict(q='NOT A and NOT B into a NAND gate give', o=['OR', 'AND', 'NOR', 'XOR'], a=0, why='\\overline{Ā·B̄} = A + B.')),
]
FORMULAS = [('Mass action', 'n_{e}n_{h} = n_{i}^{2}'), ('Conductivity', 'σ = e(n_{e}μ_{e} + n_{h}μ_{h})'), ('Band gap', 'λ = \\f{1242}{E_{g}(eV)} nm'), ('Depletion', 'N_{A}x_{p} = N_{D}x_{n}'),
            ('Zener', 'I_{Z} = \\f{V − V_{Z}}{R_{S}} − \\f{V_{Z}}{R_{L}}'), ('Protective R', 'R = \\f{V − V_{Z}}{P/V_{Z}}'), ('De Morgan', '\\overline{AB} = Ā + B̄'), ('Ripple', 'f_{out} = f or 2f')]
TRAPS = ['Reverse current comes from MINORITY carriers.', 'Solar cells need a large junction area, photodiodes are reverse biased, LEDs forward biased.', 'Full-wave output ripples at twice the supply frequency.',
         'A Zener only regulates if the open-circuit load voltage exceeds V_Z.', 'NAND/NOR with tied inputs = NOT.']
STEPS = [dict(k='s1', t='Materials', e='🧱', cards=['c1'], need=['semi'], note='Bands, doping and carriers'),
         dict(k='s2', t='Diodes', e='🔀', cards=['c2', 'c3'], need=['diode'], note='Junctions, rectifiers, Zener, LED and solar cell'),
         dict(k='s3', t='Gates', e='🔢', cards=['c4'], need=['gate'], note='Truth tables and De Morgan')]
META = dict(unit='phy-u19', subject='phy', n=19, title='Electronic Devices', cls=12, labs=['gates'],
            syllabus='Semiconductors; semiconductor diode: I-V characteristics in forward and reverse bias; diode as a rectifier; I-V characteristics of LED, photodiode, solar cell and Zener diode; Zener diode as a voltage regulator. Logic gates (OR, AND, NOT, NAND and NOR).')
