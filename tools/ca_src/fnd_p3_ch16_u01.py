"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 16 Theoretical Distributions.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below.
Exponentials use e = 2.71828 so that the validator can re-evaluate each expression."""
from math import comb, exp, factorial
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as _CM


def CM(*a, topic=None, **k):
    d = _CM(*a, **k); d['topic'] = topic
    return d

UID = 'fnd-p3-ch16-u01'
E = 2.71828


def ev(expr): return eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})


class Checks(Checks):
    """Records the check as lib.Checks does (value stored to 2 decimals), but returns the value to 4 decimals for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = round(ev(expr), 4)
        return int(v) if v == int(v) else v


def fm(v, unit=''):
    v = round(v, 4)
    s = inr(int(v)) if v == int(v) else f'{v:.4f}'.rstrip('0').rstrip('.')
    return s + (' ' + unit if unit else '')


def mq(mid, q, opts, explain, concept, diff='core', topic=None):
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit='', topic=None):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def binom(n, p, x): return comb(n, x) * p ** x * (1 - p) ** (n - x)
def pois(m, x): return E ** (-m) * m ** x / factorial(x)


def build():
    # ---------------- Illustration 1: binomial ----------------
    c1 = Checks()
    p0 = c1.add('round(0.9**6,4)', 'P(X = 0)')
    p1 = c1.add('round(6*0.1*0.9**5,4)', 'P(X = 1)')
    pl1 = c1.add('round(0.9**6+6*0.1*0.9**5,4)', 'P(X <= 1)')
    pg2 = c1.add('round(1-0.9**6-6*0.1*0.9**5,4)', 'P(X >= 2)')
    mu1 = c1.add('6*0.1', 'mean np'); v1 = c1.add('6*0.1*0.9', 'variance npq'); sd1 = c1.add('round((6*0.1*0.9)**0.5,4)', 'SD')
    rows1 = [[str(x), f'⁶C{x} (0.1)^{x} (0.9)^{6 - x}', fm(round(binom(6, 0.1, x), 4))] for x in range(4)]
    t1 = table(['x (invoices with errors)', 'Formula', 'P(x)'], rows1, title='Binomial probabilities, n = 6, p = 0.1 (first four values)')

    # ---------------- Illustration 2: parameters and mode ----------------
    c2 = Checks()
    q2 = c2.add('2.4/6', 'q = variance/mean'); p2 = c2.add('1-0.4', 'p'); n2 = c2.add('6/0.6', 'n = mean/p')
    c2.add('(10+1)*0.6', '(n+1)p for the mode')
    c2.add('(9+1)*0.5', '(n+1)p integer case')
    px6 = c2.add('round(210*0.6**6*0.4**4,4)', 'P(X = 6) with n = 10, p = 0.6')
    assert abs(px6 - round(binom(10, 0.6, 6), 4)) < 1e-4

    # ---------------- Illustration 3: Poisson ----------------
    c3 = Checks()
    e15 = c3.add('round(2.71828**(-1.5),4)', 'e^-1.5')
    pp0 = c3.add('round(2.71828**(-1.5),4)', 'P(X = 0), m = 1.5')
    pp2 = c3.add('round(2.71828**(-1.5)*(1+1.5+1.5**2/2),4)', 'P(X <= 2)')
    pp3 = c3.add('round(1-2.71828**(-1.5)*(1+1.5+1.5**2/2),4)', 'P(X > 2)')
    m3 = c3.add('200*0.01', 'm = np for the approximation')
    pa3 = c3.add('round(2.71828**(-2)*2**3/6,4)', 'Poisson approximation P(X = 3)')
    pb3 = round(binom(200, 0.01, 3), 4)
    c3.add('round(3*2.71828**(-1.5),4)', 'expected pages with no mistakes in 3 pages (sample check)')

    # ---------------- Illustration 4: normal ----------------
    c4 = Checks()
    z1 = c4.add('(75-60)/10', 'z for 75')
    pg75 = c4.add('0.5-0.4332', 'P(X > 75)')
    n75 = c4.add('round(1000*0.0668)', 'students above 75')
    pmid = c4.add('2*0.3413', 'P(50 < X < 70)')
    nmid = c4.add('round(1000*0.6826)', 'students between 50 and 70')
    c4.add('60-0.675*10', 'Q1'); c4.add('60+0.675*10', 'Q3')
    c4.add('0.8*10', 'mean deviation')
    c4.add('60-10', 'lower point of inflexion'); c4.add('60+10', 'upper point of inflexion')
    pb = c4.add('0.5-0.3413+0.4332', 'P(50 < X < 75)')

    # ---------------- Question 1 ----------------
    q1c = Checks()
    qa = q1c.add('round(0.8**5,4)', 'P(no failure)')
    qb = q1c.add('round(10*0.2**2*0.8**3,4)', 'P(exactly 2)')
    qc = q1c.add('round(1-0.8**5,4)', 'P(at least one)')
    qm = q1c.add('5*0.2', 'mean'); qv = q1c.add('5*0.2*0.8', 'variance')
    q1c.add('round(200*0.8**5)', 'expected number of batches with no failure out of 200')

    # ---------------- Question 2 ----------------
    q2c = Checks()
    q2m = q2c.add('500*0.004', 'm')
    q2p0 = q2c.add('round(0.1353,4)', 'P(0)')
    q2p1 = q2c.add('round(0.1353*2,4)', 'P(1)')
    q2le = q2c.add('round(0.1353*(1+2+2),4)', 'P(at most 2)')
    q2ge = q2c.add('round(1-0.1353*(1+2+2),4)', 'P(more than 2)')

    # ---------------- Question 3 ----------------
    q3c = Checks()
    z3a = q3c.add('(1300-1200)/80', 'z for 1300'); z3b = q3c.add('(1080-1200)/80', 'z for 1080')
    q3a = q3c.add('0.5-0.3944', 'P(X > 1300)')
    q3b = q3c.add('0.4332+0.3944', 'P(1080 < X < 1300)')
    q3n = q3c.add('round(5000*0.8276)', 'expected number of bulbs')
    q3c.add('1200-0.675*80', 'Q1'); q3c.add('0.8*80', 'MD')

    # ---------------- Case ----------------
    kc = Checks()
    kc.add('round(0.98**10,4)', 'P(no defective in 10)')
    kc.add('1000*0.02', 'm for 1,000 bolts')
    kc.add('round(2.71828**(-1)*(1+1),4)', 'P(at most 1 defective) m = 1')
    kc.add('2*0.4772', 'within mu +/- 2 sigma')
    cases = [{
        'id': 'k1', 'title': 'Quality control at a bolt factory', 'difficulty': 'hard',
        'case': ('Kaveri Fasteners makes bolts on an automatic line. On average 2% of bolts are defective, independently of each other. Bolts are packed in boxes of 10, and also shipped in lots of 50 for a customer who rejects a lot if it contains more than one defective. '
                 'Bolt length is normally distributed with mean 40 mm and SD 0.5 mm; bolts outside 39 mm to 41 mm are scrapped. (Area under the standard normal curve from z = 0 to z = 2 is 0.4772.)'),
        'mcqs': [
            CM('k1a', 'What is the probability that a box of 10 has no defective bolt?', ['0.8171', '0.98', '0.2', '0.1829'], 0,
               'Each bolt is defective with p = 0.02, independently, so a box of 10 is binomial. P(0) = q¹⁰ = 0.98¹⁰ ≈ 0.8171. The trap is 0.1829, which is the probability of at least one defective (1 − 0.8171). In practice: manufacturers quote such figures to customers as the share of defect-free packs.', 'moderate', 'round(0.98**10,4)', topic='Theoretical distributions and the binomial model'),
            CM('k1b', 'For a lot of 50 bolts, which approximation is appropriate and what is its parameter?', ['Poisson with m = 1', 'Poisson with m = 2', 'Normal with mean 50', 'Binomial with p = 0.5'], 0,
               "With n = 50 fairly large and p = 0.02 small, B(50, 0.02) is approximated by a Poisson distribution with m = np = 50 × 0.02 = 1. The trap is 'Poisson with m = 2', which uses the percentage 2 directly as the mean. In practice: buyers and suppliers use the Poisson approximation to agree acceptance-sampling plans for large lots.", 'moderate', topic='Where Poisson applies'),
            CM('k1c', 'Using that approximation, what is the probability that the lot is accepted (at most one defective)?', ['0.7358', '0.3679', '0.2642', '0.9197'], 0,
               'With m = 1, P(0) + P(1) = e⁻¹ + e⁻¹ × 1 = 2e⁻¹ = 2 × 0.3679 ≈ 0.7358. The trap is 0.3679, which is only P(0) and ignores lots with exactly one defective. In practice: this acceptance probability tells the supplier how many of its lots the customer will accept, which feeds directly into pricing and rework costs.', 'hard', 'round(2.71828**(-1)*(1+1),4)', topic='Poisson distribution'),
            CM('k1d', 'What proportion of bolts fall within the acceptable length of 39 mm to 41 mm?', ['0.9544', '0.4772', '0.6826', '0.9973'], 0,
               'z = (x − μ) ÷ σ: for 39 mm, z = (39 − 40) ÷ 0.5 = −2; for 41 mm, z = +2. Area = 2 × 0.4772 = 0.9544, so about 4.56% of bolts are scrapped. The trap is 0.4772, which covers only one side of the mean. In practice: manufacturers set tolerance limits in SD terms, the basis of six-sigma quality programmes.', 'moderate', '2*0.4772', topic='Standard normal variate and using the table'),
        ]}]

    viva = [
        V('v1', 'What conditions must hold for a binomial distribution to apply?',
          'The experiment consists of a fixed, finite number n of trials. Each trial has only two outcomes, success and failure. The probability of success p stays constant from trial to trial, and the trials are independent of each other.',
          [P('p1', 'Fixed, finite number of trials n', 2, 'fixed|finite|n trial|number of trial', min=1),
           P('p2', 'Only two outcomes — success or failure', 3, 'two outcome|two result|two possible|success and failure|success or failure|dichotom|only two'),
           P('p3', 'Probability of success p constant', 3, 'constant|same|does not change|remains the same|fixed', 'probabilit|p', min=2),
           P('p4', 'Trials independent', 2, 'independent|independence')], 'c1'),
        V('v2', 'What are the mean and variance of a binomial distribution, and how do they compare?',
          'The mean of a binomial distribution is n p and the variance is n p q, where q is one minus p. Since q is less than one, the variance is always less than the mean. The variance is greatest when p equals q equals one half, and then it equals n by four.',
          [P('p1', 'Mean = np', 3, ALT('mean {e} n p', 'mean np', 'mean is np', 'n p mean', e=('is', 'equals', 'equal to', 'equal', '='))),
           P('p2', 'Variance = npq', 3, ALT('variance {e} n p q', 'variance npq', 'variance is npq', e=('is', 'equals', 'equal to', 'equal', '='))),
           P('p3', 'Variance < mean', 2, ALT('variance {l} mean', 'mean {g} variance', l=('less than', 'smaller than', 'lower than', 'below', 'always less than', 'is less than', 'is always less than'), g=('greater than', 'more than', 'exceeds', 'larger than', 'is greater than', 'always greater than'))),
           P('p4', 'Maximum variance n/4 at p = 0.5', 2, 'n by 4|n 4|n over 4|n divided by 4|quarter|half|0.5|one half', min=1)], 'c2'),
        V('v3', 'State the main features of the Poisson distribution and when it approximates the binomial.',
          'The Poisson distribution has a single parameter m, so it is uniparametric, and its probability of x is e to the minus m times m to the power x over x factorial. Its mean and variance are both equal to m. It approximates the binomial when n is very large and p is very small so that m equals n p stays moderate.',
          [P('p1', 'Single parameter m (uniparametric)', 2, 'one parameter|single parameter|uniparametric|uni parametric|only parameter|parameter m'),
           P('p2', 'Mean = variance = m', 4, ALT('mean {a} variance {e} m', 'mean {e} variance', 'mean and variance are equal', 'mean and variance both equal', 'mean equals variance', 'variance equals mean', 'mean variance equal', 'mean variance both m', 'mean variance both equal', a=('and', 'equals', 'equal to', '=', 'is equal to'), e=('both equal', 'are equal', 'equal', 'equal to', 'equals', 'are both'))),
           P('p3', 'Approximates binomial when n large, p small, np moderate', 4, 'large|infinity|big', 'small|zero|rare|tiny', min=2)], 'c3'),
        V('v4', 'State the important properties of the normal distribution.',
          'The normal curve is bell-shaped and symmetrical about the mean, so the mean, median and mode are equal. It is defined by two parameters, mu and sigma. The quartile deviation is about 0.675 sigma and the mean deviation is about 0.8 sigma. The points of inflexion are at mu minus sigma and mu plus sigma. The two tails never touch the horizontal axis, and the total area under the curve is one.',
          [P('p1', 'Bell-shaped and symmetrical; mean = median = mode', 4, 'symmetric|bell', 'mean median mode|mean median and mode|mean equals median|equal|coincide', min=2),
           P('p2', 'QD ≈ 0.675σ and MD ≈ 0.8σ', 2, '0.675|0.67|0.8|four fifth|two third', min=1),
           P('p3', 'Points of inflexion at μ ± σ', 2, 'inflexion|inflection', 'mu minus sigma|mu plus sigma|plus or minus sigma|mu sigma|mean plus sd|mean minus sd|plus minus sigma|one standard deviation|one sigma', min=1),
           P('p4', 'Tails never touch the axis; total area = 1', 2, 'never touch|asymptot|does not touch|do not touch|total area|area 1|area is one|area one', min=1)], 'c5'),
        V('v5', 'What is the standard normal variate, and what share of values lie within one, two and three standard deviations of the mean?',
          'The standard normal variate z equals x minus mu divided by sigma; it has mean zero and standard deviation one. In a normal distribution about 68.27 percent of values lie within mu plus or minus one sigma, about 95.45 percent within two sigma, and about 99.73 percent within three sigma.',
          [P('p1', 'z = (x − μ)/σ', 3, ALT('x minus mu {d} sigma', 'x mu {d} sigma', 'x minus mean {d} sd', 'x minus mean {d} standard deviation', 'x minus mu over sigma', d=('divided by', 'by', 'over', 'upon'))),
           P('p2', 'Mean 0, SD 1', 2, 'zero|0', '1|one|unit', min=2),
           P('p3', '68.27%, 95.45%, 99.73%', 5, '68|68.27|68.26|two third', '95|95.45|95.44|95.5', '99.7|99.73|99.74|almost all', min=2)], 'c6'),
        V('v6', 'Give practical situations where the Poisson distribution is used.',
          'The Poisson distribution is used for counts of rare events in a large number of opportunities, for example the number of printing mistakes per page of a large book, the number of road accidents per minute on a busy road, the number of calls or demands per minute at a service centre, and the number of defects in a long roll of cloth.',
          [P('p1', 'Rare events over many opportunities', 4, 'rare|small probabilit|low probabilit|seldom|large number|many', min=1),
           P('p2', 'At least two examples (printing mistakes, accidents, calls/demands, defects)', 6, 'printing|misprint|typing|typo', 'accident', 'call|demand|arrival|customer', 'defect|flaw|fault', min=2)], 'c4'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch16', 'n': 1,
        'title': 'Theoretical Distributions',
        'outcomes': [
            'Explain why theoretical probability distributions are useful and distinguish discrete (binomial, Poisson) from continuous (normal) models.',
            'State the conditions and properties of the binomial distribution and compute probabilities, mean, variance and mode.',
            'Use the Poisson distribution, its properties and the Poisson approximation to the binomial.',
            'Apply the properties of the normal distribution and the standard normal table to find probabilities, quartiles and expected frequencies.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 60}, 'prereq': ['fnd-p3-ch15-u01'],
                 'exam_tip': 'MCQs here are mostly property-based: mean np, variance npq, mean = variance = m for Poisson, mean = median = mode for normal, QD = 0.675σ, MD = 0.8σ, inflexion at μ ± σ, and areas 68.27/95.45/99.73%. Learn these cold — each is a 30-second mark.'},
        'concepts': [
            {'id': 'c1', 'title': 'Theoretical distributions and the binomial model',
             'body': ['A theoretical (probability) distribution spreads the total probability 1 over the possible values of a random variable, the way a frequency distribution spreads total frequency over classes. It lets us predict frequencies, test whether data follow a model and make decisions when observation is costly.',
                      'Binomial conditions: (i) a fixed, finite number n of trials; (ii) each trial has only two outcomes — success or failure; (iii) probability of success p is constant (q = 1 − p); (iv) trials are independent.',
                      'Probability mass function: P(X = x) = ⁿCₓ pˣ qⁿ⁻ˣ, x = 0, 1, …, n. The probabilities are the successive terms of (q + p)ⁿ and add up to 1. Written X ~ B(n, p).'],
             'blocks': [t1],
             'analogy': 'Binomial is a series of n coin tosses with a possibly loaded coin — count the heads.',
             'work': 'In attribute sampling an auditor checks n vouchers, each either compliant or not; the number of exceptions follows a binomial model if the error rate is constant.'},
            {'id': 'c2', 'title': 'Properties of the binomial distribution',
             'body': ['Biparametric: n and p fix the distribution completely.',
                      'Mean μ = np; variance σ² = npq; SD = √(npq). Since q < 1, variance < mean. Variance is maximum when p = q = 0.5, and the maximum is n/4.',
                      'Mode: if (n + 1)p is not an integer, the mode is its integer part; if (n + 1)p is an integer, the distribution is bimodal with modes (n + 1)p and (n + 1)p − 1.',
                      'Symmetric when p = 0.5; positively skewed when p < 0.5 and negatively skewed when p > 0.5.',
                      'Additive property: if X ~ B(n₁, p) and Y ~ B(n₂, p) are independent (same p), X + Y ~ B(n₁ + n₂, p).'],
             'analogy': 'Variance < mean is like a binomial fingerprint — if a question says mean 4 and variance 5, it cannot be binomial.',
             'work': 'If 5% of a vendor\'s invoices are duplicates, out of 200 invoices you expect np = 10 duplicates with SD √9.5 ≈ 3.1 — a quick reasonableness check.'},
            {'id': 'c3', 'title': 'Poisson distribution',
             'body': ['P(X = x) = e⁻ᵐ mˣ / x!, x = 0, 1, 2, … (e ≈ 2.71828). Written X ~ P(m).',
                      'Uniparametric (only m). Mean = variance = m. Mode: integer part of m if m is not an integer; m and m − 1 (bimodal) if m is an integer.',
                      'Poisson approximation to binomial: when n → ∞ and p → 0 such that m = np stays finite (n large, p small, np moderate), B(n, p) ≈ P(m).',
                      'Additive property: if X ~ P(m₁) and Y ~ P(m₂) are independent, X + Y ~ P(m₁ + m₂).',
                      'Recurrence: P(x + 1) = P(x) × m/(x + 1) — handy for building a table quickly.'],
             'analogy': 'Poisson counts raindrops landing on one tile in a minute: many chances, each tiny.',
             'work': 'Claims per policy, system outages per month and errors per 1,000 transactions are typically modelled as Poisson counts.'},
            {'id': 'c4', 'title': 'Where Poisson applies',
             'body': ['Use it when the number of opportunities is very large but the chance of the event at each one is very small: printing mistakes per page of a large book; road accidents per minute on a busy road; radioactive emissions per minute; demands per minute at a health centre; defects per metre of cloth.',
                      'Binomial needs n and p; Poisson needs only the average rate m — useful when n is unknown or practically unlimited.'],
             'analogy': 'If you can count how often something happened but not how often it did not, think Poisson.',
             'work': 'A bank planning ATM cash or a call centre planning staff uses Poisson arrivals per interval.'},
            {'id': 'c5', 'title': 'Normal distribution',
             'body': ['The most important continuous distribution: f(x) = [1/(σ√(2π))] e^(−(x − μ)²/(2σ²)), −∞ < x < ∞. Written X ~ N(μ, σ²); biparametric (μ, σ).',
                      'Properties: bell-shaped and symmetrical about μ, so mean = median = mode = μ and skewness is zero; unimodal; QD ≈ 0.675σ (Q₁ = μ − 0.675σ, Q₃ = μ + 0.675σ); MD ≈ 0.8σ; points of inflexion at μ − σ and μ + σ; the two tails approach but never touch the x-axis; total area = 1, half on each side of μ.',
                      'Areas: P(μ − σ < X < μ + σ) ≈ 0.6827; P(μ − 2σ < X < μ + 2σ) ≈ 0.9545; P(μ − 3σ < X < μ + 3σ) ≈ 0.9973 — almost all values lie within ±3σ. (The ICAI material doubles the half-areas 0.34135 and 0.47725 and prints 0.6828 and 0.9546; the difference is only rounding, and either figure picks out the right option.)',
                      'Many distributions tend to normal: binomial when n is large and p not extreme, Poisson when m is large, and sampling distributions of means for large samples.'],
             'blocks': [table(['Interval', 'z-range', 'Area (approx.)'], [['μ ± σ', '−1 to 1', '0.6827'], ['μ ± 2σ', '−2 to 2', '0.9545'], ['μ ± 3σ', '−3 to 3', '0.9973'], ['μ to μ + σ', '0 to 1', '0.3413']], title='Normal curve areas to remember')],
             'analogy': 'The normal curve is a perfectly balanced hill — the peak, the middle point and the centre of gravity are all at the same spot.',
             'work': 'Value-at-risk models, process tolerances (±3σ) and grading on a curve all use normal areas.'},
            {'id': 'c6', 'title': 'Standard normal variate and using the table',
             'body': ['z = (x − μ)/σ converts any normal variable to the standard normal N(0, 1): mean, median and mode 0; SD 1; MD ≈ 0.8, QD ≈ 0.675; symmetrical about 0; inflexion at z = ±1.',
                      'Φ(k) = P(z ≤ k) is read from the table; by symmetry Φ(−k) = 1 − Φ(k). Many exam questions give the area from 0 to k instead; then P(z > k) = 0.5 − area(0, k) and P(−k < z < k) = 2 × area(0, k).',
                      'Steps: convert each x to z; sketch the curve and shade the region; combine table areas using symmetry; multiply by N for an expected frequency. For continuous X, P(X ≤ a) = P(X < a).'],
             'analogy': 'z is a currency converter: whatever the original unit (marks, grams, rupees), it restates the value as "how many SDs from the mean".',
             'work': 'A z-score of −2 for a branch\'s cash variance flags it as unusual (only about 2.3% of branches would be that low if all were normal) — a quick analytical review test.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Binomial: errors in a sample of invoices', 'difficulty': 'moderate', 'minutes': 10,
             'q': '10% of a client\'s invoices contain an error. An auditor picks 6 invoices at random. Find P(no error), P(exactly one), P(at most one), P(at least two), and the mean, variance and SD of the number of erroneous invoices.',
             'solution': [t1, wn('Working', f'P(0) = 0.9⁶ = {fm(p0)}. P(1) = 6 × 0.1 × 0.9⁵ = {fm(p1)}. P(≤ 1) = {fm(pl1)}. P(≥ 2) = 1 − {fm(pl1)} = {fm(pg2)}.'),
                          wn('Moments', f'Mean = np = {fm(mu1)}; variance = npq = {fm(v1)}; SD = {fm(sd1)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Recovering n and p; finding the mode', 'difficulty': 'moderate', 'minutes': 8,
             'q': '(a) A binomial distribution has mean 6 and variance 2.4. Find n, p and P(X = 6). (b) What is the mode of this distribution? (c) What is the mode of B(9, 0.5)?',
             'solution': [wn('(a)', f'npq/np = q = 2.4/6 = {fm(q2)}; p = {fm(p2)}; n = 6/0.6 = {fm(n2)}. P(6) = ¹⁰C₆ (0.6)⁶ (0.4)⁴ = 210 × 0.046656 × 0.0256 = {fm(px6)}.'),
                          wn('(b)', '(n + 1)p = 11 × 0.6 = 6.6, not an integer → mode = 6.'),
                          wn('(c)', '(n + 1)p = 10 × 0.5 = 5, an integer → bimodal: 5 and 4.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Poisson and the Poisson approximation', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) A long report has on average 1.5 typing mistakes per page. Find P(a page has no mistake), P(at most 2 mistakes) and P(more than 2). (Take e = 2.71828.) (b) 1% of cheques presented are returned. Use the Poisson approximation to find P(exactly 3 returns) among 200 cheques.',
             'solution': [wn('(a)', f'm = 1.5; e⁻¹·⁵ ≈ {fm(e15)}. P(0) = {fm(pp0)}. P(≤ 2) = e⁻¹·⁵ (1 + 1.5 + 1.125) = {fm(pp2)}. P(> 2) = {fm(pp3)}.'),
                          wn('(b)', f'm = np = 200 × 0.01 = {fm(m3)}. P(3) = e⁻² 2³/3! = {fm(pa3)}. (Exact binomial ≈ {fm(pb3)} — the approximation is close.)')],
             'checks': c3},
            {'id': 'i4', 'title': 'Normal distribution: marks of 1,000 students', 'difficulty': 'moderate', 'minutes': 10,
             'q': 'Marks of 1,000 students are normally distributed with mean 60 and SD 10. Given: area from z = 0 to 1 is 0.3413 and from 0 to 1.5 is 0.4332. Find (a) how many scored above 75, (b) how many scored between 50 and 70, (c) P(50 < X < 75), (d) the quartiles, mean deviation and points of inflexion.',
             'solution': [wn('(a)', f'z = (75 − 60)/10 = {fm(z1)}. P(X > 75) = 0.5 − 0.4332 = {fm(pg75)}; number ≈ 1,000 × 0.0668 ≈ {fm(n75)}.'),
                          wn('(b)', f'z = −1 to 1: 2 × 0.3413 = {fm(pmid)}; number ≈ {fm(nmid)}.'),
                          wn('(c)', f'z from −1 to 1.5: 0.3413 + 0.4332 = {fm(pb)}.'),
                          wn('(d)', 'Q₁ = 60 − 0.675 × 10 = 53.25; Q₃ = 66.75; MD ≈ 0.8 × 10 = 8; inflexion at 50 and 70.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Attribute sampling with a binomial model', 'role': 'Audit associate testing a control',
             'situation': 'The client says approvals are missing on only 2% of purchase orders. You test 25 POs and find 3 without approval.',
             'steps': ['If the true rate were 2%, X ~ B(25, 0.02); expected exceptions = 0.5.',
                       'P(X ≥ 3) = 1 − [P(0) + P(1) + P(2)] ≈ 1 − (0.6035 + 0.3079 + 0.0754) ≈ 0.013.',
                       'Such a result would occur only about 1.3% of the time if the client were right — strong evidence the rate is higher.',
                       'Conclude the control is not operating as described; extend testing and report to those charged with governance.'],
             'takeaway': 'A binomial tail probability tells you whether observed exceptions are "bad luck" or a real control failure.',
             'checks': [{'expr': 'round(1-(0.98**25+25*0.02*0.98**24+300*0.02**2*0.98**23),4)', 'value': round(1 - sum(binom(25, 0.02, x) for x in range(3)), 4), 'label': 'P(X >= 3)'}]},
            {'id': 'j2', 'title': 'Setting a cash buffer with the normal curve', 'role': 'Treasury executive',
             'situation': 'Daily net cash outflow at a branch is roughly normal with mean ₹18 lakh and SD ₹4 lakh. Management wants enough cash to cover about 97.7% of days.',
             'steps': ['97.7% corresponds to z ≈ 2 (area left of z = 2 is 0.5 + 0.4772).',
                       'Required cash = μ + 2σ = 18 + 8 = ₹26 lakh.',
                       'Revisit monthly — month-end and festival days break the "same distribution" assumption.'],
             'takeaway': 'μ + zσ turns a service level into a rupee figure.',
             'checks': [{'expr': '18+2*4', 'value': 26, 'label': 'cash buffer (₹ lakh)'}]},
        ],
        'mcqs': [
            mq('m1', 'Which is NOT a condition of the binomial distribution?', ['The probability of success changes from trial to trial', 'The number of trials is fixed', 'Each trial has two outcomes', 'Trials are independent'],
               "A binomial model needs a fixed number of independent trials, each with two outcomes and the same probability of success p. If p changes from trial to trial, the model breaks, so that is NOT a condition. 'The number of trials is fixed' is the trap: it is a genuine condition. In practice: drawing invoices without replacement from a small batch changes p, so the binomial is only an approximation there.", 'c1', topic='Theoretical distributions and the binomial model'),
            nq('m2', 'For a binomial distribution with n = 20 and p = 0.3, the mean is:', '20*0.3', [4.2, 14, 0.3],
               'The mean of a binomial distribution is np = 20 × 0.3 = 6. The trap is 4.2, which is the variance npq (20 × 0.3 × 0.7), not the mean. In practice: if 30% of 20 sampled invoices are expected to have GST errors, the auditor expects about 6 erroneous invoices on average.', 'c2', topic='Properties of the binomial distribution'),
            nq('m3', 'For a binomial distribution with n = 20 and p = 0.3, the variance is:', '20*0.3*0.7', [6, 2.05, 14],
               'The variance of a binomial is npq = 20 × 0.3 × 0.7 = 4.2. The trap is 6, which is the mean np. 2.05 is the standard deviation (√4.2). In practice: knowing the spread around the expected number of errors helps an auditor judge whether an observed error count is unusual.', 'c2', topic='Properties of the binomial distribution'),
            nq('m4', 'A binomial distribution has mean 8 and variance 4. The number of trials n is:', '8/(1-4/8)', [8, 32, 12],
               'Variance ÷ mean = npq ÷ np = q, so q = 4 ÷ 8 = 0.5 and p = 0.5. Then n = mean ÷ p = 8 ÷ 0.5 = 16. The trap is 8, which assumes n equals the mean. In practice: working backwards from summary figures to model parameters is common when only reported averages and variances are available.', 'c2', 'moderate', topic='Properties of the binomial distribution'),
            mq('m5', 'A binomial distribution with mean 4 and variance 5 is:', ['Impossible, because the variance of a binomial must be less than its mean', 'Possible with p = 0.8', 'Possible with n = 20', 'Possible only if n is very large'],
               "For a binomial, variance = npq and mean = np, so variance ÷ mean = q, which must be less than 1. Here q = 5 ÷ 4 = 1.25, which is impossible. 'Possible with p = 0.8' is the trap: no value of p can make the variance exceed the mean. In practice: checking such internal consistency is how a reviewer spots an error in a statistical report.", 'c2', 'moderate', topic='Properties of the binomial distribution'),
            nq('m6', 'The maximum possible variance of a binomial distribution with n = 12 is:', '12/4', [6, 12, 2.4],
               'Variance npq is greatest when p = q = 0.5, giving 12 × 0.5 × 0.5 = 3. The trap is 6, which is the mean at p = 0.5, not the variance. In practice: uncertainty is highest when an outcome is a 50–50 call, which is why pollsters plan sample sizes assuming p = 0.5.', 'c2', 'moderate', topic='Properties of the binomial distribution'),
            nq('m7', 'Four fair coins are tossed. The probability of exactly two heads is:', '6*0.5**4', [0.5, 0.25, 0.0625],
               "P(X = 2) = ⁴C₂ × (1/2)² × (1/2)² = 6 × 1/16 = 0.375. The trap is 0.5, the intuitive 'half the coins' guess that ignores the counting. In practice: binomial probabilities like this are used in acceptance sampling to find the chance of a given number of defectives in a sample.", 'c1', topic='Theoretical distributions and the binomial model'),
            nq('m8', 'In 5 independent trials with p = 0.4, the probability of no success is:', 'round(0.6**5,4)', [0.6, 0.0102, 0.4],
               'No success means all 5 trials fail: P(0) = q⁵ = 0.6⁵ ≈ 0.0778. The trap is 0.0102, which is p⁵ (all successes). In practice: the probability that a sample contains no errors at all is central to discovery sampling in audit, where finding zero errors supports reliance on a control.', 'c1', topic='Theoretical distributions and the binomial model'),
            mq('m9', 'The mode(s) of B(9, 0.5) is/are:', ['4 and 5', '4.5', '5 only', '4 only'],
               'For a binomial, if (n + 1)p is an integer, there are two modes: (n + 1)p and (n + 1)p − 1. Here (9 + 1) × 0.5 = 5, so the modes are 5 and 4. The trap is 4.5, the mean, which is not a possible value of a count. In practice: the most likely number of defectives in a batch guides how quality inspectors set their expectations.', 'c2', 'hard', topic='Properties of the binomial distribution'),
            mq('m10', 'If X ~ B(5, 0.3) and Y ~ B(7, 0.3) are independent, then X + Y follows:', ['B(12, 0.3)', 'B(12, 0.6)', 'B(35, 0.3)', 'B(6, 0.3)'],
               "Independent binomials with the same p can be added: n's add, p stays the same. So X + Y ~ B(5 + 7, 0.3) = B(12, 0.3). The trap is B(12, 0.6), which wrongly adds the probabilities. In practice: combining two independent audit samples with the same error rate gives one larger binomial sample, which simplifies evaluation.", 'c2', 'moderate', topic='Properties of the binomial distribution'),
            mq('m11', 'A binomial distribution is symmetrical when:', ['p = 0.5', 'p < 0.5', 'p > 0.5', 'n is large regardless of p'],
               "A binomial distribution is symmetrical only when p = q = 0.5. If p < 0.5 it is positively skewed, and if p > 0.5 it is negatively skewed. 'n is large regardless of p' is the trap: large n makes it closer to symmetric, but exact symmetry needs p = 0.5. In practice: rare events like defaults (small p) always give right-skewed counts.", 'c2', topic='Properties of the binomial distribution'),
            nq('m12', 'For a Poisson distribution the variance is 3. Its mean is:', '3', [9, 1.73, 1.5],
               'In a Poisson distribution the mean and variance are equal, both being m. So if the variance is 3, the mean is 3. The trap is 1.73, which is the standard deviation (√3). In practice: if call-centre complaints average 3 per hour, their variance is also 3, a quick check on whether a Poisson model fits.', 'c3', topic='Poisson distribution'),
            nq('m13', 'For a Poisson variable, P(X = 1) = P(X = 2). The mean is:', '2', [1, 1.5, 4],
               'Set P(1) = P(2): e⁻ᵐ m = e⁻ᵐ m² ÷ 2. Dividing both sides by e⁻ᵐ m gives 1 = m ÷ 2, so m = 2. The trap is 1: that is the mean for which P(0) = P(1), not P(1) = P(2). In practice: fitting a Poisson parameter from observed frequencies is how analysts model arrival rates of customers or claims.', 'c3', 'hard', topic='Poisson distribution'),
            nq('m14', 'For a Poisson distribution with mean 4, the standard deviation is:', '4**0.5', [4, 16, 0.5],
               'For a Poisson distribution the variance equals the mean, so the variance is 4 and SD = √4 = 2. The trap is 4, which is the variance, not the SD. In practice: if a branch receives on average 4 fraud alerts a week, the typical variation around that is about 2 alerts.', 'c3', topic='Poisson distribution'),
            mq('m15', 'The mode of a Poisson distribution with m = 3.6 is:', ['3', '4', '3.6', '3 and 4'],
               "When m is not an integer, the Poisson distribution has a single mode equal to the integer part of m. For m = 3.6, the mode is 3. The trap is '3 and 4': two modes occur only when m is an integer. In practice: the most likely number of daily insurance claims is found this way for capacity planning.", 'c3', 'moderate', topic='Poisson distribution'),
            mq('m16', 'The mode(s) of a Poisson distribution with m = 3 is/are:', ['2 and 3', '3 only', '2 only', '1.5'],
               "When m is an integer, the Poisson distribution is bimodal, with modes m and m − 1. For m = 3, the modes are 3 and 2. The trap is '3 only', which forgets that P(2) = P(3) when m = 3. In practice: knowing two counts are equally most likely helps when staffing for customer arrivals.", 'c3', 'moderate', topic='Poisson distribution'),
            nq('m17', 'For a Poisson variable with m = 2 (e⁻² = 0.1353), P(X ≥ 1) is:', '1-0.1353', [0.1353, 0.2706, 0.5],
               'P(X ≥ 1) = 1 − P(0) = 1 − e⁻² = 1 − 0.1353 = 0.8647. The trap is 0.1353, which is P(0) itself. In practice: the complement rule gives the chance of at least one event, such as at least one machine breakdown in a shift.', 'c3', topic='Poisson distribution'),
            nq('m18', 'For m = 2 (e⁻² = 0.1353), P(X = 2) is:', '0.1353*2**2/2', [0.1353, 0.5412, 0.0677],
               'P(X = 2) = e⁻ᵐ mˣ ÷ x! = 0.1353 × 2² ÷ 2! = 0.1353 × 2 = 0.2706. The trap is 0.5412, which forgets to divide by 2!. In practice: Poisson probabilities are used to estimate the chance of a given number of accidents, defects or claims in a period.', 'c3', 'moderate', topic='Poisson distribution'),
            mq('m19', 'The Poisson distribution is a good approximation to the binomial when:', ['n is large, p is small and np is moderate', 'n is small and p is large', 'p = 0.5', 'n = 1'],
               "The Poisson approximates the binomial when n is large, p is small and np (the mean) is moderate. 'p = 0.5' is the trap: with p = 0.5, the normal approximation is used instead. In practice: defects in a large production run or errors in a large population of entries are rare events, ideal for the Poisson model.", 'c3', topic='Where Poisson applies'),
            nq('m20', 'If X ~ P(1.5) and Y ~ P(2.5) are independent, the variance of X + Y is:', '1.5+2.5', [2, 3.75, 6.25],
               'Independent Poisson variables add: X + Y ~ P(1.5 + 2.5) = P(4). For a Poisson, variance = mean, so the variance is 4. The trap is 3.75, which multiplies 1.5 × 2.5 instead of adding. In practice: if two branches independently receive complaints at rates 1.5 and 2.5 per day, total daily complaints follow P(4).', 'c3', 'moderate', topic='Poisson distribution'),
            mq('m21', 'The number of printing mistakes per page of a large book is best described by:', ['Poisson distribution', 'Normal distribution', 'Binomial with p = 0.5', 'Uniform distribution'],
               'Printing mistakes per page are rare events with many opportunities (every character could be wrong), which is the classic Poisson situation. The normal distribution is the trap: it suits continuous measurements like heights, not small counts of rare events. In practice: Poisson models are used for counting rare events like insurance claims, system failures and fraud alerts.', 'c4', topic='Where Poisson applies'),
            mq('m22', 'For a normal distribution:', ['Mean = median = mode', 'Mean > median > mode', 'Mean < median < mode', 'Mode = 3 median − 2 mean is impossible'],
               "The normal curve is perfectly symmetrical and has a single peak, so mean, median and mode coincide at μ. 'Mean > median > mode' is the trap: that describes a positively skewed distribution. In practice: when the mean and median of a dataset are far apart, analysts know a normal model may not fit.", 'c5', topic='Normal distribution'),
            nq('m23', 'A normal distribution has SD 8. Its quartile deviation is approximately:', '0.675*8', [6.4, 8, 4],
               'For a normal distribution, QD ≈ 0.675σ = 0.675 × 8 = 5.4. The trap is 6.4, which is the mean deviation (0.8σ), not the quartile deviation. In practice: these fixed ratios allow quick conversions in risk models where returns are assumed to be roughly normal.', 'c5', topic='Normal distribution'),
            nq('m24', 'A normal distribution has SD 15. Its mean deviation is approximately:', '0.8*15', [10.13, 15, 7.5],
               'For a normal distribution, MD ≈ 0.8σ = 0.8 × 15 = 12. The trap is 10.13, which is the quartile deviation (0.675 × 15 = 10.125, rounded). In practice: such ratios help when a report gives only one measure of dispersion and another is needed for comparison.', 'c5', topic='Normal distribution'),
            mq('m25', 'The points of inflexion of N(50, 16) are at:', ['46 and 54', '34 and 66', '42 and 58', '50 and 66'],
               'In N(μ, σ²), the second figure is the variance, so σ = √16 = 4. The points of inflexion are μ ± σ = 50 ± 4 = 46 and 54. The trap is 34 and 66, which wrongly treats 16 as σ. In practice: misreading variance as standard deviation is a common error when reading risk reports, quadrupling or shrinking the apparent risk.', 'c5', 'moderate', topic='Normal distribution'),
            nq('m26', 'In a normal distribution, the percentage of values within μ ± 2σ is about:', '95.45', [68.27, 99.73, 50],
               'In a normal distribution, about 68.27% of values lie within μ ± σ, 95.45% within μ ± 2σ and 99.73% within μ ± 3σ. So the answer is 95.45. The trap is 68.27, which is the share within one SD. In practice: Value-at-Risk and quality-control limits in manufacturing are set using these normal coverage figures.', 'c5', topic='Normal distribution'),
            nq('m27', 'X ~ N(60, 64). The z-value for x = 72 is:', '(72-60)/8', [0.19, 12, 1.33],
               'N(60, 64) gives σ = √64 = 8. z = (x − μ) ÷ σ = (72 − 60) ÷ 8 = 1.5. The trap is 0.19, which divides 12 by 64, the variance, instead of the SD. In practice: z-scores are used to compare performance on different scales, such as standardising branch sales against the network average.', 'c6', topic='Standard normal variate and using the table'),
            nq('m28', 'Given that the area from z = 0 to z = 1 is 0.3413, P(z > 1) is:', '0.5-0.3413', [0.3413, 0.8413, 0.6826],
               'The area to the right of z = 0 is 0.5. Subtract the area from 0 to 1: P(z > 1) = 0.5 − 0.3413 = 0.1587. The trap is 0.8413, which is P(z < 1), the area to the left. In practice: such tail areas give the chance of an extreme outcome, for example a monthly return worse than one SD below average.', 'c6', topic='Standard normal variate and using the table'),
            nq('m29', 'The two quartiles of a normal distribution are 42.25 and 55.75. Its standard deviation is:', '(55.75-42.25)/2/0.675', [6.75, 13.5, 8],
               'For a normal distribution, QD = (Q₃ − Q₁) ÷ 2 = (55.75 − 42.25) ÷ 2 = 6.75, and QD ≈ 0.675σ. So σ = 6.75 ÷ 0.675 = 10. The trap is 6.75, which is the QD itself. In practice: recovering σ from quartiles helps when only a range of typical values is published, such as an interquartile salary range.', 'c5', 'hard', topic='Normal distribution'),
            mq('m30', 'The standard normal distribution has:', ['Mean 0 and SD 1', 'Mean 1 and SD 0', 'Mean 0 and SD 0', 'Mean and SD both 1'],
               "The standard normal variate z = (x − μ) ÷ σ always has mean 0 and standard deviation 1. 'Mean 1 and SD 0' is the trap: an SD of 0 would mean no variation at all. In practice: standardising variables to mean 0 and SD 1 is the first step in credit-scoring models and many statistical tools.", 'c6', topic='Standard normal variate and using the table'),
            mq('m31', 'The tails of the normal curve:', ['Approach the x-axis but never touch it', 'Touch the x-axis at μ ± 3σ', 'Cross the x-axis at μ ± 3σ', 'End at the quartiles'],
               "The normal curve is asymptotic: its tails get ever closer to the x-axis but never touch it, so any value is possible, however unlikely. 'Touch the x-axis at μ ± 3σ' is the trap: only about 0.27% of values lie beyond, but the curve continues. In practice: this is why risk managers worry about rare 'tail events' in financial markets.", 'c5', topic='Normal distribution'),
            mq('m32', 'Which statement is correct?', ['Poisson is uniparametric; binomial and normal are biparametric', 'All three are uniparametric', 'Normal is uniparametric', 'Binomial is uniparametric'],
               "The Poisson distribution has one parameter (m), so it is uniparametric. The binomial has two (n and p) and the normal has two (μ and σ), so both are biparametric. 'Binomial is uniparametric' is the trap: it needs both n and p. In practice: knowing how many parameters a model needs tells an analyst how much data must be estimated before using it.", 'c3', 'moderate', topic='Poisson distribution'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'The probability that a component fails a stress test is 0.2. A batch of 5 components is tested. Find (a) P(no failure), (b) P(exactly 2 failures), (c) P(at least one failure), (d) the mean and variance of failures, (e) in how many of 200 such batches you expect no failure.',
             'model': [wn('(a)', f'0.8⁵ = {fm(qa)}.'), wn('(b)', f'⁵C₂ (0.2)² (0.8)³ = 10 × 0.04 × 0.512 = {fm(qb)}.'),
                       wn('(c)', f'1 − 0.8⁵ = {fm(qc)}.'), wn('(d)', f'Mean = 5 × 0.2 = {fm(qm)}; variance = 5 × 0.2 × 0.8 = {fm(qv)}.'),
                       wn('(e)', '200 × 0.32768 ≈ 66 batches.')],
             'scheme': [{'id': 's1', 'pt': 'n = 5, p = 0.2, q = 0.8 identified', 'm': 0.5, 'skill': 'concept'},
                        {'id': 's2', 'pt': '(a) and (b) correct', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(c) via complement', 'm': 1, 'skill': 'application'},
                        {'id': 's4', 'pt': '(d) mean 1, variance 0.8', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': '(e) expected frequency 66', 'm': 0.5, 'skill': 'application'}],
             'remarks': ['Using p for the "success" of interest (failure) avoids confusion — define it in the first line.'],
             'mistakes': ['Swapping p and q.', 'Computing P(at least one) as 5 × 0.2.'],
             'tips': ['"At least one" → 1 − P(0) every time.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'The probability that a transaction is flagged as suspicious is 0.004. In a day, 500 transactions are processed. Using the Poisson approximation (e⁻² = 0.1353), find (a) the mean number flagged, (b) P(none), (c) P(exactly one), (d) P(at most two), (e) P(more than two).',
             'model': [wn('(a)', f'm = np = 500 × 0.004 = {fm(q2m)}.'), wn('(b)', f'e⁻² = {fm(q2p0)}.'), wn('(c)', f'e⁻² × 2 = {fm(q2p1)}.'),
                       wn('(d)', f'e⁻² (1 + 2 + 2²/2!) = 5 × 0.1353 = {fm(q2le)}.'), wn('(e)', f'1 − {fm(q2le)} = {fm(q2ge)}.')],
             'scheme': [{'id': 's1', 'pt': 'Justify Poisson (n large, p small); m = 2', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'P(0) and P(1)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'P(≤ 2) = 5 × 0.1353 = 0.6765', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'P(> 2) by complement', 'm': 1, 'skill': 'application'}],
             'remarks': ['Write the pmf once; then each value is one line.'],
             'mistakes': ['Forgetting the x! in the denominator.', 'Using m = 0.004.'],
             'tips': ['P(x + 1) = P(x) × m/(x + 1) speeds things up.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': 'The life of LED bulbs is normally distributed with mean 1,200 hours and SD 80 hours. Given: area from z = 0 to 1.25 is 0.3944 and from 0 to 1.5 is 0.4332. Out of 5,000 bulbs find (a) the probability that a bulb lasts more than 1,300 hours, (b) the probability that it lasts between 1,080 and 1,300 hours and the expected number of such bulbs, (c) the first quartile and mean deviation of life.',
             'model': [wn('(a)', f'z = (1,300 − 1,200)/80 = {fm(z3a)}; P = 0.5 − 0.3944 = {fm(q3a)}.'),
                       wn('(b)', f'z for 1,080 = {fm(z3b)}. P = 0.4332 + 0.3944 = {fm(q3b)}; number ≈ 5,000 × 0.8276 = {fm(q3n)}.'),
                       wn('(c)', 'Q₁ = 1,200 − 0.675 × 80 = 1,146 hours; MD ≈ 0.8 × 80 = 64 hours.')],
             'scheme': [{'id': 's1', 'pt': 'z-values 1.25 and −1.5', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': '(a) 0.1056', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(b) area 0.8276 using symmetry', 'm': 1.5, 'skill': 'application'},
                        {'id': 's4', 'pt': '(b) expected number 4,138', 'm': 0.5, 'skill': 'computation'},
                        {'id': 's5', 'pt': '(c) Q₁ = 1,146 and MD = 64', 'm': 2, 'skill': 'concept'}],
             'remarks': ['A quick sketch of the curve with the shaded area prevents adding when you should subtract.'],
             'mistakes': ['Subtracting the two areas in (b) although the values lie on opposite sides of the mean.', 'Using QD = 0.8σ.'],
             'tips': ['Opposite sides of μ → add areas; same side → subtract.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Binomial: n fixed, two outcomes, constant p, independent trials; P(x) = ⁿCₓ pˣ qⁿ⁻ˣ.',
                        'Binomial mean np, variance npq (< mean), max variance n/4 at p = 0.5; mode from (n + 1)p.',
                        'Poisson: P(x) = e⁻ᵐ mˣ/x!; mean = variance = m; approximates binomial when n large, p small.',
                        'Normal: symmetric, mean = median = mode = μ; QD ≈ 0.675σ; MD ≈ 0.8σ; inflexion μ ± σ.',
                        'Areas: ±1σ 68.27%, ±2σ 95.45%, ±3σ 99.73%; z = (x − μ)/σ.'],
            'remember': ['Binomial & normal are biparametric; Poisson is uniparametric.', 'Additive property needs the same p (binomial).', 'Integer (n + 1)p or integer m → bimodal.', 'Opposite sides of μ → add areas.'],
            'traps': ['Variance > mean ⇒ not binomial.', 'σ² = 16 means σ = 4 — not 16.', 'QD = 0.675σ, MD = 0.8σ — do not swap.', 'P(X ≥ 1) = 1 − P(0), never n × p.']},
        'quickref': [
            {'k': 'Binomial pmf', 'v': 'P(x) = ⁿCₓ pˣ qⁿ⁻ˣ, x = 0 … n'},
            {'k': 'Binomial moments', 'v': 'Mean np; variance npq; max variance n/4 (p = 0.5)'},
            {'k': 'Binomial mode', 'v': 'Integer part of (n + 1)p; if integer, (n + 1)p and (n + 1)p − 1'},
            {'k': 'Poisson pmf', 'v': 'P(x) = e⁻ᵐ mˣ / x!; mean = variance = m'},
            {'k': 'Poisson approx.', 'v': 'B(n, p) ≈ P(np) for large n, small p'},
            {'k': 'Normal', 'v': 'Mean = median = mode = μ; QD ≈ 0.675σ; MD ≈ 0.8σ; inflexion μ ± σ'},
            {'k': 'Areas', 'v': 'μ ± σ: 68.27%; μ ± 2σ: 95.45%; μ ± 3σ: 99.73%'},
            {'k': 'Standard normal', 'v': 'z = (x − μ)/σ ~ N(0, 1); Φ(−k) = 1 − Φ(k)'},
        ],
        'viva': viva, 'cases': cases,
    }

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        's1': _K('q 0.8|0.8 q|1 0.2 0.8|0.8'),
        's2': _N(0.3277, 0.2048),
        's3': _N(0.6723),
        's4': _K('mean 1|np 1|5 0.2 1|mean is 1', 'variance 0.8|npq 0.8|var 0.8|variance 5 0.2 0.8 0.8'),
        's5': _K('66|65.5'),
    },
    'q2': {
        's1': _K('m 2|mean 2|np 2|500 x 0.004 2|500 0.004 2|lambda 2|parameter 2|mean number 2'),
        's2': _N(0.1353, 0.2706),
        's3': _N(0.6765),
        's4': _N(0.3235),
    },
    'q3': {
        's1': _K('80 1.25|100 80 1.25|1300 1200', '80 -1.5|-120 80|1080 1200|1080 -1.5|z -1.5'),
        's2': _N(0.1056),
        's3': _N(0.8276),
        's4': _N(4138),
        's5': _N(1146, 64),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
