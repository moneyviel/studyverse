"""Paper 3 Ch 16 — Theoretical Distributions: extra MCQ templates.
Binomial answers are exact fractions; Poisson questions state the value of e^(−m) used; normal questions state
the table areas used (each area is computed from the error function and rounded to 4 decimals)."""
from common import *
import math

U = 'fnd-p3-ch16-u01'
C1, C2, C3, C4, C5, C6 = 'Theoretical distributions and the binomial model', 'Properties of the binomial distribution', 'Poisson distribution', 'Where Poisson applies', 'Normal distribution', 'Standard normal variate and using the table'


def area(z): return round(0.5 * math.erf(abs(z) / math.sqrt(2)), 4)     # area between 0 and z


def binom_pt(r):
    n = r.randint(3, 8); p = F(1, r.choice([2, 3, 4, 5, 6])) * r.choice([1, 1, 2]); k = r.randint(0, n)
    if p >= 1: return None
    v = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    ctx = r.choice([f'A fair die is thrown {n} times' if p == F(1, 6) else None, f'{n} items are chosen; each is defective with probability {fr(p)}', f'A student guesses {n} questions, each correct with probability {fr(p)}'])
    if ctx is None: return None
    what = 'a six appears' if ctx.startswith('A fair die') else 'are defective' if 'defective' in ctx else 'are correct'
    q = f'{ctx}. The probability that exactly {k} {"time" if what == "a six appears" and k == 1 else "times" if what == "a six appears" else ""}'.rstrip()
    q = (f'{ctx}. Find the chance of getting a six exactly {k} time{"s" if k != 1 else ""}.' if what == 'a six appears' else f'{ctx}. Find the chance that exactly {k} of them {what if k != 1 else what.replace("are", "is")}.')
    ws = [x for x in (p ** k * (1 - p) ** (n - k), math.comb(n, k) * p ** k, math.comb(n, k) * (1 - p) ** k * p ** (n - k), 1 - v, v / 2, math.comb(n, k) * p ** k * (1 - p) ** (n - k + 1)) if 0 < x < 1]
    return dict(q=q, a=fr(v), w=[fr(x) for x in ws],
                ex=f'Binomial: P(X = r) = ⁿCᵣ pʳ qⁿ⁻ʳ with n = {n}, p = {fr(p)}, q = {fr(1 - p)}, r = {k}. So P = {n}C{k} × ({fr(p)})^{k} × ({fr(1 - p)})^{n - k} = {math.comb(n, k)} × {fr(p ** k)} × {fr((1 - p) ** (n - k))} = {fr(v)}. Forgetting ⁿCᵣ counts only one order of successes.',
                fast='ⁿCᵣ × pʳ × qⁿ⁻ʳ — compute the numerator and the denominator separately.', secs=50, d='moderate', topic=C1, k='ch16.binpt', data={'n': n, 'p': fr(p), 'k': k})


def binom_atleast(r):
    n = r.randint(3, 8); p = F(1, r.choice([2, 3, 4, 5, 10]))
    v = 1 - (1 - p) ** n
    return dict(q=f'The probability that a machine part is defective is {fr(p)}. In a sample of {n} parts, the probability of at least one defective is:', a=fr(v), w=[fr((1 - p) ** n), fr(n * p) if n * p < 1 else fr(p ** n), fr(1 - p ** n), fr(n * p * (1 - p) ** (n - 1))],
                ex=f'"At least one" is the complement of "none": P(X ≥ 1) = 1 − P(X = 0) = 1 − q^n = 1 − ({fr(1 - p)})^{n} = 1 − {fr((1 - p) ** n)} = {fr(v)}. Adding P(X = 1), P(X = 2), … one by one is much slower and error-prone.',
                fast='At least one = 1 − qⁿ (complement of none).', secs=30, d='core', topic=C1, k='ch16.binal', data={'n': n, 'p': fr(p)})


