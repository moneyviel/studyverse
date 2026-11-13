"""Real JEE Main questions — Mathematics Unit 14: Trigonometry. Our own solutions; chk re-solves each one
numerically — identities by evaluating both sides at many points, equations by counting sign changes of the
function on a fine grid (with a check that every crossing is a genuine zero, not a jump at an asymptote), and
extreme values by dense scanning. Skipped: items whose printed expression we could not read reliably, a tan A, tan B item and a cos 3θ item whose keys we could not reproduce, and a statements item with two identical options."""
import math, itertools
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
pi = math.pi; S2, S3, S5, S6 = math.sqrt(2), math.sqrt(3), math.sqrt(5), math.sqrt(6)
def P4(opts, v, tol=1e-6): return pick(opts, round(v, 9), tol)
def zeros(f, lo, hi, n=200000, skip=()):
    """sign-change zeros of f on [lo, hi]; a change across a pole (huge |f|) is not a zero; points in skip are excluded"""
    out = []; xs = [lo + (hi - lo) * k / n for k in range(n + 1)]; prev = None
    for x in xs:
        try: v = f(x)
        except (ValueError, ZeroDivisionError): prev = None; continue
        if prev is not None:
            px, pv = prev
            if pv == 0: out.append(px)
            elif pv * v < 0 and abs(pv) < 1e3 and abs(v) < 1e3:
                a, b = px, x
                for _ in range(80):
                    m = (a + b) / 2; fm = f(m)
                    if pv * fm <= 0: b = m
                    else: a, pv = m, fm
                r = (a + b) / 2
                if abs(f(r)) < 1e-7 and not any(abs(r - s) < 1e-6 for s in skip): out.append(r)
        prev = (x, v)
    if prev and prev[1] == 0: out.append(prev[0])
    dedup = []
    for r in sorted(out):
        if not dedup or abs(r - dedup[-1]) > 1e-7: dedup.append(r)
    return dedup
def same(f, g, pts): return all(abs(f(x) - g(x)) < 1e-9 for x in pts)

# ---------- sheet 1
add(('2025', 'Apr', '2025-04-02', 1), 'eqn', 'If θ ∈ [−2π, 2π], then the number of solutions of 2√{2}cos^{2}θ + (2 − √{6})cos θ − √{3} = 0, is equal to :', ['8', '12', '10', '6'], 1,
    lambda: P4([8, 12, 10, 6], len(zeros(lambda t: 2 * S2 * math.cos(t) ** 2 + (2 - S6) * math.cos(t) - S3, -2 * pi, 2 * pi))),
    ['A quadratic in cos θ: roots cos θ = \\f{√{3}}{2} and cos θ = −\\f{1}{√{2}} (product −\\f{√{3}}{2√{2}} ✓).', 'Each value of cos θ in (−1, 1) is taken twice per period, and [−2π, 2π] holds two periods: 2 × 2 × 2 = 8.'], 'eqn', 2)
def _y17():
    vals = set(round((x - math.cos(pi / 3 + math.acos(x / 2))) ** 2 + 3 * math.cos(pi / 3 + math.acos(x / 2)) ** 2, 9) for x in (-1.7, -0.3, 0.4, 1.2, 1.9))
    assert len(vals) == 1; return round(vals.pop())
add(('2025', 'Apr', '2025-04-02', 2), 'inv', 'If y = cos(\\f{π}{3} + cos^{−1}\\f{x}{2}), then (x − y)^{2} + 3y^{2} is equal to ______.', None, 3,
    _y17, ['Let cos^{−1}\\f{x}{2} = t: x = 2cos t, y = cos(\\f{π}{3} + t) = \\f{1}{2}cos t − \\f{√{3}}{2}sin t.', 'x − y = \\f{3}{2}cos t + \\f{√{3}}{2}sin t; √{3}y = \\f{√{3}}{2}cos t − \\f{3}{2}sin t.', 'Sum of squares = (\\f{9}{4} + \\f{3}{4})(cos^{2}t + sin^{2}t) = 3.'], 'inv', 2)
def _n24():
    poles = [-3 * pi / 2, -pi / 2, pi / 2, 3 * pi / 2]
    return P4([4, 3, 5, 6], len(zeros(lambda x: 2 * x + 3 * math.tan(x) - pi, -2 * pi, 2 * pi, skip=poles)))
add(('2025', 'Apr', '2025-04-03', 1), 'eqn', 'The number of solutions of the equation 2x + 3 tan x = π, x ∈ [−2π, 2π] − {±\\f{π}{2}, ±\\f{3π}{2}} is:', ['4', '3', '5', '6'], 3,
    _n24, ['f(x) = 2x + 3 tan x − π is increasing on each piece between asymptotes, so it has at most one zero there.', 'Pieces: [−2π, −\\f{3π}{2}), (−\\f{3π}{2}, −\\f{π}{2}), (−\\f{π}{2}, \\f{π}{2}), (\\f{π}{2}, \\f{3π}{2}), (\\f{3π}{2}, 2π]. f(−2π) = −5π < 0 and f(2π) = 3π > 0, so every piece has a zero.', '5 solutions.'], 'eqn', 3)
add(('2025', 'Apr', '2025-04-03', 2), 'eqn', 'The number of solutions of the equation (4 − √{3})sin x − 2√{3}cos^{2}x = −\\f{4}{1 + √{3}}, x ∈ [−2π, \\f{5π}{2}] is', ['3', '5', '4', '6'], 2,
    lambda: P4([3, 5, 4, 6], len(zeros(lambda x: (4 - S3) * math.sin(x) - 2 * S3 * math.cos(x) ** 2 + 4 / (1 + S3), -2 * pi, 2.5 * pi))),
    ['Put cos^{2}x = 1 − sin^{2}x: 2√{3}s^{2} + (4 − √{3})s − 2√{3} + \\f{4}{1 + √{3}} = 0, with \\f{4}{1 + √{3}} = 2(√{3} − 1).', 'So 2√{3}s^{2} + (4 − √{3})s − 2 = 0 → s = \\f{1}{2} (the other root −\\f{2}{√{3}} < −1).', 'sin x = \\f{1}{2} on [−2π, \\f{5π}{2}]: x = −\\f{11π}{6}, −\\f{7π}{6}, \\f{π}{6}, \\f{5π}{6}, \\f{13π}{6} → 5.'], 'eqn', 2)
def _i44():
    pts = [-0.45, -0.2, 0.1, 0.4, 0.65, 0.7]; lhs = lambda x: math.asin(S3 / 2 * x + 0.5 * math.sqrt(1 - x * x))
    ops = [lambda x: 5 * pi / 6 - math.asin(x), lambda x: pi / 4 + math.asin(x), lambda x: -5 * pi / 6 - math.asin(x), lambda x: pi / 6 + math.asin(x)]
    h = [i + 1 for i, g in enumerate(ops) if same(lhs, g, pts)]; assert len(h) == 1; return h[0]
