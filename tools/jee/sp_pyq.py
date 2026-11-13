"""Real JEE Main questions — Mathematics Unit 13: Statistics and Probability. Our own solutions; chk re-solves each
one by brute force wherever the sample space is finite (listing every outcome, committee, word or draw), by exact
Fractions for Bayes' rule, and by scanning for the unknown data values that satisfy the stated mean and variance.
Skipped: a G.P.-triples item whose key counts only whole-number ratios, items whose printed data we could not read reliably and items that belong to other units."""
import math, itertools
from fractions import Fraction as F
from math import comb
from common import new_registry, pick, verify
P, add = new_registry()
def P4(opts, v, tol=1e-9): return pick(opts, v, tol)
def mean(xs): return F(sum(xs), len(xs))
def var(xs): m = mean(xs); return sum((F(x) - m) ** 2 for x in xs) / len(xs)
def frac(s): a, b = s.split('/'); return F(int(a), int(b))

# ---------- sheet 1
def _ab2():
    out = set()
    for a in [k / 4 for k in range(0, 100)]:
        b = 19 - a; xs = [6, 4, a, 8, b, 12, 10, 13]
        if abs(sum(x * x for x in xs) / 8 - 81 - 9.25) < 1e-9: out.add(a + b + a * b)
    assert len(out) == 1; return P4([100, 105, 103, 106], out.pop())
add(('2025', 'Apr', '2025-04-02', 2), 'stat', 'If the mean and the variance of 6, 4, a, 8, b, 12, 10, 13 are 9 and 9.25 respectively, then a + b + ab is equal to :', ['100', '105', '103', '106'], 3,
    _ab2, ['Sum = 72 → a + b = 72 − 53 = 19.', 'Σx^{2} = 8(9.25 + 81) = 722 → a^{2} + b^{2} = 722 − 529 = 193 → ab = \\f{361 − 193}{2} = 84.', 'a + b + ab = 103.'], 'stat', 2)
def _pq3():
    bags = [(3, 2, 5), (4, 3, 3), (5, 1, 4)]
    p = F(bags[0][0], sum(b[0] for b in bags)); q = F(bags[2][2], sum(b[2] for b in bags)); return P4([7, 6, 8, 9], 1 / p + 1 / q)
add(('2025', 'Apr', '2025-04-02', 2), 'cond', 'Given three identical bags each containing 10 balls, whose colours are as follows : Bag I: 3 Red, 2 Blue, 5 Green; Bag II: 4 Red, 3 Blue, 3 Green; Bag III: 5 Red, 1 Blue, 4 Green. A person chooses a bag at random and takes out a ball. If the ball is Red, the probability that it is from bag I is p and if the ball is Green, the probability that it is from bag III is q, then the value of (\\f{1}{p} + \\f{1}{q}) is :', ['7', '6', '8', '9'], 1,
    _pq3, ['Equal bag sizes and equal chance of each bag, so Bayes reduces to counting balls of that colour.', 'p = \\f{3}{3 + 4 + 5} = \\f{1}{4}; q = \\f{4}{5 + 3 + 4} = \\f{1}{3}.', '\\f{1}{p} + \\f{1}{q} = 7.'], 'cond', 1)
def _rv6():
    S = sum(F(x + 1, 3 ** x) for x in range(200)); k = 1 / S
    return P4([F(4, 9), F(1, 9), F(7, 27), F(8, 27)], 1 - k * sum(F(x + 1, 3 ** x) for x in range(3)), F(1, 10 ** 30))
add(('2025', 'Apr', '2025-04-03', 2), 'dist', 'If the probability that the random variable X takes the value x is given by P(X = x) = k(x + 1)3^{−x}, x = 0, 1, 2, 3, …, where k is a constant, then P(X ≥ 3) is equal to', ['\\f{4}{9}', '\\f{1}{9}', '\\f{7}{27}', '\\f{8}{27}'], 2,
    _rv6, ['Σ(x + 1)t^{x} = \\f{1}{(1 − t)^{2}}; with t = \\f{1}{3} the sum is \\f{9}{4} → k = \\f{4}{9}.', 'P(X ≤ 2) = \\f{4}{9}(1 + \\f{2}{3} + \\f{1}{3}) = \\f{8}{9}.', 'P(X ≥ 3) = \\f{1}{9}.'], 'dist', 2)
def _v7():
    out = set()
    for a in range(0, 30):
        b = 14 - a
        if a > b and var([1, 3, a, 7, b]) == 10 and mean([1, 3, a, 7, b]) == 5: out.add(var([n + x for n, x in enumerate([1, 3, a, 7, b], 1)]))
    assert len(out) == 1; return P4([F(87, 5), 17, 16, F(82, 5)], out.pop())
add(('2025', 'Apr', '2025-04-03', 2), 'stat', 'Let the Mean and Variance of five observations x_{1} = 1, x_{2} = 3, x_{3} = a, x_{4} = 7 and x_{5} = b, a > b, be 5 and 10 respectively. Then the Variance of the observations n + x_{n}, n = 1, 2, …, 5 is', ['17.4', '17', '16', '16.4'], 3,
    _v7, ['Mean 5 → a + b = 14; Σx^{2} = 5(10 + 25) = 175 → a^{2} + b^{2} = 116 → a = 10, b = 4.', 'New data: 2, 5, 13, 11, 9 with mean 8.', 'Variance = \\f{4 + 25 + 169 + 121 + 81}{5} − 64 = 16.'], 'stat', 2)
def _com8():
    good = sum(comb(4, e) * comb(2, d) * comb(10, 12 - e - d) for e in range(3, 5) for d in range(1, 3) if 0 <= 12 - e - d <= 10)
    return P4([F(103, 182), F(17, 26), F(19, 26), F(129, 182)], F(good, comb(16, 12)))
add(('2025', 'Apr', '2025-04-04', 1), 'prob', 'The probability, of forming a 12 persons committee from 4 engineers, 2 doctors and 10 professors containing at least 3 engineers and at least 1 doctor, is', ['\\f{103}{182}', '\\f{17}{26}', '\\f{19}{26}', '\\f{129}{182}'], 4,
    _com8, ['Total C(16, 12) = 1820.', 'Favourable: (e, d) = (3, 1): 4·2·C(10, 8) = 360; (3, 2): 4·1·C(10, 7) = 480; (4, 1): 1·2·C(10, 7) = 240; (4, 2): 1·1·C(10, 6) = 210. Total 1290.', '\\f{1290}{1820} = \\f{129}{182}.'], 'prob', 2)

# ---------- sheet 2
def _v11():
    pens = [1] * 3 + [0] * 7; X = [a + b for a, b in itertools.combinations(pens, 2)]; return P4([F(2, 15), F(28, 75), F(11, 15), F(3, 5)], var(X))
add(('2025', 'Apr', '2025-04-04', 1), 'dist', 'A box contains 10 pens of which 3 are defective. A sample of 2 pens is drawn at random and let X denote the number of defective pens. Then the variance of X is', ['\\f{2}{15}', '\\f{28}{75}', '\\f{11}{15}', '\\f{3}{5}'], 2,
    _v11, ['P(X = 0) = \\f{21}{45}, P(X = 1) = \\f{21}{45}, P(X = 2) = \\f{3}{45}.', 'E(X) = \\f{27}{45} = \\f{3}{5}; E(X^{2}) = \\f{21 + 12}{45} = \\f{11}{15}.', 'Var = \\f{11}{15} − \\f{9}{25} = \\f{28}{75}.'], 'dist', 2)
def _md12():
    out = set()
    for a in range(0, 20):
        b = 8 - a; xs = [2, 3, 3, 4, 5, 7, a, b]
        if b >= 0 and mean(xs) == 4 and var(xs) == 2:
            mode = max(set(xs), key=xs.count); out.add(sum(abs(F(x) - mode) for x in xs) / 8)
    assert len(out) == 1; return P4([F(3, 4), 2, F(1, 2), 1], out.pop())
add(('2025', 'Apr', '2025-04-04', 2), 'stat', 'Let the mean and the standard deviation of the observation 2, 3, 3, 4, 5, 7, a, b be 4 and √{2} respectively. Then the mean deviation about the mode of these observations is :', ['\\f{3}{4}', '2', '\\f{1}{2}', '1'], 4,
    _md12, ['Sum 32 → a + b = 8; Σx^{2} = 8(2 + 16) = 144 → a^{2} + b^{2} = 32 → a = b = 4.', 'Data 2, 3, 3, 4, 4, 4, 5, 7: mode 4.', 'Mean deviation about 4 = \\f{2 + 1 + 1 + 0 + 0 + 0 + 1 + 3}{8} = 1.'], 'stat', 2)
def _n13():
    for n in range(1, 13):
        ps, po = F(1, 4) * F(comb(12, n), comb(51, n)), F(3, 4) * F(comb(13, n), comb(51, n))
        if ps / (ps + po) == F(11, 50): return n
add(('2025', 'Apr', '2025-04-04', 2), 'cond', 'A card from a pack of 52 cards is lost. From the remaining 51 cards, n cards are drawn and are found to be spades. If the probability of the lost card to be a spade is \\f{11}{50}, then n is equal to ______.', None, 2,
    _n13, ['Bayes: P(lost spade | n spades drawn) = \\f{\\f{1}{4}C(12, n)}{\\f{1}{4}C(12, n) + \\f{3}{4}C(13, n)} = \\f{13 − n}{52 − n}.', '\\f{13 − n}{52 − n} = \\f{11}{50} → 650 − 50n = 572 − 11n → n = 2.'], 'cond', 2)
