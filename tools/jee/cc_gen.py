"""Practice generators — Chemistry Unit 12: Coordination Compounds. check() recomputes each answer another way:
oxidation state from its own ligand-charge table, d count from the atomic number, spin state from a separately
written field rule, unpaired electrons/CFSE by placing electrons one at a time into t2g/eg (or e/t2) levels, and
isomer counts with an independent enumerator that builds the octahedron's rotation group from two 90° turns.
Statement items come from a fact bank written from NCERT."""
import itertools, re
from common import mcq, nf
from dblock import Z3d, d_count
from cfield import LIG, ox_state, low_spin, unp_oct, unp_tet, unp_sq, cfse_oct, mu, stereo
def need(x):
    if not x: raise AssertionError('retry')
LT = {'H2O': 'H_{2}O', 'NH3': 'NH_{3}', 'en': 'en', 'CN': 'CN', 'F': 'F', 'Cl': 'Cl', 'Br': 'Br', 'ox': 'C_{2}O_{4}', 'SCN': 'SCN', 'CO': 'CO', 'NO2': 'NO_{2}', 'py': 'py', 'I': 'I', 'OH': 'OH'}
ANION = {'CN', 'F', 'Cl', 'Br', 'ox', 'SCN', 'NO2', 'I', 'OH'}
def sup(c): return '' if c == 0 else '^{' + (str(abs(c)) if abs(c) > 1 else '') + ('+' if c > 0 else '−') + '}'
def ftex(m, ligs, charge):
    order = sorted(ligs, key=lambda l: (l not in ANION, l))
    s = ''.join((LT[l] if l in ('F', 'Cl', 'Br', 'I') else f'({LT[l]})') + (f'_{{{k}}}' if k > 1 else '') for l in order for k in [ligs[l]])
    return f'[{m}{s}]{sup(charge)}'
def charge_of(m, ox, ligs): return ox + sum(LIG[l][0] * k for l, k in ligs.items())
# ---- complex pool: (metal, ox, ligs, geom)
OCT_M = [('Ti', 3), ('V', 3), ('V', 2), ('Cr', 3), ('Cr', 2), ('Mn', 2), ('Mn', 3), ('Fe', 2), ('Fe', 3), ('Co', 2), ('Co', 3), ('Ni', 2), ('Cu', 2), ('Zn', 2)]
OCT_L = [{'H2O': 6}, {'NH3': 6}, {'en': 3}, {'CN': 6}, {'F': 6}, {'ox': 3}]
def _ok(m, ox, ligs):   # leave out cases where the NCERT/JEE spin convention is unclear (d4–d7 with NH3/en, except Co3+)
    d = d_count(m, ox); mid = any(LIG[l][2] == 'mid' for l in ligs)
    return not (4 <= d <= 7 and mid and not (m == 'Co' and ox == 3))
POOL = [(m, ox, L, 'oct') for m, ox in OCT_M for L in OCT_L if _ok(m, ox, L) and not ('CN' in L and d_count(m, ox) >= 8)]
POOL += [(m, ox, L, 'oct') for m, ox in (('Co', 3), ('Cr', 3)) for L in ({'NH3': 5, 'Cl': 1}, {'NH3': 4, 'Cl': 2}, {'en': 2, 'Cl': 2}, {'H2O': 5, 'Cl': 1}, {'NH3': 5, 'H2O': 1}, {'en': 2, 'NH3': 2})]
POOL += [(m, 2, {h: 4}, 'tet') for m in ('Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn') for h in ('Cl', 'Br')] + [('Fe', 3, {'Cl': 4}, 'tet'), ('Ni', 0, {'CO': 4}, 'tet'), ('Ni', 2, {'CN': 4}, 'sq')]
def tex(c): m, ox, L, g = c; return ftex(m, L, charge_of(m, ox, L))
def info(c):
    m, ox, L, g = c
    if 'CO' in L: return dict(n=0, d=10, ls=True, t=None, e=None)
    d = d_count(m, ox)
    if g == 'tet': return dict(n=unp_tet(d), d=d, ls=False, t=None, e=None)
    if g == 'sq': return dict(n=unp_sq(d), d=d, ls=True, t=None, e=None)
    ls = low_spin(m, ox, L); t = min(d, 6) if ls else [0, 1, 2, 3, 3, 3, 4, 5, 6, 6, 6][d]
    return dict(n=unp_oct(d, ls), d=d, ls=ls, t=t, e=d - t)
def hyb(c):
    g = c[3]; i = info(c)
    if g == 'tet': return 'sp^{3}'
    if g == 'sq': return 'dsp^{2}'
    return 'd^{2}sp^{3}' if (i['ls'] or i['d'] <= 3) else 'sp^{3}d^{2}'
