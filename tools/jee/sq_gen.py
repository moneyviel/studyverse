"""Practice generators — Mathematics Unit 6: Sequence and Series. check() rebuilds each sequence term by term
with exact fractions (or searches) instead of using the closed-form formulas the generator used."""
import math
from fractions import Fraction as F
from common import mcq, fr
def ap(a, d, n): return [F(a) + k * F(d) for k in range(n)]
def gp(a, r, n): return [F(a) * F(r) ** k for k in range(n)]
def fx(x): return fr(x)
def unfx(s):
    s = s.strip().replace('−', '-')
    if s.startswith('-\\f{') or s.startswith('\\f{'):
        neg = s.startswith('-'); a, b = s.lstrip('-')[3:-1].split('}{'); v = F(int(a), int(b)); return -v if neg else v
    return F(s)

def g_ap(rng):
    t = rng.choice(['nth', 'sum', 'zero', 'two', 'common', 'fromS', 'oddeven'])
    a, d = rng.choice([1, 2, 3, 5, 7, -4, 10, F(1, 2), F(3, 2)]), rng.choice([2, 3, 4, 5, -2, -3, F(1, 2), F(3, 2), 6])
    if t == 'nth':
        n = rng.randint(8, 60); v = a + (n - 1) * d
        q = f'The {n}^{{th}} term of the A.P. {", ".join(fx(x) for x in ap(a, d, 3))}, … is :'
        o, i = mcq(rng, fx(v), [fx(x) for x in (a + n * d, a + (n - 2) * d, n * d, a * n + d, v + 1)])
        return dict(q=q, o=o, a=i, sol=[f'a = {fx(a)}, d = {fx(d)}.', f'a_{{{n}}} = a + {n - 1}d = {fx(v)}.'], p=dict(t='nth', a=str(a), d=str(d), n=n))
    if t == 'sum':
        n = rng.randint(10, 40); v = F(n, 2) * (2 * a + (n - 1) * d)
        if v.denominator != 1: return g_ap(rng)
        q = f'The sum of the first {n} terms of the A.P. {", ".join(fx(x) for x in ap(a, d, 3))}, … is ______.'
        return dict(q=q, o=None, a=int(v), sol=[f'S_{{n}} = \\f{{n}}{{2}}[2a + (n − 1)d] = \\f{{{n}}}{{2}}[{fx(2 * a)} + {n - 1} × {fx(d)}].', f'= {int(v)}.'], p=dict(t='sum', a=str(a), d=str(d), n=n))
    if t == 'zero':
        a1 = rng.choice([2, 3, 4, 5, 6, 10, 12]); m = rng.choice([4, 6, 8, 10, 12, 14, 20]); d = F(-2 * a1, m)
        n = m + 1
        q = f'An A.P. has first term {a1} and common difference {fx(d)}. The number of terms whose sum is zero is ______.'
        return dict(q=q, o=None, a=n, sol=['S_{n} = \\f{n}{2}[2a + (n − 1)d] = 0 → n − 1 = −\\f{2a}{d}.', f'n − 1 = {m} → n = {n}.'], p=dict(t='zero', a=a1, d=str(d)))
    if t == 'two':
        a, d = rng.choice([-5, -3, 1, 2, 4, F(1, 2)]), rng.choice([F(1, 2), 1, 2, 3, F(3, 2)]); p_, q_ = rng.sample([8, 10, 12, 15, 20, 30], 2); r_ = rng.choice([25, 40, 50])
        Sp, Sq, Sr = [F(k, 2) * (2 * a + (k - 1) * d) for k in (p_, q_, r_)]
        q = f'In an A.P., S_{{{p_}}} = {fx(Sp)} and S_{{{q_}}} = {fx(Sq)}. Then S_{{{r_}}} is :'
        o, i = mcq(rng, fx(Sr), [fx(x) for x in (Sr + r_, Sr - r_, Sp + Sq, Sr * 2, Sr + d * r_ / 2, Sr - 10)])
        return dict(q=q, o=o, a=i, sol=[f'Solve \\f{{{p_}}}{{2}}(2a + {p_ - 1}d) = {fx(Sp)}, \\f{{{q_}}}{{2}}(2a + {q_ - 1}d) = {fx(Sq)} → a = {fx(a)}, d = {fx(d)}.', f'S_{{{r_}}} = {fx(Sr)}.'], p=dict(t='two', P=p_, Q=q_, R=r_, Sp=str(Sp), Sq=str(Sq)))
    if t == 'common':
        a1, d1, a2, d2 = rng.choice([1, 2, 3, 4]), rng.choice([3, 4, 5, 6]), rng.choice([2, 5, 7, 9]), rng.choice([5, 7, 8, 9])
        if math.gcd(d1, d2) != 1: return g_ap(rng)
        n = rng.choice([50, 100, 120, 200])
        q = f'A = first {n} terms of {a1}, {a1 + d1}, {a1 + 2 * d1}, … and B = first {n} terms of {a2}, {a2 + d2}, {a2 + 2 * d2}, …. The number of common terms is ______.'
        c = len({a1 + d1 * k for k in range(n)} & {a2 + d2 * k for k in range(n)})
        if c == 0: return g_ap(rng)
        return dict(q=q, o=None, a=c, sol=[f'Common terms form an A.P. with difference lcm({d1}, {d2}) = {d1 * d2}.', f'Find the first common term, then count up to min of the last terms → {c}.'], p=dict(t='common', a1=a1, d1=d1, a2=a2, d2=d2, n=n))
    if t == 'fromS':
        p_, q_ = rng.choice([1, 2, 3, 4, 5]), rng.choice([-3, -1, 1, 2, 5, 7]); n = rng.randint(5, 30)
        v = 2 * p_ * n - p_ + q_
        q = f'The sum of the first n terms of an A.P. is {p_}n^{{2}} {"+" if q_ > 0 else "−"} {abs(q_)}n. Its {n}^{{th}} term is :'
        o, i = mcq(rng, str(v), [str(x) for x in (p_ * n * n + q_ * n, v + p_, v - p_, 2 * p_ * n + q_, v + 2 * p_)])
        return dict(q=q, o=o, a=i, sol=['a_{n} = S_{n} − S_{n−1} = 2pn − p + q.', f'a_{{{n}}} = {v}.'], p=dict(t='fromS', P=p_, Q=q_, n=n))
    k = rng.randint(3, 10); d = rng.choice([F(1, 2), 1, 2, 3, F(3, 2)]); a = rng.choice([F(1, 2), 1, 2, 3, -2])
    s = ap(a, d, 2 * k); odd, even = sum(s[::2]), sum(s[1::2])
    q = f'An A.P. has an even number of terms. The sum of the odd-numbered terms is {fx(odd)}, of the even-numbered terms is {fx(even)}, and the last term exceeds the first by {fx(s[-1] - s[0])}. The number of terms is ______.'
    return dict(q=q, o=None, a=2 * k, sol=['(even sum) − (odd sum) = kd for 2k terms; last − first = (2k − 1)d.', f'kd = {fx(even - odd)} and (2k − 1)d = {fx(s[-1] - s[0])} → d = {fx(d)}, k = {k} → {2 * k} terms.'], p=dict(t='oddeven', odd=str(odd), even=str(even), gap=str(s[-1] - s[0])))

