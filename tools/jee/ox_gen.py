"""Practice generators — Chemistry Unit 17: Organic Compounds Containing Oxygen. check() recomputes each answer another
way: test verdicts re-derived from the structure (CH3CO–/CH3CH(OH)– for iodoform, –CHO on sp³ carbon for Fehling,
α-H for aldol/Cannizzaro) using orgkit, alcohol class from the carbinol carbon's neighbours, acidity/reactivity orders
from pKa and reactivity tables, stoichiometry from formula masses."""
import re, itertools
from common import mcq, nf
from orgkit import Mol
def need(x):
    if not x: raise AssertionError('retry')
AM = {'C': 12, 'H': 1, 'N': 14, 'O': 16, 'Br': 80, 'Cl': 35.5}
def mm(f): return sum(AM[e] * (int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f))
def tex(f): return re.sub(r'(\d+)', r'_{\1}', f)
# carbonyl / alcohol bank: name, SMILES
CMP = [('methanal', 'C=O'), ('ethanal', 'CC=O'), ('propanal', 'CCC=O'), ('butanal', 'CCCC=O'), ('2-methylpropanal', 'CC(C)C=O'), ('2,2-dimethylpropanal', 'CC(C)(C)C=O'), ('propanone', 'CC(C)=O'), ('butanone', 'CCC(C)=O'),
       ('pentan-2-one', 'CCCC(C)=O'), ('pentan-3-one', 'CCC(=O)CC'), ('benzaldehyde', 'O=Cc1ccccc1'), ('acetophenone', 'CC(=O)c1ccccc1'), ('benzophenone', 'O=C(c1ccccc1)c1ccccc1'), ('phenylacetaldehyde', 'O=CCc1ccccc1'),
       ('cyclohexanone', 'O=C1CCCCC1'), ('cyclohexanecarbaldehyde', 'O=CC1CCCCC1'), ('ethanol', 'CCO'), ('methanol', 'CO'), ('propan-2-ol', 'CC(C)O'), ('butan-2-ol', 'CCC(C)O'), ('propan-1-ol', 'CCCO'),
       ('pentan-3-ol', 'CCC(O)CC'), ('1-phenylethanol', 'CC(O)c1ccccc1'), ('2-methylpropan-2-ol', 'CC(C)(C)O'), ('acetic acid', 'CC(=O)O'), ('formic acid', 'O=CO'), ('4-methylbenzaldehyde', 'Cc1ccc(C=O)cc1'), ('3-methylbutan-2-one', 'CC(C)C(C)=O'), ('butan-1-ol', 'CCCCO'), ('2-methylbutan-2-ol', 'CCC(C)(C)O'), ('cyclohexanol', 'OC1CCCCC1'), ('benzyl alcohol', 'OCc1ccccc1'), ('pentan-2-ol', 'CCCC(C)O'), ('2-methylpropan-1-ol', 'CC(C)CO'), ('3-methylbutan-2-ol', 'CC(C)C(C)O')]
def info(s):
    m = Mol(s); out = dict(ald=False, ket=False, acid=False, alc=None, iodo=False, aH=False, aldarom=False, formic=s == 'O=CO')
    for i, e in enumerate(m.a):
        if e != 'O': continue
        (c, o), = m.nb[i]
        cn = [j for j, _ in m.nb[c] if j != i]
        if o == 2:
            if any(m.a[j] == 'O' for j in cn): out['acid'] = True; continue
            if m.h[c] >= 1: out['ald'] = True; out['aldarom'] = any(m.a[j] == 'c' for j in cn)
            else: out['ket'] = True
            if any(m.a[j] == 'C' and m.h[j] >= 1 for j in cn if m.a[j] in ('C',)): out['aH'] = True
            if any(m.a[j] == 'C' and m.h[j] == 3 for j in cn): out['iodo'] = True
            if s == 'CC=O': out['iodo'] = True
        elif o == 1 and m.h[i] == 1 and m.a[c] == 'C' and not any(oo == 2 for _, oo in m.nb[c]):
            out['alc'] = sum(1 for j in cn if m.a[j] in ('C', 'c'))
            if any(m.a[j] == 'C' and m.h[j] == 3 for j in cn) and m.h[c] >= 1: out['iodo'] = True
    return out
