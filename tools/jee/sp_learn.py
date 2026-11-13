"""Concept cards for Mathematics Unit 13 — Statistics and Probability (written for StudyVerse)."""
TOPICS = {'stat': 'Mean, variance & mean deviation', 'prob': 'Counting probability', 'dist': 'Random variables & binomial', 'cond': 'Conditional probability & Bayes'}
CARDS = [
 dict(id='c1', t='Centre and spread', e='📊', lvl='f', topic='stat',
  body=['Mean x̄ = \\f{Σx}{n}. Median: middle value of sorted data (average of the two middles if n is even).',
        'Variance σ^{2} = \\f{Σx^{2}}{n} − x̄^{2}; SD = σ. Mean deviation = \\f{Σ|x − c|}{n} about c = mean or median.',
        'Unknown data values: use Σx = n·x̄ and Σx^{2} = n(σ^{2} + x̄^{2}) to get a + b and a^{2} + b^{2}.'],
  check=dict(q='Variance of 2, 4, 6:', o=['\\f{8}{3}', '4', '2', '\\f{4}{3}'], a=0, why='\\f{56}{3} − 16.')),
 dict(id='c2', t='Changing and merging data', e='🔁', lvl='m', topic='stat',
  body=['y = ax + b: mean becomes a x̄ + b, variance a^{2}σ^{2}, SD |a|σ.',
        'Wrong value w replaced by r: Σx changes by r − w, Σx^{2} by r^{2} − w^{2}; recompute.',
        'Combining groups: add their Σx and Σx^{2}. A.P. with difference d and n terms has variance \\f{d^{2}(n^{2} − 1)}{12}.'],
  check=dict(q='If Var(x) = 4, Var(3x − 2) =', o=['36', '12', '10', '34'], a=0, why='a^{2} = 9.')),
 dict(id='c3', t='Counting probability', e='🎲', lvl='m', topic='prob',
  body=['P(E) = \\f{favourable}{total} for equally likely outcomes; list or count carefully (ordered vs unordered).',
        'Complement: P(at least one) = 1 − P(none). Independent events multiply.',
        'Selections: C(n, r); arrangements: P(n, r). Dice: 6^{n} outcomes.'],
  check=dict(q='P(sum 7 with two dice) =', o=['\\f{1}{6}', '\\f{7}{36}', '\\f{1}{12}', '\\f{5}{36}'], a=0, why='6 of 36.')),
 dict(id='c4', t='Random variables', e='📈', lvl='m', topic='dist',
  body=['E(X) = Σx p(x); Var(X) = Σx^{2}p(x) − (E X)^{2}. Probabilities add to 1 — use that to find k.',
        'Binomial B(n, p): P(X = r) = C(n, r)p^{r}q^{n−r}, mean np, variance npq.',
        'Drawing without replacement (hypergeometric): mean n\\f{D}{N}.'],
  check=dict(q='Mean of B(10, \\f{1}{2}):', o=['5', '2.5', '10', '\\f{5}{2}'], a=0, why='np.')),
 dict(id='c5', t='Conditional probability & Bayes', e='🔍', lvl='h', topic='cond',
  body=['P(A | B) = \\f{P(A ∩ B)}{P(B)}. Total probability: P(B) = Σ P(A_{i})P(B | A_{i}).',
        'Bayes: P(A_{i} | B) = \\f{P(A_{i})P(B | A_{i})}{Σ P(A_{j})P(B | A_{j})}.',
        'Rare conditions: even an accurate test gives many false alarms when the base rate is small.'],
  check=dict(q='Two bags equally likely; P(red) = \\f{1}{2} and \\f{1}{4}. Red drawn: P(first bag) =', o=['\\f{2}{3}', '\\f{1}{2}', '\\f{3}{4}', '\\f{1}{3}'], a=0, why='\\f{1/2}{1/2 + 1/4}.')),
]
FORMULAS = [('Mean', 'x̄ = \\f{Σx}{n}'), ('Variance', '\\f{Σx^{2}}{n} − x̄^{2}'), ('Scaling', 'Var(ax + b) = a^{2}Var(x)'), ('A.P. variance', '\\f{d^{2}(n^{2} − 1)}{12}'),
            ('Complement', 'P(≥ 1) = 1 − P(0)'), ('Binomial', 'C(n, r)p^{r}q^{n−r}'), ('Binomial mean/var', 'np, npq'), ('Bayes', '\\f{P(A_{i})P(B | A_{i})}{Σ P(A_{j})P(B | A_{j})}')]
TRAPS = ['Variance uses the mean of squares minus the square of the mean — not the reverse.', 'Adding a constant does not change variance or SD.',
         'Mean deviation about the median needs the median, not the mean.', 'Without replacement the draws are not independent.',
         'Ordered and unordered counts must match top and bottom.', 'P(A | B) ≠ P(B | A).']
STEPS = [dict(k='s1', t='Statistics', e='📊', cards=['c1', 'c2'], need=['stat'], note='Mean, variance, mean deviation'),
         dict(k='s2', t='Probability', e='🎲', cards=['c3'], need=['prob'], note='Counting outcomes'),
         dict(k='s3', t='Random variables', e='📈', cards=['c4'], need=['dist'], note='Expectation, binomial'),
         dict(k='s4', t='Bayes', e='🔍', cards=['c5'], need=['cond'], note='Conditional probability and Bayes')]
META = dict(unit='math-u13', subject='math', n=13, title='Statistics and Probability', cls=11, labs=['bayes'],
            syllabus='Measures of dispersion: calculation of mean, median, mode of grouped and ungrouped data, calculation of standard deviation, variance, and mean deviation for grouped and ungrouped data. Probability: probability of an event, addition and multiplication theorems of probability, Bayes theorem, probability distribution of a random variate.')
