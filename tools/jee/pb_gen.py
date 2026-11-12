"""Practice generators — Chemistry Unit 10: p-Block Elements. Statement items come from a fact bank (each fact written
from NCERT, tagged true/false and re-checked by check()); numbers (oxidation states, basicity, lone pairs, shapes)
are recomputed from the formula — oxidation numbers by charge balance, shapes by VSEPR counting."""
import re
from common import mcq, nf
from vsepr import vsepr as V, USE
USE.setdefault('I', 1)
def need(x):
    if not x: raise AssertionError('retry')
F1314 = [('Boron has the highest first ionisation enthalpy in group 13.', True), ('Gallium is smaller than aluminium.', True), ('Thallium shows a stable +1 oxidation state because of the inert-pair effect.', True),
         ('Boric acid is a strong protonic acid.', False), ('Boric acid is a weak monobasic Lewis acid.', True), ('Diborane has two 3-centre-2-electron (banana) B−H−B bonds.', True), ('Diborane has four B−H−B bridge bonds.', False),
         ('All boron trihalides are Lewis acids.', True), ('BF_{3} is a stronger Lewis acid than BI_{3}.', False), ('Aluminium is rendered passive by concentrated HNO_{3}.', True), ('Al_{2}O_{3} is amphoteric.', True),
         ('B_{2}O_{3} is amphoteric.', False), ('Borax is Na_{2}[B_{4}O_{5}(OH)_{4}]·8H_{2}O.', True), ('Aluminium chloride exists as the dimer Al_{2}Cl_{6} in the vapour phase.', True),
         ('Carbon shows maximum covalency of 6.', False), ('Carbon has a strong tendency for catenation.', True), ('Catenation tendency increases down group 14.', False), ('Pb^{4+} compounds are strong oxidising agents.', True),
         ('Sn^{2+} is a reducing agent.', True), ('SiO_{2} is a basic oxide.', False), ('CO is a neutral oxide.', True), ('SnO_{2} and PbO_{2} are amphoteric.', True), ('Graphite is a good conductor of electricity.', True),
         ('Diamond conducts electricity.', False), ('In diamond each carbon is sp^{2} hybridised.', False), ('Fullerene C_{60} contains 20 six-membered and 12 five-membered rings.', True), ('Silicones contain repeating R_{2}SiO units.', True),
         ('Zeolites are aluminosilicates used as catalysts.', True), ('Tin has the lowest melting point in group 14.', True), ('The +2 state becomes more stable down group 14.', True)]
F15 = [('N_{2} is chemically inert at room temperature due to the high N≡N bond enthalpy.', True), ('Nitrogen can show a covalency of 5.', False), ('NH_{3} is more basic than PH_{3}.', True), ('BiH_{3} is the strongest reducing agent among group 15 hydrides.', True),
       ('Thermal stability of hydrides increases from NH_{3} to BiH_{3}.', False), ('Bond angle in PH_{3} is greater than in NH_{3}.', False), ('NH_{3} has the highest boiling point among NH_{3}, PH_{3}, AsH_{3}.', True),
       ('White phosphorus is more reactive than red phosphorus.', True), ('White phosphorus consists of discrete P_{4} tetrahedra.', True), ('Red phosphorus glows in the dark.', False), ('H_{3}PO_{3} is a dibasic acid.', True),
       ('H_{3}PO_{2} is a tribasic acid.', False), ('H_{3}PO_{2} is a good reducing agent because it has two P−H bonds.', True), ('PCl_{5} has two axial bonds longer than the three equatorial bonds.', True),
       ('In the solid state PCl_{5} exists as [PCl_{4}]^{+}[PCl_{6}]^{−}.', True), ('NO_{2} dimerises to N_{2}O_{4}.', True), ('Nitric oxide (NO) is paramagnetic.', True), ('N_{2}O_{5} is the anhydride of HNO_{3}.', True),
       ('Concentrated HNO_{3} makes iron passive.', True), ('The stability of the +5 state increases down group 15.', False), ('Bi shows a stable +3 state due to the inert-pair effect.', True), ('The Haber process makes ammonia from N_{2} and H_{2} over iron.', True),
       ('The Ostwald process oxidises NH_{3} to NO over a Pt/Rh gauze.', True), ('PH_{3} forms hydrogen bonds like NH_{3}.', False), ('Phosphine gives a black precipitate of Cu_{3}P_{2} with CuSO_{4} solution.', True)]
