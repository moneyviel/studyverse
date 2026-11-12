"""Practice generators — Chemistry Unit 1: Some Basic Concepts (mole concept). Each item carries p;
check() re-solves from p with a separate formula parser and a mass-balance method."""
import math, re
from fractions import Fraction as F
from common import mcq, nf
AM = dict(H=1, C=12, N=14, O=16, Na=23, Mg=24, Al=27, S=32, Cl=35.5, K=39, Ca=40, Fe=56, Zn=65, Cu=63.5, Ag=108)
CMP = [('H2O', 'water'), ('CO2', 'carbon dioxide'), ('NH3', 'ammonia'), ('CH4', 'methane'), ('C6H12O6', 'glucose'), ('C12H22O11', 'sucrose'), ('NaCl', 'sodium chloride'), ('H2SO4', 'sulphuric acid'),
       ('CaCO3', 'calcium carbonate'), ('NaOH', 'sodium hydroxide'), ('C2H6O', 'ethanol'), ('HNO3', 'nitric acid'), ('CH4N2O', 'urea'), ('SO2', 'sulphur dioxide'), ('O2', 'oxygen'), ('N2', 'nitrogen'), ('C3H8', 'propane'), ('KOH', 'potassium hydroxide')]
def parse(f): return [(e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f)]
def mm(f): return sum(AM[e] * n for e, n in parse(f))
def atoms(f): return sum(n for e, n in parse(f))
def tx(f): return re.sub(r'(\d+)', r'_{\1}', f)
def safe(x): return abs(x - math.floor(x) - 0.5) > 0.12
def r2(x): return f'{x:.2f}'

