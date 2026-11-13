"""Concept cards for Mathematics Unit 8 — Integral Calculus (written for StudyVerse)."""
TOPICS = {'area': 'Area under and between curves', 'def': 'Definite integrals & properties', 'gif': 'Integrals with [x] and {x}', 'indef': 'Antiderivatives'}
CARDS = [
 dict(id='c1', t='Undoing a derivative', e='↩️', lvl='f', topic='indef',
  body=['∫f(x)dx = F(x) + C means F\'(x) = f(x). Always check by differentiating your answer.',
        '<div class="jx-f">∫x^{n} = \\f{x^{n+1}}{n + 1} · ∫\\f{1}{x} = log|x| · ∫e^{x} = e^{x} · ∫sin x = −cos x · ∫cos x = sin x</div>',
        'Substitution: spot a function and its derivative together. Parts: ∫u dv = uv − ∫v du.',
        'Partial fractions split \\f{px + q}{(x − a)(x − b)} into \\f{A}{x − a} + \\f{B}{x − b}.'],
  check=dict(q='∫2x e^{x^{2}}dx =', o=['e^{x^{2}} + C', '2e^{x^{2}} + C', 'x^{2}e^{x^{2}} + C', 'e^{2x} + C'], a=0, why='u = x^{2}.')),
 dict(id='c2', t='Definite integrals', e='📏', lvl='m', topic='def',
  body=['∫_{a}^{b}f(x)dx = F(b) − F(a): the signed area under the curve.',
        'Odd f on [−a, a] → 0. Even f → 2∫_{0}^{a}.',
        '<div class="jx-f">King\'s rule: ∫_{a}^{b}f(x)dx = ∫_{a}^{b}f(a + b − x)dx</div>',
        'Pairing f(x) with f(a + b − x) often turns a hard integrand into 1: then I = \\f{b − a}{2}.'],
  check=dict(q='∫_{−2}^{2}x^{3}dx =', o=['0', '8', '16', '4'], a=0, why='Odd function.')),
 dict(id='c3', t='Trig powers and tricks', e='🔁', lvl='m', topic='def',
  body=['Wallis: ∫_{0}^{π/2}sin^{n}x dx = \\f{n − 1}{n}·\\f{n − 3}{n − 2}… (× \\f{π}{2} if n is even).',
        'a sin x + b cos x on top of c sin x + d cos x: write top = λ(bottom) + μ(bottom)\'.',
        'Rational in tan x: divide by cos^{k}x and put t = tan x.'],
  check=dict(q='∫_{0}^{π/2}sin^{2}x dx =', o=['\\f{π}{4}', '\\f{π}{2}', '1', '\\f{1}{2}'], a=0, why='\\f{1}{2} · \\f{π}{2}.')),
 dict(id='c4', t='Greatest integer inside', e='🪜', lvl='m', topic='gif',
  body=['[g(x)] is constant between the points where g(x) crosses an integer: split the integral there.',
        '∫_{0}^{n}[x]dx = 0 + 1 + … + (n − 1); ∫_{0}^{n}{x}dx = \\f{n}{2}.',
        '[x] + [−x] = −1 for non-integer x.'],
  check=dict(q='∫_{0}^{3}[x]dx =', o=['3', '6', '2', '4.5'], a=0, why='0 + 1 + 2.')),
 dict(id='c5', t='Area between curves', e='🗺️', lvl='m', topic='area',
  body=['Find where the curves meet; area = ∫(top − bottom)dx between those points.',
        'If the region is easier sideways, slice horizontally: ∫(right − left)dy.',
        'Parabola y = ax^{2} and a line cutting it at r_{1}, r_{2}: area = \\f{|a|(r_{2} − r_{1})^{3}}{6}.',
        'Use symmetry: |x|, even functions, ellipses and circles.'],
  check=dict(q='Area between y = x^{2} and y = 1:', o=['\\f{4}{3}', '\\f{2}{3}', '2', '1'], a=0, why='∫_{−1}^{1}(1 − x^{2}).')),
]
FORMULAS = [('Power', '∫x^{n}dx = \\f{x^{n+1}}{n + 1}'), ('Log', '∫\\f{dx}{x} = log|x|'), ('Parts', '∫u dv = uv − ∫v du'), ('King', '∫_{a}^{b}f(x) = ∫_{a}^{b}f(a + b − x)'),
            ('Odd', '∫_{−a}^{a}odd = 0'), ('Area', '∫(top − bottom)dx'), ('Parabola cap', '\\f{|a|(r_{2} − r_{1})^{3}}{6}'), ('Wallis', 'I_{n} = \\f{n − 1}{n}I_{n−2}')]
TRAPS = ['Area is never negative: split where the curve crosses the axis.', 'Do not forget + C in indefinite integrals.', 'Change the limits when you substitute.',
         'Find the meeting points before integrating "top − bottom".', '[x] changes value at every integer inside the limits.', 'log|x|, not log x, when x can be negative.']
STEPS = [dict(k='s1', t='Antiderivatives', e='↩️', cards=['c1'], need=['indef'], note='Rules, substitution, parts, partial fractions'),
         dict(k='s2', t='Definite integrals', e='📏', cards=['c2', 'c3', 'c4'], need=['def', 'gif'], note='Properties, tricks, [x]'),
         dict(k='s3', t='Areas', e='🗺️', cards=['c5'], need=['area'], note='Between curves, slicing either way')]
META = dict(unit='math-u08', subject='math', n=8, title='Integral Calculus', cls=12, labs=['riemann'],
            syllabus='Integral as an anti-derivative, fundamental integrals, integration by substitution, by parts and by partial fractions, integration using trigonometric identities. Evaluation of simple integrals. Fundamental theorem of calculus, properties of definite integrals, evaluation of definite integrals, determining areas of the regions bounded by simple curves in standard form.')
