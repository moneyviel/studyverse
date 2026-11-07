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


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None, topic=None):
    d = {'topic': topic, 'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
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
            M('m1', 'Asha faces North. She turns right, right again and then left. Which way does she face now?', ['East', 'West', 'South', 'North'], 0, "Track each turn from Asha's own facing: North, right gives East, right again gives South, and a left from South gives East. Short cut: two rights and one left net to a single right turn from North, which is East. The trap is West, which you get if you turn left from the reader's side instead of hers. In practice: an audit team following a storekeeper's spoken directions round a godown applies exactly this turn-by-turn tracking.", 'c2', topic='Turns: left, right, angles and about-turn'),
            M('m2', 'A man facing West turns left. Which way does he face?', ['South', 'North', 'East', 'South-West'], 0, 'A left turn is 90° anticlockwise. West is 270°, and 270° − 90° = 180°, which is South. North is the tempting wrong answer: it is what you get by turning right (clockwise) instead of left. In practice: field auditors and survey staff reading a site plan in a lease deed must apply left and right from the direction the person is facing, not from the page.', 'c2', topic='Turns: left, right, angles and about-turn'),
            M('m3', 'A girl facing South makes an about-turn. Which way does she face?', ['North', 'South', 'East', 'West'], 0, 'An about-turn means turning through 180°, so the girl ends up facing the exact opposite of South, which is North. Choosing South (unchanged) treats an about-turn as a full 360° circle, which is the usual slip. In practice: property documents describe boundaries in opposite pairs (north against south, east against west), so knowing opposites instantly helps when checking a sale deed or valuation report.', 'c2', topic='Turns: left, right, angles and about-turn'),
            M('m4', 'Facing East, Ravi turns 45° clockwise. Which way does he face?', ['South-East', 'North-East', 'South', 'North'], 0, 'Clockwise turns add to the angle measured from North. East is 90°, so 90° + 45° = 135°, which is South-East. North-East (45°) is the trap: it is the result of turning 45° anticlockwise instead. In practice: wind directions in weather reports and orientation on industrial site layouts use these 45° intermediate directions, so a 45° slip puts an asset in the wrong corner of the plant.', 'c2', 'moderate', topic='Turns: left, right, angles and about-turn'),
            M('m5', 'A man facing North-West turns right. Which way does he face?', ['North-East', 'South-West', 'South-East', 'North'], 0, "North-West is 315°. A right turn adds 90°: 315° + 90° = 405°, and 405° − 360° = 45°, which is North-East. South-West is the trap, reached by turning left (subtracting 90°) instead of right. In practice: when a valuer's report says a factory gate faces North-West, a CA checking the plant layout uses this angle arithmetic to place the other blocks correctly.", 'c2', 'moderate', topic='Turns: left, right, angles and about-turn'),
            M('m6', 'Facing North, a boy turns 135° anticlockwise. Which way does he face?', ['South-West', 'South-East', 'North-West', 'West'], 0, "Anticlockwise turns subtract from the angle. North is 0°, so 0° − 135° = −135°; adding 360° gives 225°, which is South-West. South-East (135°) is the trap: it is the clockwise answer. In practice: reducing an angle modulo 360° is the same 'wrap-around' idea used when converting a negative bearing on a survey map of land offered as loan security.", 'c2', 'moderate', topic='Turns: left, right, angles and about-turn'),
            M('m7', 'Kiran walks 4 km North, turns right and walks 3 km. How far is she from the start?', ['5 km', '7 km', '1 km', '6 km'], 0, 'She walks 4 km North and 3 km East, two legs at right angles, so the straight-line distance is √(3² + 4²) = √25 = 5 km (the 3-4-5 triple). The trap is 7 km, which is the total distance walked along the two roads, not the shortest distance. In practice: a CA reviewing a staff conveyance claim knows the straight-line distance is a minimum; a claim below it is impossible.', 'c4', 'core', '(3**2+4**2)**0.5', topic='Shortest distance — Pythagoras'),
            M('m8', 'In the previous question, in which direction is Kiran from the start?', ['North-East', 'North-West', 'East', 'North'], 0, "Kiran ends 4 km North and 3 km East of where she began, so she lies in the North-East quadrant from the start. East is the trap: it is her facing direction after the last turn, not her position from the start. In practice: confusing 'which way facing' with 'where from the start' is like confusing the last entry posted with the closing balance of an account.", 'c3', topic='Final facing vs position from the start'),
            M('m9', 'A man walks 10 km South, turns left and walks 5 km, then turns left and walks 10 km. In which direction is he from the start?', ['East', 'West', 'North', 'South'], 0, "Facing South, a left turn gives East, and another left gives North. South 10 km and North 10 km cancel, leaving 5 km East, so he is East of the start. North is the trap: it is the direction he is facing at the end, not his position. In practice: netting opposite movements is the same logic as netting debits against credits to find an account's closing balance.", 'c3', topic='Final facing vs position from the start'),
            M('m10', 'Ruchi walks 12 km East, turns left and walks 5 km. How far is she from the start?', ['13 km', '17 km', '7 km', '12 km'], 0, 'The legs are 12 km East and 5 km North, at right angles, so the distance is √(12² + 5²) = √169 = 13 km (the 5-12-13 triple). The trap is 17 km, the total length walked. In practice: logistics and finance teams use straight-line distance as a floor when checking freight or travel bills; anything claimed below it needs explaining.', 'c4', 'core', '(12**2+5**2)**0.5', topic='Shortest distance — Pythagoras'),
            M('m11', 'Arun walks 7 km East, turns North and walks 4 km, turns West and walks 10 km, then turns South and walks 4 km. In which direction is he from the start?', ['West', 'East', 'North', 'South'], 0, 'North 4 km and South 4 km cancel. East 7 km against West 10 km leaves 3 km West, so Arun is West of the start. South is the trap: it is the direction he faces on the last leg, not his position. In practice: tracing a route leg by leg and netting opposite moves is how an audit senior plans a physical-verification walk across a large plant.', 'c3', topic='Final facing vs position from the start'),
            M('m12', 'In the previous question, how far is Arun from the start?', ['3 km', '7 km', '17 km', '25 km'], 0, 'North and South movements cancel (4 − 4 = 0), and East–West nets to 10 − 7 = 3 km West, so he is 3 km from the start. The trap is 25 km, the total distance walked (7 + 4 + 10 + 4). In practice: just as only the net balance of a ledger matters, only net displacement decides the shortest distance; the gross movement is a different figure.', 'c4', 'core', '10-7', topic='Shortest distance — Pythagoras'),
            M('m13', 'Early one morning Sunil walks towards the sun, then turns right, and then turns right again. Which way is he walking now?', ['West', 'East', 'North', 'South'], 0, 'In the morning the sun is in the East, so walking towards it means walking East. A right turn gives South; another right gives West. Two right turns always reverse your direction. The trap is East, which ignores that two rights make an about-turn. In practice: fixing one known reference first (the sun) and deducing the rest is how a CA reconciles accounts, starting from a confirmed balance.', 'c5', topic='Sun and shadow'),
            M('m14', 'In the evening, Raju\'s shadow falls straight in front of him. Which way is he facing?', ['East', 'West', 'North', 'South'], 0, 'In the evening the sun is in the West, so shadows fall towards the East. If his shadow is straight in front of him, he must be facing East. West is the trap: that is where the sun is, not where the shadow falls. In practice: site photographs taken during asset verification often show shadows, and reading them correctly helps judge orientation and time of day.', 'c5', 'moderate', topic='Sun and shadow'),
            M('m15', 'At 7 a.m. the shadow of a pole falls to Kiran\'s left. Which way is Kiran facing?', ['North', 'South', 'East', 'West'], 0, "At 7 a.m. the sun is in the East, so the shadow falls to the West. If West is on Kiran's left, she must be facing North, because a person facing North has West on the left. South is the trap: facing South puts West on the right. In practice: deducing an unknown from one fixed fact is the core of analytical review, a key audit procedure.", 'c5', 'moderate', topic='Sun and shadow'),
            M('m16', 'Dev stands on his head facing North. Which way does his right hand point?', ['West', 'East', 'North', 'South'], 0, "Standing normally and facing North, the right hand points East. Standing on his head, Dev still faces North, but left and right swap sides, so the right hand now points West. East is the trap: it forgets the swap. In practice: this 'same front, swapped sides' idea also appears when reading a mirror image of a document or a reversed scan.", 'c6', 'moderate', topic='Upside down and relative-position puzzles'),
            M('m17', 'Rohan walks 3 km North, turns left and walks 4 km, turns left and walks 3 km, then turns right and walks 2 km. Which way is he facing?', ['West', 'South', 'East', 'North'], 0, 'Start North; a left gives West; another left gives South; a right from South gives West. So Rohan is facing West at the end. South is the trap: it stops one leg early, before the final right turn. In practice: missing the last step of a sequence is the same error as missing the last adjusting entry before finalising accounts.', 'c2', 'moderate', topic='Turns: left, right, angles and about-turn'),
            M('m18', 'In the previous question, how far is Rohan from the start?', ['6 km', '4 km', '12 km', '2 km'], 0, 'North 3 km and South 3 km cancel. Both westward legs add up: 4 + 2 = 6 km West, so he is 6 km from the start. The trap is 12 km, the total walked (3 + 4 + 3 + 2). In practice: travel-claim reviews compare the claimed distance with the net straight-line distance, which is a floor for any genuine trip.', 'c4', 'moderate', '4+2', topic='Shortest distance — Pythagoras'),
            M('m19', 'A is 5 m north of B. C is 5 m east of B. In which direction is A from C?', ['North-West', 'North-East', 'South-West', 'South-East'], 0, 'Place B at (0, 0). Then A = (0, 5) and C = (5, 0). A − C = (−5, 5): 5 m West and 5 m North, so A is North-West of C. North-East is the trap: it gets the East–West sign backwards by subtracting C from A the wrong way round. In practice: geo-tagged asset photos carry coordinates, and reading one point relative to another is exactly this skill.', 'c6', 'moderate', topic='Upside down and relative-position puzzles'),
            M('m20', 'A clock is laid flat so that at 3 o\'clock the minute hand points North. Which way does the hour hand point?', ['East', 'West', 'South', 'North'], 0, "At 3 o'clock the minute hand is at 12, which points North. The hour hand is at 3, which is 90° clockwise from 12, so it points East. West is the trap: it treats clockwise as anticlockwise. In practice: rotating a map or plan so that a known mark faces a given direction, and then re-orienting everything else, is common when using site plans during audits.", 'c6', 'hard', topic='Upside down and relative-position puzzles'),
            M('m21', 'A person facing East turns right twice. Through how many degrees has he turned?', ['180', '90', '270', '360'], 0, 'Each right turn is 90°, so two right turns are 2 × 90° = 180°; facing East, he now faces West. The trap is 90°, which counts only one turn. In practice: knowing that two same-side turns equal an about-turn speeds up any route question, just as knowing that a reversal entry exactly cancels the original saves time in accounts.', 'c2', 'core', '90*2', topic='Turns: left, right, angles and about-turn'),
            M('m22', 'Ankit faces South-East and turns 270° clockwise. Which way does he face?', ['North-East', 'South-West', 'North-West', 'East'], 0, 'South-East is 135°. Clockwise means add: 135° + 270° = 405°, and 405° − 360° = 45°, North-East. A 270° clockwise turn equals a 90° anticlockwise turn. South-West is the trap, reached by turning 90° clockwise instead. In practice: reducing angles beyond 360° is routine wherever bearings are used, such as land survey maps attached to loan files.', 'c2', 'hard', topic='Turns: left, right, angles and about-turn'),
            M('m23', 'A man walks 2 km East, turns left and walks 6 km, then turns right and walks 4 km. What is his shortest distance from the start (nearest 0.01 km)?', ['8.49 km', '12 km', '6 km', '10 km'], 0, 'Facing East: 2 km East, left to North for 6 km, then right to East for 4 km. Net East = 2 + 4 = 6 km; net North = 6 km. Distance = √(6² + 6²) = 6√2 ≈ 8.49 km. The trap is 12 km, the total walked. In practice: when the two net legs are equal, multiply by √2 (about 1.414), a quick check on any distance-based claim.', 'c4', 'hard', '(6**2+6**2)**0.5', topic='Shortest distance — Pythagoras'),
            M('m24', 'X and Y start from the same point. X walks 8 km North and Y walks 6 km East. How far apart are they?', ['10 km', '14 km', '2 km', '12 km'], 0, 'X and Y move at right angles (North and East) from the same point, so the gap between them is the hypotenuse: √(8² + 6²) = √100 = 10 km. The trap is 14 km, which simply adds the two distances. In practice: logistics planners estimate the direct distance between two depots this way before comparing road routes and freight quotes.', 'c4', 'core', '(8**2+6**2)**0.5', topic='Shortest distance — Pythagoras'),
            M('m25', 'Which direction is exactly opposite to South-West?', ['North-East', 'North-West', 'South-East', 'North'], 0, "South-West is 225°. The opposite direction is 180° away: 225° + 180° = 405° − 360° = 45°, which is North-East. North-West is the trap: it is only 90° from South-West, a neighbour, not the opposite. In practice: sale deeds and lease agreements list boundaries on all four sides, and checking opposite pairs is part of verifying a property's description.", 'c1', topic='The eight directions'),
            M('m26', 'A woman facing North turns left, then turns 135° clockwise. Which way does she face?', ['North-East', 'South-East', 'North-West', 'South'], 0, 'Facing North, a left turn gives West (270°). A 135° clockwise turn adds: 270° + 135° = 405°, and 405° − 360° = 45°, North-East. South-East is the trap, the result if you start the 135° turn from North instead of West. In practice: applying each step from the updated position, not the original one, is the same discipline as rolling a balance forward entry by entry.', 'c2', 'hard', topic='Turns: left, right, angles and about-turn'),
            M('m27', 'Lata walks 20 m South, turns right and walks 10 m, turns right and walks 20 m, then turns left and walks 15 m. How far is she from the start?', ['25 m', '15 m', '35 m', '65 m'], 0, 'South 20 m; a right turn gives West (10 m); another right gives North (20 m); a left gives West (15 m). South and North cancel, and West totals 10 + 15 = 25 m. The trap is 65 m, the total walked. In practice: netting opposite moves to find the true position is the same idea as netting receipts and payments to find closing cash.', 'c4', 'moderate', '10+15', topic='Shortest distance — Pythagoras'),
            M('m28', 'In the previous question, which direction is the starting point from Lata?', ['East', 'West', 'North', 'South'], 0, "Lata is 25 m West of the start, so the start lies in the opposite direction from her: East. West is the trap: it answers 'Lata from the start' instead of 'the start from Lata'. In practice: the direction of A from B is always the reverse of B from A, just as a receivable in one company's books is a payable in the other's.", 'c3', 'moderate', topic='Final facing vs position from the start'),
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
                M('k1a', 'Which way is the rider facing at the customer\'s gate?', ['East', 'West', 'South', 'North'], 0, 'Start North; a right turn gives East; another right gives South; a left from South gives East. So the rider faces East at the gate. South is the trap: it is the direction of the long third leg, before the final left turn. In practice: delivery and field-sales apps record each turn; reading the last turn correctly is what this question tests.', 'c2', 'core', topic='Turns: left, right, angles and about-turn'),
                M('k1b', 'In which direction is the customer\'s gate from the depot?', ['South-East', 'North-East', 'South-West', 'East'], 0, "North 2 km and South 6 km net to 4 km South; East 3 km and East 1 km give 4 km East. So the gate is South-East of the depot. East is the trap: it is the rider's final facing direction, not the gate's position from the depot. In practice: route-optimisation and last-mile delivery costing start from exactly this net displacement.", 'c3', 'moderate', topic='Final facing vs position from the start'),
                M('k1c', 'What is the straight-line distance from the depot to the gate (nearest 0.01 km)?', ['5.66 km', '12 km', '4 km', '8 km'], 0, "Net displacement is 4 km East and 4 km South. Distance = √(4² + 4²) = 4√2 ≈ 5.66 km. The trap is 12 km, the total distance ridden (2 + 3 + 6 + 1). In practice: a finance team checking a courier's per-km billing knows the straight-line distance is only a floor; actual road distance will be higher but should be reasonable.", 'c4', 'hard', '(4**2+4**2)**0.5', topic='Shortest distance — Pythagoras'),
                M('k1d', 'In which direction must the rider head to go straight back to the depot?', ['North-West', 'South-East', 'North-East', 'West'], 0, "The gate is South-East of the depot, so the depot lies in the opposite direction from the gate: North-West. South-East is the trap: it repeats the gate's direction from the depot instead of reversing it. In practice: return-trip planning for delivery fleets always uses the reverse bearing, the same 'A from B is opposite of B from A' rule.", 'c3', 'moderate', topic='Final facing vs position from the start'),
            ]}],
    }

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        's1': _K('east|e 5|e 3', 'south|s 3'),
        's2': _K('facing east|face east|east facing|faces east|towards east|final east|finally east|end east'),
        's3': _K('6 km north|6 north|north 6|north 9 3 6|6 km n|y 6', '8 km east|8 east|east 8|east 5 3 8|8 km e|x 8'),
        's4': _K('10 km north east|10 north east|north east 10|10 km ne|10 ne'),
    },
    'q2': {
        's1': _K('west', 'shadow east|east behind|sun west|shadow fall east|walk west|walking west|facing west|towards west|faces west'),
        's2': _K('walk south|walking south|now south|west south|west left south|towards south|turns south|moving south|heading south|faces south|facing south'),
        's3': _K('left hand north|left north|left hand point north'),
        's4': _K('left hand south|left hand point south|hand south|upside down south|inverted south|head south'),
    },
    'q3': {
        's1': _K('t 3 4|t 34|3 km west|3 west|west 3', 'k 3 0|k 30|m 3 4|m 34|4 km north|4 north|north 4'),
        's2': _K('north west|nw'),
        's3': _K('5 km|distance 5|tp 5|pt 5|5 unit|25 5'),
        's4': _K('south east|se'),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
