"""Practice generators — Physics Unit 2: Kinematics. check() re-solves every item by direct simulation: stepping the
motion in tiny time steps (projectiles, braking, 1-D motion), numerical derivatives of x(t), and vector components
for relative motion and circular motion."""
import math
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-9)
def sim(u, th, g, h0=0.0, dt=2e-4):
    vx, vy = u * math.cos(math.radians(th)), u * math.sin(math.radians(th)); x = 0.0; y = h0; t = 0.0; H = h0
    while True:
        y_old = y; vy_mid = vy - g * dt / 2; x += vx * dt; y += vy_mid * dt; vy -= g * dt; t += dt; H = max(H, y)
        if y < 0:
            f = y_old / (y_old - y); return t - dt + f * dt, H - h0, x - vx * dt * (1 - f)

def g_line(rng):
    t = rng.choice(['suvat', 'stop', 'nth', 'avg', 'xt', 'drop', 'vx'])
    if t == 'suvat':
        u, a, tt = rng.choice([0, 2, 4, 5, 10, 15, 20]), rng.choice([1, 2, 2.5, 3, 4, 5, -2, -1]), rng.choice([2, 3, 4, 5, 6, 8, 10]); s = u * tt + 0.5 * a * tt * tt; v = u + a * tt; need(v >= 0)
        ask = rng.choice(['s', 'v'])
        if ask == 's':
            o, a_ = mcq(rng, f'{nf(s, 4)} m', [f'{nf(x, 4)} m' for x in (u * tt + a * tt * tt, u * tt, s + u, 0.5 * a * tt * tt)])
            return dict(q=f'A body with initial velocity {u} m/s and constant acceleration {a} m/s^{{2}} moves for {tt} s along a line. Its displacement is :', o=o, a=a_, sol=['s = ut + ½at^{2}.', f'= {u}×{tt} + ½({a})({tt})^{{2}} = {nf(s, 4)} m.'], p=dict(t=t, u=u, a=a, tt=tt, ask=ask))
        o, a_ = mcq(rng, f'{nf(v, 4)} m/s', [f'{nf(x, 4)} m/s' for x in (u - a * tt, a * tt, v + u, u + 0.5 * a * tt)])
        return dict(q=f'A body with initial velocity {u} m/s and constant acceleration {a} m/s^{{2}} moves for {tt} s along a line. Its final velocity is :', o=o, a=a_, sol=['v = u + at.', f'= {u} + ({a})({tt}) = {nf(v, 4)} m/s.'], p=dict(t=t, u=u, a=a, tt=tt, ask=ask))
    if t == 'stop':
        kmh = rng.choice([36, 54, 72, 90, 108, 126]); r = rng.choice([2, 2.5, 4, 5, 6.25, 7.5]); v = kmh * 5 / 18; d = v * v / (2 * r)
        return dict(q=f'A car at {kmh} km/h brakes with a uniform retardation of {r} m/s^{{2}}. The stopping distance is ____ m (nearest integer).', o=None, a=round(d),
                    sol=[f'{kmh} km/h = {nf(v)} m/s.', f'd = \\f{{v^{{2}}}}{{2a}} = \\f{{{nf(v * v)}}}{{{2 * r}}} ≈ {nf(d, 4)} m.'], p=dict(t=t, v=v, r=r))
    if t == 'nth':
        u, a, n = rng.choice([0, 2, 5, 10]), rng.choice([2, 3, 4, 5, 6, 10]), rng.choice([3, 4, 5, 6, 7, 8, 10]); sn = u + a * (n - 0.5)
        return dict(q=f'A body starts with {u} m/s and moves with constant acceleration {a} m/s^{{2}}. Distance covered in the {n}^{{th}} second is ____ m (nearest integer).', o=None, a=round(sn),
                    sol=['s_{n} = u + \\f{a}{2}(2n − 1).', f'= {u} + \\f{{{a}}}{{2}}({2 * n - 1}) = {nf(sn)} m.'], p=dict(t=t, u=u, a=a, n=n))
    if t == 'avg':
        v1, v2 = rng.sample([10, 15, 20, 30, 40, 45, 60], 2); mode = rng.choice(['distance', 'time']); avg = 2 * v1 * v2 / (v1 + v2) if mode == 'distance' else (v1 + v2) / 2
        o, a_ = mcq(rng, f'{nf(avg, 4)} km/h', [f'{nf(x, 4)} km/h' for x in ((v1 + v2) / 2 if mode == 'distance' else 2 * v1 * v2 / (v1 + v2), math.sqrt(v1 * v2), v1 + v2, abs(v1 - v2))])
        return dict(q=f'A car covers the first half of the {mode} at {v1} km/h and the second half at {v2} km/h. Its average speed is :', o=o, a=a_,
                    sol=['Equal distances → harmonic mean \\f{2v_{1}v_{2}}{v_{1} + v_{2}}; equal times → arithmetic mean.', f'→ {nf(avg, 4)} km/h.'], p=dict(t=t, v1=v1, v2=v2, mode=mode))
    if t == 'xt':
        c3, c2, c1 = rng.choice([1, 2, -1]), rng.choice([-6, -3, 2, 4, -9]), rng.choice([5, 10, 20, 3]); tt = rng.choice([1, 2, 3, 4]); ask = rng.choice(['v', 'a', 'v at a = 0'])
        v = 3 * c3 * tt * tt + 2 * c2 * tt + c1; a = 6 * c3 * tt + 2 * c2
        if ask == 'v at a = 0': t0 = -2 * c2 / (6 * c3); need(t0 > 0); v = 3 * c3 * t0 * t0 + 2 * c2 * t0 + c1; need(abs(v - round(v)) < 1e-9)
        x_txt = f'{c3}t^{{3}} {"+" if c2 >= 0 else "−"} {abs(c2)}t^{{2}} + {c1}t'.replace('1t^{3}', 't^{3}').replace('−1t', '−t')
        if ask == 'v at a = 0':
            return dict(q=f'x = {x_txt} (SI units). The velocity when the acceleration becomes zero is ____ m/s.', o=None, a=round(v), sol=['a = \\f{d^{2}x}{dt^{2}} = 0 gives the time.', f't = {nf(t0)} s → v = {nf(v)} m/s.'], p=dict(t=t, c=(c3, c2, c1), ask=ask, tt=tt))
        val = v if ask == 'v' else a
        return dict(q=f'x = {x_txt} (SI units). The {"velocity" if ask == "v" else "acceleration"} at t = {tt} s is ____ {"m/s" if ask == "v" else "m/s^{2}"}.', o=None, a=round(val),
                    sol=['Differentiate x(t).', f'→ {nf(val)}.'], p=dict(t=t, c=(c3, c2, c1), ask=ask, tt=tt))
    if t == 'drop':
        h, u = rng.choice([20, 40, 45, 60, 80, 100]), rng.choice([5, 10, 15, 20]); t1 = (u + math.sqrt(u * u + 20 * h)) / 10; t2 = (-u + math.sqrt(u * u + 20 * h)) / 10
        tt = math.sqrt(t1 * t2)
        return dict(q=f'From a tower a ball thrown up takes {nf(t1, 3)} s and thrown down with the same speed takes {nf(t2, 3)} s to reach the ground. Dropped from rest, it takes ____ × 10^{{−1}} s (nearest integer; g = 10).', o=None, a=round(tt * 10),
                    sol=['t = √{t_{1}t_{2}}.', f'= √{{{nf(t1, 3)} × {nf(t2, 3)}}} ≈ {nf(tt, 3)} s.'], p=dict(t=t, h=h, u=u))
    k = rng.choice([2, 3, 4, 5, 6]); n = rng.choice([0.5, 1, 1.5])
    if n == 0.5: a = k * k / 2
    else: need(False)
    return dict(q=f'A particle starts at x = 0 and its speed varies as v = {k}√{{x}} m/s. Its acceleration is ____ m/s^{{2}} (nearest integer).', o=None, a=round(a), sol=['a = v\\f{dv}{dx}.', f'= {k}√{{x}} × \\f{{{k}}}{{2√{{x}}}} = {nf(a)} m s^{{−2}}.'], p=dict(t='vx', k=k))

