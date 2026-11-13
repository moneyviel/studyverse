"""Real JEE Main questions — Mathematics Unit 8: Integral Calculus. Our own solutions; chk re-solves each one
numerically and independently — definite integrals by the midpoint rule on a fine grid, areas by integrating the
height of the region slice by slice, antiderivatives by differentiating the claimed answer and comparing with the
integrand. Skipped: items whose key we could not reproduce (an area whose printed key does not match the two
parabolas shown, and an antiderivative item), items cut in the scan and differential-equation items (next unit)."""
import math
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
def integ(f, a, b, n=200000):
    h = (b - a) / n; return h * sum(f(a + (i + 0.5) * h) for i in range(n))
def area(lo_f, hi_f, a, b, n=200000): return integ(lambda x: max(0.0, hi_f(x) - lo_f(x)), a, b, n)
def d1(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
def same_deriv(F_, f, xs): return all(abs(d1(F_, x) - f(x)) < 1e-5 * max(1, abs(f(x))) for x in xs)
S2, S3, PI, LN = math.sqrt(2), math.sqrt(3), math.pi, math.log
def near(v, w, tol=1e-4): return abs(v - w) <= tol * max(1, abs(w))

# ---------------- areas ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'area', 'If the area of the region {(x, y) : |4 − x^{2}| ≤ y ≤ x^{2}, y ≤ 4, x ≥ 0} is (\\f{80√{2}}{α} − β), α, β ∈ N, then α + β is equal to ____.', None, 22,
    lambda: (lambda A: next(a + b for a in range(1, 40) for b in range(1, 40) if near(80 * S2 / a - b, A, 1e-6)))(area(lambda x: abs(4 - x * x), lambda x: min(x * x, 4), 0, 3)),
    ['The region lies between x = √{2} (where 4 − x^{2} = x^{2}) and x = 2√{2} (where x^{2} − 4 = 4).', '∫_{√{2}}^{2}(x^{2} − (4 − x^{2}))dx + ∫_{2}^{2√{2}}(4 − (x^{2} − 4))dx = \\f{40√{2}}{3} − 16 = \\f{80√{2}}{6} − 16 → α + β = 6 + 16 = 22.'], 'area', 3)
add(('2025', 'Apr', '2025-04-03', 1), 'area', 'The area of the region bounded by the curve y = max{|x|, x|x − 2|}, the x-axis and the lines x = −2 and x = 4 is equal to ____.', None, 12,
    lambda: round(integ(lambda x: abs(max(abs(x), x * abs(x - 2))), -2, 4), 4), ['On [−2, 0] the max is |x|; on [0, 1] it is x(2 − x); on [1, 3] it is x; on [3, 4] it is x(x − 2).', '2 + \\f{2}{3} + 4 + \\f{16}{3} = 12.'], 'area', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'area', 'The area of the region {(x, y) : |x − y| ≤ y ≤ 4√{x}} is', ['\\f{512}{3}', '\\f{2048}{3}', '\\f{1024}{3}', '512'], 3,
    lambda: pick([512 / 3, 2048 / 3, 1024 / 3, 512], round(area(lambda x: x / 2, lambda x: 4 * math.sqrt(x), 0, 64), 3), 1e-4),
    ['|x − y| ≤ y means y ≥ \\f{x}{2}. The curves y = \\f{x}{2} and y = 4√{x} meet at x = 64.', '∫_{0}^{64}(4√{x} − \\f{x}{2})dx = \\f{2048}{3} − 1024 = \\f{1024}{3}.'], 'area', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'area', 'If the area of the region {(x, y) : |x − 5| ≤ y ≤ 4√{x}} is A, then 3A is equal to ____.', None, 368,
    lambda: round(3 * area(lambda x: abs(x - 5), lambda x: 4 * math.sqrt(x), 0, 30), 3), ['y = 4√{x} meets y = 5 − x at x = 1 and y = x − 5 at x = 25.', 'A = ∫_{1}^{25} 4√{x} dx − ∫_{1}^{25}|x − 5|dx = \\f{496}{3} − 40 = \\f{368}{3} → 3A = 368.'], 'area', 3)
add(('2024', 'Apr', '2024-04-04', 2), 'area', 'The area (in sq. units) of the region described by {(x, y) : y^{2} ≤ 2x, and y ≥ 4x − 1} is', ['\\f{11}{32}', '\\f{8}{9}', '\\f{11}{12}', '\\f{9}{32}'], 4,
    lambda: pick([11 / 32, 8 / 9, 11 / 12, 9 / 32], round(area(lambda y: y * y / 2, lambda y: (y + 1) / 4, -1, 1), 5), 1e-3),
    ['Slice horizontally: \\f{y^{2}}{2} ≤ x ≤ \\f{y + 1}{4}; they meet at y = −\\f{1}{2} and y = 1.', '∫_{−1/2}^{1}(\\f{y + 1}{4} − \\f{y^{2}}{2})dy = \\f{9}{32}.'], 'area', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'area', 'The area enclosed between the curves y = x|x| and y = x − |x| is :', ['\\f{8}{3}', '\\f{2}{3}', '1', '\\f{4}{3}'], 4,
    lambda: pick([8 / 3, 2 / 3, 1, 4 / 3], round(integ(lambda x: abs(x * abs(x) - (x - abs(x))), -2, 0), 5), 1e-3),
    ['For x ≥ 0 the curves are y = x^{2} and y = 0, which only touch at 0; for x < 0 they are y = −x^{2} and y = 2x, meeting at x = −2.', '∫_{−2}^{0}(−x^{2} − 2x)dx = \\f{4}{3}.'], 'area', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'area', 'Let the area of the region enclosed by the curves y = 3x, 2y = 27 − 3x and y = 3x − x√{x} be A. Then 10A is equal to ____.', ['184', '154', '172', '162'], 4,
    lambda: pick([184, 154, 172, 162], round(10 * area(lambda x: 3 * x - x * math.sqrt(x), lambda x: min(3 * x, (27 - 3 * x) / 2), 0, 9), 3), 1e-3),
    ['y = 3x and 2y = 27 − 3x meet at x = 3; the line meets y = 3x − x√{x} at x = 9.', 'A = ∫_{0}^{3}x√{x}dx + ∫_{3}^{9}(\\f{27 − 3x}{2} − 3x + x√{x})dx = 16.2 → 10A = 162.'], 'area', 3)
