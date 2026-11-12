"""Practice generators — Chemistry Unit 7: Redox Reactions & Electrochemistry. check() re-solves each item independently:
oxidation numbers by solving the charge balance of the formula, cells via ΔG° bookkeeping and the Nernst equation,
conductance through unit-by-unit SI conversion, electrolysis by counting electrons."""
import math, re
from common import mcq, nf
F_ = 96500
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').replace('+', '').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def sg(x): return ('+' if x > 0 else '') + nf(x, 3).replace('-', '−')
def nmv(x): return nf(x, 3).replace('-', '−')

# compound, element, other atoms {sym: count}, charge — ON of element solved from fixed ONs of the rest
FIX = {'H': 1, 'O': -2, 'F': -1, 'Cl': -1, 'K': 1, 'Na': 1, 'Ba': 2, 'Ca': 2, 'Br': -1, 'N_am': 0}
CMP = [('KMnO_{4}', 'Mn', 1, {'K': 1, 'O': 4}, 0), ('K_{2}MnO_{4}', 'Mn', 1, {'K': 2, 'O': 4}, 0), ('MnO_{2}', 'Mn', 1, {'O': 2}, 0), ('Mn_{2}O_{7}', 'Mn', 2, {'O': 7}, 0),
       ('K_{2}Cr_{2}O_{7}', 'Cr', 2, {'K': 2, 'O': 7}, 0), ('CrO_{4}^{2−}', 'Cr', 1, {'O': 4}, -2), ('Cr_{2}O_{3}', 'Cr', 2, {'O': 3}, 0), ('H_{2}SO_{4}', 'S', 1, {'H': 2, 'O': 4}, 0),
       ('H_{2}SO_{3}', 'S', 1, {'H': 2, 'O': 3}, 0), ('SO_{2}', 'S', 1, {'O': 2}, 0), ('SF_{6}', 'S', 1, {'F': 6}, 0), ('SF_{4}', 'S', 1, {'F': 4}, 0), ('H_{2}S', 'S', 1, {'H': 2}, 0),
       ('Na_{2}S_{2}O_{3}', 'S', 2, {'Na': 2, 'O': 3}, 0), ('S_{4}O_{6}^{2−}', 'S', 4, {'O': 6}, -2), ('HNO_{3}', 'N', 1, {'H': 1, 'O': 3}, 0), ('NO_{2}', 'N', 1, {'O': 2}, 0),
       ('N_{2}O', 'N', 2, {'O': 1}, 0), ('NH_{3}', 'N', 1, {'H': 3}, 0), ('HNO_{2}', 'N', 1, {'H': 1, 'O': 2}, 0), ('N_{2}H_{4}', 'N', 2, {'H': 4}, 0), ('NH_{2}OH', 'N', 1, {'H': 3, 'O': 1}, 0),
       ('HClO_{4}', 'Cl', 1, {'H': 1, 'O': 4}, 0), ('ClO_{3}^{−}', 'Cl', 1, {'O': 3}, -1), ('ClO_{2}', 'Cl', 1, {'O': 2}, 0), ('HOCl', 'Cl', 1, {'H': 1, 'O': 1}, 0), ('Cl_{2}O_{7}', 'Cl', 2, {'O': 7}, 0),
       ('H_{3}PO_{4}', 'P', 1, {'H': 3, 'O': 4}, 0), ('H_{3}PO_{3}', 'P', 1, {'H': 3, 'O': 3}, 0), ('H_{3}PO_{2}', 'P', 1, {'H': 3, 'O': 2}, 0), ('PH_{3}', 'P', 1, {'H': 3}, 0), ('P_{4}O_{10}', 'P', 4, {'O': 10}, 0),
       ('Fe_{3}O_{4}', 'Fe', 3, {'O': 4}, 0), ('Fe_{2}O_{3}', 'Fe', 2, {'O': 3}, 0), ('FeO_{4}^{2−}', 'Fe', 1, {'O': 4}, -2), ('VO_{2}^{+}', 'V', 1, {'O': 2}, 1), ('VO^{2+}', 'V', 1, {'O': 1}, 2),
       ('OF_{2}', 'O', 1, {'F': 2}, 0), ('H_{2}O_{2}', 'O', 2, {'H': 2}, 0), ('KO_{2}', 'O', 2, {'K': 1}, 0), ('BaO_{2}', 'O', 2, {'Ba': 1}, 0), ('NaH', 'H', 1, {'Na': 1}, 0), ('CaH_{2}', 'H', 2, {'Ca': 1}, 0),
       ('CO_{2}', 'C', 1, {'O': 2}, 0), ('CH_{4}', 'C', 1, {'H': 4}, 0), ('HCHO', 'C', 1, {'H': 2, 'O': 1}, 0), ('H_{2}C_{2}O_{4}', 'C', 2, {'H': 2, 'O': 4}, 0), ('CH_{3}OH', 'C', 1, {'H': 4, 'O': 1}, 0),
       ('XeF_{6}', 'Xe', 1, {'F': 6}, 0), ('XeO_{3}', 'Xe', 1, {'O': 3}, 0), ('PbO_{2}', 'Pb', 1, {'O': 2}, 0), ('Pb_{3}O_{4}', 'Pb', 3, {'O': 4}, 0), ('SnCl_{4}', 'Sn', 1, {'Cl': 4}, 0)]
