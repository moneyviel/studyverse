"""Practice generators — Chemistry Unit 11: d- and f-Block Elements. check() recomputes each answer another way:
unpaired electrons by filling the five d (or seven f) orbitals one electron at a time (Hund's rule), spin-only
moments from that count, titrations by balancing the electrons each species gives or takes, and comparisons
straight from the data tables. Statement items come from a fact bank written from NCERT."""
import math, re
from common import mcq, nf
from dblock import ATOM, E2, E32, IE1, IE2, IE3, Z3d, d_count, unpaired, mu
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def hund(n, orbs=5):   # fill orbitals singly first, then pair: count the singly occupied ones
    occ = [0] * orbs
    for k in range(n): occ[k % orbs if k < orbs else k - orbs] += 1
    return sum(1 for o in occ if o == 1)
SUP = {2: '2+', 3: '3+', 4: '4+', 1: '+'}
def ion_tex(m, q): return f'{m}^{{{SUP[q]}}}'
IONS = [(m, q) for m in Z3d for q in (1, 2, 3, 4) if 0 <= d_count(m, q) <= 10 and not (m == 'Sc' and q != 3) and not (m == 'Zn' and q != 2)]
LANF = {'La': 0, 'Ce': 1, 'Pr': 3, 'Nd': 4, 'Pm': 5, 'Sm': 6, 'Eu': 7, 'Gd': 7, 'Tb': 9, 'Dy': 10, 'Ho': 11, 'Er': 12, 'Tm': 13, 'Yb': 14, 'Lu': 14}
def f_ion(m, q): return max(0, min(14, LANF[m] + (1 if m in ('La', 'Ce', 'Gd', 'Lu') else 0) + 2 - q))
LIONS = [(m, 3) for m in LANF] + [('Ce', 4), ('Tb', 4), ('Eu', 2), ('Yb', 2), ('Sm', 2)]

FT = [('Transition metals show variable oxidation states because ns and (n−1)d electrons have similar energies.', True), ('Zn, Cd and Hg are not regarded as typical transition elements.', True),
      ('Mn shows the highest oxidation state (+7) in the 3d series.', True), ('Sc shows a +2 oxidation state commonly.', False), ('Atomisation enthalpy is maximum near the middle of the 3d series.', True),
      ('Zinc has the highest enthalpy of atomisation in the 3d series.', False), ('Cu^{+} is unstable in water and disproportionates.', True), ('E°(Cu^{2+}/Cu) is negative.', False),
      ('Interstitial compounds are hard and have high melting points.', True), ('Interstitial compounds are ionic and soft.', False), ('Transition metals and their compounds are good catalysts.', True),
      ('V_{2}O_{5} is used in the contact process.', True), ('Higher oxidation states are more stable for heavier members of a d-block group.', True), ('Most transition metal ions are coloured because of d–d transitions.', True),
      ('Sc^{3+} and Zn^{2+} salts are coloured.', False), ('Mn^{2+} is especially stable because it is d^{5}.', True), ('Cr^{2+} is a reducing agent while Mn^{3+} is an oxidising agent.', True),
      ('The ionic character of oxides increases with the oxidation state of the metal.', False), ('Mn_{2}O_{7} is an acidic oxide.', True), ('CrO is an amphoteric oxide.', False)]