add(('2025', 'Apr', '2025-04-07', 1), 'area', 'If the area of the region bounded by the curves y = 4 − \\f{x^{2}}{4} and y = \\f{x − 4}{2} is equal to α, then 6α equals', ['250', '220', '240', '210'], 1,
    lambda: pick([250, 220, 240, 210], round(6 * area(lambda x: (x - 4) / 2, lambda x: 4 - x * x / 4, -6, 4), 3), 1e-3),
    ['They meet where x^{2} + 2x − 24 = 0: x = −6 and 4.', 'α = ∫_{−6}^{4}(6 − \\f{x}{2} − \\f{x^{2}}{4})dx = \\f{125}{3} → 6α = 250.'], 'area', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'area', 'If the area of the region {(x, y) : 1 + x^{2} ≤ y ≤ min{x + 7, 11 − 3x}} is A, then 3A is equal to', ['46', '47', '49', '50'], 4,
    lambda: pick([46, 47, 49, 50], round(3 * area(lambda x: 1 + x * x, lambda x: min(x + 7, 11 - 3 * x), -3, 3), 3), 1e-3),
    ['The lines meet at x = 1; the parabola meets y = x + 7 at x = −2 and y = 11 − 3x at x = 2.', 'A = ∫_{−2}^{1}(6 + x − x^{2})dx + ∫_{1}^{2}(10 − 3x − x^{2})dx = \\f{27}{2} + \\f{23}{6} = \\f{50}{3}.'], 'area', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'area', 'The area of the region in the first quadrant inside the circle x^{2} + y^{2} = 8 and outside the parabola y^{2} = 2x is equal to :', ['\\f{π}{2} − \\f{1}{3}', 'π − \\f{2}{3}', '\\f{π}{2} − \\f{2}{3}', 'π − \\f{1}{3}'], 2,
    lambda: pick([PI / 2 - 1 / 3, PI - 2 / 3, PI / 2 - 2 / 3, PI - 1 / 3], round(integ(lambda y: min(y * y / 2, math.sqrt(max(8 - y * y, 0))), 0, 2 * S2), 5), 1e-3),
    ['Outside the parabola means x < \\f{y^{2}}{2}. Slice horizontally: 0 ≤ x ≤ min{\\f{y^{2}}{2}, √{8 − y^{2}}}; the curves meet at (2, 2).', '∫_{0}^{2}\\f{y^{2}}{2}dy + ∫_{2}^{2√{2}}√{8 − y^{2}}dy = \\f{4}{3} + (2π − π − 2) = π − \\f{2}{3}.'], 'area', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'area', 'Let the area of the region enclosed by the curve y = min{sin x, cos x} and the x-axis between x = −π to x = π be A. Then A^{2} is equal to ____.', None, 16,
    lambda: round(integ(lambda x: abs(min(math.sin(x), math.cos(x))), -PI, PI) ** 2, 4), ['Track which is smaller: sin x on (−\\f{3π}{4}, \\f{π}{4}), cos x elsewhere.', 'Adding the pieces of |min{sin x, cos x}| gives A = 4 → A^{2} = 16.'], 'area', 3)
add(('2024', 'Apr', '2024-04-09', 2), 'area', 'The area (in square units) of the region enclosed by the ellipse x^{2} + 3y^{2} = 18 in the first quadrant below the line y = x is :', ['√{3}π + \\f{3}{4}', '√{3}π', '√{3}π − \\f{3}{4}', '√{3}π + 1'], 2,
    lambda: pick([S3 * PI + 0.75, S3 * PI, S3 * PI - 0.75, S3 * PI + 1], round(integ(lambda x: max(0.0, min(x, math.sqrt(max(18 - x * x, 0) / 3))), 0, math.sqrt(18)), 5), 1e-3),
    ['The line meets the ellipse at (\\f{3}{√{2}}, \\f{3}{√{2}}); below the line the region is bounded by y = x then by the ellipse.', 'In the stretched picture (y → √{3}y) this is a circular sector: area = √{3}π.'], 'area', 3)
add(('2026', 'Apr', '2026-04-02', 2), 'area', 'If the area of the region bounded by 16x^{2} − 9y^{2} = 144 and 8x − 3y = 24 is A, then 3(A + 6 log_{e}(3)) is equal to ____.', None, 24,
    lambda: round(3 * (area(lambda y: max(3 + 3 * y / 8, 0), lambda y: 3 * math.sqrt(1 + y * y / 16) if True else 0, 0, 16 / 3 * 0 + 8) * 0 + area(lambda y: 3 * math.sqrt(1 + y * y / 16), lambda y: 3 + 3 * y / 8, 0, 8) + 6 * LN(3)), 3),
    ['The line passes through the vertex (3, 0) and meets the right branch again at (5, \\f{16}{3}); slicing horizontally, x runs from the hyperbola x = 3√{1 + \\f{y^{2}}{16}} to the line x = 3 + \\f{3y}{8}.', 'A = 8 − 6 log 3 → 3(A + 6 log 3) = 24.'], 'area', 3)
add(('2026', 'Jan', '2026-01-21', 2), 'area', 'If the area of the region {(x, y) : 1 − 2x ≤ y ≤ 4 − x^{2}, x ≥ 0, y ≥ 0} is \\f{α}{β}, α, β ∈ N, gcd(α, β) = 1, then the value of (α + β) is :', ['73', '85', '91', '67'], 1,
    lambda: (lambda A: pick([73, 85, 91, 67], (lambda f: f.numerator + f.denominator)(F(A).limit_denominator(100))))(area(lambda x: max(1 - 2 * x, 0), lambda x: 4 - x * x, 0, 2)),
    ['For 0 ≤ x ≤ \\f{1}{2} the bottom is 1 − 2x, then y = 0; the top is 4 − x^{2} up to x = 2.', 'A = \\f{16}{3} − \\f{1}{4} = \\f{61}{12} → 61 + 12 = 73.'], 'area', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'area', 'The area of the region {(x, y) : x^{2} + 4x + 2 ≤ y ≤ |x + 2|} is equal to', ['\\f{24}{5}', '5', '\\f{20}{3}', '7'], 3,
    lambda: pick([24 / 5, 5, 20 / 3, 7], round(area(lambda x: x * x + 4 * x + 2, lambda x: abs(x + 2), -6, 2), 4), 1e-3),
    ['Shift t = x + 2: t^{2} − 2 ≤ y ≤ |t|, symmetric about t = 0, meeting at |t| = 2.', '2∫_{0}^{2}(t − t^{2} + 2)dt = 2(2 − \\f{8}{3} + 4) = \\f{20}{3}.'], 'area', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'area', 'The area (in sq. units) of the region {(x, y) : 0 ≤ y ≤ 2|x| + 1, 0 ≤ y ≤ x^{2} + 1, |x| ≤ 3} is', ['\\f{32}{3}', '\\f{17}{3}', '\\f{64}{3}', '\\f{80}{3}'], 3,
    lambda: pick([32 / 3, 17 / 3, 64 / 3, 80 / 3], round(integ(lambda x: min(2 * abs(x) + 1, x * x + 1), -3, 3), 4), 1e-3),
    ['The upper edge is the smaller of 2|x| + 1 and x^{2} + 1: the parabola for |x| ≤ 2, the line beyond.', '2[∫_{0}^{2}(x^{2} + 1)dx + ∫_{2}^{3}(2x + 1)dx] = 2(\\f{14}{3} + 6) = \\f{64}{3}.'], 'area', 2)
