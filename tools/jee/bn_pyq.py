"""Real JEE Main questions — Mathematics Unit 5: Binomial Theorem. Our own solutions; chk re-solves each one by actually
expanding the powers term by term with exact fractions (fractional exponents included), by computing remainders with
modular powers, and by evaluating the coefficient sums directly. Skipped: items from other units that the keyword
search also caught (trigonometry, calculus, statistics, counting)."""
import math, itertools
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
C = math.comb
def expand(terms, n):
    """(Σ coef·x^exp)^n as {exp: coef}, exps are Fractions."""
    out = {F(0): F(1)}
    for _ in range(n):
        nxt = {}
        for e1, c1 in out.items():
            for c2, e2 in terms:
                nxt[e1 + F(e2)] = nxt.get(e1 + F(e2), 0) + c1 * F(c2)
        out = nxt
    return out
def mul(A, B):
    out = {}
    for e1, c1 in A.items():
        for e2, c2 in B.items(): out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
    return out
def rat_sum(n, parts):
    """Sum of the rational terms of (Σ base_i^{1/q_i})^n; parts = [(base, q)] with base 1 meaning the constant 1."""
    tot = 0
    for ks in itertools.product(range(n + 1), repeat=len(parts)):
        if sum(ks) != n: continue
        if all(k % q == 0 or b == 1 for k, (b, q) in zip(ks, parts)):
            tot += math.factorial(n) // math.prod(math.factorial(k) for k in ks) * math.prod(b ** (k // q) if b != 1 else 1 for k, (b, q) in zip(ks, parts))
    return tot

# ---------------- general term, constant term, a given coefficient ----------------
add(('2024', 'Apr', '2024-04-05', 2), 'term', 'If the constant term in the expansion of (\\f{⁵√{3}}{x} + \\f{2x}{∛{5}})^{12}, x ≠ 0, is α × 2^{8} × ⁵√{3}, then 25α is equal to :', ['639', '724', '693', '742'], 3,
    lambda: pick([639, 724, 693, 742], 25 * F(C(12, 6) * 2 ** 6 * 3, 25 * 2 ** 8)), ['T_{r+1} = C(12, r)(3^{1/5})^{12−r}(2/5^{1/3})^{r} x^{2r − 12}: constant at r = 6.', 'C(12, 6) · 3^{6/5} · \\f{2^{6}}{5^{2}} = \\f{924 · 3 · 64}{25} · 3^{1/5} = \\f{693}{25} × 2^{8} × 3^{1/5} → 25α = 693.'], 'term', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'term', 'If the constant term in the expansion of (1 + 2x − 3x^{3})(\\f{3}{2}x^{2} − \\f{1}{3x})^{9} is p, then 108p is equal to ____.', None, 54,
    lambda: int(108 * mul({F(0): 1, F(1): 2, F(3): -3}, expand([(F(3, 2), 2), (F(-1, 3), -1)], 9)).get(F(0), 0)),
    ['T_{r+1} of the bracket: C(9, r)(\\f{3}{2})^{9−r}(−\\f{1}{3})^{r} x^{18 − 3r}.', 'x^{0} (r = 6) pairs with 1: \\f{7}{18}; x^{−3} (r = 7) is −\\f{1}{27} and pairs with −3x^{3}: \\f{1}{9}.', 'p = \\f{7}{18} + \\f{2}{18} = \\f{1}{2} → 108p = 54.'], 'term', 3)
add(('2024', 'Apr', '2024-04-06', 1), 'term', 'If the second, third and fourth terms in the expansion of (x + y)^{n} are 135, 30 and \\f{10}{3}, respectively, then 6(n^{3} + x^{2} + y) is equal to ____.', None, 806,
    lambda: next(int(6 * (n ** 3 + x * x + y)) for n in range(3, 20) for x in [F(3)] for y in [F(1, 3)] if n * x ** (n - 1) * y == 135 and C(n, 2) * x ** (n - 2) * y ** 2 == 30 and C(n, 3) * x ** (n - 3) * y ** 3 == F(10, 3)),
    ['T_{3}/T_{2} = \\f{n − 1}{2}·\\f{y}{x} = \\f{2}{9}, T_{4}/T_{3} = \\f{n − 2}{3}·\\f{y}{x} = \\f{1}{9} → n = 5, \\f{y}{x} = \\f{1}{9}.', '5x^{4}y = 135 → x = 3, y = \\f{1}{3} → 6(125 + 9 + \\f{1}{3}) = 806.'], 'term', 3)
