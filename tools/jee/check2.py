"""Independent re-solver for generated practice items: solves from the raw parameters by a DIFFERENT method
(simulation / numeric perturbation / Decimal arithmetic / the definition-built dimension table) and compares with
the option the item marks as correct."""
import math, re, itertools
from fractions import Fraction as F
from decimal import Decimal
from dims import DEFS, TABLE, D, ONE
DQ = dict(TABLE); DQ.update(DEFS)        # every derived quantity taken from its DEFINITION, not the typed table

def num(s):
    s = s.replace('−', '-').replace('%', '').replace('mm', '').replace('cm', '').replace('m^{2}', '').replace(' s', '').replace(' m', '').replace(' g', '').strip()
    m = re.match(r'^(-?[\d.]+) × 10\^\{(-?\d+)\}$', s)
    return float(m.group(1)) * 10 ** int(m.group(2)) if m else float(s)
def parse_dim(s):
    e = dict(M=0, L=0, T=0, A=0, K=0)
    for sym, ex in re.findall(r'([MLTAK])(?:\^\{([^}]*)\})?', s.replace('−', '-')):
        e[sym] = F(ex) if ex else 1
    return D(e['M'], e['L'], e['T'], e['A'], e['K'])
def close(a, b, rel=2e-3, ab=1e-9): return abs(a - b) <= max(ab, rel * abs(b))

def vernier_sim(N, k, s):
    """place N vernier marks over N-k main marks and measure the smallest positive gap = least count"""
    vsd = F(str(s)) * (N - k) / N
    gaps = [F(str(s)) * i - vsd * i for i in range(1, N + 1)]
    return float(min(g for g in gaps if g > 0))
def perturb(ff, xs, dxs):
    """max relative change of ff when each input moves by ±its error (brute force over sign choices)"""
    f0 = ff(*xs); best = 0
    for signs in itertools.product([-1, 1], repeat=len(xs)):
        best = max(best, abs(ff(*[x + sg * d for x, sg, d in zip(xs, signs, dxs)]) - f0) / abs(f0))
    return best

