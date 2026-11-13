"""Practice generators — Chemistry Unit 18: Organic Compounds Containing Nitrogen. check() recomputes each answer
another way: amine class from counting carbons on nitrogen in a written structure, test verdicts from the class
(Hinsberg, carbylamine, HNO2), basicity from pKb, masses/yields/gas volumes from formula masses."""
import re, itertools
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
AM = {'C': 12, 'H': 1, 'N': 14, 'O': 16, 'Br': 80, 'Cl': 35.5, 'S': 32}
def mm(f): return sum(AM[e] * (int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f))
# name: (condensed structure with N groups written as N(H)(H) etc., aryl?)
AMINES = {'methylamine': 'CH3-NH2', 'ethylamine': 'C2H5-NH2', 'propylamine': 'C3H7-NH2', 'isopropylamine': '(CH3)2CH-NH2', 'dimethylamine': '(CH3)2NH', 'diethylamine': '(C2H5)2NH', 'trimethylamine': '(CH3)3N',
          'triethylamine': '(C2H5)3N', 'aniline': 'C6H5-NH2', 'N-methylaniline': 'C6H5-NH-CH3', 'N,N-dimethylaniline': 'C6H5-N(CH3)2', 'benzylamine': 'C6H5CH2-NH2', 'p-toluidine': 'p-CH3C6H4-NH2',
          'diphenylamine': '(C6H5)2NH', 'cyclohexylamine': 'C6H11-NH2', 'piperidine': '(CH2)5NH', 'N-ethylethanamine': '(C2H5)2NH', 'tert-butylamine': '(CH3)3C-NH2', 'N-methylpropan-2-amine': '(CH3)2CH-NH-CH3'}
ARYL1 = {'aniline', 'p-toluidine'}
def nclass(name):
    s = AMINES[name]
    if s.endswith('NH2'): return 1
    if 'N(CH3)2' in s or s.endswith(')3N'): return 3
    return 2
PKB = {'aniline': 9.38, 'p-toluidine': 8.92, 'p-anisidine': 8.7, 'p-nitroaniline': 13.0, 'N-methylaniline': 9.3, 'N,N-dimethylaniline': 8.92, 'diphenylamine': 13.2, 'benzylamine': 4.7, 'methylamine': 3.38,
       'dimethylamine': 3.27, 'trimethylamine': 4.22, 'ethylamine': 3.29, 'diethylamine': 3.0, 'triethylamine': 3.25, 'ammonia': 4.75, 'pyridine': 8.75, 'cyclohexylamine': 3.36}
TESTS = {"Hinsberg reagent gives a product soluble in alkali": lambda c: c == 1, "Hinsberg reagent gives an alkali-insoluble product": lambda c: c == 2, "no reaction with Hinsberg reagent": lambda c: c == 3,
         'carbylamine (isocyanide) test is positive': lambda c: c == 1}
PREP = [('Hofmann bromamide degradation', 'RCONH_{2} + Br_{2} + 4NaOH → RNH_{2} (one carbon fewer)'), ('Gabriel phthalimide synthesis', 'phthalimide + KOH, then R–X, then hydrolysis → pure 1° RNH_{2}'),
        ('reduction of nitro compounds', 'ArNO_{2} + Sn/HCl or Fe/HCl → ArNH_{2}'), ('reduction of nitriles', 'RCN + LiAlH_{4} or H_{2}/Ni → RCH_{2}NH_{2} (one carbon more)'), ('ammonolysis of alkyl halides', 'RX + NH_{3} → mixture of 1°, 2°, 3° amines and quaternary salt'),
        ('reduction of amides', 'RCONH_{2} + LiAlH_{4} → RCH_{2}NH_{2}'), ('acetylation of aniline', 'C_{6}H_{5}NH_{2} + (CH_{3}CO)_{2}O → acetanilide')]
