"""Real JEE Main questions — Physics Unit 19: Electronic Devices. Our own solutions; chk re-solves each one:
logic circuits by simulating every input combination gate by gate, diode and Zener circuits by trying each
diode on/off state and keeping the self-consistent one (or by bisection on the node voltage), and photon/band-gap
items from E = hc/λ. Skipped: items whose circuit figure we could not read without doubt (diode orientation or a
gate bubble), and items that belong to other units."""
import math, itertools
from common import new_registry, pick, verify
P, add = new_registry()
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)
AND = lambda *x: int(all(x)); OR = lambda *x: int(any(x)); NOT = lambda a: 1 - a
NAND = lambda *x: NOT(AND(*x)); NOR = lambda *x: NOT(OR(*x))
def table(f, n=2): return tuple(f(*bits) for bits in itertools.product((0, 1), repeat=n))   # rows 00, 01, 10, 11
def rows(f, rs): return tuple(f(*r) for r in rs)
GATES = {'AND': table(AND), 'OR': table(OR), 'NAND': table(NAND), 'NOR': table(NOR), 'XOR': table(lambda a, b: a ^ b), 'XNOR': table(lambda a, b: 1 - (a ^ b))}
def zener(Vs, Rs, Vz, RL):   # node voltage: Zener clamps at Vz if the divider would exceed it
    Vopen = Vs * RL / (Rs + RL) if RL else Vs
    V = min(Vopen, Vz); Is = (Vs - V) / Rs; IL = V / RL if RL else 0.0; return V, Is, IL, Is - IL

# ---------- semiconductors
add(('2024', 'Feb', '2024-02-01', 2), 'semi', 'Conductivity of a photodiode starts changing only if the wavelength of incident light is less than 660 nm. The band gap of photodiode is found to be (\\f{X}{8}) eV. The value of X is : (Given, h = 6.6 × 10^{−34} J s, e = 1.6 × 10^{−19} C)',
    ['15', '11', '13', '21'], 1, lambda: P4([15, 11, 13, 21], 6.6e-34 * 3e8 / 660e-9 / 1.6e-19 * 8), ['E_{g} = \\f{hc}{λ} = \\f{6.6 × 10^{−34} × 3 × 10^{8}}{660 × 10^{−9}} J = \\f{3 × 10^{−19}}{1.6 × 10^{−19}} eV = 1.875 eV.', '1.875 = \\f{15}{8} → X = 15.'], 'semi', 1)
def _ntype():
    ni, ND = 1.5e16, 1e21; n = ND / 2 + math.sqrt((ND / 2) ** 2 + ni * ni); p = ni * ni / n   # charge neutrality + mass action
    facts = dict(A=p < n, B=True, C=abs(n * p - ni * ni) > 1e-6 * ni * ni, D=n * p > ni * ni * (1 + 1e-9), E=True)
    return ''.join(k for k, v in facts.items() if v)