def on_of(c):   # solve n·x + Σ fixed = charge
    name, el, n, rest, ch = c
    fx = dict(FIX)
    if name in ('NaH', 'CaH_{2}'): pass
    return (ch - sum(fx[k] * v for k, v in rest.items())) / n
def show_on(x): return ('+' if x > 0 else '') + (str(int(x)) if x == int(x) else nf(x, 3)).replace('-', '−') if x != 0 else '0'
DISP_Y = ['H_{2}O_{2}', 'Cl_{2}', 'Br_{2}', 'I_{2}', 'ClO^{−}', 'ClO_{2}^{−}', 'ClO_{3}^{−}', 'NO_{2}', 'HNO_{2}', 'P_{4}', 'S_{8}', 'Cu^{+}', 'MnO_{4}^{2−}', 'Hg_{2}^{2+}']
DISP_N = ['F_{2}', 'ClO_{4}^{−}', 'MnO_{4}^{−}', 'K^{+}', 'Ag', 'Na', 'Cr_{2}O_{7}^{2−}', 'F^{−}', 'SO_{4}^{2−}', 'NH_{4}^{+}', 'Zn^{2+}']
OXI = {'KMnO_{4} (acidic)': 5, 'KMnO_{4} (neutral)': 3, 'KMnO_{4} (strongly basic)': 1, 'K_{2}Cr_{2}O_{7} (acidic)': 6}
RED = {'Fe^{2+}': 1, 'C_{2}O_{4}^{2−}': 2, 'H_{2}O_{2}': 2, 'Sn^{2+}': 2, 'I^{−}': 1, 'SO_{3}^{2−}': 2, 'NO_{2}^{−}': 2, 'S^{2−} (to S)': 2}

def g_ox(rng):
    t = rng.choice(['on', 'count', 'count', 'disp', 'eq', 'eq'])
    if t == 'on':
        c = rng.choice(CMP); x = on_of(c)
        alts = [show_on(v) for v in (-x, x + 1, x - 1, x + 2, x * 2 if x else 3, x / 2 if x else -1) if show_on(v) != show_on(x)]
        o, a = mcq(rng, show_on(x), alts)
        return dict(q=f'The oxidation number of {c[1]} in {c[0]} is :', o=o, a=a, sol=['Fixed values: H +1 (−1 in metal hydrides), O −2 (−1 in peroxides, −½ in superoxides), F −1, alkali +1.', f'Solve the charge balance: {c[1]} = {show_on(x)}.'], p=dict(t=t, c=c[0]))
    if t == 'count':
        pool = rng.sample(CMP, 6); k = rng.choice(sorted({on_of(c) for c in pool if on_of(c) == int(on_of(c))})); n = sum(1 for c in pool if on_of(c) == k)
        q = f'Count the species in which the main element (not H, O, F, alkali/alkaline-earth metal) has oxidation state {show_on(k)}: {", ".join(c[0] for c in pool)}.'
        return dict(q=q, o=None, a=n, sol=['Work out each one from the charge balance.', '; '.join(f'{c[0]}: {show_on(on_of(c))}' for c in pool) + f' → {n}.'], p=dict(t=t, cs=[c[0] for c in pool], k=k))
    if t == 'disp':
        m = rng.randint(2, 5); ys = rng.sample(DISP_Y, m); ns = rng.sample(DISP_N, rng.randint(2, 5)); allsp = ys + ns; rng.shuffle(allsp)
        return dict(q=f'How many of the following can undergo disproportionation: {", ".join(allsp)} ?', o=None, a=m,
                    sol=['A species can disproportionate only if its element sits in an INTERMEDIATE oxidation state (it can go both up and down).', f'Yes: {", ".join(x for x in allsp if x in ys)} → {m}.'], p=dict(t=t, sp=allsp))
    ox = rng.choice(list(OXI)); rd = rng.choice(list(RED)); nr = rng.choice([1, 2, 3, 5, 6, 10, 0.5, 1.5, 2.5])
    mo = nr * RED[rd] / OXI[ox]; need(abs(mo * 1000 - round(mo * 1000)) < 1e-6 or True)
    q = f'Moles of {ox.split(" ")[0]} needed to oxidise {nf(nr)} mol of {rd.split(" ")[0]} with {ox.split("(")[1][:-1]} conditions are :'
    o, a = mcq(rng, nf(mo, 3), [nf(v, 3) for v in (nr * OXI[ox] / RED[rd], nr / OXI[ox], nr * RED[rd], mo * 2, mo / 2)])
    return dict(q=q, o=o, a=a, sol=[f'Electrons: {ox} takes {OXI[ox]} per formula unit; {rd} gives {RED[rd]} each.', f'n = \\f{{{nf(nr)} × {RED[rd]}}}{{{OXI[ox]}}} = {nf(mo, 3)} mol.'], p=dict(t='eq', ox=ox, rd=rd, nr=nr))

