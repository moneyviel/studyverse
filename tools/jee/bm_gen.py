"""Practice generators — Chemistry Unit 19: Biomolecules. check() re-derives each answer another way: base pairing via
str.maketrans and regex counts, peptide counts by brute-force enumeration with itertools, atom counts by parsing a
written structure, masses from formula masses, fact items from a second table keyed differently."""
import re, itertools, math
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
AM = {'C': 12, 'H': 1, 'N': 14, 'O': 16, 'S': 32}
def mm(f): return sum(AM[e] * (int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f))
def cnt(f, el): return sum(int(n) if n else 1 for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f) if e == el)

# ---------- amino acids: name -> (3-letter, formula, side chain R, essential?) ----------
AA = {'glycine': ('Gly', 'C2H5NO2', 'H', False), 'alanine': ('Ala', 'C3H7NO2', 'CH3', False), 'valine': ('Val', 'C5H11NO2', 'CHCH3CH3', True), 'leucine': ('Leu', 'C6H13NO2', 'CH2CHCH3CH3', True),
      'isoleucine': ('Ile', 'C6H13NO2', 'CHCH3CH2CH3', True), 'phenylalanine': ('Phe', 'C9H11NO2', 'CH2C6H5', True), 'tyrosine': ('Tyr', 'C9H11NO3', 'CH2C6H4OH', False), 'serine': ('Ser', 'C3H7NO3', 'CH2OH', False),
      'threonine': ('Thr', 'C4H9NO3', 'CHOHCH3', True), 'cysteine': ('Cys', 'C3H7NO2S', 'CH2SH', False), 'methionine': ('Met', 'C5H11NO2S', 'CH2CH2SCH3', True), 'lysine': ('Lys', 'C6H14N2O2', 'CH2CH2CH2CH2NH2', True),
      'aspartic acid': ('Asp', 'C4H7NO4', 'CH2COOH', False), 'glutamic acid': ('Glu', 'C5H9NO4', 'CH2CH2COOH', False), 'tryptophan': ('Trp', 'C11H12N2O2', 'CH2C8H6N', True), 'histidine': ('His', 'C6H9N3O2', 'CH2C3H3N2', True),
      'arginine': ('Arg', 'C6H14N4O2', 'CH2CH2CH2NHCNHNH2', True), 'proline': ('Pro', 'C5H9NO2', 'ring', False), 'asparagine': ('Asn', 'C4H8N2O3', 'CH2CONH2', False), 'glutamine': ('Gln', 'C5H10N2O3', 'CH2CH2CONH2', False)}
ESS_CODES = 'V L I F W T M K R H'.split()          # second, independent record of the NCERT essential list (one-letter codes)
ONE = {'glycine': 'G', 'alanine': 'A', 'valine': 'V', 'leucine': 'L', 'isoleucine': 'I', 'phenylalanine': 'F', 'tyrosine': 'Y', 'serine': 'S', 'threonine': 'T', 'cysteine': 'C', 'methionine': 'M', 'lysine': 'K',
       'aspartic acid': 'D', 'glutamic acid': 'E', 'tryptophan': 'W', 'histidine': 'H', 'arginine': 'R', 'proline': 'P', 'asparagine': 'N', 'glutamine': 'Q'}
CORE = {'C': 2, 'H': 4, 'N': 1, 'O': 2}            # H2N–CH–COOH backbone without R (R = H gives glycine)
def from_r(r):   # independent atom count: backbone + side chain written as a string
    if r == 'ring': return {'C': 5, 'H': 9, 'N': 1, 'O': 2, 'S': 0}
    d = dict(CORE); d['S'] = 0
    for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', r): d[e] = d.get(e, 0) + (int(n) if n else 1)
    return d
