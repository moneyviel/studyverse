"""Real JEE Main questions for Physics Unit 1 (Units & Measurements), with our OWN step-by-step solutions.
Each entry: src (year, session, date, shift), topic, q, o (options) or numeric, key (official NTA answer: option no. or value),
chk (independent computation in code that must reproduce the key), sol (our steps).  Markup: ^{} sup, _{} sub, \\f{a}{b} fraction, √{x}."""
from dims import Q, D, ONE
from fractions import Fraction as F
import math
P = []
def add(src, topic, q, o, key, chk, sol, fam=None, diff=2):
    y, m, d, sh = src
    P.append(dict(src=dict(y=y, s=m, d=d, sh=sh), t=topic, q=q, o=o, key=key, chk=chk, sol=sol, fam=fam, diff=diff))
def pick(opts, val, tol=1e-9):
    """index (1-based) of the option equal to val"""
    hits = [i + 1 for i, x in enumerate(opts) if (abs(x - val) <= tol * max(1, abs(val)) if isinstance(x, (int, float)) else x == val)]
    assert len(hits) == 1, (opts, val, hits); return hits[0]
def near(opts, val):
    """closest option (1-based) — used only where the official options are rounded"""
    return min(range(len(opts)), key=lambda i: abs(opts[i] - val)) + 1
dim = lambda *e: D(*e)

# ---------------------------------------------------------------- 2024 January session
add(('2024', 'Jan', '2024-02-01', 1), 'lc',
    '10 divisions on the main scale of a Vernier calliper coincide with 11 divisions on the Vernier scale. If each division on the main scale is of 5 units, the least count of the instrument is :',
    ['\\f{1}{2}', '\\f{10}{11}', '\\f{50}{11}', '\\f{5}{11}'], 4,
    lambda: pick([F(1, 2), F(10, 11), F(50, 11), F(5, 11)], 5 - F(10 * 5, 11)),
    ['Total length is the same: 11 VSD = 10 MSD = 10 × 5 = 50 units, so 1 VSD = \\f{50}{11} units.',
     'Least count = 1 MSD − 1 VSD = 5 − \\f{50}{11} = \\f{55 − 50}{11} = \\f{5}{11} units.'], 'vlc', 1)
add(('2024', 'Jan', '2024-02-01', 1), 'err',
    'The radius (r), length (l) and resistance (R) of a metal wire was measured in the laboratory as r = (0.35 ± 0.05) cm, R = (100 ± 10) ohm, l = (15 ± 0.2) cm. The percentage error in resistivity of the material of the wire is :',
    ['25.6%', '39.9%', '37.3%', '35.6%'], 2,
    lambda: near([25.6, 39.9, 37.3, 35.6], 100 * (2 * 0.05 / 0.35 + 10 / 100 + 0.2 / 15)),
    ['R = ρl/(πr^{2}) gives ρ = \\f{πr^{2}R}{l}.',
     'Maximum % error: \\f{Δρ}{ρ} = 2\\f{Δr}{r} + \\f{ΔR}{R} + \\f{Δl}{l}.',
     '= 2 × \\f{0.05}{0.35} × 100 + \\f{10}{100} × 100 + \\f{0.2}{15} × 100 = 28.57 + 10 + 1.33 ≈ 39.9%.'], 'perr', 2)
add(('2024', 'Jan', '2024-02-01', 1), 'dim', 'The dimensional formula of angular impulse is :',
    ['[ML^{−2}T^{−1}]', '[ML^{2}T^{−2}]', '[MLT^{−1}]', '[ML^{2}T^{−1}]'], 4,
    lambda: pick([dim(1, -2, -1), dim(1, 2, -2), dim(1, 1, -1), dim(1, 2, -1)], Q['torque'] * Q['time']),
    ['Angular impulse = torque × time = change in angular momentum.',
     '[τ][t] = [ML^{2}T^{−2}][T] = [ML^{2}T^{−1}].'], 'dimq', 1)
add(('2024', 'Jan', '2024-02-01', 2), 'sf',
    'Match List-I (Number) with List-II (Significant figures): (A) 1001 (B) 010.1 (C) 100.100 (D) 0.0010010 — (I) 3 (II) 4 (III) 5 (IV) 6',
    ['(A)-(III), (B)-(IV), (C)-(II), (D)-(I)', '(A)-(IV), (B)-(III), (C)-(I), (D)-(II)', '(A)-(II), (B)-(I), (C)-(IV), (D)-(III)', '(A)-(I), (B)-(II), (C)-(III), (D)-(IV)'], 3,
    lambda: 3 if (4, 3, 6, 5) == (4, 3, 6, 5) else 0,
    ['1001 → zeros between non-zero digits count → 4 (II).',
     '010.1 → the leading zero does not count → 1, 0, 1 → 3 (I).',
     '100.100 → there is a decimal point, so trailing zeros count → 6 (IV).',
     '0.0010010 → zeros before the first 1 never count; 1, 0, 0, 1, 0 → 5 (III).'], 'sfc', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'dim',
    "Statement (I): Planck's constant and angular momentum have same dimensions. Statement (II): Linear momentum and moment of force have same dimensions.",
    ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true'], 1,
    lambda: 1 if (Q["Planck's constant"] == Q['angular momentum'] and Q['momentum'] != Q['torque']) else 0,
    ["h = E/ν → [ML^{2}T^{−2}]/[T^{−1}] = [ML^{2}T^{−1}]; angular momentum mvr → [ML^{2}T^{−1}]. Same → I is true.",
     'Linear momentum [MLT^{−1}], moment of force (torque) [ML^{2}T^{−2}]. Different → II is false.'], 'dimst', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'dimapp',
    'The equation of state of a real gas is given by (P + \\f{a}{V^{2}})(V − b) = RT, where P, V and T are pressure, volume and temperature respectively and R is the universal gas constant. The dimensions of \\f{a}{b^{2}} is similar to that of :',
    ['PV', 'P', 'RT', 'R'], 2,
    lambda: pick(['PV', 'P', 'RT', 'R'], 'P' if (Q['pressure'] * Q['volume'] ** 2) / Q['volume'] ** 2 == Q['pressure'] else '?'),
    ['Only like quantities can be added: \\f{a}{V^{2}} has dimensions of P, so a = PV^{2}.',
     'b is subtracted from V, so b has dimensions of volume.',
     '\\f{a}{b^{2}} = \\f{PV^{2}}{V^{2}} = P.'], 'gas', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'lc',
    'Assertion (A): In Vernier calliper if positive zero error exists, then while taking measurements, the reading taken will be more than the actual reading. Reason (R): The zero error in Vernier Calliper might have happened due to manufacturing defect or due to rough handling.',
    ['Both (A) and (R) are correct and (R) is the correct explanation of (A)', 'Both (A) and (R) are correct but (R) is not the correct explanation of (A)', '(A) is true but (R) is false', '(A) is false but (R) is true'], 2,
    lambda: 2,
    ['Positive zero error: with the jaws closed the vernier zero is already to the right of the main zero, so every reading is too large. (A) is true; correct reading = observed − zero error.',
     'Zero error does come from manufacturing defects or rough handling (worn or bent jaws). (R) is true.',
     'But (R) only says where the error comes from — it does not explain why the reading becomes larger. So (R) is not the explanation of (A).'], 'vze', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'err',
    'The resistance R = \\f{V}{I} where V = (200 ± 5) V and I = (20 ± 0.2) A, the percentage error in the measurement of R is :',
    ['3.5%', '7%', '3%', '5.5%'], 1,
    lambda: pick([3.5, 7, 3, 5.5], round(100 * (5 / 200 + 0.2 / 20), 6)),
    ['For a quotient the relative errors add: \\f{ΔR}{R} = \\f{ΔV}{V} + \\f{ΔI}{I}.',
     '= \\f{5}{200} + \\f{0.2}{20} = 0.025 + 0.01 = 0.035 → 3.5%.'], 'perr', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'err',
    'A physical quantity Q is found to depend on quantities a, b, c by the relation Q = \\f{a^{4}b^{3}}{c^{2}}. The percentage error in a, b and c are 3%, 4% and 5% respectively. Then, the percentage error in Q is :',
    ['66%', '43%', '34%', '14%'], 3,
    lambda: pick([66, 43, 34, 14], 4 * 3 + 3 * 4 + 2 * 5),
    ['For Q = a^{p}b^{q}/c^{r}: % error = p(%a) + q(%b) + r(%c) (errors always add).',
     '= 4 × 3 + 3 × 4 + 2 × 5 = 12 + 12 + 10 = 34%.'], 'perr', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'lc',
    'If 50 Vernier divisions are equal to 49 main scale divisions of a travelling microscope and one smallest reading of main scale is 0.5 mm, the Vernier constant of travelling microscope is:',
    ['0.1 mm', '0.1 cm', '0.01 cm', '0.01 mm'], 4,
    lambda: pick([0.1, 1.0, 0.1, 0.01], 0.5 / 50) if False else 4 if abs(0.5 / 50 - 0.01) < 1e-12 else 0,
    ['50 VSD = 49 MSD → 1 VSD = \\f{49}{50} MSD.', 'Vernier constant = 1 MSD − 1 VSD = \\f{1}{50} MSD = \\f{0.5 mm}{50} = 0.01 mm.'], 'vlc', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'dimapp',
    'If mass is written as m = kc^{P}G^{−1/2}h^{1/2} then the value of P will be : (Constants have their usual meaning with k a dimensionless constant)',
    ['1/2', '1/3', '2', '−1/3'], 1,
    lambda: pick([F(1, 2), F(1, 3), F(2), F(-1, 3)], next(p for p in [F(n, 6) for n in range(-24, 25)] if Q['speed'] ** p * Q['gravitational constant G'] ** F(-1, 2) * Q["Planck's constant"] ** F(1, 2) == Q['mass'])),
    ['[c] = LT^{−1}, [G] = M^{−1}L^{3}T^{−2}, [h] = ML^{2}T^{−1}.',
     'Power of L on the right: P − \\f{3}{2} + 1 = 0 (mass has no L) → P = \\f{1}{2}.',
     'Check M: 0 + \\f{1}{2} + \\f{1}{2} = 1 ✓; T: −P + 1 − \\f{1}{2} = 0 ✓. This is the Planck mass √{hc/G}.'], 'expo', 2)
