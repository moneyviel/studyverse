"""Real JEE Main questions — Mathematics Unit 9: Differential Equations. Our own solutions; chk re-solves each one
independently with a fourth-order Runge–Kutta integration of the equation itself from the given condition (or, where
the equation is singular at the starting point, by integrating its separated form numerically), then reads off
the asked value. Skipped: an item whose options are cut in the scan, an item whose official key is "any
non-negative integer" and an item whose printed coefficients we could not read reliably."""
import math
from fractions import Fraction as F
from common import new_registry, pick, verify
P, add = new_registry()
def rk4(f, x0, y0, x1, n=4000):
    h = (x1 - x0) / n; x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y); k2 = f(x + h / 2, y + h * k1 / 2); k3 = f(x + h / 2, y + h * k2 / 2); k4 = f(x + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6; x += h
    return y
def integ(f, a, b, n=200000):
    h = (b - a) / n; return h * sum(f(a + (i + 0.5) * h) for i in range(n))
PI, S2, S3, E, LN = math.pi, math.sqrt(2), math.sqrt(3), math.e, math.log
sec = lambda x: 1 / math.cos(x)
def P4(opts, v, tol=1e-5): return pick(opts, round(v, 7), tol)

# ---------------- linear first-order equations ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'lin', 'Let y = y(x) be the solution of the differential equation \\f{dy}{dx} + 2y sec^{2}x = 2 sec^{2}x + 3 tan x · sec^{2}x such that y(0) = \\f{5}{4}. Then 12(y(\\f{π}{4}) − e^{−2}) is equal to ____.', None, 21,
    lambda: round(12 * (rk4(lambda x, y: 2 * sec(x) ** 2 + 3 * math.tan(x) * sec(x) ** 2 - 2 * y * sec(x) ** 2, 0, 1.25, PI / 4) - math.exp(-2)), 4),
    ['Put t = tan x: \\f{dy}{dt} + 2y = 2 + 3t; integrating factor e^{2t}.', 'y = \\f{1}{4} + \\f{3t}{2} + e^{−2t} (from y = \\f{5}{4} at t = 0); at t = 1: \\f{7}{4} + e^{−2} → 12 × \\f{7}{4} = 21.'], 'lin', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'lin', 'Let g be a differentiable function such that ∫_{0}^{x}g(t)dt = x − ∫_{0}^{x}tg(t)dt, x ≥ 0 and let y = y(x) satisfy the differential equation \\f{dy}{dx} − y tan x = 2(x + 1) sec x g(x), x ∈ [0, \\f{π}{2}). If y(0) = 0, then y(\\f{π}{3}) is equal to', ['\\f{2π}{3}', '\\f{4π}{3}', '\\f{2π}{3√{3}}', '\\f{4π}{3√{3}}'], 2,
    lambda: P4([2 * PI / 3, 4 * PI / 3, 2 * PI / (3 * S3), 4 * PI / (3 * S3)], rk4(lambda x, y: y * math.tan(x) + 2 * (x + 1) * sec(x) / (1 + x), 0, 0, PI / 3)),
    ['Differentiate: g(x) = 1 − xg(x) → g(x) = \\f{1}{1 + x}. The equation becomes y\' − y tan x = 2 sec x.', '(y cos x)\' = 2 → y cos x = 2x → y(\\f{π}{3}) = \\f{2π/3}{1/2} = \\f{4π}{3}.'], 'lin', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'lin', 'Let y = y(x) be the solution of the differential equation \\f{dy}{dx} + 3(tan^{2}x)y + 3y = sec^{2}x, y(0) = \\f{1}{3} + e^{3}. Then y(\\f{π}{4}) is equal to', ['\\f{2}{3}', '\\f{4}{3} + e^{3}', '\\f{4}{3}', '\\f{2}{3} + e^{3}'], 3,
    lambda: P4([2 / 3, 4 / 3 + E ** 3, 4 / 3, 2 / 3 + E ** 3], rk4(lambda x, y: sec(x) ** 2 - 3 * y * sec(x) ** 2, 0, 1 / 3 + E ** 3, PI / 4)),
    ['3 tan^{2}x + 3 = 3 sec^{2}x: y\' + 3y sec^{2}x = sec^{2}x. In t = tan x: \\f{dy}{dt} + 3y = 1.', 'y = \\f{1}{3} + Ce^{−3t}, C = e^{3} → at t = 1: \\f{1}{3} + 1 = \\f{4}{3}.'], 'lin', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'lin', 'Let y = y(x) be the solution of the differential equation (x^{2} + 4)^{2}dy + (2x^{3}y + 8xy − 2)dx = 0. If y(0) = 0, then y(2) is equal to', ['\\f{π}{8}', '\\f{π}{16}', '2π', '\\f{π}{32}'], 4,
    lambda: P4([PI / 8, PI / 16, 2 * PI, PI / 32], rk4(lambda x, y: -(2 * x * y * (x * x + 4) - 2) / (x * x + 4) ** 2, 0, 0, 2)),
    ['Divide: y\' + \\f{2x}{x^{2} + 4}y = \\f{2}{(x^{2} + 4)^{2}}; integrating factor x^{2} + 4.', '((x^{2} + 4)y)\' = \\f{2}{x^{2} + 4} → (x^{2} + 4)y = tan^{−1}\\f{x}{2} → y(2) = \\f{π/4}{8} = \\f{π}{32}.'], 'lin', 2)