def conf_tex(t, e): return f't_{{2g}}^{{{t}}}e_{{g}}^{{{e}}}'
def cf_tex(v): return ('0' if v == 0 else f'{nf(v, 2).replace("-", "−")}') + 'Δ_{o}'
OCTS = [c for c in POOL if c[3] == 'oct']
RANK = {'I': 0, 'Br': 1, 'Cl': 3, 'F': 4, 'OH': 5, 'ox': 6, 'H2O': 7, 'NH3': 10, 'en': 11, 'NO2': 12, 'CN': 13, 'CO': 14}
LNAME = {'I': 'I^{−}', 'Br': 'Br^{−}', 'Cl': 'Cl^{−}', 'F': 'F^{−}', 'OH': 'OH^{−}', 'ox': 'C_{2}O_{4}^{2−}', 'H2O': 'H_{2}O', 'NH3': 'NH_{3}', 'en': 'en', 'NO2': 'NO_{2}^{−}', 'CN': 'CN^{−}', 'CO': 'CO'}
def fr(L): return sum(RANK[l] * k * LIG[l][1] for l, k in L.items()) / sum(k * LIG[l][1] for l, k in L.items())   # mean over donor atoms
def order_opts(rng, keys, right, sep):
    perms = [list(p) for p in itertools.permutations(keys) if list(p) != right]; rng.shuffle(perms)
    return mcq(rng, sep.join(right), [sep.join(p) for p in perms])

def g_mag(rng):
    t = rng.choice(['n', 'mu', 'para', 'ord', 'spin', 'dia', 'sum', 'mu_o'])
    if t in ('n', 'mu', 'mu_o'):
        c = rng.choice(POOL); i = info(c); v = mu(i['n'])
        sol = [f'{tex(c)}: {c[0]} is +{c[1]} (d^{{{i["d"]}}}), ' + {'oct': 'octahedral, ' + ('low spin' if i['ls'] else 'high spin'), 'tet': 'tetrahedral (always high spin)', 'sq': 'square planar'}[c[3]] + f' → {i["n"]} unpaired.']
        if t == 'n': return dict(q=f'The number of unpaired electrons in {tex(c)} is ____.', o=None, a=i['n'], sol=sol, p=dict(t=t, c=c))
        if t == 'mu': return dict(q=f'The spin-only magnetic moment of {tex(c)} is ____ BM (nearest integer).', o=None, a=round(v), sol=sol + [f'μ = √(n(n + 2)) = {nf(v, 3)} ≈ {round(v)} BM.'], p=dict(t=t, c=c))
        o, a = mcq(rng, nf(v, 3) + ' BM', [nf(mu(k), 3) + ' BM' for k in rng.sample([k for k in range(6) if k != i['n']], 5)])
        return dict(q=f'The spin-only magnetic moment of {tex(c)} is', o=o, a=a, sol=sol + [f'μ = {nf(v, 3)} BM.'], p=dict(t=t, c=c))
    if t in ('para', 'sum'):
        pool = rng.sample(POOL, rng.randint(4, 6)); ns = [info(c)['n'] for c in pool]
        a = sum(1 for n in ns if n) if t == 'para' else sum(ns)
        return dict(q=('The number of paramagnetic species among ' if t == 'para' else 'The total number of unpaired electrons in ') + ', '.join(tex(c) for c in pool) + ' is ____.', o=None, a=a,
                    sol=['; '.join(f'{tex(c)}: {n}' for c, n in zip(pool, ns)) + f' → {a}.'], p=dict(t=t, pool=pool))
    if t == 'ord':
        pool = rng.sample(POOL, 3); ns = [info(c)['n'] for c in pool]; need(len(set(ns)) == 3)
        keys = ['A', 'B', 'C']; right = sorted(keys, key=lambda k: ns[keys.index(k)]); o, a = order_opts(rng, keys, right, ' < ')
        return dict(q='Arrange by increasing spin-only magnetic moment: ' + ', '.join(f'{tex(c)} ({k})' for c, k in zip(pool, keys)), o=o, a=a,
                    sol=['Unpaired: ' + '; '.join(f'{k} {n}' for k, n in zip(keys, ns)), ' < '.join(right) + '.'], p=dict(t=t, pool=pool))
    if t == 'spin':
        cand = [c for c in OCTS if 4 <= info(c)['d'] <= 7]; want = rng.choice([True, False])
        r = rng.choice([c for c in cand if info(c)['ls'] == want]); w = rng.sample([c for c in cand if info(c)['ls'] != want], 3)
        o, a = mcq(rng, tex(r), [tex(c) for c in w])
        return dict(q=f'Which of these octahedral complexes is {"low spin (spin paired)" if want else "high spin (spin free)"}?', o=o, a=a,
                    sol=[f'{tex(r)}: d^{{{info(r)["d"]}}} with {"a strong" if want else "a weak"} field → {"low" if want else "high"} spin.', 'The others are the opposite.'], p=dict(t=t, want=want))
    want0 = rng.random() < 0.5
    r = rng.choice([c for c in POOL if (info(c)['n'] == 0) == want0]); w = rng.sample([c for c in POOL if (info(c)['n'] == 0) != want0], 3)
    o, a = mcq(rng, tex(r), [tex(c) for c in w])
    return dict(q=f'Which complex is {"diamagnetic" if want0 else "paramagnetic"}?', o=o, a=a, sol=[f'{tex(r)}: {info(r)["n"]} unpaired.', 'Others: ' + '; '.join(f'{tex(c)} {info(c)["n"]}' for c in w)], p=dict(t='dia', want=want0))

