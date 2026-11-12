"""Practice generators — Physics Unit 8: Thermodynamics. check() re-solves each item another way: P dV integrated
numerically along the path, energies from explicit n, R, T numbers, polygon (shoelace) areas for cycles."""
import math
from fractions import Fraction as F
from common import mcq, nf, fr
R = 8.314
def need(c):
    if not c: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def integ(f, a, b, n=20000):
    h = (b - a) / n; return sum(f(a + (i + .5) * h) for i in range(n)) * h
GAS = {3: 'monoatomic', 5: 'diatomic (rigid)', 6: 'polyatomic (f = 6)', 7: 'diatomic (with vibration)'}

def g_first(rng):
    t = rng.choice(['isoQ', 'isoU', 'cvdu', 'ratio', 'piston', 'cyclic'])
    if t in ('isoQ', 'isoU'):
        f = rng.choice([3, 5, 6, 7]); W = rng.choice([20, 40, 50, 60, 80, 100, 120, 150, 200, 300, 400, 500, 600])
        Q = W * F(f + 2, 2); U = W * F(f, 2); v = Q if t == 'isoQ' else U; need(v.denominator == 1)
        q = f'A {GAS[f]} ideal gas does {W} J of work in an isobaric expansion. The {"heat given to" if t == "isoQ" else "increase in internal energy of"} the gas is ______ J.'
        return dict(q=q, o=None, a=int(v), sol=['Isobaric: W = nRΔT, ΔU = nC_{v}ΔT = \\f{f}{2}W, Q = ΔU + W.', f'f = {f} → ΔU = {fr(U)} J, Q = {fr(Q)} J.'], p=dict(t=t, f=f, W=W))
    if t == 'cvdu':
        n = rng.choice([1, 2, 3, 4, 5, 10]); cp = rng.choice([5, 6, 7, 8, 9]); dT = rng.choice([5, 10, 20, 25, 30, 50])
        v = n * (cp - 2) * dT
        q = f'{n} mol of a gas (C_{{p}} = {cp} cal/mol °C, R = 2 cal/mol °C) is heated at constant volume by {dT} °C. The change in internal energy is ______ cal.'
        return dict(q=q, o=None, a=v, sol=['C_{v} = C_{p} − R.', f'ΔU = {n} × {cp - 2} × {dT} = {v} cal.'], p=dict(t=t, n=n, cp=cp, dT=dT))
    if t == 'ratio':
        f = rng.choice([3, 5, 6, 7]); a, b, c = F(f + 2, 2), F(f, 2), F(1)
        m = 2; right = f'{int(a * m)} : {int(b * m)} : {int(c * m)}'
        q = f'Heat is supplied at constant pressure to a {GAS[f]} ideal gas. ΔQ : ΔU : ΔW is :'
        o, a_ = mcq(rng, right, [f'{x} : {y} : {z}' for x, y, z in ((f, f + 2, 2), (f + 2, 2, f), (f + 2, f, 1), (f, f - 2, 2), (5, 3, 2), (7, 5, 2), (4, 3, 1))])
        return dict(q=q, o=o, a=a_, sol=['Per mole per kelvin: Q = C_{p}, ΔU = C_{v}, W = R.', f'= \\f{{{f + 2}}}{{2}} : \\f{{{f}}}{{2}} : 1 = {right}.'], p=dict(t=t, f=f))
    if t == 'piston':
        n = rng.choice([1, 2]); f = rng.choice([3, 5]); dT = rng.choice([2, 3, 4, 5, 6, 8, 10]); A = rng.choice([10, 20, 25, 40, 50]); P0 = 1e5
        dx = n * R * dT / (P0 * A * 1e-4) * 100; Q = n * F(f + 2, 2) * R * dT
        q = f'{n} mol of a {GAS[f]} gas in a cylinder with a light frictionless piston of area {A} cm^{{2}} (outside pressure 10^{{5}} Pa) is heated slowly so its temperature rises {dT} K. The piston moves out by :'
        o, a_ = mcq(rng, f'{nf(dx, 3)} cm', [f'{nf(dx * k, 3)} cm' for k in (F(f, 2), F(f + 2, 2), 10, 0.1, 2)])
        return dict(q=q, o=o, a=a_, sol=['Constant pressure: W = PAΔx = nRΔT.', f'Δx = \\f{{{n} × 8.314 × {dT}}}{{10^{{5}} × {A} × 10^{{−4}}}} ≈ {nf(dx, 3)} cm.'], p=dict(t=t, n=n, dT=dT, A=A))
    Qs = [rng.choice([100, 200, 300, 400, 500, 600]), -rng.choice([50, 100, 150, 250, 350]), rng.choice([40, 80, 120, 160])]
    Ws = [rng.choice([50, 100, 150, 200, 250]), -rng.choice([20, 40, 60, 80])]
    W3 = sum(Qs) - sum(Ws)
    q = f'In a cyclic process of three steps, the heats taken in are {Qs[0]} J, {Qs[1]} J and {Qs[2]} J, and the work done by the gas in the first two steps is {Ws[0]} J and {Ws[1]} J. The work done by the gas in the third step is ______ J.'.replace('-', '−')
    need(W3 > 0)
    return dict(q=q, o=None, a=W3, sol=['Over a full cycle ΔU = 0 → total Q = total W.', f'W_{{3}} = ({Qs[0]} + {Qs[1]} + {Qs[2]}) − ({Ws[0]} + {Ws[1]}) = {W3} J.'.replace('+ -', '− ')], p=dict(t='cyc3', Qs=Qs, Ws=Ws))

