"""Practice generators — Physics Unit 3: Laws of Motion. check() re-solves each item independently: connected bodies by
solving the Newton equations as a linear system, sliding by time-stepping, equilibrium by resolving components,
circular motion from the force balance written out afresh."""
import math
from common import mcq, nf
G = 10.0
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-9)
def lin(A, b):   # Gaussian elimination
    n = len(b); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def g_newton(rng):
    t = rng.choice(['catch', 'vec', 'lift', 'sand', 'vx', 'imp'])
    if t == 'catch':
        m, v, dt = rng.choice([0.1, 0.12, 0.15, 0.16, 0.2, 0.25]), rng.choice([10, 15, 20, 25, 30, 40]), rng.choice([0.05, 0.1, 0.2, 0.25, 0.5]); F = m * v / dt
        return dict(q=f'A ball of mass {int(m * 1000)} g moving at {v} m/s is caught and stopped in {dt} s. The average force on the hand is ____ N (nearest integer).', o=None, a=round(F),
                    sol=['F = \\f{Δp}{Δt}.', f'= \\f{{{m} × {v}}}{{{dt}}} = {nf(F, 4)} N.'], p=dict(t=t, m=m, v=v, dt=dt))
    if t == 'vec':
        m = rng.choice([1, 2, 4, 5]); F1 = [rng.randint(-6, 8) for _ in range(3)]; a = [rng.randint(-3, 3) for _ in range(3)]; F2 = [m * ai - fi for ai, fi in zip(a, F1)]; need(any(a))
        vec = lambda v: ' '.join(f'{"+ " if i and c >= 0 else ("− " if c < 0 else "")}{abs(c)}{u}' for i, (c, u) in enumerate(zip(v, ['î', 'ĵ', 'k̂'])))
        right = vec(a); o, a_ = mcq(rng, right, [vec([x * 2 for x in a]), vec([-x for x in a]), vec([x + 1 for x in a]), vec(F1)])
        return dict(q=f'A {m} kg body experiences F⃗_{{1}} = {vec(F1)} N and F⃗_{{2}} = {vec(F2)} N. Its acceleration (m/s^{{2}}) is :', o=o, a=a_, sol=['a⃗ = \\f{F⃗_{1} + F⃗_{2}}{m}.', f'= {right}.'], p=dict(t=t, m=m, F1=F1, F2=F2))
    if t == 'lift':
        m, a = rng.choice([40, 50, 60, 70, 80]), rng.choice([1, 2, 2.5, 3, 4, 5]); up = rng.choice([True, False]); R = m * (G + a) if up else m * (G - a)
        return dict(q=f'A person of mass {m} kg stands on a weighing machine in a lift accelerating {"upward" if up else "downward"} at {a} m/s^{{2}}. The machine reads ____ N (g = 10).', o=None, a=round(R),
                    sol=[f'N − mg = m(±a) → N = m(g {"+" if up else "−"} a).', f'= {m}(10 {"+" if up else "−"} {a}) = {nf(R)} N.'], p=dict(t=t, m=m, a=a, up=up))
    if t == 'sand':
        m, h, d = rng.choice([0.5, 1, 2, 4]), rng.choice([5, 10, 20, 45]), rng.choice([0.05, 0.1, 0.2, 0.25]); F = m * G * (h + d) / d
        return dict(q=f'A {m} kg ball falls from {h} m and stops after sinking {int(d * 100)} cm into sand. The average force of the sand is ____ N (nearest integer; g = 10).', o=None, a=round(F),
                    sol=['Work–energy from the release point: mg(h + d) = Fd.', f'F = \\f{{{m} × 10 × {nf(h + d)}}}{{{d}}} ≈ {nf(F, 5)} N.'], p=dict(t=t, m=m, h=h, d=d))
    if t == 'vx':
        m, k = rng.choice([0.2, 0.5, 1, 2, 4]), rng.choice([2, 3, 4, 5, 6]); F = m * k * k / 2; need(abs(F * 10 % 1 - 0.5) > 0.02)
        return dict(q=f'A {m} kg body moves along x with v = {k}√{{x}} m/s. The force on it is ____ × 10^{{−1}} N (nearest integer).', o=None, a=round(F * 10), sol=['a = v\\f{dv}{dx} = \\f{k^{2}}{2} (constant).', f'F = {m} × {nf(k * k / 2)} = {nf(F)} N.'], p=dict(t=t, m=m, k=k))
    m, F0, T = rng.choice([1, 2, 4, 5]), rng.choice([2, 4, 6, 10]), rng.choice([2, 3, 4, 5]); dv = F0 * T / 2 / m; need(abs(dv * 10 % 1 - 0.5) > 0.02)   # F rises linearly from 0 to F0 over T
    return dict(q=f'A force on a {m} kg body at rest grows uniformly from 0 to {F0} N in {T} s. The speed at t = {T} s is ____ × 10^{{−1}} m/s (nearest integer).', o=None, a=round(dv * 10),
                sol=['Impulse = area under F–t = ½F_{0}T = mΔv.', f'Δv = \\f{{{F0} × {T}}}{{2 × {m}}} = {nf(dv)} m/s.'], p=dict(t='imp', m=m, F0=F0, T=T))

