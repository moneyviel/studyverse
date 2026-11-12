"""Practice generators — Physics Unit 7: Properties of Solids and Liquids. check() re-solves each item independently:
elastic and bulk problems from force/area/strain written out afresh, fluids by integrating pressure over depth or by
bisection on the balance condition, drops and bubbles from the surface areas before and after, heat by solving the
heat balance with bisection."""
import math
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
def integ(f, a, b, n=4000):
    h = (b - a) / n; return sum(f(a + (i + 0.5) * h) for i in range(n)) * h
A4 = lambda r: 4 * math.pi * r * r

def g_elas(rng):
    t = rng.choice(['e_ext', 'e_Y', 'e_energy', 'e_hang', 'e_atw', 'e_series', 'e_break'])
    if t == 'e_ext':
        F, L, A, Y = rng.choice([100, 200, 400, 500, 1000]), rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 4, 5]), rng.choice([1, 2])   # A in mm², Y × 10^11
        dl = F * L / (A * 1e-6 * Y * 1e11) * 1e6; half(dl)
        return dict(q=f'A wire {L} m long with cross-section {A} mm^{{2}} (Y = {Y} × 10^{{11}} N m^{{−2}}) carries a tension of {F} N. Its extension is ____ μm (nearest integer).', o=None, a=round(dl),
                    sol=['Δl = \\f{FL}{AY}.', f'= \\f{{{F} × {L}}}{{{A} × 10^{{−6}} × {Y} × 10^{{11}}}} ≈ {nf(dl, 4)} μm.'], p=dict(t=t, F=F, L=L, A=A, Y=Y))
    if t == 'e_Y':
        m, L, r, dl = rng.choice([5, 10, 20, 25, 50]), rng.choice([1, 2, 3]), rng.choice([0.5, 1, 2]), rng.choice([0.1, 0.2, 0.25, 0.5])   # r mm, dl mm
        Y = m * G * L / (math.pi * (r * 1e-3) ** 2 * dl * 1e-3); v = Y / 1e10; half(v)
        return dict(q=f'A {L} m wire of radius {r} mm stretches {dl} mm when it holds {m} kg. Its Young\'s modulus is ____ × 10^{{10}} N m^{{−2}} (nearest integer; g = 10).', o=None, a=round(v),
                    sol=['Y = \\f{mgL}{πr^{2}Δl}.', f'≈ {nf(Y, 4)} N m^{{−2}}.'], p=dict(t=t, m=m, L=L, r=r, dl=dl))
    if t == 'e_energy':
        Y, s = rng.choice([1, 1.1, 2, 2.2]), rng.choice([1, 2, 3, 4, 5]); V = rng.choice([100, 200, 500, 600]); u = 0.5 * Y * 1e11 * (s * 1e-3) ** 2 * V * 1e-6; half(u)
        return dict(q=f'A wire of volume {V} cm^{{3}} (Y = {Y} × 10^{{11}} N m^{{−2}}) is stretched to a strain of {s} × 10^{{−3}}. The elastic energy stored is ____ J (nearest integer).', o=None, a=round(u),
                    sol=['U = ½ × stress × strain × volume = ½Yε^{2}V.', f'= ½ × {Y} × 10^{{11}} × ({s} × 10^{{−3}})^{{2}} × {V} × 10^{{−6}} ≈ {nf(u, 4)} J.'], p=dict(t=t, Y=Y, s=s, V=V))
    if t == 'e_hang':
        rho, S, f = rng.choice([2, 4, 6, 8]), rng.choice([0.6, 1.2, 2.4, 4.8]), rng.choice([1, 0.5, 1 / 3, 0.25])   # ρ ×10^3, S ×10^8
        L = S * 1e8 / (rho * 1e3 * G * f); need(abs(L - round(L)) < 1e-6)
        where = {1: 'on Earth', 0.5: 'on a planet with g half of Earth\'s', 1 / 3: 'on a planet with g one third of Earth\'s', 0.25: 'on a planet with g a quarter of Earth\'s'}[f]
        return dict(q=f'A wire of density {rho} × 10^{{3}} kg m^{{−3}} and breaking stress {S} × 10^{{8}} N m^{{−2}} hangs from its top {where}. The longest length that does not break is ____ m (g_{{Earth}} = 10).', o=None, a=round(L),
                    sol=['The top carries the whole wire: stress = ρgL.', f'L = \\f{{{S} × 10^{{8}}}}{{{rho} × 10^{{3}} × {nf(10 * f, 3)}}} = {nf(L)} m.'], p=dict(t=t, rho=rho, S=S, f=f))
    if t == 'e_atw':
        m1, m2, r = rng.choice([1, 2, 3, 4]), rng.choice([2, 4, 5, 6, 8]), rng.choice([2, 4, 5]); need(m1 != m2); T = 2 * m1 * m2 * G / (m1 + m2); s = T / (math.pi * (r * 1e-5) ** 2 * 2e11)   # strain
        k = 1 / (s * math.pi); need(abs(k - round(k)) < 1e-6)
        return dict(q=f'Blocks of {m1} kg and {m2} kg hang over a smooth pulley on a metal wire of radius {r} × 10^{{−5}} m (Y = 2 × 10^{{11}} N m^{{−2}}). The strain in the wire is \\f{{1}}{{απ}}; α = ____ (g = 10).', o=None, a=round(k),
                    sol=['T = \\f{2m_{1}m_{2}g}{m_{1} + m_{2}}; strain = \\f{T}{πr^{2}Y}.', f'T = {nf(T, 4)} N → α = {round(k)}.'], p=dict(t=t, m1=m1, m2=m2, r=r))
    if t == 'e_series':
        ya, yb = rng.choice([(2, 1), (20, 11), (3, 2), (5, 4), (4, 3), (2, 3)]); La = rng.choice([1, 1.2, 2, 2.2, 3, 4.4]); Lb = La * yb / ya; need(abs(Lb * 100 - round(Lb * 100)) < 1e-6)
        right = f'{nf(Lb, 4)} m'; o, a = mcq(rng, right, [f'{nf(x, 4)} m' for x in (La * ya / yb, La, La * (ya / yb) ** 2, Lb * 2)])
        return dict(q=f'Wires A and B (same area) are joined end to end and pulled. Y_{{A}} : Y_{{B}} = {ya} : {yb} and they stretch by equal amounts. If A is {La} m long, B is :', o=o, a=a,
                    sol=['Same tension and area: Δl = \\f{TL}{AY} → L ∝ Y.', f'L_{{B}} = {La} × \\f{{{yb}}}{{{ya}}} = {right}.'], p=dict(t=t, ya=ya, yb=yb, La=La))
    M1, M2, A1, A2, S = rng.choice([10, 20, 30]), rng.choice([5, 10, 20]), rng.choice([0.004, 0.006, 0.008, 0.01]), rng.choice([0.002, 0.004, 0.005]), rng.choice([6, 8, 10, 12])   # areas cm², S ×10^8
    m1 = S * 1e8 * A1 * 1e-4 / G - M1 - M2; m2 = S * 1e8 * A2 * 1e-4 / G - M2; m = min(m1, m2); need(m > 0 and abs(m - round(m)) < 1e-6)
    return dict(q=f'An upper wire (area {A1} cm^{{2}}) holds a {M1} kg block; from it a lower wire (area {A2} cm^{{2}}) holds a {M2} kg block and a pan. Both wires break at {S} × 10^{{8}} N m^{{−2}}. The largest mass that can go on the pan is ____ kg (g = 10).', o=None, a=round(m),
                sol=['Each wire: (load below it) × g ≤ breaking stress × area.', f'Upper allows {nf(m1)} kg, lower allows {nf(m2)} kg → {nf(m)} kg.'], p=dict(t='e_break', M1=M1, M2=M2, A1=A1, A2=A2, S=S))

