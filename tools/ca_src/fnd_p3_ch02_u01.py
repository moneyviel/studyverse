"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 2 Equations (single unit).
Original explanations, numbers and questions; scope follows the ICAI study material (May 2027 onwards).
Every numerical answer is computed here and stored with a check expression."""
import math
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch02-u01'


class Checks(Checks):
    """lib.Checks (stored value rounded to 2 dp for the validator) that returns the unrounded value for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = eval(expr, {'__builtins__': {}}, {'round': round})
        return int(round(v)) if abs(v - round(v)) < 1e-9 else v


def num(v, dp=4):
    v = round(v, dp)
    if v == int(v): return str(int(v))
    return f'{v:.{dp}f}'.rstrip('0').rstrip('.')


def M(mid, q, options, answer, explain, concept, difficulty='moderate', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if topic: d['topic'] = topic
    if check is not None: d['check'] = check
    return d


def roots(a, b, c):
    d = b * b - 4 * a * c
    return ((-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a)) if d >= 0 else None


def build():
    # ---------- Illustration 1: linear equation with fractions ----------
    c1 = Checks()
    x1 = c1.add('(6-9-8)/(3-4)', 'x from 3(x+3) − 4(x−2) = 6')
    c1.add('(11+3)/4-(11-2)/3', 'check: LHS at x = 11 equals 1/2')

    # ---------- Illustration 2: ages ----------
    c2 = Checks()
    s2 = c2.add('(15-5)/(4-3)', 'son’s age from 4S + 5 = 3(S + 5)')
    f2 = c2.add('4*10', 'father’s age')
    c2.add('(40+5)/(10+5)', 'check: ratio after 5 years = 3')

    # ---------- Illustration 3: two equations, two methods ----------
    c3 = Checks()
    x3 = c3.add('(18*2+4*4)/(3*2+5*4)', 'x by elimination: 13x = 26')
    y3 = c3.add('(18-3*2)/4', 'y = (18 − 3x)/4')
    dx = c3.add('4*(-4)-(-2)*(-18)', 'b1c2 − b2c1')
    dy = c3.add('(-18)*5-(-4)*3', 'c1a2 − c2a1')
    dd = c3.add('3*(-2)-5*4', 'a1b2 − a2b1')
    c3.add('(4*(-4)-(-2)*(-18))/(3*(-2)-5*4)', 'x by cross-multiplication')
    c3.add('((-18)*5-(-4)*3)/(3*(-2)-5*4)', 'y by cross-multiplication')

    # ---------- Illustration 4: three unknowns ----------
    c4 = Checks()
    c4.add('9+4', 'eq(1) + eq(3): 2x + 3y = 13')
    c4.add('5+4', 'eq(2) + eq(3): 3x + y = 9')
    x4 = c4.add('(13-27)/(2-9)', 'x from 2x + 3(9 − 3x) = 13')
    y4 = c4.add('9-3*2', 'y = 9 − 3x')
    z4 = c4.add('9-2-3', 'z = 9 − x − y')
    c4.add('2*2-3+4', 'check eq(2) = 5')
    c4.add('2+2*3-4', 'check eq(3) = 4')

    # ---------- Illustration 5: quadratic by formula ----------
    c5 = Checks()
    d5 = c5.add('(-7)**2-4*6*(-20)', 'discriminant')
    r5a = c5.add('(7+23)/12', 'root 1')
    r5b = c5.add('(7-23)/12', 'root 2')
    c5.add('(7+23)/12+(7-23)/12', 'sum of roots = 7/6')
    c5.add('((7+23)/12)*((7-23)/12)', 'product of roots = −20/6')
    assert d5 == 529 and abs(r5a + r5b - 7 / 6) < 1e-9 and abs(r5a * r5b + 20 / 6) < 1e-9

    # ---------- Illustration 6: nature of roots and forming equations ----------
    c6 = Checks()
    k6 = c6.add('(4*4*9)**0.5', 'k for equal roots of 4x² − kx + 9 = 0 (positive value)')
    s6 = c6.add('5**2-2*3', 'α² + β²')
    p6 = c6.add('3**2', 'α²β²')
    c6.add('(3+2**0.5)+(3-2**0.5)', 'sum of conjugate roots')
    c6.add('(3+2**0.5)*(3-2**0.5)', 'product of conjugate roots')
    a, b = roots(1, -5, 3)
    assert abs(a * a + b * b - 19) < 1e-9 and abs((a * b) ** 2 - 9) < 1e-9

    # ---------- Illustration 7: reducible quadratic + application ----------
    c7 = Checks()
    c7.add('(13+5)/2', 'y = 9')
    c7.add('(13-5)/2', 'y = 4')
    d7 = c7.add('25+4*750', 'discriminant of p² − 5p − 750 = 0')
    p7 = c7.add('(5+55)/2', 'price per pen (positive root)')
    n7 = c7.add('600/30', 'pens bought')
    c7.add('600/(30-5)-600/30', 'check: 4 more pens at the lower price')

    # ---------- Illustration 8: cubic ----------
    c8 = Checks()
    c8.add('1**3-7*1+6', 'f(1) = 0, so x − 1 is a factor')
    c8.add('2**3-7*2+6', 'f(2) = 0')
    c8.add('(-3)**3-7*(-3)+6', 'f(−3) = 0')
    c8.add('1+2-3', 'sum of roots = 0 (no x² term)')

    # ---------- Jobs ----------
    jb1 = Checks()
    bep = jb1.add('360000/(250-160)', 'break-even units')
    jb1.add('4000*250-(360000+4000*160)', 'check: profit at break-even = 0')
    jb2 = Checks()
    ja = jb2.add('(4*1500-2000)/(4*3-2)', 'units of A')
    jbb = jb2.add('1500-3*400', 'units of B')
    jb2.add('2*400+4*300', 'machine hours used')
    jb2.add('3*400+300', 'labour hours used')
    jb3 = Checks()
    r3 = jb3.add('(1.1664**0.5-1)*100', 'rate % from (1 + r)² = 1.1664')

    # ---------- Questions ----------
    q1c = Checks()
    q1c.add('3+9', 'eq(1) + eq(2): 3x + 3y = 12')
    q1c.add('2*3+10', '2 × eq(1) + eq(3): 7x + y = 16')
    qx = q1c.add('(16-4)/(7-1)', 'x')
    qy = q1c.add('4-2', 'y')
    qz = q1c.add('2*2+2-3', 'z = 2x + y − 3')
    q1c.add('2+2*2+3', 'check eq(2) = 9')
    q1c.add('3*2-2+2*3', 'check eq(3) = 10')
    q2c = Checks()
    q2d = q2c.add('16+4*96', 'discriminant of n² − 4n − 96 = 0')
    q2n = q2c.add('(4+20)/2', 'number of friends')
    q2c.add('14400/12', 'original share')
    q2c.add('14400/8', 'new share')
    q2c.add('14400/8-14400/12', 'increase per person')
    q3c = Checks()
    q3c.add('(-1)**3-4*(-1)**2+(-1)+6', 'f(−1) = 0')
    q3c.add('-1+2+3', 'sum of roots = 4 = −b/a')
    q3c.add('(-1)*2*3', 'product of roots = −6 = −d/a')
    q3c.add('2**3-4*2**2+2+6', 'f(2) = 0')
    q3c.add('3**3-4*3**2+3+6', 'f(3) = 0')

    # ---------- Case: pricing and break-even ----------
    kc = Checks()
    q50 = kc.add('1200-20*50', 'quantity at ₹50')
    kc.add('80**2-4*1500', 'discriminant of p² − 80p + 1500 = 0')
    pmax = kc.add('80/2', 'price for maximum profit (vertex)')
    prof = kc.add('-20*40**2+1600*40-30000', 'maximum profit')
    case = {
        'id': 'k1', 'title': 'Pricing a new snack pack', 'difficulty': 'hard',
        'case': ('Raghav Foods is launching a snack pack. Market research suggests that at a price of ₹p per pack it will sell q = 1,200 − 20p packs a week. '
                 'Weekly costs are a fixed ₹6,000 plus ₹20 per pack. Weekly profit is therefore π = p(1,200 − 20p) − [6,000 + 20(1,200 − 20p)], which simplifies to π = −20p² + 1,600p − 30,000.'),
        'mcqs': [
            M('k1a', 'How many packs will be sold in a week at a price of ₹50?', ['200', '1,000', '1,150', '250'], 0, 'Substitute p = 50 into the demand equation: q = 1,200 − 20 × 50 = 1,200 − 1,000 = 200 packs a week. The trap is 1,000, which is the term 20p — the reduction in demand, not the demand itself. In practice: marketing teams estimate such linear demand functions from test-market data, and finance plugs proposed prices into them before fixing an MRP.', 'c2', 'core', '1200-20*50', topic='Linear (simple) equations in one unknown'),
            M('k1b', 'At what prices does Raghav Foods break even (profit = 0)?', ['₹30 and ₹50', '₹20 and ₹60', '₹40 only', '₹25 and ₹55'], 0,
              "Set profit to zero: −20p² + 1,600p − 30,000 = 0. Dividing by −20 gives p² − 80p + 1,500 = 0 = (p − 30)(p − 50), so break-even prices are ₹30 and ₹50. The trap is '₹40 only', which is the midpoint (best price) rather than a break-even point. In practice: a quadratic profit model has two break-even prices — price too low and margins vanish, too high and volume vanishes.", 'c5', 'hard', topic='Quadratic equations — solving, sum and product of roots'),
            M('k1c', 'The roots of the break-even equation are:', ['Real, rational and unequal', 'Real and equal', 'Real, irrational and unequal', 'Imaginary'], 0,
              "For p² − 80p + 1,500 = 0, the discriminant is 80² − 4 × 1,500 = 6,400 − 6,000 = 400 = 20². A positive perfect-square discriminant with rational coefficients means the roots are real, rational and unequal (30 and 50). The trap is 'real, irrational and unequal', which needs D positive but not a perfect square. In practice: a positive discriminant tells management that a profitable price band exists between two break-even prices.", 'c6', 'moderate', topic='Nature of roots — the discriminant'),
            M('k1d', 'Profit is highest midway between the break-even prices. The maximum weekly profit is:', [R(prof), R(30000), R(64000), R(4000)], 0,
              "The profit curve is symmetric, so the best price is midway: (30 + 50)/2 = ₹40. Profit = −20(40²) + 1,600(40) − 30,000 = −32,000 + 64,000 − 30,000 = ₹2,000 a week. The trap is ₹64,000, which is only the 1,600p term, not the profit. In practice: a pricing analyst at an FMCG company sets the launch price near this profit-maximising point and then checks it against competitors' MRPs.", 'c5', 'hard', '-20*40**2+1600*40-30000', topic='Quadratic equations — solving, sum and product of roots'),
        ]}

    # ---------- MCQs ----------
    mcqs = [
        M('m1', 'The solution of 5x − 3 = 3x + 11 is:', ['7', '4', '−7', '2'], 0, 'Collect the x-terms on one side and the numbers on the other: 5x − 3x = 11 + 3, so 2x = 14 and x = 7. Check: 5(7) − 3 = 32 and 3(7) + 11 = 32. The trap is 4, which comes from moving −3 across without changing its sign (2x = 11 − 3 = 8). In practice: a one-unknown equation like this is how a cost accountant finds the output at which two pricing or cost options give the same total.', 'c2', 'core', topic='Linear (simple) equations in one unknown'),
        M('m2', 'If x/3 + x/4 = 14, then x is:', ['24', '12', '98', '42'], 0, 'Take the LCM of 3 and 4, which is 12: (4x + 3x)/12 = 14, so 7x = 168 and x = 24. Check: 24/3 + 24/4 = 8 + 6 = 14. The trap is 12, which treats 12 as the answer instead of the common denominator; 98 multiplies 14 by 7 and forgets the 12. In practice: splitting a known total among parts stated as fractions of an unknown — for example, a budget head — reduces to exactly this kind of equation.', 'c2', 'core', '14*12/7', topic='Linear (simple) equations in one unknown'),
        M('m3', 'Which of the following is an identity (true for every value of x)?', ['(x + 1)² = x² + 2x + 1', 'x² = 2x + 1', '2x + 1 = 9', 'x² + 1 = 0'], 0,
          'An identity holds for every value of the variable. Expanding (x + 1)² always gives x² + 2x + 1, whatever x is, so it is an identity. The tempting wrong choice is x² = 2x + 1, which looks similar but is a conditional equation true only for x = 1 ± √2; 2x + 1 = 9 holds only at x = 4, and x² + 1 = 0 has no real solution. In practice: accounting identities such as Assets = Liabilities + Capital hold for every transaction, unlike equations solved for one unknown.', 'c1', 'core', topic='What an equation is — conditional equation vs identity'),
        M('m4', 'The degree of the equation 4x³ + 2x − 7 = 0 is:', ['3', '2', '1', '4'], 0, 'The degree of a polynomial equation is the highest power of the variable that appears with a non-zero coefficient. In 4x³ + 2x − 7 = 0 that power is 3, so it is a cubic equation. The trap is 4, which picks the coefficient of x³ instead of its power; 1 comes from the 2x term. In practice: knowing the degree tells an analyst how many roots to expect — a cubic cost or revenue model can have up to three turning-point solutions.', 'c1', 'core', topic='What an equation is — conditional equation vs identity'),
        M('m5', 'The sum of two numbers is 50 and their difference is 14. The larger number is:', ['32', '18', '36', '25'], 0, 'Let the numbers be x and y with x + y = 50 and x − y = 14. Adding the two equations gives 2x = 64, so x = 32 and y = 18. The trap is 18, which is the smaller number; 36 adds 14 to half the sum twice. Quick rule: larger = (sum + difference)/2. In practice: when a partner knows the total of two balances and how much one exceeds the other, this two-line method splits them instantly.', 'c3', 'core', '(50+14)/2', topic='Simultaneous linear equations in two unknowns'),
        M('m6', 'A is twice as old as B. Ten years ago A was three times as old as B. A’s present age is:', ['40 years', '20 years', '30 years', '60 years'], 0,
          "Let B's present age be B, so A = 2B. Ten years ago: 2B − 10 = 3(B − 10), which gives 2B − 10 = 3B − 30, so B = 20 and A = 40 years. Check: ten years ago A was 30 and B was 10 — three times. The trap is 20 years, which is B's age, not A's. In practice: setting up a 'then and now' equation like this is the same logic used to back-calculate opening balances from known changes.", 'c2', 'moderate', '2*(30-10)', topic='Linear (simple) equations in one unknown'),
        M('m7', 'The solution of 2x + 3y = 13 and 3x − y = 3 is:', ['x = 2, y = 3', 'x = 3, y = 2', 'x = 1, y = 0', 'x = 5, y = 1'], 0,
          "From 3x − y = 3, y = 3x − 3. Substitute: 2x + 3(3x − 3) = 13, so 11x = 22, x = 2 and y = 3. Check in both: 4 + 9 = 13 and 6 − 3 = 3. The trap is x = 3, y = 2, which swaps the values (2(3) + 3(2) = 12, not 13). In practice: two linear equations in two unknowns are how a business finds, for instance, the price of two products from two days' total sales.", 'c3', 'core', topic='Simultaneous linear equations in two unknowns'),
        M('m8', 'The equations 2x + 3y = 5 and 4x + 6y = 12 have:', ['No solution', 'A unique solution', 'Infinitely many solutions', 'Exactly two solutions'], 0,
          "Compare coefficients: 2/4 = 3/6 = 1/2, but 5/12 is not 1/2. When the x and y coefficients are in the same ratio but the constants are not, the lines are parallel and never meet, so there is no solution. The trap is 'infinitely many solutions', which would need all three ratios equal (for example 4x + 6y = 10). In practice: inconsistent equations signal contradictory data — like two budget constraints that cannot both be met — and an analyst must revisit the inputs.", 'c3', 'moderate', topic='Simultaneous linear equations in two unknowns'),
        M('m9', 'If x + 2y = 7 and 3x − y = 7, the value of xy is:', ['6', '5', '12', '1'], 0, 'From 3x − y = 7, y = 3x − 7. Substitute: x + 2(3x − 7) = 7, so 7x = 21, x = 3 and y = 2. Then xy = 3 × 2 = 6. The trap is 5, which adds x and y instead of multiplying them; always reread what the question finally asks. In practice: many exam and work problems ask for a derived figure — revenue as price × quantity, for example — after solving for the basic unknowns.', 'c3', 'core', topic='Simultaneous linear equations in two unknowns'),
        M('m10', 'If x + y = 7, y + z = 9 and z + x = 8, then z is:', ['5', '4', '3', '12'], 0, "Add all three equations: 2(x + y + z) = 24, so x + y + z = 12. Then z = 12 − (x + y) = 12 − 7 = 5 (also x = 3, y = 4). The trap is 12, which is x + y + z, not z; 4 is the value of y. In practice: when an auditor knows pairwise totals — say combined sales of each pair of three branches — this add-and-subtract trick recovers each branch's figure.", 'c4', 'moderate', topic='Three linear equations in three unknowns'),
        M('m11', 'The roots of x² − 9x + 20 = 0 are:', ['4 and 5', '−4 and −5', '2 and 10', '−4 and 5'], 0, 'Find two numbers whose sum is 9 and product is 20: they are 4 and 5, so x² − 9x + 20 = (x − 4)(x − 5) = 0 and the roots are 4 and 5. The trap is −4 and −5, which gets the factors right but the signs wrong — (x + 4)(x + 5) would give +9x. In practice: quadratic equations appear when an analyst solves for price or output in profit models where revenue and cost both depend on quantity.', 'c5', 'core', topic='Quadratic equations — solving, sum and product of roots'),
        M('m12', 'The sum of the roots of 3x² − 12x + 7 = 0 is:', ['4', '−4', '7/3', '12'], 0, 'For ax² + bx + c = 0, the sum of the roots is −b/a. Here a = 3 and b = −12, so the sum = 12/3 = 4. The trap is −4, which forgets the minus sign in −b/a; 7/3 is the product c/a. In practice: sum-and-product relations let an analyst check solver output quickly — if two break-even prices do not add to −b/a, something has gone wrong.', 'c5', 'core', topic='Quadratic equations — solving, sum and product of roots'),
        M('m13', 'The product of the roots of 2x² + 5x − 8 = 0 is:', ['-4', '4', '-2.5', '2.5'], 0, 'For ax² + bx + c = 0, the product of the roots is c/a. Here c = −8 and a = 2, so the product = −8/2 = −4. The trap is −2.5, which is the sum −b/a = −5/2, not the product; +4 drops the sign of c. A negative product also tells you one root is positive and one negative. In practice: this sign check helps an analyst see at once that only one root of a cost or demand model can be economically meaningful.', 'c5', 'core', '-8/2', topic='Quadratic equations — solving, sum and product of roots'),
        M('m14', 'The roots of x² − 6x + 9 = 0 are:', ['Real and equal', 'Real and unequal', 'Imaginary', 'Irrational'], 0, "Compute the discriminant D = b² − 4ac = 36 − 36 = 0. When D = 0, the roots are real and equal — here x² − 6x + 9 = (x − 3)², so both roots are 3. The trap is 'real and unequal', which needs D > 0. In practice: a zero discriminant in a profit equation means the profit curve just touches zero at one price — the only break-even price, which is also the best the firm can do.", 'c6', 'core', topic='Nature of roots — the discriminant'),
        M('m15', 'The roots of 2x² + 3x + 5 = 0 are:', ['Imaginary (not real)', 'Real and equal', 'Real, rational and unequal', 'Real, irrational and unequal'], 0, "The discriminant is D = b² − 4ac = 9 − 40 = −31. A negative discriminant means there are no real roots; the roots are imaginary (complex conjugates). The trap is 'real, irrational and unequal', which needs D positive but not a perfect square. In practice: if a profit equation has a negative discriminant, there is no break-even price at all — the business loses money (or always earns) at every price.", 'c6', 'core', topic='Nature of roots — the discriminant'),
        M('m16', 'The roots of x² − 5x + 3 = 0 are:', ['Real, irrational and unequal', 'Real, rational and unequal', 'Real and equal', 'Imaginary'], 0,
          "D = b² − 4ac = 25 − 12 = 13. It is positive, so the roots are real and unequal; and 13 is not a perfect square, so with rational coefficients the roots (5 ± √13)/2 are irrational. The trap is 'real, rational and unequal', which needs D to be a perfect square such as 9 or 16. In practice: irrational roots are perfectly valid answers; an analyst simply rounds them, for example to a break-even price in rupees and paise.", 'c6', 'moderate', topic='Nature of roots — the discriminant'),
        M('m17', 'The quadratic equation whose roots are 3 and −5 is:', ['x² + 2x − 15 = 0', 'x² − 2x − 15 = 0', 'x² + 2x + 15 = 0', 'x² − 8x + 15 = 0'], 0,
          'A quadratic with roots α and β is x² − (sum)x + (product) = 0. Sum = 3 + (−5) = −2 and product = −15, so the equation is x² + 2x − 15 = 0. The trap is x² − 2x − 15 = 0, which uses the sum without the minus sign in the formula; its roots would be 5 and −3. In practice: building an equation from known roots is how a modeller writes a profit function that breaks even at two chosen prices.', 'c5', 'core', topic='Quadratic equations — solving, sum and product of roots'),
        M('m18', 'For what positive value of k does x² + kx + 16 = 0 have equal roots?', ['8', '4', '16', '32'], 0, 'Equal roots need D = 0: k² − 4(1)(16) = 0, so k² = 64 and k = ±8; the positive value is 8. Check: x² + 8x + 16 = (x + 4)². The trap is 4, which takes √16 and forgets the factor 4 in 4ac; 16 and 32 are other slips. In practice: setting a discriminant to zero finds the exact parameter at which two solutions merge into one, such as the single price at which profit is just zero.', 'c6', 'moderate', '(4*16)**0.5', topic='Nature of roots — the discriminant'),
        M('m19', 'If one root of 4x² + 9x + p = 0 is the reciprocal of the other, p equals:', ['4', '9', '1/4', '−4'], 0, 'If one root is the reciprocal of the other, the roots are α and 1/α, so their product is 1. Product of roots = c/a = p/4, so p/4 = 1 and p = 4. The trap is 1/4, which sets p = a⁻¹ instead of p = a; 9 confuses the product with the x-coefficient. Rule: reciprocal roots means c = a. In practice: spotting such structural shortcuts saves precious seconds in the objective-type Paper 3, where every question is an MCQ.', 'c6', 'moderate', topic='Nature of roots — the discriminant'),
        M('m20', 'If 2 + √3 is a root of x² − 4x + c = 0 (rational coefficients), then c is:', ['1', '4', '7', '−1'], 0,
          'With rational coefficients, irrational roots come in conjugate pairs, so the other root is 2 − √3. Multiplying the two roots gives (2 + √3)(2 − √3) = 4 − 3 = 1, and that product equals c. (Sum = 4 matches the −4x term.) The trap is 7, which adds 4 and 3 instead of subtracting, while 4 confuses c with the sum of the roots. In practice: conjugate pairs let an analyst recover a whole equation from a single irrational root reported in a model.', 'c6', 'hard', topic='Nature of roots — the discriminant'),
        M('m21', 'If α and β are the roots of x² − 7x + 10 = 0, then α² + β² equals:', ['29', '49', '69', '9'], 0, 'Use α² + β² = (α + β)² − 2αβ. Here α + β = 7 and αβ = 10, so α² + β² = 49 − 20 = 29. Check with the actual roots 2 and 5: 4 + 25 = 29. The trap is 49, which squares the sum but forgets to subtract 2αβ; 69 adds it instead. In practice: identities like this let an analyst get variance-type figures from just the sum and product, without solving for each value.', 'c5', 'moderate', '7**2-2*10', topic='Quadratic equations — solving, sum and product of roots'),
        M('m22', 'If α and β are the roots of x² − 8x + 12 = 0, then 1/α + 1/β equals:', ['2/3', '3/2', '1/12', '8'], 0, 'Combine the fractions: 1/α + 1/β = (α + β)/αβ. Here α + β = 8 and αβ = 12, so the value is 8/12 = 2/3. Check: roots 2 and 6 give 1/2 + 1/6 = 2/3. The trap is 3/2, which inverts the fraction as αβ/(α + β). In practice: sums of reciprocals appear in combined-rate problems, such as two machines working together, which cost accountants meet in capacity planning.', 'c5', 'moderate', topic='Quadratic equations — solving, sum and product of roots'),
        M('m23', 'The roots of x² + (k − 4)x − 9 = 0 are equal in magnitude but opposite in sign when k is:', ['4', '−4', '9', '0'], 0,
          'Roots equal in magnitude but opposite in sign (like 3 and −3) add up to zero. Sum of roots = −b/a = −(k − 4), so −(k − 4) = 0 and k = 4. The equation becomes x² − 9 = 0, roots ±3. The trap is −4, which sets k + 4 = 0 by misreading the sign; 9 confuses the constant term with the condition. In practice: translating a verbal condition into a sum-or-product condition is a standard step in ICAI equation MCQs.', 'c6', 'moderate', topic='Nature of roots — the discriminant'),
        M('m24', 'The values of x satisfying x − 5√x + 6 = 0 are:', ['4 and 9', '2 and 3', '−2 and −3', '16 and 81'], 0, 'Substitute y = √x to get y² − 5y + 6 = 0, so y = 2 or 3. Since y = √x, x = 4 or 9. Check: 4 − 5(2) + 6 = 0 and 9 − 5(3) + 6 = 0. The trap is 2 and 3, which are the values of √x, not x — the student forgets to square back. In practice: substitution turns awkward forms into ordinary quadratics, a technique used whenever a model includes square-root terms.', 'c7', 'moderate', topic='Equations reducible to quadratics and word problems'),
        M('m25', 'The roots of x³ − 2x² − 5x + 6 = 0 are:', ['1, −2, 3', '1, 2, −3', '−1, 2, 3', '1, 2, 3'], 0,
          "Try x = 1: 1 − 2 − 5 + 6 = 0, so (x − 1) is a factor. Dividing leaves x² − x − 6 = (x − 3)(x + 2), so the roots are 1, −2 and 3. The trap is 1, 2, −3, which flips the signs of the quadratic's roots. Check: the roots add to 2 (= −b/a) and multiply to −6 (= −d/a). In practice: trial roots like 1, −1 and 2 are the quickest way to crack a cubic in an exam without a calculator's equation mode.", 'c8', 'moderate', topic='Cubic equations'),
        M('m26', 'The product of two consecutive positive integers is 132. The larger integer is:', ['12', '11', '13', '66'], 0, 'Let the integers be n and n + 1: n(n + 1) = 132, so n² + n − 132 = 0 = (n + 12)(n − 11). Since n is positive, n = 11 and the larger integer is 12. The trap is 11, the smaller integer; 66 halves 132. In practice: word problems that become quadratics, like finding dimensions from a known area, are common in business mathematics and in ICAI MCQs.', 'c7', 'core', '(-1+(1+4*132)**0.5)/2+1', topic='Equations reducible to quadratics and word problems'),
        M('m27', 'The sum of a number and its reciprocal is 2.9. If the number is greater than 1, it is:', ['2.5', '0.4', '2.9', '2'], 0,
          "Multiply x + 1/x = 2.9 by 10x: 10x² − 29x + 10 = 0. D = 841 − 400 = 441 = 21², so x = (29 ± 21)/20 = 2.5 or 0.4. Since the number exceeds 1, it is 2.5. The trap is 0.4, which is a valid root but fails the 'greater than 1' condition (it is the reciprocal of 2.5). In practice: a model often gives two mathematical answers and only one fits the business condition stated.", 'c7', 'hard', '(29+21)/20', topic='Equations reducible to quadratics and word problems'),
        M('m28', 'The digits of a two-digit number add up to 9. Reversing the digits increases the number by 27. The number is:', ['36', '63', '45', '27'], 0,
          'Let the number be 10a + b with a + b = 9. Reversing gives 10b + a, which is 27 more, so 9(b − a) = 27 and b − a = 3. Solving, a = 3 and b = 6: the number is 36. Check: 63 − 36 = 27. The trap is 63, which is the reversed number. In practice: digit-reversal checks are a classic fraud and data-entry test — a transposition error always makes a difference divisible by 9, which auditors use to trace mistakes.', 'c3', 'moderate', '10*3+6', topic='Simultaneous linear equations in two unknowns'),
        M('m29', '₹50,000 is invested partly at 8% and partly at 10% simple interest, earning ₹4,600 a year. The amount invested at 10% is:', ['₹30,000', '₹20,000', '₹25,000', '₹46,000'], 0,
          'Let ₹x be at 8%; the rest, 50,000 − x, is at 10%. Then 0.08x + 0.10(50,000 − x) = 4,600, so 5,000 − 0.02x = 4,600 and x = ₹20,000. The amount at 10% is ₹30,000. Check: 1,600 + 3,000 = 4,600. The trap is ₹20,000, which is the 8% portion. In practice: splitting a sum between two deposits to earn a target income is common in personal financial planning, for example between a bank FD and a small-savings scheme.', 'c2', 'moderate', '50000-(5000-4600)/0.02', topic='Linear (simple) equations in one unknown'),
        M('m30', 'The sum of the roots of 2x³ − 6x² + x + 5 = 0 is:', ['3', '−3', '2.5', '−2.5'], 0, 'For a cubic ax³ + bx² + cx + d = 0, the sum of the roots is −b/a. Here a = 2 and b = −6, so the sum = 6/2 = 3. The trap is −3, which forgets the minus sign in −b/a; −2.5 uses −d/a, which is the product of the roots. In practice: these root relations give quick checks on output from a cubic cost model before an analyst relies on it.', 'c8', 'moderate', topic='Cubic equations'),
    ]
    # independent verification of every MCQ key
    assert all(abs(v * v - 9 * v + 20) < 1e-9 for v in (4, 5))
    assert all(abs(v ** 3 - 2 * v * v - 5 * v + 6) < 1e-9 for v in (1, -2, 3))
    assert 11 * 12 == 132 and abs(2.5 + 1 / 2.5 - 2.9) < 1e-9 and 63 - 36 == 27
    assert abs(0.08 * 20000 + 0.10 * 30000 - 4600) < 1e-9 and abs((2 + 3 ** .5) * (2 - 3 ** .5) - 1) < 1e-9

    unit = {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch02', 'n': 1, 'title': 'Equations',
        'outcomes': ['Tell a conditional equation from an identity and classify equations by degree (linear, quadratic, cubic).',
                     'Solve linear equations in one unknown, and simultaneous linear equations in two and three unknowns by elimination, substitution and cross-multiplication.',
                     'Solve quadratic equations, use the sum and product of roots, form an equation from given roots and judge the nature of roots from the discriminant.',
                     'Solve equations reducible to quadratics and cubic equations (trial root and factorisation), and translate business word problems into equations.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 80, 'practice': 100}, 'prereq': ['fnd-p3-ch01-u01'],
                 'exam_tip': 'In the exam most equation MCQs are fastest by substituting the four options back into the equation. Learn −b/a, c/a and the discriminant cold — they answer many questions without solving anything.'},
        'concepts': [
            {'id': 'c1', 'title': 'What an equation is — conditional equation vs identity',
             'body': ['An equation is a statement that two expressions are equal. If the equality holds only for some values of the variable, it is a conditional equation; if it holds for every value, it is an identity.',
                      'A value of the variable that makes the equation true is a root (solution). Finding all roots is solving the equation.',
                      'The degree of an equation is the highest power of the unknown after simplification: degree 1 — linear (simple); degree 2 — quadratic; degree 3 — cubic. An equation of degree n has at most n roots.',
                      'Two or more linear equations that must be satisfied together by the same values are called simultaneous linear equations.'],
             'analogy': 'An identity is like "a dozen = 12" — always true. A conditional equation is a lock that opens only for the right combination.',
             'work': 'Every pricing, break-even or allocation question a client asks ("at what volume do we stop losing money?") is first written as an equation and then solved.'},
            {'id': 'c2', 'title': 'Linear (simple) equations in one unknown',
             'body': ['Standard form: ax + b = 0 with a ≠ 0; the single root is x = −b/a.',
                      'Method: clear fractions by multiplying by the LCM of the denominators, collect terms in x on one side and constants on the other (transposition changes the sign), then divide by the coefficient of x.',
                      'Word problems: name the unknown clearly ("let the son’s present age be x years"), translate each sentence into algebra, solve, and check the answer against the original words — not just against your equation.'],
             'analogy': 'Solving is like balancing a weighing scale: whatever you do to one pan you must do to the other.',
             'work': 'Break-even volume = fixed cost ÷ (selling price − variable cost per unit) is just the solution of a linear equation in the number of units.'},
            {'id': 'c3', 'title': 'Simultaneous linear equations in two unknowns',
             'body': ['Elimination: multiply the equations by suitable numbers so that one unknown has the same coefficient, then add or subtract to remove it. Substitution: express one unknown from one equation and put it into the other.',
                      'Cross-multiplication: for a₁x + b₁y + c₁ = 0 and a₂x + b₂y + c₂ = 0, x/(b₁c₂ − b₂c₁) = y/(c₁a₂ − c₂a₁) = 1/(a₁b₂ − a₂b₁). Keep every equation in the "= 0" form with signs, or the answer flips.',
                      'Number of solutions: if a₁/a₂ ≠ b₁/b₂ the lines intersect — a unique solution. If a₁/a₂ = b₁/b₂ ≠ c₁/c₂ the lines are parallel — no solution (inconsistent). If all three ratios are equal the lines coincide — infinitely many solutions.'],
             'analogy': 'Two equations are two clues in a detective story; each one alone leaves many suspects, together they point to one.',
             'work': 'Product-mix questions — how many units of two products use up the machine hours and labour hours exactly — are pairs of simultaneous equations.'},
            {'id': 'c4', 'title': 'Three linear equations in three unknowns',
             'body': ['Pick one unknown and eliminate it from two different pairs of equations. This leaves two equations in two unknowns; solve them, then back-substitute to find the third.',
                      'Shortcut patterns: when the equations are x + y, y + z, z + x type, add all three to get x + y + z first.',
                      'Always substitute the answer into the equation you did not use for elimination — it is the quickest check.'],
             'analogy': 'Like peeling an onion: remove one layer (one unknown) at a time until a single value is left.',
             'work': 'Allocating joint costs or service-department costs among three departments leads to three equations in three unknowns (the "simultaneous equation method" in cost accounting).'},
            {'id': 'c5', 'title': 'Quadratic equations — solving, sum and product of roots',
             'body': ['Standard form ax² + bx + c = 0, a ≠ 0. Solve by factorisation (split the middle term so that the two parts multiply to ac) or by the formula x = [−b ± √(b² − 4ac)] / 2a.',
                      'If α and β are the roots: α + β = −b/a and αβ = c/a.',
                      'An equation with roots α and β is x² − (sum of roots)x + (product of roots) = 0.',
                      'Useful identities: α² + β² = (α + β)² − 2αβ; (α − β)² = (α + β)² − 4αβ; 1/α + 1/β = (α + β)/αβ; α³ + β³ = (α + β)³ − 3αβ(α + β).'],
             'analogy': '−b/a and c/a are the "fingerprints" of a quadratic: you can identify the pair of roots without ever meeting them.',
             'work': 'Revenue that depends on price (price × demand) gives a quadratic profit function; its roots are the break-even prices.'},
            {'id': 'c6', 'title': 'Nature of roots — the discriminant',
             'body': ['The discriminant is D = b² − 4ac. For an equation with rational coefficients: D = 0 → roots real and equal; D > 0 and a perfect square → real, rational and unequal; D > 0 but not a perfect square → real, irrational and unequal; D < 0 → imaginary (no real roots).',
                      'Irrational roots come in conjugate pairs: if p + √q is a root, so is p − √q. Imaginary roots also come in conjugate pairs.',
                      'Special cases: roots reciprocal of each other → product 1, so c = a. Roots equal in magnitude and opposite in sign → sum 0, so b = 0. One root zero → c = 0.'],
             'analogy': 'The discriminant is a weather forecast for the roots: zero — one clear answer; positive — two answers; negative — no real answer at all.',
             'work': 'Before spending time solving, a quick D-check tells you whether a pricing or rate equation even has a real answer.'},
            {'id': 'c7', 'title': 'Equations reducible to quadratics and word problems',
             'body': ['Substitution turns many equations into quadratics: x⁴ − 13x² + 36 = 0 (put y = x²); x − 5√x + 6 = 0 (put y = √x); x + 1/x = k (multiply through by x); expressions repeated in brackets (put y = the bracket).',
                      'After substituting back, reject values that are impossible — a square root cannot be negative, a count of people cannot be fractional, a price cannot be negative.',
                      'Typical word problems: numbers and their reciprocals, consecutive integers, digits of a number, sharing a fixed cost among people, cost price and quantity, speed and time.'],
             'analogy': 'A disguised quadratic is a quadratic wearing a costume — substitution removes the costume.',
             'work': 'Cost-sharing and "if the price were lower we could buy more" situations are everyday versions of these problems in procurement and budgeting.'},
            {'id': 'c8', 'title': 'Cubic equations',
             'body': ['A cubic ax³ + bx² + cx + d = 0 has at most three roots. In this paper the cubic usually has an integer root that you find by trial (try ±1, ±2, ±3 — divisors of the constant term).',
                      'If x = k makes the expression zero, then (x − k) is a factor (factor theorem). Divide to get a quadratic and solve it.',
                      'Root relations: α + β + γ = −b/a; αβ + βγ + γα = c/a; αβγ = −d/a. These check an answer quickly or use extra information such as "the product of two roots is 12".',
                      'In MCQs, simply substitute the given triplets — any option with a value that fails is eliminated.'],
             'analogy': 'Finding one root of a cubic is like finding the first loose thread; pull it and the rest unravels into a quadratic.',
             'work': 'Cubics appear in volume-based packaging costs and in some multi-period rate calculations; in practice spreadsheets solve them, but the trial-root idea is the same.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Linear equation with fractions', 'difficulty': 'core', 'minutes': 3,
             'q': 'Solve (x + 3)/4 − (x − 2)/3 = 1/2.',
             'solution': [p('LCM of 4, 3 and 2 is 12. Multiply every term by 12: 3(x + 3) − 4(x − 2) = 6.'),
                          p(f'3x + 9 − 4x + 8 = 6 → −x + 17 = 6 → x = {x1}.'),
                          note('Check: 14/4 − 9/3 = 3.5 − 3 = 0.5. ✔ Watch the sign when removing −4(x − 2): it gives +8.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Age problem', 'difficulty': 'core', 'minutes': 3,
             'q': 'A father is four times as old as his son. After five years he will be three times as old as his son. Find their present ages.',
             'solution': [p('Let the son’s present age be S years; the father’s is 4S.'),
                          p('After 5 years: 4S + 5 = 3(S + 5) → 4S + 5 = 3S + 15 → S = 10.'),
                          p(f'Son {s2} years, father {f2} years. Check: after 5 years, 45 = 3 × 15. ✔')],
             'checks': c2},
            {'id': 'i3', 'title': 'Two equations — elimination and cross-multiplication', 'difficulty': 'core', 'minutes': 5,
             'q': 'Solve 3x + 4y = 18 and 5x − 2y = 4 (a) by elimination, (b) by cross-multiplication.',
             'solution': [p('(a) Multiply the second equation by 2: 10x − 4y = 8. Add to the first: 13x = 26 → x = 2. Then 4y = 18 − 6 → y = 3.'),
                          p('(b) Write both in "= 0" form: 3x + 4y − 18 = 0 and 5x − 2y − 4 = 0, so a₁ = 3, b₁ = 4, c₁ = −18, a₂ = 5, b₂ = −2, c₂ = −4.'),
                          table(['Denominator', 'Working', 'Value'], [['b₁c₂ − b₂c₁ (under x)', '4(−4) − (−2)(−18)', num(dx)], ['c₁a₂ − c₂a₁ (under y)', '(−18)(5) − (−4)(3)', num(dy)], ['a₁b₂ − a₂b₁ (under 1)', '3(−2) − 5(4)', num(dd)]]),
                          p(f'x = {num(dx)}/{num(dd)} = {num(x3)}; y = {num(dy)}/{num(dd)} = {num(y3)}. Both methods agree.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Three equations in three unknowns', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Solve: x + y + z = 9 … (1); 2x − y + z = 5 … (2); x + 2y − z = 4 … (3).',
             'solution': [p('Eliminate z. (1) + (3): 2x + 3y = 13 … (4). (2) + (3): 3x + y = 9 … (5).'),
                          p('From (5): y = 9 − 3x. Put in (4): 2x + 27 − 9x = 13 → −7x = −14 → x = 2.'),
                          p(f'y = 9 − 6 = {y4}; from (1): z = 9 − 2 − 3 = {z4}.'),
                          note('Check in (2): 4 − 3 + 4 = 5 ✔; in (3): 2 + 6 − 4 = 4 ✔.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Quadratic by formula; sum and product of roots', 'difficulty': 'core', 'minutes': 4,
             'q': 'Solve 6x² − 7x − 20 = 0 and verify the sum and product of the roots.',
             'solution': [p(f'a = 6, b = −7, c = −20. D = 49 + 480 = {d5} = 23².'),
                          p(f'x = (7 ± 23)/12 → x = 30/12 = {num(r5a)} or x = −16/12 = −4/3.'),
                          p('Sum = 2.5 − 4/3 = 7/6 = −b/a ✔. Product = 2.5 × (−4/3) = −10/3 = c/a = −20/6 ✔.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Nature of roots and forming new equations', 'difficulty': 'hard', 'minutes': 6,
             'q': '(a) Find k if 4x² − kx + 9 = 0 has equal roots. (b) If α, β are the roots of x² − 5x + 3 = 0, form the equation whose roots are α² and β². (c) Form the quadratic with rational coefficients one of whose roots is 3 + √2.',
             'solution': [p(f'(a) Equal roots → D = 0: k² − 4(4)(9) = 0 → k² = 144 → k = ±{num(k6)}.'),
                          p(f'(b) α + β = 5, αβ = 3. Sum of new roots α² + β² = 25 − 6 = {s6}; product α²β² = {p6}. Equation: x² − 19x + 9 = 0.'),
                          p('(c) Irrational roots come in conjugate pairs, so the other root is 3 − √2. Sum = 6, product = 9 − 2 = 7. Equation: x² − 6x + 7 = 0.')],
             'checks': c6},
            {'id': 'i7', 'title': 'Disguised quadratic and a purchase problem', 'difficulty': 'moderate', 'minutes': 6,
             'q': '(a) Solve x⁴ − 13x² + 36 = 0. (b) A shop spends ₹600 on pens. If each pen cost ₹5 less, it could buy 4 more pens for the same money. Find the price of a pen.',
             'solution': [p('(a) Put y = x²: y² − 13y + 36 = 0 → (y − 4)(y − 9) = 0 → y = 4 or 9 → x = ±2, ±3.'),
                          p('(b) Let the price be ₹p. 600/(p − 5) − 600/p = 4 → 600 × 5 = 4p(p − 5) → p² − 5p − 750 = 0.'),
                          p(f'D = 25 + 3,000 = {d7} = 55². p = (5 + 55)/2 = {num(p7)} (the negative root −25 is rejected).'),
                          p(f'Price ₹30; pens bought = {num(n7)}. Check: at ₹25, 600/25 = 24 = 20 + 4. ✔')],
             'checks': c7},
            {'id': 'i8', 'title': 'Cubic by trial root', 'difficulty': 'moderate', 'minutes': 4,
             'q': 'Solve x³ − 7x + 6 = 0.',
             'solution': [p('Try x = 1: 1 − 7 + 6 = 0, so (x − 1) is a factor.'),
                          p('Divide: x³ − 7x + 6 = (x − 1)(x² + x − 6) = (x − 1)(x + 3)(x − 2).'),
                          p('Roots: 1, 2, −3. Check: sum = 0 = −b/a (there is no x² term). ✔')],
             'checks': c8},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Break-even volume for a new product', 'role': 'Management accountant in an FMCG company',
             'situation': 'Fixed costs of a new line are ₹3,60,000 a month. Each unit sells for ₹250 and costs ₹160 in variable cost. The CFO asks how many units must be sold to break even.',
             'steps': ['Let the number of units be x. Revenue = 250x; total cost = 3,60,000 + 160x.', 'Break-even: 250x = 3,60,000 + 160x → 90x = 3,60,000.', f'x = {inr(bep)} units a month.', 'Present it with the contribution per unit (₹90) so the CFO sees how sensitive the answer is to price.'],
             'takeaway': 'Break-even is a linear equation; the contribution per unit is the coefficient of x.', 'think': 'If the price falls to ₹240, what happens to break-even volume?',
             'answer': 'Contribution falls to ₹80, so break-even rises to 3,60,000 ÷ 80 = 4,500 units.', 'checks': jb1},
            {'id': 'j2', 'title': 'Using up machine and labour hours exactly', 'role': 'Production planner (CA in industry)',
             'situation': 'Product A needs 2 machine hours and 3 labour hours; product B needs 4 machine hours and 1 labour hour. Next month 2,000 machine hours and 1,500 labour hours are available and management wants both fully used.',
             'steps': ['Machine hours: 2a + 4b = 2,000. Labour hours: 3a + b = 1,500.', 'From the second, b = 1,500 − 3a. Substitute: 2a + 6,000 − 12a = 2,000 → a = 400.', f'b = 1,500 − 1,200 = {inr(jbb)}.', 'Check: machine 800 + 1,200 = 2,000 ✔; labour 1,200 + 300 = 1,500 ✔.'],
             'takeaway': 'Simultaneous equations answer "how much of each" when every resource must be fully used.', 'think': 'Is full use of both resources always the most profitable plan?',
             'answer': 'Not necessarily — profit depends on contribution per unit. Choosing the best plan under limits is the linear-inequalities topic of the next chapter.', 'checks': jb2},
            {'id': 'j3', 'title': 'Back-solving the rate on a deposit', 'role': 'Articled assistant verifying interest income',
             'situation': 'A client’s two-year bank deposit of ₹5,00,000 matured at ₹5,83,200 with annual compounding. You need the rate to check against the bank’s certificate.',
             'steps': ['5,00,000(1 + r)² = 5,83,200 → (1 + r)² = 1.1664.', 'Take the square root: 1 + r = 1.08 (the negative root −1.08 is meaningless for a rate).', f'r = {num(r3)}% a year.', 'Match it with the certificate; any gap is a query for the client.'],
             'takeaway': 'A pure quadratic (no x term) is solved by taking the square root — then discard the root that makes no business sense.', 'think': 'Why reject 1 + r = −1.08?',
             'answer': 'It would give r = −208%, which is impossible for a deposit that grew in value.', 'checks': jb3},
        ],
        'mcqs': mcqs,
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Solve: 2x + y − z = 3; x + 2y + z = 9; 3x − y + 2z = 10. Show the elimination steps.',
             'model': [p('Label the equations (1), (2), (3). Eliminate z.'),
                       p('(1) + (2): 3x + 3y = 12 → x + y = 4 … (4).'),
                       p('2 × (1) + (3): 4x + 2y − 2z + 3x − y + 2z = 6 + 10 → 7x + y = 16 … (5).'),
                       p(f'(5) − (4): 6x = 12 → x = {num(qx)}; from (4) y = {num(qy)}; from (1) z = 2x + y − 3 = {num(qz)}.'),
                       note('Check in (2): 2 + 4 + 3 = 9 ✔; in (3): 6 − 2 + 6 = 10 ✔.')],
             'scheme': [{'id': 's1', 'pt': 'Eliminates the same variable from two pairs', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Obtains x + y = 4 and 7x + y = 16', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'x = 2, y = 2, z = 3', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Verifies in an unused equation', 'm': 0.5, 'skill': 'presentation'}],
             'remarks': ['Most errors come from eliminating different variables from the two pairs, which leaves three unknowns again.'],
             'mistakes': ['Sign slips when adding 2 × (1) and (3).', 'Back-substituting into the wrong equation and not checking.'],
             'tips': ['Number your equations and say which ones you combine.', 'In the MCQ version, just substitute the four option-triplets.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'A group of friends hires a bus for ₹14,400, sharing the cost equally. Four friends drop out, and each of the rest pays ₹600 more. How many friends were there originally?',
             'model': [p('Let the original number be n. Original share = 14,400/n; new share = 14,400/(n − 4).'),
                       p('14,400/(n − 4) − 14,400/n = 600 → 14,400 × 4 = 600 n(n − 4) → n² − 4n − 96 = 0.'),
                       p(f'D = 16 + 384 = {q2d} = 20². n = (4 + 20)/2 = {num(q2n)} (the root −8 is rejected).'),
                       p('Check: 14,400/12 = ₹1,200 and 14,400/8 = ₹1,800 — a rise of ₹600. ✔')],
             'scheme': [{'id': 's1', 'pt': 'Correct equation from the words', 'm': 1.5, 'skill': 'application'},
                        {'id': 's2', 'pt': 'Reduces to n² − 4n − 96 = 0', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'n = 12; rejects negative root with reason', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Verification', 'm': 0.5, 'skill': 'presentation'}],
             'remarks': ['Candidates who subtract the shares the wrong way round get n² − 4n + 96 = 0, which has no real roots — a signal that the set-up is wrong. Those who write n + 4 instead of n − 4 get n² + 4n − 96 = 0 and the wrong answer 8 — always check against the story.'],
             'mistakes': ['Subtracting in the wrong order (old share − new share).', 'Keeping the negative root.'],
             'tips': ['Write "let n = …" with units; it earns the set-up mark.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Solve x³ − 4x² + x + 6 = 0 and verify your roots using the sum and product relations.',
             'model': [p('Try divisors of 6. x = −1: −1 − 4 − 1 + 6 = 0, so (x + 1) is a factor.'),
                       p('Divide: x³ − 4x² + x + 6 = (x + 1)(x² − 5x + 6) = (x + 1)(x − 2)(x − 3).'),
                       p('Roots: −1, 2, 3.'),
                       p('Verify: sum = −1 + 2 + 3 = 4 = −b/a = 4 ✔; product = (−1)(2)(3) = −6 = −d/a = −6 ✔.')],
             'scheme': [{'id': 's1', 'pt': 'Finds a trial root and states the factor', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Correct quadratic quotient x² − 5x + 6', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'All three roots', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Verification with −b/a and −d/a', 'm': 1, 'skill': 'presentation'}],
             'remarks': ['Long division errors are common — synthetic division (coefficients 1, −4, 1, 6) is faster and safer.'],
             'mistakes': ['Writing the product of roots as d/a instead of −d/a for a cubic.'],
             'tips': ['List the divisors of the constant term before trying roots.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Identity: true for all x. Conditional equation: true for some x only. Degree = highest power.',
                        'Linear: ax + b = 0 → x = −b/a. Clear fractions with the LCM first.',
                        'Two unknowns: elimination, substitution, cross-multiplication x/(b₁c₂ − b₂c₁) = y/(c₁a₂ − c₂a₁) = 1/(a₁b₂ − a₂b₁).',
                        'Unique solution if a₁/a₂ ≠ b₁/b₂; none if a₁/a₂ = b₁/b₂ ≠ c₁/c₂; infinitely many if all three equal.',
                        'Quadratic: x = [−b ± √(b² − 4ac)]/2a; α + β = −b/a; αβ = c/a; equation x² − Sx + P = 0.',
                        'D = b² − 4ac: 0 equal; > 0 square rational unequal; > 0 non-square irrational unequal; < 0 imaginary.',
                        'Cubic: find a trial root k, divide by (x − k), solve the quadratic; Σα = −b/a, Σαβ = c/a, αβγ = −d/a.'],
            'remember': ['Reciprocal roots → c = a. Opposite roots → b = 0.', 'Irrational/imaginary roots come in conjugate pairs.', 'Reject roots that break the story (negative counts, negative prices, √ negative).'],
            'traps': ['Sum of roots is −b/a, not b/a.', 'Cubic product of roots is −d/a.', 'In cross-multiplication keep the equations in "= 0" form with signs.'],
        },
        'quickref': [
            {'k': 'Linear root', 'v': 'ax + b = 0 → x = −b/a'},
            {'k': 'Cross-multiplication', 'v': 'x/(b₁c₂ − b₂c₁) = y/(c₁a₂ − c₂a₁) = 1/(a₁b₂ − a₂b₁)'},
            {'k': 'Quadratic formula', 'v': 'x = [−b ± √(b² − 4ac)] / 2a'},
            {'k': 'Sum / product of roots', 'v': 'α + β = −b/a; αβ = c/a'},
            {'k': 'Equation from roots', 'v': 'x² − (sum)x + (product) = 0'},
            {'k': 'Discriminant', 'v': 'D = b² − 4ac'},
            {'k': 'α² + β²', 'v': '(α + β)² − 2αβ'},
            {'k': 'Cubic relations', 'v': 'Σα = −b/a; Σαβ = c/a; αβγ = −d/a'},
        ],
        'viva': viva(),
        'cases': [case],
    }
    return unit


def viva():
    return [
        V('v1', 'What is the difference between a conditional equation and an identity?',
          'A conditional equation is true only for particular values of the variable, which are its roots. An identity is true for every value of the variable, for example x plus one whole squared equals x squared plus two x plus one.',
          [P('p1', 'Conditional equation: true only for certain values (its roots)', 5, ALT('conditional {m} {q}', m=['', 'equation', 'equation true', 'equation hold', 'equation satisfied', 'equation valid', 'equation correct'], q=['only', 'particular', 'certain', 'some', 'specific', 'not for all', 'not every', 'not all', 'limited'])),
           P('p2', 'Identity: true for every value of the variable', 5, ALT('identity {m} {q}', m=['', 'true', 'hold', 'holds good', 'satisfied', 'valid', 'correct'], q=['every', 'all', 'any', 'always', 'whatever', 'each']))], 'c1'),
        V('v2', 'When do two linear equations in two unknowns have a unique solution, no solution, or infinitely many solutions?',
          'If the ratio of the x coefficients is not equal to the ratio of the y coefficients, the lines intersect and there is a unique solution. If those two ratios are equal but the ratio of the constants is different, the lines are parallel and there is no solution. If all three ratios are equal, the lines coincide and there are infinitely many solutions.',
          [P('p1', 'Unique solution when a₁/a₂ ≠ b₁/b₂ (lines intersect)', 4, 'not equal|unequal|different|differ', 'intersect|unique|one solution|single solution|meet at one', min=2),
           P('p2', 'No solution when a₁/a₂ = b₁/b₂ ≠ c₁/c₂ (parallel lines)', 3, 'parallel no solution|parallel there is no solution|parallel lines no solution|no solution parallel|parallel never meet|parallel inconsistent|inconsistent parallel|parallel lines never meet'),
           P('p3', 'Infinitely many when all three ratios are equal (coincident lines)', 3, 'all three ratio equal|all ratio equal|all three equal|three ratios equal|all equal', 'infinit|coincid|countless|endless|many solution', min=2)], 'c3'),
        V('v3', 'For the quadratic a x squared plus b x plus c equals zero, what are the sum and the product of the roots, and how do you form an equation from given roots?',
          'The sum of the roots is minus b by a and the product of the roots is c by a. An equation with given roots is x squared minus the sum of the roots times x plus the product of the roots equals zero.',
          [P('p1', 'Sum of roots = −b/a', 4, ALT('sum {r} minus b by a', 'sum {r} minus b over a', 'sum {r} negative b by a', 'sum {r} negative b over a', 'sum {r} minus b divided by a', 'sum {r} b by a negative', r=['', 'of roots', 'of the roots', 'is', 'equals', 'of roots is', 'of the roots is', 'of roots equals'])),
           P('p2', 'Product of roots = c/a', 3, ALT('product {r} c by a', 'product {r} c over a', 'product {r} c divided by a', r=['', 'of roots', 'of the roots', 'is', 'equals', 'of roots is', 'of the roots is', 'of roots equals'])),
           P('p3', 'Equation: x² − (sum)x + (product) = 0', 3, 'x squar minus sum|x square minus sum|x square minus the sum|x squared minus sum|minus sum x plus product|minus sum of roots x plus product|minus sum times x plus product|minus sum of root times x plus product|minus s x plus p')], 'c5'),
        V('v4', 'What is the discriminant of a quadratic, and what does it tell you about the roots?',
          'The discriminant is b squared minus four a c. If it is zero the roots are real and equal. When it is positive and also a perfect square, we get two different rational roots; when it is positive but not a perfect square, we get two different irrational roots. If it is negative the roots are imaginary, that is, not real.',
          [P('p1', 'D = b² − 4ac', 2, 'b squar minus 4 ac|b square minus 4ac|b squared minus 4 a c|b squar minus 4 c|b square minus four ac|b squared minus four ac|b2 minus 4ac'),
           P('p2', 'D = 0 → real and equal roots', 2, ALT('{z} {r} equal', '{z} equal root', 'equal root {w} {z}', z=['zero', '0', 'is zero', 'equals zero', 'is 0'], r=['real and', 'roots are real and', 'the roots are real and', 'roots', 'roots are', 'real', 'then real and', 'then roots are real and', 'then the roots are real and'], w=['when', 'if', 'for'])),
           P('p3', 'D > 0: perfect square → rational unequal; otherwise irrational unequal', 4, 'positive|greater than zero|more than zero|greater than 0', 'perfect square', 'rational', 'irrational|not perfect square irrational|not a perfect square irrational|not square irrational|not perfect square roots irrational|not perfect square roots are irrational', min=4),
           P('p4', 'D < 0 → imaginary (no real) roots', 2, ALT('negative {r} imaginar', 'negative {r} not real', 'negative {r} no real', 'less than zero {r} imaginar', 'less than zero {r} not real', 'imaginar {w} negative', r=['', 'roots', 'the roots are', 'roots are', 'then roots are', 'then the roots are', 'then'], w=['when', 'if', 'when it is', 'if it is', 'when d is', 'if d is', 'when discriminant is']))], 'c6'),
        V('v5', 'How do you solve a cubic equation in the CA Foundation exam?',
          'First find one root by trial, trying small integers that divide the constant term. If x equals k makes the expression zero, then x minus k is a factor by the factor theorem. Divide the cubic by x minus k to get a quadratic, and solve the quadratic by factorisation or the formula. In an MCQ you can also substitute the given options.',
          [P('p1', 'Find one root by trial (divisors of the constant term)', 3, 'trial|trying|try|guess|hit and trial|inspection', 'root|value|factor|divisor|divides', min=2),
           P('p2', 'x − k is a factor (factor theorem)', 3, 'factor theorem|minus k factor|minus k is a factor|is a factor|becomes a factor|will be a factor|gives a factor'),
           P('p3', 'Divide to get a quadratic and solve it', 3, 'divid|division|synthetic|reduce|reduces|quotient', 'quadratic'),
           P('p4', 'In MCQs substitute the options', 1, 'substitut|put the option|check the option|plug|try the option|options')], 'c8'),
    ]
