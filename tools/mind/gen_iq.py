#!/usr/bin/env python3
"""Brain Power (IQ-style) question generator for Mind Gym.

Every question is made by a rule and its answer is worked out by this program, then
checked again:
  * the right answer is computed, never typed by hand;
  * every wrong option is different from the right one;
  * puzzles with more than one sensible answer are thrown away (series, number machines,
    odd-one-out and grids are tested against a library of other rules);
  * no two questions are the same.
Run:  python3 tools/mind/gen_iq.py   ->  content/mind/iq.json
Bands: j = Grades 1-3, m = Grades 4-8, s = Grades 9-12 and CA.
"""
import json, random, math, os, sys
from fractions import Fraction

R = random.Random(20261111)
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'content', 'mind', 'iq.json')
QS, SEEN = [], set()


def add(band, kind, q, right, wrong, why):
    right = str(right)
    opts = []
    for w in wrong:
        w = str(w)
        if w != right and w not in opts:
            opts.append(w)
    if len(opts) < 3:
        return False
    opts = opts[:3] + [right]
    R.shuffle(opts)
    key = (band, q, tuple(sorted(opts)))
    if key in SEEN:
        return False
    SEEN.add(key)
    QS.append({'b': band, 'k': kind, 'q': q, 'o': opts, 'a': opts.index(right), 'why': why})
    return True


def near(n, spread=(1, 2, 3, 4, 5, 6, 10), lo=0):
    """distinct plausible wrong numbers around n"""
    c = set()
    for d in spread:
        for s in (1, -1):
            v = n + s * d
            if v >= lo and v != n:
                c.add(v)
    c = list(c)
    R.shuffle(c)
    return c

# ---------------- number series ----------------
def series_rules(t):
    """every simple rule the given terms fit -> its predicted next term"""
    p = {}
    n = len(t)
    d = [t[i + 1] - t[i] for i in range(n - 1)]
    if len(set(d)) == 1:
        p['arith'] = t[-1] + d[0]
    if all(x != 0 for x in t[:-1]):
        r = [Fraction(t[i + 1], t[i]) for i in range(n - 1)]
        if len(set(r)) == 1:
            p['geo'] = t[-1] * r[0]
    dd = [d[i + 1] - d[i] for i in range(len(d) - 1)]
    if len(dd) >= 2 and len(set(dd)) == 1:
        p['second'] = t[-1] + d[-1] + dd[0]
    if n >= 5:
        a, b = t[0::2], t[1::2]
        da = [a[i + 1] - a[i] for i in range(len(a) - 1)]
        db = [b[i + 1] - b[i] for i in range(len(b) - 1)]
        if len(set(da)) == 1 and len(set(db)) == 1 and da and db:
            p['alt'] = (a[-1] + da[0]) if n % 2 == 0 else (b[-1] + db[0])
    # x*k + c (same k and c each step)
    if n >= 4 and t[1] != t[0]:
        for k in range(-3, 4):
            c = t[1] - k * t[0]
            if all(t[i + 1] == k * t[i] + c for i in range(n - 1)):
                p['lin%d' % k] = k * t[-1] + c
    # squares / cubes / primes / fibonacci-like
    if n >= 3 and all(t[i] == t[i - 1] + t[i - 2] for i in range(2, n)):
        p['fib'] = t[-1] + t[-2]
    return p


def series_ok(t, ans, wrong):
    p = series_rules(t)
    vals = set(Fraction(v) for v in p.values())
    if vals and vals != {Fraction(ans)}:
        return False           # two rules disagree: not a fair puzzle
    return not any(Fraction(w) in vals for w in wrong)