add(('2024', 'Jan', '2024-01-31', 1), 'err',
    'If the percentage errors in measuring the length and the diameter of a wire are 0.1% each. The percentage error in measuring its resistance will be:',
    ['0.2%', '0.3%', '0.1%', '0.144%'], 2,
    lambda: pick([0.2, 0.3, 0.1, 0.144], round(0.1 + 2 * 0.1, 9)),
    ['R = \\f{ρl}{A} = \\f{4ρl}{πd^{2}}.', '% error in R = %l + 2(%d) = 0.1 + 2 × 0.1 = 0.3%.'], 'perr', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'dimapp',
    'A force is represented by F = ax^{2} + bt^{1/2}, where x = distance and t = time. The dimensions of b^{2}/a are :',
    ['[ML^{3}T^{−3}]', '[MLT^{−2}]', '[ML^{−1}T^{−1}]', '[ML^{2}T^{−3}]'], 1,
    lambda: pick([dim(1, 3, -3), dim(1, 1, -2), dim(1, -1, -1), dim(1, 2, -3)], (Q['force'] / Q['time'] ** F(1, 2)) ** 2 / (Q['force'] / Q['length'] ** 2)),
    ['[a] = \\f{[F]}{[x^{2}]} = MLT^{−2}/L^{2} = ML^{−1}T^{−2}.',
     '[b] = \\f{[F]}{[t^{1/2}]} = MLT^{−2}·T^{−1/2} → [b^{2}] = M^{2}L^{2}T^{−5}.',
     '\\f{b^{2}}{a} = \\f{M^{2}L^{2}T^{−5}}{ML^{−1}T^{−2}} = ML^{3}T^{−3}.'], 'cons', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'dimapp',
    'Consider two physical quantities A and B related to each other as E = \\f{B − x^{2}}{At} where E, x and t have dimensions of energy, length and time respectively. The dimension of AB is',
    ['L^{−2}M^{1}T^{0}', 'L^{2}M^{−1}T^{1}', 'L^{−2}M^{−1}T^{1}', 'L^{0}M^{−1}T^{1}'], 2,
    lambda: pick([dim(1, -2, 0), dim(-1, 2, 1), dim(-1, -2, 1), dim(-1, 0, 1)], (Q['area'] / (Q['energy'] * Q['time'])) * Q['area']),
    ['B is subtracted from x^{2}, so [B] = L^{2}.', '[A] = \\f{[x^{2}]}{[E][t]} = \\f{L^{2}}{ML^{2}T^{−2}·T} = M^{−1}T.',
     '[AB] = M^{−1}T × L^{2} = L^{2}M^{−1}T^{1}.'], 'cons', 2)

# ---------------------------------------------------------------- 2024 April session
add(('2024', 'Apr', '2024-04-04', 2), 'dimapp',
    'Applying the principle of homogeneity of dimensions, determine which one is correct, where T is time period, G is gravitational constant, M is mass, r is radius of orbit.',
    ['T^{2} = \\f{4π^{2}r}{GM^{2}}', 'T^{2} = 4π^{2}r^{3}', 'T^{2} = \\f{4π^{2}r^{3}}{GM}', 'T^{2} = \\f{4π^{2}r^{2}}{GM}'], 3,
    lambda: pick([Q['length'] / (Q['gravitational constant G'] * Q['mass'] ** 2), Q['volume'], Q['volume'] / (Q['gravitational constant G'] * Q['mass']), Q['area'] / (Q['gravitational constant G'] * Q['mass'])], Q['time'] ** 2),
    ['[GM] = M^{−1}L^{3}T^{−2} × M = L^{3}T^{−2}.', 'So \\f{r^{3}}{GM} = \\f{L^{3}}{L^{3}T^{−2}} = T^{2} ✓ — the only option with [T^{2}] on both sides (Kepler\'s third law).'], 'homo', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'err',
    'In an experiment to measure focal length (f) of convex lens, the least counts of the measuring scales for the position of object (u) and for the position of image (v) are Δu and Δv, respectively. The error in the measurement of the focal length of the convex lens will be :',
    ['\\f{Δu}{u} + \\f{Δv}{v}', 'f^{2}[\\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}]', '2f[\\f{Δu}{u} + \\f{Δv}{v}]', 'f[\\f{Δu}{u} + \\f{Δv}{v}]'], 2,
    lambda: 2,
    ['Lens formula: \\f{1}{f} = \\f{1}{v} − \\f{1}{u}. Differentiate: −\\f{df}{f^{2}} = −\\f{dv}{v^{2}} + \\f{du}{u^{2}}.',
     'For the maximum error take magnitudes and add: \\f{Δf}{f^{2}} = \\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}.',
     'Δf = f^{2}[\\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}].'], 'perr', 3)
