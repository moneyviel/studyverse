"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 3 Linear Inequalities (single unit).
Original explanations, numbers and questions; scope follows the ICAI study material (May 2027 onwards).
Every corner point and optimum is computed here and stored with a check expression."""
from fractions import Fraction as Fr
from itertools import combinations
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch03-u01'


class Checks(Checks):
    """lib.Checks (stored value rounded to 2 dp for the validator) that returns the unrounded value for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = eval(expr, {'__builtins__': {}}, {'round': round})
        return int(round(v)) if abs(v - round(v)) < 1e-9 else v


def M(mid, q, options, answer, explain, concept, difficulty='moderate', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def corners(cons):
    """Brute-force corner points of {a*x + b*y (<=|>=) c}. cons: list of (a, b, op, c). Used to verify every hand-worked answer."""
    lines = [(a, b, c) for a, b, _, c in cons]
    pts = set()
    for (a1, b1, c1), (a2, b2, c2) in combinations(lines, 2):
        d = a1 * b2 - a2 * b1
        if d == 0: continue
        x = Fr(c1 * b2 - c2 * b1, d); y = Fr(a1 * c2 - a2 * c1, d)
        ok = all((a * x + b * y <= c) if op == '<=' else (a * x + b * y >= c) for a, b, op, c in cons)
        if ok: pts.add((x, y))
    return sorted(pts)


NN = [(1, 0, '>=', 0), (0, 1, '>=', 0)]


def opt(cons, zx, zy, kind):
    pts = corners(cons)
    vals = [(zx * x + zy * y, (x, y)) for x, y in pts]
    return (max if kind == 'max' else min)(vals), pts


def build():
    # ---------- verification of every LPP used in the unit ----------
    I3 = [(2, 3, '<=', 120), (1, 2, '<=', 70)] + NN
    (z3, pt3), cp3 = opt(I3, 400, 700, 'max')
    assert cp3 == [(0, 0), (0, 35), (30, 20), (60, 0)] and z3 == 26000 and pt3 == (30, 20)
    I4 = [(1, 2, '>=', 10), (3, 2, '>=', 18)] + NN
    (z4, pt4), cp4 = opt(I4, 6, 10, 'min')
    assert cp4 == [(0, 9), (4, 3), (10, 0)] and z4 == 54
    M12 = [(1, 1, '<=', 4), (1, 3, '<=', 6)] + NN
    assert opt(M12, 2, 3, 'max')[0] == (9, (3, 1))
    M13 = [(1, 1, '>=', 4), (1, 3, '>=', 6)] + NN
    assert opt(M13, 3, 5, 'min')[0] == (14, (3, 1))
    M23 = [(1, 0, '<=', 4), (0, 1, '<=', 5), (1, 1, '<=', 7)] + NN
    assert len(opt(M23, 1, 2, 'max')[1]) == 5 and opt(M23, 1, 2, 'max')[0][0] == 12
    K = [(3, 1, '>=', 9), (1, 2, '>=', 8)] + NN
    assert opt(K, 500, 400, 'min')[0] == (2200, (2, 3))
    Q1 = [(2, 1, '<=', 10), (1, 2, '<=', 8)] + NN
    assert opt(Q1, 3, 4, 'max')[0] == (20, (4, 2))
    Q2 = [(1, 2, '<=', 40), (2, 1, '<=', 50)] + NN
    assert opt(Q2, 30, 20, 'max')[0] == (800, (20, 10))
    Q3 = [(1, 1, '>=', 6), (1, 3, '>=', 12)] + NN
    assert opt(Q3, 20, 30, 'min')[0] == (150, (3, 3))
    J2 = [(5, 1, '<=', 50), (1, 0, '>=', 2), (0, 1, '<=', 30), (0, 1, '>=', 0)]
    assert opt(J2, 60000, 15000, 'max')[0] == (690000, (4, 30))

    # ---------- Illustration 1 ----------
    c1 = Checks()
    c1.add('(1+7)/(3-5)', 'x boundary from 3x − 7 = 5x + 1 → x = −4')
    c1.add('(-3-5)/2', 'lower bound −4')
    c1.add('(9-5)/2', 'upper bound 2')
    # ---------- Illustration 2 ----------
    c2 = Checks()
    c2.add('12/2', 'x-intercept of 2x + 3y = 12')
    c2.add('12/3', 'y-intercept')
    c2.add('2*0+3*0', 'test point (0, 0): LHS = 0 ≤ 12, so origin side')
    # ---------- Illustration 3 ----------
    c3 = Checks()
    c3.add('120/2', 'carpentry x-intercept')
    c3.add('70/2', 'polishing y-intercept')
    yi = c3.add('(2*70-120)/(2*2-3)', 'y at intersection')
    xi = c3.add('70-2*20', 'x at intersection')
    zA = c3.add('400*60', 'Z at (60, 0)')
    zB = c3.add('700*35', 'Z at (0, 35)')
    zC = c3.add('400*30+700*20', 'Z at (30, 20)')
    c3.add('70-60', 'idle polishing hours at (60, 0)')
    # ---------- Illustration 4 ----------
    c4 = Checks()
    c4.add('18/2', '(0, 9) on 3x + 2y = 18')
    x4 = c4.add('(18-10)/(3-1)', 'x at intersection')
    y4 = c4.add('(10-4)/2', 'y at intersection')
    w1 = c4.add('10*9', 'Z at (0, 9)')
    w2 = c4.add('6*4+10*3', 'Z at (4, 3)')
    w3 = c4.add('6*10', 'Z at (10, 0)')
    # ---------- Illustration 5 (matrix method) ----------
    c5 = Checks()
    for (x, y) in cp3:
        c5.add(f'{int(x)}*400+{int(y)}*700', f'EC row for ({x}, {y})')
    ec = table(['Corner point (row of E)', 'x × 400 + y × 700', 'Z (₹)'], [[f'({x}, {y})', f'{x} × 400 + {y} × 700', int(400 * x + 700 * y)] for x, y in cp3])
    # ---------- Illustration 6 ----------
    c6 = Checks()
    c6.add('2*10+3*25', '(10, 25): carpentry 95 ≤ 120')
    c6.add('10+2*25', '(10, 25): polishing 60 ≤ 70')
    c6.add('2*20+3*30', '(20, 30): carpentry 130 > 120 — infeasible')
    c6.add('20+2*30', '(20, 30): polishing 80 > 70 — infeasible')

    # ---------- Jobs ----------
    j2c = Checks()
    j2c.add('(50-30)/5', 'x where 5x + y = 50 meets y = 30')
    j2c.add('60000*2', 'reach at (2, 0)')
    j2c.add('60000*10', 'reach at (10, 0)')
    j2c.add('60000*2+15000*30', 'reach at (2, 30)')
    jz = j2c.add('60000*4+15000*30', 'reach at (4, 30)')
    j2c.add('50000*4+10000*30', 'spend at (4, 30)')
    j3c = Checks()
    j3c.add('120-(2*30+3*20)', 'carpentry hours idle at (30, 20)')
    j3c.add('70-(30+2*20)', 'polishing hours idle at (30, 20)')
    j3c.add('120-2*60', 'carpentry idle at (60, 0)')
    j3c.add('70-60', 'polishing idle at (60, 0)')

    # ---------- Questions ----------
    q1c = Checks()
    q1c.add('(16-10)/(4-1)', 'y at intersection of 2x + y = 10 and x + 2y = 8')
    q1c.add('8-2*2', 'x at intersection')
    q1c.add('3*5', 'Z at (5, 0)')
    q1c.add('3*4+4*2', 'Z at (4, 2)')
    q1c.add('4*4', 'Z at (0, 4)')
    q2c = Checks()
    q2c.add('(80-50)/(4-1)', 'y at intersection')
    q2c.add('40-2*10', 'x at intersection')
    q2c.add('30*25', 'Z at (25, 0)')
    q2c.add('20*20', 'Z at (0, 20)')
    q2c.add('30*20+20*10', 'Z at (20, 10)')
    q3c = Checks()
    q3c.add('(12-6)/(3-1)', 'y at intersection')
    q3c.add('6-3', 'x at intersection')
    q3c.add('30*6', 'Z at (0, 6)')
    q3c.add('20*3+30*3', 'Z at (3, 3)')
    q3c.add('20*12', 'Z at (12, 0)')

    # ---------- Case ----------
    case = {
        'id': 'k1', 'title': 'Cheapest fertiliser mix for a farm client', 'difficulty': 'hard',
        'case': ('Shakti Agro must supply at least 9 kg of nitrogen (N) and 8 kg of phosphate (P) to a field. Fertiliser A contains 3 kg N and 1 kg P per bag and costs ₹500 a bag. '
                 'Fertiliser B contains 1 kg N and 2 kg P per bag and costs ₹400 a bag. Let x and y be the bags of A and B bought. The aim is to meet both requirements at the lowest cost.'),
        'mcqs': [
            M('k1a', 'The nitrogen requirement is written as:', ['3x + y ≥ 9', '3x + y ≤ 9', 'x + 2y ≥ 9', '3x + 2y ≥ 9'], 0, 'Each bag of A gives 3 kg N and each bag of B gives 1 kg N; "at least" means ≥.', 'c3', 'core'),
            M('k1b', 'The two requirement lines 3x + y = 9 and x + 2y = 8 meet at:', ['(2, 3)', '(3, 2)', '(1, 6)', '(4, 2)'], 0, 'From the first, y = 9 − 3x. Then x + 18 − 6x = 8 → x = 2, y = 3.', 'c4', 'moderate'),
            M('k1c', 'The minimum cost is:', ['₹2,200', '₹3,600', '₹4,000', '₹1,700'], 0, 'Corners: (0, 9) → ₹3,600; (2, 3) → 1,000 + 1,200 = ₹2,200; (8, 0) → ₹4,000.', 'c5', 'hard', '500*2+400*3'),
            M('k1d', 'If the farm buys only fertiliser A (the corner (8, 0)), how much nitrogen is supplied in excess of the requirement?', ['15 kg', '24 kg', '0 kg', '9 kg'], 0, '8 bags × 3 kg = 24 kg against 9 kg needed: 15 kg extra.', 'c5', 'moderate', '8*3-9'),
            M('k1e', 'Why can we not find a maximum cost for this problem?', ['The feasible region is unbounded', 'There are no corner points', 'The constraints are inconsistent', 'The objective function is not linear'], 0,
              'With "≥" constraints the region stretches away indefinitely; cost can rise without limit, so only a minimum exists.', 'c4', 'moderate'),
        ]}

    mcqs = [
        M('m1', 'The solution of 4x − 3 > 2x + 7 is:', ['x > 5', 'x < 5', 'x > 2', 'x ≥ 5'], 0, '2x > 10 → x > 5. The sign stays because we divided by +2.', 'c1', 'core'),
        M('m2', 'The solution of −2x + 5 ≤ 11 is:', ['x ≥ −3', 'x ≤ −3', 'x ≥ 3', 'x ≤ 3'], 0, '−2x ≤ 6 → dividing by −2 reverses the sign: x ≥ −3.', 'c1', 'core'),
        M('m3', 'When both sides of an inequality are multiplied by a negative number:', ['The inequality sign is reversed', 'The sign is unchanged', 'The inequality becomes an equation', 'Only the left side changes'], 0, 'Multiplying or dividing by a negative number reverses the direction of the inequality.', 'c1', 'core'),
        M('m4', 'The solution of −1 ≤ (3x − 2)/4 < 2 is:', ['−2/3 ≤ x < 10/3', '−2/3 < x ≤ 10/3', '−2 ≤ x < 10', '2/3 ≤ x < 10/3'], 0, '×4: −4 ≤ 3x − 2 < 8 → −2 ≤ 3x < 10 → −2/3 ≤ x < 10/3.', 'c1', 'moderate'),
        M('m5', 'While graphing 3x + 2y < 12, the line 3x + 2y = 12 is drawn:', ['As a broken (dashed) line, because points on it are excluded', 'As a solid line', 'Parallel to the x-axis', 'Through the origin'], 0, 'A strict inequality excludes the boundary, shown by a broken line.', 'c2', 'core'),
        M('m6', 'The region represented by 2x + 5y ≤ 10 is:', ['The side of the line 2x + 5y = 10 that contains the origin, including the line', 'The side away from the origin', 'Only the line itself', 'The whole plane'], 0, 'Test (0, 0): 0 ≤ 10 is true, so the origin side (with the line) is the region.', 'c2', 'core'),
        M('m7', 'Which point satisfies both x + y ≤ 6 and x − y ≥ 2?', ['(4, 1)', '(1, 4)', '(6, 2)', '(2, 3)'], 0, '(4, 1): 5 ≤ 6 and 3 ≥ 2. (1, 4) and (2, 3) fail the second; (6, 2) fails the first.', 'c4', 'core'),
        M('m8', 'The inequalities x ≥ 0 and y ≥ 0 together represent:', ['The first quadrant including the axes', 'The second quadrant', 'The whole plane', 'Only the origin'], 0, 'Both coordinates non-negative: the first quadrant with its boundary axes.', 'c2', 'core'),
        M('m9', 'The region x ≤ 0, y ≥ 0 lies in the:', ['Second quadrant', 'First quadrant', 'Third quadrant', 'Fourth quadrant'], 0, 'x negative or zero and y positive or zero: second quadrant.', 'c2', 'core'),
        M('m10', 'The line 4x + 3y = 24 cuts the axes at:', ['(6, 0) and (0, 8)', '(8, 0) and (0, 6)', '(4, 0) and (0, 3)', '(24, 0) and (0, 24)'], 0, 'y = 0 → x = 6; x = 0 → y = 8.', 'c2', 'core'),
        M('m11', 'Maximise Z = 3x + 2y subject to x + y ≤ 5, x ≥ 0, y ≥ 0. The maximum value is:', ['15', '10', '25', '5'], 0, 'Corners (0, 0), (5, 0), (0, 5): Z = 0, 15, 10.', 'c5', 'core', '3*5'),
        M('m12', 'Maximise Z = 2x + 3y subject to x + y ≤ 4, x + 3y ≤ 6, x, y ≥ 0. The maximum value is:', ['9', '8', '6', '12'], 0, 'Corners (0, 0), (4, 0), (0, 2), (3, 1): Z = 0, 8, 6, 9.', 'c5', 'moderate', '2*3+3*1'),
        M('m13', 'Minimise Z = 3x + 5y subject to x + y ≥ 4, x + 3y ≥ 6, x, y ≥ 0. The minimum value is:', ['14', '18', '20', '10'], 0, 'Corners (0, 4), (3, 1), (6, 0): Z = 20, 14, 18.', 'c5', 'moderate', '3*3+5*1'),
        M('m14', 'If an optimal solution exists, it occurs:', ['At a corner (extreme) point of the feasible region', 'Always at the origin', 'At the centre of the feasible region', 'Outside the feasible region'], 0, 'The optimum of a linear objective over a convex polygon is attained at a vertex.', 'c5', 'core'),
        M('m15', 'If the objective function line is parallel to an edge of the feasible region along which the optimum lies:', ['There are multiple optimal solutions with the same optimal value', 'There is no solution', 'The region is unbounded', 'The optimum is at the origin'], 0, 'Every point on that edge gives the same best value.', 'c5', 'moderate'),
        M('m16', 'A feasible region that is not enclosed on all sides is called:', ['Unbounded', 'Infeasible', 'Degenerate', 'Empty'], 0, 'It extends indefinitely in some direction; a maximum may not exist (a minimum may).', 'c4', 'core'),
        M('m17', 'Shirts need 2 hours and trousers 3 hours of tailoring; at most 60 hours are available. With x shirts and y trousers:', ['2x + 3y ≤ 60', '2x + 3y ≥ 60', '3x + 2y ≤ 60', 'x + y ≤ 60'], 0, 'Hours used = 2x + 3y and cannot exceed 60.', 'c3', 'core'),
        M('m18', 'Food P gives 4 units of protein per kg and food Q gives 5 units. A diet needs at least 20 units. The constraint is:', ['4x + 5y ≥ 20', '4x + 5y ≤ 20', '5x + 4y ≥ 20', 'x + y ≥ 20'], 0, '"At least" → ≥.', 'c3', 'core'),
        M('m19', 'Non-negativity constraints state that:', ['x ≥ 0 and y ≥ 0', 'x > 0 and y > 0', 'x ≤ 0 and y ≤ 0', 'x + y ≥ 0 only'], 0, 'Quantities produced or bought cannot be negative (zero is allowed).', 'c3', 'core'),
        M('m20', 'The region 3x − 4y ≥ 12 is:', ['The side of the line not containing the origin', 'The side containing the origin', 'Only the first quadrant', 'The line only'], 0, 'At (0, 0): 0 ≥ 12 is false, so the origin is not in the region.', 'c2', 'moderate'),
        M('m21', 'How many integers satisfy both 2x − 3 > 0 and x < 5?', ['3', '4', '2', '5'], 0, 'x > 1.5 and x < 5 → x = 2, 3, 4.', 'c1', 'moderate'),
        M('m22', 'How many integers satisfy −3 ≤ 2x + 1 < 7?', ['5', '6', '4', '3'], 0, '−4 ≤ 2x < 6 → −2 ≤ x < 3 → −2, −1, 0, 1, 2.', 'c1', 'moderate'),
        M('m23', 'The region x ≥ 0, y ≥ 0, x ≤ 4, y ≤ 5, x + y ≤ 7 has corner points (0, 0), (4, 0), (4, 3), (2, 5), (0, 5). The maximum of Z = x + 2y is:', ['12', '10', '11', '14'], 0, 'Z = 0, 4, 10, 12, 10. Maximum 12 at (2, 5).', 'c5', 'moderate', '2+2*5'),
        M('m24', 'At the point (3, 2), how much of the resource in the constraint 2x + y ≤ 10 is left unused?', ['2', '8', '0', '4'], 0, 'Used = 2(3) + 2 = 8; unused = 10 − 8 = 2.', 'c6', 'core'),
        M('m25', 'The region y ≥ x + 2 consists of points:', ['On and above the line y = x + 2', 'Below the line only', 'On the line only', 'To the right of the line only'], 0, 'For each x, y must be at least x + 2.', 'c2', 'core'),
        M('m26', 'Which of these is NOT a linear inequality?', ['x² + y ≤ 4', '3x − y > 2', 'x ≥ 0', '2x + 5y ≤ 30'], 0, 'x² makes it non-linear.', 'c1', 'core'),
        M('m27', 'On a number line, x > 2 is shown by:', ['An open (hollow) circle at 2 with shading to the right', 'A filled circle at 2 with shading to the right', 'An open circle at 2 with shading to the left', 'A filled circle at 2 only'], 0, 'Strict inequality → 2 itself excluded (open circle).', 'c1', 'core'),
        M('m28', 'Using the matrix method, the extreme points (0, 0), (5, 0), (2, 3), (0, 4) are multiplied by the objective column (3, 4) for Z = 3x + 4y. The maximum element of EC is:', ['18', '16', '15', '20'], 0, 'EC = (0, 15, 18, 16). The largest, 18, is at (2, 3).', 'c5', 'moderate', '3*2+4*3'),
    ]

    unit = {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch03', 'n': 1, 'title': 'Linear Inequalities',
        'outcomes': ['Solve linear inequalities in one variable, applying the sign-reversal rule, and show the solution space on a number line.',
                     'Graph linear inequalities in two variables and identify the common (feasible) region of a system, including non-negativity constraints.',
                     'Develop inequalities from a descriptive business problem (decision variables, objective, constraints).',
                     'Find corner points, evaluate the objective function (including by the extreme-point matrix method) and identify the optimal solution and unused resources.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 75}, 'prereq': ['fnd-p3-ch02-u01'],
                 'exam_tip': 'Optimisation MCQs are fastest by listing the corner points and substituting them in the objective function — never test points inside the region. For "which point is feasible", substitute each option in every constraint.'},
        'concepts': [
            {'id': 'c1', 'title': 'Inequalities and their rules; one-variable solution space',
             'body': ['An inequality states that one quantity is less than (<), less than or equal to (≤), greater than (>) or greater than or equal to (≥) another. A linear inequality has variables only to the first power.',
                      'Rules: adding or subtracting the same number on both sides keeps the sign; multiplying or dividing by a positive number keeps the sign; multiplying or dividing by a negative number reverses the sign.',
                      'The set of values that satisfy an inequality is its solution space (S.S.). On a number line, a strict inequality (x > 2) is shown with an open circle at 2; an inclusive one (x ≥ 2) with a filled circle.',
                      'Double inequalities such as −3 < 2x + 5 ≤ 9 are solved by doing the same operation on all three parts.'],
             'analogy': 'An inequality is a speed limit — not one exact speed but a whole range that is allowed.',
             'work': 'Budgets ("spend at most ₹5 lakh"), capacity ("no more than 2,000 machine hours") and contracts ("at least 500 units a month") are inequalities long before they become numbers in a plan.'},
            {'id': 'c2', 'title': 'Graphing a linear inequality in two variables',
             'body': ['Step 1: replace the inequality sign by "=" and draw the line, usually through its two intercepts (put x = 0, then y = 0).',
                      'Step 2: draw the line solid if the inequality includes equality (≤, ≥) and broken (dashed) if it is strict (<, >).',
                      'Step 3: test a point not on the line — the origin is easiest. If it satisfies the inequality, shade the side containing it; otherwise shade the other side.',
                      'Standard regions: x ≥ 0, y ≥ 0 is the first quadrant; y ≤ mx + c lies on and below the line; y ≥ mx + c lies on and above it.'],
             'analogy': 'The boundary line is a fence; the test point tells you which side of the fence is your garden.',
             'work': 'A simple graph shows management at a glance which combinations of output are possible with current resources.'},
            {'id': 'c3', 'title': 'Developing inequalities from a descriptive problem',
             'body': ['Identify the decision variables (what is to be decided — units of each product, bags of each fertiliser) and give each a symbol.',
                      'Write each limitation as an inequality: "at most / not more than / available" → ≤; "at least / not less than / minimum" → ≥.',
                      'Add the non-negativity constraints x ≥ 0, y ≥ 0 — quantities cannot be negative.',
                      'Write the objective function — the quantity to be maximised (profit, reach) or minimised (cost, time) — as a linear expression in the variables.'],
             'analogy': 'Formulation is translation: business English on the left, algebra on the right — the meaning must not change.',
             'work': 'Most real errors in planning models come from mis-translating a constraint (≤ instead of ≥, per unit instead of total), not from the arithmetic.'},
            {'id': 'c4', 'title': 'Common region (feasible region) and corner points',
             'body': ['The region where all the inequalities of a system hold at the same time is the feasible region (solution set). Every point in it is a feasible solution.',
                      'A feasible region may be bounded (enclosed on all sides — a polygon) or unbounded (extending without limit). If no point satisfies all constraints, the system is infeasible.',
                      'Corner (extreme) points are the vertices of the feasible region. Find them as axis intercepts or by solving two boundary equations simultaneously, then check that the point satisfies all the other constraints.'],
             'analogy': 'Each constraint cuts away part of a map; what is left after all the cuts is the area you may build on.',
             'work': 'Listing corner points is the core of a capacity plan: each corner is a "pure" plan that uses up some resources completely.'},
            {'id': 'c5', 'title': 'Optimal solution — corner point method and matrix method',
             'body': ['If a linear objective has an optimum over a feasible region, it is attained at a corner point. So evaluate Z at every corner: the largest value is the maximum, the smallest the minimum.',
                      'Matrix (extreme-point) method used in the study material: write the corner points as the rows of a matrix E and the objective coefficients as a column vector C. The product EC lists Z at each corner; pick the largest element for maximisation or the smallest for minimisation.',
                      'If the objective line is parallel to an edge on which the optimum lies, every point of that edge is optimal — multiple optimal solutions with the same optimal value.',
                      'In an unbounded region a minimum may exist while a maximum does not (or the reverse), depending on the direction of the objective.'],
             'analogy': 'Pushing a ruler (the objective line) across the region, the last point it touches is always a corner — or a whole edge if the ruler lies flat along it.',
             'work': 'Product-mix, diet, transport and advertising-mix decisions in management accounting are solved this way (larger versions use software, but the logic is identical).'},
            {'id': 'c6', 'title': 'Summary of the graphical method and unused resources',
             'body': ['(1) Formulate: variables, objective, constraints, non-negativity. (2) Graph each constraint and shade the feasible region. (3) Find the corner points. (4) Evaluate the objective at each corner and choose the optimum.',
                      '(5) Put the optimal values back into each constraint: the difference between the resource available and the resource used is the unused (idle) resource — useful when deciding whether to sell, rent out or reduce that resource.'],
             'analogy': 'After choosing the best route, check the fuel gauge — how much of each resource is still in the tank.',
             'work': 'Idle-capacity figures feed straight into decisions such as accepting a special order or renting out spare machine time.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'One-variable inequalities', 'difficulty': 'core', 'minutes': 3,
             'q': 'Solve (a) 3x − 7 ≤ 5x + 1; (b) −3 < 2x + 5 ≤ 9. Show each solution on a number line.',
             'solution': [p('(a) 3x − 5x ≤ 1 + 7 → −2x ≤ 8. Divide by −2 and reverse the sign: x ≥ −4. Number line: filled circle at −4, shading to the right.'),
                          p('(b) Subtract 5 from all three parts: −8 < 2x ≤ 4. Divide by 2: −4 < x ≤ 2. Number line: open circle at −4, filled circle at 2, shading between.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Graphing one inequality', 'difficulty': 'core', 'minutes': 3,
             'q': 'Show the region 2x + 3y ≤ 12.',
             'solution': [p('Boundary 2x + 3y = 12: x-intercept (6, 0), y-intercept (0, 4). Draw a solid line (≤ includes the line).'),
                          p('Test (0, 0): 0 ≤ 12 is true, so shade the side of the line containing the origin.'),
                          note('If the question adds x ≥ 0, y ≥ 0, the region becomes the triangle with vertices (0, 0), (6, 0), (0, 4).')],
             'checks': c2},
            {'id': 'i3', 'title': 'Formulate and solve a product-mix problem', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'A workshop makes chairs and tables. A chair needs 2 hours of carpentry and 1 hour of polishing; a table needs 3 hours of carpentry and 2 hours of polishing. Each week 120 carpentry hours and 70 polishing hours are available. Profit is ₹400 per chair and ₹700 per table. How many of each should be made to maximise profit?',
             'solution': [p('Let x = chairs, y = tables. Maximise Z = 400x + 700y subject to 2x + 3y ≤ 120 (carpentry), x + 2y ≤ 70 (polishing), x ≥ 0, y ≥ 0.'),
                          p('Intercepts: carpentry (60, 0), (0, 40); polishing (70, 0), (0, 35). Both regions contain the origin.'),
                          p(f'Intersection: x = 70 − 2y → 2(70 − 2y) + 3y = 120 → y = {int(yi)}, x = {int(xi)}.'),
                          table(['Corner point', 'Z = 400x + 700y (₹)'], [['(0, 0)', 0], ['(60, 0)', int(zA)], ['(0, 35)', int(zB)], ['(30, 20)', int(zC)]]),
                          p('Optimal plan: 30 chairs and 20 tables a week; maximum profit ₹26,000.'),
                          note('(60, 0) uses only 60 polishing hours — 10 hours idle. (0, 40) is not a corner because it breaks the polishing limit (80 > 70).')],
             'checks': c3},
            {'id': 'i4', 'title': 'A minimisation problem with an unbounded region', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Minimise Z = 6x + 10y subject to x + 2y ≥ 10, 3x + 2y ≥ 18, x ≥ 0, y ≥ 0.',
             'solution': [p('Boundaries: x + 2y = 10 through (10, 0) and (0, 5); 3x + 2y = 18 through (6, 0) and (0, 9). Origin fails both, so the region lies away from the origin — unbounded.'),
                          p(f'Intersection: subtract the equations → 2x = 8 → x = {int(x4)}, y = {int(y4)}.'),
                          table(['Corner point', 'Z = 6x + 10y'], [['(0, 9)', int(w1)], ['(4, 3)', int(w2)], ['(10, 0)', int(w3)]]),
                          p('Minimum Z = 54 at x = 4, y = 3. There is no maximum, because the region is unbounded and Z keeps rising.'),
                          note('(0, 5) and (6, 0) are not corners: (0, 5) breaks 3x + 2y ≥ 18 and (6, 0) breaks x + 2y ≥ 10.')],
             'checks': c4},
            {'id': 'i5', 'title': 'The extreme-point matrix method', 'difficulty': 'core', 'minutes': 4,
             'q': 'For the workshop in Illustration 3, use the matrix method to find the optimum.',
             'solution': [p('E is the 4 × 2 matrix of corner points; C is the column (400, 700) of objective coefficients. Each element of EC is x × 400 + y × 700 for one corner.'),
                          ec, p('The largest element, 26,000, is in the row (30, 20): make 30 chairs and 20 tables.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Is this plan feasible?', 'difficulty': 'core', 'minutes': 3,
             'q': 'For the workshop in Illustration 3, are the plans (10, 25) and (20, 30) feasible?',
             'solution': [table(['Plan (x, y)', 'Carpentry 2x + 3y ≤ 120', 'Polishing x + 2y ≤ 70', 'Feasible?'], [['(10, 25)', '95 ✔', '60 ✔', 'Yes'], ['(20, 30)', '130 ✘', '80 ✘', 'No']]),
                          note('A plan must satisfy every constraint (including non-negativity). Failing even one makes it infeasible.')],
             'checks': c6},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Bakery product mix', 'role': 'CA advising a small bakery',
             'situation': 'The owner bakes cakes and bread with a limited oven time and flour supply and asks, "How many of each should I bake to earn the most?"',
             'steps': ['Define x = cakes and y = loaves per day; collect oven minutes and flour per unit and the daily limits.', 'Write each limit as ≤, add x, y ≥ 0, and write profit per unit as the objective.',
                       'Plot, find the corners, evaluate the profit at each, and recommend the best corner.', 'Report idle oven time or flour at that plan — it shows where extra sales effort could pay.'],
             'takeaway': 'The graphical method is a practical advisory tool for small clients with two main products.', 'think': 'What would you check if the owner says cakes must be at least 10 a day for regular customers?',
             'answer': 'Add x ≥ 10 as a new constraint, redraw the region and recheck the corners — the optimum may move.'},
            {'id': 'j2', 'title': 'Advertising mix within a budget', 'role': 'Finance manager in a consumer company',
             'situation': 'TV spots cost ₹50,000 and reach 60,000 viewers each; radio spots cost ₹10,000 and reach 15,000 listeners each. Budget ₹5,00,000; at least 2 TV spots; at most 30 radio spots.',
             'steps': ['x = TV spots, y = radio spots. Maximise reach Z = 60,000x + 15,000y.', 'Constraints: 50,000x + 10,000y ≤ 5,00,000 (i.e. 5x + y ≤ 50), x ≥ 2, y ≤ 30, y ≥ 0.',
                       'Corners: (2, 0), (10, 0), (2, 30), (4, 30). Reach: 1,20,000; 6,00,000; 5,70,000; 6,90,000.', f'Best: 4 TV and 30 radio spots, reach {inr(jz)}, spending the whole budget.'],
             'takeaway': 'Even "soft" marketing decisions can be framed as a small linear programme.', 'think': 'Why is (10, 0) a corner but not optimal?',
             'answer': 'It spends the full budget on TV (reach 6,00,000), but moving budget into radio buys reach more cheaply (1.5 per rupee vs 1.2), until the 30-spot radio limit binds at (4, 30).', 'checks': j2c},
            {'id': 'j3', 'title': 'Idle capacity at the chosen plan', 'role': 'Cost accountant reviewing the workshop plan',
             'situation': 'Management chose 30 chairs and 20 tables (Illustration 3). The plant head asks whether any carpentry or polishing hours will be idle.',
             'steps': ['Carpentry used = 2(30) + 3(20) = 120 of 120 → idle 0.', 'Polishing used = 30 + 2(20) = 70 of 70 → idle 0.', 'Both resources are binding — any increase in output needs more of both.',
                       'Compare with the plan (60, 0): carpentry idle 0, polishing idle 10 hours.'],
             'takeaway': 'At an intersection corner both constraints are binding; at an axis corner some resource is often idle.', 'think': 'If 10 more polishing hours could be hired, would the optimum change?',
             'answer': 'Yes — the polishing line moves outward, the intersection corner shifts, and the new corner must be re-evaluated.', 'checks': j3c},
        ],
        'mcqs': mcqs,
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Find the corner points of the region 2x + y ≤ 10, x + 2y ≤ 8, x ≥ 0, y ≥ 0, and find the maximum of Z = 3x + 4y over it.',
             'model': [p('Intercepts: 2x + y = 10 → (5, 0), (0, 10); x + 2y = 8 → (8, 0), (0, 4). Origin satisfies both, so the region is towards the origin.'),
                       p('Intersection: double the second equation: 2x + 4y = 16; subtract the first: 3y = 6 → y = 2, x = 4.'),
                       table(['Corner point', 'Z = 3x + 4y'], [['(0, 0)', 0], ['(5, 0)', 15], ['(4, 2)', 20], ['(0, 4)', 16]]),
                       p('Maximum Z = 20 at (4, 2).')],
             'scheme': [{'id': 's1', 'pt': 'Correct intercepts and side of each line', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Intersection (4, 2)', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Correct list of corners (excludes (8, 0) and (0, 10))', 'm': 1, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'Evaluates Z and states the maximum', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Including (8, 0) or (0, 10) as corners is the classic error — they violate the other constraint.'],
             'mistakes': ['Not checking each candidate corner against all constraints.', 'Evaluating Z at the intercepts of only one line.'],
             'tips': ['Put the corners and Z values in a two-column table — quick to mark and to check.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'A firm makes products P and Q. P needs 1 machine hour and 2 labour hours; Q needs 2 machine hours and 1 labour hour. 40 machine hours and 50 labour hours are available. Profit is ₹30 per unit of P and ₹20 per unit of Q. Formulate and solve graphically.',
             'model': [p('Let x, y be units of P and Q. Maximise Z = 30x + 20y subject to x + 2y ≤ 40, 2x + y ≤ 50, x ≥ 0, y ≥ 0.'),
                       p('Intercepts: machine (40, 0), (0, 20); labour (25, 0), (0, 50). Intersection: x = 40 − 2y → 80 − 4y + y = 50 → y = 10, x = 20.'),
                       table(['Corner point', 'Z = 30x + 20y (₹)'], [['(0, 0)', 0], ['(25, 0)', 750], ['(20, 10)', 800], ['(0, 20)', 400]]),
                       p('Make 20 units of P and 10 of Q; maximum profit ₹800.')],
             'scheme': [{'id': 's1', 'pt': 'Correct objective and constraints with non-negativity', 'm': 1.5, 'skill': 'application'},
                        {'id': 's2', 'pt': 'Correct corners including (20, 10)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Evaluates Z, states optimum ₹800 at (20, 10)', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Swapping the coefficients (writing 2x + y ≤ 40 for machine hours) is the commonest formulation error.'],
             'mistakes': ['Missing x, y ≥ 0.', 'Choosing (40, 0) which breaks the labour constraint.'],
             'tips': ['Make a small data table (product × resource) before writing constraints.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Minimise Z = 20x + 30y subject to x + y ≥ 6, x + 3y ≥ 12, x ≥ 0, y ≥ 0. Comment on the existence of a maximum.',
             'model': [p('Lines: x + y = 6 through (6, 0), (0, 6); x + 3y = 12 through (12, 0), (0, 4). The origin fails both, so the region lies away from it and is unbounded.'),
                       p('Intersection: subtract → 2y = 6 → y = 3, x = 3.'),
                       table(['Corner point', 'Z = 20x + 30y'], [['(0, 6)', 180], ['(3, 3)', 150], ['(12, 0)', 240]]),
                       p('Minimum Z = 150 at (3, 3). No maximum exists because the region is unbounded and Z increases without limit.')],
             'scheme': [{'id': 's1', 'pt': 'Identifies region away from origin (unbounded)', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Corners (0, 6), (3, 3), (12, 0)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Minimum 150 at (3, 3)', 'm': 1, 'skill': 'conclusion'},
                        {'id': 's4', 'pt': 'Comment: no maximum (unbounded region)', 'm': 0.5, 'skill': 'analysis'}],
             'remarks': ['Many candidates use (0, 4) or (6, 0) as corners — both fail the other constraint.'],
             'mistakes': ['Shading towards the origin for ≥ constraints.', 'Stating a maximum for an unbounded region.'],
             'tips': ['Always test the origin for each constraint and write the result in one line.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Adding/subtracting keeps the sign; multiplying/dividing by a negative reverses it.',
                        'Open circle for < or >, filled circle for ≤ or ≥ on a number line.',
                        'Graph: draw the boundary (solid for ≤/≥, broken for </>), test the origin, shade the correct side.',
                        'Feasible region = common region of all constraints including x, y ≥ 0; bounded or unbounded.',
                        'Optimum occurs at a corner point; evaluate Z at all corners (or use EC in the matrix method).',
                        'Objective parallel to an optimal edge → multiple optimal solutions with the same value.',
                        'Unused resource = available − used at the optimal point.'],
            'remember': ['"At most / not more than / available" → ≤; "at least / minimum" → ≥.', 'A candidate corner must satisfy every constraint.', 'Unbounded region: a minimum may exist with no maximum.'],
            'traps': ['Forgetting to reverse the sign when dividing by a negative.', 'Taking axis intercepts that violate another constraint as corners.', 'Testing interior points instead of corners.'],
        },
        'quickref': [
            {'k': 'Sign reversal', 'v': 'Multiply or divide by a negative number → reverse <, ≤, >, ≥'},
            {'k': 'Boundary line', 'v': 'Solid for ≤ / ≥; broken for < / >'},
            {'k': 'Test point', 'v': 'Use (0, 0) unless the line passes through it'},
            {'k': 'First quadrant', 'v': 'x ≥ 0, y ≥ 0'},
            {'k': 'Corner-point rule', 'v': 'Optimum of a linear objective lies at a vertex of the feasible region'},
            {'k': 'Matrix method', 'v': 'E (corner points as rows) × C (objective coefficients) → Z at each corner'},
            {'k': 'Multiple optima', 'v': 'Objective line parallel to an optimal edge'},
            {'k': 'Unused resource', 'v': 'Available − used at the optimal point'},
        ],
        'viva': viva(),
        'cases': [case],
    }
    return unit


def viva():
    NEG = ['negative number', 'negative', 'minus number', 'negative quantity']
    return [
        V('v1', 'What happens to an inequality when you add a number to both sides, and when you multiply both sides by a negative number?',
          'Adding or subtracting the same number on both sides does not change the inequality sign. Multiplying or dividing both sides by a positive number also keeps the sign, but multiplying or dividing by a negative number reverses the direction of the inequality.',
          [P('p1', 'Adding/subtracting the same number keeps the sign', 4, ALT('{a} {m} {k}', a=['add', 'adding', 'subtract', 'added', 'addition'], m=['', 'same number', 'same number both side', 'same quantity', 'same quantity both side', 'number', 'number both side', 'both side', 'same', 'same both side', 'constant', 'constant both side', 'subtract same number both side', 'subtract same number', 'subtract same quantity'], k=['not change', 'no change', 'unchanged', 'same sign', 'remain', 'stay', 'keep', 'doesn t change', 'no effect', 'does not affect'])),
           P('p2', 'Multiplying/dividing by a negative number reverses the sign', 6, ALT('{n} revers', '{n} flip', '{n} chang the direction', '{n} opposite', 'revers {w} {n}', 'flip {w} {n}', n=NEG, w=['when multiplied by', 'if multiplied by', 'when we multiply by', 'on multiplying by', 'when divided by', 'if we multiply by']))], 'c1'),
        V('v2', 'How do you graph a linear inequality in two variables?',
          'Replace the inequality sign by an equals sign and draw that line, usually through its intercepts on the axes. Draw it solid if equality is included and broken if the inequality is strict. Then test a point such as the origin: if the origin satisfies the inequality, shade the side containing it, otherwise shade the other side.',
          [P('p1', 'Draw the boundary line by treating it as an equation (intercepts)', 3, 'equal sign|equals sign|equation|equality|replace|boundary|intercept', 'line|draw|plot|graph', min=2),
           P('p2', 'Solid line for ≤/≥, broken (dashed) for strict < / >', 3,
             ALT('{s} {x} {i}', '{i} {y} {s}', s=['solid', 'firm', 'continuous', 'full'], x=['', 'line', 'line if', 'if', 'for', 'when', 'line for', 'line when'], i=['equal', 'included', 'inclusive', 'or equal'], y=['draw', 'draw it', 'use', 'use a', 'line', 'draw a']),
             ALT('{d} {x} {t}', '{t} {y} {d}', d=['broken', 'dash', 'dotted', 'dot'], x=['', 'line', 'line if', 'if', 'for', 'when', 'line for', 'line when'], t=['strict', 'excluded', 'not included', 'less than', 'greater than'], y=['draw', 'draw it', 'use', 'use a', 'line', 'draw a'])),
           P('p3', 'Test a point (origin) to decide the side to shade', 4, 'test|check|substitut|put|try', 'origin|zero zero|0 0|point', 'shade|side|region|half plane|half', min=3)], 'c2'),
        V('v3', 'What is a feasible region in a system of linear inequalities?',
          'The feasible region is the common region where all the constraints, including the non-negativity constraints, are satisfied at the same time. Every point inside it or on its boundary is a feasible solution. It can be bounded, like a closed polygon, or unbounded.',
          [P('p1', 'Common region satisfying all constraints simultaneously', 5, 'common|overlap|intersection|satisf all|satisfy all|all constraint|all the constraint|all inequal|all the inequal|every constraint|every inequal|same time|simultaneous', 'region|area|set|part', min=2),
           P('p2', 'Every point in it is a feasible solution', 3, 'every point|each point|any point|all point', 'feasible|possible|valid|allowed|acceptable', min=2),
           P('p3', 'May be bounded or unbounded', 2, 'bounded|unbounded|closed|open|polygon')], 'c4'),
        V('v4', 'Where does the optimal solution of a linear programme lie, and how do you find it graphically?',
          'If an optimal solution exists it lies at a corner point, or extreme point, of the feasible region. So we find all the corner points, put each one into the objective function, and pick the largest value for a maximisation problem or the smallest value for a minimisation problem.',
          [P('p1', 'At a corner (extreme / vertex) point of the feasible region', 4, 'corner|vertex|vertices|extreme point|extreme|vertice'),
           P('p2', 'Evaluate the objective function at every corner', 3, 'objective|z|profit function|cost function', 'put|substitut|evaluat|calculat|comput|find value|plug|value', min=2),
           P('p3', 'Largest value for maximisation, smallest for minimisation', 3,
             ALT('{l} {x} maximi', 'maximi {y} {l}', l=['largest', 'highest', 'greatest', 'biggest', 'maximum value', 'max value'], x=['', 'value', 'value for', 'for'], y=['', 'choose', 'pick', 'select', 'take', 'problem choose', 'problem pick', 'problem take', 'we choose', 'we pick', 'gives']),
             ALT('{l} {x} minimi', 'minimi {y} {l}', l=['smallest', 'lowest', 'least', 'minimum value', 'min value'], x=['', 'value', 'value for', 'for'], y=['', 'choose', 'pick', 'select', 'take', 'problem choose', 'problem pick', 'problem take', 'we choose', 'we pick', 'gives']))], 'c5'),
        V('v5', 'When does a linear programme have multiple optimal solutions?',
          'When the objective function line is parallel to an edge, or side, of the feasible region on which the optimum lies. Then every point on that edge gives the same optimal value, so there are many optimal solutions but only one optimal value.',
          [P('p1', 'Objective line parallel to an edge of the feasible region', 6, 'parallel', 'edge|side|boundary|constraint line|binding line|constraint', 'objective|z line|iso profit|profit line|cost line', min=2),
           P('p2', 'All points on that edge give the same optimal value', 4, 'same optimal value|same value|same optimum|same maximum|same minimum|equal value|identical value|same z|value remain|value is same|value is the same|same profit|same cost')], 'c5'),
        V('v6', 'How do you develop, or formulate, inequalities from a word problem?',
          'First identify the decision variables and give them symbols, such as x and y units of two products. Then write each limited resource or requirement as an inequality, using less than or equal to for at most and greater than or equal to for at least. Add the non-negativity constraints x and y greater than or equal to zero, and write the objective function to be maximised or minimised.',
          [P('p1', 'Identify decision variables', 3, 'decision variable|variable|unknown|symbol', min=1),
           P('p2', 'Write each limit as an inequality (≤ for at most, ≥ for at least)', 3, 'constraint|inequalit|limit|restriction|resource|requirement', 'at most|at least|less than or equal|greater than or equal|not more than|not less than', min=2),
           P('p3', 'Non-negativity constraints x, y ≥ 0', 2, 'non negativ|nonnegativ|not negative|cannot be negative|greater than or equal to zero|zero or more|can t be negative'),
           P('p4', 'Objective function to maximise or minimise', 2, 'objective|goal|profit function|cost function|maximi|minimi', min=1)], 'c3'),
    ]