add(('2025', 'Apr', '2025-04-04', 1), 'inv', 'Considering the principal values of the inverse trigonometric functions, sin^{−1}(\\f{√{3}}{2}x + \\f{1}{2}√{1 − x^{2}}), −\\f{1}{2} < x < \\f{1}{√{2}}, is equal to', ['\\f{5π}{6} − sin^{−1}x', '\\f{π}{4} + sin^{−1}x', '−\\f{5π}{6} − sin^{−1}x', '\\f{π}{6} + sin^{−1}x'], 4,
    _i44, ['Put x = sin t, t ∈ (−\\f{π}{6}, \\f{π}{4}): the inside is sin t cos\\f{π}{6} + cos t sin\\f{π}{6} = sin(t + \\f{π}{6}).', 't + \\f{π}{6} ∈ (0, \\f{5π}{12}) lies in the principal range, so the value is \\f{π}{6} + sin^{−1}x.'], 'inv', 2)
def _m67():
    best = 9
    for i in range(0, 601):
        A = pi * i / 600
        for j in range(0, 601):
            B = -pi / 2 + pi * j / 600; al = A - B
            if -pi / 2 - 1e-12 <= al <= pi + 1e-12:
                x, y = math.cos(A), math.sin(B); best = min(best, x * x + y * y + 2 * x * y * math.sin(al))
    return P4([-1, 0, -0.5, 0.5], best, 1e-6)
add(('2024', 'Apr', '2024-04-04', 2), 'inv', 'Given the inverse trigonometric function assumes principal values only. Let x, y be any two real numbers in [−1, 1] such that cos^{−1}x − sin^{−1}y = α, −\\f{π}{2} ≤ α ≤ π. Then, the minimum value of x^{2} + y^{2} + 2xy sin α is', ['−1', '0', '−\\f{1}{2}', '\\f{1}{2}'], 2,
    _m67, ['x = cos A, y = sin B with α = A − B.', 'x^{2} + y^{2} + 2xy sin α = (x + y sin α)^{2} + y^{2}cos^{2}α ≥ 0.', 'It equals 0 when x = y = 0 (A = \\f{π}{2}, B = 0, α = \\f{π}{2}): minimum 0.'], 'inv', 3)

# ---------- sheet 2
def _s69():
    S = []
    for k in range(0, 200001):
        t = pi / 2 * k / 200000; u = math.sin(2 * t) ** 2; A = math.sin(t) ** 4 + math.cos(t) ** 4; C = math.sin(t) ** 6 + math.cos(t) ** 6
        if u - 4 * A * C >= -1e-12: S.append(t)
    lo, hi = min(S) - pi / 400000, min(S); h = lambda t: math.sin(2 * t) ** 2 - 4 * (math.sin(t) ** 4 + math.cos(t) ** 4) * (math.sin(t) ** 6 + math.cos(t) ** 6)
    for _ in range(100):   # sharpen the boundary of the allowed θ-range
        m = (lo + hi) / 2
        if h(m) >= 0: hi = m
        else: lo = m
    a = math.sin(2 * hi) ** 2; b = max(math.sin(2 * t) ** 2 for t in S); return round(3 * ((a - 2) ** 2 + (b - 1) ** 2), 6)
add(('2024', 'Apr', '2024-04-04', 2), 'id', 'Let S = {sin^{2}2θ : (sin^{4}θ + cos^{4}θ)x^{2} + (sin 2θ)x + (sin^{6}θ + cos^{6}θ) = 0 has real roots}. If α and β be the smallest and largest elements of the set S, respectively, then 3((α − 2)^{2} + (β − 1)^{2}) equals ______.', None, 4,
    _s69, ['With u = sin^{2}2θ: sin^{4}θ + cos^{4}θ = 1 − \\f{u}{2}, sin^{6}θ + cos^{6}θ = 1 − \\f{3u}{4}.', 'Real roots: u ≥ 4(1 − \\f{u}{2})(1 − \\f{3u}{4}) → 3u^{2} − 12u + 8 ≤ 0 → u ≥ 2 − \\f{2}{√{3}} (and u ≤ 1).', 'α = 2 − \\f{2}{√{3}}, β = 1 → 3·\\f{4}{3} = 4.'], 'id', 3)
add(('2024', 'Apr', '2024-04-05', 2), 'eqn', 'The number of solutions of sin^{2}x + (2 + 2x − x^{2})sin x − 3(x − 1)^{2} = 0, where −π ≤ x ≤ π, is ______.', None, 2,
    lambda: len(zeros(lambda x: math.sin(x) ** 2 + (2 + 2 * x - x * x) * math.sin(x) - 3 * (x - 1) ** 2, -pi, pi)),
    ['With t = (x − 1)^{2}, 2 + 2x − x^{2} = 3 − t, so the equation is (sin x + 3)(sin x − t) = 0.', 'sin x + 3 ≠ 0; so sin x = (x − 1)^{2}.', 'The parabola touches [0, 1] only near x = 1: it meets sin x twice in [−π, π].'], 'eqn', 3)
def _c102():
    t, = zeros(lambda t: 4 * math.cos(t) - 3 * math.sin(t) - 1, 0, pi / 4); return P4([4 / (3 * S6 - 2), (6 - S6) / (3 * S6 - 2), (6 + S6) / (3 * S6 + 2), 4 / (3 * S6 + 2)], math.cos(t))
add(('2024', 'Apr', '2024-04-05', 1), 'eqn', 'Suppose θ ∈ [0, \\f{π}{4}] is a solution of 4 cos θ − 3 sin θ = 1. Then cos θ is equal to :', ['\\f{4}{3√{6} − 2}', '\\f{6 − √{6}}{3√{6} − 2}', '\\f{6 + √{6}}{3√{6} + 2}', '\\f{4}{3√{6} + 2}'], 1,
    _c102, ['3 sin θ = 4c − 1 → 9(1 − c^{2}) = (4c − 1)^{2} → 25c^{2} − 8c − 8 = 0 → c = \\f{4 + 6√{6}}{25} (positive root).', 'Rationalise \\f{4}{3√{6} − 2} = \\f{4(3√{6} + 2)}{50} = \\f{6√{6} + 4}{25} ✓.'], 'eqn', 2)
def _t113():
    c = [x for x in zeros(lambda c: 64 + c * c - 2 * 8 * c * F(2, 3) - 49, 0.1, 50) if abs(x - round(x)) < 1e-9][0]; c = round(c)
    C = math.acos((49 + 64 - c * c) / (2 * 7 * 8)); v = F(49 * math.cos(3 * C) + 42).limit_denominator(1000); return v.numerator + v.denominator