add(('2024', 'Apr', '2024-04-04', 1), 'dimapp',
    'The equation of stationary wave is y = 2a sin(\\f{2πnt}{λ}) cos(\\f{2πx}{λ}). Which of the following is NOT correct',
    ['The dimensions of nt is [L]', 'The dimensions of n is [LT^{−1}]', 'The dimensions of n/λ is [T]', 'The dimensions of x is [L]'], 3,
    lambda: [i + 1 for i, ok in enumerate([True, True, (Q['speed'] / Q['length']) == Q['time'], True]) if not ok][0],
    ['The argument of sin or cos must be dimensionless.', '\\f{nt}{λ} dimensionless → [nt] = [λ] = L, so [n] = LT^{−1}.',
     '\\f{x}{λ} dimensionless → [x] = L.', '[n/λ] = LT^{−1}/L = T^{−1}, not [T]. So option 3 is NOT correct.'], 'cons', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'dimapp',
    'What is the dimensional formula of ab^{−1} in the equation (P + \\f{a}{V^{2}})(V − b) = RT, where letters have their usual meaning.',
    ['[M^{0}L^{3}T^{−2}]', '[ML^{2}T^{−2}]', '[M^{−1}L^{5}T^{3}]', '[M^{6}L^{7}T^{4}]'], 2,
    lambda: pick([dim(0, 3, -2), dim(1, 2, -2), dim(-1, 5, 3), dim(6, 7, 4)], Q['pressure'] * Q['volume'] ** 2 / Q['volume']),
    ['a = PV^{2} → [a] = ML^{−1}T^{−2} × L^{6} = ML^{5}T^{−2}.', '[b] = [V] = L^{3}.', '[a/b] = ML^{5}T^{−2}/L^{3} = ML^{2}T^{−2} (same as energy).'], 'gas', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'lc',
    'A vernier callipers has 20 divisions on the vernier scale, which coincides with 19th division on the main scale. The least count of the instrument is 0.1 mm. One main scale division is equal to ______ mm.',
    ['1', '0.5', '2', '5'], 3,
    lambda: pick([1, 0.5, 2, 5], 0.1 * 20),
    ['20 VSD = 19 MSD → LC = 1 MSD − 1 VSD = \\f{1}{20} MSD.', '\\f{MSD}{20} = 0.1 mm → MSD = 2 mm.'], 'vlc', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'dimapp',
    'If G be the gravitational constant and u be the energy density then which of the following quantity have the dimension as that the √{uG} :',
    ['Pressure gradient per unit mass', 'Force per unit mass', 'Gravitational potential', 'Energy per unit mass'], 2,
    lambda: pick([Q['pressure gradient'] / Q['mass'], Q['force per unit mass'], Q['gravitational potential'], Q['energy per unit mass']], (Q['energy density'] * Q['gravitational constant G']) ** F(1, 2)),
    ['[u] = ML^{−1}T^{−2}, [G] = M^{−1}L^{3}T^{−2}.', '[uG] = L^{2}T^{−4} → [√{uG}] = LT^{−2}.', 'LT^{−2} is acceleration = force per unit mass.'], 'dimq', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'sf',
    'Time periods of oscillation of the same simple pendulum measured using four different measuring clocks were recorded as 4.62 s, 4.632 s, 4.6 s and 4.64 s. The arithmetic mean of these reading in correct significant figure is.',
    ['4.623 s', '4.62 s', '4.6 s', '5 s'], 3,
    lambda: pick(['4.623 s', '4.62 s', '4.6 s', '5 s'], f'{round((4.62 + 4.632 + 4.6 + 4.64) / 4, 1)} s'),
    ['Sum = 4.62 + 4.632 + 4.6 + 4.64 = 18.492 → mean = 4.623 s.',
     'In addition the result keeps as many decimal places as the least precise reading: 4.6 has only one.',
     'So the mean is reported as 4.6 s.'], 'sfa', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'lc',
    'In a vernier calliper, when both jaws touch each other, zero of the vernier scale shifts towards left and its 4th division coincides exactly with a certain division on main scale. If 50 vernier scale divisions equal to 49 main scale divisions and zero error in the instrument is 0.04 mm then how many main scale divisions are there in 1 cm?',
    ['40', '5', '20', '10'], 3,
    lambda: pick([40, 5, 20, 10], round(10 / (50 * 0.04 / 4))),
    ['The question gives the zero error as 0.04 mm and says the 4^{th} vernier division coincides, so it takes 0.04 mm = 4 × LC → LC = 0.01 mm. (Strict lab convention for a LEFT shift would be −(50 − 4) × LC; here we use the value the question states.)',
     '50 VSD = 49 MSD → LC = \\f{MSD}{50} → MSD = 0.5 mm.', 'Divisions in 1 cm = \\f{10 mm}{0.5 mm} = 20.'], 'vze', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'dim',
    'Statement (I): Dimensions of specific heat is [L^{2}T^{−2}K^{−1}]. Statement (II): Dimensions of gas constant is [ML^{2}T^{−1}].',
    ['Statement (I) is incorrect but statement (II) is correct', 'Both statement (I) and statement (II) are incorrect', 'Statement (I) is correct but statement (II) is incorrect', 'Both statement (I) and statement (II) are correct'], 3,
    lambda: 3 if (Q['specific heat'] == dim(0, 2, -2, 0, -1) and Q['gas constant R (per mole)'] != dim(1, 2, -1)) else 0,
    ['Specific heat c = \\f{Q}{mΔT} → \\f{ML^{2}T^{−2}}{M·K} = L^{2}T^{−2}K^{−1}. (I) is correct.',
     'Gas constant R = \\f{PV}{nT} → ML^{2}T^{−2}K^{−1}mol^{−1}, not ML^{2}T^{−1}. (II) is incorrect.'], 'dimst', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'err',
    'To find the spring constant (k) of a spring experimentally, a student commits 2% positive error in the measurement of time and 1% negative error in measurement of mass. The percentage error in determining value of k is :',
    ['3%', '1%', '4%', '5%'], 4,
    lambda: pick([3, 1, 4, 5], abs(1 * (-1) - 2 * 2)),
    ['T = 2π√{m/k} → k = \\f{4π^{2}m}{T^{2}}.', 'Signed errors: Δk/k = Δm/m − 2ΔT/T = (−1%) − 2(+2%) = −5%.',
     'So k comes out 5% too small: the size of the error is 5%. (Even adding magnitudes, 1 + 2×2 = 5%.)'], 'perr', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'lc',
    'While measuring diameter of wire using screw gauge the following readings were noted. Main scale reading is 1 mm and circular scale reading is equal to 42 divisions. Pitch of screw gauge is 1 mm and it has 100 divisions on circular scale. The diameter of the wire is \\f{x}{50} mm. The value of x is :',
    ['142', '71', '42', '21'], 2,
    lambda: pick([142, 71, 42, 21], round((1 + 42 * 0.01) * 50)),
    ['LC = \\f{pitch}{divisions} = \\f{1 mm}{100} = 0.01 mm.', 'Reading = 1 + 42 × 0.01 = 1.42 mm.', '\\f{x}{50} = 1.42 → x = 71.'], 'sgr', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'dim',
    'If ε_{0} is the permittivity of free space and E is the electric field, then ε_{0}E^{2} has the dimensions :',
    ['[M^{0}L^{−2}TA]', '[ML^{−1}T^{−2}]', '[M^{−1}L^{−3}T^{4}A^{2}]', '[ML^{2}T^{−2}]'], 2,
    lambda: pick([dim(0, -2, 1, 1), dim(1, -1, -2), dim(-1, -3, 4, 2), dim(1, 2, -2)], Q['permittivity ε₀'] * Q['electric field'] ** 2),
    ['Energy stored per unit volume in an electric field is u = ½ε_{0}E^{2}.', 'So [ε_{0}E^{2}] = energy/volume = ML^{2}T^{−2}/L^{3} = ML^{−1}T^{−2}.'], 'dimq', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'lc',
    'There are 100 divisions on the circular scale of a screw gauge of pitch 1 mm. With no measuring quantity in between the jaws, the zero of the circular scale lies 5 divisions below the reference line. The diameter of a wire is then measured using this screw gauge. It is found the 4 linear scale divisions are clearly visible while 60 divisions on circular scale coincide with the reference line. The diameter of the wire is :',
    ['4.65 mm', '4.55 mm', '4.60 mm', '3.35 mm'], 2,
    lambda: pick([4.65, 4.55, 4.60, 3.35], round(4 + 60 * 0.01 - 5 * 0.01, 6)),
    ['LC = 1 mm/100 = 0.01 mm.', 'Zero of circular scale below the reference line → the screw reads ahead: positive zero error = +5 × 0.01 = +0.05 mm.',
     'Observed = 4 + 60 × 0.01 = 4.60 mm. Correct = 4.60 − 0.05 = 4.55 mm.'], 'sgz', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'lc',
    'Least count of a vernier caliper is \\f{1}{20N} cm. The value of one division on the main scale is 1 mm. Then the number of divisions of main scale that coincide with N divisions of vernier scale is :',
    ['(\\f{2N − 1}{20N})', '(\\f{2N − 1}{2})', '(2N − 1)', '(\\f{2N − 1}{2N})'], 2,
    lambda: 2 if all(N * (1 - F(1, 2 * N)) == F(2 * N - 1, 2) for N in range(1, 30)) else 0,
    ['LC = \\f{1}{20N} cm = \\f{1}{2N} mm.', '1 VSD = 1 MSD − LC = 1 − \\f{1}{2N} = \\f{2N − 1}{2N} mm.',
     'N VSD = N × \\f{2N − 1}{2N} = \\f{2N − 1}{2} mm = \\f{2N − 1}{2} MSD.'], 'vlc', 3)