AM_F = [('Aniline is a weaker base than ammonia.', True), ('Tertiary amines react with Hinsberg reagent.', False), ('Aliphatic amines are stronger bases than aromatic amines.', True), ('Gabriel synthesis can prepare aniline.', False),
        ('In water, (C_{2}H_{5})_{2}NH is the strongest base among the ethylamines.', True), ('Aniline does not undergo Friedel–Crafts reaction.', True), ('Acetylation lowers the activating effect of –NH_{2}.', True),
        ('Nitration of aniline gives a large amount of m-nitroaniline.', True), ('Primary aliphatic amines give stable diazonium salts at 273 K.', False), ('Benzenesulphonyl chloride is Hinsberg reagent.', True),
        ('Amines are less basic than alcohols.', False), ('The carbylamine test is given by secondary amines.', False), ('Hofmann bromamide gives an amine with one carbon more.', False)]
def g_amine(rng):
    t = rng.choice(['which', 'cnt', 'cnt', 'base', 'prep', 'fact', 'acet', 'n2'])
    if t == 'which':
        tn = rng.choice(list(TESTS)); pos = [n for n in AMINES if TESTS[tn](nclass(n))]; neg = [n for n in AMINES if not TESTS[tn](nclass(n))]
        r = rng.choice(pos); o, a = mcq(rng, r, rng.sample(neg, 3)); return dict(q=f'For which amine: {tn}?', o=o, a=a, sol=[f'{r} ({AMINES[r]}) is a {nclass(r)}° amine.'], p=dict(t=t, tn=tn))
    if t == 'cnt':
        tn = rng.choice(list(TESTS)); pool = rng.sample(list(AMINES), rng.randint(5, 7)); k = sum(1 for n in pool if TESTS[tn](nclass(n)))
        return dict(q=f'How many of these amines satisfy: {tn}? ' + ', '.join(f'{n} ({AMINES[n]})' for n in pool), o=None, a=k, sol=['; '.join(f'{n} {nclass(n)}°' for n in pool) + f' → {k}.'], p=dict(t=t, tn=tn, pool=pool))
    if t == 'base':
        ks = rng.sample(list(PKB), 4); need(min(abs(PKB[a] - PKB[b]) for a, b in itertools.combinations(ks, 2)) >= 0.15); right = sorted(ks, key=PKB.get)
        perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms); o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q='Decreasing basic strength in water:', o=o, a=a, sol=['pK_{b}: ' + ', '.join(f'{k} {PKB[k]}' for k in ks) + ' (lower = stronger).'], p=dict(t=t, ks=ks))
    if t == 'prep':
        n, e = rng.choice(PREP)
        if rng.random() < 0.5: o, a = mcq(rng, e, [x for _, x in PREP if x != e]); return dict(q=f'{n}:', o=o, a=a, sol=[e], p=dict(t='prep', n=n))
        o, a = mcq(rng, n, [x for x, _ in PREP if x != n]); return dict(q=f'{e} is', o=o, a=a, sol=[n], p=dict(t='prep2', n=n))
    if t == 'acet':
        w = rng.choice([1.86, 2.79, 4.65, 9.3, 18.6, 3.72, 6.51]); y = rng.choice([100, 90, 85, 80, 75, 70]); g = w / 93 * 135 * y / 100
        return dict(q=f'{nf(w, 3)} g of aniline is acetylated with {y}% yield. Mass of acetanilide = ____ × 10^{{−2}} g (nearest integer).', o=None, a=round(g * 100), sol=[f'{nf(w, 3)}/93 × 135 × {y}% = {nf(g, 4)} g.'], p=dict(t=t, w=w, y=y))
    if t == 'n2':
        name, f = rng.choice([('methylamine', 'CH5N'), ('ethylamine', 'C2H7N'), ('propylamine', 'C3H9N'), ('butylamine', 'C4H11N')]); w = rng.choice([0.31, 0.45, 0.59, 0.73, 0.9, 1.18, 1.46, 3.1, 4.5])
        v = w / mm(f) * 22400
        return dict(q=f'{nf(w, 3)} g of {name} reacts completely with HNO_{{2}}. Volume of N_{{2}} at STP = ____ mL (nearest integer).', o=None, a=round(v), sol=[f'RNH_{{2}} + HNO_{{2}} → ROH + N_{{2}} + H_{{2}}O; {nf(w, 3)}/{mm(f)} mol × 22400 = {nf(v, 4)} mL.'], p=dict(t=t, w=w, f=f))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in AM_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in AM_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