add(('2024', 'Apr', '2024-04-06', 2), 'id', 'In a triangle ABC, BC = 7, AC = 8, AB = α ∈ ℕ and cos A = \\f{2}{3}. If 49 cos(3C) + 42 = \\f{m}{n}, where gcd(m, n) = 1, then m + n is equal to ______.', None, 39,
    _t113, ['Cosine rule at A: 49 = 64 + α^{2} − \\f{32α}{3} → 3α^{2} − 32α + 45 = 0 → α = 9.', 'cos C = \\f{49 + 64 − 81}{112} = \\f{2}{7}; cos 3C = 4cos^{3}C − 3cos C = −\\f{262}{343}.', '49 cos 3C + 42 = \\f{32}{7} → 39.'], 'id', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'inv', 'For n ∈ ℕ, if cot^{−1}3 + cot^{−1}4 + cot^{−1}5 + cot^{−1}n = \\f{π}{4}, then n is equal to ______.', None, 47,
    lambda: [n for n in range(1, 500) if abs(sum(math.atan(1 / k) for k in (3, 4, 5, n)) - pi / 4) < 1e-9][0],
    ['cot^{−1}3 + cot^{−1}4 = cot^{−1}\\f{12 − 1}{7} = cot^{−1}\\f{11}{7}; adding cot^{−1}5: cot^{−1}\\f{55/7 − 1}{11/7 + 5} = cot^{−1}\\f{24}{23}.', 'cot^{−1}\\f{24}{23} + cot^{−1}n = cot^{−1}1 → \\f{24n/23 − 1}{24/23 + n} = 1 → 24n − 23 = 24 + 23n → n = 47.'], 'inv', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'eqn', 'The number of solutions of the equation cos 2θ cos\\f{θ}{2} + cos\\f{5θ}{2} = 2cos^{3}\\f{5θ}{2} in [−\\f{π}{2}, \\f{π}{2}] is :', ['5', '7', '9', '6'], 2,
    lambda: P4([5, 7, 9, 6], len(zeros(lambda t: math.cos(2 * t) * math.cos(t / 2) + math.cos(2.5 * t) - 2 * math.cos(2.5 * t) ** 3, -pi / 2, pi / 2))),
    ['cos 2θ cos\\f{θ}{2} = \\f{1}{2}(cos\\f{5θ}{2} + cos\\f{3θ}{2}); 2cos^{3}u − cos u = \\f{1}{2}(cos 3u + cos u) with u = \\f{5θ}{2}.', 'The equation becomes cos\\f{3θ}{2} + cos\\f{5θ}{2} = cos\\f{15θ}{2} + cos\\f{5θ}{2} → cos\\f{3θ}{2} = cos\\f{15θ}{2}.', '\\f{15θ}{2} = 2kπ ± \\f{3θ}{2} → θ = \\f{kπ}{3} or \\f{2kπ}{9}: in [−\\f{π}{2}, \\f{π}{2}] these give 0, ±\\f{π}{3}, ±\\f{2π}{9}, ±\\f{4π}{9} → 7.'], 'eqn', 3)

# ---------- sheet 3
def acot(y): return math.atan(1 / y) if y > 0 else pi + math.atan(1 / y)
def _c152():
    t2, th = math.tan(2), math.tan(0.5)
    return P4([pi + 2.5, pi - 1.5, pi - 1.25, pi + 1.5], acot((math.sqrt(1 + t2 * t2) - 1) / t2) - acot((math.sqrt(1 + th * th) + 1) / th))
add(('2025', 'Apr', '2025-04-08', 2), 'inv', 'The value of cot^{−1}(\\f{√{1 + tan^{2}(2)} − 1}{tan(2)}) − cot^{−1}(\\f{√{1 + tan^{2}(\\f{1}{2})} + 1}{tan(\\f{1}{2})}) is equal to', ['π + \\f{5}{2}', 'π − \\f{3}{2}', 'π − \\f{5}{4}', 'π + \\f{3}{2}'], 3,
    _c152, ['2 lies in (\\f{π}{2}, π), so √{1 + tan^{2}2} = |sec 2| = −sec 2: the first argument is \\f{−sec 2 − 1}{tan 2} = −\\f{1 + cos 2}{sin 2} = −cot 1, and cot^{−1}(−cot 1) = π − 1.', 'For \\f{1}{2}: \\f{sec\\f{1}{2} + 1}{tan\\f{1}{2}} = \\f{1 + cos\\f{1}{2}}{sin\\f{1}{2}} = cot\\f{1}{4} → cot^{−1} = \\f{1}{4}.', 'Difference: π − 1 − \\f{1}{4} = π − \\f{5}{4}.'], 'inv', 3)
def _s156():
    out = []
    for t in zeros(lambda t: 1 - 2 * math.cos(t) ** 2, -pi, 2 * pi):
        z = (1 + 1j * math.cos(t)) / (1 - 2j * math.cos(t))
        if abs(z.real) < 1e-9 and abs(z.imag) > 1e-9: out.append(t)
    return P4([2 * pi, 3 * pi, 5 * pi, 4 * pi], sum(out))
add(('2024', 'Apr', '2024-04-08', 2), 'eqn', 'The sum of all possible values of θ ∈ [−π, 2π], for which \\f{1 + i cos θ}{1 − 2i cos θ} is purely imaginary, is equal to', ['2π', '3π', '5π', '4π'], 2,
    _s156, ['Multiply by the conjugate 1 + 2i cos θ: real part ∝ 1 − 2cos^{2}θ, imaginary part ∝ 3cos θ.', 'Purely imaginary: cos^{2}θ = \\f{1}{2} (then cos θ ≠ 0 ✓).', 'θ = ±\\f{π}{4}, ±\\f{3π}{4}, \\f{5π}{4}, \\f{7π}{4} → sum 3π.'], 'eqn', 2)
def _t169():
    x = pi + math.asin(3 / 5); assert abs(math.sin(x) + 0.6) < 1e-12 and pi < x < 1.5 * pi; return P4([109, 108, 18, 19], 80 * (math.tan(x) ** 2 - math.cos(x)))