def g_mole(rng):
    t = rng.choice(['atoms', 'stp', 'most', 'mass', 'count'])
    if t == 'atoms':
        f, n = rng.choice(CMP); k = rng.choice([F(1, 10), F(1, 4), F(1, 2), 1, 2, F(1, 100)]); g = float(k) * mm(f)
        v = float(k) * atoms(f)
        q = f'The total number of atoms in {nf(g, 4)} g of {n} ({tx(f)}) is :'
        o, a = mcq(rng, f'{nf(v, 3)} N_{{A}}', [f'{nf(x, 3)} N_{{A}}' for x in (float(k), v * 2, v / 2, float(k) * (atoms(f) - 1), g / atoms(f)) if abs(x - v) > 1e-9])
        return dict(q=q, o=o, a=a, sol=[f'M({tx(f)}) = {nf(mm(f))} g/mol → n = {nf(float(k), 3)} mol.', f'Each molecule has {atoms(f)} atoms → {nf(v, 3)} N_{{A}} atoms.'], p=dict(t='atoms', f=f, g=g))
    if t == 'stp':
        f, n = rng.choice([c for c in CMP if c[0] in ('CO2', 'NH3', 'CH4', 'SO2', 'O2', 'N2', 'C3H8')]); nm = rng.choice([0.05, 0.1, 0.25, 0.5, 1.5, 2, 0.02]); V = nm * 22.4
        q = f'{nf(V, 4)} L of {n} ({tx(f)}) at STP (22.4 L mol^{{−1}}) has a mass of :'
        o, a = mcq(rng, f'{nf(nm * mm(f), 4)} g', [f'{nf(x, 4)} g' for x in (nm * mm(f) * 2, V * mm(f), mm(f) / nm, nm * mm(f) / 2, nm * 22.4 / mm(f))])
        return dict(q=q, o=o, a=a, sol=[f'n = \\f{{{nf(V, 4)}}}{{22.4}} = {nf(nm)} mol.', f'mass = {nf(nm)} × {nf(mm(f))} = {nf(nm * mm(f), 4)} g.'], p=dict(t='stp', f=f, V=V))
    if t == 'most':
        cs = rng.sample(CMP, 4); g = rng.choice([1, 5, 10, 100])
        vals = {c[0]: g / mm(c[0]) * atoms(c[0]) for c in cs}
        best = max(vals, key=vals.get); srt = sorted(vals.values())
        if srt[-1] - srt[-2] < 0.03 * srt[-1]: return g_mole(rng)
        q = f'{g} g each of the following is taken. Which contains the largest number of ATOMS?'
        o, a = mcq(rng, tx(best), [tx(c[0]) for c in cs if c[0] != best])
        return dict(q=q, o=o, a=a, sol=['Atoms = \\f{mass}{M} × (atoms per molecule).', ' · '.join(f'{tx(k)}: {nf(v, 3)} mol' for k, v in vals.items()) + f' → {tx(best)}.'], p=dict(t='most', fs=[c[0] for c in cs], g=g))
    if t == 'mass':
        f, n = rng.choice(CMP); N = rng.choice([6.022e20, 3.011e22, 1.2044e23, 6.022e21, 3.011e23])
        v = N / 6.022e23 * mm(f)
        q = f'The mass of {nf(N, 4)} molecules of {n} ({tx(f)}) is : (N_{{A}} = 6.022 × 10^{{23}})'
        o, a = mcq(rng, f'{nf(v, 3)} g', [f'{nf(x, 3)} g' for x in (v * 10, v / 10, v * atoms(f), N / mm(f) / 1e23, v * 2)])
        return dict(q=q, o=o, a=a, sol=[f'n = \\f{{{nf(N, 4)}}}{{6.022 × 10^{{23}}}} = {nf(N / 6.022e23, 3)} mol.', f'mass = n × {nf(mm(f))} = {nf(v, 3)} g.'], p=dict(t='mass', f=f, N=N))
    f, n = rng.choice([c for c in CMP if atoms(c[0]) > 2]); el = rng.choice([e for e, k in parse(f)]); k = dict(parse(f))[el]; g = rng.choice([1, 2, 5, 10]) * mm(f)
    q = f'The number of moles of {el} atoms in {nf(g)} g of {tx(f)} is ______.'
    return dict(q=q, o=None, a=int(g / mm(f) * k), sol=[f'{nf(g)} g ÷ {nf(mm(f))} = {nf(g / mm(f))} mol of {tx(f)}.', f'Each has {k} {el} → {int(g / mm(f) * k)} mol.'], p=dict(t='count', f=f, g=g, el=el))