def g_cfs(rng):
    t = rng.choice(['cfse', 'conf', 'eg', 'lam', 'lig', 'hi', 'tg', 'cond'])
    if t in ('cfse', 'conf', 'eg', 'tg'):
        c = rng.choice(OCTS); i = info(c); v = cfse_oct(i['d'], i['ls'])
        sol = [f'{tex(c)}: d^{{{i["d"]}}}, {"low" if i["ls"] else "high"} spin → {conf_tex(i["t"], i["e"])}.']
        if t == 'cfse':
            vals = sorted({cfse_oct(d, ls) for d in range(11) for ls in (0, 1)} - {v}); o, a = mcq(rng, cf_tex(v), [cf_tex(x) for x in rng.sample(vals, 5)])
            return dict(q=f'The CFSE of {tex(c)} (pairing energy ignored) is', o=o, a=a, sol=sol + [f'CFSE = {i["t"]}(−0.4Δ_{{o}}) + {i["e"]}(0.6Δ_{{o}}) = {cf_tex(v)}.'], p=dict(t=t, c=c))
        if t == 'conf':
            w = [conf_tex(tt, i['d'] - tt) for tt in range(max(0, i['d'] - 4), min(6, i['d']) + 1) if tt != i['t']] + [conf_tex(min(6, i['d'] + 1), 1), conf_tex(3, max(0, i['d'] - 3) % 5), conf_tex(6, 0), conf_tex(4, 2), conf_tex(5, 2)]
            o, a = mcq(rng, conf_tex(i['t'], i['e']), rng.sample(w, len(w)))
            return dict(q=f'The d-electron configuration of the metal in {tex(c)} is', o=o, a=a, sol=sol, p=dict(t=t, c=c))
        k = 'e' if t == 'eg' else 't'
        return dict(q=f'The number of electrons in the {"e_{g}" if k == "e" else "t_{2g}"} orbitals of {tex(c)} is ____.', o=None, a=i[k], sol=sol, p=dict(t=t, c=c))
    if t == 'lam':
        m, ox = rng.choice([('Co', 3), ('Cr', 3)]); cand = [c for c in OCTS if c[:2] == (m, ox)]; pool = rng.sample(cand, 4); fs = [fr(c[2]) for c in pool]; need(len(set(fs)) == 4)
        what = rng.choice(['wavelength', 'energy']); keys = ['A', 'B', 'C', 'D']
        right = sorted(keys, key=lambda k: fs[keys.index(k)] if what == 'energy' else -fs[keys.index(k)]); o, a = order_opts(rng, keys, right, ' < ')
        return dict(q=f'Arrange in increasing order of the {"wavelength" if what == "wavelength" else "energy (frequency)"} of light absorbed: ' + ', '.join(f'{tex(c)} ({k})' for c, k in zip(pool, keys)), o=o, a=a,
                    sol=['Same metal ion, so Δ_{o} follows the ligands (spectrochemical series).', f'Energy absorbed ∝ Δ_{{o}}; wavelength ∝ 1/Δ_{{o}} → ' + ' < '.join(right) + '.'], p=dict(t=t, pool=pool, what=what))
    if t == 'lig':
        ls = rng.sample(list(RANK), 4); up = rng.random() < 0.5; right = sorted(ls, key=lambda l: RANK[l] if up else -RANK[l])
        perms = [list(p) for p in itertools.permutations(ls) if list(p) != right]; rng.shuffle(perms)
        o, a = mcq(rng, (' < ' if up else ' > ').join(LNAME[l] for l in right), [(' < ' if up else ' > ').join(LNAME[l] for l in p) for p in perms])
        return dict(q=f'The ligands arranged in {"increasing" if up else "decreasing"} order of field strength are', o=o, a=a, sol=['Spectrochemical series: I^{−} < Br^{−} < Cl^{−} < F^{−} < OH^{−} < C_{2}O_{4}^{2−} < H_{2}O < NH_{3} < en < NO_{2}^{−} < CN^{−} < CO.'], p=dict(t=t, ls=ls, up=up))
    if t == 'hi':
        pool = rng.sample(OCTS, 4); vs = [cfse_oct(info(c)['d'], info(c)['ls']) for c in pool]; need(vs.count(min(vs)) == 1)
        r = pool[vs.index(min(vs))]; o, a = mcq(rng, tex(r), [tex(c) for c in pool if c != r])
        return dict(q='Which complex has the largest crystal field stabilisation (most negative CFSE in units of Δ_{o})?', o=o, a=a, sol=['; '.join(f'{tex(c)}: {cf_tex(v)}' for c, v in zip(pool, vs))], p=dict(t=t, pool=pool))
    c = rng.choice([x for x in OCTS if 4 <= info(x)['d'] <= 7]); i = info(c)
    o, a = mcq(rng, ('strong' if i['ls'] else 'weak') + ' field ligand, ' + ('low' if i['ls'] else 'high') + ' spin', ['strong field ligand, high spin', 'weak field ligand, low spin', ('weak' if i['ls'] else 'strong') + ' field ligand, ' + ('high' if i['ls'] else 'low') + ' spin'])
    return dict(q=f'The {conf_tex(i["t"], i["e"])} configuration of {tex(c)} arises from', o=o, a=a, sol=[f'{"All electrons in t_{2g} first (Δ_{o} > P)" if i["ls"] else "Electrons enter e_{g} before pairing (Δ_{o} < P)"}.'], p=dict(t='cond', c=c))

