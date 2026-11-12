"""Concept cards for Physics Unit 6 — Gravitation (written for StudyVerse)."""
TOPICS = {'law': "Newton's law & superposition", 'g': 'Acceleration due to gravity', 'pot': 'Potential energy & escape speed', 'orbit': 'Satellites & Kepler\'s laws'}
CARDS = [
 dict(id='c1', t="Newton's law of gravitation", e='🍎', lvl='f', topic='law',
  body=['<div class="jx-f">F = \\f{Gm_{1}m_{2}}{r^{2}},  G = 6.67 × 10^{−11} N m^{2} kg^{−2}</div>', 'Forces add as vectors (superposition). Equal masses placed symmetrically around a point give zero field there.',
        'Field of a uniform shell is zero inside; outside, a sphere acts as if all its mass sat at the centre.', 'Gravity is ~10^{39} times weaker than the electric force between an electron and a proton.'],
  check=dict(q='Distance doubled, force becomes :', o=['½', '¼', '2×', '4×'], a=1, why='F ∝ 1/r².')),
 dict(id='c2', t='g at height, depth and on other planets', e='🌍', lvl='m', topic='g',
  body=['<div class="jx-f">g = \\f{GM}{R^{2}},  g_{h} = g(\\f{R}{R + h})^{2} ≈ g(1 − \\f{2h}{R}),  g_{d} = g(1 − \\f{d}{R})</div>', 'g is largest at the surface; it falls going up AND going down.',
        'Other planet: g ∝ \\f{M}{R^{2}} = \\f{4}{3}πGρR. Pendulum period T = 2π√{\\f{L}{g}} changes with g, not with the bob\'s mass.', 'If the earth shrank with the same mass, angular momentum stays the same: day length ∝ R^{2}.'],
  check=dict(q='g at height h = R :', o=['g/2', 'g/4', 'g/8', '2g'], a=1, why='(R/2R)² = ¼.')),
 dict(id='c3', t='Potential energy and escape speed', e='🚀', lvl='m', topic='pot',
  body=['<div class="jx-f">U = −\\f{GMm}{r},  V = −\\f{GM}{r},  v_{e} = √{\\f{2GM}{R}} = √{2gR} ≈ 11.2 km/s</div>', 'U is zero at infinity and negative everywhere else. Energy to send a body to infinity from the surface = \\f{GMm}{R} = mgR.',
        'Raising a body to height h: ΔU = mgR(1 − \\f{R}{R + h}) — equals mgh only when h ≪ R.', 'v_{e} ∝ √{\\f{M}{R}} ∝ R√{ρ}; it does not depend on the mass of the body or the direction of launch.'],
  check=dict(q='KE to escape from the surface :', o=['½mgR', 'mgR', '2mgR', 'mgR/4'], a=1, why='GMm/R = mgR.')),
 dict(id='c4', t='Satellites and Kepler', e='🛰️', lvl='m', topic='orbit',
  body=['<div class="jx-f">v_{o} = √{\\f{GM}{r}},  T = 2π√{\\f{r^{3}}{GM}},  KE = \\f{GMm}{2r},  E = −\\f{GMm}{2r}</div>', 'Kepler: orbits are ellipses; equal areas in equal times (angular momentum constant, central force); T^{2} ∝ r^{3}.',
        'Close to the surface: v = √{gR} ≈ 7.9 km/s, T ≈ 84 min, and T = √{\\f{3π}{Gρ}} depends only on the density.', 'Geostationary: T = 24 h, r ≈ 42 000 km, above the equator. Moving to a bigger orbit needs energy \\f{GMm}{2}(\\f{1}{r_{1}} − \\f{1}{r_{2}}).'],
  check=dict(q='Orbit radius ×4, period becomes :', o=['×2', '×4', '×8', '×16'], a=2, why='T ∝ r^{3/2}.')),
]
FORMULAS = [('Newton', 'F = \\f{Gm_{1}m_{2}}{r^{2}}'), ('Surface g', 'g = \\f{GM}{R^{2}}'), ('Height', 'g_{h} = g(\\f{R}{R + h})^{2}'), ('Depth', 'g_{d} = g(1 − \\f{d}{R})'), ('Potential energy', 'U = −\\f{GMm}{r}'),
            ('Escape speed', 'v_{e} = √{\\f{2GM}{R}} = √{2gR}'), ('Orbital speed', 'v_{o} = √{\\f{GM}{r}}'), ('Period', 'T = 2π√{\\f{r^{3}}{GM}}'), ('Orbit energy', 'E = −\\f{GMm}{2r}'), ('Angular momentum', 'L = m√{GMr}')]
TRAPS = ['Height from the SURFACE vs distance from the CENTRE: r = R + h.', 'g falls both above and below the surface.', 'Total energy of an orbit is negative; KE = −E.', 'Escape speed does not depend on the launch angle or the body\'s mass.',
         'T^{2} ∝ r^{3} only for the same central mass.', 'Energy to escape is mgR, not ½mgR.']
STEPS = [dict(k='s1', t='The law', e='🍎', cards=['c1', 'c2'], need=['law', 'g'], note="Newton's law, superposition and g"),
         dict(k='s2', t='Energy', e='🚀', cards=['c3'], need=['pot'], note='Potential energy and escape speed'),
         dict(k='s3', t='Orbits', e='🛰️', cards=['c4'], need=['orbit'], note='Satellites, energy of orbits and Kepler')]
META = dict(unit='phy-u06', subject='phy', n=6, title='Gravitation', cls=11, labs=['orbit'],
            syllabus="The universal law of gravitation; acceleration due to gravity and its variation with altitude and depth; Kepler's laws of planetary motion; gravitational potential energy; gravitational potential; escape velocity; motion of a satellite, orbital velocity, time period and energy of satellite.")
