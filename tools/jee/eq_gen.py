"""Practice generators — Chemistry Unit 6: Equilibrium. check() re-solves each item independently:
ICE tables by bisection on the equilibrium expression, pH by exact charge balance (water included),
buffers by counting moles after neutralisation, solubility by bisection on K_sp = Π(ν s)^ν."""
import math
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def bis(f, lo, hi, n=300):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
def H_weak(c, Ka, Kw=1e-14): return bis(lambda h: h - Ka * c / (Ka + h) - Kw / h, 1e-15, 1.0)
def pH_of_net(nH, nOH, V):   # strong acid/base leftovers in V L, exact with water
    d = (nH - nOH) / V
    return -math.log10(bis(lambda h: h - 1e-14 / h - d, 1e-15, 10.0))
def sci(x, sig=2): return nf(x, sig)
def p2(x): return f'{x:.2f}'

REACT = [  # (equation, Δn_gas, ΔH sign)
    ('N_{2}(g) + 3H_{2}(g) ⇌ 2NH_{3}(g)', -2, -1), ('PCl_{5}(g) ⇌ PCl_{3}(g) + Cl_{2}(g)', 1, 1), ('H_{2}(g) + I_{2}(g) ⇌ 2HI(g)', 0, -1),
    ('N_{2}O_{4}(g) ⇌ 2NO_{2}(g)', 1, 1), ('2SO_{2}(g) + O_{2}(g) ⇌ 2SO_{3}(g)', -1, -1), ('N_{2}(g) + O_{2}(g) ⇌ 2NO(g)', 0, 1),
    ('CaCO_{3}(s) ⇌ CaO(s) + CO_{2}(g)', 1, 1), ('2NO_{2}(g) ⇌ N_{2}O_{4}(g)', -1, -1), ('CO(g) + 2H_{2}(g) ⇌ CH_{3}OH(g)', -2, -1),
    ('C(s) + CO_{2}(g) ⇌ 2CO(g)', 1, 1), ('2HI(g) ⇌ H_{2}(g) + I_{2}(g)', 0, 1), ('COCl_{2}(g) ⇌ CO(g) + Cl_{2}(g)', 1, 1)]
GAS = {'N_{2}O_{4}': 'NO_{2}', 'PCl_{5}': 'PCl_{3} + Cl_{2}', 'COCl_{2}': 'CO + Cl_{2}', 'SO_{2}Cl_{2}': 'SO_{2} + Cl_{2}'}