ISO_M = [('Co', 3), ('Cr', 3), ('Pt', 4)]
MONO = ['NH3', 'H2O', 'Cl', 'Br', 'NO2', 'py']
SHAPES = [((4, 2), 0), ((3, 3), 0), ((2, 2, 2), 0), ((2, 2, 1, 1), 0), ((5, 1), 0), ((4, 1, 1), 0), ((3, 2, 1), 0), ((2, 2), 1), ((4,), 1), ((2, 1, 1), 1), ((), 3), ((1, 1), 2), ((2,), 2)]
def iso_formula(m, ox, mono, bi):
    L = dict(mono); L.update({b: bi.count(b) for b in set(bi)})
    return ftex(m, L, ox + sum(LIG[l][0] * k for l, k in L.items()))
WERN = [('Co', 'NH3'), ('Cr', 'NH3'), ('Cr', 'H2O'), ('Co', 'H2O')]
MM = {'Co': 59, 'Cr': 52, 'N': 14, 'H': 1, 'O': 16, 'Cl': 35.5, 'Ag': 108}
ISOTYPES = [('[Co(NH_{3})_{5}Br]SO_{4} and [Co(NH_{3})_{5}SO_{4}]Br', 'ionisation'), ('[Co(NH_{3})_{5}NO_{2}]Cl_{2} and [Co(NH_{3})_{5}ONO]Cl_{2}', 'linkage'), ('[Co(NH_{3})_{6}][Cr(CN)_{6}] and [Cr(NH_{3})_{6}][Co(CN)_{6}]', 'coordination'),
            ('[Cr(H_{2}O)_{6}]Cl_{3} and [Cr(H_{2}O)_{5}Cl]Cl_{2}·H_{2}O', 'solvate (hydrate)'), ('[Pt(NH_{3})_{4}Cl_{2}]Br_{2} and [Pt(NH_{3})_{4}Br_{2}]Cl_{2}', 'ionisation'), ('[Mn(CO)_{5}(SCN)] and [Mn(CO)_{5}(NCS)]', 'linkage'),
            ('[Cu(NH_{3})_{4}][PtCl_{4}] and [Pt(NH_{3})_{4}][CuCl_{4}]', 'coordination'), ('[Co(en)_{2}(H_{2}O)Cl]Cl_{2} and [Co(en)_{2}Cl_{2}]Cl·H_{2}O', 'solvate (hydrate)'), ('[Co(NH_{3})_{5}Cl]SO_{4} and [Co(NH_{3})_{5}SO_{4}]Cl', 'ionisation'),
            ('[Fe(CO)_{4}(CN)]^{−} and [Fe(CO)_{4}(NC)]^{−}', 'linkage'), ('[Cr(NH_{3})_{6}][Co(C_{2}O_{4})_{3}] and [Co(NH_{3})_{6}][Cr(C_{2}O_{4})_{3}]', 'coordination'), ('cis- and trans-[Co(NH_{3})_{4}Cl_{2}]^{+}', 'geometrical'),
            ('fac- and mer-[Co(NH_{3})_{3}(NO_{2})_{3}]', 'geometrical'), ('d- and l-[Co(en)_{3}]^{3+}', 'optical'), ('cis-[PtCl_{2}(en)_{2}]^{2+} and its mirror image', 'optical'), ('[Co(NH_{3})_{5}(SCN)]^{2+} and [Co(NH_{3})_{5}(NCS)]^{2+}', 'linkage')]
