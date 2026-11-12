"""Concept cards for Physics Unit 15 — Electromagnetic Waves (written for StudyVerse)."""
TOPICS = {'disp': 'Displacement current', 'wave': 'Nature of EM waves', 'energy': 'Energy, intensity & pressure', 'spec': 'Electromagnetic spectrum'}
CARDS = [
 dict(id='c1', t='Displacement current', e='⚡', lvl='f', topic='disp',
  body=['<div class="jx-f">I_{d} = ε_{0}\\f{dΦ_{E}}{dt} = C\\f{dV}{dt}</div>', 'Maxwell: a changing electric field makes a magnetic field just like a current does — this "current" flows through the gap of a charging capacitor.',
        'Between the plates I_{d} equals the conduction current in the wires; it spreads evenly over the plate area.', 'In a conductor: \\f{J_{conduction}}{J_{displacement}} = \\f{σ}{ωε_{0}}.'],
  check=dict(q='5 μF capacitor, dV/dt = 2 × 10³ V/s. I_d =', o=['10 mA', '2.5 mA', '10 A', '1 mA'], a=0, why='5 × 10⁻⁶ × 2000.')),
 dict(id='c2', t='E, B and the direction of travel', e='🧭', lvl='m', topic='wave',
  body=['<div class="jx-f">E_{0} = cB_{0},  c = \\f{1}{√{μ_{0}ε_{0}}},  \\vec{B} = \\f{\\vec{k} × \\vec{E}}{ω},  travel along \\vec{E} × \\vec{B}</div>', 'E and B are perpendicular to each other and to the direction of travel, and are in phase.',
        'sin(kx − ωt) travels along +x; sin(kx + ωt) along −x. Speed v = \\f{ω}{k}.', 'In a medium v = \\f{c}{√{μ_{r}ε_{r}}}, n = √{μ_{r}ε_{r}} (non-magnetic: n = √{ε_{r}}).'],
  check=dict(q='Wave along +x with E along +y. B points along :', o=['+z', '−z', '+x', '−y'], a=0, why='x̂ × ŷ = ẑ.')),
 dict(id='c3', t='Energy, intensity, momentum', e='☀️', lvl='m', topic='energy',
  body=['<div class="jx-f">⟨u⟩ = ½ε_{0}E_{0}^{2} (half electric, half magnetic),  I = ½cε_{0}E_{0}^{2} = \\f{E_{0}^{2}}{2Z_{0}},  Z_{0} ≈ 377 Ω</div>', 'Momentum p = \\f{U}{c}: radiation pressure \\f{I}{c} (absorbed) or \\f{2I}{c} (reflected).',
        'Point source: I = \\f{P}{4πr^{2}}, the same in every direction at the same distance.'],
  check=dict(q='Same light: pressure on a mirror vs a black surface :', o=['equal', 'mirror twice', 'mirror half', 'mirror zero'], a=1, why='Reflection reverses momentum.')),
 dict(id='c4', t='The spectrum', e='🌈', lvl='f', topic='spec',
  body=['Shortest λ to longest: gamma (< 10^{−3} nm) · X-rays (10^{−3}–1 nm) · UV (1–400 nm) · visible (400–700 nm) · infrared (700 nm–1 mm) · microwaves (1 mm–30 cm) · radio.',
        'Higher frequency ↔ shorter wavelength ↔ more energetic photons (E = hν = \\f{hc}{λ}).', 'Uses: radio/TV, microwave ovens & radar, IR remote & heating, UV sterilising, X-ray imaging, gamma in cancer therapy.'],
  check=dict(q='Which has the longest wavelength?', o=['X-rays', 'UV', 'Infrared', 'Gamma'], a=2, why='Infrared is beyond red.')),
]
FORMULAS = [('Displacement current', 'I_{d} = ε_{0}\\f{dΦ_{E}}{dt}'), ('Speed', 'c = \\f{1}{√{μ_{0}ε_{0}}}'), ('Fields', 'E_{0} = cB_{0}'), ('Medium', 'v = \\f{c}{√{μ_{r}ε_{r}}}'),
            ('Energy density', '⟨u⟩ = ½ε_{0}E_{0}^{2}'), ('Intensity', 'I = ½cε_{0}E_{0}^{2}'), ('Pressure', 'p = \\f{I}{c} or \\f{2I}{c}'), ('Photon', 'E = \\f{hc}{λ}')]
TRAPS = ['Check direction with E × B, never by guessing.', 'Electric and magnetic energy densities are EQUAL on average.', 'Reflecting surface: pressure doubles.', 'EM waves carry momentum even though photons have no rest mass.',
         'sin(ωt − kx) and sin(kx − ωt) both travel along +x.']
STEPS = [dict(k='s1', t='Maxwell', e='⚡', cards=['c1'], need=['disp'], note='Displacement current'),
         dict(k='s2', t='The wave', e='🧭', cards=['c2', 'c3'], need=['wave', 'energy'], note='E, B, direction, energy and pressure'),
         dict(k='s3', t='Spectrum', e='🌈', cards=['c4'], need=['spec'], note='From gamma rays to radio')]
META = dict(unit='phy-u15', subject='phy', n=15, title='Electromagnetic Waves', cls=12, labs=['emw'],
            syllabus='Displacement current. Electromagnetic waves and their characteristics, transverse nature of electromagnetic waves, electromagnetic spectrum (radio waves, microwaves, infrared, visible, ultraviolet, X-rays, gamma rays), applications of e.m. waves.')
