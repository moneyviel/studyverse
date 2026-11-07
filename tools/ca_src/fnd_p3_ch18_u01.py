"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 18 Index Numbers.
Original data sets. Every product, total and index below is computed in Python and stored with a re-checkable expression."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch18-u01'


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None, topic=None):
    d = {'topic': topic, 'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def r2(x): return round(x + 1e-12, 2)
def f2(x): return f'{r2(x):.2f}'


def sums(data):
    s = {'p0q0': 0, 'p1q0': 0, 'p0q1': 0, 'p1q1': 0}
    for _, p0, q0, p1, q1 in data:
        s['p0q0'] += p0 * q0; s['p1q0'] += p1 * q0; s['p0q1'] += p0 * q1; s['p1q1'] += p1 * q1
    return s


def products_table(data, title):
    rows = [[n, str(p0), str(q0), str(p1), str(q1), str(p0 * q0), str(p1 * q0), str(p0 * q1), str(p1 * q1)] for n, p0, q0, p1, q1 in data]
    s = sums(data)
    rows.append(['Total', '', '', '', '', str(s['p0q0']), str(s['p1q0']), str(s['p0q1']), str(s['p1q1'])])
    return table(['Item', 'p0', 'q0', 'p1', 'q1', 'p0q0', 'p1q0', 'p0q1', 'p1q1'], rows, num=[5, 6, 7, 8], total=True, title=title)


def build():
    # ================= Data set 1 (illustrations and MCQs) =================
    D1 = [('A', 10, 5, 12, 6), ('B', 8, 10, 10, 8), ('C', 5, 8, 6, 10), ('D', 20, 2, 25, 3)]
    s = sums(D1); assert s == {'p0q0': 210, 'p1q0': 258, 'p0q1': 234, 'p1q1': 287}
    c1 = Checks()
    agg = c1.add('round((12+10+6+25)/(10+8+5+20)*100,2)', 'simple aggregative price index')
    rel_avg = c1.add('(12/10*100+10/8*100+6/5*100+25/20*100)/4', 'simple average of price relatives')
    c2 = Checks()
    L = c2.add('round(258/210*100,2)', 'Laspeyres price index')
    Pa = c2.add('round(287/234*100,2)', 'Paasche price index')
    ME = c2.add('round((258+287)/(210+234)*100,2)', 'Marshall-Edgeworth price index')
    F = c2.add('round((258/210*287/234)**0.5*100,2)', 'Fisher ideal price index')
    assert (L, Pa, ME, F, agg, rel_avg) == (122.86, 122.65, 122.75, 122.75, 123.26, 122.5)
    c3 = Checks()
    trt = c3.add('round((258/210*287/234)**0.5*(234/287*210/258)**0.5,6)', 'P01 x P10 for Fisher (time reversal)')
    Qf = c3.add('round((234/210*287/258)**0.5*100,2)', 'Fisher quantity index')
    Vi = c3.add('round(287/210*100,2)', 'value index')
    frt = c3.add('round((258/210*287/234)**0.5*(234/210*287/258)**0.5,6)', 'P01 x Q01 for Fisher')
    c3.add('round(287/210,6)', 'value ratio V01 = sum p1q1 / sum p0q0')
    assert trt == 1 and frt == round(287 / 210, 2)
    Lq = r2(234 / 210 * 100); Pq = r2(287 / 258 * 100)
    lasp_trt = round(258 / 210 * 234 / 287, 4)           # Laspeyres P01 x P10 (P10 by Laspeyres uses q1 as base weights)
    assert lasp_trt != 1

    # ================= Weighted average of relatives — cost of living =================
    COL = [('Food', 135, 45), ('Clothing', 120, 15), ('Fuel and light', 150, 10), ('House rent', 110, 20), ('Miscellaneous', 125, 10)]
    c4 = Checks()
    col = c4.add('(135*45+120*15+150*10+110*20+125*10)/(45+15+10+20+10)', 'cost of living index (weighted A.M. of group indices)')
    assert col == 128.25
    # base-value weighted relatives = Laspeyres (shown on D1)
    wrel = r2(sum((p1 / p0 * 100) * (p0 * q0) for _, p0, q0, p1, q1 in D1) / s['p0q0']); assert wrel == L
    c4.add('round((120*50+125*80+120*40+125*40)/210,2)', 'weighted average of relatives with base values p0q0 as weights (equals Laspeyres)')

    # ================= Chain base =================
    yrs = [2019, 2020, 2021, 2022, 2023]; price = [40, 44, 55, 66, 60]
    link = [100] + [price[i] / price[i - 1] * 100 for i in range(1, 5)]
    chain = [100]
    for lr in link[1:]: chain.append(chain[-1] * lr / 100)
    assert [r2(x) for x in link] == [100, 110, 125, 120, 90.91] and [r2(x) for x in chain] == [100, 110, 137.5, 165, 150]
    c5 = Checks()
    c5.add('44/40*100', 'link relative 2020'); c5.add('55/44*100', 'link relative 2021'); c5.add('66/55*100', 'link relative 2022'); c5.add('round(60/66*100,2)', 'link relative 2023')
    c5.add('110*125/100', 'chain index 2021'); c5.add('137.5*120/100', 'chain index 2022'); c5.add('round(165*(60/66*100)/100,2)', 'chain index 2023')
    c5.add('60/40*100', 'fixed-base index 2023 (same as chain index for one item)')

    # ================= Shifting and splicing =================
    old = [(2018, 100), (2019, 110), (2020, 125), (2021, 132), (2022, 150)]
    shifted = [(y, r2(v / 125 * 100)) for y, v in old]; assert [v for _, v in shifted] == [80, 88, 100, 105.6, 120]
    c6 = Checks(); c6.add('100/125*100', '2018 on base 2020'); c6.add('132/125*100', '2021 on base 2020'); c6.add('150/125*100', '2022 on base 2020')
    oldS = [(2015, 100), (2016, 108), (2017, 115), (2018, 120)]; newS = [(2018, 100), (2019, 105), (2020, 112)]
    fwd = [(y, r2(v * 120 / 100)) for y, v in newS]; back = [(y, r2(v * 100 / 120)) for y, v in oldS]
    assert [v for _, v in fwd] == [120, 126, 134.4] and [v for _, v in back] == [83.33, 90, 95.83, 100]
    c6.add('105*120/100', 'new 2019 spliced to old base'); c6.add('112*120/100', 'new 2020 spliced to old base'); c6.add('round(100*100/120,2)', 'old 2015 spliced to new base')

    # ================= Deflating =================
    c7 = Checks()
    real24 = c7.add('54000/180*100', 'real salary 2024 at base-year prices'); real20 = c7.add('36000/120*100', 'real salary 2020 at base-year prices')
    pp = c7.add('100/125', 'purchasing power of a rupee when CPI = 125')
    assert real24 == real20 == 30000

    # ================= Stock index =================
    c8 = Checks(); newidx = c8.add('20000*410000/400000', 'index today = yesterday\'s index x today\'s market cap / yesterday\'s market cap')
    assert newidx == 20500

    # ================= Case data =================
    D2 = [('Rice (kg)', 40, 50, 46, 45), ('Oil (litre)', 120, 10, 150, 9), ('Sugar (kg)', 36, 20, 40, 25)]
    s2 = sums(D2); assert s2 == {'p0q0': 3920, 'p1q0': 4600, 'p0q1': 3780, 'p1q1': 4420}
    kL = r2(4600 / 3920 * 100); kP = r2(4420 / 3780 * 100); kF = r2((4600 / 3920 * 4420 / 3780) ** 0.5 * 100); kV = r2(4420 / 3920 * 100)
    assert (kL, kP, kF, kV) == (117.35, 116.93, 117.14, 112.76)

    # ================= Questions =================
    D3 = [('X', 6, 10, 9, 8), ('Y', 4, 15, 5, 20), ('Z', 10, 5, 12, 6)]
    s3 = sums(D3); assert s3 == {'p0q0': 170, 'p1q0': 225, 'p0q1': 188, 'p1q1': 244}
    cq1 = Checks()
    qL = cq1.add('round(225/170*100,2)', 'Laspeyres'); qP = cq1.add('round(244/188*100,2)', 'Paasche')
    qF = cq1.add('round((225/170*244/188)**0.5*100,2)', 'Fisher price index')
    cq1.add('round((225/170*244/188)**0.5*(188/244*170/225)**0.5,6)', 'time reversal: P01 x P10 = 1')
    cq1.add('round((225/170*244/188)**0.5*(188/170*244/225)**0.5,6)', 'factor reversal: P01 x Q01')
    cq1.add('round(244/170,6)', 'V01 = 244/170')
    assert (qL, qP, qF) == (132.35, 129.79, 131.06)
    qprice = [500, 550, 660, 594, 653.4]
    qlink = [100] + [qprice[i] / qprice[i - 1] * 100 for i in range(1, 5)]
    qchain = [100]
    for lr in qlink[1:]: qchain.append(qchain[-1] * lr / 100)
    assert [r2(x) for x in qlink] == [100, 110, 120, 90, 110] and [r2(x) for x in qchain] == [100, 110, 132, 118.8, 130.68]
    cq2 = Checks(); cq2.add('550/500*100', 'LR yr 2'); cq2.add('660/550*100', 'LR yr 3'); cq2.add('594/660*100', 'LR yr 4'); cq2.add('round(653.4/594*100,2)', 'LR yr 5')
    cq2.add('110*120/100', 'CI yr 3'); cq2.add('round(132*90/100,2)', 'CI yr 4'); cq2.add('round(118.8*110/100,2)', 'CI yr 5'); cq2.add('round(653.4/500*100,2)', 'fixed-base check yr 5')
    cq3 = Checks(); cq3.add('round(140/112*100,2)', '2024 index shifted to base 2022'); cq3.add('round(48000/112*100,2)', 'real wage 2022'); cq3.add('round(56000/140*100,2)', 'real wage 2024')
    cq3.add('round((40000-42857.14)/42857.14*100,2)', 'change in real wage 2022 to 2024 (%)')
    rw22 = r2(48000 / 112 * 100); rw24 = r2(56000 / 140 * 100); assert (rw22, rw24) == (42857.14, 40000)

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch18', 'n': 1, 'title': 'Index Numbers',
        'outcomes': ['Explain what an index number measures and the issues in constructing one — purpose and data, base period, weights, average, variables and formula.',
                     'Compute price, quantity and value relatives, link and chain relatives, and simple aggregative and simple-average-of-relatives indices.',
                     'Compute weighted indices — Laspeyres, Paasche, Marshall-Edgeworth, Fisher and the weighted average of relatives — and chain-base indices.',
                     'Apply the unit, time reversal, factor reversal and circular tests; shift the base, splice two series, deflate money values and explain how a stock-market index is computed.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 70}, 'prereq': ['fnd-p3-ch14-u01'],
                 'exam_tip': 'Set up one product table (p0q0, p1q0, p0q1, p1q1) and every weighted index — Laspeyres, Paasche, Marshall-Edgeworth, Fisher, quantity and value index — comes from the same four totals. Theory MCQs on the tests (which formula satisfies which test) appear in almost every paper.'},
        'concepts': [
            {'id': 'c1', 'title': 'What an index number is', 'body': [
                'An index number measures the relative change in a variable or a group of related variables between a base period (or place) and another period (or place). The base is taken as 100, so an index of 125 means a rise of 25% over the base.',
                'Because prices of rice per kg and of cloth per metre cannot be added meaningfully, indices work with relatives (ratios to the base), which are pure numbers and can be averaged. An index number is therefore a specialised average of relatives.',
                'Simple index: one variable (e.g. price of petrol). Composite index: many variables combined (e.g. a consumer price index). Most indices in use — WPI, CPI, Sensex, Nifty — are composite.',
                'A run of index numbers for successive periods, all calculated on one common base, is called an index time series. Notation: P01 is the index for period 1 with period 0 as base; P10 is period 0 on base period 1.'],
             'analogy': 'An index is like a report card that gives marks out of 100 for the base year and compares every later year to it.',
             'work': 'CAs use indices constantly: CPI for real-salary analysis and escalation clauses, WPI or input-price indices for cost-escalation claims in contracts, and stock indices as benchmarks for portfolio performance.'},
            {'id': 'c2', 'title': 'Issues in constructing an index', 'body': [
                'Purpose and selection of data: decide exactly what the index must measure, then choose items relevant to it (a cost-of-living index for workers need not include machinery prices). Use a representative sample — random or stratified random — and keep the method of selection consistent so that periods are comparable.',
                'Base period: should be normal (free from abnormal events such as war, famine, pandemic shocks), reasonably recent, and of suitable length. Bases may be fixed, chain (previous period) or an average of several periods.',
                'Weights: each item should influence the index according to its importance — cereals must weigh more than salt in a cost-of-living index. Weights may be quantities or values.',
                'Average: the geometric mean is theoretically best for averaging relatives (it treats rises and falls symmetrically and gives time-reversible results), but the arithmetic mean is used more often because it is simple.',
                'Choice of variables and prices: wholesale or retail, period-average or end-of-period prices, depending on the purpose.',
                'Formula: different formulae give different answers from the same data, so the formula must suit the purpose and pass the important tests.'],
             'analogy': 'Building an index is like designing a thali to represent a region\'s food: choose typical dishes (items), a typical day (base), portion sizes (weights) and one way of scoring the meal (formula).',
             'work': 'When a client uses an index in a price-variation clause, the CA checks which index, which base and which month\'s figure the clause specifies — disputes usually arise from these choices.'},
            {'id': 'c3', 'title': 'Relatives — price, quantity, value, link and chain', 'body': [
                'Price relative = p1 / p0 × 100. Quantity relative = q1 / q0 × 100. Value relative = (p1q1) / (p0q0) × 100.',
                'Link relatives compare each period with the period just before it: p1/p0, p2/p1, p3/p2 … (× 100).',
                'Chain relatives (relatives chained to a fixed base) compare each period with the same base: p1/p0, p2/p0, p3/p0 … (× 100). Chaining the link relatives by successive multiplication gives them.'],
             'analogy': 'A link relative is "how did I do compared with last year"; a chain relative is "how far have I come since the first year".',
             'work': 'Year-on-year growth in an MIS is a link relative; growth since the year of acquisition is a chain relative.'},
            {'id': 'c4', 'title': 'Unweighted methods', 'body': [
                'Simple aggregative price index = Σp1 / Σp0 × 100. Easy, but items quoted in large units or at high prices dominate, and changing a unit (per kg to per quintal) changes the index — it fails the unit test.',
                'Simple average of price relatives = Σ(p1/p0 × 100) / N (or the geometric mean of the relatives). Relatives are pure numbers, so it passes the unit test — but every item gets equal importance, which over-weights minor items.'],
             'blocks': [table(['Item', 'p0', 'p1', 'Price relative'], [[n, str(p0), str(p1), f2(p1 / p0 * 100)] for n, p0, q0, p1, q1 in D1], title='Data set 1 — price relatives')],
             'analogy': 'A simple aggregative index adds apples and elephants by weight; the average of relatives scores each animal\'s growth out of 100 first, then averages.',
             'work': 'A quick unweighted index is fine for an internal trend line; for anything contractual or published, a weighted formula is expected.'},
            {'id': 'c5', 'title': 'Weighted aggregative indices', 'body': [
                'Laspeyres (base-year quantities as weights): Σp1q0 / Σp0q0 × 100 — the cost of buying the base-year basket now, compared with then.',
                'Paasche (current-year quantities as weights): Σp1q1 / Σp0q1 × 100.',
                'Typical-period weights: Σp1qt / Σp0qt × 100, where qt are quantities of some typical period; fixed weights make the index satisfy the circular test.',
                'Marshall-Edgeworth (average of base and current quantities): Σp1(q0 + q1) / Σp0(q0 + q1) × 100.',
                'Fisher\'s ideal index: the geometric mean of Laspeyres and Paasche = √(Σp1q0/Σp0q0 × Σp1q1/Σp0q1) × 100.',
                'Quantity indices swap the roles of p and q: Laspeyres Σq1p0 / Σq0p0, Paasche Σq1p1 / Σq0p1, Fisher = their geometric mean. Value index = Σp1q1 / Σp0q0 × 100.'],
             'blocks': [products_table(D1, 'Data set 1 — the four product totals')],
             'analogy': 'Laspeyres asks, "What would last year\'s shopping bag cost today?" Paasche asks, "What would this year\'s shopping bag have cost last year?"',
             'work': 'Inflation in a client\'s purchase basket (for budgeting or cost audit) is usually measured Laspeyres-style, because base-year quantities are known in advance and do not need re-collecting every period.'},
            {'id': 'c6', 'title': 'Weighted average of relatives', 'body': [
                'Index = Σ(R × W) / ΣW, where R is the price relative of each item (or group index) and W its weight. With base-year values (p0q0) as weights the result equals the Laspeyres index.',
                'Consumer price (cost-of-living) indices are built this way: group indices for food, clothing, fuel, housing and miscellaneous, weighted by the share of each group in the family budget, and combined by the arithmetic mean.',
                'A weighted geometric mean of relatives can also be used.'],
             'blocks': [table(['Group', 'Group index (R)', 'Weight (W)', 'R × W'], [[g, str(r), str(w), str(r * w)] for g, r, w in COL] + [['Total', '', '100', str(sum(r * w for _, r, w in COL))]], num=[2, 3], total=True, title='Cost-of-living index')],
             'analogy': 'It is like a weighted exam aggregate: each paper\'s percentage counts in proportion to its marks.',
             'work': 'Dearness-allowance and rent-escalation calculations often use a CPI that is exactly such a weighted average of group indices.'},
            {'id': 'c7', 'title': 'Chain-base index numbers', 'body': [
                'Step 1: link relative for each period = current price / previous price × 100. Step 2: chain index = link relative of the current period × chain index of the previous period ÷ 100, starting from 100.',
                'For a single item the chain index equals the fixed-base index; for a group it can differ.',
                'Use: when items or weights change often (new products, changing habits) — each year is compared with the year before, so new items can be brought in easily. Drawback: an error in any link is carried into every later chain index; and for a stable basket the chain method is an unnecessary complication.'],
             'blocks': [table(['Year', 'Price', 'Link relative', 'Chain index'], [[str(y), str(pr), f2(lr), f2(ci)] for y, pr, lr, ci in zip(yrs, price, link, chain)], title='Chain index (generated)')],
             'analogy': 'A chain index is a relay race: each runner (year) is timed against the previous runner, and the baton carries the total forward.',
             'work': 'GDP at constant prices and many official series are now chain-linked; CAs reading these series must know that each year\'s figure is built on the previous year\'s.'},
            {'id': 'c8', 'title': 'Tests of adequacy', 'body': [
                'Unit test: the index should not depend on the units in which prices or quantities are quoted. Every formula except the simple aggregative index passes.',
                'Time reversal test: the index computed forward and backward should be reciprocals: P01 × P10 = 1 (indices as ratios, not percentages). Fisher passes; Laspeyres and Paasche fail.',
                'Factor reversal test: price index × quantity index = value index: P01 × Q01 = Σp1q1 / Σp0q0. Fisher passes; Laspeyres and Paasche fail. Because Fisher passes both reversal tests it is called the ideal index.',
                'Circular test: an extension of the time reversal test to three or more periods — P01 × P12 × P20 = 1, so the base can be shifted without going back to the original data (e.g. P01 = 1.25 and P12 = 1.20 give P02 = 1.50). Laspeyres, Paasche and Fisher all fail; the simple geometric mean of relatives and the weighted aggregative index with fixed weights pass.'],
             'blocks': [table(['Formula', 'Unit', 'Time reversal', 'Factor reversal', 'Circular'], [
                 ['Simple aggregative', 'No', '—', '—', '—'], ['Laspeyres', 'Yes', 'No', 'No', 'No'], ['Paasche', 'Yes', 'No', 'No', 'No'],
                 ['Fisher', 'Yes', 'Yes', 'Yes', 'No'], ['Simple G.M. of relatives', 'Yes', 'Yes', '—', 'Yes'], ['Fixed-weight aggregative', 'Yes', '—', '—', 'Yes']], title='Which formula passes which test')],
             'analogy': 'The time reversal test asks whether a road map gives the same distance going and returning; the factor reversal test asks whether price change × quantity change explains the whole change in spending.',
             'work': 'When choosing an index for a long-term contract, a consistent formula (one that behaves sensibly forward and backward) prevents arguments when the base is changed.'},
            {'id': 'c9', 'title': 'Uses, limitations, deflating, shifting and splicing', 'body': [
                'Uses: framing economic and business policy; revealing trends and cyclical movements; forecasting (time-series analysis); deflating money values into real terms; measuring changes in the cost of living (and so fixing wages and allowances).',
                'Limitations: built from samples, so errors can creep in; show broad trends, not the exact picture for every person or firm; different formulae give different values, which can confuse.',
                'Deflating: real value = current value ÷ price index × 100. Purchasing power of a rupee = 100 ÷ price index. Nominal GNP deflated by a price index gives real GNP.',
                'Shifting the base: new index = old index ÷ old index of the new base year × 100.',
                'Splicing: when a series is revised (new weights, new items or a new method), the old and new series are joined at the overlap year. To carry the new series back to the old base, multiply it by (old index of the overlap year ÷ 100); to bring the old series to the new base, multiply it by (100 ÷ old index of the overlap year).'],
             'analogy': 'Deflating removes the "price inflation filter" from a photo so you see the real size of the object.',
             'work': 'A salary that rose from ₹36,000 to ₹54,000 while CPI rose from 120 to 180 has not risen in real terms at all — a point CAs make when reviewing pay revisions or pension adequacy.'},
            {'id': 'c10', 'title': 'Stock market indices', 'body': [
                'A stock index tracks the overall market and serves as a benchmark: comparing a share\'s or a fund\'s return with the index shows whether it beat the market.',
                'In India the main indices are the S&P BSE Sensex (30 stocks, base 1978-79 = 100) and the NSE Nifty 50 (50 stocks, base date 3 November 1995, base value 1000). International examples include the Dow Jones, NASDAQ and FTSE.',
                'Computation (market-capitalisation weighting): find each constituent\'s market capitalisation, add them, and roll the index forward: index today = index yesterday × total market cap today ÷ total market cap yesterday. Some indices use price weighting instead, but almost all major equity indices are market-cap weighted.'],
             'analogy': 'An index is the market\'s pulse: one number that summarises how hundreds of hearts (shares) are beating.',
             'work': 'Investment advisers and fund analysts use indices to measure alpha (return above the benchmark); auditors of mutual funds check that the scheme benchmark disclosed matches the offer document.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Simple indices from data set 1', 'difficulty': 'core', 'minutes': 4,
             'q': 'Prices (₹) of four items: A 10 → 12, B 8 → 10, C 5 → 6, D 20 → 25 (base year → current year). Compute (a) the simple aggregative price index and (b) the simple average of price relatives.',
             'solution': [p(f'(a) Σp0 = 10 + 8 + 5 + 20 = 43; Σp1 = 12 + 10 + 6 + 25 = 53. Simple aggregative index = 53/43 × 100 = {agg:.2f}.'),
                          table(['Item', 'p0', 'p1', 'Relative p1/p0 × 100'], [[n, str(p0), str(p1), f2(p1 / p0 * 100)] for n, p0, q0, p1, q1 in D1] + [['Total', '43', '53', f2(sum(p1 / p0 * 100 for _, p0, q0, p1, q1 in D1))]], num=[1, 2, 3], total=True, title='Working'),
                          p(f'(b) Average of relatives = 490 / 4 = {rel_avg}.'),
                          note('The two answers differ because the aggregative method lets the high-priced item D dominate.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Laspeyres, Paasche, Marshall-Edgeworth and Fisher', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'For data set 1 (p0, q0, p1, q1): A (10, 5, 12, 6), B (8, 10, 10, 8), C (5, 8, 6, 10), D (20, 2, 25, 3), compute the Laspeyres, Paasche, Marshall-Edgeworth and Fisher price indices.',
             'solution': [products_table(D1, 'Product table'),
                          ul([f'Laspeyres = Σp1q0 / Σp0q0 × 100 = 258/210 × 100 = {L:.2f}', f'Paasche = Σp1q1 / Σp0q1 × 100 = 287/234 × 100 = {Pa:.2f}',
                              f'Marshall-Edgeworth = (Σp1q0 + Σp1q1) / (Σp0q0 + Σp0q1) × 100 = 545/444 × 100 = {ME:.2f}', f'Fisher = √(258/210 × 287/234) × 100 = {F:.2f}']),
                          note('Fisher always lies between Laspeyres and Paasche (it is their geometric mean).')],
             'checks': c2},
            {'id': 'i3', 'title': 'Fisher satisfies time and factor reversal', 'difficulty': 'hard', 'minutes': 6,
             'q': 'Using the totals of data set 1, show that Fisher\'s index satisfies the time reversal and factor reversal tests.',
             'solution': [p('Time reversal: P01 = √(258/210 × 287/234); P10 interchanges the periods: √(Σp0q1/Σp1q1 × Σp0q0/Σp1q0) = √(234/287 × 210/258).'),
                          p('P01 × P10 = √(258/210 × 287/234 × 234/287 × 210/258) = √1 = 1. Satisfied.'),
                          p(f'Factor reversal: Q01 = √(Σq1p0/Σq0p0 × Σq1p1/Σq0p1) = √(234/210 × 287/258) = {Qf:.2f}%.'),
                          p('P01 × Q01 = √(258/210 × 287/234 × 234/210 × 287/258) = √(287² / 210²) = 287/210 = Σp1q1 / Σp0q0 = V01. Satisfied.'),
                          p(f'Contrast — Laspeyres: P01 × P10 = 258/210 × 234/287 = {lasp_trt} ≠ 1, so Laspeyres fails the time reversal test.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Cost-of-living index by weighted relatives', 'difficulty': 'core', 'minutes': 4,
             'q': 'Group indices and weights: Food 135 (45), Clothing 120 (15), Fuel and light 150 (10), House rent 110 (20), Miscellaneous 125 (10). Compute the cost-of-living index. If a worker earned ₹20,000 in the base period, what should he earn now to maintain the same standard of living?',
             'solution': [table(['Group', 'Group index (R)', 'Weight (W)', 'R × W'], [[g, str(r), str(w), str(r * w)] for g, r, w in COL] + [['Total', '', '100', str(sum(r * w for _, r, w in COL))]], num=[2, 3], total=True, title='Working'),
                          p(f'Cost-of-living index = 12,825 / 100 = {col}.'),
                          p(f'Required income = 20,000 × {col} / 100 = {R(r2(20000 * col / 100))}.')],
             'checks': c4 + [{'expr': '20000*128.25/100', 'value': 25650, 'label': 'income needed to keep the same standard of living'}]},
            {'id': 'i5', 'title': 'Chain-base index from prices', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'Average price (₹) of an item: 2019 – 40, 2020 – 44, 2021 – 55, 2022 – 66, 2023 – 60. Compute chain-base index numbers with 2019 = 100.',
             'solution': [table(['Year', 'Price', 'Link relative', 'Chain index (2019 = 100)'], [[str(y), str(pr), f2(lr), f2(ci)] for y, pr, lr, ci in zip(yrs, price, link, chain)], title='Working'),
                          p('Chain index = link relative × previous chain index ÷ 100, e.g. 2021: 125 × 110 / 100 = 137.50.'),
                          p('Check: fixed-base index for 2023 = 60/40 × 100 = 150 — equal to the chain index, as expected for a single item.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Shifting the base and splicing', 'difficulty': 'moderate', 'minutes': 5,
             'q': '(a) An index (2018 = 100) reads 110, 125, 132, 150 for 2019–2022. Shift the base to 2020. (b) An old series (2015 = 100) reads 108, 115, 120 for 2016–2018; a new series (2018 = 100) reads 105 and 112 for 2019 and 2020. Splice the new series to the old base, and the old series to the new base.',
             'solution': [table(['Year', 'Index (2018 = 100)', 'Shifted (2020 = 100)'], [[str(y), str(v), f2(sv)] for (y, v), (_, sv) in zip(old, shifted)], title='(a) Base shifted to 2020 — divide by 125'),
                          table(['Year', 'Old (2015 = 100)', 'New (2018 = 100)', 'New spliced to 2015 base', 'Old spliced to 2018 base'], [
                              ['2015', '100', '', '', f2(back[0][1])], ['2016', '108', '', '', f2(back[1][1])], ['2017', '115', '', '', f2(back[2][1])], ['2018', '120', '100', '120.00', '100.00'],
                              ['2019', '', '105', f2(fwd[1][1]), '105.00'], ['2020', '', '112', f2(fwd[2][1]), '112.00']], title='(b) Splicing at the overlap year 2018'),
                          p('Forward splicing multiplies the new series by 120/100; backward splicing multiplies the old series by 100/120.')],
             'checks': c6},
            {'id': 'i7', 'title': 'Deflating a salary', 'difficulty': 'core', 'minutes': 3,
             'q': 'A manager\'s monthly salary was ₹36,000 in 2020 and ₹54,000 in 2024. The consumer price index (2016 = 100) was 120 in 2020 and 180 in 2024. Has her real salary changed? What is the purchasing power of a rupee when the CPI is 125?',
             'solution': [p(f'Real salary 2020 = 36,000 × 100/120 = {R(real20)}; real salary 2024 = 54,000 × 100/180 = {R(real24)}.'),
                          p('The money salary rose 50%, but prices also rose 50%: the real salary is unchanged.'),
                          p(f'Purchasing power of a rupee at CPI 125 = 100/125 = ₹{pp:.2f}.')],
             'checks': c7},
            {'id': 'i8', 'title': 'Rolling a market-cap index forward', 'difficulty': 'core', 'minutes': 2,
             'q': 'Yesterday a market index closed at 20,000 when the total market capitalisation of its constituents was ₹4,00,000 crore. Today the total market capitalisation is ₹4,10,000 crore. Find today\'s index value.',
             'solution': [p(f'Index today = 20,000 × 4,10,000 / 4,00,000 = {inr(newidx)}. The 2.5% rise in market capitalisation lifts the index by 2.5%.')],
             'checks': c8},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Price-variation claim under a construction contract', 'role': 'CA advising a contractor', 'situation': 'A contract allows the price of steel work to vary with an official steel price index. The base index (month of bid) was 140; the index for the month of execution is 161. Work done at base rates: ₹50 lakh.',
             'steps': ['Read the clause: which index, which base month, which execution month, and any threshold or cap.', 'Escalation % = (161 − 140) / 140 × 100 = 15%.', 'Escalation amount = ₹50 lakh × 15% = ₹7.5 lakh (before any contractual threshold).', 'Attach the published index values and the computation to the claim.'],
             'takeaway': 'Index arithmetic is simple; the money is in reading the clause correctly and documenting the index values.',
             'checks': [{'expr': '(161-140)/140*100', 'value': 15, 'label': 'escalation %'}, {'expr': '5000000*15/100', 'value': 750000, 'label': 'escalation amount (₹)'}],
             'think': 'If the clause applies only to escalation above 5%, what is the claim?', 'answer': 'Only 10% (15% − 5%) is claimable: ₹5 lakh.'},
            {'id': 'j2', 'title': 'Is the fund beating the market?', 'role': 'CA in an investment advisory firm', 'situation': 'A client\'s equity fund NAV rose from ₹40 to ₹46 over a year; the benchmark index rose from 18,000 to 21,600.',
             'steps': ['Fund return = 46/40 − 1 = 15%.', 'Benchmark return = 21,600/18,000 − 1 = 20%.', 'The fund under-performed its benchmark by 5 percentage points — an important point in the review meeting.'],
             'takeaway': 'An index is the yardstick; a return means little until it is compared with the right index.',
             'checks': [{'expr': '(46/40-1)*100', 'value': 15, 'label': 'fund return %'}, {'expr': '(21600/18000-1)*100', 'value': 20, 'label': 'benchmark return %'}]},
            {'id': 'j3', 'title': 'Real growth in a client\'s revenue', 'role': 'CA preparing a bank CMA / project report', 'situation': 'Revenue grew from ₹2.0 crore to ₹2.4 crore; the relevant price index rose from 125 to 140.',
             'steps': ['Nominal growth = 2.4/2.0 − 1 = 20%.', 'Deflate: real revenue now = 2.4 × 125/140 = ₹2.14 crore (at last year\'s prices).', 'Real growth ≈ 2.14/2.0 − 1 ≈ 7.1% — most of the "growth" was price increase.'],
             'takeaway': 'Deflating separates volume growth from price growth — lenders care about the difference.',
             'checks': [{'expr': 'round(2.4*125/140,2)', 'value': 2.14, 'label': 'real revenue (₹ crore)'}, {'expr': 'round((2.4*125/140/2-1)*100,1)', 'value': 7.1, 'label': 'real growth %'}]},
        ],
        'mcqs': [
            M('m1', 'Data set 1 (Illustration 2): the Laspeyres price index is', [f2(L), f2(Pa), f2(agg), f2(Vi)], 0, "Laspeyres uses base-year quantities as weights: Σp1q0 ÷ Σp0q0 × 100 = 258 ÷ 210 × 100 ≈ 122.86. The trap is 122.65, the Paasche index, which uses current-year quantities (287 ÷ 234). In practice: India's CPI and WPI are Laspeyres-type indices, because base-year weights from a survey can be kept fixed for years.", 'c5', 'moderate', 'round(258/210*100,2)', topic='Weighted aggregative indices'),
            M('m2', 'Data set 1: the Paasche price index is', [f2(Pa), f2(L), '122.50', '110.86'], 0, 'Paasche uses current-year quantities as weights: Σp1q1 ÷ Σp0q1 × 100 = 287 ÷ 234 × 100 ≈ 122.65. The trap is 122.86, the Laspeyres index, which uses base-year quantities. In practice: Paasche needs fresh quantity data every period, which is costly, so statistical agencies use it less often for regular price indices.', 'c5', 'moderate', 'round(287/234*100,2)', topic='Weighted aggregative indices'),
            M('m3', 'Data set 1: the Marshall-Edgeworth price index is', [f2(ME), '122.70', f2(L), '123.26'], 0, 'Marshall-Edgeworth uses the sum of base and current quantities as weights: (Σp1q0 + Σp1q1) ÷ (Σp0q0 + Σp0q1) × 100 = (258 + 287) ÷ (210 + 234) × 100 = 545 ÷ 444 × 100 ≈ 122.75. The trap is 122.86, the Laspeyres index, which uses base-year quantities alone. In practice: such compromise weights reduce the bias of using either period alone.', 'c5', 'moderate', 'round((258+287)/(210+234)*100,2)', topic='Weighted aggregative indices'),
            M('m4', 'Data set 1: the Fisher ideal price index is', [f2(F), '122.80', f2(Pa), '245.51'], 0, "Fisher's index is the geometric mean of Laspeyres and Paasche: √(258/210 × 287/234) × 100 = √(1.2286 × 1.2265) × 100 ≈ 122.75. The trap is 245.51, which adds the two indices instead of taking their geometric mean. In practice: Fisher-type indices are used in national accounts and trade statistics where an unbiased measure of price change matters.", 'c5', 'hard', 'round((258/210*287/234)**0.5*100,2)', topic='Weighted aggregative indices'),
            M('m5', 'Data set 1: the simple aggregative price index is', [f2(agg), '122.50', '122.86', '81.13'], 0, 'Simple aggregative index = Σp1 ÷ Σp0 × 100 = (12 + 10 + 6 + 25) ÷ (10 + 8 + 5 + 20) × 100 = 53 ÷ 43 × 100 ≈ 123.26. The trap is 81.13, which inverts the ratio (43 ÷ 53). In practice: this unweighted method is easy but is distorted by high-priced items and by the units in which prices are quoted.', 'c4', 'core', 'round((12+10+6+25)/(10+8+5+20)*100,2)', topic='Unweighted methods'),
            M('m6', 'Data set 1: the simple average of price relatives is', ['122.50', '123.26', '490', '125'], 0, 'Price relatives (p1 ÷ p0 × 100) are 120, 125, 120 and 125. Their simple average = 490 ÷ 4 = 122.5. The trap is 490, which is the total of the relatives, not the average. In practice: averaging relatives removes the effect of units of quotation, so items priced per kg and per litre can be combined fairly.', 'c4', 'core', '(120+125+120+125)/4', topic='Unweighted methods'),
            M('m7', 'Data set 1: the value index is', [f2(Vi), f2(L), '73.17', '111.43'], 0, "Value index = Σp1q1 ÷ Σp0q0 × 100 = 287 ÷ 210 × 100 ≈ 136.67. It reflects changes in both price and quantity. The trap is 122.86, the Laspeyres price index, which holds quantities constant. In practice: a retailer's sales growth is a value index; splitting it into price and volume effects needs separate price and quantity indices.", 'c5', 'moderate', 'round(287/210*100,2)', topic='Weighted aggregative indices'),
            M('m8', 'Data set 1: the Laspeyres quantity index is', [f2(Lq), f2(Pq), f2(L), '89.74'], 0, 'Laspeyres quantity index uses base-year prices as weights: Σq1p0 ÷ Σq0p0 × 100 = 234 ÷ 210 × 100 ≈ 111.43. The trap is 111.24, the Paasche quantity index (287 ÷ 258). In practice: the Index of Industrial Production in India is a quantity index of this Laspeyres type.', 'c5', 'hard', 'round(234/210*100,2)', topic='Weighted aggregative indices'),
            M('m9', 'Fisher\'s ideal index is the', ['Geometric mean of Laspeyres and Paasche indices', 'Arithmetic mean of Laspeyres and Paasche indices', 'Harmonic mean of Laspeyres and Paasche indices', 'Product of Laspeyres and Paasche indices'], 0, "Fisher's ideal index is the geometric mean of the Laspeyres and Paasche indices: √(L × P). The arithmetic mean is the trap: that would be a different index (Bowley's), not Fisher's. In practice: the geometric mean balances the upward bias of Laspeyres and the downward bias of Paasche, giving a fairer measure of price change.", 'c5', topic='Weighted aggregative indices'),
            M('m10', 'Fisher\'s index is called "ideal" because it satisfies', ['Both the time reversal and factor reversal tests', 'The circular test', 'Only the unit test', 'All four tests'], 0, "Fisher's index is called 'ideal' because it satisfies both the time reversal test and the factor reversal test (as well as the unit test). 'All four tests' is the trap: Fisher does not satisfy the circular test. In practice: satisfying these tests makes Fisher's index consistent when comparing periods both forwards and backwards.", 'c8', topic='Tests of adequacy'),
            M('m11', 'Which of the following satisfies the circular test?', ['Simple geometric mean of price relatives', 'Fisher\'s ideal index', 'Laspeyres index', 'Paasche index'], 0, "The circular test is satisfied by the simple geometric mean of price relatives and by a weighted aggregative index with fixed weights. Fisher's ideal index is the trap: it passes the time and factor reversal tests but fails the circular test, as do Laspeyres and Paasche. In practice: the circular test matters when chaining indices across several years without recomputing from scratch.", 'c8', 'moderate', topic='Tests of adequacy'),
            M('m12', 'Which index does NOT satisfy the unit test?', ['Simple aggregative index', 'Simple average of price relatives', 'Laspeyres index', 'Fisher\'s index'], 0, 'The simple aggregative index adds actual prices, so changing the unit of quotation, such as from per kg to per quintal, changes the result. It therefore fails the unit test. The simple average of price relatives is the trap: relatives are unit-free, so it passes. In practice: this is why official indices never just add up raw prices of different goods.', 'c8', topic='Tests of adequacy'),
            M('m13', 'The time reversal test is expressed as', ['P01 × P10 = 1', 'P01 × Q01 = V01', 'P01 × P12 × P20 = 1', 'P01 + P10 = 1'], 0, 'The time reversal test requires the forward index and the backward index to be reciprocals: P01 × P10 = 1. The trap is P01 × Q01 = V01, which is the factor reversal test. In practice: an index that passes time reversal gives consistent answers whether 2020 is compared with 2025 or 2025 with 2020.', 'c8', topic='Tests of adequacy'),
            M('m14', 'The factor reversal test holds when', ['Price index × quantity index = value index', 'Price index × reversed price index = 1', 'The index does not depend on units', 'The base can be shifted without recomputation'], 0, "The factor reversal test says that the price index multiplied by the corresponding quantity index must equal the value index: P01 × Q01 = Σp1q1 ÷ Σp0q0. 'Price index × reversed price index = 1' is the trap: that is the time reversal test. In practice: passing this test means a company's sales growth can be split exactly into price and volume effects.", 'c8', topic='Tests of adequacy'),
            M('m15', 'With 2020 as base, the 2022 index is 125. With 2022 as base, the 2024 index is 120. If the circular test holds, the 2024 index on base 2020 is', ['150', '145', '245', '104.17'], 0, 'If the circular test holds, indices can be chained: 1.25 × 1.20 = 1.50, so the 2024 index on base 2020 is 150. The trap is 145, which simply adds the percentage rises (25% + 20%) instead of compounding them. In practice: chaining year-on-year price changes is how cumulative inflation over several years is worked out.', 'c8', 'moderate', '125*120/100', topic='Tests of adequacy'),
            M('m16', 'Link relatives for 2022 and 2023 are 110 and 125 (2021 = 100). The chain index for 2023 is', ['137.50', '135', '235', '113.64'], 0, 'Chain index = previous chain index × current link relative ÷ 100. For 2022 it is 110; for 2023 it is 110 × 125 ÷ 100 = 137.5. The trap is 135, which adds the percentage rises (10% + 25%) instead of compounding. In practice: chain-base indices let statistical agencies update item baskets each year while keeping a continuous series.', 'c7', 'moderate', '110*125/100', topic='Chain-base index numbers'),
            M('m17', 'An index (2018 = 100) is 150 for 2022 and 125 for 2020. On base 2020, the 2022 index is', ['120', '125', '187.50', '83.33'], 0, 'To shift the base to 2020, divide every index by the 2020 value and multiply by 100: 150 ÷ 125 × 100 = 120. The trap is 83.33, the inverted ratio (125 ÷ 150). In practice: analysts often rebase a series to a recent year so that changes are easier to read, as RBI and MoSPI do when indices are revised.', 'c9', 'core', '150/125*100', topic='Uses, limitations, deflating, shifting and splicing'),
            M('m18', 'Money wage ₹54,000; consumer price index 180 (base = 100). The real wage is', ['₹30,000', '₹97,200', '₹54,000', '₹36,000'], 0, 'Real wage = money wage × 100 ÷ price index = 54,000 × 100 ÷ 180 = ₹30,000. The trap is ₹97,200, which multiplies by 1.8 and inflates the wage instead of deflating it. In practice: HR and unions compare real wages to see whether pay rises have kept up with CPI inflation, for example in wage-settlement negotiations.', 'c9', 'core', '54000/180*100', topic='Uses, limitations, deflating, shifting and splicing'),
            M('m19', 'If the consumer price index is 125, the purchasing power of a rupee is', ['₹0.80', '₹1.25', '₹0.25', '₹1.80'], 0, 'Purchasing power of a rupee = 100 ÷ price index = 100 ÷ 125 = ₹0.80. In other words, a rupee now buys what 80 paise bought in the base period. The trap is ₹1.25, which is the index ÷ 100 and shows the rise in prices, not purchasing power. In practice: savers use this to see how inflation erodes the real value of money kept in cash or low-interest deposits.', 'c9', 'core', '100/125', topic='Uses, limitations, deflating, shifting and splicing'),
            M('m20', 'Group indices and weights: Food 135 (45), Clothing 120 (15), Fuel 150 (10), Rent 110 (20), Others 125 (10). The cost-of-living index is', ['128.25', '128', '640', '125'], 0, 'Cost-of-living index = Σ(I × W) ÷ ΣW = (135 × 45 + 120 × 15 + 150 × 10 + 110 × 20 + 125 × 10) ÷ 100 = 12,825 ÷ 100 = 128.25. The trap is 128, the simple average of the five indices, which ignores the weights. In practice: dearness allowance for government employees is linked to the CPI, which is built from weighted group indices like these.', 'c6', 'moderate', '(135*45+120*15+150*10+110*20+125*10)/100', topic='Weighted average of relatives'),
            M('m21', 'A market-cap weighted index closed at 20,000 yesterday when total market cap was ₹4,00,000 crore. Today market cap is ₹4,10,000 crore. Today\'s index is', ['20,500', '20,250', '21,000', '19,512'], 0, 'A market-cap weighted index moves in proportion to total market capitalisation: 20,000 × 4,10,000 ÷ 4,00,000 = 20,500. The trap is 21,000, a 5% rise, whereas market cap rose only 2.5%. In practice: indices like the Nifty 50 and Sensex are computed on free-float market capitalisation in this way.', 'c10', 'core', '20000*410000/400000', topic='Stock market indices'),
            M('m22', 'A base period for an index number should be', ['Normal and reasonably recent', 'A year of unusually high prices', 'As far back in the past as possible', 'Any year, it does not matter'], 0, "The base period is the reference point for every comparison, so it should be a normal year, free of unusual events, and reasonably recent. 'A year of unusually high prices' is the trap: an abnormal base makes later indices look misleadingly low. In practice: MoSPI revises the base year of India's CPI from time to time so that the base stays relevant.", 'c2', topic='Issues in constructing an index'),
            M('m23', 'The Laspeyres price index uses as weights', ['Base-year quantities', 'Current-year quantities', 'The average of base and current quantities', 'Equal weights'], 0, "Laspeyres weights prices by base-year quantities: Σp1q0 ÷ Σp0q0. Current-year quantities is the trap: those are Paasche's weights. In practice: because base-year quantities need to be surveyed only once, most official consumer price indices, including India's CPI, follow the Laspeyres approach.", 'c5', topic='Weighted aggregative indices'),
            M('m24', 'The Paasche price index uses as weights', ['Current-year quantities', 'Base-year quantities', 'Base-year prices', 'Typical-period quantities'], 0, 'Paasche weights prices by current-year quantities: Σp1q1 ÷ Σp0q1. Base-year quantities is the trap: those are the Laspeyres weights. In practice: Paasche-type deflators, like the GDP deflator, reflect what is actually being bought now and are derived from national accounts.', 'c5', topic='Weighted aggregative indices'),
            M('m25', 'The price of a commodity rose from ₹40 in the base year to ₹50. Its price relative is', ['125', '80', '25', '150'], 0, 'Price relative = p1 ÷ p0 × 100 = 50 ÷ 40 × 100 = 125. The trap is 25, which is the percentage rise, not the relative. 80 is the inverted relative (40 ÷ 50). In practice: price relatives are the building blocks of indices and are used for comparing cost increases in procurement contracts with price-variation clauses.', 'c3', 'core', '50/40*100', topic='Relatives — price, quantity, value, link and chain'),
            M('m26', 'Laspeyres index = 125 and Paasche index = 121. Fisher\'s index is', ['122.98', '123.00', '246', '121.50'], 0, "Fisher's index = √(Laspeyres × Paasche) = √(125 × 121) = √15,125 ≈ 122.98. The trap is 123, the arithmetic mean of 125 and 121; the geometric mean is always slightly lower. In practice: Fisher's index is used where neither base nor current weights should dominate, such as in some trade price statistics.", 'c5', 'hard', 'round((125*121)**0.5,2)', topic='Weighted aggregative indices'),
            M('m27', 'The value index is 150 and Fisher\'s price index is 125. By the factor reversal test, Fisher\'s quantity index is', ['120', '187.50', '25', '83.33'], 0, 'By the factor reversal test, P × Q = V, so Q = V ÷ P × 100 = 150 ÷ 125 × 100 = 120. The trap is 187.50, which multiplies 150 × 125 ÷ 100 instead of dividing. In practice: splitting growth in sales value into price and volume, here a 25% price effect and a 20% volume effect, is standard in business performance analysis.', 'c8', 'hard', '150/125*100', topic='Tests of adequacy'),
            M('m28', 'An old series (2015 = 100) stands at 120 in 2018, where a new series (2018 = 100) begins. The new series is 105 in 2019. Spliced to the 2015 base, the 2019 figure is', ['126', '87.50', '105', '225'], 0, 'Splicing converts the new series to the old base by multiplying by the old index at the link year: 105 × 120 ÷ 100 = 126. The trap is 225, which adds 105 and 120 instead of multiplying. In practice: when MoSPI revises the CPI base, economists splice the old and new series to get one continuous inflation history.', 'c9', 'moderate', '105*120/100', topic='Uses, limitations, deflating, shifting and splicing'),
            M('m29', 'The average theoretically most suitable for averaging relatives is the', ['Geometric mean', 'Arithmetic mean', 'Harmonic mean', 'Mode'], 0, 'The geometric mean treats proportional rises and falls symmetrically and makes an index time-reversible, so it is theoretically the best average for relatives. The arithmetic mean is the trap: it is often used for simplicity, but it has an upward bias. In practice: many modern consumer price indices use geometric means at the elementary level for this reason.', 'c2', 'moderate', topic='Issues in constructing an index'),
            M('m30', 'The test described as an extension of the time reversal test is the', ['Circular test', 'Factor reversal test', 'Unit test', 'Chain test'], 0, 'The circular test extends the time reversal test from two periods to three or more: P01 × P12 × P20 = 1. The factor reversal test is the trap: it concerns price and quantity, not a cycle of periods. In practice: passing the circular test means indices for consecutive years can be chained without any inconsistency.', 'c8', 'moderate', topic='Tests of adequacy'),
            M('m31', 'The base value of the NSE Nifty 50 index is', ['1000', '100', '500', '10000'], 0, 'The NSE Nifty 50 has a base value of 1,000, with a base date of 3 November 1995. The trap is 100, which is the base value of the BSE Sensex (1978-79 = 100). In practice: knowing the base helps interpret long-term returns; a Nifty level of 25,000 means the index has risen 25-fold since 1995.', 'c10', 'core', '1000', topic='Stock market indices'),
            M('m32', 'Which of the following is a limitation of index numbers?', ['Different formulae give different values for the same data', 'They cannot be used for forecasting', 'They can measure only prices', 'They cannot compare two places'], 0, "Index numbers are approximations: they are based on samples of items, and different formulae (Laspeyres, Paasche, Fisher) give different values for the same data. 'They can measure only prices' is the trap: quantity and value indices also exist. In practice: debates over whether official inflation figures reflect real household costs arise from exactly these limitations.", 'c9', topic='Uses, limitations, deflating, shifting and splicing'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
             'q': 'From the data below compute Fisher\'s ideal price index and show that it satisfies the time reversal and factor reversal tests. (p0, q0, p1, q1): X (6, 10, 9, 8), Y (4, 15, 5, 20), Z (10, 5, 12, 6).',
             'model': [products_table(D3, 'Product table'),
                       p(f'Laspeyres = 225/170 × 100 = {qL:.2f}; Paasche = 244/188 × 100 = {qP:.2f}.'),
                       p(f'Fisher P01 = √(225/170 × 244/188) × 100 = {qF:.2f}.'),
                       p('Time reversal: P10 = √(188/244 × 170/225); P01 × P10 = √(225/170 × 244/188 × 188/244 × 170/225) = 1. Satisfied.'),
                       p('Factor reversal: Q01 = √(Σq1p0/Σq0p0 × Σq1p1/Σq0p1) = √(188/170 × 244/225). P01 × Q01 = √(225/170 × 244/188 × 188/170 × 244/225) = √(244²/170²) = 244/170 = Σp1q1/Σp0q0. Satisfied.')],
             'scheme': [{'id': 's1', 'pt': 'Product table with all four totals (170, 225, 188, 244)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Fisher index 131.06 (via Laspeyres and Paasche)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Time reversal: P10 formed correctly and product = 1', 'm': 1.5, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'Factor reversal: Q01 formed and product = V01', 'm': 1.5, 'skill': 'analysis'}],
             'remarks': ['Most marks are lost in P10 and Q01 — candidates interchange the wrong symbols.', 'Keep the indices as ratios (not × 100) while proving the tests.'],
             'mistakes': ['Writing P10 as 1/P01 directly (that assumes what is to be proved).', 'Taking Q01 with prices and quantities in the wrong places.'],
             'tips': ['Label the four totals once and refer to them by symbol in every formula.', 'In the MCQ paper, test-related questions are usually theory: remember the "which formula passes which test" table.'],
             'checks': cq1},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'The price (₹) of an item over five years was 500, 550, 660, 594 and 653.40. Compute link relatives and chain-base index numbers (Year 1 = 100), and verify the last chain index with the fixed-base method.',
             'model': [table(['Year', 'Price', 'Link relative', 'Chain index'], [[str(i + 1), str(pr), f2(lr), f2(ci)] for i, (pr, lr, ci) in enumerate(zip(qprice, qlink, qchain))], title='Working'),
                       p('Fixed-base check for Year 5: 653.40/500 × 100 = 130.68 — equal to the chain index.')],
             'scheme': [{'id': 's1', 'pt': 'Link relatives 110, 120, 90, 110', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Chain indices 110, 132, 118.80, 130.68', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Fixed-base verification', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['A neat four-column table earns full marks quickly.'], 'mistakes': ['Multiplying link relatives without dividing by 100.', 'Taking the link relative of Year 4 as 594/500 instead of 594/660.'],
             'tips': ['A fall in price gives a link relative below 100 — the chain index then falls too.'],
             'checks': cq2},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'A clerk\'s monthly wage was ₹48,000 in 2022 and ₹56,000 in 2024. The CPI (2016 = 100) was 112 in 2022 and 140 in 2024. (a) Shift the 2024 CPI to base 2022. (b) Compute the real wage of each year at 2016 prices. (c) Did the clerk\'s real wage rise or fall, and by what percentage?',
             'model': [p('(a) 2024 CPI on base 2022 = 140/112 × 100 = 125.'),
                       p(f'(b) Real wage 2022 = 48,000 × 100/112 = {R(rw22)}; real wage 2024 = 56,000 × 100/140 = {R(rw24)}.'),
                       p('(c) Change = (40,000 − 42,857.14)/42,857.14 × 100 = −6.67%. The real wage fell by about 6.67%, although the money wage rose by 16.67%.')],
             'scheme': [{'id': 's1', 'pt': 'Base shifted: 125', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Real wage 2022', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Real wage 2024', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Conclusion: real wage fell 6.67%', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['The point of the question is the conclusion — a money rise can be a real fall.'], 'mistakes': ['Multiplying by the index instead of dividing.', 'Comparing money wages only.'],
             'tips': ['Deflating always divides by the index (× 100).'],
             'checks': cq3},
        ],
        'revision': {
            'summary': ['Index number = relative change vs a base (= 100); a specialised average of relatives. Simple (one variable) or composite (many).',
                        'Construction issues: purpose and data (representative sample), base (normal, recent), weights, average (G.M. best, A.M. common), variables, formula.',
                        'Relatives: price p1/p0, quantity q1/q0, value p1q1/p0q0 (× 100); link (vs previous period) and chain (vs fixed base).',
                        'Simple aggregative Σp1/Σp0 (fails unit test); simple average of relatives (equal weights).',
                        'Laspeyres Σp1q0/Σp0q0; Paasche Σp1q1/Σp0q1; Marshall-Edgeworth Σp1(q0+q1)/Σp0(q0+q1); Fisher √(L × P). Quantity indices swap p and q; value index Σp1q1/Σp0q0.',
                        'Weighted average of relatives Σ RW / ΣW (base-value weights → Laspeyres); used for cost-of-living indices.',
                        'Chain index = link relative × previous chain index / 100.',
                        'Tests: unit (all but simple aggregative); time reversal P01 × P10 = 1 and factor reversal P01 × Q01 = V01 (Fisher only → ideal); circular (fixed-weight aggregative, simple G.M. of relatives; not L, P or F).',
                        'Deflating: real = money ÷ index × 100; shifting base: ÷ index of new base × 100; splicing at the overlap year.',
                        'Stock index: today = yesterday × today\'s market cap / yesterday\'s market cap. Sensex 30 stocks, base 1978-79 = 100; Nifty 50 stocks, base 3 Nov 1995 = 1000.'],
            'remember': ['Fisher always lies between Laspeyres and Paasche.', 'Use ratios (not percentages) when proving the tests.', 'Purchasing power of a rupee = 100 / price index.'],
            'traps': ['Calling Laspeyres "current-year weights".', 'Saying Fisher satisfies the circular test.', 'Multiplying by the price index when deflating.', 'Forgetting to divide by 100 when chaining link relatives.']},
        'quickref': [{'k': 'Laspeyres', 'v': 'Σp1q0 / Σp0q0 × 100'}, {'k': 'Paasche', 'v': 'Σp1q1 / Σp0q1 × 100'}, {'k': 'Marshall-Edgeworth', 'v': 'Σp1(q0+q1) / Σp0(q0+q1) × 100'},
                     {'k': 'Fisher', 'v': '√(Laspeyres × Paasche)'}, {'k': 'Value index', 'v': 'Σp1q1 / Σp0q0 × 100'}, {'k': 'Weighted relatives', 'v': 'Σ(R × W) / ΣW'},
                     {'k': 'Chain index', 'v': 'LR(current) × CI(previous) / 100'}, {'k': 'Time reversal', 'v': 'P01 × P10 = 1'}, {'k': 'Factor reversal', 'v': 'P01 × Q01 = Σp1q1 / Σp0q0'},
                     {'k': 'Circular', 'v': 'P01 × P12 × P20 = 1'}, {'k': 'Deflated value', 'v': 'Current value / price index × 100'}, {'k': 'Shifted index', 'v': 'Old index / old index of new base × 100'}],
        'viva': [
            V('v1', 'What is an index number?',
              'An index number is a statistical measure of the relative change in a variable or a group of variables, such as prices or quantities, between a base period and another period or place. The base is taken as one hundred, so it is expressed as a percentage, and it is a specialised average of relatives.',
              [P('p1', 'Measures relative (percentage) change', 4, 'relative|percentage|proportion|ratio|change'),
               P('p2', 'Compared with a base period / place taken as 100', 4, 'base', '100|hundred'),
               P('p3', 'A specialised average of relatives / group of variables', 2, 'average|group|composite|several|many|set of')], 'c1'),
            V('v2', 'What is the difference between the Laspeyres and the Paasche price index?',
              'Laspeyres uses base year quantities as weights, so it is sum of p1 q0 over sum of p0 q0. Paasche uses current year quantities as weights, so it is sum of p1 q1 over sum of p0 q1.',
              [P('p1', 'Laspeyres: base-year quantities as weights', 5, 'laspeyres base|laspeyres uses base|laspeyres index base|laspeyres weights base|laspeyre base|laspeyres takes base|laspeyres is base|laspeyres based on base|laspeyres q0|laspeyres q 0|laspeyres quantities base'),
               P('p2', 'Paasche: current-year quantities as weights', 5, 'paasche current|paasche uses current|paasche index current|paasche weights current|paasches current|paasche takes current|paasche is current|paasche based on current|paasche q1|paasche q 1|paasche quantities current|paasche given year')], 'c5'),
            V('v3', 'Why is Fisher\'s index called the ideal index?',
              'Fisher\'s index is the geometric mean of the Laspeyres and Paasche indices, and it satisfies both the time reversal test and the factor reversal test. That is why it is called ideal, although it does not satisfy the circular test.',
              [P('p1', 'Geometric mean of Laspeyres and Paasche', 3, 'geometric|gm|square root|root of', 'laspeyres|paasche|both', min=2),
               P('p2', 'Satisfies the time reversal test', 3, 'time reversal|time revers'),
               P('p3', 'Satisfies the factor reversal test', 3, 'factor reversal|factor revers'),
               P('p4', 'Does not satisfy the circular test', 1, 'not circular|not the circular|not satisfy circular|not satisfy the circular|fails circular|fails the circular|does not pass circular|circular not|circular test is not|not meet circular|not meet the circular|except circular|except the circular')], 'c8'),
            V('v4', 'State the time reversal and factor reversal tests.',
              'The time reversal test says the index for period one on base zero multiplied by the index for period zero on base one should equal one, P01 into P10 equals one. The factor reversal test says the price index multiplied by the quantity index should equal the value index, that is sum of p1 q1 over sum of p0 q0.',
              [P('p1', 'Time reversal: P01 × P10 = 1', 5, 'time', 'p01|p 01|p zero one|p0 1|forward', 'p10|p 10|p one zero|p1 0|backward|reverse|recipro', '1|one|unity|recipro', min=3),
               P('p2', 'Factor reversal: price index × quantity index = value index', 5, 'factor', 'price index', 'quantity index', 'value index|value|v01')], 'c8'),
            V('v5', 'How do you compute a chain base index, and when is it useful?',
              'First compute link relatives, each year\'s price divided by the previous year\'s price times one hundred. Then the chain index equals the link relative of the current year multiplied by the chain index of the previous year divided by one hundred. It is useful when items or weights change often, but an error in one link carries forward to all later years.',
              [P('p1', 'Link relative = current ÷ previous × 100', 3, 'link relative', 'previous|preceding|last year|year before|prior'),
               P('p2', 'Chain index = LR × previous chain index ÷ 100', 4, 'chain index|chain', 'multipl|product|times'),
               P('p3', 'Useful when items/weights change; errors carry forward', 3, 'change|new item|new commodit|weights chang|basket chang|error|carr|forward', min=1)], 'c7'),
            V('v6', 'How do you deflate a money value, and why?',
              'Divide the current money value by the price index of that year and multiply by one hundred. This removes the effect of price changes and gives the real value at base year prices, for example converting money wages into real wages.',
              [P('p1', 'Divide by the price index and multiply by 100', 5, 'divid|divided|over|ratio', 'index|cpi|price level', min=2),
               P('p2', 'Removes price effect — real value at base prices (e.g. real wages)', 5, 'real|constant price|base year price|purchasing power|remove|eliminat|adjust|inflation')], 'c9'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Indore Mart — household basket', 'difficulty': 'hard',
            'case': 'A retail chain tracks a three-item household basket. Base year (p0, q0) and current year (p1, q1): Rice per kg (₹40, 50 kg; ₹46, 45 kg), Oil per litre (₹120, 10 litres; ₹150, 9 litres), Sugar per kg (₹36, 20 kg; ₹40, 25 kg).',
            'given': [products_table(D2, 'Product table (computed for you)')],
            'mcqs': [
                M('k1a', 'The Laspeyres price index is', [f2(kL), f2(kP), f2(kV), '121.69'], 0, 'Laspeyres = Σp1q0 ÷ Σp0q0 × 100. Σp0q0 = 2,000 + 1,200 + 720 = 3,920; Σp1q0 = 2,300 + 1,500 + 800 = 4,600. Index = 4,600 ÷ 3,920 × 100 ≈ 117.35. The trap is 116.93, the Paasche index, which uses current quantities. In practice: retailers track basket inflation this way to set prices and to compare with the official CPI.', 'c5', 'moderate', 'round(4600/3920*100,2)', topic='Weighted aggregative indices'),
                M('k1b', 'The Paasche price index is', [f2(kP), f2(kL), '96.43', '120.00'], 0, 'Paasche = Σp1q1 ÷ Σp0q1 × 100. Σp0q1 = 1,800 + 1,080 + 900 = 3,780; Σp1q1 = 2,070 + 1,350 + 1,000 = 4,420. Index = 4,420 ÷ 3,780 × 100 ≈ 116.93. The trap is 117.35, the Laspeyres index. In practice: Paasche reflects the shift towards sugar and away from oil, showing how buying habits change when prices rise.', 'c5', 'moderate', 'round(4420/3780*100,2)', topic='Weighted aggregative indices'),
                M('k1c', 'Fisher\'s ideal price index is', [f2(kF), '117.20', '234.28', '116.00'], 0, "Fisher's index = √(Laspeyres × Paasche) = √(1.1735 × 1.1693) × 100 ≈ 117.14. The trap is 234.28, which adds the two indices instead of taking their geometric mean. In practice: Fisher's index lies between the other two and is used where a balanced, unbiased measure of price change is needed.", 'c5', 'hard', 'round((4600/3920*4420/3780)**0.5*100,2)', topic='Weighted aggregative indices'),
                M('k1d', 'The value index is', [f2(kV), '88.69', f2(kL), '96.43'], 0, 'Value index = Σp1q1 ÷ Σp0q0 × 100 = 4,420 ÷ 3,920 × 100 ≈ 112.76. Spending rose less than prices because the family bought less rice and oil. The trap is 117.35, the Laspeyres price index, which holds quantities fixed. In practice: comparing value and price indices tells a business whether revenue growth came from price or from volume.', 'c5', 'moderate', 'round(4420/3920*100,2)', topic='Weighted aggregative indices'),
            ]}],
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
        's1': _N(170, 225, 188, 244),
        's2': _N(131.06),
        's3': _K('p10|188 244 170 225', 'p01 p10 1|p01 x p10 1|product 1|equals 1|equal 1|170 225 1|unity'),
        's4': _K('q01|188 170 244 225', 'v01|244 170|p1q1 p0q0|value index'),
    },
    'q2': {
        's1': _N(110, 120, 90),
        's2': _N(132, 118.8, 130.68),
        's3': _K('653.4 500|653.4 x 100 500|653.4 100 500', nums=[130.68]),
    },
    'q3': {
        's1': _N(125),
        's2': _N(42857.14),
        's3': _N(40000),
        's4': _K('fell|fall|decreas|declin|reduc|lower|down', nums=[6.67]),
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
