"""Practice generators — Chemistry Unit 4: Chemical Thermodynamics. check() re-solves each item independently:
work by numerical integration of p dV, Hess cycles by summing formation enthalpies atom-by-atom, bond cycles by
counting bonds broken and made, and spontaneity by scanning ΔG over temperature."""
import math
from common import mcq, nf
R = 8.314
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').replace('+', '').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def m_(x, s=4): return nf(x, s).replace('-', '−')
def integ(f, a, b, n=4000):   # Simpson
    h = (b - a) / n; s = f(a) + f(b)
    for i in range(1, n): s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3

# compound: (formula text, M, gas moles of CO2 + water state handled in reaction list), Δ_cH (kJ/mol)
FUEL = {'methane': ('CH_{4}(g)', 16, 1, 4, 0, 'g', -890.3), 'ethane': ('C_{2}H_{6}(g)', 30, 2, 6, 0, 'g', -1560), 'propane': ('C_{3}H_{8}(g)', 44, 3, 8, 0, 'g', -2220),
        'ethanol': ('C_{2}H_{5}OH(l)', 46, 2, 6, 1, 'l', -1367), 'methanol': ('CH_{3}OH(l)', 32, 1, 4, 1, 'l', -726), 'benzene': ('C_{6}H_{6}(l)', 78, 6, 6, 0, 'l', -3268),
        'glucose': ('C_{6}H_{12}O_{6}(s)', 180, 6, 12, 6, 's', -2808), 'octane': ('C_{8}H_{18}(l)', 114, 8, 18, 0, 'l', -5471), 'naphthalene': ('C_{10}H_{8}(s)', 128, 10, 8, 0, 's', -5157),
        'benzoic acid': ('C_{6}H_{5}COOH(s)', 122, 7, 6, 2, 's', -3227), 'sucrose': ('C_{12}H_{22}O_{11}(s)', 342, 12, 22, 11, 's', -5645), 'acetic acid': ('CH_{3}COOH(l)', 60, 2, 4, 2, 'l', -875)}
def dn_comb(f):   # CxHyOz + (x + y/4 − z/2) O2 → x CO2 + y/2 H2O(l)
    _, _, x, y, z, st, _ = FUEL[f]; o2 = x + y / 4 - z / 2; return x - o2 - (1 if st == 'g' else 0)