def g_bulk(rng):
    t = rng.choice(['b_frac', 'b_depth', 'b_dv', 'b_vol'])
    if t == 'b_frac':
        h, B = rng.choice([500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]), rng.choice([2, 2.1, 2.2, 2.4, 2.5]); f = 1000 * G * h / (B * 1e9) * 100; need(abs(f * 1000 - round(f * 1000)) < 1e-6)
        right = f'{nf(f, 4)}%'; o, a = mcq(rng, right, [f'{nf(x, 4)}%' for x in (f * 10, f / 10, f * 2, f / 2)])
        return dict(q=f'The fractional compression of water {h} m below the sea surface (B = {B} × 10^{{9}} N m^{{−2}}, ρ = 1000 kg m^{{−3}}, g = 10) is :', o=o, a=a,
                    sol=['\\f{ΔV}{V} = \\f{ρgh}{B}.', f'= \\f{{10^{{4}} × {h}}}{{{B} × 10^{{9}}}} = {right}.'], p=dict(t=t, h=h, B=B))
    if t == 'b_depth':
        p, B = rng.choice([0.01, 0.02, 0.04, 0.05, 0.1]), rng.choice([2, 4, 5, 8, 9, 10, 20]); h = p / 100 * B * 1e8 / (1000 * G); need(abs(h - round(h)) < 1e-6)
        return dict(q=f'A rubber ball (B = {B} × 10^{{8}} N m^{{−2}}) is taken deep into the sea (ρ = 1000 kg m^{{−3}}, g = 10). Its volume falls by {p}% at a depth of ____ m.', o=None, a=round(h),
                    sol=['ρgh = B\\f{ΔV}{V}.', f'h = \\f{{{p / 100} × {B} × 10^{{8}}}}{{10^{{4}}}} = {nf(h)} m.'], p=dict(t=t, p=p, B=B))
    if t == 'b_dv':
        a, P, B = rng.choice([5, 10, 20]), rng.choice([2, 5, 7, 10, 14]), rng.choice([0.7, 1.4, 1.6, 2]); dv = (a / 100) ** 3 * P * 1e6 / (B * 1e11) * 1e9; need(abs(dv * 10 - round(dv * 10)) < 1e-6)
        return dict(q=f'A solid cube of edge {a} cm (B = {B} × 10^{{11}} N m^{{−2}}) is placed under an extra pressure of {P} × 10^{{6}} Pa. Its volume shrinks by ____ × 10^{{−1}} mm^{{3}}.', o=None, a=round(dv * 10),
                    sol=['ΔV = \\f{VP}{B}.', f'= \\f{{{a ** 3} × 10^{{−6}} × {P} × 10^{{6}}}}{{{B} × 10^{{11}}}} m^{{3}} = {nf(dv)} mm^{{3}}.'], p=dict(t=t, a=a, P=P, B=B))
    pct, B = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 2, 3]), rng.choice([2, 2.1, 2.15, 2.2]); dP = pct / 100 * B * 1e9 / 1e5; need(abs(dP * 10 - round(dP * 10)) < 1e-6); half(dP)
    return dict(q=f'To squeeze water (B = {B} × 10^{{9}} N m^{{−2}}) by {pct}% of its volume, the pressure must rise by ____ × 10^{{5}} Pa (nearest integer).', o=None, a=round(dP),
                sol=['ΔP = B × \\f{ΔV}{V}.', f'= {B} × 10^{{9}} × {pct / 100} = {nf(dP)} × 10^{{5}} Pa.'], p=dict(t='b_vol', pct=pct, B=B))