FO = [('KMnO_{4} acts as a self-indicator in redox titrations.', True), ('In acid, MnO_{4}^{−} is reduced to Mn^{2+}.', True), ('In neutral or weakly alkaline medium MnO_{4}^{−} is reduced to MnO_{2}.', True),
      ('Manganate ion MnO_{4}^{2−} is diamagnetic.', False), ('Permanganate ion is tetrahedral.', True), ('Dichromate ion contains a Cr−O−Cr bridge.', True), ('Chromate is converted to dichromate on adding alkali.', False),
      ('K_{2}Cr_{2}O_{7} is a primary standard.', True), ('KMnO_{4} is a primary standard.', False), ('Na_{2}Cr_{2}O_{7} is preferred to K_{2}Cr_{2}O_{7} as a primary standard.', False),
      ('Oxalic acid titration with KMnO_{4} is done warm (about 60 °C).', True), ('Chromyl chloride CrO_{2}Cl_{2} contains Cr in the +6 state.', True), ('Acidified K_{2}Cr_{2}O_{7} turns green when it oxidises SO_{2}.', True),
      ('KMnO_{4} is prepared by fusing MnO_{2} with KOH and an oxidant, then oxidising the manganate.', True), ('Cr_{2}O_{7}^{2−} oxidises Fe^{3+} to Fe^{4+}.', False)]
FL = [('The common oxidation state of lanthanoids is +3.', True), ('Lanthanoid contraction makes Zr and Hf almost the same size.', True), ('Ce^{4+} is a good oxidising agent.', True), ('Eu^{2+} is a good oxidising agent.', False),
      ('Eu^{2+} and Yb^{2+} are reducing agents.', True), ('Actinoids show a wider range of oxidation states than lanthanoids.', True), ('Actinoid contraction is smaller than lanthanoid contraction.', False),
      ('La(OH)_{3} is the most basic lanthanoid hydroxide.', True), ('Lu(OH)_{3} is more basic than La(OH)_{3}.', False), ('Misch metal is an alloy of a lanthanoid metal (~95%) with iron.', True),
      ('All actinoids are radioactive.', True), ('Gd^{3+} has the highest number of unpaired electrons (7) among Ln^{3+} ions.', True), ('Lanthanoid ions with 4f^{0} or 4f^{14} are coloured.', False)]

def facts(rng, bank, fam):
    t = rng.choice(['one', 'cnt', 'pair']); T = [s for s, v in bank if v]; Fz = [s for s, v in bank if not v]
    if t == 'one':
        want = rng.choice([True, False]); r = rng.choice(T if want else Fz); w = rng.sample(Fz if want else T, 3); o, a = mcq(rng, r, w)
        return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}.'], p=dict(t='f_one', want=want))
    if t == 'cnt':
        k = rng.randint(4, 5); pool = rng.sample(bank, k); n = sum(1 for _, v in pool if v)
        return dict(q='How many of these are correct? ' + ' '.join(f'{"ABCDE"[i]}. {s}' for i, (s, _) in enumerate(pool)), o=None, a=n,
                    sol=['; '.join(f'{"ABCDE"[i]} {"✓" if v else "✗"}' for i, (_, v) in enumerate(pool)) + f' → {n}.'], p=dict(t='f_cnt', ss=[s for s, _ in pool]))
    STO = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
    s1, s2 = rng.sample(bank, 2); ans = {(True, True): STO[0], (False, False): STO[1], (True, False): STO[2], (False, True): STO[3]}[(s1[1], s2[1])]
    o, a = mcq(rng, ans, [x for x in STO if x != ans])
    return dict(q=f'Statement I: {s1[0]} Statement II: {s2[0]}', o=o, a=a, sol=[f'I is {"true" if s1[1] else "false"}; II is {"true" if s2[1] else "false"}.'], p=dict(t='f_pair', s1=s1[0], s2=s2[0]))