def g_law(rng):
    t = rng.choice(['iso', 'irr', 'dhdu', 'bomb', 'heat', 'adia', 'free'])
    if t == 'iso':
        n = rng.choice([0.5, 1, 2, 3, 5]); T = rng.choice([298, 300, 350, 400, 500]); V1 = rng.choice([1, 2, 5, 10, 20]); f = rng.choice([2, 3, 4, 5, 10, 0.5, 0.25, 0.1])
        V2 = V1 * f; w = -n * R * T * math.log(f)
        o, a = mcq(rng, f'{m_(w / 1000, 3)} kJ', [f'{m_(v / 1000, 3)} kJ' for v in (-w, w / 2.303, -n * R * T * math.log10(f), w * 2)])
        return dict(q=f'{n} mol of an ideal gas is {"expanded" if f > 1 else "compressed"} isothermally and reversibly at {T} K from {V1} L to {nf(V2)} L. The work done ON the gas (w) is :', o=o, a=a,
                    sol=['w = −nRT ln\\f{V_{2}}{V_{1}} (sign convention: w on the system).', f'= −{n} × 8.314 × {T} × ln {nf(f)} ≈ {m_(w / 1000, 3)} kJ.'], p=dict(t=t, n=n, T=T, V1=V1, V2=V2))
    if t == 'irr':
        p = rng.choice([1, 2, 3, 5, 10]); V1, V2 = rng.sample([5, 10, 15, 20, 30, 40, 50, 60], 2); w = -p * (V2 - V1)
        q = f'An ideal gas is {"expanded" if V2 > V1 else "compressed"} isothermally from {V1} L to {V2} L against a constant external pressure of {p} atm. The heat q absorbed by the gas is ____ L atm (negative means released; nearest integer).'
        return dict(q=q, o=None, a=round(-w), sol=[f'w = −p_{{ext}}ΔV = −{p}({V2} − {V1}) = {m_(w)} L atm.', f'Isothermal ideal gas: ΔU = 0 → q = −w = {m_(-w)} L atm.'], p=dict(t=t, p=p, V1=V1, V2=V2))
    if t == 'dhdu':
        f = rng.choice(list(FUEL)); dn = dn_comb(f); need(dn != 0); T = rng.choice([298, 300]); dU = FUEL[f][6] + rng.choice([-3, 0, 2, 5])
        dH = dU + dn * R * T / 1000
        o, a = mcq(rng, f'{m_(dH, 5)} kJ mol^{{−1}}', [f'{m_(v, 5)} kJ mol^{{−1}}' for v in (dU - dn * R * T / 1000, dU + dn * 8.314 * T, dU, dU + 2 * dn * R * T / 1000)])
        return dict(q=f'The heat of combustion of {f} ({FUEL[f][0]}) at constant volume is {m_(dU, 5)} kJ mol^{{−1}} at {T} K (water forms as liquid). Its enthalpy of combustion is about :', o=o, a=a,
                    sol=[f'Δn_{{g}} = {nf(dn)} (CO_{{2}} formed − O_{{2}} used − gaseous fuel).', f'ΔH = ΔU + Δn_{{g}}RT = {m_(dU, 5)} + ({nf(dn)})(8.314 × 10^{{−3}})({T}) ≈ {m_(dH, 5)} kJ mol^{{−1}}.'], p=dict(t=t, f=f, T=T, dU=dU))
    if t == 'bomb':
        f = rng.choice(list(FUEL)); M = FUEL[f][1]; C = rng.choice([2, 2.5, 4, 5, 8, 10, 12]); n = rng.choice([0.005, 0.01, 0.02, 0.025]); dT = -FUEL[f][6] * n / C
        need(0.3 < dT < 30); dT = round(dT, 2); g = n * M; dU = -C * dT / n
        return dict(q=f'{nf(g, 4)} g of {f} (M = {M}) burns in a bomb calorimeter of heat capacity {C} kJ K^{{−1}}; the temperature rises by {dT} K. The magnitude of Δ_{{c}}U is ____ kJ mol^{{−1}} (nearest integer).', o=None, a=round(-dU),
                    sol=[f'Heat released = CΔT = {C} × {dT} = {nf(C * dT, 4)} kJ for {nf(n)} mol.', f'|Δ_{{c}}U| = {round(-dU)} kJ mol^{{−1}}.'], p=dict(t=t, g=g, M=M, C=C, dT=dT))
    if t == 'heat':
        T1 = rng.choice([10, 20, 25, 30, 50]); T2 = rng.choice([-5, -10, -15, -20]); y, z, x = 75.3, rng.choice([36.8, 37.6, 38.0]), 6.01; nmol = rng.choice([1, 2, 0.5])
        H = nmol * (-(T1 * y) / 1000 - x + (T2 * z) / 1000)
        o, a = mcq(rng, f'{m_(H, 4)} kJ', [f'{m_(v, 4)} kJ' for v in (-H, nmol * (-x), nmol * (-(T1 * y) - x + T2 * z) / 1000 * 1000 / 1000 - 1, H + nmol * 2 * T2 * z / 1000)])
        return dict(q=f'{nmol} mol water at {T1} °C is turned into ice at {T2} °C. ΔH = ? (C_{{p}}(water) = {y}, C_{{p}}(ice) = {z} J mol^{{−1}} K^{{−1}}, Δ_{{fus}}H = {x} kJ mol^{{−1}})', o=o, a=a,
                    sol=['Cool the water to 0 °C, freeze it, cool the ice.', f'ΔH = {nmol}[−{T1} × {y} − {x} × 1000 − {abs(T2)} × {z}] J ≈ {m_(H, 4)} kJ.'], p=dict(t=t, T1=T1, T2=T2, z=z, n=nmol))
    if t == 'adia':
        Cv = rng.choice([1.5, 2.5, 3]); T1 = rng.choice([298, 300, 400, 500]); p1 = rng.choice([2, 4, 5, 10]); pe = rng.choice([1, 1, 2]); f = rng.choice([2, 1.5, 3]); need(pe < p1)
        T2 = T1 - pe * (f - 1) * (T1 / p1) / Cv
        return dict(q=f'An ideal gas (C_{{V}} = {nf(Cv)}R) at {T1} K and {p1} atm expands adiabatically against a constant {pe} atm until its volume becomes {nf(f)} times. The final temperature is ____ K (nearest integer).', o=None, a=round(T2),
                    sol=['q = 0 → nC_{V}ΔT = −p_{ext}ΔV with V_{1} = \\f{nRT_{1}}{p_{1}}.', f'{nf(Cv)}(T_{{2}} − {T1}) = −{pe}({nf(f - 1)})\\f{{{T1}}}{{{p1}}} → T_{{2}} ≈ {round(T2)} K.'], p=dict(t=t, Cv=Cv, T1=T1, p1=p1, pe=pe, f=f))
    pr = rng.choice(['free expansion of an ideal gas into vacuum', 'reversible isothermal expansion of an ideal gas', 'reversible adiabatic expansion of an ideal gas', 'isochoric heating of an ideal gas', 'melting of ice at 273 K and 1 atm'])
    ans = {'free expansion of an ideal gas into vacuum': 'w = 0, q = 0, ΔU = 0', 'reversible isothermal expansion of an ideal gas': 'ΔU = 0, q = −w > 0', 'reversible adiabatic expansion of an ideal gas': 'q = 0, ΔU = w < 0',
           'isochoric heating of an ideal gas': 'w = 0, ΔU = q > 0', 'melting of ice at 273 K and 1 atm': 'ΔG = 0, ΔH > 0, ΔS > 0'}
    o, a = mcq(rng, ans[pr], [v for k, v in ans.items() if k != pr])
    return dict(q=f'Which set is correct for {pr}?', o=o, a=a, sol=['First law: ΔU = q + w (w on the system).', f'{pr[0].upper() + pr[1:]}: {ans[pr]}.'], p=dict(t='free', pr=pr))

