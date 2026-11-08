"""Paper 3 Ch 17 — Correlation and Regression: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch17-u01'
C1, C2, C3, C4 = 'Bivariate data and bivariate frequency distribution', 'Types of correlation and the scatter diagram', "Karl Pearson's product moment correlation coefficient", "Spearman's rank correlation and concurrent deviations"
C5, C6, C7 = 'Coefficient of determination and spurious correlation', 'Regression and the method of least squares', 'Properties of regression coefficients and lines'


def r_cov(r):
    sx, sy = r.randint(2, 20), r.randint(2, 20); rr_ = F(r.choice([-9, -8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8, 9]), 10)
    cov = rr_ * sx * sy; kind = r.choice(['r', 'cov'])
    if kind == 'r':
        return dict(q=f'If cov(x, y) = {num(cov)}, σx = {sx} and σy = {sy}, the coefficient of correlation is:', a=num(rr_), w=[num(-rr_), num(cov / (sx * sx * sy * sy), 4), num(cov / (sx + sy), 2) if abs(cov / (sx + sy)) <= 1 and cov / (sx + sy) != rr_ else num(rr_ / 2), num(rr_ * rr_)],
                    ex=f'Karl Pearson: r = cov(x, y)/(σx σy) = {num(cov)}/({sx} × {sy}) = {num(cov)}/{sx * sy} = {num(rr_)}. The sign of r is the sign of the covariance. r always lies between −1 and +1.',
                    fast='Correlation r = covariance ÷ (σx × σy).', secs=20, d='core', topic=C3, check=frx(rr_), k='ch17.rcov', data={'cov': float(cov), 'sx': sx, 'sy': sy, 'kind': 'coefficient of correlation'})
    return dict(q=f'If r = {num(rr_)}, σx = {sx} and σy = {sy}, the covariance between x and y is:', a=num(cov), w=[num(rr_ * sx * sx * sy * sy), num(rr_ / (sx * sy), 4), num(-cov), num(rr_ * (sx + sy))],
                ex=f'From r = cov/(σx σy): cov = r × σx × σy = {num(rr_)} × {sx} × {sy} = {num(cov)}. Covariance carries the units of x times the units of y, while r has no units. A negative r gives a negative covariance.',
                fast='Covariance = r × σx × σy (multiply all three).', secs=20, d='core', topic=C3, check=frx(cov), k='ch17.rcov', data={'r': float(rr_), 'sx': sx, 'sy': sy, 'kind': 'covariance'})


GOOD = [(F(4, 5), F(9, 20)), (F(2, 5), F(9, 10)), (F(1, 2), F(1, 2)), (F(8, 5), F(2, 5)), (F(9, 10), F(2, 5)), (F(6, 5), F(3, 10)), (F(1, 4), F(1)), (F(16, 25), F(1)), (F(5, 4), F(1, 5))]


def r_from_b(r):
    byx, bxy = r.choice(GOOD); sg = r.choice([1, -1]); byx, bxy = sg * byx, sg * bxy
    r2 = byx * bxy; rv = sg * F(math.isqrt(r2.numerator), math.isqrt(r2.denominator))
    if rv * rv != r2: return None
    return dict(q=f'If the regression coefficients are byx = {num(byx)} and bxy = {num(bxy)}, the correlation coefficient r is:', a=num(rv), w=[num(-rv), num(r2), num((byx + bxy) / 2), num(byx / bxy, 3) if byx != bxy else num(rv / 2)],
                ex=f'r² = byx × bxy = {num(byx)} × {num(bxy)} = {num(r2)}, so |r| = {num(abs(rv))}. r takes the common sign of the two regression coefficients, which are both {"positive" if sg > 0 else "negative"}: r = {num(rv)}. Their arithmetic mean is always at least |r|.',
                fast='r = ±√(byx × bxy), sign of the coefficients.', secs=25, d='core', topic=C7, check=frx(rv), k='ch17.rb', data={'byx': float(byx), 'bxy': float(bxy)})


def b_from_r(r):
    rr_ = F(r.choice([-9, -8, -6, -5, -4, 4, 5, 6, 8, 9]), 10); sx, sy = r.randint(2, 15), r.randint(2, 15); kind = r.choice(['byx', 'bxy'])
    v = rr_ * sy / sx if kind == 'byx' else rr_ * sx / sy
    return dict(q=f'Given r = {num(rr_)}, σx = {sx} and σy = {sy}, find {"byx (the slope of the regression of y on x)" if kind == "byx" else "bxy (the slope of the regression of x on y)"}.', a=num(v, 4), w=[num(rr_ * sx / sy if kind == 'byx' else rr_ * sy / sx, 4), num(rr_ * sx * sy, 4), num(-v, 4), num(rr_, 4) if rr_ != v else num(v * 2, 4)],
                ex=f'byx = r × σy/σx and bxy = r × σx/σy. Here {kind} = {num(rr_)} × {sy if kind == "byx" else sx}/{sx if kind == "byx" else sy} = {num(v, 4)}. The SD of the dependent variable goes on top. Swapping the SDs gives the other coefficient.',
                fast=f'{kind} = r × (σ of the dependent variable ÷ σ of the other).', secs=25, d='core', topic=C7, check=f'round({float(v)},4)', k='ch17.br', data={'r': float(rr_), 'sx': sx, 'sy': sy, 'kind': kind})


def line_txt(a, b, c):
    return f'{poly([a, 0])} {signed(b, "y")} {"+" if c >= 0 else "−"} {abs(c)} = 0'.replace('+ 0 = 0', '= 0')


def means_lines(r):
    mx, my = r.randint(-10, 30), r.randint(-10, 30)
    a1, b1, a2, b2 = (r.choice([1, 2, 3, 4, 5, -1, -2, -3]) for _ in range(4))
    if a1 * b2 == a2 * b1: return None
    c1, c2 = -(a1 * mx + b1 * my), -(a2 * mx + b2 * my)
    return dict(q=f'The two regression lines are {line_txt(a1, b1, c1)} and {line_txt(a2, b2, c2)}. The means of x and y are:', a=f'x̄ = {mx}, ȳ = {my}', w=[f'x̄ = {my}, ȳ = {mx}', f'x̄ = {-mx}, ȳ = {-my}', f'x̄ = {mx}, ȳ = {-my}' if my else f'x̄ = {mx + 1}, ȳ = {my}', f'x̄ = {mx + 1}, ȳ = {my - 1}'],
                ex=f'Both regression lines pass through the point of means (x̄, ȳ). So solve the two equations together: x = {mx}, y = {my}. Check: {a1}({mx}) + {b1}({my}) + {c1} = 0 and {a2}({mx}) + {b2}({my}) + {c2} = 0. It does not matter which line is y on x for this question.',
                fast='Solve the two lines simultaneously (or substitute each option pair).', secs=40, d='core', topic=C7, k='ch17.means', data={'l1': [a1, b1, c1], 'l2': [a2, b2, c2]})


def r_lines(r):
    byx, bxy = r.choice(GOOD); sg = r.choice([1, -1]); byx, bxy = sg * byx, sg * bxy
    r2 = byx * bxy; rv = sg * F(math.isqrt(r2.numerator), math.isqrt(r2.denominator))
    if rv * rv != r2 or byx * bxy == 1: return None
    # y = byx x + k1  ->  write as integer coefficients;  x = bxy y + k2
    k1, k2 = r.randint(-20, 20), r.randint(-20, 20)
    d1 = byx.denominator; A1, B1, C1_ = (-byx * d1), d1, (-k1 * d1)        # A1 x + B1 y + C1 = 0
    d2 = bxy.denominator; A2, B2, C2_ = d2, (-bxy * d2), (-k2 * d2)
    l1, l2 = line_txt(int(A1), int(B1), int(C1_)), line_txt(int(A2), int(B2), int(C2_))
    if r.random() < .5: l1, l2 = l2, l1
    return dict(q=f'The two regression lines are {l1} and {l2}. The coefficient of correlation is:', a=num(rv), w=[num(-rv), num(r2), num(1 / rv) if abs(1 / rv) != abs(rv) else num(rv / 2), num((byx + bxy) / 2)],
                ex=f'Try taking one line as y on x and the other as x on y; the product of the two slopes must not exceed 1. The valid choice gives byx = {num(byx)} and bxy = {num(bxy)}, so r² = {num(r2)} and r = {num(rv)} (same sign as the coefficients). The wrong assignment gives a product of {num(1 / r2)}, which is above 1 and therefore impossible.',
                fast='Multiply the candidate slopes; if the product exceeds 1, swap which line is y on x.', secs=75, d='hard', topic=C7, check=frx(rv), k='ch17.rlines', data={'_t': 0})


def spearman(r):
    n = r.randint(5, 12); d2 = r.randint(2, n * (n * n - 1) // 3 - 2); kind = r.choice(['given', 'ranks'])
    if kind == 'given':
        rho = 1 - F(6 * d2, n * (n * n - 1))
        if rho.denominator > 200: return None
        return dict(q=f'For {n} pairs of ranks, Σd² = {d2}. Spearman\'s rank correlation coefficient is about:', a=num(rho, 4), w=[num(1 - F(6 * d2, n * (n * n + 1)), 4), num(F(6 * d2, n * (n * n - 1)), 4), num(1 - F(d2, n * (n * n - 1)), 4), num(1 - F(6 * d2, n * n * (n - 1)), 4)],
                    ex=f'R = 1 − 6Σd²/[n(n² − 1)] = 1 − 6 × {d2}/[{n}({n * n} − 1)] = 1 − {6 * d2}/{n * (n * n - 1)} = {num(rho, 4)}. Using n² + 1 in the denominator, or forgetting to subtract from 1, are the usual slips. R lies between −1 and +1.',
                    fast='Spearman R = 1 − 6Σd² ÷ (n³ − n).', secs=30, d='core', topic=C4, check=f'round(1-6*{d2}/({n}*({n}**2-1)),4)', k='ch17.spear', data={'n': n, 'd2': d2, 'kind': 'given'})
    n = r.randint(5, 7); A = list(range(1, n + 1)); B = A[:]; r.shuffle(B)
    d2 = sum((a - b) ** 2 for a, b in zip(A, B)); rho = 1 - F(6 * d2, n * (n * n - 1))
    return dict(q=f'Two judges rank {n} candidates. Judge 1: {", ".join(map(str, A))}; Judge 2: {", ".join(map(str, B))} (same order of candidates). The rank correlation coefficient is:', a=num(rho, 4),
                w=[num(1 - F(6 * sum(abs(a - b) for a, b in zip(A, B)), n * (n * n - 1)), 4), num(-rho, 4) if rho else num(F(1, 2), 4), num(1 - F(6 * d2, n * (n * n + 1)), 4), num(F(6 * d2, n * (n * n - 1)), 4)],
                ex=f'Differences d = ' + ', '.join(str(a - b) for a, b in zip(A, B)) + f'; Σd² = {d2}. R = 1 − 6 × {d2}/[{n}({n * n} − 1)] = {num(rho, 4)}. Square the differences — adding plain differences always gives 0.',
                fast='Square each rank difference, add, then 1 − 6Σd²/(n³ − n).', secs=60, d='moderate', topic=C4, check=f'round({float(rho)},4)', k='ch17.spear', data={'A': A, 'B': B, 'kind': 'ranks'})


def pearson_data(r):
    n = r.randint(5, 6); xs = r.sample(range(1, 20), n); a, b = r.randint(-3, 3), r.choice([1, 2, -1, -2])
    ys = [a + b * x + r.randint(-3, 3) for x in xs]
    mx, my = F(sum(xs), n), F(sum(ys), n)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0: return None
    rv = float(sxy) / math.sqrt(float(sxx * syy))
    return dict(q=f'For the data x: {", ".join(map(str, xs))} and y: {", ".join(map(str, ys))}, Karl Pearson\'s coefficient of correlation is about:', a=numf(rv, 3),
                w=[numf(-rv, 3), numf(rv * rv, 3), numf(float(sxy) / float(sxx), 3) if abs(float(sxy) / float(sxx)) != abs(rv) else numf(rv / 2, 3), numf(min(0.999, abs(rv) + 0.1) * (1 if rv > 0 else -1), 3)],
                ex=f'x̄ = {num(mx)}, ȳ = {num(my)}. Σ(x − x̄)(y − ȳ) = {num(sxy)}, Σ(x − x̄)² = {num(sxx)}, Σ(y − ȳ)² = {num(syy)}. r = {num(sxy)}/√({num(sxx)} × {num(syy)}) ≈ {numf(rv, 3)}. The slope Σxy/Σx² ({numf(float(sxy) / float(sxx), 3)}) is the regression coefficient, not r.',
                fast='Use deviations from the means in a three-column table: dx·dy, dx², dy².', secs=120, d='hard', topic=C3, check=f'round({rv},3)', k='ch17.pear', data={'xs': xs, 'ys': ys})


def determination(r):
    rr_ = F(r.choice([-9, -8, -7, -6, -5, 5, 6, 7, 8, 9]), 10); kind = r.choice(['r2', 'unexp'])
    if kind == 'r2':
        v = rr_ * rr_ * 100
        return dict(q=f'If r = {num(rr_)}, the percentage of variation in y explained by x (coefficient of determination) is:', a=pct(v), w=[pct(abs(rr_) * 100), pct(100 - v), pct(v / 2), pct(-v)],
                    ex=f'Coefficient of determination = r² = ({num(rr_)})² = {num(rr_ * rr_)}, i.e. {num(v)}% of the variation in y is explained by x. It is never negative, even when r is negative, because it is a square. The remaining share is due to other factors.',
                    fast='Square r, then multiply by 100 for the percentage.', secs=15, d='core', topic=C5, check=frx(v), k='ch17.det', data={'r': float(rr_), 'kind': kind})
    v = (1 - rr_ * rr_) * 100
    return dict(q=f'If r = {num(rr_)}, the percentage of variation in y NOT explained by x (coefficient of non-determination) is:', a=pct(v), w=[pct(rr_ * rr_ * 100), pct((1 - abs(rr_)) * 100), pct(100 - v / 2), pct(v + 10)],
                ex=f'Explained share = r² = {num(rr_ * rr_)}; unexplained share = 1 − r² = {num(1 - rr_ * rr_)}, i.e. {num(v)}%. Using 1 − |r| ({num((1 - abs(rr_)) * 100)}%) is a common error. Explained and unexplained shares always add up to 100%.',
                fast='Coefficient of non-determination = 1 − r², as a percentage.', secs=15, d='core', topic=C5, check=frx(v), k='ch17.det', data={'r': float(rr_), 'kind': kind})


def estimate(r):
    mx, my = r.randint(10, 80), r.randint(10, 80); sx, sy = r.randint(2, 12), r.randint(2, 12); rr_ = F(r.choice([-8, -6, -5, -4, 4, 5, 6, 8]), 10); x0 = mx + r.randint(-10, 10)
    byx = rr_ * sy / sx; y0 = my + byx * (x0 - mx)
    return dict(q=f'x̄ = {mx}, ȳ = {my}, σx = {sx}, σy = {sy} and r = {num(rr_)}. Using the regression of y on x, the estimate of y when x = {x0} is:', a=num(y0),
                w=[num(my + rr_ * sx / sy * (x0 - mx)), num(my + rr_ * (x0 - mx)), num(mx + byx * (x0 - my)) if num(mx + byx * (x0 - my)) != num(y0) else num(y0 + 1), num(y0 + byx)],
                ex=f'Regression of y on x: y − ȳ = byx(x − x̄), with byx = r σy/σx = {num(rr_)} × {sy}/{sx} = {num(byx)}. So y = {my} + {num(byx)} × ({x0} − {mx}) = {num(y0)}. Using bxy here would estimate x from y instead.',
                fast='Estimate ŷ = ȳ + r(σy/σx)(x − x̄).', secs=45, d='moderate', topic=C6, check=f'round({float(y0)},2)', k='ch17.est', data={'mx': mx, 'my': my, 'sx': sx, 'sy': sy, 'r': float(rr_), 'x0': x0})


def origin_scale(r):
    rr_ = F(r.choice([-9, -7, -6, -5, -3, 3, 5, 6, 7, 9]), 10); a, b = r.randint(-20, 50), r.randint(-20, 50); h, k = r.choice([2, 3, 5, -2, -3, -5]), r.choice([2, 4, 10, -2, -4, -10])
    v = rr_ if h * k > 0 else -rr_
    def frm(var, c, s_): return f'({var} {"−" if c >= 0 else "+"} {abs(c)})/{s_ if s_ > 0 else "(−" + str(-s_) + ")"}'
    return dict(q=f'r(x, y) = {num(rr_)}. If u = {frm("x", a, h)} and v = {frm("y", b, k)}, then r(u, v) is:', a=num(v), w=[num(-v), num(rr_ * h / k, 4) if abs(rr_ * h / k) != abs(v) else num(v / 2), num(rr_ * h * k, 4), num(rr_ * F(abs(h), abs(k)), 4) if abs(rr_ * F(abs(h), abs(k))) != abs(v) else num(v * F(1, 2))],
                ex=f'r is independent of change of origin and scale in magnitude. Subtracting {a} and {b} has no effect; dividing by {h} and {k} changes only the sign, and only when the two scale factors have opposite signs. Here {h} × {k} {"> 0" if h * k > 0 else "< 0"}, so r(u, v) = {num(v)}.',
                fast='Same r; flip the sign only if the two scale factors have opposite signs.', secs=25, d='moderate', topic=C3, check=frx(v), k='ch17.os', data={'r': float(rr_), 'h': h, 'k': k})


def concurrent(r):
    n = r.randint(8, 21); m = n - 1; c = r.randint(0, m)
    val = F(2 * c - m, m)
    if val == 0: return None
    rc = (1 if val > 0 else -1) * math.sqrt(abs(float(val)))
    return dict(q=f'In a series of {n} pairs of observations, the number of concurrent deviations is {c}. The coefficient of concurrent deviation is about:', a=numf(rc, 4),
                w=[numf(-rc, 4), numf((1 if 2 * c - n > 0 else -1) * math.sqrt(abs((2 * c - n) / n)), 4) if 2 * c != n else numf(rc / 2, 4), numf(float(val), 4) if abs(float(val)) != abs(rc) else numf(rc * 0.9, 4), numf(min(0.9999, abs(rc) * 0.5) * (1 if rc > 0 else -1), 4)],
                ex=f'With n = {n} pairs there are m = n − 1 = {m} deviations. rc = ±√[±(2c − m)/m] = ±√[±(2 × {c} − {m})/{m}] = ±√[±({2 * c - m})/{m}]. The inner value is {"positive" if val > 0 else "negative"}, so both signs are {"+" if val > 0 else "−"}: rc ≈ {numf(rc, 4)}. Using n instead of m = n − 1 is a common slip.',
                fast='m = n − 1; rc = ±√(|2c − m|/m) with the sign of (2c − m).', secs=45, d='moderate', topic=C4, check=f'round({rc},4)', k='ch17.conc', data={'n': n, 'c': c})


BANKS = {U: [(r_cov, 3), (r_from_b, 3), (b_from_r, 2), (means_lines, 3), (r_lines, 3), (spearman, 4), (pearson_data, 2), (determination, 2), (estimate, 3), (origin_scale, 2), (concurrent, 2)]}