def _v15():
    # 4a + 6b = 1 and mean 8a + 40b = 46/9, solved exactly
    D = 4 * 40 - 6 * 8; a = F(1 * 40 - 6 * F(46, 9), D); b = F(4 * F(46, 9) - 8 * 1, D)
    xs, ps = [0, 2, 4, 6, 8], [a, 2 * a, a + b, 2 * b, 3 * b]; assert sum(ps) == 1 and min(ps) >= 0
    m = sum(x * p for x, p in zip(xs, ps)); assert m == F(46, 9); return P4([F(581, 81), F(566, 81), F(173, 27), F(151, 27)], sum(x * x * p for x, p in zip(xs, ps)) - m * m)
add(('2024', 'Apr', '2024-04-04', 2), 'dist', 'If the mean of the following probability distribution of a random variable X: X = 0, 2, 4, 6, 8 with P(X) = a, 2a, a + b, 2b, 3b is \\f{46}{9}, then the variance of the distribution is', ['\\f{581}{81}', '\\f{566}{81}', '\\f{173}{27}', '\\f{151}{27}'], 2,
    _v15, ['Total 4a + 6b = 1; mean 4a + 4(a + b) + 12b + 24b = 8a + 40b = \\f{46}{9}.', 'Solving: a = \\f{1}{12}, b = \\f{1}{9}. E(X^{2}) = 4(2a) + 16(a + b) + 36(2b) + 64(3b) = 24a + 280b = 2 + \\f{280}{9}.', 'Var = E(X^{2}) − (\\f{46}{9})^{2} = \\f{566}{81}.'], 'dist', 3)
def _t16():
    p = sum(F(comb(10, x)) * F(1, 3) ** x * F(2, 3) ** (10 - x) for x in range(11) if abs(x - (10 - x)) <= 2); return int(3 ** 9 * p)
add(('2024', 'Apr', '2024-04-04', 2), 'dist', 'In a tournament, a team plays 10 matches with probabilities of winning and losing each match as \\f{1}{3} and \\f{2}{3} respectively. Let x be the number of matches that the team wins, and y be the number of matches that the team loses. If the probability P(|x − y| ≤ 2) is p, then 3^{9}p equals ______.', None, 8288,
    _t16, ['x + y = 10, so |x − y| = |2x − 10| ≤ 2 → x = 4, 5, 6.', 'p = \\f{C(10, 4)2^{6} + C(10, 5)2^{5} + C(10, 6)2^{4}}{3^{10}} = \\f{13440 + 8064 + 3360}{3^{10}}.', '3^{9}p = \\f{24864}{3} = 8288.'], 'dist', 2)
def _u17():
    urns = [(7, 5), (5, 7), (6, 6)]; pb = [F(b, r + b) for r, b in urns]; return P4([F(4, 17), F(5, 18), F(7, 18), F(5, 16)], pb[0] / sum(pb))
add(('2024', 'Apr', '2024-04-04', 1), 'cond', 'Three urns A, B and C contain 7 red, 5 black; 5 red, 7 black and 6 red, 6 black balls, respectively. One of the urn is selected at random and a ball is drawn from it. If the ball drawn is black, then the probability that it is drawn from urn A is :', ['\\f{4}{17}', '\\f{5}{18}', '\\f{7}{18}', '\\f{5}{16}'], 2,
    _u17, ['P(black | A, B, C) = \\f{5}{12}, \\f{7}{12}, \\f{6}{12}; urns equally likely.', 'P(A | black) = \\f{5}{5 + 7 + 6} = \\f{5}{18}.'], 'cond', 1)

# ---------- sheet 3
def _md18():
    out = set()
    for a in range(-20, 21):
        b = 10 - a; xs = [-3, 4, 7, -6, a, b]
        if a <= b and mean(xs) == 2 and var(xs) == 23: out.add(sum(abs(F(x) - 2) for x in xs) / 6)
    assert len(out) == 1; return P4([F(13, 3), F(16, 3), F(11, 3), F(14, 3)], out.pop())
add(('2024', 'Apr', '2024-04-04', 1), 'stat', 'Let a, b ∈ ℝ. Let the mean and the variance of 6 observations −3, 4, 7, −6, a, b be 2 and 23, respectively. The mean deviation about the mean of these 6 observations is :', ['\\f{13}{3}', '\\f{16}{3}', '\\f{11}{3}', '\\f{14}{3}'], 1,
    _md18, ['Sum 12 → a + b = 10. Σx^{2} = 6(23 + 4) = 162 → a^{2} + b^{2} = 52 → {a, b} = {4, 6}.', 'Deviations from 2: 5, 2, 5, 8, 2, 4 → total 26.', 'Mean deviation = \\f{26}{6} = \\f{13}{3}.'], 'stat', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'prob', 'The coefficients a, b, c in the quadratic equation ax^{2} + bx + c = 0 are from the set {1, 2, 3, 4, 5, 6}. If the probability of this equation having one real root bigger than the other is p, then 216p equals :', ['57', '38', '19', '76'], 2,
    lambda: P4([57, 38, 19, 76], sum(1 for a, b, c in itertools.product(range(1, 7), repeat=3) if b * b > 4 * a * c)),
    ['Two distinct real roots ⇔ b^{2} > 4ac; 216 equally likely triples.', 'b = 3: ac ≤ 2 → 3; b = 4: ac ≤ 3 → 5; b = 5: ac ≤ 6 → 14; b = 6: ac ≤ 8 → 16 (b ≤ 2 gives none).', '216p = 38.'], 'prob', 2)
def _sm21():
    K = 1 - F(1, 3) - F(1, 6) - F(1, 4); out = set()
    for al in [k / 1000 for k in range(-20000, 20001)]:
        mu = al / 3 + float(K) - 0.75; s2 = al * al / 3 + float(K) + 9 / 4 - mu * mu
        if al not in (1, 0, -3) and s2 >= 0 and abs(math.sqrt(s2) - mu - 2) < 1e-9: out.add(round(math.sqrt(s2) + mu, 6))
    assert len(out) == 1; return round(out.pop(), 6)
add(('2024', 'Apr', '2024-04-05', 2), 'dist', 'Let the mean and the standard deviation of the probability distribution X: α, 1, 0, −3 with P(X): \\f{1}{3}, K, \\f{1}{6}, \\f{1}{4} be μ and σ, respectively. If σ − μ = 2, then σ + μ is equal to ______.', None, 5,
    _sm21, ['K = 1 − \\f{1}{3} − \\f{1}{6} − \\f{1}{4} = \\f{1}{4}. μ = \\f{α}{3} − \\f{1}{2}, E(X^{2}) = \\f{α^{2}}{3} + \\f{5}{2}.', 'σ^{2} = (μ + 2)^{2} → \\f{α^{2}}{3} + \\f{5}{2} = 2μ^{2} + 4μ + 4 → \\f{α^{2}}{9} = \\f{2α}{3} → α = 6 (α = 0 would repeat the value 0).', 'μ = \\f{3}{2}, σ = \\f{7}{2} → σ + μ = 5.'], 'dist', 3)
add(('2024', 'Apr', '2024-04-05', 1), 'prob', 'The coefficients a, b, c in the quadratic equation ax^{2} + bx + c = 0 are chosen from the set {1, 2, 3, 4, 5, 6, 7, 8}. The probability of this equation having repeated roots is :', ['\\f{3}{256}', '\\f{1}{128}', '\\f{1}{64}', '\\f{3}{128}'], 3,
    lambda: P4([F(3, 256), F(1, 128), F(1, 64), F(3, 128)], F(sum(1 for a, b, c in itertools.product(range(1, 9), repeat=3) if b * b == 4 * a * c), 512)),
    ['Repeated roots ⇔ b^{2} = 4ac, so b is even and ac = (\\f{b}{2})^{2}.', 'b = 2: ac = 1 → 1; b = 4: ac = 4 → 3; b = 6: ac = 9 → 1; b = 8: ac = 16 → 3. Total 8.', '\\f{8}{512} = \\f{1}{64}.'], 'prob', 2)
def _hv(N, D, n):
    items = [1] * D + [0] * (N - D); X = [sum(c) for c in itertools.combinations(items, n)]; return var(X)
add(('2024', 'Apr', '2024-04-05', 1), 'dist', 'From a lot of 10 items, which include 3 defective items, a sample of 5 items is drawn at random. Let the random variable X denote the number of defective items in the sample. If the variance of X is σ^{2}, then 96σ^{2} is equal to ______.', None, 56,
    lambda: int(96 * _hv(10, 3, 5)), ['Hypergeometric: P(X = k) = \\f{C(3, k)C(7, 5 − k)}{C(10, 5)}: \\f{21}{252}, \\f{105}{252}, \\f{105}{252}, \\f{21}{252}.', 'E(X) = \\f{3}{2}; E(X^{2}) = \\f{105 + 420 + 189}{252} = \\f{17}{6}.', 'σ^{2} = \\f{17}{6} − \\f{9}{4} = \\f{7}{12} → 96σ^{2} = 56.'], 'dist', 2)
def _hv28(): v = _hv(12, 3, 5); return v.denominator - v.numerator
add(('2024', 'Apr', '2024-04-06', 2), 'dist', 'From a lot of 12 items containing 3 defectives, a sample of 5 items is drawn at random. Let the random variable X denote the number of defective items in the sample. Let items in the sample be drawn one by one without replacement. If variance of X is \\f{m}{n}, where gcd(m, n) = 1, then n − m is equal to ______.', None, 71,
    _hv28, ['Hypergeometric with N = 12, D = 3, n = 5: Var = n·\\f{D}{N}·\\f{N − D}{N}·\\f{N − n}{N − 1}.', '= 5·\\f{3}{12}·\\f{9}{12}·\\f{7}{11} = \\f{105}{176}.', 'n − m = 176 − 105 = 71.'], 'dist', 2)