COUP = {'Li^{+}/Li': (-3.05, 1), 'K^{+}/K': (-2.93, 1), 'Mg^{2+}/Mg': (-2.37, 2), 'Al^{3+}/Al': (-1.66, 3), 'Zn^{2+}/Zn': (-0.76, 2), 'Fe^{2+}/Fe': (-0.44, 2), 'Ni^{2+}/Ni': (-0.25, 2),
        'Sn^{2+}/Sn': (-0.14, 2), 'Pb^{2+}/Pb': (-0.13, 2), 'Cu^{2+}/Cu': (0.34, 2), 'Ag^{+}/Ag': (0.80, 1), 'Au^{3+}/Au': (1.40, 3), 'Cd^{2+}/Cd': (-0.40, 2), 'Cr^{3+}/Cr': (-0.74, 3)}
def g_ecell(rng):
    t = rng.choice(['e0', 'nernst', 'nernst', 'dg', 'logk', 'comb', 'hph', 'ksp', 'conc'])
    if t in ('e0', 'dg', 'logk', 'nernst'):
        a_, b_ = rng.sample(list(COUP), 2); (Ea, na), (Eb, nb) = COUP[a_], COUP[b_]
        if Ea > Eb: a_, b_, Ea, Eb, na, nb = b_, a_, Eb, Ea, nb, na   # a = anode
        E = Eb - Ea; n = na * nb // math.gcd(na, nb)
        an, ca = a_.split('/')[1], b_.split('/')[1]
        cell = f'{an} | {a_.split("/")[0]} || {b_.split("/")[0]} | {ca}'
        if t == 'e0':
            o, a = mcq(rng, f'{nf(E, 3)} V', [f'{nmv(v)} V' for v in (Ea + Eb, -E, Eb + abs(Ea) * 2 if Ea < 0 else E / 2, E * n)])
            return dict(q=f'E°({a_}) = {sg(Ea)} V and E°({b_}) = {sg(Eb)} V. E° of the cell {cell} is :', o=o, a=a, sol=['E°_{cell} = E°_{cathode} − E°_{anode} (both as reduction potentials).', f'= {sg(Eb)} − ({sg(Ea)}) = {nf(E, 3)} V.'], p=dict(t=t, Ea=Ea, Eb=Eb))
        if t == 'dg':
            G = -n * F_ * E / 1000
            o, a = mcq(rng, f'{nmv(G)} kJ', [f'{nmv(v)} kJ' for v in (-G, -F_ * E / 1000, G * 2, -n * F_ * (Ea + Eb) / 1000)])
            return dict(q=f'For the cell {cell} (E°({a_}) = {sg(Ea)} V, E°({b_}) = {sg(Eb)} V), ΔG° for the balanced cell reaction (F = 96500 C mol^{{−1}}) is about :', o=o, a=a,
                        sol=[f'E° = {nf(E, 3)} V; electrons transferred n = {n}.', f'ΔG° = −nFE° = −{n} × 96500 × {nf(E, 3)} ≈ {nmv(G)} kJ.'], p=dict(t=t, Ea=Ea, Eb=Eb, na=na, nb=nb))
        if t == 'logk':
            need(E < 1.3); L = n * E / 0.059
            return dict(q=f'For the cell {cell}, E°({a_}) = {sg(Ea)} V and E°({b_}) = {sg(Eb)} V. If K = 10^{{x}} for the balanced cell reaction at 298 K, x is ____ (nearest integer; \\f{{2.303RT}}{{F}} = 0.059 V).', o=None, a=round(L),
                        sol=['log K = \\f{nE°}{0.059}.', f'n = {n}, E° = {nf(E, 3)} V → log K ≈ {nf(L, 4)}.'], p=dict(t=t, Ea=Ea, Eb=Eb, na=na, nb=nb))
        c1, c2 = rng.choice([0.001, 0.01, 0.1, 0.5, 1, 2, 0.05, 0.2]), rng.choice([0.001, 0.01, 0.1, 0.5, 1, 2, 0.05, 0.2]); need(c1 != c2)
        need(na == nb); Ec = E - 0.059 / na * math.log10(c1 / c2)
        o, a = mcq(rng, f'{nf(Ec, 3)} V', [f'{nmv(v)} V' for v in (E, E + 0.059 / na * math.log10(c1 / c2), E - 0.059 * math.log10(c1 / c2), Ec + 0.1)])
        return dict(q=f'E°({a_}) = {sg(Ea)} V, E°({b_}) = {sg(Eb)} V. The emf of {an} | {a_.split("/")[0]} ({c1} M) || {b_.split("/")[0]} ({c2} M) | {ca} at 298 K is about :', o=o, a=a,
                    sol=['Nernst: E = E° − \\f{0.059}{n} log\\f{[anode ion]}{[cathode ion]}.', f'= {nf(E, 3)} − \\f{{0.059}}{{{na}}} log\\f{{{c1}}}{{{c2}}} ≈ {nf(Ec, 3)} V.'], p=dict(t=t, Ea=Ea, Eb=Eb, n=na, c1=c1, c2=c2))
    if t == 'comb':
        e1, e2 = rng.choice([0.77, 0.15, 1.51, 0.52, 1.0, -0.41, 0.34, 2.0, 1.2, 1.7, 0.9, 1.1]), rng.choice([-0.44, -0.14, 0.16, 0.34, -0.9, 0.52, 0.8, -0.5, 0.2, 1.0])
        n1, n2 = rng.choice([(1, 2), (1, 1), (2, 1), (3, 1), (1, 3), (4, 1), (3, 2)])
        E = (n1 * e1 + n2 * e2) / (n1 + n2)
        q = f'For a species X: X^{{a}} →(E° = {sg(e1)} V, {n1} e^{{−}}) X^{{b}} →(E° = {sg(e2)} V, {n2} e^{{−}}) X^{{c}}. E° for X^{{a}} → X^{{c}} directly is about :'
        o, a = mcq(rng, f'{nmv(E)} V', [f'{nmv(v)} V' for v in (e1 + e2, (e1 + e2) / 2, e1 - e2, (n2 * e1 + n1 * e2) / (n1 + n2) if n1 != n2 else e1 * 2)])
        return dict(q=q, o=o, a=a, sol=['Add ΔG° = −nFE°, not the potentials.', f'E° = \\f{{{n1}({sg(e1)}) + {n2}({sg(e2)})}}{{{n1 + n2}}} ≈ {nmv(E)} V.'], p=dict(t=t, e1=e1, e2=e2, n1=n1, n2=n2))
    if t == 'hph':
        pH = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]); pp = rng.choice([1, 1, 2, 4, 10, 100, 0.1, 0.5, 0.01]); E = -0.059 * pH - 0.0295 * math.log10(pp)
        q = f'A hydrogen electrode (p_{{H_{{2}}}} = {pp} bar) is dipped in a solution of pH {pH} at 298 K. Its reduction potential is about (\\f{{2.303RT}}{{F}} = 0.059 V) :'
        o, a = mcq(rng, f'{nmv(E)} V', [f'{nmv(v)} V' for v in (-E, -0.059 * pH, -0.0295 * pH, E - 0.059)])
        return dict(q=q, o=o, a=a, sol=['2H^{+} + 2e^{−} → H_{2}: E = −\\f{0.059}{2} log\\f{p_{H_{2}}}{[H^{+}]^{2}} = −0.059 pH − 0.0295 log p.', f'E ≈ {nmv(E)} V.'], p=dict(t=t, pH=pH, pp=pp))
    if t == 'ksp':
        m = rng.choice([('Ag^{+}/Ag', 0.80, 'AgCl', 1.8e-10, 'Cl^{−}'), ('Ag^{+}/Ag', 0.80, 'AgBr', 5e-13, 'Br^{−}'), ('Ag^{+}/Ag', 0.80, 'AgI', 8.5e-17, 'I^{−}'), ('M^{+}/M', 0.79, 'MX', 1e-10, 'X^{−}'), ('M^{+}/M', 0.70, 'MX', 1e-8, 'X^{−}'), ('M^{+}/M', 0.60, 'MY', 1e-12, 'Y^{−}')])
        E = m[1] + 0.059 * math.log10(m[3])
        return dict(q=f'E°({m[0]}) = {m[1]} V and K_{{sp}}({m[2]}) = {nf(m[3], 2)} at 298 K. E° for {m[2]}(s) + e^{{−}} → {m[0].split("/")[1]}(s) + {m[4]} is ____ mV (nearest integer).', o=None, a=round(E * 1000),
                    sol=['Add M^{+} + e^{−} → M to the dissolution MX → M^{+} + X^{−}.', f'E° = {m[1]} + 0.059 log K_{{sp}} ≈ {nf(E, 3)} V.'], p=dict(t=t, E0=m[1], K=m[3]))
    c1, c2 = rng.sample([0.001, 0.01, 0.1, 1, 0.05, 0.5, 0.002], 2); n = rng.choice([1, 2]); ion = 'Ag^{+}' if n == 1 else 'Cu^{2+}'; metal = 'Ag' if n == 1 else 'Cu'
    lo, hi = min(c1, c2), max(c1, c2); E = 0.059 / n * math.log10(hi / lo)
    q = f'Concentration cell: {metal} | {ion} ({lo} M) || {ion} ({hi} M) | {metal}. Its emf at 298 K is ____ mV (nearest integer; \\f{{2.303RT}}{{F}} = 0.059 V).'
    return dict(q=q, o=None, a=round(E * 1000), sol=['E° = 0 for a concentration cell.', f'E = \\f{{0.059}}{{{n}}} log\\f{{{hi}}}{{{lo}}} ≈ {nf(E * 1000, 4)} mV.'], p=dict(t='conc', lo=lo, hi=hi, n=n))

