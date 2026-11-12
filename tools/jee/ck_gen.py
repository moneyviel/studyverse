"""Practice generators — Chemistry Unit 8: Chemical Kinetics. Every item carries its parameters p;
check() re-solves it a different way (numerical integration / base-10 or base-2 forms) before it is accepted."""
import math
from fractions import Fraction as F
from common import mcq, nf
R = 8.314
def ok_round(x): return abs(x - round(x)) < 0.4 and abs(x - round(x)) != 0.5
def safe(x): return abs(x - math.floor(x) - 0.5) > 0.12   # stay away from .5 rounding edges

# ---------------- rate law & order ----------------
UNIT = {0: 'mol L^{−1} s^{−1}', 1: 's^{−1}', 2: 'L mol^{−1} s^{−1}', 3: 'L^{2} mol^{−2} s^{−1}'}
def g_order(rng):
    t = rng.choice(['ratio', 'data', 'two', 'unit', 'stoich', 'halfl'])
    if t == 'ratio':
        a, b = rng.choice([(1, 1), (2, 1), (1, 2), (2, 0), (0, 1), (2, 2), (1, 0), (3, 0)]); fa, fb = rng.choice([(2, 2), (2, 3), (3, 1), (2, F(1, 2)), (3, 2), (F(1, 2), 2), (4, 1), (2, 1)])
        v = F(fa) ** a * F(fb) ** b
        def tx(f): return f'halved' if f == F(1, 2) else f'unchanged' if f == 1 else f'made {f} times'
        q = f'For rate = k[A]^{{{a}}}[B]^{{{b}}}, [A] is {tx(fa)} and [B] is {tx(fb)}. The rate becomes ______ times the original.'
        if v.denominator == 1 and v < 1000:
            return dict(q=q, o=None, a=int(v), sol=[f'New/old = ({fa})^{{{a}}} × ({fb})^{{{b}}} = {v}.'.replace('1/2', '½')], p=dict(t='ratio', a=a, b=b, fa=str(fa), fb=str(fb)))
        return g_order(rng)
    if t == 'data':
        n = rng.choice([0, 1, 2, 3]); f = rng.choice([2, 3, 4]); c1 = rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]); r1 = rng.choice([1.2e-3, 2.5e-4, 4.0e-3, 6.0e-5, 3.6e-2])
        r2 = r1 * f ** n
        q = f'For the reaction A → products, the initial rate is {nf(r1, 3)} mol L^{{−1}} s^{{−1}} at [A] = {nf(c1)} M and {nf(r2, 3)} mol L^{{−1}} s^{{−1}} at [A] = {nf(c1 * f)} M. The order of the reaction with respect to A is ______.'
        return dict(q=q, o=None, a=n, sol=[f'[A] × {f} changes the rate × {nf(r2 / r1, 3)}.', f'{f}^{{n}} = {nf(r2 / r1, 3)} → n = {n}.'], p=dict(t='data', c1=c1, c2=c1 * f, r1=r1, r2=r2))
    if t == 'two':
        a, b = rng.choice([(1, 1), (1, 2), (2, 1), (2, 0), (0, 2), (1, 0), (2, 2)]); k = rng.choice([0.3, 0.6, 1.2, 2.4, 6.0])
        A1, B1 = rng.choice([0.1, 0.2]), rng.choice([0.1, 0.2]); fA, fB = rng.choice([2, 3, 4]), rng.choice([2, 3])
        ex = [(A1, B1), (A1 * fA, B1), (A1, B1 * fB)]; rows = [(x, y, k * x ** a * y ** b) for x, y in ex]
        rng.shuffle(rows)
        tb = '; '.join(f'[A] = {nf(x, 3)} M, [B] = {nf(y, 3)} M, rate = {nf(r, 3)} M s^{{−1}}' for x, y, r in rows)
        q = f'Initial-rate data for A + B → products: {tb}. The overall order of the reaction is ______.'
        return dict(q=q, o=None, a=a + b, sol=[f'Keep [B] fixed, [A] × {fA} → rate × {fA ** a} → order in A = {a}.', f'Keep [A] fixed, [B] × {fB} → rate × {fB ** b} → order in B = {b}.', f'Overall = {a + b}.'], p=dict(t='two', rows=rows))
    if t == 'unit':
        n = rng.choice([0, 1, 2, 3])
        q = f'The rate constant of a reaction has the unit {UNIT[n]}. The order of the reaction is :'
        o, a = mcq(rng, ['zero', 'first', 'second', 'third'][n], ['zero', 'first', 'second', 'third'])
        return dict(q=q, o=o, a=a, sol=['Unit of k = (mol L^{−1})^{1 − n} s^{−1}.', f'Here → n = {n}.'], p=dict(t='unit', n=n))
    if t == 'stoich':
        eq = rng.choice([('2N_{2}O_{5}', 2, '4NO_{2}', 4), ('2HI', 2, 'H_{2}', 1), ('N_{2}', 1, '2NH_{3}', 2), ('2NO', 2, 'N_{2}O_{2}', 1), ('2NH_{3}', 2, '3H_{2}', 3), ('2O_{3}', 2, '3O_{2}', 3)])
        ra, na, rb, nb = eq; d = rng.choice([1.2e-3, 2.4e-2, 6.0e-4, 3.0e-3, 4.8e-2]); v = d * nb / na
        q = f'In the reaction {ra} → {rb} + …, reactant disappears at {nf(d)} mol L^{{−1}} s^{{−1}}. The rate of formation of {rb[1:] if rb[0].isdigit() else rb} is :'
        o, a = mcq(rng, nf(v) + ' mol L^{−1} s^{−1}', [nf(x) + ' mol L^{−1} s^{−1}' for x in (d * na / nb, d, d * nb, d / na, d * 2 * nb / na)])
        return dict(q=q, o=o, a=a, sol=[f'Rates divided by coefficients are equal: \\f{{1}}{{{na}}}(−\\f{{Δ[R]}}{{Δt}}) = \\f{{1}}{{{nb}}}\\f{{Δ[P]}}{{Δt}}.', f'Rate of formation = {nf(d)} × \\f{{{nb}}}{{{na}}} = {nf(v)}.'], p=dict(t='stoich', na=na, nb=nb, d=d))
    n = rng.choice([0, 1, 2]); f = rng.choice([2, 4]); h1 = rng.choice([10, 20, 30, 40, 60])
    h2 = h1 * F(f) ** (1 - n)
    q = f'When the initial concentration of a reactant is made {f} times, its half-life changes from {h1} min to {nf(float(h2))} min. The order of the reaction is ______.'
    return dict(q=q, o=None, a=n, sol=['t_{1/2} ∝ [A]_{0}^{1 − n}.', f'{f}^{{1 − n}} = {nf(float(h2 / h1))} → n = {n}.'], p=dict(t='halfl', f=f, h1=h1, h2=float(h2)))

