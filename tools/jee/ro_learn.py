"""Concept cards for Physics Unit 5 — Rotational Motion (written for StudyVerse)."""
TOPICS = {'com': 'Centre of mass', 'moi': 'Moment of inertia', 'torq': 'Torque & rotational dynamics', 'angmom': 'Angular momentum & its conservation', 'roll': 'Rolling motion'}
CARDS = [
 dict(id='c1', t='Centre of mass', e='🎯', lvl='f', topic='com',
  body=['r⃗_{cm} = \\f{Σm r⃗}{Σm}. For a continuous body use ∫r dm. Symmetric uniform bodies: the centre.',
        'Bent rod or L-shape: treat each straight part as a point mass at its middle.',
        'Cut-outs: treat the hole as NEGATIVE mass. Hole of radius r touching the rim of a disc R: shift = \\f{r^{2}(R − r)}{R^{2} − r^{2}}.',
        'No external force → the CM does not move: m_{1}d_{1} = m_{2}d_{2}.'],
  check=dict(q='Masses 1 kg at x = 0 and 3 kg at x = 4. x_cm =', o=['1', '2', '3', '4'], a=2, why='(0 + 12)/4.')),
 dict(id='c2', t='Moment of inertia', e='🌀', lvl='m', topic='moi',
  body=['I = Σmr^{2} — how hard it is to change the spin. Ring MR^{2}, disc ½MR^{2}, solid sphere \\f{2}{5}MR^{2}, hollow sphere \\f{2}{3}MR^{2}, rod \\f{ML^{2}}{12} (centre), \\f{ML^{2}}{3} (end).',
        '<div class="jx-f">Parallel axis: I = I_{cm} + Md^{2}. Perpendicular axis (flat bodies): I_{z} = I_{x} + I_{y}</div>',
        'Ring/disc about a diameter = half the ⊥ value. Radius of gyration: I = Mk^{2}.',
        'Same material: disc of fixed thickness I ∝ R^{4}; sphere I ∝ R^{5}; cylinder I ∝ R^{4}L.'],
  check=dict(q='Ring about a tangent in its plane :', o=['MR²', '3MR²/2', '2MR²', 'MR²/2'], a=1, why='½MR² + MR².')),
 dict(id='c3', t='Torque & rotational dynamics', e='🔧', lvl='m', topic='torq',
  body=['τ⃗ = r⃗ × F⃗; τ = Iα — the rotational version of F = ma.',
        'Same equations as straight-line motion: ω = ω_{0} + αt, θ = ω_{0}t + ½αt^{2}. From rest, θ in successive equal intervals goes 1 : 3 : 5 …',
        'Block on a string round a pulley: a = \\f{mg}{m + I/R^{2}}; Atwood with a heavy pulley: add I/R^{2} to the masses.',
        'Rotational work and power: W = τθ, P = τω, KE = ½Iω^{2}.'],
  check=dict(q='τ = 2 N m on I = 0.5 kg m². α =', o=['1', '2', '4', '0.25'], a=2, why='τ/I.')),
 dict(id='c4', t='Angular momentum', e='⛸️', lvl='m', topic='angmom',
  body=['Particle: L⃗ = r⃗ × p⃗, |L| = mv × (perpendicular distance of the line of motion). Rigid body: L = Iω.',
        '<div class="jx-f">\\f{dL}{dt} = τ; no external torque → Iω = constant</div>',
        'Skater pulls arms in: I falls, ω rises. Two discs joined: ω = \\f{I_{1}ω_{1} + I_{2}ω_{2}}{I_{1} + I_{2}} — KE is LOST (like a sticky collision).',
        'Uniform circular motion: force is towards the centre, opposite to r⃗.'],
  check=dict(q='A spinning disc (I) gets an identical disc dropped on it. ω becomes', o=['ω', 'ω/2', '2ω', 'ω/4'], a=1, why='Iω = 2Iω\'.')),
 dict(id='c5', t='Rolling', e='🛞', lvl='h', topic='roll',
  body=['Rolling without slipping: v = ωR. Top of the wheel moves at 2v, the contact point is at rest, the side point at √{2}v.',
        '<div class="jx-f">K = ½mv^{2}(1 + \\f{k^{2}}{R^{2}}); down an incline a = \\f{g sinθ}{1 + k^{2}/R^{2}}</div>',
        'Fastest down a slope: solid sphere, then disc/cylinder, then hollow sphere, then ring. Smooth slope: no friction torque, so no spin change.',
        'Sliding + spinning on a rough floor: friction slows v and speeds ω until v = ωR, then pure rolling begins.'],
  check=dict(q='Which reaches the bottom first?', o=['Ring', 'Disc', 'Solid sphere', 'Hollow sphere'], a=2, why='Smallest k²/R² = 2/5.')),
]
FORMULAS = [('Centre of mass', 'x_{cm} = \\f{Σmx}{Σm}'), ('Parallel axis', 'I = I_{cm} + Md^{2}'), ('Perpendicular axis', 'I_{z} = I_{x} + I_{y}'), ('Torque', 'τ = Iα'), ('Angular momentum', 'L = Iω'),
            ('Rotational KE', '½Iω^{2}'), ('Rolling KE', '½mv^{2}(1 + k^{2}/R^{2})'), ('Rolling on incline', 'a = \\f{g sinθ}{1 + k^{2}/R^{2}}')]
TRAPS = ['The moment of inertia depends on the axis — always say which axis.', 'Parallel axis theorem only starts from an axis through the CENTRE of mass.',
         'Perpendicular axis theorem works only for flat (2-D) bodies.', 'Joining two spinning discs keeps angular momentum but loses kinetic energy.',
         'On a smooth incline a rolling body keeps its spin — only its translational KE turns into height.', 'Torque is r × F, not F × r: the order fixes the sign.']
STEPS = [dict(k='s1', t='Centre of mass & inertia', e='🎯', cards=['c1', 'c2'], need=['com', 'moi'], note='CM, I of common bodies, axis theorems'),
         dict(k='s2', t='Torque & angular momentum', e='🔧', cards=['c3', 'c4'], need=['torq', 'angmom'], note='τ = Iα, pulleys, conservation of L'),
         dict(k='s3', t='Rolling', e='🛞', cards=['c5'], need=['roll'], note='Rolling KE, inclines, slipping to rolling')]
META = dict(unit='phy-u05', subject='phy', n=5, title='Rotational Motion', cls=11, labs=['roll'],
            syllabus='Centre of the mass of a two-particle system, Centre of the mass of a rigid body; Basic concepts of rotational motion; moment of a force; torque, angular momentum, conservation of angular momentum and its applications; The moment of inertia, the radius of gyration, values of moments of inertia for simple geometrical objects, parallel and perpendicular axes theorems, and their applications. Equilibrium of rigid bodies, rigid body rotation and equations of rotational motion, comparison of linear and rotational motions.')