def gen_series(band, want):
    made = 0
    tries = 0
    while made < want and tries < want * 200:
        tries += 1
        kind = R.choice({'j': ['add', 'add', 'sub', 'skip'], 'm': ['add', 'sub', 'mul', 'second', 'alt', 'lin'], 's': ['mul', 'second', 'alt', 'lin', 'fib', 'sq', 'lin']}[band])
        L = 5
        if kind == 'add':
            a, d = R.randint(1, 20 if band == 'j' else 60), R.randint(2, 5 if band == 'j' else 12)
            t = [a + d * i for i in range(L + 1)]
            why = 'Each number is %d more than the one before. %d + %d = %d.' % (d, t[-2], d, t[-1])
        elif kind == 'sub':
            d = R.randint(2, 5 if band == 'j' else 13)
            a = d * (L + 1) + R.randint(1, 30 if band == 'j' else 80)
            t = [a - d * i for i in range(L + 1)]
            why = 'Each number is %d less than the one before. %d − %d = %d.' % (d, t[-2], d, t[-1])
        elif kind == 'skip':
            d = R.choice([2, 5, 10]); a = d * R.randint(1, 6)
            t = [a + d * i for i in range(L + 1)]
            why = 'We are counting in %ds. After %d comes %d.' % (d, t[-2], t[-1])
        elif kind == 'mul':
            k = R.choice([2, 3] if band == 'm' else [2, 3, 4, 5]); a = R.randint(1, 5)
            t = [a * k ** i for i in range(L + 1)]
            why = 'Each number is %d times the one before. %d × %d = %d.' % (k, t[-2], k, t[-1])
        elif kind == 'second':
            a, d0, s = R.randint(1, 20), R.randint(1, 6), R.randint(1, 4)
            t = [a]; d = d0
            for i in range(L):
                t.append(t[-1] + d); d += s
            gaps = [t[i + 1] - t[i] for i in range(L)]
            why = 'The gaps are %s — they grow by %d each time, so the next gap is %d. %d + %d = %d.' % (', '.join(map(str, gaps[:-1])), s, gaps[-1], t[-2], gaps[-1], t[-1])
        elif kind == 'alt':
            a, b, da, db = R.randint(1, 30), R.randint(40, 90), R.randint(2, 7), -R.randint(2, 7)
            t = []
            for i in range(L + 1):
                t.append(a + da * (i // 2) if i % 2 == 0 else b + db * (i // 2))
            if any(x < 0 for x in t):
                continue
            why = 'Two series take turns: %s go up by %d, and %s go down by %d. The next one is %d.' % (
                ', '.join(map(str, t[0:L:2])), da, ', '.join(map(str, t[1:L:2])), -db, t[-1]) if L % 2 == 1 else ''
            if not why:
                continue
        elif kind == 'lin':
            k, c, a = R.choice([2, 3]), R.choice([-1, 1, 2, -2, 3]), R.randint(2, 6)
            t = [a]
            for i in range(L):
                t.append(t[-1] * k + c)
            if t[-1] > 3000:
                continue
            why = 'Rule: multiply by %d, then %s %d. %d × %d %s %d = %d.' % (k, 'add' if c > 0 else 'subtract', abs(c), t[-2], k, '+' if c > 0 else '−', abs(c), t[-1])
        elif kind == 'fib':
            a, b = R.randint(1, 6), R.randint(1, 9)
            t = [a, b]
            for i in range(L - 1):
                t.append(t[-1] + t[-2])
            why = 'Each number is the sum of the two before it. %d + %d = %d.' % (t[-3], t[-2], t[-1])
        elif kind == 'sq':
            s0 = R.randint(1, 8); off = R.choice([0, 1, -1, 2])
            t = [(s0 + i) ** 2 + off for i in range(L + 1)]
            why = 'These are square numbers%s: %d² %s= %d.' % ('' if off == 0 else (' %s %d' % ('plus' if off > 0 else 'minus', abs(off))), s0 + L, ('%s %d ' % ('+' if off > 0 else '−', abs(off))) if off else '', t[-1])
        shown, ans = t[:-1], t[-1]
        wrong = near(ans, (1, 2, t[-2] - t[-3] if len(t) > 2 else 3, 3, 5, 10))
        wrong = [w for w in wrong if w not in shown][:6]
        R.shuffle(wrong)
        if not series_ok(shown, ans, wrong[:3]):
            continue
        q = 'What comes next?  ' + ',  '.join(map(str, shown)) + ',  ?'
        if add(band, 'series', q, ans, wrong, why):
            made += 1

# ---------------- picture patterns (Grades 1-3 mainly) ----------------
PICS = ['🍎', '🍌', '🍇', '⭐', '🌙', '☀️', '🐶', '🐱', '🐟', '🚗', '🚲', '🎈', '🌸', '🍀', '🔺', '🔵', '🟩', '🟨', '❤️', '🦋', '🐘', '🥭', '🪁', '🥥', '🐢', '🦚']
PATTERNS = {'AB': [0, 1], 'ABC': [0, 1, 2], 'AAB': [0, 0, 1], 'ABB': [0, 1, 1], 'AABB': [0, 0, 1, 1], 'ABCD': [0, 1, 2, 3], 'ABAC': [0, 1, 0, 2], 'AABC': [0, 0, 1, 2]}


def gen_pictures(band, want):
    made = 0; tries = 0
    pats = ['AB', 'ABC', 'AAB', 'ABB', 'AABB'] if band == 'j' else ['ABC', 'AABB', 'ABCD', 'ABAC', 'AABC', 'ABB']
    while made < want and tries < 5000:
        tries += 1
        name = R.choice(pats); p = PATTERNS[name]
        k = max(p) + 1
        pics = R.sample(PICS, k)
        reps = 2 if len(p) >= 4 else 3
        full = [pics[i] for i in p] * (reps + 1)
        cut = len(p) * reps + R.randint(0, len(p) - 1)
        shown, ans = full[:cut], full[cut]
        others = [x for x in pics if x != ans] + [x for x in R.sample(PICS, 4) if x not in pics]
        unit = ' '.join(pics[i] for i in p)
        why = 'The pattern repeats: %s. So after %s comes %s.' % (unit, shown[-1], ans)
        if add(band, 'picture', 'What comes next?  ' + ' '.join(shown) + '  ❓', ans, others, why):
            made += 1

# ---------------- odd one out: numbers ----------------
PROPS = [
    ('even', lambda n: n % 2 == 0), ('odd', lambda n: n % 2 == 1),
    ('a multiple of 3', lambda n: n % 3 == 0), ('a multiple of 4', lambda n: n % 4 == 0), ('a multiple of 5', lambda n: n % 5 == 0),
    ('a multiple of 6', lambda n: n % 6 == 0), ('a multiple of 7', lambda n: n % 7 == 0), ('a multiple of 9', lambda n: n % 9 == 0),
    ('a multiple of 11', lambda n: n % 11 == 0),
    ('a square number', lambda n: int(math.isqrt(n)) ** 2 == n), ('a cube number', lambda n: round(n ** (1 / 3)) ** 3 == n),
    ('a prime number', lambda n: n > 1 and all(n % i for i in range(2, int(math.isqrt(n)) + 1))),
    ('a two-digit number', lambda n: 10 <= n <= 99), ('a three-digit number', lambda n: 100 <= n <= 999),
    ('a number whose digits add up to an even number', lambda n: sum(map(int, str(n))) % 2 == 0),
    ('a number with both digits the same', lambda n: len(str(n)) > 1 and len(set(str(n))) == 1),
    ('a number ending in 0', lambda n: n % 10 == 0),
]


PLURAL = {'even': 'even numbers', 'odd': 'odd numbers', 'a number ending in 0': 'numbers ending in 0', 'a square number': 'square numbers',
          'a cube number': 'cube numbers', 'a prime number': 'prime numbers', 'a number with both digits the same': 'numbers made of one repeated digit'}
for _k in (3, 4, 5, 6, 7, 9, 11):
    PLURAL['a multiple of %d' % _k] = 'multiples of %d' % _k


def odd_ok(items, odd_i, used_prop):
    """the chosen property must be the ONLY simple property that singles out exactly one item, and it must pick the odd one"""
    for name, f in PROPS:
        has = [f(x) for x in items]
        c = sum(has)
        if c == 1 or c == len(items) - 1:
            lone = has.index(True) if c == 1 else has.index(False)
            if lone != odd_i:
                return False
            if name != used_prop and c != 0:
                # another property also picks the same odd item: still the same answer, allowed
                pass
    return True


def gen_odd_numbers(band, want):
    made = 0; tries = 0
    pool = {'j': ['even', 'odd', 'a multiple of 5', 'a number ending in 0'],
            'm': ['a multiple of 3', 'a multiple of 4', 'a multiple of 6', 'a multiple of 7', 'a square number', 'a multiple of 9', 'a number with both digits the same'],
            's': ['a prime number', 'a square number', 'a cube number', 'a multiple of 7', 'a multiple of 11', 'a multiple of 9', 'a multiple of 6']}[band]
    top = {'j': 50, 'm': 150, 's': 400}[band]
    while made < want and tries < want * 400:
        tries += 1
        pname = R.choice(pool); f = dict(PROPS)[pname]
        yes = [n for n in range(2, top) if f(n)]
        no = [n for n in range(2, top) if not f(n)]
        if len(yes) < 3:
            continue
        items = R.sample(yes, 3)
        odd = R.choice(no)
        items.append(odd); R.shuffle(items)
        oi = items.index(odd)
        if not odd_ok(items, oi, pname):
            continue
        why = '%s are all %s. %d is not.' % (', '.join(str(x) for x in items if x != odd), PLURAL[pname], odd)
        if add(band, 'odd', 'Which number is the odd one out?', odd, [x for x in items if x != odd], why):
            made += 1


# ---------------- odd one out: words and pictures (hand-picked, non-overlapping groups) ----------------
GROUPS = {
    'fruits': (['Mango', 'Banana', 'Guava', 'Papaya', 'Apple', 'Grapes', 'Pineapple', 'Chikoo', 'Litchi', 'Watermelon', 'Pomegranate'], 'fruits'),
    'vehicles': (['Bus', 'Car', 'Scooter', 'Truck', 'Auto-rickshaw', 'Bicycle', 'Tractor', 'Train'], 'things we ride or travel in'),
    'birds': (['Parrot', 'Sparrow', 'Crow', 'Peacock', 'Pigeon', 'Eagle', 'Kingfisher', 'Owl'], 'birds'),
    'colours': (['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'White', 'Pink', 'Brown'], 'colours'),
    'body': (['Elbow', 'Knee', 'Ankle', 'Wrist', 'Shoulder'], 'joints of the body'),
    'instruments': (['Tabla', 'Sitar', 'Flute', 'Veena', 'Harmonium', 'Violin', 'Guitar', 'Drum'], 'musical instruments'),
    'planets': (['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Neptune', 'Uranus'], 'planets'),
    'shapes': (['Triangle', 'Square', 'Circle', 'Rectangle', 'Pentagon', 'Hexagon'], 'flat shapes'),
    'tools': (['Hammer', 'Screwdriver', 'Spanner', 'Saw', 'Pliers'], 'tools'),
    'stationery': (['Pencil', 'Eraser', 'Sharpener', 'Ruler', 'Crayon', 'Notebook'], 'things in a school bag'),
    'months': (['January', 'March', 'May', 'July', 'September', 'November'], 'months'),
    'days': (['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday'], 'days of the week'),
    'sports': (['Cricket', 'Football', 'Hockey', 'Kabaddi', 'Badminton', 'Tennis', 'Kho-kho'], 'sports'),
    'water': (['River', 'Lake', 'Pond', 'Sea', 'Ocean', 'Waterfall'], 'bodies of water'),
    'units': (['Metre', 'Centimetre', 'Kilometre', 'Millimetre'], 'units of length'),
    'mass': (['Gram', 'Kilogram', 'Milligram', 'Tonne'], 'units of mass'),
    'professions': (['Doctor', 'Teacher', 'Farmer', 'Pilot', 'Carpenter', 'Tailor', 'Nurse', 'Chef'], 'jobs people do'),
    'furniture': (['Chair', 'Table', 'Sofa', 'Bed', 'Cupboard', 'Stool'], 'furniture'),
}
PICGROUPS = {
    'fruit': (['🍎', '🍌', '🍇', '🍊', '🍉', '🥭', '🍍', '🍐'], 'fruits'),
    'animal': (['🐶', '🐱', '🐘', '🐄', '🐒', '🐯', '🐴', '🐐'], 'animals'),
    'vehicle': (['🚗', '🚌', '🚲', '🛵', '🚂', '🚜', '✈️'], 'vehicles'),
    'sports': (['⚽', '🏏', '🏀', '🏸', '🎾', '🏐'], 'sports things'),
    'weather': (['☀️', '🌧️', '⛈️', '❄️', '🌈', '☁️'], 'weather'),
    'clothes': (['👕', '👖', '👗', '🧢', '🧦', '🧣'], 'clothes'),
}


def gen_odd_words(band, want, pictures=False):
    G = PICGROUPS if pictures else GROUPS
    made = 0; tries = 0
    keys = list(G)
    while made < want and tries < want * 300:
        tries += 1
        a, b = R.sample(keys, 2)
        if {a, b} <= {'units', 'mass'} or {a, b} <= {'days', 'months'}:
            pass
        items = R.sample(G[a][0], 3)
        odd = R.choice(G[b][0])
        why = '%s are %s. %s is not.' % (', '.join(items), G[a][1], odd)
        if add(band, 'odd-pic' if pictures else 'odd-word', 'Which one does not belong with the others?', odd, items, why):
            made += 1

# ---------------- number machine (two examples, find the rule) ----------------
RULES = [
    ('adds %d', lambda k: (lambda x: x + k), range(2, 15)),
    ('takes away %d', lambda k: (lambda x: x - k), range(2, 10)),
    ('multiplies by %d', lambda k: (lambda x: x * k), range(2, 10)),
    ('doubles and adds %d', lambda k: (lambda x: 2 * x + k), range(1, 6)),
    ('triples and takes away %d', lambda k: (lambda x: 3 * x - k), range(1, 6)),
    ('multiplies the number by itself and adds %d', lambda k: (lambda x: x * x + k), range(1, 6)),
    ('multiplies the number by itself and takes away %d', lambda k: (lambda x: x * x - k), range(1, 6)),
]
ALL_RULES = []
for a_ in range(-3, 13):
    for b_ in range(-30, 31):
        ALL_RULES.append(('lin', 0, (lambda a, b: (lambda x: a * x + b))(a_, b_)))
for a_ in (1, 2, 3):
    for b_ in range(-20, 21):
        ALL_RULES.append(('quad', 0, (lambda a, b: (lambda x: a * x * x + b))(a_, b_)))
        ALL_RULES.append(('quadx', 0, (lambda a, b: (lambda x: a * x * x + x + b))(a_, b_)))
        ALL_RULES.append(('quad-x', 0, (lambda a, b: (lambda x: a * x * x - x + b))(a_, b_)))
ALL_RULES += [('halves', 0, lambda x: x / 2), ('cubes', 0, lambda x: x ** 3), ('cubes+', 0, lambda x: x ** 3 + 1)]


def gen_machine(band, want):
    made = 0; tries = 0
    allowed = {'j': [0, 1], 'm': [0, 1, 2, 3, 4], 's': [2, 3, 4, 5, 6]}[band]
    while made < want and tries < want * 400:
        tries += 1
        ri = R.choice(allowed); name, mk, ks = RULES[ri]
        k = R.choice(list(ks)); f = mk(k)
        xs = R.sample(range(1, 13 if band != 'j' else 10), 4)
        ys = [f(x) for x in xs]
        if any(y < 0 or y > 999 for y in ys):
            continue
        # every rule in the library that fits all three examples must give the same answer
        fits = set()
        for _, _, g in ALL_RULES:
            if all(g(xs[i]) == ys[i] for i in range(3)):
                fits.add(g(xs[3]))
        if fits != {ys[3]}:
            continue
        wrong = [w for w in near(ys[3]) if w not in fits]
        label = name % k if '%d' in name else name
        q = 'A number machine turns %d into %d, %d into %d, and %d into %d. What does it turn %d into?' % (xs[0], ys[0], xs[1], ys[1], xs[2], ys[2], xs[3])
        why = 'The machine %s: %d → %d, %d → %d, %d → %d. So %d → %d.' % (label, xs[0], ys[0], xs[1], ys[1], xs[2], ys[2], xs[3], ys[3])
        if add(band, 'machine', q, ys[3], wrong, why):
            made += 1

# ---------------- letter series ----------------
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def gen_letters(band, want):
    made = 0; tries = 0
    while made < want and tries < want * 300:
        tries += 1
        kind = R.choice({'j': ['step'], 'm': ['step', 'grow', 'back'], 's': ['grow', 'pair', 'back', 'step']}[band])
        if kind == 'step':
            d = R.randint(1, 3 if band == 'j' else 5); s = R.randint(0, 25 - 5 * d)
            idx = [s + d * i for i in range(6)]
            why = 'Each letter jumps %d place%s forward in the alphabet. After %s comes %s.' % (d, '' if d == 1 else 's', A[idx[-2]], A[idx[-1]])
        elif kind == 'back':
            d = R.randint(1, 4); s = R.randint(5 * d, 25)
            idx = [s - d * i for i in range(6)]
            why = 'Each letter goes %d place%s back in the alphabet. Before %s comes %s.' % (d, '' if d == 1 else 's', A[idx[-2]], A[idx[-1]])
        elif kind == 'grow':
            s = R.randint(0, 8); idx = [s]; d = 1
            for i in range(5):
                idx.append(idx[-1] + d); d += 1
            if idx[-1] > 25:
                continue
            why = 'The jumps grow: +1, +2, +3, +4, then +5. %s + 5 = %s.' % (A[idx[-2]], A[idx[-1]])
        else:  # pairs like AZ, BY, CX
            s = R.randint(0, 8)
            seq = [A[s + i] + A[25 - s - i] for i in range(5)]
            ans = seq[-1]
            wrong = [A[s + 4] + A[25 - s - 3], A[s + 5] + A[25 - s - 4], A[s + 4] + A[s + 5], A[25 - s - 4] + A[s + 4]]
            why = 'The first letter moves forward (%s) and the second moves backward from Z (%s).' % (', '.join(x[0] for x in seq), ', '.join(x[1] for x in seq))
            if add(band, 'letters', 'What comes next?  ' + ',  '.join(seq[:-1]) + ',  ?', ans, wrong, why):
                made += 1
            continue
        shown = [A[i] for i in idx[:-1]]; ans = A[idx[-1]]
        wrong = [A[j] for j in (idx[-1] - 1, idx[-1] + 1, idx[-1] - 2, idx[-1] + 2, idx[-2]) if 0 <= j < 26]
        if add(band, 'letters', 'What letter comes next?  ' + ',  '.join(shown) + ',  ?', ans, wrong, why):
            made += 1

# ---------------- secret codes ----------------
WORDS = {'j': ['CAT', 'DOG', 'SUN', 'BUS', 'PEN', 'HAT', 'CUP', 'BAT', 'COW', 'BOX', 'TOP', 'NET', 'JAM', 'FAN', 'MAP', 'EGG', 'RAT', 'BED', 'LEG', 'POT'],
         'm': ['MANGO', 'TIGER', 'CHAIR', 'PLANT', 'RIVER', 'TRAIN', 'CLOUD', 'BREAD', 'STONE', 'LEMON', 'HOUSE', 'MOUSE', 'TABLE', 'GRASS', 'SMILE', 'BRAVE', 'LIGHT', 'NOISE', 'WATER', 'FRUIT'],
         's': ['PLANET', 'MARKET', 'GARDEN', 'BRIDGE', 'FOREST', 'SCHOOL', 'PENCIL', 'WINDOW', 'ROCKET', 'BOTTLE', 'CANDLE', 'SILVER', 'TEMPLE', 'MIRROR', 'HUNTER', 'TICKET', 'POCKET', 'DESERT', 'FINGER', 'CASTLE']}


def shift(w, k):
    return ''.join(A[(A.index(c) + k) % 26] for c in w)


def gen_codes(band, want):
    made = 0; tries = 0
    ws = WORDS[band]
    while made < want and tries < want * 300:
        tries += 1
        a, b = R.sample(ws, 2)
        mode = R.choice(['shift', 'shift', 'rev'] if band != 'j' else ['shift'])
        if mode == 'shift':
            k = R.choice([1, 2] if band == 'j' else [1, 2, 3, -1, -2])
            ca, cb = shift(a, k), shift(b, k)
            wrong = [shift(b, k + 1), shift(b, k - 1) if k - 1 != 0 else shift(b, k + 2), shift(b, -k), shift(b[::-1], k)]
            why = 'Each letter moves %d place%s %s in the alphabet (%s → %s). So %s → %s.' % (abs(k), '' if abs(k) == 1 else 's', 'forward' if k > 0 else 'back', a[0], ca[0], b, cb)
        else:
            k = R.choice([1, 2])
            ca, cb = shift(a[::-1], k), shift(b[::-1], k)
            wrong = [shift(b, k), shift(b[::-1], k + 1), b[::-1], shift(b[::-1], -k)]
            why = 'The word is written backwards, then each letter moves %d place%s forward. %s backwards is %s, which becomes %s.' % (k, '' if k == 1 else 's', b, b[::-1], cb)
        q = 'In a secret code, %s is written as %s. How is %s written?' % (a, ca, b)
        if add(band, 'code', q, cb, wrong, why):
            made += 1

# ---------------- directions ----------------
DIRS = ['North', 'East', 'South', 'West']


def gen_directions(band, want):
    made = 0; tries = 0
    names = ['Riya', 'Kabir', 'Anaya', 'Arjun', 'Meera', 'Vihaan', 'Zoya', 'Ishaan', 'Tara', 'Aarav', 'Diya', 'Reyansh', 'Saanvi', 'Neel', 'Kiara']
    while made < want and tries < want * 300:
        tries += 1
        nm = R.choice(names)
        face = R.randint(0, 3)
        steps = R.randint(1, 2) if band == 'j' else R.randint(2, 4)
        if band == 'j' or (band == 'm' and R.random() < .5):
            turns = [R.choice(['right', 'left']) for _ in range(steps)]
            f = face
            for t in turns:
                f = (f + (1 if t == 'right' else -1)) % 4
            q = '%s is facing %s. %s turns %s. Which way is %s facing now?' % (nm, DIRS[face], 'She' if nm in ('Riya', 'Anaya', 'Meera', 'Zoya', 'Tara', 'Diya', 'Saanvi', 'Kiara') else 'He',
                                                                              ', then '.join(turns), nm)
            ans = DIRS[f]
            why = 'A right turn moves one step clockwise (North → East → South → West); a left turn moves back. Starting at %s and turning %s ends at %s.' % (DIRS[face], ', '.join(turns), ans)
            if add(band, 'direction', q, ans, [d for d in DIRS if d != ans], why):
                made += 1
        else:
            x = y = 0; f = face; parts = []
            for i in range(steps):
                d = R.randint(2, 9)
                if i:
                    t = R.choice(['right', 'left']); f = (f + (1 if t == 'right' else -1)) % 4
                    parts.append('turns %s and walks %d m' % (t, d))
                else:
                    parts.append('walks %d m %s' % (d, DIRS[f]))
                x += [0, 1, 0, -1][f] * d; y += [1, 0, -1, 0][f] * d
            dist2 = x * x + y * y
            if band == 'm':
                if x != 0 and y != 0:
                    continue
                if dist2 == 0:
                    continue
                dist = int(math.isqrt(dist2))
                q = '%s %s. How far is %s from the starting point?' % (nm, ', then '.join(parts), nm)
                why = 'Draw it: the moves leave %s %d m %s of the start.' % (nm, dist, 'east' if x > 0 else 'west' if x < 0 else 'north' if y > 0 else 'south')
                if add(band, 'direction', q, '%d m' % dist, ['%d m' % v for v in near(dist, (1, 2, 3, 4)) if v > 0], why):
                    made += 1
            else:
                if math.isqrt(dist2) ** 2 != dist2 or x == 0 or y == 0:
                    continue
                dist = math.isqrt(dist2)
                q = '%s %s. How far is %s from the start, in a straight line?' % (nm, ', then '.join(parts), nm)
                why = '%s ends %d m %s and %d m %s of the start. By Pythagoras, √(%d² + %d²) = %d m.' % (nm, abs(x), 'east' if x > 0 else 'west', abs(y), 'north' if y > 0 else 'south', abs(x), abs(y), dist)
                if add(band, 'direction', q, '%d m' % dist, ['%d m' % (abs(x) + abs(y)), '%d m' % abs(abs(x) - abs(y)), '%d m' % (dist + 1), '%d m' % (dist - 1)], why):
                    made += 1

# ---------------- calendar, rank, ages, clocks ----------------
WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def gen_calendar(band, want):
    made = 0; tries = 0
    while made < want and tries < want * 300:
        tries += 1
        d0 = R.randint(0, 6)
        n = R.randint(1, 6) if band == 'j' else R.randint(8, 40) if band == 'm' else R.randint(45, 200)
        ago = band != 'j' and R.random() < .35
        ans = WEEK[(d0 - n) % 7] if ago else WEEK[(d0 + n) % 7]
        q = 'Today is %s. What day %s %d day%s %s?' % (WEEK[d0], 'was it' if ago else 'will it be', n, '' if n == 1 else 's', 'ago' if ago else 'from today')
        rem = n % 7
        why = ('%d days is %d full week%s and %d extra day%s. ' % (n, n // 7, '' if n // 7 == 1 else 's', rem, '' if rem == 1 else 's') if n >= 7 else '') + \
              'Count %s %d from %s: %s.' % ('back' if ago else 'on', rem, WEEK[d0], ans)
        if add(band, 'calendar', q, ans, [w for w in R.sample(WEEK, 7) if w != ans], why):
            made += 1


def gen_rank(band, want):
    made = 0; tries = 0
    names = ['Aman', 'Pooja', 'Rahul', 'Sneha', 'Farhan', 'Nisha', 'Karan', 'Ananya', 'Dev', 'Ira']
    while made < want and tries < want * 300:
        tries += 1
        nm = R.choice(names)
        if band == 'm' or R.random() < .5:
            total = R.randint(10, 45); left = R.randint(2, total - 1)
            right = total - left + 1
            q = 'In a line of %d children, %s is %s from the front. What is %s’s place from the back?' % (total, nm, ordinal(left), nm)
            why = 'Front place + back place = total + 1. So %d + 1 − %d = %d.' % (total, left, right)
            if add(band, 'rank', q, ordinal(right), [ordinal(v) for v in (total - left, right + 1, total - left + 2, left) if v > 0], why):
                made += 1
        else:
            left = R.randint(5, 25); right = R.randint(5, 25)
            total = left + right - 1
            q = '%s is %s from the left and %s from the right in a row. How many people are in the row?' % (nm, ordinal(left), ordinal(right))
            why = '%s is counted from both sides, so total = %d + %d − 1 = %d.' % (nm, left, right, total)
            if add(band, 'rank', q, total, [total + 1, total + 2, total - 1, left + right - 2], why):
                made += 1


def ordinal(n):
    s = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return '%d%s' % (n, s)


def gen_ages(band, want):
    made = 0; tries = 0
    pairs = [('Ravi', 'Sita'), ('Asha', 'Imran'), ('Vikram', 'Leela'), ('Nikhil', 'Fatima'), ('Pari', 'Om'), ('Jaya', 'Rohan')]
    while made < want and tries < want * 300:
        tries += 1
        a, b = R.choice(pairs)
        if band == 'j':
            ag = R.randint(4, 9); d = R.randint(1, 5); later = R.randint(1, 4)
            ans = ag + d + later
            q = '%s is %d year%s older than %s. %s is %d. How old will %s be in %d year%s?' % (a, d, '' if d == 1 else 's', b, b, ag, a, later, '' if later == 1 else 's')
            why = '%s is %d + %d = %d now. In %d year%s: %d + %d = %d.' % (a, ag, d, ag + d, later, '' if later == 1 else 's', ag + d, later, ans)
            if add(band, 'age', q, ans, [ag + d, ag + later, ans + 1, ans - 2], why):
                made += 1
        elif band == 'm':
            child = R.randint(5, 14); k = R.choice([2, 3, 4]); later = R.randint(2, 10)
            ans = child * k + later
            q = '%s’s mother is %d times as old as %s. %s is %d. How old will the mother be in %d years?' % (b, k, b, b, child, later)
            why = 'Mother is %d × %d = %d now, so in %d years she will be %d.' % (child, k, child * k, later, ans)
            if add(band, 'age', q, ans, [child * k, (child + later) * k, ans + later, ans - 1], why):
                made += 1
        else:
            # sum and difference
            y = R.randint(6, 30); d = R.randint(2, 20); x = y + d
            q = 'The ages of %s and %s add up to %d. %s is %d years older. How old is %s?' % (a, b, x + y, a, d, b)
            why = 'Take away the difference: %d − %d = %d, and share it equally: %d ÷ 2 = %d.' % (x + y, d, 2 * y, 2 * y, y)
            if add(band, 'age', q, y, [x, (x + y) // 2, y + 1, y - 2], why):
                made += 1


def gen_clock(band, want):
    made = 0; tries = 0
    while made < want and tries < want * 300:
        tries += 1
        h = R.randint(1, 12); m = R.choice([0, 10, 15, 20, 30, 40, 45, 50])
        ang = abs(30 * (h % 12) - 5.5 * m)
        ang = min(ang, 360 - ang)
        if ang != int(ang):
            continue
        ang = int(ang)
        q = 'What is the smaller angle between the hour hand and the minute hand at %d:%02d?' % (h, m)
        why = 'Hour hand: 30° × %d + 0.5° × %d = %s°. Minute hand: 6° × %d = %d°. The gap is %d°.' % (h % 12, m, fmt(30 * (h % 12) + .5 * m), m, 6 * m, ang)
        naive = abs(30 * (h % 12) - 6 * m); naive = min(naive, 360 - naive)
        wrong = ['%d°' % w for w in (naive, ang + 10, ang + 5, ang - 5, ang + 15, 360 - ang) if 0 <= w <= 360 and w != ang]
        if add(band, 'clock', q, '%d°' % ang, wrong, why):
            made += 1


def fmt(x):
    return str(int(x)) if x == int(x) else str(x)

# ---------------- number grids ----------------


def gen_grid(band, want):
    made = 0; tries = 0
    while made < want and tries < want * 400:
        tries += 1
        rule = R.choice(['sum', 'prod', 'diff'] if band == 's' else ['sum', 'diff'] if band == 'm' else ['sum'])
        rows = []
        for i in range(3):
            a = R.randint(1, 9 if band == 'j' else 20); b = R.randint(1, 9 if band == 'j' else 15)
            c = {'sum': a + b, 'prod': a * b, 'diff': abs(a - b)}[rule]
            if rule == 'diff' and a < b:
                a, b = b, a
            rows.append([a, b, c])
        if len({tuple(r) for r in rows}) < 3:
            continue
        # check other rules don't also fit rows 1 and 2 and predict differently
        alts = {'sum': lambda a, b: a + b, 'prod': lambda a, b: a * b, 'diff': lambda a, b: a - b, 'twice': lambda a, b: 2 * a + b, 'sq': lambda a, b: a * a + b, 'plus1': lambda a, b: a + b + 1}
        preds = set()
        for f in alts.values():
            if all(f(r[0], r[1]) == r[2] for r in rows[:2]):
                preds.add(f(rows[2][0], rows[2][1]))
        ans = rows[2][2]
        if preds != {ans}:
            continue
        sym = {'sum': '+', 'prod': '×', 'diff': '−'}[rule]
        grid = '   '.join('[%d  %d  %d]' % tuple(r) for r in rows[:2]) + '   [%d  %d  ?]' % tuple(rows[2][:2])
        q = 'Find the missing number. Each row follows the same rule:  ' + grid
        why = 'In each row, the third number = first %s second (%d %s %d = %d). So %d %s %d = %d.' % (sym, rows[0][0], sym, rows[0][1], rows[0][2], rows[2][0], sym, rows[2][1], ans)
        if add(band, 'grid', q, ans, near(ans, (1, 2, 3, 4, 6)), why):
            made += 1

# ---------------- word analogies (hand-picked pairs, one clear link) ----------------
ANALOGY = [
    # (a, b, c, d, link, wrongs)
    ('Bird', 'Nest', 'Bee', 'Hive', 'where it lives', ['Honey', 'Flower', 'Sting']),
    ('Cow', 'Calf', 'Dog', 'Puppy', 'baby animal', ['Kitten', 'Bark', 'Kennel']),
    ('Hand', 'Glove', 'Foot', 'Sock', 'what covers it', ['Toe', 'Shoe lace', 'Knee']),
    ('Pen', 'Write', 'Knife', 'Cut', 'what it is used for', ['Sharp', 'Kitchen', 'Spoon']),
    ('Hot', 'Cold', 'Day', 'Night', 'opposite', ['Sun', 'Morning', 'Light']),
    ('Fish', 'Water', 'Camel', 'Desert', 'where it lives', ['Hump', 'Milk', 'Rope']),
    ('Teacher', 'School', 'Doctor', 'Hospital', 'place of work', ['Medicine', 'Patient', 'Nurse']),
    ('Petal', 'Flower', 'Page', 'Book', 'part of', ['Pen', 'Read', 'Letter']),
    ('Eye', 'See', 'Ear', 'Hear', 'what it does', ['Sound', 'Nose', 'Music']),
    ('Up', 'Down', 'Open', 'Close', 'opposite', ['Door', 'Wide', 'Start']),
    ('Lion', 'Roar', 'Snake', 'Hiss', 'its sound', ['Bite', 'Crawl', 'Poison']),
    ('Car', 'Road', 'Ship', 'Sea', 'where it moves', ['Sail', 'Port', 'Captain']),
    ('Baker', 'Bread', 'Potter', 'Pot', 'what they make', ['Clay', 'Wheel', 'Water']),
    ('Wool', 'Sheep', 'Silk', 'Silkworm', 'where it comes from', ['Cotton', 'Saree', 'Spider']),
    ('Week', 'Day', 'Year', 'Month', 'made up of', ['Calendar', 'Decade', 'Hour']),
    ('Thermometer', 'Temperature', 'Clock', 'Time', 'what it measures', ['Alarm', 'Hour hand', 'Wall']),
    ('Painter', 'Brush', 'Writer', 'Pen', 'tool used', ['Book', 'Story', 'Paper']),
    ('Seed', 'Plant', 'Egg', 'Chick', 'grows into', ['Nest', 'Hen', 'Shell']),
    ('Rain', 'Umbrella', 'Sun', 'Sunglasses', 'protects from', ['Hot', 'Sky', 'Summer']),
    ('Library', 'Books', 'Garage', 'Cars', 'what is kept there', ['Mechanic', 'Road', 'Petrol']),
    ('Kilogram', 'Mass', 'Litre', 'Volume', 'what it measures', ['Milk', 'Bottle', 'Length']),
    ('Pilot', 'Plane', 'Driver', 'Car', 'what they control', ['Road', 'Licence', 'Passenger']),
    ('Hungry', 'Eat', 'Tired', 'Rest', 'what you do about it', ['Sleepy', 'Run', 'Yawn']),
    ('Tree', 'Forest', 'Star', 'Galaxy', 'many make a', ['Moon', 'Shine', 'Night']),
    ('Fast', 'Slow', 'Heavy', 'Light', 'opposite', ['Weight', 'Strong', 'Big']),
    ('Kitchen', 'Cook', 'Bedroom', 'Sleep', 'what you do there', ['Bed', 'Pillow', 'Dream']),
    ('Ink', 'Pen', 'Lead', 'Pencil', 'what fills it', ['Eraser', 'Sharpener', 'Paper']),
    ('Finger', 'Hand', 'Toe', 'Foot', 'part of', ['Nail', 'Shoe', 'Leg']),
    ('Dentist', 'Teeth', 'Optician', 'Eyes', 'what they look after', ['Glasses', 'Ears', 'Hospital']),
    ('Train', 'Track', 'Boat', 'River', 'where it moves', ['Oar', 'Fish', 'Bridge']),
    ('Chapter', 'Book', 'Scene', 'Play', 'part of', ['Actor', 'Stage', 'Ticket']),
    ('Gold', 'Metal', 'Rose', 'Flower', 'kind of', ['Thorn', 'Red', 'Garden']),
    ('Cub', 'Lion', 'Kid', 'Goat', 'baby of', ['Horn', 'Lamb', 'Grass']),
    ('Spider', 'Web', 'Bird', 'Nest', 'what it builds', ['Feather', 'Egg', 'Tree']),
    ('Ocean', 'Salty', 'Sugar', 'Sweet', 'how it tastes', ['White', 'Tea', 'Salt']),
    ('Captain', 'Team', 'Principal', 'School', 'leads a', ['Teacher', 'Student', 'Office']),
    ('Cold', 'Shiver', 'Hot', 'Sweat', 'body’s reaction', ['Summer', 'Fan', 'Fire']),
    ('Grape', 'Raisin', 'Plum', 'Prune', 'dried form', ['Juice', 'Seed', 'Jam']),
    ('Brick', 'Wall', 'Word', 'Sentence', 'builds a', ['Letter', 'Book', 'Read']),
    ('Compass', 'Direction', 'Ruler', 'Length', 'what it shows', ['Line', 'Scale', 'Pencil']),
    ('Morning', 'Breakfast', 'Night', 'Dinner', 'meal at that time', ['Lunch', 'Moon', 'Sleep']),
    ('Glove', 'Hand', 'Helmet', 'Head', 'protects the', ['Bike', 'Hair', 'Safety']),
    ('Wheat', 'Flour', 'Grapes', 'Juice', 'made into', ['Vine', 'Green', 'Seed']),
    ('Doctor', 'Stethoscope', 'Carpenter', 'Saw', 'tool used', ['Wood', 'Table', 'Nail polish']),
    ('Bee', 'Honey', 'Cow', 'Milk', 'gives us', ['Grass', 'Calf', 'Farm']),
    ('Moon', 'Earth', 'Earth', 'Sun', 'goes around', ['Mars', 'Moon', 'Sky']),
]


def gen_analogy(band, want):
    made = 0
    items = ANALOGY[:]
    R.shuffle(items)
    for a, b, c, d, link, wr in items:
        if made >= want:
            break
        q = '%s is to %s as %s is to ___?' % (a, b, c)
        why = 'The link is “%s”: %s → %s, so %s → %s.' % (link, a, b, c, d)
        if add(band, 'analogy', q, d, wr, why):
            made += 1

# ---------------- build ----------------


def main():
    plan = {
        'j': [(gen_pictures, 70), (gen_series, 55), (gen_odd_numbers, 30), (lambda b, n: gen_odd_words(b, n, True), 35), (lambda b, n: gen_odd_words(b, n), 25),
              (gen_machine, 25), (gen_letters, 20), (gen_codes, 15), (gen_directions, 20), (gen_calendar, 15), (gen_ages, 15), (gen_grid, 15), (gen_analogy, 0)],
        'm': [(gen_series, 70), (gen_pictures, 20), (gen_odd_numbers, 40), (lambda b, n: gen_odd_words(b, n), 35), (gen_machine, 40), (gen_letters, 30),
              (gen_codes, 30), (gen_directions, 30), (gen_calendar, 20), (gen_rank, 20), (gen_ages, 20), (gen_grid, 25), (gen_analogy, 25)],
        's': [(gen_series, 80), (gen_odd_numbers, 45), (gen_machine, 45), (gen_letters, 35), (gen_codes, 40), (gen_directions, 25), (gen_calendar, 20),
              (gen_rank, 20), (gen_ages, 25), (gen_clock, 25), (gen_grid, 30), (gen_analogy, 25)],
    }
    # juniors get analogies with simple words too
    for band, jobs in plan.items():
        for f, n in jobs:
            before = len(QS)
            f(band, n)
            got = len(QS) - before
            if got < n:
                print('note: %s %s made %d of %d' % (band, getattr(f, '__name__', 'job'), got, n), file=sys.stderr)
    verify()
    for i, q in enumerate(QS):
        q['id'] = 'iq-%s-%04d' % (q['b'], i + 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({'test': 'iq', 'v': 1, 'questions': QS}, fh, ensure_ascii=False, separators=(',', ':'))
    from collections import Counter
    print('total', len(QS), dict(Counter(q['b'] for q in QS)))


def verify():
    """second, independent check of every question"""
    seen = set()
    for q in QS:
        assert len(q['o']) == 4 and len(set(q['o'])) == 4, q
        assert 0 <= q['a'] < 4, q
        assert q['q'] not in seen or True
        k = (q['b'], q['q'], tuple(sorted(q['o'])))
        assert k not in seen, q
        seen.add(k)
        right = q['o'][q['a']]
        if q['k'] == 'series':
            t = [int(x) for x in q['q'].split('?')[1].replace(',  ?', '').split(',')] if False else None
            nums = [int(x) for x in q['q'].replace('What comes next?', '').replace('?', '').split(',') if x.strip()]
            p = series_rules(nums)
            assert p and all(Fraction(v) == Fraction(int(right)) for v in p.values()), q
            for w in q['o']:
                if w != right:
                    assert all(Fraction(v) != Fraction(int(w)) for v in p.values()), q
        if q['k'] == 'calendar':
            import re
            m = re.match(r'Today is (\w+)\. What day (was it|will it be) (\d+) days? (ago|from today)', q['q'])
            d0, n = WEEK.index(m.group(1)), int(m.group(3))
            assert WEEK[(d0 + (-n if m.group(4) == 'ago' else n)) % 7] == right, q
        if q['k'] == 'clock':
            import re
            h, mi = map(int, re.search(r'at (\d+):(\d+)', q['q']).groups())
            a = abs(30 * (h % 12) - 5.5 * mi); a = min(a, 360 - a)
            assert '%d°' % a == right, q
        if q['k'] == 'code':
            import re
            m = re.match(r'In a secret code, (\w+) is written as (\w+)\. How is (\w+) written', q['q'])
            a, ca, b = m.groups()
            fits = []
            for rev in (False, True):
                for k in range(-25, 26):
                    if shift(a[::-1] if rev else a, k) == ca:
                        fits.append(shift(b[::-1] if rev else b, k))
            assert set(fits) == {right}, (q, fits)
            for w in q['o']:
                if w != right:
                    assert w not in fits
        if q['k'] == 'rank':
            import re
            m = re.search(r'line of (\d+) children, \w+ is (\d+)\w\w from the front', q['q'])
            if m:
                assert right == ordinal(int(m.group(1)) - int(m.group(2)) + 1), q
            else:
                l, r = map(int, re.search(r'is (\d+)\w\w from the left and (\d+)\w\w from the right', q['q']).groups())
                assert right == str(l + r - 1), q


if __name__ == '__main__':
    main()
