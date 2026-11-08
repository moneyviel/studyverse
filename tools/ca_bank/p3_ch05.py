"""Paper 3 Ch 5 — Permutations and Combinations: extra MCQ templates (answers computed)."""
from common import *
import math
from collections import Counter

U = 'fnd-p3-ch05-u01'
C1, C2, C3, C4, C5 = 'Fundamental principles of counting', 'Factorial notation', 'Permutations: arrangements where order matters', 'Circular permutations', 'Permutations with restrictions'
C6, C7, C8, C9 = 'Alike things and repetition', 'Combinations: selections where order does not matter', 'Properties of ⁿCᵣ', 'Special selections: some or all, alike things, independent groups, geometry'
fact = math.factorial
P_ = math.perm
C_ = math.comb
WORDS = ['ACCOUNT', 'BALANCE', 'AUDITOR', 'LEDGER', 'CAPITAL', 'RESERVE', 'DIVIDEND', 'BUDGET', 'MARKET', 'TALLY', 'ASSET', 'SURPLUS', 'PAYROLL', 'TAXES',
         'VOUCHER', 'DEPOSIT', 'BANKER', 'CHEQUE', 'MORTGAGE', 'GOODWILL', 'ARREARS', 'DEBENTURE']
VOW = set('AEIOU')


def npr(r):
    n = r.randint(6, 12); k = r.randint(2, 4)
    return dict(q=f'In how many ways can {k} different prizes be given to {n} students if no student gets more than one prize?', a=inr(P_(n, k)),
                w=[inr(C_(n, k)), inr(n ** k), inr(k ** n) if k ** n < 10 ** 7 else inr(P_(n, k - 1)), inr(P_(n, k - 1))],
                ex=f'Prizes are different, so order matters: the first prize can go to any of {n} students, the second to any of the remaining {n - 1}, and so on. Ways = ⁿPᵣ = {n}P{k} = ' + ' × '.join(str(n - i) for i in range(k)) + f' = {inr(P_(n, k))}. Using {n}C{k} = {C_(n, k)} would treat the prizes as identical.',
                fast=f'Multiply {k} falling numbers starting at {n}.', secs=25, d='core', topic=C3, check=str(P_(n, k)), k='ch05.npr', data={'n': n, 'k': k})


def word_perm(w):
    c = Counter(w); v = fact(len(w))
    for x in c.values(): v //= fact(x)
    return v


