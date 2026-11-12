"""Practice generators — Physics Unit 9: Kinetic Theory of Gases. check() re-solves each item from molecule-level
numbers (k_B, N_A, molecular masses), mole bookkeeping, numerical derivatives or a direct simulation of the mixing."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
R, kB, NA = 8.314, 1.38e-23, 6.022e23
def need(c):
    if not c: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
GAS = {3: 'monoatomic', 5: 'rigid diatomic', 6: 'polyatomic (f = 6)', 7: 'non-rigid diatomic'}
M = {'H_{2}': 2, 'He': 4, 'CH_{4}': 16, 'N_{2}': 28, 'O_{2}': 32, 'Ar': 40, 'CO_{2}': 44, 'Ne': 20}

def g_law(rng):
    t = rng.choice(['pct', 'two', 'ptk', 'dens', 'mixmol', 'heat2'])
    if t == 'pct':
        p_ = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 1, 2]); dT = rng.choice([1, 2, 3, 5])
        T = dT / (p_ / 100); need(abs(T - round(T)) < 1e-9)
        q = f'The pressure of a gas in a closed rigid vessel rises by {nf(p_)} % when it is heated by {dT} °C. Its initial temperature is ______ K.'
        return dict(q=q, o=None, a=round(T), sol=['Fixed volume: P ∝ T → \\f{ΔP}{P} = \\f{ΔT}{T}.', f'T = \\f{{{dT}}}{{{nf(p_ / 100)}}} = {round(T)} K.'], p=dict(t=t, p=p_, dT=dT))
    if t == 'two':
        k = rng.choice([1, 2, 3]); P1, T1 = rng.choice([4, 6, 8, 10, 12]), rng.choice([300, 400, 500, 600, 1000]); P2, T2 = rng.choice([2, 3, 5, 7, 9]), rng.choice([250, 300, 400, 500]); Tf = rng.choice([300, 400, 500, 600])
        Pf = (F(P1 * k, T1) + F(P2, T2)) * Tf / (k + 1); need(Pf.denominator == 1)
        q = f'Vessel A ({k}V) holds a gas at {P1} kPa and {T1} K; vessel B (V) holds the same gas at {P2} kPa and {T2} K. They are joined by a thin tube and both kept at {Tf} K. The final pressure is ______ kPa.'
        return dict(q=q, o=None, a=int(Pf), sol=['Moles add: \\f{P_{1}V_{1}}{T_{1}} + \\f{P_{2}V_{2}}{T_{2}} = \\f{P(V_{1} + V_{2})}{T}.', f'P = {Pf} kPa.'], p=dict(t=t, k=k, P1=P1, T1=T1, P2=P2, T2=T2, Tf=Tf))
    if t == 'ptk':
        k = rng.choice([-3, -2, -1, 1, 2, 3, F(1, 2), F(-1, 2)]); kind = rng.choice(['PT', 'PV'])
        if kind == 'PT':   # P T^k = const → V ∝ T^{1+k}
            v = 1 + F(k); txt = f'PT^{{{fr(k)}}} = constant'.replace('\\f{', '').replace('}{', '/').replace('}}', '}')
        else:              # P V^k = const → T ∝ V^{1−k} → V ∝ T^{1/(1−k)}
            need(k != 1); v = 1 / (1 - F(k)); txt = f'PV^{{{fr(k)}}} = constant'.replace('\\f{', '').replace('}{', '/').replace('}}', '}')
        need(v != 0)
        q = f'An ideal gas changes so that {txt}. Its coefficient of volume expansion (\\f{{1}}{{V}}\\f{{dV}}{{dT}}) is :'
        o, a = mcq(rng, f'\\f{{{v.numerator}}}{{{v.denominator}T}}' if v.denominator != 1 else f'\\f{{{v}}}{{T}}', [f'\\f{{{x}}}{{T}}' for x in (1, 2, 3, 4, -1, -2, int(v) + 1 if v.denominator == 1 else 5) if x != v])
        return dict(q=q, o=o, a=a, sol=['Use PV = nRT to write V as a power of T.', f'V ∝ T^{{{fr(v)}}} → \\f{{1}}{{V}}\\f{{dV}}{{dT}} = {fr(v)}\\f{{1}}{{T}}.'], p=dict(t=t, k=float(F(k)), kind=kind))
    if t == 'dens':
        g = rng.choice(list(M)); P = rng.choice([1, 2, 4, 5, 10]) * 1e5; T = rng.choice([200, 250, 273, 300, 400, 500])
        rho = P * M[g] * 1e-3 / (R * T)
        q = f'The density of {g} at {nf(P)} Pa and {T} K (ideal gas) is about :'
        o, a = mcq(rng, f'{nf(rho, 3)} kg/m^{{3}}', [f'{nf(x, 3)} kg/m^{{3}}' for x in (rho * 1000, rho / 2, rho * 2, P * M[g] / (R * T))])
        return dict(q=q, o=o, a=a, sol=['ρ = \\f{PM}{RT} (M in kg/mol).', f'= \\f{{{nf(P)} × {M[g]} × 10^{{−3}}}}{{8.314 × {T}}} ≈ {nf(rho, 3)} kg/m^{{3}}.'], p=dict(t=t, g=g, P=P, T=T))
    if t == 'mixmol':
        a_, b_ = rng.sample(['He', 'N_{2}', 'O_{2}', 'CO_{2}', 'CH_{4}', 'Ar'], 2); x, y = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5]), rng.choice([0.1, 0.15, 0.2, 0.3, 0.5])
        m = x * M[a_] + y * M[b_]; n = x + y
        q = f'A mixture of {a_} and {b_} contains {nf(n, 3)} mol in all and has mass {nf(m, 4)} g. The amount of {a_} in it is ______ mol.'
        o, a = mcq(rng, nf(x, 3), [nf(v, 3) for v in (y, n / 2, x + 0.05, abs(x - 0.05) or 0.35, n)])
        return dict(q=q, o=o, a=a, sol=[f'x + y = {nf(n, 3)} and {M[a_]}x + {M[b_]}y = {nf(m, 4)}.', f'x = {nf(x, 3)} mol.'], p=dict(t=t, A=a_, B=b_, n=n, m=m))
    V = rng.choice([1, 2, 5, 10]); P1 = rng.choice([1, 2, 3]); f = rng.choice([3, 5]); dT_ = rng.choice([10, 20, 50, 100]); T = rng.choice([200, 250, 300, 400, 500])
    Q = F(f, 2) * P1 * 100000 * V * dT_ / T
    q = f'A rigid {V} m^{{3}} tank holds a {GAS[f]} gas at {P1} × 10^{{5}} Pa and {T} K. Heat needed to warm it by {dT_} K is about :'
    o, a = mcq(rng, f'{nf(float(Q), 3)} J', [f'{nf(float(Q) * k, 3)} J' for k in (F(f + 2, f), F(2, f), 2, F(1, 2))])
    return dict(q=q, o=o, a=a, sol=['n = \\f{PV}{RT}; Q = nC_{v}ΔT = \\f{f}{2}\\f{PV}{T}ΔT.', f'≈ {nf(float(Q), 3)} J.'], p=dict(t='heat2', V=V, P1=P1, f=f, dT=dT_, T=T))

def g_dof(rng):
    t = rng.choice(['gam', 'Uk', 'cvr', 'vib', 'U'])
    if t == 'gam':
        f = rng.choice([3, 5, 6, 7, 8]); v = 1 + F(2, f)
        q = f'A gas whose molecules have {f} effective degrees of freedom has γ = C_{{p}}/C_{{v}} :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (1 + F(1, f), 1 + F(2, f + 1), F(f, 2), 1 + F(2, f + 2), 1 + F(2, f - 1))])
        return dict(q=q, o=o, a=a, sol=['C_{v} = \\f{f}{2}R, C_{p} = (\\f{f}{2} + 1)R.', f'γ = 1 + \\f{{2}}{{{f}}} = {fr(v)}.'], p=dict(t=t, f=f))
    if t == 'Uk':
        f = rng.choice([3, 5, 6, 7]); N = rng.choice([2, 4, 5, 6, 10, 20, 100])
        v = N * F(f, 2); need(v.denominator == 1)
        q = f'The total energy of {N} {GAS[f]} molecules at temperature T is ______ k_{{B}}T.'
        return dict(q=q, o=None, a=int(v), sol=[f'Each molecule: \\f{{{f}}}{{2}}k_{{B}}T (½k_{{B}}T per degree of freedom).', f'{N} × \\f{{{f}}}{{2}} = {v}.'], p=dict(t=t, f=f, N=N))
    if t == 'cvr':
        f1, f2 = rng.sample([3, 5, 6, 7], 2); v = F(f1, f2)
        q = f'C_{{v}} of a {GAS[f1]} gas divided by C_{{v}} of a {GAS[f2]} gas is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(f2, f1), F(f1 + 2, f2 + 2), F(f1 + 2, f1), F(f2 + 2, f2), F(1))])
        return dict(q=q, o=o, a=a, sol=['C_{v} = \\f{f}{2}R.', f'= \\f{{{f1}}}{{{f2}}}.'], p=dict(t=t, f1=f1, f2=f2))
    if t == 'vib':
        tr, rot, vb = 3, rng.choice([2, 3]), rng.choice([1, 2, 3]); fa = rng.choice([3, 5]); f = tr + rot + 2 * vb
        r = (1 + F(2, fa)) / (1 + F(2, f)); n = 1 / (r - 1); need(n.denominator == 1 and n > 0)
        q = f'γ_{{A}} is for a gas with {fa} degrees of freedom; γ_{{B}} for one with 3 translational, {rot} rotational and {vb} vibrational mode(s). If \\f{{γ_{{A}}}}{{γ_{{B}}}} = 1 + \\f{{1}}{{n}}, n = ______'
        return dict(q=q, o=None, a=int(n), sol=['Each vibrational mode counts 2 (kinetic + potential).', f'f_{{B}} = {f}; γ_{{A}} = {fr(1 + F(2, fa))}, γ_{{B}} = {fr(1 + F(2, f))} → n = {n}.'], p=dict(t=t, fa=fa, rot=rot, vb=vb))
    f = rng.choice([3, 5, 7]); n = rng.choice([1, 2, 3, 4, 5]); T = rng.choice([200, 300, 400, 500])
    U = n * f / 2 * R * T
    q = f'The internal energy of {n} mol of a {GAS[f]} ideal gas at {T} K is about :'
    o, a = mcq(rng, f'{nf(U, 3)} J', [f'{nf(n * x / 2 * R * T, 3)} J' for x in (3, 5, 7, 6, 2) if x != f])
    return dict(q=q, o=o, a=a, sol=['U = \\f{f}{2}nRT.', f'= \\f{{{f}}}{{2}} × {n} × 8.314 × {T} ≈ {nf(U, 3)} J.'], p=dict(t='U', f=f, n=n, T=T))

def g_mix(rng):
    t = rng.choice(['cv', 'gamma', 'N', 'temp', 'Umix'])
    if t in ('cv', 'gamma', 'Umix'):
        (n1, f1), (n2, f2) = (rng.choice([1, 2, 3, 4, 5, 6]), rng.choice([3, 5, 6])), (rng.choice([1, 2, 3, 4, 6, 8]), rng.choice([3, 5, 6, 7]))
        need(f1 != f2); cv = F(n1 * f1 + n2 * f2, 2 * (n1 + n2))
        if t == 'cv':
            q = f'{n1} mol of a {GAS[f1]} gas is mixed with {n2} mol of a {GAS[f2]} gas. C_{{v}} of the mixture is :'
            o, a = mcq(rng, fr(cv) + 'R', [fr(x) + 'R' for x in (F(f1 + f2, 4), cv + 1, F(n1 * f2 + n2 * f1, 2 * (n1 + n2)), F(f1 * f2, f1 + f2))])
            return dict(q=q, o=o, a=a, sol=['C_{v,mix} = \\f{Σ n_{i}C_{v,i}}{Σ n_{i}}.', f'= \\f{{{n1} × {fr(F(f1, 2))} + {n2} × {fr(F(f2, 2))}}}{{{n1 + n2}}}R = {fr(cv)}R.'], p=dict(t=t, n1=n1, f1=f1, n2=n2, f2=f2))
        if t == 'Umix':
            v = cv * (n1 + n2); need(v.denominator == 1 or (2 * v).denominator == 1)
            q = f'A mixture of {n1} mol of a {GAS[f1]} gas and {n2} mol of a {GAS[f2]} gas is at temperature T. Its total internal energy is :'
            o, a = mcq(rng, fr(v) + 'RT', [fr(x) + 'RT' for x in (v + 1, v * 2, F(n1 + n2) * F(f1 + f2, 4) if F(n1 + n2) * F(f1 + f2, 4) != v else v + 2, v - F(1, 2))])
            return dict(q=q, o=o, a=a, sol=['U = Σ \\f{f_{i}}{2}n_{i}RT.', f'= {fr(v)}RT.'], p=dict(t=t, n1=n1, f1=f1, n2=n2, f2=f2))
        g = (cv + 1) / cv
        q = f'{n1} mol of a {GAS[f1]} gas is mixed with {n2} mol of a {GAS[f2]} gas. γ of the mixture is about :'
        o, a = mcq(rng, nf(float(g), 3), [nf(float(x), 3) for x in ((1 + F(2, f1) + 1 + F(2, f2)) / 2 + F(1, 100), g + F(1, 10), g - F(1, 10), (n1 * (1 + F(2, f1)) + n2 * (1 + F(2, f2))) / (n1 + n2) + F(1, 50))])
        return dict(q=q, o=o, a=a, sol=['First find C_{v,mix}; then γ = \\f{C_{v} + R}{C_{v}}.', f'C_{{v}} = {fr(cv)}R → γ ≈ {nf(float(g), 3)}.'], p=dict(t='gamma', n1=n1, f1=f1, n2=n2, f2=f2))
    if t == 'N':
        fa, na, fb, ftar = rng.choice([(6, 2, 3, 5), (3, 2, 6, 5), (7, 1, 3, 5), (6, 3, 3, 5), (5, 2, 3, 4), (6, 1, 5, F(11, 2)), (3, 4, 7, 5), (6, 4, 3, 4)])
        # N mol of f = fa mixed with na mol of f = fb → average f = ftar
        Nv = F(na) * (F(ftar) - fb) / (fa - F(ftar)); need(Nv.denominator == 1 and Nv > 0)
        q = f'How many moles of a gas with f = {fa} must be mixed with {na} mol of a gas with f = {fb} so that the mixture has C_{{v}} = {fr(F(ftar, 2))}R? ______'
        return dict(q=q, o=None, a=int(Nv), sol=['\\f{N f_{1}/2 + n f_{2}/2}{N + n} = C_{v}/R.', f'N = {Nv}.'], p=dict(t=t, fa=fa, na=na, fb=fb, ftar=float(ftar)))
    n1, n2 = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 6]); f1, f2 = rng.choice([3, 5]), rng.choice([3, 5]); T1, T2 = rng.choice([1, 2, 3]), rng.choice([2, 3, 4, 5])
    need(T1 != T2); Tm = F(n1 * f1 * T1 + n2 * f2 * T2, n1 * f1 + n2 * f2)
    q = f'{n1} mol of a {GAS[f1]} gas at temperature {T1}T is mixed (no heat lost) with {n2} mol of a {GAS[f2]} gas at {T2}T. The final temperature is :'
    o, a = mcq(rng, fr(Tm) + 'T', [fr(x) + 'T' for x in (F(n1 * T1 + n2 * T2, n1 + n2), F(T1 + T2, 2), Tm + F(1, 4), Tm - F(1, 4))])
    return dict(q=q, o=o, a=a, sol=['Internal energy is conserved: Σ n_{i}\\f{f_{i}}{2}RT_{i} = (Σ n_{i}\\f{f_{i}}{2})RT.', f'T = {fr(Tm)}T.'], p=dict(t='temp', n1=n1, n2=n2, f1=f1, f2=f2, T1=T1, T2=T2))

def g_speed(rng):
    t = rng.choice(['ratio', 'Tev', 'vrms', 'scale', 'same'])
    if t == 'ratio':
        a_, b_ = rng.sample(list(M), 2); v0 = rng.choice([0.5, 1, 1.5, 2, 3, 4, 6])
        v = v0 * math.sqrt(M[a_] / M[b_])
        q = f'At a certain temperature the rms speed of {a_} molecules is {nf(v0)} km/s. At the same temperature the rms speed of {b_} is about :'
        o, a = mcq(rng, f'{nf(v, 3)} km/s', [f'{nf(x, 3)} km/s' for x in (v0 * M[a_] / M[b_], v0 * math.sqrt(M[b_] / M[a_]), v0, v * 2)])
        return dict(q=q, o=o, a=a, sol=['v_{rms} = √{\\f{3RT}{M}} ∝ \\f{1}{√{M}}.', f'= {nf(v0)} × √{{\\f{{{M[a_]}}}{{{M[b_]}}}}} ≈ {nf(v, 3)} km/s.'], p=dict(t=t, A=a_, B=b_, v0=v0))
    if t == 'Tev':
        E = rng.choice([0.026, 0.039, 0.052, 0.069, 0.1, 0.207, 0.414, 0.621, 0.828, 1.035]); T = E * 1.6e-19 / (1.5 * kB)
        q = f'The average kinetic energy of a gas molecule is {E} eV. The temperature is about :'
        o, a = mcq(rng, f'{nf(T, 3)} K', [f'{nf(x, 3)} K' for x in (T * 2, T / 2, T * 1.5, E * 1.6e-19 / kB)])
        return dict(q=q, o=o, a=a, sol=['KE = \\f{3}{2}k_{B}T.', f'T = \\f{{{E} × 1.6 × 10^{{−19}}}}{{1.5 × 1.38 × 10^{{−23}}}} ≈ {nf(T, 3)} K.'], p=dict(t=t, E=E))
    if t == 'vrms':
        g = rng.choice(list(M)); T = rng.choice([200, 250, 273, 300, 400, 500, 600, 800, 1000])
        v = math.sqrt(3 * R * T / (M[g] * 1e-3))
        q = f'The rms speed of {g} molecules at {T} K is about :'
        o, a = mcq(rng, f'{nf(v, 3)} m/s', [f'{nf(x, 3)} m/s' for x in (v * math.sqrt(1000) / 10, v / math.sqrt(3), v * math.sqrt(2), v / 2)])
        return dict(q=q, o=o, a=a, sol=['v_{rms} = √{\\f{3RT}{M}} with M in kg/mol.', f'= √{{\\f{{3 × 8.314 × {T}}}{{{M[g]} × 10^{{−3}}}}}} ≈ {nf(v, 3)} m/s.'], p=dict(t=t, g=g, T=T))
    if t == 'scale':
        k = rng.choice([2, 3, 4, F(1, 2)]); T1 = rng.choice([200, 250, 300, 400]); T2 = T1 * F(k) ** 2
        q = f'At what temperature is the rms speed of a gas {fr(k)} times its value at {T1} K? ______ K'
        need(T2.denominator == 1)
        return dict(q=q, o=None, a=int(T2), sol=['v ∝ √{T} → T ∝ v^{2}.', f'T = {T1} × ({fr(k)})^{{2}} = {T2} K.'], p=dict(t=t, k=float(k), T1=T1))
    a_, b_ = rng.sample(list(M), 2); T = rng.choice([200, 300, 400, 500])
    Tb = F(T * M[b_], M[a_]); need(Tb.denominator == 1)
    q = f'{a_} at {T} K has the same rms speed as {b_} at ______ K.'
    return dict(q=q, o=None, a=int(Tb), sol=['Same v_{rms} → \\f{T}{M} equal.', f'T = {T} × \\f{{{M[b_]}}}{{{M[a_]}}} = {Tb} K.'], p=dict(t='same', A=a_, B=b_, T=T))

def g_mfp(rng):
    t = rng.choice(['lam', 'freq', 'scale'])
    if t == 'lam':
        d = rng.choice([2, 3, 4, 5]) * 1e-10; T = rng.choice([273, 300, 314, 400, 500]); P = rng.choice([0.5, 1, 1.38, 2]) * 1e5
        lam = kB * T / (math.sqrt(2) * math.pi * d * d * P)
        q = f'The mean free path of gas molecules of diameter {nf(d)} m at {T} K and {nf(P)} Pa is about (k_{{B}} = 1.38 × 10^{{−23}} J/K) :'
        o, a = mcq(rng, f'{nf(lam, 3)} m', [f'{nf(x, 3)} m' for x in (lam * math.sqrt(2), lam * 2, lam / math.pi, lam * 10)])
        return dict(q=q, o=o, a=a, sol=['λ = \\f{k_{B}T}{√{2}πd^{2}P}.', f'≈ {nf(lam, 3)} m.'], p=dict(t=t, d=d, T=T, P=P))
    if t == 'freq':
        lam = rng.choice([1, 2, 3, 4, 5, 6]) * 10 ** rng.choice([-7, -8]); v = rng.choice([300, 400, 450, 500, 600, 800, 1200])
        fq = v / lam
        q = f'Gas molecules move with average speed {v} m/s and mean free path {nf(lam)} m. The number of collisions per second of one molecule is :'
        o, a = mcq(rng, f'{nf(fq, 3)} /s', [f'{nf(x, 3)} /s' for x in (fq * 10, fq / 10, lam * v, fq * 2)])
        return dict(q=q, o=o, a=a, sol=['Collision frequency = \\f{v}{λ}.', f'= {nf(fq, 3)} /s.'], p=dict(t=t, lam=lam, v=v))
    kd, kn, kT = rng.choice([1, 2, F(1, 2)]), rng.choice([1, 2, 4, F(1, 2)]), rng.choice([1, 2, 4])
    what = rng.choice(['lam', 'freq'])
    v = 1 / (F(kd) ** 2 * F(kn)) if what == 'lam' else F(kd) ** 2 * F(kn)   # λ ∝ 1/(n d²); f ∝ n d² v (v ∝ √T)
    if what == 'freq':
        need(kT in (1, 4)); v = v * (2 if kT == 4 else 1)
    need(v != 1)
    q = f'Molecular diameter is made {fr(kd)} times, number density {fr(kn)} times' + (f' and temperature {kT} times (mass fixed)' if what == 'freq' else '') + f'. The {"mean free path" if what == "lam" else "collision frequency"} becomes ______ times.'
    o, a = mcq(rng, fr(v), [fr(x) for x in (1 / v, v * 2, v / 2, F(kd) * F(kn), F(1))])
    return dict(q=q.replace('______ times', '(how many times?)'), o=o, a=a, sol=['λ = \\f{1}{√{2}nπd^{2}}; collisions per second = \\f{v̄}{λ} with v̄ ∝ √{T}.', f'Factor = {fr(v)}.'], p=dict(t='scale', kd=float(F(kd)), kn=float(F(kn)), kT=kT, w=what))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(law=g_law, dof=g_dof, mix=g_mix, speed=g_speed, mfp=g_mfp).items()}
def finish(it): return it

def unf(s):
    s = s.replace('−', '-').strip(); neg = s.startswith('-'); s = s.lstrip('-')
    if s.startswith('\\f{'): a, b = s[3:-1].split('}{'); v = F(int(a), int(b))
    else: v = F(s)
    return -v if neg else v
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'pct':   # build the state numerically: n, V fixed
        n, V = 1.0, 1.0; T = Rv; P1 = n * R * T / V; P2 = n * R * (T + p['dT']) / V; return abs((P2 - P1) / P1 * 100 - p['p']) < 1e-9
    if t == 'two':
        V = 1.0; n = p['P1'] * 1e3 * p['k'] * V / (R * p['T1']) + p['P2'] * 1e3 * V / (R * p['T2']); return abs(n * R * p['Tf'] / ((p['k'] + 1) * V) / 1e3 - Rv) < 1e-9
    if t == 'ptk':
        def V(T): P = (1 / T ** p['k']) if p['kind'] == 'PT' else None; return T / P if p['kind'] == 'PT' else T ** (1 / (1 - p['k']))
        T0 = 300.0; coef = (V(T0 + 1e-4) - V(T0 - 1e-4)) / 2e-4 / V(T0) * T0
        s = Rv.replace('\\f{', '').replace('}{', '|').rstrip('}'); a, b = s.split('|'); b = b.replace('T', '') or '1'; return abs(coef - float(a) / float(b)) < 1e-5
    if t == 'dens':
        m1 = M[p['g']] * 1e-3 / NA; n = p['P'] / (kB * p['T']); return close(num(Rv), n * m1, 0.01)
    if t == 'mixmol':
        x = num(Rv); y = p['n'] - x; return abs(x * M[p['A']] + y * M[p['B']] - p['m']) < 0.01
    if t == 'heat2':
        n = p['P1'] * 1e5 * p['V'] / (R * p['T']); return close(num(Rv), n * p['f'] / 2 * R * p['dT'])
    if t == 'gam': return unf(Rv) == F(p['f'] + 2, p['f'])
    if t == 'Uk': return Rv == p['N'] * p['f'] / 2
    if t == 'cvr': return unf(Rv) == F(p['f1'], p['f2'])
    if t == 'vib':
        fb = 3 + p['rot'] + 2 * p['vb']; ga, gb = (p['fa'] + 2) / p['fa'], (fb + 2) / fb; return abs(ga / gb - (1 + 1 / Rv)) < 1e-9
    if t == 'U': return close(num(Rv), p['n'] * NA * p['f'] / 2 * kB * p['T'], 0.01)
    if t in ('cv', 'gamma', 'Umix'):
        U = lambda T: (p['n1'] * p['f1'] / 2 + p['n2'] * p['f2'] / 2) * R * T; Cv = (U(301) - U(300)) / ((p['n1'] + p['n2']) * R)
        if t == 'cv': return abs(float(unf(Rv[:-1])) - Cv) < 1e-9
        if t == 'Umix': return abs(float(unf(Rv[:-2])) - U(1) / R) < 1e-9
        return close(num(Rv), (Cv + 1) / Cv, 0.004)
    if t == 'N':
        N = Rv; return abs((N * p['fa'] + p['na'] * p['fb']) / (N + p['na']) - p['ftar']) < 1e-9
    if t == 'temp':   # simulate heat flow in small steps until equal
        c1, c2 = p['n1'] * p['f1'] / 2, p['n2'] * p['f2'] / 2; T1, T2 = float(p['T1']), float(p['T2'])
        for _ in range(400): q = 0.5 * (T2 - T1) * c1 * c2 / (c1 + c2); T1 += q / c1; T2 -= q / c2
        return abs(float(unf(Rv[:-1])) - T1) < 1e-6
    if t == 'ratio':
        def vr(g): m = M[g] * 1e-3 / NA; return math.sqrt(3 * kB * 300 / m)
        return close(num(Rv), p['v0'] * vr(p['B']) / vr(p['A']))
    if t == 'Tev': return close(num(Rv), p['E'] * 1.6e-19 / (1.5 * kB))
    if t == 'vrms': return close(num(Rv), math.sqrt(3 * kB * p['T'] / (M[p['g']] * 1e-3 / NA)), 0.005)
    if t == 'scale' and 'T1' in p: return abs(math.sqrt(Rv / p['T1']) - p['k']) < 1e-9
    if t == 'same': return abs(math.sqrt(p['T'] / M[p['A']]) - math.sqrt(Rv / M[p['B']])) < 1e-9
    if t == 'lam': return close(num(Rv), 1 / (math.sqrt(2) * (p['P'] / (kB * p['T'])) * math.pi * p['d'] ** 2))
    if t == 'freq': return close(num(Rv), p['v'] / p['lam'])
    if t == 'scale':
        def lam(d, n): return 1 / (math.sqrt(2) * n * math.pi * d * d)
        l0, l1 = lam(1, 1), lam(p['kd'], p['kn']); v = l0 / l1 if p['w'] == 'freq' else l1 / l0
        if p['w'] == 'freq': v *= math.sqrt(p['kT'])
        return abs(float(unf(Rv)) - v) < 1e-9
    raise KeyError(t)
