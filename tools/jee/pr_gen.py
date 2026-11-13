"""Practice generators — Chemistry Unit 20: Principles Related to Practical Chemistry. check() re-derives answers
another way: group from a reagent ladder walked in order, flame/test results from a second table keyed by colour,
precipitation pH from logs of Ksp, titrations from balanced-equation mole ratios (generators use n-factors)."""
import re, math
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
# ---------- cation analysis ----------
GROUP = {'Pb^{2+}': 1, 'Ag^{+}': 1, 'Hg_{2}^{2+}': 1, 'Cu^{2+}': 2, 'Cd^{2+}': 2, 'As^{3+}': 2, 'Bi^{3+}': 2, 'Al^{3+}': 3, 'Fe^{3+}': 3, 'Cr^{3+}': 3, 'Zn^{2+}': 4, 'Ni^{2+}': 4, 'Co^{2+}': 4, 'Mn^{2+}': 4,
         'Ba^{2+}': 5, 'Ca^{2+}': 5, 'Sr^{2+}': 5, 'Mg^{2+}': 6, 'NH_{4}^{+}': 0, 'K^{+}': 6}
REAG = {0: 'none (tested in the original salt with NaOH)', 1: 'dil. HCl', 2: 'H_{2}S in presence of dil. HCl', 3: 'NH_{4}OH in presence of NH_{4}Cl', 4: 'H_{2}S in presence of NH_{4}OH', 5: '(NH_{4})_{2}CO_{3} in presence of NH_{4}OH', 6: 'no group reagent (group VI)'}
PPT = {1: 'chlorides', 2: 'sulphides', 3: 'hydroxides', 4: 'sulphides', 5: 'carbonates'}
LADDER = [('Pb Ag Hg_{2}', 'chlorides'), ('Cu Cd As Bi', 'sulphides'), ('Al Fe Cr', 'hydroxides'), ('Zn Ni Co Mn', 'sulphides'), ('Ba Ca Sr', 'carbonates')]   # independent: walk groups I→V
def sym(c): return re.match(r'[A-Z][a-z]?', c).group(0) + ('_{2}' if c.startswith('Hg_{2}') else '')
def grp2(c):
    if c.startswith('NH'): return 0
    for i, (ms, _) in enumerate(LADDER):
        if sym(c) in ms.split(): return i + 1
    return 6
FLAME = {'Ca^{2+}': 'brick red', 'Sr^{2+}': 'crimson red', 'Ba^{2+}': 'apple green', 'Cu^{2+}': 'green-blue', 'Na^{+}': 'golden yellow', 'K^{+}': 'lilac (violet)'}
FL2 = {'brick': 'Ca', 'crimson': 'Sr', 'apple': 'Ba', 'green-blue': 'Cu', 'golden': 'Na', 'lilac': 'K'}
NOFLAME = ['Zn^{2+}', 'Fe^{2+}', 'Fe^{3+}', 'Al^{3+}', 'Mg^{2+}', 'Ni^{2+}', 'Co^{2+}', 'Mn^{2+}', 'NH_{4}^{+}', 'Pb^{2+}']
CONF = [('Ni^{2+}', 'dimethylglyoxime in NH_{4}OH → rose-red precipitate'), ('Fe^{3+}', 'K_{4}[Fe(CN)_{6}] → Prussian blue'), ('Cu^{2+}', 'K_{4}[Fe(CN)_{6}] (acetic acid) → chocolate-brown precipitate'),
        ('Zn^{2+}', 'K_{4}[Fe(CN)_{6}] → bluish-white precipitate'), ('Pb^{2+}', 'KI → yellow precipitate soluble in hot water'), ('Ba^{2+}', 'K_{2}CrO_{4} → yellow precipitate'), ('Ca^{2+}', 'ammonium oxalate → white precipitate'),
        ('NH_{4}^{+}', "Nessler's reagent → brown precipitate"), ('Mg^{2+}', 'disodium hydrogen phosphate + NH_{4}OH → white crystalline precipitate'), ('Al^{3+}', 'blue litmus + NH_{4}OH → blue "lake"'),
        ('Co^{2+}', 'KNO_{2} + acetic acid → yellow precipitate'), ('Mn^{2+}', 'NaOH + Br_{2} water → black/brown precipitate'), ('Cr^{3+}', 'NaOH + H_{2}O_{2} → yellow solution (chromate), then lead acetate → yellow ppt')]