ION = {'H^{+}': 349.8, 'Na^{+}': 50.1, 'K^{+}': 73.5, 'Ca^{2+}': 119.0, 'Mg^{2+}': 106.0, 'Cl^{−}': 76.3, 'OH^{−}': 198.0, 'NO_{3}^{−}': 71.4, 'CH_{3}COO^{−}': 40.9, 'SO_{4}^{2−}': 160.0, 'NH_{4}^{+}': 73.5}
def g_cond(rng):
    t = rng.choice(['kap', 'lam', 'kohl', 'alpha', 'ka', 'slope', 'cellk'])
    if t == 'kap':
        R = rng.choice([50, 100, 120, 200, 250, 400, 500, 1000, 1500]); G = rng.choice([0.5, 0.88, 1.0, 1.29, 1.5, 2.0, 0.25])
        k = G / R
        return dict(q=f'A conductivity cell of cell constant {G} cm^{{−1}} shows a resistance of {R} Ω. The conductivity is :', o=(o := mcq(rng, f'{nf(k, 3)} S cm^{{−1}}', [f'{nf(v, 3)} S cm^{{−1}}' for v in (R / G, G * R, 1 / R, k * 100)]))[0], a=o[1],
                    sol=['κ = \\f{G*}{R} (cell constant ÷ resistance).', f'κ = \\f{{{G}}}{{{R}}} = {nf(k, 3)} S cm^{{−1}}.'], p=dict(t=t, R=R, G=G))
    if t == 'lam':
        k = rng.choice([1.2, 2.4, 3.9, 5.0, 7.5, 11.8, 14.0]) * 10 ** rng.choice([-3, -4, -5]); c = rng.choice([0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1])
        L = k * 1000 / c
        o, a = mcq(rng, f'{nf(L, 3)} S cm^{{2}} mol^{{−1}}', [f'{nf(v, 3)} S cm^{{2}} mol^{{−1}}' for v in (k / c, k * c * 1000, L / 10, L * 10)])
        return dict(q=f'A {c} M solution has conductivity {nf(k, 3)} S cm^{{−1}}. Its molar conductivity is :', o=o, a=a, sol=['Λ_{m} = \\f{κ × 1000}{c} (κ in S cm^{−1}, c in mol L^{−1}).', f'= \\f{{{nf(k, 3)} × 1000}}{{{c}}} = {nf(L, 3)} S cm^{{2}} mol^{{−1}}.'], p=dict(t=t, k=k, c=c))
    if t in ('kohl', 'alpha', 'ka'):
        wk = rng.choice([('CH_{3}COOH', 'CH_{3}COONa', 'HCl', 'NaCl'), ('NH_{4}OH', 'NH_{4}Cl', 'NaOH', 'NaCl')])
        L = {s: sum(ION[i] for i in ions) for s, ions in {'CH_{3}COOH': ['H^{+}', 'CH_{3}COO^{−}'], 'CH_{3}COONa': ['Na^{+}', 'CH_{3}COO^{−}'], 'HCl': ['H^{+}', 'Cl^{−}'], 'NaCl': ['Na^{+}', 'Cl^{−}'],
                                                     'NH_{4}OH': ['NH_{4}^{+}', 'OH^{−}'], 'NH_{4}Cl': ['NH_{4}^{+}', 'Cl^{−}'], 'NaOH': ['Na^{+}', 'OH^{−}']}.items()}
        a1, a2, a3 = (round(L[wk[1]], 1), round(L[wk[2]], 1), round(L[wk[3]], 1)); L0 = a1 + a2 - a3
        giv = f'Λ°({wk[1]}) = {a1}, Λ°({wk[2]}) = {a2}, Λ°({wk[3]}) = {a3} S cm^{{2}} mol^{{−1}}'
        if t == 'kohl':
            o, a = mcq(rng, f'{nf(L0, 4)} S cm^{{2}} mol^{{−1}}', [f'{nf(v, 4)} S cm^{{2}} mol^{{−1}}' for v in (a1 + a2 + a3, a1 - a2 + a3, a2 + a3 - a1, a1 + a3 - a2)])
            return dict(q=f'{giv}. Λ° of {wk[0]} is :', o=o, a=a, sol=['Kohlrausch: combine so the spectator ions cancel.', f'Λ°({wk[0]}) = {a1} + {a2} − {a3} = {nf(L0, 4)}.'], p=dict(t=t, a1=a1, a2=a2, a3=a3))
        al = rng.choice([0.01, 0.02, 0.025, 0.04, 0.05, 0.08, 0.1, 0.12]); Lm = al * L0; c = rng.choice([0.001, 0.005, 0.01, 0.02, 0.05, 0.1])
        if t == 'alpha':
            return dict(q=f'{giv}. If Λ_{{m}} of a {c} M {wk[0]} solution is {nf(Lm, 4)} S cm^{{2}} mol^{{−1}}, its degree of dissociation is ____ × 10^{{−3}} (nearest integer).', o=None, a=round(Lm / L0 * 1000),
                        sol=[f'Λ°({wk[0]}) = {a1} + {a2} − {a3} = {nf(L0, 4)}.', f'α = \\f{{Λ_{{m}}}}{{Λ°}} ≈ {nf(Lm / L0, 3)}.'], p=dict(t=t, a1=a1, a2=a2, a3=a3, Lm=Lm))
        Ka = c * al * al / (1 - al)
        o, a = mcq(rng, nf(Ka, 3), [nf(v, 3) for v in (c * al * al, c * al, al * al, Ka * 10)])
        return dict(q=f'{giv}. A {c} M {wk[0]} solution has Λ_{{m}} = {nf(Lm, 4)} S cm^{{2}} mol^{{−1}}. Its dissociation constant is about :', o=o, a=a,
                    sol=[f'α = \\f{{Λ_{{m}}}}{{Λ°}} = {nf(al, 3)}.', f'K = \\f{{cα^{{2}}}}{{1 − α}} ≈ {nf(Ka, 3)}.'], p=dict(t=t, a1=a1, a2=a2, a3=a3, Lm=Lm, c=c))
    if t == 'slope':
        L0 = rng.choice([110, 126.4, 149.9, 98.5, 120]); A = rng.choice([2, 4, 5, 8, 10, 12, 20]); r1, r2 = rng.sample([0.1, 0.2, 0.3, 0.4, 0.5], 2)
        y1, y2 = L0 - A * r1, L0 - A * r2
        return dict(q=f'For a strong electrolyte Λ_{{m}} = Λ°_{{m}} − A√{{c}}. At c = {nf(r1 * r1, 3)} M, Λ_{{m}} = {nf(y1, 4)} and at c = {nf(r2 * r2, 3)} M, Λ_{{m}} = {nf(y2, 4)} S cm^{{2}} mol^{{−1}}. The value of A is ____ (nearest integer).', o=None, a=A,
                    sol=['Plot against √{c}: A = −slope.', f'A = \\f{{{nf(y1, 4)} − {nf(y2, 4)}}}{{{r2} − {r1}}} = {A}.'], p=dict(t=t, c1=r1 * r1, c2=r2 * r2, y1=y1, y2=y2))
    l, A_ = rng.choice([0.5, 1, 1.5, 2, 2.5, 3, 5, 10, 15]), rng.choice([0.5, 1, 1.25, 2, 2.5, 4, 5])
    return dict(q=f'Two electrodes, each of area {A_} cm^{{2}}, are {l} cm apart. The cell constant is ____ × 10^{{−2}} cm^{{−1}} (nearest integer).', o=None, a=round(l / A_ * 100),
                sol=['Cell constant G* = \\f{l}{A}.', f'= \\f{{{l}}}{{{A_}}} = {nf(l / A_, 4)} cm^{{−1}}.'], p=dict(t='cellk', l=l, A=A_))