HNO2 = {'glycine': 'glycolic acid (HOCH_{2}COOH)', 'alanine': 'lactic acid (CH_{3}CH(OH)COOH)', 'valine': '2-hydroxy-3-methylbutanoic acid', 'phenylalanine': '2-hydroxy-3-phenylpropanoic acid', 'serine': '2,3-dihydroxypropanoic acid (glyceric acid)', 'leucine': '2-hydroxy-4-methylpentanoic acid'}
LEVEL = [('sequence of amino acids joined by peptide bonds', 'primary'), ('α-helix', 'secondary'), ('β-pleated sheet', 'secondary'), ('overall folding of one polypeptide chain (globular/fibrous shape)', 'tertiary'),
         ('arrangement of two or more polypeptide subunits', 'quaternary'), ('H-bonds between C=O and N–H of the same backbone in a regular coil', 'secondary'), ('disulphide bridges, ionic and hydrophobic interactions fixing the 3-D fold', 'tertiary'),
         ('the part left intact on denaturation', 'primary'), ('haemoglobin being made of four chains', 'quaternary')]
LEV2 = {'helix': 'secondary', 'sheet': 'secondary', 'peptide bonds': 'primary', 'intact': 'primary', 'subunits': 'quaternary', 'four chains': 'quaternary', 'one polypeptide': 'tertiary', '3-D fold': 'tertiary', 'regular coil': 'secondary'}
PROT_F = [('Proteins on hydrolysis give α-amino acids.', True), ('Glycine is optically inactive.', True), ('Amino acids exist as zwitterions in solution.', True), ('Peptide bond is an amide (–CO–NH–) link.', True),
          ('Denaturation destroys the primary structure.', False), ('Enzymes are non-specific catalysts.', False), ('Most enzymes are globular proteins.', True), ('Insulin and keratin are both globular proteins.', False),
          ('Keratin and myosin are fibrous proteins.', True), ('Cysteine residues can form –S–S– bridges.', True), ('Proline has a six-membered ring.', False), ('Histidine contains an imidazole ring.', True),
          ('Tyrosine is an essential amino acid.', False), ('Lysine is an essential amino acid.', True), ('Ninhydrin gives a violet colour with proteins.', True), ('Coagulation of egg white is denaturation.', True),
          ('Enzymes lower the activation energy of a reaction.', True), ('Maltase converts maltose into glucose.', True), ('Invertase converts sucrose into glucose only.', False), ('All naturally occurring amino acids are optically active.', False)]

# ---------- carbohydrates ----------
LINK = {'sucrose': 'α1–β2', 'maltose': 'α1–4', 'lactose': 'β1–4', 'amylose': 'α1–4', 'amylopectin': 'α1–4 and α1–6', 'cellulose': 'β1–4', 'glycogen': 'α1–4 and α1–6'}
LINK2 = {'sucrose': ('a', 1, 2), 'maltose': ('a', 1, 4), 'lactose': ('b', 1, 4), 'amylose': ('a', 1, 4), 'amylopectin': ('a', 1, 4, 6), 'cellulose': ('b', 1, 4), 'glycogen': ('a', 1, 4, 6)}
def l2s(t): return ('α' if t[0] == 'a' else 'β') + '1–' + ('β2' if t[2] == 2 else '4') + (' and α1–6' if len(t) == 4 else '')
HYD = {'sucrose': 'glucose and fructose', 'maltose': 'glucose only', 'lactose': 'glucose and galactose', 'starch': 'glucose only', 'cellulose': 'glucose only', 'glycogen': 'glucose only', 'raffinose': 'glucose, fructose and galactose'}
HYD2 = {'sucrose': {'glc', 'fru'}, 'maltose': {'glc'}, 'lactose': {'glc', 'gal'}, 'starch': {'glc'}, 'cellulose': {'glc'}, 'glycogen': {'glc'}, 'raffinose': {'glc', 'fru', 'gal'}}
NM = {'glc': 'glucose', 'fru': 'fructose', 'gal': 'galactose'}
REDUCING = {'glucose': True, 'fructose': True, 'galactose': True, 'ribose': True, 'maltose': True, 'lactose': True, 'sucrose': False, 'starch': False, 'cellulose': False, 'mannose': True, 'cellobiose': True, 'trehalose': False}
FREE_ANOMER = {'glucose': 1, 'fructose': 1, 'galactose': 1, 'ribose': 1, 'mannose': 1, 'maltose': 1, 'lactose': 1, 'cellobiose': 1, 'sucrose': 0, 'trehalose': 0, 'starch': 0, 'cellulose': 0}   # free hemiacetal ends (polymers ≈ 0)
GRX = [('hydroxylamine (NH_{2}OH)', 'glucose oxime'), ('HCN', 'glucose cyanohydrin'), ('Br_{2} water', 'gluconic acid'), ('conc. HNO_{3}', 'saccharic acid'), ('HI, prolonged heating', 'n-hexane'),
       ('acetic anhydride (excess)', 'glucose pentaacetate'), ('NaHCO_{3}', 'no reaction'), ('Tollens reagent', 'silver mirror (gluconate)'), ('NaBH_{4}', 'sorbitol (glucitol)')]
