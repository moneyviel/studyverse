"""Practice generators — Mathematics Unit 1: Sets, Relations and Functions. check() re-solves every item by brute force:
relations by listing all pairs and testing each property, counting questions by enumerating the functions, domains
and ranges by scanning the real line, functional equations by substituting back."""
import itertools, math
from fractions import Fraction as F
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    return float(F(s)) if '/' in s else float(s.split(' ')[0])
def grid(lo, hi, n): return [lo + (hi - lo) * i / (n - 1) for i in range(n)]
def props(X, R):
    return all((a, a) in R for a in X), all((b, a) in R for (a, b) in R), all((a, d) in R for (a, b) in R for (c, d) in R if b == c)
def bell(n):
    row = [1]
    for _ in range(n): nr = [row[-1]]; [nr.append(nr[-1] + x) for x in row]; row = nr
    return row[0]
PROPS = ['reflexive, symmetric and transitive (an equivalence)', 'reflexive and symmetric but not transitive', 'reflexive and transitive but not symmetric', 'symmetric and transitive but not reflexive',
         'reflexive only', 'symmetric only', 'transitive only', 'none of the three']
def pname(r, s, t):
    return {(1, 1, 1): PROPS[0], (1, 1, 0): PROPS[1], (1, 0, 1): PROPS[2], (0, 1, 1): PROPS[3], (1, 0, 0): PROPS[4], (0, 1, 0): PROPS[5], (0, 0, 1): PROPS[6], (0, 0, 0): PROPS[7]}[(int(r), int(s), int(t))]
RULES = {   # name: (text, test)
    'lin': ('{a}x − y ∈ {{0, {b}}}', lambda a, b: lambda x, y: a * x - y in (0, b)),
    'le': ('{a}x + y ≤ {b}', lambda a, b: lambda x, y: a * x + y <= b),
    'max': ('y = max{{x, {a}}}', lambda a, b: lambda x, y: y == max(x, a)),
    'mod': ('|x − y| is a multiple of {a}', lambda a, b: lambda x, y: abs(x - y) % a == 0),
    'sum': ('x + y ≤ {b}', lambda a, b: lambda x, y: x + y <= b),
    'prod': ('{b} + xy > 0', lambda a, b: lambda x, y: b + x * y > 0),
    'div': ('x divides y', lambda a, b: lambda x, y: x != 0 and y % x == 0),
    'lt': ('x < y', lambda a, b: lambda x, y: x < y)}

