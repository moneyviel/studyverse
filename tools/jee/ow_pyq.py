"""Real JEE Main questions — Physics Unit 10: Oscillations and Waves. Our own solutions; chk re-solves each one — SHM by
stepping x'' = −ω²x in time, superposition by adding phasors as complex numbers, waves from the phase k x − ω t
written out afresh, pipes and strings by listing their allowed harmonics. Skipped: an item whose options are cut in
the scan, a pressure-gauge (Bernoulli) item and a two-wire elasticity item that belong to Unit 7, a car-turning
pendulum item (Unit 3) and pendulum-at-height items already used in Gravitation."""
import math, cmath
from common import new_registry, pick, near, verify
P, add = new_registry()
G = 10.0
def shm(w, x0, v0, T, dt=1e-4):   # integrate x'' = −w²x (velocity Verlet)
    x, v, t = x0, v0, 0.0
    while t < T - 1e-12:
        a = -w * w * x; x += v * dt + 0.5 * a * dt * dt; v += 0.5 * (a - w * w * x) * dt; t += dt
    return x, v
def first_time(w, A, target, dt=1e-5):   # start at x = A (rest), time to first reach |x| ≤ target
    x, v, t = A, 0.0, 0.0
    while x > target:
        a = -w * w * x; x += v * dt + 0.5 * a * dt * dt; v += 0.5 * (a - w * w * x) * dt; t += dt
    return t
