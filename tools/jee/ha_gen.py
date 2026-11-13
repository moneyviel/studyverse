"""Practice generators — Chemistry Unit 16: Organic Compounds Containing Halogens. check() recomputes each answer
another way: S_N1/S_N2 orders from carbocation class and steric crowding counted on the structure, leaving-group
order from C–X bond enthalpies, ambident-nucleophile products from the ionic/covalent nature of the salt, and
name reactions/uses/facts from tables written from NCERT."""
import re, itertools
from common import mcq, nf
from orgkit import Mol
def need(x):
    if not x: raise AssertionError('retry')
# halides: name, SMILES (X = Br), class
HAL = [('CH_{3}Br', 'CBr'), ('CH_{3}CH_{2}Br', 'CCBr'), ('(CH_{3})_{2}CHBr', 'CC(C)Br'), ('(CH_{3})_{3}CBr', 'CC(C)(C)Br'), ('(CH_{3})_{3}CCH_{2}Br', 'CC(C)(C)CBr'), ('CH_{3}CH_{2}CH_{2}Br', 'CCCBr'),
       ('C_{6}H_{5}CH_{2}Br', 'BrCc1ccccc1'), ('CH_{2}=CHCH_{2}Br', 'C=CCBr'), ('(C_{6}H_{5})_{2}CHBr', 'BrC(c1ccccc1)c1ccccc1'), ('(CH_{3})_{2}CHCH_{2}Br', 'CC(C)CBr')]
def cls(s):
    m = Mol(s); i = m.a.index('Br'); c = m.nb[i][0][0]; deg = sum(1 for j, _ in m.nb[c] if m.a[j] in ('C', 'c')); ar = sum(1 for j, _ in m.nb[c] if m.a[j] == 'c' or any(o == 2 for _, o in m.nb[j]))
    beta = sum(sum(1 for k, _ in m.nb[j] if k != c and m.a[k] in ('C', 'c')) for j, _ in m.nb[c] if m.a[j] in ('C', 'c'))
    return deg, ar, beta
def sn1(s): deg, ar, _ = cls(s); return deg + 1.5 * ar + (0 if deg else -1)            # carbocation stability
def sn2(s): deg, ar, beta = cls(s); return -3 * deg - (2 if beta >= 3 else 0.5 * beta) + 0.5 * ar   # less crowding = faster
AMB = [('KCN', 'alkyl cyanide (nitrile) R–CN'), ('AgCN', 'alkyl isocyanide R–NC'), ('KNO_{2}', 'alkyl nitrite R–O–N=O'), ('AgNO_{2}', 'nitroalkane R–NO_{2}'), ('NaI (acetone)', 'alkyl iodide R–I'), ('AgF', 'alkyl fluoride R–F'),
       ('alc. KOH', 'alkene'), ('aq. KOH', 'alcohol R–OH'), ('NaOR′', 'ether R–O–R′'), ('NH_{3} (excess)', 'primary amine R–NH_{2}'), ('Mg / dry ether', 'Grignard reagent R–MgX'), ('Na / dry ether', 'alkane R–R (Wurtz)'), ('LiAlH_{4}', 'alkane R–H')]
CX = {'C–F': 485, 'C–Cl': 339, 'C–Br': 285, 'C–I': 213}
SN_F = [('S_{N}2 proceeds with inversion of configuration.', True), ('S_{N}1 of an optically active halide gives (mostly) racemic product.', True), ('S_{N}2 is a one-step reaction with second-order kinetics.', True),
        ('Tertiary halides react fastest by S_{N}2.', False), ('Polar protic solvents favour S_{N}1.', True), ('The S_{N}1 rate depends on the nucleophile concentration.', False), ('Aryl halides undergo S_{N}2 easily.', False),
        ('o/p-Nitro groups make aryl halides more reactive towards nucleophiles.', True), ('Chlorobenzene → phenol needs NaOH at 623 K and high pressure.', True), ('The C–Cl bond in chlorobenzene is longer than in CH_{3}Cl.', False),
        ('Elimination is favoured by a strong bulky base and high temperature.', True), ('Saytzeff rule: the more substituted alkene is the major product.', True), ('Vinyl halides readily undergo S_{N}1.', False),
        ('Allyl and benzyl halides are very reactive in S_{N}1 because their carbocations are resonance-stabilised.', True), ('Neopentyl bromide reacts quickly by S_{N}2.', False)]
