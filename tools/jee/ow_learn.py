"""Concept cards for Physics Unit 10 — Oscillations and Waves (written for StudyVerse)."""
TOPICS = {'shm': 'Simple harmonic motion', 'osc': 'Springs & pendulums', 'wave': 'Travelling waves & superposition', 'sound': 'Pipes, strings & beats'}
CARDS = [
 dict(id='c1', t='Simple harmonic motion', e='〰️', lvl='f', topic='shm',
  body=['SHM: a = −ω^{2}x. Then x = A sin(ωt + φ), v = ω√{A^{2} − x^{2}}, v_{max} = Aω, a_{max} = ω^{2}A, T = \\f{2π}{ω}.',
        '<div class="jx-f">E = ½mω^{2}A^{2}; U = ½kx^{2}; K = ½k(A^{2} − x^{2})</div>',
        'K and U each oscillate at 2ω. From an extreme: x = A cos ωt — reaching A/2 takes T/6, A/√2 takes T/8, √3A/2 takes T/12.',
        'Two SHMs of the same ω add like vectors: A^{2} = a_{1}^{2} + a_{2}^{2} + 2a_{1}a_{2}cosφ.'],
  check=dict(q='At x = A/2 the kinetic energy is what fraction of the total?', o=['1/4', '1/2', '3/4', '1'], a=2, why='1 − (1/2)².')),
 dict(id='c2', t='Springs and pendulums', e='🕰️', lvl='f', topic='osc',
  body=['Spring: T = 2π√{\\f{m}{k}} (same hanging or on a table). Pendulum: T = 2π√{\\f{L}{g}} (small swings, mass does not matter).',
        'Springs in parallel: k = k_{1} + k_{2}; in series: \\f{1}{k} = \\f{1}{k_{1}} + \\f{1}{k_{2}}. Cutting a spring to 1/n of its length makes it n times stiffer.',
        'Rigid body swinging about a pivot: T = 2π√{\\f{I}{mgd}} (d = pivot to centre of mass).',
        'Floating block bobbing: k = ρAg, so T = 2π√{\\f{m}{ρAg}}.'],
  check=dict(q='A pendulum is made 4 times longer. Its period becomes', o=['2×', '4×', '½×', '16×'], a=0, why='T ∝ √L.')),
 dict(id='c3', t='Travelling waves', e='🌊', lvl='m', topic='wave',
  body=['y = A sin(kx − ωt) moves towards +x; kx + ωt moves towards −x. k = \\f{2π}{λ}, ω = 2πf, v = \\f{ω}{k} = fλ.',
        '<div class="jx-f">String: v = √{\\f{T}{μ}}; solid rod: √{\\f{Y}{ρ}}; gas: √{\\f{γRT}{M}} (v ∝ √{T})</div>',
        'Superposition: same-frequency waves add as phasors. Intensity ∝ A^{2}: coherent I = I_{1} + I_{2} + 2√{I_{1}I_{2}}cosφ, incoherent I_{1} + I_{2}.',
        'cos a·cos b = ½[cos(a + b) + cos(a − b)]: a "beating" wave is two waves with ω differing by 2a.'],
  check=dict(q='y = sin(4x + 8t) moves with speed', o=['2 towards +x', '2 towards −x', '0.5 towards −x', '32'], a=1, why='ω/k = 2, sign + → −x.')),
 dict(id='c4', t='Standing waves: pipes and strings', e='🎺', lvl='h', topic='sound',
  body=['String fixed at both ends and an open pipe: all harmonics, f_{n} = \\f{nv}{2L}.',
        'Closed pipe (one end shut): only ODD harmonics, f = \\f{(2n − 1)v}{4L}. Its k-th overtone is the (2k + 1)-th harmonic.',
        'Same tension → f ∝ \\f{1}{L}; f ∝ √{T} for a string. Water poured in a closed pipe shortens the air column and raises the pitch.',
        'Beats = |f_{1} − f_{2}|. Wax LOWERS a fork\'s frequency; filing raises it — use that to decide the sign.'],
  check=dict(q='A closed pipe can NOT produce its', o=['1st harmonic', '3rd harmonic', '4th harmonic', '5th harmonic'], a=2, why='Only odd harmonics.')),
]
FORMULAS = [('SHM speed', 'v = ω√{A^{2} − x^{2}}'), ('SHM energy', 'E = ½mω^{2}A^{2}'), ('Spring', 'T = 2π√{\\f{m}{k}}'), ('Pendulum', 'T = 2π√{\\f{L}{g}}'), ('Wave speed', 'v = fλ = \\f{ω}{k}'),
            ('String', 'v = √{\\f{T}{μ}}'), ('Open pipe', 'f_{n} = \\f{nv}{2L}'), ('Closed pipe', 'f = \\f{(2n − 1)v}{4L}'), ('Beats', 'f_{b} = |f_{1} − f_{2}|')]
TRAPS = ['Kinetic and potential energy in SHM oscillate at TWICE the SHM frequency.', 'A closed pipe has only odd harmonics: its "first overtone" is the 3rd harmonic.',
         'kx + ωt is a wave moving towards −x.', 'A pendulum\'s period does not depend on the mass of the bob.',
         'Total energy of a spring oscillator depends on k and A, not on the mass.', 'Distance in SHM: each quarter period covers A, but the displacement depends on where it started.']
STEPS = [dict(k='s1', t='SHM', e='〰️', cards=['c1', 'c2'], need=['shm', 'osc'], note='Equation, energy, springs, pendulums'),
         dict(k='s2', t='Waves', e='🌊', cards=['c3'], need=['wave'], note='Wave equation, speed, superposition'),
         dict(k='s3', t='Sound', e='🎺', cards=['c4'], need=['sound'], note='Pipes, strings, beats')]
META = dict(unit='phy-u10', subject='phy', n=10, title='Oscillations and Waves', cls=11, labs=['pipe'],
            syllabus='Oscillations and periodic motion – time period, frequency, displacement as a function of time. Periodic functions. Simple harmonic motion (S.H.M.) and its equation; phase: oscillations of a spring - restoring force and force constant: energy in S.H.M. - Kinetic and potential energies; Simple pendulum - derivation of expression for its time period: Wave motion. Longitudinal and transverse waves, speed of travelling wave. Displacement relation for a progressive wave. Principle of superposition of waves, a reflection of waves. Standing waves in strings and organ pipes, fundamental mode and harmonics. Beats.')