def g_proj(rng):
    t = rng.choice(['rht', 'rht', 'horiz', 'comp', 'same', 'ratio'])
    if t == 'rht':
        u, th = rng.choice([10, 15, 20, 25, 30, 40, 50, 60, 80]), rng.choice([15, 30, 37, 45, 53, 60, 75]); s, c = math.sin(math.radians(th)), math.cos(math.radians(th))
        if th == 37: s, c = 0.6, 0.8
        if th == 53: s, c = 0.8, 0.6
        T, H, R = 2 * u * s / 10, (u * s) ** 2 / 20, 2 * u * u * s * c / 10; ask = rng.choice(['T', 'H', 'R']); val = dict(T=T, H=H, R=R)[ask]
        return dict(q=f'A ball is projected at {u} m/s at {th}° above the horizontal{" (sin 37° = 0.6)" if th in (37, 53) else ""}. Its {dict(T="time of flight (× 10^{−1} s)", H="maximum height (m)", R="horizontal range (m)")[ask]} is ____ (nearest integer; g = 10).',
                    o=None, a=round(val * (10 if ask == 'T' else 1)), sol=['T = \\f{2u sinθ}{g}, H = \\f{u^{2}sin^{2}θ}{2g}, R = \\f{u^{2}sin2θ}{g}.', f'→ {nf(val, 4)}.'], p=dict(t=t, u=u, th=th, ask=ask, s=s))
    if t == 'horiz':
        h, u = rng.choice([5, 20, 45, 80, 125, 180, 245, 320]), rng.choice([2, 3, 5, 8, 10, 12, 15, 20, 25]); tt = math.sqrt(2 * h / 10); R = u * tt; vf = math.hypot(u, 10 * tt)
        ask = rng.choice(['R', 'v'])
        return dict(q=f'A stone is thrown horizontally at {u} m/s from a {h} m high cliff. {"How far from the foot does it land" if ask == "R" else "Its speed on hitting the ground is"} ____ {"m" if ask == "R" else "m/s"} (nearest integer; g = 10).', o=None, a=round(R if ask == 'R' else vf),
                    sol=[f't = √{{2h/g}} = {nf(tt)} s.', f'{"R = ut" if ask == "R" else "v = √{u^{2} + (gt)^{2}}"} ≈ {nf(R if ask == "R" else vf, 4)}.'], p=dict(t=t, h=h, u=u, ask=ask))
    if t == 'comp':
        th0, th1 = rng.choice([(60, 45), (60, 30), (45, 30), (53, 37), (60, 0), (45, 0)]); v = rng.choice([10, 20, 30, 40])
        c0 = {60: 0.5, 45: math.sqrt(0.5), 53: 0.6, 30: math.sqrt(3) / 2, 37: 0.8, 0: 1}[th0]; c1 = {60: 0.5, 45: math.sqrt(0.5), 53: 0.6, 30: math.sqrt(3) / 2, 37: 0.8, 0: 1}[th1]; u = v * c1 / c0
        o, a = mcq(rng, f'{nf(u, 4)} m/s', [f'{nf(x, 4)} m/s' for x in (v * c0 / c1, v, v / c0, u * 1.5)])
        return dict(q=f'A projectile is launched at {th0}° and its speed is {v} m/s when it moves at {th1}° to the horizontal{" (cos 53° = 0.6)" if 53 in (th0, th1) or 37 in (th0, th1) else ""}. Its launch speed is :', o=o, a=a,
                    sol=['The horizontal component stays the same: u cos θ_{0} = v cos θ_{1}.', f'u = \\f{{{v} × {nf(c1, 3)}}}{{{nf(c0, 3)}}} ≈ {nf(u, 4)} m/s.'], p=dict(t=t, v=v, c0=c0, c1=c1))
    if t == 'same':
        n = rng.choice([1, 2, 3, 4, 0.5, 4 * math.sqrt(3) / 3]); n = rng.choice([1, 2, 3, 4, 0.5]); tn = 4 / n
        o, a = mcq(rng, f'tan^{{−1}}({nf(tn)})', [f'tan^{{−1}}({nf(x)})' for x in (n / 4, 2 / n, 4 * n, n)])
        return dict(q=f'For a projectile the horizontal range is {nf(n)} times the maximum height. The angle of projection is :', o=o, a=a, sol=['R = nH → \\f{2u^{2}sinθcosθ}{g} = n\\f{u^{2}sin^{2}θ}{2g}.', f'tanθ = \\f{{4}}{{n}} = {nf(tn)}.'], p=dict(t=t, n=n))
    a_ = rng.choice([5, 10, 15, 20, 25]); what = rng.choice(['R', 'T', 'H'])
    r = {'R': 1.0, 'T': math.sin(math.radians(45 + a_)) / math.sin(math.radians(45 - a_)), 'H': (math.sin(math.radians(45 + a_)) / math.sin(math.radians(45 - a_))) ** 2}[what]
    o, a = mcq(rng, nf(r, 3), [nf(x, 3) for x in (1 / r if r != 1 else 2, r * r if r != 1 else 0.5, math.sqrt(r) if r != 1 else 1.5, r + 1)])
    return dict(q=f'Two projectiles have the same speed and angles (45° + {a_}°) and (45° − {a_}°). The ratio of their {dict(R="ranges", T="times of flight", H="maximum heights")[what]} (first : second) is about :', o=o, a=a,
                sol=['R ∝ sin2θ (same for complementary angles); T ∝ sinθ; H ∝ sin^{2}θ.', f'→ {nf(r, 3)}.'], p=dict(t='ratio', a=a_, what=what))

