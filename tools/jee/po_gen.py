"""Practice generators — Chemistry Unit 13: Purification and Characterisation of Organic Compounds. check() recomputes
each answer another way: Dumas with SI units (Pa, m³, R = 8.314), Kjeldahl via milli-equivalents, gravimetric
estimations from atomic masses summed atom by atom, empirical formulae by trying whole-number multipliers, R_f from
the two distances. Method and test items come from a fact bank written from NCERT."""
import re, itertools
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
AM = {'C': 12, 'H': 1, 'N': 14, 'O': 16, 'S': 32, 'Cl': 35.5, 'Br': 80, 'I': 127, 'Ag': 108, 'Ba': 137, 'P': 31, 'Mg': 24}
def cnt(f): return dict((e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f))
def mm(f): return sum(AM[e] * n for e, n in cnt(f).items())
def tex(f): return re.sub(r'(\d+)', r'_{\1}', f)
CMPDS = [('urea', 'CH4N2O'), ('acetamide', 'C2H5NO'), ('aniline', 'C6H7N'), ('glycine', 'C2H5NO2'), ('ethylamine', 'C2H7N'), ('benzamide', 'C7H7NO'), ('nitrobenzene', 'C6H5NO2'),
         ('pyridine', 'C5H5N'), ('thiourea', 'CH4N2S'), ('p-nitroaniline', 'C6H6N2O2'), ('acetanilide', 'C8H9NO'), ('alanine', 'C3H7NO2'), ('methylamine', 'CH5N'), ('piperazine', 'C4H10N2'),
         ('chlorobenzene', 'C6H5Cl'), ('bromobenzene', 'C6H5Br'), ('iodobenzene', 'C6H5I'), ('chloroform', 'CHCl3'), ('ethyl bromide', 'C2H5Br'), ('methyl iodide', 'CH3I'), ('benzyl chloride', 'C7H7Cl'),
         ('1,2-dibromoethane', 'C2H4Br2'), ('thiophene', 'C4H4S'), ('dimethyl sulphide', 'C2H6S'), ('sulphanilic acid', 'C6H7NO3S'), ('benzoic acid', 'C7H6O2'), ('ethanol', 'C2H6O'), ('acetic acid', 'C2H4O2'),
         ('glucose', 'C6H12O6'), ('phenol', 'C6H6O'), ('carbon tetrachloride', 'CCl4'), ('o-nitrophenol', 'C6H5NO3'), ('methionine', 'C5H11NO2S'), ('cysteine', 'C3H7NO2S')]
def pct_tex(x): return nf(x, 4)

