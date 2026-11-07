"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 8 Basic Applications of Differential and Integral Calculus in Business and Economics.
Original explanations, numbers and questions (scope and order follow the ICAI study material).
Every derivative and integral used in a numeric answer is confirmed here symbolically by hand-coded polynomials
or numerically, and stored with an arithmetic check the validator re-evaluates."""
from fractions import Fraction as F
import math
from lib import *
import re
from ca_viva import P, V

UID = 'fnd-p3-ch08-u01'


def ev(expr):
    v = eval(expr, {'__builtins__': {}}, {'round': round})
    v = round(v, 2)
    return int(v) if v == int(v) else v


def fmt(x):
    if isinstance(x, str): return x
    if isinstance(x, float) and x != int(x): return f'{x:g}'
    return inr(int(x))


def mq(mid, q, right, wrong, explain, concept, diff='core', check=None):
    assert len(wrong) == 3, mid
    k = sum(map(ord, mid)) % 4
    opts = [fmt(w) for w in wrong]
    opts.insert(k, fmt(right))
    d = {'id': mid, 'q': q, 'options': opts, 'answer': k, 'explain': explain, 'concept': concept, 'difficulty': diff}
    if check is not None:
        v = ev(check)
        assert abs(v - float(re.match(r'[₹\s]*(-?[\d,]*\.?\d+)', str(right)).group(1).replace(',', ''))) < 0.006, (mid, check, v, right)
        d['check'] = check
    return d


# --- tiny polynomial toolkit (coefficients low → high) used only to confirm the hand-written working ---
def pval(c, x): return sum(F(a) * F(x) ** i for i, a in enumerate(c))
def pder(c): return [i * a for i, a in enumerate(c)][1:]
def pint(c): return [F(0)] + [F(a) / (i + 1) for i, a in enumerate(c)]
def nder(f, x, h=1e-6): return (f(x + h) - f(x - h)) / (2 * h)
def nint(f, a, b, n=20000):
    h = (b - a) / n
    return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, n)) + f(b) / 2)


def build():
    # ------------------------------------------------------------------ i1 first principle
    c1 = Checks()
    c1.add('6*2+2', 'derivative of 3x² + 2x at x = 2, i.e. 6x + 2')
    c1.add('-1/2**2', 'derivative of 1/x at x = 2, i.e. −1/x²')
    f = lambda x: 3 * x * x + 2 * x
    assert abs((f(2 + 1e-7) - f(2)) / 1e-7 - 14) < 1e-4

    # ------------------------------------------------------------------ i2 rules
    c2 = Checks()
    c2.add('12*1**2-10*1+7', '(a) 12x² − 10x + 7 at x = 1')
    c2.add('-5/(2-1)**2', '(c) −5/(x − 1)² at x = 2')
    c2.add('30*1*(3*1**2+1)**4', '(d) 30x(3x² + 1)⁴ at x = 1')
    c2.add('2*2/(2**2+4)', '(e) 2x/(x² + 4) at x = 2')
    assert abs(nder(lambda x: x * x * math.exp(x), 1) - 3 * math.e) < 1e-5
    assert abs(nder(lambda x: (2 * x + 3) / (x - 1), 2) - (-5)) < 1e-5
    assert abs(nder(lambda x: (3 * x * x + 1) ** 5, 1) - 7680) < 1e-2
    assert abs(nder(lambda x: math.log(x * x + 4), 2) - 0.5) < 1e-6

    # ------------------------------------------------------------------ i3 implicit, parametric, logarithmic
    c3 = Checks()
    c3.add('-3/4', 'slope of x² + y² = 25 at (3, 4)')
    c3.add('1/2', 'dy/dx = 1/t at t = 2 for x = 2t², y = 4t')
    c3.add('2**2*(1+0.6931)', 'derivative of xˣ at x = 2 ≈ 4(1 + logₑ2)')
    assert abs(nder(lambda x: x ** x, 2) - 4 * (1 + math.log(2))) < 1e-5

    # ------------------------------------------------------------------ i4 second derivative, gradient, max/min
    y4 = [4, 9, -6, 1]  # x³ − 6x² + 9x + 4
    d4, dd4 = pder(y4), pder(pder(y4))
    assert pval(d4, 1) == 0 and pval(d4, 3) == 0 and pval(dd4, 1) == -6 and pval(dd4, 3) == 6 and pval(y4, 1) == 8 and pval(y4, 3) == 4
    c4 = Checks()
    c4.add('3*0**2-12*0+9', 'gradient at x = 0')
    c4.add('6*1-12', 'second derivative at x = 1 (negative → maximum)')
    c4.add('6*3-12', 'second derivative at x = 3 (positive → minimum)')
    c4.add('1-6+9+4', 'maximum value y(1)')
    c4.add('27-54+27+4', 'minimum value y(3)')

    # ------------------------------------------------------------------ i5 cost, revenue, profit
    c5 = Checks()
    x_ac = c5.add('(5000/2)**0.5', 'output where AC is least: 2 − 5000/x² = 0')
    ac_min = c5.add('2*50+40+5000/50', 'least average cost')
    mc50 = c5.add('4*50+40', 'MC at x = 50 (equals least AC)')
    x_p = c5.add('360/10', 'profit-maximising output: 360 − 10x = 0')
    price = c5.add('400-3*36', 'price at that output')
    pmax = c5.add('360*36-5*36**2-5000', 'maximum profit')
    c5.add('400-6*36', 'MR at x = 36')
    c5.add('4*36+40', 'MC at x = 36 (MR = MC)')
    Pp = lambda x: (400 - 3 * x) * x - (2 * x * x + 40 * x + 5000)
    assert max(range(0, 120), key=Pp) == 36 and Pp(36) == 1480
    assert min(range(1, 200), key=lambda x: 2 * x + 40 + 5000 / x) == 50

    # ------------------------------------------------------------------ i6 break-even
    c6 = Checks()
    bep = c6.add('360000/(750-450)', 'break-even output')
    p1500 = c6.add('(750-450)*1500-360000', 'profit at 1,500 units')
    c6.add('360000+450*1200', 'cost at break-even = revenue 750 × 1,200')
    c6.add('750*1200', 'revenue at break-even')

    # ------------------------------------------------------------------ i7 indefinite integrals (checked by differentiating numerically)
    c7 = Checks()
    c7.add('4-(-1+5)/(-1+2)', 'A − 4 = 0 where A = (x + 5)/(x + 2) at x = −1')
    c7.add('(-2+5)/(-2+1)', 'B = (x + 5)/(x + 1) at x = −2')
    tests = [
        (lambda x: 2 * x ** 3 - 2 * x ** 2 + 5 * x, lambda x: 6 * x * x - 4 * x + 5),
        (lambda x: (2 * x + 3) ** 5 / 10, lambda x: (2 * x + 3) ** 4),
        (lambda x: math.exp(x) * (x - 1), lambda x: x * math.exp(x)),
        (lambda x: math.log(abs((x - 3) / (x + 3))) / 6, lambda x: 1 / (x * x - 9)),
        (lambda x: 4 * math.log(x + 1) - 3 * math.log(x + 2), lambda x: (x + 5) / ((x + 1) * (x + 2))),
        (lambda x: math.log(x + math.sqrt(x * x + 4)), lambda x: 1 / math.sqrt(x * x + 4)),
    ]
    for Fn, fn in tests:
        for x0 in (0.5, 1.7, 4.2):
            assert abs(nder(Fn, x0) - fn(x0)) < 1e-4

    # ------------------------------------------------------------------ i8 definite integrals
    c8 = Checks()
    d8a = c8.add('(3**3+3**2)-(1**3+1**2)', '∫₁³ (3x² + 2x) dx')
    c8.add('2**3/3', '∫₀² x² dx')
    c8.add('(2**4-(-2)**4)/4', '∫₋₂² x³ dx (odd function)')
    c8.add('2*(1/3)', '∫₋₁¹ x² dx = 2∫₀¹ x² dx')
    area = c8.add('2*4**2-4**3/3', 'area under y = 4x − x² from 0 to 4')
    assert abs(nint(lambda x: 3 * x * x + 2 * x, 1, 3) - 34) < 1e-6
    assert abs(nint(lambda x: 4 * x - x * x, 0, 4) - 32 / 3) < 1e-6

    # ------------------------------------------------------------------ i9 marginal → total
    mc9 = [40, -12, 3]           # 3x² − 12x + 40
    tc9 = pint(mc9); tc9[0] = F(500)
    c9 = Checks()
    tc10 = c9.add('10**3-6*10**2+40*10+500', 'total cost of 10 units')
    assert pval(tc9, 10) == tc10
    inc = c9.add('(8**3-6*8**2+40*8)-(4**3-6*4**2+40*4)', 'extra cost when output rises from 4 to 8')
    assert pval(tc9, 8) - pval(tc9, 4) == inc == 320
    c9.add('100-2*10', 'price for 10 units from p = 100 − 2x')
    c9.add('3*2**2-12*2+40', 'least MC (at x = 2)')

    # ------------------------------------------------------------------ jobs
    cj1 = Checks()
    j_x = cj1.add('600/6', 'profit-maximising output: 600 − 6x = 0')
    j_p = cj1.add('700-2*100', 'price')
    j_pr = cj1.add('600*100-3*100**2-15000', 'maximum profit')
    cj2 = Checks()
    j_inc = cj2.add('(30**2+50*30)-(20**2+50*20)', 'extra cost (₹ thousand) from 20 to 30 units with MC = 2x + 50')

    # ------------------------------------------------------------------ questions
    qc1 = Checks()
    qc1.add('9*1**2-4*1+3', "(a) y′ = 9x² − 4x + 3 at x = 1")
    qc1.add('-7/(2*1-1)**2', '(b) −7/(2x − 1)² at x = 1')
    assert abs(nder(lambda x: (x * x + 1) * (3 * x - 2), 1) - 8) < 1e-6
    assert abs(nder(lambda x: (3 * x + 2) / (2 * x - 1), 1) + 7) < 1e-5

    qc2 = Checks()
    q2x = qc2.add('120/3', 'profit-maximising output: 120 − 3x = 0')
    q2p = qc2.add('150-40', 'price at x = 40')
    q2pr = qc2.add('120*40-1.5*40**2-1800', 'maximum profit')
    q2ac = qc2.add('(1800/0.5)**0.5', 'output with least AC: 0.5 − 1800/x² = 0')
    q2acm = qc2.add('0.5*60+30+1800/60', 'least AC')
    q2mc = qc2.add('60+30', 'MC at x = 60')
    Pq = lambda x: (150 - x) * x - (0.5 * x * x + 30 * x + 1800)
    assert max(range(0, 150), key=Pq) == 40 and abs(Pq(40) - 600) < 1e-9

    qc3 = Checks()
    q3b = qc3.add('1/5-1/6', '(b) ∫₀¹ x(1 − x)⁴ dx = ∫₀¹ (1 − x)x⁴ dx')
    q3c = qc3.add('6**3-4*6**2+10*6+60', '(c) total cost of 6 units')
    q3ac = qc3.add('192/6', '(c) average cost at 6 units')
    assert abs(nint(lambda x: x * (1 - x) ** 4, 0, 1) - 1 / 30) < 1e-7

    # ------------------------------------------------------------------ case
    ck = Checks()
    k_x = ck.add('800/10', 'profit-maximising output: 800 − 10x = 0')
    k_p = ck.add('1000-3*80', 'price')
    k_pr = ck.add('800*80-5*80**2-12000', 'maximum profit')
    k_mr = ck.add('1000-6*80', 'MR at 80')
    Pk = lambda x: (1000 - 3 * x) * x - (2 * x * x + 200 * x + 12000)
    assert max(range(0, 300), key=Pk) == 80 and Pk(80) == 20000

    # ------------------------------------------------------------------ MCQs
    M = []
    M.append(mq('m1', 'The gradient (slope of the tangent) of the curve y = x³ − 4x² + 7x − 2 at x = 2 is:', 3, [4, 7, -1], 'dy/dx = 3x² − 8x + 7 = 12 − 16 + 7 = 3. 4 is the value of y at x = 2, not the slope.', 'c5', 'core', '3*2**2-8*2+7'))
    M.append(mq('m2', 'd/dx (e⁴ˣ) equals:', '4e⁴ˣ', ['e⁴ˣ', 'e⁴ˣ/4', '4xe⁴ˣ⁻¹'], 'd/dx (eᵃˣ) = a eᵃˣ. Treating eˣ like a power xⁿ gives the wrong last option.', 'c2', 'core'))
    M.append(mq('m3', 'd/dx (5ˣ) equals:', '5ˣ logₑ5', ['x · 5ˣ⁻¹', '5ˣ', '5ˣ/logₑ5'], 'd/dx (aˣ) = aˣ logₑa. The power rule applies only when the variable is in the base.', 'c2', 'core'))
    M.append(mq('m4', 'The derivative of x³ logₑx is:', 'x²(1 + 3 logₑx)', ['3x²/x', '3x² logₑx', 'x²(3 + logₑx)'], 'Product rule: x³ × 1/x + logₑx × 3x² = x² + 3x² logₑx = x²(1 + 3 logₑx).', 'c3', 'moderate'))
    M.append(mq('m5', 'd/dx [x/(x + 1)] equals:', '1/(x + 1)²', ['−1/(x + 1)²', '1/(x + 1)', 'x/(x + 1)²'], 'Quotient rule: [(x + 1)(1) − x(1)]/(x + 1)² = 1/(x + 1)².', 'c3', 'core'))
    M.append(mq('m6', 'd/dx (2x + 1)⁶ equals:', '12(2x + 1)⁵', ['6(2x + 1)⁵', '12(2x + 1)⁶', '2(2x + 1)⁵'], 'Chain rule: 6(2x + 1)⁵ × d/dx(2x + 1) = 12(2x + 1)⁵. Forgetting the inner derivative gives 6(2x + 1)⁵.', 'c3', 'core'))
    M.append(mq('m7', 'If y = eˣ + e⁻ˣ, then d²y/dx² equals:', 'y', ['−y', '0', 'eˣ − e⁻ˣ'], 'y′ = eˣ − e⁻ˣ, y″ = eˣ + e⁻ˣ = y. (eˣ − e⁻ˣ is only the first derivative.)', 'c5', 'moderate'))
    M.append(mq('m8', 'The value of the second derivative of y = x⁴ at x = 1 is:', 12, [4, 24, 1], 'y′ = 4x³, y″ = 12x², which is 12 at x = 1.', 'c5', 'core', '12*1**2'))
    M.append(mq('m9', 'If xy = 16, then dy/dx equals:', '−y/x', ['y/x', '−x/y', '16/x'], 'Differentiate implicitly: x dy/dx + y = 0 → dy/dx = −y/x (= −16/x²).', 'c4', 'moderate'))
    M.append(mq('m10', 'If x = t² and y = t³, then dy/dx equals:', '3t/2', ['2t/3', '3t²', 't'], 'dy/dx = (dy/dt)/(dx/dt) = 3t²/(2t) = 3t/2.', 'c4', 'moderate'))
    M.append(mq('m11', 'The total cost of x units is C = 0.02x³ − 0.5x² + 10x + 200. The marginal cost at x = 10 is:', 6, [20, 270, 16], 'MC = 0.06x² − x + 10 = 6 − 10 + 10 = 6. 270 is the total cost of 10 units — do not confuse total with marginal; 16 forgets the −x term.', 'c6', 'moderate', '0.06*10**2-10+10'))
    M.append(mq('m12', 'Total revenue is R = 50x − 0.5x². Marginal revenue at x = 20 is:', 30, [800, 40, 10], 'MR = 50 − x = 30. 800 is total revenue at 20 units.', 'c6', 'core', '50-20'))
    M.append(mq('m13', 'Fixed cost ₹2,40,000, variable cost ₹60 per unit, selling price ₹100 per unit. The break-even output is:', 6000, [4000, 2400, 1500], 'At break-even R = C: 100x = 2,40,000 + 60x → x = 2,40,000/40 = 6,000. Dividing by 60 or by 100 is the usual slip.', 'c6', 'core', '240000/(100-60)'))
    M.append(mq('m14', 'Profit is P(x) = −2x² + 120x − 500. Profit is maximum at x =', 30, [60, 120, 15], 'P′ = −4x + 120 = 0 → x = 30; P″ = −4 < 0 confirms a maximum.', 'c6', 'core', '120/4'))
    M.append(mq('m15', 'Total cost is C = x² + 16 (x units). Average cost is least at x =', 4, [16, 8, 2], 'AC = x + 16/x; AC′ = 1 − 16/x² = 0 → x = 4 (least AC = 8).', 'c6', 'hard', '16**0.5'))
    M.append(mq('m16', 'The consumption function is C = 400 + 0.7Y. The marginal propensity to save is:', 0.3, [0.7, 400, 1.7], 'MPC = dC/dY = 0.7. Since Y = C + S, MPS = 1 − MPC = 0.3.', 'c6', 'moderate', '1-0.7'))
    M.append(mq('m17', '∫ x⁴ dx equals:', 'x⁵/5 + c', ['4x³ + c', 'x⁵ + c', '5x⁵ + c'], 'Raise the power by one and divide by the new power. 4x³ is the derivative, not the integral.', 'c7', 'core'))
    M.append(mq('m18', '∫ (1/x) dx equals:', 'logₑ|x| + c', ['x⁰/0 + c', '−1/x² + c', '1/x² + c'], 'The power formula fails for n = −1; the integral of 1/x is logₑ|x| + c.', 'c7', 'core'))
    M.append(mq('m19', '∫ e³ˣ dx equals:', 'e³ˣ/3 + c', ['3e³ˣ + c', 'e³ˣ + c', 'e⁴ˣ/4 + c'], '∫ eᵃˣ dx = eᵃˣ/a + c — divide by a when integrating, multiply when differentiating.', 'c7', 'core'))
    M.append(mq('m20', '∫₀² (3x² + 1) dx equals:', 10, [8, 13, 12], '[x³ + x]₀² = 8 + 2 = 10.', 'c9', 'core', '2**3+2'))
    M.append(mq('m21', '∫₁⁴ √x dx equals:', '14/3', ['7/3', '16/3', '2'], '[(2/3)x^(3/2)]₁⁴ = (2/3)(8 − 1) = 14/3.', 'c9', 'moderate'))
    M.append(mq('m22', '∫₋₃³ x⁵ dx equals:', 0, [243, 486, 121.5], 'x⁵ is an odd function (f(−x) = −f(x)), so its integral over [−a, a] is 0.', 'c9', 'moderate', '(3**6-(-3)**6)/6'))
    M.append(mq('m23', '∫ x eˣ dx equals:', 'eˣ(x − 1) + c', ['x eˣ + c', 'eˣ(x + 1) + c', 'x²eˣ/2 + c'], 'By parts with u = x: x eˣ − ∫ eˣ dx = eˣ(x − 1) + c.', 'c8', 'moderate'))
    M.append(mq('m24', 'Marginal cost is MC = 2x + 5 and fixed cost is ₹100. The total cost of 10 units is:', '₹250', ['₹150', '₹25', '₹125'], 'TC = x² + 5x + 100 (the constant of integration is the fixed cost). At x = 10: 100 + 50 + 100 = ₹250.', 'c10', 'core', '10**2+5*10+100'))
    M.append(mq('m25', 'Marginal revenue is MR = 40 − 2x. The demand (price) function is:', 'p = 40 − x', ['p = 40 − 2x', 'p = 40x − x²', 'p = −2'], 'R = ∫ MR dx = 40x − x² (no constant, since R = 0 when x = 0). p = R/x = 40 − x.', 'c10', 'moderate'))
    M.append(mq('m26', '∫ 2x/(x² + 1) dx equals:', 'logₑ(x² + 1) + c', ['x²/(x³/3 + x) + c', '2 logₑ(x² + 1) + c', '1/(x² + 1) + c'], 'Substitute t = x² + 1, dt = 2x dx: ∫ dt/t = logₑ t + c.', 'c8', 'moderate'))
    M.append(mq('m27', 'Using the first principle, the derivative of a constant function f(x) = k is:', '0', ['k', '1', 'Not defined'], 'f(x + h) − f(x) = k − k = 0 for every h, so the limit of 0/h is 0.', 'c1', 'core'))
    M.append(mq('m28', 'The maximum value of y = −x² + 6x + 5 is:', 14, [3, 5, 9], 'y′ = −2x + 6 = 0 → x = 3; y″ = −2 < 0. y(3) = −9 + 18 + 5 = 14. (3 is where the maximum occurs, not its value.)', 'c6', 'moderate', '-3**2+6*3+5'))
    M.append(mq('m29', 'MC = 4x + 10. The increase in total cost when output rises from 10 to 20 units is:', 700, [1000, 300, 50], '∫₁₀²⁰ (4x + 10) dx = [2x² + 10x]₁₀²⁰ = 1000 − 300 = 700.', 'c10', 'moderate', '(2*20**2+10*20)-(2*10**2+10*10)'))
    M.append(mq('m30', 'At the output where profit is maximum (with the second-order condition met):', 'MR = MC', ['MR = 0', 'AC = MC', 'TR = TC'], 'P′ = R′ − C′ = 0 gives MR = MC. TR = TC is break-even; AC = MC marks the least average cost.', 'c6', 'core'))

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch08', 'n': 1,
        'title': 'Basic Applications of Differential and Integral Calculus in Business and Economics',
        'outcomes': [
            'Explain the derivative as a rate of change and find it from the first principle for simple functions.',
            'Differentiate using standard results and the sum, product, quotient and chain rules, including implicit, parametric and logarithmic differentiation and second-order derivatives.',
            'Interpret the derivative as the gradient of a curve and use first and second derivatives to locate maxima and minima.',
            'Apply derivatives to cost, revenue and profit: average and marginal cost, marginal revenue, break-even, profit maximisation, MPC and MPS.',
            'Integrate using standard formulae, substitution, partial fractions and integration by parts; evaluate definite integrals and use their properties.',
            'Recover total cost and total revenue (and demand) from marginal functions.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 60, 'practice': 80}, 'prereq': ['fnd-p3-ch07-u01'],
                 'exam_tip': 'Questions are formula-driven: learn the standard derivative and integral tables cold. In applications, write the function you are differentiating (R, C or P) before you differentiate — most errors come from differentiating the wrong one.'},
        'concepts': [
            {'id': 'c1', 'title': 'The derivative and the first principle',
             'body': ['If y = f(x) and x changes by a small amount h, y changes by f(x + h) − f(x). The average rate of change is [f(x + h) − f(x)]/h. Its limit as h → 0 is the derivative, written dy/dx, f′(x) or d/dx f(x) (also called the differential coefficient).',
                      'Finding the derivative straight from this limit is called differentiation from the first principle (ab initio). Example: for f(x) = x², [(x + h)² − x²]/h = 2x + h → 2x.',
                      'f is differentiable at x = c if this limit exists there. A function that is differentiable at a point is continuous there (the converse is not always true).'],
             'analogy': 'A car\'s speedometer shows the derivative of distance with respect to time — the rate at this instant, not the average for the whole trip.',
             'work': 'Every "marginal" figure in economics and costing — marginal cost, marginal revenue, marginal propensity to consume — is a derivative.'},
            {'id': 'c2', 'title': 'Standard derivatives',
             'body': ['d/dx (xⁿ) = nxⁿ⁻¹ (any real n); d/dx (k) = 0 for a constant k.',
                      'd/dx (eˣ) = eˣ; d/dx (eᵃˣ) = a eᵃˣ; d/dx (aˣ) = aˣ logₑa; d/dx (logₑx) = 1/x.',
                      'd/dx [k f(x)] = k f′(x) — constants come out of the derivative.'],
             'blocks': [table(['f(x)', 'f′(x)'], [['xⁿ', 'nxⁿ⁻¹'], ['k (constant)', '0'], ['eˣ', 'eˣ'], ['eᵃˣ', 'a eᵃˣ'], ['aˣ', 'aˣ logₑa'], ['logₑx', '1/x'], ['√x', '1/(2√x)'], ['1/x', '−1/x²']])],
             'analogy': 'The table is your multiplication table for calculus — you should not have to work these out in the exam hall.',
             'work': 'Spreadsheet growth models use eˣ and aˣ; knowing their rates of change lets you sanity-check a model\'s marginal figures.'},
            {'id': 'c3', 'title': 'Rules of differentiation',
             'body': ['Sum/difference: (f ± g)′ = f′ ± g′.',
                      'Product rule: (fg)′ = f g′ + g f′ — "first × derivative of second + second × derivative of first".',
                      'Quotient rule: (f/g)′ = (g f′ − f g′)/g², g ≠ 0 — "denominator × derivative of numerator − numerator × derivative of denominator, over denominator squared".',
                      'Chain rule (function of a function): if y = f(z) and z = g(x), then dy/dx = (dy/dz)(dz/dx). Example: d/dx (3x² + 1)⁵ = 5(3x² + 1)⁴ × 6x.'],
             'analogy': 'The chain rule is a gear train: if the first gear turns 3 times for each turn of the second, and the second 4 times for each turn of the third, the first turns 12 times per turn of the third.',
             'work': 'Revenue = price × quantity, and both may depend on output — the product rule is how marginal revenue is derived from a demand curve.'},
            {'id': 'c4', 'title': 'Implicit, parametric and logarithmic differentiation',
             'body': ['Implicit: when y is mixed with x in an equation f(x, y) = 0, differentiate every term with respect to x, writing dy/dx wherever y is differentiated (d/dx of y² is 2y dy/dx), then solve for dy/dx.',
                      'Parametric: if x = f(t) and y = h(t), then dy/dx = (dy/dt) ÷ (dx/dt), provided dx/dt ≠ 0.',
                      'Logarithmic: for products of many factors or variable powers such as xˣ, take logₑ of both sides first, differentiate, then multiply back by y. For y = xˣ: logₑy = x logₑx → (1/y) dy/dx = 1 + logₑx → dy/dx = xˣ(1 + logₑx).'],
             'analogy': 'Taking logs first is like converting a multiplication problem into an addition problem before you start — the work becomes simpler.',
             'work': 'Growth-rate analysis (the percentage change of a product of factors) uses logarithmic differentiation: the growth rate of revenue ≈ growth rate of price + growth rate of quantity.'},
            {'id': 'c5', 'title': 'Second derivative and the gradient of a curve',
             'body': ['Differentiating f′(x) again gives the second derivative d²y/dx² = f″(x); further differentiation gives f‴(x), and so on.',
                      'Geometrically, f′(a) is the gradient of the curve y = f(x) at the point where x = a — the steepness of the line that just touches the curve there. Positive gradient → the curve is rising; negative → falling; zero → a stationary point.',
                      'At a stationary point (f′(a) = 0): f″(a) < 0 → local maximum; f″(a) > 0 → local minimum.'],
             'analogy': 'On a road, the first derivative tells you whether you are going uphill or downhill; the second tells you whether the slope is getting steeper or flattening out — at the top of a hill it flattens and then turns down.',
             'work': 'Finding the output that maximises profit or minimises average cost is a stationary-point problem checked with the second derivative.'},
            {'id': 'c6', 'title': 'Applications: cost, revenue, profit, break-even and propensities',
             'body': ['Total cost C(x) = fixed cost + variable cost. Average cost AC = C(x)/x; AVC = V(x)/x; AFC = F/x. Marginal cost MC = dC/dx — approximately the cost of one more unit.',
                      'Revenue R(x) = p × x (p from the demand function). Marginal revenue MR = dR/dx. Profit P(x) = R(x) − C(x); marginal profit = dP/dx.',
                      'Break-even point: R(x) = C(x) (no profit, no loss). Profit maximum: dP/dx = 0, i.e. MR = MC, with d²P/dx² < 0. Average cost is least where AC′ = 0, and at that output AC = MC.',
                      'Consumption function C = f(Y): marginal propensity to consume MPC = dC/dY. Saving S = Y − C, so MPS = dS/dY = 1 − MPC.'],
             'analogy': 'Marginal cost is the price of the next slice of pizza you order; average cost is the bill divided by the slices already eaten.',
             'work': 'Pricing studies, make-or-buy decisions and break-even analysis in cost accounting all use these definitions — the calculus version just gives exact answers for curved cost and demand functions.'},
            {'id': 'c7', 'title': 'Integration — the reverse of differentiation',
             'body': ['If d/dx F(x) = f(x), then ∫ f(x) dx = F(x) + c. The arbitrary constant c is the constant of integration, because constants vanish on differentiation.',
                      'Standard results: ∫ xⁿ dx = xⁿ⁺¹/(n + 1) + c (n ≠ −1); ∫ (1/x) dx = logₑ|x| + c; ∫ eˣ dx = eˣ + c; ∫ eᵃˣ dx = eᵃˣ/a + c; ∫ aˣ dx = aˣ/logₑa + c; ∫ k dx = kx + c.',
                      'Rules: ∫ k f(x) dx = k ∫ f(x) dx; ∫ [f(x) ± g(x)] dx = ∫ f dx ± ∫ g dx. There is no general product or quotient rule — use the methods below.'],
             'analogy': 'Differentiation turns a recipe into a list of ingredients per minute; integration rebuilds the recipe — but cannot tell how much was already in the pot (that is the + c).',
             'work': 'Totals from rates — total cost from marginal cost, total revenue from marginal revenue — are integrals.'},
            {'id': 'c8', 'title': 'Methods of integration',
             'body': ['Substitution: if the integrand contains a function and its derivative, put t = that function. ∫ (2x + 3)⁴ dx: t = 2x + 3, dx = dt/2 → (2x + 3)⁵/10 + c. Special case — when the numerator is the derivative of the denominator, the answer is the log of the denominator: logₑ|f(x)| + c is the integral of f′(x)/f(x).',
                      'Integration by parts: ∫ u v dx = u ∫ v dx − ∫ [u′ ∫ v dx] dx. Choose u as the factor that becomes simpler on differentiation (e.g. x in x eˣ).',
                      'Partial fractions: split a proper rational function into simpler fractions. (x + 5)/[(x + 1)(x + 2)] = 4/(x + 1) − 3/(x + 2).',
                      'Standard forms: ∫ dx/(x² − a²) = (1/2a) logₑ|(x − a)/(x + a)| + c; ∫ dx/(a² − x²) = (1/2a) logₑ|(a + x)/(a − x)| + c; ∫ dx/√(x² + a²) = logₑ|x + √(x² + a²)| + c; ∫ dx/√(x² − a²) = logₑ|x + √(x² − a²)| + c.'],
             'analogy': 'Substitution is renaming a messy part so the integral looks like one from the table; by parts is trading a hard integral for an easier one.',
             'work': 'These methods matter less in practice (software integrates) than in the exam — but recognising f′/f patterns gives instant answers in MCQs.'},
            {'id': 'c9', 'title': 'Definite integrals and their properties',
             'body': ['If F′ = f, then ∫ₐᵇ f(x) dx = F(b) − F(a). The constant of integration cancels, so it is not written. a is the lower limit, b the upper limit.',
                      'Properties: (I) the variable is a dummy — ∫ₐᵇ f(x) dx = ∫ₐᵇ f(t) dt; (II) ∫ₐᵇ f = −∫ᵦᵃ f (reversing limits changes sign); (III) ∫ₐᵇ f = ∫ₐᶜ f + ∫ᶜᵇ f; (IV) ∫₀ᵃ f(x) dx = ∫₀ᵃ f(a − x) dx; (V) if f(a + x) = f(x), then ∫₀ⁿᵃ f = n ∫₀ᵃ f; (VI) ∫₋ₐᵃ f = 2∫₀ᵃ f if f is even (f(−x) = f(x)) and 0 if f is odd (f(−x) = −f(x)).',
                      'For a curve above the x-axis, ∫ₐᵇ f(x) dx is the area between the curve, the x-axis and the lines x = a, x = b.'],
             'analogy': 'A definite integral is a meter reading: the total between two readings is "closing minus opening" — the starting point of the meter (the constant) does not matter.',
             'work': 'Total extra cost of raising production from one level to another is a definite integral of marginal cost between the two outputs.'},
            {'id': 'c10', 'title': 'From marginal functions back to totals',
             'body': ['Total cost: C(x) = ∫ MC dx + k, where k is found from a known value — usually the fixed cost, since C(0) = fixed cost.',
                      'Total revenue: R(x) = ∫ MR dx + k, with k = 0 because nothing sold means no revenue (R(0) = 0). The demand (average revenue) function is p = R(x)/x.',
                      'The change in total cost (or revenue) between outputs a and b is ∫ₐᵇ MC dx (or ∫ₐᵇ MR dx) — fixed cost does not affect it.',
                      'Similarly, a curve can be found from its slope: if dy/dx is known and the curve passes through a given point, integrate and use the point to fix c.'],
             'analogy': 'Knowing how much fuel a car burns per kilometre at each speed (marginal) lets you work out the fuel for the whole trip (total) — but you need the starting fuel level (the constant) to know what is left in the tank.',
             'work': 'Budgeting for an expansion: "what will the extra 10 units cost?" is ∫ MC between the two output levels — exactly what a cost accountant prepares for a capacity decision.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Derivatives from the first principle', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Using the first principle, differentiate (a) f(x) = 3x² + 2x and (b) f(x) = 1/x (x ≠ 0). Evaluate each at x = 2.',
             'solution': [p('(a) f(x + h) − f(x) = 3(x + h)² + 2(x + h) − 3x² − 2x = 6xh + 3h² + 2h. Dividing by h: 6x + 3h + 2 → 6x + 2 as h → 0. At x = 2: 14.'),
                          p('(b) f(x + h) − f(x) = 1/(x + h) − 1/x = −h/[x(x + h)]. Dividing by h: −1/[x(x + h)] → −1/x². At x = 2: −1/4.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Using the rules: sum, product, quotient, chain', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Differentiate with respect to x: (a) 4x³ − 5x² + 7x − 9; (b) x²eˣ; (c) (2x + 3)/(x − 1); (d) (3x² + 1)⁵; (e) logₑ(x² + 4).',
             'solution': [table(['Function', 'Rule', 'Derivative'], [
                 ['4x³ − 5x² + 7x − 9', 'Sum of powers', '12x² − 10x + 7'],
                 ['x²eˣ', 'Product', 'x²eˣ + 2x eˣ = x eˣ(x + 2)'],
                 ['(2x + 3)/(x − 1)', 'Quotient', '[2(x − 1) − (2x + 3)]/(x − 1)² = −5/(x − 1)²'],
                 ['(3x² + 1)⁵', 'Chain', '5(3x² + 1)⁴ × 6x = 30x(3x² + 1)⁴'],
                 ['logₑ(x² + 4)', 'Chain (log)', '2x/(x² + 4)']]),
                 note('Check (c) at x = 2: −5/1 = −5; (e) at x = 2: 4/8 = 0.5.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Implicit, parametric and logarithmic differentiation', 'difficulty': 'hard', 'minutes': 8,
             'q': '(a) Find dy/dx for x² + y² = 25 and its value at (3, 4). (b) If x = 2t² and y = 4t, find dy/dx. (c) Differentiate y = xˣ.',
             'solution': [p('(a) Differentiate term by term: 2x + 2y dy/dx = 0 → dy/dx = −x/y. At (3, 4): −3/4.'),
                          p('(b) dx/dt = 4t, dy/dt = 4 → dy/dx = 4/(4t) = 1/t. (At t = 2 the slope is 1/2.)'),
                          p('(c) logₑy = x logₑx. Differentiating: (1/y) dy/dx = x × (1/x) + logₑx = 1 + logₑx, so dy/dx = xˣ(1 + logₑx). At x = 2 this is about 4 × 1.6931 = 6.77.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Gradient, second derivative, maximum and minimum', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'For y = x³ − 6x² + 9x + 4, find the gradient at x = 0, the stationary points, and decide whether each is a maximum or a minimum.',
             'solution': [p('dy/dx = 3x² − 12x + 9; at x = 0 the gradient is 9.'),
                          p('Stationary points: 3(x² − 4x + 3) = 0 → x = 1 or x = 3. d²y/dx² = 6x − 12.'),
                          table(['x', 'd²y/dx²', 'Nature', 'y'], [['1', '−6 (< 0)', 'Maximum', '8'], ['3', '6 (> 0)', 'Minimum', '4']])],
             'checks': c4},
            {'id': 'i5', 'title': 'Least average cost and maximum profit', 'difficulty': 'hard', 'minutes': 10,
             'q': 'A firm\'s total cost is C(x) = 2x² + 40x + 5,000 and its demand function is p = 400 − 3x (₹). Find (a) the output at which average cost is least and show that AC = MC there; (b) the profit-maximising output, price and profit, and verify MR = MC.',
             'solution': [wn('(a) Average cost', f'AC = 2x + 40 + 5000/x; d(AC)/dx = 2 − 5000/x² = 0 → x² = 2500 → x = {x_ac}. Second derivative 10000/x³ > 0 → minimum. Least AC = 100 + 40 + 100 = ₹{ac_min}. MC = 4x + 40 = ₹{mc50} at x = 50 — equal to AC.'),
                          wn('(b) Profit', f'R = (400 − 3x)x = 400x − 3x². P = R − C = 360x − 5x² − 5,000. dP/dx = 360 − 10x = 0 → x = {x_p}; d²P/dx² = −10 < 0 → maximum. Price = 400 − 108 = ₹{price}. Profit = 12,960 − 6,480 − 5,000 = ₹{inr(pmax)}.'),
                          p('Check: MR = 400 − 6x = 184 and MC = 4x + 40 = 184 at x = 36 — MR = MC, as theory says.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Break-even point', 'difficulty': 'core', 'minutes': 4,
             'q': 'A start-up making smart meters has fixed costs of ₹3,60,000. Each meter costs ₹450 to make and sells for ₹750. Find the cost and revenue functions, the break-even output, and the profit if 1,500 meters are sold.',
             'solution': [p('C(x) = 3,60,000 + 450x; R(x) = 750x.'),
                          p(f'Break-even: 750x = 3,60,000 + 450x → 300x = 3,60,000 → x = {inr(bep)} meters (cost = revenue = ₹9,00,000).'),
                          p(f'P(1,500) = 300 × 1,500 − 3,60,000 = ₹{inr(p1500)}.')],
             'checks': c6},
            {'id': 'i7', 'title': 'Indefinite integrals by different methods', 'difficulty': 'hard', 'minutes': 10,
             'q': 'Integrate: (a) 6x² − 4x + 5; (b) (2x + 3)⁴; (c) x eˣ; (d) 1/(x² − 9); (e) (x + 5)/[(x + 1)(x + 2)]; (f) 1/√(x² + 4).',
             'solution': [table(['Integrand', 'Method', 'Result'], [
                 ['6x² − 4x + 5', 'Standard formulae', '2x³ − 2x² + 5x + c'],
                 ['(2x + 3)⁴', 'Substitution t = 2x + 3', '(2x + 3)⁵/10 + c'],
                 ['x eˣ', 'By parts (u = x)', 'x eˣ − eˣ + c = eˣ(x − 1) + c'],
                 ['1/(x² − 9)', 'Standard form, a = 3', '(1/6) logₑ|(x − 3)/(x + 3)| + c'],
                 ['(x + 5)/[(x + 1)(x + 2)]', 'Partial fractions: A = 4, B = −3', '4 logₑ|x + 1| − 3 logₑ|x + 2| + c'],
                 ['1/√(x² + 4)', 'Standard form, a = 2', 'logₑ|x + √(x² + 4)| + c']]),
                 wn('Partial fractions working', '(x + 5)/[(x + 1)(x + 2)] = A/(x + 1) + B/(x + 2). Put x = −1: A = 4/1 = 4. Put x = −2: B = 3/(−1) = −3.'),
                 note('Check any answer by differentiating it — you should get the integrand back.')],
             'checks': c7},
            {'id': 'i8', 'title': 'Definite integrals, properties and area', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Evaluate (a) ∫₁³ (3x² + 2x) dx; (b) ∫₀² x² dx; (c) ∫₋₂² x³ dx; (d) ∫₋₁¹ x² dx. (e) Find the area enclosed by y = 4x − x² and the x-axis.',
             'solution': [p(f'(a) [x³ + x²]₁³ = (27 + 9) − (1 + 1) = {d8a}.'),
                          p('(b) [x³/3]₀² = 8/3.'),
                          p('(c) x³ is odd, so the integral over [−2, 2] is 0. (Directly: [x⁴/4] = 4 − 4 = 0.)'),
                          p('(d) x² is even: 2∫₀¹ x² dx = 2 × 1/3 = 2/3.'),
                          p(f'(e) The curve meets the x-axis at x = 0 and x = 4 and is above it in between. Area = [2x² − x³/3]₀⁴ = 32 − 64/3 = 32/3 ≈ {area} square units.')],
             'checks': c8},
            {'id': 'i9', 'title': 'Total cost and demand from marginal functions', 'difficulty': 'moderate', 'minutes': 8,
             'q': '(a) MC = 3x² − 12x + 40 and fixed cost is ₹500. Find the total and average cost functions, the cost of 10 units, and the extra cost of raising output from 4 to 8 units. (b) MR = 100 − 4x. Find the total revenue and demand functions.',
             'solution': [p(f'(a) C(x) = ∫ (3x² − 12x + 40) dx = x³ − 6x² + 40x + k. C(0) = fixed cost → k = 500. AC = x² − 6x + 40 + 500/x. C(10) = 1000 − 600 + 400 + 500 = ₹{inr(tc10)}.'),
                          p(f'Extra cost = ∫₄⁸ MC dx = [x³ − 6x² + 40x]₄⁸ = 448 − 128 = ₹{inr(inc)} (fixed cost plays no part).'),
                          p('(b) R(x) = ∫ (100 − 4x) dx = 100x − 2x² + k; R(0) = 0 → k = 0. Demand: p = R/x = 100 − 2x.')],
             'checks': c9},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Advising a manufacturer on price', 'role': 'Cost and management accountant at a mid-sized factory',
             'situation': 'Marketing estimates that the price at which x units a week can be sold is p = 700 − 2x. Costing gives C(x) = x² + 100x + 15,000 a week. The owner wants to know the best output and price.',
             'steps': ['Revenue R = 700x − 2x²; profit P = R − C = 600x − 3x² − 15,000.',
                       f'dP/dx = 600 − 6x = 0 → x = {j_x} units; d²P/dx² = −6 < 0, so this is a maximum.',
                       f'Price = 700 − 200 = ₹{j_p}; weekly profit = ₹{inr(j_pr)}.',
                       'Present the answer with a sensitivity note: the result is only as good as the demand and cost estimates.'],
             'takeaway': 'Set MR = MC (equivalently dP/dx = 0) and confirm with the second derivative — the same steps as in the exam.',
             'checks': cj1},
            {'id': 'j2', 'title': 'Budgeting the cost of extra capacity', 'role': 'Finance executive preparing a capacity-expansion note',
             'situation': 'The plant currently makes 20 machines a month. Engineering gives marginal cost as MC = 2x + 50 (₹ thousand per machine). Management asks what it would cost to raise output to 30 machines.',
             'steps': ['The extra cost is the area under the MC curve between 20 and 30: ∫₂₀³⁰ (2x + 50) dx.',
                       f'[x² + 50x]₂₀³⁰ = (900 + 1,500) − (400 + 1,000) = {inr(j_inc)}, i.e. ₹{inr(j_inc)} thousand (₹10 lakh).',
                       'Fixed costs do not enter, because they do not change with output — mention this explicitly in the note.'],
             'takeaway': 'A definite integral of a marginal function gives the change in the total — a direct budgeting tool.',
             'think': 'If the consumption function of a household is C = 2,000 + 0.75Y, what are its MPC and MPS?',
             'answer': 'MPC = dC/dY = 0.75; MPS = 1 − 0.75 = 0.25.',
             'checks': cj2},
        ],
        'mcqs': M,
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Differentiate (a) y = (x² + 1)(3x − 2) and find its value at x = 1; (b) y = (3x + 2)/(2x − 1); (c) y = e^(x²).',
             'model': [p('(a) Product rule: y′ = (x² + 1)(3) + (3x − 2)(2x) = 3x² + 3 + 6x² − 4x = 9x² − 4x + 3. At x = 1: 9 − 4 + 3 = 8.'),
                       p('(b) Quotient rule: y′ = [(2x − 1)(3) − (3x + 2)(2)]/(2x − 1)² = (6x − 3 − 6x − 4)/(2x − 1)² = −7/(2x − 1)².'),
                       p('(c) Chain rule: y′ = e^(x²) × 2x = 2x e^(x²).')],
             'scheme': [{'id': 's1', 'pt': '(a) Product rule applied and simplified to 9x² − 4x + 3', 'm': 1, 'skill': 'application'},
                        {'id': 's2', 'pt': '(a) Value 8 at x = 1', 'm': 0.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(b) Quotient rule with correct order of terms; −7/(2x − 1)²', 'm': 1.5, 'skill': 'application'},
                        {'id': 's4', 'pt': '(c) Chain rule: 2x e^(x²)', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Reversing the order in the quotient-rule numerator flips the sign — a very common slip.', 'Candidates who expand (a) first and differentiate the cubic also score full marks.'],
             'mistakes': ['Writing d/dx e^(x²) = e^(x²).', 'Differentiating a product as the product of derivatives.'],
             'tips': ['Write "u = …, v = …" before applying the product or quotient rule.', 'Simplify the numerator fully — examiners award a mark for the final simplified form.'],
             'checks': qc1},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': 'The total cost of producing x units is C(x) = 0.5x² + 30x + 1,800 and the demand function is p = 150 − x (₹). Find (a) the output that maximises profit, the price and the maximum profit; (b) the output at which average cost is least, the least average cost, and show that MC equals AC at that output.',
             'model': [p(f'(a) R = 150x − x². P = R − C = 120x − 1.5x² − 1,800. dP/dx = 120 − 3x = 0 → x = {q2x}. d²P/dx² = −3 < 0 → maximum. Price = 150 − 40 = ₹{q2p}. Profit = 4,800 − 2,400 − 1,800 = ₹{q2pr}.'),
                       p(f'(b) AC = 0.5x + 30 + 1,800/x. d(AC)/dx = 0.5 − 1,800/x² = 0 → x² = 3,600 → x = {q2ac}. Second derivative 3,600/x³ > 0 → minimum. Least AC = 30 + 30 + 30 = ₹{q2acm}. MC = x + 30 = ₹{q2mc} at x = 60 = AC.')],
             'scheme': [{'id': 's1', 'pt': 'Profit function P = 120x − 1.5x² − 1,800', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'First-order condition gives x = 40', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Second-order condition shown (P″ < 0)', 'm': 0.5, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'Price ₹110 and profit ₹600', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'AC minimised at x = 60 with second-order check; least AC ₹90', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's6', 'pt': 'MC = AC = ₹90 verified', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Many candidates maximise revenue instead of profit — read which function is to be optimised.', 'Marks are reserved for the second-order condition; do not skip it.'],
             'mistakes': ['Differentiating C(x) and setting MC = 0.', 'Minimising total cost instead of average cost.'],
             'tips': ['Write P(x) explicitly before differentiating.', 'State the economic interpretation in one line at the end.'],
             'checks': qc2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
             'q': '(a) Evaluate ∫ (4x³ − 6x + 2/x) dx. (b) Using a property of definite integrals, evaluate ∫₀¹ x(1 − x)⁴ dx. (c) Marginal cost is MC = 3x² − 8x + 10 and fixed cost is ₹60. Find the total cost function and the total and average cost of 6 units.',
             'model': [p('(a) x⁴ − 3x² + 2 logₑ|x| + c.'),
                       p(f'(b) By ∫₀ᵃ f(x) dx = ∫₀ᵃ f(a − x) dx with a = 1: ∫₀¹ (1 − x)x⁴ dx = ∫₀¹ (x⁴ − x⁵) dx = 1/5 − 1/6 = 1/30 (≈ {q3b}).'),
                       p(f'(c) C(x) = x³ − 4x² + 10x + k; C(0) = 60 → k = 60. C(6) = 216 − 144 + 60 + 60 = ₹{q3c}; AC = 192/6 = ₹{q3ac}.')],
             'scheme': [{'id': 's1', 'pt': '(a) Each term integrated, log term and constant included', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': '(b) Property f(a − x) applied to simplify', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': '(b) Value 1/30', 'm': 0.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': '(c) Constant of integration = fixed cost; TC function', 'm': 1, 'skill': 'application'},
                        {'id': 's5', 'pt': '(c) TC ₹192 and AC ₹32', 'm': 1, 'skill': 'computation'}],
             'remarks': ['In (b), expanding (1 − x)⁴ works but takes much longer — the property is what the examiner is testing.', 'Several answers drop the constant in (c), giving TC ₹132.'],
             'mistakes': ['Integrating 2/x as 2x⁰/0.', 'Leaving out the fixed cost.'],
             'tips': ['Write the property you use in symbols before applying it.', 'Always add "+ c" to indefinite integrals.'],
             'checks': qc3},
        ],
        'revision': {
            'summary': ['dy/dx = lim [f(x + h) − f(x)]/h as h → 0 — rate of change, slope of the tangent.', 'xⁿ → nxⁿ⁻¹; eᵃˣ → a eᵃˣ; aˣ → aˣ logₑa; logₑx → 1/x; constant → 0.',
                        'Product (uv)′ = uv′ + vu′; quotient (u/v)′ = (vu′ − uv′)/v²; chain dy/dx = dy/dz · dz/dx.', 'Implicit: differentiate both sides; parametric: (dy/dt)/(dx/dt); logarithmic for xˣ and long products.',
                        'Max: f′ = 0, f″ < 0; min: f′ = 0, f″ > 0.', 'MC = dC/dx; MR = dR/dx; profit max MR = MC; break-even R = C; least AC where AC = MC; MPC + MPS = 1.',
                        '∫ xⁿ = xⁿ⁺¹/(n + 1) + c (n ≠ −1); ∫ 1/x = logₑ|x|; ∫ eᵃˣ = eᵃˣ/a; ∫ aˣ = aˣ/logₑa.', 'By parts: ∫ uv = u∫v − ∫(u′∫v). Definite: F(b) − F(a), no constant.',
                        'TC = ∫ MC + fixed cost; TR = ∫ MR (constant 0); demand p = TR/x.'],
            'remember': ['∫₋ₐᵃ odd function = 0; even function = 2∫₀ᵃ.', '∫₀ᵃ f(x) dx = ∫₀ᵃ f(a − x) dx.', 'Reversing limits changes the sign.'],
            'traps': ['Do not differentiate eˣ like a power.', 'Quotient rule: the order in the numerator matters.', 'Maximise profit, not revenue, unless asked.', 'The power formula for integration fails at n = −1.'],
        },
        'quickref': [
            {'k': 'First principle', 'v': 'f′(x) = lim [f(x + h) − f(x)]/h, h → 0'},
            {'k': 'Standard derivatives', 'v': 'xⁿ → nxⁿ⁻¹; eᵃˣ → aeᵃˣ; aˣ → aˣ logₑa; logₑx → 1/x'},
            {'k': 'Product / quotient', 'v': '(uv)′ = uv′ + vu′; (u/v)′ = (vu′ − uv′)/v²'},
            {'k': 'Chain / parametric', 'v': 'dy/dx = dy/dz · dz/dx; dy/dx = (dy/dt)/(dx/dt)'},
            {'k': 'Max / min', 'v': 'f′ = 0; f″ < 0 max, f″ > 0 min'},
            {'k': 'Business', 'v': 'MC = C′(x); MR = R′(x); P = R − C; max profit MR = MC; BEP R = C; MPS = 1 − MPC'},
            {'k': 'Standard integrals', 'v': '∫xⁿ = xⁿ⁺¹/(n + 1); ∫1/x = logₑ|x|; ∫eᵃˣ = eᵃˣ/a; ∫aˣ = aˣ/logₑa'},
            {'k': 'By parts', 'v': '∫uv dx = u∫v dx − ∫(u′∫v dx) dx'},
            {'k': 'Standard forms', 'v': '∫dx/(x² − a²) = (1/2a) log|(x − a)/(x + a)|; ∫dx/√(x² + a²) = log|x + √(x² + a²)|'},
            {'k': 'Definite integral', 'v': '∫ₐᵇ f = F(b) − F(a); odd over [−a, a] = 0; even = 2∫₀ᵃ'},
            {'k': 'Marginal → total', 'v': 'TC = ∫MC dx + FC; TR = ∫MR dx; p = TR/x'},
        ],
        'viva': VIVA,
        'cases': [{
            'id': 'k1', 'title': 'Pricing wall clocks at Samay Industries', 'difficulty': 'hard',
            'case': ('Samay Industries estimates that it can sell x wall clocks a day at a price of p = 1,000 − 3x rupees. Its total daily cost is C(x) = 2x² + 200x + 12,000 rupees. '
                     'The finance head wants the profit-maximising plan.'),
            'mcqs': [
                mq('k1a', 'The marginal revenue function is:', 'MR = 1,000 − 6x', ['MR = 1,000 − 3x', 'MR = 1,000x − 3x²', 'MR = 4x + 200'], 'R = 1,000x − 3x², so MR = 1,000 − 6x. 4x + 200 is MC.', 'c6', 'moderate'),
                mq('k1b', 'The profit-maximising output is:', '80 clocks', ['100 clocks', '160 clocks', '50 clocks'], f'P = 800x − 5x² − 12,000; P′ = 800 − 10x = 0 → x = {k_x}. (Check: MR = 520 = MC at x = 80.)', 'c6', 'hard', '800/10'),
                mq('k1c', 'The price per clock at that output is:', '₹760', ['₹520', '₹1,000', '₹700'], f'p = 1,000 − 3 × 80 = ₹{k_p}. ₹520 is the marginal revenue, not the price.', 'c6', 'moderate', '1000-3*80'),
                mq('k1d', 'The maximum daily profit is:', '₹20,000', ['₹32,000', '₹44,000', '₹8,000'], f'P(80) = 64,000 − 32,000 − 12,000 = ₹{inr(k_pr)}.', 'c6', 'hard', '800*80-5*80**2-12000'),
            ]}],
    }


VIVA = [
    V('v1', 'What is a derivative, and what does finding it from the first principle mean?',
      'The derivative of y equals f of x is the limit of the ratio of the change in f of x to the small change h in x, as h tends to zero. It measures the instantaneous rate of change of y with respect to x, and geometrically the slope of the tangent. Finding it from the first principle means computing this limit, f of x plus h minus f of x over h, directly from the definition instead of using formulas.',
      [P('p1', 'Limit of [f(x + h) − f(x)]/h as h → 0', 4, 'limit', 'h tends to zero|h tend to 0|h approach zero|h approaches 0|h goes to zero|h goes to 0|tends to zero|small change|small increment|very small|change in x', 'ratio|divid|over h|by h|change in y|change in f', min=2),
       P('p2', 'Rate of change of y with respect to x (slope of the tangent)', 3, 'rate of change|rate change|slope|gradient|tangent', min=1),
       P('p3', 'First principle = computing directly from the definition, not formulas', 3, 'definition|defin|directly|ab initio|without formula|instead of formula|not using formula|from the limit|basic definition', min=1)], 'c1'),
    V('v2', 'State the product rule and the quotient rule of differentiation.',
      'The product rule says the derivative of u times v is u times the derivative of v plus v times the derivative of u. The quotient rule says the derivative of u over v is v times the derivative of u minus u times the derivative of v, all divided by v squared, provided v is not zero.',
      [P('p1', 'Product: (uv)′ = u v′ + v u′', 5, 'product rule|product', 'u time derivative of v plus v time derivative of u|u dv plus v du|u v dash plus v u dash|first time derivative of second plus second time derivative of first|u into dv dx plus v into du dx|u v prime plus v u prime|uv prime plus vu prime|first into derivative of second plus second into derivative of first|derivative of v plus v time derivative of u|u dv dx plus v du dx', min=2),
       P('p2', 'Quotient: (u/v)′ = (v u′ − u v′)/v²', 5, 'quotient rule|quotient', 'v time derivative of u minus u time derivative of v|v du minus u dv|v u dash minus u v dash|denominator time derivative of numerator minus numerator time derivative of denominator|v du dx minus u dv dx|v u prime minus u v prime|derivative of u minus u time derivative of v', 'v square|v squared|denominator square|denominator squared|square of denominator|square of v', min=3)], 'c3'),
    V('v3', 'What are marginal cost and marginal revenue, and how are they obtained from total functions?',
      'Marginal cost is the rate of change of total cost with respect to output, roughly the extra cost of producing one more unit, and it is found by differentiating the total cost function, d C by d x. Marginal revenue is the rate of change of total revenue with respect to output, found by differentiating the total revenue function, d R by d x.',
      [P('p1', 'MC = dC/dx — rate of change of total cost (cost of one more unit)', 5, 'marginal cost|mc', 'differentiat|derivative|d c by d x|dc dx|dc/dx|rate of change of total cost|rate of change of cost|one more unit|additional unit|extra unit|next unit', min=2),
       P('p2', 'MR = dR/dx — rate of change of total revenue', 5, 'marginal revenue|mr', 'differentiat|derivative|d r by d x|dr dx|dr/dx|rate of change of total revenue|rate of change of revenue|one more unit|additional unit|extra unit|next unit', min=2)], 'c6'),
    V('v4', 'How do you find a maximum or minimum using derivatives, and what is the condition for maximum profit?',
      'First put the first derivative equal to zero and solve for x to get the stationary points. Then check the second derivative: if it is negative the point is a maximum, and if it is positive the point is a minimum. Profit is maximum where marginal revenue equals marginal cost, with the second derivative of profit negative.',
      [P('p1', 'Set the first derivative equal to zero', 3, 'first derivative zero|first derivative equal zero|first derivative equal to zero|first derivative is zero|dy dx equal zero|dy dx zero|f dash x equal zero|f prime equal zero|derivative equal zero|derivative to zero|derivative zero|derivative is zero|derivative as zero|derivative equal 0|derivative 0', min=1),
       P('p2', 'Second derivative negative → maximum; positive → minimum', 4, 'second derivative negative maximum|second derivative is negative maximum|negative maximum|negative it is a maximum|negative then maximum|negative for maximum|negative means maximum|less than zero maximum|less than 0 maximum|maximum if negative|maximum when negative', 'positive minimum|positive it is a minimum|positive then minimum|positive for minimum|positive means minimum|greater than zero minimum|greater than 0 minimum|minimum if positive|minimum when positive', min=2),
       P('p3', 'Maximum profit where MR = MC', 3, 'marginal revenue equal marginal cost|marginal revenue equals marginal cost|mr equal mc|mr equals mc|mr = mc|mr is equal to mc|marginal revenue is equal to marginal cost|marginal cost equal marginal revenue|mc equal mr|mc equals mr', min=1)], 'c5'),
    V('v5', 'Why do we add a constant in an indefinite integral but not in a definite integral?',
      'Integration is the reverse of differentiation, and since the derivative of any constant is zero, many functions differing only by a constant have the same derivative, so we add an arbitrary constant c to an indefinite integral. In a definite integral we take F of b minus F of a, so the constant cancels out and is not written.',
      [P('p1', 'Derivative of a constant is zero, so the anti-derivative is fixed only up to a constant', 5, 'derivative of constant zero|derivative of a constant is zero|derivative of any constant is zero|constant vanish|constant disappear|constant become zero|constant differentiate to zero|differentiating a constant gives zero|constant lost|constant gone', min=1),
       P('p2', 'Definite: F(b) − F(a) — the constant cancels', 5, 'cancel|cancels out|subtract out|get subtracted|eliminated|drops out|knocked out|difference remov', 'f of b minus f of a|f b minus f a|upper minus lower|upper limit minus lower limit|b minus a|difference|subtract', min=1)], 'c7'),
    V('v6', 'How do you get the total cost function and the demand function from marginal cost and marginal revenue?',
      'Total cost is the integral of marginal cost plus a constant, and that constant equals the fixed cost because cost at zero output is the fixed cost. Total revenue is the integral of marginal revenue, with the constant zero since revenue is zero when nothing is sold. The demand or price function is total revenue divided by the quantity x.',
      [P('p1', 'TC = ∫ MC dx; constant = fixed cost', 4, 'integrat', 'marginal cost', 'fixed cost', min=3),
       P('p2', 'TR = ∫ MR dx with constant zero (no sales, no revenue)', 3, 'marginal revenue', 'constant zero|constant is zero|constant equal zero|constant 0|zero revenue|revenue zero|revenue is zero|no revenue|nothing sold|no sale|zero when nothing', min=2),
       P('p3', 'Demand p = TR/x', 3, 'revenue divid by x|revenue divided by quantity|revenue divided by x|revenue over x|revenue by x|r by x|r over x|revenue divided by output|revenue per unit|average revenue|revenue upon x|revenue divid quantit|revenue divid output', min=1)], 'c10'),
]