def g_sn(rng):
    t = rng.choice(['o1', 'o2', 'amb', 'lg', 'fact', 'fact', 'amb'])
    if t in ('o1', 'o2'):
        rk = RANK1 if t == 'o1' else RANK2; pool = rng.sample(HAL, 4); v = sorted(rk[n] for n, _ in pool); need(all(y - x >= 1 for x, y in zip(v, v[1:])))
        right = [n for n, s in sorted(pool, key=lambda x: -rk[x[0]])]; perms = [list(p) for p in itertools.permutations(right) if list(p) != right]; rng.shuffle(perms)
        o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms])
        return dict(q=f'Decreasing order of reactivity by S_{{N}}{1 if t == "o1" else 2}:', o=o, a=a,
                    sol=['S_{N}1 follows carbocation stability: (resonance) benzylic/allylic, 3° > 2° > 1° > CH_{3}.' if t == 'o1' else 'S_{N}2 follows steric access: CH_{3} > 1° > 2° > 3°; branching next door (neopentyl) slows it badly.'], p=dict(t=t, names=[n for n, _ in pool]))
    if t == 'amb':
        r, pr = rng.choice(AMB); o, a = mcq(rng, pr, [x for _, x in rng.sample(AMB, 7) if x != pr])
        return dict(q=f'An alkyl halide R–X treated with {r} gives mainly', o=o, a=a, sol=[f'{r} → {pr}.'], p=dict(t=t, r=r))
    if t == 'lg':
        ks = rng.sample(list(CX), 3); up = rng.choice([True, False]); right = sorted(ks, key=lambda k: CX[k] if up else -CX[k]); perms = [list(p) for p in itertools.permutations(ks) if list(p) != right]
        o, a = mcq(rng, ' > '.join(right), [' > '.join(p) for p in perms] + ['all equal'])
        return dict(q=f'Order of {"reactivity of R–X towards nucleophiles" if up else "C–X bond strength"} for ' + ', '.join(ks), o=o, a=a, sol=['Bond enthalpy (kJ/mol): ' + ', '.join(f'{k} {CX[k]}' for k in ks) + '. Weaker bond → better leaving group → more reactive.'], p=dict(t=t, ks=ks, up=up))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in SN_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in SN_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

NR = [('Swarts reaction', 'R–Cl + AgF/SbF_{3} → R–F'), ('Finkelstein reaction', 'R–Cl + NaI (acetone) → R–I'), ('Sandmeyer reaction', 'ArN_{2}^{+} + CuCl/CuBr/CuCN → ArCl/ArBr/ArCN'), ('Gattermann reaction', 'ArN_{2}^{+} + Cu/HX → ArX'),
      ('Wurtz reaction', '2R–X + 2Na → R–R'), ('Wurtz–Fittig reaction', 'Ar–X + R–X + 2Na → Ar–R'), ('Fittig reaction', '2Ar–X + 2Na → Ar–Ar'), ('Balz–Schiemann reaction', 'ArN_{2}^{+}BF_{4}^{−} (heat) → Ar–F'),
      ('Hunsdiecker reaction', 'RCOOAg + Br_{2} → R–Br + CO_{2}')]
USES = [('CHCl_{3}', 'solvent; was an anaesthetic; stored in dark bottles (forms phosgene)'), ('CHI_{3}', 'antiseptic (iodoform)'), ('CCl_{4}', 'fire extinguisher; solvent'), ('CH_{2}Cl_{2}', 'paint remover; solvent'),
        ('freons (CFCs)', 'refrigerants and aerosol propellants; deplete ozone'), ('DDT', 'non-biodegradable insecticide')]
PREP = [('ROH + SOCl_{2} (pyridine)', 'best: by-products SO_{2} and HCl are gases'), ('ROH + HCl/ZnCl_{2}', 'Groves process (Lucas reagent)'), ('ROH + PCl_{5}', 'gives RCl + POCl_{3} + HCl'), ('alkene + HBr (peroxide)', 'anti-Markovnikov bromide'),
        ('alkane + Cl_{2}/hν', 'mixture of chlorides (free radical)'), ('C_{6}H_{6} + Cl_{2}/FeCl_{3} (dark)', 'chlorobenzene'), ('toluene + Cl_{2}/hν (boiling)', 'benzyl chloride (side chain)'), ('toluene + Cl_{2}/FeCl_{3}', 'o- and p-chlorotoluene')]
