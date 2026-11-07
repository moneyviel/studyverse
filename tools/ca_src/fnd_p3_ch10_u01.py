"""CA Foundation · Paper 3 Quantitative Aptitude · Part B Logical Reasoning · Chapter 10 Direction Sense Test.
Original problems. Every route is walked by the small simulator below; facing directions, final positions and distances are asserted."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch10-u01'

ANG = {'North': 0, 'North-East': 45, 'East': 90, 'South-East': 135, 'South': 180, 'South-West': 225, 'West': 270, 'North-West': 315}
NAME = {v: k for k, v in ANG.items()}
VEC = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}


def turn(face, how):
    """how: 'R' / 'L' (90°), 'B' (about turn) or a signed angle (+ clockwise)."""
    d = {'R': 90, 'L': -90, 'B': 180}.get(how, how)
    return NAME[(ANG[face] + d) % 360]


def walk(face, legs):
    """face: starting direction. legs: list of (turn or None, distance). Returns (x, y, final facing)."""
    x = y = 0
    for t, dist in legs:
        if t: face = turn(face, t)
        dx, dy = VEC[ANG[face]]
        x += dx * dist; y += dy * dist
    return x, y, face


def where(x, y):
    """8-point direction of (x, y) seen from the origin (quadrant name when off-axis)."""
    ns = 'North' if y > 0 else 'South' if y < 0 else ''
    ew = 'East' if x > 0 else 'West' if x < 0 else ''
    return f'{ns}-{ew}' if ns and ew else ns or ew


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def build():
    # ---------------- illustrations ----------------
    i1 = walk('North', [('R', 0), ('R', 0), ('L', 0)]); assert i1[2] == 'East'
    i2 = walk('North', [(None, 6), ('R', 8)]); assert i2[:2] == (8, 6) and where(8, 6) == 'North-East'
    c_i2 = Checks(); c_i2.add('(6**2+8**2)**0.5', 'shortest distance from the start (km)')
    i3 = walk('East', [(None, 5), ('L', 3), ('L', 9), ('L', 3)]); assert i3 == (-4, 0, 'South')
    c_i3 = Checks(); c_i3.add('9-5', 'net movement towards West (km)'); c_i3.add('3-3', 'net north-south movement (km)')
    # i4 shadow: morning shadow points West; shadow on his right => right = West => facing South
    assert turn('South', 'R') == 'West'
    # i5: P 3 km north of Q; R 4 km east of Q  -> P from R
    px, py, rx, ry = 0, 3, 4, 0; assert where(px - rx, py - ry) == 'North-West'
    c_i5 = Checks(); c_i5.add('(3**2+4**2)**0.5', 'distance between P and R (km)')
    # i6 headstand: facing North, normally right hand = East; inverted, it points West
    assert turn('North', 'R') == 'East' and turn('North', 'L') == 'West'

    # ---------------- MCQ facts ----------------
    assert walk('North', [('R', 0), ('R', 0), ('L', 0)])[2] == 'East'
    assert turn('West', 'L') == 'South' and turn('South', 'B') == 'North'
    assert turn('East', 45) == 'South-East' and turn('North-West', 'R') == 'North-East' and turn('North', -135) == 'South-West'
    m7 = walk('North', [(None, 4), ('R', 3)]); assert m7[:2] == (3, 4) and where(3, 4) == 'North-East'
    m9 = walk('South', [(None, 10), ('L', 5), ('L', 10)]); assert m9 == (5, 0, 'North') and where(5, 0) == 'East'
    m10 = walk('East', [(None, 12), ('L', 5)]); assert m10[:2] == (12, 5)
    m11 = walk('East', [(None, 7), ('L', 4), ('L', 10), ('L', 4)]); assert m11[:2] == (-3, 0) and where(-3, 0) == 'West'
    assert walk('East', [('R', 0), ('R', 0)])[2] == 'West'                       # morning, facing the sun
    m17 = walk('North', [(None, 3), ('L', 4), ('L', 3), ('R', 2)]); assert m17 == (-6, 0, 'West')
    assert where(0 - 5, 5 - 0) == 'North-West'                                   # A (0,5) seen from C (5,0)
    assert turn('North', 90) == 'East'                                            # hour hand at 3 when 12 points North
    assert turn('South-East', 270) == 'North-East' and turn(turn('North', 'L'), 135) == 'North-East'
    m23 = walk('East', [(None, 2), ('L', 6), ('R', 4)]); assert m23[:2] == (6, 6)
    m27 = walk('South', [(None, 20), ('R', 10), ('R', 20), ('L', 15)]); assert m27 == (-25, 0, 'West')
    # case: delivery rider
    k = walk('North', [(None, 2), ('R', 3), ('R', 6), ('L', 1)]); assert k == (4, -4, 'East')
    assert where(4, -4) == 'South-East'
    # questions
    q1 = walk('North', [(None, 9), ('R', 5), ('R', 3), ('L', 3)]); assert q1 == (8, 6, 'East')
    c_q1 = Checks(); c_q1.add('9-3', 'net northward movement (km)'); c_q1.add('5+3', 'net eastward movement (km)'); c_q1.add('(6**2+8**2)**0.5', 'shortest distance (km)')
    # q2: evening, shadow behind him -> sun in front -> facing West; after left turn -> South; headstand facing East: left hand?
    assert turn('West', 'L') == 'South' and turn('East', 'L') == 'North'
    # q3: K 3 km east of P; M 4 km north of K; T 6 km west of M  -> T from P
    T = (3 - 6, 0 + 4); assert T == (-3, 4) and where(*T) == 'North-West'
    c_q3 = Checks(); c_q3.add('((3-6)**2+4**2)**0.5', 'distance of T from P (km)')

    def tbl(rows, title):
        return table(['Leg', 'Turn', 'Now facing', 'Distance', 'Position after the leg (x = East, y = North)'], rows, title=title)

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch10', 'n': 1, 'title': 'Direction Sense Test',
        'outcomes': ['Name the four main and four intermediate directions and convert left/right turns and angles into a new facing direction.',
                     'Trace a multi-leg route on a rough sketch and state the final facing direction separately from the direction of the finish point from the start.',
                     'Compute the shortest distance between start and finish using net displacements and Pythagoras.',
                     'Solve sun-and-shadow, upside-down (headstand) and relative-position puzzles.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 45}, 'prereq': [],
                 'exam_tip': 'Always draw: put North at the top of your rough sheet, mark the start with a dot and draw each leg as you read. Most errors come from turning "left" while imagining yourself facing the paper instead of facing the direction of travel.'},
        'concepts': [
            {'id': 'c1', 'title': 'The eight directions', 'body': [
                'Four main (cardinal) directions: North, East, South and West, each 90° apart going clockwise. Four intermediate directions sit exactly halfway: North-East, South-East, South-West and North-West, at 45° from their neighbours.',
                'Opposite pairs: North–South, East–West, North-East–South-West, North-West–South-East.',
                'On paper the convention is North up, South down, East to the right and West to the left.'],
             'blocks': [table(['Direction', 'Angle clockwise from North', 'Opposite'], [[k, f'{v}°', NAME[(v + 180) % 360]] for k, v in ANG.items()], title='Direction wheel')],
             'analogy': 'Think of a clock lying flat with 12 pointing North: 3 is East, 6 is South, 9 is West, and the half-way numbers point to the intermediate directions.',
             'work': 'Site visits for physical verification — of a warehouse, a factory layout or land — often depend on reading a site plan correctly. Directions on title deeds and lease agreements (property bounded on the north by …) use exactly these terms.'},
            {'id': 'c2', 'title': 'Turns: left, right, angles and about-turn', 'body': [
                'A right turn is 90° clockwise from the direction you are facing; a left turn is 90° anticlockwise. Two right turns (or two left turns) make you face the opposite way; a right followed by a left (or a left then right) brings you back to your original facing.',
                'Angle turns: add the angle for clockwise, subtract for anticlockwise, and reduce by 360° if needed. Example: facing South-East (135°) and turning 270° clockwise gives 405° − 360° = 45°, i.e. North-East.',
                'About-turn or "turns back" means 180°.',
                'Left and right are always judged from the person\'s own facing direction, not from the reader\'s.'],
             'blocks': [table(['Facing', 'After a right turn', 'After a left turn', 'After an about-turn'], [[f, turn(f, 'R'), turn(f, 'L'), turn(f, 'B')] for f in ('North', 'East', 'South', 'West', 'North-East', 'South-West')], title='Turn table (generated)')],
             'analogy': 'A right turn is the minute hand moving a quarter of the clock forward; a left turn is moving it a quarter back.',
             'work': 'When a client\'s plant layout or a branch map is described verbally on a call, a CA preparing a physical-verification plan must translate "turn left after the gate" into the map correctly to plan count teams.'},
            {'id': 'c3', 'title': 'Final facing vs position from the start', 'body': [
                'Two different questions are asked: (a) Which direction is the person facing (or walking) now? — that is the direction of the last leg after the last turn. (b) In which direction is the person from the starting point? — that is found from the net displacement, not from the last turn.',
                'Net displacement: add all northward movement and subtract southward movement; add eastward and subtract westward. If the net north–south is zero, the person is due East or West; if the net east–west is zero, due North or South; otherwise, name the quadrant (e.g. North-East).',
                'Also asked: the direction of the start from the person — this is the opposite of the person\'s direction from the start.'],
             'analogy': 'Facing is the way your car\'s bonnet points; position is where your car is parked relative to home.',
             'work': 'In practice this is exactly how a net position is computed: debits and credits (north and south) cancel, and only the net balance matters.'},
            {'id': 'c4', 'title': 'Shortest distance — Pythagoras', 'body': [
                'After finding net east–west movement (x) and net north–south movement (y), the straight-line distance between start and finish is √(x² + y²).',
                'Common triples save time: 3-4-5, 6-8-10, 5-12-13, 8-15-17, 9-12-15. If x = y, the distance is x√2 (≈ 1.414x).',
                'Total distance walked is different — it is the sum of all legs. Read which one the question wants.'],
             'analogy': 'The crow flies straight over the houses (shortest distance); you walk along the roads (total distance).',
             'work': 'Distance computations appear in travel-claim checks: a claim for 25 km when the straight-line distance is 10 km may still be reasonable along roads — but a claim for 60 km needs a question.'},
            {'id': 'c5', 'title': 'Sun and shadow', 'body': [
                'The sun rises in the East and sets in the West. A shadow always falls on the side opposite the sun.',
                'Morning: sun in the East, shadow falls towards the West. Evening: sun in the West, shadow falls towards the East. Around noon in India the sun is high (roughly overhead), so shadows are shortest; such questions are normally set for morning or evening.',
                'Method: fix the shadow\'s direction from the time of day, then use "the shadow is on my left/right/in front/behind" to work out which way the person faces.'],
             'analogy': 'The shadow is the sun\'s opposite twin — wherever the sun is, the shadow points the other way.',
             'work': 'Rarely needed at a desk, but the method — fix one known reference, then deduce the rest — is how a CA reconciles any account: start from a confirmed balance and work outwards.'},
            {'id': 'c6', 'title': 'Upside down and relative-position puzzles', 'body': [
                'Headstand: a person standing on his head still faces the same direction, but his left and right hands swap sides. Facing North normally puts the right hand to the East; upside down it points West.',
                'Relative positions ("A is 3 km north of B, C is 4 km east of B …"): place one point at the origin, plot the others with coordinates, then read the required direction and distance between any two of them.',
                'A clock or map turned so that a given number points a stated direction can be solved the same way: find how much it has been rotated, then rotate every other mark by the same angle.'],
             'analogy': 'Doing a handstand is like looking at yourself in a mirror held above your head: front stays front, but left and right trade places.',
             'work': 'Coordinates are the language of geo-tagged evidence — photos of assets in physical verification carry latitude and longitude, and reading them relative to a known point is the same skill.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Facing direction after three turns', 'difficulty': 'core', 'minutes': 1,
             'q': 'Neha faces North. She turns right, then right again, then left. Which direction does she face now?',
             'solution': [table(['Step', 'Turn', 'Facing'], [['Start', '—', 'North'], ['1', 'Right (+90°)', 'East'], ['2', 'Right (+90°)', 'South'], ['3', 'Left (−90°)', 'East']], title='Working'),
                          p(f'She faces {i1[2]}. Short cut: right + right + left = one net right turn from North = East.')]},
            {'id': 'i2', 'title': 'Shortest distance with a 6-8-10 triangle', 'difficulty': 'core', 'minutes': 2,
             'q': 'Arjun walks 6 km North, turns right and walks 8 km. How far is he from the start and in which direction?',
             'solution': [tbl([['1', '—', 'North', '6 km', '(0, 6)'], ['2', 'Right', 'East', '8 km', '(8, 6)']], 'Route'),
                          p(f'Net: 8 km East and 6 km North. Distance = √(8² + 6²) = √100 = {c_i2[0]["value"]} km. Direction from start: {where(8, 6)}.')],
             'checks': c_i2},
            {'id': 'i3', 'title': 'A four-leg route that nearly closes', 'difficulty': 'moderate', 'minutes': 3,
             'q': 'Meera walks 5 km East, turns left and walks 3 km, turns left and walks 9 km, then turns left and walks 3 km. (a) Which way is she facing? (b) Where is she from the start?',
             'solution': [tbl([['1', '—', 'East', '5 km', '(5, 0)'], ['2', 'Left', 'North', '3 km', '(5, 3)'], ['3', 'Left', 'West', '9 km', '(−4, 3)'], ['4', 'Left', 'South', '3 km', '(−4, 0)']], 'Route'),
                          p(f'(a) After the last left turn she faces {i3[2]}.'),
                          p(f'(b) North 3 and South 3 cancel; East 5 and West 9 leave 4 km West. She is 4 km {where(i3[0], i3[1])} of the start — the facing direction (South) and the position (West) are different answers.')],
             'checks': c_i3},
            {'id': 'i4', 'title': 'Morning shadow on the right', 'difficulty': 'moderate', 'minutes': 2,
             'q': 'At 7 a.m. Ravi notices that his shadow falls exactly to his right. Which direction is he facing?',
             'solution': [p('At 7 a.m. the sun is in the East, so the shadow falls towards the West.'),
                          p('His right-hand side is therefore West. A person whose right is West is facing South (facing South, the right hand points West).'),
                          p('Answer: South.')]},
            {'id': 'i5', 'title': 'Relative positions on coordinates', 'difficulty': 'core', 'minutes': 2,
             'q': 'Point P is 3 km north of Q. Point R is 4 km east of Q. Find the direction and distance of P from R.',
             'solution': [p('Put Q at (0, 0). Then P = (0, 3) and R = (4, 0).'),
                          p(f'P − R = (−4, 3): 4 km West and 3 km North, so P is {where(-4, 3)} of R. Distance = √(4² + 3²) = {c_i5[0]["value"]} km.')],
             'checks': c_i5},
            {'id': 'i6', 'title': 'Standing on the head', 'difficulty': 'core', 'minutes': 1,
             'q': 'Kabir stands on his head with his face towards North. Which direction does his right hand point?',
             'solution': [p('Standing normally and facing North, the right hand points East.'),
                          p('Upside down, the face still points North but left and right swap, so the right hand now points West. Answer: West.')]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Planning a physical verification walk-through', 'role': 'Audit senior at a warehouse count', 'situation': 'The storekeeper describes the godown: "Enter by the main gate facing North. Racks A–D are on your right, the bonded area is straight ahead, and the scrap yard is behind the office on your left."',
             'steps': ['Sketch the plan with North at the top and the gate at the bottom.', 'Right of a person facing North is East: racks A–D lie on the East side; left is West: the office and scrap yard lie on the West side.', 'Allocate count teams by zone so that no rack is missed or counted twice.', 'Attach the sketch to the count instructions so every team uses the same reference.'],
             'takeaway': 'A sketch with a fixed North removes all left/right confusion — the same habit that solves direction questions in the exam.',
             'think': 'A team enters from the back door facing South. On which side will racks A–D be for them?', 'answer': 'Facing South, East is on their left — so racks A–D will appear on the left side.'},
            {'id': 'j2', 'title': 'Checking a conveyance claim', 'role': 'CA in industry reviewing staff reimbursements', 'situation': 'A sales executive claims 15 km for a client visit. On the map the client is 9 km East and 12 km North of the office.',
             'steps': ['Straight-line distance = √(9² + 12²) = 15 km.', 'Road distance is usually more than the straight-line distance, so 15 km is at the lower end of plausible.', 'Accept the claim and note the check in the reimbursement file.'],
             'takeaway': 'The straight-line distance is a floor, not a ceiling — claims below it are impossible, claims well above it need a question.',
             'checks': [{'expr': '(9**2+12**2)**0.5', 'value': 15, 'label': 'straight-line distance (km)'}],
             'think': 'If the claim had been 12 km, what would you conclude?', 'answer': '12 km is less than the straight-line distance of 15 km, so the claim cannot be right as stated — perhaps the wrong client address was used.'},
        ],
        'mcqs': [
            M('m1', 'Asha faces North. She turns right, right again and then left. Which way does she face now?', ['East', 'West', 'South', 'North'], 0, 'Right → East, right → South, left → East.', 'c2'),
            M('m2', 'A man facing West turns left. Which way does he face?', ['South', 'North', 'East', 'South-West'], 0, 'A left turn is 90° anticlockwise: from West (270°) to South (180°).', 'c2'),
            M('m3', 'A girl facing South makes an about-turn. Which way does she face?', ['North', 'South', 'East', 'West'], 0, 'An about-turn is 180°: the opposite of South is North.', 'c2'),
            M('m4', 'Facing East, Ravi turns 45° clockwise. Which way does he face?', ['South-East', 'North-East', 'South', 'North'], 0, 'East is 90°; 90° + 45° = 135°, which is South-East. North-East is the anticlockwise answer.', 'c2', 'moderate'),
            M('m5', 'A man facing North-West turns right. Which way does he face?', ['North-East', 'South-West', 'South-East', 'North'], 0, 'North-West is 315°; adding 90° gives 405° − 360° = 45°, North-East.', 'c2', 'moderate'),
            M('m6', 'Facing North, a boy turns 135° anticlockwise. Which way does he face?', ['South-West', 'South-East', 'North-West', 'West'], 0, '0° − 135° = −135° = 225°, which is South-West.', 'c2', 'moderate'),
            M('m7', 'Kiran walks 4 km North, turns right and walks 3 km. How far is she from the start?', ['5 km', '7 km', '1 km', '6 km'], 0, '√(3² + 4²) = 5 km. 7 km is the total distance walked, not the shortest distance.', 'c4', 'core', '(3**2+4**2)**0.5'),
            M('m8', 'In the previous question, in which direction is Kiran from the start?', ['North-East', 'North-West', 'East', 'North'], 0, 'She is 4 km North and 3 km East of the start, so North-East.', 'c3'),
            M('m9', 'A man walks 10 km South, turns left and walks 5 km, then turns left and walks 10 km. In which direction is he from the start?', ['East', 'West', 'North', 'South'], 0, 'Left of South is East, left of East is North. South 10 and North 10 cancel, leaving 5 km East.', 'c3'),
            M('m10', 'Ruchi walks 12 km East, turns left and walks 5 km. How far is she from the start?', ['13 km', '17 km', '7 km', '12 km'], 0, '√(12² + 5²) = √169 = 13 km (the 5-12-13 triple).', 'c4', 'core', '(12**2+5**2)**0.5'),
            M('m11', 'Arun walks 7 km East, turns North and walks 4 km, turns West and walks 10 km, then turns South and walks 4 km. In which direction is he from the start?', ['West', 'East', 'North', 'South'], 0, 'North 4 and South 4 cancel; East 7 and West 10 leave 3 km West.', 'c3'),
            M('m12', 'In the previous question, how far is Arun from the start?', ['3 km', '7 km', '17 km', '25 km'], 0, 'Net West movement = 10 − 7 = 3 km; north–south movement cancels. 25 km is the total walked.', 'c4', 'core', '10-7'),
            M('m13', 'Early one morning Sunil walks towards the sun, then turns right, and then turns right again. Which way is he walking now?', ['West', 'East', 'North', 'South'], 0, 'Towards the morning sun = East; right → South; right → West.', 'c5'),
            M('m14', 'In the evening, Raju\'s shadow falls straight in front of him. Which way is he facing?', ['East', 'West', 'North', 'South'], 0, 'Evening sun is in the West, so shadows fall to the East. A shadow in front means he faces East.', 'c5', 'moderate'),
            M('m15', 'At 7 a.m. the shadow of a pole falls to Kiran\'s left. Which way is Kiran facing?', ['North', 'South', 'East', 'West'], 0, 'Morning shadow falls West, so her left is West. Facing North, the left hand points West.', 'c5', 'moderate'),
            M('m16', 'Dev stands on his head facing North. Which way does his right hand point?', ['West', 'East', 'North', 'South'], 0, 'Normally (facing North) the right hand points East; upside down, left and right swap, so it points West.', 'c6', 'moderate'),
            M('m17', 'Rohan walks 3 km North, turns left and walks 4 km, turns left and walks 3 km, then turns right and walks 2 km. Which way is he facing?', ['West', 'South', 'East', 'North'], 0, 'North → left: West → left: South → right: West.', 'c2', 'moderate'),
            M('m18', 'In the previous question, how far is Rohan from the start?', ['6 km', '4 km', '12 km', '2 km'], 0, 'North 3 and South 3 cancel; West 4 + West 2 = 6 km West. 12 km is the total distance walked.', 'c4', 'moderate', '4+2'),
            M('m19', 'A is 5 m north of B. C is 5 m east of B. In which direction is A from C?', ['North-West', 'North-East', 'South-West', 'South-East'], 0, 'With B at (0, 0): A = (0, 5), C = (5, 0). A − C = (−5, 5): West and North, so North-West.', 'c6', 'moderate'),
            M('m20', 'A clock is laid flat so that at 3 o\'clock the minute hand points North. Which way does the hour hand point?', ['East', 'West', 'South', 'North'], 0, 'The minute hand is at 12 (North). The hour hand at 3 is 90° clockwise from 12, so it points East.', 'c6', 'hard'),
            M('m21', 'A person facing East turns right twice. Through how many degrees has he turned?', ['180', '90', '270', '360'], 0, 'Two right turns = 2 × 90° = 180°; he now faces West.', 'c2', 'core', '90*2'),
            M('m22', 'Ankit faces South-East and turns 270° clockwise. Which way does he face?', ['North-East', 'South-West', 'North-West', 'East'], 0, '135° + 270° = 405° − 360° = 45°, North-East. (A 270° clockwise turn is the same as a 90° anticlockwise turn.)', 'c2', 'hard'),
            M('m23', 'A man walks 2 km East, turns left and walks 6 km, then turns right and walks 4 km. What is his shortest distance from the start (nearest 0.01 km)?', ['8.49 km', '12 km', '6 km', '10 km'], 0, 'Net East = 2 + 4 = 6 km, net North = 6 km: distance = √(6² + 6²) = 6√2 ≈ 8.49 km.', 'c4', 'hard', '(6**2+6**2)**0.5'),
            M('m24', 'X and Y start from the same point. X walks 8 km North and Y walks 6 km East. How far apart are they?', ['10 km', '14 km', '2 km', '12 km'], 0, 'Their paths are at right angles: √(8² + 6²) = 10 km.', 'c4', 'core', '(8**2+6**2)**0.5'),
            M('m25', 'Which direction is exactly opposite to South-West?', ['North-East', 'North-West', 'South-East', 'North'], 0, '225° + 180° = 405° − 360° = 45°, North-East.', 'c1'),
            M('m26', 'A woman facing North turns left, then turns 135° clockwise. Which way does she face?', ['North-East', 'South-East', 'North-West', 'South'], 0, 'Left of North = West (270°); 270° + 135° = 405° − 360° = 45°, North-East.', 'c2', 'hard'),
            M('m27', 'Lata walks 20 m South, turns right and walks 10 m, turns right and walks 20 m, then turns left and walks 15 m. How far is she from the start?', ['25 m', '15 m', '35 m', '65 m'], 0, 'South → right: West → right: North → left: West. South 20 and North 20 cancel; West 10 + 15 = 25 m. 65 m is the total walked.', 'c4', 'moderate', '10+15'),
            M('m28', 'In the previous question, which direction is the starting point from Lata?', ['East', 'West', 'North', 'South'], 0, 'Lata is 25 m West of the start, so the start is East of her — the opposite direction.', 'c3', 'moderate'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Vikram walks 9 km North, turns right and walks 5 km, turns right and walks 3 km, then turns left and walks 3 km. (a) Which direction is he facing at the end? (b) How far and in which direction is he from the start? Show your route table.',
             'model': [tbl([['1', '—', 'North', '9 km', '(0, 9)'], ['2', 'Right', 'East', '5 km', '(5, 9)'], ['3', 'Right', 'South', '3 km', '(5, 6)'], ['4', 'Left', 'East', '3 km', '(8, 6)']], 'Route'),
                       p(f'(a) Facing {q1[2]}.'),
                       p(f'(b) Net North = 9 − 3 = 6 km; net East = 5 + 3 = 8 km. Distance = √(8² + 6²) = {c_q1[2]["value"]} km, direction {where(q1[0], q1[1])} of the start.')],
             'scheme': [{'id': 's1', 'pt': 'Each turn converted correctly (route table)', 'm': 1, 'skill': 'analysis'},
                        {'id': 's2', 'pt': '(a) final facing East', 'm': 1, 'skill': 'conclusion'},
                        {'id': 's3', 'pt': 'Net displacements 6 km N and 8 km E', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': '10 km North-East', 'm': 1, 'skill': 'computation'}],
             'remarks': ['Most errors come from the third leg — a right turn while facing East is South, not North.', 'Candidates who sketch the route get both parts right far more often.'],
             'mistakes': ['Giving 20 km (total walked) instead of 10 km.', 'Answering "East" for part (b) by confusing facing with position.'],
             'tips': ['Use coordinates (x East, y North) and update them after every leg.'],
             'checks': c_q1},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) One evening Sameer walks with his shadow directly behind him. After a while he turns left. Which way is he walking now? (2 marks)  (b) Leena stands on her head with her face towards East. Which way does her left hand point? (2 marks)',
             'model': [p('(a) Evening sun is in the West, so shadows fall East. A shadow behind him means East is behind, so he walks West. A left turn from West is South. Answer: South.'),
                       p('(b) Standing normally and facing East, the left hand points North. Upside down the face still points East but left and right swap, so the left hand points South. Answer: South.')],
             'scheme': [{'id': 's1', 'pt': '(a) evening shadow falls East → walking West', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': '(a) left of West = South', 'm': 1, 'skill': 'application'},
                        {'id': 's3', 'pt': '(b) normal position: left hand North', 'm': 1, 'skill': 'concept'},
                        {'id': 's4', 'pt': '(b) inverted: left hand South', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Part (a) needs two steps — the shadow fixes the starting facing, then the turn is applied.'],
             'mistakes': ['Putting the evening shadow in the West (the sun is there, not the shadow).', 'Forgetting that the face direction does not change when a person stands on the head.'],
             'tips': ['Write "morning shadow → West, evening shadow → East" at the top of your rough sheet.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'K is 3 km east of P. M is 4 km north of K. T is 6 km west of M. Find (a) the direction of T from P, (b) the distance between T and P, and (c) the direction of P from T.',
             'model': [p('Put P at (0, 0). K = (3, 0); M = (3, 4); T = (3 − 6, 4) = (−3, 4).'),
                       p(f'(a) T is 3 km West and 4 km North of P: {where(-3, 4)}.'),
                       p(f'(b) Distance = √(3² + 4²) = {c_q3[0]["value"]} km.'),
                       p('(c) P from T is the opposite direction: South-East.')],
             'scheme': [{'id': 's1', 'pt': 'Coordinates of K, M and T', 'm': 1, 'skill': 'analysis'},
                        {'id': 's2', 'pt': '(a) North-West', 'm': 1, 'skill': 'conclusion'},
                        {'id': 's3', 'pt': '(b) 5 km', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': '(c) South-East (opposite direction)', 'm': 1, 'skill': 'application'}],
             'remarks': ['Part (c) checks whether the candidate understands that "A from B" and "B from A" are opposite.'],
             'mistakes': ['Answering North-West again in (c).', 'Taking T 6 km west of P instead of west of M.'],
             'tips': ['Name the reference point first in every answer: "T is North-West of P".'],
             'checks': c_q3},
        ],
        'revision': {
            'summary': ['Eight directions, 45° apart, clockwise: N 0°, NE 45°, E 90°, SE 135°, S 180°, SW 225°, W 270°, NW 315°.',
                        'Right turn = +90° (clockwise); left turn = −90° (anticlockwise); about-turn = 180°. Two rights = opposite; right + left = no change.',
                        'Facing direction comes from the last leg; position comes from net displacement (north − south, east − west).',
                        'Shortest distance = √(x² + y²); total distance = sum of legs.',
                        'Morning shadow falls West, evening shadow falls East. Upside down: same face direction, left and right swap.'],
            'remember': ['Triples: 3-4-5, 6-8-10, 5-12-13, 8-15-17, 9-12-15; equal legs → x√2.', 'Direction of B from A is the opposite of A from B.'],
            'traps': ['Turning from the reader\'s viewpoint instead of the walker\'s.', 'Answering total distance when shortest distance is asked.', 'Mixing up "facing" and "from the start".', 'Placing the evening shadow in the West.']},
        'quickref': [{'k': 'Right turn', 'v': '+90° clockwise (N → E → S → W → N)'}, {'k': 'Left turn', 'v': '−90° anticlockwise (N → W → S → E → N)'},
                     {'k': 'Angle turn', 'v': 'New angle = old ± turn, reduce mod 360°'}, {'k': 'Shortest distance', 'v': '√(net E–W² + net N–S²)'},
                     {'k': 'Shadow', 'v': 'Morning → West · Evening → East'}, {'k': 'Headstand', 'v': 'Face unchanged; left ↔ right'}],
        'viva': [
            V('v1', 'Name the main and intermediate directions and the angle between neighbouring directions.',
              'The four main directions are North, East, South and West, ninety degrees apart. The four intermediate directions are North-East, South-East, South-West and North-West, each halfway between two main ones, so neighbouring directions are forty five degrees apart.',
              [P('p1', 'Four main directions: North, East, South, West', 3, 'north', 'east', 'south', 'west'),
               P('p2', 'Four intermediate: NE, SE, SW, NW', 3, 'north east|northeast|ne', 'south east|southeast|se', 'south west|southwest|sw', 'north west|northwest|nw', min=3),
               P('p3', 'Main directions are 90° apart', 2, 'west 90|west ninety|west right angle|main 90|main ninety|cardinal 90|cardinal ninety|main ones right angle|right angles to each other|right angle to each other|main right angle|four 90|four ninety'),
               P('p4', 'Neighbouring directions (with the intermediates) are 45° apart', 2, 'halfway|half way|midway|neighbour 45|neighbor 45|neighbouring 45|neighbour forty|45 away|each 45|between 45|intermediate 45|intermediate forty|adjacent 45')], 'c1'),
            V('v2', 'How do you work out the direction a person faces after a series of left and right turns?',
              'A right turn is ninety degrees clockwise and a left turn is ninety degrees anticlockwise from the way the person is facing. I track the facing after every turn. Two right turns make the person face the opposite way, and a right followed by a left cancels out.',
              [P('p1', 'Right turn = 90° clockwise; left turn = 90° anticlockwise', 5, 'right turn clockwise|right clockwise|right 90 clockwise|right is clockwise|right means clockwise|right turn 90 clockwise|right goes clockwise', 'left turn anticlockwise|left anticlockwise|left anti clockwise|left counter clockwise|left counterclockwise|left 90 anticlockwise|left turn 90 anticlockwise|left is anticlockwise|left means anticlockwise|left turn anti clockwise|left 90 anti clockwise'),
               P('p2', 'Judge each turn from the person\'s current facing; track step by step', 2, 'each turn|every turn|after each|step by step|one by one|current|own facing|track|keep track|update'),
               P('p3', 'Two rights = opposite; right + left cancel', 3, 'opposite|about turn|reverse|180|back', 'cancel|same direction|original|back to|no change|undo|neutral', min=1)], 'c2'),
            V('v3', 'How do you find the shortest distance between the starting point and the final point?',
              'Find the net movement in each axis: north minus south, and east minus west, because opposite movements cancel. Then apply Pythagoras: the shortest distance is the square root of the sum of the squares of the two net movements. The signs also tell the direction, for example north-east.',
              [P('p1', 'Net north–south and east–west movement (opposites cancel)', 4, 'net|cancel|minus|subtract|offset|difference'),
               P('p2', 'Pythagoras: √(x² + y²)', 4, 'pythagor|square root|root of|hypotenuse|root sum'),
               P('p3', 'Direction from the signs / quadrant', 2, 'direction|quadrant|sign|north east|north west|south east|south west')], 'c4'),
            V('v4', 'In which direction does a shadow fall in the morning and in the evening, and why?',
              'The sun rises in the east and sets in the west, and a shadow falls opposite the sun. So in the morning the shadow falls towards the west, and in the evening the shadow falls towards the east.',
              [P('p1', 'Sun rises in the East, sets in the West; shadow is opposite the sun', 3, 'rise east|rises in east|sun east|east rise|east in the morning sun', 'opposite|away from|other side|behind'),
               P('p2', 'Morning: shadow towards West', 4, 'morning west|morning shadow west|morning fall west|morning point west|morning towards west|morning to west|morning shadows west|morning it west'),
               P('p3', 'Evening: shadow towards East', 3, 'evening east|evening shadow east|evening fall east|evening point east|evening towards east|evening to east|evening shadows east|evening it east')], 'c5'),
            V('v5', 'A person stands on his head facing North. Which way does his right hand point, and why?',
              'His right hand points West. Normally, facing North, the right hand points East, but when he stands on his head his face still points North while left and right are swapped, so the right hand points West.',
              [P('p1', 'Answer: West', 5, 'right hand west|right hand point west|right hand points to west|right point west|right west|points west|point west|towards west|to the west'),
               P('p2', 'Normally right hand = East when facing North', 2, 'normal|usual|standing upright|upright|ordinarily|otherwise', 'east'),
               P('p3', 'Face unchanged; left and right swap', 3, 'swap|interchang|revers|exchang|flip|opposite|switch|invert')], 'c6'),
            V('v6', 'What is the difference between the direction a person is facing and the direction in which he is from the starting point?',
              'The facing direction is the direction of the last leg after the last turn. The direction from the starting point depends on the net displacement from start to finish, found by cancelling north against south and east against west. The two can be different.',
              [P('p1', 'Facing = direction of the last leg / last turn', 4, 'facing last|facing final|faces last|faces final|face last|face final|facing direction last|facing direction final|facing comes last|facing depends last|facing given by last|facing is last|facing means last'),
               P('p2', 'Position = net displacement from start', 4, 'start net|start point net|starting point net|position net|start overall|position overall|start displacement|position displacement|start resultant|position resultant|start depends net|start cancel|start total movement'),
               P('p3', 'They can differ', 2, 'differ|not same|not the same|not always same|not necessarily|can be different|may be different|need not')], 'c3'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'A delivery rider\'s route', 'difficulty': 'moderate',
            'case': 'A courier rider leaves the depot riding North for 2 km, turns right and rides 3 km, turns right again and rides 6 km, then turns left and rides 1 km to the customer\'s gate.',
            'mcqs': [
                M('k1a', 'Which way is the rider facing at the customer\'s gate?', ['East', 'West', 'South', 'North'], 0, 'North → right: East → right: South → left: East.', 'c2', 'core'),
                M('k1b', 'In which direction is the customer\'s gate from the depot?', ['South-East', 'North-East', 'South-West', 'East'], 0, 'Net North–South = 2 − 6 = 4 km South; net East = 3 + 1 = 4 km East: South-East.', 'c3', 'moderate'),
                M('k1c', 'What is the straight-line distance from the depot to the gate (nearest 0.01 km)?', ['5.66 km', '12 km', '4 km', '8 km'], 0, '√(4² + 4²) = 4√2 ≈ 5.66 km. 12 km is the distance ridden.', 'c4', 'hard', '(4**2+4**2)**0.5'),
                M('k1d', 'In which direction must the rider head to go straight back to the depot?', ['North-West', 'South-East', 'North-East', 'West'], 0, 'The depot lies in the direction opposite to South-East, i.e. North-West.', 'c3', 'moderate'),
            ]}],
    }
