"""Practice generators — Chemistry Unit 14: Some Basic Principles of Organic Chemistry. check() recomputes each answer
another way: stereo/isomer counts and hydrogen environments from the structure (orgkit), alkane names re-derived
from the SMILES by searching every chain for the longest/most-substituted/lowest-locant choice, orders re-sorted
from the data tables, Hückel counts from π electrons. Statement items come from a fact bank written from NCERT."""
import re, itertools
from common import mcq, nf
from orgkit import Mol, alkanes
def need(x):
    if not x: raise AssertionError('retry')
CMP = [('2-chlorobutane', 'CC(Cl)CC'), ('butan-2-ol', 'CC(O)CC'), ('2-bromopentane', 'CC(Br)CCC'), ('3-bromopentane', 'CCC(Br)CC'), ('lactic acid', 'CC(O)C(=O)O'), ('glycerol', 'OCC(O)CO'),
       ('2,3-dichlorobutane', 'CC(Cl)C(Cl)C'), ('2,3-dibromopentane', 'CC(Br)C(Br)CC'), ('butane-2,3-diol', 'CC(O)C(O)C'), ('pent-3-en-2-ol', 'CC(O)C=CC'), ('hex-4-en-2-ol', 'CC(O)CC=CC'), ('but-2-ene', 'CC=CC'),
       ('pent-2-ene', 'CC=CCC'), ('2-methylbut-2-ene', 'CC=C(C)C'), ('propene', 'CC=C'), ('hexa-2,4-diene', 'CC=CC=CC'), ('3-methylpent-2-ene', 'CC=C(C)CC'), ('2-methylbutanoic acid', 'CCC(C)C(=O)O'),
       ('3-methylhexane', 'CCC(C)CCC'), ('2-methylpentane', 'CC(C)CCC'), ('1-chloro-2-methylbutane', 'ClCC(C)CC'), ('2-chloro-3-methylbutane', 'CC(Cl)C(C)C'), ('alanine', 'CC(N)C(=O)O'), ('glycine', 'NCC(=O)O'),
       ('pentan-3-ol', 'CCC(O)CC'), ('3-chlorohex-1-ene', 'C=CC(Cl)CCC'), ('1,2-dichloropropane', 'CC(Cl)CCl'), ('2-methylcyclohexanone', 'CC1CCCCC1=O'), ('cyclohexanone', 'O=C1CCCCC1'), ('4-methylpent-2-ene', 'CC=CC(C)C'),
       ('but-1-ene', 'C=CCC'), ('2-bromo-3-chlorobutane', 'CC(Br)C(Cl)C'), ('penta-2,3-diol? no: pentane-2,4-diol', 'CC(O)CC(O)C'), ('2-hydroxypropanal', 'CC(O)C=O'), ('1-phenylethanol', 'CC(O)c1ccccc1')]
CMP = [(n.split('no: ')[-1], s) for n, s in CMP]
ALK = [('propane', 'CCC'), ('butane', 'CCCC'), ('2-methylpropane', 'CC(C)C'), ('pentane', 'CCCCC'), ('2-methylbutane', 'CC(C)CC'), ('2,2-dimethylpropane', 'CC(C)(C)C'), ('hexane', 'CCCCCC'), ('2-methylpentane', 'CC(C)CCC'),
       ('3-methylpentane', 'CCC(C)CC'), ('2,2-dimethylbutane', 'CC(C)(C)CC'), ('2,3-dimethylbutane', 'CC(C)C(C)C'), ('cyclopentane', 'C1CCCC1'), ('methylcyclopentane', 'CC1CCCC1'), ('cyclohexane', 'C1CCCCC1'),
       ('methylcyclohexane', 'CC1CCCCC1'), ('ethylbenzene', 'CCc1ccccc1'), ('toluene (side chain + ring)', 'Cc1ccccc1'), ('2,2,4-trimethylpentane', 'CC(C)(C)CC(C)C'), ('3-ethylpentane', 'CCC(CC)CC'), ('heptane', 'CCCCCCC')]