TESTS = {'iodoform (I_{2}/NaOH)': lambda f: f['iodo'], "Tollens' reagent": lambda f: f['ald'] or f['formic'], "Fehling's solution": lambda f: (f['ald'] and not f['aldarom']) or f['formic'],
         'aldol condensation (dil. NaOH)': lambda f: (f['ald'] or f['ket']) and f['aH'], 'Cannizzaro reaction (conc. NaOH)': lambda f: f['ald'] and not f['aH'], '2,4-DNP (orange precipitate)': lambda f: f['ald'] or f['ket']}
NUC = {'methanal': 6, 'ethanal': 5, 'propanal': 4.5, 'benzaldehyde': 3, 'propanone': 2.5, 'butanone': 2, 'acetophenone': 1.5, 'benzophenone': 1, 'trichloroethanal': 7, '4-nitrobenzaldehyde': 3.6, '4-methylbenzaldehyde': 2.7, 'di-tert-butyl ketone': 0.5}
NR = [('Rosenmund reduction', 'RCOCl + H_{2}/Pd–BaSO_{4} → RCHO'), ('Stephen reaction', 'RCN + SnCl_{2}/HCl, then H_{3}O^{+} → RCHO'), ('Etard reaction', 'toluene + CrO_{2}Cl_{2}/CS_{2} → benzaldehyde'), ('Gattermann–Koch reaction', 'benzene + CO/HCl (AlCl_{3}/CuCl) → benzaldehyde'),
      ('Clemmensen reduction', 'C=O + Zn-Hg/conc. HCl → CH_{2}'), ('Wolff–Kishner reduction', 'C=O + NH_{2}NH_{2}, KOH/glycol, heat → CH_{2}'), ('Cannizzaro reaction', '2 ArCHO + conc. NaOH → ArCOO^{−} + ArCH_{2}OH'),
      ('Hell–Volhard–Zelinsky reaction', 'RCH_{2}COOH + X_{2}/red P → RCHXCOOH'), ('Kolbe reaction', 'sodium phenoxide + CO_{2}, then H^{+} → salicylic acid'), ('Reimer–Tiemann reaction', 'phenol + CHCl_{3}/NaOH → salicylaldehyde'),
      ('Williamson synthesis', 'RONa + R′X → R–O–R′'), ('Claisen–Schmidt condensation', 'ArCHO + CH_{3}COR (dil. NaOH) → ArCH=CHCOR')]
def g_carb(rng):
    t = rng.choice(['which', 'cnt', 'cnt', 'nuc', 'nr', 'nr2', 'cs', 'cross'])
    if t == 'which':
        tn = rng.choice(list(TESTS)); want = rng.choice([True, False]); pool = [(n, s) for n, s in CMP if TESTS[tn](info(s)) == want]; other = [(n, s) for n, s in CMP if TESTS[tn](info(s)) != want]; need(len(other) >= 3)
        r = rng.choice(pool); o, a = mcq(rng, r[0], [n for n, _ in rng.sample(other, 3)])
        return dict(q=f'Which of these {"gives" if want else "does NOT give"} a positive {tn}?', o=o, a=a, sol=[f'{r[0]}: {"yes" if want else "no"}; the others are the opposite.'], p=dict(t=t, tn=tn, want=want))
    if t == 'cnt':
        tn = rng.choice(list(TESTS)); pool = rng.sample(CMP, rng.randint(5, 7)); k = sum(1 for _, s in pool if TESTS[tn](info(s)))
        return dict(q=f'How many of these give a positive {tn}? ' + ', '.join(n for n, _ in pool), o=None, a=k, sol=['; '.join(f'{n} {"✓" if TESTS[tn](info(s)) else "✗"}' for n, s in pool) + f' → {k}.'], p=dict(t=t, tn=tn, names=[n for n, _ in pool]))
    if t == 'nuc':
        ks = rng.sample(list(NUC), 4); need(len({NUC[k] for k in ks}) == 4); up = rng.choice([True, False]); right = sorted(ks, key=lambda k: NUC[k] if up else -NUC[k])
        perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms); sep = ' < ' if up else ' > '
        o, a = mcq(rng, sep.join(right), [sep.join(p) for p in perms])
        return dict(q=f'{"Increasing" if up else "Decreasing"} reactivity towards nucleophilic addition:', o=o, a=a, sol=['Fewer/smaller groups and electron-withdrawing groups on the C=O raise reactivity: aldehydes > ketones; aryl groups (resonance) and bulk lower it.'], p=dict(t=t, ks=ks, up=up))
    if t in ('nr', 'nr2'):
        n, e = rng.choice(NR)
        if t == 'nr': o, a = mcq(rng, e, [x for _, x in rng.sample(NR, 6) if x != e]); return dict(q=f'The {n} is', o=o, a=a, sol=[f'{n}: {e}.'], p=dict(t=t, n=n))
        o, a = mcq(rng, n, [x for x, _ in rng.sample(NR, 6) if x != n]); return dict(q=f'{e} is called', o=o, a=a, sol=[f'{n}.'], p=dict(t=t, n=n))
    if t == 'cs':
        w = rng.choice([1.06, 2.12, 5.3, 10.6, 21.2, 3.18]); y = rng.choice([100, 90, 80, 75, 60, 50]); g = w / mm('C7H6O') / 2 * mm('C17H14O') * y / 100
        return dict(q=f'{nf(w, 3)} g of benzaldehyde gives dibenzalacetone (2 PhCHO + acetone) in {y}% yield. Mass of product = ____ × 10^{{−2}} g (nearest integer).', o=None, a=round(g * 100),
                    sol=[f'{nf(w, 3)}/106 mol PhCHO → half as much product (M 234) × {y}% = {nf(g, 4)} g.'], p=dict(t=t, w=w, y=y))
    a1, a2 = rng.sample([c for c in CMP if info(c[1])['ald'] or info(c[1])['ket']], 2); f1, f2 = info(a1[1]), info(a2[1])
    k = sum(1 for d, acc in ((f1, f1), (f1, f2), (f2, f1), (f2, f2)) if d['aH'])
    return dict(q=f'A mixture of {a1[0]} and {a2[0]} is treated with dilute NaOH. Maximum number of aldol (β-hydroxy carbonyl) products, ignoring stereoisomers, = ____.', o=None, a=k,
                sol=['Each compound with α-H can act as donor (enolate); every carbonyl can be an acceptor.', f'Donors × acceptors = {k}.'], p=dict(t='cross', s1=a1[1], s2=a2[1]))