def bisect(f, lo, hi, n=200):
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(lo) > 0) == (f(m) > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
closed = lambda n, v, L: (2 * n - 1) * v / (4 * L)   # n-th allowed mode (odd harmonics only)
open_ = lambda n, v, L: n * v / (2 * L)

# ---------------- SHM: displacement, velocity, energy ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'shm', 'A particle is subjected to two simple harmonic motions as : x_{1} = √{7} sin 5t cm and x_{2} = 2√{7} sin(5t + \\f{π}{3}) cm where x is displacement and t is time in seconds. The maximum acceleration of the particle is x × 10^{−2} m s^{−2}. The value of x is :', ['5√{7}', '25√{7}', '175', '125'], 3,
    lambda: pick([5 * math.sqrt(7), 25 * math.sqrt(7), 175, 125], round(25 * abs(math.sqrt(7) + 2 * math.sqrt(7) * cmath.exp(1j * math.pi / 3)), 6)), ['Add as phasors: A^{2} = 7 + 28 + 2 × √{7} × 2√{7} × cos60° = 49 → A = 7 cm.', 'a_{max} = ω^{2}A = 25 × 7 = 175 cm s^{−2} = 175 × 10^{−2} m s^{−2}.'], 'shm', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'shm', 'In simple harmonic motion, the total mechanical energy of given system is E. If mass of oscillating particle P (hanging on a spring of constant K) is doubled then the new energy of the system for same amplitude is :', ['\\f{E}{√{2}}', 'E', 'E√{2}', '2E'], 2,
    lambda: (lambda k, A: pick([1 / math.sqrt(2), 1, math.sqrt(2), 2], round((0.5 * (2 * 1) * (k / 2) * A * A) / (0.5 * 1 * k * A * A), 9)))(40.0, 0.1), ['E = ½mω^{2}A^{2} = ½kA^{2} (ω^{2} = k/m).', 'Doubling m halves ω^{2}: E = ½kA^{2} — unchanged.'], 'shm', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'shm', 'The displacement of a particle executing SHM is given by x = 10 sin(ωt + \\f{π}{3}) m. The time period of motion is 3.14 s. The velocity of the particle at t = 0 is ____ m/s.', None, 10,
    lambda: (lambda w: round((10 * math.sin(w * 1e-6 + math.pi / 3) - 10 * math.sin(-w * 1e-6 + math.pi / 3)) / 2e-6))(2 * math.pi / 3.14), ['ω = \\f{2π}{3.14} = 2 rad/s.', 'v = Aω cos(π/3) = 10 × 2 × ½ = 10 m/s.'], 'shm', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'shm', 'A particle is doing simple harmonic motion of amplitude 0.06 m and time period 3.14 s. The maximum velocity of the particle is ____ cm/s.', None, 12,
    lambda: round(max(abs(shm(2 * math.pi / 3.14, 0.06, 0, k * 0.05)[1]) for k in range(64)) * 100), ['ω = \\f{2π}{3.14} = 2 rad/s.', 'v_{max} = Aω = 0.06 × 2 = 0.12 m/s = 12 cm/s.'], 'shm', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'shm', 'An object of mass 0.2 kg executes simple harmonic motion along x axis with frequency of (\\f{25}{π}) Hz. At the position x = 0.04 m the object has kinetic energy 0.5 J and potential energy 0.4 J. The amplitude of oscillation is ____ cm.', None, 6,
    lambda: round(bisect(lambda A: 0.5 * 0.2 * 50 ** 2 * A * A - 0.9, 0, 1) * 100, 4), ['ω = 2πf = 50 rad/s. Total energy = 0.5 + 0.4 = 0.9 J = ½mω^{2}A^{2}.', '0.9 = 0.1 × 2500 × A^{2} → A = 0.06 m = 6 cm.'], 'shm', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'shm', 'The position, velocity and acceleration of a particle executing simple harmonic motion are found to have magnitudes of 4 m, 2 m s^{−1} and 16 m s^{−2} at a certain instant. The amplitude of the motion is √{x} m where x is ____.', None, 17,
    lambda: (lambda w: round(4 ** 2 + (2 / w) ** 2, 6))(math.sqrt(16 / 4)), ['a = ω^{2}x → ω^{2} = \\f{16}{4} = 4.', 'A^{2} = x^{2} + \\f{v^{2}}{ω^{2}} = 16 + 1 = 17.'], 'shm', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'shm', 'The kinetic energy of a simple harmonic oscillator is oscillating with angular frequency of 176 rad/s. The frequency of this simple harmonic oscillator is ……… Hz. [take π = \\f{22}{7}]', ['14', '88', '28', '176'], 1,
    lambda: pick([14, 88, 28, 176], round(176 / 2 / (2 * 22 / 7), 6)), ['K = ½mA^{2}ω^{2}cos^{2}ωt oscillates at 2ω.', 'ω = 88 rad/s → f = \\f{88}{2π} = 14 Hz.'], 'shm', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'shm', 'A particle is executing simple harmonic motion with time period 2 s and amplitude 1 cm. If D and d are the total distance and displacement covered by the particle in 12.5 s, then \\f{D}{d} is', ['\\f{16}{5}', '25', '10', '\\f{15}{4}'], 2,
    lambda: (lambda w: (lambda xs: pick([16 / 5, 25, 10, 15 / 4], round(sum(abs(b - a) for a, b in zip(xs, xs[1:])) / abs(xs[-1] - xs[0]), 2)))([math.sin(w * k * 1e-4) for k in range(125001)]))(math.pi),
    ['12.5 s = 6¼ periods. Distance: 6 × 4A + A = 25 cm.', 'Starting at the mean, after ¼ period the displacement is A = 1 cm → \\f{D}{d} = 25.'], 'shm', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'shm', 'A particle executes simple harmonic motion with an amplitude of 4 cm. At the mean position, velocity of the particle is 10 cm/s. The distance of the particle from the mean position when its speed becomes 5 cm/s is √{α} cm, where α = ____.', None, 12,
    lambda: (lambda w: round(4 ** 2 - (5 / w) ** 2, 6))(10 / 4), ['ω = \\f{v_{max}}{A} = 2.5 rad/s.', 'x^{2} = A^{2} − \\f{v^{2}}{ω^{2}} = 16 − 4 = 12.'], 'shm', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'shm', 'When the displacement of a simple harmonic oscillator is one third of its amplitude, the ratio of total energy to the kinetic energy is \\f{x}{8}, where x = ____.', None, 9,
    lambda: round(8 * 1 / (1 - (1 / 3) ** 2), 6), ['K = ½k(A^{2} − x^{2}) = \\f{8}{9}E at x = A/3.', '\\f{E}{K} = \\f{9}{8} → x = 9.'], 'shm', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'shm', 'A simple harmonic oscillator has an amplitude A and time period 6π second. Assuming the oscillation starts from its mean position, the time required by it to travel from x = A to x = \\f{√{3}}{2}A will be \\f{π}{x} s, where x = ____.', None, 2,
    lambda: round(math.pi / first_time(1 / 3, 1.0, math.sqrt(3) / 2), 3), ['ω = \\f{2π}{6π} = \\f{1}{3} rad/s. From the extreme: x = A cos ωt.', 'cos ωt = \\f{√{3}}{2} → ωt = \\f{π}{6} → t = \\f{π}{2} s → x = 2.'], 'shm', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'shm', 'The velocity of a particle executing simple harmonic motion along x-axis is described as v^{2} = 50 − x^{2}, where x represents displacement. If the time period of motion is \\f{x}{7} s, the value of x is ____. (π = 22/7)', None, 44,
    lambda: (lambda w: round(7 * 2 * 22 / 7 / w, 6))(math.sqrt(1)), ['v^{2} = ω^{2}(A^{2} − x^{2}) → ω^{2} = 1.', 'T = 2π = \\f{44}{7} s → x = 44.'], 'shm', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'shm', 'A particle performs simple harmonic motion with amplitude A. Its speed is increased to three times at an instant when its displacement is \\f{2A}{3}. The new amplitude of motion is \\f{nA}{3}. The value of n is ____.', None, 7,
    lambda: (lambda w, A: (lambda v: round(3 * math.sqrt((2 * A / 3) ** 2 + (3 * v / w) ** 2) / A, 6))(w * math.sqrt(A * A - (2 * A / 3) ** 2)))(2.0, 1.0), ['At x = \\f{2A}{3}: v = ω\\f{√{5}A}{3}; tripled: v\' = √{5}ωA.', 'A\'^{2} = \\f{4A^{2}}{9} + 5A^{2} = \\f{49A^{2}}{9} → A\' = \\f{7A}{3} → n = 7.'], 'shm', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'shm', 'Match List - I with List - II. List – I: A. sin^{2}ωt B. sin^{3}(2ωt) C. sin(ωt) + cos(πωt) D. cos ωt + cos 2ωt. List – II: I. Periodic with time period T = \\f{π}{ω} but not simple harmonic motion (SHM) II. Periodic with time period T = \\f{2π}{ω} but not SHM III. Periodic with time period T = \\f{π}{ω} and SHM IV. Non-periodic. Choose the correct answer from the options given below :',
    ['A-III, B-I, C-IV, D-II', 'A-II, B-I, C-III, D-IV', 'A-III, B-II, C-IV, D-I', 'A-II, B-I, C-IV, D-III'], 1,
    lambda: 1 if (lambda per: per(lambda t: math.sin(t) ** 2, math.pi) and not per(lambda t: math.sin(t) ** 2, math.pi / 2) and per(lambda t: math.sin(2 * t) ** 3, math.pi) and not per(lambda t: math.sin(2 * t) ** 3, math.pi / 2)
        and per(lambda t: math.cos(t) + math.cos(2 * t), 2 * math.pi) and not per(lambda t: math.cos(t) + math.cos(2 * t), math.pi) and not any(per(lambda t: math.sin(t) + math.cos(math.pi * t), T) for T in [k * 0.5 for k in range(1, 60)]))(
        lambda f, T: all(abs(f(t + T) - f(t)) < 1e-9 for t in [0.1 * k for k in range(1, 60)])) else 0,
    ['sin^{2}ωt = ½ − ½cos2ωt: an SHM about ½ with period π/ω (III). sin^{3}2ωt repeats every π/ω but is not a pure sine (I).', 'ω and πω have no common period → non-periodic (IV). cos ωt + cos 2ωt repeats every 2π/ω, not SHM (II).'], 'shm', 3)