def binom_mv(r):
    n = r.randint(5, 100); p = F(r.randint(1, 9), 10); kind = r.choice(['var', 'sd', 'mean'])
    m, v = n * p, n * p * (1 - p)
    if kind == 'mean': val = m; w = [v, n * (1 - p), m + 1]
    elif kind == 'var': val = v; w = [m, n * p * p, v * 2]
    else:
        if math.isqrt((v * 100).numerator) ** 2 != (v * 100).numerator or (v * 100).denominator != 1: return None
        val = F(math.isqrt(int(v * 100)), 10); w = [v, m, val + 1]
    word = {'mean': 'mean', 'var': 'variance', 'sd': 'standard deviation'}[kind]
    return dict(q=f'For a binomial distribution with n = {n} and p = {num(p)}, the {word} is:', a=num(val), w=[num(x) for x in w] + [num(val + F(1, 2))],
                ex=f'Binomial mean = np = {n} × {num(p)} = {num(m)}; variance = npq = {n} × {num(p)} × {num(1 - p)} = {num(v)}; SD = √(npq). So the {word} is {num(val)}. The variance of a binomial is always smaller than its mean because q < 1.',
                fast='Mean np, variance npq, SD √(npq).', secs=20, d='core', topic=C2, check=frx(val), k='ch16.binmv', data={'n': n, 'p': float(p), 'kind': word})


def binom_np(r):
    n = r.randint(4, 60); p = F(r.randint(1, 9), 10)
    m, v = n * p, n * p * (1 - p)
    kind = r.choice(['n', 'p'])
    val = F(n) if kind == 'n' else p
    return dict(q=f'A binomial distribution has mean {num(m)} and variance {num(v)}. The value of {"n" if kind == "n" else "p"} is:', a=num(val), w=[num(1 - p) if kind == 'p' else num(m), num(v / m) if kind == 'p' else num(m * m / v) if m * m / v != n else num(n + 1), num(p * 2) if kind == 'p' and p * 2 < 1 else num(n * 2), num(F(m, 10)) if kind == 'p' else num(n - 1)],
                ex=f'Variance ÷ mean = npq/np = q, so q = {num(v)}/{num(m)} = {num(1 - p)} and p = 1 − q = {num(p)}. Then n = mean/p = {num(m)}/{num(p)} = {n}. Taking q as p is the usual error.',
                fast='q = variance ÷ mean; p = 1 − q; n = mean ÷ p.', secs=35, d='moderate', topic=C2, check=frx(val), k='ch16.binnp', data={'m': float(m), 'v': float(v), 'kind': kind})


EM = {0.5: 0.6065, 1: 0.3679, 1.5: 0.2231, 2: 0.1353, 2.5: 0.0821, 3: 0.0498, 4: 0.0183, 5: 0.0067}


def pois_pt(r):
    m = r.choice(list(EM)); k = r.randint(0, 4); e = EM[m]
    v = m ** k * e / math.factorial(k)
    ctx = r.choice(['The number of accidents per day on a road', 'The number of printing mistakes per page of a book', 'The number of calls per minute at a switchboard', 'The number of defects per metre of cloth'])
    return dict(q=f'{ctx} follows a Poisson distribution with mean {num(m)}. Given e^(−{num(m)}) = {e}, the probability of exactly {k} is about:', a=numf(v, 4),
                w=[numf(m ** k * e, 4) if k > 1 else numf(e * 2, 4), numf(e, 4) if k else numf(m * e, 4), numf(1 - v, 4), numf(m ** (k + 1) * e / math.factorial(k + 1), 4)],
                ex=f'Poisson: P(X = r) = e^(−m) mʳ/r!. With m = {num(m)} and r = {k}: {e} × {num(m)}^{k}/{k}! = {e} × {num(m ** k, 4)}/{math.factorial(k)} = {numf(v, 4)}. Forgetting to divide by r! gives too large a value. In a Poisson distribution the mean and the variance are both equal to m.',
                fast='e^(−m) × mʳ ÷ r! — use the e^(−m) value given in the question.', secs=40, d='moderate', topic=C3, check=f'round({m}**{k}*{e}/{math.factorial(k)},4)', k='ch16.poispt', data={'m': m, 'e': e, 'k': k})


