"""Paper 3 Ch 10 — Direction Sense: extra MCQ templates (walks simulated on a grid)."""
from common import *
import math

U = 'fnd-p3-ch10-u01'
C1, C2, C3, C4, C5, C6 = 'The eight directions', 'Turns: left, right, angles and about-turn', 'Final facing vs position from the start', 'Shortest distance — Pythagoras', 'Sun and shadow', 'Upside down and relative-position puzzles'
D8 = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West']
VEC = {0: (0, 1), 2: (1, 0), 4: (0, -1), 6: (-1, 0)}
NAMES = ['Ravi', 'Meena', 'Arjun', 'Kavya', 'Suresh', 'Pooja', 'Imran', 'Neha', 'Vikram', 'Asha']


def quadrant(x, y):
    if x == 0 and y == 0: return 'At the starting point'
    if x == 0: return 'North' if y > 0 else 'South'
    if y == 0: return 'East' if x > 0 else 'West'
    return ('North' if y > 0 else 'South') + '-' + ('East' if x > 0 else 'West')


def walk(r, legs):
    h = r.choice([0, 2, 4, 6]); x = y = 0; parts = []; name = r.choice(NAMES); he = 'She' if name in ('Meena', 'Kavya', 'Pooja', 'Neha', 'Asha') else 'He'
    for i in range(legs):
        dist = r.randint(2, 15)
        if i == 0: parts.append(f'{name} starts facing {D8[h]} and walks {dist} km.')
        else:
            t = r.choice(['left', 'right']); h = (h + (2 if t == 'right' else -2)) % 8
            parts.append(f'{he} turns {t} and walks {dist} km.')
        dx, dy = VEC[h]; x += dx * dist; y += dy * dist
    return ' '.join(parts), x, y, h, name, he


def distance(r):
    txt, x, y, h, name, he = walk(r, r.choice([3, 4, 5]))
    d2 = x * x + y * y; d = math.isqrt(d2)
    if d * d != d2 or x == 0 or y == 0: return None
    return dict(q=f'{txt} What is the straight-line distance between {name} and the starting point?', a=f'{d} km', w=[f'{abs(x) + abs(y)} km', f'{abs(x)} km' if abs(x) != d else f'{d + 2} km', f'{abs(y)} km' if abs(y) != d else f'{d + 1} km', f'{d + 3} km'],
                ex=f'Track the net movement: the East–West total is {abs(x)} km {"East" if x > 0 else "West"} and the North–South total is {abs(y)} km {"North" if y > 0 else "South"}. These are at right angles, so the shortest distance is √({abs(x)}² + {abs(y)}²) = √{d2} = {d} km (Pythagoras). Adding the two ({abs(x) + abs(y)} km) gives the walking path, not the straight-line distance.',
                fast='Net East–West and net North–South, then Pythagoras (look for 3-4-5, 5-12-13, 6-8-10 triples).', secs=60, d='moderate', topic=C4, check=str(d), k='ch10.dist', data={'_t': 0})


def position(r):
    txt, x, y, h, name, he = walk(r, r.choice([3, 4]))
    if x == 0 and y == 0: return None
    ans = quadrant(x, y); opp = quadrant(-x, -y)
    w = [opp, quadrant(y, -x), quadrant(-y, x), D8[h]]
    return dict(q=f'{txt} Where is {name} now with respect to the starting point?', a=ans, w=w + ['North', 'South', 'East', 'West'],
                ex=f'Net displacement: {abs(x)} km {"East" if x > 0 else "West" if x < 0 else "(no East–West)"} and {abs(y)} km {"North" if y > 0 else "South" if y < 0 else "(no North–South)"}. So {name} is {ans} of the start. The direction {name} is FACING at the end ({D8[h]}) is a different question — position is about where the person is, not where they look.',
                fast='Keep running totals of East–West and North–South; their signs give the direction.', secs=60, d='moderate', topic=C3, k='ch10.pos', data={'_t': 0})