def g_gp(rng):
    t = rng.choice(['nth', 'sum', 'inf', 'mid', 'ratio'])
    a, r = rng.choice([1, 2, 3, 4, F(1, 2), 5]), rng.choice([2, 3, -2, F(1, 2), F(1, 3), 4])
    if t == 'nth':
        n = rng.randint(5, 9); v = a * r ** (n - 1)
        q = f'The {n}^{{th}} term of the G.P. {", ".join(fx(x) for x in gp(a, r, 3))}, … is :'
        o, i = mcq(rng, fx(v), [fx(x) for x in (a * r ** n, a * r ** (n - 2), a * r * n, v * 2, -v)])
        return dict(q=q, o=o, a=i, sol=[f'a_{{n}} = ar^{{n−1}} = {fx(a)} × ({fx(r)})^{{{n - 1}}} = {fx(v)}.'], p=dict(t='nth', a=str(a), r=str(r), n=n))
    if t == 'sum':
        r = rng.choice([2, 3, -2, 4]); n = rng.randint(4, 9); v = a * (F(r) ** n - 1) / (r - 1)
        if v.denominator != 1: return g_gp(rng)
        q = f'The sum of the first {n} terms of the G.P. {", ".join(fx(x) for x in gp(a, r, 3))}, … is ______.'
        return dict(q=q, o=None, a=int(v), sol=[f'S_{{n}} = a\\f{{r^{{n}} − 1}}{{r − 1}} = {fx(a)} × \\f{{{fx(F(r) ** n)} − 1}}{{{r - 1}}} = {int(v)}.'], p=dict(t='sum', a=str(a), r=str(r), n=n))
    if t == 'inf':
        r = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(-1, 2), F(3, 4), F(1, 4), F(-1, 3)]); a = rng.choice([1, 2, 3, 4, 6, 9, 12, 64])
        v = a / (1 - r)
        q = f'The sum to infinity of the G.P. {", ".join(fx(x) for x in gp(a, r, 3))}, … is :'
        o, i = mcq(rng, fx(v), [fx(x) for x in (a / (1 + r), a * (1 - r), a / r, v * 2, v + a)])
        return dict(q=q, o=o, a=i, sol=[f'|r| = {fx(abs(r))} < 1 → S_{{∞}} = \\f{{a}}{{1 − r}} = {fx(v)}.'], p=dict(t='inf', a=str(a), r=str(r)))
    if t == 'mid':
        m = rng.choice([2, 3, 4, 5, 6, 7]); r = rng.choice([2, 3, 4]); k = rng.choice([3, 4])
        prod = m ** 2
        a_k = m; q = f'In a G.P. of positive terms, a_{{{k - 1}}}a_{{{k + 1}}} = {prod} and a_{{{k - 1}}} + a_{{{k + 1}}} = {fx(F(m, r) + m * r)}. If the G.P. is increasing, a_{{{k + 2}}} is :'
        v = m * r * r
        o, i = mcq(rng, str(v), [str(x) for x in (m * r, m * r ** 3, m + r, v * 2, m * r * r - 1)])
        return dict(q=q, o=o, a=i, sol=[f'a_{{{k - 1}}}a_{{{k + 1}}} = a_{{{k}}}^{{2}} → a_{{{k}}} = {m}.', f'{m}(\\f{{1}}{{r}} + r) = {fx(F(m, r) + m * r)} → r = {r}.', f'a_{{{k + 2}}} = {m} × {r}^{{2}} = {v}.'], p=dict(t='mid', P=prod, S=str(F(m, r) + m * r), k=k))
    r = rng.choice([2, 3, F(1, 2), 4]); a = rng.choice([1, 2, 3, F(1, 3)]); i1, i2 = rng.choice([(2, 5), (3, 6), (1, 4), (1, 2), (2, 3)])
    q = f'In a G.P., a_{{{i1}}} = {fx(a * F(r) ** (i1 - 1))} and a_{{{i2}}} = {fx(a * F(r) ** (i2 - 1))}. The common ratio (real) is :'
    o, i = mcq(rng, fx(r), [fx(x) for x in (F(r) ** 2, 1 / F(r), -F(r), F(r) + 1, F(r) ** (i2 - i1))])
    return dict(q=q, o=o, a=i, sol=[f'\\f{{a_{{{i2}}}}}{{a_{{{i1}}}}} = r^{{{i2 - i1}}} = {fx(F(r) ** (i2 - i1))}.', f'r = {fx(r)}.'], p=dict(t='ratio', x=str(a * F(r) ** (i1 - 1)), y=str(a * F(r) ** (i2 - i1 + i1 - 1)), k=i2 - i1))