def g_rel(rng):
    t = rng.choice(['r_lmn', 'r_lmn', 'r_prop', 'r_count', 'r_pairs', 'r_lattice'])
    if t in ('r_lmn', 'r_prop'):
        rule = rng.choice(list(RULES)); lo, hi = rng.choice([(-3, 3), (-2, 3), (-2, 4), (0, 5), (1, 6), (2, 9), (0, 9)]); a, b = rng.choice([2, 3]), rng.choice([1, 2, 3, 4])
        if rule == 'div': lo = max(lo, 1)
        X = list(range(lo, hi + 1)); R = {(x, y) for x in X for y in X if RULES[rule][1](a, b)(x, y)}; need(len(R) > 0)
        txt = RULES[rule][0].format(a=a, b=b); Atxt = '{' + ', '.join(str(x) for x in X) + '}'
        if t == 'r_prop':
            right = pname(*props(X, R)); o, an = mcq(rng, right, [p for p in PROPS if p != right])
            return dict(q=f'On A = {Atxt}, xRy if and only if {txt}. Then R is', o=o, a=an, sol=['Test each property on the actual pairs.', f'R is {right}.'], p=dict(t=t, rule=rule, X=X, a=a, b=b))
        ask = rng.choice(['lmn', 'lm', 'ln']); l = len(R); m = sum(1 for x in X if (x, x) not in R); n = sum(1 for (x, y) in R if (y, x) not in R)
        val = l + (m if 'm' in ask else 0) + (n if 'n' in ask else 0)
        what = {'lmn': 'l + m + n', 'lm': 'l + m', 'ln': 'l + n'}[ask]
        return dict(q=f'On A = {Atxt}, xRy if and only if {txt}. Let l = n(R), and let m and n be the fewest pairs to add to make R reflexive and symmetric respectively. Then {what} = ____.', o=None, a=val,
                    sol=['List R; m = diagonal pairs missing; n = pairs whose reverse is missing.', f'l = {l}, m = {m}, n = {n} → {val}.'], p=dict(t=t, rule=rule, X=X, a=a, b=b, ask=ask))
    if t == 'r_count':
        n, kind = rng.choice([2, 3, 4, 5]), rng.choice(['reflexive', 'symmetric', 'reflexive and symmetric', 'equivalence', 'all'])
        val = {'reflexive': 2 ** (n * n - n), 'symmetric': 2 ** (n * (n + 1) // 2), 'reflexive and symmetric': 2 ** (n * (n - 1) // 2), 'equivalence': bell(n), 'all': 2 ** (n * n)}[kind]
        need(val < 10 ** 7)
        return dict(q=f'The number of {"" if kind == "all" else kind + " "}relations on a set with {n} elements is ____.', o=None, a=val,
                    sol=['Diagonal pairs are forced for "reflexive"; symmetric relations choose unordered pairs; equivalences ↔ partitions.', f'= {val}.'], p=dict(t=t, n=n, kind=kind))
    if t == 'r_pairs':
        A = sorted(rng.sample(range(1, 10), 4)); B = sorted(rng.sample(range(2, 12), 4)); op = rng.choice(['sum', 'diff'])
        X = [(a, b) for a in A for b in B]; val = sum(1 for p in X for q in X if (p[0] + q[0] == p[1] + q[1] if op == 'sum' else p[0] - q[0] == p[1] - q[1])); need(val > 0)
        cond = 'a_{1} + a_{2} = b_{1} + b_{2}' if op == 'sum' else 'a_{1} − a_{2} = b_{1} − b_{2}'
        return dict(q=f'A = {{{", ".join(map(str, A))}}}, B = {{{", ".join(map(str, B))}}}. On A × B, (a_{{1}}, b_{{1}})R(a_{{2}}, b_{{2}}) iff {cond}. The number of elements in R is ____.', o=None, a=val,
                    sol=['Count the matching sums (or differences) of A with A and of B with B, and multiply the counts value by value.', f'= {val}.'], p=dict(t=t, A=A, B=B, op=op))
    a, b, c = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3]), rng.choice([10, 13, 17, 20, 25, 30, 36, 52]); val = sum(1 for x in range(-10, 11) for y in range(-10, 11) if a * x * x + b * y * y < c)
    return dict(q=f'The number of elements in R = {{(x, y) : {a if a > 1 else ""}x^{{2}} + {b if b > 1 else ""}y^{{2}} < {c}, x, y ∈ Z}} is ____.', o=None, a=val,
                sol=['For each integer x with ax^{2} < c, count the integers y that fit.', f'Total = {val}.'], p=dict(t='r_lattice', a=a, b=b, c=c))

