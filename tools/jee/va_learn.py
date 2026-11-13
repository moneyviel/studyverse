"""Concept cards for Mathematics Unit 12 — Vector Algebra (written for StudyVerse)."""
TOPICS = {'dot': 'Dot product, angles & projections', 'cross': 'Cross product, areas & vector equations'}
CARDS = [
 dict(id='c1', t='Vectors and the dot product', e='➡️', lvl='f', topic='dot',
  body=['a⃗ = a_{1}î + a_{2}ĵ + a_{3}k̂, |a⃗| = √{a_{1}^{2} + a_{2}^{2} + a_{3}^{2}}. Unit vector â = \\f{a⃗}{|a⃗|}.',
        'a⃗·b⃗ = a_{1}b_{1} + a_{2}b_{2} + a_{3}b_{3} = |a⃗||b⃗| cos θ. Zero ⇔ perpendicular; negative ⇔ obtuse angle.',
        '|a⃗ ± b⃗|^{2} = |a⃗|^{2} + |b⃗|^{2} ± 2a⃗·b⃗.'],
  check=dict(q='(î + 2ĵ)·(3î − ĵ + 5k̂) =', o=['1', '5', '3', '−1'], a=0, why='3 − 2 + 0.')),
 dict(id='c2', t='Projections and components', e='🔦', lvl='m', topic='dot',
  body=['Projection (length) of a⃗ on b⃗: \\f{a⃗·b⃗}{|b⃗|}. Projection vector: \\f{a⃗·b⃗}{|b⃗|^{2}}b⃗.',
        'a⃗ = (part along b⃗) + (part ⟂ b⃗); the perpendicular part is a⃗ − \\f{a⃗·b⃗}{|b⃗|^{2}}b⃗.',
        'The bisector of the angle between a⃗ and b⃗ is along â + b̂.'],
  check=dict(q='Projection of 3î + 4ĵ on î:', o=['3', '4', '5', '\\f{3}{5}'], a=0, why='Dot with the unit vector î.')),
 dict(id='c3', t='The cross product', e='✖️', lvl='m', topic='cross',
  body=['a⃗ × b⃗ is ⟂ to both, with |a⃗ × b⃗| = |a⃗||b⃗| sin θ = area of the parallelogram on a⃗, b⃗.',
        'Triangle area \\f{1}{2}|AB⃗ × AC⃗|; parallelogram from diagonals: \\f{1}{2}|d⃗_{1} × d⃗_{2}|.',
        'a⃗ × b⃗ = 0 ⇔ parallel. b⃗ × a⃗ = −a⃗ × b⃗. |a⃗ × b⃗|^{2} + (a⃗·b⃗)^{2} = |a⃗|^{2}|b⃗|^{2}.'],
  check=dict(q='î × ĵ =', o=['k̂', '−k̂', '0⃗', 'î + ĵ'], a=0, why='Cyclic order î → ĵ → k̂.')),
 dict(id='c4', t='Box product and vector equations', e='📦', lvl='h', topic='cross',
  body=['[a⃗ b⃗ c⃗] = a⃗·(b⃗ × c⃗) = the 3 × 3 determinant; |…| = volume of the parallelepiped; zero ⇔ coplanar.',
        'a⃗ × (b⃗ × c⃗) = (a⃗·c⃗)b⃗ − (a⃗·b⃗)c⃗.',
        'Solving: (pa⃗ + qb⃗) × c⃗ = 0 ⇒ c⃗ = t(pa⃗ + qb⃗); a⃗ × c⃗ = b⃗ ⇒ c⃗ = c⃗_{0} + ta⃗. A dot condition then fixes t.'],
  check=dict(q='[î ĵ k̂] =', o=['1', '0', '−1', '3'], a=0, why='î·(ĵ × k̂) = î·î.')),
]
FORMULAS = [('Dot', 'a⃗·b⃗ = |a⃗||b⃗| cos θ'), ('Projection', '\\f{a⃗·b⃗}{|b⃗|}'), ('Cross size', '|a⃗||b⃗| sin θ'), ('Triangle', '\\f{1}{2}|AB⃗ × AC⃗|'),
            ('Lagrange', '|a⃗ × b⃗|^{2} + (a⃗·b⃗)^{2} = |a⃗|^{2}|b⃗|^{2}'), ('Box', '[a⃗ b⃗ c⃗] = a⃗·(b⃗ × c⃗)'), ('BAC − CAB', 'a⃗ × (b⃗ × c⃗) = (a⃗·c⃗)b⃗ − (a⃗·b⃗)c⃗'), ('Bisector', 'â + b̂')]
TRAPS = ['Projection divides by |b⃗|, the projection VECTOR by |b⃗|^{2}.', 'a⃗ × b⃗ ≠ b⃗ × a⃗ — order flips the sign.', 'Area of a triangle needs the ½.',
         'From a⃗ × c⃗ = a⃗ × b⃗ you only get c⃗ − b⃗ ∥ a⃗, not c⃗ = b⃗.', 'Check a⃗·b⃗ = 0 before solving a⃗ × c⃗ = b⃗ — otherwise there is no solution.', 'Diagonals give area ½|d⃗_{1} × d⃗_{2}|, not |d⃗_{1} × d⃗_{2}|.']
STEPS = [dict(k='s1', t='Dot product', e='➡️', cards=['c1', 'c2'], need=['dot'], note='Angles, projections, components'),
         dict(k='s2', t='Cross product', e='✖️', cards=['c3', 'c4'], need=['cross'], note='Areas, volumes, vector equations')]
META = dict(unit='math-u12', subject='math', n=12, title='Vector Algebra', cls=12, labs=['xprod'],
            syllabus='Vectors and scalars, the addition of vectors, components of a vector in two dimensions and three-dimensional space, scalar and vector products.')
