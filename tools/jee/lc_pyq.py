"""Real JEE Main questions — Mathematics Unit 7: Limits, Continuity and Differentiability (with applications of
derivatives). Our own solutions; chk re-solves each one numerically and independently — limits by evaluating the
expression ever closer to the point (with Richardson extrapolation), continuity by comparing the two one-sided
values, derivatives by central differences, extrema by scanning a fine grid. Skipped: items whose printed
expression is cut in the scan, an item whose key was changed by NTA, and items from other units."""
import math
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
def lim(f, a, side=0, h=1e-3):
    """two-sided (side 0) or one-sided (+1 / −1) limit of f at a; Richardson on h and h/2."""
    def at(s, k): return f(a + s * k)
    sides = [side] if side else [1, -1]; vals = []
    for s in sides:
        v1, v2 = at(s, h), at(s, h / 2); vals.append(2 * v2 - v1)
    assert max(vals) - min(vals) < 1e-4 * max(1, abs(vals[0])), vals
    return sum(vals) / len(vals)
def lim_inf(f, n=1e6): return 2 * f(2 * n) - f(n)
def d1(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
def d2(f, x, h=1e-4): return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)
def grid(lo, hi, n=200001): return [lo + (hi - lo) * i / (n - 1) for i in range(n)]
def extrema(f, lo, hi, n=200001):
    xs = grid(lo, hi, n); v = [f(x) for x in xs]; mx = mn = 0
    for i in range(1, n - 1):
        if v[i] > v[i - 1] and v[i] >= v[i + 1]: mx += 1
        if v[i] < v[i - 1] and v[i] <= v[i + 1]: mn += 1
    return mn, mx
def jumps(f, pts, eps=1e-9, lo=None, hi=None):
    """points where f is not continuous: compare f(p) with the available one-sided values."""
    n = 0
    for p in pts:
        L = f(p - eps) if lo is None or p > lo else None; R = f(p + eps) if hi is None or p < hi else None; v = f(p)
        n += any(s is not None and abs(s - v) > 1e-6 for s in (L, R))
    return n
def r(x, k=6): return round(x, k)
def turn(f, lo, hi, n=400001):
    """(x of the first local maximum, x of the first local minimum) found from sign changes of f'."""
    xs = grid(lo, hi, n); mx = mn = None
    for a, b in zip(xs, xs[1:]):
        da, db = f(a + 1e-6) - f(a), f(b + 1e-6) - f(b)
        if da > 0 >= db and mx is None: mx = round((a + b) / 2, 3)
        if da < 0 <= db and mn is None: mn = round((a + b) / 2, 3)
    return mx, mn

# ---------------- limits ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'lim', 'For α, β, γ ∈ R, if \\lim_{x→0} \\f{x^{2} sin αx + (γ − 1)e^{x^{2}}}{sin 2x − βx} = 3, then β + γ − α is equal to :', ['6', '−1', '4', '7'], 4,
    lambda: (lambda al, be, ga: pick([6, -1, 4, 7], be + ga - al) if abs(lim(lambda x: (x * x * math.sin(al * x) + (ga - 1) * math.exp(x * x)) / (math.sin(2 * x) - be * x), 0, h=2e-2) - 3) < 1e-2 else None)(-4, 2, 1),
    ['As x → 0 the bottom → 0, so the top must too: γ = 1. Then the top ≈ αx^{3}.', 'Bottom ≈ (2 − β)x − \\f{4}{3}x^{3}: need β = 2, and then \\f{α}{−4/3} = 3 → α = −4. β + γ − α = 2 + 1 + 4 = 7.'], 'lim', 3)
add(('2025', 'Apr', '2025-04-02', 2), 'lim', 'If \\lim_{x→0} \\f{cos(2x) + a cos(4x) − b}{x^{4}} is finite, then (a + b) is equal to :', ['−1', '0', '\\f{3}{4}', '\\f{1}{2}'], 4,
    lambda: (lambda a, b: pick([-1, 0, 0.75, 0.5], a + b) if abs(lim(lambda x: (math.cos(2 * x) + a * math.cos(4 * x) - b) / x ** 4, 0, h=5e-2)) < 1e3 else None)(-0.25, 0.75),
    ['Expand: (1 + a − b) − (2 + 8a)x^{2} + …: both must vanish.', 'a = −\\f{1}{4}, b = \\f{3}{4} → a + b = \\f{1}{2}.'], 'lim', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'lim', 'If \\lim_{x→0} (\\f{tan x}{x})^{1/x^{2}} = p, then 96 log_{e} p is equal to ____.', None, 32,
    lambda: round(96 * lim(lambda x: math.log(math.tan(x) / x) / (x * x), 0, h=1e-2)), ['log p = lim \\f{1}{x^{2}} log(1 + \\f{x^{2}}{3} + …) = \\f{1}{3}.', '96 × \\f{1}{3} = 32.'], 'lim', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'lim', 'If \\lim_{x→1^{+}} \\f{(x − 1)(6 + λ cos(x − 1)) + μ sin(1 − x)}{(x − 1)^{3}} = −1, where λ, μ ∈ R, then λ + μ is equal to', ['18', '19', '17', '20'], 1,
    lambda: (lambda la, mu: pick([18, 19, 17, 20], la + mu) if abs(lim(lambda x: ((x - 1) * (6 + la * math.cos(x - 1)) + mu * math.sin(1 - x)) / (x - 1) ** 3, 1, 1, 1e-2) + 1) < 1e-3 else None)(6, 12),
    ['Put t = x − 1: top = (6 + λ − μ)t + (\\f{μ}{6} − \\f{λ}{2})t^{3} + …', '6 + λ − μ = 0 and \\f{μ}{6} − \\f{λ}{2} = −1 → λ = 6, μ = 12 → 18.'], 'lim', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'lim', 'Let f be a differentiable function on R such that f(2) = 1, f\'(2) = 4. Let \\lim_{x→0}(f(2 + x))^{3/x} = e^{α}. Then the number of times the curve y = 4x^{3} − 4x^{2} − 4(α − 7)x − α meets x-axis is :', ['1', '3', '0', '2'], 4,
    lambda: (lambda al: pick([1, 3, 0, 2], (lambda y: len({round((a + b) / 2, 2) for a, b in zip(grid(-20.00013, 20, 400001), grid(-20.00013, 20, 400001)[1:]) if y(a) * y(b) < 0 or (abs(y(a)) < 1e-3 and abs(y(a)) <= abs(y(a - 1e-4)) and abs(y(a)) <= abs(y(b)))}))(lambda x: 4 * x ** 3 - 4 * x * x - 4 * (al - 7) * x - al)))(round(lim(lambda x: 3 * math.log(1 + 4 * x) / x, 0, h=1e-4))),
    ['α = 3 × \\f{f\'(2)}{f(2)} = 12 → y = 4(x^{3} − x^{2} − 5x − 3) = 4(x + 1)^{2}(x − 3).', 'It touches the axis at −1 and crosses at 3: 2 points.'], 'lim', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'lim', 'If \\lim_{x→1} \\f{(5x + 1)^{1/3} − (x + 5)^{1/3}}{(2x + 3)^{1/2} − (x + 4)^{1/2}} = \\f{m√{5}}{n(2n)^{2/3}}, where gcd(m, n) = 1, then 8m + 12n is equal to ____.', None, 100,
    lambda: (lambda L: next(8 * m + 12 * n for n in range(1, 20) for m in range(1, 40) if math.gcd(m, n) == 1 and abs(m * math.sqrt(5) / (n * (2 * n) ** (2 / 3)) - L) < 1e-6))(lim(lambda x: ((5 * x + 1) ** (1 / 3) - (x + 5) ** (1 / 3)) / ((2 * x + 3) ** 0.5 - (x + 4) ** 0.5), 1)),
    ['L\'Hôpital: top\' = \\f{4}{3}·6^{−2/3}, bottom\' = \\f{1}{2√{5}} at x = 1.', 'Limit = \\f{8√{5}}{3 · 6^{2/3}} → m = 8, n = 3 → 64 + 36 = 100.'], 'lim', 3)
