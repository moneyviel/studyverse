"""Real JEE Main questions — Physics Unit 14: Electromagnetic Induction and Alternating Currents. Our own solutions;
chk re-solves each one from the raw data in SI units — emfs from the rate of change of flux (often by numerical
differencing of Φ(t)), motional emfs from (v × B)·dl summed along the conductor, LR/LC behaviour by stepping the
circuit equation in time, and ac circuits with complex impedances. Skipped: items whose printed figure or key we
could not confirm."""
import math, cmath
from common import new_registry, pick, verify
P, add = new_registry()
mu0 = 4e-7 * math.pi; pi = math.pi
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)
def Z(R=0, L=0, C=None, w=1): return complex(R, w * L - (1 / (w * C) if C else 0))
def ddt(f, t, h=1e-6): return (f(t + h) - f(t - h)) / (2 * h)
def rms(f, T, n=200000): return math.sqrt(sum(f(T * (k + 0.5) / n) ** 2 for k in range(n)) / n)
def motional(pts, v, B, n=400):   # emf = ∫ (v × B)·dl along a polyline (2D in xy, B along z)
    s = 0.0
    for a, b in zip(pts, pts[1:]):
        dl = (b[0] - a[0], b[1] - a[1]); vxB = (v[1] * B, -v[0] * B); s += vxB[0] * dl[0] + vxB[1] * dl[1]
    return s

# ---------- sheet 1
add(('2024', 'Feb', '2024-02-01', 1), 'ac', 'A parallel plate capacitor has a capacitance C = 200 pF. It is connected to 230 V ac supply with an angular frequency 300 rad/s. The rms value of conduction current in the circuit and displacement current in the capacitor respectively are :',
    ['1.38 μA and 1.38 μA', '14.3 μA and 143 μA', '13.8 μA and 138 μA', '13.8 μA and 13.8 μA'], 4,
    lambda: 4 if abs(abs(230 / Z(C=200e-12, w=300)) - 13.8e-6) < 0.05e-6 else 0,
    ['I = ωCV = 300 × 200 × 10^{−12} × 230 = 13.8 μA.', 'The displacement current between the plates equals the conduction current in the wires: both 13.8 μA.'], 'ac', 1)
add(('2024', 'Feb', '2024-02-01', 1), 'ac', 'In series LCR circuit, the capacitance is changed from C to 4C. To keep the resonance frequency unchanged, the new inductance should be :',
    ['reduced by \\f{1}{4} L', 'increased by 2 L', 'reduced by \\f{3}{4} L', 'increased to 4 L'], 3,
    lambda: P4([1 - 0.25, 3, 1 - 0.75, 4], 1 / 4), ['Resonance needs LC fixed: L′ × 4C = LC → L′ = \\f{L}{4}.', 'That is a reduction by \\f{3}{4} L.'], 'ac', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'ac', 'A transformer has an efficiency of 80% and works at 10 V and 4 kW. If the secondary voltage is 240 V, then the current in the secondary coil is :',
    ['1.59 A', '13.33 A', '1.33 A', '15.1 A'], 2, lambda: P4([1.59, 13.33, 1.33, 15.1], 0.8 * 4000 / 240), ['Output power = 0.8 × 4000 = 3200 W.', 'I_{s} = \\f{3200}{240} = 13.33 A.'], 'ac', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'ac', 'An electric bulb rated as 100 W – 220 V is connected to an ac source of rms voltage 220 V. The peak value of current through the bulb is :',
    ['0.45 A', '0.64 A', '2.2 A', '0.32 A'], 2, lambda: P4([0.45, 0.64, 2.2, 0.32], math.sqrt(2) * 220 / (220 ** 2 / 100), 5e-3), ['R = \\f{V^{2}}{P} = 484 Ω, I_{rms} = \\f{220}{484} = 0.455 A.', 'I_{0} = √{2} I_{rms} = 0.64 A.'], 'ac', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'ac', 'An alternating current is represented by the equation i = 100√{2} sin(100πt) ampere. The RMS value of current and the frequency of the given alternating current are',
    ['50√{2} A, 50 Hz', '\\f{100}{√{2}} A, 100 Hz', '100 A, 50 Hz', '100√{2} A, 100 Hz'], 3,
    lambda: 3 if abs(rms(lambda t: 100 * math.sqrt(2) * math.sin(100 * pi * t), 0.02, 20000) - 100) < 1e-3 and abs(100 * pi / (2 * pi) - 50) < 1e-12 else 0,
    ['I_{rms} = \\f{I_{0}}{√{2}} = 100 A.', 'ω = 100π → f = \\f{ω}{2π} = 50 Hz.'], 'ac', 1)
def _abcde():
    s = 0.1 / math.sqrt(2)
    A = (0.1, 2 * s); Bp = (0, 2 * s); C = (-s, s); D = (0, 0); E = (0.1, 0)
    return abs(motional([A, Bp, C, D, E], (0.1, 0), 1 / math.sqrt(2))) * 1000
add(('2025', 'Apr', '2025-04-04', 1), 'motional', 'Conductor wire ABCDE with each arm 10 cm in length is placed in magnetic field of \\f{1}{√{2}} Tesla, perpendicular to its plane. AB and DE are horizontal; BC and CD make a 90° corner at C, symmetric about the horizontal. When the conductor is pulled towards the right with constant velocity of 10 cm/s, induced emf between points A and E is ______ mV.', None, 10,
    lambda: round(_abcde(), 6), ['Only the length perpendicular to v counts: the straight line from A to E is vertical.', 'Its length = 2 × 10 sin 45° = 10√{2} cm.', 'ε = Bvℓ = \\f{1}{√{2}} × 0.1 × 0.1√{2} = 0.01 V = 10 mV.'], 'motional', 2)

# ---------- sheet 2
add(('2025', 'Apr', '2025-04-04', 2), 'ac', 'An inductor of self inductance 1 H is connected in series with a resistor of 100π ohm and an ac supply of 100π volt (rms), 50 Hz. Maximum current flowing in the circuit is ______ A.', None, 1,
    lambda: round(math.sqrt(2) * 100 * pi / abs(Z(100 * pi, 1, w=2 * pi * 50)), 9), ['X_{L} = 2π × 50 × 1 = 100π Ω, so Z = √{(100π)^{2} + (100π)^{2}} = 100√{2}π Ω.', 'I_{rms} = \\f{100π}{100√{2}π} = \\f{1}{√{2}} A; the maximum (peak) current is √{2} × that = 1 A.'], 'ac', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'ac', 'Match the circuit with its phasor diagram. (A) Purely capacitive circuit, (B) Purely inductive circuit, (C) LCR series at resonance, (D) LCR series circuit (general). Phasors: (I) I is 90° ahead of V; (II) I and V along the same line; (III) V ahead of I by some angle θ; (IV) V is 90° ahead of I.',
    ['A-I, B-IV, C-III, D-II', 'A-IV, B-I, C-III, D-II', 'A-IV, B-I, C-II, D-III', 'A-I, B-IV, C-II, D-III'], 4,
    lambda: pick(['I IV III II', 'IV I III II', 'IV I II III', 'I IV II III'], ' '.join(['I' if cmath.phase(1 / Z(C=1, w=1)) > 0 else 'IV', 'IV' if cmath.phase(Z(L=1)) > 0 else 'I', 'II' if abs(cmath.phase(Z(1, 1, 1))) < 1e-12 else 'III', 'III'])),
    ['Capacitor: current leads voltage by 90° → (I).', 'Inductor: voltage leads current by 90° → (IV).', 'At resonance X_{L} = X_{C}, so V and I are in phase → (II); in general they differ by some θ → (III).'], 'ac', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'ac', 'In an ac circuit, the instantaneous current is zero, when the instantaneous voltage is maximum. In this case, the source may be connected to : A. pure inductor. B. pure capacitor. C. pure resistor. D. combination of an inductor and capacitor.',
    ['A, B and C only', 'B, C and D only', 'A and B only', 'A, B and D only'], 4,
    lambda: pick(['ABC', 'BCD', 'AB', 'ABD'], ''.join(k for k, z in zip('ABCD', [Z(L=1), Z(C=1), Z(1), Z(L=1, C=0.5)]) if abs(abs(cmath.phase(z)) - pi / 2) < 1e-12)),
    ['Current is zero at peak voltage only when the phase difference is 90°.', 'That happens for a pure L, a pure C, and any L–C combination with no resistance; a resistor keeps them in phase.'], 'ac', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'ac', 'An alternating current at any instant is given by i = [6 + √{56} sin(100πt + \\f{π}{3})] A. The rms value of the current is ______ A.', None, 8,
    lambda: round(rms(lambda t: 6 + math.sqrt(56) * math.sin(100 * pi * t + pi / 3), 0.02, 40000), 6), ['Square and average over a cycle: the cross term averages to zero.', 'I_{rms}^{2} = 6^{2} + \\f{56}{2} = 64 → I_{rms} = 8 A.'], 'ac', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'ac', 'A series LCR circuit is subjected to an AC signal of 200 V, 50 Hz. If the voltage across the inductor (L = 10 mH) is 31.4 V, then the current in this circuit is',
    ['68 A', '63 A', '10 A', '10 mA'], 3, lambda: P4([68, 63, 10, 0.01], 31.4 / (2 * pi * 50 * 0.01), 2e-3), ['X_{L} = 2π × 50 × 0.01 = 3.14 Ω.', 'I = \\f{31.4}{3.14} = 10 A (the same current flows through every element).'], 'ac', 1)

