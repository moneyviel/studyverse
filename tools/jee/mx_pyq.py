"""Real JEE Main questions — Mathematics Unit 3: Matrices and Determinants. Our own solutions; chk re-solves each with exact
rank tests / brute force (mxs.py). Skipped: 4-Apr-2024 morning Q25 (locus is a single point, not a hyperbola), 7-Apr-2025 S1 Q18
(set-builder statement garbled in source), 9-Apr-2024 morning Q27 (data give a non-integer power)."""
from fractions import Fraction as F
from itertools import product
import math
from common import new_registry, pick, near, verify
from mxs import solve2, kind, det3, RATS
P, add = new_registry()
def one(lst): assert len(lst) == 1, lst; return lst[0]
def detN(M):   # Laplace expansion, any size
    if len(M) == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * detN([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(len(M)))
def adjdet(n, d): return d ** (n - 1)            # |adj A| = |A|^(n−1)
def kdet(n, k, d): return k ** n * d              # |kA| = k^n |A|
def fac(v, ps=(2, 3, 5)):
    v = F(v); out = {}
    for p in ps:
        e = 0
        while v.numerator % p == 0: v /= p; e += 1
        while v.denominator % p == 0: v *= p; e -= 1
        out[p] = e
    assert abs(v) == 1, v; return out

# ---------- determinants, adjoint & powers ----------
add(('2025', 'Apr', '2025-04-02', 1), 'det', 'Let a ∈ R and A be a matrix of order 3 × 3 such that det(A) = −4 and A + I = [[1, a, 1], [2, 1, 0], [a, 1, 2]], where I is the identity matrix of order 3 × 3. If det((a + 1)adj((a − 1)A)) is 2^{m}3^{n}, m, n ∈ {0, 1, 2, …, 20}, then m + n is equal to :',
    ['14', '16', '17', '15'], 2, lambda: (lambda a: pick([14, 16, 17, 15], sum(fac(kdet(3, a + 1, adjdet(3, kdet(3, a - 1, -4)))).values())))(one([a for a in range(-20, 21) if detN([[0, a, 1], [2, 0, 0], [a, 1, 1]]) == -4])),
    ['A = (A + I) − I = [[0, a, 1], [2, 0, 0], [a, 1, 1]] → det A = 2 − 2a = −4 → a = 3.', 'det(4·adj(2A)) = 4^{3}·|2A|^{2} = 64 × (8 × (−4))^{2} = 2^{6} × 2^{10} = 2^{16}.', 'm = 16, n = 0 → 16.'], 'adj', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'det', 'Let A be a matrix of order 3 × 3 and |A| = 5. If |2adj(3A adj(2A))| = 2^{α}·3^{β}·5^{γ}, α, β, γ ∈ N, then α + β + γ is equal to',
    ['28', '27', '26', '25'], 2, lambda: pick([28, 27, 26, 25], sum(fac(kdet(3, 2, adjdet(3, kdet(3, 3, 5) * adjdet(3, kdet(3, 2, 5))))).values())),
    ['|adj(2A)| = |2A|^{2} = 40^{2} = 1600; |3A adj(2A)| = 27 × 5 × 1600 = 216000 = 2^{6}3^{3}5^{3}.', '|2 adj(M)| = 2^{3}|M|^{2} = 2^{3} × 2^{12}3^{6}5^{6} = 2^{15}3^{6}5^{6}.', 'α + β + γ = 15 + 6 + 6 = 27.'], 'adj', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'det', 'Let A and B be two square matrices of order 3 such that |A| = 3 and |B| = 2. Then |A^{T}A(adj(2A))^{−1}(adj(4B))(adj(AB))^{−1}AA^{T}| is equal to :',
    ['64', '81', '32', '108'], 1, lambda: pick([64, 81, 32, 108], int(F(3 * 3 * adjdet(3, kdet(3, 4, 2)) * 3 * 3, adjdet(3, kdet(3, 2, 3)) * adjdet(3, 6)))),
    ['|adj(2A)| = (8 × 3)^{2} = 576, |adj(4B)| = (64 × 2)^{2} = 16384, |adj(AB)| = 6^{2} = 36.', 'Value = \\f{3 × 3 × 16384 × 3 × 3}{576 × 36} = 64.'], 'adj', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'det', 'If A is a square matrix of order 3 such that det(A) = 3 and det(adj(−4adj(−3adj(3adj((2A)^{−1}))))) = 2^{m}3^{n}, then m + 2n is equal to:',
    ['3', '2', '4', '6'], 3, lambda: (lambda e: pick([3, 2, 4, 6], e[2] + 2 * e[3]))(fac(adjdet(3, kdet(3, -4, adjdet(3, kdet(3, -3, adjdet(3, kdet(3, 3, adjdet(3, F(1, kdet(3, 2, 3))))))))))),
    ['|(2A)^{−1}| = \\f{1}{24}; each adj squares the determinant, each scalar k multiplies it by k^{3}.', '1/24 → 1/576 → ×27: 3/64 → 9/4096 → ×(−27): −243/4096 → 3^{10}/2^{24} → ×(−64): −3^{10}/2^{18} → 3^{20}/2^{36}.', 'm = −36, n = 20 → m + 2n = 4.'], 'adj', 3)
add(('2025', 'Jan', '2025-01-22', 1), 'det', 'Let A be a square matrix of order 3 such that det(A) = −2 and det(3adj(−6adj(3A))) = 2^{m+n}·3^{mn}, m > n. Then 4m + 2n is equal to ______.',
    None, 34, lambda: (lambda e: one([4 * m + 2 * n for m in range(30) for n in range(m) if m + n == e[2] and m * n == e[3]]))(fac(kdet(3, 3, adjdet(3, kdet(3, -6, adjdet(3, kdet(3, 3, -2))))))),
    ['|3A| = −54 → |adj| = 54^{2} = 2^{2}3^{6} → ×(−6)^{3}: −2^{5}3^{9} → adj: 2^{10}3^{18} → ×27: 2^{10}3^{21}.', 'm + n = 10, mn = 21 → m = 7, n = 3 → 4m + 2n = 34.'], 'adj', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'det', 'Let |A| = 6, where A is a 3 × 3 matrix. If |adj(3adj(A^{2}·adj(2A)))| = 2^{m}·3^{n}, m, n ∈ N, then m + n is equal to ______.',
    None, 62, lambda: sum(fac(adjdet(3, kdet(3, 3, adjdet(3, 36 * adjdet(3, kdet(3, 2, 6)))))).values()),
    ['|adj(2A)| = 48^{2}; |A^{2}adj(2A)| = 36 × 2304 = 2^{10}3^{4}.', 'adj → 2^{20}3^{8}; ×27 → 2^{20}3^{11}; adj → 2^{40}3^{22}.', 'm + n = 62.'], 'adj', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'mat', 'Let A = [[cos θ, 0, −sin θ], [0, 1, 0], [sin θ, 0, cos θ]]. If for some θ ∈ (0, π), A^{2} = A^{T}, then the sum of the diagonal elements of the matrix (A + I)^{3} + (A − I)^{3} − 6A is equal to ______.',
    None, 6, lambda: (lambda c, s: (lambda A: (lambda A2: int(round(2 * sum(sum(A2[i][k] * A[k][i] for k in range(3)) for i in range(3)))))([[sum(A[i][k] * A[k][j] for k in range(3)) for j in range(3)] for i in range(3)]))([[c, 0, -s], [0, 1, 0], [s, 0, c]]))(math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3)),
    ['A is a rotation, so A^{T} = A^{−1}; A^{2} = A^{−1} → A^{3} = I (θ = \\f{2π}{3}).', '(A + I)^{3} + (A − I)^{3} = 2A^{3} + 6A → expression = 2A^{3} = 2I.', 'Trace = 6.'], 'mat', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'mat', 'Let A be a 2 × 2 symmetric matrix such that A[1, 1]^{T} = [3, 7]^{T} and the determinant of A be 1. If A^{−1} = αA + βI, where I is an identity matrix of order 2 × 2, then α + β equals ______.',
    None, 5, lambda: one([(-1 + (a + c)) for a in range(-10, 11) for b in range(-10, 11) for c in range(-10, 11) if a + b == 3 and b + c == 7 and a * c - b * b == 1]),
    ['A = [[a, b], [b, c]]: a + b = 3, b + c = 7, ac − b^{2} = 1 → b = 2, a = 1, c = 5.', 'Cayley–Hamilton: A^{2} − 6A + I = 0 → A^{−1} = 6I − A → α = −1, β = 6.', 'α + β = 5.'], 'mat', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'mat', 'The number of singular matrices of order 2, whose elements are from the set {2, 3, 6, 9}, is ______.', None, 36,
    lambda: sum(1 for a, b, c, d in product([2, 3, 6, 9], repeat=4) if a * d == b * c),
    ['Singular ⇔ ad = bc. List the 16 ordered products ad and how often each occurs: 4 (1), 6 (2), 9 (1), 12 (2), 18 (4), 27 (2), 36 (1), 54 (2), 81 (1).', 'For each product value, (a, d) and (b, c) can each be any of its pairs → Σ (count)^{2} = 1 + 4 + 1 + 4 + 16 + 4 + 1 + 4 + 1 = 36.'], 'mat', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'mat', 'Let A = [a_{ij}] be a square matrix of order 2 with entries either 0 or 1. Let E be the event that A is an invertible matrix. Then the probability P(E) is :',
    ['\\f{5}{8}', '\\f{3}{16}', '\\f{1}{8}', '\\f{3}{8}'], 4, lambda: pick(['\\f{5}{8}', '\\f{3}{16}', '\\f{1}{8}', '\\f{3}{8}'], (lambda f: f'\\f{{{f.numerator}}}{{{f.denominator}}}')(F(sum(1 for a, b, c, d in product([0, 1], repeat=4) if a * d != b * c), 16))),
    ['16 matrices in all. det = ad − bc ≠ 0 needs exactly one of ad, bc to be 1.', 'ad = 1, bc = 0: 3 ways; ad = 0, bc = 1: 3 ways → 6.', 'P = \\f{6}{16} = \\f{3}{8}.'], 'mat', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'mat', 'Let A = [a_{ij}] be a 2 × 2 matrix such that a_{ij} ∈ {0, 1} for all i and j. Let the random variable X denote the possible values of the determinant of the matrix A. Then, the variance of X is :',
    ['\\f{1}{4}', '\\f{5}{8}', '\\f{3}{8}', '\\f{3}{4}'], 3, lambda: pick(['\\f{1}{4}', '\\f{5}{8}', '\\f{3}{8}', '\\f{3}{4}'], (lambda ds: (lambda m: (lambda v: f'\\f{{{v.numerator}}}{{{v.denominator}}}')(sum(F(x * x, 16) for x in ds) - m * m))(sum(F(x, 16) for x in ds)))([a * d - b * c for a, b, c, d in product([0, 1], repeat=4)])),
    ['det = +1 for 3 matrices, −1 for 3, 0 for 10.', 'Mean 0; variance = E(X^{2}) = \\f{6}{16} = \\f{3}{8}.'], 'mat', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'mat', 'The number of 3 × 2 matrices A, which can be formed using the elements of the set {−2, −1, 0, 1, 2} such that the sum of all the diagonal elements of A^{T}A is 5, is ______.', None, 312,
    lambda: sum(1 for v in product([-2, -1, 0, 1, 2], repeat=6) if sum(x * x for x in v) == 5),
    ['trace(A^{T}A) = sum of squares of all 6 entries = 5.', 'Either one ±2 and one ±1 (6 × 5 × 4 = 120 ways) or five ±1 and one 0 (6 × 2^{5} = 192 ways).', 'Total 312.'], 'mat', 2)