add(('2024', 'Apr', '2024-04-06', 2), 'lim', '\\lim_{n→∞} \\f{(1^{2} − 1)(n − 1) + (2^{2} − 2)(n − 2) + … + ((n − 1)^{2} − (n − 1))·1}{(1^{3} + 2^{3} + … + n^{3}) − (1^{2} + 2^{2} + … + n^{2})} is equal to:', ['\\f{2}{3}', '\\f{1}{3}', '\\f{3}{4}', '\\f{1}{2}'], 2,
    lambda: (lambda g: pick([F(2, 3), F(1, 3), F(3, 4), F(1, 2)], F(round(2 * g(4000) - g(2000), 3)).limit_denominator(10)))(lambda n: sum((k * k - k) * (n - k) for k in range(1, n)) / (sum(k ** 3 for k in range(1, n + 1)) - sum(k * k for k in range(1, n + 1)))),
    ['Top ≈ Σ k^{2}(n − k) ≈ \\f{n^{4}}{3} − \\f{n^{4}}{4} = \\f{n^{4}}{12}; bottom ≈ \\f{n^{4}}{4}.', 'Ratio → \\f{1}{3}.'], 'lim', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'lim', '\\lim_{x→0^{+}} \\f{tan(5x^{1/3}) log_{e}(1 + 3x^{2})}{(tan^{−1} 3√{x})^{2}(e^{5x^{4/3}} − 1)} is equal to', ['\\f{5}{3}', '\\f{1}{15}', '1', '\\f{1}{3}'], 4,
    lambda: pick([5 / 3, 1 / 15, 1, 1 / 3], round(lim(lambda x: math.tan(5 * x ** (1 / 3)) * math.log1p(3 * x * x) / (math.atan(3 * math.sqrt(x)) ** 2 * math.expm1(5 * x ** (4 / 3))), 0, 1, 1e-12), 3), 1e-2),
    ['Replace each factor by its small-x size: tan(5x^{1/3}) ≈ 5x^{1/3}, log(1 + 3x^{2}) ≈ 3x^{2}, (tan^{−1}3√{x})^{2} ≈ 9x, e^{5x^{4/3}} − 1 ≈ 5x^{4/3}.', '\\f{15x^{7/3}}{45x^{7/3}} = \\f{1}{3}.'], 'lim', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'lim', 'Given below are two statements: Statement I : \\lim_{x→0} (\\f{tan^{−1}x + log_{e}√{\\f{1 + x}{1 − x}} − 2x}{x^{5}}) = \\f{2}{5}. Statement II : \\lim_{x→1} (x^{\\f{2}{1 − x}}) = \\f{1}{e^{2}}. In the light of the above statements, choose the correct answer from the options given below', ['Both Statement I and Statement II are true', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false'], 1,
    lambda: (lambda a, b: {(True, True): 1, (False, True): 2, (False, False): 3, (True, False): 4}[(a, b)])(abs(lim(lambda x: (math.atan(x) + 0.5 * math.log((1 + x) / (1 - x)) - 2 * x) / x ** 5, 0, h=0.1) - 0.4) < 1e-3, abs(lim(lambda x: x ** (2 / (1 - x)), 1) - math.exp(-2)) < 1e-5),
    ['tan^{−1}x = x − \\f{x^{3}}{3} + \\f{x^{5}}{5}, log√{\\f{1 + x}{1 − x}} = x + \\f{x^{3}}{3} + \\f{x^{5}}{5} → top ≈ \\f{2x^{5}}{5}: I true.', 'log of II: \\f{2 log x}{1 − x} → −2: II true.'], 'lim', 3)
add(('2024', 'Apr', '2024-04-08', 2), 'lim', 'If α = \\lim_{x→0^{+}} (\\f{e^{√{tan x}} − e^{√{x}}}{√{tan x} − √{x}}) and β = \\lim_{x→0}(1 + sin x)^{\\f{1}{2}cot x} are the roots of the quadratic equation ax^{2} + bx − √{e} = 0, then 12 log_{e}(a + b) is equal to ____.', None, 6,
    lambda: (lambda al, be: (lambda a: round(12 * math.log(a - a * (al + be))))(-math.sqrt(math.e) / (al * be)))(lim(lambda x: (math.exp(math.sqrt(math.tan(x))) - math.exp(math.sqrt(x))) / (math.sqrt(math.tan(x)) - math.sqrt(x)), 0, 1, 1e-2), lim(lambda x: (1 + math.sin(x)) ** (0.5 / math.tan(x)), 0)),
    ['α = e^{0} = 1 (the slope of e^{t} at t = 0); β = e^{1/2}.', 'Product αβ = −\\f{√{e}}{a} → a = −1; sum = −\\f{b}{a} = b = 1 + √{e} → a + b = √{e} → 12 × \\f{1}{2} = 6.'], 'lim', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'lim', 'The value of \\lim_{x→0} 2(\\f{1 − cos x √{cos 2x} ∛{cos 3x} … ¹⁰√{cos 10x}}{x^{2}}) is ____.', None, 55,
    lambda: round(lim(lambda x: 2 * (1 - math.prod(math.cos(k * x) ** (1 / k) for k in range(1, 11))) / (x * x), 0, h=1e-2)), ['log of the product ≈ Σ \\f{1}{k}(−\\f{k^{2}x^{2}}{2}) = −\\f{55x^{2}}{2}.', '1 − product ≈ \\f{55x^{2}}{2} → 2 × \\f{55}{2} = 55.'], 'lim', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'lim', '\\lim_{x→0} \\f{e − (1 + 2x)^{\\f{1}{2x}}}{x} is equal to :', ['e', '\\f{−2}{e}', '0', 'e − e^{2}'], 1,
    lambda: pick([math.e, -2 / math.e, 0, math.e - math.e ** 2], round(lim(lambda x: (math.e - (1 + 2 * x) ** (1 / (2 * x))) / x, 0, h=1e-3), 4), 1e-3),
    ['(1 + t)^{1/t} = e(1 − \\f{t}{2} + …); with t = 2x it is e(1 − x + …).', 'Top ≈ ex → limit e.'], 'lim', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'lim', '\\lim_{x→π/2} (\\f{∫_{x^{3}}^{(π/2)^{3}} (sin(2t^{1/3}) + cos(t^{1/3}))dt}{(x − \\f{π}{2})^{2}}) is equal to :', ['\\f{9π^{2}}{8}', '\\f{11π^{2}}{10}', '\\f{3π^{2}}{2}', '\\f{5π^{2}}{9}'], 1,
    lambda: (lambda I: pick([9 * math.pi ** 2 / 8, 11 * math.pi ** 2 / 10, 1.5 * math.pi ** 2, 5 * math.pi ** 2 / 9], round(lim(lambda x: I(x) / (x - math.pi / 2) ** 2, math.pi / 2, h=1e-2), 3), 1e-3))(lambda x: (lambda a, b, n: sum((math.sin(2 * t ** (1 / 3)) + math.cos(t ** (1 / 3))) for t in [a + (b - a) * (i + 0.5) / n for i in range(n)]) * (b - a) / n)(x ** 3, (math.pi / 2) ** 3, 4000)),
    ['L\'Hôpital: top\' = −3x^{2}(sin 2x + cos x), which is 0 at \\f{π}{2}, so apply it again.', 'Second derivative of the top at \\f{π}{2}: −3x^{2}(2 cos 2x − sin x) = \\f{9π^{2}}{4}; divide by 2 → \\f{9π^{2}}{8}.'], 'lim', 3)
add(('2026', 'Jan', '2026-01-21', 1), 'lim', 'Let f : R → (0, ∞) be a twice differentiable function such that f(3) = 18, f\'(3) = 0 and f"(3) = 4. Then \\lim_{x→1} (log_{e}(\\f{f(2 + x)}{f(3)})^{\\f{18}{(x − 1)^{2}}}) is equal to :', ['1', '9', '2', '18'], 3,
    lambda: (lambda f: pick([1, 9, 2, 18], round(lim(lambda x: 18 * math.log(f(2 + x) / 18) / (x - 1) ** 2, 1, h=1e-2), 4)))(lambda x: 18 + 2 * (x - 3) ** 2),
    ['Near 3: f(3 + h) ≈ 18 + 2h^{2} (Taylor with f\'(3) = 0, f"(3) = 4).', '18 · log(1 + \\f{h^{2}}{9}) / h^{2} → 2.'], 'lim', 2)

# ---------------- continuity and differentiability ----------------
add(('2025', 'Apr', '2025-04-04', 1), 'cont', 'Let m and n be the number of points at which the function f(x) = max{x, x^{3}, x^{5}, …, x^{21}}, x ∈ R, is not differentiable and not continuous, respectively. Then m + n is equal to ____.', None, 3,
    lambda: (lambda f: sum(1 for p in grid(-1.5, 1.5, 3001) if abs((f(p + 1e-7) - f(p)) / 1e-7 - (f(p) - f(p - 1e-7)) / 1e-7) > 0.5) + jumps(f, [-1, -0.5, 0, 0.5, 1]))(lambda x: max(x ** k for k in range(1, 22, 2))),
    ['x < −1: x wins; −1 ≤ x ≤ 0: x^{21} wins; 0 ≤ x ≤ 1: x; x ≥ 1: x^{21}. f is continuous everywhere.', 'Slopes jump at −1, 0 and 1 → m = 3, n = 0 → 3.'], 'cont', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'cont', 'If the function f(x) = \\f{72^{x} − 9^{x} − 8^{x} + 1}{√{2} − √{1 + cos x}} for x ≠ 0, and f(0) = a log_{e} 2 log_{e} 3, is continuous at x = 0, then the value of a^{2} is equal to', ['968', '1152', '746', '1250'], 2,
    lambda: pick([968, 1152, 746, 1250], (lim(lambda x: (72 ** x - 9 ** x - 8 ** x + 1) / (math.sqrt(2) - math.sqrt(1 + math.cos(x))), 0, h=2e-2) / (math.log(2) * math.log(3))) ** 2, 1e-2),
    ['Top = (9^{x} − 1)(8^{x} − 1) ≈ 6 log 2 log 3 · x^{2}; bottom ≈ \\f{x^{2}}{4√{2}}.', 'Limit = 24√{2} log 2 log 3 → a = 24√{2}, a^{2} = 1152.'], 'cont', 3)
add(('2024', 'Apr', '2024-04-04', 1), 'cont', 'Let f : R → R be a function given by f(x) = \\f{1 − cos 2x}{x^{2}} for x < 0, f(0) = α, f(x) = \\f{β√{1 − cos x}}{x} for x > 0, where α, β ∈ R. If f is continuous at x = 0, then α^{2} + β^{2} is equal to :', ['48', '12', '3', '6'], 2,
    lambda: (lambda L, Rr: pick([48, 12, 3, 6], round(L ** 2 + (L / Rr) ** 2)))(lim(lambda x: (1 - math.cos(2 * x)) / x ** 2, 0, -1, 1e-2), lim(lambda x: math.sqrt(1 - math.cos(x)) / x, 0, 1, 1e-2)),
    ['Left limit: \\f{2 sin^{2}x}{x^{2}} → 2, so α = 2.', 'Right: β\\f{√{2}|sin(x/2)|}{x} → \\f{β}{√{2}} = 2 → β = 2√{2}. α^{2} + β^{2} = 4 + 8 = 12.'], 'cont', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'cont', 'Let f : [−1, 2] → R be given by f(x) = 2x^{2} + x + [x^{2}] − [x], where [t] denotes the greatest integer less than or equal to t. The number of points, where f is not continuous, is :', ['6', '3', '4', '5'], 3,
    lambda: pick([6, 3, 4, 5], jumps(lambda x: 2 * x * x + x + math.floor(x * x) - math.floor(x), [-1, 0, 1, math.sqrt(2), math.sqrt(3), 2], lo=-1, hi=2)),
    ['Only x with x^{2} or x an integer can be trouble: −1, 0, 1, √{2}, √{3}, 2.', 'At 1 and 2 the two jumps cancel; at −1, 0, √{2}, √{3} they do not → 4 points.'], 'cont', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'cont', 'If the function f(x) = \\f{sin 3x + α sin x − β cos 3x}{x^{3}}, x ∈ R, is continuous at x = 0, then f(0) is equal to :', ['2', '−2', '4', '−4'], 4,
    lambda: pick([2, -2, 4, -4], round(lim(lambda x: (math.sin(3 * x) - 3 * math.sin(x)) / x ** 3, 0, h=1e-2))), ['The top must → 0: β = 0. Then sin 3x + α sin x ≈ (3 + α)x − \\f{27 + α}{6}x^{3}.', 'α = −3, and f(0) = −\\f{24}{6} = −4.'], 'cont', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'cont', 'If f(x) = x^{3} sin(\\f{1}{x}) for x ≠ 0 and f(0) = 0, then', ['f"(0) = 1', 'f"(\\f{2}{π}) = \\f{24 − π^{2}}{2π}', 'f"(\\f{2}{π}) = \\f{12 − π^{2}}{2π}', 'f"(0) = 0'], 2,
    lambda: (lambda f: (lambda v: 2 if abs(v - (24 - math.pi ** 2) / (2 * math.pi)) < 1e-4 and abs(v - (12 - math.pi ** 2) / (2 * math.pi)) > 1e-2 else 0)(d2(f, 2 / math.pi, 1e-4)))(lambda x: x ** 3 * math.sin(1 / x)),
    ['f\'(x) = 3x^{2} sin \\f{1}{x} − x cos \\f{1}{x}; f\'(0) = 0 but \\f{f\'(x)}{x} has no limit, so f"(0) does not exist.', 'f"(x) = 6x sin \\f{1}{x} − 4 cos \\f{1}{x} − \\f{1}{x} sin \\f{1}{x}; at x = \\f{2}{π}: \\f{12}{π} − \\f{π}{2} = \\f{24 − π^{2}}{2π}.'], 'cont', 3)
add(('2025', 'Apr', '2025-04-07', 1), 'cont', 'The number of points of discontinuity of the function f(x) = [\\f{x^{2}}{2}] − [√{x}], x ∈ [0, 4], where [·] denotes the greatest integer function, is ____.', None, 8,
    lambda: jumps(lambda x: math.floor(x * x / 2 + 1e-12) - math.floor(math.sqrt(max(x, 0)) + 1e-12), sorted({math.sqrt(2 * k) for k in range(1, 9)} | {1.0, 4.0, 0.0}), lo=0, hi=4),
    ['[\\f{x^{2}}{2}] jumps at √{2}, 2, √{6}, √{8}, √{10}, √{12}, √{14}, 4; [√{x}] jumps at 1 and 4.', 'At 4 both jumps cancel (f stays 6) → 7 + 1 = 8 points.'], 'cont', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'cont', 'If the function f(x) = \\f{tan(tan x) − sin(sin x)}{tan x − sin x} is continuous at x = 0, then f(0) is equal to ____.', None, 2,
    lambda: round(lim(lambda x: (math.tan(math.tan(x)) - math.sin(math.sin(x))) / (math.tan(x) - math.sin(x)), 0, h=2e-2)), ['tan(tan x) ≈ x + \\f{2x^{3}}{3}, sin(sin x) ≈ x − \\f{x^{3}}{3} → top ≈ x^{3}.', 'tan x − sin x ≈ \\f{x^{3}}{2} → f(0) = 2.'], 'cont', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'cont', 'Let f : (0, π) → R be a function given by f(x) = (\\f{8}{7})^{\\f{tan 8x}{tan 7x}} for 0 < x < \\f{π}{2}, f(x) = a − 8 for x = \\f{π}{2}, f(x) = (1 + |cot x|)^{\\f{b}{a}|tan x|} for \\f{π}{2} < x < π, where a, b ∈ Z. If f is continuous at x = \\f{π}{2}, then a^{2} + b^{2} is equal to ____.', None, 81,
    lambda: (lambda L: (lambda a: (lambda b: a * a + b * b)(next(b for b in range(-20, 21) if abs(lim(lambda x: (1 + abs(1 / math.tan(x))) ** (b / a * abs(math.tan(x))), math.pi / 2, 1, 1e-4) - L) < 1e-3)))(round(L + 8)))(lim(lambda x: (8 / 7) ** (math.tan(8 * x) / math.tan(7 * x)), math.pi / 2, -1, 1e-3)),
    ['Left: \\f{tan 8x}{tan 7x} → 0 as x → \\f{π}{2} (top → 0, bottom → ∞), so the left limit is 1 → a − 8 = 1, a = 9.', 'Right: (1 + |cot x|)^{\\f{b}{a}|tan x|} → e^{b/a} = 1 → b = 0. a^{2} + b^{2} = 81.'], 'cont', 3)

# ---------------- derivatives ----------------
add(('2025', 'Apr', '2025-04-03', 1), 'deriv', 'If y(x) = \\begin{vmatrix} sin x & cos x & sin x + cos x + 1 \\\\ 27 & 28 & 27 \\\\ 1 & 1 & 1 \\end{vmatrix}, x ∈ R, then \\f{d^{2}y}{dx^{2}} + y is equal to', ['27', '28', '1', '−1'], 4,
    lambda: (lambda y: pick([27, 28, 1, -1], round(d2(y, 0.7) + y(0.7), 4)))(lambda x: (lambda a, b, c: a * (28 - 27) - b * (27 - 27) + c * (27 - 28))(math.sin(x), math.cos(x), math.sin(x) + math.cos(x) + 1)),
    ['Expand along the first row: y = sin x − (sin x + cos x + 1) = −cos x − 1.', 'y" + y = cos x − cos x − 1 = −1.'], 'deriv', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'deriv', 'If y(θ) = \\f{2 cos θ + cos 2θ}{cos 3θ + 4 cos 2θ + 5 cos θ + 2}, then at θ = \\f{π}{2}, y" + y\' + y is equal to:', ['\\f{3}{2}', '1', '\\f{1}{2}', '2'], 4,
    lambda: (lambda y: pick([1.5, 1, 0.5, 2], round(d2(y, math.pi / 2) + d1(y, math.pi / 2) + y(math.pi / 2), 4)))(lambda t: (2 * math.cos(t) + math.cos(2 * t)) / (math.cos(3 * t) + 4 * math.cos(2 * t) + 5 * math.cos(t) + 2)),
    ['With c = cos θ: top 2c^{2} + 2c − 1, bottom 2(c + 1)(2c^{2} + 2c − 1) → y = \\f{1}{2(1 + cos θ)}.', 'At \\f{π}{2}: y = \\f{1}{2}, y\' = \\f{1}{2}, y" = 1 → 2.'], 'deriv', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'deriv', 'Let f be a differentiable function in the interval (0, ∞) such that f(1) = 1 and \\lim_{t→x} \\f{t^{2}f(x) − x^{2}f(t)}{t − x} = 1 for each x > 0. Then 2f(2) + 3f(3) is equal to ____.', None, 24,
    lambda: (lambda f: round(2 * f(2) + 3 * f(3)) if abs(lim(lambda t: (t * t * f(1.7) - 1.7 ** 2 * f(t)) / (t - 1.7), 1.7) - 1) < 1e-6 and f(1) == 1 else None)(lambda x: 1 / (3 * x) + 2 * x * x / 3),
    ['The limit is 2xf(x) − x^{2}f\'(x) = 1, i.e. (\\f{f}{x^{2}})\' = −\\f{1}{x^{4}} → \\f{f}{x^{2}} = \\f{1}{3x^{3}} + C; f(1) = 1 → C = \\f{2}{3}.', 'f(x) = \\f{1}{3x} + \\f{2x^{2}}{3}: f(2) = \\f{17}{6}, f(3) = \\f{55}{9} → \\f{17}{3} + \\f{55}{3} = 24.'], 'deriv', 3)
add(('2024', 'Apr', '2024-04-06', 2), 'deriv', 'Suppose for a differentiable function h, h(0) = 0, h(1) = 1 and h\'(0) = h\'(1) = 2. If g(x) = h(e^{x})e^{h(x)}, then g\'(0) is equal to:', ['5', '3', '8', '4'], 4,
    lambda: (lambda h: pick([5, 3, 8, 4], round(d1(lambda x: h(math.exp(x)) * math.exp(h(x)), 0), 5)) if (h(0), h(1), round(d1(h, 0), 6), round(d1(h, 1), 6)) == (0, 1, 2, 2) else None)(lambda x: 2 * x ** 3 - 3 * x * x + 2 * x),
    ['g\'(x) = h\'(e^{x})e^{x}e^{h(x)} + h(e^{x})e^{h(x)}h\'(x).', 'At 0: h\'(1)·1·1 + h(1)·1·h\'(0) = 2 + 2 = 4.'], 'deriv', 2)
add(('2025', 'Apr', '2025-04-02', 1), 'deriv', 'Let f : R → R be a twice differentiable function such that (sin x cos y)(f(2x + 2y) − f(2x − 2y)) = (cos x sin y)(f(2x + 2y) + f(2x − 2y)), for all x, y ∈ R. If f\'(0) = \\f{1}{2}, then the value of 24f"(\\f{5π}{3}) is :', ['−2', '2', '3', '−3'], 4,
    lambda: (lambda f: pick([-2, 2, 3, -3], round(24 * d2(f, 5 * math.pi / 3), 4)) if all(abs(math.sin(x) * math.cos(y) * (f(2 * x + 2 * y) - f(2 * x - 2 * y)) - math.cos(x) * math.sin(y) * (f(2 * x + 2 * y) + f(2 * x - 2 * y))) < 1e-9 for x, y in [(0.3, 1.1), (2.0, -0.7), (1.4, 0.2)]) and abs(d1(f, 0) - 0.5) < 1e-8 else None)(lambda t: math.sin(t / 2)),
    ['Put u = 2x + 2y, v = 2x − 2y: f(u) sin \\f{v}{2} = f(v) sin \\f{u}{2} → f(t) = k sin \\f{t}{2}; f\'(0) = \\f{k}{2} = \\f{1}{2} → k = 1.', 'f" = −\\f{1}{4} sin \\f{t}{2}: at \\f{5π}{3} it is −\\f{1}{8} → 24 × (−\\f{1}{8}) = −3.'], 'deriv', 3)
add(('2025', 'Apr', '2025-04-02', 1), 'deriv', 'Let f : R → R be a thrice differentiable odd function satisfying f\'(x) ≥ 0, f"(x) = f(x), f(0) = 0, f\'(0) = 3. Then 9f(log_{e} 3) is equal to ____.', None, 36,
    lambda: (lambda f: round(9 * f(math.log(3))) if abs(d2(f, 0.8) - f(0.8)) < 1e-5 and abs(d1(f, 0) - 3) < 1e-8 and f(0) == 0 else None)(lambda x: 3 * math.sinh(x)),
    ['f" = f with f(0) = 0, f\'(0) = 3 gives f(x) = 3 sinh x = \\f{3}{2}(e^{x} − e^{−x}).', 'f(log 3) = \\f{3}{2}(3 − \\f{1}{3}) = 4 → 36.'], 'deriv', 2)

# ---------------- applications: maxima, minima, monotonicity ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'app', 'If the function f(x) = 2x^{3} − 9ax^{2} + 12a^{2}x + 1, where a > 0, attains its local maximum and local minimum values at p and q, respectively, such that p^{2} = q, then f(3) is equal to :', ['10', '55', '37', '23'], 3,
    lambda: (lambda a: pick([10, 55, 37, 23], round(2 * 27 - 9 * a * 9 + 12 * a * a * 3 + 1, 6)))(next(a for a in [k / 100 for k in range(1, 1000)] if (lambda T: abs(T[0] ** 2 - T[1]) < 1e-6)(turn(lambda x, a=a: 2 * x ** 3 - 9 * a * x * x + 12 * a * a * x + 1, 0, 40)))),
    ['f\'(x) = 6(x − a)(x − 2a): local max at x = a, local min at x = 2a.', 'a^{2} = 2a → a = 2 → f(3) = 54 − 162 + 144 + 1 = 37.'], 'app', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'app', 'Let f : R → R be a function defined by f(x) = ||x + 2| − 2|x||. If m is the number of points of local minima and n is the number of points of local maxima of f, then m + n is', ['5', '3', '2', '4'], 2,
    lambda: pick([5, 3, 2, 4], sum(extrema(lambda x: abs(abs(x + 2) - 2 * abs(x)), -10.0003, 10.0007))), ['The inside vanishes at x = −\\f{2}{3} and 2: f = 0 there, two minima.', 'At x = 0, f = 2 with f rising before and falling after: one maximum. At x = −2 f keeps decreasing → m + n = 3.'], 'app', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'app', 'Let a > 0. If the function f(x) = 6x^{3} − 45ax^{2} + 108a^{2}x + 1 attains its local maximum and minimum values at the points x_{1} and x_{2} respectively such that x_{1}x_{2} = 54, then a + x_{1} + x_{2} is equal to :', ['15', '13', '18', '24'], 3,
    lambda: (lambda a: pick([15, 13, 18, 24], a + 2 * a + 3 * a) if abs(d1(lambda x: 6 * x ** 3 - 45 * a * x * x + 108 * a * a * x + 1, 2 * a)) < 1e-4 and abs(d1(lambda x: 6 * x ** 3 - 45 * a * x * x + 108 * a * a * x + 1, 3 * a)) < 1e-4 else None)(math.sqrt(54 / 6)),
    ['f\'(x) = 18(x − 2a)(x − 3a): max at 2a, min at 3a.', '6a^{2} = 54 → a = 3 → 3 + 6 + 9 = 18.'], 'app', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'app', 'Let f(x) = 3√{x − 2} + √{4 − x} be a real valued function. If α and β are respectively the minimum and the maximum values of f, then α^{2} + 2β^{2} is equal to', ['44', '42', '24', '38'], 2,
    lambda: (lambda v: pick([44, 42, 24, 38], round(min(v) ** 2 + 2 * max(v) ** 2, 4)))([3 * math.sqrt(max(x - 2, 0)) + math.sqrt(max(4 - x, 0)) for x in grid(2, 4, 200001)]),
    ['Domain [2, 4]. By Cauchy–Schwarz the maximum is √{(9 + 1)(2)} = 2√{5} (at x = 3.8).', 'Minimum at an end: f(2) = √{2}. α^{2} + 2β^{2} = 2 + 40 = 42.'], 'app', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'app', 'Let the sum of the maximum and the minimum values of the function f(x) = \\f{2x^{2} − 3x + 8}{2x^{2} + 3x + 8} be \\f{m}{n}, where gcd(m, n) = 1. Then m + n is equal to :', ['182', '217', '195', '201'], 4,
    lambda: (lambda v: (lambda s: pick([182, 217, 195, 201], s.numerator + s.denominator))(F(max(v) + min(v)).limit_denominator(200)))([(2 * x * x - 3 * x + 8) / (2 * x * x + 3 * x + 8) for x in grid(-50, 50, 400001)]),
    ['Set y = f(x): (2y − 2)x^{2} + 3(y + 1)x + 8(y − 1) = 0 must have real x → (11 − 5y)(11y − 5) ≥ 0.', 'y ∈ [\\f{5}{11}, \\f{11}{5}] → sum \\f{146}{55} → 201.'], 'app', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'app', 'For the function f(x) = sin x + 3x − \\f{2}{π}(x^{2} + x), where x ∈ [0, \\f{π}{2}], consider the following two statements : (I) f is increasing in (0, \\f{π}{2}). (II) f\' is decreasing in (0, \\f{π}{2}). Between the above two statements,', ['only (I) is true.', 'only (II) is true.', 'neither (I) nor (II) is true.', 'both (I) and (II) are true.'], 4,
    lambda: (lambda f: (lambda a, b: {(True, False): 1, (False, True): 2, (False, False): 3, (True, True): 4}[(a, b)])(all(d1(f, x) > 0 for x in grid(0.01, 1.56, 300)), all(d2(f, x) < 0 for x in grid(0.01, 1.56, 300))))(lambda x: math.sin(x) + 3 * x - 2 / math.pi * (x * x + x)),
    ['f\'(x) = cos x + 3 − \\f{2}{π}(2x + 1); f"(x) = −sin x − \\f{4}{π} < 0, so f\' is decreasing.', 'Its smallest value f\'(\\f{π}{2}) = 1 − \\f{2}{π} > 0 → f is increasing. Both true.'], 'app', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'app', 'If the function f(x) = (\\f{1}{x})^{2x}; x > 0 attains the maximum value at x = \\f{1}{e} then :', ['e^{π} < π^{e}', 'e^{2π} < (2π)^{e}', 'e^{π} > π^{e}', '(2e)^{π} > π^{(2e)}'], 3,
    lambda: (lambda xs: 3 if (math.e ** math.pi > math.pi ** math.e) and not (math.e ** math.pi < math.pi ** math.e) and not (math.e ** (2 * math.pi) < (2 * math.pi) ** math.e) and not ((2 * math.e) ** math.pi > math.pi ** (2 * math.e)) else 0)(None),
    ['log f = −2x log x; equivalently x^{1/x} is largest at x = e, so t^{1/t} decreases for t > e.', 'π > e → π^{1/π} < e^{1/e} → π^{e} < e^{π}.'], 'app', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'app', 'The interval in which the function f(x) = x^{x}, x > 0, is strictly increasing is ____.', ['(0, \\f{1}{e}]', '[\\f{1}{e^{2}}, 1)', '(0, ∞)', '[\\f{1}{e}, ∞)'], 4,
    lambda: 4 if all(d1(lambda x: x ** x, x) > 0 for x in grid(1 / math.e + 1e-3, 10, 500)) and all(d1(lambda x: x ** x, x) < 0 for x in grid(0.01, 1 / math.e - 1e-3, 200)) else 0,
    ['f\'(x) = x^{x}(1 + log x).', 'Positive exactly when log x > −1, i.e. x > \\f{1}{e}.'], 'app', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'app', 'Let x = −1 and x = 2 be the critical points of the function f(x) = x^{3} + ax^{2} + b log_{e}|x| + 1, x ≠ 0. Let m and M respectively be the absolute minimum and the absolute maximum values of f in the interval [−2, −\\f{1}{2}]. Then |M + m| is equal to ____. (Take log_{e} 2 = 0.7) :', ['21.1', '22.1', '19.8', '20.9'], 1,
    lambda: (lambda a, b: (lambda f, g: (lambda xs: pick([21.1, 22.1, 19.8, 20.9], round(abs(g(max(xs, key=f)) + g(min(xs, key=f))), 4)))(grid(-2, -0.5, 30001) + [-1.0]))(lambda x: x ** 3 + a * x * x + b * math.log(abs(x)) + 1, lambda x: x ** 3 + a * x * x + b * (math.log(abs(x)) / math.log(2) * 0.7) + 1) if abs(3 - 2 * a - b) < 1e-12 and abs(12 + 4 * a + b / 2) < 1e-12 else None)(-4.5, 12),
    ['f\'(x) = 3x^{2} + 2ax + \\f{b}{x} = 0 at −1 and 2: 3 − 2a − b = 0, 12 + 4a + \\f{b}{2} = 0 → a = −\\f{9}{2}, b = 12.', 'f(−2) = −16.6, f(−1) = −4.5 (max), f(−\\f{1}{2}) = −8.65 → |−4.5 − 16.6| = 21.1.'], 'app', 3)
