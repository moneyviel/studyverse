"""Practice generators — Chemistry Unit 3: Chemical Bonding. Generators draw answers from a hand-written textbook
table; check() re-derives every answer from first principles (VSEPR electron counting and MO filling in vsepr.py),
so a slip in either source is caught."""
import math
from common import mcq, nf
from vsepr import vsepr, mo
def need(x):
    if not x: raise AssertionError('retry')
# name, (center, ligs, charge), textbook: shape, hybridisation, lone pairs on centre, polar?
SP = [('CO_{2}', ('C', {'O': 2}, 0), 'linear', 'sp', 0, False), ('BeCl_{2}', ('Be', {'Cl': 2}, 0), 'linear', 'sp', 0, False), ('BF_{3}', ('B', {'F': 3}, 0), 'trigonal planar', 'sp^{2}', 0, False),
      ('SO_{2}', ('S', {'O': 2}, 0), 'bent', 'sp^{2}', 1, True), ('SO_{3}', ('S', {'O': 3}, 0), 'trigonal planar', 'sp^{2}', 0, False), ('NO_{2}^{−}', ('N', {'O': 2}, -1), 'bent', 'sp^{2}', 1, True),
      ('O_{3}', ('O', {'O': 2}, 0), 'bent', 'sp^{2}', 1, True), ('CH_{4}', ('C', {'H': 4}, 0), 'tetrahedral', 'sp^{3}', 0, False), ('NH_{3}', ('N', {'H': 3}, 0), 'trigonal pyramidal', 'sp^{3}', 1, True),
      ('H_{2}O', ('O', {'H': 2}, 0), 'bent', 'sp^{3}', 2, True), ('NH_{4}^{+}', ('N', {'H': 4}, 1), 'tetrahedral', 'sp^{3}', 0, False), ('BF_{4}^{−}', ('B', {'F': 4}, -1), 'tetrahedral', 'sp^{3}', 0, False),
      ('NF_{3}', ('N', {'F': 3}, 0), 'trigonal pyramidal', 'sp^{3}', 1, True), ('PCl_{3}', ('P', {'Cl': 3}, 0), 'trigonal pyramidal', 'sp^{3}', 1, True), ('ClO_{3}^{−}', ('Cl', {'O': 3}, -1), 'trigonal pyramidal', 'sp^{3}', 1, True),
      ('ClO_{4}^{−}', ('Cl', {'O': 4}, -1), 'tetrahedral', 'sp^{3}', 0, False), ('SiF_{4}', ('Si', {'F': 4}, 0), 'tetrahedral', 'sp^{3}', 0, False), ('CCl_{4}', ('C', {'Cl': 4}, 0), 'tetrahedral', 'sp^{3}', 0, False),
      ('H_{2}S', ('S', {'H': 2}, 0), 'bent', 'sp^{3}', 2, True), ('OF_{2}', ('O', {'F': 2}, 0), 'bent', 'sp^{3}', 2, True), ('PCl_{5}', ('P', {'Cl': 5}, 0), 'trigonal bipyramidal', 'sp^{3}d', 0, False),
      ('PF_{5}', ('P', {'F': 5}, 0), 'trigonal bipyramidal', 'sp^{3}d', 0, False), ('SF_{4}', ('S', {'F': 4}, 0), 'see-saw', 'sp^{3}d', 1, True), ('ClF_{3}', ('Cl', {'F': 3}, 0), 'T-shaped', 'sp^{3}d', 2, True),
      ('BrF_{3}', ('Br', {'F': 3}, 0), 'T-shaped', 'sp^{3}d', 2, True), ('XeF_{2}', ('Xe', {'F': 2}, 0), 'linear', 'sp^{3}d', 3, False), ('I_{3}^{−}', ('I', {'I': 2}, -1), 'linear', 'sp^{3}d', 3, False),
      ('ICl_{2}^{−}', ('I', {'Cl': 2}, -1), 'linear', 'sp^{3}d', 3, False), ('IF_{4}^{+}', ('I', {'F': 4}, 1), 'see-saw', 'sp^{3}d', 1, True), ('XeO_{2}F_{2}', ('Xe', {'O': 2, 'F': 2}, 0), 'see-saw', 'sp^{3}d', 1, True),
      ('SF_{6}', ('S', {'F': 6}, 0), 'octahedral', 'sp^{3}d^{2}', 0, False), ('BrF_{5}', ('Br', {'F': 5}, 0), 'square pyramidal', 'sp^{3}d^{2}', 1, True), ('IF_{5}', ('I', {'F': 5}, 0), 'square pyramidal', 'sp^{3}d^{2}', 1, True),
      ('ClF_{5}', ('Cl', {'F': 5}, 0), 'square pyramidal', 'sp^{3}d^{2}', 1, True), ('XeF_{4}', ('Xe', {'F': 4}, 0), 'square planar', 'sp^{3}d^{2}', 2, False), ('ICl_{4}^{−}', ('I', {'Cl': 4}, -1), 'square planar', 'sp^{3}d^{2}', 2, False),
      ('BrF_{4}^{−}', ('Br', {'F': 4}, -1), 'square planar', 'sp^{3}d^{2}', 2, False), ('XeOF_{4}', ('Xe', {'O': 1, 'F': 4}, 0), 'square pyramidal', 'sp^{3}d^{2}', 1, True), ('IF_{7}', ('I', {'F': 7}, 0), 'pentagonal bipyramidal', 'sp^{3}d^{3}', 0, False),
      ('XeF_{6}', ('Xe', {'F': 6}, 0), 'distorted octahedral', 'sp^{3}d^{3}', 1, True), ('XeO_{3}', ('Xe', {'O': 3}, 0), 'trigonal pyramidal', 'sp^{3}', 1, True), ('BrF_{2}^{+}', ('Br', {'F': 2}, 1), 'bent', 'sp^{3}', 2, True),
      ('SOCl_{2}', ('S', {'O': 1, 'Cl': 2}, 0), 'trigonal pyramidal', 'sp^{3}', 1, True), ('CHCl_{3}', ('C', {'H': 1, 'Cl': 3}, 0), 'tetrahedral', 'sp^{3}', 0, True), ('ClO_{2}^{−}', ('Cl', {'O': 2}, -1), 'bent', 'sp^{3}', 2, True)]