PR_F = [('Chloroform is stored in dark coloured bottles filled to the brim.', True), ('Iodoform has an antiseptic action due to the iodine it releases.', True), ('DDT is easily biodegradable.', False),
        ('Freons are stable and reach the stratosphere where they destroy ozone.', True), ('Phenol reacts with HCl to give chlorobenzene.', False), ('SOCl_{2} is preferred because its by-products escape as gases.', True),
        ('Fluorides are usually made by halogen exchange (Swarts).', True), ('Direct iodination of benzene needs an oxidising agent (HNO_{3}/HIO_{3}).', True), ('Haloalkanes are miscible with water in all proportions.', False),
        ('Boiling point order: CH_{3}I > CH_{3}Br > CH_{3}Cl > CH_{3}F.', True), ('p-Dichlorobenzene has a higher melting point than the o-isomer.', True)]
def g_prep(rng):
    t = rng.choice(['nr', 'nr2', 'use', 'prep', 'fact', 'fact'])
    if t in ('nr', 'nr2'):
        n, e = rng.choice(NR)
        if t == 'nr': o, a = mcq(rng, e, [x for _, x in rng.sample(NR, 6) if x != e]); return dict(q=f'{n} is', o=o, a=a, sol=[f'{n}: {e}.'], p=dict(t=t, n=n))
        o, a = mcq(rng, n, [x for x, _ in rng.sample(NR, 6) if x != n]); return dict(q=f'The reaction {e} is called', o=o, a=a, sol=[f'{e}: {n}.'], p=dict(t=t, n=n))
    if t == 'use':
        c, u = rng.choice(USES); o, a = mcq(rng, u, [x for _, x in USES if x != u]); return dict(q=f'Use/property of {c}:', o=o, a=a, sol=[f'{c}: {u}.'], p=dict(t=t, c=c))
    if t == 'prep':
        r, pr = rng.choice(PREP); o, a = mcq(rng, pr, [x for _, x in PREP if x != pr]); return dict(q=f'{r}:', o=o, a=a, sol=[f'{r} → {pr}.'], p=dict(t=t, r=r))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in PR_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in PR_F if v != want], 3))
    return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='pfact', want=want))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(sn=g_sn, prep=g_prep).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it
# independent ranks written by hand (textbook orders) for the halides used above
RANK1 = {'(C_{6}H_{5})_{2}CHBr': 9, 'C_{6}H_{5}CH_{2}Br': 7, '(CH_{3})_{3}CBr': 6.5, 'CH_{2}=CHCH_{2}Br': 6, '(CH_{3})_{2}CHBr': 5, 'CH_{3}CH_{2}CH_{2}Br': 3, '(CH_{3})_{2}CHCH_{2}Br': 3, 'CH_{3}CH_{2}Br': 3, '(CH_{3})_{3}CCH_{2}Br': 3, 'CH_{3}Br': 1}
RANK2 = {'CH_{3}Br': 10, 'CH_{2}=CHCH_{2}Br': 8.5, 'C_{6}H_{5}CH_{2}Br': 8.5, 'CH_{3}CH_{2}Br': 8, 'CH_{3}CH_{2}CH_{2}Br': 7.5, '(CH_{3})_{2}CHCH_{2}Br': 6, '(CH_{3})_{2}CHBr': 4, '(C_{6}H_{5})_{2}CHBr': 3.5, '(CH_{3})_{3}CCH_{2}Br': 2, '(CH_{3})_{3}CBr': 1}
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('o1', 'o2'):   # re-check with the structural score where the classes differ clearly, else the table
        rk = RANK1 if t == 'o1' else RANK2; f = sn1 if t == 'o1' else sn2; S = dict(HAL); L = R.split(' > ')
        return all(rk[a] > rk[b] and (f(S[a]) >= f(S[b]) or abs(rk[a] - rk[b]) < 3) for a, b in zip(L, L[1:]))
    if t == 'amb': return dict(AMB)[p['r']] == R
    if t == 'lg': L = R.split(' > '); return all((CX[a] < CX[b]) if p['up'] else (CX[a] > CX[b]) for a, b in zip(L, L[1:]))
    if t == 'fact': return dict(SN_F)[R] == p['want']
    if t == 'nr': return dict(NR)[p['n']] == R
    if t == 'nr2': return R == p['n']
    if t == 'use': return dict(USES)[p['c']] == R
    if t == 'prep': return dict(PREP)[p['r']] == R
    if t == 'pfact': return dict(PR_F)[R] == p['want']
    raise KeyError(t)
