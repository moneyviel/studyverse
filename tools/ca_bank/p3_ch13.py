"""Paper 3 Ch 13 — Statistical Description of Data (u01) and Sampling (u02): extra MCQ templates.
Numeric questions are computed; a small number of definition questions (kind 'fact') carry a fixed answer that the
independent verifier checks against its own separately written answer key."""
from common import *
import math

U1, U2 = 'fnd-p3-ch13-u01', 'fnd-p3-ch13-u02'
A_CLS, A_TAB, A_DIA, A_FD, A_GR = 'Classification of data', 'Textual and tabular presentation', 'Diagrams: line, bar and pie', 'Frequency distribution and its terms', 'Graphs of a frequency distribution'
A_COL, A_LIM, A_STAT = 'Collecting data: primary, secondary and scrutiny', 'Limitations of statistics', 'Statistics — the word, its two meanings and its uses'
B_WHY, B_CEN, B_ERR, B_SE, B_TYP = 'Why sample, and the principles behind it', 'Sample survey vs complete enumeration (census)', 'Errors in sample surveys', 'Key terms, sampling distribution and standard error', 'Types of sampling'


def freq_table(r, inclusive=False):
    k = r.randint(5, 7); w = r.choice([5, 10, 20, 25]); lo = r.choice([0, 10, 20, 50, 100]); f = [r.randint(2, 30) for _ in range(k)]
    if inclusive: cls = [(lo + i * w, lo + (i + 1) * w - 1) for i in range(k)]
    else: cls = [(lo + i * w, lo + (i + 1) * w) for i in range(k)]
    return cls, f, w


def tbl(cls, f, inclusive=False):
    return '; '.join(f'{a}–{b}: {x}' for (a, b), x in zip(cls, f))


def class_mark(r):
    cls, f, w = freq_table(r, r.random() < .5); i = r.randrange(len(cls)); a, b = cls[i]
    m = F(a + b, 2)
    return dict(q=f'The class mark (mid-value) of the class {a}–{b} is:', a=num(m), w=[num(b - a), num(F(b - a, 2)), num(m + F(1, 2)), num(a + w)],
                ex=f'Class mark = (lower limit + upper limit)/2 = ({a} + {b})/2 = {num(m)}. It represents every observation of the class in calculations such as the mean. The width of the class ({b - a}) is a different quantity.',
                fast='Class mark = (lower limit + upper limit) ÷ 2.', secs=15, d='core', topic=A_FD, check=frx(m), k='ch13.mark', data={'a': a, 'b': b})


def boundary(r):
    cls, f, w = freq_table(r, True); i = r.randrange(1, len(cls)); a, b = cls[i]
    kind = r.choice(['upper', 'lower']); v = F(2 * b + 1, 2) if kind == 'upper' else F(2 * a - 1, 2)
    listing = ', '.join(f'{x}–{y}' for x, y in cls[:4])
    return dict(q=f'For the inclusive classes {listing}, …, the {kind} class boundary of the class {a}–{b} is:', a=num(v), w=[num(b if kind == 'upper' else a), num(v + 1), num(v - 1), num(F(a + b, 2))],
                ex=f'In inclusive classes there is a gap of 1 between one upper limit and the next lower limit. Half the gap (0.5) is subtracted from every lower limit and added to every upper limit. So the {kind} boundary of {a}–{b} is {num(v)}. Boundaries make the classes continuous (exclusive).',
                fast='Lower boundary = lower limit − 0.5; upper boundary = upper limit + 0.5 (gap of 1).', secs=25, d='core', topic=A_FD, check=frx(v), k='ch13.bound', data={'a': a, 'b': b, 'kind': kind})


