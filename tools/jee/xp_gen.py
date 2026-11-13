"""Practice generators — Physics Unit 20: Experimental Skills. check() re-does each experiment another way:
instrument readings by building the scales and finding the coinciding mark, error bounds by pushing every input to
its extremes, bridges by bisection on the balance point, and the pendulum/fall/resonance by direct simulation."""
import math, re
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def isint(x): return abs(x - round(x)) < 1e-9
def opts(rng, v, k=(2, 0.5, 1.5, 0.75, 10, 0.1)):
    w = []
    for f in k:
        s = nf(v * f, 3)
        if s != nf(v, 3) and s not in w: w.append(s)
    rng.shuffle(w); return mcq(rng, nf(v, 3), w)

def g_meas(rng):
    t = rng.choice(['v_lc', 'v_read', 's_read', 'e_pow', 'e_g', 'sf'])
    if t == 'v_lc':
        msd, N = rng.choice([1, 0.5, 0.1]), rng.choice([10, 20, 25, 50]); m = N - 1; lc = msd * (N - m) / N
        o, an = opts(rng, lc, (2, 0.5, 10, N / (N - m) if N != m else 3))
        return dict(q=f'In a vernier callipers, {N} vernier divisions coincide with {m} main-scale divisions of {msd} mm each. The least count (in mm) is', o=o, a=an,
                    sol=['LC = 1 MSD − 1 VSD.', f'= {msd} − \\f{{{m} × {msd}}}{{{N}}} = {nf(lc, 3)} mm.'], p=dict(t=t, msd=msd, N=N, m=m))
    if t == 'v_read':
        lc, ms, vc, z = 0.1, rng.choice([12, 15, 21, 30, 45]), rng.randint(0, 9), rng.choice([-3, -2, 0, 2, 3, 4]); L = ms + vc * lc - z * lc
        right = f'{L:.1f}'; w = list(dict.fromkeys(f'{x:.1f}' for x in (ms + vc * lc + z * lc, ms + vc * lc, ms + vc + 0.0 if vc < 10 else ms + 1, L + 1)))
        w = [x for x in w if x != right][:3]; need(len(w) == 3); o, an = mcq(rng, right, w)
        ztxt = 'no zero error' if z == 0 else f'a zero error of {"+" if z > 0 else "−"}{abs(z)} divisions'
        return dict(q=f'A vernier callipers (LC 0.1 mm) has {ztxt}. Main scale reads {ms} mm and the {vc}th vernier division coincides. The corrected length (in mm) is', o=o, a=an,
                    sol=['Reading = MSR + VC × LC − zero error.', f'= {ms} + {nf(vc * lc, 2)} − ({nf(z * lc, 2)}) = {nf(L, 4)} mm.'], p=dict(t=t, ms=ms, vc=vc, z=z))
    if t == 's_read':
        pitch, N = rng.choice([0.5, 1.0]), rng.choice([50, 100]); lc = pitch / N; ls, cs, z = rng.randint(1, 8), rng.randint(0, N - 1), rng.choice([-5, -3, 0, 2, 4])
        d = ls * pitch + cs * lc - z * lc
        right = f'{d:.3f}'; w = list(dict.fromkeys(f'{x:.3f}' for x in (d + 2 * z * lc, ls * pitch + cs * lc, d + pitch, d - pitch / 2)))
        w = [x for x in w if x != right][:3]; need(len(w) == 3); o, an = mcq(rng, right, w)
        return dict(q=f'A screw gauge has pitch {pitch} mm and {N} circular divisions; its zero error is {z:+d} divisions. Linear scale shows {ls} divisions and circular scale {cs}. The diameter (in mm) is', o=o, a=an,
                    sol=[f'LC = \\f{{{pitch}}}{{{N}}} = {nf(lc, 2)} mm.', f'd = {ls} × {pitch} + {cs} × LC − ({z} × LC) = {nf(d, 4)} mm.'], p=dict(t=t, pitch=pitch, N=N, ls=ls, cs=cs, z=z))
    if t == 'e_pow':
        pw = [rng.choice([1, 2, 3, 0.5]) for _ in range(3)]; er = [rng.choice([0.5, 1, 1.5, 2, 3]) for _ in range(3)]; E = sum(a * b for a, b in zip(pw, er))
        o, an = opts(rng, E, (2, 0.5, 1.5, 0.75))
        expo = lambda p: '' if p == 1 else ('^{1/2}' if p == 0.5 else f'^{{{p}}}')
        return dict(q=f'Q = \\f{{a{expo(pw[0])} b{expo(pw[1])}}}{{c{expo(pw[2])}}}. If a, b, c carry {er[0]}%, {er[1]}% and {er[2]}% errors, the maximum percentage error in Q is', o=o, a=an,
                    sol=['Relative errors add, each times its power.', f'= {" + ".join(f"{nf(a, 2)} × {b}" for a, b in zip(pw, er))} = {nf(E, 3)}%.'], p=dict(t=t, pw=pw, er=er))
    if t == 'e_g':
        L, dL, n, tt, dt = rng.choice([20, 50, 80, 100]), rng.choice([0.1, 0.2, 0.5]), rng.choice([10, 20, 50, 100]), rng.choice([20, 40, 50, 90, 100]), rng.choice([0.5, 1.0])
        E = (dL / L + 2 * dt / tt) * 100
        o, an = opts(rng, E, (2, 0.5, 1.5, 0.75))
        return dict(q=f'A pendulum length is {L} cm (±{dL} cm); {n} oscillations take {tt} s (±{dt} s). The maximum percentage error in g is', o=o, a=an,
                    sol=['g = \\f{4π^{2}L}{T^{2}} → \\f{Δg}{g} = \\f{ΔL}{L} + 2\\f{ΔT}{T}.', f'= {nf(dL / L * 100, 3)}% + {nf(2 * dt / tt * 100, 3)}% = {nf(E, 3)}%.'], p=dict(t=t, L=L, dL=dL, n=n, tt=tt, dt=dt))
    a, b, cc = rng.choice([12.3, 32.3, 4.56, 7.8, 2.45]), rng.choice([1125, 2.5, 3.142, 41, 0.62]), rng.choice([27.4, 1.1, 9.8, 6.0, 3.33])
    s = lambda x: len(re.sub(r'^0+', '', x.replace('.', '')).rstrip('0')) if '.' not in x else len(re.sub(r'^0+', '', x.replace('.', '')))
    n = min(s(str(a)), s(str(b)), s(str(cc))); y = a * b / cc; right = f'{y:.{n}g}'
    w = list(dict.fromkeys([f'{y:.{k}g}' for k in (n + 1, n + 2, n + 3, max(1, n - 1))] + [f'{y * 1.01:.{n}g}']))
    w = [x for x in w if x != right][:3]; need(len(w) == 3)
    o, an = mcq(rng, right, w)
    return dict(q=f'Report y = \\f{{{a} × {b}}}{{{cc}}} with the correct number of significant figures:', o=o, a=an,
                sol=['Keep the fewest significant figures among the factors.', f'{n} figures: {right}.'], p=dict(t='sf', a=a, b=b, c=cc, n=n))

