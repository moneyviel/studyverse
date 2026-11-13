"""Real JEE Main questions — Mathematics Unit 4: Permutations and Combinations. Our own solutions; chk re-solves each one
by brute force wherever the search is small — listing every word in dictionary order, every selection, every digit
string — and by an independent formula otherwise. Skipped: a probability-of-a-committee item (Statistics and
Probability unit) and a matrix-counting item already used in Matrices and Determinants."""
import itertools, math
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
C = math.comb
def words(s): return sorted(set(itertools.permutations(s)))
def rank(s): return words(s).index(tuple(s)) + 1
def nth(s, n): return ''.join(words(s)[n - 1])

# ---------------- arrangements: words, rank, rows and queues ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'arr', 'All five letter words are made using all the letters A, B, C, D, E and arranged as in an English dictionary with serial numbers. Let the word at serial number n be denoted by W_{n}. Let the probability P(W_{n}) of choosing the word W_{n} satisfy P(W_{n}) = 2P(W_{n−1}), n > 1. If P(CDBEA) = \\f{2^{α}}{2^{β} − 1}, α, β ∈ N, then α + β is equal to ____.', None, 183,
    lambda: (lambda r: (r - 1) + 120)(rank('CDBEA')), ['P(W_{n}) = 2^{n−1}P(W_{1}) and the 120 probabilities add to 1 → P(W_{1}) = \\f{1}{2^{120} − 1}.', 'Rank of CDBEA: 48 (A, B first) + 12 (CA, CB) + 2 (CDA) + 1 (CDBA) + 1 = 64 → P = \\f{2^{63}}{2^{120} − 1} → 63 + 120 = 183.'], 'arr', 3)