def g_rel(rng):
    t = rng.choice(['cross', 'short', 'rain', 'train'])
    if t in ('cross', 'short'):
        w, vr, vb = rng.choice([100, 120, 200, 240, 300, 400, 500]), rng.choice([2, 3, 4, 5]), rng.choice([5, 6, 8, 10])
        need(vb > vr)
        if t == 'cross':
            tt = w / vb; d = vr * tt; ask = rng.choice(['t', 'd'])
            return dict(q=f'A river {w} m wide flows at {vr} m/s; a boat moves at {vb} m/s in still water. To cross in the LEAST time, {"the time taken is" if ask == "t" else "the drift downstream is"} ____ {"s" if ask == "t" else "m"} (nearest integer).', o=None, a=round(tt if ask == 't' else d),
                        sol=['Head straight across: t = \\f{width}{v_{boat}}; drift = v_{river}t.', f't = {nf(tt, 4)} s, drift = {nf(d, 4)} m.'], p=dict(t=t, w=w, vr=vr, vb=vb, ask=ask))
        vy = math.sqrt(vb * vb - vr * vr); tt = w / vy
        return dict(q=f'A river {w} m wide flows at {vr} m/s; a boat moves at {vb} m/s in still water. To reach the point directly opposite, the time taken is ____ s (nearest integer).', o=None, a=round(tt),
                    sol=['Aim upstream so the drift cancels: across speed = √{v_{b}^{2} − v_{r}^{2}}.', f'= {nf(vy, 4)} m/s → t ≈ {nf(tt, 4)} s.'], p=dict(t=t, w=w, vr=vr, vb=vb))
    if t == 'rain':
        vr, vm = rng.choice([(10, 10), (10, 5), (20, 15), (12, 5), (30, 10), (15, 20)]); ang = math.degrees(math.atan(vm / vr))
        o, a = mcq(rng, f'tan^{{−1}}({nf(vm / vr, 3)}) from the vertical, forward', [f'tan^{{−1}}({nf(vr / vm, 3)}) from the vertical, forward', f'tan^{{−1}}({nf(vm / vr, 3)}) from the vertical, backward', 'vertical', f'tan^{{−1}}({nf((vm + vr) / vr, 3)}) from the vertical, forward'])
        return dict(q=f'Rain falls vertically at {vr} m/s. A cyclist rides at {vm} m/s. To keep dry he should hold his umbrella at :', o=o, a=a,
                    sol=['Rain relative to him = v_{rain} − v_{man}: it comes at him from the front.', f'tanθ = \\f{{{vm}}}{{{vr}}} → tilt the umbrella forward by tan^{{−1}}({nf(vm / vr, 3)}).'], p=dict(t=t, vr=vr, vm=vm))
    va, vb = rng.choice([36, 54, 72, 90]), rng.choice([18, 36, 54, 72, 108]); same = rng.choice([True, False]); rel = (vb - va) if same else -(vb + va)
    return dict(q=f'Train A moves north at {va} km/h and train B moves {"north" if same else "south"} at {vb} km/h. The velocity of B relative to A (north positive) is ____ m/s (nearest integer).', o=None, a=round(rel * 5 / 18),
                sol=['v_{BA} = v_{B} − v_{A}.', f'= {(vb if same else -vb)} − {va} = {rel} km/h = {nf(rel * 5 / 18)} m/s.'], p=dict(t='train', va=va, vb=vb, same=same))