def g_mix(rng):
    t = rng.choice(['amgm', 'insert', 'apgp', 'min', 'gmeans'])
    if t == 'amgm':
        a, b = rng.choice([(x, y) for x in range(1, 40) for y in range(x + 1, 120) if math.isqrt(x * y) ** 2 == x * y and (x + y) % 2 == 0])
        A, G = F(a + b, 2), int(math.isqrt(a * b))
        q = f'Two positive numbers have arithmetic mean {fx(A)} and geometric mean {G}. The larger number is :'
        o, i = mcq(rng, str(b), [str(x) for x in (a, b + 1, a + b, G * 2, b - 1)])
        return dict(q=q, o=o, a=i, sol=[f'x + y = {fx(2 * A)}, xy = {G * G}.', f'x, y are roots of t^{{2}} − {fx(2 * A)}t + {G * G} = 0 → {a} and {b}.'], p=dict(t='amgm', A=str(A), G=G))
    if t == 'insert':
        a, b, n = rng.randint(1, 20), rng.randint(25, 150), rng.randint(3, 20)
        if (b - a) % (n + 1): return g_mix(rng)
        d = (b - a) // (n + 1); s = n * F(a + b, 2)
        q = f'{n} arithmetic means are inserted between {a} and {b}. Their sum is ______.'
        return dict(q=q, o=None, a=int(s), sol=[f'Sum of n A.M.s between a and b = n × \\f{{a + b}}{{2}}.', f'= {n} × {fx(F(a + b, 2))} = {int(s)} (d = {d}).'], p=dict(t='insert', a=a, b=b, n=n))
    if t == 'apgp':
        opts = [(b, dd, x, y) for b in range(3, 25) for dd in range(1, 12) for x in range(0, 9) for y in range(0, 9) if (b - dd + x) * (b + dd + y) == b * b and b - dd > 0
                and sum(1 for e in range(1, 40) if (b - e + x) * (b + e + y) == b * b) == 1]
        b, dd, x, y = rng.choice(opts); a, c = b - dd, b + dd
        q = f'a, b, c are in A.P. with a + b + c = {3 * b}, and a + {x}, b, c + {y} are in G.P. If a < b, then abc is ______.'
        return dict(q=q, o=None, a=a * b * c, sol=[f'b = {b}; a = {b} − d, c = {b} + d.', f'({b} − d + {x})({b} + d + {y}) = {b * b} → d = {dd} → {a}, {b}, {c}.', f'abc = {a * b * c}.'], p=dict(t='apgp', b=b, x=x, y=y))
    if t == 'gmeans':
        a, r, n = rng.choice([1, 2, 3, 4, 5]), rng.choice([2, 3]), rng.randint(2, 6)
        b = a * r ** (n + 1); v = (a * b) ** n
        if v > 10 ** 12 or (n % 2 and math.isqrt(a * b) ** 2 != a * b): return g_mix(rng)
        prod = math.isqrt(v)
        q = f'{n} geometric means are inserted between {a} and {b}. Their product is ______.'
        return dict(q=q, o=None, a=prod, sol=['Product of n G.M.s between a and b = (√{ab})^{n}.', f'= (√{{{a * b}}})^{{{n}}} = {prod}.'], p=dict(t='gmeans', a=a, b=b, n=n))
    k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    q = f'For real x, the least value of {k}^{{x}} + {k}^{{−x}} + {k * k}^{{x}} + {k * k}^{{−x}} is ______.'
    return dict(q=q, o=None, a=4, sol=['By AM ≥ GM, y + \\f{1}{y} ≥ 2 for y > 0, with equality at y = 1.', 'Both pairs are least (2 each) at x = 0 → 4.'], p=dict(t='min', k=k))

