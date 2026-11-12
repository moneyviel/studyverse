"""Real JEE Main questions — Mathematics Unit 6: Sequence and Series. Our own solutions; chk re-solves each by brute force
(building the actual sequences with exact fractions). Skipped: 28-1-25 S1 Q18 (quadratic equation, not this unit), 5-Apr-2026 S2 Q18 (needs integration)."""
from fractions import Fraction as F
import math
from common import new_registry, pick, near, verify
P, add = new_registry()
def ap(a, d, n): return [F(a) + k * F(d) for k in range(n)]
def gp(a, r, n): return [F(a) * F(r) ** k for k in range(n)]
def solve_int(f, lo=-500, hi=500): return [x for x in range(lo, hi + 1) if f(x)]
def roots2(a, b, c):   # real roots of ax²+bx+c (floats)
    D = b * b - 4 * a * c
    return [] if D < 0 else sorted({(-b + s * math.sqrt(D)) / (2 * a) for s in (1, -1)})

# ---------------- A.P. ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'ap', 'Let a_{1}, a_{2}, a_{3}, … be in an A.P. such that Σ_{k=1}^{12} a_{2k−1} = −\\f{72}{5}a_{1}, a_{1} ≠ 0. If Σ_{k=1}^{n} a_{k} = 0, then n is :',
    ['18', '10', '17', '11'], 4, lambda: pick([18, 10, 17, 11], [n for n in range(2, 40) if sum(ap(1, F(-1, 5), n)) == 0 and sum(ap(1, F(-1, 5), 23)[::2]) == F(-72, 5)][0]),
    ['Odd terms a_{1}, a_{3}, …, a_{23}: 12 terms with difference 2d → sum = 12a_{1} + 132d.', '12a_{1} + 132d = −\\f{72}{5}a_{1} → d = −\\f{a_{1}}{5}.', 'S_{n} = \\f{n}{2}[2a_{1} − (n − 1)\\f{a_{1}}{5}] = 0 → n − 1 = 10 → n = 11.'], 'ap', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'ap', 'The number of terms of an A.P. is even; the sum of all the odd terms is 24, the sum of all the even terms is 30 and the last term exceeds the first by \\f{21}{2}. Then the number of terms which are integers in the A.P. is :',
    ['10', '8', '6', '4'], 4, lambda: pick([10, 8, 6, 4], next(sum(1 for t in ap(a, d, 2 * n) if t.denominator == 1) for n in range(1, 20) for d in [F(6, n)] for a in [(24 - n * (n - 1) * d) / n] if (2 * n - 1) * d == F(21, 2))),
    ['Let there be 2n terms. (even sum) − (odd sum) = nd = 6.', 'Last − first = (2n − 1)d = \\f{21}{2} → 12 − d = 10.5 → d = \\f{3}{2}, n = 4 (8 terms).', 'Odd sum: 4a + 4·3·\\f{3}{2} = 24 → a = \\f{3}{2}. Terms 1.5, 3, 4.5, …, 12 → integers 3, 6, 9, 12 → 4.'], 'ap', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'ap', 'Let A = {1, 6, 11, 16, …} and B = {9, 16, 23, 30, …} be the sets consisting of the first 2025 terms of two arithmetic progressions. Then n(A ∪ B) is',
    ['4027', '3814', '3761', '4003'], 3, lambda: pick([4027, 3814, 3761, 4003], len({1 + 5 * k for k in range(2025)} | {9 + 7 * k for k in range(2025)})),
    ['Common terms satisfy x ≡ 1 (mod 5) and x ≡ 2 (mod 7) → x = 16, 51, 86, … (difference 35).', 'A ends at 10121, so common terms 16 + 35t ≤ 10121 → 289 of them.', 'n(A ∪ B) = 2025 + 2025 − 289 = 3761.'], 'ap', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'ap', 'Consider two sets A and B, each containing three numbers in A.P. Let the sum and the product of the elements of A be 36 and p respectively and the sum and the product of the elements of B be 36 and q respectively. Let d and D be the common differences of AP\'s in A and B respectively such that D = d + 3, d > 0. If \\f{p + q}{p − q} = \\f{19}{5}, then p − q is equal to',
    ['630', '540', '450', '600'], 2, lambda: pick([630, 540, 450, 600], next(12 * (144 - d * d) - 12 * (144 - (d + 3) ** 2) for d in range(1, 60) if F(12 * (144 - d * d) + 12 * (144 - (d + 3) ** 2), 12 * (144 - d * d) - 12 * (144 - (d + 3) ** 2)) == F(19, 5))),
    ['Middle term = 12 for both. p = 12(144 − d^{2}), q = 12(144 − D^{2}).', '\\f{288 − d^{2} − D^{2}}{D^{2} − d^{2}} = \\f{19}{5} → 1440 + 14d^{2} = 24D^{2}; with D = d + 3: 5d^{2} + 72d − 612 = 0 → d = 6, D = 9.', 'p − q = 12(81 − 36) = 540.'], 'ap', 3)