F1618 = [('Oxygen shows only the −2 oxidation state.', False), ('Ozone is diamagnetic and bent.', True), ('Ozone is a powerful oxidising agent.', True), ('H_{2}S is a stronger reducing agent than H_{2}Te.', False),
         ('Acidic strength increases from H_{2}O to H_{2}Te.', True), ('Rhombic sulphur is stable below 369 K.', True), ('Both rhombic and monoclinic sulphur contain S_{8} rings.', True), ('SO_{2} acts as a reducing agent.', True),
         ('Oleum is H_{2}S_{2}O_{7}.', True), ('The contact process uses V_{2}O_{5} as catalyst.', True), ('Fluorine shows positive oxidation states.', False), ('Cl_{2} has a more negative electron gain enthalpy than F_{2}.', True),
         ('The F−F bond is weaker than the Cl−Cl bond.', True), ('HF is the strongest acid among the hydrogen halides.', False), ('HF has the highest boiling point among HX because of hydrogen bonding.', True), ('Oxidising power: F_{2} > Cl_{2} > Br_{2} > I_{2}.', True),
         ('Bleaching by chlorine is due to oxidation.', True), ('HClO_{4} is a stronger acid than HClO.', True), ('Interhalogen compounds are more reactive than halogens (except F_{2}).', True), ('ClF_{3} is T-shaped.', True),
         ('Noble gases have very high boiling points.', False), ('XeF_{4} is square planar.', True), ('XeF_{2} is bent.', False), ('XeO_{3} is pyramidal.', True), ('Helium has the lowest boiling point of all substances.', True),
         ('The first noble gas compound prepared was Xe^{+}[PtF_{6}]^{−}.', True), ('XeF_{6} has a distorted octahedral shape.', True)]
BANK = {'g1314': F1314, 'g15': F15, 'g1618': F1618}
TRUTH = {s: t for b in BANK.values() for s, t in b}
STO = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
def g_facts(rng, fam):
    t = rng.choice(['one', 'one', 'cnt', 'pair'])
    B = BANK[fam]; T = [s for s, v in B if v]; Fz = [s for s, v in B if not v]
    if t == 'one':
        want = rng.choice([True, False]); r = rng.choice(T if want else Fz); w = rng.sample(Fz if want else T, 3); o, a = mcq(rng, r, w)
        return dict(q=f'Which statement is {"correct" if want else "INCORRECT"}?', o=o, a=a, sol=[f'"{r}" is {"true" if want else "false"}; the other three are {"false" if want else "true"}.'], p=dict(t='one', want=want, fam=fam))
    if t == 'cnt':
        k = rng.randint(4, 6); pool = rng.sample(B, k); n = sum(1 for s, v in pool if v); lab = 'ABCDEF'
        q = 'How many of these statements are correct? ' + ' '.join(f'{lab[i]}. {s}' for i, (s, _) in enumerate(pool))
        return dict(q=q, o=None, a=n, sol=['; '.join(f'{lab[i]} {"✓" if v else "✗"}' for i, (_, v) in enumerate(pool)) + f' → {n}.'], p=dict(t='cnt', ss=[s for s, _ in pool]))
    s1, s2 = rng.sample(B, 2); ans = {(True, True): STO[0], (False, False): STO[1], (True, False): STO[2], (False, True): STO[3]}[(s1[1], s2[1])]
    o, a = mcq(rng, ans, [x for x in STO if x != ans])
    return dict(q=f'Statement I: {s1[0]} Statement II: {s2[0]} Choose the correct option.', o=o, a=a, sol=[f'I is {"true" if s1[1] else "false"}; II is {"true" if s2[1] else "false"}.'], p=dict(t='pair', s1=s1[0], s2=s2[0]))

