#!/usr/bin/env python3
"""IQ picture-reasoning puzzles for Mind Gym (content/mind/pics.json).

Types: mirror image, water image, figure series, odd figure out, figure analogy, paper folding & punching,
counting figures, dice (opposite faces), figure matrix, symmetry completion.

Accuracy: every picture is built from the SAME shape table the app draws (written into the JSON), and every
option is drawn here on a 60x60 grid. A question is kept only if
  * the right answer is produced by the rule, and
  * every option looks clearly different from every other option (at least 2% of the picture differs), and
  * no other rule from a small library also fits and points to a different option (series, analogy),
  * for dice / matrix / paper / counting the answer is re-derived by brute force.
Bands: j = Grades 1-3, m = 4-8, s = 9-12 and CA.
"""
import json, math, os, random, itertools, sys

R = random.Random(42)
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'content', 'mind', 'pics.json')
COL = ['#ff5a5f', '#2b8cff', '#ffc43d', '#21b573', '#9b5cff', '#ff8a1f', '#00b8c7', '#ff4fa3']

# ---------- shapes (unit coordinates, y down) ----------
def ngon(n, r=1.0, rot=-90):
    return [(round(r * math.cos(math.radians(rot + 360 * i / n)), 3), round(r * math.sin(math.radians(rot + 360 * i / n)), 3)) for i in range(n)]
def star():
    p = []
    for i in range(10):
        r = 1 if i % 2 == 0 else 0.45; a = math.radians(-90 + 36 * i)
        p.append((round(r * math.cos(a), 3), round(r * math.sin(a), 3)))
    return p
def heart():
    p = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        x = 16 * math.sin(t) ** 3; y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        p.append((round(x / 17, 3), round(y / 17 + 0.1, 3)))
    return p
SHAPES = {
    'circ': ngon(28), 'sq': [(-.85, -.85), (.85, -.85), (.85, .85), (-.85, .85)], 'tri': [(0, -1), (.95, .8), (-.95, .8)],
    'star': star(), 'heart': heart(), 'dia': [(0, -1), (.75, 0), (0, 1), (-.75, 0)], 'hex': ngon(6, 1, 0),
    'arrow': [(0, -1), (.7, -.2), (.25, -.2), (.25, 1), (-.25, 1), (-.25, -.2), (-.7, -.2)],
    'flag': [(-.6, 1), (-.6, -1), (.85, -.55), (-.3, -.1), (-.3, 1)],
    'L': [(-.6, -1), (-.15, -1), (-.15, .5), (.75, .5), (.75, 1), (-.6, 1)],
    'semi': [(round(math.cos(math.radians(180 + 180 * i / 14)), 3), round(math.sin(math.radians(180 + 180 * i / 14)) + .4, 3)) for i in range(15)],
    'bolt': [(.2, -1), (-.55, .1), (-.05, .1), (-.25, 1), (.6, -.15), (.1, -.15), (.4, -1)],
}
CHIRAL = ['flag', 'L', 'bolt']
FUNNY = ['circ', 'sq', 'tri', 'star', 'heart', 'dia', 'hex', 'arrow', 'semi']

def el(s, x, y, z, r=0, c=0, fx=1, fy=1):
    return {'s': s, 'x': round(x, 2), 'y': round(y, 2), 'z': z, 'r': r % 360, 'c': c, 'fx': fx, 'fy': fy}
def mirror(F): return [dict(e, x=round(100 - e['x'], 2), r=(-e['r']) % 360, fx=-e['fx']) for e in F]
def water(F): return [dict(e, y=round(100 - e['y'], 2), r=(-e['r']) % 360, fy=-e['fy']) for e in F]
def rot(F, t):
    a = math.radians(t); out = []
    for e in F:
        dx, dy = e['x'] - 50, e['y'] - 50
        out.append(dict(e, x=round(50 + dx * math.cos(a) - dy * math.sin(a), 2), y=round(50 + dx * math.sin(a) + dy * math.cos(a), 2), r=(e['r'] + t) % 360))
    return out
def recol(F, m): return [dict(e, c=m.get(e['c'], e['c'])) for e in F]

N = 60
def pip(px, py, poly):
    ins = False; j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi: ins = not ins
        j = i
    return ins
