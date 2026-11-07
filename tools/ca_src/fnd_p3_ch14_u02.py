"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 14 Unit 2 Dispersion.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as _CM


def CM(*a, topic=None, **k):
    d = _CM(*a, **k); d['topic'] = topic
    return d

UID = 'fnd-p3-ch14-u02'


def ev(expr): return eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})


class Checks(Checks):
    """Records the check as lib.Checks does (value stored to 2 decimals), but returns the value to 4 decimals for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = round(ev(expr), 4)
        return int(v) if v == int(v) else v


def fm(v, unit=''):
    v = round(v, 2)
    s = inr(int(v)) if v == int(v) else f'{v:.2f}'.rstrip('0').rstrip('.')
    return s + (' ' + unit if unit else '')


def mq(mid, q, opts, explain, concept, diff='core', topic=None):
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit='', topic=None):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def quart(xs, k, m):
    xs = sorted(xs); pos = k * (len(xs) + 1) / m
    i = int(pos); fr = pos - i
    return xs[i - 1] + fr * (xs[i] - xs[i - 1]) if fr else xs[i - 1]


def build():
    # ---------------- Illustration 1: range, coefficient; QD ----------------
    c1 = Checks()
    pr = [412, 398, 431, 405, 420, 389, 427]
    r1 = c1.add(f'{max(pr)}-{min(pr)}', 'range of prices')
    cr1 = c1.add(f'round(({max(pr)}-{min(pr)})/({max(pr)}+{min(pr)})*100,2)', 'coefficient of range')
    rg = c1.add('59.5-9.5', 'range of grouped data from extreme boundaries')
    crg = c1.add('round(50/(59.5+9.5)*100,2)', 'coefficient of range, grouped')
    dq = [22, 27, 31, 35, 38, 41, 45, 52, 58, 66]
    Q1, Q3 = quart(dq, 1, 4), quart(dq, 3, 4)
    q1v = c1.add('27+0.75*(31-27)', 'Q1 = 2.75th value'); q3v = c1.add('52+0.25*(58-52)', 'Q3 = 8.25th value')
    assert q1v == Q1 and q3v == Q3
    qd = c1.add('(53.5-30)/2', 'quartile deviation')
    cqd = c1.add('round((53.5-30)/(53.5+30)*100,2)', 'coefficient of QD')

    # ---------------- Illustration 2: mean deviation ----------------
    c2 = Checks()
    md = [5, 8, 10, 13, 20, 28]
    mean2 = c2.add('(5+8+10+13+20+28)/6', 'mean'); med2 = c2.add('(10+13)/2', 'median')
    rows2 = [[str(x), fm(abs(x - mean2)), fm(abs(x - med2))] for x in md]
    s_mean = sum(abs(x - mean2) for x in md); s_med = sum(abs(x - med2) for x in md)
    rows2.append(['Total', fm(s_mean), fm(s_med)])
    t2 = table(['x', '|x − 14|', '|x − 11.5|'], rows2, num=[1, 2], total=True)
    mdm = c2.add('round(40/6,2)', 'MD about mean'); mdd = c2.add('round(38/6,2)', 'MD about median')
    c2.add('round(40/6/14*100,2)', 'coefficient of MD about mean'); c2.add('round(38/6/11.5*100,2)', 'coefficient of MD about median')

    # ---------------- Illustration 3: SD grouped, CV ----------------
    c3 = Checks()
    f3 = [4, 10, 16, 12, 8]; d3 = [-2, -1, 0, 1, 2]
    sfd = sum(a * b for a, b in zip(f3, d3)); sfd2 = sum(a * b * b for a, b in zip(f3, d3))
    rows3 = [[f'{10 * i}–{10 * i + 10}', str(f3[i]), str(10 * i + 5), str(d3[i]), str(f3[i] * d3[i]), str(f3[i] * d3[i] ** 2)] for i in range(5)]
    rows3.append(['Total', '50', '', '', str(sfd), str(sfd2)])
    t3 = table(['Weekly sales (units)', 'f', 'Mid x', 'd = (x − 25)/10', 'fd', 'fd²'], rows3, num=[1, 4, 5], total=True, title='Weekly sales of 50 outlets')
    m3 = c3.add(f'25+{sfd}/50*10', 'mean')
    sd3 = c3.add(f'round(10*({sfd2}/50-({sfd}/50)**2)**0.5,2)', 'SD by step deviation')
    cv3 = c3.add(f'round(10*({sfd2}/50-({sfd}/50)**2)**0.5/27*100,2)', 'CV %')
    cva = c3.add('12/48*100', 'CV batsman A'); cvb = c3.add('7.2/36*100', 'CV batsman B')

    # ---------------- Illustration 4: combined and corrected SD ----------------
    c4 = Checks()
    cm4 = c4.add('(40*50+60*60)/100', 'combined mean')
    cs4 = c4.add('round(((40*36+60*64+40*(50-56)**2+60*(60-56)**2)/100)**0.5,2)', 'combined SD')
    sx = c4.add('20*40-53+35', 'corrected sum'); sx2 = c4.add('20*(5**2+40**2)-53**2+35**2', 'corrected sum of squares')
    cmean = c4.add('782/20', 'corrected mean')
    csd = c4.add('round((30916/20-(782/20)**2)**0.5,2)', 'corrected SD')
    n10 = c4.add('round(((10**2-1)/12)**0.5,2)', 'SD of first 10 natural numbers')
    two = c4.add('(20-8)/2', 'SD of two numbers 8 and 20')

    # ---------------- Question 1 ----------------
    q1c = Checks()
    fq = [6, 14, 20, 10]; dq1 = [-2, -1, 0, 1]
    qfd = sum(a * b for a, b in zip(fq, dq1)); qfd2 = sum(a * b * b for a, b in zip(fq, dq1))
    rq1 = [[f'{100 + 20 * i}–{120 + 20 * i}', str(fq[i]), str(110 + 20 * i), str(dq1[i]), str(fq[i] * dq1[i]), str(fq[i] * dq1[i] ** 2)] for i in range(4)]
    rq1.append(['Total', '50', '', '', str(qfd), str(qfd2)])
    tq1 = table(['Daily output (units)', 'f', 'Mid x', 'd = (x − 150)/20', 'fd', 'fd²'], rq1, num=[1, 4, 5], total=True)
    qm = q1c.add(f'150+({qfd})/50*20', 'mean')
    qs = q1c.add(f'round(20*({qfd2}/50-({qfd}/50)**2)**0.5,2)', 'SD')
    qcv = q1c.add(f'round(20*({qfd2}/50-({qfd}/50)**2)**0.5/{150 + qfd / 50 * 20}*100,2)', 'CV')

    # ---------------- Question 2 ----------------
    q2c = Checks()
    q2m = q2c.add('(50*4500+70*5100)/120', 'combined mean wage')
    q2s = q2c.add('round(((50*300**2+70*400**2+50*(4500-4850)**2+70*(5100-4850)**2)/120)**0.5,2)', 'combined SD')

    # ---------------- Question 3 ----------------
    q3c = Checks()
    d3x = [14, 19, 23, 26, 30, 34, 37, 45, 51]
    qq1 = q3c.add('19+0.5*(23-19)', 'Q1 = 2.5th value'); qq3 = q3c.add('37+0.5*(45-37)', 'Q3 = 7.5th value')
    assert qq1 == quart(d3x, 1, 4) and qq3 == quart(d3x, 3, 4)
    qqd = q3c.add('(41-21)/2', 'QD'); qcq = q3c.add('round((41-21)/(41+21)*100,2)', 'coefficient of QD')
    q3med = q3c.add('30', 'median = 5th value')
    smd = sum(abs(x - 30) for x in d3x)
    q3md = q3c.add(f'round({smd}/9,2)', 'MD about median')
    q3c.add(f'round({smd}/9/30*100,2)', 'coefficient of MD about median')

    # ---------------- Case ----------------
    kc = Checks()
    cva_ = kc.add('round(4.2/1.4*100,2)', 'CV Fund A'); cvb_ = kc.add('round(3.0/1.2*100,2)', 'CV Fund B')
    cases = [{
        'id': 'k1', 'title': 'Choosing the steadier of two mutual funds', 'difficulty': 'moderate',
        'case': ('A client asks her CA which of two equity funds has been steadier. Over the last 36 months, Fund A gave a mean monthly return of 1.4% with a standard deviation of 4.2%; '
                 'Fund B gave a mean of 1.2% with a standard deviation of 3.0%. Fund A\'s best and worst months were +11.5% and −9.1%. The client also asks what would happen to the figures if a flat 0.1% monthly fee were deducted from every return.'),
        'mcqs': [
            CM('k1a', 'What is the coefficient of variation of Fund A?', ['300%', '33.33%', '250%', '420%'], 0,
               "CV = SD ÷ mean × 100 = 4.2 ÷ 1.4 × 100 = 300%. The trap is 33.33%, which divides the mean by the SD the wrong way round. In practice: CV expresses risk per unit of return, which is how a CA compares the volatility of schemes for a client's investment portfolio.", 'core', 'round(4.2/1.4*100,2)', topic='Standard deviation, variance and coefficient of variation'),
            CM('k1b', 'Which fund is more consistent, and why?', ['Fund B — its CV (250%) is lower', 'Fund A — its mean is higher', 'Fund A — its CV is higher', 'Both are equally consistent'], 0,
               "Consistency is judged by the relative measure. Fund B's CV = 3.0 ÷ 1.2 × 100 = 250%, lower than Fund A's 300%, so Fund B is steadier. 'Fund A, because its mean is higher' is the trap: a higher return says nothing about steadiness. In practice: financial planners in India use such comparisons when advising risk-averse clients like retirees.", 'moderate', topic='Standard deviation, variance and coefficient of variation'),
            CM('k1c', 'What is the range of Fund A\'s monthly returns?', ['20.6', '2.4', '11.5', '10.3'], 0,
               'Range = largest − smallest = 11.5 − (−9.1) = 11.5 + 9.1 = 20.6 percentage points. The trap is 2.4, which subtracts 9.1 without handling the negative sign correctly. In practice: the spread between best and worst months is reported in mutual-fund factsheets as an easy-to-read indicator of volatility.', 'core', '11.5-(-9.1)', topic='Range and coefficient of range'),
            CM('k1d', 'If a flat 0.1% fee is deducted from every monthly return, Fund A\'s standard deviation will:', ['Remain 4.2%', 'Fall to 4.1%', 'Rise to 4.3%', 'Depend on the number of months'], 0,
               "Deducting the same 0.1% from every return is a change of origin, which shifts all values but does not change their spread, so the SD stays 4.2%. 'Fall to 4.1%' is the trap: only the mean falls (to 1.3%), and so the CV does change. In practice: expense ratios reduce a fund's average return but not its volatility.", 'hard', topic='Standard deviation, variance and coefficient of variation'),
        ]}]

    viva = [
        V('v1', 'What is the difference between absolute and relative measures of dispersion?',
          'Absolute measures such as range, mean deviation, standard deviation and quartile deviation are expressed in the unit of the data, so they cannot compare series in different units or with very different averages. Relative measures, the coefficients such as the coefficient of variation, are ratios or percentages and are unit-free, so they are used for comparing two or more distributions; but they are a little harder to compute.',
          [P('p1', 'Absolute measures are in the units of the data (range, MD, SD, QD)', 4, ALT('absolute {x}', x=('unit of', 'same unit', 'units of', 'in the unit', 'expressed in', 'measured in', 'original unit', 'depend on unit', 'dependent on unit', 'have unit', 'has unit', 'in rupees', 'unit'))),
           P('p2', 'Relative measures are unit-free ratios / coefficients', 4, ALT('relative {x}', x=('unit free', 'free of unit', 'free from unit', 'no unit', 'without unit', 'pure number', 'ratio', 'percentage', 'coefficient', 'independent of unit'))),
           P('p3', 'Relative measures are used to compare distributions', 2, 'compar')], 'c1'),
        V('v2', 'State the properties of standard deviation.',
          'If all observations are equal, the standard deviation is zero. It is not affected by a change of origin but is affected by a change of scale: if y equals a plus b x, the SD of y is the absolute value of b times the SD of x. And the SD of two groups can be combined using their sizes, means and SDs.',
          [P('p1', 'SD is zero when all values are equal', 3, 'zero|0', 'equal|same|constant|identical', min=2),
           P('p2', 'Unaffected by change of origin', 3, ALT('{n} {c} origin', n=('not affected by', 'unaffected by', 'independent of', 'does not change with', 'no effect of', 'not changed by', 'not affected due to', 'unaffected due to', 'does not depend on', 'remains same under'), c=('change of', 'a change of', 'shift of', 'the change of', '')), 'origin no effect|origin does not affect|change origin does not affect|change of origin does not change', min=1),
           P('p3', 'Affected by change of scale: s(y) = |b| s(x)', 2, ALT('{a} {c} scale', a=('affected by', 'changes with', 'depends on', 'affected due to', 'but by', 'only by', 'varies with'), c=('change of', 'a change of', 'the change of', '')), 'b times|mod b|absolute b|modulus of b|absolute value of b', min=1),
           P('p4', 'Combined SD of groups can be found', 2, 'combin|pooled|groups')], 'c4'),
        V('v3', 'What is the coefficient of variation and how is it used to compare consistency?',
          'The coefficient of variation is the standard deviation divided by the mean, multiplied by one hundred. It is a relative, unit-free measure. When comparing two series, the one with the lower coefficient of variation is more consistent or more stable, and the one with the higher CV is more variable.',
          [P('p1', 'CV = SD ÷ Mean × 100', 5, ALT('{s} {d} {m}', s=('sd', 'standard deviation', 'sigma'), d=('divided by', 'by', 'over', 'upon', 'to'), m=('mean', 'average', 'arithmetic mean', 'am', 'x bar'))),
           P('p2', 'Lower CV = more consistent / stable', 5, ALT('{l} {x} {c}', '{l} {x} more {c}', '{c} {l} {x}', l=('lower', 'lowest', 'less', 'least', 'smaller', 'low'), x=('cv', 'coefficient of variation', 'coefficient', ''), c=('consistent', 'stable', 'uniform', 'steady', 'consistency', 'less variable', 'less variation', 'reliable')))], 'c4'),
        V('v4', 'What is quartile deviation, and when is it the most suitable measure of dispersion?',
          'Quartile deviation, or the semi-interquartile range, is half the difference between the third and the first quartile, that is Q3 minus Q1 divided by two. Its coefficient is Q3 minus Q1 over Q3 plus Q1, times one hundred. It is the best measure for open-end classifications and is less affected by extreme values, because it ignores the lowest and highest quarters of the data.',
          [P('p1', 'QD = (Q3 − Q1)/2, semi-interquartile range', 4, ALT('q3 minus q1 {d} 2', 'q3 q1 {d} 2', 'half of q3 minus q1', 'half the difference', 'half of the difference', 'semi interquartile', 'semi inter quartile', 'half interquartile', 'half the interquartile', 'half of interquartile', d=('divided by', 'by', 'over', 'upon'))),
           P('p2', 'Best for open-end classes', 4, 'open'),
           P('p3', 'Less affected by extreme values', 2, 'extreme|outlier|not affected by extreme|not much affected by extreme|unaffected by extreme|extreme values do not|extremes do not|outliers do not|not affected by outlier|not influenced by extreme|not sensitive to extreme')], 'c5'),
        V('v5', 'What are the merits and demerits of range as a measure of dispersion?',
          'Range is the difference between the largest and smallest observations. It is very simple to understand and to calculate, and it is used in quality control and for stock price movements. But it depends only on the two extreme values, so it ignores all other observations, is greatly affected by extremes, and cannot be found for open-end classes. So it is not an ideal measure.',
          [P('p1', 'Range = largest − smallest', 3, 'largest|highest|maximum|biggest|greatest', 'smallest|lowest|minimum|least', min=2),
           P('p2', 'Merit: simple / easy to compute', 3, 'simple|easy|quick'),
           P('p3', 'Demerit: based only on two extreme values / ignores the rest', 4, 'only two|two extreme|only the extreme|two value|ignore|extreme value|not based on all|not all observation|affected by extreme', min=1)], 'c2'),
        V('v6', 'About which value is the mean deviation minimum, and how does it behave under change of origin and scale?',
          'Mean deviation is minimum when the deviations are taken about the median. Like other measures of dispersion, it does not change with a change of origin, but it changes in the same ratio as a change of scale: the mean deviation of y is the absolute value of b times that of x when y equals a plus b x.',
          [P('p1', 'Minimum about the median', 5, ALT('{m} {x} median', '{x} median {m}', 'median {m}', m=('minimum', 'least', 'smallest', 'lowest'), x=('about', 'from', 'around', 'when taken from', 'when taken about', 'taken from', 'taken about', 'measured from', 'measured about', 'with respect to'))),
           P('p2', 'Unaffected by change of origin', 3, ALT('{n} {c} origin', n=('not affected by', 'unaffected by', 'independent of', 'does not change with', 'not changed by', 'no effect of', 'does not depend on', 'remains same under', 'not change with'), c=('change of', 'a change of', 'shift of', 'the change of', '')), 'origin no effect|origin does not affect', min=1),
           P('p3', 'Changes in proportion to change of scale (|b| times)', 2, ALT('{a} {c} scale', a=('affected by', 'changes with', 'depends on', 'changes in the same ratio as', 'same ratio as', 'varies with', 'but by', 'only by', 'changes in proportion to'), c=('change of', 'a change of', 'the change of', '')), 'b times|mod b|absolute value of b|absolute b', min=1)], 'c3'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch14', 'n': 2,
        'title': 'Dispersion',
        'outcomes': [
            'Explain why averages need a measure of spread and distinguish absolute from relative measures of dispersion.',
            'Compute range, mean deviation, standard deviation, variance and quartile deviation, with their coefficients, for raw and grouped data.',
            'Use the coefficient of variation to compare consistency of two or more series.',
            'Apply the properties — effect of change of origin and scale, SD of a constant, combined SD, corrected SD, SD of the first n natural numbers and of two numbers.',
            'Choose the right measure (e.g. QD for open-end classes) and avoid the common traps.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 60}, 'prereq': ['fnd-p3-ch14-u01'],
                 'exam_tip': 'Dispersion MCQs are formula-driven and quick: change of origin/scale, CV comparisons, combined SD, SD of two numbers and of first n natural numbers. Remember ICAI expresses coefficients as percentages (× 100).'},
        'concepts': [
            {'id': 'c1', 'title': 'Why dispersion? Absolute vs relative measures',
             'body': ['Two series can have the same average and yet look nothing alike: 50, 50, 50 and 0, 50, 100 both average 50. Dispersion measures how far observations are scattered around their central value.',
                      'Absolute measures — range, mean deviation (MD), standard deviation (SD) and quartile deviation (QD) — are in the unit of the data. Relative measures — coefficient of range, coefficient of MD, coefficient of variation (CV) and coefficient of QD — are unit-free.',
                      'To compare two or more distributions (different units or very different averages) use relative measures. Relative measures are a little harder to compute and understand than absolute ones.'],
             'analogy': 'Average height tells you how tall a class is; dispersion tells you whether the class photo needs a step-stool row.',
             'work': 'Two branches with the same average debtor days but very different spreads need different credit controls. Investors look at volatility (SD of returns), not only average return.'},
            {'id': 'c2', 'title': 'Range and coefficient of range',
             'body': ['Range = L − S (largest − smallest). Coefficient of range = (L − S)/(L + S) × 100.',
                      'For grouped data, range = upper boundary of the last class − lower boundary of the first class; the coefficient uses the same two boundaries.',
                      'Range is unaffected by a change of origin but changes by |b| under a change of scale: if y = a + bx, R(y) = |b| × R(x).',
                      'Simple and quick (useful in quality control and price movements), but based only on two extreme values, so it is not an ideal measure.'],
             'analogy': 'Range is judging a road trip only by its highest and lowest altitude — ignoring everything in between.',
             'work': 'A stock\'s 52-week high–low range is printed in every market report; quality control charts use the range of small samples.'},
            {'id': 'c3', 'title': 'Mean deviation',
             'body': ['Mean deviation is the arithmetic mean of absolute deviations from a central value A (mean, median or mode): MD = Σ|x − A|/n; grouped: Σf|x − A|/N.',
                      'Coefficient of MD = MD about A ÷ A × 100.',
                      'MD is minimum when deviations are taken from the median. It is unaffected by a change of origin and changes in the same ratio as a change of scale: MD(y) = |b| × MD(x).',
                      'It uses all observations, but ignoring signs makes it awkward for further algebra.'],
             'blocks': [t2],
             'analogy': 'MD is the average distance each house in a lane is from the lane\'s centre — direction does not matter.',
             'work': 'Forecast accuracy is often reported as mean absolute deviation (MAD) of actual from budgeted sales.'},
            {'id': 'c4', 'title': 'Standard deviation, variance and coefficient of variation',
             'body': ['SD (σ or s) is the root-mean-square deviation from the AM: s = √(Σ(x − x̄)²/n) = √(Σx²/n − x̄²). Variance = s². Grouped: s = √(Σfd²/N − (Σfd/N)²) × C with d = (x − A)/C.',
                      'CV = s/x̄ × 100. The series with the lower CV is more consistent (stable, uniform); the higher CV is more variable.',
                      'Properties: (i) if all values are equal, SD = 0 (true also for range and MD); (ii) SD is unaffected by change of origin and affected by change of scale: if y = a + bx, s(y) = |b| s(x) and variance(y) = b² variance(x); (iii) combined SD of two groups: s = √[(n₁s₁² + n₂s₂² + n₁d₁² + n₂d₂²)/(n₁ + n₂)] with dᵢ = x̄ᵢ − x̄ (combined mean). Extends to k groups; if the means are equal, d terms vanish.',
                      'Useful results: SD of the first n natural numbers = √((n² − 1)/12); SD of two numbers a and b = |a − b|/2. A wrong observation is corrected by fixing Σx and Σx² and recomputing.',
                      'SD is the best measure of dispersion — rigidly defined, based on all values and suited to algebraic treatment — though more affected by extreme values than QD.'],
             'blocks': [t3],
             'analogy': 'SD is the "typical miss" of an archer around the bull\'s-eye; CV is that miss relative to the size of the target.',
             'work': 'Portfolio risk, process capability in cost audits and sampling precision in audit all rest on SD. CV is how you compare the stability of a ₹10 crore branch with a ₹500 crore one.'},
            {'id': 'c5', 'title': 'Quartile deviation and choosing a measure',
             'body': ['QD (semi-interquartile range) = (Q₃ − Q₁)/2. Coefficient of QD = (Q₃ − Q₁)/(Q₃ + Q₁) × 100.',
                      'QD is the best measure for open-end classes and is less affected by extreme values and sampling fluctuations, because it uses only the middle 50% of the data. Like the others, it is unaffected by change of origin and changes by |b| with change of scale.',
                      'Choice: SD for general use and further analysis; CV for comparing consistency; QD for open-end or highly skewed data; range for a quick look.'],
             'analogy': 'QD ignores the two noisiest quarters of a crowd and measures how spread the calm middle half is.',
             'work': 'Salary surveys report the interquartile band (Q₁–Q₃) because a few very high or very low pay packets would distort SD.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Range and quartile deviation', 'difficulty': 'core', 'minutes': 8,
             'q': '(a) Closing prices (₹) of a share for 7 days: ' + ', '.join(map(str, pr)) + '. Find the range and its coefficient. (b) For inclusive classes 10–19 to 50–59, find range and coefficient. (c) For the data ' + ', '.join(map(str, dq)) + ', find QD and its coefficient.',
             'solution': [wn('(a)', f'Range = {max(pr)} − {min(pr)} = ₹{fm(r1)}. Coefficient = {r1}/({max(pr)} + {min(pr)}) × 100 = {fm(cr1)}.'),
                          wn('(b)', f'Extreme boundaries 9.5 and 59.5: range = {fm(rg)}; coefficient = 50/69 × 100 = {fm(crg)}.'),
                          wn('(c)', f'n = 10. Q₁ = 2.75th value = 27 + 0.75 × 4 = {fm(q1v)}; Q₃ = 8.25th value = 52 + 0.25 × 6 = {fm(q3v)}. QD = (53.5 − 30)/2 = {fm(qd)}; coefficient = 23.5/83.5 × 100 = {fm(cqd)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Mean deviation about mean and about median', 'difficulty': 'core', 'minutes': 8,
             'q': 'For 5, 8, 10, 13, 20, 28 find the mean deviation about the mean and about the median, and their coefficients.',
             'solution': [wn('Centres', f'Mean = 84/6 = {fm(mean2)}; median = (10 + 13)/2 = {fm(med2)}.'), t2,
                          wn('Result', f'MD about mean = 40/6 = {fm(mdm)} (coefficient 47.62); MD about median = 38/6 = {fm(mdd)} (coefficient 55.07). MD about the median is smaller — as the minimum property says.')],
             'checks': c2},
            {'id': 'i3', 'title': 'SD and CV of a grouped distribution; comparing consistency', 'difficulty': 'moderate', 'minutes': 12,
             'q': '(a) Weekly sales of 50 outlets: 0–10: 4, 10–20: 10, 20–30: 16, 30–40: 12, 40–50: 8. Find mean, SD and CV. (b) Batsman A averages 48 runs with SD 12; batsman B averages 36 with SD 7.2. Who is more consistent?',
             'solution': [t3, wn('(a)', f'x̄ = 25 + ({sfd}/50) × 10 = {fm(m3)}. s = 10 × √({sfd2}/50 − ({sfd}/50)²) = 10 × √1.36 = {fm(sd3)}. CV = {fm(sd3)}/27 × 100 = {fm(cv3)}%.'),
                          wn('(b)', f'CV(A) = 12/48 × 100 = {fm(cva)}%; CV(B) = 7.2/36 × 100 = {fm(cvb)}%. B is more consistent (lower CV), although A scores more on average.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Combined SD, corrected SD and two handy results', 'difficulty': 'hard', 'minutes': 12,
             'q': '(a) Group 1: n = 40, mean 50, SD 6. Group 2: n = 60, mean 60, SD 8. Find the combined SD. (b) 20 observations have mean 40 and SD 5; one value 53 was wrongly recorded for 35. Correct the mean and SD. (c) SD of 1, 2, …, 10? (d) SD of 8 and 20?',
             'solution': [wn('(a)', f'Combined mean = {fm(cm4)}; d₁ = −6, d₂ = 4. s² = (40 × 36 + 60 × 64 + 40 × 36 + 60 × 16)/100 = 76.8; s = {fm(cs4)}.'),
                          wn('(b)', f'Σx = 800 → {inr(sx)}. Σx² = 20 × (25 + 1,600) = 32,500 → 32,500 − 2,809 + 1,225 = {inr(sx2)}. Mean = {fm(cmean)}; SD = √(30,916/20 − 39.1²) = √16.99 = {fm(csd)}.'),
                          wn('(c)', f'√((100 − 1)/12) = {fm(n10)}.'), wn('(d)', f'|8 − 20|/2 = {fm(two)}.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Comparing branch performance fairly', 'role': 'Internal auditor of a cooperative bank',
             'situation': 'Branch X (large) has average monthly deposits growth of ₹40 lakh with SD ₹12 lakh; branch Y (small) ₹8 lakh with SD ₹4 lakh. The board asks which is "more erratic".',
             'steps': ['SDs are in the same unit but the branches differ hugely in size, so compare CVs, not SDs.',
                       'CV(X) = 12/40 × 100 = 30%; CV(Y) = 4/8 × 100 = 50%.',
                       'Branch Y is more erratic relative to its size, though its SD is smaller.',
                       'Investigate Y\'s volatility — concentration on a few large depositors is a typical cause.'],
             'takeaway': 'Absolute spread can mislead when scales differ; CV makes the comparison fair.',
             'checks': [{'expr': '12/40*100', 'value': 30, 'label': 'CV X'}, {'expr': '4/8*100', 'value': 50, 'label': 'CV Y'}]},
            {'id': 'j2', 'title': 'Fixing a statistic after a data-entry error', 'role': 'Analyst in a corporate FP&A team',
             'situation': 'A dashboard shows mean and SD of 250 daily dispatch quantities. You find one day keyed as 9,800 instead of 980.',
             'steps': ['Do not recompute from scratch if raw data are not handy — use Σx = n x̄ and Σx² = n(s² + x̄²).',
                       'Subtract the wrong value (and its square), add the right one, then recompute mean and SD.',
                       'Document the correction and the source document, as the auditor will ask for it.'],
             'takeaway': 'Means and SDs can be corrected from totals alone — keep Σx and Σx² in your working papers.'},
        ],
        'mcqs': [
            mq('m1', 'Which of these is a relative measure of dispersion?', ['Coefficient of variation', 'Standard deviation', 'Mean deviation', 'Range'],
               'The coefficient of variation (SD ÷ mean × 100) is a ratio, free of units, so it is a relative measure. Standard deviation is the trap: it is expressed in the same units as the data, so it is an absolute measure, as are mean deviation and range. In practice: analysts use CV to compare the risk of stocks with very different price levels.', 'c1', topic='Why dispersion? Absolute vs relative measures'),
            mq('m2', 'To compare the variability of heights (cm) and weights (kg) of the same students, use:', ['Coefficient of variation', 'Standard deviation', 'Range', 'Variance'],
               'Heights in cm and weights in kg cannot be compared with absolute measures because their units differ. The coefficient of variation is unit-free, so it allows a fair comparison. Standard deviation is the trap: an SD in cm cannot be compared with an SD in kg. In practice: comparing the volatility of sales in units with costs in rupees also needs a relative measure like CV.', 'c1', topic='Why dispersion? Absolute vs relative measures'),
            nq('m3', 'The largest and smallest values of a series are 84 and 36. The coefficient of range is:', 'round((84-36)/(84+36)*100,2)', [48, 57.14, 133.33],
               "Coefficient of range = (L − S) ÷ (L + S) × 100 = (84 − 36) ÷ (84 + 36) × 100 = 48 ÷ 120 × 100 = 40. The trap is 48, which is the range itself, an absolute measure. In practice: the coefficient of range gives a quick relative sense of price fluctuation, for example in a stock's 52-week high and low.", 'c2', topic='Range and coefficient of range'),
            nq('m4', 'For classes 20–29, 30–39, …, 60–69, the range is:', '69.5-19.5', [49, 40, 45],
               'For grouped data, range uses the extreme class boundaries: upper boundary of the last class minus lower boundary of the first = 69.5 − 19.5 = 50. The trap is 49, which uses class limits (69 − 20) instead of boundaries. In practice: when only grouped data are available, such as age bands in an HR report, boundaries give the correct spread.', 'c2', 'moderate', topic='Range and coefficient of range'),
            nq('m5', 'If the range of x is 15 and 3x + 5y = 12, the range of y is:', '3/5*15', [-9, 15, 25],
               'From 3x + 5y = 12, y = 2.4 − 0.6x. Range changes by the absolute value of the coefficient: R(y) = |−0.6| × 15 = 9. The trap is −9: a range can never be negative. In practice: converting a range of prices into another currency at a fixed rate scales the range by that rate.', 'c2', 'moderate', topic='Range and coefficient of range'),
            mq('m6', 'Mean deviation is minimum when deviations are taken from the:', ['Median', 'Mean', 'Mode', 'Largest value'],
               'The sum of absolute deviations is least when measured from the median, so mean deviation is smallest about the median. The mean is the trap: the mean minimises squared deviations, not absolute ones. In practice: forecasting teams who want to minimise average absolute error often use the median as their central estimate.', 'c3', topic='Mean deviation'),
            nq('m7', 'The mean deviation about the mean of 2, 4, 6, 8, 10 is:', '(4+2+0+2+4)/5', [3, 2.83, 6],
               'Mean = 30 ÷ 5 = 6. Absolute deviations: 4, 2, 0, 2, 4, total 12. MD = 12 ÷ 5 = 2.4. The trap is 2.83, which is the standard deviation (√8), not the mean deviation. In practice: mean absolute deviation is used in demand forecasting to measure average forecast error in units.', 'c3', topic='Mean deviation'),
            nq('m8', 'The mean deviation about the median is 6 and the median is 40. The coefficient of mean deviation is:', '6/40*100', [6.67, 0.15, 24],
               'Coefficient of mean deviation = (MD ÷ the average it is measured from) × 100 = 6 ÷ 40 × 100 = 15. The trap is 0.15, which forgets to multiply by 100. In practice: relative measures like this let an analyst compare variability in two branches of different size.', 'c3', topic='Mean deviation'),
            nq('m9', 'For 10 observations, Σx = 120 and Σx² = 1,600. The standard deviation is:', '(1600/10-12**2)**0.5', [16, 12, 1.6],
               'Mean = 120 ÷ 10 = 12. Variance = Σx²/n − mean² = 160 − 144 = 16. SD = √16 = 4. The trap is 16, which is the variance, not the SD. In practice: this shortcut formula is how spreadsheet functions and calculators compute the standard deviation of returns or costs from running totals.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            nq('m10', 'If every value of a series is 7, the standard deviation is:', '0', [7, 1, 49],
               'If every value is 7, the mean is 7 and no value deviates from it, so every deviation is zero and the SD is 0. The trap is 7, which confuses the value itself with its spread. In practice: a fixed-deposit return that never changes has zero volatility, which is why such instruments are called risk-free in finance models.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            nq('m11', 'The SD of x is 4. If y = 5 − 3x, the SD of y is:', 'abs(-3)*4', [-12, 7, 17],
               'For y = a + bx, SD(y) = |b| × SD(x) = 3 × 4 = 12. The constant 5 shifts values but does not change spread. The trap is −12: a standard deviation can never be negative. In practice: if a cost depends linearly on volume, the volatility of cost is the volatility of volume times the per-unit rate.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            nq('m12', 'The variance of x is 9. The variance of 2x + 7 is:', '2**2*9', [18, 25, 43],
               "Var(a + bx) = b² × Var(x) = 2² × 9 = 36. Adding 7 has no effect on spread. The trap is 18, which multiplies by 2 instead of 2². In practice: doubling a portfolio's exposure quadruples its variance, which is why leverage magnifies risk so sharply.", 'c4', 'moderate', topic='Standard deviation, variance and coefficient of variation'),
            nq('m13', 'The mean of x is 20 and its CV is 25%. The variance of 10 − 3x is:', '9*(20*25/100)**2', [15, 75, 135],
               'CV = SD ÷ mean × 100, so SD(x) = 25% of 20 = 5. Var(10 − 3x) = (−3)² × 5² = 9 × 25 = 225. The trap is 15, which is the SD of 10 − 3x (3 × 5), not the variance. In practice: risk analysts move between CV, SD and variance routinely when modelling linear transformations of returns.', 'c4', 'hard', topic='Standard deviation, variance and coefficient of variation'),
            nq('m14', 'A series has mean 60 and SD 9. Its coefficient of variation is:', '9/60*100', [6.67, 0.15, 51],
               'CV = SD ÷ mean × 100 = 9 ÷ 60 × 100 = 15%. The trap is 6.67, which divides the mean by the SD the wrong way round. In practice: CV is quoted for comparing the consistency of returns of mutual funds or the stability of sales across branches.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            mq('m15', 'Series A: mean 50, SD 10. Series B: mean 80, SD 12. Which is more consistent?', ['B, because its CV (15%) is lower than A\'s (20%)', 'A, because its SD is lower', 'B, because its mean is higher', 'Both are equally consistent'],
               "Consistency is judged by the relative measure, the CV. A: 10 ÷ 50 × 100 = 20%. B: 12 ÷ 80 × 100 = 15%. B has the lower CV, so it is more consistent. 'A, because its SD is lower' is the trap: SDs cannot be compared when means differ. In practice: fund advisers compare risk per unit of return, not raw SDs, when recommending a scheme.", 'c4', 'moderate', topic='Standard deviation, variance and coefficient of variation'),
            nq('m16', 'Two groups of 50 and 50 have means 30 and 40 and SDs 4 and 6. The combined SD is:', 'round(((50*16+50*36+50*25+50*25)/100)**0.5,2)', [5, 5.1, 7.07],
               "Combined mean = 35, so d₁ = −5 and d₂ = +5. Combined variance = [50(16 + 25) + 50(36 + 25)] ÷ 100 = 51, and SD = √51 ≈ 7.14. The trap is 5.1 (√26), which ignores the difference between the group means. In practice: combining two branches' sales data needs this formula, since the gap between branch means adds to overall variability.", 'c4', 'hard', topic='Standard deviation, variance and coefficient of variation'),
            nq('m17', 'The standard deviation of the first 12 natural numbers is:', 'round(((12**2-1)/12)**0.5,2)', [3.61, 11.92, 6.5],
               'For the first n natural numbers, SD = √((n² − 1) ÷ 12) = √(143 ÷ 12) ≈ 3.45. The trap is 11.92, which is the variance, not the SD. In practice: shortcut formulas like this serve as a quick check on spreadsheet calculations of evenly spaced data, such as serial numbers.', 'c4', 'moderate', topic='Standard deviation, variance and coefficient of variation'),
            nq('m18', 'The standard deviation of the two numbers 15 and 27 is:', 'abs(15-27)/2', [12, 21, 8.49],
               "For two numbers, SD = |a − b| ÷ 2 = |15 − 27| ÷ 2 = 6. Check: mean 21, both deviations 6, variance 36. The trap is 12, which is the range, not the SD. In practice: such quick checks help when reviewing a two-period comparison, for example two years' profit figures.", 'c4', topic='Standard deviation, variance and coefficient of variation'),
            nq('m19', 'The mean of 5 observations is 8 and the mean of their squares is 73. The SD is:', '(73-8**2)**0.5', [9, 8.54, 65],
               'Variance = mean of squares − square of mean = 73 − 8² = 73 − 64 = 9, so SD = √9 = 3. The trap is 9, which is the variance. In practice: this formula is how calculators and software compute SD from summary totals without storing every observation.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            mq('m20', 'If each observation is increased by 10, the standard deviation:', ['Remains unchanged', 'Increases by 10', 'Is multiplied by 10', 'Decreases by 10'],
               "Adding 10 to every value shifts the whole set but does not change how spread out it is, so the SD stays the same (change of origin). 'Increases by 10' is the trap: only the mean rises by 10. In practice: adding a flat bonus to every employee's salary raises the average but leaves the salary spread unchanged.", 'c4', topic='Standard deviation, variance and coefficient of variation'),
            mq('m21', 'If each observation is doubled, the variance becomes:', ['Four times', 'Double', 'Half', 'Unchanged'],
               "Doubling every value doubles the SD, and variance is SD squared, so it becomes 2² = 4 times. 'Double' is the trap: that is what happens to the SD, not the variance. In practice: doubling the size of a position in a stock multiplies its variance by four, which matters for risk limits in treasury departments.", 'c4', 'moderate', topic='Standard deviation, variance and coefficient of variation'),
            mq('m22', 'Which measure of dispersion is generally regarded as the best?', ['Standard deviation', 'Range', 'Quartile deviation', 'Mean deviation'],
               'Standard deviation is regarded as the best measure because it is rigidly defined, based on all observations and suitable for further algebraic work. Range is the trap: it uses only the two extreme values. In practice: SD (volatility) is the standard risk measure in finance, used in portfolio theory and risk-o-meters of mutual funds.', 'c4', topic='Standard deviation, variance and coefficient of variation'),
            nq('m23', 'Q₁ = 32 and Q₃ = 58. The quartile deviation is:', '(58-32)/2', [26, 45, 29],
               'Quartile deviation = (Q₃ − Q₁) ÷ 2 = (58 − 32) ÷ 2 = 13. The trap is 26, which is the inter-quartile range, not half of it. In practice: QD is used for skewed data such as incomes or property prices, where extreme values would distort the SD.', 'c5', topic='Quartile deviation and choosing a measure'),
            nq('m24', 'Q₁ = 32 and Q₃ = 58. The coefficient of quartile deviation is:', 'round((58-32)/(58+32)*100,2)', [44.83, 13, 22.41],
               'Coefficient of QD = (Q₃ − Q₁) ÷ (Q₃ + Q₁) × 100 = 26 ÷ 90 × 100 ≈ 28.89. The trap is 44.83, which wrongly divides 26 by Q₃ (58) instead of Q₃ + Q₁. In practice: relative quartile measures help compare spreads of salary structures across companies of different sizes.', 'c5', topic='Quartile deviation and choosing a measure'),
            nq('m25', 'The QD of x is 8 and 2x + 4y = 15. The QD of y is:', '2/4*8', [16, -4, 8],
               'From 2x + 4y = 15, y = 3.75 − 0.5x. QD changes by the absolute value of the coefficient: QD(y) = 0.5 × 8 = 4. The trap is 16, which multiplies by 2 instead of 0.5. In practice: converting a quartile spread of prices into another unit or currency scales it by the conversion factor.', 'c5', 'moderate', topic='Quartile deviation and choosing a measure'),
            mq('m26', 'For a distribution with open-end classes, the most suitable measure of dispersion is:', ['Quartile deviation', 'Standard deviation', 'Range', 'Mean deviation about mean'],
               "QD needs only Q₁ and Q₃, so open-ended classes at either end do not matter. Standard deviation is the trap: it needs a mid-value for every class, which open classes lack. In practice: income-tax statistics with a top slab like 'above ₹1 crore' are better summarised with quartile measures.", 'c5', topic='Quartile deviation and choosing a measure'),
            mq('m27', 'Which measure of dispersion is most affected by extreme values?', ['Range', 'Quartile deviation', 'Mean deviation about median', 'Coefficient of QD'],
               "Range depends only on the largest and smallest values, so a single extreme value changes it completely. Quartile deviation is the trap: it ignores the top and bottom 25% of values and is barely affected by extremes. In practice: a stock's 52-week range can widen sharply because of one day's spike, so analysts also look at other volatility measures.", 'c2', topic='Range and coefficient of range'),
            mq('m28', 'All measures of dispersion (range, MD, SD, QD) are:', ['Unaffected by change of origin but affected by change of scale', 'Affected by change of origin only', 'Unaffected by both changes', 'Affected by change of origin and unaffected by scale'],
               "Shifting every value by a constant (change of origin) does not change spread, but multiplying by b (change of scale) changes every measure of dispersion by |b|. 'Unaffected by both' is the trap: scale changes always alter spread. In practice: converting rupee data into lakh changes the SD by the same factor, while adding a fixed fee does not change it.", 'c1', 'moderate', topic='Why dispersion? Absolute vs relative measures'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Daily output of 50 machines: 100–120: 6, 120–140: 14, 140–160: 20, 160–180: 10. Compute the mean, standard deviation and coefficient of variation.',
             'model': [tq1, wn('Mean', f'A = 150, C = 20, Σfd = {qfd}: x̄ = 150 + ({qfd}/50) × 20 = {fm(qm)}.'),
                       wn('SD', f's = 20 × √({qfd2}/50 − ({qfd}/50)²) = 20 × √({fm(qfd2/50)} − {qfd*qfd/2500:.4f}) = {fm(qs)}.'),
                       wn('CV', f'CV = {fm(qs)}/{fm(qm)} × 100 = {fm(qcv)}%.')],
             'scheme': [{'id': 's1', 'pt': 'd, fd, fd² columns and totals', 'm': 2, 'skill': 'computation'},
                        {'id': 's2', 'pt': f'Mean {fm(qm)}', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': f'SD {fm(qs)} (× C not forgotten)', 'm': 2, 'skill': 'computation'},
                        {'id': 's4', 'pt': f'CV {fm(qcv)}%', 'm': 1, 'skill': 'computation'}],
             'remarks': ['The most common slip is forgetting to multiply by the class width C.', 'Some candidates divide Σfd² by N but forget to subtract (Σfd/N)².'],
             'mistakes': ['Σfd² computed as (Σfd)².', 'CV computed as mean/SD.'],
             'tips': ['Keep d small (−2, −1, 0, 1) to avoid arithmetic errors.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
             'q': 'Factory A employs 50 workers with mean monthly bonus ₹4,500 and SD ₹300. Factory B employs 70 workers with mean ₹5,100 and SD ₹400. Find the combined mean and combined SD.',
             'model': [wn('Combined mean', f'(50 × 4,500 + 70 × 5,100)/120 = ₹{inr(q2m)}.'),
                       wn('Deviations', 'd₁ = 4,500 − 4,850 = −350; d₂ = 5,100 − 4,850 = 250.'),
                       wn('Combined SD', f's = √[(50 × 300² + 70 × 400² + 50 × 350² + 70 × 250²)/120] = √[(45,00,000 + 1,12,00,000 + 61,25,000 + 43,75,000)/120] = ₹{fm(q2s)}.')],
             'scheme': [{'id': 's1', 'pt': 'Combined mean ₹4,850', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'd₁ and d₂ found', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Correct combined SD formula', 'm': 1, 'skill': 'concept'},
                        {'id': 's4', 'pt': f'Combined SD ₹{fm(q2s)}', 'm': 2, 'skill': 'computation'}],
             'remarks': ['Leaving out the n·d² terms understates the combined SD.'],
             'mistakes': ['Averaging the two SDs.', 'Using SD instead of variance inside the formula.'],
             'tips': ['Write the formula first; examiners give a step mark for it.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'For the ordered data ' + ', '.join(map(str, d3x)) + ': (a) find the quartile deviation and its coefficient; (b) find the mean deviation about the median and its coefficient.',
             'model': [wn('(a)', f'n = 9. Q₁ = 2.5th value = 19 + 0.5 × 4 = {fm(qq1)}; Q₃ = 7.5th value = 37 + 0.5 × 8 = {fm(qq3)}. QD = (41 − 21)/2 = {fm(qqd)}; coefficient = 20/62 × 100 = {fm(qcq)}.'),
                       wn('(b)', f'Median = 5th value = {fm(q3med)}. Σ|x − 30| = 16 + 11 + 7 + 4 + 0 + 4 + 7 + 15 + 21 = {smd}. MD = {smd}/9 = {fm(q3md)}; coefficient = {fm(q3md)}/30 × 100 = {fm(smd / 9 / 30 * 100)}.')],
             'scheme': [{'id': 's1', 'pt': 'Q₁ and Q₃ by (n + 1) rule', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'QD and coefficient', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Median and Σ|x − Me|', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'MD and coefficient', 'm': 1, 'skill': 'computation'}],
             'remarks': ['Many write the interquartile range (20) as QD.'],
             'mistakes': ['Forgetting to halve Q₃ − Q₁.', 'Keeping signs when summing deviations.'],
             'tips': ['Show the positions (2.5th, 7.5th) before the values.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Absolute (range, MD, SD, QD) vs relative (coefficients, CV) measures.',
                        'Range = L − S; coefficient (L − S)/(L + S) × 100.',
                        'MD = Σ|x − A|/n; minimum about the median.',
                        'SD = √(Σx²/n − x̄²); CV = s/x̄ × 100; lower CV = more consistent.',
                        'QD = (Q₃ − Q₁)/2; best for open-end classes.',
                        'All are unaffected by change of origin and multiplied by |b| under change of scale.'],
            'remember': ['SD of first n natural numbers = √((n² − 1)/12).', 'SD of two numbers = |a − b|/2.', 'Var(a + bx) = b² Var(x).', 'Combined SD needs n·d² terms.'],
            'traps': ['Dispersion measures are never negative — take |b|.', 'Grouped range uses boundaries, not limits.', 'A higher mean does not mean more consistent — compare CVs.', 'Interquartile range is Q₃ − Q₁; QD is half of it.']},
        'quickref': [
            {'k': 'Range / coefficient', 'v': 'L − S; (L − S)/(L + S) × 100'},
            {'k': 'Mean deviation', 'v': 'Σf|x − A|/N; coefficient = MD/A × 100'},
            {'k': 'Standard deviation', 'v': '√(Σx²/n − x̄²); grouped √(Σfd²/N − (Σfd/N)²) × C'},
            {'k': 'Coefficient of variation', 'v': 'CV = s/x̄ × 100'},
            {'k': 'Combined SD', 'v': '√[(n₁s₁² + n₂s₂² + n₁d₁² + n₂d₂²)/(n₁ + n₂)], dᵢ = x̄ᵢ − x̄'},
            {'k': 'Quartile deviation', 'v': '(Q₃ − Q₁)/2; coefficient (Q₃ − Q₁)/(Q₃ + Q₁) × 100'},
            {'k': 'Change of origin & scale', 'v': 'y = a + bx ⇒ R, MD, SD, QD of y = |b| × those of x; Var(y) = b² Var(x)'},
            {'k': 'Special results', 'v': 'SD(1..n) = √((n² − 1)/12); SD(a, b) = |a − b|/2'},
        ],
        'viva': viva, 'cases': cases,
    }