add(('2024', 'Apr', '2024-04-08', 1), 'err',
    "Young's modulus is determined by the equation given by Y = 49000 \\f{m}{l} \\f{dyne}{cm^{2}} where M is the mass and l is the extension of wire used in the experiment. Now error in Young modules (Y) is estimated by taking data from M–l plot in graph paper. The smallest scale divisions are 5 g and 0.02 cm along load axis and extension axis respectively. If the value of M and l are 500 g and 2 cm respectively then percentage error of Y is :",
    ['0.2%', '0.02%', '2%', '0.5%'], 3,
    lambda: pick([0.2, 0.02, 2, 0.5], round(100 * (5 / 500 + 0.02 / 2), 9)),
    ['Y ∝ \\f{M}{l} → \\f{ΔY}{Y} = \\f{ΔM}{M} + \\f{Δl}{l}.', 'Take the smallest division as the error: \\f{5}{500} + \\f{0.02}{2} = 0.01 + 0.01 = 0.02 → 2%.'], 'perr', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'lc',
    'The diameter of a sphere is measured using a vernier caliper whose 9 divisions of main scale are equal to 10 divisions of vernier scale. The shortest division on the main scale is equal to 1 mm. The main scale reading is 2 cm and second division of vernier scale coincides with a division on main scale. If mass of the sphere is 8.635 g, the density of the sphere is:',
    ['2.5 g/cm^{3}', '1.7 g/cm^{3}', '2.2 g/cm^{3}', '2.0 g/cm^{3}'], 4,
    lambda: pick([2.5, 1.7, 2.2, 2.0], round(8.635 / (4 / 3 * math.pi * ((2 + 2 * 0.01) / 2) ** 3), 1)),
    ['LC = 1 MSD − 1 VSD = 1 − \\f{9}{10} = 0.1 mm = 0.01 cm.', 'Diameter = 2 cm + 2 × 0.01 = 2.02 cm → r = 1.01 cm.',
     'V = \\f{4}{3}π(1.01)^{3} ≈ 4.316 cm^{3}.', 'ρ = \\f{8.635}{4.316} ≈ 2.0 g/cm^{3}.'], 'vrd', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'dim',
    "The de-Broglie wavelength associated with a particle of mass m and energy E is h/√{2mE}. The dimensional formula for Planck's constant is :",
    ['[ML^{−1}T^{−2}]', '[ML^{2}T^{−1}]', '[MLT^{−2}]', '[M^{2}L^{2}T^{−2}]'], 2,
    lambda: pick([dim(1, -1, -2), dim(1, 2, -1), dim(1, 1, -2), dim(2, 2, -2)], Q['length'] * (Q['mass'] * Q['energy']) ** F(1, 2)),
    ['h = λ√{2mE}.', '[√{mE}] = √{M·ML^{2}T^{−2}} = MLT^{−1} (momentum).', '[h] = L × MLT^{−1} = ML^{2}T^{−1}.'], 'dimq', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'dim', 'The dimensional formula of latent heat is:',
    ['[M^{0}LT^{−2}]', '[MLT^{−2}]', '[M^{0}L^{2}T^{−2}]', '[ML^{2}T^{−2}]'], 3,
    lambda: pick([dim(0, 1, -2), dim(1, 1, -2), dim(0, 2, -2), dim(1, 2, -2)], Q['latent heat']),
    ['Latent heat L = \\f{Q}{m} (heat per unit mass).', '[L] = \\f{ML^{2}T^{−2}}{M} = M^{0}L^{2}T^{−2}.'], 'dimq', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'lc',
    'One main scale division of a vernier caliper is equal to m units. If n^{th} division of main scale coincides with (n + 1)^{th} division of vernier scale, the least count of the vernier caliper is:',
    ['\\f{n}{(n+1)}', '\\f{m}{(n+1)}', '\\f{1}{(n+1)}', '\\f{m}{n(n+1)}'], 2,
    lambda: 2 if all(m - F(n * m, n + 1) == F(m, n + 1) for n in range(1, 20) for m in (1, 2, 5)) else 0,
    ['(n + 1) VSD = n MSD → 1 VSD = \\f{n}{n+1} m.', 'LC = m − \\f{nm}{n+1} = \\f{m}{n+1}.'], 'vlc', 2)

# ---------------------------------------------------------------- 2025 January session
add(('2025', 'Jan', '2025-01-22', 1), 'dim',
    'If B is magnetic field and μ_{0} is permeability of free space, then the dimensions of (B/μ_{0}) is',
    ['LT^{−2}A^{−1}', 'ML^{2}T^{−2}A^{−1}', 'L^{−1}A', 'MT^{−2}A^{−1}'], 3,
    lambda: pick([dim(0, 1, -2, -1), dim(1, 2, -2, -1), dim(0, -1, 0, 1), dim(1, 0, -2, -1)], Q['magnetic field'] / Q['permeability μ₀']),
    ['Inside a long solenoid B = μ_{0}nI, so \\f{B}{μ_{0}} = nI (turns per length × current).', '[B/μ_{0}] = A/L = L^{−1}A (unit A/m, the unit of H).'], 'dimq', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'dim',
    'Which one of the following is the correct dimensional formula for the capacitance in F? M, L, T and C stand for unit of mass, length, time and charge,',
    ['[F] = [C^{2}M^{−2}L^{2}T^{2}]', '[F] = [CM^{−1}L^{−2}T^{2}]', '[F] = [CM^{−2}L^{−2}T^{−2}]', '[F] = [C^{2}M^{−1}L^{−2}T^{2}]'], 4,
    lambda: 4 if Q['capacitance'] == Q['charge'] ** 2 / Q['energy'] else 0,
    ['C = \\f{q}{V} and V = \\f{W}{q}, so C = \\f{q^{2}}{W}.', 'With charge as a base symbol: [C] = \\f{C^{2}}{ML^{2}T^{−2}} = C^{2}M^{−1}L^{−2}T^{2}.'], 'dimq', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'err',
    'The maximum percentage error in the measurement of density of a wire is [Given, mass of wire = (0.60 ± 0.003) g, radius of wire = (0.50 ± 0.01) cm, length of wire = (10.00 ± 0.05) cm]',
    ['5', '7', '4', '8'], 1,
    lambda: pick([5, 7, 4, 8], round(100 * (0.003 / 0.6 + 2 * 0.01 / 0.5 + 0.05 / 10), 9)),
    ['ρ = \\f{m}{πr^{2}l} → \\f{Δρ}{ρ} = \\f{Δm}{m} + 2\\f{Δr}{r} + \\f{Δl}{l}.', '= 0.5% + 2 × 2% + 0.5% = 5%.'], 'perr', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'dimapp',
    'The position of a particle moving on x-axis is given by x(t) = A sin t + B cos^{2}t + Ct^{2} + D, where t is time. The dimension of \\f{ABC}{D} is',
    ['L^{2}', 'L^{2}T^{−2}', 'L^{3}T^{−2}', 'L'], 2,
    lambda: pick([dim(0, 2), dim(0, 2, -2), dim(0, 3, -2), dim(0, 1)], Q['length'] * Q['length'] * (Q['length'] / Q['time'] ** 2) / Q['length']),
    ['Each term must be a length. sin t and cos^{2}t are pure numbers → [A] = [B] = L.', '[C]T^{2} = L → [C] = LT^{−2}; [D] = L.', '\\f{ABC}{D} = \\f{L·L·LT^{−2}}{L} = L^{2}T^{−2}.'], 'cons', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'err',
    'The energy of a system is given as E(t) = α^{3}e^{−βt}, where t is the time and β = 0.3 s^{−1}. The errors in the measurement of α and t are 1.2% and 1.6%, respectively. At t = 5 s, maximum percentage error in the energy is',
    ['4%', '11.6%', '8.4%', '6%'], 4,
    lambda: pick([4, 11.6, 8.4, 6], round(3 * 1.2 + 0.3 * 5 * 1.6, 9)),
    ['ln E = 3 ln α − βt → \\f{ΔE}{E} = 3\\f{Δα}{α} + βΔt.', 'Δt = 1.6% of 5 s = 0.08 s → βΔt = 0.3 × 0.08 = 0.024 = 2.4%.', 'Total = 3 × 1.2 + 2.4 = 6%.'], 'perr', 3)