def g_kp(rng):
    t = rng.choice(['comb', 'kpkc', 'ice', 'alpha', 'graph', 'dG', 'vh', 'pres'])
    if t == 'comb':
        m = rng.choice([1.6, 2.5, 3.6, 4, 4.9, 6.4, 8, 9, 1.21, 2.25]); e = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4]); K = m * 10 ** e
        op = rng.choice([('reverse', -1), ('double', 2), ('halve', 0.5), ('reverse and double', -2), ('reverse and halve', -0.5), ('triple', 3)])
        Kn = K ** op[1]
        q = f'For a reaction, K_{{c}} = {sci(K, 3)}. The equilibrium constant for the same reaction written after we {op[0]} its equation is :'
        o, a = mcq(rng, sci(Kn, 3), [sci(x, 3) for x in (K * op[1] if op[1] > 0 else -K * op[1], K ** -op[1], 1 / K if op[1] != -1 else K * K, K ** (2 * op[1]) if abs(op[1]) != 1 else K ** 0.5)])
        return dict(q=q, o=o, a=a, sol=['Reversing the equation → \\f{1}{K}; multiplying it by n → K^{n}.', f'K\' = ({sci(K, 3)})^{{{nf(op[1])}}} = {sci(Kn, 3)}.'], p=dict(t=t, K=K, n=op[1]))
    if t == 'kpkc':
        eq, dn, _ = rng.choice([r for r in REACT if r[1] != 0 and '(s)' not in r[0]]); T = rng.choice([300, 400, 500, 600, 700, 800, 1000]); Kc = rng.choice([0.5, 1.5, 2, 4, 12, 25, 40, 64, 100])
        Kp = Kc * (0.0821 * T) ** dn
        q = f'For {eq}, K_{{c}} = {Kc} at {T} K. K_{{p}} at the same temperature is about (R = 0.0821 L atm K^{{−1}} mol^{{−1}}) :'
        o, a = mcq(rng, sci(Kp, 3), [sci(x, 3) for x in (Kc * (0.0821 * T) ** -dn, Kc, Kc * (8.314 * T) ** dn, Kc * (0.0821 * T) ** (dn - (1 if dn > 0 else -1)) if abs(dn) > 1 else Kc * 0.0821 * T * 2)])
        return dict(q=q, o=o, a=a, sol=['K_{p} = K_{c}(RT)^{Δn}, Δn = gas moles (products − reactants).', f'Δn = {dn} → K_{{p}} = {Kc} × ({nf(0.0821 * T, 4)})^{{{dn}}} ≈ {sci(Kp, 3)}.'], p=dict(t=t, Kc=Kc, T=T, dn=dn))
    if t == 'ice':
        a0 = rng.choice([0.5, 1, 1.5, 2, 2.5, 3, 4]); b0 = rng.choice([0.5, 1, 1.5, 2, 3]); V = rng.choice([1, 2, 5]); x = rng.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8]) * min(a0, b0)
        Kc = (2 * x / V) ** 2 / (((a0 - x) / V) * ((b0 - x) / V)); need(0.05 < Kc < 500)
        Kc = float(nf(Kc, 3)); x = bis(lambda y: (2 * y) ** 2 / ((a0 - y) * (b0 - y)) - Kc, 0, min(a0, b0) - 1e-12)
        q = f'{a0} mol H_{{2}} and {b0} mol I_{{2}} are heated in a {V} L flask: H_{{2}}(g) + I_{{2}}(g) ⇌ 2HI(g), K_{{c}} = {nf(Kc, 3)}. Moles of HI at equilibrium are about :'
        o, a = mcq(rng, nf(2 * x, 3), [nf(v, 3) for v in (x, 2 * x * 1.25, 2 * min(a0, b0), 2 * x * 0.7)])
        return dict(q=q, o=o, a=a, sol=['ICE: H_{2} = a − y, I_{2} = b − y, HI = 2y (V cancels since Δn = 0).', f'\\f{{(2y)^{{2}}}}{{({a0} − y)({b0} − y)}} = {nf(Kc, 3)} → y ≈ {nf(x, 3)} → HI ≈ {nf(2 * x, 3)} mol.'], p=dict(t=t, a0=a0, b0=b0, Kc=Kc))
    if t == 'alpha':
        sp = rng.choice(list(GAS)); n = 2 if sp == 'N_{2}O_{4}' else 1; Kp = rng.choice([0.1, 0.2, 0.25, 0.5, 0.75, 1, 1.5, 2, 3]); P = rng.choice([0.5, 1, 2, 3, 4, 5])
        if n == 2: al = math.sqrt(Kp / (Kp + 4 * P))
        else: al = math.sqrt(Kp / (Kp + P))
        q = f'For {sp}(g) ⇌ {GAS[sp].replace(" + ", "(g) + ") if n == 1 else "2" + GAS[sp]}(g), K_{{p}} = {Kp} atm. At a total pressure of {P} atm the degree of dissociation is about :'
        o, a = mcq(rng, nf(al, 3), [nf(v, 3) for v in (math.sqrt(Kp / P) if Kp < P else al * 1.3, Kp / (Kp + P), math.sqrt(P / (Kp + P)) if n == 1 else math.sqrt(Kp / (Kp + P)), al / 2)])
        f_ = 'K_{p} = \\f{4α^{2}P}{1 − α^{2}}' if n == 2 else 'K_{p} = \\f{α^{2}P}{1 − α^{2}}'
        return dict(q=q, o=o, a=a, sol=['Moles: 1 − α, then products; total 1 + α.', f'{f_} → α ≈ {nf(al, 3)}.'], p=dict(t=t, n=n, Kp=Kp, P=P))
    if t == 'graph':
        p0 = rng.choice([0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]); y = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5]) * p0; tot = p0 + y
        Kp = (2 * y) ** 2 / (p0 - y)
        q = f'CO_{{2}} at {nf(p0)} atm is kept over hot graphite: C(s) + CO_{{2}}(g) ⇌ 2CO(g). The total pressure at equilibrium is {nf(tot, 4)} atm. K_{{p}} (atm) is about :'
        o, a = mcq(rng, nf(Kp, 3), [nf(v, 3) for v in ((2 * y) ** 2 / p0, 2 * y / (p0 - y), y * y / (p0 - y), Kp * 2)])
        return dict(q=q, o=o, a=a, sol=['If CO_{2} falls by p, CO rises by 2p → total = p_{0} + p.', f'p = {nf(y, 4)} → p_{{CO}} = {nf(2 * y, 4)}, p_{{CO_{{2}}}} = {nf(p0 - y, 4)} → K_{{p}} ≈ {nf(Kp, 3)}.'], p=dict(t=t, p0=p0, tot=tot))
    if t == 'dG':
        T = rng.choice([298, 300, 400, 500, 600]); K = rng.choice([2, 5, 10, 20, 50, 100, 1000, 0.1, 0.01, 1e-3, 1e5])
        G = -8.314 * T * math.log(K) / 1000
        q = f'At {T} K, K = {sci(K, 3)} for a reaction. ΔG° (kJ mol^{{−1}}) is about (R = 8.314 J K^{{−1}} mol^{{−1}}) :'
        o, a = mcq(rng, nf(G, 3), [nf(v, 3) for v in (-G, G * 2.303, G / 2.303, -8.314 * T * math.log10(K) / 1000)])
        return dict(q=q, o=o, a=a, sol=['ΔG° = −RT ln K.', f'= −8.314 × {T} × ln({sci(K, 3)}) ≈ {nf(G, 3)} kJ mol^{{−1}}.'], p=dict(t=t, T=T, K=K))
    if t == 'vh':
        T1, T2 = rng.choice([(300, 400), (300, 350), (400, 500), (500, 600), (298, 398), (350, 450)]); H = rng.choice([10, 20, 25, 30, 40, 50, 60]) * rng.choice([1, -1])
        r = math.exp(-H * 1000 / 8.314 * (1 / T2 - 1 / T1)); r = float(nf(r, 3)); Hb = -8.314 * math.log(r) / (1 / T2 - 1 / T1) / 1000
        q = f'The equilibrium constant of a reaction changes by a factor of {nf(r, 3)} (K_{{{T2}}}/K_{{{T1}}}) when the temperature goes from {T1} K to {T2} K. |ΔH°| is about ______ kJ mol^{{−1}} (nearest integer). (R = 8.314 J K^{{−1}} mol^{{−1}})'
        return dict(q=q, o=None, a=round(abs(Hb)), sol=['van \'t Hoff: ln\\f{K_{2}}{K_{1}} = \\f{ΔH°}{R}(\\f{1}{T_{1}} − \\f{1}{T_{2}}).', f'ΔH° ≈ {nf(Hb, 3)} kJ mol^{{−1}}.'], p=dict(t=t, T1=T1, T2=T2, r=r))
    sp = rng.choice(['PCl_{5}', 'COCl_{2}', 'SO_{2}Cl_{2}']); al = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]); P = rng.choice([1, 2, 3, 4, 5, 10])
    Kp = al * al / (1 - al * al) * P
    q = f'{sp}(g) dissociates into {GAS[sp]} to the extent of {int(al * 100)}% at a total pressure of {P} atm. K_{{p}} (atm) is about :'
    o, a = mcq(rng, nf(Kp, 3), [nf(v, 3) for v in (al * al * P, al * al / (1 - al) * P, al / (1 - al * al) * P, Kp / P)])
    return dict(q=q, o=o, a=a, sol=['Moles 1 − α, α, α; total 1 + α.', f'K_{{p}} = \\f{{α^{{2}}P}}{{1 − α^{{2}}}} = \\f{{{nf(al * al, 3)} × {P}}}{{{nf(1 - al * al, 3)}}} ≈ {nf(Kp, 3)}.'], p=dict(t='pres', al=al, P=P))

