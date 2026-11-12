"""Practice generators — Chemistry Unit 9: Periodicity. check() re-derives answers: trends from the NCERT data table,
IUPAC names by decoding the digit roots, group/period/block by building the electron configuration (Aufbau)."""
import math
from common import mcq, nf
from ptdata import IE1, IE2, EG, EN, RAD, ION, Z
def need(x):
    if not x: raise AssertionError('retry')
PROP = {'first ionisation enthalpy': IE1, 'electronegativity (Pauling)': EN, 'atomic radius': RAD, 'magnitude of electron gain enthalpy': {k: -v for k, v in EG.items() if v < 0}}
ROOT = ['nil', 'un', 'bi', 'tri', 'quad', 'pent', 'hex', 'sept', 'oct', 'enn']
SYM_ = {'nil': 'n', 'un': 'u', 'bi': 'b', 'tri': 't', 'quad': 'q', 'pent': 'p', 'hex': 'h', 'sept': 's', 'oct': 'o', 'enn': 'e'}
def iupac(z):
    rs = [ROOT[int(c)] for c in str(z)]; nm = ''.join(rs) + 'ium'; nm = nm.replace('nnn', 'nn').replace('iium', 'ium'); return nm[0].upper() + nm[1:]
def perms(rng, items, n=3):
    out = set(); right = ' < '.join(items)
    tries = 0
    while len(out) < n and tries < 200:
        tries += 1; sh = items[:]; rng.shuffle(sh); s = ' < '.join(sh)
        if s != right: out.add(s)
    need(len(out) == n); return list(out)

def g_trend(rng, fam):
    props = {'ie': ['first ionisation enthalpy'], 'eg': ['electronegativity (Pauling)', 'magnitude of electron gain enthalpy'], 'rad': ['atomic radius']}[fam]
    t = rng.choice(['ord', 'ord', 'ext', 'pair'] + (['ion'] if fam == 'rad' else []) + (['ie2'] if fam == 'ie' else []))
    if t == 'ion':
        grp = rng.choice([['N^{3−}', 'O^{2−}', 'F^{−}', 'Na^{+}', 'Mg^{2+}', 'Al^{3+}'], ['S^{2−}', 'Cl^{−}', 'K^{+}', 'Ca^{2+}'], ['Li^{+}', 'Na^{+}', 'K^{+}', 'Rb^{+}'], ['F^{−}', 'Cl^{−}', 'Br^{−}', 'I^{−}'], ['Be^{2+}', 'Mg^{2+}', 'Ca^{2+}', 'Al^{3+}', 'B^{3+}']])
        pool = rng.sample(grp, 4); need(len({ION[x] for x in pool}) == 4); right = ' < '.join(sorted(pool, key=ION.get)); o, a = mcq(rng, right, perms(rng, sorted(pool, key=ION.get)))
        return dict(q=f'Increasing order of ionic radius of {", ".join(pool)} is :', o=o, a=a, sol=['Ionic radii (pm): ' + ', '.join(f'{x} {nf(ION[x])}' for x in pool) + '.', 'Isoelectronic: more protons → smaller. Down a group: bigger.'], p=dict(t='ion', ns=pool))
    if t == 'ie2':
        e = rng.choice(list(IE2)); x = rng.choice([1, 2, 3.5, 5, 7, 10, 14]); M = {'Li': 7, 'Be': 9, 'B': 10.8, 'Na': 23, 'Mg': 24, 'Al': 27, 'Ga': 69.7, 'K': 39, 'Ca': 40, 'Cr': 52, 'Mn': 55, 'Fe': 56, 'In': 114.8, 'Tl': 204.4}[e]
        E = x / 1000 / M * (IE1[e] + IE2[e])
        return dict(q=f'IE_{{1}} and IE_{{2}} of {e} are {IE1[e]} and {IE2[e]} kJ mol^{{−1}}. Energy to turn {x} mg of gaseous {e} (M = {M}) into {e}^{{2+}}(g) is ____ × 10^{{−2}} kJ (nearest integer).', o=None, a=round(E * 100),
                    sol=[f'n = \\f{{{x} × 10^{{−3}}}}{{{M}}} mol.', f'E = n(IE_{{1}} + IE_{{2}}) ≈ {nf(E, 3)} kJ.'], p=dict(t='ie2', e=e, x=x, M=M))
    pr = rng.choice(props); D = PROP[pr]
    if t == 'ord':
        pool = rng.sample(list(D), 4); need(len({D[x] for x in pool}) == 4); srt = sorted(pool, key=D.get); right = ' < '.join(srt); o, a = mcq(rng, right, perms(rng, srt))
        return dict(q=f'Increasing order of {pr} for {", ".join(pool)} is :', o=o, a=a, sol=['Values: ' + ', '.join(f'{x} {nf(D[x])}' for x in pool) + '.', f'→ {right}.'], p=dict(t='ord', pr=pr, ns=pool))
    if t == 'ext':
        pool = rng.sample(list(D), 4); need(len({D[x] for x in pool}) == 4); hi = rng.choice([True, False]); r = (max if hi else min)(pool, key=D.get); o, a = mcq(rng, r, [x for x in pool if x != r])
        return dict(q=f'Which has the {"highest" if hi else "lowest"} {pr}: {", ".join(pool)} ?', o=o, a=a, sol=['Values: ' + ', '.join(f'{x} {nf(D[x])}' for x in pool) + '.'], p=dict(t='ext', pr=pr, ns=pool, hi=hi))
    a_, b_ = rng.sample(list(D), 2); need(D[a_] != D[b_]); r = f'{a_} > {b_}' if D[a_] > D[b_] else f'{b_} > {a_}'; w = f'{b_} > {a_}' if r.startswith(a_) else f'{a_} > {b_}'
    o, a = mcq(rng, f'{r} — this is correct', [f'{w} — this is correct', f'{a_} = {b_}', 'cannot be compared'])
    return dict(q=f'Compare the {pr} of {a_} and {b_}.', o=o, a=a, sol=[f'{a_} {nf(D[a_])}, {b_} {nf(D[b_])}.'], p=dict(t='pair', pr=pr, a_=a_, b_=b_))
