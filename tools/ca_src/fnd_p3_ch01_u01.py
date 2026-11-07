"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 1 Ratio and Proportion, Indices, Logarithms (single unit).
Original explanations, numbers and questions; scope follows the ICAI study material (May 2027 onwards).
Every numerical answer is computed here and stored with a check expression."""
import math
from fractions import Fraction as F
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch01-u01'


def num(v, dp=4):
    """Plain number text without trailing zeros: 3.3750 -> '3.375'."""
    v = round(v, dp)
    if v == int(v): return str(int(v))
    return f'{v:.{dp}f}'.rstrip('0').rstrip('.')


def M(mid, q, options, answer, explain, concept, difficulty='moderate', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if topic: d['topic'] = topic
    if check is not None: d['check'] = check
    return d


class Checks(Checks):
    """Same as lib.Checks (stored value rounded to 2 dp for the validator) but returns the unrounded value for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = eval(expr, {'__builtins__': {}}, {'round': round})
        return int(round(v)) if abs(v - round(v)) < 1e-9 else v


def build():
    # ---------------- Illustration 1: dividing a sum in a ratio of fractions ----------------
    c1 = Checks()
    c1.add('12/2', 'LCM 12 × 1/2')
    c1.add('12/3', 'LCM 12 × 1/3')
    c1.add('12/4', 'LCM 12 × 1/4')
    tot1 = c1.add('6+4+3', 'sum of ratio terms')
    unit1 = c1.add('390000/13', 'value of one part')
    a1 = c1.add('390000*6/13', 'Asha’s share')
    b1 = c1.add('390000*4/13', 'Bhanu’s share')
    k1 = c1.add('390000*3/13', 'Chetan’s share')
    share_tbl = table(['Partner', 'Ratio term', 'Share (₹)'], [['Asha', '6', a1], ['Bhanu', '4', b1], ['Chetan', '3', k1], ['Total', '13', 390000]], num=[2], total=True)

    # ---------------- Illustration 2: ratio after adding a number ----------------
    c2 = Checks()
    k2 = c2.add('(4*6-3*6)/(21-20)', 'k from 4(5k+6) = 3(7k+6)')
    n2a = c2.add('5*6', 'first number')
    n2b = c2.add('7*6', 'second number')
    c2.add('(30+6)/(42+6)', 'new ratio as a decimal (should be 0.75 = 3/4)')

    # ---------------- Illustration 3: proportionals ----------------
    c3 = Checks()
    fp = c3.add('8*12/3', 'fourth proportional to 3, 8, 12')
    tp = c3.add('10*10/4', 'third proportional to 4 and 10')
    mp = c3.add('(9*64)**0.5', 'mean proportional between 9 and 64')

    # ---------------- Illustration 4: componendo and dividendo ----------------
    c4 = Checks()
    c4.add('(7+3)/(7-3)', 'x/y after C&D on 7/3')
    c4.add('(2+1)/(2-1)', 'root(x+4)/root(x-4) after C&D on 2/1')
    x4 = c4.add('(36+4)/(9-1)', 'x from x+4 = 9(x-4)')
    c4.add('((5+4)**0.5+(5-4)**0.5)/((5+4)**0.5-(5-4)**0.5)', 'substitution check: LHS at x = 5 equals 2')

    # ---------------- Illustration 5: indices ----------------
    c5 = Checks()
    c5.add('27**(2/3)', '27^(2/3)')
    c5.add('16**(-3/4)', '16^(-3/4)')
    c5.add('81**(-1/4)', '81^(-1/4)')
    v5 = c5.add('27**(2/3)*16**(-3/4)/81**(-1/4)', 'value of the expression')
    x5 = c5.add('(3+5)/(5-1)', 'x from x + 3 = 5x - 5')
    c5.add('2**(2+3)-32**(2-1)', 'check: both sides equal at x = 2 (difference 0)')

    # ---------------- Illustration 6: logs from given tables ----------------
    c6 = Checks()
    l72 = c6.add('3*0.3010+2*0.4771', 'log 72 = 3 log 2 + 2 log 3')
    l045 = c6.add('2*0.4771-(0.3010+1)', 'log 0.45 = 2 log 3 − log 20')
    c6.add('1+(2*0.4771-(0.3010+1))', 'mantissa of log 0.45 (bar form 1̄.6532)')
    d6 = c6.add('50*0.3010', 'log 2^50')
    c6.add('15+1', 'number of digits in 2^50')
    assert abs(math.log10(72) - l72) < 0.001 and abs(math.log10(0.45) - l045) < 0.001
    assert len(str(2 ** 50)) == 16

    # ---------------- Illustration 7: change of base ----------------
    c7 = Checks()
    c7.add('1+1/2+1/4', 'coefficient of log2 x')
    lx = c7.add('7/(7/4)', 'log2 x')
    x7 = c7.add('2**4', 'x')
    c7.add('4+4/2+4/4', 'check: log2 16 + log4 16 + log16 16 = 7')
    assert abs(math.log(16, 2) + math.log(16, 4) + math.log(16, 16) - 7) < 1e-9

    # ---------------- Job 3: years for sales to grow five-fold ----------------
    cj = Checks()
    l12 = cj.add('2*0.3010+0.4771-1', 'log 1.2 = log 12 − 1')
    l5 = cj.add('1-0.3010', 'log 5 = 1 − log 2')
    yrs = cj.add('round((1-0.3010)/(2*0.3010+0.4771-1),2)', 'years n = log 5 / log 1.2')
    assert abs(math.log(5) / math.log(1.2) - yrs) < 0.03

    # ---------------- Questions ----------------
    q1c = Checks()
    # A:B = 2:3 and B:C = 4:5 → A:B:C = 8:12:15
    q1c.add('2*4', 'A term = 2 × 4')
    q1c.add('3*4', 'B term = 3 × 4')
    q1c.add('3*5', 'C term = 3 × 5')
    q1sum = q1c.add('8+12+15', 'sum of terms')
    q1a = q1c.add('245000*8/35', 'A’s share')
    q1b = q1c.add('245000*12/35', 'B’s share')
    q1cc = q1c.add('245000*15/35', 'C’s share')

    q2c = Checks()
    q2_l = q2c.add('3*0.3010+0.4771', 'log 24 = 3 log 2 + log 3')
    q2_r = q2c.add('3*0.3010+0.4771-2', 'log 0.24 = log 24 − 2')
    q2_m = q2c.add('3*0.3010+0.4771-2+2', 'mantissa .3801 (bar form 1̄.3801)')
    q2_d = q2c.add('20*0.4771', 'log 3^20')
    q2c.add('9+1', 'digits in 3^20')
    assert len(str(3 ** 20)) == 10

    q3c = Checks()
    q3c.add('(5+3)/(5-3)', 'C&D on 5:3 gives a:b = 4')
    q3_v = q3c.add('(3*16+2)/(3*16-2)', 'value of (3a²+2b²)/(3a²−2b²) with a:b = 4:1 → 50/46')
    q3c.add('round(50/46,4)', 'as a decimal')

    # ---------------- MCQ figures ----------------
    mc = Checks()
    m_cr = '15*8/(28*9)'
    mcqs = [
        M('m1', 'The ratio compounded of 3 : 4 and 5 : 9 is:', ['5 : 12', '8 : 13', '15 : 13', '12 : 5'], 0,
          "To compound two ratios, multiply the antecedents together and the consequents together: (3 × 5) : (4 × 9) = 15 : 36, which reduces to 5 : 12. The trap is 8 : 13, got by adding the terms — ratios are never added term by term; 12 : 5 simply writes the answer upside down. In practice: when a firm's capital ratio is combined with a time ratio to share partnership profit, the partners' accountant compounds the two ratios exactly this way.", 'c2', 'core', topic='Types of ratios'),
        M('m2', 'The duplicate ratio of 4 : 7 is:', ['16 : 49', '2 : √7', '64 : 343', '8 : 14'], 0,
          'A duplicate ratio squares both terms, so 4 : 7 becomes 4² : 7² = 16 : 49. The tempting wrong answers are its cousins: 64 : 343 cubes the terms (triplicate ratio) and 2 : √7 takes square roots (sub-duplicate ratio); 8 : 14 just doubles the terms and is still 4 : 7. In practice: an area-based rent split works like this — if two shop frontages are in the ratio 4 : 7 and the shops are similar in shape, their floor areas are in the duplicate ratio.', 'c2', 'core', topic='Types of ratios'),
        M('m3', 'The sub-triplicate ratio of 27 : 125 is:', ['3 : 5', '9 : 25', '729 : 15625', '√27 : √125'], 0,
          'Sub-triplicate means take the cube root of each term: ∛27 : ∛125 = 3 : 5. The trap is 9 : 25, which squares the correct answer instead of stopping at the cube roots; √27 : √125 is the sub-duplicate ratio, and 729 : 15625 squares the terms instead of reducing them. In practice: an analyst working back from volume to length uses this — if two similar storage tanks hold volumes in the ratio 27 : 125, their heights are in the ratio 3 : 5.', 'c2', 'core', topic='Types of ratios'),
        M('m4', 'The inverse ratio of 11 : 15 is:', ['15 : 11', '121 : 225', '11 : 15', '1 : 15'], 0, 'The inverse (reciprocal) ratio of a : b is b : a, because 1/11 : 1/15 becomes 15 : 11 when both are multiplied by 165. The tempting slip is to leave 11 : 15 unchanged or to square it into 121 : 225, which is the duplicate ratio. In practice: if two machines do the same job in 11 hours and 15 hours, their rates of work are in the inverse ratio 15 : 11 — a CA allocating machine-hour costs uses exactly this.', 'c2', 'core', topic='Types of ratios'),
        M('m5', 'Which pair of quantities can NOT form a ratio?', ['8 kg and 5 metres', '₹40 and ₹65', '20 minutes and 2 hours', '3 litres and 750 ml'], 0,
          'A ratio compares two quantities of the same kind, expressed in the same unit, so kilograms cannot be compared with metres. The tempting wrong choices — minutes against hours, or litres against millilitres — look mismatched but are the same kind of quantity; convert to a common unit (20 : 120, 3000 : 750) and a valid ratio appears. In practice: an auditor comparing stock in kg with shelf length in metres would get a meaningless figure, so cost ratios are always built from like quantities.', 'c1', 'core', topic='Ratio — meaning and basic rules'),
        M('m6', 'The ratio of 45 minutes to 2 hours is:', ['3 : 8', '45 : 2', '8 : 3', '9 : 4'], 0,
          'First bring both quantities to the same unit: 2 hours = 120 minutes, so the ratio is 45 : 120 = 3 : 8 after dividing by 15. The trap is 45 : 2, which compares minutes with hours and ignores units altogether; 8 : 3 reverses the order asked for. In practice: a cost accountant computing idle time as a share of a shift, say 45 minutes lost in a 2-hour batch, must convert to one unit first or the efficiency report is wrong.', 'c1', 'core', topic='Ratio — meaning and basic rules'),
        M('m7', 'Two numbers are in the ratio 3 : 5. If 9 is added to each, the ratio becomes 3 : 4. The larger number is:', ['15', '9', '25', '20'], 0,
          "Let the numbers be 3k and 5k. Then (3k + 9)/(5k + 9) = 3/4, so 12k + 36 = 15k + 27, giving k = 3. The numbers are 9 and 15, and the larger is 15. The trap is picking 9, which is the smaller number; check: 18 : 24 = 3 : 4. In practice: the same set-up solves questions like 'two partners add equal fresh capital and their capital ratio changes' — a routine adjustment in partnership accounts.", 'c1', 'moderate', '5*(4*9-3*9)/(15-12)', topic='Ratio — meaning and basic rules'),
        M('m8', 'Which ratio is the greatest: 5 : 7, 7 : 10, 3 : 4, 2 : 3?', ['3 : 4', '5 : 7', '7 : 10', '2 : 3'], 0,
          "Convert each ratio to a decimal to compare: 5 : 7 ≈ 0.714, 7 : 10 = 0.700, 3 : 4 = 0.750 and 2 : 3 ≈ 0.667, so 3 : 4 is the greatest. The trap is 5 : 7, because its terms look larger — but a ratio's size depends on the quotient, not the size of the numbers. In practice: an analyst comparing current ratios of four companies ranks them by the quotient, never by the absolute rupee figures behind them.", 'c1', 'core', topic='Ratio — meaning and basic rules'),
        M('m9', '₹7,800 is divided among P, Q and R in the ratio 1/2 : 1/3 : 1/4. R gets:', ['₹1,800', '₹2,400', '₹3,600', '₹1,950'], 0,
          "Clear the fractions with their LCM 12: 1/2 : 1/3 : 1/4 = 6 : 4 : 3, total 13 parts. R gets 7,800 × 3/13 = ₹1,800. The trap is ₹3,600, which is P's share (7,800 × 6/13) — always check which person the question asks about. In practice: partnership deeds sometimes state shares as fractions like 'one-half, one-third, one-fourth' that do not total one, and the accountant converts them to a whole-number ratio before dividing profit.", 'c1', 'moderate', '7800*3/13', topic='Ratio — meaning and basic rules'),
        M('m10', 'The fourth proportional to 4, 9 and 12 is:', ['27', '16', '36', '5.33'], 0, "The fourth proportional x satisfies 4 : 9 = 12 : x, so 4x = 9 × 12 and x = 108/4 = 27. The trap is 5.33, which comes from setting up 9 : 4 = 12 : x (terms in the wrong order); 36 simply multiplies 9 by 4. In practice: this is the 'rule of three' used daily — if 4 kg of raw material makes 9 units, a production planner finds how many units 12 kg will make the same way.", 'c3', 'core', '9*12/4', topic='Proportion and proportionals'),
        M('m11', 'The third proportional to 6 and 18 is:', ['54', '36', '12', '108'], 0, 'The third proportional to a and b is the x for which a : b = b : x, so x = b²/a = 18²/6 = 324/6 = 54. The trap is 12, the difference 18 − 6, which treats the pattern as additive instead of a ratio; 108 doubles the right answer. In practice: if sales grew from ₹6 crore to ₹18 crore and the business keeps the same growth ratio, the next figure is the third proportional — the basis of a simple constant-ratio projection.', 'c3', 'core', '18*18/6', topic='Proportion and proportionals'),
        M('m12', 'The mean proportional between 12 and 75 is:', ['30', '43.5', '900', '36'], 0,
          'The mean proportional between a and c is √(ac) = √(12 × 75) = √900 = 30; check 12 : 30 = 30 : 75. The trap is 43.5, which is the arithmetic mean (12 + 75)/2 — a different idea that adds instead of multiplying; 900 forgets the square root. In practice: when a value grows from 12 to 75 over two equal periods at a constant rate, the middle-period figure is the mean proportional, which is how analysts interpolate compounded figures.', 'c3', 'core', '(12*75)**0.5', topic='Proportion and proportionals'),
        M('m13', 'If a : b = 2 : 3 and b : c = 4 : 5, then a : b : c is:', ['8 : 12 : 15', '2 : 3 : 5', '2 : 12 : 5', '8 : 3 : 5'], 0,
          "Make the common term b equal. b is 3 in the first ratio and 4 in the second, so use 12: a : b = 8 : 12 and b : c = 12 : 15, giving a : b : c = 8 : 12 : 15. The trap is 2 : 3 : 5, got by simply joining the two ratios without equalising b. In practice: when an incoming partner's share is fixed relative to one existing partner, the accountant builds the new three-way profit-sharing ratio exactly this way.", 'c1', 'moderate', topic='Ratio — meaning and basic rules'),
        M('m14', 'If (a + b)/(a − b) = 9/5, then a : b is:', ['7 : 2', '9 : 5', '2 : 7', '14 : 5'], 0,
          'By componendo and dividendo, if (a + b)/(a − b) = 9/5 then a/b = (9 + 5)/(9 − 5) = 14/4 = 7/2, so a : b = 7 : 2. The trap is 9 : 5, which reads the given ratio as if it were a : b; 14 : 5 does only half the step. In practice: componendo and dividendo saves several lines of algebra in exam-pressure MCQs, and the same idea lets an analyst recover two figures from their sum-to-difference ratio.', 'c4', 'moderate', topic='Properties of proportion'),
        M('m15', 'Given p/q = r/s, the statement (p + q)/q = (r + s)/s follows by:', ['Componendo', 'Dividendo', 'Alternendo', 'Invertendo'], 0,
          "Componendo adds the consequent to the antecedent on each side: from p/q = r/s we get (p + q)/q = (r + s)/s. The trap is dividendo, which subtracts the consequent, giving (p − q)/q = (r − s)/s; alternendo and invertendo rearrange terms but add nothing. In practice: when an accountant knows two ratios are equal, componendo lets them jump straight to 'total : part', for example from cost : profit to sales : profit.", 'c4', 'core', topic='Properties of proportion'),
        M('m16', 'Given p/q = r/s, the statement p/r = q/s follows by:', ['Alternendo', 'Invertendo', 'Addendo', 'Subtrahendo'], 0,
          "Alternendo interchanges the means: from p : q = r : s we get p : r = q : s, which is exactly the statement given. The trap is invertendo, which flips both ratios to q : p = s : r rather than swapping the middle terms; addendo and subtrahendo combine terms instead. In practice: if two branches have sales in the same ratio as their costs, alternendo shows each branch's sales-to-cost ratio is the same — a quick consistency check in branch analysis.", 'c4', 'core', topic='Properties of proportion'),
        M('m17', 'The value of (64)^(2/3) × (32)^(−2/5) is:', ['4', '16', '0.25', '64'], 0,
          "Work each factor separately: 64^(2/3) = (∛64)² = 4² = 16, and 32^(−2/5) = 1/(⁵√32)² = 1/2² = 1/4. The product is 16 × 1/4 = 4. The trap is 16, which forgets the second factor's negative index entirely, while 0.25 stops after the second factor. In practice: fractional and negative indices appear whenever an accountant converts an annual rate to a monthly or quarterly equivalent, for example (1.12)^(1/12).", 'c5', 'moderate', '64**(2/3)*32**(-2/5)', topic='Indices (powers) and their laws'),
        M('m18', 'If 3^(x + 2) = 243, then x is:', ['3', '5', '7', '2'], 0, 'Write 243 as a power of 3: 243 = 3⁵. With equal bases, the indices must be equal, so x + 2 = 5 and x = 3. The trap is 5, which is the full index and forgets to subtract the 2 already in the power. In practice: equating powers like this is how one finds the number of years needed for an investment to reach a target when the growth factor is a neat power.', 'c5', 'core', topic='Indices (powers) and their laws'),
        M('m19', 'If 2^x = 3^y = 6^z, then z equals:', ['xy/(x + y)', 'x + y', '(x + y)/xy', 'xy'], 0,
          "Let 2ˣ = 3ʸ = 6ᶻ = k. Then 2 = k^(1/x), 3 = k^(1/y) and 6 = k^(1/z). Since 6 = 2 × 3, k^(1/z) = k^(1/x + 1/y), so 1/z = 1/x + 1/y and z = xy/(x + y). The trap is (x + y)/xy, which is 1/z — the student stops one step early. In practice: this 'set everything equal to k' technique is the standard way to handle growth comparisons between rates in examination algebra.", 'c5', 'hard', topic='Indices (powers) and their laws'),
        M('m20', 'The value of log₂ 128 is:', ['7', '6', '64', '8'], 0, 'By definition, log₂ 128 is the power to which 2 must be raised to get 128. Since 2⁷ = 128, log₂ 128 = 7. The trap is 64, which halves 128 instead of finding the index; 6 and 8 come from miscounting the doublings (2⁶ = 64, 2⁸ = 256). In practice: base-2 logs tell you how many doublings are needed — for example how many periods for a quantity growing 100% each period to reach a target.', 'c6', 'core', topic='Logarithm — definition'),
        M('m21', 'The value of log₀.₅ 16 (base 0.5) is:', ['−4', '4', '1/4', '−1/4'], 0, 'We need the power of 0.5 that gives 16. Since 0.5 = 2⁻¹, (0.5)^(−4) = 2⁴ = 16, so log₀.₅ 16 = −4. The trap is +4, which forgets that a base below 1 shrinks numbers when raised to positive powers ((0.5)⁴ = 1/16). In practice: bases below 1 behave like depreciation factors — an asset losing half its value each year falls, not rises, as the power increases.', 'c6', 'moderate', topic='Logarithm — definition'),
        M('m22', 'Given log 2 = 0.3010 and log 3 = 0.4771, log 18 is:', ['1.2552', '0.7781', '1.4313', '0.1436'], 0,
          'Factorise first: 18 = 2 × 3², so log 18 = log 2 + 2 log 3 = 0.3010 + 0.9542 = 1.2552. The trap is 0.1436, which multiplies log 2 by log 3 — but the log of a product is the sum of the logs; 0.7781 is log 6, which uses 3 only once. In practice: before calculators, actuaries and bankers computed compound-interest factors from log tables using exactly these product and power laws.', 'c7', 'core', '0.3010+2*0.4771', topic='Laws of logarithms and change of base'),
        M('m23', 'Given log 2 = 0.3010, the value of log 5 is:', ['0.6990', '0.1505', '1.3010', '0.3010'], 0,
          'Write 5 as 10/2: log 5 = log 10 − log 2 = 1 − 0.3010 = 0.6990, using the quotient law and log 10 = 1. The trap is 0.1505, which halves log 2 as if log 5 = log 10/2 could be split by dividing the log; 1.3010 adds instead of subtracting. In practice: log 2 and log 3 are often the only values given in ICAI papers, and expressing 5 as 10/2 is the standard trick for building other logs.', 'c7', 'core', '1-0.3010', topic='Laws of logarithms and change of base'),
        M('m24', 'log₃ 5 × log₂₅ 27 equals:', ['1.5', '0.6667', '3', '2'], 0,
          'Change everything to a common base: log₃ 5 = log 5/log 3 and log₂₅ 27 = log 27/log 25 = 3 log 3/(2 log 5). Multiplying, log 5 and log 3 cancel, leaving 3/2 = 1.5. The trap is 0.6667, which inverts the fraction by writing log 25/log 27. In practice: change of base is how a spreadsheet user computes a log to any base using only the LOG10 or LN function, for example when working out doubling periods.', 'c7', 'hard', '3/2', topic='Laws of logarithms and change of base'),
        M('m25', 'If log₂ x + log₂ (x − 2) = 3, then x is:', ['4', '−2', '8', '6'], 0,
          'Combine the logs: log₂ [x(x − 2)] = 3, so x(x − 2) = 2³ = 8, i.e. x² − 2x − 8 = 0, giving x = 4 or x = −2. A logarithm is defined only for positive arguments, so x = −2 is rejected and x = 4. The trap is −2: it solves the quadratic but fails the domain check. In practice: rejecting answers that make no economic sense, like negative prices or years, is a habit every analyst needs.', 'c7', 'hard', topic='Laws of logarithms and change of base'),
        M('m26', 'The characteristic of log 0.000732 is:', ['−4 (written 4̄)', '−3 (written 3̄)', '3', '4'], 0,
          'For a number less than 1, the characteristic is negative and equals one more than the number of zeros immediately after the decimal point. 0.000732 has three such zeros, so the characteristic is −(3 + 1) = −4, written 4̄. The trap is −3 (3̄), which counts the zeros but forgets to add one. In practice: reading log tables for small decimals, such as tiny interest rates per day, depends on getting this characteristic right.', 'c8', 'moderate', topic='Characteristic, mantissa and antilogarithm'),
        M('m27', 'Given log 2 = 0.3010, the number of digits in 2^40 is:', ['13', '12', '40', '14'], 0,
          'log 2⁴⁰ = 40 × 0.3010 = 12.04. The characteristic is 12, and a number whose log has characteristic n has n + 1 digits, so 2⁴⁰ has 13 digits. The trap is 12, which takes the characteristic itself as the number of digits. In practice: this digit-counting rule is a quick sanity check on the size of huge compounded figures, such as 40 periods of doubling, before trusting a spreadsheet result.', 'c8', 'hard', '12+1', topic='Characteristic, mantissa and antilogarithm'),
        M('m28', 'The value of 7^(log₇ 9) is:', ['9', '7', '63', '1'], 0, "Logarithm and exponent with the same base undo each other: a^(logₐ x) = x. So 7^(log₇ 9) = 9. The trap is 63 (7 × 9), which treats the expression as a product, or 7, which assumes the base survives. Think of it as: log₇ 9 is 'the power of 7 that gives 9', and raising 7 to that power gives 9. In practice: this inverse property is why taking logs and then antilogs returns the original figure in any log-based calculation.", 'c7', 'core', topic='Laws of logarithms and change of base'),
        M('m29', 'log 0.001 (base 10) is:', ['−3', '3', '−2', '0.001'], 0, '0.001 = 1/1000 = 10⁻³, so log 0.001 to base 10 is −3. The trap is +3, which counts the places correctly but forgets that numbers between 0 and 1 have negative logarithms; −2 miscounts the places. In practice: decibel and pH-style scales, and the log returns analysts use for stock prices, all rely on logs being negative for values below one.', 'c6', 'core', topic='Logarithm — definition'),
        M('m30', 'Monthly salaries of two clerks are in the ratio 4 : 5 and their expenses in the ratio 3 : 4. If each saves ₹6,000, the first clerk’s salary is:', ['₹24,000', '₹30,000', '₹18,000', '₹20,000'], 0,
          "Let salaries be 4k and 5k, expenses 3m and 4m. Savings give 4k − 3m = 6,000 and 5k − 4m = 6,000. Subtracting, k = m, so k = 6,000 and the first salary is 4 × 6,000 = ₹24,000. The trap is ₹30,000, which is the second clerk's salary. In practice: HR and payroll analysts use the same income-expense-saving framework when comparing take-home and spending patterns across employee grades.", 'c1', 'hard', '4*6000', topic='Ratio — meaning and basic rules'),
    ]
    assert abs(64 ** (2 / 3) * 32 ** (-0.4) - 4) < 1e-9 and abs(math.log(5, 3) * math.log(27, 25) - 1.5) < 1e-9
    assert math.log(16, 0.5) + 4 < 1e-9 and len(str(2 ** 40)) == 13
    # m30 check: k and m
    assert 4 * 6000 - 3 * 6000 == 6000 and 5 * 6000 - 4 * 6000 == 6000

    # ---------------- Case set ----------------
    cc = Checks()
    cap_a = cc.add('300000*12', 'Ishita capital-months')
    cap_b = cc.add('400000*6+600000*6', 'Ravi capital-months')
    cap_c = cc.add('500000*8', 'Manav capital-months')
    cc.add('3600000/400000', 'Ishita ratio term (÷4,00,000)')
    cc.add('6000000/400000', 'Ravi ratio term')
    cc.add('4000000/400000', 'Manav ratio term')
    profit = 340000
    sh_r = cc.add('340000*15/34', 'Ravi’s profit share')
    sh_i = cc.add('340000*9/34', 'Ishita’s profit share')
    sh_m = cc.add('340000*10/34', 'Manav’s profit share')
    case = {
        'id': 'k1', 'title': 'Sharing profit in the ratio of capital and time', 'difficulty': 'hard',
        'case': ('Ishita, Ravi and Manav run a coaching centre with no partnership deed on profit sharing other than "in proportion to capital employed and the time for which it was employed". '
                 'For 2026-27: Ishita kept ₹3,00,000 in the business for all 12 months. Ravi brought ₹4,00,000 on 1 April and added ₹2,00,000 more on 1 October. Manav brought ₹5,00,000 on 1 August. '
                 f'The profit for the year is ₹{inr(profit)}.'),
        'given': [table(['Partner', 'Capital × months', 'Capital-months (₹)'], [['Ishita', '3,00,000 × 12', cap_a], ['Ravi', '4,00,000 × 6 + 6,00,000 × 6', cap_b], ['Manav', '5,00,000 × 8', cap_c], ['Total', '', cap_a + cap_b + cap_c]], num=[2], total=True)],
        'mcqs': [
            M('k1a', 'The profit-sharing ratio Ishita : Ravi : Manav is:', ['9 : 15 : 10', '3 : 6 : 5', '3 : 4 : 5', '9 : 12 : 10'], 0,
              'Profit is shared in the ratio of capital × time. Ishita: 3 lakh × 12 = 36 lakh; Ravi: 4 lakh × 6 + 6 lakh × 6 = 60 lakh; Manav: 5 lakh × 8 = 40 lakh. 36 : 60 : 40 = 9 : 15 : 10. The trap is 3 : 4 : 5 or 3 : 6 : 5, which use opening or closing capital and ignore the months. In practice: when a partnership deed links profit to capital employed, accountants use these product (capital-month) figures.', 'c2', 'hard', topic='Types of ratios'),
            M('k1b', 'Ravi’s share of profit is:', [R(sh_r), R(120000), R(136000), R(100000)], 0,
              "Total ratio terms are 9 + 15 + 10 = 34, and Ravi's term is 15. His share = 3,40,000 × 15/34 = ₹1,50,000. The trap is ₹1,20,000, which would follow from a ratio that ignores Ravi's extra ₹2,00,000 brought in on 1 October. Check: shares of ₹90,000 + ₹1,50,000 + ₹1,00,000 total ₹3,40,000. In practice: the partners' profit and loss appropriation account shows these shares, and a total check catches arithmetic slips.", 'c2', 'moderate', '340000*15/34', topic='Types of ratios'),
            M('k1c', 'Manav’s share of profit is:', [R(sh_m), R(sh_i), R(113333), R(121429)], 0,
              "Manav's ratio term is 10 out of 34, so his share = 3,40,000 × 10/34 = ₹1,00,000. The trap is ₹90,000, which is Ishita's share (9/34); another trap is to give Manav credit for 12 months even though he joined on 1 August and was in only 8 months. In practice: late-joining partners in Indian professional firms commonly get time-weighted shares in the first year, computed exactly this way.", 'c2', 'moderate', '340000*10/34', topic='Types of ratios'),
            M('k1d', 'The ratio used here (capital ratio combined with time ratio by multiplying term by term) is an example of a:', ['Compound ratio', 'Duplicate ratio', 'Inverse ratio', 'Continued proportion'], 0,
              'Combining the capital ratio with the time ratio by multiplying corresponding terms (capital × months) is the definition of a compound ratio. The trap is continued proportion, which is a chain like a : b = b : c — nothing here requires that; duplicate ratio squares one ratio, and inverse ratio flips it. In practice: compound ratios also appear when rent is shared by floor area × months occupied, or wages by workers × days.', 'c2', 'core', topic='Types of ratios'),
        ]}

    unit = {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch01', 'n': 1, 'title': 'Ratio and Proportion, Indices, Logarithms',
        'outcomes': ['Write, simplify and compare ratios, and work with inverse, compound, duplicate, triplicate, sub-duplicate, sub-triplicate and continued ratios.',
                     'Use proportion — fourth, third and mean proportional, continued proportion — and the properties invertendo, alternendo, componendo, dividendo, componendo-dividendo, addendo and subtrahendo.',
                     'Apply the laws of indices (zero, negative and fractional powers) to simplify expressions and solve exponential equations.',
                     'Use the definition and laws of logarithms, change of base, characteristic, mantissa and antilogarithm to evaluate expressions and count digits.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 75, 'practice': 90}, 'prereq': [],
                 'exam_tip': 'This chapter gives several quick marks in the 100-question paper. Most questions are solved in under a minute by substituting the options back — but a wrong guess costs ¼ mark, so substitute, do not guess.'},
        'concepts': [
            {'id': 'c1', 'title': 'Ratio — meaning and basic rules',
             'body': ['A ratio compares two quantities of the same kind by dividing one by the other. For quantities a and b it is written a : b (read "a is to b"). The first term a is the antecedent and the second term b is the consequent.',
                      'Rules: both quantities must be in the same unit before comparing (convert hours to minutes, litres to ml); the ratio itself has no unit; scaling both terms up or down by one common non-zero factor leaves the ratio unchanged, so we normally reduce to lowest terms; and order matters — 2 : 5 and 5 : 2 are different.',
                      'To compare two ratios, turn them into fractions and cross-multiply (or convert to decimals). a : b is a ratio of greater inequality if a > b, of lesser inequality if a < b, and of equality if a = b.',
                      'Dividing an amount in a given ratio: add the terms, find the value of one part, then multiply. If the ratio has fractions, multiply every term by the LCM of the denominators first.'],
             'analogy': 'A ratio is a recipe: 2 cups of rice to 3 cups of water stays the same recipe whether you cook for two people or twenty.',
             'work': 'Partners share profit in an agreed ratio; costs are apportioned to departments in the ratio of floor area or headcount; analysts compare companies through ratios. Each of these starts with "same unit, same kind, lowest terms".'},
            {'id': 'c2', 'title': 'Types of ratios',
             'body': ['Inverse (reciprocal) ratio of a : b is b : a (that is, 1/a : 1/b). Compound ratio of a : b and c : d is ac : bd — multiply antecedents together and consequents together.',
                      'Duplicate ratio of a : b is a² : b²; triplicate ratio is a³ : b³. Sub-duplicate ratio is √a : √b; sub-triplicate ratio is ∛a : ∛b.',
                      'Commensurable quantities have a ratio that can be expressed as a ratio of two integers (e.g. 6 : 9 = 2 : 3). If not — for example √2 : 3 — they are incommensurable.',
                      'A continued ratio compares three or more quantities of the same kind, e.g. a : b : c. To combine a : b and b : c, make the common term b equal in both and then write the three terms together.'],
             'analogy': 'Duplicate is "square it", triplicate is "cube it"; add "sub-" and you go the other way — take the root.',
             'work': 'Profit sharing "in the ratio of capital and time" is a compound ratio of capital and months — a common situation in partnership accounts and in Paper 1.'},
            {'id': 'c3', 'title': 'Proportion and proportionals',
             'body': ['Four quantities p, q, r, s are in proportion when p : q = r : s (sometimes written p : q :: r : s). The outer terms p and s are the extremes, the inner terms q and r are the means, and extremes multiplied together equal means multiplied together: ps = qr. Here s is called the fourth proportional to p, q and r.',
                      'Three quantities a, b, c are in continued proportion when a : b = b : c. Then b² = ac; b = √(ac) is the mean proportional between a and c, and c = b²/a is the third proportional to a and b.',
                      'More generally a, b, c, d, … are in continued proportion when each term bears the same ratio to the next one.',
                      'Unlike a ratio, the four terms of a proportion need not all be of the same kind — only each ratio must compare like with like (e.g. 3 kg : 5 kg = ₹36 : ₹60).'],
             'analogy': 'In a proportion the two sides of the "=" are two photographs of the same object at different zoom levels.',
             'work': 'Unitary-method costing, scaling a budget to a new activity level, or estimating a missing figure from a known relationship are all fourth-proportional problems.'},
            {'id': 'c4', 'title': 'Properties of proportion',
             'body': ['Start from a proportion written as fractions, a/b = c/d. Each property below is a new, equally true proportion obtained from it (see the table).',
                      'Addendo: if a/b = c/d = e/f = …, then each ratio also equals (a + c + e + …)/(b + d + f + …). Subtrahendo: each ratio also equals (a − c − e − …)/(b − d − f − …).',
                      'Useful shortcut ("k-method"): when several ratios are equal, put each equal to k, write a = bk, c = dk and so on, and substitute.',
                      'Componendo and dividendo works in reverse too: if (x + y)/(x − y) = p/q, then x/y = (p + q)/(p − q). It is the fastest way to remove square roots in equations like (√A + √B)/(√A − √B) = p/q.'],
             'blocks': [table(['Property', 'What you do', 'Result'], [
                 ['Invertendo', 'Flip both fractions', 'b/a = d/c'],
                 ['Alternendo', 'Swap the two middle terms', 'a/c = b/d'],
                 ['Componendo', 'Add denominator to numerator', '(a+b)/b = (c+d)/d'],
                 ['Dividendo', 'Subtract denominator from numerator', '(a−b)/b = (c−d)/d'],
                 ['Componendo and dividendo', 'Sum over difference, both sides', '(a+b)/(a−b) = (c+d)/(c−d)'],
             ], title='Properties when a/b = c/d')],
             'analogy': 'These properties are legal moves in a game: each one changes the look of the proportion without breaking the equality.',
             'work': 'In MCQs these properties turn a long algebraic simplification into a two-line step — speed that matters when you have about 72 seconds per question.'},
            {'id': 'c5', 'title': 'Indices (powers) and their laws',
             'body': ['aⁿ means a multiplied by itself n times; a is the base and n is the index (power or exponent).',
                      'Laws (a, b non-zero; m, n rational): aᵐ × aⁿ = aᵐ⁺ⁿ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; (ab)ⁿ = aⁿbⁿ; (a/b)ⁿ = aⁿ/bⁿ.',
                      'Special indices: a⁰ = 1; a⁻ⁿ = 1/aⁿ; a^(1/n) is the n-th root of a; a^(p/q) = (q-th root of a)^p.',
                      'Equal bases: if aˣ = aʸ (a > 0, a ≠ 1), then x = y. Equal powers: if xⁿ = yⁿ with x, y positive, then x = y. Exponential equations are solved by writing both sides with the same base.'],
             'analogy': 'An index is a shorthand counter: instead of writing "×2" ten times you write 2¹⁰ — and the laws are simply ways of adding up those counters.',
             'work': 'Compound growth (1 + r)ⁿ, depreciation (1 − r)ⁿ and discounting (1 + r)⁻ⁿ in Chapter 4 are all index expressions; a CA evaluates them daily in valuation and loan work.'},
            {'id': 'c6', 'title': 'Logarithm — definition',
             'body': ['If aˣ = N, where a > 0 and a ≠ 1, then x is the logarithm of N to the base a, written x = logₐ N. The two statements aˣ = N and logₐ N = x say the same thing in two forms.',
                      'Only positive numbers have real logarithms, and the base must be positive and not equal to 1.',
                      'logₐ 1 = 0 (because a⁰ = 1) and logₐ a = 1 (because a¹ = a).',
                      'Logarithms to base 10 are common logarithms (if no base is written, take base 10). Logarithms to base e (about 2.718) are natural logarithms, written ln.'],
             'analogy': 'A logarithm answers the question "how many times must I multiply the base to reach this number?" — log₂ 32 = 5 because you double 1 five times to reach 32.',
             'work': 'Whenever the unknown sits in the power — "how many years until this deposit doubles?" — a logarithm brings it down so it can be solved.'},
            {'id': 'c7', 'title': 'Laws of logarithms and change of base',
             'body': ['Product: logₐ (mn) = logₐ m + logₐ n. Quotient: logₐ (m/n) = logₐ m − logₐ n. Power: logₐ (mⁿ) = n logₐ m.',
                      'Change of base: logₐ m = log_b m ÷ log_b a (any convenient base b, usually 10). Consequences: logₐ b × log_b a = 1, so log_b a = 1/logₐ b; and log_b a × log_c b = log_c a (the chain rule).',
                      'Inverse property: a^(logₐ x) = x.',
                      'Traps: log (m + n) is NOT log m + log n; log m × log n is NOT log (mn); (log m)/(log n) is NOT log (m/n).'],
             'analogy': 'Logs turn multiplication into addition — like converting a hard climb into a flat walk. Change of base is a currency converter between log "currencies".',
             'work': 'Before calculators, logs were how actuaries and accountants multiplied large numbers. Today the same laws appear in growth and period calculations in finance.'},
            {'id': 'c8', 'title': 'Characteristic, mantissa and antilogarithm',
             'body': ['A common logarithm has an integer part (the characteristic) and a decimal part (the mantissa). The mantissa is always kept positive and depends only on the digits of the number, not on where the decimal point is.',
                      'For a number greater than 1, the characteristic is one less than the number of digits before the decimal point (log 4,812 has characteristic 3). For a number less than 1, the characteristic is negative and equal to one more than the number of zeros immediately after the decimal point (log 0.0048 has characteristic −3, written 3̄).',
                      'Bar notation: 2̄.6021 means −2 + 0.6021. A negative logarithm such as −1.3468 is rewritten as −2 + 0.6532 = 2̄.6532 before using tables.',
                      'Antilogarithm: if log N = x then N = antilog x = 10ˣ. The characteristic tells where to place the decimal point in the antilog. Number of digits in a large power: digits = characteristic + 1.'],
             'analogy': 'The mantissa is the "face" of the number and the characteristic is its "address" — the same face (digits 48) can live at 4,800 or 0.048.',
             'work': 'Counting digits of large powers and placing decimal points from log tables are classic ICAI MCQs; the same skill helps sanity-check the size of a compounded figure.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Dividing a sum in a ratio of fractions', 'difficulty': 'core', 'minutes': 4,
             'q': '₹3,90,000 is to be divided among Asha, Bhanu and Chetan in the ratio 1/2 : 1/3 : 1/4. Find each share.',
             'solution': [p('Step 1 — clear the fractions: LCM of 2, 3 and 4 is 12. Multiply each term by 12: 6 : 4 : 3.'),
                          p(f'Step 2 — total parts = 6 + 4 + 3 = {tot1}; value of one part = 3,90,000 ÷ 13 = ₹{inr(unit1)}.'), share_tbl,
                          note('Check: shares add back to ₹3,90,000. A common slip is to divide in the ratio 2 : 3 : 4 (the denominators) — which reverses who gets most.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Finding numbers when a ratio changes', 'difficulty': 'core', 'minutes': 4,
             'q': 'Two numbers are in the ratio 5 : 7. When 6 is added to each, the ratio becomes 3 : 4. Find the numbers.',
             'solution': [p('Let the numbers be 5k and 7k. Then (5k + 6)/(7k + 6) = 3/4.'),
                          p(f'Cross-multiply: 4(5k + 6) = 3(7k + 6) → 20k + 24 = 21k + 18 → k = {k2}.'),
                          p(f'Numbers: 5 × 6 = {n2a} and 7 × 6 = {n2b}. Check: 36 : 48 = 3 : 4. ✔')],
             'checks': c2},
            {'id': 'i3', 'title': 'Fourth, third and mean proportional', 'difficulty': 'core', 'minutes': 4,
             'q': 'Find (a) the fourth proportional to 3, 8 and 12; (b) the third proportional to 4 and 10; (c) the mean proportional between 9 and 64.',
             'solution': [p(f'(a) 3 : 8 = 12 : x → 3x = 96 → x = {fp}.'),
                          p(f'(b) 4 : 10 = 10 : x → x = 10²/4 = {tp}.'),
                          p(f'(c) Mean proportional = √(9 × 64) = √576 = {mp}.'),
                          note('Keep the order exactly as given: "third proportional to 4 and 10" is 25, but to 10 and 4 it would be 1.6.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Componendo and dividendo in action', 'difficulty': 'moderate', 'minutes': 5,
             'q': '(a) If (x + y)/(x − y) = 7/3, find x : y. (b) Solve (√(x + 4) + √(x − 4)) / (√(x + 4) − √(x − 4)) = 2.',
             'solution': [p('(a) Apply componendo and dividendo: x/y = (7 + 3)/(7 − 3) = 10/4, so x : y = 5 : 2.'),
                          p('(b) Apply componendo and dividendo to the left side: [2√(x + 4)] / [2√(x − 4)] = (2 + 1)/(2 − 1) = 3.'),
                          p('So √(x + 4)/√(x − 4) = 3. Square both sides: (x + 4)/(x − 4) = 9 → x + 4 = 9x − 36 → 8x = 40.'),
                          p(f'x = {x4}. Check: (√9 + √1)/(√9 − √1) = 4/2 = 2. ✔')],
             'checks': c4},
            {'id': 'i5', 'title': 'Laws of indices', 'difficulty': 'moderate', 'minutes': 5,
             'q': '(a) Evaluate 27^(2/3) × 16^(−3/4) ÷ 81^(−1/4). (b) Solve 2^(x + 3) = 32^(x − 1).',
             'solution': [p('(a) 27^(2/3) = (3³)^(2/3) = 3² = 9. 16^(−3/4) = (2⁴)^(−3/4) = 2⁻³ = 1/8. 81^(−1/4) = (3⁴)^(−1/4) = 1/3.'),
                          p(f'Value = 9 × 1/8 ÷ 1/3 = 9 × 1/8 × 3 = 27/8 = {num(v5)}.'),
                          p('(b) Write 32 as 2⁵: 2^(x + 3) = 2^(5x − 5). Equal bases → x + 3 = 5x − 5 → 4x = 8.'),
                          p(f'x = {x5}. Check: 2⁵ = 32 and 32¹ = 32. ✔')],
             'checks': c5},
            {'id': 'i6', 'title': 'Using given logarithms; digits in a large power', 'difficulty': 'hard', 'minutes': 6,
             'q': 'Given log 2 = 0.3010 and log 3 = 0.4771, find (a) log 72, (b) log 0.45 in bar form, (c) the number of digits in 2⁵⁰.',
             'solution': [p(f'(a) 72 = 2³ × 3², so log 72 = 3(0.3010) + 2(0.4771) = 0.9030 + 0.9542 = {num(l72)}.'),
                          p(f'(b) 0.45 = 9/20, so log 0.45 = 2 log 3 − (log 2 + log 10) = 0.9542 − 1.3010 = {num(l045)}.'),
                          p('Make the mantissa positive: −0.3468 = −1 + 0.6532 = 1̄.6532 (characteristic −1, because there is no zero right after the decimal point in 0.45).'),
                          p(f'(c) log 2⁵⁰ = 50 × 0.3010 = {num(d6)}. Characteristic 15 → the number has 15 + 1 = 16 digits.')],
             'checks': c6},
            {'id': 'i7', 'title': 'Change of base inside an equation', 'difficulty': 'hard', 'minutes': 5,
             'q': 'Solve log₂ x + log₄ x + log₁₆ x = 7.',
             'solution': [p('Change every term to base 2: log₄ x = log₂ x / log₂ 4 = (1/2) log₂ x; log₁₆ x = (1/4) log₂ x.'),
                          p('So (1 + 1/2 + 1/4) log₂ x = 7 → (7/4) log₂ x = 7.'),
                          p(f'log₂ x = {lx}, so x = 2⁴ = {x7}.'),
                          note('Check: log₂ 16 + log₄ 16 + log₁₆ 16 = 4 + 2 + 1 = 7. ✔')],
             'checks': c7},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Apportioning a common cost', 'role': 'Cost accountant in a manufacturing company',
             'situation': 'The factory rent of ₹9,60,000 a year must be shared by three departments. Floor areas are 2,400, 1,600 and 800 square feet.',
             'steps': ['Reduce the floor areas to the simplest ratio: 2,400 : 1,600 : 800 = 3 : 2 : 1.', 'Total parts = 6; one part = 9,60,000 ÷ 6 = ₹1,60,000.',
                       'Shares: ₹4,80,000, ₹3,20,000 and ₹1,60,000.', 'Document the basis (floor area) in the cost sheet so the allocation can be audited and repeated next year.'],
             'takeaway': 'Cost apportionment is ratio arithmetic plus a defensible basis.', 'think': 'If rent rises by 10% next year and areas stay the same, does the ratio change?',
             'answer': 'No. The ratio 3 : 2 : 1 depends only on the areas. Each share simply rises by 10%.',
             'checks': [{'expr': '960000*3/6', 'value': 480000, 'label': 'Department A'}, {'expr': '960000*2/6', 'value': 320000, 'label': 'Department B'}, {'expr': '960000/6', 'value': 160000, 'label': 'Department C'}]},
            {'id': 'j2', 'title': 'Admitting a partner — new ratio', 'role': 'CA advising a partnership firm',
             'situation': 'X and Y share profits 3 : 2. Z is admitted for a 1/5 share, which he takes from X and Y in their existing ratio.',
             'steps': ['Remaining share after Z = 1 − 1/5 = 4/5.', 'X gets 3/5 of 4/5 = 12/25; Y gets 2/5 of 4/5 = 8/25; Z gets 1/5 = 5/25.', 'New ratio X : Y : Z = 12 : 8 : 5.', 'Record the new ratio in the supplementary deed and update the profit-sharing schedule.'],
             'takeaway': 'Partnership ratio changes are ratio-of-ratio problems — keep fractions until the last step.', 'think': 'Check that 12 + 8 + 5 parts give Z exactly one-fifth.',
             'answer': 'Total = 25 parts; Z has 5 parts = 5/25 = 1/5. ✔'},
            {'id': 'j3', 'title': 'How long until sales grow five-fold?', 'role': 'Analyst in a CA firm preparing a business plan',
             'situation': 'A client expects sales to grow at 20% a year and wants to know when sales will be five times today’s level. Log tables give log 2 = 0.3010 and log 3 = 0.4771.',
             'steps': ['Set up (1.2)ⁿ = 5 and take logs: n log 1.2 = log 5.', f'log 1.2 = log 12 − 1 = 2(0.3010) + 0.4771 − 1 = {num(l12)}; log 5 = 1 − 0.3010 = {num(l5)}.',
                       f'n = {num(l5)} ÷ {num(l12)} ≈ {num(yrs, 2)} years — so sales cross five times in the 9th year.', 'State the assumption (constant 20% growth) clearly in the report.'],
             'takeaway': 'When the unknown is in the power, logarithms bring it down to a simple division.', 'think': 'Why is the answer "in the 9th year" and not "after 8 years"?',
             'answer': 'After 8 full years sales are 1.2⁸ ≈ 4.3 times; the five-fold mark is reached only part-way through the 9th year.', 'checks': cj},
        ],
        'mcqs': mcqs,
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'A : B = 2 : 3 and B : C = 4 : 5. Find A : B : C and divide ₹2,45,000 among A, B and C in that ratio. Show every step.',
             'model': [p('Make B common: B is 3 in the first ratio and 4 in the second. LCM = 12.'),
                       p('A : B = 2 : 3 = 8 : 12 (multiply by 4). B : C = 4 : 5 = 12 : 15 (multiply by 3).'),
                       p(f'So A : B : C = 8 : 12 : 15; total {q1sum} parts.'),
                       table(['Person', 'Ratio term', 'Share (₹)'], [['A', '8', q1a], ['B', '12', q1b], ['C', '15', q1cc], ['Total', '35', 245000]], num=[2], total=True)],
             'scheme': [{'id': 's1', 'pt': 'Makes the common term B equal (LCM 12)', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Correct continued ratio 8 : 12 : 15', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Shares ₹56,000, ₹84,000, ₹1,05,000', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Checks total = ₹2,45,000', 'm': 0.5, 'skill': 'presentation'}],
             'remarks': ['The commonest error is writing 2 : 3 : 5 by simply joining the ratios — B must be made equal first.', 'A one-line check that the shares total the given sum costs ten seconds and catches most slips.'],
             'mistakes': ['Joining the ratios directly as 2 : 3 : 5.', 'Multiplying only one term of a ratio when making B common.'],
             'tips': ['Write the LCM step explicitly — it earns the concept mark even if arithmetic later slips.', 'Present shares in a small table with a total row.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Given log 2 = 0.3010 and log 3 = 0.4771, find (a) log 24, (b) log 0.24 in bar notation, and (c) the number of digits in 3²⁰.',
             'model': [p(f'(a) 24 = 2³ × 3 → log 24 = 3(0.3010) + 0.4771 = {num(q2_l)}.'),
                       p(f'(b) 0.24 = 24/100 → log 0.24 = 1.3801 − 2 = {num(q2_r)} = −1 + 0.3801 = 1̄.3801.'),
                       p(f'(c) log 3²⁰ = 20 × 0.4771 = {num(q2_d)}. Characteristic 9, so 3²⁰ has 9 + 1 = 10 digits.')],
             'scheme': [{'id': 's1', 'pt': 'Factorises 24 and applies product/power laws', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'log 24 = 1.3801', 'm': 0.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'log 0.24 written with positive mantissa as 1̄.3801', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Digits = characteristic + 1 = 10', 'm': 1, 'skill': 'application'}],
             'remarks': ['Candidates often leave log 0.24 as −0.6199 and then cannot read the mantissa; the bar form is expected.', 'Digit counting is asked frequently — remember "characteristic + 1".'],
             'mistakes': ['Writing 1̄.3801 as −1.3801 (which is a different number).', 'Counting digits as the characteristic itself.'],
             'tips': ['For numbers below 1, find the log of the digits first, then subtract the power of 10.', 'State the rule used in each line in a few words.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
             'q': 'If (a + b) : (a − b) = 5 : 3, find the value of (3a² + 2b²) : (3a² − 2b²).',
             'model': [p('Componendo and dividendo on (a + b)/(a − b) = 5/3: a/b = (5 + 3)/(5 − 3) = 8/2 = 4, so a = 4b.'),
                       p('Substitute a = 4b: 3a² = 3 × 16b² = 48b².'),
                       p('(3a² + 2b²) : (3a² − 2b²) = (48b² + 2b²) : (48b² − 2b²) = 50 : 46 = 25 : 23.')],
             'scheme': [{'id': 's1', 'pt': 'Applies componendo and dividendo correctly', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'a : b = 4 : 1', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Substitutes and simplifies to 25 : 23', 'm': 1.5, 'skill': 'computation'}],
             'remarks': ['Many candidates expand (a + b)/(a − b) by cross-multiplying, which works but wastes time; C&D is the expected route.'],
             'mistakes': ['Writing a : b = 5 : 3 straight from the question.', 'Forgetting to square when substituting a = 4b.'],
             'tips': ['Reduce the final ratio to lowest terms — 50 : 46 is not the final answer.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Ratio a : b compares like quantities in the same unit; reduce to lowest terms; order matters.',
                        'Inverse b : a; compound ac : bd; duplicate a² : b²; triplicate a³ : b³; sub-duplicate √a : √b; sub-triplicate ∛a : ∛b.',
                        'Proportion p : q = r : s ⇔ ps = qr. Mean proportional √(ac); third proportional b²/a; fourth proportional bc/a.',
                        'Properties: invertendo, alternendo, componendo, dividendo, componendo-dividendo, addendo, subtrahendo.',
                        'Indices: add powers when multiplying, subtract when dividing, multiply for a power of a power; a⁰ = 1, a⁻ⁿ = 1/aⁿ, a^(1/n) = n-th root.',
                        'Logs: aˣ = N ⇔ logₐ N = x; product → sum, quotient → difference, power → multiple; change of base logₐ m = log m / log a.',
                        'Characteristic: digits − 1 (numbers ≥ 1); −(zeros after the point + 1) (numbers < 1). Mantissa always positive. Digits in N = characteristic + 1.'],
            'remember': ['logₐ 1 = 0, logₐ a = 1, a^(logₐ x) = x.', 'logₐ b × log_b a = 1.', 'C&D reverse: (x + y)/(x − y) = p/q ⇒ x/y = (p + q)/(p − q).'],
            'traps': ['log (m + n) ≠ log m + log n.', '1̄.3801 ≠ −1.3801.', 'Third proportional "to a and b" is b²/a — not a²/b.', 'Reject solutions that make a log argument zero or negative.'],
        },
        'quickref': [
            {'k': 'Compound ratio', 'v': 'a : b and c : d → ac : bd'},
            {'k': 'Duplicate / triplicate', 'v': 'a² : b² / a³ : b³'},
            {'k': 'Sub-duplicate / sub-triplicate', 'v': '√a : √b / ∛a : ∛b'},
            {'k': 'Mean proportional', 'v': 'b = √(ac)'},
            {'k': 'Third proportional to a, b', 'v': 'b² / a'},
            {'k': 'Fourth proportional to a, b, c', 'v': 'bc / a'},
            {'k': 'Componendo and dividendo', 'v': 'p/q = r/s ⇒ (p + q)/(p − q) = (r + s)/(r − s)'},
            {'k': 'Index laws', 'v': 'aᵐaⁿ = aᵐ⁺ⁿ; aᵐ/aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; a⁰ = 1; a⁻ⁿ = 1/aⁿ'},
            {'k': 'Log laws', 'v': 'log mn = log m + log n; log m/n = log m − log n; log mⁿ = n log m'},
            {'k': 'Change of base', 'v': 'logₐ m = log_b m / log_b a; logₐ b · log_b a = 1'},
            {'k': 'Digits in N', 'v': 'characteristic of log N + 1'},
        ],
        'viva': viva(),
        'cases': [case],
    }
    return unit


def viva():
    return [
        V('v1', 'What is a ratio, and what conditions must its two terms satisfy?',
          'A ratio compares two quantities by division. Both quantities must be of the same kind and expressed in the same unit, so the ratio itself has no unit. The first term is called the antecedent and the second term is the consequent, and the order matters, so 2 is to 5 is not the same as 5 is to 2.',
          [P('p1', 'Comparison of two quantities by division', 2, 'divid|division|fraction|quotient|compar'),
           P('p2', 'Same kind and same unit; a ratio has no unit', 3, 'same kind|same type|like quantit|similar quantit|same unit|same units|common unit|no unit|without unit|pure number', min=1),
           P('p3', 'Antecedent = first term, consequent = second term', 3, 'antecedent', 'consequent'),
           P('p4', 'Order matters — a : b differs from b : a', 2, 'order matter|order important|order is important|order does matter|order counts|not same as|not the same|different|cannot swap|cannot interchange|can not swap|reverse')], 'c1'),
        V('v2', 'Explain duplicate, triplicate, sub-duplicate and sub-triplicate ratios of a is to b.',
          'The duplicate ratio squares both terms, giving a squared is to b squared. The triplicate ratio cubes both terms, giving a cubed is to b cubed. The sub-duplicate ratio takes the square root of each term, and the sub-triplicate ratio takes the cube root of each term.',
          [P('p1', 'Duplicate = squares of the terms (a² : b²)', 3, ALT('{d} {s}', d=['duplicate ratio', 'duplicate'], s=['squares', 'square both', 'squaring', 'a squared', 'squared'])),
           P('p2', 'Triplicate = cubes of the terms (a³ : b³)', 3, ALT('{d} {s}', d=['triplicate ratio', 'triplicate'], s=['cubes', 'cube both', 'cubing', 'a cubed', 'cubed'])),
           P('p3', 'Sub-duplicate = square roots', 2, 'sub duplicate square root|subduplicate square root|sub duplicate root|sub duplicate under root'),
           P('p4', 'Sub-triplicate = cube roots', 2, 'sub triplicate cube root|subtriplicate cube root|sub triplicate root')], 'c2'),
        V('v3', 'If a, b and c are in continued proportion, what is b called, what relation holds, and what is c called?',
          'If a, b, c are in continued proportion then a is to b as b is to c. The middle term b is the mean proportional between a and c, and b squared equals a times c, so b is the square root of a c. The last term c is the third proportional to a and b.',
          [P('p1', 'b is the mean proportional between a and c', 4, 'b mean proportional|mean proportional b|b is mean|b called mean|middle term mean|b geometric mean|mean proportion'),
           P('p2', 'b² = ac (b = √ac)', 4, 'b squar equal ac|b squar ac|b squar equal c|b squared equals a times c|b squar equal times c|b square product|square b equal product|b square equal product|b root ac|b square root ac|b under root ac|b equal root ac|b equal square root ac|b squar root c|b root c|b equal root c|b equal squar root c'),
           P('p3', 'c is the third proportional to a and b', 2, 'c third proportional|c is third|c called third|third proportional c|last term third')], 'c3'),
        V('v4', 'State the three basic laws of logarithms.',
          'First, the log of a product equals the sum of the logs: log of m n equals log m plus log n. Second, the log of a quotient equals the difference of the logs: log of m by n equals log m minus log n. Third, the log of a power equals the power times the log: log of m to the power n equals n log m.',
          [P('p1', 'Product law: log mn = log m + log n', 4, ALT('{l} product {e} sum', 'product {e} {a} {l}', 'log mn {e} log m plus log n', 'log m n log m plus log n', l=['log', 'logarithm'], e=['equal', 'is', 'becomes', 'gives'], a=['sum', 'addition', 'add'])),
           P('p2', 'Quotient law: log m/n = log m − log n', 3, ALT('{l} quotient {e} difference', 'quotient {e} {a}', 'division {e} {a}', 'log m by n log m minus log n', 'log m over n log m minus log n', 'divid subtract', l=['log', 'logarithm'], e=['equal', 'is', 'becomes', 'gives'], a=['difference', 'subtraction', 'subtract'])),
           P('p3', 'Power law: log mⁿ = n log m', 3, 'power time log|power multipli log|power multiply log|n log m|index time log|exponent time log|multiplied by the log|power come down|power comes in front|power in front')], 'c7'),
        V('v5', 'What are the characteristic and the mantissa of a common logarithm, and how is the characteristic found?',
          'The characteristic is the integer part of the logarithm and the mantissa is the decimal part, which is always kept positive. For a number greater than one, the characteristic is one less than the number of digits before the decimal point. For a number less than one, it is negative and equal to one more than the number of zeros right after the decimal point.',
          [P('p1', 'Characteristic = integral (whole-number) part', 2, 'characteristic integ|characteristic whole|characteristic integral|integer part characteristic|integral part characteristic|whole number part characteristic|characteristic is the integer'),
           P('p2', 'Mantissa = decimal (fractional) part, always positive', 3, 'mantissa decimal|mantissa fraction|decimal part mantissa|fractional part mantissa', 'positive|never negative|not negative', min=2),
           P('p3', 'Number > 1: characteristic = digits before decimal − 1', 3, ALT('{o} less than {n} digit', '{n} digit minus {o}', '{n} digit less {o}', 'digit before decimal minus 1', 'digits minus 1', o=['one', '1'], n=['number of', 'no of', 'count of', ''])),
           P('p4', 'Number < 1: negative, one more than zeros after the decimal point', 2, 'negative', ALT('{o} more than {n} {z}', '{z} plus {o}', '{z} after decimal plus 1', o=['one', '1'], n=['number of', 'no of', ''], z=['zeros', 'zero', 'zeroes']))], 'c8'),
        V('v6', 'What do a to the power zero, a to the power minus n, and a to the power one by n mean?',
          'Any non-zero number raised to the power zero equals one. A negative index means a reciprocal, so a to the power minus n equals one over a to the power n. A fractional index one by n means the n-th root of a.',
          [P('p1', 'a⁰ = 1 (a ≠ 0)', 3, 'power zero equal 1|power zero is 1|power 0 equal 1|power zero equals one|zero power 1|zero index 1|power zero one|zero is one|power zero 1'),
           P('p2', 'a⁻ⁿ = 1/aⁿ — reciprocal', 4, 'reciprocal|1 over a power n|1 by a power n|one over a|inverse|1 divided by'),
           P('p3', 'a^(1/n) = n-th root of a', 3, 'nth root|n th root|root of a|n root|th root')], 'c5'),
    ]