# ---------- systems of linear equations ----------
def sysq(src, q, o, key, chk, sol, diff=2): add(src, 'sys', q, o, key, chk, sol, 'sys', diff)
sysq(('2025', 'Apr', '2025-04-02', 1), 'If the system of linear equations 3x + y + βz = 3, 2x + αy − z = −3, x + 2y + z = 4 has infinitely many solutions, then the value of 22β − 9α is :',
     ['31', '43', '49', '37'], 1, lambda: pick([31, 43, 49, 37], (lambda b, a: 22 * b - 9 * a)(*one(solve2(lambda b, a: ([[3, 1, b], [2, a, -1], [1, 2, 1]], [3, -3, 4]))))),
     ['Infinite solutions need D = 0 and D_{x} = D_{y} = D_{z} = 0.', 'D_{y} = 11β − 6 = 0 → β = \\f{6}{11}; D = 3α + 3 + 4β − αβ = 0 → α = −\\f{19}{9}.', '22β − 9α = 12 + 19 = 31.'])
sysq(('2025', 'Apr', '2025-04-02', 2), 'If the system of equations 2x + λy + 3z = 5, 3x + 2y − z = 7, 4x + 5y + μz = 9 has infinitely many solutions, then (λ^{2} + μ^{2}) is equal to :',
     ['26', '18', '22', '30'], 1, lambda: pick([26, 18, 22, 30], (lambda l, m: l * l + m * m)(*one(solve2(lambda l, m: ([[2, l, 3], [3, 2, -1], [4, 5, m]], [5, 7, 9]))))),
     ['D_{z} = det[[2, λ, 5], [3, 2, 7], [4, 5, 9]] = 0 and D = 0.', 'Solving gives λ = −1, μ = −5.', 'λ^{2} + μ^{2} = 26.'])