add(('2025', 'Apr', '2025-04-07', 2), 'app', 'Let f : R → R be a polynomial function of degree four having extreme values at x = 4 and x = 5. If \\lim_{x→0} \\f{f(x)}{x^{2}} = 5, then f(2) is equal to :', ['10', '8', '12', '14'], 1,
    lambda: (lambda f: pick([10, 8, 12, 14], round(f(2), 6)) if abs(d1(f, 4)) < 1e-6 and abs(d1(f, 5)) < 1e-6 and abs(lim(lambda x: f(x) / x ** 2, 0) - 5) < 1e-4 else None)(lambda x: 5 * x * x - 1.5 * x ** 3 + x ** 4 / 8),
    ['The limit forces f(x) = 5x^{2} + ax^{3} + bx^{4}; f\'(x) = x(10 + 3ax + 4bx^{2}) vanishes at 4 and 5.', '4b · 20 = 10 → b = \\f{1}{8}; 3a = −4b · 9 → a = −\\f{3}{2}. f(2) = 20 − 12 + 2 = 10.'], 'app', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'app', 'Let the function f(x) = \\f{x}{3} + \\f{3}{x} + 3, x ≠ 0 be strictly increasing in (−∞, α_{1}) ∪ (α_{2}, ∞) and strictly decreasing in (α_{3}, α_{4}) ∪ (α_{4}, α_{5}). Then Σ_{i=1}^{5} α_{i}^{2} is equal to', ['48', '36', '28', '40'], 2,
    lambda: pick([48, 36, 28, 40], (lambda c: 2 * c * c + c * c + 0 + c * c)(next(x for x in grid(0.1, 10, 9901) if abs(1 / 3 - 3 / x ** 2) < 1e-9))),
    ['f\'(x) = \\f{1}{3} − \\f{3}{x^{2}} = 0 at x = ±3.', 'α_{1} = −3, α_{2} = 3, α_{3} = −3, α_{4} = 0, α_{5} = 3 → 9 + 9 + 9 + 0 + 9 = 36.'], 'app', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'app', 'If the function f(x) = 2x^{3} − 9ax^{2} + 12a^{2}x + 1, a > 0 has a local maximum at x = α and a local minimum at x = α^{2}, then α and α^{2} are the roots of the equation :', ['x^{2} − 6x + 8 = 0', '8x^{2} + 6x − 8 = 0', '8x^{2} − 6x + 1 = 0', 'x^{2} + 6x + 8 = 0'], 1,
    lambda: (lambda al: pick([(6, 8), (-0.75, -1), (0.75, 0.125), (-6, 8)], (al + al * al, al ** 3)))(2),
    ['Max at x = a, min at x = 2a; so a = α and 2a = α^{2} → α = 2.', 'Roots 2 and 4: x^{2} − 6x + 8 = 0.'], 'app', 2)