def g_det(rng):
    t = rng.choice(['dumas', 'dumas_o', 'kjel', 'kjel_o', 'stp', 'lass', 'test'])
    if t in ('dumas', 'dumas_o'):
        w = rng.choice([0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75, 1.0]); V = rng.choice(range(20, 160, 5)); T = rng.choice([287, 290, 293, 295, 298, 300, 303, 310]); Pt = rng.choice(range(700, 920, 5)); aq = rng.choice([12, 14, 15, 17, 18, 20])
        n = (Pt - aq) / 760 * V / 1000 / (0.0821 * T); pc = n * 28 / w * 100; need(3 < pc < 80)
        q = f"In Dumas' method, {nf(w, 3)} g of an organic compound gave {V} mL of moist N_{{2}} collected at {T} K and {Pt} mm Hg (aqueous tension {aq} mm Hg). The percentage of nitrogen is"
        sol = [f'Dry N_{{2}}: {Pt} − {aq} = {Pt - aq} mm Hg.', f'n = PV/RT = ({Pt - aq}/760)({V}/1000)/(0.0821 × {T}) = {nf(n, 4)} mol → {nf(n * 28, 4)} g.', f'% N = {nf(pc, 4)}%.']
        if t == 'dumas': return dict(q=q + ' ____ % (nearest integer).', o=None, a=round(pc), sol=sol, p=dict(t=t, w=w, V=V, T=T, P=Pt, aq=aq))
        o, a = mcq(rng, pct_tex(pc) + '%', [pct_tex(x) + '%' for x in (n * 28 / w * 100 * Pt / (Pt - aq), n * 14 / w * 100, pc * 273 / T, pc * 2.24)])
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t=t, w=w, V=V, T=T, P=Pt, aq=aq))
    if t in ('kjel', 'kjel_o'):
        w = rng.choice([0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5]); acid = rng.choice(['H2SO4', 'HCl']); M = rng.choice([0.1, 0.2, 0.25, 0.5, 1.0]); V = rng.choice(range(5, 61, 5)); b = 2 if acid == 'H2SO4' else 1
        pc = b * M * V / 1000 * 14 / w * 100; need(2 < pc < 70)
        q = f"In Kjeldahl's method, the ammonia from {nf(w, 3)} g of an organic compound neutralised {V} mL of {nf(M, 3)} M {tex(acid)}. The percentage of nitrogen is"
        sol = [f'mol NH_{{3}} = {b} × {nf(M, 3)} × {V}/1000 = {nf(b * M * V / 1000, 4)}.', f'N = {nf(b * M * V / 1000 * 14, 4)} g → {nf(pc, 4)}%.']
        if t == 'kjel': return dict(q=q + ' ____ % (nearest integer).', o=None, a=round(pc), sol=sol, p=dict(t=t, w=w, M=M, V=V, acid=acid))
        o, a = mcq(rng, pct_tex(pc) + '%', [pct_tex(x) + '%' for x in (pc / b if b == 2 else pc * 2, pc * 17 / 14, pc / 2 if b == 1 else pc * 1.5, pc * 28 / 14)])
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t=t, w=w, M=M, V=V, acid=acid))
    if t == 'stp':
        name, f = rng.choice([c for c in CMPDS if 'N' in cnt(c[1])]); w = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]); v = w / mm(f) * cnt(f)['N'] / 2 * 22400
        return dict(q=f"In Dumas' method, {nf(w, 3)} g of {name} ({tex(f)}) is analysed. Volume of N_{{2}} at STP = ____ mL (nearest integer; 1 mol gas = 22.4 L).", o=None, a=round(v),
                    sol=[f'M = {mm(f)}; mol = {nf(w / mm(f), 4)}; each molecule gives {cnt(f)["N"]}/2 N_{{2}}.', f'V = {nf(v, 4)} mL.'], p=dict(t=t, w=w, f=f))
    if t == 'lass':
        el = rng.choice(['N', 'S', 'NS', 'Cl', 'Br', 'I', 'P'])
        A = {'N': 'Prussian blue with FeSO_{4}, then FeCl_{3}/H_{2}SO_{4}', 'S': 'violet with sodium nitroprusside', 'NS': 'blood red with FeCl_{3}', 'Cl': 'white ppt with HNO_{3}/AgNO_{3}, soluble in NH_{3}',
             'Br': 'pale yellow ppt with AgNO_{3}, sparingly soluble in NH_{3}', 'I': 'yellow ppt with AgNO_{3}, insoluble in NH_{3}', 'P': 'yellow ppt with ammonium molybdate'}
        N = {'N': 'nitrogen', 'S': 'sulphur', 'NS': 'nitrogen and sulphur together', 'Cl': 'chlorine', 'Br': 'bromine', 'I': 'iodine', 'P': 'phosphorus'}
        if rng.random() < 0.5:
            o, a = mcq(rng, A[el], [A[k] for k in rng.sample([k for k in A if k != el], 5)])
            return dict(q=f'In the sodium fusion (Lassaigne) extract, {N[el]} is shown by', o=o, a=a, sol=[f'{N[el]}: {A[el]}.'], p=dict(t='lass', el=el, dir=0))
        o, a = mcq(rng, N[el], [N[k] for k in rng.sample([k for k in N if k != el], 5)])
        return dict(q=f'The sodium fusion extract of a compound gives {A[el]}. This shows the presence of', o=o, a=a, sol=[f'{A[el]} ↔ {N[el]}.'], p=dict(t='lass', el=el, dir=1))
    F = [("Kjeldahl's method cannot be used for nitro, azo compounds or pyridine.", True), ("CuSO_{4} acts as a catalyst in Kjeldahl's method.", True), ("K_{2}SO_{4} is added in Kjeldahl digestion to raise the boiling point.", True),
         ("In Dumas' method the compound is heated with CuO in CO_{2}.", True), ("In Dumas' method nitrogen is converted to ammonium sulphate.", False), ('Lassaigne\'s test uses fusion with magnesium.', False),
         ('Hydrazine gives a positive Lassaigne test for nitrogen.', False), ('Sodium fusion converts covalent N, S, X into ionic NaCN, Na_{2}S, NaX.', True), ('The extract is boiled with HNO_{3} before the halogen test to destroy CN^{−} and S^{2−}.', True),
         ('A compound with N and S gives Prussian blue in Lassaigne\'s test when Na is in excess.', True), ('Phosphorus is estimated as Mg_{2}P_{2}O_{7}.', True), ("In Carius method halogens are precipitated as AgX.", True),
         ("In Carius method sulphur is precipitated as BaSO_{4}.", True), ('Carbon and hydrogen are estimated by absorbing CO_{2} in anhydrous CaCl_{2}.', False), ('Water formed in combustion is absorbed in anhydrous CaCl_{2}.', True),
         ('CO_{2} formed in combustion is absorbed in KOH solution.', True), ('Oxygen is usually found by difference.', True), ('Nitroprusside test for S gives a violet colour.', True)]
    want = rng.choice([True, False]); r = rng.choice([s for s, v in F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want, F=dict(F)))