add(('2024', 'Apr', '2024-04-08', 1), 'id', 'If sin x = −\\f{3}{5}, where π < x < \\f{3π}{2}, then 80(tan^{2}x − cos x) is equal to :', ['109', '108', '18', '19'], 1,
    _t169, ['Third quadrant: cos x = −\\f{4}{5}, tan x = \\f{3}{4}.', '80(\\f{9}{16} + \\f{4}{5}) = 45 + 64 = 109.'], 'id', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'inv', 'Let the inverse trigonometric functions take principal values. The number of real solutions of the equation 2 sin^{−1}x + 3 cos^{−1}x = \\f{2π}{5}, is ______.', None, 0,
    lambda: len(zeros(lambda x: 2 * math.asin(x) + 3 * math.acos(x) - 2 * pi / 5, -1, 1)) + (1 if min(abs(2 * math.asin(x) + 3 * math.acos(x) - 2 * pi / 5) for x in [k / 1000 - 1 for k in range(2001)]) < 1e-9 else 0),
    ['2 sin^{−1}x + 3 cos^{−1}x = π + cos^{−1}x (using sin^{−1}x + cos^{−1}x = \\f{π}{2}).', 'π + cos^{−1}x ≥ π > \\f{2π}{5}: no solution.'], 'inv', 1)
def _k200():
    K = math.sin(pi / 18) * math.sin(5 * pi / 18) * math.sin(7 * pi / 18); return P4([(S3 + 1) / (2 * S2), (S3 - 1) / S2, S3 / 2, 0.5], math.sin(10 * K * pi / 3))
add(('2026', 'Apr', '2026-04-02', 1), 'id', 'If sin(\\f{π}{18})sin(\\f{5π}{18})sin(\\f{7π}{18}) = K, then the value of sin(\\f{10Kπ}{3}) is', ['\\f{√{3} + 1}{2√{2}}', '\\f{√{3} − 1}{√{2}}', '\\f{√{3}}{2}', '\\f{1}{2}'], 1,
    _k200, ['sin 10° sin 50° sin 70° = sin 10° sin(60° − 10°) sin(60° + 10°) = \\f{1}{4}sin 30° = \\f{1}{8}.', 'sin(\\f{10π}{24}) = sin 75° = \\f{√{3} + 1}{2√{2}}.'], 'id', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'id', 'The value of cosec 10° − √{3} sec 10° is equal to :', ['4', '2', '8', '6'], 1,
    lambda: P4([4, 2, 8, 6], 1 / math.sin(math.radians(10)) - S3 / math.cos(math.radians(10))),
    ['= \\f{cos 10° − √{3} sin 10°}{sin 10° cos 10°} = \\f{2 cos 70°}{\\f{1}{2}sin 20°}.', 'cos 70° = sin 20° → 4.'], 'id', 1)

# ---------- sheet 4
add(('2026', 'Jan', '2026-01-28', 2), 'inv', 'Considering the principal values of inverse trigonometric functions, the value of the expression tan(2 sin^{−1}(\\f{2}{√{13}}) − 2 cos^{−1}(\\f{3}{√{10}})) is equal to :', ['\\f{33}{56}', '\\f{16}{63}', '−\\f{16}{63}', '−\\f{33}{56}'], 1,
    lambda: P4([33 / 56, 16 / 63, -16 / 63, -33 / 56], math.tan(2 * math.asin(2 / math.sqrt(13)) - 2 * math.acos(3 / math.sqrt(10)))),
    ['sin^{−1}\\f{2}{√{13}} = tan^{−1}\\f{2}{3}; cos^{−1}\\f{3}{√{10}} = tan^{−1}\\f{1}{3}.', 'tan(2A) = \\f{4/3}{1 − 4/9} = \\f{12}{5}; tan(2B) = \\f{2/3}{1 − 1/9} = \\f{3}{4}.', 'tan(2A − 2B) = \\f{12/5 − 3/4}{1 + 9/5} = \\f{33/20}{14/5} = \\f{33}{56}.'], 'inv', 2)
def _v241():
    th = math.acos(1 / S3); p = (2 * S3, 0, 0); q = (2 * math.cos(th), 2 * math.sin(th), 0); r = tuple(a + b for a, b in zip(p, q))   # BC + CA = BA
    w = tuple(a - 3 * b for a, b in zip(q, r)); c = (p[1] * w[2] - p[2] * w[1], p[2] * w[0] - p[0] * w[2], p[0] * w[1] - p[1] * w[0])
    return P4([340, 220, 410, 200], sum(x * x for x in c) + 3 * sum(x * x for x in r))
add(('2026', 'Jan', '2026-01-21', 2), 'id', 'For a triangle ABC, let p⃗ = BC⃗, q⃗ = CA⃗ and r⃗ = BA⃗. If |p⃗| = 2√{3}, |q⃗| = 2 and cos θ = \\f{1}{√{3}}, where θ is the angle between p⃗ and q⃗, then |p⃗ × (q⃗ − 3r⃗)|^{2} + 3|r⃗|^{2} is equal to :', ['340', '220', '410', '200'], 4,
    _v241, ['BC⃗ + CA⃗ = BA⃗, so r⃗ = p⃗ + q⃗ and q⃗ − 3r⃗ = −3p⃗ − 2q⃗ → p⃗ × (q⃗ − 3r⃗) = −2(p⃗ × q⃗).', '|p⃗ × q⃗|^{2} = 12·4·(1 − \\f{1}{3}) = 32 → 4·32 = 128.', '|r⃗|^{2} = 12 + 4 + 2·2√{3}·2·\\f{1}{√{3}} = 24 → 128 + 72 = 200.'], 'id', 2)
def _h263():
    out = set()
    for al in zeros(lambda a: 8 - 10 * math.sin(a) + 10 * math.cos(a) - 9, 0, 2 * pi):
        A, B, C = (6, 8), (10 * math.cos(al), -10 * math.sin(al)), (-10 * math.sin(al), 10 * math.cos(al))
        # orthocentre by intersecting two altitudes
        a1, b1, c1 = C[0] - B[0], C[1] - B[1], (C[0] - B[0]) * A[0] + (C[1] - B[1]) * A[1]; a2, b2, c2 = C[0] - A[0], C[1] - A[1], (C[0] - A[0]) * B[0] + (C[1] - A[1]) * B[1]
        D = a1 * b2 - a2 * b1; H = ((c1 * b2 - c2 * b1) / D, (a1 * c2 - a2 * c1) / D); assert abs(H[1] - 9) < 1e-7
        G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3); out.add(round(5 * H[0] - 3 * G[0] + 6 * G[1] + 100 * math.sin(2 * al), 6))
    assert len(out) == 1; return round(out.pop())
add(('2025', 'Jan', '2025-01-22', 2), 'id', 'Let A(6, 8), B(10 cos α, −10 sin α) and C(−10 sin α, 10 cos α), be the vertices of a triangle. If L(a, 9) and G(h, k) be its orthocenter and centroid respectively, then (5a − 3h + 6k + 100 sin 2α) is equal to ______.', None, 145,
    _h263, ['All three vertices are at distance 10 from O, so O is the circumcentre and H = A + B + C.', 'H_{y} = 8 + 10(cos α − sin α) = 9 → cos α − sin α = \\f{1}{10}; squaring, sin 2α = \\f{99}{100}. a = 6 + 1 = 7.', 'G = \\f{H}{3} = (\\f{7}{3}, 3): 35 − 7 + 18 + 99 = 145.'], 'id', 3)