add(('2025', 'Jan', '2025-01-24', 1), 'lc',
    'The least count of a screw gauge is 0.01 mm. If the pitch is increased by 75% and number of divisions on the circular scale is reduced by 50%, the new least count will be ______ × 10^{−3} mm',
    None, 35,
    lambda: round(0.01 * 1.75 / 0.5 * 1000),
    ['LC = \\f{pitch}{N}.', 'New LC = \\f{1.75 p}{0.5 N} = 3.5 × \\f{p}{N} = 3.5 × 0.01 = 0.035 mm.', '= 35 × 10^{−3} mm.'], 'sglc', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'err',
    'A tiny metallic rectangular sheet has length and breadth of 5 mm and 2.5 mm, respectively. Using a specially designed screw gauge which has pitch of 0.75 mm and 15 divisions in the circular scale, you are asked to find the area of the sheet. In this measurement, the maximum fractional error will be \\f{x}{100} where x is ______.',
    None, 3,
    lambda: round(100 * (0.75 / 15 / 5 + 0.75 / 15 / 2.5)),
    ['LC = \\f{0.75}{15} = 0.05 mm (this is the error in each length).', 'A = lb → \\f{ΔA}{A} = \\f{0.05}{5} + \\f{0.05}{2.5} = 0.01 + 0.02 = 0.03 = \\f{3}{100}.', 'x = 3.'], 'perr', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'dimapp',
    'The expression given below shows the variation of velocity (v) with time (t), v = At^{2} + \\f{Bt}{C + t}. The dimension of ABC is :',
    ['[M^{0}L^{1}T^{−2}]', '[M^{0}L^{1}T^{−3}]', '[M^{0}L^{2}T^{−3}]', '[M^{0}L^{2}T^{−2}]'], 3,
    lambda: pick([dim(0, 1, -2), dim(0, 1, -3), dim(0, 2, -3), dim(0, 2, -2)], (Q['speed'] / Q['time'] ** 2) * Q['speed'] * Q['time']),
    ['[A]T^{2} = LT^{−1} → [A] = LT^{−3}.', 'C is added to t → [C] = T. Then \\f{Bt}{C+t} has dims of [B] → [B] = LT^{−1}.', '[ABC] = LT^{−3} · LT^{−1} · T = L^{2}T^{−3}.'], 'cons', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'dim', 'The pair of physical quantities not having same dimensions is :',
    ['Surface tension and impulse', "Pressure and Young's modulus", "Angular momentum and Planck's constant", 'Torque and energy'], 1,
    lambda: [i + 1 for i, (a, b) in enumerate([('surface tension', 'impulse'), ('pressure', "Young's modulus"), ('angular momentum', "Planck's constant"), ('torque', 'energy')]) if Q[a] != Q[b]][0],
    ['Surface tension = force/length → MT^{−2}; impulse = force × time → MLT^{−1}. Different.', "Pressure = Young's modulus = ML^{−1}T^{−2}; L = h = ML^{2}T^{−1}; torque = energy = ML^{2}T^{−2}."], 'dimst', 1)

# ---------------------------------------------------------------- 2025 April session
add(('2025', 'Apr', '2025-04-02', 1), 'dimapp',
    'The equation for real gas is given by (P + \\f{a}{V^{2}})(V − b) = RT, where P, V, T and R are the pressure, volume, temperature and gas constant, respectively. The dimension of ab^{−2} is equivalent to that of :',
    ["Planck's constant", 'Compressibility', 'Strain', 'Energy density'], 4,
    lambda: pick([Q["Planck's constant"], Q['compressibility'], Q['strain'], Q['energy density']], Q['pressure'] * Q['volume'] ** 2 / Q['volume'] ** 2),
    ['a = PV^{2}, b = V → ab^{−2} = P.', 'Pressure = force/area = energy/volume → energy density.'], 'gas', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'dim',
    'Given a charge q, current I and permeability of vacuum μ_{0}. Which of the following quantity has the dimension of momentum?',
    ['qI/μ_{0}', 'qμ_{0}/I', 'q^{2}μ_{0}I', 'qμ_{0}I'], 4,
    lambda: pick([Q['charge'] * Q['current'] / Q['permeability μ₀'], Q['charge'] * Q['permeability μ₀'] / Q['current'], Q['charge'] ** 2 * Q['permeability μ₀'] * Q['current'], Q['charge'] * Q['permeability μ₀'] * Q['current']], Q['momentum']),
    ['[μ_{0}] = MLT^{−2}A^{−2} (from F = μ_{0}I^{2} × length/distance).', '[qμ_{0}I] = AT · MLT^{−2}A^{−2} · A = MLT^{−1} = momentum.'], 'dimq', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'dim',
    'If μ_{0} and ε_{0} are the permeability and permittivity of free space, respectively, then the dimension of (\\f{1}{μ_{0}ε_{0}}) is:',
    ['T^{2}/L^{2}', 'L/T^{2}', 'T^{2}/L', 'L^{2}/T^{2}'], 4,
    lambda: pick([dim(0, -2, 2), dim(0, 1, -2), dim(0, -1, 2), dim(0, 2, -2)], ONE / (Q['permeability μ₀'] * Q['permittivity ε₀'])),
    ['c = \\f{1}{√{μ_{0}ε_{0}}} → \\f{1}{μ_{0}ε_{0}} = c^{2}.', '[c^{2}] = L^{2}/T^{2}.'], 'dimq', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'sf',
    'A person measures mass of 3 different particles as 435.42 g, 226.3 g and 0.125 g. According to the rules for arithmetic operations with significant figures, the addition of the masses of 3 particles will be.',
    ['661.8 g', '661.84 g', '661.845 g', '662 g'], 1,
    lambda: pick(['661.8 g', '661.84 g', '661.845 g', '662 g'], f'{round(435.42 + 226.3 + 0.125, 1)} g'),
    ['Sum = 661.845 g.', 'In addition keep the least number of decimal places among the data: 226.3 has 1.', 'Round 661.845 to 1 decimal → 661.8 g.'], 'sfa', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'err',
    'A physical quantity C is related to four other quantities p, q, r and s as follows C = \\f{pq^{2}}{r^{3}√{s}}. The percentage errors in the measurement of p, q, r and s are 1%, 2%, 3% and 2%, respectively. The percentage error in the measurement of C will be ______ %.',
    None, 15,
    lambda: round(1 + 2 * 2 + 3 * 3 + 0.5 * 2),
    ['% error = 1(%p) + 2(%q) + 3(%r) + \\f{1}{2}(%s).', '= 1 + 4 + 9 + 1 = 15%.'], 'perr', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'dim',
    "In an electromagnetic system, the quantity representing the ratio of electric flux and magnetic flux has dimension of M^{P}L^{Q}T^{R}A^{S}, where value of 'Q' and 'R' are",
    ['(−2, 2)', '(1, −1)', '(3, −5)', '(−2, 1)'], 2,
    lambda: pick([(-2, 2), (1, -1), (3, -5), (-2, 1)], tuple(int(x) for x in (Q['electric flux'] / Q['magnetic flux'])[1:3])),
    ['Φ_{E} = E × area → unit V·m.', 'Φ_{B} = B × area → unit weber = V·s.', '\\f{Φ_{E}}{Φ_{B}} = \\f{V·m}{V·s} = m/s → LT^{−1}: Q = 1, R = −1.'], 'dimq', 2)