# ---------- sheet 4
def fixstat(n, m, s, wrong, right):   # corrected mean and variance after replacing one observation
    S = n * m - wrong + right; Q = n * (s * s + m * m) - wrong * wrong + right * right; mu = F(S) / n; return mu, F(Q) / n - mu * mu
add(('2024', 'Apr', '2024-04-06', 1), 'stat', 'The mean and standard deviation of 20 observations are found to be 10 and 2, respectively. On rechecking, it was found that an observation by mistake was taken 8 instead of 12. The correct standard deviation is ______.', ['√{3.86}', '1.8', '√{3.96}', '1.94'], 3,
    lambda: P4([math.sqrt(3.86), 1.8, math.sqrt(3.96), 1.94], math.sqrt(float(fixstat(20, 10, 2, 8, 12)[1])), 1e-12),
    ['Σx = 200 → 204; Σx^{2} = 20(4 + 100) = 2080 → 2080 − 64 + 144 = 2160.', 'New mean 10.2; variance = 108 − 104.04 = 3.96.', 'SD = √{3.96}.'], 'stat', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'cond', 'A company has two plants A and B to manufacture motorcycles. 60% motorcycles are manufactured at plant A and the remaining are manufactured at plant B. 80% of the motorcycles manufactured at plant A are rated of the standard quality, while 90% of the motorcycles manufactured at plant B are rated of the standard quality. A motorcycle picked up randomly from the total production is found to be of the standard quality. If p is the probability that it was manufactured at plant B, then 126p is ______.', ['54', '64', '66', '56'], 1,
    lambda: P4([54, 64, 66, 56], 126 * (F(4, 10) * F(9, 10)) / (F(6, 10) * F(8, 10) + F(4, 10) * F(9, 10))),
    ['P(standard) = 0.6·0.8 + 0.4·0.9 = 0.84.', 'p = \\f{0.36}{0.84} = \\f{3}{7} → 126p = 54.'], 'cond', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'stat', 'The mean and standard deviation of 100 observations are 40 and 5.1, respectively. By mistake one observation is taken as 50 instead of 40. If the correct mean and the correct standard deviation are μ and σ respectively, then 10(μ + σ) is equal to', ['445', '451', '449', '447'], 3,
    lambda: (lambda r: P4([445, 451, 449, 447], 10 * (float(r[0]) + math.sqrt(float(r[1]))), 1e-9))(fixstat(100, 40, F(51, 10), 50, 40)),
    ['Σx = 4000 → 3990, μ = 39.9.', 'Σx^{2} = 100(26.01 + 1600) = 162601 → 162601 − 2500 + 1600 = 161701; σ^{2} = 1617.01 − 1592.01 = 25.', '10(39.9 + 5) = 449.'], 'stat', 2)
def _p33():
    for k in range(1, 400):
        p = F(k, 800); q = (1 - 2 * p) / 2
        if q >= 0 and (p + 4 * q + 9 * q) == 2 * (p + 2 * q + 3 * q): return P4([0, 2, 3, 1], 8 * p - 1)
add(('2025', 'Apr', '2025-04-07', 2), 'dist', 'Let a random variable X take values 0, 1, 2, 3 with P(X = 0) = P(X = 1) = p, P(X = 2) = P(X = 3) and E(X^{2}) = 2E(X). Then the value of 8p − 1 is:', ['0', '2', '3', '1'], 2,
    _p33, ['Let P(X = 2) = P(X = 3) = q: 2p + 2q = 1.', 'E(X) = p + 5q, E(X^{2}) = p + 13q; p + 13q = 2p + 10q → p = 3q.', 'p = \\f{3}{8} → 8p − 1 = 2.'], 'dist', 2)
def _c34():
    v = (F(19, 20) * F(1, 2)) / (F(19, 20) * F(1, 2) + F(1, 20) * 1); return P4([72, 64, 60, 80], v.denominator ** 2 - v.numerator ** 2)
add(('2025', 'Apr', '2025-04-07', 2), 'cond', 'A bag contains 19 unbiased coins and one coin with head on both sides. One coin drawn at random is tossed and head turns up. If the probability that the drawn coin was unbiased, is \\f{m}{n}, gcd(m, n) = 1, then n^{2} − m^{2} is equal to :', ['72', '64', '60', '80'], 4,
    _c34, ['P(H) = \\f{19}{20}·\\f{1}{2} + \\f{1}{20}·1 = \\f{21}{40}.', 'P(unbiased | H) = \\f{19/40}{21/40} = \\f{19}{21}.', 'n^{2} − m^{2} = 441 − 361 = 80.'], 'cond', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'cond', 'There are three bags X, Y and Z. Bag X contains 5 one-rupee coins and 4 five-rupee coins; Bag Y contains 4 one-rupee coins and 5 five-rupee coins and Bag Z contains 3 one-rupee coins and 6 five-rupee coins. A bag is selected at random and a coin drawn from it at random is found to be a one-rupee coin. Then the probability, that it came from bag Y, is :', ['\\f{1}{3}', '\\f{1}{2}', '\\f{1}{4}', '\\f{5}{12}'], 1,
    lambda: P4([F(1, 3), F(1, 2), F(1, 4), F(5, 12)], F(4, 9) / (F(5, 9) + F(4, 9) + F(3, 9))),
    ['All bags have 9 coins and are equally likely.', 'P(Y | one-rupee) = \\f{4}{5 + 4 + 3} = \\f{1}{3}.'], 'cond', 1)

# ---------- sheet 5
def _abc36():
    res = []
    for a in range(1, 80):
        for b in range(a + 1, 80):
            for c in range(b + 1, 80):
                xs = [9, 25, a, b, c]
                if mean(xs) == 18 and sum(abs(F(x) - 18) for x in xs) / 5 == 4 and var(xs) == F(136, 5): res.append(2 * a + b - c)
    assert len(res) == 1; return res[0]
add(('2024', 'Apr', '2024-04-08', 2), 'stat', 'Let a, b, c ∈ ℕ and a < b < c. Let the mean, the mean deviation about the mean and the variance of the 5 observations 9, 25, a, b, c be 18, 4 and \\f{136}{5}, respectively. Then 2a + b − c is equal to ______.', None, 33,
    _abc36, ['Mean 18 → a + b + c = 56. Variance: Σ(x − 18)^{2} = 136 → 81 + 49 + Σ(a, b, c deviations)^{2} = 136 → their squares add to 6.', 'Mean deviation: 9 + 7 + Σ|dev| = 20 → Σ|dev| = 4 with squares summing to 6 and deviations summing to 2 (to balance −9 + 7): −1, 1, 2.', 'a = 17, b = 19, c = 20 → 2a + b − c = 33.'], 'stat', 3)
def _n37():
    pairs = [(x, 24 - x) for x in range(1, 24)]; best = max(x * y for x, y in pairs); v = F(sum(1 for x, y in pairs if x * y >= F(3, 4) * best), len(pairs))
    return P4([9, 11, 8, 10], v.denominator - v.numerator)
add(('2024', 'Apr', '2024-04-08', 1), 'prob', 'Let the sum of two positive integers be 24. If the probability, that their product is not less than \\f{3}{4} times their greatest positive product, is \\f{m}{n}, where gcd(m, n) = 1, then n − m equals :', ['9', '11', '8', '10'], 4,
    _n37, ['Pairs (x, 24 − x), x = 1, …, 23; greatest product 144.', 'x(24 − x) ≥ 108 ⇔ 6 ≤ x ≤ 18: 13 pairs.', '\\f{13}{23} → n − m = 10.'], 'prob', 2)
def _xy38():
    balls = ['B'] * 5 + ['Y'] * 4; draws = list(itertools.combinations(range(9), 3))
    X = mean([sum(balls[i] == 'B' for i in d) for d in draws]); Y = mean([sum(balls[i] == 'Y' for i in d) for d in draws]); return int(7 * X + 4 * Y)
add(('2024', 'Apr', '2024-04-08', 1), 'dist', 'Three balls are drawn at random from a bag containing 5 blue and 4 yellow balls. Let the random variables X and Y respectively denote the number of blue and Yellow balls. If X̄ and Ȳ are the means of X and Y respectively, then 7X̄ + 4Ȳ is equal to ______.', None, 17,
    _xy38, ['Each ball is in the sample with chance \\f{3}{9}: X̄ = \\f{5}{3}, Ȳ = \\f{4}{3}.', '7·\\f{5}{3} + 4·\\f{4}{3} = \\f{51}{3} = 17.'], 'dist', 1)
def _c40():
    for c in range(1, 50):
        xs = [c, c] + [k * c for k in range(2, 7)]
        if var(xs) == 160: return P4([5, 8, 7, 6], c)
add(('2024', 'Apr', '2024-04-09', 2), 'stat', 'If the variance of the frequency distribution x: c, 2c, 3c, 4c, 5c, 6c with f: 2, 1, 1, 1, 1, 1 is 160, then the value of c ∈ ℕ is', ['5', '8', '7', '6'], 3,
    _c40, ['For c = 1 the data are 1, 1, 2, 3, 4, 5, 6: mean \\f{22}{7}, mean of squares \\f{92}{7} → variance \\f{92}{7} − \\f{484}{49} = \\f{160}{49}.', 'Scaling by c multiplies the variance by c^{2}: \\f{160}{49}c^{2} = 160 → c = 7.'], 'stat', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'prob', 'If an unbiased dice is rolled thrice, then the probability of getting a greater number in the i^{th} roll than the number obtained in the (i − 1)^{th} roll, i = 2, 3, is equal to :', ['\\f{3}{54}', '\\f{2}{54}', '\\f{5}{54}', '\\f{1}{54}'], 3,
    lambda: P4([F(3, 54), F(2, 54), F(5, 54), F(1, 54)], F(sum(1 for a, b, c in itertools.product(range(1, 7), repeat=3) if a < b < c), 216)),
    ['Strictly increasing triples are just choices of 3 different faces: C(6, 3) = 20.', '\\f{20}{216} = \\f{5}{54}.'], 'prob', 1)