def density(r):
    cls, f, w = freq_table(r); i = r.randrange(len(cls)); a, b = cls[i]
    v = F(f[i], b - a)
    return dict(q=f'A class {a}–{b} has frequency {f[i]}. Its frequency density is:', a=num(v, 3), w=[num(f[i] * (b - a)), num(F(b - a, f[i]), 3), num(F(f[i], F(a + b, 2)), 3), num(f[i])],
                ex=f'Frequency density = class frequency ÷ class width = {f[i]} ÷ {b - a} = {num(v, 3)}. It is used to draw histograms correctly when classes have unequal widths, because the area (not the height) of each bar must show the frequency.',
                fast='Frequency density = frequency ÷ class width.', secs=15, d='core', topic=A_FD, check=f'round({f[i]}/{b - a},3)', k='ch13.dens', data={'a': a, 'b': b, 'f': f[i]})


def rel_freq(r):
    cls, f, w = freq_table(r); i = r.randrange(len(cls)); a, b = cls[i]; N = sum(f)
    v = F(f[i] * 100, N)
    return dict(q=f'Frequency distribution — {tbl(cls, f)}. The relative frequency of the class {a}–{b}, as a percentage, is about:', a=pct(v), w=[pct(F(f[i] * 100, N - f[i])), pct(F(sum(f[:i + 1]) * 100, N)), pct(f[i]), pct(F(100, len(cls)))],
                ex=f'Total frequency N = {N}. Relative frequency = class frequency ÷ N = {f[i]} ÷ {N} = {num(v / 100, 4)}, i.e. about {num(v)}%. Using the cumulative frequency ({sum(f[:i + 1])}) instead of the class frequency is a common slip.',
                fast=f'Add the frequencies once (N = {N}), then f ÷ N × 100.', secs=40, d='core', topic=A_FD, check=f'{f[i]}*100/{N}', k='ch13.relf', data={'f': f, 'i': i})


def cum_freq(r):
    cls, f, w = freq_table(r); i = r.randrange(1, len(cls) - 1); kind = r.choice(['less', 'more'])
    if kind == 'less': v = sum(f[:i + 1]); point = cls[i][1]; phrase = f'less than {point}'
    else: v = sum(f[i:]); point = cls[i][0]; phrase = f'{point} or more'
    return dict(q=f'Frequency distribution — {tbl(cls, f)}. The number of observations {phrase} is:', a=str(v), w=[str(sum(f[:i])), str(sum(f[i + 1:])), str(sum(f) - v), str(v + f[i + 1 if kind == "less" else i - 1])],
                ex=f'This is a {"less-than" if kind == "less" else "more-than"} cumulative frequency. ' + (f'Add the frequencies of all classes up to the one ending at {point}: {" + ".join(map(str, f[:i + 1]))} = {v}.' if kind == 'less' else f'Add the frequencies of the classes from {point} upwards: {" + ".join(map(str, f[i:]))} = {v}.') + ' Cumulative frequencies are exactly what an ogive plots against the class boundaries, so read the class limits carefully before adding.',
                fast='Keep a running total from the correct end of the table.', secs=35, d='core', topic=A_GR, check=str(v), k='ch13.cum', data={'f': f, 'i': i, 'kind': kind})


ITEMS = [('Food', 'Rent', 'Education', 'Transport', 'Savings'), ('Raw material', 'Wages', 'Power', 'Overheads', 'Profit'), ('Wheat', 'Rice', 'Pulses', 'Oilseeds', 'Others')]


def pie(r):
    names = r.choice(ITEMS); k = r.randint(4, 5); vals = [r.randint(2, 30) * 100 for _ in range(k)]; T = sum(vals); i = r.randrange(k)
    ang = F(vals[i] * 360, T)
    if ang.denominator > 4: return None
    return dict(q=f'Monthly spending (₹): ' + ', '.join(f'{n} {inr(v)}' for n, v in zip(names, vals)) + f'. In a pie chart, the angle for {names[i]} is:', a=f'{num(ang)}°',
                w=[f'{num(F(vals[i] * 100, T))}°', f'{num(F(vals[i] * 180, T))}°', f'{num(ang + 10)}°', f'{num(F(360, k))}°'],
                ex=f'Total = ₹{inr(T)}. Each item gets a share of 360° in proportion to its value: {names[i]} angle = {inr(vals[i])}/{inr(T)} × 360° = {num(ang)}°. Writing the percentage ({num(F(vals[i] * 100, T))}%) as degrees is the classic mistake. All the angles together must add up to 360°.',
                fast='Angle = (value ÷ total) × 360; or percentage × 3.6.', secs=35, d='core', topic=A_DIA, check=frx(ang), k='ch13.pie', data={'vals': vals, 'i': i})