add(('2026', 'Apr', '2026-04-06', 1), 'shm', 'A particle is executing simple harmonic motion. Its amplitude is A and time period is 5 sec. The time required by it to move from x = A to x = \\f{A}{√{2}} is ____ sec.', ['\\f{1}{4}', '\\f{5}{4}', '\\f{5}{8}', '\\f{3}{8}'], 3,
    lambda: near([0.25, 1.25, 5 / 8, 3 / 8], first_time(2 * math.pi / 5, 1.0, 1 / math.sqrt(2))), ['x = A cos ωt = \\f{A}{√{2}} → ωt = \\f{π}{4}.', 't = \\f{T}{8} = \\f{5}{8} s.'], 'shm', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'shm', 'The displacement of a particle, executing simple harmonic motion with time period T, is expressed as x(t) = A sin ωt, where A is the amplitude. The maximum value of potential energy of this oscillator is found at t = T/2β. The value of β is ____ .', None, 2,
    lambda: (lambda T: round(T / (2 * next(k * T / 10000 for k in range(1, 10000) if abs(math.sin(2 * math.pi * k / 10000)) > 1 - 1e-9 or abs(math.sin(2 * math.pi * k / 10000)) >= max(abs(math.sin(2 * math.pi * j / 10000)) for j in (k - 1, k + 1)) and abs(math.sin(2 * math.pi * k / 10000)) > 0.999)), 3))(1.0),
    ['PE is largest at the extreme, first reached at t = T/4.', '\\f{T}{2β} = \\f{T}{4} → β = 2.'], 'shm', 1)

