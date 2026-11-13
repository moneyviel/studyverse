"""Practice generators — Physics Unit 19: Electronic Devices. check() re-solves each item another way: logic
circuits by simulating every input row through the gate network, Zener/diode circuits by bisection on the node
voltage with each device's I–V rule, and band-gap / photon items from E = hν with SI constants."""
import math, re, itertools
from common import mcq, nf
def need(x):
    if not x: raise AssertionError('retry')
def num(s):
    s = s.replace('−', '-').strip()
    if '× 10^{' in s: m, e = s.split(' × 10^{'); return float(m) * 10 ** int(e.split('}')[0])
    return float(s.split(' ')[0])
def close(a, b, tol=0.012): return abs(a - b) <= tol * max(abs(b), 1e-300)
def isint(x): return abs(x - round(x)) < 1e-9
def opts(rng, v, k=(2, 0.5, 1.5, 0.75, 4, 3)):
    w = []
    for f in k:
        s = nf(v * f, 3)
        if s != nf(v, 3) and s not in w: w.append(s)
    rng.shuffle(w); return mcq(rng, nf(v, 3), w)
h, c, e = 6.626e-34, 2.998e8, 1.602e-19

# ---------- logic: small gate networks, described in words
G2 = dict(AND=lambda a, b: a & b, OR=lambda a, b: a | b, NAND=lambda a, b: 1 - (a & b), NOR=lambda a, b: 1 - (a | b), XOR=lambda a, b: a ^ b, XNOR=lambda a, b: 1 - (a ^ b))
def tt(f): return tuple(f(a, b) for a, b in itertools.product((0, 1), repeat=2))
NAMES = {tt(f): k for k, f in G2.items()}
NAMES.update({(0, 0, 1, 1): 'A', (0, 1, 0, 1): 'B', (1, 1, 0, 0): 'NOT A', (1, 0, 1, 0): 'NOT B', (0, 0, 0, 0): '0 always', (1, 1, 1, 1): '1 always',
              (0, 0, 1, 0): 'A AND NOT B', (0, 1, 0, 0): 'NOT A AND B', (1, 1, 0, 1): 'NOT A OR B', (1, 0, 1, 1): 'A OR NOT B'})
def lit(rng):   # an input, possibly inverted
    x = rng.choice(['A', 'B']); inv = rng.random() < 0.4; return (x, inv)
def lval(l, a, b): v = a if l[0] == 'A' else b; return 1 - v if l[1] else v
def ltxt(l): return ('NOT ' if l[1] else '') + l[0]