PKA = {'phenol': 10.0, 'p-nitrophenol': 7.15, 'o-nitrophenol': 7.23, 'm-nitrophenol': 8.4, 'p-cresol': 10.3, 'm-cresol': 10.1, 'p-methoxyphenol': 10.2, '2,4,6-trinitrophenol': 0.4, 'ethanol': 15.9, 'methanol': 15.5, 'water': 15.7, '2-methylpropan-2-ol': 18, 'p-chlorophenol': 9.4, '2,4-dinitrophenol': 4.1}
ETH = [('anisole + HI', 'phenol + CH_{3}I'), ('ethyl methyl ether + HI (cold, 1 eq.)', 'CH_{3}I + ethanol'), ('tert-butyl methyl ether + HI', 'tert-butyl iodide + methanol'), ('diethyl ether + excess HI, heat', '2 ethyl iodide'), ('benzyl phenyl ether + HI', 'phenol + benzyl iodide')]
ALC_F = [('Phenol is more acidic than ethanol because phenoxide is resonance-stabilised.', True), ('Tertiary alcohols give immediate turbidity with Lucas reagent.', True), ('Primary alcohols are oxidised by PCC to aldehydes.', True),
         ('Tertiary alcohols are easily oxidised to ketones.', False), ('Ethers are cleaved by HI more readily than by HCl.', True), ('Phenol undergoes nitration only with conc. HNO_{3}/H_{2}SO_{4}.', False), ('Bromine water converts phenol to 2,4,6-tribromophenol.', True),
         ('o-Nitrophenol is steam volatile because of intramolecular H-bonding.', True), ('Alcohols are more acidic than water in the gas phase and in solution alike.', False), ('Dehydration of alcohols is easiest for 3° alcohols.', True),
         ('Williamson synthesis works well with tertiary alkyl halides.', False), ('Phenol gives a violet colour with neutral FeCl_{3}.', True), ('Phenol is converted to benzene by heating with zinc dust.', True), ('Ethanol gives the iodoform test.', True),
         ('Methanol gives the iodoform test.', False), ('Electron-withdrawing groups decrease the acidity of phenol.', False)]
