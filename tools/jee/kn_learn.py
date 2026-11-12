"""Concept cards for Physics Unit 2 — Kinematics (written for StudyVerse)."""
TOPICS = {'line': 'Motion in a straight line', 'proj': 'Projectile motion', 'rel': 'Relative velocity, river & rain', 'circ': 'Vectors in a plane & circular motion'}
CARDS = [
 dict(id='c1', t='Describing motion on a line', e='📏', lvl='f', topic='line',
  body=['Distance is the path length; displacement is the straight change of position (can be zero). Average speed = distance/time; average velocity = displacement/time.',
        '<div class="jx-f">v = \\f{dx}{dt},  a = \\f{dv}{dt} = v\\f{dv}{dx}</div>',
        'Graphs: slope of x–t = v; slope of v–t = a; area under v–t = displacement.',
        'Equal distances at v_{1}, v_{2} → average speed \\f{2v_{1}v_{2}}{v_{1} + v_{2}}; equal times → \\f{v_{1} + v_{2}}{2}.'],
  check=dict(q='Area under a v–t graph gives', o=['acceleration', 'displacement', 'speed', 'jerk'], a=1, why='∫v dt.')),
 dict(id='c2', t='Constant acceleration', e='🚗', lvl='m', topic='line',
  body=['<div class="jx-f">v = u + at,  s = ut + ½at^{2},  v^{2} = u^{2} + 2as,  s_{n} = u + \\f{a}{2}(2n − 1)</div>',
        'Stopping distance = \\f{u^{2}}{2a} (∝ u^{2}: double the speed, four times the distance).',
        'Free fall: a = g downward. Thrown up and down from a tower in t_{1}, t_{2} → dropped takes √{t_{1}t_{2}}.',
        'If x(t) is a polynomial, differentiate: x = t^{3} − 6t^{2} → v = 3t^{2} − 12t, a = 6t − 12.'],
  check=dict(q='u = 0, a = 2, t = 5 → s =', o=['10', '25', '50', '5'], a=1, why='½ × 2 × 25.')),
 dict(id='c3', t='Projectile motion', e='🏀', lvl='m', topic='proj',
  body=['Horizontal: no acceleration (u cosθ constant). Vertical: a = −g.',
        '<div class="jx-f">T = \\f{2u sinθ}{g},  H = \\f{u^{2}sin^{2}θ}{2g},  R = \\f{u^{2}sin2θ}{g}</div>',
        'Max range at 45°; θ and (90° − θ) give the same range. R = nH ⇔ tanθ = \\f{4}{n} (R = H at tan^{−1}4).',
        'Thrown horizontally from height h: t = √{2h/g}, range = u√{2h/g}. Path: y = x tanθ − \\f{gx^{2}}{2u^{2}cos^{2}θ}.'],
  check=dict(q='Same range as 30° :', o=['45°', '60°', '15°', '75°'], a=1, why='Complementary angles.')),
 dict(id='c4', t='Relative velocity', e='🚣', lvl='m', topic='rel',
  body=['<div class="jx-f">v⃗_{AB} = v⃗_{A} − v⃗_{B}</div>',
        'River: least TIME → head straight across (t = d/v_{b}, drift = v_{r}t). Least DRIFT (if v_{b} > v_{r}) → aim upstream at sinθ = v_{r}/v_{b}, t = \\f{d}{√{v_{b}^{2} − v_{r}^{2}}}.',
        'Rain: find v⃗_{rain} − v⃗_{man}; tilt the umbrella against that relative velocity.',
        'Ball thrown up inside a moving boat: the ground observer sees the boat\'s horizontal speed added.'],
  check=dict(q='To cross fastest you should head', o=['upstream', 'straight across', 'downstream', 'at 45°'], a=1, why='Full speed across.')),
 dict(id='c5', t='Circular motion and vectors', e='🎡', lvl='m', topic='circ',
  body=['<div class="jx-f">ω = \\f{2π}{T} = 2πf,  v = ωr,  a_{c} = \\f{v^{2}}{r} = ω^{2}r</div>',
        'Uniform circular motion: speed constant, velocity and acceleration change direction. Non-uniform: add a_{t} = \\f{dv}{dt}.',
        'Displacement after angle θ on a circle = 2r sin\\f{θ}{2}; distance = rθ.',
        'Under r⃗ → −r⃗: v⃗, p⃗, a⃗ flip but L⃗ = r⃗ × p⃗ does not (an axial vector).'],
  check=dict(q='Half a circle of radius r: displacement =', o=['πr', '2r', 'r', '0'], a=1, why='The diameter.')),
]
FORMULAS = [('Velocity', 'v = u + at'), ('Displacement', 's = ut + ½at^{2}'), ('Third', 'v^{2} = u^{2} + 2as'), ('nth second', 's_{n} = u + \\f{a}{2}(2n − 1)'), ('Range', 'R = \\f{u^{2}sin2θ}{g}'),
            ('Height', 'H = \\f{u^{2}sin^{2}θ}{2g}'), ('Flight time', 'T = \\f{2u sinθ}{g}'), ('Relative', 'v⃗_{AB} = v⃗_{A} − v⃗_{B}'), ('Centripetal', 'a = \\f{v^{2}}{r} = ω^{2}r')]
TRAPS = ['Average speed for equal distances is the harmonic mean, not the simple average.', 'At the top of a projectile, speed is u cosθ — not zero.', 'Max range is at 45° only on level ground.',
         'Least time and least drift are different river crossings.', 'Displacement on a circle uses the chord, not the arc.', 'Convert km/h to m/s: multiply by 5/18.']
STEPS = [dict(k='s1', t='Straight line', e='📏', cards=['c1', 'c2'], need=['line'], note='Graphs and the equations of motion'),
         dict(k='s2', t='Projectiles', e='🏀', cards=['c3'], need=['proj'], note='Range, height, flight time'),
         dict(k='s3', t='Relative & circular', e='🚣', cards=['c4', 'c5'], need=['rel', 'circ'], note='River, rain, vectors, circular motion')]
META = dict(unit='phy-u02', subject='phy', n=2, title='Kinematics', cls=11, labs=['projectile'],
            syllabus="The frame of reference, motion in a straight line, Position- time graph, speed and velocity; Uniform and non-uniform motion, average speed and instantaneous velocity, uniformly accelerated motion, velocity-time, position-time graph, relations for uniformly accelerated motion, Scalars and Vectors, Vector. Addition and subtraction, scalar and vector products, Unit Vector, Resolution of a Vector. Relative Velocity, Motion in a plane, Projectile Motion, Uniform Circular Motion.")