def g_tele(rng):
    t = rng.choice(['kk1', 'kk2', 'sq', 'cube', 'four', 'kk1p'])
    n = rng.randint(5, 120)
    if t == 'kk1':
        s = F(n, n + 1)
        q = f'The sum \\f{{1}}{{1·2}} + \\f{{1}}{{2·3}} + … + \\f{{1}}{{{n}·{n + 1}}} is :'
        o, i = mcq(rng, fx(s), [fx(x) for x in (F(n - 1, n), F(n + 1, n + 2), F(1, n + 1), F(n, n + 2), F(n + 1, n))])
        return dict(q=q, o=o, a=i, sol=['\\f{1}{k(k + 1)} = \\f{1}{k} − \\f{1}{k + 1} — telescoping.', f'Sum = 1 − \\f{{1}}{{{n + 1}}} = {fx(s)}.'], p=dict(t='kk1', n=n))
    if t == 'kk2':
        s = F(1, 2) * (1 + F(1, 2) - F(1, n + 1) - F(1, n + 2))
        q = f'The sum \\f{{1}}{{1·3}} + \\f{{1}}{{2·4}} + … + \\f{{1}}{{{n}·{n + 2}}} is :'
        o, i = mcq(rng, fx(s), [fx(x) for x in (F(1, 2) * (1 - F(1, n + 2)), F(3, 4), s * 2, F(n, 2 * n + 2), F(3, 4) - F(1, n + 2))])
        return dict(q=q, o=o, a=i, sol=['\\f{1}{k(k + 2)} = \\f{1}{2}(\\f{1}{k} − \\f{1}{k + 2}).', f'Sum = \\f{{1}}{{2}}(1 + \\f{{1}}{{2}} − \\f{{1}}{{{n + 1}}} − \\f{{1}}{{{n + 2}}}) = {fx(s)}.'], p=dict(t='kk2', n=n))
    if t == 'sq':
        n = rng.randint(8, 40); v = n * (n + 1) * (2 * n + 1) // 6
        return dict(q=f'1^{{2}} + 2^{{2}} + 3^{{2}} + … + {n}^{{2}} = ______.', o=None, a=v, sol=['Σk^{2} = \\f{n(n + 1)(2n + 1)}{6}.', f'= \\f{{{n} × {n + 1} × {2 * n + 1}}}{{6}} = {v}.'], p=dict(t='sq', n=n))
    if t == 'cube':
        n = rng.randint(5, 30); v = (n * (n + 1) // 2) ** 2
        return dict(q=f'1^{{3}} + 2^{{3}} + … + {n}^{{3}} = ______.', o=None, a=v, sol=['Σk^{3} = (\\f{n(n + 1)}{2})^{2}.', f'= {n * (n + 1) // 2}^{{2}} = {v}.'], p=dict(t='cube', n=n))
    if t == 'kk1p':
        n = rng.randint(5, 30); v = n * (n + 1) * (n + 2) // 3
        return dict(q=f'1·2 + 2·3 + 3·4 + … + {n}·{n + 1} = ______.', o=None, a=v, sol=['Σk(k + 1) = \\f{n(n + 1)(n + 2)}{3}.', f'= {v}.'], p=dict(t='kk1p', n=n))
    n = rng.randint(4, 30); s = F(1, 4) * (1 - F(1, 2 * n * n + 2 * n + 1))
    q = f'The sum of the first {n} terms of \\f{{1}}{{1 + 4·1^{{4}}}} + \\f{{2}}{{1 + 4·2^{{4}}}} + \\f{{3}}{{1 + 4·3^{{4}}}} + … is \\f{{m}}{{n}} in lowest terms. m + n is ______.'
    return dict(q=q, o=None, a=s.numerator + s.denominator, sol=['1 + 4k^{4} = (2k^{2} − 2k + 1)(2k^{2} + 2k + 1) → \\f{k}{1 + 4k^{4}} = \\f{1}{4}[\\f{1}{2k^{2} − 2k + 1} − \\f{1}{2k^{2} + 2k + 1}].', f'Sum = \\f{{1}}{{4}}(1 − \\f{{1}}{{{2 * n * n + 2 * n + 1}}}) = {fx(s)}.'], p=dict(t='four', n=n))

GEN = dict(ap=g_ap, gp=g_gp, mix=g_mix, tele=g_tele)
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'nth': return unfx(R) == (ap(F(p['a']), F(p['d']), p['n'])[-1] if 'd' in p else gp(F(p['a']), F(p['r']), p['n'])[-1])
    if t == 'sum': return R == (sum(ap(F(p['a']), F(p['d']), p['n'])) if 'd' in p else sum(gp(F(p['a']), F(p['r']), p['n'])))
    if t == 'zero':
        s, n = F(0), 0
        for x in ap(p['a'], F(p['d']), 200):
            s += x; n += 1
            if s == 0: return R == n
        return False
    if t == 'two':   # solve the 2×2 system by search over a grid of halves
        for a in [F(k, 2) for k in range(-40, 41)]:
            for d in [F(k, 2) for k in range(-20, 21)]:
                if sum(ap(a, d, p['P'])) == F(p['Sp']) and sum(ap(a, d, p['Q'])) == F(p['Sq']): return unfx(R) == sum(ap(a, d, p['R']))
        return False
    if t == 'common':
        A = [p['a1'] + p['d1'] * k for k in range(p['n'])]; B = set(p['a2'] + p['d2'] * k for k in range(p['n'])); return R == sum(1 for x in A if x in B)
    if t == 'fromS': S = lambda n: p['P'] * n * n + p['Q'] * n; return int(R) == S(p['n']) - S(p['n'] - 1)
    if t == 'oddeven':
        for k in range(1, 60):
            d = (F(p['even']) - F(p['odd'])) / k
            if (2 * k - 1) * d == F(p['gap']): return R == 2 * k
        return False
    if t == 'inf':   # partial sums converge
        s = sum(gp(F(p['a']), F(p['r']), 200)); return abs(float(unfx(R)) - float(s)) < 1e-9
    if t == 'mid':
        for r in range(2, 10):
            m = math.isqrt(p['P'])
            if F(m, r) + m * r == F(p['S']): return int(R) == m * r * r
        return False
    if t == 'ratio':
        return p['k'] % 2 == 1 and F(p['x']) * unfx(R) ** p['k'] == F(p['y'])
    if t == 'amgm':
        A, G = F(p['A']), p['G']; xs = [x for x in range(1, 200) if (2 * A - x) > 0 and x * (2 * A - x) == G * G]; return int(R) == max(xs)
    if t == 'insert': means = ap(p['a'], F(p['b'] - p['a'], p['n'] + 1), p['n'] + 2)[1:-1]; return R == sum(means)
    if t == 'apgp':
        for d in range(1, 30):
            a, c = p['b'] - d, p['b'] + d
            if (a + p['x']) * (c + p['y']) == p['b'] ** 2: return R == a * p['b'] * c
        return False
    if t == 'gmeans':
        for rr in range(2, 10):
            if p['a'] * rr ** (p['n'] + 1) == p['b']:
                pr = 1
                for i in range(1, p['n'] + 1): pr *= p['a'] * rr ** i
                return R == pr
        return False
    if t == 'min': return R == round(min(p['k'] ** x + p['k'] ** -x + (p['k'] ** 2) ** x + (p['k'] ** 2) ** -x for x in [i / 1000 for i in range(-2000, 2000)]))
    if t == 'kk1': return unfx(R) == sum(F(1, k * (k + 1)) for k in range(1, p['n'] + 1))
    if t == 'kk2': return unfx(R) == sum(F(1, k * (k + 2)) for k in range(1, p['n'] + 1))
    if t == 'sq': return R == sum(k * k for k in range(1, p['n'] + 1))
    if t == 'cube': return R == sum(k ** 3 for k in range(1, p['n'] + 1))
    if t == 'kk1p': return R == sum(k * (k + 1) for k in range(1, p['n'] + 1))
    if t == 'four': s = sum(F(k, 1 + 4 * k ** 4) for k in range(1, p['n'] + 1)); return R == s.numerator + s.denominator
    raise KeyError(t)