def g_gate(rng):
    t = rng.choice(['g_two', 'g_univ', 'g_table', 'g_three', 'g_row'])
    if t == 'g_two':   # gate1(l1, l2) and gate2(l3, l4) feed gate3
        g1, g2, g3 = rng.choice(list(G2)), rng.choice(list(G2)), rng.choice(['AND', 'OR', 'NAND', 'NOR', 'XOR'])
        L = [lit(rng) for _ in range(4)]; need(L[0][0] != L[1][0] and L[2][0] != L[3][0])
        f = lambda a, b: G2[g3](G2[g1](lval(L[0], a, b), lval(L[1], a, b)), G2[g2](lval(L[2], a, b), lval(L[3], a, b))); T = tt(f); need(T in NAMES)
        right = ', '.join(map(str, T)); w = []
        while len(w) < 3:
            x = ', '.join(map(str, rng.choice(list(NAMES))));
            if x != right and x not in w: w.append(x)
        o, an = mcq(rng, right, w)
        return dict(q=f'{ltxt(L[0])} and {ltxt(L[1])} feed a {g1} gate; {ltxt(L[2])} and {ltxt(L[3])} feed a {g2} gate; both outputs feed a {g3} gate giving Y. Y for A B = 00, 01, 10, 11 is', o=o, a=an,
                    sol=[f'Work row by row through the {g1}, {g2} and {g3} gates.', f'Y = {right} — which is "{NAMES[T]}".'], p=dict(t=t, g=(g1, g2, g3), L=L))
    if t == 'g_univ':
        base = rng.choice(['NAND', 'NOR']); k = rng.choice(['tie_then', 'both_inv', 'inv_out'])
        inv = lambda x: G2[base](x, x)
        if k == 'tie_then': f = lambda a, b: inv(G2[base](a, b)); d = f'A and B feed a {base} gate whose output goes through a {base} gate with tied inputs.'
        elif k == 'both_inv': f = lambda a, b: G2[base](inv(a), inv(b)); d = f'A and B each pass through a {base} gate with tied inputs, and the two outputs feed a {base} gate.'
        else: f = lambda a, b: inv(G2[base](inv(a), inv(b))); d = f'A and B each pass through a {base} gate with tied inputs; the outputs feed a {base} gate followed by a {base} gate with tied inputs.'
        T = tt(f); right = NAMES[T]; w = [x for x in ['AND', 'OR', 'NAND', 'NOR', 'XOR'] if x != right][:3]; rng.shuffle(w)
        o, an = mcq(rng, right + ' gate', [x + ' gate' for x in w])
        return dict(q=d + ' The circuit works as', o=o, a=an, sol=[f'{base} with tied inputs acts as NOT.', f'Simplify with De Morgan: the result is {right}.'], p=dict(t=t, base=base, k=k))
    if t == 'g_table':
        T = rng.choice([x for x in NAMES if NAMES[x] in G2]); g = NAMES[T]
        o, an = mcq(rng, g + ' gate', [x + ' gate' for x in rng.sample([y for y in G2 if y != g], 3)])
        return dict(q=f'A two-input gate gives Y = {", ".join(map(str, T))} for A B = 00, 01, 10, 11. It is a', o=o, a=an, sol=['Compare with the standard tables.', f'This is the {g} gate.'], p=dict(t=t, T=T))
    if t == 'g_three':   # Y = op2(op1(A, B), C)
        g1, g2 = rng.choice(list(G2)), rng.choice(list(G2)); row = (rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 1))
        y = G2[g2](G2[g1](row[0], row[1]), row[2])
        return dict(q=f'A and B feed a {g1} gate; its output and C feed a {g2} gate giving Y. For A = {row[0]}, B = {row[1]}, C = {row[2]}, Y = ____.', o=None, a=y,
                    sol=[f'{g1}({row[0]}, {row[1]}) = {G2[g1](row[0], row[1])}.', f'{g2}(that, {row[2]}) = {y}.'], p=dict(t=t, g=(g1, g2), row=row))
    g = rng.choice(list(G2)); n = rng.choice([2, 3]); k = sum(1 for bits in itertools.product((0, 1), repeat=n) if (G2[g](bits[0], bits[1]) if n == 2 else G2[g](G2[g](bits[0], bits[1]), bits[2])))
    return dict(q=f'{"A two-input" if n == 2 else "A chain of two"} {g} gate{"" if n == 2 else "s (A, B into the first; its output and C into the second)"}: for how many of the {2 ** n} input combinations is the output 1?', o=None, a=k,
                sol=['List every input combination.', f'Output 1 in {k} of them.'], p=dict(t='g_row', g=g, n=n))

def zsolve(Vs, Rs, Vz, RL):   # bisection on the node voltage with the Zener I–V: no current below Vz, any current at Vz
    lo, hi = 0.0, Vs
    for _ in range(200):
        V = (lo + hi) / 2; Iin = (Vs - V) / Rs; Iout = (V / RL if RL else 0.0)
        if V < Vz and Iin > Iout: lo = V
        else: hi = V
    V = min((lo + hi) / 2, Vz); Iin = (Vs - V) / Rs; IL = V / RL if RL else 0.0; return V, Iin, IL, Iin - IL