MET = {'Cu': (63.5, 2, 'CuSO_{4}'), 'Ag': (108, 1, 'AgNO_{3}'), 'Zn': (65.4, 2, 'ZnSO_{4}'), 'Al': (27, 3, 'AlCl_{3} (molten)'), 'Ni': (58.7, 2, 'NiSO_{4}'), 'Au': (197, 3, 'AuCl_{3}'), 'Cr': (52, 3, 'Cr_{2}(SO_{4})_{3}')}
def g_elys(rng):
    t = rng.choice(['mass', 'time', 'cur', 'gas', 'series', 'ph'])
    m = rng.choice(list(MET)); M, z, salt = MET[m]
    if t == 'mass':
        I, tm = rng.choice([0.5, 1, 1.5, 2, 2.5, 3, 5, 10]), rng.choice([10, 15, 20, 30, 45, 60, 90, 120])
        w = I * tm * 60 / F_ / z * M
        o, a = mcq(rng, f'{nf(w, 3)} g', [f'{nf(v, 3)} g' for v in (w * z, w / 2 if z != 2 else w * 1.5, I * tm / F_ * M, w * 60)])
        return dict(q=f'A current of {I} A is passed through {salt} for {tm} min. Mass of {m} deposited (M = {M} g/mol) is about :', o=o, a=a, sol=[f'Q = {I} × {tm * 60} = {nf(I * tm * 60, 5)} C; {m}^{{{z}+}} needs {z} F per mol.', f'm = \\f{{Q}}{{{z} × 96500}} × {M} ≈ {nf(w, 3)} g.'], p=dict(t=t, m=m, I=I, tm=tm))
    if t == 'time':
        w = rng.choice([0.5, 1, 1.27, 2, 2.16, 3, 5.4]); I = rng.choice([0.5, 1, 2, 2.5, 5]); s = w / M * z * F_ / I
        return dict(q=f'How many minutes does it take to deposit {w} g of {m} (M = {M}) from {salt} with a current of {I} A? ____ (nearest integer)', o=None, a=round(s / 60),
                    sol=[f'Moles of e^{{−}} = \\f{{{w}}}{{{M}}} × {z}.', f't = \\f{{n_{{e}}F}}{{I}} ≈ {nf(s, 4)} s ≈ {round(s / 60)} min.'], p=dict(t=t, m=m, w=w, I=I))
    if t == 'cur':
        w = rng.choice([0.254, 0.5, 1.08, 1.27, 2.16, 0.635]); tm = rng.choice([5, 10, 16, 20, 30, 40]); I = w / M * z * F_ / (tm * 60)
        o, a = mcq(rng, f'{nf(I, 3)} A', [f'{nf(v, 3)} A' for v in (I * 60, I / z, I * z, I / 2 if z == 1 else I * 1.5)])
        return dict(q=f'{w} g of {m} (M = {M}) is deposited from {salt} in {tm} min. The current used is about :', o=o, a=a, sol=[f'Charge = \\f{{{w}}}{{{M}}} × {z} × 96500.', f'I = \\f{{Q}}{{{tm} × 60}} ≈ {nf(I, 3)} A.'], p=dict(t=t, m=m, w=w, tm=tm))
    if t == 'gas':
        g, ne = rng.choice([('H_{2}', 2), ('O_{2}', 4), ('Cl_{2}', 2)]); Q = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 2, 4]); V = Q / ne * 22.7
        o, a = mcq(rng, f'{nf(V, 3)} L', [f'{nf(v, 3)} L' for v in (Q * 22.7, Q / 2 * 22.7 if ne == 4 else Q / 4 * 22.7, V * 2, Q * 11.35 / 4 if ne != 4 else V / 2)])
        return dict(q=f'{Q} F of charge is passed and {g} is evolved. Its volume at STP (22.7 L mol^{{−1}}) is about :', o=o, a=a, sol=[f'{g} needs {ne} mol e^{{−}} per mol.', f'V = \\f{{{Q}}}{{{ne}}} × 22.7 ≈ {nf(V, 3)} L.'], p=dict(t=t, ne=ne, Q=Q))
    if t == 'series':
        m2 = rng.choice([x for x in MET if x != m]); M2, z2, s2 = MET[m2]; w = rng.choice([0.5, 1, 1.08, 2, 3.175, 5])
        w2 = w / M * z / z2 * M2
        o, a = mcq(rng, f'{nf(w2, 3)} g', [f'{nf(v, 3)} g' for v in (w * M2 / M, w * z2 / z, w2 * 2, w * M / M2)])
        return dict(q=f'Two cells containing {salt} and {s2} are in series. When {w} g of {m} (M = {M}) deposits, the mass of {m2} (M = {M2}) deposited is :', o=o, a=a,
                    sol=['Same charge flows through both → equal moles of electrons (Faraday\'s 2nd law).', f'm = {w} × \\f{{{M2}/{z2}}}{{{M}/{z}}} ≈ {nf(w2, 3)} g.'], p=dict(t=t, m=m, m2=m2, w=w))
    V = rng.choice([100, 200, 250, 500, 600, 1000]); I = rng.choice([0.5, 0.965, 1, 1.93, 2, 9.65]); s = rng.choice([50, 100, 193, 300, 500])
    oh = I * s / F_ / (V / 1000); pH = 14 + math.log10(oh); need(9 < pH < 13.5)
    return dict(q=f'{V} mL of brine (NaCl solution) is electrolysed with {I} A for {s} s. The pH of the solution afterwards is about ____ × 10^{{−1}} (nearest integer).', o=None, a=round(pH * 10),
                sol=['Cathode: 2H_{2}O + 2e^{−} → H_{2} + 2OH^{−}: one OH^{−} per electron.', f'[OH^{{−}}] = \\f{{{I} × {s}/96500}}{{{V / 1000}}} ≈ {nf(oh, 3)} M → pH ≈ {nf(pH, 3)}.'], p=dict(t='ph', V=V, I=I, s=s))

