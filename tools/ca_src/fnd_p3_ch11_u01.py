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


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
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
            M('m1', 'People sit round a table facing the centre. Moving to a person\'s left means moving:', ['Clockwise', 'Anticlockwise', 'Towards the centre', 'Either way, it depends on the table'], 0, 'Facing the centre, the left hand points clockwise (seen from above).', 'c4'),
            M('m2', 'People sit round a table facing outward. Moving to a person\'s left means moving:', ['Anticlockwise', 'Clockwise', 'Towards the centre', 'Across the table'], 0, 'Facing outward reverses the rule: left is anticlockwise.', 'c4'),
            M('m3', 'Five people sit in a row facing you. The person at YOUR extreme left is at THEIR:', ['Extreme right', 'Extreme left', 'Middle', 'Second seat from the left'], 0, 'People facing you (South) have left and right opposite to yours.', 'c2'),
            M('m4', '"A sits second to the right of E" is an example of:', ['Comparative information', 'Definite information', 'Negative information', 'Irrelevant information'], 0, 'It places A only in relation to E.', 'c1'),
            M('m5', '"C is not sitting next to A" is an example of:', ['Negative information', 'Definite information', 'Comparative information', 'Circular information'], 0, 'It only removes possibilities.', 'c1'),
            M('m6', '"X sits at the right end of the bench" is an example of:', ['Definite information', 'Negative information', 'Comparative information', 'Conditional information'], 0, 'It fixes X\'s seat by itself.', 'c1'),
            M('m7', 'Nine people sit round a table facing the centre. B is 4th to the left of A. How many people sit between them on the clockwise side from A to B?', ['3', '4', '5', '2'], 0, 'Fourth to the left is 4 seats clockwise, so 4 − 1 = 3 people sit between them on that side.', 'c4', 'moderate', '4-1'),
            M('m8', 'Eight people sit round a table facing the centre. The person 3rd to the right of X is also how many places to the left of X?', ['5', '3', '4', '6'], 0, 'Going the other way round: 8 − 3 = 5.', 'c4', 'moderate', '8-3'),
            M('m9', 'Seven people sit in a row. How many people sit to the right of the person in the middle?', ['3', '4', '2', '7'], 0, '(7 − 1) ÷ 2 = 3 on each side.', 'c2', 'core', '(7-1)/2'),
            M('m10', 'In a row, Ravi is 9th from the left end and 6th from the right end. How many people are in the row?', ['14', '15', '13', '16'], 0, 'p + q − 1 = 9 + 6 − 1 = 14 (Ravi is counted in both).', 'c2', 'moderate', '9+6-1'),
            M('m11', 'MCQ set A (Illustration 3): who sits at the extreme left?', ['C', 'E', 'F', 'A'], 0, f'Arrangement: {", ".join(A)}.', 'c2', 'moderate'),
            M('m12', 'MCQ set A: who sits between A and D?', ['G', 'B', 'F', 'C'], 0, 'Seats 3, 4, 5 are A, G, D.', 'c2', 'moderate'),
            M('m13', 'MCQ set A: how many people sit between F and B?', ['3', '2', '4', '1'], 0, 'F is in seat 2 and B in seat 6: seats 3, 4, 5 lie between — 3 people.', 'c2', 'moderate', '6-2-1'),
            M('m14', 'MCQ set A: who is third to the left of D?', ['F', 'C', 'A', 'B'], 0, 'D is in seat 5; three seats to the left is seat 2 — F.', 'c2', 'moderate'),
            M('m15', 'MCQ set A: which pair sits at the two ends?', ['C and E', 'C and B', 'F and E', 'A and E'], 0, 'Seat 1 C, seat 7 E.', 'c2', 'core'),
            M('m16', 'MCQ set B (Illustration 4): who sits opposite M?', ['P', 'N', 'O', 'L'], 0, f'Clockwise: {", ".join(B)}. M is seat 2; opposite is seat 5 — P.', 'c4', 'moderate'),
            M('m17', 'MCQ set B: who is to the immediate left of P?', ['N', 'O', 'K', 'L'], 0, 'Left = clockwise: after P (seat 5) comes N (seat 6).', 'c4', 'moderate'),
            M('m18', 'MCQ set B: who is second to the right of L?', ['K', 'P', 'O', 'N'], 0, 'Right = anticlockwise: from L (seat 3) two seats back is seat 1 — K.', 'c4', 'moderate'),
            M('m19', 'MCQ set B: who sits between O and N?', ['P', 'K', 'M', 'L'], 0, 'Seats 4, 5, 6 are O, P, N.', 'c4', 'core'),
            M('m20', 'MCQ set C (Illustration 5): who sits opposite F?', ['H', 'G', 'E', 'D'], 0, f'Clockwise: {", ".join(C)}. F is seat 4; opposite is seat 8 — H.', 'c4', 'hard'),
            M('m21', 'MCQ set C: who is to the immediate right of D?', ['G', 'H', 'C', 'A'], 0, 'Right = anticlockwise: before D (seat 7) is G (seat 6).', 'c4', 'hard'),
            M('m22', 'MCQ set C: which woman sits to the immediate left of F?', ['C', 'B', 'D', 'A'], 0, 'Left = clockwise: after F (seat 4) is C (seat 5).', 'c4', 'hard'),
            M('m23', 'MCQ set C: who is second to the right of B?', ['A', 'F', 'C', 'H'], 0, 'Right = anticlockwise: from B (seat 3) back two seats is seat 1 — A.', 'c4', 'hard'),
            M('m24', 'MCQ set C: going clockwise from A to C, how many people sit between them?', ['3', '4', '2', '5'], 0, 'A seat 1, C seat 5: seats 2, 3, 4 lie between — 3 people (the same on the other side, since they are opposite).', 'c4', 'moderate', '5-1-1'),
            M('m25', 'MCQ set D (Illustration 6): who faces X?', ['P', 'Q', 'R', 'Y'], 0, 'X and P are in the same column (your left).', 'c3', 'moderate'),
            M('m26', 'MCQ set D: who is diagonally opposite R?', ['X', 'Z', 'Y', 'P'], 0, 'R is at your right end of the South-facing row; the far end of the other row is X.', 'c3', 'moderate'),
            M('m27', 'MCQ set D: who is to the immediate left of Q?', ['R', 'P', 'Y', 'X'], 0, 'Q faces South, so his left is your right — R.', 'c3', 'hard'),
            M('m28', 'MCQ set D: who is to the immediate left of Y?', ['X', 'Z', 'Q', 'P'], 0, 'Y faces North, so his left is your left — X.', 'c3', 'moderate'),
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
                M('k1a', 'Who sits between Jain and Dutta?', ['Chawla', 'Bose', 'Iyer', 'Ahuja'], 0, f'Clockwise from Ahuja: {", ".join(K)}. Jain (4) – Chawla (5) – Dutta (6).', 'c4', 'hard'),
                M('k1b', 'Who sits opposite Bose?', ['Dutta', 'Chawla', 'Ahuja', 'Iyer'], 0, 'Bose is seat 3; three seats on is seat 6 — Dutta.', 'c4', 'moderate'),
                M('k1c', 'Who is to the immediate right of Jain?', ['Bose', 'Chawla', 'Iyer', 'Dutta'], 0, 'Right = anticlockwise: the seat before Jain (4) is Bose (3).', 'c4', 'hard'),
                M('k1d', 'If Ahuja and Chawla exchange seats, who will sit opposite Jain?', ['Chawla', 'Ahuja', 'Dutta', 'Bose'], 0, 'Seat 1 (opposite Jain) will now be occupied by Chawla.', 'c4', 'moderate'),
            ]}],
    }
