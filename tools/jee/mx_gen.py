"""Practice generators — Mathematics Unit 3: Matrices and Determinants. check() re-solves each item independently:
determinant chains on an actual matrix with cofactor adjoints, linear systems by exact rank tests, counts by brute force."""
import math
from fractions import Fraction as F
from itertools import product
from common import mcq, fr
from mxs import kind, solve2, det3
HALF = [F(k, 2) for k in range(-500, 501)]

def g_adj(rng):
    n = rng.choice([2, 3]); d = rng.choice([-3, -2, 2, 3, 4, 5])
    ops = rng.choice([[('k', 2), ('adj',)], [('adj',), ('k', 3)], [('k', 2), ('adj',), ('k', 3)], [('adj',), ('adj',)], [('k', -1), ('adj',), ('adj',)], [('adj',), ('k', 2), ('adj',)], [('inv',), ('adj',)], [('k', 3), ('inv',)]])
    v, txt = F(d), 'A'
    for op in ops:
        if op[0] == 'k': v *= F(op[1]) ** n; txt = f'{op[1]}{txt}' if txt == 'A' else f'{op[1]}({txt})'
        elif op[0] == 'adj': v = v ** (n - 1); txt = f'adj({txt})'
        else: v = 1 / v; txt = f'({txt})^{{−1}}'
    q = f'A is a square matrix of order {n} with |A| = {d}. The value of |{txt}| is :'
    alts = [v * 2, -v, v ** 2 if abs(v) < 1e6 else v * 4, v / 2, F(d) ** n, v * n]
    o, a = mcq(rng, fr(v), [fr(x) for x in alts if x != v])
    return dict(q=q, o=o, a=a, sol=[f'Order n = {n}: |kA| = k^{{n}}|A|, |adj A| = |A|^{{n−1}}, |A^{{−1}}| = \\f{{1}}{{|A|}}.', f'Work from the inside out → {fr(v)}.'], p=dict(t='chain', n=n, d=d, ops=ops))

def g_sys(rng):
    t = rng.choice(['inf', 'inf', 'none', 'nontriv'])
    while True:
        r1 = [rng.randint(-4, 6) for _ in range(3)]; r2 = [rng.randint(-4, 6) for _ in range(3)]; b1, b2 = rng.randint(-6, 9), rng.randint(-6, 9)
        if sum(1 for i in range(3) for j in range(i + 1, 3) if r1[i] * r2[j] - r1[j] * r2[i] != 0) < 2: continue
        break
    p, q = rng.choice([1, 2, 3, -1]), rng.choice([1, 2, -1, 3])
    r3 = [p * a + q * b for a, b in zip(r1, r2)]; b3 = p * b1 + q * b2
    hide = rng.randint(0, 2); lam = r3[hide]
    o1, o2 = [i for i in range(3) if i != hide]
    if r1[o1] * r2[o2] - r1[o2] * r2[o1] == 0: return g_sys(rng)
    def row3(l): return [l if i == hide else r3[i] for i in range(3)]
    def lin(cs):
        out = ''
        for c, v in zip(cs, 'xyz'):
            if isinstance(c, str): term = c + v; sgn = '+'
            elif c == 0: continue
            else: sgn = '−' if c < 0 else '+'; term = ('' if abs(c) == 1 else str(abs(c))) + v
            out += (('−' if sgn == '−' else '') if not out else f' {sgn} ') + term
        return out or '0'
    def eqs(rows, rhs): return ', '.join(f'{lin(r)} = {str(c).replace("-", "−")}' for r, c in zip(rows, rhs))
    if t == 'inf':
        shown = eqs([r1, r2], [b1, b2]); third = lin(['λ' if i == hide else r3[i] for i in range(3)]) + ' = μ'
        q = f'The system {shown}, {third} has infinitely many solutions. Then λ + μ is ______.'
        return dict(q=q, o=None, a=lam + b3, sol=[f'Equation 3 must be p × (eq 1) + q × (eq 2). Matching the two known coefficients gives p = {p}, q = {q}.', f'Then λ = {lam} and μ = {p} × {b1} + {q} × {b2} = {b3} → λ + μ = {lam + b3}.'],
                    p=dict(t='inf', r1=r1, r2=r2, r3=r3, b=[b1, b2], hide=hide))
    if t == 'none':
        mu = b3 + rng.choice([1, 2, 3, -1, -2])
        third = lin(['λ' if i == hide else r3[i] for i in range(3)]) + f' = {str(mu).replace("-", "−")}'
        q = f'The system {eqs([r1, r2], [b1, b2])}, {third} has NO solution. Then λ is ______.'
        return dict(q=q, o=None, a=lam, sol=['No solution needs the coefficient matrix to be singular (D = 0) while the right side is inconsistent.', f'D = 0 forces equation 3 to be {p} × (eq 1) + {q} × (eq 2) on the left → λ = {lam}; the right side {mu} ≠ {b3}, so it is inconsistent.'],
                    p=dict(t='none', r1=r1, r2=r2, r3=r3, b=[b1, b2], mu=mu, hide=hide))
    rows = [r1, r2, r3]; third = lin(['k' if i == hide else r3[i] for i in range(3)]) + ' = 0'
    q = f'The homogeneous system {eqs([r1, r2], [0, 0])}, {third} has a non-trivial solution. Then k is ______.'
    return dict(q=q, o=None, a=lam, sol=['A homogeneous system has a non-trivial solution exactly when its determinant is 0.', f'D is linear in k; D = 0 gives k = {lam}.'], p=dict(t='hom', r1=r1, r2=r2, r3=r3, hide=hide))