sysq(('2024', 'Apr', '2024-04-04', 1), 'If the system of equations x + (√{2}sin α)y + (√{2}cos α)z = 0, x + (cos α)y + (sin α)z = 0, x + (sin α)y − (cos α)z = 0 has a non-trivial solution, then α ∈ (0, \\f{π}{2}) is equal to :',
     ['\\f{3π}{4}', '\\f{7π}{24}', '\\f{5π}{24}', '\\f{11π}{24}'], 3, lambda: (lambda D: [i + 1 for i, k in enumerate([18, 7, 5, 11]) if abs(D(k * math.pi / 24)) < 1e-9 and k * math.pi / 24 < math.pi / 2][0])(
         lambda a: (lambda s, c: 1 * (-c * c - s * s) - 2 ** 0.5 * s * (-c - s) + 2 ** 0.5 * c * (s - c))(math.sin(a), math.cos(a))),
     ['Non-trivial solution ⇔ determinant = 0.', 'D = −1 + √{2}(sin 2α − cos 2α) = −1 + 2sin(2α − \\f{π}{4}) = 0.', '2α − \\f{π}{4} = \\f{π}{6} → α = \\f{5π}{24} (the other value \\f{13π}{24} is outside (0, \\f{π}{2})).'])
sysq(('2024', 'Apr', '2024-04-05', 2), 'The values of m, n, for which the system of equations x + y + z = 4, 2x + 5y + 5z = 17, x + 2y + mz = n has infinitely many solutions, satisfy the equation :',
     ['m^{2} + n^{2} − m − n = 46', 'm^{2} + n^{2} + m + n = 64', 'm^{2} + n^{2} + mn = 68', 'm^{2} + n^{2} − mn = 39'], 4,
     lambda: (lambda m, n: [i + 1 for i, v in enumerate([m * m + n * n - m - n == 46, m * m + n * n + m + n == 64, m * m + n * n + m * n == 68, m * m + n * n - m * n == 39]) if v])(*one(solve2(lambda m, n: ([[1, 1, 1], [2, 5, 5], [1, 2, m]], [4, 17, n]))))[0],
     ['D = 3m − 6 = 0 → m = 2.', 'First two equations give x = 1, y + z = 3; third: 1 + 2(y + z) = n → n = 7.', 'm^{2} + n^{2} − mn = 4 + 49 − 14 = 39.'])