def g_iso(rng):
    t = rng.choice(['geo', 'geo', 'stereo', 'opt', 'werner', 'agcl', 'type'])
    if t in ('geo', 'stereo', 'opt'):
        shape, nb = rng.choice(SHAPES); labs = rng.sample(MONO, len(shape)); mono = dict(zip(labs, shape)); bi = [rng.choice(['en', 'ox'])] * nb
        m, ox = rng.choice(ISO_M); tot, geo = stereo(mono, bi); opt = 2 * (tot - geo)
        a = {'geo': geo, 'stereo': tot, 'opt': opt}[t]
        what = {'geo': 'geometrical isomers', 'stereo': 'stereoisomers (geometrical + optical)', 'opt': 'optically active isomers'}[t]
        return dict(q=f'The number of {what} possible for the octahedral complex {iso_formula(m, ox, mono, bi)} is ____.', o=None, a=a,
                    sol=[f'Distinct arrangements on the octahedron: {geo} geometrical isomer(s); {tot - geo} of them chiral (each a pair of enantiomers).', f'Stereoisomers = {tot}; optically active = {opt}.'], p=dict(t=t, mono=mono, bi=bi))
    if t in ('werner', 'agcl'):
        m, L = rng.choice(WERN); x = rng.randint(3, 6); free = x - 3; inside = 3 - free
        name = f'{m}Cl_{{3}}·{x}{LT[L]}'; struct = ftex(m, {L: x, 'Cl': inside} if inside else {L: x}, free) + (f'Cl_{{{free}}}' if free > 1 else 'Cl' if free else '')
        if t == 'werner':
            ask = rng.choice(['agcl', 'ions'])
            a = free if ask == 'agcl' else 1 + free
            return dict(q=f'An octahedral complex {name} (coordination number 6, no ligand other than {LT[L]} and Cl) is treated in solution. ' + ('Moles of AgCl precipitated per mole of complex with excess AgNO_{3} = ____.' if ask == 'agcl' else 'Number of ions produced per formula unit in water = ____.'), o=None, a=a,
                        sol=[f'{x} {LT[L]} occupy {x} sites; {inside} Cl fill the rest → {struct}.', f'{free} ionisable Cl^{{−}} → {free} AgCl; ions = {1 + free}.'], p=dict(t=t, x=x, ask=ask))
        need(free > 0); w = rng.choice([1.0, 1.5, 2.0, 2.5, 3.0, 5.0]); M = MM[m] + 3 * 35.5 + x * ({'NH3': 17, 'H2O': 18}[L])
        g = w / M * free * 143.5; a = round(g * 1000)
        return dict(q=f'{nf(w, 2)} g of the octahedral complex {name} ({LT[L]} and Cl are the only possible ligands; {free} mole(s) of AgCl form per mole with excess AgNO_{{3}}) is treated with excess AgNO_{{3}}. Mass of AgCl formed = ____ mg (nearest integer). [Co 59, Cr 52, N 14, O 16, H 1, Cl 35.5, Ag 108]', o=None, a=a,
                    sol=[f'M = {nf(M, 4)} g/mol → {nf(w / M, 4)} mol.', f'AgCl = {free} × {nf(w / M, 4)} × 143.5 g = {nf(g, 4)} g ≈ {a} mg.'], p=dict(t='agcl', w=w, m=m, L=L, x=x, free=free))
    pair, kind = rng.choice(ISOTYPES); o, a = mcq(rng, kind + ' isomerism', [k + ' isomerism' for k in rng.sample([k for k in ('ionisation', 'linkage', 'coordination', 'solvate (hydrate)', 'geometrical', 'optical') if k != kind], 5)])
    return dict(q=f'{pair} are examples of', o=o, a=a, sol=[{'ionisation': 'Counter-ion and ligand exchange places → different ions in solution.', 'linkage': 'An ambidentate ligand binds through different atoms.', 'coordination': 'Ligands are swapped between the cationic and anionic complexes of different metals.',
                                                            'solvate (hydrate)': 'Water is inside vs outside the coordination sphere.', 'geometrical': 'Same ligands, different spatial arrangement (cis/trans, fac/mer).', 'optical': 'Non-superimposable mirror images.'}[kind]], p=dict(t='type', pair=pair))

FB = [('Ethane-1,2-diamine is a bidentate chelating ligand.', True), ('EDTA^{4−} is a hexadentate ligand.', True), ('NO_{2}^{−} and SCN^{−} are ambidentate ligands.', True), ('Chelate complexes are generally less stable than similar complexes of unidentate ligands.', False),
      ('In metal carbonyls the M–C bond has both σ and π character.', True), ('Synergic bonding weakens the metal–carbon bond in carbonyls.', False), ('Back-bonding lowers the C–O bond order in metal carbonyls.', True),
      ('Ni(CO)_{4} is tetrahedral and diamagnetic.', True), ('Fe(CO)_{5} is trigonal bipyramidal.', True), ('Cr(CO)_{6} is octahedral.', True), ('[Ni(CN)_{4}]^{2−} is tetrahedral.', False), ('[NiCl_{4}]^{2−} is square planar.', False),
      ('Wilkinson\'s catalyst [RhCl(PPh_{3})_{3}] is used for hydrogenation of alkenes.', True), ('Nickel dimethylglyoximate is a red precipitate.', True), ('Nickel dimethylglyoximate is paramagnetic.', False),
      ('Hardness of water is estimated by titration with Na_{2}EDTA.', True), ('Silver and gold are extracted using cyanide complexes.', True), ('Cis-platin is used in cancer treatment.', True), ('Chlorophyll contains Mg.', True), ('Haemoglobin contains Co.', False),
      ('Vitamin B_{12} (cyanocobalamin) contains Co.', True), ('Valence bond theory explains the colour of complexes.', False), ('Crystal field theory treats ligands as point charges or dipoles.', True),
      ('Δ_{t} is about 4/9 of Δ_{o}.', True), ('Tetrahedral complexes are commonly low spin.', False), ('In a tetrahedral field the e orbitals lie lower than t_{2}.', True), ('In an octahedral field d_{x²−y²} and d_{z²} lie lower than t_{2g}.', False),
      ('A homoleptic complex has only one type of ligand.', True), ('[Co(NH_{3})_{4}Cl_{2}]^{+} is a homoleptic complex.', False), ('Tetrahedral MABCD complexes show geometrical isomerism.', False),
      ('The stability constant of [Cu(en)_{2}]^{2+} is greater than that of [Cu(NH_{3})_{4}]^{2+}.', True), ('[Co(NH_{3})_{6}]^{3+} is an inner orbital complex.', True), ('[CoF_{6}]^{3−} is an inner orbital complex.', False)]
