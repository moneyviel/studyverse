"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 5 Basic Concepts of Permutations and Combinations.
Original explanations, numbers and questions (scope and order follow the ICAI study material).
Every count is computed here (math.perm / math.comb) and stored with an arithmetic check the validator re-evaluates."""
from math import comb, factorial, perm
from lib import *
import re
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch05-u01'


# ---------- small helpers (expressions only use + - * / so ca_validate can re-evaluate them) ----------
def fe(n):
    """n! written out as a product."""
    return '*'.join(str(i) for i in range(n, 0, -1)) if n > 1 else '1'


def pe(n, r):
    """nPr written out: n(n-1)...(n-r+1)."""
    return '*'.join(str(n - i) for i in range(r)) if r > 0 else '1'


def ce(n, r):
    """nCr written out: nPr / r!"""
    r = min(r, n - r)
    return f'({pe(n, r)})/({"*".join(str(i) for i in range(1, r + 1))})' if r > 0 else '1'


def ev(expr):
    v = eval(expr, {'__builtins__': {}}, {'round': round})
    v = round(v, 2)
    return int(v) if v == int(v) else v


def fmt(x):
    if isinstance(x, str): return x
    if isinstance(x, float) and x != int(x): return f'{x:g}'
    return inr(int(x))


def mq(mid, q, right, wrong, explain, concept, diff='core', check=None, topic=None):
    """MCQ with the key placed by a fixed rule (UI shuffles anyway); numeric keys are verified against `check`."""
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


def build():
    # ------------------------------------------------------------------ verified counts
    # Illustration 1: factorial equations
    c1 = Checks()
    c1.add('9*8', '(n+2)(n+1) for n = 7')
    x1 = c1.add('(9*8*7*6*5*4*3*2*1)*(1/(7*6*5*4*3*2*1)+1/(8*7*6*5*4*3*2*1))', 'x in 1/7! + 1/8! = x/9!')
    assert x1 == 81
    c1.add(f'({fe(10)})/(({fe(4)})*({fe(6)}))', '10!/(4! 6!) = 10C4')

    # Illustration 2: four-digit numbers from 0,1,2,3,5,7 (no repetition) — brute force confirms
    from itertools import permutations as _perms
    digs = '012357'
    four = [int(''.join(t)) for t in _perms(digs, 4) if t[0] != '0']
    n_all, n_gt, n_even = len(four), sum(1 for v in four if v > 5000), sum(1 for v in four if v % 2 == 0)
    c2 = Checks()
    assert c2.add('5*5*4*3', 'all four-digit numbers: 5 choices for the first place (0 not allowed), then 5P3') == n_all == 300
    assert c2.add('2*5*4*3', 'greater than 5000: first digit 5 or 7, then 5P3') == n_gt == 120
    c2.add('5*4*3', 'even, ending in 0: first place 5 ways, then 4P2')
    c2.add('4*4*3', 'even, ending in 2: first place 4 ways (not 0, not 2), then 4P2')
    assert c2.add('5*4*3+4*4*3', 'even numbers in all') == n_even == 108

    # Illustration 3: AUDITOR (7 distinct letters; vowels A U I O; consonants D T R)
    c3 = Checks()
    w_all = c3.add(fe(7), '7! arrangements')
    w_vt = c3.add(f'({fe(4)})*({fe(4)})', 'vowels together: 4 units (block + D,T,R) × 4! inside the block')
    w_gap = c3.add(f'({fe(4)})*({pe(5, 3)})', 'no two consonants together: 4! vowels × 5P3 gaps')
    w_even = c3.add(f'({fe(3)})*({fe(4)})', 'consonants in the 3 even places: 3! × 4!')
    w_nvt = c3.add(f'{w_all}-{w_vt}', 'vowels not all together')
    word = 'AUDITOR'
    arr = list(_perms(word))
    assert len(arr) == w_all
    vow = set('AUIO')
    assert sum(1 for a in arr if max(i for i, ch in enumerate(a) if ch in vow) - min(i for i, ch in enumerate(a) if ch in vow) == 3) == w_vt
    assert sum(1 for a in arr if all(not (a[i] not in vow and a[i + 1] not in vow) for i in range(6))) == w_gap
    assert sum(1 for a in arr if all(a[i] not in vow for i in (1, 3, 5))) == w_even

    # Illustration 4: ACCOUNTANT — A2 C2 N2 T2 O U (10 letters)
    c4 = Checks()
    acc_all = c4.add(f'({fe(10)})/(2*2*2*2)', '10!/(2!2!2!2!)')
    acc_a = c4.add(f'({fe(9)})/(2*2*2)', 'starting with A: remaining 9 letters with C,N,T doubled')
    acc_ends = c4.add(f'({fe(8)})/(2*2*2)', 'starting and ending with A: middle 8 letters C,C,N,N,T,T,O,U')
    assert acc_all == factorial(10) // 16 and acc_a == factorial(9) // 8 and acc_ends == factorial(8) // 8 == 5040
    from collections import Counter as _C
    _w = 'ACCOUNTANT'; _cnt = _C(_w)
    _den = 1
    for _v in _cnt.values(): _den *= factorial(_v)
    assert factorial(len(_w)) // _den == acc_all

    # Illustration 5: circular arrangements
    c5 = Checks()
    r8 = c5.add(fe(7), '8 people at a round table: (8-1)!')
    r8t = c5.add(f'({fe(6)})*2', 'two particular people together: 7 units round the table (6!) × 2!')
    r8n = c5.add(f'{r8}-{r8t}', 'two particular people never together')
    neck = c5.add(f'({fe(8)})/2', 'necklace of 9 different beads: (9-1)!/2')

    # Illustration 6: committee of 5 from 6 men and 5 women with at least 2 women
    c6 = Checks()
    t2 = c6.add(f'({ce(5, 2)})*({ce(6, 3)})', '2 women and 3 men')
    t3 = c6.add(f'({ce(5, 3)})*({ce(6, 2)})', '3 women and 2 men')
    t4 = c6.add(f'({ce(5, 4)})*({ce(6, 1)})', '4 women and 1 man')
    t5 = c6.add(f'({ce(5, 5)})*1', '5 women')
    at2 = c6.add(f'{t2}+{t3}+{t4}+{t5}', 'at least 2 women — direct method')
    tot11 = c6.add(ce(11, 5), 'all committees of 5 from 11')
    c6.add(f'{tot11}-{ce(6, 5)}-5*({ce(6, 4)})', 'complement check: total − (no woman) − (exactly one woman)')
    assert at2 == sum(comb(5, k) * comb(6, 5 - k) for k in range(2, 6)) == 381

    # Illustration 7: geometry counts
    c7 = Checks()
    lines = c7.add(f'({ce(14, 2)})-({ce(5, 2)})+1', 'lines from 14 points, 5 collinear')
    tri = c7.add(f'({ce(14, 3)})-({ce(5, 3)})', 'triangles from 14 points, 5 collinear')
    dec = c7.add(f'({ce(10, 2)})-10', 'diagonals of a decagon')
    c7.add('12*(12-3)/2', 'n(n-3)/2 = 54 gives n = 12')

    # Illustration 8: using properties of nCr
    c8 = Checks()
    n16 = c8.add(ce(16, 2), '16C14 = 16C2')
    c8.add('720/120', 'r! = nPr / nCr')
    c8.add('10*9*8', '10P3 = 720 confirms n = 10')

    # Jobs
    cj1 = Checks()
    samp = cj1.add(ce(20, 4), 'ways to pick 4 vouchers out of 20')
    samp2 = cj1.add(f'({ce(12, 2)})*({ce(8, 2)})', '2 of 12 cash vouchers and 2 of 8 bank vouchers')
    cj2 = Checks()
    code_nr = cj2.add(f'({pe(26, 2)})*({pe(10, 3)})', '2 letters then 3 digits, no repetition')
    code_r = cj2.add('26*26*10*10*10', '2 letters then 3 digits, repetition allowed')
    otp = cj2.add('10*10*10*10*10*10', '6-digit OTP, any digit in any place')

    # Questions
    qc1 = Checks()
    q1_all = qc1.add('5*5*4', 'three-digit numbers from 0,2,4,5,6,9 without repetition')
    q1_0 = qc1.add('5*4', 'ending in 0: 5P2')
    q1_5 = qc1.add('4*4', 'ending in 5: first place 4 ways (not 0, not 5) × middle 4 ways')
    q1_t = qc1.add('5*4+4*4', 'divisible by 5')
    three = [int(''.join(t)) for t in _perms('024569', 3) if t[0] != '0']
    assert len(three) == q1_all and sum(1 for v in three if v % 5 == 0) == q1_t

    qc2 = Checks()
    q2a = qc2.add(f'({ce(7, 3)})*({ce(5, 3)})', '3 CAs and 3 CSs')
    q2b = qc2.add(f'({ce(7, 4)})*({ce(5, 2)})', '4 CAs and 2 CSs')
    q2t = qc2.add(f'{q2a}+{q2b}', 'panels with at least 3 CAs and at least 2 CSs')
    q2c = qc2.add(f'({ce(6, 2)})*({ce(5, 3)})', 'Mr. Iyer included — 3 CAs case')
    q2d = qc2.add(f'({ce(6, 3)})*({ce(5, 2)})', 'Mr. Iyer included — 4 CAs case')
    q2i = qc2.add(f'{q2c}+{q2d}', 'panels that include Mr. Iyer')

    qc3 = Checks()
    q3a = qc3.add(fe(9), 'INCOMETAX: 9 different letters')
    q3b = qc3.add(f'({fe(6)})*({fe(4)})', 'vowels together: 6 units × 4!')
    q3c = qc3.add(f'({fe(5)})*({pe(6, 4)})', 'no two vowels together: 5! × 6P4')
    q3d = qc3.add(f'({fe(9)})/({fe(4)})', 'vowels in the order I, O, E, A: 9!/4!')


    # Case set
    ck = Checks()
    k_a = ck.add(f'({ce(4, 2)})*({ce(6, 3)})', 'exactly 2 seniors and 3 assistants')
    k_b = ck.add(f'({ce(10, 5)})-({ce(6, 5)})', 'at least one senior = total − no senior')
    k_c = ck.add(fe(4), '5 people round a table: 4!')
    k_d = ck.add(f'({fe(4)})*2', '5 in a row with two particular seniors side by side')

    # ------------------------------------------------------------------ MCQs (each numeric key has a check)
    M = []
    M.append(mq('m1', 'The value of 8!/6! is:', 56, [2, 48, 1680], 'Expand only as far as needed: 8! = 8 × 7 × 6!, so 8!/6! = 8 × 7 = 56. The trap is 48, which multiplies 8 by 6 as if the factorials could be dropped; 2 does the same and divides 8 by 6 roughly. Factorials cancel as blocks, not as single numbers. In practice: cancelling factorials before multiplying keeps numbers small, which is how an analyst computes large counts like possible audit-sample combinations without overflowing a calculator.', 'c2', 'core', '8*7', topic='Factorial notation'))
    M.append(mq('m2', 'The value of ⁷P₃ is:', 210, [35, 343, 21], 'ⁿPᵣ is the product of r consecutive numbers counting down from n: ⁷P₃ = 7 × 6 × 5 = 210. The trap is 35, which is ⁷C₃ — the number of selections, not arrangements (210 ÷ 3! = 35). 343 = 7³ allows repetition. In practice: if 3 of 7 audit assistants are to be assigned to three different branches, the order of assignment matters, so the count is ⁷P₃.', 'c3', 'core', pe(7, 3), topic='Permutations: arrangements where order matters'))
    M.append(mq('m3', 'By convention, 0! is taken as:', '1', ['0', 'Not defined', '∞'], '0! is defined as 1 so that formulas stay consistent: ⁿPₙ = n!/(n − n)! = n!/0! must equal n!, which works only if 0! = 1. The trap is 0 — but then the formula would involve division by zero. It also matches the fact that there is exactly one way to arrange nothing. In practice: spreadsheet functions like FACT(0) return 1, and probability and binomial models used by actuaries rely on this convention.', 'c2', 'core', topic='Factorial notation'))
    M.append(mq('m4', 'If ⁿP₂ = 90, the value of n is:', 10, [9, 45, 15], 'ⁿP₂ = n(n − 1) = 90. Since 10 × 9 = 90, n = 10 (the other root, −9, is rejected because n must be a positive integer). The trap is 9, which takes the smaller factor; 45 halves 90 as if it were ⁿC₂. In practice: working backwards from a count to the number of items — for example from the number of possible ordered pairings to the number of participants — is a common exam pattern.', 'c3', 'core', 'round((1+(1+4*90)**0.5)/2)', topic='Permutations: arrangements where order matters'))
    M.append(mq('m5', 'Six friends sit at a round table. The number of different seatings is:', 120, [720, 60, 360], 'In a circle there is no fixed starting seat, so fix one person and arrange the rest: (n − 1)! = 5! = 120. The trap is 720 = 6!, which treats the round table like a row and counts each rotation as a different seating. In practice: event planners and protocol officers use (n − 1)! when working out seating options for round-table board meetings or client dinners.', 'c4', 'core', fe(5), topic='Circular permutations'))
    M.append(mq('m6', 'The number of different necklaces that can be made with 7 beads, all of different colours, is:', 360, [720, 5040, 2520], 'Fix one bead to remove rotations: (7 − 1)! = 720. A necklace can also be flipped over, so clockwise and anticlockwise orders are the same, and we divide by 2: 720/2 = 360. The trap is 720, which forgets that turning the necklace over gives the same piece. In practice: jewellery designers and manufacturers counting distinct bead or stone patterns apply this halving rule.', 'c4', 'moderate', f'({fe(6)})/2', topic='Circular permutations'))
    M.append(mq('m7', 'The number of arrangements of the letters of the word SUCCESS is:', 420, [5040, 840, 210], "SUCCESS has 7 letters with S repeated 3 times and C repeated 2 times. Arrangements = 7!/(3! × 2!) = 5,040/12 = 420. The trap is 840, which divides only by 3! for the S's and forgets the repeated C's; 5,040 ignores repetition altogether. In practice: the same 'divide by repeats' rule counts distinct sequences when identical items are involved, such as orders of identical cartons on a dispatch line.", 'c6', 'moderate', f'({fe(7)})/(({fe(3)})*2)', topic='Alike things and repetition'))
    M.append(mq('m8', 'How many 3-letter codes can be formed from the letters A, B, C, D, E, F if letters may repeat?', 216, [120, 20, 18], 'With repetition allowed, each of the 3 positions can be filled in 6 ways independently: 6 × 6 × 6 = 216. The trap is 120 = ⁶P₃, which assumes letters cannot repeat; 20 = ⁶C₃ ignores order as well. In practice: the number of possible codes with repetition, like PINs or OTPs, is why IT auditors check code length — each extra character multiplies the possibilities.', 'c6', 'core', '6*6*6', topic='Alike things and repetition'))
    M.append(mq('m9', 'The value of ¹²C₁₀ is:', 66, [132, 2, 120], 'Use ⁿCᵣ = ⁿCₙ₋ᵣ: ¹²C₁₀ = ¹²C₂ = (12 × 11)/2 = 66. Choosing 10 to include is the same as choosing 2 to leave out. The trap is 132 = ¹²P₂, which forgets to divide by 2! for the order of the two items. In practice: choosing the 10 staff who stay on a project is the same as choosing the 2 who leave, a shortcut that saves time in counting.', 'c8', 'core', ce(12, 2), topic='Properties of ⁿCᵣ'))
    M.append(mq('m10', 'If ⁿC₈ = ⁿC₁₂, then ⁿC₁₇ equals:', 1140, [20, 6840, 190], 'If ⁿCₓ = ⁿCᵧ with x ≠ y, then x + y = n, so n = 8 + 12 = 20. Then ²⁰C₁₇ = ²⁰C₃ = (20 × 19 × 18)/6 = 1,140. The trap is 20, which stops after finding n; 6,840 = ²⁰P₃ forgets to divide by 3!. In practice: the symmetry property ⁿCᵣ = ⁿCₙ₋ᵣ is used constantly to simplify binomial calculations in probability and statistics.', 'c8', 'moderate', ce(20, 3), topic='Properties of ⁿCᵣ'))
    M.append(mq('m11', 'In how many ways can 4 auditors be chosen from a panel of 9?', 126, [3024, 36, 252], 'A team of 4 auditors is a selection, so order does not matter: ⁹C₄ = (9 × 8 × 7 × 6)/(4 × 3 × 2 × 1) = 126. The trap is 3,024 = ⁹P₄, which counts the same team once for every order in which it could be listed. In practice: audit firms choosing an engagement team from a panel are making combinations; only if each member got a distinct role would order matter.', 'c7', 'core', ce(9, 4), topic='Combinations: selections where order does not matter'))
    M.append(mq('m12', 'The number of ways of choosing one or more items from 6 different items is:', 63, [64, 720, 36], "Each of the 6 different items is either taken or left — 2 choices each — giving 2⁶ = 64 selections. Removing the one selection in which nothing is taken leaves 63. The trap is 64, which forgets that 'one or more' excludes the empty selection. In practice: a manager deciding which of 6 optional features to include in a product has 63 non-empty bundles to evaluate.", 'c9', 'core', '2**6-1', topic='Special selections: some or all, alike things, independent groups, geometry'))
    M.append(mq('m13', 'A basket has 3 identical apples, 4 identical oranges and 2 identical mangoes. In how many ways can at least one fruit be selected?', 59, [60, 23, 9], 'Identical items: apples can be chosen 0, 1, 2 or 3 at a time (4 ways), oranges in 5 ways and mangoes in 3 ways. Total = 4 × 5 × 3 = 60, minus the empty selection = 59. The trap is 60, which forgets to exclude taking no fruit at all; 23 treats the fruits as different. In practice: a retailer counting possible gift-hamper combinations from stocks of identical items uses this (n + 1) rule.', 'c9', 'moderate', '(3+1)*(4+1)*(2+1)-1', topic='Special selections: some or all, alike things, independent groups, geometry'))
    M.append(mq('m14', 'The number of diagonals of an octagon is:', 20, [28, 16, 40], "Any 2 of the 8 vertices define a line segment: ⁸C₂ = 28. Of these, 8 are sides, so diagonals = 28 − 8 = 20. The trap is 28, which counts all segments including the sides. General rule: n(n − 3)/2. In practice: the same 'pairs minus adjacent pairs' logic counts possible direct links in a network, such as courier routes between 8 branches excluding existing neighbour routes.", 'c9', 'core', f'({ce(8, 2)})-8', topic='Special selections: some or all, alike things, independent groups, geometry'))
    M.append(mq('m15', 'How many triangles can be formed by joining 12 points in a plane, no three of which are collinear?', 220, [1320, 66, 495], 'With no three points collinear, every choice of 3 points gives a triangle: ¹²C₃ = (12 × 11 × 10)/6 = 220. The trap is 1,320 = ¹²P₃, which counts each triangle 6 times by ordering its corners; 66 = ¹²C₂ counts lines, not triangles. In practice: counting triangles of points is the same as counting three-member groups, such as possible sub-committees of 3 from 12 members.', 'c9', 'core', ce(12, 3), topic='Special selections: some or all, alike things, independent groups, geometry'))
    M.append(mq('m16', 'At a meeting, each of 15 partners shakes hands once with every other partner. The number of handshakes is:', 105, [210, 225, 120], 'A handshake involves an unordered pair — A with B is the same as B with A — so the count is ¹⁵C₂ = (15 × 14)/2 = 105. The trap is 210 = ¹⁵P₂, which counts each handshake twice; 225 = 15² even lets people shake their own hand. In practice: this pair-counting rule tells a firm how many one-to-one review meetings are needed if every partner meets every other partner once.', 'c7', 'core', ce(15, 2), topic='Combinations: selections where order does not matter'))
    M.append(mq('m17', 'A committee of 3 men out of 7 and 2 women out of 5 can be formed in:', 350, [45, 792, 2100], 'Choose the men and the women independently, then multiply: ⁷C₃ × ⁵C₂ = 35 × 10 = 350. The trap is 45, which adds the two counts — but each choice of men can go with each choice of women. 792 = ¹²C₅ ignores the gender split. In practice: forming an Internal Complaints Committee or a board committee with fixed numbers from different groups is counted this way.', 'c9', 'core', f'({ce(7, 3)})*({ce(5, 2)})', topic='Special selections: some or all, alike things, independent groups, geometry'))
    M.append(mq('m18', 'Five books are arranged on a shelf. In how many arrangements are two particular books together?', 48, [24, 72, 120], "Tie the two particular books together as one unit: there are now 4 units, arranged in 4! = 24 ways. The two books can swap inside the bundle in 2! ways, so the total is 24 × 2 = 48. The trap is 24, which forgets that the two books can be in either order. In practice: scheduling two linked tasks back-to-back — say, an audit opening meeting and walkthrough — uses this 'treat as one block' method.", 'c5', 'core', f'({fe(4)})*2', topic='Permutations with restrictions'))
    M.append(mq('m19', 'In the previous question, in how many arrangements are the two particular books never together?', 72, [48, 96, 24], 'Use the complement: never together = total − together = 5! − 48 = 120 − 48 = 72. The trap is 48, which is the number of arrangements in which they are together — the opposite of what is asked; 96 doubles 48. In practice: counting by complement (all cases minus the unwanted ones) is often much quicker, as when an analyst counts schedules in which two conflicting meetings do not clash.', 'c5', 'core', f'({fe(5)})-({fe(4)})*2', topic='Permutations with restrictions'))
    M.append(mq('m20', 'Four of nine different files are to be placed in order on a rack. In how many orders does one particular file always appear?', 1344, [336, 3024, 1680], "Place the particular file first: it can occupy any of the 4 positions. The other 3 positions are filled from the remaining 8 files in ⁸P₃ = 336 ways. Total = 4 × 336 = 1,344. The trap is 336, which fixes the file in one position only. In practice: if a specific client file must appear on a 4-slot review rack, the reviewer's possible line-ups are counted this way.", 'c5', 'moderate', f'4*({pe(8, 3)})', topic='Permutations with restrictions'))
    M.append(mq('m21', 'Four of nine different files are to be placed in order on a rack. In how many orders is one particular file never used?', 1680, [1344, 3024, 70], 'If the particular file is never used, simply leave it out and arrange 4 of the remaining 8: ⁸P₄ = 8 × 7 × 6 × 5 = 1,680. The trap is 1,344, the count when the file is always included. Check: 1,344 + 1,680 = 3,024 = ⁹P₄, the total with no restriction. In practice: excluding an item first and then counting is how a planner counts schedules that avoid an unavailable staff member.', 'c5', 'moderate', pe(8, 4), topic='Permutations with restrictions'))
    M.append(mq('m22', 'Using only the digits 1 to 6, each at most once, how many 3-digit numbers above 400 are possible?', 60, [120, 72, 36], "For a number above 400, the hundreds digit must be 4, 5 or 6 — 3 ways. The other two places are filled from the remaining 5 digits in ⁵P₂ = 20 ways. Total = 3 × 20 = 60. The trap is 120 = ⁶P₃, which ignores the 'above 400' condition. In practice: filling the restricted position first is the standard approach, just as a planner first fixes the slot that has a constraint.", 'c5', 'moderate', f'3*({pe(5, 2)})', topic='Permutations with restrictions'))
    M.append(mq('m23', 'How many 3-digit numbers have all three digits different (digits 0 to 9)?', 648, [720, 504, 900], 'Fill the hundreds place first: 9 ways (1–9, since 0 cannot lead). The tens place can then use any of the remaining 9 digits (0 is now allowed), and the units place 8. Total = 9 × 9 × 8 = 648. The trap is 720 = ¹⁰P₃, which wrongly allows 0 in the hundreds place. In practice: invoice and voucher numbering systems must account for leading-zero rules in exactly this way.', 'c1', 'hard', '9*9*8', topic='Fundamental principles of counting'))
    M.append(mq('m24', 'For any n and r (0 ≤ r ≤ n), ⁿPᵣ equals:', 'ⁿCᵣ × r!', ['ⁿCᵣ ÷ r!', 'ⁿCᵣ × (n − r)!', 'ⁿCᵣ + r!'], 'Every selection of r things can be arranged among themselves in r! ways, so arrangements = selections × r!, i.e. ⁿPᵣ = ⁿCᵣ × r!. The trap is ⁿCᵣ ÷ r!, which reverses the relationship — permutations are always at least as many as combinations. In practice: if 3 people are chosen from 8 and then given distinct roles (chair, secretary, treasurer), the count is ⁸C₃ × 3! = ⁸P₃.', 'c7', 'core', topic='Combinations: selections where order does not matter'))
    M.append(mq('m25', 'Five speakers A, B, C, D, E are to address a seminar. In how many orders does A speak before B (not necessarily just before)?', 60, [120, 24, 48], 'Of the 5! = 120 possible orders, A speaks before B in exactly half by symmetry (every order with B before A pairs with one where they swap). So the answer is 120/2 = 60. The trap is 120, which ignores the condition; 24 = 4! counts only the orders in which A speaks immediately before B. In practice: event organisers use this halving argument whenever one item must simply precede another.', 'c5', 'hard', f'({fe(5)})/2', topic='Permutations with restrictions'))
    M.append(mq('m26', 'Which situation calls for a combination rather than a permutation?', 'Choosing 3 directors out of 8 for a board committee', ['Allotting gold, silver and bronze to 3 of 8 runners', 'Forming 3-digit PINs from 8 digits', 'Seating 3 of 8 guests in a row of 3 chairs'], 'A combination is used when only the group matters, not the order. Choosing 3 directors for a committee forms the same committee whatever order they are picked in. The trap is the medals: gold, silver and bronze are different positions, so who gets which matters — a permutation; PINs and seat positions are also ordered. In practice: under the Companies Act, boards constitute committees like the audit committee by selecting members — a combination problem.', 'c7', 'core', topic='Combinations: selections where order does not matter'))
    M.append(mq('m27', '¹⁰C₄ + ¹⁰C₃ equals:', 330, [210, 120, 462], "Pascal's rule says ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ, so ¹⁰C₄ + ¹⁰C₃ = ¹¹C₄ = 330. Check directly: 210 + 120 = 330. The trap is 210, which is ¹⁰C₄ alone; 462 = ¹¹C₅ uses the wrong r. In practice: Pascal's rule is the logic behind the binomial table that statisticians use in probability, and it lets you combine counts without recalculating.", 'c8', 'moderate', ce(11, 4), topic='Properties of ⁿCᵣ'))
    M.append(mq('m28', 'In how many ways can 4 different prizes be given to 6 students if a student may win any number of prizes?', 1296, [4096, 360, 15], "Each of the 4 different prizes can go to any of the 6 students, independently: 6 × 6 × 6 × 6 = 6⁴ = 1,296. The trap is 4⁶ = 4,096, which reverses the roles (as if each student chose a prize); 360 = ⁶P₄ forbids a student from winning twice. Ask: 'what is being assigned, and how many choices does each have?' In practice: allocating several distinct tasks to staff, where one person can take many tasks, is counted this way.", 'c6', 'hard', '6*6*6*6', topic='Alike things and repetition'))
    M.append(mq('m29', 'Five trainees and three managers line up for a photo. If no manager may stand next to another manager, the number of line-ups is:', 14400, [2880, 40320, 7200], 'First line up the 5 trainees: 5! = 120 ways. They create 6 gaps (including both ends). Put the 3 managers in 3 different gaps, in order: ⁶P₃ = 120. Total = 120 × 120 = 14,400. The trap is 40,320 = 8!, which ignores the restriction. In practice: the gap method is used to schedule items that must not be adjacent, such as spacing high-risk audit tests between routine ones.', 'c5', 'hard', f'({fe(5)})*({pe(6, 3)})', topic='Permutations with restrictions'))
    M.append(mq('m30', 'In how many ways can 4 passengers occupy 7 vacant seats in a row?', 840, [35, 28, 2401], 'The seats are distinct positions, so who sits where matters: the first passenger has 7 choices, then 6, 5 and 4: ⁷P₄ = 840. The trap is 35 = ⁷C₄, which counts only which seats are filled, ignoring who sits in them; 2,401 = 7⁴ lets two passengers share a seat. In practice: railway and airline seat-allocation systems face exactly this kind of count when assigning passengers to vacant seats.', 'c3', 'core', pe(7, 4), topic='Permutations: arrangements where order matters'))
    M.append(mq('m31', 'If ⁿPᵣ = 720 and ⁿCᵣ = 120, then r is:', 3, [6, 4, 2], 'Since ⁿPᵣ = ⁿCᵣ × r!, r! = 720/120 = 6 = 3!, so r = 3 (and ¹⁰P₃ = 720 confirms n = 10). The trap is 6, which stops at r! = 6 and reports 6 instead of finding r. In practice: the link between arrangements and selections lets an analyst recover hidden information — for example how many roles exist — from two related counts.', 'c7', 'moderate', topic='Combinations: selections where order does not matter'))

    # ------------------------------------------------------------------ unit
    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch05', 'n': 1,
        'title': 'Basic Concepts of Permutations and Combinations',
        'outcomes': [
            'Count outcomes quickly with the multiplication ("and") and addition ("or") principles instead of listing them.',
            'Use factorial notation and evaluate or solve expressions with factorials, ⁿPᵣ and ⁿCᵣ.',
            'Tell an arrangement (order matters — permutation) from a selection (order does not matter — combination) in a worded problem.',
            'Handle restrictions: things always or never included, things kept together or apart, fixed places, numbers with zero, alike things and repetition.',
            'Count circular arrangements, necklaces and garlands, and geometric figures such as lines, triangles and diagonals.',
            'Apply the properties ⁿCᵣ = ⁿCₙ₋ᵣ, ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ and the "some or all" selection results.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 70}, 'prereq': ['fnd-p3-ch02-u01'],
                 'exam_tip': 'Expect about 3–5 one-mark questions from this chapter. Before you calculate, ask one question: "If I swap two of the chosen items, do I get a new outcome?" Yes → permutation; no → combination.'},
        'concepts': [
            {'id': 'c1', 'title': 'Fundamental principles of counting',
             'body': ['Multiplication rule: if one job can be done in m ways and, after it, a second job in n ways, the two jobs together can be done in m × n ways. It extends to any number of jobs done one after the other.',
                      'Addition rule: if a job can be done in either of two exclusive ways — m ways by the first method or n ways by the second — it can be done in m + n ways.',
                      'Memory hook: "AND → multiply, OR → add". A 3-course meal with 4 starters, 5 mains and 3 desserts gives 4 × 5 × 3 = 60 meals; travelling by one of 6 buses or one of 2 trains gives 6 + 2 = 8 choices.'],
             'analogy': 'Ordering a thali: you pick a dal AND a sabzi AND a sweet — multiply the menu sizes. Paying by card OR UPI — add the options.',
             'work': 'When designing internal controls, a CA estimates how many distinct document numbers, approval paths or user-role combinations a system allows. These are multiplication-rule counts.'},
            {'id': 'c2', 'title': 'Factorial notation',
             'body': ['n! (read "n factorial") is the product 1 × 2 × 3 × … × n for a positive integer n. So 4! = 24, 5! = 120, 6! = 720, 7! = 5040.',
                      'Useful identity: n! = n × (n − 1)!. It lets you cancel quickly: 10!/8! = 10 × 9 = 90 — never cancel "10/8".',
                      '0! is defined to be 1. The reason: ⁿPₙ = n!/(n − n)! must equal n!, which works only if 0! = 1. Factorials of negative numbers or fractions are not defined at this level.'],
             'analogy': 'A factorial is a countdown multiplied together: 5! is "5, 4, 3, 2, 1 — multiply!".',
             'work': 'In practice exams and aptitude tests, factorial simplification is the fastest route through long counting expressions — cancel first, multiply last, to avoid calculator overflow.'},
            {'id': 'c3', 'title': 'Permutations: arrangements where order matters',
             'body': ['A permutation is an arrangement of some or all of a set of things in a definite order. ABC and BAC are different permutations of the same three letters.',
                      'Number of permutations of n different things taken r at a time: ⁿPᵣ = n(n − 1)(n − 2)…(n − r + 1) — exactly r factors — which equals n!/(n − r)!.',
                      'Special cases: ⁿPₙ = n! (all things arranged), ⁿP₁ = n, ⁿP₀ = 1. A handy recursion: ⁿPᵣ = ⁿ⁻¹Pᵣ + r × ⁿ⁻¹Pᵣ₋₁ (arrangements without a particular thing plus those with it).'],
             'blocks': [table(['Expression', 'Expanded', 'Value'], [['⁶P₂', '6 × 5', str(perm(6, 2))], ['⁸P₃', '8 × 7 × 6', str(perm(8, 3))], ['⁵P₅', '5!', str(perm(5, 5))], ['¹⁰P₁', '10', '10']])],
             'analogy': 'Awarding first, second and third prize: the same three winners in a different order is a different result sheet.',
             'work': 'Ranking bids, assigning distinct roles (chair, secretary, treasurer) or ordering audit visits to branches are permutation problems.'},
            {'id': 'c4', 'title': 'Circular permutations',
             'body': ['When things are placed round a circle, rotating everyone by one seat does not create a new arrangement — only relative positions matter. Fix one person and arrange the rest: n different things can be arranged in a circle in (n − 1)! ways.',
                      'If clockwise and anticlockwise orders are the same — a necklace, garland or key-ring that can be flipped over — the count is halved: (n − 1)!/2.',
                      'For people at a round table, clockwise and anticlockwise seatings are different (each person\'s left and right neighbours swap), so use (n − 1)! unless the question says the two directions are not to be distinguished, or asks for seatings in which no person has the same two neighbours, which gives (n − 1)!/2.'],
             'analogy': 'Spinning a lazy Susan does not change who sits next to whom. Turning a bracelet over does not change it either — that is the extra halving.',
             'work': 'Seating plans for board meetings or round-table conferences, and rotation rosters that repeat in a cycle, use circular counting.'},
            {'id': 'c5', 'title': 'Permutations with restrictions',
             'body': ['A particular thing never included: arrange r out of the other (n − 1) things — ⁿ⁻¹Pᵣ.',
                      'A particular thing always included: it can sit in any of the r places, and the other r − 1 places are filled from n − 1 things — r × ⁿ⁻¹Pᵣ₋₁.',
                      'Things that must be together: tie them into one block, arrange the blocks, then multiply by the internal arrangements of the block.',
                      'Things that must never be together (no two of them adjacent): arrange the others first, then put the restricted things into the gaps (gap method). "Not all together" is different — use total minus all-together.',
                      'Fixed places or numbers with digit conditions: fill the restricted place first (for example the first digit cannot be 0, the last digit decides even/odd or divisibility by 5), then fill the rest.'],
             'analogy': 'A wedding photographer told "the couple must stand together" first glues them into one person; told "the two rival uncles must not stand side by side" first lines up everyone else and drops the uncles into separate gaps.',
             'work': 'Rule-based scheduling — "these two partners must not audit the same client", "the reviewer must sign last" — is permutation with restrictions. Doing the restricted step first avoids double counting.'},
            {'id': 'c6', 'title': 'Alike things and repetition',
             'body': ['If n things include p alike of one kind, q alike of a second kind and r alike of a third kind (the rest different), the number of arrangements of all n things is n!/(p! q! r!). Swapping identical things produces no new arrangement, so we divide out those swaps.',
                      'If each of n different things may be used any number of times, r places can be filled in nʳ ways (each place has all n choices).'],
             'analogy': 'Rearranging the letters of "MAMMA": swapping two M\'s looks exactly the same, so we divide out the 3! ways of shuffling the M\'s and the 2! ways of shuffling the A\'s: 5!/(3! 2!) = 10.',
             'work': 'Counting possible PINs, product codes or invoice series (repetition allowed) is nʳ; counting distinct strings from a fixed batch of characters uses the alike-things formula.'},
            {'id': 'c7', 'title': 'Combinations: selections where order does not matter',
             'body': ['A combination is a selection (group) of some or all things, ignoring order. ABC and BAC are the same combination.',
                      'Each combination of r things can be arranged in r! ways, so ⁿPᵣ = ⁿCᵣ × r!, which gives ⁿCᵣ = n!/{r!(n − r)!}.',
                      'ⁿC₀ = ⁿCₙ = 1 and ⁿC₁ = n. For the same n and r, ⁿPᵣ is never smaller than ⁿCᵣ.'],
             'analogy': 'A fruit salad of apple, banana and mango is the same salad whatever order you drop the fruit in. A combination lock is badly named — order matters there, so it is really a permutation lock.',
             'work': 'Selecting a sample of vouchers, choosing members of an audit committee, picking 5 stocks out of a coverage list of 45 — all are combinations.'},
            {'id': 'c8', 'title': 'Properties of ⁿCᵣ',
             'body': ['Complementary combinations: ⁿCᵣ = ⁿCₙ₋ᵣ — choosing r to include is the same as choosing n − r to leave out. Hence if ⁿCₓ = ⁿCᵧ, then either x = y or x + y = n.',
                      'Pascal\'s rule: ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ — a group of r from n + 1 things either excludes a particular thing (ⁿCᵣ) or includes it (ⁿCᵣ₋₁).',
                      'ⁿCᵣ has meaning only for integers with 0 ≤ r ≤ n. Use ⁿCₙ₋ᵣ to shorten work: ²⁰C₁₈ = ²⁰C₂ = 190.'],
             'analogy': 'Picking the 11 players for a match from a squad of 15 is the same decision as picking the 4 who sit out.',
             'work': 'Shortcuts like ⁿCᵣ = ⁿCₙ₋ᵣ save precious seconds in a 100-question, 120-minute objective paper.'},
            {'id': 'c9', 'title': 'Special selections: some or all, alike things, independent groups, geometry',
             'body': ['Some or all of n different things: each thing is either taken or left, 2ⁿ ways, less the empty choice: 2ⁿ − 1 (= ⁿC₁ + ⁿC₂ + … + ⁿCₙ).',
                      'Some or all from alike things (p of one kind, q of another, r of a third): (p + 1)(q + 1)(r + 1) − 1, because from p alike things you may take 0, 1, …, p.',
                      'Independent selections from different groups are multiplied: choosing r₁ from n₁ and r₂ from n₂ gives ⁿ¹Cᵣ₁ × ⁿ²Cᵣ₂. "At least" problems: add the cases, or use total minus the unwanted cases.',
                      'Geometry: n points with no three collinear give ⁿC₂ lines and ⁿC₃ triangles; a polygon with n sides has ⁿC₂ − n = n(n − 3)/2 diagonals. If m of the points are collinear: lines = ⁿC₂ − ᵐC₂ + 1, triangles = ⁿC₃ − ᵐC₃.'],
             'analogy': 'At a buffet each dish gets a yes/no vote — that is the 2ⁿ. Identical laddoos only matter by how many you take, not which ones — that is the (p + 1).',
             'work': 'Audit sampling across strata (some cash vouchers AND some bank vouchers) multiplies independent combinations; "at least one high-value item" is total minus none.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Solving factorial equations', 'difficulty': 'core', 'minutes': 5,
             'q': '(a) Find n if (n + 2)! = 72 × n!. (b) Find x if 1/7! + 1/8! = x/9!. (c) Evaluate 10!/(4! × 6!).',
             'solution': [p('(a) (n + 2)! = (n + 2)(n + 1) × n!. Cancelling n!: (n + 2)(n + 1) = 72 = 9 × 8. So n + 2 = 9, giving n = 7. (The other root of n² + 3n − 70 = 0 is n = −10, which is rejected.)'),
                          p(f'(b) Take 1/7! common: 1/7! × (1 + 1/8) = 9/(8 × 7!). Also x/9! = x/(9 × 8 × 7!). Equate: 9/(8 × 7!) = x/(9 × 8 × 7!), so x = 9 × 9 = {x1}.'),
                          p('(c) 10!/(4! 6!) = (10 × 9 × 8 × 7)/(4 × 3 × 2 × 1) = 5040/24 = 210 — which is simply ¹⁰C₄.'),
                          note('Always expand the larger factorial only down to the smaller one and cancel.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Forming numbers when zero is one of the digits', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Using the digits 0, 1, 2, 3, 5, 7 (no digit repeated), how many four-digit numbers can be formed? How many of them are (a) greater than 5000, (b) even?',
             'solution': [wn('Step 1 — all four-digit numbers', f'The thousands place cannot be 0, so it has 5 choices. The remaining 3 places are filled from the 5 digits left: ⁵P₃ = 60. Total = 5 × 60 = {n_all}.'),
                          wn('Step 2 — greater than 5000', f'The first digit must be 5 or 7 (2 ways). The other three places: ⁵P₃ = 60. Total = {n_gt}. (5000 itself cannot be formed, since digits do not repeat.)'),
                          wn('Step 3 — even numbers', 'The units digit must be 0 or 2. Treat the two cases separately because 0 also affects the first place.'),
                          table(['Case', 'Units', 'Thousands', 'Middle two places', 'Count'], [
                              ['Ends in 0', '1 way', '5 ways (1, 2, 3, 5, 7)', '⁴P₂ = 12', '60'],
                              ['Ends in 2', '1 way', '4 ways (not 0, not 2)', '⁴P₂ = 12', '48'],
                              ['Even numbers', '', '', '', str(n_even)]], num=[4], total=True),
                          note('Fill the most restricted place first (here the units place), and split into cases whenever the restriction on one place changes the choices for another.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Letters together, apart and in fixed places — AUDITOR', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'The word AUDITOR has 7 different letters (vowels A, U, I, O; consonants D, T, R). Find the number of arrangements (a) in all, (b) with all vowels together, (c) with no two consonants together, (d) with consonants only in the even places, (e) in which the vowels are not all together.',
             'solution': [table(['Part', 'Method', 'Working', 'Answer'], [
                 ['(a)', 'All 7 letters, all different', '7!', inr(w_all)],
                 ['(b)', 'Vowel block + D, T, R = 4 units; vowels inside block', '4! × 4!', inr(w_vt)],
                 ['(c)', 'Place 4 vowels (4!), 5 gaps around them, put 3 consonants in 3 gaps', '4! × ⁵P₃ = 24 × 60', inr(w_gap)],
                 ['(d)', 'Even places 2, 4, 6 take D, T, R; odd places 1, 3, 5, 7 take the vowels', '3! × 4!', inr(w_even)],
                 ['(e)', 'Total − all vowels together', f'{inr(w_all)} − {inr(w_vt)}', inr(w_nvt)]]),
                 note('"No two consonants together" (gap method) and "consonants not all together" (total − together) are different questions — read the wording carefully.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Arrangements with repeated letters — ACCOUNTANT', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Find the number of arrangements of the letters of ACCOUNTANT (a) in all, (b) beginning with A, (c) beginning and ending with A.',
             'solution': [wn('Letter count', 'A × 2, C × 2, N × 2, T × 2, O × 1, U × 1 — 10 letters.'),
                          p(f'(a) 10!/(2! 2! 2! 2!) = 36,28,800/16 = {inr(acc_all)}.'),
                          p(f'(b) Put one A first. The other 9 letters are A, C, C, N, N, T, T, O, U: 9!/(2! 2! 2!) = 3,62,880/8 = {inr(acc_a)}.'),
                          p(f'(c) Both A\'s fixed at the ends. The middle 8 letters C, C, N, N, T, T, O, U: 8!/(2! 2! 2!) = 40,320/8 = {inr(acc_ends)}.'),
                          note('Re-count the repeated letters after fixing any letter — fixing one A removes the A from the denominator.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Round tables and necklaces', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Eight members of a finance committee sit at a round table. Find the number of seatings (a) in all, (b) with the chairperson and the treasurer side by side, (c) with these two never side by side. (d) How many different necklaces can be made from 9 beads of different colours?',
             'solution': [p(f'(a) Circular arrangement of 8 different people: (8 − 1)! = 7! = {inr(r8)}.'),
                          p(f'(b) Treat the two as one unit: 7 units round the table in (7 − 1)! = 720 ways; the two can swap seats in 2! ways. Total {inr(r8t)}.'),
                          p(f'(c) Total − together = {inr(r8)} − {inr(r8t)} = {inr(r8n)}.'),
                          p(f'(d) A necklace can be flipped, so clockwise and anticlockwise orders coincide: (9 − 1)!/2 = 40,320/2 = {inr(neck)}.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Committee with an "at least" condition', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'A committee of 5 is to be chosen from 6 men and 5 women so that it has at least 2 women. In how many ways can this be done?',
             'solution': [table(['Women', 'Men', 'Working', 'Ways'], [
                 ['2', '3', '⁵C₂ × ⁶C₃ = 10 × 20', str(t2)],
                 ['3', '2', '⁵C₃ × ⁶C₂ = 10 × 15', str(t3)],
                 ['4', '1', '⁵C₄ × ⁶C₁ = 5 × 6', str(t4)],
                 ['5', '0', '⁵C₅ × ⁶C₀ = 1 × 1', str(t5)],
                 ['Total', '', '', str(at2)]], num=[3], total=True),
                 wn('Cross-check by complement', f'All committees ¹¹C₅ = {tot11}. Unwanted: no woman ⁶C₅ = 6; exactly one woman 5 × ⁶C₄ = 75. {tot11} − 6 − 75 = {at2}.'),
                 note('Never compute "at least 2 women" as ⁵C₂ × ⁹C₃ (choose 2 women, then any 3) — that counts the same committee several times.')],
             'checks': c6},
            {'id': 'i7', 'title': 'Lines, triangles and diagonals', 'difficulty': 'moderate', 'minutes': 6,
             'q': '(a) There are 14 points in a plane, of which exactly 5 lie on one straight line; no other three are collinear. How many straight lines and how many triangles can be formed? (b) Find the number of diagonals of a decagon. (c) A polygon has 54 diagonals. How many sides does it have?',
             'solution': [p(f'(a) Lines: ¹⁴C₂ − ⁵C₂ + 1 = 91 − 10 + 1 = {lines}. The 10 pairs from the collinear points all give the same single line. Triangles: ¹⁴C₃ − ⁵C₃ = 364 − 10 = {tri} (three collinear points make no triangle).'),
                          p(f'(b) Diagonals = ¹⁰C₂ − 10 = 45 − 10 = {dec}.'),
                          p('(c) n(n − 3)/2 = 54 → n² − 3n − 108 = 0 → (n − 12)(n + 9) = 0 → n = 12 sides.')],
             'checks': c7},
            {'id': 'i8', 'title': 'Using the properties of ⁿCᵣ', 'difficulty': 'core', 'minutes': 4,
             'q': '(a) If ⁿC₆ = ⁿC₁₀, find ⁿC₁₄. (b) If ⁿPᵣ = 720 and ⁿCᵣ = 120, find n and r.',
             'solution': [p(f'(a) 6 ≠ 10, so 6 + 10 = n, n = 16. ¹⁶C₁₄ = ¹⁶C₂ = (16 × 15)/2 = {n16}.'),
                          p('(b) ⁿPᵣ = ⁿCᵣ × r!, so r! = 720/120 = 6 = 3!, r = 3. Then n(n − 1)(n − 2) = 720 = 10 × 9 × 8, so n = 10.')],
             'checks': c8},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'How many different audit samples are possible?', 'role': 'Articled assistant planning vouching in a statutory audit',
             'situation': 'Your manager asks you to pick 4 vouchers out of 20 high-value payments for detailed vouching, and later to pick 2 out of 12 cash vouchers and 2 out of 8 bank vouchers. The client\'s accountant asks: "Surely you will just look at the first four?"',
             'steps': [f'Order of picking does not matter, so the number of possible samples is ²⁰C₄ = {inr(samp)}.',
                       f'For the stratified sample the two picks are independent, so multiply: ¹²C₂ × ⁸C₂ = 66 × 28 = {inr(samp2)}.',
                       'Explain that because there are thousands of equally possible samples, the client cannot predict which vouchers will be checked — that is what makes sampling a deterrent.',
                       'Record the selection method (random numbers or systematic) in the working paper so a reviewer can re-perform it.'],
             'takeaway': 'Combinations show why an unpredictable sample is powerful: the number of possible selections grows very fast.',
             'think': 'If the sample size rose from 4 to 5 out of the same 20 vouchers, how many samples would be possible?',
             'answer': '²⁰C₅ = 15,504 — more than three times as many.',
             'checks': cj1},
            {'id': 'j2', 'title': 'Is the voucher-numbering scheme big enough?', 'role': 'Accounts executive helping to set up an ERP numbering series',
             'situation': 'The company wants voucher codes made of 2 capital letters followed by 3 digits and expects about 5 lakh vouchers over the life of the system. IT also asks about the strength of a 6-digit OTP.',
             'steps': [f'If letters and digits may not repeat within a code: ²⁶P₂ × ¹⁰P₃ = 650 × 720 = {inr(code_nr)} — fewer than 5 lakh, so this scheme is too small.',
                       f'If repetition is allowed: 26² × 10³ = {inr(code_r)} codes — enough, with headroom.',
                       f'A 6-digit OTP with any digit in any place gives 10⁶ = {inr(otp)} possibilities, which is why systems also limit the number of attempts.'],
             'takeaway': 'Repetition allowed → nʳ; no repetition → ⁿPᵣ. Choosing the wrong one can make a numbering series run out years early.',
             'checks': cj2},
        ],
        'mcqs': M,
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'How many three-digit numbers can be formed from the digits 0, 2, 4, 5, 6, 9 if no digit is repeated? How many of these are divisible by 5? Show your steps.',
             'model': [wn('All three-digit numbers', f'Hundreds place: 5 ways (0 not allowed). Tens and units from the remaining 5 digits: 5 × 4. Total = 5 × 5 × 4 = {q1_all}.'),
                       wn('Divisible by 5 — units digit 0 or 5', f'Ending in 0: the other two places from 5 digits, ⁵P₂ = {q1_0}. Ending in 5: hundreds place 4 ways (not 0, not 5), tens place 4 ways → {q1_5}.'),
                       p(f'Numbers divisible by 5 = {q1_0} + {q1_5} = {q1_t}.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Hundreds place restricted (no 0): total 100', 'm': 1, 'skill': 'computation'},
                 {'id': 's2', 'pt': 'Divisibility by 5 identified as units digit 0 or 5, split into two cases', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': 'Case ending in 0 = 20 and case ending in 5 = 16 (zero excluded from first place)', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's4', 'pt': 'Final answer 36 stated clearly', 'm': 0.5, 'skill': 'conclusion'}],
             'remarks': ['Most errors come from treating both cases alike: when 5 is in the units place, 0 is still available and must be kept out of the hundreds place.',
                         'Candidates who list numbers instead of counting run out of time — the case table takes under two minutes.'],
             'mistakes': ['Taking ⁶P₃ = 120 as the total (allows 0 in the hundreds place).', 'Writing 2 × ⁵P₂ = 40 for divisibility by 5.'],
             'tips': ['Draw three boxes, fill the restricted ones first and write the number of choices in each box.', 'Whenever 0 is a digit, split cases on whether 0 has already been used.'],
             'checks': qc1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'An expert panel of 6 is to be formed from 7 Chartered Accountants and 5 Company Secretaries so that it contains at least 3 CAs and at least 2 CSs. (a) In how many ways can the panel be formed? (b) In how many of these is a particular CA, Mr. Iyer, a member?',
             'model': [table(['CAs', 'CSs', 'Working', 'Ways'], [
                 ['3', '3', '⁷C₃ × ⁵C₃ = 35 × 10', str(q2a)], ['4', '2', '⁷C₄ × ⁵C₂ = 35 × 10', str(q2b)], ['Total (a)', '', '', str(q2t)]], num=[3], total=True, title='(a) Possible compositions'),
                 table(['CAs', 'CSs', 'Working (Mr. Iyer fixed)', 'Ways'], [
                     ['3', '3', '⁶C₂ × ⁵C₃ = 15 × 10', str(q2c)], ['4', '2', '⁶C₃ × ⁵C₂ = 20 × 10', str(q2d)], ['Total (b)', '', '', str(q2i)]], num=[3], total=True, title='(b) Panels including Mr. Iyer'),
                 note('5 CAs + 1 CS is not allowed (fewer than 2 CSs) and 2 CAs + 4 CSs is not allowed (fewer than 3 CAs).')],
             'scheme': [
                 {'id': 's1', 'pt': 'Valid compositions identified: (3 CA, 3 CS) and (4 CA, 2 CS) only', 'm': 1, 'skill': 'analysis'},
                 {'id': 's2', 'pt': 'Each case computed by multiplying independent combinations', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Total 700 for part (a)', 'm': 0.5, 'skill': 'conclusion'},
                 {'id': 's4', 'pt': 'Part (b): Mr. Iyer fixed, choose remaining CAs from 6 in each case — 150 and 200', 'm': 1.5, 'skill': 'application'},
                 {'id': 's5', 'pt': 'Total 350 for part (b)', 'm': 0.5, 'skill': 'conclusion'}],
             'remarks': ['Good answers start by listing the allowed compositions — it shows the examiner the logic and earns method marks.',
                         'Some candidates add the two products inside a case instead of multiplying them.'],
             'mistakes': ['Including the (5, 1) or (2, 4) compositions.', 'For (b), choosing the remaining CAs from 7 instead of 6.'],
             'tips': ['Use a composition table: one row per case, then total.', 'Fixing a person = remove him from the pool and reduce the number to be chosen by one.'],
             'checks': qc2},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
             'q': 'Consider the letters of the word INCOMETAX (9 different letters; vowels I, O, E, A). Find the number of arrangements (a) in all, (b) with all vowels together, (c) with no two vowels together, (d) with the vowels appearing in the order I, O, E, A (not necessarily next to each other).',
             'model': [table(['Part', 'Method', 'Working', 'Answer'], [
                 ['(a)', '9 different letters', '9!', inr(q3a)],
                 ['(b)', 'Vowel block + 5 consonants = 6 units', '6! × 4! = 720 × 24', inr(q3b)],
                 ['(c)', 'Arrange 5 consonants, 6 gaps, place 4 vowels in 4 gaps', '5! × ⁶P₄ = 120 × 360', inr(q3c)],
                 ['(d)', 'Only 1 of the 4! vowel orders is allowed', '9!/4!', inr(q3d)]])],
             'scheme': [
                 {'id': 's1', 'pt': '(a) 9! = 3,62,880', 'm': 1, 'skill': 'computation'},
                 {'id': 's2', 'pt': '(b) Block method: 6! × 4! = 17,280', 'm': 1.5, 'skill': 'application'},
                 {'id': 's3', 'pt': '(c) Gap method with 6 gaps and ⁶P₄: 43,200', 'm': 2, 'skill': 'application'},
                 {'id': 's4', 'pt': '(d) Fixed relative order: divide by 4! — 15,120', 'm': 1.5, 'skill': 'concept'}],
             'remarks': ['Part (c) separates strong candidates: many compute total − together, which answers "not all together", not "no two together".',
                         'In (d) some candidates fix the vowels in four particular places; the vowels can be anywhere as long as their order is I, O, E, A.'],
             'mistakes': ['Using ⁶C₄ instead of ⁶P₄ in the gap method (vowels are different, so order in the gaps matters).', 'Forgetting the 4! inside the block in (b).'],
             'tips': ['Write the method in words in one column — examiners award step marks for the method even if arithmetic slips.', 'For "in a given order", divide the total by the factorial of the number of ordered things.'],
             'checks': qc3},
        ],
        'revision': {
            'summary': ['AND → multiply; OR → add.', 'n! = n(n − 1)!, 0! = 1.', 'ⁿPᵣ = n!/(n − r)! (order matters); ⁿCᵣ = n!/{r!(n − r)!} (order does not matter); ⁿPᵣ = ⁿCᵣ × r!.',
                        'Circle: (n − 1)!; necklace/garland: (n − 1)!/2.', 'Alike things: n!/(p! q! r!); repetition allowed: nʳ.',
                        'Particular thing excluded: ⁿ⁻¹Pᵣ; included: r × ⁿ⁻¹Pᵣ₋₁.', 'Together: block × internal arrangements; no two together: gap method.',
                        'ⁿCᵣ = ⁿCₙ₋ᵣ; ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ; some or all: 2ⁿ − 1; from alike groups: (p + 1)(q + 1)… − 1.',
                        'Lines ⁿC₂, triangles ⁿC₃, diagonals ⁿC₂ − n; with m collinear: lines − ᵐC₂ + 1, triangles − ᵐC₃.'],
            'remember': ['Fill the most restricted place first.', 'If ⁿCₓ = ⁿCᵧ and x ≠ y, then n = x + y.', 'Independent selections from different groups are multiplied, not added.'],
            'traps': ['"Not all together" ≠ "no two together".', 'Zero cannot be the first digit of a number — split cases when 0 is among the digits.', 'Round table with people: do not halve unless clockwise and anticlockwise are to be treated alike.', 'Choosing a committee is a combination — do not multiply by r!.'],
        },
        'quickref': [
            {'k': 'Factorial', 'v': 'n! = 1 × 2 × … × n; 0! = 1'},
            {'k': 'Permutations', 'v': 'ⁿPᵣ = n!/(n − r)!; ⁿPₙ = n!'},
            {'k': 'Combinations', 'v': 'ⁿCᵣ = n!/{r!(n − r)!}; ⁿPᵣ = ⁿCᵣ × r!'},
            {'k': 'Circular', 'v': '(n − 1)!; necklace or garland (n − 1)!/2'},
            {'k': 'Alike things', 'v': 'n!/(p! q! r!)'},
            {'k': 'Repetition allowed', 'v': 'nʳ'},
            {'k': 'Particular thing', 'v': 'never: ⁿ⁻¹Pᵣ; always: r × ⁿ⁻¹Pᵣ₋₁'},
            {'k': 'Properties of ⁿCᵣ', 'v': 'ⁿCᵣ = ⁿCₙ₋ᵣ; ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ; ⁿC₀ = ⁿCₙ = 1'},
            {'k': 'Some or all', 'v': '2ⁿ − 1; alike groups (p + 1)(q + 1)(r + 1) − 1'},
            {'k': 'Geometry', 'v': 'lines ⁿC₂; triangles ⁿC₃; diagonals n(n − 3)/2'},
        ],
        'viva': VIVA,
        'cases': [{
            'id': 'k1', 'title': 'Staffing an audit team at Mehra & Associates', 'difficulty': 'hard',
            'case': ('Mehra & Associates, a CA firm, has 4 seniors and 6 articled assistants free for a new bank audit. The partner wants a team of 5. '
                     'For the kick-off meeting the team will sit at a round table, and for the team photograph they will stand in a single row.'),
            'mcqs': [
                mq('k1a', 'In how many ways can a team with exactly 2 seniors and 3 assistants be formed?', k_a, [26, 720, 252], "Choose 2 of the 4 seniors (⁴C₂ = 6) and 3 of the 6 assistants (⁶C₃ = 20). The choices are independent, so multiply: 6 × 20 = 120. The trap is 26, which adds instead of multiplying; 252 = ¹⁰C₅ ignores the required mix. In practice: CA firms staff bank audits with a set senior-to-article ratio, and the partner's options are counted exactly this way.", 'c9', 'moderate', f'({ce(4, 2)})*({ce(6, 3)})', topic='Special selections: some or all, alike things, independent groups, geometry'),
                mq('k1b', 'In how many ways can the team of 5 be formed so that it has at least one senior?', k_b, [252, 126, 240], 'Use the complement: all teams of 5 from 10 = ¹⁰C₅ = 252; teams with no senior (all from the 6 assistants) = ⁶C₅ = 6. At least one senior = 252 − 6 = 246. The trap is 252, which forgets to remove the all-assistant teams. In practice: quality-control standards require at least one experienced member on each engagement, and complement counting is the fastest way to apply such rules.', 'c9', 'hard', f'({ce(10, 5)})-({ce(6, 5)})', topic='Special selections: some or all, alike things, independent groups, geometry'),
                mq('k1c', 'Once the team of 5 is fixed, in how many ways can they sit at the round table?', k_c, [120, 12, 60], "Round-table seating of 5 different people: fix one person and arrange the other 4, giving (5 − 1)! = 4! = 24. The trap is 120 = 5!, which treats the round table as a row and counts rotations of the same seating separately. In practice: kick-off meetings at a round table have no 'head' seat, which is why rotations are not counted as new arrangements.", 'c4', 'moderate', fe(4), topic='Circular permutations'),
                mq('k1d', 'For the photograph, the team chosen has exactly 2 seniors (as in the first question). In how many ways can the 5 stand in a row if the two seniors must stand side by side?', k_d, [24, 120, 72], "Tie the two seniors together as one unit: 4 units can stand in 4! = 24 orders, and the two seniors can swap within the unit in 2! = 2 ways. Total = 24 × 2 = 48. The trap is 24, which forgets the seniors can stand in either order; 120 ignores the restriction. In practice: photo line-ups and stage seating with 'must be together' conditions are planned with this block method.", 'c5', 'hard', f'({fe(4)})*2', topic='Permutations with restrictions'),
            ]}],
    }


# ------------------------------------------------------------------ viva (speak & revise)
VIVA = [
    V('v1', 'What is the difference between a permutation and a combination?',
      'A permutation is an arrangement, so the order of the things matters, while a combination is only a selection, where order does not matter. Each combination of r things can be arranged in r factorial ways, so n P r equals n C r multiplied by r factorial, and the number of permutations is never less than the number of combinations.',
      [P('p1', 'Permutation = arrangement; order matters', 4, 'permutation arrang|permutation order matter|permutation order important|permutation order count|permutation sequence matter|permutation order relevant|permutation mean arrang|permutation about order|permutation care order|order matter in permutation|order important in permutation'),
       P('p2', 'Combination = selection; order does not matter', 4, 'combination order not|combination order doesn|combination order irrelevant|combination order ignor|combination order unimportant|combination selection|combination select|combination group|combination ignor order|combination without order|combination not care order|combination no order|combination doesn care order'),
       P('p3', 'nPr = nCr × r!', 2, 'r factorial|r!|factorial r|multiplied by r|times r', min=1)], 'c7'),
    V('v2', 'Why is zero factorial taken as one?',
      'If we put r equal to n in the formula n P r equals n factorial divided by n minus r factorial, we get n factorial divided by zero factorial. But arranging all n things gives n factorial ways, so zero factorial must equal one for the formula to stay consistent.',
      [P('p1', 'Put r = n in nPr = n!/(n − r)!', 4, 'r equal n|r equals n|r is n|r n|put r|n minus n|n p n|npn|all n thing', min=1),
       P('p2', 'Gives n!/0!, which must equal n! (arranging all n things)', 3, 'n factorial divid zero factorial|divid zero factorial|over zero factorial|n factorial over 0|equal n factorial|must be n factorial|n factorial way|gives n factorial', min=1),
       P('p3', 'So 0! = 1 to keep the formula consistent', 3, 'zero factorial one|zero factorial equal one|0 factorial 1|zero factorial is 1|0! 1|zero factorial must equal one|zero factorial must be one|zero factorial must be 1', 'consistent|formula|work|valid|hold|true|defin|convention|meaningful', min=1)], 'c2'),
    V('v3', 'How many ways can n different things be arranged in a circle, and when do we halve that number?',
      'Round a circle only the relative positions matter, so we fix one thing and arrange the other n minus one, giving n minus one factorial arrangements. We halve it, that is n minus one factorial divided by two, when clockwise and anticlockwise arrangements are the same, as with a necklace or a garland that can be turned over.',
      [P('p1', 'Circular arrangements = (n − 1)!', 4, 'n minus 1 factorial|n minus one factorial|n 1 factorial|n-1 factorial|n 1 !|n-1!'),
       P('p2', 'Reason: fix one thing — rotations give no new arrangement', 2, 'fix one|fix 1|fixing one|fixed one|rotat|relative position|relative order|one place fixed|keep one fixed', min=1),
       P('p3', 'Halve when clockwise and anticlockwise are the same (necklace / garland)', 4, 'clockwise|anticlockwise|anti clockwise|both direction|turn over|flip|necklace|garland|bracelet', 'half|halve|divid by 2|divid by two|divide 2|over 2|over two', min=2)], 'c4'),
    V('v4', 'What is the formula for arranging n things when some of them are alike, and why do we divide?',
      'If p things are alike of one kind, q alike of another and r alike of a third, the number of arrangements is n factorial divided by p factorial, q factorial and r factorial. We divide because swapping identical things among themselves does not produce a new arrangement, so those repeated counts must be removed.',
      [P('p1', 'n!/(p! q! r!)', 5, 'n factorial', 'p factorial|p!|factorial of p|factorial of the alike|factorial of each repeat|factorial of repeat', 'divid|over|ratio', min=3),
       P('p2', 'Swapping identical things gives no new arrangement — duplicates removed', 5, 'identical|alike|same|repeat', 'no new|not new|not different|no different|same arrangement|duplicat|counted more than once|double count|overcount|over count|not distinct|remov|look same|indistinguishable', min=2)], 'c6'),
    V('v5', 'Explain why n C r equals n C n minus r.',
      'Every time we choose r things to include from n, we automatically leave out the remaining n minus r things. So each selection of r corresponds to exactly one selection of n minus r to leave out, and the two counts are equal. These are called complementary combinations; for example, twenty C eighteen equals twenty C two.',
      [P('p1', 'Choosing r to include = choosing n − r to leave out', 6, 'leave out|left out|leave|reject|exclud|remaining|rest|not chosen|not select', 'n minus r|n-r|n r', min=2),
       P('p2', 'One-to-one correspondence — equal counts (complementary combinations)', 4, 'exactly one|one to one|correspond|each select|same number|equal|complementary', min=1)], 'c8'),
    V('v6', 'State the two fundamental principles of counting.',
      'The multiplication rule says that if one job can be done in m ways and after that a second job in n ways, both jobs together can be done in m times n ways. The addition rule says that if a job can be done either in m ways or, alternatively, in n ways, it can be done in m plus n ways. In short, and means multiply and or means add.',
      [P('p1', 'Multiplication rule: one job then another → m × n', 5, 'multiplication rule|multiply rule|rule of product|m times n|m multipli n|product m n|after multipl|another multipl|together multipl|both multipl|mean multipl|successive multipl|sequence multipl|multipl both|multipl when both|multipl if both|multipl one after'),
       P('p2', 'Addition rule: either/or alternatives → m + n', 5, 'addition rule|add rule|rule of sum|m plus n|m add n|m added n|sum m n|alternative add|altern add|either add|mean add|exclusive add|instead add|add when either|add if either|add altern|add for altern')], 'c1'),
]
