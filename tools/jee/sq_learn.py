"""Concept cards for Mathematics Unit 6 — Sequence and Series (written for StudyVerse)."""
TOPICS = {'ap': 'Arithmetic progression', 'gp': 'Geometric progression', 'means': 'Means and mixed A.P.–G.P. problems', 'special': 'Special series & telescoping'}
CARDS = [
 dict(id='c1', t='Arithmetic progression', e='🪜', lvl='f', topic='ap',
  body=['Each term adds the same d: <div class="jx-f">a_{n} = a + (n − 1)d,  S_{n} = \\f{n}{2}[2a + (n − 1)d] = \\f{n}{2}(a + l)</div>',
        'Gauss\'s trick: write the sum forwards and backwards — every pair adds to (first + last).', 'Terms equally far from the ends add up the same: a_{1} + a_{n} = a_{2} + a_{n−1} = …',
        'a_{n} = S_{n} − S_{n−1}. If S_{n} = pn^{2} + qn then d = 2p.', 'Choose terms smartly: three in A.P. → a − d, a, a + d; four → a − 3d, a − d, a + d, a + 3d (difference 2d).',
        'Even number of terms 2k: (sum of even-placed) − (sum of odd-placed) = kd.'],
  check=dict(q='S_{n} = 3n^{2} + 5n. a_{10} :', o=['62', '65', '59', '350'], a=0, why='S_{10} − S_{9} = 350 − 288 = 62.')),
 dict(id='c2', t='Geometric progression', e='🌱', lvl='f', topic='gp',
  body=['Each term multiplies by r: <div class="jx-f">a_{n} = ar^{n−1},  S_{n} = a\\f{r^{n} − 1}{r − 1} (r ≠ 1),  S_{∞} = \\f{a}{1 − r} (|r| < 1)</div>',
        'Terms equally far from the ends MULTIPLY to the same: a_{3}a_{5} = a_{4}^{2}, a_{1}a_{5} = a_{3}^{2}.', 'Three in G.P.: \\f{a}{r}, a, ar (product a^{3}). Dividing two terms kills a: \\f{a_{m}}{a_{n}} = r^{m−n}.',
        'If a_{1}, a_{2}, … is a G.P. then a_{1}^{3}, a_{2}^{3}, … is a G.P. with ratio r^{3}.'],
  check=dict(q='a_{3}a_{5} = 729 in a positive G.P. a_{4} :', o=['27', '9', '81', '243'], a=0, why='a_{4}^{2} = 729.')),
 dict(id='c3', t='Means and A.M. ≥ G.M.', e='⚖️', lvl='m', topic='means',
  body=['b is the A.M. of a, c if 2b = a + c; the G.M. if b^{2} = ac.', 'n arithmetic means between a and b: d = \\f{b − a}{n + 1}; their sum is n × \\f{a + b}{2}.',
        '<div class="jx-f">For positive numbers: A.M. ≥ G.M. (equality only when all are equal)</div>', 'So y + \\f{1}{y} ≥ 2 for y > 0 — the key to many "least value" questions.',
        'Mixed problems: write the A.P. condition and the G.P. condition as two equations and solve.'],
  check=dict(q='Least value of 4^{x} + 4^{−x} :', o=['1', '2', '4', '0'], a=1, why='y + 1/y ≥ 2.')),
 dict(id='c4', t='Special sums and telescoping', e='🔭', lvl='m', topic='special',
  body=['<div class="jx-f">Σk = \\f{n(n + 1)}{2},  Σk^{2} = \\f{n(n + 1)(2n + 1)}{6},  Σk^{3} = (\\f{n(n + 1)}{2})^{2}</div>', 'Telescoping: write each term as f(k) − f(k + 1); everything in the middle cancels.',
        '\\f{1}{k(k + 1)} = \\f{1}{k} − \\f{1}{k + 1};  \\f{1}{k(k + 2)} = \\f{1}{2}(\\f{1}{k} − \\f{1}{k + 2}).', 'The JEE favourite: 1 + 4k^{4} = (2k^{2} + 1)^{2} − (2k)^{2} = (2k^{2} − 2k + 1)(2k^{2} + 2k + 1); the two factors differ by 4k.',
        'Similarly k^{4} + k^{2} + 1 = (k^{2} − k + 1)(k^{2} + k + 1) and k^{4} + 3k^{2} + 4 = (k^{2} − k + 2)(k^{2} + k + 2).'],
  check=dict(q='\\f{1}{1·2} + \\f{1}{2·3} + … + \\f{1}{9·10} :', o=['\\f{9}{10}', '\\f{10}{11}', '1', '\\f{1}{10}'], a=0, why='1 − 1/10.')),
]
FORMULAS = [('A.P. term', 'a_{n} = a + (n − 1)d'), ('A.P. sum', 'S_{n} = \\f{n}{2}[2a + (n − 1)d]'), ('From S_{n}', 'a_{n} = S_{n} − S_{n−1}'), ('G.P. term', 'a_{n} = ar^{n−1}'), ('G.P. sum', 'S_{n} = a\\f{r^{n} − 1}{r − 1}'),
            ('Infinite G.P.', 'S_{∞} = \\f{a}{1 − r}, |r| < 1'), ('Means', 'A.M. = \\f{a + b}{2},  G.M. = √{ab}'), ('Σk', '\\f{n(n + 1)}{2}'), ('Σk^{2}', '\\f{n(n + 1)(2n + 1)}{6}'), ('Σk^{3}', '(\\f{n(n + 1)}{2})^{2}')]
TRAPS = ['S_{n} = 0 does not mean any term is 0.', '"Increasing G.P. of positive terms" decides between r and 1/r.', 'S_{∞} needs |r| < 1.', 'A.M. ≥ G.M. only for POSITIVE numbers.',
         'For four terms in A.P. written a − 3d, …, a + 3d the common difference is 2d.', 'Count terms carefully: rows of a triangle use 1 + 2 + … + k terms.']
STEPS = [dict(k='s1', t='A.P.', e='🪜', cards=['c1'], need=['ap'], note='Terms, sums and smart choices of terms'),
         dict(k='s2', t='G.P.', e='🌱', cards=['c2'], need=['gp'], note='Terms, finite and infinite sums'),
         dict(k='s3', t='Means & special series', e='🔭', cards=['c3', 'c4'], need=['means', 'special'], note='A.M. ≥ G.M., Σk^{2}, Σk^{3} and telescoping')]
META = dict(unit='math-u06', subject='math', n=6, title='Sequence and Series', cls=11, labs=['pattern', 'tele'],
            syllabus="Arithmetic and geometric progressions; insertion of arithmetic and geometric means between two given numbers; relation between A.M. and G.M.; sum of n terms of special series (Σn, Σn², Σn³); telescoping sums.")
