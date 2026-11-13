"""Concept cards for Physics Unit 13 — Magnetic Effects of Current and Magnetism (written for StudyVerse)."""
TOPICS = {'field': 'Field of currents (Biot–Savart & Ampère)', 'force': 'Force on charges and wires', 'moment': 'Torque, dipoles & magnetic materials', 'galv': 'Galvanometer, ammeter & voltmeter'}
CARDS = [
 dict(id='c1', t='Biot–Savart: building blocks', e='🧲', lvl='f', topic='field',
  body=['<div class="jx-f">dB = \\f{μ_{0}}{4π}\\f{I dl sin θ}{r^{2}},  μ_{0} = 4π × 10^{−7} T m/A</div>', 'Finite wire: B = \\f{μ_{0}I}{4πd}(sin α_{1} + sin α_{2}); infinite wire: \\f{μ_{0}I}{2πd}; a point on the wire\'s own line gets zero.',
        'Ring centre: \\f{μ_{0}NI}{2R}; an arc of angle φ: \\f{μ_{0}I}{4πR}φ; on the axis: \\f{μ_{0}IR^{2}}{2(R^{2} + x^{2})^{3/2}}.', 'Direction: right-hand grip — thumb along current, fingers curl with B.'],
  check=dict(q='Field at the centre of a semicircle (radius R) compared with a full ring :', o=['half', 'same', 'double', 'quarter'], a=0, why='φ = π instead of 2π.')),
 dict(id='c2', t='Ampère\'s law & solenoids', e='🌀', lvl='m', topic='field',
  body=['<div class="jx-f">∮ \\vec{B}·d\\vec{l} = μ_{0}I_{enclosed}</div>', 'Long solenoid: B = μ_{0}nI inside, ≈ 0 outside; at an end, half of that. Toroid: B = \\f{μ_{0}NI}{2πr}.',
        'Thick wire of radius R: B = \\f{μ_{0}Ir}{2πR^{2}} inside (grows with r), \\f{μ_{0}I}{2πr} outside.', 'Fields of several wires add as vectors — find each, then combine.'],
  check=dict(q='Inside a long hollow pipe carrying current, B =', o=['0', 'μ₀I/2πr', 'μ₀nI', 'μ₀I/2R'], a=0, why='No current is enclosed.')),
 dict(id='c3', t='Lorentz force & circular motion', e='🌐', lvl='m', topic='force',
  body=['<div class="jx-f">\\vec{F} = q(\\vec{E} + \\vec{v} × \\vec{B}),  r = \\f{mv}{qB} = \\f{√{2mK}}{qB},  T = \\f{2πm}{qB}</div>', 'The magnetic force is ⟂ v, so it does no work — speed and kinetic energy stay fixed.',
        'Velocity at an angle: helix with pitch v_{∥}T. Crossed fields pass undeflected when v = \\f{E}{B}.', 'Cyclotron frequency \\f{qB}{2πm} does not depend on speed.'],
  check=dict(q='Doubling speed in the same field changes the period by :', o=['nothing', '×2', '×½', '×4'], a=0, why='T = 2πm/qB has no v.')),
 dict(id='c4', t='Force on wires', e='⚡', lvl='f', topic='force',
  body=['<div class="jx-f">\\vec{F} = I\\vec{L} × \\vec{B},  \\f{F}{L} = \\f{μ_{0}I_{1}I_{2}}{2πd}</div>', 'Parallel currents attract, antiparallel repel.',
        'A bent wire in a uniform field feels the same force as the straight line joining its ends; a closed loop feels zero net force.'],
  check=dict(q='Closed loop in a uniform field: net force =', o=['0', 'BIL', '2BIL', 'BIA'], a=0, why='The effective length is zero.')),
 dict(id='c5', t='Magnetic moment & torque', e='🔄', lvl='m', topic='moment',
  body=['<div class="jx-f">\\vec{m} = NI\\vec{A},  \\vec{τ} = \\vec{m} × \\vec{B},  U = −\\vec{m}·\\vec{B}</div>', 'Work to turn from θ_{1} to θ_{2}: mB(cos θ_{1} − cos θ_{2}). Stable at θ = 0, unstable at 180°.',
        'Bar magnet: axial field \\f{μ_{0}}{4π}\\f{2m}{d^{3}}, equatorial \\f{μ_{0}}{4π}\\f{m}{d^{3}}. Orbiting charge: m = \\f{q}{2m_{e}}L.', 'Same wire into a ring (m = \\f{IL^{2}}{4π}) gives more moment than any polygon.'],
  check=dict(q='τ is greatest when m and B are at :', o=['90°', '0°', '180°', '45°'], a=0, why='τ = mB sin θ.')),
 dict(id='c6', t='Magnetic materials', e='🧱', lvl='m', topic='moment',
  body=['<div class="jx-f">B = μ_{0}(H + M),  M = χH,  μ_{r} = 1 + χ</div>', 'Diamagnetic: χ small negative (Bi, Cu, water), pushed out of strong fields. Paramagnetic: χ small positive, χ ∝ \\f{1}{T} (Curie). Ferromagnetic: χ huge, becomes paramagnetic above the Curie temperature.',
        'Hysteresis: retentivity = B left at H = 0; coercivity = reverse H to wipe it. Permanent magnets want both large; electromagnet cores want small coercivity and narrow loops.'],
  check=dict(q='Soft iron suits transformer cores because of its :', o=['low coercivity', 'high retentivity', 'negative χ', 'low μ'], a=0, why='Narrow loop → little energy lost per cycle.')),
 dict(id='c7', t='Moving-coil galvanometer & meters', e='📟', lvl='m', topic='galv',
  body=['<div class="jx-f">NIAB = kθ,  current sensitivity \\f{θ}{I} = \\f{NAB}{k},  voltage sensitivity \\f{NAB}{kR_{G}}</div>', 'Ammeter: low shunt in parallel, S = \\f{I_{g}G}{I − I_{g}}. Voltmeter: big series resistor, R = \\f{V}{I_{g}} − G.',
        'Radial field keeps sin θ = 1 so the scale is linear. Doubling turns doubles current sensitivity but (with doubled resistance) leaves voltage sensitivity unchanged.'],
  check=dict(q='An ideal ammeter has resistance :', o=['zero', 'infinite', 'equal to G', '1 Ω'], a=0, why='It must not change the current it measures.')),
]
FORMULAS = [('Long wire', 'B = \\f{μ_{0}I}{2πd}'), ('Ring centre', 'B = \\f{μ_{0}NI}{2R}'), ('Solenoid', 'B = μ_{0}nI'), ('Lorentz', '\\vec{F} = q\\vec{v} × \\vec{B}'),
            ('Radius', 'r = \\f{mv}{qB}'), ('Period', 'T = \\f{2πm}{qB}'), ('Parallel wires', '\\f{F}{L} = \\f{μ_{0}I_{1}I_{2}}{2πd}'), ('Torque', 'τ = NIAB sin θ'),
            ('Energy', 'U = −mB cos θ'), ('Shunt', 'S = \\f{I_{g}G}{I − I_{g}}'), ('Voltmeter', 'R = \\f{V}{I_{g}} − G'), ('Materials', 'μ_{r} = 1 + χ')]
