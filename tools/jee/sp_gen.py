"""Practice generators — Mathematics Unit 13: Statistics and Probability. Each item is built from planted data;
check() re-solves it independently — unknown data values by scanning every candidate that meets the stated mean
and variance, probabilities by listing the whole sample space, and Bayes items by simulating the two-stage
experiment as exact weighted outcomes."""
import math, itertools, re
from fractions import Fraction as F
from math import comb
from common import mcq, fr
def need(x):
    if not x: raise AssertionError('retry')
def mean(xs): return F(sum(xs), len(xs))
def var(xs): m = mean(xs); return sum((F(x) - m) ** 2 for x in xs) / len(xs)
def lst(xs): return ', '.join(str(x) for x in xs)
def wrong4(rng, v, extra=()):
    c = [v + 1, v - 1 if v > 1 else v + 2, v * 2, v / 2 if v else F(1, 2), v + F(1, 2)] + list(extra); rng.shuffle(c); return [fr(x) for x in c]

def wp(rng, v, extra=()):   # distractors that are still valid probabilities
    d = v.denominator; c = list(extra) + [1 - v, v * 2, v / 2, v + F(1, d), v - F(1, d), (v + 1) / 2, v * F(3, 4)]
    out = []
    for x in c:
        x = F(x)
        if 0 < x < 1 and x != v and fr(x) not in out: out.append(fr(x))
    rng.shuffle(out); return out
