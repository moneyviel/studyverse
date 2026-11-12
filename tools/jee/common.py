"""Shared helpers for JEE unit builds: question registry, option builder, number formatting and an
exact circuit solver (nodal analysis with Fractions) used as an independent checker."""
from fractions import Fraction as F
import math, re
def new_registry():
    P = []
    def add(src, topic, q, o, key, chk, sol, fam=None, diff=2, fig=None):
        y, m, d, sh = src
        P.append(dict(src=dict(y=y, s=m, d=d, sh=sh), t=topic, q=q, o=o, key=key, chk=chk, sol=sol, fam=fam, diff=diff, fig=fig))
    return P, add
def pick(opts, val, tol=1e-9):
    hits = [i + 1 for i, x in enumerate(opts) if (abs(float(x) - float(val)) <= tol * max(1, abs(float(val))) if isinstance(x, (int, float, F)) else x == val)]
    assert len(hits) == 1, (opts, val, hits); return hits[0]
def near(opts, val): return min(range(len(opts)), key=lambda i: abs(opts[i] - val)) + 1
def verify(P):
    for i, p in enumerate(P):
        got = p['chk'](); assert got == p['key'], (i, p['q'][:80], 'code says', got, 'key', p['key'])
        if p['o']: assert 1 <= p['key'] <= len(p['o']) and len(set(p['o'])) == len(p['o']), i
    return len(P)
def nf(x, sig=4):
    if isinstance(x, F): x = float(x)
    if x == 0: return '0'
    s = f'{x:.{sig}g}'
    if 'e' in s: m, e = s.split('e'); return f'{m} × 10^{{{int(e)}}}'
    return s
def fr(x):
    """exact fraction text: 4/5 → \\f{4}{5}, 3 → 3"""
    x = F(x)
    if x.denominator == 1: return str(x.numerator).replace('-', '−')
    return ('−' if x < 0 else '') + f'\\f{{{abs(x.numerator)}}}{{{x.denominator}}}'
def ordn(n): return f'{n}^{{' + ('th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')) + '}'
def mcq(rng, right, wrong, n=4):
    seen, opts = {right}, [right]
    for w in wrong:
        if w not in seen and len(opts) < n: seen.add(w); opts.append(w)
    assert len(opts) == n, ('not enough distinct distractors', right, wrong)
    rng.shuffle(opts); return opts, opts.index(right)

def solve_net(edges, a, b, nodes=None):
    """Equivalent resistance between nodes a and b. edges: [(u, v, R)] with exact Fractions.
    Nodal analysis: inject 1 A at a, take it out at b (grounded), solve G·V = I by Gaussian elimination."""
    ns = sorted({u for u, v, r in edges} | {v for u, v, r in edges}, key=str)
    idx = {n: i for i, n in enumerate(x for x in ns if x != b)}
    N = len(idx); G = [[F(0)] * (N + 1) for _ in range(N)]
    for u, v, r in edges:
        g = 1 / F(r)
        for x, y in ((u, v), (v, u)):
            if x == b: continue
            G[idx[x]][idx[x]] += g
            if y != b: G[idx[x]][idx[y]] -= g
    G[idx[a]][N] += 1
    for c in range(N):
        p = next(r for r in range(c, N) if G[r][c] != 0); G[c], G[p] = G[p], G[c]
        for r in range(N):
            if r != c and G[r][c] != 0:
                f = G[r][c] / G[c][c]; G[r] = [x - f * y for x, y in zip(G[r], G[c])]
    return G[idx[a]][N] / G[idx[a]][idx[a]]

def solve_dc(edges, srcs, gnd):
    """Node voltages for a DC circuit: resistor edges [(u,v,R)] and ideal current-free emf sources modelled as
    (u, v, E, r): a cell from u(−) to v(+) with internal resistance r (Norton equivalent). Returns {node: V}."""
    E2 = list(edges); inj = {}
    for u, v, E, r in srcs:
        E2.append((u, v, r)); I = F(E) / F(r)
        inj[v] = inj.get(v, 0) + I; inj[u] = inj.get(u, 0) - I
    ns = sorted({x for e in E2 for x in e[:2]}, key=str); idx = {n: i for i, n in enumerate(x for x in ns if x != gnd)}
    N = len(idx); G = [[F(0)] * (N + 1) for _ in range(N)]
    for u, v, r in E2:
        g = 1 / F(r)
        for x, y in ((u, v), (v, u)):
            if x == gnd: continue
            G[idx[x]][idx[x]] += g
            if y != gnd: G[idx[x]][idx[y]] -= g
    for n, I in inj.items():
        if n != gnd: G[idx[n]][N] += I
    for c in range(N):
        p = next(r for r in range(c, N) if G[r][c] != 0); G[c], G[p] = G[p], G[c]
        for r in range(N):
            if r != c and G[r][c] != 0:
                f = G[r][c] / G[c][c]; G[r] = [x - f * y for x, y in zip(G[r], G[c])]
    V = {n: G[i][N] / G[i][i] for n, i in idx.items()}; V[gnd] = F(0); return V

# standard networks (each wire / resistor = r)
def tri(r): return [(0, 1, r), (1, 2, r), (2, 0, r)]
def square(r): return [(0, 1, r), (1, 2, r), (2, 3, r), (3, 0, r)]
def tetra(r): return [(i, j, r) for i in range(4) for j in range(i + 1, 4)]
def cube(r):
    V = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    return [(a, b, r) for i, a in enumerate(V) for b in V[i + 1:] if sum(p != q for p, q in zip(a, b)) == 1]
def hexspoke(r): return [(i, (i + 1) % 6, r) for i in range(6)] + [(i, 'c', r) for i in range(6)]
def hexring(r): return [(i, (i + 1) % 6, r) for i in range(6)]