from vsepr import USE
USE.setdefault('I', 1)
SHAPES = sorted({s[2] for s in SP})
def chk_sp(name):   # first-principles
    c, l, q = next(s[1] for s in SP if s[0] == name); return vsepr(c, l, q)
def g_shape(rng):
    t = rng.choice(['shape', 'hyb', 'lp', 'count', 'count', 'iso', 'odd'])
    if t == 'shape':
        s = rng.choice(SP); o, a = mcq(rng, s[2], rng.sample([x for x in SHAPES if x != s[2]], 6))
        return dict(q=f'The shape of {s[0]} is :', o=o, a=a, sol=[f'{s[0]}: {s[4]} lone pair(s) on the central atom.', f'Shape: {s[2]} ({s[3]}).'], p=dict(t=t, n=s[0]))
    if t == 'hyb':
        s = rng.choice(SP); H = ['sp', 'sp^{2}', 'sp^{3}', 'sp^{3}d', 'sp^{3}d^{2}', 'sp^{3}d^{3}']; o, a = mcq(rng, s[3], [h for h in H if h != s[3]])
        return dict(q=f'The hybridisation of the central atom in {s[0]} is :', o=o, a=a, sol=['Steric number = σ bonds + lone pairs on the central atom.', f'{s[0]} → {s[3]}.'], p=dict(t=t, n=s[0]))
    if t == 'lp':
        pool = rng.sample(SP, rng.randint(4, 7)); tot = sum(s[4] for s in pool)
        return dict(q=f'Total number of lone pairs on the CENTRAL atoms of {", ".join(s[0] for s in pool)} is ____.', o=None, a=tot,
                    sol=['lone pairs = ½(valence e^{−} of centre − charge − electrons used in bonds).', '; '.join(f'{s[0]} {s[4]}' for s in pool) + f' → {tot}.'], p=dict(t=t, ns=[s[0] for s in pool]))
    if t == 'count':
        pool = rng.sample(SP, rng.randint(5, 8)); key, val = rng.choice([('hyb', h) for h in ('sp^{2}', 'sp^{3}', 'sp^{3}d', 'sp^{3}d^{2}')] + [('shape', x) for x in ('linear', 'tetrahedral', 'square planar', 'see-saw', 'T-shaped', 'bent', 'trigonal pyramidal', 'square pyramidal')])
        n = sum(1 for s in pool if (s[3] if key == 'hyb' else s[2]) == val); need(n >= 1)
        return dict(q=f'Number of species with {"a " + val + " hybridised central atom" if key == "hyb" else val + " shape"} among {", ".join(s[0] for s in pool)} is ____.', o=None, a=n,
                    sol=['Work out σ bonds and lone pairs for each.', '; '.join(f'{s[0]} {s[3] if key == "hyb" else s[2]}' for s in pool) + f' → {n}.'], p=dict(t=t, ns=[s[0] for s in pool], key=key, val=val))
    if t == 'iso':
        s = rng.choice(SP); same = [x for x in SP if x[2] == s[2] and x[0] != s[0]]; need(same); r = rng.choice(same)
        wrong = rng.sample([x[0] for x in SP if x[2] != s[2]], 3); o, a = mcq(rng, r[0], wrong)
        return dict(q=f'Which species is isostructural with {s[0]}?', o=o, a=a, sol=[f'{s[0]} is {s[2]}.', f'{r[0]} is also {s[2]}.'], p=dict(t=t, n=s[0], r=r[0]))
    pool = rng.sample(SP, 4); shapes = [s[2] for s in pool]; need(len(set(shapes)) >= 2)
    for odd in pool:
        others = [x for x in pool if x is not odd]
        if len({x[3] for x in others}) == 1 and odd[3] != others[0][3]:
            o, a = mcq(rng, odd[0], [x[0] for x in others])
            return dict(q=f'Which one has a DIFFERENT hybridisation of the central atom from the other three?', o=o, a=a, sol=['; '.join(f'{x[0]} {x[3]}' for x in pool) + '.'], p=dict(t='odd', ns=[x[0] for x in pool], odd=odd[0]))
    raise AssertionError

