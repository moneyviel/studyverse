"""Coordination-chemistry helpers: ligand data, oxidation state, d count, spin state (simple strong/weak-field
rules used in NCERT/JEE), unpaired electrons, CFSE, and stereoisomer counting by brute force over the
octahedron's (or square's) symmetry operations."""
import itertools, math
from dblock import d_count, Z3d
# name: (charge, denticity, field) — field 'strong' pairs electrons in 3d metals (CN-, CO, NO2-, en/NH3 for Co3+ d6 ...)
LIG = {'H2O': (0, 1, 'weak'), 'NH3': (0, 1, 'mid'), 'en': (0, 2, 'mid'), 'CN': (-1, 1, 'strong'), 'CO': (0, 1, 'strong'), 'NO2': (-1, 1, 'strong'), 'F': (-1, 1, 'weak'),
       'Cl': (-1, 1, 'weak'), 'Br': (-1, 1, 'weak'), 'I': (-1, 1, 'weak'), 'OH': (-1, 1, 'weak'), 'ox': (-2, 2, 'weak'), 'SCN': (-1, 1, 'weak'), 'PPh3': (0, 1, 'strong'), 'py': (0, 1, 'mid'),
       'EDTA': (-4, 6, 'mid'), 'gly': (-1, 2, 'mid'), 'acac': (-1, 2, 'weak'), 'NH2CH3': (0, 1, 'mid'), 'O': (-2, 1, 'weak'), 'C2O4': (-2, 2, 'weak'), 'dien': (0, 3, 'mid')}
SERIES = ['I', 'Br', 'SCN', 'Cl', 'F', 'OH', 'ox', 'H2O', 'NCS', 'EDTA', 'NH3', 'en', 'NO2', 'CN', 'CO']   # spectrochemical, weak → strong
def ox_state(charge, ligs):
    return charge - sum(LIG[l][0] * k for l, k in ligs.items())
def cn(ligs): return sum(LIG[l][1] * k for l, k in ligs.items())
def low_spin(metal, ox, ligs, geom='oct'):
    d = d_count(metal, ox) if metal in Z3d else None
    if metal not in Z3d: return True   # 4d/5d: always low spin
    if geom != 'oct': return False
    f = [LIG[l][2] for l in ligs]
    if 'strong' in f: return True
    if d == 6 and metal == 'Co' and ox == 3 and sum(k for l, k in ligs.items() if l in ('F', 'Cl', 'Br', 'I')) < 3: return True   # Co3+ d6 pairs with NH3, en, H2O, ox; [CoF6]3-, [CoF3(H2O)3] stay high spin
    return False
def unp_oct(d, ls):
    if ls: t = min(d, 6); e = d - t; return (t if t <= 3 else 6 - t) + (e if e <= 2 else 4 - e)
    return d if d <= 5 else 10 - d
def unp_tet(d):   # e (2) then t2 (3), always high spin
    order = [0, 1, 2, 3, 4]; occ = [0] * 5
    for k in range(d): occ[k % 5 if k < 5 else k - 5] += 1
    return sum(1 for o in occ if o == 1)
def unp_sq(d):   # square planar d8 → 0 (strong splitting, dx2-y2 empty)
    return 0 if d == 8 else (d if d <= 4 else 10 - d) if d < 8 else 10 - d
def cfse_oct(d, ls):   # in units of Δo (pairing energy ignored)
    if ls: t = min(d, 6); e = d - t
    else:
        occ = [0] * 5
        for k in range(d): occ[k % 5 if k < 5 else k - 5] += 1
        t = sum(occ[:3]); e = sum(occ[3:])
    return round(-0.4 * t + 0.6 * e, 2)
def cfse_tet(d):
    occ = [0] * 5
    for k in range(d): occ[k % 5 if k < 5 else k - 5] += 1
    e = sum(occ[:2]); t = sum(occ[2:]); return round((-0.6 * e + 0.4 * t) * 4 / 9, 3)   # in Δo units (Δt = 4/9 Δo)
def mu(n): return math.sqrt(n * (n + 2))

# ---- stereoisomers: positions on an octahedron ±x ±y ±z = 0..5 as (axis, sign)
POS = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]
def _rots():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3): m[i][perm[i]] = signs[i]
            det = round(_det(m)); mats.append((m, det))
    return mats
def _det(m): return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
OPS = _rots()
def _apply(m, p):
    v = [0, 0, 0]; v[p[0]] = p[1]; w = [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]
    ax = [i for i in range(3) if w[i]][0]; return POS.index((ax, w[ax]))
PERMS = [([_apply(m, POS[i]) for i in range(6)], det) for m, det in OPS]
def _cis(a, b): return POS[a][0] != POS[b][0]
def stereo(mono, bi=(), sym_bi=True):
    """mono: dict label → count; bi: list of bidentate labels (symmetric AA if sym_bi). returns (total stereoisomers, geometrical isomers)"""
    labels = []
    configs = set(); n_bi = len(bi)
    for bpos in itertools.permutations(range(6), 2 * n_bi):
        pairs = [tuple(sorted(bpos[2 * i:2 * i + 2])) for i in range(n_bi)]
        if not all(_cis(a, b) for a, b in pairs): continue
        rest = [i for i in range(6) if i not in bpos]
        ml = [l for l, k in mono.items() for _ in range(k)]
        for arr in set(itertools.permutations(ml)):
            cfg = {}
            for (a, b), lab in zip(pairs, bi): cfg[a] = cfg[b] = lab
            for i, lab in zip(rest, arr): cfg[i] = lab
            edges = frozenset((frozenset(pr), lab) for pr, lab in zip(pairs, bi))
            configs.add((tuple(cfg[i] for i in range(6)), edges))
    def img(c, perm):
        t, edges = c; nt = [None] * 6
        for i in range(6): nt[perm[i]] = t[i]
        ne = frozenset((frozenset(perm[x] for x in e), lab) for e, lab in edges); return (tuple(nt), ne)
    def canon(c, proper_only):
        return min((img(c, p)[0], tuple(sorted((tuple(sorted(e)), l) for e, l in img(c, p)[1]))) for p, det in PERMS if (det == 1 or not proper_only))
    total = len({canon(c, True) for c in configs}); geo = len({canon(c, False) for c in configs})
    return total, geo
def stereo_sq(mono):   # square planar: 4 positions; geometric only
    POS4 = [0, 1, 2, 3]; ml = [l for l, k in mono.items() for _ in range(k)]
    syms = [[(i + r) % 4 for i in range(4)] for r in range(4)] + [[(r - i) % 4 for i in range(4)] for r in range(4)]
    return len({min(tuple(arr[s.index(i)] for i in range(4)) for s in syms) for arr in set(itertools.permutations(ml))})