add(('2024', 'Apr', '2024-04-04', 1), 'lin', 'Let the solution y = y(x) of the differential equation \\f{dy}{dx} − y = 1 + 4 sin x satisfy y(π) = 1. Then y(\\f{π}{2}) + 10 is equal to ____.', None, 7,
    lambda: round(rk4(lambda x, y: y + 1 + 4 * math.sin(x), PI, 1, PI / 2) + 10, 4),
    ['Integrating factor e^{−x}: y = −1 − 2(sin x + cos x) + Ce^{x}.', 'y(π) = 1 + Ce^{π} = 1 → C = 0. y(\\f{π}{2}) = −3 → −3 + 10 = 7.'], 'lin', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'lin', 'Let y = y(x) be the solution of the differential equation \\f{dy}{dx} + \\f{2x}{(1 + x^{2})^{2}}y = xe^{\\f{1}{1 + x^{2}}}; y(0) = 0. Then the area enclosed by the curve f(x) = y(x)e^{−\\f{1}{1 + x^{2}}} and the line y − x = 4 is ____.', None, 18,
    lambda: (lambda f: round(integ(lambda x: max(0.0, x + 4 - f(x)), -3, 5, 4000), 3))(lambda x: rk4(lambda t, y: t * math.exp(1 / (1 + t * t)) - 2 * t / (1 + t * t) ** 2 * y, 0, 0, x, 200) * math.exp(-1 / (1 + x * x))),
    ['Integrating factor e^{∫2x/(1 + x^{2})^{2}} = e^{−1/(1 + x^{2})}: (ye^{−1/(1 + x^{2})})\' = x → f(x) = \\f{x^{2}}{2}.', 'y = \\f{x^{2}}{2} and y = x + 4 meet at x = −2, 4: area = \\f{1}{2} · \\f{6^{3}}{6} = 18.'], 'lin', 3)
add(('2024', 'Apr', '2024-04-05', 1), 'lin', 'If y = y(x) is the solution of the differential equation \\f{dy}{dx} + 2y = sin(2x), y(0) = \\f{3}{4}, then y(\\f{π}{8}) is equal to :', ['e^{−π/8}', 'e^{−π/4}', 'e^{π/4}', 'e^{π/8}'], 2,
    lambda: P4([math.exp(-PI / 8), math.exp(-PI / 4), math.exp(PI / 4), math.exp(PI / 8)], rk4(lambda x, y: math.sin(2 * x) - 2 * y, 0, 0.75, PI / 8)),
    ['y = \\f{sin 2x − cos 2x}{4} + Ce^{−2x}; y(0) = \\f{3}{4} → C = 1.', 'At \\f{π}{8}: sin \\f{π}{4} = cos \\f{π}{4}, so y = e^{−π/4}.'], 'lin', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'lin', 'Let y = y(x) be the solution of the differential equation (1 + x^{2})\\f{dy}{dx} + y = e^{tan^{−1}x}, y(1) = 0. Then y(0) is', ['\\f{1}{4}(e^{π/2} − 1)', '\\f{1}{2}(1 − e^{π/2})', '\\f{1}{4}(1 − e^{π/2})', '\\f{1}{2}(e^{π/2} − 1)'], 2,
    lambda: P4([(math.exp(PI / 2) - 1) / 4, (1 - math.exp(PI / 2)) / 2, (1 - math.exp(PI / 2)) / 4, (math.exp(PI / 2) - 1) / 2], rk4(lambda x, y: (math.exp(math.atan(x)) - y) / (1 + x * x), 1, 0, 0)),
    ['Integrating factor e^{tan^{−1}x}: (ye^{tan^{−1}x})\' = \\f{e^{2tan^{−1}x}}{1 + x^{2}} → ye^{t} = \\f{e^{2t}}{2} + C (t = tan^{−1}x).', 'y(1) = 0: C = −\\f{e^{π/2}}{2}. At x = 0: y = \\f{1}{2} − \\f{e^{π/2}}{2}.'], 'lin', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'lin', 'Let y = y(x) be the solution of the differential equation (2x log_{e}x)\\f{dy}{dx} + 2y = \\f{3}{x}log_{e}x, x > 0 and y(e^{−1}) = 0. Then, y(e) is equal to ____.', ['−\\f{3}{2e}', '−\\f{2}{3e}', '−\\f{3}{e}', '−\\f{2}{e}'], 3,
    lambda: (lambda Y: P4([-3 / (2 * E), -2 / (3 * E), -3 / E, -2 / E], Y(E)) if all(abs(2 * x * LN(x) * (Y(x + 1e-6) - Y(x - 1e-6)) / 2e-6 + 2 * Y(x) - 3 / x * LN(x)) < 1e-5 for x in (0.5, 1.7, 2.4)) and abs(Y(1 / E)) < 1e-12 else None)(lambda x: -1.5 * (LN(x) + 1) / (x * LN(x))),
    ['Divide by 2x log x: y\' + \\f{y}{x log x} = \\f{3}{2x^{2}}; integrating factor log x.', '(y log x)\' = \\f{3 log x}{2x^{2}} → y log x = −\\f{3}{2}·\\f{log x + 1}{x} (the constant is 0 from y(e^{−1}) = 0) → y(e) = −\\f{3}{e}.'], 'lin', 3)
