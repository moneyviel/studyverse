"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 13 Unit 1 Statistical Description of Data.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as _CM


def CM(*a, topic=None, **k):
    d = _CM(*a, **k); d['topic'] = topic
    return d

UID = 'fnd-p3-ch13-u01'


def ev(expr): return eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})


class Checks(Checks):
    """Records the check as lib.Checks does (value stored to 2 decimals), but returns the value to 4 decimals for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = round(ev(expr), 4)
        return int(v) if v == int(v) else v


def fm(v, unit=''):
    v = round(v, 2)
    s = inr(int(v)) if v == int(v) else (f'{v:.2f}'.rstrip('0').rstrip('.'))
    return s + (' ' + unit if unit else '')


def mq(mid, q, opts, explain, concept, diff='core', topic=None):
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit='', topic=None):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def build():
    # ---------------- Illustration 1: grouped marks, all the terms ----------------
    c1 = Checks()
    lim = [(10, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69)]
    f1 = [4, 7, 12, 15, 8, 4]
    N1 = c1.add('+'.join(map(str, f1)), 'total frequency')
    rows1, lt, cum = [], [], 0
    for (a, b), f in zip(lim, f1):
        lcb, ucb = a - 0.5, b + 0.5
        mid = c1.add(f'({a}+{b})/2', f'mid-value of {a}-{b}')
        cum += f
        rows1.append([f'{a}–{b}', f'{lcb}–{ucb}', fm(mid), str(f), fm(f / N1), fm(f / 10), str(cum), str(N1 - cum + f)])
    c1.add('4+7+12', 'less-than cumulative frequency up to 39.5')
    c1.add('50-4-7', 'more-than cumulative frequency from 29.5')
    c1.add('15/50', 'relative frequency of 40-49')
    rows1.append(['Total', '', '', str(N1), '1', '', '', ''])
    t1 = table(['Marks (class limits)', 'Class boundaries', 'Mid-value', 'Frequency (f)', 'Relative frequency', 'Frequency density (f ÷ 10)', 'Less-than c.f. (up to UCB)', 'More-than c.f. (from LCB)'],
               rows1, num=[3, 4], total=True, title='Marks of 50 students in a practice test')

    # ---------------- Illustration 2: pie chart ----------------
    c2 = Checks()
    items2 = [('Raw material', 48), ('Wages', 30), ('Power and fuel', 18), ('Administration', 12), ('Profit', 12)]
    T2 = c2.add('48+30+18+12+12', 'total of ₹ lakh')
    rows2 = []
    for nm, x in items2:
        ang = c2.add(f'{x}/{T2}*360', f'angle for {nm}')
        rows2.append([nm, str(x), fm(x / T2 * 100), fm(ang)])
    rows2.append(['Total', str(T2), '100', '360'])
    t2 = table(['Item', '₹ lakh', 'Share (%)', 'Angle (degrees)'], rows2, num=[1, 2, 3], total=True, title='How each ₹120 lakh of sales revenue of Neelgiri Foods is used')

    # ---------------- Illustration 3: percentage bar diagram ----------------
    c3 = Checks()
    y1 = [('A', 60), ('B', 90), ('C', 50)]; y2 = [('A', 84), ('B', 105), ('C', 61)]
    s1 = c3.add('60+90+50', 'sales 2025'); s2 = c3.add('84+105+61', 'sales 2026')
    rows3 = []
    for (nm, a), (_, b) in zip(y1, y2):
        pa = c3.add(f'{a}/{s1}*100', f'{nm} share 2025'); pb = c3.add(f'{b}/{s2}*100', f'{nm} share 2026')
        rows3.append([f'Product {nm}', str(a), fm(pa), str(b), fm(pb)])
    rows3.append(['Total', str(s1), '100', str(s2), '100'])
    t3 = table(['Product', '2025 (₹ lakh)', '2025 %', '2026 (₹ lakh)', '2026 %'], rows3, num=[1, 2, 3, 4], total=True, title='Product-wise sales and percentage shares')

    # ---------------- Illustration 4: histogram with unequal classes ----------------
    c4 = Checks()
    cls4 = [(0, 10, 5), (10, 20, 12), (20, 40, 24), (40, 70, 18), (70, 100, 6)]
    rows4 = []
    for a, b, f in cls4:
        w = b - a
        d = c4.add(f'{f}/{w}', f'density {a}-{b}')
        h = c4.add(f'{f}/{w}*10', f'height on standard width 10 for {a}-{b}')
        rows4.append([f'{a}–{b}', str(w), str(f), fm(d), fm(h)])
    c4.add('5+12+24+18+6', 'total frequency')
    rows4.append(['Total', '', '65', '', ''])
    t4 = table(['Days outstanding', 'Width', 'No. of invoices (f)', 'Frequency density', 'Adjusted height (per 10 days)'], rows4, num=[2], total=True)

    # ---------------- Question 1: raw data -> frequency distribution ----------------
    q1c = Checks()
    raw = [23, 37, 41, 28, 33, 45, 26, 39, 31, 48, 22, 35, 29, 44, 36, 27, 40, 34, 38, 25, 42, 30, 47, 32, 36, 24, 43, 39, 33, 29]
    assert len(raw) == 30
    rng = q1c.add(f'{max(raw)}-{min(raw)}', 'range')
    k = q1c.add(f'-(-{rng}//5)', 'number of classes = next integer of range/5')
    bins = [(20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50)]
    cnt = [sum(1 for x in raw if a <= x < b) for a, b in bins]
    assert sum(cnt) == 30
    q1c.add('+'.join(map(str, cnt)), 'total of frequencies equals 30 observations')
    tally = lambda n: ' '.join(['IIII/'] * (n // 5) + (['I' * (n % 5)] if n % 5 else []))
    rows_q1 = [[f'{a}–{b}', tally(n), str(n)] for (a, b), n in zip(bins, cnt)] + [['Total', '', str(sum(cnt))]]
    tq1 = table(['Age (years)', 'Tally marks', 'No. of employees'], rows_q1, num=[2], total=True, title='Ages of 30 employees of Vardhan Logistics')

    # ---------------- Question 2: pie chart ----------------
    q2c = Checks()
    it2 = [('Food', 13500), ('Rent', 9000), ('Education', 6000), ('Transport', 3600), ('Savings', 3900)]
    T = q2c.add('13500+9000+6000+3600+3900', 'monthly income')
    rows_q2 = []
    for nm, x in it2:
        a = q2c.add(f'{x}/{T}*360', f'angle {nm}')
        rows_q2.append([nm, inr(x), fm(a)])
    rows_q2.append(['Total', inr(T), '360'])
    tq2 = table(['Head', 'Amount (₹)', 'Angle (degrees)'], rows_q2, num=[1, 2], total=True)

    # ---------------- Question 3: inclusive classes, c.f., ogive location ----------------
    q3c = Checks()
    lim3 = [(100, 199), (200, 299), (300, 399), (400, 499), (500, 599)]
    f3 = [6, 14, 22, 12, 6]
    N3 = q3c.add('6+14+22+12+6', 'total frequency')
    rows_q3, cum = [], 0
    for (a, b), f in zip(lim3, f3):
        cum += f
        rows_q3.append([f'{a}–{b}', f'{a - 0.5}–{b + 0.5}', fm((a + b) / 2), str(f), str(cum), str(N3 - cum + f)])
    rows_q3.append(['Total', '', '', str(N3), '', ''])
    half = q3c.add('60/2', 'N/2, where the two ogives cross')
    q3c.add('6+14', 'less-than c.f. at 299.5')
    q3c.add('6+14+22', 'less-than c.f. at 399.5')
    tq3 = table(['Units sold (limits)', 'Class boundaries', 'Mid-value', 'No. of days (f)', 'Less-than c.f.', 'More-than c.f.'], rows_q3, num=[3], total=True)

    # ---------------- Case ----------------
    kc = Checks()
    k_tot = kc.add('8+20+32+25+15', 'total shops')
    k_ang = kc.add('32/100*360', 'pie angle for 30-39 class')
    cases = [{
        'id': 'k1', 'title': 'Sales-per-shop data for a distributor', 'difficulty': 'moderate',
        'case': ('Amrit Distributors supplies 100 retail shops. Its analyst groups the number of cartons each shop bought in October into the classes 10–19, 20–29, 30–39, 40–49 and 50–59, '
                 'with 8, 20, 32, 25 and 15 shops respectively. She wants a table for the management report, an ogive to read off the middle shop, and a pie chart for the board deck.'),
        'mcqs': [
            CM('k1a', 'What are the class boundaries of the class 30–39?', ['29.5 and 39.5', '30 and 39', '30 and 40', '29 and 40'], 0,
               'The classes 10–19, 20–29, 30–39 are inclusive with a gap of 1 between them. Subtract and add half the gap: 30 − 0.5 = 29.5 and 39 + 0.5 = 39.5. The trap is 30 and 39, which are the class limits, not boundaries. In practice: using boundaries ensures every carton count, even if averaged to 29.6, falls into exactly one class.', 'core', topic='Frequency distribution and its terms'),
            CM('k1b', 'What is the less-than cumulative frequency at 39.5?', ['60', '32', '72', '40'], 0,
               'The less-than cumulative frequency at 39.5 counts all shops in the classes up to 30–39: 8 + 20 + 32 = 60. The trap is 32, the frequency of the class 30–39 alone, not the cumulative figure. In practice: running totals like this are how a distributor sees, for example, that 60% of shops bought fewer than 40 cartons.', 'core', '8+20+32', topic='Frequency distribution and its terms'),
            CM('k1c', 'If the two ogives are drawn, at what cumulative frequency will they cross?', ['50', '100', '60', '25'], 0,
               "The less-than and more-than ogives always cross at half the total frequency. With 100 shops, that is 100 ÷ 2 = 50; the x-value there is the median. The trap is 100, the total, where one ogive ends rather than where they meet. In practice: the median shop's purchase is a fairer 'typical' figure than the mean if a few large shops buy far more.", 'moderate', '100/2', topic='Graphs of a frequency distribution'),
            CM('k1d', 'In the pie chart, what angle represents the shops in the class 30–39?', ['115.2 degrees', '32 degrees', '120 degrees', '96 degrees'], 0,
               'A pie-chart angle = (class frequency ÷ total) × 360. For 30–39: 32 ÷ 100 × 360 = 115.2 degrees. The trap is 32 degrees, which uses the frequency itself as the angle. In practice: board decks often present the customer base as a pie chart, and every slice must be calculated this way to be accurate.', 'moderate', '32/100*360', topic='Diagrams: line, bar and pie'),
        ]}]

    viva = [
        V('v1', 'What is the difference between primary data and secondary data?',
          'Primary data are collected for the first time by the investigator himself for his own purpose, so they are original. Secondary data are data that were already collected by someone else and are only used by the investigator, for example from published government reports. The same data are primary for the one who collected them and secondary for anyone who later uses them.',
          [P('p1', 'Primary data: collected first-hand / for the first time by the investigator', 4, ALT('primary {d}', d=('first time', 'first hand', 'firsthand', 'original', 'himself', 'herself', 'ourselves', 'own', 'fresh', 'directly', 'investigator', 'first'))),
           P('p2', 'Secondary data: already collected by someone else and only used', 4, ALT('secondary {d}', d=('someone else', 'somebody else', 'other', 'another', 'already', 'published', 'existing', 'second hand', 'earlier', 'previously', 'collected by others'))),
           P('p3', 'Same data can be primary for one user and secondary for another', 2, 'same data|same|one person|depend|relative|for anyone|for another|later', min=1)], 'c3'),
        V('v2', 'Name the methods of collecting primary data. Which method usually suffers the most non-response?',
          'Primary data can be collected by the interview method, which may be personal, indirect or telephone interview, by the mailed questionnaire method, by direct observation, and through questionnaires filled in by enumerators. The mailed questionnaire method usually has the maximum non-response.',
          [P('p1', 'Interview method (personal, indirect, telephone)', 3, 'interview'),
           P('p2', 'Mailed questionnaire', 2, 'mail|post|questionnaire sent|questionnaire'),
           P('p3', 'Observation', 2, 'observ'),
           P('p4', 'Mailed questionnaire has maximum non-response', 3, ALT('{m} {x}', '{x} {m}', m=('mail', 'mailed questionnaire', 'postal'), x=('maximum non response', 'most non response', 'highest non response', 'maximum nonresponse', 'most nonresponse', 'maximum non-response', 'most non-response', 'non response maximum', 'non response highest', 'non response most', 'non response is maximum', 'non response is highest', 'least response', 'lowest response', 'most people do not reply', 'many do not reply')))], 'c3'),
        V('v3', 'What are the main parts of a statistical table?',
          'A table has a table number and a clear title. The caption gives the headings of the columns, and the box-head is the whole upper part with the column headings and units. The stub is the left part that describes the rows. The body holds the figures. Footnotes and the source note come at the bottom.',
          [P('p1', 'Table number and title', 2, 'title|number|heading', min=1),
           P('p2', 'Caption / box-head: column headings', 3, ALT('{c} {x}', c=('caption', 'box head', 'boxhead'), x=('column', 'heading', 'top', 'upper'))),
           P('p3', 'Stub: row descriptions on the left', 3, ALT('stub {x}', x=('row', 'left'))),
           P('p4', 'Body holds the figures; footnote / source at the bottom', 2, 'body', 'footnote|foot note|source|bottom', min=1)], 'c5'),
        V('v4', 'How do class limits differ from class boundaries, and how do you get boundaries from inclusive classes like 10 to 19?',
          'Class limits are the smallest and largest values written for a class, such as 10 and 19. Class boundaries are the actual limits with no gaps between classes. For inclusive classes we take half the gap between one upper limit and the next lower limit, here half of one, and subtract it from the lower limit and add it to the upper limit, so 10 to 19 becomes 9.5 to 19.5.',
          [P('p1', 'Limits: the stated lowest and highest values of a class', 3, 'limit', 'stated|written|smallest|lowest|minimum|given|largest|highest|maximum', min=2),
           P('p2', 'Boundaries: actual limits with no gap between classes', 3, 'boundar', 'actual|true|no gap|without gap|continuous|real', min=2),
           P('p3', 'Subtract half the gap from the lower limit and add it to the upper limit', 2, 'half|0.5|half the gap|half of', 'subtract|minus|deduct|less|reduce|take away|lower', min=2),
           P('p4', '10–19 becomes 9.5–19.5', 2, '9.5', '19.5')], 'c7'),
        V('v5', 'What is an ogive and what can you read from it?',
          'An ogive is a cumulative frequency graph. The less-than ogive plots less-than cumulative frequencies against upper class boundaries and rises; the more-than ogive plots more-than cumulative frequencies against lower class boundaries and falls. The point where the two ogives cross gives the median on the horizontal axis, and ogives can also be used to read quartiles.',
          [P('p1', 'Cumulative frequency graph', 3, 'cumulative'),
           P('p2', 'Less-than ogive (upper boundaries, rising) and more-than ogive (lower boundaries, falling)', 3, 'less than', 'more than', min=2),
           P('p3', 'Intersection of the two ogives gives the median', 4, 'median', 'cross|intersect|meet|cut', min=2)], 'c8'),
        V('v6', 'State any three limitations of statistics.',
          'Statistics studies aggregates, not individuals; a single item has no importance by itself. It deals with quantitative data, so qualities must first be given numbers. Projections hold only if the underlying conditions stay the same. And if the sample is not random, the conclusions can be wrong.',
          [P('p1', 'Deals with aggregates, not individuals', 4, 'aggregate|group|mass|not individual|no individual|not with individual|individual has no', min=1),
           P('p2', 'Only quantitative data (qualities must be quantified)', 3, 'quantitative|numerical|number|numeric', min=1),
           P('p3', 'Projections/inferences fail if conditions change or sample is not random', 3, 'condition|random|sample', 'projection|forecast|wrong|mislead|conclusion|inference', min=1)], 'c2'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch13', 'n': 1,
        'title': 'Statistical Description of Data',
        'outcomes': [
            'Explain what statistics means in its singular and plural senses, where it is used in economics, management and business, and its limitations.',
            'Distinguish primary from secondary data, choose a suitable method of collecting primary data and scrutinise data for consistency.',
            'Classify data (time series, geographical, qualitative, quantitative) and present them in text, a well-built table or the right diagram.',
            'Build a frequency distribution and work out class limits, boundaries, mid-values, width, frequency density, relative and cumulative frequencies.',
            'Read and draw a histogram, frequency polygon, ogives and frequency curves, and know what each one reveals.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': [],
                 'exam_tip': 'This unit gives quick, almost free marks in Paper 3: definitions (stub, caption, primary data), class boundaries, mid-values, cumulative frequencies and pie-chart angles. Questions are short — do not over-think them, but watch for inclusive vs exclusive classes.'},
        'concepts': [
            {'id': 'c1', 'title': 'Statistics — the word, its two meanings and its uses',
             'body': ['The word is traced to the Latin "status", the Italian "statista", the German "statistik" and the French "statistique" — all linked to the state, because early statistics were records kept by rulers. Kautilya\'s Arthashastra recorded births and deaths; Abul Fazl\'s Ain-i-Akbari kept agricultural records in Akbar\'s time.',
                      'In the plural sense, statistics means the numbers themselves — figures collected about some characteristic with a view to analysis (e.g. "the GST collection statistics"). In the singular sense, statistics is the science of collecting, organising, analysing and presenting data and then drawing conclusions from them; it is sometimes called the science of counting or the science of averages.',
                      'Economics uses it for time series, index numbers, demand analysis, regression-based forecasts and econometrics. Business management uses sampling and decision theory instead of guesswork. Commerce and industry use averages, dispersion, correlation, index numbers and quality control to plan output and maximise profit.'],
             'analogy': 'Plural "statistics" is the pile of bricks; singular "statistics" is the art of building a house from them.',
             'work': 'An auditor who picks 60 vouchers out of 6,000, an analyst forecasting next year\'s sales, a cost accountant tracking material usage — all of them use statistics every week, even if they never call it that.'},
            {'id': 'c2', 'title': 'Limitations of statistics',
             'body': ['It studies aggregates. One person\'s salary is not a statistic; the average salary of 500 employees is.',
                      'It works with quantitative data. Qualities (honesty, colour) must first be given numbers or counted before analysis.',
                      'Projections hold only under the conditions they assumed. If conditions change, a sales forecast can be badly wrong.',
                      'Inference rests on random sampling. A sample picked carelessly gives misleading conclusions — experts should design the sample.'],
             'analogy': 'Statistics is a wide-angle lens: superb for the crowd, useless for one face in it.',
             'work': 'When a client says "your sample did not include my biggest customer", you explain that statistical conclusions are about the population as a whole, and that a carefully designed sample is what makes them reliable.'},
            {'id': 'c3', 'title': 'Collecting data: primary, secondary and scrutiny',
             'body': ['Primary data are collected for the first time by the investigator for the purpose in hand. Secondary data were collected earlier by someone else and are now being reused. The same figures are primary for the collector and secondary for a later user.',
                      'Methods of collecting primary data: (i) interview — personal (meet the respondent; accurate, good even after disasters), indirect (ask people connected with the event, e.g. after a rail accident) and telephone (quick, cheap, wide coverage but less consistent); (ii) mailed questionnaire (wide area, but non-response is highest); (iii) observation (measure directly, e.g. heights — most reliable but slow, costly and covers a small area); (iv) questionnaires filled in by enumerators, who meet people and explain the questions — used for large enquiries.',
                      'Sources of secondary data: international bodies (WHO, ILO, IMF, World Bank), government publications (CSO\'s Statistical Abstract, ministry reports), private and quasi-government bodies (ISI, ICAR, NCERT) and unpublished research.',
                      'Scrutiny means checking data for accuracy and consistency before using them. There are no fixed rules — the statistician uses intelligence, patience and experience: look for copying errors, test internal consistency (density should equal population ÷ area), spot identical-looking returns from a careless enumerator, and get disputed cases recollected.'],
             'analogy': 'Primary data are vegetables you grow yourself; secondary data are vegetables from the market — cheaper and quicker, but check them for freshness (scrutiny) before you cook.',
             'work': 'In audit, a debtor confirmation you send yourself is primary evidence; the client\'s own ageing report is secondary. Checking that total sales in the GST returns agree with the books is exactly an internal-consistency check.'},
            {'id': 'c4', 'title': 'Classification of data',
             'body': ['Classification arranges data into groups or classes of similar items. It condenses the data, makes comparison possible, removes needless detail and is the starting point of any analysis.',
                      'Four bases: chronological (temporal / time series — e.g. monthly production for five years); geographical (spatial — e.g. candidates by State); qualitative (by an attribute such as gender or nationality — ICAI also calls it ordinal); quantitative (by a measurable variable such as profit or weight — also called cardinal).',
                      'Qualitative and quantitative data are frequency data (we count how many fall in each group). Time series and geographical data are non-frequency data.'],
             'analogy': 'Sorting a heap of laundry by owner (attribute), by size (variable), by the day it was washed (time) or by the room it goes to (place).',
             'work': 'A sales ledger can be classified by month (time series), by branch (geographical), by product type (qualitative) or by invoice size (quantitative). Each view answers a different management question.'},
            {'id': 'c5', 'title': 'Textual and tabular presentation',
             'body': ['Textual presentation writes the data in paragraphs. It is simple and keeps exact figures, but it is dull and comparison is hard; it is unsuitable for data classified in many ways.',
                      'Tabulation arranges data in rows and columns. A good table has: a table number; a self-explanatory title; a caption (the column headings) — the box-head is the whole upper part including column headings, sub-columns, column numbers and units; a stub (the left part describing the rows); the body (the figures); footnotes and the source at the bottom. It should be balanced, show totals and units, and make comparison easy.',
                      'Tabulation is preferred to text because it makes comparison easy, handles complicated data, is needed before drawing diagrams and is essential for statistical analysis.'],
             'analogy': 'A table is like a railway timetable: stations down the left (stub), trains across the top (caption), times in the body.',
             'work': 'Every schedule to the financial statements is a statistical table. Partners review whether totals, units ("₹ in lakh") and notes are shown — the same rules as here.'},
            {'id': 'c6', 'title': 'Diagrams: line, bar and pie',
             'body': ['Diagrams reach even a non-technical audience and reveal hidden trends, but they are less accurate than tables — when precision matters, use a table.',
                      'Line diagram (historiagram): plots a time series against time. When values vary over a wide range or we care about rates of growth, use a ratio chart (log chart) — log of the value is plotted. Multiple line chart: two or more related series in the same unit. Multiple-axis chart: related series in different units.',
                      'Bar diagrams: horizontal bars for qualitative or spatial data; vertical bars for quantitative or time series data. Multiple (grouped) bars compare related series; component (sub-divided) bars show the parts of a total; percentage bars show each part as a share of 100.',
                      'Pie chart (circle diagram): shows the parts of a whole. Angle of a part = (part ÷ total) × 360°.'],
             'analogy': 'A line chart is a cardiogram (how things move over time); a pie chart is a pizza (who got how big a slice).',
             'work': 'Annual reports show revenue mix as a pie, five-year revenue as a bar chart and share price as a line chart. Choosing the wrong one confuses readers.'},
            {'id': 'c7', 'title': 'Frequency distribution and its terms',
             'body': ['An attribute is a qualitative characteristic (gender); a variable is quantitative. A discrete variable takes isolated values (number of printing errors); a continuous variable can take any value in a range (weight).',
                      'Steps: find the range (largest − smallest); decide the class width and number of classes so that number of classes × width ≥ range (always round up); write the classes; put tally marks; count them into a frequency column; confirm the total equals the number of observations.',
                      'Class limits: the lowest (LCL) and highest (UCL) values a class can hold. Class boundaries: the true limits. In exclusive (overlapping) classes like 10–20, 20–30, boundaries equal limits, and a value equal to 20 goes to 20–30. In inclusive (non-overlapping) classes like 10–19, 20–29, LCB = LCL − D/2 and UCB = UCL + D/2, where D is the gap between the UCL of a class and the LCL of the next.',
                      'Mid-value (class mark) = (LCL + UCL) ÷ 2 = (LCB + UCB) ÷ 2. Width = UCB − LCB. Frequency density = class frequency ÷ class width. Relative frequency = class frequency ÷ total frequency (× 100 gives percentage frequency). Less-than cumulative frequency counts observations up to an upper boundary; more-than cumulative frequency counts those from a lower boundary onwards.'],
             'blocks': [t1],
             'analogy': 'A frequency table is a set of labelled boxes; class boundaries are the walls between boxes, with no gap left for any value to fall through.',
             'work': 'A receivables ageing schedule (0–30, 31–60, 61–90 days) is a frequency distribution of invoices by age. Auditors use it to judge the provision for doubtful debts.'},
            {'id': 'c8', 'title': 'Graphs of a frequency distribution',
             'body': ['Histogram: adjacent rectangles on class boundaries; area represents frequency. With equal widths, height = frequency; with unequal widths, height = frequency density. The histogram is used to locate the mode graphically.',
                      'Frequency polygon: join the mid-points of the tops of the histogram rectangles (or plot frequency against mid-values) and close it by joining to the mid-points of an empty class at each end.',
                      'Ogives (cumulative frequency graphs): less-than ogive — less-than c.f. against upper boundaries (rises); more-than ogive — more-than c.f. against lower boundaries (falls). They intersect at N/2, and the foot of that point on the x-axis is the median. Ogives also give quartiles and short-term projections.',
                      'Frequency curve: a smooth curve through the points of the polygon. Shapes: bell-shaped (most common — heights, marks, profits); U-shaped (frequency lowest in the middle, highest at the ends); J-shaped (rises to a maximum at one end) and inverted J; mixed curves.'],
             'blocks': [t4],
             'analogy': 'An ogive is a staircase of running totals; the step where half the crowd has passed is the median.',
             'work': 'Credit teams chart cumulative overdue amounts to show "x% of receivables are within 60 days" — that is reading an ogive.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'All the frequency-distribution terms in one table', 'difficulty': 'core', 'minutes': 10,
             'q': 'Marks of 50 students: 10–19: 4, 20–29: 7, 30–39: 12, 40–49: 15, 50–59: 8, 60–69: 4. Find class boundaries, mid-values, relative frequencies, frequency densities and both cumulative frequencies.',
             'solution': [t1, wn('Working notes', 'Gap between 19 and 20 is 1, so D/2 = 0.5: each class becomes LCL − 0.5 to UCL + 0.5; width = 10. Mid-value of 10–19 = (10 + 19) ÷ 2 = 14.5. Relative frequency of 40–49 = 15 ÷ 50 = 0.3. Less-than c.f. at 39.5 = 4 + 7 + 12 = 23. More-than c.f. from 29.5 = 50 − 4 − 7 = 39.'),
                          note('Read the less-than column against the upper boundary (e.g. 23 students scored below 39.5) and the more-than column against the lower boundary (e.g. 39 students scored 29.5 or more).')],
             'checks': c1},
            {'id': 'i2', 'title': 'Angles for a pie chart', 'difficulty': 'core', 'minutes': 6,
             'q': 'Of every ₹120 lakh of sales, Neelgiri Foods spends ₹48 lakh on raw material, ₹30 lakh on wages, ₹18 lakh on power and fuel and ₹12 lakh on administration; profit is ₹12 lakh. Compute the angles for a pie chart.',
             'solution': [t2, wn('Rule', 'Angle = item ÷ total × 360. Raw material: 48 ÷ 120 × 360 = 144°. The angles must add up to 360°.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Choosing and preparing a percentage bar diagram', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Sales (₹ lakh) of products A, B and C were 60, 90, 50 in 2025 and 84, 105, 61 in 2026. Management wants to compare the product mix of the two years. Which diagram suits, and what figures are plotted?',
             'solution': [t3, p('Because totals differ (₹200 lakh vs ₹250 lakh) and the question is about mix, a percentage (divided) bar diagram is best: two bars of equal height (100%), each divided into A, B and C. Two pie charts would also work. A component bar in absolute ₹ would show growth, not mix.'),
                          wn('Shares', 'A: 60 ÷ 200 = 30% → 84 ÷ 250 = 33.6%. B: 45% → 42%. C: 25% → 24.4%. Product A gained share even though all three grew in value.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Histogram with unequal class widths', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Invoices by days outstanding: 0–10: 5, 10–20: 12, 20–40: 24, 40–70: 18, 70–100: 6. What heights should the histogram bars have?',
             'solution': [t4, p('With unequal widths the area — not the height — must represent frequency, so heights are frequency densities (f ÷ width). Taking 10 days as the standard width, the 20–40 bar is 24 ÷ 20 × 10 = 12 units tall, not 24. Plotting raw frequencies would make the wide classes look far bigger than they are.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Turning a debtors list into an ageing distribution', 'role': 'Articled assistant, statutory audit of a distributor',
             'situation': 'The client gives you a list of 1,240 open invoices with dates. Your senior wants an ageing summary (0–30, 31–60, 61–90, 91–180, over 180 days) and a chart for the audit committee.',
             'steps': ['Compute the days outstanding for each invoice at the year-end date (a discrete variable — whole days).',
                       'Use inclusive classes (0–30, 31–60 …) because days are whole numbers; note that the true boundaries are 30.5, 60.5 and so on.',
                       'Count invoices and amounts in each class; check that both totals agree with the ledger (scrutiny / internal consistency).',
                       'Add a percentage column and a less-than cumulative percentage column ("82% of the amount is within 90 days").',
                       'Because the last class is open-ended and widths differ, present a table plus a bar chart of amounts rather than a histogram.'],
             'takeaway': 'An ageing schedule is just a frequency distribution of receivables. The totals check and the cumulative column are what make it useful evidence.',
             'think': 'Why would a histogram of invoice counts drawn with raw frequencies mislead if the class 91–180 is three times as wide as 61–90?',
             'answer': 'Area would overstate the wide class threefold. Heights must be frequency densities (count ÷ width) for a histogram with unequal widths.'},
            {'id': 'j2', 'title': 'Picking the right chart for a management deck', 'role': 'Finance executive in a listed FMCG company',
             'situation': 'You must show (a) the cost structure of every ₹100 of sales, (b) eight years of revenue that grew from ₹40 crore to ₹900 crore, and (c) revenue by State.',
             'steps': ['(a) Parts of a whole → pie chart or a percentage bar; compute angles as share × 360°.',
                       '(b) Huge range and interest in growth rates → a ratio (log) line chart, so equal growth rates show as equal slopes.',
                       '(c) Spatial, qualitative categories → horizontal bar diagram, sorted by size.',
                       'Put the supporting table with exact figures in the appendix — diagrams are attractive but less accurate.'],
             'takeaway': 'The type of data decides the diagram: time → line, categories/places → horizontal bars, parts of a whole → pie or percentage bar.',
             'think': 'On an ordinary line chart, would growth from ₹40 crore to ₹80 crore look as important as growth from ₹450 crore to ₹900 crore?',
             'answer': 'No — both are 100% growth, but on a natural scale the second rise looks ten times bigger. A ratio (log) chart shows both as equal slopes.'},
        ],
        'mcqs': [
            mq('m1', 'Statistics used in the plural sense means:', ['Numerical data collected with a view to analysis', 'The science of collecting and analysing data', 'A single figure such as an average', 'Only data published by the government'],
               "In the plural sense, 'statistics' means the numerical facts themselves, collected with a view to analysis, such as figures on prices, output or population. The trap is 'the science of collecting and analysing data', which is the singular sense (the method). In practice: when the RBI or MoSPI publishes 'statistics' on inflation or GDP, the word is used in the plural sense: the figures themselves.", 'c1', topic='Statistics — the word, its two meanings and its uses'),
            mq('m2', 'In the singular sense, statistics is best described as:', ['The scientific method of collecting, analysing and presenting data and drawing inferences', 'A set of numbers about a characteristic', 'The study of individuals', 'A branch of accounting'],
               "Used as a singular noun, statistics is the scientific method of collecting, presenting, analysing and interpreting data and drawing conclusions from it. The trap is 'a set of numbers about a characteristic', which is the plural sense (the data). In practice: an analyst who applies statistics to a company's sales figures to forecast demand is using it in the singular sense, as a method.", 'c1', topic='Statistics — the word, its two meanings and its uses'),
            mq('m3', 'Which of these is a limitation of statistics?', ['It does not study individuals', 'It cannot be used in economics', 'It ignores aggregates', 'It does not use averages'],
               "Statistics deals with aggregates, so it does not study individual items; a single value matters only as part of a group. 'It cannot be used in economics' is the trap: economics is one of the biggest users of statistics. In practice: an average salary figure for a firm tells you nothing about any one employee, so an HR audit of a single pay slip needs other evidence.", 'c2', topic='Limitations of statistics'),
            mq('m4', 'Data collected by an investigator for the first time for his own enquiry are called:', ['Primary data', 'Secondary data', 'Ordinal data', 'Grouped data'],
               "Data collected for the first time by the investigator for his own enquiry are primary data: original and first-hand. Secondary data is the trap: those are data already collected by someone else and only reused. In practice: a CA firm's own survey of its clients' GST compliance gives primary data, while using RBI's published bank-credit figures gives secondary data.", 'c3', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m5', 'Which method of collecting primary data usually suffers the highest non-response?', ['Mailed questionnaire method', 'Personal interview method', 'Observation method', 'Questionnaires filled in by enumerators'],
               'Many people who receive a mailed questionnaire simply never return it, so this method usually has the highest non-response. The personal interview method is the trap: the investigator meets each respondent, so non-response is low. In practice: firms sending balance-confirmation requests to debtors by post often face exactly this problem of unreturned replies and must follow up.', 'c3', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m6', 'After a train accident the injured cannot be reached, so information is collected from relatives and railway staff. This is:', ['Indirect interview method', 'Personal interview method', 'Observation method', 'Mailed questionnaire method'],
               'When respondents cannot be approached directly, information is collected from third parties connected with the matter. That is the indirect interview method, as used by enquiry committees. The personal interview method is the trap: it requires meeting the injured persons themselves. In practice: when a debtor cannot be contacted, an auditor may gather evidence from third parties like the bank or the transporter.', 'c3', 'moderate', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m7', 'The method that is quick and cheap with wide coverage, but less consistent, is the:', ['Telephone interview method', 'Personal interview method', 'Observation method', 'Indirect interview method'],
               "Telephone interviews reach a wide area quickly and cheaply, but responses are less consistent and less detailed. The personal interview method is the trap: it is accurate but slow and costly and cannot cover a large area. In practice: market-research firms and banks' customer-feedback teams in India rely heavily on phone surveys because of their reach and low cost.", 'c3', 'moderate', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m8', 'Measuring the heights of students directly is an example of:', ['Observation method — reliable but slow and limited in coverage', 'Mailed questionnaire method', 'Secondary data', 'Telephone interview'],
               'Measuring heights directly is observation: the investigator records what is seen. It is generally the most accurate method, but it is slow and can cover only a limited area. The mailed questionnaire is the trap: nothing is posted here. In practice: physical verification of inventory during an audit is observation, reliable but time-consuming.', 'c3', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m9', 'Which of these is a source of secondary data?', ['A report published by the World Bank', 'A survey you conduct yourself', 'Your own measurement of machine output', 'Interviews you hold with customers'],
               'A published World Bank report contains data collected by someone else, so using it gives secondary data. Data from your own survey is the trap: anything you collect first-hand is primary. In practice: equity analysts routinely use secondary data from the World Bank, IMF, RBI and company annual reports to build their economic and industry models.', 'c3', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m10', 'Checking whether Density = Population ÷ Area holds for the data of several towns is a part of:', ['Scrutiny of data (internal consistency)', 'Tabulation', 'Classification', 'Sampling'],
               'When two or more related series exist, checking whether they agree with each other (here Density = Population ÷ Area) is the internal-consistency test done during scrutiny of data. Tabulation is the trap: it only arranges data in rows and columns. In practice: auditors do the same when they check that gross profit equals sales minus cost of sales across schedules.', 'c3', 'moderate', topic='Collecting data: primary, secondary and scrutiny'),
            mq('m11', 'Data on CA Foundation candidates arranged State-wise are:', ['Geographical (spatial) data', 'Chronological data', 'Qualitative data', 'Cardinal data'],
               "Data arranged by place, such as State or district, form a geographical (spatial) series. Chronological data is the trap: that is data arranged by time. In practice: ICAI's examination results and GST collection figures are frequently published State-wise, a geographical classification.", 'c4', topic='Classification of data'),
            mq('m12', 'Which pair belongs to the non-frequency group of data?', ['Time series data and geographical data', 'Qualitative data and quantitative data', 'Discrete data and continuous data', 'Primary data and secondary data'],
               'Time series data and geographical data are arranged by time and by place, not counted into frequency groups, so they form the non-frequency group. Qualitative and quantitative data is the trap: those are classified by attribute or value and counted, so they are frequency data. In practice: a monthly GST collection table is a time series, not a frequency distribution.', 'c4', 'moderate', topic='Classification of data'),
            mq('m13', 'Data on the smoking habits of a group of people are:', ['Qualitative data', 'Quantitative data', 'Chronological data', 'Continuous data'],
               'Smoking habit is an attribute that can only be described (smoker, non-smoker), not measured, so the data are qualitative. Quantitative data is the trap: that requires a measurable value like height or income. In practice: insurance proposal forms record such attributes (smoker or not), and actuaries classify customers by them when pricing policies.', 'c4', topic='Classification of data'),
            mq('m14', 'In a statistical table, the stub is:', ['The left part of the table describing the rows', 'The upper part describing the columns', 'The main part containing the figures', 'The note at the bottom of the table'],
               'The stub is the left-hand part of a table, giving the headings that describe each row. The caption, describing columns, is the trap: it sits at the top. The body holds the figures and footnotes sit at the bottom. In practice: in a financial statement schedule, the line items down the left are the stub and the year columns are the caption.', 'c5', topic='Textual and tabular presentation'),
            mq('m15', 'In tabulation, the caption refers to:', ['The headings of the columns and sub-columns', 'The headings of the rows', 'The source of the data', 'The figures in the table'],
               "The caption is the heading of the columns and sub-columns at the top of the table. Row headings is the trap: those form the stub on the left. In practice: in a comparative balance sheet, the captions 'As at 31 March 2026' and 'As at 31 March 2025' head the columns, while the line items form the stub.", 'c5', topic='Textual and tabular presentation'),
            mq('m16', 'Compared with tabulation, diagrammatic representation is:', ['More attractive but less accurate', 'More accurate but less attractive', 'Both more accurate and more attractive', 'Of no use to a lay reader'],
               "Diagrams are attractive and reveal trends at a glance, even to a lay reader, but they show values only approximately. A table is therefore preferred when accuracy matters. 'More accurate but less attractive' is the trap: it reverses the comparison. In practice: annual reports use charts for highlights but always give the exact figures in tables.", 'c6', topic='Diagrams: line, bar and pie'),
            nq('m17', 'In a pie chart of total expenses of ₹1,20,000, rent of ₹27,000 is shown by an angle of:', '27000/120000*360', [27, 75, 22.5],
               "A pie chart has 360° in all, so each item's angle = (item ÷ total) × 360. Rent: 27,000 ÷ 1,20,000 × 360 = 81 degrees. 22.5 is the trap: it is rent as a percentage of total expenses, not the angle. In practice: CFO presentations to a board often show cost structure as a pie chart, and every slice is worked out exactly like this.", 'c6', unit='degrees', topic='Diagrams: line, bar and pie'),
            mq('m18', 'For a time series whose values range from very small to very large, and where the rate of growth matters, the most suitable diagram is:', ['A ratio (logarithmic) chart', 'A pie chart', 'A horizontal bar diagram', 'A frequency polygon'],
               "On a ratio (logarithmic) chart, the log of each value is plotted, so equal rates of change show as equal slopes whether values are small or large. A horizontal bar diagram is the trap: it suits categories or places, not growth over time. In practice: long-run charts of the Sensex or a company's revenue over decades often use a log scale so early growth is visible.", 'c6', 'moderate', topic='Diagrams: line, bar and pie'),
            mq('m19', 'Horizontal bar diagrams are generally used for:', ['Qualitative data or data varying over space', 'Time series data', 'Continuous frequency distributions', 'Cumulative frequencies'],
               'Horizontal bars suit qualitative categories and data varying over place, because long category or region names fit easily. Time series data is the trap: time is normally shown on the horizontal axis with vertical bars or lines. In practice: a chart ranking Indian States by GST collection uses horizontal bars sorted by size.', 'c6', topic='Diagrams: line, bar and pie'),
            mq('m20', 'To compare the components of a total and also show each as a share of the whole, one may use:', ['A percentage (divided) bar diagram or a pie chart', 'A multiple line chart', 'An ogive', 'A histogram'],
               'A percentage (divided) bar diagram and a pie chart both show each component as a share of the whole total. An ogive is the trap: it shows cumulative frequencies, not parts of a total. In practice: a cost-sheet breakdown of where each rupee of revenue goes (materials, wages, overheads, profit) is commonly drawn as a pie chart or percentage bar.', 'c6', topic='Diagrams: line, bar and pie'),
            nq('m21', 'For the inclusive classes 20–29, 30–39, 40–49, the lower class boundary of 30–39 is:', '30-(30-29)/2', [30, 29, 30.5],
               "For inclusive classes, the gap between one class's upper limit and the next lower limit is 30 − 29 = 1. Subtract half of it: LCB = 30 − 0.5 = 29.5. The trap is 30, the class limit, not the boundary. In practice: boundaries matter when data like invoice values are grouped, so that an item worth 29.7 is not left out of every class.", 'c7', topic='Frequency distribution and its terms'),
            nq('m22', 'A class has boundaries 24.5 and 34.5. Its mid-value is:', '(24.5+34.5)/2', [29, 30, 10],
               'Mid-value = (lower boundary + upper boundary) ÷ 2 = (24.5 + 34.5) ÷ 2 = 29.5. The trap is 10, which is the class width (34.5 − 24.5), not the mid-value. In practice: when the mean of grouped data is computed, for example the average ticket size of grouped sales invoices, each class is represented by its mid-value.', 'c7', topic='Frequency distribution and its terms'),
            nq('m23', 'In a distribution of 120 items, a class has frequency 18. Its relative frequency is:', '18/120', [18, 0.18, 6.67],
               'Relative frequency = class frequency ÷ total frequency = 18 ÷ 120 = 0.15, or 15%. The trap is 0.18, which wrongly divides 18 by 100. In practice: a bank analysing loan sizes reports the share of loans in each bracket, which is just relative frequency expressed as a percentage.', 'c7', topic='Frequency distribution and its terms'),
            nq('m24', 'The class 20–40 has frequency 24. Its frequency density is:', '24/(40-20)', [24, 0.83, 12],
               'Frequency density = frequency ÷ class width. The width of 20–40 is 20, so density = 24 ÷ 20 = 1.2. The trap is 0.83, which divides width by frequency the wrong way round. In practice: densities are needed when classes are unequal, such as income brackets in tax data, so that wider brackets do not look artificially large.', 'c7', 'moderate', topic='Frequency distribution and its terms'),
            nq('m25', 'Frequencies of the classes 0–10, 10–20, 20–30, 30–40 are 5, 9, 14, 7. The more-than cumulative frequency corresponding to 20 is:', '14+7', [28, 14, 35],
               'The more-than cumulative frequency at 20 counts every item from 20 upwards, i.e. the classes 20–30 and 30–40: 14 + 7 = 21. The trap is 28, which is the less-than cumulative frequency up to 30 (5 + 9 + 14). In practice: credit teams use more-than counts, such as the number of debtors overdue by more than 90 days, when ageing receivables.', 'c7', 'moderate', topic='Frequency distribution and its terms'),
            nq('m26', 'The largest observation is 82 and the smallest is 24. With a class width of 8, the number of classes needed is:', '-(-(82-24)//8)', [7, 7.25, 10],
               'Range = 82 − 24 = 58. Classes × 8 must cover at least 58, and 58 ÷ 8 = 7.25, so round up to 8 classes. The trap is 7, which would cover only 56 and leave extreme values outside every class. In practice: when grouping data for a report, such as ageing invoices by value, always round the number of classes up so that nothing falls outside.', 'c7', 'moderate', topic='Frequency distribution and its terms'),
            mq('m27', 'With exclusive classes 10–20, 20–30, 30–40, an observation of exactly 20 is placed in:', ['20–30', '10–20', 'Either class', 'Neither class'],
               'In exclusive classes, the upper limit of each class is excluded and belongs to the next class. So an observation of exactly 20 goes into 20–30. The trap is 10–20, which would count 20 in a class whose upper limit is excluded. In practice: ageing schedules (0–30 days, 30–60 days) must state such a convention, or a 30-day invoice could be counted twice or missed.', 'c7', topic='Frequency distribution and its terms'),
            mq('m28', 'The number of children in a family is an example of:', ['A discrete variable', 'A continuous variable', 'An attribute', 'A geographical series'],
               'The number of children can only be a whole number (0, 1, 2, …); there are no values in between, so it is a discrete variable. A continuous variable is the trap: that can take any value in a range, like height or weight. In practice: the number of invoices or employees is discrete, while amounts in rupees or weights of stock are treated as continuous.', 'c7', topic='Frequency distribution and its terms'),
            mq('m29', 'The point where the less-than and more-than ogives intersect gives the:', ['Median', 'Mean', 'Mode', 'Range'],
               'The less-than and more-than ogives always cross at a cumulative frequency of N/2, where half the items lie on each side. The x-value of that point is the median. The mean is the trap: it cannot be read from ogives. In practice: an analyst can read the median salary or median invoice value straight off an ogive drawn from a frequency table.', 'c8', topic='Graphs of a frequency distribution'),
            mq('m30', 'A histogram is used to find which measure graphically?', ['Mode', 'Median', 'Mean', 'Quartile deviation'],
               "In a histogram the modal class is the tallest rectangle, and the mode is located by joining the corners of that rectangle with those of its neighbours. The median is the trap: it is found from ogives. In practice: a retailer's histogram of bill sizes shows the most common bill value at a glance, useful for pricing combo offers.", 'c8', 'moderate', topic='Graphs of a frequency distribution'),
            mq('m31', 'A frequency polygon is obtained by joining:', ['The mid-points of the tops of histogram rectangles', 'The upper corners of histogram rectangles', 'Cumulative frequencies at class boundaries', 'Class limits with frequencies'],
               'A frequency polygon is drawn by plotting frequencies against mid-values, which means joining the mid-points of the tops of the histogram rectangles, and closing the figure at both ends. The upper corners is the trap: joining corners does not represent class mid-values. In practice: frequency polygons let analysts overlay two distributions, such as sales in two regions, on one chart.', 'c8', topic='Graphs of a frequency distribution'),
            mq('m32', 'In a histogram with unequal class widths, the heights of the rectangles should be proportional to:', ['Frequency densities', 'Class frequencies', 'Cumulative frequencies', 'Mid-values'],
               'In a histogram, the area of each rectangle represents frequency. With unequal widths, height must therefore be frequency ÷ width, the frequency density. Class frequencies is the trap: using them would make wider classes look too large. In practice: income-distribution charts with brackets of unequal size, such as tax slabs, must use densities to avoid misleading readers.', 'c8', 'moderate', topic='Graphs of a frequency distribution'),
            mq('m33', 'A frequency curve in which frequency is lowest in the middle and highest at both ends is:', ['U-shaped', 'Bell-shaped', 'J-shaped', 'Inverted J-shaped'],
               'A U-shaped curve has its lowest frequency near the middle and rises towards both extremes. A bell-shaped curve is the trap: it is the opposite, peaking in the middle. In practice: the number of accidents or claims by age group is often U-shaped, high for the very young and the very old, which insurers use in pricing.', 'c8', topic='Graphs of a frequency distribution'),
            mq('m34', 'Most distributions of heights, weights and marks give a:', ['Bell-shaped curve', 'U-shaped curve', 'J-shaped curve', 'Straight line'],
               'Heights, weights and marks usually start with low frequencies, rise to a peak around the average and fall again, giving a bell-shaped curve. The J-shaped curve is the trap: it keeps rising (or falling) towards one end. In practice: the normal (bell) shape underlies many business models, such as quality-control limits in manufacturing and risk models in finance.', 'c8', topic='Graphs of a frequency distribution'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'Ages (years) of 30 employees of Vardhan Logistics: ' + ', '.join(map(str, raw)) + '. Construct a frequency distribution with exclusive classes of width 5 starting at 20. Show the range, the number of classes and tally marks.',
             'model': [wn('Step 1 — range and classes', f'Range = {max(raw)} − {min(raw)} = {rng}. Number of classes × 5 ≥ {rng}, so number of classes = next integer of {rng} ÷ 5 = {k}. Starting at 20: 20–25, 25–30, …, 45–50.'),
                       tq1, wn('Step 3 — check', 'Total of frequencies = 30 = number of observations. Values such as 25, 30, 35, 40 and 45 are put in the class that starts with them (upper limit excluded).')],
             'scheme': [{'id': 's1', 'pt': f'Range {rng} and number of classes {k} worked out', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Exclusive classes formed correctly (upper limit excluded)', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Tally marks and frequencies correct', 'm': 2, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Total = 30 checked; title and column heads given', 'm': 1, 'skill': 'presentation'}],
             'remarks': ['Most errors come from boundary values: 30 belongs to 30–35, not 25–30.', 'Several candidates forget to show the total and therefore miss a tallying error.'],
             'mistakes': ['Rounding 26 ÷ 5 = 5.2 down to 5 classes.', 'Counting a boundary value twice.', 'No title for the table.'],
             'tips': ['Tick each raw value as you tally it.', 'Always end with a total row and compare it with n.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'A family spends its monthly income as follows: food ₹13,500, rent ₹9,000, education ₹6,000, transport ₹3,600 and savings ₹3,900. Compute the angles to draw a pie chart.',
             'model': [tq2, wn('Working', f'Total = ₹{inr(T)}. Food: 13,500 ÷ {inr(T)} × 360 = 135°. The angles total 360°.')],
             'scheme': [{'id': 's1', 'pt': f'Total ₹{inr(T)} found', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Formula: item ÷ total × 360', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'All five angles correct and adding to 360°', 'm': 2, 'skill': 'computation'}],
             'remarks': ['Good answers show the formula once and then a table.', 'Weak answers give percentages and stop.'],
             'mistakes': ['Using 100 instead of 360.', 'Forgetting the savings component.'],
             'tips': ['Check that the angles total 360°.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Daily units sold by a dealer over 60 days: 100–199: 6, 200–299: 14, 300–399: 22, 400–499: 12, 500–599: 6. (a) Find class boundaries and mid-values. (b) Prepare less-than and more-than cumulative frequencies. (c) If both ogives are drawn, at what cumulative frequency do they meet, and in which class does that point lie?',
             'model': [tq3, wn('(a)', 'Gap between 199 and 200 is 1, so subtract 0.5 from lower limits and add 0.5 to upper limits; width = 100. Mid-value of 100–199 = 149.5.'),
                       wn('(c)', f'The ogives meet at N/2 = {half}. Less-than c.f. is 20 at 299.5 and 42 at 399.5, so the 30th value lies in 299.5–399.5 (class 300–399). The x-value of the meeting point is the median.')],
             'scheme': [{'id': 's1', 'pt': 'Boundaries (±0.5) correct', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Mid-values correct', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Less-than c.f. column correct', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'More-than c.f. column correct', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Meeting point at N/2 = 30 and class 300–399 identified', 'm': 2, 'skill': 'application'}],
             'remarks': ['Many candidates plot the less-than c.f. against lower boundaries — it belongs at upper boundaries.', 'The idea that ogives cross at N/2 is tested often in MCQs.'],
             'mistakes': ['Using class limits instead of boundaries for ogives.', 'Writing the more-than c.f. in the wrong order.'],
             'tips': ['Less-than goes with UCB, more-than goes with LCB.', 'Both cumulative columns end at N — use that as a check.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Statistics: plural = data; singular = science of collecting, presenting, analysing and interpreting data.',
                        'Limitations: aggregates only, quantitative only, conditional projections, needs random samples.',
                        'Primary (first-hand) vs secondary (reused). Primary methods: interview (personal, indirect, telephone), mailed questionnaire, observation, enumerators.',
                        'Classification: chronological, geographical, qualitative (ordinal), quantitative (cardinal).',
                        'Table parts: number, title, caption/box-head, stub, body, footnote, source.',
                        'Diagrams: line/historiagram, ratio (log) chart, bar diagrams (horizontal, vertical, multiple, component, percentage), pie chart.',
                        'Frequency terms: limits, boundaries, mid-value, width, density, relative and cumulative frequency.',
                        'Graphs: histogram (mode), frequency polygon, ogives (median, quartiles), frequency curves (bell, U, J).'],
            'remember': ['Pie angle = part ÷ total × 360°.', 'Inclusive classes: LCB = LCL − D/2, UCB = UCL + D/2.', 'Number of classes = range ÷ width, rounded UP.', 'Ogives meet at N/2 → median.', 'Mailed questionnaire → highest non-response.'],
            'traps': ['Stub (rows) vs caption (columns) — do not swap them.', 'Unequal widths: histogram heights are densities, not frequencies.', 'Time series and geographical data are non-frequency data.', 'Exclusive classes: the upper limit belongs to the next class.']},
        'quickref': [
            {'k': 'Pie chart angle', 'v': '(Component ÷ Total) × 360°'},
            {'k': 'Class boundaries (inclusive)', 'v': 'LCB = LCL − D/2; UCB = UCL + D/2 (D = gap between UCL and next LCL)'},
            {'k': 'Mid-value', 'v': '(LCL + UCL)/2 = (LCB + UCB)/2'},
            {'k': 'Width', 'v': 'UCB − LCB'},
            {'k': 'Frequency density', 'v': 'Class frequency ÷ class width'},
            {'k': 'Relative frequency', 'v': 'Class frequency ÷ total frequency (× 100 = percentage frequency)'},
            {'k': 'Number of classes', 'v': 'Smallest integer ≥ Range ÷ width'},
            {'k': 'Ogives', 'v': 'Less-than: c.f. vs UCB (rising); more-than: c.f. vs LCB (falling); meet at N/2 → median'},
        ],
        'viva': viva, 'cases': cases,
    }