def solve(it):
    p = it['p']; t = p['t']; right = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'vlc': return close(num(right), vernier_sim(p['N'], p['k'], p['s']))
    if t == 'vlc_inv': return close(num(right), p['lc'] * p['N'])
    if t == 'vze': return close(num(right.replace('+', '')), p['z'] * p['lc'] * p['side'])
    if t == 'vread': return close(num(right), p['M'] + p['v'] * p['lc'] - p['z'] * p['lc'])
    if t == 'vneg': return close(num(right), p['M'] + p['v'] * p['lc'] + p['ze'])
    if t == 'vsph': return close(num(right), p['m'] / (math.pi / 6 * (p['d'] / 10) ** 3), 0.03)
    if t == 'vcyl': return close(num(right), math.pi / 4 * (p['d'] / 10) ** 2 * p['h'] / 10, 0.005)
    if t == 'sgr': return close(num(right) / p['mult'], p['M'] + p['c'] * p['p'] / p['N'])
    if t == 'sgz':
        ze = (1 if p['below'] else -1) * p['z'] * p['p'] / p['N']
        return close(num(right), p['M'] + p['c'] * p['p'] / p['N'] - ze)
    if t == 'sglc': return close(float(right), p['pitch'] / p['N'] * 1000)
    if t == 'sglc2': return close(float(right), p['base'] * 1000 * (1 + p['up'] / 100) / (1 - p['down'] / 100))
    if t == 'pow':
        pw = [float(F(x)) for x in p['pw']]; xs = [10.0] * len(pw); dxs = [10.0 * e / 100 * 1e-4 for e in p['e']]
        rel = perturb(lambda *v: math.prod(a ** b for a, b in zip(v, pw)), xs, dxs) / 1e-4 * 100
        return close(num(right) if isinstance(right, str) else float(right), rel, 1e-3)
    if t == 'dens': return close(num(right), 100 * perturb(lambda m, r, l: m / (math.pi * r * r * l), [p['m'], p['r'], p['l']], [p['dm'] * 1e-4, p['dr'] * 1e-4, p['dl'] * 1e-4]) / 1e-4, 1e-4, 0.0051)
    if t == 'ohm': return close(num(right), p['V'] / p['I'] * perturb(lambda v, i: v / i, [p['V'], p['I']], [p['dV'] * 1e-4, p['dI'] * 1e-4]) / 1e-4, 1e-4, 0.000051)
    if t == 'shm': return close(num(right), 100 * perturb(lambda m, T: m / T ** 2, [p['m'], p['tt']], [p['dm'] * 1e-4, p['res'] * 1e-4]) / 1e-4, 1e-4, 0.0051)
    if t == 'young': return close(num(right), 100 * perturb(lambda M, l: M / l, [p['M'], p['l']], [p['dM'] * 1e-4, p['dl'] * 1e-4]) / 1e-4, 1e-4, 0.00051)
    if t == 'exp':
        f = lambda a, tt: a ** p['n'] * math.exp(-p['beta'] * tt)
        return close(num(right), 100 * perturb(f, [1.0, p['t0']], [p['ea'] / 100 * 1e-4, p['t0'] * p['et'] / 100 * 1e-4]) / 1e-4, 1e-4, 0.00051)
    if t == 'aerr':
        S = p['a1'] - p['a2'] if p['diff'] else p['a1'] + p['a2']
        worst = max(abs((p['a1'] + s1 * p['d1']) + (-1 if p['diff'] else 1) * (p['a2'] + s2 * p['d2']) - S) for s1 in (-1, 1) for s2 in (-1, 1))
        return close(num(right), 100 * worst / S, 0, 0.0051)
    if t == 'sfc': return int(right) == sig_decimal(p['x'].split(' × ')[0])
    if t == 'sfm': return all(f'{L}–{sig_decimal(x.split(" × ")[0])}' in right for L, x in zip('ABCD', p['xs']))
    if t == 'sfadd':
        k = min(len(x.split('.')[1]) if '.' in x else 0 for x in p['xs']); s = sum(Decimal(x) for x in p['xs'])
        return right.split(' ')[0] == str(s.quantize(Decimal(1).scaleb(-k), rounding='ROUND_HALF_UP'))
    if t == 'sfmul':
        n = min(sig_decimal(p['a']), sig_decimal(p['b'])); pr = Decimal(p['a']) * Decimal(p['b'])
        return right.split(' ')[0] == str(pr.quantize(Decimal(1).scaleb(pr.adjusted() - n + 1), rounding='ROUND_HALF_EVEN'))
    if t == 'sfmean':
        k = min(len(x.split('.')[1]) for x in p['xs']); m = sum(Decimal(x) for x in p['xs']) / len(p['xs'])
        return right.split(' ')[0] == str(m.quantize(Decimal(1).scaleb(-k), rounding='ROUND_HALF_UP'))
    if t == 'mean':
        xs = p['xs']; m = sum(xs) / len(xs); mad = sum(abs(x - m) for x in xs) / len(xs)
        v = {'rel': mad / m, 'pct': 100 * mad / m, 'mad': mad}[p['what']]; return close(num(right), v, 6e-3)
    if t == 'lcr': return close(num(right), 10 ** -max(len(x.split('.')[1]) for x in p['xs']))
    if t == 'dname': return parse_dim(right) == DQ[p['n']]
    if t in ('dexpr', 'dwhich', 'dunit'):
        d = ONE
        for n, pw in p['fs']: d = d * DQ[n] ** F(pw)
        return parse_dim(right) == d if t == 'dexpr' else DQ[p['eq']] == d
    if t == 'dst':
        s1 = DQ[p['p1'][0]] == DQ[p['p1'][1]]; s2 = DQ[p['p2'][0]] == DQ[p['p2'][1]]
        want = 'Both Statement I and Statement II are true' if s1 and s2 else 'Both Statement I and Statement II are false' if not (s1 or s2) else 'Statement I is true but Statement II is false' if s1 else 'Statement I is false but Statement II is true'
        return right == want
    if t == 'dodd': return DQ[p['diff'][0]] != DQ[p['diff'][1]] and all(DQ[a] == DQ[b] for a, b in p['sames'])
    if t == 'cons':
        ks = CONS2[p['eq']]; x, y = ks[p['x']], (ks[p['y']] if p['y'] else None)
        d = {'x': x, 'xy': x * (y if y else ONE), 'x/y': x / y if y else x, 'x^2/y': x ** 2 / y if y else x, 'xy^2': x * y ** 2 if y else x}[p['op']]
        return parse_dim(right) == d
    if t == 'gas':
        V = DQ['length'] ** 3
        a_ = {'van der Waals': DQ['pressure'] * V * V, 'Berthelot': DQ['pressure'] * V * V * DQ['temperature'], 'Dieterici': DQ['work'] * V}[p['eq']]; b_ = V
        d = {'ab': a_ * b_, '\\f{a}{b}': a_ / b_, '\\f{a}{b^{2}}': a_ / b_ ** 2, 'ab^{2}': a_ * b_ ** 2, '\\f{b^{2}}{a}': b_ ** 2 / a_, 'a': a_, 'b': b_, '\\f{a}{b^{3}}': a_ / b_ ** 3}[p['lab']]
        return (right in DQ and DQ[right] == d) or (right.startswith('[') and parse_dim(right) == d)
    if t == 'homo':
        import u01_gen as G
        what, lhs, forms = next(h for h in G.HOMO if h[0] == p['what'])
        ok = [f[0] for f in forms if G.evald(f[1], DQ) == DQ[lhs]]
        return ok == [right]
    if t == 'expo':
        import u01_gen as G
        s = G.solve_expo(p['target'], p['bases'], DQ); assert len(s) == 1
        s = s[0]; val = sum(s) if p['ask'] == 'sum' else s['xyz'.index(p['ask'])]
        return F(right.replace('−', '-')) == val
    raise KeyError(t)