def g_expt(rng):
    t = rng.choice(['b_bal', 'p_ratio', 'p_int', 'vi', 'cap', 'stokes', 'pend', 'res'])
    if t == 'b_bal':
        X, l = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15]), rng.choice([20, 25, 30, 40, 50, 60, 75]); R = X * (100 - l) / l
        o, an = opts(rng, R)
        return dict(q=f'In a metre bridge a {X} Ω resistor is in the left gap and an unknown R in the right gap. Balance is at {l} cm from the left. R (in Ω) is', o=o, a=an,
                    sol=['\\f{X}{R} = \\f{l}{100 − l}.', f'R = {nf(R, 3)} Ω.'], p=dict(t=t, X=X, l=l))
    if t == 'p_ratio':
        l1, l2 = rng.choice([200, 250, 300, 350, 400, 480]), rng.choice([150, 180, 200, 240, 300]); need(l1 != l2); r = l1 / l2
        o, an = opts(rng, r, (1 / r / r, 2, 0.5, 1.5))
        return dict(q=f'Two cells give balancing lengths {l1} cm and {l2} cm on a potentiometer. The ratio of their emfs E_{{1}}/E_{{2}} is', o=o, a=an, sol=['E ∝ balancing length.', f'= {nf(r, 3)}.'], p=dict(t=t, l1=l1, l2=l2))
    if t == 'p_int':
        R, l1, l2 = rng.choice([2, 5, 10, 20]), rng.choice([500, 600, 550, 400, 450]), rng.choice([400, 450, 500, 350, 300]); need(l1 > l2); r = R * (l1 - l2) / l2
        o, an = opts(rng, r)
        return dict(q=f'A potentiometer balances a cell at {l1} cm on open circuit and at {l2} cm when it is shunted by {R} Ω. The internal resistance (in Ω) is', o=o, a=an,
                    sol=['r = R(\\f{l_{1}}{l_{2}} − 1).', f'= {nf(r, 3)} Ω.'], p=dict(t=t, R=R, l1=l1, l2=l2))
    if t == 'vi':
        Rv, Req = rng.choice([5000, 10000, 20000]), rng.choice([1000, 2000, 2500, 4000]); need(Req < Rv); R = Req * Rv / (Rv - Req)
        o, an = opts(rng, R, (Req / R, 2, 0.5, 1.5))
        return dict(q=f'A voltmeter ({Rv} Ω) is across a resistor R and an ammeter measures the total current. The V/I readings give {Req} Ω. The true R (in Ω) is', o=o, a=an,
                    sol=['\\f{V}{I} = R ∥ R_{V}.', f'R = \\f{{R_{{eq}}R_{{V}}}}{{R_{{V}} − R_{{eq}}}} = {nf(R, 3)} Ω.'], p=dict(t=t, Rv=Rv, Req=Req))
    if t == 'cap':
        r1, r2 = rng.choice([0.2, 0.25, 0.3, 0.5]), rng.choice([0.1, 0.15, 0.4, 0.6]); need(r1 != r2); h = r2 / r1
        o, an = opts(rng, h, (1 / h / h, 2, 0.5, h))
        return dict(q=f'The same liquid rises in capillaries of radii {r1} mm and {r2} mm. The ratio of heights h_{{1}}/h_{{2}} is', o=o, a=an, sol=['h = \\f{2T cos θ}{ρgr} ∝ \\f{1}{r}.', f'\\f{{h_{{1}}}}{{h_{{2}}}} = \\f{{{r2}}}{{{r1}}} = {nf(h, 3)}.'], p=dict(t=t, r1=r1, r2=r2))
    if t == 'stokes':
        r1, r2 = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 5, 6]); need(r1 != r2); k = (r2 / r1) ** 2
        o, an = opts(rng, k, (r2 / r1, 2, 0.5, (r2 / r1) ** 3))
        return dict(q=f'Steel balls of radii {r1} mm and {r2} mm fall through the same glycerine. The ratio of the terminal speed of the second to the first is', o=o, a=an,
                    sol=['v_{t} = \\f{2r^{2}(ρ − σ)g}{9η} ∝ r^{2}.', f'= ({r2}/{r1})^{{2}} = {nf(k, 3)}.'], p=dict(t=t, r1=r1, r2=r2))
    if t == 'pend':
        L, T = rng.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0]), None; gtrue = rng.choice([9.6, 9.7, 9.8, 9.81]); T = 2 * math.pi * math.sqrt(L / gtrue); Tr = round(T, 2); g = 4 * math.pi ** 2 * L / Tr ** 2
        o, an = opts(rng, g, (1.1, 0.9, 1.05, 0.95))
        return dict(q=f'A pendulum of length {L} m has a measured period {Tr} s. The value of g (in m/s^{{2}}) from these data is', o=o, a=an, sol=['g = \\f{4π^{2}L}{T^{2}}.', f'= {nf(g, 3)} m/s^{{2}}.'], p=dict(t=t, L=L, T=Tr))
    f, l1 = rng.choice([256, 288, 320, 384, 480, 512]), rng.choice([15, 16, 17, 18, 20, 25, 30]); v = rng.choice([330, 340, 345, 350]); l1 = round((v / (4 * f)) * 100 - rng.choice([0.5, 1.0, 1.2]), 1); l2 = round(l1 + v / (2 * f) * 100, 1)
    vv = 2 * f * (l2 - l1) / 100
    o, an = opts(rng, vv, (2, 0.5, 1.05, 0.95))
    return dict(q=f'In a resonance-tube experiment with a {f} Hz fork, the first and second resonances occur at {l1} cm and {l2} cm. The speed of sound (in m/s) is', o=o, a=an,
                sol=['Successive resonances differ by \\f{λ}{2} (the end correction cancels).', f'v = 2f(l_{{2}} − l_{{1}}) = {nf(vv, 3)} m/s.'], p=dict(t='res', f=f, l1=l1, l2=l2))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(meas=g_meas, expt=g_expt).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'sf': return float(R) == float(f'{p["a"] * p["b"] / p["c"]:.{p["n"]}g}')
    V = num(R) if isinstance(R, str) else R
    if t == 'v_lc':   # lay out both scales and find the smallest gap between any vernier mark and the next main mark
        msd, N, m = p['msd'], p['N'], p['m']; vsd = m * msd / N
        gaps = [((k * vsd) // msd + 1) * msd - k * vsd for k in range(1, N)]; return close(V, min(g for g in gaps if g > 1e-12))
    if t == 'v_read':
        lc = 0.1; true = p['ms'] + p['vc'] * lc - p['z'] * lc
        vernier_zero = true + p['z'] * lc; return close(V, vernier_zero - p['z'] * lc, 1e-6)
    if t == 's_read':
        lc = p['pitch'] / p['N']; raw = p['ls'] * p['pitch'] + p['cs'] * lc; return close(V, raw - p['z'] * lc, 1e-6)
    if t == 'e_pow':
        pw, er = p['pw'], p['er']; Q = lambda a, b, c: a ** pw[0] * b ** pw[1] / c ** pw[2]
        worst = max(abs(Q(1 + s1 * er[0] / 100, 1 + s2 * er[1] / 100, 1 - s3 * er[2] / 100) - 1) for s1 in (-1, 1) for s2 in (-1, 1) for s3 in (-1, 1)) * 100
        return close(V, worst, 0.12)
    if t == 'e_g':
        g = lambda L, tt: 4 * math.pi ** 2 * L / (tt / p['n']) ** 2
        worst = max(abs(g(p['L'] + a * p['dL'], p['tt'] - b * p['dt']) - g(p['L'], p['tt'])) for a in (-1, 1) for b in (-1, 1)) / g(p['L'], p['tt']) * 100
        return close(V, worst, 0.1)
    if t == 'b_bal':
        lo, hi = 0.0, 100.0
        for _ in range(100):
            x = (lo + hi) / 2
            if p['X'] / V > x / (100 - x): lo = x
            else: hi = x
        return close(lo, p['l'], 3e-3)
    if t == 'p_ratio': return close(V, p['l1'] / p['l2'])
    if t == 'p_int':   # E = k l1; with shunt the terminal voltage E R/(R + r) = k l2
        r = V; return close(p['R'] / (p['R'] + r), p['l2'] / p['l1'])
    if t == 'vi': return close(V * p['Rv'] / (V + p['Rv']), p['Req'])
    if t == 'cap':
        T, rho, g = 0.072, 1000, 9.8; h = lambda r: 2 * T / (rho * g * r * 1e-3); return close(V, h(p['r1']) / h(p['r2']))
    if t == 'stokes':
        def vt(r):
            r *= 1e-3; m = 7800 * 4 / 3 * math.pi * r ** 3; v = 0.0
            for _ in range(20000): v += (m * 9.8 * (1 - 1260 / 7800) - 6 * math.pi * 1.5 * r * v) / m * 2e-5
            return v
        return close(V, vt(p['r2']) / vt(p['r1']), 2e-3)
    if t == 'pend':
        g = V; th, w, tt, dt, times, prev = 0.01, 0.0, 0.0, 1e-4, [], 0.01
        while len(times) < 3:   # one full period lies between the 1st and 3rd zero crossings
            w += -g / p['L'] * math.sin(th) * dt; th += w * dt; tt += dt
            if (prev > 0 >= th) or (prev < 0 <= th): times.append(tt)
            prev = th
        return close(times[2] - times[0], p['T'], 3e-3)
    if t == 'res': lam = 2 * (p['l2'] - p['l1']) / 100; return close(V, p['f'] * lam)
    raise KeyError(t)