CHG = [('pressure is increased (volume decreased)', 'P'), ('volume is increased', 'V'), ('temperature is raised', 'T+'), ('temperature is lowered', 'T-'),
       ('a catalyst is added', 'cat'), ('an inert gas is added at constant volume', 'inV'), ('an inert gas is added at constant pressure', 'inP')]
def g_shift(rng):
    t = rng.choice(['lc', 'lc', 'readd', 'Q', 'Kchg'])
    if t in ('lc', 'Kchg'):
        eq, dn, dh = rng.choice(REACT); txt, c = rng.choice(CHG)
        if t == 'Kchg':
            need(c in ('P', 'V', 'cat', 'inV', 'inP', 'T+', 'T-'))
            q = f'For {eq} (ΔH {"<" if dh < 0 else ">"} 0), what happens to the equilibrium constant K when {txt}?'
            o = ['increases', 'decreases', 'stays the same', 'becomes zero']; ans = 'stays the same' if c[0] != 'T' else ('increases' if (dh > 0) == (c == 'T+') else 'decreases')
            o, a = mcq(rng, ans, [x for x in o if x != ans])
            return dict(q=q, o=o, a=a, sol=['K changes only with temperature.', 'Raising T favours the endothermic direction; K grows if the forward reaction is endothermic.'], p=dict(t=t, dn=dn, dh=dh, c=c))
        q = f'For {eq} (ΔH {"<" if dh < 0 else ">"} 0) at equilibrium, the {txt}. The equilibrium :'
        o = ['shifts forward', 'shifts backward', 'does not shift', 'shifts forward and K becomes zero']
        if c == 'P': s = -dn
        elif c in ('V', 'inP'): s = dn
        elif c in ('cat', 'inV'): s = 0
        else: s = dh if c == 'T+' else -dh
        ans = 'does not shift' if s == 0 else ('shifts forward' if s > 0 else 'shifts backward')
        o, a = mcq(rng, ans, [x for x in o if x != ans])
        return dict(q=q, o=o, a=a, sol=['Le Chatelier: the system opposes the change.', 'Pressure up → fewer gas moles; volume up / inert gas at constant P → more gas moles; inert gas at constant V or catalyst → no shift; heat → endothermic side.'], p=dict(t=t, dn=dn, dh=dh, c=c))
    if t == 'readd':
        A, B = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]), rng.choice([0.1, 0.2, 0.3, 0.4, 0.6, 0.9, 1.2]); add = rng.choice([0.1, 0.2, 0.3, 0.5]); who = rng.choice(['A', 'B'])
        K = B / A
        if who == 'A': y = bis(lambda y: (B + y) / (A + add - y) - K, 0, A + add); nA, nB = A + add - y, B + y
        else: y = bis(lambda y: (B + add - y) / (A + y) - K, 0, B + add); nA, nB = A + y, B + add - y
        q = f'For A(g) ⇌ B(g) in a 1 L flask, equilibrium has [A] = {A} M and [B] = {B} M. Then {add} mol of {who} is added at the same temperature. The new [A] is about :'
        o, a = mcq(rng, f'{nf(nA, 3)} M', [f'{nf(v, 3)} M' for v in (A + (add if who == 'A' else 0), A, nA * 1.15, A + add / 2)])
        return dict(q=q, o=o, a=a, sol=[f'K = \\f{{{B}}}{{{A}}} = {nf(K, 3)} — it does not change.', f'Re-solve with the extra {who}: [A] ≈ {nf(nA, 3)} M, [B] ≈ {nf(nB, 3)} M.'], p=dict(t=t, A=A, B=B, add=add, who=who))
    if t == 'Q':
        K = rng.choice([0.5, 1, 2, 4, 9, 16, 25, 50]); a_, b_, c_ = rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([0.1, 0.4, 0.5, 1, 2, 3, 4])
        Q = c_ * c_ / (a_ * b_); need(abs(Q - K) > 1e-9)
        ans = 'goes forward (Q < K)' if Q < K else 'goes backward (Q > K)'
        q = f'For H_{{2}}(g) + I_{{2}}(g) ⇌ 2HI(g), K_{{c}} = {K}. A mixture has [H_{{2}}] = {a_} M, [I_{{2}}] = {b_} M, [HI] = {c_} M. The reaction :'
        o, a = mcq(rng, ans, [x for x in ['goes forward (Q < K)', 'goes backward (Q > K)', 'is at equilibrium (Q = K)', 'goes forward (Q > K)'] if x != ans])
        return dict(q=q, o=o, a=a, sol=['Q = \\f{[HI]^{2}}{[H_{2}][I_{2}]}.', f'Q = {nf(Q, 3)} vs K = {K} → {ans}.'], p=dict(t=t, K=K, a_=a_, b_=b_, c_=c_))
    raise AssertionError

