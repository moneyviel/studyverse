"""Concept cards for Physics Unit 4 — Work, Energy and Power (written for StudyVerse)."""
TOPICS = {'work': 'Work done by constant and variable forces', 'power': 'Power', 'ke': 'Kinetic energy & the work–energy theorem', 'cons': 'Potential energy, springs & conservation of energy', 'coll': 'Collisions'}
CARDS = [
 dict(id='c1', t='Work', e='🏋️', lvl='f', topic='work',
  body=['Constant force: W = F⃗ · d⃗ = Fd cosθ. Positive when the force helps the motion, negative when it opposes, zero when perpendicular.',
        '<div class="jx-f">Variable force: W = ∫F dx = area under the F–x graph</div>',
        'Gravity and springs are conservative: their work depends only on the end points (mgh, ½kx^{2}). Friction is not: W = μN × path length.',
        'Spring from x_{1} to x_{2}: W = ½k(x_{2}^{2} − x_{1}^{2}).'],
  check=dict(q='F⃗ = 2î + 3ĵ N, d⃗ = 3î − 2ĵ m. W =', o=['12 J', '0 J', '6 J', '13 J'], a=1, why='6 − 6 = 0: the force is perpendicular to the motion.')),
 dict(id='c2', t='Kinetic energy & work–energy theorem', e='⚡', lvl='f', topic='ke',
  body=['K = ½mv^{2} = \\f{p^{2}}{2m}. Same momentum → the lighter body has more KE. K × n → p × √{n}.',
        '<div class="jx-f">W_{net} = ΔK (work by ALL forces)</div>',
        'Projectile: at the top only u cosθ remains → K_{top} = K cos^{2}θ.',
        'Bullet through a plank: fraction of KE lost = 1 − (\\f{v}{u})^{2}.'],
  check=dict(q='KE becomes 4 times. Momentum becomes', o=['2 times', '4 times', '16 times', '√2 times'], a=0, why='p = √(2mK).')),
 dict(id='c3', t='Power', e='🔌', lvl='m', topic='power',
  body=['P = \\f{dW}{dt} = F⃗ · v⃗. Average power = \\f{total work}{time}.',
        'Time-dependent force from rest: integrate a = F/m to get v⃗, then P = F⃗ · v⃗.',
        'Constant power from rest: ½mv^{2} = Pt → v ∝ t^{1/2}, x ∝ t^{3/2}.',
        'Constant force from rest: instantaneous P grows as t, so P_{avg} = ½P_{final}.'],
  check=dict(q='Constant power: speed after time t ∝', o=['t', 't^{1/2}', 't^{2}', 't^{3/2}'], a=1, why='Pt = ½mv².')),
 dict(id='c4', t='Potential energy & conservation', e='🎢', lvl='m', topic='cons',
  body=['U_{gravity} = mgh; U_{spring} = ½kx^{2}. Force = −\\f{dU}{dx}.',
        '<div class="jx-f">No friction: K + U = constant</div>',
        'Hanging spring in equilibrium: x = \\f{mg}{k}, U = \\f{(mg)^{2}}{2k}. Cutting a spring: k × length stays constant.',
        'Loop of radius R: just making the top needs h = 2.5R; if the track pushes with nmg at the top, h = 2R + \\f{(n + 1)R}{2}.'],
  check=dict(q='A spring of constant k is cut in half. Each half has constant', o=['k/2', 'k', '2k', '4k'], a=2, why='k ∝ 1/length.')),
 dict(id='c5', t='Collisions', e='🎱', lvl='h', topic='coll',
  body=['Momentum is conserved in every collision; KE only in elastic ones.',
        '<div class="jx-f">e = \\f{speed of separation}{speed of approach}; e = 1 elastic, e = 0 sticks together</div>',
        'Elastic, target at rest: v_{1} = \\f{m_{1} − m_{2}}{m_{1} + m_{2}}u, v_{2} = \\f{2m_{1}}{m_{1} + m_{2}}u. Equal masses swap velocities.',
        'Bounce with restitution e: rebound height = e^{2}h. Gun recoil: \\f{K_{gun}}{K_{bullet}} = \\f{m}{M}.'],
  check=dict(q='Two equal masses collide elastically head-on; one was at rest. After impact the first ball', o=['stops', 'moves at u/2', 'reverses', 'keeps u'], a=0, why='Equal masses exchange velocities.')),
]
FORMULAS = [('Work', 'W = Fd cosθ = ∫F dx'), ('Work–energy', 'W_{net} = ΔK'), ('KE–momentum', 'K = \\f{p^{2}}{2m}'), ('Power', 'P = F⃗ · v⃗'), ('Spring PE', 'U = ½kx^{2}'),
            ('Elastic (target at rest)', 'v_{2} = \\f{2m_{1}u}{m_{1} + m_{2}}'), ('Restitution', 'h\' = e^{2}h'), ('Loop', 'h_{min} = 2.5R')]
TRAPS = ['Work against gravity is mgh whatever the path — a ramp only spreads it over a longer distance.', 'The work–energy theorem uses the work of ALL forces, including friction.',
         'Same momentum does NOT mean same KE: K = p²/2m.', 'In an inelastic collision momentum is still conserved — only KE is lost.',
         'For a hanging spring, the extra pull-down adds to the stretch already present: U_max uses the total stretch.', 'Cutting a spring makes each piece STIFFER, not softer.']
STEPS = [dict(k='s1', t='Work', e='🏋️', cards=['c1'], need=['work'], note='Dot product, variable force, friction'),
         dict(k='s2', t='Energy & power', e='⚡', cards=['c2', 'c3'], need=['ke', 'power'], note='KE, work–energy theorem, power'),
         dict(k='s3', t='Conservation & collisions', e='🎱', cards=['c4', 'c5'], need=['cons', 'coll'], note='Springs, loops, elastic and inelastic collisions')]
META = dict(unit='phy-u04', subject='phy', n=4, title='Work, Energy and Power', cls=11, labs=['collision'],
            syllabus='Work done by a constant force and a variable force; kinetic and potential energies, work-energy theorem, power. The potential energy of spring conservation of mechanical energy, conservative and non-conservative forces; motion in a vertical circle: Elastic and inelastic collisions in one and two dimensions.')