def g_ie(rng): return g_trend(rng, 'ie')
def g_eg(rng): return g_trend(rng, 'eg')
def g_rad(rng): return g_trend(rng, 'rad')

ORDER = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p']
CAP = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
def config(z):
    out = []; left = z
    for sh in ORDER:
        if left <= 0: break
        k = min(left, CAP[sh[1]]); out.append((sh, k)); left -= k
    return out
def gpb(z):
    c = config(z); period = max(int(sh[0]) for sh, _ in c); last = c[-1][0][1]
    if last == 's': grp = c[-1][1] if z != 2 else 18
    elif last == 'p': grp = 12 + c[-1][1]
    elif last == 'd': grp = 2 + c[-1][1]
    else: grp = 3
    return period, grp, last
def g_pt(rng):
    t = rng.choice(['name', 'zname', 'grp', 'per', 'blk', 'hyd'])
    if t == 'name':
        z = rng.randint(101, 118); r = iupac(z); o, a = mcq(rng, r, [iupac(x) for x in rng.sample([y for y in range(101, 120) if y != z], 3)])
        return dict(q=f'The IUPAC (temporary) name of element Z = {z} is :', o=o, a=a, sol=['Digit roots: 0 nil, 1 un, 2 bi, 3 tri, 4 quad, 5 pent, 6 hex, 7 sept, 8 oct, 9 enn; add "-ium".', f'{z} → {r}.'], p=dict(t=t, z=z))
    if t == 'zname':
        z = rng.randint(101, 118); nm = iupac(z); per, grp, _ = gpb(z)
        return dict(q=f'"{nm}" belongs to group n of the periodic table. n = ____', o=None, a=grp, sol=[f'{nm} → Z = {z}.', f'Configuration ends …{config(z)[-1][0]}^{{{config(z)[-1][1]}}} → group {grp}.'], p=dict(t=t, nm=nm))
    if t in ('grp', 'per', 'blk'):
        z = rng.choice(list(range(3, 57)) + list(range(72, 87)) + [104, 107, 110, 113, 115, 117, 118])
        if z in (24, 29, 41, 42, 44, 45, 46, 47, 78, 79): need(False)   # exceptional configurations: skip to keep the Aufbau rule honest
        per, grp, blk = gpb(z)
        if t == 'grp': return dict(q=f'An element has atomic number {z}. Its group number is ____.', o=None, a=grp, sol=['Write the configuration and look at the last subshell.', f'Z = {z}: …{config(z)[-1][0]}^{{{config(z)[-1][1]}}} → group {grp}.'], p=dict(t=t, z=z))
        if t == 'per': return dict(q=f'An element has atomic number {z}. The period it belongs to is ____.', o=None, a=per, sol=['Period = highest principal quantum number used.', f'Z = {z} → period {per}.'], p=dict(t=t, z=z))
        o, a = mcq(rng, f'{blk}-block', [f'{x}-block' for x in 'spdf' if x != blk])
        return dict(q=f'The element with atomic number {z} belongs to the :', o=o, a=a, sol=[f'Last electron enters a {blk} subshell.'], p=dict(t=t, z=z))
    ion, zz = rng.choice([('He^{+}', 2), ('Li^{2+}', 3), ('Be^{3+}', 4), ('B^{4+}', 5)]); n = rng.choice([1, 2, 3]); E = 2.18e-18 * zz * zz / n / n
    o, a = mcq(rng, f'{nf(E, 4)} J', [f'{nf(v, 4)} J' for v in (2.18e-18 * zz / n / n, 2.18e-18 * zz * zz, 2.18e-18 * zz * zz * n, E * 2)])
    return dict(q=f'Energy needed to remove the electron of {ion} from its n = {n} level (IE of H = 2.18 × 10^{{−18}} J) is :', o=o, a=a, sol=['Hydrogen-like ion: E = 2.18 × 10^{−18} \\f{Z^{2}}{n^{2}} J.', f'= 2.18 × 10^{{−18}} × \\f{{{zz * zz}}}{{{n * n}}} ≈ {nf(E, 4)} J.'], p=dict(t='hyd', z=zz, n=n))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(ie=g_ie, eg=g_eg, rad=g_rad, pt=g_pt).items()}