PPT = {'Cl': 'AgCl', 'Br': 'AgBr', 'I': 'AgI', 'S': 'BaSO4', 'P': 'Mg2P2O7'}
def g_est(rng):
    t = rng.choice(['carius', 'carius_o', 'comb', 'pctf', 'emp', 'mol', 'ppt'])
    if t in ('carius', 'carius_o'):
        el = rng.choice(['Cl', 'Br', 'I', 'S', 'P']); ppt = PPT[el]; w = rng.choice([0.15, 0.18, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]); wp = round(rng.uniform(0.1, 1.2), 3)
        k = cnt(ppt)[el]; pc = wp * k * AM[el] / mm(ppt) / w * 100; need(5 < pc < 90)
        q = f'In the estimation of {el}, {nf(w, 3)} g of an organic compound gave {nf(wp, 4)} g of {tex(ppt)}. The percentage of {el} is'
        sol = [f'{tex(ppt)}: M = {mm(ppt)}, contains {k} {el} ({k * AM[el]} g per mol).', f'{el} = {nf(wp, 4)} × {k * AM[el]}/{mm(ppt)} = {nf(pc * w / 100, 4)} g → {nf(pc, 4)}%.']
        if t == 'carius': return dict(q=q + ' ____ % (nearest integer).', o=None, a=round(pc), sol=sol, p=dict(t=t, el=el, w=w, wp=wp))
        o, a = mcq(rng, pct_tex(pc) + '%', [pct_tex(x) + '%' for x in (wp / w * 100, pc * mm(ppt) / (mm(ppt) - 108) if el in ('Cl', 'Br', 'I') else pc * 2, pc / 2, pc * 1.5)])
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t=t, el=el, w=w, wp=wp))
    if t == 'comb':
        name, f = rng.choice([c for c in CMPDS if 'H' in cnt(c[1])]); w = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5]); which = rng.choice(['C', 'H'])
        co2 = w / mm(f) * cnt(f)['C'] * 44; h2o = w / mm(f) * cnt(f)['H'] / 2 * 18
        pc = (co2 * 12 / 44 if which == 'C' else h2o * 2 / 18) / w * 100
        return dict(q=f'{nf(w, 3)} g of an organic compound on complete combustion gave {nf(co2, 4)} g CO_{{2}} and {nf(h2o, 4)} g H_{{2}}O. The percentage of {"carbon" if which == "C" else "hydrogen"} is ____ (nearest integer).', o=None, a=round(pc),
                    sol=[f'{"C = CO_{2} × 12/44" if which == "C" else "H = H_{2}O × 2/18"} = {nf(pc * w / 100, 4)} g.', f'% = {nf(pc, 4)} ≈ {round(pc)}.'], p=dict(t=t, w=w, co2=co2, h2o=h2o, which=which))
    if t == 'pctf':
        name, f = rng.choice(CMPDS); el = rng.choice([e for e in cnt(f) if e != 'H' or rng.random() < 0.3]); pc = AM[el] * cnt(f)[el] / mm(f) * 100
        return dict(q=f'The percentage of {el} in {name} ({tex(f)}) is ____ (nearest integer).', o=None, a=round(pc), sol=[f'M = {mm(f)}; {el}: {cnt(f)[el]} × {AM[el]} = {AM[el] * cnt(f)[el]}.', f'% = {nf(pc, 4)}.'], p=dict(t=t, f=f, el=el))
    if t in ('emp', 'mol'):
        name, f = rng.choice([c for c in CMPDS if len(cnt(c[1])) >= 2]); c = cnt(f); M = mm(f); pcs = {e: AM[e] * n / M * 100 for e, n in c.items()}
        from math import gcd
        from functools import reduce
        g = reduce(gcd, c.values()); emp = {e: n // g for e, n in c.items()}; et = ''.join(f'{e}{n if n > 1 else ""}' for e, n in emp.items())
        shown = ', '.join(f'{e} = {nf(v, 4)}%' for e, v in pcs.items())
        if t == 'emp':
            e = rng.choice(list(emp))
            return dict(q=f'A compound contains {shown}. The number of {e} atoms in its empirical formula is ____.', o=None, a=emp[e], sol=['Divide each % by its atomic mass, then by the smallest.', f'Empirical formula {tex(et)}.'], p=dict(t=t, pcs=pcs, e=e))
        e = rng.choice(list(c))
        return dict(q=f'A compound contains {shown} and its molar mass is {M} g mol^{{−1}}. The number of {e} atoms in one molecule is ____.', o=None, a=c[e], sol=[f'Empirical formula {tex(et)} (mass {mm(et)}); n = {M}/{mm(et)} = {g}.', f'Molecular formula {tex(f)}.'], p=dict(t=t, pcs=pcs, e=e, M=M))
    name, f = rng.choice([c for c in CMPDS if any(e in cnt(c[1]) for e in ('Cl', 'Br', 'I', 'S'))]); el = [e for e in ('Cl', 'Br', 'I', 'S') if e in cnt(f)][0]; ppt = PPT[el]; w = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.5])
    wp = w / mm(f) * cnt(f)[el] * mm(ppt)
    return dict(q=f'In Carius analysis, {nf(w, 3)} g of {name} ({tex(f)}) gives ____ mg of {tex(ppt)} (nearest integer).', o=None, a=round(wp * 1000), sol=[f'mol = {nf(w / mm(f), 4)}; each gives {cnt(f)[el]} {tex(ppt)} (M = {mm(ppt)}).', f'mass = {nf(wp, 4)} g.'], p=dict(t='ppt', w=w, f=f))