FH = {'CO_{2}(g)': -393.5, 'H_{2}O(l)': -285.8, 'H_{2}O(g)': -241.8, 'CO(g)': -110.5, 'NH_{3}(g)': -46.1, 'NO(g)': 90.3, 'NO_{2}(g)': 33.2, 'SO_{2}(g)': -296.8, 'SO_{3}(g)': -395.7,
      'HCl(g)': -92.3, 'CH_{4}(g)': -74.8, 'C_{2}H_{4}(g)': 52.3, 'C_{2}H_{6}(g)': -84.7, 'C_{2}H_{2}(g)': 226.7, 'H_{2}S(g)': -20.6, 'Fe_{2}O_{3}(s)': -824.2, 'Al_{2}O_{3}(s)': -1675.7,
      'CaO(s)': -635.1, 'CaCO_{3}(s)': -1206.9, 'N_{2}O_{4}(g)': 9.2, 'CH_{3}OH(l)': -238.7, 'C_{2}H_{5}OH(l)': -277.7}
RX = [({'CH_{4}(g)': 1}, {'CO_{2}(g)': 1, 'H_{2}O(l)': 2}), ({'C_{2}H_{4}(g)': 1}, {'C_{2}H_{6}(g)': 1}), ({'NH_{3}(g)': 4}, {'NO(g)': 4, 'H_{2}O(g)': 6}), ({'SO_{2}(g)': 2}, {'SO_{3}(g)': 2}),
      ({'Fe_{2}O_{3}(s)': 1, 'CO(g)': 3}, {'CO_{2}(g)': 3}), ({'CaCO_{3}(s)': 1}, {'CaO(s)': 1, 'CO_{2}(g)': 1}), ({'Fe_{2}O_{3}(s)': 1}, {'Al_{2}O_{3}(s)': 1}), ({'NO_{2}(g)': 2}, {'N_{2}O_{4}(g)': 1}),
      ({'H_{2}S(g)': 2}, {'H_{2}O(l)': 2, 'SO_{2}(g)': 2}), ({'C_{2}H_{2}(g)': 1}, {'C_{2}H_{6}(g)': 1}), ({'CH_{3}OH(l)': 2}, {'CO_{2}(g)': 2, 'H_{2}O(l)': 4}), ({'C_{2}H_{5}OH(l)': 1}, {'CO_{2}(g)': 2, 'H_{2}O(l)': 3}),
      ({'CO(g)': 2}, {'CO_{2}(g)': 2}), ({'NO(g)': 2}, {'NO_{2}(g)': 2})]