PAIRS = [('butan-1-ol and butan-2-ol', 'position'), ('pentan-2-one and pentan-3-one', 'metamerism'), ('ethoxyethane and methoxypropane', 'metamerism'), ('propanal and propanone', 'functional'), ('ethanol and methoxymethane', 'functional'),
         ('butane and 2-methylpropane', 'chain'), ('pentane and 2,2-dimethylpropane', 'chain'), ('but-1-ene and but-2-ene', 'position'), ('cis- and trans-but-2-ene', 'geometrical'), ('(R)- and (S)-butan-2-ol', 'optical'),
         ('propanoic acid and methyl acetate', 'functional'), ('1-chloropropane and 2-chloropropane', 'position'), ('acetone and its enol prop-1-en-2-ol', 'tautomerism'), ('butanenitrile and butyl isocyanide', 'functional'),
         ('diethylamine and methylpropylamine', 'metamerism'), ('o-cresol and m-cresol', 'position'), ('2-methylpropene and but-1-ene', 'chain'), ('cyclopropane and propene', 'functional'), ('phenol and its keto form cyclohexa-2,4-dienone', 'tautomerism')]
ISO_N = {'position': 'position isomers', 'metamerism': 'metamers', 'functional': 'functional isomers', 'chain': 'chain isomers', 'geometrical': 'geometrical isomers', 'optical': 'optical isomers (enantiomers)', 'tautomerism': 'tautomers'}
def g_iso(rng):
    t = rng.choice(['chir', 'chir', 'stereo', 'mono', 'monost', 'alk', 'pair', 'geo', 'opt', 'chir'])
    if t == 'chir':
        pool = rng.sample(CMP, rng.randint(4, 6)); k = sum(1 for _, s in pool if Mol(s).chiral())
        return dict(q='How many of these have at least one chiral carbon? ' + ', '.join(n for n, _ in pool), o=None, a=k, sol=['; '.join(f'{n}: {len(Mol(s).chiral())}' for n, s in pool) + f' → {k}.'], p=dict(t=t, ss=[s for _, s in pool]))
    if t in ('stereo', 'opt'):
        n, s = rng.choice(CMP); m = Mol(s); a = m.stereo_count() if t == 'stereo' else m.optically_active()
        sol = [f'{n}: {len(m.chiral())} chiral C, {len(m.geo_db())} C=C with cis/trans.', f'{"Stereoisomers" if t == "stereo" else "Optically active isomers"} = {a}.']
        return dict(q=f'The number of {"stereoisomers" if t == "stereo" else "optically active stereoisomers"} of {n} is ____.', o=None, a=a, sol=sol, p=dict(t=t, s=s))
    if t in ('mono', 'monost'):
        n, s = rng.choice(ALK); m = Mol(s); prods = m.substitute()
        a = len(prods) if t == 'mono' else sum(p.stereo_count() for p in prods)
        return dict(q=f'Monochlorination of {n} (light) gives ____ {"structural isomers" if t == "mono" else "isomeric products including stereoisomers"}.', o=None, a=a,
                    sol=[f'{n} has {len(prods)} kinds of C–H → {len(prods)} structural monochlorides.'] + ([f'Counting enantiomers of chiral products → {a}.'] if t == 'monost' else []), p=dict(t=t, s=s))
    if t == 'alk':
        k = rng.randint(4, 8); return dict(q=f'The number of structural isomers of C_{{{k}}}H_{{{2 * k + 2}}} is ____.', o=None, a=alkanes(k), sol=[f'Build every carbon skeleton of {k} C: {alkanes(k)}.'], p=dict(t=t, k=k))
    if t == 'pair':
        pr, kind = rng.choice(PAIRS); o, a = mcq(rng, ISO_N[kind], [ISO_N[x] for x in rng.sample([x for x in ISO_N if x != kind], 6)])
        return dict(q=f'{pr} are', o=o, a=a, sol=[f'{pr}: {ISO_N[kind]}.'], p=dict(t=t, pr=pr))
    want = rng.choice([True, False]); t = 'geo'; c = [(n, s) for n, s in CMP if bool(Mol(s).geo_db() if want else Mol(s).chiral()) and len(Mol(s).geo_db() if want else Mol(s).chiral()) >= 1]
    r = rng.choice(c); w = [n for n, s in CMP if not (Mol(s).geo_db() if want else Mol(s).chiral())]; need(len(w) >= 3)
    o, a = mcq(rng, r[0], rng.sample(w, 3))
    return dict(q=f'Which of these shows {"geometrical (cis–trans)" if want else "optical"} isomerism?', o=o, a=a, sol=[f'{r[0]} {"has a C=C with two different groups on each end" if want else "has a chiral carbon"}; the others do not.'], p=dict(t=t, want=want))