BAT = {'dry (Leclanché) cell': ['anode is a zinc container', 'cathode: MnO_{2} + NH_{4}^{+} + e^{−} → MnO(OH) + NH_{3}', 'used in transistors and torches', 'is a primary (non-rechargeable) cell'],
       'mercury cell': ['electrolyte is a paste of KOH and ZnO', 'voltage stays constant (~1.35 V) through its life', 'used in hearing aids and watches', 'cathode: HgO + H_{2}O + 2e^{−} → Hg + 2OH^{−}'],
       'lead storage battery': ['electrolyte is 38% H_{2}SO_{4}', 'on discharge both electrodes become PbSO_{4}', 'is rechargeable — used in cars and invertors', 'anode is spongy Pb'],
       'nickel–cadmium cell': ['is rechargeable with a longer life than the lead battery', 'anode is cadmium', 'cathode involves NiO(OH)', 'is a secondary cell'],
       'H_{2}–O_{2} fuel cell': ['converts combustion energy directly into electricity', 'efficiency is about 70%', 'used in the Apollo space programme', 'uses finely divided Pt or Pd as catalyst'],
       'rusting of iron': ['needs both water and oxygen', 'iron acts as the anode: Fe → Fe^{2+} + 2e^{−}', 'is speeded up by dissolved salts and acidic oxides', 'is prevented by a coating of zinc (sacrificial protection)']}