EXTRA = {0: ' + 2O_{2}(g)', 1: ' + H_{2}(g)', 2: ' + 5O_{2}(g)', 3: ' + O_{2}(g)', 4: ' → 2Fe(s) + ', 5: '', 6: ' + 2Al(s) → 2Fe(s) + ', 7: '', 8: ' + 3O_{2}(g)', 9: ' + 2H_{2}(g)', 10: ' + 3O_{2}(g)', 11: ' + 3O_{2}(g)', 12: ' + O_{2}(g)', 13: ' + O_{2}(g)'}
def side(d): return ' + '.join(f'{"" if c == 1 else c}{s}' for s, c in d.items())
def g_hess(rng):
    t = rng.choice(['rxn', 'rxn', 'form', 'comb2', 'combo'])
    if t == 'rxn':
        i = rng.randrange(len(RX)); re_, pr = RX[i]
        dH = sum(c * FH[s] for s, c in pr.items()) - sum(c * FH[s] for s, c in re_.items())
        jitter = rng.choice([0, 0.5, -0.4, 1.1]); fh = {s: round(FH[s] + jitter, 1) for s in list(re_) + list(pr)}
        dH = sum(c * fh[s] for s, c in pr.items()) - sum(c * fh[s] for s, c in re_.items())
        ex = EXTRA[i]
        if ex.startswith(' →'): eq = f'{side(re_)} → 2Fe(s) + {side(pr)}' if i == 4 else ''
        elif ex.startswith(' + 2Al'): eq = f'{side(re_)} + 2Al(s) → 2Fe(s) + {side(pr)}'
        else: eq = f'{side(re_)}{ex} → {side(pr)}'
        given = ', '.join(f'{s}: {m_(v, 5)}' for s, v in fh.items())
        return dict(q=f'Using Δ_{{f}}H° (kJ mol^{{−1}}) — {given} (elements = 0) — the magnitude of ΔH° for {eq} is ____ kJ (nearest integer).', o=None, a=round(abs(dH)),
                    sol=['ΔH° = ΣνΔ_{f}H°(products) − ΣνΔ_{f}H°(reactants); elements in their standard state count 0.', f'ΔH° ≈ {m_(dH, 5)} kJ.'], p=dict(t=t, re=re_, pr=pr, fh=fh))
    if t == 'form':
        f = rng.choice(list(FUEL)); _, _, x, y, z, st, dc = FUEL[f]; dc = dc + rng.choice([0, 3, -2, 1])
        hf = x * -393.5 + y / 2 * -285.8 - dc
        return dict(q=f'Δ_{{c}}H° of {f} ({FUEL[f][0]}) is {m_(dc, 5)} kJ mol^{{−1}}. With Δ_{{f}}H°(CO_{{2}}) = −393.5 and Δ_{{f}}H°(H_{{2}}O, l) = −285.8 kJ mol^{{−1}}, the magnitude of its Δ_{{f}}H° is ____ kJ mol^{{−1}} (nearest integer).', o=None, a=round(abs(hf)),
                    sol=[f'Combustion: → {x}CO_{{2}} + {nf(y / 2)}H_{{2}}O(l).', f'Δ_{{f}}H = {x}(−393.5) + {nf(y / 2)}(−285.8) − ({m_(dc, 5)}) ≈ {m_(hf, 5)} kJ mol^{{−1}}.'], p=dict(t=t, f=f, dc=dc))
    if t == 'comb2':
        f = rng.choice(list(FUEL)); _, _, x, y, z, st, dc = FUEL[f]; hf = round(x * -393.5 + y / 2 * -285.8 - dc + rng.choice([0, 2, -3]), 1); nm = rng.choice([1, 2, 0.5, 3])
        H = nm * (x * -393.5 + y / 2 * -285.8 - hf)
        return dict(q=f'Δ_{{f}}H° of {f} ({FUEL[f][0]}) is {m_(hf, 5)} kJ mol^{{−1}}; Δ_{{f}}H°(CO_{{2}}) = −393.5, Δ_{{f}}H°(H_{{2}}O, l) = −285.8 kJ mol^{{−1}}. The heat released when {nf(nm)} mol of it burns is ____ kJ (nearest integer).', o=None, a=round(-H),
                    sol=[f'Δ_{{c}}H = {x}(−393.5) + {nf(y / 2)}(−285.8) − ({m_(hf, 5)}) per mol.', f'× {nf(nm)} → {m_(H, 5)} kJ → {round(-H)} kJ released.'], p=dict(t=t, f=f, hf=hf, nm=nm))
    a1, a2 = rng.choice([-822, -1648, -571.6, -296.8, -393.5, -110.5, -241.8, -92.3]), rng.choice([-110.5, -285.8, -393.5, -46.1, -184.6, 52.3])
    c1, c2 = rng.choice([1, -1, 2, -2, 0.5]), rng.choice([1, -1, 3, 2, -0.5, 1.5]); H = c1 * a1 + c2 * a2; need(abs(H) > 1)
    q = f'ΔH_{{1}} = {m_(a1, 5)} kJ and ΔH_{{2}} = {m_(a2, 5)} kJ for reactions (1) and (2). A target reaction equals {nf(c1)} × (1) + {nf(c2)} × (2). The magnitude of its ΔH is ____ kJ (nearest integer).'
    return dict(q=q, o=None, a=round(abs(H)), sol=['Hess: add equations → add ΔH with the same multipliers (reversing flips the sign).', f'ΔH = {nf(c1)}({m_(a1, 5)}) + {nf(c2)}({m_(a2, 5)}) ≈ {m_(H, 5)} kJ.'], p=dict(t='combo', a1=a1, a2=a2, c1=c1, c2=c2))