def g_ph(rng):
    t = rng.choice(['strong', 'dil', 'weak', 'ostw', 'kb', 'salt', 'mix', 'ka'])
    if t == 'strong':
        k = rng.choice(['HCl', 'HNO_{3}', 'H_{2}SO_{4}', 'NaOH', 'KOH', 'Ba(OH)_{2}']); c = rng.choice([1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 4e-4]); n = 2 if k in ('H_{2}SO_{4}', 'Ba(OH)_{2}') else 1; base = 'OH' in k
        ph = pH_of_net(0 if base else n * c, n * c if base else 0, 1)
        q = f'The pH of {sci(c, 2)} M {k} (fully ionised) is about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (14 - ph, -math.log10(c) if n == 2 else ph + 0.3, ph + 1 if ph < 13 else ph - 1, ph - 0.3 if n == 1 else ph + 0.3)])
        return dict(q=q, o=o, a=a, sol=[f'[{"OH^{−}" if base else "H^{+}"}] = {n} × {sci(c, 2)} M.', f'pH ≈ {p2(ph)}.'], p=dict(t=t, c=c, n=n, base=base))
    if t == 'dil':
        ph0 = rng.choice([1, 2, 3, 4]); f = rng.choice([2, 4, 5, 10, 100]); ph = pH_of_net(10 ** -ph0 / f, 0, 1)
        q = f'A strong acid solution of pH {ph0} is diluted {f} times with water. The new pH is about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (ph0 * f, ph0 + f, ph0 - math.log10(f), ph0 / f)])
        return dict(q=q, o=o, a=a, sol=[f'[H^{{+}}] drops {f}-fold.', f'pH = {ph0} + log {f} ≈ {p2(ph)}.'], p=dict(t=t, ph0=ph0, f=f))
    if t in ('weak', 'ostw'):
        pKa = rng.choice([3, 3.5, 4, 4.5, 4.74, 5, 5.5, 6]); c = rng.choice([0.001, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]); Ka = 10 ** -pKa; h = H_weak(c, Ka)
        need(h / c < 0.12)
        if t == 'weak':
            q = f'The pH of {c} M weak acid HA (K_{{a}} = {sci(Ka, 3)}) is about :'
            o, a = mcq(rng, p2(-math.log10(h)), [p2(v) for v in (-math.log10(c), pKa, -math.log10(Ka * c), -math.log10(h) + 1)])
            return dict(q=q, o=o, a=a, sol=['[H^{+}] ≈ √{K_{a}c}.', f'pH ≈ ½(pK_{{a}} − log c) ≈ {p2(-math.log10(h))}.'], p=dict(t=t, c=c, Ka=Ka))
        q = f'The degree of dissociation of {c} M HA (K_{{a}} = {sci(Ka, 3)}) is about :'
        o, a = mcq(rng, sci(h / c, 3), [sci(v, 3) for v in (Ka / c, math.sqrt(Ka * c), h / c * 10, math.sqrt(Ka))])
        return dict(q=q, o=o, a=a, sol=['Ostwald: α ≈ √{\\f{K_{a}}{c}}.', f'α ≈ {sci(h / c, 3)}.'], p=dict(t=t, c=c, Ka=Ka))
    if t == 'kb':
        c = rng.choice([1e-3, 1e-2, 0.1, 0.05, 0.02]); pOH = rng.choice([2.5, 3, 3.5, 4, 4.5, 5]); oh = 10 ** -pOH; need(oh / c < 0.1)
        Kb = oh * oh / (c - oh)
        q = f'A {c} M solution of a weak base has pH {nf(14 - pOH)}. K_{{b}} of the base is about :'
        o, a = mcq(rng, sci(Kb, 3), [sci(v, 3) for v in (oh / c, (10 ** -(14 - pOH)) ** 2 / c, oh * oh, oh)])
        return dict(q=q, o=o, a=a, sol=[f'pOH = {nf(pOH)} → [OH^{{−}}] = {sci(oh, 3)}.', f'K_{{b}} = \\f{{[OH^{{−}}]^{{2}}}}{{c − [OH^{{−}}]}} ≈ {sci(Kb, 3)}.'], p=dict(t=t, c=c, pOH=pOH))
    if t == 'salt':
        pKa = rng.choice([4, 4.74, 5, 6, 3.5]); c = rng.choice([0.01, 0.05, 0.1, 0.2, 1]); s = rng.choice(['acid', 'base'])
        ph = 7 + 0.5 * pKa + 0.5 * math.log10(c) if s == 'acid' else 7 - 0.5 * pKa - 0.5 * math.log10(c)
        nm = f'sodium salt NaA of a weak acid (pK_{{a}} = {pKa})' if s == 'acid' else f'chloride BHCl of a weak base (pK_{{b}} = {pKa})'
        q = f'The pH of a {c} M solution of the {nm} is about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (14 - ph, 7, 7 + pKa if s == 'acid' else 7 - pKa, ph + 0.5)])
        return dict(q=q, o=o, a=a, sol=['A salt of weak acid + strong base is basic; of weak base + strong acid, acidic.', f'pH = 7 {"+" if s == "acid" else "−"} ½p{"K_{a}" if s == "acid" else "K_{b}"} {"+" if s == "acid" else "−"} ½log c ≈ {p2(ph)}.'], p=dict(t=t, pKa=pKa, c=c, s=s))
    if t == 'mix':
        V1, c1, V2, c2 = rng.choice([10, 20, 25, 50, 100]), rng.choice([0.1, 0.2, 0.05, 0.01]), rng.choice([10, 20, 25, 40, 50, 100]), rng.choice([0.1, 0.2, 0.05, 0.01])
        nH, nOH = V1 * c1 / 1000, V2 * c2 / 1000; need(abs(nH - nOH) > 1e-6); ph = pH_of_net(nH, nOH, (V1 + V2) / 1000)
        q = f'{V1} mL of {c1} M HCl is mixed with {V2} mL of {c2} M NaOH. The pH of the mixture is about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (14 - ph, 7, -math.log10(abs(nH - nOH)), ph + 0.3)])
        return dict(q=q, o=o, a=a, sol=[f'Leftover {"H^{+}" if nH > nOH else "OH^{−}"} = |{nf(nH * 1000, 3)} − {nf(nOH * 1000, 3)}| mmol in {V1 + V2} mL.', f'pH ≈ {p2(ph)}.'], p=dict(t=t, V1=V1, c1=c1, V2=V2, c2=c2))
    pH = rng.choice([2.5, 3, 3.5, 4, 4.5, 5]); c = rng.choice([0.01, 0.05, 0.1, 0.2, 1]); h = 10 ** -pH; need(h / c < 0.1)
    Ka = h * h / (c - h)
    q = f'A {c} M solution of a weak monobasic acid has pH {pH}. K_{{a}} is about :'
    o, a = mcq(rng, sci(Ka, 3), [sci(v, 3) for v in (h / c, h * h, h, h * h / c * 10)])
    return dict(q=q, o=o, a=a, sol=[f'[H^{{+}}] = 10^{{−{pH}}}.', f'K_{{a}} = \\f{{[H^{{+}}]^{{2}}}}{{c − [H^{{+}}]}} ≈ {sci(Ka, 3)}.'], p=dict(t='ka', c=c, pH=pH))