def g_adia(rng):
    t = rng.choice(['P', 'T', 'W', 'expo', 'gasid', 'dT'])
    if t == 'P':
        g, k = rng.choice([(F(5, 3), 8), (F(5, 3), 27), (F(3, 2), 4), (F(3, 2), 9), (F(3, 2), 16), (F(4, 3), 8), (F(4, 3), 27), (F(7, 5), 32), (F(5, 3), F(1, 8)), (F(3, 2), F(1, 4)), (F(4, 3), F(1, 8)), (F(5, 4), 16)])
        v = F(k) ** g if (F(k) ** g) == int(F(k) ** g) or True else 0
        vv = float(F(k)) ** float(g); need(abs(vv - round(vv)) < 1e-9 or abs(1 / vv - round(1 / vv)) < 1e-9)
        r = fr(F(round(vv))) if vv >= 1 else fr(F(1, round(1 / vv)))
        q = f'An ideal gas (γ = {fr(g)}) is {"compressed" if F(k) > 1 else "expanded"} adiabatically so that its volume becomes {fr(1 / F(k))} of the initial value. P_{{final}}/P_{{initial}} is :'
        o, a = mcq(rng, r, [fr(x) for x in (F(k), F(k) ** 2, 1 / F(k), F(round(vv) * 2) if vv >= 1 else F(1, round(1 / vv) * 2), F(k) * g)])
        return dict(q=q, o=o, a=a, sol=['PV^{γ} = constant → \\f{P_{2}}{P_{1}} = (\\f{V_{1}}{V_{2}})^{γ}.', f'= ({fr(k)})^{{{fr(g)}}} = {r}.'], p=dict(t=t, g=float(g), k=float(F(k))))
    if t == 'T':
        g, k = rng.choice([(F(3, 2), 4), (F(3, 2), 9), (F(3, 2), 16), (F(5, 3), 8), (F(5, 3), 27), (F(4, 3), 8), (F(4, 3), 27), (F(3, 2), F(1, 4)), (F(5, 3), F(1, 8))])
        T1 = rng.choice([200, 250, 273, 300, 320, 360, 400, 450, 600])
        T2 = T1 * float(F(k)) ** float(g - 1); need(abs(T2 - round(T2)) < 1e-6)
        ask = rng.choice(['final', 'change'])
        v = round(T2) if ask == 'final' else abs(round(T2) - T1)
        q = f'A gas (γ = {fr(g)}) at {T1} K is {"compressed" if F(k) > 1 else "expanded"} adiabatically to {fr(1 / F(k))} of its volume. The {"final temperature" if ask == "final" else "change in temperature"} is ______ K.'
        return dict(q=q, o=None, a=v, sol=['TV^{γ − 1} = constant.', f'T_{{2}} = {T1} × ({fr(k)})^{{{fr(g - 1)}}} = {round(T2)} K.'], p=dict(t=t, g=float(g), k=float(F(k)), T1=T1, ask=ask))
    if t == 'W':
        g = rng.choice([F(3, 2), F(5, 3), F(4, 3), F(7, 5)]); P1 = rng.choice([2, 4, 6, 8, 10, 16, 20]) * 1e5; V1 = rng.choice([0.01, 0.02, 0.05, 0.1, 0.15, 0.2]); r = rng.choice([2, 4, 8, 27, 3])
        V2 = V1 * r; P2 = P1 * (V1 / V2) ** float(g); Wv = (P1 * V1 - P2 * V2) / float(g - 1)
        q = f'A gas (γ = {fr(g)}) at {nf(P1)} Pa occupying {nf(V1)} m^{{3}} expands adiabatically to {nf(V2)} m^{{3}}. Work done by the gas is about :'
        o, a = mcq(rng, f'{nf(Wv, 3)} J', [f'{nf(x, 3)} J' for x in (Wv * float(g), P1 * V1 * math.log(r), Wv * 2, Wv / 2, P1 * (V2 - V1))])
        return dict(q=q, o=o, a=a, sol=['W = \\f{P_{1}V_{1} − P_{2}V_{2}}{γ − 1} with P_{2} = P_{1}(\\f{V_{1}}{V_{2}})^{γ}.', f'≈ {nf(Wv, 3)} J.'], p=dict(t=t, g=float(g), P1=P1, V1=V1, V2=V2))
    if t == 'expo':
        g = rng.choice([F(5, 3), F(7, 5), F(3, 2), F(4, 3), F(9, 7), F(5, 4)]); k = g / (g - 1)
        q = f'Along an adiabatic process of a gas, P ∝ T^{{{k}}}. The ratio C_{{p}}/C_{{v}} is :' if k.denominator == 1 else f'Along an adiabatic process of a gas, P ∝ T^{{{k.numerator}/{k.denominator}}}. The ratio C_{{p}}/C_{{v}} is :'
        o, a = mcq(rng, fr(g), [fr(x) for x in (F(5, 3), F(7, 5), F(3, 2), F(4, 3), F(9, 7), F(5, 4)) if x != g])
        return dict(q=q, o=o, a=a, sol=['On an adiabat P^{1 − γ}T^{γ} is constant → P ∝ T^{γ/(γ − 1)}.', f'\\f{{γ}}{{γ − 1}} = {fr(k)} → γ = {fr(g)}.'], p=dict(t=t, k=float(k)))
    if t == 'gasid':
        f = rng.choice([3, 5, 6]); g = 1 + F(2, f); vr = rng.choice([8, 27, 64, 4, 9])
        Tr = float(vr) ** -float(g - 1); need(abs(1 / Tr - round(1 / Tr)) < 1e-9)
        q = f'In a reversible process with no heat exchange, the volume of an ideal gas becomes {vr} times and its temperature becomes 1/{round(1 / Tr)} of the initial value. The gas is :'
        nm = {3: 'He', 5: 'O_{2}', 6: 'CH_{4}'}
        o, a = mcq(rng, nm[f], [x for x in ('He', 'O_{2}', 'CH_{4}', 'Ar' if f != 3 else 'N_{2}') if x != nm[f]])
        return dict(q=q, o=o, a=a, sol=['TV^{γ − 1} = constant.', f'{vr}^{{γ − 1}} = {round(1 / Tr)} → γ = {fr(g)} → {nm[f]}.'], p=dict(t=t, f=f, vr=vr))
    n = rng.choice([1, 2]); f = rng.choice([3, 5]); T = rng.choice([300, 400, 500]); r = rng.choice([2, 3, 4])
    Wiso = n * R * T * math.log(r); dT = Wiso / (n * F(f, 2) * R)
    q = f'{n} mol of a {GAS[f]} gas expands isothermally at {T} K to {r} times its volume and does work W. Doing the same work W adiabatically from {T} K, its final temperature is about :'
    o, a = mcq(rng, f'{nf(T - float(dT), 3)} K', [f'{nf(x, 3)} K' for x in (T + float(dT), T - float(dT) * 2, T - float(dT) / 2, T / r)])
    return dict(q=q, o=o, a=a, sol=['Isothermal: W = nRT ln r. Adiabatic: W = nC_{v}ΔT.', f'ΔT = \\f{{T ln {r}}}{{{f}/2}} ≈ {nf(float(dT), 3)} K → T ≈ {nf(T - float(dT), 3)} K.'], p=dict(t='dT', n=n, f=f, T=T, r=r))