def g_fluid(rng):
    t = rng.choice(['f_lift', 'f_bern', 'f_float', 'f_coin', 'f_hyd', 'f_bot', 'f_bub', 'f_osc'])
    if t == 'f_lift':
        v1, v2, Aw, rho = rng.choice([50, 60, 65, 70]), rng.choice([70, 75, 80, 90]), rng.choice([2, 10, 20, 40]), rng.choice([1, 1.2, 1.3]); need(v2 > v1)
        Lf = 0.5 * rho * (v2 ** 2 - v1 ** 2) * Aw; half(Lf)
        return dict(q=f'Air (ρ = {rho} kg m^{{−3}}) flows at {v2} m/s over the top and {v1} m/s under a wing of area {Aw} m^{{2}}. The lift is ____ N (nearest integer).', o=None, a=round(Lf),
                    sol=['Bernoulli: ΔP = ½ρ(v_{top}^{2} − v_{bottom}^{2}); lift = ΔP × area.', f'= ½ × {rho} × ({v2 * v2} − {v1 * v1}) × {Aw} ≈ {nf(Lf, 5)} N.'], p=dict(t=t, v1=v1, v2=v2, Aw=Aw, rho=rho))
    if t == 'f_bern':
        rho, A1, A2, v1 = rng.choice([600, 800, 1000, 1200]), rng.choice([1, 2, 4, 5]), rng.choice([10, 20, 25, 50]), rng.choice([5, 10, 20])   # A1 cm², A2 mm², v1 cm/s
        v2 = v1 * A1 * 100 / A2; dP = 0.5 * rho * ((v2 / 100) ** 2 - (v1 / 100) ** 2); need(v2 > v1); half(dP)
        return dict(q=f'A liquid (ρ = {rho} kg m^{{−3}}) flows through a level pipe from a section of {A1} cm^{{2}} at {v1} cm/s into a section of {A2} mm^{{2}}. The pressure drop is ____ Pa (nearest integer).', o=None, a=round(dP),
                    sol=['Continuity: A_{1}v_{1} = A_{2}v_{2}. Bernoulli: ΔP = ½ρ(v_{2}^{2} − v_{1}^{2}).', f'v_{{2}} = {nf(v2)} cm/s → ΔP ≈ {nf(dP, 4)} Pa.'], p=dict(t=t, rho=rho, A1=A1, A2=A2, v1=v1))
    if t == 'f_float':
        a, m = rng.choice([5, 10, 20]), rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8]); V = a ** 3; inside = m * V; liq = rng.choice([1, 1, 0.8, 1.2]); inside = m * V / liq; need(inside < V)
        out = V - inside; need(abs(out - round(out)) < 1e-6)
        return dict(q=f'A cube of edge {a} cm and relative density {m} floats in a liquid of relative density {liq}. The volume above the surface is ____ cm^{{3}}.', o=None, a=round(out),
                    sol=['Floating: weight = weight of liquid displaced → V_{in} = \\f{ρ_{body}}{ρ_{liquid}}V.', f'V_{{in}} = {nf(inside)} cm^{{3}} → above = {nf(out)} cm^{{3}}.'], p=dict(t=t, a=a, m=m, liq=liq))
    if t == 'f_coin':
        a, d = rng.choice([5, 10, 20]), rng.choice([0.5, 1, 1.5, 2, 2.5, 3.2, 3.87]); m = a * a * d; need(abs(m * 10 - round(m * 10)) < 1e-6); half(m)
        return dict(q=f'A floating wooden cube of edge {a} cm sinks a further {d} cm into water when a coin is put on top. The coin\'s mass is ____ g (nearest integer).', o=None, a=round(m),
                    sol=['Extra weight = extra buoyancy = weight of the extra water pushed aside.', f'= {a} × {a} × {d} cm^{{3}} × 1 g/cm^{{3}} = {nf(m)} g.'], p=dict(t=t, a=a, d=d))
    if t == 'f_hyd':
        a1, a2, F, h = rng.choice([2, 5, 6, 10]), rng.choice([500, 1000, 1500, 2000]), rng.choice([50, 100, 200]), rng.choice([5, 10, 20, 25])
        W = F * a2 / a1 * h / 100; need(abs(W - round(W)) < 1e-6)
        return dict(q=f'A hydraulic lift has pistons of {a1} cm^{{2}} and {a2} cm^{{2}}. A {F} N push on the small piston raises the big piston by {h} cm. The work done is ____ J.', o=None, a=round(W),
                    sol=['Pascal: F_{out} = F × \\f{A_{2}}{A_{1}}; W = F_{out} × h.', f'= {nf(F * a2 / a1)} × {h / 100} = {nf(W)} J.'], p=dict(t=t, a1=a1, a2=a2, F=F, h=h))
    if t == 'f_bot':
        r, h, rho = rng.choice([1, 2, 3, 5]), rng.choice([10, 20, 30, 50]), rng.choice([1, 13.6, 0.8]); Fb = (1e5 + rho * 1e3 * G * h / 100) * math.pi * (r / 100) ** 2; half(Fb)
        return dict(q=f'A tube of radius {r} cm holds {h} cm of a liquid of relative density {rho}, open to the air (P_{{0}} = 10^{{5}} Pa, g = 10). The force on the bottom is ____ N (nearest integer).', o=None, a=round(Fb),
                    sol=['P_{bottom} = P_{0} + ρgh; F = P × πr^{2}.', f'≈ {nf(Fb, 4)} N.'], p=dict(t=t, r=r, h=h, rho=rho))
    if t == 'f_bub':
        V, d, T1, T2 = rng.choice([1, 2, 2.9, 3, 5]), rng.choice([5, 10, 15, 20]), rng.choice([7, 17, 27]), rng.choice([17, 27, 37]); V2 = V * (1e5 + 1e4 * d) / 1e5 * (T2 + 273) / (T1 + 273); half(V2 * 10)
        return dict(q=f'A {V} cm^{{3}} air bubble rises from the bottom of a {d} m deep lake ({T1} °C) to the surface ({T2} °C). Its volume at the surface is ____ × 10^{{−1}} cm^{{3}} (nearest integer; P_{{0}} = 10^{{5}} Pa, g = 10).', o=None, a=round(V2 * 10),
                    sol=['\\f{PV}{T} stays fixed; P_{bottom} = P_{0} + ρgd.', f'V = {V} × \\f{{{nf(1 + d / 10)}}}{{1}} × \\f{{{T2 + 273}}}{{{T1 + 273}}} ≈ {nf(V2, 4)} cm^{{3}}.'], p=dict(t=t, V=V, d=d, T1=T1, T2=T2))
    m, A = rng.choice([10, 20, 40, 50, 100]), rng.choice([0.01, 0.02, 0.04, 0.05])   # m in g, A in m²
    T = 2 * math.pi * math.sqrt(m / 1000 / (1000 * A * G)); y = T / math.pi * 1000; half(y)
    return dict(q=f'A light hollow box of mass {m} g with base area {A} m^{{2}} floats upright in water. Pushed down a little and released, it bobs with period yπ × 10^{{−3}} s; y = ____ (nearest integer; g = 10).', o=None, a=round(y),
                sol=['Extra buoyancy ρAgx → k = ρAg; T = 2π√{\\f{m}{ρAg}}.', f'T ≈ {nf(T, 4)} s.'], p=dict(t='f_osc', m=m, A=A))