add(('2024', 'Apr', '2024-04-05', 1), 'ap', 'Let a_{1}, a_{2}, a_{3}, … be in an arithmetic progression of positive terms. Let A_{k} = a_{1}^{2} − a_{2}^{2} + a_{3}^{2} − a_{4}^{2} + … + a_{2k−1}^{2} − a_{2k}^{2}. If A_{3} = −153, A_{5} = −435 and a_{1}^{2} + a_{2}^{2} + a_{3}^{2} = 66, then a_{17} − A_{7} is equal to ______',
    None, 910, lambda: next(int(s[16] - sum(s[i] ** 2 * (-1) ** i for i in range(14))) for a in range(1, 30) for d in range(1, 30) for s in [ap(a, d, 20)] if sum(s[i] ** 2 * (-1) ** i for i in range(6)) == -153 and sum(s[i] ** 2 * (-1) ** i for i in range(10)) == -435 and sum(x * x for x in s[:3]) == 66),
    ['a_{2k−1}^{2} − a_{2k}^{2} = −d(a_{2k−1} + a_{2k}) → A_{k} = −d·S_{2k}.', 'd·S_{6} = 153 and d·S_{10} = 435 → d(2a + 5d) = 51, d(2a + 9d) = 87 → d = 3, a = 1 (check 1 + 16 + 49 = 66).', 'a_{17} = 49; A_{7} = −3·S_{14} = −3 × 7 × 41 = −861 → 49 + 861 = 910.'], 'ap', 3)
add(('2024', 'Apr', '2024-04-08', 2), 'ap', 'An arithmetic progression is written in the following way: row 1: 2; row 2: 5, 8; row 3: 11, 14, 17; row 4: 20, 23, 26, 29; … The sum of all the terms of the 10^{th} row is ______',
    None, 1505, lambda: int(sum(ap(2, 3, 55)[45:55])),
    ['Row k has k terms, so rows 1–9 use 45 terms; row 10 is terms 46 to 55 of 2, 5, 8, … (d = 3).', 'a_{46} = 137, a_{55} = 164 → sum = 5(137 + 164) = 1505.'], 'ap', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'ap', 'Let A be the set of first 101 terms of an A.P., whose first term is 1 and the common difference is 5 and let B be the set of first 71 terms of an A.P., whose first term is 9 and the common difference is 7. Then the number of elements in A ∩ B, which are divisible by 3, is :',
    ['4', '5', '6', '7'], 2, lambda: pick([4, 5, 6, 7], sum(1 for x in {1 + 5 * k for k in range(101)} & {9 + 7 * k for k in range(71)} if x % 3 == 0)),
    ['Common terms: x ≡ 1 (mod 5), x ≡ 2 (mod 7) → 16, 51, 86, …, 471 (14 terms, up to min(501, 499)).', 'Divisible by 3 as well: 16 + 35t with t ≡ 1 (mod 3) → t = 1, 4, 7, 10, 13 → 5 numbers.'], 'ap', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'ap', 'Suppose that the number of terms in an A.P. is 2k, k ∈ N. If the sum of all odd terms of the A.P. is 40, the sum of all even terms is 55 and the last term of the A.P. exceeds the first term by 27, then k is equal to :',
    ['4', '5', '6', '8'], 2, lambda: pick([4, 5, 6, 8], next(k for k in range(1, 40) if (2 * k - 1) * F(15, k) == 27)),
    ['(even sum) − (odd sum) = kd = 15.', '(2k − 1)d = 27 → 30 − d = 27 → d = 3 → k = 5.'], 'ap', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'ap', 'If the first term of an A.P. is 3 and the sum of its first four terms is equal to one-fifth of the sum of the next four terms, then the sum of the first 20 terms is equal to',
    ['−1200', '−1020', '−1080', '−120'], 3, lambda: pick([-1200, -1020, -1080, -120], next(int(sum(ap(3, d, 20))) for d in range(-50, 50) if 5 * sum(ap(3, d, 4)) == sum(ap(3, d, 8)[4:]))),
    ['S_{4} = 12 + 6d and the next four sum to 12 + 22d.', '5(12 + 6d) = 12 + 22d → d = −6.', 'S_{20} = 10(6 − 114) = −1080.'], 'ap', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'ap', 'The roots of the quadratic equation 3x^{2} − px + q = 0 are 10^{th} and 11^{th} terms of an arithmetic progression with common difference \\f{3}{2}. If the sum of the first 11 terms of this arithmetic progression is 88, then q − 2p is equal to ______.',
    None, 474, lambda: (lambda s: int(3 * s[9] * s[10] - 2 * 3 * (s[9] + s[10])))(next(s for a in [F(k, 2) for k in range(-100, 100)] for s in [ap(a, F(3, 2), 11)] if sum(s) == 88)),
    ['S_{11} = 11a_{6} = 88 → a_{6} = 8 → a_{10} = 14, a_{11} = 15.5.', 'p = 3(14 + 15.5) = 88.5, q = 3 × 14 × 15.5 = 651.', 'q − 2p = 651 − 177 = 474.'], 'ap', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'ap', 'In an arithmetic progression, if S_{40} = 1030 and S_{12} = 57, then S_{30} − S_{10} is equal to :',
    ['505', '515', '510', '525'], 2, lambda: pick([505, 515, 510, 525], next(int(sum(ap(a, d, 30)) - sum(ap(a, d, 10))) for a in [F(k, 2) for k in range(-40, 40)] for d in [F(k, 2) for k in range(-20, 20)] if sum(ap(a, d, 40)) == 1030 and sum(ap(a, d, 12)) == 57)),
    ['20(2a + 39d) = 1030 and 6(2a + 11d) = 57 → 28d = 42 → d = 1.5, a = −3.5.', 'S_{30} − S_{10} = 15(−7 + 43.5) − 5(−7 + 13.5) = 547.5 − 32.5 = 515.'], 'ap', 2)