def width_from_marks(r):
    w = r.choice([4, 5, 8, 10, 15, 20]); m0 = r.randint(2, 30) * w // 2 * 1 + w // 2
    marks = [m0 + i * w for i in range(4)]; i = r.randrange(4); kind = r.choice(['lower', 'upper'])
    v = F(2 * marks[i] - w, 2) if kind == 'lower' else F(2 * marks[i] + w, 2)
    return dict(q=f'The class marks of a distribution are {", ".join(map(str, marks))}. The {kind} limit of the class whose mark is {marks[i]} is (exclusive classes):', a=num(v),
                w=[num(marks[i] - w if kind == 'lower' else marks[i] + w), num(marks[i]), num(v + (1 if kind == 'lower' else -1)), num(F(marks[i], 2))],
                ex=f'Consecutive class marks differ by the class width: {marks[1]} − {marks[0]} = {w}. A class extends half the width on each side of its mark, so the {kind} limit is {marks[i]} {"−" if kind == "lower" else "+"} {num(F(w, 2))} = {num(v)}. Adding or subtracting the full width overshoots into the next class.',
                fast='Width = difference of marks; limit = mark ± width/2.', secs=30, d='moderate', topic=A_FD, check=frx(v), k='ch13.marks', data={'marks': marks, 'i': i, 'kind': kind})