add(('2024', 'Apr', '2024-04-08', 2), 'term', 'If the term independent of x in the expansion of (√{a}x^{2} + \\f{1}{2x^{3}})^{10} is 105, then a^{2} is equal to :', ['4', '9', '6', '2'], 1,
    lambda: pick([4, 9, 6, 2], next(a * a for a in range(1, 10) if expand([(1, 2), (F(1, 2), -3)], 10)[F(0)] * a ** 3 == 105)),   # (√a)^{6} = a^{3} rides along with r = 4
    ['Power of x in T_{r+1}: 2(10 − r) − 3r = 0 → r = 4.', 'C(10, 4) a^{3} / 2^{4} = 105 → a^{3} = 8 → a = 2, a^{2} = 4.'], 'term', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'term', 'The sum of the coefficient of x^{2/3} and x^{−2/5} in the binomial expansion of (x^{2/3} + \\f{1}{2}x^{−2/5})^{9} is :', ['\\f{21}{4}', '\\f{69}{16}', '\\f{63}{16}', '\\f{19}{4}'], 1,
    lambda: (lambda E: pick([F(21, 4), F(69, 16), F(63, 16), F(19, 4)], E[F(2, 3)] + E[F(-2, 5)]))(expand([(1, F(2, 3)), (F(1, 2), F(-2, 5))], 9)),
    ['Power in T_{r+1}: \\f{2(9 − r)}{3} − \\f{2r}{5}. It is \\f{2}{3} at r = 5 and −\\f{2}{5} at r = 6.', '\\f{C(9, 5)}{32} + \\f{C(9, 6)}{64} = \\f{63}{16} + \\f{21}{16} = \\f{21}{4}.'], 'term', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'term', 'If the coefficient of x in the expansion of (ax^{2} + bx + c)(1 − 2x)^{26} is −56 and the coefficients of x^{2} and x^{3} are both zero, then a + b + c is equal to:', ['1300', '1500', '1403', '1483'], 3,
    lambda: (lambda d: pick([1300, 1500, 1403, 1483], next(a + b + c for c in range(-50, 51) for b in [-56 - c * d(1)] for a in [-(c * d(2) + b * d(1))] if c * d(3) + b * d(2) + a * d(1) == 0)))(lambda k: expand([(1, 0), (-2, 1)], 26)[F(k)]),
    ['With d_{k} = C(26, k)(−2)^{k}: x: c d_{1} + b = −56; x^{2}: c d_{2} + b d_{1} + a = 0; x^{3}: c d_{3} + b d_{2} + a d_{1} = 0.', 'd_{1} = −52, d_{2} = 1300, d_{3} = −20800 → c = 3, b = 100, a = 1300 → a + b + c = 1403.'], 'term', 3)
add(('2025', 'Jan', '2025-01-22', 2), 'term', 'Let α, β, γ and δ be the coefficients of x^{7}, x^{5}, x^{3} and x respectively in the expansion of (x + √{x^{3} − 1})^{5} + (x − √{x^{3} − 1})^{5}, x > 1. If u and v satisfy the equations αu + βv = 18, γu + δv = 20, then u + v equals :', ['8', '3', '5', '4'], 3,
    lambda: (lambda co: (lambda al, be, ga, de: pick([8, 3, 5, 4], (lambda D: (F(18 * de - 20 * be, D) + F(al * 20 - ga * 18, D)))(al * de - be * ga)))(co(7), co(5), co(3), co(1)))(lambda k: sum(2 * C(5, 2 * j) * c * (1 if e + 5 - 2 * j == k else 0) for j in range(3) for e, c in expand([(1, 3), (-1, 0)], j).items())),
    ['Odd powers of the root cancel: 2[x^{5} + 10x^{3}(x^{3} − 1) + 5x(x^{3} − 1)^{2}] = 10x^{7} + 20x^{6} + 2x^{5} − 20x^{4} − 20x^{3} + 10x.', 'α = 10, β = 2, γ = −20, δ = 10: 10u + 2v = 18, −20u + 10v = 20 → u = 1, v = 4 → 5.'], 'term', 3)