H_BOND = {'H_{2}O': True, 'NH_{3}': True, 'HF': True, 'CH_{3}OH': True, 'C_{2}H_{5}OH': True, 'CH_{3}COOH': True, 'CH_{4}': False, 'C_{2}H_{6}': False, 'PH_{3}': False, 'H_{2}S': False, 'HCl': False, 'CHCl_{3}': False,
          'C_{6}H_{6}': False, 'CH_{3}NH_{2}': True, 'N_{2}H_{4}': True, 'H_{2}O_{2}': True, '(CH_{3})_{3}N': False, 'CH_{3}OCH_{3}': False, 'HCOOH': True, 'SiH_{4}': False}
MU = {'NF_{3}': 0.24, 'NH_{3}': 1.47, 'H_{2}O': 1.85, 'HF': 1.91, 'HCl': 1.03, 'HBr': 0.82, 'HI': 0.38, 'H_{2}S': 0.95, 'CHCl_{3}': 1.04, 'CH_{2}Cl_{2}': 1.60, 'CH_{3}Cl': 1.86, 'SO_{2}': 1.63, 'PH_{3}': 0.58}
def g_polar(rng):
    t = rng.choice(['zero', 'zero', 'pol', 'hb', 'mu', 'ionic'])
    if t == 'zero':
        pool = rng.sample(SP, rng.randint(5, 8)); n = sum(1 for s in pool if not s[5])
        return dict(q=f'Number of species with ZERO dipole moment among {", ".join(s[0] for s in pool)} is ____.', o=None, a=n,
                    sol=['μ = 0 only if the shape is symmetric AND all ligands are the same.', '; '.join(f'{s[0]} {"0" if not s[5] else "≠ 0"}' for s in pool) + f' → {n}.'], p=dict(t=t, ns=[s[0] for s in pool]))
    if t == 'pol':
        P = [s for s in SP if s[5]]; N = [s for s in SP if not s[5]]; r = rng.choice(P); w = rng.sample(N, 3); o, a = mcq(rng, r[0], [x[0] for x in w])
        return dict(q='Which of the following has a non-zero dipole moment?', o=o, a=a, sol=[f'{r[0]} is {r[2]} → bond dipoles do not cancel.', 'The others are symmetric: ' + ', '.join(f'{x[0]} ({x[2]})' for x in w) + '.'], p=dict(t=t, r=r[0], w=[x[0] for x in w]))
    if t == 'hb':
        pool = rng.sample(list(H_BOND), rng.randint(5, 8)); n = sum(1 for s in pool if H_BOND[s])
        return dict(q=f'How many of these can form intermolecular hydrogen bonds: {", ".join(pool)} ?', o=None, a=n, sol=['Needs H bonded directly to N, O or F.', f'Yes: {", ".join(s for s in pool if H_BOND[s])} → {n}.'], p=dict(t=t, ns=pool))
    if t == 'mu':
        pool = rng.sample(list(MU), 4); need(len({MU[x] for x in pool}) == 4); right = ' < '.join(sorted(pool, key=MU.get))
        alts = set()
        while len(alts) < 3:
            sh = pool[:]; rng.shuffle(sh); s = ' < '.join(sh)
            if s != right: alts.add(s)
        o, a = mcq(rng, right, list(alts))
        return dict(q=f'Increasing order of dipole moment of {", ".join(pool)} is :', o=o, a=a, sol=['Measured μ (D): ' + ', '.join(f'{x} {MU[x]}' for x in pool) + '.'], p=dict(t=t, ns=pool))
    mu = rng.choice([0.38, 0.82, 1.03, 1.2, 1.5, 1.91, 2.0, 2.5]); d = rng.choice([0.92, 1.0, 1.27, 1.41, 1.5, 1.6, 2.0])
    pct = mu * 1e-18 / (4.8e-10 * d * 1e-8) * 100; need(abs(pct % 1 - 0.5) > 0.02)
    return dict(q=f'A diatomic molecule has dipole moment {mu} D and bond length {d} Å. Its percentage ionic character is ____ (nearest integer; e = 4.8 × 10^{{−10}} esu, 1 D = 10^{{−18}} esu cm).', o=None, a=round(pct),
                sol=['μ(100% ionic) = e × d.', f'% = \\f{{{mu} × 10^{{−18}}}}{{4.8 × 10^{{−10}} × {d} × 10^{{−8}}}} × 100 ≈ {nf(pct, 3)}.'], p=dict(t='ionic', mu=mu, d=d))