def g_mat(rng):
    t = rng.choice(['sing', 'trace', 'inv', 'prob', 'ch'])
    if t == 'sing':
        S = sorted(rng.sample([1, 2, 3, 4, 6, 8, 9, 12], 4))
        v = sum(1 for a, b, c, d in product(S, repeat=4) if a * d == b * c)
        return dict(q=f'The number of singular 2 × 2 matrices whose entries are from {{{", ".join(map(str, S))}}} is ______.', o=None, a=v,
                    sol=['Singular ⇔ ad = bc.', 'Group the 16 ordered pairs (a, d) by their product; the count is Σ (pairs with that product)^{2}' + f' = {v}.'], p=dict(t='sing', S=S))
    if t == 'trace':
        S = rng.choice([[-1, 0, 1], [-2, -1, 0, 1, 2], [0, 1, 2], [-1, 0, 1, 2]]); r, c = rng.choice([(2, 2), (3, 2), (2, 3), (3, 1)]); k = rng.choice([2, 3, 4, 5])
        v = sum(1 for e in product(S, repeat=r * c) if sum(x * x for x in e) == k)
        if v == 0: return g_mat(rng)
        return dict(q=f'The number of {r} × {c} matrices A with entries from {{{", ".join(map(str, S))}}} such that trace(A^{{T}}A) = {k} is ______.', o=None, a=v,
                    sol=['trace(A^{T}A) = sum of squares of ALL entries.', f'Count the ways to choose entries whose squares add to {k} → {v}.'], p=dict(t='trace', S=S, r=r, c=c, k=k))
    if t == 'inv':
        a, b, c, d = [rng.randint(-4, 6) for _ in range(4)]
        D = a * d - b * c
        if D == 0: return g_mat(rng)
        tr = a + d
        q = f'For A = [[{a}, {b}], [{c}, {d}]], A^{{−1}} = αA + βI. Then α + β is :'
        v = F(-1, D) + F(tr, D)
        o, i = mcq(rng, fr(v), [fr(x) for x in (F(1, D) + F(tr, D), F(-1, D) - F(tr, D), F(tr), F(D), v + 1)])
        return dict(q=q, o=o, a=i, sol=[f'Cayley–Hamilton: A^{{2}} − ({tr})A + ({D})I = 0.', f'Multiply by A^{{−1}}: A^{{−1}} = \\f{{{tr}I − A}}{{{D}}} → α = {fr(F(-1, D))}, β = {fr(F(tr, D))}.', f'α + β = {fr(v)}.'], p=dict(t='inv', A=[a, b, c, d]))
    if t == 'prob':
        S = rng.choice([[0, 1], [0, 1, 2], [-1, 1], [1, 2]])
        good = sum(1 for a, b, c, d in product(S, repeat=4) if a * d != b * c); v = F(good, len(S) ** 4)
        q = f'A 2 × 2 matrix is formed by choosing each entry at random from {{{", ".join(map(str, S))}}}. The probability that it is invertible is :'
        o, i = mcq(rng, fr(v), [fr(x) for x in (1 - v, v / 2, F(1, 2), F(good + 1, len(S) ** 4), F(3, 8), F(5, 8)) if x != v])
        return dict(q=q, o=o, a=i, sol=[f'{len(S) ** 4} matrices in all; invertible ⇔ ad ≠ bc.', f'Counting gives {good} → P = {fr(v)}.'], p=dict(t='prob', S=S))
    k = rng.choice([2, 3, 4])
    q = f'If A is a 3 × 3 matrix with |A| = {k}, then |adj(adj A)| is ______.'
    return dict(q=q, o=None, a=k ** 4, sol=['|adj B| = |B|^{2} for order 3, so |adj(adj A)| = (|A|^{2})^{2} = |A|^{4}.', f'= {k}^{{4}} = {k ** 4}.'], p=dict(t='ch', k=k))