def g_fric(rng):
    t = rng.choice(['slide', 'repose', 'pull', 'ratio', 'work', 'push'])
    if t == 'slide':
        th, mu = rng.choice([30, 37, 45, 53, 60]), rng.choice([0.1, 0.2, 0.25, 0.3, 0.5]); s, c = {37: (0.6, 0.8), 53: (0.8, 0.6)}.get(th, (math.sin(math.radians(th)), math.cos(math.radians(th))))
        a = G * (s - mu * c); need(a > 0)
        return dict(q=f'A block slides down a {th}° incline{" (sin 37° = 0.6)" if th in (37, 53) else ""} with μ_{{k}} = {mu}. Its acceleration is ____ × 10^{{−1}} m/s^{{2}} (nearest integer; g = 10).', o=None, a=round(a * 10),
                    sol=['a = g(sinθ − μ cosθ).', f'= 10({nf(s, 3)} − {mu} × {nf(c, 3)}) ≈ {nf(a, 3)} m s^{{−2}}.'], p=dict(t=t, s=s, c=c, mu=mu))
    if t == 'repose':
        th = rng.choice([30, 37, 45, 53, 60]); mu = {30: 1 / math.sqrt(3), 37: 0.75, 45: 1.0, 53: 4 / 3, 60: math.sqrt(3)}[th]
        o, a = mcq(rng, nf(mu, 3), [nf(x, 3) for x in (1 / mu, math.sin(math.radians(th)), math.cos(math.radians(th)), mu / 2)])
        return dict(q=f'A block just begins to slide when the incline is raised to {th}°{" (tan 37° = 3/4)" if th in (37, 53) else ""}. The coefficient of static friction is :', o=o, a=a, sol=['At the angle of repose μ_{s} = tanθ.', f'tan {th}° ≈ {nf(mu, 3)}.'], p=dict(t=t, th=th))
    if t == 'pull':
        m, mu, ang = rng.choice([5, 10, 20, 25, 40]), rng.choice([0.2, 0.25, 0.4, 0.5]), rng.choice([0, 30, 37, 45, 60]); c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        F = mu * m * G / (c + mu * s)
        return dict(q=f'A {m} kg box (μ = {mu}) is pulled at constant velocity by a force at {ang}° above the horizontal. The force is ____ N (nearest integer; g = 10).', o=None, a=round(F),
                    sol=['F cosθ = μ(mg − F sinθ) → F = \\f{μmg}{cosθ + μ sinθ}.', f'≈ {nf(F, 4)} N.'], p=dict(t=t, m=m, mu=mu, ang=ang))
    if t == 'ratio':
        th, n = rng.choice([30, 45, 60]), rng.choice([1.25, 1.5, 2, 2.5, 3]); mu = math.tan(math.radians(th)) * (1 - 1 / n ** 2)
        o, a = mcq(rng, nf(mu, 3), [nf(x, 3) for x in (math.tan(math.radians(th)) * (1 - 1 / n), 1 - 1 / n ** 2 if th != 45 else 1 - 1 / n, math.tan(math.radians(th)) / n ** 2, mu * 1.5)])
        return dict(q=f'Sliding down a rough {th}° incline takes {n} times as long as down an identical smooth one. μ_{{k}} is about :', o=o, a=a,
                    sol=['Same length: a_{rough} = \\f{a_{smooth}}{n^{2}}.', f'μ = tanθ(1 − \\f{{1}}{{n^{{2}}}}) ≈ {nf(mu, 3)}.'], p=dict(t=t, th=th, n=n))
    if t == 'work':
        m, mu, th, d = rng.choice([1, 2, 5]), rng.choice([0.1, 0.2, 0.25, 0.5]), rng.choice([0, 30, 60]), rng.choice([2, 5, 10, 20]); W = mu * m * G * math.cos(math.radians(th)) * d
        return dict(q=f'A {m} kg block moves {d} m {"along a horizontal floor" if th == 0 else f"up a {th}° incline"} with μ = {mu}. Work done against friction is ____ J (nearest integer; g = 10).', o=None, a=round(W),
                    sol=['f = μmg cosθ; W = f × d.', f'= {mu} × {m} × 10 × {nf(math.cos(math.radians(th)), 3)} × {d} ≈ {nf(W, 4)} J.'], p=dict(t=t, m=m, mu=mu, th=th, d=d))
    m, mu, th = rng.choice([1, 2, 5, 10]), rng.choice([0.1, 0.2, 0.25]), rng.choice([30, 37, 53]); s, c = {37: (0.6, 0.8), 53: (0.8, 0.6)}.get(th, (0.5, math.sqrt(3) / 2))
    F = m * G * (s + mu * c)
    return dict(q=f'Minimum force parallel to a {th}° incline{" (sin 37° = 0.6)" if th != 30 else ""} needed to push a {m} kg block UP at constant speed (μ = {mu}) is ____ N (nearest integer; g = 10).', o=None, a=round(F),
                sol=['Pushing up: F = mg(sinθ + μ cosθ) (friction now points down the slope).', f'≈ {nf(F, 4)} N.'], p=dict(t='push', m=m, mu=mu, s=s, c=c))