ACIDS = {'H_{3}PO_{4}': 3, 'H_{3}PO_{3}': 2, 'H_{3}PO_{2}': 1, 'H_{4}P_{2}O_{7}': 4, 'HPO_{3}': 1, 'H_{4}P_{2}O_{6}': 4, 'H_{2}SO_{4}': 2, 'H_{2}SO_{3}': 2, 'H_{2}S_{2}O_{7}': 2, 'HNO_{3}': 1, 'HClO_{4}': 1, 'H_{3}BO_{3}': 1}
PH = {'H_{3}PO_{4}': 0, 'H_{3}PO_{3}': 1, 'H_{3}PO_{2}': 2, 'H_{4}P_{2}O_{7}': 0, 'H_{4}P_{2}O_{6}': 0, 'HPO_{3}': 0}
OXO = ['HClO', 'HClO_{2}', 'HClO_{3}', 'HClO_{4}', 'HNO_{2}', 'HNO_{3}', 'H_{3}PO_{2}', 'H_{3}PO_{3}', 'H_{3}PO_{4}', 'H_{2}SO_{3}', 'H_{2}SO_{4}', 'H_{2}S_{2}O_{7}', 'H_{4}P_{2}O_{7}', 'HIO_{4}', 'HBrO_{3}', 'H_{2}SeO_{4}', 'N_{2}O_{5}', 'N_{2}O', 'NO_{2}', 'P_{4}O_{10}', 'XeO_{3}', 'XeF_{6}', 'XeOF_{4}', 'ClO_{2}', 'Cl_{2}O_{7}']
def parse(f):
    return {el: int(n) if n else 1 for el, n in re.findall(r'([A-Z][a-z]?)(?:_\{(\d+)\})?', f)}
def on_central(f):
    d = parse(f); c = [e for e in d if e not in ('H', 'O', 'F')][0]
    return (0 - d.get('H', 0) * 1 + d.get('O', 0) * 2 + d.get('F', 0) * 1) / d[c], c
def g_num(rng, fam):
    t = rng.choice({'g1314': ['on', 'bas'], 'g15': ['on', 'bas', 'ph'], 'g1618': ['on', 'shape'], 'gen': ['shape', 'on', 'lin']}[fam])
    if t == 'on':
        pool = [x for x in OXO if (fam != 'g15' or 'P' in x or 'N' in x)]; f = rng.choice(pool); x, c = on_central(f); need(x == int(x)); x = int(x)
        o, a = mcq(rng, ('+' if x > 0 else '') + str(x), [('+' if v > 0 else '') + str(v) for v in (x - 2, x + 2, x - 1, x + 1, -x) if v != x and abs(v) <= 8])
        return dict(q=f'The oxidation state of {c} in {f} is :', o=o, a=a, sol=['H +1, O −2, F −1; the total is 0.', f'{c} = {"+" if x > 0 else ""}{x}.'], p=dict(t='on', f=f))
    if t == 'bas':
        pool = rng.sample(list(ACIDS), rng.randint(3, 5)); tgt = rng.choice([1, 2, 3, 4]); n = sum(1 for x in pool if ACIDS[x] == tgt); need(n >= 1)
        return dict(q=f'Number of {"mono" if tgt == 1 else "di" if tgt == 2 else "tri" if tgt == 3 else "tetra"}basic acids among {", ".join(pool)} is ____.', o=None, a=n,
                    sol=['Basicity = number of ionisable O−H groups (P−H hydrogens are not acidic; H_{3}BO_{3} is monobasic as a Lewis acid).', '; '.join(f'{x} {ACIDS[x]}' for x in pool) + f' → {n}.'], p=dict(t='bas', ns=pool, tgt=tgt))
    if t == 'ph':
        pool = rng.sample(list(PH), rng.randint(3, 5)); n = sum(PH[x] for x in pool)
        return dict(q=f'Total number of P−H bonds in {", ".join(pool)} is ____.', o=None, a=n, sol=['Every P is tetrahedral with one P=O; the rest is O−H or P−H.', '; '.join(f'{x} {PH[x]}' for x in pool) + f' → {n}.'], p=dict(t='ph', ns=pool))
    SP = [('XeF_{2}', 'Xe', {'F': 2}, 0, 'linear'), ('XeF_{4}', 'Xe', {'F': 4}, 0, 'square planar'), ('XeF_{6}', 'Xe', {'F': 6}, 0, 'distorted octahedral'), ('XeO_{3}', 'Xe', {'O': 3}, 0, 'trigonal pyramidal'),
          ('XeOF_{4}', 'Xe', {'O': 1, 'F': 4}, 0, 'square pyramidal'), ('ClF_{3}', 'Cl', {'F': 3}, 0, 'T-shaped'), ('BrF_{5}', 'Br', {'F': 5}, 0, 'square pyramidal'), ('IF_{7}', 'I', {'F': 7}, 0, 'pentagonal bipyramidal'),
          ('ICl_{4}^{−}', 'I', {'Cl': 4}, -1, 'square planar'), ('I_{3}^{−}', 'I', {'I': 2}, -1, 'linear'), ('SF_{4}', 'S', {'F': 4}, 0, 'see-saw'), ('PCl_{5}', 'P', {'Cl': 5}, 0, 'trigonal bipyramidal'),
          ('SO_{3}', 'S', {'O': 3}, 0, 'trigonal planar'), ('NO_{2}^{+}', 'N', {'O': 2}, 1, 'linear'), ('BF_{3}', 'B', {'F': 3}, 0, 'trigonal planar'), ('ClO_{3}^{−}', 'Cl', {'O': 3}, -1, 'trigonal pyramidal'), ('O_{3}', 'O', {'O': 2}, 0, 'bent')]
    if t == 'lin':
        pool = rng.sample(SP, rng.randint(5, 8)); n = sum(1 for s in pool if s[4] == 'linear')
        return dict(q=f'Number of linear species among {", ".join(s[0] for s in pool)} is ____.', o=None, a=n, sol=['; '.join(f'{s[0]} {s[4]}' for s in pool) + f' → {n}.'], p=dict(t='lin', ns=[s[:4] for s in pool]))
    s = rng.choice(SP); SH = sorted({x[4] for x in SP}); o, a = mcq(rng, s[4], rng.sample([x for x in SH if x != s[4]], 3))
    return dict(q=f'The shape of {s[0]} is :', o=o, a=a, sol=['Count bond pairs and lone pairs on the central atom (VSEPR).', f'{s[0]}: {s[4]}.'], p=dict(t='shape', sp=s[:4]))

