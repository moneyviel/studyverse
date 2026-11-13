"""Practice generators — Mathematics Unit 14: Trigonometry. Items are built from exact data (Pythagorean triples,
special angles, rational tangents); check() re-solves each numerically — evaluating the expression with the
calculator functions, counting roots by sign changes on a fine grid, and finding extreme values by scanning."""
import math, re
from fractions import Fraction as F
from common import mcq, fr
pi = math.pi
def need(x):
    if not x: raise AssertionError('retry')
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]
QN = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}
QI = {1: '0 < x < \\f{π}{2}', 2: '\\f{π}{2} < x < π', 3: 'π < x < \\f{3π}{2}', 4: '\\f{3π}{2} < x < 2π'}
def sq(q): return {1: (1, 1), 2: (1, -1), 3: (-1, -1), 4: (-1, 1)}[q]   # signs of (sin, cos)
def wr(rng, v, extra=()):
    c = list(extra) + [-v, v + 1, v - 1, 1 / v if v else F(2), v * 2, v / 2]; out = []
    for x in c:
        x = F(x)
        if x != v and fr(x) not in out: out.append(fr(x))
    rng.shuffle(out); return out
def zeros(f, lo, hi, n=60000):
    out = []; prev = None
    for k in range(n + 1):
        x = lo + (hi - lo) * k / n
        try: v = f(x)
        except (ValueError, ZeroDivisionError): prev = None; continue
        if prev is not None:
            px, pv = prev
            if pv == 0: out.append(px)
            elif pv * v < 0 and abs(pv) < 1e3 and abs(v) < 1e3:
                a, b = px, x
                for _ in range(70):
                    m = (a + b) / 2; fm = f(m)
                    if pv * fm <= 0: b = m
                    else: a, pv = m, fm
                if abs(f((a + b) / 2)) < 1e-7: out.append((a + b) / 2)
        prev = (x, v)
    if prev and prev[1] == 0: out.append(prev[0])
    d = []
    for r in sorted(out):
        if not d or r - d[-1] > 1e-7: d.append(r)
    return d

def allroots(f, lo, hi, n=120000):
    """sign-change zeros plus touching zeros (local minima of |f| that reach 0) plus zero endpoints"""
    out = zeros(f, lo, hi, n); xs = [lo + (hi - lo) * k / n for k in range(n + 1)]; vs = [abs(f(x)) for x in xs]
    for i in range(1, n):
        if vs[i] <= vs[i - 1] and vs[i] <= vs[i + 1] and vs[i] < 1e-3:
            a, b = xs[i - 1], xs[i + 1]
            for _ in range(200):
                m1, m2 = a + (b - a) / 3, b - (b - a) / 3
                if abs(f(m1)) < abs(f(m2)): b = m2
                else: a = m1
            x = (a + b) / 2
            if abs(f(x)) < 1e-10: out.append(x)
    for x in (lo, hi):
        if abs(f(x)) < 1e-10: out.append(x)
    d = []
    for r in sorted(out):
        if not d or r - d[-1] > 1e-6: d.append(r)
    return d
