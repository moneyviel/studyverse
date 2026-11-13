"""Concept cards for Mathematics Unit 14 — Trigonometry (written for StudyVerse)."""
TOPICS = {'id': 'Ratios & identities', 'inv': 'Inverse trigonometric functions', 'eqn': 'Trigonometric equations'}
CARDS = [
 dict(id='c1', t='Ratios on the unit circle', e='⭕', lvl='f', topic='id',
  body=['A point at angle θ on the unit circle is (cos θ, sin θ); tan θ = \\f{sin θ}{cos θ}.',
        'Signs by quadrant — I: all +, II: sin +, III: tan +, IV: cos +.',
        'sin^{2}θ + cos^{2}θ = 1, 1 + tan^{2}θ = sec^{2}θ, 1 + cot^{2}θ = cosec^{2}θ.'],
  check=dict(q='If sin x = \\f{3}{5} with x in quadrant II, cos x =', o=['−\\f{4}{5}', '\\f{4}{5}', '−\\f{3}{4}', '\\f{3}{4}'], a=0, why='cos < 0 in quadrant II.')),
 dict(id='c2', t='Compound & multiple angles', e='🔁', lvl='m', topic='id',
  body=['sin(A ± B) = sin A cos B ± cos A sin B; cos(A ± B) = cos A cos B ∓ sin A sin B; tan(A ± B) = \\f{tan A ± tan B}{1 ∓ tan A tan B}.',
        'sin 2A = 2 sin A cos A; cos 2A = 1 − 2sin^{2}A = 2cos^{2}A − 1; sin 3A = 3 sin A − 4sin^{3}A; cos 3A = 4cos^{3}A − 3 cos A.',
        'sin θ sin(60° − θ) sin(60° + θ) = \\f{1}{4}sin 3θ (same pattern for cos and tan). a sin x + b cos x ranges over ±√{a^{2} + b^{2}}.'],
  check=dict(q='cos 75° =', o=['\\f{√{6} − √{2}}{4}', '\\f{√{6} + √{2}}{4}', '\\f{1}{2}', '\\f{√{3}}{2}'], a=0, why='cos(45° + 30°).')),
 dict(id='c3', t='Inverse functions', e='↩️', lvl='m', topic='inv',
  body=['Principal ranges: sin^{−1}: [−\\f{π}{2}, \\f{π}{2}], cos^{−1}: [0, π], tan^{−1}: (−\\f{π}{2}, \\f{π}{2}), cot^{−1}: (0, π).',
        'sin^{−1}x + cos^{−1}x = \\f{π}{2}; tan^{−1}x + cot^{−1}x = \\f{π}{2}; sin^{−1}(sin θ) = θ only when θ is in the principal range.',
        'tan^{−1}a ± tan^{−1}b = tan^{−1}\\f{a ± b}{1 ∓ ab} (when ab < 1 for +). Telescoping: \\f{(k + 1) − k}{1 + k(k + 1)}.'],
  check=dict(q='sin^{−1}(sin \\f{5π}{6}) =', o=['\\f{π}{6}', '\\f{5π}{6}', '−\\f{π}{6}', '\\f{π}{3}'], a=0, why='Bring back into [−\\f{π}{2}, \\f{π}{2}].')),
 dict(id='c4', t='Solving equations', e='🎯', lvl='h', topic='eqn',
  body=['sin x = sin α ⇒ x = nπ + (−1)^{n}α; cos x = cos α ⇒ x = 2nπ ± α; tan x = tan α ⇒ x = nπ + α.',
        'Quadratics in sin x or cos x: keep only roots in [−1, 1]. Each value in (−1, 1) is hit twice per 2π.',
        'Counting on an interval: list the solutions or count periods; watch endpoints and values ±1 (hit once per period).'],
  check=dict(q='Number of solutions of sin x = \\f{1}{2} in [0, 2π]:', o=['2', '1', '4', '3'], a=0, why='\\f{π}{6} and \\f{5π}{6}.')),
]
FORMULAS = [('Pythagoras', 'sin^{2}θ + cos^{2}θ = 1'), ('Sum', 'sin(A + B) = sin A cos B + cos A sin B'), ('Double', 'cos 2A = 2cos^{2}A − 1'), ('Triple', 'sin 3A = 3 sin A − 4sin^{3}A'),
            ('Range', '|a sin x + b cos x| ≤ √{a^{2} + b^{2}}'), ('Inverse sum', 'sin^{−1}x + cos^{−1}x = \\f{π}{2}'), ('tan^{−1} sum', 'tan^{−1}\\f{a + b}{1 − ab}'), ('General solution', 'x = nπ + (−1)^{n}α')]
TRAPS = ['Check the quadrant before choosing the sign of a ratio.', 'sin^{−1}(sin θ) ≠ θ outside [−\\f{π}{2}, \\f{π}{2}].', 'Squaring an equation can add false solutions — check them.',
         'Do not divide by cos x or sin x without checking whether it can be 0.', 'Values ±1 are reached once per period, not twice.', 'Degrees and radians: keep one unit throughout.']
STEPS = [dict(k='s1', t='Identities', e='⭕', cards=['c1', 'c2'], need=['id'], note='Ratios, compound angles, ranges'),
         dict(k='s2', t='Inverse', e='↩️', cards=['c3'], need=['inv'], note='Principal values and sums'),
         dict(k='s3', t='Equations', e='🎯', cards=['c4'], need=['eqn'], note='General solutions and counting')]
META = dict(unit='math-u14', subject='math', n=14, title='Trigonometry', cls=11, labs=['ucircle'],
            syllabus='Trigonometrical identities and trigonometrical functions, inverse trigonometrical functions, and their properties.')
