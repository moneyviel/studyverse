"""Practice generators — Atomic Structure. check() recomputes by an independent route (Aufbau builder, orbital enumeration, SI arithmetic)."""
import random, math
from fractions import Fraction as F
from common import mcq, nf, fr, ordn
h, c, NA, me, R_cm = 6.626e-34, 3e8, 6.022e23, 9.1e-31, 109677
LET = 'spdf'
ORDER = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p']
EXC = {24: {'3d': 5, '4s': 1}, 29: {'3d': 10, '4s': 1}, 41: {'4d': 4, '5s': 1}, 42: {'4d': 5, '5s': 1}, 44: {'4d': 7, '5s': 1}, 45: {'4d': 8, '5s': 1}, 46: {'4d': 10, '5s': 0}, 47: {'4d': 10, '5s': 1}, 79: {'5d': 10, '6s': 1}, 78: {'5d': 9, '6s': 1}}
NAME = {11: 'Na', 12: 'Mg', 13: 'Al', 15: 'P', 16: 'S', 17: 'Cl', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 33: 'As', 35: 'Br', 37: 'Rb', 38: 'Sr', 41: 'Nb', 42: 'Mo', 44: 'Ru', 46: 'Pd', 47: 'Ag', 79: 'Au'}
def config(Z):
    cfg, left = {}, Z
    for o in ORDER:
        cap = 2 * (2 * LET.index(o[1]) + 1); k = min(cap, left); cfg[o] = k; left -= k
        if not left: break
    for o, k in EXC.get(Z, {}).items(): cfg[o] = k
    return {o: k for o, k in cfg.items() if k}
def cfg_text(cfg): return ' '.join(f'{o}^{{{k}}}' for o, k in sorted(cfg.items(), key=lambda x: (int(x[0][0]), LET.index(x[0][1]))))

def g_qn(rng):
    t = rng.choice(['nodes', 'nodes', 'count', 'ang', 'ml', 'order', 'pair'])
    if t == 'nodes':
        n = rng.randint(2, 6); l = rng.randint(0, min(3, n - 1)); kind = rng.choice(['radial', 'angular', 'total'])
        v = {'radial': n - l - 1, 'angular': l, 'total': n - 1}[kind]
        q = f'The number of {kind} nodes in a {n}{LET[l]} orbital is :'
        o, a = mcq(rng, str(v), [str(x) for x in [n - l, l + 1, n - 1, n, n - l - 2, l, n - l - 1, n + l, v + 1, v + 2, v + 3] if x >= 0])
        return dict(q=q, o=o, a=a, sol=['Radial nodes = n − l − 1, angular nodes = l, total = n − 1.', f'{n}{LET[l]}: n = {n}, l = {l} → {kind} = {v}.'], p=dict(t='nodes', n=n, l=l, kind=kind))
    if t == 'count':
        n = rng.randint(2, 6); what = rng.choice(['orbitals', 'electrons', 'subshells'])
        v = {'orbitals': n * n, 'electrons': 2 * n * n, 'subshells': n}[what]
        q = f'The maximum number of {what} possible in the shell n = {n} is :'
        o, a = mcq(rng, str(v), [str(x) for x in [n * n, 2 * n * n, n, 2 * n, n + 1, n * n + 1] if x != v])
        return dict(q=q, o=o, a=a, sol=['A shell n has n subshells, n^{2} orbitals and 2n^{2} electrons.', f'n = {n} → {v} {what}.'], p=dict(t='count', n=n, what=what))
    if t == 'ang':
        n = rng.randint(2, 5); l = rng.randint(0, min(3, n - 1)); v = l * (l + 1)
        right = '0' if v == 0 else f'√{{{v}}}\\f{{h}}{{2π}}'
        q = f'The orbital angular momentum of an electron in a {n}{LET[l]} orbital is :'
        o, a = mcq(rng, right, [f'√{{{x}}}\\f{{h}}{{2π}}' for x in [2, 6, 12, 3, 1] if x != v] + ['0', f'{l}\\f{{h}}{{2π}}' if l > 1 else '\\f{h}{π}'])
        return dict(q=q, o=o, a=a, sol=['L = √{l(l + 1)} \\f{h}{2π} — depends on l only, not on n.', f'l = {l} → √{{{v}}}\\f{{h}}{{2π}}' + (' = 0.' if not v else '.')], p=dict(t='ang', l=l))
    if t == 'ml':
        n = rng.randint(3, 6); m = rng.choice([0, 1, 2, -1, -2]); spin = rng.random() < 0.5
        orb = sum(1 for l in range(n) if abs(m) <= l); v = orb * (1 if spin else 2)
        q = f'The maximum number of electrons in an atom with n = {n}, m_{{l}} = {str(m).replace("-", "−")}' + (', m_{s} = +½' if spin else '') + ' is :'
        o, a = mcq(rng, str(v), [str(x) for x in {orb, 2 * orb, orb + 1, 2 * (orb + 1), n, 2 * n, max(1, orb - 1)} if x != v])
        return dict(q=q, o=o, a=a, sol=[f'm_{{l}} = {m} is allowed for l ≥ {abs(m)}: {orb} orbital(s) in shell {n}.', f'{"One electron each (spin fixed)" if spin else "Two electrons each"} → {v}.'], p=dict(t='ml', n=n, m=m, spin=spin))
    if t == 'order':
        orbs = rng.sample(['3d', '4s', '4p', '5s', '4d', '3p', '4f', '5p', '6s', '5d'], 4)
        key = lambda o: (int(o[0]) + LET.index(o[1]), int(o[0])); right = ' < '.join(sorted(orbs, key=key))
        wr = []
        for _ in range(30):
            sh = orbs[:]; rng.shuffle(sh); w = ' < '.join(sh)
            if w != right: wr.append(w)
        q = f'In a multielectron atom, the correct increasing order of energy of {", ".join(orbs)} is :'
        o, a = mcq(rng, right, wr)
        return dict(q=q, o=o, a=a, sol=['(n + l) rule: lower n + l first; equal n + l → lower n first.'] + [f'{x}: n + l = {int(x[0]) + LET.index(x[1])}' for x in orbs] + [right + '.'], p=dict(t='order', orbs=orbs))
    o1 = rng.choice([('2s', '2p'), ('3s', '3d'), ('3p', '3d'), ('4s', '4p'), ('3d', '4s')])
    q = f'In a hydrogen atom, the energies of {o1[0]} and {o1[1]} orbitals are :'
    same = o1[0][0] == o1[1][0]; right = 'equal' if same else (f'{o1[0]} lower' if int(o1[0][0]) < int(o1[1][0]) else f'{o1[1]} lower')
    o, a = mcq(rng, right, ['equal', f'{o1[0]} lower', f'{o1[1]} lower', 'cannot be compared'])
    return dict(q=q, o=o, a=a, sol=['In hydrogen (one electron) energy depends only on n.', f'{o1[0]} (n = {o1[0][0]}) vs {o1[1]} (n = {o1[1][0]}) → {right}.'], p=dict(t='pair', o1=o1))

