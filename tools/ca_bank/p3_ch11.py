"""Paper 3 Ch 11 — Seating Arrangements: extra MCQ templates.
Puzzles are generated from a random arrangement; clues are added until brute force over all arrangements
leaves exactly one solution. Conventions: in a row facing North a person's right is East (towards the
right end as we look at the row from behind); facing South it is the opposite; in a circle facing the
centre a person's right is anticlockwise."""
from common import *
import itertools

U = 'fnd-p3-ch11-u01'
C1, C2, C3, C4, C5 = 'Types of arrangement and types of information', 'One row: facing North vs facing South', 'Two rows facing each other', 'Circular arrangements', 'Method — from clues to diagram'
NUMW = {5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight'}
ORDW = {1: 'immediate', 2: 'second', 3: 'third'}


def names_for(r, n):
    pool = r.choice(['ABCDEFGH', 'PQRSTUVW', 'JKLMNOPQ'])
    return list(pool[:n])


# ---------- row ----------
def row_right(pos, face, k):          # position index of the person k places to the right
    return pos + k if face == 'North' else pos - k


def row_clues(r, arr, face):
    n = len(arr); P = {x: i for i, x in enumerate(arr)}; out = []
    a, b = r.sample(arr, 2); kind = r.choice(['right', 'left', 'end', 'between', 'nbr', 'notnbr', 'middle'])
    if kind in ('right', 'left'):
        k = r.choice([1, 1, 2, 3]); x = None
        tgt = row_right(P[b], face, k if kind == 'right' else -k)
        if 0 <= tgt < n: x = arr[tgt]
        if x: return (x, kind, k, b), f'{x} is {ORDW[k]} to the {kind} of {b}.' if k > 1 else f'{x} is immediately to the {kind} of {b}.'
        return None
    if kind == 'end':
        if P[a] in (0, n - 1): return (a, 'end'), f'{a} is at one of the two ends.'
        return (a, 'notend'), f'{a} is not at either end.'
    if kind == 'between':
        g = abs(P[a] - P[b]) - 1
        if g in (1, 2): return (a, b, 'gap', g), f'There {"is exactly one person" if g == 1 else "are exactly two people"} between {a} and {b}.'
        return None
    if kind == 'nbr':
        if abs(P[a] - P[b]) == 1: return (a, b, 'nbr'), f'{a} sits next to {b}.'
        return (a, b, 'notnbr'), f'{a} does not sit next to {b}.'
    if kind == 'middle' and n % 2 == 1:
        m = arr[n // 2]; return (m, 'middle'), f'{m} is in the exact middle of the row.'
    return None


def row_ok(arr, c, face):
    n = len(arr); P = {x: i for i, x in enumerate(arr)}
    t = c[-1] if isinstance(c[-1], str) else c[-2]
    if c[1] in ('right', 'left'):
        x, kind, k, b = c; return P[x] == row_right(P[b], face, k if kind == 'right' else -k)
    if c[1] == 'end': return P[c[0]] in (0, n - 1)
    if c[1] == 'notend': return P[c[0]] not in (0, n - 1)
    if c[1] == 'middle': return P[c[0]] == n // 2
    if c[2] == 'gap': return abs(P[c[0]] - P[c[1]]) - 1 == c[3]
    if c[2] == 'nbr': return abs(P[c[0]] - P[c[1]]) == 1
    if c[2] == 'notnbr': return abs(P[c[0]] - P[c[1]]) != 1
    raise ValueError(c)


def solve_row(r, n, face):
    people = names_for(r, n); arr = people[:]; r.shuffle(arr)
    clues, texts = [], []
    sols = list(itertools.permutations(people))
    for _ in range(60):
        c = row_clues(r, arr, face)
        if not c or c[1] in texts: continue
        new = [s for s in sols if row_ok(s, c[0], face)]
        if len(new) == len(sols): continue
        sols = new; clues.append(c[0]); texts.append(c[1])
        if len(sols) == 1: break
    if len(sols) != 1 or len(texts) > 7: return None
    return people, arr, texts


def row_q(r):
    n = r.choice([5, 6, 7]); face = r.choice(['North', 'North', 'South'])
    s = solve_row(r, n, face)
    if not s: return None
    people, arr, texts = s
    # the left end as seen by the persons themselves
    left_end = arr[0] if face == 'North' else arr[-1]; right_end = arr[-1] if face == 'North' else arr[0]
    kind = r.choice(['leftend', 'rightend', 'kright', 'between', 'count'])
    P = {x: i for i, x in enumerate(arr)}
    if kind in ('leftend', 'rightend'):
        ans = left_end if kind == 'leftend' else right_end; ask = f'Who is at the extreme {"left" if kind == "leftend" else "right"} end of the row?'
    elif kind == 'kright':
        b = r.choice(arr); k = r.choice([1, 2]); side = r.choice(['right', 'left'])
        t = row_right(P[b], face, k if side == 'right' else -k)
        if not 0 <= t < n: return None
        ans = arr[t]; ask = f'Who is immediately to the {side} of {b}?' if k == 1 else f'Who is second to the {side} of {b}?'
    elif kind == 'between':
        i = r.randint(1, n - 2); ans = arr[i]; ask = f'Who sits between {arr[i - 1]} and {arr[i + 1]}?'
    else:
        a, b = r.sample(arr, 2); g = abs(P[a] - P[b]) - 1
        if g < 1: return None
        ans = str(g); ask = f'How many people sit between {a} and {b}?'
    order = ' – '.join(arr)
    if kind == 'count':
        w = [str(x) for x in range(0, n - 1) if str(x) != ans]
    else:
        w = [x for x in people if x != ans]
    r.shuffle(w)
    view = 'listed from left to right as seen from behind them' if face == 'North' else 'listed from West to East; facing South, their right hand points West'
    return dict(q=f'{NUMW[n]} friends {", ".join(people[:-1])} and {people[-1]} sit in a row facing {face}. ' + ' '.join(texts) + ' ' + ask, a=ans, w=w,
                ex=f'Draw {n} seats and place the definite clues first (ends, middle, "immediate" clues), then test the remaining possibilities. Only one arrangement satisfies every clue: {order} ({view}). Reading the question from this diagram gives {ans}. Remember that left and right are taken from the persons\' own point of view.',
                fast='Start with the clue that fixes a position (end/middle/immediate neighbour), draw two cases at most, and kill cases with "not" clues.', secs=150, d='hard', topic=C2 if kind != 'count' else C5,
                check=ans if kind == 'count' else None, k='ch11.row', data={'_t': 0})


# ---------- circle ----------
def circ_clues(r, arr):
    n = len(arr); P = {x: i for i, x in enumerate(arr)}
    a, b = r.sample(arr, 2); kind = r.choice(['right', 'left', 'nbr', 'notnbr', 'opp'])
    if kind in ('right', 'left'):
        k = r.choice([1, 1, 2, 3]); t = (P[b] - k) % n if kind == 'right' else (P[b] + k) % n     # right = anticlockwise (index − 1)
        x = arr[t]
        return (x, kind, k, b), (f'{x} is {ORDW[k]} to the {kind} of {b}.' if k > 1 else f'{x} is immediately to the {kind} of {b}.')
    if kind == 'nbr':
        if (P[a] - P[b]) % n in (1, n - 1): return (a, b, 'nbr'), f'{a} sits next to {b}.'
        return (a, b, 'notnbr'), f'{a} does not sit next to {b}.'
    if kind == 'opp' and n % 2 == 0:
        if (P[a] - P[b]) % n == n // 2: return (a, b, 'opp'), f'{a} sits directly opposite {b}.'
        return None
    return None


def circ_ok(arr, c):
    n = len(arr); P = {x: i for i, x in enumerate(arr)}
    if c[1] in ('right', 'left'):
        x, kind, k, b = c; return P[x] == ((P[b] - k) % n if kind == 'right' else (P[b] + k) % n)
    if c[2] == 'nbr': return (P[c[0]] - P[c[1]]) % n in (1, n - 1)
    if c[2] == 'notnbr': return (P[c[0]] - P[c[1]]) % n not in (1, n - 1)
    if c[2] == 'opp': return (P[c[0]] - P[c[1]]) % n == n // 2


def circle_q(r):
    n = r.choice([5, 6, 7, 8]); people = names_for(r, n); arr = people[:]; r.shuffle(arr)
    first = people[0]
    sols = [(first,) + p for p in itertools.permutations(people[1:])]     # fix one person: rotations are the same arrangement
    k0 = arr.index(first); arr = arr[k0:] + arr[:k0]
    texts = []
    for _ in range(80):
        c = circ_clues(r, arr)
        if not c or c[1] in texts: continue
        new = [s for s in sols if circ_ok(s, c[0])]
        if len(new) == len(sols): continue
        sols = new; texts.append(c[1])
        if len(sols) == 1: break
    if len(sols) != 1 or len(texts) > 7: return None
    P = {x: i for i, x in enumerate(arr)}
    kind = r.choice(['right', 'left', 'opp' if n % 2 == 0 else 'right'])
    b = r.choice(arr)
    if kind == 'opp': ans = arr[(P[b] + n // 2) % n]; ask = f'Who sits directly opposite {b}?'
    else:
        k = r.choice([1, 2]); ans = arr[(P[b] - k) % n] if kind == 'right' else arr[(P[b] + k) % n]
        ask = f'Who is {"immediately to the" if k == 1 else "second to the"} {kind} of {b}?'
    if ans == b: return None
    w = [x for x in people if x not in (ans, b)]; r.shuffle(w)
    cw = ' → '.join(arr + [arr[0]])
    return dict(q=f'{NUMW[n]} friends {", ".join(people[:-1])} and {people[-1]} sit around a round table, all facing the centre. ' + ' '.join(texts) + ' ' + ask, a=ans, w=w,
                ex=f'Fix one person\'s seat (rotations do not create new arrangements) and place the others using the clues. Facing the centre, a person\'s right is the anticlockwise side. The only arrangement that fits all clues, going clockwise, is {cw}. From it, the answer is {ans}.',
                fast='Fix the person mentioned most, place "immediate" and "opposite" clues next, and write left/right as anticlockwise/clockwise for people facing the centre.', secs=150, d='hard', topic=C4, k='ch11.circle', data={'_t': 0})


# ---------- simple position counting in a row (types of information) ----------
def rank_q(r):
    n = r.randint(15, 60); a = r.randint(2, n - 3); b = n - a + 1
    kind = r.choice(['total', 'right'])
    name = r.choice(['Kiran', 'Rohit', 'Sana', 'Dev'])
    if kind == 'total':
        return dict(q=f'In a row of students facing North, {name} is {ordn(a)} from the left end and {ordn(b)} from the right end. How many students are in the row?', a=str(n),
                    w=[str(n + 1), str(n - 1), str(a + b + 1), str(abs(a - b) + 1)],
                    ex=f'Positions from both ends count {name} twice. Total = (position from left) + (position from right) − 1 = {a} + {b} − 1 = {n}. Adding without subtracting 1 gives {a + b}, which double-counts {name}.',
                    fast='Total = left rank + right rank − 1.', secs=20, d='core', topic=C1, check=str(n), k='ch11.rank', data={'a': a, 'b': b, 'kind': 'total'})
    return dict(q=f'In a row of {n} students facing North, {name} is {ordn(a)} from the left end. What is {name}\'s position from the right end?', a=ordn(b),
                w=[ordn(b + 1), ordn(b - 1), ordn(n - a), ordn(a)] if n - a != b else [ordn(b + 1), ordn(b - 1), ordn(b + 2), ordn(a)],
                ex=f'Position from right = total − position from left + 1 = {n} − {a} + 1 = {b}. So {name} is {ordn(b)} from the right end. Forgetting the +1 gives {ordn(n - a)}.',
                fast='Right rank = total − left rank + 1.', secs=20, d='core', topic=C1, check=str(b), k='ch11.rank', data={'a': a, 'n': n, 'kind': 'right'})


BANKS = {U: [(row_q, 14), (circle_q, 10), (rank_q, 3)]}