MIX = [('aniline + water', 'steam'), ('essential oil from flowers', 'steam'), ('o-nitrophenol from p-nitrophenol', 'steam'), ('glycerol from spent-lye', 'reduced'), ('a liquid that decomposes at its boiling point', 'reduced'),
       ('chloroform (b.p. 334 K) + aniline (b.p. 457 K)', 'simple'), ('diethyl ether + toluene', 'simple'), ('crude oil into petrol, kerosene, diesel', 'fractional'), ('two liquids with close boiling points', 'fractional'), ('acetone (329 K) + methanol (338 K)', 'fractional'),
       ('camphor + common salt', 'sublimation'), ('naphthalene + sand', 'sublimation'), ('iodine + sand', 'sublimation'), ('benzoic acid from a solution in hot water', 'crystallisation'), ('sugar with a little common salt', 'crystallisation'),
       ('an organic compound from its aqueous solution with ether', 'extraction'), ('plant pigments (chlorophylls)', 'chromatography'), ('coloured components of ink', 'chromatography')]
MN = {'steam': 'steam distillation', 'reduced': 'distillation under reduced pressure', 'simple': 'simple distillation', 'fractional': 'fractional distillation', 'sublimation': 'sublimation', 'crystallisation': 'crystallisation',
      'extraction': 'differential extraction', 'chromatography': 'chromatography'}
