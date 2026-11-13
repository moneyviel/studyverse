"""Concept cards for Physics Unit 20 — Experimental Skills (written for StudyVerse)."""
TOPICS = {'meas': 'Instruments, readings & errors', 'expt': 'Standard experiments'}
CARDS = [
 dict(id='c1', t='Vernier callipers', e='📏', lvl='f', topic='meas',
  body=['<div class="jx-f">LC = 1 MSD − 1 VSD = \\f{1 MSD}{N};  reading = MSR + VC × LC − zero error</div>', 'N vernier divisions span N − 1 main divisions, so each vernier division is a little shorter.',
        'Zero error: if the vernier zero sits to the right of the main zero (jaws closed) it is positive; subtract it.'],
  check=dict(q='10 VSD = 9 MSD of 1 mm. LC =', o=['0.1 mm', '0.9 mm', '1 mm', '0.01 mm'], a=0, why='1 − 0.9 mm.')),
 dict(id='c2', t='Screw gauge', e='🔩', lvl='f', topic='meas',
  body=['<div class="jx-f">LC = \\f{pitch}{circular divisions};  reading = LSR × pitch + CSR × LC − zero error</div>', 'Zero below the reference line (circular zero has passed) → positive error; above → negative.',
        'Spherometer: measures small heights, hence thickness and radius of curvature R = \\f{l^{2}}{6h} + \\f{h}{2}.'],
  check=dict(q='Pitch 0.5 mm, 50 divisions: LC =', o=['0.01 mm', '0.1 mm', '0.05 mm', '0.001 mm'], a=0, why='0.5/50.')),
 dict(id='c3', t='Errors & significant figures', e='🎯', lvl='m', topic='meas',
  body=['<div class="jx-f">Q = \\f{a^{p}b^{q}}{c^{r}} → \\f{ΔQ}{Q} = p\\f{Δa}{a} + q\\f{Δb}{b} + r\\f{Δc}{c}</div>', 'Pendulum: \\f{Δg}{g} = \\f{ΔL}{L} + 2\\f{ΔT}{T}; timing many swings shrinks ΔT/T.',
        'Products/quotients: keep the fewest significant figures; sums: the fewest decimal places.'],
  check=dict(q='ΔL/L = 1% and ΔT/T = 0.5%. Δg/g =', o=['2%', '1.5%', '0.5%', '3%'], a=0, why='1 + 2 × 0.5.')),
 dict(id='c4', t='Electrical experiments', e='🔌', lvl='m', topic='expt',
  body=['Metre bridge: \\f{X}{R} = \\f{l}{100 − l}; potentiometer: E ∝ balancing length, r = R(\\f{l_{1}}{l_{2}} − 1).', 'A voltmeter across R draws current: V/I gives R ∥ R_{V}, so correct for it.',
        'Ohm\'s law, Zener and diode characteristics are read from V–I plots (slope = 1/R).'],
  check=dict(q='Metre bridge: 5 Ω on the left balances at 40 cm. R =', o=['7.5 Ω', '3.3 Ω', '5 Ω', '2 Ω'], a=0, why='5 × 60/40.')),
 dict(id='c5', t='Mechanics & heat experiments', e='⚗️', lvl='m', topic='expt',
  body=['Pendulum: \\f{1}{T^{2}} ∝ \\f{1}{L} (hyperbola) and T^{2} ∝ L (straight line). Capillary rise: h = \\f{2T cos θ}{ρgr}.', 'Falling ball in glycerine: v rises and levels at v_{t} = \\f{2r^{2}(ρ − σ)g}{9η} ∝ r^{2}.',
        'Resonance tube: v = 2f(l_{2} − l_{1}); end correction e = 0.3d. Standard resistors use alloys (manganin) with nearly zero temperature coefficient.'],
  check=dict(q='Doubling the ball radius makes the terminal speed', o=['4 times', '2 times', '8 times', 'the same'], a=0, why='v_t ∝ r².')),
]
FORMULAS = [('Vernier LC', 'LC = \\f{1 MSD}{N}'), ('Screw LC', 'LC = \\f{pitch}{N}'), ('Error', '\\f{ΔQ}{Q} = Σ |p|\\f{Δa}{a}'), ('Pendulum', 'g = \\f{4π^{2}L}{T^{2}}'), ('Metre bridge', '\\f{X}{R} = \\f{l}{100 − l}'),
            ('Internal r', 'r = R(\\f{l_{1}}{l_{2}} − 1)'), ('Capillary', 'h = \\f{2T cos θ}{ρgr}'), ('Stokes', 'v_{t} = \\f{2r^{2}(ρ − σ)g}{9η}'), ('Resonance', 'v = 2f(l_{2} − l_{1})')]
TRAPS = ['Subtract a positive zero error; add a negative one.', 'Errors multiply by the power, and ADD even when quantities divide.', 'In V/I measurements, remember the meter that sits in parallel.',
         'Wider capillary → lower rise; same liquid → same T.', 'Resonance-tube end correction cancels in l₂ − l₁.']
STEPS = [dict(k='s1', t='Instruments', e='📏', cards=['c1', 'c2', 'c3'], need=['meas'], note='Vernier, screw gauge, errors'),
         dict(k='s2', t='Experiments', e='⚗️', cards=['c4', 'c5'], need=['expt'], note='Bridges, pendulum, capillary, viscosity')]
META = dict(unit='phy-u20', subject='phy', n=20, title='Experimental Skills', cls=12, labs=['vernier'],
            syllabus='Familiarity with the basic approach and observations of the experiments and activities: vernier callipers and screw gauge; simple pendulum; metre scale; Young\'s modulus by Searle\'s method; surface tension by capillary rise; coefficient of viscosity by terminal velocity; specific heat capacity; speed of sound using resonance tube; resistivity using metre bridge; Ohm\'s law; galvanometer resistance and figure of merit; focal length of mirrors and lenses; refractive index of a glass slab using a travelling microscope; p-n junction and Zener diode characteristics; identification of diode, LED, resistor and capacitor.')
