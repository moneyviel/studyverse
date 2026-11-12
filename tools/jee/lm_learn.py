"""Concept cards for Physics Unit 3 — Laws of Motion (written for StudyVerse)."""
TOPICS = {'newton': "Newton's laws, momentum & impulse", 'fric': 'Friction & inclined planes', 'pulley': 'Connected bodies, pulleys & equilibrium', 'circd': 'Dynamics of circular motion'}
CARDS = [
 dict(id='c1', t="Newton's three laws", e='🍎', lvl='f', topic='newton',
  body=['1st: no net force → no change in velocity (inertia). 2nd: F⃗ = \\f{dp⃗}{dt} = ma⃗. 3rd: action and reaction are equal, opposite and act on DIFFERENT bodies.',
        '<div class="jx-f">Impulse J = FΔt = Δp = area under the F–t graph</div>',
        'Catching a ball: F = \\f{mv}{t} — pulling the hands back raises t and lowers F.',
        'Lift: apparent weight N = m(g + a) going up with acceleration a, m(g − a) going down; free fall → 0.'],
  check=dict(q='Action and reaction act on', o=['the same body', 'different bodies', 'only on Earth', 'only on moving bodies'], a=1, why='They can never cancel each other.')),
 dict(id='c2', t='Free-body diagrams', e='📐', lvl='m', topic='pulley',
  body=['Draw each body alone, add every force on it (weight, normal, tension, friction, applied), choose axes, write ΣF = ma.',
        'Atwood: a = \\f{(m_{2} − m_{1})g}{m_{1} + m_{2}}, T = \\f{2m_{1}m_{2}g}{m_{1} + m_{2}}.',
        'Blocks pulled in a line: a = \\f{F}{Σm}; a string\'s tension = (mass behind it) × a.',
        'Equilibrium with two strings: resolve horizontally and vertically (or use Lami\'s theorem). Movable pulley: the hanging block moves half as far.'],
  check=dict(q='Atwood with 3 kg and 1 kg: a =', o=['g/4', 'g/2', 'g/3', '2g/3'], a=1, why='(3 − 1)/(3 + 1).')),
 dict(id='c3', t='Friction', e='🧱', lvl='m', topic='fric',
  body=['Static friction adjusts up to μ_{s}N; kinetic friction = μ_{k}N (μ_{k} < μ_{s}). Independent of contact area.',
        'Angle of repose: μ_{s} = tanθ. Sliding down: a = g(sinθ − μ cosθ). Pushing up at steady speed: F = mg(sinθ + μ cosθ).',
        'Pulling at angle θ (steady): F = \\f{μmg}{cosθ + μ sinθ} — lifting a little reduces N and friction.',
        'Rough vs smooth incline time ratio n → μ = tanθ(1 − \\f{1}{n^{2}}).'],
  check=dict(q='A block just slips at 30°. μ_s =', o=['0.5', '1/√3', '√3', '1'], a=1, why='tan 30°.')),
 dict(id='c4', t='Circular motion dynamics', e='🎢', lvl='h', topic='circd',
  body=['Centripetal force is not a new force — it is the net inward force (tension, friction, normal, gravity).',
        '<div class="jx-f">Flat road: v_{max} = √{μrg}. Banked: v^{2} = rg\\f{μ + tanθ}{1 − μ tanθ} (μ = 0 → v^{2} = rg tanθ)</div>',
        'Vertical circle on a string: v_{top} ≥ √{gr}, v_{bottom} ≥ √{5gr}; then T_{bottom} − T_{top} = 6mg.',
        'Coin on a turntable: ω_{max} = √{μg/r}. Rotor wall: μ_{min} = \\f{g}{ω^{2}r}.'],
  check=dict(q='Minimum speed at the bottom of a vertical circle :', o=['√(gr)', '√(5gr)', '√(2gr)', '√(3gr)'], a=1, why='Energy from the top.')),
]
FORMULAS = [('2nd law', 'F = \\f{dp}{dt} = ma'), ('Impulse', 'J = FΔt = Δp'), ('Atwood', 'a = \\f{(m_{2} − m_{1})g}{m_{1} + m_{2}}'), ('Friction', 'f_{k} = μ_{k}N'), ('Repose', 'μ_{s} = tanθ'),
            ('Incline', 'a = g(sinθ − μ cosθ)'), ('Banking', 'v^{2} = rg\\f{μ + tanθ}{1 − μ tanθ}'), ('Vertical circle', 'v_{top} ≥ √{gr}')]
TRAPS = ['Action–reaction pairs never cancel: they act on different bodies.', 'Normal force is not always mg (inclines, lifts, angled pulls).', 'Static friction is "up to" μN, not always μN.',
         'At maximum banked speed friction acts DOWN the slope; at minimum speed, UP.', 'In a lift going up at constant speed the reading is just mg.', 'A movable pulley halves the motion of the hanging block.']
STEPS = [dict(k='s1', t="Newton's laws", e='🍎', cards=['c1'], need=['newton'], note='Force, momentum, impulse, lifts'),
         dict(k='s2', t='Connected bodies', e='📐', cards=['c2'], need=['pulley'], note='Free-body diagrams, pulleys, tensions'),
         dict(k='s3', t='Friction & circles', e='🧱', cards=['c3', 'c4'], need=['fric', 'circd'], note='Friction, inclines, banking, vertical circle')]
META = dict(unit='phy-u03', subject='phy', n=3, title='Laws of Motion', cls=11, labs=['incline'],
            syllabus="Force and inertia, Newton's First law of motion; Momentum, Newton's Second Law of motion, Impulses; Newton's Third Law of motion. Law of conservation of linear momentum and its applications. Equilibrium of concurrent forces. Static and Kinetic friction, laws of friction, rolling friction. Dynamics of uniform circular motion: centripetal force and its applications: vehicle on a level circular road, vehicle on a banked road.")