def g_mag(rng):
    t = rng.choice(['mu', 'n', 'match', 'which', 'sum', 'hi'])
    if t == 'mu':
        m, q = rng.choice(IONS); n = unpaired(d_count(m, q)); v = mu(n)
        if rng.random() < 0.5: return dict(q=f'The spin-only magnetic moment of {ion_tex(m, q)} (nearest integer, BM) is ____.', o=None, a=round(v), sol=[f'{ion_tex(m, q)} is d^{{{d_count(m, q)}}}: {n} unpaired.', f'μ = √({n} × {n + 2}) = {nf(v, 3)} BM ≈ {round(v)}.'], p=dict(t=t, m=m, q=q))
        w = [nf(mu(k), 3) for k in range(6) if k != n]; rng.shuffle(w); o, a = mcq(rng, nf(v, 3) + ' BM', [x + ' BM' for x in w[:3]])
        return dict(q=f'The spin-only magnetic moment of {ion_tex(m, q)} is', o=o, a=a, sol=[f'd^{{{d_count(m, q)}}} → {n} unpaired.', f'μ = {nf(v, 3)} BM.'], p=dict(t='mu_o', m=m, q=q))
    if t == 'n':
        m, q = rng.choice(IONS); n = unpaired(d_count(m, q))
        return dict(q=f'The number of unpaired electrons in {ion_tex(m, q)} (Z of {m} = {Z3d[m]}) is ____.', o=None, a=n, sol=[f'{m} [Ar]3d…4s…; {ion_tex(m, q)} is 3d^{{{d_count(m, q)}}}.', f'Hund\'s rule → {n} unpaired.'], p=dict(t=t, m=m, q=q))
    if t == 'match':
        target = rng.choice([1.73, 2.83, 3.87, 4.9, 5.92]); n = {1.73: 1, 2.83: 2, 3.87: 3, 4.9: 4, 5.92: 5}[target]
        pool = rng.sample(IONS, 5); k = sum(1 for m, q in pool if unpaired(d_count(m, q)) == n); need(k >= 1)
        return dict(q=f'How many of these ions have a spin-only moment of {target} BM? ' + ', '.join(ion_tex(m, q) for m, q in pool), o=None, a=k,
                    sol=[f'{target} BM ↔ {n} unpaired electrons.', '; '.join(f'{ion_tex(m, q)}: {unpaired(d_count(m, q))}' for m, q in pool) + f' → {k}.'], p=dict(t=t, n=n, pool=pool))
    if t == 'which':
        pool = rng.sample(IONS, 4); ns = [unpaired(d_count(m, q)) for m, q in pool]; need(ns.count(max(ns)) == 1)
        o, a = mcq(rng, ion_tex(*pool[ns.index(max(ns))]), [ion_tex(m, q) for (m, q), k in zip(pool, ns) if k != max(ns)])
        return dict(q='Which ion has the highest spin-only magnetic moment?', o=o, a=a, sol=['; '.join(f'{ion_tex(m, q)}: {k} unpaired' for (m, q), k in zip(pool, ns))], p=dict(t=t, pool=pool))
    if t == 'sum':
        pool = rng.sample(IONS, 3); s = sum(unpaired(d_count(m, q)) for m, q in pool)
        return dict(q='The total number of unpaired electrons in ' + ', '.join(ion_tex(m, q) for m, q in pool) + ' is ____.', o=None, a=s, sol=['; '.join(f'{ion_tex(m, q)}: {unpaired(d_count(m, q))}' for m, q in pool) + f' → {s}.'], p=dict(t=t, pool=pool))
    q = rng.choice([2, 3]); val = rng.choice([1, 2, 3, 4, 5]); cands = [m for m in Z3d if (m, q) in IONS and unpaired(d_count(m, q)) == val]; need(cands)
    m = rng.choice(cands); tgt = round(mu(val), 2)
    return dict(q=f'A first-row transition metal in its +{q} state has a spin-only moment of {tgt} BM. Its d-electron count could be ____ (give the smaller possibility).', o=None, a=min(d for d in range(11) if unpaired(d) == val),
                sol=[f'{tgt} BM ↔ {val} unpaired.', f'd^{{{val}}} or d^{{{10 - val}}} — smaller is {min(val, 10 - val)}.'], p=dict(t='hi', val=val))