def vt(r, rs, rl, eta, g=G): return 2 * r * r * (rs - rl) * g / (9 * eta)
def g_visc(rng):
    t = rng.choice(['v_term', 'v_eta', 'v_merge', 'v_scale', 'v_force', 'v_bubble'])
    if t == 'v_term':
        d, rs, rl, eta = rng.choice([1, 2, 3, 4]), rng.choice([2.5, 7.8, 8.9, 10.5, 11.3]), rng.choice([0.9, 1.0, 1.26, 1.5]), rng.choice([0.5, 1, 1.5, 10])   # mm, g/cc, Pa s
        v = vt(d / 2 * 1e-3, rs * 1e3, rl * 1e3, eta) * 100; half(v * 10)
        return dict(q=f'A sphere of diameter {d} mm and density {rs} g/cm^{{3}} falls through a liquid (density {rl} g/cm^{{3}}, η = {eta} Pa s). Its terminal speed is ____ × 10^{{−1}} cm/s (nearest integer; g = 10).', o=None, a=round(v * 10),
                    sol=['v_{t} = \\f{2r^{2}(ρ − σ)g}{9η}.', f'≈ {nf(v, 4)} cm/s.'], p=dict(t=t, d=d, rs=rs, rl=rl, eta=eta))
    if t == 'v_eta':
        d, rs, rl, v = rng.choice([1, 2, 3, 4]), rng.choice([2.5, 7.8, 8.9]), rng.choice([0.9, 1.0, 1.26]), rng.choice([0.5, 1, 2, 5])   # v cm/s
        eta = vt(d / 2 * 1e-3, rs * 1e3, rl * 1e3, 1) / (v / 100); half(eta * 100)
        return dict(q=f'A {d} mm diameter ball (density {rs} g/cm^{{3}}) reaches a steady {v} cm/s in an oil of density {rl} g/cm^{{3}}. The oil\'s viscosity is ____ × 10^{{−2}} Pa s (nearest integer; g = 10).', o=None, a=round(eta * 100),
                    sol=['η = \\f{2r^{2}(ρ − σ)g}{9v}.', f'≈ {nf(eta, 4)} Pa s.'], p=dict(t=t, d=d, rs=rs, rl=rl, v=v))
    if t == 'v_merge':
        n, v = rng.choice([8, 27, 64, 125, 1000]), rng.choice([1, 2, 5, 10]); k = round(n ** (1 / 3)); V = v * k * k
        return dict(q=f'{n} identical rain drops, each falling at a terminal {v} cm/s, merge into one drop. Its terminal speed is ____ cm/s.', o=None, a=V,
                    sol=[f'Volume × {n} → radius × {k}.', f'v ∝ r^{{2}} → {v} × {k * k} = {V} cm/s.'], p=dict(t=t, n=n, v=v))
    if t == 'v_scale':
        r1, r2, v = rng.choice([2, 3, 4, 6]), rng.choice([1, 2, 3, 6, 8]), rng.choice([4, 8, 12, 20, 36]); need(r1 != r2); V = v * (r2 / r1) ** 2; need(abs(V - round(V)) < 1e-6)
        return dict(q=f'A ball of radius {r1} mm falls at a terminal {v} cm/s in a fluid. Another ball of the same material with radius {r2} mm falls at ____ cm/s.', o=None, a=round(V),
                    sol=['Same materials: v ∝ r^{2}.', f'{v} × (\\f{{{r2}}}{{{r1}}})^{{2}} = {nf(V)} cm/s.'], p=dict(t=t, r1=r1, r2=r2, v=v))
    if t == 'v_force':
        k = rng.choice([2, 3, 4, 5, 8, 10]); f = 1 - 1 / k
        right = f'{nf(f, 3)}Mg'; o, a = mcq(rng, right, [f'{nf(x, 3)}Mg' for x in (1, 1 / k, 1 + 1 / k, k / (k + 1))])
        return dict(q=f'A ball of mass M falls at terminal speed through a liquid whose density is 1/{k} of the ball\'s. The viscous force on it is :', o=o, a=a,
                    sol=['Steady: Mg = buoyancy + viscous force; buoyancy = \\f{Mg}{k}.', f'F = Mg(1 − \\f{{1}}{{{k}}}) = {right}.'], p=dict(t=t, k=k))
    d, rho, v = rng.choice([1, 2, 3, 4]), rng.choice([800, 1000, 1200, 2000]), rng.choice([0.2, 0.5, 1, 2])   # bubble in mm, v cm/s; answer in poise
    eta = vt(d / 2 * 1e-3, 0, -rho, 1) / (v / 100) * 10; half(eta * 10)
    return dict(q=f'An air bubble of diameter {d} mm rises steadily at {v} cm/s through a liquid of density {rho} kg m^{{−3}}. The liquid\'s viscosity is ____ × 10^{{−1}} poise (nearest integer; g = 10; ignore the air\'s weight).', o=None, a=round(eta * 10),
                sol=['Buoyancy = Stokes drag: \\f{4}{3}πr^{3}ρg = 6πηrv → η = \\f{2r^{2}ρg}{9v}.', f'≈ {nf(eta / 10, 4)} Pa s = {nf(eta, 4)} poise.'], p=dict(t='v_bubble', d=d, rho=rho, v=v))

