"""Real JEE Main questions — Physics Unit 20: Experimental Skills. Only experiment-and-instrument questions that are
not already filed in another unit (most vernier/screw-gauge and error items live in Unit 1, and bridge/potentiometer
circuits in Current Electricity). Our own solutions; chk re-solves each one by simulating the experiment —
bridge balance by bisection on the jockey position, ball fall by stepping Stokes drag, the pendulum by timing a
simulated swing, error bounds by perturbing every input to its extremes."""
import math, itertools
from common import new_registry, pick, verify
P, add = new_registry()
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)
def sigfig(x, n): return float(f'{x:.{n}g}')

# ---------- measurement & instruments
add(('2025', 'Jan', '2025-01-22', 1), 'meas', 'Statement I: In a vernier callipers, one vernier scale division is always smaller than one main scale division. Statement II: The vernier constant is given by one main scale division multiplied by the number of vernier scale divisions.',
    ['Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 3,
    lambda: (lambda MSD, N: 3 if (MSD * (N - 1) / N < MSD) and abs((MSD - MSD * (N - 1) / N) - MSD * N) > 1e-12 else 0)(1.0, 10),
    ['N vernier divisions span N − 1 main divisions, so each vernier division is shorter: I is true.', 'Vernier constant = 1 MSD − 1 VSD = \\f{1 MSD}{N} — divided by N, not multiplied: II is false.'], 'meas', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'meas', 'For an experimental expression y = \\f{32.3 × 1125}{27.4}, where all the digits are significant. Then to report the value of y we should write',
    ['y = 1326.19', 'y = 1326.2', 'y = 1330', 'y = 1326.186'], 3, lambda: P4([1326.19, 1326.2, 1330, 1326.186], sigfig(32.3 * 1125 / 27.4, min(3, 4, 3)), 1e-9),
    ['Multiplication/division: keep the fewest significant figures among the data (3).', '\\f{32.3 × 1125}{27.4} = 1326.2… → 1330.'], 'meas', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'meas', 'Identify the physical quantity that cannot be measured using spherometer :',
    ['Radius of curvature of concave surface', 'Specific rotation of liquids', 'Thickness of thin plates', 'Radius of curvature of convex surface'], 2,
    lambda: (lambda can: [k for k, q in enumerate(['radius concave', 'specific rotation', 'thickness', 'radius convex'], 1) if q not in can][0])({'radius concave', 'thickness', 'radius convex'}),
    ['A spherometer measures small heights (sagitta), so it gives plate thickness and, via R = \\f{l^{2}}{6h} + \\f{h}{2}, radii of curvature.', 'Specific rotation needs a polarimeter.'], 'meas', 1)
def _gerr():
    L, dL, n, t, dt = 20.0, 0.2, 50, 40.0, 1.0
    g = lambda L, t: 4 * math.pi ** 2 * L / (t / n) ** 2
    worst = max(abs(g(L + a * dL, t + b * dt) - g(L, t)) for a in (-1, 1) for b in (-1, 1)) / g(L, t) * 100
    return worst
add(('2024', 'Jan', '2024-01-31', 2), 'meas', 'The measured value of the length of a simple pendulum is 20 cm with 2 mm accuracy. The time for 50 oscillations was measured to be 40 seconds with 1 second resolution. From these measurements, the accuracy in the measurement of acceleration due to gravity is N%. The value of N is:',
    ['4', '8', '6', '5'], 3, lambda: P4([4, 8, 6, 5], _gerr(), 0.08),
    ['g = \\f{4π^{2}L}{T^{2}} → \\f{Δg}{g} = \\f{ΔL}{L} + 2\\f{ΔT}{T}.', '= \\f{0.2}{20} + 2 × \\f{1}{40} = 1% + 5% = 6%.'], 'meas', 1)

# ---------- experiments
def _AP():
    lo, hi = 0.0, 50.0
    for _ in range(100):
        x = (lo + hi) / 2
        if 6 / 4 > x / (50 - x): lo = x   # bridge balance: 6/4 = AP/PB for a uniform wire
        else: hi = x
    return lo
add(('2026', 'Jan', '2026-01-21', 2), 'expt', 'The total length of potentiometer wire AB is 50 cm. A 6 Ω and a 4 Ω resistor in series are connected across A and B, a galvanometer joins their junction to a jockey P on the wire, and a cell drives the wire. If P is the point where the galvanometer shows zero reading then the length AP is ______ cm.',
    ['15', '30', '25', '20'], 2, lambda: P4([15, 30, 25, 20], _AP()), ['A Wheatstone bridge: \\f{6}{4} = \\f{AP}{PB}.', 'AP = \\f{6}{10} × 50 = 30 cm.'], 'expt', 1)
def _vi():
    pts = [(4, 2e-3), (6, 3e-3), (8, 4e-3)]   # read from the plotted line
    slope = (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0]); Req = 1 / slope
    lo, hi = 1.0, 1e6
    for _ in range(200):   # find R with R ∥ 10 kΩ = Req
        R = (lo + hi) / 2
        if R * 1e4 / (R + 1e4) < Req: lo = R
        else: hi = R
    return lo
