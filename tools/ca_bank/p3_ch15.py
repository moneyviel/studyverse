"""Paper 3 Ch 15 — Probability: extra MCQ templates (exact fractions)."""
from common import *
import math, itertools

U = 'fnd-p3-ch15-u01'
C1, C2, C3, C4, C5, C6, C7 = 'Random experiments, sample space and events', 'Definitions of probability and odds', 'Mutually exclusive vs independent', 'Addition theorems', 'Conditional probability and compound probability', 'Random variable and probability distribution', 'Expected value and variance'


def dice(r):
    kind = r.choice(['sum', 'atleast', 'double', 'prodeven', 'diff'])
    outs = list(itertools.product(range(1, 7), repeat=2))
    if kind == 'sum': s = r.randint(3, 11); ev = [o for o in outs if sum(o) == s]; txt = f'the sum is {s}'
    elif kind == 'atleast': s = r.randint(7, 11); ev = [o for o in outs if sum(o) >= s]; txt = f'the sum is at least {s}'
    elif kind == 'double': ev = [o for o in outs if o[0] == o[1]]; txt = 'both dice show the same number'
    elif kind == 'prodeven': ev = [o for o in outs if o[0] * o[1] % 2 == 0]; txt = 'the product of the numbers is even'
    else: k = r.randint(1, 4); ev = [o for o in outs if abs(o[0] - o[1]) == k]; txt = f'the numbers differ by exactly {k}'
    p = F(len(ev), 36)
    return dict(q=f'Two fair dice are thrown. The probability that {txt} is:', a=fr(p), w=[fr(F(len(ev), 12)) if len(ev) < 12 else fr(1 - p), fr(F(len(ev) + 1, 36)), fr(F(len(ev), 21)) if F(len(ev), 21) <= 1 else fr(p / 2), fr(1 - p) if 1 - p != p else fr(p / 3)],
                ex=f'There are 6 × 6 = 36 equally likely outcomes. Favourable outcomes ({txt}): {len(ev)}' + (f', e.g. {", ".join(str(o) for o in ev[:4])}{"…" if len(ev) > 4 else ""}' if ev else '') + f'. Probability = {len(ev)}/36 = {fr(p)}. Counting only unordered pairs (21 of them) is wrong, because (1, 2) and (2, 1) are different outcomes.',
                fast='List favourable pairs on a 6 × 6 grid mentally; divide by 36.', secs=40, d='core', topic=C2, k='ch15.dice', data={'txt': txt})


def coins(r):
    n = r.randint(3, 6); k = r.randint(1, n - 1); kind = r.choice(['atleast', 'exactly', 'atmost'])
    c = {'atleast': sum(math.comb(n, j) for j in range(k, n + 1)), 'exactly': math.comb(n, k), 'atmost': sum(math.comb(n, j) for j in range(0, k + 1))}[kind]
    p = F(c, 2 ** n); word = {'atleast': 'at least', 'exactly': 'exactly', 'atmost': 'at most'}[kind]
    return dict(q=f'{n} fair coins are tossed together. The probability of getting {word} {k} head{"s" if k > 1 else ""} is:', a=fr(p), w=[fr(F(math.comb(n, k), 2 ** n)) if kind != 'exactly' else fr(F(sum(math.comb(n, j) for j in range(k, n + 1)), 2 ** n)), fr(F(k, n)), fr(1 - p) if 1 - p != p else fr(F(1, 2 ** n)), fr(F(c, 2 ** n - 1))],
                ex=f'Total outcomes = 2^{n} = {2 ** n}. Favourable outcomes ({word} {k} heads) = ' + ' + '.join(f'{n}C{j}' for j in ({'atleast': range(k, n + 1), 'exactly': [k], 'atmost': range(0, k + 1)}[kind])) + f' = {c}. Probability = {c}/{2 ** n} = {fr(p)}. For "at least" questions the complement (1 − P(fewer)) is often quicker. Each coin has 2 equally likely faces, so all 2ⁿ outcomes are equally likely.',
                fast='Use ⁿCₖ/2ⁿ for each count; use the complement for "at least one".', secs=45, d='core', topic=C1, k='ch15.coins', data={'n': n, 'k': k, 'word': word})


SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


def cards(r):
    deck = [(rk, s) for s in SUITS for rk in RANKS]
    kind = r.choice(['rank_or_suit', 'face', 'red_or_rank', 'not_suit'])
    if kind == 'rank_or_suit': rk = r.choice(['king', 'queen', 'ace', 'jack', '7']); su = r.choice(SUITS); ev = [c for c in deck if c[0] == rk or c[1] == su]; txt = f'{"an" if rk == "ace" else "a"} {rk} or a {su[:-1]}'
    elif kind == 'face': ev = [c for c in deck if c[0] in ('jack', 'queen', 'king')]; txt = 'a face card (jack, queen or king)'
    elif kind == 'red_or_rank': rk = r.choice(['king', 'queen', 'ace', 'jack', '10']); ev = [c for c in deck if c[1] in ('hearts', 'diamonds') or c[0] == rk]; txt = f'a red card or {"an" if rk == "ace" else "a"} {rk}'
    else: su = r.choice(SUITS); ev = [c for c in deck if c[1] != su]; txt = f'not a {su[:-1]}'
    p = F(len(ev), 52)
    naive = F(len(ev) + (1 if kind in ('rank_or_suit',) else 2 if kind == 'red_or_rank' else 0), 52)
    return dict(q=f'One card is drawn at random from a well-shuffled pack of 52 cards. The probability that it is {txt} is:', a=fr(p), w=[fr(naive) if naive != p else fr(p + F(1, 52)), fr(1 - p), fr(F(len(ev), 13)) if len(ev) < 13 else fr(p / 2), fr(p - F(1, 52))],
                ex=f'Count favourable cards: {len(ev)} of 52. ' + ('Add the two groups and subtract the cards that belong to both, so that no card is counted twice. ' if kind in ('rank_or_suit', 'red_or_rank') else '') + f'Probability = {len(ev)}/52 = {fr(p)}. A pack has 4 suits of 13 cards; hearts and diamonds are red; each suit has 3 face cards. Reduce the fraction to its lowest terms before matching the options.',
                fast='Count cards directly (avoid double counting the overlap), then reduce the fraction.', secs=35, d='core', topic=C4, k='ch15.cards', data={'txt': txt})


def balls(r):
    a, b = r.randint(2, 9), r.randint(2, 9); kind = r.choice(['both_a', 'one_each', 'same'])
    col = r.choice([('red', 'blue'), ('white', 'black'), ('green', 'yellow')])
    T = math.comb(a + b, 2)
    c = {'both_a': math.comb(a, 2), 'one_each': a * b, 'same': math.comb(a, 2) + math.comb(b, 2)}[kind]
    txt = {'both_a': f'both are {col[0]}', 'one_each': f'one is {col[0]} and the other {col[1]}', 'same': 'both are of the same colour'}[kind]
    p = F(c, T)
    wr = [F(a, a + b) ** 2 if kind == 'both_a' else F(a * b, (a + b) ** 2) * 2 if kind == 'one_each' else F(a * a + b * b, (a + b) ** 2), F(c, (a + b) ** 2), 1 - p, F(c + 1, T)]
    return dict(q=f'A bag contains {a} {col[0]} and {b} {col[1]} balls. Two balls are drawn at random without replacement. The probability that {txt} is:', a=fr(p), w=[fr(x) for x in wr],
                ex=f'Number of ways to draw 2 balls from {a + b}: {a + b}C2 = {T}. Favourable ways ({txt}) = ' + {'both_a': f'{a}C2 = {c}', 'one_each': f'{a} × {b} = {c}', 'same': f'{a}C2 + {b}C2 = {c}'}[kind] + f'. Probability = {c}/{T} = {fr(p)}. Using "with replacement" products (like ({a}/{a + b})²) is wrong here because the first ball is not put back.',
                fast='Combinations: favourable selections ÷ ⁿC₂; or multiply conditional probabilities ball by ball.', secs=45, d='moderate', topic=C5, k='ch15.balls', data={'a': a, 'b': b, 'txt': txt})