GRX2 = {'oxime': 'NH2OH', 'cyanohydrin': 'HCN', 'gluconic': 'Br2', 'saccharic': 'HNO3', 'hexane': 'HI', 'pentaacetate': 'Ac2O', 'no reaction': 'NaHCO3', 'silver': 'Tollens', 'sorbitol': 'NaBH4'}
def gkey(r): return {'hydroxylamine (NH_{2}OH)': 'NH2OH', 'HCN': 'HCN', 'Br_{2} water': 'Br2', 'conc. HNO_{3}': 'HNO3', 'HI, prolonged heating': 'HI', 'acetic anhydride (excess)': 'Ac2O', 'NaHCO_{3}': 'NaHCO3', 'Tollens reagent': 'Tollens', 'NaBH_{4}': 'NaBH4'}[r]
CARB_F = [('Glucose is an aldohexose.', True), ('Fructose is a ketohexose.', True), ('Sucrose is a reducing sugar.', False), ('Maltose is a reducing sugar.', True), ('Glucose pentaacetate reacts with hydroxylamine.', False),
          ('Glucose does not give Schiff\'s test although it has –CHO.', True), ('α- and β-D-glucose are anomers.', True), ('α- and β-D-glucose differ at C-4.', False), ('Invert sugar is laevorotatory.', True),
          ('Cellulose has β1→4 links.', True), ('Amylose is a branched polymer.', False), ('Amylopectin has α1→6 branch points.', True), ('Starch is a polymer of β-glucose.', False), ('Fructose reduces Tollens reagent.', True),
          ('D/L refers to the sign of optical rotation.', False), ('Glucose on heating with HI gives n-hexane.', True), ('Lactose is milk sugar.', True), ('Sucrose on hydrolysis gives only glucose.', False),
          ('Glycogen is called animal starch.', True), ('Fructose exists mainly as a five-membered (furanose) ring in sucrose.', True)]

# ---------- nucleic acids ----------
NUC_F = [('DNA contains the sugar 2-deoxyribose.', True), ('RNA contains thymine.', False), ('DNA contains uracil.', False), ('Adenine pairs with thymine by two H-bonds.', True), ('Guanine pairs with cytosine by two H-bonds.', False),
         ('Nucleotides are linked by phosphodiester bonds.', True), ('A nucleoside = base + sugar + phosphate.', False), ('DNA is a double helix.', True), ('RNA is usually single-stranded.', True), ('DNA is the reserve of genetic information.', True),
         ('In DNA, the amount of A equals the amount of T.', True), ('Purines are adenine and guanine.', True), ('Cytosine is a purine.', False), ('The base–sugar link in a nucleoside is a glycosidic bond.', True), ('Proteins are synthesised by DNA directly.', False)]
# ---------- vitamins ----------
VIT = {'A': ('retinol', 'fat', 'night blindness, xerophthalmia'), 'B1': ('thiamine', 'water', 'beriberi'), 'B2': ('riboflavin', 'water', 'cheilosis, digestive disorders'), 'B6': ('pyridoxine', 'water', 'convulsions'),
       'B12': ('cyanocobalamin', 'water', 'pernicious anaemia'), 'C': ('ascorbic acid', 'water', 'scurvy'), 'D': ('calciferol', 'fat', 'rickets, osteomalacia'), 'E': ('tocopherol', 'fat', 'increased fragility of RBCs, muscular weakness'),
       'K': ('phylloquinone', 'fat', 'increased blood-clotting time'), 'H': ('biotin', 'water', 'hair loss, dermatitis')}