def _i264():
    pts = [pi / 2 + k * pi / 40 for k in range(0, 11)]; lhs = lambda x: math.acos(12 / 13 * math.cos(x) + 5 / 13 * math.sin(x))
    ops = [lambda x: x + math.atan(5 / 12), lambda x: x - math.atan(4 / 3), lambda x: x + math.atan(4 / 5), lambda x: x - math.atan(5 / 12)]
    h = [i + 1 for i, g in enumerate(ops) if same(lhs, g, pts)]; assert len(h) == 1; return h[0]
add(('2025', 'Jan', '2025-01-23', 1), 'inv', 'If \\f{π}{2} ≤ x ≤ \\f{3π}{4}, then cos^{−1}(\\f{12}{13}cos x + \\f{5}{13}sin x) is equal to', ['x + tan^{−1}\\f{5}{12}', 'x − tan^{−1}\\f{4}{3}', 'x + tan^{−1}\\f{4}{5}', 'x − tan^{−1}\\f{5}{12}'], 4,
    _i264, ['With φ = tan^{−1}\\f{5}{12}: cos φ = \\f{12}{13}, sin φ = \\f{5}{13}, so the inside is cos(x − φ).', 'x − φ ∈ [\\f{π}{2} − φ, \\f{3π}{4} − φ] ⊂ [0, π], so cos^{−1} returns x − tan^{−1}\\f{5}{12}.'], 'inv', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'id', 'The value of (sin 70°)(cot 10° cot 70° − 1) is', ['\\f{2}{3}', '\\f{3}{2}', '1', '0'], 3,
    lambda: P4([2 / 3, 1.5, 1, 0], math.sin(math.radians(70)) * (1 / math.tan(math.radians(10)) / math.tan(math.radians(70)) - 1)),
    ['cot 10° cot 70° − 1 = \\f{cos 10° cos 70° − sin 10° sin 70°}{sin 10° sin 70°} = \\f{cos 80°}{sin 10° sin 70°}.', 'cos 80° = sin 10°, so the product is sin 70°·\\f{1}{sin 70°} = 1.'], 'id', 1)
def _ab283():
    for a2 in range(-40, 41):
        a = F(a2, 2); b = 8 - a
        if a <= b and (1 + a * a) + (1 + b * b) == 36:   # sec²(tan⁻¹α) = 1 + α², cosec²(cot⁻¹β) = 1 + β²
            assert abs(1 / math.cos(math.atan(a)) ** 2 + 1 / math.sin(acot(float(b))) ** 2 - 36) < 1e-9; return int(a * a + b)
add(('2025', 'Jan', '2025-01-24', 1), 'inv', 'If for some α, β; α ≤ β, α + β = 8 and sec^{2}(tan^{−1}α) + cosec^{2}(cot^{−1}β) = 36, then α^{2} + β is ______.', None, 14,
    _ab283, ['sec^{2}(tan^{−1}α) = 1 + α^{2}; cosec^{2}(cot^{−1}β) = 1 + β^{2}.', 'α^{2} + β^{2} = 34 with α + β = 8 → αβ = 15 → α = 3, β = 5.', 'α^{2} + β = 14.'], 'inv', 1)

# ---------- sheet 5
def _u285():
    A = zeros(lambda x: (math.log(abs(math.sin(x))) + math.log(abs(math.cos(x)))) / math.log(2 / pi) - 2, 1e-9, pi - 1e-9, skip=[pi / 2])
    B = [t * t for t in range(0, 400) if abs(t * (t - 4) - 3 * abs(t - 2) + 6) < 1e-12]   # x = t², t = √x ≥ 0 (the equation is a polynomial in t)
    B += [t * t for t in zeros(lambda t: t * (t - 4) - 3 * abs(t - 2) + 6, 0, 50) if abs(t - round(t)) > 1e-6]
    U = sorted(set([round(a, 9) for a in A] + [round(b, 9) for b in B])); return P4([4, 2, 6, 8], len(U))
add(('2025', 'Jan', '2025-01-24', 2), 'eqn', 'Let A = {x ∈ (0, π) − {\\f{π}{2}} : log_{(2/π)}|sin x| + log_{(2/π)}|cos x| = 2} and B = {x ≥ 0 : √{x}(√{x} − 4) − 3|√{x} − 2| + 6 = 0}. Then n(A ∪ B) is equal to :', ['4', '2', '6', '8'], 4,
    _u285, ['A: |sin x cos x| = \\f{4}{π^{2}} → |sin 2x| = \\f{8}{π^{2}} ≈ 0.81: four values of x in (0, π).', 'B: with t = √{x}: t ≥ 2 gives t^{2} − 7t + 12 = 0 → t = 3, 4; t < 2 gives t^{2} − t = 0 → t = 0, 1. So B = {0, 1, 9, 16}.', 'No overlap: n(A ∪ B) = 8.'], 'eqn', 3)
def _e287():
    hits = set()
    for a, b, c in ((5, 3, 1), (2.5, 1.2, 0.3), (9, 4, 2)):
        v = acot(b + (1 + b * b) / (a - b)) + acot(c + (1 + c * c) / (b - c)) + acot(a + (1 + a * a) / (c - a))
        ops = [pi / 2 - (a + b + c), 0, pi, 3 * pi]; hits.add(tuple(i + 1 for i, o in enumerate(ops) if abs(o - v) < 1e-9))
    (h,), = hits; return h
add(('2025', 'Jan', '2025-01-24', 2), 'inv', 'If α > β > γ > 0, then the expression cot^{−1}{β + \\f{1 + β^{2}}{α − β}} + cot^{−1}{γ + \\f{1 + γ^{2}}{β − γ}} + cot^{−1}{α + \\f{1 + α^{2}}{γ − α}} is equal to :', ['\\f{π}{2} − (α + β + γ)', '0', 'π', '3π'], 3,
    _e287, ['β + \\f{1 + β^{2}}{α − β} = \\f{1 + αβ}{α − β}: so the first term is cot^{−1}\\f{1 + αβ}{α − β} = tan^{−1}α − tan^{−1}β; likewise the second is tan^{−1}β − tan^{−1}γ.', 'The third argument is negative (γ − α < 0): cot^{−1}\\f{1 + αγ}{γ − α} = π + (tan^{−1}γ − tan^{−1}α).', 'Sum = π.'], 'inv', 3)