BE = {'H−H': 436, 'C−H': 414, 'C−C': 347, 'C=C': 614, 'C≡C': 839, 'O=O': 498, 'C=O': 741, 'O−H': 464, 'N≡N': 946, 'N−H': 389, 'Cl−Cl': 243, 'H−Cl': 431, 'C−Cl': 330, 'Br−Br': 193, 'H−Br': 366, 'C=O (CO_{2})': 799}
BRX = [('C_{2}H_{4} + H_{2} → C_{2}H_{6}', {'C=C': 1, 'C−H': 4, 'H−H': 1}, {'C−C': 1, 'C−H': 6}), ('C_{2}H_{2} + 2H_{2} → C_{2}H_{6}', {'C≡C': 1, 'C−H': 2, 'H−H': 2}, {'C−C': 1, 'C−H': 6}),
       ('H_{2} + Cl_{2} → 2HCl', {'H−H': 1, 'Cl−Cl': 1}, {'H−Cl': 2}), ('N_{2} + 3H_{2} → 2NH_{3}', {'N≡N': 1, 'H−H': 3}, {'N−H': 6}), ('CH_{4} + Cl_{2} → CH_{3}Cl + HCl', {'C−H': 4, 'Cl−Cl': 1}, {'C−H': 3, 'C−Cl': 1, 'H−Cl': 1}),
       ('2H_{2} + O_{2} → 2H_{2}O(g)', {'H−H': 2, 'O=O': 1}, {'O−H': 4}), ('CH_{4} + 2O_{2} → CO_{2} + 2H_{2}O(g)', {'C−H': 4, 'O=O': 2}, {'C=O (CO_{2})': 2, 'O−H': 4}), ('H_{2} + Br_{2} → 2HBr', {'H−H': 1, 'Br−Br': 1}, {'H−Br': 2}),
       ('C_{2}H_{4} + Cl_{2} → C_{2}H_{4}Cl_{2}', {'C=C': 1, 'C−H': 4, 'Cl−Cl': 1}, {'C−C': 1, 'C−H': 4, 'C−Cl': 2})]