add(('2024', 'Apr', '2024-04-05', 2), 'arr', '60 words can be made using all the letters of the word BHBJO, with or without meaning. If these words are written as in a dictionary, then the 50^{th} word is :', ['OBBHJ', 'HBBJO', 'OBBJH', 'JBBOH'], 3,
    lambda: pick(['OBBHJ', 'HBBJO', 'OBBJH', 'JBBOH'], nth('BHBJO', 50)), ['Words starting B: 4! = 24, H: 12, J: 12 → 48 words before O.', 'Starting O, the remaining B, B, H, J in order: OBBHJ (49th), OBBJH (50th).'], 'arr', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'arr', 'If all the words with or without meaning made using all the letters of the word "NAGPUR" are arranged as in a dictionary, then the word at 315^{th} position in this arrangement is :', ['NRAGUP', 'NRAGPU', 'NRAPGU', 'NRAPUG'], 3,
    lambda: pick(['NRAGUP', 'NRAGPU', 'NRAPGU', 'NRAPUG'], nth('NAGPUR', 315)), ['Letters in order A, G, N, P, R, U. Words starting A or G: 2 × 120 = 240.', 'NA, NG, NP: 3 × 24 = 72 → 312. Then NRAGPU (313), NRAGUP (314), NRAPGU (315).'], 'arr', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'arr', 'If all the words with or without meaning made using all the letters of the word "KANPUR" are arranged as in a dictionary, then the word at 440^{th} position in this arrangement is :', ['PRNAUK', 'PRNAKU', 'PRKAUN', 'PRKANU'], 3,
    lambda: pick(['PRNAUK', 'PRNAKU', 'PRKAUN', 'PRKANU'], nth('KANPUR', 440)), ['Order A, K, N, P, R, U: words starting A, K, N → 360. PA, PK, PN: 3 × 24 = 72 → 432.', 'PRA… : 6 → 438. Then PRKANU (439), PRKAUN (440).'], 'arr', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'arr', 'The letters of the word "UDAYPUR" are written in all possible ways with or without meaning and these words are arranged as in a dictionary. The rank of the word "UDAYPUR" is', ['1580', '1578', '1579', '1581'], 1,
    lambda: pick([1580, 1578, 1579, 1581], rank('UDAYPUR')), ['Letters A, D, P, R, U, U, Y. Words starting A, D, P, R: 4 × \\f{6!}{2!} = 1440.', 'UA…: 5! = 120. UDAP…, UDAR…, UDAU…: 3 × 3! = 18. Then UDAYPRU, and UDAYPUR is next.', '1440 + 120 + 18 + 1 + 1 = 1580.'], 'arr', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'arr', 'The number of words, which can be formed using all the letters of the word "DAUGHTER", so that all the vowels never come together, is', ['35000', '34000', '36000', '37000'], 3,
    lambda: pick([35000, 34000, 36000, 37000], sum(1 for w in itertools.permutations('DAUGHTER') if not any(set(w[i:i + 3]) == set('AUE') for i in range(6)))), ['All words: 8! = 40320. Vowels A, U, E together: treat them as a block → 6! × 3! = 4320.', '40320 − 4320 = 36000.'], 'arr', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'arr', 'The number of ways, 5 boys and 4 girls can sit in a row so that either all the boys sit together or no two boys sit together, is ____.', None, 17280,
    lambda: sum(1 for b in itertools.combinations(range(9), 5) if b[-1] - b[0] == 4 or all(y - x > 1 for x, y in zip(b, b[1:]))) * 120 * 24,
    ['Boys as one block with the 4 girls: 5! × 5! = 14400.', 'No two boys together: girls 4! and boys in the 5 gaps 5! → 2880. The two cases cannot both happen → 17280.'], 'arr', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'arr', 'In a group of 3 girls and 4 boys, there are two boys B_{1} and B_{2}. The number of ways, in which these girls and boys can stand in a queue such that all the girls stand together, all the boys stand together, but B_{1} and B_{2} are not adjacent to each other, is :', ['120', '72', '144', '96'], 3,
    lambda: pick([120, 72, 144, 96], sum(1 for p in itertools.permutations(['g1', 'g2', 'g3', 'B1', 'B2', 'b3', 'b4']) if (lambda s: s in ('GGGBBBB', 'BBBBGGG'))(''.join('G' if x[0] == 'g' else 'B' for x in p)) and abs(p.index('B1') - p.index('B2')) > 1)),
    ['Girls block and boys block: 2 orders, girls inside 3! = 6.', 'Boys inside with B_{1}, B_{2} apart: 4! − 3! × 2 = 12 → 2 × 6 × 12 = 144.'], 'arr', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'arr', 'The number of ways, of forming a queue of 4 boys and 3 girls such that all the girls are not together, is:', ['5040', '3050', '3410', '4320'], 4,
    lambda: pick([5040, 3050, 3410, 4320], sum(1 for p in itertools.permutations(range(7)) if not any(set(p[i:i + 3]) == {4, 5, 6} for i in range(5)))), ['All queues: 7! = 5040. All three girls together: 5! × 3! = 720.', '5040 − 720 = 4320.'], 'arr', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'arr', 'Let S be the set of all the words that can be formed by arranging all the letters of the word GARDEN. From the set S, one word is selected at random. The probability that the selected word will NOT have vowels in alphabetical order is :', ['\\f{2}{3}', '\\f{1}{2}', '\\f{1}{4}', '\\f{1}{3}'], 2,
    lambda: pick([F(2, 3), F(1, 2), F(1, 4), F(1, 3)], F(sum(1 for w in itertools.permutations('GARDEN') if w.index('E') < w.index('A')), 720)), ['The two vowels A and E are equally likely to come in either order.', 'So half the words have E before A → \\f{1}{2}.'], 'arr', 1)
add(('2025', 'Jan', '2025-01-29', 1), 'arr', 'The number of 6-letter words, with or without meaning, that can be formed using the letters of the word MATHS such that any letter that appears in the word must appear at least twice, is ____.', None, 1405,
    lambda: sum(1 for w in itertools.product('MATHS', repeat=6) if all(w.count(c) != 1 for c in set(w))),
    ['Split 6 into parts ≥ 2: 6, 4 + 2, 3 + 3, 2 + 2 + 2.', '5 + 5·4·15 + 10·20 + 10·90 = 5 + 300 + 200 + 900 = 1405.'], 'arr', 3)