ACID = {'HCOOH': 3.75, 'CH_{3}COOH': 4.76, 'C_{2}H_{5}COOH': 4.87, 'ClCH_{2}COOH': 2.86, 'Cl_{2}CHCOOH': 1.29, 'Cl_{3}CCOOH': 0.65, 'FCH_{2}COOH': 2.59, 'C_{6}H_{5}COOH': 4.20, 'phenol': 10.0, 'p-nitrophenol': 7.15,
        'o-nitrophenol': 7.23, 'p-cresol': 10.26, '2,4,6-trinitrophenol': 0.4, 'ethanol': 15.9, 'water': 15.7, 'ethyne': 25, 'H_{2}CO_{3}': 6.35, 'p-methoxyphenol': 10.2, 'm-nitrophenol': 8.4}
BASE = {'piperidine': 11.1, 'pyridine': 5.2, 'pyrrole': -3.8, 'aniline': 4.6, 'p-toluidine': 5.1, 'p-nitroaniline': 1.0, 'N-methylaniline': 4.85, 'benzylamine': 9.3, 'methylamine': 10.6, 'dimethylamine': 10.7,
        'trimethylamine (aq.)': 9.8, 'ammonia': 9.25, 'acetamide': -0.5, 'p-anisidine': 5.3}
CATION = [('tropylium', 10), ('triphenylmethyl', 8), ('diphenylmethyl', 6), ('p-methoxybenzyl', 5.5), ('benzyl', 4.5), ('tert-butyl', 4), ('allyl', 3.5), ('isopropyl', 3), ('ethyl', 2), ('methyl', 1), ('vinyl', 0.5), ('phenyl', 0.4)]
SIG = {'NO_{2}': 0.78, 'CN': 0.66, 'CHO': 0.42, 'COCH_{3}': 0.50, 'Cl': 0.23, 'Br': 0.23, 'H': 0, 'CH_{3}': -0.17, 'OCH_{3}': -0.27, 'NH_{2}': -0.66}
EFF = {'–NO_{2}': '−R, −I', '–CN': '−R, −I', '–CHO': '−R, −I', '–COOH': '−R, −I', '–OH': '+R, −I', '–NH_{2}': '+R, −I', '–OCH_{3}': '+R, −I', '–Cl': '+R, −I (−I wins)', '–CH_{3}': '+I (and hyperconjugation)', '–C(CH_{3})_{3}': '+I (no hyperconjugation)', '–NHCOCH_{3}': '+R, −I', '–SO_{3}H': '−R, −I'}
RING = [('benzene', 6, True), ('cyclopentadienyl anion', 6, True), ('cyclopentadienyl cation', 4, True), ('tropylium cation', 6, True), ('cycloheptatriene', 6, False), ('cyclooctatetraene (tub)', 8, False), ('cyclobutadiene', 4, True),
        ('cyclopropenyl cation', 2, True), ('cyclopropenyl anion', 4, True), ('pyridine', 6, True), ('pyrrole', 6, True), ('furan', 6, True), ('thiophene', 6, True), ('cyclopentadiene', 4, False), ('naphthalene', 10, True),
        ('cyclooctatetraene dianion', 10, True), ('cyclobutadiene dication', 2, True), ('azulene', 10, True)]
def ring_kind(pi, conj): return 'aromatic' if conj and pi % 4 == 2 else ('antiaromatic' if conj and pi % 4 == 0 else 'non-aromatic')
HYP = [('ethyl cation', 'CC', 0), ('isopropyl cation', 'CCC', 1), ('tert-butyl cation', 'CC(C)C', 1), ('sec-butyl cation', 'CCCC', 1), ('2-methylbut-2-yl cation', 'CC(C)CC', 1), ('propene', 'C=CC', 'db'), ('but-2-ene', 'CC=CC', 'db'),
       ('2-methylpropene', 'C=C(C)C', 'db'), ('2,3-dimethylbut-2-ene', 'CC(C)=C(C)C', 'db'), ('2-methylbut-2-ene', 'CC=C(C)C', 'db'), ('but-1-ene', 'C=CCC', 'db'), ('toluene (CH_{3} on ring)', 'Cc1ccccc1', 'ar')]