def facing(r):
    h = r.randrange(8); name = r.choice(NAMES); steps = []; cur = h
    for _ in range(r.randint(2, 4)):
        kind = r.choice(['left', 'right', 'deg', 'about'])
        if kind == 'left': cur = (cur - 2) % 8; steps.append('turns left')
        elif kind == 'right': cur = (cur + 2) % 8; steps.append('turns right')
        elif kind == 'about': cur = (cur + 4) % 8; steps.append('takes an about-turn')
        else:
            a = r.choice([45, 90, 135, 180, 225, 270]); cw = r.choice([True, False]); cur = (cur + (a // 45 if cw else -a // 45)) % 8
            steps.append(f'turns {a}° {"clockwise" if cw else "anticlockwise"}')
    txt = ', then '.join(steps)
    w = [D8[(cur + 4) % 8], D8[(cur + 2) % 8], D8[(cur - 2) % 8], D8[h]]
    return dict(q=f'{name} is facing {D8[h]}. {name} {txt}. Which direction is {name} facing now?', a=D8[cur], w=w,
                ex=f'Measure every turn in 45° steps clockwise from {D8[h]}: right = +90°, left = −90°, about-turn = 180°, clockwise adds and anticlockwise subtracts. The net turn is {((cur - h) % 8) * 45}° clockwise, so {name} faces {D8[cur]}. Distances walked do not change the facing direction.',
                fast='Add up all turns as signed degrees (clockwise +), reduce modulo 360°, then rotate the starting direction.', secs=40, d='core', topic=C2, k='ch10.face', data={'_t': 0})


def shadow(r):
    time = r.choice(['morning', 'evening']); side = r.choice(['right', 'left', 'behind', 'in front of']); name = r.choice(NAMES)
    shadow_dir = 6 if time == 'morning' else 2          # sun East in the morning -> shadow West
    rel = {'right': 2, 'left': -2, 'behind': 4, 'in front of': 0}[side]
    face = (shadow_dir - rel) % 8
    where = {'right': 'to the right of', 'left': 'to the left of', 'behind': 'behind', 'in front of': 'in front of'}[side]
    return dict(q=f'One {time}, {name} stands in the sun so that {name}\'s shadow falls exactly {where} {name}. Which direction is {name} facing?', a=D8[face], w=[D8[(face + 4) % 8], D8[(face + 2) % 8], D8[(face - 2) % 8]] + D8[1::2],
                ex=f'In the {time} the sun is in the {"East" if time == "morning" else "West"}, so shadows fall towards the {D8[shadow_dir]}. The shadow is {where} {name}, i.e. {D8[shadow_dir]} is {"on the right" if side == "right" else "on the left" if side == "left" else "behind" if side == "behind" else "in front"}. That happens when {name} faces {D8[face]}.',
                fast='Morning shadow points West, evening shadow points East; then turn yourself until that direction is on the stated side.', secs=40, d='moderate', topic=C5, k='ch10.shadow', data={'_t': 0})


def renamed(r):
    k = r.choice([1, 2, 3, 5, 6, 7])          # every direction is renamed k steps (45° each) clockwise
    a, b = r.sample(range(8), 2)
    ask = r.choice([x for x in range(8) if x not in (a, b)])
    ans = D8[(ask + k) % 8]
    return dict(q=f'If {D8[a]} is called {D8[(a + k) % 8]}, {D8[b]} is called {D8[(b + k) % 8]}, and the other directions are renamed in the same way, what is {D8[ask]} called?', a=ans,
                w=[D8[(ask - k) % 8], D8[(ask + k + 2) % 8], D8[(ask + 4) % 8], D8[ask]],
                ex=f'{D8[a]} → {D8[(a + k) % 8]} is a rotation of {k * 45}° clockwise, and {D8[b]} → {D8[(b + k) % 8]} confirms it. Rotating {D8[ask]} by the same {k * 45}° clockwise gives {ans}. Rotating the other way (anticlockwise) is the common mistake. Drawing the compass and turning it helps.',
                fast='Find the rotation angle from one given pair, then rotate the asked direction by the same angle.', secs=40, d='moderate', topic=C6, k='ch10.rename', data={'_t': 0})


def relative(r):
    names = r.sample(['P', 'Q', 'R', 'S', 'T'], 3); A, B, C = names
    trip = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
    a_dir = r.choice([0, 4]); c_dir = r.choice([2, 6])
    pa = (0, trip[0] if a_dir == 0 else -trip[0]); pc = (trip[1] if c_dir == 2 else -trip[1], 0)
    kind = r.choice(['dist', 'dir'])
    if kind == 'dist':
        return dict(q=f'{A} is {trip[0]} m to the {D8[a_dir]} of {B}. {C} is {trip[1]} m to the {D8[c_dir]} of {B}. What is the distance between {A} and {C}?', a=f'{trip[2]} m',
                    w=[f'{trip[0] + trip[1]} m', f'{abs(trip[1] - trip[0])} m', f'{trip[2] + 1} m', f'{trip[2] * 2} m'],
                    ex=f'{A} and {C} are along perpendicular lines from {B}, so {B} is the right-angle corner. Distance {A}{C} = √({trip[0]}² + {trip[1]}²) = √{trip[2] ** 2} = {trip[2]} m.',
                    fast=f'Recognise the {trip[0]}-{trip[1]}-{trip[2]} Pythagorean triple.', secs=30, d='core', topic=C4, check=str(trip[2]), k='ch10.rel', data={'_t': 0})
    dx, dy = pc[0] - pa[0], pc[1] - pa[1]; ans = quadrant(dx, dy)
    return dict(q=f'{A} is {trip[0]} m to the {D8[a_dir]} of {B}. {C} is {trip[1]} m to the {D8[c_dir]} of {B}. In which direction is {C} from {A}?', a=ans,
                w=[quadrant(-dx, -dy), quadrant(dx, -dy), quadrant(-dx, dy), D8[c_dir]],
                ex=f'Put {B} at the origin: {A} is at ({pa[0]}, {pa[1]}) and {C} at ({pc[0]}, {pc[1]}). Going from {A} to {C} means moving {abs(dx)} m {"East" if dx > 0 else "West"} and {abs(dy)} m {"North" if dy > 0 else "South"}, so {C} is {ans} of {A}. "{A} from {C}" would be the opposite direction.',
                fast='Draw B as the centre, mark A and C, and read the direction from A (the reference point) to C.', secs=40, d='moderate', topic=C1, k='ch10.rel', data={'_t': 0})


BANKS = {U: [(distance, 5), (position, 5), (facing, 5), (shadow, 4), (renamed, 3), (relative, 5)]}