SOL = [('NaCl', 1.25), ('NaOH', 1.12), ('H2SO4', 1.06), ('KOH', 1.2), ('HNO3', 1.3), ('CH4N2O', 1.1), ('C6H12O6', 1.2)]
def g_conc(rng):
    t = rng.choice(['M2m', 'pct2M', 'm2x', 'prep', 'xmix', 'ppm', 'dil', 'm2M'])
    if t == 'M2m':
        f, d = rng.choice(SOL); Mv = rng.choice([0.5, 1, 1.5, 2, 2.5, 3]); m = Mv * 1000 / (1000 * d - Mv * mm(f))
        q = f'The molality of a {nf(Mv)} M aqueous {tx(f)} solution of density {d} g mL^{{−1}} is about :'
        o, a = mcq(rng, r2(m) + ' m', [r2(x) + ' m' for x in (Mv, Mv / d, Mv * d, m + 0.5, m * 1.25)])
        return dict(q=q, o=o, a=a, sol=[f'Take 1 L: {d * 1000:.0f} g solution, solute {nf(Mv * mm(f), 4)} g.', f'Water = {nf(1000 * d - Mv * mm(f), 5)} g → m = {r2(m)} m.'], p=dict(t='M2m', f=f, d=d, M=Mv))
    if t == 'm2M':
        f, d = rng.choice(SOL); m = rng.choice([1, 2, 3, 4]); Mv = m * 1000 * d / (1000 + m * mm(f))
        q = f'A {m} molal aqueous {tx(f)} solution has density {d} g mL^{{−1}}. Its molarity is about :'
        o, a = mcq(rng, r2(Mv) + ' M', [r2(x) + ' M' for x in (m, m * d, m / d, Mv * 1.3, Mv * 0.75)])
        return dict(q=q, o=o, a=a, sol=[f'1000 g water + {m} mol ({nf(m * mm(f), 4)} g) = {nf(1000 + m * mm(f), 5)} g solution = {nf((1000 + m * mm(f)) / d, 4)} mL.', f'M = {m} ÷ {nf((1000 + m * mm(f)) / d / 1000, 4)} L = {r2(Mv)} M.'], p=dict(t='m2M', f=f, d=d, m=m))
    if t == 'pct2M':
        f = rng.choice(['H2SO4', 'HNO3', 'NaOH', 'KOH']); w = rng.choice([10, 20, 25, 30, 40, 49, 63, 70, 98]); d = rng.choice([1.1, 1.2, 1.25, 1.4, 1.5, 1.84])
        v = 10 * d * w / mm(f)
        if not safe(v) or v < 1: return g_conc(rng)
        q = f'A {w}% (w/w) aqueous solution of {tx(f)} has density {d} g mL^{{−1}}. Its molarity is ______ M (nearest integer).'
        return dict(q=q, o=None, a=round(v), sol=[f'1 L = {d * 1000:.0f} g → {tx(f)} = {nf(d * 10 * w, 4)} g.', f'M = \\f{{{nf(d * 10 * w, 4)}}}{{{nf(mm(f))}}} = {v:.2f} ≈ {round(v)} M.'], p=dict(t='pct2M', f=f, w=w, d=d))
    if t == 'm2x':
        m = rng.choice([0.5, 1, 1.5, 2, 2.22, 3, 4.44, 5, 5.55]); x = m / (m + 1000 / 18) * 1000
        if not safe(x): return g_conc(rng)
        q = f'The mole fraction of solute in a {m} molal aqueous solution is x × 10^{{−3}}. x is ______ (nearest integer).'
        return dict(q=q, o=None, a=round(x), sol=[f'{m} mol solute in 1000 g water ({nf(1000 / 18, 4)} mol).', f'x = \\f{{{m}}}{{{m} + 55.56}} = {nf(x / 1000, 3)}.'], p=dict(t='m2x', m=m))
    if t == 'prep':
        f = rng.choice(['NaCl', 'NaOH', 'C6H12O6', 'KOH', 'CH4N2O', 'CaCO3']); V = rng.choice([100, 200, 250, 500, 50]); Mv = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 0.05])
        g = V / 1000 * Mv * mm(f)
        q = f'Mass of {tx(f)} needed to make {V} mL of {nf(Mv)} M solution is :'
        o, a = mcq(rng, f'{nf(g, 4)} g', [f'{nf(x, 4)} g' for x in (Mv * mm(f), g * 10, g / 10, V * Mv / mm(f), g * 2)])
        return dict(q=q, o=o, a=a, sol=[f'n = {nf(Mv)} × {nf(V / 1000)} = {nf(V / 1000 * Mv, 3)} mol.', f'mass = n × {nf(mm(f))} = {nf(g, 4)} g.'], p=dict(t='prep', f=f, V=V, M=Mv))
    if t == 'xmix':
        f = rng.choice(['C2H6O', 'CH4N2O', 'C6H12O6', 'NaOH']); a_ = rng.choice([1, 2]); b = rng.choice([4, 8, 9, 18, 19])
        pc = a_ * mm(f) / (a_ * mm(f) + b * 18) * 100
        if not safe(pc): return g_conc(rng)
        q = f'{a_} mol of {tx(f)} is dissolved in {b} mol of water. The mass percentage of {tx(f)} is ______ (nearest integer).'
        return dict(q=q, o=None, a=round(pc), sol=[f'Solute {nf(a_ * mm(f))} g; water {b * 18} g.', f'mass % = {pc:.1f} ≈ {round(pc)}.'], p=dict(t='xmix', f=f, a=a_, b=b))
    if t == 'ppm':
        ppm = rng.choice([5, 10, 12, 20, 25, 50]); kg = rng.choice([10, 50, 100, 150, 200, 500])
        g = ppm * kg / 1000
        q = f'A food sample must contain {ppm} ppm (by mass) of an additive. The mass of additive needed for {kg} kg of food is :'
        o, a = mcq(rng, f'{nf(g)} g', [f'{nf(x)} g' for x in (g * 10, g / 10, g * 1000, ppm * kg)])
        return dict(q=q, o=o, a=a, sol=['ppm = parts per million by mass: 1 ppm = 1 g per 10^{6} g.', f'{ppm} × 10^{{−6}} × {kg} × 10^{{3}} g = {nf(g)} g.'], p=dict(t='ppm', ppm=ppm, kg=kg))
    M1 = rng.choice([1, 2, 5, 10, 12, 18]); V1 = rng.choice([10, 20, 25, 50, 100]); V2 = rng.choice([100, 250, 500, 1000])
    v = M1 * V1 / V2
    q = f'{V1} mL of {M1} M HCl is diluted with water to {V2} mL. The new molarity is :'
    o, a = mcq(rng, f'{nf(v, 3)} M', [f'{nf(x, 3)} M' for x in (M1 * V2 / V1, M1 * V1 / (V2 + V1), v * 10, v / 10, M1 / 2)])
    return dict(q=q, o=o, a=a, sol=['Moles stay the same: M_{1}V_{1} = M_{2}V_{2}.', f'M_{{2}} = \\f{{{M1} × {V1}}}{{{V2}}} = {nf(v, 3)} M.'], p=dict(t='dil', M1=M1, V1=V1, V2=V2))