sysq(('2024', 'Apr', '2024-04-05', 1), 'If the system of equations 11x + y + λz = −5, 2x + 3y + 5z = 3, 8x − 19y − 39z = μ has infinitely many solutions, then λ^{4} − μ is equal to :',
     ['49', '45', '47', '51'], 3, lambda: pick([49, 45, 47, 51], (lambda l, m: l ** 4 - m)(*one(solve2(lambda l, m: ([[11, 1, l], [2, 3, 5], [8, -19, -39]], [-5, 3, m]))))),
     ['D = −124 − 62λ = 0 → λ = −2.', 'Row 3 = 2 × row 1 − 7 × row 2 on the left, so μ = 2(−5) − 7(3) = −31.', 'λ^{4} − μ = 16 + 31 = 47.'])
sysq(('2024', 'Apr', '2024-04-06', 2), 'If the system of equations 2x + 7y + λz = 3, 3x + 2y + 5z = 4, x + μy + 32z = −1 has infinitely many solutions, then (λ − μ) is equal to ______.',
     None, 38, lambda: (lambda m, l: int(l - m))(*one(solve2(lambda m, l: ([[2, 7, l], [3, 2, 5], [1, m, 32]], [3, 4, -1])))),
     ['Infinitely many solutions → equation 3 = p × (eq 1) + q × (eq 2). Use the x-coefficients and the right sides: 2p + 3q = 1, 3p + 4q = −1 → q = 5, p = −7.', 'y: 7p + 2q = −39 = μ; z: λp + 5q = 32 → −7λ + 25 = 32 → λ = −1.', 'λ − μ = −1 + 39 = 38.'])
