"""Real JEE Main questions — Chemistry Unit 8: Chemical Kinetics. Our own solutions; chk re-solves each.
Skipped on purpose (ambiguous/disputed): 22-1-25 S1 Q23 (69 vs 70 ps), 31-1-24 S1 Q13 (stoichiometry not stated),
2-Apr-2026 S1 Q58 (non-standard '(t½)^∞' notation)."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
L2, L3, L10 = math.log(2), math.log(3), math.log(10)
ST = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
def st(a, b): return 1 if a and b else 2 if not a and not b else 3 if a else 4
def combo(opts, truth):   # opts like 'A and B Only' → pick the one listing exactly the true letters
    want = ''.join(sorted(k for k, v in truth.items() if v))
    hits = [i + 1 for i, o in enumerate(opts) if ''.join(sorted(c for c in o.replace('Only', '').replace('only', '') if c in 'ABCDE')) == want]
    assert len(hits) == 1, (opts, want); return hits[0]

# ---------- rate law & order ----------
add(('2025', 'Apr', '2025-04-04', 1), 'rate', 'Rate law for a reaction between A and B is given by r = k[A]^{n}[B]^{m}. If concentration of A is doubled and concentration of B is halved from their initial value, the ratio of new rate of reaction to the initial rate of reaction (\\f{r_{2}}{r_{1}}) is',
    ['(n − m)', '(m + n)', '\\f{1}{2^{m + n}}', '2^{(n − m)}'], 4, lambda: 4 if all(abs(2 ** n * 0.5 ** m - 2 ** (n - m)) < 1e-12 for n in range(4) for m in range(4)) else 0,
    ['r_{2}/r_{1} = \\f{k(2[A])^{n}([B]/2)^{m}}{k[A]^{n}[B]^{m}} = 2^{n} × 2^{−m}.', '= 2^{(n − m)}.'], 'order', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'rate', 'Consider the following data for the given reaction 2HI(g) → H_{2}(g) + I_{2}(g). [HI] (mol L^{−1}): 0.005, 0.01, 0.02; Rate (mol L^{−1} s^{−1}): 7.5 × 10^{−4}, 3.0 × 10^{−3}, 1.2 × 10^{−2}. The order of the reaction is ______.',
    None, 2, lambda: round(math.log(3.0e-3 / 7.5e-4) / math.log(0.01 / 0.005)),
    ['Doubling [HI] (0.005 → 0.01) raises the rate 4 times (7.5 × 10^{−4} → 3.0 × 10^{−3}).', '2^{x} = 4 → x = 2 (check: 0.01 → 0.02 again ×4).', 'Second order.'], 'order', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'rate', 'During kinetic study of reaction 2A + B → C + D, the following results were obtained: I. [A] = 0.1 M, [B] = 0.1 M, rate = 6.0 × 10^{−3}; II. [A] = 0.3 M, [B] = 0.2 M, rate = 7.2 × 10^{−2}; III. [A] = 0.3 M, [B] = 0.4 M, rate = 2.88 × 10^{−1}; IV. [A] = 0.4 M, [B] = 0.1 M, rate = 2.40 × 10^{−2} (initial rate of formation of D, M min^{−1}). Based on above data, overall order of the reaction is ______.',
    None, 3, lambda: round(math.log(2.4e-2 / 6e-3) / math.log(4)) + round(math.log(2.88e-1 / 7.2e-2) / math.log(2)),
    ['Order in A: I → IV, [B] fixed, [A] ×4, rate ×4 → first order in A.', 'Order in B: II → III, [A] fixed, [B] ×2, rate ×4 → second order in B.', 'Check I → II: 3 × 2^{2} = 12, and 6.0 × 10^{−3} × 12 = 7.2 × 10^{−2} ✓.', 'Overall order = 1 + 2 = 3.'], 'order', 2)
add(('2024', 'Apr', '2024-04-08', 1), 'rate', 'Consider the following reaction A + B → C. The time taken for A to become 1/4^{th} of its initial concentration is twice the time taken to become 1/2 of the same. Also, when the change of concentration of B is plotted against time, the resulting graph gives a straight line with a negative slope and a positive intercept on the concentration axis. The overall order of the reaction is ______.',
    None, 1, lambda: 1 + 0,
    ['t_{1/4} = 2t_{1/2} means every half-life is the same → constant half-life → first order in A.', '[B] falling as a straight line with time → zero order in B.', 'Overall order = 1 + 0 = 1.'], 'order', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'rate', 'The reaction A_{2} + B_{2} → 2AB follows the mechanism: A_{2} ⇌ A + A (fast, k_{1}, k_{−1}); A + B_{2} → AB + B (slow, k_{2}); A + B → AB (fast). The overall order of the reaction is :',
    ['2.5', '1.5', '3', '2'], 2, lambda: pick([2.5, 1.5, 3, 2], F(1, 2) + 1),
    ['Rate = k_{2}[A][B_{2}] (slow step).', 'Fast equilibrium: K = \\f{[A]^{2}}{[A_{2}]} → [A] = √{K[A_{2}]}.', 'Rate = k_{2}√{K}[A_{2}]^{1/2}[B_{2}] → order ½ + 1 = 1.5.'], 'order', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'rate', 'Given below are two statements : Statement I : The rate law for the reaction A + B → C is rate (r) = k[A]^{2}[B]. When the concentration of both A and B is doubled, the reaction rate is increased "x" times. Statement II : A plot of concentration of reactant against time is a straight line starting at [R]_{0} with slope −k for a "y" order reaction. The value of x + y is ______.',
    None, 8, lambda: 2 ** 2 * 2 + 0,
    ['x = 2^{2} × 2 = 8.', 'A straight-line fall of [R] with time (slope −k) is the zero-order law [R] = [R]_{0} − kt → y = 0.', 'x + y = 8.'], 'order', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'rate', 'Observe the following reactions at T(K). I. A → products. II. 5Br^{−}(aq) + BrO_{3}^{−}(aq) + 6H^{+}(aq) → 3Br_{2}(aq) + 3H_{2}O(l). Both the reactions are started at 10.00 am. The rates of these reactions at 10.10 am are same. The value of −\\f{Δ[Br^{−}]}{Δt} at 10.10 am is 2 × 10^{−4} mol L^{−1} min^{−1}. The concentration of A at 10.10 am is 10^{−2} mol L^{−1}. What is the first order rate constant (in min^{−1}) of reaction I ?',
    ['2 × 10^{−3}', '10^{−3}', '10^{−2}', '4 × 10^{−3}'], 4, lambda: pick([2e-3, 1e-3, 1e-2, 4e-3], 2e-4 / 5 / 1e-2),
    ['Rate of reaction II = −\\f{1}{5}\\f{Δ[Br^{−}]}{Δt} = \\f{2 × 10^{−4}}{5} = 4 × 10^{−5} mol L^{−1} min^{−1}.', 'Reaction I has the same rate: k[A] = 4 × 10^{−5} → k = \\f{4 × 10^{−5}}{10^{−2}} = 4 × 10^{−3} min^{−1}.'], 'order', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'rate', 'NO_{2} required for a reaction is produced by decomposition of N_{2}O_{5} in CCl_{4} as by equation 2N_{2}O_{5}(g) → 4NO_{2}(g) + O_{2}(g). The initial concentration of N_{2}O_{5} is 3 mol L^{−1} and it is 2.75 mol L^{−1} after 30 minutes. The rate of formation of NO_{2} is x × 10^{−3} mol L^{−1} min^{−1}, value of x is ______. (nearest integer)',
    None, 17, lambda: round((3 - 2.75) / 30 * 2 * 1000),
    ['Rate of disappearance of N_{2}O_{5} = \\f{3 − 2.75}{30} = 8.33 × 10^{−3} mol L^{−1} min^{−1}.', '4 NO_{2} form per 2 N_{2}O_{5} → rate of formation of NO_{2} = 2 × 8.33 × 10^{−3} = 16.7 × 10^{−3} ≈ 17 × 10^{−3}.'], 'order', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'rate', 'For a reaction A →(K_{1}) B →(K_{2}) C. If the rate of formation of B is set to be zero then the concentration of B is given by :',
    ['K_{1}K_{2}[A]', '(K_{1} − K_{2})[A]', '(K_{1} + K_{2})[A]', '(K_{1}/K_{2})[A]'], 4, lambda: 4,
    ['Net rate of formation of B = K_{1}[A] − K_{2}[B].', 'Setting it to zero (steady state): K_{1}[A] = K_{2}[B] → [B] = (K_{1}/K_{2})[A].'], 'order', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'rate', 'A → product (First order reaction). Three sets of experiment were performed for a reaction under similar experimental conditions: Run 1 ⇒ 100 mL of 10 M solution of reactant A; Run 2 ⇒ 200 mL of 10 M solution of reactant A; Run 3 ⇒ 100 mL of 10 M solution of reactant A + 100 mL of H_{2}O added. The correct variation of rate of reaction is',
    ['Run 1 = Run 2 = Run 3', 'Run 3 < Run 1 = Run 2', 'Run 3 < Run 1 < Run 2', 'Run 1 < Run 2 < Run 3'], 2, lambda: 2 if (10 == 10 and 10 * 100 / 200 < 10) else 0,
    ['Rate = k[A] depends on CONCENTRATION, not on volume.', 'Runs 1 and 2: [A] = 10 M → equal rates.', 'Run 3: diluted to 200 mL → [A] = 5 M → half the rate.', 'Run 3 < Run 1 = Run 2.'], 'order', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'rate', "Consider the reaction aX → bY, for which the rate constant at 30 °C is 1 × 10^{−3} mol^{−1} L s^{−1}. Which of the following statements are true ? A. When concentration of 'X' is increased to four times, the rate of reaction becomes 16 times. B. The reaction is a second order reaction. C. The half-life period is independent of the concentration of X. D. Decomposition of N_{2}O_{5} is an example of the above reaction. E. A plot of ln\\f{[R_{0}]}{[R]} against time is a straight line through the origin for the above reaction.",
    ['A and B Only', 'A, B and C Only', 'A, B, D and E Only', 'C and D Only'], 1, lambda: combo(['A and B Only', 'A, B and C Only', 'A, B, D and E Only', 'C and D Only'], dict(A=4 ** 2 == 16, B=True, C=False, D=False, E=False)),
    ['Unit mol^{−1} L s^{−1} = (mol L^{−1})^{1−n} s^{−1} with n = 2 → second order (B true).', 'Rate ∝ [X]^{2} → ×4 gives ×16 (A true).', 'For second order t_{1/2} = \\f{1}{k[X]_{0}} depends on [X]_{0} (C false).', 'N_{2}O_{5} decomposition is first order (D false), and the ln plot is the first-order test (E false).'], 'order', 2)

# ---------- first-order kinetics ----------
add(('2025', 'Apr', '2025-04-03', 1), 'first', 'In a reaction A + B → C, initial concentrations of A and B are related as [A]_{0} = 8[B]_{0}. The half lives of A and B are 10 min and 40 min, respectively. If they start to disappear at the same time, both following first order kinetics, after how much time will the concentration of both the reactants be same?',
    ['60 min', '20 min', '40 min', '80 min'], 3, lambda: pick([60, 20, 40, 80], 3 / (F(1, 10) - F(1, 40))),
    ['[A] = 8[B]_{0}·2^{−t/10},  [B] = [B]_{0}·2^{−t/40}.', 'Equal when 8 = 2^{t/10 − t/40} = 2^{3t/40} → \\f{3t}{40} = 3 → t = 40 min.'], 'first', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'first', 'Time required for completion of 99.9% of a First order reaction is ______ times of half life (t_{1/2}) of the reaction. (nearest integer)',
    None, 10, lambda: round(math.log(1000) / L2),
    ['t_{99.9%} = \\f{ln 1000}{k} and t_{1/2} = \\f{ln 2}{k}.', 'Ratio = \\f{3 × 2.303}{0.693} = 9.97 ≈ 10.'], 'first', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'first', 'Time required for 99.9% completion of a first order reaction is ______ times the time required for completion of 90% reaction. (nearest integer)',
    None, 3, lambda: round(math.log(1000) / L10),
    ['t = \\f{1}{k}ln\\f{[A]_{0}}{[A]}.', '99.9%: ln 1000 = 3 ln 10. 90%: ln 10.', 'Ratio = 3.'], 'first', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'first', 'Consider the first order reaction R → P. The fraction of molecules decomposed in the given first order reaction can be expressed as',
    ['1 − e^{k_{1}t}', '1 + e^{k_{1}t}', '1 + e^{−k_{1}t}', '1 − e^{−k_{1}t}'], 4, lambda: 4,
    ['[R] = [R]_{0}e^{−k_{1}t}, so the fraction LEFT is e^{−k_{1}t}.', 'Fraction decomposed = 1 − e^{−k_{1}t}.'], 'first', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'first', 'The rate of first order reaction is 0.04 mol L^{−1} s^{−1} at 10 minutes and 0.03 mol L^{−1} s^{−1} at 20 minutes after initiation. Half life of the reaction is ______ minutes. (Given log 2 = 0.3010, log 3 = 0.4771) (nearest integer)',
    None, 24, lambda: round(10 * L2 / math.log(4 / 3)),
    ['First order: rate ∝ [A], so \\f{r_{1}}{r_{2}} = \\f{[A]_{1}}{[A]_{2}} = \\f{4}{3} over 10 min.', 'k = \\f{2.303}{10}log\\f{4}{3} = \\f{2.303 × 0.1249}{10} min^{−1}.', 't_{1/2} = \\f{0.693}{k} = \\f{10 × 0.3010}{0.1249} ≈ 24 min.'], 'first', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'first', 'For a first order reaction A → B, [A] = 0.6500 M at t = 0, 0.0650 M at t = x min and 0.00065 M at t = 20 min. x = ______ min. (Nearest integer)',
    None, 7, lambda: round(20 * math.log(10) / math.log(1000)),
    ['0.65 → 0.00065 is a 1000-fold fall in 20 min: kt = ln 1000 = 3 ln 10.', '0.65 → 0.065 is a 10-fold fall: kx = ln 10.', 'x = \\f{20}{3} = 6.67 ≈ 7 min.'], 'first', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'first', 'An organic compound undergoes first order decomposition. The time taken for decomposition to (\\f{1}{8}) and (\\f{1}{10})^{th} of its initial concentration are t_{1/8} and t_{1/10} respectively. What is the value of \\f{t_{1/8}}{t_{1/10}} × 10 ? (log 2 = 0.3)',
    ['9', '0.9', '3', '30'], 1, lambda: pick([9, 0.9, 3, 30], round(3 * 0.3 / 1 * 10, 6)),
    ['t = \\f{2.303}{k}log\\f{[A]_{0}}{[A]}.', '\\f{t_{1/8}}{t_{1/10}} = \\f{log 8}{log 10} = 3 × 0.3 = 0.9.', '× 10 = 9.'], 'first', 1)
add(('2024', 'Feb', '2024-02-01', 1), 'first', 'The ratio of \\f{^{14}C}{^{12}C} in a piece of wood is \\f{1}{8} part that of atmosphere. If half life of ^{14}C is 5730 years, the age of wood sample is ______ years.',
    None, 17190, lambda: 3 * 5730,
    ['\\f{1}{8} = (\\f{1}{2})^{3} → three half-lives have passed.', 'Age = 3 × 5730 = 17190 years.'], 'first', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'first', 'The half-life of radioisotopic bromine-82 is 36 hours. The fraction which remains after one day is ______ × 10^{−2}. (Given antilog 0.2006 = 1.587) (nearest integer)',
    None, 63, lambda: round(100 * 2 ** (-24 / 36)),
    ['Fraction left = (\\f{1}{2})^{t/t_{1/2}} = 2^{−24/36} = 2^{−2/3}.', 'log 2^{2/3} = \\f{2}{3} × 0.301 = 0.2006 → 2^{2/3} = 1.587.', 'Fraction = \\f{1}{1.587} = 0.63 = 63 × 10^{−2}.'], 'first', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'first', 'Drug X becomes ineffective after 50% decomposition. The original concentration of drug in a bottle was 16 mg/mL which becomes 4 mg/mL in 12 months. The expiry time of the drug in months is ______. Assume that the decomposition of the drug follows first order kinetics.',
    ['3', '2', '12', '6'], 4, lambda: pick([3, 2, 12, 6], 12 / round(math.log2(16 / 4))),
    ['16 → 4 mg/mL is two half-lives (16 → 8 → 4) in 12 months.', 't_{1/2} = 6 months, and the drug expires at 50% → 6 months.'], 'first', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'first', 'If the half life of a first order reaction is 6.93 minutes then the time required for completion of 99% of the reaction will be ______ minutes. (Given : log 2 = 0.3010) (nearest integer)',
    None, 46, lambda: round(math.log(100) / (L2 / 6.93)),
    ['k = \\f{0.693}{6.93} = 0.1 min^{−1}.', 't_{99%} = \\f{2.303}{0.1}log 100 = 46.06 ≈ 46 min.'], 'first', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'first', 'Sucrose hydrolyses in acidic medium into glucose and fructose by first order rate law with t_{1/2} = 3 hour. The percentage of sucrose remaining after 6 hours is ______. (Nearest integer) (Given : log 2 = 0.3010 and log 3 = 0.4771)',
    None, 25, lambda: round(100 * 0.5 ** (6 / 3)),
    ['6 hours = 2 half-lives.', 'Remaining = 100 × (\\f{1}{2})^{2} = 25%.'], 'first', 1)
add(('2026', 'Jan', '2026-01-24', 2), 'first', 'The half-life of ^{65}Zn is 245 days. After x days, 75% of original activity remained. The value of x in days is ______. (Nearest integer) (Given: log 3 = 0.4771 and log 2 = 0.3010)',
    None, 102, lambda: round(245 * math.log(4 / 3) / L2),
    ['t = \\f{t_{1/2}}{log 2}log\\f{N_{0}}{N} = \\f{245}{0.3010}log\\f{4}{3}.', 'log\\f{4}{3} = 0.6020 − 0.4771 = 0.1249 → t = 245 × 0.415 ≈ 102 days.'], 'first', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'first', 'Consider the following reaction, the rate expression of which is given below: A + B → C, rate = k[A]^{1/2}[B]^{1/2}. The reaction is initiated by taking 1 M concentration of A and B each. If the rate constant (k) is 4.6 × 10^{−2} s^{−1}, then the time taken for A to become 0.1 M is ______ sec. (nearest integer)',
    None, 50, lambda: round(L10 / 4.6e-2),
    ['A and B start equal and are used 1 : 1, so [A] = [B] at all times.', 'Rate = k[A]^{1/2}[A]^{1/2} = k[A] → behaves as first order.', 't = \\f{2.303}{0.046}log\\f{1}{0.1} = 50 s.'], 'first', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'first', 'Consider the two different first order reactions given below: A + B → C (Reaction 1); P → Q (Reaction 2). The ratio of the half life of Reaction 1 : Reaction 2 is 5 : 2. If t_{1} and t_{2} represent the time taken to complete 2/3^{rd} and 4/5^{th} of Reaction 1 and Reaction 2, respectively, then the value of the ratio t_{1} : t_{2} is ______ × 10^{−1} (nearest integer). [Given: log_{10}(3) = 0.477 and log_{10}(5) = 0.699]',
    None, 17, lambda: round(10 * (math.log(3) * 5) / (math.log(5) * 2)),
    ['t = \\f{t_{1/2}}{ln 2}ln\\f{[A]_{0}}{[A]}.', '2/3 complete → 1/3 left → ln 3. 4/5 complete → 1/5 left → ln 5.', '\\f{t_{1}}{t_{2}} = \\f{5 × 0.477}{2 × 0.699} = 1.706 ≈ 17 × 10^{−1}.'], 'first', 2)

# ---------- gas-phase (pressure) kinetics ----------
add(('2025', 'Apr', '2025-04-07', 1), 'gas', 'Reaction A(g) → 2B(g) + C(g) is a first order reaction. It was started with pure A. Pressure of system: 160 mm Hg at t = 10 min and 240 mm Hg at t = ∞. Which of the following option is incorrect?',
    ['Rate constant of the reaction is 1.693 min^{−1}', 'The reaction never goes to completion', 'Partial pressure of A after 10 minute is 40 mm Hg', 'Initial pressure of A is 80 mm Hg'], 1,
    lambda: [i + 1 for i, ok in enumerate([abs(math.log(80 / 40) / 10 - 1.693) < 1e-3, True, 80 - (160 - 80) / 2 == 40, 240 / 3 == 80]) if not ok][0],
    ['P_{∞} = 3P_{0} → P_{0} = 80 mm Hg (option 4 correct).', 'At 10 min: 80 + 2x = 160 → x = 40 → p_{A} = 80 − 40 = 40 mm Hg (option 3 correct).', 'k = \\f{1}{10}ln\\f{80}{40} = 0.0693 min^{−1}, not 1.693 → option 1 is INCORRECT.', 'A first-order reaction only approaches completion asymptotically (option 2 is acceptable).'], 'gas', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'gas', 'A(g) → B(g) + C(g) is a first order reaction. The total pressure is P_{t} at time t and P_{∞} at t = ∞. The reaction was started with reactant A only. Which of the following expression is correct for rate constant k ?',
    ['k = \\f{1}{t}ln\\f{P_{∞}}{P_{t}}', 'k = \\f{1}{t}ln\\f{2(P_{∞} − P_{t})}{P_{t}}', 'k = \\f{1}{t}ln\\f{P_{∞}}{(P_{∞} − P_{t})}', 'k = \\f{1}{t}ln\\f{P_{∞}}{2(P_{∞} − P_{t})}'], 4, lambda: 4,
    ['P_{∞} = 2P_{0} → P_{0} = P_{∞}/2.', 'P_{t} = P_{0} + x → p_{A} = P_{0} − x = 2P_{0} − P_{t} = P_{∞} − P_{t}.', 'k = \\f{1}{t}ln\\f{P_{0}}{p_{A}} = \\f{1}{t}ln\\f{P_{∞}}{2(P_{∞} − P_{t})}.'], 'gas', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'gas', 'Consider the following first order gas phase reaction at constant temperature A(g) → 2B(g) + C(g). If the total pressure of the gases is found to be 200 torr after 23 sec. and 300 torr upon the complete decomposition of A after a very long time, then the rate constant of the given reaction is ______ × 10^{−2} s^{−1} (nearest integer) [Given : log_{10}(2) = 0.301]',
    None, 3, lambda: round(100 * math.log(100 / (100 - (200 - 100) / 2)) / 23),
    ['P_{∞} = 3P_{0} = 300 → P_{0} = 100 torr.', '100 + 2x = 200 → x = 50 → p_{A} = 50 torr (exactly one half-life).', 'k = \\f{0.693}{23} = 0.0301 s^{−1} = 3 × 10^{−2} s^{−1}.'], 'gas', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'gas', 'Decomposition of A is a first order reaction at T(K) and is given by A(g) → B(g) + C(g). In a closed 1 L vessel, 1 bar A(g) is allowed to decompose at T(K). After 100 minutes, the total pressure was 1.5 bar. What is the rate constant (in min^{−1}) of the reaction? (log 2 = 0.3)',
    ['6.9 × 10^{−1}', '6.9 × 10^{−3}', '6.9 × 10^{−2}', '6.9 × 10^{−4}'], 2, lambda: near([6.9e-1, 6.9e-3, 6.9e-2, 6.9e-4], math.log(1 / (1 - 0.5)) / 100),
    ['1 + x = 1.5 → x = 0.5 → p_{A} = 0.5 bar: one half-life in 100 min.', 'k = \\f{2.303 × 0.3}{100} = 6.9 × 10^{−3} min^{−1}.'], 'gas', 1)
add(('2025', 'Jan', '2025-01-23', 1), 'gas', "For the thermal decomposition of N_{2}O_{5}(g) at constant volume, 2N_{2}O_{5}(g) → 2N_{2}O_{4}(g) + O_{2}(g), the total pressure is 0.6 atm at t = 0 and 'x' at t = 100 s. Given: Rate constant for the reaction is 4.606 × 10^{−2} s^{−1}. x = ______ × 10^{−3} atm [nearest integer]",
    None, 897, lambda: round(1000 * (0.6 * math.exp(-4.606) + (0.6 - 0.6 * math.exp(-4.606)) * 1.5)),
    ['First order in N_{2}O_{5}: kt = 4.606 = 2 × 2.303 → N_{2}O_{5} falls 100 times → p = 0.006 atm.', 'Decomposed 0.594 atm gives 0.594 atm N_{2}O_{4} + 0.297 atm O_{2}.', 'Total = 0.006 + 0.594 + 0.297 = 0.897 atm = 897 × 10^{−3} atm.'], 'gas', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'gas', 'First order gas phase reaction A → B + C. p_{i} = initial pressure of gas A, p_{t} = total pressure of the reaction mixture at time t. Expression of rate constant (k) is',
    ['\\f{1}{t}ln\\f{p_{i}}{2p_{i} − p_{t}}', '\\f{1}{t}ln\\f{2p_{i}}{p_{i} − p_{t}}', '\\f{1}{t}ln\\f{p_{i}}{3p_{i} − 2p_{t}}', '\\f{1}{t}ln\\f{3p_{i}}{4p_{i} − p_{t}}'], 1, lambda: 1,
    ['p_{t} = p_{i} + x → x = p_{t} − p_{i}.', 'p_{A} = p_{i} − x = 2p_{i} − p_{t}.', 'k = \\f{1}{t}ln\\f{p_{i}}{2p_{i} − p_{t}}.'], 'gas', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'gas', 'The following data were obtained during the first order thermal decomposition of a gas A at constant volume: A(g) → 2B(g) + C(g). Total pressure 0.1 atm at t = 0 and 0.28 atm at t = 115 s. The rate constant of the reaction is ______ × 10^{−2} s^{−1} (nearest integer)',
    None, 2, lambda: round(100 * math.log(0.1 / (0.1 - (0.28 - 0.1) / 2)) / 115),
    ['0.1 + 2x = 0.28 → x = 0.09 → p_{A} = 0.01 atm (fallen 10 times).', 'k = \\f{2.303}{115}log 10 = 0.02 s^{−1} = 2 × 10^{−2} s^{−1}.'], 'gas', 2)

# ---------- zero order & half-life ----------
add(('2025', 'Apr', '2025-04-04', 2), 'zero', 'Half life of zero order reaction A → product is 1 hour, when initial concentration of reactant is 2.0 mol L^{−1}. The time required to decrease concentration of A from 0.50 to 0.25 mol L^{−1} is :',
    ['0.5 hour', '15 min', '4 hour', '60 min'], 2, lambda: pick(['0.5 hour', '15 min', '4 hour', '60 min'], f'{round((0.5 - 0.25) / (2.0 / (2 * 1)) * 60)} min'),
    ['Zero order: t_{1/2} = \\f{[A]_{0}}{2k} → k = \\f{2.0}{2 × 1} = 1 mol L^{−1} h^{−1}.', 'Time = \\f{Δ[A]}{k} = \\f{0.25}{1} = 0.25 h = 15 min.'], 'zero', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'zero', 'For a given reaction R → P, t_{1/2} is related to [A]_{0} as given in table: [A]_{0} = 0.100 mol L^{−1}, t_{1/2} = 200 min; [A]_{0} = 0.025 mol L^{−1}, t_{1/2} = 100 min. Given: log 2 = 0.30. Which of the following is true? A. The order of the reaction is 1/2. B. If [A]_{0} is 1 M, then t_{1/2} is 200√{10} min. C. The order of the reaction changes to 1 if the concentration of reactant changes from 0.100 M to 0.500 M. D. t_{1/2} is 800 min for [A]_{0} = 1.6 M.',
    ['A, B and D Only', 'A and B Only', 'C and D Only', 'A and C Only'], 1,
    lambda: combo(['A, B and D Only', 'A and B Only', 'C and D Only', 'A and C Only'], dict(A=abs(1 - math.log(2) / math.log(4) - 0.5) < 1e-9, B=abs(200 * 10 ** 0.5 - 200 * math.sqrt(10)) < 1e-9, C=False, D=abs(200 * (1.6 / 0.1) ** 0.5 - 800) < 1e-9)),
    ['t_{1/2} ∝ [A]_{0}^{1 − n}. [A]_{0} ×4 gives t_{1/2} ×2 → 4^{1 − n} = 2 → n = ½ (A true).', '[A]_{0} = 1 M is 10 × 0.1 → t_{1/2} = 200√{10} min (B true).', 'Order does not change with concentration (C false).', '1.6 M is 16 × 0.1 → t_{1/2} = 200 × 4 = 800 min (D true).'], 'zero', 2)

# ---------- temperature & Arrhenius ----------
add(('2026', 'Apr', '2026-04-02', 1), 'arr', 'For reaction A → P, rate constant k = 1.5 × 10^{3} s^{−1} at 27 °C. If activation energy for the above reaction is 60 kJ mol^{−1}, then the temperature (in °C) at which rate constant, k = 4.5 × 10^{3} s^{−1} is ______. (Nearest integer) Given : log 2 = 0.30, log 3 = 0.48, R = 8.3 J K^{−1} mol^{−1}, ln 10 = 2.3',
    None, 41, lambda: round(1 / (1 / 300 - 0.48 * 2.3 * 8.3 / 60000) - 273),
    ['log\\f{k_{2}}{k_{1}} = \\f{E_{a}}{2.3R}(\\f{1}{T_{1}} − \\f{1}{T_{2}}), with k_{2}/k_{1} = 3.', '0.48 = \\f{60000}{2.3 × 8.3}(\\f{1}{300} − \\f{1}{T_{2}}) → \\f{1}{300} − \\f{1}{T_{2}} = 1.527 × 10^{−4}.', 'T_{2} ≈ 314.4 K = 41 °C.'], 'arr', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'arr', 'Pre-exponential factors of two different reactions of same order are identical. Let activation energy of first reaction exceeds the activation energy of second reaction by 20 kJ mol^{−1}. If k_{1} and k_{2} are the rate constants of first and second reaction respectively at 300 K, then ln\\f{k_{2}}{k_{1}} will be ______ (nearest integer) [R = 8.3 J K^{−1} mol^{−1}]',
    None, 8, lambda: round(20000 / (8.3 * 300)),
    ['k = Ae^{−E_{a}/RT} with the same A.', 'ln\\f{k_{2}}{k_{1}} = \\f{E_{a1} − E_{a2}}{RT} = \\f{20000}{8.3 × 300} = 8.03 ≈ 8.'], 'arr', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'arr', 'A → B (first reaction), C → D (second reaction). Consider the above two first-order reactions. The rate constant for first reaction at 500 K is double of the same at 300 K. At 500 K, 50% of the reaction becomes complete in 2 hour. The activation energy of the second reaction is half of that of first reaction. If the rate constant at 500 K of the second reaction becomes double of the rate constant of first reaction at the same temperature; then rate constant for the second reaction at 300 K is ______ × 10^{−1} hour^{−1} (Nearest integer).',
    None, 5, lambda: round(10 * 2 * (L2 / 2) / math.sqrt(2)),
    ['First reaction at 500 K: t_{1/2} = 2 h → k_{1} = 0.3465 h^{−1}.', 'Its ratio k(500)/k(300) = 2 = e^{E_{a}X} (X = \\f{1}{R}(\\f{1}{300} − \\f{1}{500})). Half the E_{a} → ratio e^{E_{a}X/2} = √{2}.', 'Second reaction: k_{2}(500) = 2 × 0.3465 = 0.693 h^{−1} → k_{2}(300) = \\f{0.693}{1.414} = 0.49 ≈ 5 × 10^{−1} h^{−1}.'], 'arr', 3)
add(('2024', 'Jan', '2024-01-29', 1), 'arr', 'For a reaction taking place in three steps at same temperature, overall rate constant K = \\f{K_{1}K_{2}}{K_{3}}. If Ea_{1}, Ea_{2} and Ea_{3} are 40, 50 and 60 kJ/mol respectively, the overall Ea is ______ kJ/mol.',
    None, 30, lambda: 40 + 50 - 60,
    ['Each K = Ae^{−E/RT}: multiplying constants ADDS their activation energies, dividing SUBTRACTS.', 'E_{a} = 40 + 50 − 60 = 30 kJ/mol.'], 'arr', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'arr', 'Consider the following transformation involving first order elementary reaction in each step at constant temperature: A + B ⇌ C (step 1 forward, step 3 backward), C → P (step 2). Activation energies: step 1 = 300, step 2 = 200, step 3 = Ea_{3} kJ mol^{−1}. If the overall rate constant of the above transformation (k) is given as k = \\f{k_{1}k_{2}}{k_{3}} and the overall activation energy (E_{a}) is 400 kJ mol^{−1}, then the value of Ea_{3} is ______ kJ mol^{−1} (nearest integer)',
    None, 100, lambda: 300 + 200 - 400,
    ['E_{a} = E_{1} + E_{2} − E_{3}.', '400 = 300 + 200 − E_{3} → E_{3} = 100 kJ mol^{−1}.'], 'arr', 1)
add(('2025', 'Jan', '2025-01-24', 2), 'arr', 'Consider a complex reaction taking place in three steps with rate constants k_{1}, k_{2} and k_{3} respectively. The overall rate constant k is given by the expression k = √{\\f{k_{1}k_{3}}{k_{2}}}. If the activation energies of the three steps are 60, 30 and 10 kJ mol^{−1} respectively, then the overall energy of activation in kJ mol^{−1} is ______. (Nearest integer)',
    None, 20, lambda: round((60 + 10 - 30) / 2),
    ['Taking logs: ln k = ½(ln k_{1} + ln k_{3} − ln k_{2}) → E_{a} = ½(E_{1} + E_{3} − E_{2}).', 'E_{a} = ½(60 + 10 − 30) = 20 kJ mol^{−1}.'], 'arr', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'arr', 'Consider A →(k_{1}) B and C →(k_{2}) D are two reactions. If the rate constant (k_{1}) of the A → B reaction can be expressed by the following equation log_{10} k = 14.34 − \\f{1.5 × 10^{4}}{T/K} and activation energy of C → D reaction (Ea_{2}) is \\f{1}{5}th of the A → B reaction (Ea_{1}), then the value of (Ea_{2}) is ______ kJ mol^{−1}. (Nearest Integer)',
    None, 57, lambda: round(1.5e4 * 2.303 * 8.314 / 1000 / 5),
    ['Compare with log k = log A − \\f{E_{a}}{2.303RT}: \\f{E_{a1}}{2.303R} = 1.5 × 10^{4} K.', 'E_{a1} = 1.5 × 10^{4} × 2.303 × 8.314 = 287.2 kJ mol^{−1}.', 'E_{a2} = \\f{287.2}{5} = 57.4 ≈ 57 kJ mol^{−1}.'], 'arr', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'arr', 'At 27 °C in presence of a catalyst, activation energy of a reaction is lowered by 10 kJ mol^{−1}. The logarithm of ratio of \\f{k (catalysed)}{k (uncatalysed)} is.... (Consider that the frequency factor for both the reactions is same)',
    ['17.41', '1.741', '3.482', '0.1741'], 2, lambda: near([17.41, 1.741, 3.482, 0.1741], 10000 / (2.303 * 8.314 * 300)),
    ['log\\f{k_{cat}}{k} = \\f{ΔE_{a}}{2.303RT} (same A).', '= \\f{10000}{2.303 × 8.314 × 300} = 1.741.'], 'arr', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'arr', 'The temperature at which the rate constants of the given below two gaseous reactions become equal is ______ K. (Nearest integer) X → Y: k_{1} = 10^{6}e^{−30000/T}; P → Q: k_{2} = 10^{4}e^{−24000/T}. Given: ln 10 = 2.303',
    None, 1303, lambda: round(6000 / (2 * 2.303)),
    ['10^{6}e^{−30000/T} = 10^{4}e^{−24000/T} → 100 = e^{6000/T}.', '\\f{6000}{T} = 2 × 2.303 → T = \\f{6000}{4.606} ≈ 1303 K.'], 'arr', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'arr', 'Given below are two statements : R = 8.314 J K^{−1} mol^{−1} and 1 cal = 4.2 J. Statement I: When Ea = 12.6 kcal/mol, the room temperature rate constant is doubled by a 10 °C increase in temperature (298 K to 308 K). Statement II: For a first order reaction A → B, a plot of t_{1/2} (s) against [A]_{0} (mol L^{−1}) is a straight line through the origin with positive slope.',
    ST, 3, lambda: st(abs(math.exp(12.6 * 4200 / 8.314 * (1 / 298 - 1 / 308)) - 2) < 0.02, False),
    ['I: E_{a} = 12.6 × 4.2 = 52.92 kJ. ln\\f{k_{2}}{k_{1}} = \\f{52920}{8.314}(\\f{1}{298} − \\f{1}{308}) = 0.693 → k doubles. TRUE.', 'II: first-order t_{1/2} = 0.693/k does not depend on [A]_{0} — the plot is a horizontal line. FALSE.'], 'arr', 2)
add(('2026', 'Jan', '2026-01-22', 2), 'arr', 'Correct statements regarding Arrhenius equation among the following are : A. Factor e^{−Ea/RT} corresponds to fraction of molecules having kinetic energy less than Ea. B. At a given temperature, lower the Ea, faster is the reaction. C. Increase in temperature by about 10 °C doubles the rate of reaction. D. Plot of log k vs \\f{1}{T} gives a straight line with slope = −\\f{Ea}{R}.',
    ['B and D Only', 'A and B Only', 'A and C Only', 'B and C Only'], 4, lambda: combo(['B and D Only', 'A and B Only', 'A and C Only', 'B and C Only'], dict(A=False, B=True, C=True, D=False)),
    ['A false: e^{−E_{a}/RT} is the fraction with energy EQUAL TO OR MORE than E_{a}.', 'B true. C true (the usual rule of thumb).', 'D false: slope of log k vs 1/T is −\\f{E_{a}}{2.303R}; −E_{a}/R is the slope for ln k.'], 'arr', 2)
add(('2025', 'Apr', '2025-04-03', 2), 'arr', 'Consider the following statements related to temperature dependence of rate constants. Identify the correct statements. A. The Arrhenius equation holds true only for an elementary homogenous reaction. B. The unit of A is same as that of k in Arrhenius equation. C. At a given temperature, a low activation energy means a fast reaction. D. A and Ea as used in Arrhenius equation depend on temperature. E. When Ea >> RT, A and Ea become interdependent.',
    ['B and C Only', 'B, D and E Only', 'A and B Only', 'A, C and D Only'], 1, lambda: combo(['B and C Only', 'B, D and E Only', 'A and B Only', 'A, C and D Only'], dict(A=False, B=True, C=True, D=False, E=False)),
    ['A false: it also describes complex and heterogeneous reactions (with apparent E_{a}).', 'B true: e^{−E_{a}/RT} has no unit, so A has the unit of k. C true.', 'D false: A and E_{a} are treated as temperature-independent. E false: they are independent constants.'], 'arr', 2)

if __name__ == '__main__': print(verify(P), 'real questions verified')
