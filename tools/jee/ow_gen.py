"""Practice generators — Physics Unit 10: Oscillations and Waves. check() re-solves each item independently: SHM by
stepping x'' = −ω²x in time, springs from the force balance, superposition by adding complex phasors, pipes and
strings by listing their allowed modes and searching for the match."""
import math, cmath
from common import mcq, nf
G = 10.0
def need(x):
    if not x: raise AssertionError('retry')
def half(x): need(abs(x % 1 - 0.5) > 0.03)
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-9)
def bisect(f, lo, hi, n=200):
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(lo) > 0) == (f(m) > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
def step(w, x0, v0, T, dt=2e-4):
    x, v, t = x0, v0, 0.0
    while t < T - 1e-12:
        a = -w * w * x; x += v * dt + 0.5 * a * dt * dt; v += 0.5 * (a - w * w * x) * dt; t += dt
    return x, v
def track(w, x0, v0, T, dt=2e-4):   # one pass: largest |x| and |v| seen up to time T
    x, v, t, mx, mv = x0, v0, 0.0, abs(x0), abs(v0)
    while t < T - 1e-12:
        a = -w * w * x; x += v * dt + 0.5 * a * dt * dt; v += 0.5 * (a - w * w * x) * dt; t += dt; mx = max(mx, abs(x)); mv = max(mv, abs(v))
    return mx, mv
def modes(kind, v, L, n=60):   # allowed frequencies, in order (n-th entry = n-th mode)
    return [(2 * k - 1) * v / (4 * L) if kind == 'closed' else k * v / (2 * L) for k in range(1, n + 1)]

def g_shm(rng):
    t = rng.choice(['h_vmax', 'h_amax', 'h_xv', 'h_energy', 'h_time', 'h_add', 'h_new', 'h_v0'])
    if t == 'h_vmax':
        A, T = rng.choice([2, 3, 4, 5, 6, 8, 10]), rng.choice([0.5, 1, 1.57, 2, 3.14, 6.28]); v = A * 2 * math.pi / T; half(v * 10)
        return dict(q=f'A particle moves in SHM with amplitude {A} cm and period {T} s. Its maximum speed is ____ × 10^{{−1}} cm/s (nearest integer).', o=None, a=round(v * 10),
                    sol=['v_{max} = Aω = A\\f{2π}{T}.', f'≈ {nf(v, 4)} cm/s.'], p=dict(t=t, A=A, T=T))
    if t == 'h_amax':
        A, w = rng.choice([2, 3, 4, 5, 10]), rng.choice([2, 3, 4, 5, 10]); a = w * w * A
        return dict(q=f'x = {A} sin({w}t) cm describes an SHM. The largest acceleration is ____ cm/s^{{2}}.', o=None, a=a, sol=['a_{max} = ω^{2}A.', f'= {w * w} × {A} = {a} cm/s^{{2}}.'], p=dict(t=t, A=A, w=w))
    if t == 'h_xv':
        A, w = rng.choice([3, 4, 5, 6, 8, 10]), rng.choice([1, 2, 2.5, 3, 4]); x = rng.choice([1, 2, 3, 4, 5, 6]); need(x < A); v = w * math.sqrt(A * A - x * x); half(v * 10)
        return dict(q=f'An SHM has amplitude {A} cm and ω = {w} rad/s. At {x} cm from the centre the speed is ____ × 10^{{−1}} cm/s (nearest integer).', o=None, a=round(v * 10),
                    sol=['v = ω√{A^{2} − x^{2}}.', f'= {w}√{{{A * A - x * x}}} ≈ {nf(v, 4)} cm/s.'], p=dict(t=t, A=A, w=w, x=x))
    if t == 'h_energy':
        f = rng.choice([2, 3, 4, 5]); ask = rng.choice(['E/K', 'U/E', 'K/U']); x = 1 / f; U, K = x * x, 1 - x * x
        val = {'E/K': 1 / K, 'U/E': U, 'K/U': K / U}[ask]; right = nf(val, 4); o, a = mcq(rng, right, [nf(z, 4) for z in (1 / U, K, U / K, 1 - U, x)])
        txt = {'E/K': 'total energy : kinetic energy', 'U/E': 'potential energy : total energy', 'K/U': 'kinetic energy : potential energy'}[ask]
        return dict(q=f'When an SHM is at 1/{f} of its amplitude from the centre, the ratio {txt} is :', o=o, a=a,
                    sol=['U = ½kx^{2}, E = ½kA^{2}, K = E − U.', f'U/E = 1/{f * f} → ratio = {right}.'], p=dict(t=t, f=f, ask=ask))
    if t == 'h_time':
        T, frac = rng.choice([2, 3, 4, 5, 6, 8, 12]), rng.choice(['A/2', 'A/√2', '√3A/2', '0']); ang = {'A/2': math.pi / 3, 'A/√2': math.pi / 4, '√3A/2': math.pi / 6, '0': math.pi / 2}[frac]
        tt = ang / (2 * math.pi) * T; right = nf(tt, 4) + ' s'; o, a = mcq(rng, right, [nf(z, 4) + ' s' for z in (T / 4, T / 6, T / 8, T / 12, T / 3) if abs(z - tt) > 1e-9])
        return dict(q=f'An SHM of period {T} s starts at x = +A. The time to first reach x = {frac} is :', o=o, a=a,
                    sol=['x = A cos ωt.', f'ωt = {nf(ang / math.pi, 3)}π → t = {right}.'], p=dict(t=t, T=T, frac=frac))
    if t == 'h_add':
        a1, a2, ph, w = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 5]), rng.choice([0, 60, 90, 120, 180]), rng.choice([2, 3, 5]); R = abs(a1 + a2 * cmath.exp(1j * math.radians(ph))); need(R > 1e-9)
        val = w * w * R; half(val * 10)
        return dict(q=f'A particle takes part in x_{{1}} = {a1} sin {w}t cm and x_{{2}} = {a2} sin({w}t + {ph}°) cm at once. Its maximum acceleration is ____ × 10^{{−1}} cm/s^{{2}} (nearest integer).', o=None, a=round(val * 10),
                    sol=['Resultant amplitude: A^{2} = a_{1}^{2} + a_{2}^{2} + 2a_{1}a_{2}cosφ.', f'A ≈ {nf(R, 4)} cm → a_{{max}} = ω^{{2}}A ≈ {nf(val, 4)} cm/s^{{2}}.'], p=dict(t=t, a1=a1, a2=a2, ph=ph, w=w))
    if t == 'h_new':
        A, f, k = rng.choice([1, 2, 3]), rng.choice([(1, 3), (2, 3), (1, 2), (3, 4), (1, 4)]), rng.choice([2, 3, 4]); x = A * f[0] / f[1]
        An = math.sqrt(x * x + k * k * (A * A - x * x)); r = An / A; half(r * 100)
        return dict(q=f'In an SHM of amplitude A, the speed is suddenly made {k} times larger when x = {f[0]}A/{f[1]}. The new amplitude is ____ × 10^{{−2}} A (nearest integer).', o=None, a=round(r * 100),
                    sol=['v^{2} = ω^{2}(A^{2} − x^{2}); after the kick v\' = kv, same ω.', f'A\'^{{2}} = x^{{2}} + k^{{2}}(A^{{2}} − x^{{2}}) → A\' ≈ {nf(r, 4)}A.'], p=dict(t=t, A=A, f=f, k=k))
    A, T, ph = rng.choice([2, 5, 10, 20]), rng.choice([3.14, 6.28, 1.57]), rng.choice([0, 30, 45, 60, 90])
    w = 2 * math.pi / T; v = A * w * math.cos(math.radians(ph)); half(v * 10)
    return dict(q=f'x = {A} sin(ωt + {ph}°) m with period {T} s. The velocity at t = 0 is ____ × 10^{{−1}} m/s (nearest integer).', o=None, a=round(v * 10),
                sol=['v = Aω cos(ωt + φ).', f'ω = {nf(w, 4)} rad/s → v(0) ≈ {nf(v, 4)} m/s.'], p=dict(t='h_v0', A=A, T=T, ph=ph))

