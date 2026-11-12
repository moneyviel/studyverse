"""Practice generators — Physics Unit 15: Electromagnetic Waves. check() re-solves each item another way: field
directions from the Poynting vector E × B, magnitudes from μ0 and ε0 numbers, spectrum bands from a wavelength table."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
c, e0, mu0 = 3e8, 8.85e-12, 4e-7 * math.pi
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
AX = {'î': (1, 0, 0), 'ĵ': (0, 1, 0), 'k̂': (0, 0, 1)}
def vec(s): neg = s.startswith('−'); v = AX[s.lstrip('−')]; return tuple(-x for x in v) if neg else v
def name(v):
    for k, a in AX.items():
        if a == v: return k
        if tuple(-x for x in a) == v: return '−' + k
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
BANDS = [('gamma rays', 1e-14, 1e-11), ('X-rays', 1e-11, 1e-8), ('ultraviolet', 1e-8, 4e-7), ('visible light', 4e-7, 7e-7), ('infrared', 7e-7, 1e-3), ('microwaves', 1e-3, 0.3), ('radio waves', 0.3, 1e5)]
TYP = {'gamma rays': 1e-12, 'X-rays': 1e-10, 'ultraviolet': 1e-7, 'visible light': 5.5e-7, 'infrared': 1e-5, 'microwaves': 1e-2, 'radio waves': 10}

def g_eb(rng):
    t = rng.choice(['dir', 'dir', 'lam', 'mag', 'speed', 'wk'])
    if t == 'dir':
        k = rng.choice(['î', 'ĵ', 'k̂', '−î', '−ĵ', '−k̂']); E = rng.choice([a for a in ('î', 'ĵ', 'k̂', '−î', '−ĵ', '−k̂') if vec(a) != vec(k) and vec(a) != tuple(-x for x in vec(k))])
        ask = rng.choice(['B', 'E']); E0 = rng.choice([3, 6, 9, 12, 15, 24, 30, 45, 60, 90, 120, 150, 300, 600]); B0 = E0 / c
        Bv = name(cross(vec(k), vec(E)))
        if ask == 'B':
            q = f'An EM wave travels along {k.replace("−", "−")} in free space. At some instant the electric field at a point is {E0} {E} V/m. The magnetic field there is :'
            right = f'{nf(B0)} {Bv} T'; wrong = [f'{nf(B0)} {x} T' for x in ('î', 'ĵ', 'k̂', '−î', '−ĵ', '−k̂') if x != Bv] + [f'{E0} {Bv} T', f'{nf(B0 * 3)} {Bv} T']
            o, a = mcq(rng, right, wrong[:2] + wrong[-2:] + wrong[2:4])
            return dict(q=q, o=o, a=a, sol=['B = \\f{E}{c}; \\vec{E} × \\vec{B} points along the travel direction → B̂ = k̂_{travel} × Ê.', f'B̂ = {Bv}, |B| = {nf(B0)} T.'], p=dict(t=t, k=k, E=E, ask=ask, E0=E0))
        q = f'An EM wave travels along {k} in free space. At some instant the magnetic field at a point is {nf(B0)} {Bv} T. The electric field there is :'
        right = f'{E0} {E} V/m'; wrong = [f'{E0} {x} V/m' for x in ('î', 'ĵ', 'k̂', '−î', '−ĵ', '−k̂') if x != E] + [f'{nf(B0)} {E} V/m', f'{E0 * 3} {E} V/m']
        o, a = mcq(rng, right, wrong[:2] + wrong[-2:] + wrong[2:4])
        return dict(q=q, o=o, a=a, sol=['E = cB; Ê = B̂ × k̂_{travel}.', f'\\vec{{E}} = {E0} {E} V/m.'], p=dict(t=t, k=k, E=E, ask=ask, E0=E0, B=Bv))
    if t == 'lam':
        f = rng.choice([1, 2, 3, 5, 6, 10, 15, 20, 30, 50, 60, 75, 100, 150, 300, 600]); unit = rng.choice(['MHz', 'GHz'])
        lam = c / (f * (1e6 if unit == 'MHz' else 1e9))
        q = f'An EM wave of frequency {f} {unit} travels in vacuum. Its wavelength is :'
        o, a = mcq(rng, f'{nf(lam, 3)} m', [f'{nf(lam * k, 3)} m' for k in (10, 0.1, 2, 0.5, 1000)])
        return dict(q=q, o=o, a=a, sol=['λ = \\f{c}{f}.', f'= \\f{{3 × 10^{{8}}}}{{{nf(f * (1e6 if unit == "MHz" else 1e9))}}} = {nf(lam, 3)} m.'], p=dict(t=t, f=f * (1e6 if unit == 'MHz' else 1e9)))
    if t == 'mag':
        E0 = rng.choice([1.5, 3, 6, 9, 9.3, 9.6, 12, 18, 30, 45, 60, 69, 90, 120, 300]); ask = rng.choice(['B', 'E'])
        if ask == 'B':
            q = f'In an EM wave in vacuum the electric field amplitude is {nf(E0)} V/m. The magnetic field amplitude is :'
            o, a = mcq(rng, f'{nf(E0 / c, 3)} T', [f'{nf(E0 / c * k, 3)} T' for k in (2, 0.5, 10, 3)])
        else:
            q = f'In an EM wave in vacuum the magnetic field amplitude is {nf(E0 / c, 3)} T. The electric field amplitude is :'
            o, a = mcq(rng, f'{nf(E0, 3)} V/m', [f'{nf(E0 * k, 3)} V/m' for k in (2, 0.5, 10, 3)])
        return dict(q=q, o=o, a=a, sol=['E_{0} = cB_{0}.', f'E_{{0}} = {nf(E0, 3)} V/m ↔ B_{{0}} = {nf(E0 / c, 3)} T.'], p=dict(t=t, E0=E0, ask=ask))
    if t == 'speed':
        mr, er = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 6, 8, 9, 16]); need(mr * er > 1)
        ask = rng.choice(['v', 'n'])
        v = c / math.sqrt(mr * er); n = math.sqrt(mr * er)
        q = f'A medium has relative permeability {mr} and relative permittivity {er}. The {"speed of EM waves in it" if ask == "v" else "refractive index"} is :'
        right = f'{nf(v, 3)} m/s' if ask == 'v' else nf(n, 3)
        wrong = [f'{nf(c / (mr * er), 3)} m/s', f'{nf(c * math.sqrt(mr * er) / 10, 3)} m/s', f'{nf(c / math.sqrt(er), 3)} m/s', f'{nf(v * 2, 3)} m/s'] if ask == 'v' else [nf(mr * er, 3), nf(math.sqrt(er), 3), nf(n * 2, 3), nf(math.sqrt(mr * er + 1), 3)]
        o, a = mcq(rng, right, wrong)
        return dict(q=q, o=o, a=a, sol=['v = \\f{1}{√{με}} = \\f{c}{√{μ_{r}ε_{r}}}; n = \\f{c}{v}.', f'{"v ≈ " + nf(v, 3) + " m/s" if ask == "v" else "n ≈ " + nf(n, 3)}.'], p=dict(t=t, mr=mr, er=er, ask=ask))
    k = rng.choice([1, 2, 3, 4, 5, 6]) * 10 ** rng.choice([3, 5, 6, 7]); n = rng.choice([1, 1.2, 1.25, 1.5, 2, 2.5, 3, 4])
    w = k * c / n; ask = rng.choice(['n', 'er'])
    q = f'An EM wave in a non-magnetic medium is E_{{y}} = 20 sin({nf(k)}x − {nf(w, 4)}t) V/m (SI). The {"refractive index" if ask == "n" else "dielectric constant"} of the medium is :'
    v = n if ask == 'n' else n * n
    o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (n * n if ask == 'n' else n, 1 / n, v * 2, v + 1)])
    return dict(q=q, o=o, a=a, sol=['Wave speed v = \\f{ω}{k}; n = \\f{c}{v}; non-magnetic → ε_{r} = n^{2}.', f'v = {nf(c / n, 3)} m/s → {"n" if ask == "n" else "ε_r"} = {nf(v, 3)}.'], p=dict(t=t, k=k, w=w, ask=ask))

def g_energy(rng):
    t = rng.choice(['I', 'u', 'press', 'point', 'photons', 'IB'])
    if t == 'I':
        E0 = rng.choice([10, 20, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000])
        I = 0.5 * c * e0 * E0 ** 2
        q = f'The electric field amplitude of an EM wave in vacuum is {E0} V/m (ε_{{0}} = 8.85 × 10^{{−12}}). Its intensity is about :'
        o, a = mcq(rng, f'{nf(I, 3)} W/m^{{2}}', [f'{nf(I * k, 3)} W/m^{{2}}' for k in (2, 0.5, 4, 0.25)])
        return dict(q=q, o=o, a=a, sol=['I = ½cε_{0}E_{0}^{2}.', f'≈ {nf(I, 3)} W/m^{{2}}.'], p=dict(t=t, E0=E0))
    if t == 'u':
        E0 = rng.choice([5, 10, 20, 30, 50, 60, 100, 200]); what = rng.choice(['total', 'electric'])
        u = 0.5 * e0 * E0 ** 2 * (1 if what == 'total' else 0.5)
        q = f'For an EM wave with E_{{0}} = {E0} V/m, the {"total average energy density" if what == "total" else "average energy density of the electric field alone"} is :'
        o, a = mcq(rng, f'{nf(u, 3)} J/m^{{3}}', [f'{nf(u * k, 3)} J/m^{{3}}' for k in (2, 0.5, 4, 0.25)])
        return dict(q=q, o=o, a=a, sol=['⟨u_{E}⟩ = ¼ε_{0}E_{0}^{2} and ⟨u_{B}⟩ is equal to it; total ½ε_{0}E_{0}^{2}.', f'≈ {nf(u, 3)} J/m^{{3}}.'], p=dict(t=t, E0=E0, what=what))
    if t == 'press':
        I = rng.choice([1, 3, 6, 9, 12, 15, 30, 60, 90, 120, 300, 600, 900]) * 10 ** rng.choice([0, 2, 3]); kind = rng.choice(['absorbs', 'reflects'])
        Pv = I / c * (2 if kind == 'reflects' else 1)
        q = f'Light of intensity {nf(I)} W/m^{{2}} falls normally on a surface that completely {kind} it. The radiation pressure is :'
        o, a = mcq(rng, f'{nf(Pv, 3)} Pa', [f'{nf(Pv * k, 3)} Pa' for k in ((0.5 if kind == "reflects" else 2), 3, 10, 0.1)])
        return dict(q=q, o=o, a=a, sol=['Absorbed: p = \\f{I}{c}; reflected: \\f{2I}{c}.', f'≈ {nf(Pv, 3)} Pa.'], p=dict(t=t, I=I, kind=kind))
    if t == 'point':
        Pw = rng.choice([50, 100, 200, 300, 450, 500, 1000]); r = rng.choice([1, 2, 3, 4, 5, 10])
        I = Pw / (4 * math.pi * r * r)
        q = f'A {Pw} W point source radiates equally in all directions. The intensity {r} m away is about :'
        o, a = mcq(rng, f'{nf(I, 3)} W/m^{{2}}', [f'{nf(x, 3)} W/m^{{2}}' for x in (Pw / (4 * math.pi * r), Pw / (math.pi * r * r), I * 2, Pw / (2 * math.pi * r * r) * 3)])
        return dict(q=q, o=o, a=a, sol=['I = \\f{P}{4πr^{2}}.', f'= \\f{{{Pw}}}{{4π × {r}^{{2}}}} ≈ {nf(I, 3)} W/m^{{2}}.'], p=dict(t=t, Pw=Pw, r=r))
    if t == 'photons':
        Pw = rng.choice([1, 2, 5, 10, 15, 20, 50, 100]); lam = rng.choice([200, 300, 400, 500, 600, 662, 700, 900, 1000]) * 1e-9
        N = Pw * lam / (6.6e-34 * c)
        q = f'A source emits {Pw} W of light of wavelength {round(lam * 1e9)} nm (h = 6.6 × 10^{{−34}} J s). Photons emitted per second ≈'
        o, a = mcq(rng, nf(N, 3), [nf(N * k, 3) for k in (10, 0.1, 2, 0.5)])
        return dict(q=q, o=o, a=a, sol=['N = \\f{P}{hc/λ} = \\f{Pλ}{hc}.', f'≈ {nf(N, 3)} per second.'], p=dict(t=t, Pw=Pw, lam=lam))
    B0 = rng.choice([1, 2, 3, 4, 5, 6, 10]) * 1e-8
    I = c * B0 ** 2 / (2 * mu0)
    q = f'The magnetic field amplitude of a plane EM wave is {nf(B0)} T. Its intensity is about (μ_{{0}} = 4π × 10^{{−7}}) :'
    o, a = mcq(rng, f'{nf(I, 3)} W/m^{{2}}', [f'{nf(I * k, 3)} W/m^{{2}}' for k in (2, 0.5, 4, 0.25)])
    return dict(q=q, o=o, a=a, sol=['I = \\f{cB_{0}^{2}}{2μ_{0}}.', f'≈ {nf(I, 3)} W/m^{{2}}.'], p=dict(t=t, B0=B0))

def g_disp(rng):
    t = rng.choice(['dvdt', 'rate', 'ac', 'part', 'ratio'])
    if t in ('dvdt', 'rate'):
        C = rng.choice([1, 2, 2.5, 4, 5, 6, 8, 10, 20]); Id = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 2, 4, 5, 10]); unit = rng.choice(['mA', 'A'])
        Ia = Id * (1e-3 if unit == 'mA' else 1); r = Ia / (C * 1e-6)
        q = f'A displacement current of {nf(Id)} {unit} flows between the plates of a {nf(C)} μF capacitor. The rate of change of potential difference is :'
        o, a = mcq(rng, f'{nf(r, 3)} V/s', [f'{nf(r * k, 3)} V/s' for k in (10, 0.1, 2, 0.5)])
        return dict(q=q, o=o, a=a, sol=['I_{d} = ε_{0}\\f{dΦ_{E}}{dt} = C\\f{dV}{dt}.', f'\\f{{dV}}{{dt}} = \\f{{{nf(Ia)}}}{{{nf(C)} × 10^{{−6}}}} ≈ {nf(r, 3)} V/s.'], p=dict(t='dvdt', C=C, I=Ia))
    if t == 'ac':
        C = rng.choice([1, 2, 5, 10, 12, 20]); f = rng.choice([50, 100, 500, 1000, 2000, 4000]); V0 = rng.choice([10, 20, 40, 100, 220])
        I = C * 1e-6 * 2 * math.pi * f * V0
        q = f'An AC voltage of amplitude {V0} V and frequency {f} Hz is applied across a {C} μF capacitor. The peak displacement current between its plates is about :'
        o, a = mcq(rng, f'{nf(I, 3)} A', [f'{nf(I * k, 3)} A' for k in (1 / (2 * math.pi), 2, 0.5, 1 / math.sqrt(2))])
        return dict(q=q, o=o, a=a, sol=['I_{d} = C\\f{dV}{dt}, peak CωV_{0}.', f'= {C} × 10^{{−6}} × 2π × {f} × {V0} ≈ {nf(I, 3)} A.'], p=dict(t=t, C=C, f=f, V0=V0))
    if t == 'part':
        A = rng.choice([10, 16, 20, 25, 40, 50, 100]); a0 = rng.choice([1, 2, 2.5, 3.2, 4, 5, 8, 10]); I = rng.choice([1, 2, 3, 4, 5, 6, 10]); need(a0 < A)
        v = I * a0 / A * 1000; need(abs(v - round(v)) < 1e-9)
        q = f'A parallel-plate capacitor with plates of area {A} cm^{{2}} is being charged by a current of {I} A. The displacement current through a flat area of {nf(a0)} cm^{{2}} between the plates, parallel to them, is ______ mA.'
        return dict(q=q, o=None, a=round(v), sol=['The field between the plates is uniform, so the displacement current spreads evenly over the area.', f'{I} × \\f{{{nf(a0)}}}{{{A}}} = {round(v)} mA.'], p=dict(t=t, A=A, a0=a0, I=I))
    sg = rng.choice([1, 2, 5, 10, 20, 50]); f = rng.choice([1, 2, 5, 10, 50, 100]) * 1e6
    r = sg / (2 * math.pi * f / (4 * math.pi * 9e9))
    need(abs(r - round(r)) < 1e-6)
    q = f'An EM wave of frequency {nf(f / 1e6)} MHz travels in a medium of conductivity {sg} S/m. The ratio of peak conduction current density to peak displacement current density is ______. (\\f{{1}}{{4πε_{{0}}}} = 9 × 10^{{9}})'
    return dict(q=q, o=None, a=round(r), sol=['J_{c} = σE_{0}, J_{d} = ε_{0}ωE_{0}.', f'\\f{{σ}}{{ωε_{{0}}}} = {round(r)}.'], p=dict(t=t, sg=sg, f=f))

def g_spec(rng):
    t = rng.choice(['order', 'band', 'bandE'])
    if t == 'order':
        names = rng.sample(list(TYP), 4); desc = rng.choice([True, False])
        lab = {n: f'λ_{{{i + 1}}}' for i, n in enumerate(names)}
        sep = ' > ' if desc else ' < '
        right = sep.join(lab[n] for n in sorted(names, key=TYP.get, reverse=desc))
        others = set()
        while len(others) < 6:
            p = rng.sample(names, 4); s = sep.join(lab[n] for n in p)
            if s != right: others.add(s)
        q = f'Arrange in {"DESCENDING" if desc else "ascending"} order of wavelength: ' + ', '.join(f'{n} ({lab[n]})' for n in names) + '. The order is :'
        o, a = mcq(rng, right, sorted(others))
        return dict(q=q, o=o, a=a, sol=['Shortest to longest: gamma, X-rays, UV, visible, infrared, microwaves, radio.', right + '.'], p=dict(t=t, names=names, desc=desc))
    lam = rng.choice([1e-12, 5e-11, 1e-10, 2e-9, 5e-8, 1e-7, 3e-7, 5e-7, 6e-7, 2e-6, 1e-5, 1e-4, 5e-3, 1e-2, 5e-2, 1, 10, 100])
    band = next(b for b, lo, hi in BANDS if lo <= lam < hi)
    if t == 'band':
        f = c / lam; q = f'An EM wave has frequency {nf(f, 3)} Hz. It belongs to :'
    else:
        E = 6.6e-34 * c / lam / 1.6e-19; need(1e-6 < E < 1e8); q = f'A photon of energy {nf(E, 3)} eV belongs to the region :'
    o, a = mcq(rng, band, [b for b, *_ in BANDS if b != band])
    return dict(q=q, o=o, a=a, sol=['Find λ = \\f{c}{f} (or λ = \\f{hc}{E}) and compare with the band edges.', f'λ ≈ {nf(lam, 3)} m → {band}.'], p=dict(t='band', lam=lam))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, StopIteration): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(eb=g_eb, energy=g_energy, disp=g_disp, spec=g_spec).items()}
def finish(it): return it

def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'dir':   # Poynting S = E × B / μ0 must point along k
        if p['ask'] == 'B':
            *m, ax, _ = Rv.split(' '); S = cross(vec(p['E']), vec(ax)); return S == vec(p['k']) and close(num(' '.join(m)), p['E0'] / c)
        *m, ax, _ = Rv.split(' '); S = cross(vec(ax), vec(p['B'])); return S == vec(p['k']) and abs(num(' '.join(m)) - p['E0']) < 1e-9
    if t == 'lam': return close(num(Rv), c / p['f'])
    if t == 'mag':   # equal energy densities: ε0E²/2 = B²/2μ0
        if p['ask'] == 'B': return close(num(Rv), math.sqrt(e0 * mu0) * p['E0'], 0.01)
        return close(num(Rv), num(nf(p['E0'] / c, 3)) / math.sqrt(e0 * mu0), 0.01)
    if t == 'speed':
        v = 1 / math.sqrt(p['mr'] * mu0 * p['er'] * e0); return close(num(Rv), v if p['ask'] == 'v' else 1 / math.sqrt(mu0 * e0) / v, 0.01)
    if t == 'wk':
        n = c / (p['w'] / p['k']); return close(num(Rv), n if p['ask'] == 'n' else n * n, 0.01)
    if t == 'I':   # I = c × (average total energy density)
        return close(num(Rv), c * (0.25 * e0 * p['E0'] ** 2 + (p['E0'] / c) ** 2 / (4 * mu0)), 0.01)
    if t == 'u':
        uE = 0.25 * e0 * p['E0'] ** 2; uB = (p['E0'] / c) ** 2 / (4 * mu0); return close(num(Rv), uE + uB if p['what'] == 'total' else uE, 0.01)
    if t == 'press':   # momentum flux: p = U/c per area per time; reflection doubles it
        return close(num(Rv), p['I'] / c * (2 if p['kind'] == 'reflects' else 1))
    if t == 'point':
        N = 2000; A = sum(2 * math.pi * p['r'] ** 2 * math.sin(math.pi * (i + .5) / N) * math.pi / N for i in range(N)); return close(num(Rv), p['Pw'] / A)
    if t == 'photons': return close(num(Rv), p['Pw'] / (6.6e-34 * c / p['lam']))
    if t == 'IB': return close(num(Rv), 0.5 * c * e0 * (c * p['B0']) ** 2, 0.01)
    if t == 'dvdt': return close(num(Rv), p['I'] / (p['C'] * 1e-6))
    if t == 'ac':
        N = 4000; T = 1 / p['f']; mx = max(abs(p['C'] * 1e-6 * (p['V0'] * math.sin(2 * math.pi * p['f'] * (i + 1) * T / N) - p['V0'] * math.sin(2 * math.pi * p['f'] * i * T / N)) / (T / N)) for i in range(N)); return close(num(Rv), mx, 0.01)
    if t == 'part': return abs(Rv - p['I'] * p['a0'] / p['A'] * 1000) < 1e-6
    if t == 'ratio': return abs(Rv - p['sg'] / (2 * math.pi * p['f'] * (1 / (4 * math.pi * 9e9)))) < 1e-6
    if t == 'order':
        names = p['names']; lab = {n: f'λ_{{{i + 1}}}' for i, n in enumerate(names)}; order = [x.strip() for x in Rv.replace('>', '<').split('<')]
        lam = [TYP[next(n for n in names if lab[n] == s)] for s in order]; return lam == sorted(lam, reverse=p['desc'])
    if t == 'band':
        b = next(b for b, lo, hi in BANDS if lo <= p['lam'] < hi); return Rv == b
    raise KeyError(t)
