"""Paper 3 Ch 9 — Number Series, Coding-Decoding, Odd Man Out: extra MCQ templates.
Every question is checked for a UNIQUE answer: the options are tested against a library of series rules /
code rules / classification properties, and only questions where exactly one option fits are kept."""
from common import *
import math, string

U = 'fnd-p3-ch09-u01'
C1, C2, C3, C4 = 'Number series — the testing ladder', 'Missing term vs wrong term', 'Alphabet series and letter positions', 'Letter series (blanks in a repeating block)'
C5, C6, C7 = 'Letter coding — finding and applying the rule', 'Number coding', 'Odd man out (classification)'
AL = string.ascii_uppercase
PRIMES = [p for p in range(2, 400) if all(p % k for k in range(2, int(p ** .5) + 1))]


# ---------- series rule library (generator side) ----------
def fits_any(seq):
    """True if a simple rule explains the whole sequence"""
    n = len(seq); xs = [F(x) for x in seq]
    def poly_fit(deg):
        if n < deg + 3: return False
        d = xs[:]
        for _ in range(deg + 1): d = [b - a for a, b in zip(d, d[1:])]
        return all(v == 0 for v in d)
    if any(poly_fit(k) for k in (0, 1, 2)) or (n >= 6 and poly_fit(3)): return True
    if all(x != 0 for x in xs) and len({b / a for a, b in zip(xs, xs[1:])}) == 1: return True
    for a in range(-3, 6):
        if a == 0: continue
        b = xs[1] - a * xs[0]
        if all(xs[i + 1] == a * xs[i] + b for i in range(n - 1)): return True
    ds = [b - a for a, b in zip(xs, xs[1:])]
    if all(d != 0 for d in ds) and len({b / a for a, b in zip(ds, ds[1:])}) == 1 and len(ds) >= 3: return True
    if n >= 5 and len({xs[i + 2] - xs[i] for i in range(0, n - 2, 2)}) == 1 and len({xs[i + 2] - xs[i] for i in range(1, n - 2, 2)}) == 1: return True
    if all(xs[i + 2] == xs[i + 1] + xs[i] for i in range(n - 2)): return True
    # alternating two operations (×a then +b, or +a then +b)
    for i0 in (0, 1):
        pass
    o1 = [(xs[i], xs[i + 1]) for i in range(0, n - 1, 2)]; o2 = [(xs[i], xs[i + 1]) for i in range(1, n - 1, 2)]
    def one_op(pairs):
        if len({b - a for a, b in pairs}) == 1: return True
        if all(a != 0 for a, b in pairs) and len({b / a for a, b in pairs}) == 1: return True
        return False
    if len(o1) >= 2 and len(o2) >= 2 and one_op(o1) and one_op(o2): return True
    return False