sysq(('2025', 'Apr', '2025-04-07', 1), 'Let the system of equations 2x + 3y + 5z = 9, 7x + 3y − 2z = 8, 12x + 3y − (4 + λ)z = 16 − μ have infinitely many solutions. Then the radius of the circle centred at (λ, μ) and touching the line 4x = 3y is',
     ['\\f{17}{5}', '7', '\\f{7}{5}', '\\f{21}{5}'], 3, lambda: (lambda l, m: pick([F(17, 5), 7, F(7, 5), F(21, 5)], abs(4 * l - 3 * m) / 5))(*one(solve2(lambda l, m: ([[2, 3, 5], [7, 3, -2], [12, 3, -(4 + l)]], [9, 8, 16 - m])))),
     ['Row 3 = 2 × row 2 − row 1 on x, y: 14 − 2 = 12 ✓, 6 − 3 = 3 ✓; z: −4 − 5 = −9 = −(4 + λ) → λ = 5.', 'RHS: 16 − 9 = 7 = 16 − μ → μ = 9.', 'Radius = \\f{|4·5 − 3·9|}{5} = \\f{7}{5}.'])
sysq(('2025', 'Apr', '2025-04-07', 2), 'Let the system of equations x + 5y − z = 1, 4x + 3y − 3z = 7, 24x + y + λz = μ, λ, μ ∈ R, have infinitely many solutions. Then the number of the solutions of this system, if x, y, z are integers and satisfy 7 ≤ x + y + z ≤ 77, is :',
     ['3', '5', '6', '4'], 1, lambda: (lambda l, m: pick([3, 5, 6, 4], sum(1 for x in range(-300, 301) for y in range(-300, 301) for z in [x + 5 * y - 1] if 4 * x + 3 * y - 3 * z == 7 and 24 * x + y + l * z == m and 7 <= x + y + z <= 77)))(*one(solve2(lambda l, m: ([[1, 5, -1], [4, 3, -3], [24, 1, l]], [1, 7, m])))),
     ['With infinitely many solutions, every solution of the first two equations works (λ = −17, μ = 45).', 'From eq 1: x = 1 − 5y + z. Put in eq 2: −17y + z = 3 → z = 17y + 3, x = 12y + 4 — integers for every integer y.', 'x + y + z = 30y + 7; 7 ≤ 30y + 7 ≤ 77 → y = 0, 1, 2 → 3 solutions.'])
sysq(('2024', 'Apr', '2024-04-08', 2), 'If the system of equations x + 4y − z = λ, 7x + 9y + μz = −3, 5x + y + 2z = −1 has infinitely many solutions, then (2μ + 3λ) is equal to :',
     ['2', '−3', '3', '−2'], 2, lambda: (lambda m, l: pick([2, -3, 3, -2], 2 * m + 3 * l))(*one(solve2(lambda m, l: ([[1, 4, -1], [7, 9, m], [5, 1, 2]], [l, -3, -1])))),
     ['Eq 2 must be p × (eq 1) + q × (eq 3): x: p + 5q = 7, y: 4p + q = 9 → p = 2, q = 1.', 'z: −2 + 2 = 0 = μ; RHS: 2λ − 1 = −3 → λ = −1.', '2μ + 3λ = 0 − 3 = −3.'])
sysq(('2024', 'Apr', '2024-04-09', 1), 'Let λ, μ ∈ R. If the system of equations 3x + 5y + λz = 3, 7x + 11y − 9z = 2, 97x + 155y − 189z = μ has infinitely many solutions, then μ + 2λ is equal to :',
     ['25', '24', '27', '22'], 1, lambda: (lambda l, m: pick([25, 24, 27, 22], m + 2 * l))(*one(solve2(lambda l, m: ([[3, 5, l], [7, 11, -9], [97, 155, -189]], [3, 2, m])))),
     ['Eq 3 = a × (eq 1) + b × (eq 2) on x, y: 3a + 7b = 97, 5a + 11b = 155 → a = 9, b = 10.', 'z: 9λ − 90 = −189 → λ = −11; RHS: μ = 27 + 20 = 47.', 'μ + 2λ = 47 − 22 = 25.'])