add(('2025', 'Jan', '2025-01-28', 2), 'area', 'The area of the region bounded by the curves x(1 + y^{2}) = 1 and y^{2} = 2x is:', ['\\f{1}{2}(\\f{π}{2} − \\f{1}{3})', '\\f{π}{2} − \\f{1}{3}', '2(\\f{π}{2} − \\f{1}{3})', '\\f{π}{4} − \\f{1}{3}'], 2,
    lambda: pick([0.5 * (PI / 2 - 1 / 3), PI / 2 - 1 / 3, 2 * (PI / 2 - 1 / 3), PI / 4 - 1 / 3], round(area(lambda y: y * y / 2, lambda y: 1 / (1 + y * y), -1, 1), 5), 1e-3),
    ['Slice horizontally: \\f{y^{2}}{2} ≤ x ≤ \\f{1}{1 + y^{2}}; they meet at y = ±1.', '∫_{−1}^{1}(\\f{1}{1 + y^{2}} − \\f{y^{2}}{2})dy = \\f{π}{2} − \\f{1}{3}.'], 'area', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'area', 'Let the area of the region {(x, y) : 2y ≤ x^{2} + 3, y + |x| ≤ 3, y ≥ |x − 1|} be A. Then 6A is equal to :', ['14', '16', '18', '12'], 1,
    lambda: pick([14, 16, 18, 12], round(6 * area(lambda x: abs(x - 1), lambda x: min((x * x + 3) / 2, 3 - abs(x)), -3, 3), 3), 1e-3),
    ['Upper edge: the smaller of \\f{x^{2} + 3}{2} and 3 − |x|; lower edge |x − 1|.', 'Add the pieces between the crossing points: A = \\f{7}{3} → 6A = 14.'], 'area', 3)
add(('2025', 'Jan', '2025-01-29', 2), 'area', 'Let the area enclosed between the curves |y| = 1 − x^{2} and x^{2} + y^{2} = 1 be α. If 9α = βπ + γ; β, γ are integers, then the value of |β − γ| equals.', ['18', '15', '33', '27'], 3,
    lambda: (lambda a: pick([18, 15, 33, 27], next(abs(b - g) for b in range(-20, 21) for g in range(-60, 61) if abs(b * PI + g - 9 * a) < 1e-3)))(integ(lambda x: 2 * (math.sqrt(max(1 - x * x, 0)) - (1 - x * x)), -1, 1)),
    ['The curve |y| = 1 − x^{2} sits inside the unit circle; between them the area is π − 2∫_{−1}^{1}(1 − x^{2})dx = π − \\f{8}{3}.', '9α = 9π − 24 → |9 − (−24)| = 33.'], 'area', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'area', 'The area of the region {(x, y) : y ≤ π − |x|, y ≤ |x sin x|, y ≥ 0} is:', ['1 + \\f{π^{2}}{8}', '2 + \\f{π^{2}}{4}', '\\f{π^{2}}{8} − 1', '4 + \\f{π^{2}}{2}'], 2,
    lambda: pick([1 + PI ** 2 / 8, 2 + PI ** 2 / 4, PI ** 2 / 8 - 1, 4 + PI ** 2 / 2], round(integ(lambda x: max(0.0, min(PI - abs(x), abs(x * math.sin(x)))), -PI, PI), 5), 1e-3),
    ['y = |x sin x| meets y = π − |x| at |x| = \\f{π}{2}. Use symmetry: twice the area for x ≥ 0.', '2[∫_{0}^{π/2} x sin x dx + ∫_{π/2}^{π}(π − x)dx] = 2(1 + \\f{π^{2}}{8}) = 2 + \\f{π^{2}}{4}.'], 'area', 3)
add(('2026', 'Jan', '2026-01-22', 2), 'area', 'The area of the region A = {(x, y) : 4x^{2} + y^{2} ≤ 8 and y^{2} ≤ 4x} is:', ['π + 4', 'π + \\f{2}{3}', '\\f{π}{2} + 2', '\\f{π}{2} + \\f{1}{3}'], 2,
    lambda: pick([PI + 4, PI + 2 / 3, PI / 2 + 2, PI / 2 + 1 / 3], round(area(lambda y: y * y / 4, lambda y: math.sqrt(max(8 - y * y, 0) / 4), -2, 2), 5), 1e-3),
    ['Slice horizontally: \\f{y^{2}}{4} ≤ x ≤ \\f{√{8 − y^{2}}}{2}; the curves meet at y = ±2.', '∫_{−2}^{2}(\\f{√{8 − y^{2}}}{2} − \\f{y^{2}}{4})dy = (π + 2) − \\f{4}{3} = π + \\f{2}{3}.'], 'area', 3)
add(('2026', 'Apr', '2026-04-05', 1), 'area', 'The area of the region R = {(x, y) : xy ≤ 27, 1 ≤ y ≤ x^{2}} is equal to:', ['78 log_{e}3 − \\f{52}{3}', '54 log_{e}3 − \\f{52}{3}', '54 log_{e}3 − \\f{26}{3}', '54 log_{e}3 + \\f{26}{3}'], 2,
    lambda: pick([78 * LN(3) - 52 / 3, 54 * LN(3) - 52 / 3, 54 * LN(3) - 26 / 3, 54 * LN(3) + 26 / 3], round(area(lambda y: math.sqrt(y), lambda y: 27 / y, 1, 9), 5), 1e-3),
    ['Slice horizontally: √{y} ≤ x ≤ \\f{27}{y} (x > 0 since xy ≤ 27 with x ≥ √{y}); they meet at y = 9.', '∫_{1}^{9}(\\f{27}{y} − √{y})dy = 54 log 3 − \\f{52}{3}.'], 'area', 3)