DIA = {'H_{2}': (1, 0), 'H_{2}^{+}': (0.5, 1), 'He_{2}^{+}': (0.5, 1), 'Li_{2}': (1, 0), 'Be_{2}': (0, 0), 'B_{2}': (1, 2), 'C_{2}': (2, 0), 'N_{2}': (3, 0), 'N_{2}^{+}': (2.5, 1), 'N_{2}^{−}': (2.5, 1),
       'N_{2}^{2−}': (2, 2), 'O_{2}': (2, 2), 'O_{2}^{+}': (2.5, 1), 'O_{2}^{−}': (1.5, 1), 'O_{2}^{2−}': (1, 0), 'O_{2}^{2+}': (3, 0), 'F_{2}': (1, 0), 'Ne_{2}': (0, 0), 'CO': (3, 0), 'NO': (2.5, 1), 'NO^{+}': (3, 0), 'CN^{−}': (3, 0), 'C_{2}^{2−}': (3, 0), 'NO^{−}': (2, 2)}
DIA_MO = {'H_{2}': ('H', 'H', 0), 'H_{2}^{+}': ('H', 'H', 1), 'He_{2}^{+}': ('He', 'He', 1), 'Li_{2}': ('Li', 'Li', 0), 'Be_{2}': ('Be', 'Be', 0), 'B_{2}': ('B', 'B', 0), 'C_{2}': ('C', 'C', 0), 'N_{2}': ('N', 'N', 0),
          'N_{2}^{+}': ('N', 'N', 1), 'N_{2}^{−}': ('N', 'N', -1), 'N_{2}^{2−}': ('N', 'N', -2), 'O_{2}': ('O', 'O', 0), 'O_{2}^{+}': ('O', 'O', 1), 'O_{2}^{−}': ('O', 'O', -1), 'O_{2}^{2−}': ('O', 'O', -2), 'O_{2}^{2+}': ('O', 'O', 2),
          'F_{2}': ('F', 'F', 0), 'Ne_{2}': ('Ne', 'Ne', 0), 'CO': ('C', 'O', 0), 'NO': ('N', 'O', 0), 'NO^{+}': ('N', 'O', 1), 'CN^{−}': ('C', 'N', -1), 'C_{2}^{2−}': ('C', 'C', -2), 'NO^{−}': ('N', 'O', -1)}