add(('2025', 'Apr', '2025-04-07', 2), 'lin', 'Let y = y(x) be the solution of the differential equation (x^{2} + 1)y\' − 2xy = (x^{4} + 2x^{2} + 1)cos x, y(0) = 1. Then ∫_{−3}^{3}y(x)dx is :', ['24', '30', '18', '36'], 1,
    lambda: P4([24, 30, 18, 36], integ(lambda x: rk4(lambda t, y: (2 * t * y + (t * t + 1) ** 2 * math.cos(t)) / (t * t + 1), 0, 1, x, 300), -3, 3, 600), 1e-4),
    ['(\\f{y}{x^{2} + 1})\' = cos x → y = (x^{2} + 1)(sin x + 1).', 'The (x^{2} + 1)sin x part is odd: ∫_{−3}^{3}(x^{2} + 1)dx = 18 + 6 = 24.'], 'lin', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'lin', 'Let y = y(x) be the solution of the differential equation x\\f{dy}{dx} − y = x^{2} cot x, x ∈ (0, π). If y(\\f{π}{2}) = \\f{π}{2}, then 6y(\\f{π}{6}) − 8y(\\f{π}{4}) is equal to :', ['3π', 'π', '−3π', '−π'], 4,
    lambda: (lambda y: P4([3 * PI, PI, -3 * PI, -PI], 6 * y(PI / 6) - 8 * y(PI / 4)))(lambda x: rk4(lambda t, u: (u + t * t / math.tan(t)) / t, PI / 2, PI / 2, x)),
    ['(\\f{y}{x})\' = cot x → \\f{y}{x} = log sin x + C; y(\\f{π}{2}) = \\f{π}{2} gives C = 1.', '6 · \\f{π}{6}(1 − log 2) − 8 · \\f{π}{4}(1 − \\f{1}{2}log 2) = −π.'], 'lin', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'lin', 'Let y = y(x) be the solution of the differential equation sec x \\f{dy}{dx} − 2y = 2 + 3 sin x, x ∈ (−\\f{π}{2}, \\f{π}{2}), y(0) = −\\f{7}{4}. Then y(\\f{π}{6}) is equal to:', ['−\\f{5}{2}', '−\\f{5}{4}', '−3√{3} − 7', '−3√{2} − 7'], 1,
    lambda: P4([-2.5, -1.25, -3 * S3 - 7, -3 * S2 - 7], rk4(lambda x, y: (2 + 3 * math.sin(x) + 2 * y) * math.cos(x), 0, -1.75, PI / 6)),
    ['In t = sin x: \\f{dy}{dt} − 2y = 2 + 3t → y = −1 − \\f{3t}{2} − \\f{3}{4} + Ce^{2t}.', 'y(0) = −\\f{7}{4} gives C = 0; at t = \\f{1}{2}: −\\f{7}{4} − \\f{3}{4} = −\\f{5}{2}.'], 'lin', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'lin', 'Let x = x(y) be the solution of the differential equation y^{2}dx + (x − \\f{1}{y})dy = 0. If x(1) = 1, then x(\\f{1}{2}) is :', ['3 − e', '3 + e', '\\f{3}{2} + e', '\\f{1}{2} + e'], 1,
    lambda: P4([3 - E, 3 + E, 1.5 + E, 0.5 + E], rk4(lambda y, x: -(x - 1 / y) / (y * y), 1, 1, 0.5)),
    ['Linear in x: \\f{dx}{dy} + \\f{x}{y^{2}} = \\f{1}{y^{3}}; integrating factor e^{−1/y}.', 'x = 1 + \\f{1}{y} + Ce^{1/y}; x(1) = 1 → C = −\\f{1}{e}. x(\\f{1}{2}) = 3 − e.'], 'lin', 3)
add(('2025', 'Jan', '2025-01-22', 2), 'lin', 'If x = f(y) is the solution of the differential equation (1 + y^{2}) + (x − 2e^{tan^{−1}y})\\f{dy}{dx} = 0, y ∈ (−\\f{π}{2}, \\f{π}{2}) with f(0) = 1, then f(\\f{1}{√{3}}) is equal to :', ['e^{π/12}', 'e^{π/6}', 'e^{π/3}', 'e^{π/4}'], 2,
    lambda: P4([math.exp(PI / 12), math.exp(PI / 6), math.exp(PI / 3), math.exp(PI / 4)], rk4(lambda y, x: -(x - 2 * math.exp(math.atan(y))) / (1 + y * y), 0, 1, 1 / S3)),
    ['Linear in x: \\f{dx}{dy} + \\f{x}{1 + y^{2}} = \\f{2e^{tan^{−1}y}}{1 + y^{2}} → xe^{t} = e^{2t} + C (t = tan^{−1}y).', 'f(0) = 1 gives C = 0 → x = e^{t}; at y = \\f{1}{√{3}}: e^{π/6}.'], 'lin', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'lin', 'Let y = f(x) be the solution of the differential equation \\f{dy}{dx} + \\f{xy}{x^{2} − 1} = \\f{x^{6} + 4x}{√{1 − x^{2}}}, −1 < x < 1 such that f(0) = 0. If 6∫_{−1/2}^{1/2}f(x)dx = 2π − α then α^{2} is equal to ____.', None, 27,
    lambda: round((2 * PI - 6 * integ(lambda x: rk4(lambda t, y: (t ** 6 + 4 * t) / math.sqrt(1 - t * t) - t * y / (t * t - 1), 0, 0, x, 300), -0.5, 0.5, 600)) ** 2, 3),
    ['Integrating factor √{1 − x^{2}}: (y√{1 − x^{2}})\' = x^{6} + 4x → y = \\f{x^{7}/7 + 2x^{2}}{√{1 − x^{2}}}.', 'The odd part integrates to 0: 6∫_{−1/2}^{1/2}\\f{2x^{2}}{√{1 − x^{2}}}dx = 2π − 3√{3} → α^{2} = 27.'], 'lin', 3)
add(('2025', 'Jan', '2025-01-24', 1), 'lin', 'Let y = y(x) be the solution of the differential equation (xy − 5x^{2}√{1 + x^{2}})dx + (1 + x^{2})dy = 0, y(0) = 0. Then y(√{3}) is equal to', ['\\f{5√{3}}{2}', '√{\\f{14}{3}}', '√{\\f{15}{2}}', '2√{2}'], 1,
    lambda: P4([5 * S3 / 2, math.sqrt(14 / 3), math.sqrt(7.5), 2 * S2], rk4(lambda x, y: -(x * y - 5 * x * x * math.sqrt(1 + x * x)) / (1 + x * x), 0, 0, S3)),
    ['y\' + \\f{x}{1 + x^{2}}y = \\f{5x^{2}}{√{1 + x^{2}}}; integrating factor √{1 + x^{2}}.', '(y√{1 + x^{2}})\' = 5x^{2} → y = \\f{5x^{3}}{3√{1 + x^{2}}} → at √{3}: \\f{5 · 3√{3}}{3 · 2} = \\f{5√{3}}{2}.'], 'lin', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'lin', 'Let y = y(x) be the solution of the differential equation 2 cos x\\f{dy}{dx} = sin 2x − 4y sin x, x ∈ (0, \\f{π}{2}). If y(\\f{π}{3}) = 0, then y\'(\\f{π}{4}) + y(\\f{π}{4}) is equal to ____.', None, 1,
    lambda: (lambda Y: round((math.sin(PI / 4) - 2 * Y * math.tan(PI / 4)) + Y, 4))(rk4(lambda x, y: math.sin(x) - 2 * y * math.tan(x), PI / 3, 0, PI / 4)),
    ['y\' + 2y tan x = sin x; integrating factor sec^{2}x: (y sec^{2}x)\' = sin x sec^{2}x → y sec^{2}x = sec x + C.', 'y(\\f{π}{3}) = 0 → C = −2: y = cos x − 2cos^{2}x. At \\f{π}{4}: y = \\f{1}{√{2}} − 1, y\' = −\\f{1}{√{2}} + 2 → sum 1.'], 'lin', 3)