SF = [('R_{f} is always less than 1.', True), ('A polar compound has a smaller R_{f} on silica gel than a non-polar one.', True), ('In paper chromatography water held in the paper is the stationary phase.', True), ('Paper chromatography is a kind of adsorption chromatography.', False),
      ('In column chromatography the least strongly adsorbed component comes out first.', True), ('Silica gel and alumina are common adsorbents.', True), ('Steam distillation works for water-miscible liquids.', False),
      ('Reducing the pressure lowers the boiling point of a liquid.', True), ('An azeotrope can be separated by fractional distillation.', False), ('In fractional distillation the vapour rising up the column gets richer in the lower-boiling liquid.', True),
      ('A pure compound shows a sharp melting point.', True), ('Sublimation is used for compounds with low melting points.', False), ('Differential extraction depends on different solubility in two immiscible solvents.', True),
      ('Colourless spots on a TLC plate can be seen under UV light or with iodine vapour.', True), ('In steam distillation the liquid boils when the sum of its vapour pressure and that of water equals atmospheric pressure.', True),
      ('Crystallisation depends on the difference in solubility of the compound and impurities in a solvent.', True), ('The mobile phase is fixed in place in chromatography.', False)]
def g_sep(rng):
    t = rng.choice(['mix', 'mix', 'rf', 'rfd', 'sfact', 'cnt', 'match'])
    if t == 'mix':
        m, k = rng.choice(MIX); o, a = mcq(rng, MN[k], [MN[x] for x in rng.sample([x for x in MN if x != k], 7)])
        return dict(q=f'The best method to separate/purify {m} is', o=o, a=a, sol=[f'{m}: {MN[k]}.'], p=dict(t=t, m=m))
    if t in ('rf', 'rfd'):
        s = rng.choice(range(5, 16)); x = round(rng.uniform(0.5, s - 0.5) * 2) / 2; need(0 < x < s)
        if t == 'rf':
            rf = x / s; need(abs(rf * 100 - round(rf * 100)) < 1e-9)
            return dict(q=f'On a TLC plate a spot moved {nf(x, 3)} cm while the solvent front moved {s} cm. R_{{f}} = ____ × 10^{{−2}}.', o=None, a=round(rf * 100), sol=[f'R_{{f}} = {nf(x, 3)}/{s} = {nf(rf, 3)}.'], p=dict(t=t, x=x, s=s))
        rf = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8]); s = rng.choice([4, 6, 8, 10, 12, 16, 20]); x = rf * s; need(abs(x * 10 - round(x * 10)) < 1e-9)
        return dict(q=f'A compound has R_{{f}} = {rf}. If the solvent front moves {s} cm, the spot moves ____ mm.', o=None, a=round(x * 10), sol=[f'distance = R_{{f}} × {s} cm = {nf(x, 3)} cm = {round(x * 10)} mm.'], p=dict(t=t, rf=rf, s=s))
    if t == 'sfact':
        want = rng.choice([True, False]); r = rng.choice([s for s, v in SF if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in SF if v != want], 3))
        return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t=t, want=want))
    if t == 'cnt':
        pool = rng.sample(SF, rng.randint(4, 5)); n = sum(v for _, v in pool)
        return dict(q='How many of these are correct? ' + ' '.join(f'{"ABCDE"[i]}. {s}' for i, (s, _) in enumerate(pool)), o=None, a=n, sol=['; '.join(f'{"ABCDE"[i]} {"✓" if v else "✗"}' for i, (_, v) in enumerate(pool)) + f' → {n}.'], p=dict(t=t, ss=[s for s, _ in pool]))
    ks = rng.sample(['steam', 'reduced', 'simple', 'fractional', 'sublimation', 'crystallisation', 'chromatography'], 4); ms = [rng.choice([m for m, k in MIX if k == kk]) for kk in ks]
    perm = list(range(4)); rng.shuffle(perm)   # List II order
    right = ', '.join(f'{"ABCD"[i]}-{"I II III IV".split()[perm.index(i)]}' for i in range(4))
    wrong = []
    for p2 in itertools.permutations(range(4)):
        s = ', '.join(f'{"ABCD"[i]}-{"I II III IV".split()[p2[i]]}' for i in range(4))
        if s != right: wrong.append(s)
    rng.shuffle(wrong); o, a = mcq(rng, right, wrong)
    q = 'Match List-I (method) with List-II (use): ' + ' '.join(f'({"ABCD"[i]}) {MN[k]}' for i, k in enumerate(ks)) + '; ' + ' '.join(f'({r}) {ms[perm[j]]}' for j, r in enumerate('I II III IV'.split()))
    return dict(q=q, o=o, a=a, sol=['; '.join(f'{MN[k]} → {m}' for k, m in zip(ks, ms))], p=dict(t='match', ks=ks, ms=ms, perm=perm))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(det=g_det, est=g_est, sep=g_sep).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent re-solve ----------------