FALSE = {'dry (Leclanché) cell': 'can be recharged many times', 'mercury cell': 'its voltage falls steadily as it is used', 'lead storage battery': 'electrolyte is KOH paste',
         'nickel–cadmium cell': 'is a primary cell', 'H_{2}–O_{2} fuel cell': 'uses aluminium as catalyst', 'rusting of iron': 'is prevented by tin even after the tin coating is scratched'}
def g_batt(rng):
    t = rng.choice(['true', 'false', 'match'])
    b = rng.choice(list(BAT))
    if t == 'true':
        right = rng.choice(BAT[b]); wrong = rng.sample([FALSE[b]] + [x for k, v in BAT.items() if k != b for x in v if x not in BAT[b]], 3)
        o, a = mcq(rng, right, wrong)
        return dict(q=f'Which statement is correct for the {b}?', o=o, a=a, sol=[f'{b[0].upper() + b[1:]}: ' + '; '.join(BAT[b]) + '.'], p=dict(t=t, b=b))
    if t == 'false':
        right = FALSE[b]; wrong = rng.sample(BAT[b], 3); o, a = mcq(rng, right, wrong)
        return dict(q=f'Which statement is NOT correct for the {b}?', o=o, a=a, sol=[f'Correct facts: ' + '; '.join(BAT[b]) + '.', f'So "{right}" is the wrong one.'], p=dict(t=t, b=b))
    fact = rng.choice(BAT[b]); others = rng.sample([k for k in BAT if k != b], 3); o, a = mcq(rng, b, others)
    return dict(q=f'Which one fits the description: "{fact}"?', o=o, a=a, sol=[f'This describes the {b}.'], p=dict(t=t, b=b, fact=fact))

