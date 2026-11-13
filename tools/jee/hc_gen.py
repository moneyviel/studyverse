"""Practice generators — Chemistry Unit 15: Hydrocarbons. check() recomputes each answer another way: combustion by
balancing C, H and O atoms one at a time, ozonolysis and HBr addition by editing the SMILES-lite structure and
comparing canonical forms (orgkit), monochloride counts from hydrogen environments, Wurtz products by pairing
alkyl groups, EAS orientation from a directing-group table, masses from formulae."""
import re, itertools
from common import mcq, nf
from orgkit import Mol, canon
def need(x):
    if not x: raise AssertionError('retry')
AM = {'C': 12, 'H': 1, 'N': 14, 'O': 16, 'Br': 80, 'Cl': 35.5, 'S': 32}
def mm(f): return sum(AM[e] * (int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f))
def ftex(f): return re.sub(r'(\d+)', r'_{\1}', f)
# alkenes: name, SMILES, ozonolysis products (names), Markovnikov HBr product, anti-Markovnikov (peroxide) product
ALKENE = [('propene', 'C=CC', ['methanal', 'ethanal'], ('2-bromopropane', 'CC(Br)C'), ('1-bromopropane', 'BrCCC')),
          ('but-1-ene', 'C=CCC', ['methanal', 'propanal'], ('2-bromobutane', 'CC(Br)CC'), ('1-bromobutane', 'BrCCCC')),
          ('but-2-ene', 'CC=CC', ['ethanal', 'ethanal'], ('2-bromobutane', 'CC(Br)CC'), ('2-bromobutane', 'CC(Br)CC')),
          ('2-methylpropene', 'C=C(C)C', ['methanal', 'propanone'], ('2-bromo-2-methylpropane', 'CC(C)(C)Br'), ('1-bromo-2-methylpropane', 'BrCC(C)C')),
          ('2-methylbut-2-ene', 'CC=C(C)C', ['ethanal', 'propanone'], ('2-bromo-2-methylbutane', 'CCC(C)(C)Br'), ('2-bromo-3-methylbutane', 'CC(Br)C(C)C')),
          ('pent-1-ene', 'C=CCCC', ['methanal', 'butanal'], ('2-bromopentane', 'CC(Br)CCC'), ('1-bromopentane', 'BrCCCCC')),
          ('pent-2-ene', 'CC=CCC', ['ethanal', 'propanal'], ('2-bromopentane + 3-bromopentane', None), ('2-bromopentane + 3-bromopentane', None)),
          ('2-methylbut-1-ene', 'C=C(C)CC', ['methanal', 'butanone'], ('2-bromo-2-methylbutane', 'CCC(C)(C)Br'), ('1-bromo-2-methylbutane', 'BrCC(C)CC')),
          ('3-methylbut-1-ene', 'C=CC(C)C', ['methanal', '2-methylpropanal'], ('2-bromo-3-methylbutane', 'CC(Br)C(C)C'), ('1-bromo-3-methylbutane', 'BrCCC(C)C')),
          ('2,3-dimethylbut-2-ene', 'CC(C)=C(C)C', ['propanone', 'propanone'], ('2-bromo-2,3-dimethylbutane', 'CC(C)C(C)(C)Br'), ('2-bromo-2,3-dimethylbutane', 'CC(C)C(C)(C)Br')),
          ('hex-3-ene', 'CCC=CCC', ['propanal', 'propanal'], ('3-bromohexane', 'CCC(Br)CCC'), ('3-bromohexane', 'CCC(Br)CCC')),
          ('cyclohexene', 'C1=CCCCC1', ['hexanedial'], ('bromocyclohexane', 'BrC1CCCCC1'), ('bromocyclohexane', 'BrC1CCCCC1')),
          ('1-methylcyclohexene', 'CC1=CCCCC1', ['6-oxoheptanal'], ('1-bromo-1-methylcyclohexane', 'CC1(Br)CCCCC1'), ('1-bromo-2-methylcyclohexane', 'CC1CCCCC1Br')),
          ('styrene', 'C=Cc1ccccc1', ['methanal', 'benzaldehyde'], ('1-bromo-1-phenylethane', 'CC(Br)c1ccccc1'), ('1-bromo-2-phenylethane', 'BrCCc1ccccc1'))]