def g_osc(rng):
    t = rng.choice(['o_spring', 'o_pend', 'o_comb', 'o_cut', 'o_count', 'o_mass'])
    if t == 'o_spring':
        m, k = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 2]), rng.choice([10, 20, 40, 50, 100, 200]); T = 2 * math.pi * math.sqrt(m / k); half(T * 100)
        return dict(q=f'A {m} kg block on a spring of k = {k} N/m oscillates. Its period is ____ × 10^{{−2}} s (nearest integer).', o=None, a=round(T * 100),
                    sol=['T = 2π√{\\f{m}{k}}.', f'≈ {nf(T, 4)} s.'], p=dict(t=t, m=m, k=k))
    if t == 'o_pend':
        L, gf = rng.choice([0.25, 0.5, 1, 1.5, 2, 4]), rng.choice([1, 0.25, 4, 1 / 6]); T = 2 * math.pi * math.sqrt(L / (9.8 * gf)); half(T * 100)
        where = {1: 'on Earth (g = 9.8)', 0.25: 'where g is a quarter of 9.8', 4: 'where g is 4 × 9.8', 1 / 6: 'on the Moon (g = 9.8/6)'}[gf]
        return dict(q=f'A simple pendulum {L} m long swings {where}. Its period is ____ × 10^{{−2}} s (nearest integer).', o=None, a=round(T * 100),
                    sol=['T = 2π√{\\f{L}{g}}.', f'≈ {nf(T, 4)} s.'], p=dict(t=t, L=L, gf=gf))
    if t == 'o_comb':
        k1, k2, kind = rng.choice([10, 20, 30, 40]), rng.choice([10, 20, 60, 80]), rng.choice(['series', 'parallel']); m = rng.choice([0.5, 1, 2])
        ke = k1 + k2 if kind == 'parallel' else k1 * k2 / (k1 + k2); T = 2 * math.pi * math.sqrt(m / ke); half(T * 100)
        return dict(q=f'Springs of {k1} N/m and {k2} N/m are joined in {kind} and hold a {m} kg block. The period is ____ × 10^{{−2}} s (nearest integer).', o=None, a=round(T * 100),
                    sol=['Parallel: k = k_{1} + k_{2}; series: \\f{1}{k} = \\f{1}{k_{1}} + \\f{1}{k_{2}}.', f'k = {nf(ke, 4)} N/m → T ≈ {nf(T, 4)} s.'], p=dict(t=t, k1=k1, k2=k2, kind=kind, m=m))
    if t == 'o_cut':
        n = rng.choice([2, 3, 4, 9]); ask = rng.choice(['frequency', 'period'])
        val = math.sqrt(n) if ask == 'frequency' else 1 / math.sqrt(n); right = nf(val, 4); o, a = mcq(rng, right, [nf(z, 4) for z in (n, 1 / n, 1 / val, val * 2) if abs(z - val) > 1e-9])
        return dict(q=f'A spring is cut to 1/{n} of its length and the same mass hung from one piece. New {ask} : old {ask} =', o=o, a=a,
                    sol=['k × length is fixed → k becomes n times.', f'f ∝ √{{k}} → ratio = {right}.'], p=dict(t=t, n=n, ask=ask))
    if t == 'o_count':
        L, n1, n2 = rng.choice([20, 30, 40, 60, 80, 120]), rng.choice([10, 20, 30]), rng.choice([10, 20, 40, 60]); need(n1 != n2); L2 = L * (n1 / n2) ** 2; half(L2 * 10)
        return dict(q=f'A {L} cm pendulum makes {n1} swings in a certain time. To make {n2} swings in the same time its length must be ____ × 10^{{−1}} cm (nearest integer).', o=None, a=round(L2 * 10),
                    sol=['f ∝ \\f{1}{√{L}} → L ∝ \\f{1}{f^{2}}.', f'L = {L} × ({n1}/{n2})^{{2}} ≈ {nf(L2, 4)} cm.'], p=dict(t=t, L=L, n1=n1, n2=n2))
    k = rng.choice([4, 9, 16, 25, 1 / 4, 1 / 9]); r = 1 / math.sqrt(k)
    right = nf(r, 4); o, a = mcq(rng, right, [nf(z, 4) for z in (k, 1 / k, math.sqrt(k), r * 2) if abs(z - r) > 1e-9])
    return dict(q=f'A mass m on a spring oscillates with frequency f. With a mass {nf(k, 3)}m on the same spring, the frequency becomes (in units of f) :', o=o, a=a,
                sol=['f ∝ \\f{1}{√{m}}.', f'→ {right}f.'], p=dict(t='o_mass', k=k))