TRUTH = dict(FB)
def facts(rng):
    t = rng.choice(['one', 'cnt', 'pair']); T = [s for s, v in FB if v]; Fz = [s for s, v in FB if not v]
    if t == 'one':
        want = rng.choice([True, False]); r = rng.choice(T if want else Fz); o, a = mcq(rng, r, rng.sample(Fz if want else T, 3))
        return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='f_one', want=want))
    if t == 'cnt':
        pool = rng.sample(FB, rng.randint(4, 5)); n = sum(1 for _, v in pool if v)
        return dict(q='How many of these are correct? ' + ' '.join(f'{"ABCDE"[i]}. {s}' for i, (s, _) in enumerate(pool)), o=None, a=n, sol=['; '.join(f'{"ABCDE"[i]} {"✓" if v else "✗"}' for i, (_, v) in enumerate(pool)) + f' → {n}.'], p=dict(t='f_cnt', ss=[s for s, _ in pool]))
    STO = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
    s1, s2 = rng.sample(FB, 2); ans = {(True, True): STO[0], (False, False): STO[1], (True, False): STO[2], (False, True): STO[3]}[(s1[1], s2[1])]; o, a = mcq(rng, ans, [x for x in STO if x != ans])
    return dict(q=f'Statement I: {s1[0]} Statement II: {s2[0]}', o=o, a=a, sol=[f'I is {"true" if s1[1] else "false"}; II is {"true" if s2[1] else "false"}.'], p=dict(t='f_pair', s1=s1[0], s2=s2[0]))
HYB = ['sp^{3}', 'dsp^{2}', 'd^{2}sp^{3}', 'sp^{3}d^{2}']
def g_vbt(rng):
    t = rng.choice(['hyb', 'io', 'ox', 'cn', 'homo', 'fact', 'fact', 'hybw'])
    if t == 'fact': return facts(rng)
    if t in ('hyb', 'io'):
        c = rng.choice(POOL); h = hyb(c); i = info(c); sol = [f'{tex(c)}: {c[0]}(+{c[1]}) d^{{{i["d"]}}}, ' + {'oct': 'octahedral', 'tet': 'tetrahedral', 'sq': 'square planar'}[c[3]] + f', {i["n"]} unpaired → {h}.']
        if t == 'hyb': o, a = mcq(rng, h, [x for x in HYB if x != h]); return dict(q=f'The hybridisation of the metal in {tex(c)} is', o=o, a=a, sol=sol, p=dict(t=t, c=c))
        need(c[3] == 'oct'); io = ('inner' if h == 'd^{2}sp^{3}' else 'outer') + ' orbital, ' + ('diamagnetic' if i['n'] == 0 else 'paramagnetic')
        o, a = mcq(rng, io, [f'{x} orbital, {y}' for x in ('inner', 'outer') for y in ('diamagnetic', 'paramagnetic')])
        return dict(q=f'{tex(c)} is', o=o, a=a, sol=sol, p=dict(t=t, c=c))
    if t == 'hybw':
        h = rng.choice(HYB); r = rng.choice([c for c in POOL if hyb(c) == h]); w = rng.sample([c for c in POOL if hyb(c) != h], 3); o, a = mcq(rng, tex(r), [tex(c) for c in w])
        return dict(q=f'Which complex involves {h} hybridisation?', o=o, a=a, sol=[f'{tex(r)} → {h}.', 'Others: ' + '; '.join(f'{tex(c)} {hyb(c)}' for c in w)], p=dict(t=t, h=h))
    if t in ('ox', 'cn'):
        c = rng.choice(POOL); m, ox, L, g = c; cnum = sum(LIG[l][1] * k for l, k in L.items())
        a = ox if t == 'ox' else cnum
        return dict(q=f'The {"oxidation state" if t == "ox" else "coordination number"} of {m} in {tex(c)} is ____.', o=None, a=a,
                    sol=[f'Ligand charges/denticities: ' + ', '.join(f'{LT[l]} ({LIG[l][0]}, {LIG[l][1]}-dentate)' for l in L) + '.', f'Oxidation state {ox}; coordination number {cnum}.'], p=dict(t=t, c=c))
    pool = rng.sample(POOL, 5); k = sum(1 for c in pool if len(c[2]) == 1)
    return dict(q='The number of homoleptic complexes among ' + ', '.join(tex(c) for c in pool) + ' is ____.', o=None, a=k, sol=['Homoleptic = one kind of ligand only.', f'Count = {k}.'], p=dict(t='homo', pool=pool))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(mag=g_mag, cfs=g_cfs, iso=g_iso, vbt=g_vbt).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent re-solve ----------------