DZ = [('CuCl/HCl', 'chlorobenzene (Sandmeyer)'), ('CuBr/HBr', 'bromobenzene (Sandmeyer)'), ('CuCN/KCN', 'benzonitrile (Sandmeyer)'), ('Cu powder/HCl', 'chlorobenzene (Gattermann)'), ('KI', 'iodobenzene'),
      ('HBF_{4}, then heat', 'fluorobenzene (Balz–Schiemann)'), ('warm H_{2}O', 'phenol'), ('H_{3}PO_{2} or CH_{3}CH_{2}OH', 'benzene'), ('HBF_{4}, then NaNO_{2}/Cu, heat', 'nitrobenzene'), ('phenol (alkaline)', 'p-hydroxyazobenzene (orange dye)'),
      ('aniline (mildly acidic)', 'p-aminoazobenzene (aniline yellow)'), ('2-naphthol (alkaline)', 'orange-red azo dye (1-phenylazo-2-naphthol)')]
SIG = {'p-OCH_{3}': -0.27, 'p-CH_{3}': -0.17, 'H': 0, 'p-Cl': 0.23, 'p-CN': 0.66, 'p-NO_{2}': 0.78}
DYE = [('phenol', 'C12H10N2O', 'p-hydroxyazobenzene'), ('aniline', 'C12H11N3', 'p-aminoazobenzene'), ('2-naphthol', 'C16H12N2O', '1-phenylazo-2-naphthol'), ('N,N-dimethylaniline', 'C14H15N3', 'p-dimethylaminoazobenzene')]
DZ_F = [('Benzenediazonium chloride is prepared at 273–278 K.', True), ('Aliphatic diazonium salts are stable at room temperature.', False), ('Diazonium coupling with phenol is done in alkaline medium.', True),
        ('Coupling with aniline is done in mildly acidic medium.', True), ('Aryl diazonium salts are stabilised by resonance of the N≡N with the ring.', True), ('Electron-withdrawing groups make the diazonium ion a weaker electrophile.', False),
        ('Azo dyes contain the –N=N– group linking two aromatic rings.', True), ('Diazonium salts are usually stored dry and used later.', False), ('Bromine water converts aniline into 2,4,6-tribromoaniline.', True),
        ('Fluorobenzene is made by the Sandmeyer reaction.', False)]