add(('2024', 'Apr', '2024-04-08', 1), 'app', 'For the function f(x) = (cos x) − x + 1, x ∈ R, between the following two statements (S1) f(x) = 0 for only one value of x in [0, π]. (S2) f(x) is decreasing in [0, \\f{π}{2}] and increasing in [\\f{π}{2}, π].', ['Both (S1) and (S2) are correct', 'Only (S1) is correct', 'Both (S1) and (S2) are incorrect', 'Only (S2) is correct'], 2,
    lambda: (lambda f: (lambda s1, s2: {(True, True): 1, (True, False): 2, (False, False): 3, (False, True): 4}[(s1, s2)])(sum(1 for a, b in zip(grid(0, math.pi, 10001), grid(0, math.pi, 10001)[1:]) if f(a) * f(b) < 0) == 1, all(d1(f, x) > 0 for x in grid(1.6, 3.1, 50))))(lambda x: math.cos(x) - x + 1),
    ['f\'(x) = −sin x − 1 ≤ 0: f decreases on all of R, so (S2) is false.', 'f(0) = 2 > 0, f(π) = −π < 0 and f is decreasing → exactly one root: (S1) true.'], 'app', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'app', 'Let the set of all positive values of λ, for which the point of local minimum of the function (1 + x(λ^{2} − x^{2})) satisfies \\f{x^{2} + x + 2}{x^{2} + 5x + 6} < 0, be (α, β). Then α^{2} + β^{2} is equal to ____.', None, 39,
    lambda: (lambda ok: (lambda L: round(min(L) ** 2 + max(L) ** 2))([l for l in grid(0.01, 10, 99901) if ok(l)]))(lambda l: (lambda x: (x * x + x + 2) / (x * x + 5 * x + 6) < 0)(-l / math.sqrt(3))),
    ['f\'(x) = λ^{2} − 3x^{2}: the local minimum is at x = −\\f{λ}{√{3}}.', 'The fraction is negative only for −3 < x < −2 → 2√{3} < λ < 3√{3} → 12 + 27 = 39.'], 'app', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'app', 'The number of critical points of the function f(x) = |\\f{sin x}{x}| for x ≠ 0, f(0) = 1, in the interval (−2π, 2π) is equal to :', ['1', '3', '5', '7'], 3,
    lambda: pick([1, 3, 5, 7], sum(extrema(lambda x: abs(math.sin(x) / x) if x else 1.0, -2 * math.pi + 1e-3, 2 * math.pi - 1e-3, 400001)) - 0),
    ['|\\f{sin x}{x}| has a peak at 0, corners (minima) at ±π, and turning points where tan x = x (about ±4.49).', 'Total 5 critical points.'], 'app', 3)