def g_alc(rng):
    t = rng.choice(['acid', 'cls', 'ox', 'eth', 'fact', 'br', 'acid', 'acid', 'br'])
    if t == 'acid':
        ks = rng.sample(list(PKA), 4); need(min(abs(PKA[a] - PKA[b]) for a, b in itertools.combinations(ks, 2)) >= 0.2); right = sorted(ks, key=PKA.get)
        perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms); o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q='Decreasing acidic strength:', o=o, a=a, sol=['pKa: ' + ', '.join(f'{k} {PKA[k]}' for k in ks) + '.'], p=dict(t=t, ks=ks))
    if t in ('cls', 'ox'):
        al = [(n, s) for n, s in CMP if info(s)['alc'] is not None]; n, s = rng.choice(al); d = info(s)['alc']; cls = {0: 'primary', 1: 'primary', 2: 'secondary', 3: 'tertiary'}[d]
        if t == 'cls':
            r = {'primary': 'no turbidity at room temperature (only on heating)', 'secondary': 'turbidity in about 5 minutes', 'tertiary': 'turbidity immediately'}[cls]
            o, a = mcq(rng, r, ['no turbidity at room temperature (only on heating)', 'turbidity in about 5 minutes', 'turbidity immediately', 'a violet colour'])
            return dict(q=f'With Lucas reagent (conc. HCl + ZnCl_{{2}}), {n} gives', o=o, a=a, sol=[f'{n} is a {cls} alcohol.'], p=dict(t=t, s=s))
        r = {'primary': 'an aldehyde (then an acid)', 'secondary': 'a ketone', 'tertiary': 'no oxidation under mild conditions'}[cls]
        o, a = mcq(rng, r, ['an aldehyde (then an acid)', 'a ketone', 'no oxidation under mild conditions', 'an ether'])
        return dict(q=f'Oxidation of {n} with acidified K_{{2}}Cr_{{2}}O_{{7}} gives', o=o, a=a, sol=[f'{n} is {cls}.'], p=dict(t='ox', s=s))
    if t == 'eth':
        r, pr = rng.choice(ETH); o, a = mcq(rng, pr, [x for _, x in ETH if x != pr]); return dict(q=f'{r} gives', o=o, a=a, sol=['The halide goes to the smaller alkyl (S_{N}2) or to the group giving the stable carbocation (S_{N}1); aryl–O is never cleaved.'], p=dict(t=t, r=r))
    if t == 'br':
        w = rng.choice([0.94, 1.88, 2.35, 4.7, 9.4, 3.76]); g = w / 94 * 3 * 160 if rng.random() < 0.5 else None
        if g is not None: return dict(q=f'Mass of Br_{{2}} (g, ×10^{{−2}}, nearest integer) needed to convert {nf(w, 3)} g phenol to 2,4,6-tribromophenol = ____.', o=None, a=round(g * 100), sol=[f'3 Br_{{2}} per phenol: {nf(w, 3)}/94 × 3 × 160 = {nf(g, 4)} g.'], p=dict(t='br', w=w, k='br2'))
        g = w / 94 * mm('C6H3Br3O'); return dict(q=f'Mass of 2,4,6-tribromophenol (g, ×10^{{−2}}, nearest integer) from {nf(w, 3)} g phenol (complete reaction) = ____.', o=None, a=round(g * 100), sol=[f'{nf(w, 3)}/94 × 331 = {nf(g, 4)} g.'], p=dict(t='br', w=w, k='prod'))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in ALC_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in ALC_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

AC = {'HCOOH': 3.75, 'CH_{3}COOH': 4.76, 'CH_{3}CH_{2}COOH': 4.87, 'ClCH_{2}COOH': 2.86, 'Cl_{2}CHCOOH': 1.29, 'Cl_{3}CCOOH': 0.65, 'FCH_{2}COOH': 2.59, 'C_{6}H_{5}COOH': 4.20, 'p-NO_{2}C_{6}H_{4}COOH': 3.41,
      'p-CH_{3}OC_{6}H_{4}COOH': 4.46, 'C_{6}H_{5}CH_{2}COOH': 4.31, 'CF_{3}COOH': 0.23, 'BrCH_{2}COOH': 2.90, 'CH_{3}CHClCOOH': 2.83, 'ClCH_{2}CH_{2}COOH': 4.08}