def g_wave(rng):
    t = rng.choice(['w_speed', 'w_lambda', 'w_string', 'w_sum', 'w_int', 'w_temp', 'w_beat', 'w_dir'])
    if t == 'w_speed':
        w, k = rng.choice([50, 100, 120, 200, 300, 330, 600, 1000]), rng.choice([0.5, 1, 2, 2.5, 4, 5, 10]); v = w / k; need(abs(v - round(v)) < 1e-9)
        return dict(q=f'y = 0.02 sin({k}x − {w}t) (SI units). The wave speed is ____ m/s.', o=None, a=round(v), sol=['v = \\f{ω}{k}.', f'= \\f{{{w}}}{{{k}}} = {nf(v)} m/s.'], p=dict(t=t, w=w, k=k))
    if t == 'w_lambda':
        k = rng.choice([0.01, 0.012, 0.015, 0.018, 0.02, 0.025, 0.03, 0.05, 0.1, 0.2, 0.25]); lam = 2 * math.pi / k; half(lam)
        return dict(q=f'y = 3 sin(40t − {k}x) with x in cm. The distance between successive crests is ____ cm (nearest integer).', o=None, a=round(lam),
                    sol=['Successive crests are λ apart; λ = \\f{2π}{k}.', f'≈ {nf(lam, 5)} cm.'], p=dict(t=t, k=k))
    if t == 'w_string':
        T, mu = rng.choice([10, 16, 20, 40, 50, 80, 100, 120]), rng.choice([0.001, 0.002, 0.004, 0.005, 0.01, 0.02]); v = math.sqrt(T / mu); half(v)
        return dict(q=f'A string with linear density {mu} kg/m is under {T} N tension. A transverse wave travels on it at ____ m/s (nearest integer).', o=None, a=round(v),
                    sol=['v = √{\\f{T}{μ}}.', f'≈ {nf(v, 5)} m/s.'], p=dict(t=t, T=T, mu=mu))
    if t == 'w_sum':
        a1, a2, ph = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4]), rng.choice([60, 90, 120]); z = a1 + a2 * cmath.exp(1j * math.radians(ph)); R = abs(z); half(R * 100)
        return dict(q=f'Waves y_{{1}} = {a1} sin(kx − ωt) and y_{{2}} = {a2} sin(kx − ωt + {ph}°) superpose. The resultant amplitude is ____ × 10^{{−2}} (nearest integer).', o=None, a=round(R * 100),
                    sol=['A^{2} = a_{1}^{2} + a_{2}^{2} + 2a_{1}a_{2}cosφ.', f'A ≈ {nf(R, 4)}.'], p=dict(t=t, a1=a1, a2=a2, ph=ph))
    if t == 'w_int':
        r, ph = rng.choice([4, 9, 16, 25]), rng.choice([60, 90, 120, 0]); s = math.sqrt(r); I2 = 1 + r + 2 * s * math.cos(math.radians(ph)); I1 = 1 + r; val = I2 / I1
        right = nf(val, 4); o, a = mcq(rng, right, [nf(z, 4) for z in (1 / val, (1 + s) ** 2 / I1, (s - 1) ** 2 / I1, 1) if abs(z - val) > 1e-9])
        return dict(q=f'Two waves of intensity ratio 1 : {r} meet. (Intensity when coherent with phase difference {ph}°) : (intensity when incoherent) =', o=o, a=a,
                    sol=['Coherent: I = I_{1} + I_{2} + 2√{I_{1}I_{2}}cosφ; incoherent: I_{1} + I_{2}.', f'= \\f{{{nf(I2, 4)}}}{{{nf(I1)}}} = {right}.'], p=dict(t=t, r=r, ph=ph))
    if t == 'w_temp':
        f = rng.choice([2, 3, 1.5, 1.2, 1.1, 2.5]); T0 = rng.choice([0, 27, -73, 127, 77]); Tn = (T0 + 273) * f * f - 273; need(abs(Tn - round(Tn)) < 1e-6)
        return dict(q=f'The speed of sound in air becomes {f} times as the temperature rises from {T0} °C. The new temperature is ____ °C.', o=None, a=round(Tn),
                    sol=['v ∝ √{T} (kelvin).', f'T = {T0 + 273} × {nf(f * f)} − 273 = {nf(Tn)} °C.'], p=dict(t=t, f=f, T0=T0))
    if t == 'w_beat':
        w1, w2 = rng.choice([(49, 52), (98, 102), (60, 64), (30, 33), (100, 106)]); Tb = 2 * math.pi / (w2 - w1)
        right = nf(Tb, 3) + ' s'; o, a = mcq(rng, right, [nf(z, 3) + ' s' for z in (1 / (w2 - w1), 4 * math.pi / (w2 - w1), math.pi / (w2 - w1), 2 * math.pi / (w1 + w2))])
        return dict(q=f'x = a cos({nf((w2 - w1) / 2)}t) cos({nf((w1 + w2) / 2)}t) is the sum of two harmonic waves. The beat period is :', o=o, a=a,
                    sol=[f'= \\f{{a}}{{2}}[cos {w2}t + cos {w1}t].', f'Beat ω = {w2 - w1} → period \\f{{2π}}{{{w2 - w1}}} ≈ {right}.'], p=dict(t=t, w1=w1, w2=w2))
    k, w, sg = rng.choice([0.01, 0.02, 0.05, 0.1]), rng.choice([100, 200, 300, 600]), rng.choice(['+', '−']); v = w / k / 1000 * (-1 if sg == '+' else 1); need(abs(v * 10 - round(v * 10)) < 1e-9)
    right = f'{"−" if v < 0 else "+"}{nf(abs(v))} m/s'; o, a = mcq(rng, right, [f'{"+" if v < 0 else "−"}{nf(abs(v))} m/s', f'{"−" if v < 0 else "+"}{nf(abs(v) * 2)} m/s', f'{"−" if v < 0 else "+"}{nf(abs(v) / 2)} m/s', f'{"+" if v < 0 else "−"}{nf(abs(v) * 2)} m/s'])
    return dict(q=f'y = 4 sin({k}x {sg} {w}t) mm, with x in mm and t in s. The wave velocity (+ means along +x) is :', o=o, a=a,
                sol=['kx − ωt moves towards +x; kx + ωt moves towards −x. Speed = ω/k.', f'→ {right}.'], p=dict(t='w_dir', k=k, w=w, sg=sg))

