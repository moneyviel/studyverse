"""CA Foundation · Paper 3 Quantitative Aptitude · Part B Logical Reasoning · Chapter 11 Seating Arrangements.
Original puzzles. Each puzzle is solved by brute force below (every permutation tried) and asserted to have exactly one arrangement."""
from itertools import permutations
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch11-u01'


def solve(names, cons, circular=False):
    """All arrangements meeting every condition. Row: index 0 = reader's left end. Circle: index increases clockwise; first name fixed (rotations are the same seating)."""
    out = []
    for perm in permutations(names):
        if circular and perm[0] != names[0]: continue
        pos = {n: i for i, n in enumerate(perm)}
        if all(c(pos) for c in cons): out.append(list(perm))
    return out


def one(names, cons, circular=False):
    s = solve(names, cons, circular); assert len(s) == 1, s
    return s[0]


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None, topic=None):
    d = {'topic': topic, 'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def build():
    # Row facing North: a person's right = higher index.  Circle facing the centre: a person's left = clockwise = index + 1.
    # ---- Illustration 1 (row of 5, facing North) ----
    I1 = one(['Asha', 'Bina', 'Chetan', 'Dev', 'Esha'], [
        lambda p: p['Chetan'] == p['Dev'] - 2, lambda p: p['Asha'] == p['Esha'] + 1,
        lambda p: p['Bina'] not in (0, 4), lambda p: p['Esha'] in (0, 4)])
    assert I1 == ['Esha', 'Asha', 'Chetan', 'Bina', 'Dev']
    # ---- Illustration 2 (same five facing South): "X is to the immediate right of Y" means X is one place to the READER's left ----
    I2 = one(['Asha', 'Bina', 'Chetan', 'Dev', 'Esha'], [
        lambda p: p['Chetan'] == p['Dev'] + 2, lambda p: p['Asha'] == p['Esha'] - 1,
        lambda p: p['Bina'] not in (0, 4), lambda p: p['Esha'] in (0, 4)])
    assert I2 == I1[::-1]
    # ---- MCQ set A: row of 7 facing North ----
    A = one(list('ABCDEFG'), [
        lambda p: p['A'] == p['C'] + 2, lambda p: p['G'] == 3, lambda p: p['E'] in (0, 6), lambda p: p['B'] == p['E'] - 1,
        lambda p: abs(p['D'] - p['G']) == 1 and abs(p['D'] - p['B']) == 1, lambda p: p['F'] not in (0, 6)])
    assert A == ['C', 'F', 'A', 'G', 'D', 'B', 'E']
    pa = {n: i for i, n in enumerate(A)}
    assert A[pa['D'] - 3] == 'F' and pa['B'] - pa['F'] - 1 == 3
    # ---- MCQ set B: circle of 6 facing the centre ----
    B = one(list('KLMNOP'), [
        lambda p: p['M'] == (p['K'] + 1) % 6, lambda p: p['O'] == (p['K'] + 3) % 6, lambda p: p['N'] == (p['K'] - 1) % 6,
        lambda p: {(p['L'] - 1) % 6, (p['L'] + 1) % 6} == {p['M'], p['O']}], circular=True)
    assert B == ['K', 'M', 'L', 'O', 'P', 'N']
    pb = {n: i for i, n in enumerate(B)}
    left6 = lambda x, k=1: B[(pb[x] + k) % 6]; right6 = lambda x, k=1: B[(pb[x] - k) % 6]
    assert B[(pb['M'] + 3) % 6] == 'P' and left6('P') == 'N' and right6('L', 2) == 'K'
    # ---- MCQ set C: circle of 8, men and women alternate, facing the centre ----
    W = set('ABCD')
    def alt(p):
        order = sorted('ABCDEFGH', key=lambda x: p[x]); return all((order[i] in W) != (order[(i + 1) % 8] in W) for i in range(8))
    C = one(list('ABCDEFGH'), [alt, lambda p: p['C'] == (p['A'] + 4) % 8, lambda p: p['E'] == (p['A'] + 1) % 8, lambda p: p['G'] == (p['E'] + 4) % 8,
                               lambda p: {(p['B'] - 1) % 8, (p['B'] + 1) % 8} == {p['E'], p['F']}, lambda p: p['H'] == (p['A'] - 1) % 8], circular=True)
    assert C == ['A', 'E', 'B', 'F', 'C', 'G', 'D', 'H']
    pc = {n: i for i, n in enumerate(C)}
    assert C[(pc['F'] + 4) % 8] == 'H' and C[(pc['D'] - 1) % 8] == 'G' and C[(pc['F'] + 1) % 8] == 'C' and C[(pc['B'] - 2) % 8] == 'A'
    # ---- MCQ set D: two rows of three facing each other. idx 0-2 north row facing South, idx 3-5 south row facing North; column = idx mod 3 (reader's left = 0) ----
    col = lambda i: i % 3
    D = one(list('PQRXYZ'), [
        lambda p: all(p[x] < 3 for x in 'PQR'), lambda p: col(p['Q']) == col(p['Y']),
        lambda p: col(p['P']) == col(p['Q']) - 1,                       # P faces South, so his right is the reader's left
        lambda p: col(p['X']) in (0, 2) and col(p['X']) != col(p['R'])])
    assert D == ['P', 'Q', 'R', 'X', 'Y', 'Z']
    # ---- Case: board meeting, circle of 6 facing the centre ----
    K = one(['Ahuja', 'Bose', 'Chawla', 'Dutta', 'Iyer', 'Jain'], [
        lambda p: p['Jain'] == (p['Ahuja'] + 3) % 6, lambda p: p['Iyer'] == (p['Ahuja'] + 1) % 6,
        lambda p: p['Chawla'] == (p['Bose'] + 2) % 6, lambda p: (p['Dutta'] - p['Iyer']) % 6 not in (1, 5)], circular=True)
    assert K == ['Ahuja', 'Iyer', 'Bose', 'Jain', 'Chawla', 'Dutta']
    # ---- Question 1: row of 6 facing North ----
    Q1 = one(list('UVWXYZ'), [lambda p: p['X'] == 5, lambda p: p['U'] == p['X'] - 3, lambda p: abs(p['W'] - p['Y']) == 1 and p['W'] in (0, 5),
                              lambda p: abs(p['V'] - p['U']) != 1])
    assert Q1 == ['W', 'Y', 'U', 'Z', 'V', 'X']
    # ---- Question 2: circle of 6 facing OUTWARD: a person's left = anticlockwise = index - 1 ----
    Q2 = one(list('RSTUVW'), [lambda p: p['U'] == (p['R'] + 3) % 6, lambda p: p['S'] == (p['T'] - 1) % 6, lambda p: p['W'] == (p['R'] + 1) % 6,
                              lambda p: (p['V'] - p['U']) % 6 in (1, 5), lambda p: (p['T'] - p['W']) % 6 not in (1, 5)], circular=True)
    assert Q2 == ['R', 'W', 'V', 'U', 'S', 'T']

    c_q1 = Checks(); c_q1.add('6-3', 'U\'s seat counted from the left end: third to the left of seat 6')

    row = lambda names, title: table(['Seat (reader\'s left → right)'] + [str(i + 1) for i in range(len(names))], [['Person'] + names], title=title)
    circ = lambda names, title: table(['Clockwise order (seen from above)'] + [str(i + 1) for i in range(len(names))], [['Person'] + names], title=title)

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch11', 'n': 1, 'title': 'Seating Arrangements',
        'outcomes': ['Sort the clues of a seating puzzle into definite, comparative and negative information and use them in that order.',
                     'Solve linear arrangements — one row facing North, one row facing South, and two rows facing each other — reading left and right from the sitter\'s own view.',
                     'Solve circular arrangements with people facing the centre or facing outward, using clockwise/anticlockwise for left/right.',
                     'Answer the follow-up questions (ends, middle, between, nth to the left/right, opposite, how many between) quickly from the final diagram.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 60}, 'prereq': ['fnd-p3-ch10-u01'],
                 'exam_tip': 'A seating puzzle usually carries 3–5 linked MCQs, so the time spent drawing the diagram pays back several times. Draw once, carefully, and answer every linked question from that one diagram.'},
        'concepts': [
            {'id': 'c1', 'title': 'Types of arrangement and types of information', 'body': [
                'Arrangements are linear (one or two rows), circular (round table) or polygon (square, rectangle, hexagon tables). The Foundation syllabus concentrates on linear and circular arrangements.',
                'Definite information fixes a seat by itself: "X sits at the right end", "G sits in the middle".',
                'Comparative information places one person relative to another: "A is second to the right of E". It becomes useful once the reference person is placed.',
                'Negative information rules a seat out: "C is not next to A". It never places anyone, but it eliminates possibilities when two cases remain.',
                'Order of use: definite → comparative (chained from what is fixed) → negative (to choose between remaining cases). Finally check every clue against the finished diagram.'],
             'analogy': 'Definite clues are pegs hammered into the board; comparative clues are strings tied to those pegs; negative clues are "do not park here" signs.',
             'work': 'Planning a stock-count or a client meeting room often needs exactly this logic — "the partner must sit opposite the client\'s CFO, the article must be next to the partner, the tax head cannot sit beside the auditor".'},
            {'id': 'c2', 'title': 'One row: facing North vs facing South', 'body': [
                'If the people face North (away from you, or when no direction is stated), their left and right are the same as yours: "X is to the right of Y" means X is further to your right.',
                'If they face South (towards you), their left and right are the opposite of yours: "X is to the immediate right of Y" means X sits one seat to YOUR left of Y.',
                '"To the right of" includes everyone on that side; "to the immediate right of" means the very next seat. "Between" (unless stated otherwise) means sitting in the seat(s) directly between the two.',
                'Useful counts: in a row of n, the middle seat (n odd) has (n − 1)/2 people on each side; if someone is p-th from the left and q-th from the right, the row holds p + q − 1 people.'],
             'blocks': [row(I1, 'Same five people facing North (Illustration 1)'), row(I2, 'Facing South with the same clues — the order flips (Illustration 2)')],
             'analogy': 'A team photograph: when the players face the camera, the player on their right is on your left.',
             'work': 'Directions in drawings, site plans and photographs of assets taken for verification depend on which way the viewer faces — exactly the left/right flip in this topic.'},
            {'id': 'c3', 'title': 'Two rows facing each other', 'body': [
                'Usually one row faces South and the other faces North, each person facing the one directly opposite.',
                'For the row facing North, left/right match yours; for the row facing South, they are reversed. Write the two rows one above the other and mark the facing with arrows.',
                'Diagonally opposite = the end seat of one row and the far end seat of the other row.'],
             'analogy': 'Two teams at a negotiation table: my right-hand neighbour sits across from the other side\'s left-hand neighbour.',
             'work': 'Meeting-room seating for a due-diligence or audit closing meeting is often two rows facing each other — the same reading of left, right and opposite applies.'},
            {'id': 'c4', 'title': 'Circular arrangements', 'body': [
                'Facing the centre: a person\'s left is the clockwise direction and right is the anticlockwise direction (seen from above).',
                'Facing outward: the opposite — left is anticlockwise and right is clockwise.',
                'In a circle of n (n even), the person opposite you is n/2 seats away in either direction. The k-th person to your left is the (n − k)-th to your right.',
                'Rotating every person by the same number of seats gives the same arrangement, so fix one person first and place the others relative to them. Mixed facing (some in, some out) must be handled person by person.'],
             'blocks': [circ(B, 'Six people facing the centre (MCQ set B): left of each person = next name in this list')],
             'analogy': 'Sitting round a dinner table facing the food: passing a dish to your left sends it clockwise round the table.',
             'work': 'Round-table seating at board and audit-committee meetings is planned with these rules — for instance, keeping the statutory auditor away from the person whose area is under discussion.'},
            {'id': 'c5', 'title': 'Method — from clues to diagram', 'body': [
                'Step 1: count the people and note the shape (row/circle) and the facing.',
                'Step 2: draw the empty seats. Place definite information first.',
                'Step 3: chain comparative clues to placed people. Where a clue fits in two ways, draw both cases side by side.',
                'Step 4: use negative clues and any remaining clue to strike out the impossible case.',
                'Step 5: verify every clue on the final diagram, then answer all linked questions from it.'],
             'analogy': 'Like reconciling a bank statement: tick the certain items first, match the related ones, and investigate what is left.',
             'work': 'Breaking a messy problem into fixed facts, relationships and exclusions is the core of audit planning and of drafting a complex consolidation.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Five in a row facing North', 'difficulty': 'core', 'minutes': 3,
             'q': 'Asha, Bina, Chetan, Dev and Esha sit in a row facing North. Chetan is second to the left of Dev. Asha sits to the immediate right of Esha. Bina is at neither end. Esha sits at one of the ends. Find the arrangement and say who sits in the middle.',
             'solution': [p('Definite-type clue: Esha is at an end. Comparative: Asha is just right of Esha — so Esha must be at the LEFT end (if Esha were at the right end, there would be no seat to her right). Seats 1–2: Esha, Asha.'),
                          p('Chetan is second to the left of Dev: Chetan and Dev occupy seats k and k + 2 among seats 3–5, so Chetan 3, Dev 5. Bina takes seat 4 (not an end — consistent).'),
                          row(I1, 'Final arrangement'), p(f'Middle seat: {I1[2]}.')]},
            {'id': 'i2', 'title': 'The same clues with the row facing South', 'difficulty': 'moderate', 'minutes': 3,
             'q': 'Repeat Illustration 1 if the five face South (towards you). Who now sits at your extreme left?',
             'solution': [p('Facing South, a person\'s right is your left. "Asha to the immediate right of Esha" now means Asha is one seat to YOUR left of Esha, so Esha must be at YOUR right end. "Chetan second to the left of Dev" means Chetan is two seats to YOUR right of Dev.'),
                          row(I2, 'Arrangement as seen by you'), p(f'Your extreme left: {I2[0]}. Every clue still holds; the picture is simply the mirror image of Illustration 1.')]},
            {'id': 'i3', 'title': 'Seven in a row (MCQ set A worked)', 'difficulty': 'hard', 'minutes': 5,
             'q': 'A, B, C, D, E, F and G sit in a row facing North. G is in the middle. E sits at one end. B is to the immediate left of E. D sits between G and B. A is second to the right of C. F is not at an end. Find the arrangement.',
             'solution': [p('G = seat 4 (middle of 7). B is immediately left of E, so E must be at the RIGHT end: E = 7, B = 6. D between G (4) and B (6): D = 5.'),
                          p('Left seats 1, 2, 3 remain for A, C, F. A is second to the right of C: C = 1, A = 3 (C = 2 would need A = 4, which is G). F = 2 — not an end, as required.'),
                          row(A, 'Final arrangement')]},
            {'id': 'i4', 'title': 'Circle of six facing the centre (MCQ set B worked)', 'difficulty': 'moderate', 'minutes': 4,
             'q': 'K, L, M, N, O and P sit round a circular table facing the centre. M is to the immediate left of K. O sits opposite K. N is to the immediate right of K. L sits between M and O. Find the arrangement.',
             'solution': [p('Fix K. Facing the centre, left = clockwise: M is the next seat clockwise from K; N is the next seat anticlockwise. O is 3 seats away (opposite).'),
                          p('Clockwise from K: K, M, _, O, _, N. L sits between M and O, so L takes the seat after M; P takes the last seat.'),
                          circ(B, 'Clockwise order')]},
            {'id': 'i5', 'title': 'Eight round a table, men and women alternating', 'difficulty': 'hard', 'minutes': 6,
             'q': 'Four women A, B, C, D and four men E, F, G, H sit round a table facing the centre; no two women sit together. C sits opposite A. E is to the immediate left of A and H to the immediate right of A. G sits opposite E. B sits between E and F. Find the arrangement.',
             'solution': [p('Fix A. Clockwise (A\'s left): E next; anticlockwise (A\'s right): H. C is 4 seats from A.'),
                          p('Clockwise: A, E, _, _, C, _, _, H. G is opposite E, i.e. 4 seats from E: G takes seat 6. B sits between E and F: B in seat 3 and F in seat 4 (alternation: seats 1, 3, 5, 7 women; 2, 4, 6, 8 men — B a woman in seat 3, F a man in seat 4). D takes seat 7.'),
                          circ(C, 'Clockwise order')]},
            {'id': 'i6', 'title': 'Two rows facing each other (MCQ set D worked)', 'difficulty': 'moderate', 'minutes': 4,
             'q': 'P, Q and R sit in a row facing South; X, Y and Z sit in a parallel row facing North, each person facing one person of the other row. Q faces Y. P is to the immediate right of Q. X sits at an end but does not face R. Find the arrangement.',
             'solution': [p('Q faces South, so P (to Q\'s right) is one seat to YOUR left of Q. Q cannot be at your left end; Q at your right end would put Y at the right end and leave X only the end facing R, which is barred. So Q is in the middle: P–Q–R from your left, and Y is in the middle of the other row.'),
                          p('X at an end not facing R: X faces P (your left). Z faces R.'),
                          table(['Row', 'Your left', 'Middle', 'Your right'], [['Facing South', 'P', 'Q', 'R'], ['Facing North', 'X', 'Y', 'Z']], title='Two rows')]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Seating plan for an audit committee meeting', 'role': 'Company secretary / CA in a listed company', 'situation': 'Six people will sit at a round table: the chair, the CFO, the statutory auditor, the internal auditor and two independent directors. The chair wants the statutory auditor directly opposite her, the CFO on her immediate left, and the two independent directors not next to each other.',
             'steps': ['Fix the chair first (definite information).', 'Place the statutory auditor three seats away (opposite) and the CFO clockwise next to the chair (left of a person facing the centre).', 'Two seats remain on one side and one on the other; seat the independent directors one on each side of the auditor so they are not neighbours, and give the internal auditor the leftover seat.', 'Check every condition and circulate the plan with the agenda.'],
             'takeaway': 'A seating puzzle is just a set of constraints. Solving it in the right order avoids last-minute reshuffles.',
             'think': 'Can both independent directors sit next to the statutory auditor?', 'answer': 'Yes — the two seats beside the auditor are not next to each other (the auditor sits between them), so that satisfies the "not neighbours" condition.'},
            {'id': 'j2', 'title': 'Reading a two-row panel photograph', 'role': 'Articled assistant preparing an annual-report check', 'situation': 'The caption under the board photograph reads "Left to right: …". The directors face the camera.',
             'steps': ['Captions normally list names from the viewer\'s left to right.', 'The director on the viewer\'s left is on his or her own right — a "facing South" row.', 'Match each name to the face using the company\'s own records before the report is printed.'],
             'takeaway': 'Whenever people face you, their left and right are the reverse of yours — check which convention a document uses.'},
        ],
        'mcqs': [
            M('m1', 'People sit round a table facing the centre. Moving to a person\'s left means moving:', ['Clockwise', 'Anticlockwise', 'Towards the centre', 'Either way, it depends on the table'], 0, "Imagine sitting at the table looking at the centre: your left hand points clockwise when the table is seen from above. So moving to a person's left means moving clockwise. Anticlockwise is the trap: that is the rule when people face outward. In practice: arranging seats for a board meeting or an audit committee, a company secretary uses this rule to place directors as instructed.", 'c4', topic='Circular arrangements'),
            M('m2', 'People sit round a table facing outward. Moving to a person\'s left means moving:', ['Anticlockwise', 'Clockwise', 'Towards the centre', 'Across the table'], 0, "When people face outward, everything flips: a person's left hand now points anticlockwise (seen from above). So moving to the left means moving anticlockwise. Clockwise is the trap: it applies only when people face the centre. In practice: reading the question's facing direction first avoids exactly this error, just as reading the reporting framework first avoids applying the wrong standard.", 'c4', topic='Circular arrangements'),
            M('m3', 'Five people sit in a row facing you. The person at YOUR extreme left is at THEIR:', ['Extreme right', 'Extreme left', 'Middle', 'Second seat from the left'], 0, "People facing you have their left and right reversed relative to yours. The person at your extreme left is therefore at their extreme right. Extreme left is the trap: it describes the seat from your viewpoint instead of the sitters'. In practice: when a client describes 'the rack on my right' while facing you across a godown, you must translate it to your own left before planning the count.", 'c2', topic='One row: facing North vs facing South'),
            M('m4', '"A sits second to the right of E" is an example of:', ['Comparative information', 'Definite information', 'Negative information', 'Irrelevant information'], 0, "This clue places A only in relation to E, so it is comparative information. It becomes useful once E's seat is known. Definite information is the trap: a definite clue fixes a seat on its own, such as 'A sits at the left end'. In practice: auditors also chain relative evidence, such as one balance agreed to another, only after an anchor figure has been confirmed.", 'c1', topic='Types of arrangement and types of information'),
            M('m5', '"C is not sitting next to A" is an example of:', ['Negative information', 'Definite information', 'Comparative information', 'Circular information'], 0, "The clue does not place C anywhere; it only removes some seats as possibilities, so it is negative information. It is used last, to choose between cases left over. Comparative information is the trap: a comparative clue positively places one person relative to another. In practice: negative findings in audit, such as 'no related-party transactions above ₹1 lakh', also only narrow down possibilities.", 'c1', topic='Types of arrangement and types of information'),
            M('m6', '"X sits at the right end of the bench" is an example of:', ['Definite information', 'Negative information', 'Comparative information', 'Conditional information'], 0, 'The right end of a bench is a single, fixed seat, so the clue places X with no reference to anyone else. That is definite information, and it should be used first. Comparative information is the trap: it needs another person as reference. In practice: starting from a confirmed fixed point, such as the bank balance per certificate, is how every reconciliation begins.', 'c1', topic='Types of arrangement and types of information'),
            M('m7', 'Nine people sit round a table facing the centre. B is 4th to the left of A. How many people sit between them on the clockwise side from A to B?', ['3', '4', '5', '2'], 0, "Facing the centre, left means clockwise. B is 4th to the left of A, so B is 4 seats clockwise from A. The seats in between are 4 − 1 = 3 people. The trap is 4, which counts B's seat as well. In practice: counting 'between' versus 'up to and including' is the same care needed when counting days for interest or working days for a statutory deadline.", 'c4', 'moderate', '4-1', topic='Circular arrangements'),
            M('m8', 'Eight people sit round a table facing the centre. The person 3rd to the right of X is also how many places to the left of X?', ['5', '3', '4', '6'], 0, "Round a table of 8, going 3 places one way is the same as going 8 − 3 = 5 places the other way. So the person 3rd to the right of X is 5th to the left of X. The trap is 3, which assumes left and right counts are equal. In practice: this 'go the other way round' trick is how roster and shift rotations are worked out in a circular cycle.", 'c4', 'moderate', '8-3', topic='Circular arrangements'),
            M('m9', 'Seven people sit in a row. How many people sit to the right of the person in the middle?', ['3', '4', '2', '7'], 0, 'In a row of 7 the middle person is in seat 4. The remaining 6 people split equally, (7 − 1) ÷ 2 = 3 on each side, so 3 people sit to the right. The trap is 4, which wrongly includes the middle person. In practice: the middle position of an odd list is also how the median is located when arranging data in order.', 'c2', 'core', '(7-1)/2', topic='One row: facing North vs facing South'),
            M('m10', 'In a row, Ravi is 9th from the left end and 6th from the right end. How many people are in the row?', ['14', '15', '13', '16'], 0, 'Ravi is counted in both positions, so the total = 9 + 6 − 1 = 14. The trap is 15, which adds the two ranks without removing the double count. In practice: avoiding double counting is a constant concern, for example when consolidating two branches that both record the same inter-branch transfer.', 'c2', 'moderate', '9+6-1', topic='One row: facing North vs facing South'),
            M('m11', 'MCQ set A (Illustration 3): who sits at the extreme left?', ['C', 'E', 'F', 'A'], 0, 'Solving the clues of Illustration 3 for seven people facing North gives the order, from left to right: C, F, A, G, D, B, E. The extreme left seat is C. E is the trap: it sits at the other end (extreme right). In practice: once the diagram is drawn correctly, several follow-up questions can be answered from it, just as one well-built working paper answers many review points.', 'c2', 'moderate', topic='One row: facing North vs facing South'),
            M('m12', 'MCQ set A: who sits between A and D?', ['G', 'B', 'F', 'C'], 0, 'In the final row C, F, A, G, D, B, E, seats 3, 4 and 5 are A, G and D. So G sits between A and D. B is the trap: it sits next to D but on the other side. In practice: reading neighbours correctly from one diagram is like reading adjacent line items in a trial balance; one wrong row and every linked answer goes wrong.', 'c2', 'moderate', topic='One row: facing North vs facing South'),
            M('m13', 'MCQ set A: how many people sit between F and B?', ['3', '2', '4', '1'], 0, "F is in seat 2 and B is in seat 6. The seats strictly between them are 3, 4 and 5, so 6 − 2 − 1 = 3 people sit between F and B. The trap is 4, which subtracts the seat numbers without removing one end. In practice: the same 'exclusive count' logic is used when counting the days between two dates for a penalty or interest calculation.", 'c2', 'moderate', '6-2-1', topic='One row: facing North vs facing South'),
            M('m14', 'MCQ set A: who is third to the left of D?', ['F', 'C', 'A', 'B'], 0, "The row faces North, so a person's left is the reader's left. D is in seat 5; three seats to the left is seat 2, which is F. B is the trap: it lies to D's right, so it comes from counting the wrong way. In practice: knowing which way the people face before counting is as basic as checking the sign convention before posting entries.", 'c2', 'moderate', topic='One row: facing North vs facing South'),
            M('m15', 'MCQ set A: which pair sits at the two ends?', ['C and E', 'C and B', 'F and E', 'A and E'], 0, 'The two end seats in the row C, F, A, G, D, B, E are seat 1 (C) and seat 7 (E). So the pair at the ends is C and E. C and B is the trap: B is second from the right end, not at the end. In practice: checking both ends of a list, such as the first and last cheque numbers in a series, is how gaps and missing items are spotted.', 'c2', 'core', topic='One row: facing North vs facing South'),
            M('m16', 'MCQ set B (Illustration 4): who sits opposite M?', ['P', 'N', 'O', 'L'], 0, "Solving Illustration 4 for six people facing the centre gives, clockwise: K, M, L, O, P, N. In a circle of 6, the person opposite is 3 seats away. M is seat 2, so seat 5, P, is opposite. O is the trap: it is only two seats from M. In practice: opposite-seat planning is common for negotiation meetings where each party's lead faces the other.", 'c4', 'moderate', topic='Circular arrangements'),
            M('m17', 'MCQ set B: who is to the immediate left of P?', ['N', 'O', 'K', 'L'], 0, "Facing the centre, left means clockwise. Clockwise order is K, M, L, O, P, N, so the seat just after P (seat 5) is N (seat 6). N is to P's immediate left. O is the trap: it is P's immediate right, reached by going anticlockwise. In practice: event planners for AGMs and board meetings arrange name cards using this clockwise rule.", 'c4', 'moderate', topic='Circular arrangements'),
            M('m18', 'MCQ set B: who is second to the right of L?', ['K', 'P', 'O', 'N'], 0, 'Facing the centre, right means anticlockwise. From L (seat 3), going two seats anticlockwise reaches seat 1, which is K. P is the trap: it is reached by going two seats clockwise, which is second to the left. In practice: a single direction error spoils every linked answer, which is why reviewers check the method, not just the final figure.', 'c4', 'moderate', topic='Circular arrangements'),
            M('m19', 'MCQ set B: who sits between O and N?', ['P', 'K', 'M', 'L'], 0, 'In the clockwise order K, M, L, O, P, N, seats 4, 5 and 6 are O, P and N. So P sits between O and N. K is the trap: K sits next to N but on the other side (between N and M round the circle). In practice: reading a circle in one consistent direction avoids such slips, just as using one consistent cut-off date avoids errors in accounts.', 'c4', 'core', topic='Circular arrangements'),
            M('m20', 'MCQ set C (Illustration 5): who sits opposite F?', ['H', 'G', 'E', 'D'], 0, 'Illustration 5 gives, clockwise: A, E, B, F, C, G, D, H, with men and women alternating. In a circle of 8 the opposite seat is 4 away. F is seat 4, so seat 8, H, is opposite. G is the trap: it is only two seats from F. In practice: alternating and opposite-seat rules are often specified for interview panels and committee meetings.', 'c4', 'hard', topic='Circular arrangements'),
            M('m21', 'MCQ set C: who is to the immediate right of D?', ['G', 'H', 'C', 'A'], 0, "Facing the centre, right means anticlockwise, i.e. the seat just before in the clockwise list. D is seat 7, so the seat before it, seat 6, is G. H is the trap: it is D's immediate left (the next seat clockwise). In practice: getting the direction rule right once and applying it every time is what keeps a multi-question puzzle consistent.", 'c4', 'hard', topic='Circular arrangements'),
            M('m22', 'MCQ set C: which woman sits to the immediate left of F?', ['C', 'B', 'D', 'A'], 0, "Left means clockwise when facing the centre. After F (seat 4) comes C (seat 5), and C is one of the women (A, B, C, D). So C is the woman to F's immediate left. B is the trap: B is F's immediate right. In practice: puzzles that mix two conditions (gender and position) mirror real tasks like staffing count teams with one senior beside each junior.", 'c4', 'hard', topic='Circular arrangements'),
            M('m23', 'MCQ set C: who is second to the right of B?', ['A', 'F', 'C', 'H'], 0, "Right means anticlockwise. From B (seat 3), going back two seats gives seat 1, A. F is the trap: it is only one seat from B, on the left side. In practice: counting 'second to the right' carefully is like counting the second preceding period in a trend analysis; starting the count from the wrong place shifts every figure.", 'c4', 'hard', topic='Circular arrangements'),
            M('m24', 'MCQ set C: going clockwise from A to C, how many people sit between them?', ['3', '4', '2', '5'], 0, "A is seat 1 and C is seat 5. Going clockwise, the seats between them are 2, 3 and 4, so 5 − 1 − 1 = 3 people. Because A and C are opposite in a circle of 8, there are also 3 on the other side. The trap is 4, which forgets to exclude one end. In practice: 'how many in between' counting matters when computing days between two dates for interest.", 'c4', 'moderate', '5-1-1', topic='Circular arrangements'),
            M('m25', 'MCQ set D (Illustration 6): who faces X?', ['P', 'Q', 'R', 'Y'], 0, 'In Illustration 6 the two rows face each other, so each person faces the one in the same column of the other row. X and P are both in the column at your left, so P faces X. Q is the trap: Q faces Y, the middle person. In practice: arranging a negotiation table so each finance lead faces the counterpart uses this same column logic.', 'c3', 'moderate', topic='Two rows facing each other'),
            M('m26', 'MCQ set D: who is diagonally opposite R?', ['X', 'Z', 'Y', 'P'], 0, "R sits at your right end of the South-facing row. The diagonally opposite seat is the far end of the other row, at your left, which is X. Z is the trap: Z faces R directly, so Z is opposite, not diagonally opposite. In practice: 'opposite' versus 'diagonally opposite' is exactly the kind of wording a careful reader must not blur.", 'c3', 'moderate', topic='Two rows facing each other'),
            M('m27', 'MCQ set D: who is to the immediate left of Q?', ['R', 'P', 'Y', 'X'], 0, "Q sits in the row facing South, so Q's left is your right. The person next to Q on your right is R, so R is to Q's immediate left. P is the trap: P is to your left of Q, which is Q's right. In practice: whenever someone faces you, their left is your right; mixing this up is a common error when taking directions on a site visit.", 'c3', 'hard', topic='Two rows facing each other'),
            M('m28', 'MCQ set D: who is to the immediate left of Y?', ['X', 'Z', 'Q', 'P'], 0, "Y sits in the row facing North, the same way as you, so Y's left is your left. The person next to Y on your left is X. Z is the trap: Z is on Y's right. In practice: always fix which way each person faces before reading left and right, as you would fix the reporting entity before deciding whose asset or liability a balance is.", 'c3', 'moderate', topic='Two rows facing each other'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Six people U, V, W, X, Y and Z sit in a row facing North. X sits at the right end. U is third to the left of X. W and Y are neighbours and W sits at an end. V is not next to U. (a) Draw the arrangement. (b) Who sits fourth from the left? (c) Who sits between U and V?',
             'model': [p('X = seat 6 (right end). U is third to the left of X: seat 6 − 3 = 3.'),
                       p('W sits at an end; the right end is taken, so W = seat 1 and Y (neighbour) = seat 2.'),
                       p('Seats 4 and 5 remain for V and Z. V is not next to U (seat 3), so V = 5 and Z = 4.'),
                       row(Q1, '(a) Arrangement'), p(f'(b) Fourth from the left: {Q1[3]}.  (c) Between U and V: {Q1[3]}.')],
             'scheme': [{'id': 's1', 'pt': 'X and U placed using definite and comparative clues', 'm': 1, 'skill': 'analysis'},
                        {'id': 's2', 'pt': 'W at left end and Y beside W', 'm': 1, 'skill': 'analysis'},
                        {'id': 's3', 'pt': 'Negative clue used to fix V and Z', 'm': 1, 'skill': 'application'},
                        {'id': 's4', 'pt': '(b) and (c) answered: Z, Z', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Good answers say which clue is used at each step.'], 'mistakes': ['Counting "third to the left" as seat 2 by including X.', 'Putting W at the right end without noticing X is already there.'],
             'tips': ['Number the seats from the left before you start.'], 'checks': c_q1},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
             'q': 'Six friends R, S, T, U, V and W sit round a circular table facing OUTWARD. U sits opposite R. S is to the immediate left of T. W is to the immediate right of R. V sits next to U. T is not next to W. Find the arrangement and answer: (a) Who sits opposite W? (b) Who is to the immediate left of V? (c) Who sits between U and T?',
             'model': [p('Facing outward, a person\'s right is clockwise and left is anticlockwise.'),
                       p('Fix R. W (R\'s right) is the next seat clockwise. U is three seats from R.'),
                       p('Clockwise: R, W, _, U, _, _. V sits next to U: seat 3 or 5. S is just left (anticlockwise) of T, so S and T occupy consecutive seats with S first in clockwise order: the free pairs are (5, 6) or, if V is in seat 5, none. So V = 3, S = 5, T = 6. T (seat 6) is next to R and seat 5, not to W — consistent.'),
                       circ(Q2, 'Clockwise order'),
                       p('(a) Opposite W (seat 2) is seat 5 — S. (b) Left of V = anticlockwise neighbour — W. (c) Between U (seat 4) and T (seat 6) — S.')],
             'scheme': [{'id': 's1', 'pt': 'Outward facing: right = clockwise, left = anticlockwise', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'R, W and U placed', 'm': 1, 'skill': 'analysis'},
                        {'id': 's3', 'pt': 'V, S, T placed; negative clue checked', 'm': 1, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'All three answers: S, W, S', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Most wrong answers come from using the facing-the-centre rule for an outward-facing table.'], 'mistakes': ['Placing W anticlockwise of R.', 'Not checking the last (negative) clue.'],
             'tips': ['Write "OUT: L = anticlockwise" in the corner of the diagram before placing anyone.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Explain, with a small example for each, how "to the immediate left of" is read in (a) a row facing North, (b) a row facing South, (c) a circle facing the centre and (d) a circle facing outward.',
             'model': [table(['Case', 'Rule', 'Example'], [
                 ['(a) Row facing North', 'Same as your left', 'In P Q R facing North, P is immediately left of Q'],
                 ['(b) Row facing South', 'Opposite of your left — the seat to YOUR right', 'In P Q R (your view) facing South, R is immediately left of Q'],
                 ['(c) Circle facing centre', 'Next seat clockwise', 'With K, M clockwise, M is immediately left of K'],
                 ['(d) Circle facing outward', 'Next seat anticlockwise', 'With R, W clockwise (outward), R is immediately left of W'],
             ])],
             'scheme': [{'id': 's1', 'pt': '(a) row facing North', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': '(b) row facing South', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': '(c) facing centre — clockwise', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': '(d) facing outward — anticlockwise', 'm': 1, 'skill': 'concept'}],
             'remarks': ['A four-row table answers this in under two minutes.'], 'mistakes': ['Saying left is anticlockwise for a table facing the centre.'],
             'tips': ['Imagine sitting in the seat yourself and pointing with your left hand.']},
        ],
        'revision': {
            'summary': ['Clues: definite (fixes a seat) → comparative (relative to someone placed) → negative (eliminates). Verify every clue at the end.',
                        'Row facing North (or direction not given): their left/right = yours. Row facing South: reversed.',
                        'Two rows facing each other: same column = facing; end of one row and far end of the other = diagonally opposite.',
                        'Circle facing centre: left = clockwise, right = anticlockwise. Facing outward: left = anticlockwise, right = clockwise.',
                        'Circle of n: opposite = n/2 seats away; k-th to the left = (n − k)-th to the right.'],
            'remember': ['Row: p-th from left and q-th from right → p + q − 1 people.', 'People between two seats i and j in a row: |i − j| − 1.', '"Immediate" = next seat; "to the left" = anywhere on that side.'],
            'traps': ['Using the North rule for a row facing you.', 'Using the centre rule for an outward-facing circle.', 'Counting the reference person when finding "third to the left".', 'Answering from a half-finished diagram before checking negative clues.']},
        'quickref': [{'k': 'Facing North row', 'v': 'Left/right = yours'}, {'k': 'Facing South row', 'v': 'Left/right reversed'},
                     {'k': 'Circle, facing centre', 'v': 'Left = clockwise, right = anticlockwise'}, {'k': 'Circle, facing outward', 'v': 'Left = anticlockwise, right = clockwise'},
                     {'k': 'Opposite in a circle of n', 'v': 'n/2 seats away'}, {'k': 'k-th left in a circle of n', 'v': '= (n − k)-th right'}, {'k': 'Row size', 'v': 'p-th from left + q-th from right − 1'}],
        'viva': [
            V('v1', 'What are definite, comparative and negative information in a seating puzzle? Give an example of each.',
              'Definite information fixes a person\'s seat by itself, for example X sits at the right end. Comparative information places a person relative to another, for example A is second to the right of E. Negative information only rules out a seat, for example C is not next to A. Definite clues are used first, then comparative, and negative clues to eliminate cases.',
              [P('p1', 'Definite: fixes a seat by itself (e.g. at the right end)', 3, 'definite fix|definite exact|definite certain|definite particular|definite specific|definite clear|definite seat|definite position|definite tell exact|definite give exact|definite end|definite middle|definite inform fix|definite clue fix|definite place'),
               P('p2', 'Comparative: relative to another person (e.g. second to the right of E)', 3, 'comparative relative|comparative relation|comparative another|comparative other person|comparative respect|comparative reference|comparative compar|comparative position relative|comparative information relative|comparative information another|comparative clue relative|comparative clue another|comparative place relative|comparative someone else|comparative person relative'),
               P('p3', 'Negative: only rules out / eliminates (e.g. not next to)', 3, 'negative rule|negative eliminat|negative exclud|negative not next|negative remov|negative cannot|negative only|negative does not place|negative never place|negative information rule|negative information eliminat|negative clue eliminat|negative clue rule|negative tell not|negative strike|negative cross out|negative not sit'),
               P('p4', 'Order: definite first, then comparative, then negative', 1, 'definite first|start with definite|first definite|begin with definite|definite clue first|use definite')], 'c1'),
            V('v2', 'In a circular arrangement, how are left and right read when people face the centre and when they face outward?',
              'When people face the centre, a person\'s left is clockwise and the right is anticlockwise. When they face outward it reverses: the left is anticlockwise and the right is clockwise.',
              [P('p1', 'Facing centre: left = clockwise', 4, 'centre left clockwise|center left clockwise|centre left is clockwise|centre their left clockwise|center their left clockwise|centre person left clockwise|center person left clockwise|inside left clockwise|inward left clockwise|centre left means clockwise|center left means clockwise|centre left goes clockwise'),
               P('p2', 'Facing centre: right = anticlockwise', 2, 'right anticlockwise|right anti clockwise|right counter clockwise|right counterclockwise|right is anticlockwise|right is anti clockwise'),
               P('p3', 'Facing outward: reversed — left = anticlockwise, right = clockwise', 4, 'outward left anticlockwise|outward left anti clockwise|outward left counter|outside left anticlockwise|outside left anti clockwise|outward revers|outward opposite|outward it revers|outward everything revers|outward other way|outward flip|outward swap')], 'c4'),
            V('v3', 'How does the reading of left and right change between a row facing North and a row facing South?',
              'In a row facing North, the people\'s left and right are the same as mine. In a row facing South, they face me, so their left and right are the opposite of mine: someone to the immediate right of a person is actually one seat to my left.',
              [P('p1', 'Facing North: same as the viewer\'s left/right', 5, 'north same|north their left right same|north same as mine|north same as ours|north same as yours|north same as viewer|north matches|north same direction|north identical|north just like'),
               P('p2', 'Facing South (towards you): reversed', 5, 'south opposite|south revers|south flip|south swap|south mirror|south interchang|south other way|south face me opposite|south facing me opposite|south toward opposite|south towards opposite|south face us opposite|south facing us opposite|south face you opposite')], 'c2'),
            V('v4', 'What is the difference between "to the left of" and "to the immediate left of"?',
              'Immediate left means the very next seat on the left side, with nobody in between. To the left of means anywhere on the left side, so there may be other people in between.',
              [P('p1', '"Immediate left" = the very next seat, nobody between', 5, 'immediate next|immediate adjacent|immediate beside|immediate directly|immediate left next|immediate left very next|immediate left adjacent|immediate left beside|immediate left directly|immediate left person sit next|immediate left sitting next|immediate left seat next|immediate left person right next|immediate left nobody between|immediate left no one between|immediate left one seat'),
               P('p2', '"To the left" = anywhere on that side; people may be between', 5, 'left anywhere|left any seat|left any position|left could any|left could be any|left somewhere|left whole side|left entire side|left could be people|left may be people|left people in between|left others in between|left not necessarily next|left need not|left not always next|left not just next')], 'c2'),
            V('v5', 'Describe the steps you follow to solve a seating arrangement puzzle.',
              'First count the people and note whether it is a row or a circle and which way they face. Draw the empty seats and place the definite information. Then chain the comparative clues to people already placed, drawing two cases if needed. Use the negative clues to strike out impossible cases, and finally check every clue against the finished diagram before answering.',
              [P('p1', 'Note number of people, shape (row/circle) and facing', 2, 'count|number of people|how many|row or circle|shape|facing|which way'),
               P('p2', 'Draw seats; place definite information first', 3, 'draw|diagram|sketch|seat', 'definite|fixed|certain|sure', min=2),
               P('p3', 'Chain comparative clues; draw cases', 2, 'comparative|relative|chain|case|possibilit'),
               P('p4', 'Use negative clues to eliminate', 2, 'negative|eliminat|strike out|rule out|cross out|discard'),
               P('p5', 'Verify every clue at the end', 1, 'check|verify|confirm|recheck|cross check')], 'c5'),
            V('v6', 'In two rows facing each other, how do you tell who faces whom and who is diagonally opposite?',
              'The person directly across in the same column faces you. Diagonally opposite means one end of one row and the far end of the other row. Remember that the row facing south has left and right reversed compared with the row facing north.',
              [P('p1', 'Same column / directly across = facing', 4, 'same column|directly across|straight across|directly opposite|right across|exactly opposite|in front|same position|same place|across from'),
               P('p2', 'Diagonally opposite = end of one row and far end of the other', 4, 'diagonal', 'end|corner|far|other side|extreme'),
               P('p3', 'South-facing row has left/right reversed', 2, 'revers|opposite|flip|swap|mirror|interchang')], 'c3'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Board meeting round table', 'difficulty': 'hard',
            'case': 'Six directors — Ahuja, Bose, Chawla, Dutta, Iyer and Jain — sit round a circular table facing the centre. Jain sits opposite Ahuja. Iyer is to the immediate left of Ahuja. Chawla is second to the left of Bose. Dutta is not next to Iyer.',
            'mcqs': [
                M('k1a', 'Who sits between Jain and Dutta?', ['Chawla', 'Bose', 'Iyer', 'Ahuja'], 0, 'Solving the clues: clockwise from Ahuja the order is Ahuja, Iyer, Bose, Jain, Chawla, Dutta. Jain is seat 4 and Dutta is seat 6, so Chawla (seat 5) sits between them. Bose is the trap: Bose sits next to Jain but on the other side. In practice: seating directors for a board meeting under several conditions is exactly this kind of constraint puzzle.', 'c4', 'hard', topic='Circular arrangements'),
                M('k1b', 'Who sits opposite Bose?', ['Dutta', 'Chawla', 'Ahuja', 'Iyer'], 0, 'In a circle of 6, the opposite seat is 3 places away. Bose is seat 3, so seat 6, Dutta, is opposite. Chawla is the trap: Chawla is only two seats from Bose (second to the left). In practice: company secretaries often place the chairperson opposite the CEO or the auditor; counting half the table finds the opposite seat quickly.', 'c4', 'moderate', topic='Circular arrangements'),
                M('k1c', 'Who is to the immediate right of Jain?', ['Bose', 'Chawla', 'Iyer', 'Dutta'], 0, "Facing the centre, right means anticlockwise, i.e. the seat just before in the clockwise list. Jain is seat 4, so the seat before is seat 3, Bose. Chawla is the trap: Chawla is Jain's immediate left. In practice: a single left–right slip changes who sits beside whom, which matters when protocol says the independent director must sit beside the chair.", 'c4', 'hard', topic='Circular arrangements'),
                M('k1d', 'If Ahuja and Chawla exchange seats, who will sit opposite Jain?', ['Chawla', 'Ahuja', 'Dutta', 'Bose'], 0, "Jain sits opposite seat 1, Ahuja's original seat. After Ahuja and Chawla swap, Chawla occupies seat 1, so Chawla is now opposite Jain. Ahuja is the trap: it ignores the swap and keeps the old seating. In practice: when one change is made to a seating plan, only the moved people's relations change; the rest of the diagram stays valid, which saves redrawing.", 'c4', 'moderate', topic='Circular arrangements'),
            ]}],
    }