def g_oxo(rng):
    t = rng.choice(['mno4_ox', 'mno4_fe', 'cr_fe', 'os', 'iod', 'facts'])
    if t == 'facts': return facts(rng, FO, 'oxo')
    if t == 'mno4_ox':
        V, M, Mo = rng.choice([10, 15, 20, 25, 40, 50]), rng.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1, 2]), rng.choice([0.02, 0.04, 0.05, 0.1, 0.2]); vk = V * M * 2 / 5 / Mo
        o, a = mcq(rng, nf(vk, 3) + ' mL', [nf(vk * f, 3) + ' mL' for f in (2.5, 0.4, 5)])
        return dict(q=f'{V} mL of {M} M oxalic acid is titrated in acid with {Mo} M KMnO_{{4}}. The volume of KMnO_{{4}} used is', o=o, a=a,
                    sol=['2MnO_{4}^{−} : 5C_{2}O_{4}^{2−}.', f'V = \\f{{2 × {V} × {M}}}{{5 × {Mo}}} = {nf(vk, 3)} mL.'], p=dict(t=t, V=V, M=M, Mo=Mo))
    if t == 'mno4_fe':
        n = rng.choice([0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7.5, 10]); r = n / 5
        o, a = mcq(rng, nf(r, 3), [nf(n / k, 3) for k in (1, 3, 6)])
        return dict(q=f'Moles of KMnO_{{4}} needed (acid medium) to oxidise {n} mol of Fe^{{2+}} is', o=o, a=a, sol=['MnO_{4}^{−} + 5Fe^{2+} + 8H^{+} → Mn^{2+} + 5Fe^{3+} + 4H_{2}O.', f'{n}/5 = {nf(r, 3)} mol.'], p=dict(t=t, n=n))
    if t == 'cr_fe':
        Vf, Mf, Vc = rng.choice([100, 150, 250, 300, 750]), rng.choice([0.1, 0.2, 0.3, 0.6]), rng.choice([50, 100, 200, 250]); Mc = Vf * Mf / 6 / Vc
        o, a = mcq(rng, nf(Mc, 3) + ' M', [nf(Mc * f, 3) + ' M' for f in (6, 3, 0.5)])
        return dict(q=f'{Vc} mL of K_{{2}}Cr_{{2}}O_{{7}} exactly oxidises {Vf} mL of {Mf} M Mohr\'s salt (Fe^{{2+}}) in acid. The dichromate molarity is', o=o, a=a,
                    sol=['Cr_{2}O_{7}^{2−} takes 6 e^{−}: 1 dichromate : 6 Fe^{2+}.', f'M = \\f{{{Vf} × {Mf}}}{{6 × {Vc}}} = {nf(Mc, 3)} M.'], p=dict(t=t, Vf=Vf, Mf=Mf, Vc=Vc))
    if t == 'os':
        sp = rng.choice([('MnO_{4}^{−}', 'Mn', [('O', 4)], -1), ('MnO_{4}^{2−}', 'Mn', [('O', 4)], -2), ('Cr_{2}O_{7}^{2−}', 'Cr', [('O', 7)], -2), ('CrO_{4}^{2−}', 'Cr', [('O', 4)], -2),
                         ('CrO_{2}Cl_{2}', 'Cr', [('O', 2), ('Cl', 2)], 0), ('VO_{2}^{+}', 'V', [('O', 2)], 1), ('FeO_{4}^{2−}', 'Fe', [('O', 4)], -2), ('MnO_{2}', 'Mn', [('O', 2)], 0), ('Mn_{2}O_{7}', 'Mn', [('O', 7)], 0), ('CrO_{5}', 'Cr', [], 0)])
        f, mtl, lig, ch = sp
        x = 6 if f == 'CrO_{5}' else (ch - sum({'O': -2, 'Cl': -1}[e] * k for e, k in lig)) / (2 if f.startswith(('Cr_{2}', 'Mn_{2}')) else 1)
        return dict(q=f'The oxidation state of {mtl} in {f} is ____.', o=None, a=int(x), sol=['Sum of oxidation numbers = charge (O = −2, Cl = −1; CrO_{5} has two peroxide groups).', f'{mtl}: {int(x)}.'], p=dict(t=t, f=f))
    Vm, Mm, Vk, Mk, Mt = rng.choice([200, 250, 500]), rng.choice([0.1, 0.2]), rng.choice([250, 500]), rng.choice([1.0, 1.2, 1.5, 2.0]), rng.choice([0.1, 0.2, 0.5, 1.0])
    e = min(Vm * Mm * 3, Vk * Mk) / 1000; V = e / Mt
    o, a = mcq(rng, nf(V, 3) + ' L', [nf(V * f, 3) + ' L' for f in (5 / 3, 0.5, 2)])
    return dict(q=f'{Vm} mL of {Mm} M KMnO_{{4}} (basic medium, → MnO_{{2}}) reacts with {Vk} mL of {Mk} M KI. The liberated I_{{2}} needs what volume of {Mt} M Na_{{2}}S_{{2}}O_{{3}}?', o=o, a=a,
                sol=['Basic: MnO_{4}^{−} + 3e^{−} → MnO_{2}; thiosulphate needs one per electron transferred.', f'{nf(e, 3)} mol e^{{−}} → {nf(V, 3)} L.'], p=dict(t='iod', Vm=Vm, Mm=Mm, Vk=Vk, Mk=Mk, Mt=Mt))