# ---------- sheet 3
add(('2024', 'Apr', '2024-04-05', 2), 'induct', 'The current in an inductor is given by I = (3t + 8) where t is in second. The magnitude of induced emf produced in the inductor is 12 mV. The self-inductance of the inductor is ______ mH.', None, 4,
    lambda: round(12e-3 / ddt(lambda t: 3 * t + 8, 1.0) * 1000, 6), ['\\f{dI}{dt} = 3 A/s.', 'L = \\f{ε}{dI/dt} = \\f{12 mV}{3} = 4 mH.'], 'induct', 1)
def _mut():
    a, b = 0.01, 1.0; Bc = mu0 * 1 / (2 * b); return Bc * pi * a * a / (mu0 * pi * a * a / (2 * b))
add(('2024', 'Apr', '2024-04-05', 1), 'induct', 'Two conducting circular loops A (radius a) and B (radius b) are placed in the same plane with their centres coinciding, b ≫ a. The mutual inductance between them is:',
    ['\\f{μ_{0}πa^{2}}{2b}', '\\f{μ_{0}}{2π}·\\f{b^{2}}{a}', '\\f{μ_{0}πb^{2}}{2a}', '\\f{μ_{0}}{2π}·\\f{a^{2}}{b}'], 1,
    lambda: P4([pi / 2 * 1e-4, 1 / (2 * pi) * 1e4, pi / 2 * 1e4, 1e-4 / (2 * pi)], mu0 * 1 / (2 * 1.0) * pi * 0.01 ** 2 / mu0),
    ['Pass current I through the big loop B: near its centre B = \\f{μ_{0}I}{2b}, nearly uniform over the tiny loop.', 'Flux through A = \\f{μ_{0}I}{2b}·πa^{2}, so M = \\f{μ_{0}πa^{2}}{2b}.'], 'induct', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'ac', 'An alternating voltage of amplitude 40 V and frequency 4 kHz is applied directly across the capacitor of 12 μF. The maximum displacement current between the plates of the capacitor is nearly:',
    ['13 A', '8 A', '10 A', '12 A'], 4, lambda: P4([13, 8, 10, 12], 40 * 2 * pi * 4000 * 12e-6, 0.03), ['I_{0} = ωCV_{0} = 2π × 4000 × 12 × 10^{−6} × 40.', '≈ 12 A; the displacement current between the plates equals the conduction current.'], 'ac', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'ac', 'An ac source V = 50√{2} sin 100t volt is connected to a series circuit with L = 1 H, C = 20 μF and R = 300 Ω. The rms potential difference across the capacitor of 20 μF is ______ V.', None, 50,
    lambda: round(50 / abs(Z(300, 1, 20e-6, 100)) * (1 / (100 * 20e-6)), 6), ['X_{L} = 100 Ω, X_{C} = \\f{1}{100 × 20 × 10^{−6}} = 500 Ω.', 'Z = √{300^{2} + 400^{2}} = 500 Ω, I_{rms} = \\f{50}{500} = 0.1 A.', 'V_{C} = 0.1 × 500 = 50 V.'], 'ac', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'induct', 'In a coil, the current changes from −2 A to +2 A in 0.2 s and induces an emf of 0.1 V. The self inductance of the coil is :',
    ['5 mH', '1 mH', '2.5 mH', '4 mH'], 1, lambda: P4([5, 1, 2.5, 4], 0.1 / (4 / 0.2) * 1000), ['\\f{dI}{dt} = \\f{4}{0.2} = 20 A/s.', 'L = \\f{0.1}{20} = 5 mH.'], 'induct', 1)

