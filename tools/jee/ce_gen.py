"""Our own practice questions for Current Electricity. Each item carries its parameters (p); check() re-solves it
with the exact nodal circuit solver or another independent route and must match the marked answer."""
import random, math
from fractions import Fraction as F
from common import mcq, nf, fr, solve_net, solve_dc, tri, square, tetra, cube, hexspoke, hexring
par = lambda *r: 1 / sum(1 / F(x) for x in r)
TINY = F(1, 10 ** 12)

def g_cells(rng):
    t = rng.choice(['ratio', 'internal', 'same', 'reverse', 'terminal'])
    if t == 'ratio':
        E1, r1, E2, r2 = rng.choice([(1, 2, 2, 1), (2, 1, 3, 2), (1, 1, 2, 1), (3, 1, 3, 2), (2, 2, 4, 1)]); R = rng.choice([2, 4, 6, 8])
        I1 = F(E1 + E2, R + r1 + r2); Eq = (F(E1, r1) + F(E2, r2)) / (F(1, r1) + F(1, r2)); rq = par(r1, r2); I2 = Eq / (R + rq)
        k = I1 / I2
        q = f'Two cells of emf {E1} V and {E2} V with internal resistances {r1} Ω and {r2} Ω are joined (a) in series, (b) in parallel (like terminals together), each time with an external {R} Ω resistor. The ratio of currents I_{{series}} : I_{{parallel}} is :'
        o, a = mcq(rng, fr(k), [fr(1 / k), fr(k * 2), fr(k + F(1, 2)), fr(F(E1 + E2, R) / (F(E1 + E2, 2) / R)), fr(k - F(1, 3))])
        sol = [f'Series: I = \\f{{{E1 + E2}}}{{{R} + {r1 + r2}}} = {fr(I1)} A.', f'Parallel: E_{{eq}} = \\f{{E_{{1}}/r_{{1}} + E_{{2}}/r_{{2}}}}{{1/r_{{1}} + 1/r_{{2}}}} = {fr(Eq)} V, r_{{eq}} = {fr(rq)} Ω → I = {fr(I2)} A.', f'Ratio = {fr(k)}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='ratio', E1=E1, r1=r1, E2=E2, r2=r2, R=R))
    if t == 'internal':
        E, r = rng.choice([(F(3, 2), 1), (2, 1), (3, 2), (6, 1), (F(9, 2), F(1, 2))]); R1, R2 = rng.sample([1, 2, 4, 5, 8, 10], 2)
        I1, I2 = E / (R1 + F(r)), E / (R2 + F(r))
        q = f'A cell gives a current of {nf(I1)} A through a {R1} Ω resistor and {nf(I2)} A through a {R2} Ω resistor. Its internal resistance is ______ Ω.'
        if (F(r) * 100).denominator != 1 or (I1 * 10000).denominator != 1 or (I2 * 10000).denominator != 1: return g_cells(rng)
        if F(r).denominator != 1: return g_cells(rng)
        return dict(q=q, o=None, a=int(r), sol=[f'E = {nf(I1)}({R1} + r) = {nf(I2)}({R2} + r).', f'Solve: r = \\f{{{nf(I2)}×{R2} − {nf(I1)}×{R1}}}{{{nf(I1)} − {nf(I2)}}} = {int(r)} Ω (E = {nf(E)} V).'], p=dict(t='internal', I1=str(I1), R1=R1, I2=str(I2), R2=R2))
    if t == 'same':
        R = rng.choice([2, 3, 4, 5, 6, 8, 10]); n = rng.choice([2, 3])
        q = f'{n} identical cells, each of emf E and internal resistance r, send the same current through an external {R} Ω resistor whether they are joined in series or in parallel. Then r = ______ Ω.'
        return dict(q=q, o=None, a=R, sol=[f'Series: I = \\f{{{n}E}}{{{R} + {n}r}}; parallel: I = \\f{{E}}{{{R} + r/{n}}}.', f'Equate: {n}({R} + r/{n}) = {R} + {n}r → {n * R} + r = {R} + {n}r → r = {R} Ω (always r = R).'], p=dict(t='same', R=R, n=n))
    if t == 'reverse':
        E1, r1, E2, r2 = rng.choice([(1, 2, 2, 1), (2, 1, 4, 1), (1, 1, 3, 1), (2, 2, 6, 2), (3, 1, 1, 1)]); R = rng.choice([1, 2, 3])
        Eq = (-F(E1, r1) + F(E2, r2)) / (F(1, r1) + F(1, r2)); I = abs(Eq) / (R + par(r1, r2))
        q = f'Cells of emf {E1} V (r = {r1} Ω) and {E2} V (r = {r2} Ω) are joined in parallel with OPPOSITE terminals together, across a {R} Ω resistor. The current through the resistor is :'
        o, a = mcq(rng, fr(I) + ' A', [fr((F(E1, r1) + F(E2, r2)) / (F(1, r1) + F(1, r2)) / (R + par(r1, r2))) + ' A', fr(F(abs(E2 - E1), R)) + ' A', fr(F(abs(E2 - E1), R + r1 + r2)) + ' A', fr(I * 2) + ' A', fr(I / 2) + ' A', fr(I + 1) + ' A'])
        return dict(q=q, o=o, a=a, sol=['With one cell reversed its emf enters with a minus sign.', f'E_{{eq}} = \\f{{−{E1}/{r1} + {E2}/{r2}}}{{1/{r1} + 1/{r2}}} = {fr(Eq)} V, r_{{eq}} = {fr(par(r1, r2))} Ω.', f'I = \\f{{{fr(abs(Eq))}}}{{{R} + {fr(par(r1, r2))}}} = {fr(I)} A.'], p=dict(t='reverse', E1=E1, r1=r1, E2=E2, r2=r2, R=R))
    E, r, R = rng.choice([(12, 1, 5), (6, F(1, 2), 2), (9, 1, 8), (10, 2, 3), (3, F(1, 2), 1)])
    V = E * F(R) / (R + F(r))
    q = f'A cell of emf {E} V and internal resistance {fr(r)} Ω is connected to a {R} Ω resistor. The terminal potential difference of the cell is :'
    o, a = mcq(rng, fr(V) + ' V', [str(E) + ' V', fr(E * F(r) / (R + F(r))) + ' V', fr(E - V / 2) + ' V', fr(F(E) * R / (R + 2 * F(r))) + ' V'])
    return dict(q=q, o=o, a=a, sol=[f'I = \\f{{{E}}}{{{R} + {fr(r)}}} = {fr(E / (R + F(r)))} A.', f'V = E − Ir = IR = {fr(V)} V.'], p=dict(t='terminal', E=E, r=str(r), R=R))

def g_power(rng):
    t = rng.choice(['rated', 'series', 'cut', 'electrons', 'heater'])
    if t == 'rated':
        P0, V0 = rng.choice([40, 50, 60, 75, 100, 150, 200]), rng.choice([100, 120, 200, 220, 240]); V = rng.choice([V0 // 2] + ([V0 // 4, V0 * 3 // 4] if V0 % 4 == 0 else []))
        P = F(P0) * F(V, V0) ** 2
        q = f'A bulb rated {P0} W – {V0} V is run on a {V} V supply. Its power is :'
        o, a = mcq(rng, nf(P) + ' W', [nf(F(P0) * F(V, V0)) + ' W', str(P0) + ' W', nf(P * 2) + ' W', nf(P / 2) + ' W'])
        return dict(q=q, o=o, a=a, sol=[f'R = \\f{{V^{{2}}}}{{P}} = \\f{{{V0}^{{2}}}}{{{P0}}} = {nf(F(V0 * V0, P0))} Ω (resistance does not change).', f'P = \\f{{{V}^{{2}}}}{{R}} = {nf(P)} W.'], p=dict(t='rated', P0=P0, V0=V0, V=V))
    if t == 'series':
        n = rng.choice([2, 3, 4, 5, 6, 8, 10]); p0 = rng.choice([25, 40, 60, 75, 100, 120, 200])
        q = f'{n} identical bulbs, each drawing {p0} W when connected alone to the mains, are joined in series across the same mains. The total power drawn is :'
        o, a = mcq(rng, nf(F(p0, n)) + ' W', [nf(F(p0, n * n)) + ' W', str(n * p0) + ' W', str(p0) + ' W', nf(F(p0 * n * n)) + ' W'])
        return dict(q=q, o=o, a=a, sol=['Each bulb has R = V^{2}/p.', f'In series R_{{total}} = {n}R → P = \\f{{V^{{2}}}}{{{n}R}} = \\f{{{p0}}}{{{n}}} = {nf(F(p0, n))} W.'], p=dict(t='bseries', n=n, p0=p0))
    if t == 'cut':
        n = rng.choice([2, 3, 4]); 
        q = f'A wire dissipates power W when connected to a supply. It is cut into {n} equal pieces which are joined in parallel across the same supply. The new power is :'
        o, a = mcq(rng, f'{n * n}W', [f'{n}W', f'W/{n * n}', f'W/{n}', 'W'])
        return dict(q=q, o=o, a=a, sol=[f'Each piece R/{n}; {n} in parallel → R/{n * n}.', f'P = V^{{2}}/(R/{n * n}) = {n * n}W.'], p=dict(t='cut', n=n))
    if t == 'electrons':
        P0, V0 = rng.choice([(110, 220), (100, 200), (60, 240), (40, 160), (16, 8)]); I = F(P0, V0); N = I / F(16, 10 ** 20)
        q = f'The number of electrons passing per second through the filament of a {P0} W, {V0} V bulb working at its rating is (e = 1.6 × 10^{{−19}} C) :'
        return dict(q=q, o=(lambda o: o)(mcq(rng, nf(N), [nf(N * 2), nf(N / 10), nf(N * 10), nf(F(P0 * V0) / F(16, 10 ** 20))])[0]), a=None, sol=[f'I = P/V = {nf(I)} A.', f'n = I/e = {nf(N)} per second.'], p=dict(t='electrons', P0=P0, V0=V0), right=nf(N))
    P0, V0 = rng.choice([(1000, 100), (500, 100), (2000, 200), (800, 200)]); Rh = F(V0 * V0, P0); k = rng.choice([2, 4]); Pn = F(P0, k * k)
    Rs = Rh * (k - 1)
    q = f'A heater rated {P0} W at {V0} V is connected in series with a resistor R across the same {V0} V supply. For the heater to give {nf(Pn)} W, R must be ______ Ω.'
    if Rs.denominator != 1: return g_power(rng)
    return dict(q=q, o=None, a=int(Rs), sol=[f'R_{{heater}} = \\f{{{V0}^{{2}}}}{{{P0}}} = {nf(Rh)} Ω.', f'Power ∝ I^{{2}}: {nf(Pn)} W is 1/{k * k} of {P0} W → current must be 1/{k} → total resistance {k} × {nf(Rh)} = {nf(Rh * k)} Ω.', f'R = {nf(Rh * k)} − {nf(Rh)} = {int(Rs)} Ω.'], p=dict(t='heater', P0=P0, V0=V0, k=k))

def g_pot(rng):
    t = rng.choice(['shunt', 'shunt', 'compare'])
    if t == 'shunt':
        r = rng.choice([1, 2, 3, 4, 5, 6]); R1, R2 = rng.sample([2, 3, 4, 6, 8, 10, 12, 15], 2); L1 = rng.choice([100, 120, 150, 200])
        L2 = F(L1) * (F(R2) / (R2 + r)) / (F(R1) / (R1 + r))
        if L2.denominator != 1 or not (50 < L2 < 400): return g_pot(rng)
        q = f'In a potentiometer experiment, a cell shunted by {R1} Ω balances at {L1} cm. When the shunt is changed to {R2} Ω the balance length becomes {int(L2)} cm. The internal resistance of the cell is ______ Ω.'
        return dict(q=q, o=None, a=r, sol=['Balance length ∝ terminal voltage \\f{ER}{R + r}.', f'\\f{{{R1}/({R1} + r)}}{{{R2}/({R2} + r)}} = \\f{{{L1}}}{{{int(L2)}}}.', f'Solving: r = {r} Ω.'], p=dict(t='shunt', R1=R1, R2=R2, L1=L1, L2=int(L2)))
    l1, l2 = rng.choice([(300, 200), (250, 150), (400, 300), (360, 240), (450, 300)])
    q = f'In a potentiometer, two cells balance at {l1} cm and {l2} cm. The ratio of their emfs is :'
    o, a = mcq(rng, fr(F(l1, l2)), [fr(F(l2, l1)), fr(F(l1 + l2, l1 - l2)), fr(F(l1 - l2, l1 + l2)), fr(F(l1, l2) ** 2)])
    return dict(q=q, o=o, a=a, sol=['No current is drawn at balance, so emf ∝ balancing length.', f'E_{{1}}/E_{{2}} = {l1}/{l2} = {fr(F(l1, l2))}.'], p=dict(t='cmp', l1=l1, l2=l2))

def g_meter(rng):
    t = rng.choice(['read', 'rv', 'range', 'shunt'])
    if t == 'read':
        R1, R2, Rv, E = rng.choice([50, 100, 200, 300, 400]), rng.choice([50, 100, 200, 300, 400]), rng.choice([100, 200, 300, 400, 600, 1000]), rng.choice([3, 4, 6, 9, 12])
        V = E * par(R1, Rv) / (par(R1, Rv) + R2)
        q = f'Resistors {R1} Ω and {R2} Ω are in series with an ideal {E} V battery. A voltmeter of resistance {Rv} Ω is connected across the {R1} Ω resistor. It reads :'
        o, a = mcq(rng, fr(V) + ' V', [fr(F(E * R1, R1 + R2)) + ' V', fr(V * 2) + ' V', fr(E - V) + ' V', fr(F(E * Rv, Rv + R2)) + ' V', fr(V / 2) + ' V', fr(V + 1) + ' V'])
        return dict(q=q, o=o, a=a, sol=[f'{R1} Ω ∥ {Rv} Ω = {fr(par(R1, Rv))} Ω.', f'V = {E} × \\f{{{fr(par(R1, Rv))}}}{{{fr(par(R1, Rv))} + {R2}}} = {fr(V)} V (less than the ideal {fr(F(E * R1, R1 + R2))} V).'], p=dict(t='vread', R1=R1, R2=R2, Rv=Rv, E=E))
    if t == 'rv':
        R1, R2, E, Rv = rng.choice([100, 200, 300]), rng.choice([100, 200, 300, 600]), rng.choice([3, 4, 6, 9, 12]), rng.choice([100, 200, 300, 600, 900])
        V = E * par(R1, Rv) / (par(R1, Rv) + R2)
        q = f'{R1} Ω and {R2} Ω are in series with an ideal {E} V battery. A voltmeter across the {R1} Ω resistor reads {fr(V)} V. The resistance of the voltmeter is ______ Ω.'
        return dict(q=q, o=None, a=Rv, sol=[f'Current through {R2} Ω: \\f{{{E} − {fr(V)}}}{{{R2}}}.', f'{R1} ∥ R_{{V}} = \\f{{{fr(V)}}}{{I}} = {fr(par(R1, Rv))} Ω → R_{{V}} = {Rv} Ω.'], p=dict(t='rv', R1=R1, R2=R2, E=E, V=str(V)))
    if t == 'range':
        V1 = rng.choice([2, 3, 5, 10, 15, 20]); V2 = V1 * rng.choice([F(3, 2), 2, 3, 4, 5, 10]); V2 = int(V2) if F(V2).denominator == 1 else None
        if V2 is None: return g_meter(rng)
        k = F(V2, V1) - 1
        q = f'A voltmeter of resistance G reads up to {V1} V. To make it read up to {V2} V you must connect :'
        o, a = mcq(rng, f'{fr(k)}G in series', [f'{fr(k)}G in parallel', f'{fr(F(V2, V1))}G in series', f'{fr(1 / k)}G in series', f'{fr(F(V2, V1))}G in parallel'])
        return dict(q=q, o=o, a=a, sol=[f'Full-scale current I = {V1}/G stays the same.', f'{V2} = I(G + R) → R = ({V2}/{V1} − 1)G = {fr(k)}G, in series.'], p=dict(t='range', V1=V1, V2=V2))
    G, Ig, I = rng.choice([10, 20, 25, 50, 60, 99, 100, 120, 200]), F(rng.choice([1, 2, 5, 10]), 1000), F(rng.choice([1, 5, 10, 20, 50]), 10)
    S = Ig * G / (I - Ig)
    q = f'A galvanometer of resistance {G} Ω gives full deflection at {nf(Ig * 1000)} mA. The shunt needed to convert it into an ammeter of range {nf(I)} A is :'
    o, a = mcq(rng, nf(S) + ' Ω', [nf(Ig * G / I) + ' Ω' if Ig * G / I != S else nf(S * 10) + ' Ω', nf(G * (I / Ig - 1)) + ' Ω', nf(S * 2) + ' Ω', nf(S / 2) + ' Ω'])
    return dict(q=q, o=o, a=a, sol=['The shunt carries I − I_{g} at the same voltage as the galvanometer.', f'S = \\f{{I_{{g}}G}}{{I − I_{{g}}}} = \\f{{{nf(Ig)} × {G}}}{{{nf(I - Ig)}}} = {nf(S)} Ω.'], p=dict(t='shunt', G=G, Ig=str(Ig), I=str(I)))

def g_bridge(rng):
    t = rng.choice(['unknown', 'parallel', 'wire', 'twice'])
    if t == 'unknown':
        L = rng.choice([20, 25, 30, 40, 60, 75, 80]); R = rng.choice([2, 3, 4, 6, 10, 12])
        X = F(R) * (100 - L) / L
        q = f'In a meter bridge, an unknown resistance X is in the left gap and {R} Ω in the right gap. The null point is {L} cm from the left end. Then X is :'
        o, a = mcq(rng, fr(X) + ' Ω', [fr(F(R) * L / (100 - L)) + ' Ω', fr(F(R) * L / 100) + ' Ω', fr(X * 2) + ' Ω', fr(X + 1) + ' Ω'])
        return dict(q=q, o=o, a=a, sol=[f'Balance: \\f{{X}}{{{R}}} = \\f{{{L}}}{{{100 - L}}}.', f'X = {fr(X)} Ω... wait — careful: the LEFT gap pairs with the LEFT length.'], p=dict(t='mb', L=L, R=R)) if False else \
            dict(q=q, o=mcq(rng, fr(F(R) * L / (100 - L)) + ' Ω', [fr(X) + ' Ω', fr(F(R) * L / 100) + ' Ω', fr(F(R) * L / (100 - L) * 2) + ' Ω', fr(F(R) * L / (100 - L) + 1) + ' Ω'])[0], a=None,
                 sol=['Balance: \\f{X}{R} = \\f{l}{100 − l} (left gap ↔ left length).', f'X = {R} × \\f{{{L}}}{{{100 - L}}} = {fr(F(R) * L / (100 - L))} Ω.'], p=dict(t='mb', L=L, R=R), right=fr(F(R) * L / (100 - L)) + ' Ω')
    if t in ('parallel', 'twice'):
        a_, b_, x = rng.randint(1, 8), rng.randint(1, 12), rng.randint(1, 15)
        l1 = F(100 * a_, a_ + b_); bb = par(b_, x); l2 = F(100 * a_) / (a_ + bb)
        if l1.denominator != 1 and (l1 * 2).denominator != 1: return g_bridge(rng)
        if (l2 * 2).denominator != 1: return g_bridge(rng)
        q = f'In a meter bridge, {a_} Ω is in the left gap and {b_} Ω in the right gap. When a resistance x is joined in parallel with the {b_} Ω resistor, the null point moves {nf(l2 - l1)} cm to the right. Then x = ______ Ω.'
        return dict(q=q, o=None, a=x, sol=[f'First: l = \\f{{100 × {a_}}}{{{a_ + b_}}} = {nf(l1)} cm; new l = {nf(l2)} cm.', f'\\f{{{a_}}}{{R}} = \\f{{{nf(l2)}}}{{{nf(100 - l2)}}} → R = {fr(bb)} Ω.', f'\\f{{{b_}x}}{{{b_} + x}} = {fr(bb)} → x = {x} Ω.'], p=dict(t='mbp', a=a_, b=b_, shift=str(l2 - l1)))
    L = rng.choice([30, 40, 60, 70]); k = rng.choice([2, 3, F(1, 2)])
    q = f'A meter bridge balances at {L} cm. The bridge wire is replaced by one with {fr(k)} times the resistance per cm (same length). The new balance point is :'
    o, a = mcq(rng, f'{L} cm', [f'{nf(F(L) * k) if F(L) * k < 100 else nf(F(L) / k)} cm', f'{100 - L} cm', f'{nf(F(L) / k) if F(L) / k != F(L) * k else nf(F(L) / 2)} cm', '50 cm'])
    return dict(q=q, o=o, a=a, sol=['Balance: \\f{P}{Q} = \\f{l·ρ_{wire}}{(100 − l)·ρ_{wire}} — the resistance per cm cancels.', f'So the null point stays at {L} cm.'], p=dict(t='mbw', L=L))

def g_drift(rng):
    L, A_mm, V, n, m4 = rng.choice([1, 2, 4, 5]), rng.choice([F(1, 10), F(1, 5), F(1, 2), 1, 2]), rng.choice([1, 2, 4, 5]), rng.choice([5, 6, 8]), rng.randint(2, 40)
    A = A_mm * F(1, 10 ** 6); E = F(V, L); mu = F(m4, 10 ** 4); vd = mu * E; I = n * 10 ** 28 * F(16, 10 ** 20) * A * vd
    q = f'A wire {L} m long, of cross-section {nf(A_mm)} mm^{{2}}, carries {nf(I)} A when {V} V is applied. With n = {n} × 10^{{28}} m^{{−3}} and e = 1.6 × 10^{{−19}} C, the electron mobility is ______ × 10^{{−4}} m^{{2}}/(V s).'
    return dict(q=q, o=None, a=m4, sol=[f'v_{{d}} = \\f{{I}}{{neA}} = {nf(vd)} m/s.', f'E = V/L = {nf(E)} V/m.', f'μ = v_{{d}}/E = {nf(mu)} → {m4} × 10^{{−4}}.'], p=dict(t='drift', L=L, A=str(A), V=V, n=n, I=str(I)))

def g_charge(rng):
    I0, b, T = rng.randint(1, 30), rng.randint(1, 6), rng.choice([2, 4, 5, 6, 8, 10, 12, 15, 20])
    Q = I0 * T + F(b * T * T, 2)
    q = f'The current in a wire varies as I = {I0} + {b}t (SI units). The charge that passes a cross-section from t = 0 to t = {T} s is :'
    o, a = mcq(rng, nf(Q) + ' C', [nf(I0 * T) + ' C', nf((I0 + b * T) * T) + ' C', nf(I0 * T + b * T * T) + ' C', nf(Q / 2) + ' C', nf(b * T * T) + ' C', nf(Q * 2) + ' C', nf(Q + I0) + ' C'])
    return dict(q=q, o=o, a=a, sol=['q = ∫ I dt (area under the I–t graph).', f'= {I0}×{T} + \\f{{{b}×{T}^{{2}}}}{{2}} = {nf(Q)} C.'], p=dict(t='charge', I0=I0, b=b, T=T))

NETS = [('a triangle of three equal resistors r, across two corners', lambda: (tri(1), 0, 1)), ('a square of four equal resistors r, across two ADJACENT corners', lambda: (square(1), 0, 1)),
        ('a square of four equal resistors r, across two OPPOSITE corners', lambda: (square(1), 0, 2)), ('a tetrahedron made of six equal resistors r, across two corners', lambda: (tetra(1), 0, 1)),
        ('a cube of twelve equal resistors r, across the ends of one EDGE', lambda: (cube(1), (0, 0, 0), (0, 0, 1))), ('a cube of twelve equal resistors r, across a FACE diagonal', lambda: (cube(1), (0, 0, 0), (0, 1, 1))),
        ('a cube of twelve equal resistors r, across the BODY diagonal', lambda: (cube(1), (0, 0, 0), (1, 1, 1))), ('a hexagon of six equal resistors r, across OPPOSITE corners', lambda: (hexring(1), 0, 3)),
        ('a hexagon of six equal resistors r, across ADJACENT corners', lambda: (hexring(1), 0, 1)), ('a hexagon of six resistors r with six spokes r to the centre, across OPPOSITE corners', lambda: (hexspoke(1), 0, 3)),
        ('a hexagon of six resistors r with six spokes r to the centre, across ADJACENT corners', lambda: (hexspoke(1), 0, 1))]
FORM = {F(2, 3): 'r ∥ 2r', F(3, 4): 'r ∥ 3r', F(1, 1): '2r ∥ 2r', F(1, 2): 'symmetry: the far edge carries no current → r ∥ 2r ∥ 2r', F(7, 12): 'edge of a cube', F(3, 4) * 1: '', F(5, 6): 'body diagonal: r/3 + r/6 + r/3', F(3, 2): '3r ∥ 3r', F(5, 6) * 1: ''}
NOTES = {0: 'One resistor (r) is in parallel with the other two in series (2r): \\f{r·2r}{3r} = \\f{2r}{3}.', 1: 'r in parallel with 3r: \\f{3r}{4}.', 2: 'Two paths of 2r in parallel: r.', 3: 'The two other corners are at the same potential, so the resistor between them carries no current; r ∥ 2r ∥ 2r = \\f{r}{2}.',
         4: 'Edge of a cube: by symmetry, R = \\f{7r}{12}.', 5: 'Face diagonal of a cube: by symmetry, R = \\f{3r}{4}.', 6: 'Body diagonal: currents split 3 → 6 → 3, so R = \\f{r}{3} + \\f{r}{6} + \\f{r}{3} = \\f{5r}{6}.', 7: 'Two paths of 3r in parallel: \\f{3r}{2}.', 8: 'r ∥ 5r = \\f{5r}{6}.',
         9: 'Symmetry puts the centre halfway; Kirchhoff at a neighbouring corner gives \\f{4r}{5}.', 10: 'Solve with Kirchhoff (or nodal analysis): R = \\f{8r}{15}.'}
def g_net(rng):
    k = rng.randrange(len(NETS)); txt, f = NETS[k]; E, a_, b_ = f(); R = solve_net(E, a_, b_); rv = rng.choice([0, 0, 1, 2, 3, 4, 6, 12])
    others = sorted({solve_net(*NETS[j][1]()[:1], *NETS[j][1]()[1:]) for j in range(len(NETS))} - {R}, key=lambda x: abs(x - R))
    U = (lambda x: fr(x) + 'r') if not rv else (lambda x: nf(x * rv) + ' Ω')
    q = f'The equivalent resistance of {txt}' + (f', with r = {rv} Ω' if rv else '') + ', is :'
    o, a = mcq(rng, U(R), [U(x) for x in others])
    return dict(q=q, o=o, a=a, sol=[NOTES[k].replace('R = \\f{8r}{15}', f'R = {fr(R)}r'), f'R_{{eq}} = {fr(R)}r.'], p=dict(t='net', k=k, rv=rv))

def g_wire(rng):
    t = rng.choice(['stretch', 'cut', 'shape', 'temp'])
    if t == 'stretch':
        how, k = rng.choice([('its length is doubled', 4), ('its length is tripled', 9), ('its radius becomes half', 16), ('its diameter becomes one-third', 81), ('its length increases by 10%', F(121, 100))])
        q = f'A wire of resistance R is stretched (volume constant) until {how}. The new resistance is :'
        o, a = mcq(rng, nf(k) + 'R', [nf(F(k) ** F(1, 2) if isinstance(k, int) and int(math.isqrt(k)) ** 2 == k else F(k) * 2) + 'R', nf(F(k) * 2) + 'R', nf(F(1) / F(k)) + 'R', nf(F(k) / 2) + 'R', '2R'])
        return dict(q=q, o=o, a=a, sol=['Volume is fixed: AL = constant, so R = ρL/A ∝ L^{2} ∝ \\f{1}{r^{4}}.', f'Here the factor is {nf(k)} → {nf(k)}R.'], p=dict(t='stretch', k=str(F(k))))
    if t == 'cut':
        n = rng.choice([2, 3, 4, 5, 10]); m = rng.choice([1, 2]) if n % 2 == 0 else 1
        if m == 1:
            q = f'A wire of resistance R is cut into {n} equal parts which are joined in parallel. The resistance of the combination is :'
            o, a = mcq(rng, f'R/{n * n}', [f'R/{n}', f'{n}R', f'{n * n}R', 'R'])
            return dict(q=q, o=o, a=a, sol=[f'Each part R/{n}; {n} in parallel → R/{n * n}.'], p=dict(t='cut', n=n))
        R0 = rng.choice([10, 20, 40]); each = F(R0, n)
        Req = (n // 2) * par(each, each)
        q = f'A wire of resistance {R0} Ω is cut into {n} equal parts. They are joined in pairs in parallel, and the {n // 2} pairs are joined in series. The resistance is ______ Ω.'
        if Req.denominator != 1: return g_wire(rng)
        return dict(q=q, o=None, a=int(Req), sol=[f'Each part {nf(each)} Ω; a pair in parallel {nf(each / 2)} Ω.', f'{n // 2} pairs in series: {int(Req)} Ω.'], p=dict(t='cut2', R0=R0, n=n))
    if t == 'shape':
        R0 = rng.choice([6, 9, 12, 18, 24, 27, 36, 48, 60]); s = rng.choice(['triangle', 'square'])
        R = par(F(R0, 3), F(2 * R0, 3)) if s == 'triangle' else par(F(R0, 4), F(3 * R0, 4))
        q = f'A wire of resistance {R0} Ω is bent into {"an equilateral triangle" if s == "triangle" else "a square"}. The resistance between the ends of one side is :'
        o, a = mcq(rng, nf(R) + ' Ω', [nf(F(R0, 3 if s == 'triangle' else 4)) + ' Ω', nf(R * 2) + ' Ω', nf(F(R0, 2)) + ' Ω', nf(R + 1) + ' Ω'])
        return dict(q=q, o=o, a=a, sol=[f'One side ({nf(F(R0, 3 if s == "triangle" else 4))} Ω) is in parallel with the rest of the wire.', f'R = {nf(R)} Ω.'], p=dict(t='shape', R0=R0, s=s))
    R0, al = rng.choice([(10, F(2, 10000)), (20, F(4, 1000)), (5, F(4, 1000)), (50, F(1, 1000))]); t1 = 100; Rt_c = rng.choice([200, 250, 300, 400, 475])
    R1 = R0 * (1 + al * t1); Rt = R0 * (1 + al * Rt_c)
    q = f'A wire has resistance {nf(R0)} Ω at 0 ºC and {nf(R1)} Ω at 100 ºC. At what temperature (in kelvin) is its resistance {nf(Rt)} Ω?'
    return dict(q=q, o=None, a=Rt_c + 273, sol=[f'α = \\f{{{nf(R1)} − {nf(R0)}}}{{{nf(R0)} × 100}} = {nf(al)} /ºC.', f't = \\f{{{nf(Rt)} − {nf(R0)}}}{{{nf(R0)} × α}} = {Rt_c} ºC = {Rt_c + 273} K.'], p=dict(t='temp', R0=R0, R1=str(R1), Rt=str(Rt)))

STMT = [('In a meter bridge, the balance point does not depend on the resistance per unit length of the wire.', True), ('Resistivity of a wire doubles when its length is doubled.', False),
        ('Maximum power is delivered to an external resistor R when R equals the internal resistance r.', True), ('The emf of two different cells in parallel is less than the smaller emf.', False),
        ('A potentiometer measures emf without drawing current from the cell at balance.', True), ('Drift speed of electrons is of the order of 10^{8} m/s.', False),
        ('Resistance of a metal increases with temperature.', True), ('An ideal voltmeter has zero resistance.', False), ('An ammeter is made by connecting a small resistance in parallel with a galvanometer.', True),
        ('Two equal resistors in parallel have a resistance twice that of one.', False)]
def g_stmt(rng):
    (s1, v1), (s2, v2) = rng.sample(STMT, 2)
    opts = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
    right = opts[0] if v1 and v2 else opts[1] if not (v1 or v2) else opts[2] if v1 else opts[3]
    o, a = mcq(rng, right, [x for x in opts if x != right])
    return dict(q=f'Statement I: {s1} Statement II: {s2}', o=o, a=a, sol=[f'I is {"true" if v1 else "false"}.', f'II is {"true" if v2 else "false"}.'], p=dict(t='stmt', s1=s1, s2=s2))

GEN = dict(cells=g_cells, power=g_power, pot=g_pot, meter=g_meter, bridge=g_bridge, drift=g_drift, charge=g_charge, net=g_net, wire=g_wire, stmt=g_stmt)
def finish(it):
    """some generators return the right answer as text and options without index: fix the index here"""
    if it.get('a') is None and it.get('o'):
        it['a'] = it['o'].index(it.pop('right'))
    return it

def check(it):
    """independent re-solve (circuit solver / alternative algebra) → must equal the marked answer"""
    p = it['p']; t = p['t']; R_ = it['o'][it['a']] if it.get('o') else it['a']
    val = lambda s: F(s.split(' ')[0].replace('−', '-').replace('\\f{', '').replace('}{', '/').replace('}', '').replace('r', '')) if '\\f' in s or '/' in s or s.replace('.', '').replace(' ', '').split('Ω')[0].split('V')[0].split('A')[0].replace('r', '').lstrip('-').isdigit() else None
    if t == 'ratio':
        I1 = solve_dc([('a', 'g', p['R'])], [('g', 'm', p['E1'], p['r1']), ('m', 'a', p['E2'], p['r2'])], 'g')['a'] / p['R']
        I2 = solve_dc([('a', 'g', p['R'])], [('g', 'a', p['E1'], p['r1']), ('g', 'a', p['E2'], p['r2'])], 'g')['a'] / p['R']
        return val(R_) == I1 / I2
    if t == 'internal':
        I1, I2 = F(p['I1']), F(p['I2']); r = (I2 * p['R2'] - I1 * p['R1']) / (I1 - I2); return r == R_
    if t == 'same':
        n, R = p['n'], p['R']; r = F(R_); E = 1
        s = solve_dc([('a', 'g', R)], [((k if k else 'g'), (k + 1 if k + 1 < n else 'a'), E, r) for k in range(n)], 'g')['a']
        pp = solve_dc([('a', 'g', R)], [('g', 'a', E, r) for _ in range(n)], 'g')['a']; return s == pp
    if t == 'reverse':
        V = solve_dc([('a', 'g', p['R'])], [('a', 'g', p['E1'], p['r1']), ('g', 'a', p['E2'], p['r2'])], 'g')['a']; return val(R_) == abs(V) / p['R']
    if t == 'terminal':
        V = solve_dc([('a', 'g', p['R'])], [('g', 'a', p['E'], F(p['r']))], 'g')['a']; return val(R_) == V
    if t == 'rated': v = p['P0'] * (p['V'] / p['V0']) ** 2; return abs(float(R_.split(' ')[0]) - v) < 1e-3 * v
    if t == 'bseries': return abs(float(R_.split(' ')[0]) - (p['p0'] * 1.0) / p['n']) < 1e-3 * p['p0'] / p['n']
    if t == 'cut' and it.get('o') and 'W' in R_: return R_ == f"{p['n'] ** 2}W"
    if t == 'cut': return R_ == f"R/{p['n'] ** 2}"
    if t == 'electrons': return abs(float(R_.replace(' × 10^{', 'e').replace('}', '')) - p['P0'] / p['V0'] / 1.6e-19) / (p['P0'] / p['V0'] / 1.6e-19) < 1e-3
    if t == 'heater':
        Rh = F(p['V0'] ** 2, p['P0']); I = F(p['V0']) / (Rh + R_); return I * I * Rh == F(p['P0'], p['k'] ** 2)
    if t == 'shunt' and 'R1' in p:
        r = F(R_); return F(p['R1']) / (p['R1'] + r) / (F(p['R2']) / (p['R2'] + r)) == F(p['L1'], p['L2'])
    if t == 'cmp': return val(R_) == F(p['l1'], p['l2'])
    if t == 'vread':
        V = solve_dc([('a', 'm', p['R2']), ('m', 'g', p['R1']), ('m', 'g', p['Rv'])], [('g', 'a', p['E'], TINY)], 'g')['m']; return abs(val(R_) - V) < F(1, 10 ** 6)
    if t == 'rv':
        V = solve_dc([('a', 'm', p['R2']), ('m', 'g', p['R1']), ('m', 'g', R_)], [('g', 'a', p['E'], TINY)], 'g')['m']; return abs(V - F(p['V'])) < F(1, 10 ** 6)
    if t == 'range':
        k = F(R_.split('G')[0].replace('\\f{', '').replace('}{', '/').replace('}', '')); return 'series' in R_ and (1 + k) * F(p['V1']) == p['V2']
    if t == 'shunt':
        S = float(R_.split(' ')[0]); G, Ig, I = p['G'], float(F(p['Ig'])), float(F(p['I'])); return abs(Ig * G - (I - Ig) * S) < 1e-3 * Ig * G
    if t == 'mb':
        X = val(R_); V = solve_dc([('a', 'm', X), ('m', 'g', p['R']), ('a', 'w', p['L']), ('w', 'g', 100 - p['L'])], [('g', 'a', 1, TINY)], 'g'); return V['m'] == V['w']
    if t == 'mbp':
        x = F(R_); l2 = F(100 * p['a'] , p['a'] + p['b']) + F(p['shift'])
        V = solve_dc([('a', 'm', p['a']), ('m', 'g', p['b']), ('m', 'g', x), ('a', 'w', l2), ('w', 'g', 100 - l2)], [('g', 'a', 1, TINY)], 'g'); return V['m'] == V['w']
    if t == 'mbw': return R_ == f"{p['L']} cm"
    if t == 'drift':
        I, A, n = F(p['I']), F(p['A']), p['n'] * 10 ** 28; sigma = I * p['L'] / (p['V'] * A); return sigma / (n * F(16, 10 ** 20)) * 10 ** 4 == R_
    if t == 'charge':
        T = p['T']; N = 1000; s = sum((p['I0'] + p['b'] * (T * (k + 0.5) / N)) * T / N for k in range(N)); return abs(float(R_.split(' ')[0]) - s) < 1e-6
    if t == 'net':
        E, a_, b_ = NETS[p['k']][1](); Rn = solve_net(E, a_, b_)
        if p.get('rv'): return abs(float(R_.split(' ')[0]) - float(Rn * p['rv'])) < 1e-3 * float(Rn * p['rv'])
        return F(R_.replace('r', '').replace('\\f{', '').replace('}{', '/').replace('}', '') or '1') == Rn
    if t == 'stretch':
        k = F(p['k']); return R_ == nf(k) + 'R'
    if t == 'cut2':
        each = F(p['R0'], p['n']); return (p['n'] // 2) * (each / 2) == R_
    if t == 'shape':
        E = tri(F(p['R0'], 3)) if p['s'] == 'triangle' else square(F(p['R0'], 4)); v = float(solve_net(E, 0, 1)); return abs(float(R_.split(' ')[0]) - v) < 1e-3 * v
    if t == 'temp':
        R0, R1, Rt = p['R0'], F(p['R1']), F(p['Rt']); al = (R1 - R0) / (R0 * 100); return (Rt / R0 - 1) / al + 273 == R_
    if t == 'stmt':
        tv = dict(STMT); v1, v2 = tv[p['s1']], tv[p['s2']]
        want = 'Both Statement I and Statement II are true' if v1 and v2 else 'Both Statement I and Statement II are false' if not (v1 or v2) else 'Statement I is true but Statement II is false' if v1 else 'Statement I is false but Statement II is true'
        return R_ == want
    raise KeyError(t)