def g_sound(rng):
    t = rng.choice(['s_pipe', 's_beats', 's_match', 's_water', 's_sono', 's_fork', 's_diff'])
    if t == 's_pipe':
        kind, L, n, v = rng.choice(['open', 'closed']), rng.choice([0.25, 0.5, 0.6, 0.75, 1, 1.5]), rng.choice([1, 2, 3]), rng.choice([330, 340])
        f = modes(kind, v, L)[n - 1]; half(f)
        word = {1: 'fundamental', 2: 'first overtone', 3: 'second overtone'}[n]
        return dict(q=f'The {word} of a {kind} pipe {L} m long (v = {v} m/s) has frequency ____ Hz (nearest integer).', o=None, a=round(f),
                    sol=['Open: f_{n} = \\f{nv}{2L}. Closed: only odd harmonics, \\f{(2n − 1)v}{4L}.', f'≈ {nf(f, 5)} Hz.'], p=dict(t=t, kind=kind, L=L, n=n, v=v))
    if t == 's_beats':
        L1, L2, b = rng.choice([0.5, 1, 1.5]), rng.choice([0.6, 1.2, 2, 3.5]), rng.choice([5, 7, 10, 15]); k1, k2 = rng.choice(['closed', 'open']), rng.choice(['closed', 'open'])
        f1, f2 = modes(k1, 1, L1)[0], modes(k2, 1, L2)[0]; need(abs(f1 - f2) > 1e-9); v = b / abs(f1 - f2); need(250 <= v <= 400); half(v)
        return dict(q=f'A {k1} pipe {L1} m long and a {k2} pipe {L2} m long, both in their fundamental, give {b} beats per second. The speed of sound is ____ m/s (nearest integer).', o=None, a=round(v),
                    sol=['Beat frequency = |f_{1} − f_{2}| with f = \\f{v}{4L} (closed) or \\f{v}{2L} (open).', f'v ≈ {nf(v, 5)} m/s.'], p=dict(t=t, L1=L1, L2=L2, b=b, k1=k1, k2=k2))
    if t == 's_match':
        n1, n2 = rng.choice([1, 3, 5, 7]), rng.choice([1, 2, 3, 4]); Lo = rng.choice([30, 40, 60, 90]); Lc = n1 * Lo / (2 * n2); need(abs(Lc * 10 - round(Lc * 10)) < 1e-9)
        return dict(q=f'The harmonic number {n1} of a closed pipe is in unison with harmonic number {n2} of an open pipe {Lo} cm long. The closed pipe is ____ × 10^{{−1}} cm long.', o=None, a=round(Lc * 10),
                    sol=['\\f{n_{1}v}{4L_{c}} = \\f{n_{2}v}{2L_{o}}.', f'L_{{c}} = \\f{{{n1} × {Lo}}}{{2 × {n2}}} = {nf(Lc)} cm.'], p=dict(t=t, n1=n1, n2=n2, Lo=Lo))
    if t == 's_water':
        f1, f2, A, v = rng.choice([30, 50, 55, 66, 110]), rng.choice([110, 150, 165, 220, 330]), rng.choice([1, 2, 5]), 330; need(f2 > f1)
        dL = v / (4 * f1) - v / (4 * f2); m = dL * 100 * A; half(m)
        return dict(q=f'A closed pipe (area {A} cm^{{2}}, v = 330 m/s) has fundamental {f1} Hz. Water is poured in until the fundamental is {f2} Hz. The water added is ____ g (nearest integer).', o=None, a=round(m),
                    sol=['L = \\f{v}{4f} before and after; the difference is the water column.', f'ΔL = {nf(dL * 100, 4)} cm → {nf(m, 4)} g.'], p=dict(t=t, f1=f1, f2=f2, A=A))
    if t == 's_sono':
        L, f1, f2 = rng.choice([30, 60, 90, 120]), rng.choice([200, 300, 400, 600]), rng.choice([300, 400, 500, 800]); need(f1 != f2); L2 = L * f1 / f2; half(L2 * 10)
        return dict(q=f'A sonometer wire resonates at {f1} Hz with {L} cm between the bridges. At the same tension, the length for {f2} Hz is ____ × 10^{{−1}} cm (nearest integer).', o=None, a=round(L2 * 10),
                    sol=['Same tension → same v; f ∝ \\f{1}{L}.', f'L = {L} × \\f{{{f1}}}{{{f2}}} ≈ {nf(L2, 4)} cm.'], p=dict(t=t, L=L, f1=f1, f2=f2))
    if t == 's_fork':
        fB, b, way = rng.choice([256, 320, 380, 400, 512]), rng.choice([2, 3, 4, 5, 6]), rng.choice(['wax', 'file']); fA = fB + b if way == 'wax' else fB - b
        return dict(q=f'Forks A and B give {b} beats per second; B is {fB} Hz. {"Loading A with wax" if way == "wax" else "Filing A"} makes the beats fewer. A\'s frequency was ____ Hz.', o=None, a=fA,
                    sol=['A = B ± beats. Wax lowers a fork\'s frequency; filing raises it.', f'Fewer beats means A moved towards B → A = {fA} Hz.'], p=dict(t=t, fB=fB, b=b, way=way))
    kind, n1, n2, d = rng.choice(['open', 'open', 'closed']), rng.choice([1, 2, 3]), rng.choice([3, 4, 5, 6]), rng.choice([550, 1100, 2200, 3300]); need(n2 > n1)
    fac = (n2 - n1) / 2 if kind == 'open' else (n2 - n1) / 2   # closed: modes (2n−1) → difference 2(n2−n1)·v/4L
    L = (n2 - n1) * 330 / (2 * d) if kind == 'open' else 2 * (n2 - n1) * 330 / (4 * d); mm = L * 1000; half(mm)
    word = 'harmonics' if kind == 'open' else 'allowed modes (odd harmonics)'
    return dict(q=f'In a {kind} pipe (v = 330 m/s) the {"" if kind == "open" else "allowed "}mode number {n2} and mode number {n1} differ by {d} Hz. The pipe is ____ mm long (nearest integer).', o=None, a=round(mm),
                sol=[f'Open: f_{{n}} = \\f{{nv}}{{2L}}. Closed: f = \\f{{(2n − 1)v}}{{4L}}.', f'L ≈ {nf(mm, 5)} mm.'], p=dict(t='s_diff', kind=kind, n1=n1, n2=n2, d=d))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(shm=g_shm, osc=g_osc, wave=g_wave, sound=g_sound).items()}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'h_vmax':
        w = 2 * math.pi / p['T']; v = track(w, p['A'], 0, p['T'], p['T'] / 20000)[1]; return abs(Rv - v * 10) <= 0.6
    if t == 'h_amax': return Rv == round(p['w'] ** 2 * track(p['w'], 0, p['A'] * p['w'], 2 * math.pi / p['w'], 1e-5)[0])
    if t == 'h_xv':
        E = 0.5 * p['w'] ** 2 * p['A'] ** 2; return Rv == round(math.sqrt(2 * (E - 0.5 * p['w'] ** 2 * p['x'] ** 2)) * 10)
    if t == 'h_energy':
        A, x = 1.0, 1 / p['f']; E = 0.5 * A * A; U = 0.5 * x * x; K = E - U; return close(num(Rv), {'E/K': E / K, 'U/E': U / E, 'K/U': K / U}[p['ask']], 1e-3)
    if t == 'h_time':
        w = 2 * math.pi / p['T']; tgt = {'A/2': 0.5, 'A/√2': 1 / math.sqrt(2), '√3A/2': math.sqrt(3) / 2, '0': 0}[p['frac']]; x, v, tt, dt = 1.0, 0.0, 0.0, 1e-5 * p['T']
        while x > tgt + 1e-12: a = -w * w * x; x += v * dt + 0.5 * a * dt * dt; v += 0.5 * (a - w * w * x) * dt; tt += dt
        return close(num(Rv), tt, 2e-3)
    if t == 'h_add':
        R = max(abs(p['a1'] * math.sin(p['w'] * s) + p['a2'] * math.sin(p['w'] * s + math.radians(p['ph']))) for s in [k * 2 * math.pi / p['w'] / 20000 for k in range(20000)]); return abs(Rv - p['w'] ** 2 * R * 10) <= 0.6
    if t == 'h_new':
        A = float(p['A']); x = A * p['f'][0] / p['f'][1]; w = 1.0; v = w * math.sqrt(A * A - x * x) * p['k']
        An = track(w, x, v, 2 * math.pi, 1e-4)[0]; return abs(Rv - An / A * 100) <= 0.6
    if t == 'h_v0':
        w = 2 * math.pi / p['T']; x = lambda s: p['A'] * math.sin(w * s + math.radians(p['ph'])); return Rv == round((x(1e-6) - x(-1e-6)) / 2e-6 * 10)
    if t == 'o_spring':
        w = math.sqrt(p['k'] / p['m']); return Rv == round(2 * math.pi / w * 100)
    if t == 'o_pend': return Rv == round(2 * math.pi / math.sqrt(9.8 * p['gf'] / p['L']) * 100)
    if t == 'o_comb':
        k1, k2 = p['k1'], p['k2']
        if p['kind'] == 'parallel': ke = k1 + k2
        else: x1 = bisect(lambda x: k1 * x - k2 * (1 - x), 0, 1); ke = k1 * x1 / 1.0   # unit stretch shared; the tension is the stiffness
        return Rv == round(2 * math.pi * math.sqrt(p['m'] / ke) * 100)
    if t == 'o_cut':
        k = 1.0 * p['n']; r = math.sqrt(k) if p['ask'] == 'frequency' else 1 / math.sqrt(k); return close(num(Rv), r, 1e-3)
    if t == 'o_count': return Rv == round(bisect(lambda L: 1 / math.sqrt(L) - (p['n2'] / p['n1']) / math.sqrt(p['L']), 1e-6, 1e4) * 10)
    if t == 'o_mass': return close(num(Rv), math.sqrt(1 / p['k']), 1e-3)
    if t == 'w_speed':
        # follow a crest: phase kx − ωt = π/2
        t1 = 0.37; x1 = (math.pi / 2 + p['w'] * t1) / p['k']; x0 = (math.pi / 2) / p['k']; return Rv == round((x1 - x0) / t1)
    if t == 'w_lambda':
        f = lambda x: math.sin(40 * 0.3 - p['k'] * x); d = next(i * 0.01 for i in range(50, 10 ** 6) if all(abs(f(x + i * 0.01) - f(x)) < 0.006 * p['k'] for x in (0.0, 1.3, 7.1)))   # smallest repeat distance
        return abs(Rv - d) <= 0.6
    if t == 'w_string': return Rv == round(math.sqrt(p['T'] / p['mu']))
    if t == 'w_sum':
        R = max(abs(p['a1'] * math.sin(s) + p['a2'] * math.sin(s + math.radians(p['ph']))) for s in [k * 2 * math.pi / 20000 for k in range(20000)]); return abs(Rv - R * 100) <= 0.6
    if t == 'w_int':
        a1, a2 = 1.0, math.sqrt(p['r']); I2 = abs(a1 + a2 * cmath.exp(1j * math.radians(p['ph']))) ** 2; return close(num(Rv), I2 / (a1 * a1 + a2 * a2), 1e-3)
    if t == 'w_temp': return Rv == round(bisect(lambda T: math.sqrt((T + 273) / (p['T0'] + 273)) - p['f'], p['T0'], 1e5))
    if t == 'w_beat':
        return close(num(Rv), 2 * math.pi / abs(p['w2'] - p['w1']), 3e-3)
    if t == 'w_dir':
        s = 1 if p['sg'] == '−' else -1; v = s * p['w'] / p['k'] / 1000; got = float(Rv.replace('−', '-').replace('+', '').split(' ')[0]); return abs(got - v) < 1e-9
    if t == 's_pipe': return Rv == round(modes(p['kind'], p['v'], p['L'])[p['n'] - 1])
    if t == 's_beats':
        v = bisect(lambda v: abs(modes(p['k1'], v, p['L1'])[0] - modes(p['k2'], v, p['L2'])[0]) - p['b'], 1, 2000); return Rv == round(v)
    if t == 's_match':
        f = modes('open', 1, p['Lo'])[p['n2'] - 1]; Lc = bisect(lambda L: p['n1'] / (4 * L) - f, 1e-3, 1e4); return Rv == round(Lc * 10)
    if t == 's_water':
        L1 = bisect(lambda L: modes('closed', 330, L)[0] - p['f1'], 1e-3, 100); L2 = bisect(lambda L: modes('closed', 330, L)[0] - p['f2'], 1e-3, 100); return Rv == round((L1 - L2) * 100 * p['A'])
    if t == 's_sono': return Rv == round(bisect(lambda L: p['f1'] * p['L'] / L - p['f2'], 0.1, 1e4) * 10)
    if t == 's_fork':
        for fA in (p['fB'] + p['b'], p['fB'] - p['b']):
            new = fA - 1 if p['way'] == 'wax' else fA + 1
            if abs(new - p['fB']) < p['b']: return Rv == fA
        return False
    if t == 's_diff':
        L = bisect(lambda L: (lambda m: m[p['n2'] - 1] - m[p['n1'] - 1])(modes(p['kind'], 330, L)) - p['d'], 1e-4, 100); return Rv == round(L * 1000)
    raise KeyError(t)