def g_bond(rng):
    t = rng.choice(['be', 'be', 'avg', 'bh', 'bh'])
    if t == 'be':
        nm, br, mk = rng.choice(BRX); used = sorted(set(br) | set(mk)); vals = {b: BE[b] + rng.choice([0, 0, 1, -1, 2, 5, -4]) for b in used}
        H = sum(c * vals[b] for b, c in br.items()) - sum(c * vals[b] for b, c in mk.items())
        return dict(q=f'Using bond enthalpies (kJ mol^{{−1}}) {", ".join(f"{b}: {v}" for b, v in vals.items())}, the magnitude of ΔH for {nm} is ____ kJ (nearest integer).', o=None, a=round(abs(H)),
                    sol=['ΔH = Σ(bonds broken) − Σ(bonds formed).', f'≈ {m_(H, 5)} kJ.'], p=dict(t=t, br=br, mk=mk, vals=vals))
    if t == 'avg':
        mol, nb, atoms = rng.choice([('CH_{4}', 4, {'C': 1, 'H': 4}), ('NH_{3}', 3, {'N': 1, 'H': 3}), ('H_{2}O', 2, {'O': 1, 'H': 2}), ('CCl_{4}', 4, {'C': 1, 'Cl': 4}), ('PCl_{3}', 3, {'P': 1, 'Cl': 3})])
        af = {'C': 716.7, 'H': 218.0, 'N': 472.7, 'O': 249.2, 'Cl': 121.7, 'P': 316.5}; hf = rng.choice([-74.8, -46.1, -241.8, -102.9, -287.0]) + rng.choice([0, 3, -2])
        be = (sum(c * af[a] for a, c in atoms.items()) - hf) / nb; bond = mol[0] + '−' + [a for a in atoms if a != mol[0]][0]
        return dict(q=f'Δ_{{f}}H°({mol}, g) = {m_(hf, 4)} kJ mol^{{−1}}; Δ_{{f}}H° of the gaseous atoms: {", ".join(f"{a}(g) {af[a]}" for a in atoms)} kJ mol^{{−1}}. The average {bond} bond enthalpy is ____ kJ mol^{{−1}} (nearest integer).', o=None, a=round(be),
                    sol=[f'{mol}(g) → atoms: ΔH = Σ Δ_{{f}}H(atoms) − Δ_{{f}}H({mol}).', f'÷ {nb} bonds → ≈ {nf(be, 4)} kJ mol^{{−1}}.'], p=dict(t=t, atoms=atoms, hf=hf, nb=nb))
    salt = rng.choice([('NaCl', 'Na', 'Cl'), ('KCl', 'K', 'Cl'), ('LiF', 'Li', 'F'), ('NaBr', 'Na', 'Br'), ('KBr', 'K', 'Br'), ('MX', 'M', 'X')])
    sub, ie, d, eg, hf = rng.choice([108, 89, 155, 100, 78]), rng.choice([496, 419, 520, 500, 403]), rng.choice([242, 158, 150, 193, 200]), rng.choice([-349, -328, -325, -300, -313]), rng.choice([-411, -437, -594, -361, -400, -394])
    U = sub + ie + d / 2 + eg - hf
    return dict(q=f'For {salt[0]}: sublimation of {salt[1]} = {sub}, ionisation enthalpy = {ie}, dissociation of {salt[2]}_{{2}} = {d}, electron gain enthalpy = {eg}, Δ_{{f}}H°({salt[0]}) = {hf} kJ mol^{{−1}}. The lattice enthalpy (solid → gaseous ions) is ____ kJ mol^{{−1}} (nearest integer).', o=None, a=round(U),
                sol=['Born–Haber: Δ_{f}H = sub + IE + ½D + EG − U_{lattice}.', f'U = {sub} + {ie} + {nf(d / 2)} + ({eg}) − ({hf}) = {nf(U, 5)} kJ mol^{{−1}}.'], p=dict(t='bh', sub=sub, ie=ie, d=d, eg=eg, hf=hf))

S0 = {'N_{2}': 191.6, 'H_{2}': 130.7, 'NH_{3}': 192.5, 'O_{2}': 205.1, 'H_{2}O(l)': 69.9, 'H_{2}O(g)': 188.8, 'CO_{2}': 213.7, 'CO': 197.7, 'CaCO_{3}': 92.9, 'CaO': 39.8, 'N_{2}O_{4}': 304.3, 'NO_{2}': 240.1, 'SO_{2}': 248.2, 'SO_{3}': 256.8, 'Cl_{2}': 223.1, 'HCl': 186.9}
SRX = [('N_{2} + 3H_{2} → 2NH_{3}', {'N_{2}': 1, 'H_{2}': 3}, {'NH_{3}': 2}), ('CaCO_{3} → CaO + CO_{2}', {'CaCO_{3}': 1}, {'CaO': 1, 'CO_{2}': 1}), ('N_{2}O_{4} → 2NO_{2}', {'N_{2}O_{4}': 1}, {'NO_{2}': 2}),
       ('2SO_{2} + O_{2} → 2SO_{3}', {'SO_{2}': 2, 'O_{2}': 1}, {'SO_{3}': 2}), ('2H_{2} + O_{2} → 2H_{2}O(l)', {'H_{2}': 2, 'O_{2}': 1}, {'H_{2}O(l)': 2}), ('H_{2} + Cl_{2} → 2HCl', {'H_{2}': 1, 'Cl_{2}': 1}, {'HCl': 2}),
       ('2CO + O_{2} → 2CO_{2}', {'CO': 2, 'O_{2}': 1}, {'CO_{2}': 2}), ('H_{2}O(l) → H_{2}O(g)', {'H_{2}O(l)': 1}, {'H_{2}O(g)': 1})]