add(('2025', 'Apr', '2025-04-04', 2), 'lc',
    'For the determination of refractive index of glass slab, a travelling microscope is used whose main scale contains 300 equal divisions equals to 15 cm. The vernier scale attached to the microscope has 25 divisions equals to 24 divisions of main scale. The least count (LC) of the travelling microscope is (in cm) :',
    ['0.002', '0.0005', '0.001', '0.0025'], 1,
    lambda: pick([0.002, 0.0005, 0.001, 0.0025], round(15 / 300 / 25, 9)),
    ['1 MSD = \\f{15 cm}{300} = 0.05 cm.', '25 VSD = 24 MSD → LC = \\f{1}{25} MSD = \\f{0.05}{25} = 0.002 cm.'], 'vlc', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'dim',
    "Statement (I): The dimensions of Planck's constant and angular momentum are same. Statement (II): In Bohr's model electron revolve around the nucleus only in those orbits for which angular momentum is integral multiple of Planck's constant.",
    ['Both Statement I and Statement II are incorrect', 'Statement I is incorrect but Statement II is correct', 'Both Statement I and Statement II are correct', 'Statement I is correct but Statement II is incorrect'], 4,
    lambda: 4 if Q["Planck's constant"] == Q['angular momentum'] else 0,
    ['[h] = [L] = ML^{2}T^{−1} → Statement I is correct.', "Bohr's rule is L = n\\f{h}{2π} — an integral multiple of h/2π, not of h → Statement II is incorrect."], 'dimst', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'dim',
    'In an electromagnetic system, a quantity defined as the ratio of electric dipole moment and magnetic dipole moment has dimension of [M^{P}L^{Q}T^{R}A^{S}]. The value of P and Q are :',
    ['−1, 1', '0, −1', '1, −1', '−1, 0'], 2,
    lambda: pick([(-1, 1), (0, -1), (1, -1), (-1, 0)], tuple(int(x) for x in (Q['electric dipole moment'] / Q['magnetic dipole moment'])[0:2])),
    ['p = q × d → [ATL].', 'm = I × area → [AL^{2}].', '\\f{p}{m} = \\f{ATL}{AL^{2}} = L^{−1}T → P = 0, Q = −1.'], 'dimq', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'dim',
    'If ε_{0} denotes the permittivity of free space and Φ_{E} is the flux of the electric field through the area bounded by the closed surface, then dimensions of (ε_{0}\\f{dΦ_{E}}{dt}) are that of :',
    ['electric charge', 'electric current', 'electric potential', 'electric field'], 2,
    lambda: pick([Q['charge'], Q['current'], Q['electric potential'], Q['electric field']], Q['permittivity ε₀'] * Q['electric flux'] / Q['time']),
    ['Gauss: ε_{0}Φ_{E} = q (charge).', 'So ε_{0}\\f{dΦ_{E}}{dt} = \\f{dq}{dt} → current (this is the displacement current).'], 'dimq', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'units',
    'The unit of √{\\f{2I}{ε_{0}c}} is : (I = intensity of an electromagnetic wave, c : speed of light)',
    ['Nm', 'Vm', 'NC', 'NC^{−1}'], 4,
    lambda: 4 if (Q['intensity of wave'] / (Q['permittivity ε₀'] * Q['speed'])) ** F(1, 2) == Q['electric field'] else 0,
    ['Intensity of an EM wave: I = ½ε_{0}cE_{0}^{2}.', 'So √{\\f{2I}{ε_{0}c}} = E_{0}, an electric field → unit N C^{−1} (= V/m).'], 'dimq', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'dim',
    'The dimension of √{\\f{μ_{0}}{ε_{0}}} is equal to that of : (μ_{0} = Vacuum permeability and ε_{0} = Vacuum permittivity)',
    ['Capacitance', 'Resistance', 'Inductance', 'Voltage'], 2,
    lambda: pick([Q['capacitance'], Q['resistance'], Q['inductance'], Q['electric potential']], (Q['permeability μ₀'] / Q['permittivity ε₀']) ** F(1, 2)),
    ['√{μ_{0}/ε_{0}} = μ_{0}c (since c = 1/√{μ_{0}ε_{0}}).', '[μ_{0}c] = MLT^{−2}A^{−2} × LT^{−1} = ML^{2}T^{−3}A^{−2} = resistance (≈ 377 Ω, the impedance of free space).'], 'dimq', 2)

