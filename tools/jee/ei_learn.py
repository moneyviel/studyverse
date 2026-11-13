"""Concept cards for Physics Unit 14 — Electromagnetic Induction and Alternating Currents (written for StudyVerse)."""
TOPICS = {'flux': 'Faraday & Lenz: changing flux', 'motional': 'Motional emf & generators', 'induct': 'Self & mutual inductance, LR & LC', 'ac': 'AC circuits, resonance & transformers'}
CARDS = [
 dict(id='c1', t='Faraday\'s law & Lenz', e='🧲', lvl='f', topic='flux',
  body=['<div class="jx-f">ε = −N\\f{dΦ}{dt},  Φ = BA cos θ,  q = \\f{NΔΦ}{R}</div>', 'Flux changes if B, the area A, or the angle θ (between B and the normal) changes.',
        'Lenz: the induced current opposes the CHANGE in flux — approaching magnet is repelled, receding one attracted.', 'The charge that flows depends only on the total flux change, not on how fast.'],
  check=dict(q='A loop is moved through a uniform field without leaving it. Induced emf =', o=['0', 'BAv', 'Bℓv', 'depends on speed'], a=0, why='The flux does not change.')),
 dict(id='c2', t='Motional emf', e='🏃', lvl='m', topic='motional',
  body=['<div class="jx-f">ε = Bℓv,  rotating rod: ε = ½BωL^{2},  generator: ε = NBAω sin ωt</div>', 'Only the length perpendicular to v counts: a bent wire acts like the straight line joining its ends.',
        'Rod on rails: I = \\f{Bℓv}{R}, magnetic drag F = \\f{B^{2}ℓ^{2}v}{R}; falling rod reaches v_{t} = \\f{mgR}{B^{2}ℓ^{2}}.', 'Coil: flux is maximum when B ⟂ plane, emf is maximum when B lies in the plane.'],
  check=dict(q='Rod spinning about its centre: potential difference between its ends =', o=['0', '½BωL²', 'BωL²', '¼BωL²'], a=0, why='Both halves give the same rise from the centre.')),
 dict(id='c3', t='Self & mutual inductance', e='🌀', lvl='m', topic='induct',
  body=['<div class="jx-f">ε = −L\\f{dI}{dt},  L = μ_{0}n^{2}Aℓ,  U = ½LI^{2},  ε_{2} = −M\\f{dI_{1}}{dt}</div>', 'L depends on geometry and on the core\'s permeability; it acts like inertia for current.',
        'Small loop at the centre of a big one: M = \\f{μ_{0}πa^{2}}{2b} (field of the big loop × area of the small).'],
  check=dict(q='Doubling the turns of a solenoid (same length) multiplies L by', o=['4', '2', '½', '8'], a=0, why='L ∝ N².')),
 dict(id='c4', t='LR growth & LC oscillations', e='⏱️', lvl='m', topic='induct',
  body=['<div class="jx-f">i = \\f{E}{R}(1 − e^{−t/τ}),  τ = \\f{L}{R};  LC: ω = \\f{1}{√{LC}},  I_{max} = V√{\\f{C}{L}}</div>', 'At the instant of switching on, an inductor acts as an open circuit; long after, as a plain wire.',
        'The voltage across the inductance itself is E − iR. In LC, energy swaps: capacitor keeps cos^{2} ωt, inductor gets sin^{2} ωt.'],
  check=dict(q='Just after closing the switch, current through an ideal inductor is', o=['0', 'E/R', 'E/2R', 'infinite'], a=0, why='Current cannot jump.')),
 dict(id='c5', t='RMS, reactance & phase', e='〰️', lvl='f', topic='ac',
  body=['<div class="jx-f">I_{rms} = \\f{I_{0}}{√{2}},  X_{L} = ωL,  X_{C} = \\f{1}{ωC},  Z = √{R^{2} + (X_{L} − X_{C})^{2}}</div>', 'R: V and I in phase. L: V leads I by 90°. C: I leads V by 90°.',
        'DC + AC: I_{rms}^{2} = I_{dc}^{2} + \\f{I_{0}^{2}}{2}. A ramp 0 → i_{0}: \\f{i_{0}}{√{3}}.'],
  check=dict(q='Raising the frequency makes a capacitor\'s reactance', o=['smaller', 'larger', 'unchanged', 'zero'], a=0, why='X_C = 1/ωC.')),
 dict(id='c6', t='Power & resonance', e='🎯', lvl='m', topic='ac',
  body=['<div class="jx-f">P = V_{rms}I_{rms} cos φ,  cos φ = \\f{R}{Z},  ω_{0} = \\f{1}{√{LC}}</div>', 'At resonance X_{L} = X_{C}, Z = R (smallest), current is greatest and cos φ = 1.',
        'Pure L or C: cos φ = 0 — wattless current. Q-factor \\f{ω_{0}L}{R} measures sharpness.'],
  check=dict(q='At resonance the power factor is', o=['1', '0', '½', '1/√2'], a=0, why='Z = R.')),
 dict(id='c7', t='Transformers', e='🔌', lvl='f', topic='ac',
  body=['<div class="jx-f">\\f{V_{s}}{V_{p}} = \\f{N_{s}}{N_{p}},  η = \\f{V_{s}I_{s}}{V_{p}I_{p}}</div>', 'Step-up raises voltage and lowers current; power can\'t increase.',
        'Losses: copper (I^{2}R), eddy currents (cut by laminating), hysteresis (soft iron), flux leakage. Works only with AC.'],
  check=dict(q='An ideal step-down transformer 10:1 with 2 A in the primary gives secondary current', o=['20 A', '0.2 A', '2 A', '10 A'], a=0, why='Power is conserved.')),
]
FORMULAS = [('Faraday', 'ε = −N\\f{dΦ}{dt}'), ('Charge', 'q = \\f{NΔΦ}{R}'), ('Motional', 'ε = Bℓv'), ('Rotating rod', 'ε = ½BωL^{2}'), ('Generator', 'ε_{0} = NBAω'),
            ('Solenoid', 'L = μ_{0}n^{2}Aℓ'), ('Energy', 'U = ½LI^{2}'), ('LR', 'τ = \\f{L}{R}'), ('LC', 'ω = \\f{1}{√{LC}}'), ('Impedance', 'Z = √{R^{2} + (X_{L} − X_{C})^{2}}'),
            ('Power', 'P = V_{rms}I_{rms} cos φ'), ('Transformer', '\\f{V_{s}}{V_{p}} = \\f{N_{s}}{N_{p}}')]