CONF2 = {'dimethylglyoxime': 'Ni', 'Prussian': 'Fe', 'chocolate': 'Cu', 'bluish-white': 'Zn', 'hot water': 'Pb', 'K_{2}CrO_{4}': 'Ba', 'oxalate': 'Ca', 'Nessler': 'NH', 'phosphate': 'Mg', 'lake': 'Al', 'KNO_{2}': 'Co', 'Br_{2}': 'Mn', 'H_{2}O_{2}': 'Cr'}
# ---------- anions / gases / elements ----------
ANION = [('CO_{3}^{2−}', 'dil. H_{2}SO_{4}: CO_{2} turns lime water milky'), ('S^{2−}', 'dil. H_{2}SO_{4}: H_{2}S blackens lead acetate paper'), ('SO_{3}^{2−}', 'dil. H_{2}SO_{4}: SO_{2} turns acidified K_{2}Cr_{2}O_{7} green'),
         ('NO_{2}^{−}', 'dil. H_{2}SO_{4}: brown NO_{2} fumes'), ('Cl^{−}', 'AgNO_{3}: white ppt soluble in NH_{4}OH'), ('Br^{−}', 'AgNO_{3}: pale-yellow ppt sparingly soluble in NH_{4}OH'), ('I^{−}', 'AgNO_{3}: yellow ppt insoluble in NH_{4}OH'),
         ('NO_{3}^{−}', 'FeSO_{4} + conc. H_{2}SO_{4}: brown ring'), ('SO_{4}^{2−}', 'BaCl_{2}: white ppt insoluble in conc. HCl'), ('PO_{4}^{3−}', 'ammonium molybdate + HNO_{3}: canary-yellow ppt'),
         ('CH_{3}COO^{−}', 'neutral FeCl_{3}: deep red colour'), ('C_{2}O_{4}^{2−}', 'acidified KMnO_{4} decolourised on warming')]
AN2 = {'lime water': 'CO', 'lead acetate': 'S^', 'K_{2}Cr_{2}O_{7}': 'SO_{3}', 'brown NO_{2}': 'NO_{2}', 'white ppt soluble': 'Cl', 'pale-yellow': 'Br', 'yellow ppt insoluble': 'I', 'brown ring': 'NO_{3}', 'BaCl_{2}': 'SO_{4}',
       'molybdate': 'PO', 'deep red': 'CH', 'KMnO_{4}': 'C_{2}'}
LAS = [('nitrogen', 'Prussian blue (FeSO_{4}, then FeCl_{3}/acid) — from NaCN'), ('sulphur', 'black PbS with lead acetate / violet with sodium nitroprusside — from Na_{2}S'), ('nitrogen and sulphur together', 'blood-red colour with FeCl_{3} — from NaSCN'),
       ('chlorine', 'white AgCl with AgNO_{3} (after boiling with HNO_{3})'), ('phosphorus', 'canary-yellow ammonium phosphomolybdate'), ('iodine', 'yellow AgI insoluble in NH_{4}OH')]