def g_buf(rng):
    t = rng.choice(['hh', 'hhb', 'addH', 'half', 'ratio', 'tit'])
    if t in ('hh', 'hhb'):
        pK = rng.choice([4.74, 4.75, 4.2, 3.75, 9.25, 4.76, 5.0, 6.4]) if t == 'hh' else rng.choice([4.74, 4.75, 3.4, 5.0]); na, ns = rng.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.3]), rng.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.4])
        need(0.2 <= ns / na <= 5 and 10 ** -(pK if t == 'hh' else pK) / min(na, ns) < 0.002)
        ph = pK + math.log10(ns / na) if t == 'hh' else 14 - (pK + math.log10(ns / na))
        q = (f'A buffer contains {na} mol of a weak acid (pK_{{a}} = {pK}) and {ns} mol of its sodium salt in 1 L. Its pH is about :' if t == 'hh'
             else f'A buffer contains {na} mol NH_{{3}}-like weak base (pK_{{b}} = {pK}) and {ns} mol of its chloride salt in 1 L. Its pH is about :')
        alt = pK - math.log10(ns / na) if t == 'hh' else 14 - (pK - math.log10(ns / na))
        o, a = mcq(rng, p2(ph), [p2(v) for v in (alt, pK, 14 - ph, ph + 0.5)])
        return dict(q=q, o=o, a=a, sol=['Henderson: pH = pK_{a} + log\\f{[salt]}{[acid]}; for a base, pOH = pK_{b} + log\\f{[salt]}{[base]}.', f'pH ≈ {p2(ph)}.'], p=dict(t=t, pK=pK, na=na, ns=ns))
    if t == 'addH':
        pKb = rng.choice([4.74, 4.75]); nb, ns = rng.choice([0.1, 0.2, 0.3]), rng.choice([0.1, 0.2, 0.3]); x = rng.choice([0.01, 0.02, 0.05]); need(x < nb)
        d = abs(math.log10((ns + x) / (nb - x)) - math.log10(ns / nb))
        q = f'1 L of buffer has {nb} mol NH_{{3}} and {ns} mol NH_{{4}}Cl (pK_{{b}} = {pKb}). The change in pH on adding {x} mol HCl is ______ × 10^{{−2}} (nearest integer).'
        return dict(q=q, o=None, a=round(d * 100), sol=[f'HCl converts {x} mol NH_{{3}} → NH_{{4}}^{{+}}.', f'ΔpH = log\\f{{{nf(ns + x)}}}{{{nf(nb - x)}}} − log\\f{{{ns}}}{{{nb}}} ≈ {nf(d, 3)}.'], p=dict(t=t, nb=nb, ns=ns, x=x))
    if t == 'half':
        pKa = rng.choice([3.3, 4.2, 4.74, 4.75, 5.0, 3.75]); V, c = rng.choice([10, 20, 25, 50]), rng.choice([0.1, 0.2]); f = rng.choice([0.25, 0.5, 0.75, 0.2, 0.8])
        ph = pKa + math.log10(f / (1 - f))
        q = f'{V} mL of {c} M weak acid HA (pK_{{a}} = {pKa}) is titrated with {c} M NaOH. pH after {nf(V * f)} mL NaOH is added is about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (pKa, pKa - math.log10(f / (1 - f)), 7, ph + 1)])
        return dict(q=q, o=o, a=a, sol=[f'{int(f * 100)}% neutralised: salt : acid = {nf(f)} : {nf(1 - f)}.', f'pH = pK_{{a}} + log\\f{{{nf(f)}}}{{{nf(1 - f)}}} ≈ {p2(ph)}.'], p=dict(t=t, pKa=pKa, f=f))
    if t == 'ratio':
        pKa = rng.choice([4.2, 4.74, 4.76, 3.75]); d = rng.choice([-0.3, 0.3, 0, 0.6, -0.6, 0.477, -0.477]); tot = rng.choice([100, 150, 200, 300, 400, 600])
        r = 10 ** d; va = tot / (1 + r); need(abs(va - round(va)) < 0.6)
        q = f'Equal-molarity solutions of a weak acid (pK_{{a}} = {pKa}) and its sodium salt are mixed to make {tot} mL of buffer of pH {nf(pKa + d, 4)}. The volume of acid solution used is ______ mL (nearest integer).'
        return dict(q=q, o=None, a=round(va), sol=[f'log\\f{{salt}}{{acid}} = {nf(d, 3)} → ratio ≈ {nf(r, 3)}.', f'acid = \\f{{{tot}}}{{1 + {nf(r, 3)}}} ≈ {round(va)} mL.'], p=dict(t=t, pKa=pKa, d=d, tot=tot))
    V1, c1 = rng.choice([10, 20, 25, 50]), rng.choice([0.1, 0.2]); Ka = rng.choice([1e-5, 1.8e-5, 5e-4, 2e-5, 1e-4]); h = H_weak(c1, Ka)
    q = f'The pH of {V1} mL of {c1} M weak acid (K_{{a}} = {sci(Ka, 2)}) before any NaOH is added is about :'
    o, a = mcq(rng, p2(-math.log10(h)), [p2(v) for v in (-math.log10(c1), -math.log10(Ka), -math.log10(h) + 1, -math.log10(Ka * c1))])
    return dict(q=q, o=o, a=a, sol=['Only the weak acid: [H^{+}] ≈ √{K_{a}c}.', f'pH ≈ {p2(-math.log10(h))}.'], p=dict(t='tit', c=c1, Ka=Ka))