LQ = {'H2O': 0, 'NH3': 0, 'en': 0, 'py': 0, 'CO': 0, 'CN': -1, 'F': -1, 'Cl': -1, 'Br': -1, 'I': -1, 'SCN': -1, 'NO2': -1, 'OH': -1, 'ox': -2}
DENT = {'en': 2, 'ox': 2}
def spin2(m, ox, L, d):   # strong-field ligands pair; Co(III) d6 pairs unless mostly halide; otherwise high spin
    if any(l in ('CN', 'CO', 'NO2') for l in L): return True
    return m == 'Co' and ox == 3 and sum(k for l, k in L.items() if l in ('F', 'Cl', 'Br', 'I')) < 3
def place(d, levels, paired_first):
    """levels: list of (energy, n_orbitals) low→high. Electrons placed one at a time: lowest free slot,
    pairing within a level before moving up only if paired_first. returns occupancy per level (list of lists)"""
    occ = [[0] * n for _, n in levels]
    for _ in range(d):
        done = False
        for lv in occ:   # singly fill the lowest level with an empty orbital (or pair there, if allowed)
            if 0 in lv: lv[lv.index(0)] = 1; done = True; break
            if paired_first and 1 in lv: lv[lv.index(1)] = 2; done = True; break
        if not done:
            for lv in occ:
                if 1 in lv: lv[lv.index(1)] = 2; break
    return occ
def solve(c):
    m, ox, L, g = c
    if 'CO' in L: return dict(n=0)
    d = Z3d[m] - 18 - ox if ox >= 2 else None
    if g == 'sq': occ = place(d, [(0, 4), (1, 1)], True); return dict(n=sum(v == 1 for lv in occ for v in lv), d=d)
    if g == 'tet': occ = place(d, [(0, 2), (1, 3)], False); return dict(n=sum(v == 1 for lv in occ for v in lv), d=d)
    ls = spin2(m, ox, L, d); occ = place(d, [(-0.4, 3), (0.6, 2)], ls); t, e = sum(occ[0]), sum(occ[1])
    return dict(n=sum(v == 1 for lv in occ for v in lv), d=d, ls=ls, t=t, e=e, cf=round(-0.4 * t + 0.6 * e, 2))
def mu2(n): return (n * n + 2 * n) ** 0.5
# octahedron positions +x −x +y −y +z −z; rotation group generated by two quarter turns
C4Z = [2, 3, 1, 0, 4, 5]; C4X = [0, 1, 4, 5, 3, 2]; INV = [1, 0, 3, 2, 5, 4]
def _group(gens):
    G = {tuple(range(6))}; frontier = list(G)
    while frontier:
        new = []
        for p in frontier:
            for gg in gens:
                q = tuple(gg[p[i]] for i in range(6))
                if q not in G: G.add(q); new.append(q)
        frontier = new
    return list(G)
