"""Concept cards for Physics Unit 9 — Kinetic Theory of Gases (written for StudyVerse)."""
TOPICS = {'gas': 'Ideal gas equation', 'ke': 'Kinetic energy & molecular speeds', 'dof': 'Degrees of freedom & specific heats', 'mfp': 'Mean free path'}
CARDS = [
 dict(id='c1', t='Ideal gas equation', e='🎈', lvl='f', topic='gas',
  body=['<div class="jx-f">PV = nRT = Nk_{B}T,  ρ = \\f{PM}{RT},  R = 8.314 J mol^{−1} K^{−1},  k_{B} = 1.38 × 10^{−23} J/K</div>', 'Fixed V: P ∝ T (so \\f{ΔP}{P} = \\f{ΔT}{T}); fixed P: V ∝ T; fixed T: P ∝ \\f{1}{V}.',
        'Joining two vessels: moles add — \\f{P_{1}V_{1}}{T_{1}} + \\f{P_{2}V_{2}}{T_{2}} = \\f{P(V_{1} + V_{2})}{T}.', 'Graphs: on P–T the slope ∝ density; on V–T the slope ∝ \\f{1}{P}.'],
  check=dict(q='Rigid vessel: P rises 0.5 % for a 1 K rise. Initial T :', o=['50 K', '200 K', '500 K', '2000 K'], a=1, why='ΔT/T = 0.005.')),
 dict(id='c2', t='Pressure and kinetic energy', e='🏃', lvl='m', topic='ke',
  body=['<div class="jx-f">P = \\f{1}{3}ρ\\overline{v^{2}},  KE_{avg} = \\f{3}{2}k_{B}T,  v_{rms} = √{\\f{3RT}{M}}</div>', 'Average KE depends ONLY on T (not on the gas). Speeds depend on T and M: v ∝ √{\\f{T}{M}}.',
        'v_{rms} > v_{avg} > v_{mp} (√{3} : √{8/π} : √{2}). \\overline{v^{2}} ∝ T is a straight line.', 'Internal energy of air in a room = \\f{5}{2}PV — it does not change when you heat the room at fixed P!'],
  check=dict(q='v_rms of H₂ is 2 km/s. v_rms of O₂ at the same T :', o=['0.5 km/s', '1 km/s', '8 km/s', '0.125 km/s'], a=0, why='√(2/32) = 1/4.')),
 dict(id='c3', t='Degrees of freedom', e='🎲', lvl='m', topic='dof',
  body=['<div class="jx-f">½k_{B}T per degree of freedom;  C_{v} = \\f{f}{2}R,  C_{p} = (\\f{f}{2} + 1)R,  γ = 1 + \\f{2}{f}</div>', 'Monoatomic f = 3; rigid diatomic 5; non-linear (CH_{4}, NH_{3}) 6 (3 translation + 3 rotation). Each vibrational mode adds 2.',
        'Mixtures: C_{v,mix} = \\f{Σn_{i}C_{v,i}}{Σn_{i}}; then γ_{mix} = \\f{C_{v} + R}{C_{v}} (NOT the average of the γs). Mixing gases conserves total U.'],
  check=dict(q='γ for a gas with f = 6 :', o=['4/3', '5/3', '7/5', '3/2'], a=0, why='1 + 2/6.')),
 dict(id='c4', t='Mean free path', e='🎯', lvl='h', topic='mfp',
  body=['<div class="jx-f">λ = \\f{1}{√{2}nπd^{2}} = \\f{k_{B}T}{√{2}πd^{2}P},  collisions per second = \\f{v̄}{λ}</div>', 'λ ∝ \\f{1}{d^{2}} and ∝ \\f{1}{n}; at fixed n it does not depend on T.', 'Thin gas (low P) → long free paths.'],
  check=dict(q='Molecular diameter doubled, same n. λ becomes :', o=['×2', '×½', '×¼', '×4'], a=2, why='λ ∝ 1/d².')),
]
FORMULAS = [('Ideal gas', 'PV = nRT'), ('Density', 'ρ = \\f{PM}{RT}'), ('Pressure', 'P = \\f{1}{3}ρ\\overline{v^{2}}'), ('Mean KE', 'KE = \\f{3}{2}k_{B}T'), ('rms speed', 'v_{rms} = √{\\f{3RT}{M}}'),
            ('Specific heat', 'C_{v} = \\f{f}{2}R'), ('Gamma', 'γ = 1 + \\f{2}{f}'), ('Mean free path', 'λ = \\f{1}{√{2}nπd^{2}}')]
TRAPS = ['Average KE depends only on T — the same for H₂ and O₂ at the same T; their speeds differ.', 'Vibration adds 2 to f, not 1.', 'γ of a mixture: average C_{v} first, never the γs.',
         'Use M in kg/mol in v_{rms} = √{3RT/M}.', 'Per molecule use k_{B}; per mole use R.']
STEPS = [dict(k='s1', t='Gas laws', e='🎈', cards=['c1'], need=['gas'], note='PV = nRT and its graphs'),
         dict(k='s2', t='Molecules', e='🏃', cards=['c2', 'c4'], need=['ke', 'mfp'], note='KE, speeds and mean free path'),
         dict(k='s3', t='Heat capacities', e='🎲', cards=['c3'], need=['dof'], note='Degrees of freedom, C_{v}, γ and mixtures')]
META = dict(unit='phy-u09', subject='phy', n=9, title='Kinetic Theory of Gases', cls=11, labs=['box'],
            syllabus='Equation of state of a perfect gas, work done on compressing a gas. Kinetic theory of gases — assumptions, the concept of pressure. Kinetic interpretation of temperature: RMS speed of gas molecules; degrees of freedom, law of equipartition of energy, applications to specific heat capacities of gases; mean free path, Avogadro\'s number.')