FATSET = 'ADEK'
def isfat(v): return v in tuple(FATSET)
NAME2 = {'retinol': 'A', 'thiamine': 'B1', 'riboflavin': 'B2', 'pyridoxine': 'B6', 'cyanocobalamin': 'B12', 'ascorbic acid': 'C', 'calciferol': 'D', 'tocopherol': 'E', 'phylloquinone': 'K', 'biotin': 'H'}
DEF2 = {'night': 'A', 'beriberi': 'B1', 'cheilosis': 'B2', 'convulsions': 'B6', 'pernicious': 'B12', 'scurvy': 'C', 'rickets': 'D', 'fragility': 'E', 'clotting': 'K', 'hair': 'H'}

def letterset(rng, bank, sub, want_true=True):
    """five statements A–E; options are letter sets; exactly one option lists the wanted ones"""
    st = rng.sample(bank, 5); truth = ''.join(k for k, (_, v) in zip('ABCDE', st) if v == want_true); need(1 <= len(truth) <= 4)
    pool = set()
    for r in (2, 3):
        for c in itertools.combinations('ABCDE', r): pool.add(''.join(c))
    pool.discard(truth); wr = rng.sample(sorted(pool), 6)
    fmt = lambda s: (', '.join(s[:-1]) + ' and ' + s[-1] if len(s) > 1 else s) + ' only'
    o, a = mcq(rng, fmt(truth), [fmt(w) for w in wr])
    q = f'Identify the {"correct" if want_true else "incorrect"} statements ({sub}): ' + ' '.join(f'{k}. {s}' for k, (s, _) in zip('ABCDE', st))
    return dict(q=q, o=o, a=a, sol=['; '.join(f'{k} {"true" if v else "false"}' for k, (_, v) in zip('ABCDE', st)) + '.'], p=dict(t='set', st=[s for s, _ in st], want=want_true))
ALLF = dict(PROT_F + CARB_F + NUC_F)