add(('2026', 'Apr', '2026-04-04', 2), 'term', 'In the expansion of (9x − \\f{1}{3√{x}})^{18}, x > 0, if the term independent of x is (221)k, then k is equal to:', ['84', '78', '168', '198'], 1,
    lambda: pick([84, 78, 168, 198], expand([(9, 1), (F(-1, 3), F(-1, 2))], 18)[F(0)] / 221), ['Power: (18 − r) − \\f{r}{2} = 0 → r = 12.', 'C(18, 12) 9^{6} 3^{−12} = 18564 = 221 × 84.'], 'term', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'term', 'If the sum of the coefficients of x^{7} and x^{14} in the expansion of (\\f{1}{x^{3}} − x^{4})^{n}, x ≠ 0, is zero, then the value of n is ____.', None, 21,
    lambda: next(n for n in range(1, 60) if (lambda E: E.get(F(7), 0) + E.get(F(14), 0) == 0 and (F(7) in E or F(14) in E))(expand([(1, -3), (-1, 4)], n))),
    ['T_{r+1} has x^{7r − 3n}: n must be a multiple of 7, say 7m, giving r = 3m + 1 and 3m + 2 (opposite signs).', 'C(7m, 3m + 1) = C(7m, 3m + 2) → 7m = 6m + 3 → m = 3, n = 21.'], 'term', 2)

# ---------------- rational and integral terms ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'rat', 'The sum of all rational terms in the expansion of (2 + √{3})^{8} is', ['16923', '33845', '3763', '18817'], 4,
    lambda: pick([16923, 33845, 3763, 18817], rat_sum(8, [(2, 1), (3, 2)])), ['Rational terms are those with an even power of √{3}.', 'Their sum = \\f{(2 + √{3})^{8} + (2 − √{3})^{8}}{2} = 18817.'], 'rat', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'rat', 'The sum of all rational terms in the expansion of (2^{1/5} + 5^{1/3})^{15} is equal to :', ['3133', '633', '931', '6131'], 1,
    lambda: pick([3133, 633, 931, 6131], rat_sum(15, [(2, 5), (5, 3)])), ['T_{r+1} = C(15, r) 2^{(15 − r)/5} 5^{r/3}: need 3 | r and 5 | (15 − r).', 'r = 0 and 15: 2^{3} + 5^{5} = 8 + 3125 = 3133.'], 'rat', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'rat', 'The number of integral terms in the expansion of (5^{1/2} + 7^{1/8})^{1016} is', ['129', '128', '130', '127'], 2,
    lambda: pick([129, 128, 130, 127], sum(1 for r in range(1017) if r % 8 == 0 and (1016 - r) % 2 == 0)), ['Need 8 | r (power of 7) and (1016 − r) even.', 'r = 0, 8, …, 1016 → 128 terms.'], 'rat', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'rat', 'The sum of all rational terms in the expansion of (1 + 2^{1/3} + 3^{1/2})^{6} is equal to ____.', None, 612,
    lambda: rat_sum(6, [(1, 1), (2, 3), (3, 2)]), ['General term \\f{6!}{a!b!c!} 2^{b/3} 3^{c/2}: need 3 | b and 2 | c.', 'Add the terms for the allowed (a, b, c) → 612.'], 'rat', 3)
add(('2025', 'Jan', '2025-01-28', 2), 'rat', 'Let the coefficients of three consecutive terms T_{r}, T_{r+1} and T_{r+2} in the binomial expansion of (a + b)^{12} be in a G.P. and let p be the number of all possible values of r. Let q be the sum of all rational terms in the binomial expansion of (∜{3} + ∛{4})^{12}. Then p + q is equal to :', ['299', '287', '283', '295'], 3,
    lambda: pick([299, 287, 283, 295], sum(1 for r in range(1, 12) if C(12, r) ** 2 == C(12, r - 1) * C(12, r + 1)) + rat_sum(12, [(3, 4), (4, 3)])),
    ['C(12, r)^{2} > C(12, r − 1)C(12, r + 1) always, so p = 0.', 'Rational terms of (3^{1/4} + 4^{1/3})^{12}: r = 0 and 12 → 3^{3} + 4^{4} = 283.'], 'rat', 2)