def g_pulley(rng):
    t = rng.choice(['atw', 'atwT', 'table', 'train', 'eq', 'ratio'])
    if t in ('atw', 'atwT'):
        m1, m2 = rng.sample([1, 2, 3, 4, 5, 6, 8, 10], 2); a = abs(m1 - m2) * G / (m1 + m2); T = 2 * m1 * m2 * G / (m1 + m2)
        if t == 'atw':
            o, a_ = mcq(rng, f'{nf(a, 3)} m/s^{{2}}', [f'{nf(x, 3)} m/s^{{2}}' for x in ((m1 + m2) * G / abs(m1 - m2) if m1 != m2 else 1, abs(m1 - m2) * G / max(m1, m2), G, a / 2)])
            return dict(q=f'Masses {m1} kg and {m2} kg hang over a smooth light pulley (Atwood machine). The acceleration is (g = 10) :', o=o, a=a_, sol=['a = \\f{(m_{2} − m_{1})g}{m_{1} + m_{2}}.', f'= \\f{{{abs(m1 - m2)} × 10}}{{{m1 + m2}}} ≈ {nf(a, 3)} m s^{{−2}}.'], p=dict(t=t, m1=m1, m2=m2))
        return dict(q=f'Masses {m1} kg and {m2} kg hang over a smooth light pulley. The string tension is ____ N (nearest integer; g = 10).', o=None, a=round(T), sol=['T = \\f{2m_{1}m_{2}g}{m_{1} + m_{2}}.', f'= {nf(T, 4)} N.'], p=dict(t=t, m1=m1, m2=m2))
    if t == 'table':
        M, m, mu = rng.choice([2, 4, 5, 8, 10, 20]), rng.choice([1, 2, 3, 4, 5, 6]), rng.choice([0, 0.1, 0.2, 0.25]); a = (m * G - mu * M * G) / (M + m); need(a > 0)
        return dict(q=f'A {M} kg block on a table (μ = {mu}) is tied over a smooth pulley at the edge to a hanging {m} kg block. The acceleration is ____ × 10^{{−1}} m/s^{{2}} (nearest integer; g = 10).', o=None, a=round(a * 10),
                    sol=['(M + m)a = mg − μMg.', f'a = \\f{{{m * 10} − {nf(mu * M * 10)}}}{{{M + m}}} ≈ {nf(a, 3)} m s^{{−2}}.'], p=dict(t=t, M=M, m=m, mu=mu))
    if t == 'train':
        ms = [rng.choice([1, 2, 3, 4, 5]) for _ in range(3)]; F = rng.choice([12, 18, 24, 30, 60, 80]); a = F / sum(ms); T1, T2 = ms[0] * a, (ms[0] + ms[1]) * a
        o, a_ = mcq(rng, f'{nf(T1, 3)} N, {nf(T2, 3)} N', [f'{nf(x, 3)} N, {nf(y, 3)} N' for x, y in ((T2, T1), (ms[2] * a, (ms[1] + ms[2]) * a), (T1 * 2, T2), (F / 3, 2 * F / 3))])
        return dict(q=f'Blocks of {ms[0]}, {ms[1]} and {ms[2]} kg lie in a line on a smooth floor joined by strings; {F} N pulls the last ({ms[2]} kg) block. The tensions in the first and second strings are :', o=o, a=a_,
                    sol=[f'a = \\f{{{F}}}{{{sum(ms)}}} m s^{{−2}}.', f'T_{{1}} = {ms[0]}a = {nf(T1, 3)} N; T_{{2}} = {ms[0] + ms[1]}a = {nf(T2, 3)} N.'], p=dict(t=t, ms=ms, F=F))
    if t == 'eq':
        a1, a2 = rng.choice([(30, 60), (60, 30), (45, 45), (37, 53), (53, 37), (30, 30), (60, 60)]); W = rng.choice([10, 20, 30, 50, 100])
        T1, T2 = lin([[math.cos(math.radians(a1)), -math.cos(math.radians(a2))], [math.sin(math.radians(a1)), math.sin(math.radians(a2))]], [0, W])
        return dict(q=f'A weight of {W} N hangs from two strings making {a1}° and {a2}° with the ceiling. The tension in the {a1}° string is ____ N (nearest integer).', o=None, a=round(T1),
                    sol=['Horizontal: T_{1}cosθ_{1} = T_{2}cosθ_{2}; vertical: T_{1}sinθ_{1} + T_{2}sinθ_{2} = W.', f'T_{{1}} ≈ {nf(T1, 4)} N.'], p=dict(t=t, a1=a1, a2=a2, W=W))
    k = rng.choice([2, 3, 4, 5, 6, 8, 10]); r = (k + 1) / (k - 1)
    o, a_ = mcq(rng, f'{k + 1} : {k - 1}', [f'{x}' for x in (f'{k} : 1', f'{k - 1} : {k + 1}', f'{k + 2} : {k - 2}' if k > 2 else '7 : 1', f'{2 * k} : 1')])
    return dict(q=f'Two blocks connected over a smooth pulley accelerate at g/{k}. The ratio of the heavier to the lighter mass is :', o=o, a=a_, sol=['\\f{m_{2} − m_{1}}{m_{2} + m_{1}} = \\f{1}{k}.', f'\\f{{m_{{2}}}}{{m_{{1}}}} = \\f{{k + 1}}{{k − 1}} = {k + 1} : {k - 1}.'], p=dict(t='mratio', k=k))

