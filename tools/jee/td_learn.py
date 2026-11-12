"""Concept cards for Physics Unit 8 — Thermodynamics (written for StudyVerse)."""
TOPICS = {'law': 'First law, heat, work & internal energy', 'proc': 'Thermodynamic processes', 'cycle': 'Cycles, engines & refrigerators'}
CARDS = [
 dict(id='c1', t='Zeroth and first law', e='🌡️', lvl='f', topic='law',
  body=['<div class="jx-f">ΔQ = ΔU + ΔW  (Q in, W done BY the gas)</div>', 'Zeroth law: bodies in equilibrium with a third are in equilibrium with each other — this defines temperature.',
        'U of an ideal gas depends only on T: ΔU = nC_{v}ΔT for ANY process. Q and W depend on the path; U does not.', 'Extensive (doubles with size): U, V, mass. Intensive: P, T, density. Extensive ÷ mass is intensive.'],
  check=dict(q='A gas absorbs 500 J and does 200 J of work. ΔU =', o=['700 J', '300 J', '−300 J', '200 J'], a=1, why='ΔU = Q − W.')),
 dict(id='c2', t='Specific heats and work', e='🔧', lvl='f', topic='law',
  body=['<div class="jx-f">C_{p} − C_{v} = R,  γ = \\f{C_{p}}{C_{v}},  W = ∫P dV = area under the P–V curve</div>', 'Monoatomic C_{v} = \\f{3}{2}R; rigid diatomic \\f{5}{2}R.',
        'At constant pressure: W = nRΔT, ΔU = \\f{W}{γ − 1}, Q = \\f{γ}{γ − 1}W. Diatomic: Q : ΔU : W = 7 : 5 : 2.'],
  check=dict(q='Diatomic gas does 100 J isobarically. Heat given :', o=['250 J', '350 J', '140 J', '100 J'], a=1, why='Q = (7/2)/1 × 100.')),
 dict(id='c3', t='Isothermal, isobaric, isochoric', e='📐', lvl='m', topic='proc',
  body=['<div class="jx-f">isothermal: W = nRT ln\\f{V_{2}}{V_{1}}, ΔU = 0, Q = W;  isochoric: W = 0, Q = ΔU = nC_{v}ΔT;  isobaric: W = PΔV, Q = nC_{p}ΔT</div>',
        'P ∝ T (straight line through origin on P–T) means constant volume.', 'In a P–V picture: work = area under the path; for a cycle, the enclosed area (clockwise = done by the gas).'],
  check=dict(q='Isothermal expansion of an ideal gas: ΔU =', o=['Q', 'W', '0', 'nC_pΔT'], a=2, why='U depends only on T.')),
 dict(id='c4', t='Adiabatic process', e='🧊', lvl='m', topic='proc',
  body=['<div class="jx-f">PV^{γ} = const,  TV^{γ − 1} = const,  P^{1 − γ}T^{γ} = const,  W = \\f{P_{1}V_{1} − P_{2}V_{2}}{γ − 1} = nC_{v}(T_{1} − T_{2})</div>',
        'No heat: work comes out of U, so expansion cools and compression heats (bicycle pump). Molar heat capacity is 0.', 'An adiabat is steeper than an isotherm by a factor γ. Sudden compression in an insulated vessel = adiabatic.',
        'P ∝ T^{k} on an adiabat → k = \\f{γ}{γ − 1}.'],
  check=dict(q='Monoatomic gas compressed adiabatically to 1/8 volume. P becomes :', o=['8×', '16×', '32×', '64×'], a=2, why='8^{5/3} = 32.')),
 dict(id='c5', t='Heat engines and refrigerators', e='⚙️', lvl='m', topic='cycle',
  body=['<div class="jx-f">η = \\f{W}{Q_{H}} = 1 − \\f{Q_{C}}{Q_{H}};  Carnot: η = 1 − \\f{T_{C}}{T_{H}};  refrigerator β = \\f{Q_{C}}{W} = \\f{T_{C}}{T_{H} − T_{C}}</div>',
        'Over a full cycle ΔU = 0, so net Q = net W.', 'Carnot cycle: two isotherms + two adiabats; no engine between the same temperatures beats it.',
        'Two Carnot engines in series: the combined efficiency is LESS than the sum of the two efficiencies.'],
  check=dict(q='Carnot engine between 500 K and 300 K. η =', o=['40 %', '60 %', '30 %', '50 %'], a=0, why='1 − 300/500.')),
]
FORMULAS = [('First law', 'ΔQ = ΔU + ΔW'), ('Internal energy', 'ΔU = nC_{v}ΔT'), ('Mayer', 'C_{p} − C_{v} = R'), ('Isothermal work', 'W = nRT ln\\f{V_{2}}{V_{1}}'), ('Adiabatic', 'PV^{γ} = const'),
            ('Adiabatic T', 'TV^{γ − 1} = const'), ('Adiabatic work', 'W = \\f{P_{1}V_{1} − P_{2}V_{2}}{γ − 1}'), ('Carnot', 'η = 1 − \\f{T_{C}}{T_{H}}'), ('Refrigerator', 'β = \\f{T_{C}}{T_{H} − T_{C}}')]
TRAPS = ['ΔU = nC_{v}ΔT for EVERY process of an ideal gas, not only isochoric.', 'Sign: W is work done BY the gas; Q is heat INTO it.', 'Adiabatic ≠ isothermal: in an adiabat T changes.', 'Use kelvin in every efficiency formula.',
         'Melting ice shrinks: the atmosphere does work on it.', 'Cycle clockwise on P–V (V across) → net work by the gas is positive.']
STEPS = [dict(k='s1', t='First law', e='🌡️', cards=['c1', 'c2'], need=['law'], note='Heat, work, internal energy'),
         dict(k='s2', t='Processes', e='📐', cards=['c3', 'c4'], need=['proc'], note='Isothermal, adiabatic, isobaric, isochoric'),
         dict(k='s3', t='Cycles', e='⚙️', cards=['c5'], need=['cycle'], note='Cycles, Carnot, engines and fridges')]
META = dict(unit='phy-u08', subject='phy', n=8, title='Thermodynamics', cls=11, labs=['pv'],
            syllabus='Thermal equilibrium, zeroth law of thermodynamics, the concept of temperature. Heat, work, and internal energy. The first law of thermodynamics, isothermal and adiabatic processes. The second law of thermodynamics: reversible and irreversible processes.')