def g_dom(rng):
    t = rng.choice(['d_quad', 'd_trig', 'd_log', 'd_rat', 'd_logq'])
    if t == 'd_quad':
        p, q = sorted(rng.sample(range(-6, 9), 2)); need(q > 0)   # 1/√(−(x−p)(x−q)) + 1/√(x + |x|) → (max(p,0), q)
        a = max(p, 0); b = q; k = rng.choice([1, 2]); val = (k + a) ** 2 + b * b
        S, P = p + q, p * q
        return dict(q=f'If the domain of f(x) = \\f{{1}}{{√{{{-P} + {S}x − x^{{2}}}}}} + \\f{{1}}{{√{{x + |x|}}}} is (a, b), then ({k} + a)^{{2}} + b^{{2}} = ____.'.replace('+ -', '− ').replace('+ 0x', ''), o=None, a=val,
                    sol=[f'{-P} + {S}x − x^{{2}} > 0 → {p} < x < {q}; x + |x| > 0 → x > 0.'.replace('+ -', '− '), f'(a, b) = ({a}, {b}) → {val}.'], p=dict(t=t, p=p, q=q, k=k))
    if t == 'd_trig':
        c, k = rng.choice([3, 4, 5, 6, 7, 9]), rng.choice([2, 3, 5]); lo, hi = F(1, c + 1), F(1, c - 1)
        right = f'[{lo}, {hi}]'; o, a = mcq(rng, right, [f'[{x}, {y}]' for x, y in ((F(1, c), F(1, c - 1)), (F(1, c + 1), F(1, c)), (F(1, c + 2), F(1, c - 2)), (F(-1, c + 1), F(1, c - 1)))])
        return dict(q=f'The range of f(x) = \\f{{1}}{{{c} − sin {k}x}}, x ∈ R, is', o=o, a=a, sol=[f'sin {k}x ∈ [−1, 1] → denominator ∈ [{c - 1}, {c + 1}].', f'Range {right}.'], p=dict(t=t, c=c, k=k))
    if t == 'd_log':
        r1, r2 = sorted(rng.sample(range(1, 15), 2)); base = rng.choice([2, 3, 5, 7]); val = r1 * r1 + r2 * r2
        return dict(q=f'If the domain of log_{{{base}}}({r1 + r2}x − x^{{2}} − {r1 * r2}) is (α, β), then α^{{2}} + β^{{2}} = ____.', o=None, a=val,
                    sol=[f'Need x^{{2}} − {r1 + r2}x + {r1 * r2} < 0 → {r1} < x < {r2}.', f'α^{{2}} + β^{{2}} = {val}.'], p=dict(t=t, r1=r1, r2=r2, base=base))
    if t == 'd_rat':
        p, q = sorted(rng.sample(range(-3, 5), 2)); k = rng.choice([x for x in range(-6, 8) if x not in (p, q)])
        s, Pp = p + q, p * q; D = s * s - 4 * Pp; y1y2 = F(1, D); ysum = F(2 * s - 4 * k, D); val = ysum * ysum - 2 * y1y2
        need(val.denominator == 1)
        return dict(q=f'The range of f(x) = \\f{{{k} − x}}{{(x − {p})(x − {q})}} is (−∞, α] ∪ [β, ∞). Then α^{{2}} + β^{{2}} = ____.'.replace('− -', '+ ').replace('(x − 0)', 'x'), o=None, a=int(val),
                    sol=['y(x^{2} − (p + q)x + pq) = k − x must have a real x: its discriminant in x must be ≥ 0.', f'α, β are the roots of {D}y^{{2}} + ({4 * k - 2 * s})y + 1 = 0 → α^{{2}} + β^{{2}} = {val}.'], p=dict(t=t, p=p, q=q, k=k))
    r1, r2, b = rng.choice([(2, 3), (3, 6), (2, 7), (1, 4), (3, 5)]) + (rng.choice([4, 2, 3]),)   # log_7(1 − log_b(quadratic)) style
    S, Pq = r1 + r2, r1 * r2
    # domain: (x−r1)(x−r2) > 0 and (x−r1)(x−r2) < b → endpoints: roots of x²−Sx+Pq−b
    disc = S * S - 4 * (Pq - b); need(disc > 0)
    e1, e2 = (S - math.sqrt(disc)) / 2, (S + math.sqrt(disc)) / 2; val = e1 + r1 + r2 + e2
    need(abs(val - round(val)) < 1e-9)
    return dict(q=f'If the domain of f(x) = log_{{7}}(1 − log_{{{b}}}(x^{{2}} − {S}x + {Pq})) is (α, β) ∪ (γ, δ), then α + β + γ + δ = ____.', o=None, a=round(val),
                sol=[f'Need x^{{2}} − {S}x + {Pq} > 0 (x < {r1} or x > {r2}) and < {b}.', f'The four end points add to {round(val)}.'], p=dict(t='d_logq', r1=r1, r2=r2, b=b))

FT = {   # name: (formula text, f, domain sample, codomain text, one-one?, onto?)
    'lin': ('3x + 2', lambda x: 3 * x + 2, 'R'),
    'cube': ('x^{3} + x', lambda x: x ** 3 + x, 'R'),
    'sq': ('x^{2} + 1', lambda x: x * x + 1, 'R'),
    'frac': ('\\f{x}{1 + |x|}', lambda x: x / (1 + abs(x)), 'R'),
    'exp': ('e^{x}', lambda x: math.exp(min(x, 50)), 'R'),
    'rat': ('\\f{x^{2} − 1}{x^{2} + 1}', lambda x: (x * x - 1) / (x * x + 1), 'R'),
    'sin': ('x + sin x', lambda x: x + math.sin(x), 'R'),
    'abs': ('|x| + x', lambda x: abs(x) + x, 'R'),
    'cos': ('x^{2} − 4x', lambda x: x * x - 4 * x, 'R')}