def _md42():
    out = set()
    for x in range(0, 11):
        y = 10 - x; data = [15] * 5 + [16] * 8 + [17] * 5 + [18] * 12 + [19] * x + [20] * y; s = sorted(data); med = F(s[19] + s[20], 2)
        if sum(abs(F(v) - med) for v in data) / 40 == F(5, 4): out.add(4 * x + 5 * y)
    assert len(out) == 1; return P4([43, 44, 47, 46], out.pop())
add(('2024', 'Apr', '2024-04-09', 1), 'stat', 'The frequency distribution of the age of students in a class of 40 students is: age 15, 16, 17, 18, 19, 20 with numbers 5, 8, 5, 12, x, y. If the mean deviation about the median is 1.25, then 4x + 5y is equal to :', ['43', '44', '47', '46'], 2,
    _md42, ['x + y = 10. Cumulative 5, 13, 18, 30: the 20th and 21st ages are 18 → median 18.', 'Σ|age − 18| = 15 + 16 + 5 + 0 + x + 2y = 36 + x + 2y = 40·1.25 = 50 → x + 2y = 14.', 'y = 4, x = 6 → 4x + 5y = 44.'], 'stat', 2)

# ---------- sheet 6
def _mn(cond):
    v = F(sum(1 for a, b, c in itertools.product(range(1, 5), repeat=3) if cond(a, b, c)), 64); return v.numerator + v.denominator
add(('2024', 'Apr', '2024-04-09', 1), 'prob', 'Let a, b and c denote the outcome of three independent rolls of a fair tetrahedral die, whose four faces are marked 1, 2, 3, 4. If the probability that ax^{2} + bx + c = 0 has all real roots is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to ______.', None, 19,
    lambda: _mn(lambda a, b, c: b * b >= 4 * a * c), ['Real roots ⇔ b^{2} ≥ 4ac. b = 2: ac = 1 → 1; b = 3: ac ≤ 2 → 3; b = 4: ac ≤ 4 → 8 (ac = 1, 2, 2, 3, 3, 4, 4, 4).', 'Total 12 of 64 = \\f{3}{16} → m + n = 19.'], 'prob', 2)
def _k44():
    mids = [F(15, 2) + 5 * i for i in range(6)]
    for k in range(0, 200):
        f = [2, k, 28, 54, k + 1, 5]
        if sum(m * x for m, x in zip(mids, f)) / sum(f) == 21:
            eq = [2 * k * k - 23 * k - 10, 4 * k * k - 35 * k + 24, 2 * k * k - 19 * k - 10, 2 * k * k - 35 * k + 98]; h = [i + 1 for i, e in enumerate(eq) if e == 0]; assert len(h) == 1; return h[0]
add(('2026', 'Apr', '2026-04-02', 1), 'stat', 'If the mean of the data with classes 5–10, 10–15, 15–20, 20–25, 25–30, 30–35 and frequencies 2, k, 28, 54, k + 1, 5 is 21, then k is one of the roots of the equation :', ['2x^{2} − 23x − 10 = 0', '4x^{2} − 35x + 24 = 0', '2x^{2} − 19x − 10 = 0', '2x^{2} − 35x + 98 = 0'], 3,
    _k44, ['Use mid-points 7.5, 12.5, …, 32.5: Σfx = 15 + 12.5k + 490 + 1215 + 27.5(k + 1) + 162.5 = 1910 + 40k.', 'Σf = 90 + 2k; mean 21: 1910 + 40k = 1890 + 42k → k = 10.', '2(100) − 190 − 10 = 0 ✓ → 2x^{2} − 19x − 10 = 0.'], 'stat', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'prob', 'Let a, b, c ∈ {1, 2, 3, 4}. If the probability, that ax^{2} + 2√{2}bx + c > 0 for all x ∈ ℝ, is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to ______.', None, 81,
    lambda: _mn(lambda a, b, c: 2 * b * b < a * c), ['a > 0 always, so need discriminant < 0: 8b^{2} < 4ac ⇔ ac > 2b^{2}.', 'b = 1: ac ≥ 3 → 13; b = 2: ac ≥ 9 → 4 (ac = 9, 12, 12, 16). b ≥ 3 impossible.', '\\f{17}{64} → m + n = 81.'], 'prob', 2)
def _p47():
    for x in range(0, 20):
        y = 14 - x; xs = [2, 4, 10, x, 12, 14, y]
        if x > y and mean(xs) == 8 and var(xs) == 16:
            S = [1, 2, 3, x - 4, y, 5]; pr = list(itertools.permutations(S, 2)); return P4([F(3, 5), F(4, 5), F(2, 5), F(1, 3)], F(sum(1 for u, v in pr if min(u, v) < 4), len(pr)))
add(('2026', 'Jan', '2026-01-21', 1), 'prob', 'Let the mean and variance of 7 observations 2, 4, 10, x, 12, 14, y, x > y, be 8 and 16 respectively. Two numbers are chosen from {1, 2, 3, x − 4, y, 5} one after another without replacement, then the probability, that the smaller number among the two chosen numbers is less than 4, is :', ['\\f{3}{5}', '\\f{4}{5}', '\\f{2}{5}', '\\f{1}{3}'], 2,
    _p47, ['x + y = 14 and Σx^{2} = 7(16 + 64) = 560 → x^{2} + y^{2} = 100 → x = 8, y = 6.', 'Set {1, 2, 3, 4, 6, 5}. The smaller is ≥ 4 only if both come from {4, 5, 6}: 3·2 = 6 of 30 ordered pairs.', 'P = 1 − \\f{6}{30} = \\f{4}{5}.'], 'prob', 2)
def _k50():
    xs = [F(4), F(30, 7), F(32, 7), F(34, 7), F(36, 7), F(38, 7), F(40, 7), F(6)]; ps = [F(2, 15), F(1, 15), F(2, 15), F(1, 5), F(1, 15), F(2, 15), F(1, 5), F(1, 15)]
    k = F(263, 15) / sum(x * p for x, p in zip(xs, ps)); return P4([F(3, 5), F(14, 15), F(8, 15), F(11, 15)], sum(p for x, p in zip(xs, ps) if x * k < 20))
add(('2026', 'Jan', '2026-01-28', 2), 'dist', 'The probability distribution of a random variable X is: X = 4k, \\f{30}{7}k, \\f{32}{7}k, \\f{34}{7}k, \\f{36}{7}k, \\f{38}{7}k, \\f{40}{7}k, 6k with P(X) = \\f{2}{15}, \\f{1}{15}, \\f{2}{15}, \\f{1}{5}, \\f{1}{15}, \\f{2}{15}, \\f{1}{5}, \\f{1}{15}. If E(X) = \\f{263}{15}, then P(X < 20) is equal to :', ['\\f{3}{5}', '\\f{14}{15}', '\\f{8}{15}', '\\f{11}{15}'], 4,
    _k50, ['E(X) = k·\\f{1}{105}(56 + 30 + 64 + 102 + 36 + 76 + 120 + 42) = \\f{526k}{105}; = \\f{263}{15} → k = \\f{7}{2}.', 'Values: 14, 15, 16, 17, 18, 19, 20, 21.', 'P(X < 20) = 1 − \\f{1}{5} − \\f{1}{15} = \\f{11}{15}.'], 'dist', 2)
def _c51():
    p = [F(1), F(1, 2)]
    for n in range(2, 7): p.append(F(1, 2) * p[-1] + F(1, 2) * p[-2])
    return P4([53, 55, 107, 105], p[6].numerator + p[6].denominator)
add(('2026', 'Apr', '2026-04-02', 2), 'dist', 'A man throws a fair coin repeatedly. He gets 10 points for each head he throws and 5 points for each tail he throws. If the probability that he gets exactly 30 points is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to:', ['53', '55', '107', '105'], 3,
    _c51, ['In units of 5 points each toss adds 1 (tail) or 2 (head). Let p_{n} = P(the running total ever equals n).', 'p_{n} = \\f{1}{2}p_{n−1} + \\f{1}{2}p_{n−2}, p_{0} = 1, p_{1} = \\f{1}{2}: \\f{3}{4}, \\f{5}{8}, \\f{11}{16}, \\f{21}{32}, \\f{43}{64}.', 'p_{6} = \\f{43}{64} → 107.'], 'dist', 3)

# ---------- sheet 7
def _n52():
    for n in range(2, 200):
        x = 8 * n - 48
        if 496 + x * x == 80 * n: return P4([21, 16, 13, 7], n)
add(('2026', 'Apr', '2026-04-02', 2), 'stat', 'The mean and variance of n observations are 8 and 16, respectively. If the sum of the first (n − 1) observations is 48 and the sum of squares of the first (n − 1) observations is 496, then the value of n is :', ['21', '16', '13', '7'], 4,
    _n52, ['Last observation x = 8n − 48; Σx^{2} = n(16 + 64) = 80n → x^{2} = 80n − 496.', '(8n − 48)^{2} = 80n − 496 → 4n^{2} − 53n + 175 = 0 → n = 7 (or \\f{25}{4}, not whole).'], 'stat', 2)
def _ab54():
    for k in range(-300, 301):
        a = F(k, 10); ps = [(2 * a + 1) / 30, (8 * a - 1) / 30, (4 * a + 1) / 30]; b = 1 - sum(ps); ps.append(b)
        if min(ps) >= 0 and b > 0 and sum(x * x * p for x, p in enumerate(ps)) == 2: return P4([30, 3, 60, 12], a / b)