def g_id(rng):
    t = rng.choice(['i_quad', 'i_double', 'i_comp', 'i_tri', 'i_range', 'i_half'])
    if t == 'i_quad':
        a, b, c = rng.choice(TRI); a, b = rng.sample((a, b), 2); q = rng.randint(1, 4); ss, cs = sq(q); s, co = F(ss * a, c), F(cs * b, c)
        exprs = [('tan x + sec x', s / co + 1 / co), ('sec x − tan x', 1 / co - s / co), ('cosec x + cot x', 1 / s + co / s), ('tan^{2}x − cos x', (s / co) ** 2 - co), ('sin x + cos x', s + co), ('cot x − cosec x', co / s - 1 / s)]
        name, v = rng.choice(exprs); k = rng.choice([1, c, 2 * c, a * b]); val = k * v
        o, an = mcq(rng, fr(val), wr(rng, val))
        return dict(q=f'If sin x = {fr(s)} and x lies in the {QN[q]} quadrant, then {"" if k == 1 else k}({name}) is equal to', o=o, a=an,
                    sol=[f'In the {QN[q]} quadrant cos x = {fr(co)}, tan x = {fr(s / co)}.', f'Value = {fr(val)}.'], p=dict(t=t, s=float(s), q=q, name=name, k=k))
    if t == 'i_double':
        a, b, c = rng.choice(TRI); q = rng.randint(1, 4); ss, cs = sq(q); s, co = F(ss * a, c), F(cs * b, c); which = rng.choice(['sin 2x', 'cos 2x', 'tan 2x'])
        v = {'sin 2x': 2 * s * co, 'cos 2x': co * co - s * s, 'tan 2x': 2 * s * co / (co * co - s * s)}[which]
        o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'If tan x = {fr(s / co)} and {QI[q]}, then {which} =', o=o, a=an, sol=[f'sin x = {fr(s)}, cos x = {fr(co)}.', f'{which} = {fr(v)}.'], p=dict(t=t, tn=float(s / co), q=q, which=which))
    if t == 'i_comp':
        (a1, b1, c1), (a2, b2, c2) = rng.sample(TRI, 2); q1, q2 = rng.randint(1, 2), rng.randint(1, 2)
        sA, cA = F(a1, c1), F(sq(q1)[1] * b1, c1); sB, cB = F(sq(q2)[0] * a2, c2) if False else F(a2, c2), F(sq(q2)[1] * b2, c2)
        which = rng.choice(['sin(A + B)', 'cos(A + B)', 'sin(A − B)', 'cos(A − B)'])
        v = {'sin(A + B)': sA * cB + cA * sB, 'cos(A + B)': cA * cB - sA * sB, 'sin(A − B)': sA * cB - cA * sB, 'cos(A − B)': cA * cB + sA * sB}[which]
        o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'If sin A = {fr(sA)}, cos A {"> 0" if cA > 0 else "< 0"} and sin B = {fr(sB)}, cos B {"> 0" if cB > 0 else "< 0"}, then {which} =', o=o, a=an,
                    sol=[f'cos A = {fr(cA)}, cos B = {fr(cB)}.', f'{which} = {fr(v)}.'], p=dict(t=t, A=(float(sA), float(cA)), B=(float(sB), float(cB)), which=which))
    if t == 'i_tri':
        a, b = rng.randint(2, 15), rng.randint(2, 15); c = rng.randint(abs(a - b) + 1, a + b - 1); which = rng.choice(['A', 'B', 'C'])
        v = {'A': F(b * b + c * c - a * a, 2 * b * c), 'B': F(a * a + c * c - b * b, 2 * a * c), 'C': F(a * a + b * b - c * c, 2 * a * b)}[which]; need(v != 0)
        o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'In triangle ABC, a = {a}, b = {b}, c = {c}. Then cos {which} =', o=o, a=an, sol=['Cosine rule.', f'cos {which} = {fr(v)}.'], p=dict(t=t, s=(a, b, c), which=which))
    if t == 'i_range':
        a, b, c = rng.choice(TRI[:5]); a, b = a * rng.choice([1, -1]), b * rng.choice([1, -1]); d = rng.randint(-10, 10); ask = rng.choice(['max', 'min', 'sum of max and min', 'difference of max and min'])
        v = {'max': c + d, 'min': d - c, 'sum of max and min': 2 * d, 'difference of max and min': 2 * c}[ask]
        return dict(q=f'The {ask.replace("max", "maximum value").replace("min", "minimum value") if ask in ("max", "min") else ask} of {a} sin x {"+" if b > 0 else "−"} {abs(b)} cos x {"+" if d >= 0 else "−"} {abs(d)} (x ∈ ℝ) is ____.'.replace('−-', '−').replace(f'{a} sin', f'{a} sin'), o=None, a=v,
                    sol=['a sin x + b cos x ranges over [−√{a^{2} + b^{2}}, √{a^{2} + b^{2}}].', f'√{{{a * a} + {b * b}}} = {c} → {ask} = {v}.'], p=dict(t=t, a=a, b=b, d=d, ask=ask))
    a, b, c = rng.choice(TRI); q = rng.choice([1, 2]); co = F(b if q == 1 else -b, c); which = rng.choice(['cos^{2}\\f{x}{2}', 'sin^{2}\\f{x}{2}', 'tan^{2}\\f{x}{2}'])
    v = {'cos^{2}\\f{x}{2}': (1 + co) / 2, 'sin^{2}\\f{x}{2}': (1 - co) / 2, 'tan^{2}\\f{x}{2}': (1 - co) / (1 + co)}[which]
    o, an = mcq(rng, fr(v), wr(rng, v))
    return dict(q=f'If cos x = {fr(co)}, then {which} =', o=o, a=an, sol=['Half-angle: cos^{2}\\f{x}{2} = \\f{1 + cos x}{2}, sin^{2}\\f{x}{2} = \\f{1 − cos x}{2}.', f'= {fr(v)}.'], p=dict(t='i_half', co=float(co), which=which))