sysq(('2026', 'Apr', '2026-04-02', 2), 'If the system of equations x + 5y + 6z = 4, 2x + 3y + 4z = 7, x + 6y + az = b has infinitely many solutions, then the point (a, b) lies on the line',
     ['y − x = 3', 'x − y = 3', 'x + y = 11', 'x + y = 12'], 2, lambda: (lambda a, b: [i + 1 for i, v in enumerate([b - a == 3, a - b == 3, a + b == 11, a + b == 12]) if v][0])(*one(solve2(lambda a, b: ([[1, 5, 6], [2, 3, 4], [1, 6, a]], [4, 7, b])))),
     ['Write row 3 = p·row 1 + q·row 2: p + 2q = 1, 5p + 3q = 6 → p = \\f{9}{7}, q = −\\f{1}{7}.', 'a = 6p + 4q = \\f{50}{7}, b = 4p + 7q = \\f{29}{7}.', 'a − b = 3 → the point lies on x − y = 3.'])
sysq(('2026', 'Jan', '2026-01-21', 2), 'If the system of equations 3x + y + 4z = 3, 2x + αy − z = −3, x + 2y + z = 4 has no solution, then the value of α is equal to :',
     ['19', '4', '13', '23'], 1, lambda: pick([19, 4, 13, 23], int(one([a for a in RATS if kind([[3, 1, 4], [2, a, -1], [1, 2, 1]], [3, -3, 4]) == 'none']))),
     ['No solution needs D = 0: D = 19 − α → α = 19.', 'Then D_{x} ≠ 0, so the system is inconsistent.'])
sysq(('2025', 'Jan', '2025-01-22', 2), 'If the system of linear equations : x + y + 2z = 6, 2x + 3y + az = a + 1, −x − 3y + bz = 2b, where a, b ∈ R, has infinitely many solutions, then 7a + 3b is equal to :',
     ['9', '16', '22', '12'], 2, lambda: (lambda a, b: pick([9, 16, 22, 12], 7 * a + 3 * b))(*one([s for s in solve2(lambda a, b: ([[1, 1, 2], [2, 3, a], [-1, -3, b]], [6, a + 1, 2 * b]))])),
     ['Eq 3 = p × (eq 1) + q × (eq 2) on x, y: p + 2q = −1, p + 3q = −3 → q = −2, p = 3.', 'z: 6 − 2a = b; RHS: 18 − 2(a + 1) = 2b → b = 8 − a.', '6 − 2a = 8 − a → a = −2, b = 10 → 7a + 3b = −14 + 30 = 16.'])
sysq(('2025', 'Jan', '2025-01-23', 1), 'If the system of equations (λ − 1)x + (λ − 4)y + λz = 5, λx + (λ − 1)y + (λ − 4)z = 7, (λ + 1)x + (λ + 2)y − (λ + 2)z = 9 has infinitely many solutions, then λ^{2} + λ is equal to',
     ['20', '10', '6', '12'], 4, lambda: pick([20, 10, 6, 12], int(one([l * l + l for l in RATS if kind([[l - 1, l - 4, l], [l, l - 1, l - 4], [l + 1, l + 2, -(l + 2)]], [5, 7, 9]) == 'infinite']))),
     ['D = 0 gives the candidate values of λ; checking D_{x} = D_{y} = D_{z} = 0 as well leaves only λ = 3.', 'λ^{2} + λ = 9 + 3 = 12.'], 3)
sysq(('2025', 'Jan', '2025-01-23', 2), 'The system of equations x + y + z = 6, x + 2y + 5z = 9, x + 5y + λz = μ, has no solution if',
     ['λ = 17, μ ≠ 18', 'λ = 17, μ = 18', 'λ ≠ 17, μ ≠ 18', 'λ = 15, μ ≠ 17'], 1,
     lambda: 1 if kind([[1, 1, 1], [1, 2, 5], [1, 5, 17]], [6, 9, 20]) == 'none' and kind([[1, 1, 1], [1, 2, 5], [1, 5, 17]], [6, 9, 18]) == 'infinite' and kind([[1, 1, 1], [1, 2, 5], [1, 5, 15]], [6, 9, 20]) == 'unique' else 0,
     ['D = λ − 17 → singular only for λ = 17.', 'With λ = 17, row 3 = 4 × row 2 − 3 × row 1 on the left, so consistency needs μ = 36 − 18 = 18.', 'No solution: λ = 17, μ ≠ 18.'])