ROT = _group([C4Z, C4X]); ALL = _group([C4Z, C4X, INV])
def count_iso(mono, bi):
    trans = {(0, 1), (2, 3), (4, 5)}; seen_p, seen_a = set(), set()
    labels = [l for l, k in mono.items() for _ in range(k)]
    for pos in itertools.permutations(range(6)):
        cfg = [None] * 6; edges = []; j = 0
        for b in bi:
            a1, a2 = pos[j], pos[j + 1]; j += 2
            if (min(a1, a2), max(a1, a2)) in trans: break
            cfg[a1] = cfg[a2] = b; edges.append(frozenset((a1, a2)))
        else:
            for i, l in enumerate(labels): cfg[pos[j + i]] = l
            def key(G): return min((tuple(cfg[g.index(i)] for i in range(6)), tuple(sorted(tuple(sorted(g[x] for x in e)) for e in edges))) for g in G)
            seen_p.add(key(ROT)); seen_a.add(key(ALL))
    return len(seen_p), len(seen_a)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'f_one': return TRUTH[R] == p['want']
    if t == 'f_cnt': return R == sum(1 for s in p['ss'] if TRUTH[s])
    if t == 'f_pair':
        a, b = TRUTH[p['s1']], TRUTH[p['s2']]; lo = R.lower()
        return {(True, True): 'both' in lo and 'true' in lo, (False, False): 'both' in lo and 'false' in lo, (True, False): lo.startswith('statement i is true'), (False, True): lo.startswith('statement i is false')}[(a, b)]
    if t == 'n': return R == solve(p['c'])['n']
    if t == 'mu': return R == round(mu2(solve(p['c'])['n']))
    if t == 'mu_o': return abs(float(R.split()[0]) - mu2(solve(p['c'])['n'])) < 0.01
    if t == 'para': return R == sum(1 for c in p['pool'] if solve(c)['n'] > 0)
    if t == 'sum': return R == sum(solve(c)['n'] for c in p['pool'])
    if t == 'ord':
        ks = R.split(' < '); ns = {k: solve(c)['n'] for k, c in zip('ABC', p['pool'])}; return all(ns[a] < ns[b] for a, b in zip(ks, ks[1:]))
    if t == 'spin':
        c = next(c for c in OCTS if tex(c) == R); s = solve(c); return 4 <= s['d'] <= 7 and s['ls'] == p['want']
    if t == 'dia': c = next(c for c in POOL if tex(c) == R); return (solve(c)['n'] == 0) == p['want']
    if t == 'cfse': s = solve(p['c']); return R == cf_tex(s['cf'])
    if t == 'conf': s = solve(p['c']); return R == conf_tex(s['t'], s['e'])
    if t == 'eg': return R == solve(p['c'])['e']
    if t == 'tg': return R == solve(p['c'])['t']
    if t == 'cond': s = solve(p['c']); return R.startswith('strong field ligand, low' if s['ls'] else 'weak field ligand, high')
    if t == 'lam':
        ks = R.split(' < '); f = {k: sum(RANK[l] * n * DENT.get(l, 1) for l, n in c[2].items()) / 6 for k, c in zip('ABCD', p['pool'])}   # mean over the 6 donor sites
        return all((f[a] < f[b]) if p['what'] == 'energy' else (f[a] > f[b]) for a, b in zip(ks, ks[1:]))
    if t == 'lig':
        inv = {v: k for k, v in LNAME.items()}; ls = [inv[x] for x in re.split(r' [<>] ', R)]
        return sorted(ls) == sorted(p['ls']) and all((RANK[a] < RANK[b]) if p['up'] else (RANK[a] > RANK[b]) for a, b in zip(ls, ls[1:]))
    if t == 'hi':
        c = next(c for c in p['pool'] if tex(c) == R); return all(solve(c)['cf'] < solve(x)['cf'] for x in p['pool'] if x is not c)
    if t in ('geo', 'stereo', 'opt'):
        tot, geo = count_iso(p['mono'], p['bi']); return R == {'geo': geo, 'stereo': tot, 'opt': 2 * (tot - geo)}[t]
    if t == 'werner': free = p['x'] - 3; return R == (free if p['ask'] == 'agcl' else free + 1)
    if t == 'agcl':
        M = MM[p['m']] + 3 * MM['Cl'] + p['x'] * (MM['N'] + 3 * MM['H'] if p['L'] == 'NH3' else 2 * MM['H'] + MM['O'])
        return R == round(p['w'] / M * p['free'] * (MM['Ag'] + MM['Cl']) * 1000) and p['free'] == p['x'] - 3
    if t == 'type':
        kind = R.replace(' isomerism', ''); pr = p['pair']
        if pr.startswith('d-') or 'mirror image' in pr: return kind == 'optical'
        if pr.startswith(('cis', 'fac')): return kind == 'geometrical'
        if 'H_{2}O' in pr and '·' in pr: return kind == 'solvate (hydrate)'
        if any(a in pr for a in ('ONO', 'NCS', '(NC)')): return kind == 'linkage'
        if pr.count('][') == 2: return kind == 'coordination'
        return kind == 'ionisation'
    if t in ('hyb', 'io'):
        m, ox, L, g = c = p['c']; s = solve(c)
        h = {'tet': 'sp^{3}', 'sq': 'dsp^{2}'}.get(g) or ('d^{2}sp^{3}' if s['ls'] or s['d'] <= 3 else 'sp^{3}d^{2}')
        if t == 'hyb': return R == h
        return R == ('inner' if h == 'd^{2}sp^{3}' else 'outer') + ' orbital, ' + ('diamagnetic' if s['n'] == 0 else 'paramagnetic')
    if t == 'hybw': c = next(c for c in POOL if tex(c) == R); return hyb(c) == p['h'] and sum(1 for o in it['o'] if hyb(next(x for x in POOL if tex(x) == o)) == p['h']) == 1
    if t == 'ox': m, ox, L, g = p['c']; return R + sum(LQ[l] * k for l, k in L.items()) == charge_of(m, ox, L)
    if t == 'cn': return R == sum(DENT.get(l, 1) * k for l, k in p['c'][2].items())
    if t == 'homo': return R == sum(1 for c in p['pool'] if len(set(c[2])) == 1)
    raise KeyError(t)