def alpha_h(s, site):
    m = Mol(s)
    if site == 'db': cs = [i for (i, j), o in m.b.items() if o == 2] + [j for (i, j), o in m.b.items() if o == 2]
    elif site == 'ar': cs = [i for i, e in enumerate(m.a) if e == 'c']
    else: cs = [site]
    return sum(m.h[j] for i in cs for j, _ in m.nb[i] if j not in cs and m.a[j] == 'C')
def g_eff(rng):
    t = rng.choice(['acid', 'base', 'cat', 'anion', 'ring', 'eff', 'hyp', 'acid2', 'acid', 'cat', 'base'])
    if t in ('acid', 'acid2', 'base'):
        tab = BASE if t == 'base' else ACID; ks = rng.sample(list(tab), 4); v = [tab[k] for k in ks]; need(min(abs(a - b) for a, b in itertools.combinations(v, 2)) > 0.1)
        if t == 'acid2':
            hi = rng.choice([True, False]); r = (min if hi else max)(ks, key=tab.get); o, a = mcq(rng, r, [k for k in ks if k != r])
            return dict(q=f'The {"strongest" if hi else "weakest"} acid among these is', o=o, a=a, sol=['pKa: ' + ', '.join(f'{k} {tab[k]}' for k in ks) + '.'], p=dict(t=t, ks=ks, hi=hi))
        right = sorted(ks, key=lambda k: -tab[k] if t == 'base' else tab[k]); perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms)
        o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q=f'The decreasing order of {"basic" if t == "base" else "acidic"} strength is', o=o, a=a, sol=[('pKa of conjugate acid: ' if t == 'base' else 'pKa: ') + ', '.join(f'{k} {tab[k]}' for k in ks) + '.'], p=dict(t=t, ks=ks))
    if t == 'cat':
        pool = rng.sample(CATION, 4); right = [n for n, _ in sorted(pool, key=lambda x: -x[1])]; perms = [list(p) for p in itertools.permutations(right) if list(p) != right]; rng.shuffle(perms)
        o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q='Decreasing order of stability of these carbocations: ' + ', '.join(n for n, _ in pool), o=o, a=a, sol=['Aromatic (tropylium) > extensive resonance (trityl > benzhydryl > benzyl, allyl) > 3° > 2° > 1° > CH_{3}^{+} > vinyl/phenyl (sp^{2} C^{+}).'], p=dict(t=t, names=[n for n, _ in pool]))
    if t == 'anion':
        ks = rng.sample(list(SIG), 4); need(len({SIG[k] for k in ks}) == 4); right = sorted(ks, key=lambda k: -SIG[k]); perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]; rng.shuffle(perms)
        tx = lambda L: ' > '.join(f'p-{k}' for k in L); o, a = mcq(rng, tx(right), [tx(p) for p in perms])
        return dict(q='Decreasing stability of the benzylic carbanions p-X–C_{6}H_{4}–C^{−}H_{2} for X = ' + ', '.join(ks), o=o, a=a, sol=['Electron-withdrawing para groups spread the negative charge: σ_{p} ' + ', '.join(f'{k} {SIG[k]}' for k in ks) + '.'], p=dict(t=t, ks=ks))
    if t == 'ring':
        n, pi, conj = rng.choice(RING); k = ring_kind(pi, conj); o, a = mcq(rng, k, ['aromatic', 'antiaromatic', 'non-aromatic', 'cannot be decided'])
        return dict(q=f'{n} is', o=o, a=a, sol=[f'{pi} π electrons; {"cyclic, planar, fully conjugated" if conj else "not a continuous planar cycle of p orbitals"} → {k}.'], p=dict(t=t, n=n))
    if t == 'eff':
        g = rng.choice(list(EFF)); o, a = mcq(rng, EFF[g], [v for v in dict.fromkeys(EFF.values()) if v != EFF[g]])
        return dict(q=f'The electronic effects shown by the {g} group on a benzene ring are', o=o, a=a, sol=[f'{g}: {EFF[g]}.'], p=dict(t=t, g=g))
    n, s, site = rng.choice(HYP)
    if isinstance(site, int):   # cation centre: the carbon index given in our SMILES (the C^{+})
        c = {'ethyl cation': 0, 'isopropyl cation': 1, 'tert-butyl cation': 1, 'sec-butyl cation': 1, '2-methylbut-2-yl cation': 1}[n]; k = alpha_h(s, c)
    else: k = alpha_h(s, site)
    return dict(q=f'The number of hyperconjugative (α-H) structures for {n} is ____.', o=None, a=k, sol=['Count C–H bonds on carbons attached to the C^{+} (or to the C=C / ring).', f'{n}: {k}.'], p=dict(t='hyp', n=n))