def addition(r):
    pa, pb = F(r.randint(2, 7), 10), F(r.randint(2, 7), 10); pab = F(r.randint(1, int(min(pa, pb) * 10) - 1 if min(pa, pb) > F(1, 10) else 1), 10)
    if pa + pb - pab > 1: return None
    kind = r.choice(['union', 'inter', 'neither'])
    if kind == 'union':
        v = pa + pb - pab; q = f'P(A) = {num(pa)}, P(B) = {num(pb)} and P(A ∩ B) = {num(pab)}. Then P(A ∪ B) ='; w = [pa + pb, pa * pb, pa + pb - 2 * pab]
    elif kind == 'inter':
        u = pa + pb - pab; v = pab; q = f'P(A) = {num(pa)}, P(B) = {num(pb)} and P(A ∪ B) = {num(u)}. Then P(A ∩ B) ='; w = [pa * pb, u - pa, pa + pb - u + F(1, 10)]
    else:
        v = 1 - (pa + pb - pab); q = f'P(A) = {num(pa)}, P(B) = {num(pb)} and P(A ∩ B) = {num(pab)}. The probability that neither A nor B occurs is:'; w = [1 - pa - pb if pa + pb < 1 else F(1, 10), (1 - pa) * (1 - pb), pa + pb - pab]
    return dict(q=q, a=num(v), w=[num(x) for x in w] + [num(v + F(1, 10))],
                ex=f'Addition theorem: the chance of A or B equals the chance of A plus the chance of B minus the chance of both. With the given values, P(A ∪ B) = {num(pa)} + {num(pb)} − {num(pab)} = {num(pa + pb - pab)}. ' + ('"Neither" is the complement of A ∪ B: 1 − ' + num(pa + pb - pab) + ' = ' + num(v) + '. ' if kind == 'neither' else '') + 'Multiplying P(A) × P(B) is valid only for independent events.',
                fast='Write the addition theorem and solve for the unknown; use 1 − P(A ∪ B) for "neither".', secs=30, d='core', topic=C4, check=frx(v), k='ch15.add', data={'pa': float(pa), 'pb': float(pb), 'kind': kind})


def independent(r):
    pa, pb = F(r.randint(1, 5), r.choice([6, 7, 8, 10])), F(r.randint(1, 5), r.choice([6, 7, 8, 10]))
    if pa >= 1 or pb >= 1: return None
    kind = r.choice(['union', 'neither', 'exactly'])
    names = r.choice([('A solves the problem', 'B solves it'), ('machine X works', 'machine Y works'), ('Ravi passes', 'Sita passes')])
    v = {'union': 1 - (1 - pa) * (1 - pb), 'neither': (1 - pa) * (1 - pb), 'exactly': pa * (1 - pb) + pb * (1 - pa)}[kind]
    txt = {'union': 'at least one of the two events happens', 'neither': 'neither event happens', 'exactly': 'exactly one of the two events happens'}[kind]
    w = [pa + pb if pa + pb <= 1 else pa * pb, pa * pb, 1 - v, v + F(1, 20)]
    return dict(q=f'The probability that {names[0]} is {fr(pa)} and that {names[1]} is {fr(pb)}, independently. The probability that {txt} is:', a=fr(v), w=[fr(x) for x in w],
                ex=f'For independent events, P(A ∩ B) = P(A) × P(B) = {fr(pa * pb)}. ' + {'union': f'At least one = 1 − P(neither) = 1 − (1 − {fr(pa)})(1 − {fr(pb)}) = {fr(v)}.', 'neither': f'Neither = (1 − {fr(pa)}) × (1 − {fr(pb)}) = {fr(v)}.', 'exactly': f'Exactly one = P(A)(1 − P(B)) + P(B)(1 − P(A)) = {fr(v)}.'}[kind] + ' Simply adding the probabilities double-counts the case when both happen, and can even give a value above 1.',
                fast='Work with complements: 1 − P(A), 1 − P(B); multiply for independence.', secs=40, d='moderate', topic=C3, k='ch15.indep', data={'pa': fr(pa), 'pb': fr(pb), 'txt': txt})