Z = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10}
def bo_s(x): return nf(x) if x != int(x) else str(int(x))
def g_mot(rng):
    t = rng.choice(['bo', 'para', 'len', 'cnt', 'same'])
    if t == 'bo':
        s = rng.choice(list(DIA)); b = DIA[s][0]; o, a = mcq(rng, bo_s(b), [bo_s(x) for x in (0, 0.5, 1, 1.5, 2, 2.5, 3) if x != b])
        return dict(q=f'The bond order of {s} is :', o=o, a=a, sol=['Bond order = ½(bonding − antibonding electrons).', f'{s}: {bo_s(b)}.'], p=dict(t=t, s=s))
    if t == 'para':
        pool = rng.sample(list(DIA), rng.randint(5, 8)); n = sum(1 for s in pool if DIA[s][1] > 0)
        return dict(q=f'Number of paramagnetic species among {", ".join(pool)} is ____.', o=None, a=n, sol=['Fill the MOs (s–p mixing up to 14 electrons) and look for unpaired electrons.', f'Paramagnetic: {", ".join(s for s in pool if DIA[s][1] > 0) or "none"} → {n}.'], p=dict(t=t, ns=pool))
    if t == 'len':
        fam = rng.choice([['O_{2}^{+}', 'O_{2}', 'O_{2}^{−}', 'O_{2}^{2−}'], ['N_{2}', 'N_{2}^{+}', 'N_{2}^{2−}', 'O_{2}^{2−}'], ['NO^{+}', 'NO', 'NO^{−}', 'O_{2}^{2−}'], ['C_{2}', 'B_{2}', 'N_{2}', 'O_{2}^{−}']])
        pool = fam[:]; rng.shuffle(pool); need(len({DIA[x][0] for x in pool}) == 4); right = ' < '.join(sorted(pool, key=lambda x: -DIA[x][0]))
        alts = set()
        while len(alts) < 3:
            sh = pool[:]; rng.shuffle(sh); s = ' < '.join(sh)
            if s != right: alts.add(s)
        o, a = mcq(rng, right, list(alts))
        return dict(q=f'Increasing order of bond LENGTH of {", ".join(pool)} is :', o=o, a=a, sol=['Higher bond order → shorter bond.', 'Bond orders: ' + ', '.join(f'{x} {bo_s(DIA[x][0])}' for x in pool) + '.'], p=dict(t=t, ns=pool))
    if t == 'cnt':
        b = rng.choice([1, 2, 2.5, 3, 0.5]); pool = rng.sample(list(DIA), rng.randint(5, 8)); n = sum(1 for s in pool if DIA[s][0] == b); need(n >= 1)
        return dict(q=f'Number of species with bond order {bo_s(b)} among {", ".join(pool)} is ____.', o=None, a=n, sol=['; '.join(f'{s} {bo_s(DIA[s][0])}' for s in pool) + f' → {n}.'], p=dict(t=t, ns=pool, b=b))
    s = rng.choice(list(DIA)); same = [x for x in DIA if x != s and sum(Z[e] for e in DIA_MO[x][:2]) - DIA_MO[x][2] == sum(Z[e] for e in DIA_MO[s][:2]) - DIA_MO[s][2]]; need(same)
    r = rng.choice(same); wrong = rng.sample([x for x in DIA if x not in same and x != s], 3); o, a = mcq(rng, r, wrong)
    return dict(q=f'Which species is isoelectronic with {s}?', o=o, a=a, sol=[f'Count electrons: {s} has {sum(Z[e] for e in DIA_MO[s][:2]) - DIA_MO[s][2]}.', f'{r} has the same number.'], p=dict(t='same', s=s, r=r))