def g_diaz(rng):
    t = rng.choice(['dz', 'dz2', 'stab', 'dye', 'tba', 'fact'])
    if t == 'dz':
        r, pr = rng.choice(DZ); o, a = mcq(rng, pr, [x for _, x in rng.sample(DZ, 7) if x != pr]); return dict(q=f'Benzenediazonium chloride + {r} gives', o=o, a=a, sol=[f'{r} → {pr}.'], p=dict(t=t, r=r))
    if t == 'dz2':
        r, pr = rng.choice(DZ); o, a = mcq(rng, r, [x for x, _ in rng.sample(DZ, 7) if x != r]); return dict(q=f'To convert benzenediazonium chloride into {pr}, use', o=o, a=a, sol=[f'{r}.'], p=dict(t=t, pr=pr))
    if t == 'stab':
        ks = rng.sample(list(SIG), 4); right = sorted(ks, key=SIG.get); perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms)
        tx = lambda L: ' > '.join(f'{k}–C_{{6}}H_{{4}}N_{{2}}^{{+}}' if k != 'H' else 'C_{6}H_{5}N_{2}^{+}' for k in L); o, a = mcq(rng, tx(right), [tx(p) for p in perms])
        return dict(q='Decreasing stability of these diazonium ions:', o=o, a=a, sol=['Donor groups delocalise the + charge (stabilise); acceptors destabilise.'], p=dict(t=t, ks=ks))
    if t == 'dye':
        cp, f, n = rng.choice(DYE); w = rng.choice([0.93, 1.86, 4.65, 9.3, 2.79, 13.95]); y = rng.choice([100, 90, 80, 75]); g = w / 93 * mm(f) * y / 100
        return dict(q=f'{nf(w, 3)} g of aniline is diazotised and coupled with {cp} ({y}% overall). Mass of {n} = ____ × 10^{{−2}} g (nearest integer).', o=None, a=round(g * 100), sol=[f'{n} M = {mm(f)}; {nf(w, 3)}/93 × {mm(f)} × {y}% = {nf(g, 4)} g.'], p=dict(t=t, w=w, f=f, y=y))
    if t == 'tba':
        w = rng.choice([0.93, 1.86, 4.65, 9.3, 2.79]); k = rng.choice(['br2', 'prod']); g = w / 93 * (480 if k == 'br2' else mm('C6H4Br3N'))
        return dict(q=f'{nf(w, 3)} g of aniline + bromine water. Mass of {"Br_{2} used" if k == "br2" else "2,4,6-tribromoaniline"} = ____ × 10^{{−2}} g (nearest integer).', o=None, a=round(g * 100), sol=[f'C_{{6}}H_{{5}}NH_{{2}} + 3Br_{{2}} → C_{{6}}H_{{2}}Br_{{3}}NH_{{2}} (330) + 3HBr; {nf(g, 4)} g.'], p=dict(t=t, w=w, k=k))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in DZ_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in DZ_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='dfact', want=want))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(amine=g_amine, diaz=g_diaz).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it
def nclass2(name):   # independent: count N–H in the written structure
    s = AMINES[name]; return {2: 1, 1: 2, 0: 3}[2 if 'NH2' in s else 1 if 'NH' in s else 0]
VERD = {"Hinsberg reagent gives a product soluble in alkali": 1, "Hinsberg reagent gives an alkali-insoluble product": 2, "no reaction with Hinsberg reagent": 3, 'carbylamine (isocyanide) test is positive': 1}
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'which': return nclass2(R) == VERD[p['tn']] and all(nclass2(x) != VERD[p['tn']] for x in it['o'] if x != R)
    if t == 'cnt': return R == sum(1 for n in p['pool'] if nclass2(n) == VERD[p['tn']])
    if t == 'base': L = R.split(' > '); return all(PKB[a] < PKB[b] for a, b in zip(L, L[1:]))
    if t == 'prep': return dict(PREP)[p['n']] == R
    if t == 'prep2': return R == p['n']
    if t == 'acet': return abs(R - p['w'] * 135 / 93 * p['y']) <= 0.5 + 1e-9
    if t == 'n2': return R == round(p['w'] * 22400 / mm(p['f']))
    if t == 'fact': return dict(AM_F)[R] == p['want']
    if t == 'dz': return dict(DZ)[p['r']] == R
    if t == 'dz2': return dict(DZ)[R] == p['pr']
    if t == 'stab':
        L = [x.split('–C_')[0] if '–C_' in x else 'H' for x in R.split(' > ')]; return all(SIG[a] < SIG[b] for a, b in zip(L, L[1:]))
    if t == 'dye': return abs(R - p['w'] * mm(p['f']) / 93 * p['y']) <= 0.5 + 1e-9
    if t == 'tba': return R == round(p['w'] * (3 * 160 if p['k'] == 'br2' else 6 * 12 + 4 + 3 * 80 + 14) / 93 * 100)
    if t == 'dfact': return dict(DZ_F)[R] == p['want']
    raise KeyError(t)