def g_iso(rng):
    t = rng.choice(['isoW', 'isoch', 'isoQ'])
    if t == 'isoW':
        n = rng.choice([1, 2, 3, 4, 5]); T = rng.choice([250, 300, 350, 400, 500]); r = rng.choice([2, 3, 4, 5, 8, 10, F(1, 2), F(1, 4)])
        W = n * R * T * math.log(float(r))
        q = f'{n} mol of an ideal gas at {T} K is {"expanded" if r > 1 else "compressed"} isothermally to {fr(r)} times its volume. Work done BY the gas is about :'
        o, a = mcq(rng, f'{nf(W, 3)} J', [f'{nf(x, 3)} J' for x in (-W, W / math.log(10) * math.log(10) * 2, n * R * T * (float(r) - 1), W / 2, n * R * T * math.log10(float(r)))])
        return dict(q=q, o=o, a=a, sol=['W = nRT ln\\f{V_{2}}{V_{1}}.', f'= {n} × 8.314 × {T} × ln {fr(r)} ≈ {nf(W, 3)} J.'], p=dict(t=t, n=n, T=T, r=float(r)))
    if t == 'isoch':
        n = rng.choice([1, 2, 5, 10]); f = rng.choice([3, 5]); V = rng.choice([1, 2, 3, 5]); P1, P2 = sorted(rng.sample([10, 20, 30, 40, 50, 60, 80, 100], 2))
        Q = F(f, 2) * V * (P2 - P1)
        q = f'{n} mol of a {GAS[f]} gas at constant volume {V} m^{{3}} goes from {P1} Pa to {P2} Pa. The heat supplied is ______ J.'
        need(Q.denominator == 1)
        return dict(q=q, o=None, a=int(Q), sol=['Isochoric: Q = nC_{v}ΔT and nRΔT = VΔP.', f'Q = \\f{{{f}}}{{2}} × {V} × {P2 - P1} = {Q} J.'], p=dict(t=t, f=f, V=V, P1=P1, P2=P2, n=n))
    n = rng.choice([1, 2, 3]); T = rng.choice([300, 400, 500, 600]); r = rng.choice([2, 4, 8])
    Q = n * R * T * math.log(r)
    q = f'{n} mol of an ideal gas expands isothermally at {T} K to {r} times its volume. The heat absorbed is about :'
    o, a = mcq(rng, f'{nf(Q, 3)} J', [f'{nf(x, 3)} J' for x in (0, -Q, n * R * T * (r - 1), Q / 2, n * 1.5 * R * T)])
    return dict(q=q, o=o, a=a, sol=['Isothermal ideal gas: ΔU = 0 → Q = W = nRT ln r.', f'≈ {nf(Q, 3)} J.'], p=dict(t='isoQ', n=n, T=T, r=r))