def g_spont(rng):
    t = rng.choice(['teq', 'dg', 'ds', 'sign', 'vap'])
    if t == 'teq':
        H = rng.choice([20, 30, 40, 50, 80, 100, 178, 200, 400]) * rng.choice([1, -1]); S = rng.choice([50, 75, 100, 125, 160, 200, 250]) * (1 if H > 0 else -1)
        T = H * 1000 / S; need(abs(T % 1 - 0.5) > 0.02)
        return dict(q=f'For a reaction ΔH = {m_(H)} kJ mol^{{−1}} and ΔS = {m_(S)} J K^{{−1}} mol^{{−1}}. It is spontaneous {"above" if H > 0 else "below"} ____ K (nearest integer; assume ΔH, ΔS constant).', o=None, a=round(T),
                    sol=['ΔG = ΔH − TΔS changes sign at T = \\f{ΔH}{ΔS}.', f'T = \\f{{{m_(H * 1000)}}}{{{m_(S)}}} ≈ {nf(T, 4)} K.'], p=dict(t=t, H=H, S=S))
    if t == 'dg':
        H = rng.choice([-92, -57, 55, 178, 44, -285, 90, 131]); S = rng.choice([-199, 175, 161, -163, 119, 134, -44, 25]); T = rng.choice([298, 300, 400, 500, 1000])
        G = H - T * S / 1000
        o, a = mcq(rng, f'{m_(G, 4)} kJ mol^{{−1}}', [f'{m_(v, 4)} kJ mol^{{−1}}' for v in (H + T * S / 1000, H - T * S, -G, H - S / 1000)])
        return dict(q=f'ΔH = {m_(H)} kJ mol^{{−1}} and ΔS = {m_(S)} J K^{{−1}} mol^{{−1}}. ΔG at {T} K is about :', o=o, a=a,
                    sol=['ΔG = ΔH − TΔS (watch J vs kJ).', f'= {m_(H)} − {T}({m_(S)} × 10^{{−3}}) ≈ {m_(G, 4)} kJ mol^{{−1}}.'], p=dict(t=t, H=H, S=S, T=T))
    if t == 'ds':
        nm, re_, pr = rng.choice(SRX); vals = {s: round(S0[s] + rng.choice([0, 0.3, -0.5, 1.0]), 1) for s in list(re_) + list(pr)}
        dS = sum(c * vals[s] for s, c in pr.items()) - sum(c * vals[s] for s, c in re_.items())
        return dict(q=f'Standard molar entropies (J K^{{−1}} mol^{{−1}}): {", ".join(f"{s} {v}" for s, v in vals.items())}. The magnitude of ΔS° for {nm} is ____ J K^{{−1}} (nearest integer).', o=None, a=round(abs(dS)),
                    sol=['ΔS° = ΣνS°(products) − ΣνS°(reactants) (elements do NOT have zero entropy).', f'ΔS° ≈ {m_(dS, 4)} J K^{{−1}}.'], p=dict(t=t, re=re_, pr=pr, vals=vals))
    if t == 'sign':
        h, s = rng.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        ans = {(1, 1): 'spontaneous only at high temperature', (1, -1): 'non-spontaneous at all temperatures', (-1, 1): 'spontaneous at all temperatures', (-1, -1): 'spontaneous only at low temperature'}[(h, s)]
        ex = rng.choice(['A reaction', 'A process', 'A change'])
        o, a = mcq(rng, ans, [x for x in ['spontaneous only at high temperature', 'non-spontaneous at all temperatures', 'spontaneous at all temperatures', 'spontaneous only at low temperature'] if x != ans])
        lbl = rng.choice(['', ' (constant p)', ' at 1 bar'])
        return dict(q=f'{ex}{lbl} has ΔH {"> 0" if h > 0 else "< 0"} and ΔS {"> 0" if s > 0 else "< 0"}. It is :', o=o, a=a, sol=['ΔG = ΔH − TΔS.', f'Here: {ans}.'], p=dict(t=t, h=h, s=s))
    liq, H, Tb = rng.choice([('water', 40.7, 373), ('ethanol', 38.6, 351), ('benzene', 30.8, 353), ('CCl_{4}', 30.0, 350), ('acetone', 29.1, 329), ('chloroform', 29.2, 334), ('methanol', 35.3, 338)])
    H = round(H + rng.choice([0, 0.2, -0.3]), 1)
    return dict(q=f'Δ_{{vap}}H of {liq} is {H} kJ mol^{{−1}} at its boiling point {Tb} K. Δ_{{vap}}S is ____ J K^{{−1}} mol^{{−1}} (nearest integer).', o=None, a=round(H * 1000 / Tb),
                sol=['At the boiling point ΔG = 0 → ΔS = \\f{ΔH}{T_{b}}.', f'= \\f{{{H} × 1000}}{{{Tb}}} ≈ {nf(H * 1000 / Tb, 4)}.'], p=dict(t='vap', H=H, Tb=Tb))