ACID_F = [('HVZ reaction halogenates the α-carbon of carboxylic acids.', True), ('Carboxylic acids give the iodoform test.', False), ('Carboxylic acids dimerise through hydrogen bonds in the vapour/aprotic solvents.', True),
          ('Formic acid reduces Tollens reagent.', True), ('Decarboxylation of RCOONa with soda lime gives an alkane with one carbon less.', True), ('LiAlH_{4} reduces RCOOH to RCH_{2}OH.', True),
          ('Benzoic acid undergoes Friedel–Crafts reaction readily.', False), ('Electron-withdrawing groups increase the acidity of carboxylic acids.', True), ('Carboxylic acids are weaker acids than phenols.', False),
          ('Kolbe electrolysis of sodium acetate gives ethane.', True), ('RMgX + CO_{2} followed by acid gives RCOOH.', True), ('Carboxylic acids react with NaHCO_{3} to liberate CO_{2}.', True)]
GR = [('CH_{3}MgBr', 'CH_{3}COOH', 'C2H4O2'), ('C_{2}H_{5}MgBr', 'CH_{3}CH_{2}COOH', 'C3H6O2'), ('C_{6}H_{5}MgBr', 'C_{6}H_{5}COOH', 'C7H6O2'), ('C_{6}H_{5}CH_{2}MgCl', 'C_{6}H_{5}CH_{2}COOH', 'C8H8O2'), ('(CH_{3})_{2}CHMgBr', '(CH_{3})_{2}CHCOOH', 'C4H8O2')]
def g_acid(rng):
    t = rng.choice(['ord', 'ord', 'gr', 'dec', 'fact'])
    if t == 'ord':
        ks = rng.sample(list(AC), 4); need(min(abs(AC[a] - AC[b]) for a, b in itertools.combinations(ks, 2)) >= 0.08); right = sorted(ks, key=AC.get)
        perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms); o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q='Decreasing acid strength:', o=o, a=a, sol=['pKa: ' + ', '.join(f'{k} {AC[k]}' for k in ks) + ' (lower pKa = stronger).'], p=dict(t=t, ks=ks))
    if t == 'gr':
        g, prod, f = rng.choice(GR); n = rng.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1.5, 2.0])
        return dict(q=f'{n} mol of {g} is treated with dry ice, then H_{{3}}O^{{+}}. Mass of {prod} formed = ____ × 10^{{−1}} g (nearest integer).', o=None, a=round(n * mm(f) * 10), sol=[f'RMgX + CO_{{2}} → RCOOH; {n} × {mm(f)} = {nf(n * mm(f), 4)} g.'], p=dict(t=t, n=n, f=f))
    if t == 'dec':
        k = rng.randint(2, 6); names = {1: 'methane', 2: 'ethane', 3: 'propane', 4: 'butane', 5: 'pentane'}; sal = f'C_{{{k - 1}}}H_{{{2 * k - 1}}}COONa' if k > 2 else 'CH_{3}COONa'
        o, a = mcq(rng, names[k - 1], [names[x] for x in names if x != k - 1])
        return dict(q=f'Heating {sal} with soda lime (NaOH + CaO) gives', o=o, a=a, sol=['RCOONa + NaOH → R–H + Na_{2}CO_{3}: one carbon fewer.'], p=dict(t=t, k=k))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in ACID_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in ACID_F if v != want], 3))
    return dict(q=f'Which statement about carboxylic acids is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='afact', want=want))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(carb=g_carb, alc=g_alc, acid=g_acid).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it
# ---- independent verdicts by name patterns (textbook rules written separately)
V = {'methanal': dict(ald=1, aH=0, ar=0, me=0), 'ethanal': dict(ald=1, aH=1, ar=0, me=1), 'propanal': dict(ald=1, aH=1, ar=0, me=0), 'butanal': dict(ald=1, aH=1, ar=0, me=0), '2-methylpropanal': dict(ald=1, aH=1, ar=0, me=0),
     '2,2-dimethylpropanal': dict(ald=1, aH=0, ar=0, me=0), 'propanone': dict(ket=1, aH=1, me=1), 'butanone': dict(ket=1, aH=1, me=1), 'pentan-2-one': dict(ket=1, aH=1, me=1), 'pentan-3-one': dict(ket=1, aH=1, me=0),
     'benzaldehyde': dict(ald=1, aH=0, ar=1, me=0), 'acetophenone': dict(ket=1, aH=1, me=1), 'benzophenone': dict(ket=1, aH=0, me=0), 'phenylacetaldehyde': dict(ald=1, aH=1, ar=0, me=0), 'cyclohexanone': dict(ket=1, aH=1, me=0),
     'cyclohexanecarbaldehyde': dict(ald=1, aH=1, ar=0, me=0), 'ethanol': dict(me=1), 'methanol': dict(me=0), 'propan-2-ol': dict(me=1), 'butan-2-ol': dict(me=1), 'propan-1-ol': dict(me=0), 'pentan-3-ol': dict(me=0),
     '1-phenylethanol': dict(me=1), '2-methylpropan-2-ol': dict(me=0), 'acetic acid': dict(me=0), 'formic acid': dict(formic=1), '4-methylbenzaldehyde': dict(ald=1, aH=0, ar=1, me=0), '3-methylbutan-2-one': dict(ket=1, aH=1, me=1), 'butan-1-ol': dict(me=0), '2-methylbutan-2-ol': dict(me=0), 'cyclohexanol': dict(me=0), 'benzyl alcohol': dict(me=0), 'pentan-2-ol': dict(me=1), '2-methylpropan-1-ol': dict(me=0), '3-methylbutan-2-ol': dict(me=1)}
def verdict(tn, n):
    v = V[n]; ald, ket, aH, ar, me, fo = v.get('ald', 0), v.get('ket', 0), v.get('aH', 0), v.get('ar', 0), v.get('me', 0), v.get('formic', 0)
    return {'iodoform (I_{2}/NaOH)': me, "Tollens' reagent": ald or fo, "Fehling's solution": (ald and not ar) or fo, 'aldol condensation (dil. NaOH)': (ald or ket) and aH,
            'Cannizzaro reaction (conc. NaOH)': ald and not aH, '2,4-DNP (orange precipitate)': ald or ket}[tn]
ALCLS = {'ethanol': 'primary', 'methanol': 'primary', 'propan-2-ol': 'secondary', 'butan-2-ol': 'secondary', 'propan-1-ol': 'primary', 'pentan-3-ol': 'secondary', '1-phenylethanol': 'secondary', '2-methylpropan-2-ol': 'tertiary', 'butan-1-ol': 'primary', '2-methylbutan-2-ol': 'tertiary', 'cyclohexanol': 'secondary', 'benzyl alcohol': 'primary', 'pentan-2-ol': 'secondary', '2-methylpropan-1-ol': 'primary', '3-methylbutan-2-ol': 'secondary'}
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'which': return bool(verdict(p['tn'], R)) == p['want'] and all(bool(verdict(p['tn'], x)) != p['want'] for x in it['o'] if x != R)
    if t == 'cnt': return R == sum(1 for n in p['names'] if verdict(p['tn'], n))
    if t == 'nuc': L = re.split(r' [<>] ', R); return all((NUC[a] < NUC[b]) if p['up'] else (NUC[a] > NUC[b]) for a, b in zip(L, L[1:]))
    if t == 'nr': return dict(NR)[p['n']] == R
    if t == 'nr2': return R == p['n']
    if t == 'cs': return R == round(p['w'] * 234 / 212 * p['y'])
    if t == 'cross':
        n1 = next(n for n, s in CMP if s == p['s1']); n2 = next(n for n, s in CMP if s == p['s2']); return R == 2 * (V[n1].get('aH', 0) + V[n2].get('aH', 0))
    if t == 'acid': L = R.split(' > '); return all(PKA[a] < PKA[b] for a, b in zip(L, L[1:]))
    if t in ('cls', 'ox'):
        n = next(n for n, s in CMP if s == p['s']); c = ALCLS[n]
        return R == ({'primary': 'no turbidity at room temperature (only on heating)', 'secondary': 'turbidity in about 5 minutes', 'tertiary': 'turbidity immediately'} if t == 'cls' else {'primary': 'an aldehyde (then an acid)', 'secondary': 'a ketone', 'tertiary': 'no oxidation under mild conditions'})[c]
    if t == 'eth': return dict(ETH)[p['r']] == R
    if t == 'br': return R == round(p['w'] / 94 * (480 if p['k'] == 'br2' else 331) * 100)
    if t == 'fact': return dict(ALC_F)[R] == p['want']
    if t == 'ord': L = R.split(' > '); return all(AC[a] < AC[b] for a, b in zip(L, L[1:]))
    if t == 'gr': return R == round(p['n'] * mm(p['f']) * 10)
    if t == 'dec': return R == {1: 'methane', 2: 'ethane', 3: 'propane', 4: 'butane', 5: 'pentane'}[p['k'] - 1]
    if t == 'afact': return dict(ACID_F)[R] == p['want']
    raise KeyError(t)