def g_trend(rng):
    t = rng.choice(['cmp', 'cmp', 'facts'])
    if t == 'facts': return facts(rng, FT, 'trend')
    prop, tab, nm = rng.choice([('atomisation enthalpy', ATOM, 'kJ/mol'), ('first ionisation enthalpy', IE1, 'kJ/mol'), ('second ionisation enthalpy', IE2, 'kJ/mol'), ('third ionisation enthalpy', IE3, 'kJ/mol'), ('E°(M^{2+}/M)', E2, 'V')])
    pool = rng.sample(sorted(tab), 4); hi = rng.choice([True, False]); vals = [tab[x] for x in pool]; best = max(vals) if hi else min(vals); need(vals.count(best) == 1)
    r = pool[vals.index(best)]; o, a = mcq(rng, r, [x for x in pool if x != r])
    return dict(q=f'Among {", ".join(pool)}, which has the {"highest" if hi else "lowest"} {prop}?', o=o, a=a, sol=['; '.join(f'{x}: {tab[x]} {nm}' for x in pool), f'→ {r}.'], p=dict(t='cmp', prop=prop, pool=pool, hi=hi))

def g_lanth(rng):
    t = rng.choice(['fn', 'col', 'dia', 'facts'])
    if t == 'facts': return facts(rng, FL, 'lanth')
    if t == 'fn':
        m, q = rng.choice(LIONS); k = f_ion(m, q); n = k if k <= 7 else 14 - k
        if rng.random() < 0.5: return dict(q=f'The number of 4f electrons in {m}^{{{q}+}} is ____.', o=None, a=k, sol=[f'{m}: [Xe]4f^{{{LANF[m]}}}{"5d^{1}" if m in ("La", "Ce", "Gd", "Lu") else ""}6s^{{2}}.', f'Remove {q} electrons → 4f^{{{k}}}.'], p=dict(t='fn', m=m, q=q))
        return dict(q=f'The number of unpaired electrons in {m}^{{{q}+}} is ____.', o=None, a=n, sol=[f'{m}^{{{q}+}} is 4f^{{{k}}}.', f'Hund\'s rule → {n} unpaired.'], p=dict(t='fu', m=m, q=q))
    pool = rng.sample(LIONS, 5); k = sum(1 for m, q in pool if f_ion(m, q) in (0, 14))
    word = 'colourless' if t == 'col' else 'diamagnetic'
    return dict(q=f'How many of these ions are {word}? ' + ', '.join(f'{m}^{{{q}+}}' for m, q in pool), o=None, a=k, sol=['Only 4f^{0} and 4f^{14} ions have no unpaired f electrons (and no f–f colour).', '; '.join(f'{m}^{{{q}+}}: 4f^{{{f_ion(m, q)}}}' for m, q in pool) + f' → {k}.'], p=dict(t='cd', pool=pool))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(mag=g_mag, oxo=g_oxo, trend=g_trend, lanth=g_lanth).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