add(('2025', 'Jan', '2025-01-29', 1), 'lin', 'Let y = y(x) be the solution of the differential equation cos x(log_{e}(cos x))^{2}dy + (sin x − 3y sin x log_{e}(cos x))dx = 0, x ∈ (0, \\f{π}{2}). If y(\\f{π}{4}) = \\f{−1}{log_{e}2}, then y(\\f{π}{6}) is equal to:', ['\\f{1}{log_{e}(4) − log_{e}(3)}', '\\f{1}{log_{e}(3) − log_{e}(4)}', '\\f{2}{log_{e}(3) − log_{e}(4)}', '−\\f{1}{log_{e}(4)}'], 2,
    lambda: P4([1 / (LN(4) - LN(3)), 1 / (LN(3) - LN(4)), 2 / (LN(3) - LN(4)), -1 / LN(4)], rk4(lambda x, y: -(math.sin(x) - 3 * y * math.sin(x) * LN(math.cos(x))) / (math.cos(x) * LN(math.cos(x)) ** 2), PI / 4, -1 / LN(2), PI / 6)),
    ['Put u = log cos x (du = −tan x dx): u^{2}\\f{dy}{du} = 1 − 3yu, i.e. \\f{dy}{du} + \\f{3y}{u} = \\f{1}{u^{2}} → yu^{3} = \\f{u^{2}}{2} + C.', 'At \\f{π}{4}, u = −\\f{1}{2}log 2 gives C = 0 → y = \\f{1}{2u}; at \\f{π}{6}, u = \\f{1}{2}log \\f{3}{4} → y = \\f{1}{log 3 − log 4}.'], 'lin', 3)
add(('2025', 'Jan', '2025-01-29', 2), 'lin', 'If for the solution curve y = f(x) of the differential equation \\f{dy}{dx} + (tan x)y = \\f{2 + sec x}{(1 + 2 sec x)^{2}}, x ∈ (−\\f{π}{2}, \\f{π}{2}), f(\\f{π}{3}) = \\f{√{3}}{10}, then f(\\f{π}{4}) is equal to :', ['\\f{√{3} + 1}{10(4 + √{3})}', '\\f{9√{3} + 3}{10(4 + √{3})}', '\\f{5 − √{3}}{2√{2}}', '\\f{4 − √{2}}{14}'], 4,
    lambda: P4([(S3 + 1) / (10 * (4 + S3)), (9 * S3 + 3) / (10 * (4 + S3)), (5 - S3) / (2 * S2), (4 - S2) / 14], rk4(lambda x, y: (2 + sec(x)) / (1 + 2 * sec(x)) ** 2 - math.tan(x) * y, PI / 3, S3 / 10, PI / 4)),
    ['Integrating factor sec x: (y sec x)\' = \\f{sec x(2 + sec x)}{(1 + 2 sec x)^{2}} = \\f{1 + 2 cos x}{(cos x + 2)^{2}} → y sec x = \\f{sin x}{cos x + 2} + C.', 'f(\\f{π}{3}) gives C = 0 → y = \\f{sin x cos x}{cos x + 2}; at \\f{π}{4}: \\f{1/2}{2 + 1/√{2}} = \\f{4 − √{2}}{14}.'], 'lin', 3)
add(('2026', 'Apr', '2026-04-04', 2), 'lin', 'Let y = y(x) be the solution of the differential equation: \\f{dy}{dx} + (\\f{6x^{2} + (3x^{2} + 2x^{3} + 4)e^{−2x}}{(x^{3} + 2)(2 + e^{−2x})})y = 2 + e^{−2x}, x ∈ (−1, 2), satisfying y(0) = \\f{3}{2}. If y(1) = α(2 + e^{−2}), then α is equal to:', ['\\f{13}{8}', '\\f{6}{13}', '\\f{12}{13}', '\\f{13}{12}'], 4,
    lambda: P4([13 / 8, 6 / 13, 12 / 13, 13 / 12], rk4(lambda x, y: 2 + math.exp(-2 * x) - (6 * x * x + (3 * x * x + 2 * x ** 3 + 4) * math.exp(-2 * x)) / ((x ** 3 + 2) * (2 + math.exp(-2 * x))) * y, 0, 1.5, 1) / (2 + math.exp(-2))),
    ['The coefficient is \\f{d}{dx}log\\f{x^{3} + 2}{2 + e^{−2x}}, so the integrating factor is \\f{x^{3} + 2}{2 + e^{−2x}} and (IF · y)\' = x^{3} + 2.', 'IF · y = \\f{x^{4}}{4} + 2x + 1 (y(0) = \\f{3}{2}); at x = 1: \\f{3y}{2 + e^{−2}} = \\f{13}{4} → α = \\f{13}{12}.'], 'lin', 3)