# ---------------- springs, pendulums, oscillating bodies ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'osc', 'A simple pendulum of length 1 m has a wooden bob of mass 1 kg. It is struck by a bullet of mass 10^{−2} kg moving with a speed of 2 × 10^{2} m s^{−1}. The bullet gets embedded into the bob. The height to which the bob rises before swinging back is. (use g = 10 m/s^{2})', ['0.30 m', '0.20 m', '0.35 m', '0.40 m'], 2,
    lambda: near([0.30, 0.20, 0.35, 0.40], (0.01 * 200 / 1.01) ** 2 / (2 * G)), ['Momentum: v = \\f{0.01 × 200}{1.01} ≈ 1.98 m/s.', 'h = \\f{v^{2}}{2g} ≈ 0.196 m ≈ 0.20 m.'], 'osc', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'osc', 'Two simple pendulums having lengths l_{1} and l_{2} with negligible string mass undergo angular displacements θ_{1} and θ_{2}, from their mean positions, respectively. If the angular accelerations of both pendulums are same, then which expression is correct?', ['θ_{1}l_{2}^{2} = θ_{2}l_{1}^{2}', 'θ_{1}l_{1}^{2} = θ_{2}l_{2}^{2}', 'θ_{1}l_{1} = θ_{2}l_{2}', 'θ_{1}l_{2} = θ_{2}l_{1}'], 4,
    lambda: (lambda l1, l2, th1: (lambda th2: [i + 1 for i, ok in enumerate([abs(th1 * l2 * l2 - th2 * l1 * l1) < 1e-12, abs(th1 * l1 * l1 - th2 * l2 * l2) < 1e-12, abs(th1 * l1 - th2 * l2) < 1e-12, abs(th1 * l2 - th2 * l1) < 1e-12]) if ok][0])(th1 * l2 / l1))(1.3, 0.7, 0.05),
    ['α = \\f{g}{l}θ for small swings.', '\\f{θ_{1}}{l_{1}} = \\f{θ_{2}}{l_{2}} → θ_{1}l_{2} = θ_{2}l_{1}.'], 'osc', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'osc', 'A particle of mass 0.50 kg executes simple harmonic motion under force F = −50 (N m^{−1}) x. The time period of oscillation is \\f{x}{35} s. The value of x is ____. (Given π = \\f{22}{7})', None, 22,
    lambda: round(35 * 2 * 22 / 7 * math.sqrt(0.5 / 50), 6), ['k = 50 N/m: T = 2π√{\\f{0.5}{50}} = \\f{2π}{10}.', '= \\f{44}{70} = \\f{22}{35} s → x = 22.'], 'osc', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'osc', 'Two bodies A and B of equal mass are suspended from two massless springs of spring constant k_{1} and k_{2}, respectively. If the bodies oscillate vertically such that their amplitudes are equal, the ratio of the maximum velocity of A to the maximum velocity of B is', ['\\f{k_{2}}{k_{1}}', '\\f{k_{1}}{k_{2}}', '√{\\f{k_{1}}{k_{2}}}', '√{\\f{k_{2}}{k_{1}}}'], 3,
    lambda: (lambda k1, k2: near([k2 / k1, k1 / k2, math.sqrt(k1 / k2), math.sqrt(k2 / k1)], max(abs(shm(math.sqrt(k1), 1, 0, j * 0.01)[1]) for j in range(300)) / max(abs(shm(math.sqrt(k2), 1, 0, j * 0.01)[1]) for j in range(300))))(9.0, 4.0),
    ['v_{max} = Aω = A√{\\f{k}{m}}.', 'Same A and m → ratio √{\\f{k_{1}}{k_{2}}}.'], 'osc', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'osc', 'The time period of simple harmonic motion of mass M in the given figure is π√{\\f{αM}{5K}}, where the value of α is ____. (One spring k holds M directly; next to it, two springs k side by side hold a third spring k that holds M.)', None, 12,
    lambda: (lambda k: (lambda keff: round((2 * math.sqrt(1 / keff)) ** 2 * 5 * k, 6))(k + 1 / (1 / (2 * k) + 1 / k)))(3.0), ['Two k side by side = 2k; in series with k: \\f{2k × k}{3k} = \\f{2k}{3}. In parallel with the single k: k_{eff} = \\f{5k}{3}.', 'T = 2π√{\\f{3M}{5k}} = π√{\\f{12M}{5k}} → α = 12.'], 'osc', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'osc', 'A uniform disc of radius R and mass M is free to oscillate about the axis A (a tangent to the disc lying in its plane, at its top). For small oscillations the time period is ____ . (g is acceleration due to gravity)', ['2π√{\\f{5R}{4g}}', '2π√{\\f{2R}{3g}}', '2π√{\\f{3R}{2g}}', '2π√{\\f{3R}{g}}'], 1,
    lambda: (lambda R: near([2 * math.pi * math.sqrt(5 * R / (4 * G)), 2 * math.pi * math.sqrt(2 * R / (3 * G)), 2 * math.pi * math.sqrt(3 * R / (2 * G)), 2 * math.pi * math.sqrt(3 * R / G)], 2 * math.pi * math.sqrt((R * R / 4 + R * R) / (G * R))))(0.4),
    ['I about the tangent in the plane = \\f{MR^{2}}{4} + MR^{2} = \\f{5}{4}MR^{2}; pivot to centre = R.', 'T = 2π√{\\f{I}{MgR}} = 2π√{\\f{5R}{4g}}.'], 'osc', 3)