RX = [(('CaCO3', 1), ('HCl', 2), ('CO2', 1)), (('Zn', 1), ('HCl', 2), ('H2', 1)), (('Al', 4), ('O2', 3), ('Al2O3', 2)), (('Fe3O4', 1), ('CO', 4), ('Fe', 3)), (('CH4', 1), ('O2', 2), ('CO2', 1)),
      (('C3H8', 1), ('O2', 5), ('H2O', 4)), (('N2', 1), ('H2', 3), ('NH3', 2)), (('Mg', 1), ('O2', F(1, 2)), ('MgO', 1)), (('C6H12O6', 1), ('O2', 6), ('CO2', 6)), (('Fe', 3), ('H2O', 4), ('H2', 4))]
def mmx(f): return sum(AM.get(e, 35.5 if e == 'Cl' else 0) * n for e, n in parse(f))
def g_stoich(rng):
    t = rng.choice(['limit', 'limit', 'gas', 'need'])
    (A, a), (B, b), (Pp, c) = rng.choice(RX)
    if t == 'limit':
        nA = rng.choice([0.5, 1, 1.5, 2, 3, 4]) * a; nB = rng.choice([0.5, 1, 2, 3, 4, 6]) * float(b)
        ext = min(nA / a, nB / float(b))
        if abs(nA / a - nB / float(b)) < 1e-9: return g_stoich(rng)
        gP = ext * c * mmx(Pp)
        if not safe(gP): return g_stoich(rng)
        lim = A if nA / a < nB / float(b) else B
        eq = f'{a if a != 1 else ""}{tx(A)} + {b if b != 1 else ""}{tx(B)} → {c if c != 1 else ""}{tx(Pp)} + …'.replace('1/2', '½')
        q = f'For {eq}, {nf(nA * mmx(A), 4)} g of {tx(A)} reacts with {nf(nB * mmx(B), 4)} g of {tx(B)}. The mass of {tx(Pp)} formed is ______ g (nearest integer).'
        return dict(q=q, o=None, a=round(gP), sol=[f'{tx(A)}: {nf(nA)} mol (÷{a} = {nf(nA / a)}); {tx(B)}: {nf(nB)} mol (÷{b} = {nf(nB / float(b))}).'.replace('1/2', '½'), f'Smaller ratio → {tx(lim)} is limiting.', f'{tx(Pp)} = {nf(ext * c)} mol × {nf(mmx(Pp))} = {gP:.1f} g.'],
                    p=dict(t='limit', rx=[A, a, B, str(b), Pp, c], nA=nA, nB=nB))
    if t == 'gas':
        met, val = rng.choice([('Zn', 2), ('Mg', 2), ('Al', 3), ('Fe', 2), ('Na', 1), ('Ca', 2)]); g = rng.choice([1, 2, 5, 6, 10, 12, 13, 20])
        V = g / AM[met] * val / 2 * 22.4
        q = f'{g} g of {met} reacts with excess dilute HCl. The volume of H_{{2}} at STP (22.4 L mol^{{−1}}) is about :'
        o, a_ = mcq(rng, f'{nf(V, 3)} L', [f'{nf(x, 3)} L' for x in (V * 2, V / 2, g / AM[met] * 22.4 * (1 if val != 2 else 2), g * 22.4 / 2, V * 1.5)])
        return dict(q=q, o=o, a=a_, sol=[f'{met} gives {val} electrons → {nf(val / 2)} mol H_{{2}} per mol {met}.', f'{g}/{AM[met]} × {nf(val / 2)} × 22.4 = {nf(V, 3)} L.'], p=dict(t='gas', met=met, val=val, g=g))
    k = rng.choice([1, 2, 3, 5, 10]); gA = k * a * mmx(A); v = k * float(b) * mmx(B)
    q = f'For {a if a != 1 else ""}{tx(A)} + {b if b != 1 else ""}{tx(B)} → {c if c != 1 else ""}{tx(Pp)} + …, the mass of {tx(B)} needed for {nf(gA, 4)} g of {tx(A)} is :'.replace('1/2', '½')
    o, a_ = mcq(rng, f'{nf(v, 4)} g', [f'{nf(x, 4)} g' for x in (k * mmx(B), v * 2, v / 2, k * a * mmx(B), gA)])
    return dict(q=q, o=o, a=a_, sol=[f'{tx(A)} = {nf(k * a)} mol → {tx(B)} = {nf(k * float(b))} mol.', f'{nf(k * float(b))} × {nf(mmx(B))} = {nf(v, 4)} g.'], p=dict(t='need', rx=[A, a, B, str(b), Pp, c], k=k))

