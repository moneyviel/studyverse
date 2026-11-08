"""Paper 3 Ch 7 — Sets, Relations, Functions, Limits and Continuity: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch07-u01'
C1, C2, C3, C4, C5 = 'Sets, elements and the two ways of writing a set', 'Types of sets', 'Subsets and the power set', "Operations on sets and De Morgan's laws", 'Venn diagrams and counting'
C6, C7, C8, C9, C10 = 'Ordered pairs and the Cartesian product', 'Relations: domain, range, inverse and types', 'Functions (mappings) and their types', 'Limit of a function', 'Continuity at a point'


def S(xs): return '{' + ', '.join(str(x) for x in sorted(xs)) + '}' if xs else 'φ (empty set)'


def union(r):
    a, b = r.randint(10, 80), r.randint(10, 80); c = r.randint(1, min(a, b) - 1); ask = r.choice(['union', 'inter'])
    u = a + b - c
    if ask == 'union':
        return dict(q=f'If n(A) = {a}, n(B) = {b} and n(A ∩ B) = {c}, then n(A ∪ B) =', a=str(u), w=[str(a + b), str(a + b + c), str(abs(a - b) + c), str(u - 1)],
                    ex=f'n(A ∪ B) = n(A) + n(B) − n(A ∩ B) = {a} + {b} − {c} = {u}. The elements in both sets are counted twice when we add n(A) and n(B), so they are subtracted once. Adding only ({a + b}) double-counts the common part.',
                    fast='Add the two sets, subtract the overlap once.', secs=15, d='core', topic=C5, check=str(u), k='ch07.union', data={'a': a, 'b': b, 'c': c, 'ask': 'n(A ∪ B) ='})
    return dict(q=f'If n(A) = {a}, n(B) = {b} and n(A ∪ B) = {u}, then n(A ∩ B) =', a=str(c), w=[str(a + b + u), str(u - a), str(u - b) if u - b != c else str(c + 1), str(a + b - c)],
                ex=f'From n(A ∪ B) = n(A) + n(B) − n(A ∩ B): n(A ∩ B) = {a} + {b} − {u} = {c}. Whenever n(A) + n(B) is more than n(A ∪ B), the excess is exactly the common part counted twice.',
                fast='Overlap = n(A) + n(B) − n(A ∪ B).', secs=15, d='core', topic=C5, check=str(c), k='ch07.union', data={'a': a, 'b': b, 'u': u, 'ask': 'n(A ∩ B) ='})


def neither(r):
    N = r.randint(50, 500); a = r.randint(10, N // 2 + 20); b = r.randint(10, N // 2 + 20); c = r.randint(2, min(a, b) - 1)
    nei = N - (a + b - c)
    if nei < 1: return None
    x, y = r.choice([('tea', 'coffee'), ('cricket', 'football'), ('Hindi newspapers', 'English newspapers'), ('Maths', 'Economics')])
    return dict(q=f'In a group of {N} people, {a} like {x}, {b} like {y} and {c} like both. How many like neither?', a=str(nei), w=[str(N - a - b) if N - a - b > 0 else str(nei + 2 * c), str(N - c), str(a + b - c), str(nei + c)],
                ex=f'People who like at least one = {a} + {b} − {c} = {a + b - c}. Neither = total − at least one = {N} − {a + b - c} = {nei}. Subtracting {a} and {b} from {N} without adding back the {c} who like both removes them twice.',
                fast=f'Neither = {N} − ({a} + {b} − {c}).', secs=25, d='core', topic=C5, check=str(nei), k='ch07.neither', data={'N': N, 'a': a, 'b': b, 'c': c})


def three_sets(r):
    reg = [r.randint(1, 30) for _ in range(7)]   # only A, only B, only C, AB only, BC only, CA only, ABC
    oa, ob, oc, ab, bc, ca, abc = reg
    nA, nB, nC = oa + ab + ca + abc, ob + ab + bc + abc, oc + bc + ca + abc
    nAB, nBC, nCA = ab + abc, bc + abc, ca + abc; u = sum(reg)
    return dict(q=f'n(A) = {nA}, n(B) = {nB}, n(C) = {nC}, n(A ∩ B) = {nAB}, n(B ∩ C) = {nBC}, n(C ∩ A) = {nCA} and n(A ∩ B ∩ C) = {abc}. Then n(A ∪ B ∪ C) =', a=str(u),
                w=[str(nA + nB + nC), str(nA + nB + nC - nAB - nBC - nCA), str(u + abc), str(u - abc)],
                ex=f'n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A ∩ B) − n(B ∩ C) − n(C ∩ A) + n(A ∩ B ∩ C) = {nA + nB + nC} − {nAB + nBC + nCA} + {abc} = {u}. The triple overlap is added three times, subtracted three times, so it must be added back once.',
                fast='Add singles, subtract pairs, add the triple.', secs=35, d='moderate', topic=C5, check=str(u), k='ch07.three', data={'n': [nA, nB, nC, nAB, nBC, nCA, abc]})


WORDS = ['ACCOUNTANCY', 'STATISTICS', 'COMMERCE', 'ECONOMICS', 'TAXATION', 'BALANCESHEET', 'FINANCE', 'MANAGEMENT', 'AUDITING', 'BUSINESS']


def power_set(r):
    w = r.choice(WORDS); k = len(set(w)); kind = r.choice(['subsets', 'proper'])
    if k > 9: return None
    v = 2 ** k - (1 if kind == 'proper' else 0)
    return dict(q=f'A is the set of letters of the word "{w}". The number of {"subsets" if kind == "subsets" else "proper subsets"} of A is:', a=inr(v),
                w=[inr(2 ** len(w) - (1 if kind == 'proper' else 0)), inr(2 ** k - (0 if kind == 'proper' else 1)), inr(2 ** (k - 1)), inr(k * k)],
                ex=f'A set lists each element once, so A has the {k} distinct letters {S(set(w)).replace("{", "{").replace("}", "}")}, not {len(w)}. A set with n elements has 2ⁿ subsets' + (f' and 2ⁿ − 1 proper subsets (all except A itself). So 2^{k} − 1 = {inr(v)}.' if kind == 'proper' else f'. So 2^{k} = {inr(v)}.'),
                fast='Count distinct letters first, then 2ⁿ (minus 1 for proper subsets).', secs=30, d='core', topic=C3, check=str(v), k='ch07.power', data={'w': w, 'kind': kind})


def cartesian(r):
    m, n = r.randint(2, 6), r.randint(2, 5); kind = r.choice(['prod', 'rel'])
    if kind == 'prod':
        v = m * n
        return dict(q=f'If A has {m} elements and B has {n} elements, the number of elements in A × B is:', a=str(v), w=[str(m + n), inr(2 ** v) if 2 ** v < 10 ** 6 else str(v + 1), str(m ** n), str(n ** m) if n ** m != m ** n else str(v + 2)],
                    ex=f'A × B is the set of all ordered pairs (a, b) with a from A and b from B. Each of the {m} elements of A pairs with each of the {n} elements of B, so n(A × B) = {m} × {n} = {v}. Order inside a pair matters, but the count is still the product.',
                    fast='n(A × B) = n(A) × n(B).', secs=15, d='core', topic=C6, check=str(v), k='ch07.cart', data={'m': m, 'n': n, 'kind': 'elements in A × B'})
    v = 2 ** (m * n)
    return dict(q=f'If A has {m} elements and B has {n} elements, the number of relations from A to B is:', a=inr(v), w=[inr(m * n), inr(2 ** (m + n)), inr((m * n) ** 2), inr(2 ** (m * n) - 1)],
                ex=f'A relation from A to B is any subset of A × B. A × B has {m} × {n} = {m * n} ordered pairs, so the number of subsets (relations) is 2^{m * n} = {inr(v)}. This count includes the empty relation and A × B itself.',
                fast='Relations = 2^(mn): every ordered pair is either in or out.', secs=20, d='moderate', topic=C7, check=str(v), k='ch07.cart', data={'m': m, 'n': n, 'kind': 'relations from A to B'})


def isprime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))


def builder(r):
    a = r.randint(1, 60); b = a + r.randint(10, 60); kind = r.choice(['prime', 'square', 'mult'])
    if kind == 'prime': xs = [x for x in range(a + 1, b) if isprime(x)]; desc = 'x is a prime number'
    elif kind == 'square': xs = [x for x in range(a + 1, b) if math.isqrt(x) ** 2 == x]; desc = 'x is a perfect square'
    else: k = r.choice([3, 4, 6, 7]); xs = [x for x in range(a + 1, b) if x % k == 0]; desc = f'x is a multiple of {k}'
    v = len(xs)
    if v < 2: return None
    return dict(q=f'How many members does {{x : {desc} and {a} < x < {b}}} have?', a=str(v), w=[str(v + 1), str(v - 1), str(v + 2), str(b - a - 1)],
                ex=f'Write the set in roster form: {S(xs)}. The strict signs exclude {a} and {b} themselves. Counting gives {v} elements. Listing the members is the safest way to avoid including or dropping an end value.',
                fast='List the members quickly in roster form and count; watch whether the end values are included.', secs=40, d='core', topic=C1, check=str(v), k='ch07.builder', data={'a': a, 'b': b, 'desc': desc})


def ops(r):
    U_ = list(range(1, 13)); A = set(r.sample(U_, r.randint(4, 7))); B = set(r.sample(U_, r.randint(4, 7)))
    kind = r.choice(['A − B', 'B − A', 'A Δ B (symmetric difference)', "(A ∪ B)′ with U = {1, 2, …, 12}"])
    res = {'A − B': A - B, 'B − A': B - A, 'A Δ B (symmetric difference)': A ^ B, "(A ∪ B)′ with U = {1, 2, …, 12}": set(U_) - (A | B)}[kind]
    if not res or len(res) == len(U_): return None
    w = [A & B, A | B, (B - A) if kind != 'B − A' else (A - B), set(U_) - (A & B)]
    return dict(q=f'If A = {S(A)} and B = {S(B)}, then {kind} is:', a=S(res), w=[S(x) for x in w],
                ex=f'A − B keeps elements of A that are not in B; A Δ B = (A − B) ∪ (B − A); the complement (A ∪ B)′ keeps elements of U outside both sets, which by De Morgan equals A′ ∩ B′. Applying the definition element by element gives {S(res)}.',
                fast='Go through the elements one by one and tick membership in A and B; keep those the operation asks for.', secs=40, d='core', topic=C4,
                k='ch07.ops', data={'A': S(A), 'B': S(B), 'kind': kind})


PROPS = ['reflexive', 'symmetric', 'transitive']


def relprops(R, X):
    ref = all((x, x) in R for x in X); sym = all((b, a) in R for a, b in R); tra = all((a, d) in R for a, b in R for c, d in R if b == c)
    return ref, sym, tra


def describe(p):
    ref, sym, tra = p
    if all(p): return 'An equivalence relation'
    if not any(p): return 'Neither reflexive, symmetric nor transitive'
    yes = [n for n, v in zip(PROPS, p) if v]; no = [n for n, v in zip(PROPS, p) if not v]
    return (('' if not yes else ' and '.join(yes).capitalize() + ' but ') + ('not ' if yes else 'Not ') + ' or '.join(no)).replace('  ', ' ')


def reltype(r):
    X = [1, 2, 3]; pairs = [(a, b) for a in X for b in X]
    R = set(p for p in pairs if r.random() < .45)
    if not R: return None
    p = relprops(R, X); ans = describe(p)
    others = set()
    import itertools
    for q in itertools.product([True, False], repeat=3):
        if q != p: others.add(describe(q))
    w = sorted(others); r.shuffle(w)
    Rs = '{' + ', '.join(f'({a}, {b})' for a, b in sorted(R)) + '}'
    why = []
    why.append('every (x, x) is present' if p[0] else 'some (x, x) is missing, so it is not reflexive')
    why.append('every pair has its reverse' if p[1] else 'some (a, b) has no (b, a), so it is not symmetric')
    why.append('whenever (a, b) and (b, c) are present, (a, c) is too' if p[2] else 'some (a, b), (b, c) lack (a, c), so it is not transitive')
    return dict(q=f'On the set {{1, 2, 3}}, the relation R = {Rs} is:', a=ans, w=w,
                ex=f'Check the three properties one at a time. Reflexive: {why[0]}. Symmetric: {why[1]}. Transitive: {why[2]}. Hence R is: {ans.lower()}. An equivalence relation needs all three properties.',
                fast='Check (1,1),(2,2),(3,3) first; then reverse each pair; then chain pairs end-to-start.', secs=60, d='hard', topic=C7, k='ch07.reltype', data={'R': [list(x) for x in sorted(R)]})


def compose(r):
    a, b = r.randint(-5, 6), r.randint(-9, 9); c, d_ = r.randint(1, 4), r.randint(-6, 6); x0 = r.randint(-4, 5); order = r.choice(['fog', 'gof'])
    if a == 0: return None
    f = lambda x: a * x + b; g = lambda x: c * x * x + d_
    v = f(g(x0)) if order == 'fog' else g(f(x0))
    other = g(f(x0)) if order == 'fog' else f(g(x0))
    if v == other: return None
    lbl = 'f(g(' if order == 'fog' else 'g(f('
    return dict(q=f'If f(x) = {poly([a, b])} and g(x) = {poly([c, 0, d_])}, then {lbl}{x0})) =', a=str(v), w=[str(other), str(f(x0) * g(x0)), str(f(x0) + g(x0)), str(v + 1)],
                ex=f'Work from the inside out. ' + (f'g({x0}) = {g(x0)}, then f({g(x0)}) = {v}.' if order == 'fog' else f'f({x0}) = {f(x0)}, then g({f(x0)}) = {v}.') + f' Composition is generally not commutative: the other order gives {other}. Multiplying f({x0}) and g({x0}) is not composition at all: in a composition the output of one function becomes the input of the other.',
                fast='Evaluate the inner function first, then feed the result to the outer one.', secs=30, d='core', topic=C8, check=str(v), k='ch07.compose', data={'f': [a, b], 'g': [c, d_], 'x0': x0, 'order': lbl})


def inverse(r):
    a = r.choice([2, 3, 4, 5, -2, -3]); b = r.randint(-10, 10); y = r.randint(-20, 30)
    x = F(y - b, a)
    return dict(q=f'If f(x) = {poly([a, b])}, then f⁻¹({y}) =', a=fr(x), w=[fr(F(a * y + b)), fr(F(y + b, a)), fr(F(1, a * y + b)) if a * y + b else fr(x + 1), fr(-x) if x else fr(x + 2)],
                ex=f'f⁻¹({y}) is the x for which f(x) = {y}. Solve {poly([a, b])} = {y}: {a}x = {y} − ({b}) = {y - b}, so x = {fr(x)}. In general f⁻¹(y) = (y − {b})/{a}. Computing f({y}) instead of solving f(x) = {y} is the usual mix-up.',
                fast=f'Back-substitute options into f: f({fr(x)}) = {y}.', secs=25, d='core', topic=C8, check=frx(x), k='ch07.inverse', data={'a': a, 'b': b, 'y': y})


def lim_power(r):
    n = r.randint(2, 7); a = r.choice([1, 2, 3, -1, -2]); v = n * a ** (n - 1)
    an = a ** n
    return dict(q=f'The value of lim (x → {a}) (x{sup(n)} − {an if an >= 0 else "(" + str(an) + ")"})/(x − {a if a >= 0 else "(" + str(a) + ")"}) is:', a=str(v), w=[str(a ** (n - 1)), str(n * a ** n), str((n - 1) * a ** (n - 1)), str(0)],
                ex=f'Direct substitution gives 0/0. Use the standard limit lim (x → a) (xⁿ − aⁿ)/(x − a) = n·aⁿ⁻¹. With n = {n} and a = {a}: {n} × ({a})^{n - 1} = {v}. Answering 0 confuses the indeterminate form 0/0 with the limit itself.',
                fast='n·aⁿ⁻¹ — it is the derivative of xⁿ at x = a.', secs=20, d='core', topic=C9, check=str(v), k='ch07.limpow', data={'n': n, 'a': a})


def lim_factor(r):
    p, q_ = r.sample(range(-6, 8), 2)
    if p == q_: return None
    c2 = r.choice([1, 2, 3])
    # (c2 x^2 - c2(p+q) x + c2 p q)/(x - p) -> c2 (p - q)
    v = c2 * (p - q_)
    num_ = poly([c2, -c2 * (p + q_), c2 * p * q_]); den = poly([1, -p])
    return dict(q=f'lim (x → {p}) ({num_})/({den}) =', a=str(v), w=[str(c2 * (p + q_)), str(-v), str(0) if v != 0 else str(1), str(c2 * p * q_) if c2 * p * q_ != v else str(v + 2)],
                ex=f'At x = {p} both numerator and denominator are 0, so factorise: {num_} = {c2 if c2 > 1 else ""}({den})({poly([1, -q_])}). Cancel ({den}) and substitute x = {p}: {c2 if c2 > 1 else 1} × ({p} − ({q_})) = {v}.',
                fast='Factor out (x − a) and substitute; or differentiate top and bottom (derivative of the numerator at x = a).', secs=40, d='moderate', topic=C9, check=str(v), k='ch07.limfac', data={'num': num_, 'p': p})


def lim_inf(r):
    a, b, c = r.randint(1, 9), r.randint(-9, 9), r.randint(-9, 9); d_, e, f = r.randint(1, 9), r.randint(-9, 9), r.randint(-9, 9)
    deg = r.choice([2, 3]); v = F(a, d_)
    top = poly([a, b, c] if deg == 2 else [a, 0, b, c]); bot = poly([d_, e, f] if deg == 2 else [d_, e, 0, f])
    return dict(q=f'lim (x → ∞) ({top})/({bot}) =', a=fr(v), w=[fr(F(c, f)) if f and F(c, f) != v else '∞', fr(F(d_, a)) if F(d_, a) != v else '0', '0' if v != 0 else '1', '1' if v != 1 else fr(F(b, e)) if e else '2'],
                ex=f'Divide numerator and denominator by the highest power x{sup(deg)}. Every term with a lower power tends to 0 as x → ∞, leaving the ratio of leading coefficients {a}/{d_} = {fr(v)}. The constant terms decide the limit at x → 0, not at infinity.',
                fast='Same degree on top and bottom ⇒ ratio of leading coefficients.', secs=20, d='core', topic=C9, k='ch07.liminf', data={'top': top, 'bot': bot})


def continuity(r):
    a = r.randint(-6, 8); kind = r.choice(['removable', 'piece'])
    if kind == 'removable':
        if a == 0: return None
        k = 2 * a
        sq = a * a
        return dict(q=f'f(x) = (x² − {sq})/(x {"−" if a > 0 else "+"} {abs(a)}) for x ≠ {a}, and f({a}) = k. For f to be continuous at x = {a}, k =', a=str(k), w=[str(a), str(sq), str(0), str(-k)],
                    ex=f'Continuity at x = {a} needs f({a}) = lim (x → {a}) f(x). For x ≠ {a}, (x² − {sq})/(x {"−" if a > 0 else "+"} {abs(a)}) = x {"+" if a > 0 else "−"} {abs(a)}, so the limit is {a} + ({a}) = {k}. Hence k = {k}. Leaving k undefined or 0 creates a hole in the graph.',
                    fast='Cancel the common factor and substitute x = a: the limit is 2a.', secs=30, d='core', topic=C10, check=str(k), k='ch07.cont', data={'sq': sq, 'a': a, 'kind': 'removable'})
    p, s, c = r.randint(1, 6), r.randint(-5, 5), r.randint(-4, 4); q_ = r.randint(-10, 10)
    # f = p x + q (x < c), s x + k (x >= c): continuity  p c + q = s c + k  -> k
    k = p * c + q_ - s * c
    return dict(q=f'f(x) = {poly([p, q_])} for x < {c} and f(x) = {poly([s, 0]) if s else ""} + k for x ≥ {c}. If f is continuous at x = {c}, then k ='.replace(' 0 + k', ' k').replace('=  + k', '= k'), a=str(k), w=[str(q_), str(-k) if k else str(k + 1), str(p * c + q_), str(k + s)],
                ex=f'Left-hand limit at x = {c}: {p}({c}) + ({q_}) = {p * c + q_}. Right-hand value: {s}({c}) + k = {s * c} + k. Continuity needs them equal: {s * c} + k = {p * c + q_}, so k = {k}. Both pieces must meet at the same point.',
                fast='Put x = c in both pieces and equate.', secs=35, d='moderate', topic=C10, check=str(k), k='ch07.cont', data={'p': p, 'q': q_, 's': s, 'c': c, 'kind': 'piece'})


def nfunctions(r):
    m, n = r.randint(2, 5), r.randint(2, 6); kind = r.choice(['all', 'oneone'])
    if kind == 'oneone' and m > n: return None
    v = n ** m if kind == 'all' else math.perm(n, m)
    return dict(q=f'If A has {m} elements and B has {n} elements, the number of {"functions" if kind == "all" else "one-one (injective) functions"} from A to B is:', a=inr(v),
                w=[inr(m ** n), inr(2 ** (m * n)), inr(n ** m - n if kind == 'all' else n ** m), inr(m * n)],
                ex=(f'Each of the {m} elements of A must go to exactly one of the {n} elements of B, independently: {n} choices each, so {n}^{m} = {inr(v)} functions.' if kind == 'all' else
                    f'One-one: different elements of A need different images. The first element has {n} choices, the next {n - 1}, and so on: ⁿPₘ = {n}P{m} = {inr(v)}.') + ' Writing m^n reverses the roles of domain and co-domain.',
                fast=('(size of B)^(size of A)' if kind == 'all' else 'ⁿPₘ: falling product starting at n(B)') + ' — think "each element of A chooses".', secs=25, d='moderate', topic=C8, check=str(v), k='ch07.nfun', data={'m': m, 'n': n, 'kind': kind})


def rel_range(r):
    A = sorted(r.sample(range(-3, 10), r.randint(4, 6))); a, b = r.choice([2, 3, -1, 1]), r.randint(-5, 5)
    rng = sorted({a * x + b for x in A}); dom = A
    kind = r.choice(['range', 'inverse'])
    if kind == 'range':
        return dict(q=f'R = {{(x, y) : y = {poly([a, b])}, x ∈ {S(A)}}}. The range of R is:', a=S(rng), w=[S(A), S(sorted({x + b for x in A})), S(sorted({a * x for x in A})), S(sorted({(x - b) // a if a else x for x in A}))],
                    ex=f'The range is the set of second elements. Substitute each x: ' + ', '.join(f'{x} → {a * x + b}' for x in A) + f'. So the range is {S(rng)}. The set {S(A)} itself is the domain, not the range.',
                    fast='Apply the rule to each element of the domain and collect the outputs.', secs=30, d='core', topic=C7, k='ch07.range', data={'A': S(A), 'a': a, 'b': b})
    pairs = [(x, a * x + b) for x in A[:3]]
    inv = '{' + ', '.join(f'({y}, {x})' for x, y in pairs) + '}'
    Rs = '{' + ', '.join(f'({x}, {y})' for x, y in pairs) + '}'
    wrong1 = '{' + ', '.join(f'({-x}, {-y})' for x, y in pairs) + '}'
    wrong2 = '{' + ', '.join(f'({x}, {x})' for x, y in pairs) + '}'
    wrong3 = '{' + ', '.join(f'({y}, {y})' for x, y in pairs) + '}'
    if len({inv, Rs, wrong1, wrong2, wrong3}) < 5: return None
    return dict(q=f'If R = {Rs}, then R⁻¹ is:', a=inv, w=[Rs, wrong1, wrong2, wrong3],
                ex=f'The inverse relation R⁻¹ is obtained by swapping the two entries of every ordered pair in R. So R⁻¹ = {inv}. The domain of R becomes the range of R⁻¹ and the range of R becomes the domain of R⁻¹.',
                fast='Swap each pair (a, b) → (b, a).', secs=15, d='core', topic=C7, k='ch07.relinv', data={'R': Rs})


BANKS = {U: [(union, 2), (neither, 2), (three_sets, 2), (power_set, 2), (cartesian, 2), (builder, 2), (ops, 2), (reltype, 3), (compose, 2), (inverse, 2),
             (lim_power, 2), (lim_factor, 2), (lim_inf, 2), (continuity, 2), (nfunctions, 2), (rel_range, 2)]}
