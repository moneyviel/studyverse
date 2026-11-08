"""Paper 3 Ch 14 — Central Tendency (u01) and Dispersion (u02): extra MCQ templates (exact arithmetic)."""
from common import *
import math

U1, U2 = 'fnd-p3-ch14-u01', 'fnd-p3-ch14-u02'
A_AM, A_MED, A_PART, A_MODE, A_GH, A_CMP = 'Arithmetic mean and its properties', 'Median', 'Partition values — quartiles, deciles, percentiles', 'Mode and the empirical relationship', 'Geometric mean and harmonic mean', 'AM ≥ GM ≥ HM, weighted averages and choosing an average'
B_REL, B_RNG, B_MD, B_SD, B_QD = 'Why dispersion? Absolute vs relative measures', 'Range and coefficient of range', 'Mean deviation', 'Standard deviation, variance and coefficient of variation', 'Quartile deviation and choosing a measure'


def L(xs): return ', '.join(map(str, xs))


def mean_list(r):
    xs = [r.randint(5, 99) for _ in range(r.randint(6, 10))]; m = F(sum(xs), len(xs))
    if m.denominator not in (1, 2, 4, 5): return None
    return dict(q=f'The arithmetic mean of {L(xs)} is:', a=num(m), w=[num(F(sum(xs), len(xs) - 1)), num(F(min(xs) + max(xs), 2)) if F(min(xs) + max(xs), 2) != m else num(m + 1), num(sorted(xs)[len(xs) // 2]) if sorted(xs)[len(xs) // 2] != m else num(m - 1), num(m + F(1, 2))],
                ex=f'Mean = sum ÷ number of observations = {sum(xs)} ÷ {len(xs)} = {num(m)}. A quick check: the sum of deviations from the mean is always zero. The average of the smallest and largest values is the mid-range, not the mean.',
                fast='Assumed mean: subtract a round number from each value, average the small deviations, add back.', secs=40, d='core', topic=A_AM, check=frx(m), k='ch14.mean', data={'xs': xs})


def combined(r):
    n1, n2 = r.randint(10, 80), r.randint(10, 80); m1, m2 = r.randint(30, 90), r.randint(30, 90)
    if m1 == m2: return None
    m = F(n1 * m1 + n2 * m2, n1 + n2)
    return dict(q=f'Group A has {n1} students with mean marks {m1}; group B has {n2} students with mean marks {m2}. The combined mean is:', a=num(m), w=[num(F(m1 + m2, 2)), num(F(n1 * m2 + n2 * m1, n1 + n2)), num(F(n1 * m1 + n2 * m2, n1 + n2 - 1)), num(m + 1)],
                ex=f'Combined mean = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂) = ({n1} × {m1} + {n2} × {m2})/{n1 + n2} = {n1 * m1 + n2 * m2}/{n1 + n2} = {num(m)}. The simple average ({num(F(m1 + m2, 2))}) is right only when both groups are the same size. The combined mean always lies between the two group means.',
                fast='Weighted average: the answer lies between the two means, closer to the bigger group.', secs=35, d='core', topic=A_AM, check=frx(m), k='ch14.comb', data={'n1': n1, 'm1': m1, 'n2': n2, 'm2': m2})


def corrected(r):
    n = r.randint(10, 60); m = r.randint(20, 80); wrong = r.randint(10, 99); right = r.randint(10, 99)
    if wrong == right: return None
    cm = F(n * m - wrong + right, n)
    return dict(q=f'The mean of {n} observations was found to be {m}. Later it was found that one observation {right} was wrongly read as {wrong}. The correct mean is:', a=num(cm),
                w=[num(F(n * m + wrong - right, n)), num(F(n * m - wrong + right, n - 1)), num(m + right - wrong), num(F(n * m - wrong, n - 1))],
                ex=f'Wrong total = {n} × {m} = {n * m}. Correct total = {n * m} − {wrong} + {right} = {n * m - wrong + right}. Correct mean = {n * m - wrong + right}/{n} = {num(cm)}. The number of observations does not change; only the total is corrected.',
                fast=f'Shift the mean by (right − wrong)/n = ({right} − {wrong})/{n}.', secs=35, d='core', topic=A_AM, check=frx(cm), k='ch14.corr', data={'n': n, 'm': m, 'wrong': wrong, 'right': right})


def weighted(r):
    k = r.randint(3, 4); xs = [r.randint(40, 99) for _ in range(k)]; ws = [r.randint(1, 6) for _ in range(k)]
    m = F(sum(x * w for x, w in zip(xs, ws)), sum(ws))
    subj = ['Accounts', 'Law', 'Maths', 'Economics'][:k]
    return dict(q=f'A student scores ' + ', '.join(f'{x} in {s} (weight {w})' for x, s, w in zip(xs, subj, ws)) + '. The weighted average score is:', a=num(m), w=[num(F(sum(xs), k)), num(F(sum(x * w for x, w in zip(xs, ws)), k)), num(F(sum(xs) * sum(ws), k * sum(ws)) + 1), num(m + 2)],
                ex=f'Weighted mean = Σwx/Σw = ({" + ".join(f"{w}×{x}" for x, w in zip(xs, ws))})/{sum(ws)} = {sum(x * w for x, w in zip(xs, ws))}/{sum(ws)} = {num(m)}. Ignoring the weights gives the simple mean {num(F(sum(xs), k))}. Weights show the relative importance of each item, so items with bigger weights pull the average towards themselves.',
                fast='Multiply each score by its weight, add, divide by the total weight.', secs=40, d='core', topic=A_CMP, check=frx(m), k='ch14.wmean', data={'xs': xs, 'ws': ws})


def median_list(r):
    xs = [r.randint(5, 99) for _ in range(r.randint(7, 12))]; s = sorted(xs); n = len(s)
    med = F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)
    return dict(q=f'The median of {L(xs)} is:', a=num(med), w=[num(xs[n // 2]) if xs[n // 2] != med else num(med + 1), num(F(sum(xs), n)) if F(sum(xs), n) != med else num(med + 2), num(s[n // 2 - 1]) if s[n // 2 - 1] != med else num(med - 1), num(s[(n + 1) // 2]) if s[(n + 1) // 2] != med else num(med + 3)],
                ex=f'Arrange in order: {L(s)}. With n = {n} ({"odd" if n % 2 else "even"}), the median is ' + (f'the {(n + 1) // 2}th value = {num(med)}.' if n % 2 else f'the average of the {n // 2}th and {n // 2 + 1}th values = ({s[n // 2 - 1]} + {s[n // 2]})/2 = {num(med)}.') + ' Taking the middle value without sorting is the usual error. The median is not affected by extreme values, which makes it useful for skewed data such as incomes.',
                fast='Sort first; middle position = (n + 1)/2.', secs=40, d='core', topic=A_MED, check=frx(med), k='ch14.med', data={'xs': xs})


def grouped(r, kind):
    k = r.randint(5, 6); w = r.choice([10, 20]); lo = r.choice([0, 10, 20, 100]); f = [r.randint(3, 25) for _ in range(k)]
    cls = [(lo + i * w, lo + (i + 1) * w) for i in range(k)]; N = sum(f)
    if kind == 'median':
        c = 0; i = 0
        while c + f[i] < F(N, 2): c += f[i]; i += 1
        l = cls[i][0]; v = l + (F(N, 2) - c) / f[i] * w
        if c + f[i] == F(N, 2): return None
        ex = f'N = {N}, N/2 = {num(F(N, 2))}. Cumulative frequencies reach N/2 in the class {cls[i][0]}–{cls[i][1]} (c.f. before it = {c}, f = {f[i]}). Median = l + (N/2 − c.f.)/f × h = {l} + ({num(F(N, 2))} − {c})/{f[i]} × {w} = {num(v)}.'
        wr = [l + (F(N, 2) - c) / f[i], l + F(N, 2) / f[i] * w if l + F(N, 2) / f[i] * w < cls[-1][1] else v + w, F(cls[i][0] + cls[i][1], 2), v + w / F(2)]
        topic = A_MED; fast = 'Find the median class from cumulative frequencies, then interpolate inside it.'
    else:
        i = max(range(k), key=lambda j: f[j])
        if f.count(f[i]) > 1 or i in (0, k - 1): return None
        d1, d2 = f[i] - f[i - 1], f[i] - f[i + 1]; l = cls[i][0]; v = l + F(d1, d1 + d2) * w
        ex = f'The modal class has the highest frequency: {cls[i][0]}–{cls[i][1]} (f = {f[i]}). Mode = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h = {l} + ({f[i]} − {f[i - 1]})/({2 * f[i]} − {f[i - 1]} − {f[i + 1]}) × {w} = {num(v)}.'
        wr = [F(cls[i][0] + cls[i][1], 2), l + F(d1, f[i]) * w, l + F(d2, d1 + d2) * w, v + w / F(2)]
        topic = A_MODE; fast = 'Modal class = highest frequency; plug f₀, f₁, f₂ into the formula.'
    return dict(q=f'For the distribution {"; ".join(f"{a}–{b}: {x}" for (a, b), x in zip(cls, f))}, the {kind} is about:', a=num(v), w=[num(x) for x in wr],
                ex=ex + ' Use class boundaries for l when classes are inclusive.', fast=fast, secs=75, d='moderate', topic=topic, check=f'round({float(v)},2)', k='ch14.grp', data={'kind': kind, 'f': f})


def g_median(r): return grouped(r, 'median')
def g_mode(r): return grouped(r, 'mode')


def empirical(r):
    mean, median = r.randint(20, 90), r.randint(20, 90)
    if mean == median: return None
    mode = 3 * median - 2 * mean; ask = r.choice(['mode', 'median', 'mean'])
    if ask == 'mode':
        q = f'For a moderately skewed distribution, mean = {mean} and median = {median}. The mode is about:'; v = F(mode); w = [3 * mean - 2 * median, F(mean + median, 2), 2 * median - mean, mode + 3]
    elif ask == 'median':
        q = f'For a moderately skewed distribution, mean = {mean} and mode = {mode}. The median is about:'; v = F(median); w = [F(2 * mean + mode, 3) + 1, F(mean + mode, 2), F(mean + 2 * mode, 3), median + 2]
    else:
        q = f'For a moderately skewed distribution, median = {median} and mode = {mode}. The mean is about:'; v = F(mean); w = [F(3 * median - mode, 3), F(median + mode, 2), 2 * median - mode, mean + 2]
    return dict(q=q, a=num(v), w=[num(x) for x in w],
                ex=f'Empirical relationship (Karl Pearson): Mode = 3 Median − 2 Mean, equivalently Mean − Mode = 3(Mean − Median). With mean {mean}, median {median} and mode {mode}: 3 × {median} − 2 × {mean} = {mode}. Solving for the missing value gives {num(v)}.',
                fast='Mode = 3 Median − 2 Mean; rearrange for the unknown.', secs=30, d='core', topic=A_MODE, check=frx(v), k='ch14.emp', data={'given': [x for x in (mean, median, mode)], 'ask': ask})


def gm(r):
    k = r.choice([2, 3]); base = r.choice([2, 3, 5]); es = [r.randint(0, 4) for _ in range(k)]
    if (sum(es)) % k: return None
    xs = [base ** e * r.choice([1]) for e in es]
    if len(set(xs)) < k: return None
    g = base ** (sum(es) // k)
    return dict(q=f'The geometric mean of {L(xs)} is:', a=str(g), w=[num(F(sum(xs), k)), num(F(k, sum(F(1, x) for x in xs))), str(math.prod(xs)) if math.prod(xs) != g else str(g + 1), str(g * base)],
                ex=f'GM = (product of the values)^(1/n) = ({" × ".join(map(str, xs))})^(1/{k}) = {math.prod(xs)}^(1/{k}) = {g}. It is used for averaging ratios and growth rates. The arithmetic mean {num(F(sum(xs), k))} is larger, as AM ≥ GM always for positive numbers.',
                fast=f'Write each value as a power of {base}; GM = {base}^(average power).', secs=30, d='core', topic=A_GH, check=str(g), k='ch14.gm', data={'xs': xs})


def hm_speed(r):
    a, b = r.sample([20, 24, 30, 36, 40, 45, 48, 50, 60, 72, 75, 80, 90], 2); D = r.choice([60, 120, 180, 240, 360])
    h = F(2 * a * b, a + b)
    return dict(q=f'Towns P and Q are {D} km apart. A car goes from P to Q at {a} km/h and comes back from Q to P at {b} km/h. Its average speed for the round trip is:', a=f'{num(h)} km/h',
                w=[f'{num(F(a + b, 2))} km/h', f'{num(math.sqrt(a * b))} km/h' if math.isqrt(a * b) ** 2 == a * b else f'{num(F(a + b, 2) + 2)} km/h', f'{num(h - 2)} km/h', f'{num(F(a * b, a + b))} km/h'],
                ex=f'For equal distances, average speed = total distance/total time = 2D/(D/{a} + D/{b}) = 2 × {a} × {b}/({a} + {b}) = {num(h)} km/h, the harmonic mean. The simple average {num(F(a + b, 2))} km/h is wrong because more time is spent at the slower speed.',
                fast='Equal distances ⇒ HM = 2ab/(a + b); the distance does not matter.', secs=30, d='moderate', topic=A_GH, check=frx(h), k='ch14.hm', data={'a': a, 'b': b, 'D': D})


def quartile(r):
    n = r.choice([7, 11, 15, 8, 12]); xs = sorted(r.sample(range(10, 99), n)); which = r.choice([1, 3])
    pos = F(which * (n + 1), 4); i = int(pos); fr_ = pos - i
    v = xs[i - 1] + fr_ * (xs[i] - xs[i - 1]) if fr_ else F(xs[i - 1])
    sh = xs[:]; r.shuffle(sh)
    return dict(q=f'Using the (n + 1) rule, the {"first" if which == 1 else "third"} quartile of {L(sh)} is:', a=num(v),
                w=[num(xs[i]) if xs[i] != v else num(v + 1), num(xs[which * n // 4]) if xs[which * n // 4] != v else num(v + 2), num(xs[n // 2]), num(v - 1)],
                ex=f'Sort: {L(xs)}. Q{which} is at position {which}(n + 1)/4 = {which}({n + 1})/4 = {num(pos)}. ' + (f'Interpolate between the {i}th ({xs[i - 1]}) and {i + 1}th ({xs[i]}) values: {xs[i - 1]} + {num(fr_)} × {xs[i] - xs[i - 1]} = {num(v)}.' if fr_ else f'That is the {i}th value, {num(v)}.') + ' Always sort the data first. Q₁ has a quarter of the observations below it and Q₃ has three quarters below it.',
                fast='Sort, find position k(n + 1)/4, interpolate if it is fractional.', secs=50, d='moderate', topic=A_PART, check=frx(v), k='ch14.quart', data={'xs': sh, 'which': which})


def origin_scale(r):
    a, b, c = r.randint(1, 6), r.choice([-5, -4, -3, -2, 2, 3, 4, 5]), r.randint(-30, 60); mx = r.randint(5, 50)
    stat = r.choice(['mean', 'median', 'mode'])
    # a x + b y = c  -> y = (c - a x)/b
    v = F(c - a * mx, b)
    return dict(q=f'Two variables are related by {poly([a, 0])} {signed(b, "y")} = {c}. If the {stat} of x is {mx}, the {stat} of y is:', a=num(v),
                w=[num(F(c - b * mx, a)), num(F(c + a * mx, b)), num(-v) if v else '1', num(F(c - a * mx, abs(b)) if b < 0 else v + 1)],
                ex=f'Rewrite: y = ({c} − {a}x)/{b}. Averages (mean, median, mode) follow the same linear change of origin and scale, so {stat} of y = ({c} − {a} × {mx})/{b} = {num(v)}. Keep the sign of {b} when dividing.',
                fast='Put the given average of x straight into the equation and solve for y.', secs=30, d='core', topic=A_AM, check=frx(v), k='ch14.lin', data={'a': a, 'b': b, 'c': c, 'mx': mx})


def am_gm(r):
    a, b = r.sample([1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48], 2)
    if math.isqrt(a * b) ** 2 != a * b: return None
    A, G = F(a + b, 2), math.isqrt(a * b); H = F(G * G) / A; kind = r.choice(['hm', 'nums'])
    if kind == 'hm':
        return dict(q=f'The arithmetic mean of two positive numbers is {num(A)} and their geometric mean is {G}. Their harmonic mean is:', a=num(H), w=[num(A - G) if A - G != H else num(H + 1), num(A / G), num(F(G * G, 1)), num(2 * G - A) if 2 * G - A != H else num(H + 2)],
                    ex=f'For two positive numbers, GM² = AM × HM. So HM = GM²/AM = {G * G}/{num(A)} = {num(H)}. This also confirms AM ≥ GM ≥ HM: {num(A)} ≥ {G} ≥ {num(H)}. (The numbers are {min(a, b)} and {max(a, b)}.)',
                    fast='HM = GM² ÷ AM for two numbers.', secs=25, d='moderate', topic=A_CMP, check=frx(H), k='ch14.amgm', data={'A': float(A), 'G': G, 'kind': 'harmonic'})
    lo, hi = sorted((a, b))
    return dict(q=f'The arithmetic mean of two positive numbers is {num(A)} and their geometric mean is {G}. The larger number is:', a=str(hi), w=[str(lo), num(A + G), str(G * 2), num(A * 2 - G)],
                ex=f'Sum = 2 × AM = {num(2 * A)} and product = GM² = {G * G}. The numbers are the roots of t² − {num(2 * A)}t + {G * G} = 0, i.e. {lo} and {hi}. The larger number is {hi}.',
                fast=f'Find two numbers with sum {num(2 * A)} and product {G * G} — test the options.', secs=40, d='moderate', topic=A_CMP, check=str(hi), k='ch14.amgm', data={'A': float(A), 'G': G, 'kind': 'larger'})


def missing_val(r):
    xs = [r.randint(5, 60) for _ in range(r.randint(4, 7))]; x = r.randint(5, 60); n = len(xs) + 1; s = sum(xs) + x
    m = F(s, n)
    if m.denominator != 1: return None
    return dict(q=f'The mean of the values {L(xs)} and x is {m}. Then x =', a=str(x), w=[str(int(m)), str(x + n), str(int(m) * len(xs) - sum(xs)) if int(m) * len(xs) - sum(xs) != x else str(x - 1), str(x + 1)],
                ex=f'Total of all {n} values = mean × n = {m} × {n} = {s}. The given values add to {sum(xs)}, so x = {s} − {sum(xs)} = {x}. Dividing by {n - 1} instead of {n} forgets that x is itself one of the observations.',
                fast='x = mean × (number of values) − sum of the known values.', secs=30, d='core', topic=A_AM, check=str(x), k='ch14.miss', data={'xs': xs, 'm': int(m)})


# ---------------- Dispersion (u02) ----------------
def rng_coef(r):
    xs = [r.randint(10, 150) for _ in range(r.randint(6, 9))]; hi, lo = max(xs), min(xs); kind = r.choice(['range', 'coef'])
    if kind == 'range':
        return dict(q=f'The range of {L(xs)} is:', a=str(hi - lo), w=[str(hi + lo), num(F(hi - lo, hi + lo), 4), str(sorted(xs)[-2] - sorted(xs)[1]), str(hi)],
                    ex=f'Range = largest − smallest = {hi} − {lo} = {hi - lo}. It is the simplest absolute measure of dispersion but depends only on the two extreme values, so a single outlier changes it a lot.',
                    fast='Spot the maximum and minimum and subtract.', secs=20, d='core', topic=B_RNG, check=str(hi - lo), k='ch14.range', data={'xs': xs, 'kind': kind})
    v = F(hi - lo, hi + lo)
    return dict(q=f'The coefficient of range of {L(xs)} is:', a=num(v, 4), w=[str(hi - lo), num(F(hi - lo, hi), 4), num(F(hi + lo, hi - lo), 4), num(F(hi - lo, sum(xs)), 4)],
                ex=f'Coefficient of range = (L − S)/(L + S) = ({hi} − {lo})/({hi} + {lo}) = {hi - lo}/{hi + lo} = {num(v, 4)}. Being a ratio, it has no units and is used to compare spread across different series.',
                fast='(Max − Min) ÷ (Max + Min).', secs=25, d='core', topic=B_RNG, check=f'round({hi - lo}/{hi + lo},4)', k='ch14.range', data={'xs': xs, 'kind': kind})


def mean_dev(r):
    xs = [r.randint(2, 40) for _ in range(r.randint(5, 8))]; about = r.choice(['mean', 'median']); n = len(xs); s = sorted(xs)
    c = F(sum(xs), n) if about == 'mean' else (F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2))
    if c.denominator > 2: return None
    md = sum(abs(x - c) for x in xs) / n
    other = F(sum(xs), n) if about == 'median' else (F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2))
    return dict(q=f'The mean deviation about the {about} of {L(xs)} is:', a=num(md), w=[num(sum(abs(x - other) for x in xs) / n) if sum(abs(x - other) for x in xs) / n != md else num(md + 1), num(sum(abs(x - c) for x in xs) / (n - 1)), num(math.sqrt(sum((x - c) ** 2 for x in xs) / n)), num(F(0))],
                ex=f'The {about} is {num(c)}. Absolute deviations: {", ".join(num(abs(x - c)) for x in xs)}; their sum is {num(sum(abs(x - c) for x in xs))}. Mean deviation = sum ÷ n = {num(sum(abs(x - c) for x in xs))}/{n} = {num(md)}. Signs are ignored — with signs, deviations from the mean would add to zero.',
                fast='Find the centre, add the distances |x − centre|, divide by n.', secs=60, d='moderate', topic=B_MD, check=f'round({float(md)},2)', k='ch14.md', data={'xs': xs, 'about': about})


def sd_list(r):
    n = r.randint(4, 7); xs = [r.randint(1, 30) for _ in range(n)]; m = F(sum(xs), n)
    if m.denominator > 2: return None
    var = sum((x - m) ** 2 for x in xs) / n; sd = math.sqrt(var)
    return dict(q=f'The standard deviation of {L(xs)} is about:', a=num(sd, 2), w=[num(var, 2), num(math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)), 2), num(sum(abs(x - m) for x in xs) / n, 2), num(sd + 1, 2)],
                ex=f'Mean = {num(m)}. Squared deviations: {", ".join(num((x - m) ** 2) for x in xs)}; sum = {num(sum((x - m) ** 2 for x in xs))}. Variance = sum/n = {num(var)} and SD = √{num(var)} ≈ {num(sd, 2)}. Giving the variance as the SD (forgetting the root) is the trap.',
                fast='Variance = mean of squares − (mean)²; then take the square root.', secs=60, d='moderate', topic=B_SD, check=f'round({sd},2)', k='ch14.sd', data={'xs': xs})


def var_sums(r):
    n = r.randint(10, 50); m = r.randint(5, 40); sd = r.randint(2, 12)
    Sx = n * m; Sx2 = n * (sd * sd + m * m)
    return dict(q=f'For {n} observations, Σx = {inr(Sx)} and Σx² = {inr(Sx2)}. The standard deviation is:', a=str(sd), w=[str(sd * sd), num(math.sqrt(Sx2 / n), 2), str(m), num(math.sqrt(Sx2 / n - m), 2)],
                ex=f'Mean = Σx/n = {inr(Sx)}/{n} = {m}. Variance = Σx²/n − (mean)² = {inr(Sx2)}/{n} − {m}² = {sd * sd + m * m} − {m * m} = {sd * sd}. SD = √{sd * sd} = {sd}. Forgetting to subtract the square of the mean, or forgetting the final square root, are the two common slips.',
                fast='Variance = Σx²/n minus the square of Σx/n.', secs=40, d='moderate', topic=B_SD, check=str(sd), k='ch14.varsum', data={'n': n, 'Sx': Sx, 'Sx2': Sx2})


def cv(r):
    m = r.randint(20, 200); sd = r.randint(2, 40); kind = r.choice(['cv', 'sd', 'compare'])
    if kind == 'cv':
        v = F(sd * 100, m)
        return dict(q=f'A series has mean {m} and standard deviation {sd}. Its coefficient of variation is:', a=pct(v), w=[pct(F(m * 100, sd)), pct(F(sd, m)), pct(F(sd * sd * 100, m)), pct(v + 5)],
                    ex=f'CV = (SD ÷ mean) × 100 = {sd}/{m} × 100 = {num(v)}%. It is a relative measure, free of units, so it compares the consistency of series with different means. A lower CV means a more consistent (less variable) series.',
                    fast='Coefficient of variation = SD ÷ mean × 100.', secs=20, d='core', topic=B_SD, check=f'{sd}*100/{m}', k='ch14.cv', data={'m': m, 'sd': sd, 'kind': kind})
    if kind == 'sd':
        c = r.choice([5, 10, 12, 15, 20, 25]); v = F(c * m, 100)
        return dict(q=f'The coefficient of variation of a series is {c}% and its mean is {m}. Its variance is:', a=num(v * v), w=[num(v), num(F(c * 100, m)), num(v * v / 100), num(c * m)],
                    ex=f'CV = SD/mean × 100 ⇒ SD = CV × mean/100 = {c} × {m}/100 = {num(v)}. Variance = SD² = {num(v * v)}. Stopping at the SD ({num(v)}) answers a different question, so read whether the SD or the variance is asked.',
                    fast='SD = CV% × mean; variance = SD squared.', secs=30, d='moderate', topic=B_SD, check=frx(v * v), k='ch14.cv', data={'m': m, 'c': c, 'kind': kind})
    m2, sd2 = r.randint(20, 200), r.randint(2, 40)
    c1, c2 = F(sd, m), F(sd2, m2)
    if c1 == c2: return None
    ans = 'Series A' if c1 < c2 else 'Series B'
    return dict(q=f'Series A: mean {m}, SD {sd}. Series B: mean {m2}, SD {sd2}. Which series is more consistent?', a=ans, w=['Series B' if ans == 'Series A' else 'Series A', 'Both are equally consistent', 'Cannot be compared'],
                ex=f'Compare coefficients of variation, not SDs: CV(A) = {sd}/{m} × 100 = {num(c1 * 100)}%, CV(B) = {sd2}/{m2} × 100 = {num(c2 * 100)}%. The lower CV means less relative variation, so {ans} is more consistent. Comparing the SDs directly would mislead because the means differ.',
                fast='Lower SD/mean ratio = more consistent.', secs=35, d='core', topic=B_REL, k='ch14.cvcmp', data={'m': m, 'sd': sd, 'm2': m2, 'sd2': sd2})


def qd(r):
    q1 = r.randint(10, 80); q3 = q1 + r.randint(4, 60); kind = r.choice(['qd', 'coef'])
    if kind == 'qd':
        v = F(q3 - q1, 2)
        return dict(q=f'If Q₁ = {q1} and Q₃ = {q3}, the quartile deviation is:', a=num(v), w=[str(q3 - q1), num(F(q3 - q1, q3 + q1), 4), num(F(q3 + q1, 2)), num(v + 1)],
                    ex=f'Quartile deviation (semi-interquartile range) = (Q₃ − Q₁)/2 = ({q3} − {q1})/2 = {num(v)}. It ignores the top and bottom 25% of the data, so extreme values do not affect it. It is the preferred measure of spread for open-ended distributions.',
                    fast='Half the gap between Q₃ and Q₁.', secs=15, d='core', topic=B_QD, check=frx(v), k='ch14.qd', data={'q1': q1, 'q3': q3, 'kind': kind})
    v = F(q3 - q1, q3 + q1)
    return dict(q=f'If Q₁ = {q1} and Q₃ = {q3}, the coefficient of quartile deviation is:', a=num(v, 4), w=[num(F(q3 - q1, 2)), num(F(q3 + q1, q3 - q1), 4), num(F(q3 - q1, q3), 4), num(F(q3 - q1, 2 * (q3 + q1)), 4)],
                ex=f'Coefficient of QD = (Q₃ − Q₁)/(Q₃ + Q₁) = ({q3} − {q1})/({q3} + {q1}) = {q3 - q1}/{q3 + q1} = {num(v, 4)}. As a relative measure it has no units, so it can compare the spread of two series measured in different units.',
                fast='(Q₃ − Q₁) ÷ (Q₃ + Q₁).', secs=20, d='core', topic=B_QD, check=f'round({q3 - q1}/{q3 + q1},4)', k='ch14.qd', data={'q1': q1, 'q3': q3, 'kind': kind})


def sd_special(r):
    kind = r.choice(['two', 'natural'])
    if kind == 'two':
        a, b = r.sample(range(2, 90), 2); v = F(abs(a - b), 2)
        return dict(q=f'The standard deviation of the two numbers {a} and {b} is:', a=num(v), w=[str(abs(a - b)), num(F(a + b, 2)), num(v * v), num(math.sqrt(abs(a - b)), 2)],
                    ex=f'For two values the mean is ({a} + {b})/2 and each value is |a − b|/2 = {num(v)} away from it. So SD = √[(d² + d²)/2] = |a − b|/2 = {num(v)}. Range is {abs(a - b)}, twice the SD here.',
                    fast='SD of two numbers = half their difference.', secs=15, d='core', topic=B_SD, check=frx(v), k='ch14.sd2', data={'a': a, 'b': b})
    n = r.choice([5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]); var = F(n * n - 1, 12)
    return dict(q=f'The variance of the first {n} natural numbers is:', a=num(var), w=[num(F(n * n - 1, 6)), num(F(n + 1, 2)), num(F(n * n + 1, 12)), num(math.sqrt(var), 2)],
                ex=f'For 1, 2, …, n the variance is (n² − 1)/12 = ({n * n} − 1)/12 = {num(var)}. The mean is (n + 1)/2 = {num(F(n + 1, 2))}, which is a different measure. The SD would be √{num(var)}.',
                fast='Variance of 1…n = (n² − 1)/12.', secs=20, d='moderate', topic=B_SD, check=frx(var), k='ch14.nat', data={'n': n})


def sd_linear(r):
    a, b = r.randint(-20, 40), r.choice([-5, -4, -3, -2, 2, 3, 4, 5]); s = r.randint(2, 15); kind = r.choice(['sd', 'range', 'var'])
    word = {'sd': 'standard deviation', 'range': 'range', 'var': 'variance'}[kind]
    v = abs(b) * s if kind != 'var' else b * b * s
    w = [b * s if b < 0 else abs(b) * s + abs(a), abs(a) + s * (1 if kind != 'var' else s), s if kind != 'var' else abs(b) * s, (abs(b) * s) ** 2 if kind != 'var' else abs(b) * s * s * 2]
    return dict(q=f'If y = {poly([b, a])} and the {word} of x is {s}, the {word} of y is:', a=str(v), w=[str(x) for x in w],
                ex=f'Adding a constant ({a}) shifts every value equally, so it does not change spread (change of origin). Multiplying by {b} scales spread by |{b}| (change of scale); variance scales by {b}² = {b * b}. So the {word} of y = {"|" + str(b) + "| × " + str(s) if kind != "var" else str(b * b) + " × " + str(s)} = {v}. Measures of dispersion are never negative.',
                fast='Ignore the added constant; multiply by |b| (or b² for variance).', secs=25, d='core', topic=B_SD if kind != 'range' else B_RNG, check=str(v), k='ch14.lin2', data={'a': a, 'b': b, 's': s, 'kind': word})


def combined_sd(r):
    n1, n2 = r.randint(10, 60), r.randint(10, 60); m1, m2 = r.randint(20, 60), r.randint(20, 60); s1, s2 = r.randint(2, 10), r.randint(2, 10)
    m = F(n1 * m1 + n2 * m2, n1 + n2)
    var = F(n1 * (s1 * s1 + (m1 - m) ** 2) + n2 * (s2 * s2 + (m2 - m) ** 2), n1 + n2)
    v = math.sqrt(var)
    return dict(q=f'Group 1: n = {n1}, mean {m1}, SD {s1}. Group 2: n = {n2}, mean {m2}, SD {s2}. The combined standard deviation is about:', a=num(v, 2),
                w=[num(F(n1 * s1 + n2 * s2, n1 + n2), 2), num(math.sqrt(F(n1 * s1 * s1 + n2 * s2 * s2, n1 + n2)), 2) if m1 != m2 else num(v + 1, 2), num(F(s1 + s2, 2), 2) if F(s1 + s2, 2) != F(n1 * s1 + n2 * s2, n1 + n2) else num(v + 0.5, 2), num(float(var), 2)],
                ex=f'Combined mean = {num(m)}. Combined variance = [n₁(σ₁² + d₁²) + n₂(σ₂² + d₂²)]/(n₁ + n₂), where d = group mean − combined mean: d₁ = {num(m1 - m)}, d₂ = {num(m2 - m)}. This gives {num(var, 4)}, so SD ≈ {num(v, 2)}. Averaging the SDs ignores the gap between the group means.',
                fast='Find the combined mean first; add each group\'s d² to its σ² before weighting.', secs=90, d='hard', topic=B_SD, check=f'round({float(v)},2)', k='ch14.csd', data={'n1': n1, 'm1': m1, 's1': s1, 'n2': n2, 'm2': m2, 's2': s2})


BANKS = {U1: [(mean_list, 2), (combined, 2), (corrected, 2), (weighted, 2), (median_list, 2), (g_median, 3), (g_mode, 3), (empirical, 3), (gm, 2), (hm_speed, 2),
              (quartile, 3), (origin_scale, 2), (am_gm, 2), (missing_val, 2)],
         U2: [(rng_coef, 3), (mean_dev, 3), (sd_list, 3), (var_sums, 2), (cv, 4), (qd, 3), (sd_special, 3), (sd_linear, 3), (combined_sd, 2)]}