add(('2026', 'Jan', '2026-01-23', 2), 'area', 'The area of the region enclosed between the circles x^{2} + y^{2} = 4 and x^{2} + (y − 2)^{2} = 4 is :', ['\\f{2}{3}(2π − 3√{3})', '\\f{4}{3}(2π − 3√{3})', '\\f{4}{3}(2π − √{3})', '\\f{2}{3}(4π − 3√{3})'], 4,
    lambda: pick([2 / 3 * (2 * PI - 3 * S3), 4 / 3 * (2 * PI - 3 * S3), 4 / 3 * (2 * PI - S3), 2 / 3 * (4 * PI - 3 * S3)], round(area(lambda x: 2 - math.sqrt(max(4 - x * x, 0)), lambda x: math.sqrt(max(4 - x * x, 0)), -2, 2), 5), 1e-3),
    ['The circles meet at y = 1, x = ±√{3}: the lens is two equal circular segments.', 'Each segment: \\f{1}{2} · 4(\\f{2π}{3} − sin \\f{2π}{3}) = \\f{4π}{3} − √{3}; twice that = \\f{2}{3}(4π − 3√{3}).'], 'area', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'area', 'The area of the region {(x, y) : 0 ≤ y ≤ 6 − x, y^{2} ≥ 4x − 3, x ≥ 0} is:', ['8', '9', '12', '15'], 2,
    lambda: pick([8, 9, 12, 15], round(integ(lambda y: max(0.0, min(6 - y, (y * y + 3) / 4)), 0, 6), 4), 1e-3),
    ['Slice horizontally: 0 ≤ x ≤ min{6 − y, \\f{y^{2} + 3}{4}}; the two meet at y = 3.', '∫_{0}^{3}\\f{y^{2} + 3}{4}dy + ∫_{3}^{6}(6 − y)dy = \\f{9}{2} + \\f{9}{2} = 9.'], 'area', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'area', 'The area of the region {(x, y) : x^{2} − 8x ≤ y ≤ −x} is:', ['\\f{343}{6}', '\\f{637}{6}', '\\f{437}{6}', '\\f{523}{6}'], 1,
    lambda: pick([343 / 6, 637 / 6, 437 / 6, 523 / 6], round(area(lambda x: x * x - 8 * x, lambda x: -x, 0, 7), 4), 1e-3),
    ['They meet where x^{2} − 7x = 0: x = 0 and 7.', '∫_{0}^{7}(7x − x^{2})dx = \\f{343}{2} − \\f{343}{3} = \\f{343}{6}.'], 'area', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'area', 'The area of the region R = {(x, y) : xy ≤ 8, 1 ≤ y ≤ x^{2}, x ≥ 0} is', ['\\f{1}{3}(49 log_{e}2 − 15)', '\\f{2}{3}(20 log_{e}2 + 9)', '\\f{2}{3}(24 log_{e}2 − 7)', '\\f{1}{3}(40 log_{e}2 + 27)'], 3,
    lambda: pick([(49 * LN(2) - 15) / 3, 2 / 3 * (20 * LN(2) + 9), 2 / 3 * (24 * LN(2) - 7), (40 * LN(2) + 27) / 3], round(area(lambda y: math.sqrt(y), lambda y: 8 / y, 1, 4), 5), 1e-3),
    ['Slice horizontally: √{y} ≤ x ≤ \\f{8}{y}, meeting at y = 4.', '∫_{1}^{4}(\\f{8}{y} − √{y})dy = 16 log 2 − \\f{14}{3} = \\f{2}{3}(24 log 2 − 7).'], 'area', 2)

# ---------------- definite integrals ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'def', '4∫_{0}^{1}(\\f{1}{√{3 + x^{2}} + √{1 + x^{2}}})dx − 3 log_{e}(√{3}) is equal to :', ['2 − √{2} + log_{e}(1 + √{2})', '2 − √{2} − log_{e}(1 + √{2})', '2 + √{2} − log_{e}(1 + √{2})', '2 + √{2} + log_{e}(1 + √{2})'], 2,
    lambda: (lambda v: pick([2 - S2 + LN(1 + S2), 2 - S2 - LN(1 + S2), 2 + S2 - LN(1 + S2), 2 + S2 + LN(1 + S2)], round(v, 6), 1e-5))(4 * integ(lambda x: 1 / (math.sqrt(3 + x * x) + math.sqrt(1 + x * x)), 0, 1) - 3 * LN(S3)),
    ['Rationalise: \\f{1}{√{3 + x^{2}} + √{1 + x^{2}}} = \\f{√{3 + x^{2}} − √{1 + x^{2}}}{2}.', 'Use ∫√{a^{2} + x^{2}} = \\f{x}{2}√{a^{2} + x^{2}} + \\f{a^{2}}{2} log(x + √{a^{2} + x^{2}}) → 2 − √{2} − log(1 + √{2}).'], 'def', 3)
add(('2025', 'Apr', '2025-04-04', 1), 'def', 'The value of ∫_{−1}^{1} \\f{(1 + √{|x| − x})e^{x} + (√{|x| − x})e^{−x}}{e^{x} + e^{−x}} dx is equal to', ['1 + \\f{2√{2}}{3}', '2 + \\f{2√{2}}{3}', '3 − \\f{2√{2}}{3}', '1 − \\f{2√{2}}{3}'], 1,
    lambda: pick([1 + 2 * S2 / 3, 2 + 2 * S2 / 3, 3 - 2 * S2 / 3, 1 - 2 * S2 / 3], round(integ(lambda x: ((1 + math.sqrt(abs(x) - x)) * math.exp(x) + math.sqrt(abs(x) - x) * math.exp(-x)) / (math.exp(x) + math.exp(-x)), -1, 1), 6), 1e-5),
    ['The integrand = √{|x| − x} + \\f{e^{x}}{e^{x} + e^{−x}}; the second part pairs with x → −x to give 1 on average → contributes 1.', '∫_{−1}^{0}√{−2x}dx = \\f{2√{2}}{3} → 1 + \\f{2√{2}}{3}.'], 'def', 3)
add(('2024', 'Apr', '2024-04-05', 1), 'def', 'The integral ∫_{0}^{π/4} \\f{136 sin x}{3 sin x + 5 cos x}dx is equal to :', ['3π − 50 log_{e}2 + 20 log_{e}5', '3π − 25 log_{e}2 + 10 log_{e}5', '3π − 10 log_{e}(2√{2}) + 10 log_{e}5', '3π − 30 log_{e}2 + 20 log_{e}5'], 1,
    lambda: pick([3 * PI - 50 * LN(2) + 20 * LN(5), 3 * PI - 25 * LN(2) + 10 * LN(5), 3 * PI - 10 * LN(2 * S2) + 10 * LN(5), 3 * PI - 30 * LN(2) + 20 * LN(5)], round(integ(lambda x: 136 * math.sin(x) / (3 * math.sin(x) + 5 * math.cos(x)), 0, PI / 4), 6), 1e-5),
    ['Write 136 sin x = A(3 sin x + 5 cos x) + B(3 cos x − 5 sin x): A = 12, B = −20.', '12 · \\f{π}{4} − 20 log \\f{8/√{2}}{5} = 3π − 50 log 2 + 20 log 5.'], 'def', 3)