add(('2025', 'Jan', '2025-01-28', 2), 'ap', 'The interior angles of a polygon with n sides, are in an A.P. with common difference 6°. If the largest interior angle of the polygon is 219°, then n is equal to ______.',
    None, 20, lambda: next(n for n in range(3, 60) if sum(ap(219, -6, n)) == (n - 2) * 180),
    ['Angles 219, 213, …: sum = \\f{n}{2}[438 − 6(n − 1)].', 'Equal to (n − 2)180 → n^{2} − 14n − 120 = 0 → n = 20.'], 'ap', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'ap', 'Let a_{1}, a_{2}, …, a_{2024} be an Arithmetic Progression such that a_{1} + (a_{5} + a_{10} + a_{15} + … + a_{2020}) + a_{2024} = 2233. Then a_{1} + a_{2} + a_{3} + … + a_{2024} is equal to ______.',
    None, 11132, lambda: (lambda c: int(F(2233, c) * 1012))(1 + F(404, 2)),
    ['a_{1} + a_{2024} = a_{5} + a_{2020} = … = s (indices add to 2025).', 'a_{5}, a_{10}, …, a_{2020} are 404 terms pairing up to 202s → total 203s = 2233 → s = 11.', 'Sum of 2024 terms = 1012s = 11132.'], 'ap', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'ap', 'The first term of an A.P. of 30 non-negative terms is \\f{10}{3}. If the sum of this A.P. is the cube of its last term, then its common difference is:',
    ['\\f{5}{87}', '\\f{25}{83}', '\\f{15}{29}', '\\f{5}{29}'], 1, lambda: pick(['\\f{5}{87}', '\\f{25}{83}', '\\f{15}{29}', '\\f{5}{29}'], (lambda d: f'\\f{{{d.numerator}}}{{{d.denominator}}}')(next((l - F(10, 3)) / 29 for l in range(0, 50) if 15 * (F(10, 3) + l) == l ** 3))),
    ['S = 15(\\f{10}{3} + l) = l^{3} → l^{3} − 15l − 50 = 0 → l = 5.', 'd = \\f{5 − 10/3}{29} = \\f{5}{87}.'], 'ap', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'ap', 'If the sum of the first four terms of an A.P. is 6 and the sum of its first six terms is 4, then the sum of its first twelve terms is',
    ['−20', '−24', '−26', '−22'], 4, lambda: pick([-20, -24, -26, -22], next(int(sum(ap(a, d, 12))) for a in [F(k, 4) for k in range(-40, 40)] for d in [F(k, 6) for k in range(-30, 30)] if sum(ap(a, d, 4)) == 6 and sum(ap(a, d, 6)) == 4)),
    ['2(2a + 3d) = 6 and 3(2a + 5d) = 4 → d = −\\f{5}{6}, 2a = \\f{11}{2}.', 'S_{12} = 6(\\f{11}{2} − \\f{55}{6}) = −22.'], 'ap', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'ap', 'Let the sum of the first n terms of an A.P. be 3n^{2} + 5n. Then the sum of squares of the first 10 terms of the A.P. is:',
    ['10220', '12860', '15220', '19780'], 3, lambda: pick([10220, 12860, 15220, 19780], sum(((3 * n * n + 5 * n) - (3 * (n - 1) ** 2 + 5 * (n - 1))) ** 2 for n in range(1, 11))),
    ['a_{n} = S_{n} − S_{n−1} = 6n + 2.', 'Σ(6n + 2)^{2} = 36·385 + 24·55 + 4·10 = 15220.'], 'ap', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'ap', 'Consider an A.P.: a_{1}, a_{2}, …, a_{n}; a_{1} > 0. If a_{2} − a_{1} = −\\f{3}{4}, a_{n} = \\f{1}{4}a_{1}, and Σ_{i=1}^{n} a_{i} = \\f{525}{2}, then Σ_{i=1}^{17} a_{i} is equal to',
    ['476', '952', '238', '136'], 3, lambda: pick([476, 952, 238, 136], next(int(sum(ap(a1, F(-3, 4), 17))) for n in range(2, 100) for a1 in [F(n - 1)] if sum(ap(a1, F(-3, 4), n)) == F(525, 2))),
    ['a_{n} = a_{1} − \\f{3}{4}(n − 1) = \\f{a_{1}}{4} → a_{1} = n − 1.', 'S_{n} = \\f{n}{2} × \\f{5}{4}(n − 1) = \\f{525}{2} → n(n − 1) = 420 → n = 21, a_{1} = 20.', 'Σ_{1}^{17} = \\f{17}{2}(40 − 12) = 238.'], 'ap', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'ap', 'Let a_{1}, a_{2}, a_{3}, a_{4} be an A.P. of four terms such that each term of the A.P. and its common difference l are integers. If a_{1} + a_{2} + a_{3} + a_{4} = 48 and a_{1}a_{2}a_{3}a_{4} + l^{4} = 361, then the largest term of the A.P. is equal to',
    ['27', '24', '21', '23'], 1, lambda: pick([27, 24, 21, 23], max(max(s) for a in range(-100, 100) for l in range(-30, 31) for s in [[a + k * l for k in range(4)]] if sum(s) == 48 and s[0] * s[1] * s[2] * s[3] + l ** 4 == 361)),
    ['Terms 12 − \\f{3l}{2}, 12 − \\f{l}{2}, 12 + \\f{l}{2}, 12 + \\f{3l}{2}.', '(144 − \\f{9l^{2}}{4})(144 − \\f{l^{2}}{4}) + l^{4} = 361 → l^{2} = 100 (the other root 130.4 is not a square).', 'l = ±10 → terms −3, 7, 17, 27 → largest 27.'], 'ap', 3)