def nclasses(r):
    lo = r.randint(5, 200); rng = r.randint(40, 400); w = r.choice([5, 10, 15, 20, 25])
    k = math.ceil(F(rng, w)) if rng % w else rng // w + 1
    hi = lo + rng
    return dict(q=f'The smallest observation is {lo} and the largest is {hi}. Using exclusive classes of width {w} starting at {lo}, how many classes are needed so that every observation is included?', a=str(k),
                w=[str(k - 1), str(k + 1), str(rng // w if rng // w not in (k, k - 1, k + 1) else k + 2), str(math.ceil(hi / w))],
                ex=f'Range = {hi} − {lo} = {rng}. Classes {lo}–{lo + w}, {lo + w}–{lo + 2 * w}, … each include the lower limit and exclude the upper limit. {rng} ÷ {w} = {num(F(rng, w))}; ' + (f'since the largest value {hi} would be the upper limit of the last class (and excluded), one more class is needed: {k}.' if rng % w == 0 else f'rounding up gives {k} classes.') + ' Too few classes would leave the largest values outside the table.',
                fast='Classes = range ÷ width, rounded up; add one if the maximum falls exactly on an upper limit.', secs=40, d='moderate', topic=A_CLS, check=str(k), k='ch13.ncls', data={'lo': lo, 'hi': hi, 'w': w})


def comp_pct(r):
    names = r.choice(ITEMS); k = 4; vals = [r.randint(5, 60) * 10 for _ in range(k)]; T = sum(vals); i = r.randrange(k)
    v = F(vals[i] * 100, T)
    return dict(q=f'A percentage bar diagram is drawn for: ' + ', '.join(f'{n} {inr(x)}' for n, x in zip(names, vals)) + f'. The length of the {names[i]} segment, as a percentage of the bar, is about:', a=pct(v),
                w=[pct(F(vals[i] * 360, T)), pct(F(vals[i] * 100, T - vals[i])), pct(F(100, k)), pct(v + 5)],
                ex=f'In a percentage (sub-divided) bar each component is shown as its share of the total. Total = {inr(T)}; {names[i]} = {inr(vals[i])}/{inr(T)} × 100 = {num(v)}%. The whole bar always represents 100%, and the segments are stacked in the same order in every bar.',
                fast='Segment share = value ÷ total × 100.', secs=30, d='core', topic=A_DIA, check=f'{vals[i]}*100/{T}', k='ch13.comp', data={'vals': vals, 'i': i})


FACTS1 = [
    ('The point where the "less than" ogive and the "more than" ogive intersect gives the:', 'Median', ['Mean', 'Mode', 'Range'], A_GR, 'The two ogives cross where the cumulative frequency is N/2 from both ends; the x-value of that point is the median.'),
    ('The mode of a frequency distribution can be located graphically with the help of a:', 'Histogram', ['Ogive', 'Pie chart', 'Line diagram'], A_GR, 'In a histogram the tallest rectangle (modal class) and lines joining its corners to the neighbouring bars locate the mode.'),
    ('Joining the mid-points of the tops of adjacent rectangles of a histogram gives a:', 'Frequency polygon', ['Ogive', 'Pie chart', 'Bar chart'], A_GR, 'The frequency polygon joins the mid-points of the tops of the rectangles (at the class marks); an ogive plots cumulative frequencies instead.'),
    ('Data collected by an investigator for the first time, for a specific purpose, are called:', 'Primary data', ['Secondary data', 'Published data', 'Classified data'], A_COL, 'Primary data are original, first-hand data; once they are published and used by someone else, they become secondary data for that user.'),
    ('Classification of data according to time (years, months) is called:', 'Chronological classification', ['Geographical classification', 'Qualitative classification', 'Quantitative classification'], A_CLS, 'Time-based classification is chronological; place-based is geographical (spatial); attribute-based is qualitative; measurement-based is quantitative.'),
    ('The part of a statistical table that describes the rows is called the:', 'Stub', ['Caption', 'Body', 'Footnote'], A_TAB, 'The stub is the left-hand column with the row headings; captions are the column headings and the body holds the figures.'),
    ('Which of the following is a limitation of statistics?', 'It does not study individual cases', ['It deals with aggregates of facts', 'It uses numerical data', 'It helps in comparison'], A_LIM, 'Statistics deals with groups (aggregates); a single isolated figure about one individual is not a statistic, which is why it does not study individuals.'),
    ('Data classified according to place (states, cities) is an example of:', 'Geographical classification', ['Chronological classification', 'Qualitative classification', 'Ordinal classification'], A_CLS, 'Region or place as the basis of grouping is geographical (spatial) classification.'),
]

FACTS2 = [
    ('Sampling error can generally be reduced by:', 'Increasing the sample size', ['Decreasing the sample size', 'Using a census', 'Removing non-response'], B_ERR, 'Sampling error arises because only part of the population is studied; it falls as the sample size increases (standard error ∝ 1/√n).'),
    ('Non-sampling errors can occur in:', 'Both sample surveys and complete enumeration', ['Sample surveys only', 'Complete enumeration only', 'Neither'], B_ERR, 'Errors of measurement, recording, non-response and processing can happen whether we study a sample or the whole population.'),
    ('The standard deviation of the sampling distribution of a statistic is called its:', 'Standard error', ['Sampling error', 'Bias', 'Variance'], B_SE, 'The spread of a statistic from sample to sample is measured by its standard deviation, which is named the standard error.'),
    ('Selecting every k-th unit from a list after a random start is called:', 'Systematic sampling', ['Stratified sampling', 'Cluster sampling', 'Purposive sampling'], B_TYP, 'A random start followed by a fixed interval k = N/n is systematic sampling.'),
    ('Dividing the population into homogeneous groups and drawing a random sample from each group is:', 'Stratified sampling', ['Systematic sampling', 'Multi-stage sampling', 'Quota sampling'], B_TYP, 'Homogeneous sub-groups are strata; sampling from each stratum is stratified random sampling.'),
    ('The lottery method is a way of drawing a:', 'Simple random sample', ['Purposive sample', 'Systematic sample', 'Quota sample'], B_TYP, 'Lottery (or random number tables) gives every unit an equal chance of selection, which defines simple random sampling.'),
    ('A sample is preferred to complete enumeration especially when:', 'The population is infinite or testing destroys the item', ['The population is very small', 'Every unit must be studied', 'No time limit exists'], B_CEN, 'For infinite populations or destructive tests (e.g. testing bulbs till they fuse) a census is impossible or self-defeating, so sampling is used.'),
    ('A characteristic calculated from sample observations is called a:', 'Statistic', ['Parameter', 'Constant', 'Population'], B_SE, 'Measures computed from the population are parameters; the same measures computed from a sample are statistics.'),
]


def fact_maker(facts, key):
    state = {'i': 0}
    def fact(r):
        i = r.randrange(len(facts)); stem, ans, ws, topic, why = facts[i]
        return dict(q=stem, a=ans, w=ws, ex=f'{why} So the correct answer is "{ans}". The other options describe different terms, so read the key word in the question carefully before choosing.',
                    fast='Recall the definition keyword; eliminate options that describe a different tool or term.', secs=20, d='core', topic=topic, k='ch13.fact', data={'_t': 0})
    fact.__name__ = 'fact_' + key
    return fact


fact1 = fact_maker(FACTS1, 'u01')
fact2 = fact_maker(FACTS2, 'u02')


# ---------- sampling (u02) ----------
def n_samples(r):
    N = r.randint(6, 20); n = r.randint(2, 4); kind = r.choice(['wor', 'wr'])
    v = math.comb(N, n) if kind == 'wor' else N ** n
    how = 'without replacement (order of selection ignored)' if kind == 'wor' else 'with replacement (counting ordered draws)'
    return dict(q=f'How many different samples of size {n} can be drawn from a population of {N} units by simple random sampling {how}?', a=inr(v),
                w=[inr(N ** n if kind == 'wor' else math.comb(N, n)), inr(math.perm(N, n)) if kind == 'wor' else inr(math.comb(N + n - 1, n)), inr(N * n), inr(v + N)],
                ex=(f'Without replacement and ignoring order, the number of samples is ᴺCₙ = {N}C{n} = {inr(v)}.' if kind == 'wor' else f'With replacement each of the {n} draws can be any of the {N} units, so there are Nⁿ = {N}^{n} = {inr(v)} ordered samples.') + ' This count matters when listing the sampling distribution of a statistic, because every possible sample must appear once in that list.',
                fast='Without replacement use ᴺCₙ; with replacement (ordered) use Nⁿ.', secs=25, d='core', topic=B_SE, check=str(v), k='ch13.nsamp', data={'N': N, 'n': n, 'kind': 'without' if kind == 'wor' else 'with'})


def se_mean(r):
    s = r.choice([4, 5, 6, 8, 10, 12, 15, 20, 24, 30]); n = r.choice([4, 9, 16, 25, 36, 49, 64, 100, 144])
    v = F(s, math.isqrt(n))
    return dict(q=f'A population has standard deviation {s}. The standard error of the mean of a random sample of size {n} (large population) is:', a=num(v, 2), w=[num(F(s, n), 3), num(F(s * s, n), 2), num(s * math.isqrt(n)), num(F(s, math.isqrt(n - 1)) if math.isqrt(n - 1) else v + 1, 2)],
                ex=f'SE of the sample mean = σ/√n = {s}/√{n} = {s}/{math.isqrt(n)} = {num(v)}. Dividing by n instead of √n understates the error. Quadrupling the sample size halves the standard error, which is why larger samples give more reliable estimates.',
                fast='σ ÷ √n — pick n as a perfect square and divide.', secs=20, d='core', topic=B_SE, check=f'{s}/{n}**0.5', k='ch13.se', data={'s': s, 'n': n})


def se_fpc(r):
    N = r.randint(50, 500); n = r.randint(10, 40); s = r.randint(3, 25)
    v = s / math.sqrt(n) * math.sqrt((N - n) / (N - 1))
    return dict(q=f'From a population of {N} units with standard deviation {s}, a sample of {n} is drawn without replacement. The standard error of the sample mean (with finite population correction) is about:', a=num(v, 3),
                w=[num(s / math.sqrt(n), 3), num(s / n * math.sqrt((N - n) / (N - 1)), 3), num(s / math.sqrt(n) * (N - n) / (N - 1), 3), num(s / math.sqrt(n) * math.sqrt((N - 1) / (N - n)), 3)],
                ex=f'SE = (σ/√n) × √[(N − n)/(N − 1)] = ({s}/√{n}) × √({N - n}/{N - 1}) = {num(s / math.sqrt(n), 4)} × {num(math.sqrt((N - n) / (N - 1)), 4)} ≈ {num(v, 3)}. The correction factor is below 1, so sampling without replacement from a finite population reduces the error.',
                fast='Compute σ/√n first, then multiply by √((N − n)/(N − 1)).', secs=60, d='moderate', topic=B_SE, check=f'round({s}/{n}**0.5*(({N}-{n})/({N}-1))**0.5,3)', k='ch13.fpc', data={'N': N, 'n': n, 's': s})


def se_prop(r):
    p = r.choice([F(1, 10), F(1, 5), F(1, 4), F(2, 5), F(1, 2), F(3, 5), F(3, 4)]); n = r.choice([25, 36, 64, 100, 144, 225, 400])
    v = math.sqrt(float(p * (1 - p)) / n)
    return dict(q=f'In a large town the proportion of households that own a two-wheeler is {num(p)}. The standard error of this proportion in a random sample of {n} households is about:', a=num(v, 4),
                w=[num(float(p * (1 - p)) / n, 4), num(math.sqrt(float(p) / n), 4), num(math.sqrt(float(p * (1 - p))) / n, 4), num(math.sqrt(float(p * (1 - p)) / n) * 2, 4), num(math.sqrt(float(p * (1 - p)) / n) + 0.01, 4)],
                ex=f'SE(p) = √(PQ/n) with P = {num(p)} and Q = 1 − P = {num(1 - p)}: √({num(p)} × {num(1 - p)}/{n}) = √{num(float(p * (1 - p)) / n, 6)} ≈ {num(v, 4)}. Forgetting the square root gives the variance, not the standard error. The SE is largest when P = 0.5.',
                fast='Multiply P × Q, divide by n, take the square root.', secs=40, d='moderate', topic=B_SE, check=f'round(({float(p)}*{float(1 - p)}/{n})**0.5,4)', k='ch13.seprop', data={'p': float(p), 'n': n})


def systematic(r):
    n = r.randint(5, 20); k = r.randint(4, 25); N = n * k; start = r.randint(1, k); j = r.randint(3, n)
    v = start + (j - 1) * k
    return dict(q=f'A systematic sample of {n} units is to be drawn from a list of {N} units. If the random start is {start}, the {ordn(j)} unit selected is number:', a=str(v),
                w=[str(start + j * k), str(start * j), str(v - 1), str(j * k)],
                ex=f'Sampling interval k = N/n = {N}/{n} = {k}. Units selected: {start}, {start + k}, {start + 2 * k}, …, i.e. start + (j − 1)k. The {ordn(j)} unit is {start} + {j - 1} × {k} = {v}. Only the first unit is chosen at random; the rest follow automatically.',
                fast='Interval k = N ÷ n; jth unit = start + (j − 1)k.', secs=30, d='core', topic=B_TYP, check=str(v), k='ch13.sys', data={'n': n, 'N': N, 'start': start, 'j': j})


def stratified(r):
    sizes = [r.randint(2, 30) * 100 for _ in range(r.randint(3, 4))]; N = sum(sizes); n = r.choice([50, 60, 80, 100, 120, 150, 200]); i = r.randrange(len(sizes))
    v = F(n * sizes[i], N)
    if v.denominator != 1: return None
    return dict(q=f'A population has strata of sizes {", ".join(inr(s) for s in sizes)}. With proportional allocation, a total sample of {n} gives how many units from the stratum of size {inr(sizes[i])}?', a=str(v),
                w=[str(n // len(sizes)), str(round(n * sizes[i] / (N - sizes[i]))), str(int(v) + 1), str(round(sizes[i] / 100))],
                ex=f'Proportional allocation: nᵢ = n × Nᵢ/N. Total N = {inr(N)}. So nᵢ = {n} × {inr(sizes[i])}/{inr(N)} = {v}. Equal allocation ({n // len(sizes)} each) ignores the different stratum sizes. Bigger strata therefore contribute more units to the sample.',
                fast='Sample share of a stratum = its share of the population.', secs=35, d='moderate', topic=B_TYP, check=str(v), k='ch13.strat', data={'sizes': sizes, 'n': n, 'i': i})


def sample_size(r):
    s = r.choice([5, 6, 8, 10, 12, 15, 20, 30]); se = r.choice([F(1, 2), 1, 2, F(3, 2), F(5, 2)])
    v = F(s) ** 2 / F(se) ** 2
    if v.denominator != 1: return None
    return dict(q=f'The population standard deviation is {s}. What sample size is needed so that the standard error of the mean is {num(se)}?', a=str(v),
                w=[str(int(F(s) / F(se))), str(int(v) * 2), str(s * s), str(int(v) + s)],
                ex=f'SE = σ/√n, so √n = σ/SE = {s}/{num(se)} = {num(F(s) / F(se))} and n = {num(F(s) / F(se))}² = {v}. Stopping at √n is the usual slip. Halving the SE needs four times the sample, because the SE falls only with the square root of n.',
                fast='Required sample size n = (σ ÷ SE) squared.', secs=30, d='moderate', topic=B_SE, check=str(v), k='ch13.size', data={'s': s, 'se': float(se)})


def mean_of_means(r):
    pop = sorted(r.sample(range(1, 30), r.randint(4, 6))); n = 2
    mu = F(sum(pop), len(pop))
    if mu.denominator > 2: return None
    return dict(q=f'All possible samples of size 2 are drawn without replacement from the population {{{", ".join(map(str, pop))}}}. The mean of the sampling distribution of the sample mean is:', a=num(mu),
                w=[num(F(sum(pop), len(pop) - 1)), num(F(pop[0] + pop[-1], 2)) if F(pop[0] + pop[-1], 2) != mu else num(mu + 1), num(F(sum(pop), 2)), num(mu * 2)],
                ex=f'The sample mean is an unbiased estimator: the mean of all possible sample means equals the population mean μ = ({" + ".join(map(str, pop))})/{len(pop)} = {num(mu)}. There is no need to list all {math.comb(len(pop), 2)} samples.',
                fast='The mean of all sample means equals the population mean.', secs=25, d='moderate', topic=B_SE, check=frx(mu), k='ch13.mom', data={'pop': pop})


BANKS = {U1: [(class_mark, 2), (boundary, 2), (density, 2), (rel_freq, 2), (cum_freq, 3), (pie, 2), (width_from_marks, 2), (nclasses, 2), (comp_pct, 1), (fact1, 6)],
         U2: [(n_samples, 3), (se_mean, 3), (se_fpc, 3), (se_prop, 2), (systematic, 2), (stratified, 2), (sample_size, 2), (mean_of_means, 2), (fact2, 5)]}