def g_cycle(rng):
    t = rng.choice(['rect', 'tri', 'circ', 'carnot', 'fridge', 'carnotW'])
    if t == 'rect':
        P1, P2 = sorted(rng.sample([1, 2, 3, 4, 5, 6, 8, 10], 2)); V1, V2 = sorted(rng.sample([1, 2, 3, 4, 5, 6, 8], 2)); u = rng.choice([100, 1000, 10000])
        W = (P2 - P1) * (V2 - V1) * u; cw = rng.choice([True, False])
        q = f'A gas goes round a rectangle in the P–V diagram with corners ({V1} m^{{3}}, {P1 * u} Pa), ({V2} m^{{3}}, {P1 * u} Pa), ({V2} m^{{3}}, {P2 * u} Pa), ({V1} m^{{3}}, {P2 * u} Pa), {"clockwise" if cw else "anticlockwise"} (V across, P up). Net work done BY the gas is ______ J.'
        if not cw: q = q.replace('Net work done BY the gas is ______ J.', 'Net work done ON the gas is ______ J.')
        return dict(q=q, o=None, a=W, sol=['Work in a cycle = enclosed area; clockwise → done by the gas, anticlockwise → done on it.', f'Area = {P2 - P1} × {u} × {V2 - V1} = {W} J.'], p=dict(t=t, pts=[(V1, P1 * u), (V2, P1 * u), (V2, P2 * u), (V1, P2 * u)]))
    if t == 'tri':
        V1, V2 = sorted(rng.sample([1, 2, 3, 4, 5, 6, 8], 2)); P1, P2 = sorted(rng.sample([100, 200, 300, 400, 500], 2))
        W = F((V2 - V1) * (P2 - P1), 2); need(W.denominator == 1)
        q = f'A system goes A → B → C → A with A = ({V1} m^{{3}}, {P1} Pa), B = ({V2} m^{{3}}, {P2} Pa), C = ({V2} m^{{3}}, {P1} Pa); AB straight, BC at constant volume, CA at constant pressure. Work done by the system in the cycle is ______ J.'
        return dict(q=q, o=None, a=int(W), sol=['Clockwise loop → positive work = area of the triangle.', f'½ × {V2 - V1} × {P2 - P1} = {W} J.'], p=dict(t=t, pts=[(V1, P1), (V2, P2), (V2, P1)]))
    if t == 'circ':
        a_ = rng.choice([50, 100, 140, 150, 200]); b = rng.choice([50, 100, 140, 200]); W = math.pi * a_ * 1e3 * b * 1e-6
        q = f'A gas is taken round a circle-shaped cycle on a P–V diagram whose pressure spans {2 * a_} kPa and volume spans {2 * b} cm^{{3}}. The heat absorbed in one cycle (magnitude) is about :'
        o, a = mcq(rng, f'{nf(W, 3)} J', [f'{nf(x, 3)} J' for x in (W * 4, W / math.pi, W * 10, W / 4, 4 * a_ * b * 1e-3)])
        return dict(q=q, o=o, a=a, sol=['ΔU = 0 over a cycle → Q = W = area.', f'π × {a_} kPa × {b} cm^{{3}} ≈ {nf(W, 3)} J.'], p=dict(t=t, a=a_, b=b))
    if t == 'carnot':
        TH = rng.choice([400, 500, 600, 800, 1000, 1200]); TC = rng.choice([200, 250, 300, 400]); need(TC < TH)
        eta = F(TH - TC, TH) * 100; need(eta.denominator == 1)
        q = f'A Carnot engine works between {TH} K and {TC} K. Its efficiency is ______ %.'
        return dict(q=q, o=None, a=int(eta), sol=['η = 1 − \\f{T_{C}}{T_{H}}.', f'= 1 − \\f{{{TC}}}{{{TH}}} = {eta} %.'], p=dict(t=t, TH=TH, TC=TC))
    if t == 'carnotW':
        TH = rng.choice([400, 500, 600, 800, 1000]); TC = rng.choice([200, 250, 300]); QH = rng.choice([500, 1000, 1200, 2000, 3000, 4000]); need(TC < TH)
        W = F(QH) * (1 - F(TC, TH)); need(W.denominator == 1)
        q = f'A Carnot engine takes {QH} J per cycle from a source at {TH} K and rejects heat to a sink at {TC} K. The work done per cycle is ______ J.'
        return dict(q=q, o=None, a=int(W), sol=['\\f{Q_{C}}{Q_{H}} = \\f{T_{C}}{T_{H}} → W = Q_{H}(1 − \\f{T_{C}}{T_{H}}).', f'= {QH} × {fr(1 - F(TC, TH))} = {W} J.'], p=dict(t=t, TH=TH, TC=TC, QH=QH))
    TH = rng.choice([300, 303, 310, 320, 330]); TC = rng.choice([250, 260, 270, 273, 280]); need(TC < TH)
    cop = F(TC, TH - TC)
    q = f'A Carnot refrigerator keeps its inside at {TC} K in a room at {TH} K. Its coefficient of performance is :'
    o, a = mcq(rng, nf(float(cop), 3), [nf(float(x), 3) for x in (F(TH, TH - TC), F(TH - TC, TH), F(TH - TC, TC), cop * 2)])
    return dict(q=q, o=o, a=a, sol=['β = \\f{T_{C}}{T_{H} − T_{C}}.', f'= \\f{{{TC}}}{{{TH - TC}}} ≈ {nf(float(cop), 3)}.'], p=dict(t='fridge', TH=TH, TC=TC))

