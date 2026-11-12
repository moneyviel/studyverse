"""Exact linear-algebra helpers for the matrices unit checks (Fractions only)."""
from fractions import Fraction as F
from itertools import product
def rank(M):
    M = [[F(x) for x in r] for r in M]; rk, cols = 0, len(M[0])
    for c in range(cols):
        p = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]; M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk
def det3(m): return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
def kind(A, b):
    ra, rb = rank(A), rank([r + [x] for r, x in zip(A, b)])
    return 'unique' if ra == 3 else 'none' if ra < rb else 'infinite'
INTS = [F(i) for i in range(-120, 121)]
RATS = sorted({F(p, q) for q in range(1, 13) for p in range(-400, 401)})
def search(build, want, grids):
    """build(*params) -> (A, b); return list of params where kind == want."""
    return [ps for ps in product(*grids) if kind(*build(*ps)) == want]
def solve_infinite(build, lam_grid=RATS, mu_grid=RATS):
    """lam enters A (det must vanish), mu only in b: find lam by det, then mu by rank."""
    out = []
    for l in lam_grid:
        A, _ = build(l, F(0))
        if det3(A) != 0: continue
        for m in mu_grid:
            if kind(*build(l, m)) == 'infinite': out.append((l, m))
    return out
def solve2(build, want='infinite', grid=RATS):
    """Two parameters p1, p2. For each p1 on the grid, the determinant is affine in p2 (p2 appears once in A)
    or does not involve p2 (p2 only in b) — handle both exactly."""
    out = []
    for p1 in grid:
        d0, d1 = det3(build(p1, F(0))[0]), det3(build(p1, F(1))[0])
        if d0 != d1:
            p2 = d0 / (d0 - d1)
            if kind(*build(p1, p2)) == want: out.append((p1, p2))
        elif d0 == 0:
            out += [(p1, p2) for p2 in grid if kind(*build(p1, p2)) == want]
    return out