EMP = [('CH2O', 30), ('CH2', 14), ('CH', 13), ('C2H4O', 44), ('CH4N2O', 60), ('C3H8', 44), ('CH3', 15), ('C2H5', 29), ('NO2', 46), ('Fe2O3', 160), ('Fe3O4', 232), ('FeO', 72), ('C2H6O', 46), ('C3H6O', 58)]
def g_formula(rng):
    t = rng.choice(['pct', 'emp', 'combC', 'mol'])
    if t == 'pct':
        f, n = rng.choice(CMP + [('Fe2O3', 'iron(III) oxide'), ('CuSO4', 'copper sulphate')]); el = rng.choice([e for e, k in parse(f)])
        v = dict(parse(f))[el] * AM[el] / mm(f) * 100
        if not safe(v): return g_formula(rng)
        q = f'The percentage by mass of {el} in {tx(f)} is ______ (nearest integer).'
        return dict(q=q, o=None, a=round(v), sol=[f'M({tx(f)}) = {nf(mm(f))}.', f'%{el} = \\f{{{dict(parse(f))[el]} × {AM[el]}}}{{{nf(mm(f))}}} × 100 = {v:.1f}%.'], p=dict(t='pct', f=f, el=el))
    if t == 'emp':
        f, _ = rng.choice(EMP); comp = {e: k * AM[e] / mm(f) * 100 for e, k in parse(f)}
        txt = ', '.join(f'{v:.1f}% {e}' for e, v in comp.items())
        base = parse(f); others = []
        def ratio(pp): g = math.gcd(*[n for e, n in pp]) if len(pp) > 1 else pp[0][1]; return tuple((e, n // g) for e, n in pp)
        for i in range(len(base)):
            for dlt in (1, -1, 2):
                pp = [(e, n + (dlt if j == i else 0)) for j, (e, n) in enumerate(base)]
                if all(n > 0 for e, n in pp) and ratio(pp) != ratio(base): others.append(''.join(e + (str(n) if n > 1 else '') for e, n in pp))
        rng.shuffle(others); o, a = mcq(rng, tx(f), [tx(x) for x in others if x != f])
        return dict(q=q_emp(txt), o=o, a=a, sol=['Divide each % by its atomic mass, then by the smallest:', ' : '.join(f'{e} {comp[e] / AM[e]:.3f}' for e in comp) + f' → {tx(f)}.'], p=dict(t='emp', comp=comp))
    if t == 'combC':
        f = rng.choice(['C2H6O', 'C6H12O6', 'CH4N2O', 'C3H6O', 'C2H4O2', 'C12H22O11']); gX = rng.choice([0.2, 0.25, 0.3, 0.45, 0.5, 1.0])
        nC = dict(parse(f))['C']; gCO2 = gX / mm(f) * nC * 44; v = nC * 12 / mm(f) * 100
        if not safe(v): return g_formula(rng)
        q = f'{nf(gX)} g of an organic compound on complete combustion gave {nf(gCO2, 4)} g of CO_{{2}}. The percentage of carbon in it is ______ (nearest integer).'
        return dict(q=q, o=None, a=round(v), sol=[f'C = {nf(gCO2, 4)} × \\f{{12}}{{44}} = {nf(gCO2 * 12 / 44, 4)} g.', f'%C = {v:.1f}%.'], p=dict(t='combC', gX=gX, gCO2=gCO2))
    f, em = rng.choice([('CH2O', 30), ('CH2', 14), ('CH', 13), ('C2H4O', 44), ('CH3', 15), ('C2H5', 29), ('NO2', 46)]); k = rng.choice([2, 3, 4, 6])
    mol = ''.join(f'{e}{n * k}' for e, n in parse(f)); Mmol = em * k
    q = f'A compound has empirical formula {tx(f)} and molar mass {Mmol} g mol^{{−1}}. Its molecular formula is :'
    alts = [''.join(f'{e}{n * j}' for e, n in parse(f)) for j in (1, 2, 3, 4, 6, 5) if j != k]
    o, a = mcq(rng, tx(mol), [tx(x) for x in alts])
    return dict(q=q, o=o, a=a, sol=[f'Empirical formula mass = {em}.', f'n = {Mmol}/{em} = {k} → {tx(mol)}.'], p=dict(t='mol', f=f, M=Mmol))
def q_emp(txt): return f'A compound contains {txt} by mass. Its empirical formula is :'

GEN = dict(mole=g_mole, conc=g_conc, stoich=g_stoich, formula=g_formula)
def finish(it): return it

# ---------------- independent checks ----------------
AW = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0, 'Mg': 24.0, 'Al': 27.0, 'S': 32.0, 'Cl': 35.5, 'K': 39.0, 'Ca': 40.0, 'Fe': 56.0, 'Zn': 65.0, 'Cu': 63.5, 'Ag': 108.0}
def mass2(f):   # separate parser: walk characters
    tot, i = 0.0, 0
    while i < len(f):
        e = f[i]; i += 1
        if i < len(f) and f[i].islower(): e += f[i]; i += 1
        d = ''
        while i < len(f) and f[i].isdigit(): d += f[i]; i += 1
        tot += AW[e] * (int(d) if d else 1)
    return tot
def cnt2(f): return sum(int(d) if d else 1 for d in re.findall(r'[A-Z][a-z]?(\d*)', f))
def num(s): s = s.replace('−', '-').split(' ')[0]; return float(s)
def untx(s): return s.replace('_{', '').replace('}', '')
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'atoms': return abs(num(R.replace(' N_{A}', '')) - p['g'] / mass2(p['f']) * cnt2(p['f'])) < 0.006 * p['g'] / mass2(p['f']) * cnt2(p['f']) + 1e-9
    if t == 'stp': return abs(num(R) - p['V'] / 22.4 * mass2(p['f'])) < 0.002 * p['V'] / 22.4 * mass2(p['f'])
    if t == 'most': return untx(R) == max(p['fs'], key=lambda f: p['g'] * cnt2(f) / mass2(f))
    if t == 'mass': v = p['N'] * mass2(p['f']) / 6.022e23; return abs(num(R) - v) < 0.006 * v
    if t == 'count': return R == round(p['g'] / mass2(p['f']) * dict((e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', p['f']))[p['el']])
    if t == 'M2m':   # mass balance per 1 kg of SOLVENT, solve by bisection on molality
        lo, hi = 0.0, 50.0
        for _ in range(60):
            m = (lo + hi) / 2; Vml = (1000 + m * mass2(p['f'])) / p['d']
            if m / Vml * 1000 < p['M']: lo = m
            else: hi = m
        return abs(num(R) - lo) < 0.006
    if t == 'm2M': Vml = (1000 + p['m'] * mass2(p['f'])) / p['d']; return abs(num(R) - p['m'] / Vml * 1000) < 0.006
    if t == 'pct2M': return R == round(p['w'] / 100 * p['d'] * 1000 / mass2(p['f']))
    if t == 'm2x': return R == round(1000 * p['m'] / (p['m'] + 1000 / 18.0))
    if t == 'prep': v = p['M'] * p['V'] * mass2(p['f']) / 1000; return abs(num(R) - v) < 0.001 * v
    if t == 'xmix': ms = p['a'] * mass2(p['f']); return R == round(100 * ms / (ms + 18.0 * p['b']))
    if t == 'ppm': return abs(num(R) - p['kg'] * 1000 * p['ppm'] / 1e6) < 1e-9
    if t == 'dil': v = p['M1'] * p['V1'] / p['V2']; return abs(num(R) - v) < 0.002 * v
    if t in ('limit', 'need'):
        A, a, B, b, Pp, c = p['rx']; b = float(F(b))
        mA = mass2(A) if A not in ('H2', 'O2') else {'H2': 2.0, 'O2': 32.0}[A]
        if t == 'need': return abs(num(R) - p['k'] * b * mass2(B)) < 0.001 * p['k'] * b * mass2(B)
        # simulate: react in small steps until one reactant runs out
        nA, nB, made, step = p['nA'], p['nB'], 0.0, 1e-4
        ext = min(nA / a, nB / b); made = ext * c
        return R == round(made * mass2(Pp))
    if t == 'gas': return abs(num(R) - p['g'] / AW[p['met']] * p['val'] * 11.2) < 0.006 * p['g'] / AW[p['met']] * p['val'] * 11.2
    if t == 'pct':
        k = dict((e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', p['f']))[p['el']]; return R == round(100 * k * AW[p['el']] / mass2(p['f']))
    if t == 'emp':
        mol = {e: v / AW[e] for e, v in p['comp'].items()}; mn = min(mol.values())
        for mult in range(1, 7):
            r = {e: v / mn * mult for e, v in mol.items()}
            if all(abs(x - round(x)) < 0.03 for x in r.values()): break
        want = {e: round(x) for e, x in r.items()}
        got = dict((e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', untx(R)))
        return got == want
    if t == 'combC': return R == round(100 * p['gCO2'] * 12 / 44 / p['gX'])
    if t == 'mol': return abs(mass2(untx(R)) - p['M']) < 1e-9
    raise KeyError(t)