# ---------------- remainders ----------------
add(('2025', 'Apr', '2025-04-07', 1), 'rem', 'The remainder when ((64)^{(64)})^{(64)} is divided by 7 is equal to', ['4', '6', '3', '1'], 4,
    lambda: pick([4, 6, 3, 1], pow(64, 64 * 64, 7)), ['64 = 63 + 1 ≡ 1 (mod 7).', 'Any power of 1 is 1 → remainder 1.'], 'rem', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'rem', 'The remainder when 428^{2024} is divided by 21 is ____.', None, 1,
    lambda: pow(428, 2024, 21), ['428 = 420 + 8 ≡ 8 (mod 21), and 8^{2} = 64 = 63 + 1 ≡ 1.', '8^{2024} = (8^{2})^{1012} ≡ 1.'], 'rem', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'rem', 'The remainder, when 7^{103} is divided by 23, is equal to :', ['9', '14', '17', '6'], 2,
    lambda: pick([9, 14, 17, 6], pow(7, 103, 23)), ['7^{2} = 49 = 46 + 3 → 7^{103} = 7 · 3^{51}; 3^{3} = 27 ≡ 4, so 3^{51} ≡ 4^{17}.', '4^{17} = 2^{34}; 2^{11} = 2048 ≡ 1 (mod 23) → 2^{34} ≡ 2 → 7 × 2 = 14.'], 'rem', 2)

# ---------------- binomial coefficients and their sums ----------------
add(('2025', 'Apr', '2025-04-04', 2), 'coef', 'If 1^{2}·(^{15}C_{1}) + 2^{2}·(^{15}C_{2}) + 3^{2}·(^{15}C_{3}) + … + 15^{2}·(^{15}C_{15}) = 2^{m}·3^{n}·5^{k}, where m, n, k ∈ N, then m + n + k is equal to :', ['20', '21', '18', '19'], 4,
    lambda: (lambda S: pick([20, 21, 18, 19], next(m + n + k for m in range(1, 30) for n in range(1, 5) for k in range(1, 5) if 2 ** m * 3 ** n * 5 ** k == S)))(sum(r * r * C(15, r) for r in range(16))),
    ['Σ r^{2}C(n, r) = n(n + 1)2^{n − 2}.', '15 · 16 · 2^{13} = 2^{17} · 3 · 5 → 17 + 1 + 1 = 19.'], 'coef', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'coef', 'If the coefficients of x^{4}, x^{5} and x^{6} in the expansion of (1 + x)^{n} are in the arithmetic progression, then the maximum value of n is :', ['14', '21', '28', '7'], 1,
    lambda: pick([14, 21, 28, 7], max(n for n in range(6, 100) if 2 * C(n, 5) == C(n, 4) + C(n, 6))), ['2C(n, 5) = C(n, 4) + C(n, 6) simplifies to n^{2} − 21n + 98 = 0.', 'n = 7 or 14 → maximum 14.'], 'coef', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'coef', 'The sum of the series 2 × 1 × ^{20}C_{4} − 3 × 2 × ^{20}C_{5} + 4 × 3 × ^{20}C_{6} − 5 × 4 × ^{20}C_{7} + … + 18 × 17 × ^{20}C_{20}, is equal to ____.', None, 34,
    lambda: sum((-1) ** r * (r - 2) * (r - 3) * C(20, r) for r in range(4, 21)),
    ['Σ_{r=0}^{20}(−1)^{r}(r − 2)(r − 3)C(20, r) = 0 (a polynomial of degree 2 < 20 in r).', 'So the asked sum = −[r = 0, 1, 2, 3 terms] = −(6 − 2 · 20 + 0 + 0) = 34.'], 'coef', 3)
add(('2026', 'Jan', '2026-01-21', 2), 'coef', 'If (\\f{1}{^{15}C_{0}} + \\f{1}{^{15}C_{1}})(\\f{1}{^{15}C_{1}} + \\f{1}{^{15}C_{2}}) … (\\f{1}{^{15}C_{12}} + \\f{1}{^{15}C_{13}}) = \\f{α^{13}}{^{14}C_{0} ^{14}C_{1} … ^{14}C_{12}}, then 30α is equal to ____.', None, 32,
    lambda: (lambda v: next(k for k in range(1, 200) if F(k, 30) ** 13 == v))(math.prod(F(1, C(15, r)) + F(1, C(15, r + 1)) for r in range(13)) * math.prod(C(14, r) for r in range(13))),
    ['\\f{1}{^{15}C_{r}} + \\f{1}{^{15}C_{r+1}} = \\f{16}{15} · \\f{1}{^{14}C_{r}}.', 'The product is \\f{(16/15)^{13}}{Π ^{14}C_{r}} → α = \\f{16}{15} → 30α = 32.'], 'coef', 3)