def pois_equal(r):
    k = r.randint(1, 4); m = k + 1; kind = r.choice(['m', 'sd'])
    if kind == 'm':
        return dict(q=f'For a Poisson variate X, P(X = {k}) = P(X = {k + 1}). The mean of the distribution is:', a=str(m), w=[str(k), str(k + 2), num(math.sqrt(m), 4), str(2 * k + 1)],
                    ex=f'e^(−m)m^{k}/{k}! = e^(−m)m^{k + 1}/{k + 1}!. Cancel e^(−m) m^{k}/{k}!: 1 = m/{k + 1}, so m = {m}. In general P(X = r) = P(X = r + 1) gives m = r + 1. The mean of a Poisson distribution equals its variance.',
                    fast='P(r) = P(r + 1) ⇒ m = r + 1.', secs=30, d='moderate', topic=C3, check=str(m), k='ch16.poiseq', data={'k': k, 'kind': 'mean'})
    return dict(q=f'For a Poisson variate X, P(X = {k}) = P(X = {k + 1}). The standard deviation of X is:', a=numf(math.sqrt(m), 4), w=[str(m), numf(math.sqrt(k), 4), str(m * m), numf(math.sqrt(m) / 2, 4)],
                ex=f'P(X = {k}) = P(X = {k + 1}) gives m = {k + 1} = {m}. For a Poisson distribution, mean = variance = m, so SD = √m = √{m} ≈ {numf(math.sqrt(m), 4)}. Giving the variance ({m}) as the SD is the trap.',
                fast='m = r + 1; SD = √m.', secs=35, d='moderate', topic=C3, check=f'round({m}**0.5,4)', k='ch16.poiseq', data={'k': k, 'kind': 'standard deviation'})


def pois_approx(r):
    n = r.choice([100, 200, 400, 500, 1000, 2000]); m = r.choice([1, 2, 3, 4, 5]); p = F(m, n); e = EM[m]; kind = r.choice([0, 1])
    v = e if kind == 0 else m * e
    return dict(q=f'The probability that an item is defective is {fr(p)}. Using the Poisson approximation (e^(−{m}) = {e}), the probability that a box of {n} items contains {"no" if kind == 0 else "exactly one"} defective is about:', a=numf(v, 4),
                w=[numf(1 - v, 4), numf(m * e, 4) if kind == 0 else numf(e, 4), numf(e / m, 4), numf(v * 2, 4)],
                ex=f'n is large and p is small, so use Poisson with m = np = {n} × {fr(p)} = {m}. P(X = {kind}) = e^(−{m}) × {m}^{kind}/{kind}! = {numf(v, 4)}. Poisson suits rare events: many trials, each with a tiny chance.',
                fast='m = np, then e^(−m) mʳ/r!.', secs=35, d='moderate', topic=C4, check=f'round({v},4)', k='ch16.poisap', data={'n': n, 'p': fr(p), 'e': e, 'kind': kind})


def zscore(r):
    mu = r.randint(20, 200); s = r.randint(2, 30); x = mu + r.choice([-1, 1]) * r.choice([F(1, 2), 1, F(3, 2), 2, F(5, 2), 3]) * s
    if x.denominator != 1: return None
    z = (x - mu) / s
    return dict(q=f'X is normally distributed with mean {mu} and standard deviation {s}. The standard normal variate z for x = {x} is:', a=num(z), w=[num(-z), num((x - mu) / (s * s)), num(x / s), num(z * 2)],
                ex=f'z = (x − μ)/σ = ({x} − {mu})/{s} = {num(z)}. z measures how many standard deviations x lies from the mean; a negative z means x is below the mean. Dividing by the variance instead of the SD is a common slip.',
                fast='Subtract the mean, divide by the SD.', secs=20, d='core', topic=C6, check=frx(z), k='ch16.z', data={'mu': mu, 's': s, 'x': int(x)})


def normal_prob(r):
    mu = r.randint(30, 200); s = r.randint(4, 25); z1 = r.choice([0.5, 1, 1.25, 1.5, 2, 2.5]); kind = r.choice(['above', 'below', 'between', 'between2'])
    x1 = mu + z1 * s
    if x1 != int(x1): return None
    A1 = area(z1)
    if kind == 'above': v = 0.5 - A1; txt = f'more than {int(x1)}'; given = f'area under the standard normal curve between z = 0 and z = {num(z1)} is {A1:.4f}'
    elif kind == 'below': v = 0.5 + A1; txt = f'less than {int(x1)}'; given = f'area between z = 0 and z = {num(z1)} is {A1:.4f}'
    elif kind == 'between': v = 2 * A1; txt = f'between {int(mu - z1 * s)} and {int(x1)}'; given = f'area between z = 0 and z = {num(z1)} is {A1:.4f}'
    else:
        z2 = r.choice([z for z in (0.5, 1, 1.5, 2) if z != z1]); x2 = mu - z2 * s
        if x2 != int(x2): return None
        A2 = area(z2); v = A1 + A2; txt = f'between {int(x2)} and {int(x1)}'; given = f'areas between z = 0 and z = {num(z2)} and between z = 0 and z = {num(z1)} are {A2:.4f} and {A1:.4f}'
    return dict(q=f'X is normal with mean {mu} and SD {s}. Given that the {given}, the probability that X is {txt} is:', a=numf(v, 4), w=[numf(A1, 4), numf(1 - v, 4) if abs(1 - 2 * v) > 1e-9 else numf(v / 2, 4), numf(abs(0.5 - v), 4) if abs(0.5 - v) > 1e-9 and abs(abs(0.5 - v) - A1) > 1e-9 else numf(v + 0.1, 4), numf(v + 0.05, 4)],
                ex=f'Convert to z: z = (x − {mu})/{s}. The normal curve is symmetric and each half has area 0.5. ' + {'above': f'P(X > {int(x1)}) = 0.5 − (area 0 to {num(z1)}) = 0.5 − {A1:.4f} = {v:.4f}.', 'below': f'P(X < {int(x1)}) = 0.5 + {A1:.4f} = {v:.4f}.', 'between': f'The interval is symmetric (z from −{num(z1)} to {num(z1)}), so P = 2 × {A1:.4f} = {v:.4f}.', 'between2': f'The interval crosses the mean, so add the two areas: {v:.4f}.'}[kind] + ' Draw the curve and shade the region before adding or subtracting.',
                fast='Sketch the bell, shade, then add areas on opposite sides of the mean or subtract on the same side.', secs=60, d='moderate', topic=C5, check=f'round({v},4)', k='ch16.norm', data={'mu': mu, 's': s})