# ---------------- first order ----------------
def g_first(rng):
    t = rng.choice(['pct', 'left', 'tratio', 'twor', 'age', 'race', 'k'])
    if t == 'pct':
        th = rng.choice([5, 6.93, 10, 13.86, 15, 20, 23.1, 30, 34.65, 40, 69.3]); p = rng.choice([50, 75, 87.5, 90, 99, 99.9, 80, 60])
        v = th * math.log(100 / (100 - p)) / math.log(2)
        if not safe(v): return g_first(rng)
        q = f'The half-life of a first order reaction is {nf(th)} min. The time required for {nf(p)}% completion is ______ min. (nearest integer)'
        return dict(q=q, o=None, a=round(v), sol=[f'k = \\f{{0.693}}{{{nf(th)}}} min^{{−1}}.', f't = \\f{{2.303}}{{k}}log\\f{{100}}{{{nf(100 - p)}}} ≈ {v:.2f} min.'], p=dict(t='pct', th=th, pc=p))
    if t == 'left':
        th = rng.choice([2, 3, 5, 8, 10, 12, 15, 20]); n = rng.choice([1, 2, 3, 4, 5]); m0 = rng.choice([80, 160, 320, 640, 100, 400])
        q = f'A first order reaction has t_{{1/2}} = {th} h. Starting with {m0} g, the mass left after {th * n} h is :'
        v = m0 / 2 ** n
        o, a = mcq(rng, nf(v) + ' g', [nf(x) + ' g' for x in (m0 / 2 / n, m0 / 2 ** (n + 1), m0 / 2 ** (n - 1), m0 - m0 / 2 ** n, m0 / n)])
        return dict(q=q, o=o, a=a, sol=[f'{th * n} h = {n} half-lives.', f'Left = {m0} × (½)^{{{n}}} = {nf(v)} g.'], p=dict(t='left', th=th, tt=th * n, m0=m0))
    if t == 'tratio':
        a_, b_ = rng.sample([(50, 2), (75, 4), (87.5, 8), (90, 10), (99, 100), (99.9, 1000), (93.75, 16), (96.875, 32)], 2)
        v = math.log(a_[1]) / math.log(b_[1])
        if abs(v * 100 - round(v * 100)) > 1e-6 and not safe(v * 10): return g_first(rng)
        q = f'For a first order reaction, the ratio t_{{{nf(a_[0])}%}} : t_{{{nf(b_[0])}%}} is :'
        right = f'{v:.2f}'.rstrip('0').rstrip('.')
        o, a = mcq(rng, right, [f'{x:.2f}'.rstrip('0').rstrip('.') for x in (a_[0] / b_[0], 1 / v, v * 2, v / 2, (100 - b_[0]) / (100 - a_[0]))])
        return dict(q=q, o=o, a=a, sol=['t ∝ log\\f{[A]_{0}}{[A]}.', f'= \\f{{log {a_[1]}}}{{log {b_[1]}}} ≈ {right}.'], p=dict(t='tratio', f1=a_[1], f2=b_[1]))
    if t == 'twor':
        r1, r2 = rng.choice([(0.04, 0.03), (0.08, 0.04), (0.09, 0.06), (0.05, 0.04), (0.12, 0.08), (0.06, 0.03), (0.16, 0.12)]); dt = rng.choice([5, 10, 15, 20, 30])
        v = dt * math.log(2) / math.log(r1 / r2)
        if not safe(v): return g_first(rng)
        q = f'The rate of a first order reaction is {r1} mol L^{{−1}} s^{{−1}} at some instant and {r2} mol L^{{−1}} s^{{−1}} {dt} minutes later. Its half-life is ______ minutes. (nearest integer)'
        return dict(q=q, o=None, a=round(v), sol=['First order: rate ∝ [A] → \\f{[A]_{1}}{[A]_{2}} = \\f{r_{1}}{r_{2}}.', f'k = \\f{{2.303}}{{{dt}}}log\\f{{{r1}}}{{{r2}}}; t_{{1/2}} = \\f{{0.693}}{{k}} ≈ {v:.1f} min.'], p=dict(t='twor', r1=r1, r2=r2, dt=dt))
    if t == 'age':
        n = rng.choice([2, 3, 4, 5]); iso = rng.choice([('^{14}C', 5730, 'years'), ('^{3}H', 12, 'years'), ('^{32}P', 14, 'days'), ('^{131}I', 8, 'days'), ('^{60}Co', 5, 'years')])
        q = f'The activity of {iso[0]} (t_{{1/2}} = {iso[1]} {iso[2]}) in a sample is \\f{{1}}{{{2 ** n}}} of its original value. Time elapsed is ______ {iso[2]}.'
        return dict(q=q, o=None, a=n * iso[1], sol=[f'\\f{{1}}{{{2 ** n}}} = (½)^{{{n}}} → {n} half-lives.', f'Time = {n} × {iso[1]} = {n * iso[1]} {iso[2]}.'], p=dict(t='age', fr=2 ** n, th=iso[1]))
    if t == 'race':
        m = rng.choice([1, 2, 3]); hA = rng.choice([5, 10, 15, 20]); hB = hA * rng.choice([2, 3, 4])
        v = m / (F(1, hA) - F(1, hB))
        if v.denominator != 1: return g_first(rng)
        q = f'Two first order reactants start together with [A]_{{0}} = {2 ** m}[B]_{{0}}. Their half-lives are {hA} min (A) and {hB} min (B). After how long will [A] = [B]?'
        o, a = mcq(rng, f'{int(v)} min', [f'{x} min' for x in (int(v) * 2, int(v) // 2, m * hA, m * hB, hA + hB, int(v) + hA)])
        return dict(q=q, o=o, a=a, sol=[f'{2 ** m}·2^{{−t/{hA}}} = 2^{{−t/{hB}}} → {m} = t(\\f{{1}}{{{hA}}} − \\f{{1}}{{{hB}}}).', f't = {int(v)} min.'], p=dict(t='race', m=m, hA=hA, hB=hB))
    c0 = rng.choice([0.8, 1.0, 0.5, 0.64, 2.0]); f = rng.choice([2, 4, 10, 100, 8]); tt = rng.choice([10, 20, 23.03, 30, 46.06, 69.3, 50])
    k = math.log(f) / tt
    q = f'In a first order reaction the concentration falls from {nf(c0)} M to {nf(c0 / f, 3)} M in {nf(tt)} min. The rate constant is :'
    o, a = mcq(rng, nf(k, 3) + ' min^{−1}', [nf(x, 3) + ' min^{−1}' for x in (math.log10(f) / tt, f / tt, k * 2, (c0 - c0 / f) / tt, k / 2)])
    return dict(q=q, o=o, a=a, sol=[f'k = \\f{{2.303}}{{t}}log\\f{{[A]_{{0}}}}{{[A]}} = \\f{{2.303}}{{{nf(tt)}}}log {f}.', f'k ≈ {nf(k, 3)} min^{{−1}}.'], p=dict(t='kfirst', f=f, tt=tt))

# ---------------- gas phase (pressure) ----------------
GAS = [('A(g) → B(g) + C(g)', 2), ('A(g) → 2B(g) + C(g)', 3), ('A(g) → 2B(g)', 2), ('2A(g) → 4B(g) + C(g)', F(5, 2)), ('A(g) → 3B(g)', 3)]
def g_gas(rng):
    eq, nu = rng.choice(GAS); nu = F(nu); P0 = rng.choice([40, 80, 100, 120, 160, 200, 0.4, 0.6, 1.0])
    t = rng.choice(['pA', 'k', 'P0'])
    f = rng.choice([2, 4, 8, 10]); x = F(P0) * (1 - F(1, f)) if not isinstance(P0, float) else P0 * (1 - 1 / f)
    Pt = float(P0) + float(nu - 1) * float(x); unit = 'atm' if isinstance(P0, float) else 'mm Hg'
    if t == 'pA':
        q = f'The first order reaction {eq} is started with pure A at {nf(P0)} {unit}. When the total pressure is {nf(Pt, 4)} {unit}, the partial pressure of A is :'
        pa = float(P0) - float(x)
        o, a = mcq(rng, f'{nf(pa, 3)} {unit}', [f'{nf(v, 3)} {unit}' for v in (Pt - float(P0), float(P0) - (Pt - float(P0)) / 2, Pt - pa, float(x), Pt / float(nu), 2 * float(P0) - Pt) if abs(v - pa) > 1e-6 and v > 0])
        return dict(q=q, o=o, a=a, sol=[f'Per mole of A, gas moles increase by {nu - 1}: P_{{t}} = P_{{0}} + {nu - 1}x.'.replace('5/2', '\\f{5}{2}').replace('3/2', '\\f{3}{2}'), f'x = {nf(float(x), 4)} → p_{{A}} = P_{{0}} − x = {nf(pa, 3)} {unit}.'], p=dict(t='pA', nu=str(nu), P0=float(P0), Pt=Pt))
    if t == 'P0':
        Pinf = float(P0) * float(nu)
        q = f'For the first order reaction {eq}, started with pure A, the total pressure after a very long time is {nf(Pinf, 4)} {unit}. The initial pressure of A was :'
        o, a = mcq(rng, f'{nf(P0)} {unit}', [f'{nf(v, 3)} {unit}' for v in (Pinf / 2, Pinf, Pinf * 2 / 3, Pinf / 4, Pinf / 3, Pinf / 5) if abs(v - float(P0)) > 1e-6])
        return dict(q=q, o=o, a=a, sol=[f'Complete reaction: every A gives {nu} mol of gas → P_{{∞}} = {nu}P_{{0}}.'.replace('5/2', '\\f{5}{2}'), f'P_{{0}} = {nf(P0)} {unit}.'], p=dict(t='P0', nu=str(nu), Pinf=Pinf))
    tt = rng.choice([10, 20, 23, 30, 46, 50, 69, 100, 115]); k = math.log(f) / tt
    q = f'The first order reaction {eq} is started with pure A at {nf(P0)} {unit}. After {tt} s the total pressure is {nf(Pt, 4)} {unit}. The rate constant is about :'
    o, a = mcq(rng, nf(k, 3) + ' s^{−1}', [nf(v, 3) + ' s^{−1}' for v in (math.log(Pt / float(P0)) / tt, k * 2, k / 2, math.log10(f) / tt, k * 10)])
    return dict(q=q, o=o, a=a, sol=[f'P_{{t}} = P_{{0}} + {nu - 1}x → x = {nf(float(x), 4)}, p_{{A}} = {nf(float(P0) - float(x), 3)} ({f} times smaller).'.replace('5/2', '\\f{5}{2}').replace('3/2', '\\f{3}{2}'), f'k = \\f{{2.303}}{{{tt}}}log {f} ≈ {nf(k, 3)} s^{{−1}}.'], p=dict(t='kgas', nu=str(nu), P0=float(P0), Pt=Pt, tt=tt))

# ---------------- zero order & half-life ----------------
def g_zero(rng):
    t = rng.choice(['zt', 'zk', 'nh', 'zhalf'])
    if t == 'zt':
        c0 = rng.choice([1.0, 2.0, 0.8, 1.6, 4.0]); h = rng.choice([1, 2, 0.5, 4]); k = c0 / (2 * h); a, b = rng.choice([(0.5, 0.25), (0.8, 0.4), (1.0, 0.6), (0.6, 0.2), (0.4, 0.1)])
        if a > c0: return g_zero(rng)
        v = (a - b) / k * 60
        q = f'A zero order reaction has a half-life of {nf(h)} h when [A]_{{0}} = {nf(c0)} mol L^{{−1}}. The time needed for [A] to fall from {a} to {b} mol L^{{−1}} is :'
        o, a_ = mcq(rng, f'{nf(v, 3)} min', [f'{nf(x, 3)} min' for x in (h * 60, v * 2, v / 2, h * 60 * math.log(a / b) / math.log(2), (a - b) / c0 * 60)])
        return dict(q=q, o=o, a=a_, sol=[f'Zero order: t_{{1/2}} = \\f{{[A]_{{0}}}}{{2k}} → k = {nf(k, 3)} mol L^{{−1}} h^{{−1}}.', f't = \\f{{Δ[A]}}{{k}} = \\f{{{nf(a - b, 3)}}}{{{nf(k, 3)}}} h = {nf(v, 3)} min.'], p=dict(t='zt', c0=c0, h=h, A=a, B=b))
    if t == 'zk':
        k = rng.choice([0.01, 0.02, 0.05, 0.002, 0.004]); c0 = rng.choice([0.5, 1.0, 0.2, 0.8])
        v = c0 / k
        q = f'A zero order reaction has k = {nf(k)} mol L^{{−1}} s^{{−1}}. Starting from {nf(c0)} mol L^{{−1}}, the time for complete reaction is ______ s.'
        if v != int(v): return g_zero(rng)
        return dict(q=q, o=None, a=int(v), sol=['[A] = [A]_{0} − kt → completes when kt = [A]_{0}.', f't = {nf(c0)}/{nf(k)} = {int(v)} s (twice the half-life).'], p=dict(t='zk', k=k, c0=c0))
    if t == 'nh':
        n = rng.choice([F(1, 2), 0, 2, F(3, 2), 3]); f = 4; h1 = rng.choice([100, 200, 50, 400])
        h2 = h1 * f ** float(1 - n)
        if abs(h2 - round(h2)) > 1e-9 or h2 < 1: return g_zero(rng)
        h2 = round(h2)
        c1 = rng.choice([0.025, 0.05, 0.1])
        q = f'For R → P, t_{{1/2}} = {h1} min at [A]_{{0}} = {c1} M and {nf(float(h2))} min at [A]_{{0}} = {nf(c1 * f)} M. The order of the reaction is :'
        o, a = mcq(rng, str(n).replace('1/2', '½').replace('3/2', '\\f{3}{2}'), [str(x).replace('1/2', '½').replace('3/2', '\\f{3}{2}') for x in (F(1, 2), 0, 1, 2, F(3, 2), 3) if x != n])
        return dict(q=q, o=o, a=a, sol=['t_{1/2} ∝ [A]_{0}^{1 − n}.', f'{f}^{{1 − n}} = {nf(h2 / h1)} → n = {n}.'.replace('1/2', '½').replace('3/2', '\\f{3}{2}')], p=dict(t='nh', f=f, h1=h1, h2=float(h2)))
    kind = rng.choice(['zero', 'first', 'second'])
    q = f'For a {kind} order reaction, if the initial concentration is doubled, the half-life :'
    right = {'zero': 'doubles', 'first': 'stays the same', 'second': 'is halved'}[kind]
    o, a = mcq(rng, right, ['doubles', 'stays the same', 'is halved', 'becomes four times'])
    return dict(q=q, o=o, a=a, sol=['t_{1/2} ∝ [A]_{0}^{1 − n}: zero order ∝ [A]_{0}, first order independent, second order ∝ 1/[A]_{0}.', f'{kind.title()} order → {right}.'], p=dict(t='zhalf', kind=kind))

# ---------------- Arrhenius ----------------
def g_arr(rng):
    t = rng.choice(['T2', 'Ea', 'cat', 'comb', 'eq', 'slope', 'same'])
    if t == 'T2':
        f = rng.choice([2, 3, 4, 10]); Ea = rng.choice([40, 50, 60, 75, 80, 100]); T1 = rng.choice([300, 310, 320, 350])
        T2 = 1 / (1 / T1 - math.log(f) * R / (Ea * 1000)); v = T2 - 273
        if not safe(v): return g_arr(rng)
        q = f'A reaction with E_{{a}} = {Ea} kJ mol^{{−1}} has rate constant k at {T1 - 273} °C. The temperature at which the rate constant becomes {f}k is ______ °C. (R = 8.314 J K^{{−1}} mol^{{−1}}, nearest integer)'
        return dict(q=q, o=None, a=round(v), sol=[f'ln {f} = \\f{{E_{{a}}}}{{R}}(\\f{{1}}{{{T1}}} − \\f{{1}}{{T_{{2}}}}).', f'T_{{2}} ≈ {T2:.1f} K = {v:.1f} °C.'], p=dict(t='T2', f=f, Ea=Ea, T1=T1))
    if t == 'Ea':
        T1, T2 = rng.choice([(300, 310), (298, 308), (300, 320), (300, 350), (400, 500), (300, 400)]); f = rng.choice([2, 3, 4, 10])
        Ea = R * math.log(f) / (1 / T1 - 1 / T2) / 1000
        q = f'The rate constant of a reaction becomes {f} times when the temperature rises from {T1} K to {T2} K. Its activation energy is about :'
        o, a = mcq(rng, f'{Ea:.1f} kJ mol^{{−1}}', [f'{x:.1f} kJ mol^{{−1}}' for x in (Ea / 2.303, Ea * 2.303, Ea * 2, Ea / 2, Ea * 10)])
        return dict(q=q, o=o, a=a, sol=[f'E_{{a}} = \\f{{R ln {f}}}{{\\f{{1}}{{{T1}}} − \\f{{1}}{{{T2}}}}}.', f'≈ {Ea:.1f} kJ mol^{{−1}}.'], p=dict(t='Ea', f=f, T1=T1, T2=T2))
    if t == 'cat':
        d = rng.choice([5, 10, 15, 20, 25, 30]); T = rng.choice([300, 310, 350, 400, 500])
        v = d * 1000 / (2.303 * R * T)
        q = f'At {T} K a catalyst lowers the activation energy by {d} kJ mol^{{−1}} (same A). log\\f{{k_{{cat}}}}{{k}} is about :'
        o, a = mcq(rng, f'{v:.3g}', [f'{x:.3g}' for x in (v * 2.303, v / 10, v * 10, v * 2, v / 2)])
        return dict(q=q, o=o, a=a, sol=['log\\f{k_{cat}}{k} = \\f{ΔE_{a}}{2.303RT}.', f'= \\f{{{d}000}}{{2.303 × 8.314 × {T}}} ≈ {v:.3g}.'], p=dict(t='cat', d=d, T=T))
    if t == 'comb':
        E = rng.sample([10, 20, 30, 40, 50, 60, 80, 100, 120], 3); form = rng.choice(['k_{1}k_{2}/k_{3}', 'k_{1}k_{3}/k_{2}', '√{k_{1}k_{2}/k_{3}}', 'k_{1}√{k_{2}/k_{3}}', 'k_{1}^{2}k_{2}/k_{3}'])
        cf = {'k_{1}k_{2}/k_{3}': (1, 1, -1), 'k_{1}k_{3}/k_{2}': (1, -1, 1), '√{k_{1}k_{2}/k_{3}}': (F(1, 2), F(1, 2), F(-1, 2)), 'k_{1}√{k_{2}/k_{3}}': (1, F(1, 2), F(-1, 2)), 'k_{1}^{2}k_{2}/k_{3}': (2, 1, -1)}[form]
        v = sum(F(c) * e for c, e in zip(cf, E))
        if v <= 0 or v.denominator != 1: return g_arr(rng)
        form_tx = {'k_{1}k_{2}/k_{3}': '\\f{k_{1}k_{2}}{k_{3}}', 'k_{1}k_{3}/k_{2}': '\\f{k_{1}k_{3}}{k_{2}}', '√{k_{1}k_{2}/k_{3}}': '√{\\f{k_{1}k_{2}}{k_{3}}}', 'k_{1}√{k_{2}/k_{3}}': 'k_{1}√{\\f{k_{2}}{k_{3}}}', 'k_{1}^{2}k_{2}/k_{3}': '\\f{k_{1}^{2}k_{2}}{k_{3}}'}[form]
        q = f'For a multistep reaction the overall rate constant is k = {form_tx}. If E_{{a1}}, E_{{a2}}, E_{{a3}} are {E[0]}, {E[1]} and {E[2]} kJ mol^{{−1}}, the overall E_{{a}} is ______ kJ mol^{{−1}}.'
        return dict(q=q, o=None, a=int(v), sol=['ln k is a weighted sum of ln k_{i}, so E_{a} is the same weighted sum of E_{ai}.', f'E_{{a}} = {int(v)} kJ mol^{{−1}}.'], p=dict(t='comb', E=E, cf=[str(c) for c in cf]))
    if t == 'eq':
        A1, A2 = rng.choice([(1e6, 1e4), (1e8, 1e6), (1e10, 1e8), (1e7, 1e4), (1e9, 1e6)]); e1 = rng.choice([30000, 36000, 40000, 45000]); de = rng.choice([4000, 6000, 8000, 9000])
        T = de / math.log(A1 / A2)
        if not safe(T): return g_arr(rng)
        q = f'k_{{1}} = {nf(A1)}e^{{−{e1}/T}} and k_{{2}} = {nf(A2)}e^{{−{e1 - de}/T}}. The temperature at which k_{{1}} = k_{{2}} is ______ K. (nearest integer)'
        return dict(q=q, o=None, a=round(T), sol=[f'\\f{{{nf(A1)}}}{{{nf(A2)}}} = e^{{{de}/T}} → T = \\f{{{de}}}{{ln {nf(A1 / A2)}}} ≈ {T:.1f} K.'], p=dict(t='eq', A1=A1, A2=A2, de=de))
    if t == 'slope':
        s = rng.choice([1.0e4, 1.2e4, 1.5e4, 5000, 8000, 2.0e4]); base = rng.choice(['log', 'ln'])
        v = s * (2.303 if base == 'log' else 1) * R / 1000
        q = f'For a reaction {base} k = 14.3 − \\f{{{nf(s)}}}{{T}}. The activation energy is about :'
        o, a = mcq(rng, f'{v:.1f} kJ mol^{{−1}}', [f'{x:.1f} kJ mol^{{−1}}' for x in ((s * R / 1000) if base == 'log' else s * 2.303 * R / 1000, s / 1000, v * 2, v / 2, s * 2.303 / 1000)])
        return dict(q=q, o=o, a=a, sol=[f'Compare with {base} k = {base} A − \\f{{E_{{a}}}}{{{"2.303" if base == "log" else ""}RT}}.', f'E_{{a}} = {nf(s)} × {"2.303 × " if base == "log" else ""}8.314 ≈ {v:.1f} kJ mol^{{−1}}.'], p=dict(t='slope', s=s, base=base))
    d = rng.choice([10, 15, 20, 25, 30]); T = rng.choice([300, 250, 400, 500])
    v = d * 1000 / (R * T)
    if not safe(v): return g_arr(rng)
    q = f'Two reactions have the same pre-exponential factor; E_{{a}} of the first is {d} kJ mol^{{−1}} higher. At {T} K, ln\\f{{k_{{2}}}}{{k_{{1}}}} is ______ (nearest integer).'
    return dict(q=q, o=None, a=round(v), sol=['ln\\f{k_{2}}{k_{1}} = \\f{E_{a1} − E_{a2}}{RT}.', f'= \\f{{{d}000}}{{8.314 × {T}}} ≈ {v:.2f}.'], p=dict(t='same', d=d, T=T))

def robust(g):
    def w(rng):
        for _ in range(50):
            try: return g(rng)
            except AssertionError: continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(order=g_order, first=g_first, gas=g_gas, zero=g_zero, arr=g_arr).items()}
def finish(it): return it

# ---------------- independent checks ----------------
def num(s):
    s = s.replace('−', '-').split(' ')
    if len(s) >= 4 and s[1] == '×': return float(s[0]) * 10 ** int(s[3].replace('10^{', '').rstrip('}'))
    return float(s[0])
def decay(k, t, c0=1.0, steps=20000):   # numerical integration of d[A]/dt = −k[A] (RK4)
    h, c = t / steps, c0
    for _ in range(steps):
        a = -k * c; b = -k * (c + h * a / 2); d = -k * (c + h * b / 2); e = -k * (c + h * d); c += h * (a + 2 * b + 2 * d + e) / 6
    return c
def solve_time(k, frac):   # bisection on the integrated decay
    lo, hi = 0.0, 1.0
    while math.exp(-k * hi) > frac: hi *= 2
    for _ in range(80):
        m = (lo + hi) / 2
        if 2 ** (-k * m / math.log(2)) > frac: lo = m
        else: hi = m
    return lo
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'ratio': return Rv == F(p['fa']) ** p['a'] * F(p['fb']) ** p['b']
    if t == 'data': return Rv == round(math.log10(p['r2'] / p['r1']) / math.log10(p['c2'] / p['c1']))
    if t == 'two':
        rows = p['rows']; base = min(rows, key=lambda r: (r[0], r[1]))
        ra = next(r for r in rows if r[1] == base[1] and r[0] != base[0]); rb = next(r for r in rows if r[0] == base[0] and r[1] != base[1])
        a = round(math.log10(ra[2] / base[2]) / math.log10(ra[0] / base[0])); b = round(math.log10(rb[2] / base[2]) / math.log10(rb[1] / base[1])); return Rv == a + b
    if t == 'unit': return Rv == ['zero', 'first', 'second', 'third'][p['n']]
    if t == 'stoich': return abs(num(Rv) - p['d'] / p['na'] * p['nb']) < 1e-9 * p['d'] * 10
    if t == 'halfl': return Rv == round(1 - math.log10(p['h2'] / p['h1']) / math.log10(p['f']))
    if t == 'pct': k = math.log(2) / p['th']; return Rv == round(solve_time(k, 1 - p['pc'] / 100))
    if t == 'left': return abs(num(Rv) - decay(math.log(2) / p['th'], p['tt'], p['m0'])) < 1e-3 * p['m0']
    if t == 'tratio': return abs(float(Rv) - math.log10(p['f1']) / math.log10(p['f2'])) < 0.006
    if t == 'twor': k = math.log10(p['r1'] / p['r2']) * 2.302585 / p['dt']; return Rv == round(solve_time(k, 0.5))
    if t == 'age': return Rv == round(solve_time(math.log(2) / p['th'], 1 / p['fr']))
    if t == 'race':
        tt = int(Rv.split(' ')[0]); a = 2 ** p['m'] * decay(math.log(2) / p['hA'], tt); b = decay(math.log(2) / p['hB'], tt); return abs(a - b) < 1e-6
    if t == 'kfirst': return abs(num(Rv) - 2.302585 * math.log10(p['f']) / p['tt']) < 0.01 * num(Rv)
    if t in ('pA', 'P0', 'kgas'):
        nu = F(p['nu'])
        if t == 'P0': return abs(num(Rv) - p['Pinf'] / float(nu)) < 1e-6 * p['Pinf']
        pa = p['P0'] - (p['Pt'] - p['P0']) / float(nu - 1)
        if t == 'pA': return abs(num(Rv) - pa) < 0.006 * max(pa, 1e-9)
        k = math.log(p['P0'] / pa) / p['tt']; return abs(num(Rv) - k) < 0.02 * k
    if t == 'zt':
        c, tt, k, dt = p['A'], 0.0, p['c0'] / (2 * p['h']), 1e-4   # march [A] down at constant rate
        steps = round((p['A'] - p['B']) / (k * dt)); return abs(num(Rv) - steps * dt * 60) < 0.01 * num(Rv)
    if t == 'zk': return Rv == round(p['c0'] / p['k'])
    if t == 'nh':
        n = 1 - math.log(p['h2'] / p['h1']) / math.log(p['f']); txt = Rv.replace('½', '1/2').replace('\\f{3}{2}', '3/2'); return abs(float(F(txt)) - n) < 1e-9
    if t == 'zhalf': return Rv == {0: 'doubles', 1: 'stays the same', 2: 'is halved'}[['zero', 'first', 'second'].index(p['kind'])]
    if t == 'T2':   # bisection on Arrhenius ratio
        lo, hi = p['T1'], p['T1'] + 400.0
        for _ in range(80):
            m = (lo + hi) / 2
            if math.exp(p['Ea'] * 1000 / R * (1 / p['T1'] - 1 / m)) < p['f']: lo = m
            else: hi = m
        return Rv == round(lo - 273)
    if t == 'Ea': Ea = num(Rv) * 1000; return abs(math.exp(Ea / R * (1 / p['T1'] - 1 / p['T2'])) - p['f']) < 0.01 * p['f']
    if t == 'cat': return abs(math.log10(math.exp(p['d'] * 1000 / (R * p['T']))) - float(Rv)) < 0.01 * float(Rv)
    if t == 'comb': return Rv == sum(F(c) * e for c, e in zip(p['cf'], p['E']))
    if t == 'eq':
        return Rv == round(p['de'] / (2.302585 * math.log10(p['A1'] / p['A2'])))
    if t == 'slope': return abs(num(Rv) - p['s'] * (math.log(10) if p['base'] == 'log' else 1) * R / 1000) < 0.15
    if t == 'same': return Rv == round(math.log(math.exp(p['d'] * 1000 / (R * p['T']))))
    raise KeyError(t)