add(('2026', 'Jan', '2026-01-21', 2), 'dist', 'A random variable X takes values 0, 1, 2, 3 with probabilities \\f{2a + 1}{30}, \\f{8a − 1}{30}, \\f{4a + 1}{30}, b respectively, where a, b ∈ ℝ. Let μ and σ respectively be the mean and standard deviation of X such that σ^{2} + μ^{2} = 2. Then \\f{a}{b} is equal to :', ['30', '3', '60', '12'], 3,
    _ab54, ['σ^{2} + μ^{2} = E(X^{2}) = \\f{8a − 1}{30} + \\f{4(4a + 1)}{30} + 9b = 2.', 'Total probability: \\f{14a + 1}{30} + b = 1 → b = \\f{29 − 14a}{30}.', 'Then 24a + 3 + 9(29 − 14a) = 60 → a = 2, b = \\f{1}{30} → \\f{a}{b} = 60.'], 'dist', 2)
def _bb55():
    balls = 'W' * 4 + 'B' * 6; pr = list(itertools.permutations(range(10), 2)); sec = [p for p in pr if balls[p[1]] == 'B']
    v = F(sum(1 for p in sec if balls[p[0]] == 'B'), len(sec)); return P4([4, 14, 13, 11], v.numerator + v.denominator)
add(('2025', 'Jan', '2025-01-22', 1), 'cond', 'Two balls are selected at random one by one without replacement from a bag containing 4 white and 6 black balls. If the probability that the first selected ball is black, given that the second selected ball is also black, is \\f{m}{n}, where gcd(m, n) = 1, then m + n is equal to :', ['4', '14', '13', '11'], 2,
    _bb55, ['P(2nd black) = \\f{6}{10} (by symmetry); P(both black) = \\f{6}{10}·\\f{5}{9}.', 'P(1st B | 2nd B) = \\f{5}{9} → m + n = 14.'], 'cond', 1)
def _ht57():
    X = [sum(1 for i in range(2) if s[i] == 'H' and s[i + 1] == 'T') for s in itertools.product('HT', repeat=3)]; return P4([64, 51, 48, 32], 64 * (mean(X) + var(X)))
add(('2025', 'Jan', '2025-01-22', 1), 'dist', 'A coin is tossed three times. Let X denote the number of times a tail follows a head. If μ and σ^{2} denote the mean and variance of X, then the value of 64(μ + σ^{2}) is :', ['64', '51', '48', '32'], 3,
    _ht57, ['List the 8 outcomes: HT appears once in HHT, HTH, HTT, THT; never in HHH, THH, TTH, TTT.', 'X ∈ {0, 1}: P(X = 1) = \\f{4}{8} = \\f{1}{2}. μ = \\f{1}{2}, σ^{2} = \\f{1}{4}.', '64·\\f{3}{4} = 48.'], 'dist', 2)
def _n59():
    for N in range(20, 200):
        if 12 + F(F(N, 2) - 18, 12) * 6 == 14: return P4([44, 48, 52, 40], N)
add(('2025', 'Jan', '2025-01-23', 1), 'stat', 'Marks obtains by all the students of class 12 are presented in a frequency distribution with classes of equal width. Let the median of this grouped data be 14 with median class interval 12–18 and median class frequency 12. If the number of students whose marks are less than 12 is 18, then the total number of students is', ['44', '48', '52', '40'], 1,
    _n59, ['Median = l + \\f{N/2 − cf}{f}·h = 12 + \\f{N/2 − 18}{12}·6 = 14.', '\\f{N}{2} − 18 = 4 → N = 44.'], 'stat', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'prob', 'One die has two faces marked 1, two faces marked 2, one face marked 3 and one face marked 4. Another die has one face marked 1, two faces marked 2, two faces marked 3 and one face marked 4. The probability of getting the sum of numbers to be 4 or 5, when both the dice are thrown together, is', ['\\f{2}{3}', '\\f{4}{9}', '\\f{1}{2}', '\\f{3}{5}'], 3,
    lambda: P4([F(2, 3), F(4, 9), F(1, 2), F(3, 5)], F(sum(1 for a in (1, 1, 2, 2, 3, 4) for b in (1, 2, 2, 3, 3, 4) if a + b in (4, 5)), 36)),
    ['List all 36 face pairs.', 'Sum 4: (1, 3)×4, (2, 2)×4, (3, 1)×1 = 9; sum 5: (1, 4)×2, (2, 3)×4, (3, 2)×2, (4, 1)×1 = 9.', '\\f{18}{36} = \\f{1}{2}.'], 'prob', 1)

# ---------- sheet 8
def _sq62():
    cells = [(r, c) for r in range(4) for c in range(4)]; pr = list(itertools.combinations(cells, 2))
    return P4([F(23, 30), F(4, 5), F(3, 5), F(7, 10)], F(sum(1 for a, b in pr if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1), len(pr)))
add(('2025', 'Jan', '2025-01-23', 2), 'prob', 'A board has 16 squares arranged in a 4 × 4 grid. Out of these 16 squares, two squares are chosen at random. The probability that they have no side in common is:', ['\\f{23}{30}', '\\f{4}{5}', '\\f{3}{5}', '\\f{7}{10}'], 2,
    _sq62, ['Pairs: C(16, 2) = 120. Pairs sharing a side: 4 rows × 3 + 4 columns × 3 = 24.', 'P = 1 − \\f{24}{120} = \\f{4}{5}.'], 'prob', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'stat', 'The variance of the numbers 8, 21, 34, 47, …, 320 is ______.', None, 8788,
    lambda: int(var(list(range(8, 321, 13)))), ['An A.P. with d = 13 and n = \\f{320 − 8}{13} + 1 = 25 terms.', 'Variance of an A.P. = \\f{d^{2}(n^{2} − 1)}{12} = \\f{169·624}{12} = 8788.'], 'stat', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'stat', 'For a statistical data x_{1}, x_{2}, …, x_{10} of 10 values, a student obtained the mean as 5.5 and Σx_{i}^{2} = 371. He later found that he had noted two values in the data incorrectly as 4 and 5, instead of the correct values 6 and 8, respectively. The variance of the corrected data is', ['5', '7', '9', '4'], 2,
    lambda: (lambda S, Q: P4([5, 7, 9, 4], F(Q, 10) - F(S, 10) ** 2))(55 - 4 - 5 + 6 + 8, 371 - 16 - 25 + 36 + 64),
    ['Σx = 55 − 9 + 14 = 60 → mean 6; Σx^{2} = 371 − 41 + 100 = 430.', 'Variance = 43 − 36 = 7.'], 'stat', 1)
def _ab65():
    pA = F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 5), 36); pB = F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8), 36)
    win, carry = F(0), F(1)
    for _ in range(400): win += carry * pA; carry *= (1 - pA) * (1 - pB)   # partial sums of the geometric series, exact
    return P4([F(8, 19), F(9, 19), F(8, 17), F(9, 17)], win, 1e-12)
add(('2025', 'Jan', '2025-01-24', 1), 'prob', 'A and B alternately throw a pair of dice. A wins if he throws a sum of 5 before B throws a sum of 8, and B wins if he throws a sum of 8 before A throws a sum of 5. The probability, that A wins if A makes the first throw, is', ['\\f{8}{19}', '\\f{9}{19}', '\\f{8}{17}', '\\f{9}{17}'], 2,
    _ab65, ['P(A gets 5) = \\f{4}{36} = \\f{1}{9}; P(B gets 8) = \\f{5}{36}.', 'P(A wins) = \\f{1}{9}[1 + r + r^{2} + …] with r = \\f{8}{9}·\\f{31}{36} = \\f{62}{81}.', '= \\f{1/9}{19/81} = \\f{9}{19}.'], 'prob', 2)
def _i67():
    pw = [1, 1j, -1, -1j]; return P4([F(1, 4), F(3, 4), F(2, 3), F(1, 2)], F(sum(1 for a in range(4) for b in range(4) if abs(pw[a] + pw[b]) > 1e-12), 16))
add(('2025', 'Jan', '2025-01-28', 1), 'prob', 'Two numbers k_{1} and k_{2} are randomly chosen from the set of natural numbers. Then, the probability that the value of i^{k_{1}} + i^{k_{2}}, (i = √{−1}) is non-zero, equals', ['\\f{1}{4}', '\\f{3}{4}', '\\f{2}{3}', '\\f{1}{2}'], 2,
    _i67, ['Only k mod 4 matters, each remainder equally likely.', 'The sum is zero when the powers are opposite: (0, 2), (2, 0), (1, 3), (3, 1) → 4 of 16.', 'P(non-zero) = \\f{3}{4}.'], 'prob', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'dist', 'Three defective oranges are accidently mixed with seven good ones and on looking at them, it is not possible to differentiate between them. Two oranges are drawn at random from the lot. If x denote the number of defective oranges, then the variance of x is', ['\\f{28}{75}', '\\f{14}{25}', '\\f{18}{25}', '\\f{26}{75}'], 1,
    lambda: P4([F(28, 75), F(14, 25), F(18, 25), F(26, 75)], _hv(10, 3, 2)),
    ['P(x = 0, 1, 2) = \\f{21}{45}, \\f{21}{45}, \\f{3}{45}.', 'E(x) = \\f{3}{5}, E(x^{2}) = \\f{11}{15}; variance = \\f{11}{15} − \\f{9}{25} = \\f{28}{75}.'], 'dist', 1)

# ---------- sheet 9
add(('2025', 'Jan', '2025-01-28', 2), 'cond', 'Bag B_{1} contains 6 white and 4 blue balls, Bag B_{2} contains 4 white and 6 blue balls, and Bag B_{3} contains 5 white and 5 blue balls. One of the bags is selected at random and a ball is drawn from it. If the ball is white, then the probability, that the ball is drawn from Bag B_{2}, is', ['\\f{1}{3}', '\\f{2}{5}', '\\f{2}{3}', '\\f{4}{15}'], 4,
    lambda: P4([F(1, 3), F(2, 5), F(2, 3), F(4, 15)], F(4, 10) / (F(6, 10) + F(4, 10) + F(5, 10))),
    ['Equal bags of 10, equally likely: P(B_{2} | white) = \\f{4}{6 + 4 + 5} = \\f{4}{15}.'], 'cond', 1)