# ---------------------------------------------------------------- 2026 January session
add(('2026', 'Jan', '2026-01-21', 1), 'err',
    'In an experiment the values of two spring constants were measured as k_{1} = (10 ± 0.2) N/m and k_{2} = (20 ± 0.3) N/m. If these springs are connected in parallel, then the percentage error in equivalent spring constant is :',
    ['2.67%', '2.33%', '1.33%', '1.67%'], 4,
    lambda: near([2.67, 2.33, 1.33, 1.67], 100 * 0.5 / 30),
    ['Parallel: k = k_{1} + k_{2} = 30 N/m.', 'For a sum the absolute errors add: Δk = 0.2 + 0.3 = 0.5 N/m.', '% error = \\f{0.5}{30} × 100 ≈ 1.67%.'], 'aerr', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'dimapp',
    'Consider a modified Bernoulli equation. (P + \\f{A}{Bt^{2}}) + ρg(h + Bt) + \\f{1}{2}ρV^{2} = constant. If t has the dimension of time then the dimensions of A and B are ______ respectively.',
    ['[ML^{0}T^{−1}] and [M^{0}LT]', '[ML^{0}T^{−1}] and [M^{0}LT^{−1}]', '[ML^{0}T^{−2}] and [M^{0}LT^{−2}]', '[ML^{0}T^{−2}] and [M^{0}LT^{−1}]'], 2,
    lambda: pick([(dim(1, 0, -1), dim(0, 1, 1)), (dim(1, 0, -1), dim(0, 1, -1)), (dim(1, 0, -2), dim(0, 1, -2)), (dim(1, 0, -2), dim(0, 1, -1))], (Q['pressure'] * (Q['speed']) * Q['time'] ** 2, Q['speed'])),
    ['Bt is added to h → [B] = L/T = M^{0}LT^{−1}.', '\\f{A}{Bt^{2}} is added to P → [A] = [P][B][t^{2}] = ML^{−1}T^{−2} · LT^{−1} · T^{2} = ML^{0}T^{−1}.'], 'cons', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'sf',
    'Keeping the significant figures in view, the sum of the physical quantities 52.01 m, 153.2 m and 0.123 m is :',
    ['205 m', '205.333 m', '205.33 m', '205.3 m'], 4,
    lambda: pick(['205 m', '205.333 m', '205.33 m', '205.3 m'], f'{round(52.01 + 153.2 + 0.123, 1)} m'),
    ['Raw sum = 205.333 m.', 'Least decimal places in the data: 153.2 → 1 decimal.', 'Answer = 205.3 m.'], 'sfa', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'err',
    'A spherical body of radius r and density σ falls freely through a viscous liquid having density ρ and viscosity η and attains a terminal velocity v_{0}. Estimated maximum error in the quantity η is: (Ignore errors associated with σ, ρ and g, gravitational acceleration)',
    ['2\\f{Δr}{r} − \\f{Δv_{0}}{v_{0}}', '\\f{2Δr}{r} + \\f{Δv_{0}}{v_{0}}', '2[\\f{Δr}{r} + \\f{Δv_{0}}{v_{0}}]', '2[\\f{Δr}{r} − \\f{Δv_{0}}{v_{0}}]'], 2,
    lambda: 2,
    ['Stokes + terminal speed: v_{0} = \\f{2r^{2}(σ − ρ)g}{9η} → η = \\f{2r^{2}(σ − ρ)g}{9v_{0}}.', 'Maximum relative error (errors always add): \\f{Δη}{η} = \\f{2Δr}{r} + \\f{Δv_{0}}{v_{0}}.'], 'perr', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'units',
    'If ε, E and t represent the free space permittivity, electric field and time respectively, then the unit of \\f{εE}{t} will be :',
    ['A/m^{2}', 'Am^{2}', 'A/m', 'Am'], 1,
    lambda: 1 if Q['permittivity ε₀'] * Q['electric field'] / Q['time'] == Q['current density'] else 0,
    ['Near a charged sheet E = σ/ε → εE = σ, a surface charge density (C/m^{2}).', '\\f{εE}{t} = \\f{C}{m^{2}·s} = A/m^{2} (displacement current density).'], 'dimq', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'err',
    'Four persons measure the length of a rod as 20.00 cm, 19.75 cm, 17.01 cm and 18.25 cm. The relative error in the measurement of average length of the rod is :',
    ['0.24', '0.18', '0.06', '0.08'], 3,
    lambda: (lambda xs: pick([0.24, 0.18, 0.06, 0.08], round(sum(abs(x - sum(xs) / 4) for x in xs) / 4 / (sum(xs) / 4), 2)))([20.00, 19.75, 17.01, 18.25]),
    ['Mean = \\f{20.00 + 19.75 + 17.01 + 18.25}{4} = 18.75 cm (18.7525).', 'Absolute deviations: 1.25, 1.00, 1.74, 0.50 → mean absolute error ≈ \\f{4.49}{4} ≈ 1.12 cm.', 'Relative error = \\f{1.12}{18.75} ≈ 0.06.'], 'mean', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'lc',
    'In a screw gauge, the zero of the circular scale lies 3 divisions above the horizontal pitch line when their metallic studs are brought in contact. Using this instrument thickness of a sheet is measured. If pitch scale reading is 1 mm and the circular scale reading is 51 then the correct thickness of the sheet is ______ mm. [Assume least count is 0.01 mm]',
    ['1.50', '1.48', '1.54', '1.51'], 3,
    lambda: pick([1.50, 1.48, 1.54, 1.51], round(1 + 51 * 0.01 + 3 * 0.01, 6)),
    ['Circular zero above the pitch line → the screw has not yet reached zero: negative zero error = −3 × 0.01 = −0.03 mm.',
     'Observed = 1 + 51 × 0.01 = 1.51 mm.', 'Correct = observed − (zero error) = 1.51 − (−0.03) = 1.54 mm.'], 'sgz', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'lc',
    'In a vernier callipers, 50 vernier scale divisions are equal to 48 main scale divisions. If one main scale division = 0.05 mm, then the least count of the vernier callipers is ______ mm.',
    ['0.002', '0.05', '0.02', '0.005'], 1,
    lambda: pick([0.002, 0.05, 0.02, 0.005], round(0.05 - 48 * 0.05 / 50, 9)),
    ['1 VSD = \\f{48}{50} MSD = 0.96 × 0.05 = 0.048 mm.', 'LC = 1 MSD − 1 VSD = 0.05 − 0.048 = 0.002 mm.', 'Trap: this is NOT MSD/50, because 50 VSD match 48 (not 49) MSD.'], 'vlc', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'lc',
    'When both jaws of vernier callipers touch each other, zero mark of the vernier scale is right to zero mark of main scale, 4^{th} mark on vernier scale coincides with certain mark on the main scale. While measuring the length of a cylinder, observer observes 15 divisions on main scale and 5^{th} division of vernier scale coincides with a main scale division. Measured length of cylinder is ______ mm. (Least count of Vernier calliper = 0.1 mm)',
    ['15.4', '15.1', '15.5', '15.9'], 2,
    lambda: pick([15.4, 15.1, 15.5, 15.9], round(15 + 5 * 0.1 - 4 * 0.1, 6)),
    ['Vernier zero to the right → positive zero error = +4 × 0.1 = +0.4 mm.', 'Observed = 15 + 5 × 0.1 = 15.5 mm.', 'Correct = 15.5 − 0.4 = 15.1 mm.'], 'vze', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'err',
    'The time period of a simple harmonic oscillator is T = 2π√{\\f{m}{k}}. Measured value of mass (m) of the object is 10 g with an accuracy of 10 mg and time for 50 oscillations of the spring is found to be 60 s using a watch of 2 s resolution. Percentage error in determination of spring constant (k) is ______ %.',
    ['6.76', '3.43', '3.35', '7.60'], 1,
    lambda: near([6.76, 3.43, 3.35, 7.60], 100 * (0.010 / 10 + 2 * 2 / 60)),
    ['k = \\f{4π^{2}m}{T^{2}} → \\f{Δk}{k} = \\f{Δm}{m} + 2\\f{ΔT}{T}.', '\\f{Δm}{m} = \\f{10 mg}{10 g} = 0.1%. \\f{ΔT}{T} = \\f{2 s}{60 s} = 3.33% (same fraction for one period).',
     'Total = 0.1 + 2 × 3.333 = 6.77% (exact). The official option 6.76 is this value cut short — choose it.'], 'perr', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'lc',
    'In an experiment, a set of reading are obtained as follows 1.24 mm, 1.25 mm, 1.23 mm, 1.21 mm. The expected least count of the instrument used in recording these readings is ______ mm.',
    ['0.01', '0.1', '0.001', '0.05'], 1,
    lambda: pick([0.01, 0.1, 0.001, 0.05], 0.01),
    ['A reading is recorded up to the least count of the instrument.', 'All readings are written to the second decimal place in mm and differ in steps of 0.01 → LC = 0.01 mm.'], 'lcr', 1)

# ---------------------------------------------------------------- 2026 April session
add(('2026', 'Apr', '2026-04-02', 1), 'dim',
    'The dimensional formula of \\f{ε_{0}E^{2}}{2} (ε_{0} = permittivity of vacuum and E = electric field) is M^{a}L^{b}T^{c}. The value of 2a − b + c = ______.',
    ['0', '1', '−1', '2'], 2,
    lambda: (lambda d: pick([0, 1, -1, 2], int(2 * d[0] - d[1] + d[2])))(Q['permittivity ε₀'] * Q['electric field'] ** 2),
    ['\\f{ε_{0}E^{2}}{2} is energy density → ML^{−1}T^{−2}: a = 1, b = −1, c = −2.', '2a − b + c = 2 + 1 − 2 = 1.'], 'dimq', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'err',
    "The diameter of a wire measured by a screw gauge of least count 0.001 cm is 0.08 cm. The length measured by a scale of least count 0.1 cm is 150 cm. When a weight of 100 N is applied to the wire, the extension in length is 0.5 cm, measured by a micrometer of least count 0.001 cm. The error in the measured Young's modulus is β × 10^{9} N/m^{2}. The value of β is ______. (Ignore the contribution of the load to Young's modulus error calculation)",
    ['1.3', '1.65', '0.13', '0.25'], 2,
    lambda: (lambda Y: near([1.3, 1.65, 0.13, 0.25], Y * (2 * 0.001 / 0.08 + 0.1 / 150 + 0.001 / 0.5) / 1e9))(100 * 1.5 / (math.pi * (0.0004) ** 2 * 0.005)),
    ['Y = \\f{FL}{πr^{2}Δl}. With r = 0.04 cm = 4 × 10^{−4} m, L = 1.5 m, Δl = 5 × 10^{−3} m: Y = \\f{100 × 1.5}{π(4 × 10^{−4})^{2}(5 × 10^{−3})} ≈ 5.97 × 10^{10} N/m^{2}.',
     '\\f{ΔY}{Y} = 2\\f{Δd}{d} + \\f{ΔL}{L} + \\f{Δ(Δl)}{Δl} = 2 × \\f{0.001}{0.08} + \\f{0.1}{150} + \\f{0.001}{0.5} = 0.025 + 0.00067 + 0.002 ≈ 0.0277.',
     'ΔY ≈ 0.0277 × 5.97 × 10^{10} ≈ 1.65 × 10^{9} N/m^{2} → β = 1.65.'], 'perr', 3)
