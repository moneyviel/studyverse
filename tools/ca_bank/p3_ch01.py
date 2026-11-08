"""Paper 3 Ch 1 — Ratio and Proportion, Indices, Logarithms: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch01-u01'
T_RATIO, T_TYPES, T_PROP, T_PROPS = 'Ratio — meaning and basic rules', 'Types of ratios', 'Proportion and proportionals', 'Properties of proportion'
T_IND, T_LOG, T_LAWS, T_CHAR = 'Indices (powers) and their laws', 'Logarithm — definition', 'Laws of logarithms and change of base', 'Characteristic, mantissa and antilogarithm'


def rr(*xs):
    g = 0
    for x in xs: g = math.gcd(g, x)
    return ' : '.join(str(x // g) for x in xs)


def chain(r):
    a, b, c, d = (r.randint(2, 9) for _ in range(4))
    if math.gcd(a, b) > 1 or math.gcd(c, d) > 1 or b == c: return None
    ans = rr(a * c, b * c, b * d)
    return dict(q=f'If A : B = {a} : {b} and B : C = {c} : {d}, then A : B : C is:', a=ans,
                w=[rr(a, b, d), rr(a * d, b * c, b * d), rr(a * c, b * d, c * d), rr(a, b * c, d), rr(c, b, a)],
                ex=f'Make the common term B equal in both ratios. B is {b} in the first and {c} in the second, so multiply the first ratio by {c} and the second by {b}: A : B = {a*c} : {b*c} and B : C = {b*c} : {b*d}. Hence A : B : C = {ans}. Simply writing {a} : {b} : {d} ignores that the two B values differ.',
                fast=f'Cross pattern: A = {a}×{c}, B = {b}×{c}, C = {b}×{d}; then cancel the common factor.',
                secs=30, d='core', topic=T_RATIO, k='ch01.chain', data={'ab': [a, b], 'bc': [c, d]})


def share(r):
    p, q, s = sorted(r.sample(range(2, 12), 3))
    if math.gcd(math.gcd(p, q), s) > 1: return None
    k = r.choice([45, 60, 75, 120, 150, 250, 400, 35, 85])
    N = (p + q + s) * k; who = r.choice(['B', 'C'])
    x = {'B': q, 'C': s}[who]; ans = N * x // (p + q + s)
    other = {'B': s, 'C': q}[who]
    return dict(q=f'₹{inr(N)} is divided among A, B and C in the ratio {p} : {q} : {s}. What is {who}\'s share?', a=rs(ans),
                w=[rs(N * other // (p + q + s)), rs(N // 3), rs(N * x // (p + q)), rs(N * p // (p + q + s)), rs(ans + k)],
                ex=f'Total parts = {p} + {q} + {s} = {p+q+s}. One part = {inr(N)} ÷ {p+q+s} = ₹{inr(k)}. {who} gets {x} parts = {x} × {inr(k)} = ₹{inr(ans)}. A common slip is dividing the total equally by 3 or forgetting one of the three terms in the total parts.',
                fast=f'One part = ₹{inr(k)}; multiply by {who}\'s {x} parts. Check: the three shares must add back to ₹{inr(N)}.',
                secs=30, d='core', topic=T_RATIO, check=f'{N}*{x}/{p+q+s}', k='ch01.share', data={'N': N, 'ratio': [p, q, s], 'who': who})


def equal_multiples(r):
    p, q, s = r.sample(range(2, 10), 3)
    if len({p, q, s}) < 3: return None
    ans = rr(q * s, p * s, p * q)
    if ans == rr(p, q, s) or ans == rr(s, q, p): return None
    return dict(q=f'If {p}x = {q}y = {s}z, then x : y : z is:', a=ans, w=[rr(p, q, s), rr(s, q, p), rr(p * q, q * s, p * s), rr(q, s, p)],
                ex=f'Let {p}x = {q}y = {s}z = k. Then x = k/{p}, y = k/{q}, z = k/{s}, so x : y : z = 1/{p} : 1/{q} : 1/{s}. Multiply by the LCM of {p}, {q} and {s} to clear the fractions: x : y : z = {ans}. The trap is {rr(p, q, s)}, which copies the multipliers instead of their reciprocals.',
                fast=f'Reciprocals: x : y : z = {q}×{s} : {p}×{s} : {p}×{q}, then reduce. A bigger multiplier means a smaller variable.',
                secs=35, d='core', topic=T_RATIO, k='ch01.eqmult', data={'m': [p, q, s]})


def fourth_prop(r):
    a = r.randint(3, 15); b = r.randint(4, 40); c = r.randint(4, 40)
    if (b * c) % a or b == c or a in (b, c): return None
    ans = b * c // a
    return dict(q=f'The fourth proportional to {a}, {b} and {c} is:', a=num(ans),
                w=[num(F(a * c, b)), num(F(a * b, c)), num(a * b * c), num(b + c - a), num(F(b * b, a))],
                ex=f'If d is the fourth proportional, then {a} : {b} = {c} : d, so {a} × d = {b} × {c}. Hence d = {b} × {c} ÷ {a} = {inr(ans)}. Remember the order matters: the first term multiplies the unknown fourth term, and the two middle terms (means) are multiplied together.',
                fast=f'Fourth proportional = (2nd × 3rd) ÷ 1st = {b}×{c}/{a}.', secs=25, d='core', topic=T_PROP,
                check=f'{b}*{c}/{a}', k='ch01.fourth', data={'a': a, 'b': b, 'c': c})


def mean_prop(r):
    m = r.randint(2, 9); a = m * r.randint(1, 6) ** 2; b = m * r.randint(1, 9) ** 2
    if a == b or a < 4: return None
    ans = math.isqrt(a * b)
    return dict(q=f'The mean proportional between {a} and {b} is:', a=num(ans),
                w=[num(F(a + b, 2)), num(a * b), num(F(b * b, a)), num(F(a * a, b)), num(ans + m)],
                ex=f'If x is the mean proportional, then {a} : x = x : {b}, so x² = {a} × {b} = {inr(a*b)} and x = √{inr(a*b)} = {ans}. The arithmetic average ({num(F(a+b,2))}) is a different idea; the mean proportional is the geometric mean of the two numbers.',
                fast=f'√({a}×{b}): split into square factors — √{a*b} = {ans}. Or test options: x² must equal {a*b}.', secs=30, d='core', topic=T_PROP,
                check=f'({a}*{b})**0.5', k='ch01.meanp', data={'a': a, 'b': b})


def third_prop(r):
    a = r.randint(2, 20); b = r.randint(a + 1, 60)
    if (b * b) % a: return None
    ans = b * b // a
    return dict(q=f'The third proportional to {a} and {b} is:', a=num(ans),
                w=[num(math.sqrt(a * b)) if math.isqrt(a * b) ** 2 == a * b else num(a * b), num(F(a * a, b)), num(2 * b - a), num(a * b), num(b * b)],
                ex=f'If c is the third proportional, then {a} : {b} = {b} : c, so {a} × c = {b}². Hence c = {b*b} ÷ {a} = {inr(ans)}. Do not confuse it with the mean proportional √({a} × {b}); the third proportional continues the proportion beyond the second number.',
                fast=f'Third proportional = (2nd)² ÷ 1st = {b}²/{a}.', secs=25, d='core', topic=T_PROP, check=f'{b}**2/{a}', k='ch01.third', data={'a': a, 'b': b})


def mixture(r):
    a, b = r.randint(3, 9), r.randint(1, 5)
    if math.gcd(a, b) > 1: return None
    c, d = r.randint(1, 9), r.randint(1, 9)
    if math.gcd(c, d) > 1 or F(c, d) >= F(a, b): return None
    V = (a + b) * r.randint(2, 12)
    milk, water = F(V * a, a + b), F(V * b, a + b)
    add = milk * d / c - water
    if add.denominator != 1 or add <= 0 or add > 200: return None
    return dict(q=f'A mixture of {V} litres contains milk and water in the ratio {a} : {b}. How much water must be added to make the ratio {c} : {d}?',
                a=f'{fr(add)} litres', w=[f'{fr(F(V*d, c+d) - water)} litres' if F(V*d, c+d) > water else f'{fr(add + 2)} litres', f'{fr(milk*d/c)} litres', f'{fr(add*2)} litres', f'{fr(abs(add - (d - b)))} litres', f'{fr(add + c)} litres'],
                ex=f'Milk = {V} × {a}/{a+b} = {fr(milk)} litres and water = {fr(water)} litres. Adding water does not change the milk, so the new water must be {fr(milk)} × {d}/{c} = {fr(milk*d/c)} litres. Water to add = {fr(milk*d/c)} − {fr(water)} = {fr(add)} litres. The trap is to keep the total fixed; only the milk stays fixed.',
                fast=f'Keep milk constant ({fr(milk)} L). New water = milk × {d}/{c}; subtract the old water. Back-substitute an option to confirm the ratio {c} : {d}.',
                secs=60, d='moderate', topic=T_RATIO, check=frx(add), k='ch01.mix', data={'V': V, 'r1': [a, b], 'r2': [c, d]})


def add_each(r):
    a, b = r.randint(2, 9), r.randint(2, 11)
    if a >= b or math.gcd(a, b) > 1: return None
    x = r.randint(2, 15); k = r.randint(2, 20)
    c, d = a * x + k, b * x + k; g = math.gcd(c, d); c //= g; d //= g
    if d > 30 or (c, d) == (a, b): return None
    return dict(q=f'Two numbers are in the ratio {a} : {b}. If {k} is added to each, the ratio becomes {c} : {d}. The smaller number is:', a=num(a * x),
                w=[num(b * x), num(x), num(a * x + k), num(a * (x + 1)), num(c * (k // max(1, abs(d - c)) or 1))],
                ex=f'Let the numbers be {a}x and {b}x. Then ({a}x + {k}) : ({b}x + {k}) = {c} : {d}, so {d}({a}x + {k}) = {c}({b}x + {k}). This gives {d*a - c*b}x = {c*k - d*k}, so x = {x}. The smaller number is {a} × {x} = {a*x} (the larger is {b*x}).',
                fast=f'Test the options: the smaller must be a multiple of {a}; add {k} to it and to its partner and check the ratio {c} : {d}.',
                secs=50, d='moderate', topic=T_RATIO, check=f'{a}*{x}', k='ch01.addeach', data={'r1': [a, b], 'k': k, 'r2': [c, d]})


def dup_ratio(r):
    kind = r.choice(['duplicate', 'triplicate', 'sub-duplicate', 'sub-triplicate'])
    a, b = r.randint(2, 9), r.randint(2, 9)
    if a == b or math.gcd(a, b) > 1: return None
    pw = {'duplicate': 2, 'triplicate': 3, 'sub-duplicate': 2, 'sub-triplicate': 3}[kind]
    if kind.startswith('sub'):
        given = f'{a**pw} : {b**pw}'; ans = f'{a} : {b}'
        w = [f'{a**pw//1*1} : {b**pw}' if False else f'{a*pw} : {b*pw}', f'{a**(pw+1)} : {b**(pw+1)}', f'{b} : {a}', f'{a**pw*a**pw} : {b**pw*b**pw}']
        how = f'{"square" if pw == 2 else "cube"} root of each term'
    else:
        given = f'{a} : {b}'; ans = f'{a**pw} : {b**pw}'
        w = [f'{a*pw} : {b*pw}', f'{b**pw} : {a**pw}', f'{a**(5-pw)} : {b**(5-pw)}', f'{a+pw} : {b+pw}']
        how = f'{"square" if pw == 2 else "cube"} of each term'
    return dict(q=f'The {kind} ratio of {given} is:', a=ans, w=w,
                ex=f'The {kind} ratio is found by taking the {how}. So the {kind} ratio of {given} is {ans}. Students often multiply the terms by {pw} instead of raising them to the power, which keeps the same ratio and is wrong.',
                fast=f'Duplicate = square, triplicate = cube, sub-duplicate = square root, sub-triplicate = cube root — apply to each term.', secs=20, d='core', topic=T_TYPES,
                k='ch01.dup', data={'kind': kind, 'a': a, 'b': b})


def idx_eq(r):
    b = r.choice([2, 3, 5]); m, n = r.sample([1, 2, 3], 2); a = r.randint(-4, 9); c = r.randint(-3, 4)
    if (a - n * c) % (n - m) or c == 0: return None
    x = (a - n * c) // (n - m)
    if x == 0: return None
    L = f'{b**m}^x' if m > 1 else f'{b}^x'
    ans = num(x)
    return dict(q=f'If {L} × {b}^{a if a >= 0 else "(" + str(a) + ")"} = {b**n}^(x {"+" if c > 0 else "−"} {abs(c)}), then x =', a=ans,
                w=[num(-x), num(x + 1), num(F(a - c, n - m)) if F(a - c, n - m) != x else num(x + 2), num(x - 2)],
                ex=f'Write every term as a power of {b}: {b}^({m}x) × {b}^({a}) = {b}^({n}(x {"+" if c > 0 else "−"} {abs(c)})). Equal bases mean equal powers: {m}x + {a} = {n}x {"+" if n*c >= 0 else "−"} {abs(n*c)}. So {n-m}x = {a - n*c} and x = {x}.',
                fast=f'Substitute an option: with x = {x} both sides become {b}^{m*x + a}.', secs=45, d='moderate', topic=T_IND,
                check=str(x), k='ch01.idxeq', data={'b': b, 'm': m, 'n': n, 'a': a, 'c': c})


def frac_power(r):
    t = r.choice([2, 3, 4, 5]); s = r.choice([2, 3, 4, 5]); rr_ = r.choice([1, 2, 3, 4]); neg = r.random() < .6
    base = t ** s
    if base > 3000 or math.gcd(rr_, s) > 1 or rr_ == s: return None
    e = F(-rr_ if neg else rr_, s); val = F(t) ** (-rr_ if neg else rr_)
    return dict(q=f'The value of ({base})^({fr(e)}) is:', a=fr(val), w=[fr(1 / val), fr(-val), fr(F(base) * e) if F(base) * e != val else fr(val * t), fr(val * t), fr(val / t)],
                ex=f'{base} = {t}^{s}, so ({base})^({fr(e)}) = {t}^({s} × {fr(e)}) = {t}^({-rr_ if neg else rr_}) = {fr(val)}. The denominator {s} of the power means the {ordn(s)} root and the numerator is the power. {"A negative power gives the reciprocal, not a negative number." if neg else "Take the root first to keep numbers small."}',
                fast=f'Root first, then power{", then flip for the minus sign" if neg else ""}: {s}th root of {base} = {t}.', secs=25, d='core', topic=T_IND,
                check=frx(val), k='ch01.fracpow', data={'base': base, 'e': [e.numerator, e.denominator]})


def log_base(r):
    a = r.choice([2, 3, 5]); p = r.choice([1, 2, 3, 4]); q = r.choice([-3, -2, 1, 2, 3, 4, 5, 6]); half = r.random() < .3
    P = F(p, 2) if half else F(p)
    if P == 1 or q == 0: return None
    v = F(q) / P
    bs = (f'√{a}' if p == 1 else f'√{a**p}' if a ** p < 200 else None) if half else str(a ** p)
    if bs is None: return None
    arg = str(a ** q) if q > 0 else f'1/{a**(-q)}'
    if v == 1 or v == F(P) / q: return None
    return dict(q=f'The value of log {arg} to the base {bs} is:', a=fr(v), w=[fr(P / q), fr(-v), fr(q * P), fr(v + 1), fr(F(q) - P)],
                ex=f'Write both numbers as powers of {a}: {bs} = {a}^({fr(P)}) and {arg} = {a}^({q}). By definition, log of {a}^({q}) to base {a}^({fr(P)}) is the power y with {a}^({fr(P)}·y) = {a}^({q}), so y = {q} ÷ {fr(P)} = {fr(v)}. The trap is inverting the fraction to {fr(P/q)}.',
                fast=f'log_(a^m) a^n = n/m. Here n = {q}, m = {fr(P)}.', secs=30, d='moderate', topic=T_LOG, check=frx(v), k='ch01.logbase', data={'a': a, 'P': [P.numerator, P.denominator], 'q': q})


L2, L3 = 0.3010, 0.4771


def log_value(r):
    i, j, k5 = r.randint(0, 4), r.randint(0, 3), r.randint(0, 2); e = r.randint(-3, 1)
    if i + j + k5 < 2: return None
    n = F(2) ** i * F(3) ** j * F(5) ** k5 * F(10) ** e
    nv = float(n)
    if nv > 1e6 or nv < 1e-4 or n.denominator not in (1, 10, 100, 1000, 10000) and n.denominator % 10: return None
    # decimal text of n
    s = f'{nv:.6f}'.rstrip('0').rstrip('.')
    if F(s) != n: return None
    val = i * L2 + j * L3 + k5 * (1 - L2) + e
    ex_ = f'{i}*0.3010+{j}*0.4771+{k5}*(1-0.3010)+({e})'
    w = [i * L2 + j * L3 + k5 * L2 + e, val + 1, val - 1, i * L3 + j * L2 + k5 * (1 - L2) + e]
    fmt = lambda x: f'{x:.4f}'
    fac = ' × '.join([f'2{sup(i)}' if i > 1 else '2'] * (i > 0) + [f'3{sup(j)}' if j > 1 else '3'] * (j > 0) + [f'5{sup(k5)}' if k5 > 1 else '5'] * (k5 > 0))
    return dict(q=f'Given log 2 = 0.3010 and log 3 = 0.4771 (base 10), the value of log {s} is:', a=fmt(val), w=[fmt(x) for x in w],
                ex=f'{s} = {fac}{f" × 10{sup(e)}" if e else ""}. Use log 5 = log(10/2) = 1 − 0.3010 = 0.6990. So log {s} = {i}(0.3010) + {j}(0.4771) + {k5}(0.6990){f" + ({e})" if e else ""} = {fmt(val)}. Laws used: log(mn) = log m + log n and log mᵏ = k log m.',
                fast=f'Factorise into 2s, 3s, 5s and powers of 10 first; log 5 = 0.6990. Each power of 10 just adds or subtracts 1.', secs=50, d='moderate', topic=T_LAWS,
                check=ex_, k='ch01.logval', data={'n': s, 'i': i, 'j': j, 'k5': k5, 'e': e})


def digits(r):
    b = r.choice([2, 3]); n = r.randint(20, 120)
    lg = {2: 0.30103, 3: 0.47712}[b]; d = math.floor(n * lg) + 1
    if d != len(str(b ** n)) or abs(n * lg - round(n * lg)) < .02: return None
    return dict(q=f'Given log 2 = 0.30103 and log 3 = 0.47712, the number of digits in {b}{sup(n)} is:', a=str(d),
                w=[str(d - 1), str(d + 1), str(math.ceil(n * lg) + 1) if math.ceil(n * lg) + 1 != d else str(d + 2), str(round(n * lg * 10) // 10 + 3)],
                ex=f'log {b}{sup(n)} = {n} × {lg} = {n*lg:.5f}. The characteristic (integer part) is {math.floor(n*lg)}, and a number whose characteristic is c has c + 1 digits before the decimal point. So {b}{sup(n)} has {d} digits. Forgetting to add 1 gives {d-1}.',
                fast=f'Digits = integer part of ({n} × {lg}) + 1.', secs=30, d='moderate', topic=T_CHAR, check=str(d), k='ch01.digits', data={'b': b, 'n': n})


def log_eq(r):
    x = r.randint(3, 20); a = r.randint(1, x - 1); bb = x * (x - a)
    if bb < 6: return None
    return dict(q=f'If log x + log (x − {a}) = log {bb}, then x =', a=num(x), w=[num(a - x) if a - x != 0 else num(x + 1), num(x - a), num(F(bb, a)) if bb % a == 0 and bb // a != x else num(x + 2), num(x + a)],
                ex=f'log x + log(x − {a}) = log[x(x − {a})], so x² − {a}x = {bb}, i.e. x² − {a}x − {bb} = 0, which factorises as (x − {x})(x + {x - a}) = 0. The root −{x - a} is rejected because the log of a negative number is not defined. Hence x = {x}.',
                fast=f'Back-substitute: {x} × {x - a} = {bb}. Discard any option that makes x or x − {a} negative.', secs=40, d='moderate', topic=T_LAWS,
                check=str(x), k='ch01.logeq', data={'a': a, 'b': bb})


def characteristic(r):
    z = r.randint(0, 5); digs = r.randint(1, 4)
    big = r.random() < .4
    if big: n = r.randint(1, 9) * 10 ** (z + 1) + r.randint(0, 9) * 10 ** z; c = len(str(n)) - 1; s = inr(n)
    else:
        m = r.randint(10 ** (digs - 1), 10 ** digs - 1)
        if m % 10 == 0: return None
        s = '0.' + '0' * z + str(m); c = -(z + 1)
    w = [str(c + 1), str(c - 1), str(-c)] if c else ['1', '-1', '2']
    return dict(q=f'The characteristic of log {s} (base 10) is:', a=str(c), w=w,
                ex=(f'For a number of 1 or more, the characteristic is one less than the number of digits before the decimal point. {s} has {c+1} digits, so the characteristic is {c}.' if big else
                    f'For a number below 1, the characteristic is negative: one more than the number of zeros right after the decimal point, with a minus sign. {s} has {z} zero(s) after the point, so the characteristic is {c} (written as bar {-c}).') + ' The mantissa (decimal part) is always positive and comes from the log table.',
                fast='Count digits (number ≥ 1: digits − 1) or zeros after the point (number < 1: −(zeros + 1)).', secs=20, d='core', topic=T_CHAR,
                check=str(c), k='ch01.char', data={'n': s})


BANKS = {U: [(chain, 2), (share, 2), (equal_multiples, 2), (fourth_prop, 2), (mean_prop, 2), (third_prop, 2), (mixture, 2), (add_each, 2),
             (dup_ratio, 2), (idx_eq, 2), (frac_power, 2), (log_base, 2), (log_value, 2), (digits, 2), (log_eq, 1), (characteristic, 2)]}