add(('2026', 'Jan', '2026-01-23', 1), 'lin', 'Let y = y(x) be the solution of the differential equation x^{4}dy + (4x^{3}y + 2 sin x)dx = 0, x > 0, y(\\f{π}{2}) = 0. Then π^{4}y(\\f{π}{3}) is equal to :', ['81', '92', '64', '72'], 1,
    lambda: P4([81, 92, 64, 72], PI ** 4 * rk4(lambda x, y: -(4 * x ** 3 * y + 2 * math.sin(x)) / x ** 4, PI / 2, 0, PI / 3)),
    ['(x^{4}y)\' = −2 sin x → x^{4}y = 2 cos x + C; y(\\f{π}{2}) = 0 → C = 0.', 'At \\f{π}{3}: \\f{π^{4}}{81}y = 1 → π^{4}y = 81.'], 'lin', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'lin', 'If the solution curve y = f(x) of the differential equation (x^{2} − 4)y\' − 2xy + 2x(4 − x^{2})^{2} = 0, x > 2, passes through the point (3, 15), then the local maximum value of f is ____.', None, 16,
    lambda: round(max(rk4(lambda x, y: (2 * x * y - 2 * x * (4 - x * x) ** 2) / (x * x - 4), 3, 15, s, 800) for s in [2.5 + k * 0.001 for k in range(0, 1501, 1)][::25] + [math.sqrt(8)]), 3),
    ['(\\f{y}{x^{2} − 4})\' = −2x → y = (x^{2} − 4)(12 − x^{2}) (from the point (3, 15)).', 'With u = x^{2}: (u − 4)(12 − u) is largest at u = 8 → 4 × 4 = 16.'], 'lin', 3)

# ---------------- separable, exact and homogeneous equations ----------------
add(('2025', 'Apr', '2025-04-04', 2), 'sep', 'If a curve y = y(x) passes through the point (1, \\f{π}{2}) and satisfies the differential equation (7x^{4} cot y − e^{x} cosec y)\\f{dx}{dy} = x^{5}, x ≥ 1, then at x = 2, the value of cos y is :', ['\\f{2e^{2} − e}{128}', '\\f{2e^{2} − e}{64}', '\\f{2e^{2} + e}{128}', '\\f{2e^{2} + e}{64}'], 1,
    lambda: P4([(2 * E ** 2 - E) / 128, (2 * E ** 2 - E) / 64, (2 * E ** 2 + E) / 128, (2 * E ** 2 + E) / 64], math.cos(rk4(lambda x, y: (7 * x ** 4 / math.tan(y) - math.exp(x) / math.sin(y)) / x ** 5, 1, PI / 2, 2))),
    ['Multiply by sin y: with u = cos y, \\f{du}{dx} = −sin y\\f{dy}{dx} gives \\f{du}{dx} + \\f{7u}{x} = \\f{e^{x}}{x^{5}} — linear.', 'x^{7}u = ∫x^{2}e^{x}dx = e^{x}(x^{2} − 2x + 2) − e (u = 0 at x = 1) → at x = 2: 128u = 2e^{2} − e.'], 'sep', 3)
add(('2024', 'Apr', '2024-04-04', 2), 'sep', 'Let y = y(x) be the solution of the differential equation (x + y + 2)^{2}dx = dy, y(0) = −2. Let the maximum and minimum values of the function y = y(x) in [0, \\f{π}{3}] be α and β, respectively. If (3α + π)^{2} + β^{2} = γ + δ√{3}, γ, δ ∈ Z, then γ + δ equals ____.', None, 31,
    lambda: (lambda ys: (lambda a, b: next(g + d for g in range(-200, 201) for d in range(-100, 101) if abs(g + d * S3 - ((3 * a + PI) ** 2 + b * b)) < 1e-6))(max(ys), min(ys)))([rk4(lambda x, y: (x + y + 2) ** 2, 0, -2, t, 400) for t in [k * PI / 300 for k in range(1, 101)]] + [-2]),
    ['u = x + y + 2: u\' = 1 + u^{2}, u(0) = 0 → u = tan x → y = tan x − x − 2 (increasing).', 'α = √{3} − \\f{π}{3} − 2, β = −2: (3√{3} − 6)^{2} + 4 = 67 − 36√{3} → 31.'], 'sep', 3)
add(('2024', 'Apr', '2024-04-04', 1), 'sep', 'If the solution y = y(x) of the differential equation (x^{4} + 2x^{3} + 3x^{2} + 2x + 2)dy − (2x^{2} + 2x + 3)dx = 0 satisfies y(−1) = −\\f{π}{4}, then y(0) is equal to :', ['−\\f{π}{12}', '0', '\\f{π}{4}', '\\f{π}{2}'], 3,
    lambda: P4([-PI / 12, 0, PI / 4, PI / 2], rk4(lambda x, y: (2 * x * x + 2 * x + 3) / (x ** 4 + 2 * x ** 3 + 3 * x * x + 2 * x + 2), -1, -PI / 4, 0)),
    ['x^{4} + 2x^{3} + 3x^{2} + 2x + 2 = (x^{2} + 1)(x^{2} + 2x + 2) and \\f{2x^{2} + 2x + 3}{(x^{2} + 1)(x^{2} + 2x + 2)} = \\f{1}{x^{2} + 1} + \\f{1}{(x + 1)^{2} + 1}.', 'y = tan^{−1}x + tan^{−1}(x + 1) + C; y(−1) = −\\f{π}{4} gives C = 0 → y(0) = \\f{π}{4}.'], 'sep', 3)