TRAPS = ['Magnetic force never changes speed — no work is done.', 'The angle in τ = mB sin θ is between the MOMENT (the coil\'s axis) and B, not the coil\'s plane and B.',
         'A point on the line of a straight wire gets no field from it.', 'Field midway between wires: same-direction currents CANCEL there.', 'Shunts go in parallel, multiplier resistors in series.',
         'Electrons bend the opposite way to protons — flip the force direction for negative charges.']
STEPS = [dict(k='s1', t='Sources', e='🧲', cards=['c1', 'c2'], need=['field'], note='Wires, rings, arcs and solenoids'),
         dict(k='s2', t='Forces', e='🌐', cards=['c3', 'c4'], need=['force'], note='Charges in circles and helices; wires pushing wires'),
         dict(k='s3', t='Dipoles', e='🔄', cards=['c5', 'c6'], need=['moment'], note='Torque, energy and materials'),
         dict(k='s4', t='Meters', e='📟', cards=['c7'], need=['galv'], note='Turning a galvanometer into an ammeter or voltmeter')]
META = dict(unit='phy-u13', subject='phy', n=13, title='Magnetic Effects of Current and Magnetism', cls=12, labs=['helix'],
            syllabus='Biot–Savart law and its application to current carrying circular loop. Ampère\'s law and its applications to infinitely long current carrying straight wire and solenoid. Force on a moving charge in uniform magnetic and electric fields. Force on a current-carrying conductor in a uniform magnetic field. Force between two parallel current-carrying conductors — definition of ampere. Torque experienced by a current loop in uniform magnetic field; moving coil galvanometer, its sensitivity and conversion to ammeter and voltmeter. Current loop as a magnetic dipole and its magnetic dipole moment. Bar magnet as an equivalent solenoid, magnetic field lines; magnetic field due to a magnetic dipole (bar magnet) along its axis and perpendicular to its axis. Torque on a magnetic dipole in a uniform magnetic field. Para-, dia- and ferro-magnetic substances with examples, effect of temperature on magnetic properties.')