def normal_count(r):
    N = r.choice([500, 1000, 2000, 5000]); mu = r.randint(40, 80); s = r.randint(4, 12); z = r.choice([1, 1.5, 2]); x = mu + z * s
    if x != int(x): return None
    A = area(z); v = round(N * (0.5 - A))
    return dict(q=f'Marks of {inr(N)} students are normally distributed with mean {mu} and SD {s}. Given that the area between z = 0 and z = {num(z)} is {A:.4f}, about how many students score above {int(x)}?', a=inr(v),
                w=[inr(round(N * A)), inr(round(N * (0.5 + A))), inr(round(N * (1 - A))), inr(v + 50)],
                ex=f'z = ({int(x)} − {mu})/{s} = {num(z)}. P(X > {int(x)}) = 0.5 − {A:.4f} = {0.5 - A:.4f}. Expected number = {inr(N)} × {0.5 - A:.4f} ≈ {inr(v)}. Multiplying N by the table area itself counts students between the mean and {int(x)}.',
                fast='Tail area = 0.5 − table area; multiply by the number of students.', secs=50, d='moderate', topic=C5, check=str(v), k='ch16.ncount', data={'N': N, 'mu': mu, 's': s})


def md_normal(r):
    s = r.choice([5, 10, 15, 20, 25, 30, 35, 40]); kind = r.choice(['md', 'sd'])
    if kind == 'md':
        v = F(4 * s, 5)
        return dict(q=f'For a normal distribution with standard deviation {s}, the mean deviation about the mean is approximately:', a=num(v), w=[num(F(2 * s, 3)), str(s), num(F(5 * s, 4)), num(F(s, 2))],
                    ex=f'For a normal distribution, mean deviation ≈ (4/5)σ = 0.8 × {s} = {num(v)}. (Quartile deviation ≈ (2/3)σ.) These approximate relations hold only for the normal curve, which is symmetric with mean = median = mode.',
                    fast='MD ≈ 0.8σ for a normal distribution.', secs=15, d='core', topic=C5, check=frx(v), k='ch16.md', data={'s': s, 'kind': 'mean deviation'})
    md = F(4 * s, 5); v = F(s)
    return dict(q=f'For a normal distribution the mean deviation about the mean is {num(md)}. The standard deviation is approximately:', a=num(v), w=[num(md * F(4, 5)), num(md), num(md * F(3, 2)), num(md * 2)],
                ex=f'For a normal distribution, MD ≈ (4/5)σ, so σ ≈ (5/4) × MD = 1.25 × {num(md)} = {num(v)}. Multiplying by 4/5 again goes the wrong way. The SD is always larger than the mean deviation for a normal curve.',
                fast='For a normal curve σ ≈ 1.25 × mean deviation.', secs=20, d='moderate', topic=C5, check=frx(v), k='ch16.md', data={'md': float(md), 'kind': 'standard deviation'})


BANKS = {U: [(binom_pt, 3), (binom_atleast, 2), (binom_mv, 3), (binom_np, 2), (pois_pt, 3), (pois_equal, 2), (pois_approx, 2), (zscore, 2), (normal_prob, 4), (normal_count, 2), (md_normal, 2)]}