CARB = {'methanal': 'C=O', 'ethanal': 'CC=O', 'propanal': 'CCC=O', 'butanal': 'CCCC=O', 'propanone': 'CC(C)=O', 'butanone': 'CCC(C)=O', '2-methylpropanal': 'CC(C)C=O', 'benzaldehyde': 'O=Cc1ccccc1',
        'hexanedial': 'O=CCCCCC=O', '6-oxoheptanal': 'CC(=O)CCCCC=O'}
ALKANE = [('ethane', 'CC'), ('propane', 'CCC'), ('butane', 'CCCC'), ('2-methylpropane', 'CC(C)C'), ('pentane', 'CCCCC'), ('2-methylbutane', 'CC(C)CC'), ('2,2-dimethylpropane', 'CC(C)(C)C'), ('hexane', 'CCCCCC'),
          ('2-methylpentane', 'CC(C)CCC'), ('3-methylpentane', 'CCC(C)CC'), ('2,2-dimethylbutane', 'CC(C)(C)CC'), ('2,3-dimethylbutane', 'CC(C)C(C)C'), ('cyclohexane', 'C1CCCCC1'), ('methylcyclohexane', 'CC1CCCCC1'), ('2,2,4-trimethylpentane', 'CC(C)(C)CC(C)C')]
RX = {'CH_{3}Br': 'CH3', 'C_{2}H_{5}Br': 'C2H5', 'n-C_{3}H_{7}Br': 'nPr', '(CH_{3})_{2}CHBr': 'iPr', 'n-C_{4}H_{9}Br': 'nBu'}
ALKY = {'CH3': 'C', 'C2H5': 'CC', 'nPr': 'CCC', 'iPr': 'CC(C)', 'nBu': 'CCCC'}      # written so the joining atom is the LAST one
ALKF = {'CH3': 'C', 'C2H5': 'CC', 'nPr': 'CCC', 'iPr': 'C(C)C', 'nBu': 'CCCC'}      # … and here the FIRST one
ALK_F = [('Lindlar catalyst (Pd/BaSO_{4}, quinoline) reduces alkynes to cis-alkenes.', True), ('Na in liquid NH_{3} reduces alkynes to trans-alkenes.', True), ('Ethyne is more acidic than ethene and ethane.', True),
         ('Alkenes give ozonides that are reduced by Zn/H_{2}O to carbonyl compounds.', True), ("Baeyer's reagent is cold dilute alkaline KMnO_{4}.", True), ('Peroxide effect is shown by HCl and HI as well as HBr.', False),
         ('Staggered ethane is more stable than eclipsed ethane.', True), ('Kolbe electrolysis of sodium ethanoate gives methane.', False), ('Decarboxylation of sodium propanoate with soda lime gives ethane.', True),
         ('Wurtz reaction is suitable for alkanes with an odd number of carbons from two different halides.', False), ('Alkynes react with water in presence of Hg^{2+}/H^{+} to give carbonyl compounds.', True),
         ('Branched alkanes have higher boiling points than their straight-chain isomers.', False), ('The C–C bond length order is C≡C < C=C < C–C.', True), ('Propyne gives a white precipitate with ammoniacal AgNO_{3}.', True),
         ('But-2-yne gives a precipitate with ammoniacal AgNO_{3}.', False), ('Cis-alkenes are more stable than trans-alkenes.', False), ('Alkanes are cracked (pyrolysed) into smaller alkanes and alkenes on strong heating.', True)]