def raster(F):
    g = [[-1] * N for _ in range(N)]
    for e in F:
        a = math.radians(e['r']); ca, sa = math.cos(a), math.sin(a)
        poly = []
        for (px, py) in SHAPES[e['s']]:
            x, y = px * e['fx'] * e['z'], py * e['fy'] * e['z']
            poly.append((e['x'] + x * ca - y * sa, e['y'] + x * sa + y * ca))
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        for i in range(max(0, int(min(ys) * N / 100) - 1), min(N, int(max(ys) * N / 100) + 2)):
            for k in range(max(0, int(min(xs) * N / 100) - 1), min(N, int(max(xs) * N / 100) + 2)):
                if pip((k + .5) * 100 / N, (i + .5) * 100 / N, poly): g[i][k] = e['c']
    return g
def diff(a, b): return sum(1 for i in range(N) for k in range(N) if a[i][k] != b[i][k])
MIN = int(N * N * 0.02)
def distinct(figs):
    rs = [raster(f) for f in figs]
    return all(diff(rs[i], rs[j]) >= MIN for i in range(len(rs)) for j in range(i + 1, len(rs)))
def same(a, b): return diff(raster(a), raster(b)) < MIN // 3
def inside(F): return all(8 <= e['x'] <= 92 and 8 <= e['y'] <= 92 for e in F)

def figure(band, n=None):
    n = n or {'j': R.randint(2, 3), 'm': R.randint(3, 4), 's': R.randint(4, 5)}[band]
    spots = [(28, 28), (72, 28), (28, 72), (72, 72), (50, 50), (50, 22), (22, 50), (78, 50), (50, 78)]
    R.shuffle(spots); F = []
    cols = R.sample(range(len(COL)), min(n, len(COL)))
    for i in range(n):
        s = R.choice(CHIRAL if i == 0 else FUNNY + CHIRAL)
        F.append(el(s, spots[i][0] + R.uniform(-4, 4), spots[i][1] + R.uniform(-4, 4), {'j': 16, 'm': 14, 's': 12}[band], R.choice([0, 90, 180, 270, 45]) if band == 's' else R.choice([0, 90, 180, 270]), cols[i % len(cols)]))
    return F

QS, SEEN = [], set()
def add(band, kind, q, opts, a, why, extra):
    key = json.dumps([band, kind, extra.get('stem'), opts], sort_keys=True)
    if key in SEEN: return False
    SEEN.add(key)
    order = list(range(len(opts))); R.shuffle(order)
    QS.append(dict({'b': band, 'k': kind, 'q': q, 'o': [opts[i] for i in order], 'a': order.index(a), 'why': why}, **extra))
    return True

# ---------- 1 mirror / water ----------
def gen_mirror(band, n, water_kind=False):
    made = 0; tries = 0
    while made < n and tries < n * 60:
        tries += 1
        F = figure(band)
        ans = water(F) if water_kind else mirror(F)
        wrong = [mirror(F) if water_kind else water(F), rot(F, 180), F if band != 'j' else rot(F, 90)]
        if not distinct([ans] + wrong): continue
        if water_kind:
            q = 'Which picture is the WATER image (reflection in a lake below the picture)?'
            why = 'In water the picture turns upside down: top goes to the bottom, but left and right stay the same.'
        else:
            q = 'Which picture shows how this looks in a MIRROR placed on its right?'
            why = 'A mirror swaps left and right: shapes on the left move to the right and face the other way. Top and bottom stay the same.'
        if add(band, 'water' if water_kind else 'mirror', q, [ans] + wrong, 0, why, {'stem': F, 'mode': 'water' if water_kind else 'mirror'}): made += 1

