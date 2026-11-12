"""Practice generators — Physics Unit 18: Atoms and Nuclei. check() re-solves each item another way: Bohr orbits
built from force balance with SI constants, spectral lines from level energies, decay by stepping dN = −λN dt,
mass defects from nucleon counts, closest approach by marching the particle in."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
k, e, me, h, c, eps0 = 9e9, 1.6e-19, 9.11e-31, 6.626e-34, 3e8, 8.854e-12
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, ex = s.split(' × 10^{'); return float(m) * 10 ** int(ex.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
ION = {1: 'H', 2: 'He^{+}', 3: 'Li^{2+}', 4: 'Be^{3+}'}
ORD = {1: 'ground state', 2: 'first excited state', 3: 'second excited state', 4: 'third excited state', 5: 'fourth excited state', 6: 'fifth excited state'}
SER = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund'}
def En(n, Z=1): return -13.6 * Z * Z / n ** 2

def g_bohr(rng):
    t = rng.choice(['E', 'r', 'ratio', 'L', 'ion', 'scale', 'KE', 'v'])
    if t == 'v':
        Z, n = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        v = 2.19e6 * Z / n; q = f'The speed of the electron of {ION[Z]} in orbit n = {n} is about (Bohr model; v_{{1}} for hydrogen = 2.19 × 10^{{6}} m/s) :'
        o, a = mcq(rng, f'{nf(v, 3)} m/s', [f'{nf(x, 3)} m/s' for x in (2.19e6 * Z * Z / n, 2.19e6 * Z / n ** 2, 2.19e6 / (Z * n), v * 2)])
        return dict(q=q, o=o, a=a, sol=['v = v_{1}\\f{Z}{n}.', f'= 2.19 × 10^{{6}} × \\f{{{Z}}}{{{n}}} ≈ {nf(v, 3)} m/s.'], p=dict(t='speed', Z=Z, n=n))
    if t == 'E':
        Z, n = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 5, 6])
        v = En(n, Z); q = f'The energy of the electron of {ION[Z]} in its {ORD[n]} is (Bohr model) :'
        o, a = mcq(rng, f'{nf(v, 3)} eV', [f'{nf(x, 3)} eV' for x in (-13.6 * Z / n ** 2, -13.6 * Z * Z / n, -13.6 / n ** 2, -v, v * 2)])
        return dict(q=q, o=o, a=a, sol=['E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV.', f'Z = {Z}, n = {n} → {nf(v, 3)} eV.'], p=dict(t=t, Z=Z, n=n))
    if t == 'r':
        Z, n = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 5])
        v = 0.529 * n * n / Z; q = f'The radius of the electron\'s orbit in {ION[Z]}, {ORD[n]}, is (a_{{0}} = 0.529 Å) :'
        o, a = mcq(rng, f'{nf(v, 3)} Å', [f'{nf(x, 3)} Å' for x in (0.529 * n / Z, 0.529 * n * n / Z ** 2, 0.529 * n * n * Z, v * 2)])
        return dict(q=q, o=o, a=a, sol=['r = a_{0}\\f{n^{2}}{Z}.', f'= 0.529 × \\f{{{n * n}}}{{{Z}}} ≈ {nf(v, 3)} Å.'], p=dict(t=t, Z=Z, n=n))
    if t == 'ratio':
        what = rng.choice(['radius', 'speed', 'energy', 'frequency of revolution', 'angular momentum', 'magnetic moment']); n1, n2 = rng.sample([1, 2, 3, 4, 5], 2)
        pw = {'radius': 2, 'speed': -1, 'energy': -2, 'frequency of revolution': -3, 'angular momentum': 1, 'magnetic moment': 1}[what]
        v = F(n1) ** pw / F(n2) ** pw
        q = f'For the hydrogen atom, the ratio of the {what} of the electron in orbit n = {n1} to that in n = {n2} is (magnitudes) :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (1 / v, F(n1, n2), F(n2, n1), v * v if v * v != v else v + 1, F(n1 * n1, n2 * n2) if pw != 2 else F(n1, n2) ** 3)])
        return dict(q=q, o=o, a=a, sol=['Bohr: r ∝ n^{2}, v ∝ \\f{1}{n}, E ∝ \\f{1}{n^{2}}, f ∝ \\f{1}{n^{3}}, L ∝ n, μ ∝ n.', f'{what} ∝ n^{{{pw}}} → {fr(v)}.'], p=dict(t=t, w=what, n1=n1, n2=n2))
    if t == 'L':
        n = rng.choice([1, 2, 3, 4, 5, 6, 7, 8]); form = rng.choice(['h/π', 'h/2π'])
        Ltxt = (f'\\f{{{n}h}}{{2π}}' if form == 'h/2π' else (f'\\f{{{F(n, 2).numerator}h}}{{{"π" if F(n, 2).denominator == 1 else "2π"}}}'))
        v = En(n); q = f'The angular momentum of the electron in a hydrogen atom is {Ltxt}. Its energy is :'
        o, a = mcq(rng, f'{nf(v, 3)} eV', [f'{nf(En(x), 3)} eV' for x in range(1, 10) if x != n][:5])
        return dict(q=q, o=o, a=a, sol=['L = \\f{nh}{2π} gives n.', f'n = {n} → E = −\\f{{13.6}}{{{n * n}}} ≈ {nf(v, 3)} eV.'], p=dict(t=t, n=n))
    if t == 'ion':
        Z1, n1 = rng.choice([(1, 1), (1, 2), (2, 2), (2, 4), (3, 3), (2, 1), (3, 6), (4, 4), (4, 2)]); cands = [(Z, n) for Z in (1, 2, 3, 4) for n in range(1, 9) if Z * n1 == Z1 * n and (Z, n) != (Z1, n1)]
        need(cands); Z2, n2 = rng.choice(cands)
        Zw = rng.choice([z for z in (1, 2, 3, 4) if z != Z2])
        q = f'Which state has the same energy as {ION[Z1]} in its {ORD.get(n1, f"level n = {n1}")} (Bohr model)?'
        right = f'{ION[Z2]}, n = {n2}'; wrong = [f'{ION[Zw]}, n = {n2}', f'{ION[Z2]}, n = {n2 + 1}', f'{ION[Z2]}, n = {max(1, n2 - 1) if n2 > 1 else n2 + 2}', f'{ION[Z1]}, n = {n1 + 1}']
        o, a = mcq(rng, right, wrong)
        return dict(q=q, o=o, a=a, sol=['E ∝ \\f{Z^{2}}{n^{2}} → equal when \\f{Z}{n} is equal.', f'{right}.'], p=dict(t=t, Z1=Z1, n1=n1))
    if t == 'scale':
        r0 = rng.choice([0.529, 2.116, 4.761, 8.464, 13.225]); E0 = rng.choice(['E', 'E_{1}'])
        n = round(math.sqrt(r0 / 0.529))
        q = f'An orbit of the hydrogen atom has radius {r0} Å (a_{{0}} = 0.529 Å). If the energy there is \\f{{{E0}}}{{x}} ({E0} = ground-state energy), x = ______'
        need(n > 1)
        return dict(q=q, o=None, a=n * n, sol=['r = n^{2}a_{0} → n.', f'n = {n} → E = \\f{{{E0}}}{{{n * n}}}.'], p=dict(t=t, r0=r0))
    n = rng.choice([1, 2, 3, 4, 5]); Z = rng.choice([1, 2, 3]); ask = rng.choice(['KE', 'PE'])
    v = -En(n, Z) if ask == 'KE' else 2 * En(n, Z)
    q = f'For {ION[Z]} in the {ORD[n]}, the {"kinetic" if ask == "KE" else "potential"} energy of the electron is :'
    o, a = mcq(rng, f'{nf(v, 3)} eV', [f'{nf(x, 3)} eV' for x in (En(n, Z), -v, v / 2, v * 2 if ask == 'KE' else -En(n, Z) * 2)])
    return dict(q=q, o=o, a=a, sol=['KE = −E, PE = 2E.', f'E = {nf(En(n, Z), 3)} eV → {nf(v, 3)} eV.'], p=dict(t='KE', n=n, Z=Z, ask=ask))

def g_spec(rng):
    t = rng.choice(['lam', 'ratio', 'lines', 'minE', 'limit', 'combine', 'recoil', 'ionE', 'ionE'])
    if t == 'ionE':
        Z, nl = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3]); nh_ = rng.choice([nl + 1, nl + 2, nl + 3, nl + 4])
        v = 13.6 * Z * Z * (1 / nl ** 2 - 1 / nh_ ** 2)
        q = f'The energy of the photon emitted when the electron of {ION[Z]} jumps from n = {nh_} to n = {nl} is about :'
        o, a = mcq(rng, f'{nf(v, 3)} eV', [f'{nf(x, 3)} eV' for x in (13.6 * Z * (1 / nl ** 2 - 1 / nh_ ** 2), 13.6 * (1 / nl ** 2 - 1 / nh_ ** 2) if Z > 1 else v * 4, 13.6 * Z * Z / nl ** 2, v / 2)])
        return dict(q=q, o=o, a=a, sol=['ΔE = 13.6Z^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}) eV.', f'≈ {nf(v, 3)} eV.'], p=dict(t='ionE', Z=Z, nl=nl, nh=nh_))
    if t == 'lam':
        nl = rng.choice([1, 2, 3, 4]); nh_ = rng.choice([x for x in range(nl + 1, nl + 5)]); Z = rng.choice([1, 1, 2, 3])
        RR = rng.choice([1.097e7, 1.1e7, 1.0973e7]); lam = 1 / (RR * Z * Z * (1 / nl ** 2 - 1 / nh_ ** 2))
        q = f'The wavelength of the photon emitted when the electron of {ION[Z]} drops from n = {nh_} to n = {nl} is (R = {nf(RR / 1e7, 5)} × 10^{{7}} m^{{−1}}) :'
        o, a = mcq(rng, f'{nf(lam * 1e9, 3)} nm', [f'{nf(x * 1e9, 3)} nm' for x in (lam * Z * Z if Z > 1 else lam * 2, 1 / (RR * (1 / nl - 1 / nh_)), lam / 2, lam * 1.5)])
        return dict(q=q, o=o, a=a, sol=['\\f{1}{λ} = RZ^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}).', f'λ ≈ {nf(lam * 1e9, 3)} nm.'], p=dict(t=t, nl=nl, nh=nh_, Z=Z, RR=RR))
    if t == 'ratio':
        s1, s2 = rng.sample([1, 2, 3, 4, 5], 2); w1, w2 = rng.choice(['longest', 'shortest']), rng.choice(['longest', 'shortest'])
        def L(s, w): return 1 / ((F(1, s * s) - F(1, (s + 1) ** 2)) if w == 'longest' else F(1, s * s))
        v = L(s1, w1) / L(s2, w2)
        q = f'For hydrogen, the {w1} wavelength of the {SER[s1]} series divided by the {w2} wavelength of the {SER[s2]} series is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (1 / v, L(s1, 'shortest' if w1 == 'longest' else 'longest') / L(s2, w2), L(s1, w1) / L(s2, 'shortest' if w2 == 'longest' else 'longest'), v * 2)])
        return dict(q=q, o=o, a=a, sol=['Longest = first line (n_{1} + 1 → n_{1}); shortest = series limit (∞ → n_{1}).', f'Ratio = {fr(v)}.'], p=dict(t=t, s1=s1, s2=s2, w1=w1, w2=w2))
    if t == 'lines':
        n = rng.choice([2, 3, 4, 5, 6, 7]); how = rng.choice(['n', 'E'])
        txt = f'in the n = {n} level' if how == 'n' else f'with energy {nf(En(n), 3)} eV'
        q = f'A hydrogen atom {txt} returns to the ground state. The maximum number of different spectral lines it can produce (many atoms) is ______.'
        return dict(q=q, o=None, a=n * (n - 1) // 2, sol=['Lines = \\f{n(n − 1)}{2}.', f'n = {n} → {n * (n - 1) // 2}.'], p=dict(t=t, n=n))
    if t == 'minE':
        s = rng.choice([1, 2, 3, 4, 5]); E_ = En(s + 1) - En(1)
        need(s > 1 or True)
        q = f'The minimum energy a ground-state hydrogen atom must absorb before it can emit a line of the {SER[s]} series is about :'
        o, a = mcq(rng, f'{nf(E_, 3)} eV', [f'{nf(x, 3)} eV' for x in (En(s + 1) - En(s), 13.6, -En(s + 1), E_ + 1)] )
        return dict(q=q, o=o, a=a, sol=[f'{SER[s]} lines end on n = {s}; the atom must reach at least n = {s + 1}.', f'E_{{{s + 1}}} − E_{{1}} ≈ {nf(E_, 3)} eV.'], p=dict(t=t, s=s))
    if t == 'limit':
        L0 = rng.choice([91, 91.2, 912, 915, 910]); unit = 'nm' if L0 < 100 else 'Å'; s = rng.choice([2, 3]); w = rng.choice(['longest', 'shortest'])
        v = L0 * float(1 / ((F(1, s * s) - F(1, (s + 1) ** 2)) if w == 'longest' else F(1, s * s)))
        q = f'The shortest wavelength of the Lyman series is {L0} {unit}. The {w} wavelength of the {SER[s]} series is about :'
        o, a = mcq(rng, f'{nf(v, 4)} {unit}', [f'{nf(x, 4)} {unit}' for x in (v * 2, v / 2, L0 * s * s * 2, v * 1.25)])
        return dict(q=q, o=o, a=a, sol=['Lyman limit = \\f{1}{R}.', f'{SER[s]} {w}: ≈ {nf(v, 4)} {unit}.'], p=dict(t=t, L0=L0, s=s, w=w))
    if t == 'combine':
        a_, b_ = rng.choice([(2000, 6000), (1000, 3000), (1500, 3000), (3000, 6000), (1200, 2400), (4000, 12000), (2000, 3000)])
        v = 1 / (1 / a_ - 1 / b_); need(abs(v - round(v)) < 1e-6)
        q = f'An electron jumping A → C emits {a_} Å; jumping B → C it emits {b_} Å. The wavelength for A → B is ______ Å.'
        return dict(q=q, o=None, a=round(v), sol=['Photon energies add: \\f{1}{λ_{AB}} = \\f{1}{λ_{AC}} − \\f{1}{λ_{BC}}.', f'λ_{{AB}} = {round(v)} Å.'], p=dict(t=t, a=a_, b=b_))
    n2, n1 = rng.choice([(2, 1), (3, 1), (3, 2), (4, 1), (4, 2)]); M = 1.67e-27
    Eph = (En(n1) - En(n2)) * -1 * e; v = Eph / (M * c)
    q = f'A hydrogen atom (mass 1.67 × 10^{{−27}} kg) at rest emits a photon going from n = {n2} to n = {n1}. Its recoil speed is about :'
    o, a = mcq(rng, f'{nf(v, 3)} m/s', [f'{nf(x, 3)} m/s' for x in (v * 2, v / 2, v * 10, math.sqrt(2 * Eph / M) / 1000)])
    return dict(q=q, o=o, a=a, sol=['Momentum: \\f{E}{c} = Mv.', f'E = {nf(Eph / e, 3)} eV → v ≈ {nf(v, 3)} m/s.'], p=dict(t='recoil', n1=n1, n2=n2))

NUC = [('He', 4, 2, 4.002603), ('Li', 7, 3, 7.016003), ('C', 12, 6, 12.0), ('N', 14, 7, 14.003074), ('O', 16, 8, 15.994915), ('Fe', 56, 26, 55.934937), ('Cu', 63, 29, 62.929598), ('Ag', 107, 47, 106.905097), ('U', 238, 92, 238.050788)]
MH, MN = 1.007825, 1.008665
def g_nuc(rng):
    t = rng.choice(['R', 'A', 'BE', 'dm', 'dens', 'iso'])
    if t == 'R':
        A1, A2 = rng.choice([(8, 64), (27, 125), (1, 8), (64, 216), (27, 64), (8, 27), (64, 125), (1, 27), (125, 216), (16, 128)]); R1 = rng.choice([1.2, 1.4, 2, 2.4, 3, 3.6, 4.8])
        R2 = R1 * (A2 / A1) ** (1 / 3)
        q = f'A nucleus of mass number {A1} has radius {R1} fm. The radius of a nucleus of mass number {A2} is :'
        o, a = mcq(rng, f'{nf(R2, 3)} fm', [f'{nf(x, 3)} fm' for x in (R1 * A2 / A1, R1 * (A2 / A1) ** 0.5, R1 * (A2 / A1) ** (2 / 3), R2 * 1.5)])
        return dict(q=q, o=o, a=a, sol=['R = R_{0}A^{1/3}.', f'R = {R1} × ({A2}/{A1})^{{1/3}} ≈ {nf(R2, 3)} fm.'], p=dict(t=t, A1=A1, A2=A2, R1=R1))
    if t == 'A':
        A1 = rng.choice([8, 27, 64, 125, 192, 216, 81, 24]); f = rng.choice([F(1, 2), 2, F(2, 3), F(3, 2), F(1, 3)])
        A2 = A1 * f ** 3; need(A2.denominator == 1 and 1 <= A2 <= 300)
        q = f'The mass number of a nucleus whose radius is {fr(f)} times that of a nucleus with A = {A1} is ______.'
        return dict(q=q, o=None, a=int(A2), sol=['A ∝ R^{3}.', f'A = {A1} × ({fr(f)})^{{3}} = {A2}.'], p=dict(t=t, A1=A1, f=float(f)))
    if t in ('BE', 'dm'):
        nm, A, Z, m = rng.choice(NUC[1:]); dm = Z * MH + (A - Z) * MN - m; BE = dm * 931.5
        if t == 'dm':
            q = f'^{{{A}}}_{{{Z}}}{nm} has atomic mass {m} u (m_{{H}} = {MH} u, m_{{n}} = {MN} u, 1 u = 931.5 MeV). Its total binding energy is about :'
            o, a = mcq(rng, f'{nf(BE, 4)} MeV', [f'{nf(x, 4)} MeV' for x in (BE / A, BE * 2, dm * 931.5 / Z, BE * 0.9)])
        else:
            q = f'^{{{A}}}_{{{Z}}}{nm} has atomic mass {m} u (m_{{H}} = {MH} u, m_{{n}} = {MN} u, 1 u = 931.5 MeV). Its binding energy per nucleon is about :'
            o, a = mcq(rng, f'{nf(BE / A, 3)} MeV', [f'{nf(x, 3)} MeV' for x in (BE, BE / Z, BE / A * 1.1, BE / (A - Z))])
        return dict(q=q, o=o, a=a, sol=['Δm = Zm_{H} + (A − Z)m_{n} − M_{atom} (electron masses cancel).', f'Δm ≈ {nf(dm, 4)} u → BE ≈ {nf(BE, 4)} MeV, per nucleon ≈ {nf(BE / A, 3)} MeV.'], p=dict(t=t, n=nm))
    if t == 'dens':
        A1, A2 = rng.sample([4, 12, 27, 56, 64, 107, 197, 238], 2); what = rng.choice(['density', 'volume'])
        v = F(1) if what == 'density' else F(A2, A1)
        q = f'The ratio of nuclear {what} of a nucleus with A = {A2} to one with A = {A1} is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(A2, A1) if what == 'density' else F(1), F(A2, A1) ** 2, F(A1, A2), F(A2 * A2, A1 * A1) if what == 'density' else F(A2, A1) ** 3)])
        return dict(q=q, o=o, a=a, sol=['R ∝ A^{1/3} → volume ∝ A, density independent of A.', f'{what}: {fr(v)}.'], p=dict(t=t, A1=A1, A2=A2, w=what))
    pairs = [('isotopes', (1, 2, 1, 3)), ('isobars', (3, 1, 3, 2)), ('isotones', (13, 6, 14, 7))]
    kind, _ = rng.choice(pairs)
    gen = {'isotopes': lambda: (lambda Z, A: (A, Z, A + rng.choice([1, 2, 3]), Z))(rng.choice([6, 8, 17, 26, 92]), rng.choice([12, 16, 35, 56, 235])),
           'isobars': lambda: (lambda Z, A: (A, Z, A, Z + rng.choice([1, 2])))(rng.choice([1, 6, 18, 19, 20]), rng.choice([3, 14, 40, 60])),
           'isotones': lambda: (lambda Z, A: (A, Z, A + 1, Z + 1))(rng.choice([6, 7, 15, 79]), rng.choice([13, 14, 31, 197]))}
    right = gen[kind](); others = [gen[x]() for x in ('isotopes', 'isobars', 'isotones') if x != kind]
    def s(p): return f'^{{{p[0]}}}_{{{p[1]}}}X and ^{{{p[2]}}}_{{{p[3]}}}Y'
    extra = (right[0] + 1, right[1] + 1, right[2] + 3, right[3] + 2)
    o, a = mcq(rng, s(right), [s(x) for x in others] + [s(extra)])
    return dict(q=f'Which pair are {kind}?', o=o, a=a, sol=['Isotopes: same Z. Isobars: same A. Isotones: same N = A − Z.', s(right) + '.'], p=dict(t='iso', kind=kind))

def g_react(rng):
    t = rng.choice(['beQ', 'fission', 'massQ', 'count', 'alpha', 'split', 'energy', 'beGen', 'beGen'])
    if t == 'beGen':
        A1, A2 = rng.choice([(2, 2), (3, 1), (2, 3), (3, 3), (6, 2), (7, 1), (4, 4), (3, 4), (6, 4)]); A3 = A1 + A2
        bs = {1: 0, 2: rng.choice([1.1, 1.12]), 3: rng.choice([2.6, 2.8, 5.6]), 4: rng.choice([7.0, 7.07, 7.4]), 6: rng.choice([5.3, 5.33]), 7: rng.choice([5.6, 5.61])}
        b3 = rng.choice([5.6, 6.1, 6.5, 7.0, 7.07, 7.2, 7.5, 7.68, 8.0]); Q = A3 * b3 - (A1 * bs[A1] + A2 * bs[A2])
        need(abs(Q) > 0.05)
        q = f'Nuclei with A = {A1} (BE/A = {bs[A1]} MeV) and A = {A2} (BE/A = {bs[A2]} MeV) fuse into one nucleus with A = {A3} and BE/A = {b3} MeV. |Q| for the reaction is about :'.replace('(BE/A = 0 MeV)', '(a single nucleon, BE = 0)')
        o, a = mcq(rng, f'{nf(abs(Q), 3)} MeV', [f'{nf(x, 3)} MeV' for x in (abs(b3 - bs[A1] - bs[A2]), A3 * b3, abs(Q) + 2, abs(Q) * 2)])
        return dict(q=q, o=o, a=a, sol=['Q = BE(product) − ΣBE(reactants), with BE = A × (BE/A).', f'= {A3} × {b3} − ({A1} × {bs[A1]} + {A2} × {bs[A2]}) = {nf(Q, 3)} MeV.'], p=dict(t='beGen', A=(A1, A2, A3), b=(bs[A1], bs[A2], b3)))
    if t == 'speed': return close(num(Rv), orbit(p['n'], p['Z'])['v'], 0.01)
    if t == 'ionE': return close(num(Rv), orbit(p['nh'], p['Z'])['E'] - orbit(p['nl'], p['Z'])['E'], 0.01)
    if t == 'beGen':
        (A1, A2, A3), (b1, b2, b3) = p['A'], p['b']; before = A1 * b1 + A2 * b2; after = A3 * b3; return close(num(Rv), abs(after - before), 0.006)
    if t == 'beQ':
        b1, b2 = rng.choice([1.1, 1.2, 2.8, 2.6]), rng.choice([7.0, 7.1, 7.2, 7.4]); kind = rng.choice([('^{2}H', 2, 2), ('^{3}He', 3, 0)])
        Q = 4 * b2 - 2 * 2 * b1
        q = f'Two deuterons (^{{2}}H, BE/A = {b1} MeV) fuse into ^{{4}}He (BE/A = {b2} MeV). Energy released is about :'
        o, a = mcq(rng, f'{nf(Q, 3)} MeV', [f'{nf(x, 3)} MeV' for x in (b2 - b1, 4 * b2 - 2 * b1, 4 * b2, Q + 2)])
        return dict(q=q, o=o, a=a, sol=['Q = Σ BE(products) − Σ BE(reactants).', f'= 4 × {b2} − 2 × 2 × {b1} = {nf(Q, 3)} MeV.'], p=dict(t=t, b1=b1, b2=b2))
    if t == 'fission':
        A = rng.choice([200, 220, 236, 240]); b1, b2 = rng.choice([(7.6, 8.5), (7.6, 8.6), (7.5, 8.4), (7.4, 8.3), (7.8, 8.6)])
        Q = A * (b2 - b1)
        q = f'A nucleus with A = {A} and BE/A = {b1} MeV splits into two equal fragments with BE/A = {b2} MeV. Energy released ≈ ______ MeV.'
        need(abs(Q - round(Q)) < 1e-9)
        return dict(q=q, o=None, a=round(Q), sol=['Q = A(b_{2} − b_{1}) (nucleon number conserved).', f'= {A} × {nf(b2 - b1, 2)} = {round(Q)} MeV.'], p=dict(t=t, A=A, b1=b1, b2=b2))
    if t == 'massQ':
        mi, mf = rng.choice([(3 * 4.002603, 12.0), (2 * 2.014102, 4.002603), (2.014102 + 3.016049, 4.002603 + 1.008665), (7.016003 + 1.007825, 2 * 4.002603)])
        Q = (mi - mf) * 931.5
        q = f'In a nuclear reaction the total mass of the reactants is {nf(mi, 7)} u and of the products {nf(mf, 7)} u. Energy released (1 u = 931.5 MeV) is about :'
        o, a = mcq(rng, f'{nf(Q, 3)} MeV', [f'{nf(x, 3)} MeV' for x in (Q * 10, Q / 2, (mi - mf) * 931.5 * 2, Q + 1)])
        return dict(q=q, o=o, a=a, sol=['Q = Δm × 931.5 MeV.', f'Δm = {nf(mi - mf, 4)} u → {nf(Q, 3)} MeV.'], p=dict(t=t, mi=mi, mf=mf))
    if t == 'count':
        m = rng.choice([47, 94, 117.5, 235, 470]); Ef = rng.choice([190, 200, 210])
        v = m / 235 * 6e23 * Ef / 1e23; need(abs(v - round(v)) < 1e-6)
        q = f'Each fission of ^{{235}}U releases {Ef} MeV. Fission of all atoms in {nf(m)} g of ^{{235}}U releases α × 10^{{23}} MeV (N_{{A}} = 6 × 10^{{23}}). α = ______'
        return dict(q=q, o=None, a=round(v), sol=['N = \\f{m}{235}N_{A}.', f'E = {nf(m / 235 * 6)} × 10^{{23}} × {Ef} = {round(v)} × 10^{{23}} MeV.'], p=dict(t=t, m=m, Ef=Ef))
    if t == 'alpha':
        A = rng.choice([200, 210, 212, 220, 226, 238]); Q = rng.choice([4, 4.8, 5, 5.5, 6, 6.5, 7])
        Ka = Q * (A - 4) / A
        q = f'A nucleus of mass number {A} at rest undergoes α-decay with Q = {Q} MeV. The kinetic energy of the α-particle is about :'
        o, a = mcq(rng, f'{nf(Ka, 4)} MeV', [f'{nf(x, 4)} MeV' for x in (Q, Q * 4 / A, Q / 2, Q * A / (A + 4))])
        return dict(q=q, o=o, a=a, sol=['Equal and opposite momenta → K_{α} = Q\\f{A − 4}{A}.', f'≈ {nf(Ka, 4)} MeV.'], p=dict(t=t, A=A, Q=Q))
    if t == 'split':
        r1, r2 = rng.choice([(2, 1), (3, 1), (3, 2), (4, 1), (5, 3)]); what = rng.choice(['speeds', 'kinetic energies', 'momenta'])
        v = {'speeds': F(r2, r1), 'kinetic energies': F(r2, r1), 'momenta': F(1)}[what]
        q = f'A nucleus at rest splits into two pieces with masses in the ratio {r1} : {r2}. The ratio of their {what} (first : second) is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(r1, r2), F(r1 * r1, r2 * r2), F(r2 * r2, r1 * r1), F(1) if v != 1 else F(r1, r2) + 1)])
        return dict(q=q, o=o, a=a, sol=['Momentum is conserved: equal and opposite p.', 'v ∝ \\f{1}{m}; K = \\f{p^{2}}{2m} ∝ \\f{1}{m}.'], p=dict(t=t, r1=r1, r2=r2, w=what))
    dm = rng.choice([0.1, 0.2, 0.4, 0.5, 1, 2, 4]); unit = rng.choice(['g', 'mg'])
    Ej = dm * (1e-3 if unit == 'g' else 1e-6) * 9e16
    q = f'A mass of {nf(dm)} {unit} is completely converted into energy. The energy released is about :'
    o, a = mcq(rng, f'{nf(Ej, 3)} J', [f'{nf(x, 3)} J' for x in (Ej / 3e8, Ej * 1000, Ej / 1000, Ej * 3)])
    return dict(q=q, o=o, a=a, sol=['E = mc^{2}.', f'= {nf(dm)} × 10^{{{-3 if unit == "g" else -6}}} × 9 × 10^{{16}} ≈ {nf(Ej, 3)} J.'], p=dict(t='energy', dm=dm, unit=unit))

def g_decay(rng):
    t = rng.choice(['frac', 'ratio', 'mean', 'activity'])
    if t == 'frac':
        n = rng.choice([1, 2, 3, 4, 5, 6]); T = rng.choice([2, 3, 5, 8, 10, 12, 20]); what = rng.choice(['left', 'decayed'])
        v = F(1, 2 ** n) if what == 'left' else 1 - F(1, 2 ** n)
        q = f'A radioactive sample has half-life {T} days. After {n * T} days the fraction {"remaining" if what == "left" else "that has decayed"} is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(1, 2 ** (n + 1)), F(1, 2 ** max(1, n - 1)) if n > 1 else F(3, 4), 1 - v, F(1, n + 1))])
        return dict(q=q, o=o, a=a, sol=['N = N_{0}(\\f{1}{2})^{t/T}.', f'{n} half-lives → {fr(F(1, 2 ** n))} remains.'], p=dict(t=t, n=n, T=T, w=what))
    if t == 'ratio':
        kk = rng.choice([2, 3, 4]); nh = rng.choice([1, 2])
        v = F(1, 2 ** ((kk - 1) * nh))
        q = f'Nucleus B has {kk} times the decay constant of nucleus A; both start with equal numbers. After {nh} half-life(s) of A, N_{{B}} : N_{{A}} is :'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(1, 2 ** (kk * nh)), F(1, kk), 1 / v, F(1, 2 ** nh))])
        return dict(q=q, o=o, a=a, sol=['N = N_{0}e^{−λt}; t = nT_{A} = \\f{n ln 2}{λ}.', f'\\f{{N_{{B}}}}{{N_{{A}}}} = e^{{−({kk} − 1)n ln 2}} = {fr(v)}.'], p=dict(t=t, k=kk, nh=nh))
    if t == 'mean':
        T = rng.choice([1, 2, 5, 6.93, 10, 13.86, 20, 69.3])
        tau = T / math.log(2)
        q = f'A nuclide has half-life {nf(T)} s. Its mean life is about :'
        o, a = mcq(rng, f'{nf(tau, 3)} s', [f'{nf(x, 3)} s' for x in (T * math.log(2), T / 2, T * 2, T)])
        return dict(q=q, o=o, a=a, sol=['τ = \\f{1}{λ} = \\f{T_{1/2}}{ln 2}.', f'≈ {nf(tau, 3)} s.'], p=dict(t=t, T=T))
    A0 = rng.choice([800, 1600, 3200, 6400, 1000, 4000]); n = rng.choice([1, 2, 3, 4]); T = rng.choice([5, 10, 15, 30])
    v = A0 / 2 ** n; need(v == int(v))
    q = f'A source has activity {A0} Bq. Its half-life is {T} min. After {n * T} min the activity is ______ Bq.'
    return dict(q=q, o=None, a=int(v), sol=['Activity halves every half-life.', f'{A0} / 2^{{{n}}} = {int(v)} Bq.'], p=dict(t='act', A0=A0, n=n))

def g_ruth(rng):
    t = rng.choice(['r0', 'v', 'db', 'dbK'])
    if t == 'r0':
        K = rng.choice([4, 5, 5.5, 6, 7.7, 7.9, 8, 10]); Z = rng.choice([29, 47, 50, 79, 80, 82])
        r0 = k * 2 * Z * e / (K * 1e6)
        q = f'An α-particle of {K} MeV approaches a nucleus of atomic number {Z} head-on. Its distance of closest approach is about :'
        o, a = mcq(rng, f'{nf(r0, 3)} m', [f'{nf(x, 3)} m' for x in (r0 / 2, r0 * 2, r0 * 100, r0 / 10)])
        return dict(q=q, o=o, a=a, sol=['K = \\f{k(2e)(Ze)}{r_{0}}.', f'r_{{0}} = \\f{{9 × 10^{{9}} × {2 * Z} × 1.6 × 10^{{−19}}}}{{{K} × 10^{{6}}}} ≈ {nf(r0, 3)} m.'], p=dict(t=t, K=K, Z=Z))
    if t == 'v':
        r0 = rng.choice([2, 3, 4.5, 5, 6]) * 1e-14; Z = rng.choice([50, 79, 80]); m = 6.64e-27
        v = math.sqrt(2 * k * 2 * Z * e * e / (r0 * m))
        q = f'In α scattering from a nucleus with Z = {Z}, the closest approach is {nf(r0)} m (m_{{α}} = 6.64 × 10^{{−27}} kg). The initial speed of the α-particle is about :'
        o, a = mcq(rng, f'{nf(v, 3)} m/s', [f'{nf(x, 3)} m/s' for x in (v * math.sqrt(2), v / 2, v * 2, v / math.sqrt(2))])
        return dict(q=q, o=o, a=a, sol=['½mv^{2} = \\f{k(2e)(Ze)}{r_{0}}.', f'v ≈ {nf(v, 3)} m/s.'], p=dict(t=t, r0=r0, Z=Z, m=m))
    if t == 'db':
        ps = rng.sample([('electron', 1), ('proton', 1836), ('α-particle', 4 * 1836), ('deuteron', 2 * 1836)], 3)
        order = sorted(ps, key=lambda x: -x[1])
        right = ' < '.join(f'λ_{{{n}}}' for n, _ in order)
        perms = set()
        while len(perms) < 4:
            p_ = rng.sample(ps, 3); s = ' < '.join(f'λ_{{{n}}}' for n, _ in p_)
            if s != right: perms.add(s)
        q = 'A ' + ', a '.join(n for n, _ in ps) + ' all have the same kinetic energy. Their de Broglie wavelengths satisfy :'
        o, a = mcq(rng, right, sorted(perms))
        return dict(q=q, o=o, a=a, sol=['λ = \\f{h}{√{2mK}} → same K: λ ∝ \\f{1}{√{m}}.', right + '.'], p=dict(t=t, ps=ps))
    (n1, m1), (n2, m2) = rng.sample([('proton', 1), ('deuteron', 2), ('α-particle', 4), ('triton', 3)], 2); K1, K2 = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4])
    v = math.sqrt(m2 * K2 / (m1 * K1))
    q = f'The ratio of the de Broglie wavelength of a {n1} with kinetic energy {K1}E to that of a{"n" if n2[0] in "aeiouα" else ""} {n2} with kinetic energy {K2}E is (m_{{p}} = m_{{n}}) :'
    o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (1 / v, v * v, v * 2, math.sqrt(m2 / m1))])
    return dict(q=q, o=o, a=a, sol=['λ ∝ \\f{1}{√{mK}}.', f'= √{{\\f{{{m2} × {K2}}}{{{m1} × {K1}}}}} ≈ {nf(v, 3)}.'], p=dict(t='dbK', m1=m1, m2=m2, K1=K1, K2=K2))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, StopIteration): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k_: robust(v) for k_, v in dict(bohr=g_bohr, spec=g_spec, nuc=g_nuc, react=g_react, decay=g_decay, ruth=g_ruth).items()}
def finish(it): return it

# ---------------- independent: Bohr orbit from force balance + quantisation (SI) ----------------
def orbit(n, Z=1):
    r = eps0 * h * h * n * n / (math.pi * me * Z * e * e); v = Z * e * e / (2 * eps0 * h * n)
    KE = 0.5 * me * v * v; PE = -k * Z * e * e / r
    return dict(r=r, v=v, KE=KE / e, PE=PE / e, E=(KE + PE) / e, L=me * v * r, f=v / (2 * math.pi * r), mu=e * v * r / 2)
def unf(s):
    s = s.replace('−', '-').strip(); neg = s.startswith('-'); s = s.lstrip('-')
    if s.startswith('\\f{'): a, b = s[3:-1].split('}{'); v = F(int(a), int(b))
    else: v = F(s)
    return -v if neg else v
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'E': return close(num(Rv), orbit(p['n'], p['Z'])['E'], 0.01)
    if t == 'r': return close(num(Rv), orbit(p['n'], p['Z'])['r'] * 1e10, 0.01)
    if t == 'ratio':
        key = {'radius': 'r', 'speed': 'v', 'energy': 'E', 'frequency of revolution': 'f', 'angular momentum': 'L', 'magnetic moment': 'mu'}[p['w']]
        return close(float(unf(Rv)), abs(orbit(p['n1'])[key] / orbit(p['n2'])[key]), 1e-6)
    if t == 'L': return close(num(Rv), orbit(p['n'])['E'], 0.01)
    if t == 'ion':
        z, n = Rv.split(', n = '); Z = next(k_ for k_, v in ION.items() if v == z); return close(orbit(int(n), Z)['E'], orbit(p['n1'], p['Z1'])['E'], 1e-9)
    if t == 'scale': n = round(math.sqrt(p['r0'] / (orbit(1)['r'] * 1e10))); return close(orbit(n)['E'] * Rv, orbit(1)['E'], 1e-6)
    if t == 'KE': o_ = orbit(p['n'], p['Z']); return close(num(Rv), o_['KE'] if p['ask'] == 'KE' else o_['PE'], 0.01)
    if t == 'lam':
        dE = (orbit(p['nh'], p['Z'])['E'] - orbit(p['nl'], p['Z'])['E']) * e; return close(num(Rv), h * c / dE * 1e9 * 1.097e7 / p['RR'], 0.02)
    if t == 'ratio2' or (t == 'ratio' and 's1' in p): pass
    if t == 'lines': return Rv == len({(a, b) for a in range(1, p['n'] + 1) for b in range(1, a)})
    if t == 'minE': return close(num(Rv), orbit(p['s'] + 1)['E'] - orbit(1)['E'], 0.01)
    if t == 'limit':
        s, w = p['s'], p['w']; Elim = -orbit(1)['E']; dE = (-orbit(s)['E'] if w == 'shortest' else orbit(s + 1)['E'] - orbit(s)['E']); return close(num(Rv), p['L0'] * Elim / dE, 0.01)
    if t == 'combine': return abs(Rv - round(1 / (1 / p['a'] - 1 / p['b']))) == 0 and abs(h * c / (Rv * 1e-10) - (h * c / (p['a'] * 1e-10) - h * c / (p['b'] * 1e-10))) < 1e-25
    if t == 'recoil':
        Ep = (orbit(p['n2'])['E'] - orbit(p['n1'])['E']) * e; return close(num(Rv), Ep / c / 1.67e-27, 0.02)
    if t == 'R': return close(num(Rv), p['R1'] * (p['A2'] / p['A1']) ** (1 / 3))
    if t == 'A': return abs(Rv - p['A1'] * p['f'] ** 3) < 1e-6
    if t in ('BE', 'dm'):
        nm, A, Z, m = next(x for x in NUC if x[0] == p['n']); dm = Z * (1.007276 + 0.000549) + (A - Z) * MN - m; BE = dm * 931.5
        return close(num(Rv), BE if t == 'dm' else BE / A, 0.01)
    if t == 'dens':
        def vol(A): return 4 / 3 * math.pi * (1.2e-15 * A ** (1 / 3)) ** 3
        v = (p['A2'] / vol(p['A2'])) / (p['A1'] / vol(p['A1'])) if p['w'] == 'density' else vol(p['A2']) / vol(p['A1']); return close(float(unf(Rv)), v, 1e-6)
    if t == 'iso':
        import re
        A1, Z1, A2, Z2 = map(int, re.findall(r'\^\{(\d+)\}_\{(\d+)\}', Rv)[0] + re.findall(r'\^\{(\d+)\}_\{(\d+)\}', Rv)[1])
        return {'isotopes': Z1 == Z2 and A1 != A2, 'isobars': A1 == A2 and Z1 != Z2, 'isotones': A1 - Z1 == A2 - Z2 and A1 != A2}[p['kind']]
    if t == 'speed': return close(num(Rv), orbit(p['n'], p['Z'])['v'], 0.01)
    if t == 'ionE': return close(num(Rv), orbit(p['nh'], p['Z'])['E'] - orbit(p['nl'], p['Z'])['E'], 0.01)
    if t == 'beGen':
        (A1, A2, A3), (b1, b2, b3) = p['A'], p['b']; before = A1 * b1 + A2 * b2; after = A3 * b3; return close(num(Rv), abs(after - before), 0.006)
    if t == 'beQ': return close(num(Rv), 4 * p['b2'] - 4 * p['b1'], 0.01)
    if t == 'fission': return abs(Rv - (2 * (p['A'] / 2) * p['b2'] - p['A'] * p['b1'])) < 1e-6
    if t == 'massQ': return close(num(Rv), (p['mi'] - p['mf']) * 1.66054e-27 * c * c / 1.602e-13, 0.01)
    if t == 'count': return abs(Rv - p['m'] / 235 * 6e23 * p['Ef'] / 1e23) < 1e-6
    if t == 'alpha':   # momentum balance numerically: p_α = p_d, K_α + K_d = Q
        Ka = None; lo, hi = 0.0, p['Q']
        for _ in range(100):
            m_ = (lo + hi) / 2; pa = math.sqrt(2 * 4 * m_); Kd = pa * pa / (2 * (p['A'] - 4))
            if m_ + Kd > p['Q']: hi = m_
            else: lo = m_
        return close(num(Rv), lo, 0.002)
    if t == 'split':
        m1, m2 = p['r1'], p['r2']; v1, v2 = 1 / m1, 1 / m2; vals = {'speeds': v1 / v2, 'kinetic energies': (m1 * v1 * v1) / (m2 * v2 * v2), 'momenta': (m1 * v1) / (m2 * v2)}
        return close(float(unf(Rv)), vals[p['w']], 1e-9)
    if t == 'energy': return close(num(Rv), p['dm'] * (1e-3 if p['unit'] == 'g' else 1e-6) * c * c)
    if t == 'frac':
        N, lam, dt = 1.0, math.log(2) / p['T'], p['T'] / 4000
        for _ in range(4000 * p['n']): N -= lam * N * dt
        v = N if p['w'] == 'left' else 1 - N; return close(float(unf(Rv)), v, 0.002)
    if t == 'ratio' and 'k' in p: pass
    if t == 'mean':
        lam = math.log(2) / p['T']; N = 4000; T_ = 20 / lam; tm = sum((i + .5) * T_ / N * lam * math.exp(-lam * (i + .5) * T_ / N) * T_ / N for i in range(N)); return close(num(Rv), tm, 0.01)
    if t == 'act': return Rv == p['A0'] * 0.5 ** p['n']
    if t == 'r0':   # march the α in until it stops
        r = 1e-10; K = p['K'] * 1e6 * e; U = lambda x: k * 2 * p['Z'] * e * e / x
        lo, hi = 1e-16, 1e-10
        for _ in range(200):
            m_ = (lo + hi) / 2
            if U(m_) > K: lo = m_
            else: hi = m_
        return close(num(Rv), lo, 0.01)
    if t == 'v': return close(num(Rv), math.sqrt(2 * (k * 2 * p['Z'] * e * e / p['r0']) / p['m']), 0.01)
    if t == 'db':
        ms = dict((n, m) for n, m in p['ps']); order = [x.strip()[3:-1] for x in Rv.split('<')]; lam = [1 / math.sqrt(ms[n]) for n in order]; return lam == sorted(lam)
    if t == 'dbK': return close(num(Rv), math.sqrt(p['m2'] * p['K2'] / (p['m1'] * p['K1'])), 0.01)
    raise KeyError(t)

_check = check
def check(it):   # route the two 'ratio' kinds
    p = it['p']
    if p['t'] == 'ratio' and 's1' in p:
        Rv = it['o'][it['a']]
        def L(s, w): return h * c / (((orbit(s + 1)['E'] - orbit(s)['E']) if w == 'longest' else -orbit(s)['E']) * e)
        return close(float(unf(Rv)), L(p['s1'], p['w1']) / L(p['s2'], p['w2']), 1e-6)
    if p['t'] == 'ratio' and 'k' in p:
        Rv = it['o'][it['a']]; lA = math.log(2); tA = p['nh'] * math.log(2) / lA; return close(float(unf(Rv)), math.exp(-p['k'] * lA * tA) / math.exp(-lA * tA), 1e-9)
    return _check(it)