def finish(it): return it
def decode(nm):
    s = nm.lower()[:-3]; z = ''
    while s:
        for i, r in sorted(enumerate(ROOT), key=lambda t: -len(t[1])):
            if s.startswith(r): z += str(i); s = s[len(r):]; break
            if r == 'nil' and s.startswith('il') and z.endswith('1') and False: pass
        else:
            if s.startswith('il') and z and z[-1] in '0': s = s[2:]; continue
            if s.startswith('nnil'): pass
            raise ValueError(nm)
    return int(z)
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'ord':
        D = PROP[p['pr']]; xs = Rv.split(' < '); return all(D[a] < D[b] for a, b in zip(xs, xs[1:])) and sorted(xs) == sorted(p['ns'])
    if t == 'ext': D = PROP[p['pr']]; return all((D[Rv] > D[x]) if p['hi'] else (D[Rv] < D[x]) for x in p['ns'] if x != Rv)
    if t == 'pair':
        D = PROP[p['pr']]; big, small = Rv.split(' — ')[0].split(' > '); return D[big] > D[small]
    if t == 'ion': xs = Rv.split(' < '); return all(ION[a] < ION[b] for a, b in zip(xs, xs[1:]))
    if t == 'ie2': return Rv == round(p['x'] / 1000 / p['M'] * (IE1[p['e']] + IE2[p['e']]) * 100)
    if t == 'name':
        z = p['z']; built = ''.join(ROOT[int(c)] for c in str(z)) + 'ium'; built = built.replace('enn' + 'nil', 'ennil').replace('iium', 'ium')
        return Rv.lower() == built.replace('nnn', 'nn') or Rv.lower() == built
    if t == 'zname':
        nm = p['nm'].lower(); digits = []
        i = 0
        while i < len(nm) - 3:
            for k, r in sorted(enumerate(ROOT), key=lambda t: -len(t[1])):
                if nm.startswith(r, i): digits.append(k); i += len(r); break
                if r == 'nil' and nm.startswith('il', i) and digits and digits[-1] == 9: digits.append(0); i += 2; break
            else: return False
        z = int(''.join(map(str, digits))); col = (z - 86 - 32) if z > 86 else 0   # period 7 runs Fr(87)…Og(118): groups 1, 2, then f-block (89-103), then d from 104
        g = 1 if z == 87 else 2 if z == 88 else 3 if 89 <= z <= 103 else z - 104 + 4 if z <= 112 else z - 113 + 13
        return Rv == g
    if t in ('grp', 'per', 'blk'):
        z = p['z']; nb = [2, 10, 18, 36, 54, 86, 118]; per = next(i + 1 for i, v in enumerate(nb) if z <= v)
        if t == 'per': return Rv == per
        start = [0] + nb; pos = z - start[per - 1]   # position within the period
        if per <= 3: g = pos if pos <= 2 else pos + 10 if per > 1 else (1 if pos == 1 else 18)
        elif per <= 5: g = pos
        else: g = pos if pos <= 2 else (3 if pos <= 17 else pos - 14)
        blk = 's' if g in (1, 2) or z == 2 else 'p' if g >= 13 else 'f' if (per >= 6 and 4 <= pos <= 17) else 'd'
        if t == 'grp': return Rv == g
        return Rv == f'{blk}-block'
    if t == 'hyd': return abs(float(Rv.split(' J')[0].replace(' × 10^{', 'e').replace('}', '').replace('−', '-')) - 13.6 * 1.602e-19 * p['z'] ** 2 / p['n'] ** 2) / (2.18e-18 * p['z'] ** 2 / p['n'] ** 2) < 0.01
    raise KeyError(t)
