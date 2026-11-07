"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 14 Unit 1 Measures of Central Tendency.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below."""
from math import prod, log10
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as CM

UID = 'fnd-p3-ch14-u01'


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


def mq(mid, q, opts, explain, concept, diff='core'):
    return {'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit=''):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def grouped(lo, w, f):
    """mean (step deviation), median, mode, quartiles for equal-width classes starting at lo."""
    k = len(f); N = sum(f)
    mids = [lo + w * i + w / 2 for i in range(k)]
    cf = []; c = 0
    for x in f: c += x; cf.append(c)
    mean = sum(m * x for m, x in zip(mids, f)) / N

    def part(pp):
        t = N * pp
        i = next(j for j in range(k) if cf[j] >= t)
        nl = cf[i - 1] if i else 0
        return lo + w * i + (t - nl) / f[i] * w, i, nl
    i0 = max(range(k), key=lambda j: f[j])
    fm1 = f[i0 - 1] if i0 else 0; fp1 = f[i0 + 1] if i0 + 1 < k else 0
    mode = lo + w * i0 + (f[i0] - fm1) / (2 * f[i0] - fm1 - fp1) * w
    return dict(N=N, mids=mids, cf=cf, mean=mean, med=part(0.5), q1=part(0.25), q3=part(0.75), mode=mode, i0=i0, fm1=fm1, fp1=fp1)


def build():
    # ---------------- Illustration 1: mean, median, mode of daily wages ----------------
    c1 = Checks()
    lo, w, f1 = 200, 50, [6, 14, 25, 30, 15, 10]
    g = grouped(lo, w, f1)
    A = 375
    d = [int((m - A) / w) for m in g['mids']]
    sfd = sum(a * b for a, b in zip(d, f1))
    rows1 = [[f'{lo + w * i}–{lo + w * (i + 1)}', str(f1[i]), fm(g['mids'][i]), str(d[i]), str(d[i] * f1[i]), str(g['cf'][i])] for i in range(6)]
    rows1.append(['Total', str(g['N']), '', '', str(sfd), ''])
    t1 = table(['Wages (₹)', 'Workers (f)', 'Mid-value x', 'd = (x − 375)/50', 'fd', 'Less-than c.f.'], rows1, num=[1, 4], total=True, title='Daily wages of 100 workers')
    mean1 = c1.add(f'375+({sfd})/100*50', 'mean by step-deviation method')
    assert abs(mean1 - g['mean']) < 1e-9
    med1 = c1.add('350+(50-45)/30*50', 'median: l1 + (N/2 - Nl)/(Nu - Nl) x C')
    mode1 = c1.add('350+(30-25)/(2*30-25-15)*50', 'mode: l1 + (f0 - f-1)/(2f0 - f-1 - f1) x C')
    assert abs(med1 - g['med'][0]) < 0.01 and abs(mode1 - g['mode']) < 1e-9
    c1.add('3*358.33-2*357', 'empirical mode check (approximate)')

    # ---------------- Illustration 2: partition values ----------------
    c2 = Checks()
    data2 = sorted([42, 35, 58, 61, 47, 39, 53, 66, 44, 50, 71])
    assert len(data2) == 11
    q1u = c2.add(f'{data2[2]}', 'Q1 = (n+1)/4 = 3rd value')
    q3u = c2.add(f'{data2[8]}', 'Q3 = 3(n+1)/4 = 9th value')
    d7 = c2.add(f'{data2[7]}+0.4*({data2[8]}-{data2[7]})', 'D7 = 7(n+1)/10 = 8.4th value')
    p30 = c2.add(f'{data2[2]}+0.6*({data2[3]}-{data2[2]})', 'P30 = 30(n+1)/100 = 3.6th value')
    gq1 = c2.add('300+(25-20)/25*50', 'grouped Q1 for the wage data')
    gq3 = c2.add('350+(75-45)/30*50', 'grouped Q3 for the wage data')
    assert abs(gq1 - g['q1'][0]) < 1e-9 and abs(gq3 - g['q3'][0]) < 1e-9

    # ---------------- Illustration 3: AM properties ----------------
    c3 = Checks()
    cm = c3.add('(40*21000+60*26000)/100', 'combined mean salary')
    corr = c3.add('(50*64-82+28)/50', 'corrected mean after replacing 82 by 28')
    ym = c3.add('(30-2*18)/5', 'mean of y when 2x + 5y = 30 and mean of x = 18')
    n3 = c3.add('(25*48-20*45)/5', 'mean of the remaining five numbers')

    # ---------------- Illustration 4: GM, HM ----------------
    c4 = Checks()
    gm4 = c4.add('round((1.10*1.20*1.32)**(1/3),4)', 'GM of growth factors')
    c4.add('round(((1.10*1.20*1.32)**(1/3)-1)*100,2)', 'average annual growth %')
    c4.add('round((10+20+32)/3,2)', 'simple AM of growth rates (wrong method)')
    c4.add('1000*1.10*1.20*1.32', 'value after three years')
    hm4 = c4.add('2/(1/60+1/40)', 'average speed over equal distances = HM')
    c4.add('(60*3+40*2)/5', 'average speed over equal times = AM (3 h and 2 h)')
    am2, gm2, hm2 = c4.add('(4+9)/2', 'AM of 4 and 9'), c4.add('(4*9)**0.5', 'GM of 4 and 9'), c4.add('round(2*4*9/(4+9),2)', 'HM of 4 and 9')
    c4.add('6.5*72/13', 'AM x HM = GM^2 for two numbers')
    wam = c4.add('(78*3+64*2+85*4+70*1)/(3+2+4+1)', 'weighted mean marks')

    # ---------------- Question 1: grouped marks ----------------
    q1c = Checks()
    fq = [5, 8, 15, 22, 12, 8]
    g1 = grouped(0, 10, fq)
    sd1 = [-3, -2, -1, 0, 1, 2]
    sfd1 = sum(a * b for a, b in zip(sd1, fq))
    rq1 = [[f'{10 * i}–{10 * i + 10}', str(fq[i]), fm(g1['mids'][i]), str(sd1[i]), str(sd1[i] * fq[i]), str(g1['cf'][i])] for i in range(6)]
    rq1.append(['Total', str(g1['N']), '', '', str(sfd1), ''])
    tq1 = table(['Marks', 'f', 'Mid-value', 'd = (x − 35)/10', 'fd', 'c.f.'], rq1, num=[1, 4], total=True)
    qm = q1c.add(f'round(35+({sfd1})/70*10,2)', 'mean')
    qmed = q1c.add('round(30+(35-28)/22*10,2)', 'median')
    qmo = q1c.add('round(30+(22-15)/(44-15-12)*10,2)', 'mode')
    assert abs(qm - round(g1['mean'], 2)) < 0.01 and abs(qmed - round(g1['med'][0], 2)) < 0.01 and abs(qmo - round(g1['mode'], 2)) < 0.01

    # ---------------- Question 2: missing frequency from median ----------------
    q2c = Checks()
    x2 = q2c.add('40/2', 'missing frequency: 27 = 20 + ((40+x)/2 - 16)/x x 10 gives 2x = 40')
    q2c.add('20+((40+20)/2-16)/20*10', 'median check with x = 20')

    # ---------------- Question 3: combined/ corrected / two numbers ----------------
    q3c = Checks()
    q3a = q3c.add('(30*52+45*60+25*48)/100', 'combined mean of three groups')
    q3g = q3c.add('(25*16)**0.5', 'GM from AM x HM = GM^2')
    q3c.add('(50+(50**2-4*400)**0.5)/2', 'larger number'); q3c.add('(50-(50**2-4*400)**0.5)/2', 'smaller number')

    # ---------------- Case ----------------
    kc = Checks()
    kcm = kc.add('(12*38000+30*24000+18*29000)/60', 'combined mean salary')
    kc.add('round(((1.08*1.15*1.25)**(1/3)-1)*100,2)', 'average growth')
    cases = [{
        'id': 'k1', 'title': 'Salary analysis for an HR policy note', 'difficulty': 'hard',
        'case': ('Tanvi, a CA in a mid-sized firm, is asked to report "average" salaries. The firm has three departments: Audit (12 staff, mean ₹38,000), Tax (30 staff, mean ₹24,000) and Advisory (18 staff, mean ₹29,000). '
                 'The salary register is grouped with an open last class "₹60,000 and above". Revenue grew by 8%, 15% and 25% in the last three years. One partner wants the "most common" salary band highlighted.'),
        'mcqs': [
            CM('k1a', 'What is the combined mean salary of the 60 staff?', [R(kcm), '₹30,333', '₹29,000', '₹27,600'], 0,
               f'Combined mean = (12 × 38,000 + 30 × 24,000 + 18 × 29,000) ÷ 60 = ₹{inr(kcm)}. ₹30,333 is the simple average of the three means — wrong, because group sizes differ.', 'moderate', '(12*38000+30*24000+18*29000)/60'),
            CM('k1b', 'With an open-ended last class, which average can be computed from the grouped register without assuming a mid-value?', ['Median', 'Arithmetic mean', 'Geometric mean', 'Harmonic mean'], 0,
               'The median needs only cumulative frequencies up to the middle; AM, GM and HM need every class mid-value, which the open class lacks.', 'moderate'),
            CM('k1c', 'The average annual revenue growth over the three years is closest to:', ['15.79%', '16%', '55.25%', '15%'], 0,
               'Growth compounds, so use the GM of growth factors: (1.08 × 1.15 × 1.25)^(1/3) − 1 = 1.5525^(1/3) − 1 ≈ 15.79%. The AM of 8, 15 and 25 (16%) overstates it; 55.25% is the total growth over three years.', 'hard', 'round(((1.08*1.15*1.25)**(1/3)-1)*100,2)'),
            CM('k1d', 'The "most common salary band" requested by the partner is the:', ['Modal class', 'Median class', 'Class containing the mean', 'Last class'], 0,
               'Mode is the value (or class) with the highest frequency — the most common one.', 'core'),
        ]}]

    viva = [
        V('v1', 'What are the requisites of an ideal measure of central tendency?',
          'An ideal average should be rigidly and clearly defined, easy to understand and simple to calculate. It should be based on all the observations, it should be capable of further mathematical treatment, and it should be least affected by extreme observations and by fluctuations of sampling.',
          [P('p1', 'Rigidly / clearly defined', 2, 'rigid|clear|unambiguous|properly defined|well defined|defined'),
           P('p2', 'Easy to understand and simple to compute', 2, 'easy|simple|understand|comprehend|calculat|comput', min=1),
           P('p3', 'Based on all observations', 2, 'all observation|all the observation|all value|every observation|all item|every item|all data|whole data'),
           P('p4', 'Amenable to mathematical treatment', 2, 'mathematical|algebraic|further treatment|further analysis'),
           P('p5', 'Least affected by extreme values / sampling fluctuations', 2, 'extreme|outlier|sampling fluctuation|fluctuation|stable|not affected by extreme|not much affected by extreme|unaffected by extreme|extreme values do not|extremes do not|outliers do not|not affected by outlier|not influenced by extreme|not sensitive to extreme')], 'c1'),
        V('v2', 'State the important properties of the arithmetic mean.',
          'If all observations equal a constant, the mean is that constant. The algebraic sum of deviations of the observations from their mean is zero. The mean is affected by change of origin and scale: if y equals a plus b x, the mean of y is a plus b times the mean of x. And two groups can be combined: the combined mean is n1 x1 bar plus n2 x2 bar divided by n1 plus n2.',
          [P('p1', 'Sum of deviations from the mean is zero', 4, ALT('{s} {d}', s=('sum', 'total', 'algebraic sum'), d=('deviation zero', 'deviations from mean zero', 'deviation from the mean is zero', 'deviation from mean zero', 'deviation from mean is zero', 'deviation from the mean zero', 'deviation from arithmetic mean zero', 'deviation from am zero', 'deviation from its mean is zero', 'deviation is zero'))),
           P('p2', 'Affected by change of origin and scale: ȳ = a + b x̄', 3, 'origin|scale|a plus b|a b x|y a bx|a bx', min=1),
           P('p3', 'Combined mean formula (n1x̄1 + n2x̄2)/(n1 + n2)', 3, 'combin|pooled|two group|groups')], 'c2'),
        V('v3', 'Why is the median preferred for open-ended distributions, and what is its minimum property?',
          'The median is a positional average; it needs only the cumulative frequencies up to the middle, so open-end classes do not matter, and it is not affected by extreme values. Its special property is that the total of the absolute deviations is least when they are measured from the median.',
          [P('p1', 'Positional — needs only middle position / cumulative frequencies; open classes do not matter', 4, 'position|middle|cumulative|open|mid value not needed|no mid', min=1),
           P('p2', 'Not affected by extreme values', 2, 'not affected by extreme|unaffected by extreme|extreme value do not|extreme values does not|extremes do not|not influenced by extreme|not disturbed by extreme|resistant to extreme|robust|insensitive to extreme|not sensitive to extreme|outlier do not|outliers does not|not affected by outlier|unaffected by outlier|no effect of extreme|not much affected by extreme|less affected by extreme|least affected by extreme'),
           P('p3', 'Sum of absolute deviations is minimum about the median', 4, 'absolute', 'minimum|least|smallest|lowest|minimal', min=2)], 'c3'),
        V('v4', 'State the empirical relationship between mean, median and mode.',
          'For a moderately skewed distribution, mean minus mode is approximately three times mean minus median. So mode is approximately three times the median minus two times the mean.',
          [P('p1', 'Mean − Mode = 3 (Mean − Median)', 5, ALT('mean minus mode {e} 3', 'mean mode {e} 3', e=('equal', 'equals', 'is', 'approximately', 'approximately equal', 'is approximately', '')), 'mode 3 median minus 2 mean|mode 3 median 2 mean|mode equal 3 median minus 2 mean|mode is 3 median minus 2 mean|3 times median minus 2 times mean|3 median minus twice mean|mode equal 3 times median minus 2 times mean|mode is 3 times the median minus 2 times the mean', min=1),
           P('p2', 'Mode = 3 Median − 2 Mean', 3, '3 median minus 2 mean|3 median 2 mean|3 times median minus 2 times mean|three times the median minus two times the mean|3 times the median minus 2 times the mean|3 median minus twice mean|mean minus mode|3 times mean minus median|three times mean minus median'),
           P('p3', 'Holds for moderately skewed distributions (approximately)', 2, 'moderately|approximate|skew|asymmetric|nearly', min=1)], 'c5'),
        V('v5', 'What is the relationship between AM, GM and HM? What special result holds for two positive numbers?',
          'For positive observations, the arithmetic mean is greater than or equal to the geometric mean, which is greater than or equal to the harmonic mean; they are equal only when all observations are equal. For two positive numbers, AM multiplied by HM equals the square of GM.',
          [P('p1', 'AM ≥ GM ≥ HM', 5, ALT('am {g} gm {g} hm', 'arithmetic mean {g} geometric mean {g} harmonic mean', 'hm {l} gm {l} am', 'harmonic mean {l} geometric mean {l} arithmetic mean',
                                       g=('greater than or equal to', 'greater than', 'greater or equal', 'at least', 'not less than', 'more than', 'greater equal', 'exceed', 'ge', 'is greater than or equal to', 'is greater than'),
                                       l=('less than or equal to', 'less than', 'less or equal', 'at most', 'not more than', 'smaller than'))),
           P('p2', 'Equal only when all observations are equal', 2, 'equal|same|constant|identical', 'all|every', min=2),
           P('p3', 'For two numbers AM × HM = GM²', 3, ALT('am {x} hm {e} gm square', 'am hm gm square', 'am {x} hm {e} square gm', 'am {x} hm {e} square of gm', 'arithmetic mean {x} harmonic mean {e} square of geometric mean', 'gm square {e} am {x} hm', 'square of gm {e} am {x} hm', 'gm squared {e} am {x} hm', 'am {x} hm {e} gm squared', 'a h {e} g square', 'ah {e} g square', 'ah g2', 'ah g squared',
                                            x=('times', 'multiplied by', 'into', 'x'), e=('equal', 'equals', 'is', 'equal to', 'is equal to')))], 'c7'),
        V('v6', 'When should we use the geometric mean and when the harmonic mean?',
          'The geometric mean is used to average rates of growth, ratios and percentage changes, for example average annual growth of sales or in index numbers, because the changes compound. The harmonic mean is used to average rates such as speed or price per unit when the distance or the amount spent is fixed, for example the average speed over equal distances.',
          [P('p1', 'GM: growth rates, ratios, percentage changes (compounding)', 5, ALT('{g} {u}', g=('geometric mean', 'gm', 'geometric'), u=('growth', 'ratio', 'percentage', 'compound', 'rate of change', 'index number', 'rate of increase', 'average growth', 'used for growth', 'used for ratio', 'used to average growth', 'used to average ratio', 'used to average rates of growth', 'is used for average growth', 'is used for growth'))),
           P('p2', 'HM: rates like speed / price per unit when distance or amount is fixed', 5, ALT('{h} {u}', h=('harmonic mean', 'hm', 'harmonic'), u=('speed', 'rate', 'per unit', 'price', 'equal distance', 'same distance', 'fixed distance', 'average speed', 'used for speed', 'used for rate', 'used to average speed', 'used to average rate', 'is used for speed', 'is used for average speed', 'is used to average speed', 'when distance')))], 'c6'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch14', 'n': 1,
        'title': 'Measures of Central Tendency',
        'outcomes': [
            'List the requisites of an ideal average and judge AM, median, mode, GM and HM against them.',
            'Compute the AM (direct and step-deviation), median, mode, GM, HM and weighted averages for raw and grouped data.',
            'Use the properties of averages — deviations, change of origin and scale, combined and corrected means, minimum absolute deviation.',
            'Find quartiles, deciles and percentiles for raw and grouped data and read them from an ogive.',
            'Apply the empirical relation Mode ≈ 3 Median − 2 Mean and the inequality AM ≥ GM ≥ HM (with AH = G² for two numbers).',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 60}, 'prereq': ['fnd-p3-ch13-u01'],
                 'exam_tip': 'Central tendency is one of the highest-scoring areas of Part C. Expect 4–6 MCQs: combined/corrected mean, change of origin and scale, median/mode formula, empirical relation, AM–GM–HM. Learn the formulas so well that each takes under a minute.'},
        'concepts': [
            {'id': 'c1', 'title': 'Central tendency and the ideal average',
             'body': ['A measure of central tendency (an average) is a single value around which the observations cluster and which represents the whole set. The five measures are arithmetic mean (AM), median (Me), mode (Mo), geometric mean (GM) and harmonic mean (HM).',
                      'An ideal measure should be (i) properly and unambiguously defined, (ii) easy to understand, (iii) simple to compute, (iv) based on all observations, (v) capable of mathematical treatment, and (vi) least affected by extreme observations (and by sampling fluctuations).'],
             'analogy': 'An average is a team captain — one person who represents everyone. A good captain is chosen by clear rules, understood by all, and not swayed by one loud member.',
             'work': 'When a company reports "average realisation per tonne", analysts check which average was used. A mean dragged up by a few premium sales can mislead; that is why medians often appear in compensation disclosures.'},
            {'id': 'c2', 'title': 'Arithmetic mean and its properties',
             'body': ['Raw data: x̄ = Σx/n. Grouped data: x̄ = Σfx/N with x the mid-value. Step-deviation (short-cut) method: take an origin A and class width C, d = (x − A)/C, then x̄ = A + (Σfd/N) × C.',
                      'Properties: (i) if every value is a constant k, the AM is k; (ii) the algebraic sum of deviations from the AM is zero — Σ(x − x̄) = 0, Σf(x − x̄) = 0; (iii) change of origin and scale: if y = a + bx then ȳ = a + b x̄; (iv) combined mean of two groups x̄ = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂), extendable to more groups.',
                      'Merits: rigidly defined, based on all values, easy, mathematically tractable, stable from sample to sample. Demerits: badly affected by extreme values and cannot be found for open-end classes without assuming mid-values.'],
             'blocks': [t1],
             'analogy': 'The mean is the balancing point of a see-saw loaded with the observations — deviations on the two sides cancel exactly.',
             'work': 'Correcting a mean after one wrong entry (subtract the wrong value, add the right one, divide again) is exactly how you fix an average debtor-days figure once a mis-keyed invoice is found.'},
            {'id': 'c3', 'title': 'Median',
             'body': ['Median is the middle value when observations are arranged in order — half lie below it and half above. Raw data: the ((n + 1)/2)th value; for even n, the AM of the two middle values.',
                      'Grouped data: find N/2 in the less-than cumulative frequency column to locate the median class. Me = l₁ + ((N/2 − Nl)/(Nu − Nl)) × C, where l₁ = lower boundary of the median class, Nl and Nu = less-than c.f. at its lower and upper boundaries (Nu − Nl = its frequency) and C = its width. Graphically, it is the x-value where the two ogives meet (or where N/2 cuts the less-than ogive).',
                      'Properties: if y = a + bx, then median of y = a + b × median of x. The sum of absolute deviations Σ|x − A| is minimum when A is the median.',
                      'Merits: easy, not affected by extreme values, the best average for open-end classes. Demerits: not based on all observations and not amenable to algebraic treatment.'],
             'analogy': 'The median is the middle person in a queue sorted by height — the very tall basketball player at the end does not move him.',
             'work': 'Median house price and median salary are quoted instead of means because a few very large values distort the mean.'},
            {'id': 'c4', 'title': 'Partition values — quartiles, deciles, percentiles',
             'body': ['Quartiles split ordered data into 4 equal parts (Q₁, Q₂ = median, Q₃); deciles into 10 parts (D₁ … D₉); percentiles into 100 parts (P₁ … P₉₉). Hence Q₂ = D₅ = P₅₀ = median, and Q₁ = P₂₅, Q₃ = P₇₅.',
                      'Raw data (ICAI rule): Q₁ is the ((n + 1)/4)th value, Q₃ the (3(n + 1)/4)th, Dₖ the (k(n + 1)/10)th, Pₖ the (k(n + 1)/100)th. For a fractional position, interpolate: 2.75th value = 2nd value + 0.75 × (3rd − 2nd).',
                      'Grouped data: replace N/2 in the median formula by Np (N/4 for Q₁, 3N/4 for Q₃, kN/10 for Dₖ …). Graphically, draw a horizontal line at Np to the less-than ogive and drop a perpendicular.'],
             'analogy': 'Cutting a sorted loaf into 4, 10 or 100 equal slices — the cut positions are the quartiles, deciles and percentiles.',
             'work': '"Top-quartile" fund performance, "90th percentile" response times in service contracts and salary benchmarking bands are all partition values.'},
            {'id': 'c5', 'title': 'Mode and the empirical relationship',
             'body': ['Mode is the value that occurs most often. It may not exist (all values occur equally often) or there may be more than one (bimodal).',
                      'Grouped data: the modal class has the highest frequency. Mo = l₁ + ((f₀ − f₋₁)/(2f₀ − f₋₁ − f₁)) × C, where f₀, f₋₁, f₁ are the frequencies of the modal, pre-modal and post-modal classes. Graphically, the mode is found from the histogram.',
                      'Empirical relation (moderately skewed distributions): Mean − Mode = 3(Mean − Median), i.e. Mode ≈ 3 Median − 2 Mean. Also, if y = a + bx, the mode of y = a + b × mode of x.',
                      'Merits: easy, the most "typical" value, not affected by extremes, usable for qualitative data. Demerits: may be undefined or multiple, has no mathematical properties and is affected by sampling fluctuations.'],
             'analogy': 'The mode is the most popular dish at a canteen — the one ordered most, not the "average" dish.',
             'work': 'Retailers stock to the modal size; quality teams look at the modal defect type first.'},
            {'id': 'c6', 'title': 'Geometric mean and harmonic mean',
             'body': ['GM of n positive values = (x₁ × x₂ × … × xₙ)^(1/n); log G = (Σ log x)/n — the log of the GM is the AM of the logs. Grouped: log G = Σf log x / N.',
                      'Properties of GM: if all values are k, GM = k; GM of a product z = xy is GM(x) × GM(y); GM of a ratio z = x/y is GM(x) ÷ GM(y). Use: average rates of growth, ratios, percentages and index numbers.',
                      'HM = n / Σ(1/x); grouped: N / Σ(f/x). If all values are k, HM = k. Combined HM of two groups = (n₁ + n₂)/(n₁/H₁ + n₂/H₂). Use: average of rates (speed, price per unit) when the distance or money spent is the same for each rate.',
                      'GM and HM are rigidly defined and based on all observations, but harder to understand and compute, so their use is limited to rates and ratios.'],
             'blocks': [table(['Situation', 'Correct average', 'Why'], [
                 ['Sales grew 10%, 20%, 32% in three years', 'GM of 1.10, 1.20, 1.32', 'Growth compounds on the previous year'],
                 ['Car goes 120 km at 60 km/h and returns 120 km at 40 km/h', 'HM of 60 and 40 = 48 km/h', 'Same distance at each speed'],
                 ['Car runs 3 h at 60 km/h and 2 h at 40 km/h', 'Weighted AM = 52 km/h', 'Weights are times'],
             ])],
             'analogy': 'GM is the "compound interest" average; HM is the "same-distance" average.',
             'work': 'CAGR quoted in equity research is a GM. The average cost per unit when a fixed amount is invested every month (rupee-cost averaging) is an HM of the prices.'},
            {'id': 'c7', 'title': 'AM ≥ GM ≥ HM, weighted averages and choosing an average',
             'body': ['For positive observations AM ≥ GM ≥ HM; equality holds only when all observations are equal. For two positive numbers a and b: A = (a + b)/2, G = √(ab), H = 2ab/(a + b), and A × H = G². This identity holds only for two numbers.',
                      'Weighted averages: weighted AM = Σwx/Σw; weighted GM = antilog(Σw log x/Σw); weighted HM = Σw/Σ(w/x). Use when observations differ in importance (marks with credit weights, prices with quantities).',
                      'Choosing: AM is usually the best (rigid, all values, stable) but avoid it with extreme values or open-end classes; median for open-end classes and skewed data; mode for the most typical value or qualitative data; GM for growth rates and ratios; HM for rates with a fixed numerator.'],
             'analogy': 'Three cousins who always stand in the same order of height — AM tallest, HM shortest — unless everyone in the family is identical.',
             'work': 'A cost accountant averaging material rates weights each rate by quantity (weighted AM). An investment analyst averaging P/E ratios across a portfolio of equal investments may use an HM.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Mean, median and mode of a wage distribution', 'difficulty': 'moderate', 'minutes': 14,
             'q': 'Daily wages (₹) of 100 workers: 200–250: 6, 250–300: 14, 300–350: 25, 350–400: 30, 400–450: 15, 450–500: 10. Find the mean (step-deviation method), median and mode.',
             'solution': [t1, wn('Mean', f'A = 375, C = 50, Σfd = {sfd}. x̄ = 375 + ({sfd}/100) × 50 = ₹{fm(mean1)}.'),
                          wn('Median', f'N/2 = 50 lies in 350–400 (c.f. 45 → 75). Me = 350 + (50 − 45)/30 × 50 = ₹{fm(med1)}.'),
                          wn('Mode', f'Modal class 350–400: f₀ = 30, f₋₁ = 25, f₁ = 15. Mo = 350 + (30 − 25)/(60 − 25 − 15) × 50 = ₹{fm(mode1)}.'),
                          note('Mean < Median < Mode: the distribution is slightly negatively skewed. Check with the empirical relation: 3 × 358.33 − 2 × 357 ≈ 361 — close to 362.5.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Quartiles, deciles and percentiles', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) Sorted test scores of 11 trainees: ' + ', '.join(map(str, data2)) + '. Find Q₁, Q₃, D₇ and P₃₀. (b) For the wage data of Illustration 1, find Q₁ and Q₃.',
             'solution': [wn('(a) Raw data — position k(n + 1)/m', f'Q₁: 12/4 = 3rd value = {fm(q1u)}. Q₃: 3 × 12/4 = 9th value = {fm(q3u)}. D₇: 7 × 12/10 = 8.4th value = {data2[7]} + 0.4 × ({data2[8]} − {data2[7]}) = {fm(d7)}. P₃₀: 30 × 12/100 = 3.6th value = {data2[2]} + 0.6 × ({data2[3]} − {data2[2]}) = {fm(p30)}.'),
                          wn('(b) Grouped', f'Q₁: N/4 = 25 lies in 300–350 (c.f. 20 → 45): Q₁ = 300 + (25 − 20)/25 × 50 = ₹{fm(gq1)}. Q₃: 3N/4 = 75 lies in 350–400 (c.f. 45 → 75): Q₃ = 350 + (75 − 45)/30 × 50 = ₹{fm(gq3)}.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Combined, corrected and transformed means', 'difficulty': 'moderate', 'minutes': 8,
             'q': '(a) 40 trainees earn a mean of ₹21,000 and 60 seniors ₹26,000. Combined mean? (b) The mean of 50 values was 64, but 82 was wrongly read for 28. Correct mean? (c) 2x + 5y = 30 and x̄ = 18. Find ȳ. (d) The mean of 25 numbers is 48; the mean of 20 of them is 45. Mean of the other 5?',
             'solution': [wn('(a)', f'(40 × 21,000 + 60 × 26,000)/100 = ₹{inr(cm)}.'),
                          wn('(b)', f'Correct total = 50 × 64 − 82 + 28 = 3,146; mean = {fm(corr)}.'),
                          wn('(c)', f'y = 6 − 0.4x, so ȳ = 6 − 0.4 × 18 = {fm(ym)}.'),
                          wn('(d)', f'(25 × 48 − 20 × 45)/5 = 300/5 = {fm(n3)}.')],
             'checks': c3},
            {'id': 'i4', 'title': 'GM for growth, HM for speed, weighted mean', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) Sales grew by 10%, 20% and 32% in three successive years. Average annual growth? (b) A courier drives 120 km at 60 km/h and back at 40 km/h. Average speed? (c) Verify AM ≥ GM ≥ HM and AH = G² for 4 and 9. (d) A student scores 78, 64, 85, 70 in papers with credit weights 3, 2, 4, 1. Weighted mean?',
             'solution': [wn('(a)', f'GM of growth factors = (1.10 × 1.20 × 1.32)^(1/3) = {gm4}; average growth ≈ 20.33% per year (the AM, 20.67%, overstates it). Check: ₹1,000 → ₹1,742.40 either way.'),
                          wn('(b)', f'Equal distances → HM = 2/(1/60 + 1/40) = {fm(hm4)} km/h (not 50).'),
                          wn('(c)', f'AM = {fm(am2)}, GM = {fm(gm2)}, HM = 72/13 ≈ {fm(hm2)}; 6.5 ≥ 6 ≥ 5.54 and 6.5 × 72/13 = 36 = 6².'),
                          wn('(d)', f'Σwx/Σw = (234 + 128 + 340 + 70)/10 = {fm(wam)}.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Which "average" goes into the board note?', 'role': 'Management accountant in a retail chain',
             'situation': 'Average bill value across 50,000 bills is ₹1,240, but 300 corporate bulk bills above ₹50,000 pull it up. The median bill is ₹640 and the most common bill band is ₹400–500.',
             'steps': ['Explain that the mean is distorted by a few extreme bills — it does not describe a typical customer.',
                       'Report the median (₹640) as the typical bill and the modal band for store staffing and stocking.',
                       'Keep the mean for revenue planning, because total revenue = mean × number of bills.',
                       'Show quartiles (Q₁, Q₃) so the board sees the spread of the middle 50% of bills.'],
             'takeaway': 'Choose the average that answers the question: totals → mean; typical value → median; most common → mode.',
             'think': 'Which average still lets you recover total revenue?', 'answer': 'Only the arithmetic mean: total = mean × count.'},
            {'id': 'j2', 'title': 'Computing CAGR for an equity research note', 'role': 'Research associate at a broking house',
             'situation': 'A company\'s revenue was ₹500 crore and is ₹845 crore four years later after uneven growth each year.',
             'steps': ['Average growth of a compounding quantity needs the GM of growth factors, not the AM of percentages.',
                       'CAGR = (845/500)^(1/4) − 1 = 1.69^(1/4) − 1 ≈ 14.02%.',
                       'Cross-check by compounding ₹500 crore at 14.02% for four years.',
                       'State the base and end year clearly — CAGR is sensitive to the choice of endpoints.'],
             'takeaway': 'CAGR is a geometric mean; an AM of yearly growth rates always overstates it when rates vary.',
             'checks': [{'expr': 'round(((845/500)**0.25-1)*100,2)', 'value': round(((845 / 500) ** 0.25 - 1) * 100, 2), 'label': 'CAGR %'}]},
        ],
        'mcqs': [
            nq('m1', 'The mean of the first 20 natural numbers is:', '(20+1)/2', [10, 11, 210],
               'Mean of 1, 2, …, n = (n + 1)/2 = 21/2 = @A. (210 is their sum.)', 'c2'),
            mq('m2', 'The algebraic sum of deviations of observations from their arithmetic mean is:', ['Zero', 'Minimum but positive', 'One', 'Maximum'],
               'Σ(x − x̄) = 0 always. The sum of squared deviations is minimum about the mean; the sum of absolute deviations is minimum about the median.', 'c2'),
            nq('m3', 'If y = 3 − 2x and the mean of x is 10, the mean of y is:', '3-2*10', [17, 23, -20],
               'ȳ = a + b x̄ = 3 − 2 × 10 = @A.', 'c2'),
            nq('m4', 'If 3x + 4y = 48 and x̄ = 8, then ȳ is:', '(48-3*8)/4', [8, 18, 4],
               'y = 12 − 0.75x, so ȳ = 12 − 0.75 × 8 = @A.', 'c2', 'moderate'),
            nq('m5', 'The mean weight of 30 boys is 52 kg and of 20 girls is 45 kg. The combined mean weight is:', '(30*52+20*45)/50', [48.5, 50, 47.8],
               '(30 × 52 + 20 × 45)/50 = 2,460/50 = @A kg. (48.5 is the simple average of the two means.)', 'c2'),
            nq('m6', 'The mean of 40 observations was 160. Later it was found that 165 was misread as 125. The correct mean is:', '(40*160-125+165)/40', [159, 164, 160.5],
               'Correct total = 6,400 − 125 + 165 = 6,440; mean = @A.', 'c2', 'moderate'),
            nq('m7', 'The mean of 10 numbers is 30. If each number is multiplied by 3 and then 5 is added, the new mean is:', '30*3+5', [105, 90, 93],
               'Change of origin and scale: new mean = 3 × 30 + 5 = @A.', 'c2'),
            nq('m8', 'The median of 18, 25, 11, 30, 22, 14, 27, 20 is:', '(20+22)/2', [20, 22, 20.88],
               'Sorted: 11, 14, 18, 20, 22, 25, 27, 30. n = 8, so median = (4th + 5th)/2 = (20 + 22)/2 = @A.', 'c3'),
            nq('m9', 'For a distribution, N = 80, the median class is 30–40, c.f. up to 30 is 32 and the median class frequency is 16. The median is:', '30+(40-32)/16*10', [35.5, 30.5, 38],
               'Me = 30 + (N/2 − 32)/16 × 10 = 30 + 8/16 × 10 = @A.', 'c3', 'moderate'),
            mq('m10', 'The sum of absolute deviations of a set of observations is minimum when taken from the:', ['Median', 'Mean', 'Mode', 'Geometric mean'],
               'Σ|x − A| is least for A = median.', 'c3'),
            mq('m11', 'The most suitable average for a distribution with open-end classes is the:', ['Median', 'Arithmetic mean', 'Geometric mean', 'Harmonic mean'],
               'The median uses only the middle position, so open ends do not matter.', 'c3'),
            nq('m12', 'For x and y related by 2x − 5y = 10, the median of x is 30. The median of y is:', '(2*30-10)/5', [4, 14, 12],
               'y = (2x − 10)/5 = −2 + 0.4x, so median of y = −2 + 0.4 × 30 = @A.', 'c3', 'moderate'),
            nq('m13', 'For the ordered data 8, 12, 15, 19, 23, 26, 31, the first quartile (ICAI positional rule) is:', '12', [15, 10, 13.5],
               'Q₁ = ((n + 1)/4)th = (8/4)th = 2nd value = @A.', 'c4'),
            nq('m14', 'For the ordered data 48, 53, 61, 70, 72, 79, 84, 92, 110, 125, the third quartile (ICAI positional rule) is:', '92+0.25*(110-92)', [92, 110, 101],
               'Q₃ = 3(n + 1)/4 = 8.25th value = 92 + 0.25 × (110 − 92) = @A.', 'c4', 'moderate'),
            mq('m15', 'Which of the following is equal to the median?', ['D₅ and P₅₀', 'D₂ and P₂₀', 'Q₁ and P₂₅', 'Q₃ and P₇₅'],
               'Median = Q₂ = D₅ = P₅₀.', 'c4'),
            mq('m16', 'The number of deciles in a distribution is:', ['9', '10', '4', '99'],
               'Ten equal parts need nine dividing points D₁ … D₉.', 'c4'),
            nq('m17', 'For a moderately skewed distribution, mean = 54 and median = 50. The mode is approximately:', '3*50-2*54', [46, 58, 48],
               'Mode = 3 Median − 2 Mean = 150 − 108 = @A.', 'c5'),
            nq('m18', 'For a moderately skewed distribution, mode = 24 and mean = 30. The median is approximately:', '(24+2*30)/3', [27, 26, 32],
               'From Mode = 3Me − 2x̄: Me = (Mode + 2 Mean)/3 = (24 + 60)/3 = @A.', 'c5', 'moderate'),
            nq('m19', 'The modal class is 40–50 with frequency 28; the classes before and after have frequencies 20 and 16. The mode is:', '40+(28-20)/(2*28-20-16)*10', [45, 46.67, 42],
               'Mo = 40 + (28 − 20)/(56 − 36) × 10 = 40 + 8/20 × 10 = @A.', 'c5', 'moderate'),
            mq('m20', 'For the values 5, 9, 12, 17, 21, no value repeats. The mode:', ['Does not exist', 'Is 12', 'Is 5', 'Is 21'],
               'When all values occur equally often there is no mode.', 'c5'),
            nq('m21', 'The geometric mean of 4, 6 and 9 is:', 'round((4*6*9)**(1/3),2)', [6.33, 5.68, 7],
               '(4 × 6 × 9)^(1/3) = 216^(1/3) = @A. (6.33 is the AM; 5.68 = 108/19 is the HM.)', 'c6'),
            nq('m22', 'The harmonic mean of 2, 3 and 6 is:', '3/(1/2+1/3+1/6)', [3.67, 3.3, 11],
               'HM = 3/(1/2 + 1/3 + 1/6) = 3/1 = @A.', 'c6'),
            nq('m23', 'A car travels from A to B at 30 km/h and returns over the same road at 60 km/h. The average speed for the round trip is:', '2/(1/30+1/60)', [45, 42.43, 50],
               'Equal distances → HM = 2/(1/30 + 1/60) = @A km/h.', 'c6', 'moderate', 'kmph'),
            mq('m24', 'The most appropriate average for the average rate of growth of population is the:', ['Geometric mean', 'Arithmetic mean', 'Harmonic mean', 'Mode'],
               'Growth compounds, so the GM of growth factors is used.', 'c6'),
            nq('m25', 'For two positive numbers, AM = 10 and GM = 8. The HM is:', '8**2/10', [6, 9, 7.2],
               'For two numbers AH = G², so H = 64/10 = @A.', 'c7', 'moderate'),
            nq('m26', 'The AM and GM of two positive numbers are 13 and 12. The larger number is:', '(26+(26**2-4*144)**0.5)/2', [16, 12, 13],
               'a + b = 26, ab = 144 ⇒ a, b are roots of t² − 26t + 144 = 0, i.e. 18 and 8. Larger = @A.', 'c7', 'hard'),
            mq('m27', 'For any set of positive observations, not all equal:', ['AM > GM > HM', 'AM < GM < HM', 'GM > AM > HM', 'HM > GM > AM'],
               'AM ≥ GM ≥ HM, with strict inequality unless all values are equal.', 'c7'),
            mq('m28', 'The relation AM × HM = GM² holds:', ['Only for two positive numbers', 'For any set of positive numbers', 'Only for three numbers', 'Never'],
               'It is an identity for two positive numbers only.', 'c7', 'moderate'),
            nq('m29', 'Marks 60, 75 and 90 carry weights 2, 3 and 5. The weighted mean is:', '(60*2+75*3+90*5)/10', [75, 77.5, 81],
               'Σwx/Σw = (120 + 225 + 450)/10 = @A.', 'c7'),
            nq('m30', 'The mean of the frequency distribution x: 10, 20, 30, 40 with f: 3, 7, f, 2 is 25. The missing frequency f is:', '(25*12-30-140-80)/(30-25)', [8, 6, 12],
               'Σfx = 30 + 140 + 30f + 80 = 25(12 + f) ⇒ 250 + 30f = 300 + 25f ⇒ f = @A.', 'c2', 'hard'),
            mq('m31', 'Which average is most affected by extreme observations?', ['Arithmetic mean', 'Median', 'Mode', 'Quartile'],
               'The AM uses every value with its full size, so one extreme value pulls it.', 'c1'),
            mq('m32', 'Which average is generally considered the best measure of central tendency?', ['Arithmetic mean', 'Mode', 'Harmonic mean', 'Median'],
               'ICAI: the AM is usually the best — rigidly defined, based on all observations, easy and mathematically tractable.', 'c7'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Marks of 70 students: 0–10: 5, 10–20: 8, 20–30: 15, 30–40: 22, 40–50: 12, 50–60: 8. Compute the mean (step-deviation), median and mode, and comment on the shape of the distribution.',
             'model': [tq1, wn('Mean', f'A = 35, C = 10, Σfd = {sfd1}: x̄ = 35 + ({sfd1}/70) × 10 = {fm(qm)}.'),
                       wn('Median', f'N/2 = 35 → class 30–40 (c.f. 28 → 50): Me = 30 + (35 − 28)/22 × 10 = {fm(qmed)}.'),
                       wn('Mode', f'Modal class 30–40: Mo = 30 + (22 − 15)/(44 − 15 − 12) × 10 = {fm(qmo)}.'),
                       p('Mean < Median < Mode, so the distribution is negatively skewed (a longer tail towards low marks).')],
             'scheme': [{'id': 's1', 'pt': 'Mid-values, d and fd column; Σfd correct', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': f'Mean = {fm(qm)}', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Median class located using N/2 and c.f.', 'm': 1, 'skill': 'application'},
                        {'id': 's4', 'pt': f'Median = {fm(qmed)}', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': f'Mode = {fm(qmo)}', 'm': 1, 'skill': 'computation'},
                        {'id': 's6', 'pt': 'Shape: negatively skewed (mean < median < mode)', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Most errors come from using class limits instead of boundaries and from wrong Nl in the median formula.'],
             'mistakes': ['Taking the c.f. of the median class itself as Nl.', 'Using f₀ − f₁ in the numerator of the mode formula.'],
             'tips': ['Write l₁, Nl, f, C before substituting.', 'Mean–median–mode order tells you the skew in one line.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
             'q': 'The median of the distribution below is 27. Find the missing frequency x. Classes: 0–10: 6, 10–20: 10, 20–30: x, 30–40: 18, 40–50: 6.',
             'model': [wn('Step 1', 'N = 40 + x. Median 27 lies in 20–30, so l₁ = 20, Nl = 16, f = x, C = 10.'),
                       wn('Step 2', '27 = 20 + ((40 + x)/2 − 16)/x × 10 ⇒ 7x = 5(40 + x) − 160 = 40 + 5x ⇒ 2x = 40.'),
                       wn('Step 3', f'x = {fm(x2)}. Check: N = 60, N/2 = 30, c.f. 16 → 36, Me = 20 + 14/20 × 10 = 27 ✓.')],
             'scheme': [{'id': 's1', 'pt': 'Median class and N = 40 + x identified', 'm': 1, 'skill': 'application'},
                        {'id': 's2', 'pt': 'Equation set up with the median formula', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'x = 20 and verified', 'm': 1.5, 'skill': 'computation'}],
             'remarks': ['Forgetting that N itself contains x is the usual slip.'],
             'mistakes': ['Taking N = 40.', 'Using Nl = 16 + x.'],
             'tips': ['Always verify by recomputing the median with the value found.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) Three sections of 30, 45 and 25 students have mean marks 52, 60 and 48. Find the combined mean. (b) Two positive numbers have AM 25 and HM 16. Find their GM and the numbers.',
             'model': [wn('(a)', f'(30 × 52 + 45 × 60 + 25 × 48)/100 = (1,560 + 2,700 + 1,200)/100 = {fm(q3a)}.'),
                       wn('(b)', f'For two numbers G² = A × H = 25 × 16 = 400 ⇒ G = {fm(q3g)}. a + b = 50, ab = 400 ⇒ t² − 50t + 400 = 0 ⇒ t = 40 or 10. Numbers: 40 and 10. Check: HM = 2 × 400/50 = 16 ✓.')],
             'scheme': [{'id': 's1', 'pt': 'Combined mean formula applied', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Combined mean 54.6', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'G = √(AH) = 20', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Quadratic set up and numbers 40, 10 found', 'm': 2, 'skill': 'computation'}],
             'remarks': ['Averaging the three means (53.33) is wrong — sizes differ.'],
             'mistakes': ['Using AH = G² for three numbers.', 'Solving the quadratic incorrectly.'],
             'tips': ['Verify the numbers by recomputing AM and HM.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Ideal average: rigid definition, easy, all values, algebraic treatment, least affected by extremes.',
                        'AM: Σx/n; step-deviation A + (Σfd/N)C; Σ(x − x̄) = 0; ȳ = a + bx̄; combined mean.',
                        'Median: middle value; l₁ + ((N/2 − Nl)/f)C; best for open-end classes; Σ|x − A| min at median.',
                        'Partition values: Q, D, P; raw data position k(n + 1)/m; grouped Np.',
                        'Mode: l₁ + ((f₀ − f₋₁)/(2f₀ − f₋₁ − f₁))C; Mode ≈ 3Me − 2x̄.',
                        'GM for growth/ratios; HM for rates over equal distances; AM ≥ GM ≥ HM; AH = G² (two numbers).'],
            'remember': ['Mean of first n natural numbers = (n + 1)/2.', 'Combined mean weights by group size.', 'Corrected mean: (n x̄ − wrong + right)/n.', 'Average speed for equal distances = HM.'],
            'traps': ['Do not average averages without weights.', 'AH = G² is only for TWO numbers.', 'Median of even n = mean of the two middle values.', 'Mode may not exist.']},
        'quickref': [
            {'k': 'AM (step deviation)', 'v': 'x̄ = A + (Σfd/N) × C, d = (x − A)/C'},
            {'k': 'Combined mean', 'v': '(n₁x̄₁ + n₂x̄₂)/(n₁ + n₂)'},
            {'k': 'Median (grouped)', 'v': 'l₁ + ((N/2 − Nl)/(Nu − Nl)) × C'},
            {'k': 'Quartile (grouped)', 'v': 'l₁ + ((Np − Nl)/(Nu − Nl)) × C, p = 1/4, 3/4'},
            {'k': 'Raw-data positions', 'v': 'Q₁: (n+1)/4; Q₃: 3(n+1)/4; Dₖ: k(n+1)/10; Pₖ: k(n+1)/100'},
            {'k': 'Mode (grouped)', 'v': 'l₁ + ((f₀ − f₋₁)/(2f₀ − f₋₁ − f₁)) × C'},
            {'k': 'Empirical relation', 'v': 'Mean − Mode = 3(Mean − Median); Mode ≈ 3Me − 2x̄'},
            {'k': 'GM / HM', 'v': 'GM = (Πx)^(1/n), log G = Σlog x / n; HM = n/Σ(1/x)'},
            {'k': 'Two numbers', 'v': 'AM ≥ GM ≥ HM and AM × HM = GM²'},
            {'k': 'Change of origin & scale', 'v': 'y = a + bx ⇒ ȳ = a + bx̄, Me(y) = a + b Me(x), Mo(y) = a + b Mo(x)'},
        ],
        'viva': viva, 'cases': cases,
    }