add(('2025', 'Jan', '2025-01-28', 1), 'inv', 'cos(sin^{−1}\\f{3}{5} + sin^{−1}\\f{5}{13} + sin^{−1}\\f{33}{65}) is equal to:', ['1', '\\f{33}{65}', '\\f{32}{65}', '0'], 4,
    lambda: P4([1, 33 / 65, 32 / 65, 0], math.cos(math.asin(3 / 5) + math.asin(5 / 13) + math.asin(33 / 65))),
    ['sin^{−1}\\f{3}{5} + sin^{−1}\\f{5}{13} = sin^{−1}(\\f{3}{5}·\\f{12}{13} + \\f{4}{5}·\\f{5}{13}) = sin^{−1}\\f{56}{65}.', 'sin^{−1}\\f{56}{65} + sin^{−1}\\f{33}{65}: the sines and cosines swap (56^{2} + 33^{2} = 65^{2}), so the sum is \\f{π}{2}.', 'cos\\f{π}{2} = 0.'], 'inv', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'inv', 'Let S = {x : cos^{−1}x = π + sin^{−1}x + sin^{−1}(2x + 1)}. Then Σ_{x ∈ S}(2x − 1)^{2} is equal to ______.', None, 5,
    lambda: round(sum((2 * x - 1) ** 2 for x in zeros(lambda x: math.acos(x) - pi - math.asin(x) - math.asin(2 * x + 1), -1, 0)), 6),
    ['cos^{−1}x − sin^{−1}x = \\f{π}{2} − 2sin^{−1}x, so sin^{−1}(2x + 1) = −\\f{π}{2} − 2 sin^{−1}x.', 'Take sine of both sides: 2x + 1 = −cos(2 sin^{−1}x) = 2x^{2} − 1 → x^{2} − x − 1 = 0; the root in [−1, 0] is x = \\f{1 − √{5}}{2}.', '(2x − 1)^{2} = 5.'], 'inv', 3)
def _ba341():
    d = math.radians; A = math.sin(d(3)) / math.cos(d(9)) + math.sin(d(9)) / math.cos(d(27)) + math.sin(d(27)) / math.cos(d(81)); B = math.tan(d(81)) - math.tan(d(3))
    return round(B / A, 6)
add(('2026', 'Apr', '2026-04-04', 1), 'id', 'If A = \\f{sin 3°}{cos 9°} + \\f{sin 9°}{cos 27°} + \\f{sin 27°}{cos 81°} and B = tan 81° − tan 3°, then \\f{B}{A} is equal to ______.', None, 2,
    _ba341, ['\\f{sin θ}{cos 3θ} = \\f{1}{2}(tan 3θ − tan θ), because tan 3θ − tan θ = \\f{sin 2θ}{cos 3θ cos θ} = \\f{2 sin θ}{cos 3θ}.', 'A telescopes: \\f{1}{2}(tan 81° − tan 3°) = \\f{B}{2}.', '\\f{B}{A} = 2.'], 'id', 3)
add(('2026', 'Jan', '2026-01-22', 1), 'inv', 'The number of solutions of tan^{−1}4x + tan^{−1}6x = \\f{π}{6}, where −\\f{1}{2√{6}} < x < \\f{1}{2√{6}}, is equal to', ['3', '0', '1', '2'], 3,
    lambda: P4([3, 0, 1, 2], len(zeros(lambda x: math.atan(4 * x) + math.atan(6 * x) - pi / 6, -1 / (2 * S6) + 1e-12, 1 / (2 * S6) - 1e-12))),
    ['In this range 24x^{2} < 1, so tan^{−1}4x + tan^{−1}6x = tan^{−1}\\f{10x}{1 − 24x^{2}}.', '\\f{10x}{1 − 24x^{2}} = \\f{1}{√{3}} → 24x^{2} + 10√{3}x − 1 = 0; only the positive root lies in the range.', '1 solution.'], 'inv', 2)

# ---------- sheet 6
def _ab350():
    d = math.radians; v = (math.cos(d(48)) ** 2 - math.sin(d(12)) ** 2) / (math.sin(d(24)) ** 2 - math.sin(d(6)) ** 2)
    h = [(a, b) for a in range(1, 50) for b in range(1, 50) if abs((a + b * S5) / 2 - v) < 1e-9]; assert len(h) == 1; return sum(h[0])
add(('2026', 'Jan', '2026-01-22', 1), 'id', 'If \\f{cos^{2}48° − sin^{2}12°}{sin^{2}24° − sin^{2}6°} = \\f{α + β√{5}}{2}, where α, β ∈ ℕ, then α + β is equal to ______.', None, 4,
    _ab350, ['cos^{2}A − sin^{2}B = cos(A + B)cos(A − B) = cos 60° cos 36°; sin^{2}A − sin^{2}B = sin(A + B)sin(A − B) = sin 30° sin 18°.', 'Ratio = \\f{cos 36°}{sin 18°} = \\f{√{5} + 1}{√{5} − 1} = \\f{3 + √{5}}{2}.', 'α = 3, β = 1 → 4.'], 'id', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'id', 'max_{0 ≤ x ≤ π}(16 sin(\\f{x}{2})cos^{3}(\\f{x}{2})) is equal to:', ['\\f{3√{3}}{2}', '3√{3}', '4√{3}', '6√{3}'], 2,
    lambda: P4([1.5 * S3, 3 * S3, 4 * S3, 6 * S3], max(16 * math.sin(x / 2) * math.cos(x / 2) ** 3 for x in [pi * k / 300000 for k in range(300001)]), 1e-8),
    ['With t = \\f{x}{2} ∈ [0, \\f{π}{2}], maximise sin t cos^{3}t: derivative cos^{2}t(cos^{2}t − 3 sin^{2}t) = 0 → tan t = \\f{1}{√{3}}, t = \\f{π}{6}.', '16·\\f{1}{2}·(\\f{√{3}}{2})^{3} = 3√{3}.'], 'id', 2)
def _rs369():
    A, B = math.acos(-0.1), math.asin(3 / 8); al, be = (A + B) / 2, (A - B) / 2; assert 0 < al < pi / 3 and 0 < be < pi / 4
    h = [(r, s) for r in range(1, 80) for s in range(1, 80) if abs(3 * (1 - r * S5) / (math.sqrt(11) * (s + S5)) - math.tan(2 * al)) < 1e-9]; assert len(h) == 1; return sum(h[0])
add(('2026', 'Jan', '2026-01-22', 2), 'id', 'Let cos(α + β) = −\\f{1}{10} and sin(α − β) = \\f{3}{8}, where 0 < α < \\f{π}{3} and 0 < β < \\f{π}{4}. If tan 2α = \\f{3(1 − r√{5})}{√{11}(s + √{5})}, r, s ∈ ℕ, then r + s is equal to ______.', None, 20,
    _rs369, ['2α = (α + β) + (α − β). tan(α + β) = −3√{11} (α + β in the 2nd quadrant), tan(α − β) = \\f{3}{√{55}}.', 'tan 2α = \\f{−3√{11} + \\f{3}{√{55}}}{1 + \\f{9√{11}}{√{55}}} = \\f{3(1 − 11√{5})}{√{11}(9 + √{5})} after multiplying through by √{55}.', 'r = 11, s = 9 → 20.'], 'id', 3)