def g_lewis(rng):
    t = rng.choice(['fc', 'fc', 'pct', 'octet'])
    if t == 'fc':
        V_, nb, b = rng.choice([(6, 4, 2), (6, 6, 1), (6, 2, 3), (5, 0, 4), (5, 2, 3), (5, 4, 2), (4, 0, 4), (4, 2, 3), (7, 6, 1), (6, 0, 4)]); el = {4: 'C', 5: 'N', 6: 'O', 7: 'Cl'}[V_]
        fc = V_ - nb - b; ctx = rng.choice(['a Lewis structure', 'one resonance form', 'a structure drawn on the board'])
        o, a = mcq(rng, ('+' if fc > 0 else '−' if fc < 0 else '') + str(abs(fc)), [x for x in ['−2', '−1', '0', '+1', '+2'] if x != ('+' if fc > 0 else '−' if fc < 0 else '') + str(abs(fc))])
        return dict(q=f'In {ctx}, a(n) {el} atom has {nb} non-bonding electrons and forms {b} bond(s). Its formal charge is :', o=o, a=a, sol=['FC = valence e^{−} − non-bonding e^{−} − bonds.', f'= {V_} − {nb} − {b} = {fc}.'], p=dict(t=t, V=V_, nb=nb, b=b))
    if t == 'pct':
        mu = rng.choice([0.4, 0.8, 1.0, 1.1, 1.6, 1.8, 2.4, 3.0]); d = rng.choice([1.0, 1.2, 1.3, 1.5, 1.6, 2.0, 2.4])
        q = mu * 1e-18 / (d * 1e-8); need(abs(mu / d * 10 % 1 - 0.5) > 0.02)
        return dict(q=f'A diatomic molecule has μ = {mu} D and bond length {d} Å. The charge on each end is ____ × 10^{{−11}} esu (nearest integer; 1 D = 10^{{−18}} esu cm).', o=None, a=round(q / 1e-11), sol=['μ = q × d.', f'q = \\f{{{mu} × 10^{{−18}}}}{{{d} × 10^{{−8}}}} ≈ {nf(q, 3)} esu.'], p=dict(t=t, mu=mu, d=d))
    pool = rng.sample(['BF_{3}', 'BeCl_{2}', 'NO_{2}', 'NO', 'ClO_{2}', 'PCl_{5}', 'SF_{6}', 'H_{2}SO_{4}', 'CO_{2}', 'NH_{3}', 'CH_{4}', 'H_{2}O', 'AlCl_{3}', 'IF_{7}', 'N_{2}'], rng.randint(5, 8))
    bad = {'BF_{3}', 'BeCl_{2}', 'NO_{2}', 'NO', 'ClO_{2}', 'PCl_{5}', 'SF_{6}', 'H_{2}SO_{4}', 'AlCl_{3}', 'IF_{7}'}; n = sum(1 for x in pool if x in bad)
    return dict(q=f'How many of these violate the octet rule (incomplete octet, odd electron or expanded octet) at the central atom: {", ".join(pool)} ?', o=None, a=n,
                sol=['Incomplete: BF_{3}, BeCl_{2}, AlCl_{3}. Odd-electron: NO, NO_{2}, ClO_{2}. Expanded: PCl_{5}, SF_{6}, H_{2}SO_{4}, IF_{7}.', f'→ {n}.'], p=dict(t='octet', ns=pool))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, StopIteration): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(shape=g_shape, polar=g_polar, mot=g_mot, lewis=g_lewis).items()}
