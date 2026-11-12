"""Practice generators — Physics Unit 6: Gravitation. check() re-solves each item a different way
(numerical integration of energy / Kepler from first principles with explicit G, M values)."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
G, ME, RE, g0 = 6.67e-11, 6e24, 6.4e6, 9.8

def g_law(rng):
    t = rng.choice(['ratio', 'scale', 'two', 'zero'])
    if t == 'ratio':
        k = rng.choice([1, 2, 3, 4, 5]); m = rng.choice([30, 45, 60, 72, 80, 90, 100, 120]); gg = 10
        v = F(m * gg, (1 + k) ** 2)
        q = f'A {m} kg body is at a height {k}R above the earth\'s surface (R = radius of earth, g = 10 m s^{{−2}}). The gravitational pull on it is :'
        o, a = mcq(rng, nf(float(v), 4) + ' N', [nf(x, 4) + ' N' for x in (m * gg / k ** 2, m * gg / (k + 1), m * gg / (2 * k + 1) ** 2, m * gg / (k * k + 1), float(v) * 2)])
        return dict(q=q, o=o, a=a, sol=[f'Distance from the centre = (1 + {k})R → force ÷ {(1 + k) ** 2}.', f'F = \\f{{{m * gg}}}{{{(1 + k) ** 2}}} = {nf(float(v), 4)} N.'], p=dict(t='ratio', k=k, m=m))
    if t == 'scale':
        fa, fm = rng.choice([2, 3, 4, F(1, 2)]), rng.choice([2, 3, 4, F(1, 2), 1]); T0 = rng.choice([2, 3, 4, 5, 6, 8])
        v = T0 * math.sqrt(float(F(fa) ** 3 / F(fm)))
        if abs(v - round(v)) > 1e-9: return g_law(rng)
        q = f'Three identical spheres at the corners of an equilateral triangle, released from rest, collide after {T0} s under their mutual gravity. If the side is made {fr(fa)} times and each mass {fr(fm)} times, they collide after ______ s.'
        return dict(q=q, o=None, a=round(v), sol=['Only G, m and a can set the time: t ∝ √{\\f{a^{3}}{Gm}}.', f't = {T0} × √{{\\f{{({fr(fa)})^{{3}}}}{{{fr(fm)}}}}} = {round(v)} s.'], p=dict(t='scale', fa=str(fa), fm=str(fm), T0=T0))
    if t == 'two':
        m1, m2, d = rng.choice([1, 2, 4, 9, 16]), rng.choice([1, 4, 9, 16, 25]), rng.choice([1, 2, 3, 4, 6, 10])
        if m1 == m2: return g_law(rng)
        x = d * math.sqrt(m1) / (math.sqrt(m1) + math.sqrt(m2))
        q = f'Point masses {m1} kg and {m2} kg are {d} m apart. The gravitational field is zero at a distance from the {m1} kg mass of :'
        o, a = mcq(rng, nf(x, 3) + ' m', [nf(v, 3) + ' m' for v in (d * m1 / (m1 + m2), d * m2 / (m1 + m2), d - x, d / 2 + 0.1 if abs(d / 2 - x) < 1e-6 else d / 2, d * math.sqrt(m2) / (math.sqrt(m1) + math.sqrt(m2)) + 0.3)])
        return dict(q=q, o=o, a=a, sol=['Between the masses: \\f{Gm_{1}}{x^{2}} = \\f{Gm_{2}}{(d − x)^{2}} → \\f{x}{d − x} = √{\\f{m_{1}}{m_{2}}}.', f'x = \\f{{{d}√{{{m1}}}}}{{√{{{m1}}} + √{{{m2}}}}} = {nf(x, 3)} m.'], p=dict(t='two', m1=m1, m2=m2, d=d))
    n = rng.choice([3, 4, 5, 6, 8])
    q = f'{n} equal point masses sit at the corners of a regular {n}-sided polygon. The net gravitational field at its centre is :'
    o, a = mcq(rng, 'zero', ['\\f{GM}{r^{2}}', f'\\f{{{n}GM}}{{r^{{2}}}}', '\\f{GM}{2r^{2}}', '\\f{2GM}{r^{2}}'])
    return dict(q=q, o=o, a=a, sol=['The pulls are equal in size and spread evenly in direction.', 'By symmetry they cancel → zero.'], p=dict(t='zero', n=n))

def g_gvar(rng):
    t = rng.choice(['h', 'd', 'shape', 'pend', 'hfor', 'small'])
    if t == 'h':
        k = rng.choice([F(1, 2), 1, 2, 3, 4, 5, 7, 9, F(1, 3), F(1, 4), F(3, 2), F(2, 3)]); v = 1 / (1 + F(k)) ** 2
        q = f'At a height h = {fr(k)}R above the earth\'s surface, g becomes ______ times its surface value.'
        o, a = mcq(rng, fr(v), [fr(x) for x in (1 - 2 * F(k), 1 / (1 + F(k)), 1 / F(k) ** 2 if k else F(1, 7), 1 - F(k), v * 2)])
        return dict(q=q, o=o, a=a, sol=['g′ = g(\\f{R}{R + h})^{2}.', f'= (\\f{{1}}{{1 + {fr(k)}}})^{{2}} = {fr(v)}.'], p=dict(t='h', k=str(k)))
    if t == 'd':
        f = rng.choice([F(1, 4), F(1, 2), F(1, 3), F(3, 4), F(1, 5), F(2, 3), F(1, 10), F(2, 5), F(3, 5), F(1, 8)]); v = 1 - f
        q = f'At a depth equal to {fr(f)} of the earth\'s radius, g becomes ______ times its surface value.'
        o, a = mcq(rng, fr(v), [fr(x) for x in ((1 - f) ** 2, 1 / (1 + f) ** 2, f, 1 - 2 * f if 1 - 2 * f > 0 else F(1, 9), v / 2)])
        return dict(q=q, o=o, a=a, sol=['Inside a uniform earth: g′ = g(1 − \\f{d}{R}).', f'= 1 − {fr(f)} = {fr(v)}.'], p=dict(t='d', f=str(f)))
    if t == 'shape':
        fm, fr_ = rng.choice([1, 2, 3, 4, F(1, 2), 8, 9, 16, F(1, 4)]), rng.choice([2, F(1, 2), 3, F(1, 3), 4, F(3, 2)])
        v = F(fm) / F(fr_) ** 2
        q = f'A planet has {fr(fm)} times the mass and {fr(fr_)} times the radius of the earth. g on its surface is ______ times g on earth.'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(fm) / F(fr_), F(fm) * F(fr_) ** 2, F(fr_) ** 2 / F(fm), F(fm) / F(fr_) ** 3, v * 2)])
        return dict(q=q, o=o, a=a, sol=['g = \\f{GM}{R^{2}} ∝ \\f{M}{R^{2}}.', f'= \\f{{{fr(fm)}}}{{({fr(fr_)})^{{2}}}} = {fr(v)}.'], p=dict(t='shape', fm=str(fm), fr=str(fr_)))
    if t == 'pend':
        k = rng.choice([1, 2, 3, 4, 5]); L = rng.choice([1, 4, 9, 16, 25]) * F(1, 1); T = 2 * math.pi * math.sqrt(float(L) / (math.pi ** 2 / (1 + k) ** 2))
        if abs(T - round(T)) > 1e-9: return g_gvar(rng)
        q = f'A simple pendulum of length {L} m is at a height {k}R above the earth\'s surface. Taking g = π^{{2}} m s^{{−2}} on the surface, its period is ______ s.'
        return dict(q=q, o=None, a=round(T), sol=[f'g′ = \\f{{g}}{{{(1 + k) ** 2}}}.', f'T = 2π√{{\\f{{L}}{{g′}}}} = 2π × \\f{{{1 + k}√{{{L}}}}}{{π}} = {round(T)} s.'], p=dict(t='pend', k=k, L=int(L)))
    if t == 'hfor':
        n = rng.choice([4, 9, 16, 25, 36, 49, 64, 100]); v = math.isqrt(n) - 1
        q = f'g falls to \\f{{g}}{{{n}}} at a height of ______ R above the earth\'s surface.'
        return dict(q=q, o=None, a=v, sol=[f'(\\f{{R}}{{R + h}})^{{2}} = \\f{{1}}{{{n}}} → R + h = {math.isqrt(n)}R.', f'h = {v}R.'], p=dict(t='hfor', n=n))
    h = rng.choice([4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 3.2, 6.4, 1.6]); R = 6400
    v = 100 * (h / R)
    q = f'g at a depth of {nf(h)} km is compared with g at a height of {nf(h)} km (R = 6400 km). The difference is about ______ % of g.'
    o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (2 * v, v / 2, 3 * v, 4 * v)])
    return dict(q=q, o=o, a=a, sol=['Depth: 1 − \\f{d}{R}; height (h ≪ R): 1 − \\f{2h}{R}.', f'Difference = \\f{{h}}{{R}} = {nf(v, 3)} %.'], p=dict(t='small', h=h))

def g_escape(rng):
    t = rng.choice(['ratio', 'dens', 'from', 'energy', 'fall', 'work'])
    if t == 'ratio':
        fm, fr_ = rng.choice([8, 2, 4, F(1, 6), F(1, 2), 9, 16]), rng.choice([2, F(1, 3), 4, F(1, 2), 1, 3]); ve = 11.2
        v = ve * math.sqrt(float(F(fm) / F(fr_)))
        q = f'A planet has {fr(fm)} times the mass and {fr(fr_)} times the radius of the earth (v_{{e}} = 11.2 km/s). Its escape speed is about :'
        o, a = mcq(rng, nf(v, 3) + ' km/s', [nf(x, 3) + ' km/s' for x in (ve * float(F(fm) / F(fr_)), ve * math.sqrt(float(F(fr_) / F(fm))), ve * math.sqrt(float(F(fm) * F(fr_))), v * 2, v / 2)])
        return dict(q=q, o=o, a=a, sol=['v_{e} = √{\\f{2GM}{R}} ∝ √{\\f{M}{R}}.', f'= 11.2 × √{{{nf(float(F(fm) / F(fr_)), 3)}}} ≈ {nf(v, 3)} km/s.'], p=dict(t='eratio', fm=str(fm), fr=str(fr_)))
    if t == 'dens':
        fr_, fd = rng.choice([2, F(1, 2), F(1, 10), 3]), rng.choice([2, F(1, 2), 4, F(1, 10), 1])
        v = float(F(fr_)) * math.sqrt(float(F(fd)))
        q = f'Planet B has {fr(fr_)} times the radius and {fr(fd)} times the density of planet A. v_{{e}}(B)/v_{{e}}(A) is :'
        o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (float(F(fr_)) * float(F(fd)), math.sqrt(float(F(fr_) * F(fd))), float(F(fr_)) ** 1.5 * math.sqrt(float(F(fd))), v * 2)])
        return dict(q=q, o=o, a=a, sol=['M = \\f{4}{3}πR^{3}ρ → v_{e} ∝ R√{ρ}.', f'= {fr(fr_)} × √{{{fr(fd)}}} ≈ {nf(v, 3)}.'], p=dict(t='dens', fr=str(fr_), fd=str(fd)))
    if t == 'from':
        k = rng.choice([1, 2, 3, 4, 7, 8]); r = 1 + k
        q = f'From rest at a height {k}R above the earth\'s surface, the least speed to escape the earth is :'
        o, a = mcq(rng, f'√{{\\f{{2GM}}{{{r}R}}}}', [f'√{{\\f{{2GM}}{{{x}R}}}}' for x in (k, r * r, 1, 2 * r)] + ['√{\\f{GM}{R}}'])
        return dict(q=q, o=o, a=a, sol=[f'Distance from the centre r = {r}R; need ½mv^{{2}} = \\f{{GMm}}{{r}}.', f'v = √{{\\f{{2GM}}{{{r}R}}}}.'], p=dict(t='from', k=k))
    if t == 'energy':
        k = rng.choice([1, 2, 3, 4, F(1, 2)]); v = 1 - 1 / (1 + F(k))
        q = f'The increase in potential energy when a mass m is raised from the earth\'s surface to a height {fr(k)}R is ______ × mgR.'
        o, a = mcq(rng, fr(v), [fr(x) for x in (F(k), F(k) / (1 + F(k)) ** 2, 1 / (1 + F(k)), v / 2, v * 2)])
        return dict(q=q, o=o, a=a, sol=['ΔU = GMm(\\f{1}{R} − \\f{1}{R + h}) = mgR(1 − \\f{R}{R + h}).', f'= {fr(v)} mgR.'], p=dict(t='energy', k=str(k)))
    if t == 'fall':
        m = rng.choice([1, 2, 5, 10]); K = m * g0 * RE
        q = f'A {m} kg body falls to the earth from very far away (R = 6400 km, g = 9.8 m s^{{−2}}). Its kinetic energy on reaching the surface is about :'
        o, a = mcq(rng, nf(K, 3) + ' J', [nf(x, 3) + ' J' for x in (K / 2, 2 * K, K / 10, m * g0 * RE / 4)])
        return dict(q=q, o=o, a=a, sol=['Energy: 0 = ½mv^{2} − \\f{GMm}{R} → KE = mgR.', f'= {m} × 9.8 × 6.4 × 10^{{6}} ≈ {nf(K, 3)} J.'], p=dict(t='fall', m=m))
    ms = sorted(rng.sample([100, 200, 300, 400, 500, 600], 3)); a1, a2 = rng.choice([(10, 20), (20, 25), (10, 15), (20, 40), (5, 10)])
    W = 6.7e-11 * (ms[0] * ms[1] + ms[1] * ms[2] + ms[0] * ms[2]) * (1 / a1 - 1 / a2)
    q = f'Masses {ms[0]}, {ms[1]} and {ms[2]} kg at the corners of an equilateral triangle of side {a1} m are moved to the corners of one of side {a2} m. Work done against gravity (G = 6.7 × 10^{{−11}}) is about :'
    o, a = mcq(rng, nf(W, 3) + ' J', [nf(x, 3) + ' J' for x in (W * 2, W / 2, W * a2 / a1, 6.7e-11 * sum(ms) * (1 / a1 - 1 / a2))])
    return dict(q=q, o=o, a=a, sol=['W = ΔU = G(m_{1}m_{2} + m_{2}m_{3} + m_{1}m_{3})(\\f{1}{a_{1}} − \\f{1}{a_{2}}).', f'≈ {nf(W, 3)} J.'], p=dict(t='work', ms=ms, a1=a1, a2=a2))

def g_orbit(rng):
    t = rng.choice(['v', 'T', 'kep', 'E', 'L', 'geo', 'pct'])
    if t == 'v':
        k = rng.choice([4, 9, 16, 25, F(1, 4), F(1, 9), 2, 3]); v0 = rng.choice([1, 2, 3, 4, 5, 6, 8, 10])
        v = v0 * math.sqrt(float(F(k)))
        q = f'Satellites A and B circle a planet at radii {fr(k)}R and R. If A moves at {v0}v, B moves at :'
        o, a = mcq(rng, f'{nf(v, 3)}v', [f'{nf(x, 3)}v' for x in (v0 * float(F(k)), v0 / math.sqrt(float(F(k))), v0 / float(F(k)), v0)])
        return dict(q=q, o=o, a=a, sol=['v_{o} = √{\\f{GM}{r}} ∝ \\f{1}{√{r}}.', f'v_{{B}} = {v0}v × √{{{fr(k)}}} = {nf(v, 3)}v.'], p=dict(t='v', k=str(k), v0=v0))
    if t == 'T':
        T0 = rng.choice([8, 16, 27, 40, 64, 80, 100, 125, 160, 200, 216, 240, 320, 365, 400, 1000]); f = rng.choice([F(1, 4), F(1, 9), 4, F(1, 16), 9, 16, F(1, 25), 25])
        v = T0 * float(F(f)) ** 1.5
        if abs(v - round(v)) > 1e-9: return g_orbit(rng)
        q = f'A planet takes {T0} days per revolution. If its orbit radius becomes {fr(f)} times, the new period is ______ days.'
        return dict(q=q, o=None, a=round(v), sol=['Kepler: T ∝ r^{3/2}.', f'T = {T0} × ({fr(f)})^{{3/2}} = {round(v)} days.'], p=dict(t='T', T0=T0, f=str(f)))
    if t == 'kep':
        fm, fr_ = rng.choice([2, 3, 4, F(1, 4), 8, F(1, 2), 9]), rng.choice([2, 4, F(1, 2), 1, 3, 9, F(1, 4)])
        v = math.sqrt(float(F(fr_) ** 3 / F(fm)))
        q = f'Around a star of {fr(fm)} times the mass, a planet orbits at {fr(fr_)} times the radius of another planet around the original star. The period ratio (new/old) is :'
        o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (math.sqrt(float(F(fr_) ** 3 * F(fm))), float(F(fr_)) ** 1.5, float(F(fr_)) ** 3 / float(F(fm)), v * 2)])
        return dict(q=q, o=o, a=a, sol=['T^{2} = \\f{4π^{2}r^{3}}{GM} → T ∝ √{\\f{r^{3}}{M}}.', f'= √{{\\f{{({fr(fr_)})^{{3}}}}{{{fr(fm)}}}}} ≈ {nf(v, 3)}.'], p=dict(t='kep', fm=str(fm), fr=str(fr_)))
    if t == 'E':
        m = rng.choice([50, 100, 150, 200, 300, 400, 500, 600, 1000, 1200]); r1, r2 = rng.choice([(F(3, 2), 3), (2, 4), (2, 3), (2, 6), (1, 2), (1, 3), (3, 6), (1, 4), (4, 8), (2, 8)])
        dE = 10 * 6e6 * m / 2 * float(1 / F(r1) - 1 / F(r2))
        q = f'A {m} kg satellite moves from a circular orbit of radius {fr(r1)}R to one of radius {fr(r2)}R (R = 6 × 10^{{6}} m, g = 10 m s^{{−2}}). Energy needed is ______ × 10^{{6}} J.'
        v = dE / 1e6
        if abs(v - round(v)) > 1e-6: return g_orbit(rng)
        return dict(q=q, o=None, a=round(v), sol=['E = −\\f{GMm}{2r} with GM = gR^{2}.', f'ΔE = \\f{{gRm}}{{2}}(\\f{{1}}{{{fr(r1)}}} − \\f{{1}}{{{fr(r2)}}}) = {round(v)} × 10^{{6}} J.'], p=dict(t='E', m=m, r1=str(r1), r2=str(r2)))
    if t == 'L':
        fm, fr_ = rng.choice([2, 3, 4, 5, 6, F(1, 2), F(1, 3)]), rng.choice([4, 9, F(1, 4), 16, F(1, 9), 25])
        v = float(F(fm)) * math.sqrt(float(F(fr_)))
        q = f'Planet B has {fr(fm)} times the mass of planet A and orbits the same star at {fr(fr_)} times A\'s radius. L_{{B}}/L_{{A}} is :'
        o, a = mcq(rng, nf(v, 3), [nf(x, 3) for x in (float(F(fm)) * float(F(fr_)), float(F(fm)) / math.sqrt(float(F(fr_))), math.sqrt(float(F(fm) * F(fr_))), v * 2)])
        return dict(q=q, o=o, a=a, sol=['L = mvr = m√{GMr}.', f'= {fr(fm)} × √{{{fr(fr_)}}} = {nf(v, 3)}.'], p=dict(t='L', fm=str(fm), fr=str(fr_)))
    if t == 'geo':
        T = rng.choice([3, 6, 8, 12, 16, 36, 48, 72]); fm = rng.choice([F(1, 4), 4, 2, F(1, 2), 1, 8, F(1, 8), 3]); r0 = 4.2e4
        r = r0 * (float(fm) * (T / 24) ** 2) ** (1 / 3)
        q = f'A "stationary" satellite of a planet ({fr(fm)} × earth\'s mass) has period {T} h. Earth\'s geostationary orbit radius is 4.2 × 10^{{4}} km. The planet\'s orbit radius is about :'
        o, a = mcq(rng, nf(r, 3) + ' km', [nf(x, 3) + ' km' for x in (r * 2, r / 2, r0 * float(fm) * T / 24, r * 1.5)])
        return dict(q=q, o=o, a=a, sol=['r^{3} ∝ MT^{2}.', f'r = 4.2 × 10^{{4}} × ({fr(fm)} × ({T}/24)^{{2}})^{{1/3}} ≈ {nf(r, 3)} km.'], p=dict(t='geo', T=T, fm=str(fm)))
    p_ = rng.choice([1, 2, 3, 4, 5, 6, 0.5, 1.5, 2.5]); v = 1.5 * p_
    q = f'If a satellite\'s orbit radius increases by {p_} %, its period increases by about :'
    o, a = mcq(rng, f'{nf(v)} %', [f'{nf(x)} %' for x in (p_, 2 * p_, p_ / 2, 3 * p_)])
    return dict(q=q, o=o, a=a, sol=['T ∝ r^{3/2} → \\f{ΔT}{T} ≈ \\f{3}{2}\\f{Δr}{r}.', f'= {nf(v)} %.'], p=dict(t='pct', p=p_))

def robust(gf):
    def w(rng):
        for _ in range(80):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(law=g_law, gvar=g_gvar, escape=g_escape, orbit=g_orbit).items()}
def finish(it): return it

# ---------------- independent checks: explicit G, M, R numbers and numerical integration ----------------
def unf(s):
    s = s.replace('−', '-').strip()
    if s.startswith('\\f{') or s.startswith('-\\f{'): neg = s.startswith('-'); a, b = s.lstrip('-')[3:-1].split('}{'); v = F(int(a), int(b)); return -v if neg else v
    return F(s)
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0].rstrip('v%'))
def gsurf(M, R): return G * M / R ** 2
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'ratio':
        gS = gsurf(ME, RE); f = G * ME * p['m'] / ((1 + p['k']) * RE) ** 2 * 10 / gS; return abs(num(Rv) - f) < 1e-3 * f
    if t == 'scale':   # integrate the fall of 3 bodies (radial, by symmetry) for both settings and compare
        def tcol(a, m):
            r, v, dt, tt = a / math.sqrt(3), 0.0, 1e-4, 0.0
            while r > a / math.sqrt(3) * 0.02:
                acc = -m / (math.sqrt(3) * r * r)   # pull of the other two, resolved toward the centre (G = 1)
                v += acc * dt; r += v * dt; tt += dt
            return tt
        k = tcol(float(F(p['fa'])), float(F(p['fm']))) / tcol(1.0, 1.0); return abs(Rv - p['T0'] * k) < 0.02 * Rv
    if t == 'two':
        x = num(Rv); lo, hi = 1e-9, p['d'] - 1e-9
        for _ in range(100):
            m = (lo + hi) / 2
            if p['m1'] / m ** 2 > p['m2'] / (p['d'] - m) ** 2: lo = m
            else: hi = m
        return abs(x - lo) < 0.006 * lo
    if t == 'zero':
        fx = sum(math.cos(2 * math.pi * k / p['n']) for k in range(p['n'])); fy = sum(math.sin(2 * math.pi * k / p['n']) for k in range(p['n'])); return Rv == 'zero' and abs(fx) + abs(fy) < 1e-9
    if t == 'h': h = float(F(p['k'])) * RE; return abs(float(unf(Rv)) - gsurf(ME, RE + h) / gsurf(ME, RE)) < 1e-9
    if t == 'd':   # shell theorem: mass inside ∝ r³
        r = RE * (1 - float(F(p['f']))); return abs(float(unf(Rv)) - G * ME * (r / RE) ** 3 / r ** 2 / gsurf(ME, RE)) < 1e-9
    if t == 'shape': return abs(float(unf(Rv)) - gsurf(ME * float(F(p['fm'])), RE * float(F(p['fr']))) / gsurf(ME, RE)) < 1e-9
    if t == 'pend': gp = math.pi ** 2 * (RE / (RE * (1 + p['k']))) ** 2; return Rv == round(2 * math.pi * math.sqrt(p['L'] / gp))
    if t == 'hfor':
        lo, hi = 0.0, 10.0
        for _ in range(80):
            m = (lo + hi) / 2
            if 1 / (1 + m) ** 2 > 1 / p['n']: lo = m
            else: hi = m
        return Rv == round(lo)
    if t == 'small':
        d = p['h'] * 1000; gd = G * ME * ((RE - d) / RE) ** 3 / (RE - d) ** 2; gh = G * ME / (RE + d) ** 2; return abs(num(Rv) - 100 * (gd - gh) / gsurf(ME, RE)) < 0.05 * num(Rv) + 1e-4
    if t == 'eratio': v = math.sqrt(2 * G * ME * float(F(p['fm'])) / (RE * float(F(p['fr'])))) / math.sqrt(2 * G * ME / RE) * 11.2; return abs(num(Rv) - v) < 0.006 * v
    if t == 'dens':
        R1, rho1 = 1.0, 1.0; R2, rho2 = float(F(p['fr'])), float(F(p['fd'])); v = math.sqrt(R2 ** 3 * rho2 / R2) / math.sqrt(R1 ** 3 * rho1 / R1); return abs(num(Rv) - v) < 0.006 * v
    if t == 'from': r = 1 + p['k']; return Rv == f'√{{\\f{{2GM}}{{{r}R}}}}'
    if t == 'energy':   # integrate F dr from R to R + h
        h = float(F(p['k'])); n = 20000; s = sum(1 / (1 + (i + 0.5) * h / n) ** 2 * h / n for i in range(n)); return abs(float(unf(Rv)) - s) < 1e-6
    if t == 'fall':
        n = 200000; W = sum(G * ME * p['m'] / (RE * (1 + 1e3 * (i + 0.5) / n)) ** 2 * RE * 1e3 / n for i in range(n)); K = W * g0 / gsurf(ME, RE)
        return abs(num(Rv) - K) < 0.01 * K
    if t == 'work':
        ms = p['ms']; U = lambda a: -6.7e-11 * (ms[0] * ms[1] + ms[1] * ms[2] + ms[0] * ms[2]) / a; W = U(p['a2']) - U(p['a1']); return abs(num(Rv) - W) < 0.006 * W
    if t == 'v': v = p['v0'] * math.sqrt(G * ME / RE) / math.sqrt(G * ME / (RE * float(F(p['k'])))); return abs(num(Rv) - v) < 0.006 * v
    if t == 'T': return Rv == round(p['T0'] * math.sqrt(float(F(p['f'])) ** 3))
    if t == 'kep':
        T = lambda r, M: 2 * math.pi * math.sqrt(r ** 3 / (G * M)); v = T(RE * float(F(p['fr'])), ME * float(F(p['fm']))) / T(RE, ME); return abs(num(Rv) - v) < 0.006 * v
    if t == 'E':
        gR2 = 10 * 6e6 ** 2; E = lambda r: -gR2 * p['m'] / (2 * r * 6e6); return Rv == round((E(float(F(p['r2']))) - E(float(F(p['r1'])))) / 1e6)
    if t == 'L': v = float(F(p['fm'])) * math.sqrt(G * ME * float(F(p['fr'])) * RE) / math.sqrt(G * ME * RE); return abs(num(Rv) - v) < 0.006 * v
    if t == 'geo':
        Tsec = p['T'] * 3600; M = 6e24 * float(F(p['fm'])); r0 = (G * 6e24 * (24 * 3600) ** 2 / (4 * math.pi ** 2)) ** (1 / 3); r = (G * M * Tsec ** 2 / (4 * math.pi ** 2)) ** (1 / 3) / r0 * 4.2e4
        return abs(num(Rv) - r) < 0.006 * r
    if t == 'pct': return abs(num(Rv) - 100 * ((1 + p['p'] / 100) ** 1.5 - 1)) < 0.1 * num(Rv)
    raise KeyError(t)
