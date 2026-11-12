"""Concept cards for Mathematics Unit 3 — Matrices and Determinants (written for StudyVerse)."""
TOPICS = {'det': 'Determinants & adjoint', 'sys': 'Systems of linear equations', 'mat': 'Matrix algebra & counting'}
CARDS = [
 dict(id='c1', t='Matrices and their algebra', e='🔢', lvl='f', topic='mat',
  body=['A matrix is a table of numbers; AB is defined when columns of A = rows of B, and usually AB ≠ BA.', 'Transpose: (AB)^{T} = B^{T}A^{T}. Symmetric: A^{T} = A; skew-symmetric: A^{T} = −A (diagonal zero).',
        'trace(A) = sum of the diagonal. trace(A^{T}A) = sum of the squares of ALL entries.', '<b>Cayley–Hamilton</b> (2 × 2): A^{2} − (trace A)A + (det A)I = 0. Multiply by A^{−1} to get A^{−1} in terms of A and I.'],
  check=dict(q='trace(A^{T}A) for A = [[1, 2], [0, −1]] :', o=['0', '6', '2', '4'], a=1, why='1 + 4 + 0 + 1.')),
 dict(id='c2', t='Determinant, adjoint and inverse', e='🧮', lvl='m', topic='det',
  body=['A is singular when |A| = 0. A^{−1} = \\f{adj A}{|A|} exists only when |A| ≠ 0.', 'For a matrix of order n: <div class="jx-f">|kA| = k^{n}|A|,  |adj A| = |A|^{n−1},  |A^{−1}| = \\f{1}{|A|},  |AB| = |A||B|,  |A^{T}| = |A|</div>',
        'Also adj(kA) = k^{n−1}adj A and adj(adj A) = |A|^{n−2}A.', 'Long chains like |3 adj(2A)|: work from the INSIDE out, one rule at a time.'],
  check=dict(q='Order 3, |A| = 2. |adj(2A)| :', o=['16', '64', '256', '32'], a=2, why='|2A| = 16 → 16^{2} = 256.')),
 dict(id='c3', t='Solving systems: three possibilities', e='🧭', lvl='m', topic='sys',
  body=['For AX = B with D = |A|: <div class="jx-f">D ≠ 0 → unique solution (Cramer: x = \\f{D_{x}}{D}, …)</div>', 'D = 0 and some D_{x}, D_{y}, D_{z} ≠ 0 → no solution.',
        'D = 0 and all D_{x} = D_{y} = D_{z} = 0 → usually infinitely many solutions (check consistency).', 'Fast trick for "infinitely many": the third equation must be p × (eq 1) + q × (eq 2). Find p, q from two known coefficients, then read off λ and μ.',
        'A homogeneous system (B = 0) always has x = y = z = 0; it has a non-trivial solution exactly when D = 0.'],
  check=dict(q='D = 0, D_{x} ≠ 0. The system has :', o=['unique solution', 'no solution', 'infinitely many', 'only zero solution'], a=1, why='Inconsistent.')),
]
FORMULAS = [('Scalar', '|kA| = k^{n}|A|'), ('Adjoint', '|adj A| = |A|^{n−1}'), ('Inverse', 'A^{−1} = \\f{adj A}{|A|}'), ('Product', '|AB| = |A||B|'), ('adj of adj', 'adj(adj A) = |A|^{n−2}A'),
            ('Cayley–Hamilton', 'A^{2} − (tr A)A + |A|I = 0'), ('Cramer', 'x = \\f{D_{x}}{D}, y = \\f{D_{y}}{D}, z = \\f{D_{z}}{D}'), ('trace', 'tr(A^{T}A) = Σ a_{ij}^{2}')]
TRAPS = ['|kA| = k^{n}|A|, not k|A|.', '|adj A| = |A|^{n−1}: for order 3 that is |A|^{2}.', 'D = 0 alone does not mean infinitely many solutions — check consistency.', 'AB ≠ BA in general.', '"Non-trivial solution" questions are about D = 0 only.']
STEPS = [dict(k='s1', t='Matrices', e='🔢', cards=['c1'], need=['mat'], note='Algebra, trace and Cayley–Hamilton'),
         dict(k='s2', t='Determinants', e='🧮', cards=['c2'], need=['det'], note='Adjoint, inverse and determinant chains'),
         dict(k='s3', t='Linear systems', e='🧭', cards=['c3'], need=['sys'], note='Unique, none or infinitely many solutions')]
META = dict(unit='math-u03', subject='math', n=3, title='Matrices and Determinants', cls=12, labs=['transform', 'planes'],
            syllabus="Matrices, algebra of matrices, types of matrices, determinants and matrices of order two and three, evaluation of determinants, area of triangles using determinants, adjoint and inverse of a square matrix, test of consistency and solution of simultaneous linear equations in two or three variables using matrices.")