def word(r):
    w = r.choice(WORDS)
    if len(w) > 8: return None
    c = Counter(w); v = word_perm(w); reps = {k: x for k, x in c.items() if x > 1}
    if not reps: return None
    den = ' × '.join(f'{x}!' for x in reps.values())
    return dict(q=f'How many different arrangements can be made from all the letters of the word "{w}"?', a=inr(v),
                w=[inr(fact(len(w))), inr(v * 2) if v * 2 != fact(len(w)) else inr(v // 2), inr(fact(len(w) - 1)), inr(v // 2 if len(reps) > 1 and v // 2 != fact(len(w)) else v * 3)],
                ex=f'"{w}" has {len(w)} letters, of which ' + ', '.join(f'{k} occurs {x} times' for k, x in reps.items()) + f'. Swapping identical letters gives no new word, so divide: {len(w)}!/({den}) = {inr(fact(len(w)))}/{math.prod(fact(x) for x in reps.values())} = {inr(v)}. Writing {len(w)}! ignores the repeated letters.',
                fast=f'n!/(p!q!…): count each repeated letter once; {len(w)}! = {inr(fact(len(w)))}.', secs=30, d='core', topic=C6, check=str(v), k='ch05.word', data={'w': w})


def vowels_together(r):
    w = r.choice(WORDS)
    if len(w) > 8 or len(w) < 5: return None
    vs = [x for x in w if x in VOW]; cs = [x for x in w if x not in VOW]
    if len(vs) < 2: return None
    block = word_perm(''.join(vs)); outer = word_perm(''.join(cs) + '*')
    v = block * outer
    return dict(q=f'In how many arrangements of the letters of "{w}" do all the vowels come together?', a=inr(v),
                w=[inr(word_perm(w)), inr(outer), inr(word_perm(w) - v), inr(v * 2)],
                ex=f'Tie the vowels ({", ".join(vs)}) into one block. Then arrange the block with the {len(cs)} consonants: {len(cs) + 1} units, giving {inr(outer)} ways (dividing for repeated letters). The vowels arrange inside the block in {block} ways. Total = {inr(outer)} × {block} = {inr(v)}. Forgetting the inside arrangement gives {inr(outer)}.',
                fast='Block method: (units outside)! × (letters inside)!, each divided for repeats.', secs=45, d='moderate', topic=C5, check=str(v), k='ch05.vowels', data={'w': w})


def row_together(r):
    n = r.randint(5, 8); k = r.randint(2, 3)
    if k >= n - 1: return None
    v = fact(n - k + 1) * fact(k); kind = r.choice(['together', 'not'])
    if kind == 'not' and k == 2:
        ans = fact(n) - v
        return dict(q=f'In how many ways can {n} people sit in a row so that two particular people do NOT sit next to each other?', a=inr(ans),
                    w=[inr(v), inr(fact(n)), inr(fact(n) - fact(n - 1)), inr(ans // 2)],
                    ex=f'Total arrangements = {n}! = {inr(fact(n))}. Arrangements with the two together: treat them as one unit, ({n - 1})! × 2! = {inr(v)}. So "not together" = {inr(fact(n))} − {inr(v)} = {inr(ans)}. Forgetting the 2! inside the unit is the usual slip.',
                    fast=f'Not together = total − together = {n}! − 2 × ({n - 1})!.', secs=40, d='moderate', topic=C5, check=str(ans), k='ch05.row', data={'n': n, 'k': 2, 'kind': 'NOT'})
    return dict(q=f'In how many ways can {n} books be arranged on a shelf if {k} particular books must always be together?', a=inr(v),
                w=[inr(fact(n - k + 1)), inr(fact(n)), inr(fact(n) - v), inr(fact(n - k) * fact(k))],
                ex=f'Tie the {k} books into one bundle. Now there are {n - k} + 1 = {n - k + 1} units, arranged in {n - k + 1}! = {inr(fact(n - k + 1))} ways. The books inside the bundle can be arranged in {k}! = {fact(k)} ways. Total = {inr(fact(n - k + 1))} × {fact(k)} = {inr(v)}.',
                fast=f'Bundle method: ({n - k + 1})! outside × {k}! inside.', secs=30, d='core', topic=C5, check=str(v), k='ch05.row', data={'n': n, 'k': k, 'kind': 'together'})


def circular(r):
    n = r.randint(5, 9); kind = r.choice(['together', 'apart', 'plain'])
    if kind == 'plain':
        v = fact(n - 1)
        return dict(q=f'In how many ways can {n} persons be seated around a circular table?', a=inr(v), w=[inr(fact(n)), inr(fact(n - 1) // 2), inr(fact(n - 2)), inr(fact(n) // 2)],
                    ex=f'In a circle, rotating everybody one seat gives the same arrangement, so fix one person and arrange the other {n - 1} around: ({n} − 1)! = {inr(v)}. Dividing by 2 is only for garlands/necklaces, where clockwise and anticlockwise look the same.',
                    fast=f'Circular seating of n people = (n − 1)! = {n - 1}!.', secs=20, d='core', topic=C4, check=str(v), k='ch05.circ', data={'n': n, 'kind': 'plain'})
    tog = fact(n - 2) * 2
    v = tog if kind == 'together' else fact(n - 1) - tog
    return dict(q=f'In how many ways can {n} persons sit around a round table if two particular persons {"always sit together" if kind == "together" else "never sit next to each other"}?', a=inr(v),
                w=[inr(fact(n - 2)), inr(fact(n - 1)), inr(fact(n - 1) - tog if kind == 'together' else tog), inr(fact(n - 1) * 2)],
                ex=f'Circular arrangements of {n} = ({n} − 1)! = {inr(fact(n - 1))}. With the pair tied together there are {n - 1} units in a circle: ({n - 2})! × 2 = {inr(tog)}. ' + (f'So the answer is {inr(tog)}.' if kind == 'together' else f'Never together = {inr(fact(n - 1))} − {inr(tog)} = {inr(v)}.') + ' The pair can swap seats, hence × 2.',
                fast=f'Together = 2 × ({n} − 2)!; apart = ({n} − 1)! − 2 × ({n} − 2)!.', secs=40, d='moderate', topic=C4, check=str(v), k='ch05.circ', data={'n': n, 'kind': kind})


def garland(r):
    n = r.randint(5, 10); v = fact(n - 1) // 2
    return dict(q=f'In how many ways can {n} different beads be strung into a necklace?', a=inr(v), w=[inr(fact(n - 1)), inr(fact(n)), inr(fact(n) // 2), inr(fact(n - 2))],
                ex=f'Fix one bead to remove rotations: ({n} − 1)! = {inr(fact(n - 1))}. A necklace can also be turned over, so each clockwise arrangement equals its anticlockwise mirror. Divide by 2: {inr(v)}. Seating people around a table does not use this division, because people facing inward are not mirror-equal.',
                fast=f'Necklace / garland = ({n} − 1)!/2.', secs=20, d='core', topic=C4, check=str(v), k='ch05.neck', data={'n': n})


def committee(r):
    m, w = r.randint(4, 9), r.randint(3, 7); k = r.randint(3, 6); at = r.randint(1, min(3, w, k - 1))
    if k > m + w - 1: return None
    v = sum(C_(w, j) * C_(m, k - j) for j in range(at, min(w, k) + 1))
    naive = C_(w, at) * C_(m + w - at, k - at)
    if naive == v: return None
    return dict(q=f'A committee of {k} is to be chosen from {m} men and {w} women. In how many ways can this be done if it must include at least {at} wom{"a" if at == 1 else "e"}n?', a=inr(v),
                w=[inr(naive), inr(C_(m + w, k)), inr(C_(w, at) * C_(m, k - at)), inr(C_(m + w, k) - v)],
                ex=f'Add the cases by the exact number of women: ' + ' + '.join(f'{w}C{j} × {m}C{k - j}' for j in range(at, min(w, k) + 1)) + f' = {inr(v)}. (Or total {m + w}C{k} minus the cases with fewer than {at} women.) Choosing {at} women first and then "any" {k - at} counts some committees more than once ({inr(naive)}).',
                fast=f'Complement: {m + w}C{k} − Σ (cases with fewer than {at} women).', secs=60, d='moderate', topic=C7, check=str(v), k='ch05.comm', data={'m': m, 'w': w, 'k': k, 'at': at})


def ncr_eq(r):
    a, b = r.sample(range(2, 12), 2); n = a + b
    return dict(q=f'If ⁿC{a} = ⁿC{b} (where {a} ≠ {b}), then n =', a=str(n), w=[str(abs(a - b)), str(a * b), str(n + 1), str(n - 1)],
                ex=f'ⁿCᵣ = ⁿCₙ₋ᵣ: choosing r items to take is the same as choosing n − r items to leave. So ⁿC{a} = ⁿC{b} with {a} ≠ {b} means {a} + {b} = n, i.e. n = {n}. The difference {abs(a - b)} is a common slip.',
                fast='Equal ⁿCs with different lower numbers: n = sum of the lower numbers.', secs=15, d='core', topic=C8, check=str(n), k='ch05.ncreq', data={'a': a, 'b': b})


def pascal(r):
    n = r.randint(6, 14); k = r.randint(2, n - 2); v = C_(n + 1, k)
    return dict(q=f'The value of {n}C{k} + {n}C{k - 1} is:', a=inr(v), w=[inr(C_(n, k + 1)), inr(C_(n + 1, k - 1)) if C_(n + 1, k - 1) != v else inr(v + 1), inr(C_(n, k) * 2), inr(C_(n + 1, k + 1))],
                ex=f'Pascal\'s rule: ⁿCᵣ + ⁿCᵣ₋₁ = ⁽ⁿ⁺¹⁾Cᵣ. So {n}C{k} + {n}C{k - 1} = {n + 1}C{k} = {inr(v)}. Check by direct values: {inr(C_(n, k))} + {inr(C_(n, k - 1))} = {inr(v)}. The idea: a selection of {k} from {n + 1} items either includes one particular item or it does not.',
                fast='Pascal: add 1 to the upper number and keep the larger lower number.', secs=20, d='core', topic=C8, check=str(v), k='ch05.pascal', data={'n': n, 'k': k})


def geometry(r):
    n = r.randint(8, 16); k = r.randint(3, 6); kind = r.choice(['lines', 'triangles'])
    if kind == 'lines': v = C_(n, 2) - C_(k, 2) + 1; naive = C_(n, 2)
    else: v = C_(n, 3) - C_(k, 3); naive = C_(n, 3)
    return dict(q=f'There are {n} points in a plane, of which exactly {k} lie on one straight line; no other three are collinear. The number of {"straight lines" if kind == "lines" else "triangles"} that can be formed by joining them is:',
                a=inr(v), w=[inr(naive), inr(naive - C_(k, 2 if kind == 'lines' else 3) - 1) if kind == 'lines' else inr(naive - C_(k, 2)), inr(v + 1), inr(naive - C_(k, 3 if kind == 'lines' else 2))],
                ex=(f'Pairs of points: {n}C2 = {C_(n, 2)}. The {k} collinear points would give {k}C2 = {C_(k, 2)} lines but really form only 1 line. Lines = {C_(n, 2)} − {C_(k, 2)} + 1 = {v}.' if kind == 'lines' else
                    f'Any 3 points make a triangle unless they are collinear. Triples: {n}C3 = {C_(n, 3)}; the {k} collinear points give {k}C3 = {C_(k, 3)} useless triples. Triangles = {C_(n, 3)} − {C_(k, 3)} = {v}.') + ' Forgetting the collinear correction is the usual error.',
                fast=('ⁿC₂ − ᵏC₂ + 1' if kind == 'lines' else 'ⁿC₃ − ᵏC₃') + ' — subtract the collinear selections.', secs=40, d='moderate', topic=C9, check=str(v),
                k='ch05.geom', data={'n': n, 'k': k, 'kind': kind})


def diagonals(r):
    n = r.randint(6, 20); kind = r.choice(['diag', 'shake'])
    if kind == 'diag':
        v = n * (n - 3) // 2
        return dict(q=f'How many diagonals does a polygon with {n} sides have?', a=str(v), w=[str(C_(n, 2)), str(n * (n - 3)), str(C_(n, 2) - 1), str(v + n)],
                    ex=f'Any two vertices are joined by a line: {n}C2 = {C_(n, 2)}. Of these, {n} are the sides, so diagonals = {C_(n, 2)} − {n} = {v} = n(n − 3)/2. Each vertex joins {n - 3} others by diagonals; halve because each diagonal has two ends.',
                    fast='Diagonals of an n-sided polygon = n(n − 3)/2.', secs=20, d='core', topic=C9, check=str(v), k='ch05.diag', data={'n': n})
    v = C_(n, 2)
    return dict(q=f'At a meeting each of {n} members shakes hands once with every other member. The total number of handshakes is:', a=str(v), w=[str(n * (n - 1)), str(n * n), str(v - n), str(v + n)],
                ex=f'A handshake is a selection of 2 people out of {n}; order does not matter. Number = {n}C2 = {n} × {n - 1}/2 = {v}. Using {n} × {n - 1} = {n * (n - 1)} counts each handshake twice (A with B and B with A).',
                fast='Handshakes among n people = n(n − 1)/2 = ⁿC₂.', secs=15, d='core', topic=C7, check=str(v), k='ch05.shake', data={'n': n})


def digits(r):
    pool = sorted(r.sample(range(0, 10), r.randint(5, 7))); k = r.choice([3, 4]); cond = r.choice(['even', 'div5', 'odd'])
    import itertools
    test = {'even': lambda x: x % 2 == 0, 'div5': lambda x: x % 5 == 0, 'odd': lambda x: x % 2 == 1}[cond]
    nums_ = [p for p in itertools.permutations(pool, k) if p[0] != 0]
    v = sum(1 for p in nums_ if test(int(''.join(map(str, p)))))
    if v < 5: return None
    word = {'even': 'even', 'div5': 'divisible by 5', 'odd': 'odd'}[cond]
    desc = f'{word} {k}-digit numbers' if cond != 'div5' else f'{k}-digit numbers divisible by 5'
    return dict(q=f'How many {desc}, with no digit repeated, can be formed using the digits {", ".join(map(str, pool))}?', a=inr(v),
                w=[inr(len(nums_)), inr(P_(len(pool), k)), inr(v + P_(len(pool) - 2, k - 2)), inr(abs(len(nums_) - v)) if len(nums_) != 2 * v else inr(v * 2)],
                ex=f'Fill the restricted places first: the last digit must make the number {word}, and the first digit cannot be 0. ' + ('Because 0 is among the digits, split into "last digit 0" and "last digit not 0" cases. ' if 0 in pool else '') + f'Counting each case and adding gives {inr(v)}. Ignoring the restriction on the first digit or on the last digit gives a larger number.',
                fast='Units place first, then the first digit (no 0), then the remaining places in falling order; add cases when 0 is a possible last digit.', secs=60, d='hard', topic=C5,
                check=str(v), k='ch05.digits', data={'pool': pool, 'k': k, 'cond': word})


def alike_sel(r):
    a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 5)
    v = (a + 1) * (b + 1) * (c + 1) - 1
    return dict(q=f'A basket has {a} identical apples, {b} identical mangoes and {c} identical oranges. In how many ways can a selection of at least one fruit be made?', a=str(v),
                w=[str(v + 1), str(2 ** (a + b + c) - 1), str(a * b * c), str((a + 1) * (b + 1) * (c + 1) - 3)],
                ex=f'Identical items: from {a} apples we can take 0, 1, …, {a} — that is {a + 1} choices; similarly {b + 1} for mangoes and {c + 1} for oranges. Total = {a + 1} × {b + 1} × {c + 1} = {v + 1}, which includes taking nothing. Subtract that one case: {v}. 2ⁿ − 1 applies only to different items.',
                fast='(p + 1)(q + 1)(r + 1) − 1 for identical items.', secs=30, d='moderate', topic=C9, check=str(v), k='ch05.alike', data={'a': a, 'b': b, 'c': c})


def letters_boxes(r):
    n = r.randint(3, 7); m = r.randint(2, 5)
    v = m ** n
    return dict(q=f'In how many ways can {n} different letters be posted in {m} letter boxes (any box may receive any number of letters)?', a=inr(v),
                w=[inr(n ** m), inr(P_(max(m, n), min(m, n))), inr(C_(m + n - 1, n)), inr(m * n)],
                ex=f'Each letter independently chooses one of the {m} boxes, so by the multiplication principle the number of ways is {m} × {m} × … ({n} times) = {m}^{n} = {inr(v)}. Writing {n}^{m} reverses the roles: it is the letters that choose boxes, not the boxes that choose letters.',
                fast='Each letter picks a box: (number of boxes) raised to (number of letters).', secs=20, d='core', topic=C1, check=str(v), k='ch05.boxes', data={'n': n, 'm': m})


def routes(r):
    m, n = r.randint(2, 7), r.randint(2, 7)
    v = m * n * (m - 1) * (n - 1)
    return dict(q=f'There are {m} roads from town A to town B and {n} roads from B to C. In how many ways can a person go from A to C via B and return, without using any road twice?', a=str(v),
                w=[str((m * n) ** 2), str(m * n), str(m * n * (m + n)), str(2 * m * n)],
                ex=f'Going: {m} × {n} = {m * n} ways. Returning without reusing a road: {n - 1} roads from C to B and {m - 1} from B to A, so {(n - 1) * (m - 1)} ways. By the multiplication principle, total = {m * n} × {(m - 1) * (n - 1)} = {v}. Allowing the same roads again gives {(m * n) ** 2}.',
                fast='Going m × n, returning (n − 1) × (m − 1); multiply the two.', secs=30, d='core', topic=C1, check=str(v), k='ch05.routes', data={'m': m, 'n': n})


def perm_eq(r):
    n = r.randint(6, 15); a = r.choice([3, 4, 5]); b = a - 2
    k = P_(n, a) // P_(n, b)
    return dict(q=f'If ⁿP{a} = {k} × ⁿP{b}, then n =', a=str(n), w=[str(n + 1), str(n - 1), str(n + 2), str(n - 3)],
                ex=f'ⁿP{a} ÷ ⁿP{b} = (n − {b})(n − {b + 1}) because the first {b} factors cancel. So (n − {b})(n − {b + 1}) = {k}, two consecutive numbers whose product is {k}: {n - b} × {n - b - 1}. Hence n − {b} = {n - b} and n = {n}.',
                fast=f'Find consecutive numbers with product {k} ({n - b} × {n - b - 1}); then add {b}.', secs=40, d='moderate', topic=C3, check=str(n), k='ch05.permeq', data={'a': a, 'b': b, 'k': k})


def fact_eq(r):
    n = r.randint(4, 15); v = fact(n + 1) // fact(n - 1)
    return dict(q=f'If (n + 1)!/(n − 1)! = {v}, then n =', a=str(n), w=[str(n + 1), str(n - 1), str(n + 2), str(v // 2) if v // 2 > 20 else str(n - 2)],
                ex=f'(n + 1)! = (n + 1) × n × (n − 1)!, so (n + 1)!/(n − 1)! = n(n + 1). We need n(n + 1) = {v}, two consecutive numbers whose product is {v}: {n} × {n + 1}. So n = {n}. The other choice of consecutive numbers would be negative.',
                fast=f'√{v} ≈ {num(math.sqrt(v), 1)}: the smaller neighbour is n.', secs=25, d='core', topic=C2, check=str(n), k='ch05.facteq', data={'v': v})


BANKS = {U: [(npr, 2), (word, 3), (vowels_together, 2), (row_together, 2), (circular, 3), (garland, 1), (committee, 2), (ncr_eq, 2), (pascal, 1),
             (geometry, 2), (diagonals, 2), (digits, 2), (alike_sel, 2), (letters_boxes, 2), (routes, 1), (perm_eq, 2), (fact_eq, 2)]}