def g_surf(rng):
    t = rng.choice(['s_merge', 's_break', 's_blow', 's_press', 's_cap', 's_contact', 's_ratio', 's_depth', 's_eratio', 's_scale'])
    if t == 's_eratio':
        n = rng.choice([8, 27, 64, 125, 216, 343, 512, 729, 1000]); k = round(n ** (1 / 3)); way = rng.choice(['small', 'big'])
        return dict(q=f'{n} identical drops merge into one big drop. The ratio (total surface energy of the {n} drops) : (surface energy of the big drop) is x : 1 where x = ____.' if way == 'small' else f'{n} identical drops merge into one big drop. The surface energy of the big drop is \\f{{1}}{{x}} of the total of the small drops; x = ____.', o=None, a=k,
                    sol=[f'R = {k}r.', f'\\f{{{n} × 4πr^{{2}}}}{{4π({k}r)^{{2}}}} = {k}.'], p=dict(t=t, n=n, way=way))
    if t == 's_scale':
        f1, f2, f3 = rng.choice([(1, 1, 1), (2, 1, 1), (1, 2, 1), (1, 1, 2), (2, 2, 1), (0.5, 1, 1), (1, 0.5, 2), (3, 1, 1), (1, 3, 1)]); h0 = rng.choice([2, 3, 4, 5, 6, 8])
        H = h0 * f2 / (f1 * f3); need((f1, f2, f3) != (1, 1, 1)); need(abs(H * 100 - round(H * 100)) < 1e-6)
        return dict(q=f'Water rises {h0} cm in a capillary. If the tube radius is made {f1}×, the surface tension {f2}× and the density {f3}× (same contact angle), the new rise is ____ × 10^{{−2}} cm.', o=None, a=round(H * 100),
                    sol=['h = \\f{2T cosθ}{rρg} ∝ \\f{T}{rρ}.', f'{h0} × \\f{{{f2}}}{{{f1} × {f3}}} = {nf(H)} cm.'], p=dict(t=t, f1=f1, f2=f2, f3=f3, h0=h0))
    if t == 's_merge':
        n, r, T = rng.choice([8, 27, 64, 125, 216, 1000]), rng.choice([0.2, 0.5, 1, 2]), rng.choice([0.05, 0.07, 0.072, 0.465])   # r mm
        k = round(n ** (1 / 3)); E = T * 4 * math.pi * (r * 1e-3) ** 2 * (n - k * k) * 1e6; half(E * 10)
        return dict(q=f'{n} identical drops of radius {r} mm (T = {T} N/m) merge into one drop. The surface energy released is ____ × 10^{{−7}} J (nearest integer).', o=None, a=round(E * 10),
                    sol=[f'R = {k}r; area falls from {n} × 4πr^{{2}} to {k * k} × 4πr^{{2}}.', f'E = T × 4πr^{{2}}({n} − {k * k}) ≈ {nf(E, 4)} × 10^{{−6}} J.'], p=dict(t=t, n=n, r=r, T=T))
    if t == 's_break':
        n, R, T = rng.choice([8, 27, 64, 125, 512, 1000]), rng.choice([1, 2, 3]), rng.choice([0.05, 0.07, 0.08]); k = round(n ** (1 / 3)); W = T * 4 * math.pi * (R * 1e-3) ** 2 * (k - 1) * 1e6; half(W * 10)
        return dict(q=f'A drop of radius {R} mm (T = {T} N/m) is broken into {n} identical droplets. The work needed is ____ × 10^{{−7}} J (nearest integer).', o=None, a=round(W * 10),
                    sol=[f'Each droplet r = R/{k}; total area = {n} × 4π(R/{k})^{{2}} = {k} × 4πR^{{2}}.', f'W = T × 4πR^{{2}}({k} − 1) ≈ {nf(W, 4)} × 10^{{−6}} J.'], p=dict(t=t, n=n, R=R, T=T))
    if t == 's_blow':
        r1, r2, T = rng.choice([1, 1.5, 2, 3, 3.5]), rng.choice([2, 2.5, 4, 5, 6, 7]), rng.choice([0.025, 0.03, 0.035, 0.04, 0.05]); need(r2 > r1); W = 2 * T * 4 * math.pi * ((r2 / 100) ** 2 - (r1 / 100) ** 2) * 1e6; half(W)
        return dict(q=f'A soap bubble (T = {T} N/m) is blown from radius {r1} cm to {r2} cm. The work done is ____ μJ (nearest integer).', o=None, a=round(W),
                    sol=['Two surfaces: W = 2T × 4π(r_{2}^{2} − r_{1}^{2}).', f'≈ {nf(W, 5)} μJ.'], p=dict(t=t, r1=r1, r2=r2, T=T))
    if t == 's_press':
        kind = rng.choice(['soap bubble in air', 'drop of liquid', 'air bubble inside a liquid']); r, T = rng.choice([0.2, 0.5, 1, 1.5, 2, 2.5, 4, 5]), rng.choice([0.03, 0.035, 0.04, 0.05, 0.07, 0.072, 0.1]); f = 4 if kind.startswith('soap') else 2
        P = f * T / (r * 1e-3); half(P)
        return dict(q=f'The excess pressure inside a {kind} of radius {r} mm (T = {T} N/m) is ____ Pa (nearest integer).', o=None, a=round(P),
                    sol=['Each surface adds \\f{2T}{r}; a soap bubble has two surfaces, a drop or an air bubble in liquid has one.', f'ΔP = \\f{{{f}T}}{{r}} ≈ {nf(P, 4)} Pa.'], p=dict(t=t, kind=kind, r=r, T=T))
    if t == 's_cap':
        r, T, th, tilt = rng.choice([0.1, 0.2, 0.25, 0.5]), rng.choice([0.07, 0.072, 0.05]), rng.choice([0, 0, 60]), rng.choice([0, 30, 60]); h = 2 * T * math.cos(math.radians(th)) / (r * 1e-3 * 1000 * G); L = h / math.cos(math.radians(tilt)) * 100; half(L * 10)
        return dict(q=f'A capillary of radius {r} mm stands in water (T = {T} N/m, contact angle {th}°){"" if tilt == 0 else f" tilted {tilt}° from the vertical"}. The length of water column in the tube is ____ × 10^{{−1}} cm (nearest integer; g = 10).', o=None, a=round(L * 10),
                    sol=['Vertical rise h = \\f{2T cosθ}{rρg}; a tilted tube holds a longer column h/cosα.', f'≈ {nf(L, 4)} cm.'], p=dict(t=t, r=r, T=T, th=th, tilt=tilt))
    if t == 's_contact':
        r1, r2 = rng.choice([(1, 2), (2, 3), (2, 4), (3, 6), (4, 6), (1, 3), (3, 4)]); R = r1 * r2 / (r2 - r1); need(abs(R * 100 - round(R * 100)) < 1e-6)
        right = f'{nf(R, 4)} cm'; o, a = mcq(rng, right, [f'{nf(x, 4)} cm' for x in (r1 + r2, r2 - r1, r1 * r2 / (r1 + r2), (r1 + r2) / 2)])
        return dict(q=f'Soap bubbles of radius {r1} cm and {r2} cm stick together. The radius of curvature of the common film is :', o=o, a=a,
                    sol=['\\f{1}{r} = \\f{1}{r_{1}} − \\f{1}{r_{2}} (difference of excess pressures).', f'r = \\f{{{r1} × {r2}}}{{{r2} − {r1}}} = {right}.'], p=dict(t=t, r1=r1, r2=r2))
    if t == 's_ratio':
        k = rng.choice([2, 3, 4, 5]); ask = rng.choice(['volume', 'area'])
        right = f'1 : {k ** 3 if ask == "volume" else k * k}'; o, a = mcq(rng, right, [f'1 : {x}' for x in (k, k * k, k ** 3, k ** 4) if f'1 : {x}' != right] + [f'{k} : 1'])
        return dict(q=f'The excess pressure inside soap bubble A is {k} times that inside bubble B. Their {ask}s are in the ratio A : B =', o=o, a=a,
                    sol=['ΔP = \\f{4T}{r} → r_{A} = \\f{r_{B}}{' + str(k) + '}.', f'{ask} ratio = {right}.'], p=dict(t=t, k=k, ask=ask))
    r, d, T = rng.choice([0.2, 0.5, 1, 2]), rng.choice([5, 10, 20, 30, 50]), rng.choice([0.05, 0.06, 0.07, 0.072, 0.095])
    P = 1000 * G * d / 100 + 2 * T / (r * 1e-3); half(P)
    return dict(q=f'An air bubble of radius {r} mm is {d} cm below the surface of water (T = {T} N/m). The pressure inside it exceeds the atmosphere by ____ Pa (nearest integer; g = 10).', o=None, a=round(P),
                sol=['Inside = P_{0} + ρgh + \\f{2T}{r} (one surface).', f'= {nf(1000 * G * d / 100)} + {nf(2 * T / (r * 1e-3), 4)} ≈ {nf(P, 5)} Pa.'], p=dict(t='s_depth', r=r, d=d, T=T))