add(('2026', 'Jan', '2026-01-23', 1), 'osc', 'A simple pendulum of string length 30 cm performs 20 oscillations in 10 s. The length of the string required for the pendulum to perform 40 oscillations in the same time duration is ____ cm. [Assume that the mass of the pendulum remains same.]', ['120', '0.75', '7.5', '15'], 3,
    lambda: pick([120, 0.75, 7.5, 15], round(30 * (0.25 / 0.5) ** 2, 6)), ['Period halves (0.5 s → 0.25 s); T ∝ √{L}.', 'L = 30 × (½)^{2} = 7.5 cm.'], 'osc', 1)
add(('2026', 'Apr', '2026-04-08', 2), 'osc', 'The frequency of oscillation of a mass m suspended by a spring is υ_{1}. If the length of the spring is cut to half, the same mass oscillates with frequency υ_{2}. The value of υ_{2}/υ_{1} is ____ .', ['1', '2', '√{2}', '√{3}'], 3,
    lambda: near([1, 2, math.sqrt(2), math.sqrt(3)], math.sqrt(2 * 50 / 0.3) / math.sqrt(50 / 0.3)), ['Half the length → k doubles.', 'υ ∝ √{k} → √{2}.'], 'osc', 1)

# ---------------- travelling waves, superposition ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'wave', 'A sinusoidal wave of wavelength 7.5 cm travels a distance of 1.2 cm along the x-direction in 0.3 sec. The crest P is at x = 0 at t = 0 sec and maximum displacement of the wave is 2 cm. Which equation correctly represents this wave ?', ['y = 2cos(0.83x − 3.35t) cm', 'y = 2cos(0.13x − 0.5t) cm', 'y = 2sin(0.83x − 3.5t) cm', 'y = 2cos(3.35x − 0.83t) cm'], 1,
    lambda: (lambda k, w: [i + 1 for i, (f, kk, ww) in enumerate([(math.cos, 0.83, 3.35), (math.cos, 0.13, 0.5), (math.sin, 0.83, 3.5), (math.cos, 3.35, 0.83)]) if f(0) == 1 and abs(kk - k) < 0.01 and abs(ww - w) < 0.02][0])(2 * math.pi / 7.5, 2 * math.pi / 7.5 * 1.2 / 0.3),
    ['v = \\f{1.2}{0.3} = 4 cm/s; k = \\f{2π}{7.5} ≈ 0.83 cm^{−1}; ω = kv ≈ 3.35 s^{−1}.', 'A crest at x = 0 when t = 0 → cosine: y = 2cos(0.83x − 3.35t).'], 'wave', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'wave', 'Displacement of a wave is expressed as x(t) = 5cos(628t + \\f{π}{2}) m. The wavelength of the wave when its velocity is 300 m/s is : (π = 3.14)', ['0.33 m', '0.5 m', '3 m', '5 m'], 3,
    lambda: near([0.33, 0.5, 3, 5], 300 / (628 / (2 * 3.14))), ['f = \\f{628}{2 × 3.14} = 100 Hz.', 'λ = \\f{v}{f} = 3 m.'], 'wave', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'wave', 'The equation of a wave travelling on a string is y = sin[20πx + 10πt], where x and t are distance and time in SI units. The minimum distance between two points having the same oscillating speed is :', ['5.0 cm', '20 cm', '10 cm', '2.5 cm'], 1,
    lambda: near([5, 20, 10, 2.5], 100 * next(d * 1e-4 for d in range(1, 2000) if all(abs(abs(math.cos(20 * math.pi * x + 1.1)) - abs(math.cos(20 * math.pi * (x + d * 1e-4) + 1.1))) < 1e-6 for x in (0.013, 0.071, 0.2)))),
    ['Speed ∝ |cos(kx + ωt)|: equal for points half a wavelength apart.', 'λ = \\f{2π}{20π} = 0.1 m → λ/2 = 5 cm.'], 'wave', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'wave', 'The amplitude and phase of a wave that is formed by the superposition of two harmonic travelling waves, y_{1}(x, t) = 4sin(kx − ωt) and y_{2}(x, t) = 2sin(kx − ωt + \\f{2π}{3}), are: (Take the angular frequency of initial waves same as ω)', ['[√{3}, π/6]', '[2√{3}, π/6]', '[6, π/3]', '[6, 2π/3]'], 2,
    lambda: (lambda z: [i + 1 for i, (a, ph) in enumerate([(math.sqrt(3), math.pi / 6), (2 * math.sqrt(3), math.pi / 6), (6, math.pi / 3), (6, 2 * math.pi / 3)]) if abs(abs(z) - a) < 1e-9 and abs(cmath.phase(z) - ph) < 1e-9][0])(4 + 2 * cmath.exp(2j * math.pi / 3)),
    ['Phasors: 4 + 2∠120° = 4 − 1 + i√{3} = 3 + i√{3}.', 'Amplitude √{12} = 2√{3}; phase tan^{−1}(√{3}/3) = π/6.'], 'wave', 2)