add(('2026', 'Jan', '2026-01-23', 1), 'arr', 'The number of 4-letter words, with or without meaning, which can be formed using the letters PQRPQRSTUVP, is ____.', None, 1422,
    lambda: len(set(itertools.permutations('PQRPQRSTUVP', 4))),
    ['Available: P ×3, Q ×2, R ×2, S, T, U, V — 7 different letters.', 'All different: P(7, 4) = 840. One pair (P, Q or R) + 2 others: 3 · C(6, 2) · \\f{4!}{2!} = 540.', 'Two pairs: C(3, 2) · \\f{4!}{2!2!} = 18. P three times + 1 other: 6 · 4 = 24. Total 1422.'], 'arr', 3)
add(('2026', 'Apr', '2026-04-06', 1), 'arr', 'The number of 4-letter words, with or without meaning, each consisting of two vowels and two consonants that can be formed from the letters of the word INCONSEQUENTIAL, without repeating any letter, is:', ['2670', '2840', '2920', '3600'], 4,
    lambda: pick([2670, 2840, 2920, 3600], (lambda v, c: C(len(v), 2) * C(len(c), 2) * 24)({x for x in 'INCONSEQUENTIAL' if x in 'AEIOU'}, {x for x in 'INCONSEQUENTIAL' if x not in 'AEIOU'})),
    ['Different vowels: I, O, E, U, A (5); different consonants: N, C, S, Q, T, L (6).', 'C(5, 2) × C(6, 2) × 4! = 10 × 15 × 24 = 3600.'], 'arr', 2)

# ---------------- selections ----------------
add(('2024', 'Apr', '2024-04-04', 2), 'sel', 'There are 4 men and 5 women in Group A, and 5 men and 4 women in Group B. If 4 persons are selected from each group, then the number of ways of selecting 4 men and 4 women is ____.', None, 5626,
    lambda: sum(1 for a in itertools.combinations(range(9), 4) for b in itertools.combinations(range(9), 4) if sum(x < 4 for x in a) + sum(x < 5 for x in b) == 4),
    ['If k men come from A, then 4 − k women from A, 4 − k men and k women from B.', 'Σ[C(4, k)C(5, 4 − k)]^{2} = 25 + 1600 + 3600 + 400 + 1 = 5626.'], 'sel', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'sel', 'From a group of 7 batsmen and 6 bowlers, 10 players are to be chosen for a team, which should include atleast 4 batsmen and atleast 4 bowlers. One batsmen and one bowler who are captain and vice-captain respectively of the team should be included. Then the total number of ways such a selection can be made, is', ['135', '145', '155', '165'], 3,
    lambda: pick([135, 145, 155, 165], sum(1 for t in itertools.combinations(range(13), 10) if 0 in t and 7 in t and sum(x < 7 for x in t) >= 4 and sum(x >= 7 for x in t) >= 4)),
    ['Captain and vice-captain fixed: choose 8 more from 6 batsmen and 5 bowlers, at least 3 of each kind.', '(3, 5): 20 · 1, (4, 4): 15 · 5, (5, 3): 6 · 10 → 20 + 75 + 60 = 155.'], 'sel', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'sel', 'The number of ways five alphabets can be chosen from the alphabets of the word MATHEMATICS, where the chosen alphabets are not necessarily distinct, is equal to :', ['175', '181', '177', '179'], 4,
    lambda: pick([175, 181, 177, 179], len({tuple(sorted(c)) for c in itertools.combinations('MATHEMATICS', 5)})),
    ['Letters: M, A, T twice each; H, E, I, C, S once (8 kinds).', 'All different C(8, 5) = 56; one pair 3 · C(7, 3) = 105; two pairs 3 · 6 = 18 → 179.'], 'sel', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'sel', 'From all the English alphabets, five letters are chosen and are arranged in alphabetical order. The total number of ways, in which the middle letter is \'M\', is :', ['14950', '5148', '4356', '6084'], 2,
    lambda: pick([14950, 5148, 4356, 6084], sum(1 for c in itertools.combinations(range(26), 5) if c[2] == 12)), ['Two letters from the 12 before M and two from the 13 after it.', 'C(12, 2) × C(13, 2) = 66 × 78 = 5148.'], 'sel', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'sel', 'Group A consists of 7 boys and 3 girls, while group B consists of 6 boys and 5 girls. The number of ways, 4 boys and 4 girls can be invited for a picnic if 5 of them must be from group A and the remaining 3 from group B, is equal to :', ['9100', '8925', '8750', '8575'], 2,
    lambda: pick([9100, 8925, 8750, 8575], sum(C(7, b) * C(3, 5 - b) * C(6, 4 - b) * C(5, b - 1) for b in range(0, 6) if 0 <= 5 - b <= 3 and 0 <= 4 - b and b - 1 >= 0)),
    ['b boys from A means 5 − b girls from A, 4 − b boys and b − 1 girls from B.', 'b = 2: 21·1·15·5 = 1575; b = 3: 35·3·6·10 = 6300; b = 4: 35·3·1·10 = 1050 → 8925.'], 'sel', 3)
