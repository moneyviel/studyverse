"""Practice generators — Chemistry Unit 5: Solutions. check() re-solves each item by building the actual sample
(grams, moles, litres) and recomputing, by direct Raoult/Dalton sums, or by bisection on the colligative equation."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
SOL = {'NaCl': (58.5, 2), 'KCl': (74.5, 2), 'CaCl_{2}': (111.0, 3), 'MgCl_{2}': (95.0, 3), 'K_{2}SO_{4}': (174.0, 3), 'Al_{2}(SO_{4})_{3}': (342.0, 5), 'glucose': (180.0, 1), 'urea': (60.0, 1), 'sucrose': (342.0, 1), 'NaOH': (40.0, 2)}
NONEL = ['glucose', 'urea', 'sucrose']
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def bis(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2

def g_conc(rng):
    t = rng.choice(['M', 'm_from_M', 'M_from_m', 'x', 'mass%', 'mix', 'ppm'])
    if t == 'M':
        s = rng.choice(['NaCl', 'NaOH', 'glucose', 'urea', 'KCl']); mw = SOL[s][0]; n = rng.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1]); V = rng.choice([100, 200, 250, 500, 1000])
        g = n * mw; Mv = n / (V / 1000)
        q = f'{nf(g, 4)} g of {s} (M = {nf(mw)} g/mol) is dissolved to make {V} mL of solution. Its molarity is :'
        o, a = mcq(rng, f'{nf(Mv, 3)} M', [f'{nf(x, 3)} M' for x in (n, Mv * 10, Mv / 2, g / V)])
        return dict(q=q, o=o, a=a, sol=['M = \\f{moles}{litres of solution}.', f'{nf(n)} mol / {nf(V / 1000)} L = {nf(Mv, 3)} M.'], p=dict(t=t, g=g, mw=mw, V=V))
    if t == 'm_from_M':
        s = rng.choice(['NaCl', 'NaOH', 'KCl', 'urea', 'glucose']); mw = SOL[s][0]; Mv = rng.choice([0.5, 1, 2, 3, 4]); d = rng.choice([1.02, 1.05, 1.1, 1.12, 1.2, 1.25])
        w = 1000 * d - Mv * mw; need(w > 300); m = Mv / (w / 1000)
        q = f'A {nf(Mv)} M solution of {s} (M = {nf(mw)}) has density {d} g/mL. Its molality is about :'
        o, a = mcq(rng, f'{nf(m, 3)} m', [f'{nf(x, 3)} m' for x in (Mv, Mv / d, m * 1.2, Mv * d)])
        return dict(q=q, o=o, a=a, sol=['Take 1 L: mass = 1000d g; solvent = 1000d − M × molar mass.', f'Water = {nf(w, 4)} g → m = \\f{{{nf(Mv)}}}{{{nf(w / 1000, 4)}}} ≈ {nf(m, 3)}.'], p=dict(t=t, Mv=Mv, d=d, mw=mw))
    if t == 'M_from_m':
        s = rng.choice(['NaOH', 'NaCl', 'urea']); mw = SOL[s][0]; m = rng.choice([1, 2, 3, 4, 5]); d = rng.choice([1.04, 1.08, 1.1, 1.12, 1.15, 1.2])
        Mv = 1000 * d * m / (1000 + m * mw)
        q = f'A {m} molal solution of {s} (M = {nf(mw)}) has density {d} g/mL. Its molarity is about :'
        o, a = mcq(rng, f'{nf(Mv, 3)} M', [f'{nf(x, 3)} M' for x in (m, m * d, Mv * 1.25, m / d)])
        return dict(q=q, o=o, a=a, sol=['Take 1 kg water: mass = 1000 + m × molar mass, volume = mass / d.', f'M = \\f{{{m}}}{{V}} ≈ {nf(Mv, 3)} M.'], p=dict(t=t, m=m, d=d, mw=mw))
    if t == 'x':
        s = rng.choice(['urea', 'glucose', 'NaOH', 'sucrose']); m = rng.choice([0.5, 1, 1.11, 2, 2.22, 3, 4.44, 5, 5.55])
        x = m / (m + 1000 / 18)
        q = f'A {nf(m)} molal aqueous solution of {s} (non-dissociated for this count). The mole fraction of the solute is about :'
        o, a = mcq(rng, nf(x, 3), [nf(v, 3) for v in (m / 55.5 + 0.01, m / 1000, x * 2, 1 - x)])
        return dict(q=q, o=o, a=a, sol=['In 1 kg water: 55.56 mol water.', f'x = \\f{{{nf(m)}}}{{{nf(m)} + 55.56}} ≈ {nf(x, 3)}.'], p=dict(t=t, m=m))
    if t == 'mass%':
        a_, b_ = rng.choice([('ethanol', 46), ('methanol', 32), ('glycerol', 92), ('acetone', 58)]); n1, n2 = rng.choice([1, 2, 3]), rng.choice([5, 9, 10, 15, 20])
        v = 100 * n1 * b_ / (n1 * b_ + n2 * 18)
        q = f'{n1} mol of {a_} (M = {b_}) is mixed with {n2} mol of water. Mass percent of {a_} is about :'
        o, a = mcq(rng, f'{nf(v, 3)} %', [f'{nf(x, 3)} %' for x in (100 * n1 / (n1 + n2), v * 1.3, 100 - v, v / 2)])
        return dict(q=q, o=o, a=a, sol=['mass % = \\f{solute mass}{total mass} × 100.', f'= \\f{{{n1 * b_}}}{{{n1 * b_ + n2 * 18}}} × 100 ≈ {nf(v, 3)} %.'], p=dict(t=t, n1=n1, mw=b_, n2=n2))
    if t == 'mix':
        V1, M1, V2, M2 = rng.choice([10, 20, 25, 50, 100]), rng.choice([0.5, 1, 2, 3]), rng.choice([50, 100, 200, 250, 400]), rng.choice([0.1, 0.2, 0.25, 0.5, 1])
        Mf = (V1 * M1 + V2 * M2) / (V1 + V2); v = Mf * 100; need(abs(v - round(v)) < 0.5)
        q = f'{V1} mL of {M1} M NaOH is mixed with {V2} mL of {M2} M NaOH. The final concentration is ______ × 10^{{−2}} M (nearest integer).'
        return dict(q=q, o=None, a=round(v), sol=['Moles add; volumes add.', f'M = \\f{{{nf(V1 * M1)} + {nf(V2 * M2)}}}{{{V1 + V2}}} ≈ {nf(Mf, 3)} M.'], p=dict(t=t, V1=V1, M1=M1, V2=V2, M2=M2))
    ppm = rng.choice([2, 5, 5.8, 8, 10, 20]); mass = rng.choice([100, 500, 1000, 2000])
    g = ppm * 1e-6 * mass
    q = f'A {mass} g sample of water contains {ppm} ppm (by mass) of dissolved oxygen. The mass of O_{{2}} present is :'
    o, a = mcq(rng, f'{nf(g * 1000, 3)} mg', [f'{nf(x * 1000, 3)} mg' for x in (g * 1000, g / 1000, g * 10, g / 10)])
    return dict(q=q, o=o, a=a, sol=['1 ppm = 1 g per 10^{6} g.', f'{ppm} × 10^{{−6}} × {mass} g = {nf(g * 1000, 3)} mg.'], p=dict(t='ppm', ppm=ppm, mass=mass))

def g_vp(rng):
    t = rng.choice(['ptot', 'y', 'pB', 'rlvp', 'dev', 'Mfromrl'])
    if t in ('ptot', 'y'):
        pA, pB = rng.sample([20, 24, 40, 60, 80, 100, 120, 150, 200, 300, 350, 400, 750], 2); xA = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75])
        P_ = xA * pA + (1 - xA) * pB; yA = xA * pA / P_
        if t == 'ptot':
            q = f'Liquids A (p^{{0}} = {pA} mm Hg) and B (p^{{0}} = {pB} mm Hg) form an ideal solution with x_{{A}} = {xA}. The total vapour pressure is :'
            o, a = mcq(rng, f'{nf(P_, 4)} mm Hg', [f'{nf(x, 4)} mm Hg' for x in ((pA + pB) / 2, xA * pB + (1 - xA) * pA, pA + pB, P_ * 1.1)])
            return dict(q=q, o=o, a=a, sol=['Raoult: p = x_{A}p_{A}^{0} + x_{B}p_{B}^{0}.', f'= {xA} × {pA} + {nf(1 - xA)} × {pB} = {nf(P_, 4)} mm Hg.'], p=dict(t=t, pA=pA, pB=pB, xA=xA))
        q = f'Liquids A (p^{{0}} = {pA} Torr) and B (p^{{0}} = {pB} Torr) form an ideal solution with x_{{A}} = {xA}. The mole fraction of A in the vapour is :'
        o, a = mcq(rng, nf(yA, 3), [nf(x, 3) for x in (xA, 1 - yA, pA / (pA + pB), yA * 1.2 if yA * 1.2 < 1 else yA / 1.2)])
        return dict(q=q, o=o, a=a, sol=['Dalton: y_{A} = \\f{x_{A}p_{A}^{0}}{p_{total}}.', f'= \\f{{{nf(xA * pA)}}}{{{nf(P_, 4)}}} ≈ {nf(yA, 3)}.'], p=dict(t=t, pA=pA, pB=pB, xA=xA))
    if t == 'pB':
        nA, nB = rng.choice([1, 2, 3]), rng.choice([1, 2, 3, 4]); pA = rng.choice([100, 150, 200, 300, 400]); pBv = rng.choice([100, 200, 300, 500, 600, 800]); need(pA != pBv)
        Ptot = F(nA * pA + nB * pBv, nA + nB); need(Ptot.denominator == 1)
        q = f'{nA} mol of liquid A (p^{{0}} = {pA} mm Hg) and {nB} mol of liquid B form an ideal solution with vapour pressure {Ptot} mm Hg. p^{{0}} of B is ______ mm Hg.'
        return dict(q=q, o=None, a=pBv, sol=['p = x_{A}p_{A}^{0} + x_{B}p_{B}^{0} → solve for p_{B}^{0}.', f'p_{{B}}^{{0}} = \\f{{{Ptot} − {fr(F(nA, nA + nB))} × {pA}}}{{{fr(F(nB, nA + nB))}}} = {pBv} mm Hg.'], p=dict(t=t, nA=nA, nB=nB, pA=pA, P=int(Ptot)))
    if t == 'rlvp':
        s = rng.choice(NONEL); mw = SOL[s][0]; g = rng.choice([5, 9, 10, 18, 20, 30, 36, 60]); W = rng.choice([90, 100, 180, 200, 500]); p0 = rng.choice([17.5, 23.8, 31.8, 760])
        n2, n1 = g / mw, W / 18; p = p0 * n1 / (n1 + n2)
        q = f'{g} g of {s} (M = {nf(mw)}) is dissolved in {W} g of water (p^{{0}} = {p0} mm Hg). The vapour pressure of the solution is about :'
        o, a = mcq(rng, f'{nf(p, 4)} mm Hg', [f'{nf(x, 4)} mm Hg' for x in (p0 * n2 / (n1 + n2), p0 - p0 * n2 / n1 * 2, p0 * 0.9, p0 - (p0 - p) * 10)])
        return dict(q=q, o=o, a=a, sol=['p = x_{water}p^{0}.', f'x_{{water}} = \\f{{{nf(n1, 4)}}}{{{nf(n1 + n2, 4)}}} → p ≈ {nf(p, 4)} mm Hg.'], p=dict(t=t, g=g, mw=mw, W=W, p0=p0))
    if t == 'dev':
        kind = rng.choice(['positive', 'negative']); ask = rng.choice(['vp', 'bp', 'mix', 'example'])
        ans = {('positive', 'vp'): 'higher than Raoult\'s law predicts', ('negative', 'vp'): 'lower than Raoult\'s law predicts', ('positive', 'bp'): 'a minimum-boiling azeotrope can form', ('negative', 'bp'): 'a maximum-boiling azeotrope can form',
               ('positive', 'mix'): 'ΔH_{mix} > 0 and ΔV_{mix} > 0', ('negative', 'mix'): 'ΔH_{mix} < 0 and ΔV_{mix} < 0', ('positive', 'example'): 'ethanol + water', ('negative', 'example'): 'chloroform + acetone'}
        right = ans[(kind, ask)]; other = 'negative' if kind == 'positive' else 'positive'
        wrong = [ans[(other, ask)]] + {'vp': ['exactly as Raoult\'s law predicts', 'zero'], 'bp': ['no azeotrope can ever form', 'the boiling point equals that of the purer liquid'],
                                       'mix': ['ΔH_{mix} = 0 and ΔV_{mix} = 0', 'ΔH_{mix} > 0 and ΔV_{mix} < 0'], 'example': ['benzene + toluene', 'n-hexane + n-heptane']}[ask]
        txt = {'vp': 'its vapour pressure is', 'bp': 'regarding azeotropes,', 'mix': 'on mixing,', 'example': 'a typical example is'}[ask]
        o, a = mcq(rng, right, wrong)
        return dict(q=f'For a solution showing {kind} deviation from Raoult\'s law, {txt} :', o=o, a=a, sol=['Positive: A–B attraction weaker than A–A/B–B → more escape. Negative: stronger → fewer escape.', right + '.'], p=dict(t=t, kind=kind, ask=ask))
    s_mw = rng.choice([60, 90, 120, 180, 200, 240, 300, 342]); g = rng.choice([2, 3, 5, 6, 9, 10, 12]); W = rng.choice([50, 100, 150, 200]); Ms = rng.choice([18, 78])
    rl = (g / s_mw) / (g / s_mw + W / Ms)
    q = f'{g} g of a non-volatile solute dissolved in {W} g of a solvent (M = {Ms}) lowers its vapour pressure by a fraction {nf(rl, 4)}. The molar mass of the solute is about ______ g/mol.'
    return dict(q=q, o=None, a=s_mw, sol=['\\f{Δp}{p^{0}} = x_{solute} = \\f{n_{2}}{n_{1} + n_{2}}.', f'Solve: n_{{2}} = {nf(g / s_mw, 4)} → M = {s_mw}.'], p=dict(t=t, g=g, W=W, Ms=Ms, rl=rl))

def g_colli(rng):
    t = rng.choice(['dTf', 'dTb', 'mass', 'M2', 'pi', 'pimix', 'iso'])
    if t in ('dTf', 'dTb'):
        s = rng.choice(list(SOL)); mw, i = SOL[s]; g = rng.choice([1, 2, 5, 6, 9, 10, 18, 20, 30, 36]); W = rng.choice([50, 100, 200, 250, 500])
        K = 1.86 if t == 'dTf' else 0.52; dT = i * K * (g / mw) / (W / 1000)
        q = f'{g} g of {s} (M = {nf(mw)}) is dissolved in {W} g of water. Assuming complete dissociation, the {"depression in freezing point" if t == "dTf" else "elevation in boiling point"} is about (K_{{{"f" if t == "dTf" else "b"}}} = {K}) :'
        o, a = mcq(rng, f'{nf(dT, 3)} K', [f'{nf(x, 3)} K' for x in (dT / i if i > 1 else dT * 2, dT * W / 1000, dT * 1.5, dT / 2)])
        return dict(q=q, o=o, a=a, sol=['ΔT = iKm.', f'i = {i}, m = {nf((g / mw) / (W / 1000), 3)} → ΔT ≈ {nf(dT, 3)} K.'], p=dict(t=t, g=g, mw=mw, i=i, W=W, K=K))
    if t == 'mass':
        dT = rng.choice([2, 4, 6, 9.3, 10, 12, 18.6, 24]); W = rng.choice([1, 2, 5, 10, 18.6]); mw = rng.choice([62, 60, 92])
        kg = dT / 1.86 * W * mw / 1000
        q = f'Mass of an antifreeze (M = {mw} g/mol, non-electrolyte) to be added to {nf(W)} kg of water to lower its freezing point to −{nf(dT)} °C (K_{{f}} = 1.86) is about :'
        o, a = mcq(rng, f'{nf(kg, 3)} kg', [f'{nf(x, 3)} kg' for x in (kg * 1000 / W, kg / 2, kg * 1.86, kg * 2)])
        return dict(q=q, o=o, a=a, sol=['m = \\f{ΔT_{f}}{K_{f}} → moles = m × kg water → mass.', f'≈ {nf(kg, 3)} kg.'], p=dict(t=t, dT=dT, W=W, mw=mw))
    if t == 'M2':
        mw = rng.choice([60, 90, 120, 128, 150, 180, 200, 256, 342]); g = rng.choice([1, 2, 2.5, 5, 10]); W = rng.choice([20, 25, 50, 100]); K = rng.choice([0.52, 1.86, 5.12, 2.53])
        dT = K * g / mw / (W / 1000)
        q = f'{nf(g)} g of a non-electrolyte in {W} g of solvent changes its boiling/freezing point by {nf(dT, 4)} K (K = {K} K kg/mol). The molar mass of the solute is ______ g/mol (nearest integer).'
        return dict(q=q, o=None, a=mw, sol=['M = \\f{Kw}{ΔT W}.', f'= \\f{{{K} × {nf(g)}}}{{{nf(dT, 4)} × {nf(W / 1000)}}} ≈ {mw}.'], p=dict(t=t, g=g, W=W, K=K, dT=dT))
    if t == 'pi':
        s = rng.choice(list(SOL)); mw, i = SOL[s]; c = rng.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.25]); T = rng.choice([273, 298, 300, 310])
        pi = i * c * 0.083 * T
        q = f'The osmotic pressure of a {nf(c)} M aqueous solution of {s} at {T} K (complete dissociation, R = 0.083 L bar mol^{{−1}} K^{{−1}}) is about :'
        o, a = mcq(rng, f'{nf(pi, 3)} bar', [f'{nf(x, 3)} bar' for x in (pi / i if i > 1 else pi * 2, pi * 10, pi / 2, c * 0.083 * 273)])
        return dict(q=q, o=o, a=a, sol=['π = iCRT.', f'= {i} × {nf(c)} × 0.083 × {T} ≈ {nf(pi, 3)} bar.'], p=dict(t=t, i=i, c=c, T=T))
    if t == 'pimix':
        c_in = rng.choice([0.1, 0.2, 0.3, 0.4]); s = rng.choice(['NaCl', 'KCl', 'CaCl_{2}']); i = SOL[s][1]; c_out = rng.choice([0.01, 0.02, 0.05, 0.08])
        pi = abs(c_in - i * c_out) * 0.083 * 300; v = pi * 10; need(abs(v - round(v)) < 0.5 and c_in != i * c_out)
        q = f'A cell filled with {c_in} M glucose (semipermeable wall) is placed in {c_out} M {s} at 300 K. The osmotic pressure difference across the wall is ______ × 10^{{−1}} bar (nearest integer; complete dissociation, R = 0.083).'
        return dict(q=q, o=None, a=round(v), sol=['Use effective (particle) concentrations: inside c, outside i × c.', f'Δc = |{c_in} − {i} × {c_out}| → π ≈ {nf(pi, 3)} bar.'], p=dict(t=t, ci=c_in, co=c_out, i=i))
    pi = rng.choice([4.8, 6, 7.2, 9.6, 12, 14.4]); T = 300; s = rng.choice(['NaCl', 'glucose', 'urea', 'KCl']); mw, i = SOL[s]
    gl = pi / (i * 0.08 * T) * mw; need(abs(gl - round(gl)) < 0.5)
    q = f'The osmotic pressure of a cell is {pi} atm at 300 K. The concentration (g/L) of {s} solution isotonic with it is ______ (nearest integer; R = 0.08 L atm K^{{−1}} mol^{{−1}}, complete dissociation).'
    return dict(q=q, o=None, a=round(gl), sol=['Isotonic: iCRT = π.', f'C = \\f{{{pi}}}{{{i} × 0.08 × 300}} M → × {nf(mw)} ≈ {round(gl)} g/L.'], p=dict(t='iso', pi=pi, mw=mw, i=i))

def g_vant(rng):
    t = rng.choice(['alpha', 'i', 'order', 'alphaT', 'Ka'])
    if t == 'alpha':
        n = rng.choice([2, 3, 4, 5]); iv = rng.choice([1.5, 1.8, 2, 2.2, 2.5, 3, 3.4]); need(1 < iv < n)
        al = (iv - 1) / (n - 1); v = al * 100; need(abs(v - round(v)) < 0.5)
        names = {2: 'AB', 3: 'AB_{2}', 4: 'AB_{3}', 5: 'A_{2}B_{3}'}
        q = f'A salt {names[n]} (gives {n} ions per formula unit) has van\'t Hoff factor {iv} in solution. Its percentage dissociation is about ______ %.'
        return dict(q=q, o=None, a=round(v), sol=['i = 1 + (n − 1)α.', f'α = \\f{{{iv} − 1}}{{{n - 1}}} ≈ {nf(al, 3)} → {round(v)} %.'], p=dict(t=t, n=n, i=iv))
    if t == 'i':
        n = rng.choice([2, 3, 4, 5]); al = rng.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 0.9])
        iv = 1 + (n - 1) * al
        q = f'An electrolyte giving {n} ions per formula unit is {round(al * 100)} % dissociated. Its van\'t Hoff factor is :'
        o, a = mcq(rng, nf(iv, 3), [nf(x, 3) for x in (n * al, 1 + n * al, 1 - al + al, iv + 0.5)])
        return dict(q=q, o=o, a=a, sol=['i = 1 + (n − 1)α.', f'= 1 + {n - 1} × {al} = {nf(iv, 3)}.'], p=dict(t=t, n=n, al=al))
    if t == 'order':
        picks = rng.sample(list(SOL), 4); cs = {s: rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]) for s in picks}
        eff = {s: SOL[s][1] * cs[s] for s in picks}; need(len(set(eff.values())) == 4)
        lab = {s: f'({"ABCD"[k]})' for k, s in enumerate(picks)}
        right = ' < '.join(lab[s] for s in sorted(picks, key=eff.get)); wrongs = set()
        while len(wrongs) < 4:
            pp = rng.sample(picks, 4); w = ' < '.join(lab[s] for s in pp)
            if w != right: wrongs.add(w)
        q = 'Arrange in increasing order of boiling point (complete dissociation): ' + '; '.join(f'{lab[s]} {nf(cs[s])} m {s}' for s in picks) + '.'
        o, a = mcq(rng, right, sorted(wrongs))
        return dict(q=q, o=o, a=a, sol=['Compare i × m.', ', '.join(f'{lab[s]} {nf(eff[s], 3)}' for s in picks) + '.'], p=dict(t=t, picks=picks, cs=cs))
    if t == 'alphaT':
        n = rng.choice([2, 3]); mw = rng.choice([100, 120, 150, 200]); g = rng.choice([5, 10, 15, 20]); W = rng.choice([100, 200]); al = rng.choice([0.25, 0.5, 0.75, 1])
        dT = 0.52 * (1 + (n - 1) * al) * (g / mw) / (W / 1000); v = al * 10
        q = f'{g} g of an electrolyte (M = {mw}, gives {n} ions) in {W} g of water raises the boiling point by {nf(dT, 4)} K (K_{{b}} = 0.52). Its degree of ionisation is ______ × 10^{{−1}} (nearest integer).'
        need(abs(v - round(v)) < 0.01)
        return dict(q=q, o=None, a=round(v), sol=['i = \\f{ΔT_{b}}{K_{b}m}; α = \\f{i − 1}{n − 1}.', f'm = {nf((g / mw) / (W / 1000), 3)} → i = {nf(1 + (n - 1) * al, 3)} → α = {al}.'], p=dict(t=t, n=n, mw=mw, g=g, W=W, dT=dT))
    c = rng.choice([0.1, 0.2, 0.25, 0.5]); al = rng.choice([0.02, 0.05, 0.075, 0.1, 0.2]); dT = 1.86 * c * (1 + al)
    Ka = c * al * al / (1 - al)
    q = f'A {nf(c)} m aqueous solution of a weak monobasic acid freezes at −{nf(dT, 4)} °C (K_{{f}} = 1.86; take molarity = molality). Its K_{{a}} is about :'
    o, a = mcq(rng, nf(Ka, 3), [nf(x, 3) for x in (c * al, al * al, Ka * 10, Ka / 10)])
    return dict(q=q, o=o, a=a, sol=['i = \\f{ΔT_{f}}{K_{f}m} = 1 + α.', f'α = {al} → K_{{a}} = \\f{{cα^{{2}}}}{{1 − α}} ≈ {nf(Ka, 3)}.'], p=dict(t='Ka', c=c, dT=dT))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(conc=g_conc, vp=g_vp, colli=g_colli, vant=g_vant).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'M': return close(num(Rv), (p['g'] / p['mw']) * 1000 / p['V'])
    if t == 'm_from_M':   # build 1 L, then test molality by bisection on solvent mass
        mass = 1000 * p['d']; solute = p['Mv'] * p['mw']; return close(num(Rv), p['Mv'] * 1000 / (mass - solute))
    if t == 'M_from_m':
        V = bis(lambda V: V * p['d'] - (1000 + p['m'] * p['mw']), 1, 5000); return close(num(Rv), p['m'] / (V / 1000))
    if t == 'x': n1 = 1000 / 18; return close(num(Rv), p['m'] / (p['m'] + n1))
    if t == 'mass%': return close(num(Rv), 100 * p['n1'] * p['mw'] / (p['n1'] * p['mw'] + p['n2'] * 18))
    if t == 'mix': return Rv == round(100 * (p['V1'] * p['M1'] + p['V2'] * p['M2']) / (p['V1'] + p['V2']))
    if t == 'ppm': return close(num(Rv) / 1000, p['ppm'] * p['mass'] / 1e6)
    if t in ('ptot', 'y'):
        pa, pb = p['xA'] * p['pA'], (1 - p['xA']) * p['pB']; return close(num(Rv), pa + pb if t == 'ptot' else pa / (pa + pb))
    if t == 'pB': return abs(bis(lambda pb: (p['nA'] * p['pA'] + p['nB'] * pb) / (p['nA'] + p['nB']) - p['P'], 0, 5000) - Rv) < 1e-6
    if t == 'rlvp': return close(num(Rv), p['p0'] * (1 - (p['g'] / p['mw']) / (p['g'] / p['mw'] + p['W'] / 18)), 0.002)
    if t == 'dev':
        good = {('positive', 'vp'): 'higher', ('negative', 'vp'): 'lower', ('positive', 'bp'): 'minimum', ('negative', 'bp'): 'maximum', ('positive', 'mix'): 'ΔH_{mix} > 0 and ΔV_{mix} > 0', ('negative', 'mix'): 'ΔH_{mix} < 0',
                ('positive', 'example'): 'ethanol', ('negative', 'example'): 'chloroform'}[(p['kind'], p['ask'])]
        return Rv.startswith(good) or (good in Rv and p['ask'] in ('bp', 'mix'))
    if t == 'Mfromrl': return abs(bis(lambda M: (p['g'] / M) / (p['g'] / M + p['W'] / p['Ms']) - p['rl'], 1, 5000) - Rv) < 0.5
    if t in ('dTf', 'dTb'): return close(num(Rv), p['K'] * p['i'] * (p['g'] / p['mw']) * 1000 / p['W'])
    if t == 'mass': return close(num(Rv), (p['dT'] / 1.86) * p['W'] * p['mw'] / 1000)
    if t == 'M2': return abs(bis(lambda M: p['K'] * p['g'] / M / (p['W'] / 1000) - p['dT'], 1, 10000) - Rv) < 0.5
    if t == 'pi': return close(num(Rv), p['i'] * p['c'] * 0.083 * p['T'])
    if t == 'pimix': return Rv == round(abs(p['ci'] - p['i'] * p['co']) * 0.083 * 300 * 10)
    if t == 'iso': return Rv == round(p['pi'] / (p['i'] * 0.08 * 300) * p['mw'])
    if t == 'alpha': return Rv == round(100 * (p['i'] - 1) / (p['n'] - 1))
    if t == 'i': return close(num(Rv), 1 - p['al'] + p['n'] * p['al'])
    if t == 'order':
        picks, cs = p['picks'], p['cs']; lab = {s: f'({"ABCD"[k]})' for k, s in enumerate(picks)}; inv = {v: k for k, v in lab.items()}
        seq = [inv[x.strip()] for x in Rv.split('<')]; e = [SOL[s][1] * cs[s] for s in seq]; return e == sorted(e)
    if t == 'alphaT':
        m = (p['g'] / p['mw']) / (p['W'] / 1000); i = p['dT'] / (0.52 * m); return Rv == round((i - 1) / (p['n'] - 1) * 10)
    if t == 'Ka':
        i = p['dT'] / (1.86 * p['c']); al = i - 1; return close(num(Rv), p['c'] * al * al / (1 - al), 0.03)
    raise KeyError(t)