def _b71():
    out = set()
    for beta in [F(k, 4) for k in range(9, 200)]:
        # any 10 values with Σx = 50 and variance 4/5: Σ(x − β)² = Σ(x − 5)² + 10(5 − β)²
        if 8 + 10 * (5 - beta) ** 2 == 98:
            xs = [7, 3] + [5] * 8; assert sum(xs) == 50 and var(xs) == F(4, 5)
            ys = [2 * (x - 1) + 4 * beta for x in xs]; out.add(beta * mean(ys) / var(ys))
    assert len(out) == 1; return P4([110, 90, 120, 100], out.pop())
add(('2025', 'Jan', '2025-01-29', 1), 'stat', 'Let x_{1}, x_{2}, …, x_{10} be ten observations such that Σ(x_{i} − 2) = 30, Σ(x_{i} − β)^{2} = 98, β > 2, and their variance is \\f{4}{5}. If μ and σ^{2} are respectively the mean and the variance of 2(x_{1} − 1) + 4β, 2(x_{2} − 1) + 4β, …, 2(x_{10} − 1) + 4β, then \\f{βμ}{σ^{2}} is equal to :', ['110', '90', '120', '100'], 4,
    _b71, ['Σx = 50 → mean 5; Σ(x − 5)^{2} = 10·\\f{4}{5} = 8.', 'Σ(x − β)^{2} = 8 + 10(5 − β)^{2} = 98 → β = 8 (β > 2).', 'μ = 2·5 − 2 + 32 = 40, σ^{2} = 4·\\f{4}{5} = \\f{16}{5} → \\f{8·40}{16/5} = 100.'], 'stat', 2)
def _n74():
    for n in range(1, 100):
        if F(4, 9) * F(n + 1, n + 4) + F(5, 9) * F(n, n + 4) == F(29, 45): return P4([6, 4, 5, 3], n)
add(('2025', 'Jan', '2025-01-29', 2), 'cond', 'Bag 1 contains 4 white balls and 5 black balls, and Bag 2 contains n white balls and 3 black balls. One ball is drawn randomly from Bag 1 and transferred to Bag 2. A ball is then drawn randomly from Bag 2. If the probability, that the ball drawn is white, is \\f{29}{45}, then n is equal to :', ['6', '4', '5', '3'], 1,
    _n74, ['P(W) = \\f{4}{9}·\\f{n + 1}{n + 4} + \\f{5}{9}·\\f{n}{n + 4} = \\f{9n + 4}{9(n + 4)}.', '\\f{9n + 4}{9(n + 4)} = \\f{29}{45} → 16n = 96 → n = 6.'], 'cond', 1)
def _a76():
    out = set()
    for b2 in range(0, 161):
        b = F(b2, 2); a = 80 - b
        if a > b >= 0:
            xs = sorted([21, 8, 17, a, 51, 103, b, 13, 67])
            if mean(xs) == 40 and xs[4] == 21 and sum(abs(x - 21) for x in xs) / 9 == 26: out.add(2 * a)
    assert len(out) == 1; return P4([109, 117, 161, 131], out.pop())
add(('2026', 'Apr', '2026-04-04', 1), 'stat', 'Suppose that the mean and median of the non-negative numbers 21, 8, 17, a, 51, 103, b, 13, 67, (a > b), are 40 and 21, respectively. If the mean deviation about the median is 26, then 2a is equal to:', ['109', '117', '161', '131'], 4,
    _a76, ['Sum 360 → a + b = 80.', 'Σ|x − 21| = 234; the known numbers give 183, so |a − 21| + |b − 21| = 51.', 'With b < 21 < a: a − b = 51 → a = 65.5 (median stays 21) → 2a = 131.'], 'stat', 2)
def _c78():
    good = sum(1 for s in itertools.product((0, 1), repeat=8) if sum(s[:6]) == 4 and sum(s[3:]) == 3); return int(96 * F(good, 256))
add(('2026', 'Apr', '2026-04-04', 1), 'prob', 'A coin is tossed 8 times. If the probability that exactly 4 heads appear in the first six tosses and exactly 3 heads appear in the last five tosses is p, then 96p is equal to ______.', None, 9,
    _c78, ['Tosses 4–6 are shared. Let k heads be among them: first three need 4 − k, last two need 3 − k.', 'Count Σ_{k} C(3, 4 − k)C(3, k)C(2, 3 − k): k = 1: 1·3·1 = 3; k = 2: 3·3·2 = 18; k = 3: 3·1·1 = 3 → 24.', 'p = \\f{24}{256} → 96p = 9.'], 'prob', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'prob', 'Two distinct numbers a and b are selected at random from 1, 2, 3, …, 50. The probability, that their product ab is divisible by 3, is', ['\\f{561}{1225}', '\\f{664}{1225}', '\\f{272}{1225}', '\\f{8}{25}'], 2,
    lambda: P4([F(561, 1225), F(664, 1225), F(272, 1225), F(8, 25)], F(sum(1 for a, b in itertools.combinations(range(1, 51), 2) if a * b % 3 == 0), comb(50, 2))),
    ['ab is not divisible by 3 only if neither is: 34 such numbers → C(34, 2) = 561 pairs.', 'P = 1 − \\f{561}{1225} = \\f{664}{1225}.'], 'prob', 1)

# ---------- sheet 10
def _k80():
    for j in range(1, 1000):
        k = F(j, 1000); ps = [0, 2 * k, k, 3 * k, 2 * k * k, 2 * k, k * k + k, 7 * k * k]
        if sum(ps) == 1: return P4([F(34, 100), F(22, 100), F(64, 100), F(33, 100)], ps[4] + ps[5] + ps[6])
add(('2026', 'Jan', '2026-01-22', 1), 'dist', 'If a random variable x has the probability distribution x = 0, 1, 2, 3, 4, 5, 6, 7 with P(x) = 0, 2k, k, 3k, 2k^{2}, 2k, k^{2} + k, 7k^{2}, then P(3 < x ≤ 6) is equal to', ['0.34', '0.22', '0.64', '0.33'], 4,
    _k80, ['Total: 10k^{2} + 9k = 1 → k = \\f{1}{10}.', 'P(4) + P(5) + P(6) = 3k^{2} + 3k = 0.03 + 0.3 = 0.33.'], 'dist', 1)
def _ap81():
    v = F(sum(1 for a, b, c in itertools.combinations(range(1, 32), 3) if b - a == c - b), comb(31, 3)); return v.numerator + v.denominator
add(('2026', 'Apr', '2026-04-04', 2), 'prob', 'From a month of 31 days, 3 different dates are selected at random. If the probability that these dates are in an increasing A.P. is equal to \\f{a}{b}, where a, b ∈ ℕ and gcd(a, b) = 1, then a + b is equal to ______.', None, 944,
    _ap81, ['Common difference d = 1, …, 15 gives 31 − 2d triples: total Σ(31 − 2d) = 465 − 240 = 225.', 'C(31, 3) = 4495 → \\f{225}{4495} = \\f{45}{899}.', 'a + b = 944.'], 'prob', 2)
def _k82():
    base = list(range(1, 1001)); med = F(500 + 501, 2); md1 = sum(abs(x - med) for x in base) / 1000   # mean deviation for k = 1
    k = F(500) / md1; return P4([4, 9, 1, 16], k * k)
add(('2026', 'Jan', '2026-01-22', 2), 'stat', 'If the mean deviation about the median of the numbers k, 2k, 3k, …, 1000k is 500, then k^{2} is equal to :', ['4', '9', '1', '16'], 1,
    _k82, ['Median = 500.5k; for k = 1 the deviations of 1, …, 1000 from 500.5 add to 2(0.5 + 1.5 + … + 499.5) = 250000.', 'Mean deviation = \\f{250000}{1000}|k| = 250|k| = 500 → |k| = 2.', 'k^{2} = 4.'], 'stat', 2)
def _n83():
    det = lambda m: m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    g = [n for n in range(1, 7) if det([[1, -n, 1], [1, n - 2, n + 1], [0, n - 1, 1]]) != 0]; return P4([21, 20, 22, 24], len(g) + sum(g))
add(('2026', 'Jan', '2026-01-22', 2), 'prob', 'Let n be the number obtained on rolling a fair die. If the probability that the system x − ny + z = 6, x + (n − 2)y + (n + 1)z = 8, (n − 1)y + z = 1 has a unique solution is \\f{k}{6}, then the sum of k and all possible values of n is :', ['21', '20', '22', '24'], 3,
    _n83, ['Unique solution ⇔ determinant ≠ 0. R_{2} − R_{1}: (0, 2n − 2, n); with row (0, n − 1, 1): det = (2n − 2) − n(n − 1) = −(n − 1)(n − 2).', 'Non-zero for n = 3, 4, 5, 6 → k = 4.', 'Sum = 4 + 18 = 22.'], 'prob', 2)
def _an84():
    pk = F(sum(1 for i in range(5) if 'KANPUR'[i:i + 2] == 'AN'), 5); pa = F(sum(1 for i in range(7) if 'ANANTPUR'[i:i + 2] == 'AN'), 7)
    return P4([F(7, 10), F(10, 17), F(12, 19), F(7, 19)], pa / (pa + pk))