def mass2(f):   # atom by atom
    tot = 0.0
    for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f):
        for _ in range(int(n) if n else 1): tot += AM[e]
    return tot
def pnum(R): return float(R.rstrip('%'))
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('dumas', 'dumas_o'):
        n = (p['P'] - p['aq']) * 101325 / 760 * p['V'] * 1e-6 / (8.314 * p['T']); pc = n * 28 / p['w'] * 100
        return (R == round(pc) or abs(R - pc) < 0.5 + 0.004 * pc) if t == 'dumas' else close(pnum(R), pc, 0.006)
    if t in ('kjel', 'kjel_o'):
        meq = p['M'] * (2 if p['acid'] == 'H2SO4' else 1) * p['V']; pc = 1.4 * meq / 1000 * 100 / p['w'] / 100 * 100   # 1 meq NH3 = 14 mg N
        pc = meq * 14 / 1000 / p['w'] * 100
        return R == round(pc) if t == 'kjel' else close(pnum(R), pc, 0.002)
    if t == 'stp': return R == round(p['w'] / mass2(p['f']) * cnt(p['f'])['N'] * 11200)
    if t == 'lass':
        A = {'N': 'Prussian blue', 'S': 'nitroprusside', 'NS': 'blood red', 'Cl': 'white ppt', 'Br': 'pale yellow', 'I': 'yellow ppt with AgNO', 'P': 'molybdate'}
        N = {'N': 'nitrogen', 'S': 'sulphur', 'NS': 'nitrogen and sulphur together', 'Cl': 'chlorine', 'Br': 'bromine', 'I': 'iodine', 'P': 'phosphorus'}
        return A[p['el']] in R if p['dir'] == 0 else R == N[p['el']]
    if t == 'fact': return p['F'][R] == p['want']
    if t in ('carius', 'carius_o'):
        ppt = PPT[p['el']]; pc = p['wp'] * cnt(ppt)[p['el']] * AM[p['el']] / mass2(ppt) / p['w'] * 100
        return R == round(pc) if t == 'carius' else close(pnum(R), pc, 0.002)
    if t == 'comb': x = p['co2'] * 12 / 44 if p['which'] == 'C' else p['h2o'] / 9; return R == round(x / p['w'] * 100)
    if t == 'pctf': return R == round(cnt(p['f'])[p['el']] * AM[p['el']] / mass2(p['f']) * 100)
    if t in ('emp', 'mol'):
        mol = {e: v / AM[e] for e, v in p['pcs'].items()}; lo = min(mol.values())
        k = next(k for k in range(1, 13) if all(abs(k * v / lo - round(k * v / lo)) < 0.03 for v in mol.values())); emp = {e: round(k * v / lo) for e, v in mol.items()}
        if t == 'emp': return R == emp[p['e']]
        em = sum(AM[e] * n for e, n in emp.items()); return R == emp[p['e']] * round(p['M'] / em)
    if t == 'ppt':
        el = [e for e in ('Cl', 'Br', 'I', 'S') if e in cnt(p['f'])][0]; return R == round(p['w'] / mass2(p['f']) * cnt(p['f'])[el] * mass2(PPT[el]) * 1000)
    if t == 'mix': return MN[dict(MIX)[p['m']]] == R
    if t == 'rf': return R * p['s'] == round(p['x'] * 100)
    if t == 'rfd': return R == round(p['rf'] * p['s'] * 10)
    if t == 'sfact': return dict(SF)[R] == p['want']
    if t == 'cnt': return R == sum(dict(SF)[s] for s in p['ss'])
    if t == 'match':
        use = dict(MIX); pairs = dict(x.split('-') for x in R.split(', ')); IIs = 'I II III IV'.split()
        return all(MN[use[p['ms'][p['perm'][IIs.index(pairs[L])]]]] == MN[k] for L, k in zip('ABCD', p['ks']))
    raise KeyError(t)