add(('2026', 'Apr', '2026-04-05', 2), 'sel', 'A box contains 5 blue, 6 yellow and 4 red balls. The number of ways, of drawing 8 balls containing at least two balls of each colour, is :', ['4100', '4140', '4230', '4290'], 1,
    lambda: pick([4100, 4140, 4230, 4290], sum(C(5, b) * C(6, y) * C(4, 8 - b - y) for b in range(2, 6) for y in range(2, 7) if 2 <= 8 - b - y <= 4)),
    ['List (blue, yellow, red) with each ≥ 2 and total 8.', 'Add C(5, b)C(6, y)C(4, r) over the 10 cases → 4100.'], 'sel', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'sel', 'Let p be the number of all triangles that can be formed by joining the vertices of a regular polygon P of n sides and q be the number of all quadrilaterals that can be formed by joining the vertices of P. If p + q = 126, then the eccentricity of the ellipse \\f{x^{2}}{16} + \\f{y^{2}}{n} = 1 is :', ['\\f{√{7}}{4}', '\\f{1}{2}', '\\f{1}{√{2}}', '\\f{3}{4}'], 3,
    lambda: (lambda n: pick([math.sqrt(7) / 4, 0.5, 1 / math.sqrt(2), 0.75], math.sqrt(1 - n / 16), 1e-9))(next(n for n in range(4, 30) if C(n, 3) + C(n, 4) == 126)),
    ['C(n, 3) + C(n, 4) = C(n + 1, 4) = 126 → n + 1 = 9, n = 8.', 'e = √{1 − \\f{8}{16}} = \\f{1}{√{2}}.'], 'sel', 2)

# ---------------- points and figures ----------------
add(('2025', 'Apr', '2025-04-03', 2), 'geo', 'Line L_{1} of slope 2 and line L_{2} of slope \\f{1}{2} intersect at the origin O. In the first quadrant, P_{1}, P_{2}, …, P_{12} are 12 points on line L_{1} and Q_{1}, Q_{2}, …, Q_{9} are 9 points on line L_{2}. Then the total number of triangles, that can be formed having vertices at three of the 22 points O, P_{1}, P_{2}, …, P_{12}, Q_{1}, Q_{2}, …, Q_{9}, is:', ['1134', '1188', '1080', '1026'], 1,
    lambda: (lambda pts: pick([1134, 1188, 1080, 1026], sum(1 for a, b, c in itertools.combinations(pts, 3) if (b[0] - a[0]) * (c[1] - a[1]) != (c[0] - a[0]) * (b[1] - a[1]))))([(0, 0)] + [(k, 2 * k) for k in range(1, 13)] + [(2 * k, k) for k in range(1, 10)]),
    ['O lies on both lines: 13 collinear points on L_{1}, 10 on L_{2}.', 'C(22, 3) − C(13, 3) − C(10, 3) = 1540 − 286 − 120 = 1134.'], 'geo', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'geo', 'There are 5 points P_{1}, P_{2}, P_{3}, P_{4}, P_{5} on the side AB, excluding A and B, of a triangle ABC. Similarly there are 6 points P_{6}, P_{7}, …, P_{11} on the side BC and 7 points P_{12}, P_{13}, …, P_{18} on the side CA of the triangle. The number of triangles, that can be formed using the points P_{1}, P_{2}, …, P_{18} as vertices, is :', ['776', '751', '796', '771'], 2,
    lambda: (lambda side: pick([776, 751, 796, 771], sum(1 for t in itertools.combinations(range(18), 3) if len({side(x) for x in t}) > 1)))(lambda x: 0 if x < 5 else 1 if x < 11 else 2),
    ['Any 3 of the 18 points, minus the triples lying on one side.', 'C(18, 3) − C(5, 3) − C(6, 3) − C(7, 3) = 816 − 10 − 20 − 35 = 751.'], 'geo', 1)