def g_carb(rng):
    t = rng.choice(['link', 'link2', 'hyd', 'grx', 'grx2', 'red', 'cnt', 'fact', 'set', 'mass'])
    if t == 'link':
        s = rng.choice(list(LINK)); o, a = mcq(rng, LINK[s], sorted(set(LINK.values()) - {LINK[s]}) + ['β1–6', 'α1–6 only'])
        return dict(q=f'The glycosidic linkage present in {s} is', o=o, a=a, sol=[f'{s}: {LINK[s]}.'], p=dict(t=t, s=s))
    if t == 'link2':
        L = rng.choice(sorted(set(LINK.values()))); r = rng.choice([s for s in LINK if LINK[s] == L]); o, a = mcq(rng, r, rng.sample([s for s in LINK if LINK[s] != L], 3))
        return dict(q=f'Which saccharide contains {L} glycosidic linkage(s)?', o=o, a=a, sol=[f'{r}: {L}.'], p=dict(t=t, L=L))
    if t == 'hyd':
        s = rng.choice(list(HYD)); o, a = mcq(rng, HYD[s], sorted(set(HYD.values()) - {HYD[s]}) + ['galactose only', 'fructose only', 'glucose and mannose'])
        return dict(q=f'Complete acid hydrolysis of {s} gives', o=o, a=a, sol=[f'{s} → {HYD[s]}.'], p=dict(t=t, s=s))
    if t == 'grx':
        r, pr = rng.choice(GRX); o, a = mcq(rng, pr, [x for _, x in rng.sample(GRX, 6) if x != pr]); return dict(q=f'Glucose reacts with {r} to give', o=o, a=a, sol=[f'{r} → {pr}.'], p=dict(t=t, r=r))
    if t == 'grx2':
        r, pr = rng.choice(GRX); o, a = mcq(rng, r, [x for x, _ in rng.sample(GRX, 6) if x != r]); return dict(q=f'Which reagent converts glucose into {pr}?', o=o, a=a, sol=[f'{r}.'], p=dict(t=t, pr=pr))
    if t == 'red':
        want = rng.choice([True, False]); r = rng.choice([s for s in REDUCING if REDUCING[s] == want]); o, a = mcq(rng, r, rng.sample([s for s in REDUCING if REDUCING[s] != want], 3))
        return dict(q=f'Which of the following is a {"reducing" if want else "NON-reducing"} sugar?', o=o, a=a, sol=[f'{r}: {"free hemiacetal/hemiketal carbon" if want else "no free anomeric carbon"}.'], p=dict(t=t, want=want))
    if t == 'cnt':
        pool = rng.sample(list(REDUCING), rng.randint(5, 8)); k = sum(REDUCING[s] for s in pool)
        return dict(q='How many of the following reduce Fehling\'s solution? ' + ', '.join(pool), o=None, a=k, sol=['Reducing: ' + ', '.join(s for s in pool if REDUCING[s]) + f' → {k}.'], p=dict(t=t, pool=pool))
    if t == 'set': return letterset(rng, CARB_F, 'carbohydrates', rng.choice([True, False]))
    if t == 'mass':
        s, f, prods = rng.choice([('sucrose', 'C12H22O11', 'glucose'), ('maltose', 'C12H22O11', 'glucose'), ('lactose', 'C12H22O11', 'galactose')]); w = rng.choice([17.1, 34.2, 68.4, 85.5, 171, 3.42, 51.3]); n2 = 2 if s == 'maltose' else 1
        g = w / 342 * n2 * 180
        return dict(q=f'{nf(w, 4)} g of {s} is completely hydrolysed. Mass of {prods} formed = ____ g (nearest integer).', o=None, a=round(g), sol=[f'{s} (342) gives {n2} mol {prods} (180) per mol: {nf(w, 4)}/342 × {n2} × 180 = {nf(g, 4)} g.'], p=dict(t=t, s=s, w=w))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in CARB_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in CARB_F if v != want], 3))
    return dict(q=f'Which statement about carbohydrates is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

def g_prot(rng):
    t = rng.choice(['perm', 'perm2', 'pb', 'ess', 'ess2', 'atoms', 'hno2', 'pct', 'mass', 'level', 'fact', 'set'])
    t = 'dmass' if t == 'mass' else t
    names = list(AA)
    if t == 'perm':
        n = rng.randint(2, 5); ps = rng.sample(names, n)
        return dict(q=f'Number of different {["", "", "di", "tri", "tetra", "penta"][n]}peptides that contain each of ' + ', '.join(ps) + ' exactly once:', o=None, a=math.factorial(n), sol=[f'Ordered sequences of {n} different residues: {n}! = {math.factorial(n)}.'], p=dict(t=t, ps=ps))
    if t == 'perm2':
        n = rng.randint(2, 4); k = rng.randint(2, 3); ps = rng.sample(names, n); rep = rng.choice([True, False]); need(rep or k <= n)
        v = n ** k if rep else math.perm(n, k); nm = {2: 'dipeptides', 3: 'tripeptides'}[k]
        return dict(q=f'Using only {", ".join(ps)}, how many {nm} are possible if an amino acid {"may be repeated" if rep else "may be used at most once"}?', o=None, a=v, sol=[f'{"n^k" if rep else "nPk"} = {v}.'], p=dict(t=t, n=n, k=k, rep=rep))
    if t == 'pb':
        n = rng.randint(3, 60); w = rng.choice(['peptide bonds', 'water molecules eliminated in forming it'])
        return dict(q=f'A linear polypeptide contains {n} amino-acid residues. Number of {w} = ____', o=None, a=n - 1, sol=[f'n residues are joined by n − 1 amide links, each releasing one H_{{2}}O → {n - 1}.'], p=dict(t=t, n=n))
    if t == 'ess':
        pool = rng.sample(names, rng.randint(5, 8)); k = sum(AA[x][3] for x in pool)
        return dict(q='Number of essential amino acids among: ' + ', '.join(pool), o=None, a=k, sol=['Essential: ' + (', '.join(x for x in pool if AA[x][3]) or 'none') + f' → {k}.'], p=dict(t=t, pool=pool))
    if t == 'ess2':
        want = rng.choice([True, False]); r = rng.choice([x for x in names if AA[x][3] == want]); o, a = mcq(rng, r, rng.sample([x for x in names if AA[x][3] != want], 3))
        return dict(q=f'Which is {"an essential" if want else "a NON-essential"} amino acid?', o=o, a=a, sol=[f'{r} is {"essential" if want else "non-essential"}.'], p=dict(t=t, want=want))
    if t == 'atoms':
        x = rng.choice(names); el = rng.choice(['C', 'N', 'O', 'H']); k = cnt(AA[x][1], el)
        return dict(q=f'Total number of {el} atoms in one molecule of {x}:', o=None, a=k, sol=[f'{x} = {AA[x][1]} → {k}.'], p=dict(t=t, x=x, el=el))
    if t == 'hno2':
        x = rng.choice(list(HNO2)); o, a = mcq(rng, HNO2[x], [v for k, v in HNO2.items() if k != x])
        return dict(q=f'{x.capitalize()} on treatment with aqueous HNO_{{2}} gives', o=o, a=a, sol=['H_{2}N–CHR–COOH + HNO_{2} → HO–CHR–COOH + N_{2} + H_{2}O.'], p=dict(t=t, x=x))
    if t == 'pct':
        x = rng.choice(names); el = rng.choice(['N', 'C', 'O']); v = 100 * cnt(AA[x][1], el) * AM[el] / mm(AA[x][1])
        need(abs(v - round(v) - 0.5) > 0.05)
        return dict(q=f'Percentage by mass of {el} in {x} ({AA[x][1]}) = ____ % (nearest integer). (C 12, H 1, N 14, O 16, S 32)', o=None, a=round(v), sol=[f'M = {mm(AA[x][1])}; {el}: {cnt(AA[x][1], el) * AM[el]} → {nf(v, 4)}%.'], p=dict(t=t, x=x, el=el))
    if t == 'dmass':
        a1, a2 = rng.sample(names, 2); v = mm(AA[a1][1]) + mm(AA[a2][1]) - 18
        return dict(q=f'Molar mass (g mol^{{−1}}) of the dipeptide {AA[a1][0]}-{AA[a2][0]} formed from {a1} and {a2} = ____ (C 12, H 1, N 14, O 16, S 32)', o=None, a=v, sol=[f'{mm(AA[a1][1])} + {mm(AA[a2][1])} − 18 (H_{{2}}O lost) = {v}.'], p=dict(t='dmass', a1=a1, a2=a2))
    if t == 'level':
        d, lv = rng.choice(LEVEL); o, a = mcq(rng, lv + ' structure', ['primary structure', 'secondary structure', 'tertiary structure', 'quaternary structure'])
        return dict(q=f'"{d.capitalize()}" describes which level of protein structure?', o=o, a=a, sol=[f'{lv}.'], p=dict(t=t, d=d))
    if t == 'set': return letterset(rng, PROT_F, 'amino acids, proteins, enzymes', rng.choice([True, False]))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in PROT_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in PROT_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

PAIR = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
def g_nucl(rng):
    t = rng.choice(['comp', 'rna', 'hb', 'chargaff', 'fact', 'set', 'pur'])
    if t in ('comp', 'rna'):
        s = ''.join(rng.choice('ATGC') for _ in range(rng.randint(7, 10))); c = ''.join(PAIR[b] for b in s)
        if t == 'rna': c = c.replace('T', 'U')
        wr = [c[::-1], s, s.replace('T', 'U') if t == 'rna' else s[::-1], ''.join({'A': 'G', 'G': 'A', 'T': 'C', 'C': 'T'}[b] for b in s), (c.replace('U', 'T') if t == 'rna' else c.replace('T', 'U'))]
        o, a = mcq(rng, c, wr)
        q = f'One DNA strand reads {s}. The {"complementary DNA strand" if t == "comp" else "mRNA transcribed using it as the template"} reads' + ('' if t == 'comp' else ' (same direction as written)')
        return dict(q=q, o=o, a=a, sol=['A pairs with T (U in RNA), G with C.', f'{s} → {c}.'], p=dict(t=t, s=s))
    if t == 'hb':
        s = ''.join(rng.choice('ATGC') for _ in range(rng.randint(8, 16))); gc = sum(b in 'GC' for b in s); v = 3 * gc + 2 * (len(s) - gc)
        return dict(q=f'Total number of hydrogen bonds between the two strands of a DNA segment whose one strand is 5′-{s}-3′:', o=None, a=v, sol=[f'G/C pairs {gc} × 3 + A/T pairs {len(s) - gc} × 2 = {v}.'], p=dict(t=t, s=s))
    if t == 'chargaff':
        x = rng.randint(10, 40); b = rng.choice('ATGC'); ask = rng.choice([q for q in 'ATGC' if q != b]); same = PAIR[b] == ask; v = x if same else 50 - x
        return dict(q=f'A double-stranded DNA sample contains {x}% {b} (by number of bases). Percentage of {ask} = ____', o=None, a=v, sol=[f'Chargaff: A = T, G = C, A + G = 50%. {ask} = {v}%.'], p=dict(t=t, x=x, b=b, ask=ask))
    if t == 'pur':
        want = rng.choice(['purine', 'pyrimidine']); P = ['adenine', 'guanine']; Y = ['cytosine', 'thymine', 'uracil']; r = rng.choice(P if want == 'purine' else Y)
        o, a = mcq(rng, r, (Y if want == 'purine' else P) + ['ribose', 'phosphate']); return dict(q=f'Which base is a {want}?', o=o, a=a, sol=['Purines (two rings): A, G. Pyrimidines (one ring): C, T, U.'], p=dict(t=t, want=want))
    if t == 'set': return letterset(rng, NUC_F, 'nucleic acids', rng.choice([True, False]))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in NUC_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in NUC_F if v != want], 3))
    return dict(q=f'Which statement about nucleic acids is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

def g_vit(rng):
    t = rng.choice(['name', 'name2', 'def', 'def2', 'sol', 'store', 'which'])
    V = list(VIT)
    if t == 'name':
        v = rng.choice(V); o, a = mcq(rng, VIT[v][0], [VIT[w][0] for w in rng.sample(V, 6) if w != v]); return dict(q=f'Chemical name of vitamin {v}:', o=o, a=a, sol=[f'Vitamin {v} = {VIT[v][0]}.'], p=dict(t=t, v=v))
    if t == 'name2':
        v = rng.choice(V); o, a = mcq(rng, f'Vitamin {v}', [f'Vitamin {w}' for w in rng.sample(V, 6) if w != v]); return dict(q=f'{VIT[v][0].capitalize()} is', o=o, a=a, sol=[f'{VIT[v][0]} = vitamin {v}.'], p=dict(t=t, n=VIT[v][0]))
    if t == 'def':
        v = rng.choice(V); o, a = mcq(rng, VIT[v][2], [VIT[w][2] for w in rng.sample(V, 6) if w != v]); return dict(q=f'Deficiency of vitamin {v} causes', o=o, a=a, sol=[f'{v}: {VIT[v][2]}.'], p=dict(t=t, v=v))
    if t == 'def2':
        v = rng.choice(V); o, a = mcq(rng, f'Vitamin {v}', [f'Vitamin {w}' for w in rng.sample(V, 6) if w != v]); return dict(q=f'"{VIT[v][2].capitalize()}" is caused by lack of', o=o, a=a, sol=[f'Vitamin {v}.'], p=dict(t=t, d=VIT[v][2]))
    if t in ('sol', 'store'):
        pool = rng.sample(V, rng.randint(5, 8)); k = sum(1 for v in pool if VIT[v][1] == 'fat' or (t == 'store' and v == 'B12'))
        q = 'Number of fat-soluble vitamins among: ' if t == 'sol' else 'Number of vitamins that can be stored in the body among: '
        return dict(q=q + ', '.join(pool), o=None, a=k, sol=['Fat-soluble: A, D, E, K' + (' (stored), plus B_{12} stored in the liver' if t == 'store' else '') + f' → {k}.'], p=dict(t=t, pool=pool))
    want = rng.choice(['fat', 'water']); r = rng.choice([v for v in V if VIT[v][1] == want]); o, a = mcq(rng, f'Vitamin {r}', [f'Vitamin {v}' for v in rng.sample(V, 8) if VIT[v][1] != want])
    return dict(q=f'Which vitamin is {want}-soluble?', o=o, a=a, sol=['Fat-soluble: A, D, E, K; the rest (B-group, C, H) are water-soluble.'], p=dict(t=t, want=want))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(carb=g_carb, prot=g_prot, nucl=g_nucl, vit=g_vit).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def _ess(x): return ONE[x] in ESS_CODES
def _lev(d): return next(v for k, v in LEV2.items() if k in d)
def _vit_by_name(n): return NAME2[n]
def _vit_by_def(d): return next(v for k, v in DEF2.items() if k in d)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'link': return R == l2s(LINK2[p['s']])
    if t == 'link2': return l2s(LINK2[R]) == p['L']
    if t == 'hyd':
        L = [NM[k] for k in ('glc', 'fru', 'gal') if k in HYD2[p['s']]]
        return R == (L[0] + ' only' if len(L) == 1 else ', '.join(L[:-1]) + ' and ' + L[-1])
    if t == 'grx': return GRX2[next(k for k in GRX2 if k in R)] == gkey(p['r'])
    if t == 'grx2': return GRX2[next(k for k in GRX2 if k in p['pr'])] == gkey(R)
    if t == 'red': return bool(FREE_ANOMER[R]) == p['want']
    if t == 'cnt': return R == sum(FREE_ANOMER[s] for s in p['pool'])
    if t == 'mass': return R == round(p['w'] / mm('C12H22O11') * (2 if p['s'] == 'maltose' else 1) * mm('C6H12O6'))
    if t == 'set':
        L = re.findall(r'\b([A-E])\b', R.replace(' only', '')); return ''.join(L) == ''.join(k for k, s in zip('ABCDE', p['st']) if ALLF[s] == p['want'])
    if t == 'fact': return ALLF[R] == p['want']
    if t == 'perm': return R == sum(1 for _ in itertools.permutations(p['ps']))
    if t == 'perm2': return R == sum(1 for _ in (itertools.product(range(p['n']), repeat=p['k']) if p['rep'] else itertools.permutations(range(p['n']), p['k'])))
    if t == 'pb': return R == len(['–CO–NH–' for _ in range(p['n'])][1:])
    if t == 'ess': return R == sum(_ess(x) for x in p['pool'])
    if t == 'ess2': return _ess(R) == p['want']
    if t == 'atoms': return R == from_r(AA[p['x']][2])[p['el']]
    if t == 'hno2': return R == HNO2[p['x']]
    if t == 'pct':
        d = from_r(AA[p['x']][2]); M = sum(AM[e] * n for e, n in d.items()); return R == round(100 * d[p['el']] * AM[p['el']] / M)
    if t == 'dmass':
        return R == sum(sum(AM[e] * n for e, n in from_r(AA[x][2]).items()) for x in (p['a1'], p['a2'])) - 18
    if t == 'level': return R == _lev(p['d']) + ' structure'
    if t == 'comp': return R == p['s'].translate(str.maketrans('ATGC', 'TACG'))
    if t == 'rna': return R == p['s'].translate(str.maketrans('ATGC', 'UACG'))
    if t == 'hb': return R == 3 * len(re.findall('[GC]', p['s'])) + 2 * len(re.findall('[AT]', p['s']))
    if t == 'chargaff': return R == (p['x'] if {p['b'], p['ask']} in ({'A', 'T'}, {'G', 'C'}) else 50 - p['x'])
    if t == 'pur': return (R in ('adenine', 'guanine')) == (p['want'] == 'purine')
    if t == 'name': return _vit_by_name(R) == p['v']
    if t == 'name2': return R == 'Vitamin ' + _vit_by_name(p['n'])
    if t == 'def': return _vit_by_def(R) == p['v']
    if t == 'def2': return R == 'Vitamin ' + _vit_by_def(p['d'])
    if t == 'sol': return R == sum(1 for v in p['pool'] if v in ('A', 'D', 'E', 'K'))
    if t == 'store': return R == sum(1 for v in p['pool'] if v in ('A', 'D', 'E', 'K', 'B12'))
    if t == 'which': return (R.split()[-1] in ('A', 'D', 'E', 'K')) == (p['want'] == 'fat')
    raise KeyError(t)