LAS2 = {'Prussian': 'nitrogen', 'PbS': 'sulphur', 'blood-red': 'nitrogen and sulphur together', 'AgCl': 'chlorine', 'phosphomolybdate': 'phosphorus', 'AgI': 'iodine'}
PR_F = [('NH_{4}Cl is added before NH_{4}OH in group III to lower [OH^{−}].', True), ('Group II sulphides are precipitated in alkaline medium.', False), ('Group IV sulphides need a high [S^{2−}], so H_{2}S is passed in ammoniacal medium.', True),
        ('Lassaigne extract is prepared by fusing the compound with sodium.', True), ('Blood-red colour in the Lassaigne test shows both N and S.', True), ('Before testing halogens, the Lassaigne extract is boiled with HNO_{3} to remove CN^{−} and S^{2−}.', True),
        ('Oxalic acid–KMnO_{4} titration is done at room temperature without heating.', False), ('KMnO_{4} acts as its own indicator.', True), ('Phenolphthalein is used for KMnO_{4} titrations.', False), ('Dil. H_{2}SO_{4} is added while preparing Mohr\'s salt to prevent hydrolysis of Fe^{2+}.', True),
        ('HCl is used to acidify KMnO_{4} titrations.', False), ('Ba^{2+} gives an apple-green flame.', True), ('Zn^{2+} gives a characteristic flame colour.', False), ('The brown ring test is for nitrate.', True), ('Potash alum is K_{2}SO_{4}·Al_{2}(SO_{4})_{3}·24H_{2}O.', True),
        ('Nessler\'s reagent detects NH_{4}^{+} as a brown precipitate.', True), ('AgI dissolves readily in NH_{4}OH.', False)]
PR_FD = dict(PR_F)