TYPES = ['one-one and onto', 'one-one but not onto', 'onto but not one-one', 'neither one-one nor onto']
def classify(f):
    xs = grid(-60, 60, 24001); v = [f(x) for x in xs]; d = [b - a for a, b in zip(v, v[1:])]
    inj = all(x > 0 for x in d) or all(x < 0 for x in d); sur = max(v) > 50 and min(v) < -50
    return TYPES[{(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}[(int(inj), int(sur))]]
def g_ftype(rng):
    t = rng.choice(['t_type', 't_inv', 't_comp', 't_iter'])
    if t == 't_type':
        k = rng.choice(list(FT)); txt, f, _ = FT[k]; right = classify(f); o, a = mcq(rng, right, [x for x in TYPES if x != right])
        return dict(q=f'The function f : R → R, f(x) = {txt}, is', o=o, a=a, sol=['One-one: strictly monotonic. Onto R: every real value is reached.', f'f is {right}.'], p=dict(t=t, k=k))
    if t == 't_inv':
        c = [rng.randint(1, 3), rng.randint(0, 3), rng.randint(1, 4), rng.randint(-3, 3)]   # c0 x^5 + c1 x^3 + c2 x + c3
        x0 = rng.choice([0, 1, 2, -1]); f = lambda x: c[0] * x ** 5 + c[1] * x ** 3 + c[2] * x + c[3]; df = 5 * c[0] * x0 ** 4 + 3 * c[1] * x0 ** 2 + c[2]; y0 = f(x0); ask = rng.choice(['g', 'ratio'])
        val = F(1, df) if ask == 'g' else F(x0) * df; need(ask == 'g' or x0 != 0)
        right = str(val); o, a = mcq(rng, right, [str(z) for z in (F(df), -val, val * 2, F(1, df + 1), F(x0)) if z != val])
        poly = f'{c[0] if c[0] > 1 else ""}x^{{5}}' + (f' + {c[1] if c[1] > 1 else ""}x^{{3}}' if c[1] else '') + f' + {c[2] if c[2] > 1 else ""}x' + (f' {"+" if c[3] > 0 else "−"} {abs(c[3])}' if c[3] else '')
        return dict(q=f'f(x) = {poly} and g is its inverse (g(f(x)) = x). {"g′(" + str(y0) + ")" if ask == "g" else "g(" + str(y0) + ") / g′(" + str(y0) + ")"} equals', o=o, a=a,
                    sol=[f'f({x0}) = {y0} → g({y0}) = {x0}.', f'g′({y0}) = \\f{{1}}{{f′({x0})}} = \\f{{1}}{{{df}}} → {right}.'], p=dict(t=t, c=c, x0=x0, ask=ask))
    if t == 't_comp':
        a, b, c, d, x = rng.randint(1, 5), rng.randint(-5, 5), rng.randint(1, 5), rng.randint(-5, 5), rng.randint(-3, 4); which = rng.choice(['fog', 'gof'])
        val = (a * (c * x + d) + b) if which == 'fog' else (c * (a * x + b) + d)
        return dict(q=f'f(x) = {a}x {"+" if b >= 0 else "−"} {abs(b)} and g(x) = {c}x {"+" if d >= 0 else "−"} {abs(d)}. ({which[0]}o{which[2]})({x}) = ____.', o=None, a=val,
                    sol=[f'({which[0]}o{which[2]})(x) = {which[0]}({which[2]}(x)).', f'= {val}.'], p=dict(t=t, a=a, b=b, c=c, d=d, x=x, which=which))
    k, n = rng.choice([2, 3, 4]), rng.choice([2, 3, 4, 5, 6])   # f(x) = kx/√(1 + c x²) iterated
    cc = rng.choice([1, 3, 8]); cn = cc * sum(k ** (2 * i) for i in range(n))
    return dict(q=f'f(x) = \\f{{{k}x}}{{√{{1 + {cc}x^{{2}}}}}}. Composing f with itself {n} times gives \\f{{{k}^{{{n}}}x}}{{√{{1 + Cx^{{2}}}}}}. C = ____.', o=None, a=cn,
                sol=['If f^{m} = \\f{k^{m}x}{√{1 + c_{m}x^{2}}}, then c_{m+1} = c_{m} + c·k^{2m}.', f'c_{{{n}}} = {cc}(1 + {k * k} + … ) = {cn}.'], p=dict(t='t_iter', k=k, n=n, cc=cc))

def g_fcount(rng):
    t = rng.choice(['c_onto', 'c_not', 'c_inj', 'c_many', 'c_sum', 'c_exact'])
    m, n = rng.choice([3, 4, 5, 6]), rng.choice([2, 3, 4])
    if t == 'c_onto':
        val = sum((-1) ** k * math.comb(n, k) * (n - k) ** m for k in range(n + 1)); need(val > 0)
        return dict(q=f'The number of onto functions from a {m}-element set to a {n}-element set is ____.', o=None, a=val,
                    sol=['Inclusion–exclusion: Σ(−1)^{k}C(n, k)(n − k)^{m}.', f'= {val}.'], p=dict(t=t, m=m, n=n))
    if t == 'c_not':
        val = n ** m - sum((-1) ** k * math.comb(n, k) * (n - k) ** m for k in range(n + 1))
        return dict(q=f'The number of functions from {{1, …, {m}}} to a {n}-element set that are NOT onto is ____.', o=None, a=val,
                    sol=[f'All functions: {n}^{{{m}}}; subtract the onto ones.', f'= {val}.'], p=dict(t=t, m=m, n=n))
    if t == 'c_inj':
        a, b = rng.choice([2, 3, 4]), rng.choice([4, 5, 6, 7, 10]); need(b >= a); val = math.perm(b, a)
        return dict(q=f'The number of one-one functions from a {a}-element set to a {b}-element set is ____.', o=None, a=val, sol=['Choose images in order without repeats.', f'{b}P{a} = {val}.'], p=dict(t=t, a=a, b=b))
    if t == 'c_many':
        k = rng.choice([3, 4]); val = (k ** k - (k - 1) ** k) - math.factorial(k)
        return dict(q=f'A = {{1, …, {k}}} and B has {k} elements, one of them b. The number of many-one functions f : A → B with b in the range is ____.', o=None, a=val,
                    sol=[f'Functions hitting b: {k}^{{{k}}} − {k - 1}^{{{k}}}.', f'Remove the {math.factorial(k)} one-one ones (they all hit b) → {val}.'], p=dict(t=t, k=k))
    if t == 'c_sum':
        B = sorted(rng.sample(range(1, 15), 7)); A = 5; s = rng.choice(sorted({x + y for x in B for y in B if x != y}))
        pairs = sum(1 for x in B for y in B if x != y and x + y == s); val = pairs * math.perm(len(B) - 2, A - 2); need(pairs > 0)
        return dict(q=f'A has 5 elements including p and q; B = {{{", ".join(map(str, B))}}}. The number of one-one f : A → B with f(p) + f(q) = {s} is ____.', o=None, a=val,
                    sol=[f'Ordered pairs (f(p), f(q)) adding to {s}: {pairs}.', f'The other 3 elements: {len(B) - 2}P3 = {math.perm(len(B) - 2, 3)} → {val}.'], p=dict(t=t, B=B, s=s))
    N, k = rng.choice([10, 20, 50, 98, 100]), rng.choice([1, 2, 3]); val = N * 2 ** k
    return dict(q=f'The number of functions f : {{1, …, {N + k}}} → {{0, 1}} that give the value 1 to exactly one of 1, …, {N} is ____.', o=None, a=val,
                sol=[f'Pick that one number: {N} ways; the last {k} inputs are free: 2^{{{k}}}.', f'= {val}.'], p=dict(t='c_exact', N=N, k=k))

def g_feq(rng):
    t = rng.choice(['e_pair', 'e_add', 'e_exp', 'e_quad'])
    if t == 'e_pair':
        k, c, a = rng.choice([2, 3]), rng.choice([6, 12, 15, 24, 36]), rng.choice([2, 4, 5]); p, q = rng.sample([d for d in range(1, c + 1) if c % d == 0], 2)
        f = lambda x: (F(a) * x - k * a * F(c, x)) / (1 - k * k); val = f(p) + f(q); need(val.denominator <= 4)
        right = str(val); o, an = mcq(rng, right, [str(z) for z in (-val, val + 1, val * 2, f(p) - f(q)) if z != val])
        return dict(q=f'f(x) + {k}f(\\f{{{c}}}{{x}}) = {a}x for all x ≠ 0. Then f({p}) + f({q}) =', o=o, a=an,
                    sol=[f'Replace x by {c}/x and solve the two equations for f(x).', f'f(x) = \\f{{{a}x − {k * a * c}/x}}{{{1 - k * k}}} → {right}.'], p=dict(t=t, k=k, c=c, a=a, pq=[p, q]))
    if t == 'e_add':
        a, n = rng.choice([1, 2, 3]), rng.choice([5, 10, 20, 50]); val = a * n * (n + 1) // 2
        return dict(q=f'f(m + n) = f(m) + f(n) for all natural m, n and f(1) = {a}. Then f(1) + f(2) + … + f({n}) = ____.', o=None, a=val,
                    sol=[f'Additive → f(n) = {a}n.', f'Sum = {a} × \\f{{{n}·{n + 1}}}{{2}} = {val}.'], p=dict(t=t, a=a, n=n))
    if t == 'e_exp':
        a, n = rng.choice([2, 3, 5, 7]), rng.choice([3, 4, 5, 6]); val = sum(a ** x for x in range(1, n + 1))
        return dict(q=f'f(x + y) = f(x)f(y) for all natural x, y and f(1) = {a}. If Σ_{{x=1}}^{{n}} f(x) = {val}, then n = ____.', o=None, a=n,
                    sol=[f'f(x) = {a}^{{x}}.', f'{a} + {a}^{{2}} + … + {a}^{{n}} = {val} → n = {n}.'], p=dict(t=t, a=a, n=n))
    p_, q_, f0 = rng.choice([1, 2, 3]), rng.choice([1, 2, 3]), rng.choice([-2, -1, 0, 1]); n = rng.choice([3, 4, 5])   # f(x+y) = f(x) + p y² + q y + α xy
    al = 2 * p_; val = sum(al + p_ * k * k + q_ * k + f0 for k in range(1, n + 1))
    return dict(q=f'f(x + y) = f(x) + {p_ if p_ > 1 else ""}y^{{2}} + {q_ if q_ > 1 else ""}y + αxy for all real x, y, and f(0) = {f0}. Then Σ_{{k=1}}^{{{n}}}(α + f(k)) = ____.', o=None, a=val,
                sol=[f'x = 0: f(y) = {p_}y^{{2}} + {q_}y + {f0}; expanding f(x + y) gives the xy coefficient {2 * p_} → α = {al}.', f'Sum = {val}.'], p=dict(t='e_quad', p=p_, q=q_, f0=f0, n=n))

def g_sets(rng):
    t = rng.choice(['s_incl', 's_nocons', 's_part', 's_union'])
    if t == 's_incl':
        a, b = rng.choice([(1, 100), (100, 700), (1, 500), (50, 300), (1, 1000)]); p, q = rng.choice([(2, 3), (3, 4), (3, 5), (4, 6), (2, 5)])
        val = sum(1 for n in range(a, b + 1) if n % p and n % q)
        return dict(q=f'The number of integers n with {a} ≤ n ≤ {b} that are multiples of neither {p} nor {q} is ____.', o=None, a=val,
                    sol=['Total − (multiples of p) − (multiples of q) + (multiples of lcm).', f'= {val}.'], p=dict(t=t, a=a, b=b, pq=[p, q]))
    if t == 's_nocons':
        n, g = rng.choice([4, 5, 6, 7, 8]), rng.choice([2, 3]); val = sum(1 for r in range(n + 1) for c in itertools.combinations(range(1, n + 1), r) if all(y - x >= g for x, y in zip(c, c[1:])))
        return dict(q=f'How many subsets of {{1, …, {n}}} (including the empty set) have any two of their elements at least {g} apart?', o=None, a=val,
                    sol=['Build up n by n: s_{n} = s_{n−1} + s_{n−g} (n unused, or used with n − g + 1 … n − 1 unused).', f'= {val}.'], p=dict(t=t, n=n, g=g))
    if t == 's_part':
        k, sz = rng.choice([2, 3, 4]), rng.choice([2, 3]); val = math.factorial(k * sz) // math.factorial(sz) ** k; named = rng.choice([True, False])
        if not named: val //= math.factorial(k)
        return dict(q=f'A set of {k * sz} elements is split into {k} {"named " if named else ""}subsets of {sz} elements each{" (the subsets are labelled)" if named else " (the order of the subsets does not matter)"}. The number of ways is ____.', o=None, a=val,
                    sol=['Multinomial: \\f{(k·s)!}{(s!)^{k}}' + ('' if named else ', divided by k! for unlabelled groups') + '.', f'= {val}.'], p=dict(t=t, k=k, sz=sz, named=named))
    a1, d1, a2, d2, N = rng.choice([1, 2, 3, 4]), rng.choice([3, 4, 5]), rng.choice([5, 9, 11]), rng.choice([6, 7]), rng.choice([20, 50, 100])
    A = {a1 + d1 * i for i in range(N)}; B = {a2 + d2 * i for i in range(N)}; val = len(A | B)
    return dict(q=f'A = {{{a1}, {a1 + d1}, {a1 + 2 * d1}, …}} and B = {{{a2}, {a2 + d2}, {a2 + 2 * d2}, …}} each hold the first {N} terms of their A.P. Then n(A ∪ B) = ____.', o=None, a=val,
                sol=['n(A ∪ B) = n(A) + n(B) − n(A ∩ B); common terms form an A.P. with difference lcm(d_{1}, d_{2}).', f'= {val}.'], p=dict(t='s_union', a1=a1, d1=d1, a2=a2, d2=d2, N=N))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(sets=g_sets, rel=g_rel, dom=g_dom, ftype=g_ftype, fcount=g_fcount, feq=g_feq).items()}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('r_lmn', 'r_prop'):
        X = p['X']; f = RULES[p['rule']][1](p['a'], p['b']); R = {(x, y) for x in X for y in X if f(x, y)}
        if t == 'r_prop': return Rv == pname(*props(X, R))
        R2 = set(R) | {(x, x) for x in X}; R3 = set(R) | {(y, x) for (x, y) in R}
        val = len(R) + (len(R2) - len(R) if 'm' in p['ask'] else 0) + (len(R3) - len(R) if 'n' in p['ask'] else 0); return Rv == val
    if t == 'r_count':
        n = p['n']; X = list(range(n)); pairs = [(a, b) for a in X for b in X]
        if n > 4 and p['kind'] in ('all', 'reflexive', 'symmetric'):   # too many to list: count by independent formula pieces
            return Rv == {'all': 2 ** len(pairs), 'reflexive': 2 ** (len(pairs) - n), 'symmetric': 2 ** (n + len(list(itertools.combinations(X, 2))))}[p['kind']]
        if p['kind'] == 'equivalence':   # count set partitions by enumerating labelings
            seen = set()
            for lab in itertools.product(range(n), repeat=n):
                canon, mp = [], {}
                for x in lab: mp.setdefault(x, len(mp)); canon.append(mp[x])
                seen.add(tuple(canon))
            return Rv == len(seen)
        off = [q for q in itertools.combinations(X, 2)]
        if p['kind'] == 'reflexive and symmetric': return Rv == sum(1 for _ in itertools.product((0, 1), repeat=len(off)))
        return Rv == sum(1 for k in range(1 << len(pairs)) for R in [{pairs[i] for i in range(len(pairs)) if k >> i & 1}] if (p['kind'] == 'all' or (p['kind'] == 'reflexive' and props(X, R)[0]) or (p['kind'] == 'symmetric' and props(X, R)[1])))
    if t == 'r_pairs':
        X = [(a, b) for a in p['A'] for b in p['B']]; return Rv == sum(1 for q1 in X for q2 in X if ((q1[0] + q2[0] - q1[1] - q2[1]) if p['op'] == 'sum' else (q1[0] - q2[0] - q1[1] + q2[1])) == 0)
    if t == 'r_lattice': return Rv == len({(x, y) for x in range(-12, 13) for y in range(-12, 13) if p['a'] * x * x + p['b'] * y * y < p['c']})
    if t == 'd_quad':
        S, P = p['p'] + p['q'], p['p'] * p['q']; xs = [x for x in grid(-10, 10, 200001) if -P + S * x - x * x > 0 and x + abs(x) > 0]; a, b = round(min(xs)), round(max(xs)); return Rv == (p['k'] + a) ** 2 + b * b
    if t == 'd_trig':
        v = [1 / (p['c'] - math.sin(p['k'] * x)) for x in grid(0, 2 * math.pi, 20001)]; lo, hi = [num(z) for z in Rv.strip('[]').split(', ')]; return abs(min(v) - lo) < 1e-6 and abs(max(v) - hi) < 1e-6
    if t == 'd_log':
        xs = [x for x in grid(0, 20, 200001) if (p['r1'] + p['r2']) * x - x * x - p['r1'] * p['r2'] > 0]; return Rv == round(min(xs) ** 2 + max(xs) ** 2)
    if t == 'd_rat':
        f = lambda x: (p['k'] - x) / ((x - p['p']) * (x - p['q'])); ext = []   # turning points of f are the two ends of the gap in its range
        for lo, hi in ((-300, min(p['p'], p['q'])), (min(p['p'], p['q']), max(p['p'], p['q'])), (max(p['p'], p['q']), 300)):
            xs = grid(lo + 1e-4, hi - 1e-4, 200001); v = [f(x) for x in xs]
            ext += [v[i] for i in range(1, len(v) - 1) if (v[i] - v[i - 1]) * (v[i + 1] - v[i]) < 0]
        return len(ext) == 2 and abs(Rv - sum(e * e for e in ext)) < 1e-3 * max(1, Rv)
    if t == 'd_logq':
        S, Pq, b = p['r1'] + p['r2'], p['r1'] * p['r2'], p['b']; ok = lambda x: x * x - S * x + Pq > 0 and math.log(x * x - S * x + Pq, b) < 1
        xs = grid(-20, 30, 500001); ends = [x for i, x in enumerate(xs[1:], 1) if ok(x) != ok(xs[i - 1])]; return len(ends) == 4 and abs(Rv - sum(ends)) < 0.01
    if t == 't_type': return Rv == classify(FT[p['k']][1])
    if t == 't_inv':
        c = p['c']; f = lambda x: c[0] * x ** 5 + c[1] * x ** 3 + c[2] * x + c[3]; x0 = p['x0']; d = (f(x0 + 1e-6) - f(x0 - 1e-6)) / 2e-6
        want = 1 / d if p['ask'] == 'g' else x0 * d; return abs(float(F(Rv)) - want) < 1e-5
    if t == 't_comp':
        f = lambda x: p['a'] * x + p['b']; g = lambda x: p['c'] * x + p['d']; return Rv == (f(g(p['x'])) if p['which'] == 'fog' else g(f(p['x'])))
    if t == 't_iter':
        x = 0.01; y = x
        for _ in range(p['n']): y = p['k'] * y / math.sqrt(1 + p['cc'] * y * y)
        C = ((p['k'] ** p['n'] * x / y) ** 2 - 1) / (x * x); return abs(Rv - C) < 1e-3 * max(1, C)
    if t == 'c_onto': return Rv == sum(1 for f in itertools.product(range(p['n']), repeat=p['m']) if len(set(f)) == p['n'])
    if t == 'c_not': return Rv == sum(1 for f in itertools.product(range(p['n']), repeat=p['m']) if len(set(f)) < p['n'])
    if t == 'c_inj': return Rv == sum(1 for _ in itertools.permutations(range(p['b']), p['a']))
    if t == 'c_many': return Rv == sum(1 for f in itertools.product(range(p['k']), repeat=p['k']) if 0 in f and len(set(f)) < p['k'])
    if t == 'c_sum': return Rv == sum(1 for f in itertools.permutations(p['B'], 5) if f[0] + f[1] == p['s'])
    if t == 'c_exact':
        N, k = p['N'], p['k']; return Rv == N * len(list(itertools.product((0, 1), repeat=k)))   # 1 position among N, rest of 1..N zero, k free
    if t == 'e_pair':
        k, c, a = p['k'], p['c'], p['a']; f = lambda x: (F(a) * x - k * a * F(c, x)) / (1 - k * k)
        ok = all(f(x) + k * f(F(c, x)) == a * x for x in (F(1), F(2), F(3, 2), F(7)))
        return ok and F(Rv) == sum(f(F(x)) for x in p['pq'])
    if t == 'e_add': return Rv == sum(p['a'] * n for n in range(1, p['n'] + 1))
    if t == 'e_exp':
        tot = 0
        for n in range(1, 30):
            tot += p['a'] ** n
            if tot == sum(p['a'] ** x for x in range(1, p['n'] + 1)): return Rv == n
        return False
    if t == 'e_quad':
        f = lambda x: p['p'] * x * x + p['q'] * x + p['f0']; al = (f(2) - f(1) - p['p'] - p['q']) / 1   # f(1+1) = f(1) + p + q + α
        return Rv == round(sum(al + f(k) for k in range(1, p['n'] + 1)))
    if t == 's_incl':
        q1, q2 = p['pq']; return Rv == len([n for n in range(p['a'], p['b'] + 1) if n % q1 != 0 and n % q2 != 0])
    if t == 's_nocons':
        s = [1] * (p['g']) + [0] * (p['n'] + 1)
        cnt = sum(1 for mask in range(1 << p['n']) for c in [[i + 1 for i in range(p['n']) if mask >> i & 1]] if all(y - x >= p['g'] for x, y in zip(c, c[1:]))); return Rv == cnt
    if t == 's_part':
        k, sz = p['k'], p['sz']; n = k * sz
        if n > 9: return Rv == math.factorial(n) // math.factorial(sz) ** k // (1 if p['named'] else math.factorial(k))
        labs = sum(1 for lab in itertools.product(range(k), repeat=n) if all(lab.count(j) == sz for j in range(k)))
        return Rv == (labs if p['named'] else labs // math.factorial(k))
    if t == 's_union':
        A = [p['a1'] + p['d1'] * i for i in range(p['N'])]; B = [p['a2'] + p['d2'] * i for i in range(p['N'])]; return Rv == len(A) + len(B) - len([x for x in A if x in B])
    raise KeyError(t)