def robust(gf):
    def w(rng):
        for _ in range(200):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, OverflowError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(first=g_first, adia=g_adia, iso=g_iso, cycle=g_cycle).items()}
def finish(it): return it

def unf(s):
    s = s.replace('−', '-').strip(); neg = s.startswith('-'); s = s.lstrip('-')
    if s.startswith('\\f{'): a, b = s[3:-1].split('}{'); v = F(int(a), int(b))
    else: v = F(s)
    return -v if neg else v
def shoelace(pts): return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t in ('isoQ', 'isoU') and 'f' in p:
        n = 1.0; dT = p['W'] / (n * R); U = n * p['f'] / 2 * R * dT; return abs(Rv - (U + p['W'] if t == 'isoQ' else U)) < 1e-6
    if t == 'cvdu': return Rv == p['n'] * (p['cp'] - 2) * p['dT']
    if t == 'ratio':
        f = p['f']; Q, U, W = (f / 2 + 1) * R, f / 2 * R, R; a, b, c = [int(x) for x in Rv.split(' : ')]; return abs(a / c - Q / W) < 1e-9 and abs(b / c - U / W) < 1e-9
    if t == 'piston': return close(num(Rv), p['n'] * R * p['dT'] / (1e5 * p['A'] * 1e-4) * 100)
    if t == 'cyc3': return Rv == sum(p['Qs']) - sum(p['Ws'])
    if t == 'P':
        V1, P1 = 1.0, 1.0; V2 = V1 / p['k']; P2 = P1 * (V1 / V2) ** p['g']; return abs(float(unf(Rv)) - P2) < 1e-6 * max(1, P2)
    if t == 'T':   # march along the adiabat with dT = −(γ − 1) T dV / V
        V2 = 1 / p['k']; T2 = p['T1'] * math.exp(-(p['g'] - 1) * integ(lambda v: 1 / v, 1.0, V2))
        return Rv == (round(T2) if p['ask'] == 'final' else abs(round(T2) - p['T1']))
    if t == 'W': return close(num(Rv), integ(lambda v: p['P1'] * (p['V1'] / v) ** p['g'], p['V1'], p['V2']))
    if t == 'expo':
        for g in (5 / 3, 7 / 5, 3 / 2, 4 / 3, 9 / 7, 5 / 4):
            if abs(g / (g - 1) - p['k']) < 1e-9: return abs(float(unf(Rv)) - g) < 1e-9
        return False
    if t == 'gasid':
        nm = {'He': 5 / 3, 'O_{2}': 7 / 5, 'CH_{4}': 4 / 3}; g = nm.get(Rv); return g is not None and abs(p['vr'] ** (g - 1) - p['vr'] ** (2 / p['f'])) < 1e-9
    if t == 'dT':
        W = integ(lambda v: p['n'] * R * p['T'] / v, 1.0, float(p['r'])); return close(num(Rv), p['T'] - W / (p['n'] * p['f'] / 2 * R), 0.006)
    if t == 'isoW': return close(num(Rv), integ(lambda v: p['n'] * R * p['T'] / v, 1.0, p['r']))
    if t == 'isoch':
        dT = p['V'] * (p['P2'] - p['P1']) / (p['n'] * R); return abs(Rv - p['n'] * p['f'] / 2 * R * dT) < 1e-6
    if t == 'isoQ': return close(num(Rv), integ(lambda v: p['n'] * R * p['T'] / v, 1.0, float(p['r'])))
    if t in ('rect', 'tri'): return Rv == abs(shoelace(p['pts']))
    if t == 'circ':
        N = 4000; pts = [(p['b'] * 1e-6 * math.cos(2 * math.pi * k / N), p['a'] * 1e3 * math.sin(2 * math.pi * k / N)) for k in range(N)]; return close(num(Rv), abs(shoelace(pts)))
    if t == 'carnot': return abs(Rv - 100 * (1 - p['TC'] / p['TH'])) < 1e-9
    if t == 'carnotW': return abs(Rv - (p['QH'] - p['QH'] * p['TC'] / p['TH'])) < 1e-9
    if t == 'fridge':
        QC = 1000.0; W = QC * (p['TH'] / p['TC'] - 1); return close(num(Rv), QC / W)
    raise KeyError(t)