TRUTH = {s: v for b in (FT, FO, FL) for s, v in b}
def dcount2(m, q):   # independent: build the configuration electron by electron (Aufbau with Cr/Cu exceptions), then remove 4s first
    z = Z3d[m] - 18; s, d = 2, z - 2
    if m in ('Cr', 'Cu'): s, d = 1, z - 1
    for _ in range(q):
        if s: s -= 1
        else: d -= 1
    return d
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'f_one': return TRUTH[R] == p['want']
    if t == 'f_cnt': return R == sum(1 for s in p['ss'] if TRUTH[s])
    if t == 'f_pair':
        a, b = TRUTH[p['s1']], TRUTH[p['s2']]; lo = R.lower()
        return {(True, True): 'both' in lo and 'true' in lo, (False, False): 'both' in lo and 'false' in lo, (True, False): lo.startswith('statement i is true'), (False, True): lo.startswith('statement i is false')}[(a, b)]
    if t in ('mu', 'mu_o'): v = mu(hund(dcount2(p['m'], p['q']))); return R == round(v) if t == 'mu' else R == nf(v, 3) + ' BM'
    if t == 'n': return R == hund(dcount2(p['m'], p['q']))
    if t == 'match': return R == sum(1 for m, q in p['pool'] if hund(dcount2(m, q)) == p['n'])
    if t == 'which': return R == ion_tex(*max(p['pool'], key=lambda x: hund(dcount2(*x))))
    if t == 'sum': return R == sum(hund(dcount2(m, q)) for m, q in p['pool'])
    if t == 'hi': return R == min(d for d in range(11) if hund(d) == p['val'])
    if t == 'mno4_ox': return close(num(R) * p['Mo'] * 5, p['V'] * p['M'] * 2)   # electrons: 5 per MnO4- = 2 per oxalate
    if t == 'mno4_fe': return close(float(R) * 5, p['n'])
    if t == 'cr_fe': return close(num(R) * p['Vc'] * 6, p['Vf'] * p['Mf'])
    if t == 'os':
        f = p['f']; ch = {'^{−}': -1, '^{2−}': -2, '^{+}': 1}; c = next((v for k, v in ch.items() if f.endswith(k)), 0)
        cnt = dict((e, int(n) if n else 1) for e, n in re.findall(r'(Mn|Cr|Fe|V|O|Cl)(?:_\{(\d+)\})?', f.split('^')[0]))
        mt = [e for e in cnt if e in ('Mn', 'Cr', 'Fe', 'V')][0]
        if f == 'CrO_{5}': return R == 6   # Cr(O)(O2)2: one oxide, two peroxides
        return R * cnt[mt] + cnt.get('O', 0) * -2 + cnt.get('Cl', 0) * -1 == c
    if t == 'iod': e = min(p['Vm'] * p['Mm'] * 3, p['Vk'] * p['Mk']) / 1000; return close(num(R) * p['Mt'], e)
    if t == 'cmp':
        tab = {'atomisation enthalpy': ATOM, 'first ionisation enthalpy': IE1, 'second ionisation enthalpy': IE2, 'third ionisation enthalpy': IE3, 'E°(M^{2+}/M)': E2}[p['prop']]
        return R == sorted(p['pool'], key=tab.get, reverse=p['hi'])[0]
    if t in ('fn', 'fu'):
        e = LANF[p['m']] + (1 if p['m'] in ('La', 'Ce', 'Gd', 'Lu') else 0)   # f + d electrons beyond [Xe] besides 6s2
        k = max(0, min(14, e - (p['q'] - 2))); return R == (k if t == 'fn' else hund(k, 7))
    if t == 'cd': return R == sum(1 for m, q in p['pool'] if hund(f_ion(m, q), 7) == 0)
    raise KeyError(t)