add(('2024', 'Apr', '2024-04-06', 2), 'sep', 'If the solution y(x) of the given differential equation (e^{y} + 1)cos x dx + e^{y} sin x dy = 0 passes through the point (\\f{π}{2}, 0), then the value of e^{y(π/6)} is equal to ____.', None, 3,
    lambda: round(math.exp(rk4(lambda x, y: -(math.exp(y) + 1) * math.cos(x) / (math.exp(y) * math.sin(x)), PI / 2, 0, PI / 6)), 4),
    ['The left side is d[(e^{y} + 1) sin x] = 0 → (e^{y} + 1) sin x = 2.', 'At \\f{π}{6}: e^{y} + 1 = 4 → e^{y} = 3.'], 'sep', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'sep', 'Let y = y(x) be the solution curve of the differential equation sec y\\f{dy}{dx} + 2x sin y = x^{3} cos y, y(1) = 0. Then y(√{3}) is equal to :', ['\\f{π}{3}', '\\f{π}{6}', '\\f{π}{4}', '\\f{π}{12}'], 3,
    lambda: P4([PI / 3, PI / 6, PI / 4, PI / 12], rk4(lambda x, y: (x ** 3 * math.cos(y) - 2 * x * math.sin(y)) * math.cos(y), 1, 0, S3)),
    ['Divide by cos y: sec^{2}y y\' + 2x tan y = x^{3}; with t = tan y this is linear: t\' + 2xt = x^{3}.', 't = \\f{x^{2} − 1}{2} (t = 0 at x = 1) → at √{3}: tan y = 1 → y = \\f{π}{4}.'], 'sep', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'sep', 'Let α|x| = |y|e^{xy − β}, α, β ∈ N be the solution of the differential equation xdy − ydx + xy(xdy + ydx) = 0, y(1) = 2. Then α + β is equal to', None, 4,
    lambda: (lambda pts: next(a + b for a in range(1, 10) for b in range(1, 10) if all(abs(a * abs(x) - abs(y) * math.exp(x * y - b)) < 1e-6 * max(1, a * abs(x)) for x, y in pts)))([(x, rk4(lambda t, u: -u * (1 + t * u) / (t * (1 + t * u) - 2 * t * t * u) if False else u * (1 - t * u) / (t * (1 + t * u)), 1, 2, x)) for x in (1.2, 1.5, 0.8)]),
    ['Divide by xy: d(log\\f{y}{x}) + d(xy) = 0 → log|\\f{y}{x}| + xy = log 2 + 2.', '|y| = 2|x|e^{2 − xy}, i.e. 2|x| = |y|e^{xy − 2} → α = 2, β = 2 → 4.'], 'sep', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'sep', 'Let y = y(x) be the solution of the differential equation (1 + y^{2})e^{tan x}dx + cos^{2}x(1 + e^{2 tan x})dy = 0, y(0) = 1. Then y(\\f{π}{4}) is equal to :', ['\\f{2}{e}', '\\f{1}{e^{2}}', '\\f{1}{e}', '\\f{2}{e^{2}}'], 3,
    lambda: P4([2 / E, 1 / E ** 2, 1 / E, 2 / E ** 2], rk4(lambda x, y: -(1 + y * y) * math.exp(math.tan(x)) / (math.cos(x) ** 2 * (1 + math.exp(2 * math.tan(x)))), 0, 1, PI / 4)),
    ['Separate: \\f{dy}{1 + y^{2}} = −\\f{e^{tan x}sec^{2}x}{1 + e^{2 tan x}}dx → tan^{−1}y = −tan^{−1}e^{tan x} + C, C = \\f{π}{2}.', 'So y = e^{−tan x} → y(\\f{π}{4}) = \\f{1}{e}.'], 'sep', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'sep', 'The solution curve, of the differential equation 2y\\f{dy}{dx} + 3 = 5\\f{dy}{dx}, passing through the point (0, 1) is a conic, whose vertex lies on the line :', ['2x + 3y = 9', '2x + 3y = −9', '2x + 3y = −6', '2x + 3y = 6'], 1,
    lambda: (lambda xs: (lambda v: pick([9, -9, -6, 6], round(2 * v[0] + 3 * v[1], 4)))(max(xs)))([(rk4(lambda y, x: (2 * y - 5) / -3, 1, 0, y), y) for y in [1 + k * 0.001 for k in range(0, 3001)]]),
    ['(2y − 5)dy = −3dx → y^{2} − 5y = −3x − 4 (through (0, 1)) → (y − \\f{5}{2})^{2} = \\f{9}{4} − 3x.', 'Vertex (\\f{3}{4}, \\f{5}{2}): 2x + 3y = \\f{3}{2} + \\f{15}{2} = 9.'], 'sep', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'sep', 'The solution of the differential equation (x^{2} + y^{2})dx − 5xydy = 0, y(1) = 0, is :', ['|x^{2} − 4y^{2}|^{5} = x^{2}', '|x^{2} − 2y^{2}|^{5} = x', '|x^{2} − 4y^{2}|^{6} = x', '|x^{2} − 2y^{2}|^{5} = x^{2}'], 1,
    lambda: (lambda pts: [i + 1 for i, g in enumerate([lambda x, y: abs(x * x - 4 * y * y) ** 5 - x * x, lambda x, y: abs(x * x - 2 * y * y) ** 5 - x, lambda x, y: abs(x * x - 4 * y * y) ** 6 - x, lambda x, y: abs(x * x - 2 * y * y) ** 5 - x * x]) if all(abs(g(x, y)) < 1e-5 * max(1, x ** 2) for x, y in pts)][0])([(x, rk4(lambda t, u: (t * t + u * u) / (5 * t * u), 1.2, math.sqrt(1.44 - 1.2 ** 0.4) / 2, x)) for x in (1.5, 2.0)]),   # start on the branch through (1, 0)
    ['Homogeneous: y = vx gives x\\f{dv}{dx} = \\f{1 − 4v^{2}}{5v} → −\\f{5}{8}log|1 − 4v^{2}| = log x (C = 0 from y(1) = 0).', '|1 − 4v^{2}|^{5} = x^{−8} → |x^{2} − 4y^{2}|^{5} = x^{2}.'], 'sep', 3)