def g_stat(rng):
    t = rng.choice(['s_ab', 's_fix', 's_comb', 's_md', 's_ap', 's_lin', 's_grp'])
    if t == 's_ab':
        base = [rng.randint(1, 20) for _ in range(rng.randint(4, 6))]; a, b = rng.randint(1, 20), rng.randint(1, 20); need(a > b)
        xs = base + [a, b]; m, v = mean(xs), var(xs); ask = rng.choice(['ab', 'a2b2', 'diff'])
        val = {'ab': a * b, 'a2b2': a * a + b * b, 'diff': a - b}[ask]; lab = {'ab': 'ab', 'a2b2': 'a^{2} + b^{2}', 'diff': 'a − b'}[ask]
        return dict(q=f'The mean and variance of the observations {lst(base)}, a, b (a > b) are {fr(m)} and {fr(v)}. Then {lab} = ____.', o=None, a=val,
                    sol=[f'Sum condition: a + b = {fr(m * len(xs))} − {sum(base)} = {a + b}.', f'Σx^{{2}} = n(σ^{{2}} + μ^{{2}}) gives a^{{2}} + b^{{2}} = {a * a + b * b}, so a = {a}, b = {b} → {val}.'], p=dict(t=t, base=base, m=m, v=v, ask=ask, n=len(xs)))
    if t == 's_fix':
        n = rng.choice([10, 20, 25, 50]); xs = [rng.randint(2, 20) for _ in range(n)]; i = rng.randrange(n); right = xs[i]; wrong = right + rng.choice([-4, -3, -2, 2, 3, 5])
        bad = xs[:]; bad[i] = wrong; mb, vb = mean(bad), var(bad); vr = var(xs)
        o, an = mcq(rng, fr(vr), wrong4(rng, vr, [vb]))
        return dict(q=f'The mean and variance of {n} observations were found to be {fr(mb)} and {fr(vb)}. Later one observation recorded as {wrong} was found to be {right}. The correct variance is', o=o, a=an,
                    sol=['Correct Σx and Σx^{2} (from n(σ^{2} + μ^{2})) by removing the wrong value and adding the right one.', f'Corrected variance = {fr(vr)}.'], p=dict(t=t, n=n, m=mb, v=vb, wrong=wrong, right=right))
    if t == 's_comb':
        n1, n2 = rng.randint(2, 8), rng.randint(2, 8); m1, m2 = rng.randint(0, 10), rng.randint(0, 10); v1, v2 = rng.randint(1, 20), rng.randint(1, 20)
        M = F(n1 * m1 + n2 * m2, n1 + n2); V = F(n1 * (v1 + m1 * m1) + n2 * (v2 + m2 * m2), n1 + n2) - M * M
        o, an = mcq(rng, fr(V), wrong4(rng, V, [F(n1 * v1 + n2 * v2, n1 + n2)]))
        return dict(q=f'One set of {n1} observations has mean {m1} and variance {v1}; another set of {n2} observations has mean {m2} and variance {v2}. The variance of all {n1 + n2} observations together is', o=o, a=an,
                    sol=['Add Σx and Σx^{2} = n(σ^{2} + μ^{2}) of both sets.', f'Mean {fr(M)}; variance = \\f{{Σx^{{2}}}}{{N}} − mean^{{2}} = {fr(V)}.'], p=dict(t=t, s=(n1, m1, v1, n2, m2, v2)))
    if t == 's_md':
        xs = sorted(rng.randint(1, 30) for _ in range(rng.choice([5, 6, 7, 8]))); about = rng.choice(['mean', 'median'])
        c = mean(xs) if about == 'mean' else (F(xs[len(xs) // 2]) if len(xs) % 2 else F(xs[len(xs) // 2 - 1] + xs[len(xs) // 2], 2)); md = sum(abs(F(x) - c) for x in xs) / len(xs)
        o, an = mcq(rng, fr(md), wrong4(rng, md, [sum(abs(F(x) - (mean(xs) if about == 'median' else c + 1)) for x in xs) / len(xs)]))
        return dict(q=f'The mean deviation about the {about} of {lst(xs)} is', o=o, a=an, sol=[f'{about.capitalize()} = {fr(c)}.', f'\\f{{Σ|x − {fr(c)}|}}{{{len(xs)}}} = {fr(md)}.'], p=dict(t=t, xs=xs, about=about))
    if t == 's_ap':
        a, d, n = rng.randint(1, 20), rng.randint(2, 15), rng.randint(5, 40); xs = [a + d * i for i in range(n)]; v = var(xs); need(v.denominator == 1)
        return dict(q=f'The variance of the numbers {a}, {a + d}, {a + 2 * d}, …, {xs[-1]} is ____.', o=None, a=int(v), sol=[f'An A.P. with d = {d}, n = {n}.', f'Variance = \\f{{d^{{2}}(n^{{2}} − 1)}}{{12}} = {int(v)}.'], p=dict(t=t, a=a, d=d, n=n))
    if t == 's_lin':
        N = rng.randint(5, 25); a = rng.choice([2, 3, 4, 5, -2, -3]); b = rng.randint(-20, 30); X = list(range(1, N + 1)); Y = [a * x + b for x in X]
        mY, vY = mean(Y), var(Y); need(mY.denominator == 1 and vY.denominator == 1)
        mA = mean([abs(a) * x + b for x in X]); need(mA.denominator == 1)
        return dict(q=f'For X = {{1, 2, …, {N}}} and Y = {{ax + b : x ∈ X}} with a > 0, the mean and variance of Y are {mA} and {vY}. Then a + b = ____.', o=None, a=abs(a) + b,
                    sol=[f'X has mean {fr(mean(X))} and variance \\f{{{N}^{{2}} − 1}}{{12}} = {fr(var(X))}.', f'a^{{2}}·{fr(var(X))} = {vY} → a = {abs(a)}; then b from the mean: a + b = {abs(a) + b}.'], p=dict(t=t, N=N, m=mean([abs(a) * x + b for x in X]), v=vY))
    st, wd = rng.randint(1, 5) * 5, rng.choice([5, 10]); mids = [st + wd * i for i in range(4)]; k = rng.randint(1, 15); fs = [rng.randint(1, 10), 0, rng.randint(1, 10), rng.randint(1, 10)]; j = rng.randrange(4); fs[j] = k
    m = F(sum(x * f for x, f in zip(mids, fs)), sum(fs)); need(m.denominator <= 20 and m != mids[j])
    return dict(q=f'Values {lst(mids)} occur with frequencies {lst(["k" if i == j else f for i, f in enumerate(fs)])}. If the mean is {fr(m)}, then k = ____.', o=None, a=k,
                sol=['Mean = \\f{Σfx}{Σf}; it is linear in k after clearing the denominator.', f'Solving gives k = {k}.'], p=dict(t='s_grp', mids=mids, fs=fs, j=j, m=m))

def g_prob(rng):
    t = rng.choice(['p_dice', 'p_quad', 'p_comm', 'p_div', 'p_inc', 'p_atl'])
    if t == 'p_dice':
        n = rng.choice([2, 3]); s = rng.randint(n + 1, 6 * n - 1); kind = rng.choice(['=', '≤', '≥'])
        cnt = sum(1 for r in itertools.product(range(1, 7), repeat=n) if (sum(r) == s if kind == '=' else sum(r) <= s if kind == '≤' else sum(r) >= s)); v = F(cnt, 6 ** n); need(0 < v < 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [1 - v]))
        return dict(q=f'{n} fair dice are thrown. The probability that the sum is {kind} {s} is'.replace('is = ', 'is exactly '), o=o, a=an, sol=[f'{6 ** n} equally likely outcomes; count those with sum {kind} {s}: {cnt}.', f'P = {fr(v)}.'], p=dict(t=t, n=n, s=s, kind=kind))
    if t == 'p_quad':
        N = rng.choice([3, 4, 5, 6]); kind = rng.choice(['real', 'equal', 'none'])
        f = {'real': lambda a, b, c: b * b >= 4 * a * c, 'equal': lambda a, b, c: b * b == 4 * a * c, 'none': lambda a, b, c: b * b < 4 * a * c}[kind]
        cnt = sum(1 for a, b, c in itertools.product(range(1, N + 1), repeat=3) if f(a, b, c)); v = F(cnt, N ** 3); need(0 < v < 1)
        txt = {'real': 'has real roots', 'equal': 'has equal roots', 'none': 'has no real roots'}[kind]
        return dict(q=f'a, b, c are chosen independently from {{1, 2, …, {N}}}. If the probability that ax^{{2}} + bx + c = 0 {txt} is \\f{{m}}{{n}} in lowest terms, then m + n = ____.', o=None, a=v.numerator + v.denominator,
                    sol=['Compare b^{2} with 4ac for every triple.', f'{cnt} of {N ** 3} triples → {fr(v)} → {v.numerator + v.denominator}.'], p=dict(t=t, N=N, kind=kind))
    if t == 'p_comm':
        A, B = rng.randint(3, 7), rng.randint(3, 7); k = rng.randint(3, min(6, A + B - 1)); amin = rng.randint(1, min(A, k) - 1 if min(A, k) > 1 else 1)
        cnt = sum(comb(A, i) * comb(B, k - i) for i in range(amin, min(A, k) + 1)); v = F(cnt, comb(A + B, k)); need(0 < v < 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [1 - v]))
        return dict(q=f'A committee of {k} is chosen at random from {A} women and {B} men. The probability that it has at least {amin} wom{"a" if amin == 1 else "e"}n is', o=o, a=an,
                    sol=[f'Total C({A + B}, {k}) = {comb(A + B, k)}.', f'Favourable Σ_{{i ≥ {amin}}} C({A}, i)C({B}, {k} − i) = {cnt} → {fr(v)}.'], p=dict(t=t, A=A, B=B, k=k, amin=amin))
    if t == 'p_div':
        N = rng.randint(10, 60); d = rng.choice([2, 3, 4, 5, 6]); v = F(sum(1 for a, b in itertools.combinations(range(1, N + 1), 2) if a * b % d == 0), comb(N, 2)); need(0 < v < 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [1 - v]))
        return dict(q=f'Two distinct numbers are chosen at random from 1, 2, …, {N}. The probability that their product is divisible by {d} is', o=o, a=an,
                    sol=[f'Count the C({N}, 2) = {comb(N, 2)} pairs whose product is a multiple of {d}.', f'P = {fr(v)}.'], p=dict(t=t, N=N, d=d))
    if t == 'p_inc':
        n, f = rng.choice([(3, 6), (3, 8), (4, 6), (2, 6), (3, 4), (4, 8)]); kind = rng.choice(['strictly increasing', 'non-decreasing'])
        cnt = comb(f, n) if kind[0] == 's' else comb(f + n - 1, n); v = F(cnt, f ** n)
        o, an = mcq(rng, fr(v), wp(rng, v, [F(comb(f, n), f ** n) if kind[0] == 'n' else F(comb(f + n - 1, n), f ** n)]))
        return dict(q=f'A fair {f}-faced die is rolled {n} times. The probability that the results are {kind} is', o=o, a=an,
                    sol=['A ' + kind + ' sequence is fixed by which values appear' + (' (all different).' if kind[0] == 's' else ' (repeats allowed).'), f'{cnt} of {f ** n} → {fr(v)}.'], p=dict(t=t, n=n, f=f, kind=kind))
    r, b, k = rng.randint(2, 7), rng.randint(2, 7), rng.randint(2, 4); need(k <= r + b - 1); v = 1 - F(comb(b, k), comb(r + b, k))
    o, an = mcq(rng, fr(v), wp(rng, v, [F(comb(b, k), comb(r + b, k))]))
    return dict(q=f'{k} balls are drawn together from a bag of {r} red and {b} blue balls. The probability that at least one is red is', o=o, a=an,
                sol=['Complement: all blue.', f'1 − \\f{{C({b}, {k})}}{{C({r + b}, {k})}} = {fr(v)}.'], p=dict(t='p_atl', r=r, b=b, k=k))

