"""Practice generators — Mathematics Unit 4: Permutations and Combinations. check() re-counts every item by brute force:
it lists the actual words, selections, digit strings and distributions and counts the ones that pass the condition."""
import itertools, math
from common import mcq
C = math.comb
def need(x):
    if not x: raise AssertionError('retry')
def words(s): return sorted(set(itertools.permutations(s)))
WORDS = ['GARDEN', 'MOTHER', 'PLANET', 'SUNDAY', 'FRIDAY', 'BRIGHT', 'CANDLE', 'MANGO', 'TIGER', 'HONEY', 'DELHI', 'AGRA', 'PUNE', 'NOIDA', 'BIHAR', 'KERALA', 'ASSAM', 'GOA', 'INDIA', 'APPLE',
         'BANANA', 'LETTER', 'COFFEE', 'PEPPER', 'RUPEE', 'MADAM', 'SCHOOL', 'JAIPUR', 'MUMBAI', 'BHOPAL', 'RANCHI', 'SHIMLA', 'MYSORE', 'NASHIK', 'SURAT', 'UDAIPUR', 'KANPUR', 'NAGPUR', 'PATNA', 'INDORE']
VOW = set('AEIOU')
def fmtw(t): return ''.join(t)

def g_arr(rng):
    t = rng.choice(['a_rank', 'a_nth', 'a_apart', 'a_rep', 'a_block', 'a_ends'])
    if t == 'a_rank':
        w = rng.choice([x for x in WORDS if 4 <= len(x) <= 7]); L = words(w); tgt = rng.choice(L); r = L.index(tgt) + 1
        return dict(q=f'All the words (with or without meaning) made from all the letters of "{w}" are arranged as in a dictionary. The rank of the word "{fmtw(tgt)}" is ____.', o=None, a=r,
                    sol=['Count the words that start with a smaller letter, then fix that letter and repeat for the next place.', f'Rank = {r}.'], p=dict(t=t, w=w, x=fmtw(tgt)))
    if t == 'a_nth':
        w = rng.choice([x for x in WORDS if 5 <= len(x) <= 7]); L = words(w); n = rng.randint(2, len(L) - 1); right = fmtw(L[n - 1])
        wr = [fmtw(L[k]) for k in (n, n - 2, n + 1, n - 3, 0) if 0 <= k < len(L)]
        o, a = mcq(rng, right, wr)
        return dict(q=f'The words made from all the letters of "{w}" are written in dictionary order. The word at position {n} is', o=o, a=a,
                    sol=['Count blocks of words by their first letter, then by the second letter, until you reach the position.', f'Position {n}: {right}.'], p=dict(t=t, w=w, n=n))
    if t == 'a_apart':
        w = rng.choice([x for x in WORDS if len(set(x)) == len(x) and 5 <= len(x) <= 8 and sum(c in VOW for c in x) >= 2]); k = sum(c in VOW for c in w); n = len(w)
        ask = rng.choice(['never', 'always']); tog = math.factorial(n - k + 1) * math.factorial(k); val = tog if ask == 'always' else math.factorial(n) - tog
        return dict(q=f'The number of words made from all the letters of "{w}" in which the vowels {"are always together" if ask == "always" else "never all come together"} is ____.', o=None, a=val,
                    sol=[f'Vowels as one block: ({n} − {k} + 1)! × {k}! = {tog}.', f'{"That is the answer" if ask == "always" else f"Subtract from {n}! = {math.factorial(n)}"} → {val}.'], p=dict(t=t, w=w, ask=ask))
    if t == 'a_rep':
        w = rng.choice(['BANANA', 'LETTER', 'COFFEE', 'PEPPER', 'ASSAM', 'APPLE', 'MADAM', 'SCHOOL', 'INDIA', 'RUPEE', 'MISSISSIPPI', 'BALLOON', 'COMMITTEE', 'ALLAHABAD']); r = rng.choice([3, 4])
        val = len(set(itertools.permutations(w, r)))
        return dict(q=f'The number of {r}-letter words (with or without meaning) that can be formed from the letters of "{w}" is ____.', o=None, a=val,
                    sol=['Split by pattern: all letters different, one letter twice, and so on — use only letters that occur often enough.', f'Total {val}.'], p=dict(t=t, w=w, r=r))
    if t == 'a_block':
        b, g = rng.randint(2, 5), rng.randint(2, 4); ask = rng.choice(['gt', 'gnt', 'alt', 'nobb'])
        F = math.factorial; val = {'gt': F(b + 1) * F(g), 'gnt': F(b + g) - F(b + 1) * F(g), 'alt': (2 if b == g else 1) * F(b) * F(g) if abs(b - g) <= 1 else 0, 'nobb': F(g) * math.perm(g + 1, b)}[ask]
        need(val)
        txt = {'gt': 'all the girls stand together', 'gnt': 'all the girls are not together', 'alt': 'boys and girls alternate', 'nobb': 'no two boys stand together'}[ask]
        return dict(q=f'{b} boys and {g} girls stand in a queue. The number of ways in which {txt} is ____.', o=None, a=val,
                    sol=['Treat a group that must stay together as one block; for "no two together", seat the others first and use the gaps.', f'→ {val}.'], p=dict(t=t, b=b, g=g, ask=ask))
    w = rng.choice([x for x in WORDS if len(set(x)) == len(x) and 5 <= len(x) <= 7]); ask = rng.choice(['vv', 'cc', 'vc'])
    n, k = len(w), sum(c in VOW for c in w); m = n - k; need(k >= 2 and m >= 2 if ask != 'vc' else k >= 1 and m >= 1)
    rest = math.factorial(n - 2); ends = {'vv': k * (k - 1), 'cc': m * (m - 1), 'vc': 2 * k * m}[ask]; val = ends * rest
    txt = {'vv': 'begin and end with a vowel', 'cc': 'begin and end with a consonant', 'vc': 'have one vowel and one consonant at the two ends'}[ask]
    return dict(q=f'The number of words made from all the letters of "{w}" that {txt} is ____.', o=None, a=val,
                sol=['Fill the two ends first, then arrange the rest in the middle.', f'{ends} × {n - 2}! = {val}.'], p=dict(t='a_ends', w=w, ask=ask))