add(('2025', 'Apr', '2025-04-02', 2), 'app', 'Let A(4, −2), B(1, 1) and C(9, −3) be the vertices of a triangle ABC. Then the maximum area of the parallelogram AFDE, formed with vertices D, E and F on the sides BC, CA and AB of the triangle ABC respectively, is ____.', None, 3,
    lambda: (lambda T: round(max(2 * t * (1 - t) * T for t in grid(0, 1, 10001)), 6))(abs((1 - 4) * (-3 + 2) - (9 - 4) * (1 + 2)) / 2),
    ['If AF = t·AB then AE = (1 − t)AC and the parallelogram\'s area is 2t(1 − t) × area(ABC).', 'Area(ABC) = 6; the maximum (t = \\f{1}{2}) is half of it: 3.'], 'app', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'app', 'Let A be the region enclosed by the parabola y^{2} = 2x and the line x = 24. Then the maximum area of the rectangle inscribed in the region A is ____.', None, 128,
    lambda: round(max(2 * math.sqrt(2 * t) * (24 - t) for t in grid(0, 24, 240001))), ['A rectangle from x = t to x = 24 with height 2√{2t}: area 2√{2t}(24 − t).', 'Derivative zero at t = 8 → 2 × 4 × 16 = 128.'], 'app', 2)
for _p in P: _p['t'] = _p['fam']