def robust(g):
    def w(rng):
        for _ in range(60):
            try: return g(rng)
            except AssertionError: continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(adj=g_adj, sys=g_sys, mat=g_mat).items()}
def finish(it): return it

# ---------------- independent checks ----------------
def cof_adj(M):
    n = len(M)
    def minor(i, j): return [r[:j] + r[j + 1:] for k, r in enumerate(M) if k != i]
    return [[(-1) ** (i + j) * detL(minor(j, i)) for j in range(n)] for i in range(n)]
def detL(M):
    if len(M) == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * detL([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(len(M)))
def inv(M): d = detL(M); return [[x / d for x in r] for r in cof_adj(M)]
def unfr(s):
    s = s.replace('−', '-')
    if '\\f{' in s: neg = s.startswith('-'); a, b = s.lstrip('-')[3:-1].split('}{'); v = F(int(a), int(b)); return -v if neg else v
    return F(s)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'chain':   # a real matrix with the required determinant, mixed with a unimodular matrix so it is not diagonal
        n, d = p['n'], p['d']
        U = [[1, 2], [1, 3]] if n == 2 else [[1, 2, 0], [0, 1, 3], [1, 2, 1]]
        D = [[F(d) if i == j == 0 else F(int(i == j)) for j in range(n)] for i in range(n)]
        M = [[sum(U[i][k] * D[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        assert detL(M) == d
        for op in p['ops']:
            if op[0] == 'k': M = [[x * op[1] for x in r] for r in M]
            elif op[0] == 'adj': M = cof_adj(M)
            else: M = inv(M)
        return unfr(R) == detL(M)
    if t in ('inf', 'none', 'hom'):
        h = p['hide']
        if t == 'hom':
            ks = [k for k in range(-80, 81) if detL([p['r1'], p['r2'], [k if i == h else p['r3'][i] for i in range(3)]]) == 0]; return ks == [R]
        if t == 'inf':
            sols = solve2(lambda l, m: ([p['r1'], p['r2'], [l if i == h else p['r3'][i] for i in range(3)]], [p['b'][0], p['b'][1], m]), grid=HALF)
            return len(sols) == 1 and R == sols[0][0] + sols[0][1]
        ls = [l for l in range(-80, 81) if kind([p['r1'], p['r2'], [l if i == h else p['r3'][i] for i in range(3)]], [p['b'][0], p['b'][1], p['mu']]) == 'none']; return ls == [R]
    if t == 'sing': return R == sum(1 for e in product(p['S'], repeat=4) if detL([[e[0], e[1]], [e[2], e[3]]]) == 0)
    if t == 'trace':
        cnt = 0
        for e in product(p['S'], repeat=p['r'] * p['c']):
            A = [list(e[i * p['c']:(i + 1) * p['c']]) for i in range(p['r'])]
            if sum(sum(A[k][j] * A[k][j] for k in range(p['r'])) for j in range(p['c'])) == p['k']: cnt += 1
        return R == cnt
    if t == 'inv':
        a, b, c, d = p['A']; A = [[F(a), F(b)], [F(c), F(d)]]; Ai = inv(A)
        for al in [F(x, y) for y in range(1, 40) for x in range(-200, 201)]:
            beta = Ai[0][0] - al * A[0][0]
            if all(Ai[i][j] == al * A[i][j] + (beta if i == j else 0) for i in range(2) for j in range(2)): return unfr(R) == al + beta
        return False
    if t == 'prob': return unfr(R) == F(sum(1 for e in product(p['S'], repeat=4) if e[0] * e[3] != e[1] * e[2]), len(p['S']) ** 4)
    if t == 'ch':
        A = [[F(p['k']), 1, 0], [0, 1, 2], [0, 0, 1]]; return R == detL(cof_adj(cof_adj(A)))
    raise KeyError(t)