def g_circd(rng):
    t = rng.choice(['bank', 'bank0', 'string', 'vert', 'coin', 'drum'])
    if t in ('bank', 'bank0'):
        r, th = rng.choice([50, 100, 150, 200, 300, 400]), rng.choice([10, 15, 20, 30, 37, 45]); mu = rng.choice([0.1, 0.2, 0.25, 0.3]) if t == 'bank' else 0
        tn = 0.75 if th == 37 else math.tan(math.radians(th)); v = math.sqrt(r * G * (mu + tn) / (1 - mu * tn))
        return dict(q=f'A road of radius {r} m is banked at {th}°{" (tan 37° = 3/4)" if th == 37 else ""}{f" with μ = {mu}" if mu else " and is frictionless"}. The {"maximum" if mu else "safe"} speed is ____ m/s (nearest integer; g = 10).', o=None, a=round(v),
                    sol=['v^{2} = rg\\f{μ + tanθ}{1 − μ tanθ} (μ = 0 gives v^{2} = rg tanθ).', f'v ≈ {nf(v, 4)} m/s.'], p=dict(t=t, r=r, tn=tn, mu=mu))
    if t == 'string':
        m, L, T = rng.choice([0.1, 0.2, 0.25, 0.5, 1]), rng.choice([0.25, 0.5, 1, 2]), rng.choice([10, 20, 40, 50, 100, 200, 400]); w = math.sqrt(T / (m * L))
        return dict(q=f'A {m} kg ball on a {L} m string whirls in a horizontal circle (ignore gravity). If the string can bear {T} N, the maximum ω is ____ rad/s (nearest integer).', o=None, a=round(w),
                    sol=['T = mω^{2}L.', f'ω = √{{\\f{{{T}}}{{{m} × {L}}}}} ≈ {nf(w, 4)} rad/s.'], p=dict(t=t, m=m, L=L, T=T))
    if t == 'vert':
        m, r = rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([0.5, 1, 1.6, 2, 2.5]); ask = rng.choice(['vmin_top', 'vmin_bot', 'Tbot'])
        if ask == 'vmin_top': val = math.sqrt(G * r); unit = 'm/s (× 10^{−1})'; val10 = val * 10
        elif ask == 'vmin_bot': val = math.sqrt(5 * G * r); unit = 'm/s (× 10^{−1})'; val10 = val * 10
        else: val = 6 * m * G; unit = 'N (× 10^{−1})'; val10 = val * 10
        txt = {'vmin_top': 'the minimum speed at the TOP', 'vmin_bot': 'the minimum speed at the BOTTOM', 'Tbot': 'the tension at the bottom when it just completes the circle'}[ask]
        return dict(q=f'A {m} kg stone on a {r} m string moves in a vertical circle. Find {txt}: ____ {unit} (nearest integer; g = 10).', o=None, a=round(val10),
                    sol=['Just completing: T_{top} = 0 → v_{top} = √{gr}; energy → v_{bottom} = √{5gr}; T_{bottom} = mg + mv^{2}/r = 6mg.', f'→ {nf(val, 4)}.'], p=dict(t=t, m=m, r=r, ask=ask))
    if t == 'coin':
        mu, r = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 0.8]), rng.choice([0.05, 0.1, 0.2, 0.25, 0.4, 0.5]); w = math.sqrt(mu * G / r)
        return dict(q=f'A coin sits {int(r * 100)} cm from the centre of a turntable (μ = {mu}). The maximum ω without slipping is ____ × 10^{{−1}} rad/s (nearest integer; g = 10).', o=None, a=round(w * 10),
                    sol=['μmg = mω^{2}r → ω = √{μg/r}.', f'≈ {nf(w, 4)} rad/s.'], p=dict(t=t, mu=mu, r=r))
    r, w = rng.choice([1, 2, 2.5, 4, 5]), rng.choice([2, 4, 5, 8, 10]); mu = G / (w * w * r); need(mu < 1.5)
    o, a = mcq(rng, nf(mu, 3), [nf(x, 3) for x in (w * w * r / G, G / (w * r), mu * 2, mu / 2)])
    return dict(q=f'In a rotor of radius {r} m spinning at {w} rad/s a person stays pressed to the wall without falling. The minimum friction coefficient is :', o=o, a=a, sol=['N = mω^{2}r (inward); μN ≥ mg.', f'μ = \\f{{g}}{{ω^{{2}}r}} = {nf(mu, 3)}.'], p=dict(t='drum', r=r, w=w))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(newton=g_newton, fric=g_fric, pulley=g_pulley, circd=g_circd).items()}
