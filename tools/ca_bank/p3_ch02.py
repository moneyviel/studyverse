"""Paper 3 Ch 2 — Equations: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch02-u01'
T_LIN, T_SIM, T_THREE = 'Linear (simple) equations in one unknown', 'Simultaneous linear equations in two unknowns', 'Three linear equations in three unknowns'
T_QUAD, T_NAT, T_RED, T_CUB = 'Quadratic equations — solving, sum and product of roots', 'Nature of roots — the discriminant', 'Equations reducible to quadratics and word problems', 'Cubic equations'
TIMES = {2: 'twice', 3: 'three times', 4: 'four times', 5: 'five times', 6: 'six times', 7: 'seven times'}


def xy(x, y): return f'x = {x}, y = {y}'


def ages(r):
    s = r.randint(6, 25); f = r.randint(s + 18, s + 40); k = r.randint(2, 10); j = r.randint(2, 15)
    if s - k <= 0: return None
    if (f - k) % (s - k) or (f + j) % (s + j): return None
    m, n = (f - k) // (s - k), (f + j) // (s + j)
    if m not in TIMES or n not in TIMES or m == n: return None
    return dict(q=f'{k} years ago a father was {TIMES[m]} as old as his son. {j} years from now he will be {TIMES[n]} as old as the son. The son\'s present age is:',
                a=f'{s} years', w=[f'{f} years', f'{s - k} years', f'{s + j} years', f'{s + k} years', f'{s + 2} years'],
                ex=f'Let the son be x and the father y today. Then y − {k} = {m}(x − {k}) and y + {j} = {n}(x + {j}), so y = {m}x − {(m-1)*k} and y = {n}x + {(n-1)*j}. Equating, {m-n}x = {(m-1)*k + (n-1)*j}, so x = {s} and the father is {f}. Check: {s-k} and {f-k} ({TIMES[m]}); {s+j} and {f+j} ({TIMES[n]}).',
                fast=f'Back-substitute: take the son\'s age from an option, find the father from the first statement ({m} × (x − {k}) + {k}) and test the second.', secs=60,
                d='moderate', topic=T_LIN, check=str(s), k='ch02.ages', data={'k': k, 'j': j, 'm': TIMES[m], 'n': TIMES[n]})


def two_digit(r):
    t, u = r.randint(1, 9), r.randint(1, 9)
    if t >= u: return None
    n = 10 * t + u; D = 9 * (u - t); S = t + u
    return dict(q=f'The sum of the digits of a two-digit number is {S}. The number obtained by reversing the digits is {D} more than the original number. The number is:',
                a=str(n), w=[str(10 * u + t), str(10 * (t + 1) + (u - 1)) if t + 1 != u else str(n + 9), str(10 * (t - 1) + u + 1) if t > 1 else str(n + 18), str(n + 9)],
                ex=f'Let the tens digit be a and the units digit b, so the number is 10a + b. Then a + b = {S} and (10b + a) − (10a + b) = {D}, i.e. 9(b − a) = {D}, so b − a = {u - t}. Solving, a = {t}, b = {u}, and the number is {n}. The reversed number {10*u+t} is the trap.',
                fast=f'Reversal changes a number by 9 × (difference of digits): {D} ÷ 9 = {u - t}. Two digits summing to {S} and differing by {u-t}, smaller digit first.', secs=40,
                d='core', topic=T_LIN, check=str(n), k='ch02.twodigit', data={'S': S, 'D': D})


def lin_frac(r):
    b, d_ = r.sample([2, 3, 4, 5, 6], 2); x = r.randint(-6, 15); a = r.randint(1, 9); c = r.randint(1, 9)
    e = F(x + a, b) - F(x - c, d_)
    if e.denominator != 1 or b == d_: return None
    e = int(e)
    return dict(q=f'Solve: (x + {a})/{b} − (x − {c})/{d_} = {e}', a=f'x = {x}', w=[f'x = {-x}' if x else 'x = 1', f'x = {x + 1}', f'x = {x - 2}', f'x = {x + 3}'],
                ex=f'Multiply both sides by the LCM {b*d_//math.gcd(b,d_)}: this removes the denominators. Expand carefully — the minus sign in front of the second fraction changes the sign of BOTH terms, giving −x + {c} in the numerator. Collect x terms on one side and solve to get x = {x}. Check by putting x = {x} back: ({x+a})/{b} − ({x-c})/{d_} = {e}.',
                fast=f'Plug each option into the left side; only x = {x} gives {e}. Integer options make this faster than solving.', secs=45, d='core', topic=T_LIN,
                k='ch02.linfrac', data={'a': a, 'b': b, 'c': c, 'd': d_, 'e': e})


def sim2(r):
    x, y = r.randint(-6, 9), r.randint(-6, 9)
    a, b, c, d_ = (r.choice([1, 2, 3, 4, 5, -2, -3]) for _ in range(4))
    if a * d_ - b * c == 0 or x == y or 0 in (x, y): return None
    e, f = a * x + b * y, c * x + d_ * y
    def side(p, q, z): return f'{poly([p], "x") if True else ""}'
    l1 = f'{poly([a, 0], "x")} {signed(b, "y")} = {e}'.replace('x x', 'x'); l2 = f'{poly([c, 0], "x")} {signed(d_, "y")} = {f}'
    return dict(q=f'Solve the simultaneous equations {l1} and {l2}.', a=xy(x, y), w=[xy(y, x), xy(-x, y), xy(x, -y), xy(x + 1, y - 1)],
                ex=f'Eliminate one unknown: multiply the equations so that the coefficients of x (or y) match, then subtract. The determinant {a}×{d_} − {b}×{c} = {a*d_ - b*c} is not zero, so there is exactly one solution: x = {x}, y = {y}. Always check in both equations: {a}({x}) + {b}({y}) = {e} and {c}({x}) + {d_}({y}) = {f}.',
                fast='Substitute each option pair into the first equation, then the second; usually only one pair passes the first.', secs=45, d='core', topic=T_SIM,
                k='ch02.sim2', data={'eq': [[a, b, e], [c, d_, f]]})


def sim3(r):
    x, y, z = (r.randint(-4, 6) for _ in range(3))
    rows = [[r.choice([1, 1, 2, -1, 3]) for _ in range(3)] for _ in range(3)]
    det = (rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1]) - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0]) + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0]))
    if det == 0 or len({x, y, z}) < 3: return None
    def eq(rw): s = poly([rw[0], 0], 'x'); s += ' ' + signed(rw[1], 'y') + ' ' + signed(rw[2], 'z'); return f'{s} = {rw[0]*x + rw[1]*y + rw[2]*z}'
    ask = r.choice(['x', 'y', 'z']); val = {'x': x, 'y': y, 'z': z}[ask]
    others = [v for v in (x, y, z) if v != val]
    return dict(q=f'If {eq(rows[0])}, {eq(rows[1])} and {eq(rows[2])}, then {ask} =', a=str(val), w=[str(o) for o in others] + [str(-val) if val else '1', str(val + 1)],
                ex=f'Eliminate one unknown from two different pairs of equations to get two equations in two unknowns, solve them, and back-substitute. The solution is x = {x}, y = {y}, z = {z}, so {ask} = {val}. The other two values in the options are the remaining unknowns — read which variable is asked.',
                fast=f'Test option triples mentally: put x = {x}, y = {y}, z = {z} in all three equations. Cramer\'s rule on a calculator also works (D = {det}).', secs=90, d='hard', topic=T_THREE,
                check=str(val), k='ch02.sim3', data={'rows': [rw + [rw[0]*x + rw[1]*y + rw[2]*z] for rw in rows], 'ask': ask})


def quad_str(p, q_):
    """x² + px + q = 0 text"""
    return poly([1, p, q_]) + ' = 0'


def form_quad(r):
    a, b = r.sample(range(-9, 10), 2)
    if 0 in (a, b) or a == -b: return None
    S, P = a + b, a * b
    return dict(q=f'The quadratic equation whose roots are {a} and {b} is:', a=quad_str(-S, P), w=[quad_str(S, P), quad_str(-S, -P), quad_str(S, -P), quad_str(-P, S)],
                ex=f'An equation with roots α and β is x² − (α + β)x + αβ = 0. Here α + β = {S} and αβ = {P}, so the equation is {quad_str(-S, P)}. The usual slip is the sign of the x-term: it is MINUS the sum of the roots.',
                fast=f'Put x = {a} into each option — only the right one gives 0 (then check x = {b}).', secs=30, d='core', topic=T_QUAD, k='ch02.formq', data={'roots': [a, b]})


def sym_fn(r):
    a = r.randint(1, 5); b = r.randint(-12, 12); c = r.randint(-9, 9)
    if c == 0 or b == 0: return None
    S, P = F(-b, a), F(c, a)
    kind = r.choice(['sq', 'recip', 'ratio'])
    val = {'sq': S * S - 2 * P, 'recip': S / P, 'ratio': (S * S - 2 * P) / P}[kind]
    txt = {'sq': 'α² + β²', 'recip': '1/α + 1/β', 'ratio': 'α/β + β/α'}[kind]
    wr = {'sq': [S * S + 2 * P, S * S - P, S * S], 'recip': [P / S if S else S + 1, -S / P, S * P], 'ratio': [(S * S + 2 * P) / P, (S * S - 2 * P), S * S / P]}[kind]
    form = {'sq': '(α + β)² − 2αβ', 'recip': '(α + β)/αβ', 'ratio': '(α² + β²)/αβ = [(α + β)² − 2αβ]/αβ'}[kind]
    return dict(q=f'If α and β are the roots of {poly([a, b, c])} = 0, then {txt} =', a=fr(val), w=[fr(x) for x in wr] + [fr(val + 1)],
                ex=f'For ax² + bx + c = 0, α + β = −b/a = {fr(S)} and αβ = c/a = {fr(P)}. Write the expression in terms of these: {txt} = {form} = {fr(val)}. Watch the sign of α + β — it is −b/a, not b/a.',
                fast=f'Sum = {fr(S)}, product = {fr(P)}; plug into {form}. No need to find the roots.', secs=45, d='moderate', topic=T_QUAD, check=frx(val),
                k='ch02.symfn', data={'abc': [a, b, c], 'kind': txt})


NAT = ['Real, rational and unequal', 'Real, irrational and unequal', 'Real and equal', 'Imaginary (not real)']


def nature(r):
    a = r.randint(1, 6); b = r.randint(-12, 12); c = r.randint(-10, 10)
    if c == 0: return None
    D = b * b - 4 * a * c
    ans = NAT[2] if D == 0 else NAT[3] if D < 0 else NAT[0] if math.isqrt(D) ** 2 == D else NAT[1]
    if ans == NAT[2] and r.random() < .5: return None
    return dict(q=f'The roots of {poly([a, b, c])} = 0 are:', a=ans, w=[x for x in NAT if x != ans],
                ex=f'Find the discriminant D = b² − 4ac = ({b})² − 4({a})({c}) = {D}. If D > 0 and a perfect square, the roots are real, rational and unequal; if D > 0 but not a perfect square, real and irrational; D = 0 gives equal roots; D < 0 gives imaginary roots. Here D = {D}, so: {ans.lower()}.',
                fast='Compute only b² − 4ac and read its sign; then check whether it is a perfect square.', secs=30, d='core', topic=T_NAT, k='ch02.nature', data={'abc': [a, b, c]})


def equal_roots(r):
    a = r.choice([1, 4, 9, 16, 25]); c = r.choice([1, 4, 9, 16, 25, 36, 49, 64, 81])
    k = 2 * math.isqrt(a) * math.isqrt(c)
    if a == c: return None
    lead = f'{a}x²' if a > 1 else 'x²'
    return dict(q=f'If {lead} − kx + {c} = 0 has equal roots and k > 0, then k =', a=str(k), w=[str(k // 2), str(4 * a * c), str(k * 2), str(a + c), str(k + 2)],
                ex=f'Equal roots need the discriminant to be zero: k² − 4 × {a} × {c} = 0, so k² = {4*a*c} and k = ±{k}. With k > 0, k = {k}. Then the left side is a perfect square: ({math.isqrt(a) if a > 1 else ""}x − {math.isqrt(c)})².',
                fast=f'Perfect-square pattern: k = 2 × √{a} × √{c} = {k}.', secs=25, d='core', topic=T_NAT, check=str(k), k='ch02.eqroots', data={'a': a, 'c': c})


def cubic_coefs(rs_):
    a, b, c = rs_
    return [1, -(a + b + c), a * b + b * c + c * a, -a * b * c]


def cubic_other(r):
    roots = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 3)
    g, o1, o2 = roots; co = cubic_coefs(roots)
    if 0 in co[1:]: return None
    def pr(a, b): a, b = sorted((a, b)); return f'{a} and {b}'
    return dict(q=f'One root of {poly(co)} = 0 is {g}. The other two roots are:', a=pr(o1, o2), w=[pr(-o1, -o2), pr(o1, -o2), pr(-o1, o2), pr(o1 + 1, o2 + 1)],
                ex=f'Divide by (x − {g}) using synthetic division: the quotient is a quadratic, {poly([1, -(o1 + o2), o1 * o2])}. Its roots are {o1} and {o2}. Check with the sum of all three roots: {g} + {o1} + {o2} = {g + o1 + o2}, which equals −(coefficient of x²) = {-co[1]}.',
                fast=f'Sum of roots = {-co[1]} and product = {-co[3]}: the other two must add to {-co[1] - g} and multiply to {fr(F(-co[3], g))}. Pick the matching option.', secs=50,
                d='moderate', topic=T_CUB, k='ch02.cubother', data={'co': co, 'g': g})


def cubic_coef(r):
    rt = r.choice([-3, -2, -1, 1, 2, 3, 4]); p = r.randint(-8, 8); q_ = r.randint(-30, 30)
    # x³ + p x² + a x + q = 0 with x = rt a root: rt³ + p rt² + a rt + q = 0
    num_ = -(rt ** 3 + p * rt * rt + q_)
    if num_ % rt or p == 0 or q_ == 0: return None
    a = num_ // rt
    if a == 0: return None
    s = f'x³ {signed(p, "x²")} + ax {"+" if q_ > 0 else "−"} {abs(q_)} = 0'
    return dict(q=f'If x = {rt} is a root of {s}, then a =', a=str(a), w=[str(-a), str(a + rt), str(a - 1), str(2 * a)],
                ex=f'A root satisfies the equation. Put x = {rt}: ({rt})³ + ({p})({rt})² + a({rt}) + ({q_}) = 0, i.e. {rt**3 + p*rt*rt + q_} + {rt}a = 0. So a = {a}. Errors usually come from squaring or cubing a negative root with the wrong sign.',
                fast=f'Substitute x = {rt} once and solve the one-line equation for a.', secs=35, d='core', topic=T_CUB, check=str(a), k='ch02.cubcoef', data={'rt': rt, 'p': p, 'q': q_})


def cubic_vieta(r):
    roots = r.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 3); co = cubic_coefs(roots); lead = r.choice([1, 2])
    co = [c * lead for c in co]
    kind = r.choice(['sum', 'pair', 'prod'])
    val = {'sum': F(-co[1], co[0]), 'pair': F(co[2], co[0]), 'prod': F(-co[3], co[0])}[kind]
    txt = {'sum': 'α + β + γ', 'pair': 'αβ + βγ + γα', 'prod': 'αβγ'}[kind]
    if 0 in co: return None
    return dict(q=f'If α, β, γ are the roots of {poly(co)} = 0, then {txt} =', a=fr(val), w=[fr(-val), fr(F(co[1], co[0])) if kind != 'sum' else fr(F(co[2], co[0])), fr(F(co[3], co[0])) if kind != 'prod' else fr(F(-co[1], co[0])), fr(val + 1)],
                ex=f'For ax³ + bx² + cx + d = 0: α + β + γ = −b/a, αβ + βγ + γα = c/a and αβγ = −d/a. Here a = {co[0]}, b = {co[1]}, c = {co[2]}, d = {co[3]}, so {txt} = {fr(val)}. The signs alternate: minus, plus, minus.',
                fast='Vieta with alternating signs: −b/a, +c/a, −d/a.', secs=25, d='core', topic=T_CUB, check=frx(val), k='ch02.cubvieta', data={'co': co, 'kind': txt})


def rect(r):
    b = r.randint(4, 40); dd = r.randint(2, 15); A = b * (b + dd)
    return dict(q=f'The length of a rectangular plot is {dd} m more than its breadth and its area is {inr(A)} sq m. The breadth is:', a=f'{b} m',
                w=[f'{b + dd} m', f'{b + 1} m' if (b + 1) != b + dd else f'{b + 2} m', f'{b - 1} m', f'{round(math.sqrt(A))} m' if round(math.sqrt(A)) not in (b, b + dd) else f'{b + dd + 1} m'],
                ex=f'Let breadth = x m; length = x + {dd}. Then x(x + {dd}) = {A}, i.e. x² + {dd}x − {A} = 0, which factorises as (x − {b})(x + {b + dd}) = 0. A length cannot be negative, so x = {b} m and the length is {b + dd} m.',
                fast=f'Find two numbers {dd} apart whose product is {inr(A)}: test the options ({b} × {b + dd} = {A}).', secs=40, d='core', topic=T_RED, check=str(b), k='ch02.rect', data={'d': dd, 'A': A})


def share_word(r):
    n = r.randint(4, 20); k = r.randint(2, 6); less = r.randint(2, 50)
    # N/n − N/(n+k) = less  -> N = less * n (n+k) / k
    N = F(less * n * (n + k), k)
    if N.denominator != 1 or N > 200000: return None
    N = int(N)
    return dict(q=f'₹{inr(N)} is shared equally among some students. If there were {k} more students, each would get ₹{less} less. The number of students is:',
                a=str(n), w=[str(n + k), str(n - 1), str(n * 2), str(n + 1)],
                ex=f'Let there be x students. Then {inr(N)}/x − {inr(N)}/(x + {k}) = {less}. Simplifying, {inr(N)} × {k} = {less} × x(x + {k}), i.e. x² + {k}x − {N*k//less} = 0, so x = {n} (the negative root is rejected). Check: ₹{inr(N//n)} each now, ₹{inr(N//(n+k))} each with {n+k} students.',
                fast=f'Test options: ₹{inr(N)} ÷ x − ₹{inr(N)} ÷ (x + {k}) must equal ₹{less}.', secs=60, d='moderate', topic=T_RED, check=str(n), k='ch02.share', data={'N': N, 'k': k, 'less': less})


def expo_quad(r):
    a = r.choice([2, 3]); p, q_ = r.sample([0, 1, 2, 3, 4], 2)
    if a ** max(p, q_) > 100: return None
    S, P = a ** p + a ** q_, a ** (p + q_)
    lo, hi = sorted((p, q_))
    def opt(x, y): return f'x = {x} or x = {y}'
    return dict(q=f'Solve: {a}^(2x) − {S}·{a}^x + {P} = 0', a=opt(lo, hi), w=[opt(a ** lo, a ** hi), opt(-hi, -lo), opt(lo + 1, hi + 1), opt(hi, hi + 1)],
                ex=f'Put y = {a}^x. The equation becomes y² − {S}y + {P} = 0, i.e. (y − {a**lo})(y − {a**hi}) = 0, so y = {a**lo} or {a**hi}. Then {a}^x = {a**lo} gives x = {lo} and {a}^x = {a**hi} gives x = {hi}. The trap is stopping at the y-values {a**lo} and {a**hi}.',
                fast=f'Substitute x from each option: {a}^(2x) − {S}·{a}^x + {P} must be 0 for both values.', secs=45, d='moderate', topic=T_RED, k='ch02.expoq', data={'a': a, 'S': S, 'P': P})


BANKS = {U: [(ages, 2), (two_digit, 2), (lin_frac, 2), (sim2, 2), (sim3, 2), (form_quad, 2), (sym_fn, 3), (nature, 3), (equal_roots, 2), (cubic_other, 2),
             (cubic_coef, 2), (cubic_vieta, 2), (rect, 2), (share_word, 2), (expo_quad, 2)]}