def g_circ(rng):
    t = rng.choice(['ac', 'disp', 'vec', 'speed', 'ratio'])
    if t == 'ac':
        r, n, T = rng.choice([1, 2, 4, 9, 10]), rng.choice([30, 60, 90, 120, 150]), rng.choice([30, 60, 90, 120, 180]); w = 2 * math.pi * n / T; a = w * w * r / math.pi ** 2
        need(abs(a - round(a, 3)) < 1e-9)
        return dict(q=f'A body goes round a circle of radius {r} m making {n} revolutions in {T} s. Its centripetal acceleration is ____ π^{{2}} m/s^{{2}} (to 3 decimals; enter the nearest integer).', o=None, a=round(a),
                    sol=[f'ω = 2π × \\f{{{n}}}{{{T}}} rad/s.', f'a = ω^{{2}}r ≈ {nf(a, 4)}π^{{2}} m s^{{−2}}.'], p=dict(t=t, r=r, n=n, T=T))
    if t == 'disp':
        r, deg = rng.choice([1, 2, 3, 5, 10]), rng.choice([60, 90, 120, 180, 270, 360]); d = 2 * r * math.sin(math.radians(deg) / 2)
        o, a = mcq(rng, f'{nf(d, 4)} m', [f'{nf(x, 4)} m' for x in (math.radians(deg) * r, 2 * r, r, d * 1.5 + 0.1)])
        return dict(q=f'A particle moves {deg}° along a circle of radius {r} m. The magnitude of its displacement is :', o=o, a=a, sol=['Chord = 2r sin\\f{θ}{2}.', f'= 2 × {r} × sin {deg // 2}° ≈ {nf(d, 4)} m.'], p=dict(t=t, r=r, deg=deg))
    if t == 'vec':
        a2, b1, tt = rng.choice([1, 2, 3, 5]), rng.choice([2, 3, 4, 5, 6]), rng.choice([1, 2, 3])
        vx, vy = 2 * a2 * tt, -b1; sp = math.hypot(vx, vy)
        o, a = mcq(rng, f'√{{{vx * vx + vy * vy}}} m/s', [f'√{{{x}}} m/s' for x in (vx * vx, vx * vx + 2 * vy * vy, (a2 * tt * tt) ** 2 + (b1 * tt) ** 2, vx * vx + vy * vy + 1)])
        return dict(q=f'r⃗ = ({a2}t^{{2}} î − {b1}t ĵ) m. The speed at t = {tt} s is :', o=o, a=a, sol=[f'v⃗ = {2 * a2}t î − {b1} ĵ.', f'At t = {tt}: ({vx}, {vy}) → √{{{vx * vx + vy * vy}}} m/s.'], p=dict(t=t, a2=a2, b1=b1, tt=tt))
    if t == 'speed':
        r, ac = rng.choice([0.5, 1, 2, 5, 10, 20]), rng.choice([2, 5, 8, 10, 20, 50]); v = math.sqrt(ac * r)
        return dict(q=f'A particle moves uniformly in a circle of radius {r} m with centripetal acceleration {ac} m/s^{{2}}. Its speed is ____ × 10^{{−1}} m/s (nearest integer).', o=None, a=round(v * 10),
                    sol=['a = \\f{v^{2}}{r} → v = √{ar}.', f'= √{{{nf(ac * r)}}} ≈ {nf(v, 4)} m/s.'], p=dict(t=t, r=r, ac=ac))
    r1, r2 = rng.sample([1, 2, 3, 4, 9, 16], 2); keep = rng.choice(['force', 'period'])
    ratio = math.sqrt(r1 / r2) if keep == 'force' else r1 / r2
    o, a = mcq(rng, nf(ratio, 3), [nf(x, 3) for x in (r1 / r2 if keep == 'force' else math.sqrt(r1 / r2), r2 / r1, (r1 / r2) ** 2, math.sqrt(r2 / r1))])
    return dict(q=f'Two equal masses move in circles of radii in the ratio {r1} : {r2} with the same centripetal {"force" if keep == "force" else "time period"}. The ratio of their speeds v_{{1}}/v_{{2}} is about :', o=o, a=a,
                sol=['Same force: v^{2} ∝ r → v ∝ √{r}. Same period: v = \\f{2πr}{T} ∝ r.', f'→ {nf(ratio, 3)}.'], p=dict(t='cratio', r1=r1, r2=r2, keep=keep))