add(('2025', 'Apr', '2025-04-08', 2), 'wave', 'Two strings with circular cross section and made of same material, are stretched to have same amount of tension. A transverse wave is then made to pass through both the strings. The velocity of the wave in the first string having the radius of cross section R is v_{1}, and that in the other string having the radius of cross section R/2 is v_{2}. Then \\f{v_{2}}{v_{1}} =', ['8', '4', '√{2}', '2'], 4,
    lambda: (lambda T, rho, R: pick([8, 4, math.sqrt(2), 2], round(math.sqrt(T / (rho * math.pi * (R / 2) ** 2)) / math.sqrt(T / (rho * math.pi * R * R)), 9)))(50.0, 7800.0, 1e-3), ['v = √{\\f{T}{μ}}, μ = ρπR^{2}.', 'Half the radius → μ/4 → speed × 2.'], 'wave', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'wave', 'A plane progressive wave is given by y = 2cos2π(330t − x) m. The frequency of the wave is :', ['165 Hz', '330 Hz', '660 Hz', '340 Hz'], 2,
    lambda: pick([165, 330, 660, 340], round(2 * math.pi * 330 / (2 * math.pi), 6)), ['ω = 2π × 330.', 'f = 330 Hz.'], 'wave', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'wave', 'The equation of a plane progressive wave is given by y = 5cos π(200t − \\f{x}{150}) where x and y are in cm and t is in second. The velocity of the wave is ____ m/s.', ['120', '150', '200', '300'], 4,
    lambda: pick([120, 150, 200, 300], round(200 * math.pi / (math.pi / 150) / 100, 6)), ['v = \\f{ω}{k} = \\f{200π}{π/150} = 30000 cm/s.', '= 300 m/s.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'wave', 'The speed of a longitudinal wave in a metallic bar is 400 m/s. If the density and Young\'s modulus of the bar material are increased by 0.5% and 1%, respectively then the speed of the wave is changed approximately to ____ m/s.', ['401', '399', '398', '402'], 1,
    lambda: near([401, 399, 398, 402], 400 * math.sqrt(1.01 / 1.005)), ['v = √{\\f{Y}{ρ}}: \\f{Δv}{v} ≈ ½(1% − 0.5%) = 0.25%.', '400 × 1.0025 ≈ 401 m/s.'], 'wave', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'wave', 'A wave on a string is y(x, t) = 4.0 sin[20 × 10^{−3}x + 600t] mm, where x is in mm and t is in second. The velocity of the wave is :', ['−30 m/s', '+60 m/s', '+30 m/s', '−60 m/s'], 1,
    lambda: near([-30, 60, 30, -60], -600 / 20e-3 / 1000), ['kx + ωt → moves towards −x with v = \\f{ω}{k}.', '= \\f{600}{0.02} mm/s = 30 m/s, in the −x direction → −30 m/s.'], 'wave', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'wave', 'A transverse wave on a string is described by y = 3 sin(36t + 0.018x + π/4), where x, y are in cm and t in seconds. The least distance between the two successive crests in the wave is ____ cm. (Nearest integer) (π = 3.14)', None, 349,
    lambda: round(2 * 3.14 / 0.018), ['Successive crests are one wavelength apart: λ = \\f{2π}{k}.', '= \\f{6.28}{0.018} ≈ 349 cm.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'wave', 'The velocity of sound in air is doubled when the temperature is raised from 0 °C to α °C. The value of α is ____ .', None, 819,
    lambda: round(bisect(lambda T: math.sqrt((T + 273) / 273) - 2, 0, 5000)), ['v ∝ √{T} (kelvin): doubling needs 4 × 273 = 1092 K.', 'α = 1092 − 273 = 819 °C.'], 'wave', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'wave', 'The speed of sound in oxygen at S.T.P. will be approximately: (Given, R = 8.3 J K^{−1}, γ = 1.4)', ['310 m/s', '333 m/s', '341 m/s', '325 m/s'], 1,
    lambda: near([310, 333, 341, 325], math.sqrt(1.4 * 8.3 * 273 / 0.032)), ['v = √{\\f{γRT}{M}} with M = 0.032 kg/mol, T = 273 K.', '= √{\\f{1.4 × 8.3 × 273}{0.032}} ≈ 315 m/s — closest 310 m/s.'], 'wave', 2)
add(('2024', 'Jan', '2024-01-31', 1), 'wave', 'Two waves of intensity ratio 1 : 9 cross each other at a point. The resultant intensities at the point, when (a) Waves are incoherent is I_{1} (b) Waves are coherent is I_{2} and differ in phase by 60°. If \\f{I_{1}}{I_{2}} = \\f{10}{x} then x = ____.', None, 13,
    lambda: (lambda z: round(10 / ((1 + 9) / abs(z) ** 2), 6))(1 + 3 * cmath.exp(1j * math.pi / 3)), ['Incoherent: I_{1} = I + 9I = 10I.', 'Coherent: I_{2} = I + 9I + 2√{9}I cos60° = 13I → x = 13.'], 'wave', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'wave', 'Two harmonic waves moving in the same direction superimpose to form a wave x = a cos(1.5t) cos(50.5t) where t is in seconds. Find the period with which they beat. (close to nearest integer)', ['1 s', '2 s', '6 s', '4 s'], 2,
    lambda: near([1, 2, 6, 4], 2 * math.pi / ((50.5 + 1.5) - (50.5 - 1.5))), ['cos A cos B = ½[cos(52t) + cos(49t)]: two waves of ω = 52 and 49.', 'Beat ω = 3 rad/s → period \\f{2π}{3} ≈ 2 s.'], 'wave', 2)

# ---------------- sound: pipes, strings, beats ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'sound', 'A tuning fork resonates with a sonometer wire of length 1 m stretched with a tension of 6 N. When the tension in the wire is changed to 54 N, the same tuning fork produces 12 beats per second with it. The frequency of the tuning fork is ____ Hz.', None, 6,
    lambda: round(bisect(lambda f: f * math.sqrt(54 / 6) - f - 12, 0.1, 1000), 6), ['f ∝ √{T}: tension × 9 → wire frequency × 3.', '3f − f = 12 → f = 6 Hz.'], 'sound', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'sound', 'In the resonance experiment, two air columns (closed at one end) of 100 cm and 120 cm long, give 15 beats per second when each one is sounding in the respective fundamental modes. The velocity of sound in the air column is:', ['340 m/s', '370 m/s', '360 m/s', '335 m/s'], 3,
    lambda: near([340, 370, 360, 335], bisect(lambda v: closed(1, v, 1.0) - closed(1, v, 1.2) - 15, 1, 1000)), ['\\f{v}{4 × 1} − \\f{v}{4 × 1.2} = 15.', 'v(0.25 − 0.2083) = 15 → v = 360 m/s.'], 'sound', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'sound', 'In an experiment with a closed organ pipe, it is filled with water by (\\f{1}{5})th of its volume. The frequency of the fundamental note will change by', ['25%', '20%', '−25%', '−20%'], 1,
    lambda: pick([25, 20, -25, -20], round(100 * (closed(1, 330, 0.8) / closed(1, 330, 1) - 1), 6)), ['The air column becomes \\f{4}{5} as long; f ∝ \\f{1}{L}.', 'New f = \\f{5}{4}f → +25%.'], 'sound', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'sound', 'A sonometer wire of resonating length 90 cm has a fundamental frequency of 400 Hz when kept under some tension. The resonating length of the wire with fundamental frequency of 600 Hz under same tension ____ cm.', None, 60,
    lambda: round(bisect(lambda L: 400 * 90 / L - 600, 1, 1000), 4), ['Same tension → same wave speed: f ∝ \\f{1}{L}.', 'L = 90 × \\f{400}{600} = 60 cm.'], 'sound', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'sound', 'Two open organ pipes of length 60 cm and 90 cm resonate at 6th and 5th harmonics respectively. The difference of frequencies for the given modes is ____ Hz. (Velocity of sound in air = 333 m/s)', None, 740,
    lambda: round(open_(6, 333, 0.6) - open_(5, 333, 0.9)), ['f_{n} = \\f{nv}{2L}: \\f{6 × 333}{1.2} = 1665 Hz; \\f{5 × 333}{1.8} = 925 Hz.', 'Difference = 740 Hz.'], 'sound', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'sound', 'A closed and an open organ pipe have same lengths. If the ratio of frequencies of their seventh overtones is (\\f{a − 1}{a}) then the value of a is ____.', None, 16,
    lambda: (lambda r: round(1 / (1 - r), 6))(closed(8, 1, 1) / open_(8, 1, 1)), ['Closed pipe, 7th overtone = 8th allowed mode = 15th harmonic: \\f{15v}{4L}. Open pipe, 7th overtone = 8th harmonic: \\f{8v}{2L} = \\f{16v}{4L}.', 'Ratio \\f{15}{16} → a = 16.'], 'sound', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'sound', 'Two tuning forks A and B are sounded together giving rise to 8 beats in 2 s. When fork A is loaded with wax, the beat frequency is reduced to 4 beats in 2 s. If the original frequency of tuning fork B is 380 Hz then original frequency of tuning fork A is ____ Hz.', None, 384,
    lambda: [fA for fA in (380 + 4, 380 - 4) if abs(abs((fA - 2) - 380) - 2) < 1e-9][0], ['4 beats/s → A is 384 or 376 Hz.', 'Wax lowers A: from 384 it moves towards 380 (beats fall to 2/s); from 376 they would rise. So A = 384 Hz.'], 'sound', 2)
add(('2025', 'Jan', '2025-01-22', 1), 'sound', 'A closed organ and an open organ tube are filled by two different gases having same bulk modulus but different densities ρ_{1} and ρ_{2}, respectively. The frequency of 9^{th} harmonic of closed tube is identical with 4^{th} harmonic of open tube. If the length of the closed tube is 10 cm and the density ratio of the gases is ρ_{1} : ρ_{2} = 1 : 16, then the length of the open tube is :', ['\\f{15}{9} cm', '\\f{15}{7} cm', '\\f{20}{7} cm', '\\f{20}{9} cm'], 4,
    lambda: (lambda v1, v2: near([15 / 9, 15 / 7, 20 / 7, 20 / 9], bisect(lambda L2: 9 * v1 / (4 * 10) - 4 * v2 / (2 * L2), 0.01, 100)))(math.sqrt(1 / 1), math.sqrt(1 / 16)), ['v = √{\\f{B}{ρ}} → v_{1} = 4v_{2}.', '\\f{9 × 4v_{2}}{4 × 10} = \\f{4v_{2}}{2L_{2}} → L_{2} = \\f{20}{9} cm.'], 'sound', 3)
add(('2024', 'Jan', '2024-01-27', 2), 'sound', 'A closed organ pipe 150 cm long gives 7 beats per second with an open organ pipe of length 350 cm, both vibrating in fundamental mode. The velocity of sound is ____ m/s.', None, 294,
    lambda: round(bisect(lambda v: closed(1, v, 1.5) - open_(1, v, 3.5) - 7, 1, 2000), 4), ['\\f{v}{4 × 1.5} − \\f{v}{2 × 3.5} = 7.', '\\f{v}{6} − \\f{v}{7} = \\f{v}{42} = 7 → v = 294 m/s.'], 'sound', 2)
add(('2024', 'Jan', '2024-01-30', 1), 'sound', 'In a closed organ pipe, the frequency of fundamental note is 30 Hz. A certain amount of water is now poured in the organ pipe so that the fundamental frequency is increased to 110 Hz. If the organ pipe has a cross-sectional area of 2 cm^{2}, the amount of water poured in the organ tube is ____ g. (Take speed of sound in air is 330 m/s)', None, 400,
    lambda: (lambda L1, L2: round((L1 - L2) * 100 * 2 * 1, 4))(bisect(lambda L: closed(1, 330, L) - 30, 0.01, 100), bisect(lambda L: closed(1, 330, L) - 110, 0.01, 100)), ['L = \\f{v}{4f}: 2.75 m before, 0.75 m after.', 'Water column 200 cm × 2 cm^{2} = 400 cm^{3} = 400 g.'], 'sound', 2)
add(('2024', 'Jan', '2024-01-31', 1), 'sound', 'The fundamental frequency of a closed organ pipe is equal to the first overtone frequency of an open organ pipe. If length of the open pipe is 60 cm, the length of the closed pipe will be :', ['60 cm', '45 cm', '30 cm', '15 cm'], 4,
    lambda: pick([60, 45, 30, 15], round(bisect(lambda L: closed(1, 330, L) - open_(2, 330, 0.6), 0.01, 10) * 100, 4)), ['Open pipe first overtone: \\f{2v}{2 × 60} = \\f{v}{60}.', 'Closed: \\f{v}{4L} = \\f{v}{60} → L = 15 cm.'], 'sound', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'sound', 'In an open organ pipe υ_{3} and υ_{6} are 3^{rd} and 6^{th} harmonic frequencies, respectively. If υ_{6} − υ_{3} = 2200 Hz then length of the pipe is ____ mm. (Take velocity of sound in air is 330 m/s)', ['250', '225', '275', '200'], 2,
    lambda: pick([250, 225, 275, 200], round(bisect(lambda L: open_(6, 330, L) - open_(3, 330, L) - 2200, 0.01, 10) * 1000, 4)), ['υ_{6} − υ_{3} = \\f{3v}{2L} = 2200.', 'L = \\f{3 × 330}{4400} = 0.225 m = 225 mm.'], 'sound', 1)
add(('2026', 'Jan', '2026-01-24', 2), 'sound', 'The fifth harmonic of a closed organ pipe is found to be in unison with the first harmonic of an open pipe. The ratio of lengths of closed pipe to that of the open pipe is 5/x. The value of x is ____.', ['4', '2', '1', '3'], 2,
    lambda: pick([4, 2, 1, 3], round(5 / bisect(lambda Lc: 5 * 330 / (4 * Lc) - open_(1, 330, 1.0), 0.01, 100), 6)), ['Closed 5th harmonic: \\f{5v}{4L_{c}} = open fundamental \\f{v}{2L_{o}}.', '\\f{L_{c}}{L_{o}} = \\f{5}{2} → x = 2.'], 'sound', 2)
for _p in P: _p['t'] = _p['fam']
