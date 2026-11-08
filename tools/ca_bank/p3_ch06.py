"""Paper 3 Ch 6 — Sequence and Series (AP, GP): extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch06-u01'
C1, C2, C3, C4 = 'Sequence and series', 'Arithmetic progression (AP), its general term and arithmetic means', 'Sum of the first n terms of an AP', 'Special series'
C5, C6, C7, C8 = 'Geometric progression (GP), its general term and geometric means', 'Sum of a GP — finite and infinite; recurring decimals', 'Series that reduce to a GP', 'Applications in commerce and finance'


def seq(xs): return ', '.join(fr(x) for x in xs)


def ap_term(r):
    a = r.randint(-20, 40); d = r.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 9, 11]); n = r.randint(12, 60)
    t = a + (n - 1) * d
    return dict(q=f'The {ordn(n)} term of the AP {seq([a, a + d, a + 2 * d])}, … is:', a=num(t), w=[num(a + n * d), num(a + (n - 2) * d), num(n * d), num(a * n + d) if a * n + d != t else num(t + 1)],
                ex=f'tₙ = a + (n − 1)d with a = {a} and d = {a + d} − ({a}) = {d}. So t{n} = {a} + ({n} − 1)({d}) = {a} + {(n - 1) * d} = {t}. Using n instead of n − 1 adds one extra step of {d} and gives {a + n * d}.',
                fast=f'Jump {n - 1} steps of {d} from {a}.', secs=25, d='core', topic=C2, check=str(t), k='ch06.apterm', data={'first3': [a, a + d, a + 2 * d], 'n': n})


def which_term(r):
    a = r.randint(-10, 30); d = r.choice([2, 3, 4, 5, 6, 7, -3, -4]); n = r.randint(10, 70); X = a + (n - 1) * d
    return dict(q=f'Which term of the AP {seq([a, a + d, a + 2 * d])}, … is {X}?', a=f'{ordn(n)} term', w=[f'{ordn(n - 1)} term', f'{ordn(n + 1)} term', f'{ordn(abs(X) // abs(d) or 2)} term' if abs(X) // abs(d) not in (n, n - 1, n + 1, 0) else f'{ordn(n + 2)} term', f'{ordn(n - 2)} term'],
                ex=f'Set a + (n − 1)d = {X}: {a} + (n − 1)({d}) = {X}, so n − 1 = ({X} − {a})/{d} = {n - 1} and n = {n}. Dividing {X} by {d} directly forgets that the AP starts at {a}, not at 0.',
                fast=f'n = (last − first)/d + 1 = ({X} − {a})/{d} + 1.', secs=25, d='core', topic=C2, check=str(n), k='ch06.which', data={'first3': [a, a + d, a + 2 * d], 'X': X})


def ap_sum(r):
    a = F(r.randint(-10, 30), r.choice([1, 1, 1, 2])); d = F(r.choice([-3, -2, 1, 2, 3, 4, 5, 6]), r.choice([1, 1, 2])); n = r.randint(10, 40)
    S = F(n, 2) * (2 * a + (n - 1) * d)
    return dict(q=f'The sum of the first {n} terms of the AP {seq([a, a + d, a + 2 * d])}, … is:', a=num(S), w=[num(F(n, 2) * (2 * a + n * d)), num(n * (a + (n - 1) * d)), num(F(n, 2) * (a + (n - 1) * d)), num(S + n)],
                ex=f'Sₙ = n/2 × [2a + (n − 1)d] with a = {fr(a)}, d = {fr(d)}, n = {n}: S = {n}/2 × [{fr(2 * a)} + {n - 1} × {fr(d)}] = {fr(F(n, 2))} × {fr(2 * a + (n - 1) * d)} = {num(S)}. Equivalent shortcut: n × (first + last)/2 with last term {fr(a + (n - 1) * d)}.',
                fast=f'Average of first and last ({fr(a)} and {fr(a + (n - 1) * d)}) × {n}.', secs=40, d='core', topic=C3, check=frx(S), k='ch06.apsum', data={'first3': [str(a), str(a + d), str(a + 2 * d)], 'n': n})


def two_terms(r):
    a = r.randint(-15, 25); d = r.choice([-4, -3, -2, 2, 3, 4, 5, 6, 7]); p, q_, s = r.sample(range(3, 40), 3)
    tp, tq, ts = a + (p - 1) * d, a + (q_ - 1) * d, a + (s - 1) * d
    return dict(q=f'In an AP the {ordn(p)} term is {tp} and the {ordn(q_)} term is {tq}. The {ordn(s)} term is:', a=num(ts), w=[num(ts + d), num(ts - d), num(a + s * d + d), num(tp + tq - ts) if tp + tq - ts != ts else num(ts + 2 * d)],
                ex=f'Subtract: t{q_} − t{p} = ({q_} − {p})d, so {tq - tp} = {q_ - p}d and d = {d}. Then a = t{p} − ({p} − 1)d = {tp} − {(p - 1) * d} = {a}. Hence t{s} = a + ({s} − 1)d = {a} + {(s - 1) * d} = {ts}.',
                fast=f'd = {tq - tp}/{q_ - p} = {d}; t{s} = t{p} + ({s} − {p})d.', secs=40, d='moderate', topic=C2, check=str(ts), k='ch06.two', data={'p': p, 'tp': tp, 'q': q_, 'tq': tq, 's': s})


def multiples_sum(r):
    k = r.choice([3, 4, 6, 7, 9, 11, 13]); A = r.randint(10, 150); B = A + r.randint(100, 600)
    xs = [x for x in range(A, B + 1) if x % k == 0]; S = sum(xs)
    return dict(q=f'The sum of all numbers between {A} and {B} (inclusive) that are divisible by {k} is:', a=inr(S),
                w=[inr(S + xs[-1] + k), inr(S - xs[0]), inr(len(xs) * (A + B) // 2), inr(S - xs[-1])],
                ex=f'The multiples of {k} form an AP: first {xs[0]}, last {xs[-1]}, d = {k}. Number of terms = ({xs[-1]} − {xs[0]})/{k} + 1 = {len(xs)}. Sum = n/2 × (first + last) = {len(xs)}/2 × ({xs[0]} + {xs[-1]}) = {inr(S)}. Using {A} and {B} as first and last terms is wrong unless they are multiples of {k}.',
                fast=f'Find first and last multiples, count = (last − first)/{k} + 1, sum = count × average.', secs=60, d='moderate', topic=C3, check=str(S), k='ch06.mult', data={'A': A, 'B': B, 'k': k})


def ams(r):
    a = r.randint(-10, 40); m = r.randint(3, 9); d = r.choice([-5, -3, -2, 2, 3, 4, 5, 6]); b = a + (m + 1) * d; j = r.randint(2, m)
    t = a + j * d
    return dict(q=f'{m} arithmetic means are inserted between {a} and {b}. The {ordn(j)} mean is:', a=num(t), w=[num(a + (j - 1) * d), num(a + (j + 1) * d), num(F(a + b, 2)) if F(a + b, 2) != t else num(t + 2 * d), num(a + j * F(b - a, m))],
                ex=f'With {m} means inserted, there are {m + 2} terms in all, so {b} is the {ordn(m + 2)} term: {b} = {a} + ({m + 1})d, giving d = {d}. The {ordn(j)} mean is the {ordn(j + 1)} term: {a} + {j} × ({d}) = {t}. Dividing by {m} instead of {m + 1} is the usual slip.',
                fast=f'd = (b − a)/(m + 1) = {b - a}/{m + 1} = {d}; jth mean = a + j·d.', secs=40, d='moderate', topic=C2, check=str(t), k='ch06.ams', data={'m': m, 'a': a, 'b': b, 'j': j})


def gp_term(r):
    a = F(r.choice([1, 2, 3, 4, 5, 6, 8, 81, 64, 243, 128])); rr_ = F(r.choice([2, 3, -2, -3, 1, 1, -1]), r.choice([1, 1, 2, 3])); n = r.randint(5, 9)
    if abs(rr_) == 1 or rr_ == 0: return None
    t = a * rr_ ** (n - 1)
    if abs(t.numerator) > 10 ** 6 or t.denominator > 10 ** 5: return None
    return dict(q=f'The {ordn(n)} term of the GP {seq([a, a * rr_, a * rr_ ** 2])}, … is:', a=fr(t), w=[fr(a * rr_ ** n), fr(a * rr_ ** (n - 2)), fr(-t), fr(a * rr_ * (n - 1))],
                ex=f'tₙ = a·rⁿ⁻¹ with a = {fr(a)} and r = {fr(a * rr_)} ÷ {fr(a)} = {fr(rr_)}. So t{n} = {fr(a)} × ({fr(rr_)})^{n - 1} = {fr(t)}. ' + ('With a negative ratio the sign alternates: odd-numbered terms share the sign of a.' if rr_ < 0 else 'Using rⁿ instead of rⁿ⁻¹ gives one extra multiplication.'),
                fast=f'Multiply {fr(a)} by {fr(rr_)} repeatedly ({n - 1} times) or use the power key.', secs=30, d='core', topic=C5, check=frx(t), k='ch06.gpterm', data={'first3': [str(a), str(a * rr_), str(a * rr_ ** 2)], 'n': n})


def gp_find(r):
    a = r.choice([1, 2, 3, 4, 5, 6, 7]); rr_ = r.choice([2, 3, -2, -3, 4]); p, q_ = sorted(r.sample(range(2, 8), 2))
    tp, tq = a * rr_ ** (p - 1), a * rr_ ** (q_ - 1)
    if abs(tq) > 10 ** 6: return None
    if (q_ - p) % 2 == 0: return None     # an even gap leaves the sign of r ambiguous (r and −r both fit)
    ask = r.choice(['a', 'r'])
    val = a if ask == 'a' else rr_
    w = ([a * rr_, a * abs(rr_) + 1, tp // rr_ if tp % rr_ == 0 and tp // rr_ != a else a + 2, -a] if ask == 'a' else [-rr_, rr_ * 2, q_ - p, rr_ + 1])
    return dict(q=f'In a GP the {ordn(p)} term is {tp} and the {ordn(q_)} term is {tq}. The {"first term" if ask == "a" else "common ratio"} is:', a=str(val), w=[str(x) for x in w],
                ex=f'Divide: t{q_}/t{p} = r^({q_} − {p}) = {tq}/{tp} = {fr(F(tq, tp))}, so r = {rr_}. Then a = t{p}/r^{p - 1} = {tp}/{rr_ ** (p - 1)} = {a}. Dividing the terms (not subtracting, as in an AP) is the key step.',
                fast=f'Ratio of terms → r^{q_ - p}; take the {ordn(q_ - p)} root.', secs=40, d='moderate', topic=C5, check=str(val), k='ch06.gpfind', data={'p': p, 'tp': tp, 'q': q_, 'tq': tq, 'ask': 'first term' if ask == 'a' else 'common ratio'})


def gp_sum(r):
    a = r.choice([1, 2, 3, 4, 5, 6, 10]); rr_ = r.choice([2, 3, -2, 4, 5]); n = r.randint(4, 9)
    S = a * (rr_ ** n - 1) // (rr_ - 1)
    if abs(S) > 10 ** 7: return None
    return dict(q=f'The sum of the first {n} terms of the GP {a}, {a * rr_}, {a * rr_ ** 2}, … is:', a=inr(S), w=[inr(a * (rr_ ** (n + 1) - 1) // (rr_ - 1)), inr(a * rr_ ** (n - 1)), inr(a * (rr_ ** n - 1)), inr(a * (rr_ ** (n - 1) - 1) // (rr_ - 1))],
                ex=f'Sₙ = a(rⁿ − 1)/(r − 1) with a = {a}, r = {rr_}, n = {n}: S = {a}({rr_}^{n} − 1)/({rr_} − 1) = {a} × {rr_ ** n - 1}/{rr_ - 1} = {inr(S)}. The {ordn(n)} term alone is {inr(a * rr_ ** (n - 1))}; do not confuse the last term with the sum.',
                fast=f'For r = 2 the sum is next term − first term; generally a(rⁿ − 1)/(r − 1).', secs=35, d='core', topic=C6, check=str(S), k='ch06.gpsum', data={'first3': [a, a * rr_, a * rr_ ** 2], 'n': n})


def inf_gp(r):
    a = F(r.randint(2, 40)); rr_ = F(r.choice([1, 1, 2, -1, 3, -2]), r.choice([2, 3, 4, 5]))
    if abs(rr_) >= 1: return None
    S = a / (1 - rr_)
    if r.random() < .5:
        return dict(q=f'The sum to infinity of the GP {seq([a, a * rr_, a * rr_ ** 2])}, … is:', a=fr(S), w=[fr(a / (1 + rr_)), fr(a * (1 - rr_)), fr(a / rr_) if rr_ != 0 else fr(S + 1), fr(S + a)],
                    ex=f'For |r| < 1, S∞ = a/(1 − r). Here a = {fr(a)} and r = {fr(rr_)}, so S∞ = {fr(a)}/(1 − ({fr(rr_)})) = {fr(a)}/{fr(1 - rr_)} = {fr(S)}. The terms shrink towards zero, so the total settles at this value. Using 1 + r in the denominator is a sign slip.',
                    fast=f'a ÷ (1 − r) = {fr(a)} ÷ {fr(1 - rr_)}.', secs=25, d='core', topic=C6, check=frx(S), k='ch06.inf', data={'first3': [str(a), str(a * rr_), str(a * rr_ ** 2)]})
    return dict(q=f'The sum to infinity of a GP is {fr(S)} and its first term is {fr(a)}. The common ratio is:', a=fr(rr_), w=[fr(-rr_), fr(1 - rr_), fr(a / S), fr(rr_ + F(1, 10))],
                ex=f'S∞ = a/(1 − r), so 1 − r = a/S∞ = {fr(a)}/{fr(S)} = {fr(1 - rr_)} and r = 1 − {fr(1 - rr_)} = {fr(rr_)}. The value a/S∞ = {fr(a / S)} is 1 − r, not r itself.',
                fast=f'r = 1 − a/S∞ = 1 − {fr(a)}/{fr(S)}.', secs=30, d='moderate', topic=C6, check=frx(rr_), k='ch06.infr', data={'S': fr(S), 'a': fr(a)})


def recurring(r):
    nr = r.choice(['', '', str(r.randint(1, 9))]); rep = str(r.randint(1, 98)).zfill(2) if r.random() < .7 else str(r.randint(1, 9))
    if len(set(rep)) == 1 and len(rep) == 2: return None
    k, m = len(nr), len(rep)
    v = (F(int(nr + rep) - (int(nr) if nr else 0)) / (10 ** k * (10 ** m - 1)))
    shown = '0.' + nr + rep * (3 if m == 2 else 5) + '…'
    return dict(q=f'The recurring decimal {shown} ({rep} repeating) as a fraction in lowest terms is:', a=fr(v),
                w=[fr(F(int(nr + rep), 10 ** (k + m))), fr(F(int(rep), 10 ** m - 1)) if nr else fr(F(int(rep), 10 ** m - 1) * F(10, 11) if m == 2 else F(int(rep), 10)), fr(F(int(nr + rep), 10 ** k * (10 ** m - 1))), fr(v + F(1, 10 ** (k + m)))],
                ex=f'A recurring decimal is a GP: e.g. 0.{rep}{rep}… = {rep}/{10 ** m} + {rep}/{10 ** (2 * m)} + … = {rep}/{10 ** m - 1}. ' + (f'With the non-repeating digit {nr}, use (all digits − non-repeating digits)/({"9" * m} followed by {"0" * k}) = ({int(nr + rep)} − {int(nr)})/{10 ** k * (10 ** m - 1)}.' if nr else '') + f' In lowest terms: {fr(v)}.',
                fast=f'Numerator: (digits up to one cycle) − (non-repeating part); denominator: one 9 per repeating digit, one 0 per non-repeating digit.', secs=40, d='moderate', topic=C6,
                check=frx(v), k='ch06.recur', data={'nr': nr, 'rep': rep})


def special(r):
    n = r.randint(8, 30); kind = r.choice(['sq', 'cube', 'odd', 'nat'])
    v = {'sq': n * (n + 1) * (2 * n + 1) // 6, 'cube': (n * (n + 1) // 2) ** 2, 'odd': n * n, 'nat': n * (n + 1) // 2}[kind]
    txt = {'sq': f'1² + 2² + 3² + … + {n}²', 'cube': f'1³ + 2³ + 3³ + … + {n}³', 'odd': f'1 + 3 + 5 + … + {2 * n - 1}', 'nat': f'1 + 2 + 3 + … + {n}'}[kind]
    form = {'sq': 'n(n + 1)(2n + 1)/6', 'cube': '[n(n + 1)/2]²', 'odd': 'n² (n odd numbers)', 'nat': 'n(n + 1)/2'}[kind]
    w = {'sq': [n * (n + 1) // 2, (n * (n + 1) // 2) ** 2, n * (n + 1) * (2 * n + 1) // 3], 'cube': [n * (n + 1) * (2 * n + 1) // 6, (n * (n + 1)) ** 2, n * (n + 1) // 2 * n],
         'odd': [(2 * n - 1) ** 2, n * (n + 1), (2 * n - 1) * n // 2 + 1], 'nat': [n * n, n * (n - 1) // 2, n * (n + 1)]}[kind]
    return dict(q=f'The value of {txt} is:', a=inr(v), w=[inr(x) for x in w] + [inr(v + n)],
                ex=f'Use the standard result {form} with n = {n}' + (f' (there are {n} odd numbers up to {2 * n - 1})' if kind == 'odd' else '') + f'. This gives {inr(v)}. Remember the link: the sum of the first n cubes is the square of the sum of the first n natural numbers.',
                fast=f'Formula {form}; for odd numbers count the terms first.', secs=30, d='core', topic=C4, check=str(v), k='ch06.special', data={'n': n, 'kind': kind})


def three_ap(r):
    m = r.randint(2, 15); d = r.randint(1, 9)
    S, P = 3 * m, (m - d) * m * (m + d)
    if P == 0: return None
    return dict(q=f'Three numbers in AP have sum {S} and product {inr(P)}. The largest of them is:', a=str(m + d), w=[str(m), str(m - d), str(m + 2 * d), str(m + d + 1)],
                ex=f'Take the numbers as a − d, a, a + d. Their sum is 3a = {S}, so a = {m}. Product: (a − d) a (a + d) = a(a² − d²) = {P}, so {m}({m * m} − d²) = {P} and d² = {d * d}, d = ±{d}. The numbers are {m - d}, {m}, {m + d}; the largest is {m + d}.',
                fast=f'Middle = sum/3 = {m}; product ÷ {m} = {m * m - d * d} = {m}² − d².', secs=45, d='moderate', topic=C2, check=str(m + d), k='ch06.three', data={'S': S, 'P': P})


def salary(r):
    A = r.choice(range(180000, 900001, 12000)); I = r.choice(range(6000, 60001, 2000)); n = r.randint(5, 20); kind = r.choice(['total', 'year'])
    if kind == 'total':
        v = n * (2 * A + (n - 1) * I) // 2
        return dict(q=f'A person joins at an annual salary of ₹{inr(A)} with a fixed increment of ₹{inr(I)} every year. The total salary received in the first {n} years is:', a=rs(v),
                    w=[rs(n * A + n * I * n // 2), rs(n * (A + (n - 1) * I)), rs(n * A), rs(n * (2 * A + n * I) // 2)],
                    ex=f'Yearly salaries form an AP: a = ₹{inr(A)}, d = ₹{inr(I)}. Total for n = {n} years: Sₙ = n/2 × [2a + (n − 1)d] = {n}/2 × [{inr(2 * A)} + {n - 1} × {inr(I)}] = ₹{inr(v)}. The first year has no increment, which is why (n − 1) appears.',
                    fast=f'{n} × average salary, where average = first + {n - 1}/2 increments.', secs=50, d='moderate', topic=C8, check=str(v), k='ch06.salary', data={'A': A, 'I': I, 'n': n, 'kind': 'total'})
    v = A + (n - 1) * I
    return dict(q=f'A person joins at an annual salary of ₹{inr(A)} with a fixed increment of ₹{inr(I)} every year. The salary in the {ordn(n)} year is:', a=rs(v),
                w=[rs(A + n * I), rs(A + (n - 2) * I), rs(A * n), rs(n * I)],
                ex=f'Salaries form an AP with a = ₹{inr(A)} and d = ₹{inr(I)}. In year n the salary is a + (n − 1)d = {inr(A)} + {n - 1} × {inr(I)} = ₹{inr(v)}. In the first year no increment has been added, so year {n} carries only {n - 1} increments.',
                fast='tₙ = a + (n − 1)d: count increments = years − 1.', secs=25, d='core', topic=C8, check=str(v), k='ch06.salary', data={'A': A, 'I': I, 'n': n, 'kind': 'year'})


def gp_app(r):
    P = r.choice(range(500, 20001, 500)); g = r.choice([2, 2, 3]); n = r.randint(4, 8 if g == 2 else 6)
    v = P * (g ** n - 1) // (g - 1)
    word = {2: 'doubles', 3: 'triples'}[g]
    return dict(q=f'A person saves ₹{inr(P)} in the first month and each month the saving {word} the previous month\'s saving. The total saved in {n} months is:', a=rs(v),
                w=[rs(P * g ** (n - 1)), rs(P * g ** n), rs(P * n * g), rs(P * (g ** (n - 1) - 1) // (g - 1))],
                ex=f'Savings form a GP: a = ₹{inr(P)}, r = {g}. Total = a(rⁿ − 1)/(r − 1) = {inr(P)}({g}^{n} − 1)/{g - 1} = ₹{inr(v)}. The saving in month {n} alone is ₹{inr(P * g ** (n - 1))}, which is not the total.',
                fast=f'Sₙ = {inr(P)} × ({g}^{n} − 1)/{g - 1}.', secs=35, d='core', topic=C8, check=str(v), k='ch06.gpapp', data={'P': P, 'g': word, 'n': n})


def reduce_gp(r):
    dgt = r.randint(1, 9); n = r.randint(3, 6)
    terms = [F(int(str(dgt) * k), 10 ** k) for k in range(1, n + 1)]; S = sum(terms)
    shown = ' + '.join(f'0.{str(dgt) * k}' for k in range(1, 4)) + ' + …'
    sv = f'{float(S):.{n}f}'
    return dict(q=f'The sum of the first {n} terms of {shown} is:', a=sv, w=[f'{float(S - terms[-1]):.{n}f}', f'{float(F(dgt, 9) * n):.{n}f}', f'{float(S + F(int(str(dgt) * (n + 1)), 10 ** (n + 1))):.{n}f}', f'{float(F(dgt * n, 10)):.{n}f}'],
                ex=f'Write each term as {dgt}/9 × (1 − 1/10ᵏ): 0.{dgt} = {dgt}/9 × 0.9, 0.{dgt * 2 if False else str(dgt) * 2} = {dgt}/9 × 0.99, and so on. Sum = {dgt}/9 × [n − (0.1 + 0.01 + … )] = ({dgt}/81)[9n − 1 + 10^(−n)] with n = {n}, which equals {sv}. Direct addition confirms it.',
                fast=f'Add the {n} decimals column-wise (only {n} terms), or use ({dgt}/81)(9n − 1 + 10⁻ⁿ).', secs=45, d='moderate', topic=C7, check=sv, k='ch06.reduce', data={'dgt': dgt, 'n': n})


BANKS = {U: [(ap_term, 2), (which_term, 2), (ap_sum, 2), (two_terms, 2), (multiples_sum, 2), (ams, 2), (gp_term, 2), (gp_find, 2), (gp_sum, 2), (inf_gp, 3),
             (recurring, 2), (special, 3), (three_ap, 2), (salary, 2), (gp_app, 1), (reduce_gp, 2)]}