def g_inv(rng):
    t = rng.choice(['v_sum', 'v_comp', 'v_tele', 'v_dom', 'v_pv', 'v_double'])
    if t == 'v_sum':
        a, b = rng.sample(range(2, 12), 2); s = rng.choice([1, -1]); v = F(1, a) + s * F(1, b); v = v / (1 - s * F(1, a * b)); need(v != 0)
        o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'tan(tan^{{−1}}\\f{{1}}{{{a}}} {"+" if s > 0 else "−"} tan^{{−1}}\\f{{1}}{{{b}}}) =', o=o, a=an, sol=['tan(A ± B) = \\f{tan A ± tan B}{1 ∓ tan A tan B}.', f'= {fr(v)}.'], p=dict(t=t, a=a, b=b, s=s))
    if t == 'v_comp':
        a, b, c = rng.choice(TRI); a, b = rng.sample((a, b), 2); outer, inner = rng.choice([('sin', 'cos'), ('cos', 'sin'), ('tan', 'sin'), ('tan', 'cos'), ('sec', 'tan'), ('cosec', 'cot')])
        arg = {'cos': F(b, c), 'sin': F(a, c), 'tan': F(a, b), 'cot': F(b, a)}[inner]
        th = {'cos': (a, b), 'sin': (a, b), 'tan': (a, b), 'cot': (a, b)}[inner]; s_, c_ = F(th[0], c), F(th[1], c)   # angle with sin a/c, cos b/c
        v = {'sin': s_, 'cos': c_, 'tan': s_ / c_, 'sec': 1 / c_, 'cosec': 1 / s_}[outer]
        o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'{outer}({inner}^{{−1}}{fr(arg)}) =', o=o, a=an, sol=[f'The angle has sin = {fr(s_)}, cos = {fr(c_)} (first quadrant).', f'{outer} = {fr(v)}.'], p=dict(t=t, outer=outer, inner=inner, arg=float(arg)))
    if t == 'v_tele':
        n = rng.randint(3, 30); kind = rng.choice(['kk', 'two'])
        if kind == 'kk':
            v = F(n, n + 2)   # Σ tan⁻¹(1/(1 + k(k+1))) = tan⁻¹(n+1) − tan⁻¹1
            return dict(q=f'If Σ_{{k=1}}^{{{n}}} tan^{{−1}}(\\f{{1}}{{1 + k(k + 1)}}) = θ, then tan θ = ', o=mcq(rng, fr(v), wr(rng, v, [F(n, n + 1)]))[0], a=None,
                        sol=['\\f{1}{1 + k(k + 1)} = \\f{(k + 1) − k}{1 + k(k + 1)}: each term is tan^{−1}(k + 1) − tan^{−1}k.', f'θ = tan^{{−1}}{n + 1} − tan^{{−1}}1 → tan θ = \\f{{{n}}}{{{n + 2}}}.'], p=dict(t=t, n=n, kind=kind, v=v))
        v = F(2 ** n - 1, 1 + 2 ** n)   # Σ tan⁻¹(2^{k−1}/(1+2^{2k−1})) = tan⁻¹2^n − π/4
        return dict(q=f'If Σ_{{k=1}}^{{{n}}} tan^{{−1}}(\\f{{2^{{k−1}}}}{{1 + 2^{{2k−1}}}}) = θ, then tan θ = ', o=mcq(rng, fr(v), wr(rng, v, [F(2 ** n, 2 ** n + 1)]))[0], a=None,
                    sol=['Each term is tan^{−1}2^{k} − tan^{−1}2^{k−1}.', f'θ = tan^{{−1}}2^{{{n}}} − \\f{{π}}{{4}} → tan θ = \\f{{{2 ** n - 1}}}{{{2 ** n + 1}}}.'], p=dict(t=t, n=n, kind=kind, v=v))
    if t == 'v_dom':
        a = rng.choice([1, 2, 3, 4, 5]); b = rng.randint(-8, 8); c = rng.randint(1, 9); fn = rng.choice(['sin', 'cos'])
        lo, hi = F(-c - b, a), F(c - b, a); ask = rng.choice(['length', 'sum of the endpoints'])
        v = hi - lo if ask == 'length' else hi + lo; o, an = mcq(rng, fr(v), wr(rng, v))
        return dict(q=f'The domain of {fn}^{{−1}}(\\f{{{a if a > 1 else ""}x {"+" if b >= 0 else "−"} {abs(b)}}}{{{c}}}) is [p, q]. The {ask} of this interval {"is" if ask == "length" else "is p + q ="}'.replace('{1}x', 'x'), o=o, a=an,
                    sol=['Need −1 ≤ argument ≤ 1.', f'{fr(lo)} ≤ x ≤ {fr(hi)} → {fr(v)}.'], p=dict(t=t, a=a, b=b, c=c, fn=fn, ask=ask))
    if t == 'v_pv':
        fn = rng.choice(['sin', 'cos', 'tan']); deg = rng.choice([d for d in range(-360, 721, 10) if (fn != 'tan' or (d - 90) % 180)])
        v = {'sin': math.degrees(math.asin(math.sin(math.radians(deg)))), 'cos': math.degrees(math.acos(math.cos(math.radians(deg)))), 'tan': math.degrees(math.atan(math.tan(math.radians(deg))))}[fn]; v = round(v); need(abs(v) <= 180)
        return dict(q=f'The principal value of {fn}^{{−1}}({fn} {deg}°), in degrees, is ____.', o=None, a=v,
                    sol=[f'Principal range of {fn}^{{−1}}: ' + {'sin': '[−90°, 90°]', 'cos': '[0°, 180°]', 'tan': '(−90°, 90°)'}[fn] + '.', f'Find the angle in that range with the same {fn}: {v}°.'], p=dict(t=t, fn=fn, deg=deg))
    p_, q_ = rng.sample(range(1, 10), 2); need(p_ < q_ and math.gcd(p_, q_) == 1); r = F(p_, q_); which = rng.choice(['tan', 'sin', 'cos'])
    v = {'tan': 2 * r / (1 - r * r), 'sin': 2 * r / (1 + r * r), 'cos': (1 - r * r) / (1 + r * r)}[which]
    o, an = mcq(rng, fr(v), wr(rng, v))
    return dict(q=f'{which}(2 tan^{{−1}}{fr(r)}) =', o=o, a=an, sol=['With t = tan θ: tan 2θ = \\f{2t}{1 − t^{2}}, sin 2θ = \\f{2t}{1 + t^{2}}, cos 2θ = \\f{1 − t^{2}}{1 + t^{2}}.', f'= {fr(v)}.'], p=dict(t='v_double', r=float(r), which=which))

