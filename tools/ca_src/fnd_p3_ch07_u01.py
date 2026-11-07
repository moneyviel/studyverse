"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 7 Sets, Relations and Functions, Basics of Limits and Continuity functions.
Original explanations, numbers and questions (scope and order follow the ICAI study material).
Set counts, relation properties and limits are computed here (sets, brute force, exact fractions) and stored with checks."""
from fractions import Fraction as F
from itertools import product
from lib import *
import re
from ca_viva import P, V

UID = 'fnd-p3-ch07-u01'


def ev(expr):
    v = eval(expr, {'__builtins__': {}}, {'round': round})
    v = round(v, 2)
    return int(v) if v == int(v) else v


def fmt(x):
    if isinstance(x, str): return x
    if isinstance(x, float) and x != int(x): return f'{x:g}'
    return inr(int(x))


def mq(mid, q, right, wrong, explain, concept, diff='core', check=None, topic=None):
    assert len(wrong) == 3, mid
    k = sum(map(ord, mid)) % 4
    opts = [fmt(w) for w in wrong]
    opts.insert(k, fmt(right))
    d = {'id': mid, 'q': q, 'options': opts, 'answer': k, 'explain': explain, 'concept': concept, 'difficulty': diff}
    if topic: d['topic'] = topic
    if check is not None:
        v = ev(check)
        assert abs(v - float(re.match(r'[₹\s]*(-?[\d,]*\.?\d+)', str(right)).group(1).replace(',', ''))) < 0.006, (mid, check, v, right)
        d['check'] = check
    return d


def fs(s):
    """Set to text. A one-element set is written with spaces, '{ 7 }', and the empty set as ∅."""
    s = sorted(s, key=lambda x: (str(type(x)), x))
    if not s: return '∅'
    if len(s) == 1: return '{ ' + str(s[0]) + ' }'
    return '{' + ', '.join(str(x) for x in s) + '}'


def fr(R):
    return '{' + ', '.join(f'({a}, {b})' for a, b in sorted(R)) + '}'


def props(R, S):
    refl = all((a, a) in R for a in S)
    sym = all((b, a) in R for a, b in R)
    trans = all((a, d) in R for a, b in R for c, d in R if b == c)
    return refl, sym, trans


def yn(b): return 'Yes' if b else 'No'


def build():
    # ------------------------------------------------------------------ Illustration 1: set operations
    U = set(range(1, 13)); A = {2, 4, 6, 8, 10, 12}; B = {3, 6, 9, 12}
    AuB, AnB, AmB, BmA, Bc = A | B, A & B, A - B, B - A, U - B
    lhs, rhs = U - (A | B), (U - A) & (U - B)
    lhs2, rhs2 = U - (A & B), (U - A) | (U - B)
    assert lhs == rhs and lhs2 == rhs2
    c1 = Checks()
    c1.add('6+4-2', 'n(A ∪ B) = n(A) + n(B) − n(A ∩ B)')
    assert len(AuB) == 8
    c1.add('12-8', "n((A ∪ B)′) = 12 − 8")

    # ------------------------------------------------------------------ Illustration 2: three-set survey (regions built explicitly)
    tot, nG, nI, nA, GI, IA, GA, GIA = 200, 120, 90, 70, 50, 30, 25, 15
    only_G = nG - GI - GA + GIA; only_I = nI - GI - IA + GIA; only_A = nA - IA - GA + GIA
    GI_only, IA_only, GA_only = GI - GIA, IA - GIA, GA - GIA
    union = only_G + only_I + only_A + GI_only + IA_only + GA_only + GIA
    c2 = Checks()
    assert c2.add('120+90+70-50-30-25+15', 'n(G ∪ I ∪ A)') == union == 190
    c2.add('200-190', 'clients using none of the three')
    assert c2.add('120-50-25+15', 'GST only') == only_G == 60
    c2.add('90-50-30+15', 'income tax only')
    c2.add('70-30-25+15', 'audit only')
    c2.add('(50+30+25)-3*15', 'exactly two services')
    c2.add('60+25+30', 'exactly one service')
    assert only_I == 25 and only_A == 30 and GI_only + IA_only + GA_only == 60

    # ------------------------------------------------------------------ Illustration 3: power set and Cartesian product
    from itertools import combinations
    Ap = ['p', 'q', 'r']
    subsets = [c for k in range(4) for c in combinations(Ap, k)]
    assert len(subsets) == 8
    sub_txt = ', '.join('∅' if not c else ('{ ' + c[0] + ' }' if len(c) == 1 else '{' + ', '.join(c) + '}') for c in subsets)
    AxB = [(a, b) for a in Ap for b in (1, 2)]
    c3 = Checks()
    c3.add('2**3', 'number of subsets of a 3-element set')
    c3.add('2**3-1', 'proper subsets')
    c3.add('3*2', 'n(A × B)')
    c3.add('3*2*4', 'n(A × B × C) when n(C) = 4')
    c3.add('2**(3*2)', 'number of relations from A to B')

    # ------------------------------------------------------------------ Illustration 4: relations on S = {1, 2, 3}
    S = {1, 2, 3}
    R1 = {(1, 1), (2, 2), (3, 3), (2, 3), (3, 2)}
    R2 = {(1, 2), (2, 3), (1, 3)}
    R3 = {(1, 1), (2, 2), (3, 3), (2, 3), (3, 1)}
    p1, p2, p3 = props(R1, S), props(R2, S), props(R3, S)
    assert p1 == (True, True, True) and p2 == (False, False, True) and p3 == (True, False, False)
    R2inv = {(b, a) for a, b in R2}
    dom2, ran2 = {a for a, b in R2}, {b for a, b in R2}
    c4 = Checks()
    c4.add('2**(3*3)', 'number of relations on a 3-element set')

    # ------------------------------------------------------------------ Illustration 5: functions
    c5 = Checks()
    c5.add('(3+2)**2', 'g(f(3)) with f(x) = x + 2, g(x) = x²')
    c5.add('3**2+2', 'f(g(3))')
    c5.add('(20-5)/3', 'f⁻¹(20) for f(x) = 3x + 5')
    c5.add('3**4', 'number of functions from a 4-element set to a 3-element set')
    c5.add('5*4*3', 'one-one functions from a 3-element set into a 5-element set')

    # ------------------------------------------------------------------ Illustration 6: limits
    c6 = Checks()
    c6.add('3+3', 'lim (x² − 9)/(x − 3) as x → 3 = x + 3 at x = 3')
    c6.add('5*2**4', 'lim (x⁵ − 32)/(x − 2) as x → 2 = 5·2⁴')
    c6.add('3/6', 'lim (3x² + 5x)/(6x² − 1) as x → ∞')
    c6.add('2*2+3', 'left-hand limit of 2x + 3 at x = 2')
    c6.add('2**2', 'right-hand limit of x² at x = 2')
    # numeric confirmation
    f6a = lambda x: (x * x - 9) / (x - 3)
    assert abs(f6a(3.000001) - 6) < 1e-4
    f6b = lambda x: (x ** 5 - 32) / (x - 2)
    assert abs(f6b(2.000001) - 80) < 1e-3

    # ------------------------------------------------------------------ Illustration 7: continuity and standard limits
    c7 = Checks()
    c7.add('4+4', 'k = lim (x² − 16)/(x − 4) as x → 4')
    c7.add('3*1', 'lim (e³ˣ − 1)/x = 3 × lim (eᵗ − 1)/t')
    c7.add('1-2+3', 'value at x = 1 of x² − 2x + 3 (polynomial — continuous)')
    import math
    assert abs((math.exp(3e-7) - 1) / 1e-7 - 3) < 1e-4

    # ------------------------------------------------------------------ Jobs
    cj1 = Checks()
    j_none = cj1.add('480-(310+260+150-140-90-70+40)', 'customers using none of the three products')
    j_onlyL = cj1.add('310-140-70+40', 'loan only')
    cj2 = Checks()
    cj2.add('100*12', 'max different employee IDs mapped if each code is used once (one-one into)')

    # ------------------------------------------------------------------ Questions
    qc1 = Checks()
    q_union = qc1.add('40+35+25-12-10-8+4', 'n(S ∪ F ∪ R)')
    q_none = qc1.add('100-74', 'pieces with no defect')
    q_oS = qc1.add('40-12-10+4', 'strength defect only')
    q_oF = qc1.add('35-12-8+4', 'flexibility defect only')
    q_oR = qc1.add('25-10-8+4', 'radius defect only')
    q_one = qc1.add('22+19+11', 'exactly one defect')
    q_two = qc1.add('(12+10+8)-3*4', 'exactly two defects')
    q_chk = qc1.add('52+18+4+26', 'regions add back to 100')

    A2 = [1, 2, 3, 6]
    RD = {(a, b) for a in A2 for b in A2 if b % a == 0}
    pd = props(RD, set(A2))
    assert pd == (True, False, True) and len(RD) == 9
    qc2 = Checks()
    qc2.add('4+2+2+1', 'pairs (a, b) with a dividing b: from 1, 2, 3, 6 respectively')
    qc2.add('2**(4*4)', 'number of relations on a 4-element set')

    qc3 = Checks()
    qa = qc3.add('(3*3**2)/(2*3)', '(a) lim (x³ − 27)/(x² − 9) = 3x²/(2x)… = 27/6 at x = 3')
    qb = qc3.add('2/5', '(b) lim (2x³ − x + 7)/(5x³ + 4x²) as x → ∞')
    qk = qc3.add('(3*2-1-1)/2', '(c) k from 2k + 1 = 3(2) − 1')
    assert F(27, 6) == F(9, 2) and abs(((3.000001 ** 3 - 27) / (3.000001 ** 2 - 9)) - 4.5) < 1e-4

    ck = Checks()
    k_n = ck.add('300-(210+150-90)', 'neither filed online nor used a CA')
    k_o = ck.add('210-90', 'online only')
    k_e = ck.add('(210-90)+(150-90)', 'exactly one of the two')
    k_p = ck.add('(150-90)/300*100', 'used a CA but did not file online, % of all')

    # ------------------------------------------------------------------ MCQs
    M = []
    M.append(mq('m1', 'How many subsets does a set with 5 elements have?', 32, [25, 31, 10], "Each of the 5 elements is either in a subset or not — 2 choices each — so the number of subsets is 2⁵ = 32, which includes the empty set and the set itself. The trap is 31, which is the number of proper subsets (excluding the set itself); 25 squares 5 instead of raising 2 to the power 5. In practice: if a client can opt for any combination of 5 add-on services, a firm has 32 possible service bundles, including 'none' and 'all'.", 'c3', 'core', '2**5', topic='Subsets and the power set'))
    M.append(mq('m2', 'The number of proper subsets of {a, b, c, d} is:', 15, [16, 14, 4], '{a, b, c, d} has 2⁴ = 16 subsets. A proper subset is any subset other than the set itself, so there are 16 − 1 = 15. The trap is 16, which counts all subsets; 14 wrongly removes the empty set as well — but ∅ is a proper subset. In practice: listing proper subsets is how a planner counts the ways of choosing some, but not all, of a set of options, such as partial rollouts of a new policy.', 'c3', 'core', '2**4-1', topic='Subsets and the power set'))
    M.append(mq('m3', 'If n(A) = 40, n(B) = 25 and n(A ∩ B) = 10, then n(A ∪ B) is:', 55, [65, 75, 30], 'By the addition rule, n(A ∪ B) = n(A) + n(B) − n(A ∩ B) = 40 + 25 − 10 = 55. The overlap is subtracted once because it was counted in both A and B. The trap is 65, which adds without removing the double-counted overlap. In practice: when merging two customer lists, a marketing analyst subtracts customers who appear on both lists to get the true number of unique customers.', 'c5', 'core', '40+25-10', topic='Venn diagrams and counting'))
    M.append(mq('m4', 'In a group of 100 people, 60 drink tea, 45 drink coffee and 20 drink both. How many drink neither?', 15, [35, 5, 0], "People who drink tea or coffee = 60 + 45 − 20 = 85. Those who drink neither = 100 − 85 = 15. The trap is subtracting 60 and 45 straight from 100, which counts the 20 who drink both twice (and even gives a negative number); always find the union first. In practice: survey analysts at market-research firms use this exact Venn calculation to find the 'neither' segment, often the target for a new product.", 'c5', 'core', '100-(60+45-20)', topic='Venn diagrams and counting'))
    M.append(mq('m5', 'Which of these is the empty set?', '{x : x is a natural number less than 1}', ['{x : x is an even prime}', '{x : x² = 4}', '{ 0 }'], "The empty set has no elements. Since the smallest natural number is 1, there is no natural number less than 1, so that set is empty. The trap is { 0 }, which looks empty but contains one element, the number 0. The even prime set contains 2, and x² = 4 gives {−2, 2}. In practice: database queries that return 'no records' — for example, invoices dated before the company existed — are empty sets, and auditors treat them as meaningful results.", 'c2', 'core', topic='Types of sets'))
    M.append(mq('m6', 'If A ⊆ B, then A ∪ B equals:', 'B', ['A', 'A ∩ B', '∅'], "If A ⊆ B, every element of A already belongs to B, so joining them adds nothing new: A ∪ B = B. The trap is A, which is the answer for A ∩ B (the common part is all of A). In practice: if every GST-registered client is also on a firm's master client list, combining the two lists simply gives the master list.", 'c4', 'core', topic="Operations on sets and De Morgan's laws"))
    M.append(mq('m7', 'By De Morgan\'s law, (A ∪ B)′ equals:', 'A′ ∩ B′', ['A′ ∪ B′', 'A ∩ B', '(A ∩ B)′'], "De Morgan's law: the complement of a union is the intersection of the complements, (A ∪ B)′ = A′ ∩ B′ — 'not in A or B' means 'not in A and not in B'. The trap is A′ ∪ B′, which is the complement of the intersection, (A ∩ B)′. In practice: an auditor selecting entries that are 'neither cash nor above ₹1 lakh' is applying De Morgan's law in a spreadsheet filter.", 'c4', 'core', topic="Operations on sets and De Morgan's laws"))
    M.append(mq('m8', 'If A = {1, 2, 3} and B = {3, 4}, then A − B is:', '{1, 2}', ['{ 4 }', '{1, 2, 4}', '{ 3 }'], "A − B keeps the elements of A that are not in B. From {1, 2, 3}, remove 3 (which is in B), leaving {1, 2}. The trap is { 4 }, which is B − A — the order of the difference matters. {1, 2, 4} is the symmetric difference. In practice: comparing a sales ledger with a debtors' list, 'invoices in the ledger but not on the list' is a set difference that auditors investigate.", 'c4', 'core', topic="Operations on sets and De Morgan's laws"))
    M.append(mq('m9', 'If A has 4 elements and B has 3, the number of elements in A × B is:', 12, [7, 64, 81], 'A × B is the set of all ordered pairs (a, b) with a from A and b from B, so n(A × B) = n(A) × n(B) = 4 × 3 = 12. The trap is 7, which adds the sizes instead of multiplying; 64 = 4³ and 81 = 3⁴ confuse the product with powers. In practice: a retailer with 4 shirt sizes and 3 colours needs 12 SKU codes — a Cartesian product.', 'c6', 'core', '4*3', topic='Ordered pairs and the Cartesian product'))
    M.append(mq('m10', 'Sets P, Q and R have 3, 5 and 2 elements. The Cartesian product P × Q × R has:', 30, [10, 15, 60], 'The Cartesian product of three sets contains ordered triples, one choice from each set, so the count is 3 × 5 × 2 = 30. The trap is 10, which adds the sizes; 15 multiplies only two of them. In practice: a travel portal combining 3 airlines, 5 time-slots and 2 fare classes offers 30 distinct options — a three-set product.', 'c6', 'core', '3*5*2', topic='Ordered pairs and the Cartesian product'))
    M.append(mq('m11', 'The number of different relations from a set with 2 elements to a set with 3 elements is:', 64, [6, 8, 9], 'A relation from A to B is any subset of A × B. Here A × B has 2 × 3 = 6 ordered pairs, and a set of 6 elements has 2⁶ = 64 subsets, so there are 64 relations (including the empty relation). The trap is 6, which counts the ordered pairs, not the relations; 8 and 9 are 2³ and 3². In practice: access-control matrices in IT audits map users to permissions, and each possible mapping is one relation.', 'c7', 'moderate', '2**(2*3)', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m12', 'On the set of natural numbers, the relation "is less than" is:', 'Transitive only', ['An equivalence relation', 'Reflexive and transitive', 'Symmetric only'], "Check each property. a < a is false, so it is not reflexive. a < b does not give b < a, so it is not symmetric. a < b and b < c give a < c, so it is transitive. Hence 'transitive only'. The trap is 'reflexive and transitive', which describes 'less than or equal to' (≤), not strict '<'. In practice: approval hierarchies work this way — if A ranks below B and B below C, then A ranks below C.", 'c7', 'moderate', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m13', 'The relation "has the same date of birth as" on a set of people is:', 'An equivalence relation', ['Reflexive only', 'Symmetric only', 'Transitive but not symmetric'], "Everyone has the same birth date as themselves (reflexive); if A shares B's birth date, B shares A's (symmetric); and if A matches B and B matches C, A matches C (transitive). All three hold, so it is an equivalence relation. The trap is 'symmetric only', which overlooks the reflexive and transitive properties. In practice: equivalence relations split data into groups — for example, grouping employees by birth month for payroll or celebration lists.", 'c7', 'core', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m14', 'On S = {1, 2}, the relation R = {(1, 2), (2, 1)} is:', 'Symmetric but neither reflexive nor transitive', ['An equivalence relation', 'Reflexive and symmetric', 'Transitive but not symmetric'], "R is symmetric because (1, 2) and (2, 1) both appear. It is not reflexive since (1, 1) and (2, 2) are missing. It is not transitive: (1, 2) and (2, 1) would require (1, 1). So it is symmetric but neither reflexive nor transitive. The trap is 'an equivalence relation', which needs all three properties. In practice: a 'has traded with' relation between two firms is symmetric, but it need not be transitive across a chain of firms.", 'c7', 'hard', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m15', 'For R = {(1, 4), (2, 5), (3, 4)}, the range of R is:', '{4, 5}', ['{1, 2, 3}', '{1, 2, 3, 4, 5}', '{ 4 }'], 'The range of a relation is the set of second elements of its ordered pairs. From (1, 4), (2, 5) and (3, 4), the second elements are 4, 5 and 4, so the range is {4, 5}. The trap is {1, 2, 3}, which is the domain (first elements). In practice: if a relation maps employees to departments, the range is the set of departments that actually have staff.', 'c7', 'core', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m16', 'The inverse of the relation R = {(1, a), (2, b), (3, b)} is:', '{(a, 1), (b, 2), (b, 3)}', ['{(1, a), (2, b), (3, b)}', '{(a, 1), (b, 2)}', '{(1, b), (2, a), (3, a)}'], "The inverse of a relation is formed by reversing every ordered pair: (1, a) → (a, 1), (2, b) → (b, 2), (3, b) → (b, 3). So R⁻¹ = {(a, 1), (b, 2), (b, 3)}. The trap is {(a, 1), (b, 2)}, which drops (b, 3) because b repeats — but in a relation, an element may pair with several others. In practice: inverting a 'client → partner' mapping gives each partner's list of clients.", 'c7', 'core', topic='Relations: domain, range, inverse and types'))
    M.append(mq('m17', 'How many functions can be defined from a set with 3 elements to a set with 2 elements?', 8, [6, 9, 5], 'A function assigns exactly one image to every element of the domain. Each of the 3 domain elements can choose either of 2 images, so there are 2 × 2 × 2 = 2³ = 8 functions. The trap is 9 = 3², which reverses the roles of the two sets; 6 multiplies 3 × 2. In practice: assigning each of 3 clients to one of 2 staff members, where a staff member may handle several clients, gives 8 possible allocations.', 'c8', 'moderate', '2**3', topic='Functions (mappings) and their types'))
    M.append(mq('m18', 'How many one-one functions are there from a set with 3 elements into a set with 5 elements?', 60, [125, 10, 15], 'In a one-one function different elements must get different images. The first element has 5 choices, the second 4, the third 3: 5 × 4 × 3 = 60 (= ⁵P₃). The trap is 125 = 5³, which allows two elements to share an image. In practice: assigning 3 interns to 3 different desks out of 5 — no desk shared — is a one-one function.', 'c8', 'hard', '5*4*3', topic='Functions (mappings) and their types'))
    M.append(mq('m19', 'f : R → R defined by f(x) = x² is:', 'Many-one and into', ['One-one and onto', 'One-one and into', 'Many-one and onto'], "f(x) = x² is many-one because different inputs give the same output, e.g. f(2) = f(−2) = 4. It is into, not onto, because negative real numbers in the co-domain have no pre-image (no real x has x² = −1). The trap is 'many-one and onto', which would be true only if the co-domain were restricted to non-negative reals. In practice: a mapping from sales figures to tax slabs is many-one, since many sales figures fall in the same slab.", 'c8', 'moderate', topic='Functions (mappings) and their types'))
    M.append(mq('m20', 'If f(x) = 2x + 1 (f : R → R), then f⁻¹(x) is:', '(x − 1)/2', ['(x + 1)/2', '1/(2x + 1)', '2x − 1'], 'Write y = 2x + 1 and solve for x: x = (y − 1)/2. Swapping letters, f⁻¹(x) = (x − 1)/2. Check: f(3) = 7 and f⁻¹(7) = 3. The trap is 1/(2x + 1), which is the reciprocal of f, not its inverse — an inverse undoes the function. In practice: converting a gross amount back to the base figure, such as removing a fixed charge and halving, is applying an inverse function.', 'c8', 'core', topic='Functions (mappings) and their types'))
    M.append(mq('m21', 'If f(x) = x + 1 and g(x) = 2x, then f(g(3)) is:', 7, [8, 6, 9], 'Work from the inside out: g(3) = 2 × 3 = 6, then f(6) = 6 + 1 = 7. The trap is 8, which computes g(f(3)) = g(4) instead — order matters in composite functions. In practice: a flat ₹100 discount given before adding 18% GST produces a different bill from the same discount given after GST, so billing formulas must fix the order.', 'c8', 'core', '2*3+1', topic='Functions (mappings) and their types'))
    M.append(mq('m22', 'A function has an inverse function if and only if it is:', 'One-one and onto', ['One-one only', 'Onto only', 'A constant function'], "An inverse function must send every element of the co-domain back to exactly one element. Onto guarantees at least one pre-image, and one-one guarantees at most one, so both are needed: the function must be one-one and onto (a bijection). The trap is 'one-one only', which still leaves some co-domain elements without a pre-image. In practice: a unique ID like PAN works both ways only because each person has one PAN and each PAN belongs to one person.", 'c8', 'core', topic='Functions (mappings) and their types'))
    M.append(mq('m23', 'lim (x³ − 8)/(x − 2) as x → 2 equals:', 12, [4, 8, 0], 'Direct substitution gives 0/0. Use the standard limit lim (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹: 3 × 2² = 12. Or factorise: x³ − 8 = (x − 2)(x² + 2x + 4), and x² + 2x + 4 at x = 2 is 12. The trap is 8, which just substitutes 2³; 0 reads 0/0 as zero. In practice: limits of this form underlie the derivative, which economists use to find marginal cost from a total-cost formula.', 'c9', 'core', '3*2**2', topic='Limit of a function'))
    M.append(mq('m24', 'lim (4x² + 1)/(2x² − 3x) as x → ∞ equals:', 2, [0, 4, '∞'], "For x → ∞, divide top and bottom by the highest power, x²: (4 + 1/x²)/(2 − 3/x) → 4/2 = 2, since 1/x² and 3/x tend to zero. The trap is 4, which takes only the numerator's leading coefficient; ∞ assumes large x makes the fraction blow up. In practice: such limits describe long-run behaviour — for example, average cost per unit settling to a steady value as output becomes very large.", 'c9', 'moderate', '4/2', topic='Limit of a function'))
    M.append(mq('m25', 'lim (e⁵ˣ − 1)/x as x → 0 equals:', 5, [1, 0, 'e⁵'], 'Rewrite as 5 × (e⁵ˣ − 1)/(5x). As x → 0, 5x → 0, and the standard limit (eᵗ − 1)/t → 1, so the answer is 5 × 1 = 5. The trap is 1, which applies the standard limit without adjusting for the 5 in the exponent; e⁵ substitutes x = 1. In practice: this limit is the basis of continuous compounding, where interest at rate r grows money by the factor eʳᵗ.', 'c9', 'moderate', '5*1', topic='Limit of a function'))
    M.append(mq('m26', 'lim (x² + 3x − 4)/(x − 1) as x → 1 equals:', 5, [0, 4, 3], "Substitution gives 0/0, so factorise: x² + 3x − 4 = (x − 1)(x + 4). Cancel (x − 1) (allowed because x ≠ 1 near the limit) and put x = 1: 1 + 4 = 5. The trap is 0, which reads the 0/0 form as zero — 0/0 is indeterminate and needs simplification. In practice: removing a common factor before evaluating avoids 'division by zero' errors in spreadsheet models of per-unit figures.", 'c9', 'core', '1+4', topic='Limit of a function'))
    M.append(mq('m27', 'lim f(x) as x → a exists when:', 'The left-hand and right-hand limits both exist and are equal', ['f(a) is defined', 'Only the right-hand limit exists', 'f(a) = 0'], "A limit at a exists when the left-hand limit and the right-hand limit both exist and are equal; the limit is that common value. The trap is 'f(a) is defined' — the limit concerns values near a, not at a, so f(a) may be undefined or different without affecting the limit. In practice: in tax-slab calculations, checking the left and right limits at a threshold shows whether tax jumps suddenly, which is why marginal relief exists.", 'c9', 'core', topic='Limit of a function'))
    M.append(mq('m28', 'f(x) = (x² − 25)/(x − 5) for x ≠ 5 and f(5) = k. For f to be continuous at x = 5, k must be:', 10, [5, 0, 25], 'For x ≠ 5, (x² − 25)/(x − 5) = x + 5, so the limit as x → 5 is 10. Continuity requires f(5) to equal the limit, so k = 10. The trap is 0, from substituting x = 5 directly and reading 0/0 as zero; 25 uses 5² alone. In practice: defining a value at a gap so that a formula stays smooth is like a pricing table that must not jump at a slab boundary.', 'c10', 'moderate', '5+5', topic='Continuity at a point'))
    M.append(mq('m29', 'f(x) = 3x + 1 for x < 2 and f(x) = 5x − 3 for x ≥ 2. At x = 2, f is:', 'Continuous, because both one-sided limits and f(2) equal 7', ['Discontinuous, because the formula changes', 'Discontinuous, because the left limit is 6', 'Continuous, because f(2) = 10'], "Left-hand limit = 3(2) + 1 = 7; right-hand limit = 5(2) − 3 = 7; and f(2) = 5(2) − 3 = 7. All three are equal, so f is continuous at x = 2. The trap is 'discontinuous because the formula changes' — a change of formula breaks continuity only if the pieces fail to meet. In practice: slab-based tariffs, like electricity bills, are designed so the charge formula changes but the bill does not jump at the boundary.", 'c10', 'hard', topic='Continuity at a point'))
    M.append(mq('m30', 'Two sets A and B are equivalent when:', 'n(A) = n(B)', ['A = B', 'A ⊆ B', 'A ∩ B = ∅'], 'Equivalent sets have the same number of elements, n(A) = n(B), even if the elements differ — {1, 2, 3} and {a, b, c} are equivalent. The trap is A = B, which is equality: the same elements exactly. Equal sets are always equivalent, but equivalent sets need not be equal. In practice: matching a list of 50 invoices with 50 payments shows equal counts (equivalence), but an auditor still checks that the items actually correspond.', 'c2', 'core', topic='Types of sets'))

    rows4 = [[name, fr(R), yn(pp[0]), yn(pp[1]), yn(pp[2]), 'Yes' if all(pp) else 'No'] for name, R, pp in (('R₁', R1, p1), ('R₂', R2, p2), ('R₃', R3, p3))]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch07', 'n': 1,
        'title': 'Sets, Relations and Functions, Basics of Limits and Continuity functions',
        'outcomes': [
            'Write sets in roster and set-builder form, recognise types of sets and count subsets and proper subsets.',
            'Perform union, intersection, difference and complement, apply De Morgan\'s laws and solve two- and three-set survey problems with Venn diagrams.',
            'Form Cartesian products and relations; find domain, range and inverse; test a relation for reflexive, symmetric, transitive and equivalence properties.',
            'Identify functions and classify them as one-one, many-one, onto, into or bijective; work with identity, constant, composite and inverse functions.',
            'Evaluate limits using left- and right-hand limits, the algebra of limits and standard results, and test a function for continuity at a point.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 70}, 'prereq': ['fnd-p3-ch02-u01'],
                 'exam_tip': 'Venn-diagram survey questions are the most frequent; draw the three circles and fill the centre first, then work outwards. For relations, test each property on the given pairs — do not guess from the wording.'},
        'concepts': [
            {'id': 'c1', 'title': 'Sets, elements and the two ways of writing a set',
             'body': ['A set is a collection of distinct objects described clearly enough that, for any object, we can say for certain whether it belongs. "The vowels of English" is a set; "the good books in the library" is not, because "good" is a matter of opinion.',
                      'Objects in a set are its elements; x ∈ A means x belongs to A and x ∉ A means it does not. Sets are named by capital letters and elements by small letters.',
                      'Roster (tabular) form lists the elements inside braces: {2, 4, 6, 8}. Set-builder (rule) form states the property: {x : x is an even natural number less than 10}. Repeating an element or changing the order does not change a set.'],
             'analogy': 'A guest list with a clear rule — "all partners of the firm" — is a set; "people the host likes" is not well-defined.',
             'work': 'Defining a population precisely ("all purchase invoices above ₹1 lakh dated in FY 2025-26") is the first step of any audit sample — it is set-builder form in practice.'},
            {'id': 'c2', 'title': 'Types of sets',
             'body': ['Empty (null) set ∅: no elements, e.g. {x : x is a natural number and x < 1}. A singleton set has exactly one element, such as { 0 } — which is not empty.',
                      'Finite sets have a countable last element; infinite sets do not (the natural numbers). n(A), the cardinal number, is the number of distinct elements of a finite set.',
                      'Equal sets (A = B) have exactly the same elements. Equivalent sets have the same number of elements, n(A) = n(B), even if the elements differ. Equal sets are always equivalent; equivalent sets need not be equal.',
                      'The universal set U contains every element under discussion in a given problem; all other sets are subsets of it.'],
             'analogy': 'Two teams of eleven players are equivalent (same count) but not equal (different players).',
             'work': 'Reconciliations compare equivalent-looking lists: the same number of entries in the bank statement and the cash book does not mean the entries are equal.'},
            {'id': 'c3', 'title': 'Subsets and the power set',
             'body': ['A ⊆ B (A is a subset of B) when every element of A is also in B. A is a proper subset (A ⊂ B) if, in addition, B has at least one element not in A.',
                      'The empty set is a subset of every set, and every set is a subset of itself.',
                      'A set with n elements has 2ⁿ subsets (each element is either in or out) and 2ⁿ − 1 proper subsets. The power set P(A) is the set of all subsets of A, so n(P(A)) = 2ⁿ.'],
             'analogy': 'Choosing toppings for a pizza from 3 options: each topping is on or off, so 2 × 2 × 2 = 8 possible pizzas, including the plain one (∅).',
             'work': 'The 2ⁿ idea tells you how fast the number of possible combinations of controls, user permissions or product features grows.'},
            {'id': 'c4', 'title': 'Operations on sets and De Morgan\'s laws',
             'body': ['Union A ∪ B: elements in A or B or both. Intersection A ∩ B: elements common to both. Disjoint sets have A ∩ B = ∅.',
                      'Difference A − B: elements of A that are not in B (A − B ≠ B − A in general). Complement A′ = U − A: elements of U not in A.',
                      'Laws: union and intersection are commutative and associative; A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C) and A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C); A ∪ A′ = U, A ∩ A′ = ∅.',
                      'De Morgan\'s laws: (A ∪ B)′ = A′ ∩ B′ and (A ∩ B)′ = A′ ∪ B′ — complement each set and swap ∪ with ∩.'],
             'analogy': 'De Morgan in plain words: "not (tea or coffee)" means "no tea and no coffee"; "not (tea and coffee)" means "no tea, or no coffee, or neither".',
             'work': 'Database filters and spreadsheet conditions (AND, OR, NOT) are set operations. Getting De Morgan wrong is a classic cause of a filter that silently drops records.'},
            {'id': 'c5', 'title': 'Venn diagrams and counting',
             'body': ['Two sets: n(A ∪ B) = n(A) + n(B) − n(A ∩ B). Only A = n(A) − n(A ∩ B).',
                      'Three sets: n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A ∩ B) − n(B ∩ C) − n(A ∩ C) + n(A ∩ B ∩ C).',
                      'Only A = n(A) − n(A ∩ B) − n(A ∩ C) + n(A ∩ B ∩ C). Exactly two = (sum of pairwise intersections) − 3 × n(A ∩ B ∩ C). None = n(U) − n(A ∪ B ∪ C).',
                      'If any region comes out negative, or the total exceeds n(U), the data are inconsistent.'],
             'blocks': [table(['Region (three sets)', 'Formula'], [['All three', 'n(A ∩ B ∩ C)'], ['A and B only', 'n(A ∩ B) − n(A ∩ B ∩ C)'], ['A only', 'n(A) − n(A ∩ B) − n(A ∩ C) + n(A ∩ B ∩ C)'], ['None', 'n(U) − n(A ∪ B ∪ C)']])],
             'analogy': 'Overlapping circles of friends at a party: people in two circles get counted twice unless you subtract the overlap once.',
             'work': 'Customer surveys, overlapping debtor lists and duplicate-vendor checks in audits are all Venn problems. A negative region is how auditors detect a fabricated survey.'},
            {'id': 'c6', 'title': 'Ordered pairs and the Cartesian product',
             'body': ['An ordered pair (a, b) has a first and a second element; (a, b) = (c, d) only when a = c and b = d, so (1, 2) ≠ (2, 1).',
                      'A × B = {(a, b) : a ∈ A, b ∈ B}. n(A × B) = n(A) × n(B). In general A × B ≠ B × A, though both have the same number of elements. If either set is empty, A × B = ∅.',
                      'A × B × C is the set of ordered triples, with n(A) × n(B) × n(C) elements.'],
             'analogy': 'A menu with 3 starters and 4 mains gives 12 (starter, main) meal pairs — the Cartesian product.',
             'work': 'Every row of a pivot table is an element of a Cartesian product (branch × month, product × region).'},
            {'id': 'c7', 'title': 'Relations: domain, range, inverse and types',
             'body': ['A relation from A to B is any subset of A × B. Since A × B has mn pairs, there are 2ᵐⁿ relations from A to B.',
                      'Domain = set of first elements; range = set of second elements. The inverse relation R⁻¹ reverses every pair, so domain of R⁻¹ = range of R and range of R⁻¹ = domain of R. The identity relation on A is {(a, a) : a ∈ A}.',
                      'A relation R on a set S is reflexive if (a, a) ∈ R for every a in S; symmetric if (a, b) ∈ R always gives (b, a) ∈ R; transitive if (a, b) ∈ R and (b, c) ∈ R always give (a, c) ∈ R.',
                      'A relation that is reflexive, symmetric and transitive is an equivalence relation — e.g. "is equal to", "is parallel to" (counting a line as parallel to itself), "has the same birthday as".'],
             'analogy': '"Is a sibling of" is symmetric but not reflexive (you are not your own sibling); "is an ancestor of" is transitive but not symmetric.',
             'work': 'Grouping ledger accounts by "belongs to the same group as" is an equivalence relation — it splits the chart of accounts into non-overlapping groups.'},
            {'id': 'c8', 'title': 'Functions (mappings) and their types',
             'body': ['A function f : A → B is a relation in which every element of A has exactly one image in B. A is the domain, B the co-domain, and the set of actual images f(A) is the range (a subset of B).',
                      'One-one (injective): different elements have different images, i.e. f(x₁) = f(x₂) ⇒ x₁ = x₂. Many-one: at least two elements share an image.',
                      'Onto (surjective): every element of B has at least one pre-image, i.e. range = co-domain. Into: at least one element of B has no pre-image. One-one and onto together = bijective.',
                      'Identity function I(x) = x (a bijection of A onto A). Constant function: every element has the same image. Equal functions: same domain and f(x) = g(x) for every x.',
                      'Composite: (g∘f)(x) = g(f(x)) — apply f first; in general g∘f ≠ f∘g. Inverse f⁻¹ exists only when f is one-one and onto, and then f⁻¹ is also one-one and onto. Number of functions from an m-element set to an n-element set = nᵐ.'],
             'analogy': 'A function is a vending machine: each button gives exactly one item. Two buttons may give the same item (many-one), and some items may not be on any button (into).',
             'work': 'A good master-data mapping (employee → employee code) must be one-one; a mapping of ledgers to financial-statement lines is many-one and should be onto so no line is left empty.'},
            {'id': 'c9', 'title': 'Limit of a function',
             'body': ['lim f(x) as x → a = l means f(x) gets as close to l as we like when x is taken close enough to a (but not equal to a). The value f(a) itself does not matter for the limit.',
                      'Left-hand limit (x → a⁻, i.e. lim f(a − h) as h → 0, h > 0) and right-hand limit (x → a⁺, lim f(a + h)). The limit exists only when both exist and are equal.',
                      'Algebra of limits (when lim f = l and lim g = m are finite): the limit of a sum, difference, product or constant multiple is the sum, difference, product or constant multiple of the limits; lim f/g = l/m if m ≠ 0; lim c = c.',
                      'Standard results: lim (xⁿ − aⁿ)/(x − a) = n aⁿ⁻¹ (x → a); lim (eˣ − 1)/x = 1, lim (aˣ − 1)/x = logₑ a, lim logₑ(1 + x)/x = 1 and lim (1 + x)^(1/x) = e (all as x → 0).',
                      'Methods: substitute first; if you get 0/0, factorise and cancel or use a standard result; as x → ∞, divide numerator and denominator by the highest power of x.'],
             'analogy': 'Walking towards a closed door: the limit is where you are heading, even if you never step through it — and you must arrive at the same spot whether you come from the left or the right corridor.',
             'work': 'Marginal cost and marginal revenue in the next chapter are limits of average changes; understanding limits is what makes the derivative meaningful.'},
            {'id': 'c10', 'title': 'Continuity at a point',
             'body': ['f is continuous at x = a if (i) f(a) is defined, (ii) lim f(x) as x → a exists (LHL = RHL), and (iii) that limit equals f(a). If any condition fails, f is discontinuous at a.',
                      'Polynomials are continuous everywhere; a rational function is continuous wherever its denominator is not zero. Sums, differences, products and quotients (non-zero denominator) of continuous functions are continuous.',
                      'For a function defined piece by piece, test the joining point: compute LHL with the left formula, RHL with the right formula and compare with the defined value. A change of formula alone does not make a function discontinuous.'],
             'analogy': 'A continuous graph can be drawn without lifting your pen. A jump in a tax-slab chart is a point where you must lift the pen.',
             'work': 'Slab-based tax or tariff schedules are often discontinuous at the slab limits; marginal relief provisions exist precisely to smooth such jumps.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Set operations and De Morgan\'s laws', 'difficulty': 'core', 'minutes': 6,
             'q': 'U = {1, 2, …, 12}, A = {2, 4, 6, 8, 10, 12}, B = {3, 6, 9, 12}. Find A ∪ B, A ∩ B, A − B, B − A and B′, and verify both De Morgan\'s laws.',
             'solution': [table(['Set', 'Elements'], [['A ∪ B', fs(AuB)], ['A ∩ B', fs(AnB)], ['A − B', fs(AmB)], ['B − A', fs(BmA)], ["B′", fs(Bc)],
                                                     ["(A ∪ B)′", fs(lhs)], ["A′ ∩ B′", fs(rhs)], ["(A ∩ B)′", fs(lhs2)], ["A′ ∪ B′", fs(rhs2)]]),
                          p('(A ∪ B)′ and A′ ∩ B′ have the same elements, and so do (A ∩ B)′ and A′ ∪ B′ — both laws verified. Also n(A ∪ B) = 6 + 4 − 2 = 8.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Three-set survey of a CA firm\'s clients', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'A CA firm has 200 clients. 120 use its GST service (G), 90 income-tax service (I) and 70 audit service (A); 50 use G and I, 30 use I and A, 25 use G and A, and 15 use all three. How many clients use (a) none of the three, (b) GST only, (c) exactly one service, (d) exactly two services?',
             'solution': [wn('Fill the Venn diagram from the centre', 'All three = 15. G and I only = 50 − 15 = 35; I and A only = 30 − 15 = 15; G and A only = 25 − 15 = 10.'),
                          table(['Region', 'Working', 'Clients'], [
                              ['G only', '120 − 35 − 10 − 15', str(only_G)], ['I only', '90 − 35 − 15 − 15', str(only_I)], ['A only', '70 − 15 − 10 − 15', str(only_A)],
                              ['G and I only', '50 − 15', str(GI_only)], ['I and A only', '30 − 15', str(IA_only)], ['G and A only', '25 − 15', str(GA_only)],
                              ['All three', 'given', str(GIA)], ['At least one service', '', str(union)]], num=[2], total=True),
                          p(f'(a) None = 200 − {union} = {tot - union}. (b) GST only = {only_G}. (c) Exactly one = {only_G} + {only_I} + {only_A} = {only_G + only_I + only_A}. (d) Exactly two = 35 + 15 + 10 = {GI_only + IA_only + GA_only}.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Power set and Cartesian product', 'difficulty': 'core', 'minutes': 5,
             'q': 'A = {p, q, r} and B = {1, 2}. (a) List the power set of A and count its proper subsets. (b) Write A × B. (c) If n(C) = 4, find n(A × B × C). (d) How many relations are there from A to B?',
             'solution': [p(f'(a) P(A) = {{{sub_txt}}} — 2³ = 8 subsets; proper subsets = 8 − 1 = 7.'),
                          p('(b) A × B = {' + ', '.join(f'({a}, {b})' for a, b in AxB) + '} — 6 ordered pairs.'),
                          p('(c) n(A × B × C) = 3 × 2 × 4 = 24.'),
                          p('(d) Each of the 6 pairs of A × B may be in or out of a relation: 2⁶ = 64 relations.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Testing relations on S = {1, 2, 3}', 'difficulty': 'moderate', 'minutes': 8,
             'q': f'Examine each relation on S = {{1, 2, 3}} for reflexivity, symmetry and transitivity: R₁ = {fr(R1)}; R₂ = {fr(R2)}; R₃ = {fr(R3)}. Also find the domain, range and inverse of R₂.',
             'solution': [table(['Relation', 'Pairs', 'Reflexive', 'Symmetric', 'Transitive', 'Equivalence'], rows4),
                          wn('Reasons', 'R₂: (1, 1) missing → not reflexive; (1, 2) present but (2, 1) absent → not symmetric; the only chain (1, 2), (2, 3) needs (1, 3), which is present → transitive. R₃: (2, 3) and (3, 1) present but (2, 1) absent → not transitive; (3, 2) absent → not symmetric. R₁ passes all three tests, so it is an equivalence relation.'),
                          p(f'For R₂: domain = {fs(dom2)}, range = {fs(ran2)}, R₂⁻¹ = {fr(R2inv)}.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Classifying functions; composite and inverse', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Classify: (a) f : N → N, f(x) = 2x; (b) f : R → R, f(x) = 3x + 5; (c) f : R → R, f(x) = x². (d) If f(x) = x + 2 and g(x) = x², find g(f(3)) and f(g(3)). (e) Find f⁻¹ for (b) and f⁻¹(20).',
             'solution': [table(['Function', 'One-one?', 'Onto?', 'Type'], [
                 ['2x on N', 'Yes — 2x₁ = 2x₂ gives x₁ = x₂', 'No — odd numbers have no pre-image', 'One-one, into'],
                 ['3x + 5 on R', 'Yes', 'Yes — any y has pre-image (y − 5)/3', 'Bijection'],
                 ['x² on R', 'No — f(3) = f(−3)', 'No — negatives have no pre-image', 'Many-one, into']]),
                 p('(d) g(f(3)) = g(5) = 25, while f(g(3)) = f(9) = 11 — so g∘f ≠ f∘g.'),
                 p('(e) y = 3x + 5 → x = (y − 5)/3, so f⁻¹(x) = (x − 5)/3 and f⁻¹(20) = 15/3 = 5. Only (b) has an inverse, because only (b) is one-one and onto.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Evaluating limits; when a limit fails to exist', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Evaluate (a) lim (x² − 9)/(x − 3) as x → 3; (b) lim (x⁵ − 32)/(x − 2) as x → 2; (c) lim (3x² + 5x)/(6x² − 1) as x → ∞. (d) f(x) = 2x + 3 for x < 2 and f(x) = x² for x ≥ 2. Does lim f(x) exist as x → 2?',
             'solution': [p('(a) Substitution gives 0/0. Factorise: (x − 3)(x + 3)/(x − 3) = x + 3 → 6.'),
                          p('(b) Standard result with n = 5, a = 2: 5 × 2⁴ = 80.'),
                          p('(c) Divide by x²: (3 + 5/x)/(6 − 1/x²) → 3/6 = 1/2.'),
                          p('(d) LHL = 2(2) + 3 = 7; RHL = 2² = 4. They are unequal, so the limit does not exist at x = 2 (even though f(2) = 4 is defined).')],
             'checks': c6},
            {'id': 'i7', 'title': 'Continuity and a standard exponential limit', 'difficulty': 'moderate', 'minutes': 6,
             'q': '(a) f(x) = (x² − 16)/(x − 4) for x ≠ 4 and f(4) = k. Find k so that f is continuous at x = 4. (b) Evaluate lim (e³ˣ − 1)/x as x → 0. (c) Is g(x) = x² − 2x + 3 continuous at x = 1?',
             'solution': [p('(a) lim (x² − 16)/(x − 4) = lim (x + 4) = 8. Continuity needs f(4) = 8, so k = 8.'),
                          p('(b) Put t = 3x: (e³ˣ − 1)/x = 3 × (eᵗ − 1)/t → 3 × 1 = 3.'),
                          p('(c) A polynomial is continuous everywhere: lim g(x) as x → 1 = 1 − 2 + 3 = 2 = g(1). Yes.')],
             'checks': c7},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Cross-selling analysis for a bank branch', 'role': 'Management trainee in a bank\'s internal audit team',
             'situation': 'A branch reports 480 customers: 310 have a loan (L), 260 a fixed deposit (D), 150 a credit card (C); 140 have L and D, 90 have D and C, 70 have L and C, and 40 have all three. The branch claims every customer holds at least one product.',
             'steps': ['Use the three-set formula: n(L ∪ D ∪ C) = 310 + 260 + 150 − 140 − 90 − 70 + 40 = 460.',
                       f'Customers with none = 480 − 460 = {j_none}, so the claim is wrong.',
                       f'Loan only = 310 − 140 − 70 + 40 = {j_onlyL} — a target list for deposit cross-selling.',
                       'Check that no region is negative; if one were, the underlying data would be inconsistent and need investigation.'],
             'takeaway': 'A Venn diagram is a quick consistency test for overlapping data.',
             'checks': cj1},
            {'id': 'j2', 'title': 'Is the mapping of ledgers a proper function?', 'role': 'Accounts executive migrating to a new ERP',
             'situation': 'Each old ledger code must be mapped to a new ledger code. The import file shows one old code mapped to two new codes, and two new codes with no old code mapped to them.',
             'steps': ['A mapping is a function only if every old code has exactly one new code — the code with two targets breaks this and must be fixed.',
                       'New codes with no old code mean the mapping is into, not onto. That is acceptable for new ledgers created fresh, but should be confirmed.',
                       'If you need to trace back from new to old (an inverse), the mapping must be one-one and onto; otherwise several old ledgers merge and history is lost.'],
             'takeaway': 'Function types are a practical checklist for any data-mapping exercise: exactly one image, one-one for reversibility, onto for completeness.'},
        ],
        'mcqs': M,
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'An inspector examined 100 units from an assembly line and reported: strength defect (S) 40, flexibility defect (F) 35, radius defect (R) 25, S and F 12, S and R 10, F and R 8, all three 4. Find the number of units with (a) no defect, (b) exactly one defect, (c) exactly two defects, (d) only a radius defect. Is the report consistent?',
             'model': [table(['Region', 'Working', 'Units'], [
                 ['All three', 'given', '4'], ['S and F only', '12 − 4', '8'], ['S and R only', '10 − 4', '6'], ['F and R only', '8 − 4', '4'],
                 ['S only', '40 − 12 − 10 + 4', str(q_oS)], ['F only', '35 − 12 − 8 + 4', str(q_oF)], ['R only', '25 − 10 − 8 + 4', str(q_oR)],
                 ['No defect', f'100 − {q_union}', str(q_none)], ['Total', '', '100']], num=[2], total=True),
                 p(f'(a) {q_none}; (b) {q_oS} + {q_oF} + {q_oR} = {q_one}; (c) 8 + 6 + 4 = {q_two}; (d) {q_oR}. Every region is non-negative and the regions add up to 100, so the report is consistent.')],
             'scheme': [{'id': 's1', 'pt': 'n(S ∪ F ∪ R) = 74 by the three-set formula', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Pairwise-only regions found by subtracting the centre', 'm': 1, 'skill': 'analysis'},
                        {'id': 's3', 'pt': 'Single-defect regions 22, 19, 11 and answers (a)–(d)', 'm': 2, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Consistency conclusion (no negative region; regions add to 100)', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Candidates who start from the centre of the Venn diagram rarely go wrong.', 'Many forget to add back the triple overlap for the "only" regions.'],
             'mistakes': ['Taking "exactly two" as 12 + 10 + 8 = 30 (the triple overlap is inside each pair).', 'Treating the report as inconsistent because the defect counts add to more than 100.'],
             'tips': ['Draw the diagram and write every region inside it before answering.', 'End with a one-line consistency check — it often earns the last mark.'],
             'checks': qc1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Let A = {1, 2, 3, 6} and R be the relation on A defined by "a R b if a divides b". (a) List R in roster form. (b) State its domain and range. (c) Is R reflexive, symmetric, transitive? Is it an equivalence relation? (d) How many relations in all can be defined on A?',
             'model': [p(f'(a) R = {fr(RD)} — {len(RD)} pairs.'),
                       p('(b) Domain = {1, 2, 3, 6}; range = {1, 2, 3, 6}.'),
                       p('(c) Reflexive: every number divides itself — yes. Symmetric: 1 divides 2 but 2 does not divide 1 — no. Transitive: if a divides b and b divides c, then a divides c — yes. Since it is not symmetric, R is not an equivalence relation.'),
                       p('(d) A × A has 16 pairs, so the number of relations on A is 2¹⁶ = 65,536.')],
             'scheme': [{'id': 's1', 'pt': 'All 9 pairs listed correctly', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Domain and range', 'm': 0.5, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Each property decided with a reason or counter-example', 'm': 1.5, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'Not an equivalence relation — conclusion stated', 'm': 0.5, 'skill': 'conclusion'},
                        {'id': 's5', 'pt': '2¹⁶ relations', 'm': 1, 'skill': 'computation'}],
             'remarks': ['A single counter-example is enough to show a property fails; a general reason is needed to show it holds.', 'Several candidates omit the pairs (a, a) when listing R.'],
             'mistakes': ['Missing (1, 1), (2, 2), … in the list.', 'Calling R symmetric because (1, 1) "reverses to itself".', 'Writing 2⁴ relations instead of 2¹⁶.'],
             'tips': ['Test properties in the order reflexive → symmetric → transitive.', 'For "not" answers, quote the failing pair.'],
             'checks': qc2},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': '(a) Evaluate lim (x³ − 27)/(x² − 9) as x → 3. (b) Evaluate lim (2x³ − x + 7)/(5x³ + 4x²) as x → ∞. (c) f(x) = kx + 1 for x ≤ 2 and f(x) = 3x − 1 for x > 2. Find k so that f is continuous at x = 2, and show the three continuity conditions.',
             'model': [p('(a) 0/0 form. Factorise: (x − 3)(x² + 3x + 9) / [(x − 3)(x + 3)] = (x² + 3x + 9)/(x + 3) → 27/6 = 9/2 = 4.5.'),
                       p('(b) Divide by x³: (2 − 1/x² + 7/x³)/(5 + 4/x) → 2/5 = 0.4.'),
                       p('(c) f(2) = 2k + 1 (defined). LHL = lim (kx + 1) = 2k + 1. RHL = lim (3x − 1) = 5. Continuity requires LHL = RHL = f(2): 2k + 1 = 5 → k = 2. Then f(2) = 5 = LHL = RHL, so all three conditions hold.')],
             'scheme': [{'id': 's1', 'pt': '(a) 0/0 recognised and factorisation correct', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': '(a) Answer 9/2', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(b) Division by highest power; answer 2/5', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': '(c) LHL, RHL and f(2) written separately', 'm': 1.5, 'skill': 'application'},
                        {'id': 's5', 'pt': '(c) k = 2 with the conditions verified', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['In (a) some candidates "cancel" x³ with x² — not allowed; factorise first.', 'For (c), examiners look for all three conditions, not just an equation.'],
             'mistakes': ['Answering 0 or "not defined" in (a) after direct substitution.', 'Dividing only the numerator by x³ in (b).'],
             'tips': ['Always try substitution first and write the form you get (0/0, ∞/∞).', 'For piecewise functions, write "LHL = … , RHL = … , f(a) = …" on separate lines.'],
             'checks': qc3},
        ],
        'revision': {
            'summary': ['Set = well-defined collection of distinct objects; roster or set-builder form.', 'Subsets 2ⁿ, proper subsets 2ⁿ − 1, n(P(A)) = 2ⁿ; ∅ ⊆ every set.',
                        'n(A ∪ B) = n(A) + n(B) − n(A ∩ B); three-set formula adds back the triple overlap.', 'De Morgan: (A ∪ B)′ = A′ ∩ B′; (A ∩ B)′ = A′ ∪ B′.',
                        'n(A × B) = n(A)n(B); relations from A to B: 2ᵐⁿ.', 'Equivalence = reflexive + symmetric + transitive.',
                        'Function: each element of the domain has exactly one image. Bijection = one-one + onto; only bijections have inverses. Functions from m to n elements: nᵐ.',
                        'Limit exists ⇔ LHL = RHL; continuity ⇔ f(a) defined and lim f(x) = f(a).', 'lim (xⁿ − aⁿ)/(x − a) = n aⁿ⁻¹; lim (eˣ − 1)/x = 1; lim (aˣ − 1)/x = logₑ a.'],
            'remember': ['Equal sets ⇒ equivalent, not conversely.', 'Exactly two = Σ pairs − 3 × all three.', 'g∘f means f first, then g.', 'As x → ∞, divide by the highest power.'],
            'traps': ['{ 0 } is not the empty set.', 'A − B ≠ B − A.', 'A relation can be symmetric and transitive yet not reflexive.', 'A limit can exist even if f(a) is undefined; continuity needs both and equality.'],
        },
        'quickref': [
            {'k': 'Subsets', 'v': '2ⁿ; proper 2ⁿ − 1; power set has 2ⁿ elements'},
            {'k': 'Two sets', 'v': 'n(A ∪ B) = n(A) + n(B) − n(A ∩ B)'},
            {'k': 'Three sets', 'v': 'ΣA − Σ(pairs) + n(A ∩ B ∩ C)'},
            {'k': 'De Morgan', 'v': "(A ∪ B)′ = A′ ∩ B′; (A ∩ B)′ = A′ ∪ B′"},
            {'k': 'Cartesian product', 'v': 'n(A × B) = n(A) · n(B); relations 2ᵐⁿ'},
            {'k': 'Equivalence relation', 'v': 'Reflexive, symmetric and transitive'},
            {'k': 'Function types', 'v': 'one-one, many-one, onto, into; bijection = one-one + onto'},
            {'k': 'Number of functions', 'v': 'nᵐ (m elements to n elements); one-one: ⁿPₘ'},
            {'k': 'Limit exists', 'v': 'LHL = RHL (finite)'},
            {'k': 'Standard limits', 'v': '(xⁿ − aⁿ)/(x − a) → n aⁿ⁻¹; (eˣ − 1)/x → 1; (aˣ − 1)/x → logₑ a; (1 + x)^(1/x) → e'},
            {'k': 'Continuity at a', 'v': 'f(a) defined, limit exists, limit = f(a)'},
        ],
        'viva': VIVA,
        'cases': [{
            'id': 'k1', 'title': 'Return-filing survey for a tax-practice newsletter', 'difficulty': 'moderate',
            'case': ('A tax practitioner surveyed 300 individual taxpayers. 210 filed their return online themselves, 150 took the help of a CA, and 90 did both (filed online and also consulted a CA). '
                     'The newsletter wants a few headline figures.'),
            'mcqs': [
                mq('k1a', 'How many taxpayers neither filed online nor consulted a CA?', k_n, [60, 0, 90], "Taxpayers who used at least one = 210 + 150 − 90 = 270 (the 90 in both are counted once). Those who used neither = 300 − 270 = 30. The trap is 0, which adds 210 + 150 = 360 and concludes everyone is covered, forgetting the overlap. In practice: a tax practitioner's newsletter might highlight this 'neither' group — taxpayers who may not have filed at all — as a target for outreach.", 'c5', 'core', '300-(210+150-90)', topic='Venn diagrams and counting'),
                mq('k1b', 'How many filed online without consulting a CA?', k_o, [210, 60, 90], "Of the 210 who filed online, 90 also consulted a CA. Online only = 210 − 90 = 120. The trap is 210, which is everyone who filed online, including those who also took a CA's help. In practice: separating 'only' groups from overlaps tells a practice which taxpayers handle compliance themselves — a different market from those who already consult a CA.", 'c5', 'core', '210-90', topic='Venn diagrams and counting'),
                mq('k1c', 'How many used exactly one of the two?', k_e, [270, 90, 120], "Exactly one means online only or CA only. Online only = 210 − 90 = 120; CA only = 150 − 90 = 60; total = 180. The trap is 270, which is 'at least one' and includes the 90 who used both. In practice: survey reports distinguish 'exactly one' from 'at least one', and mixing them up is a common error in market-research summaries.", 'c5', 'moderate', '(210-90)+(150-90)', topic='Venn diagrams and counting'),
                mq('k1d', 'What percentage of all those surveyed consulted a CA but did not file online?', '20%', ['50%', '30%', '40%'], "CA only = 150 − 90 = 60 taxpayers. As a percentage of all 300 surveyed: 60/300 × 100 = 20%. The trap is 40%, which divides 60 by the 150 who consulted a CA rather than by all 300 surveyed; 50% is 150/300, which includes those who also filed online. In practice: always check the base of a percentage — 'of all taxpayers' versus 'of CA clients' changes the headline figure.", 'c5', 'moderate', '(150-90)/300*100', topic='Venn diagrams and counting'),
            ]}],
    }


VIVA = [
    V('v1', 'What is the difference between equal sets and equivalent sets?',
      'Equal sets have exactly the same elements. Equivalent sets only have the same number of elements, so their cardinal numbers are equal, but the elements can be different. Every pair of equal sets is equivalent, but equivalent sets need not be equal.',
      [P('p1', 'Equal sets: exactly the same elements', 4, 'equal set same element|equal same element|equal set identical|equal identical element|equal exactly same|equal set exactly|equal set have same element|equal set contain same', min=1),
       P('p2', 'Equivalent sets: same number of elements (n(A) = n(B))', 4, 'equivalent same number|equivalent number of element|equivalent set same number|equivalent cardinal|equivalent set same cardinal|equivalent same count|equivalent same size|equivalent n a equal n b|equivalent set have same number|equivalent equal number', min=1),
       P('p3', 'Equal ⇒ equivalent, but not the other way round', 2, 'equal set always equivalent|equal always equivalent|equal sets are equivalent|equal set are equivalent|equivalent need not equal|equivalent not necessarily equal|equivalent not always equal|equivalent may not equal|equivalent need not be equal|not every equivalent|converse not true|converse is not true|not vice versa', min=1)], 'c2'),
    V('v2', 'How many subsets does a set of n elements have, and why?',
      'A set with n elements has two to the power n subsets, because while forming a subset each element can either be included or left out, giving two choices for every element. Leaving out the set itself, there are two to the power n minus one proper subsets.',
      [P('p1', '2ⁿ subsets', 4, '2 power n|two power n|2 to power n|two to the power n|2 to the n|two to the n|2^n|2 raised n|two raised n|2 n subset|two n subset'),
       P('p2', 'Each element either in or out — two choices each', 4, 'include|in or out|taken or left|either|two choice|2 choice|two option|2 option|chosen or not|select or not|present or absent', min=1),
       P('p3', 'Proper subsets 2ⁿ − 1', 2, '2 power n minus 1|two power n minus one|2 to the power n minus 1|two to the power n minus one|2^n minus 1|2^n - 1|2 n minus 1|two n minus one', min=1)], 'c3'),
    V('v3', 'State De Morgan\'s laws.',
      'De Morgan\'s laws say that the complement of the union of two sets is the intersection of their complements, and the complement of the intersection of two sets is the union of their complements. In symbols, A union B whole complement equals A complement intersection B complement, and A intersection B whole complement equals A complement union B complement.',
      [P('p1', '(A ∪ B)′ = A′ ∩ B′', 5, 'complement of union is intersection|complement of the union is the intersection|complement union intersection complement|complement of union equal intersection|union complement equal intersection|union whole complement equal a complement intersection|a union b complement equal a complement intersection b complement|not a or b equal not a and not b|complement of a union b is a complement intersection', min=1),
       P('p2', '(A ∩ B)′ = A′ ∪ B′', 5, 'complement of intersection is union|complement of the intersection is the union|complement intersection union complement|complement of intersection equal union|intersection complement equal union|intersection whole complement equal a complement union|a intersection b complement equal a complement union b complement|not a and b equal not a or not b|complement of a intersection b is a complement union', min=1)], 'c4'),
    V('v4', 'When is a relation called an equivalence relation? Explain each property.',
      'A relation on a set is an equivalence relation when it is reflexive, symmetric and transitive. Reflexive means every element is related to itself. Symmetric means if a is related to b then b is related to a. Transitive means if a is related to b and b is related to c, then a is related to c.',
      [P('p1', 'Reflexive, symmetric and transitive', 4, 'reflexive', 'symmetric', 'transitive'),
       P('p2', 'Reflexive: every element related to itself, (a, a) ∈ R', 2, 'related to itself|relate itself|itself|own self|with itself', min=1),
       P('p3', 'Symmetric: a R b ⇒ b R a', 2, 'b related to a|b relate a|b r a|b is related to a|then b a|reverse|vice versa|both way', min=1),
       P('p4', 'Transitive: a R b and b R c ⇒ a R c', 2, 'a related to c|a relate c|a r c|a is related to c|then a c|chain|a to c', min=1)], 'c7'),
    V('v5', 'Distinguish between a one-one function and an onto function. When does a function have an inverse?',
      'In a one-one function different elements of the domain always have different images, so no two elements share an image. In an onto function every element of the co-domain has at least one pre-image, so the range equals the co-domain. A function has an inverse only when it is both one-one and onto, that is, a bijection.',
      [P('p1', 'One-one: different elements have different images', 4, 'different element different image|distinct element distinct image|different input different output|no two element same image|no two share|different images|distinct image|different output|no two have same image|unique image', min=1),
       P('p2', 'Onto: every element of the co-domain has a pre-image (range = co-domain)', 3, 'every element of co domain|every element codomain|each element of co domain|every element in co domain|range equal co domain|range equal codomain|range is co domain|range same as co domain|range is the codomain|every element of b|pre image|preimage|nothing left out|no element left', min=1),
       P('p3', 'Inverse exists only for one-one and onto (bijective) functions', 3, 'bijection|bijective|one one and onto|one-one and onto|one one onto|both one one and onto|injective and surjective', min=1)], 'c8'),
    V('v6', 'When does the limit of a function exist at a point, and when is the function continuous there?',
      'The limit of f of x as x tends to a exists when the left-hand limit and the right-hand limit both exist and are equal. The function is continuous at a when f of a is defined, the limit exists, and the limit equals the value f of a.',
      [P('p1', 'Limit exists when LHL and RHL exist and are equal', 5, 'left hand|left-hand|lhl|left limit|from the left', 'right hand|right-hand|rhl|right limit|from the right', 'equal|same|agree|match|coincide', min=3),
       P('p2', 'Continuous: f(a) defined and limit equals f(a)', 5, 'limit equal f a|limit equals f of a|limit equal value|limit is equal to f a|limit same as f a|limit equal function value|equal to value of function|limit equal f(a)|equal f of a|equal to f a|equals the value|value equal limit|f a equal limit|f of a equal limit|f of a equals the limit', 'defined|exist|finite', min=2)], 'c10'),
]