def sig_decimal(s):
    """significant figures via Decimal's own digit tuple (a second method)"""
    d = Decimal(s); digits = d.as_tuple().digits
    i = 0
    while i < len(digits) - 1 and digits[i] == 0: i += 1
    return len(digits) - i

# each constant re-derived by hand from "every added term has the same dimensions", using the DEFINITION table
_q = DQ
CONS2 = {
 'x = At + Bt^{2}': {'A': _q['length'] / _q['time'], 'B': _q['length'] / _q['time'] ** 2},
 'v = At^{2} + \\f{Bt}{C + t}': {'A': _q['speed'] * _q['time'] ** -2, 'B': _q['speed'], 'C': _q['time']},
 'F = ax^{2} + bt^{1/2} (x distance, t time)': {'a': _q['force'] * _q['length'] ** -2, 'b': _q['force'] * _q['time'] ** F(-1, 2)},
 'x = A sin(ωt) + Bt^{3} + C (x in m, t in s)': {'A': _q['length'], 'B': _q['length'] * _q['time'] ** -3, 'C': _q['length']},
 'E = \\f{B − x^{2}}{At} (E energy, x length, t time)': {'B': _q['length'] ** 2, 'A': _q['length'] ** 2 * _q['energy'] ** -1 * _q['time'] ** -1},
 'V = \\f{A√{x}}{x + B} (V energy, x length)': {'B': _q['length'], 'A': _q['energy'] * _q['length'] * _q['length'] ** F(-1, 2)},
 'P = \\f{a − t^{2}}{bx} (P pressure, x distance, t time)': {'a': _q['time'] ** 2, 'b': _q['time'] ** 2 * _q['pressure'] ** -1 * _q['length'] ** -1},
 'y = A sin(Bt − Cx) (y, x in m; t in s)': {'A': _q['length'], 'B': _q['time'] ** -1, 'C': _q['length'] ** -1},
 'F = αv + βv^{2} (F force, v speed)': {'α': _q['force'] * _q['speed'] ** -1, 'β': _q['force'] * _q['speed'] ** -2},
 'U = \\f{a}{x^{2}} − \\f{b}{x} (U energy, x distance)': {'a': _q['energy'] * _q['length'] ** 2, 'b': _q['energy'] * _q['length']},
 '(P + \\f{a}{V^{2}})(V − b) = RT': {'a': _q['pressure'] * _q['length'] ** 6, 'b': _q['length'] ** 3},
 'P = \\f{A}{Bt^{2}} + ρgBt (P pressure, t time)': {'B': _q['length'] / _q['time'], 'A': _q['pressure'] * _q['length'] * _q['time']},
}

def homo_check():
    Q = DQ; L, T_, M = Q['length'], Q['time'], Q['mass']
    assert (L / Q['acceleration']) ** F(1, 2) == T_
    assert L ** 3 / (Q['gravitational constant G'] * M) == T_ ** 2
    assert (Q['gravitational constant G'] * M / L) ** F(1, 2) == Q['speed']
    assert (Q['force'] / Q['linear mass density']) ** F(1, 2) / L == Q['frequency']
    assert Q['coefficient of viscosity'] * L * Q['speed'] == Q['force']
    assert Q['surface tension'] / (L * Q['density'] * Q['acceleration']) == L
    return True
