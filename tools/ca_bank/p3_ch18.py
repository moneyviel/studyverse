"""Paper 3 Ch 18 — Index Numbers: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch18-u01'
C1, C2, C3, C4, C5 = 'What an index number is', 'Issues in constructing an index', 'Relatives — price, quantity, value, link and chain', 'Unweighted methods', 'Weighted aggregative indices'
C6, C7, C8, C9, C10 = 'Weighted average of relatives', 'Chain-base index numbers', 'Tests of adequacy', 'Uses, limitations, deflating, shifting and splicing', 'Stock market indices'


def table(r, k=3):
    rows = []
    for name in 'ABCD'[:k]:
        p0 = r.randint(2, 40); p1 = p0 + r.randint(-3, 15); q0 = r.randint(2, 20); q1 = q0 + r.randint(-3, 8)
        if p1 <= 0 or q1 <= 0: return None
        rows.append((name, p0, q0, p1, q1))
    return rows


def show(rows, cols=('p0', 'q0', 'p1', 'q1')):
    lab = {'p0': 'p₀', 'q0': 'q₀', 'p1': 'p₁', 'q1': 'q₁'}; idx = {'p0': 1, 'q0': 2, 'p1': 3, 'q1': 4}
    return '; '.join(f'{rw[0]}: ' + ', '.join(f'{lab[c]} = {rw[idx[c]]}' for c in cols) for rw in rows)


def S(rows, a, b): return sum(rw[a] * rw[b] for rw in rows)


def weighted_index(r):
    rows = table(r)
    if not rows: return None
    kind = r.choice(['Laspeyres', 'Paasche', 'Fisher', 'Marshall-Edgeworth', 'Bowley', 'value'])
    L = F(S(rows, 3, 2), S(rows, 1, 2)) * 100; P = F(S(rows, 3, 4), S(rows, 1, 4)) * 100
    Fi = math.sqrt(L * P); ME = F(sum(rw[3] * (rw[2] + rw[4]) for rw in rows), sum(rw[1] * (rw[2] + rw[4]) for rw in rows)) * 100; B = (L + P) / 2
    V = F(S(rows, 3, 4), S(rows, 1, 2)) * 100
    vals = {'Laspeyres': float(L), 'Paasche': float(P), 'Fisher': Fi, 'Marshall-Edgeworth': float(ME), 'Bowley': float(B), 'value': float(V)}
    v = vals[kind]; cand = [x for k_, x in vals.items() if k_ != kind] + [float(F(sum(rw[3] for rw in rows), sum(rw[1] for rw in rows)) * 100), v * 1.06, v * 0.94, v + 3.5]
    others = []
    for x in cand:                     # keep distractors clearly apart (≥ 0.5) so rounding cannot blur the key
        if abs(x - v) >= 0.5 and all(abs(x - y) >= 0.5 for y in others): others.append(x)
    form = {'Laspeyres': 'Σp₁q₀/Σp₀q₀ × 100', 'Paasche': 'Σp₁q₁/Σp₀q₁ × 100', 'Fisher': '√(Laspeyres × Paasche)', 'Marshall-Edgeworth': 'Σp₁(q₀ + q₁)/Σp₀(q₀ + q₁) × 100', 'Bowley': '(Laspeyres + Paasche)/2', 'value': 'Σp₁q₁/Σp₀q₀ × 100'}[kind]
    name = f"{kind}'s price index" if kind not in ('value', 'Marshall-Edgeworth', 'Bowley') else ('the value index' if kind == 'value' else f'the {kind} price index')
    return dict(q=f'Data — {show(rows)}. {name[0].upper() + name[1:]} is about:', a=num(v, 2), w=[num(x, 2) for x in others],
                ex=f'Use {form}. Here Σp₀q₀ = {S(rows, 1, 2)}, Σp₁q₀ = {S(rows, 3, 2)}, Σp₀q₁ = {S(rows, 1, 4)}, Σp₁q₁ = {S(rows, 3, 4)}. Laspeyres = {num(L, 2)}, Paasche = {num(P, 2)}, so {name} ≈ {num(v, 2)}. Laspeyres weights by base quantities, Paasche by current quantities.',
                fast='Compute the four products Σp₀q₀, Σp₁q₀, Σp₀q₁, Σp₁q₁ once; every weighted index is built from them.', secs=90, d='hard' if kind in ('Fisher', 'Marshall-Edgeworth') else 'moderate', topic=C5,
                check=f'round({v},2)', k='ch18.windex', data={'rows': [list(rw[1:]) for rw in rows], 'kind': kind})


def simple_index(r):
    rows = table(r, r.randint(3, 4))
    if not rows: return None
    kind = r.choice(['agg', 'avg'])
    agg = F(sum(rw[3] for rw in rows), sum(rw[1] for rw in rows)) * 100; avg = sum(F(rw[3], rw[1]) * 100 for rw in rows) / len(rows)
    v = agg if kind == 'agg' else avg; o = avg if kind == 'agg' else agg
    if abs(agg - avg) < F(1, 100): return None
    return dict(q=f'Prices — {show(rows, ("p0", "p1"))}. The {"simple aggregative" if kind == "agg" else "simple arithmetic mean of price relatives"} index is about:', a=num(v, 2), w=[num(o, 2), num(v - 100, 2), num(F(sum(rw[1] for rw in rows), sum(rw[3] for rw in rows)) * 100, 2), num(v + 5, 2)],
                ex=(f'Simple aggregative index = Σp₁/Σp₀ × 100 = {sum(rw[3] for rw in rows)}/{sum(rw[1] for rw in rows)} × 100 = {num(agg, 2)}.' if kind == 'agg' else
                    f'Price relatives p₁/p₀ × 100: ' + ', '.join(num(F(rw[3], rw[1]) * 100, 2) for rw in rows) + f'. Their average = {num(avg, 2)}.') + ' The aggregative method is affected by the units in which prices are quoted; the average of relatives is not, because each relative is a pure number.',
                fast='Aggregative: add the prices; relatives: average the ratios. Do not mix them.', secs=60, d='moderate', topic=C4, check=f'round({float(v)},2)', k='ch18.simple', data={'p0': [rw[1] for rw in rows], 'p1': [rw[3] for rw in rows], 'kind': kind})


def relative(r):
    p0 = r.randint(5, 500); p1 = p0 + r.randint(-p0 // 3, p0); kind = r.choice(['price', 'reverse'])
    if p1 <= 0: return None
    v = F(p1 * 100, p0) if kind == 'price' else F(p0 * 100, p1)
    q = f'The price of an item was ₹{inr(p0)} in the base year and is ₹{inr(p1)} now. The price relative for the current year is:' if kind == 'price' else f'The price of an item was ₹{inr(p0)} in year 0 and ₹{inr(p1)} in year 1. Taking year 1 as the base, the price relative for year 0 is:'
    return dict(q=q, a=num(v, 2), w=[num(F(p0 * 100, p1) if kind == 'price' else F(p1 * 100, p0), 2), num(F((p1 - p0) * 100, p0), 2), num(p1 - p0 + 100), num(F(p1, p0), 4)],
                ex=f'Price relative = (price in the given year ÷ price in the base year) × 100 = ' + (f'{inr(p1)}/{inr(p0)} × 100 = {num(v, 2)}.' if kind == 'price' else f'{inr(p0)}/{inr(p1)} × 100 = {num(v, 2)}.') + ' The base year always goes in the denominator. A relative of 100 means no change.',
                fast='Given-year price ÷ base-year price × 100.', secs=20, d='core', topic=C3, check=f'round({float(v)},2)', k='ch18.rel', data={'p0': p0, 'p1': p1, 'kind': kind})


def fisher_p(r):
    L = r.randint(105, 160); Fi = r.randint(L - 6, L + 2)
    if Fi == L: return None
    P = F(Fi * Fi, L)
    return dict(q=f'Laspeyres\'s index is {L} and Fisher\'s ideal index is {Fi}. Paasche\'s index is about:', a=num(P, 2), w=[num(2 * Fi - L), num(F(L + Fi, 2), 2), num(math.sqrt(L * Fi), 2), num(F(L * L, Fi), 2)],
                ex=f'Fisher = √(L × P), so P = F²/L = {Fi}²/{L} = {Fi * Fi}/{L} = {num(P, 2)}. The answer 2F − L ({2 * Fi - L}) would be right only for an arithmetic mean (Bowley), not the geometric mean used by Fisher.',
                fast='Since Fisher = √(L × P), Paasche = Fisher² ÷ Laspeyres.', secs=25, d='moderate', topic=C5, check=f'round({float(P)},2)', k='ch18.fp', data={'L': L, 'Fi': Fi})


def chain(r):
    links = [r.choice([90, 95, 98, 102, 104, 105, 108, 110, 112, 115, 120, 125]) for _ in range(r.randint(3, 4))]
    v = F(100)
    for l in links: v = v * l / 100
    yrs = list(range(2021, 2021 + len(links) + 1))
    return dict(q=f'Link relatives for {", ".join(map(str, yrs[1:]))} (each on the previous year = 100) are {", ".join(map(str, links))}. With {yrs[0]} = 100, the chain index for {yrs[-1]} is about:', a=num(v, 2),
                w=[num(F(sum(links), len(links)), 2), num(100 + sum(l - 100 for l in links), 2), num(links[-1]), num(v * links[0] / 100, 2)],
                ex=f'Chain index = previous chain index × link relative/100. Starting from 100: ' + ' → '.join(num(math.prod(F(l, 100) for l in links[:i + 1]) * 100, 2) for i in range(len(links))) + f'. So {yrs[-1]} = {num(v, 2)}. Adding the percentage changes ignores compounding, because each link is measured on a different base (the previous year).',
                fast='Multiply the link relatives as decimals (1.05 × 0.98 × …) and × 100.', secs=50, d='moderate', topic=C7, check=f'round({float(v)},2)', k='ch18.chain', data={'links': links})


def shift(r):
    old = [r.randint(80, 250) for _ in range(5)]; yrs = list(range(2019, 2024)); b = r.randrange(5); t = r.choice([i for i in range(5) if i != b])
    v = F(old[t] * 100, old[b])
    return dict(q=f'Index numbers (base 2018 = 100) for {", ".join(map(str, yrs))} are {", ".join(map(str, old))}. Shifting the base to {yrs[b]} = 100, the index for {yrs[t]} becomes about:', a=num(v, 2),
                w=[num(old[t] - old[b] + 100) if old[t] - old[b] + 100 > 0 else num(v - 10, 2), num(F(old[b] * 100, old[t]), 2), num(old[t]), num(v + 10, 2)],
                ex=f'Base shifting: new index = old index ÷ old index of the new base year × 100 = {old[t]}/{old[b]} × 100 = {num(v, 2)}. Subtracting the difference ({old[t] - old[b] + 100}) is wrong because index numbers are ratios, not differences.',
                fast='Divide every index by the new base year\'s index and × 100.', secs=30, d='core', topic=C9, check=f'round({float(v)},2)', k='ch18.shift', data={'old': old, 'b': b, 't': t})


def deflate(r):
    W = r.choice(range(15000, 120001, 500)); cpi = r.randint(110, 260); kind = r.choice(['real', 'pp'])
    if kind == 'real':
        v = F(W * 100, cpi)
        return dict(q=f'A worker\'s monthly wage is ₹{inr(W)} and the consumer price index is {cpi} (base = 100). The real wage is about:', a=rs(round(v, 2)), w=[rs(round(F(W * cpi, 100), 2)), rs(W - (cpi - 100) * 100), rs(W), rs(round(F(W * 100, cpi + 10), 2))],
                    ex=f'Real wage = money wage ÷ CPI × 100 = {inr(W)}/{cpi} × 100 = ₹{numf(v)}. This "deflating" removes the effect of price rise, showing what the wage buys at base-year prices. Multiplying by the CPI goes the wrong way.',
                    fast='Money wage × 100 ÷ CPI.', secs=25, d='core', topic=C9, check=f'round({float(v)},2)', k='ch18.defl', data={'W': W, 'cpi': cpi, 'kind': kind})
    v = F(100, cpi)
    return dict(q=f'If the consumer price index is {cpi} (base = 100), the purchasing power of a rupee compared with the base year is about:', a='₹' + numf(v, 2), w=['₹' + numf(F(cpi, 100), 2), '₹' + numf(v + F(1, 10), 2), '₹1.00', '₹' + numf(v / 2, 2)],
                ex=f'Purchasing power of money = 100 ÷ price index = 100/{cpi} = {numf(v, 4)}, i.e. a rupee now buys what ₹{numf(v, 2)} bought in the base year. It moves opposite to prices: when prices rise, each rupee buys less than before.',
                fast='Purchasing power of a rupee = 100 ÷ CPI.', secs=20, d='core', topic=C9, check=f'round({float(v)},2)', k='ch18.defl', data={'cpi': cpi, 'kind': kind})


def wavg_rel(r):
    k = r.randint(3, 4); R = [r.randint(90, 180) for _ in range(k)]; W = [r.randint(1, 10) for _ in range(k)]
    v = F(sum(a * b for a, b in zip(R, W)), sum(W))
    grp = ['Food', 'Clothing', 'Fuel', 'Rent'][:k]
    return dict(q=f'Group indices and weights: ' + ', '.join(f'{g} {x} (weight {w})' for g, x, w in zip(grp, R, W)) + '. The weighted index is about:', a=num(v, 2), w=[num(F(sum(R), k), 2), num(F(sum(a * b for a, b in zip(R, W)), k), 2), num(v + 3, 2), num(F(sum(R) * sum(W), k * sum(W)) - 2, 2)],
                ex=f'Weighted average of relatives = ΣRW/ΣW = ({" + ".join(f"{x}×{w}" for x, w in zip(R, W))})/{sum(W)} = {sum(a * b for a, b in zip(R, W))}/{sum(W)} = {num(v, 2)}. This is how a consumer price index combines group indices. Dividing by the number of groups ignores the weights.',
                fast='Multiply each index by its weight, add, divide by the total weight.', secs=40, d='moderate', topic=C6, check=f'round({float(v)},2)', k='ch18.wavg', data={'R': R, 'W': W})


def qty_index(r):
    rows = table(r)
    if not rows: return None
    v = F(S(rows, 4, 1), S(rows, 2, 1)) * 100
    return dict(q=f'Data — {show(rows)}. Laspeyres\'s QUANTITY index (Σq₁p₀/Σq₀p₀ × 100) is about:', a=num(v, 2), w=[num(F(S(rows, 3, 2), S(rows, 1, 2)) * 100, 2), num(F(S(rows, 4, 3), S(rows, 2, 3)) * 100, 2), num(F(sum(rw[4] for rw in rows), sum(rw[2] for rw in rows)) * 100, 2), num(v + 4, 2)],
                ex=f'A quantity index keeps prices fixed and lets quantities change. Laspeyres uses base-year prices as weights: Σq₁p₀ = {S(rows, 4, 1)} and Σq₀p₀ = {S(rows, 2, 1)}, so the index = {num(v, 2)}. Swapping the roles of p and q gives the price index instead.',
                fast='Same layout as the price index, with p and q interchanged.', secs=60, d='moderate', topic=C3, check=f'round({float(v)},2)', k='ch18.qty', data={'rows': [list(rw[1:]) for rw in rows]})


def stock(r):
    a = r.randint(15000, 85000); chg = r.choice([-1, 1]) * r.randint(50, 3000); b = a + chg
    v = F(chg * 100, a)
    return dict(q=f'A stock market index closed at {inr(a)} yesterday and at {inr(b)} today. The percentage change is about:', a=pct(v, 2), w=[pct(F(chg * 100, b), 2) if abs(F(chg * 100, b) - v) > F(1, 100) else pct(v * 2, 2), pct(-v, 2), pct(F(chg, 100), 2), pct(v * 10, 2)],
                ex=f'Change = {inr(b)} − {inr(a)} = {chg:+} points. Percentage change = change ÷ previous close × 100 = {chg}/{inr(a)} × 100 ≈ {num(v, 2)}%. Index points are not percentages; always divide by the starting level, i.e. the previous close.',
                fast='(New − old) ÷ old × 100.', secs=25, d='core', topic=C10, check=f'round({float(v)},2)', k='ch18.stock', data={'a': a, 'b': b})


FACTS = [
    ('Which index number satisfies both the time reversal test and the factor reversal test?', "Fisher's ideal index", ["Laspeyres's index", "Paasche's index", 'Simple aggregative index'], C8, "Fisher's index, the geometric mean of Laspeyres and Paasche, is called 'ideal' because it satisfies both the time reversal test and the factor reversal test."),
    ('The time reversal test requires that (P₀₁ = index for year 1 on base 0, P₁₀ = index for year 0 on base 1):', 'P₀₁ × P₁₀ = 1', ['P₀₁ + P₁₀ = 1', 'P₀₁ × Q₀₁ = V₀₁', 'P₀₁ = P₁₀'], C8, 'If the time subscripts are interchanged, the new index should be the reciprocal of the old one, so their product (as ratios) is 1.'),
    ('The factor reversal test requires that the product of the price index and the quantity index equals the:', 'Value index', ['Price relative', 'Chain index', 'Base index'], C8, 'Interchanging p and q in the formula gives the quantity index; price index × quantity index should equal the value ratio Σp₁q₁/Σp₀q₀.'),
    ('The index number commonly used to deflate money wages into real wages is the:', 'Consumer price index', ['Wholesale price index', 'Stock market index', 'Quantity index'], C9, 'Real wage = money wage ÷ consumer price index × 100, because the CPI measures the change in the cost of living of wage earners.'),
]


def fact(r):
    stem, ans, ws, topic, why = r.choice(FACTS)
    return dict(q=stem, a=ans, w=ws, ex=f'{why} So the correct answer is "{ans}". The other options are real terms from this chapter, so read the question\'s key words carefully before choosing.',
                fast='Recall the definition keyword; eliminate options that describe a different test or index.', secs=20, d='core', topic=topic, k='ch18.fact', data={'_t': 0})


BANKS = {U: [(weighted_index, 6), (simple_index, 3), (relative, 2), (fisher_p, 2), (chain, 2), (shift, 2), (deflate, 3), (wavg_rel, 2), (qty_index, 2), (stock, 2), (fact, 3)]}