add(('2024', 'Apr', '2024-04-05', 1), 'def', 'The value of ∫_{−π}^{π} \\f{2y(1 + sin y)}{1 + cos^{2}y}dy is :', ['π^{2}', '\\f{π^{2}}{2}', '\\f{π}{2}', '2π^{2}'], 1,
    lambda: pick([PI ** 2, PI ** 2 / 2, PI / 2, 2 * PI ** 2], round(integ(lambda y: 2 * y * (1 + math.sin(y)) / (1 + math.cos(y) ** 2), -PI, PI), 6), 1e-5),
    ['The 2y part is odd and vanishes; 2y sin y/(1 + cos^{2}y) is even → 4∫_{0}^{π}\\f{y sin y}{1 + cos^{2}y}dy.', 'With y → π − y: ∫_{0}^{π}\\f{y sin y}{1 + cos^{2}y} = \\f{π}{2}∫_{0}^{π}\\f{sin y}{1 + cos^{2}y} = \\f{π^{2}}{4} → π^{2}.'], 'def', 3)
add(('2024', 'Apr', '2024-04-06', 1), 'def', '∫_{0}^{π/4} \\f{cos^{2}x sin^{2}x}{(cos^{3}x + sin^{3}x)^{2}}dx is equal to ____.', ['\\f{1}{12}', '\\f{1}{9}', '\\f{1}{6}', '\\f{1}{3}'], 3,
    lambda: pick([1 / 12, 1 / 9, 1 / 6, 1 / 3], round(integ(lambda x: (math.cos(x) * math.sin(x)) ** 2 / (math.cos(x) ** 3 + math.sin(x) ** 3) ** 2, 0, PI / 4), 6), 1e-5),
    ['Divide by cos^{6}x: \\f{tan^{2}x sec^{2}x}{(1 + tan^{3}x)^{2}}; put t = 1 + tan^{3}x.', '\\f{1}{3}∫_{1}^{2}\\f{dt}{t^{2}} = \\f{1}{3} · \\f{1}{2} = \\f{1}{6}.'], 'def', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'def', 'The integral ∫_{0}^{π} \\f{(x + 3) sin x}{1 + 3 cos^{2}x}dx is equal to', ['\\f{π}{2√{3}}(π + 4)', '\\f{π}{√{3}}(π + 1)', '\\f{π}{√{3}}(π + 2)', '\\f{π}{3√{3}}(π + 6)'], 4,
    lambda: pick([PI / (2 * S3) * (PI + 4), PI / S3 * (PI + 1), PI / S3 * (PI + 2), PI / (3 * S3) * (PI + 6)], round(integ(lambda x: (x + 3) * math.sin(x) / (1 + 3 * math.cos(x) ** 2), 0, PI), 6), 1e-5),
    ['∫_{0}^{π}\\f{sin x}{1 + 3 cos^{2}x} = \\f{2}{√{3}} · \\f{π}{3}; the x-part equals \\f{π}{2} times it (x → π − x).', '(\\f{π}{2} + 3) · \\f{2π}{3√{3}} = \\f{π(π + 6)}{3√{3}}.'], 'def', 3)
add(('2024', 'Apr', '2024-04-09', 2), 'def', 'The integral ∫_{1/4}^{3/4} cos(2 cot^{−1}√{\\f{1 − x}{1 + x}})dx is equal to:', ['−\\f{1}{2}', '\\f{1}{4}', '\\f{1}{2}', '−\\f{1}{4}'], 4,
    lambda: pick([-0.5, 0.25, 0.5, -0.25], round(integ(lambda x: math.cos(2 * math.atan(1 / math.sqrt((1 - x) / (1 + x)))), 0.25, 0.75), 6), 1e-5),
    ['Put x = cos 2θ: √{\\f{1 − x}{1 + x}} = tan θ, so cot^{−1}(tan θ) = \\f{π}{2} − θ and the integrand is cos(π − 2θ) = −x.', '∫_{1/4}^{3/4}(−x)dx = −\\f{1}{4}.'], 'def', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'def', 'The value of the integral ∫_{−1}^{2} log_{e}(x + √{x^{2} + 1})dx is :', ['√{5} − √{2} + log_{e}(\\f{9 + 4√{5}}{1 + √{2}})', '√{2} − √{5} + log_{e}(\\f{9 + 4√{5}}{1 + √{2}})', '√{5} − √{2} + log_{e}(\\f{7 + 4√{5}}{1 + √{2}})', '√{2} − √{5} + log_{e}(\\f{7 + 4√{5}}{1 + √{2}})'], 2,
    lambda: (lambda S5: pick([S5 - S2 + LN((9 + 4 * S5) / (1 + S2)), S2 - S5 + LN((9 + 4 * S5) / (1 + S2)), S5 - S2 + LN((7 + 4 * S5) / (1 + S2)), S2 - S5 + LN((7 + 4 * S5) / (1 + S2))], round(integ(lambda x: math.asinh(x), -1, 2), 6), 1e-5))(math.sqrt(5)),
    ['By parts: ∫ sinh^{−1}x dx = x sinh^{−1}x − √{x^{2} + 1}.', 'From −1 to 2: 2 log(2 + √{5}) − √{5} − log(1 + √{2}) + √{2} = √{2} − √{5} + log \\f{9 + 4√{5}}{1 + √{2}}.'], 'def', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'def', 'If α = ∫_{0}^{2√{3}} log_{2}(x^{2} + 4)dx + ∫_{2}^{4}√{2^{x} − 4}dx, then α^{2} is equal to ____.', None, 192,
    lambda: round((integ(lambda x: math.log2(x * x + 4), 0, 2 * S3) + integ(lambda x: math.sqrt(2 ** x - 4), 2, 4)) ** 2, 3),
    ['The two functions are inverses: y = √{2^{x} − 4} ⇔ x = log_{2}(y^{2} + 4).', 'So the two areas fill a rectangle: α = 4 × 2√{3} − 2 × 0 = 8√{3} → α^{2} = 192.'], 'def', 3)