def g_cat(rng):
    t = rng.choice(['grp', 'reag', 'ppt', 'flame', 'flame2', 'fcnt', 'conf', 'conf2', 'ksp', 'first'])
    C = [c for c in GROUP if GROUP[c]]
    if t == 'grp':
        c = rng.choice(C); g = GROUP[c]; o, a = mcq(rng, f'group {["0", "I", "II", "III", "IV", "V", "VI"][g]}', [f'group {x}' for x in ['I', 'II', 'III', 'IV', 'V', 'VI'] if x != ['0', 'I', 'II', 'III', 'IV', 'V', 'VI'][g]])
        return dict(q=f'In qualitative analysis, {c} belongs to', o=o, a=a, sol=[f'{c}: group reagent {REAG[g]}.'], p=dict(t=t, c=c))
    if t == 'reag':
        c = rng.choice([x for x in C if GROUP[x] <= 5]); g = GROUP[c]; o, a = mcq(rng, REAG[g], [REAG[k] for k in range(1, 6) if k != g])
        return dict(q=f'The group reagent that precipitates {c} is', o=o, a=a, sol=[f'{c} is in group {g}: {REAG[g]}.'], p=dict(t=t, c=c))
    if t == 'ppt':
        c = rng.choice([x for x in C if GROUP[x] <= 5]); g = GROUP[c]; o, a = mcq(rng, PPT[g], ['chlorides', 'sulphides', 'hydroxides', 'carbonates', 'sulphates', 'phosphates'])
        return dict(q=f'In group analysis, {c} is precipitated as its', o=o, a=a, sol=[f'Group {g} → {PPT[g]}.'], p=dict(t=t, c=c))
    if t == 'flame':
        c = rng.choice(list(FLAME)); o, a = mcq(rng, FLAME[c], [v for k, v in FLAME.items() if k != c] + ['no characteristic colour'])
        return dict(q=f'Flame colour given by {c} (with conc. HCl) is', o=o, a=a, sol=[f'{c}: {FLAME[c]}.'], p=dict(t=t, c=c))
    if t == 'flame2':
        c = rng.choice(list(FLAME)); o, a = mcq(rng, c, [k for k in FLAME if k != c] + rng.sample(NOFLAME, 2))
        return dict(q=f'A salt gives a {FLAME[c]} flame. The cation is', o=o, a=a, sol=[f'{FLAME[c]} → {c}.'], p=dict(t=t, col=FLAME[c]))
    if t == 'fcnt':
        pool = rng.sample(list(FLAME), rng.randint(2, 5)) + rng.sample(NOFLAME, rng.randint(2, 4)); rng.shuffle(pool); k = sum(c in FLAME for c in pool)
        return dict(q='Number of ions among the following that give a characteristic flame colour: ' + ', '.join(pool), o=None, a=k, sol=[', '.join(f'{c} {FLAME[c]}' for c in pool if c in FLAME) + f' → {k}.'], p=dict(t=t, pool=pool))
    if t == 'conf':
        c, tst = rng.choice(CONF); o, a = mcq(rng, tst, [x for _, x in rng.sample(CONF, 6) if x != tst]); return dict(q=f'Confirmatory test for {c}:', o=o, a=a, sol=[tst], p=dict(t=t, c=c))
    if t == 'conf2':
        c, tst = rng.choice(CONF); o, a = mcq(rng, c, [x for x, _ in rng.sample(CONF, 6) if x != c]); return dict(q=f'"{tst}" confirms', o=o, a=a, sol=[c], p=dict(t=t, tst=tst))
    if t == 'ksp':
        n = rng.choice([2, 3]); M = rng.choice(['Mg', 'Fe', 'Mn', 'Zn', 'Ni']) if n == 2 else rng.choice(['Al', 'Fe', 'Cr']); pK = rng.randint(10, 16) if n == 2 else rng.randint(30, 38); c = rng.choice([0.1, 0.01, 0.001, 1.0])
        oh = (10 ** -pK / c) ** (1 / n); ph = 14 + math.log10(oh); need(abs(ph * 10 - round(ph * 10) - 0.5) > 0.06 and 0 < ph < 14)
        return dict(q=f'K_{{sp}} of {M}(OH)_{{{n}}} = 1 × 10^{{−{pK}}}. pH at which it begins to precipitate from {nf(c, 3)} M {M}^{{{n}+}} = ____ × 10^{{−1}} (nearest integer).', o=None, a=round(ph * 10),
                    sol=[f'[OH^{{−}}] = (K_{{sp}}/{nf(c, 3)})^{{1/{n}}} = {nf(oh, 3)} M; pH = 14 + log[OH^{{−}}] = {nf(ph, 3)}.'], p=dict(t=t, n=n, pK=pK, c=c))
    pa = rng.randint(9, 15); pb = rng.randint(25, 36); c = rng.choice([1, 0.1]); oa = math.sqrt(10 ** -pa / c); ob = (10 ** -pb / c) ** (1 / 3); need(abs(math.log10(oa / ob)) > 0.3)
    right = 'B(OH)_{3} precipitates first' if ob < oa else 'A(OH)_{2} precipitates first'
    o, a = mcq(rng, right, ['A(OH)_{2} precipitates first', 'B(OH)_{3} precipitates first', 'both precipitate together', 'neither precipitates']);
    return dict(q=f'NH_{{4}}OH is added slowly to a solution {c} M in A^{{2+}} and {c} M in B^{{3+}}. K_{{sp}}[A(OH)_{{2}}] = 10^{{−{pa}}}, K_{{sp}}[B(OH)_{{3}}] = 10^{{−{pb}}}. Then', o=o, a=a,
                sol=[f'[OH^{{−}}] needed: A {nf(oa, 3)} M, B {nf(ob, 3)} M; smaller need precipitates first.'], p=dict(t='first', pa=pa, pb=pb, c=c))