add(('2026', 'Apr', '2026-04-05', 1), 'inv', 'If \\f{π}{4} + Σ_{p=1}^{11} tan^{−1}(\\f{2^{p−1}}{1 + 2^{2p−1}}) = α, then tan α is equal to ______.', None, 2048,
    lambda: round(math.tan(pi / 4 + sum(math.atan(2 ** (p - 1) / (1 + 2 ** (2 * p - 1))) for p in range(1, 12)))),
    ['\\f{2^{p−1}}{1 + 2^{2p−1}} = \\f{2^{p} − 2^{p−1}}{1 + 2^{p}·2^{p−1}}, so each term is tan^{−1}2^{p} − tan^{−1}2^{p−1}.', 'The sum telescopes to tan^{−1}2^{11} − tan^{−1}1 = tan^{−1}2048 − \\f{π}{4}.', 'α = tan^{−1}2048 → tan α = 2048.'], 'inv', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'eqn', 'Number of solutions of √{3}cos 2θ + 8 cos θ + 3√{3} = 0, θ ∈ [−3π, 2π] is :', ['0', '5', '3', '4'], 2,
    lambda: P4([0, 5, 3, 4], len(zeros(lambda t: S3 * math.cos(2 * t) + 8 * math.cos(t) + 3 * S3, -3 * pi, 2 * pi))),
    ['cos 2θ = 2cos^{2}θ − 1: 2√{3}c^{2} + 8c + 2√{3} = 0 → √{3}c^{2} + 4c + √{3} = 0 → c = −\\f{1}{√{3}} (or −√{3}, impossible).', 'cos θ = −\\f{1}{√{3}} twice per 2π; [−3π, 2π] has length 5π: count gives 5.'], 'eqn', 2)

# ---------- sheet 7
def _n398():
    S = {F(2 * k, 9) for k in range(-9, 10)} | {F(k, 6) for k in range(-12, 13)}; S = {s for s in S if -1 <= s <= 1}   # multiples of π
    f = lambda t: math.cos(t) * math.cos(2.5 * t) - math.cos(7 * t) * math.cos(3.5 * t)
    assert all(abs(f(float(s) * pi)) < 1e-9 for s in S)
    num = zeros(f, -pi, pi); assert all(any(abs(z - float(s) * pi) < 1e-6 for s in S) for z in num)   # nothing missed by the formula
    return len(S)
add(('2026', 'Apr', '2026-04-05', 2), 'eqn', 'If S = {θ ∈ [−π, π] : cos θ cos\\f{5θ}{2} = cos 7θ cos\\f{7θ}{2}}, then n(S) is equal to ______.', None, 19,
    _n398, ['Product to sum: cos\\f{7θ}{2} + cos\\f{3θ}{2} = cos\\f{21θ}{2} + cos\\f{7θ}{2} → cos\\f{3θ}{2} = cos\\f{21θ}{2}.', '\\f{21θ}{2} = 2kπ ± \\f{3θ}{2} → θ = \\f{2kπ}{9} (9 values in [−π, π]) or θ = \\f{kπ}{6} (13 values).', 'Common: 0, ±\\f{2π}{3}. n(S) = 9 + 13 − 3 = 19.'], 'eqn', 3)
def _v401():
    th = pi - math.atan(2 * S2); assert abs(1 / math.tan(th) + 1 / (2 * S2)) < 1e-12
    v = math.sin(7.5 * th) * (math.cos(8 * th) + math.sin(8 * th)) + math.cos(7.5 * th) * (math.cos(8 * th) - math.sin(8 * th))
    return P4([(1 - S2) / S3, -S2 / S3, (S2 - 1) / S3, S2 / S3], v)
add(('2026', 'Jan', '2026-01-23', 2), 'id', 'Let \\f{π}{2} < θ < π and cot θ = −\\f{1}{2√{2}}. Then the value of sin(\\f{15θ}{2})(cos 8θ + sin 8θ) + cos(\\f{15θ}{2})(cos 8θ − sin 8θ) is equal to', ['\\f{1 − √{2}}{√{3}}', '−\\f{√{2}}{√{3}}', '\\f{√{2} − 1}{√{3}}', '\\f{√{2}}{√{3}}'], 1,
    _v401, ['Group: (sin\\f{15θ}{2}cos 8θ − cos\\f{15θ}{2}sin 8θ) + (sin\\f{15θ}{2}sin 8θ + cos\\f{15θ}{2}cos 8θ) = sin(−\\f{θ}{2}) + cos\\f{θ}{2}.', 'cos θ = −\\f{1}{3} (2nd quadrant, tan θ = −2√{2}) → cos\\f{θ}{2} = \\f{1}{√{3}}, sin\\f{θ}{2} = \\f{√{2}}{√{3}}.', 'Value = \\f{1 − √{2}}{√{3}}.'], 'id', 3)
def _gp417():
    for b in (1, 2, 3):
        for a in [b * k / 4 for k in range(5, 200)]:
            mn = min(a * math.tan(t) ** 2 + b / math.tan(t) ** 2 for t in [k * pi / 2 / 20000 for k in range(1, 20000)])
            mx = max(a * math.sin(t) ** 2 + b * math.cos(t) ** 2 for t in [k * pi / 20000 for k in range(1, 20000)])
            if abs(mn - mx) < 1e-6:
                r = F(2 * b) / F(a).limit_denominator(); a1 = F(a).limit_denominator() / (2 * b); S = a1 * (1 - r ** 10) / (1 - r); return S.numerator + S.denominator
add(('2026', 'Apr', '2026-04-06', 1), 'id', 'For the functions f(θ) = α tan^{2}θ + β cot^{2}θ, and g(θ) = α sin^{2}θ + β cos^{2}θ, α > β > 0, let min_{0<θ<π/2} f(θ) = max_{0<θ<π} g(θ). If the first term of a G.P. is (\\f{α}{2β}), its common ratio is (\\f{2β}{α}) and the sum of its first 10 terms is \\f{m}{n}, gcd(m, n) = 1, then m + n is equal to ______.', None, 1279,
    _gp417, ['min f = 2√{αβ} (AM–GM); max g = α (since α > β).', '2√{αβ} = α → α = 4β: first term 2, ratio \\f{1}{2}.', 'S_{10} = 4(1 − 2^{−10}) = \\f{1023}{256} → 1279.'], 'id', 3)
