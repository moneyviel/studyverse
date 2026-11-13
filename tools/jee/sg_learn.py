"""Concept cards for Mathematics Unit 11 — Three Dimensional Geometry (written for StudyVerse)."""
TOPICS = {'line3': 'Lines in space', 'img': 'Feet, images & distances', 'sd': 'Shortest distance & meeting lines'}
CARDS = [
 dict(id='c1', t='A line in space', e='📍', lvl='f', topic='line3',
  body=['A line through A with direction d: r⃗ = A + t d, or \\f{x − x_{1}}{l} = \\f{y − y_{1}}{m} = \\f{z − z_{1}}{n}. A 0 in a denominator just means that coordinate stays fixed.',
        'Direction cosines: divide (l, m, n) by √{l^{2} + m^{2} + n^{2}}; their squares add to 1. Equal angles with the axes means direction (1, 1, 1).',
        'Angle between lines: cos θ = \\f{|d_{1}·d_{2}|}{|d_{1}||d_{2}|}. Perpendicular ⇔ d_{1}·d_{2} = 0.'],
  check=dict(q='Direction cosines of a line with direction ratios 2, −1, 2:', o=['\\f{2}{3}, −\\f{1}{3}, \\f{2}{3}', '2, −1, 2', '\\f{2}{5}, −\\f{1}{5}, \\f{2}{5}', '\\f{1}{3}, \\f{1}{3}, \\f{1}{3}'], a=0, why='Divide by √{9} = 3.')),
 dict(id='c2', t='Foot and image', e='🪞', lvl='m', topic='img',
  body=['Foot of the perpendicular from P to A + td: t = \\f{(P − A)·d}{|d|^{2}}, F = A + td.',
        'Image of P in the line: Q = 2F − P. Distance of P from the line = PF = \\f{|(P − A) × d|}{|d|}.',
        'Area tricks: if R is on the line, triangle P(image)R has base PQ = 2PF and height RF.'],
  check=dict(q='Foot of the perpendicular from (1, 2, 3) on the x-axis:', o=['(1, 0, 0)', '(0, 2, 3)', '(1, 2, 0)', '(0, 0, 3)'], a=0, why='Drop y and z.')),
 dict(id='c3', t='Shortest distance', e='📏', lvl='m', topic='sd',
  body=['Skew lines A_{1} + s d_{1}, A_{2} + t d_{2}: SD = \\f{|(A_{2} − A_{1})·(d_{1} × d_{2})|}{|d_{1} × d_{2}|}.',
        'Parallel lines (same d): SD = \\f{|(A_{2} − A_{1}) × d|}{|d|}.',
        'SD = 0 ⇔ the lines meet (are coplanar). Equate two coordinates to find the parameters; the third must agree.'],
  check=dict(q='Shortest distance between the x-axis and the line x = 0, z = 3 (parallel to y):', o=['3', '0', '√{3}', '9'], a=0, why='The common perpendicular is along z.')),
 dict(id='c4', t='Line of shortest distance', e='🧷', lvl='h', topic='sd',
  body=['Its direction is d_{1} × d_{2}. Its ends are the points where the joining vector is perpendicular to both lines (two linear equations in s, t).',
        'A line through a point meeting two given lines lies in the plane through the point containing each line: its direction is n_{1} × n_{2}.',
        'Distance "along a direction u": move P + ku until you hit the line; distance = |k||u|.'],
  check=dict(q='The common perpendicular to lines with directions (1, 0, 0) and (0, 1, 0) is along', o=['(0, 0, 1)', '(1, 1, 0)', '(1, 0, 0)', '(1, 1, 1)'], a=0, why='i × j = k.')),
]
FORMULAS = [('Line', 'r⃗ = A + t d'), ('Angle', 'cos θ = \\f{|d_{1}·d_{2}|}{|d_{1}||d_{2}|}'), ('Foot', 't = \\f{(P − A)·d}{|d|^{2}}'), ('Image', 'Q = 2F − P'),
            ('Point–line distance', '\\f{|(P − A) × d|}{|d|}'), ('Skew SD', '\\f{|(A_{2} − A_{1})·(d_{1} × d_{2})|}{|d_{1} × d_{2}|}'), ('Parallel SD', '\\f{|(A_{2} − A_{1}) × d|}{|d|}'), ('Direction cosines', 'l^{2} + m^{2} + n^{2} = 1')]
TRAPS = ['Read the point from the numerators carefully: \\f{x + 3}{2} means x_{1} = −3.', 'A form like \\f{1 − y}{2} is \\f{y − 1}{−2}: the direction ratio changes sign.',
         'For parallel lines d_{1} × d_{2} = 0 — use the parallel formula instead.', 'The image is 2F − P, not F.',
         '"Distance along a line" is not the perpendicular distance.', 'Check the third coordinate when testing whether two lines meet.']
STEPS = [dict(k='s1', t='Lines', e='📍', cards=['c1'], need=['line3'], note='Forms, direction cosines, angles'),
         dict(k='s2', t='Feet & images', e='🪞', cards=['c2'], need=['img'], note='Foot, image, point–line distance'),
         dict(k='s3', t='Shortest distance', e='📏', cards=['c3', 'c4'], need=['sd'], note='Skew, parallel and meeting lines')]
META = dict(unit='math-u11', subject='math', n=11, title='Three Dimensional Geometry', cls=12, labs=['skew'],
            syllabus='Coordinates of a point in space, the distance between two points, section formula, direction ratios and direction cosines, and the angle between two intersecting lines. Skew lines, the shortest distance between them, and its equation. Equations of a line.')