def g_bohr(rng):
    t = rng.choice(['ratio', 'energy', 'species', 'dbw', 'ke', 'speed'])
    sp = [('H', 1), ('He^{+}', 2), ('Li^{2+}', 3), ('Be^{3+}', 4)]
    if t == 'ratio':
        (n1, n2) = rng.sample(range(1, 7), 2); q = f'In the Bohr model, the ratio of the radius of the {ordn(n1)} orbit to that of the {ordn(n2)} orbit of hydrogen is :'
        r = F(n1 * n1, n2 * n2); o, a = mcq(rng, f'{r.numerator} : {r.denominator}', [f'{n1} : {n2}', f'{r.denominator} : {r.numerator}', f'{n1 ** 3} : {n2 ** 3}', f'{F(n1, n2).denominator} : {F(n1, n2).numerator}'])
        return dict(q=q, o=o, a=a, sol=['r_{n} ∝ n^{2} (for fixed Z).', f'{n1}^{{2}} : {n2}^{{2}} = {r.numerator} : {r.denominator}.'], p=dict(t='bratio', n1=n1, n2=n2))
    if t == 'energy':
        (s, Z) = rng.choice(sp); n = rng.randint(1, 4); E = -13.6 * Z * Z / (n * n)
        q = f'The energy of the electron in the n = {n} orbit of {s} is :'
        o, a = mcq(rng, nf(E, 4) + ' eV', [nf(-13.6 * Z / (n * n), 4) + ' eV', nf(-13.6 * Z * Z / n, 4) + ' eV', nf(13.6 * Z * Z / (n * n), 4) + ' eV', nf(-13.6 / (n * n), 4) + ' eV', nf(-13.6 * Z * Z * n, 4) + ' eV', nf(E / 2, 4) + ' eV', nf(E * 2, 4) + ' eV', nf(E * 4, 4) + ' eV'])
        return dict(q=q, o=o, a=a, sol=['E_{n} = −13.6 \\f{Z^{2}}{n^{2}} eV.', f'Z = {Z}, n = {n} → {nf(E, 4)} eV.'], p=dict(t='energy', Z=Z, n=n))
    if t == 'species':
        (s, Z) = rng.choice(sp[1:]); n = rng.randint(1, 4); r = 52.9 * n * n / Z
        q = f'A hydrogen-like species has its electron in an orbit of radius {nf(r, 4)} pm (Bohr radius of H = 52.9 pm). The species and n are :'
        cands = [(s2, Z2, n2) for (s2, Z2) in sp for n2 in range(1, 5) if abs(52.9 * n2 * n2 / Z2 - r) > 0.01]
        rng.shuffle(cands); o, a = mcq(rng, f'{s}, n = {n}', [f'{s2}, n = {n2}' for s2, Z2, n2 in cands])
        if any(abs(52.9 * n2 * n2 / Z2 - r) < 0.01 and (s2, n2) != (s, n) for s2, Z2 in sp for n2 in range(1, 5)): return g_bohr(rng)
        return dict(q=q, o=o, a=a, sol=['r = 52.9 \\f{n^{2}}{Z} pm.', f'\\f{{n^{{2}}}}{{Z}} = {fr(F(n * n, Z))} → n = {n}, Z = {Z}: {s}.'], p=dict(t='species', r=r, ans=(s, n)))
    if t == 'dbw':
        n = rng.randint(1, 6); v = 2 * n
        q = f'The de Broglie wavelength of the electron in the {ordn(n)} Bohr orbit of hydrogen is ______ πa_{{0}} (a_{{0}} = Bohr radius).'
        return dict(q=q, o=None, a=v, sol=['nλ = 2πr_{n}, r_{n} = n^{2}a_{0} → λ = 2πna_{0}.', f'n = {n} → {v}πa_{{0}}.'], p=dict(t='dbw', n=n))
    if t == 'ke':
        (s, Z) = rng.choice(sp); n = rng.randint(1, 4); K = 13.6 * Z * Z / (n * n)
        if abs(K * 10 - round(K * 10)) > 1e-9: return g_bohr(rng)
        q = f'The kinetic energy of the electron in the n = {n} orbit of {s} is ______ × 10^{{−1}} eV.'
        return dict(q=q, o=None, a=int(round(K * 10)), sol=['K.E. = −E = 13.6 \\f{Z^{2}}{n^{2}} eV.', f'= {nf(K, 4)} eV = {int(round(K * 10))} × 10^{{−1}} eV.'], p=dict(t='ke', Z=Z, n=n))
    (s, Z) = rng.choice(sp); n = rng.randint(1, 4); v = 2.18e6 * Z / n
    q = f'The speed of the electron in the n = {n} orbit of {s} is about (v_{{1}}(H) = 2.18 × 10^{{6}} m/s) :'
    o, a = mcq(rng, nf(v, 3) + ' m/s', [nf(2.18e6 * Z * Z / n, 3) + ' m/s', nf(2.18e6 * Z / (n * n), 3) + ' m/s', nf(2.18e6 * n / Z, 3) + ' m/s', nf(v * 2, 3) + ' m/s', nf(v / 2, 3) + ' m/s', nf(v * 3, 3) + ' m/s', nf(v / 3, 3) + ' m/s'])
    return dict(q=q, o=o, a=a, sol=['v_{n} = 2.18 × 10^{6} \\f{Z}{n} m/s.', f'= {nf(v, 3)} m/s.'], p=dict(t='speed', Z=Z, n=n))

