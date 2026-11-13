"""Concept cards for Mathematics Unit 9 — Differential Equations (written for StudyVerse)."""
TOPICS = {'lin': 'Linear first-order equations', 'sep': 'Separable, exact & homogeneous', 'form': 'Order, degree & forming equations'}
CARDS = [
 dict(id='c1', t='What a differential equation says', e='🧭', lvl='f', topic='form',
  body=['An equation linking x, y and derivatives of y. A solution is a function that makes it true; a condition like y(0) = 1 picks one curve from the family.',
        'Order = highest derivative present. Degree = power of that derivative once the equation is a polynomial in the derivatives.',
        'Forming the equation of a family with n constants: differentiate n times and eliminate the constants.'],
  check=dict(q='Order and degree of (y")^{3} + (y\')^{4} + y = 0:', o=['2, 3', '2, 4', '1, 4', '3, 2'], a=0, why='Highest derivative y", raised to 3.')),
 dict(id='c2', t='Separate the variables', e='✂️', lvl='m', topic='sep',
  body=['If \\f{dy}{dx} = f(x)g(y): \\f{dy}{g(y)} = f(x)dx, integrate both sides, then use the condition for C.',
        'Exact forms: x dy + y dx = d(xy), \\f{x dy − y dx}{x^{2}} = d(\\f{y}{x}), \\f{x dy − y dx}{x^{2} + y^{2}} = d(tan^{−1}\\f{y}{x}).',
        'Homogeneous (every term the same degree): put y = vx, then separate v and x.'],
  check=dict(q='Solution of \\f{dy}{dx} = \\f{y}{x}, y(1) = 2:', o=['y = 2x', 'y = x + 1', 'y = x^{2} + 1', 'y = 2'], a=0, why='log y = log x + log 2.')),
 dict(id='c3', t='Linear equations', e='📐', lvl='m', topic='lin',
  body=['\\f{dy}{dx} + P(x)y = Q(x). Multiply by the integrating factor μ = e^{∫P dx}:',
        '<div class="jx-f">(μy)\' = μQ → μy = ∫μQ dx + C</div>',
        'If the equation is linear in x instead, swap roles: \\f{dx}{dy} + P(y)x = Q(y).',
        'Bernoulli \\f{dy}{dx} + Py = Qy^{n}: put u = y^{1−n} to make it linear.'],
  check=dict(q='Integrating factor of y\' + \\f{2}{x}y = x:', o=['x^{2}', '2x', 'e^{2x}', '\\f{1}{x^{2}}'], a=0, why='e^{2 log x}.')),
 dict(id='c4', t='Reading off answers', e='🔎', lvl='h', topic='lin',
  body=['Many JEE questions only need μ(x)y at two points: compute μy at the start, add ∫μQ between them.',
        'Look for a derivative hiding in the equation: (1 + x^{2})y\' + 2xy = ((1 + x^{2})y)\'.',
        'Substitutions like t = tan x or u = x + y + 2 turn awkward equations into standard ones.'],
  check=dict(q='(x^{2}y)\' = 2x and y(1) = 3. Then y(2) =', o=['\\f{3}{2}', '3', '\\f{1}{2}', '2'], a=0, why='x^{2}y = x^{2} + 2 → 4y(2) = 6.')),
]
FORMULAS = [('Separable', '∫\\f{dy}{g(y)} = ∫f(x)dx'), ('Linear', '\\f{dy}{dx} + Py = Q'), ('Integrating factor', 'μ = e^{∫P dx}'), ('Solution', 'μy = ∫μQ dx + C'),
            ('Homogeneous', 'y = vx'), ('Bernoulli', 'u = y^{1−n}'), ('Exact piece', 'x dy + y dx = d(xy)'), ('Quotient piece', '\\f{x dy − y dx}{x^{2}} = d(\\f{y}{x})')]
TRAPS = ['Do not forget the constant C — the condition fixes it.', 'Integrating factor uses P with the + sign form y\' + Py = Q.', 'Degree is undefined if a derivative sits inside sin, log, e^{…}.',
         'After y = vx, dy/dx = v + x dv/dx, not just v.', 'Check which variable the equation is linear in.', 'A solution can blow up before the asked point — watch tan and 1/(…).']
STEPS = [dict(k='s1', t='Basics', e='🧭', cards=['c1'], need=['form'], note='Order, degree, forming equations'),
         dict(k='s2', t='Separable', e='✂️', cards=['c2'], need=['sep'], note='Separable, exact, homogeneous'),
         dict(k='s3', t='Linear', e='📐', cards=['c3', 'c4'], need=['lin'], note='Integrating factor and tricks')]
META = dict(unit='math-u09', subject='math', n=9, title='Differential Equations', cls=12, labs=['slope'],
            syllabus='Ordinary differential equations, their order and degree, the solution of differential equation by the method of separation of variables, solution of a homogeneous and linear differential equation of the type dy/dx + p(x)y = q(x).')