# ---- alkane names: build main chain + substituents, name independently in check
SUB = {1: 'methyl', 2: 'ethyl', 3: 'propyl'}
MULT = {1: '', 2: 'di', 3: 'tri', 4: 'tetra'}
def build(rng):
    n = rng.randint(5, 9); subs = []
    for _ in range(rng.randint(1, 3)):
        L = rng.choice([1, 1, 1, 2] if n >= 7 else [1]); p = rng.randint(2, n - 1) if L == 1 else rng.randint(4, n - 3)   # ethyl at least 3 from an end, so the main chain stays longest
        subs.append((p, L))
    cnt = {}
    for p, L in subs: cnt[p] = cnt.get(p, 0) + 1
    need(all(v <= 2 for v in cnt.values()))
    # SMILES: main chain C1..Cn with branches
    out = ''
    for i in range(1, n + 1):
        out += 'C' + ''.join('(' + 'C' * L + ')' for p, L in subs if p == i)
    return n, subs, out
def name_from(n, subs):
    def locs(rev): return sorted(((n + 1 - p) if rev else p, L) for p, L in subs)
    a, b = locs(False), locs(True); best = min(a, b, key=lambda x: [p for p, _ in x])
    if [p for p, _ in a] == [p for p, _ in b]: best = min(a, b, key=lambda x: [p for p, L in sorted(x, key=lambda y: SUB[y[1]])])
    groups = {}
    for p, L in best: groups.setdefault(SUB[L], []).append(p)
    parts = [','.join(map(str, sorted(groups[g]))) + '-' + MULT[len(groups[g])] + g for g in sorted(groups)]
    return '-'.join(parts) + ['', '', '', '', '', 'pentane', 'hexane', 'heptane', 'octane', 'nonane', 'decane'][n]
NOM_F = [('–COOH outranks –CHO, ketone, –OH, –NH_{2} as the principal group.', True), ('Ester > amide > nitrile > aldehyde > ketone > alcohol > amine in suffix priority.', True), ('Halogens and –NO_{2} are always written as prefixes.', True),
         ('Substituent prefixes are listed in increasing order of locant.', False), ('Prefixes di-, tri- are ignored when alphabetising substituents.', True), ('In ring compounds the ring is always the parent.', False),
         ('The longest chain containing the principal group is the parent chain.', True), ('A carbocyclic non-aromatic ring compound is called alicyclic.', True), ('Pyridine is a homocyclic compound.', False),
         ('Furan, thiophene and pyrrole are heterocyclic aromatic compounds.', True), ('The suffix for a nitrile is -nitrile and its carbon is counted in the chain.', True), ('–CHO as a prefix is called carbonyl.', False)]
CLASS = [('CH_{3}CH_{2}OH', 'alcohol'), ('CH_{3}OCH_{3}', 'ether'), ('CH_{3}CHO', 'aldehyde'), ('CH_{3}COCH_{3}', 'ketone'), ('CH_{3}COOH', 'carboxylic acid'), ('CH_{3}COOCH_{3}', 'ester'), ('CH_{3}CONH_{2}', 'amide'),
         ('CH_{3}CN', 'nitrile'), ('CH_{3}NC', 'isocyanide'), ('CH_{3}NH_{2}', 'amine'), ('CH_{3}NO_{2}', 'nitro compound'), ('CH_{3}COCl', 'acid chloride'), ('(CH_{3}CO)_{2}O', 'acid anhydride'), ('C_{6}H_{5}OH', 'phenol')]