add(('2025', 'Apr', '2025-04-08', 2), 'geo', 'There are 12 points in a plane, no three of which are in the same straight line, except 5 points which are collinear. Then the total number of triangles that can be formed with the vertices at any three of these 12 points is', ['230', '200', '210', '220'], 3,
    lambda: pick([230, 200, 210, 220], sum(1 for t in itertools.combinations(range(12), 3) if not set(t) <= set(range(5)))), ['C(12, 3) counts 220 triples.', 'The C(5, 3) = 10 triples from the collinear points give no triangle → 210.'], 'geo', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'geo', 'Let ABC be a triangle. Consider four points p_{1}, p_{2}, p_{3}, p_{4} on the side AB, five points p_{5}, p_{6}, p_{7}, p_{8}, p_{9} on the side BC, and four points p_{10}, p_{11}, p_{12}, p_{13} on the side AC. None of these points is a vertex of the triangle ABC. Then the total number of pentagons, that can be formed by taking all the vertices from the points p_{1}, p_{2}, …, p_{13}, is ____.', None, 660,
    lambda: (lambda side: sum(1 for t in itertools.combinations(range(13), 5) if max([side(x) for x in t].count(s) for s in range(3)) <= 2))(lambda x: 0 if x < 4 else 1 if x < 9 else 2),
    ['A pentagon needs no three vertices on one line, so at most 2 points from each side: split 5 = 2 + 2 + 1.', 'Single point on AB: 4·10·6 = 240; on BC: 5·6·6 = 180; on AC: 240 → 660.'], 'geo', 3)