def g_ani(rng):
    t = rng.choice(['an', 'an2', 'agx', 'las', 'las2', 'fact', 'lcnt'])
    if t == 'an':
        x, tst = rng.choice(ANION); o, a = mcq(rng, tst, [v for _, v in rng.sample(ANION, 6) if v != tst]); return dict(q=f'Test that identifies {x}:', o=o, a=a, sol=[tst], p=dict(t=t, x=x))
    if t == 'an2':
        x, tst = rng.choice(ANION); o, a = mcq(rng, x, [k for k, _ in rng.sample(ANION, 6) if k != x]); return dict(q=f'"{tst}" — the anion present is', o=o, a=a, sol=[x], p=dict(t=t, tst=tst))
    if t == 'agx':
        x = rng.choice(['Cl^{−}', 'Br^{−}', 'I^{−}']); d = dict(ANION)[x].split(': ')[1]; o, a = mcq(rng, d, [dict(ANION)[y].split(': ')[1] for y in ('Cl^{−}', 'Br^{−}', 'I^{−}') if y != x] + ['no precipitate', 'black precipitate'])
        return dict(q=f'Sodium carbonate extract containing {x} is acidified with dil. HNO_{{3}} and AgNO_{{3}} is added. Observation:', o=o, a=a, sol=[f'{x}: {d}.'], p=dict(t=t, x=x))
    if t == 'las':
        e, r = rng.choice(LAS); o, a = mcq(rng, r, [v for _, v in LAS if v != r]); return dict(q=f'In the Lassaigne test, {e} is shown by', o=o, a=a, sol=[r], p=dict(t=t, e=e))
    if t == 'las2':
        e, r = rng.choice(LAS); o, a = mcq(rng, e, [k for k, _ in LAS if k != e]); return dict(q=f'Lassaigne extract gives {r.split(" — ")[0]}. The element(s) present:', o=o, a=a, sol=[f'{r} → {e}.'], p=dict(t=t, r=r))
    if t == 'lcnt':
        pool = rng.sample(['CH_{3}NH_{2}', 'C_{6}H_{5}NO_{2}', 'NH_{2}NH_{2}', 'NH_{2}OH', 'C_{6}H_{5}NHNH_{2}', 'CH_{3}CONH_{2}', 'C_{6}H_{5}N_{2}^{+}Cl^{−}', 'HN_{3}', 'C_{6}H_{5}CN', 'urea (NH_{2}CONH_{2})', 'pyridine'], rng.randint(5, 8))
        k = sum('C' in re.sub(r'Cl', '', s) or s == 'pyridine' or s.startswith('urea') for s in pool)
        return dict(q='Lassaigne\'s test (Prussian blue) works only for nitrogen compounds that also contain carbon (NaCN must form). How many of these give it? ' + ', '.join(pool), o=None, a=k, sol=['Compounds without C (hydrazine, hydroxylamine, HN_{3}) cannot form NaCN.', f'Count = {k}.'], p=dict(t=t, pool=pool))
    want = rng.choice([True, False]); r = rng.choice([s for s, v in PR_F if v == want]); o, a = mcq(rng, r, rng.sample([s for s, v in PR_F if v != want], 3))
    return dict(q=f'Which statement about qualitative analysis / lab practice is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='fact', want=want))

TITR = {'oxalic acid': ('C2H2O4·2H2O', 126, 2), 'Mohr\'s salt': ('FeSO4·(NH4)2SO4·6H2O', 392, 1), 'ferrous sulphate': ('FeSO4·7H2O', 278, 1)}
EQN = {'oxalic acid': (2, 5), 'Mohr\'s salt': (1, 5), 'ferrous sulphate': (1, 5)}   # 2MnO4− + 5C2O4^2−; MnO4− + 5Fe2+ : (mol MnO4−, mol reductant)
def g_titr(rng):
    t = rng.choice(['mol', 'mol', 'vol', 'mass', 'nf', 'ind'])
    s = rng.choice(list(TITR)); f, M, nr = TITR[s]
    if t == 'mol':
        Vr = rng.choice([10, 20, 25]); Vk = rng.choice([8.0, 10.0, 12.5, 15.0, 16.0, 20.0]); Mk = rng.choice([0.01, 0.02, 0.005]); Mr = Mk * Vk * 5 / (Vr * nr)
        need(abs(Mr * 1000 - round(Mr * 1000)) < 1e-6)
        return dict(q=f'{Vr} mL of {s} solution needs {nf(Vk, 3)} mL of {nf(Mk, 3)} M KMnO_{{4}} (acidic) for complete reaction. Molarity of the {s} solution = ____ × 10^{{−3}} M.', o=None, a=round(Mr * 1000),
                    sol=[f'Equivalents equal: {nf(Mk, 3)} × 5 × {nf(Vk, 3)} = M × {nr} × {Vr} → M = {nf(Mr, 4)}.'], p=dict(t=t, s=s, Vr=Vr, Vk=Vk, Mk=Mk))
    if t == 'vol':
        Vr = rng.choice([10, 20, 25, 50]); Mr = rng.choice([0.05, 0.1, 0.02, 0.04]); Mk = rng.choice([0.01, 0.02, 0.05]); Vk = Mr * nr * Vr / (5 * Mk); need(abs(Vk * 10 - round(Vk * 10)) < 1e-6)
        return dict(q=f'Volume of {nf(Mk, 3)} M KMnO_{{4}} (acidic) needed for {Vr} mL of {nf(Mr, 3)} M {s} = ____ × 10^{{−1}} mL.', o=None, a=round(Vk * 10), sol=[f'{nf(Mr, 3)} × {nr} × {Vr} = {nf(Mk, 3)} × 5 × V → V = {nf(Vk, 4)} mL.'], p=dict(t=t, s=s, Vr=Vr, Mr=Mr, Mk=Mk))
    if t == 'mass':
        V = rng.choice([100, 250, 500]); Mr = rng.choice([0.05, 0.1, 0.02, 0.04, 0.025]); g = M * Mr * V / 1000; need(abs(g * 100 - round(g * 100)) < 1e-6)
        return dict(q=f'Mass of {s} ({f}, M = {M}) needed to make {V} mL of {nf(Mr, 3)} M solution = ____ × 10^{{−2}} g.', o=None, a=round(g * 100), sol=[f'{nf(Mr, 3)} × {V}/1000 × {M} = {nf(g, 4)} g.'], p=dict(t=t, s=s, V=V, Mr=Mr))
    if t == 'nf':
        x = rng.choice(['KMnO_{4} in acidic medium', 'oxalate ion (to CO_{2})', 'Fe^{2+} (to Fe^{3+})', 'K_{2}Cr_{2}O_{7} in acidic medium', 'KMnO_{4} in neutral/weakly alkaline medium'])
        v = {'KMnO_{4} in acidic medium': 5, 'oxalate ion (to CO_{2})': 2, 'Fe^{2+} (to Fe^{3+})': 1, 'K_{2}Cr_{2}O_{7} in acidic medium': 6, 'KMnO_{4} in neutral/weakly alkaline medium': 3}[x]
        return dict(q=f'n-factor (electrons per formula unit) of {x}:', o=None, a=v, sol=[f'{v}.'], p=dict(t=t, x=x))
    x = rng.choice([('KMnO_{4} vs oxalic acid', 'KMnO_{4} itself (self-indicator)'), ('HCl vs NaOH', 'phenolphthalein or methyl orange'), ('Na_{2}CO_{3} vs HCl (to CO_{2})', 'methyl orange'),
                    ('CH_{3}COOH vs NaOH', 'phenolphthalein'), ('NH_{4}OH vs HCl', 'methyl orange'), ('I_{2} vs Na_{2}S_{2}O_{3}', 'starch')])
    o, a = mcq(rng, x[1], ['KMnO_{4} itself (self-indicator)', 'phenolphthalein', 'methyl orange', 'starch', 'phenolphthalein or methyl orange', 'diphenylamine'])
    return dict(q=f'Suitable indicator for the titration {x[0]}:', o=o, a=a, sol=[x[1]], p=dict(t='ind', x=x[0]))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(cat=g_cat, ani=g_ani, titr=g_titr).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it
ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6}
REAG2 = {'dil. HCl': 1, 'H_{2}S in presence of dil. HCl': 2, 'NH_{4}OH in presence of NH_{4}Cl': 3, 'H_{2}S in presence of NH_{4}OH': 4, '(NH_{4})_{2}CO_{3} in presence of NH_{4}OH': 5}
IND = {'KMnO_{4} vs oxalic acid': 'KMnO_{4} itself (self-indicator)', 'HCl vs NaOH': 'phenolphthalein or methyl orange', 'Na_{2}CO_{3} vs HCl (to CO_{2})': 'methyl orange', 'CH_{3}COOH vs NaOH': 'phenolphthalein', 'NH_{4}OH vs HCl': 'methyl orange', 'I_{2} vs Na_{2}S_{2}O_{3}': 'starch'}
def _flame(col): return next(v for k, v in FL2.items() if k in col)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'grp': return ROMAN[R.split()[1]] == grp2(p['c'])
    if t == 'reag': return REAG2[R] == grp2(p['c'])
    if t == 'ppt': return R == LADDER[grp2(p['c']) - 1][1]
    if t == 'flame': return sym(p['c']) == _flame(R)
    if t == 'flame2': return sym(R) == _flame(p['col'])
    if t == 'fcnt': return R == sum(1 for c in p['pool'] if sym(c) in FL2.values())
    if t == 'conf': return next(v for k, v in CONF2.items() if k in R) == ('NH' if p['c'].startswith('NH') else sym(p['c']))
    if t == 'conf2': return next(v for k, v in CONF2.items() if k in p['tst']) == ('NH' if R.startswith('NH') else sym(R))
    if t == 'ksp': return R == round(10 * (14 - (p['pK'] + math.log10(p['c'])) / p['n']))
    if t == 'first':
        la = (-p['pa'] - math.log10(p['c'])) / 2; lb = (-p['pb'] - math.log10(p['c'])) / 3; return R == ('B(OH)_{3} precipitates first' if lb < la else 'A(OH)_{2} precipitates first')
    if t == 'an': return AN2[next(k for k in AN2 if k in R)] in p['x']
    if t == 'an2': return AN2[next(k for k in AN2 if k in p['tst'])] in R
    if t == 'agx': return {'white': 'Cl', 'pale-yellow': 'Br', 'yellow': 'I'}[R.split()[0]] in p['x']
    if t == 'las': return LAS2[next(k for k in LAS2 if k in R)] == p['e']
    if t == 'las2': return LAS2[next(k for k in LAS2 if k in p['r'])] == R
    if t == 'lcnt': return R == sum(1 for s in p['pool'] if s not in ('NH_{2}NH_{2}', 'NH_{2}OH', 'HN_{3}'))
    if t == 'fact': return PR_FD[R] == p['want']
    if t in ('mol', 'vol'):
        a, b = EQN[p['s']]                                         # mole ratio from the balanced equation
        if t == 'mol': return abs(R - p['Mk'] * p['Vk'] / a * b / p['Vr'] * 1000) < 1e-6
        return abs(R - p['Mr'] * p['Vr'] / b * a / p['Mk'] * 10) < 1e-6
    if t == 'mass': return abs(R - p['V'] / 1000 * p['Mr'] * {'oxalic acid': 2 * 12 + 2 + 64 + 36, "Mohr's salt": 56 + 96 + 132 + 108, 'ferrous sulphate': 56 + 96 + 126}[p['s']] * 100) < 1e-6
    if t == 'nf': return R == {'KMnO_{4} in acidic medium': 7 - 2, 'oxalate ion (to CO_{2})': 2 * (4 - 3), 'Fe^{2+} (to Fe^{3+})': 3 - 2, 'K_{2}Cr_{2}O_{7} in acidic medium': 2 * (6 - 3), 'KMnO_{4} in neutral/weakly alkaline medium': 7 - 4}[p['x']]
    if t == 'ind': return R == IND[p['x']]
    raise KeyError(t)