def g_nom(rng):
    t = rng.choice(['alk', 'alk', 'alk', 'cls', 'nf'])
    if t == 'alk':
        n, subs, smi = build(rng); right = name_from(n, subs)
        wrong = {name_from(n, [(n + 1 - p, L) for p, L in subs]).replace('-', '–', 0), right.replace('ane', 'ene', 1)}
        alt = [(p + 1 if p + 1 < n else p - 1, L) for p, L in subs]; wrong.add(name_from(n, alt)); wrong.add(name_from(n + 1, [(p, L) for p, L in subs]) if n < 10 else right + 'x')
        if len(subs) and subs[0][1] == 1: wrong.add(name_from(n - 1, [(max(1, p - 1), L) for p, L in subs]))
        wrong = [w for w in wrong if w != right]; need(len(set(wrong)) >= 3)
        o, a = mcq(rng, right, rng.sample(sorted(set(wrong)), len(set(wrong))))
        return dict(q=f'The IUPAC name of the alkane written as {pretty(smi)} is', o=o, a=a, sol=[f'Longest chain: {n} C. Number from the end that gives the lower locants; list substituents alphabetically.', right + '.'], p=dict(t='name', smi=smi))
    if t == 'cls':
        f, c = rng.choice(CLASS); o, a = mcq(rng, c, [x for _, x in rng.sample(CLASS, 6) if x != c])
        return dict(q=f'{f} belongs to the class', o=o, a=a, sol=[f'{f}: {c}.'], p=dict(t=t, f=f))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in NOM_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in NOM_F if v != want], 3))
    return dict(q=f'Which statement about IUPAC naming/classification is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='nf', want=want))
def pretty(smi):   # CCC(C)CC → CH3–CH2–CH(CH3)–CH2–CH3 (main chain + branches)
    m = Mol(smi); main = [i for i in range(len(m.a)) if not any(smi[:0])]
    toks = re.findall(r'C|\(C+\)', smi); out = []
    for tk in toks:
        if tk == 'C': out.append(['C', []])
        else: out[-1][1].append(len(tk) - 2)
    n = len(out); res = []
    for k, (c, br) in enumerate(out):
        h = 4 - (2 if 0 < k < n - 1 else 1) - len(br) if n > 1 else 4
        res.append('C' + (f'H_{{{h}}}' if h > 1 else ('H' if h == 1 else '')) + ''.join('(' + ('CH_{3}' if L == 1 else 'C_{2}H_{5}' if L == 2 else 'C_{3}H_{7}') + ')' for L in br))
    return '–'.join(res)
MECH = [('CH_{3}Br + OH^{−} → CH_{3}OH + Br^{−}', 'nucleophilic substitution'), ('C_{6}H_{6} + HNO_{3}/H_{2}SO_{4} → C_{6}H_{5}NO_{2}', 'electrophilic substitution'), ('CH_{2}=CH_{2} + Br_{2} → BrCH_{2}CH_{2}Br', 'electrophilic addition'),
        ('CH_{4} + Cl_{2} (light) → CH_{3}Cl', 'free radical substitution'), ('CH_{3}CHO + HCN → CH_{3}CH(OH)CN', 'nucleophilic addition'), ('CH_{3}CH_{2}Br + alc. KOH → CH_{2}=CH_{2}', 'elimination'),
        ('C_{6}H_{6} + CH_{3}Cl/AlCl_{3} → C_{6}H_{5}CH_{3}', 'electrophilic substitution'), ('CH_{2}=CH_{2} + HBr → CH_{3}CH_{2}Br', 'electrophilic addition'), ('C_{2}H_{5}ONa + CH_{3}I → C_{2}H_{5}OCH_{3}', 'nucleophilic substitution'),
        ('C_{6}H_{5}CH_{3} + Cl_{2} (light) → C_{6}H_{5}CH_{2}Cl', 'free radical substitution'), ('CH_{3}CH_{2}OH + conc. H_{2}SO_{4}, 443 K → CH_{2}=CH_{2}', 'elimination'), ('propanone + NaHSO_{3} → bisulphite adduct', 'nucleophilic addition')]
NUC = [('NH_{3}', 'nucleophile'), ('H_{2}O', 'nucleophile'), ('OH^{−}', 'nucleophile'), ('CN^{−}', 'nucleophile'), ('R–NH_{2}', 'nucleophile'), ('CH_{2}=CH_{2} (π electrons)', 'nucleophile'), ('C_{2}H_{5}O^{−}', 'nucleophile'),
       ('H^{+}', 'electrophile'), ('NO_{2}^{+}', 'electrophile'), ('BF_{3}', 'electrophile'), ('AlCl_{3}', 'electrophile'), ('CH_{3}^{+}', 'electrophile'), ('Br^{+}', 'electrophile'), ('carbonyl carbon of CH_{3}CHO', 'electrophile'), ('SO_{3}', 'electrophile')]
INT = [('carbocation', 'sp^{2}', 'trigonal planar', 6), ('carbanion (simple alkyl)', 'sp^{3}', 'pyramidal', 8), ('free radical (alkyl)', 'sp^{2}', 'planar (or nearly)', 7), ('carbene (singlet)', 'sp^{2}', 'bent', 6)]
def g_mech(rng):
    t = rng.choice(['rx', 'nuc', 'cnt', 'int', 'clv'])
    if t == 'rx':
        r, k = rng.choice(MECH); o, a = mcq(rng, k, [x for x in dict.fromkeys(v for _, v in MECH) if x != k])
        return dict(q=f'The reaction {r} is an example of', o=o, a=a, sol=[f'{k}.'], p=dict(t=t, r=r))
    if t == 'nuc':
        s, k = rng.choice(NUC); o, a = mcq(rng, k, ['nucleophile', 'electrophile', 'free radical', 'neither'])
        return dict(q=f'{s} acts as a(n)', o=o, a=a, sol=[f'{s}: {"electron-pair donor" if k == "nucleophile" else "electron-pair acceptor"} → {k}.'], p=dict(t=t, s=s))
    if t == 'cnt':
        pool = rng.sample(NUC, rng.randint(5, 7)); want = rng.choice(['nucleophile', 'electrophile']); k = sum(1 for _, v in pool if v == want)
        return dict(q=f'Number of {want}s among: ' + ', '.join(s for s, _ in pool), o=None, a=k, sol=['; '.join(f'{s} {v}' for s, v in pool)], p=dict(t=t, ss=[s for s, _ in pool], want=want))
    if t == 'int':
        n, h, g, e = rng.choice(INT); what = rng.choice(['hyb', 'geo', 'e'])
        if what == 'e': return dict(q=f'The number of valence electrons around the reactive carbon of a {n} is ____.', o=None, a=e, sol=[f'{n}: {e}.'], p=dict(t='int', n=n, what=what))
        right = h if what == 'hyb' else g; pool = [x[1] if what == 'hyb' else x[2] for x in INT] + (['sp'] if what == 'hyb' else ['linear', 'tetrahedral'])
        o, a = mcq(rng, right, [x for x in dict.fromkeys(pool) if x != right])
        return dict(q=f'The {"hybridisation" if what == "hyb" else "shape"} of a {n} is', o=o, a=a, sol=[f'{n}: {h}, {g}.'], p=dict(t='int', n=n, what=what))
    homo = rng.choice([True, False]); o, a = mcq(rng, 'free radicals' if homo else 'ions (carbocation/carbanion)', ['free radicals' if not homo else 'ions (carbocation/carbanion)', 'only carbenes', 'no intermediate'])
    return dict(q=f'{"Homolytic" if homo else "Heterolytic"} bond cleavage produces', o=o, a=a, sol=[f'{"Each atom keeps one electron" if homo else "One atom takes both electrons"}.'], p=dict(t='clv', homo=homo))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(iso=g_iso, eff=g_eff, nom=g_nom, mech=g_mech).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent re-solve ----------------
def name2(smi):
    """name a branched alkane from scratch: try every longest chain, prefer most substituents, then lowest locants, then alphabetical"""
    m = Mol(smi); n = len(m.a); adj = [[j for j, _ in m.nb[i]] for i in range(n)]; ends = [i for i in range(n) if len(adj[i]) == 1]
    def path(a, b):
        prev = {a: None}; q = [a]
        for u in q:
            for v in adj[u]:
                if v not in prev: prev[v] = u; q.append(v)
        p = [b]
        while prev[p[-1]] is not None: p.append(prev[p[-1]])
        return p[::-1]
    paths = [path(a, b) for a in ends for b in ends if a != b]; L = max(map(len, paths)); best = None
    for p in paths:
        if len(p) != L: continue
        s = set(p); subs = []
        for k, c in enumerate(p):
            for d in adj[c]:
                if d in s: continue
                size, st = 0, [d]; seen = {c}
                while st:
                    u = st.pop(); seen.add(u); size += 1; st += [v for v in adj[u] if v not in seen]
                subs.append((k + 1, size))
        key = (-len(subs), sorted(x for x, _ in subs), sorted((SUB[sz], x) for x, sz in subs))
        if best is None or key < best[0]: best = (key, subs)
    subs = best[1]; groups = {}
    for x, sz in subs: groups.setdefault(SUB[sz], []).append(x)
    return '-'.join(','.join(map(str, sorted(groups[g]))) + '-' + MULT[len(groups[g])] + g for g in sorted(groups)) + ['', '', '', '', '', 'pentane', 'hexane', 'heptane', 'octane', 'nonane', 'decane'][L]
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'chir': return R == sum(1 for s in p['ss'] if Mol(s).chiral())
    if t == 'stereo': return R == Mol(p['s']).stereo_count()
    if t == 'opt': return R == Mol(p['s']).optically_active()
    if t == 'mono': return R == Mol(p['s']).h_classes('C') + (Mol(p['s']).h_classes('c') if 'c' in p['s'] else 0)
    if t == 'monost': return R == sum(x.stereo_count() for x in Mol(p['s']).substitute())
    if t == 'alk': return R == {4: 2, 5: 3, 6: 5, 7: 9, 8: 18}[p['k']]
    if t == 'pair': return ISO_N[dict(PAIRS)[p['pr']]] == R
    if t in ('geo', 'opt2'): pass
    if t == 'geo' and 'want' in p:
        s = dict(CMP)[R]; return bool(Mol(s).geo_db() if p['want'] else Mol(s).chiral()) and all(not (Mol(dict(CMP)[o]).geo_db() if p['want'] else Mol(dict(CMP)[o]).chiral()) for o in it['o'] if o != R)
    if t in ('acid', 'base'):
        tab = BASE if t == 'base' else ACID; L = R.split(' > '); return all((tab[a] > tab[b]) if t == 'base' else (tab[a] < tab[b]) for a, b in zip(L, L[1:]))
    if t == 'acid2': return all((ACID[R] < ACID[k]) if p['hi'] else (ACID[R] > ACID[k]) for k in p['ks'] if k != R)
    if t == 'cat': d = dict(CATION); L = R.split(' > '); return all(d[a] > d[b] for a, b in zip(L, L[1:]))
    if t == 'anion': L = [x[2:] for x in R.split(' > ')]; return all(SIG[a] > SIG[b] for a, b in zip(L, L[1:]))
    if t == 'ring':
        n, pi, conj = next(x for x in RING if x[0] == p['n'])
        return R == ('aromatic' if conj and (pi - 2) % 4 == 0 else 'antiaromatic' if conj else 'non-aromatic')
    if t == 'eff': return EFF[p['g']] == R
    if t == 'hyp':
        exp = {'ethyl cation': 3, 'isopropyl cation': 6, 'tert-butyl cation': 9, 'sec-butyl cation': 5, '2-methylbut-2-yl cation': 8, 'propene': 3, 'but-2-ene': 6, '2-methylpropene': 6, '2,3-dimethylbut-2-ene': 12,
               '2-methylbut-2-ene': 9, 'but-1-ene': 2, 'toluene (CH_{3} on ring)': 3}
        return R == exp[p['n']]
    if t == 'name': return R == name2(p['smi'])
    if t == 'cls': return dict(CLASS)[p['f']] == R
    if t == 'nf': return dict(NOM_F)[R] == p['want']
    if t == 'rx': return dict(MECH)[p['r']] == R
    if t == 'nuc': return dict(NUC)[p['s']] == R
    if t == 'cnt': return R == sum(1 for s in p['ss'] if dict(NUC)[s] == p['want'])
    if t == 'int':
        n, h, g, e = next(x for x in INT if x[0] == p['n']); return R == {'hyb': h, 'geo': g, 'e': e}[p['what']]
    if t == 'clv': return R == ('free radicals' if p['homo'] else 'ions (carbocation/carbanion)')
    raise KeyError(t)