# ---------------- forming numbers ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'dig', 'If the number of seven-digit numbers, such that the sum of their digits is even, is m · n · 10^{n}; m, n ∈ {1, 2, 3, …, 9}, then m + n is equal to ____.', None, 14,
    lambda: (lambda N: next(m + n for m in range(1, 10) for n in range(1, 10) if m * n * 10 ** n == N))(9 * 10 ** 6 // 2 if sum(1 for x in range(10 ** 3, 10 ** 4) if sum(map(int, str(x))) % 2 == 0) * 2 == 9 * 10 ** 3 else None),
    ['Fix the first six digits; exactly 5 of the 10 last digits make the sum even.', '9 × 10^{5} × 5 = 45 × 10^{5} = 9 · 5 · 10^{5} → m = 9, n = 5 → 14.'], 'dig', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'dig', 'Let m and n, (m < n), be two 2-digit numbers. Then the total numbers of pairs (m, n), such that gcd(m, n) = 6, is ____.', None, 64,
    lambda: sum(1 for m in range(10, 100) for n in range(m + 1, 100) if math.gcd(m, n) == 6), ['m = 6a, n = 6b with gcd(a, b) = 1 and 2 ≤ a < b ≤ 16.', 'Count coprime pairs in 2…16: 64.'], 'dig', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'dig', 'The number of 3-digit numbers, formed using the digits 2, 3, 4, 5 and 7, when the repetition of digits is not allowed, and which are not divisible by 3, is equal to ____.', None, 36,
    lambda: sum(1 for p in itertools.permutations([2, 3, 4, 5, 7], 3) if sum(p) % 3), ['All: 5 · 4 · 3 = 60. Digit sets with sum divisible by 3: {2, 3, 4}, {2, 3, 7}, {3, 4, 5}, {3, 5, 7}.', '4 sets × 6 = 24 → 60 − 24 = 36.'], 'dig', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'dig', 'The number of 3-digit numbers, that are divisible by 2 and 3, but not divisible by 4 and 9, is ____.', None, 125,
    lambda: sum(1 for x in range(100, 1000) if x % 6 == 0 and x % 36), ['Divisible by 2 and 3 means a multiple of 6: 102 to 996 → 150 numbers.', 'The official answer reads "not divisible by 4 and 9" as not divisible by both, i.e. by 36: 25 multiples of 36 → 150 − 25 = 125.'], 'dig', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'dig', 'The number of different 5 digit numbers greater than 50000 that can be formed using the digits 0, 1, 2, 3, 4, 5, 6, 7, such that the sum of their first and last digits should not be more than 8, is', ['4608', '5719', '4607', '5720'], 3,
    lambda: pick([4608, 5719, 4607, 5720], sum(1 for a in range(5, 8) for e in range(8) if a + e <= 8) * 512 - 1), ['First digit 5, 6, 7 with last digit ≤ 3, ≤ 2, ≤ 1: 4 + 3 + 2 = 9 pairs, middle three digits 8^{3} = 512.', '9 × 512 = 4608, minus 50000 itself → 4607.'], 'dig', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'dig', 'Let P be the set of seven digit numbers with sum of their digits equal to 11. If the numbers in P are formed by using the digits 1, 2 and 3 only, then the number of elements in the set P is :', ['161', '164', '173', '158'], 1,
    lambda: pick([161, 164, 173, 158], sum(1 for d in itertools.product((1, 2, 3), repeat=7) if sum(d) == 11)), ['Seven digits each ≥ 1 add to 11: the extra 4 is shared as 2s (+1) and 3s (+2).', 'Four 2s: 35; two 2s and one 3: \\f{7!}{2!·4!·1!} = 105; two 3s: 21 → 161.'], 'dig', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'dig', 'Let S denote the set of 4-digit numbers abcd such that a > b > c > d and P denote the set of 5-digit numbers having product of its digits equal to 20. Then n(S) + n(P) is equal to ____.', None, 260,
    lambda: sum(1 for x in range(1000, 10000) if (lambda s: s[0] > s[1] > s[2] > s[3])(str(x))) + sum(1 for x in range(10000, 100000) if math.prod(map(int, str(x))) == 20),
    ['Any 4 different digits in falling order: C(10, 4) = 210.', '20 = 5·4·1·1·1 (20 ways) or 5·2·2·1·1 (30 ways) → 50; total 260.'], 'dig', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'dig', 'The number of numbers greater than 5000, less than 9000 and divisible by 3, that can be formed using the digits 0, 1, 2, 5, 9, if the repetition of the digits is allowed, is ____.', None, 42,
    lambda: sum(1 for x in range(5001, 9000) if x % 3 == 0 and set(str(x)) <= set('01259')), ['The first digit must be 5 (9 would give 9xxx ≥ 9000).', 'The other three digits (125 choices) must make the total a multiple of 3: 42 of them do.'], 'dig', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'dig', 'Let S = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Let x be the number of 9-digit numbers formed using the digits of the set S such that only one digit is repeated and it is repeated exactly twice. Let y be the number of 9-digit numbers formed using the digits of the set S such that only two digits are repeated and each of these is repeated exactly twice. Then,', ['29x = 5y', '45x = 7y', '21x = 4y', '56x = 9y'], 3,
    lambda: (lambda x, y: pick(['29x = 5y', '45x = 7y', '21x = 4y', '56x = 9y'], next(s for s, (a, b) in zip(['29x = 5y', '45x = 7y', '21x = 4y', '56x = 9y'], [(29, 5), (45, 7), (21, 4), (56, 9)]) if a * x == b * y)))(9 * C(8, 7) * math.factorial(9) // 2, C(9, 2) * C(7, 5) * math.factorial(9) // 4),
    ['x: the doubled digit (9) and 7 others from 8 (8 ways), arranged \\f{9!}{2!}.', 'y: two doubled digits C(9, 2) and 5 others C(7, 5), arranged \\f{9!}{2!2!} → \\f{x}{y} = \\f{36}{189} = \\f{4}{21}.'], 'dig', 3)

# ---------------- distributing and placing ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'dist', 'The number of ways, in which the letters A, B, C, D, E can be placed in the 8 boxes of the figure below so that no row remains empty and at most one letter can be placed in a box, is : (The figure has three rows of 3, 3 and 2 boxes.)', ['5880', '840', '960', '5760'], 4,
    lambda: pick([5880, 840, 960, 5760], sum(1 for s in itertools.combinations(range(8), 5) if {0 if b < 3 else 1 if b < 6 else 2 for b in s} == {0, 1, 2}) * 120),
    ['Choose 5 of the 8 boxes leaving no row empty: C(8, 5) − 1 − 1 − C(6, 5) = 56 − 8 = 48.', 'Place the 5 letters: 5! → 48 × 120 = 5760.'], 'dist', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'dist', 'The number of ways of getting a sum 16 on throwing a dice four times is ____.', None, 125,
    lambda: sum(1 for d in itertools.product(range(1, 7), repeat=4) if sum(d) == 16), ['Put d_{i} = 7 − e_{i}: e_{1} + … + e_{4} = 12 with 1 ≤ e_{i} ≤ 6.', 'C(11, 3) − 4C(5, 3) = 165 − 40 = 125.'], 'dist', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'dist', 'The number of seven-digit numbers, that can be formed by using the digits 1, 2, 3, 5 and 7 such that each digit is used at least once, is :', ['15400', '17800', '16800', '29400'], 3,
    lambda: pick([15400, 17800, 16800, 29400], sum(1 for d in itertools.product('12357', repeat=7) if len(set(d)) == 5)),
    ['Either one digit thrice (5 · \\f{7!}{3!} = 4200) or two digits twice (10 · \\f{7!}{2!2!} = 12600).', '4200 + 12600 = 16800.'], 'dist', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'dist', 'Three persons enter in a lift at the ground floor. The lift will go upto 10^{th} floor. The number of ways, in which the three persons can exit the lift at three different floors, if the lift does not stop at first, second and third floors, is equal to ____.', None, 210,
    lambda: sum(1 for f in itertools.product(range(4, 11), repeat=3) if len(set(f)) == 3), ['Usable floors: 4 to 10 — 7 floors.', 'Different floors for three people: 7 × 6 × 5 = 210.'], 'dist', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'dist', 'Two players A and B play a series of games of badminton. The player, who wins 5 games first, wins the series. Assuming that no game ends in a draw, the number of ways, in which player A wins the series is ____.', None, 126,
    lambda: sum(1 for n in range(5, 10) for s in itertools.product('AB', repeat=n) if s[-1] == 'A' and s.count('A') == 5 and s.count('B') == n - 5),
    ['A wins the last game; before it, A has 4 wins and B has k wins (k = 0 to 4) in any order.', 'Σ C(4 + k, k) = 1 + 5 + 15 + 35 + 70 = 126.'], 'dist', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'dist', 'The number of ways, in which 16 oranges can be distributed to four children such that each child gets at least one orange, is', ['429', '384', '403', '455'], 4,
    lambda: pick([429, 384, 403, 455], sum(1 for a in range(1, 14) for b in range(1, 14) for c in range(1, 14) if 1 <= 16 - a - b - c)), ['Identical oranges: x_{1} + x_{2} + x_{3} + x_{4} = 16 with each ≥ 1.', 'Stars and bars: C(15, 3) = 455.'], 'dist', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'dist', 'A building has ground floor and 10 more floors. Nine persons enter in a lift at the ground floor. The lift goes up to the 10^{th} floor. The number of ways, in which any 4 persons exit at a floor and the remaining 5 persons exit at a different floor, if the lift does not stop at the first and the second floors, is equal to :', ['2184', '3064', '7056', '11340'], 3,
    lambda: pick([2184, 3064, 7056, 11340], sum(1 for g in itertools.combinations(range(9), 4)) * sum(1 for a in range(3, 11) for b in range(3, 11) if a != b)),
    ['Choose the group of 4: C(9, 4) = 126; the other 5 leave together.', 'Two different floors from 3 to 10 for the two groups: 8 × 7 = 56 → 126 × 56 = 7056.'], 'dist', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'dist', 'A person has three different bags and four different books. The number of ways, in which he can put these books in the bags so that no bag is empty, is :', ['18', '36', '39', '72'], 2,
    lambda: pick([18, 36, 39, 72], sum(1 for f in itertools.product(range(3), repeat=4) if len(set(f)) == 3)), ['Every book goes in one of 3 bags: 3^{4} = 81; remove the cases with an empty bag.', '81 − 3 · 2^{4} + 3 · 1 = 36.'], 'dist', 1)
for _p in P: _p['t'] = _p['fam']