def robust(gf):
    def w(rng):
        for _ in range(300):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, OverflowError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(ox=g_ox, ecell=g_ecell, cond=g_cond, elys=g_elys, batt=g_batt).items()}
def finish(it): return it

def _on(name):   # independent: re-derive from the printed formula text
    c = next(c for c in CMP if c[0] == name); _, el, n, rest, ch = c
    fx = {'H': 1, 'O': -2, 'F': -1, 'Cl': -1, 'K': 1, 'Na': 1, 'Ba': 2, 'Ca': 2, 'Br': -1}
    if el == 'O': fx.pop('O')
    if el == 'H': fx.pop('H')
    tot = sum(fx[k] * v for k, v in rest.items()); return F_frac(ch - tot, n)
def F_frac(a, b):
    from fractions import Fraction; return Fraction(a) / b
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'on': return abs(num(Rv) - float(_on(p['c']))) < 6e-3
    if t == 'count': return Rv == sum(1 for c in p['cs'] if float(_on(c)) == p['k'])
    if t == 'disp': return Rv == sum(1 for s in p['sp'] if s in DISP_Y)
    if t == 'eq':   # electron balance: n_ox × e_ox = n_red × e_red
        e_ox = {'KMnO_{4} (acidic)': 7 - 2, 'KMnO_{4} (neutral)': 7 - 4, 'KMnO_{4} (strongly basic)': 7 - 6, 'K_{2}Cr_{2}O_{7} (acidic)': 2 * (6 - 3)}[p['ox']]
        e_rd = {'Fe^{2+}': 3 - 2, 'C_{2}O_{4}^{2−}': 2 * (4 - 3), 'H_{2}O_{2}': 2 * (0 + 1), 'Sn^{2+}': 4 - 2, 'I^{−}': 0 + 1, 'SO_{3}^{2−}': 6 - 4, 'NO_{2}^{−}': 5 - 3, 'S^{2−} (to S)': 0 + 2}[p['rd']]
        return close(num(Rv), p['nr'] * e_rd / e_ox)
    if t == 'e0': return close(num(Rv), p['Eb'] - p['Ea'], 0.005)
    if t in ('dg', 'logk'):
        na, nb = p['na'], p['nb']; n = math.lcm(na, nb); G = -(n // na) * na * F_ * (-p['Ea']) - (n // nb) * nb * F_ * p['Eb']   # oxidation + reduction ΔG°s
        return close(num(Rv), G / 1000, 0.005) if t == 'dg' else Rv == round(-G / (F_ * 0.059))
    if t == 'nernst':
        Q = p['c1'] / p['c2']; return abs(num(Rv) - ((p['Eb'] - p['Ea']) - 0.059 / p['n'] * math.log10(Q))) < 0.006
    if t == 'comb':
        G = -p['n1'] * p['e1'] - p['n2'] * p['e2']; return abs(num(Rv) - (-G / (p['n1'] + p['n2']))) < 0.006
    if t == 'hph': return abs(num(Rv) - (-(0.059 / 2) * math.log10(p['pp'] / (10 ** -p['pH']) ** 2))) < 0.006
    if t == 'ksp': return Rv == round((p['E0'] - 0.059 * -math.log10(p['K'])) * 1000)
    if t == 'conc': return Rv == round(0.059 / p['n'] * (math.log10(p['hi']) - math.log10(p['lo'])) * 1000)
    if t == 'kap': return close(num(Rv), p['G'] / p['R'])
    if t == 'lam':   # SI route: κ S/m ÷ c mol/m³ → S m² mol⁻¹ → × 10⁴ cm²
        return close(num(Rv), (p['k'] * 100) / (p['c'] * 1000) * 1e4)
    if t in ('kohl', 'alpha', 'ka'):
        L0 = p['a1'] + p['a2'] - p['a3']
        if t == 'kohl': return close(num(Rv), L0)
        al = p['Lm'] / L0
        if t == 'alpha': return Rv == round(al * 1000)
        return close(num(Rv), p['c'] * al * al / (1 - al), 0.02)
    if t == 'slope': return Rv == round((p['y1'] - p['y2']) / (math.sqrt(p['c2']) - math.sqrt(p['c1'])))
    if t == 'cellk': return Rv == round(p['l'] / p['A'] * 100)
    if t in ('mass', 'time', 'cur', 'series'):
        M, z, _ = MET[p['m']]
        if t == 'mass': return close(num(Rv), p['I'] * p['tm'] * 60 * M / (z * F_))
        if t == 'time': return Rv == round(p['w'] * z * F_ / M / p['I'] / 60)
        if t == 'cur': return close(num(Rv), p['w'] * z * F_ / M / (p['tm'] * 60))
        M2, z2, _ = MET[p['m2']]; ne = p['w'] / M * z; return close(num(Rv), ne / z2 * M2)
    if t == 'gas': return close(num(Rv), p['Q'] / p['ne'] * 22.7)
    if t == 'ph': return Rv == round((14 + math.log10(p['I'] * p['s'] / F_ / (p['V'] / 1000))) * 10)
    if t == 'true': return Rv in BAT[p['b']]
    if t == 'false': return Rv == FALSE[p['b']] and Rv not in BAT[p['b']]
    if t == 'match': return Rv == p['b'] and p['fact'] in BAT[Rv]
    raise KeyError(t)