def g_heat(rng):
    t = rng.choice(['h_fall', 'h_mix', 'h_ice', 'h_rod', 'h_bullet', 'h_cond', 'h_area'])
    if t == 'h_fall':
        h, c = rng.choice([50, 100, 200, 420, 840]), rng.choice([4200, 4180]); dT = G * h / c * 100; half(dT)
        return dict(q=f'Water falls {h} m and all its energy turns into heat (c = {c} J kg^{{−1}} K^{{−1}}, g = 10). Its temperature rises by ____ × 10^{{−2}} K (nearest integer).', o=None, a=round(dT),
                    sol=['mgh = mcΔT → ΔT = \\f{gh}{c}.', f'≈ {nf(dT / 100, 4)} K.'], p=dict(t=t, h=h, c=c))
    if t == 'h_mix':
        m1, t1, m2, t2 = rng.choice([1, 2, 3, 5]), rng.choice([20, 30, 40]), rng.choice([1, 2, 4]), rng.choice([60, 70, 80, 90]); T = (m1 * t1 + m2 * t2) / (m1 + m2); half(T * 10)
        return dict(q=f'{m1} kg of water at {t1} °C is mixed with {m2} kg of water at {t2} °C (no heat lost). The final temperature is ____ × 10^{{−1}} °C (nearest integer).', o=None, a=round(T * 10),
                    sol=['Heat lost = heat gained.', f'T = \\f{{{m1} × {t1} + {m2} × {t2}}}{{{m1 + m2}}} ≈ {nf(T, 4)} °C.'], p=dict(t=t, m1=m1, t1=t1, m2=m2, t2=t2))
    if t == 'h_ice':
        mi, ti, mw, tw = rng.choice([1, 2, 5, 10]), rng.choice([0, -5, -10]), rng.choice([20, 50, 100]), rng.choice([25, 30, 40, 50])
        Q = lambda T: mi * (2100 * (0 - ti) + 3.36e5 + 4200 * T) - mw * 4200 * (tw - T); need(Q(0) < 0)
        T = bisect(Q, 0, tw); half(T * 10)
        return dict(q=f'{mi} kg of ice at {ti} °C is dropped into {mw} kg of water at {tw} °C. The final temperature is ____ × 10^{{−1}} °C (nearest integer; c_{{ice}} = 2100, c_{{water}} = 4200 J kg^{{−1}} K^{{−1}}, L = 3.36 × 10^{{5}} J/kg).', o=None, a=round(T * 10),
                    sol=['Ice: warm to 0 °C, melt, warm to T. Water: cool from its temperature to T. Set gain = loss.', f'T ≈ {nf(T, 4)} °C.'], p=dict(t=t, mi=mi, ti=ti, mw=mw, tw=tw))
    if t == 'h_rod':
        L, a, dT = rng.choice([50, 60, 100, 120, 200]), rng.choice([12, 17, 19, 24]), rng.choice([20, 50, 70, 100]); dL = L * a * 1e-6 * dT * 1e4; half(dL)
        return dict(q=f'A rod {L} cm long (α = {a} × 10^{{−6}} K^{{−1}}) is heated by {dT} K. It gets longer by ____ × 10^{{−4}} cm (nearest integer).', o=None, a=round(dL),
                    sol=['ΔL = LαΔT.', f'= {L} × {a} × 10^{{−6}} × {dT} ≈ {nf(dL / 1e4, 4)} cm.'], p=dict(t=t, L=L, a=a, dT=dT))
    if t == 'h_bullet':
        Q, Tm, T0 = rng.choice([250, 500, 625, 1000, 1250]), 600, rng.choice([300, 350, 400]); m = Q / (125 * (Tm - T0) + 2.5e4) * 1000; half(m * 10)
        return dict(q=f'A lead bullet at {T0} K stops in a block and just melts (melting point 600 K, c = 125 J kg^{{−1}} K^{{−1}}, L = 2.5 × 10^{{4}} J/kg). If this needs {Q} J, its mass is ____ × 10^{{−1}} g (nearest integer).', o=None, a=round(m * 10),
                    sol=['Q = m(cΔT + L).', f'm = \\f{{{Q}}}{{125 × {600 - T0} + 25000}} ≈ {nf(m, 4)} g.'], p=dict(t=t, Q=Q, T0=T0))
    if t == 'h_cond':
        k1, k2, k3, a3 = rng.choice([30, 60, 90]), rng.choice([60, 120, 150]), rng.choice([45, 90, 135, 180]), rng.choice([1, 2])
        th = (k1 + k2) * 100 / (k1 + k2 + k3 * a3); half(th * 10)
        return dict(q=f'Rods 1 and 2 (k = {k1} and {k2} W m^{{−1}} K^{{−1}}, same length and area A) are side by side from a 100 °C source to a junction; rod 3 (k = {k3}, same length, area {a3}A) goes from the junction to 0 °C. The junction temperature is ____ × 10^{{−1}} °C (nearest integer).', o=None, a=round(th * 10),
                    sol=['Steady state: heat in through 1 and 2 = heat out through 3.', f'({k1} + {k2})(100 − θ) = {k3} × {a3} × θ → θ ≈ {nf(th, 4)} °C.'], p=dict(t=t, k1=k1, k2=k2, k3=k3, a3=a3))
    l, w, a, dT = rng.choice([5, 9, 10, 20]), rng.choice([2, 4, 5, 10]), rng.choice([1.2, 2.4, 3.1]), rng.choice([9, 10, 20, 50]); dA = 2 * a * 1e-5 * l * w * dT * 1e-4 * 1e8; half(dA * 10)
    return dict(q=f'A {l} cm × {w} cm plate (α = {a} × 10^{{−5}} K^{{−1}}) is heated by {dT} K. Its area grows by ____ × 10^{{−9}} m^{{2}} (nearest integer).', o=None, a=round(dA * 10),
                sol=['Area expansion β = 2α: ΔA = 2αAΔT.', f'≈ {nf(dA / 1e8, 4)} m^{{2}}.'], p=dict(t='h_area', l=l, w=w, a=a, dT=dT))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(elas=g_elas, bulk=g_bulk, fluid=g_fluid, visc=g_visc, surf=g_surf, heat=g_heat).items()}