add(('2026', 'Apr', '2026-04-05', 1), 'cond', 'A letter is known to have arrived by post either from KANPUR or from ANANTPUR. On the envelope just two consecutive letters AN are visible. The probability, that the letter came from ANANTPUR, is:', ['\\f{7}{10}', '\\f{10}{17}', '\\f{12}{19}', '\\f{7}{19}'], 2,
    _an84, ['KANPUR has 5 consecutive pairs, one AN: \\f{1}{5}. ANANTPUR has 7 pairs, two AN: \\f{2}{7}.', 'P = \\f{2/7}{2/7 + 1/5} = \\f{10}{17}.'], 'cond', 2)
def _md85():
    data = [5] * 8 + [7] * 6 + [9] * 2 + [10] * 2 + [12] * 2 + [15] * 6; m = mean(data); return P4([F(40, 13), F(42, 13), F(44, 13), F(46, 13)], sum(abs(x - m) for x in data) / len(data))
add(('2026', 'Apr', '2026-04-05', 1), 'stat', 'The mean deviation about the mean for the data x_{i}: 5, 7, 9, 10, 12, 15 with f_{i}: 8, 6, 2, 2, 2, 6 is equal to:', ['\\f{40}{13}', '\\f{42}{13}', '\\f{44}{13}', '\\f{46}{13}'], 3,
    _md85, ['N = 26, Σfx = 40 + 42 + 18 + 20 + 24 + 90 = 234 → mean 9.', 'Σf|x − 9| = 32 + 12 + 0 + 2 + 6 + 36 = 88.', '\\f{88}{26} = \\f{44}{13}.'], 'stat', 1)

# ---------- sheet 11
def _m86():
    out = set()
    for x in range(-30, 40):
        y = 19 - x; xs = [-10, -7, -1, x, y, 9, 2, 16]
        if x <= y and mean(xs) == F(7, 2) and var(xs) == F(293, 4): out.add(mean([x, y, x + y + 1, abs(x - y)]))
    assert len(out) == 1; return P4([11, 9, 10, 12], out.pop())
add(('2026', 'Jan', '2026-01-23', 1), 'stat', 'Let the mean and variance of 8 numbers −10, −7, −1, x, y, 9, 2, 16 be \\f{7}{2} and \\f{293}{4}, respectively. Then the mean of 4 numbers x, y, x + y + 1, |x − y| is :', ['11', '9', '10', '12'], 1,
    _m86, ['Sum 28 → x + y = 19. Σx^{2} = 8(\\f{293}{4} + \\f{49}{4}) = 684 → x^{2} + y^{2} = 193 → xy = 84 → {x, y} = {7, 12}.', 'Numbers: 7, 12, 20, 5 → mean 11.'], 'stat', 2)
def _ab88():
    pr = list(itertools.permutations(range(1, 101), 2)); v = F(sum(1 for a, b in pr if a - b >= 10), len(pr)); return v.numerator + v.denominator
add(('2026', 'Jan', '2026-01-23', 1), 'prob', 'From the first 100 natural numbers, two numbers first a and then b are selected randomly without replacement. If the probability that a − b ≥ 10 is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to ______.', None, 311,
    _ab88, ['Ordered pairs: 100·99 = 9900.', 'For b = 1, …, 90, a can be b + 10, …, 100: 91 − b choices → 1 + 2 + … + 90 = 4095.', '\\f{4095}{9900} = \\f{91}{220} → 311.'], 'prob', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'cond', 'The probabilities that players A and B of a team are selected for the captaincy for a tournament are 0.6 and 0.4, respectively. If A is selected the captain, the probability that the team wins the tournament is 0.8 and if B is selected the captain, the probability that the team wins the tournament is 0.7. Then the probability, that the team wins the tournament, is :', ['0.74', '0.76', '0.72', '0.78'], 2,
    lambda: P4([F(74, 100), F(76, 100), F(72, 100), F(78, 100)], F(6, 10) * F(8, 10) + F(4, 10) * F(7, 10)),
    ['Total probability: 0.6 × 0.8 + 0.4 × 0.7 = 0.48 + 0.28 = 0.76.'], 'cond', 1)