def g_alk(rng):
    t = rng.choice(['comb', 'combn', 'ozo', 'hbr', 'hbrp', 'mono', 'wurtz', 'fact', 'fact'])
    if t in ('comb', 'combn'):
        kind = rng.choice(['alkane', 'alkene', 'alkyne']); n = rng.randint(1 if kind == 'alkane' else 2, 9); h = {'alkane': 2 * n + 2, 'alkene': 2 * n, 'alkyne': 2 * n - 2}[kind]; o2 = n + h / 4
        if t == 'comb':
            need(o2 == int(o2)); return dict(q=f'Moles of O_{{2}} needed to burn 1 mol of C_{{{n}}}H_{{{h}}} completely = ____.', o=None, a=int(o2), sol=[f'C_{{{n}}}H_{{{h}}} + {nf(o2, 3)} O_{{2}} → {n} CO_{{2}} + {h // 2} H_{{2}}O.'], p=dict(t=t, n=n, h=h))
        need(o2 == int(o2)); return dict(q=f'One mole of an {kind} needs {int(o2)} mol O_{{2}} for complete combustion. The number of carbon atoms in it is ____.', o=None, a=n, sol=[f'C_{{n}}H_{{{"2n+2" if kind == "alkane" else "2n" if kind == "alkene" else "2n−2"}}} needs n + H/4 mol O_{{2}} → n = {n}.'], p=dict(t=t, kind=kind, o2=int(o2)))
    if t == 'ozo':
        n, s, prods, _, _ = rng.choice(ALKENE); right = ' + '.join(sorted(prods)); pool = sorted({' + '.join(sorted(x[2])) for x in ALKENE} - {right}); o, a = mcq(rng, right, rng.sample(pool, 3))
        return dict(q=f'Ozonolysis of {n} followed by Zn/H_{{2}}O gives', o=o, a=a, sol=[f'Cut each C=C and put =O on both carbons: {right}.'], p=dict(t=t, s=s))
    if t in ('hbr', 'hbrp'):
        rows = [x for x in ALKENE if (x[3] if t == 'hbr' else x[4])[1]]; n, s, _, mk, am = rng.choice(rows); r = (mk if t == 'hbr' else am)[0]
        pool = sorted({x[3][0] for x in ALKENE} | {x[4][0] for x in ALKENE} - {r}); o, a = mcq(rng, r, rng.sample([x for x in pool if x != r], 3))
        return dict(q=f'The major product of {n} + HBr{" in the presence of benzoyl peroxide" if t == "hbrp" else ""} is', o=o, a=a,
                    sol=[('Markovnikov: H goes to the carbon with more H; Br to the carbon giving the more stable carbocation.' if t == 'hbr' else 'Peroxide effect (only HBr): Br^{•} adds first to give the more stable radical → Br on the carbon with more H.'), f'→ {r}.'], p=dict(t=t, s=s))
    if t == 'mono':
        n, s = rng.choice(ALKANE); k = Mol(s).h_classes()
        return dict(q=f'The number of structurally different monochloro products of {n} (Cl_{{2}}, hν) is ____.', o=None, a=k, sol=[f'{n} has {k} kind(s) of hydrogen.'], p=dict(t=t, s=s))
    if t == 'wurtz':
        a1, a2 = rng.sample(list(RX), 2); prods = {canon(Mol(ALKY[RX[x]] + ALKF[RX[y]])) for x in (a1, a2) for y in (a1, a2)}
        return dict(q=f'A mixture of {a1} and {a2} is treated with Na in dry ether (Wurtz). The number of different alkanes formed is ____.', o=None, a=len(prods), sol=['R–R, R′–R′ and R–R′ form; identical ones count once.', f'→ {len(prods)}.'], p=dict(t=t, a1=a1, a2=a2))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in ALK_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in ALK_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

GRP = {'–CH_{3}': ('op', 1), '–OH': ('op', 3), '–NH_{2}': ('op', 3), '–OCH_{3}': ('op', 2), '–NHCOCH_{3}': ('op', 1.5), '–Cl': ('op', -0.5), '–Br': ('op', -0.6), '–C_{2}H_{5}': ('op', 1.1),
       '–NO_{2}': ('m', -3), '–CN': ('m', -2.5), '–CHO': ('m', -1.8), '–COOH': ('m', -1.9), '–COCH_{3}': ('m', -1.7), '–SO_{3}H': ('m', -2.4), '–N^{+}(CH_{3})_{3}': ('m', -3.2)}
EAS = [('nitration (conc. HNO_{3}/H_{2}SO_{4})', 'NO2'), ('bromination (Br_{2}/FeBr_{3})', 'Br'), ('sulphonation (fuming H_{2}SO_{4})', 'SO3H'), ('Friedel–Crafts acylation (CH_{3}COCl/AlCl_{3})', 'COCH3')]
ARO_F = [('The electrophile in nitration is NO_{2}^{+}.', True), ('The electrophile in sulphonation is SO_{3}.', True), ('Friedel–Crafts reactions fail on nitrobenzene.', True), ('Aniline gives Friedel–Crafts alkylation easily.', False),
         ('Benzene prefers substitution over addition to keep its aromaticity.', True), ('Benzene adds Cl_{2} in sunlight to give C_{6}H_{6}Cl_{6}.', True), ('Benzene decolourises bromine water.', False),
         ('Halogens deactivate the ring but direct o/p.', True), ('–NO_{2} activates the ring for electrophilic substitution.', False), ('Polynuclear hydrocarbons such as benzpyrene are carcinogenic.', True),
         ('Benzene is formed by passing ethyne through a red-hot iron tube.', True), ('Phenol is converted to benzene by heating with zinc dust.', True), ('Sodium benzoate with soda lime gives benzene.', True),
         ('In Friedel–Crafts alkylation the product is less reactive than benzene.', False), ('The σ-complex (arenium ion) is aromatic.', False)]