def g_sel(rng):
    t = rng.choice(['s_grp', 's_atl', 's_multi', 's_mid', 's_team'])
    if t == 's_grp':
        m1, w1, m2, w2 = (rng.randint(3, 6) for _ in range(4)); k = rng.choice([2, 3]); M = rng.randint(1, 2 * k - 1)
        val = sum(C(m1, a) * C(w1, k - a) * C(m2, M - a) * C(w2, k - M + a) for a in range(0, k + 1) if 0 <= M - a <= k); need(val)
        return dict(q=f'Group A has {m1} men and {w1} women; group B has {m2} men and {w2} women. {k} persons are chosen from each group. The number of ways of getting exactly {M} men in all is ____.', o=None, a=val,
                    sol=['If a men come from A, then M − a men come from B; the rest are women.', f'Add over a → {val}.'], p=dict(t=t, g=[m1, w1, m2, w2], k=k, M=M))
    if t == 's_atl':
        cs = [rng.randint(3, 6) for _ in range(3)]; k = rng.choice([1, 2]); n = rng.randint(3 * k + 1, min(sum(cs) - 1, 3 * k + 5))
        val = sum(C(cs[0], a) * C(cs[1], b) * C(cs[2], n - a - b) for a in range(k, cs[0] + 1) for b in range(k, cs[1] + 1) if k <= n - a - b <= cs[2]); need(val)
        return dict(q=f'A box has {cs[0]} blue, {cs[1]} yellow and {cs[2]} red balls (all different). The number of ways of drawing {n} balls with at least {k} of each colour is ____.', o=None, a=val,
                    sol=['List the colour splits (b, y, r) allowed, then add C(·)·C(·)·C(·) for each.', f'→ {val}.'], p=dict(t=t, cs=cs, k=k, n=n))
    if t == 's_multi':
        w = rng.choice(['MATHEMATICS', 'STATISTICS', 'ASSASSINATION', 'EXAMINATION', 'COMMITTEE', 'BANANA', 'ALLAHABAD', 'MISSISSIPPI', 'PARALLEL', 'INDEPENDENCE']); r = rng.choice([3, 4, 5])
        val = len({tuple(sorted(c)) for c in itertools.combinations(w, r)}); need(val > 5)
        return dict(q=f'The number of ways of choosing {r} letters from the letters of the word {w} (letters may repeat as often as they appear; order does not matter) is ____.', o=None, a=val,
                    sol=['Split by pattern: all different, one pair, two pairs, a triple …, using only letters that occur enough times.', f'→ {val}.'], p=dict(t=t, w=w, r=r))
    if t == 's_mid':
        r = rng.choice([3, 5]); pos = rng.randint(r // 2 + 1, 26 - r // 2); L = chr(64 + pos)
        val = C(pos - 1, r // 2) * C(26 - pos, r // 2)
        return dict(q=f'{r} different letters of the English alphabet are chosen and written in alphabetical order. The number of ways in which the middle letter is \'{L}\' is ____.', o=None, a=val,
                    sol=[f'{r // 2} letters from the {pos - 1} before {L} and {r // 2} from the {26 - pos} after it.', f'C({pos - 1}, {r // 2}) × C({26 - pos}, {r // 2}) = {val}.'], p=dict(t=t, r=r, pos=pos))
    a, b = rng.randint(5, 8), rng.randint(4, 7); n = rng.randint(6, min(11, a + b - 1)); k = rng.randint(2, 4); need(2 * k <= n)
    val = sum(C(a, x) * C(b, n - x) for x in range(k, a + 1) if n - x >= k and n - x <= b); need(val)
    return dict(q=f'A team of {n} is chosen from {a} batsmen and {b} bowlers so that it has at least {k} batsmen and at least {k} bowlers. The number of ways is ____.', o=None, a=val,
                sol=['Add over the number x of batsmen allowed.', f'Σ C({a}, x)C({b}, {n} − x) = {val}.'], p=dict(t='s_team', a=a, b=b, n=n, k=k))

def g_geo(rng):
    t = rng.choice(['g_sides', 'g_coll', 'g_lines', 'g_poly', 'g_ngon'])
    if t == 'g_sides':
        s = [rng.randint(2, 7) for _ in range(3)]; ask = rng.choice(['tri', 'quad']); n = sum(s)
        val = C(n, 3) - sum(C(x, 3) for x in s) if ask == 'tri' else sum(1 for q in itertools.combinations(range(n), 4) if max(sum(1 for x in q if sum(s[:i]) <= x < sum(s[:i + 1])) for i in range(3)) <= 2)
        return dict(q=f'A triangle ABC has {s[0]} points on AB, {s[1]} on BC and {s[2]} on CA (none at a vertex). The number of {"triangles" if ask == "tri" else "quadrilaterals"} with vertices among these points is ____.', o=None, a=val,
                    sol=['Points on one side are collinear: a triangle needs them not all on one side; a quadrilateral needs at most 2 from each side.', f'→ {val}.'], p=dict(t=t, s=s, ask=ask))
    if t == 'g_coll':
        n, m = rng.randint(8, 15), rng.randint(3, 6); ask = rng.choice(['tri', 'lines']); need(m < n)
        val = C(n, 3) - C(m, 3) if ask == 'tri' else C(n, 2) - C(m, 2) + 1
        return dict(q=f'There are {n} points in a plane, no three collinear except {m} that lie on one line. The number of {"triangles" if ask == "tri" else "different straight lines through two of the points"} is ____.', o=None, a=val,
                    sol=[f'{"C(n, 3) − C(m, 3): the collinear triples give no triangle." if ask == "tri" else "C(n, 2) − C(m, 2) + 1: the collinear points give just one line."}', f'→ {val}.'], p=dict(t=t, n=n, m=m, ask=ask))
    if t == 'g_lines':
        p, q = rng.randint(4, 12), rng.randint(4, 12); val = C(p + q + 1, 3) - C(p + 1, 3) - C(q + 1, 3)
        return dict(q=f'Two lines meet at O. There are {p} points on the first line and {q} on the second (other than O). The number of triangles with vertices among these {p + q + 1} points (O included) is ____.', o=None, a=val,
                    sol=[f'O is on both lines: {p + 1} collinear points on one, {q + 1} on the other.', f'C({p + q + 1}, 3) − C({p + 1}, 3) − C({q + 1}, 3) = {val}.'], p=dict(t=t, p=p, q=q))
    if t == 'g_poly':
        s = [rng.randint(2, 5) for _ in range(3)]; n = sum(s)
        val = sum(1 for q in itertools.combinations(range(n), 5) if max(sum(1 for x in q if sum(s[:i]) <= x < sum(s[:i + 1])) for i in range(3)) <= 2); need(val)
        return dict(q=f'There are {s[0]}, {s[1]} and {s[2]} points on the three sides of a triangle (none at a vertex). The number of pentagons with all vertices among these points is ____.', o=None, a=val,
                    sol=['At most 2 vertices on any side: split 5 = 2 + 2 + 1.', f'→ {val}.'], p=dict(t=t, s=s))
    n = rng.randint(5, 20); ask = rng.choice(['diag', 'tri0', 'tri'])
    val = {'diag': n * (n - 3) // 2, 'tri0': C(n, 3) - n * (n - 4) - n, 'tri': C(n, 3)}[ask]; need(val > 0)
    txt = {'diag': 'diagonals', 'tri0': 'triangles (using its vertices) with no side common with the polygon', 'tri': 'triangles that can be formed using its vertices'}[ask]
    return dict(q=f'A convex polygon has {n} sides. The number of {txt} is ____.', o=None, a=val,
                sol=['Count pairs or triples of vertices, then remove the ones that do not qualify.', f'→ {val}.'], p=dict(t='g_ngon', n=n, ask=ask))

def g_dig(rng):
    t = rng.choice(['d_div3', 'd_sum', 'd_range', 'd_desc', 'd_mult'])
    if t == 'd_div3':
        ds = sorted(rng.sample(range(0, 10), rng.randint(5, 6))); k = rng.choice([3, 4]); ask = rng.choice(['is', 'not']); m = rng.choice([3, 5, 4])
        val = sum(1 for p in itertools.permutations(ds, k) if p[0] and ((int(''.join(map(str, p))) % m == 0) == (ask == 'is'))); need(val)
        return dict(q=f'The number of {k}-digit numbers formed from the digits {", ".join(map(str, ds))} without repetition that are {"" if ask == "is" else "not "}divisible by {m} is ____.', o=None, a=val,
                    sol=[f'Use the divisibility rule for {m} ({"digit sum" if m == 3 else "last digit" if m == 5 else "last two digits"}), and remember the first digit cannot be 0.', f'→ {val}.'], p=dict(t=t, ds=ds, k=k, ask=ask, m=m))
    if t == 'd_sum':
        ds = rng.choice([(1, 2), (1, 2, 3), (1, 3), (2, 3), (1, 2, 4)]); n = rng.randint(4, 7); s = rng.randint(n * min(ds) + 1, n * max(ds) - 1)
        val = sum(1 for d in itertools.product(ds, repeat=n) if sum(d) == s); need(val)
        return dict(q=f'The number of {n}-digit numbers using only the digits {", ".join(map(str, ds))} whose digits add up to {s} is ____.', o=None, a=val,
                    sol=['Find how many of each digit are needed, then arrange: \\f{n!}{a!b!…}.', f'→ {val}.'], p=dict(t=t, ds=list(ds), n=n, s=s))
    if t == 'd_range':
        ds = sorted(rng.sample(range(0, 10), 5)); lo = rng.choice([1000, 2000, 3000, 5000]); hi = lo + rng.choice([2000, 3000, 4000]); m = rng.choice([3, 4, 5, 6])
        val = sum(1 for x in range(lo + 1, hi) if x % m == 0 and set(str(x)) <= set(map(str, ds))); need(val)
        return dict(q=f'The number of numbers greater than {lo} and less than {hi}, divisible by {m}, that can be formed from the digits {", ".join(map(str, ds))} (repetition allowed) is ____.', o=None, a=val,
                    sol=['Fix the allowed first digits, then count the endings that make the number divisible.', f'→ {val}.'], p=dict(t=t, ds=ds, lo=lo, hi=hi, m=m))
    if t == 'd_desc':
        k = rng.randint(2, 5); ask = rng.choice(['dec', 'inc'])
        val = C(10, k) if ask == 'dec' else C(9, k)
        return dict(q=f'The number of {k}-digit numbers whose digits are strictly {"decreasing" if ask == "dec" else "increasing"} from left to right is ____.', o=None, a=val,
                    sol=['Any set of different digits can be written in exactly one such order.', f'{"0 may be used (it lands last): C(10, k)" if ask == "dec" else "0 cannot be used (it would come first): C(9, k)"} = {val}.'], p=dict(t=t, k=k, ask=ask))
    a, b = rng.choice([(6, 4), (6, 9), (4, 6), (5, 3), (3, 5), (8, 3), (9, 4), (12, 8), (15, 4)]); k = rng.choice([3, 4])
    val = sum(1 for x in range(10 ** (k - 1), 10 ** k) if x % a == 0 and x % b)
    return dict(q=f'The number of {k}-digit numbers divisible by {a} but not by {b} is ____.', o=None, a=val,
                sol=[f'Multiples of {a} minus multiples of lcm({a}, {b}) = {a * b // math.gcd(a, b)}.', f'→ {val}.'], p=dict(t='d_mult', a=a, b=b, k=k))

def g_dist(rng):
    t = rng.choice(['t_stars', 't_onto', 't_lift', 't_dice', 't_series'])
    if t == 't_stars':
        k = rng.randint(3, 4); m = rng.randint(0, 2); n = rng.randint(k * m + 2, k * m + 14)
        val = C(n - k * m + k - 1, k - 1)
        return dict(q=f'{n} identical sweets are shared among {k} children so that each child gets at least {m}. The number of ways is ____.', o=None, a=val,
                    sol=[f'Give {m} to each first; share the remaining {n - k * m} freely: stars and bars.', f'C({n - k * m + k - 1}, {k - 1}) = {val}.'], p=dict(t=t, k=k, m=m, n=n))
    if t == 't_onto':
        n, k = rng.randint(4, 7), rng.randint(2, 4); need(n >= k)
        val = sum((-1) ** j * C(k, j) * (k - j) ** n for j in range(k + 1))
        return dict(q=f'The number of ways of putting {n} different books into {k} different bags so that no bag is empty is ____.', o=None, a=val,
                    sol=['All ways k^{n}, then inclusion–exclusion over the empty bags.', f'Σ(−1)^{{j}}C({k}, j)({k} − j)^{{{n}}} = {val}.'], p=dict(t=t, n=n, k=k))
    if t == 't_lift':
        p, top, s = rng.randint(2, 4), rng.randint(6, 12), rng.randint(0, 3); f = top - s; ask = rng.choice(['diff', 'any'])
        val = math.perm(f, p) if ask == 'diff' else f ** p; need(f >= p)
        return dict(q=f'{p} persons enter a lift at the ground floor; it goes up to floor {top} and does not stop at the first {s} floors. The number of ways they can get out {"at different floors" if ask == "diff" else "(any floor each)"} is ____.'.replace(' and does not stop at the first 0 floors', ''), o=None, a=val,
                    sol=[f'Usable floors: {f}.', f'{"P(f, p)" if ask == "diff" else "f^{p}"} = {val}.'], p=dict(t=t, p=p, top=top, s=s, ask=ask))
    if t == 't_dice':
        k = rng.randint(3, 4); S = rng.randint(k + 2, 6 * k - 2); val = sum(1 for d in itertools.product(range(1, 7), repeat=k) if sum(d) == S)
        return dict(q=f'The number of ways of getting a total of {S} when a die is thrown {k} times is ____.', o=None, a=val,
                    sol=['Count solutions of d_{1} + … + d_{k} = S with 1 ≤ d_{i} ≤ 6 (stars and bars, then remove the ones with a d_{i} > 6).', f'→ {val}.'], p=dict(t=t, k=k, S=S))
    n = rng.randint(3, 7); val = C(2 * n - 1, n)
    return dict(q=f'In a series, the first player to win {n} games wins (no draws). The number of ways in which player A can win the series is ____.', o=None, a=val,
                sol=[f'A wins the last game; before it A has {n - 1} wins and B has k ≤ {n - 1}.', f'Σ C({n - 1} + k, k) = C({2 * n - 1}, {n}) = {val}.'], p=dict(t='t_series', n=n))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(arr=g_arr, sel=g_sel, geo=g_geo, dig=g_dig, dist=g_dist).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'a_rank': return R == words(p['w']).index(tuple(p['x'])) + 1
    if t == 'a_nth': return R == ''.join(words(p['w'])[p['n'] - 1])
    if t == 'a_apart':
        k = sum(c in VOW for c in p['w']); tog = sum(1 for w in itertools.permutations(p['w']) if (lambda ix: max(ix) - min(ix) == k - 1)([i for i, c in enumerate(w) if c in VOW]))
        return R == (tog if p['ask'] == 'always' else math.factorial(len(p['w'])) - tog)
    if t == 'a_rep': return R == sum(1 for _ in set(itertools.permutations(p['w'], p['r'])))
    if t == 'a_block':
        b, g = p['b'], p['g']; tot = 0
        for pos in itertools.combinations(range(b + g), g):
            s = ['B'] * (b + g)
            for x in pos: s[x] = 'G'
            s = ''.join(s); ok = {'gt': 'G' * g in s, 'gnt': 'G' * g not in s, 'alt': 'BB' not in s and 'GG' not in s, 'nobb': 'BB' not in s}[p['ask']]; tot += ok
        return R == tot * math.factorial(b) * math.factorial(g)
    if t == 'a_ends':
        def ok(w): return {'vv': w[0] in VOW and w[-1] in VOW, 'cc': w[0] not in VOW and w[-1] not in VOW, 'vc': (w[0] in VOW) != (w[-1] in VOW)}[p['ask']]
        return R == sum(1 for w in itertools.permutations(p['w']) if ok(w))
    if t == 's_grp':
        m1, w1, m2, w2 = p['g']; k = p['k']
        return R == sum(1 for a in itertools.combinations(range(m1 + w1), k) for b in itertools.combinations(range(m2 + w2), k) if sum(x < m1 for x in a) + sum(x < m2 for x in b) == p['M'])
    if t == 's_atl':
        cs = p['cs']; col = [0] * cs[0] + [1] * cs[1] + [2] * cs[2]
        return R == sum(1 for s in itertools.combinations(range(len(col)), p['n']) if all(sum(col[x] == c for x in s) >= p['k'] for c in range(3)))
    if t == 's_multi':
        from collections import Counter
        cnt = Counter(p['w']); L = sorted(cnt)
        return R == sum(1 for v in itertools.product(*[range(cnt[c] + 1) for c in L]) if sum(v) == p['r'])
    if t == 's_mid': return R == sum(1 for c in itertools.combinations(range(1, 27), p['r']) if c[p['r'] // 2] == p['pos'])
    if t == 's_team':
        a, b = p['a'], p['b']; return R == sum(1 for s in itertools.combinations(range(a + b), p['n']) if sum(x < a for x in s) >= p['k'] and sum(x >= a for x in s) >= p['k'])
    if t in ('g_sides', 'g_poly'):
        s = p['s']; side = lambda x: 0 if x < s[0] else 1 if x < s[0] + s[1] else 2; k = 5 if t == 'g_poly' else 3 if p['ask'] == 'tri' else 4
        return R == sum(1 for q in itertools.combinations(range(sum(s)), k) if (len({side(x) for x in q}) > 1 if k == 3 else max([side(x) for x in q].count(i) for i in range(3)) <= 2))
    if t == 'g_coll':
        n, m = p['n'], p['m']; pts = [(i, 0) for i in range(m)] + [(i, i * i + 1 + 7 * i * i * i) for i in range(1, n - m + 1)]
        col = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])
        if p['ask'] == 'tri': return R == sum(1 for a, b, c in itertools.combinations(pts, 3) if not col(a, b, c))
        lines = set()
        for a, b in itertools.combinations(pts, 2):
            A, B = b[1] - a[1], a[0] - b[0]; Cc = A * a[0] + B * a[1]; g = math.gcd(math.gcd(A, B), Cc) or 1
            if A < 0 or (A == 0 and B < 0): g = -g
            lines.add((A // g, B // g, Cc // g))
        return R == len(lines)
    if t == 'g_lines':
        pts = [(0, 0)] + [(k, 2 * k) for k in range(1, p['p'] + 1)] + [(2 * k, k) for k in range(1, p['q'] + 1)]
        return R == sum(1 for a, b, c in itertools.combinations(pts, 3) if (b[0] - a[0]) * (c[1] - a[1]) != (c[0] - a[0]) * (b[1] - a[1]))
    if t == 'g_ngon':
        n = p['n']; adj = lambda i, j: (i - j) % n in (1, n - 1)
        if p['ask'] == 'diag': return R == sum(1 for i, j in itertools.combinations(range(n), 2) if not adj(i, j))
        if p['ask'] == 'tri': return R == sum(1 for _ in itertools.combinations(range(n), 3))
        return R == sum(1 for a, b, c in itertools.combinations(range(n), 3) if not (adj(a, b) or adj(b, c) or adj(a, c)))
    if t == 'd_div3': return R == sum(1 for x in range(10 ** (p['k'] - 1), 10 ** p['k']) if len(set(str(x))) == p['k'] and set(str(x)) <= set(map(str, p['ds'])) and ((x % p['m'] == 0) == (p['ask'] == 'is')))
    if t == 'd_sum': return R == sum(1 for x in range(10 ** (p['n'] - 1), 10 ** p['n']) if set(str(x)) <= set(map(str, p['ds'])) and sum(map(int, str(x))) == p['s'])
    if t == 'd_range': return R == sum(1 for d in itertools.product(map(str, p['ds']), repeat=4) if d[0] != '0' and p['lo'] < int(''.join(d)) < p['hi'] and int(''.join(d)) % p['m'] == 0) + sum(1 for x in range(p['lo'] + 1, p['hi']) if x >= 10000 and x % p['m'] == 0 and set(str(x)) <= set(map(str, p['ds'])))
    if t == 'd_desc':
        k = p['k']; return R == sum(1 for x in range(10 ** (k - 1), 10 ** k) if all((a > b) if p['ask'] == 'dec' else (a < b) for a, b in zip(str(x), str(x)[1:])))
    if t == 'd_mult': return R == len([x for x in range(10 ** (p['k'] - 1), 10 ** p['k']) if x % p['a'] == 0]) - len([x for x in range(10 ** (p['k'] - 1), 10 ** p['k']) if x % p['a'] == 0 and x % p['b'] == 0])
    if t == 't_stars':
        k, m, n = p['k'], p['m'], p['n']; return R == sum(1 for v in itertools.product(range(m, n + 1), repeat=k - 1) if n - sum(v) >= m)
    if t == 't_onto': return R == sum(1 for f in itertools.product(range(p['k']), repeat=p['n']) if len(set(f)) == p['k'])
    if t == 't_lift':
        fl = range(p['s'] + 1, p['top'] + 1); return R == sum(1 for f in itertools.product(fl, repeat=p['p']) if p['ask'] == 'any' or len(set(f)) == p['p'])
    if t == 't_dice': return R == sum(1 for d in itertools.product(range(1, 7), repeat=p['k']) if sum(d) == p['S'])
    if t == 't_series':
        n = p['n']; return R == sum(1 for L in range(n, 2 * n) for s in itertools.product('AB', repeat=L) if s[-1] == 'A' and s.count('A') == n)
    raise KeyError(t)