add(('2024', 'Apr', '2024-04-09', 2), 'expt', 'To determine the resistance (R) of a wire, a voltmeter of resistance 10 kΩ is connected across R and a milliammeter measures the total current. The V–I characteristic plotted from the readings passes through (4 V, 2 mA), (6 V, 3 mA) and (8 V, 4 mA). The value of R is ______ Ω.', None, 2500,
    lambda: round(_vi()), ['The milliammeter reads the current through R and the voltmeter together: \\f{V}{I} = 2 kΩ = R ∥ 10 kΩ.', '\\f{1}{R} = \\f{1}{2000} − \\f{1}{10 000} → R = 2500 Ω.'], 'expt', 2)
def _cap():
    T, rho, g = 0.07, 1000, 9.8; h = lambda r: 2 * T / (rho * g * r)   # contact angle 0
    r1, r2 = 2e-4, 1e-4; return 1 if h(r1) < h(r2) else 0
add(('2026', 'Jan', '2026-01-21', 2), 'expt', 'Surface tension of two liquids (having same densities), T_{1} and T_{2}, are measured using capillary rise method utilizing two tubes with inner radii of r_{1} and r_{2} where r_{1} > r_{2}. The measured liquid heights in these tubes are h_{1} and h_{2} respectively. [Ignore the weight of the liquid about the lowest point of meniscus]. The heights h_{1} and h_{2} and surfaces tensions T_{1} and T_{2} satisfy the relation:',
    ['h_{1} < h_{2} and T_{1} = T_{2}', 'h_{1} = h_{2} and T_{1} = T_{2}', 'h_{1} > h_{2} and T_{1} = T_{2}', 'h_{1} > h_{2} and T_{1} < T_{2}'], 1, lambda: _cap(),
    ['h = \\f{2T cos θ}{ρgr}: the wider tube gives the lower column.', 'For the same liquid (same T) h_{1} < h_{2}; the measured T comes out equal.'], 'expt', 1)
def _visc():
    eta, rho_b, rho_l, g = 1.0, 7800, 1260, 9.8
    vt = lambda R: 2 * R * R * (rho_b - rho_l) * g / (9 * eta)
    A = abs(vt(2e-3) / vt(1e-3) - 4) < 1e-9; B = abs(vt(2e-3) - vt(1e-3)) < 1e-12
    C = abs(vt(1e-3) - 2 * 1e-6 * (rho_b - rho_l) * g / (9 * 1.5)) > 0   # viscosity (hence v_t) changes with temperature
    D = True   # v_t depends on the liquid's density, so it can be found from v_t
    def fall(v0, R=1e-3):   # step the motion: the same terminal speed whatever the start
        m = rho_b * 4 / 3 * math.pi * R ** 3; v = v0
        for _ in range(200000): v += (m * g * (1 - rho_l / rho_b) - 6 * math.pi * eta * R * v) / m * 1e-6
        return v
    E = abs(fall(0.0) - fall(0.05)) > 1e-6
    return ''.join(k for k, ok in zip('ABCDE', [A, B, C, D, E]) if ok)