add(('2026', 'Jan', '2026-01-21', 1), 'def', 'The value of ∫_{−π/6}^{π/6}(\\f{π + 4x^{11}}{1 − sin(|x| + π/6)})dx is equal to:', ['2π', '4π', '8π', '6π'], 2,
    lambda: pick([2 * PI, 4 * PI, 8 * PI, 6 * PI], round(integ(lambda x: (PI + 4 * x ** 11) / (1 - math.sin(abs(x) + PI / 6)), -PI / 6, PI / 6), 6), 1e-5),
    ['The x^{11} part is odd → 0. The rest is even: 2π∫_{0}^{π/6}\\f{dx}{1 − sin(x + π/6)}.', '∫\\f{dt}{1 − sin t} = tan t + sec t; from \\f{π}{6} to \\f{π}{3}: (√{3} + 2) − (\\f{1}{√{3}} + \\f{2}{√{3}}) = 2 → 4π.'], 'def', 3)
add(('2026', 'Jan', '2026-01-21', 1), 'def', '6∫_{0}^{π}|(sin 3x + sin 2x + sin x)|dx is equal to ____.', None, 17,
    lambda: round(6 * integ(lambda x: abs(math.sin(3 * x) + math.sin(2 * x) + math.sin(x)), 0, PI), 4), ['sin 3x + sin 2x + sin x = sin 2x(2 cos x + 1): zero at \\f{π}{2} and \\f{2π}{3}.', 'Integrate piece by piece with the right signs: total \\f{17}{6} → 17.'], 'def', 3)
add(('2025', 'Jan', '2025-01-23', 1), 'def', 'The value of ∫_{e^{2}}^{e^{4}} \\f{1}{x}(\\f{e^{((log_{e}x)^{2} + 1)^{−1}}}{e^{((log_{e}x)^{2} + 1)^{−1}} + e^{((6 − log_{e}x)^{2} + 1)^{−1}}})dx is', ['1', 'e^{2}', 'log_{e}2', '2'], 1,
    lambda: pick([1, math.e ** 2, LN(2), 2], round(integ(lambda t: (lambda g: g(t) / (g(t) + g(6 - t)))(lambda u: math.exp(1 / (u * u + 1))), 2, 4), 6), 1e-5),
    ['Put t = log x: ∫_{2}^{4}\\f{g(t)}{g(t) + g(6 − t)}dt.', 't → 6 − t swaps the two terms, so twice the integral = ∫_{2}^{4}1 dt = 2 → answer 1.'], 'def', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'def', 'If I = ∫_{0}^{π/2}\\f{sin^{3/2}x}{sin^{3/2}x + cos^{3/2}x}dx, then ∫_{0}^{2I}\\f{x sin x cos x}{sin^{4}x + cos^{4}x}dx equals :', ['\\f{π^{2}}{16}', '\\f{π^{2}}{12}', '\\f{π^{2}}{4}', '\\f{π^{2}}{8}'], 1,
    lambda: (lambda I: pick([PI ** 2 / 16, PI ** 2 / 12, PI ** 2 / 4, PI ** 2 / 8], round(integ(lambda x: x * math.sin(x) * math.cos(x) / (math.sin(x) ** 4 + math.cos(x) ** 4), 0, 2 * I), 6), 1e-5))(integ(lambda x: math.sin(x) ** 1.5 / (math.sin(x) ** 1.5 + math.cos(x) ** 1.5), 0, PI / 2)),
    ['I = \\f{π}{4} (x → \\f{π}{2} − x). So the upper limit is \\f{π}{2}.', 'Same trick: \\f{π}{4}∫_{0}^{π/2}\\f{sin x cos x}{sin^{4}x + cos^{4}x}dx = \\f{π}{4} · \\f{π}{4} = \\f{π^{2}}{16}.'], 'def', 3)
add(('2025', 'Jan', '2025-01-24', 1), 'def', 'If I(m, n) = ∫_{0}^{1}x^{m−1}(1 − x)^{n−1}dx, m, n > 0, then I(9, 14) + I(10, 13) is', ['I(1, 13)', 'I(9, 1)', 'I(19, 27)', 'I(9, 13)'], 4,
    lambda: (lambda I: pick([I(1, 13), I(9, 1), I(19, 27), I(9, 13)], I(9, 14) + I(10, 13)))(lambda m, n: F(math.factorial(m - 1) * math.factorial(n - 1), math.factorial(m + n - 1))),
    ['Add the integrands: x^{8}(1 − x)^{12}[(1 − x) + x] = x^{8}(1 − x)^{12}.', 'That is I(9, 13).'], 'def', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'def', 'The value of the integral ∫_{0}^{∞}\\f{log_{e}(x)}{x^{2} + 4}dx is:', ['\\f{π log_{e}(2)}{2}', '\\f{π log_{e}(2)}{4}', '1 + π log_{e}(2)', '2 + π log_{e}(2)'], 2,
    lambda: pick([PI * LN(2) / 2, PI * LN(2) / 4, 1 + PI * LN(2), 2 + PI * LN(2)], round(integ(lambda t: LN(2 * math.tan(t)) / 2, 0, PI / 2, 400000), 5), 1e-3),   # x = 2 tan t
    ['Put x = \\f{4}{t}: the integral becomes ∫_{0}^{∞}\\f{log 4 − log t}{t^{2} + 4}dt, so 2I = log 4 · ∫_{0}^{∞}\\f{dt}{t^{2} + 4} = log 4 · \\f{π}{4}.', 'I = \\f{π log 2}{4}.'], 'def', 3)
add(('2026', 'Apr', '2026-04-05', 1), 'def', 'The value of the integral ∫_{π/6}^{π/3}(\\f{4 − cosec^{2}x}{cos^{4}x})dx is:', ['\\f{11}{√{3}}', '\\f{16}{√{3}}', '\\f{32}{3√{3}}', '\\f{64}{3√{3}}'], 3,
    lambda: pick([11 / S3, 16 / S3, 32 / (3 * S3), 64 / (3 * S3)], round(integ(lambda x: (4 - 1 / math.sin(x) ** 2) / math.cos(x) ** 4, PI / 6, PI / 3), 6), 1e-5),
    ['Put t = tan x: the integral becomes ∫(3t^{2} + 2 − \\f{1}{t^{2}})dt from \\f{1}{√{3}} to √{3}.', '[t^{3} + 2t + \\f{1}{t}] = \\f{16}{√{3}} − \\f{16}{3√{3}} = \\f{32}{3√{3}}.'], 'def', 3)