add(('2026', 'Jan', '2026-01-28', 1), 'ap', 'The common difference of the A.P.: a_{1}, a_{2}, …, a_{m} is 13 more than the common difference of the A.P.: b_{1}, b_{2}, …, b_{n}. If b_{31} = −277, b_{43} = −385 and a_{78} = 327, then a_{1} is equal to',
    ['21', '24', '19', '16'], 3, lambda: pick([21, 24, 19, 16], 327 - 77 * ((-385 + 277) // 12 + 13)),
    ['d_{b} = \\f{−385 + 277}{12} = −9 → d_{a} = 4.', 'a_{1} = 327 − 77 × 4 = 19.'], 'ap', 1)

# ---------------- G.P. ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'gp', 'Let a_{1}, a_{2}, a_{3}, … be a G.P. of increasing positive numbers. If a_{3}a_{5} = 729 and a_{2} + a_{4} = \\f{111}{4}, then 24(a_{1} + a_{2} + a_{3}) is equal to',
    ['131', '129', '128', '130'], 2, lambda: pick([131, 129, 128, 130], next(int(24 * sum(gp(F(27, r ** 3), r, 3))) for r in range(2, 20) if F(27, r * r) + 27 == F(111, 4))),
    ['a_{3}a_{5} = a_{4}^{2} = 729 → a_{4} = 27.', 'a_{2} = \\f{111}{4} − 27 = \\f{3}{4} → r^{2} = 36, r = 6.', 'a_{1} = \\f{1}{8}: 24(\\f{1}{8} + \\f{3}{4} + \\f{9}{2}) = 3 + 18 + 108 = 129.'], 'gp', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'gp', 'If the sum of the second, fourth and sixth terms of a G.P. of positive terms is 21 and the sum of its eighth, tenth and twelfth terms is 15309, then the sum of its first nine terms is :',
    ['755', '757', '760', '750'], 2, lambda: pick([755, 757, 760, 750], next(int(sum(gp(a, 3, 9))) for a in [F(21, 3 + 27 + 243)] if sum(gp(a, 3, 12)[7::2]) == 15309)),
    ['Second triple ÷ first = r^{6} = \\f{15309}{21} = 729 → r = 3.', 'a(3 + 27 + 243) = 21 → a = \\f{1}{13}.', 'S_{9} = \\f{1}{13} × \\f{3^{9} − 1}{2} = 757.'], 'gp', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'gp', 'In an increasing geometric progression of positive terms, the sum of the second and sixth terms is \\f{70}{3} and the product of the third and fifth terms is 49. Then the sum of the 4^{th}, 6^{th} and 8^{th} terms is :',
    ['96', '78', '91', '84'], 3, lambda: pick([96, 78, 91, 84], int(7 + 7 * 3 + 7 * 9) if abs(7 / 3 + 7 * 3 - 70 / 3) < 1e-9 else 0),
    ['a_{3}a_{5} = a_{4}^{2} = 49 → a_{4} = 7.', 'a_{2} + a_{6} = 7(\\f{1}{r^{2}} + r^{2}) = \\f{70}{3} → r^{2} = 3.', 'a_{4} + a_{6} + a_{8} = 7 + 21 + 63 = 91.'], 'gp', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'gp', 'Let a, ar, ar^{2}, … be an infinite G.P. If Σ_{n=0}^{∞} ar^{n} = 57 and Σ_{n=0}^{∞} a^{3}r^{3n} = 9747, then a + 18r is equal to :',
    ['27', '46', '38', '31'], 4, lambda: pick([27, 46, 38, 31], next(int(a + 18 * r) for r in [F(k, 12) for k in range(-11, 12)] for a in [57 * (1 - r)] if a ** 3 / (1 - r ** 3) == 9747)),
    ['\\f{a}{1 − r} = 57 and \\f{a^{3}}{1 − r^{3}} = 9747. Cube the first and divide: \\f{(1 − r)^{2}}{1 + r + r^{2}} = \\f{1}{19}.', '6r^{2} − 13r + 6 = 0 → r = \\f{2}{3} (|r| < 1), a = 19.', 'a + 18r = 19 + 12 = 31.'], 'gp', 3)
add(('2026', 'Jan', '2026-01-21', 1), 'gp', 'Let a_{1}, a_{2}, a_{3}, … be a G.P. of increasing positive terms such that a_{2}·a_{3}·a_{4} = 64 and a_{1} + a_{3} + a_{5} = \\f{813}{7}. Then a_{3} + a_{5} + a_{7} is equal to:',
    ['3256', '3252', '3244', '3248'], 2, lambda: pick([3256, 3252, 3244, 3248], next(int(4 + 4 * u + 4 * u * u) for u in range(2, 100) if F(4, u) + 4 + 4 * u == F(813, 7))),
    ['a_{2}a_{3}a_{4} = a_{3}^{3} = 64 → a_{3} = 4.', '\\f{4}{r^{2}} + 4 + 4r^{2} = \\f{813}{7} → r^{2} = 28.', 'a_{3} + a_{5} + a_{7} = 4 + 112 + 3136 = 3252.'], 'gp', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'gp', 'Let a_{1}, \\f{a_{2}}{2}, \\f{a_{3}}{2^{2}}, …, \\f{a_{10}}{2^{9}} be a G.P. of common ratio \\f{1}{√{2}}. If a_{1} + a_{2} + … + a_{10} = 62, then a_{1} is equal to:',
    ['2(√{2} − 1)', '2 − √{2}', '√{2} − 1', '2(2 − √{2})'], 1, lambda: near([2 * (2 ** 0.5 - 1), 2 - 2 ** 0.5, 2 ** 0.5 - 1, 2 * (2 - 2 ** 0.5)], 62 / sum(2 ** (k / 2) for k in range(10))),
    ['\\f{a_{k}}{2^{k−1}} = a_{1}(\\f{1}{√{2}})^{k−1} → a_{k} = a_{1}(√{2})^{k−1}.', 'Sum = a_{1}\\f{(√{2})^{10} − 1}{√{2} − 1} = \\f{31a_{1}}{√{2} − 1} = 62 → a_{1} = 2(√{2} − 1).'], 'gp', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'gp', 'Let a_{1}, a_{2}, a_{3}, … be a G.P. of increasing positive terms. If a_{1}a_{5} = 28 and a_{2} + a_{4} = 29, then a_{6} is equal to :',
    ['784', '812', '628', '526'], 1, lambda: near([784, 812, 628, 526], max(r for r in roots2(1, -29 / 28 ** 0.5, 1)) ** 3 * 28 ** 0.5),
    ['a_{1}a_{5} = a_{3}^{2} = 28 → a_{3} = 2√{7}.', 'a_{3}(r + \\f{1}{r}) = 29 → r = 2√{7} (increasing).', 'a_{6} = a_{3}r^{3} = 2√{7} × 56√{7} = 784.'], 'gp', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'gp', 'In a G.P., if the product of the first three terms is 27 and the set of all possible values for the sum of its first three terms is R − (a, b), then a^{2} + b^{2} is equal to ______.',
    None, 90, lambda: (lambda lo, hi: lo * lo + hi * hi)(3 * (-2 + 1), 3 * (2 + 1)),
    ['Terms \\f{3}{r}, 3, 3r (product 27). Sum = 3(1 + r + \\f{1}{r}).', 'r + \\f{1}{r} ≤ −2 or ≥ 2 → sum ≤ −3 or ≥ 9 → R − (−3, 9).', 'a^{2} + b^{2} = 9 + 81 = 90.'], 'gp', 2)

# ---------------- mixed A.P. / G.P. and means ----------------
add(('2024', 'Apr', '2024-04-04', 2), 'means', 'Let three real numbers a, b, c be in arithmetic progression and a + 1, b, c + 3 be in geometric progression. If a > 10 and the arithmetic mean of a, b and c is 8, then the cube of the geometric mean of a, b and c is',
    ['120', '312', '316', '128'], 1, lambda: pick([120, 312, 316, 128], next(a * 8 * (16 - a) for a in range(11, 17) if (a + 1) * (16 - a + 3) == 64)),
    ['b = 8, a + c = 16.', '(a + 1)(c + 3) = 64 → (a + 1)(19 − a) = 64 → a = 15 (a > 10), c = 1.', '(GM)^{3} = abc = 15 × 8 × 1 = 120.'], 'mix', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'means', 'Let the first three terms 2, p and q, with q ≠ 2, of a G.P. be respectively the 7^{th}, 8^{th} and 13^{th} terms of an A.P. If the 5^{th} term of the G.P. is the n^{th} term of the A.P., then n is equal to',
    ['151', '169', '177', '163'], 4, lambda: pick([151, 169, 177, 163], next(int((2 * F(2 + d, 2) ** 4 - (2 - 6 * d)) / d) + 1 for d in range(1, 50) if (2 + d) ** 2 == 2 * (2 + 6 * d))),
    ['p = 2 + d, q = 2 + 6d; p^{2} = 2q → d^{2} = 8d → d = 8 (q ≠ 2).', 'p = 10 → r = 5; 5th G.P. term = 2 × 5^{4} = 1250.', 'A.P.: a_{1} = 2 − 48 = −46; −46 + 8(n − 1) = 1250 → n = 163.'], 'mix', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'means', 'For x ≥ 0, the least value of K, for which 4^{1+x} + 4^{1−x}, \\f{K}{2}, 16^{x} + 16^{−x} are three consecutive terms of an A.P., is equal to :',
    ['10', '4', '8', '16'], 1, lambda: pick([10, 4, 8, 16], round(min(4 * (4 ** x + 4 ** -x) + 16 ** x + 16 ** -x for x in [i / 1000 for i in range(0, 3000)]), 6)),
    ['K = 4(4^{x} + 4^{−x}) + (16^{x} + 16^{−x}). Let t = 4^{x} + 4^{−x} ≥ 2 → 16^{x} + 16^{−x} = t^{2} − 2.', 'K = t^{2} + 4t − 2 is increasing for t ≥ 2 → least at t = 2: K = 10.'], 'mix', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'means', 'Let x_{1}, x_{2}, x_{3}, x_{4} be in a geometric progression. If 2, 7, 9, 5 are subtracted respectively from x_{1}, x_{2}, x_{3}, x_{4}, then the resulting numbers are in an arithmetic progression. Then the value of \\f{1}{24}(x_{1}x_{2}x_{3}x_{4}) is:',
    ['18', '36', '216', '72'], 3, lambda: pick([18, 36, 216, 72], next(int(F(a * a * r * a * r * r * a * r ** 3, 24)) for a in range(-50, 51) if a for r in range(-10, 11) if r not in (0, 1) and len({a - 2 - (a * r - 7), a * r - 7 - (a * r * r - 9), a * r * r - 9 - (a * r ** 3 - 5)}) == 1)),
    ['Terms a, ar, ar^{2}, ar^{3}. AP conditions: a(r − 1)^{2} = −3 and ar(r − 1)^{2} = −6 → r = 2, a = −3.', 'x: −3, −6, −12, −24 → product 5184 → \\f{5184}{24} = 216.'], 'mix', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'means', 'Let the arithmetic mean of \\f{1}{a} and \\f{1}{b} be \\f{5}{16}, a > 2. If α is such that a, 4, α, b are in A.P., then the equation αx^{2} − ax + 2(α − 2b) = 0 has:',
    ['complex roots of magnitude less than 2', 'one root in (0, 2) and another in (−4, −2)', 'one root in (1, 4) and another in (−2, 0)', 'both roots in the interval (−2, 0)'], 3,
    lambda: (lambda a: (lambda al, b: 3 if (lambda r: len(r) == 2 and 1 < r[1] < 4 and -2 < r[0] < 0)(roots2(al, -a, 2 * (al - 2 * b))) else 0)(8 - a, 12 - 2 * a))(max(r for r in roots2(5, -34, 48))),
    ['a, 4, α, b in A.P. → α = 8 − a, b = 12 − 2a.', '\\f{1}{a} + \\f{1}{12 − 2a} = \\f{5}{8} → 5a^{2} − 34a + 48 = 0 → a = \\f{24}{5} (a > 2).', 'α = \\f{16}{5}, b = \\f{12}{5}: equation 2x^{2} − 3x − 2 = 0 → x = 2, −\\f{1}{2}.'], 'mix', 3)
add(('2026', 'Apr', '2026-04-02', 2), 'means', 'Let a_{1}, a_{2}, a_{3}, … be an A.P. and g_{1} = a_{1}, g_{2}, g_{3}, … be an increasing G.P. If a_{1} = a_{2} + g_{2} = 1 and a_{3} + g_{3} = 4, then a_{10} + g_{5} is equal to :',
    ['81', '76', '62', '55'], 4, lambda: pick([81, 76, 62, 55], next(1 + 9 * (-r) + r ** 4 for r in range(2, 20) if 1 + 2 * (-r) + r * r == 4)),
    ['a_{2} + g_{2} = (1 + d) + r = 1 → d = −r.', 'a_{3} + g_{3} = 1 − 2r + r^{2} = 4 → r = 3, d = −3.', 'a_{10} + g_{5} = (1 − 27) + 81 = 55.'], 'mix', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'means', 'Suppose a, b, c are in A.P. and a^{2}, 2b^{2}, c^{2} are in G.P. If a < b < c and a + b + c = 1, then 9(a^{2} + b^{2} + c^{2}) is equal to ______.',
    None, 9, lambda: int(9 * (F(4, 9) - 2 * F(-2, 9) + F(1, 9))),
    ['b = \\f{1}{3}, a + c = \\f{2}{3}. G.P.: 4b^{4} = a^{2}c^{2} → ac = ±\\f{2}{9}; ac = \\f{2}{9} gives no real a ≠ c, so ac = −\\f{2}{9}.', 'a^{2} + c^{2} = \\f{4}{9} + \\f{4}{9} = \\f{8}{9} → 9(\\f{8}{9} + \\f{1}{9}) = 9.'], 'mix', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'means', 'The sum of the first ten terms of an A.P. is 160 and the sum of the first two terms of a G.P. is 8. If the first term of the A.P. is equal to the common ratio of the G.P. and the first term of the G.P. is equal to common difference of the A.P., then the sum of all possible values of the first term of the G.P. is:',
    ['\\f{34}{9}', '\\f{34}{13}', '\\f{32}{9}', '\\f{32}{13}'], 1, lambda: pick(['\\f{34}{9}', '\\f{34}{13}', '\\f{32}{9}', '\\f{32}{13}'], '\\f{' + str(F(34, 9).numerator) + '}{' + str(F(34, 9).denominator) + '}') if len(roots2(9, -34, 16)) == 2 else 0,
    ['A.P.: first term r, difference g → 2r + 9g = 32. G.P.: g(1 + r) = 8.', 'Substitute r = \\f{32 − 9g}{2}: 9g^{2} − 34g + 16 = 0 (two real roots).', 'Sum of the possible g = \\f{34}{9}.'], 'mix', 2)

# ---------------- special series (telescoping) ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'special', 'If the sum of the first 10 terms of the series \\f{4·1}{1 + 4·1^{4}} + \\f{4·2}{1 + 4·2^{4}} + \\f{4·3}{1 + 4·3^{4}} + … is \\f{m}{n}, where gcd(m, n) = 1, then m + n is equal to ______',
    None, 441, lambda: (lambda s: s.numerator + s.denominator)(sum(F(4 * k, 1 + 4 * k ** 4) for k in range(1, 11))),
    ['1 + 4k^{4} = (2k^{2} − 2k + 1)(2k^{2} + 2k + 1) and their difference is 4k.', 'So T_{k} = \\f{1}{2k^{2} − 2k + 1} − \\f{1}{2k^{2} + 2k + 1} — it telescopes.', 'Sum = 1 − \\f{1}{221} = \\f{220}{221} → m + n = 441.'], 'tele', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'special', 'If the sum of the first 20 terms of the series \\f{4·1}{4 + 3·1^{2} + 1^{4}} + \\f{4·2}{4 + 3·2^{2} + 2^{4}} + \\f{4·3}{4 + 3·3^{2} + 3^{4}} + \\f{4·4}{4 + 3·4^{2} + 4^{4}} + … is \\f{m}{n}, where m and n are coprime, then m + n is equal to :',
    ['423', '420', '422', '421'], 4, lambda: pick([423, 420, 422, 421], (lambda s: s.numerator + s.denominator)(sum(F(4 * k, 4 + 3 * k * k + k ** 4) for k in range(1, 21)))),
    ['k^{4} + 3k^{2} + 4 = (k^{2} + k + 2)(k^{2} − k + 2).', 'T_{k} = 2[\\f{1}{k^{2} − k + 2} − \\f{1}{k^{2} + k + 2}] — telescoping.', 'Sum = 2[\\f{1}{2} − \\f{1}{422}] = \\f{210}{211} → 421.'], 'tele', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'special', 'Let S_{n} = \\f{1}{2} + \\f{1}{6} + \\f{1}{12} + \\f{1}{20} + … upto n terms. If the sum of the first six terms of an A.P. with first term −p and common difference p is √{2026S_{2025}}, then the absolute difference between 20^{th} and 15^{th} terms of the A.P. is',
    ['45', '20', '25', '90'], 3, lambda: pick([45, 20, 25, 90], (lambda root: 5 * root / 9)(math.isqrt(int(2026 * F(2025, 2026))))),
    ['\\f{1}{k(k + 1)} = \\f{1}{k} − \\f{1}{k + 1} → S_{n} = \\f{n}{n + 1}; 2026S_{2025} = 2025 → √ = 45.', 'Six terms: 3(−2p + 5p) = 9p = 45 → p = 5.', '|a_{20} − a_{15}| = 5p = 25.'], 'tele', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'special', 'If the sum of the first 10 terms of the series \\f{1}{1 + 1^{4} × 4} + \\f{2}{1 + 2^{4} × 4} + \\f{3}{1 + 3^{4} × 4} + \\f{4}{1 + 4^{4} × 4} + … is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to :',
    ['256', '264', '276', '284'], 3, lambda: pick([256, 264, 276, 284], (lambda s: s.numerator + s.denominator)(sum(F(k, 1 + 4 * k ** 4) for k in range(1, 11)))),
    ['\\f{k}{1 + 4k^{4}} = \\f{1}{4}[\\f{1}{2k^{2} − 2k + 1} − \\f{1}{2k^{2} + 2k + 1}].', 'Sum = \\f{1}{4}(1 − \\f{1}{221}) = \\f{55}{221} → 276.'], 'tele', 2)

if __name__ == '__main__': print(verify(P), 'real questions verified')