def g_eqn(rng):
    t = rng.choice(['e_quad', 'e_lin', 'e_sum', 'e_mult'])
    if t == 'e_quad':
        fn = rng.choice(['sin', 'cos']); r1 = rng.choice([F(1, 2), F(-1, 2), F(0), F(1), F(-1), F(1, 3), F(2, 3), F(-1, 4)]); r2 = rng.choice([F(2), F(-2), F(3), F(1, 2), F(-1, 2), F(3, 4)]); need(r1 != r2)
        A, B, C = 1, -(r1 + r2), r1 * r2; den = math.lcm(B.denominator, C.denominator); A, B, C = den, int(B * den), int(C * den)
        lo, hi = rng.choice([(0, 2), (-1, 1), (0, 4), (-2, 2), (0, 3), (-1, 3)])
        f = (lambda x: A * math.sin(x) ** 2 + B * math.sin(x) + C) if fn == 'sin' else (lambda x: A * math.cos(x) ** 2 + B * math.cos(x) + C)
        n = len(allroots(f, lo * pi, hi * pi)); need(n > 0)
        txt = f'{A if A > 1 else ""}{fn}^{{2}}x {"+" if B >= 0 else "−"} {abs(B)} {fn} x {"+" if C >= 0 else "−"} {abs(C)} = 0'.replace(' 1 sin', ' sin').replace(' 1 cos', ' cos').replace(' + 0 = 0', ' = 0').replace(' − 0 = 0', ' = 0').replace(' + 0 sin x', '').replace(' + 0 cos x', '')
        return dict(q=f'The number of solutions of {txt} in [{lo if lo else 0}π, {hi}π] is ____.'.replace('[0π', '[0').replace('[-1π', '[−π').replace('[-2π', '[−2π').replace(', 1π]', ', π]'), o=None, a=n,
                    sol=[f'Solve the quadratic for {fn} x: roots {fr(r1)} and {fr(r2)}; only values in [−1, 1] count.', f'Count the angles on the interval: {n}.'], p=dict(t=t, fn=fn, abc=(A, B, C), lo=lo, hi=hi))
    if t == 'e_lin':
        a, b, c = rng.choice(TRI[:5]); a, b = a * rng.choice([1, -1]), b * rng.choice([1, -1]); k = rng.randint(-c, c); lo, hi = rng.choice([(0, 2), (-1, 1), (0, 4), (-2, 2), (0, 3)])
        need(abs(k) != c); ph = math.atan2(b, a); base = math.asin(k / c); sols = set()
        for mm in range(-10, 11):
            for x in (base - ph + 2 * mm * pi, pi - base - ph + 2 * mm * pi):
                if lo * pi - 1e-9 <= x <= hi * pi + 1e-9: sols.add(round(x, 9))
        n = len(sols)
        return dict(q=f'The number of solutions of {a} sin x {"+" if b > 0 else "−"} {abs(b)} cos x = {k} in [{lo}π, {hi}π] is ____.'.replace('[0π', '[0').replace('[-1π', '[−π').replace('[-2π', '[−2π').replace(', 1π]', ', π]'), o=None, a=n,
                    sol=[f'Write as {c} sin(x + φ) = {k}: |k| < {c}, so two solutions per period.', f'Count on the interval: {n}.'], p=dict(t=t, a=a, b=b, k=k, lo=lo, hi=hi))
    if t == 'e_sum':
        fn = rng.choice(['sin', 'cos', 'tan']); val = rng.choice({'sin': ['\\f{1}{2}', '−\\f{1}{2}', '\\f{√{3}}{2}', '\\f{1}{√{2}}'], 'cos': ['\\f{1}{2}', '−\\f{1}{2}', '\\f{√{3}}{2}', '−\\f{1}{√{2}}'], 'tan': ['1', '√{3}', '−1', '\\f{1}{√{3}}']}[fn])
        nv = {'\\f{1}{2}': 0.5, '−\\f{1}{2}': -0.5, '\\f{√{3}}{2}': math.sqrt(3) / 2, '\\f{1}{√{2}}': 1 / math.sqrt(2), '−\\f{1}{√{2}}': -1 / math.sqrt(2), '1': 1, '√{3}': math.sqrt(3), '−1': -1, '\\f{1}{√{3}}': 1 / math.sqrt(3)}[val]
        hi = rng.randint(1, 4); f = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[fn]; zs = zeros(lambda x: f(x) - nv, 0, hi * pi); need(zs)
        S = F(sum(zs) / pi).limit_denominator(12); need(abs(float(S) * pi - sum(zs)) < 1e-6)
        o, an = mcq(rng, fr(S) + 'π', [fr(x) + 'π' for x in (S + F(1, 2), S - F(1, 2) if S > F(1, 2) else S + 1, S * 2, S + F(1, 3), S / 2)])
        return dict(q=f'The sum of all solutions of {fn} x = {val} in [0, {hi if hi > 1 else ""}π] is', o=o, a=an,
                    sol=[f'List the solutions of {fn} x = {val} in [0, {hi}π].', f'They add to {fr(S)}π.'], p=dict(t=t, fn=fn, nv=nv, hi=hi))
    m, n = rng.sample(range(1, 8), 2); fn = rng.choice(['sin', 'cos']); lo, hi = rng.choice([(0, 1), (-1, 1), (0, 2)])
    sols = set()
    for k in range(-40, 41):
        for x in ([2 * k * pi / (m - n), (2 * k + 1) * pi / (m + n)] if fn == 'sin' else [2 * k * pi / (m - n), 2 * k * pi / (m + n)]):
            if lo * pi - 1e-9 <= x <= hi * pi + 1e-9: sols.add(round(x, 9))
    cnt = len(sols)
    return dict(q=f'The number of solutions of {fn} {m if m > 1 else ""}x = {fn} {n if n > 1 else ""}x in [{lo}π, {hi}π] is ____.'.replace('[0π', '[0').replace('[-1π', '[−π').replace(', 1π]', ', π]'), o=None, a=cnt,
                sol=[f'{fn} A = {fn} B ⇔ ' + ('A = 2kπ + B or A = (2k + 1)π − B.' if fn == 'sin' else 'A = 2kπ ± B.'), f'List those in the interval (removing repeats): {cnt}.'], p=dict(t='e_mult', m=m, n=n, fn=fn, lo=lo, hi=hi))