# ---------- sheets 4–5
add(('2024', 'Apr', '2024-04-06', 2), 'ac', 'For a given series LCR circuit it is found that maximum current is drawn when value of variable capacitance is 2.5 nF. If resistance of 200 Ω and 100 mH inductor is being used in the given circuit, the frequency of ac source is ______ × 10^{3} Hz. (given π^{2} = 10)', None, 10,
    lambda: round(1 / (2 * math.sqrt(10) * math.sqrt(0.1 * 2.5e-9)) / 1e3, 6), ['Maximum current means resonance: f = \\f{1}{2π√{LC}}.', '√{LC} = √{0.1 × 2.5 × 10^{−9}} = 5 × 10^{−6}/√{10}; with 2π = 2√{10}, f = \\f{1}{10^{−4}} = 10 × 10^{3} Hz.'], 'ac', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'ac', 'Statement I : In an LCR series circuit, current is maximum at resonance. Statement II : Current in a purely resistive circuit can never be less than that in a series LCR circuit when connected to same voltage source (same R).',
    ['Statement I is true but Statement II is false', 'Statement I is false but Statement II is true', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false'], 3,
    lambda: 3 if all(abs(Z(100, L, 1e-6, w)) >= 100 - 1e-9 for L in (0.01, 0.1, 1) for w in (100, 1000, 10000)) and abs(Z(100, 1, 1e-6, 1000)) == 100 else 0,
    ['Z = √{R^{2} + (X_{L} − X_{C})^{2}} is smallest (= R) at resonance → I is maximum there: I is true.', 'Since Z ≥ R always, \\f{V}{Z} ≤ \\f{V}{R}: II is true.'], 'ac', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'ac', 'When a dc voltage of 100 V is applied to an inductor, a dc current of 5 A flows through it. When an ac voltage of 200 V peak value is connected to the inductor, its inductive reactance is found to be 20√{3} Ω. The power dissipated in the circuit is ______ W.', None, 250,
    lambda: round((200 / math.sqrt(2) / abs(Z(20, 20 * math.sqrt(3) / 1, w=1))) ** 2 * 20, 6), ['dc gives the coil\'s resistance: R = \\f{100}{5} = 20 Ω.', 'Z = √{20^{2} + (20√{3})^{2}} = 40 Ω, I_{rms} = \\f{200/√{2}}{40} = \\f{5}{√{2}} A.', 'P = I_{rms}^{2}R = 12.5 × 20 = 250 W.'], 'ac', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'ac', 'An ac current is represented as i = 5√{2} + 10 cos(650πt + \\f{π}{6}) Amp. The r.m.s value of the current is',
    ['100 Amp', '10 Amp', '5√{2} Amp', '50 Amp'], 2, lambda: P4([100, 10, 5 * math.sqrt(2), 50], rms(lambda t: 5 * math.sqrt(2) + 10 * math.cos(650 * pi * t + pi / 6), 2 / 650, 40000)), ['I_{rms}^{2} = (5√{2})^{2} + \\f{10^{2}}{2} = 50 + 50.', 'I_{rms} = 10 A.'], 'ac', 2)
def _shift():
    R, C = 1e5, 1e-10
    for x in range(1, 10):
        w = 10 ** x; zc = 1 / complex(0, w * C); VA = zc / (R + zc); VB = R / (zc + R)
        if abs(abs(cmath.phase(VB - VA)) - pi / 2) < 1e-9: return x
add(('2025', 'Apr', '2025-04-07', 1), 'ac', 'In an ac circuit two branches are connected across the same source V_{in}: branch 1 is R then C (A is the junction, so V_{A} is the voltage across this C), and branch 2 is C then R (B is the junction, V_{B} is the voltage across this R). R = 100 kΩ and C = 100 pF and the phase difference between V_{in} and (V_{B} − V_{A}) is 90°. The input signal frequency is 10^{x} rad/sec, where x is ____.', None, 5,
    lambda: _shift(), ['V_{B} − V_{A} = V_{in}\\f{jωRC − 1}{jωRC + 1}: its size is always V_{in}, its phase is π − 2 tan^{−1}(ωRC).', 'For 90°: ωRC = 1 → ω = \\f{1}{10^{5} × 10^{−10}} = 10^{5} rad/s, x = 5.'], 'ac', 3)
add(('2025', 'Apr', '2025-04-07', 2), 'ac', 'An inductor of reactance 100 Ω, a capacitor of reactance 50 Ω, and a resistor of resistance 50 Ω are connected in series with an AC source of 10 V, 50 Hz. Average power dissipated by the circuit is ______ W.', None, 1,
    lambda: round(abs(10 / complex(50, 50)) ** 2 * 50, 9), ['Z = √{50^{2} + (100 − 50)^{2}} = 50√{2} Ω.', 'I_{rms} = \\f{10}{50√{2}}, P = I^{2}R = \\f{100}{5000} × 50 = 1 W.'], 'ac', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'ac', 'A coil of negligible resistance is connected in series with 90 Ω resistor across 120 V, 60 Hz supply. A voltmeter reads 36 V across resistance. Inductance of the coil is :',
    ['0.76 H', '2.86 H', '0.286 H', '0.91 H'], 1, lambda: P4([0.76, 2.86, 0.286, 0.91], math.sqrt(120 ** 2 - 36 ** 2) / (36 / 90) / (2 * pi * 60), 5e-3), ['I = \\f{36}{90} = 0.4 A.', 'V_{L} = √{120^{2} − 36^{2}} = 114.5 V → X_{L} = 286 Ω.', 'L = \\f{286}{2π × 60} = 0.76 H.'], 'ac', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'ac', 'An alternating emf E = 110√{2} sin 100t volt is applied to a capacitor of 2 μF, the rms value of current in the circuit is ______ mA.', None, 22,
    lambda: round(110 / abs(Z(C=2e-6, w=100)) * 1000, 6), ['X_{C} = \\f{1}{ωC} = \\f{1}{100 × 2 × 10^{−6}} = 5000 Ω.', 'I_{rms} = \\f{110}{5000} = 22 mA.'], 'ac', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'ac', 'A LCR circuit is at resonance for a capacitor C, inductance L and resistance R. Now the value of resistance is halved keeping all other parameters same. The current amplitude at resonance will be now:',
    ['Zero', 'double', 'same', 'halved'], 2, lambda: P4([0, 2, 1, 0.5], abs(1 / Z(50, 1, 1e-6, 1000)) / abs(1 / Z(100, 1, 1e-6, 1000))), ['At resonance Z = R, so I_{0} = \\f{V_{0}}{R}.', 'Halving R doubles the current amplitude.'], 'ac', 1)

# ---------- sheets 6–7
def _sq(t):
    v, a, W, B = 0.02, 0.15, 0.50, 1.0
    def phi(t): x = v * t; return B * a * max(0.0, min(x, a, W, W + a - x))   # overlap length × side
    return abs(ddt(phi, t, 1e-4))
add(('2024', 'Apr', '2024-04-09', 2), 'flux', 'A square loop of side 15 cm is being moved towards right at a constant speed of 2 cm/s. The front edge enters a 50 cm wide region of uniform magnetic field B = 1.0 T (perpendicular to the loop) at t = 0. The value of induced emf in the loop at t = 10 s will be :',
    ['0.3 mV', '4.5 mV', 'zero', '3 mV'], 3, lambda: pick([0.3e-3, 4.5e-3, 0, 3e-3], round(_sq(10.0), 9)), ['The loop is fully inside after \\f{15}{2} = 7.5 s and its front edge leaves at \\f{50}{2} = 25 s.', 'At t = 10 s the whole loop is inside: flux is constant, so ε = 0.'], 'flux', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'ac', 'A capacitor of reactance 4√{3} Ω and a resistor of resistance 4 Ω are connected in series with an ac source of peak value 8√{2} V. The power dissipation in the circuit is ______ W.', None, 4,
    lambda: round(abs(8 / complex(4, -4 * math.sqrt(3))) ** 2 * 4, 9), ['Z = √{4^{2} + 48} = 8 Ω, V_{rms} = 8 V → I_{rms} = 1 A.', 'P = I^{2}R = 4 W.'], 'ac', 1)
def _sqloop():
    L, R, I = 1.0, 0.01, 1.0; h = L / 2; c = [(h, -h), (h, h), (-h, h), (-h, -h), (h, -h)]; B = 0.0
    for (x1, y1), (x2, y2) in zip(c, c[1:]):   # each side: μ0 I/(4π d)(sin α1 + sin α2) at the centre
        B += mu0 * I / (4 * pi * h) * 2 * (h / math.hypot(h, h))
    return B * pi * R * R / I / (mu0 * R * R / L)
add(('2026', 'Apr', '2026-04-02', 2), 'induct', 'A circular current loop of radius R is placed inside square loop of side length L (L ≫ R) such that they are co-planar and their centers coincide. The permeability of free space is μ_{0}. The mutual inductance between circular loop and square loop is ______.',
    ['2√{2}\\f{μ_{0}L^{2}}{R}', '√{2}\\f{μ_{0}L^{2}}{R}', '√{2}\\f{μ_{0}R^{2}}{L}', '2√{2}\\f{μ_{0}R^{2}}{L}'], 4,
    lambda: pick([1e9, 1e9, math.sqrt(2), 2 * math.sqrt(2)], round(_sqloop(), 9), 1e-6),
    ['Send I round the square: each side is \\f{L}{2} from the centre and subtends 45° each way.', 'B = 4 × \\f{μ_{0}I}{4π(L/2)}(2 sin 45°) = \\f{2√{2}μ_{0}I}{πL}, almost uniform over the small circle.', 'M = \\f{BπR^{2}}{I} = 2√{2}\\f{μ_{0}R^{2}}{L}.'], 'induct', 2)
def _lc():
    L, C = 1.0, 1.0; q, i, dt, t, U0 = 1.0, 0.0, 1e-5, 0.0, 0.5
    while 0.5 * L * i * i < 0.25 * U0: i += -q / (L * C) * dt; q += i * dt; t += dt
    return t / (pi * math.sqrt(L * C))
add(('2026', 'Jan', '2026-01-21', 2), 'induct', 'A capacitor C is first charged fully with potential difference of V_{0} and disconnected from the battery. The charged capacitor is connected across an inductor having inductance L. In the time t s 25% of the initial energy in the capacitor is transferred to the inductor. The value of t is ______ s.',
    ['\\f{π√{LC}}{3}', '\\f{π√{LC}}{6}', '\\f{π√{LC}}{2}', 'π√{\\f{LC}{2}}'], 2, lambda: P4([1 / 3, 1 / 6, 1 / 2, 1 / math.sqrt(2)], _lc(), 2e-3),
    ['q = Q cos ωt, so the capacitor keeps cos^{2} ωt of the energy and the inductor gets sin^{2} ωt.', 'sin^{2} ωt = \\f{1}{4} → ωt = \\f{π}{6} → t = \\f{π√{LC}}{6}.'], 'induct', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'ac', 'A series LCR circuit is connected to an alternating source of emf E. The current amplitude at resonant frequency is I_{0}. If the value of resistance R becomes twice of its initial value then amplitude of current at resonance will be',
    ['\\f{I_{0}}{√{2}}', '2I_{0}', '\\f{I_{0}}{2}', 'I_{0}'], 3, lambda: P4([1 / math.sqrt(2), 2, 0.5, 1], abs(1 / Z(200, 1, 1e-6, 1000)) / abs(1 / Z(100, 1, 1e-6, 1000))), ['At resonance the reactances cancel and I_{0} = \\f{E_{0}}{R}.', 'Doubling R halves it: \\f{I_{0}}{2}.'], 'ac', 1)

# ---------- sheets 8–9
def _out():   # loop of side a leaving the field at speed v: flux = B a (a − v t) while partly inside
    B, a, v = 1.0, 0.2, 0.05; e = [abs(ddt(lambda t: B * a * max(0.0, a - v * t), t, 1e-5)) for t in (0.5, 1.5, 2.5, 3.5)]
    return 3 if max(e) - min(e) < 1e-9 else 0
add(('2025', 'Jan', '2025-01-22', 2), 'flux', 'A rectangular metallic loop is moving out of a uniform magnetic field region to a field free region with a constant speed. When the loop is partially inside the magnetic field, the plot of magnitude of induced emf (ε) with time (t) is given by',
    ['ε falls along a curve (concave up) as t increases', 'ε rises along a curve (concave up) as t increases', 'a horizontal line: ε stays constant', 'a straight line through the origin: ε ∝ t'], 3, lambda: _out(),
    ['The flux falls linearly: Φ = Bℓ(x_{0} − vt) for the part still inside.', 'ε = Bℓv is constant while the loop is partly inside.'], 'flux', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'induct', 'Regarding self-inductance: A. The self-inductance of the coil depends on its geometry. B. Self-inductance does not depend on the permeability of the medium. C. Self-induced e.m.f. opposes any change in the current in a circuit. D. Self-inductance is electromagnetic analogue of mass in mechanics. E. Work needs to be done against self-induced e.m.f. in establishing the current.',
    ['A, B, C, E only', 'A, C, D, E only', 'A, B, C, D only', 'B, C, D, E only'], 2,
    lambda: pick(['ABCE', 'ACDE', 'ABCD', 'BCDE'], ''.join(k for k, ok in zip('ABCDE', [True, (lambda L: L(1) == L(2))(lambda mu: mu * 1000 ** 2 * 1e-4 * 0.5) , True, True, True]) if ok)),
    ['L = μN^{2}A/ℓ for a solenoid: it depends on geometry AND on the permeability of the core, so B is false.', 'The induced emf opposes changes (Lenz), L plays the role of inertia, and energy ½LI^{2} is the work done against the back emf.'], 'induct', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'ac', 'In a series LCR circuit, a resistor of 300 Ω, a capacitor of 25 nF and an inductor of 100 mH are used. For maximum current in the circuit, the angular frequency of the ac source is ______ × 10^{4} radians s^{−1}.', None, 2,
    lambda: round(1 / math.sqrt(0.1 * 25e-9) / 1e4, 6), ['Maximum current at resonance: ω = \\f{1}{√{LC}}.', '= \\f{1}{√{0.1 × 25 × 10^{−9}}} = 2 × 10^{4} rad/s.'], 'ac', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'ac', 'An alternating current is given by I = I_{A} sin ωt + I_{B} cos ωt. The r.m.s current will be',
    ['\\f{|I_{A} + I_{B}|}{√{2}}', '√{\\f{I_{A}^{2} + I_{B}^{2}}{2}}', '√{I_{A}^{2} + I_{B}^{2}}', '\\f{√{I_{A}^{2} + I_{B}^{2}}}{2}'], 2,
    lambda: P4([7 / math.sqrt(2), 5 / math.sqrt(2), 5, 2.5], rms(lambda t: 3 * math.sin(t) + 4 * math.cos(t), 2 * pi, 20000)),
    ['I_{A} sin ωt + I_{B} cos ωt is one sinusoid of amplitude √{I_{A}^{2} + I_{B}^{2}}.', 'Divide the amplitude by √{2}: I_{rms} = √{\\f{I_{A}^{2} + I_{B}^{2}}{2}}.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'flux', 'A rectangular loop of length 2.5 m and width 2 m is placed with its normal at 60° to a magnetic field of 4 T. The loop is removed from the field in 10 sec. The average emf induced in the loop during this time is',
    ['−2 V', '+2 V', '+1 V', '−1 V'], 3, lambda: P4([-2, 2, 1, -1], -(0 - 4 * 2.5 * 2 * math.cos(pi / 3)) / 10), ['Initial flux Φ = BA cos 60° = 4 × 5 × ½ = 10 Wb; final flux 0.', 'ε = −\\f{ΔΦ}{Δt} = −\\f{0 − 10}{10} = +1 V.'], 'flux', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'induct', 'Two coils have mutual inductance 0.002 H. The current changes in the first coil according to the relation i = i_{0} sin ωt, where i_{0} = 5 A and ω = 50π rad/s. The maximum value of emf in the second coil is \\f{π}{α} V. The value of α is', None, 2,
    lambda: round(pi / max(abs(0.002 * ddt(lambda t: 5 * math.sin(50 * pi * t), k * 1e-4)) for k in range(400)), 4), ['ε = M\\f{di}{dt} = Mi_{0}ω cos ωt.', 'Maximum = 0.002 × 5 × 50π = \\f{π}{2} → α = 2.'], 'induct', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'ac', 'Primary side of a transformer is connected to 230 V, 50 Hz supply. Turns ratio of primary to secondary winding is 10 : 1. Load resistance connected to secondary side is 46 Ω. The power consumed in it is :',
    ['12.5 W', '10.0 W', '11.5 W', '12.0 W'], 3, lambda: P4([12.5, 10, 11.5, 12], (230 / 10) ** 2 / 46), ['V_{s} = \\f{230}{10} = 23 V.', 'P = \\f{23^{2}}{46} = 11.5 W.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'ac', 'A series LCR circuit with L = \\f{100}{π} mH, C = \\f{10^{−3}}{π} F and R = 10 Ω, is connected across an ac source of 220 V, 50 Hz supply. The power factor of the circuit would be', None, 1,
    lambda: round(math.cos(cmath.phase(Z(10, 0.1 / pi, 1e-3 / pi, 100 * pi))), 9), ['X_{L} = 100π × \\f{0.1}{π} = 10 Ω, X_{C} = \\f{1}{100π × 10^{−3}/π} = 10 Ω.', 'They cancel (resonance), so cos φ = \\f{R}{Z} = 1.'], 'ac', 1)

# ---------- sheets 10–11
def _vrail():
    B, v, th = 1.0, 1.0, pi / 4
    emf = lambda t: B * v * 2 * v * t * math.tan(th)   # bar length across a V of half-angle θ at distance vt from the vertex
    return round(math.log(emf(2.0) / emf(1.0)) / math.log(2), 9)
add(('2025', 'Jan', '2025-01-28', 2), 'motional', 'A conducting bar moves on two conducting rails that form a V (the bar slides across the V, perpendicular to its axis). A constant magnetic field B exists into the page. The bar starts to move from the vertex at time t = 0 with a constant velocity. If the induced EMF is E ∝ t^{n}, then value of n is ______.', None, 1,
    lambda: _vrail(), ['The length of bar between the rails grows as ℓ = 2vt tan θ.', 'E = Bℓv ∝ t → n = 1.'], 'motional', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'induct', 'A capacitor of capacitance 100 μF is charged to a potential of 12 V and connected to a 6.4 mH inductor to produce oscillations. The maximum current in the circuit would be :',
    ['3.2 A', '1.5 A', '2.0 A', '1.2 A'], 2, lambda: P4([3.2, 1.5, 2.0, 1.2], 12 * math.sqrt(100e-6 / 6.4e-3)), ['All the energy moves to the inductor: ½CV^{2} = ½LI^{2}.', 'I = V√{\\f{C}{L}} = 12 × √{\\f{10^{−4}}{6.4 × 10^{−3}}} = 12 × 0.125 = 1.5 A.'], 'induct', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'flux', 'A square loop of side 10 cm and resistance 0.7 Ω is placed vertically in east-west plane. A uniform magnetic field of 0.20 T is set up across the plane in north east direction. The magnetic field is decreased to zero in 1 s at a steady rate. Then, magnitude of induced emf is √{x} × 10^{−3} V. The value of x is', None, 2,
    lambda: round((0.01 * 0.2 * math.cos(pi / 4) / 1 / 1e-3) ** 2, 9), ['The loop\'s normal points north; the field (north-east) makes 45° with it.', 'Φ = BA cos 45° = 0.2 × 0.01 × \\f{1}{√{2}} = √{2} × 10^{−3} Wb, removed in 1 s.', 'ε = √{2} × 10^{−3} V → x = 2.'], 'flux', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'ac', 'In an a.c. circuit, voltage and current are given by : V = 100 sin(100t) V and I = 100 sin(100t + \\f{π}{3}) mA respectively. The average power dissipated in one cycle is :',
    ['5 W', '10 W', '2.5 W', '25 W'], 3, lambda: P4([5, 10, 2.5, 25], sum(100 * math.sin(100 * t) * 0.1 * math.sin(100 * t + pi / 3) for t in [2 * pi / 100 * (k + 0.5) / 20000 for k in range(20000)]) / 20000),
    ['P = \\f{V_{0}I_{0}}{2} cos φ.', '= \\f{100 × 0.1}{2} × cos 60° = 2.5 W.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'motional', 'A horizontal straight wire 5 m long extending from east to west falling freely at right angle to horizontal component of earth\'s magnetic field 0.60 × 10^{−4} Wb m^{−2}. The instantaneous value of emf induced in the wire when its velocity is 10 m s^{−1} is ______ × 10^{−3} V.', None, 3,
    lambda: round(abs(motional([(0, 0), (5, 0)], (0, -10), 0.6e-4)) / 1e-3, 9), ['Wire, velocity and field are mutually perpendicular.', 'ε = Bℓv = 0.6 × 10^{−4} × 5 × 10 = 3 × 10^{−3} V.'], 'motional', 1)
def _rot():
    N, A, B, w = 10, 0.2, 0.5, 30.0; phi = lambda t: N * B * A * math.cos(w * t)   # B parallel to the plane when ωt = π/2
    t = pi / 2 / w; return (round(phi(t) / N, 9), round(abs(ddt(phi, t, 1e-7)) / (N * A * B * w), 6))
add(('2025', 'Jan', '2025-01-29', 1), 'motional', 'A coil of area A and N turns is rotating with angular velocity ω in a uniform magnetic field B⃗ about an axis perpendicular to B⃗. Magnetic flux φ and induced emf ε across it, at an instant when B⃗ is parallel to the plane of coil, are :',
    ['φ = AB, ε = NABω', 'φ = 0, ε = NABω', 'φ = 0, ε = 0', 'φ = AB, ε = 0'], 2, lambda: pick([(1, 1), (0, 1), (0, 0), (1, 0)], _rot()),
    ['φ = BA cos ωt and ε = NBAω sin ωt, with ωt the angle between B and the coil\'s normal.', 'B in the plane means ωt = 90°: φ = 0 while ε is at its maximum NABω.'], 'motional', 1)
add(('2025', 'Jan', '2025-01-29', 1), 'ac', 'Assertion (A): Choke coil is simply a coil having a large inductance but a small resistance. Choke coils are used with fluorescent mercury-tube fittings. If household electric power is directly connected to a mercury tube, the tube will be damaged. Reason (R): By using the choke coil, the voltage across the tube is reduced by a factor (R/√{R^{2} + ω^{2}L^{2}}), where ω is frequency of the supply across resistor R and inductor L. If the choke coil were not used, the voltage across the resistor would be the same as the applied voltage.',
    ['(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)', '(A) is false but (R) is true'], 2,
    lambda: 2 if abs(abs(100 / Z(100, 1, w=314)) - 100 / math.hypot(100, 314)) < 1e-12 else 0,
    ['Choke: large L, tiny R, so it limits current while wasting almost no power — A is true.', 'In series with the tube (resistance R), the tube gets V·\\f{R}{√{R^{2} + ω^{2}L^{2}}}, which is why it is protected — R explains A.'], 'ac', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'induct', 'Consider I_{1} and I_{2} are the currents flowing simultaneously in two nearby coils 1 & 2, respectively. If L_{1} = self inductance of coil 1, M_{12} = mutual inductance of coil 1 with respect to coil 2, then the value of induced emf in coil 1 will be',
    ['ε_{1} = −L_{1}\\f{dI_{2}}{dt} − M_{12}\\f{dI_{1}}{dt}', 'ε_{1} = −L_{1}\\f{dI_{1}}{dt} + M_{12}\\f{dI_{2}}{dt}', 'ε_{1} = −L_{1}\\f{dI_{1}}{dt} − M_{12}\\f{dI_{1}}{dt}', 'ε_{1} = −L_{1}\\f{dI_{1}}{dt} − M_{12}\\f{dI_{2}}{dt}'], 4,
    lambda: (lambda L1, M, d1, d2: pick([-L1 * d2 - M * d1, -L1 * d1 + M * d2, -L1 * d1 - M * d1, -L1 * d1 - M * d2], -ddt(lambda t: L1 * (d1 * t) + M * (d2 * t), 0.3)))(2.0, 0.7, 3.0, 5.0),
    ['Flux through coil 1: Φ_{1} = L_{1}I_{1} + M_{12}I_{2}.', 'ε_{1} = −\\f{dΦ_{1}}{dt} = −L_{1}\\f{dI_{1}}{dt} − M_{12}\\f{dI_{2}}{dt}.'], 'induct', 1)

# ---------- sheets 12–13
add(('2026', 'Apr', '2026-04-04', 1), 'ac', 'An inductor of 10 mH, capacitor of 0.1 μF and a resistor of 100 Ω are connected in series across an a.c power supply 220 V. The power factor of the given circuit is 0.5. The difference in the inductive reactance and capacitance reactance is √{3}α Ω. The value of α is ______.', None, 100,
    lambda: round(100 * math.tan(math.acos(0.5)) / math.sqrt(3), 6), ['cos φ = \\f{R}{Z} = 0.5 → Z = 200 Ω.', '|X_{L} − X_{C}| = √{200^{2} − 100^{2}} = 100√{3} Ω → α = 100.'], 'ac', 1)
def _coax():
    # flux through C2 (at z = 0) from C1 at z = −d (anticlockwise, +z moment) and C3 at z = +d (clockwise, −z moment); positive = anticlockwise flux
    def phi(d1, d3): a = 1.0; f = lambda d: a ** 2 / (a * a + d * d) ** 1.5; return f(d1) - f(d3)
    cases = [(+1, +1), (-1, +1), (+1, -1), (-1, -1)]   # d(d1)/dt, d(d3)/dt for options 1–4 (+ = moving away)
    res = []
    for s1, s3 in cases:
        dphi = (phi(1 + s1 * 1e-5, 1 + s3 * 1e-5) - phi(1, 1)) / 1e-5; res.append('cw' if dphi > 1e-9 else ('acw' if dphi < -1e-9 else 'none'))
    return pick(res, 'cw')
add(('2026', 'Jan', '2026-01-22', 1), 'flux', 'Three identical coils C_{1}, C_{2} and C_{3} are closely placed such that they share a common axis. C_{2} is exactly midway. C_{1} carries current I in anti-clockwise direction while C_{3} carries current I in clockwise direction (both as seen from the same side). An induced current flows through C_{2} in clockwise direction when',
    ['C_{1} and C_{3} move with equal speeds away from C_{2}', 'C_{1} moves towards C_{2} and C_{3} moves away from C_{2}', 'C_{1} moves away from C_{2} and C_{3} moves towards C_{2}', 'C_{1} and C_{3} move with equal speeds towards C_{2}'], 2, lambda: _coax(),
    ['C_{1} sends "anticlockwise" flux through C_{2}, C_{3} sends "clockwise" flux; equal distances cancel.', 'A clockwise induced current opposes a growth of anticlockwise flux: C_{1} must come closer and/or C_{3} move away.', 'Moving both the same way keeps them balanced → no current.'], 'flux', 2)
add(('2024', 'Jan', '2024-01-30', 1), 'ac', 'Primary coil of a transformer is connected to 220 V ac. Primary and secondary turns of the transformer are 100 and 10 respectively. Secondary coil of transformer is connected to two series resistances 15 kΩ and 7 kΩ. The output voltage V_{0} across the 7 kΩ resistor is :',
    ['7 V', '15 V', '44 V', '22 V'], 1, lambda: P4([7, 15, 44, 22], 220 * 10 / 100 * 7 / 22), ['V_{s} = 220 × \\f{10}{100} = 22 V.', 'Divider: V_{0} = 22 × \\f{7}{15 + 7} = 7 V.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'ac', 'A series L, R circuit connected with an ac source E = (25 sin 1000t) V has a power factor of \\f{1}{√{2}}. If the source of emf is changed to E = (20 sin 2000t) V, the new power factor of the circuit will be :',
    ['\\f{1}{√{2}}', '\\f{1}{√{3}}', '\\f{1}{√{5}}', '\\f{1}{√{7}}'], 3, lambda: P4([1 / math.sqrt(k) for k in (2, 3, 5, 7)], math.cos(cmath.phase(Z(1.0, 1.0 / 1000, w=2000)))),
    ['At ω = 1000: cos φ = \\f{1}{√{2}} → X_{L} = R.', 'Doubling ω doubles X_{L} = 2R → cos φ = \\f{R}{√{R^{2} + 4R^{2}}} = \\f{1}{√{5}}.'], 'ac', 1)
def _fan():
    Bv = 0.5e-4 * math.sin(pi / 6); w = 1200 * 2 * pi / 60; L = 0.8; n = 100000
    e = sum(Bv * w * (L * (k + 0.5) / n) * L / n for k in range(n))   # ∫ B ω r dr
    return round(e / (pi * 1e-5), 4)
add(('2024', 'Jan', '2024-01-30', 1), 'motional', 'A ceiling fan having 3 blades of length 80 cm each is rotating with an angular velocity of 1200 rpm. The magnetic field of earth in that region is 0.5 G and angle of dip is 30°. The emf induced across the blades is Nπ × 10^{−5} V. The value of N is', None, 32,
    lambda: _fan(), ['A horizontal fan cuts only the vertical component: B_{V} = 0.5 sin 30° = 0.25 G = 2.5 × 10^{−5} T.', 'ω = 40π rad/s, ε = ½B_{V}ωℓ^{2} = ½ × 2.5 × 10^{−5} × 40π × 0.64 = 32π × 10^{−5} V (blades are in parallel, so the emf is the same).'], 'motional', 2)
def _half():
    f = lambda t: math.sin(100 * pi * t); t = 0.0
    while f(t) < 0.5: t += 1e-7
    t1 = t
    while f(t + 1e-7) > f(t): t += 1e-7
    return (t - t1) * 1000
add(('2024', 'Jan', '2024-01-30', 2), 'ac', 'An alternating voltage V(t) = 220 sin 100πt volt is applied to a purely resistive load of 50 Ω. The time taken for the current to rise from half of the peak value to the peak value is:',
    ['5 ms', '3.3 ms', '7.2 ms', '2.2 ms'], 2, lambda: P4([5, 3.3, 7.2, 2.2], _half(), 0.02), ['Current is in phase with voltage: i ∝ sin 100πt.', 'Half peak at 100πt = \\f{π}{6} (t = \\f{1}{600} s), peak at \\f{π}{2} (t = \\f{1}{200} s).', 'Δt = \\f{1}{300} s ≈ 3.3 ms.'], 'ac', 2)

# ---------- sheets 14–15
add(('2024', 'Jan', '2024-01-30', 2), 'ac', 'A power transmission line feeds input power at 2.3 kV to a step down transformer with its primary winding having 3000 turns. The output power is delivered at 230 V by the transformer. The current in the primary of the transformer is 5 A and its efficiency is 90%. The output current of transformer is ______ A.', None, 45,
    lambda: round(0.9 * 2300 * 5 / 230, 9), ['Input power = 2300 × 5 = 11 500 W; output = 0.9 × 11 500 = 10 350 W.', 'I_{s} = \\f{10 350}{230} = 45 A.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'flux', 'A coil is placed perpendicular to a magnetic field of 5000 T. When the field is changed to 3000 T in 2 s, an induced emf of 22 V is produced in the coil. If the diameter of the coil is 0.02 m, then the number of turns in the coil is :',
    ['7', '70', '35', '140'], 2, lambda: P4([7, 70, 35, 140], 22 / (pi * 0.01 ** 2 * 2000 / 2), 2e-3), ['ε = NA\\f{ΔB}{Δt} with A = π(0.01)^{2} and \\f{ΔB}{Δt} = 1000 T/s.', 'N = \\f{22}{π × 10^{−4} × 1000} ≈ 70.'], 'flux', 1)
def _sqsq():
    l = 0.05; L = l * l; h = L / 2; B = 4 * mu0 / (4 * pi * h) * 2 * math.sin(pi / 4)   # big loop, unit current, at its centre
    return round((B * l * l / 1e-7) ** 2, 6)
add(('2024', 'Jan', '2024-01-31', 1), 'induct', 'A small square loop of wire of side ℓ is placed inside a large square loop of wire of side L (L = ℓ^{2}). The loops are coplanar and their centres coincide. The value of the mutual inductance of the system is √{x} × 10^{−7} H, where x = ______.', None, 128,
    lambda: round(_sqsq()), ['Field at the centre of the big square (current I): B = 4 × \\f{μ_{0}I}{4π(L/2)} × 2 sin 45° = \\f{2√{2}μ_{0}I}{πL}.', 'M = \\f{Bℓ^{2}}{I} = \\f{2√{2}μ_{0}ℓ^{2}}{πL} = \\f{2√{2} × 4π × 10^{−7}}{π} = 8√{2} × 10^{−7} H (using L = ℓ^{2}).', 'x = 128.'], 'induct', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'ac', 'An AC voltage V = 20 sin 200πt is applied to a series LCR circuit which drives a current I = 10 sin(200πt + \\f{π}{3}). The average power dissipated is:',
    ['21.6 W', '200 W', '173.2 W', '50 W'], 4, lambda: P4([21.6, 200, 173.2, 50], sum(20 * math.sin(2 * pi * (k + 0.5) / 20000) * 10 * math.sin(2 * pi * (k + 0.5) / 20000 + pi / 3) for k in range(20000)) / 20000),
    ['P = \\f{V_{0}I_{0}}{2} cos φ with φ = 60°.', '= \\f{20 × 10}{2} × \\f{1}{2} = 50 W.'], 'ac', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'flux', 'The magnetic flux φ (in weber) linked with a closed circuit of resistance 8 Ω varies with time (in seconds) as φ = 5t^{2} − 36t + 1. The induced current in the circuit at t = 2 s is ______ A.', None, 2,
    lambda: round(abs(ddt(lambda t: 5 * t * t - 36 * t + 1, 2.0)) / 8, 6), ['ε = −\\f{dφ}{dt} = −(10t − 36) = 16 V at t = 2 s.', 'I = \\f{16}{8} = 2 A.'], 'flux', 1)
def _rotloop():
    B, w, e = 0.5, 100, 15.4e-3; pi7 = 22 / 7; th = pi / 6
    # Φ = BπR² cos ωt (flux maximum in the horizontal position); |dΦ/dt| at ωt = 30° = BπR²ω sin 30°
    R2 = e / (B * pi7 * w * math.sin(th)); return round(math.sqrt(R2) * 1000, 6)
add(('2026', 'Jan', '2026-01-22', 2), 'motional', 'A conducting circular loop is rotated about its diameter at a constant angular speed of 100 rad/s in a magnetic field of 0.5 T perpendicular to the axis of rotation (the field is perpendicular to the loop in its horizontal position). When the loop is rotated by 30° from the horizontal position, the induced EMF is 15.4 mV. The radius of the loop is ______ mm. (Take π = \\f{22}{7})', None, 14,
    lambda: round(_rotloop()), ['Φ = BπR^{2} cos ωt → ε = BπR^{2}ω sin ωt.', 'At 30°: 15.4 × 10^{−3} = 0.5 × \\f{22}{7} × R^{2} × 100 × ½ → R^{2} = 1.96 × 10^{−4} m^{2}.', 'R = 0.014 m = 14 mm.'], 'motional', 2)
def _dims():   # exponents (M, L, T, A)
    R = (1, 2, -3, -2); Lh = (1, 2, -2, -2); C = (-1, -2, 4, 2)
    add_ = lambda *xs: tuple(sum(c * x[i] for c, x in xs) for i in range(4))
    return pick([add_((1, R), (-0.5, Lh), (-0.5, C)), add_((1, R), (-1, Lh), (-1, C)), add_((1, C), (-0.5, Lh), (-0.5, R)), add_((-1, R), (0.5, Lh), (-0.5, C))], (1, 2, -4, -2))
add(('2026', 'Apr', '2026-04-05', 1), 'induct', 'L, C and R represent physical quantities inductance, capacitance and resistance respectively. The dimensional formula ML^{2}T^{−4}A^{−2} corresponds to ______.',
    ['\\f{R}{√{LC}}', '\\f{R}{LC}', '\\f{C}{√{LR}}', '\\f{1}{R}√{\\f{L}{C}}'], 1, lambda: _dims(),
    ['√{LC} has the dimension of time (ω = \\f{1}{√{LC}}).', 'R = ML^{2}T^{−3}A^{−2}, so \\f{R}{√{LC}} = ML^{2}T^{−4}A^{−2}.'], 'induct', 2)

# ---------- sheets 16–17
def _rc():
    X = 1.0
    lo, hi = 0.0, 10.0   # bisection on R/X: the ratio I(ω/4)/I(ω) rises from 1/4 towards 1 as R grows
    for _ in range(200):
        R = (lo + hi) / 2
        if abs(complex(R, -X)) / abs(complex(R, -4 * X)) < 1 / 3: lo = R
        else: hi = R
    return lo
add(('2026', 'Apr', '2026-04-05', 1), 'ac', 'An a.c. source of angular frequency ω is connected across a resistor R and a capacitor C in series. The current is observed as I. Now the frequency of the source is changed to ω/4, (keeping the voltage unchanged) the current is found to be I/3. The ratio of resistance to reactance at frequency ω is',
    ['√{\\f{6}{7}}', '√{\\f{3}{5}}', '√{\\f{7}{8}}', '√{\\f{3}{4}}'], 3, lambda: P4([math.sqrt(6 / 7), math.sqrt(3 / 5), math.sqrt(7 / 8), math.sqrt(3 / 4)], _rc(), 1e-4),
    ['At ω/4 the reactance becomes 4X.', 'Current falls to a third: R^{2} + 16X^{2} = 9(R^{2} + X^{2}) → 8R^{2} = 7X^{2}.', '\\f{R}{X} = √{\\f{7}{8}}.'], 'ac', 2)
def _L3():
    L, I = 1.0, 2.0
    Ut = 0.5 * L * I * I + 2 * 0.5 * L * (I / 2) ** 2   # equal inductors in parallel share the current equally
    return round(Ut / (0.5 * L * (I / 2) ** 2), 9)
add(('2026', 'Apr', '2026-04-05', 1), 'induct', 'In a circuit inductor L_{1} is in series with a parallel pair L_{2} and L_{3}; the inductance values of L_{1}, L_{2} and L_{3} are the same. The magnetic energy stored in the entire circuit is (U_{t}) and that stored in the L_{2} inductor is (U_{l}). \\f{U_{t}}{U_{l}} is ______. (Ignore the mutual inductance if any)', None, 6,
    lambda: _L3(), ['Equal parallel inductors share the current: \\f{I}{2} each.', 'U_{t} = ½LI^{2} + 2 × ½L\\f{I^{2}}{4} = \\f{3}{4}LI^{2}; U_{l} = \\f{1}{8}LI^{2}.', 'Ratio = 6.'], 'induct', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'motional', 'A 20 m long uniform copper wire held horizontally is allowed to fall under the gravity (g = 10 m/s^{2}) through a uniform horizontal magnetic field of 0.5 Gauss perpendicular to the length of the wire. The induced EMF across the wire when it travels a vertical distance of 200 m is ______ mV.',
    ['0.2√{10}', '20√{10}', '2√{10}', '200√{10}'], 2, lambda: P4([0.2, 20, 2, 200], abs(motional([(0, 0), (20, 0)], (0, -math.sqrt(2 * 10 * 200)), 0.5e-4)) / 1e-3 / math.sqrt(10)),
    ['v = √{2gh} = √{4000} = 20√{10} m/s.', 'ε = Bℓv = 0.5 × 10^{−4} × 20 × 20√{10} = 20√{10} mV.'], 'motional', 1)
def _pend():
    g, L, B = 10, 0.1, 2.0; v = math.sqrt(2 * g * L * (1 - math.cos(pi / 3))); w = v / L; n = 10000
    return round(sum(B * w * (L * (k + 0.5) / n) * L / n for k in range(n)) * 1000, 6)
add(('2026', 'Jan', '2026-01-23', 1), 'motional', 'A simple pendulum made of mass 10 g and a metallic wire of length 10 cm is suspended vertically in a uniform magnetic field of 2 T. The magnetic field direction is perpendicular to the plane of oscillations of the pendulum. If the pendulum is released from an angle of 60° with vertical, then maximum induced EMF between the point of suspension and point of oscillation is ______ mV (Take g = 10 m/s^{2})', None, 100,
    lambda: round(_pend()), ['Fastest at the bottom: v = √{2gL(1 − cos 60°)} = 1 m/s, so ω = \\f{v}{L} = 10 rad/s.', 'A rotating wire: ε = ½BωL^{2} = ½ × 2 × 10 × 0.01 = 0.1 V = 100 mV.'], 'motional', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'ac', 'Using a variable frequency a.c. voltage source the maximum current measured in a series LCR circuit (L = 2 H, R = 100 Ω) is 50 mA for V = 5 sin(100t). The capacitance of the capacitor (C) used is ______ μF.', None, 50,
    lambda: round(next(c for c in [k * 1e-6 for k in range(1, 1000)] if abs(abs(5 / Z(100, 2, c, 100)) - 0.05) < 1e-12) * 1e6), ['5 V / 100 Ω = 50 mA means Z = R: the circuit is at resonance at ω = 100 rad/s.', 'C = \\f{1}{ω^{2}L} = \\f{1}{10^{4} × 2} = 50 μF.'], 'ac', 2)
def _rod():
    B0, w, lam, L = 1.0, 1.0, 2.0, 0.7; n = 200000
    e = sum(B0 * math.exp(-lam * r) * w * r * L / n for r in [L * (k + 0.5) / n for k in range(n)])
    f = [B0 * w * (1 / lam ** 2 - math.exp(-lam * L) * (1 / lam ** 2 + L / lam)), B0 * w * (1 / lam ** 2 + math.exp(-lam * L) * (1 / lam ** 2 + L / lam)),
         B0 * w * (4 / lam ** 2 - math.exp(-2 * lam * L) * (1 / lam ** 2 + 2 * L / lam)), B0 * w * (3 / lam ** 2 - math.exp(-3 * lam * L) * (3 / lam ** 2 + L / lam))]
    return P4(f, e, 1e-6)
add(('2026', 'Apr', '2026-04-05', 2), 'motional', 'A metal rod of length L rotates about one end at origin with a uniform angular velocity ω. The magnetic field radially falls off as B(r) = B_{0}e^{−λr}; λ being a positive constant. The emf induced (neglecting the centripetal force on electrons in the rod) is :',
    ['B_{0}ω[\\f{1}{λ^{2}} − e^{−λL}(\\f{1}{λ^{2}} + \\f{L}{λ})]', 'B_{0}ω[\\f{1}{λ^{2}} + e^{−λL}(\\f{1}{λ^{2}} + \\f{L}{λ})]', 'B_{0}ω[\\f{4}{λ^{2}} − e^{−2λL}(\\f{1}{λ^{2}} + \\f{2L}{λ})]', 'B_{0}ω[\\f{3}{λ^{2}} − e^{−3λL}(\\f{3}{λ^{2}} + \\f{L}{λ})]'], 1, lambda: _rod(),
    ['A slice dr at r moves at ωr: dε = B(r)ωr dr.', 'ε = B_{0}ω∫_{0}^{L} re^{−λr} dr = B_{0}ω[\\f{1}{λ^{2}} − e^{−λL}(\\f{1}{λ^{2}} + \\f{L}{λ})] (integration by parts).'], 'motional', 3)
add(('2026', 'Apr', '2026-04-05', 2), 'ac', 'A series LCR circuit with R = 20 Ω, L = 1.6 H and C = 40 μF is connected to a variable frequency a.c. source. The inductive reactance at resonant frequency is ______ Ω.', None, 200,
    lambda: round(1.6 / math.sqrt(1.6 * 40e-6), 6), ['ω_{0} = \\f{1}{√{LC}} = \\f{1}{√{64 × 10^{−6}}} = 125 rad/s.', 'X_{L} = ω_{0}L = 125 × 1.6 = 200 Ω.'], 'ac', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'flux', 'A circular loop of radius 20 cm and resistance 2 Ω is placed in a time varying magnetic field B⃗ = (2t^{2} + 2t + 3) T, with the plane of the loop perpendicular to the field. The induced current in the loop at t = 3 s is \\f{α}{50} A. The value of α is ______. (Take π = 22/7)', None, 44,
    lambda: round(ddt(lambda t: (2 * t * t + 2 * t + 3) * 22 / 7 * 0.04, 3.0) / 2 * 50, 6), ['\\f{dB}{dt} = 4t + 2 = 14 T/s at t = 3 s.', 'ε = πr^{2}\\f{dB}{dt} = \\f{22}{7} × 0.04 × 14 = 1.76 V, I = 0.88 A = \\f{44}{50} A.'], 'flux', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'flux', 'A circular loop of radius 7 cm is placed in uniform magnetic field of 0.2 T directed perpendicular to plane of loop. The loop is converted into a square loop in 0.5 s. The EMF induced in the loop is ______ mV.',
    ['6.6', '13.2', '8.25', '1.32'], 4, lambda: P4([6.6, 13.2, 8.25, 1.32], 0.2 * (22 / 7 * 49 - (2 * 22 / 7 * 7 / 4) ** 2) * 1e-4 / 0.5 * 1000, 2e-3),
    ['Same wire: perimeter 2π × 7 = 44 cm → square of side 11 cm.', 'Area falls from 154 cm^{2} to 121 cm^{2}: ΔA = 33 cm^{2}.', 'ε = \\f{BΔA}{Δt} = \\f{0.2 × 33 × 10^{−4}}{0.5} = 1.32 mV.'], 'flux', 2)

# ---------- sheets 18–19
def _sol_loop():
    n, I0, w, r, R = 500, 10, 1000, 0.01, 10   # 500 turns per metre
    phi = lambda t: mu0 * n * I0 * math.sin(w * t) * pi * r * r   # flux through B (field inside the solenoid, uniform)
    T = 2 * pi / w; i = lambda t: -ddt(phi, t, 1e-8) / R
    return round(rms(i, T, 4000) * math.sqrt(2) / 1e-6, 2)
add(('2026', 'Jan', '2026-01-23', 2), 'flux', 'Suppose a long solenoid of 100 cm length, radius 2 cm having 500 turns per unit length, carries a current I = 10 sin(ωt) A, where ω = 1000 rad/s. A circular conducting loop (B) of radius 1 cm coaxially slided through the solenoid at a speed v = 1 cm/s. The r.m.s. current through the loop when the coil B is inserted 10 cm inside the solenoid is α/√{2} μA. The value of α is ______. [Resistance of the loop = 10 Ω]',
    ['197', '80', '280', '100'], 1, lambda: P4([197, 80, 280, 100], _sol_loop(), 3e-3),
    ['Deep inside, B = μ_{0}nI is uniform, so the loop\'s position (and its slow speed) does not matter.', 'Φ = μ_{0}nπr^{2}I, ε_{0} = μ_{0}nπr^{2}I_{0}ω = 4π × 10^{−7} × 500 × π × 10^{−4} × 10 × 1000 ≈ 1.97 × 10^{−3} V.', 'Peak current \\f{ε_{0}}{10 Ω} = 197 μA → rms = \\f{197}{√{2}} μA.'], 'flux', 3)
def _lr():
    L, R, E = 10e-3, 100, 1.0; i, dt, t, out = 0.0, 1e-8, 0.0, {}
    while i < 4.2e-3:
        vL = E - i * R
        for k in (2e-3, 4e-3):
            if k not in out and i >= k: out[k] = vL
        i += vL / L * dt
    return out[2e-3] / out[4e-3]
add(('2026', 'Apr', '2026-04-06', 1), 'induct', 'An inductor of inductance 10 mH having resistance of 100 Ω is connected to battery of E.M.F. 1.0 V through a switch. After switch is closed, the ratio of instantaneous voltages across the inductor when the current passing through it is 2 mA and 4 mA is ______.',
    ['4/3', '3/4', '5/3', '3/5'], 1, lambda: P4([4 / 3, 3 / 4, 5 / 3, 3 / 5], _lr(), 2e-3), ['The emf across the pure inductance is E − iR.', 'At 2 mA: 1 − 0.2 = 0.8 V; at 4 mA: 1 − 0.4 = 0.6 V.', 'Ratio = \\f{4}{3}.'], 'induct', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'ac', 'A LCR series circuit driven with E_{rms} = 90 V at frequency f_{d} = 30 Hz has resistance R = 80 Ω, an inductance with inductive reactance X_{L} = 20.0 Ω and capacitance with capacitive reactance X_{C} = 80.0 Ω. The power factor of the circuit is ____.',
    ['0.8', '0.64', '0.9', '0.5'], 1, lambda: P4([0.8, 0.64, 0.9, 0.5], math.cos(cmath.phase(complex(80, 20 - 80)))), ['Z = √{80^{2} + (20 − 80)^{2}} = 100 Ω.', 'cos φ = \\f{R}{Z} = 0.8.'], 'ac', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'ac', 'For the series LCR circuit connected with 220 V, 50 Hz a.c source (X_{L} = 70 Ω, X_{C} = 150 Ω, R = 60 Ω), the power factor is \\f{α}{10}. The value of α is ____ .',
    ['4', '10', '6', '8'], 3, lambda: P4([4, 10, 6, 8], 10 * math.cos(cmath.phase(complex(60, 70 - 150)))), ['Z = √{60^{2} + 80^{2}} = 100 Ω.', 'cos φ = \\f{60}{100} = \\f{6}{10} → α = 6.'], 'ac', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'flux', 'A square loop of side 2 cm is placed in a time varying magnetic field with magnitude as B = 0.4 sin(300t) Tesla. The normal to the plane of loop makes an angle of 60° with the field. The maximum induced emf produced in the loop is ______ mV.',
    ['12', '18', '21', '24'], 4, lambda: P4([12, 18, 21, 24], max(abs(ddt(lambda t: 4e-4 * 0.4 * math.sin(300 * t) * math.cos(pi / 3), k * 1e-5)) for k in range(2200)) * 1000, 1e-3),
    ['Φ = BA cos 60° = 0.4 sin 300t × 4 × 10^{−4} × ½.', 'ε_{max} = 0.4 × 300 × 4 × 10^{−4} × ½ = 0.024 V = 24 mV.'], 'flux', 1)
add(('2026', 'Apr', '2026-04-08', 2), 'induct', 'A 30 cm long solenoid has 10 turns per cm and area of 5 cm^{2}. The current through the solenoid coil varies from 2 A to 4 A in 3.14 s. The e.m.f. induced in the coil is α × 10^{−5} V. The value of α is ______.',
    ['60', '12', '120', '34'], 2, lambda: P4([60, 12, 120, 34], mu0 * 1000 ** 2 * 5e-4 * 0.3 * (2 / 3.14) / 1e-5, 2e-3),
    ['L = μ_{0}n^{2}Aℓ = 4π × 10^{−7} × 10^{6} × 5 × 10^{−4} × 0.3 ≈ 1.88 × 10^{−4} H.', 'ε = L\\f{ΔI}{Δt} = 1.88 × 10^{−4} × \\f{2}{3.14} = 12 × 10^{−5} V.'], 'induct', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'ac', 'The electric current in the circuit is given as i = i_{0}(t/T). The r.m.s current for the period t = 0 to t = T is ______ .',
    ['\\f{i_{0}}{√{2}}', 'i_{0}', '\\f{i_{0}}{√{6}}', '\\f{i_{0}}{√{3}}'], 4, lambda: P4([1 / math.sqrt(2), 1, 1 / math.sqrt(6), 1 / math.sqrt(3)], rms(lambda t: t, 1.0, 100000), 1e-4),
    ['I_{rms}^{2} = \\f{1}{T}∫_{0}^{T} i_{0}^{2}\\f{t^{2}}{T^{2}} dt = \\f{i_{0}^{2}}{3}.', 'I_{rms} = \\f{i_{0}}{√{3}}.'], 'ac', 1)

# ---------- induction items found while building Unit 13
def _grad():
    a, b, v, R = 0.12, 0.05, 0.05, 6e-3
    B = lambda x, t: 1.0 - 0.1 * x - 1e-3 * t   # T: falls by 10⁻³ T per cm going +x, and by 10⁻³ T each second
    def phi(t, n=2000):
        x0 = v * t; return sum(B(x0 + a * (k + 0.5) / n, t) * b * a / n for k in range(n))
    e = ddt(phi, 1.0, 1e-3); return round(e * e / R / 1e-9, 6)
add(('2024', 'Feb', '2024-02-01', 1), 'flux', 'A rectangular loop of sides 12 cm and 5 cm, with its sides parallel to the x-axis and y-axis respectively moves with a velocity of 5 cm/s in the positive x axis direction, in a space containing a variable magnetic field in the positive z direction. The field has a gradient of 10^{−3} T/cm along the negative x direction and it is decreasing with time at the rate of 10^{−3} T/s. If the resistance of the loop is 6 mΩ, the power dissipated by the loop as heat is ______ × 10^{−9} W.', None, 216,
    lambda: round(_grad()), ['Moving into weaker field and the field also falling: both reduce the flux.', '\\f{dΦ}{dt} = A(\\f{∂B}{∂t} + v\\f{∂B}{∂x}) = 60 × 10^{−4}(−10^{−3} − 0.05 × 0.1) = −3.6 × 10^{−5} V.', 'P = \\f{ε^{2}}{R} = \\f{1.296 × 10^{−9}}{6 × 10^{−3}} = 216 × 10^{−9} W.'], 'flux', 3)
add(('2024', 'Feb', '2024-02-01', 2), 'motional', 'A coil of 200 turns and area 0.20 m^{2} is rotated at half a revolution per second and is placed in uniform magnetic field of 0.01 T perpendicular to axis of rotation of the coil. The maximum voltage generated in the coil is \\f{2π}{β} volt. The value of β is', None, 5,
    lambda: round(2 * pi / max(abs(ddt(lambda t: 200 * 0.01 * 0.2 * math.cos(pi * t), k * 1e-3)) for k in range(2000)), 4), ['ω = 2π × ½ = π rad/s.', 'ε_{max} = NBAω = 200 × 0.01 × 0.2 × π = \\f{2π}{5} V → β = 5.'], 'motional', 1)
def _bisect_rod():
    B, w, L = 0.5, 20, 0.6; n = 10000; half = lambda: sum(B * w * (L / 2 * (k + 0.5) / n) * L / 2 / n for k in range(n))
    return round(half() - half(), 12)   # each end is at the same potential relative to the centre
add(('2024', 'Apr', '2024-04-04', 2), 'motional', 'A rod of length 60 cm rotates with a uniform angular velocity 20 rad s^{−1} about its perpendicular bisector, in a uniform magnetic field 0.5 T. The direction of magnetic field is parallel to the axis of rotation. The potential difference between the two ends of the rod is ____ V.', None, 0,
    lambda: round(_bisect_rod()), ['Each half develops ½Bω(\\f{L}{2})^{2} between the centre and its end, in the same sense.', 'So both ends sit at the same potential: the difference is 0.'], 'motional', 1)
def _coil2():
    ratio = lambda N, A, r: (N * A) ** 2 / (N * math.sqrt(A) / (r * r))   # P = ε²/R, ε ∝ NA, R ∝ N √A / r²
    return round(ratio(2, 2, 3) / ratio(1, 1, 1) / math.sqrt(2), 6)
add(('2026', 'Apr', '2026-04-02', 1), 'flux', 'When a coil is placed in a time dependent magnetic field the power dissipated in it is P. The number of turns, area of the coil and radius of the coil wire are N, A and r respectively. For a second coil, number of turns, area of the coil and radius of the coil wire are 2N, 2A and 3r respectively. When the first coil is replaced with the second coil the power dissipated in it is √{2}αP. The value of α is ______ .',
    ['36', '128√{2}', '16', '64'], 1, lambda: P4([36, 128 * math.sqrt(2), 16, 64], _coil2()),
    ['ε ∝ NA: it becomes 4 times.', 'R ∝ \\f{(wire length)}{r^{2}} ∝ \\f{N√{A}}{r^{2}}: it becomes \\f{2√{2}}{9} times.', 'P = \\f{ε^{2}}{R} → 16 × \\f{9}{2√{2}} = 36√{2} → α = 36.'], 'flux', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'flux', 'A conducting circular loop of area 1.0 m^{2} is placed perpendicular to a magnetic field which varies as B = sin(100t) Tesla. If the resistance of the loop is 100 Ω, then the average thermal energy dissipated in the loop in one period is ____ J.',
    ['\\f{π}{2}', '2π', 'π', 'π^{2}'], 3, lambda: P4([pi / 2, 2 * pi, pi, pi * pi], sum(ddt(lambda t: math.sin(100 * t), 2 * pi / 100 * (k + 0.5) / 4000, 1e-7) ** 2 / 100 * 2 * pi / 100 / 4000 for k in range(4000)), 1e-4),
    ['ε = A\\f{dB}{dt} = 100 cos 100t V.', 'Mean power = \\f{100^{2}}{2 × 100} = 50 W; period T = \\f{2π}{100} s.', 'Energy = 50 × \\f{2π}{100} = π J.'], 'flux', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'motional', 'A 1 m long metal rod AB completes a circuit with a 2 Ω resistor through rails. The area of circuit is perpendicular to the magnetic field of 0.10 T. If the resistance of the total circuit is 2 Ω then the force needed to move the rod towards right with constant speed (v) of 1.5 m/s is ______ N.',
    ['7.5 × 10^{−2}', '5.7 × 10^{−3}', '5.7 × 10^{−2}', '7.5 × 10^{−3}'], 4, lambda: P4([7.5e-2, 5.7e-3, 5.7e-2, 7.5e-3], 0.1 * (abs(motional([(0, 0), (0, 1)], (1.5, 0), 0.1)) / 2) * 1),
    ['ε = Bℓv = 0.1 × 1 × 1.5 = 0.15 V, I = \\f{0.15}{2} = 0.075 A.', 'Constant speed: applied force = BIℓ = 0.1 × 0.075 × 1 = 7.5 × 10^{−3} N.'], 'motional', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'motional', 'A uniform magnetic field of 0.4 T acts perpendicular to a circular copper disc 20 cm in radius. The disc is having a uniform angular velocity of 10π rad s^{−1} about an axis through its centre and perpendicular to the disc. What is the potential difference developed between the axis of the disc and the rim? (π = 3.14)',
    ['0.1256 V', '0.2512 V', '0.0628 V', '0.5024 V'], 2, lambda: P4([0.1256, 0.2512, 0.0628, 0.5024], 0.5 * 0.4 * 10 * 3.14 * 0.2 ** 2), ['Any radius acts like a rod spinning about one end.', 'V = ½Bωr^{2} = ½ × 0.4 × 31.4 × 0.04 = 0.2512 V.'], 'motional', 1)
def _term():
    m, g, R, B, l = 0.1, 10, 2.0, 0.5, 0.4; v, dt = 0.0, 1e-3
    for _ in range(400000): v += (g - B * B * l * l * v / (m * R)) * dt
    return v / (m * g * R / (B * B * l * l))
add(('2026', 'Jan', '2026-01-22', 1), 'motional', 'XPQY is a vertical smooth long loop having a total resistance R where PX is parallel to QY and separation between them is l. A constant magnetic field B perpendicular to the plane of the loop exists in the entire space. A rod CD of length L (L > l) and mass m is made to slide down from rest under the gravity. The terminal speed acquired by the rod is ____ m/s. (g = acceleration due to gravity)',
    ['\\f{2mgR}{B^{2}l^{2}}', '\\f{8mgR}{B^{2}l^{2}}', '\\f{2mgR}{B^{2}L^{2}}', '\\f{mgR}{B^{2}l^{2}}'], 4, lambda: P4([2, 8, 2 * (0.4 / 0.6) ** 2, 1], _term(), 1e-3),
    ['Only the part between the rails (length l) is in the circuit: ε = Blv, I = \\f{Blv}{R}.', 'Terminal speed when BIl = mg: \\f{B^{2}l^{2}v}{R} = mg → v = \\f{mgR}{B^{2}l^{2}}.'], 'motional', 2)
for _p in P: _p["t"] = _p["fam"]