add(('2026', 'Apr', '2026-04-02', 1), 'sep', 'If the curve y = f(x) passes through the point (1, e) and satisfies the differential equation dy = y(2 + log_{e}x)dx, x > 0, then f(e) is equal to:', ['e^{e}', 'e^{e^{2}}', 'e^{2e}', 'e^{2^{e}}'], 3,
    lambda: P4([E ** E, E ** (E * E), E ** (2 * E), E ** (2 ** E)], rk4(lambda x, y: y * (2 + LN(x)), 1, E, E), 1e-4),
    ['log y = ∫(2 + log x)dx = x + x log x + C; at (1, e): C = 0.', 'At e: log y = 2e → y = e^{2e}.'], 'sep', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'sep', 'Let y = y(x) be the solution curve of the differential equation (1 + sin x)\\f{dy}{dx} + (y + 1)cos x = 0, y(0) = 0. If the curve y = y(x) passes through the point (α, −\\f{1}{2}), then a value of α is :', ['\\f{π}{6}', '\\f{π}{4}', '\\f{π}{3}', '\\f{π}{2}'], 4,
    lambda: P4([PI / 6, PI / 4, PI / 3, PI / 2], next(a for a in [PI / 6, PI / 4, PI / 3, PI / 2] if abs(rk4(lambda x, y: -(y + 1) * math.cos(x) / (1 + math.sin(x)), 0, 0, a) + 0.5) < 1e-6)),
    ['The equation is d[(1 + sin x)(y + 1)] = 0 → (1 + sin x)(y + 1) = 1.', 'y = −\\f{1}{2} → 1 + sin α = 2 → α = \\f{π}{2}.'], 'sep', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'sep', 'Let x = x(y) be the solution of the differential equation 2y^{2}\\f{dx}{dy} − 2xy + x^{2} = 0, y > 1, x(e) = e. Then x(e^{2}) is equal to :', ['\\f{3}{2}e^{2}', '\\f{2}{3}e^{2}', 'e^{2}', '2e^{2}'], 2,
    lambda: P4([1.5 * E ** 2, 2 / 3 * E ** 2, E ** 2, 2 * E ** 2], rk4(lambda y, x: (2 * x * y - x * x) / (2 * y * y), E, E, E ** 2)),
    ['Bernoulli in x: put u = \\f{1}{x}: \\f{du}{dy} + \\f{u}{y} = \\f{1}{2y^{2}} → uy = \\f{1}{2}log y + C.', 'x(e) = e: C = \\f{1}{2}. At e^{2}: \\f{e^{2}}{x} = \\f{3}{2} → x = \\f{2e^{2}}{3}.'], 'sep', 3)
add(('2025', 'Jan', '2025-01-23', 1), 'sep', 'Let a curve y = f(x) pass through the points (0, 5) and (log_{e}2, k). If the curve satisfies the differential equation 2(3 + y)e^{2x}dx − (7 + e^{2x})dy = 0, then k is equal to', ['16', '32', '8', '4'], 3,
    lambda: P4([16, 32, 8, 4], rk4(lambda x, y: 2 * (3 + y) * math.exp(2 * x) / (7 + math.exp(2 * x)), 0, 5, LN(2))),
    ['Separate: \\f{dy}{3 + y} = \\f{2e^{2x}}{7 + e^{2x}}dx → 3 + y = A(7 + e^{2x}), A = 1.', 'k = 7 + 4 − 3 = 8.'], 'sep', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'sep', 'Let x = x(y) be the solution of the differential equation y = (x − y\\f{dx}{dy})sin(\\f{x}{y}), y > 0 and x(1) = \\f{π}{2}. Then cos(x(2)) is equal to :', ['1 − 2(log_{e}2)', '1 − 2(log_{e}2)^{2}', '2(log_{e}2)^{2} − 1', '2(log_{e}2) − 1'], 3,
    lambda: P4([1 - 2 * LN(2), 1 - 2 * LN(2) ** 2, 2 * LN(2) ** 2 - 1, 2 * LN(2) - 1], math.cos(rk4(lambda y, x: (x - y / math.sin(x / y)) / y, 1, PI / 2, 2))),
    ['Homogeneous: x = vy gives −y\\f{dv}{dy} sin v = 1 → cos v = log y + C, C = 0 (v = \\f{π}{2} at y = 1).', 'At y = 2: cos\\f{x}{2} = log 2 → cos x = 2(log 2)^{2} − 1.'], 'sep', 3)
add(('2026', 'Apr', '2026-04-04', 1), 'sep', 'Let y = y(x) be the solution of the differential equation \\f{dy}{dx} = (1 + x + x^{2})(1 − y + y^{2}), y(0) = \\f{1}{2}. Then (2y(1) − 1) is equal to', ['√{3} tan(\\f{11√{3}}{6})', '\\f{√{3}}{2} tan(\\f{11√{3}}{12})', '√{3} tan(\\f{11√{3}}{12})', '\\f{√{3}}{2} tan(\\f{11√{3}}{6})'], 3,
    lambda: (lambda G: P4([S3 * math.tan(11 * S3 / 6), S3 / 2 * math.tan(11 * S3 / 12), S3 * math.tan(11 * S3 / 12), S3 / 2 * math.tan(11 * S3 / 6)], S3 * math.tan(S3 / 2 * (G + 2 / S3 * math.atan(0)))) if all(abs((2 / S3 * math.atan((2 * (y + 1e-6) - 1) / S3) - 2 / S3 * math.atan((2 * (y - 1e-6) - 1) / S3)) / 2e-6 - 1 / (1 - y + y * y)) < 1e-6 for y in (0.1, 0.9, 2.5)) else None)(integ(lambda x: 1 + x + x * x, 0, 1)),   # the solution passes through a vertical asymptote before x = 1, so integrate the separated form
    ['Separate: \\f{dy}{(y − 1/2)^{2} + 3/4} = (1 + x + x^{2})dx → \\f{2}{√{3}}tan^{−1}\\f{2y − 1}{√{3}} = x + \\f{x^{2}}{2} + \\f{x^{3}}{3}.', 'At x = 1 the right side is \\f{11}{6} → 2y − 1 = √{3} tan\\f{11√{3}}{12}.'], 'sep', 3)