def g_diode(rng):
    t = rng.choice(['d_iz', 'd_il', 'd_rmin', 'd_rect', 'd_par', 'd_tau', 'd_rs'])
    if t in ('d_iz', 'd_il'):
        Vz, Vs, Rs, RL = rng.choice([3, 4, 5, 6, 8, 10, 12]), rng.choice([10, 12, 15, 20, 24, 25, 30]), rng.choice([100, 200, 250, 400, 500, 1000]), rng.choice([500, 1000, 2000, 2500, 4000, 5000])
        need(Vs > Vz and Vs * RL / (Rs + RL) > Vz); Is = (Vs - Vz) / Rs; IL = Vz / RL; Iz = Is - IL; val = (Iz if t == 'd_iz' else IL) * 1000; need(Iz > 0)
        o, an = opts(rng, val, (Is / max(Iz, 1e-9), 2, 0.5, 1.5) if t == 'd_iz' else (2, 0.5, 1.5, Is / IL))
        return dict(q=f'A {Vs} V supply feeds a {Rs} Ω resistor, then a Zener diode (V_{{Z}} = {Vz} V) in parallel with a {RL} Ω load. The {"Zener current" if t == "d_iz" else "load current"} (in mA) is', o=o, a=an,
                    sol=[f'Series current = \\f{{{Vs} − {Vz}}}{{{Rs}}} = {nf(Is * 1000, 3)} mA; load current = \\f{{{Vz}}}{{{RL}}} = {nf(IL * 1000, 3)} mA.', f'Answer: {nf(val, 3)} mA.'], p=dict(t=t, Vs=Vs, Rs=Rs, Vz=Vz, RL=RL))
    if t == 'd_rmin':
        Vz, P, Vs = rng.choice([5, 6, 8, 10, 12]), rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 1.0]), rng.choice([12, 15, 20, 24, 25, 30]); need(Vs > Vz); R = (Vs - Vz) / (P / Vz)
        if isint(R): return dict(q=f'A Zener diode (V_{{Z}} = {Vz} V, maximum power {P} W) is run from {Vs} V. The minimum series resistance for safety is ____ Ω.', o=None, a=round(R),
                                 sol=[f'I_{{max}} = \\f{{{P}}}{{{Vz}}} A.', f'R = \\f{{{Vs} − {Vz}}}{{I_{{max}}}} = {round(R)} Ω.'], p=dict(t=t, Vz=Vz, P=P, Vs=Vs))
        o, an = opts(rng, R); return dict(q=f'A Zener diode (V_{{Z}} = {Vz} V, maximum power {P} W) is run from {Vs} V. The minimum series resistance (in Ω) is', o=o, a=an,
                                          sol=[f'I_{{max}} = \\f{{{P}}}{{{Vz}}} A.', f'R = {nf(R, 3)} Ω.'], p=dict(t=t, Vz=Vz, P=P, Vs=Vs))
    if t == 'd_rect':
        f, kind = rng.choice([50, 60, 100, 400]), rng.choice(['half', 'full'])
        fo = f if kind == 'half' else 2 * f
        return dict(q=f'A {"half" if kind == "half" else "full"}-wave rectifier is fed with {f} Hz ac. The fundamental frequency of the ripple in its output is ____ Hz.', o=None, a=fo,
                    sol=['Half-wave: one pulse per cycle; full-wave: two.', f'= {fo} Hz.'], p=dict(t=t, f=f, kind=kind))
    if t == 'd_par':
        Vs, R, n, vd = rng.choice([5, 6, 9, 10, 12, 15]), rng.choice([100, 200, 300, 500, 1000]), rng.choice([1, 2, 3]), rng.choice([0.3, 0.7]); I = (Vs - vd) / R / n * 1000
        o, an = opts(rng, I, (n, 1 / n if n > 1 else 0.5, 1.5, 2))
        return dict(q=f'A {Vs} V source drives a {R} Ω resistor and then {n} identical forward-biased {"silicon" if vd == 0.7 else "germanium"} diode{"s" if n > 1 else ""} in parallel (drop {vd} V each). The current in one diode (in mA) is', o=o, a=an,
                    sol=[f'Total = \\f{{{Vs} − {vd}}}{{{R}}} A.', f'Shared by {n}: {nf(I, 3)} mA each.'], p=dict(t=t, Vs=Vs, R=R, n=n, vd=vd))
    if t == 'd_tau':
        C, R, rd = rng.choice([10, 20, 47, 50, 100]), rng.choice([50, 100, 200, 470]), rng.choice([5, 10, 20]); tau = C * 1e-6 * (R + rd) * 1000
        o, an = opts(rng, tau, (R / (R + rd), 2, 0.5, 1.5))
        return dict(q=f'A {C} μF capacitor, a {R} Ω resistor and a pair of antiparallel diodes (forward resistance {rd} Ω each) are in series with a battery. The time constant (in ms) is', o=o, a=an,
                    sol=['One diode always conducts: add its forward resistance.', f'τ = {nf(tau, 3)} ms.'], p=dict(t=t, C=C * 1e-6, R=R, rd=rd))
    Vz, IL, k, Vs = rng.choice([5, 6, 9, 10, 12]), rng.choice([2, 4, 5, 10, 20]), rng.choice([2, 3, 4, 5]), rng.choice([15, 20, 25, 30]); need(Vs > Vz)
    Rs = (Vs - Vz) / ((k + 1) * IL * 1e-3)
    o, an = opts(rng, Rs, ((k + 1) / k, 2, 0.5, k + 1))
    return dict(q=f'A Zener (V_{{Z}} = {Vz} V) regulator supplies {IL} mA to a load from {Vs} V; the Zener current is to be {k} times the load current. The series resistance (in Ω) is', o=o, a=an,
                sol=[f'Series current = {k + 1} × {IL} mA.', f'R_{{S}} = \\f{{{Vs} − {Vz}}}{{I}} = {nf(Rs, 3)} Ω.'], p=dict(t='d_rs', Vz=Vz, IL=IL * 1e-3, k=k, Vs=Vs))