def robust(gf):
    def w(rng):
        for _ in range(800):
            try:
                it = gf(rng)
                if it['p']['t'] == 'v_tele' and it['a'] is None: it['a'] = it['o'].index(fr(it['p']['v']))
                return it
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(id=g_id, inv=g_inv, eqn=g_eqn).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def tofr(s):
    s = s.replace('−', '-').replace('π', ''); neg = s.startswith('-'); s = s.lstrip('-')
    v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def close(a, b, tol=1e-7): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = tofr(R) if isinstance(R, str) else R
    if t in ('i_quad', 'i_double', 'i_half'):
        if t == 'i_quad':   # find the actual angle in the quadrant with that sine
            base = math.asin(abs(p['s'])); x = {1: base, 2: pi - base, 3: pi + base, 4: 2 * pi - base}[p['q']]; assert abs(math.sin(x) - p['s']) < 1e-12
            e = {'tan x + sec x': math.tan(x) + 1 / math.cos(x), 'sec x − tan x': 1 / math.cos(x) - math.tan(x), 'cosec x + cot x': 1 / math.sin(x) + 1 / math.tan(x), 'tan^{2}x − cos x': math.tan(x) ** 2 - math.cos(x), 'sin x + cos x': math.sin(x) + math.cos(x), 'cot x − cosec x': 1 / math.tan(x) - 1 / math.sin(x)}[p['name']]
            return close(V, p['k'] * e)
        if t == 'i_double':
            base = math.atan(abs(p['tn'])); x = {1: base, 2: pi - base, 3: pi + base, 4: 2 * pi - base}[p['q']]; assert abs(math.tan(x) - p['tn']) < 1e-9
            return close(V, {'sin 2x': math.sin(2 * x), 'cos 2x': math.cos(2 * x), 'tan 2x': math.tan(2 * x)}[p['which']])
        x = math.acos(p['co']); return close(V, {'cos^{2}\\f{x}{2}': math.cos(x / 2) ** 2, 'sin^{2}\\f{x}{2}': math.sin(x / 2) ** 2, 'tan^{2}\\f{x}{2}': math.tan(x / 2) ** 2}[p['which']])
    if t == 'i_comp':
        A = math.atan2(*p['A']); B = math.atan2(*p['B'])
        return close(V, {'sin(A + B)': math.sin(A + B), 'cos(A + B)': math.cos(A + B), 'sin(A − B)': math.sin(A - B), 'cos(A − B)': math.cos(A - B)}[p['which']])
    if t == 'i_tri':   # build the triangle with coordinates and measure the angle
        a, b, c = p['s']; B_ = (c, 0); x = (b * b + c * c - a * a) / (2 * c); C_ = (x, math.sqrt(max(0, b * b - x * x))); A_ = (0, 0)
        def ang(P, Q, R):
            u = (Q[0] - P[0], Q[1] - P[1]); v = (R[0] - P[0], R[1] - P[1]); return math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v)))
        th = {'A': ang(A_, B_, C_), 'B': ang(B_, A_, C_), 'C': ang(C_, A_, B_)}[p['which']]; return close(V, math.cos(th))
    if t == 'i_range':
        vals = [p['a'] * math.sin(x) + p['b'] * math.cos(x) + p['d'] for x in [2 * pi * k / 200000 for k in range(200000)]]; M, m = max(vals), min(vals)
        return close(V, {'max': M, 'min': m, 'sum of max and min': M + m, 'difference of max and min': M - m}[p['ask']], 1e-6)
    if t == 'v_sum': return close(V, math.tan(math.atan(1 / p['a']) + p['s'] * math.atan(1 / p['b'])))
    if t == 'v_comp':
        inv = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan, 'cot': lambda y: math.atan(1 / y)}[p['inner']](p['arg'])
        return close(V, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sec': lambda u: 1 / math.cos(u), 'cosec': lambda u: 1 / math.sin(u)}[p['outer']](inv))
    if t == 'v_tele':
        n = p['n']; s = sum(math.atan(1 / (1 + k * (k + 1))) for k in range(1, n + 1)) if p['kind'] == 'kk' else sum(math.atan(2 ** (k - 1) / (1 + 2 ** (2 * k - 1))) for k in range(1, n + 1))
        return close(V, math.tan(s))
    if t == 'v_dom':
        f = math.asin if p['fn'] == 'sin' else math.acos; ok = []
        for k in range(-60000, 60001):
            x = k / 1000
            try: f((p['a'] * x + p['b']) / p['c']); ok.append(x)
            except ValueError: pass
        lo, hi = min(ok), max(ok); return close(V, (hi - lo) if p['ask'] == 'length' else (hi + lo), 1e-3)
    if t == 'v_pv':
        r = math.radians(p['deg']); v = {'sin': math.asin(math.sin(r)), 'cos': math.acos(math.cos(r)), 'tan': math.atan(math.tan(r))}[p['fn']]; return abs(math.degrees(v) - V) < 1e-6
    if t == 'v_double': return close(V, {'tan': math.tan, 'sin': math.sin, 'cos': math.cos}[p['which']](2 * math.atan(p['r'])))
    if t == 'e_quad':
        A, B, C = p['abc']; g = math.sin if p['fn'] == 'sin' else math.cos
        # independent: count x on a fine grid where g(x) equals one of the quadratic's roots in [−1, 1]
        d = B * B - 4 * A * C; rts = [(-B + s * math.sqrt(d)) / (2 * A) for s in (1, -1)] if d >= 0 else []; rts = {round(r, 12) for r in rts if -1 <= r <= 1}
        cnt = 0
        for r in rts:
            if abs(abs(r) - 1) < 1e-12:   # touching values: count exact points
                base = (pi / 2 if r > 0 else -pi / 2) if p['fn'] == 'sin' else (0 if r > 0 else pi)
                cnt += sum(1 for k in range(-10, 11) if p['lo'] * pi - 1e-9 <= base + 2 * k * pi <= p['hi'] * pi + 1e-9)
            else:
                cnt += len(allroots(lambda x, r=r: g(x) - r, p['lo'] * pi, p['hi'] * pi))
        return V == cnt
    if t == 'e_lin': return V == len(allroots(lambda x: p['a'] * math.sin(x) + p['b'] * math.cos(x) - p['k'], p['lo'] * pi, p['hi'] * pi))
    if t == 'e_sum':
        fn = rng.choice(['sin', 'cos', 'tan']); val = rng.choice({'sin': ['\\f{1}{2}', '−\\f{1}{2}', '\\f{√{3}}{2}', '\\f{1}{√{2}}'], 'cos': ['\\f{1}{2}', '−\\f{1}{2}', '\\f{√{3}}{2}', '−\\f{1}{√{2}}'], 'tan': ['1', '√{3}', '−1', '\\f{1}{√{3}}']}[fn])
        nv = {'\\f{1}{2}': 0.5, '−\\f{1}{2}': -0.5, '\\f{√{3}}{2}': math.sqrt(3) / 2, '\\f{1}{√{2}}': 1 / math.sqrt(2), '−\\f{1}{√{2}}': -1 / math.sqrt(2), '1': 1, '√{3}': math.sqrt(3), '−1': -1, '\\f{1}{√{3}}': 1 / math.sqrt(3)}[val]
        hi = rng.randint(1, 4); f = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[fn]; zs = zeros(lambda x: f(x) - nv, 0, hi * pi); need(zs)
        S = F(sum(zs) / pi).limit_denominator(12); need(abs(float(S) * pi - sum(zs)) < 1e-6)
        o, an = mcq(rng, fr(S) + 'π', [fr(x) + 'π' for x in (S + F(1, 2), S - F(1, 2) if S > F(1, 2) else S + 1, S * 2, S + F(1, 3), S / 2)])
        return dict(q=f'The sum of all solutions of {fn} x = {val} in [0, {hi if hi > 1 else ""}π] is', o=o, a=an,
                    sol=[f'List the solutions of {fn} x = {val} in [0, {hi}π].', f'They add to {fr(S)}π.'], p=dict(t=t, fn=fn, nv=nv, hi=hi))
    m, n = rng.sample(range(1, 8), 2); fn = rng.choice(['sin', 'cos']); lo, hi = rng.choice([(0, 1), (-1, 1), (0, 2)])
    sols = set()
    for k in range(-40, 41):
        for x in ([2 * k * pi / (m - n), (2 * k + 1) * pi / (m + n)] if fn == 'sin' else [2 * k * pi / (m - n), 2 * k * pi / (m + n)]):
            if lo * pi - 1e-9 <= x <= hi * pi + 1e-9: sols.add(round(x, 9))
    cnt = len(sols)
    return dict(q=f'The number of solutions of {fn} {m if m > 1 else ""}x = {fn} {n if n > 1 else ""}x in [{lo}π, {hi}π] is ____.'.replace('[0π', '[0').replace('[-1π', '[−π').replace(', 1π]', ', π]'), o=None, a=cnt,
                sol=[f'{fn} A = {fn} B ⇔ ' + ('A = 2kπ + B or A = (2k + 1)π − B.' if fn == 'sin' else 'A = 2kπ ± B.'), f'List those in the interval (removing repeats): {cnt}.'], p=dict(t='e_mult', m=m, n=n, fn=fn, lo=lo, hi=hi))

def robust(gf):
    def w(rng):
        for _ in range(800):
            try:
                it = gf(rng)
                if it['p']['t'] == 'v_tele' and it['a'] is None: it['a'] = it['o'].index(fr(it['p']['v']))
                return it
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(id=g_id, inv=g_inv, eqn=g_eqn).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def tofr(s):
    s = s.replace('−', '-').replace('π', ''); neg = s.startswith('-'); s = s.lstrip('-')
    v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def close(a, b, tol=1e-7): return abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = tofr(R) if isinstance(R, str) else R
    if t in ('i_quad', 'i_double', 'i_half'):
        if t == 'i_quad':   # find the actual angle in the quadrant with that sine
            base = math.asin(abs(p['s'])); x = {1: base, 2: pi - base, 3: pi + base, 4: 2 * pi - base}[p['q']]; assert abs(math.sin(x) - p['s']) < 1e-12
            e = {'tan x + sec x': math.tan(x) + 1 / math.cos(x), 'sec x − tan x': 1 / math.cos(x) - math.tan(x), 'cosec x + cot x': 1 / math.sin(x) + 1 / math.tan(x), 'tan^{2}x − cos x': math.tan(x) ** 2 - math.cos(x), 'sin x + cos x': math.sin(x) + math.cos(x), 'cot x − cosec x': 1 / math.tan(x) - 1 / math.sin(x)}[p['name']]
            return close(V, p['k'] * e)
        if t == 'i_double':
            base = math.atan(abs(p['tn'])); x = {1: base, 2: pi - base, 3: pi + base, 4: 2 * pi - base}[p['q']]; assert abs(math.tan(x) - p['tn']) < 1e-9
            return close(V, {'sin 2x': math.sin(2 * x), 'cos 2x': math.cos(2 * x), 'tan 2x': math.tan(2 * x)}[p['which']])
        x = math.acos(p['co']); return close(V, {'cos^{2}\\f{x}{2}': math.cos(x / 2) ** 2, 'sin^{2}\\f{x}{2}': math.sin(x / 2) ** 2, 'tan^{2}\\f{x}{2}': math.tan(x / 2) ** 2}[p['which']])
    if t == 'i_comp':
        A = math.atan2(*p['A']); B = math.atan2(*p['B'])
        return close(V, {'sin(A + B)': math.sin(A + B), 'cos(A + B)': math.cos(A + B), 'sin(A − B)': math.sin(A - B), 'cos(A − B)': math.cos(A - B)}[p['which']])
    if t == 'i_tri':   # build the triangle with coordinates and measure the angle
        a, b, c = p['s']; B_ = (c, 0); x = (b * b + c * c - a * a) / (2 * c); C_ = (x, math.sqrt(max(0, b * b - x * x))); A_ = (0, 0)
        def ang(P, Q, R):
            u = (Q[0] - P[0], Q[1] - P[1]); v = (R[0] - P[0], R[1] - P[1]); return math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v)))
        th = {'A': ang(A_, B_, C_), 'B': ang(B_, A_, C_), 'C': ang(C_, A_, B_)}[p['which']]; return close(V, math.cos(th))
    if t == 'i_range':
        vals = [p['a'] * math.sin(x) + p['b'] * math.cos(x) + p['d'] for x in [2 * pi * k / 200000 for k in range(200000)]]; M, m = max(vals), min(vals)
        return close(V, {'max': M, 'min': m, 'sum of max and min': M + m, 'difference of max and min': M - m}[p['ask']], 1e-6)
    if t == 'v_sum': return close(V, math.tan(math.atan(1 / p['a']) + p['s'] * math.atan(1 / p['b'])))
    if t == 'v_comp':
        inv = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan, 'cot': lambda y: math.atan(1 / y)}[p['inner']](p['arg'])
        return close(V, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sec': lambda u: 1 / math.cos(u), 'cosec': lambda u: 1 / math.sin(u)}[p['outer']](inv))
    if t == 'v_tele':
        n = p['n']; s = sum(math.atan(1 / (1 + k * (k + 1))) for k in range(1, n + 1)) if p['kind'] == 'kk' else sum(math.atan(2 ** (k - 1) / (1 + 2 ** (2 * k - 1))) for k in range(1, n + 1))
        return close(V, math.tan(s))
    if t == 'v_dom':
        f = math.asin if p['fn'] == 'sin' else math.acos; ok = []
        for k in range(-60000, 60001):
            x = k / 1000
            try: f((p['a'] * x + p['b']) / p['c']); ok.append(x)
            except ValueError: pass
        lo, hi = min(ok), max(ok); return close(V, (hi - lo) if p['ask'] == 'length' else (hi + lo), 1e-3)
    if t == 'v_pv':
        r = math.radians(p['deg']); v = {'sin': math.asin(math.sin(r)), 'cos': math.acos(math.cos(r)), 'tan': math.atan(math.tan(r))}[p['fn']]; return abs(math.degrees(v) - V) < 1e-6
    if t == 'v_double': return close(V, {'tan': math.tan, 'sin': math.sin, 'cos': math.cos}[p['which']](2 * math.atan(p['r'])))
    if t == 'e_quad':
        A, B, C = p['abc']; g = math.sin if p['fn'] == 'sin' else math.cos
        # independent: count x on a fine grid where g(x) equals one of the quadratic's roots in [−1, 1]
        d = B * B - 4 * A * C; rts = [(-B + s * math.sqrt(d)) / (2 * A) for s in (1, -1)] if d >= 0 else []; rts = {round(r, 12) for r in rts if -1 <= r <= 1}
        cnt = 0
        for r in rts:
            if abs(abs(r) - 1) < 1e-12:   # touching values: count exact points
                base = (pi / 2 if r > 0 else -pi / 2) if p['fn'] == 'sin' else (0 if r > 0 else pi)
                cnt += sum(1 for k in range(-10, 11) if p['lo'] * pi - 1e-9 <= base + 2 * k * pi <= p['hi'] * pi + 1e-9)
            else:
                cnt += len(allroots(lambda x, r=r: g(x) - r, p['lo'] * pi, p['hi'] * pi))
        return V == cnt
    if t == 'e_lin':
        c = math.hypot(p['a'], p['b']); ph = math.atan2(p['b'], p['a']); k = p['k']   # c·sin(x + φ) = k
        base = math.asin(k / c); sols = set()
        for m in range(-10, 11):
            for x in (base - ph + 2 * m * pi, pi - base - ph + 2 * m * pi):
                if p['lo'] * pi - 1e-9 <= x <= p['hi'] * pi + 1e-9: sols.add(round(x, 9))
        return V == len(sols)
    if t == 'e_sum':
        f = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan}[p['fn']]; b = f(p['nv']); sols = set()
        for m in range(-10, 11):
            cand = {'sin': (b + 2 * m * pi, pi - b + 2 * m * pi), 'cos': (b + 2 * m * pi, -b + 2 * m * pi), 'tan': (b + m * pi,)}[p['fn']]
            for x in cand:
                if -1e-9 <= x <= p['hi'] * pi + 1e-9: sols.add(round(x, 9))
        return close(float(V) * pi, sum(sols))
    if t == 'e_mult':
        m, n = p['m'], p['n']; f = (lambda x: math.sin(m * x) - math.sin(n * x)) if p['fn'] == 'sin' else (lambda x: math.cos(m * x) - math.cos(n * x))
        return V == len(allroots(f, p['lo'] * pi, p['hi'] * pi))
    raise KeyError(t)