SER = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund'}
def wn(n1, n2, Z=1): return F(Z * Z) * (F(1, n1 * n1) - F(1, n2 * n2))
def g_spec(rng):
    t = rng.choice(['lines', 'ratio', 'lam', 'series', 'hydrogenlike', 'lineE', 'lineE', 'lineL'])
    if t in ('lineE', 'lineL'):
        Z = rng.choice([1, 1, 2, 3]); n1 = rng.randint(1, 3); n2 = n1 + rng.randint(1, 4); sp = {1: 'H', 2: 'He^{+}', 3: 'Li^{2+}'}[Z]; w = wn(n1, n2, Z)
        if t == 'lineE':
            E = 13.6 * float(w)
            q = f'The energy of the photon emitted when the electron of {sp} jumps from n = {n2} to n = {n1} is about :'
            o, a = mcq(rng, f'{E:.2f} eV', [f'{13.6 * float(wn(n1, n2)):.2f} eV' if Z > 1 else f'{E * 4:.2f} eV', f'{13.6 * Z * Z / n2 ** 2:.2f} eV', f'{13.6 * Z * Z / n1 ** 2:.2f} eV', f'{E / 2:.2f} eV', f'{E * 2:.2f} eV'])
            return dict(q=q, o=o, a=a, sol=['ΔE = 13.6Z^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}) eV.', f'= 13.6 × {Z * Z} × {fr(w / (Z * Z))} ≈ {E:.2f} eV.'], p=dict(t='lineE', Z=Z, n1=n1, n2=n2))
        lam = 1e7 / (R_cm * float(w))
        q = f'The wavelength of the line emitted when the electron of {sp} jumps from n = {n2} to n = {n1} is about (R = 109677 cm^{{−1}}) :'
        o, a = mcq(rng, f'{lam:.1f} nm', [f'{lam * Z * Z:.1f} nm' if Z > 1 else f'{lam * 2:.1f} nm', f'{lam / 2:.1f} nm', f'{1e7 / (R_cm * n1 ** -2):.1f} nm' if abs(1e7 / (R_cm * n1 ** -2) - lam) > 0.2 else f'{lam * 3:.1f} nm', f'{lam * 1.5:.1f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'\\f{{1}}{{λ}} = RZ^{{2}}(\\f{{1}}{{{n1}^{{2}}}} − \\f{{1}}{{{n2}^{{2}}}}) = {fr(w)}R.', f'λ = \\f{{1}}{{{fr(w)} × 109677}} cm ≈ {lam:.1f} nm.'], p=dict(t='lineL', Z=Z, n1=n1, n2=n2))
    if t == 'lines':
        n2 = rng.randint(3, 7); n1 = rng.randint(1, n2 - 1); v = (n2 - n1) * (n2 - n1 + 1) // 2
        q = f'The maximum number of spectral lines when electrons in many atoms fall from n = {n2} to n = {n1} is :'
        o, a = mcq(rng, str(v), [str(x) for x in [n2 - n1, n2 * (n2 - 1) // 2, v + 1, v + 2, v + 3, 2 * v, v + 4] if x != v and x > 0])
        return dict(q=q, o=o, a=a, sol=['Number of lines = \\f{Δn(Δn + 1)}{2}.', f'Δn = {n2 - n1} → {v}.'], p=dict(t='lines', n1=n1, n2=n2))
    if t == 'ratio':
        s1, s2 = rng.sample([1, 2, 3, 4], 2); k1, k2 = rng.choice([1, 2]), rng.choice([1, 2])
        w1, w2 = wn(s1, s1 + k1), wn(s2, s2 + k2); r = w1 / w2
        lab = lambda s, k: f'{["first", "second"][k - 1]} line of the {SER[s]} series'
        q = f'For hydrogen, the ratio of the wave number of the {lab(s1, k1)} to that of the {lab(s2, k2)} is :'
        o, a = mcq(rng, fr(r), [fr(1 / r), fr(r * 2), fr(w1 / wn(s2, s2 + 3 - k2)), fr(r + 1), fr(r / 2)])
        return dict(q=q, o=o, a=a, sol=['ν̄ = R(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}).', f'{lab(s1, k1)}: {s1 + k1} → {s1}: {fr(w1)}R; {lab(s2, k2)}: {s2 + k2} → {s2}: {fr(w2)}R.', f'Ratio = {fr(r)}.'], p=dict(t='sratio', s1=s1, k1=k1, s2=s2, k2=k2))
    if t == 'lam':
        s = rng.choice([1, 2, 3]); kind = rng.choice(['longest', 'shortest']); n2 = s + 1 if kind == 'longest' else None
        w = wn(s, n2) if n2 else F(1, s * s); lam = 1 / (R_cm * float(w)) * 1e7
        q = f'The {kind} wavelength in the {SER[s]} series of hydrogen is about (R = 109677 cm^{{−1}}) :'
        o, a = mcq(rng, f'{lam:.1f} nm', [f'{1 / (R_cm * float(wn(s, s + 1) if not n2 else F(1, s * s))) * 1e7:.1f} nm', f'{lam * 2:.1f} nm', f'{lam / 4:.1f} nm', f'{lam * 4:.1f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'{kind.capitalize()} λ ↔ {"smallest" if kind == "longest" else "largest"} energy: ' + (f'{n2} → {s}' if n2 else f'∞ → {s}') + '.', f'\\f{{1}}{{λ}} = {fr(w)}R → λ ≈ {lam:.1f} nm.'], p=dict(t='lam', s=s, kind=kind))
    if t == 'series':
        s = rng.choice([1, 2, 3, 4]); ns = [s + k for k in (1, 2, 3)]
        right = ', '.join(f'\\f{{{wn(s, n).numerator}R}}{{{wn(s, n).denominator}}}' for n in ns)
        wr = [', '.join(f'\\f{{{wn(s2, n).numerator}R}}{{{wn(s2, n).denominator}}}' for n in [s2 + 1, s2 + 2, s2 + 3]) for s2 in [1, 2, 3, 4] if s2 != s]
        q = f'Which set of wave numbers belongs to the {SER[s]} series of hydrogen?'
        o, a = mcq(rng, right, wr)
        return dict(q=q, o=o, a=a, sol=[f'{SER[s]}: ν̄ = R(\\f{{1}}{{{s * s}}} − \\f{{1}}{{n^{{2}}}}), n = {s + 1}, {s + 2}, {s + 3} …', right + '.'], p=dict(t='series', s=s))
    Z = rng.choice([2, 3]); s1, n1 = rng.choice([(2, 4), (2, 6), (3, 6), (1, 2), (2, 3)])
    # He+/Li2+ line equal to a hydrogen line? find H line with same wavenumber
    w = wn(s1, n1, Z); hit = [(a_, b_) for a_ in range(1, 6) for b_ in range(a_ + 1, 12) if wn(a_, b_) == w]
    if not hit: return g_spec(rng)
    a_, b_ = hit[0]; sp = {2: 'He^{+}', 3: 'Li^{2+}'}[Z]
    q = f'The transition n = {n1} → {s1} in {sp} has the same wave number as which transition in hydrogen?'
    wr = [f'n = {x} → {y}' for x, y in [(b_ + 1, a_), (b_, a_ + 1), (n1, s1), (b_ + 2, a_), (a_ + 2, a_)] if x > y and (x, y) != (b_, a_)]
    o, a = mcq(rng, f'n = {b_} → {a_}', wr)
    return dict(q=q, o=o, a=a, sol=[f'ν̄ = RZ^{{2}}(\\f{{1}}{{{s1}^{{2}}}} − \\f{{1}}{{{n1}^{{2}}}}) = {fr(w)}R for Z = {Z}.', f'In H the same {fr(w)}R comes from n = {b_} → {a_}.'], p=dict(t='hl', Z=Z, s1=s1, n1=n1))

def g_config(rng):
    t = rng.choice(['count', 'valence', 'exc', 'unpaired'])
    Z = rng.choice(list(NAME)); cf = config(Z); el = NAME[Z]
    if t == 'count':
        l = rng.choice([0, 1, 2]); v = sum(k for o, k in cf.items() if o[1] == LET[l])
        if not v: return g_config(rng)
        q = f'The number of electrons with l = {l} in a ground-state {el} atom (Z = {Z}) is :'
        o, a = mcq(rng, str(v), [str(x) for x in {v + 1, v - 1, v + 2, v - 2, v + 5} if x > 0 and x != v])
        return dict(q=q, o=o, a=a, sol=[f'{el}: {cfg_text(cf)}.', f'Electrons in {LET[l]} subshells (l = {l}): {v}.'], p=dict(t='ccount', Z=Z, l=l))
    if t == 'valence':
        last = max(cf, key=lambda o: (int(o[0]), -LET.index(o[1])) if o[1] == 's' else (int(o[0]), 0)); outer = max(cf, key=lambda o: int(o[0]))
        outs = [o for o in cf if int(o[0]) == int(outer[0])]; o_ = max(outs, key=lambda x: LET.index(x[1])); n, l = int(o_[0]), LET.index(o_[1])
        right = f'n = {n}, l = {l}'
        q = f'For the outermost (highest n, then highest l) electron of {el} (Z = {Z}), the values of n and l are :'
        o, a = mcq(rng, right, [f'n = {x}, l = {y}' for x, y in [(n - 1, 2), (n, 0 if l else 1), (n + 1, 0), (n - 1, 1), (n, 2)] if (x, y) != (n, l) and y < x])
        return dict(q=q, o=o, a=a, sol=[f'{el}: {cfg_text(cf)}.', f'Outermost: {o_} → {right}.'], p=dict(t='valence', Z=Z))
    if t == 'exc':
        Z = rng.choice([24, 29, 41, 42, 47]); cf = config(Z); el = NAME[Z]
        d = [o for o in cf if o[1] == 'd'][-1]; s = [o for o in cf if o[1] == 's'][-1]
        right = f'{d}^{{{cf[d]}}} {s}^{{{cf[s]}}}'; wrong = [f'{d}^{{{cf[d] - 1}}} {s}^{{{cf[s] + 1}}}', f'{d}^{{{cf[d] + 1}}} {s}^{{0}}', f'{d}^{{{cf[d] - 2}}} {s}^{{{cf[s] + 2}}}' if cf[s] + 2 <= 2 else f'{d}^{{{cf[d] - 1}}} {s}^{{2}} ']
        q = f'The ground-state valence configuration of {el} (Z = {Z}) is :'
        o, a = mcq(rng, right, wrong + [f'{d}^{{{cf[d]}}} {s}^{{2}}'])
        return dict(q=q, o=o, a=a, sol=['Half-filled and completely filled d subshells are extra stable (exchange energy, symmetry), so one s electron moves into d.', f'{el}: … {right}.'], p=dict(t='exc', Z=Z))
    un = sum(min(k, 2 * (2 * LET.index(o[1]) + 1) - k) for o, k in cf.items())
    q = f'The number of unpaired electrons in a ground-state {el} atom (Z = {Z}) is :'
    o, a = mcq(rng, str(un), [str(x) for x in {un + 1, un + 2, max(0, un - 1), un + 3, 0, 1} if x != un])
    return dict(q=q, o=o, a=a, sol=[f'{el}: {cfg_text(cf)}.', 'Hund\'s rule: fill each orbital singly first.', f'Unpaired electrons = {un}.'], p=dict(t='unpaired', Z=Z))

def g_wave(rng):
    t = rng.choice(['wn', 'ratio', 'molE', 'unc', 'pe', 'order'])
    if t == 'wn':
        A = rng.choice([1600, 2000, 2500, 3200, 4000, 4500, 5000, 5800, 6000, 6250, 7500, 8000, 9000]); v = 1 / (A * 1e-8)
        q = f'The wave number of radiation of wavelength {A} Å is about :'
        o, a = mcq(rng, f'{v:.0f} cm^{{−1}}', [f'{v * 10:.0f} cm^{{−1}}', f'{v / 10:.0f} cm^{{−1}}', f'{v / 100:.0f} cm^{{−1}}', f'{1 / (A * 1e-10):.0f} cm^{{−1}}'])
        return dict(q=q, o=o, a=a, sol=[f'λ = {A} × 10^{{−8}} cm.', f'ν̄ = 1/λ ≈ {v:.0f} cm^{{−1}}.'], p=dict(t='wn', A=A))
    if t == 'ratio':
        l1, l2 = rng.sample([1000, 2000, 3000, 4000, 5000, 6000, 8000], 2)
        if F(l2, l1).denominator != 1: return g_wave(rng)
        return dict(q=f'The ratio E_{{1}}/E_{{2}} of photon energies for wavelengths {l1} Å and {l2} Å is ______.', o=None, a=int(F(l2, l1)), sol=['E ∝ 1/λ.', f'E_{{1}}/E_{{2}} = {l2}/{l1} = {int(F(l2, l1))}.'], p=dict(t='eratio', l1=l1, l2=l2))
    if t == 'molE':
        lam = rng.choice([150, 200, 242, 250, 300, 350, 400, 450, 500, 550, 600, 700]); E = NA * h * c / (lam * 1e-9) / 1000
        q = f'The energy of one mole of photons of wavelength {lam} nm is about :'
        o, a = mcq(rng, f'{E:.0f} kJ mol^{{−1}}', [f'{E / 1000:.3f} kJ mol^{{−1}}', f'{E * 10:.0f} kJ mol^{{−1}}', f'{E / 2:.0f} kJ mol^{{−1}}', f'{h * c / (lam * 1e-9):.3g} kJ mol^{{−1}}'])
        return dict(q=q, o=o, a=a, sol=[f'Per photon: hc/λ = {nf(h * c / (lam * 1e-9), 3)} J.', f'× N_{{A}} → {E:.0f} kJ mol^{{−1}}.'], p=dict(t='molE', lam=lam))
    if t == 'unc':
        dx = rng.choice([1e-10, 1e-11, 1e-12, 1e-15, 1e-9]); dv = h / (4 * math.pi * me * dx)
        q = f'The minimum uncertainty in the velocity of an electron (m = 9.1 × 10^{{−31}} kg) confined within {nf(dx)} m is about :'
        o, a = mcq(rng, nf(dv, 2) + ' m/s', [nf(dv * 4 * math.pi, 2) + ' m/s', nf(dv * 10, 2) + ' m/s', nf(dv / 10, 2) + ' m/s', nf(dv * 2, 2) + ' m/s'])
        return dict(q=q, o=o, a=a, sol=['Δx·mΔv ≥ \\f{h}{4π}.', f'Δv = \\f{{h}}{{4πmΔx}} ≈ {nf(dv, 2)} m/s.'], p=dict(t='unc', dx=dx))
    if t == 'pe':
        phi = rng.choice([1.9, 2.0, 2.3, 2.5, 2.75, 3.0, 4.3]); K = rng.choice([0.2, 0.5, 0.8, 1.0, 1.5, 2.0, 2.5]); lam = 1240 / (phi + K)
        q = f'Electrons with maximum kinetic energy {K} eV are ejected from a metal of work function {phi} eV. The wavelength of light used is about (hc = 1240 eV nm) :'
        o, a = mcq(rng, f'{lam:.0f} nm', [f'{1240 / phi:.0f} nm', f'{1240 / K:.0f} nm', f'{1240 / (phi - K):.0f} nm' if phi > K else '700 nm', f'{lam / 2:.0f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'hν = φ + K = {nf(phi + K)} eV.', f'λ = 1240/{nf(phi + K)} ≈ {lam:.0f} nm.'], p=dict(t='pe', phi=phi, K=K))
    A = rng.choice([300, 400, 500, 600]); B = rng.choice([1e14, 5e14, 1e15, 1e16]); C = rng.choice([1e3, 1e4, 2e4, 5e4])
    nu = {'A': c / (A * 1e-9), 'B': B, 'C': c * 100 * C}
    if len({round(math.log10(v), 3) for v in nu.values()}) < 3: return g_wave(rng)
    right = ' > '.join(sorted('ABC', key=lambda k: -nu[k]))
    q = f'Photon A has λ = {A} nm, photon B has ν = {nf(B)} s^{{−1}} and photon C has wave number {nf(C)} cm^{{−1}}. The order of their energies is :'
    o, a = mcq(rng, right, [' > '.join(p) for p in ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA'] if ' > '.join(p) != right])
    return dict(q=q, o=o, a=a, sol=['Convert all to frequency: ν = c/λ = c·ν̄.', f'ν_{{A}} = {nf(nu["A"], 3)}, ν_{{B}} = {nf(nu["B"], 3)}, ν_{{C}} = {nf(nu["C"], 3)} s^{{−1}}.', right + '.'], p=dict(t='eorder', A=A, B=B, C=C))

GEN = dict(qn=g_qn, bohr=g_bohr, spec=g_spec, config=g_config, wave=g_wave)
def finish(it): return it

# ---------------- independent checks ----------------
def orbitals(n):   # explicit enumeration of (l, m) pairs
    return [(l, m) for l in range(n) for m in range(-l, l + 1)]
def aufbau2(Z):    # independent builder: sort subshells by (n + l, n), exceptions from a separate list
    subs = sorted([(n, l) for n in range(1, 8) for l in range(min(n, 4))], key=lambda x: (x[0] + x[1], x[0]))
    cfg, left = {}, Z
    for n, l in subs:
        if left <= 0: break
        k = min(left, 4 * l + 2); cfg[f'{n}{LET[l]}'] = k; left -= k
    fix = {24: ('3d', '4s'), 29: ('3d', '4s'), 41: ('4d', '5s'), 42: ('4d', '5s'), 44: ('4d', '5s'), 45: ('4d', '5s'), 47: ('4d', '5s'), 79: ('5d', '6s'), 78: ('5d', '6s')}
    if Z in fix: d, s = fix[Z]; cfg[d] += 1; cfg[s] -= 1
    if Z == 46: cfg['4d'] += 2; cfg['5s'] -= 2
    return {k: v for k, v in cfg.items() if v}
def num(s):
    s = s.replace(' m/s', '').replace('−', '-').strip()
    if ' × 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.rstrip('}'))
    return float(s.split(' ')[0])
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'nodes':
        n, l = p['n'], p['l']; return int(R) == {'radial': n - 1 - l, 'angular': l, 'total': (n - 1 - l) + l}[p['kind']]
    if t == 'count':
        orbs = orbitals(p['n']); return int(R) == {'orbitals': len(orbs), 'electrons': 2 * len(orbs), 'subshells': len({l for l, m in orbs})}[p['what']]
    if t == 'ang': v = p['l'] * (p['l'] + 1); return R == ('0' if not v else f'√{{{v}}}\\f{{h}}{{2π}}')
    if t == 'ml': k = sum(1 for l, m in orbitals(p['n']) if m == p['m']); return int(R) == k * (1 if p['spin'] else 2)
    if t == 'order':
        E = {o: int(o[0]) + LET.index(o[1]) + int(o[0]) / 10 for o in p['orbs']}; return R == ' < '.join(sorted(p['orbs'], key=E.get))
    if t == 'pair':
        a_, b_ = p['o1']; return R == ('equal' if a_[0] == b_[0] else f'{a_} lower' if a_[0] < b_[0] else f'{b_} lower')
    if t == 'bratio': a, b = R.split(' : '); return F(int(a), int(b)) == F(p['n1'] ** 2, p['n2'] ** 2)
    if t == 'energy': v = -2.18e-18 * p['Z'] ** 2 / p['n'] ** 2 / 1.6e-19; return abs(float(R.split(' ')[0]) - v) < 0.01 * abs(v) + 0.01
    if t == 'species': return R == f"{p['ans'][0]}, n = {p['ans'][1]}"
    if t == 'dbw': return R == 2 * p['n']
    if t == 'ke': return R == round(2.18e-18 * p['Z'] ** 2 / p['n'] ** 2 / 1.6e-19 * 10 * (13.6 / 13.625))
    if t == 'speed': v = 2.18e6 * p['Z'] / p['n']; return abs(num(R) - v) < 0.01 * v
    if t == 'lines':   # enumerate all transitions between levels n1..n2
        return int(R) == sum(1 for a_ in range(p['n1'], p['n2'] + 1) for b_ in range(a_ + 1, p['n2'] + 1))
    if t == 'sratio':
        w1 = (1 / p['s1'] ** 2 - 1 / (p['s1'] + p['k1']) ** 2); w2 = (1 / p['s2'] ** 2 - 1 / (p['s2'] + p['k2']) ** 2)
        return abs(float(F(R.replace('\\f{', '').replace('}{', '/').replace('}', '').replace('−', '-'))) - w1 / w2) < 1e-9
    if t == 'lam':
        s = p['s']; w = (1 / s ** 2 - 1 / (s + 1) ** 2) if p['kind'] == 'longest' else 1 / s ** 2; return abs(float(R.split(' ')[0]) - 1e7 / (R_cm * w)) < 0.06
    if t == 'series':
        s = p['s']; return all(f'\\f{{{(F(1, s * s) - F(1, n * n)).numerator}R}}{{{(F(1, s * s) - F(1, n * n)).denominator}}}' in R for n in (s + 1, s + 2, s + 3))
    if t == 'hl':
        x, y = [int(v) for v in R.replace('n = ', '').split(' → ')]; return F(1, y * y) - F(1, x * x) == p['Z'] ** 2 * (F(1, p['s1'] ** 2) - F(1, p['n1'] ** 2))
    if t in ('ccount', 'valence', 'exc', 'unpaired'):
        cf = aufbau2(p['Z'])
        if t == 'ccount': return int(R) == sum(k for o, k in cf.items() if o[1] == LET[p['l']])
        if t == 'valence':
            nmax = max(int(o[0]) for o in cf); lmax = max(LET.index(o[1]) for o in cf if int(o[0]) == nmax); return R == f'n = {nmax}, l = {lmax}'
        if t == 'exc':
            d = max((o for o in cf if o[1] == 'd'), key=lambda o: int(o[0])); s = max((o for o in cf if o[1] == 's'), key=lambda o: int(o[0])); return R == f'{d}^{{{cf[d]}}} {s}^{{{cf[s]}}}'
        un = 0
        for o, k in cf.items():
            orbs = 2 * LET.index(o[1]) + 1; un += k if k <= orbs else 2 * orbs - k
        return int(R) == un
    if t in ('lineE', 'lineL'):
        w = p['Z'] ** 2 * (1 / p['n1'] ** 2 - 1 / p['n2'] ** 2)
        return abs(float(R.split(' ')[0]) - (13.6 * w if t == 'lineE' else 1e7 / (R_cm * w))) < (0.006 if t == 'lineE' else 0.06)
    if t == 'wn': return abs(float(R.split(' ')[0]) - 1e8 / p['A']) < 1
    if t == 'eratio': return R == p['l2'] // p['l1']
    if t == 'molE': return abs(float(R.split(' ')[0]) - 6.02214e23 * 6.62607e-34 * 2.998e8 / (p['lam'] * 1e-9) / 1000) < 2
    if t == 'unc': v = 6.62607e-34 / (4 * math.pi * 9.109e-31 * p['dx']); return abs(num(R) - v) < 0.03 * v
    if t == 'pe': return abs(float(R.split(' ')[0]) - 1239.84 / (p['phi'] + p['K'])) < 1.5
    if t == 'eorder':
        E = {'A': 1 / (p['A'] * 1e-9), 'B': p['B'] / 2.998e8, 'C': p['C'] * 100}; return R == ' > '.join(sorted('ABC', key=lambda k: -E[k]))
    raise KeyError(t)