add(('2026', 'Jan', '2026-01-22', 1), 'sep', 'Let the solution curve of the differential equation xdy − ydx = √{x^{2} + y^{2}}dx, x > 0, y(1) = 0, be y = y(x). Then y(3) is equal to', ['4', '6', '1', '2'], 1,
    lambda: P4([4, 6, 1, 2], rk4(lambda x, y: (y + math.sqrt(x * x + y * y)) / x, 1, 0, 3)),
    ['Homogeneous: y = vx gives \\f{dv}{√{1 + v^{2}}} = \\f{dx}{x} → v + √{1 + v^{2}} = x.', 'v = \\f{x^{2} − 1}{2x} → y = \\f{x^{2} − 1}{2} → y(3) = 4.'], 'sep', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'sep', 'Let y = y(x) be the solution of the differential equation x\\f{dy}{dx} − sin 2y = x^{3}(2 − x^{3})cos^{2}y, x ≠ 0. If y(2) = 0, then tan(y(1)) is equal to', ['\\f{3}{4}', '\\f{7}{4}', '−\\f{7}{4}', '−\\f{3}{4}'], 2,
    lambda: P4([0.75, 1.75, -1.75, -0.75], math.tan(rk4(lambda x, y: (math.sin(2 * y) + x ** 3 * (2 - x ** 3) * math.cos(y) ** 2) / x, 2, 0, 1))),
    ['Divide by cos^{2}y; with t = tan y: xt\' − 2t = x^{3}(2 − x^{3}) → (\\f{t}{x^{2}})\' = 2 − x^{3}.', '\\f{t}{x^{2}} = 2x − \\f{x^{4}}{4} + C; t(2) = 0 → C = 0. t(1) = 2 − \\f{1}{4} = \\f{7}{4}.'], 'sep', 3)

# ---------------- forming equations and families of curves ----------------
add(('2024', 'Apr', '2024-04-05', 2), 'form', 'The differential equation of the family of circles passing the origin and having center at the line y = x is :', ['(x^{2} − y^{2} + 2xy)dx = (x^{2} − y^{2} + 2xy)dy', '(x^{2} + y^{2} + 2xy)dx = (x^{2} + y^{2} − 2xy)dy', '(x^{2} − y^{2} + 2xy)dx = (x^{2} − y^{2} − 2xy)dy', '(x^{2} + y^{2} − 2xy)dx = (x^{2} + y^{2} + 2xy)dy'], 3,
    lambda: (lambda pts: [i + 1 for i, (A, B) in enumerate([(lambda x, y: x * x - y * y + 2 * x * y, lambda x, y: x * x - y * y + 2 * x * y), (lambda x, y: x * x + y * y + 2 * x * y, lambda x, y: x * x + y * y - 2 * x * y), (lambda x, y: x * x - y * y + 2 * x * y, lambda x, y: x * x - y * y - 2 * x * y), (lambda x, y: x * x + y * y - 2 * x * y, lambda x, y: x * x + y * y + 2 * x * y)]) if all(abs(A(x, y) - B(x, y) * m) < 1e-9 for x, y, m in pts)][0])([(a + a * S2 * math.cos(t), a + a * S2 * math.sin(t), -math.cos(t) / math.sin(t)) for a, t in ((1.3, 0.7), (-0.6, 2.0), (2.1, 4.0))]),
    ['Circles x^{2} + y^{2} − 2ax − 2ay = 0. Differentiate: a = \\f{x + yy\'}{1 + y\'}.', 'Eliminate a: (x^{2} + y^{2})(1 + y\') = 2(x + y)(x + yy\') → (x^{2} − y^{2} + 2xy)dx = (x^{2} − y^{2} − 2xy)dy.'], 'form', 3)
add(('2024', 'Apr', '2024-04-06', 2), 'form', 'Suppose the solution of the differential equation \\f{dy}{dx} = \\f{(2 + α)x − βy + 2}{βx − 2αy − (βy − 4α)} represents a circle passing through origin. Then the radius of this circle is :', ['√{17}', '\\f{1}{2}', '\\f{√{17}}{2}', '2'], 3,
    lambda: (lambda al: (lambda h, k: P4([math.sqrt(17), 0.5, math.sqrt(17) / 2, 2], math.hypot(h, k)))(-2 / (2 + al), 2) if abs((2 + al) - 2 * al) < 1e-12 else None)(2),
    ['A circle\'s slope is −\\f{x − h}{y − k}: no y on top means β = 0; then \\f{(2 + α)x + 2}{−2α(y − 2)} needs \\f{2 + α}{2α} = 1 → α = 2.', 'Slope = −\\f{x + 1/2}{y − 2}: centre (−\\f{1}{2}, 2), through O → r = √{\\f{1}{4} + 4} = \\f{√{17}}{2}.'], 'form', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'form', 'Let f(x) be a positive function such that the area bounded by y = f(x), y = 0 from x = 0 to x = a > 0 is e^{−a} + 4a^{2} + a − 1. Then the differential equation, whose general solution is y = c_{1}f(x) + c_{2}, where c_{1} and c_{2} are arbitrary constants, is :', ['(8e^{x} − 1)\\f{d^{2}y}{dx^{2}} + \\f{dy}{dx} = 0', '(8e^{x} + 1)\\f{d^{2}y}{dx^{2}} − \\f{dy}{dx} = 0', '(8e^{x} + 1)\\f{d^{2}y}{dx^{2}} + \\f{dy}{dx} = 0', '(8e^{x} − 1)\\f{d^{2}y}{dx^{2}} − \\f{dy}{dx} = 0'], 3,
    lambda: (lambda f1, f2: [i + 1 for i, (p, q) in enumerate([(lambda x: 8 * math.exp(x) - 1, 1), (lambda x: 8 * math.exp(x) + 1, -1), (lambda x: 8 * math.exp(x) + 1, 1), (lambda x: 8 * math.exp(x) - 1, -1)]) if all(abs(p(x) * f2(x) + q * f1(x)) < 1e-9 for x in (0.1, 0.7, 1.9))][0])(lambda x: math.exp(-x) + 8, lambda x: -math.exp(-x)),
    ['f(a) = \\f{d}{da}(e^{−a} + 4a^{2} + a − 1) = −e^{−a} + 8a + 1, so y\' = c_{1}(e^{−x} + 8), y" = −c_{1}e^{−x}.', '\\f{y"}{y\'} = \\f{−e^{−x}}{e^{−x} + 8} → (1 + 8e^{x})y" + y\' = 0.'], 'form', 2)
for _p in P: _p['t'] = _p['fam']