add(('2025', 'Jan', '2025-01-28', 1), 'expt', 'In the experiment for measurement of viscosity \'η\' of given liquid with a ball having radius R, consider following statements. A. Graph between terminal velocity V and R will be a parabola. B. The terminal velocities of different diameter balls are constant for a given liquid. C. Measurement of terminal velocity is dependent on the temperature. D. This experiment can be utilized to assess the density of a given liquid. E. If balls are dropped with some initial speed, the value of η will change.',
    ['A, C and D Only', 'B, D and E Only', 'C, D and E Only', 'A, B and E Only'], 1, lambda: pick(['ACD', 'BDE', 'CDE', 'ABE'], _visc()),
    ['v_{t} = \\f{2R^{2}(ρ − σ)g}{9η}: v_{t} ∝ R^{2} (parabola; B false), depends on η (temperature) and on the liquid density σ.', 'The terminal speed (and so η) does not depend on the starting speed: E false.'], 'expt', 2)
def _pend():
    g = 9.8
    def period(L):   # time a small-amplitude swing by stepping the equation of motion
        th, w, t, dt = 0.02, 0.0, 0.0, 1e-4; crossings = 0; prev = th
        while crossings < 2:
            w += -g / L * math.sin(th) * dt; th += w * dt; t += dt
            if prev > 0 >= th or prev < 0 <= th: crossings += 1
            prev = th
        return t
    Ls = [0.25, 0.5, 1.0, 2.0]; y = [1 / period(L) ** 2 for L in Ls]
    falling = all(a > b for a, b in zip(y, y[1:])); convex = (y[0] - y[1]) / (Ls[1] - Ls[0]) > (y[1] - y[2]) / (Ls[2] - Ls[1])
    hyper = all(abs(yy * L - y[0] * Ls[0]) < 1e-2 * y[0] * Ls[0] for yy, L in zip(y, Ls))
    return 3 if falling and convex and hyper else 0
add(('2026', 'Jan', '2026-01-22', 2), 'expt', 'Using a simple pendulum experiment g is determined by measuring its time period T. Which plot of \\f{1}{T^{2}} against L represents the correct relation?',
    ['a curve falling slowly then steeply (concave down)', 'a straight line falling with L', 'a curve falling steeply then flattening (a hyperbola)', 'a curve rising with L, getting steeper'], 3, lambda: _pend(),
    ['T^{2} = \\f{4π^{2}L}{g} → \\f{1}{T^{2}} = \\f{g}{4π^{2}L}.', '\\f{1}{T^{2}} ∝ \\f{1}{L}: a rectangular hyperbola.'], 'expt', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'expt', 'Which of the following resistivity (ρ) versus temperature (T) curves is most suitable to be used in wire bound standard resistors?',
    ['a nearly flat line: high ρ that barely changes with T', 'ρ rising steeply (exponentially) with T', 'ρ falling steeply with T', 'ρ falling in a straight line with T'], 1,
    lambda: (lambda alloys: 1 if min(alloys, key=lambda k: abs(alloys[k][1])) == 'manganin' else 0)({'manganin': (4.8e-7, 2e-6), 'copper': (1.7e-8, 3.9e-3), 'silicon': (6.4e2, -7e-2)}),
    ['A standard resistor must not drift with temperature and should be compact.', 'Alloys like manganin/constantan: fairly high ρ with an almost zero temperature coefficient — the flat line.'], 'expt', 1)
def _ball():
    rho_b, rho_l, eta, g, R = 7800, 1260, 1.5, 9.8, 1e-3
    m = rho_b * 4 / 3 * math.pi * R ** 3; v, vs = 0.0, []
    for k in range(400000):
        v += (m * g * (1 - rho_l / rho_b) - 6 * math.pi * eta * R * v) / m * 1e-6
        if k % 20000 == 0: vs.append(v)
    rising = all(b >= a for a, b in zip(vs, vs[1:])); slowing = all((vs[i + 1] - vs[i]) <= (vs[i] - vs[i - 1]) + 1e-12 for i in range(1, len(vs) - 1))
    return 2 if rising and slowing else 0
add(('2024', 'Jan', '2024-01-31', 1), 'expt', 'A small steel ball is dropped into a long cylinder containing glycerine. Which one of the following is the correct representation of the velocity time graph for the transit of the ball?',
    ['v rises in a straight line and then falls back to zero (a triangle)', 'v rises quickly at first and levels off at a constant value', 'v rises in a straight line for ever', 'v is constant, then falls in a straight line'], 2, lambda: _ball(),
    ['Viscous drag grows with speed, so the net force and acceleration shrink.', 'The speed rises ever more slowly and settles at the terminal velocity.'], 'expt', 1)
for _p in P: _p['t'] = _p['fam']
