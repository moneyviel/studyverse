"""Real JEE Main questions — Mathematics Unit 12: Vector Algebra. Our own solutions; chk re-solves each one
numerically — unknown vectors by solving the stated linear conditions (Gaussian elimination), parameters by
scanning for every root, and areas/volumes from cross and box products of the actual vectors. Skipped: items that
belong to 3D-geometry (filed in Unit 11) and items we could not read reliably."""
import math, itertools
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
S2, S3, S5, S6 = math.sqrt(2), math.sqrt(3), math.sqrt(5), math.sqrt(6)
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def addv(a, b, k=1): return tuple(x + k * y for x, y in zip(a, b))
def sc(k, a): return tuple(k * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(dot(a, a))
def box(a, b, c): return dot(a, cross(b, c))
def par(a, b): return nrm(cross(a, b)) < 1e-9 * max(1, nrm(a) * nrm(b))
def solve(rows, rhs):   # least-squares solve of an over-determined but consistent linear system (normal equations, Gauss)
    n = len(rows[0]); A = [[sum(r[i] * r[j] for r in rows) for j in range(n)] + [sum(r[i] * b for r, b in zip(rows, rhs))] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c: f = A[r][c] / A[c][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    x = [A[i][n] / A[i][i] for i in range(n)]
    assert all(abs(sum(a * xi for a, xi in zip(r, x)) - b) < 1e-7 * max(1, abs(b)) for r, b in zip(rows, rhs)), 'inconsistent'
    return tuple(x)
def crossrows(b):   # rows of the linear map c ↦ c × b
    return [(0, b[2], -b[1]), (-b[2], 0, b[0]), (b[1], -b[0], 0)]
def roots(f, lo, hi, n=20000):
    out = []; xs = [lo + (hi - lo) * k / n + 1.37e-5 for k in range(n + 1)]
    for a, b in zip(xs, xs[1:]):
        fa, fb = f(a), f(b)
        if fa * fb < 0:
            for _ in range(100):
                m = (a + b) / 2
                if f(a) * f(m) <= 0: b = m
                else: a = m
            out.append((a + b) / 2)
    return out
def P4(opts, v, tol=1e-6): return pick(opts, round(v, 9), tol)

# ---------- sheet 1
def _u1():
    n = cross(sub((2, -1, 2), (0, 0, 3)), sub((1, 2, -2), (0, 0, 3)))   # rows of (proj_u1 − proj_k, proj_u2 − proj_k) after ×3
    ops = [(-7, 9, 5), (7, 9, 5), (7, 9, -5), (-7, 9, -5)]; h = [i + 1 for i, o in enumerate(ops) if par(o, n)]; assert len(h) == 1; return h[0]
add(('2025', 'Apr', '2025-04-02', 1), 'dot', 'If a⃗ is a nonzero vector such that its projections on the vectors 2î − ĵ + 2k̂, î + 2ĵ − 2k̂ and k̂ are equal, then a unit vector along a⃗ is :', ['\\f{1}{√{155}}(−7î + 9ĵ + 5k̂)', '\\f{1}{√{155}}(7î + 9ĵ + 5k̂)', '\\f{1}{√{155}}(7î + 9ĵ − 5k̂)', '\\f{1}{√{155}}(−7î + 9ĵ − 5k̂)'], 2,
    _u1, ['Both vectors have length 3. With a⃗ = (x, y, z): \\f{2x − y + 2z}{3} = \\f{x + 2y − 2z}{3} = z.', 'So 2x − y − z = 0 and x + 2y − 5z = 0 → a⃗ ∥ (2, −1, −1) × (1, 2, −5) = (7, 9, 5).', 'Unit vector \\f{1}{√{155}}(7î + 9ĵ + 5k̂).'], 'dot', 2)
def _c3():
    a, b = (2, -3, 1), (3, 2, 5); R = (-18, -3, 12)   # (a − c) × b = R  ⇔  c × b = a × b − R
    rhs = list(sub(cross(a, b), R)) + [3]; c = solve(crossrows(b) + [a], rhs); return P4([18, 9, 12, 15], abs(dot(a, cross(b, c))))
add(('2025', 'Apr', '2025-04-02', 2), 'cross', 'Let a⃗ = 2î − 3ĵ + k̂, b⃗ = 3î + 2ĵ + 5k̂ and a vector c⃗ be such that (a⃗ − c⃗) × b⃗ = −18î − 3ĵ + 12k̂ and a⃗·c⃗ = 3. If b⃗ × c⃗ = d⃗, then |a⃗·d⃗| is equal to:', ['18', '9', '12', '15'], 4,
    _c3, ['a⃗·d⃗ = a⃗·(b⃗ × c⃗) = [a⃗ b⃗ c⃗] = c⃗·(a⃗ × b⃗).', 'a⃗ × b⃗ = (−17, −7, 13); (a⃗ − c⃗) × b⃗ = R gives c⃗ × b⃗ = (1, −4, 1), and with a⃗·c⃗ = 3 this fixes c⃗.', 'Then |c⃗·(a⃗ × b⃗)| = 15.'], 'cross', 3)
def _d4():
    a, b = (1, 1, 1), (3, 2, -1); out = set()
    for sgn in (1, -1):
        dh = sc(sgn / 3, sub(a, b))   # a × d̂ = b × d̂ ⇒ d̂ ∥ a − b, |a − b| = 3
        # c = (0, λ, μ): c ⟂ a and c·d̂ = 1
        lam, mu = solve([(1, 1), (dh[1], dh[2])], [0, 1]); c = (0, lam, mu); v = addv(sc(3 * lam, dh), sc(mu, c)); out.add(round(dot(v, v), 9))
    assert len(out) == 1; return round(out.pop())
add(('2025', 'Apr', '2025-04-03', 1), 'cross', 'Let a⃗ = î + ĵ + k̂, b⃗ = 3î + 2ĵ − k̂, c⃗ = λĵ + μk̂ and d̂ be a unit vector such that a⃗ × d̂ = b⃗ × d̂ and c⃗·d̂ = 1. If c⃗ is perpendicular to a⃗, then |3λd̂ + μc⃗|^{2} is equal to ______.', None, 5,
    _d4, ['(a⃗ − b⃗) × d̂ = 0 → d̂ = ±\\f{1}{3}(−2, −1, 2).', 'c⃗ ⟂ a⃗ → λ + μ = 0; c⃗·d̂ = ±μ = 1. Take d̂ = \\f{1}{3}(−2, −1, 2): μ = 1, λ = −1.', '3λd̂ + μc⃗ = (2, 1, −2) + (0, −1, 1) = (2, 0, −1) → 5 (the other sign gives the same).'], 'cross', 2)
def _d5():
    a, b, c = (1, 2, 1), (3, -3, 3), (2, -1, 2); u = sub(b, c)   # (b − c) × d = 0 ⇒ d = t(b − c)
    t = 4 / dot(a, u); d = sc(t, u); return round(dot(cross(a, d), cross(a, d)), 6)
add(('2025', 'Apr', '2025-04-03', 2), 'cross', 'Let a⃗ = î + 2ĵ + k̂, b⃗ = 3(î − ĵ + k̂), c⃗ = 2î − ĵ + 2k̂ and d⃗ be a vector such that b⃗ × d⃗ = c⃗ × d⃗ and a⃗·d⃗ = 4. Then |a⃗ × d⃗|^{2} is equal to ______.', None, 128,
    _d5, ['(b⃗ − c⃗) × d⃗ = 0 → d⃗ = t(1, −2, 1).', 'a⃗·d⃗ = t(1 − 4 + 1) = −2t = 4 → d⃗ = (−2, 4, −2).', 'a⃗ × d⃗ = (−8, 0, 8) → 128.'], 'cross', 2)
def _v6():
    u = (3, -1, 0); lam, = [l for l in roots(lambda l: dot(u, (2, 1, -l)) / (nrm(u) * nrm((2, 1, -l))) - S5 / (2 * math.sqrt(7)), 0, 50) if l > 0]
    v = (2, 1, -lam); v1 = sc(dot(v, u) / dot(u, u), u); v2 = sub(v, v1); return P4([14, 10, 12.5, 11.5], dot(v1, v1) + dot(v2, v2))
add(('2025', 'Apr', '2025-04-04', 1), 'dot', 'Consider two vectors u⃗ = 3î − ĵ and v⃗ = 2î + ĵ − λk̂, λ > 0. The angle between them is given by cos^{−1}(\\f{√{5}}{2√{7}}). Let v⃗ = v⃗_{1} + v⃗_{2}, where v⃗_{1} is parallel to u⃗ and v⃗_{2} is perpendicular to u⃗. Then the value |v⃗_{1}|^{2} + |v⃗_{2}|^{2} is equal to', ['14', '10', '\\f{25}{2}', '\\f{23}{2}'], 1,
    _v6, ['v⃗_{1} ⟂ v⃗_{2}, so |v⃗_{1}|^{2} + |v⃗_{2}|^{2} = |v⃗|^{2} = 5 + λ^{2}.', 'cos θ = \\f{5}{√{10}√{5 + λ^{2}}} = \\f{√{5}}{2√{7}} → 5 + λ^{2} = 14.'], 'dot', 2)
def _g8():
    A = (0, 0, 0); B = addv(A, (2, -1, 1)); C = addv(B, (1, -3, -5)); assert nrm(sub(sub(C, A), (3, -4, -4))) < 1e-12
    G = sc(1 / 3, addv(addv(A, B), C)); return round(6 * sum(dot(sub(X, G), sub(X, G)) for X in (A, B, C)), 6)
add(('2025', 'Apr', '2025-04-04', 2), 'dot', 'Let the three sides of a triangle ABC be given by the vectors 2î − ĵ + k̂, î − 3ĵ − 5k̂ and 3î − 4ĵ − 4k̂. Let G be the centroid of the triangle ABC. Then 6(|AG⃗|^{2} + |BG⃗|^{2} + |CG⃗|^{2}) is equal to ______.', None, 164,
    _g8, ['|AG|^{2} + |BG|^{2} + |CG|^{2} = \\f{1}{3}(a^{2} + b^{2} + c^{2}).', 'Side squares 6, 35, 41 → sum 82.', '6·\\f{82}{3} = 164.'], 'dot', 2)

# ---------- sheet 2
def _l9():
    lam, = [l for l in roots(lambda l: dot(addv((1, l, -3), (3, -1, 2)), sub((1, l, -3), (3, -1, 2))), 0, 50) if l > 0]
    a, b = (1, lam, -3), (3, -1, 2); return P4([25, 20, 50, 40], (14 * dot(a, b) / (nrm(a) * nrm(b))) ** 2)
add(('2024', 'Apr', '2024-04-04', 2), 'dot', 'If λ > 0, let θ be the angle between the vectors a⃗ = î + λĵ − 3k̂ and b⃗ = 3î − ĵ + 2k̂. If the vectors a⃗ + b⃗ and a⃗ − b⃗ are mutually perpendicular, then the value of (14 cos θ)^{2} is equal to', ['25', '20', '50', '40'], 1,
    _l9, ['(a⃗ + b⃗)·(a⃗ − b⃗) = |a⃗|^{2} − |b⃗|^{2} = 0 → 10 + λ^{2} = 14 → λ = 2.', 'cos θ = \\f{3 − 2 − 6}{14} = −\\f{5}{14} → (14 cos θ)^{2} = 25.'], 'dot', 1)
def _x10():
    a, b = (1, 1, 1), (2, 4, -5); x, = roots(lambda x: dot(a, addv(b, (x, 2, 3))) / nrm(addv(b, (x, 2, 3))) - 1, -50, 50)
    return P4([9, 6, 3, 11], box(a, b, (x, 2, 3)))
add(('2024', 'Apr', '2024-04-04', 2), 'cross', 'Let a⃗ = î + ĵ + k̂, b⃗ = 2î + 4ĵ − 5k̂ and c⃗ = xî + 2ĵ + 3k̂, x ∈ ℝ. If d⃗ is the unit vector in the direction of b⃗ + c⃗ such that a⃗·d⃗ = 1, then (a⃗ × b⃗)·c⃗ is equal to', ['9', '6', '3', '11'], 4,
    _x10, ['b⃗ + c⃗ = (2 + x, 6, −2); a⃗·(b⃗ + c⃗) = |b⃗ + c⃗|: (x + 6)^{2} = (x + 2)^{2} + 40 → x = 1.', 'a⃗ × b⃗ = (−9, 7, 2); ·(1, 2, 3) = 11.'], 'cross', 2)
def _c11():
    sols = []
    for z in roots(lambda z: (1 + z) ** 2 + ((1.5 - 2 * (1 + z) + z) / 2) ** 2 + z * z - 1, -2, 2):
        C = (1 + z, (1.5 - 2 * (1 + z) + z) / 2, z); assert abs(dot(C, (2, 2, -1)) / 3 - 0.5) < 1e-9 and abs(dot(C, (1, 0, -1)) / S2 - S2 / 2) < 1e-9
        sols.append(addv(C, (-0.5, 1 / (3 * S2), -S2 / 3)))
    ops = [(-S2 / 3, S2 / 3, 0.5 + 2 * S2 / 3), (S2 / 3, 1 / (3 * S2), -0.5), (1 / S3 + 0.5, 1 / S3 - 1 / (3 * S2), 1 / S3 + S2 / 3), (S2 / 3, 0, -0.5)]
    h = [i + 1 for i, o in enumerate(ops) if any(nrm(sub(o, s)) < 1e-9 for s in sols)]; assert len(h) == 1; return h[0]
add(('2024', 'Apr', '2024-04-04', 1), 'dot', 'Let a unit vector which makes an angle of 60° with 2î + 2ĵ − k̂ and an angle of 45° with î − k̂ be C⃗. Then C⃗ + (−\\f{1}{2}î + \\f{1}{3√{2}}ĵ − \\f{√{2}}{3}k̂) is :', ['−\\f{√{2}}{3}î + \\f{√{2}}{3}ĵ + (\\f{1}{2} + \\f{2√{2}}{3})k̂', '\\f{√{2}}{3}î + \\f{1}{3√{2}}ĵ − \\f{1}{2}k̂', '(\\f{1}{√{3}} + \\f{1}{2})î + (\\f{1}{√{3}} − \\f{1}{3√{2}})ĵ + (\\f{1}{√{3}} + \\f{√{2}}{3})k̂', '\\f{√{2}}{3}î − \\f{1}{2}k̂'], 4,
    _c11, ['C⃗ = (x, y, z): 2x + 2y − z = \\f{3}{2}, x − z = 1, x^{2} + y^{2} + z^{2} = 1.', 'Two unit vectors fit; one is (\\f{1}{2} + \\f{√{2}}{3}, −\\f{1}{3√{2}}, −\\f{1}{2} + \\f{√{2}}{3}).', 'Adding the given vector: \\f{√{2}}{3}î − \\f{1}{2}k̂ (the other solution matches no option).'], 'dot', 3)
def _s12():
    AB = (1, 2, -7); d, = [d for d in roots(lambda d: nrm(cross(AB, (6, d, -2))) / 2 - 15 * S2, -50, 50) if d > 0]
    AC = (6, d, -2); BC = sub(AC, AB); return round(max(dot(v, v) for v in (AB, BC, AC)), 6)
add(('2024', 'Apr', '2024-04-04', 1), 'cross', 'Let ABC be a triangle of area 15√{2} and the vectors AB⃗ = î + 2ĵ − 7k̂, BC⃗ = aî + bĵ + ck̂ and AC⃗ = 6î + dĵ − 2k̂, d > 0. Then the square of the length of the largest side of the triangle ABC is', None, 54,
    _s12, ['AB⃗ × AC⃗ = (7d − 4, −40, d − 12); area condition |…|^{2} = 1800 → 5d^{2} − 8d − 4 = 0 → d = 2.', 'AB^{2} = 54, AC^{2} = 44, BC⃗ = (5, 0, 5) → 50.', 'Largest: 54.'], 'cross', 2)
def _c13():
    a, b = (2, 5, -1), (2, -2, 2); i = (1, 0, 0); u = addv(addv(sc(2, a), b), i)   # (c + i) × (2a + b + i) = 0
    t, = roots(lambda t: dot(a, sub(sc(t, u), i)) + 29, -50, 50); c = sub(sc(t, u), i); return P4([10, 5, 15, 12], dot(c, (-2, 1, 1)))
add(('2024', 'Apr', '2024-04-05', 2), 'cross', 'Let a⃗ = 2î + 5ĵ − k̂, b⃗ = 2î − 2ĵ + 2k̂ and c⃗ be three vectors such that (c⃗ + î) × (a⃗ + b⃗ + î) = a⃗ × (c⃗ + î). If a⃗·c⃗ = −29, then c⃗·(−2î + ĵ + k̂) is equal to :', ['10', '5', '15', '12'], 2,
    _c13, ['Put w⃗ = c⃗ + î: w⃗ × (a⃗ + b⃗ + î) + w⃗ × a⃗ = 0 → w⃗ ∥ 2a⃗ + b⃗ + î = (7, 8, 0).', 'c⃗ = (7t − 1, 8t, 0); a⃗·c⃗ = 54t − 2 = −29 → t = −\\f{1}{2}, c⃗ = (−\\f{9}{2}, −4, 0).', 'c⃗·(−2, 1, 1) = 9 − 4 = 5.'], 'cross', 3)
def _m14():
    best = min(27 * ((2 / (3 * math.sin(al))) ** 2 + 4) for al in [k / 100000 * math.pi / 3 for k in range(1, 100001)])   # a ⟂ c, |a| = |b||c| sin α
    return P4([110, 105, 124, 121], best)
add(('2024', 'Apr', '2024-04-05', 2), 'cross', 'Consider three vectors a⃗, b⃗, c⃗. Let |a⃗| = 2, |b⃗| = 3 and a⃗ = b⃗ × c⃗. If α ∈ [0, \\f{π}{3}] is the angle between the vectors b⃗ and c⃗, then the minimum value of 27|c⃗ − a⃗|^{2} is equal to :', ['110', '105', '124', '121'], 3,
    _m14, ['a⃗ = b⃗ × c⃗ is ⟂ c⃗, so |c⃗ − a⃗|^{2} = |c⃗|^{2} + 4.', '|a⃗| = |b⃗||c⃗| sin α → |c⃗| = \\f{2}{3 sin α}, least at α = \\f{π}{3}: |c⃗|^{2} = \\f{16}{27}.', '27(\\f{16}{27} + 4) = 124.'], 'cross', 2)

# ---------- sheet 3
def _c15():
    a, b = (1, -3, 7), (2, -1, 1); u = addv(sc(4, a), sc(2, b))   # (a + 2b) × c + 3(a × c) = (4a + 2b) × c = 0
    t = 130 / dot(a, u); c = sc(t, u); assert nrm(sub(cross(addv(a, sc(2, b)), c), sc(3, cross(c, a)))) < 1e-9; return round(dot(b, c), 6)
add(('2024', 'Apr', '2024-04-05', 1), 'cross', 'Let a⃗ = î − 3ĵ + 7k̂, b⃗ = 2î − ĵ + k̂ and c⃗ be a vector such that (a⃗ + 2b⃗) × c⃗ = 3(c⃗ × a⃗). If a⃗·c⃗ = 130, then b⃗·c⃗ is equal to ______.', None, 30,
    _c15, ['(a⃗ + 2b⃗) × c⃗ + 3(a⃗ × c⃗) = 0 → (4a⃗ + 2b⃗) × c⃗ = 0 → c⃗ ∥ (4, −7, 15).', 'a⃗·c⃗ = 130t = 130 → c⃗ = (4, −7, 15).', 'b⃗·c⃗ = 8 + 7 + 15 = 30.'], 'cross', 2)
def _c16():
    a, b = (6, 1, -1), (1, 1, 0); r = [x for x in roots(lambda m: m * m - 2 * 6 * m + dot(a, a) - 8, 0, 50) if x >= 6][0]   # |c − a|² = |c|² − 2a·c + |a|²
    v = nrm(cross(a, b)) * r * math.sin(math.pi / 3); return P4([4.5 * (6 - S6), 1.5 * S3, 1.5 * S6, 4.5 * (6 + S6)], v)
add(('2024', 'Apr', '2024-04-06', 2), 'cross', 'Let a⃗ = 6î + ĵ − k̂ and b⃗ = î + ĵ. If c⃗ is a vector such that |c⃗| ≥ 6, a⃗·c⃗ = 6|c⃗|, |c⃗ − a⃗| = 2√{2} and the angle between a⃗ × b⃗ and c⃗ is 60°, then |(a⃗ × b⃗) × c⃗| is equal to:', ['\\f{9}{2}(6 − √{6})', '\\f{3}{2}√{3}', '\\f{3}{2}√{6}', '\\f{9}{2}(6 + √{6})'], 4,
    _c16, ['|c⃗ − a⃗|^{2} = |c⃗|^{2} − 12|c⃗| + 38 = 8 → |c⃗| = 6 ± √{6}; |c⃗| ≥ 6 → 6 + √{6}.', '|a⃗ × b⃗| = |(1, −1, 5)| = 3√{3}.', '|(a⃗ × b⃗) × c⃗| = 3√{3}(6 + √{6}) sin 60° = \\f{9}{2}(6 + √{6}).'], 'cross', 2)
def _p17():
    a, i = (2, 1, -1), (1, 0, 0); b = cross(cross(cross(a, (1, 1, 0)), i), i); return P4([0.2, 2, 1 / 3, 2 / 3], (dot(a, b) / nrm(b)) ** 2)
add(('2024', 'Apr', '2024-04-06', 2), 'cross', 'Let a⃗ = 2î + ĵ − k̂, b⃗ = ((a⃗ × (î + ĵ)) × î) × î. Then the square of the projection of a⃗ on b⃗ is :', ['\\f{1}{5}', '2', '\\f{1}{3}', '\\f{2}{3}'], 2,
    _p17, ['a⃗ × (î + ĵ) = (1, −1, 1). (1, −1, 1) × î = (0, 1, 1); (0, 1, 1) × î = (0, 1, −1) = b⃗.', 'a⃗·b⃗ = 2, |b⃗| = √{2} → projection √{2}, square 2.'], 'cross', 2)
def _c18():
    a, b = (2, -3, 4), (3, 4, -5); rhs = sub(cross(a, b), (1, 8, 13))   # (a + b) × c = R − a × b  ⇔  c × (a + b) = a × b − R
    c = solve(crossrows(addv(a, b)) + [a], list(rhs) + [13]); return round(24 - dot(b, c), 6)
add(('2024', 'Apr', '2024-04-06', 1), 'cross', 'Let a⃗ = 2î − 3ĵ + 4k̂, b⃗ = 3î + 4ĵ − 5k̂, and a vector c⃗ be such that a⃗ × (b⃗ + c⃗) + b⃗ × c⃗ = î + 8ĵ + 13k̂. If a⃗·c⃗ = 13, then (24 − b⃗·c⃗) is equal to ______.', None, 46,
    _c18, ['a⃗ × b⃗ = (−1, 22, 17), so (a⃗ + b⃗) × c⃗ = (1, 8, 13) − (−1, 22, 17) = (2, −14, −4).', 'With a⃗ + b⃗ = (5, 1, −1) and a⃗·c⃗ = 13 the components solve to c⃗ = (−1, −1, 3).', 'b⃗·c⃗ = −3 − 4 − 15 = −22 → 24 + 22 = 46.'], 'cross', 3)
def _c19():
    th = math.asin(math.sqrt(65) / 9); a = (1, 0, 0); b = (math.cos(th), math.sin(th), 0); c = addv(addv(sc(3, a), sc(6, b)), sc(9, cross(a, b)))
    return P4([29, 24, 27, 31], 9 * dot(c, a) - 3 * dot(c, b))
add(('2025', 'Apr', '2025-04-07', 1), 'dot', 'Let the angle θ, 0 < θ < \\f{π}{2} between two unit vectors â and b̂ be sin^{−1}(\\f{√{65}}{9}). If the vector c⃗ = 3â + 6b̂ + 9(â × b̂), then the value of 9(c⃗·â) − 3(c⃗·b̂) is', ['29', '24', '27', '31'], 1,
    _c19, ['â × b̂ is ⟂ to both, so c⃗·â = 3 + 6 cos θ and c⃗·b̂ = 3 cos θ + 6.', 'cos θ = √{1 − \\f{65}{81}} = \\f{4}{9}.', '9(3 + \\f{8}{3}) − 3(\\f{4}{3} + 6) = 51 − 22 = 29.'], 'dot', 2)
def _r20():
    def g(ph):
        a, b = (1, 0, 0), (math.cos(ph), math.sin(ph), 0); p, q = nrm(addv(a, b)), nrm(sub(a, b)); return (p + q) / (p - q) - (S2 + 1)
    ph, = roots(g, 0.01, math.pi / 2 - 0.01); a, b = (1, 0, 0), (math.cos(ph), math.sin(ph), 0)
    return P4([2 + 4 * S2, 4 + 2 * S2, 2 + S2, 1 + S2], dot(addv(a, b), addv(a, b)))
add(('2025', 'Apr', '2025-04-07', 2), 'dot', 'Let a⃗ and b⃗ be the vectors of the same magnitude such that \\f{|a⃗ + b⃗| + |a⃗ − b⃗|}{|a⃗ + b⃗| − |a⃗ − b⃗|} = √{2} + 1. Then \\f{|a⃗ + b⃗|^{2}}{|a⃗|^{2}} is :', ['2 + 4√{2}', '4 + 2√{2}', '2 + √{2}', '1 + √{2}'], 3,
    _r20, ['Put p = |a⃗ + b⃗|, q = |a⃗ − b⃗|: \\f{p}{q} = \\f{√{2} + 2}{√{2}} = 1 + √{2}, and p^{2} + q^{2} = 4|a⃗|^{2}.', '\\f{p^{2}}{|a⃗|^{2}} = \\f{4(3 + 2√{2})}{4 + 2√{2}} = 2 + √{2}.'], 'dot', 3)

# ---------- sheet 4
def _c22():
    a, b = (1, 2, 1), (2, 1, -1); c = sub(b, sc(dot(a, b) / dot(a, a), a))
    ops = [(0, 1, -2), (1, -1, 1), (-1, 1, -1), (-1, 0, 1)]; h = [i + 1 for i, o in enumerate(ops) if par(o, c)]; assert len(h) == 1; return h[0]
add(('2025', 'Apr', '2025-04-08', 2), 'dot', 'Let a⃗ = î + 2ĵ + k̂ and b⃗ = 2î + ĵ − k̂. Let ĉ be a unit vector in the plane of the vectors a⃗ and b⃗ and be perpendicular to a⃗. Then such a vector ĉ is :', ['\\f{1}{√{5}}(ĵ − 2k̂)', '\\f{1}{√{3}}(î − ĵ + k̂)', '\\f{1}{√{3}}(−î + ĵ − k̂)', '\\f{1}{√{2}}(−î + k̂)'], 4,
    _c22, ['Remove from b⃗ its part along a⃗: b⃗ − \\f{a⃗·b⃗}{|a⃗|^{2}}a⃗ = (2, 1, −1) − \\f{1}{2}(1, 2, 1) = (\\f{3}{2}, 0, −\\f{3}{2}).', 'So ĉ = ±\\f{1}{√{2}}(î − k̂); option \\f{1}{√{2}}(−î + k̂).'], 'dot', 2)
def _l23():
    a, b = (1, 2, 3), (2, 3, -5); lam, = roots(lambda l: dot(a, addv(b, (3, -1, l))) / nrm(addv(b, (3, -1, l))) - 3, -50, 50); return round(3 * lam, 6)
add(('2024', 'Apr', '2024-04-08', 2), 'dot', 'Let a⃗ = î + 2ĵ + 3k̂, b⃗ = 2î + 3ĵ − 5k̂ and c⃗ = 3î − ĵ + λk̂ be three vectors. Let r⃗ be a unit vector along b⃗ + c⃗. If r⃗·a⃗ = 3, then 3λ is equal to ______.', None, 25,
    _l23, ['b⃗ + c⃗ = (5, 2, λ − 5); a⃗·(b⃗ + c⃗) = 3λ − 6 = 3|b⃗ + c⃗|.', '(λ − 2)^{2} = 29 + (λ − 5)^{2} → 6λ = 50 → 3λ = 25.'], 'dot', 2)
def _c24():
    a, b = (4, -1, 1), (11, -1, 1); u = addv(sc(-1, a), sc(4, b))   # (a + b) × c + (−2a + 3b) × c = (−a + 4b) × c = 0
    w = addv(sc(2, a), sc(3, b)); c = sc(1670 / dot(w, u), u); assert nrm(sub(cross(addv(a, b), c), cross(c, addv(sc(-2, a), sc(3, b))))) < 1e-9
    return P4([1627, 1618, 1600, 1609], dot(c, c))
add(('2024', 'Apr', '2024-04-08', 2), 'cross', 'Let a⃗ = 4î − ĵ + k̂, b⃗ = 11î − ĵ + k̂ and c⃗ be a vector such that (a⃗ + b⃗) × c⃗ = c⃗ × (−2a⃗ + 3b⃗). If (2a⃗ + 3b⃗)·c⃗ = 1670, then |c⃗|^{2} is equal to :', ['1627', '1618', '1600', '1609'], 2,
    _c24, ['Move everything to one side: (a⃗ + b⃗ − 2a⃗ + 3b⃗) × c⃗ = (−a⃗ + 4b⃗) × c⃗ = 0 → c⃗ = t(40, −3, 3).', '2a⃗ + 3b⃗ = (41, −5, 5); dot = 1670t = 1670 → t = 1.', '|c⃗|^{2} = 1600 + 9 + 9 = 1618.'], 'cross', 2)
def _s26():
    ok = lambda al: all(al * t * t + 6 * al * t - 12 < 0 for t in [k / 10 for k in range(-400, 401)] + [s * 10 ** e for s in (1, -1) for e in range(2, 7)])
    S = [al for al in [k / 1000 for k in range(-3000, 3001)] if ok(al)]
    lo, hi = min(S), max(S); assert abs(lo + 4 / 3) < 2e-3 and hi == 0 and not ok(-4 / 3 - 1e-3) and ok(0) and not ok(1e-3)
    return 3   # (−4/3, 0]: the left end fails (the quadratic touches 0), 0 itself works
add(('2024', 'Apr', '2024-04-08', 1), 'dot', 'The set of all α, for which the vector a⃗ = αtî + 6ĵ − 3k̂ and b⃗ = tî − 2ĵ − 2αtk̂ are inclined at an obtuse angle for all t ∈ ℝ is :', ['[0, 1)', '(−2, 0]', '(−\\f{4}{3}, 0]', '(−\\f{4}{3}, 1)'], 3,
    _s26, ['Need a⃗·b⃗ = αt^{2} + 6αt − 12 < 0 for every t.', 'α = 0 gives −12 < 0 ✓. For α ≠ 0 need α < 0 and discriminant 36α^{2} + 48α < 0 → −\\f{4}{3} < α < 0.', 'Answer (−\\f{4}{3}, 0].'], 'dot', 2)
def _r27():
    a, b, c = (9, -13, 25), (3, 7, -13), (17, -2, 1); s = addv(b, c)   # (r − b − c) × a = 0 ⇒ r = b + c + t a
    t = -dot(s, sub(b, c)) / dot(a, sub(b, c)); r = addv(s, sc(t, a)); v = addv(sc(593, r), sc(67, a)); return round(dot(v, v) / 593 ** 2, 6)
add(('2024', 'Apr', '2024-04-08', 1), 'cross', 'Let a⃗ = 9î − 13ĵ + 25k̂, b⃗ = 3î + 7ĵ − 13k̂ and c⃗ = 17î − 2ĵ + k̂ be three given vectors. If r⃗ is a vector such that r⃗ × a⃗ = (b⃗ + c⃗) × a⃗ and r⃗·(b⃗ − c⃗) = 0, then \\f{|593r⃗ + 67a⃗|^{2}}{(593)^{2}} is equal to ______.', None, 569,
    _r27, ['(r⃗ − b⃗ − c⃗) × a⃗ = 0 → r⃗ = b⃗ + c⃗ + ta⃗ = (20, 5, −12) + ta⃗.', 'b⃗ − c⃗ = (−14, 9, −14): (20, 5, −12)·(b⃗ − c⃗) = −67, a⃗·(b⃗ − c⃗) = −593 → t = −\\f{67}{593}.', '593r⃗ + 67a⃗ = 593(20, 5, −12) → square/593^{2} = 400 + 25 + 144 = 569.'], 'cross', 3)
def _st28():
    a, b = (1, 2, -3), (2, 1, -1); r = addv(b, sc(-dot(a, b) / dot(a, a), a)); s1 = abs(nrm(r) - math.sqrt(10)) < 1e-9
    mn = min(math.cos(2 * A) + math.cos(2 * B) + math.cos(2 * (math.pi - A - B)) for A in [k * math.pi / 300 for k in range(1, 300)] for B in [k * math.pi / 300 for k in range(1, 300)] if A + B < math.pi)
    s2 = mn >= -1.5 - 1e-9; return {(False, False): 1, (False, True): 2, (True, True): 3, (True, False): 4}[(s1, s2)]
add(('2024', 'Apr', '2024-04-09', 2), 'cross', 'Between the following two statements : Statement-I : Let a⃗ = î + 2ĵ − 3k̂ and b⃗ = 2î + ĵ − k̂. Then the vector r⃗ satisfying a⃗ × r⃗ = a⃗ × b⃗ and a⃗·r⃗ = 0 is of magnitude √{10}. Statement-II : In a triangle ABC, cos 2A + cos 2B + cos 2C ≥ −\\f{3}{2}.', ['Both Statement-I and Statement-II are incorrect', 'Statement-I is incorrect but Statement-II is correct', 'Both Statement-I and Statement-II are correct', 'Statement-I is correct but Statement-II is incorrect'], 2,
    _st28, ['I: a⃗ × (r⃗ − b⃗) = 0 → r⃗ = b⃗ + ta⃗; a⃗·r⃗ = 7 + 14t = 0 → t = −\\f{1}{2}, r⃗ = (\\f{3}{2}, 0, \\f{1}{2}), |r⃗| = √{\\f{5}{2}} ≠ √{10}: false.', 'II: cos 2A + cos 2B + cos 2C = −1 − 4 cos A cos B cos C ≥ −\\f{3}{2}, since cos A cos B cos C ≤ \\f{1}{8}: true.'], 'cross', 2)

# ---------- sheet 5
def _ab29():
    vals = set()
    for al in range(-6, 7):
        for be in range(-6, 7):
            if al * be == -6 and abs(nrm(cross(addv((2, al, 1), (-1, 0, 1)), addv((-1, 0, 1), (0, be, -1)))) / 2 - math.sqrt(21) / 2) < 1e-9: vals.add((al, be))
    (a1, b1), (a2, b2) = sorted(vals); r = {a1 * a1 + b1 * b1 - a2 * b2, a2 * a2 + b2 * b2 - a1 * b1}; assert len(r) == 1; return P4([17, 24, 21, 19], r.pop())
add(('2024', 'Apr', '2024-04-09', 2), 'cross', 'Let a⃗ = 2î + αĵ + k̂, b⃗ = −î + k̂, c⃗ = βĵ − k̂, where α and β are integers and αβ = −6. Let the values of the ordered pair (α, β) for which the area of the parallelogram of diagonals a⃗ + b⃗ and b⃗ + c⃗ is \\f{√{21}}{2}, be (α_{1}, β_{1}) and (α_{2}, β_{2}). Then α_{1}^{2} + β_{1}^{2} − α_{2}β_{2} is equal to', ['17', '24', '21', '19'], 4,
    _ab29, ['Area from diagonals = \\f{1}{2}|d⃗_{1} × d⃗_{2}|. a⃗ + b⃗ = (1, α, 2), b⃗ + c⃗ = (−1, β, 0); cross = (−2β, −2, β + α).', '4β^{2} + 4 + (α + β)^{2} = 21 with αβ = −6 → (α, β) = (3, −2) or (−3, 2).', 'α_{1}^{2} + β_{1}^{2} − α_{2}β_{2} = 13 + 6 = 19.'], 'cross', 3)
def _q30():
    a, b = (1, 0, 0), (0.3, 2.5, 0); assert abs(nrm(cross(sc(2, a), sc(3, b))) - 15) < 1e-9   # any a, b with |a × b| = 2.5
    O, A, B, C = (0, 0, 0), sc(2, a), addv(sc(6, a), sc(5, b)), sc(3, b); V = [O, A, B, C]
    ar = abs(sum(V[i][0] * V[(i + 1) % 4][1] - V[(i + 1) % 4][0] * V[i][1] for i in range(4))) / 2; return P4([38, 40, 32, 35], ar)
add(('2024', 'Apr', '2024-04-09', 1), 'cross', 'Let OA⃗ = 2a⃗, OB⃗ = 6a⃗ + 5b⃗ and OC⃗ = 3b⃗, where O is the origin. If the area of the parallelogram with adjacent sides OA⃗ and OC⃗ is 15 sq. units, then the area (in sq. units) of the quadrilateral OABC is equal to :', ['38', '40', '32', '35'], 4,
    _q30, ['|OA⃗ × OC⃗| = 6|a⃗ × b⃗| = 15 → |a⃗ × b⃗| = \\f{5}{2}.', 'Quadrilateral area = \\f{1}{2}|OB⃗ × AC⃗| with AC⃗ = 3b⃗ − 2a⃗: (6a⃗ + 5b⃗) × (3b⃗ − 2a⃗) = 28(a⃗ × b⃗).', 'Area = \\f{1}{2}·28·\\f{5}{2} = 35.'], 'cross', 2)
def _c31():
    al, = [x for x in roots(lambda al: nrm(cross((al, 4, 2), (5, 3, 4))) / 2 - 5 * S6, -50, 50) if x > 1e-6]; c = sub((al, 4, 2), (5, 3, 4)); return P4([16, 14, 12, 10], dot(c, c))
add(('2024', 'Apr', '2024-04-09', 1), 'cross', 'Let three vectors a⃗ = αî + 4ĵ + 2k̂, b⃗ = 5î + 3ĵ + 4k̂, c⃗ = xî + yĵ + zk̂ form a triangle such that c⃗ = a⃗ − b⃗ and the area of the triangle is 5√{6}. If α is a positive real number, then |c⃗|^{2} is :', ['16', '14', '12', '10'], 2,
    _c31, ['Area = \\f{1}{2}|a⃗ × b⃗|; a⃗ × b⃗ = (10, 10 − 4α, 3α − 20).', '100 + (10 − 4α)^{2} + (3α − 20)^{2} = 600 → 25α^{2} − 200α = 0 → α = 8.', 'c⃗ = (3, 1, −2) → 14.'], 'cross', 2)
def _m32():
    best = max(3 * nrm(addv(sc(3, (2, 0, 0)), sc(2, (3 * math.cos(t), 3 * math.sin(t), 0)))) + 4 * nrm(sub(sc(3, (2, 0, 0)), sc(2, (3 * math.cos(t), 3 * math.sin(t), 0)))) for t in [k * math.pi / 200000 for k in range(200001)])
    return P4([30, 36, 60, 72], best, 1e-6)
add(('2026', 'Apr', '2026-04-02', 1), 'dot', 'If a⃗ and b⃗ are two vectors such that |a⃗| = 2 and |b⃗| = 3, then the maximum value of 3|3a⃗ + 2b⃗| + 4|3a⃗ − 2b⃗| is :', ['30', '36', '60', '72'], 3,
    _m32, ['x = |3a⃗ + 2b⃗|, y = |3a⃗ − 2b⃗|: x^{2} + y^{2} = 2(36 + 36) = 144.', 'By Cauchy–Schwarz 3x + 4y ≤ 5·√{144} = 60, reached when \\f{x}{3} = \\f{y}{4}.'], 'dot', 2)
def _c34():
    a, b = (-1, 2, 2), (8, 7, -3); c = solve([(0, -a[2], a[1]), (a[2], 0, -a[0]), (-a[1], a[0], 0), (1, 1, 1)], list(b) + [4])
    return P4([33, 30, 35, 27], dot(addv(a, c), addv(a, c)))
add(('2026', 'Jan', '2026-01-21', 1), 'cross', 'Let a⃗ = −î + 2ĵ + 2k̂, b⃗ = 8î + 7ĵ − 3k̂ and c⃗ be a vector such that a⃗ × c⃗ = b⃗. If c⃗·(î + ĵ + k̂) = 4, then |a⃗ + c⃗|^{2} is equal to :', ['33', '30', '35', '27'], 4,
    _c34, ['a⃗·b⃗ = 0 ✓, so solutions exist: c⃗ = c⃗_{0} + ta⃗. Componentwise a⃗ × c⃗ = b⃗ plus c⃗·(1, 1, 1) = 4 gives c⃗ = (2, −1, 3).', 'a⃗ + c⃗ = (1, 1, 5) → 27.'], 'cross', 2)
def _k35():
    lams = sorted(dot(sc(s * math.sqrt(29) / nrm((2, 3, 4)), (2, 3, 4)), (-7, 2, 3)) for s in (1, -1)); l2, l1 = lams
    K = [k for k in range(-10, 11) if k * k - 5 * k + l1 == 0 and k * k == 3 * k + l2 / 2]
    assert len(K) == 1; k = K[0]; A = k * k; assert (4 / A) ** 2 + (6 / A) ** 2 - l2 / A > 0   # real radius
    return P4([4, 1, -1, 2], k)
add(('2026', 'Jan', '2026-01-21', 1), 'cross', 'Let c⃗ and d⃗ be vectors such that |c⃗ + d⃗| = √{29} and c⃗ × (2î + 3ĵ + 4k̂) = (2î + 3ĵ + 4k̂) × d⃗. If λ_{1}, λ_{2} (λ_{1} > λ_{2}) are the possible values of (c⃗ + d⃗)·(−7î + 2ĵ + 3k̂), then the equation K^{2}x^{2} + (K^{2} − 5K + λ_{1})xy + (3K + \\f{λ_{2}}{2})y^{2} − 8x + 12y + λ_{2} = 0 represents a circle, for K equal to:', ['4', '1', '−1', '2'], 2,
    _k35, ['(c⃗ + d⃗) × (2, 3, 4) = 0 and |c⃗ + d⃗| = √{29} = |(2, 3, 4)| → c⃗ + d⃗ = ±(2, 3, 4); λ = ±4.', 'Circle: no xy term → K^{2} − 5K + 4 = 0 → K = 1, 4; equal x^{2}, y^{2} coefficients → K^{2} = 3K − 2 → K = 1, 2.', 'K = 1 (then x^{2} + y^{2} − 8x + 12y − 4 = 0, a real circle).'], 'cross', 3)

# ---------- sheet 6
def _c39():
    a, b = (-1, 1, 3), (1, 3, 1); l, m = solve([(dot(a, (3, -6, 2)), dot(b, (3, -6, 2))), (dot(a, (1, 1, 1)), dot(b, (1, 1, 1)))], [10, -2])
    c = addv(sc(l, a), sc(m, b)); return P4([8, 12, 14, 15], dot(c, c))
add(('2026', 'Apr', '2026-04-02', 2), 'dot', 'Let the vectors a⃗ = −î + ĵ + 3k̂ and b⃗ = î + 3ĵ + k̂. For some λ, μ ∈ ℝ, let c⃗ = λa⃗ + μb⃗. If c⃗·(3î − 6ĵ + 2k̂) = 10 and c⃗·(î + ĵ + k̂) = −2, then |c⃗|^{2} is equal to :', ['8', '12', '14', '15'], 2,
    _c39, ['a⃗·(3, −6, 2) = −3, b⃗·(3, −6, 2) = −13; a⃗·(1, 1, 1) = 3, b⃗·(1, 1, 1) = 5.', '−3λ − 13μ = 10, 3λ + 5μ = −2 → μ = −1, λ = 1.', 'c⃗ = a⃗ − b⃗ = (−2, −2, 2) → 12.'], 'dot', 1)
def _r40():
    PQ, PS = (0, 1, 1), (1, -1, 0); w = sub(PQ, sc(dot(PQ, PS) / dot(PS, PS), PS)); w = sc(nrm(PS) / nrm(w), w)   # in-plane, ⟂ PS, towards PQ
    al, = [x for x in roots(lambda t: dot(addv(sc(math.cos(t), PS), sc(math.sin(t), w)), PQ), 0.001, math.pi / 2 - 0.001)]
    return P4([0.5, S3 / 2, S3 / 4, 2 * S3 / 5], math.sin(2.5 * al) ** 2 - math.sin(al / 2) ** 2)
add(('2026', 'Apr', '2026-04-02', 2), 'dot', 'Two adjacent sides of a parallelogram PQRS are given by PQ⃗ = ĵ + k̂ and PS⃗ = î − ĵ. If the side PS is rotated about the point P by an acute angle α in the plane of the parallelogram so that it becomes perpendicular to the side PQ, then sin^{2}(\\f{5α}{2}) − sin^{2}(\\f{α}{2}) is equal to:', ['\\f{1}{2}', '\\f{√{3}}{2}', '\\f{√{3}}{4}', '\\f{2√{3}}{5}'], 2,
    _r40, ['cos∠QPS = \\f{−1}{√{2}·√{2}} = −\\f{1}{2} → 120°. Turning PS by 30° towards PQ makes it 90°: α = 30°.', 'sin^{2}A − sin^{2}B = sin(A + B) sin(A − B) = sin 90° sin 60° = \\f{√{3}}{2}.'], 'dot', 2)
def _a42():
    a = (1, 2, 2); lam, = [x for x in roots(lambda l: nrm(addv(a, sc(dot((l, 0, 4), a) / dot(a, a), a))) - 7, -50, 50) if x > 0]
    b = (lam, 0, 4); c = sc(dot(b, a) / dot(a, a), a); return round(nrm(cross(b, c)), 6)
add(('2025', 'Jan', '2025-01-22', 1), 'dot', 'Let c⃗ be the projection vector of b⃗ = λî + 4k̂, λ > 0, on the vector a⃗ = î + 2ĵ + 2k̂. If |a⃗ + c⃗| = 7, then the area of the parallelogram formed by the vectors b⃗ and c⃗ is ______.', None, 16,
    _a42, ['c⃗ = \\f{λ + 8}{9}a⃗, so |a⃗ + c⃗| = 3(1 + \\f{λ + 8}{9}) = 7 → λ = 4, c⃗ = \\f{4}{3}(1, 2, 2).', 'b⃗ × c⃗ = \\f{4}{3}(4, 0, 4) × (1, 2, 2) = \\f{4}{3}(−8, −4, 8) → |…| = 16.'], 'dot', 2)
def _n43():
    a, b = (1, 0, 0), (0.5, math.sqrt(3) / 2, 0); r = [l for l in roots(lambda l: dot(addv(sc(l, a), sc(2, b)), sub(sc(3, a), sc(l, b))), -10, 10) if -1 <= l <= 3]
    return P4([3, 1, 0, 2], len(r))
add(('2025', 'Jan', '2025-01-22', 2), 'dot', 'Let a⃗ and b⃗ be two unit vectors such that the angle between them is \\f{π}{3}. If λa⃗ + 2b⃗ and 3a⃗ − λb⃗ are perpendicular to each other, then the number of values of λ in [−1, 3] is :', ['3', '1', '0', '2'], 3,
    _n43, ['(λa⃗ + 2b⃗)·(3a⃗ − λb⃗) = 3λ − \\f{λ^{2}}{2} + 3 − 2λ = 0 → λ^{2} − 2λ − 6 = 0.', 'λ = 1 ± √{7} ≈ 3.65, −1.65: none in [−1, 3].'], 'dot', 1)
def _e45():
    A, B, C = (1, 2, 1), (1, 3, -2), (2, 1, -1); n = cross(sub(B, A), sub(C, A)); h = 3 * (math.sqrt(805) / (6 * S2)) / (nrm(n) / 2); M = sc(0.5, addv(B, C))
    s, = [s for s in roots(lambda s: dot(sc(s, sub(M, A)), sc(s, sub(M, A))) + h * h - 110 / 9, -3, 3) if 0 <= s <= 1]; E = addv(A, sub(M, A), s)
    ops = [sc(1 / 6, (12, 12, 1)), sc(1 / 12, (7, 4, 3)), sc(1 / 6, (7, 12, 1)), sc(0.5, (1, 4, 7))]; h_ = [i + 1 for i, o in enumerate(ops) if nrm(sub(o, E)) < 1e-9]; assert len(h_) == 1; return h_[0]
add(('2025', 'Jan', '2025-01-23', 1), 'cross', 'Let the position vectors of the vertices A, B and C of a tetrahedron ABCD be î + 2ĵ + k̂, î + 3ĵ − 2k̂ and 2î + ĵ − k̂ respectively. The altitude from the vertex D to the opposite face ABC meets the median line segment through A of the triangle ABC at the point E. If the length of AD is \\f{√{110}}{3} and the volume of the tetrahedron is \\f{√{805}}{6√{2}}, then the position vector of E is', ['\\f{1}{6}(12î + 12ĵ + k̂)', '\\f{1}{12}(7î + 4ĵ + 3k̂)', '\\f{1}{6}(7î + 12ĵ + k̂)', '\\f{1}{2}(î + 4ĵ + 7k̂)'], 3,
    _e45, ['AB⃗ × AC⃗ = (−5, −3, −1), area ABC = \\f{√{35}}{2}; height DE = \\f{3V}{area} = √{\\f{23}{2}}.', 'AE^{2} = AD^{2} − DE^{2} = \\f{110}{9} − \\f{23}{2} = \\f{13}{18}; E = A + s(M − A) with M = (\\f{3}{2}, 2, −\\f{3}{2}) gives s = \\f{1}{3}.', 'E = (\\f{7}{6}, 2, \\f{1}{6}) = \\f{1}{6}(7î + 12ĵ + k̂).'], 'cross', 3)

# ---------- sheet 7
def _c46():
    a, b = (1, 2, 3), (3, 1, -1); l, m = solve([(dot(a, b), dot(b, b)), (dot(a, a), dot(a, b))], [0, 5]); c = addv(sc(l, a), sc(m, b))
    return P4([18, 16, math.sqrt(11 / 6), 1 / (3 * S2)], nrm(c))
add(('2025', 'Jan', '2025-01-24', 1), 'dot', 'Let a⃗ = î + 2ĵ + 3k̂, b⃗ = 3î + ĵ − k̂ and c⃗ be three vectors such that c⃗ is coplanar with a⃗ and b⃗. If the vector c⃗ is perpendicular to b⃗ and a⃗·c⃗ = 5, then |c⃗| is equal to', ['18', '16', '√{\\f{11}{6}}', '\\f{1}{3√{2}}'], 3,
    _c46, ['c⃗ = λa⃗ + μb⃗. a⃗·b⃗ = 2, |a⃗|^{2} = 14, |b⃗|^{2} = 11.', 'c⃗·b⃗ = 2λ + 11μ = 0 and a⃗·c⃗ = 14λ + 2μ = 5 → λ = \\f{55}{150} = \\f{11}{30}, μ = −\\f{1}{15}.', '|c⃗|^{2} = c⃗·(λa⃗ + μb⃗) = 5λ = \\f{11}{6} → |c⃗| = √{\\f{11}{6}}.'], 'dot', 2)
def _p47():
    a = (3, -1, 2); b = cross(a, (1, 0, -2)); c = cross(b, (0, 0, 1)); v = sub(c, (0, 2, 0)); return P4([2 * math.sqrt(7), math.sqrt(14), 3 * math.sqrt(7), 2 * math.sqrt(14)], dot(v, a) / nrm(a))
add(('2025', 'Jan', '2025-01-24', 2), 'cross', 'Let a⃗ = 3î − ĵ + 2k̂, b⃗ = a⃗ × (î − 2k̂) and c⃗ = b⃗ × k̂. Then the projection of c⃗ − 2ĵ on a⃗ is:', ['2√{7}', '√{14}', '3√{7}', '2√{14}'], 4,
    _p47, ['b⃗ = (3, −1, 2) × (1, 0, −2) = (2, 8, 1).', 'c⃗ = b⃗ × k̂ = (8, −2, 0); c⃗ − 2ĵ = (8, −4, 0).', 'Projection on a⃗ = \\f{24 + 4}{√{14}} = 2√{14}.'], 'cross', 1)
def _o48():
    V = [(F(4), F(1), F(-3)), (F(-5), F(1), F(2)), (F(2), F(-1), F(2))]; G = tuple(sum(v[i] for v in V) / 3 for i in range(3)); H = (F(1, 4),) * 3
    O = tuple((3 * g - h) / 2 for g, h in zip(G, H)); return P4([3, 6, 1, 4], O[0] + 2 * O[1] + 5 * O[2])   # Euler line: G divides HO in 1 : 2 (coordinates in the basis p, q, r)
add(('2025', 'Jan', '2025-01-24', 2), 'cross', 'Let the position vectors of three vertices of a triangle be 4p⃗ + q⃗ − 3r⃗, −5p⃗ + q⃗ + 2r⃗ and 2p⃗ − q⃗ + 2r⃗. If the position vectors of the orthocenter and the circumcenter of the triangle are \\f{p⃗ + q⃗ + r⃗}{4} and αp⃗ + βq⃗ + γr⃗ respectively, then α + 2β + 5γ is equal to :', ['3', '6', '1', '4'], 1,
    _o48, ['Centroid G = \\f{1}{3}(sum of vertices) = \\f{p⃗ + q⃗ + r⃗}{3}.', 'G divides HO in 1 : 2, so O = \\f{3G − H}{2} = \\f{3}{8}(p⃗ + q⃗ + r⃗).', 'α + 2β + 5γ = \\f{3}{8}·8 = 3.'], 'cross', 2)
def _a51():
    A, B = (S3, 1, 0), (1, S3, 0); u = addv(sc(1 / nrm(A), A), sc(1 / nrm(B), B))   # internal bisector direction
    r = roots(lambda a: nrm(cross((a, 1 - a, 0), u)) / nrm(u) - 9 / S2, -50, 50); return P4([4.5, 1, 2, 0], sum(r))
add(('2025', 'Jan', '2025-01-28', 2), 'dot', 'Let A, B, C be three points in √{3}î + ĵ, î + √{3}ĵ and aî + (1 − a)ĵ respectively with respect to the origin O. If the distance of the point C from the line bisecting the angle between the vectors OA⃗ and OB⃗ is \\f{9}{√{2}}, then the sum of all the possible values of a is :', ['\\f{9}{2}', '1', '2', '0'], 2,
    _a51, ['|OA⃗| = |OB⃗| = 2, so the bisector is along OA⃗ + OB⃗ ∥ (1, 1): the line y = x.', 'Distance of (a, 1 − a): \\f{|2a − 1|}{√{2}} = \\f{9}{√{2}} → a = 5 or −4.', 'Sum = 1.'], 'dot', 1)
def _c52():
    b = (3, 1, -1); par_ = sc(16 / 11, b); perp = sc(1 / 11, (-4, -5, -17)); assert abs(dot(perp, b)) < 1e-12; a = addv(par_, perp)
    assert abs(dot(a, b) / dot(b, b) - 16 / 11) < 1e-12; return P4([23, 26, 16, 18], dot(a, a))
add(('2025', 'Jan', '2025-01-28', 2), 'dot', 'If the components of a⃗ = αî + βĵ + γk̂ along and perpendicular to b⃗ = 3î + ĵ − k̂ respectively, are \\f{16}{11}(3î + ĵ − k̂) and \\f{1}{11}(−4î − 5ĵ − 17k̂), then α^{2} + β^{2} + γ^{2} is equal to :', ['23', '26', '16', '18'], 2,
    _c52, ['a⃗ = sum of its two components = \\f{1}{11}(48 − 4, 16 − 5, −16 − 17) = (4, 1, −3).', 'α^{2} + β^{2} + γ^{2} = 16 + 1 + 9 = 26.'], 'dot', 1)
def _c53():
    a, b = (2, -1, 3), (3, -5, 1); u = addv(a, b)   # a × c = c × b ⇒ (a + b) × c = 0
    ts = roots(lambda t: dot(addv(a, sc(t, u)), addv(b, sc(t, u))) - 168, -20, 20); return P4([462, 77, 308, 154], max(dot(sc(t, u), sc(t, u)) for t in ts))
add(('2025', 'Jan', '2025-01-29', 1), 'cross', 'Let a⃗ = 2î − ĵ + 3k̂, b⃗ = 3î − 5ĵ + k̂ and c⃗ be a vector such that a⃗ × c⃗ = c⃗ × b⃗ and (a⃗ + c⃗)·(b⃗ + c⃗) = 168. Then the maximum value of |c⃗|^{2} is :', ['462', '77', '308', '154'], 3,
    _c53, ['(a⃗ + b⃗) × c⃗ = 0 → c⃗ = t(5, −6, 4), |a⃗ + b⃗|^{2} = 77.', '(a⃗ + c⃗)·(b⃗ + c⃗) = a⃗·b⃗ + t·77 + 77t^{2} = 14 + 77t + 77t^{2} = 168 → t = 1 or −2.', 'Max |c⃗|^{2} = 77·4 = 308.'], 'cross', 2)

# ---------- sheet 8
def _al56():
    n = cross((1, -2, 3), (2, 3, -1)); u = sc(1 / nrm(n), n)
    a, = [s for s in (u, sc(-1, u)) if abs(dot(s, (1, 1, 1)) / S3 + 1 / 3) < 1e-9]
    r = roots(lambda al: dot(a, (1, al, 1)) / nrm((1, al, 1)) - 0.5, -50, 50); assert len(r) == 1
    return P4([S6, -S3, -S6, S3], r[0])
add(('2025', 'Jan', '2025-01-29', 2), 'cross', 'Let â be a unit vector perpendicular to the vectors b⃗ = î − 2ĵ + 3k̂ and c⃗ = 2î + 3ĵ − k̂, and makes an angle of cos^{−1}(−\\f{1}{3}) with the vector î + ĵ + k̂. If â makes an angle of \\f{π}{3} with the vector î + αĵ + k̂, then the value of α is:', ['√{6}', '−√{3}', '−√{6}', '√{3}'], 3,
    _al56, ['b⃗ × c⃗ = (−7, 7, 7) → â = ±\\f{1}{√{3}}(−1, 1, 1). The angle condition with (1, 1, 1) picks â = \\f{1}{√{3}}(1, −1, −1).', 'cos \\f{π}{3}: \\f{−α}{√{3}√{α^{2} + 2}} = \\f{1}{2} → α < 0 and α^{2} = 6.', 'α = −√{6}.'], 'cross', 2)
def _r57():
    vals = set()
    for n in range(6, 12):
        th = [2 ** (k - 1) * math.pi / (2 ** n + 1) for k in range(1, n + 1)]
        vals.add(round(sum(dot((math.tan(t), 1), (math.tan(t), 1)) for t in th) / sum(dot((1, -1 / math.tan(t)), (1, -1 / math.tan(t))) for t in th), 6))
    assert len(vals) == 1; return round(vals.pop())
add(('2026', 'Apr', '2026-04-04', 1), 'dot', 'Let a⃗_{k} = (tan θ_{k})î + ĵ and b⃗_{k} = î − (cot θ_{k})ĵ, where θ_{k} = \\f{2^{k−1}π}{2^{n} + 1}, for some n ∈ ℕ, n > 5. Then the value of \\f{Σ_{k=1}^{n}|a⃗_{k}|^{2}}{Σ_{k=1}^{n}|b⃗_{k}|^{2}} is ______.', None, 3,
    _r57, ['|a⃗_{k}|^{2} = sec^{2}θ_{k}, |b⃗_{k}|^{2} = cosec^{2}θ_{k}; the ratio is \\f{Σ sec^{2}θ_{k}}{Σ cosec^{2}θ_{k}}.', 'Use cot θ − 2 cot 2θ = tan θ and cosec^{2}θ = 1 + cot^{2}θ: with doubling angles ending at 2^{n}θ_{1} = π − θ_{1}, both sums telescope.', 'The ratio comes out 3 for every n (checked numerically for n = 6 … 11).'], 'dot', 3)
def _l58():
    AB = (2, 4, -5); lam, = roots(lambda l: abs(dot((1, 1, 1), addv(AB, (1, 2, l)))) / nrm(addv(AB, (1, 2, l))) - 1, -50, 50)
    r = sorted(roots(lambda x: lam * lam * x * x - 6 * lam * x + 5, -10, 10)); return P4([1, 4, 3, 6], 2 * r[1] - r[0])
add(('2026', 'Jan', '2026-01-22', 1), 'dot', 'Let AB⃗ = 2î + 4ĵ − 5k̂ and AD⃗ = î + 2ĵ + λk̂, λ ∈ ℝ. Let the projection of the vector v⃗ = î + ĵ + k̂ on the diagonal AC⃗ of the parallelogram ABCD be of length one unit. If α, β, where α > β, be the roots of the equation λ^{2}x^{2} − 6λx + 5 = 0, then 2α − β is equal to', ['1', '4', '3', '6'], 3,
    _l58, ['AC⃗ = AB⃗ + AD⃗ = (3, 6, λ − 5). |v⃗·AC⃗| = |AC⃗|: (λ + 4)^{2} = 45 + (λ − 5)^{2} → λ = 3.', '9x^{2} − 18x + 5 = 0 → x = \\f{5}{3}, \\f{1}{3}.', '2α − β = \\f{10}{3} − \\f{1}{3} = 3.'], 'dot', 2)
def _l59():
    u = (1, 0, 0); v = (0.5, S3 / 2, 0); assert abs(nrm(cross(u, v)) - S3 / 2) < 1e-12
    hits = set()
    for lam in (-2.3, 0.7, 4.1):
        A = addv(addv(sc(lam, u), v), cross(u, v)); au, av = dot(A, u), dot(A, v)
        ops = [4 / 3 * au - 2 / 3 * av, 2 / 3 * au - 1 / 3 * av, 4 / 3 * au + 2 / 3 * av, au - 0.5 * av]; hits.add(tuple(i + 1 for i, o in enumerate(ops) if abs(o - lam) < 1e-9))
    (h,), = hits; return h
add(('2026', 'Apr', '2026-04-04', 2), 'dot', 'Let û and v̂ be unit vectors inclined at an acute angle such that |û × v̂| = \\f{√{3}}{2}. If A⃗ = λû + v̂ + (û × v̂), then λ is equal to:', ['\\f{4}{3}(A⃗·û) − \\f{2}{3}(A⃗·v̂)', '\\f{2}{3}(A⃗·û) − \\f{1}{3}(A⃗·v̂)', '\\f{4}{3}(A⃗·û) + \\f{2}{3}(A⃗·v̂)', '(A⃗·û) − \\f{1}{2}(A⃗·v̂)'], 1,
    _l59, ['Acute angle with sine \\f{√{3}}{2} → 60°, û·v̂ = \\f{1}{2}; û × v̂ is ⟂ to both.', 'A⃗·û = λ + \\f{1}{2}, A⃗·v̂ = \\f{λ}{2} + 1.', 'Eliminate: \\f{4}{3}(λ + \\f{1}{2}) − \\f{2}{3}(\\f{λ}{2} + 1) = λ.'], 'dot', 2)
def _d60():
    a = (2, -1, 1); lam, = [l for l in range(-20, 21) if abs(nrm(cross(a, (0, l, 2))) - math.sqrt(53)) < 1e-9]; c = cross(a, (0, lam, 2))
    best = max(dot(c, (0, 2 * math.cos(t), 2 * math.sin(t))) ** 2 for t in [k * 2 * math.pi / 100000 for k in range(100000)]); return P4([104, 26, 52, 208], best, 1e-6)
add(('2026', 'Jan', '2026-01-22', 2), 'cross', 'Let a⃗ = 2î − ĵ + k̂ and b⃗ = λĵ + 2k̂, λ ∈ ℤ be two vectors. Let c⃗ = a⃗ × b⃗ and d⃗ be a vector of magnitude 2 in yz-plane. If |c⃗| = √{53}, then the maximum possible value of (c⃗·d⃗)^{2} is equal to:', ['104', '26', '52', '208'], 4,
    _d60, ['c⃗ = (−2 − λ, −4, 2λ); |c⃗|^{2} = 5λ^{2} + 4λ + 20 = 53 → λ = −3 (integer).', 'c⃗ = (1, −4, −6). d⃗ = 2(0, cos t, sin t): c⃗·d⃗ = 2(−4 cos t − 6 sin t), max square 4·52 = 208.'], 'cross', 2)
def _s61():
    good = lambda l: dot((S2, -1, l), (-l * l, 4 * S2, 4 * S2)) < 0 and math.pi / 6 < math.acos(l / nrm((S2, -1, l))) < math.pi / 2
    G = [l for l in [k / 1000 for k in range(1, 10001)] if good(l)]; lo, hi = min(G), max(G); gaps = [x for x in [k / 1000 for k in range(1, 10001)] if lo < x < hi and not good(x)]
    assert len(gaps) == 1; return round(round(lo) + round(hi) + gaps[0])
add(('2026', 'Jan', '2026-01-22', 2), 'dot', 'Let a vector a⃗ = √{2}î − ĵ + λk̂, λ > 0, make an obtuse angle with the vector b⃗ = −λ^{2}î + 4√{2}ĵ + 4√{2}k̂ and an angle θ, \\f{π}{6} < θ < \\f{π}{2}, with the positive z-axis. If the set of all possible values of λ is (α, β) − {γ}, then α + β + γ is equal to ______.', None, 5,
    _s61, ['a⃗·b⃗ = −√{2}(λ − 2)^{2} < 0 → λ ≠ 2.', 'cos θ = \\f{λ}{√{3 + λ^{2}}} < \\f{√{3}}{2} → λ^{2} < 9; with λ > 0: (0, 3).', 'Set (0, 3) − {2} → 0 + 3 + 2 = 5.'], 'dot', 2)

# ---------- sheet 9
def _r62():
    a, b = (math.sqrt(7), 1, -1), (0, 1, 2); t = -dot(a, b) / dot(a, a); r = addv(b, sc(t, a))   # (r − b) × a = 0 ⇒ r = b + t a
    assert nrm(addv(cross(r, a), cross(a, b))) < 1e-9 and abs(dot(r, a)) < 1e-9; return P4([44, 54, 86, 132], 9 * dot(r, r))
add(('2026', 'Apr', '2026-04-05', 1), 'cross', 'Let a⃗ = √{7}î + ĵ − k̂ and b⃗ = ĵ + 2k̂. If r⃗ is a vector such that r⃗ × a⃗ + a⃗ × b⃗ = 0⃗ and r⃗·a⃗ = 0, then |3r⃗|^{2} is equal to:', ['44', '54', '86', '132'], 1,
    _r62, ['r⃗ × a⃗ = b⃗ × a⃗ → (r⃗ − b⃗) × a⃗ = 0 → r⃗ = b⃗ + ta⃗.', 'r⃗·a⃗ = a⃗·b⃗ + 9t = −1 + 9t = 0 → t = \\f{1}{9}.', '3r⃗ = 3b⃗ + \\f{a⃗}{3} = (\\f{√{7}}{3}, \\f{10}{3}, \\f{17}{3}) → \\f{7 + 100 + 289}{9} = 44.'], 'cross', 2)
def _d64():
    a, b = (-1, 1, 2), (1, -1, -3); d = cross(cross(a, b), a); return P4([4, -4, -2, 2], dot(sub(a, b), d))
add(('2026', 'Jan', '2026-01-23', 1), 'cross', 'Let a⃗ = −î + ĵ + 2k̂, b⃗ = î − ĵ − 3k̂, c⃗ = a⃗ × b⃗ and d⃗ = c⃗ × a⃗. Then (a⃗ − b⃗)·d⃗ is equal to :', ['4', '−4', '−2', '2'], 3,
    _d64, ['c⃗ = a⃗ × b⃗ = (−1, −1, 0); d⃗ = c⃗ × a⃗ = (−2, 2, −2).', 'a⃗ − b⃗ = (−2, 2, 5) → 4 + 4 − 10 = −2.'], 'cross', 1)
def _p65():
    a, b = (1, -2, 3), (2, 1, -1); v = cross(a, b); lam, = roots(lambda l: dot(v, (l, 1, 1)) - 11, -50, 50); c = (lam, 1, 1)
    return P4([9, 6, 4, 12], 9 * (dot(b, c) / nrm(c)) ** 2)
add(('2026', 'Jan', '2026-01-23', 2), 'cross', 'Let a⃗ = î − 2ĵ + 3k̂, b⃗ = 2î + ĵ − k̂, c⃗ = λî + ĵ + k̂ and v⃗ = a⃗ × b⃗. If v⃗·c⃗ = 11 and the length of the projection of b⃗ on c⃗ is p, then 9p^{2} is equal to', ['9', '6', '4', '12'], 4,
    _p65, ['v⃗ = (−1, 7, 5); v⃗·c⃗ = −λ + 12 = 11 → λ = 1.', 'p = \\f{b⃗·c⃗}{|c⃗|} = \\f{2}{√{3}} → 9p^{2} = 12.'], 'cross', 1)
def _ac66():
    out = set()
    for ph in (0.3, 1.9):   # any placement with |b| = 4, |c| = 2 at 60°
        b = (4 * math.cos(ph), 4 * math.sin(ph), 0); c = (2 * math.cos(ph + math.pi / 3), 2 * math.sin(ph + math.pi / 3), 0); w = sub(b, sc(2, c))
        for s in (1, -1):
            a = sc(s / nrm(w), w); assert nrm(sub(cross(a, b), sc(2, cross(a, c)))) < 1e-9; out.add(round(abs(dot(a, c)), 9))
    assert len(out) == 1; return P4([2, 4, 0, 1], out.pop())
add(('2026', 'Jan', '2026-01-23', 2), 'cross', 'Let a⃗, b⃗, c⃗ be three vectors such that a⃗ × b⃗ = 2(a⃗ × c⃗). If |a⃗| = 1, |b⃗| = 4, |c⃗| = 2, and the angle between b⃗ and c⃗ is 60°, then |a⃗·c⃗| is equal to', ['2', '4', '0', '1'], 4,
    _ac66, ['a⃗ × (b⃗ − 2c⃗) = 0 → b⃗ − 2c⃗ = ta⃗; |b⃗ − 2c⃗|^{2} = 16 + 16 − 4·4 = 16 → |t| = 4.', 'Dot with c⃗: b⃗·c⃗ − 2|c⃗|^{2} = 4 − 8 = t(a⃗·c⃗) → |a⃗·c⃗| = 1.'], 'cross', 2)
def _c67():
    a, b = (1, 1, 1), (0, 1, -1); c = solve([(0, -a[2], a[1]), (a[2], 0, -a[0]), (-a[1], a[0], 0), a], list(b) + [3]); return round(dot(c, sub(a, sc(2, b))), 6)
add(('2026', 'Apr', '2026-04-06', 1), 'cross', 'If a⃗ = î + ĵ + k̂, b⃗ = ĵ − k̂ and c⃗ be three vectors such that a⃗ × c⃗ = b⃗ and a⃗·c⃗ = 3, then c⃗·(a⃗ − 2b⃗) is equal to ______.', None, 3,
    _c67, ['a⃗ × c⃗ = b⃗ with c⃗ = (x, y, z): z − y = 0, x − z = 1, y − x = −1; with x + y + z = 3 → c⃗ = (\\f{5}{3}, \\f{2}{3}, \\f{2}{3}).', 'a⃗ − 2b⃗ = (1, −1, 3) → \\f{5}{3} − \\f{2}{3} + 2 = 3.'], 'cross', 2)
def _d68():
    a, b = (2, 1, -2), (1, 1, 0); c = cross(a, b); dn = 3 / (nrm(c) * math.sin(math.pi / 4))   # |c × d| = |c||d| sin 45°
    return P4([11, 3, 0, 1], (dn * dn + dot(a, a) - 11) / 2)   # |d − a|² = |d|² + |a|² − 2a·d
add(('2026', 'Jan', '2026-01-24', 1), 'cross', 'Let a⃗ = 2î + ĵ − 2k̂, b⃗ = î + ĵ and c⃗ = a⃗ × b⃗. Let d⃗ be a vector such that |d⃗ − a⃗| = √{11}, |c⃗ × d⃗| = 3 and the angle between c⃗ and d⃗ is \\f{π}{4}. Then a⃗·d⃗ is equal to', ['11', '3', '0', '1'], 3,
    _d68, ['c⃗ = (2, −2, 1), |c⃗| = 3. |c⃗ × d⃗| = 3|d⃗| sin 45° = 3 → |d⃗| = √{2}.', '|d⃗ − a⃗|^{2} = 2 + 9 − 2a⃗·d⃗ = 11 → a⃗·d⃗ = 0.'], 'cross', 2)

# ---------- sheet 10
add(('2026', 'Apr', '2026-04-06', 2), 'cross', 'Let a⃗ = 2î + 3ĵ + 3k̂ and b⃗ = 6î + 3ĵ + 3k̂. Then the square of the area of the triangle with adjacent sides determined by the vectors (2a⃗ + 3b⃗) and (a⃗ − b⃗) is :', ['450', '900', '1800', '2400'], 3,
    lambda: (lambda a, b: P4([450, 900, 1800, 2400], (nrm(cross(addv(sc(2, a), sc(3, b)), sub(a, b))) / 2) ** 2))((2, 3, 3), (6, 3, 3)),
    ['(2a⃗ + 3b⃗) × (a⃗ − b⃗) = −2a⃗ × b⃗ + 3b⃗ × a⃗ = −5(a⃗ × b⃗).', 'a⃗ × b⃗ = (0, 12, −12), |…| = 12√{2}; area = \\f{1}{2}·5·12√{2} = 30√{2}.', 'Square = 1800.'], 'cross', 1)
def _c71():
    a, b = (2, -5, 5), (1, -1, 3); u = addv(sc(2, a), sc(3, b)); c = sc(-97 / dot(sub(a, b), u), u)   # (2a + 3b) × c = 0
    assert nrm(addv(sc(2, cross(a, c)), sc(3, cross(b, c)))) < 1e-9; k = cross(c, (0, 0, 1)); return P4([193, 233, 218, 205], dot(k, k))
add(('2026', 'Jan', '2026-01-24', 2), 'cross', 'Let a⃗ = 2î − 5ĵ + 5k̂ and b⃗ = î − ĵ + 3k̂. If c⃗ is a vector such that 2(a⃗ × c⃗) + 3(b⃗ × c⃗) = 0⃗ and (a⃗ − b⃗)·c⃗ = −97, then |c⃗ × k̂|^{2} is equal to', ['193', '233', '218', '205'], 3,
    _c71, ['(2a⃗ + 3b⃗) × c⃗ = 0 → c⃗ = t(7, −13, 19).', '(a⃗ − b⃗)·c⃗ = (1, −4, 2)·t(7, −13, 19) = 97t = −97 → t = −1.', 'c⃗ × k̂ = (c_{y}, −c_{x}, 0) → 169 + 49 = 218.'], 'cross', 2)
def _c72():
    a, b = (4, -1, 3), (10, 2, -1); t, = roots(lambda t: dot(a, sc(1 / 3, addv(sc(2, a), sc(t, b)))) - 15, -50, 50); c = sc(1 / 3, addv(sc(2, a), sc(t, b)))
    assert nrm(addv(sc(2, cross(a, b)), sc(3, cross(b, c)))) < 1e-9; return P4([-6, -5, -4, -3], dot(c, (1, 1, -3)))
add(('2026', 'Apr', '2026-04-08', 2), 'cross', 'Let a⃗ = 4î − ĵ + 3k̂, b⃗ = 10î + 2ĵ − k̂ and a vector c⃗ be such that 2(a⃗ × b⃗) + 3(b⃗ × c⃗) = 0⃗. If a⃗·c⃗ = 15, then c⃗·(î + ĵ − 3k̂) is equal to :', ['−6', '−5', '−4', '−3'], 2,
    _c72, ['b⃗ × (3c⃗ − 2a⃗) = 0 → 3c⃗ = 2a⃗ + tb⃗.', 'a⃗·c⃗: \\f{2·26 + 35t}{3} = 15 → t = −\\f{1}{5}.', 'c⃗·(1, 1, −3) = \\f{2(−6) − \\f{1}{5}·15}{3} = −5.'], 'cross', 2)
for _p in P: _p['t'] = _p['fam']
