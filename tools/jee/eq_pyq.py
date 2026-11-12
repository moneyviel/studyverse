"""Real JEE Main questions — Chemistry Unit 6: Equilibrium. Our own solutions; chk re-solves each one numerically
(ICE tables solved by bisection, exact charge balance for pH, Henderson–Hasselbalch checked against mole counts).
Skipped: graph-only items, items whose key we could not reproduce (03-04-25 S1 Q17, 05-04-24 S2 Q6, 06-04-26 S1 Q58),
and electrochemistry/thermodynamics items that belong to other units."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
def bis(f, lo, hi, n=300):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
def weak_acid_H(c, Ka, Kw=1e-14):   # exact: [H+] from charge balance h = Ka c/(Ka + h) + Kw/h
    return bis(lambda h: h - Ka * c / (Ka + h) - Kw / h, 1e-14, 1.0)
ST4 = ['Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']

# ---------------- K, Kp, Kc ----------------
add(('2024', 'Apr', '2024-04-04', 2), 'gas', 'The equilibrium constant for the reaction SO_{3}(g) ⇌ SO_{2}(g) + \\f{1}{2}O_{2}(g) is K_{c} = 4.9 × 10^{−2}. The value of K_{c} for the reaction given below is 2SO_{2}(g) + O_{2}(g) ⇌ 2SO_{3}(g) is',
    ['4.9', '41.6', '49', '416'], 4, lambda: near([4.9, 41.6, 49, 416], (1 / 4.9e-2) ** 2), ['Reverse → \\f{1}{K}; double the equation → square it.', 'K = (\\f{1}{0.049})^{2} ≈ 416.'], 'kp', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'gas', 'For the given hypothetical reactions, the equilibrium constants are as follows: X ⇌ Y; K_{1} = 1.0, Y ⇌ Z; K_{2} = 2.0, Z ⇌ W; K_{3} = 4.0. The equilibrium constant for the reaction X ⇌ W is',
    ['6.0', '12.0', '8.0', '7.0'], 3, lambda: pick([6, 12, 8, 7], 1.0 * 2.0 * 4.0), ['Adding reactions multiplies K: 1 × 2 × 4 = 8.'], 'kp', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'gas', 'At T(K), the equilibrium constant of A_{2}(g) + B_{2}(g) ⇌ C(g) is 2.7 × 10^{−5}. What is the equilibrium constant for \\f{1}{3}A_{2}(g) + \\f{1}{3}B_{2}(g) ⇌ \\f{1}{3}C(g) at the same temperature?',
    ['(2.7 × 10^{−5})^{3}', '6 × 10^{−2}', '√{2.7 × 10^{−5}}', '3 × 10^{−2}'], 4, lambda: near([2e-14, 6e-2, 5.2e-3, 3e-2], (2.7e-5) ** (1 / 3)), ['Multiplying an equation by n raises K to the power n.', 'K^{1/3} = (27 × 10^{−6})^{1/3} = 3 × 10^{−2}.'], 'kp', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'gas', 'Consider the general reaction given below at 400 K: xA(g) ⇌ yB(g). The values of K_{p} and K_{c} are studied under the same condition of temperature but variation in x and y. (i) K_{p} = 85.87 and K_{c} = 2.586 appropriate units (ii) K_{p} = 0.862 and K_{c} = 28.62 appropriate units. The values of x and y in (i) and (ii) respectively are :',
    ['(i) 3,1; (ii) 3, 1', '(i) 4, 1; (ii) 4, 1', '(i) 1,3; (ii) 2, 1', '(i) 1,2; (ii) 2, 1'], 4,
    lambda: (lambda d1, d2: 4 if (d1, d2) == (1, -1) else 0)(round(math.log(85.87 / 2.586) / math.log(0.0821 * 400)), round(math.log(0.862 / 28.62) / math.log(0.0821 * 400))),
    ['K_{p} = K_{c}(RT)^{Δn}, RT = 0.0821 × 400 ≈ 32.8.', '(i) K_{p}/K_{c} ≈ 33 → Δn = +1 → x = 1, y = 2. (ii) ratio ≈ \\f{1}{33} → Δn = −1 → x = 2, y = 1.'], 'kp', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'gas', 'At −20 °C and 1 atm pressure, a cylinder is filled with equal number of H_{2}, I_{2} and HI molecules for the reaction H_{2}(g) + I_{2}(g) ⇌ 2HI(g), the K_{P} for the process is x × 10^{−1}. x = [Given : R = 0.082 L atm K^{−1} mol^{−1}]',
    ['2', '1', '10', '0.01'], 3, lambda: pick([2, 1, 10, 0.01], round((1 / 3) ** 2 / ((1 / 3) * (1 / 3)) * 10, 9)), ['Equal partial pressures p each: K_{p} = \\f{p^{2}}{p × p} = 1 = 10 × 10^{−1}.'], 'kp', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'gas', 'Consider the following equilibrium, CO(g) + 2H_{2}(g) ⇌ CH_{3}OH(g). 0.1 mol of CO along with a catalyst is present in a 2 dm^{3} flask maintained at 500 K. Hydrogen is introduced into the flask until the pressure is 5 bar and 0.04 mol of CH_{3}OH is formed. The K_{p}^{θ} is ______ × 10^{−3} (nearest integer). Given : R = 0.08 dm^{3} bar K^{−1} mol^{−1}. Assume only methanol is formed as the product and the system follows ideal gas behaviour.',
    None, 74, lambda: (lambda nt: round(((0.04 / nt * 5) / ((0.06 / nt * 5) * (((nt - 0.1) / nt * 5) ** 2))) * 1000))(5 * 2 / (0.08 * 500)),
    ['Total moles = \\f{PV}{RT} = \\f{5 × 2}{0.08 × 500} = 0.25; CO = 0.06, CH_{3}OH = 0.04, H_{2} = 0.25 − 0.10 = 0.15.', 'Partial pressures: 0.8, 1.2, 3.0 bar → K_{p} = \\f{0.8}{1.2 × 3^{2}} ≈ 0.074 = 74 × 10^{−3}.'], 'kp', 3)
add(('2025', 'Jan', '2025-01-22', 1), 'gas', 'A vessel at 1000 K contains CO_{2} with a pressure of 0.5 atm. Some of CO_{2} is converted into CO on addition of graphite. If total pressure at equilibrium is 0.8 atm, then K_{p} is :',
    ['3 atm', '0.3 atm', '0.18 atm', '1.8 atm'], 4, lambda: (lambda p: near([3, 0.3, 0.18, 1.8], (2 * p) ** 2 / (0.5 - p)))(bis(lambda p: 0.5 + p - 0.8, 0, 0.5)),
    ['CO_{2} + C ⇌ 2CO: 0.5 − p + 2p = 0.8 → p = 0.3.', 'p_{CO} = 0.6, p_{CO_{2}} = 0.2 → K_{p} = \\f{0.36}{0.2} = 1.8 atm.'], 'kp', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'gas', '37.8 g N_{2}O_{5} was taken in a 1 L reaction vessel and allowed to undergo the following reaction at 500 K: 2N_{2}O_{5}(g) ⇌ 2N_{2}O_{4}(g) + O_{2}(g). The total pressure at equilibrium was found to be 18.65 bar. Then, K_{p} = ______ × 10^{−2} [nearest integer]. Assume N_{2}O_{5} to behave ideally under these conditions. Given: R = 0.082 bar L mol^{−1} K^{−1}',
    None, 962, lambda: (lambda P0: (lambda y: round((2 * y) ** 2 * y / (P0 - 2 * y) ** 2 * 100))(18.65 - P0))(37.8 / 108 * 0.082 * 500),
    ['Initial p(N_{2}O_{5}) = 0.35 × 0.082 × 500 = 14.35 bar.', 'Let O_{2} = y: total = 14.35 + y = 18.65 → y = 4.3; N_{2}O_{4} = 8.6, N_{2}O_{5} = 5.75.', 'K_{p} = \\f{8.6^{2} × 4.3}{5.75^{2}} ≈ 9.62 = 962 × 10^{−2}.'], 'kp', 3)
add(('2026', 'Jan', '2026-01-23', 1), 'gas', 'For the following gas phase equilibrium reaction at constant temperature, NH_{3}(g) ⇌ \\f{1}{2}N_{2}(g) + \\f{3}{2}H_{2}(g), if the total pressure is √{3} atm and the pressure equilibrium constant (K_{p}) is 9 atm, then the degree of dissociation is given as (x × 10^{−2})^{−1/2}. The value of x is ____ . (nearest integer)',
    None, 125, lambda: (lambda a: round(1 / a ** 2 * 100))(bis(lambda a: ((a / 2) / (1 + a) * 3 ** 0.5) ** 0.5 * ((1.5 * a) / (1 + a) * 3 ** 0.5) ** 1.5 / ((1 - a) / (1 + a) * 3 ** 0.5) - 9, 1e-6, 1 - 1e-9)),
    ['Moles: 1 − α, \\f{α}{2}, \\f{3α}{2}; total 1 + α.', 'K_{p} = \\f{3√{3}}{4} × \\f{α^{2}P}{1 − α^{2}}; with P = √{3}: \\f{9}{4} × \\f{α^{2}}{1 − α^{2}} = 9 → α^{2} = 0.8.', 'α = (1.25)^{−1/2} = (125 × 10^{−2})^{−1/2} → x = 125.'], 'kp', 3)
add(('2026', 'Apr', '2026-04-05', 2), 'gas', 'The reaction A(g) ⇌ B(g) + C(g) was initiated with the amount \'a\' of A(g). At equilibrium it is found that the amount of A(g) remaining is (a − x) at a total pressure of p. The equilibrium constant K_{p} of the reaction can be calculated from the expression :',
    ['\\f{x^{2}}{a^{2} + x^{2}} × p', '\\f{x^{2}}{a^{2} − x^{2}} × p', '\\f{a + x^{2}}{x^{2}} × p', '\\f{a^{2} − x^{2}}{x^{2}} × p'], 2,
    lambda: (lambda a, x, p: near([x * x / (a * a + x * x) * p, x * x / (a * a - x * x) * p, (a + x * x) / (x * x) * p, (a * a - x * x) / (x * x) * p], (x / (a + x) * p) ** 2 / ((a - x) / (a + x) * p)))(2.0, 0.7, 3.0),
    ['Moles a − x, x, x; total a + x.', 'K_{p} = \\f{(\\f{x}{a + x}p)^{2}}{\\f{a − x}{a + x}p} = \\f{x^{2}p}{a^{2} − x^{2}}.'], 'kp', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'gas', 'For A(g) ⇌ B(g) + \\f{1}{2}C(g), the correct relationship between K_{P}, α and equilibrium pressure P is',
    ['K_{P} = \\f{α^{1/2}P^{1/2}}{(2 + α)^{1/2}}', 'K_{P} = \\f{α^{3/2}P^{1/2}}{(2 + α)^{1/2}(1 − α)}', 'K_{P} = \\f{α^{1/2}P^{3/2}}{(2 + α)^{3/2}}', 'K_{P} = \\f{α^{1/2}P^{1/2}}{(2 + α)^{3/2}}'], 2,
    lambda: (lambda a, Pp: near([(a * Pp / (2 + a)) ** 0.5, a ** 1.5 * Pp ** 0.5 / ((2 + a) ** 0.5 * (1 - a)), a ** 0.5 * Pp ** 1.5 / (2 + a) ** 1.5, (a * Pp) ** 0.5 / (2 + a) ** 1.5], (a / (1 + a / 2) * Pp) * ((a / 2) / (1 + a / 2) * Pp) ** 0.5 / ((1 - a) / (1 + a / 2) * Pp)))(0.3, 2.0),
    ['Moles 1 − α, α, \\f{α}{2}; total \\f{2 + α}{2}.', 'K_{P} = \\f{\\f{2αP}{2 + α}(\\f{αP}{2 + α})^{1/2}}{\\f{2(1 − α)P}{2 + α}} = \\f{α^{3/2}P^{1/2}}{(2 + α)^{1/2}(1 − α)}.'], 'kp', 3)
add(('2025', 'Jan', '2025-01-23', 2), 'gas', 'Consider the reaction X_{2}Y(g) ⇌ X_{2}(g) + \\f{1}{2}Y_{2}(g). The equation representing correct relationship between the degree of dissociation (x) of X_{2}Y(g) with its equilibrium constant Kp is ______. Assume x to be very very small.',
    ['x = ∛{\\f{2Kp}{p}}', 'x = ∛{\\f{Kp}{2p}}', 'x = ∛{\\f{Kp}{p}}', 'x = ∛{\\f{2Kp^{2}}{p}}'], 4,
    lambda: (lambda Kp, Pp: near([(2 * Kp / Pp) ** (1 / 3), (Kp / (2 * Pp)) ** (1 / 3), (Kp / Pp) ** (1 / 3), (2 * Kp * Kp / Pp) ** (1 / 3)], bis(lambda x: (x / (1 + x / 2) * Pp) * ((x / 2) / (1 + x / 2) * Pp) ** 0.5 / ((1 - x) / (1 + x / 2) * Pp) - Kp, 1e-9, 0.5)))(1e-6, 2.0),
    ['For small x: p_{X_{2}} ≈ xP, p_{Y_{2}} ≈ \\f{xP}{2}, p_{X_{2}Y} ≈ P.', 'K_{p} = x(\\f{xP}{2})^{1/2} → x^{3} = \\f{2K_{p}^{2}}{P}.'], 'kp', 3)
add(('2025', 'Jan', '2025-01-29', 1), 'gas', 'At temperature T, compound AB_{2}(g) dissociates as AB_{2}(g) ⇌ AB(g) + \\f{1}{2}B_{2}(g) having degree of dissociation x (small compared to unity). The correct expression for x in terms of K_{p} and p is',
    ['√{K_{p}}', '∜{\\f{2K_{p}}{p}}', '∛{\\f{2K_{p}}{p}}', '∛{\\f{2K_{p}^{2}}{p}}'], 4,
    lambda: (lambda Kp, Pp: near([Kp ** 0.5, (2 * Kp / Pp) ** 0.25, (2 * Kp / Pp) ** (1 / 3), (2 * Kp * Kp / Pp) ** (1 / 3)], bis(lambda x: (x / (1 + x / 2) * Pp) * ((x / 2) / (1 + x / 2) * Pp) ** 0.5 / ((1 - x) / (1 + x / 2) * Pp) - Kp, 1e-9, 0.5)))(1e-6, 3.0),
    ['Same as any A ⇌ B + ½C with small x: K_{p} ≈ x^{3/2}(\\f{P}{2})^{1/2}.', 'x = ∛{\\f{2K_{p}^{2}}{P}}.'], 'kp', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'gas', 'Dissociation of a gas A_{2} takes place according to the following chemical reaction. At equilibrium, the total pressure is 1 bar at 300 K: A_{2}(g) ⇌ 2A(g). The standard Gibbs energy of formation of the involved substances: A_{2}: −100.00 kJ mol^{−1}; A: −50.832 kJ mol^{−1}. The degree of dissociation of A_{2}(g) is given by (x × 10^{−2})^{1/2} where x = ____. (Nearest integer). [Given: R = 8 J mol^{−1} K^{−1}, log 2 = 0.3010, log 3 = 0.48] Assume degree of dissociation is not negligible.',
    None, 33, lambda: (lambda K: round(bis(lambda a: 4 * a * a / (1 - a * a) - K, 1e-9, 1 - 1e-9) ** 2 * 100))(math.exp(-(2 * -50.832 + 100.0) * 1000 / (8 * 300))),
    ['Δ_{r}G° = 2(−50.832) − (−100) = −1.664 kJ → K = e^{1664/2400} ≈ 2.', 'K_{p} = \\f{4α^{2}}{1 − α^{2}}P = 2 → α^{2} = \\f{1}{3} ≈ 33 × 10^{−2}.'], 'kp', 3)
add(('2026', 'Apr', '2026-04-06', 2), 'gas', 'In a closed flask at 600 K, one mole of X_{2}Y_{4}(g) attains equilibrium as given below: X_{2}Y_{4}(g) ⇌ 2XY_{2}(g). At equilibrium, 75% X_{2}Y_{4}(g) was dissociated and the total pressure is 1 atm. The magnitude of Δ_{r}G^{⊖} (in kJ mol^{−1}) at this temperature is ______. (Nearest Integer) (Given : R = 8.3 J mol^{−1} K^{−1}; ln 10 = 2.3, log 2 = 0.3, log 3 = 0.48, log 5 = 0.69, log 7 = 0.84)',
    None, 8, lambda: round(abs(-8.3 * 600 * math.log((1.5 / 1.75) ** 2 / (0.25 / 1.75))) / 1000),
    ['Moles 0.25 and 1.5; total 1.75 at 1 atm → K_{p} = \\f{(1.5/1.75)^{2}}{0.25/1.75} = \\f{36}{7} ≈ 5.14.', '|ΔG°| = RT ln K = 8.3 × 600 × 1.64 ≈ 8.2 kJ → 8.'], 'kp', 3)
add(('2026', 'Jan', '2026-01-21', 1), 'gas', 'Use the following data (500 K): AB(g): Δ_{f}H° = 32 kJ mol^{−1}, S° = 222 J K^{−1} mol^{−1}; A_{2}(g): Δ_{f}H° = 6, S° = 146; B_{2}(g): Δ_{f}H° = x, S° = 280. One mole each of A_{2}(g) and B_{2}(g) are taken in a 1 L closed flask and allowed to establish the equilibrium at 500 K: A_{2}(g) + B_{2}(g) ⇌ 2AB(g). The value of x (in kJ mol^{−1}) is ____ . (Nearest integer) (Given : log K = 2.2, R = 8.3 J K^{−1} mol^{−1})',
    None, 70, lambda: round(bis(lambda x: (2 * 32 - 6 - x) - 500 * (2 * 222 - 146 - 280) / 1000 + 8.3 * 500 * 2.303 * 2.2 / 1000, -500, 500)),
    ['ΔG° = −2.303RT log K = −2.303 × 8.3 × 500 × 2.2 ≈ −21.0 kJ.', 'ΔS° = 2(222) − 146 − 280 = 18 J/K → TΔS = 9 kJ; ΔH° = 64 − 6 − x.', '58 − x − 9 = −21 → x ≈ 70.'], 'kp', 3)
add(('2026', 'Apr', '2026-04-05', 1), 'gas', 'The values of pressure equilibrium constant recorded at different temperatures for the equilibrium reaction A(g) ⇌ B(g) + C(g): 1/T = 0.05, 0.06, 0.07 K^{−1} with log_{10} K_{p} = 3.5, 2.5, 1.5 respectively. The magnitude of \\f{ΔH°}{R} calculated from the above data is ____ . (Nearest integer)',
    None, 230, lambda: round(abs((1.5 - 3.5) / (0.07 - 0.05)) * 2.303), ['log K = −\\f{ΔH°}{2.303R} × \\f{1}{T} + c.', 'Slope = \\f{1.5 − 3.5}{0.02} = −100 → \\f{ΔH°}{R} = 230.3 ≈ 230.'], 'kp', 2)

# ---------------- shifts, Le Chatelier, ICE ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'gas', 'Consider the following chemical equilibrium of the gas phase reaction at a constant temperature : A(g) ⇌ B(g) + C(g). If p being the total pressure, K_{p} is the pressure equilibrium constant and α is the degree of dissociation, then which of the following is true at equilibrium?',
    ['When p increases α increases', 'If p value is extremely high compared to K_{p}, α ≈ 1', 'When p increases α decreases', 'If K_{p} value is extremely high compared to p, α becomes much less than unity'], 3,
    lambda: 3 if bis(lambda a: a * a / (1 - a * a) * 10 - 1, 1e-9, 1 - 1e-9) < bis(lambda a: a * a / (1 - a * a) * 1 - 1, 1e-9, 1 - 1e-9) else 0,
    ['K_{p} = \\f{α^{2}p}{1 − α^{2}} → α = √{\\f{K_{p}}{K_{p} + p}}.', 'Higher p → smaller α (fewer gas moles favoured).'], 'shift', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'gas', 'Given below are two statements: Statement I : A catalyst cannot alter the equilibrium constant (K_{c}) of the reaction, temperature remaining constant. Statement II : A homogenous catalyst can change the equilibrium composition of a system, temperature remaining constant. In the light of the above statements, choose the correct answer from the options below',
    ST4, 3, lambda: 3, ['A catalyst speeds up forward and backward reactions equally → same K and same equilibrium composition.', 'I true, II false.'], 'shift', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'gas', 'Observe the following equilibrium in a 1 L flask: A(g) ⇌ B(g). At T(K), the equilibrium concentrations of A and B are 0.5 M and 0.375 M respectively. 0.1 moles of A is added into the flask and heated to T(K) to establish the equilibrium again. The new equilibrium concentrations (in M) of A and B are respectively',
    ['0.557, 0.418', '0.367, 0.275', '0.742, 0.557', '0.53, 0.4'], 1,
    lambda: (lambda y: [i + 1 for i, (a, b) in enumerate([(0.557, 0.418), (0.367, 0.275), (0.742, 0.557), (0.53, 0.4)]) if abs(a - (0.6 - y)) < 0.002 and abs(b - (0.375 + y)) < 0.002][0])(bis(lambda y: (0.375 + y) / (0.6 - y) - 0.75, 0, 0.5)),
    ['K = \\f{0.375}{0.5} = 0.75. After adding A: \\f{0.375 + y}{0.6 − y} = 0.75 → y = 0.043.', 'A = 0.557 M, B = 0.418 M.'], 'shift', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'gas', 'X_{2}(g) + Y_{2}(g) ⇌ 2Z(g). X_{2}(g) and Y_{2}(g) are added to a 1 L flask and it is found that the system attains the above equilibrium at T(K) with the number of moles of X_{2}(g), Y_{2}(g) and Z(g) being 3, 3 and 9 mol respectively (equilibrium moles). Under this condition of equilibrium, 10 mol of Z(g) is added to the flask and the temperature is maintained at T(K). Then the number of moles of Z(g) in the flask when the new equilibrium is established is ______. (Nearest integer)',
    None, 15, lambda: round(19 - 2 * bis(lambda y: (19 - 2 * y) ** 2 / (3 + y) ** 2 - 9, 0, 9)), ['K = \\f{81}{9} = 9.', 'Back-reaction y: \\f{(19 − 2y)^{2}}{(3 + y)^{2}} = 9 → 19 − 2y = 9 + 3y → y = 2 → Z = 15.'], 'shift', 2)
add(('2026', 'Jan', '2026-01-24', 2), 'gas', 'Consider the following gaseous equilibrium in a closed container of volume \'V\' at T(K): P_{2}(g) + Q_{2}(g) ⇌ 2PQ(g). 2 moles each of P_{2}(g), Q_{2}(g) and PQ(g) are present at equilibrium. Now one mole each of \'P_{2}\' and \'Q_{2}\' are added to the equilibrium keeping the temperature at T(K). The number of moles of P_{2}, Q_{2} and PQ at the new equilibrium, respectively, are',
    ['2.67, 2.67, 2.67', '1.21, 2.24, 1.56', '1.66, 1.66, 1.66', '2.56, 1.62, 2.24'], 1,
    lambda: (lambda y: near([2.67, 1.21, 1.66, 2.56], 3 - y))(bis(lambda y: (2 + 2 * y) ** 2 / (3 - y) ** 2 - 1, 0, 2.9)),
    ['K = \\f{2^{2}}{2 × 2} = 1 (V cancels, Δn = 0).', '\\f{(2 + 2y)^{2}}{(3 − y)^{2}} = 1 → y = \\f{1}{3} → all three ≈ 2.67 mol.'], 'shift', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'gas', 'One mole each of He and A(g) are taken in a 10 L closed flask and heated to 400 K to establish the following equilibrium: A(g) ⇌ B(g). K_{c} for this reaction at 400 K is 4.0. The partial pressures (in atm) of He and B(g) are respectively (at equilibrium) (Assume He, A(g) and B(g) behave as ideal gases) (Given : R = 0.082 L atm K^{−1} mol^{−1})',
    ['3.28, 2.624', '2.624, 3.28', '3.28, 0.656', '0.656, 6.56'], 1,
    lambda: (lambda b: [i + 1 for i, (h, bb) in enumerate([(3.28, 2.624), (2.624, 3.28), (3.28, 0.656), (0.656, 6.56)]) if abs(h - 0.082 * 400 / 10) < 1e-6 and abs(bb - b * 0.082 * 400 / 10) < 1e-6][0])(bis(lambda b: b / (1 - b) - 4, 0, 0.999)),
    ['\\f{[B]}{[A]} = 4 → B = 0.8 mol, A = 0.2 mol (He is inert).', 'p = \\f{nRT}{V}: He = \\f{0.082 × 400}{10} = 3.28 atm; B = 0.8 × 3.28 = 2.624 atm.'], 'shift', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'gas', 'Consider the equilibrium CO(g) + 3H_{2}(g) ⇌ CH_{4}(g) + H_{2}O(g). If the pressure applied over the system increases by two fold at constant temperature then (A) Concentration of reactants and products increases. (B) Equilibrium will shift in forward direction. (C) Equilibrium constant increases since concentration of products increases. (D) Equilibrium constant remains unchanged as concentration of reactants and products remain same. Choose the correct answer from the options given below :',
    ['(A), (B) and (D) only', '(B) and (C) only', '(A), (B) and (C) only', '(A) and (B) only'], 4, lambda: 4,
    ['Squeezing raises every concentration (A ✓) and favours fewer gas moles (4 → 2): forward (B ✓).', 'K depends only on T: C ✗; D ✗ (K is unchanged, but the concentrations do change).'], 'shift', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'gas', 'The equilibrium Cr_{2}O_{7}^{2−} ⇌ 2CrO_{4}^{2−} is shifted to the right in :',
    ['an acidic medium', 'a basic medium', 'a weakly acidic medium', 'a neutral medium'], 2, lambda: 2,
    ['Cr_{2}O_{7}^{2−} + 2OH^{−} ⇌ 2CrO_{4}^{2−} + H_{2}O.', 'Adding OH^{−} (basic medium) pushes it right (orange → yellow).'], 'shift', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'gas', 'For the reaction N_{2}O_{4} ⇌ 2NO_{2}, the Gibbs energy at constant p, T is plotted against the fraction of N_{2}O_{4} dissociated: pure NO_{2} (point B) lies 5.40 kJ mol^{−1} above pure N_{2}O_{4} (point A), and the minimum (equilibrium, E) lies 0.84 kJ mol^{−1} below A. Identify correct statements. A. Standard free energy change for the reaction is −5.40 kJ mol^{−1}. B. As ΔG° in graph is positive, N_{2}O_{4} will not dissociate into NO_{2} at all. C. Reverse reaction will go to completion. D. When 1 mole of N_{2}O_{4} changes into equilibrium mixture, value of ΔG° = −0.84 kJ mol^{−1}. E. When 2 mole of NO_{2} changes into equilibrium mixture, ΔG° for equilibrium mixture is −6.24 kJ mol^{−1}. Choose the correct answer from the options given below :',
    ['D and E only', 'C and E only', 'A and D only', 'B and C only'], 1, lambda: 1 if abs(-(5.40 + 0.84) + 6.24) < 1e-9 else 0,
    ['ΔG° (N_{2}O_{4} → 2NO_{2}) = +5.40 kJ → A ✗; a positive ΔG° still allows some dissociation → B ✗; neither direction goes to completion → C ✗.', 'A → E: −0.84 kJ (D ✓). B → E: −(5.40 + 0.84) = −6.24 kJ (E ✓).'], 'shift', 2)

# ---------------- pH, weak acids/bases ----------------
add(('2025', 'Apr', '2025-04-07', 1), 'ion', 'An aqueous solution of HCl with pH 1.0 is diluted by adding equal volume of water (ignoring dissociation of water). The pH of HCl solution would (Given log 2 = 0.30)',
    ['increase to 2', 'increase to 1.3', 'remain same', 'reduce to 0.5'], 2, lambda: near([2, 1.3, 1.0, 0.5], -math.log10(0.1 / 2)), ['[H^{+}] = 0.1 → 0.05 M.', 'pH = −log 0.05 = 1.3.'], 'ph', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'ion', 'pH of water is 7 at 25 °C. If water is heated to 80 °C, it\'s pH will :',
    ['Increase', 'Decrease', 'H^{+} concentration increases, OH^{−} concentration decrease', 'Remains the same'], 2, lambda: 2,
    ['Self-ionisation of water is endothermic → K_{w} grows on heating.', '[H^{+}] = [OH^{−}] both rise → pH falls below 7 (water stays neutral).'], 'ph', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'ion', 'Consider the dissociation equilibrium of the following weak acid: HA ⇌ H^{+}(aq) + A^{−}(aq). If the pK_{a} of the acid is 4, then the pH of 10 mM HA solution is ____. (Nearest integer) [Given: The degree of dissociation can be neglected with respect to unity]',
    None, 3, lambda: round(-math.log10(weak_acid_H(0.01, 1e-4))), ['pH = ½(pK_{a} − log c) = ½(4 + 2) = 3.'], 'ph', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'ion', 'If 1 mM solution of ethylamine produces pH = 9, then the ionization constant (K_{b}) of ethylamine is 10^{−x}. The value of x is ____ (nearest integer). [The degree of ionization of ethylamine can be neglected with respect to unity.]',
    None, 7, lambda: round(-math.log10((1e-5) ** 2 / 1e-3)), ['pH 9 → [OH^{−}] = 10^{−5}.', 'K_{b} = \\f{(10^{−5})^{2}}{10^{−3}} = 10^{−7}.'], 'ph', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'ion', 'The pH of a 0.01 M weak acid HX (K_{a} = 4 × 10^{−10}) is found to be 5. Now the acid solution is diluted with excess of water so that the pH of the solution changes to 6. The new concentration of the diluted weak acid is given as x × 10^{−4} M. The value of x is ____ (nearest integer)',
    None, 25, lambda: round(bis(lambda c: weak_acid_H(c, 4e-10) - 1e-6, 1e-8, 0.01) * 1e4),
    ['For so weak an acid, water\'s own H^{+} matters: [H^{+}]^{2} ≈ K_{a}c + K_{w}.', '(10^{−6})^{2} = 4 × 10^{−10}c + 10^{−14} → c ≈ 2.5 × 10^{−3} = 25 × 10^{−4} M.'], 'ph', 3)
add(('2026', 'Jan', '2026-01-21', 2), 'ion', 'The first and second ionization constants of H_{2}X are 2.5 × 10^{−8} and 1.0 × 10^{−13} respectively. The concentration of X^{2−} in 0.1 M H_{2}X solution is ______ × 10^{−15} M. (Nearest Integer)',
    None, 100, lambda: (lambda h: round(1e-13 * (2.5e-8 * 0.1 / h) / h * 1e15))(weak_acid_H(0.1, 2.5e-8)), ['The second step is tiny and [H^{+}] ≈ [HX^{−}] from the first step.', '[X^{2−}] ≈ K_{a2} = 10^{−13} = 100 × 10^{−15} M.'], 'ph', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'ion', 'The first and second ionization constants of a weak dibasic acid H_{2}A are 8.1 × 10^{−8} and 1.0 × 10^{−13} respectively. 0.1 mol of H_{2}A was dissolved in 1 L of 0.1 M HCl solution. The concentration of HA^{−} in the resultant solution is :',
    ['0.1 M', '9.53 × 10^{−6} M', '8.1 × 10^{−8} M', '1.0 × 10^{−13} M'], 3, lambda: near([math.log10(0.1), math.log10(9.53e-6), math.log10(8.1e-8), -13], math.log10(8.1e-8 * 0.1 / 0.1)),
    ['HCl fixes [H^{+}] = 0.1 M and suppresses H_{2}A (common ion).', '[HA^{−}] = K_{a1}\\f{[H_{2}A]}{[H^{+}]} = 8.1 × 10^{−8} × \\f{0.1}{0.1} = 8.1 × 10^{−8} M.'], 'ph', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'ion', 'A weak acid HA has degree of dissociation x. Which option gives the correct expression of (pH − pK_{a})?',
    ['log(\\f{x}{1 − x})', 'log(\\f{1 − x}{x})', '0', 'log(1 + 2x)'], 1, lambda: (lambda c, x: near([math.log10(x / (1 - x)), math.log10((1 - x) / x), 0, math.log10(1 + 2 * x)], -math.log10(c * x) - (-math.log10(c * x * x / (1 - x)))))(0.1, 0.2),
    ['K_{a} = \\f{[H^{+}][A^{−}]}{[HA]} → pH = pK_{a} + log\\f{[A^{−}]}{[HA]} = pK_{a} + log\\f{x}{1 − x}.'], 'ph', 2)
add(('2024', 'Apr', '2024-04-06', 1), 'ion', 'Consider the dissociation of the weak acid HX as given below: HX(aq) ⇌ H^{+}(aq) + X^{−}(aq), K_{a} = 1.2 × 10^{−5} [K_{a} : dissociation constant]. The osmotic pressure of 0.03 M aqueous solution of HX at 300 K is ______ × 10^{−2} bar (nearest integer). [Given : R = 0.083 L bar mol^{−1} K^{−1}]',
    None, 76, lambda: (lambda h: round((0.03 + h) * 0.083 * 300 * 100))(weak_acid_H(0.03, 1.2e-5, 0)), ['α ≈ √{\\f{K_{a}}{c}} = √{\\f{1.2 × 10^{−5}}{0.03}} = 0.02 → i = 1.02.', 'π = 1.02 × 0.03 × 0.083 × 300 ≈ 0.76 bar = 76 × 10^{−2}.'], 'ph', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'ion', 'Considering acetic acid dissociates in water, its dissociation constant is 6.25 × 10^{−5}. If 5 mL of acetic acid is dissolved in 1 litre water, the solution will freeze at −x × 10^{−2} °C, provided pure water freezes at 0 °C. x = ______ (Nearest integer) Given : (K_{f})_{water} = 1.86 K kg mol^{−1}, density of acetic acid is 1.2 g mL^{−1}, molar mass of water = 18 g mol^{−1}, molar mass of acetic acid = 60 g mol^{−1}, density of water = 1 g cm^{−3}',
    None, 19, lambda: (lambda c: (lambda h: round(1.86 * (c + h) * 100))(weak_acid_H(c, 6.25e-5, 0)))(5 * 1.2 / 60),
    ['Acetic acid: 5 × 1.2 = 6 g = 0.1 mol in 1 kg water.', 'α = √{\\f{6.25 × 10^{−5}}{0.1}} = 0.025 → i = 1.025 → ΔT_{f} = 1.86 × 0.1 × 1.025 ≈ 0.19 °C → x = 19.'], 'ph', 2)

# ---------------- buffers, titration ----------------
add(('2025', 'Apr', '2025-04-07', 2), 'ion', 'One litre buffer solution was prepared by adding 0.10 mol each of NH_{3} and NH_{4}Cl in deionised water. The change in pH on addition of 0.05 mol of HCl to the above solution is ____ × 10^{−2}. (Nearest integer) Given : pK_{b} of NH_{3} = 4.745 and log_{10} 3 = 0.477',
    None, 48, lambda: round(abs((14 - 4.745 - math.log10(0.10 / 0.10)) - (14 - 4.745 - math.log10(0.15 / 0.05))) * 100), ['Before: pOH = pK_{b} + log 1 = 4.745.', 'HCl turns 0.05 mol NH_{3} into NH_{4}^{+}: pOH = 4.745 + log\\f{0.15}{0.05} = 5.222.', 'ΔpH = 0.477 ≈ 48 × 10^{−2}.'], 'buf', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'ion', 'Given below are two statements : Statement (I) : A Buffer solution is the mixture of a salt and an acid or a base mixed in any particular quantities. Statement (II) : Blood is naturally occurring buffer solution whose pH is maintained by H_{2}CO_{3}/HCO_{3}^{−} concentrations. In the light of the above statements, choose the correct answer from the options given below.',
    ['Statement I is false but Statement II is true', 'Both Statement I and Statement II is true', 'Both Statement I and Statement II is false', 'Statement I is true but Statement II is false'], 1, lambda: 1,
    ['A buffer needs a WEAK acid/base with its conjugate in comparable amounts — not any salt in any amount → I false.', 'Blood is buffered by H_{2}CO_{3}/HCO_{3}^{−} → II true.'], 'buf', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'ion', 'The pH of a solution obtained by mixing 5 mL of 0.1 M NH_{4}OH solution with 250 mL of 0.1 M NH_{4}Cl solution is ____ × 10^{−2}. (Nearest integer) Given: pK_{b}(NH_{4}OH) = 4.74, log 2 = 0.30, log 3 = 0.48, log 5 = 0.70',
    None, 756, lambda: round((14 - (4.74 + math.log10(25 / 0.5))) * 100), ['Base 0.5 mmol, salt 25 mmol → pOH = 4.74 + log 50 = 6.44.', 'pH = 7.56 = 756 × 10^{−2}.'], 'buf', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'ion', 'The pH of an aqueous solution containing 1 M benzoic acid (pK_{a} = 4.20) and 1 M sodium benzoate is 4.5. The volume of benzoic acid solution in 300 mL of this buffer solution is ______ mL.',
    None, 100, lambda: round(300 / (1 + 10 ** (4.5 - 4.20))), ['pH = pK_{a} + log\\f{[salt]}{[acid]} → \\f{salt}{acid} = 10^{0.3} = 2.', 'Same molarity → volumes 2 : 1 → acid = 100 mL.'], 'buf', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'ion', 'Which of the following mixture gives a buffer solution with pH = 9.25 ? Given : pK_{b}(NH_{4}OH) = 4.75',
    ['0.4 M NH_{4}OH (1 L) + 0.1 M HCl (1 L)', '0.5 M NH_{4}OH (0.2 L) + 0.2 M HCl (0.5 L)', '0.2 M NH_{4}OH (0.4 L) + 0.1 M HCl (1 L)', '0.2 M NH_{4}OH (0.5 L) + 0.1 M HCl (0.5 L)'], 4,
    lambda: [i + 1 for i, (b, a) in enumerate([(0.4, 0.1), (0.1, 0.1), (0.08, 0.1), (0.1, 0.05)]) if b > a and abs(14 - (4.75 + math.log10(a / (b - a))) - 9.25) < 1e-9][0],
    ['pH 9.25 → pOH 4.75 = pK_{b} → need [NH_{4}^{+}] = [NH_{4}OH].', '(4): 0.1 mol base + 0.05 mol HCl → 0.05 : 0.05 ✓.'], 'buf', 2)
add(('2026', 'Apr', '2026-04-02', 2), 'ion', 'At 25 °C, 20.0 mL of 0.2 M weak monoprotic acid HX is titrated against 0.2 M NaOH. The pH of the solution (a) at the start of the titration (when NaOH has not been added) and (b) when 10 mL of NaOH is added respectively, are : Given: K_{a} = 5 × 10^{−4}, pK_{a} = 3.3',
    ['(a) 0.7, (b) 2.0', '(a) 2.0, (b) 3.3', '(a) 1.1, (b) 2.2', '(a) 3.0, (b) 2.2'], 2,
    lambda: (lambda a, b: [i + 1 for i, (x, y) in enumerate([(0.7, 2.0), (2.0, 3.3), (1.1, 2.2), (3.0, 2.2)]) if abs(x - a) < 0.06 and abs(y - b) < 0.06][0])(-math.log10(math.sqrt(5e-4 * 0.2)), 3.3 + math.log10(2 / 2)),
    ['(a) [H^{+}] ≈ √{K_{a}c} = √{5 × 10^{−4} × 0.2} = 10^{−2} → pH 2.0.', '(b) Half neutralised: [X^{−}] = [HX] → pH = pK_{a} = 3.3.'], 'buf', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'ion', '20 mL of a solution of acetic acid required 28.4 mL of 0.1 M NaOH for its neutralization. A solution (X) was prepared by mixing 20 mL of the above acetic acid and 14.2 mL of 0.1 M NaOH solution. What is the pH of the solution (X) ? (pK_{a} value of acetic acid is 4.75).',
    ['7.0', '4.75', '3.5', '4.82'], 2, lambda: near([7, 4.75, 3.5, 4.82], 4.75 + math.log10(1.42 / (2.84 - 1.42))), ['Acid = 2.84 mmol; NaOH 1.42 mmol = exactly half.', 'Salt = acid → pH = pK_{a} = 4.75.'], 'buf', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'ion', 'Consider a weak base \'B\' of pK_{b} = 5.699. \'x\' mL of 0.02 M HCl and \'y\' mL of 0.02 M weak base \'B\' are mixed to make 100 mL of a buffer of pH 9 at 25 °C. The values of \'x\' and \'y\' respectively are : [Given: log 2 = 0.3010, log 3 = 0.4771, log 5 = 0.699]',
    ['x = 11.1, y = 88.9', 'x = 42.7, y = 57.3', 'x = 14.3, y = 85.7', 'x = 85.7, y = 14.3'], 3,
    lambda: (lambda x: near([11.1, 42.7, 14.3, 85.7], x))(bis(lambda x: 14 - (5.699 + math.log10(x / ((100 - x) - x))) - 9, 0.01, 49.9)),
    ['pOH = 5 → log\\f{[BH^{+}]}{[B]} = 5 − 5.699 → \\f{BH^{+}}{B} = 0.2.', 'Same molarity: \\f{x}{y − x} = 0.2 with x + y = 100 → x ≈ 14.3, y ≈ 85.7.'], 'buf', 3)
add(('2026', 'Apr', '2026-04-05', 1), 'ion', 'Arrange the following resultant mixtures in increasing order of their pH values: A. 10 mL 0.2 M Ca(OH)_{2} + 25 mL 0.1 M HCl B. 10 mL 0.01 M H_{2}SO_{4} + 10 mL 0.01 M Ca(OH)_{2} C. 10 mL 0.1 M H_{2}SO_{4} + 10 mL 0.1 M KOH. Choose the correct answer from the options given below:',
    ['B < C < A', 'C < A < B', 'C < B < A', 'A < C < B'], 3,
    lambda: (lambda v: pick(['B < C < A', 'C < A < B', 'C < B < A', 'A < C < B'], ' < '.join(sorted(v, key=v.get))))({'A': 2 * 2 - 2.5, 'B': 0.2 - 0.2, 'C': 1.0 - 2.0}),
    ['A: OH^{−} 4 mmol − H^{+} 2.5 → basic. B: 0.2 mmol each → neutral. C: H^{+} 2 − OH^{−} 1 → acidic.', 'C < B < A.'], 'buf', 2)

# ---------------- solubility product ----------------
add(('2024', 'Apr', '2024-04-09', 2), 'ksp', 'For a sparingly soluble salt AB_{2}, the equilibrium concentrations of A^{2+} ions and B^{−} ions are 1.2 × 10^{−4} M and 0.24 × 10^{−3} M, respectively. The solubility product of AB_{2} is :',
    ['0.069 × 10^{−12}', '6.91 × 10^{−12}', '0.276 × 10^{−1}', '27.65 × 10^{−12}'], 2, lambda: near([0.069e-12, 6.91e-12, 0.0276, 27.65e-12], 1.2e-4 * (0.24e-3) ** 2), ['K_{sp} = [A^{2+}][B^{−}]^{2} = 1.2 × 10^{−4} × (2.4 × 10^{−4})^{2} ≈ 6.91 × 10^{−12}.'], 'ksp', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'ksp', 'K_{sp} for Cr(OH)_{3} is 1.6 × 10^{−30}. What is the molar solubility of this salt in water?',
    ['∜{1.8 × 10^{−30}}', '∜{1.6 × 10^{−30}}', '∜{\\f{1.6 × 10^{−30}}{27}}', '\\f{1.8 × 10^{−30}}{27}'], 3, lambda: near([(1.8e-30) ** 0.25, (1.6e-30) ** 0.25, (1.6e-30 / 27) ** 0.25, 1.8e-30 / 27], bis(lambda s: s * (3 * s) ** 3 - 1.6e-30, 0, 1e-5)),
    ['Cr(OH)_{3} → Cr^{3+} + 3OH^{−}: K_{sp} = s(3s)^{3} = 27s^{4}.', 's = ∜{\\f{K_{sp}}{27}}.'], 'ksp', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'ksp', 'The solubility product constants of Ag_{2}CrO_{4} and AgBr are 32x and 4y respectively at 298 K. The value of (\\f{molarity of Ag_{2}CrO_{4}}{molarity of AgBr}) can be expressed as :',
    ['\\f{2∛{x}}{y}', '2√{\\f{x}{y}}', '√{\\f{x}{y}}', '\\f{∛{x}}{√{y}}'], 4,
    lambda: (lambda x, y: near([2 * x ** (1 / 3) / y, 2 * (x / y) ** 0.5, (x / y) ** 0.5, x ** (1 / 3) / y ** 0.5], bis(lambda s: 4 * s ** 3 - 32 * x, 0, 10) / math.sqrt(4 * y)))(0.3, 0.7),
    ['Ag_{2}CrO_{4}: 4s^{3} = 32x → s = 2∛{x}. AgBr: s^{2} = 4y → s = 2√{y}.', 'Ratio = \\f{∛{x}}{√{y}}.'], 'ksp', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'ksp', 'M_{3}A_{2} is a sparingly soluble salt of molar mass y g mol^{−1} and solubility x g L^{−1}. The ratio of the molar concentration of the anion (A^{3−}) to the solubility product of the salt is',
    ['\\f{1}{54} · \\f{y^{4}}{x^{4}}', '\\f{y^{5}}{108x^{4}}', '108 · \\f{x^{5}}{y^{5}}', '\\f{1}{108} · \\f{y^{4}}{x^{4}}'], 1,
    lambda: (lambda x, y: (lambda s: near([y ** 4 / (54 * x ** 4), y ** 5 / (108 * x ** 4), 108 * x ** 5 / y ** 5, y ** 4 / (108 * x ** 4)], 2 * s / ((3 * s) ** 3 * (2 * s) ** 2)))(x / y))(0.002, 300.0),
    ['s = \\f{x}{y} mol/L; [A^{3−}] = 2s; K_{sp} = (3s)^{3}(2s)^{2} = 108s^{5}.', 'Ratio = \\f{2s}{108s^{5}} = \\f{1}{54s^{4}} = \\f{1}{54}\\f{y^{4}}{x^{4}}.'], 'ksp', 2)
add(('2025', 'Jan', '2025-01-28', 2), 'ksp', 'Arrange the following in increasing order of solubility product : Ca(OH)_{2}, AgBr, PbS, HgS',
    ['HgS < AgBr < PbS < Ca(OH)_{2}', 'HgS < PbS < AgBr < Ca(OH)_{2}', 'Ca(OH)_{2} < AgBr < HgS < PbS', 'PbS < HgS < Ca(OH)_{2} < AgBr'], 2,
    lambda: (lambda v: pick(['HgS < AgBr < PbS < Ca(OH)_{2}', 'HgS < PbS < AgBr < Ca(OH)_{2}', 'Ca(OH)_{2} < AgBr < HgS < PbS', 'PbS < HgS < Ca(OH)_{2} < AgBr'], ' < '.join(sorted(v, key=v.get))))({'Ca(OH)_{2}': 5.5e-6, 'AgBr': 5.0e-13, 'PbS': 8e-28, 'HgS': 4e-53}),
    ['Typical K_{sp}: HgS ~10^{−53}, PbS ~10^{−28}, AgBr ~5 × 10^{−13}, Ca(OH)_{2} ~5 × 10^{−6}.'], 'ksp', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'ksp', 'If equal volumes of AB_{2} and XY (both are salts) aqueous solutions are mixed, which of the following combination will give a precipitate of AY_{2} at 300 K ? (Given K_{sp} (at 300 K) for AY_{2} = 5.2 × 10^{−7})',
    ['2.0 × 10^{−4} M AB_{2}, 0.8 × 10^{−3} M XY', '3.6 × 10^{−3} M AB_{2}, 5.0 × 10^{−4} M XY', '2.0 × 10^{−2} M AB_{2}, 2.0 × 10^{−2} M XY', '1.5 × 10^{−4} M AB_{2}, 1.5 × 10^{−3} M XY'], 3,
    lambda: [i + 1 for i, (a, b) in enumerate([(2e-4, 0.8e-3), (3.6e-3, 5e-4), (2e-2, 2e-2), (1.5e-4, 1.5e-3)]) if (a / 2) * (b / 2) ** 2 > 5.2e-7][0],
    ['Mixing equal volumes halves each concentration.', '(3): Q = (10^{−2})(10^{−2})^{2} = 10^{−6} > 5.2 × 10^{−7} → precipitate; the others give Q far smaller.'], 'ksp', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'ksp', 'Consider two Group IV metal ions X^{2+} and Y^{2+}. A solution containing 0.01 M X^{2+} and 0.01 M Y^{2+} is saturated with H_{2}S. The pH at which the metal sulphide YS will form as a precipitate is ____. (Nearest integer) (Given: K_{sp}(XS) = 1 × 10^{−22} at 25 °C, K_{sp}(YS) = 4 × 10^{−16} at 25 °C, [H_{2}S] = 0.1 M in solution, K_{a1} × K_{a2}(H_{2}S) = 1.0 × 10^{−21}, log 2 = 0.30, log 3 = 0.48, log 5 = 0.70)',
    None, 4, lambda: round(-math.log10(math.sqrt(1e-21 * 0.1 / (4e-16 / 0.01)))), ['YS needs [S^{2−}] = \\f{4 × 10^{−16}}{0.01} = 4 × 10^{−14} M.', '[H^{+}]^{2} = \\f{K_{a1}K_{a2}[H_{2}S]}{[S^{2−}]} = \\f{10^{−22}}{4 × 10^{−14}} → [H^{+}] = 5 × 10^{−5} → pH ≈ 4.3 → 4.'], 'ksp', 3)
add(('2026', 'Apr', '2026-04-08', 2), 'gas', 'Solid carbon, CaO and CaCO_{3} are mixed and allowed to attain equilibrium at T K: CaCO_{3}(s) ⇌ CaO(s) + CO_{2}(g), K_{p1} = 0.08 atm; C(s) + CO_{2}(g) ⇌ 2CO(g), K_{p2} = 2 atm. The partial pressure of CO is ____ × 10^{−1} atm',
    None, 4, lambda: round(math.sqrt(2 * 0.08) * 10), ['Solids fix p_{CO_{2}} = K_{p1} = 0.08 atm.', 'p_{CO}^{2} = 2 × 0.08 = 0.16 → p_{CO} = 0.4 atm = 4 × 10^{−1}.'], 'kp', 2)
add(('2026', 'Apr', '2026-04-06', 2), 'ion', 'Given is a concentrated solution of a weak electrolyte A_{x}B_{y} of concentration \'c\' and dissociation constant \'K\'. The degree of dissociation is given by :',
    ['[K × c^{x + y − 1}x^{x}y^{y}]^{x + y}', '(\\f{K}{c^{x + y − 1}x^{x}y^{y}})^{1/(x + y)}', '(\\f{c^{x + y − 1}x^{x}y^{y}}{K})^{x + y}', '(\\f{c^{x + y − 1}x^{x}y^{y}}{K})^{1/(x + y)}'], 2,
    lambda: (lambda x, y, c, K: (lambda D: near([(K * D) ** (x + y), (K / D) ** (1 / (x + y)), (D / K) ** (x + y), (D / K) ** (1 / (x + y))], bis(lambda a: (x * a * c) ** x * (y * a * c) ** y / (c * (1 - a)) - K, 1e-12, 0.5)))(c ** (x + y - 1) * x ** x * y ** y))(1, 2, 0.5, 1e-9),
    ['A_{x}B_{y} ⇌ xA + yB: K = \\f{(xαc)^{x}(yαc)^{y}}{c(1 − α)} ≈ x^{x}y^{y}α^{x + y}c^{x + y − 1} (α ≪ 1).', 'α = (\\f{K}{c^{x + y − 1}x^{x}y^{y}})^{1/(x + y)}.'], 'ph', 3)

for _p in P: _p['t'] = _p['fam']   # topics = families (kp, shift, ph, buf, ksp)