add(('2026', 'Apr', '2026-04-06', 1), 'def', 'The value of the integral ∫_{−π/4}^{π/4}(\\f{32 cos^{4}x}{1 + e^{sin x}})dx is:', ['4π + 2', '3π + 8', '3π + 4', '4π + 3'], 2,
    lambda: pick([4 * PI + 2, 3 * PI + 8, 3 * PI + 4, 4 * PI + 3], round(integ(lambda x: 32 * math.cos(x) ** 4 / (1 + math.exp(math.sin(x))), -PI / 4, PI / 4), 6), 1e-5),
    ['x → −x turns \\f{1}{1 + e^{sin x}} into \\f{e^{sin x}}{1 + e^{sin x}}: adding, 2I = ∫ 32 cos^{4}x dx.', 'I = ∫_{0}^{π/4} 32 cos^{4}x dx = 32(\\f{3π}{32} + \\f{1}{4}) = 3π + 8.'], 'def', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'def', 'The value of the integral ∫_{−1}^{1}(\\f{x^{3} + |x| + 1}{x^{2} + 2|x| + 1})dx is equal to:', ['3 log_{e}2', '2 log_{e}2', '5 log_{e}3', '3 log_{e}3'], 2,
    lambda: pick([3 * LN(2), 2 * LN(2), 5 * LN(3), 3 * LN(3)], round(integ(lambda x: (x ** 3 + abs(x) + 1) / (x * x + 2 * abs(x) + 1), -1, 1), 6), 1e-5),
    ['x^{3} part is odd → 0. The rest is even: 2∫_{0}^{1}\\f{x + 1}{(x + 1)^{2}}dx.', '2 log 2.'], 'def', 1)

# ---------------- greatest-integer integrals ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'gif', 'Let [.] denote the greatest integer function. If ∫_{0}^{e^{3}}[\\f{1}{e^{x−1}}]dx = α − log_{e}2, then α^{3} is equal to ____.', None, 8,
    lambda: round((integ(lambda x: math.floor(math.exp(1 - x)), 0, math.e ** 3, 400000) + LN(2)) ** 3, 2),
    ['[e^{1−x}] = 2 for x < 1 − log 2, 1 for x up to 1, 0 after.', 'Integral = 2(1 − log 2) + log 2 = 2 − log 2 → α = 2, α^{3} = 8.'], 'gif', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'gif', 'Let [·] denote the greatest integer function. Then the value of ∫_{0}^{3}(\\f{e^{x} + e^{−x}}{[x]!})dx is :', ['e^{2} + e^{3} − \\f{1}{e^{2}} − \\f{1}{e^{3}}', '\\f{1}{2}(e^{2} + e^{3} − \\f{1}{e^{2}} − \\f{1}{e^{3}})', 'e^{2} + e^{3} − \\f{1}{2e^{2}} − \\f{1}{2e^{3}}', '\\f{1}{2}(e^{2} + e^{3}) − \\f{1}{e^{2}} − \\f{1}{e^{3}}'], 2,
    lambda: (lambda E2, E3: pick([E2 + E3 - 1 / E2 - 1 / E3, 0.5 * (E2 + E3 - 1 / E2 - 1 / E3), E2 + E3 - 1 / (2 * E2) - 1 / (2 * E3), 0.5 * (E2 + E3) - 1 / E2 - 1 / E3], round(integ(lambda x: (math.exp(x) + math.exp(-x)) / math.factorial(math.floor(x)), 0, 3), 5), 1e-4))(math.e ** 2, math.e ** 3),
    ['On [0, 1) and [1, 2) divide by 1, on [2, 3) by 2. With F = e^{x} − e^{−x}:', 'F(2) − F(0) + \\f{F(3) − F(2)}{2} = \\f{1}{2}(e^{2} + e^{3} − e^{−2} − e^{−3}).'], 'gif', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'gif', 'Let [·] denote the greatest integer function. Then ∫_{−π/2}^{π/2}(\\f{12(3 + [x])}{3 + [sin x] + [cos x]})dx is equal to :', ['11π + 2', '12π + 5', '13π + 1', '15π + 4'], 1,
    lambda: pick([11 * PI + 2, 12 * PI + 5, 13 * PI + 1, 15 * PI + 4], round(integ(lambda x: 12 * (3 + math.floor(x)) / (3 + math.floor(math.sin(x)) + math.floor(math.cos(x))), -PI / 2, PI / 2, 400000), 4), 1e-4),
    ['Split at −1, 0, 1: [x] and [sin x], [cos x] are constant on each piece.', 'Adding the pieces gives 11π + 2.'], 'gif', 3)
add(('2025', 'Jan', '2025-01-29', 2), 'gif', 'If 24∫_{0}^{π/4}(sin|4x − \\f{π}{12}| + [2 sin x])dx = 2π + α, where [•] denotes the greatest integer function, then α is equal to ____.', None, 12,
    lambda: round(24 * integ(lambda x: math.sin(abs(4 * x - PI / 12)) + math.floor(2 * math.sin(x)), 0, PI / 4, 400000) - 2 * PI, 3),
    ['[2 sin x] = 1 from \\f{π}{6} to \\f{π}{4} → 24 · \\f{π}{12} = 2π.', '∫ sin|4x − \\f{π}{12}| = \\f{1}{4}(2 − cos \\f{π}{12} + cos \\f{π}{12}) = \\f{1}{2} → 24 × \\f{1}{2} = 12.'], 'gif', 3)
add(('2026', 'Apr', '2026-04-04', 1), 'gif', 'Let ∫_{−2}^{2}(|sin x| + [x sin x])dx = 2(3 − cos 2) + β, where [·] is the greatest integer function. Then β sin(\\f{β}{2}) equals:', ['1', '2', '4', '8'], 2,
    lambda: (lambda b: pick([1, 2, 4, 8], round(b * math.sin(b / 2), 3), 1e-3))(integ(lambda x: abs(math.sin(x)) + math.floor(x * math.sin(x)), -2, 2, 400000) - 2 * (3 - math.cos(2))),
    ['∫_{−2}^{2}|sin x| = 2(1 − cos 2). [x sin x] = 1 where x sin x ≥ 1, i.e. a ≤ |x| ≤ 2 with a sin a = 1, and 0 elsewhere → contributes 2(2 − a).', 'Total 2(3 − cos 2) − 2a → β = −2a and β sin \\f{β}{2} = 2a sin a = 2.'], 'gif', 3)