TRAPS = ['Angle in Φ = BA cos θ is with the NORMAL to the loop, not its plane.', 'Wholly inside a uniform field, a moving loop has no emf.', 'Peak = √2 × rms: mains "220 V" is rms.',
         'Average power uses cos φ; pure L or C dissipates nothing.', 'At resonance V_{L} and V_{C} can each be far larger than the supply voltage — they cancel each other.',
         'Rod rotating about its centre: ends at equal potential.']
STEPS = [dict(k='s1', t='Flux', e='🧲', cards=['c1'], need=['flux'], note='Faraday, Lenz and charge flow'),
         dict(k='s2', t='Motion', e='🏃', cards=['c2'], need=['motional'], note='Rods, discs and generators'),
         dict(k='s3', t='Inductors', e='🌀', cards=['c3', 'c4'], need=['induct'], note='L, M, LR and LC'),
         dict(k='s4', t='AC', e='〰️', cards=['c5', 'c6', 'c7'], need=['ac'], note='Phasors, power, resonance, transformers')]
META = dict(unit='phy-u14', subject='phy', n=14, title='Electromagnetic Induction and Alternating Currents', cls=12, labs=['lcr'],
            syllabus='Electromagnetic induction: Faraday\'s law, induced emf and current; Lenz\'s law, eddy currents; self and mutual inductance. Alternating currents, peak and rms value of alternating current/voltage; reactance and impedance; LCR series circuit, resonance; power in AC circuits, wattless current; AC generator and transformer.')