SALT = {'AgCl': (1, 1), 'BaSO_{4}': (1, 1), 'CaF_{2}': (1, 2), 'PbI_{2}': (1, 2), 'Mg(OH)_{2}': (1, 2), 'Ag_{2}CrO_{4}': (2, 1), 'Ag_{2}CO_{3}': (2, 1), 'Al(OH)_{3}': (1, 3), 'Fe(OH)_{3}': (1, 3), 'Ca_{3}(PO_{4})_{2}': (3, 2)}
def kf(p, q, s): return (p * s) ** p * (q * s) ** q
def g_ksp(rng):
    t = rng.choice(['s', 'K', 'common', 'ppt', 'pHppt', 'gL'])
    if t == 's':
        sl = rng.choice(list(SALT)); p, q_ = SALT[sl]; K = rng.choice([1.6, 2.7, 3.2, 4, 5, 6.4, 8, 1.08, 1.0]) * 10 ** rng.choice([-10, -11, -12, -13, -15, -18, -20, -25, -30])
        s = (K / (p ** p * q_ ** q_)) ** (1 / (p + q_))
        q = f'K_{{sp}} of {sl} is {sci(K, 3)}. Its molar solubility in water is about :'
        o, a = mcq(rng, sci(s, 3), [sci(v, 3) for v in (K ** (1 / (p + q_)), math.sqrt(K), s * (p + q_), s / 2)])
        return dict(q=q, o=o, a=a, sol=[f'K_{{sp}} = ({p}s)^{{{p}}}({q_}s)^{{{q_}}} = {p ** p * q_ ** q_}s^{{{p + q_}}}.', f's ≈ {sci(s, 3)} M.'], p=dict(t=t, sl=sl, K=K))
    if t == 'K':
        sl = rng.choice(list(SALT)); p, q_ = SALT[sl]; s = rng.choice([1, 1.5, 2, 2.5, 3, 4, 5]) * 10 ** rng.choice([-3, -4, -5, -6]); K = kf(p, q_, s)
        q = f'The molar solubility of {sl} is {sci(s, 2)} M. Its K_{{sp}} is about :'
        o, a = mcq(rng, sci(K, 3), [sci(v, 3) for v in (s ** (p + q_), s * s, K * 2, K / 4 if K / 4 != s ** (p + q_) else K * 3)])
        return dict(q=q, o=o, a=a, sol=[f'Ions: {p}s and {q_}s.', f'K_{{sp}} = {p ** p * q_ ** q_} × ({sci(s, 2)})^{{{p + q_}}} ≈ {sci(K, 3)}.'], p=dict(t=t, sl=sl, s=s))
    if t == 'common':
        sl = rng.choice(['AgCl', 'BaSO_{4}', 'CaF_{2}', 'PbI_{2}', 'Mg(OH)_{2}']); p, q_ = SALT[sl]; K = rng.choice([1.6, 1.8, 4, 5, 8, 1.1]) * 10 ** rng.choice([-10, -11, -12, -9, -8]); c = rng.choice([0.01, 0.02, 0.05, 0.1, 0.2])
        an = {'AgCl': 'NaCl', 'BaSO_{4}': 'Na_{2}SO_{4}', 'CaF_{2}': 'NaF', 'PbI_{2}': 'KI', 'Mg(OH)_{2}': 'NaOH'}[sl]
        s = K / (c ** q_); need(s < 0.002 * c)
        q = f'K_{{sp}} of {sl} is {sci(K, 2)}. Its solubility in {c} M {an} is about :'
        o, a = mcq(rng, sci(s, 3), [sci(v, 3) for v in ((K / (q_ ** q_)) ** (1 / (1 + q_)), K / c if q_ == 2 else K / c ** 2, K, s * 2)])
        return dict(q=q, o=o, a=a, sol=['Common ion: the anion comes almost entirely from the added salt.', f's ≈ \\f{{K_{{sp}}}}{{({c})^{{{q_}}}}} ≈ {sci(s, 3)} M.'], p=dict(t=t, sl=sl, K=K, c=c))
    if t == 'ppt':
        K = rng.choice([1.8e-10, 5e-13, 1.1e-10, 8e-9]); c1, c2 = rng.choice([1e-3, 2e-4, 1e-5, 4e-5, 2e-6]), rng.choice([1e-3, 2e-4, 1e-5, 4e-5, 2e-6])
        Q = (c1 / 2) * (c2 / 2); need(abs(math.log10(Q / K)) > 0.15)
        ans = 'precipitate forms (Q > K_{sp})' if Q > K else 'no precipitate (Q < K_{sp})'
        q = f'Equal volumes of {sci(c1, 2)} M AgNO_{{3}} and {sci(c2, 2)} M NaX are mixed. K_{{sp}}(AgX) = {sci(K, 2)}. Then :'
        o, a = mcq(rng, ans, [x for x in ['precipitate forms (Q > K_{sp})', 'no precipitate (Q < K_{sp})', 'precipitate forms (Q < K_{sp})', 'no precipitate (Q > K_{sp})'] if x != ans])
        return dict(q=q, o=o, a=a, sol=['Mixing equal volumes halves each concentration.', f'Q = {sci(c1 / 2, 2)} × {sci(c2 / 2, 2)} = {sci(Q, 2)} vs K_{{sp}} = {sci(K, 2)}.'], p=dict(t=t, K=K, c1=c1, c2=c2))
    if t == 'pHppt':
        K = rng.choice([1, 4, 1.6, 9, 2.5]) * 10 ** rng.choice([-11, -12, -13, -15, -17]); c = rng.choice([0.01, 0.1, 0.001, 0.04])
        oh = math.sqrt(K / c); ph = 14 + math.log10(oh); need(4 < ph < 13)
        q = f'K_{{sp}} of M(OH)_{{2}} is {sci(K, 2)}. Precipitation from a {c} M M^{{2+}} solution begins at pH about :'
        o, a = mcq(rng, p2(ph), [p2(v) for v in (14 - ph, -math.log10(oh), 14 + math.log10(K / c), ph + 1)])
        return dict(q=q, o=o, a=a, sol=['Starts when [M^{2+}][OH^{−}]^{2} = K_{sp}.', f'[OH^{{−}}] = √{{\\f{{{sci(K, 2)}}}{{{c}}}}} = {sci(oh, 3)} → pH ≈ {nf(ph, 3)}.'], p=dict(t=t, K=K, c=c))
    sl = rng.choice(['AgCl', 'BaSO_{4}', 'CaF_{2}', 'PbI_{2}']); p, q_ = SALT[sl]; mw = {'AgCl': 143.5, 'BaSO_{4}': 233, 'CaF_{2}': 78, 'PbI_{2}': 461}[sl]; g = rng.choice([1, 1.5, 2, 2.5, 3, 4, 6, 8]) * 10 ** rng.choice([-3, -4, -2])
    s = g / mw; K = kf(p, q_, s)
    q = f'The solubility of {sl} (M = {mw} g/mol) is {sci(g, 2)} g L^{{−1}}. Its K_{{sp}} is about :'
    o, a = mcq(rng, sci(K, 3), [sci(v, 3) for v in (kf(p, q_, g), s ** (p + q_), K * 4, s)])
    return dict(q=q, o=o, a=a, sol=[f's = \\f{{{sci(g, 2)}}}{{{mw}}} = {sci(s, 3)} M.', f'K_{{sp}} = {p ** p * q_ ** q_}s^{{{p + q_}}} ≈ {sci(K, 3)}.'], p=dict(t='gL', sl=sl, g=g, mw=mw))