add(('2025', 'Jan', '2025-01-24', 1), 'coef', 'For some n ≠ 10, let the coefficients of the 5th, 6th and 7th terms in the binomial expansion of (1 + x)^{n+4} be in A.P. Then the largest coefficient in the expansion of (1 + x)^{n+4} is:', ['70', '10', '20', '35'], 4,
    lambda: pick([70, 10, 20, 35], max(C(m, k) for m in range(6, 60) if m != 14 and 2 * C(m, 5) == C(m, 4) + C(m, 6) for k in range(m + 1))), ['C(m, 4), C(m, 5), C(m, 6) in A.P. → m = 7 or 14; n ≠ 10 rules out 14.', 'm = 7: largest coefficient C(7, 3) = 35.'], 'coef', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'coef', 'Suppose A and B are the coefficients of 30^{th} and 12^{th} terms respectively in the binomial expansion of (1 + x)^{2n−1}. If 2A = 5B, then n is equal to :', ['19', '21', '20', '22'], 2,
    lambda: pick([19, 21, 20, 22], next(n for n in range(15, 40) if 2 * C(2 * n - 1, 29) == 5 * C(2 * n - 1, 11))), ['A = C(2n − 1, 29), B = C(2n − 1, 11).', 'Try the options (or simplify the ratio): n = 21 works.'], 'coef', 3)
add(('2026', 'Jan', '2026-01-22', 1), 'coef', 'The coefficient of x^{48} in (1 + x) + 2(1 + x)^{2} + 3(1 + x)^{3} + … + 100(1 + x)^{100} is equal to', ['100·^{100}C_{49} − ^{100}C_{50}', '^{100}C_{50} + ^{101}C_{49}', '100·^{100}C_{49} − ^{100}C_{48}', '100·^{101}C_{49} − ^{101}C_{50}'], 4,
    lambda: (lambda v: pick([100 * C(100, 49) - C(100, 50), C(100, 50) + C(101, 49), 100 * C(100, 49) - C(100, 48), 100 * C(101, 49) - C(101, 50)], v))(sum(k * C(k, 48) for k in range(1, 101))),
    ['Coefficient = Σ_{k} k·C(k, 48). Write k = (k + 1) − 1 and use Σ C(k, 48) = C(101, 49) (hockey stick).', 'Result 100·C(101, 49) − C(101, 50).'], 'coef', 3)
add(('2026', 'Jan', '2026-01-22', 2), 'coef', 'Let C_{r} denote the coefficient of x^{r} in the binomial expansion of (1 + x)^{n}, n ∈ N, 0 ≤ r ≤ n. If P_{n} = C_{0} − C_{1} + \\f{2^{2}}{3}C_{2} − \\f{2^{3}}{4}C_{3} + … + \\f{(−2)^{n}}{n + 1}C_{n}, then the value of Σ_{n=1}^{25} \\f{1}{P_{2n}} equals.', ['675', '525', '650', '580'], 1,
    lambda: pick([675, 525, 650, 580], sum(1 / sum(F((-2) ** r, r + 1) * C(2 * n, r) for r in range(2 * n + 1)) for n in range(1, 26))),
    ['Σ C(n, r)\\f{t^{r}}{r + 1} = \\f{(1 + t)^{n+1} − 1}{(n + 1)t}; at t = −2 with n even this is \\f{1}{n + 1}.', 'So \\f{1}{P_{2n}} = 2n + 1 → Σ_{1}^{25}(2n + 1) = 650 + 25 = 675.'], 'coef', 3)
add(('2026', 'Jan', '2026-01-28', 2), 'coef', 'The sum of the coefficients of x^{499} and x^{500} in (1 + x)^{1000} + x(1 + x)^{999} + x^{2}(1 + x)^{998} + … + x^{1000} is :', ['^{1002}C_{501}', '^{1002}C_{500}', '^{1001}C_{501}', '^{1000}C_{501}'], 2,
    lambda: (lambda co: pick([C(1002, 501), C(1002, 500), C(1001, 501), C(1000, 501)], co(499) + co(500)))(lambda k: sum(C(1000 - j, k - j) for j in range(k + 1))),
    ['Coefficient of x^{k} = Σ_{j} C(1000 − j, k − j) = C(1001, k) (hockey stick).', 'C(1001, 499) + C(1001, 500) = C(1002, 500).'], 'coef', 3)
for _p in P: _p['t'] = _p['fam']