def _v422():
    x = pi + math.atan(12 / 5); assert abs(1 / math.tan(x) - 5 / 12) < 1e-12
    v = math.sin(7 * x) * (math.cos(6.5 * x) + math.sin(6.5 * x)) + math.cos(7 * x) * (math.cos(6.5 * x) - math.sin(6.5 * x)); return P4([4 / math.sqrt(26), 6 / math.sqrt(26), 1 / math.sqrt(13), 5 / math.sqrt(13)], v)
add(('2026', 'Jan', '2026-01-24', 1), 'id', 'If cot x = \\f{5}{12} for some x ∈ (π, \\f{3π}{2}), then sin 7x(cos\\f{13x}{2} + sin\\f{13x}{2}) + cos 7x(cos\\f{13x}{2} − sin\\f{13x}{2}) is equal to', ['\\f{4}{√{26}}', '\\f{6}{√{26}}', '\\f{1}{√{13}}', '\\f{5}{√{13}}'], 3,
    _v422, ['Regroup: (sin 7x cos\\f{13x}{2} − cos 7x sin\\f{13x}{2}) + (sin 7x sin\\f{13x}{2} + cos 7x cos\\f{13x}{2}) = sin\\f{x}{2} + cos\\f{x}{2}.', 'cos x = −\\f{5}{13} with \\f{x}{2} ∈ (\\f{π}{2}, \\f{3π}{4}): sin\\f{x}{2} = \\f{3}{√{13}}, cos\\f{x}{2} = −\\f{2}{√{13}}.', 'Sum = \\f{1}{√{13}}.'], 'id', 3)
add(('2026', 'Jan', '2026-01-24', 2), 'eqn', 'The number of elements in the set {x ∈ [0, 180°] : tan(x + 100°) = tan(x + 50°)tan x tan(x − 50°)} is ______.', None, 4,
    lambda: len(zeros(lambda x: math.tan(math.radians(x + 100)) - math.tan(math.radians(x + 50)) * math.tan(math.radians(x)) * math.tan(math.radians(x - 50)), 0, 180, 400000)),
    ['Write \\f{tan(x + 100°)}{tan x} = \\f{sin(x + 50°)sin(x − 50°)}{cos(x + 50°)cos(x − 50°)} = \\f{cos 100° − cos 2x}{cos 100° + cos 2x}, then apply componendo–dividendo to both sides.', 'This gives \\f{sin(2x + 100°)}{sin 100°} = −\\f{cos 100°}{cos 2x} → sin(4x + 100°) + sin 100° = −sin 200° → sin(4x + 100°) = −sin 40°.', '4x + 100° = −40° + 360°k or 220° + 360°k → x = 30°, 55°, 120°, 145°: 4 elements.'], 'eqn', 3)

# ---------- sheet 8
def _n468():
    k = math.tan(pi / 4 + 0.5 * math.acos(2 / 3)) + math.tan(0.5 * math.asin(2 / 3))
    def f(x):
        y = k * x - 1
        if abs(y) > 1 + 1e-12: raise ValueError
        return math.asin(max(-1, min(1, y))) - (math.asin(x) - math.acos(x))
    return len(zeros(f, -1, 1))
add(('2026', 'Jan', '2026-01-28', 1), 'inv', 'If k = tan(\\f{π}{4} + \\f{1}{2}cos^{−1}(\\f{2}{3})) + tan(\\f{1}{2}sin^{−1}(\\f{2}{3})), then the number of solutions of the equation sin^{−1}(kx − 1) = sin^{−1}x − cos^{−1}x is ______.', None, 1,
    _n468, ['tan(\\f{π}{4} + \\f{θ}{2}) = \\f{1 + sin θ}{cos θ} with cos θ = \\f{2}{3}: \\f{3 + √{5}}{2}; tan(\\f{φ}{2}) = \\f{1 − cos φ}{sin φ} with sin φ = \\f{2}{3}: \\f{3 − √{5}}{2}. k = 3.', 'RHS = 2 sin^{−1}x − \\f{π}{2}. Taking sine: 3x − 1 = −cos(2 sin^{−1}x) = 2x^{2} − 1 → x = 0 or \\f{3}{2}.', 'Only x = 0 is valid (both sides −\\f{π}{2}): 1 solution.'], 'inv', 3)
def _g17():
    fs = [(math.sin(t) ** 4 + 3 * math.cos(t) ** 2) / (math.sin(t) ** 4 + math.cos(t) ** 2) for t in [k * pi / 200000 for k in range(200001)]]
    a, b = min(fs), max(fs); return round(64 / (1 - a / b), 6)
add(('2024', 'Apr', '2024-04-08', 1), 'id', 'If the range of f(θ) = \\f{sin^{4}θ + 3cos^{2}θ}{sin^{4}θ + cos^{2}θ}, θ ∈ ℝ is [α, β], then the sum of the infinite G.P., whose first term is 64 and the common ratio is \\f{α}{β}, is equal to ______.', None, 96,
    _g17, ['f = 1 + \\f{2cos^{2}θ}{sin^{4}θ + cos^{2}θ}; with c = cos^{2}θ: denominator (1 − c)^{2} + c = 1 − c + c^{2}.', '\\f{2c}{1 − c + c^{2}} on [0, 1] runs from 0 (c = 0) to 2 (c = 1): range [1, 3].', 'Sum = \\f{64}{1 − 1/3} = 96.'], 'id', 2)
def _s23():
    vals = []
    for k in range(-200000, 200001):
        x = k / 1000
        if abs(x) >= 1:
            a = math.acos(1 / x); b = math.asin(1 / x); vals.append(16 * (a * a + b * b))
    return P4([24 * pi ** 2, 22 * pi ** 2, 18 * pi ** 2, 31 * pi ** 2], max(vals) + min(vals), 1e-5)
add(('2025', 'Jan', '2025-01-22', 1), 'inv', 'Using the principal values of the inverse trigonometric functions, the sum of the maximum and the minimum values of 16((sec^{−1}x)^{2} + (cosec^{−1}x)^{2}) is :', ['24π^{2}', '22π^{2}', '18π^{2}', '31π^{2}'], 2,
    _s23, ['With a = sec^{−1}x, cosec^{−1}x = \\f{π}{2} − a, a ∈ [0, π] − {\\f{π}{2}}.', 'a^{2} + (\\f{π}{2} − a)^{2} is least at a = \\f{π}{4} (\\f{π^{2}}{8}) and largest at a = π (\\f{5π^{2}}{4}).', '16(\\f{π^{2}}{8} + \\f{5π^{2}}{4}) = 22π^{2}.'], 'inv', 2)
for _p in P: _p['t'] = _p['fam']
