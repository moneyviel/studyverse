"""Practice generators — Dual Nature. check() re-solves in SI units (joules) while generators work in eV / ratios."""
import random, math
from fractions import Fraction as F
from common import mcq, nf, fr
h, c, e = 6.63e-34, 3e8, 1.6e-19
HC = 1240   # eV nm
def g_pe(rng):
    t = rng.choice(['v0', 'k', 'phi', 'lam', 'lmax', 'which'])
    phi = rng.choice([1.9, 2.0, 2.1, 2.3, 2.5, 3.0, 3.2, 4.0, 4.5]); lam = rng.choice([150, 200, 248, 250, 300, 310, 400, 413])
    E = round(HC / lam, 3); K = round(E - phi, 3)
    if K <= 0.05: return g_pe(rng)
    if t in ('v0', 'k'):
        q = f'Light of wavelength {lam} nm falls on a metal of work function {phi} eV (hc = 1240 eV nm). The ' + ('stopping potential' if t == 'v0' else 'maximum kinetic energy of the photoelectrons') + ' is :'
        u = ' V' if t == 'v0' else ' eV'
        o, a = mcq(rng, nf(K, 3) + u, [nf(E, 3) + u, nf(E + phi, 3) + u, nf(K * 2, 3) + u, nf(abs(K - 0.5), 3) + u, nf(phi, 3) + u])
        return dict(q=q, o=o, a=a, sol=[f'Photon energy = \\f{{1240}}{{{lam}}} = {nf(E, 4)} eV.', f'K_{{max}} = {nf(E, 4)} − {phi} = {nf(K, 3)} eV' + (f' → V_{{0}} = {nf(K, 3)} V.' if t == 'v0' else '.')], p=dict(t='pe', lam=lam, phi=phi))
    if t == 'phi':
        v0 = rng.choice([0.5, 1, 1.5, 2, 2.5]); Ev = rng.choice([2.48, 3.1, 4.13, 4.96, 6.2])
        if Ev - v0 <= 0.3: return g_pe(rng)
        q = f'Photons of energy {Ev} eV produce photoelectrons with stopping potential {v0} V. The work function is :'
        o, a = mcq(rng, nf(round(Ev - v0, 3)) + ' eV', [nf(Ev + v0) + ' eV', nf(Ev) + ' eV', nf(v0) + ' eV', nf(round(Ev - 2 * v0, 3)) + ' eV' if Ev > 2 * v0 else nf(Ev * 2) + ' eV'])
        return dict(q=q, o=o, a=a, sol=[f'φ = hν − eV_{{0}} = {Ev} − {v0} = {nf(round(Ev - v0, 3))} eV.'], p=dict(t='phi', Ev=Ev, v0=v0))
    if t == 'lam':
        v0 = rng.choice([1, 1.5, 2, 2.5, 3]); phi2 = rng.choice([2.14, 2.0, 2.5, 1.96, 3.0]); lm = HC / (phi2 + v0)
        q = f'For a metal of work function {phi2} eV the stopping potential is {v0} V. The wavelength of the light is (hc = 1240 eV nm) :'
        o, a = mcq(rng, f'{lm:.0f} nm', [f'{HC / phi2:.0f} nm', f'{HC / v0:.0f} nm', f'{lm * 2:.0f} nm', f'{lm / 2:.0f} nm', f'{lm + 50:.0f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'hν = φ + eV_{{0}} = {nf(phi2 + v0)} eV.', f'λ = \\f{{1240}}{{{nf(phi2 + v0)}}} ≈ {lm:.0f} nm.'], p=dict(t='lam', phi=phi2, v0=v0))
    if t == 'lmax':
        q = f'The longest wavelength that can eject photoelectrons from a metal of work function {phi} eV is about (hc = 1240 eV nm) :'
        o, a = mcq(rng, f'{HC / phi:.0f} nm', [f'{HC / phi / 2:.0f} nm', f'{HC * phi / 10:.0f} nm', f'{HC / (phi + 1):.0f} nm', f'{HC / (phi - 0.5):.0f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'λ_{{0}} = \\f{{hc}}{{φ}} = \\f{{1240}}{{{phi}}} ≈ {HC / phi:.0f} nm.'], p=dict(t='lmax', phi=phi))
    L = rng.choice([450, 500, 550, 600, 400]); E2 = HC / L; mets = [('Cs', 1.9), ('K', 2.3), ('Na', 2.75), ('Li', 2.5), ('Ca', 3.2), ('Zn', 4.3)]
    two = rng.sample(mets, 2); ok = [m for m, p in two if p < E2]
    if not (0.05 < min(abs(E2 - p) for _, p in two)): return g_pe(rng)
    right = 'Both' if len(ok) == 2 else 'Neither' if not ok else f'{ok[0]} only'
    q = f'Light of wavelength {L} nm (hc = 1240 eV nm) falls on {two[0][0]} (φ = {two[0][1]} eV) and {two[1][0]} (φ = {two[1][1]} eV). Photoemission occurs for :'
    o, a = mcq(rng, right, ['Both', 'Neither', f'{two[0][0]} only', f'{two[1][0]} only'])
    return dict(q=q, o=o, a=a, sol=[f'Photon energy = \\f{{1240}}{{{L}}} ≈ {E2:.2f} eV.', 'Emission needs hν ≥ φ → ' + right + '.'], p=dict(t='which', L=L, two=two))

def g_pe2(rng):
    t = rng.choice(['thr', 'lam1', 'phi'])
    a1, k = rng.randint(2, 12), rng.choice([2, 3, 4])   # V1 at λ, V2 at kλ, with V1 = a1·V2
    # eV1 = X − φ, eV2 = X/k − φ, V1 = a1 V2 → solve X/φ
    # X − φ = a1(X/k − φ) → X(1 − a1/k) = φ(1 − a1) → X/φ = (1 − a1)/(1 − a1/k)
    if a1 == k: return g_pe2(rng)
    r = F(1 - a1) / (1 - F(a1, k))
    if r <= k or r <= 1: return g_pe2(rng)
    if t == 'thr':
        q = f'Light of wavelength λ gives a stopping potential {a1}V_{{0}}; light of wavelength {k}λ on the same metal gives V_{{0}}. The threshold wavelength is :'
        o, a = mcq(rng, fr(r) + 'λ', [fr(r + 1) + 'λ', fr(r * 2) + 'λ', fr(F(k * a1)) + 'λ', fr(r - F(1, 2)) + 'λ', fr(F(k + 1)) + 'λ'])
        return dict(q=q, o=o, a=a, sol=[f'{a1}eV_{{0}} = \\f{{hc}}{{λ}} − φ and eV_{{0}} = \\f{{hc}}{{{k}λ}} − φ.', 'Eliminate V_{0}: \\f{hc}{λφ} = ' + fr(r) + '.', f'λ_{{0}} = \\f{{hc}}{{φ}} = {fr(r)}λ.'], p=dict(t='thr', a1=a1, k=k))
    V1 = rng.choice([1.5, 2.0, 2.4, 2.5, 3.0, 3.2, 3.6, 4.0, 4.4, 5.0]); V2 = rng.choice([0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2])
    X = 2 * (V1 - V2)      # hc/(eλ) in volts with k = 2
    phi = X - V1
    if phi <= 0: return g_pe2(rng)
    if t == 'lam1':
        lm = HC / X
        q = f'Light of some wavelength gives a stopping potential of {V1} V on a metal; light of twice that wavelength gives {V2} V. The first wavelength is about (hc = 1240 eV nm) :'
        o, a = mcq(rng, f'{lm:.0f} nm', [f'{lm * 2:.0f} nm', f'{HC / V1:.0f} nm', f'{HC / (V1 - V2):.0f} nm', f'{lm / 2:.0f} nm', f'{lm + 40:.0f} nm', f'{lm * 1.5:.0f} nm'])
        return dict(q=q, o=o, a=a, sol=[f'{V1} = \\f{{hc}}{{eλ}} − \\f{{φ}}{{e}}, {V2} = \\f{{hc}}{{2eλ}} − \\f{{φ}}{{e}}.', f'Subtract: \\f{{hc}}{{2eλ}} = {nf(V1 - V2)} → \\f{{hc}}{{eλ}} = {nf(X)} V.', f'λ = \\f{{1240}}{{{nf(X)}}} ≈ {lm:.0f} nm.'], p=dict(t='lam1', V1=V1, V2=V2))
    q = f'Light of some wavelength gives a stopping potential of {V1} V on a metal; light of twice that wavelength gives {V2} V. The work function of the metal is :'
    o, a = mcq(rng, nf(phi) + ' eV', [nf(X) + ' eV', nf(V1 - V2) + ' eV', nf(phi + V2) + ' eV', nf(phi * 2) + ' eV', nf(phi + 1) + ' eV', nf(phi + 0.5) + ' eV', nf(V1) + ' eV'])
    return dict(q=q, o=o, a=a, sol=[f'From the two equations: \\f{{hc}}{{eλ}} = 2({V1} − {V2}) = {nf(X)} V.', f'φ = {nf(X)} − {V1} = {nf(phi)} eV.'], p=dict(t='phi2', V1=V1, V2=V2))

def g_photon(rng):
    t = rng.choice(['n', 'ratio', 'region'])
    if t == 'n':
        P = rng.choice([1, 2, 3, 5, 6, 10, 20]); lam = rng.choice([331.5, 442, 497.25, 552.5, 663, 994.5])
        n = P * 1e-3 * lam * 1e-9 / (h * c)
        q = f'A {P} mW laser emits light of wavelength {nf(lam)} nm. The number of photons emitted per second is (h = 6.63 × 10^{{−34}} J s, c = 3 × 10^{{8}} m/s) :'
        o, a = mcq(rng, nf(n, 3), [nf(n * 10, 3), nf(n / 2, 3), nf(n * 2, 3), nf(n / 10, 3)])
        return dict(q=q, o=o, a=a, sol=[f'E = \\f{{hc}}{{λ}} = {nf(h * c / (lam * 1e-9), 3)} J.', f'n = \\f{{P}}{{E}} = {nf(n, 3)} per second.'], p=dict(t='n', P=P, lam=lam))
    if t == 'ratio':
        l1, l2 = rng.sample([300, 400, 500, 600, 700, 450], 2); p1, p2 = rng.choice([(1, 1), (1, 2), (2, 1), (3, 1)])
        r = F(p1 * l1, p2 * l2)
        q = f'Two sources of power ratio {p1} : {p2} emit light of wavelengths {l1} nm and {l2} nm. The ratio of photons emitted per second is :'
        rat = lambda x: f'{x.numerator} : {x.denominator}'
        o, a = mcq(rng, rat(r), [rat(1 / r), rat(F(p1 * l2, p2 * l1)), rat(F(l1, l2)), rat(F(p1, p2)), '1 : 1', rat(r * 2), rat(r / 2)])
        return dict(q=q, o=o, a=a, sol=['n = \\f{Pλ}{hc} ∝ Pλ.', f'n_{{1}} : n_{{2}} = {p1}×{l1} : {p2}×{l2} = {r.numerator} : {r.denominator}.'], p=dict(t='ratio', l1=l1, l2=l2, p1=p1, p2=p2))
    E = rng.choice([1e-21, 2e-20, 3e-19, 4e-19, 6e-19, 1e-18]); lam = h * c / E
    reg = 'Microwave' if lam > 1e-3 else 'Infrared' if lam > 7e-7 else 'Visible' if lam > 4e-7 else 'Ultraviolet'
    if abs(lam - 4e-7) < 0.2e-7 or abs(lam - 7e-7) < 0.3e-7: return g_photon(rng)
    N = rng.choice([1e20, 2.5e20, 5e21]); Pw = E * N
    q = f'A source of power {nf(Pw, 3)} W emits {nf(N, 3)} photons per second. Its radiation lies in the :'
    o, a = mcq(rng, reg, ['Microwave', 'Infrared', 'Visible', 'Ultraviolet'])
    return dict(q=q, o=o, a=a, sol=[f'Energy per photon = {nf(E, 3)} J.', f'λ = hc/E ≈ {nf(lam * 1e9, 3)} nm → {reg}.'], p=dict(t='region', E=E))

PART = [('electron', 1, 1), ('proton', 1836, 1), ('deuteron', 3672, 1), ('alpha particle', 7344, 2), ('neutron', 1839, 0), ('triton', 5508, 1)]
def g_dbw(rng):
    t = rng.choice(['sameK', 'sameV', 'ratioV', 'speed', 'sameL', 'elV', 'elV', 'thermal'])
    if t == 'elV':
        V = rng.choice([25, 36, 49, 64, 81, 100, 121, 144, 196, 225, 400, 625, 900, 2500, 10000]); lam = 1.227 / math.sqrt(V)
        q = f'An electron is accelerated from rest through {V} V. Its de Broglie wavelength is about :'
        o, a = mcq(rng, nf(lam, 3) + ' nm', [nf(lam * 10, 3) + ' nm', nf(lam / 10, 3) + ' nm', nf(1.227 / V, 3) + ' nm', nf(lam * 2, 3) + ' nm'])
        return dict(q=q, o=o, a=a, sol=['λ = \\f{h}{√{2meV}} ≈ \\f{1.227}{√{V}} nm for an electron.', f'= \\f{{1.227}}{{√{{{V}}}}} = {nf(lam, 3)} nm.'], p=dict(t='elV', V=V))
    if t == 'thermal':
        gas, M = rng.choice([('helium atom', 4), ('neon atom', 20), ('nitrogen molecule', 28), ('oxygen molecule', 32), ('argon atom', 40)]); T = rng.choice([27, 127, 227, 327, 927])
        m = M * 1.66e-27; lam = h / math.sqrt(3 * m * 1.38e-23 * (T + 273))
        q = f'The de Broglie wavelength of {"an" if gas[0] in "aeiou" else "a"} {gas} (mass {M} u, 1 u = 1.66 × 10^{{−27}} kg) moving with its rms speed at {T} ºC is about (k = 1.38 × 10^{{−23}} J/K) :'
        o, a = mcq(rng, nf(lam * 1e12, 3) + ' pm', [nf(lam * 1e12 * math.sqrt(3 / 2), 3) + ' pm', nf(lam * 1e12 * 2, 3) + ' pm', nf(lam * 1e12 / 2, 3) + ' pm', nf(lam * 1e13, 3) + ' pm'])
        return dict(q=q, o=o, a=a, sol=['p = m v_{rms} = √{3mkT}.', f'λ = \\f{{h}}{{√{{3mkT}}}} with T = {T + 273} K → ≈ {nf(lam * 1e12, 3)} pm.'], p=dict(t='thermal', M=M, T=T))
    if t in ('sameK', 'sameV'):
        a_, b_ = rng.sample([x for x in PART if t == 'sameK' or x[2]], 2)
        if t == 'sameK': r = math.sqrt(b_[1] / a_[1]); why = 'same K: λ ∝ 1/√{m}'
        else: r = math.sqrt(b_[1] * b_[2] / (a_[1] * a_[2])); why = 'accelerated through the same V: K = qV, so λ ∝ 1/√{mq}'
        q = f'A {a_[0]} and {"an" if b_[0][0] in "aeiou" else "a"} {b_[0]} ' + ('have the same kinetic energy.' if t == 'sameK' else 'are accelerated from rest through the same potential difference.') + f' The ratio λ_{{{a_[0][0]}}} : λ_{{{b_[0][0]}}} of their de Broglie wavelengths is about (m_{{p}} = 1836 m_{{e}}) :'
        o, a = mcq(rng, nf(r, 3), [nf(1 / r, 3), nf(r * r, 3), nf(1 / (r * r), 3), nf(r * 2, 3)])
        return dict(q=q, o=o, a=a, sol=[f'λ = \\f{{h}}{{√{{2mK}}}}; {why}.', f'Ratio = {nf(r, 3)}.'], p=dict(t=t, a=a_[0], b=b_[0]))
    if t == 'ratioV':
        k = rng.choice([F(3, 2), 2, 3, F(1, 2), F(5, 4), F(4, 3), F(2, 3), F(5, 2), 4, F(1, 3), F(6, 5)]); V1V2 = k * k
        q = f'When the accelerating voltage of an electron is changed from V_{{1}} to V_{{2}}, its de Broglie wavelength becomes {fr(k)} times. Then V_{{1}}/V_{{2}} is :'
        o, a = mcq(rng, fr(V1V2), [fr(k), fr(1 / V1V2), fr(1 / k), fr(V1V2 * 2)])
        return dict(q=q, o=o, a=a, sol=['λ ∝ 1/√{V} → \\f{V_{1}}{V_{2}} = (\\f{λ_{2}}{λ_{1}})^{2}.', f'= ({fr(k)})^{{2}} = {fr(V1V2)}.'], p=dict(t='ratioV', k=str(k)))
    if t == 'speed':
        pct = rng.choice([10, 20, 25, 30, 40, 50, 60, 75]); up = rng.random() < 0.5; f = F(100, 100 + pct) if up else F(100, 100 - pct)
        q = f"An electron's speed {'increases' if up else 'decreases'} by {pct}%. Its de Broglie wavelength becomes ______ times the original."
        o, a = mcq(rng, nf(f, 4), [nf(1 / f, 4), nf(f * f, 4), '1', nf(f + F(1, 10), 4)])
        return dict(q=q, o=o, a=a, sol=['λ = h/(mv) ∝ 1/v.', f'Factor = {nf(f, 4)}.'], p=dict(t='speed', pct=pct, up=up))
    a_, b_ = rng.sample(PART, 2)
    q = f'A {a_[0]} and {"an" if b_[0][0] in "aeiou" else "a"} {b_[0]} have the same de Broglie wavelength. The ratio of their kinetic energies K_{{{a_[0][0]}}} : K_{{{b_[0][0]}}} is :'
    r = F(b_[1], a_[1])
    o, a = mcq(rng, f'{r.numerator} : {r.denominator}', [f'{r.denominator} : {r.numerator}', '1 : 1', f'{nf(math.sqrt(float(r)), 3)} : 1', f'{r.numerator * r.numerator} : {r.denominator * r.denominator}'])
    return dict(q=q, o=o, a=a, sol=['Same λ → same momentum p.', 'K = p^{2}/2m ∝ 1/m → ' + f'{r.numerator} : {r.denominator}.'], p=dict(t='sameL', a=a_[0], b=b_[0]))

def g_dbm(rng):
    t = rng.choice(['perpE', 'alongE', 'B'])
    if t == 'B':
        q = f'An electron moving with velocity v_{{0}}î enters a uniform magnetic field B_{{0}}{rng.choice(["ĵ", "k̂"])}. Its de Broglie wavelength after time t is (λ_{{0}} at t = 0) :'
        o, a = mcq(rng, 'λ_{0}', ['\\f{λ_{0}}{√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}}', 'λ_{0}√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}', '\\f{λ_{0}}{1 + \\f{eB_{0}t}{m}}'])
        return dict(q=q, o=o, a=a, sol=['Magnetic force ⟂ velocity → no work → speed constant.', 'So λ stays λ_{0}.'], p=dict(t='B'))
    v0, E0 = rng.choice([5e5, 1e6, 2e6, 3e6]), rng.choice([50, 100, 200, 500, 1000]); m = 9.1e-31; a_ = e * E0 / m
    tt = float(f'{rng.choice([0.4, 0.75, 1, 1.5, 2, 3]) * v0 / a_:.2g}')
    if t == 'perpE':
        v = math.sqrt(v0 ** 2 + (a_ * tt) ** 2); r = v0 / v
        q = f'An electron (m = 9.1 × 10^{{−31}} kg) moving at {nf(v0)} m/s along x enters a uniform electric field of {E0} V/m along y. After {nf(tt)} s its de Broglie wavelength is ______ times the initial value.'
    else:
        v = v0 + a_ * tt; r = v0 / v
        q = f'An electron (m = 9.1 × 10^{{−31}} kg) moving at {nf(v0)} m/s along +x enters a uniform electric field of {E0} V/m along −x. After {nf(tt)} s its de Broglie wavelength is ______ times the initial value.'
    o, a = mcq(rng, nf(r, 3), [nf(1 / r, 3), nf(math.sqrt(r), 3), nf(r * r, 3), '1'])
    return dict(q=q, o=o, a=a, sol=[f'Acceleration eE/m = {nf(a_, 3)} m/s^{{2}}.', ('Perpendicular gain: v = √{v_{0}^{2} + (at)^{2}}' if t == 'perpE' else 'Force on the electron is along +x (opposite to E), so v = v_{0} + at') + f' = {nf(v, 3)} m/s.', f'λ ∝ 1/v → factor {nf(r, 3)}.'], p=dict(t=t, v0=v0, E0=E0, tt=tt))

LAW = [('Stopping potential increases with the intensity of light.', False), ('Stopping potential depends on the frequency of light and the metal.', True), ('Photoelectric current at saturation is proportional to intensity.', True),
       ('There is a measurable time lag before photoemission starts.', False), ('Below the threshold frequency no electrons are emitted, however intense the light.', True), ('The slope of K_{max} vs ν graph equals Planck\'s constant.', True),
       ('The slope of V_{0} vs ν graph equals h.', False), ('Photons have zero rest mass but carry momentum h/λ.', True), ('For a fixed power, more photons per second are emitted at higher frequency.', False),
       ('A magnetic field changes the de Broglie wavelength of a moving electron.', False), ('Electron diffraction (Davisson–Germer) supports the wave nature of matter.', True), ('The photoelectric effect is explained by the wave theory of light.', False),
       ('Photoemission is practically instantaneous.', True), ('Work function is the same for all metals.', False), ('K_{max} vs ν lines for different metals are parallel.', True), ('A heavier particle with the same kinetic energy has a longer de Broglie wavelength.', False),
       ('Two particles with equal de Broglie wavelengths have equal momenta.', True), ('Light of higher frequency always produces a larger photocurrent.', False), ('Stopping potential is 1/e times the maximum kinetic energy of photoelectrons.', True),
       ('Photons of red light carry more energy than photons of violet light.', False), ('Radiation pressure shows that light carries momentum.', True), ('The saturation current does not depend on intensity.', False)]
def g_law(rng):
    (s1, v1), (s2, v2) = rng.sample(LAW, 2)
    opts = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
    right = opts[0] if v1 and v2 else opts[1] if not (v1 or v2) else opts[2] if v1 else opts[3]
    o, a = mcq(rng, right, [x for x in opts if x != right])
    return dict(q=f'Statement I: {s1} Statement II: {s2}', o=o, a=a, sol=[f'I is {"true" if v1 else "false"}.', f'II is {"true" if v2 else "false"}.'], p=dict(t='law', s1=s1, s2=s2))

GEN = dict(pe=g_pe, pe2=g_pe2, photon=g_photon, dbw=g_dbw, dbm=g_dbm, law=g_law)
def finish(it): return it
MASS = {'electron': 9.1e-31, 'proton': 9.1e-31 * 1836, 'deuteron': 9.1e-31 * 3672, 'alpha particle': 9.1e-31 * 7344, 'neutron': 9.1e-31 * 1839, 'triton': 9.1e-31 * 5508}; Q = {'electron': 1, 'proton': 1, 'deuteron': 1, 'alpha particle': 2, 'neutron': 0, 'triton': 1}
HCX = 6.62607015e-34 * 299792458 / 1.602176634e-19 * 1e9   # hc in eV nm from SI constants (1239.84)
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    num = lambda s: float(s.split(' ')[0].replace('−', '-').replace(' × 10^{', 'e').replace('}', '')) if 'e' not in s.split(' ')[0] else float(s.split(' ')[0])
    rel = lambda a, b, tol=6e-3: abs(a - b) <= tol * abs(b)
    if t == 'pe': K = HCX / p['lam'] - p['phi']; return abs(num(R) - K) < 0.012
    if t == 'phi': return rel(num(R), p['Ev'] - p['v0'])
    if t == 'lam': return abs(num(R) - HCX / (p['phi'] + p['v0'])) < 1.5
    if t == 'lmax': return abs(num(R) - HCX / p['phi']) < 1.5
    if t == 'which':
        E = HCX / p['L']; ok = [m for m, ph in p['two'] if ph < E]
        return R == ('Both' if len(ok) == 2 else 'Neither' if not ok else f'{ok[0]} only')
    if t == 'thr':   # substitute the marked answer back: with λ0 = rλ, φ = (hc/λ)/r; both stopping potentials must keep the ratio a1
        r = F(R.replace('λ', '').replace('\\f{', '').replace('}{', '/').replace('}', '')); V1 = 1 - 1 / r; V2 = F(1, p['k']) - 1 / r
        return V2 > 0 and V1 == p['a1'] * V2
    if t == 'lam1': X = 2 * (p['V1'] - p['V2']); return abs(num(R) - HCX / X) < 1.5
    if t == 'phi2': return rel(num(R), 2 * (p['V2'] - p['V1']) * -1 - p['V1'] if False else 2 * (p['V1'] - p['V2']) - p['V1'])
    if t == 'n': return rel(float(R.replace(' × 10^{', 'e').replace('}', '').replace('−', '-')), p['P'] * 1e-3 / (h * c / (p['lam'] * 1e-9)), 0.01)
    if t == 'ratio': a, b = R.split(' : '); return F(int(a), int(b)) == F(p['p1'] * p['l1'], p['p2'] * p['l2'])
    if t == 'region':
        lam = h * c / p['E']; return R == ('Microwave' if lam > 1e-3 else 'Infrared' if lam > 7e-7 else 'Visible' if lam > 4e-7 else 'Ultraviolet')
    if t in ('sameK', 'sameV'):
        K = 1e-16
        la = h / math.sqrt(2 * MASS[p['a']] * (K if t == 'sameK' else K * Q[p['a']])); lb = h / math.sqrt(2 * MASS[p['b']] * (K if t == 'sameK' else K * Q[p['b']]))
        return rel(num(R), la / lb)
    if t == 'ratioV': k = float(F(p['k'])); return abs(float(F(R.replace('\\f{', '').replace('}{', '/').replace('}', ''))) - k * k) < 1e-9
    if t == 'speed': f = 1 / (1 + (p['pct'] / 100 if p['up'] else -p['pct'] / 100)); return rel(num(R), f, 1e-3)
    if t == 'elV': return rel(num(R), h / math.sqrt(2 * 9.1e-31 * e * p['V']) * 1e9, 0.01)
    if t == 'thermal': m = p['M'] * 1.66e-27; return rel(num(R), h / (m * math.sqrt(3 * 1.38e-23 * (p['T'] + 273) / m)) * 1e12, 6e-3)
    if t == 'sameL': a, b = R.split(' : '); return abs(float(a) / float(b) - MASS[p['b']] / MASS[p['a']]) < 1e-6
    if t == 'B': return R == 'λ_{0}'
    if t in ('perpE', 'alongE'):
        m = 9.1e-31; a_ = e * p['E0'] / m; N = 20000; vx, vy = p['v0'], 0.0
        for _ in range(N):   # numeric integration of the motion (independent of the closed form)
            if t == 'perpE': vy += a_ * p['tt'] / N
            else: vx += a_ * p['tt'] / N
        return rel(num(R), p['v0'] / math.hypot(vx, vy), 6e-3)
    if t == 'law':
        tv = dict(LAW); v1, v2 = tv[p['s1']], tv[p['s2']]
        want = 'Both Statement I and Statement II are true' if v1 and v2 else 'Both Statement I and Statement II are false' if not (v1 or v2) else 'Statement I is true but Statement II is false' if v1 else 'Statement I is false but Statement II is true'
        return R == want
    raise KeyError(t)