def robust(gf):
    def w(rng):
        for _ in range(300):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(law=g_law, hess=g_hess, bond=g_bond, spont=g_spont).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'iso':   # integrate −p dV with p = nRT/V
        w = -integ(lambda V: p['n'] * R * p['T'] / V, p['V1'], p['V2']); return close(num(Rv) * 1000, w, 0.006)
    if t == 'irr': return Rv == round(p['p'] * (p['V2'] - p['V1']))
    if t == 'dhdu':
        _, _, x, y, z, st, _ = FUEL[p['f']]; gas_before = (x + y / 4 - z / 2) + (1 if st == 'g' else 0); return close(num(Rv), p['dU'] + (x - gas_before) * R * p['T'] / 1000, 0.0005)
    if t == 'bomb': return Rv == round(p['C'] * p['dT'] / (p['g'] / p['M']))
    if t == 'heat':
        H = p['n'] * (75.3 * (0 - p['T1']) - 6010 + p['z'] * (p['T2'] - 0)) / 1000; return close(num(Rv), H, 0.003)
    if t == 'adia':
        T2 = (lambda: next(T for T in [p['T1'] - k * 0.001 for k in range(0, 400000)] if p['Cv'] * (p['T1'] - T) >= p['pe'] * (p['f'] - 1) * p['T1'] / p['p1'] - 1e-9))(); return Rv == round(T2)
    if t == 'free':
        facts = {'free expansion of an ideal gas into vacuum': ('w = 0', 'q = 0'), 'reversible isothermal expansion of an ideal gas': ('ΔU = 0',), 'reversible adiabatic expansion of an ideal gas': ('q = 0', 'w < 0'),
                 'isochoric heating of an ideal gas': ('w = 0', 'q > 0'), 'melting of ice at 273 K and 1 atm': ('ΔG = 0',)}
        return all(f in Rv for f in facts[p['pr']])
    if t == 'rxn':
        H = sum(c * p['fh'][s] for s, c in p['pr'].items()) - sum(c * p['fh'][s] for s, c in p['re'].items()); return Rv == round(abs(H))
    if t in ('form', 'comb2'):   # build the cycle: elements → fuel (Δf) ; fuel + O2 → CO2 + H2O (Δc); elements → CO2 + H2O directly
        _, _, x, y, z, st, _ = FUEL[p['f']]; direct = x * -393.5 + (y / 2) * -285.8
        if t == 'form': return Rv == round(abs(direct - p['dc']))
        return Rv == round(-(direct - p['hf']) * p['nm'])
    if t == 'combo': return Rv == round(abs(p['c1'] * p['a1'] + p['c2'] * p['a2']))
    if t == 'be':
        brk = sum(c * p['vals'][b] for b, c in p['br'].items()); mk = sum(c * p['vals'][b] for b, c in p['mk'].items()); return Rv == round(abs(brk - mk))
    if t == 'avg':
        af = {'C': 716.7, 'H': 218.0, 'N': 472.7, 'O': 249.2, 'Cl': 121.7, 'P': 316.5}; return Rv == round((sum(af[a] * c for a, c in p['atoms'].items()) - p['hf']) / p['nb'])
    if t == 'bh': return Rv == round(-(p['hf'] - p['sub'] - p['ie'] - p['d'] / 2 - p['eg']))
    if t == 'teq':   # scan for the sign change of ΔG
        G = lambda T: p['H'] * 1000 - T * p['S']; lo, hi = 1, 100000
        for _ in range(200):
            m = (lo + hi) / 2
            if (G(m) > 0) == (G(lo) > 0): lo = m
            else: hi = m
        return Rv == round(lo)
    if t == 'dg': return close(num(Rv), (p['H'] * 1000 - p['T'] * p['S']) / 1000, 0.003)
    if t == 'ds': return Rv == round(abs(sum(c * p['vals'][s] for s, c in p['pr'].items()) - sum(c * p['vals'][s] for s, c in p['re'].items())))
    if t == 'sign':
        G = lambda T: p['h'] * 50 - T * p['s'] * 0.1; lo, hi = G(50) < 0, G(5000) < 0
        want = {(True, True): 'spontaneous at all temperatures', (False, False): 'non-spontaneous at all temperatures', (False, True): 'spontaneous only at high temperature', (True, False): 'spontaneous only at low temperature'}[(lo, hi)]
        return Rv == want
    if t == 'vap': return Rv == round(p['H'] * 1000 / p['Tb'])
    raise KeyError(t)