add(('2026', 'Jan', '2026-01-22', 1), 'gif', 'The value of ∫_{−π/2}^{π/2}(\\f{1}{[x] + 4})dx, where [·] denotes the greatest integer function, is', ['\\f{1}{60}(21π − 1)', '\\f{1}{60}(π − 7)', '\\f{7}{60}(3π − 1)', '\\f{7}{60}(π − 3)'], 3,
    lambda: pick([(21 * PI - 1) / 60, (PI - 7) / 60, 7 / 60 * (3 * PI - 1), 7 / 60 * (PI - 3)], round(integ(lambda x: 1 / (math.floor(x) + 4), -PI / 2, PI / 2, 400000), 5), 1e-4),
    ['[x] = −2, −1, 0, 1 on [−\\f{π}{2}, −1), [−1, 0), [0, 1), [1, \\f{π}{2}].', '\\f{π/2 − 1}{2} + \\f{1}{3} + \\f{1}{4} + \\f{π/2 − 1}{5} = \\f{7}{60}(3π − 1).'], 'gif', 2)

# ---------------- antiderivatives ----------------
add(('2024', 'Apr', '2024-04-04', 2), 'indef', 'If ∫cosec^{5}x dx = α cot x cosec x(cosec^{2}x + \\f{3}{2}) + β log_{e}|tan \\f{x}{2}| + C where α, β ∈ R and C is constant of integration then the value of 8(α + β) equals', None, 1,
    lambda: next(round(8 * (a + b)) for a in [F(k, 8) for k in range(-16, 17)] for b in [F(k, 8) for k in range(-16, 17)] if same_deriv(lambda x: float(a) / math.tan(x) / math.sin(x) * (1 / math.sin(x) ** 2 + 1.5) + float(b) * LN(abs(math.tan(x / 2))), lambda x: 1 / math.sin(x) ** 5, [0.4, 0.9, 1.3, 2.2])),
    ['Reduction: ∫cosec^{n} = −\\f{cot x cosec^{n−2}x}{n − 1} + \\f{n − 2}{n − 1}∫cosec^{n−2}.', '∫cosec^{5} = −\\f{1}{4}cot x cosec x(cosec^{2}x + \\f{3}{2}) + \\f{3}{8}log|tan \\f{x}{2}| → 8(−\\f{1}{4} + \\f{3}{8}) = 1.'], 'indef', 3)
add(('2024', 'Apr', '2024-04-08', 2), 'indef', 'If ∫\\f{1}{⁵√{(x − 1)^{4}(x + 3)^{6}}}dx = A(\\f{αx − 1}{βx + 3})^{B} + C, where C is the constant of integration, then the value of α + β + 20AB is', None, 7,
    lambda: (lambda A, al, be, B: round(al + be + 20 * A * B) if same_deriv(lambda x: A * ((al * x - 1) / (be * x + 3)) ** B, lambda x: 1 / ((x - 1) ** 4 * (x + 3) ** 6) ** 0.2, [1.5, 2.3, 4.0]) else None)(1.25, 1, 1, 0.2),
    ['Put t = \\f{x − 1}{x + 3}: dt = \\f{4}{(x + 3)^{2}}dx and the root becomes (x + 3)^{2}t^{4/5}.', '∫\\f{dt}{4t^{4/5}} = \\f{5}{4}t^{1/5} → A = \\f{5}{4}, α = β = 1, B = \\f{1}{5} → 2 + 5 = 7.'], 'indef', 3)
add(('2024', 'Apr', '2024-04-09', 1), 'indef', 'Let ∫\\f{2 − tan x}{3 + tan x}dx = \\f{1}{2}(αx + log_{e}|β sin x + γ cos x|) + C, where C is the constant of integration. Then α + \\f{γ}{β} is equal to :', ['3', '1', '4', '7'], 3,
    lambda: (lambda al, be, ga: pick([3, 1, 4, 7], al + ga / be) if same_deriv(lambda x: 0.5 * (al * x + LN(abs(be * math.sin(x) + ga * math.cos(x)))), lambda x: (2 - math.tan(x)) / (3 + math.tan(x)), [0.2, 0.7, 1.1]) else None)(1, 1, 3),
    ['Write 2 cos x − sin x = A(3 cos x + sin x) + B(cos x − 3 sin x): A = B = \\f{1}{2}.', 'Integral = \\f{1}{2}(x + log|sin x + 3 cos x|) → α = 1, β = 1, γ = 3 → 4.'], 'indef', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'indef', 'Let f(x) = ∫(\\f{16x + 24}{x^{2} + 2x − 15})dx. If f(4) = 14 log_{e}(3) and f(7) = log_{e}(2^{α} · 3^{β}), α, β ∈ N, then α + β is equal to :', ['31', '37', '39', '41'], 3,
    lambda: (lambda f: pick([31, 37, 39, 41], next(a + b for a in range(1, 60) for b in range(1, 60) if abs(a * LN(2) + b * LN(3) - f(7)) < 1e-9)))(lambda x: 9 * LN(abs(x - 3)) + 7 * LN(abs(x + 5)) + 14 * LN(3) - (9 * LN(1) + 7 * LN(9)) if same_deriv(lambda t: 9 * LN(abs(t - 3)) + 7 * LN(abs(t + 5)), lambda t: (16 * t + 24) / (t * t + 2 * t - 15), [4.5, 6.0, 8.0]) else None),
    ['\\f{16x + 24}{(x − 3)(x + 5)} = \\f{9}{x − 3} + \\f{7}{x + 5} → f = 9 log|x − 3| + 7 log|x + 5| + C; f(4) = 14 log 3 gives C = 0.', 'f(7) = 9 log 4 + 7 log 12 = log(2^{32} · 3^{7}) → 39.'], 'indef', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'indef', 'If ∫\\f{2x^{2} + 5x + 9}{√{x^{2} + x + 1}}dx = x√{x^{2} + x + 1} + α√{x^{2} + x + 1} + β log_{e}|x + \\f{1}{2} + √{x^{2} + x + 1}| + C, where C is the constant of integration, then α + 2β is equal to ____.', None, 16,
    lambda: next(round(a + 2 * b) for a in [k / 4 for k in range(-40, 41)] for b in [k / 4 for k in range(-40, 41)] if same_deriv(lambda x: (x + a) * math.sqrt(x * x + x + 1) + b * LN(abs(x + 0.5 + math.sqrt(x * x + x + 1))), lambda x: (2 * x * x + 5 * x + 9) / math.sqrt(x * x + x + 1), [-1.2, 0.3, 1.7])),
    ['2x^{2} + 5x + 9 = 2Q + \\f{3}{2}(2x + 1) + \\f{11}{2} with Q = x^{2} + x + 1.', '∫ = (x + \\f{1}{2})√{Q} + \\f{3}{4}log(…) + 3√{Q} + \\f{11}{2}log(…) → α = \\f{7}{2}, β = \\f{25}{4} → 16.'], 'indef', 3)
for _p in P: _p['t'] = _p['fam']