def finish(it): return it
def slide_time(a, L, dt=1e-4):
    x = v = t = 0.0
    while x < L: x += (v + a * dt / 2) * dt; v += a * dt; t += dt
    return t
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'catch': return Rv == round(p['m'] * p['v'] / p['dt'])
    if t == 'vec':
        s = Rv.replace('− ', '-').replace('+ ', '').replace('î', ' ').replace('ĵ', ' ').replace('k̂', ' ').split(); got = [int(x) for x in s]
        return got == [(a + b) / p['m'] for a, b in zip(p['F1'], p['F2'])]
    if t == 'lift': return Rv == round(p['m'] * G + p['m'] * (p['a'] if p['up'] else -p['a']))
    if t == 'sand':   # two-stage: free fall then constant deceleration
        v2 = 2 * G * p['h']; dec = v2 / (2 * p['d']); return Rv == round(p['m'] * (dec + G))
    if t == 'vx':
        x = 1.7; v = lambda X: p['k'] * math.sqrt(X); a = v(x) * (v(x + 1e-6) - v(x - 1e-6)) / 2e-6; return Rv == round(p['m'] * a * 10)
    if t == 'imp':
        v = 0.0; dt = 1e-4; tt = 0.0
        while tt < p['T'] - 1e-12: v += (p['F0'] * (tt + dt / 2) / p['T']) / p['m'] * dt; tt += dt
        return Rv == round(v * 10)
    if t == 'slide':
        a = G * p['s'] - p['mu'] * G * p['c']; return Rv == round(a * 10)
    if t == 'repose':
        s_, c_ = {37: (0.6, 0.8), 53: (0.8, 0.6)}.get(p['th'], (math.sin(math.radians(p['th'])), math.cos(math.radians(p['th'])))); return close(num(Rv), s_ / c_, 0.003)   # 3-4-5 convention for 37°/53°
    if t == 'pull':
        th = math.radians(p['ang']); F = lin([[math.cos(th), -p['mu']], [math.sin(th), 1]], [0, p['m'] * G])[0]; return Rv == round(F)   # unknowns F, N
    if t == 'ratio':
        th = math.radians(p['th']); L = 2.0; ts = slide_time(G * math.sin(th), L); mu = num(Rv); tr = slide_time(G * (math.sin(th) - mu * math.cos(th)), L); return abs(tr / ts - p['n']) < 0.01 * p['n']
    if t == 'work': return Rv == round(p['mu'] * p['m'] * G * math.cos(math.radians(p['th'])) * p['d'])
    if t == 'push': return Rv == round(lin([[1, -p['mu']], [0, 1]], [p['m'] * G * p['s'], p['m'] * G * p['c']])[0])   # F − μN = mg sinθ, N = mg cosθ
    if t in ('atw', 'atwT'):
        m1, m2 = p['m1'], p['m2']; a, T = lin([[m2, 1], [-m1, 1]], [m2 * G, m1 * G])   # heavier m2 down: m2 g − T = m2 a ; T − m1 g = m1 a
        if t == 'atw': return close(num(Rv), abs(a), 0.006)
        return Rv == round(T)
    if t == 'table':
        a, T = lin([[p['M'], -1], [p['m'], 1]], [-p['mu'] * p['M'] * G, p['m'] * G]); return Rv == round(a * 10)
    if t == 'train':
        m1, m2, m3 = p['ms']; a, T1, T2 = lin([[m1, -1, 0], [m2, 1, -1], [m3, 0, 1]], [0, 0, p['F']])
        x, y = Rv.split(', '); return close(num(x), T1, 0.006) and close(num(y), T2, 0.006)
    if t == 'eq':
        a1, a2 = math.radians(p['a1']), math.radians(p['a2'])   # Lami: T1 / sin(angle opposite) …
        T1 = p['W'] * math.cos(a2) / math.sin(a1 + a2); return Rv == round(T1)
    if t == 'mratio':
        a, b = [int(x) for x in Rv.split(' : ')]; return abs((a - b) / (a + b) - 1 / p['k']) < 1e-9
    if t in ('bank', 'bank0'):
        r, tn, mu = p['r'], p['tn'], p['mu']; th = math.atan(tn)
        # unknowns N, v²/r: vertical N cosθ − μN sinθ = g ; horizontal N sinθ + μN cosθ = v²/r (per unit mass)
        N = G / (math.cos(th) - mu * math.sin(th)); v = math.sqrt(r * N * (math.sin(th) + mu * math.cos(th))); return Rv == round(v)
    if t == 'string': return Rv == round(math.sqrt(p['T'] / (p['m'] * p['L'])))
    if t == 'vert':
        r, m = p['r'], p['m']; vt = math.sqrt(G * r); vb = math.sqrt(vt * vt + 2 * G * 2 * r)
        val = {'vmin_top': vt, 'vmin_bot': vb, 'Tbot': m * G + m * vb * vb / r}[p['ask']]; return Rv == round(val * 10)
    if t == 'coin': return Rv == round(math.sqrt(p['mu'] * G / p['r']) * 10)
    if t == 'drum': return close(num(Rv), G / (p['w'] ** 2 * p['r']), 0.003)
    raise KeyError(t)