def conditional(r):
    pa, pb = F(r.randint(2, 8), 10), F(r.randint(2, 8), 10); pab = F(r.randint(1, 9), 20)
    if pab > min(pa, pb) or pa + pb - pab > 1: return None
    kind = r.choice(['AgB', 'BgA'])
    v = pab / pb if kind == 'AgB' else pab / pa
    return dict(q=f'P(A) = {num(pa)}, P(B) = {num(pb)} and P(A ∩ B) = {num(pab)}. Then {"P(A | B)" if kind == "AgB" else "P(B | A)"} =', a=fr(v), w=[fr(pab / pa) if kind == 'AgB' else fr(pab / pb), fr(pab), fr(pa * pb), fr(v + F(1, 10)) if v + F(1, 10) <= 1 else fr(v / 2)],
                ex=f'Conditional probability: P(A | B) = P(A ∩ B)/P(B) and P(B | A) = P(A ∩ B)/P(A). Here the condition is {"B" if kind == "AgB" else "A"}, so divide {num(pab)} by {num(pb if kind == "AgB" else pa)}: {fr(v)}. Dividing by the wrong event is the classic slip.',
                fast='Divide the joint probability by the probability of the GIVEN event (after the bar).', secs=30, d='core', topic=C5, k='ch15.cond', data={'pa': float(pa), 'pb': float(pb), 'pab': float(pab), 'kind': 'P(A | B)' if kind == 'AgB' else 'P(B | A)'})