def finish(it): return it

def _mo(s): a, b, q = DIA_MO[s]; return mo(a, b, q)
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'shape': return Rv == chk_sp(p['n'])['shape']
    if t == 'hyb': return Rv == chk_sp(p['n'])['hyb']
    if t == 'lp': return Rv == sum(chk_sp(n)['lp'] for n in p['ns'])
    if t == 'count': return Rv == sum(1 for n in p['ns'] if chk_sp(n)[p['key']] == p['val'])
    if t == 'iso': return chk_sp(Rv)['shape'] == chk_sp(p['n'])['shape'] and sum(1 for x in it['o'] if chk_sp(x)['shape'] == chk_sp(p['n'])['shape']) == 1
    if t == 'odd':
        hs = {n: chk_sp(n)['hyb'] for n in p['ns']}; return sum(1 for n in p['ns'] if hs[n] == hs[Rv]) == 1 and len(set(hs.values())) == 2
    if t == 'zero': return Rv == sum(1 for n in p['ns'] if not chk_sp(n)['polar'])
    if t == 'pol': return chk_sp(Rv)['polar'] and all(not chk_sp(x)['polar'] for x in it['o'] if x != Rv)
    if t == 'hb':   # H on N/O/F, read from the formula text
        def hb(f): return f in ('H_{2}O', 'NH_{3}', 'HF', 'H_{2}O_{2}', 'N_{2}H_{4}') or f.endswith('OH') or 'COOH' in f or 'NH_{2}' in f
        return Rv == sum(1 for x in p['ns'] if hb(x))
    if t == 'mu': return Rv == ' < '.join(sorted(p['ns'], key=MU.get))
    if t == 'ionic': return Rv == round(p['mu'] / (4.8 * p['d']) * 100)   # 100% ionic: 4.8 D per Å
    if t == 'bo': return float(Rv) == _mo(p['s'])['bo']
    if t == 'para': return Rv == sum(1 for s in p['ns'] if _mo(s)['unpaired'] > 0)
    if t == 'len': return Rv == ' < '.join(sorted(p['ns'], key=lambda s: -_mo(s)['bo']))
    if t == 'cnt': return Rv == sum(1 for s in p['ns'] if _mo(s)['bo'] == p['b'])
    if t == 'same': return _mo(Rv)['electrons'] + (16 if False else 0) == _mo(p['s'])['electrons']
    if t == 'fc': return int(Rv.replace('−', '-').replace('+', '')) == p['V'] - p['nb'] - p['b']
    if t == 'pct': return Rv == round(p['mu'] / p['d'] * 10)
    if t == 'octet':
        def viol(f):
            if f in ('NO', 'NO_{2}', 'ClO_{2}'): return True
            d = {'BF_{3}': ('B', {'F': 3}, 0), 'BeCl_{2}': ('Be', {'Cl': 2}, 0), 'AlCl_{3}': ('Al', {'Cl': 3}, 0), 'PCl_{5}': ('P', {'Cl': 5}, 0), 'SF_{6}': ('S', {'F': 6}, 0), 'H_{2}SO_{4}': ('S', {'O': 2, 'OH': 2}, 0),
                 'CO_{2}': ('C', {'O': 2}, 0), 'NH_{3}': ('N', {'H': 3}, 0), 'CH_{4}': ('C', {'H': 4}, 0), 'H_{2}O': ('O', {'H': 2}, 0), 'IF_{7}': ('I', {'F': 7}, 0), 'N_{2}': None}[f]
            if d is None: return False
            v = vsepr(*d); shared = sum((2 if k == 'O' else 1) * n for k, n in d[1].items()); return 2 * shared + 2 * v['lp'] != 8
        return Rv == sum(1 for x in p['ns'] if viol(x))
    raise KeyError(t)