def robust(gf):
    def w(rng):
        for _ in range(300):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, OverflowError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(kp=g_kp, shift=g_shift, ph=g_ph, buf=g_buf, ksp=g_ksp).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'comb': return close(num(Rv), math.exp(p['n'] * math.log(p['K'])), 0.03)
    if t == 'kpkc': return close(num(Rv), p['Kc'] * math.exp(p['dn'] * math.log(0.0821 * p['T'])), 0.01)
    if t == 'ice':   # independent: march the reaction until Q = K
        y = bis(lambda y: math.log(max((2 * y) ** 2, 1e-300)) - math.log((p['a0'] - y) * (p['b0'] - y)) - math.log(p['Kc']), 1e-12, min(p['a0'], p['b0']) - 1e-12)
        return close(num(Rv), 2 * y)
    if t == 'alpha':
        P = p['P']
        if p['n'] == 2: f = lambda a: (2 * a / (1 + a) * P) ** 2 / ((1 - a) / (1 + a) * P) - p['Kp']
        else: f = lambda a: (a / (1 + a) * P) ** 2 / ((1 - a) / (1 + a) * P) - p['Kp']
        return close(num(Rv), bis(f, 1e-12, 1 - 1e-12))
    if t == 'graph':
        y = bis(lambda y: p['p0'] + y - p['tot'], 0, p['p0']); return close(num(Rv), (2 * y) ** 2 / (p['p0'] - y))
    if t == 'dG': return close(num(Rv), -8.314 * p['T'] * 2.302585 * math.log10(p['K']) / 1000)
    if t == 'vh':
        H = bis(lambda H: math.exp(-H * 1000 / 8.314 * (1 / p['T2'] - 1 / p['T1'])) - p['r'], -500, 500); return Rv == round(abs(H))
    if t == 'pres':
        a, P = p['al'], p['P']; return close(num(Rv), (a / (1 + a) * P) ** 2 / ((1 - a) / (1 + a) * P))
    if t == 'Kchg':
        if p['c'][0] != 'T': return Rv == 'stays the same'
        up = (p['c'] == 'T+'); return Rv == ('increases' if (p['dh'] > 0) == up else 'decreases')
    if t == 'lc':   # simulate: sign of change in Q at fixed K, or K change at fixed Q
        dn, dh, c = p['dn'], p['dh'], p['c']
        if c in ('P', 'V', 'inP'):
            f = 0.5 if c == 'P' else 2.0   # volume factor
            Qfac = f ** (-dn)   # concentrations scale by 1/f → Q_c scales by f^{-Δn}
            want = 'does not shift' if dn == 0 else ('shifts forward' if Qfac < 1 else 'shifts backward')
        elif c in ('cat', 'inV'): want = 'does not shift'
        else:
            Kup = (dh > 0) == (c == 'T+'); want = 'shifts forward' if Kup else 'shifts backward'
        return Rv == want
    if t == 'readd':
        K = p['B'] / p['A']; nA = p['A'] + (p['add'] if p['who'] == 'A' else 0); nB = p['B'] + (p['add'] if p['who'] == 'B' else 0); tot = nA + nB
        a = tot / (1 + K); return close(num(Rv), a)
    if t == 'Q':
        Q = p['c_'] ** 2 / (p['a_'] * p['b_']); return Rv.startswith('goes forward (Q <') if Q < p['K'] else Rv.startswith('goes backward (Q >')
    if t == 'strong':
        n = p['n'] * p['c']; ph = (-math.log10(H_weak(n, 1e6)) if not p['base'] else 14 + math.log10(n)); return abs(num(Rv) - ph) < 0.02
    if t == 'dil':
        c = 10 ** -p['ph0'] / p['f']; h = bis(lambda h: h - c - 1e-14 / h, 1e-15, 1); return abs(num(Rv) + math.log10(h)) < 0.02
    if t in ('weak', 'tit'):
        Ka, c = p['Ka'], p['c']; return abs(num(Rv) + math.log10((-Ka + math.sqrt(Ka * Ka + 4 * Ka * c)) / 2)) < 0.02
    if t == 'ostw': return close(num(Rv), H_weak(p['c'], p['Ka'], 0) / p['c'], 0.03)
    if t == 'kb':
        oh = 10 ** -p['pOH']; return close(num(Rv), oh * oh / (p['c'] - oh), 0.02)
    if t == 'ka':
        h = 10 ** -p['pH']; return close(num(Rv), h * h / (p['c'] - h), 0.02)
    if t == 'salt':   # hydrolysis by exact balance
        Kh = 1e-14 / 10 ** -p['pKa']; x = bis(lambda x: x * x / (p['c'] - x) - Kh, 1e-15, p['c']); return abs(num(Rv) - ((14 + math.log10(x)) if p['s'] == 'acid' else -math.log10(x))) < 0.02
    if t == 'mix':
        nH, nOH, V = p['V1'] * p['c1'], p['V2'] * p['c2'], p['V1'] + p['V2']; d = (nH - nOH) / V
        return abs(num(Rv) - (-math.log10(d) if d > 0 else 14 + math.log10(-d))) < 0.02
    if t == 'hh':   # build the mixture: solve [H+] with acid/salt charge balance
        Ka = 10 ** -p['pK']; h = bis(lambda h: Ka * (p['na'] - h) - h * (p['ns'] + h), 1e-15, p['na']); return abs(num(Rv) + math.log10(h)) < 0.02
    if t == 'hhb':
        Kb = 10 ** -p['pK']; oh = bis(lambda x: Kb * (p['na'] - x) - x * (p['ns'] + x), 1e-15, p['na']); return abs(num(Rv) - 14 - math.log10(oh)) < 0.02
    if t == 'addH':
        Kb = 10 ** -4.75; f = lambda nb, ns: 14 + math.log10(Kb * nb / ns); return Rv == round(abs(f(p['nb'], p['ns']) - f(p['nb'] - p['x'], p['ns'] + p['x'])) * 100)
    if t == 'half':
        Ka = 10 ** -p['pKa']; return abs(num(Rv) + math.log10(Ka * (1 - p['f']) / p['f'])) < 0.02
    if t == 'ratio':
        va = bis(lambda va: p['pKa'] + math.log10((p['tot'] - va) / va) - (p['pKa'] + p['d']), 1e-6, p['tot'] - 1e-6); return Rv == round(va)
    if t in ('s', 'K', 'gL'):
        a_, b_ = SALT[p['sl']]
        if t == 's': return close(num(Rv), bis(lambda s: math.log(kf(a_, b_, s)) - math.log(p['K']), 1e-40, 1), 0.01)
        s = p['s'] if t == 'K' else p['g'] / p['mw']; return close(num(Rv), (a_ * s) ** a_ * (b_ * s) ** b_, 0.01)
    if t == 'common':
        a_, b_ = SALT[p['sl']]; s = bis(lambda s: (a_ * s) ** a_ * (p['c'] + b_ * s) ** b_ - p['K'], 0, 1); return close(num(Rv), s, 0.02)
    if t == 'ppt':
        return ('forms' in Rv and 'Q > ' in Rv) if (p['c1'] / 2) * (p['c2'] / 2) > p['K'] else ('no precipitate' in Rv and 'Q < ' in Rv)
    if t == 'pHppt': return abs(num(Rv) - (14 + 0.5 * math.log10(p['K'] / p['c']))) < 0.02
    raise KeyError(t)