def series_patterns(r):
    k = r.choice(range(8))
    if k == 0:  # n^2 + c  or  n^3 + c
        p = r.choice([2, 3]); c = r.randint(-5, 6); s = r.randint(1, 5); seq = [(s + i) ** p + c for i in range(6)]
        rule = f'each term is a {"square" if p == 2 else "cube"} {"plus" if c >= 0 else "minus"} {abs(c)}: ' + ', '.join(f'{s + i}{sup(p)}{"+" if c >= 0 else "−"}{abs(c)}' for i in range(3)) + ' …'
    elif k == 1:  # x -> a x + b
        a = r.choice([2, 3]); b = r.choice([-3, -2, -1, 1, 2, 3, 4]); x = r.randint(1, 6); seq = [x]
        for _ in range(5): seq.append(a * seq[-1] + b)
        rule = f'each term = previous × {a} {"+" if b > 0 else "−"} {abs(b)}'
    elif k == 2:  # differences in AP
        a = r.randint(1, 30); d0 = r.randint(1, 6); dd = r.randint(1, 4); seq = [a]
        for i in range(5): seq.append(seq[-1] + d0 + i * dd)
        rule = f'the differences {", ".join(str(d0 + i * dd) for i in range(4))} … increase by {dd}'
    elif k == 3:  # differences in GP
        a = r.randint(1, 20); d0 = r.randint(1, 4); g = r.choice([2, 3]); seq = [a]
        for i in range(5): seq.append(seq[-1] + d0 * g ** i)
        rule = f'the differences {", ".join(str(d0 * g ** i) for i in range(4))} … are multiplied by {g} each time'
    elif k == 4:  # alternate × and +
        a = r.choice([2, 3]); b = r.randint(1, 9); x = r.randint(1, 9); seq = [x]
        for i in range(5): seq.append(seq[-1] * a if i % 2 == 0 else seq[-1] + b)
        rule = f'the operations alternate: × {a}, + {b}, × {a}, + {b} …'
    elif k == 5:  # interleaved
        a, b = r.randint(1, 30), r.randint(1, 30); d1, d2 = r.choice([2, 3, 4, 5, 7]), r.choice([-3, -2, 2, 3, 6]); seq = []
        for i in range(7): seq.append(a + (i // 2) * d1 if i % 2 == 0 else b + (i // 2) * d2)
        rule = f'two series are interleaved: {seq[0]}, {seq[2]}, {seq[4]} … (step {d1}) and {seq[1]}, {seq[3]}, {seq[5]} … (step {d2})'
    elif k == 6:  # consecutive primes
        i = r.randint(3, 25); seq = PRIMES[i:i + 6]; rule = 'consecutive prime numbers'
    else:  # products n(n+1)
        s = r.randint(1, 8); seq = [(s + i) * (s + i + 1) for i in range(6)]; rule = f'n × (n + 1): {s}×{s + 1}, {s + 1}×{s + 2}, …'
    return seq, rule


def near_wrongs(r, v, extra=()):
    out = list(extra) + [v + 1, v - 1, v + 2, v - 2, v + 3, v * 2, v + 10, v - 10]
    return out


def series_q(r, mode):
    seq, rule = series_patterns(r)
    if not fits_any(seq): return None
    pos = len(seq) - 1 if mode == 'next' else r.randint(1, len(seq) - 2)
    ans = seq[pos]; shown = [str(x) if i != pos else '?' for i, x in enumerate(seq)]
    cands = [w for w in near_wrongs(r, ans) if w != ans]
    good = []
    for w in cands:
        t = seq[:]; t[pos] = w
        if not fits_any(t): good.append(w)
    if len(good) < 3: return None
    ws = r.sample(good[:6], 3)
    return dict(q=f'Find the {"next term" if mode == "next" else "missing term"}: {", ".join(shown)}', a=str(ans), w=[str(x) for x in ws],
                ex=f'Test the ladder: differences, ratios, squares/cubes, alternating steps. Here {rule}. So the {"next" if mode == "next" else "missing"} term is {ans}. Check that the rule works across every given term before choosing; each of the other options breaks the pattern somewhere.',
                fast='Write the differences under the terms first; if they do not settle, try ratios, then alternate terms.', secs=45, d='moderate', topic=C1 if mode == 'next' else C2,
                check=str(ans), k='ch09.series', data={'shown': ', '.join(shown)})


def series_next(r): return series_q(r, 'next')
def series_missing(r): return series_q(r, 'missing')


def series_wrong(r):
    seq, rule = series_patterns(r)
    if not fits_any(seq) or len(seq) < 6: return None
    pos = r.randint(2, len(seq) - 1); bad = seq[pos] + r.choice([-3, -2, -1, 1, 2, 3, 5])
    t = seq[:]; t[pos] = bad
    if fits_any(t) or bad in seq: return None
    # no other single position can be "repaired" by some simple rule
    for j in range(len(t)):
        if j == pos: continue
        for cand in range(-50, 2000):
            u = t[:]; u[j] = cand
            if fits_any(u): return None
    others = [x for i, x in enumerate(t) if i != pos and i >= 1]
    ws = r.sample(others, 3)
    return dict(q=f'Find the wrong term in the series: {", ".join(map(str, t))}', a=str(bad), w=[str(x) for x in ws],
                ex=f'The intended rule: {rule}. Following it, the term in position {pos + 1} should be {seq[pos]}, but {bad} is given. Every other term fits the rule, so {bad} is the wrong term. Always confirm by checking the terms after the suspect as well.',
                fast='Find the rule from the first three or four terms, then scan for the single term that breaks it.', secs=60, d='hard', topic=C2,
                check=str(bad), k='ch09.wrong', data={'shown': ', '.join(map(str, t))})


def letter_series(r):
    kind = r.choice(['step', 'grow', 'pairs'])
    if kind == 'step':
        s = r.randint(0, 5); d = r.choice([2, 3, 4, 5]); idx = [s + i * d for i in range(5)]
        if idx[-1] > 25: return None
        rule = f'each letter moves {d} places forward'
    elif kind == 'grow':
        s = r.randint(0, 3); idx = [s]; d = r.randint(1, 2)
        for i in range(4): idx.append(idx[-1] + d + i)
        if idx[-1] > 25: return None
        rule = f'the gaps grow by one: +{d}, +{d + 1}, +{d + 2}, +{d + 3}'
    else:
        s = r.randint(0, 3); d = r.choice([3, 4, 5]); groups = [(s + i * d, s + i * d + 1) for i in range(4)]
        if groups[-1][1] > 25: return None
        shown = ', '.join(AL[a] + AL[b] for a, b in groups[:3]) + ', ?'; ans = AL[groups[3][0]] + AL[groups[3][1]]
        ws = [AL[groups[3][0] + 1] + AL[groups[3][1] + 1] if groups[3][1] < 25 else 'ZA', AL[groups[3][0] - 1] + AL[groups[3][1] - 1], AL[groups[3][1]] + AL[groups[3][0]], AL[groups[3][0]] + AL[min(25, groups[3][1] + 1)]]
        return dict(q=f'Find the next term: {shown}', a=ans, w=ws,
                    ex=f'Each pair is two consecutive letters, and the first letters move {d} places: {", ".join(AL[a] for a, b in groups[:3])}, so the next first letter is {AL[groups[3][0]]} and the pair is {ans}. Write the letter positions (A = 1 … Z = 26) to see steps quickly.',
                    fast='Convert to positions: first letters ' + ', '.join(str(a + 1) for a, b in groups[:3]) + f' … step {d}.', secs=30, d='core', topic=C3, k='ch09.letters', data={'shown': shown})
    shown = ', '.join(AL[i] for i in idx[:4]) + ', ?'; ans = AL[idx[4]]
    ws = [AL[idx[4] + 1] if idx[4] < 25 else 'A', AL[idx[4] - 1], AL[idx[3] + (idx[3] - idx[2])] if AL[idx[3] + (idx[3] - idx[2])] != ans else AL[idx[4] - 2], AL[min(25, idx[4] + 2)]]
    if any(fits_any([i + 1 for i in idx[:4]] + [AL.index(w) + 1]) for w in ws if w != ans): return None      # another simple rule would give a different letter
    return dict(q=f'Find the next letter: {shown}', a=ans, w=ws,
                ex=f'Write the positions (A = 1, B = 2, …): {", ".join(str(i + 1) for i in idx[:4])}. Here {rule}, so the next position is {idx[4] + 1}, which is {ans}. Remembering E = 5, J = 10, O = 15, T = 20 and Y = 25 makes the conversion fast.',
                fast='Use the EJOTY anchors (5, 10, 15, 20, 25) to convert letters to numbers instantly.', secs=30, d='core', topic=C3, k='ch09.letters', data={'shown': shown})


# ---------- coding rules (generator side) ----------
def shift(w, k): return ''.join(AL[(AL.index(c) + k) % 26] for c in w)
def opp(w): return ''.join(AL[25 - AL.index(c)] for c in w)
def alt(w, k): return ''.join(AL[(AL.index(c) + (k if i % 2 == 0 else -k)) % 26] for i, c in enumerate(w))
def swap2(w): return ''.join(w[i + 1] + w[i] if i + 1 < len(w) else w[i] for i in range(0, len(w), 2))


def code_rules():
    rules = []
    for k in range(-6, 7):
        if k: rules.append((f'shift{k}', lambda w, k=k: shift(w, k)))
        if k: rules.append((f'rev+shift{k}', lambda w, k=k: shift(w[::-1], k)))
        if k > 0: rules.append((f'alt{k}', lambda w, k=k: alt(w, k)))
    rules += [('opp', opp), ('rev', lambda w: w[::-1]), ('rev+opp', lambda w: opp(w[::-1])), ('swap2', swap2)]
    return rules


WORDS = ['BANK', 'CASH', 'LOAN', 'GOLD', 'COST', 'BOND', 'FUND', 'RATE', 'SALE', 'TAX', 'DEBT', 'GAIN', 'LOSS', 'PROFIT', 'MARGIN', 'CREDIT', 'ASSET', 'AUDIT', 'STOCK', 'TRADE', 'PRICE', 'MONEY', 'BUDGET', 'LEDGER', 'INCOME', 'EQUITY']


def coding(r):
    rules = code_rules(); name, f = r.choice(rules)
    if name in ('rev',): return None
    w1, w2 = r.sample(WORDS, 2)
    c1 = f(w1); ans = f(w2)
    if c1 == w1: return None
    fit = [g for n_, g in rules if g(w1) == c1]
    if len({g(w2) for g in fit}) != 1: return None
    wrong = list({g(w2) for n_, g in rules if g(w2) != ans})
    r.shuffle(wrong)
    # prefer near-misses: same rule family with a different step
    near = [shift(ans, 1), shift(ans, -1), ans[::-1]] + wrong
    desc = {'shift': 'every letter moves the same number of places', 'rev+shift': 'the word is reversed and each letter is shifted', 'alt': 'letters move alternately forward and backward',
            'opp': 'each letter is replaced by its opposite (A↔Z, B↔Y, …)', 'rev+opp': 'the word is reversed and each letter replaced by its opposite (A↔Z)', 'swap2': 'each pair of neighbouring letters is swapped'}
    fam = next(v for k_, v in desc.items() if name.startswith(k_) and (k_ != 'shift' or not name.startswith('rev')))
    if name.startswith('rev+shift'): fam = desc['rev+shift']
    if name.startswith('rev+opp'): fam = desc['rev+opp']
    return dict(q=f'In a certain code, {w1} is written as {c1}. How is {w2} written in that code?', a=ans, w=near,
                ex=f'Compare {w1} and {c1} letter by letter using positions (A = 1 … Z = 26). The rule: {fam}' + (f' (step {name.split("shift")[-1] if "shift" in name else name[3:]})' if any(x in name for x in ('shift', 'alt')) else '') + f'. Applying the same rule to {w2} gives {ans}. Always test the rule on every letter of the example, not just the first one.',
                fast='Write positions of the first two letters of the word and the code; the gap or mirror (sum 27) shows the rule at once.', secs=45, d='moderate', topic=C5,
                k='ch09.code', data={'w1': w1, 'c1': c1, 'w2': w2})


def wordval(w, kind):
    p = [AL.index(c) + 1 for c in w]
    return {'sum': sum(p), 'rsum': sum(27 - x for x in p), 'sum+len': sum(p) + len(w), 'twice': 2 * sum(p), 'sumsq': sum(x * x for x in p) if False else sum(p) * len(w)}[kind]


NKINDS = ['sum', 'rsum', 'sum+len', 'twice', 'sumsq']


def num_coding(r):
    kind = r.choice(NKINDS); w1, w2 = r.sample(WORDS, 2)
    v1 = wordval(w1, kind); fit = [k for k in NKINDS if wordval(w1, k) == v1]
    if len({wordval(w2, k) for k in fit}) != 1: return None
    ans = wordval(w2, kind)
    desc = {'sum': 'the sum of the letter positions (A = 1 … Z = 26)', 'rsum': 'the sum of the reverse positions (A = 26 … Z = 1)', 'sum+len': 'the sum of the letter positions plus the number of letters',
            'twice': 'twice the sum of the letter positions', 'sumsq': 'the sum of the letter positions multiplied by the number of letters'}[kind]
    ws = [wordval(w2, k) for k in NKINDS if wordval(w2, k) != ans] + [ans + 1, ans - 2]
    return dict(q=f'If {w1} is coded as {v1}, then {w2} is coded as:', a=str(ans), w=[str(x) for x in ws],
                ex=f'Find what {v1} means for {w1}: the positions are {", ".join(str(AL.index(c) + 1) for c in w1)}. The code is {desc}, which gives {v1}. For {w2} the positions are {", ".join(str(AL.index(c) + 1) for c in w2)}, so its code is {ans}.',
                fast='Add the letter positions first; compare with the given number to see what extra step (×2, + letters, reverse) is used.', secs=60, d='moderate', topic=C6,
                check=str(ans), k='ch09.numcode', data={'w1': w1, 'v1': v1, 'w2': w2})


# ---------- odd man out (generator side) ----------
def props():
    P = [('prime', lambda n: n in PRIMES or (n > 1 and all(n % k for k in range(2, int(n ** .5) + 1)))), ('square', lambda n: math.isqrt(n) ** 2 == n), ('cube', lambda n: round(n ** (1 / 3)) ** 3 == n),
         ('even', lambda n: n % 2 == 0), ('digit sum even', lambda n: sum(map(int, str(n))) % 2 == 0)]
    P.append(('palindrome', lambda n: str(n) == str(n)[::-1]))
    for k in range(3, 21):
        P.append((f'multiple of {k}', lambda n, k=k: n % k == 0))
    return P


def odd_ones(nums_):
    out = set()
    for name, f in props():
        v = [f(x) for x in nums_]
        if v.count(True) == 1: out.add(nums_[v.index(True)])
        if v.count(False) == 1: out.add(nums_[v.index(False)])
    return out


def odd_number(r):
    kind = r.choice(['prime', 'square', 'cube', 'mult'])
    if kind == 'prime': good = r.sample([p for p in PRIMES if 20 < p < 200], 3); bad = r.choice([x for x in range(21, 200, 2) if x not in PRIMES and x % 3 and x % 5]); why = f'{bad} = {next(k for k in range(2, bad) if bad % k == 0)} × {bad // next(k for k in range(2, bad) if bad % k == 0)} is not prime, while the others are prime'
    elif kind == 'square': good = [x * x for x in r.sample(range(5, 25), 3)]; bad = r.choice(good) + r.choice([-2, 2, 3, 5]); why = f'{bad} is not a perfect square; the others are ' + ', '.join(f'{math.isqrt(g)}²' for g in good)
    elif kind == 'cube': good = [x ** 3 for x in r.sample(range(2, 11), 3)]; bad = r.choice(good) + r.choice([-1, 1, 2]); why = f'{bad} is not a perfect cube; the others are ' + ', '.join(f'{round(g ** (1 / 3))}³' for g in good)
    else:
        k = r.choice([7, 11, 13, 17]); good = [k * x for x in r.sample(range(3, 15), 3)]; bad = r.choice(good) + r.choice([1, 2, 3, -1, -2]); why = f'all except {bad} are multiples of {k}'
    nums_ = good + [bad]
    if len(set(nums_)) < 4 or odd_ones(nums_) != {bad}: return None
    return dict(q=f'Find the odd one out: {", ".join(map(str, sorted(nums_)))}', a=str(bad), w=[str(x) for x in good],
                ex=f'Look for a property shared by three numbers. Here {why}. So {bad} is the odd one out. Check simple properties in order: even/odd, prime, perfect square or cube, and common multiples (7, 11, 13, 17).',
                fast='Test prime / square / cube / divisibility by 7, 11, 13 on all four quickly; one number will fail.', secs=40, d='moderate', topic=C7,
                check=str(bad), k='ch09.odd', data={'shown': ', '.join(map(str, sorted(nums_)))})


def odd_letters(r):
    k = r.choice([1, 2, 3, 4]); groups = []
    starts = r.sample(range(0, 26 - 2 * k - 1), 4)
    for s in starts[:3]: groups.append(AL[s] + AL[s + k] + AL[s + 2 * k])
    s = starts[3]; k2 = k + r.choice([1, -1]) if k > 1 else k + 1
    bad = AL[s] + AL[s + k] + AL[min(25, s + k + k2)]
    if s + k + k2 > 25 or bad in groups: return None
    def step_set(g): return {AL.index(g[1]) - AL.index(g[0]), AL.index(g[2]) - AL.index(g[1])}
    if len(step_set(bad)) == 1: return None
    allg = groups + [bad]
    hasv = [any(c in 'AEIOU' for c in g) for g in allg]
    if hasv.count(True) == 1 or hasv.count(False) == 1: return None      # a vowel rule would pick a different group
    return dict(q=f'Find the odd one out: {", ".join(sorted(allg))}', a=bad, w=groups,
                ex=f'Write the letter positions. In {", ".join(groups)} the letters move by a constant step of {k} (skip {k - 1} letter{"s" if k != 2 else ""} each time). In {bad} the steps are {AL.index(bad[1]) - AL.index(bad[0])} and {AL.index(bad[2]) - AL.index(bad[1])}, so it does not follow the pattern and is the odd one out.',
                fast='Count the gaps inside each group; the group with unequal gaps is odd.', secs=35, d='core', topic=C7, k='ch09.oddlet', data={'shown': ', '.join(sorted(allg))})


BANKS = {U: [(series_next, 4), (series_missing, 4), (series_wrong, 3), (letter_series, 4), (coding, 5), (num_coding, 3), (odd_number, 4), (odd_letters, 2)]}