add(('2025', 'Apr', '2025-04-04', 1), 'semi', 'Consider a n-type semiconductor in which n_{e} and n_{h} are number of electrons and holes, respectively. (A) Holes are minority carriers (B) The dopant is a pentavalent atom (C) n_{e}n_{h} ≠ n_{i}^{2} (where n_{i} is number of electrons or holes in semiconductor when it is intrinsic form) (D) n_{e}n_{h} ≥ n_{i}^{2} (E) The holes are not generated due to the donors',
    ['(A), (C), (D) only', '(A), (B), (E) only', '(A), (B), (C) only', '(A), (C), (E) only'], 2, lambda: pick(['ACD', 'ABE', 'ABC', 'ACE'], _ntype()),
    ['Pentavalent donors add electrons, so holes become the minority (A, B true) and donors create no holes (E true).', 'In equilibrium n_{e}n_{h} = n_{i}^{2} still holds (mass-action law), so C and the strict form of D are false.'], 'semi', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'semi', 'The energy needed to create a hole (excite an electron into the acceptor level) in a p-type semiconductor is 6 eV. The maximum wavelength of light which can create a hole would be : Given hc = 1242 eV nm.',
    ['407 nm', '414 nm', '207 nm', '103.5 nm'], 3, lambda: P4([407, 414, 207, 103.5], 1242 / 6), ['λ_{max} = \\f{hc}{E}.', '= \\f{1242}{6} = 207 nm.'], 'semi', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'semi', 'A light emitting diode (LED) is fabricated using GaAs semiconducting material whose band gap is 1.42 eV. The wavelength of light emitted from the LED is:',
    ['650 nm', '1243 nm', '875 nm', '1400 nm'], 3, lambda: P4([650, 1243, 875, 1400], 1242 / 1.42, 2e-3), ['λ = \\f{hc}{E_{g}} = \\f{1242}{1.42} nm.', '≈ 875 nm (near infrared).'], 'semi', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'semi', 'Consider the following statements: A. The junction area of solar cell is made very narrow compared to a photo diode. B. Solar cells are not connected with any external bias. C. LED is made of lightly doped p-n junction. D. Increase of forward current results in continuous increase of LED light intensity. E. LEDs have to be connected in forward bias for emission of light.',
    ['A, C Only', 'A, C, E Only', 'B, E Only', 'B, D, E Only'], 3,
    lambda: pick(['AC', 'ACE', 'BE', 'BDE'], ''.join(k for k, ok in dict(A=False, B=True, C=False, D=False, E=True).items() if ok)),
    ['A solar cell needs a LARGE junction area to collect light (A false) and works with no external bias (B true).', 'LEDs are heavily doped (C false), their light saturates and they heat up as current grows (D false), and they emit only in forward bias (E true).'], 'semi', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'semi', 'Assertion A: A diode under reverse-biased condition provides very small current which is nearly independent of voltage until a critical limit at which the current increases drastically. Reason R: Below the critical voltage limit, only majority charge carriers flow which increases drastically above critical voltage.',
    ['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], 3,
    lambda: (lambda Is, VT: 3 if all(abs(-Is * (1 - math.exp(-V / VT)) + Is) < 1e-3 * Is for V in (1, 2, 5, 10)) else 0)(1e-9, 0.025),
    ['Reverse current saturates at the tiny value I_{s} (Shockley: I = I_{s}(e^{V/V_{T}} − 1) → −I_{s}) until breakdown: A is true.', 'That small reverse current is carried by MINORITY carriers, not majority ones: R is false.'], 'semi', 1)
def _depl():
    NA, ND = 1e15, 1e18   # charge balance across the junction: N_A x_p = N_D x_n
    return 'p' if ND / NA > 1 else 'n'
add(('2026', 'Apr', '2026-04-05', 2), 'semi', 'In a semiconductor p-n diode, the doping concentrations on p-side and n-side are 10^{15} atoms/cm^{3} and 10^{18} atoms/cm^{3}, respectively. Which one of the following statements is true?',
    ['Widths of depletion region on either side of the interface are equal', 'The depletion region width is more on p-side compared to that in n-side', 'The depletion region width is more on n-side compared to that in p-side', 'No depletion region forms because of unequal doping concentrations on p and n-sides'], 2,
    lambda: 2 if _depl() == 'p' else 3, ['The uncovered charges must balance: N_{A}x_{p} = N_{D}x_{n}.', 'The lightly doped p-side must spread 1000 times wider: more depletion on the p-side.'], 'semi', 2)

# ---------- diodes, Zener, rectifiers
add(('2024', 'Feb', '2024-02-01', 2), 'diode', 'A zener diode with 5 V zener voltage is used to regulate an unregulated dc voltage input of 25 V. For a 400 Ω resistor connected in series, the zener current is found to be 4 times load current. The load current (I_{L}) and load resistance (R_{L}) are :',
    ['I_{L} = 0.02 mA; R_{L} = 250 Ω', 'I_{L} = 10 mA; R_{L} = 500 Ω', 'I_{L} = 20 mA; R_{L} = 250 Ω', 'I_{L} = 10 A; R_{L} = 0.5 Ω'], 2,
    lambda: (lambda V, Is, IL, Iz: pick([(0.02e-3, 250), (10e-3, 500), (20e-3, 250), (10, 0.5)], (round(IL, 6), 500) if abs(Iz - 4 * IL) < 1e-9 else None))(*zener(25, 400, 5, 500)),
    ['Series current = \\f{25 − 5}{400} = 50 mA = I_{Z} + I_{L} = 5I_{L} → I_{L} = 10 mA.', 'R_{L} = \\f{5}{0.01} = 500 Ω.'], 'diode', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'diode', 'In the following circuit (12 V source, 100 Ω in series, then a Zener diode of breakdown voltage 4 V in parallel with a voltmeter and a 400 Ω load with an ammeter in series with the load), the reading of the ammeter will be',
    ['24 mA', '80 mA', '10 mA', '60 mA'], 3, lambda: P4([24, 80, 10, 60], zener(12, 100, 4, 400)[2] * 1000), ['Without the Zener the load would get 12 × \\f{400}{500} = 9.6 V > 4 V, so the Zener conducts and fixes 4 V.', 'I_{load} = \\f{4}{400} = 10 mA.'], 'diode', 1)
def _vout():
    # node joined to +5 V through R; D1 from the node (anode) to a +5 V terminal (cathode); D2 from the node (anode) to ground (cathode)
    for d1, d2 in itertools.product((0, 1), repeat=2):
        V = 0.0 if d2 else (5.0 if d1 else 5.0)
        ok1 = (V >= 5.0) if d1 else (V <= 5.0); ok2 = (V >= 0.0) if d2 else (V <= 0.0)
        I_R = (5 - V) / 1000
        if ok1 and ok2 and (d2 == 0 or I_R >= 0): return V
add(('2025', 'Apr', '2025-04-08', 2), 'diode', 'A node is connected to +5 V through a resistor; V_{out} is taken at this node. Ideal diode D_{1} has its anode at the node and cathode at a +5 V terminal; ideal diode D_{2} has its anode at the node and cathode at ground. The output voltage is (consider ideal diode case)',
    ['+5 V', '0 V', '10 V', '−5 V'], 2, lambda: pick([5, 0, 10, -5], _vout()), ['D_{2} is forward biased (node above ground) and, being ideal, pins the node to 0 V.', 'Then D_{1} sees 0 V on its anode and +5 V on its cathode: reverse biased. V_{out} = 0 V.'], 'diode', 2)
def _pq():
    V, L = 20.0, 0.20; need = 1.8 + 3.2   # LED glow voltage + Zener breakdown, in series across PQ
    lo, hi = 0.0, L
    for _ in range(100):
        x = (lo + hi) / 2
        if V * x / L < need: lo = x
        else: hi = x
    return hi * 100
add(('2024', 'Apr', '2024-04-08', 2), 'diode', 'A potential divider circuit is connected with a dc source of 20 V, a light emitting diode of glow in voltage 1.8 V and a zener diode of breakdown voltage of 3.2 V (LED and Zener in series across the part PQ of the wire). The length (PR) of the resistive wire is 20 cm. The minimum length of PQ to just glow the LED is ______ cm.', None, 5,
    lambda: round(_pq(), 6), ['Across PQ we need 1.8 + 3.2 = 5 V.', 'The wire drops 1 V per cm, so PQ = 5 cm.'], 'diode', 2)
def _bias():
    # (left terminal V, right terminal V, anode side)
    c = dict(A=(-10, 0, 'L'), B=(-10, -15, 'L'), C=(4, 2, 'L'), D=(-5, -10, 'R'), E=(0, 2, 'R'))
    return ''.join(k for k, (l, r, a) in c.items() if (l - r if a == 'L' else r - l) > 0)
add(('2025', 'Jan', '2025-01-22', 1), 'diode', 'Which of the following circuits represents a forward biased diode? (A) anode at −10 V, cathode at 0 V; (B) anode at −10 V, cathode at −15 V; (C) anode at 4 V, cathode at 2 V; (D) cathode at −5 V, anode at −10 V; (E) cathode at 0 V (ground), anode at 2 V.',
    ['(C) and (E) only', '(B), (D) and (E) only', '(A) and (D) only', '(B), (C) and (E) only'], 4, lambda: pick(['CE', 'BDE', 'AD', 'BCE'], _bias()),
    ['Forward bias means the anode is at a higher potential than the cathode.', 'B (−10 > −15), C (4 > 2) and E (2 > 0) qualify; A and D have the anode lower.'], 'diode', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'diode', 'In the given circuit, the breakdown voltage of the Zener diode is 3.0 V. A 10 V source drives a 1 kΩ series resistor, then the Zener in parallel with a 2 kΩ load. What is the value of I_{z}?',
    ['3.3 mA', '5.5 mA', '10 mA', '7 mA'], 2, lambda: P4([3.3, 5.5, 10, 7], zener(10, 1000, 3, 2000)[3] * 1000), ['Series current = \\f{10 − 3}{1000} = 7 mA; load current = \\f{3}{2000} = 1.5 mA.', 'I_{Z} = 7 − 1.5 = 5.5 mA.'], 'diode', 1)
def _rc():
    R, Rd, C = 100.0, 10.0, 20e-6   # anti-parallel diodes: one of them always conducts, whichever way the current flows
    q, t, dt, V = 0.0, 0.0, 1e-7, 1.0
    while q < C * V * (1 - math.exp(-1)): q += (V - q / C) / (R + Rd) * dt; t += dt
    return t / 1e-3
add(('2026', 'Apr', '2026-04-04', 1), 'diode', 'Consider a circuit consisting of a capacitor (20 μF), resistor (100 Ω) and two identical diodes connected in parallel with opposite polarity, all in series with a battery. The resistance of diode under forward biasing condition is 10 Ω. The time constant of the circuit is α × 10^{−3} s. The value of α is ____.',
    ['2.2', '2.0', '2.1', '2.4'], 1, lambda: P4([2.2, 2.0, 2.1, 2.4], _rc(), 3e-3), ['Whichever way the current flows one diode is forward biased (10 Ω) and the other is off.', 'τ = (100 + 10) × 20 × 10^{−6} = 2.2 × 10^{−3} s.'], 'diode', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'diode', 'A Zener diode of breakdown voltage 10 V is used as a voltage regulator: a 20 V source, 200 Ω in series, and a 500 Ω load across the Zener. The current through the Zener diode is',
    ['50 mA', '0', '30 mA', '20 mA'], 3, lambda: P4([50, 1e-9, 30, 20], zener(20, 200, 10, 500)[3] * 1000), ['Series current = \\f{20 − 10}{200} = 50 mA; load = \\f{10}{500} = 20 mA.', 'I_{Z} = 30 mA.'], 'diode', 1)
def _rmin(Vs, Vz, Pmax):
    lo, hi = 1.0, 1e5
    for _ in range(100):
        R = (lo + hi) / 2; Iz = zener(Vs, R, Vz, None)[3]
        if Iz * Vz > Pmax: lo = R
        else: hi = R
    return hi
add(('2026', 'Apr', '2026-04-04', 2), 'diode', 'A diode has Zener voltage of 10 V and maximum power dissipation of 0.5 W, then the minimum resistance to be used in series with this diode for safety when it is connected to a 25 V power supply is ______ Ω.', None, 300,
    lambda: round(_rmin(25, 10, 0.5), 3), ['I_{max} = \\f{0.5}{10} = 50 mA.', 'R = \\f{25 − 10}{0.05} = 300 Ω.'], 'diode', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'diode', 'A voltage regulating circuit consisting of Zener diode, having break-down voltage of 10 V and maximum power dissipation of 0.4 W, is operated at 15 V. The approximate value of protective resistance in this circuit is ______ Ω.', None, 125,
    lambda: round(_rmin(15, 10, 0.4), 3), ['I_{max} = \\f{0.4}{10} = 40 mA.', 'R = \\f{15 − 10}{0.04} = 125 Ω.'], 'diode', 1)
def _three():
    # 12 V → 300 Ω → node; three silicon diodes from the node to ground: D1 and D3 forward, D2 reversed. 0.7 V drop when on
    best = None
    for st in itertools.product((0, 1), repeat=3):
        if st[1]: continue   # D2 points the wrong way: it can never conduct here
        on = sum(st); V = 0.7 if on else 12.0
        I = (12 - V) / 300
        if on and V <= 12: best = (st, I / on)
    return best[1] * 1000
add(('2026', 'Jan', '2026-01-28', 1), 'diode', 'Assuming in forward bias condition there is a voltage drop of 0.7 V across a silicon diode, the current through diode D_{1} in the circuit is ______ mA. (12 V source, R_{1} = 0.3 kΩ in series, then three identical silicon diodes in parallel from the node to the return line: D_{1} and D_{3} forward biased, D_{2} reverse biased.)',
    ['20.15', '11.7', '17.6', '18.8'], 4, lambda: P4([20.15, 11.7, 17.6, 18.8], _three(), 3e-3), ['D_{2} is reverse biased and carries nothing; D_{1} and D_{3} conduct and hold the node at 0.7 V.', 'Total current = \\f{12 − 0.7}{300} = 37.7 mA, shared equally: 18.8 mA each.'], 'diode', 2)

# ---------- logic gates
def _tt(spec): return {tuple(map(int, k)): v for k, v in (x.split('→') for x in spec)}
_ed11 = [['00→1', '10→0', '01→0', '11→0'], ['00→0', '01→0', '10→1', '11→1'], ['00→1', '01→0', '10→0', '11→0'], ['00→0', '10→0', '01→0', '11→1']]
add(('2024', 'Feb', '2024-02-01', 2), 'gate', 'In a circuit, A and B feed an OR gate; the OR output and input A feed an AND gate whose output is C. The truth table (written as AB→C) is :',
    [', '.join(r) for r in _ed11], 2, lambda: [k + 1 for k, r in enumerate(_ed11) if all(int(v) == AND(OR(a, b), a) for (a, b), v in _tt(r).items())][0] if sum(all(int(v) == AND(OR(a, b), a) for (a, b), v in _tt(r).items()) for r in _ed11) == 1 else 0,
    ['C = A·(A + B).', 'Absorption law: A(A + B) = A, so C simply follows A.'], 'gate', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'gate', 'In a logic circuit, A and B feed an AND gate; A is also inverted by a NOT gate; the NOT output and the AND output feed an OR gate whose output is Y. The correct truth table (Y for A B = 00, 01, 10, 11) is :',
    ['0, 1, 0, 1', '1, 1, 0, 1', '1, 1, 0, 0', '0, 0, 0, 1'], 2, lambda: pick([(0, 1, 0, 1), (1, 1, 0, 1), (1, 1, 0, 0), (0, 0, 0, 1)], table(lambda a, b: OR(NOT(a), AND(a, b)))),
    ['Y = Ā + AB = Ā + B.', 'Y is 0 only when A = 1 and B = 0.'], 'gate', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'gate', 'In a circuit, A and B feed an AND gate; Ā and B̄ (through NOT gates) feed a second AND gate; both AND outputs feed a NOR gate with output E. In the truth table, E = X for A = 0, B = 1 and E = Y for A = 1, B = 0. The values of X and Y are :',
    ['1, 1', '1, 0', '0, 1', '0, 0'], 1, lambda: pick([(1, 1), (1, 0), (0, 1), (0, 0)], (lambda f: (f(0, 1), f(1, 0)))(lambda a, b: NOR(AND(a, b), AND(NOT(a), NOT(b))))),
    ['E = NOT(AB + ĀB̄) — the complement of XNOR, i.e. XOR.', 'For unequal inputs E = 1: X = 1, Y = 1.'], 'gate', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'gate', 'In a circuit, input A goes to a NOR gate with both its inputs tied (NOT), and B likewise; these outputs feed a NOR gate; its output goes to another NOR gate with tied inputs, giving the output. The given circuit works as :',
    ['AND gate', 'NOR gate', 'NAND gate', 'OR gate'], 3, lambda: pick(['AND', 'NOR', 'NAND', 'OR'], next(k for k, v in GATES.items() if v == table(lambda a, b: NOR(NOR(NOR(a, a), NOR(b, b)), NOR(NOR(a, a), NOR(b, b)))))),
    ['NOR with tied inputs is NOT: NOR(Ā, B̄) = AB.', 'The last NOT gives \\overline{AB}: a NAND gate.'], 'gate', 2)
def _diode_gate():
    # 5 V → R → C; diodes from C (anode) to inputs A, B (cathodes). Ideal: an input at 0 V pulls C down
    out = []
    for a, b in itertools.product((0, 5), repeat=2):
        V = min(5.0, a, b); out.append(1 if V > 2.5 else 0)
    return tuple(out)
add(('2026', 'Jan', '2026-01-28', 2), 'gate', 'Two p-n junction diodes D_{1} and D_{2} have their anodes joined at output C, which is connected to V_{dc} = 5 V through a resistor R; their cathodes are the inputs A and B. The given circuit will function as a ____ .',
    ['NAND Gate', 'OR Gate', 'AND Gate', 'NOR Gate'], 3, lambda: pick(['NAND', 'OR', 'AND', 'NOR'], next(k for k, v in GATES.items() if v == _diode_gate())),
    ['If either input is LOW its diode conducts and pulls C LOW.', 'C is HIGH only when both inputs are HIGH: an AND gate.'], 'gate', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'gate', 'If X and Y are the inputs, each goes through a NAND gate with tied inputs; these outputs feed a NAND gate, whose output goes through another NAND gate with tied inputs to the output. The given circuit works as ______ .',
    ['OR gate', 'AND gate', 'NAND gate', 'NOR gate'], 4, lambda: pick(['OR', 'AND', 'NAND', 'NOR'], next(k for k, v in GATES.items() if v == table(lambda x, y: NAND(NAND(NAND(x, x), NAND(y, y)), NAND(NAND(x, x), NAND(y, y)))))),
    ['NAND(X̄, Ȳ) = X + Y.', 'The final NOT gives \\overline{X + Y}: a NOR gate.'], 'gate', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'gate', 'In a circuit, A and B feed an AND gate, and Ā and B̄ feed a second AND gate; both outputs go into gate G, whose output Y follows the truth table Y = 1, 0, 0, 1 for A B = 00, 01, 10, 11. To obtain the given truth table, the following logic gate should be placed at G :',
    ['OR Gate', 'AND Gate', 'NAND Gate', 'NOR Gate'], 1,
    lambda: pick(['OR', 'AND', 'NAND', 'NOR'], next(k for k in ('OR', 'AND', 'NAND', 'NOR') if table(lambda a, b: dict(OR=OR, AND=AND, NAND=NAND, NOR=NOR)[k](AND(a, b), AND(NOT(a), NOT(b)))) == (1, 0, 0, 1))),
    ['The two AND outputs are AB and ĀB̄.', 'Y = AB + ĀB̄ (XNOR) needs an OR gate at G.'], 'gate', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'gate', 'In a circuit, A and B̄ feed one AND gate, Ā and B feed another AND gate, and both outputs feed an OR gate with output Y. The truth table (Y for A B = 00, 01, 10, 11) is :',
    ['1, 0, 0, 1', '0, 1, 1, 0', '0, 1, 0, 1', '1, 1, 1, 0'], 2, lambda: pick([(1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1), (1, 1, 1, 0)], table(lambda a, b: OR(AND(a, NOT(b)), AND(NOT(a), b)))),
    ['Y = AB̄ + ĀB: the XOR gate.', 'Y = 1 only when the inputs differ.'], 'gate', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'gate', 'In a circuit, A and B̄ feed one AND gate, Ā and B feed another, and both feed an OR gate with output Y. The truth table for the circuit (Y for A B = 00, 01, 10, 11) is :',
    ['0, 1, 1, 0', '0, 0, 1, 0', '0, 0, 0, 1', '0, 1, 1, 1'], 1, lambda: pick([(0, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 1), (0, 1, 1, 1)], table(lambda a, b: OR(AND(a, NOT(b)), AND(NOT(a), b)))),
    ['Y = AB̄ + ĀB (exclusive OR).', 'Rows: 0, 1, 1, 0.'], 'gate', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'gate', 'Identify the logic operation performed by the given circuit: A and B each pass through a NOT gate, and the two outputs feed a NAND gate giving Y.',
    ['NAND', 'NOR', 'OR', 'AND'], 3, lambda: pick(['NAND', 'NOR', 'OR', 'AND'], next(k for k, v in GATES.items() if v == table(lambda a, b: NAND(NOT(a), NOT(b))))),
    ['Y = \\overline{Ā·B̄}.', 'De Morgan: = A + B, an OR gate.'], 'gate', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'gate', 'In a logic circuit, A and B feed an AND gate followed by a NOT gate; C and D feed an OR gate; these two outputs feed an AND gate followed by a NOT gate giving Y. The correct truth table for the inputs (A B C D) = 1101, 0011, 1010, 1111 is Y =',
    ['0, 1, 1, 1', '0, 0, 1, 1', '1, 0, 0, 1', '1, 0, 1, 0'], 3, lambda: pick([(0, 1, 1, 1), (0, 0, 1, 1), (1, 0, 0, 1), (1, 0, 1, 0)], rows(lambda a, b, c, d: NOT(AND(NOT(AND(a, b)), OR(c, d))), [(1, 1, 0, 1), (0, 0, 1, 1), (1, 0, 1, 0), (1, 1, 1, 1)])),
    ['Y = \\overline{\\overline{AB}·(C + D)} = AB + C̄D̄.', '1101 → 1; 0011 → 0; 1010 → 0; 1111 → 1.'], 'gate', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'gate', 'In a logic circuit, n and m feed an OR gate; the OR output and n feed a NAND gate giving z. Which of the following is the correct truth table (z for n m = 00, 01, 11, 10)?',
    ['1, 0, 0, 0', '0, 1, 0, 1', '1, 0, 1, 0', '1, 1, 0, 0'], 4, lambda: pick([(1, 0, 0, 0), (0, 1, 0, 1), (1, 0, 1, 0), (1, 1, 0, 0)], rows(lambda n, m: NAND(n, OR(n, m)), [(0, 0), (0, 1), (1, 1), (1, 0)])),
    ['z = \\overline{n(n + m)} = n̄ (absorption).', 'z = 1 when n = 0, else 0.'], 'gate', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'gate', 'In a logic circuit, A goes into an AND gate with both inputs tied, B goes into a NAND gate with tied inputs followed by an AND gate with tied inputs, and the two results feed a final AND gate giving Y. Identify the correct truth table (Y for A B = 00, 01, 10, 11).',
    ['0, 1, 1, 0', '1, 0, 1, 0', '1, 1, 1, 0', '0, 0, 1, 0'], 4, lambda: pick([(0, 1, 1, 0), (1, 0, 1, 0), (1, 1, 1, 0), (0, 0, 1, 0)], table(lambda a, b: AND(AND(a, a), AND(NAND(b, b), NAND(b, b))))),
    ['AND with tied inputs passes A; NAND with tied inputs gives B̄.', 'Y = AB̄: 1 only for A = 1, B = 0.'], 'gate', 2)
for _p in P: _p['t'] = _p['fam']
