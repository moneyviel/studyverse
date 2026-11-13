"""Real JEE Main questions — Mathematics Unit 11: Three Dimensional Geometry. Our own solutions; chk re-solves each
one numerically from the raw data — feet of perpendiculars by projecting onto the line, images by reflecting through
the foot, shortest distances from the cross product of the directions, and unknown parameters by scanning for every
root of the stated condition. Skipped: items that belong to other units and items we could not read reliably."""
import math, itertools
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
S2, S3, S5, S6 = math.sqrt(2), math.sqrt(3), math.sqrt(5), math.sqrt(6)
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def addv(a, b, k=1): return tuple(x + k * y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(dot(a, a))
def foot(Pt, A, d): t = dot(sub(Pt, A), d) / dot(d, d); return addv(A, d, t)
def image(Pt, A, d): Fo = foot(Pt, A, d); return tuple(2 * f - p for f, p in zip(Fo, Pt))
def dline(Pt, A, d): return nrm(sub(Pt, foot(Pt, A, d)))
def sd(A1, d1, A2, d2):
    n = cross(d1, d2)
    if nrm(n) < 1e-12: return nrm(cross(sub(A2, A1), d1)) / nrm(d1)
    return abs(dot(sub(A2, A1), n)) / nrm(n)
def meet(A1, d1, A2, d2):   # intersection point of two lines (least squares on the first two independent equations)
    best = None
    for i, j in ((0, 1), (0, 2), (1, 2)):
        D = d1[i] * (-d2[j]) - d1[j] * (-d2[i])
        if abs(D) > 1e-12:
            r = sub(A2, A1); s = (r[i] * (-d2[j]) - r[j] * (-d2[i])) / D; return addv(A1, d1, s)
    return best
def roots(f, lo, hi, n=20000):
    out = []; xs = [lo + (hi - lo) * k / n for k in range(n + 1)]
    for a, b in zip(xs, xs[1:]):
        fa, fb = f(a), f(b)
        if fa == 0: out.append(a)
        elif fa * fb < 0:
            for _ in range(100):
                m = (a + b) / 2
                if f(a) * f(m) <= 0: b = m
                else: a = m
            out.append((a + b) / 2)
    return out
def P4(opts, v, tol=1e-6): return pick(opts, round(v, 9), tol)
def near(x, y, t=1e-6): return abs(x - y) <= t * max(1, abs(y))

# ---------- sheet 1
add(('2025', 'Apr', '2025-04-02', 2), 'img', 'If the image of the point P(1, 0, 3) in the line joining the points A(4, 7, 1) and B(3, 5, 3) is Q(α, β, γ), then α + β + γ is equal to :', ['13', '\\f{47}{3}', '18', '\\f{46}{3}'], 4,
    lambda: P4([13, 47 / 3, 18, 46 / 3], sum(image((1, 0, 3), (4, 7, 1), sub((3, 5, 3), (4, 7, 1))))),
    ['Direction AB = (−1, −2, 2). Foot: t = \\f{(P − A)·d}{|d|^{2}} = \\f{21}{9} = \\f{7}{3} → F = (\\f{5}{3}, \\f{7}{3}, \\f{17}{3}).', 'Q = 2F − P = (\\f{7}{3}, \\f{14}{3}, \\f{25}{3}) → sum \\f{46}{3}.'], 'img', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'sd', 'Line L_{1} passes through the point (1, 2, 3) and is parallel to the z-axis. Line L_{2} passes through the point (λ, 5, 6) and is parallel to the y-axis. Let for λ = λ_{1}, λ_{2}, λ_{2} < λ_{1}, the shortest distance between the two lines be 3. Then the square of the distance of the point (λ_{1}, λ_{2}, 7) from the line L_{1} is', ['37', '32', '40', '25'], 4,
    lambda: (lambda R: P4([37, 32, 40, 25], dline((R[1], R[0], 7), (1, 2, 3), (0, 0, 1)) ** 2))(roots(lambda l: sd((1, 2, 3), (0, 0, 1), (l, 5, 6), (0, 1, 0)) - 3, -20, 20, 4001)),
    ['Directions (0, 0, 1) and (0, 1, 0): the common perpendicular is along x, so the shortest distance is |λ − 1| = 3 → λ = 4, −2.', 'Point (4, −2, 7); L_{1} is x = 1, y = 2 → distance^{2} = 3^{2} + 4^{2} = 25.'], 'sd', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'sd', 'Let the shortest distance between the lines \\f{x − 3}{3} = \\f{y − α}{−1} = \\f{z − 3}{1} and \\f{x + 3}{−3} = \\f{y + 7}{2} = \\f{z − β}{4} be 3√{30}. Then the positive value of 5α + β is', ['48', '42', '40', '46'], 4,
    lambda: P4([48, 42, 40, 46], max(roots(lambda s: sd((3, 0, 3), (3, -1, 1), (-3, -7, s), (-3, 2, 4)) - 3 * math.sqrt(30), -500, 500, 20001))),
    ['d_{1} × d_{2} = (−6, −15, 3), |n| = 3√{30}.', '(A_{2} − A_{1})·n = 36 + 105 + 15α + 3β − 9 = 132 + 3(5α + β).', '|132 + 3(5α + β)| = 270 → 5α + β = 46 or −134. Positive: 46.'], 'sd', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'sd', 'Let the values of p, for which the shortest distance between the lines \\f{x + 1}{3} = \\f{y}{4} = \\f{z}{5} and r⃗ = (pî + 2ĵ + k̂) + λ(2î + 3ĵ + 4k̂) is \\f{1}{√{6}}, be a, b (a < b). Then the length of the latus rectum of the ellipse \\f{x^{2}}{a^{2}} + \\f{y^{2}}{b^{2}} = 1 is :', ['\\f{2}{3}', '18', '9', '\\f{3}{2}'], 1,
    lambda: (lambda R: P4([2 / 3, 18, 9, 1.5], 2 * min(abs(R[0]), abs(R[1])) ** 2 / max(abs(R[0]), abs(R[1]))))(roots(lambda p: sd((-1, 0, 0), (3, 4, 5), (p, 2, 1), (2, 3, 4)) - 1 / S6, -50, 50, 10001)),
    ['n = (3, 4, 5) × (2, 3, 4) = (1, −2, 1), |n| = √{6}.', '(p + 1, 2, 1)·n = p − 2 → |p − 2| = 1 → a = 1, b = 3.', 'Major axis along y: latus rectum \\f{2a^{2}}{b} = \\f{2}{3}.'], 'sd', 2)

# ---------- sheet 2
def fl(x):   # ∫_0^k [x²] dx
    s, j = 0.0, 0
    while math.sqrt(j) < x: s += j * (min(math.sqrt(j + 1), x) - math.sqrt(j)); j += 1
    return s
add(('2024', 'Apr', '2024-04-04', 1), 'sd', 'If the shortest distance between the lines \\f{x + 2}{2} = \\f{y + 3}{3} = \\f{z − 5}{4} and \\f{x − 3}{1} = \\f{y − 2}{−3} = \\f{z + 4}{2} is \\f{38}{3√{5}}k and ∫_{0}^{k} [x^{2}] dx = α − √{α}, where [x] denotes the greatest integer function, then 6α^{3} is equal to', None, 48,
    lambda: (lambda k: (lambda v: round(6 * roots(lambda a: a - math.sqrt(a) - v, 1, 50)[0] ** 3))(fl(k)))(sd((-2, -3, 5), (2, 3, 4), (3, 2, -4), (1, -3, 2)) / (38 / (3 * S5))),
    ['n = (2, 3, 4) × (1, −3, 2) = (18, 0, −9), |n| = 9√{5}; (5, 5, −9)·n = 171 → distance \\f{19}{√{5}} → k = \\f{3}{2}.', '∫_{0}^{3/2}[x^{2}]dx = (√{2} − 1)·1 + (\\f{3}{2} − √{2})·2 = 2 − √{2}.', 'So α = 2 and 6α^{3} = 48.'], 'sd', 2)
def sdpts(A1, d1, A2, d2):   # feet of the common perpendicular
    r = sub(A1, A2); a, b, c = dot(d1, d1), dot(d1, d2), dot(d2, d2); d, e = dot(d1, r), dot(d2, r); D = a * c - b * b
    s, t = (b * e - c * d) / D, (a * e - b * d) / D; return addv(A1, d1, s), addv(A2, d2, t)
add(('2024', 'Apr', '2024-04-05', 2), 'sd', 'Let the point (−1, α, β) lie on the line of the shortest distance between the lines \\f{x + 2}{−3} = \\f{y − 2}{4} = \\f{z − 5}{2} and \\f{x + 2}{−1} = \\f{y + 6}{2} = \\f{z − 1}{0}. Then (α − β)^{2} is equal to', None, 25,
    lambda: (lambda U: (lambda t: round((U[0][1] + t * (U[1][1] - U[0][1]) - U[0][2] - t * (U[1][2] - U[0][2])) ** 2, 6))((-1 - U[0][0]) / (U[1][0] - U[0][0])))(sdpts((-2, 2, 5), (-3, 4, 2), (-2, -6, 1), (-1, 2, 0))),
    ['Common perpendicular direction n = (−3, 4, 2) × (−1, 2, 0) = (−4, −2, −2) ∥ (2, 1, 1).', 'Its feet (where the joining vector is ⟂ to both lines): (1, −2, 3) and (−3, −4, 1). The line: (1, −2, 3) + t(2, 1, 1).', 'x = −1 → t = −1 → (−1, −3, 2): (α − β)^{2} = 25.'], 'sd', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'img', 'Let P(α, β, γ) be the image of the point Q(3, −3, 1) in the line \\f{x − 0}{1} = \\f{y − 3}{1} = \\f{z − 1}{−1} and R be the point (2, 5, −1). If the area of the triangle PQR is λ and λ^{2} = 14K, then K is equal to:', ['36', '72', '18', '81'], 4,
    lambda: (lambda Pp: P4([36, 72, 18, 81], (nrm(cross(sub(Pp, (3, -3, 1)), sub((2, 5, -1), (3, -3, 1)))) / 2) ** 2 / 14))(image((3, -3, 1), (0, 3, 1), (1, 1, -1))),
    ['Foot of Q: t = \\f{(3, −6, 0)·(1, 1, −1)}{3} = −1 → F = (−1, 2, 2); image P = 2F − Q = (−5, 7, 3).', 'R lies on the line (t = 2), and QP ⟂ line, so area = \\f{1}{2}·QP·RF = \\f{1}{2}·2√{42}·√{27}.', 'λ^{2} = 42·27 = 1134 = 14·81 → K = 81.'], 'img', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'sd', 'If the shortest distance between the lines \\f{x − λ}{3} = \\f{y − 2}{−1} = \\f{z − 1}{1} and \\f{x + 2}{−3} = \\f{y + 5}{2} = \\f{z − 4}{4} is \\f{44}{√{30}}, then the largest possible value of |λ| is equal to', None, 43,
    lambda: round(max(abs(r) for r in roots(lambda l: sd((l, 2, 1), (3, -1, 1), (-2, -5, 4), (-3, 2, 4)) - 44 / math.sqrt(30), -200, 200, 40001))),
    ['n = (3, −1, 1) × (−3, 2, 4) = (−6, −15, 3), |n| = 3√{30}.', '(−2 − λ, −7, 3)·n = 12 + 6λ + 105 + 9 = 6λ + 126.', '|6λ + 126| = 132 → λ = 1 or −43. Largest |λ| = 43.'], 'sd', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'sd', 'The shortest distance between the lines \\f{x − 3}{2} = \\f{y + 15}{−7} = \\f{z − 9}{5} and \\f{x + 1}{2} = \\f{y − 1}{1} = \\f{z − 9}{−3} is ______.', ['6√{3}', '4√{3}', '5√{3}', '8√{3}'], 2,
    lambda: P4([6 * S3, 4 * S3, 5 * S3, 8 * S3], sd((3, -15, 9), (2, -7, 5), (-1, 1, 9), (2, 1, -3))),
    ['n = (2, −7, 5) × (2, 1, −3) = (16, 16, 16) ∥ (1, 1, 1).', '(A_{2} − A_{1}) = (−4, 16, 0); dot with (1, 1, 1) = 12 → \\f{12}{√{3}} = 4√{3}.'], 'sd', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'sd', 'If the shortest distance between the lines \\f{x − 1}{2} = \\f{y − 2}{3} = \\f{z − 3}{4} and \\f{x}{1} = \\f{y}{α} = \\f{z − 5}{1} is \\f{5}{√{6}}, then the sum of all possible values of α is', ['\\f{3}{2}', '−3', '−\\f{3}{2}', '3'], 2,
    lambda: P4([1.5, -3, -1.5, 3], sum(roots(lambda a: sd((1, 2, 3), (2, 3, 4), (0, 0, 5), (1, a, 1)) - 5 / S6, -100, 100, 40001))),
    ['n = (2, 3, 4) × (1, α, 1) = (3 − 4α, 2, 2α − 3).', '(−1, −2, 2)·n = 4α − 3 − 4 + 4α − 6 = 8α − 13; |n|^{2} = 20α^{2} − 36α + 22.', 'Square: 6(8α − 13)^{2} = 25(20α^{2} − 36α + 22) → 116α^{2} + 348α − 464 = 0 → α^{2} + 3α − 4 = 0.', 'α = 1 or −4: sum −3.'], 'sd', 3)

# ---------- sheet 3
def circR(A, B, C):
    a, b, c = math.dist(B, C), math.dist(A, C), math.dist(A, B); s = (a + b + c) / 2; return a * b * c / (4 * math.sqrt(s * (s - a) * (s - b) * (s - c)))
add(('2025', 'Apr', '2025-04-08', 2), 'sd', 'Let the values of λ for which the shortest distance between the lines \\f{x − 1}{2} = \\f{y − 2}{3} = \\f{z − 3}{4} and \\f{x − λ}{3} = \\f{y − 4}{4} = \\f{z − 5}{5} is \\f{1}{√{6}} be λ_{1} and λ_{2}. Then the radius of the circle passing through the points (0, 0), (λ_{1}, λ_{2}) and (λ_{2}, λ_{1}) is', ['3', '4', '\\f{5√{2}}{3}', '\\f{√{2}}{3}'], 3,
    lambda: (lambda R: P4([3, 4, 5 * S2 / 3, S2 / 3], circR((0, 0), (R[0], R[1]), (R[1], R[0]))))(roots(lambda l: sd((1, 2, 3), (2, 3, 4), (l, 4, 5), (3, 4, 5)) - 1 / S6, -100, 100, 40001)),
    ['n = (2, 3, 4) × (3, 4, 5) = (−1, 2, −1), |n| = √{6}.', '(λ − 1, 2, 2)·n = 1 − λ + 4 − 2 = 3 − λ → |3 − λ| = 1 → λ = 2, 4.', 'Circle through (0, 0), (2, 4), (4, 2): centre (\\f{5}{3}, \\f{5}{3}) → r = \\f{5√{2}}{3}.'], 'sd', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'sd', 'If the shortest distance between the lines \\f{x − λ}{2} = \\f{y − 4}{3} = \\f{z − 3}{4} and \\f{x − 2}{4} = \\f{y − 4}{6} = \\f{z − 7}{8} is \\f{13}{√{29}}, then a value of λ is :', ['−\\f{13}{25}', '\\f{13}{25}', '1', '−1'], 3,
    lambda: (lambda R: P4([-13 / 25, 13 / 25, 1, -1], [r for r in R if min(abs(r - v) for v in (-13 / 25, 13 / 25, 1, -1)) < 1e-6][0]))(roots(lambda l: sd((l, 4, 3), (2, 3, 4), (2, 4, 7), (4, 6, 8)) - 13 / math.sqrt(29), -100, 100, 40001)),
    ['The lines are parallel (direction (2, 3, 4)). Distance = \\f{|(A_{2} − A_{1}) × d|}{|d|} with A_{2} − A_{1} = (2 − λ, 0, 4).', '(2 − λ, 0, 4) × (2, 3, 4) = (−12, 4λ, 6 − 3λ); |…|^{2} = 144 + 16λ^{2} + (6 − 3λ)^{2}.', 'Set \\f{…}{29} = \\f{169}{29}: 25λ^{2} − 36λ + 11 = 0 → λ = 1 or \\f{11}{25}. A value: 1.'], 'sd', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'img', 'Let P(α, β, γ) be the image of the point Q(1, 6, 4) in the line \\f{x}{1} = \\f{y − 1}{2} = \\f{z − 2}{3}. Then 2α + β + γ is equal to', None, 11,
    lambda: (lambda I: round(2 * I[0] + I[1] + I[2], 6))(image((1, 6, 4), (0, 1, 2), (1, 2, 3))),
    ['Foot: t = \\f{(1, 5, 2)·(1, 2, 3)}{14} = \\f{17}{14} → F = (\\f{17}{14}, \\f{24}{7}, \\f{79}{14}).', 'Image = 2F − Q = (\\f{10}{7}, \\f{6}{7}, \\f{51}{7}) → 2α + β + γ = \\f{77}{7} = 11.'], 'img', 1)

# ---------- sheet 4
def _oct():
    g, th, ph = 2.3, 0.4, 0.9; Pt = (g * math.sin(ph) * math.cos(th), g * math.sin(ph) * math.sin(th), g * math.cos(ph)); d = math.hypot(Pt[1], Pt[2])
    ops = [g * math.sqrt(1 - math.sin(ph) ** 2 * math.cos(th) ** 2), g * math.sqrt(1 + math.cos(th) ** 2 * math.sin(ph) ** 2), g * math.sqrt(1 - math.sin(th) ** 2 * math.cos(ph) ** 2), g * math.sqrt(1 + math.cos(ph) ** 2 * math.sin(th) ** 2)]
    return pick(ops, d, 1e-9)
add(('2024', 'Apr', '2024-04-08', 1), 'line3', 'Let P(x, y, z) be a point in the first octant, whose projection in the xy-plane is the point Q. Let OP = γ; the angle between OQ and the positive x-axis be θ; and the angle between OP and the positive z-axis be φ, where O is the origin. Then the distance of P from the x-axis is :', ['γ√{1 − sin^{2}φ cos^{2}θ}', 'γ√{1 + cos^{2}θ sin^{2}φ}', 'γ√{1 − sin^{2}θ cos^{2}φ}', 'γ√{1 + cos^{2}φ sin^{2}θ}'], 1,
    _oct, ['OQ = γ sin φ, so x = γ sin φ cos θ.', 'Distance from the x-axis = √{y^{2} + z^{2}} = √{γ^{2} − x^{2}} = γ√{1 − sin^{2}φ cos^{2}θ}.'], 'line3', 2)
def _mn():
    d1, d2 = (1, -3, 4), (2, 3, 1); N = cross(d1, d2); v = F(dot(sub((2, 3, 5), (2, 1, 3)), N) ** 2, dot(N, N)); m = math.isqrt(v.numerator); assert m * m == v.numerator
    return P4([384, 387, 377, 390], m + v.denominator)
add(('2024', 'Apr', '2024-04-08', 1), 'sd', 'If the shortest distance between the lines L_{1} : r⃗ = (2 + λ)î + (1 − 3λ)ĵ + (3 + 4λ)k̂, λ ∈ ℝ and L_{2} : r⃗ = 2(1 + μ)î + 3(1 + μ)ĵ + (5 + μ)k̂, μ ∈ ℝ is \\f{m}{√{n}}, where gcd(m, n) = 1, then the value of m + n equals', ['384', '387', '377', '390'], 2,
    _mn, ['L_{1}: (2, 1, 3) + λ(1, −3, 4); L_{2}: (2, 3, 5) + μ(2, 3, 1).', 'n = (−15, 7, 9), |n| = √{355}; (0, 2, 2)·n = 32.', 'Distance \\f{32}{√{355}} → m + n = 387.'], 'sd', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'img', 'The square of the distance of the image of the point (6, 1, 5) in the line \\f{x − 1}{3} = \\f{y}{2} = \\f{z − 2}{4}, from the origin is', None, 62,
    lambda: round(dot(image((6, 1, 5), (1, 0, 2), (3, 2, 4)), image((6, 1, 5), (1, 0, 2), (3, 2, 4))), 6),
    ['Foot: t = \\f{(5, 1, 3)·(3, 2, 4)}{29} = 1 → F = (4, 2, 6).', 'Image = (2, 3, 7) → distance^{2} = 4 + 9 + 49 = 62.'], 'img', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'sd', 'The shortest distance between the line \\f{x − 3}{4} = \\f{y + 7}{−11} = \\f{z − 1}{5} and \\f{x − 5}{3} = \\f{y − 9}{−6} = \\f{z + 2}{1} is :', ['\\f{187}{√{563}}', '\\f{178}{√{563}}', '\\f{185}{√{563}}', '\\f{179}{√{563}}'], 1,
    lambda: P4([187 / math.sqrt(563), 178 / math.sqrt(563), 185 / math.sqrt(563), 179 / math.sqrt(563)], sd((3, -7, 1), (4, -11, 5), (5, 9, -2), (3, -6, 1))),
    ['n = (4, −11, 5) × (3, −6, 1) = (19, 11, 9), |n| = √{563}.', '(2, 16, −3)·n = 38 + 176 − 27 = 187.'], 'sd', 1)
def _ab():
    hit = []
    for a in range(-20, 21):
        for b in range(-20, 21):
            d1, d2, A1, A2 = (3, 5, 7), (1, 4, 7), (-1, -a, -b - 1), (2, b, 2 * a)
            if nrm(cross(d1, d2)) and sd(A1, d1, A2, d2) < 1e-9:
                X = meet(A1, d1, A2, d2)
                if abs(X[2]) < 1e-9: hit.append(a + b)
    assert len(set(hit)) == 1; return P4([2, 5, 7, 9], hit[0])
add(('2026', 'Apr', '2026-04-02', 1), 'line3', 'If the point of intersection of the lines \\f{x + 1}{3} = \\f{y + a}{5} = \\f{z + b + 1}{7} and \\f{x − 2}{1} = \\f{y − b}{4} = \\f{z − 2a}{7} lies on xy-plane, then the value of a + b is :', ['2', '5', '7', '9'], 3,
    _ab, ['Put z = 0 in each line: first gives t = \\f{b + 1}{7}, second gives s = −\\f{2a}{7}.', 'Match x: −1 + \\f{3(b + 1)}{7} = 2 − \\f{2a}{7} → 2a + 3b = 18. Match y: −a + \\f{5(b + 1)}{7} = b − \\f{8a}{7} → a − 2b = −5.', 'a = 3, b = 4 → a + b = 7.'], 'line3', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'line3', 'Let a line L passing through the point (1, 1, 1) be perpendicular to both the vectors 2î + 2ĵ + k̂ and î + 2ĵ + 2k̂. If P(a, b, c) is the foot of perpendicular from the origin on the line L, then the value of 34(a + b + c) is :', ['50', '80', '100', '120'], 3,
    lambda: P4([50, 80, 100, 120], 34 * sum(foot((0, 0, 0), (1, 1, 1), cross((2, 2, 1), (1, 2, 2))))),
    ['Direction = (2, 2, 1) × (1, 2, 2) = (2, −3, 2).', 'Foot from O: t = −\\f{(1, 1, 1)·(2, −3, 2)}{17} = −\\f{1}{17} → P = (\\f{15}{17}, \\f{20}{17}, \\f{15}{17}).', '34·\\f{50}{17} = 100.'], 'line3', 1)

# ---------- sheet 5
add(('2026', 'Jan', '2026-01-28', 2), 'img', 'Let Q(a, b, c) be the image of the point P(3, 2, 1) in the line \\f{x − 1}{1} = \\f{y}{2} = \\f{z − 1}{1}. Then the distance of Q from the line \\f{x − 9}{3} = \\f{y − 9}{2} = \\f{z − 5}{−2} is', ['6', '7', '8', '5'], 2,
    lambda: P4([6, 7, 8, 5], dline(image((3, 2, 1), (1, 0, 1), (1, 2, 1)), (9, 9, 5), (3, 2, -2))),
    ['Foot of P: t = \\f{(2, 2, 0)·(1, 2, 1)}{6} = 1 → F = (2, 2, 2); Q = 2F − P = (1, 2, 3).', 'From A = (9, 9, 5): Q − A = (−8, −7, −2); projection on (3, 2, −2)/√{17} is −34/√{17} = −2√{17}.', 'Distance^{2} = 117 − 68 = 49 → 7.'], 'img', 2)
def _al():
    for s in (13, -13):   # P + s(3, −1, 0)/… : the step along (3, −1, 0) has length |s|√10
        mu = (43 + 3 * s - 4) / 2; al = s; be = -1 + 3 * mu   # land on 4 + 2μ, 0, −1 + 3μ
        if be < 0 and abs(math.hypot(3 * s, s) - 13 * math.sqrt(10)) < 1e-9: return round(al * al + be * be)
add(('2026', 'Jan', '2026-01-28', 2), 'line3', 'If the distance of the point P(43, α, β), β < 0, from the line r⃗ = 4î − k̂ + μ(2î + 3k̂), μ ∈ ℝ along a line with direction ratios 3, −1, 0 is 13√{10}, then α^{2} + β^{2} is equal to', None, 170,
    _al, ['Move from P along (3, −1, 0): (43 + 3s, α − s, β) must lie on the line (4 + 2μ, 0, −1 + 3μ); the distance is |s|√{10} = 13√{10} → s = ±13.', 's = 13 gives μ = 39, β = 116 > 0 ✗. s = −13 gives μ = 0, β = −1, α = −13.', 'α^{2} + β^{2} = 169 + 1 = 170.'], 'line3', 2)
def _onsd():
    U = sdpts((1, 2, 3), (2, 3, 4), (2, 4, 5), (3, 4, 5)); d = sub(U[1], U[0])
    ops = [(-5 / 3, -7, 1), (8 / 3, -1, 1 / 3), (2, 3, 1 / 3), (14 / 3, -3, 22 / 3)]; hit = [i + 1 for i, o in enumerate(ops) if nrm(cross(sub(o, U[0]), d)) < 1e-9]
    assert len(hit) == 1; return hit[0]
add(('2025', 'Jan', '2025-01-22', 1), 'sd', 'Let L_{1} : \\f{x − 1}{2} = \\f{y − 2}{3} = \\f{z − 3}{4} and L_{2} : \\f{x − 2}{3} = \\f{y − 4}{4} = \\f{z − 5}{5} be two lines. Then which of the following points lies on the line of the shortest distance between L_{1} and L_{2} ?', ['(−\\f{5}{3}, −7, 1)', '(\\f{8}{3}, −1, \\f{1}{3})', '(2, 3, \\f{1}{3})', '(\\f{14}{3}, −3, \\f{22}{3})'], 4,
    _onsd, ['Common perpendicular direction: (2, 3, 4) × (3, 4, 5) = (−1, 2, −1).', 'Points (1 + 2s, 2 + 3s, 3 + 4s), (2 + 3t, 4 + 4t, 5 + 5t); the joining vector ⟂ both lines gives s = \\f{1}{3}, t = −\\f{1}{6}: foot (\\f{5}{3}, 3, \\f{13}{3}).', '(\\f{14}{3}, −3, \\f{22}{3}) − (\\f{5}{3}, 3, \\f{13}{3}) = (3, −6, 3) ∥ (1, −2, 1) ✓.'], 'sd', 3)
add(('2025', 'Jan', '2025-01-23', 1), 'img', 'Let P be the foot of the perpendicular from the point Q(10, −3, −1) on the line \\f{x − 3}{7} = \\f{y − 2}{−1} = \\f{z + 1}{−2}. Then the area of the right angled triangle PQR, where R is the point (3, −2, 1), is', ['8√{15}', '√{30}', '3√{30}', '9√{15}'], 3,
    lambda: (lambda Pp: P4([8 * math.sqrt(15), math.sqrt(30), 3 * math.sqrt(30), 9 * math.sqrt(15)], nrm(cross(sub((10, -3, -1), Pp), sub((3, -2, 1), Pp))) / 2))(foot((10, -3, -1), (3, 2, -1), (7, -1, -2))),
    ['Foot: t = \\f{(7, −5, 0)·(7, −1, −2)}{54} = 1 → P = (10, 1, −3).', 'QP = (0, 4, −2) and QR = (−7, 1, 2) are perpendicular: right angle at Q.', 'Area = \\f{1}{2}·√{20}·√{54} = 3√{30}.'], 'img', 2)

# ---------- sheet 6
def solve3(M, b):
    def det(m): return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    D = det(M); return [det([[b[r] if c == j else M[r][c] for c in range(3)] for r in range(3)]) / D for j in range(3)]
def transversal(A1, d1, A2, d2, v):   # a line along v meeting both lines: A1 + s d1 + k v = A2 + t d2
    s, t, k = solve3([[d1[i], -d2[i], v[i]] for i in range(3)], sub(A2, A1)); return addv(A1, d1, s), addv(A2, d2, t)
add(('2025', 'Jan', '2025-01-24', 2), 'img', 'Let P be the image of the point Q(7, −2, 5) in the line L : \\f{x − 1}{2} = \\f{y + 1}{3} = \\f{z}{4} and R(5, p, q) be a point on L. Then the square of the area of △PQR is ________.', None, 957,
    lambda: (lambda Pp, R: round((nrm(cross(sub(Pp, (7, -2, 5)), sub(R, (7, -2, 5)))) / 2) ** 2, 6))(image((7, -2, 5), (1, -1, 0), (2, 3, 4)), addv((1, -1, 0), (2, 3, 4), (5 - 1) / 2)),
    ['Foot of Q: t = \\f{(6, −1, 5)·(2, 3, 4)}{29} = 1 → F = (3, 2, 4); P = 2F − Q = (−1, 6, 3).', 'R on L with x = 5: R = (5, 5, 8).', 'QP ⟂ L, so area = \\f{1}{2}·QP·FR = \\f{1}{2}·2√{33}·√{29}.', 'Area^{2} = 33·29 = 957.'], 'img', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'img', 'If the image of the point (4, 4, 3) in the line \\f{x − 1}{2} = \\f{y − 2}{1} = \\f{z − 1}{3} is (α, β, γ), then α + β + γ is equal to', ['9', '8', '12', '7'], 1,
    lambda: P4([9, 8, 12, 7], sum(image((4, 4, 3), (1, 2, 1), (2, 1, 3)))),
    ['Foot: t = \\f{(3, 2, 2)·(2, 1, 3)}{14} = 1 → F = (3, 3, 4).', 'Image = 2F − P = (2, 2, 5) → sum 9.'], 'img', 1)
def _s12():
    pts = [(0, 3, 2), (2, 0, 3), (0, 0, 1)]; best = None
    for x2 in range(-40, 41):
        for y2 in range(-40, 41):
            A = (x2 / 2, y2 / 2, 0); d = [nrm(sub(A, p)) for p in pts]
            if max(d) - min(d) < 1e-9: best = A
    B, C = (1, 4, -1), (2, 0, -2); s = sorted(dot(sub(u, v), sub(u, v)) for u, v in ((best, B), (B, C), (best, C)))
    s1 = abs(s[0] - s[1]) < 1e-9 and abs(s[0] + s[1] - s[2]) < 1e-9; s2 = abs(nrm(cross(sub(B, best), sub(C, best))) / 2 - 9 * S2 / 2) < 1e-9
    return {(False, True): 1, (False, False): 2, (True, True): 3, (True, False): 4}[(s1, s2)]
add(('2025', 'Jan', '2025-01-28', 1), 'line3', 'Let A(x, y, z) be a point in xy-plane, which is equidistant from three points (0, 3, 2), (2, 0, 3) and (0, 0, 1). Let B = (1, 4, −1) and C = (2, 0, −2). Then among the statements (S1): △ABC is an isosceles right angled triangle, and (S2): the area of △ABC is \\f{9√{2}}{2}', ['only (S2) is true', 'both are false', 'both are true', 'only (S1) is true'], 4,
    _s12, ['With z = 0: |A − (0, 3, 2)|^{2} = |A − (0, 0, 1)|^{2} → −6y + 13 = 1 → y = 2; |A − (2, 0, 3)|^{2} = |A − (0, 0, 1)|^{2} → −4x + 12 = 0 → x = 3.', 'AB^{2} = 9, AC^{2} = 9, BC^{2} = 18 → isosceles right-angled at A (S1 true).', 'Area = \\f{1}{2}·3·3 = \\f{9}{2} ≠ \\f{9√{2}}{2} (S2 false).'], 'line3', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'line3', 'Let a straight line L pass through the point P(2, −1, 3) and be perpendicular to the lines \\f{x − 1}{2} = \\f{y + 1}{1} = \\f{z − 3}{−2} and \\f{x − 3}{1} = \\f{y − 2}{3} = \\f{z + 2}{4}. If the line L intersects the yz-plane at the point Q, then the distance between the points P and Q is :', ['2√{3}', '3', '2', '√{10}'], 2,
    lambda: (lambda d: P4([2 * S3, 3, 2, math.sqrt(10)], nrm(sub(addv((2, -1, 3), d, -2 / d[0]), (2, -1, 3)))))(cross((2, 1, -2), (1, 3, 4))),
    ['Direction = (2, 1, −2) × (1, 3, 4) = (10, −10, 5) ∥ (2, −2, 1).', 'From P, x = 0 at t = −1: Q = (0, 1, 2).', 'PQ = √{4 + 4 + 1} = 3.'], 'line3', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'img', 'Let P be the foot of the perpendicular from the point (1, 2, 2) on the line L : \\f{x − 1}{1} = \\f{y + 1}{−1} = \\f{z − 2}{2}. Let the line r⃗ = (−î + ĵ − 2k̂) + λ(î − ĵ + k̂), λ ∈ ℝ, intersect the line L at Q. Then 2(PQ)^{2} is equal to:', ['19', '29', '25', '27'], 4,
    lambda: (lambda Pp, Q: P4([19, 29, 25, 27], 2 * dot(sub(Pp, Q), sub(Pp, Q))))(foot((1, 2, 2), (1, -1, 2), (1, -1, 2)), transversal((1, -1, 2), (1, -1, 2), (-1, 1, -2), (1, -1, 1), cross((1, -1, 2), (1, -1, 1)))[0]),
    ['Foot: t = \\f{(0, 3, 0)·(1, −1, 2)}{6} = −\\f{1}{2} → P = (\\f{1}{2}, −\\f{1}{2}, 1).', 'Meet: 1 + t = −1 + λ, −1 − t = 1 − λ, 2 + 2t = −2 + λ → t = −2, Q = (−1, 1, −2).', 'PQ^{2} = \\f{9}{4} + \\f{9}{4} + 9 = \\f{27}{2} → 2PQ^{2} = 27.'], 'img', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'line3', 'A line with direction ratios 1, −1, 2 intersects the lines \\f{x}{2} = \\f{y}{3} = \\f{z + 1}{3} and \\f{x + 1}{−1} = \\f{y − 2}{1} = \\f{z}{4} at the points P and Q, respectively. If the length of the line segment PQ is α, then 225α^{2} is equal to:', ['1024', '1014', '1104', '1204'], 2,
    lambda: (lambda U: P4([1024, 1014, 1104, 1204], 225 * dot(sub(U[0], U[1]), sub(U[0], U[1]))))(transversal((0, 0, -1), (2, 3, 3), (-1, 2, 0), (-1, 1, 4), (1, -1, 2))),
    ['P = (2s, 3s, −1 + 3s), Q = (−1 − t, 2 + t, 4t); Q − P = k(1, −1, 2).', 'Adding the x and y equations: 1 − 5s = 0 → s = \\f{1}{5}; then t = −\\f{8}{15}, k = −\\f{13}{15}.', 'α^{2} = 6k^{2} = \\f{1014}{225} → 225α^{2} = 1014.'], 'line3', 2)

# ---------- sheet 7
def _img37():
    for a in range(-60, 61):
        Q = image((1, 2, a), (6, 7, 7), (3, 2, -2))
        if abs(Q[0] - 5) < 1e-9: return P4([293, 264, 298, 283], a * a + Q[1] ** 2 + Q[2] ** 2)
add(('2026', 'Jan', '2026-01-22', 1), 'img', 'If the image of the point P(1, 2, a) in the line \\f{x − 6}{3} = \\f{y − 7}{2} = \\f{7 − z}{2} is Q(5, b, c), then a^{2} + b^{2} + c^{2} is equal to', ['293', '264', '298', '283'], 3,
    _img37, ['The line is (6, 7, 7) + t(3, 2, −2). The mid-point of PQ, (3, \\f{2 + b}{2}, \\f{a + c}{2}), lies on it: t = −1 → b = 8, a + c = 18.', 'PQ = (4, b − 2, c − a) ⟂ (3, 2, −2): 12 + 12 − 2(c − a) = 0 → c − a = 12.', 'a = 3, c = 15 → 9 + 64 + 225 = 298.'], 'img', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'sd', 'The shortest distance between the lines r⃗ = (\\f{1}{3}î + 2ĵ + \\f{8}{3}k̂) + λ(2î − 5ĵ + 6k̂) and r⃗ = (−\\f{2}{3}î − \\f{1}{3}k̂) + μ(ĵ − k̂), λ, μ ∈ ℝ, is:', ['√{5}', '3', '2√{3}', '√{15}'], 2,
    lambda: P4([S5, 3, 2 * S3, math.sqrt(15)], sd((1 / 3, 2, 8 / 3), (2, -5, 6), (-2 / 3, 0, -1 / 3), (0, 1, -1))),
    ['n = (2, −5, 6) × (0, 1, −1) = (−1, 2, 2), |n| = 3.', 'A_{2} − A_{1} = (−1, −2, −3); dot with n = 1 − 4 − 6 = −9 → distance 3.'], 'sd', 1)
def _dc():
    dirs = []
    for r in roots(lambda m: 2 * m * (4 + m) + 10 * (4 + m) + 3 * m, -50, 50, 20001):   # l = 1, n = 4 + m
        dirs.append((1, r, 4 + r))
    c = abs(dot(*dirs)) / (nrm(dirs[0]) * nrm(dirs[1])); return P4([10 / math.sqrt(38), 20 / (3 * math.sqrt(38)), 10 / (7 * math.sqrt(38)), 10 / (3 * math.sqrt(38))], c)
add(('2026', 'Jan', '2026-01-23', 1), 'line3', 'Let the direction cosines of two lines satisfy the equations : 4l + m − n = 0 and 2mn + 10nl + 3lm = 0. Then the cosine of the acute angle between these lines is :', ['\\f{10}{√{38}}', '\\f{20}{3√{38}}', '\\f{10}{7√{38}}', '\\f{10}{3√{38}}'], 4,
    _dc, ['n = 4l + m. Substitute: 2m^{2} + 21lm + 40l^{2} = 0 → \\f{m}{l} = −\\f{5}{2} or −8.', 'Directions (2, −5, 3) and (1, −8, −4).', 'cos θ = \\f{|2 + 40 − 12|}{√{38}·9} = \\f{10}{3√{38}}.'], 'line3', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'img', 'If the distance of the point (a, 2, 5) from the image of the point (1, 2, 7) in the line \\f{x}{1} = \\f{y − 1}{1} = \\f{z − 2}{2} is 4, then the sum of all possible values of a is equal to :', ['11', '9', '6', '4'], 3,
    lambda: P4([11, 9, 6, 4], sum(roots(lambda a: nrm(sub((a, 2, 5), image((1, 2, 7), (0, 1, 2), (1, 1, 2)))) - 4, -50, 50, 10001))),
    ['Foot: t = \\f{(1, 1, 5)·(1, 1, 2)}{6} = 2 → F = (2, 3, 6); image (3, 4, 5).', '(a − 3)^{2} + 4 + 0 = 16 → a = 3 ± 2√{3}; sum 6.'], 'img', 1)
def _ab42():
    h = set()
    for a2 in range(-60, 61):
        for b2 in range(-60, 61):
            a, b = a2 / 2, b2 / 2; Pp = (a, 2, a); Q = image(Pp, (0, -a, 0), (2, 1, 1))
            if nrm(sub(image(Q, (2 * b, a, -2 * b), (2, 1, -5)), Pp)) < 1e-9: h.add(a + b)
    assert len(h) == 1; return round(h.pop(), 6)
add(('2026', 'Jan', '2026-01-23', 2), 'img', 'If the image of the point P(a, 2, a) in the line \\f{x}{2} = \\f{y + a}{1} = \\f{z}{1} is Q and the image of Q in the line \\f{x − 2b}{2} = \\f{y − a}{1} = \\f{z + 2b}{−5} is P, then a + b is equal to ________.', None, 3,
    _ab42, ['P and Q are mirror images in both lines, so the mid-point M of PQ lies on both lines and PQ ⟂ both directions.', 'PQ ∥ (2, 1, 1) × (2, 1, −5) = (−6, 12, 0) ∥ (1, −2, 0).', 'Meeting point of the lines with P − M ∥ (1, −2, 0) gives a = 1, b = 2 (M = (2, 0, 1), Q = (3, −2, 1)): a + b = 3.'], 'img', 3)

# ---------- sheet 8
def _s43():
    hits = []
    for a in range(-30, 31):
        for bn in range(1, 61):
            b = bn / 2; I = image((1, 6, a), (0, 1, a - 1), (1, 2, b))
            if abs(I[0] - a / 3) < 1e-9 and abs(I[1]) < 1e-9: hits.append((a, b))
    (a, b), = hits; d = (1, 2, b); Fo = foot((1, 6, a), (0, 1, a - 1), d); u = tuple(x / nrm(d) for x in d)
    S = [addv(Fo, u, k * 2 * math.sqrt(14)) for k in (1, -1)]; S = [s for s in S if s[0] > 0]; assert len(S) == 1
    return P4([19, 20, 21, 22], sum(S[0]))
add(('2026', 'Apr', '2026-04-06', 1), 'img', 'Let the image of the point P(1, 6, a) in the line L : \\f{x}{1} = \\f{y − 1}{2} = \\f{z − a + 1}{b}, b > 0, be (\\f{a}{3}, 0, a + c). If S(α, β, γ), α > 0, is the point on L such that the distance of S from the foot of perpendicular from the point P on L is 2√{14}, then α + β + γ is equal to:', ['19', '20', '21', '22'], 3,
    _s43, ['The mid-point of P and its image, (\\f{1 + a/3}{2}, 3, …), lies on L: y = 3 gives t = 1, so x = 1 → a = 3.', 'Then the foot is F = (1, 3, 2 + b); PF ⟂ (1, 2, b): 0 − 6 + b(b − 1) = 0 → b = 3, F = (1, 3, 5), image (1, 0, 7).', 'Unit direction (1, 2, 3)/√{14}: S = F ± (2, 4, 6) → with α > 0, S = (3, 7, 11): sum 21.'], 'img', 3)
add(('2026', 'Jan', '2026-01-24', 1), 'line3', 'Let a line L passing through the point P(1, 1, 1) be perpendicular to the lines \\f{x − 4}{4} = \\f{y − 1}{1} = \\f{z − 1}{1} and \\f{x − 17}{1} = \\f{y − 71}{1} = \\f{z}{0}. Let the line L intersect the yz-plane at the point Q. Another line parallel to L and passing through the point S(1, 0, −1) intersects the yz-plane at the point R. Then the square of the area of the parallelogram PQRS is equal to ______.', None, 6,
    lambda: (lambda d: round(dot(cross(sub(addv((1, 1, 1), d, -1 / d[0]), (1, 1, 1)), sub((1, 0, -1), (1, 1, 1))), cross(sub(addv((1, 1, 1), d, -1 / d[0]), (1, 1, 1)), sub((1, 0, -1), (1, 1, 1)))), 6))(cross((4, 1, 1), (1, 1, 0))),
    ['Direction of L = (4, 1, 1) × (1, 1, 0) = (−1, 1, 3). Q = P + (−1, 1, 3) = (0, 2, 4); R = S + (−1, 1, 3) = (0, 1, 2).', 'Area = |PQ × PS| with PQ = (−1, 1, 3), PS = (0, −1, −2): cross = (1, −2, 1).', 'Area^{2} = 6.'], 'line3', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'sd', 'The shortest distance between the lines \\f{x − 4}{1} = \\f{y − 3}{2} = \\f{z − 2}{−3} and \\f{x + 2}{2} = \\f{y − 6}{4} = \\f{z − 5}{−5} is:', ['\\f{5√{6}}{6}', '2√{5}', '3√{5}', '4√{5}'], 3,
    lambda: P4([5 * S6 / 6, 2 * S5, 3 * S5, 4 * S5], sd((4, 3, 2), (1, 2, -3), (-2, 6, 5), (2, 4, -5))),
    ['n = (1, 2, −3) × (2, 4, −5) = (2, −1, 0), |n| = √{5}.', 'A_{2} − A_{1} = (−6, 3, 3); dot with n = −15 → \\f{15}{√{5}} = 3√{5}.'], 'sd', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'img', 'Let the image of the point P(0, −5, 0) in the line \\f{x − 1}{2} = \\f{y}{1} = \\f{z + 1}{−2} be the point R and the image of the point Q(0, −\\f{1}{2}, 0) in the line \\f{x − 1}{−1} = \\f{y + 9}{4} = \\f{z + 1}{1} be the point S. Then the square of the area of the parallelogram PQRS is ______.', None, 162,
    lambda: (lambda R, S: round((nrm(cross(sub(R, (0, -5, 0)), sub(S, (0, -0.5, 0)))) / 2) ** 2, 6))(image((0, -5, 0), (1, 0, -1), (2, 1, -2)), image((0, -0.5, 0), (1, -9, -1), (-1, 4, 1))),
    ['Foot of P: t = −1 → (−1, −1, 1); R = (−2, 3, 2). Foot of Q: t = 2 → (−1, −1, 1); S = (−2, −\\f{3}{2}, 2).', 'PQ = SR = (0, \\f{9}{2}, 0) ✓ parallelogram; PS = (−2, \\f{7}{2}, 2).', 'Area = |PQ × PS| = \\f{9}{2}·√{8} → area^{2} = \\f{81}{4}·8 = 162.'], 'img', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'sd', 'The sum of all values of α, for which the shortest distance between the lines \\f{x + 1}{α} = \\f{y − 2}{−1} = \\f{z − 4}{−α} and \\f{x}{α} = \\f{y − 1}{2} = \\f{z − 1}{2α} is √{2}, is', ['8', '−6', '6', '−8'], 2,
    lambda: P4([8, -6, 6, -8], sum(roots(lambda a: sd((-1, 2, 4), (a, -1, -a), (0, 1, 1), (a, 2, 2 * a)) - S2, -50, 50, 20001))),
    ['n = (α, −1, −α) × (α, 2, 2α) = (0, −3α^{2}, 3α), |n| = 3|α|√{α^{2} + 1}.', 'A_{2} − A_{1} = (1, −1, −3): dot = 3α^{2} − 9α.', '\\f{|α − 3|}{√{α^{2} + 1}} = √{2} → α^{2} + 6α − 7 = 0 → sum −6.'], 'sd', 2)

# ---------- sheet 9
def _s49():
    lam, = roots(lambda l: foot((l, 2, 3), (4, 9, 5), (1, 2, 1))[0] - 1, -50, 50, 10001); mu = foot((lam, 2, 3), (4, 9, 5), (1, 2, 1))[1]
    return P4([12 / 7, math.sqrt(145) / 7, math.sqrt(146) / 7, math.sqrt(143) / 7], sd((1, 2, -4), (2, 3, 6), (lam, mu, -5), (2, 3, 6)))
add(('2026', 'Apr', '2026-04-08', 2), 'sd', 'Let the foot of perpendicular from the point (λ, 2, 3) on the line \\f{x − 4}{1} = \\f{y − 9}{2} = \\f{z − 5}{1} be the point (1, μ, 2). Then the distance between the lines \\f{x − 1}{2} = \\f{y − 2}{3} = \\f{z + 4}{6} and \\f{x − λ}{2} = \\f{y − μ}{3} = \\f{z + 5}{6} is equal to:', ['\\f{12}{7}', '\\f{√{145}}{7}', '\\f{√{146}}{7}', '\\f{√{143}}{7}'], 3,
    _s49, ['x = 1 on the line → t = −3 → foot (1, 3, 2), μ = 3. (1 − λ, 1, −1) ⟂ (1, 2, 1) → λ = 2.', 'Parallel lines, direction (2, 3, 6), |d| = 7; A_{2} − A_{1} = (1, 1, −1).', '(1, 1, −1) × (2, 3, 6) = (9, −8, 1) → distance \\f{√{146}}{7}.'], 'sd', 2)

# ---------- extra sheet 1
add(('2025', 'Apr', '2025-04-02', 1), 'line3', 'Let the vertices Q and R of the triangle PQR lie on the line \\f{x + 3}{5} = \\f{y − 1}{2} = \\f{z + 4}{3}, QR = 5 and the coordinates of the point P be (0, 2, 3). If the area of the triangle PQR is \\f{m}{n} then:', ['2m − 5√{21}n = 0', '5m − 2√{21}n = 0', '5m − 21√{2}n = 0', 'm − 5√{21}n = 0'], 1,
    lambda: P4([5 * math.sqrt(21) / 2, 2 * math.sqrt(21) / 5, 21 * S2 / 5, 5 * math.sqrt(21)], 0.5 * 5 * dline((0, 2, 3), (-3, 1, -4), (5, 2, 3))),
    ['Height = distance of P from the line. P − A = (3, 1, 7); (3, 1, 7) × (5, 2, 3) = (−11, 26, 1), |…| = √{798}, |d| = √{38}.', 'Height = √{21}; area = \\f{1}{2}·5·√{21} → \\f{m}{n} = \\f{5√{21}}{2}: 2m − 5√{21}n = 0.'], 'line3', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'sd', 'The line L_{1} is parallel to vector a⃗ = −3î + 2ĵ + 4k̂ and passes through the point (7, 6, 2) and the line L_{2} is parallel to vector b⃗ = 2î + ĵ + 3k̂ and passes through the point (5, 3, 4). The shortest distance between the lines L_{1} and L_{2} is :', ['\\f{21}{√{38}}', '\\f{23}{√{57}}', '\\f{21}{√{57}}', '\\f{23}{√{38}}'], 4,
    lambda: P4([21 / math.sqrt(38), 23 / math.sqrt(57), 21 / math.sqrt(57), 23 / math.sqrt(38)], sd((7, 6, 2), (-3, 2, 4), (5, 3, 4), (2, 1, 3))),
    ['n = (−3, 2, 4) × (2, 1, 3) = (2, 17, −7), |n| = √{342} = 3√{38}.', '(−2, −3, 2)·n = −4 − 51 − 14 = −69 → \\f{69}{3√{38}} = \\f{23}{√{38}}.'], 'sd', 1)
def _det5():
    Pt = (4, 1, 0); n = cross(sub((1, 2, 3), Pt), (2, 3, 4)); s = -dot(n, sub((6, 0, 4), Pt)) / dot(n, (1, 1, -1)); B = addv((6, 0, 4), (1, 1, -1), s); A = meet((1, 2, 3), (2, 3, 4), Pt, sub(B, Pt))
    assert sd((1, 2, 3), (2, 3, 4), Pt, sub(B, Pt)) < 1e-9
    M = [(1, 0, 1), A, B]; return P4([6, 8, 16, 12], M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
add(('2025', 'Apr', '2025-04-03', 1), 'line3', 'Let a line passing through the point (4, 1, 0) intersect the line L_{1} : \\f{x − 1}{2} = \\f{y − 2}{3} = \\f{z − 3}{4} at the point A(α, β, γ) and the line L_{2} : x − 6 = y = −z + 4 at the point B(a, b, c). Then the determinant with rows (1, 0, 1), (α, β, γ), (a, b, c) is equal to', ['6', '8', '16', '12'], 2,
    _det5, ['The required line lies in the plane through (4, 1, 0) containing L_{1}: normal (−3, 1, 3) × (2, 3, 4) = (−5, 18, −11).', 'Meet this plane with L_{2} = (6 + s, s, 4 − s): s = 3 → B = (9, 3, 1). Line PB meets L_{1} at A = (−1, −1, −1).', 'det of (1, 0, 1), (−1, −1, −1), (9, 3, 1) = 1(−1 + 3) + 1(−3 + 9) = 8.'], 'line3', 3)
def _oaob():
    d = (3, 2, -2); Fo = foot((1, 2, 3), (6, 7, 7), d); u = tuple(x / nrm(d) for x in d); A = addv(Fo, u, 2 * math.sqrt(17)); B = addv(Fo, u, -2 * math.sqrt(17))
    return P4([62, 47, 21, 49], dot(A, B))
add(('2025', 'Apr', '2025-04-04', 1), 'img', 'Let A and B be two distinct points on the line L : \\f{x − 6}{3} = \\f{y − 7}{2} = \\f{z − 7}{−2}. Both A and B are at a distance 2√{17} from the foot of perpendicular drawn from the point (1, 2, 3) on the line L. If O is the origin, then OA⃗·OB⃗ is equal to', ['62', '47', '21', '49'], 2,
    _oaob, ['Foot: t = \\f{(−5, −5, −4)·(3, 2, −2)}{17} = −1 → F = (3, 5, 9).', 'Unit direction (3, 2, −2)/√{17}: A, B = F ± (6, 4, −4) = (9, 9, 5) and (−3, 1, 13).', 'OA⃗·OB⃗ = −27 + 9 + 65 = 47.'], 'img', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'img', 'Consider a line L passing through the points P(1, 2, 1) and Q(2, 1, −1). If the mirror image of the point A(2, 2, 2) in the line L is (α, β, γ), then α + β + 6γ is equal to ______.', None, 6,
    lambda: (lambda I: round(I[0] + I[1] + 6 * I[2], 6))(image((2, 2, 2), (1, 2, 1), sub((2, 1, -1), (1, 2, 1)))),
    ['Direction (1, −1, −2). Foot: t = \\f{(1, 0, 1)·(1, −1, −2)}{6} = −\\f{1}{6} → F = (\\f{5}{6}, \\f{13}{6}, \\f{4}{3}).', 'Image = 2F − A = (−\\f{1}{3}, \\f{7}{3}, \\f{2}{3}) → α + β + 6γ = 2 + 4 = 6.'], 'img', 2)

# ---------- extra sheet 2
def _far():
    Pt, d = (1, -2, 3), sub((5, -4, 7), (1, -2, 3)); u = tuple(x / nrm(d) for x in d); C = [addv(Pt, u, k) for k in (9, -9)]
    return P4([155, 150, 160, 165], max(dot(c, c) for c in C))
add(('2024', 'Apr', '2024-04-04', 1), 'line3', 'Let the point, on the line passing through the points P(1, −2, 3) and Q(5, −4, 7), farther from the origin and at a distance of 9 units from the point P, be (α, β, γ). Then α^{2} + β^{2} + γ^{2} is equal to :', ['155', '150', '160', '165'], 1,
    _far, ['Direction (4, −2, 4), unit (2, −1, 2)/3. Points P ± 9·unit = P ± (6, −3, 6).', '(7, −5, 9) with square-distance 155, or (−5, 1, −3) with 35. Farther: 155.'], 'line3', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'img', 'Let (α, β, γ) be the image of the point (8, 5, 7) in the line \\f{x − 1}{2} = \\f{y + 1}{3} = \\f{z − 2}{5}. Then α + β + γ is equal to', ['16', '18', '14', '20'], 3,
    lambda: P4([16, 18, 14, 20], sum(image((8, 5, 7), (1, -1, 2), (2, 3, 5)))),
    ['Foot: t = \\f{(7, 6, 5)·(2, 3, 5)}{38} = \\f{57}{38} = \\f{3}{2} → F = (4, \\f{7}{2}, \\f{19}{2}).', 'Image = 2F − P = (0, 2, 12) → sum 14.'], 'img', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'line3', 'Let d be the distance of the point of intersection of the lines \\f{x + 6}{3} = \\f{y}{2} = \\f{z + 1}{1} and \\f{x − 7}{4} = \\f{y − 9}{3} = \\f{z − 4}{2} from the point (7, 8, 9). Then d^{2} + 6 is equal to :', ['72', '69', '75', '78'], 3,
    lambda: (lambda X: P4([72, 69, 75, 78], dot(sub(X, (7, 8, 9)), sub(X, (7, 8, 9))) + 6))(meet((-6, 0, -1), (3, 2, 1), (7, 9, 4), (4, 3, 2))),
    ['(−6 + 3s, 2s, −1 + s) = (7 + 4t, 9 + 3t, 4 + 2t). From the first two: 3s − 4t = 13 and 2s − 3t = 9 → s = 3, t = −1; z checks (2 = 2). Point (3, 6, 2).', 'd^{2} = 16 + 4 + 49 = 69 → d^{2} + 6 = 75.'], 'line3', 1)
def _quad():
    A, B, C, D = (3, 1, -1), (5 / 3, 7 / 3, 1 / 3), (2, 2, 1), (10 / 3, 2 / 3, -1 / 3); assert abs(dot(cross(sub(B, A), sub(C, A)), sub(D, A))) < 1e-9
    return P4([4 * S2 / 3, 5 * S2 / 3, 2 * S2, 2 * S2 / 3], (nrm(cross(sub(B, A), sub(C, A))) + nrm(cross(sub(C, A), sub(D, A)))) / 2)
add(('2024', 'Apr', '2024-04-06', 1), 'line3', 'If A(3, 1, −1), B(\\f{5}{3}, \\f{7}{3}, \\f{1}{3}), C(2, 2, 1) and D(\\f{10}{3}, \\f{2}{3}, −\\f{1}{3}) are the vertices of a quadrilateral ABCD, then its area is', ['\\f{4√{2}}{3}', '\\f{5√{2}}{3}', '2√{2}', '\\f{2√{2}}{3}'], 1,
    _quad, ['AB⃗ = DC⃗ = \\f{4}{3}(−1, 1, 1): a parallelogram.', 'AD⃗ = \\f{1}{3}(1, −1, 2). Area = |AB⃗ × AD⃗| = \\f{4}{9}|(3, 3, 0)| = \\f{4√{2}}{3}.'], 'line3', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'img', 'Let P be the point (10, −2, −1) and Q be the foot of the perpendicular drawn from the point R(1, 7, 6) on the line passing through the points (2, −5, 11) and (−6, 7, −5). Then the length of the line segment PQ is equal to ______.', None, 13,
    lambda: round(nrm(sub(foot((1, 7, 6), (2, -5, 11), sub((-6, 7, -5), (2, -5, 11))), (10, -2, -1))), 6),
    ['Line: (2, −5, 11) + t(−2, 3, −4). Foot: t = \\f{(−1, 12, −5)·(−2, 3, −4)}{29} = 2 → Q = (−2, 1, 3).', 'PQ = √{144 + 9 + 16} = 13.'], 'img', 1)
def _thru():
    Pt = (1, 1, 1); d = cross(cross(sub((1, -1, 1), Pt), (2, 3, 4)), cross(sub((3, 4, 0), Pt), (1, 2, 1)))
    assert sd(Pt, d, (1, -1, 1), (2, 3, 4)) < 1e-9 and sd(Pt, d, (3, 4, 0), (1, 2, 1)) < 1e-9
    ops = [(5, 4, 3), (7, 15, 13), (4, 22, 7), (10, -29, -50)]; h = [i + 1 for i, o in enumerate(ops) if nrm(cross(sub(o, Pt), d)) < 1e-9]; assert len(h) == 1; return h[0]
add(('2025', 'Apr', '2025-04-07', 1), 'line3', 'Let the line L pass through (1, 1, 1) and intersect the lines \\f{x − 1}{2} = \\f{y + 1}{3} = \\f{z − 1}{4} and \\f{x − 3}{1} = \\f{y − 4}{2} = \\f{z}{1}. Then, which of the following points lies on the line L ?', ['(5, 4, 3)', '(7, 15, 13)', '(4, 22, 7)', '(10, −29, −50)'], 2,
    _thru, ['L lies in the plane through (1, 1, 1) containing each line: normals (0, −2, 0) × (2, 3, 4) = (−8, 0, 4) and (2, 3, −1) × (1, 2, 1) = (5, −3, 1).', 'Direction of L = (−8, 0, 4) × (5, −3, 1) ∥ (12, 28, 24) ∥ (3, 7, 6).', '(1, 1, 1) + 2(3, 7, 6) = (7, 15, 13).'], 'line3', 3)

# ---------- extra sheet 3
add(('2024', 'Apr', '2024-04-09', 2), 'line3', 'Consider the line L passing through the points (1, 2, 3) and (2, 3, 5). The distance of the point (\\f{11}{3}, \\f{11}{3}, \\f{19}{3}) from the line L along the line \\f{3x − 11}{2} = \\f{3y − 11}{1} = \\f{3z − 19}{2} is equal to :', ['3', '5', '4', '6'], 1,
    lambda: (lambda Q: P4([3, 5, 4, 6], nrm(sub(meet((1, 2, 3), (1, 1, 2), Q, (2, 1, 2)), Q))))((11 / 3, 11 / 3, 19 / 3)),
    ['The second line has direction (\\f{2}{3}, \\f{1}{3}, \\f{2}{3}) ∥ (2, 1, 2). Move from the point: (\\f{11}{3} + 2k, \\f{11}{3} + k, \\f{19}{3} + 2k).', 'Meet L = (1 + t, 2 + t, 3 + 2t): k = −1 → (\\f{5}{3}, \\f{8}{3}, \\f{13}{3}) (t = \\f{2}{3}).', 'Distance = |k|·3 = 3.'], 'line3', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'img', 'Let (α, β, γ) be the co-ordinates of the foot of the perpendicular drawn from the point (5, 4, 2) on the line r⃗ = (−î + 3ĵ + k̂) + λ(2î + 3ĵ − k̂). Then the length of the projection of the vector αî + βĵ + γk̂ on the vector 6î + 2ĵ + 3k̂ is :', ['\\f{15}{7}', '4', '\\f{18}{7}', '3'], 3,
    lambda: P4([15 / 7, 4, 18 / 7, 3], abs(dot(foot((5, 4, 2), (-1, 3, 1), (2, 3, -1)), (6, 2, 3))) / 7),
    ['Foot: λ = \\f{(6, 1, 1)·(2, 3, −1)}{14} = 1 → (1, 6, 0).', 'Projection on (6, 2, 3): \\f{6 + 12 + 0}{7} = \\f{18}{7}.'], 'img', 1)
def _mid30():
    M = (0, 0.75, -0.25)
    def g(t):   # A on the line at parameter t (its z must make P's z equal 0); P = 2M − A
        A = (1 + 2 * t, 2 + t, 2 * M[2] - 0); Pt = tuple(2 * m - x for m, x in zip(M, A)); return Pt, A
    t, = roots(lambda t: dot(sub(g(t)[1], g(t)[0]), (2, 1, 3)), -20, 20, 4001); Pt, A = g(t); al = A[2] - 3 * t
    return P4([1, 2, 6, 9], Pt[0] ** 2 + Pt[1] ** 2 + al ** 2)
add(('2026', 'Apr', '2026-04-02', 2), 'img', 'Let the point A be the foot of perpendicular drawn from the point P(a, b, 0) on the line \\f{x − 1}{2} = \\f{y − 2}{1} = \\f{z − α}{3}. If the midpoint of the line segment PA is (0, \\f{3}{4}, −\\f{1}{4}), then the value of a^{2} + b^{2} + α^{2} is equal to :', ['1', '2', '6', '9'], 1,
    _mid30, ['A = 2M − P = (−a, \\f{3}{2} − b, −\\f{1}{2}). On the line: −a = 1 + 2t, \\f{3}{2} − b = 2 + t, −\\f{1}{2} = α + 3t.', 'PA ⟂ (2, 1, 3): −4a + \\f{3}{2} − 2b − \\f{3}{2} = 0 → 2a + b = 0 → t = −\\f{1}{2}.', 'a = 0, b = 0, α = 1 → 1.'], 'img', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'line3', 'Let the line L pass through the point (−3, 5, 2) and make equal angles with the positive coordinate axes. If the distance of L from the point (−2, r, 1) is √{\\f{14}{3}}, then the sum of all possible values of r is:', ['12', '16', '6', '10'], 4,
    lambda: P4([12, 16, 6, 10], sum(roots(lambda r: dline((-2, r, 1), (-3, 5, 2), (1, 1, 1)) - math.sqrt(14 / 3), -50, 50, 10001))),
    ['Direction (1, 1, 1). From A = (−3, 5, 2): v = (1, r − 5, −1), v·d = r − 5.', 'Distance^{2} = |v|^{2} − \\f{(r − 5)^{2}}{3} = 2 + \\f{2(r − 5)^{2}}{3} = \\f{14}{3} → (r − 5)^{2} = 4.', 'r = 3 or 7 → sum 10.'], 'line3', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'line3', 'Let the line L_{1} be parallel to the vector −3î + 2ĵ + 4k̂ and pass through the point (2, 6, 7), and the line L_{2} be parallel to the vector 2î + ĵ + 3k̂ and pass through the point (4, 3, 5). If the line L_{3} is parallel to the vector −3î + 5ĵ + 16k̂ and intersects the lines L_{1} and L_{2} at the points C and D, respectively, then |CD⃗|^{2} is equal to :', ['171', '290', '312', '89'], 2,
    lambda: (lambda U: P4([171, 290, 312, 89], dot(sub(U[0], U[1]), sub(U[0], U[1]))))(transversal((2, 6, 7), (-3, 2, 4), (4, 3, 5), (2, 1, 3), (-3, 5, 16))),
    ['C = (2 − 3s, 6 + 2s, 7 + 4s), D = (4 + 2t, 3 + t, 5 + 3t), C − D = k(−3, 5, 16).', 'Solving: s = −3, t = 2, so C = (11, 0, −5), D = (8, 5, 11).', '|CD|^{2} = 9 + 25 + 256 = 290.'], 'line3', 2)
def _b34():
    a, = roots(lambda a: dot(sub((2, 0, -4), (1, 1, -1)), cross((3, -1, 0), (2, 0, a))), -50, 50, 10001)
    B = meet((1, 1, -1), (3, -1, 0), (2, 0, -4), (2, 0, a)); Pp = foot((1, 1, -1), (2, 0, -4), (2, 0, a)); return round(26 * a * dot(sub(Pp, B), sub(Pp, B)), 6)
add(('2025', 'Jan', '2025-01-22', 1), 'img', 'Let L_{1} : \\f{x − 1}{3} = \\f{y − 1}{−1} = \\f{z + 1}{0} and L_{2} : \\f{x − 2}{2} = \\f{y}{0} = \\f{z + 4}{α}, α ∈ ℝ, be two lines, which intersect at the point B. If P is the foot of perpendicular from the point A(1, 1, −1) on L_{2}, then the value of 26α(PB)^{2} is ______.', None, 216,
    _b34, ['Meeting: y gives 1 − s = 0 → B = (4, 0, −1); on L_{2}: t = 1, −4 + α = −1 → α = 3.', 'A lies on L_{1}; foot on L_{2} = (2, 0, −4) + t(2, 0, 3): t = \\f{(−1, 1, 3)·(2, 0, 3)}{13} = \\f{7}{13}.', 'PB = (1 − \\f{7}{13})√{13} = \\f{6}{√{13}} → 26·3·\\f{36}{13} = 216.'], 'img', 2)

# ---------- extra sheet 4
def _q35():
    Pt, R = (-2, -1, 3), (1, 3, 3); out = []
    for t in roots(lambda t: nrm(sub(addv(Pt, (3, 2, 2), t), R)) - 5, -20, 20, 4001):
        Q = addv(Pt, (3, 2, 2), t)
        if nrm(sub(Q, Pt)) > 1e-6: out.append((nrm(cross(sub(Q, Pt), sub(R, Pt))) / 2) ** 2)
    assert len(out) == 1; return P4([144, 136, 140, 148], out[0])
add(('2025', 'Jan', '2025-01-22', 2), 'line3', 'Let a line pass through two distinct points P(−2, −1, 3) and Q, and be parallel to the vector 3î + 2ĵ + 2k̂. If the distance of the point Q from the point R(1, 3, 3) is 5, then the square of the area of △PQR is equal to :', ['144', '136', '140', '148'], 2,
    _q35, ['Q = (−2 + 3t, −1 + 2t, 3 + 2t). QR^{2} = (3t − 3)^{2} + (2t − 4)^{2} + (2t)^{2} = 17t^{2} − 34t + 25 = 25 → t = 0 (that is P) or t = 2.', 'Q = (4, 3, 7). PQ⃗ = (6, 4, 4), PR⃗ = (3, 4, 0); cross = (−16, 12, 12), |…|^{2} = 544.', 'Area^{2} = \\f{544}{4} = 136.'], 'line3', 2)
def _r36():
    def f(r):
        A = tuple((r * q + p) / (r + 1) for p, q in zip((-1, -1, 2), (5, 5, 10))); return dot((5, 5, 10), A) - dot(cross((-1, -1, 2), A), cross((-1, -1, 2), A)) / 5 - 10
    return P4([7, 14, 3, math.sqrt(7)], roots(f, 0.01, 100, 20000)[0])
add(('2025', 'Jan', '2025-01-23', 2), 'line3', 'Let the point A divide the line segment joining the points P(−1, −1, 2) and Q(5, 5, 10) internally in the ratio r : 1 (r > 0). If O is the origin and (OQ⃗·OA⃗) − \\f{1}{5}|OP⃗ × OA⃗|^{2} = 10, then the value of r is :', ['7', '14', '3', '√{7}'], 1,
    _r36, ['A = \\f{(5r − 1, 5r − 1, 10r + 2)}{r + 1}.', 'OQ⃗·OA⃗ = \\f{150r + 10}{r + 1}; OP⃗ × OA⃗ = \\f{(−20r, 20r, 0)}{r + 1}, |…|^{2} = \\f{800r^{2}}{(r + 1)^{2}}.', '(150r + 10)(r + 1) − 160r^{2} = 10(r + 1)^{2} → 20r^{2} = 140r → r = 7.'], 'line3', 3)
add(('2025', 'Jan', '2025-01-23', 2), 'line3', 'The distance of the line \\f{x − 2}{2} = \\f{y − 6}{3} = \\f{z − 3}{4} from the point (1, 4, 0) along the line \\f{x}{1} = \\f{y − 2}{2} = \\f{z + 3}{3} is :', ['√{13}', '√{17}', '√{15}', '√{14}'], 4,
    lambda: P4([math.sqrt(13), math.sqrt(17), math.sqrt(15), math.sqrt(14)], nrm(sub(meet((2, 6, 3), (2, 3, 4), (1, 4, 0), (1, 2, 3)), (1, 4, 0)))),
    ['Move from (1, 4, 0) along (1, 2, 3): (1 + k, 4 + 2k, 3k). On the first line: \\f{k − 1}{2} = \\f{2k − 2}{3} = \\f{3k − 3}{4} → k = 1.', 'Point (2, 6, 3); distance = √{14}.'], 'line3', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'line3', 'Let the line passing through the points (−1, 2, 1) and parallel to the line \\f{x − 1}{2} = \\f{y + 1}{3} = \\f{z}{4} intersect the line \\f{x + 2}{3} = \\f{y − 3}{2} = \\f{z − 4}{1} at the point P. Then the distance of P from the point Q(4, −5, 1) is', ['5√{6}', '5√{5}', '5', '10'], 2,
    lambda: P4([5 * S6, 5 * S5, 5, 10], nrm(sub(meet((-1, 2, 1), (2, 3, 4), (-2, 3, 4), (3, 2, 1)), (4, -5, 1)))),
    ['(−1 + 2s, 2 + 3s, 1 + 4s) = (−2 + 3t, 3 + 2t, 4 + t): s = 1, t = 1 → P = (1, 5, 5).', 'PQ = √{9 + 100 + 16} = 5√{5}.'], 'line3', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'line3', 'Let in a △ABC, the length of the side AC be 6, the vertex B be (1, 2, 3) and the vertices A, C lie on the line \\f{x − 6}{3} = \\f{y − 7}{2} = \\f{z − 7}{−2}. Then the area (in sq. units) of △ABC is:', ['17', '21', '56', '42'], 2,
    lambda: P4([17, 21, 56, 42], 0.5 * 6 * dline((1, 2, 3), (6, 7, 7), (3, 2, -2))),
    ['Height = distance of B from the line: foot t = \\f{(−5, −5, −4)·(3, 2, −2)}{17} = −1 → (3, 5, 9); height = √{4 + 9 + 36} = 7.', 'Area = \\f{1}{2}·6·7 = 21.'], 'line3', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'line3', 'The square of the distance of the point (\\f{15}{7}, \\f{32}{7}, 7) from the line \\f{x + 1}{3} = \\f{y + 3}{5} = \\f{z + 5}{7} in the direction of the vector î + 4ĵ + 7k̂ is:', ['41', '66', '44', '54'], 2,
    lambda: (lambda Q: P4([41, 66, 44, 54], dot(sub(meet((-1, -3, -5), (3, 5, 7), Q, (1, 4, 7)), Q), sub(meet((-1, -3, -5), (3, 5, 7), Q, (1, 4, 7)), Q))))((15 / 7, 32 / 7, 7)),
    ['Move along (1, 4, 7): (\\f{15}{7} + k, \\f{32}{7} + 4k, 7 + 7k) must equal (−1 + 3t, −3 + 5t, −5 + 7t).', 'Solving: k = −1, t = \\f{5}{7} → point (\\f{8}{7}, \\f{4}{7}, 0).', 'Distance^{2} = 66k^{2} = 66.'], 'line3', 2)

# ---------- extra sheet 5
def _s52():
    tot = 0
    for t in [x / 10 for x in range(-200, 201)]:   # candidate points of L, then move along L to meet the other line
        A = addv((-1, -1, -3), (2, 3, 6), t)
        if sd(A, (2, 3, 6), (-1, -1, 9), (2, 3, 0)) < 1e-9:
            X = meet(A, (2, 3, 6), (-1, -1, 9), (2, 3, 0))
            if abs(nrm(sub(A, X)) - 7) < 1e-9: tot += sum(A)
    return P4([28, 40, 6, 34], tot)
add(('2026', 'Jan', '2026-01-22', 2), 'line3', 'Let L be the line \\f{x + 1}{2} = \\f{y + 1}{3} = \\f{z + 3}{6} and let S be the set of all points (a, b, c) on L, whose distance from the line \\f{x + 1}{2} = \\f{y + 1}{3} = \\f{z − 9}{0} along the line L is 7. Then Σ_{(a, b, c) ∈ S}(a + b + c) is equal to :', ['28', '40', '6', '34'], 4,
    _s52, ['The two lines meet: (−1 + 2t, −1 + 3t, −3 + 6t) has z = 9 at t = 2, giving (3, 5, 9), which is on the second line (s = 2).', 'Along L, |(2, 3, 6)| = 7, so the points are (3, 5, 9) ± (2, 3, 6) = (5, 8, 15) and (1, 2, 3).', 'Sum = 28 + 6 = 34.'], 'line3', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'img', 'The square of the distance of the point P(5, 6, 7) from the line \\f{x − 2}{2} = \\f{y − 5}{3} = \\f{z − 2}{4} is equal to:', ['3', '5', '6', '8'], 3,
    lambda: P4([3, 5, 6, 8], dline((5, 6, 7), (2, 5, 2), (2, 3, 4)) ** 2),
    ['Foot: t = \\f{(3, 1, 5)·(2, 3, 4)}{29} = 1 → (4, 8, 6).', 'Distance^{2} = 1 + 4 + 1 = 6.'], 'img', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'line3', 'The vertices B and C of a triangle ABC lie on the line \\f{x}{1} = \\f{1 − y}{−2} = \\f{z − 2}{3}. The coordinates of A and B are (1, 6, 3) and (4, 9, α) respectively and C is at a distance of 10 units from B. The area (in sq. units) of △ABC is :', ['5√{13}', '15√{13}', '20√{13}', '10√{13}'], 1,
    lambda: P4([5 * math.sqrt(13), 15 * math.sqrt(13), 20 * math.sqrt(13), 10 * math.sqrt(13)], 0.5 * 10 * dline((1, 6, 3), (0, 1, 2), (1, 2, 3))),
    ['The line is (0, 1, 2) + t(1, 2, 3) (note \\f{1 − y}{−2} = \\f{y − 1}{2}).', 'Height from A: foot t = \\f{(1, 5, 1)·(1, 2, 3)}{14} = 1 → (1, 3, 5); height = √{0 + 9 + 4} = √{13}.', 'Area = \\f{1}{2}·10·√{13} = 5√{13}.'], 'line3', 2)
def _cen():
    Q = [addv((-3, 4, -1), (8, 2, 2), t) for t in roots(lambda t: nrm(sub(addv((-3, 4, -1), (8, 2, 2), t), (1, 2, 3))) - 6, -20, 20, 4001)]
    assert len(Q) == 2; return P4([4, 5, 6, 8], sum(sum(x) for x in Q + [(1, 2, 3)]) / 3)
add(('2026', 'Apr', '2026-04-05', 2), 'line3', 'Let a triangle PQR be such that P and Q lie on the line \\f{x + 3}{8} = \\f{y − 4}{2} = \\f{z + 1}{2} and are at a distance of 6 units from R(1, 2, 3). If (α, β, γ) is the centroid of △PQR, then α + β + γ is equal to :', ['4', '5', '6', '8'], 3,
    _cen, ['Points (−3 + 8t, 4 + 2t, −1 + 2t) with distance 6 from R: (8t − 4)^{2} + (2t + 2)^{2} + (2t − 4)^{2} = 36 → 72t^{2} − 72t = 0.', 't = 0, 1 → P = (−3, 4, −1), Q = (5, 6, 1).', 'Centroid = \\f{1}{3}(3, 12, 3) = (1, 4, 1) → 6.'], 'line3', 2)
def _qr61():
    R = meet((1, 2, 3), (2, 3, 4), (4, 1, 0), (5, 2, 1)); assert sd((1, 2, 3), (2, 3, 4), (4, 1, 0), (5, 2, 1)) < 1e-9
    Ps = [addv(R, (2, 3, 4), k) for k in (1, -1)]; Pp, = [p for p in Ps if min(p) > 0]
    assert near(dline(Pp, (4, 1, 0), (5, 2, 1)) ** 2, 47 / 3)   # the given PQ is the least distance, so Q is the foot
    Q = foot(Pp, (4, 1, 0), (5, 2, 1)); return P4([340, 360, 320, 348], 27 * dot(sub(Q, R), sub(Q, R)))
add(('2026', 'Jan', '2026-01-24', 1), 'line3', 'Let the lines L_{1} : r⃗ = î + 2ĵ + 3k̂ + λ(2î + 3ĵ + 4k̂), λ ∈ ℝ and L_{2} : r⃗ = (4î + ĵ) + μ(5î + 2ĵ + k̂), μ ∈ ℝ, intersect at the point R. Let P and Q be the points lying on lines L_{1} and L_{2}, respectively, such that |PR⃗| = √{29} and |PQ⃗| = √{\\f{47}{3}}. If the point P lies in the first octant, then 27(QR)^{2} is equal to', ['340', '360', '320', '348'], 2,
    _qr61, ['Meet: 1 + 2λ = 4 + 5μ, 2 + 3λ = 1 + 2μ → λ = −1, μ = −1: R = (−1, −1, −1).', '|(2, 3, 4)| = √{29}, so P = R + (2, 3, 4) = (1, 2, 3) (first octant).', 'Distance of P from L_{2} is exactly √{\\f{47}{3}}, so Q is the foot: μ = −\\f{1}{3}, Q = (\\f{7}{3}, \\f{1}{3}, −\\f{1}{3}); 27·QR^{2} = 27·\\f{40}{3} = 360.'], 'line3', 3)
def _abc64():
    d1 = cross((1, 2, 2), (2, 2, 1)); X = meet((0, 0, 0), d1, (3, -1, 4), (1, 2, 2)); assert sd((0, 0, 0), d1, (3, -1, 4), (1, 2, 2)) < 1e-9
    pts = [addv((3, 3, 2), (2, 2, 1), s) for s in roots(lambda s: nrm(sub(addv((3, 3, 2), (2, 2, 1), s), X)) - math.sqrt(17), -20, 20, 8001)]
    p, = [q for q in pts if abs(q[0] - round(q[0])) < 1e-9]; return round(sum(p) ** 2, 6)
add(('2026', 'Apr', '2026-04-08', 2), 'line3', 'Let a line L_{1} pass through the origin and be perpendicular to the lines L_{2} : r⃗ = (3 + t)î + (2t − 1)ĵ + (2t + 4)k̂ and L_{3} : r⃗ = (3 + 2s)î + (3 + 2s)ĵ + (2 + s)k̂, t, s ∈ ℝ. If (a, b, c), a ∈ ℤ, is the point on L_{3} at a distance of √{17} from the point of intersection of L_{1} and L_{2}, then (a + b + c)^{2} is equal to ______.', None, 4,
    _abc64, ['Direction of L_{1} = (1, 2, 2) × (2, 2, 1) = (−2, 3, −2). It meets L_{2} at k = −1, t = −1: (2, −3, 2).', 'Point of L_{3}: (3 + 2s, 3 + 2s, 2 + s); distance^{2} from (2, −3, 2) = 9s^{2} + 28s + 37 = 17 → s = −2 or −\\f{10}{9}.', 'a ∈ ℤ → s = −2: (−1, −1, 0) → (a + b + c)^{2} = 4.'], 'line3', 3)
def _a65():
    def hit(dx, dy):   # where (1 + dx·k, 2 + dy·k) meets (1 + t, 2t): solve the 2 × 2 system for k, t
        D = dx * (-2) - dy * (-1); k = ((0) * (-2) - (-2) * (-1)) / D; t = (dx * (-2) - dy * 0) / D; return k, (1 + t, 2 * t, 1 + t)
    k1, X1 = hit(3, 4); k2, X2 = hit(1, 4)
    a, = roots(lambda a: nrm(sub(X1, (1, 2, a))) - nrm(sub(X2, (1, 2, a))), -20, 20, 4001)
    b, c = (X1[2] - a) / k1, (X2[2] - a) / k2; return P4([7, 5, 6, 4], a + b + c)
add(('2026', 'Jan', '2026-01-28', 1), 'line3', 'If the distances of the point (1, 2, a) from the line \\f{x − 1}{1} = \\f{y}{2} = \\f{z − 1}{1} along the lines L_{1} : \\f{x − 1}{3} = \\f{y − 2}{4} = \\f{z − a}{b} and L_{2} : \\f{x − 1}{1} = \\f{y − 2}{4} = \\f{z − a}{c} are equal, then a + b + c is equal to', ['7', '5', '6', '4'], 1,
    _a65, ['L_{1} meets the line where (1 + 3k, 2 + 4k) = (1 + t, 2t): k = 1, t = 3 → point (4, 6, 4), so a + b = 4.', 'L_{2}: (1 + k, 2 + 4k) = (1 + t, 2t) → k = −1 → point (0, −2, 0), so a − c = 0.', 'Equal distances: 9 + 16 + (4 − a)^{2} = 1 + 16 + a^{2} → a = 3, b = 1, c = 3 → 7.'], 'line3', 3)
for _p in P: _p['t'] = _p['fam']
