"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 17 Correlation and Regression.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as _CM


def CM(*a, topic=None, **k):
    d = _CM(*a, **k); d['topic'] = topic
    return d

UID = 'fnd-p3-ch17-u01'


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


def ranks(vals, desc=True):
    """average ranks (1 = highest when desc)"""
    order = sorted(vals, reverse=desc)
    return [sum(i + 1 for i, v in enumerate(order) if v == x) / order.count(x) for x in vals]


def build():
    # ---------------- Illustration 1: Pearson r ----------------
    c1 = Checks()
    x = [2, 4, 5, 7, 8, 10]; y = [6, 9, 8, 13, 14, 16]
    mx = c1.add('36/6', 'mean of x'); my = c1.add('66/6', 'mean of y')
    dx = [a - 6 for a in x]; dy = [b - 11 for b in y]
    sdx2, sdy2, sdxy = sum(a * a for a in dx), sum(b * b for b in dy), sum(a * b for a, b in zip(dx, dy))
    rows1 = [[str(a), str(b), str(p_), str(q_), str(p_ * p_), str(q_ * q_), str(p_ * q_)] for a, b, p_, q_ in zip(x, y, dx, dy)]
    rows1.append(['36', '66', '0', '0', str(sdx2), str(sdy2), str(sdxy)])
    t1 = table(['x (ad spend, ₹ lakh)', 'y (sales, ₹ lakh)', 'u = x − 6', 'v = y − 11', 'u²', 'v²', 'uv'], rows1, num=[0, 1, 2, 3, 4, 5, 6], total=True, title='Advertising and sales of six months')
    r1 = c1.add(f'round({sdxy}/({sdx2}*{sdy2})**0.5,4)', 'Pearson r')
    c1.add(f'round(({sdxy}/({sdx2}*{sdy2})**0.5)**2,4)', 'coefficient of determination')
    byx = c1.add(f'round({sdxy}/{sdx2},4)', 'b_yx'); bxy = c1.add(f'round({sdxy}/{sdy2},4)', 'b_xy')
    est = c1.add(f'round(11+{sdxy}/{sdx2}*(12-6),2)', 'estimated sales at x = 12')
    c1.add(f'round(6+{sdxy}/{sdy2}*(18-11),2)', 'estimated x for y = 18 (x on y)')
    c1.add(f'round(({sdxy}/{sdx2}*{sdxy}/{sdy2})**0.5,4)', 'r as GM of regression coefficients')

    # ---------------- Illustration 2: Spearman ----------------
    c2 = Checks()
    ja = [1, 2, 3, 4, 5, 6, 7]; jb = [2, 1, 4, 3, 7, 5, 6]
    d2 = sum((a - b) ** 2 for a, b in zip(ja, jb))
    rs = c2.add(f'round(1-6*{d2}/(7*(7**2-1)),4)', 'rank correlation, no ties')
    m_e = [72, 65, 80, 65, 58, 90, 65, 74]; m_s = [68, 70, 78, 60, 55, 85, 62, 70]
    re_, rs_ = ranks(m_e), ranks(m_s)
    d2t = sum((a - b) ** 2 for a, b in zip(re_, rs_))
    corr = ((3 ** 3 - 3) + (2 ** 3 - 2)) / 12
    rows2 = [[str(a), str(b), fm(p_), fm(q_), fm(p_ - q_), fm((p_ - q_) ** 2)] for a, b, p_, q_ in zip(m_e, m_s, re_, rs_)]
    rows2.append(['', '', '', '', '0', fm(d2t)])
    t2 = table(['Economics', 'Statistics', 'Rank (Eco)', 'Rank (Stats)', 'd', 'd²'], rows2, num=[4, 5], total=True, title='Marks of 8 students with tied values')
    rt = c2.add(f'round(1-6*({d2t}+(3**3-3)/12+(2**3-2)/12)/(8*(8**2-1)),4)', 'rank correlation with tie correction')

    # ---------------- Illustration 3: concurrent deviations ----------------
    c3 = Checks()
    px = [100, 104, 101, 106, 110, 108, 112, 115]
    py = [50, 53, 52, 55, 54, 51, 56, 58]
    sx_ = ['+' if b > a else '−' for a, b in zip(px, px[1:])]
    sy_ = ['+' if b > a else '−' for a, b in zip(py, py[1:])]
    cc = sum(1 for a, b in zip(sx_, sy_) if a == b); mm = len(sx_)
    assert (cc, mm) == (6, 7)
    rc = c3.add('round(((2*6-7)/7)**0.5,4)', 'coefficient of concurrent deviations')
    rows3 = [[str(px[0]), '', str(py[0]), '', '']] + [[str(px[i + 1]), sx_[i], str(py[i + 1]), sy_[i], '+' if sx_[i] == sy_[i] else '−'] for i in range(mm)]
    t3 = table(['Price index x', 'Sign of change', 'Demand y', 'Sign of change', 'Product of signs'], rows3)

    # ---------------- Illustration 4: identifying regression lines ----------------
    c4 = Checks()
    yb = c4.add('20-17', 'ybar from solving x + 2y = 10 and 2x + 3y = 17'); xb = c4.add('10-2*3', 'xbar')
    b1 = c4.add('-1/2', 'b_yx if x + 2y = 10 is y on x'); b2 = c4.add('-3/2', 'b_xy if 2x + 3y = 17 is x on y')
    c4.add('0.5*1.5', 'product of regression coefficients (valid, <= 1)')
    c4.add('round((2/3)*2,4)', 'product under the other assignment (> 1, invalid)')
    r4 = c4.add('round(-(0.5*1.5)**0.5,4)', 'r (negative, common sign)')
    sy4 = c4.add('round(0.5/(0.75**0.5)*4,4)', 'sigma_y when sigma_x = 4 using b_yx = r sy/sx')

    # ---------------- Question 1 ----------------
    q1c = Checks()
    qx = [10, 12, 15, 18, 20]; qy = [40, 38, 33, 30, 24]
    qmx = sum(qx) / 5; qmy = sum(qy) / 5
    assert qmx == 15 and qmy == 33
    qu = [a - 15 for a in qx]; qv = [b - 33 for b in qy]
    su2, sv2, suv = sum(a * a for a in qu), sum(b * b for b in qv), sum(a * b for a, b in zip(qu, qv))
    rq1 = [[str(a), str(b), str(p_), str(q_), str(p_ * p_), str(q_ * q_), str(p_ * q_)] for a, b, p_, q_ in zip(qx, qy, qu, qv)]
    rq1.append(['75', '165', '0', '0', str(su2), str(sv2), str(suv)])
    tq1 = table(['Price x (₹)', 'Demand y (units)', 'u = x − 15', 'v = y − 33', 'u²', 'v²', 'uv'], rq1, num=[0, 1, 2, 3, 4, 5, 6], total=True)
    qr = q1c.add(f'round({suv}/({su2}*{sv2})**0.5,4)', 'r')
    q1c.add(f'round(({suv}/({su2}*{sv2})**0.5)**2,4)', 'r squared')

    # ---------------- Question 2 ----------------
    q2c = Checks()
    q2byx = q2c.add('0.8*12/8', 'b_yx = r sy/sx'); q2bxy = q2c.add('0.8*8/12', 'b_xy = r sx/sy')
    q2e = q2c.add('50+1.2*(45-40)', 'estimate y at x = 45')
    q2x = q2c.add('round(40+0.8*8/12*(62-50),4)', 'estimate x at y = 62')
    q2c.add('round(1.2*0.5333,2)', 'product approx r^2')

    # ---------------- Question 3 ----------------
    q3c = Checks()
    sa = [85, 70, 70, 62, 90, 55, 78, 70]; sb = [80, 72, 65, 60, 88, 58, 74, 69]
    ra, rb = ranks(sa), ranks(sb)
    d3 = sum((a - b) ** 2 for a, b in zip(ra, rb))
    rows_q3 = [[str(a), str(b), fm(p_), fm(q_), fm(p_ - q_), fm((p_ - q_) ** 2)] for a, b, p_, q_ in zip(sa, sb, ra, rb)]
    rows_q3.append(['', '', '', '', '0', fm(d3)])
    tq3 = table(['Judge A score', 'Judge B score', 'Rank A', 'Rank B', 'd', 'd²'], rows_q3, num=[4, 5], total=True)
    q3r = q3c.add(f'round(1-6*({d3}+(3**3-3)/12)/(8*(8**2-1)),4)', 'rank correlation with one tie of length 3')

    # ---------------- Case ----------------
    kc = Checks()
    kb = kc.add('0.75*6/2', 'b_yx'); kc.add('40+2.25*(14-12)', 'estimate'); kc.add('0.75**2', 'r squared')
    cases = [{
        'id': 'k1', 'title': 'Do training hours lift sales productivity?', 'difficulty': 'hard',
        'case': ('An FMCG company records, for 40 sales executives, the training hours attended last quarter (x) and the sales achieved this quarter in ₹ lakh (y). '
                 'Summary: mean x = 12 hours, mean y = ₹40 lakh, SD of x = 2 hours, SD of y = ₹6 lakh, correlation coefficient r = 0.75. The HR head wants to predict sales for an executive who attends 14 hours.'),
        'mcqs': [
            CM('k1a', 'What is the regression coefficient of y on x?', ['2.25', '0.25', '0.75', '4'], 0,
               'byx = r × σy ÷ σx = 0.75 × 6 ÷ 2 = 2.25, i.e. ₹2.25 lakh of extra sales per extra training hour. The trap is 0.25, which is bxy = r × σx ÷ σy (0.75 × 2 ÷ 6). In practice: HR and sales heads use such slopes to estimate the payoff from training budgets.', 'moderate', '0.75*6/2', topic='Regression and the method of least squares'),
            CM('k1b', 'What sales would you predict for an executive with 14 training hours?', ['₹44.5 lakh', '₹42.25 lakh', '₹41.5 lakh', '₹54 lakh'], 0,
               'ŷ = ȳ + byx (x − x̄) = 40 + 2.25 × (14 − 12) = 40 + 4.5 = ₹44.5 lakh. The trap is ₹42.25 lakh, which adds byx only once instead of multiplying by the 2-hour gap. In practice: regression-based forecasting is commonly used in sales planning and incentive-target setting.', 'moderate', '40+2.25*(14-12)', topic='Regression and the method of least squares'),
            CM('k1c', 'What proportion of the variation in sales is explained by training hours?', ['56.25%', '75%', '43.75%', '86.6%'], 0,
               'The coefficient of determination r² = 0.75² = 0.5625, so 56.25% of the variation in sales is explained by training hours. The trap is 75%, which is r expressed as a percentage, not r². 43.75% is unexplained. In practice: management reports quote R-squared to show how much of a performance gap a single factor really explains.', 'core', '0.75**2*100', topic='Coefficient of determination and spurious correlation'),
            CM('k1d', 'Which conclusion is appropriate?', ['Training and sales are strongly positively related, but correlation alone does not prove that training causes higher sales', 'Training certainly causes higher sales', 'There is no relationship', 'The relationship is negative'], 0,
               "r = 0.75 shows a strong positive linear association, but correlation does not prove causation: motivated executives might choose more training and also sell more. 'Training certainly causes higher sales' is the trap: it ignores possible third factors. In practice: before approving a large training budget, a CFO would want a controlled comparison, not just a correlation.", 'hard', topic='Coefficient of determination and spurious correlation'),
        ]}]

    viva = [
        V('v1', 'State the important properties of the correlation coefficient.',
          'The correlation coefficient is a pure number without units. It always lies between minus one and plus one, both included. It is unaffected by a change of origin, and a change of scale does not change its value either, only its sign can change when the two scale factors have opposite signs. It is the geometric mean of the two regression coefficients.',
          [P('p1', 'Lies between −1 and +1', 4, ALT('between minus 1 and {p}1', 'between {m} 1 and {p}1', 'minus 1 to {p}1', '{m}1 to {p}1', 'minus one to plus one', 'minus one and plus one', 'from minus 1 to plus 1', 'cannot exceed 1|not exceed 1|not more than 1', p=('plus ', '+', ''), m=('minus', 'negative', '-'))),
           P('p2', 'Unit-free / pure number', 2, 'unit free|no unit|without unit|pure number|independent of unit|free of unit|free from unit|unitless'),
           P('p3', 'Unaffected by change of origin and scale (sign may change with opposite-sign scales)', 4, ALT('{n} {c} origin', n=('not affected by', 'unaffected by', 'independent of', 'does not change with', 'not changed by', 'invariant under', 'remains unchanged under', 'unchanged by', 'no effect of', 'does not depend on'), c=('change of', 'a change of', 'shift of', 'the change of', '')), 'origin and scale|origin or scale|invariant', min=1)], 'c3'),
        V('v2', 'Explain Spearman\'s rank correlation coefficient. When is it preferred, and how are ties handled?',
          'Spearman\'s rank correlation is one minus six times the sum of squared rank differences, divided by n times n squared minus one. It is preferred for qualitative characteristics such as beauty or honesty that can only be ranked, or when the data are ranks. When values tie, each gets the average of the ranks they would have taken, and a correction of t cubed minus t over twelve is added to the sum of d squared for each tie.',
          [P('p1', 'r = 1 − 6Σd² / [n(n² − 1)]', 4, ALT('1 minus 6 {s} d square', '1 minus 6 {s} d squared', '1 minus 6 {s} d2', 'one minus six {s} d square', 'one minus six times the sum of squared', '1 minus 6 times sum of squared', s=('sum', 'sigma', 'times sum', 'times sigma', 'times the sum of', 'sum of', 'into sum'))),
           P('p2', 'Used for qualitative / ranked data', 3, 'qualitative|rank|beauty|honesty|intelligence|attribute|cannot be measured|not measurable|ordinal', min=1),
           P('p3', 'Ties: average rank and correction (t³ − t)/12', 3, 'average|mean rank|tie', 'correction|t cube|t3|cube minus|12|twelve', min=2)], 'c4'),
        V('v3', 'What is the difference between correlation and regression?',
          'Correlation measures the degree and direction of the linear relationship between two variables and is symmetric, so r of x and y equals r of y and x, and it is a pure number. Regression gives the average functional relationship, an equation used to estimate the value of a dependent variable from a known value of the independent variable. There are two regression lines, y on x and x on y, and regression coefficients have units.',
          [P('p1', 'Correlation: degree / strength and direction of relationship', 4, ALT('correlation {x}', x=('measure', 'degree', 'strength', 'extent', 'how strongly', 'closeness', 'direction', 'association', 'tells how', 'shows how'))),
           P('p2', 'Regression: equation to estimate/predict one variable from another', 4, ALT('regression {x}', x=('estimate', 'predict', 'equation', 'functional', 'forecast', 'average relationship', 'cause and effect', 'dependent', 'line'))),
           P('p3', 'Two regression lines (y on x, x on y)', 2, 'two line|two regression|y on x|x on y|both line', min=1)], 'c6'),
        V('v4', 'State the properties of regression coefficients and regression lines.',
          'The regression coefficients are unaffected by a change of origin but are affected by a change of scale. The two regression lines intersect at the point x bar, y bar, the means. The correlation coefficient is the geometric mean of the two regression coefficients, with the common sign, so both coefficients have the same sign and their product cannot exceed one. The lines coincide when r is plus or minus one and are perpendicular when r is zero.',
          [P('p1', 'Unaffected by change of origin, affected by change of scale', 2, 'origin', 'scale', min=2),
           P('p2', 'Lines intersect at (x̄, ȳ)', 3, 'intersect|meet|cross|cut', 'mean|x bar|xbar|average', min=2),
           P('p3', 'r = ±√(byx·bxy), same sign; product ≤ 1', 3, ALT('geometric mean', 'square root of {t} product', 'root of {t} product', 'square root of b y x', t=('the', '')), 'same sign|common sign|both positive|both negative', min=1),
           P('p4', 'Coincide when r = ±1; perpendicular when r = 0', 2, 'coincid|identical|same line|one line', 'perpendicular|right angle|90', min=1)], 'c7'),
        V('v5', 'What is the coefficient of determination, and how is it interpreted?',
          'The coefficient of determination is the square of the correlation coefficient, r squared. It is the ratio of the explained variance to the total variance, so it shows the proportion of variation in the dependent variable explained by the independent variable. For example, if r is 0.8, r squared is 0.64, so 64 percent of the variation is explained. One minus r squared is the coefficient of non-determination, the unexplained part.',
          [P('p1', 'Square of r', 4, 'r square|square of r|r squared|square of the correlation|square of correlation|r2|square of coefficient of correlation'),
           P('p2', 'Explained variance ÷ total variance (proportion explained)', 4, 'explained', 'total|proportion|percent|ratio|share|fraction', min=2),
           P('p3', '1 − r² = non-determination (unexplained)', 2, 'non determination|nondetermination|unexplained|1 minus r', min=1)], 'c5'),
        V('v6', 'What is spurious correlation? Give an example.',
          'Spurious or nonsense correlation is a correlation between two variables that have no cause and effect relationship; it appears because a third variable, such as time, influences both. For example, the production of rice and the production of iron may both rise over twenty years and show a high correlation, only because both grow with time. The influence of the third variable should be removed before reading meaning into r.',
          [P('p1', 'Correlation without a causal link (nonsense)', 4, 'nonsense|non sense|no cause|without cause|no causal|not causal|no real|meaningless|no logical|by chance', min=1),
           P('p2', 'Due to a third variable affecting both (e.g. time)', 4, 'third|common factor|another variable|other variable|lurking|time|both', min=1),
           P('p3', 'An example given', 2, 'example|rice|iron|ice cream|for instance|instance|like', min=1)], 'c5'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch17', 'n': 1,
        'title': 'Correlation and Regression',
        'outcomes': [
            'Describe bivariate data, a bivariate frequency table and its marginal and conditional distributions.',
            'Identify positive, negative, linear and non-linear correlation from a scatter diagram and measure it with Karl Pearson\'s r, Spearman\'s rank correlation (with ties) and the coefficient of concurrent deviations.',
            'Use the properties of r — limits, effect of change of origin and scale, coefficient of determination — and recognise spurious correlation.',
            'Fit the regression lines of y on x and x on y by least squares, use them to estimate values and apply the properties of regression coefficients.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 70}, 'prereq': ['fnd-p3-ch14-u02'],
                 'exam_tip': 'Expect 5–6 MCQs: r from summary data, r = ±√(byx·bxy), byx = r σy/σx, regression lines meet at the means, which given line is y on x, rank correlation from Σd², concurrent deviations, change of origin/scale. Always check that byx × bxy ≤ 1.'},
        'concepts': [
            {'id': 'c1', 'title': 'Bivariate data and bivariate frequency distribution',
             'body': ['When two variables are observed together on each unit — marks in two subjects, price and demand — the data are bivariate: pairs (xᵢ, yᵢ).',
                      'A bivariate (joint) frequency distribution, or two-way table, classifies the pairs by x-classes (columns) and y-classes (rows); each cell holds the frequency of that combination.',
                      'Marginal distributions: the row totals (distribution of y) and column totals (distribution of x). Conditional distribution: the distribution of one variable for a fixed class of the other (e.g. distribution of y for x in 40–50). Number of conditional distributions = number of classes of the conditioning variable.'],
             'analogy': 'A two-way table is a cricket scorecard by batsman and bowler; row totals give runs per batsman, column totals runs off each bowler.',
             'work': 'A debtors ageing by region (two-way: age band × region) is a bivariate frequency table; management reads both the marginal totals and the conditional rows.'},
            {'id': 'c2', 'title': 'Types of correlation and the scatter diagram',
             'body': ['Correlation: the two variables tend to move together. Positive — both move in the same direction (income and spending); negative — opposite directions (price and demand); zero — no linear relationship.',
                      'Linear correlation: the points lie close to a straight line; non-linear (curvilinear): they follow a curve.',
                      'Scatter diagram: plot each pair as a point. It shows direction, rough strength and whether the relation is linear or curvilinear, and it works for any type of relation — but it does not give a numerical measure. Always draw one first: r = 0 does not mean independence (y = x² over symmetric x gives r = 0).'],
             'analogy': 'A scatter diagram is a crowd photo from above — you see at once whether people are walking in a line, in a curve or milling about.',
             'work': 'Analysts plot fuel cost against kilometres for a fleet before trusting a cost-per-km rate; outliers on the plot point to data errors or unusual trips.'},
            {'id': 'c3', 'title': 'Karl Pearson\'s product moment correlation coefficient',
             'body': ['r = Cov(x, y)/(σx σy), where Cov(x, y) = Σ(x − x̄)(y − ȳ)/n. Working forms: r = Σuv/√(Σu² Σv²) with u = x − x̄, v = y − ȳ; or r = [nΣxy − ΣxΣy]/√{[nΣx² − (Σx)²][nΣy² − (Σy)²]}.',
                      'Properties: (i) r is a pure number (unit-free); (ii) −1 ≤ r ≤ 1 — r = 1 perfect positive, r = −1 perfect negative, r = 0 no linear correlation; (iii) r is unchanged by change of origin and scale — if u = (x − a)/b and v = (y − c)/d then r(u, v) = r(x, y) when b and d have the same sign, and r(u, v) = −r(x, y) when they have opposite signs; (iv) r = ±√(byx × bxy).',
                      'Change of origin (e.g. u = x − A) simplifies arithmetic without changing r.'],
             'blocks': [t1],
             'analogy': 'r is a "togetherness score" from −1 (perfect mirror image) through 0 (strangers) to +1 (perfect twins).',
             'work': 'Correlating monthly sales with advertising, or a stock\'s returns with the index (the basis of beta), is everyday analytical work.'},
            {'id': 'c4', 'title': 'Spearman\'s rank correlation and concurrent deviations',
             'body': ['Spearman: rR = 1 − 6Σd²/[n(n² − 1)], d = difference between the two ranks of each item. Used for qualitative traits (beauty, honesty) or when only ranks are available. Lies between −1 and 1.',
                      'Ties: give tied items the average of the ranks they occupy; then rR = 1 − 6[Σd² + Σ(t³ − t)/12]/[n(n² − 1)], adding (t³ − t)/12 for every group of t tied values (in either series).',
                      'Coefficient of concurrent deviations: compare the direction of change of each series from one period to the next (+ or −); c = number of pairs with the same sign (concurrent), m = number of pairs of deviations (= n − 1). rC = ±√[±(2c − m)/m] — take the plus sign inside and outside when 2c − m > 0, the minus sign both places when 2c − m < 0. It too lies between −1 and 1; it shows direction quickly but is a rough measure.'],
             'blocks': [t2],
             'analogy': 'Rank correlation asks only "did the two judges put the contestants in the same order?", not by how many points.',
             'work': 'Comparing two credit-rating agencies\' rankings of the same borrowers, or two interviewers\' rankings of candidates, uses rank correlation.'},
            {'id': 'c5', 'title': 'Coefficient of determination and spurious correlation',
             'body': ['Coefficient of determination = r² = explained variance ÷ total variance: the share of variation in y accounted for by x. r = 0.8 ⇒ r² = 0.64, i.e. 64% explained. Coefficient of non-determination = 1 − r² (unexplained share).',
                      'Spurious (nonsense) correlation: a correlation between variables with no causal link, produced by a third variable affecting both — e.g. rice output and iron output both rising with time. Remove the third variable\'s influence before interpreting r. Correlation never proves causation by itself.'],
             'analogy': 'Ice-cream sales and drowning cases rise together — not because ice-cream drowns people, but because summer drives both.',
             'work': 'Before telling a client that a marketing campaign "caused" higher sales, check for seasonal effects or price changes that moved both.'},
            {'id': 'c6', 'title': 'Regression and the method of least squares',
             'body': ['Regression estimates the average relationship between a dependent (explained) variable and an independent (explanatory) variable, so that one can be estimated from the other.',
                      'Regression line of y on x (to estimate y from x): y − ȳ = byx (x − x̄), with byx = Cov(x, y)/σx² = r σy/σx = Σuv/Σu². It minimises the sum of squared vertical deviations Σ(y − ŷ)² — the method of least squares. Normal equations for y = a + bx: Σy = na + bΣx and Σxy = aΣx + bΣx².',
                      'Regression line of x on y (to estimate x from y): x − x̄ = bxy (y − ȳ), bxy = r σx/σy = Σuv/Σv². It minimises horizontal squared deviations.',
                      'Use the y-on-x line to estimate y and the x-on-y line to estimate x — they are different lines unless r = ±1.'],
             'analogy': 'The least-squares line is the "fairest" straight line through a cloud of points — it keeps the total squared miss as small as possible.',
             'work': 'Cost accountants split semi-variable costs into fixed and variable parts by regressing total cost on output (y = a + bx: a = fixed cost, b = variable cost per unit).'},
            {'id': 'c7', 'title': 'Properties of regression coefficients and lines',
             'body': ['(i) Regression coefficients are unchanged by a shift of origin but change with scale: if u = (x − a)/p and v = (y − c)/q, then byx = (q/p) bvu and bxy = (p/q) buv.',
                      '(ii) The two lines intersect at (x̄, ȳ) — solve the two equations simultaneously to get the means.',
                      '(iii) r = ±√(byx × bxy), the geometric mean of the regression coefficients, taking their common sign. Hence both coefficients have the same sign as r, and byx × bxy = r² ≤ 1; they cannot both be numerically greater than 1.',
                      '(iv) The lines coincide (are identical) when r = ±1, and are perpendicular when r = 0.',
                      'Identifying lines from two equations: assume one is y on x, find byx and bxy; if their product is ≤ 1 (and signs agree) the assumption is right; otherwise swap.'],
             'analogy': 'Two regression lines are scissors hinged at the means: fully closed when r = ±1, opened to a right angle when r = 0.',
             'work': 'When a client gives only two fitted equations, these properties let you recover the means and r in a minute — and spot an impossible pair of coefficients.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Pearson r, regression lines and an estimate', 'difficulty': 'moderate', 'minutes': 15,
             'q': 'Advertising (x, ₹ lakh) and sales (y, ₹ lakh) for six months: x: ' + ', '.join(map(str, x)) + '; y: ' + ', '.join(map(str, y)) + '. Find r, r², both regression lines and estimate sales when advertising is ₹12 lakh.',
             'solution': [t1, wn('Correlation', f'x̄ = {fm(mx)}, ȳ = {fm(my)}. r = Σuv/√(Σu²Σv²) = {sdxy}/√({sdx2} × {sdy2}) = {fm(r1)}; r² ≈ {fm(round(r1 ** 2, 4))} — about 95% of the variation in sales is explained by advertising.'),
                          wn('Regression lines', f'byx = Σuv/Σu² = {sdxy}/{sdx2} = {fm(byx)} ⇒ y − 11 = {fm(byx)}(x − 6). bxy = Σuv/Σv² = {sdxy}/{sdy2} = {fm(bxy)} ⇒ x − 6 = {fm(bxy)}(y − 11).'),
                          wn('Estimate and check', f'At x = 12: ŷ = 11 + {fm(byx)} × 6 = ₹{fm(est)} lakh. Check: √(byx × bxy) = √({fm(byx)} × {fm(bxy)}) = {fm(r1)} = r.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Rank correlation without and with ties', 'difficulty': 'moderate', 'minutes': 12,
             'q': '(a) Two judges rank 7 entries: Judge A 1, 2, 3, 4, 5, 6, 7; Judge B 2, 1, 4, 3, 7, 5, 6. Find the rank correlation. (b) Marks of 8 students in Economics: ' + ', '.join(map(str, m_e)) + '; in Statistics: ' + ', '.join(map(str, m_s)) + '. Find the rank correlation (rank 1 = highest).',
             'solution': [wn('(a)', f'd: −1, 1, −1, 1, −2, 1, 1; Σd² = {d2}. rR = 1 − 6 × {d2}/(7 × 48) = {fm(rs)}.'), t2,
                          wn('(b)', f'Economics: 65 appears three times (ranks 5, 6, 7 → 6 each). Statistics: 70 appears twice (ranks 3, 4 → 3.5 each). Correction = (3³ − 3)/12 + (2³ − 2)/12 = 2 + 0.5 = {fm(corr)}. rR = 1 − 6({fm(d2t)} + 2.5)/(8 × 63) = {fm(rt)}.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Coefficient of concurrent deviations', 'difficulty': 'core', 'minutes': 7,
             'q': 'Price index x: ' + ', '.join(map(str, px)) + '. Demand index y: ' + ', '.join(map(str, py)) + '. Find the coefficient of concurrent deviations.',
             'solution': [t3, wn('Working', f'm = {mm} pairs of deviations, c = {cc} concurrent (+ products). 2c − m = 5 > 0, so rC = +√(5/7) = {fm(rc)}.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Which line is which? Means and r from two regression equations', 'difficulty': 'hard', 'minutes': 10,
             'q': 'The two regression lines are x + 2y = 10 and 2x + 3y = 17, and σx = 4. Find x̄, ȳ, identify the lines, and find r and σy.',
             'solution': [wn('Means', f'Solving: x = 10 − 2y ⇒ 20 − 4y + 3y = 17 ⇒ ȳ = {fm(yb)}, x̄ = {fm(xb)}.'),
                          wn('Identify', f'Assume x + 2y = 10 is y on x: y = 5 − 0.5x ⇒ byx = {fm(b1)}. Then 2x + 3y = 17 is x on y: x = 8.5 − 1.5y ⇒ bxy = {fm(b2)}. Product 0.75 ≤ 1 ✓ (the other assignment gives (−2/3)(−2) = 1.33 > 1 — impossible).'),
                          wn('r and σy', f'r = −√0.75 = {fm(r4)} (negative, the common sign). byx = r σy/σx ⇒ −0.5 = −0.866 × σy/4 ⇒ σy ≈ {fm(sy4)}.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Separating fixed and variable cost by regression', 'role': 'Cost accountant in a manufacturing unit',
             'situation': 'Monthly power cost and machine hours for 12 months are available. The plant head wants a budget formula.',
             'steps': ['Plot cost (y) against machine hours (x) — check the relation is linear and remove months with breakdowns.',
                       'Fit y = a + bx by least squares: b = Σuv/Σu² (variable cost per hour), a = ȳ − b x̄ (fixed cost).',
                       'Report r²: if 0.9, about 90% of the cost variation is explained by machine hours.',
                       'Use the y-on-x line only within the range of hours observed — extrapolation is risky.'],
             'takeaway': 'Least-squares regression turns past cost data into a flexible-budget formula.'},
            {'id': 'j2', 'title': 'Testing an analytical review assumption', 'role': 'Audit senior performing substantive analytics',
             'situation': 'You expect commission expense to move with sales. For 12 months r = 0.35, much lower than in prior years (0.9).',
             'steps': ['A weak r means sales explain only about 12% (r²) of the variation in commission this year.',
                       'Scatter the data — one or two months may hold large one-off commissions or misposted entries.',
                       'Investigate those months with documents before concluding.',
                       'If the scheme changed (e.g. slab-based payouts), the relation may be non-linear — r understates it.'],
             'takeaway': 'A sudden fall in r is an audit signal: either the business changed or the books contain errors.',
             'checks': [{'expr': '0.35**2', 'value': round(0.35 ** 2, 2), 'label': 'r squared'}]},
        ],
        'mcqs': [
            mq('m1', 'The correlation coefficient always lies between:', ['−1 and +1, both inclusive', '0 and 1', '−∞ and +∞', '0 and ∞'],
               "Karl Pearson's correlation coefficient always lies between −1 and +1, both inclusive: −1 is perfect negative, +1 perfect positive and 0 no linear correlation. '0 and 1' is the trap: it ignores negative correlation, which is common. In practice: analysts quoting the correlation between two stocks' returns, say −0.3 or +0.8, rely on this bounded scale.", 'c3', topic="Karl Pearson's product moment correlation coefficient"),
            mq('m2', 'Price and quantity demanded usually show:', ['Negative correlation', 'Positive correlation', 'Zero correlation', 'Perfect positive correlation'],
               'As price rises, quantity demanded usually falls, so the two move in opposite directions, which is negative correlation (the law of demand). Positive correlation is the trap: that is typical of price and quantity supplied. In practice: FMCG companies study this negative relation when deciding whether a price increase will reduce volumes too much.', 'c2', topic='Types of correlation and the scatter diagram'),
            mq('m3', 'A scatter diagram can be used to study:', ['Both linear and non-linear relationships', 'Only linear relationships', 'Only the exact value of r', 'Only qualitative data'],
               "A scatter diagram simply plots the pairs, so it reveals the pattern of any relationship, straight-line or curved, although it gives no numerical value. 'Only linear relationships' is the trap: that limitation belongs to Pearson's r, not the scatter diagram. In practice: analysts plot advertising spend against sales first, to see whether a straight-line model is even sensible.", 'c2', topic='Types of correlation and the scatter diagram'),
            nq('m4', 'Cov(x, y) = 18, σx = 4 and σy = 5. The correlation coefficient is:', '18/(4*5)', [3.6, 4.5, 0.36],
               'r = Cov(x, y) ÷ (σx σy) = 18 ÷ (4 × 5) = 18 ÷ 20 = 0.9. The trap is 3.6, which divides by σy alone (18 ÷ 5); in any case r can never exceed 1. In practice: risk models compute correlation between assets from their covariance and volatilities exactly this way.', 'c3', topic="Karl Pearson's product moment correlation coefficient"),
            nq('m5', 'For 10 pairs: Σuv = 48, Σu² = 64, Σv² = 100 (u, v deviations from means). r is:', '48/(64*100)**0.5', [0.75, 0.48, 0.0075],
               'With deviations from means, r = Σuv ÷ √(Σu² × Σv²) = 48 ÷ √(64 × 100) = 48 ÷ 80 = 0.6. The trap is 0.75, which is 48 ÷ 64, a regression coefficient (b of v on u), not r. In practice: spreadsheet CORREL functions use this formula when finding how strongly, say, rainfall and fertiliser sales move together.', 'c3', 'moderate', topic="Karl Pearson's product moment correlation coefficient"),
            mq('m6', 'If u = 2x + 5 and v = −3y + 1, and r(x, y) = 0.6, then r(u, v) is:', ['−0.6', '0.6', '−3.6', '0.4'],
               "Correlation is unaffected by change of origin, and by change of scale except for sign. The scale factors 2 and −3 have opposite signs, so the size stays 0.6 but the sign flips: r(u, v) = −0.6. The trap is 0.6, which ignores the negative factor. In practice: converting a cost into 'savings' (a negative transformation) reverses the sign of its correlation with other variables.", 'c3', 'moderate', topic="Karl Pearson's product moment correlation coefficient"),
            mq('m7', 'If r = 0 between x and y, then:', ['There is no linear relationship, though a non-linear one may exist', 'x and y are always independent', 'The regression lines coincide', 'r² = 1'],
               "r = 0 means there is no linear relationship, but a curved relationship may still exist; for example y = x² over symmetric x values gives r = 0. 'x and y are always independent' is the trap: zero correlation does not prove independence. In practice: a near-zero r between price and profit may hide an optimum price, so analysts always look at the scatter plot.", 'c2', 'moderate', topic='Types of correlation and the scatter diagram'),
            nq('m8', 'For 7 items, Σd² = 28. Spearman\'s rank correlation is:', '1-6*28/(7*48)', [0.75, 0.6667, 0.1667],
               "Spearman's formula: R = 1 − 6Σd² ÷ (n(n² − 1)) = 1 − (6 × 28) ÷ (7 × 48) = 1 − 168 ÷ 336 = 0.5. The traps 0.6667 and 0.75 come from computing n(n² − 1) wrongly; for n = 7 it is 7 × 48 = 336. In practice: rank correlation is used when only rankings are available, such as comparing two judges' rankings of contestants or two analysts' stock rankings.", 'c4', topic="Spearman's rank correlation and concurrent deviations"),
            nq('m9', 'Rank correlation is 0.4 for 10 pairs. Σd² is:', '(1-0.4)*10*99/6', [66, 165, 39.6],
               'From R = 1 − 6Σd² ÷ (n(n² − 1)): 0.4 = 1 − 6Σd² ÷ 990, so 6Σd² = 0.6 × 990 = 594 and Σd² = 99. The trap is 66, which uses 0.4 instead of 1 − 0.4. In practice: working backwards from a coefficient helps auditors check published survey results for internal consistency.', 'c4', 'hard', topic="Spearman's rank correlation and concurrent deviations"),
            mq('m10', 'Spearman\'s rank correlation is most suitable for:', ['Qualitative characteristics that can be ranked, like beauty', 'Data with exact measurements only', 'Open-end classes', 'Time series only'],
               "Spearman's method needs only ranks, so it suits qualitative characteristics that can be ordered but not measured, such as beauty, honesty or leadership. 'Data with exact measurements only' is the trap: exact measurements suit Pearson's r. In practice: HR teams use rank correlation to compare two interviewers' rankings of candidates.", 'c4', topic="Spearman's rank correlation and concurrent deviations"),
            nq('m11', 'Three items are tied in one series. The correction added to Σd² is:', '(3**3-3)/12', [3, 0.25, 6],
               'For each group of t tied items, add (t³ − t) ÷ 12 to Σd². With t = 3: (27 − 3) ÷ 12 = 24 ÷ 12 = 2. The trap is 3, which simply uses the number of tied items. In practice: ties are common when ranking things like branch performance grades, and this correction keeps the coefficient accurate.', 'c4', 'moderate', topic="Spearman's rank correlation and concurrent deviations"),
            nq('m12', 'For 9 pairs of observations (8 pairs of deviations), the number of concurrent deviations is 6. The coefficient of concurrent deviations is:', 'round(((2*6-8)/8)**0.5,4)', [0.5, 0.75, -0.7071],
               'With m = 8 pairs of deviations and c = 6 concurrent, 2c − m = 4, which is positive, so rC = +√((2c − m) ÷ m) = √(4 ÷ 8) = √0.5 ≈ 0.7071. The trap is 0.5, which forgets the square root. In practice: concurrent deviations offer a quick, rough check on whether two series, such as monthly sales and advertising, move in the same direction.', 'c4', 'moderate', topic="Spearman's rank correlation and concurrent deviations"),
            nq('m13', 'With m = 10 deviations and c = 2 concurrent, the coefficient of concurrent deviations is:', 'round(-((10-2*2)/10)**0.5,4)', [0.7746, -0.6, 0.2],
               '2c − m = 4 − 10 = −6, which is negative. The rule is to take the sign of (2c − m) both inside and outside the root: rC = −√(6 ÷ 10) = −√0.6 ≈ −0.7746. The trap is +0.7746, which drops the negative sign. In practice: a negative value shows that two series, such as interest rates and bond prices, usually move in opposite directions.', 'c4', 'hard', topic="Spearman's rank correlation and concurrent deviations"),
            nq('m14', 'If r = 0.9, the coefficient of determination is:', '0.81', [0.9, 0.19, 0.95],
               'The coefficient of determination is r² = 0.9² = 0.81, meaning 81% of the variation in y is explained by x. The trap is 0.9, which is r itself. 0.19 is the unexplained part (1 − r²). In practice: analysts report r² (R-squared) to show how much of the variation in sales a regression model actually explains.', 'c5', topic='Coefficient of determination and spurious correlation'),
            mq('m15', 'A high positive correlation between the number of mobile phones sold and the number of cars sold over 15 years, caused by rising incomes, is an example of:', ['Spurious (nonsense) correlation', 'Negative correlation', 'Perfect correlation', 'Rank correlation'],
               'Both phone sales and car sales are driven by a third factor, rising incomes over time, so their high correlation does not mean one causes the other. This is spurious (nonsense) correlation. Perfect correlation is the trap: that would need r = ±1 exactly. In practice: analysts must check for a common driver before claiming that one business metric causes another.', 'c5', topic='Coefficient of determination and spurious correlation'),
            nq('m16', 'r = 0.6, σx = 3, σy = 5. The regression coefficient of y on x is:', '0.6*5/3', [0.36, 0.6, 1.8],
               'byx = r × σy ÷ σx = 0.6 × 5 ÷ 3 = 1. The trap is 0.36, which is bxy = r × σx ÷ σy = 0.6 × 3 ÷ 5. In practice: byx tells a business how much y changes for each one-unit change in x, such as extra sales per ₹1 lakh of advertising.', 'c6', topic='Regression and the method of least squares'),
            nq('m17', 'byx = 0.8 and bxy = 0.45. The correlation coefficient is:', 'round((0.8*0.45)**0.5,4)', [0.36, 0.625, -0.6],
               'r² = byx × bxy = 0.8 × 0.45 = 0.36, so r = √0.36 = 0.6, taking the sign of the coefficients (both positive). The trap is 0.36, which is r², not r. In practice: when a report gives both regression slopes but not r, this relation recovers it quickly.', 'c7', topic='Properties of regression coefficients and lines'),
            nq('m18', 'byx = −0.5 and bxy = −1.28. The correlation coefficient is:', 'round(-(0.5*1.28)**0.5,4)', [0.8, 0.64, -0.64],
               'r² = byx × bxy = (−0.5) × (−1.28) = 0.64, so |r| = 0.8. r takes the common sign of the coefficients, which is negative, so r = −0.8. The trap is +0.8, which ignores the sign. In practice: a negative r between, for example, interest rates and housing loans disbursed tells a bank that demand falls as rates rise.', 'c7', 'moderate', topic='Properties of regression coefficients and lines'),
            mq('m19', 'Which pair of regression coefficients is impossible?', ['byx = 1.6, bxy = 0.8', 'byx = 0.4, bxy = 0.9', 'byx = −0.3, bxy = −2', 'byx = 2, bxy = 0.25'],
               "Since r² = byx × bxy, the product must not exceed 1. For 1.6 and 0.8, the product is 1.28 > 1, which would make r² > 1, impossible. 'byx = 2, bxy = 0.25' is the trap: the product is 0.5, which is fine. In practice: checking this product is a quick way to spot errors in a regression report.", 'c7', 'moderate', topic='Properties of regression coefficients and lines'),
            mq('m20', 'The two regression lines intersect at:', ['(x̄, ȳ)', '(0, 0)', '(σx, σy)', '(byx, bxy)'],
               'Both regression lines pass through the point of means, so they intersect at (x̄, ȳ). (0, 0) is the trap: lines pass through the origin only if both means are zero. In practice: solving the two regression equations together is a quick way to recover the averages when only the equations are reported.', 'c7', topic='Properties of regression coefficients and lines'),
            nq('m21', 'The regression lines are 2x − y = 1 and 3x − 2y = 0. The mean of x is:', '2', [3, 1, 1.5],
               'Both regression lines pass through (x̄, ȳ), so solve them together. From the first, y = 2x − 1. Substitute into the second: 3x − 2(2x − 1) = 0, so −x + 2 = 0 and x̄ = 2 (then ȳ = 3). The trap is 3, which is ȳ. In practice: recovering means from regression equations is a common shortcut when only a fitted model is published.', 'c7', 'moderate', topic='Properties of regression coefficients and lines'),
            mq('m22', 'The two regression lines are perpendicular to each other when:', ['r = 0', 'r = 1', 'r = −1', 'r = 0.5'],
               "When r = 0 there is no linear relation, and the two regression lines become perpendicular (one horizontal, one vertical). 'r = 1' is the trap: with perfect correlation the lines coincide instead. In practice: the angle between the two lines gives a visual sense of how strongly two business variables are linearly related.", 'c7', topic='Properties of regression coefficients and lines'),
            mq('m23', 'The regression lines coincide when:', ['r = ±1', 'r = 0', 'byx = 0', 'σx = σy'],
               "With perfect correlation, r = ±1, all points lie on one straight line, so the two regression lines coincide. 'r = 0' is the trap: that makes the lines perpendicular, not coincident. In practice: perfectly correlated variables, such as a fixed per-unit cost against volume, give a single exact line.", 'c7', topic='Properties of regression coefficients and lines'),
            mq('m24', 'Regression coefficients are:', ['Unaffected by change of origin but affected by change of scale', 'Affected by change of origin only', 'Unaffected by both', 'Affected by both origin and scale equally'],
               "Shifting origin does not change slopes, so regression coefficients are unaffected by a change of origin; but a change of scale multiplies them by the ratio of the scale factors. 'Unaffected by both' is the trap: it holds for r's size, not for regression coefficients. In practice: re-expressing sales from ₹ to ₹ lakh changes the regression slope accordingly.", 'c7', 'moderate', topic='Properties of regression coefficients and lines'),
            nq('m25', 'If u = (x − 10)/2 and v = (y − 20)/5 and bvu = 0.4, then byx is:', '5/2*0.4', [0.16, 0.4, 2],
               'With u = (x − 10) ÷ 2 and v = (y − 20) ÷ 5, the scale factors are p = 2 for x and q = 5 for y. byx = (q ÷ p) × bvu = (5 ÷ 2) × 0.4 = 1. The trap is 0.16, which uses the ratio the wrong way round (2 ÷ 5 × 0.4). In practice: coding data to simplify arithmetic is common, but slopes must be converted back to original units.', 'c7', 'hard', topic='Properties of regression coefficients and lines'),
            nq('m26', 'The regression line of y on x is y = 4 + 1.5x. The estimate of y when x = 6 is:', '4+1.5*6', [9, 15, 10],
               'Substitute x = 6 into the regression line: ŷ = 4 + 1.5 × 6 = 4 + 9 = 13. The trap is 9, which forgets the intercept 4. In practice: companies use such fitted lines to forecast sales or costs, for example estimating maintenance cost from machine hours.', 'c6', topic='Regression and the method of least squares'),
            nq('m27', 'x̄ = 20, ȳ = 30, byx = 0.6. The estimate of y when x = 25 is:', '30+0.6*(25-20)', [33.75, 15, 45],
               'ŷ = ȳ + byx (x − x̄) = 30 + 0.6 × (25 − 20) = 30 + 3 = 33. The trap is 15, which multiplies 0.6 by 25 and ignores the means. In practice: this form of the regression line is used for budgeting, such as estimating power cost at a planned production level.', 'c6', 'moderate', topic='Regression and the method of least squares'),
            mq('m28', 'The method of least squares for the regression of y on x minimises:', ['The sum of squares of vertical deviations of y from the line', 'The sum of horizontal deviations', 'The sum of absolute deviations of x', 'The product of deviations'],
               "For the regression of y on x, the method of least squares chooses the line that makes Σ(y − ŷ)², the sum of squared vertical deviations, as small as possible. 'The sum of horizontal deviations' is the trap: horizontal deviations are used for the regression of x on y. In practice: cost-estimation models in management accounting use least squares to split mixed costs.", 'c6', topic='Regression and the method of least squares'),
            mq('m29', 'In a bivariate frequency table with 5 classes of x and 4 classes of y, the number of conditional distributions of y (given x) is:', ['5', '4', '20', '9'],
               'There is one conditional distribution of y for each class of x, so with 5 classes of x there are 5 conditional distributions of y. The trap is 4, which counts the classes of y instead. In practice: bivariate tables, such as employees by age group and salary band, allow analysts to study salary patterns within each age group.', 'c1', 'moderate', topic='Bivariate data and bivariate frequency distribution'),
            mq('m30', 'Which statement about correlation and regression is correct?', ['r is symmetric in x and y, but byx and bxy generally differ', 'byx always equals bxy', 'Regression is unit-free', 'r has the units of y per unit of x'],
               "The correlation coefficient is symmetric: r(x, y) = r(y, x). But byx = rσy ÷ σx and bxy = rσx ÷ σy usually differ, being equal only when σx = σy. 'byx always equals bxy' is the trap. In practice: predicting sales from advertising and predicting advertising from sales use different regression lines, so analysts must pick the right one.", 'c6', 'moderate', topic='Regression and the method of least squares'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Price (₹) and demand (units) of a product over five weeks: x: ' + ', '.join(map(str, qx)) + '; y: ' + ', '.join(map(str, qy)) + '. Compute Karl Pearson\'s coefficient of correlation and interpret it with r².',
             'model': [tq1, wn('Means', 'x̄ = 75/5 = 15; ȳ = 165/5 = 33.'),
                       wn('r', f'r = Σuv/√(Σu² Σv²) = {suv}/√({su2} × {sv2}) = {fm(qr)}.'),
                       p(f'Very high negative correlation: as price rises demand falls. r² ≈ {fm(round(qr * qr, 4))} — about {round(qr * qr * 100)}% of the variation in demand is associated with price.')],
             'scheme': [{'id': 's1', 'pt': 'Means and deviations u, v', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Σu², Σv², Σuv correct', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': f'r = {fm(qr)}', 'm': 2, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Interpretation incl. r²', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Losing the minus sign of Σuv is the commonest error.'],
             'mistakes': ['Dividing by n in the numerator but not the denominator.', 'Interpreting r² as r.'],
             'tips': ['Deviations from the actual means make Σu = Σv = 0 — a built-in check.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'For two variables, x̄ = 40, ȳ = 50, σx = 8, σy = 12 and r = 0.8. (a) Find both regression equations. (b) Estimate y when x = 45. (c) Estimate x when y = 62. (d) Verify that r is the geometric mean of the regression coefficients.',
             'model': [wn('(a)', f'byx = 0.8 × 12/8 = {fm(q2byx)} ⇒ y − 50 = 1.2(x − 40), i.e. y = 1.2x + 2. bxy = 0.8 × 8/12 = {fm(q2bxy)} ⇒ x − 40 = 0.5333(y − 50), i.e. x = 0.5333y + 13.33.'),
                       wn('(b)', f'ŷ = 50 + 1.2 × 5 = {fm(q2e)}.'), wn('(c)', f'x̂ = 40 + 0.5333 × 12 = {fm(q2x)}.'),
                       wn('(d)', '√(1.2 × 0.5333) = √0.64 = 0.8 = r ✓.')],
             'scheme': [{'id': 's1', 'pt': 'byx = 1.2 and y-on-x equation', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'bxy = 0.5333 and x-on-y equation', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'y estimated with y-on-x line (56)', 'm': 1, 'skill': 'application'},
                        {'id': 's4', 'pt': 'x estimated with x-on-y line (46.4)', 'm': 1, 'skill': 'application'},
                        {'id': 's5', 'pt': 'Verification r = √(byx·bxy)', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Using the y-on-x line to estimate x (by rearranging it) is wrong and is penalised.'],
             'mistakes': ['byx = r σx/σy (inverted).', 'Rearranging one line for both estimates.'],
             'tips': ['Label each line "y on x" or "x on y" before using it.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'table',
             'q': 'Two judges scored 8 contestants. Judge A: ' + ', '.join(map(str, sa)) + '. Judge B: ' + ', '.join(map(str, sb)) + '. Compute the rank correlation coefficient (rank 1 = highest score).',
             'model': [tq3, wn('Ties', 'Judge A gives 70 to three contestants (ranks 4, 5, 6 → 5 each): correction (3³ − 3)/12 = 2. Judge B has no ties.'),
                       wn('Result', f'rR = 1 − 6({fm(d3)} + 2)/(8 × 63) = {fm(q3r)} — a high positive agreement between the judges.')],
             'scheme': [{'id': 's1', 'pt': 'Ranks with average rank for ties', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'd and Σd²', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Tie correction (t³ − t)/12 = 2', 'm': 1, 'skill': 'concept'},
                        {'id': 's4', 'pt': f'rR = {fm(q3r)} and interpretation', 'm': 1.5, 'skill': 'computation'}],
             'remarks': ['Many give tied scores the same integer rank (4, 4, 4) — use the average (5, 5, 5).'],
             'mistakes': ['Omitting the tie correction.', 'Ranking one judge ascending and the other descending.'],
             'tips': ['Check Σd = 0 before squaring.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Bivariate data; two-way table; marginal (totals) and conditional distributions.',
                        'Scatter diagram shows direction and form; r measures linear association only.',
                        'r = Cov/(σxσy) = Σuv/√(Σu²Σv²); −1 ≤ r ≤ 1; unit-free; unchanged by origin/scale (sign flips if scales have opposite signs).',
                        'Spearman 1 − 6Σd²/[n(n² − 1)], ties add (t³ − t)/12; concurrent deviations ±√[±(2c − m)/m].',
                        'r² explained share; 1 − r² unexplained; beware spurious correlation.',
                        'y on x: y − ȳ = byx(x − x̄), byx = rσy/σx; x on y: x − x̄ = bxy(y − ȳ), bxy = rσx/σy; lines meet at (x̄, ȳ); r = ±√(byx bxy).'],
            'remember': ['byx × bxy = r² ≤ 1; same sign as r.', 'r = ±1 → lines coincide; r = 0 → perpendicular.', 'm = n − 1 in concurrent deviations.', 'Estimate y with the y-on-x line, x with the x-on-y line.'],
            'traps': ['Correlation is not causation.', 'r = 0 does not prove independence.', 'Regression coefficients DO change with scale.', 'Do not forget the tie correction for every tied group in either series.']},
        'quickref': [
            {'k': 'Pearson r', 'v': 'Cov(x, y)/(σxσy) = [nΣxy − ΣxΣy]/√{[nΣx² − (Σx)²][nΣy² − (Σy)²]}'},
            {'k': 'Spearman (ties)', 'v': '1 − 6[Σd² + Σ(t³ − t)/12]/[n(n² − 1)]'},
            {'k': 'Concurrent deviations', 'v': 'rC = ±√[±(2c − m)/m], m = n − 1'},
            {'k': 'Regression y on x', 'v': 'y − ȳ = byx(x − x̄); byx = rσy/σx = Cov/σx²'},
            {'k': 'Regression x on y', 'v': 'x − x̄ = bxy(y − ȳ); bxy = rσx/σy = Cov/σy²'},
            {'k': 'Link', 'v': 'r = ±√(byx · bxy); byx · bxy ≤ 1'},
            {'k': 'Change of origin & scale', 'v': 'u = (x − a)/p, v = (y − c)/q: r unchanged (sign of pq); byx = (q/p)bvu, bxy = (p/q)buv'},
            {'k': 'Determination', 'v': 'r² = explained/total variance; 1 − r² = non-determination'},
        ],
        'viva': viva, 'cases': cases,
    }