sysq(('2025', 'Jan', '2025-01-24', 1), 'If the system of equations 2x − y + z = 4, 5x + λy + 3z = 12, 100x − 47y + μz = 212 has infinitely many solutions, then μ − 2λ is equal to',
     ['55', '57', '59', '56'], 2, lambda: (lambda l, m: pick([55, 57, 59, 56], m - 2 * l))(*one(solve2(lambda l, m: ([[2, -1, 1], [5, l, 3], [100, -47, m]], [4, 12, 212])))),
     ['Eq 3 = p × (eq 1) + q × (eq 2) on x and the right side: 2p + 5q = 100, 4p + 12q = 212 → q = 6, p = 35.', 'y: −35 + 6λ = −47 → λ = −2; z: 35 + 18 = 53 = μ.', 'μ − 2λ = 53 + 4 = 57.'])
sysq(('2025', 'Jan', '2025-01-24', 2), 'If the system of equations x + 2y − 3z = 2, 2x + λy + 5z = 5, 14x + 3y + μz = 33 has infinitely many solutions, then λ + μ is equal to :',
     ['10', '12', '13', '11'], 2, lambda: (lambda l, m: pick([10, 12, 13, 11], l + m))(*one(solve2(lambda l, m: ([[1, 2, -3], [2, l, 5], [14, 3, m]], [2, 5, 33])))),
     ['Row 3 = p·row 1 + q·row 2 with RHS: 2p + 5q = 33 and p + 2q = 14 → q = 5, p = 4.', 'y: 8 + 5λ = 3 → λ = −1; z: −12 + 25 = 13 = μ.', 'λ + μ = 12.'])
sysq(('2026', 'Apr', '2026-04-04', 2), 'If the system of equations: x + y + z = 5, x + 2y + 3z = 9, x + 3y + λz = μ has infinitely many solutions, then the value of λ + μ is:',
     ['16', '18', '19', '21'], 2, lambda: (lambda l, m: pick([16, 18, 19, 21], l + m))(*one(solve2(lambda l, m: ([[1, 1, 1], [1, 2, 3], [1, 3, l]], [5, 9, m])))),
     ['Row 3 = 2 × row 2 − row 1 on x, y → z: 6 − 1 = 5 = λ; RHS: 18 − 5 = 13 = μ.', 'λ + μ = 18.'], 1)
sysq(('2026', 'Jan', '2026-01-23', 2), 'The system of linear equations x + y + z = 6, 2x + 5y + az = 36, x + 2y + 3z = b has',
     ['unique solution for a = 8 and b = 16', 'infinitely many solutions for a = 8 and b = 14', 'infinitely many solutions for a = 8 and b = 16', 'unique solution for a = 8 and b = 14'], 2,
     lambda: pick(['unique solution for a = 8 and b = 16', 'infinitely many solutions for a = 8 and b = 14', 'infinitely many solutions for a = 8 and b = 16', 'unique solution for a = 8 and b = 14'],
                  f'{ {"unique": "unique solution", "infinite": "infinitely many solutions"}[kind([[1, 1, 1], [2, 5, 8], [1, 2, 3]], [6, 36, 14])]} for a = 8 and b = 14' if kind([[1, 1, 1], [2, 5, 8], [1, 2, 3]], [6, 36, 16]) == 'none' else '?'),
     ['D = 8 − a → a = 8 makes the system singular.', 'Row 3 = \\f{1}{3}(row 1 + row 2) on the left → b = \\f{6 + 36}{3} = 14 for consistency.', 'a = 8, b = 14 → infinitely many solutions (b = 16 → none).'])
sysq(('2026', 'Apr', '2026-04-08', 2), 'If the system of linear equations: x + y + z = 6, x + 2y + 5z = 10, 2x + 3y + λz = μ has infinitely many solutions, then the value of λ + μ equals:',
     ['12', '16', '22', '28'], 3, lambda: (lambda l, m: pick([12, 16, 22, 28], l + m))(*one(solve2(lambda l, m: ([[1, 1, 1], [1, 2, 5], [2, 3, l]], [6, 10, m])))),
     ['Row 3 = row 1 + row 2 on x, y → λ = 1 + 5 = 6 and μ = 6 + 10 = 16.', 'λ + μ = 22.'], 1)

if __name__ == '__main__': print(verify(P), 'real questions verified')