def odds(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if math.gcd(a, b) > 1 or a == b: return None
    kind = r.choice(['favour', 'against'])
    p = F(a, a + b) if kind == 'favour' else F(b, a + b)
    return dict(q=f'The odds {"in favour of" if kind == "favour" else "against"} an event are {a} : {b}. The probability that the event happens is:', a=fr(p), w=[fr(F(b, a + b)) if kind == 'favour' else fr(F(a, a + b)), fr(F(a, b)) if F(a, b) <= 1 else fr(F(b, a)), fr(F(a, a + b + 1)), fr(F(1, a + b))],
                ex=f'Odds in favour a : b means a favourable cases for every b unfavourable, so P(happens) = a/(a + b). ' + (f'Here P = {a}/{a + b} = {fr(p)}.' if kind == 'favour' else f'Odds against {a} : {b} means P(happens) = {b}/({a} + {b}) = {fr(p)}.') + ' The ratio a/b itself is not a probability; a probability always compares favourable cases with ALL cases.',
                fast='Probability = (favourable part) ÷ (sum of both parts).', secs=20, d='core', topic=C2, k='ch15.odds', data={'a': a, 'b': b, 'kind': 'in favour of' if kind == 'favour' else 'against'})


def dist_table(r):
    k = r.randint(3, 5); xs = sorted(r.sample(range(-3, 10), k)); ws = [r.randint(1, 6) for _ in range(k)]; T = sum(ws)
    ps = [F(w, T) for w in ws]
    return xs, ps


def expectation(r):
    xs, ps = dist_table(r); kind = r.choice(['mean', 'var'])
    E = sum(x * p for x, p in zip(xs, ps)); V = sum(x * x * p for x, p in zip(xs, ps)) - E * E
    tb = ', '.join(f'P(X = {x}) = {fr(p)}' for x, p in zip(xs, ps))
    if kind == 'mean':
        return dict(q=f'A random variable X has the distribution {tb}. E(X) =', a=fr(E), w=[fr(F(sum(xs), len(xs))), fr(sum(x * x * p for x, p in zip(xs, ps))), fr(E + F(1, 2)), fr(-E) if E else '1'],
                    ex=f'E(X) = Σ x·P(x) = ' + ' + '.join(f'({x})({fr(p)})' for x, p in zip(xs, ps)) + f' = {fr(E)}. The simple average of the x-values ({fr(F(sum(xs), len(xs)))}) ignores the probabilities. E(X) is the long-run average value of X over many repetitions, so values with higher probability count more.',
                    fast='Multiply each value by its probability and add (use a common denominator).', secs=50, d='moderate', topic=C7, k='ch15.exp', data={'tb': tb, 'kind': 'E(X) ='})
    return dict(q=f'A random variable X has the distribution {tb}. Var(X) =', a=fr(V), w=[fr(sum(x * x * p for x, p in zip(xs, ps))), fr(E * E), fr(V + E) if E else fr(V + 1), fr(F(sum((x - E) ** 2 for x in xs), len(xs)))],
                ex=f'E(X) = {fr(E)} and E(X²) = Σ x²·P(x) = {fr(sum(x * x * p for x, p in zip(xs, ps)))}. Var(X) = E(X²) − [E(X)]² = {fr(sum(x * x * p for x, p in zip(xs, ps)))} − {fr(E * E)} = {fr(V)}. Forgetting to subtract [E(X)]² gives E(X²). Variance measures how widely X spreads around its expected value and can never be negative.',
                fast='Var = E(X²) − [E(X)]²; build both sums in one pass.', secs=75, d='hard', topic=C7, k='ch15.exp', data={'tb': tb, 'kind': 'Var(X) ='})


def find_k(r):
    n = r.randint(3, 6); kind = r.choice(['kx', 'kx2'])
    xs = list(range(1, n + 1)); S = sum(xs) if kind == 'kx' else sum(x * x for x in xs); k = F(1, S)
    form = 'kx' if kind == 'kx' else 'kx²'
    return dict(q=f'A random variable X takes the values {", ".join(map(str, xs))} with P(X = x) = {form}. The value of k is:', a=fr(k), w=[fr(F(1, n)), fr(F(1, sum(x * x for x in xs) if kind == 'kx' else sum(xs))), fr(F(S)), fr(F(2, S))],
                ex=f'Probabilities of all values must add to 1: k(' + ' + '.join(str(x if kind == 'kx' else x * x) for x in xs) + f') = 1, i.e. {S}k = 1, so k = {fr(k)}. Every probability is then between 0 and 1, as required for a valid probability distribution.',
                fast=f'k = 1 ÷ (sum of the {"values" if kind == "kx" else "squares"}).', secs=25, d='core', topic=C6, k='ch15.k', data={'n': n, 'form': form})


def divisible(r):
    N = r.choice([50, 60, 75, 100, 120, 150, 200]); a, b = r.sample([2, 3, 4, 5, 6, 7, 8, 9, 11], 2)
    c = sum(1 for x in range(1, N + 1) if x % a == 0 or x % b == 0); p = F(c, N)
    l = a * b // math.gcd(a, b)
    return dict(q=f'A number is chosen at random from 1 to {N}. The probability that it is divisible by {a} or {b} is:', a=fr(p), w=[fr(F(N // a + N // b, N)), fr(F(N // l, N)), fr(1 - p), fr(F(c + 1, N))],
                ex=f'Multiples of {a}: {N // a}; multiples of {b}: {N // b}; multiples of both (of LCM {l}): {N // l}. By the addition rule, favourable = {N // a} + {N // b} − {N // l} = {c}. Probability = {c}/{N} = {fr(p)}. Not subtracting the common multiples double-counts them.',
                fast='⌊N/a⌋ + ⌊N/b⌋ − ⌊N/LCM⌋, then divide by N.', secs=40, d='moderate', topic=C4, k='ch15.div', data={'N': N, 'a': a, 'b': b})


def committee(r):
    m, w = r.randint(3, 8), r.randint(3, 8); k = r.choice([3, 4]); j = r.randint(1, min(k, w))
    if k - j > m: return None
    p = F(math.comb(w, j) * math.comb(m, k - j), math.comb(m + w, k))
    return dict(q=f'A committee of {k} is chosen at random from {m} men and {w} women. The probability that it has exactly {j} wom{"a" if j == 1 else "e"}n is:', a=fr(p),
                w=[fr(F(math.comb(w, j), math.comb(m + w, k))), fr(F(j, k)), fr(1 - p), fr(F(math.comb(w, j) * math.comb(m, k - j), math.comb(m + w, k) * 2))],
                ex=f'Total selections = {m + w}C{k} = {math.comb(m + w, k)}. Favourable = {w}C{j} × {m}C{k - j} = {math.comb(w, j)} × {math.comb(m, k - j)} = {math.comb(w, j) * math.comb(m, k - j)}. Probability = {fr(p)}. Remember to choose the men for the remaining {k - j} places as well; every committee of {k} is equally likely.',
                fast='(ways for women × ways for men) ÷ total ways — all combinations.', secs=45, d='moderate', topic=C5, k='ch15.comm', data={'m': m, 'w': w, 'k': k, 'j': j})


def sundays(r):
    leap = r.choice([True, False]); day = r.choice(['Sundays', 'Mondays', 'Fridays'])
    p = F(2, 7) if leap else F(1, 7)
    return dict(q=f'The probability that a randomly chosen {"leap" if leap else "non-leap"} year has 53 {day} is:', a=fr(p), w=[fr(F(1, 7) if leap else F(2, 7)), fr(F(53, 365 if not leap else 366)), fr(F(1, 53)), fr(F(3, 7))],
                ex=f'A {"leap" if leap else "non-leap"} year has 52 full weeks plus {2 if leap else 1} extra day{"s" if leap else ""}. ' + ('The two extra consecutive days can be any of 7 pairs (Sun–Mon, Mon–Tue, …), and 2 of these pairs include the given day.' if leap else 'The one extra day can be any of the 7 days, and only 1 of them is the given day.') + f' So the probability is {fr(p)}.',
                fast='Extra days beyond 52 weeks: 1 (ordinary) or 2 (leap); count how many of the 7 possibilities contain the day.', secs=25, d='core', topic=C1, k='ch15.sun', data={'leap': 'non-leap' if not leap else 'leap'})


def game(r):
    win, lose = r.randint(10, 300), r.randint(5, 100); fav = r.randint(1, 3)
    E = F(win * fav - lose * (6 - fav), 6)
    return dict(q=f'In a game a player throws a fair die. He wins ₹{win} if the number is {"6" if fav == 1 else "5 or 6" if fav == 2 else "4, 5 or 6"} and loses ₹{lose} otherwise. His expected gain per throw is:', a=rs(E) if E >= 0 else f'Loss of {rs(-E)}',
                w=[rs(F(win - lose, 2)) if win > lose else f'Loss of {rs(F(lose - win, 2))}', rs(F(win * fav, 6)), f'Loss of {rs(abs(E) + 5)}' if E >= 0 else rs(abs(E)), rs(abs(E) + 10)],
                ex=f'P(win) = {fav}/6 and P(lose) = {6 - fav}/6. Expected gain = {win} × {fav}/6 − {lose} × {6 - fav}/6 = ({win * fav} − {lose * (6 - fav)})/6 = ₹{num(E)}. ' + ('A positive value means the game favours the player in the long run.' if E >= 0 else 'A negative value is an expected loss for the player in the long run.'),
                fast='E = Σ (amount × probability), with losses negative.', secs=40, d='moderate', topic=C7, check=frx(abs(E)) if E >= 0 else None, k='ch15.game', data={'win': win, 'lose': lose, 'fav': fav})


BANKS = {U: [(dice, 3), (coins, 2), (cards, 3), (balls, 3), (addition, 3), (independent, 2), (conditional, 2), (odds, 2), (expectation, 3), (find_k, 2), (divisible, 2), (committee, 2), (sundays, 1), (game, 2)]}