def _med93():
    for n in range(2, 30):
        tot = 2 ** n
        if F(sum(comb(n, i) * i * (i - 1) for i in range(n + 1)), tot) == 60:
            cum, vals = 0, []
            for i in range(n + 1):
                cum += comb(n, i); vals.append((cum, i * (i - 1)))
            pos = lambda k: next(v for c, v in vals if c >= k); return P4([56, 42, 72, 90], F(pos(tot // 2) + pos(tot // 2 + 1), 2))
add(('2026', 'Apr', '2026-04-05', 2), 'stat', 'A variable X takes values 0, 0, 2, 6, 12, 20, …, n(n − 1) with frequencies ^{n}C_{0}, ^{n}C_{1}, ^{n}C_{2}, ^{n}C_{3}, ^{n}C_{4}, ^{n}C_{5}, …, ^{n}C_{n}, respectively. If the mean of this data is 60, then its median is :', ['56', '42', '72', '90'], 1,
    _med93, ['Value i(i − 1) has frequency C(n, i). ΣC(n, i)i(i − 1) = n(n − 1)2^{n−2}, total 2^{n} → mean \\f{n(n − 1)}{4} = 60 → n = 16.', 'The middle of 2^{16} observations falls in the i = 8 block (the symmetric centre of C(16, i)).', 'Median = 8·7 = 56.'], 'stat', 3)
def _w94():
    v = F(6, 10) * F(10, 18) + F(4, 10) * F(9, 18); return P4([22, 23, 24, 21], v.numerator + v.denominator)
add(('2026', 'Jan', '2026-01-23', 2), 'cond', 'Bag A contains 9 white and 8 black balls, while bag B contains 6 white and 4 black balls. One ball is randomly picked up from the bag B and mixed up with the balls in the bag A. Then a ball is randomly drawn from the bag A. If the probability, that the ball drawn is white, is \\f{p}{q}, gcd(p, q) = 1, then p + q is equal to', ['22', '23', '24', '21'], 2,
    _w94, ['Transferred white (0.6): A has 10 W of 18; transferred black (0.4): 9 W of 18.', 'P(W) = 0.6·\\f{10}{18} + 0.4·\\f{9}{18} = \\f{9.6}{18} = \\f{8}{15} → 23.'], 'cond', 1)
def _lm95():
    out = set()
    for lam in range(0, 100):
        xs = [6] * 3 + [10] * lam + [14] * 4 + [18] * 7
        if var(xs) == 19: out.add(lam + mean(xs))
    assert len(out) == 1; return P4([18, 21, 20, 19], out.pop())
add(('2026', 'Jan', '2026-01-23', 2), 'stat', 'If the mean and the variance of the data with classes 4–8, 8–12, 12–16, 16–20 and frequencies 3, λ, 4, 7 are μ and 19 respectively, then the value of λ + μ is', ['18', '21', '20', '19'], 4,
    _lm95, ['Use mid-points 6, 10, 14, 18. Variance as a function of λ: \\f{Σfx^{2}}{N} − (\\f{Σfx}{N})^{2} = 19.', 'λ = 6: N = 20, Σfx = 18 + 60 + 56 + 126 = 260 → μ = 13; Σfx^{2} = 108 + 600 + 784 + 2268 = 3760 → 188 − 169 = 19 ✓.', 'λ + μ = 19.'], 'stat', 2)

# ---------- sheet 12
def _r97():
    S = F(2500 - 100, 20); Q = 100 + 10 * S - 500   # Σ(x+5)² − Σ(x−5)² = 20Σx ; Σ(x−5)² = Σx² − 10Σx + 500
    m = S / 20; v = Q / 20 - m * m; sd = F(math.isqrt(v.numerator), math.isqrt(v.denominator)); assert sd * sd == v
    r = m / sd; return P4([2, 3, F(3, 2), 4], r)
add(('2026', 'Apr', '2026-04-06', 1), 'stat', 'A data consists of 20 observations x_{1}, x_{2}, …, x_{20}. If Σ(x_{i} + 5)^{2} = 2500 and Σ(x_{i} − 5)^{2} = 100, then the ratio of mean to standard deviation of this data is:', ['2 : 1', '3 : 1', '3 : 2', '4 : 1'], 2,
    _r97, ['Subtract: 20Σx = 2400 → Σx = 120, mean 6.', 'Σ(x − 5)^{2} = Σx^{2} − 1200 + 500 = 100 → Σx^{2} = 800; variance 40 − 36 = 4, SD 2.', 'Mean : SD = 6 : 2 = 3 : 1.'], 'stat', 2)
def _n98():
    for N in range(1, 100):
        if F(N, N + 1) * F(1, 2) + F(1, N + 1) == F(9, 16): return P4([5, 7, 8, 9], N)
add(('2026', 'Apr', '2026-04-06', 1), 'cond', 'A bag contains (N + 1) coins — N fair coins, and one coin with \'Head\' on both sides. A coin is selected at random and tossed. If the probability of getting \'Head\' is \\f{9}{16}, then N is equal to:', ['5', '7', '8', '9'], 2,
    _n98, ['P(H) = \\f{N}{N + 1}·\\f{1}{2} + \\f{1}{N + 1} = \\f{N + 2}{2(N + 1)}.', '\\f{N + 2}{2(N + 1)} = \\f{9}{16} → 16N + 32 = 18N + 18 → N = 7.'], 'cond', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'dist', 'From a lot containing 10 defective and 90 non-defective bulbs, 8 bulbs are selected one by one with replacement. Then the probability of getting at least 7 defective bulbs is', ['\\f{7}{10^{7}}', '\\f{81}{10^{8}}', '\\f{67}{10^{8}}', '\\f{73}{10^{8}}'], 4,
    lambda: P4([F(7, 10 ** 7), F(81, 10 ** 8), F(67, 10 ** 8), F(73, 10 ** 8)], sum(comb(8, k) * F(1, 10) ** k * F(9, 10) ** (8 - k) for k in (7, 8))),
    ['Binomial with n = 8, p = \\f{1}{10}.', 'P(7) + P(8) = 8·\\f{9}{10^{8}} + \\f{1}{10^{8}} = \\f{73}{10^{8}}.'], 'dist', 1)
def _ab100():
    S, Q = 100, 10 * (2 + 100); S2, Q2 = 101, 10 * (F(199, 100) + F(101, 10) ** 2)
    d, e = S2 - S, Q2 - Q   # β − α and β² − α²
    return P4([10, 15, 5, 20], e / d)
add(('2026', 'Jan', '2026-01-24', 1), 'stat', 'The mean and variance of a data of 10 observations are 10 and 2, respectively. If an observation α in this data is replaced by β, then the mean and variance become 10.1 and 1.99, respectively. Then α + β equals', ['10', '15', '5', '20'], 4,
    _ab100, ['Σx: 100 → 101, so β − α = 1.', 'Σx^{2}: 10(2 + 100) = 1020 → 10(1.99 + 102.01) = 1040, so β^{2} − α^{2} = 20.', 'α + β = \\f{20}{1} = 20.'], 'stat', 2)
def _q101():
    for a in range(0, 17):
        b = 16 - a; xs = [2, 4, a, 8, b, 12, 14]
        if a < b and mean(xs) == 8 and var(xs) == 16:
            r1, r2 = 3 * a + 2, 2 * b + 1; eq = [(35, 306), (41, 420), (45, 506), (37, 342)]; h = [i + 1 for i, (s, p) in enumerate(eq) if s == r1 + r2 and p == r1 * r2]; assert len(h) == 1; return h[0]
add(('2026', 'Apr', '2026-04-06', 2), 'stat', 'Let the mean and the variance of seven observations 2, 4, α, 8, β, 12, 14, α < β, be 8 and 16 respectively. Then the quadratic equation whose roots are 3α + 2 and 2β + 1 is :', ['x^{2} − 35x + 306 = 0', 'x^{2} − 41x + 420 = 0', 'x^{2} − 45x + 506 = 0', 'x^{2} − 37x + 342 = 0'], 2,
    _q101, ['α + β = 56 − 40 = 16; Σx^{2} = 7·80 = 560 → α^{2} + β^{2} = 136 → αβ = 60 → α = 6, β = 10.', 'Roots 20 and 21: sum 41, product 420.'], 'stat', 2)
def _bg102():
    p = F(1)
    for b in range(6, 0, -1): p *= F(b * b, comb(2 * b, 2))   # one blue and one green from b of each
    return P4([F(63, 925), F(17, 231), F(16, 231), F(64, 925)], p)
add(('2026', 'Apr', '2026-04-06', 2), 'prob', 'A bag contains 6 blue and 6 green balls. Pairs of balls are drawn without replacement until the bag is empty. The probability that each drawn pair consists of one blue and one green ball is:', ['\\f{63}{925}', '\\f{17}{231}', '\\f{16}{231}', '\\f{64}{925}'], 3,
    _bg102, ['With b of each colour left, P(one of each) = \\f{b·b}{C(2b, 2)} = \\f{b}{2b − 1}.', 'Product: \\f{6}{11}·\\f{5}{9}·\\f{4}{7}·\\f{3}{5}·\\f{2}{3}·1 = \\f{720}{10395} = \\f{16}{231}.'], 'prob', 2)

# ---------- sheet 13
def _b105():
    X = list(range(1, 20)); out = set()
    for a in [F(k, 2) for k in range(-40, 41) if k]:
        Y = [a * x for x in X]
        if var(Y) == 750: out.add(30 - mean(Y))   # b fixed by the mean 30
    return P4([20, 80, 100, 60], sum(out))
add(('2026', 'Jan', '2026-01-24', 2), 'stat', 'Let X = {x ∈ ℕ : 1 ≤ x ≤ 19} and for some a, b ∈ ℝ, Y = {ax + b : x ∈ X}. If the mean and variance of the elements of Y are 30 and 750, respectively, then the sum of all possible values of b is', ['20', '80', '100', '60'], 4,
    _b105, ['X has mean 10 and variance \\f{19^{2} − 1}{12} = 30.', 'Var(Y) = 30a^{2} = 750 → a = ±5; mean 10a + b = 30 → b = −20 or 80.', 'Sum = 60.'], 'stat', 2)
def _e106():
    subs = list(range(32)); good = sum(1 for A in subs for B in subs if A & B == 0); v = F(good, 32 * 32)
    for p in range(1, 20):
        for q in range(1, 30):
            if F(3 ** p, 2 ** q) == v: return p + q
add(('2026', 'Jan', '2026-01-24', 2), 'prob', 'Let S be a set of 5 elements and P(S) denote the power set of S. Let E be an event of choosing an ordered pair (A, B) from the set P(S) × P(S) such that A ∩ B = φ. If the probability of the event E is \\f{3^{p}}{2^{q}}, where p, q ∈ ℕ, then p + q is equal to ______.', None, 15,
    _e106, ['Each element is in A only, B only or neither (not both): 3^{5} favourable pairs out of 4^{5}.', '\\f{3^{5}}{2^{10}} → p + q = 15.'], 'prob', 1)
def _bus107():
    pr = [F(2, 5), F(1, 5), F(2, 5)]; late = [F(1, 5), F(1, 3), F(1, 4)]; tot = sum(p * l for p, l in zip(pr, late))
    return P4([F(11, 37), F(12, 37), F(13, 37), F(14, 37)], pr[0] * late[0] / tot)
add(('2026', 'Apr', '2026-04-08', 2), 'cond', 'A candidate has to go to the examination centre to appear in an examination. The candidate uses only one means of transportation for the entire distance out of bus, scooter and car. The probabilities of the candidate going by bus, scooter and car, respectively, are \\f{2}{5}, \\f{1}{5} and \\f{2}{5}. The probabilities that the candidate reaches late at the examination centre are \\f{1}{5}, \\f{1}{3} and \\f{1}{4} if the candidate uses bus, scooter and car, respectively. Given that the candidate reached late at the examination centre, the probability that the candidate travelled by bus is :', ['\\f{11}{37}', '\\f{12}{37}', '\\f{13}{37}', '\\f{14}{37}'], 2,
    _bus107, ['P(late) = \\f{2}{25} + \\f{1}{15} + \\f{1}{10} = \\f{12 + 10 + 15}{150} = \\f{37}{150}.', 'P(bus | late) = \\f{12/150}{37/150} = \\f{12}{37}.'], 'cond', 1)
def _cv108():
    xs = [1 - math.sqrt(13), 1 + math.sqrt(13)] * 2; ys = [2 - 1, 2 + 1] * 3   # any sets with the given mean/variance
    allv = xs + ys; m = sum(allv) / 10; return P4([5.96, 6.14, 6.04, 6.24], sum((v - m) ** 2 for v in allv) / 10, 1e-9)
add(('2026', 'Apr', '2026-04-08', 2), 'stat', 'A set of four observations has mean 1 and variance 13. Another set of six observations has mean 2 and variance 1. Then, the variance of all these 10 observations is equal to :', ['5.96', '6.14', '6.04', '6.24'], 3,
    _cv108, ['Σx^{2}: 4(13 + 1) = 56 and 6(1 + 4) = 30 → 86; Σx = 4 + 12 = 16.', 'Combined variance = \\f{86}{10} − 1.6^{2} = 8.6 − 2.56 = 6.04.'], 'stat', 1)
def _k112():
    like = [F(comb(10 - k, 3), comb(10, 3)) for k in range(11)]; return P4([F(7, 11), F(7, 55), F(7, 110), F(14, 55)], like[1] / sum(like))
add(('2026', 'Jan', '2026-01-28', 1), 'cond', 'A bag contains 10 balls out of which k are red and (10 − k) are black, where 0 ≤ k ≤ 10. If three balls are drawn at random without replacement and all of them are found to be black, then the probability that the bag contains 1 red and 9 black balls is:', ['\\f{7}{11}', '\\f{7}{55}', '\\f{7}{110}', '\\f{14}{55}'], 4,
    _k112, ['Each k equally likely; P(3 black | k) = \\f{C(10 − k, 3)}{C(10, 3)}.', 'Σ_{k}C(10 − k, 3) = C(11, 4) = 330.', 'P(k = 1 | 3 black) = \\f{C(9, 3)}{330} = \\f{84}{330} = \\f{14}{55}.'], 'cond', 2)

# ---------- sheet 14
def _md113():
    out = set()
    for x in range(0, 11):
        y = 10 - x; xs = sorted([2, 3, 5, 10, 11, 13, 15, 21, x, y])
        if x <= y and mean(xs) == 9 and var(xs) == F(342, 10):
            med = F(xs[4] + xs[5], 2); out.add(sum(abs(v - med) for v in xs) / 10)
    assert len(out) == 1; return P4([5, 4, 6, 7], out.pop())
add(('2026', 'Jan', '2026-01-28', 1), 'stat', 'The mean and variance of 10 observations are 9 and 34.2, respectively. If 8 of these observations are 2, 3, 5, 10, 11, 13, 15, 21, then the mean deviation about the median of all the 10 observations is', ['5', '4', '6', '7'], 1,
    _md113, ['Missing two: sum 90 − 80 = 10; Σx^{2} = 10(34.2 + 81) = 1152 → their squares add to 1152 − 1094 = 58 → 3 and 7.', 'Sorted: 2, 3, 3, 5, 7, 10, 11, 13, 15, 21 → median 8.5.', 'Σ|x − 8.5| = 50 → mean deviation 5.'], 'stat', 2)
for _p in P: _p['t'] = _p['fam']