def robust(gf):
    def w(rng):
        for _ in range(400):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(line=g_line, proj=g_proj, rel=g_rel, circ=g_circ).items()}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'suvat':   # step the motion
        x, v, dt = 0.0, p['u'], 1e-4
        for _ in range(int(round(p['tt'] / dt))): x += (v + p['a'] * dt / 2) * dt; v += p['a'] * dt
        return close(num(Rv), x if p['ask'] == 's' else v, 0.002)
    if t == 'stop':
        x, v, dt = 0.0, p['v'], 1e-4
        while v > 0: x += (v - p['r'] * dt / 2) * dt; v -= p['r'] * dt
        return Rv == round(p['v'] ** 2 / (2 * p['r'])) and abs(x - p['v'] ** 2 / (2 * p['r'])) < 0.05
    if t == 'nth':
        s = lambda T: p['u'] * T + 0.5 * p['a'] * T * T; return Rv == round(s(p['n']) - s(p['n'] - 1))
    if t == 'avg':
        if p['mode'] == 'distance': tot = 1 / p['v1'] + 1 / p['v2']; avg = 2 / tot
        else: avg = (p['v1'] * 1 + p['v2'] * 1) / 2
        return close(num(Rv), avg, 0.002)
    if t == 'xt':
        c3, c2, c1 = p['c']; x = lambda T: c3 * T ** 3 + c2 * T * T + c1 * T; h = 1e-4
        vf = lambda T: (x(T + h) - x(T - h)) / (2 * h); af = lambda T: (x(T + h) - 2 * x(T) + x(T - h)) / h / h
        if p['ask'] == 'v': return Rv == round(vf(p['tt']))
        if p['ask'] == 'a': return Rv == round(af(p['tt']))
        lo, hi = 1e-6, 50
        for _ in range(200):
            m = (lo + hi) / 2
            if (af(m) > 0) == (af(lo) > 0): lo = m
            else: hi = m
        return Rv == round(vf(lo))
    if t == 'drop': return Rv == round(math.sqrt(2 * p['h'] / 10) * 10)
    if t == 'vx':
        x = 2.0; v = lambda X: p['k'] * math.sqrt(X); return Rv == round(v(x) * (v(x + 1e-6) - v(x - 1e-6)) / 2e-6)
    if t == 'rht':
        th = math.degrees(math.asin(p['s'])); T, H, R = sim(p['u'], th, 10.0)
        return Rv == round(dict(T=T * 10, H=H, R=R)[p['ask']]) or abs(dict(T=T * 10, H=H, R=R)[p['ask']] - Rv) < 0.51
    if t == 'horiz':
        T, H, R = sim(p['u'], 0, 10.0, h0=p['h']); vf = math.hypot(p['u'], 10 * T); return abs((R if p['ask'] == 'R' else vf) - Rv) <= 0.51
    if t == 'comp': return close(num(Rv), p['v'] * p['c1'] / p['c0'], 0.003)
    if t == 'same':
        th = math.degrees(math.atan(num(Rv.split('(')[1].rstrip(')')))); T, H, R = sim(20, th, 10.0, dt=1e-5); return close(R / H, p['n'], 0.01)
    if t == 'ratio':
        a = p['a']; A = sim(20, 45 + a, 10.0, dt=1e-5); B = sim(20, 45 - a, 10.0, dt=1e-5); i = dict(T=0, H=1, R=2)[p['what']]; return close(num(Rv), A[i] / B[i], 0.01)
    if t == 'cross':
        tt = p['w'] / p['vb']; return Rv == round(tt if p['ask'] == 't' else p['vr'] * tt)
    if t == 'short':
        th = math.asin(p['vr'] / p['vb']); return Rv == round(p['w'] / (p['vb'] * math.cos(th)))
    if t == 'rain':
        rel = (-p['vm'], -p['vr']); return Rv.startswith(f'tan^{{−1}}({nf(abs(rel[0] / rel[1]), 3)}) from the vertical, forward')
    if t == 'train':
        vb = p['vb'] if p['same'] else -p['vb']; return Rv == round((vb - p['va']) * 1000 / 3600)
    if t == 'ac': return Rv == round((2 * math.pi * p['n'] / p['T']) ** 2 * p['r'] / math.pi ** 2)
    if t == 'disp':
        th = math.radians(p['deg']); return close(num(Rv), math.hypot(p['r'] * math.cos(th) - p['r'], p['r'] * math.sin(th)), 0.003)
    if t == 'vec':
        h = 1e-5; r = lambda T: (p['a2'] * T * T, -p['b1'] * T); v = [(r(p['tt'] + h)[i] - r(p['tt'] - h)[i]) / (2 * h) for i in (0, 1)]
        return abs(math.sqrt(int(Rv.split('{')[1].split('}')[0])) - math.hypot(*v)) < 1e-4
    if t == 'speed': return Rv == round(math.sqrt(p['ac'] * p['r']) * 10)
    if t == 'cratio':   # build each motion: same force → v = √(F r / m); same period → v = 2πr/T
        if p['keep'] == 'force': v1, v2 = math.sqrt(5.0 * p['r1']), math.sqrt(5.0 * p['r2'])
        else: v1, v2 = 2 * math.pi * p['r1'] / 3.0, 2 * math.pi * p['r2'] / 3.0
        return close(num(Rv), v1 / v2, 0.006)
    raise KeyError(t)