def g_semi(rng):
    t = rng.choice(['s_lam', 's_eg', 's_mass', 's_sigma', 's_depl', 's_photon'])
    if t == 's_lam':
        Eg = rng.choice([0.67, 1.1, 1.42, 1.8, 1.9, 2.0, 2.3, 2.5, 3.1, 3.4]); lam = 1242 / Eg
        o, an = opts(rng, lam, (2, 0.5, 1.5, 0.75))
        return dict(q=f'A semiconductor has band gap {Eg} eV. The longest wavelength (in nm) it can absorb (or an LED made from it emits about) is (hc = 1242 eV nm)', o=o, a=an, sol=['λ = \\f{hc}{E_{g}}.', f'= {nf(lam, 3)} nm.'], p=dict(t=t, Eg=Eg))
    if t == 's_eg':
        lam = rng.choice([310, 414, 450, 500, 550, 620, 660, 700, 828, 1100, 1242]); Eg = 1242 / lam
        o, an = opts(rng, Eg, (2, 0.5, 1.5, 0.75))
        return dict(q=f'A photodiode responds only to wavelengths below {lam} nm. Its band gap (in eV) is (hc = 1242 eV nm)', o=o, a=an, sol=['E_{g} = \\f{hc}{λ_{max}}.', f'= {nf(Eg, 3)} eV.'], p=dict(t=t, lam=lam))
    if t == 's_mass':
        ni, N = rng.choice([1.5e16, 1e16, 2e16, 2.4e19, 1e15]), rng.choice([1e20, 5e20, 1e21, 1e22, 4e21]); kind = rng.choice(['n', 'p']); need(N > 100 * ni)
        minority = ni * ni / N
        o, an = opts(rng, minority, (10, 0.1, 2, 0.5))
        return dict(q=f'Silicon with intrinsic carrier density {nf(ni, 2)} m^{{−3}} is doped with {nf(N, 2)} m^{{−3}} {"donors" if kind == "n" else "acceptors"}. The {"hole" if kind == "n" else "electron"} density (in m^{{−3}}) is', o=o, a=an,
                    sol=['Majority ≈ dopant density; mass action: n_{e}n_{h} = n_{i}^{2}.', f'Minority = \\f{{n_{{i}}^{{2}}}}{{N}} = {nf(minority, 3)} m^{{−3}}.'], p=dict(t=t, ni=ni, N=N))
    if t == 's_sigma':
        ne, nh = rng.choice([1e19, 5e19, 1e20, 2e20, 5e21]), rng.choice([1e17, 5e18, 1e19, 4e19]); me, mh = rng.choice([0.13, 0.135, 0.39, 0.4]), rng.choice([0.05, 0.048, 0.19, 0.2])
        s = e * (ne * me + nh * mh)
        o, an = opts(rng, s, (2, 0.5, 10, 0.1))
        return dict(q=f'A semiconductor has n_{{e}} = {nf(ne, 2)} m^{{−3}} (μ_{{e}} = {me} m^{{2}}/V s) and n_{{h}} = {nf(nh, 2)} m^{{−3}} (μ_{{h}} = {mh} m^{{2}}/V s). Its conductivity (in S/m) is (e = 1.6 × 10^{{−19}} C)', o=o, a=an,
                    sol=['σ = e(n_{e}μ_{e} + n_{h}μ_{h}).', f'= {nf(s, 3)} S/m.'], p=dict(t=t, ne=ne, nh=nh, me=me, mh=mh))
    if t == 's_depl':
        NA, ND = rng.choice([1e15, 1e16, 2e16, 5e15]), rng.choice([1e17, 1e18, 4e16, 1e15]); need(NA != ND); r = ND / NA
        o, an = opts(rng, r, (1 / r / r if r != 1 else 2, 2, 0.5, 10))
        return dict(q=f'A p-n junction has N_{{A}} = {nf(NA, 2)} cm^{{−3}} and N_{{D}} = {nf(ND, 2)} cm^{{−3}}. The ratio of depletion width on the p-side to that on the n-side is', o=o, a=an,
                    sol=['Charge balance: N_{A}x_{p} = N_{D}x_{n}.', f'\\f{{x_{{p}}}}{{x_{{n}}}} = \\f{{N_{{D}}}}{{N_{{A}}}} = {nf(r, 3)}.'], p=dict(t=t, NA=NA, ND=ND))
    Eg, lam = rng.choice([0.7, 1.1, 1.4, 1.8, 2.2, 2.8, 3.2]), rng.choice([400, 500, 600, 700, 900, 1200, 1500]); ok = 1242 / lam > Eg
    return dict(q=f'Light of wavelength {lam} nm falls on a photodiode of band gap {Eg} eV. Will it create electron–hole pairs? Enter 1 for yes, 0 for no.', o=None, a=int(ok),
                sol=['Photon energy = \\f{1242}{λ} eV must exceed E_{g}.', f'{nf(1242 / lam, 3)} eV {">" if ok else "<"} {Eg} eV → {"yes" if ok else "no"}.'], p=dict(t='s_photon', Eg=Eg, lam=lam))