def g_dist(rng):
    t = rng.choice(['d_bin', 'd_hyp', 'd_k', 'd_ev', 'd_binmv'])
    if t == 'd_bin':
        n = rng.randint(3, 8); p = rng.choice([F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(2, 3), F(1, 10)]); k = rng.randint(0, n); kind = rng.choice(['=', '≥', '≤'])
        rng_ = [k] if kind == '=' else (range(k, n + 1) if kind == '≥' else range(0, k + 1)); v = sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in rng_); need(0 < v < 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [1 - v]))
        return dict(q=f'A trial succeeds with probability {fr(p)}. In {n} independent trials, P(number of successes {kind} {k}) is', o=o, a=an,
                    sol=['Binomial: P(X = i) = C(n, i)p^{i}(1 − p)^{n − i}.', f'Adding the needed terms gives {fr(v)}.'], p=dict(t=t, n=n, P=p, k=k, kind=kind))
    if t == 'd_hyp':
        N = rng.randint(6, 12); D = rng.randint(2, N - 3); n = rng.randint(2, min(5, N - 1)); items = [1] * D + [0] * (N - D)
        X = [sum(c) for c in itertools.combinations(items, n)]; m, v = mean(X), var(X); ask = rng.choice(['mean', 'variance'])
        val = m if ask == 'mean' else v; o, an = mcq(rng, fr(val), wrong4(rng, val, [m if ask == 'variance' else v]))
        return dict(q=f'A sample of {n} is drawn at random from {N} items of which {D} are defective. If X is the number of defectives in the sample, the {ask} of X is', o=o, a=an,
                    sol=[f'Hypergeometric: mean n·\\f{{D}}{{N}} = {fr(m)}; variance n·\\f{{D}}{{N}}·\\f{{N − D}}{{N}}·\\f{{N − n}}{{N − 1}} = {fr(v)}.', f'{ask.capitalize()} = {fr(val)}.'], p=dict(t=t, N=N, D=D, n=n, ask=ask))
    if t == 'd_k':
        cs = [rng.randint(0, 4) for _ in range(rng.randint(4, 6))]; need(sum(cs) > 0); k = F(1, sum(cs)); lo = rng.randrange(len(cs)); hi = rng.randrange(lo, len(cs))
        v = sum(cs[lo:hi + 1]) * k; need(0 < v < 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [k]))
        return dict(q=f'X takes values {lst(range(len(cs)))} with P(X = x) = {lst([f"{c}k" if c > 1 else ("k" if c == 1 else "0") for c in cs])}. Then P({lo} ≤ X ≤ {hi}) is', o=o, a=an,
                    sol=[f'Total {sum(cs)}k = 1 → k = {fr(k)}.', f'P = {sum(cs[lo:hi + 1])}k = {fr(v)}.'], p=dict(t=t, cs=cs, lo=lo, hi=hi))
    if t == 'd_ev':
        xs = sorted(rng.sample(range(-3, 8), rng.randint(3, 4))); ws = [rng.randint(1, 5) for _ in xs]; tot = sum(ws); ps = [F(w, tot) for w in ws]
        m = sum(x * p for x, p in zip(xs, ps)); v = sum(x * x * p for x, p in zip(xs, ps)) - m * m; ask = rng.choice(['mean', 'variance'])
        val = m if ask == 'mean' else v; o, an = mcq(rng, fr(val), wrong4(rng, val, [m if ask == 'variance' else v]))
        return dict(q=f'X takes values {lst(xs)} with probabilities {lst([fr(p) for p in ps])}. The {ask} of X is', o=o, a=an,
                    sol=['E(X) = Σxp, Var = Σx^{2}p − (E X)^{2}.', f'E(X) = {fr(m)}, Var = {fr(v)}.'], p=dict(t=t, xs=xs, ps=ps, ask=ask))
    n = rng.randint(4, 40); p = rng.choice([F(1, 2), F(1, 4), F(1, 5), F(3, 4), F(2, 5)]); m, v = n * p, n * p * (1 - p); need(m.denominator == 1 and v.denominator <= 4)
    return dict(q=f'A binomial variable X has mean {fr(m)} and variance {fr(v)}. Then the number of trials n = ____.', o=None, a=n,
                sol=['np = mean, np(1 − p) = variance → 1 − p = \\f{variance}{mean}.', f'p = {fr(p)} → n = {n}.'], p=dict(t='d_binmv', m=m, v=v))