def finish(it): return it
def check(it):
    p = it['p']; t = p['t']; Rv = it['o'][it['a']] if it.get('o') else it['a']
    if t == 'e_ext':
        k = p['A'] * 1e-6 * p['Y'] * 1e11 / p['L']; return Rv == round(bisect(lambda x: k * x - p['F'], 0, 1) * 1e6)   # wire as a spring k = AY/L
    if t == 'e_Y':
        stress = p['m'] * G / (math.pi * (p['r'] * 1e-3) ** 2); strain = p['dl'] * 1e-3 / p['L']; return Rv == round(stress / strain / 1e10)
    if t == 'e_energy':
        Y = p['Y'] * 1e11; e = p['s'] * 1e-3; return Rv == round(integ(lambda x: Y * x, 0, e) * p['V'] * 1e-6)
    if t == 'e_hang': return Rv == round(bisect(lambda L: p['rho'] * 1e3 * G * p['f'] * L - p['S'] * 1e8, 0, 1e6))
    if t == 'e_atw':
        m1, m2 = p['m1'], p['m2']; a = abs(m2 - m1) * G / (m1 + m2); T = min(m1, m2) * (G + a); s = T / (math.pi * (p['r'] * 1e-5) ** 2 * 2e11); return Rv == round(1 / (s * math.pi))
    if t == 'e_series': return close(num(Rv), bisect(lambda Lb: p['La'] / p['ya'] - Lb / p['yb'], 0, 100), 1e-4)
    if t == 'e_break':
        up = bisect(lambda m: (p['M1'] + p['M2'] + m) * G - p['S'] * 1e8 * p['A1'] * 1e-4, -1e4, 1e5); lo = bisect(lambda m: (p['M2'] + m) * G - p['S'] * 1e8 * p['A2'] * 1e-4, -1e4, 1e5); return Rv == round(min(up, lo))
    if t == 'b_frac': return close(num(Rv.rstrip('%')), integ(lambda y: 1000 * G, 0, p['h'], 100) / (p['B'] * 1e9) * 100, 1e-4)
    if t == 'b_depth': return Rv == round(bisect(lambda h: 1000 * G * h / (p['B'] * 1e8) - p['p'] / 100, 0, 1e6))
    if t == 'b_dv': V = (p['a'] / 100) ** 3; return Rv == round(V * p['P'] * 1e6 / (p['B'] * 1e11) * 1e9 * 10)
    if t == 'b_vol': return Rv == round(bisect(lambda P: P / (p['B'] * 1e9) - p['pct'] / 100, 0, 1e10) / 1e5)
    if t == 'f_lift': return Rv == round((p['rho'] * p['v2'] ** 2 / 2 - p['rho'] * p['v1'] ** 2 / 2) * p['Aw'])
    if t == 'f_bern':
        v1 = p['v1'] / 100; v2 = v1 * p['A1'] * 1e-4 / (p['A2'] * 1e-6); return Rv == round(p['rho'] * (v2 * v2 - v1 * v1) / 2)
    if t == 'f_float':
        V = p['a'] ** 3; sub = bisect(lambda v: v * p['liq'] - V * p['m'], 0, V); return Rv == round(V - sub)
    if t == 'f_coin': return Rv == round(p['a'] ** 2 * p['d'] * 1.0)
    if t == 'f_hyd':
        dsmall = p['h'] / 100 * p['a2'] / p['a1']; return Rv == round(p['F'] * dsmall)   # input work = output work
    if t == 'f_bot':
        r = p['r'] / 100; P = 1e5 + integ(lambda y: p['rho'] * 1e3 * G, 0, p['h'] / 100, 200); return Rv == round(P * math.pi * r * r)
    if t == 'f_bub':
        P1 = 1e5 + 1000 * G * p['d']; return Rv == round(p['V'] * P1 / (p['T1'] + 273) * (p['T2'] + 273) / 1e5 * 10)
    if t == 'f_osc':
        m = p['m'] / 1000; k = 1000 * p['A'] * G; return Rv == round(2 * math.pi / math.sqrt(k / m) / math.pi * 1000)
    if t == 'v_term':
        r = p['d'] / 2 * 1e-3; W = 4 / 3 * math.pi * r ** 3 * (p['rs'] - p['rl']) * 1e3 * G; v = bisect(lambda v: 6 * math.pi * p['eta'] * r * v - W, 0, 100); return Rv == round(v * 1000)
    if t == 'v_eta':
        r = p['d'] / 2 * 1e-3; W = 4 / 3 * math.pi * r ** 3 * (p['rs'] - p['rl']) * 1e3 * G; return Rv == round(W / (6 * math.pi * r * p['v'] / 100) * 100)
    if t == 'v_merge': return Rv == round(p['v'] * (p['n'] ** (1 / 3)) ** 2)
    if t == 'v_scale': return Rv == round(p['v'] * (p['r2'] / p['r1']) ** 2)
    if t == 'v_force': return close(num(Rv.replace('Mg', '')), 1 - 1 / p['k'], 3e-3)
    if t == 'v_bubble':
        r = p['d'] / 2 * 1e-3; B = 4 / 3 * math.pi * r ** 3 * p['rho'] * G; eta = B / (6 * math.pi * r * p['v'] / 100); return Rv == round(eta * 10 * 10)
    if t == 's_merge':
        r = p['r'] * 1e-3; R = (p['n'] * r ** 3) ** (1 / 3); return Rv == round(p['T'] * (p['n'] * A4(r) - A4(R)) * 1e7)
    if t == 's_break':
        R = p['R'] * 1e-3; r = R / p['n'] ** (1 / 3); return Rv == round(p['T'] * (p['n'] * A4(r) - A4(R)) * 1e7)
    if t == 's_blow': return Rv == round(p['T'] * 2 * (A4(p['r2'] / 100) - A4(p['r1'] / 100)) * 1e6)
    if t == 's_press':
        n = 2 if p['kind'].startswith('soap') else 1; return Rv == round(n * 2 * p['T'] / (p['r'] * 1e-3))
    if t == 's_cap':
        r = p['r'] * 1e-3; h = bisect(lambda h: 1000 * G * h * math.pi * r * r - p['T'] * math.cos(math.radians(p['th'])) * 2 * math.pi * r, 0, 10); return Rv == round(h / math.cos(math.radians(p['tilt'])) * 1000)
    if t == 's_contact': return close(num(Rv), bisect(lambda r: 4 / r - (4 / p['r1'] - 4 / p['r2']), 0.01, 1000), 1e-4)
    if t == 's_ratio':
        rA, rB = 1 / p['k'], 1.0; want = (rA / rB) ** (3 if p['ask'] == 'volume' else 2); a, b = [float(x) for x in Rv.split(' : ')]; return abs(a / b - want) < 1e-9
    if t == 's_eratio':
        r = 1.0; R = (p['n'] * r ** 3) ** (1 / 3); return Rv == round(p['n'] * A4(r) / A4(R))
    if t == 's_scale':
        h = lambda r, T, rho: bisect(lambda x: rho * G * x * math.pi * r * r - T * 2 * math.pi * r, 0, 100)
        return Rv == round(p['h0'] * h(p['f1'], p['f2'], p['f3']) / h(1, 1, 1) * 100)
    if t == 's_depth': return Rv == round(1000 * G * p['d'] / 100 + 2 * p['T'] / (p['r'] * 1e-3))
    if t == 'h_fall': return Rv == round(bisect(lambda dT: p['c'] * dT - G * p['h'], 0, 10) * 100)
    if t == 'h_mix': return Rv == round(bisect(lambda T: p['m1'] * (T - p['t1']) - p['m2'] * (p['t2'] - T), 0, 100) * 10)
    if t == 'h_ice':
        T = (p['mw'] * 4200 * p['tw'] - p['mi'] * (2100 * -p['ti'] + 3.36e5)) / ((p['mw'] + p['mi']) * 4200); return Rv == round(T * 10)
    if t == 'h_rod': return Rv == round(p['L'] * (1 + p['a'] * 1e-6 * p['dT']) * 1e4 - p['L'] * 1e4)
    if t == 'h_bullet': return Rv == round(bisect(lambda m: m / 1000 * (125 * (600 - p['T0']) + 2.5e4) - p['Q'], 0, 1e4) * 10)
    if t == 'h_cond':
        th = bisect(lambda th: (p['k1'] + p['k2']) * (100 - th) - p['k3'] * p['a3'] * th, 0, 100); return Rv == round(th * 10)
    if t == 'h_area':
        a = p['a'] * 1e-5; A0 = p['l'] * p['w'] * 1e-4; A1 = p['l'] * (1 + a * p['dT']) * p['w'] * (1 + a * p['dT']) * 1e-4; return abs(Rv - (A1 - A0) * 1e9) <= max(0.6, 2e-3 * Rv)   # 2αAΔT drops the tiny α²AΔT² term
    raise KeyError(t)