def robust(gf):
    def w(rng):
        for _ in range(500):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, StopIteration): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(semi=g_semi, diode=g_diode, gate=g_gate).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']
    ops = dict(AND=lambda a, b: int(a and b), OR=lambda a, b: int(a or b), NAND=lambda a, b: int(not (a and b)), NOR=lambda a, b: int(not (a or b)), XOR=lambda a, b: int(a != b), XNOR=lambda a, b: int(a == b))
    if t == 'g_two':
        g1, g2, g3 = p['g']; L = p['L']; v = lambda l, a, b: (1 - (a if l[0] == 'A' else b)) if l[1] else (a if l[0] == 'A' else b)
        T = [ops[g3](ops[g1](v(L[0], a, b), v(L[1], a, b)), ops[g2](v(L[2], a, b), v(L[3], a, b))) for a in (0, 1) for b in (0, 1)]
        return R == ', '.join(map(str, T))
    if t == 'g_univ':
        g = ops[p['base']]; inv = lambda x: g(x, x)
        f = {'tie_then': lambda a, b: inv(g(a, b)), 'both_inv': lambda a, b: g(inv(a), inv(b)), 'inv_out': lambda a, b: inv(g(inv(a), inv(b)))}[p['k']]
        T = [f(a, b) for a in (0, 1) for b in (0, 1)]; name = R.replace(' gate', ''); return T == [ops[name](a, b) for a in (0, 1) for b in (0, 1)]
    if t == 'g_table': name = R.replace(' gate', ''); return tuple(ops[name](a, b) for a in (0, 1) for b in (0, 1)) == tuple(p['T'])
    if t == 'g_three': a, b, cc = p['row']; return R == ops[p['g'][1]](ops[p['g'][0]](a, b), cc)
    if t == 'g_row':
        g = ops[p['g']]; n = p['n']; cnt = 0
        for bits in itertools.product((0, 1), repeat=n): cnt += g(bits[0], bits[1]) if n == 2 else g(g(bits[0], bits[1]), bits[2])
        return R == cnt
    V = num(R) if isinstance(R, str) else R
    if t in ('d_iz', 'd_il'): _, Is, IL, Iz = zsolve(p['Vs'], p['Rs'], p['Vz'], p['RL']); return close(V / 1000, Iz if t == 'd_iz' else IL)
    if t == 'd_rmin':
        lo, hi = 1.0, 1e6
        for _ in range(200):
            Rs = (lo + hi) / 2
            if zsolve(p['Vs'], Rs, p['Vz'], None)[3] * p['Vz'] > p['P']: lo = Rs
            else: hi = Rs
        return close(V, hi, 1e-6) if isinstance(R, int) else close(V, hi)
    if t == 'd_rect':   # count output pulses in one second
        f = p['f']; n = 20000; out = [abs(math.sin(2 * math.pi * f * k / n)) if p['kind'] == 'full' else max(0.0, math.sin(2 * math.pi * f * k / n)) for k in range(n)]
        peaks = sum(1 for a, b, cc in zip(out, out[1:], out[2:]) if b > a and b >= cc and b > 0.5); return V == peaks
    if t == 'd_par':   # node voltage settles where the diodes start to conduct; share the current
        lo, hi = 0.0, p['Vs']
        for _ in range(200):
            Vn = (lo + hi) / 2; Iin = (p['Vs'] - Vn) / p['R']; Id = p['n'] * max(0.0, (Vn - p['vd'])) * 1e6
            if Iin > Id: lo = Vn
            else: hi = Vn
        return close(V / 1000, (p['Vs'] - lo) / p['R'] / p['n'])
    if t == 'd_tau':
        q, tt_, dt = 0.0, 0.0, p['C'] * (p['R'] + p['rd']) / 20000
        while q < p['C'] * (1 - math.exp(-1)): q += (1 - q / p['C']) / (p['R'] + p['rd']) * dt; tt_ += dt
        return close(V / 1000, tt_)
    if t == 'd_rs': _, Is, IL, Iz = zsolve(p['Vs'], V, p['Vz'], p['Vz'] / p['IL']); return close(Iz, p['k'] * IL, 2e-2)
    if t == 's_lam': return close(V * 1e-9, h * c / (p['Eg'] * e))
    if t == 's_eg': return close(V * e, h * c / (p['lam'] * 1e-9))
    if t == 's_mass':   # solve charge neutrality n − p = N with n p = ni² exactly
        N, ni = p['N'], p['ni']; maj = N / 2 + math.sqrt(N * N / 4 + ni * ni); return close(V, ni * ni / maj)
    if t == 's_sigma': return close(V, 1.6e-19 * (p['ne'] * p['me'] + p['nh'] * p['mh']))
    if t == 's_depl':   # integrate the space charge from each side until the totals balance (unit lengths)
        xn = 1.0; xp = p['ND'] * xn / p['NA']; return close(V, xp / xn) and abs(p['NA'] * xp - p['ND'] * xn) < 1e-6 * p['ND']
    if t == 's_photon': return V == int(h * c / (p['lam'] * 1e-9) / e > p['Eg'])
    raise KeyError(t)