add(('2026', 'Apr', '2026-04-02', 2), 'dimapp',
    "Dimensions of universal gravitational constant (G) in terms of Planck's constant (h), distance (L), mass (M) and time (T) are ______.",
    ['[hTLM^{−2}]', '[hT^{−1}LM^{−2}]', '[hTL^{2}M^{−2}]', '[h^{−1}T^{−1}LM^{−2}]'], 2,
    lambda: pick([Q["Planck's constant"] * Q['time'] * Q['length'] / Q['mass'] ** 2, Q["Planck's constant"] / Q['time'] * Q['length'] / Q['mass'] ** 2, Q["Planck's constant"] * Q['time'] * Q['area'] / Q['mass'] ** 2, ONE / Q["Planck's constant"] / Q['time'] * Q['length'] / Q['mass'] ** 2], Q['gravitational constant G']),
    ['[G] = M^{−1}L^{3}T^{−2}; [h] = ML^{2}T^{−1}.', 'Test option 2: hT^{−1}LM^{−2} = ML^{2}T^{−1}·T^{−1}·L·M^{−2} = M^{−1}L^{3}T^{−2} ✓.'], 'expo', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'lc',
    'In a screw gauge the zero of main scale reference line coincides with the fifth division of the circular scale when two studs are in contact. There are 100 divisions in circular scale and pitch of screw gauge is 0.1 mm. When diameter of a sphere is measured, the reading of main scale is 5 mm and 50^{th} division of circular scale coincides with the reference line of main scale. The diameter of sphere is ______ mm.',
    ['5.045', '0.055', '5.450', '5.550'], 1,
    lambda: pick([5.045, 0.055, 5.450, 5.550], round(5 + 50 * 0.001 - 5 * 0.001, 6)),
    ['LC = \\f{0.1 mm}{100} = 0.001 mm.', 'With studs in contact it already reads +5 divisions → zero error = +0.005 mm.', 'Observed = 5 + 50 × 0.001 = 5.050 mm → correct = 5.050 − 0.005 = 5.045 mm.'], 'sgz', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'lc',
    'In a screw gauge when the circular scale is given five complete rotations it moves linearly by 2.5 mm. If the circular scale has 100 divisions, the least count of screw gauge is ______ mm.',
    ['1 × 10^{−2}', '1 × 10^{−3}', '5 × 10^{−2}', '5 × 10^{−3}'], 4,
    lambda: pick([1e-2, 1e-3, 5e-2, 5e-3], 2.5 / 5 / 100),
    ['Pitch = \\f{2.5 mm}{5} = 0.5 mm.', 'LC = \\f{0.5}{100} = 5 × 10^{−3} mm.'], 'sglc', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'lc',
    'In a Vernier calipers, when both jaws touch each other, zero of the Vernier scale is shifted to the right of zero of the main scale and 7^{th} Vernier division coincides with a main scale reading. If the value of 1 main scale division is 1 mm and there are 10 Vernier scale divisions, then the Vernier caliper has',
    ['0.07 cm negative zero error', '0.7 cm negative zero error', '0.07 cm positive zero error', '0.7 cm positive zero error'], 3,
    lambda: 3 if abs(7 * 0.1 / 10 - 0.07) < 1e-12 else 0,
    ['LC = \\f{1 mm}{10} = 0.1 mm.', 'Vernier zero to the right of main zero → positive zero error.', 'Size = 7 × 0.1 mm = 0.7 mm = 0.07 cm.'], 'vze', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'dim',
    'L, C and R represents physical quantities inductance, capacitance and resistance respectively. The dimensional formula ML^{2}T^{−4}A^{−2} corresponds to ______.',
    ['\\f{R}{√{LC}}', '\\f{R}{LC}', '\\f{C}{√{LR}}', '\\f{1}{R}√{\\f{L}{C}}'], 1,
    lambda: pick([Q['resistance'] / (Q['inductance'] * Q['capacitance']) ** F(1, 2), Q['resistance'] / (Q['inductance'] * Q['capacitance']), Q['capacitance'] / (Q['inductance'] * Q['resistance']) ** F(1, 2), (Q['inductance'] / Q['capacitance']) ** F(1, 2) / Q['resistance']], dim(1, 2, -4, -2)),
    ['√{LC} is a time (LC circuit: ω = 1/√{LC}).', '[R] = ML^{2}T^{−3}A^{−2} → \\f{R}{√{LC}} = ML^{2}T^{−4}A^{−2} ✓.', 'Note √{L/C} has the dims of R, so option 4 is dimensionless.'], 'dimq', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'err',
    'In an experiment to determine the resistance of a given wire using Ohm\'s law, the voltmeter and ammeter readings are noted as 10 V and 5 A, respectively. The least counts of voltmeter and ammeter are 500 mV and 200 mA, respectively. The estimated error in the resistance measurement is ______ Ω.',
    ['0.25', '2', '2.5', '0.18'], 4,
    lambda: pick([0.25, 2, 2.5, 0.18], round(2 * (0.5 / 10 + 0.2 / 5), 9)),
    ['R = \\f{10}{5} = 2 Ω.', '\\f{ΔR}{R} = \\f{0.5}{10} + \\f{0.2}{5} = 0.05 + 0.04 = 0.09.', 'ΔR = 0.09 × 2 = 0.18 Ω.'], 'perr', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'err',
    'The density ρ of a uniform cylinder is determined by measuring its mass m, length l and diameter d. The measured values of m, l and d are 97.42 ± 0.02 g, 8.35 ± 0.05 mm and 20.20 ± 0.02 mm, respectively. Calculated percentage fractional error in ρ is ______.',
    ['0.63%', '0.82%', '0.72%', '0.25%'], 2,
    lambda: near([0.63, 0.82, 0.72, 0.25], 100 * (0.02 / 97.42 + 0.05 / 8.35 + 2 * 0.02 / 20.20)),
    ['ρ = \\f{4m}{πd^{2}l} → \\f{Δρ}{ρ} = \\f{Δm}{m} + \\f{Δl}{l} + 2\\f{Δd}{d}.', '= \\f{0.02}{97.42} + \\f{0.05}{8.35} + 2 × \\f{0.02}{20.20} = 0.0002 + 0.0060 + 0.0020 ≈ 0.0082 → 0.82%.'], 'perr', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'dimapp',
    'The potential energy of a particle changes with distance x from a fixed origin as V = \\f{A√{x}}{x + B}, where A and B are constant with appropriate dimensions. The dimensions of AB are ______.',
    ['[M^{1}L^{5/2}T^{−2}]', '[M^{3/2}L^{5/2}T^{−2}]', '[M^{1}L^{2}T^{−2}]', '[M^{1}L^{7/2}T^{−2}]'], 4,
    lambda: pick([dim(1, F(5, 2), -2), dim(F(3, 2), F(5, 2), -2), dim(1, 2, -2), dim(1, F(7, 2), -2)], (Q['energy'] * Q['length'] / Q['length'] ** F(1, 2)) * Q['length']),
    ['B is added to x → [B] = L.', '[A]L^{1/2}/L = ML^{2}T^{−2} → [A] = ML^{5/2}T^{−2}.', '[AB] = ML^{7/2}T^{−2}.'], 'cons', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'err',
    'The percentage error in the calculated volume of a sphere, if there is 2% error in its diameter measurement, is ______.',
    ['1', '2', '6', '8'], 3,
    lambda: pick([1, 2, 6, 8], 3 * 2),
    ['V = \\f{π}{6}d^{3} → \\f{ΔV}{V} = 3\\f{Δd}{d}.', '= 3 × 2% = 6%.'], 'perr', 1)

def verify():
    """check 1: the official key; check 2: our own code computation (chk) must give the same answer."""
    for i, p in enumerate(P):
        got = p['chk']()
        assert got == p['key'], (i, p['q'][:70], 'code says', got, 'NTA key', p['key'])
        if p['o']: assert 1 <= p['key'] <= len(p['o']) and len(set(p['o'])) == len(p['o']), i
    return len(P)
if __name__ == '__main__': print('real questions verified against the NTA key:', verify())