def mk(fam):
    def g(rng): return g_facts(rng, fam) if (fam != 'gen' and rng.random() < 0.7) else g_num(rng, fam)
    return g
def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(mk(k)) for k in ('g1314', 'g15', 'g1618', 'gen')}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'one': return TRUTH[Rv] == p['want'] and all(TRUTH[x] != p['want'] for x in it['o'] if x != Rv)
    if t == 'cnt': return Rv == sum(1 for s in p['ss'] if TRUTH[s])
    if t == 'pair': return Rv == {(True, True): STO[0], (False, False): STO[1], (True, False): STO[2], (False, True): STO[3]}[(TRUTH[p['s1']], TRUTH[p['s2']])]
    if t == 'on':   # independent: solve the charge balance element by element
        d = parse(p['f']); c = [e for e in d if e not in ('H', 'O', 'F')][0]; known = sum({'H': 1, 'O': -2, 'F': -1}[e] * n for e, n in d.items() if e != c)
        return int(Rv.replace('+', '')) == -known // d[c] and -known % d[c] == 0
    if t == 'bas':
        def basic(f):   # count O−H: for P acids, H atoms minus P−H; boric acid is a Lewis acid (1)
            if f == 'H_{3}BO_{3}': return 1
            d = parse(f); return d.get('H', 0) - PH.get(f, 0)
        return Rv == sum(1 for x in p['ns'] if basic(x) == p['tgt'])
    if t == 'ph':
        def nph(f):   # P(+1) in H3PO2 has 2 P−H, P(+3) in H3PO3 has 1, P(+5)/P(+4) none
            x, _ = on_central(f); return {1: 2, 3: 1}.get(int(x), 0)
        return Rv == sum(nph(x) for x in p['ns'])
    if t == 'lin': return Rv == sum(1 for nm, c, l, q in p['ns'] if V(c, l, q)['shape'] == 'linear')
    if t == 'shape': nm, c, l, q = p['sp']; return Rv == V(c, l, q)['shape']
    raise KeyError(t)