def g_cond(rng):
    t = rng.choice(['c_bags', 'c_transfer', 'c_coin', 'c_total', 'c_test'])
    if t == 'c_bags':
        bags = [(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(3)]; pri = rng.choice([(1, 1, 1), (1, 2, 1), (2, 1, 1), (1, 1, 2)]); j = rng.randrange(3); col = rng.choice(['white', 'black'])
        lik = [F(w if col == 'white' else b, w + b) for w, b in bags]; post = F(pri[j]) * lik[j] / sum(F(p) * l for p, l in zip(pri, lik))
        o, an = mcq(rng, fr(post), wp(rng, post, [lik[j]]))
        pt = 'equally likely' if pri == (1, 1, 1) else f'chosen with probabilities {lst([fr(F(x, sum(pri))) for x in pri])}'
        return dict(q=f'Bags I, II, III contain {bags[0][0]} white & {bags[0][1]} black, {bags[1][0]} white & {bags[1][1]} black, {bags[2][0]} white & {bags[2][1]} black balls; a bag is {pt}. A ball drawn is {col}. The probability it came from bag {"I" * (j + 1) if j < 2 else "III"} is', o=o, a=an,
                    sol=['Bayes: P(bag | colour) = \\f{P(bag)P(colour | bag)}{Σ P(bag)P(colour | bag)}.', f'= {fr(post)}.'], p=dict(t=t, bags=bags, pri=pri, j=j, col=col))
    if t == 'c_transfer':
        w1, b1, w2, b2 = [rng.randint(1, 9) for _ in range(4)]
        v = F(w1, w1 + b1) * F(w2 + 1, w2 + b2 + 1) + F(b1, w1 + b1) * F(w2, w2 + b2 + 1)
        o, an = mcq(rng, fr(v), wp(rng, v, [F(w2, w2 + b2)]))
        return dict(q=f'Bag A has {w1} white and {b1} black balls, bag B has {w2} white and {b2} black. One ball is moved at random from A to B, then a ball is drawn from B. The probability that it is white is', o=o, a=an,
                    sol=['Split on the colour moved.', f'\\f{{{w1}}}{{{w1 + b1}}}·\\f{{{w2 + 1}}}{{{w2 + b2 + 1}}} + \\f{{{b1}}}{{{w1 + b1}}}·\\f{{{w2}}}{{{w2 + b2 + 1}}} = {fr(v)}.'], p=dict(t=t, s=(w1, b1, w2, b2)))
    if t == 'c_coin':
        N, h = rng.randint(2, 20), rng.randint(1, 4); like_f = F(1, 2 ** h); post = F(N) * like_f / (N * like_f + 1)
        o, an = mcq(rng, fr(post), wp(rng, post, [1 - post]))
        return dict(q=f'A bag has {N} fair coins and 1 two-headed coin. A coin is chosen at random and tossed {h} time{"s" if h > 1 else ""}, showing heads every time. The probability that it is a fair coin is', o=o, a=an,
                    sol=[f'P(all heads) = \\f{{{N}}}{{{N + 1}}}·\\f{{1}}{{{2 ** h}}} + \\f{{1}}{{{N + 1}}}.', f'P(fair | heads) = {fr(post)}.'], p=dict(t=t, N=N, h=h))
    if t == 'c_total':
        ps = [F(rng.randint(1, 9), 10) for _ in range(2)]; need(ps[0] + ps[1] <= 1); ps.append(1 - ps[0] - ps[1]); need(ps[2] > 0); qs = [F(rng.randint(1, 9), 10) for _ in range(3)]
        v = sum(p * q for p, q in zip(ps, qs)); o, an = mcq(rng, fr(v), wp(rng, v, [sum(qs) / 3]))
        return dict(q=f'Machines A, B, C make {lst([fr(p * 100) + "%" for p in ps])} of the output; their items pass inspection with probabilities {lst([fr(q) for q in qs])}. The probability that a random item passes is', o=o, a=an,
                    sol=['Total probability: Σ P(machine)·P(pass | machine).', f'= {fr(v)}.'], p=dict(t=t, ps=ps, qs=qs))
    prev = F(rng.randint(1, 20), 100); sens = F(rng.randint(80, 99), 100); fpos = F(rng.randint(1, 15), 100); post = prev * sens / (prev * sens + (1 - prev) * fpos)
    o, an = mcq(rng, fr(post), wp(rng, post, [sens]))
    return dict(q=f'{fr(prev * 100)}% of a population has a condition. A test detects it with probability {fr(sens)} and gives a false positive with probability {fr(fpos)}. If a person tests positive, the probability they have the condition is', o=o, a=an,
                sol=['Bayes with the two groups (has it / does not).', f'\\f{{{fr(prev)}·{fr(sens)}}}{{{fr(prev)}·{fr(sens)} + {fr(1 - prev)}·{fr(fpos)}}} = {fr(post)}.'], p=dict(t='c_test', prev=prev, sens=sens, fpos=fpos))

def robust(gf):
    def w(rng):
        for _ in range(800):
            try: return gf(rng)
            except (AssertionError, ZeroDivisionError, ValueError, KeyError, IndexError, TypeError): continue
        raise RuntimeError('generator kept failing')
    return w
GEN = {k: robust(v) for k, v in dict(stat=g_stat, prob=g_prob, dist=g_dist, cond=g_cond).items()}
def _m(x): return re.sub(r'(?<![\w{])-(?=\d)', '−', x) if isinstance(x, str) else x
def finish(it):
    it['q'] = _m(it['q']); it['sol'] = [_m(x) for x in it['sol']]
    if it.get('o'): it['o'] = [_m(x) for x in it['o']]
    return it

# ---------------- independent checks
def tofr(s):
    s = s.replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-')
    v = F(s.replace('\\f{', '').replace('}{', '/').replace('}', '')) if '\\f' in s else F(s); return -v if neg else v
def check(it):
    p = it['p']; t = p['t']; R = it['o'][it['a']] if it.get('o') else it['a']; V = tofr(R) if isinstance(R, str) else R
    if t == 's_ab':
        hits = set()
        for a in range(-5, 60):
            for b in range(-5, a):
                xs = p['base'] + [a, b]
                if mean(xs) == p['m'] and var(xs) == p['v']: hits.add({'ab': a * b, 'a2b2': a * a + b * b, 'diff': a - b}[p['ask']])
        return hits == {V}
    if t == 's_fix':   # rebuild a data set with the reported mean/variance, swap the value, recompute directly
        n, m, v = p['n'], p['m'], p['v']; S, Q = m * n, (v + m * m) * n; S2, Q2 = S - p['wrong'] + p['right'], Q - p['wrong'] ** 2 + p['right'] ** 2
        return V == Q2 / n - (S2 / n) ** 2
    if t == 's_comb':
        n1, m1, v1, n2, m2, v2 = p['s']
        A = [m1 + math.sqrt(v1) * s for s in [1, -1] * (n1 // 2)] + ([m1] if n1 % 2 else []); B = [m2 + math.sqrt(v2) * s for s in [1, -1] * (n2 // 2)] + ([m2] if n2 % 2 else [])
        # odd sizes: rescale the spread so the variance still matches
        def fix(arr, m, v, n):
            if n % 2 == 0: return arr
            k = math.sqrt(v * n / (n - 1)); return [m + k * s for s in [1, -1] * (n // 2)] + [m]
        A, B = fix(A, m1, v1, n1), fix(B, m2, v2, n2); allv = A + B; M = sum(allv) / len(allv); return abs(float(V) - sum((x - M) ** 2 for x in allv) / len(allv)) < 1e-9
    if t == 's_md':
        xs = p['xs']; c = sorted(xs)[(len(xs) - 1) // 2] if p['about'] == 'median' and len(xs) % 2 else None
        if p['about'] == 'median':   # the median minimises the mean deviation: check V equals that minimum over a fine grid
            best = min(sum(abs(F(x) - F(k, 2)) for x in xs) / len(xs) for k in range(0, 70)); return V == best
        return V == sum(abs(F(x) * len(xs) - sum(xs)) for x in xs) / len(xs) ** 2
    if t == 's_ap':
        xs = list(range(p['a'], p['a'] + p['d'] * p['n'], p['d'])); m = sum(xs) / len(xs); return abs(V - sum((x - m) ** 2 for x in xs) / len(xs)) < 1e-6
    if t == 's_lin':
        X = list(range(1, p['N'] + 1)); hits = set()
        for a in range(1, 10):
            for b in range(-60, 80):
                Y = [a * x + b for x in X]
                if mean(Y) == p['m'] and var(Y) == p['v']: hits.add(a + b)
        return hits == {V}
    if t == 's_grp':
        hits = [k for k in range(0, 100) if (lambda fs: sum(fs) and F(sum(x * f for x, f in zip(p['mids'], fs)), sum(fs)) == p['m'])([k if i == p['j'] else f for i, f in enumerate(p['fs'])])]
        return hits == [V]
    if t == 'p_dice':
        n, s, kd = p['n'], p['s'], p['kind']; tot = 0
        for r in itertools.product(range(1, 7), repeat=n):
            tot += (sum(r) == s) if kd == '=' else (sum(r) <= s) if kd == '≤' else (sum(r) >= s)
        return V == F(tot, 6 ** n)
    if t == 'p_quad':
        N = p['N']; cnt = 0
        for a, b, c in itertools.product(range(1, N + 1), repeat=3):
            d = b * b - 4 * a * c; cnt += (d >= 0) if p['kind'] == 'real' else (d == 0) if p['kind'] == 'equal' else (d < 0)
        v = F(cnt, N ** 3); return V == v.numerator + v.denominator
    if t == 'p_comm':
        people = ['W'] * p['A'] + ['M'] * p['B']; cs = list(itertools.combinations(range(len(people)), p['k'])); return V == F(sum(1 for c in cs if sum(people[i] == 'W' for i in c) >= p['amin']), len(cs))
    if t == 'p_div':
        N, d = p['N'], p['d']; return V == F(sum(1 for a in range(1, N + 1) for b in range(1, N + 1) if a != b and (a * b) % d == 0), N * (N - 1))
    if t == 'p_inc':
        n, f = p['n'], p['f']; ok = (lambda r: all(x < y for x, y in zip(r, r[1:]))) if p['kind'][0] == 's' else (lambda r: all(x <= y for x, y in zip(r, r[1:])))
        return V == F(sum(1 for r in itertools.product(range(f), repeat=n) if ok(r)), f ** n)
    if t == 'p_atl':
        balls = ['R'] * p['r'] + ['B'] * p['b']; cs = list(itertools.combinations(range(len(balls)), p['k'])); return V == F(sum(1 for c in cs if any(balls[i] == 'R' for i in c)), len(cs))
    if t == 'd_bin':   # enumerate all 2^n success patterns with their weights
        n, P_, k, kd = p['n'], p['P'], p['k'], p['kind']; tot = F(0)
        for s in itertools.product((0, 1), repeat=n):
            c = sum(s)
            if (c == k) if kd == '=' else (c >= k) if kd == '≥' else (c <= k): tot += P_ ** c * (1 - P_) ** (n - c)
        return V == tot
    if t == 'd_hyp':
        items = [1] * p['D'] + [0] * (p['N'] - p['D']); X = [sum(items[i] for i in c) for c in itertools.permutations(range(p['N']), p['n'])]
        return V == (mean(X) if p['ask'] == 'mean' else var(X))
    if t == 'd_k':
        cs = p['cs']; k = F(1, sum(cs)); assert sum(c * k for c in cs) == 1; return V == sum(c * k for c in cs[p['lo']:p['hi'] + 1])
    if t == 'd_ev':
        xs, ps = p['xs'], p['ps']; den = math.lcm(*[q.denominator for q in ps]); pop = sum([[x] * int(q * den) for x, q in zip(xs, ps)], [])   # as an equally weighted population
        return V == (mean(pop) if p['ask'] == 'mean' else var(pop))
    if t == 'd_binmv':
        n = V; hits = [nn for nn in range(1, 200) for q in [F(k, 100) for k in range(1, 100)] if nn * q == p['m'] and nn * q * (1 - q) == p['v']]; return hits == [n]
    if t == 'c_bags':   # weighted list of (bag, ball) outcomes
        out = []
        for i, ((w, b), pr) in enumerate(zip(p['bags'], p['pri'])):
            for ball in ['white'] * w + ['black'] * b: out.append((i, ball, F(pr, sum(p['pri'])) / (w + b)))
        num = sum(wt for i, ball, wt in out if i == p['j'] and ball == p['col']); den = sum(wt for i, ball, wt in out if ball == p['col']); return V == num / den
    if t == 'c_transfer':
        w1, b1, w2, b2 = p['s']; tot = F(0)
        for moved in ['w'] * w1 + ['b'] * b1:
            bag = ['w'] * w2 + ['b'] * b2 + [moved]; tot += F(1, w1 + b1) * F(bag.count('w'), len(bag))
        return V == tot
    if t == 'c_coin':
        N, h = p['N'], p['h']; coins = [0.5] * N + [1.0]; num = sum(F(1, N + 1) * F(c).limit_denominator() ** h for c in coins[:N]); den = num + F(1, N + 1); return V == num / den
    if t == 'c_total': return V == sum(a * b for a, b in zip(p['ps'], p['qs']))
    if t == 'c_test':
        pop = 10 ** 6; sick = p['prev'] * pop; tp = sick * p['sens']; fp = (pop - sick) * p['fpos']; return V == tp / (tp + fp)
    raise KeyError(t)