def g_aro(rng):
    t = rng.choice(['dir', 'act', 'prod', 'mass', 'fact', 'fact', 'prod'])
    if t == 'dir':
        g = rng.choice(list(GRP)); d = GRP[g][0]; lab = {'op': 'ortho and para', 'm': 'meta'}
        o, a = mcq(rng, lab[d] + (' (activating)' if GRP[g][1] > 0 else ' (deactivating)'), [lab[x] + y for x in lab for y in (' (activating)', ' (deactivating)')])
        return dict(q=f'In electrophilic substitution, the {g} group on benzene is', o=o, a=a, sol=[f'{g}: {lab[d]}-directing, {"activating" if GRP[g][1] > 0 else "deactivating"}.'], p=dict(t=t, g=g))
    if t == 'act':
        ks = rng.sample(list(GRP), 4); need(len({GRP[k][1] for k in ks}) == 4); right = sorted(ks, key=lambda k: -GRP[k][1]); perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms)
        tx = lambda L: ' > '.join(f'C_{{6}}H_{{5}}{k[1:]}' for k in L); o, a = mcq(rng, tx(right), [tx(p) for p in perms])
        return dict(q='Decreasing reactivity towards electrophilic substitution:', o=o, a=a, sol=['Strong donors (+R) > alkyl (+I) > H > halogens (−I > +R) > −R groups.'], p=dict(t=t, ks=ks))
    if t == 'prod':
        g = rng.choice(list(GRP)); rx, e = rng.choice(EAS); need(not (e == 'COCH3' and (GRP[g][1] < -1 or g in ('–NH_{2}', '–OH'))))
        d = GRP[g][0]; r = {'op': 'mainly para (+ ortho) product', 'm': 'mainly meta product'}[d]
        o, a = mcq(rng, r, ['mainly meta product', 'mainly para (+ ortho) product', 'no reaction', 'equal o, m, p mixture'])
        return dict(q=f'{rx} of C_{{6}}H_{{5}}{g[1:]} gives', o=o, a=a, sol=[f'{g} is {"o/p" if d == "op" else "m"}-directing.'], p=dict(t=t, g=g, e=e))
    if t == 'mass':
        start, prod = rng.choice([('C6H6', 'C6H5NO2'), ('C6H5NO2', 'C6H4N2O4'), ('C6H6', 'C6H5Br'), ('C7H8', 'C7H7NO2'), ('C6H6', 'C8H8O'), ('C6H6', 'C6H6O3S')]); w = rng.choice([1.56, 2.34, 3.9, 7.8, 15.6, 2.46, 4.6, 9.2, 12.3])
        y = rng.choice([100, 80, 75, 60, 50]); g = w / mm(start) * mm(prod) * y / 100
        return dict(q=f'{nf(w, 3)} g of {ftex(start)} gives {ftex(prod)} in {y}% yield. Mass of product = ____ × 10^{{−2}} g (nearest integer).', o=None, a=round(g * 100),
                    sol=[f'{nf(w, 3)}/{mm(start)} mol × {mm(prod)} × {y}/100 = {nf(g, 4)} g.'], p=dict(t=t, w=w, s=start, pr=prod, y=y))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in ARO_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in ARO_F if v != want], 3))
    return dict(q=f'Which statement about benzene/arenes is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='afact', want=want))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(alk=g_alk, aro=g_aro).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent re-solve ----------------
def ozonolyse(s):
    """cut every C=C in the structure; each half gets =O. returns list of canonical strings of the pieces"""
    m = Mol(s); dbs = [(i, j) for (i, j), o in m.b.items() if o == 2 and m.a[i] == 'C' and m.a[j] == 'C']
    a = list(m.a); b = {k: v for k, v in m.b.items() if k not in dbs}
    for i, j in dbs:
        for c in (i, j): a.append('O'); b[(c, len(a) - 1)] = 2
    n = len(a); adj = [[] for _ in range(n)]
    for (i, j) in b: adj[i].append(j); adj[j].append(i)
    seen, out = set(), []
    for st in range(n):
        if st in seen: continue
        comp, q = [], [st]; seen.add(st)
        while q:
            u = q.pop(); comp.append(u)
            for v in adj[u]:
                if v not in seen: seen.add(v); q.append(v)
        idx = {o: k for k, o in enumerate(sorted(comp))}; mol = Mol.__new__(Mol); mol.a = [a[o] for o in sorted(comp)]
        mol.b = {(idx[i], idx[j]): o for (i, j), o in b.items() if i in idx}; mol.nb = [[] for _ in mol.a]
        for (i, j), o in mol.b.items(): mol.nb[i].append((j, o)); mol.nb[j].append((i, o))
        from orgkit import VAL
        mol.h = [max(0, round(VAL[e] - sum(o for _, o in mol.nb[i]))) for i, e in enumerate(mol.a)]; out.append(canon(mol))
    return sorted(out)
def add_hbr(s, peroxide):
    m = Mol(s); (i, j), = [(i, j) for (i, j), o in m.b.items() if o == 2]
    # carbocation/radical stability: count carbon neighbours (degree) of each alkene carbon; aryl counts extra
    def deg(c, other): return sum(1 for k, _ in m.nb[c] if k != other and m.a[k] in ('C', 'c')) + sum(2 for k, _ in m.nb[c] if m.a[k] == 'c')
    br = i if deg(i, j) > deg(j, i) else j   # Br goes where the more stable C+ / radical is …
    if peroxide: br = j if br == i else i     # … or, with peroxide, Br adds first to the other carbon
    if deg(i, j) == deg(j, i): return None
    a = m.a + ['Br']; b = dict(m.b); b[(i, j)] = 1; b[(min(br, len(m.a)), len(m.a))] = 1
    mol = Mol.__new__(Mol); mol.a = a; mol.b = b; mol.nb = [[] for _ in a]
    for (x, y), o in b.items(): mol.nb[x].append((y, o)); mol.nb[y].append((x, o))
    from orgkit import VAL
    mol.h = [max(0, round(VAL[e] - sum(o for _, o in mol.nb[k]))) for k, e in enumerate(a)]; return canon(mol)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'comb':
        c, h = p['n'], p['h']; o_atoms = 2 * c + h // 2; return R * 2 == o_atoms
    if t == 'combn':
        for n in range(1, 12):
            h = {'alkane': 2 * n + 2, 'alkene': 2 * n, 'alkyne': 2 * n - 2}[p['kind']]
            if 2 * n + h / 2 == 2 * p['o2']: return R == n
        return False
    if t == 'ozo': return ozonolyse(p['s']) == sorted(canon(Mol(CARB[x])) for x in R.split(' + '))
    if t in ('hbr', 'hbrp'):
        row = next(x for x in ALKENE if x[1] == p['s']); ps = (row[3] if t == 'hbr' else row[4])[1]
        sym = add_hbr(p['s'], t == 'hbrp'); got = canon(Mol(ps))
        if sym is None: return got == canon(Mol(ps)) and R == (row[3] if t == 'hbr' else row[4])[0] and row[3][1] == row[4][1]
        return sym == got and R == (row[3] if t == 'hbr' else row[4])[0]
    if t == 'mono': return R == Mol(p['s']).h_classes()
    if t == 'wurtz':
        L1, L2, F1, F2 = ALKY[RX[p['a1']]], ALKY[RX[p['a2']]], ALKF[RX[p['a1']]], ALKF[RX[p['a2']]]; return R == len({canon(Mol(x)) for x in (L1 + F1, L2 + F2, L1 + F2)})
    if t == 'fact': return dict(ALK_F)[R] == p['want']
    if t == 'dir': g = GRP[p['g']]; return R.startswith('ortho' if g[0] == 'op' else 'meta') and (('(activating)' in R) == (g[1] > 0))
    if t == 'act': L = ['–' + x.split('C_{6}H_{5}')[1] for x in R.split(' > ')]; return all(GRP[a][1] > GRP[b][1] for a, b in zip(L, L[1:]))
    if t == 'prod': return R == ('mainly meta product' if GRP[p['g']][0] == 'm' else 'mainly para (+ ortho) product')
    if t == 'mass': return R == round(p['w'] * mm(p['pr']) / mm(p['s']) * p['y'])
    if t == 'afact': return dict(ARO_F)[R] == p['want']
    raise KeyError(t)