# ---------- 2 figure series (turning) ----------
def gen_series(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 80:
        tries += 1
        F = figure(band, {'j': 2, 'm': 3, 's': 4}[band])
        t = R.choice([90, -90] if band != 's' else [45, -45, 90, -90, 135])
        frames = [rot(F, t * k) for k in range(5)]
        if not distinct(frames[:4]): continue
        ans = frames[4]
        wrong = [rot(F, t * 3), rot(F, t * 5), mirror(ans)]
        if not distinct([ans] + wrong): continue
        # the other direction must not fit the shown frames
        if all(same(rot(F, -t * k), frames[k]) for k in range(1, 4)): continue
        dirw = 'clockwise' if t > 0 else 'anticlockwise'
        if add(band, 'series', 'The picture keeps turning. What comes next?', [ans] + wrong, 0,
               'Each step the whole picture turns %d° %s. Turn it once more to get the next one.' % (abs(t), dirw), {'stem': frames[:4], 'turn': t}): made += 1

# ---------- 3 odd figure out ----------
def gen_odd(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 80:
        tries += 1
        F = figure(band, {'j': 2, 'm': 3, 's': 3}[band])
        rots = [rot(F, a) for a in (0, 90, 180, 270)]
        if not distinct(rots): continue
        M = mirror(F)
        if any(same(rot(M, a), F) for a in (0, 90, 180, 270)): continue          # odd must truly be different
        pick = R.sample([0, 90, 180, 270], 4)
        same3 = [rot(F, a) for a in pick[:3]]; odd = rot(M, pick[3])
        if add(band, 'odd', 'Three of these are the SAME picture, just turned. Which one is the odd one out?', same3 + [odd], 3,
               'Turn the pictures in your mind: three match after turning. The odd one is a mirror image — no amount of turning makes it match.', {}): made += 1

# ---------- 4 figure analogy ----------
TRANS = [('mirror', mirror, 'is flipped left-to-right'), ('water', water, 'is flipped upside down'), ('r90', lambda f: rot(f, 90), 'turns 90° clockwise'),
         ('r180', lambda f: rot(f, 180), 'turns half a circle'), ('rm90', lambda f: rot(f, -90), 'turns 90° anticlockwise')]
def gen_analogy(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 80:
        tries += 1
        A = figure(band, {'j': 2, 'm': 2, 's': 3}[band]); C = figure(band, {'j': 2, 'm': 2, 's': 3}[band])
        name, f, words = R.choice(TRANS[:3] if band == 'j' else TRANS)
        B, ans = f(A), f(C)
        fits = [g for _, g, _ in TRANS if same(g(A), B)]
        if any(not same(g(C), ans) for g in fits): continue
        wrong = [g(C) for nm, g, _ in TRANS if nm != name]
        wrong = [w for w in wrong if not same(w, ans)][:2] + [C]
        if len(wrong) < 3 or not distinct([ans] + wrong): continue
        if add(band, 'analogy', 'The first picture changes into the second. Change the third picture the SAME way. Which is it?', [ans] + wrong, 0,
               'The first picture %s. Do exactly that to the third picture.' % words, {'stem': [A, B, C]}): made += 1

# ---------- 5 paper folding and punching (grid 4x4) ----------
G = 4
def unfold(holes, folds):
    hs = set(holes)
    for f in reversed(folds):
        new = set(hs)
        for (r, c) in hs:
            if f == 'v': new.add((r, G - 1 - c))
            if f == 'h': new.add((G - 1 - r, c))
            if f == 'd': new.add((c, r))
        hs = new
    return sorted(hs)
def folded_region(folds):
    cells = {(r, c) for r in range(G) for c in range(G)}
    for f in folds:
        if f == 'v': cells = {x for x in cells if x[1] >= G // 2}          # left half folded onto right
        if f == 'h': cells = {x for x in cells if x[0] >= G // 2}          # top folded onto bottom
        if f == 'd': cells = {x for x in cells if x[0] >= x[1]}            # top-right triangle onto bottom-left
    return sorted(cells)
def gen_paper(band, n):
    made = 0; tries = 0
    seqs = {'j': [['v'], ['h']], 'm': [['v'], ['h'], ['v', 'h'], ['h', 'v']], 's': [['v', 'h'], ['h', 'v'], ['d'], ['v', 'd'], ['h', 'd']]}[band]
    while made < n and tries < n * 80:
        tries += 1
        folds = R.choice(seqs); reg = folded_region(folds)
        if 'd' in folds: reg = [x for x in reg if x[0] != x[1]] or reg            # keep holes off the diagonal fold line
        k = 1 if band == 'j' else R.randint(1, 2)
        holes = R.sample(reg, min(k, len(reg)))
        ans = unfold(holes, folds)
        moved = sorted({(min(G - 1, r + 1), c) for (r, c) in ans})
        pool = [sorted(holes), unfold(holes, ['h' if f == 'v' else 'v' if f == 'h' else 'v' for f in folds]), unfold(holes, ['d']), unfold(holes, ['v', 'h']),
                sorted(set(ans) - {ans[-1]}), moved]
        wrong = []
        for w in pool:
            if w and w != ans and w not in wrong: wrong.append(w)
        if len(wrong) < 3: continue
        wrong = wrong[:3]
        opts = [ans] + wrong
        nf = len(folds)
        why = 'Unfold step by step: every fold makes a matching hole on the other side of the fold line, like a mirror. %d hole%s punched → %d hole%s when opened.' % (len(holes), '' if len(holes) == 1 else 's', len(ans), '' if len(ans) == 1 else 's')
        if add(band, 'paper', 'A square paper is folded%s and punched. What does it look like when opened?' % (' twice' if nf == 2 else ''), [[list(x) for x in o] for o in opts], 0, why,
               {'folds': folds, 'holes': [list(h) for h in holes]}): made += 1

# ---------- 6 counting figures ----------
def squares_in(w, h):
    out = []
    for s in range(1, min(w, h) + 1):
        for x in range(w - s + 1):
            for y in range(h - s + 1): out.append([x, y, s, s])
    return out
def rects_in(w, h):
    return [[x1, y1, x2 - x1, y2 - y1] for x1, x2 in itertools.combinations(range(w + 1), 2) for y1, y2 in itertools.combinations(range(h + 1), 2)]
def fan_triangles(m, hl):
    """triangle with apex, base split into m parts by lines from the apex, crossed by hl lines parallel to the base"""
    levels = [(i + 1) / (hl + 1) for i in range(hl + 1)]               # fraction of height for each base-parallel line (incl. base)
    tris = []
    for i, j in itertools.combinations(range(m + 1), 2):
        for L in levels: tris.append([i / m, j / m, L])
    return tris
def gen_count(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 50:
        tries += 1
        kind = R.choice({'j': ['sq', 'tri'], 'm': ['sq', 'rect', 'tri'], 's': ['sq', 'rect', 'tri', 'tri']}[band])
        if kind == 'sq':
            w, h = (R.randint(2, 3), R.randint(1, 3)) if band == 'j' else (R.randint(2, 4), R.randint(2, 4))
            items = squares_in(w, h); ans = len(items)
            naive = w * h
            q = 'How many squares can you find in this picture? (Count big ones too!)'
            why = 'Small squares: %d. Then look for bigger squares made of 2×2%s small squares. Total = %d.' % (naive, ', 3×3' if min(w, h) >= 3 else '', ans)
            extra = {'grid': [w, h], 'find': 'sq', 'items': items}
        elif kind == 'rect':
            w, h = R.randint(2, 4), R.randint(1, 3)
            items = rects_in(w, h); ans = len(items); naive = w * h
            q = 'How many rectangles are in this picture? (Squares count as rectangles too.)'
            why = 'Pick any 2 of the %d upright lines and any 2 of the %d flat lines: %d × %d = %d rectangles.' % (w + 1, h + 1, (w + 1) * w // 2, (h + 1) * h // 2, ans)
            extra = {'grid': [w, h], 'find': 'rect', 'items': items}
        else:
            m, hl = (R.randint(2, 3), 0) if band == 'j' else (R.randint(2, 4), R.randint(0, 2 if band == 's' else 1))
            items = fan_triangles(m, hl); ans = len(items); naive = m * (hl + 1)
            q = 'How many triangles are in this picture?'
            why = 'Along each flat line there are %d triangles (1+2+…+%d), and there are %d flat line%s. %d × %d = %d.' % (m * (m + 1) // 2, m, hl + 1, '' if hl == 0 else 's', m * (m + 1) // 2, hl + 1, ans)
            extra = {'fan': [m, hl], 'find': 'tri', 'items': items}
        if len(extra['items']) > 60: continue
        wrong = list(dict.fromkeys([naive, ans - 1, ans + 1, ans + 2, ans - 2]))
        wrong = [w for w in wrong if w != ans and w > 0][:3]
        if add(band, 'count', q, [str(ans)] + [str(w) for w in wrong], 0, why, dict(extra, stem=[kind, extra.get('grid') or extra.get('fan')])): made += 1

# ---------- 7 dice: which number is opposite? ----------
FACES = ['U', 'D', 'F', 'B', 'L', 'Rt']
OPP = {'U': 'D', 'D': 'U', 'F': 'B', 'B': 'F', 'L': 'Rt', 'Rt': 'L'}
def rotations():
    def rx(d): return {'U': d['F'], 'F': d['D'], 'D': d['B'], 'B': d['U'], 'L': d['L'], 'Rt': d['Rt']}
    def ry(d): return {'U': d['U'], 'D': d['D'], 'F': d['Rt'], 'Rt': d['B'], 'B': d['L'], 'L': d['F']}
    def rz(d): return {'F': d['F'], 'B': d['B'], 'U': d['L'], 'Rt': d['U'], 'D': d['Rt'], 'L': d['D']}
    start = {f: f for f in FACES}; seen = {}; stack = [start]
    while stack:
        d = stack.pop(); k = tuple(d[f] for f in FACES)
        if k in seen: continue
        seen[k] = d; stack += [rx(d), ry(d), rz(d)]
    return list(seen.values())
ROTS = rotations(); assert len(ROTS) == 24
def views_of(die):
    return {(die[r['U']], die[r['F']], die[r['Rt']]) for r in ROTS}
ALL_DICE = [dict(zip(FACES, p)) for p in itertools.permutations(range(1, 7))]
def gen_dice(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 200:
        tries += 1
        die = R.choice(ALL_DICE)
        vs = list(views_of(die)); v1, v2 = R.sample(vs, 2)
        if len(set(v1) & set(v2)) != 1 and band == 'm': continue
        if len(set(v1) & set(v2)) == 0: continue
        cons = [d for d in ALL_DICE if v1 in views_of(d) and v2 in views_of(d)]
        shown = sorted(set(v1) | set(v2))
        asks = [x for x in shown if len({d[OPP[[f for f in FACES if d[f] == x][0]]] for d in cons}) == 1]
        if not asks: continue
        x = R.choice(asks)
        ans = {d[OPP[[f for f in FACES if d[f] == x][0]]] for d in cons}.pop()
        assert ans == die[OPP[[f for f in FACES if die[f] == x][0]]]
        wrong = [y for y in range(1, 7) if y not in (x, ans)]; R.shuffle(wrong)
        common = sorted(set(v1) & set(v2))
        why = ('%d is on both dice. Look at the faces around it: ' % common[0] if len(common) == 1 else 'Compare the two dice: ') + \
              'a number can never touch the number opposite it, so the number that is never next to %d is %d.' % (x, ans)
        if add(band, 'dice', 'Two views of the SAME dice. Which number is opposite %d?' % x, [str(ans)] + [str(w) for w in wrong[:3]], 0, why, {'views': [list(v1), list(v2)], 'stem': [x, sorted([v1, v2])]}): made += 1

# ---------- 8 figure matrix 3x3 (each row and column has every shape and colour once) ----------
def latin():
    base = [[(r + c) % 3 for c in range(3)] for r in range(3)]
    p = R.sample(range(3), 3); rows = R.sample(range(3), 3); cols = R.sample(range(3), 3)
    return [[p[base[rows[r]][cols[c]]] for c in range(3)] for r in range(3)]
def gen_matrix(band, n):
    made = 0; tries = 0
    while made < n and tries < n * 80:
        tries += 1
        S = latin(); C = latin()
        if len({(S[r][c], C[r][c]) for r in range(3) for c in range(3)}) != 9: continue     # orthogonal: every pair different
        shapes = R.sample(['circ', 'sq', 'tri', 'star', 'heart', 'dia', 'hex'], 3); cols = R.sample(range(len(COL)), 3)
        cnt = [1, 2, 3] if band != 'j' else [1, 1, 1]
        if band == 's': R.shuffle(cnt)
        mr, mc = R.randint(0, 2), R.randint(0, 2)
        cell = lambda s, c, k: {'s': shapes[s], 'c': cols[c], 'n': k}
        grid = [[cell(S[r][c], C[r][c], cnt[c]) for c in range(3)] for r in range(3)]
        ans = grid[mr][mc]
        cands = []
        for s in range(3):
            for c in range(3):
                for k in set(cnt): cands.append(cell(s, c, k))
        def ok(x):
            rs = [grid[mr][c] for c in range(3) if c != mc]; cs = [grid[r][mc] for r in range(3) if r != mr]
            return x['s'] not in [y['s'] for y in rs + cs] and x['c'] not in [y['c'] for y in rs + cs] and all(y['n'] == x['n'] for y in cs)
        good = [x for x in cands if ok(x)]
        if good != [ans] and not (len(good) == 1 and good[0] == ans): continue
        wrong = [dict(ans, s=shapes[(shapes.index(ans['s']) + 1) % 3]), dict(ans, c=cols[(cols.index(ans['c']) + 1) % 3])]
        wrong.append(dict(ans, n=ans['n'] % 3 + 1) if band != 'j' else dict(ans, s=shapes[(shapes.index(ans['s']) + 2) % 3], c=cols[(cols.index(ans['c']) + 2) % 3]))
        if any(ok(w) for w in wrong) or len({json.dumps(w, sort_keys=True) for w in [ans] + wrong}) < 4: continue
        g = [[None if (r, c) == (mr, mc) else grid[r][c] for c in range(3)] for r in range(3)]
        why = 'Every row and every column has each shape once and each colour once' + (', and each column keeps the same number of shapes.' if band != 'j' else '.') + ' Only one picture fits the empty box.'
        if add(band, 'matrix', 'Which picture fits in the empty box?', [ans] + wrong, 0, why, {'grid': g, 'stem': g}): made += 1

# ---------- 9 symmetry completion (6x6 tile, symmetric about both middle lines; one quarter missing) ----------
def gen_sym(band, n):
    made = 0; tries = 0
    H = 3
    while made < n and tries < n * 80:
        tries += 1
        cols = R.sample(range(len(COL)), 2)
        q0 = [[R.choice([-1, cols[0], cols[1]]) for _ in range(H)] for _ in range(H)]
        if sum(1 for r in q0 for x in r if x != -1) < 4: continue
        full = [[None] * 6 for _ in range(6)]
        for r in range(H):
            for c in range(H):
                v = q0[r][c]; full[r][c] = v; full[r][5 - c] = v; full[5 - r][c] = v; full[5 - r][5 - c] = v
        quad = R.choice([(0, 0), (0, 3), (3, 0), (3, 3)])
        part = lambda g, r0, c0: [[g[r0 + r][c0 + c] for c in range(H)] for r in range(H)]
        ans = part(full, *quad)
        flipH = [row[::-1] for row in ans]; flipV = ans[::-1]; turn = [list(x) for x in zip(*ans[::-1])]
        opts = [ans, flipH, flipV, turn]
        if len({json.dumps(o) for o in opts}) < 4: continue
        shown = [[None if quad[0] <= r < quad[0] + H and quad[1] <= c < quad[1] + H else full[r][c] for c in range(6)] for r in range(6)]
        if add(band, 'symmetry', 'This tile is the same on both sides of the dotted lines. Which piece completes it?', opts, 0,
               'Fold along the dotted lines in your mind: the missing piece is a mirror copy of the piece beside it.', {'tile': shown, 'hole': list(quad), 'stem': shown}): made += 1

PLAN = {
    'j': [(gen_mirror, 22), (lambda b, n: gen_mirror(b, n, True), 10), (gen_series, 18), (gen_odd, 14), (gen_analogy, 14), (gen_paper, 14), (gen_count, 9), (gen_matrix, 20), (gen_sym, 14)],
    'm': [(gen_mirror, 18), (lambda b, n: gen_mirror(b, n, True), 16), (gen_series, 18), (gen_odd, 16), (gen_analogy, 16), (gen_paper, 20), (gen_count, 18), (gen_dice, 18), (gen_matrix, 16), (gen_sym, 14)],
    's': [(gen_mirror, 16), (lambda b, n: gen_mirror(b, n, True), 14), (gen_series, 18), (gen_odd, 16), (gen_analogy, 18), (gen_paper, 20), (gen_count, 18), (gen_dice, 22), (gen_matrix, 16), (gen_sym, 14)],
}
if __name__ == '__main__':
    for b, jobs in PLAN.items():
        for f, n in jobs:
            k = len(QS); f(b, n)
            if len(QS) - k < n: print('note: %s %s %d/%d' % (b, getattr(f, '__name__', 'job'), len(QS) - k, n), file=sys.stderr)
    for i, q in enumerate(QS):
        q['id'] = 'pic-%s-%04d' % (q['b'], i + 1)
        if q['k'] not in ('mirror', 'water', 'series', 'analogy'): q.pop('stem', None)
    json.dump({'test': 'iq-pics', 'v': 1, 'shapes': SHAPES, 'colors': COL, 'questions': QS}, open(OUT, 'w'), separators=(',', ':'))
    from collections import Counter
    print(len(QS), Counter(q['b'] for q in QS), Counter(q['k'] for q in QS))
