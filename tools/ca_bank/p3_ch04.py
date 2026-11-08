"""Paper 3 Ch 4 — Mathematics of Finance: extra MCQ templates (answers computed)."""
from common import *
import math

U = 'fnd-p3-ch04-u01'
C2, C3, C4, C5 = 'Simple interest', 'Compound interest and conversion period', 'Effective, nominal and real rates', 'Annuities — regular and due; future value; sinking fund'
C6, C7, C8, C9, C10 = 'Present value of annuities; loan amortisation (EMI)', 'Applications: leasing, capital expenditure, bond valuation', 'Perpetuities — level and growing', 'Net present value (NPV) technique', 'Compound annual growth rate (CAGR) and rate of return'
MW = {2: 'half-yearly', 4: 'quarterly', 12: 'monthly'}


def money(v): return rs(round(v, 2))


def keys(base, n): return f'type {base}, press × once, then = {n - 1} times to get ({base})^{n}'


def si_rate(r):
    P = r.choice(range(5000, 200001, 2500)); R = F(r.choice([4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 25]), r.choice([1, 2])); t = F(r.choice([2, 3, 4, 5, 6, 8, 10]), r.choice([1, 1, 2]))
    I = P * R * t / 100
    if I.denominator != 1 or R * t > 100: return None
    A = P + int(I)
    def yrs(x): return f'{fr(x)} years' if x.denominator == 1 else f'{int(x)}½ years' if x.denominator == 2 else f'{fr(x)} years'
    return dict(q=f'A sum of ₹{inr(P)} amounts to ₹{inr(A)} in {yrs(t)} at simple interest. The rate of interest per annum is:', a=pct(R),
                w=[pct(F(A, P) * 100 / t), pct(R * 2), pct(F(I * 100, A * t)), pct(R + 1)],
                ex=f'Interest = amount − principal = {inr(A)} − {inr(P)} = ₹{inr(int(I))}. Simple interest I = P × R × T / 100, so R = 100 × I / (P × T) = 100 × {inr(int(I))} / ({inr(P)} × {fr(t)}) = {num(R)}%. Dividing by the amount instead of the principal gives a lower, wrong rate.',
                fast=f'Interest per year = ₹{num(I / t)}; as a % of ₹{inr(P)} that is {num(R)}%.', secs=40, d='core', topic=C2,
                check=f'100*{int(I)}/({P}*{float(t)})', k='ch04.sirate', data={'P': P, 'A': A, 't': float(t)})


def si_parts(r):
    N = r.choice(range(10000, 150001, 5000)); r1, r2 = sorted(r.sample([4, 5, 6, 8, 9, 10, 12, 15], 2)); x = r.choice(range(1000, N, 1000))
    I = F(x * r1 + (N - x) * r2, 100)
    if I.denominator != 1: return None
    I = int(I)
    return dict(q=f'₹{inr(N)} is lent in two parts, one at {r1}% and the other at {r2}% simple interest per annum. The total interest for one year is ₹{inr(I)}. The part lent at {r1}% is:',
                a=rs(x), w=[rs(N - x), rs(N // 2), rs(round(I * 100 / r1)) if round(I * 100 / r1) < N else rs(x + 1000), rs(x + 500)],
                ex=f'Let ₹x be lent at {r1}%; then ₹({inr(N)} − x) is at {r2}%. Interest: {r1}x/100 + {r2}({inr(N)} − x)/100 = {inr(I)}. So ({r2} − {r1})x/100 = {inr(N * r2 // 100) if N * r2 % 100 == 0 else num(N * r2 / 100)} − {inr(I)}, giving x = ₹{inr(x)}. The other part, ₹{inr(N - x)}, is at {r2}%.',
                fast=f'Alligation: if all were at {r2}% interest = ₹{num(N * r2 / 100)}; each rupee moved to {r1}% cuts {r2 - r1} paise. Shortfall ₹{num(N * r2 / 100 - I)} ÷ 0.{r2 - r1:02d} = ₹{inr(x)}.', secs=60,
                d='moderate', topic=C2, check=str(x), k='ch04.siparts', data={'N': N, 'r1': r1, 'r2': r2, 'I': I})


def ci_periodic(r):
    P = r.choice(range(10000, 300001, 5000)); R = r.choice([6, 8, 10, 12, 16, 20]); m = r.choice([2, 4]); t = F(r.choice([1, 2, 3, 3, 5]), r.choice([1, 2]))
    n = m * t
    if n.denominator != 1 or n > 12: return None
    n = int(n); i = R / (100 * m)
    A = P * (1 + i) ** n; ci = A - P
    yrs = ('1 year' if t == 1 else f'{fr(t)} years') if t.denominator == 1 else f'{int(t)}½ years' if t > 1 else '6 months'
    return dict(q=f'The compound interest on ₹{inr(P)} for {yrs} at {R}% per annum, compounded {MW[m]}, is:', a=money(ci),
                w=[money(P * (1 + R / 100) ** float(t) - P), money(P * R * float(t) / 100), money(A), money(P * (1 + i) ** (n - 1) - P), money(P * (1 + i) ** (n + 1) - P)],
                ex=f'Compounded {MW[m]}: rate per period i = {R}% ÷ {m} = {num(R / m)}% and periods n = {fr(t)} × {m} = {n}. Amount = {inr(P)} × (1 + {num(i, 4)})^{n} = ₹{numf(A)}. CI = amount − principal = ₹{numf(ci)}. Using {R}% with annual periods ignores the more frequent compounding.',
                fast=f'Calculator: {keys(num(1 + i, 4), n)}; then × {inr(P)} and subtract {inr(P)}.', secs=60, d='moderate', topic=C3,
                check=f'{P}*(1+{R}/{100*m})**{n}-{P}', k='ch04.ciper', data={'P': P, 'R': R, 'm': MW[m], 't': float(t)})


def ci_si_diff(r):
    R = r.choice([4, 5, 8, 10, 12, 15, 20]); P = r.choice(range(5000, 200001, 2500))
    dif = F(P * R * R, 10000)
    if dif.denominator != 1: return None
    return dict(q=f'At {R}% per annum, the 2-year compound interest on a certain sum exceeds the 2-year simple interest on it by ₹{inr(int(dif))}. The sum is:', a=rs(P),
                w=[rs(P * 2), rs(P // 2), rs(int(dif) * 100 // R), rs(P + 2500 * R // 5)],
                ex=f'For 2 years, CI − SI = P × (R/100)², because the only extra is the interest earned in year 2 on year-1 interest. So {inr(int(dif))} = P × ({R}/100)² = P × {num(R*R/10000, 4)}, giving P = ₹{inr(P)}. Using P × R/100 only (₹{inr(int(dif) * 100 // R)}) is the common slip.',
                fast=f'P = difference × (100/R)² = {inr(int(dif))} × {num((100 / R) ** 2, 4)}.', secs=30, d='core', topic=C3, check=f'{int(dif)}*(100/{R})**2', k='ch04.cisi', data={'R': R, 'D': int(dif)})


def effective(r):
    R = r.choice([6, 7, 8, 9, 10, 12, 14, 15, 16, 18]); m = r.choice([2, 4, 12])
    E = ((1 + R / (100 * m)) ** m - 1) * 100
    return dict(q=f'The effective annual rate of interest equivalent to a nominal rate of {R}% per annum compounded {MW[m]} is:', a=pct(E),
                w=[pct(R), pct(((1 + R / 100 / m) ** (m // 2 if m > 2 else 1) - 1) * 100 * (2 if m > 2 else 1)) if m > 2 else pct(R + R * R / 400 + 0.5), pct(R / m), pct(((1 + R / 100) ** m - 1) * 100 / m)],
                ex=f'Effective rate E = (1 + i)^m − 1, where i = {R}%/{m} = {num(R / m, 4)}% per period and m = {m}. E = (1 + {num(R / (100 * m), 6)})^{m} − 1 = {numf(E / 100, 4)}, i.e. {num(E)}%. It is always above the nominal rate when interest is compounded more than once a year.',
                fast=f'Calculator: {keys(num(1 + R / (100 * m), 6), m)}; subtract 1. Answer must be a little above {R}%.', secs=45, d='core', topic=C4,
                check=f'((1+{R}/{100*m})**{m}-1)*100', k='ch04.eff', data={'R': R, 'm': MW[m]})


def real_rate(r):
    n_ = r.choice([8, 9, 10, 11, 12, 14, 15]); inf = r.choice([3, 4, 5, 6, 7])
    if inf >= n_: return None
    rr_ = ((1 + n_ / 100) / (1 + inf / 100) - 1) * 100
    return dict(q=f'A deposit earns a nominal {n_}% per annum while inflation is {inf}% per annum. The real rate of interest (exact formula) is about:', a=pct(rr_),
                w=[pct(n_ - inf), pct(n_ + inf), pct((n_ - inf) * (1 + inf / 100)), pct(n_ / inf)],
                ex=f'Real rate = (1 + nominal)/(1 + inflation) − 1 = {1 + n_ / 100}/{1 + inf / 100} − 1 = {numf(rr_ / 100, 4)}, i.e. about {num(rr_)}%. The quick estimate {n_} − {inf} = {n_ - inf}% slightly overstates the real return because it ignores that inflation also erodes the interest.',
                fast=f'Divide: {1 + n_ / 100} ÷ {1 + inf / 100} − 1; the answer is a little below {n_ - inf}%.', secs=35, d='moderate', topic=C4,
                check=f'((1+{n_}/100)/(1+{inf}/100)-1)*100', k='ch04.real', data={'n': n_, 'inf': inf})


def fv_annuity(r):
    A = r.choice(range(2000, 100001, 1000)); R = r.choice([5, 6, 7, 8, 9, 10, 12]); n = r.randint(3, 12)
    i = R / 100; fv = A * ((1 + i) ** n - 1) / i
    return dict(q=f'₹{inr(A)} is deposited at the end of every year for {n} years at {R}% per annum compound interest. The amount at the end of {n} years is:', a=money(fv),
                w=[money(fv * (1 + i)), money(A * n), money(A * n * (1 + i * n)), money(A * ((1 + i) ** (n - 1) - 1) / i)],
                ex=f'This is the future value of an annuity regular: FV = A × [(1 + i)^n − 1]/i = {inr(A)} × [(1.{R:02d})^{n} − 1]/{i} = ₹{numf(fv)}. The last deposit earns no interest. If deposits were at the beginning of each year (annuity due), multiply by 1.{R:02d}, giving the trap ₹{numf(fv * (1 + i))}.',
                fast=f'A({n}, {R}%) = [(1.{R:02d})^{n} − 1]/{i} = {numf(((1 + i) ** n - 1) / i, 4)}; × {inr(A)}.', secs=60, d='moderate', topic=C5,
                check=f'{A}*((1+{i})**{n}-1)/{i}', k='ch04.fva', data={'A': A, 'R': R, 'n': n})


def annuity_due(r):
    A = r.choice(range(5000, 200001, 5000)); R = r.choice([5, 6, 8, 10, 12]); n = r.randint(3, 10); i = R / 100
    pv = A * (1 + i) * (1 - (1 + i) ** (-n)) / i
    return dict(q=f'A scholarship pays ₹{inr(A)} at the BEGINNING of each year for {n} years. At {R}% per annum, its present value is:', a=money(pv),
                w=[money(pv / (1 + i)), money(A * n), money(A * (1 + i) ** n), money(A + A * (1 - (1 + i) ** (-(n - 2))) / i)],
                ex=f'Payments at the beginning of each period form an annuity due. PV = A × [1 − (1 + i)^−n]/i × (1 + i) = {inr(A)} × {numf((1 - (1 + i) ** (-n)) / i, 4)} × 1.{R:02d} = ₹{numf(pv)}. Equivalently, the first payment is received today and the other {n - 1} form an annuity regular.',
                fast=f'PV due = PV regular × 1.{R:02d}; or A + A × P({n - 1}, {R}%).', secs=60, d='moderate', topic=C5,
                check=f'{A}*(1+{i})*(1-(1+{i})**(-{n}))/{i}', k='ch04.due', data={'A': A, 'R': R, 'n': n})


def sinking(r):
    FV = r.choice(range(100000, 5000001, 50000)); R = r.choice([5, 6, 8, 10, 12]); n = r.randint(4, 15); i = R / 100
    dep = FV * i / ((1 + i) ** n - 1)
    return dict(q=f'A company must replace a machine costing ₹{inr(FV)} after {n} years. How much must it set aside at the end of each year in a sinking fund earning {R}% per annum?', a=money(dep),
                w=[money(FV / n), money(FV * i / ((1 + i) ** n - 1) / (1 + i)), money(FV * i / (1 - (1 + i) ** (-n))), money(FV / (1 + i) ** n)],
                ex=f'The deposits are an annuity regular whose future value must equal ₹{inr(FV)}: A × [(1 + i)^n − 1]/i = {inr(FV)}. So A = {inr(FV)} × {i}/[(1.{R:02d})^{n} − 1] = ₹{numf(dep)}. Dividing ₹{inr(FV)} by {n} ignores the interest the fund earns.',
                fast=f'A = FV ÷ A({n}, {R}%), where A({n}, {R}%) = {numf(((1 + i) ** n - 1) / i, 4)}.', secs=60, d='moderate', topic=C5,
                check=f'{FV}*{i}/((1+{i})**{n}-1)', k='ch04.sink', data={'FV': FV, 'R': R, 'n': n})


def pv_annuity(r):
    A = r.choice(range(2000, 100001, 500)); R = r.choice([6, 8, 9, 10, 12, 14]); n = r.randint(3, 15); i = R / 100
    pv = A * (1 - (1 + i) ** (-n)) / i
    return dict(q=f'Find the present value of ₹{inr(A)} received at the end of each year for {n} years if money is worth {R}% per annum.', a=money(pv),
                w=[money(A * n), money(pv * (1 + i)), money(A * n / (1 + i * n)), money(A * ((1 + i) ** n - 1) / i)],
                ex=f'PV of an annuity regular = A × [1 − (1 + i)^−n]/i = {inr(A)} × [1 − (1.{R:02d})^−{n}]/{i} = ₹{numf(pv)}. The present value is always less than the total paid ({inr(A)} × {n} = ₹{inr(A * n)}) because later rupees are worth less today.',
                fast=f'P({n}, {R}%) = {numf((1 - (1 + i) ** (-n)) / i, 4)}; × {inr(A)}. Reject any option ≥ ₹{inr(A * n)}.', secs=60, d='moderate', topic=C6,
                check=f'{A}*(1-(1+{i})**(-{n}))/{i}', k='ch04.pva', data={'A': A, 'R': R, 'n': n})


def emi(r):
    L = r.choice(range(100000, 3000001, 50000)); R = r.choice([6, 8, 9, 10, 12, 15]); yrs = r.randint(2, 5); m = r.choice([1, 12])
    i = R / 100 / m; n = yrs * m
    e = L * i / (1 - (1 + i) ** (-n))
    per = 'monthly' if m == 12 else 'annual'
    return dict(q=f'A loan of ₹{inr(L)} at {R}% per annum is to be repaid in equal {per} instalments over {yrs} years (interest {"compounded monthly" if m == 12 else "compounded annually"}). The instalment (EMI) is:', a=money(e),
                w=[money(L / n), money(L * (1 + R / 100 * yrs) / n), money(L * i / ((1 + i) ** n - 1)), money(e / (1 + i))],
                ex=f'The loan equals the present value of the instalments: L = E × [1 − (1 + i)^−n]/i, with i = {num(i * 100, 4)}% per period and n = {n}. So E = {inr(L)} × {num(i, 6)}/[1 − (1 + {num(i, 6)})^−{n}] = ₹{numf(e)}. Spreading flat interest (₹{numf(L * (1 + R / 100 * yrs) / n)}) overstates the cost.',
                fast='EMI = L × i/(1 − (1 + i)^−n): compute (1 + i)^n with repeated ×, take its reciprocal, subtract from 1.', secs=75, d='hard', topic=C6,
                check=f'{L}*{R}/{100*m}/(1-(1+{R}/{100*m})**(-{n}))', k='ch04.emi', data={'L': L, 'R': R, 'yrs': yrs, 'per': per})


def lease(r):
    C = r.choice(range(200000, 3000001, 100000)); R = r.choice([8, 10, 12, 14, 15]); n = r.randint(3, 8); i = R / 100
    rent = C * i / (1 - (1 + i) ** (-n))
    return dict(q=f'A firm leases out an asset costing ₹{inr(C)} for {n} years with no salvage value. To earn {R}% per annum, the annual lease rent (paid at year end) should be:', a=money(rent),
                w=[money(C / n), money(C / n * (1 + i)), money(C * i), money(C * i / ((1 + i) ** n - 1))],
                ex=f'The lessor wants the present value of the {n} rents at {R}% to equal the cost: Rent × P({n}, {R}%) = {inr(C)}. P({n}, {R}%) = [1 − (1.{R:02d})^−{n}]/{i} = {numf((1 - (1 + i) ** (-n)) / i, 4)}, so Rent = ₹{numf(rent)}. Cost ÷ years recovers the cost but no return.',
                fast=f'Rent = cost ÷ P({n}, {R}%) — the same calculation as an EMI.', secs=60, d='moderate', topic=C7,
                check=f'{C}*{i}/(1-(1+{i})**(-{n}))', k='ch04.lease', data={'C': C, 'R': R, 'n': n})


def bond(r):
    face = r.choice([100, 1000, 10000]); c = r.choice([6, 7, 8, 9, 10, 11, 12]); y = r.choice([6, 7, 8, 9, 10, 11, 12, 14]); n = r.randint(2, 8)
    if c == y: return None
    cp = face * c / 100; i = y / 100
    pr = cp * (1 - (1 + i) ** (-n)) / i + face * (1 + i) ** (-n)
    return dict(q=f'A bond of face value ₹{inr(face)} pays a {c}% annual coupon and is redeemed at par after {n} years. If the required yield is {y}% per annum, its value is:', a=money(pr),
                w=[money(face), money(cp * n + face), money(cp * (1 - (1 + i) ** (-n)) / i), money(face * (1 + i) ** (-n) + cp * n / (1 + i))],
                ex=f'Value = PV of coupons + PV of redemption = {num(cp)} × P({n}, {y}%) + {inr(face)} × (1.{y:02d})^−{n} = {numf(cp * (1 - (1 + i) ** (-n)) / i)} + {numf(face * (1 + i) ** (-n))} = ₹{numf(pr)}. When the coupon rate is {"above" if c > y else "below"} the yield, the bond sells at a {"premium" if c > y else "discount"} to face value.',
                fast=f'Sanity check first: coupon {c}% {">" if c > y else "<"} yield {y}% ⇒ price {">" if c > y else "<"} ₹{inr(face)}; then discount the coupons and the redemption.', secs=75, d='hard', topic=C7,
                check=f'{cp}*(1-(1+{i})**(-{n}))/{i}+{face}*(1+{i})**(-{n})', k='ch04.bond', data={'face': face, 'c': c, 'y': y, 'n': n})


def perpetuity(r):
    A = r.choice(range(1000, 100001, 500)); R = r.choice([5, 6, 8, 10, 12, 15]); g = r.choice([0, 0, 2, 3, 4, 5])
    if g >= R: return None
    pv = A / ((R - g) / 100)
    if g:
        q = f'What should you pay today for a stream that pays ₹{inr(A)} at the end of the first year and then grows at {g}% a year forever, when money is worth {R}% a year?'
        w = [money(A / (R / 100)), money(A / ((R + g) / 100)), money(A * (1 + g / 100) / ((R - g) / 100)), money(A * R / g)]
        ex = f'This is a growing perpetuity: PV = first payment ÷ (r − g) = {inr(A)} ÷ ({R}% − {g}%) = {inr(A)} ÷ {num((R - g) / 100, 2)} = ₹{numf(pv)}. Growth makes it worth more than the level perpetuity (₹{numf(A / (R / 100))}). The formula needs r > g.'
        fast = f'Divide the first payment by (r − g) = {R - g}%: {inr(A)} × 100/{R - g}.'
    else:
        q = f'The present value of a perpetuity of ₹{inr(A)} receivable at the end of every year, at {R}% per annum, is:'
        w = [money(A * R / 100), money(A / (R / 100) * (1 + R / 100)), money(A * 100), money(A / (R / 100) - A)]
        ex = f'A perpetuity pays for ever, yet its PV is finite because far-off payments are worth almost nothing today. PV = payment ÷ rate = {inr(A)} ÷ {R / 100} = ₹{numf(pv)}. If the first payment were received today (perpetuity due), add one payment.'
        fast = f'PV = A × 100/{R} = {inr(A)} × {num(100 / R, 4)}.'
    return dict(q=q, a=money(pv), w=w, ex=ex, fast=fast, secs=30, d='core' if not g else 'moderate', topic=C8, check=f'{A}/(({R}-{g})/100)', k='ch04.perp', data={'A': A, 'R': R, 'g': g})


def npv(r):
    C0 = r.choice(range(100000, 1000001, 50000)); n = r.randint(3, 5); k = r.choice([8, 10, 12, 15])
    cfs = [r.choice(range(int(C0 / n * 0.8) // 1000 * 1000, int(C0 / n * 1.6) // 1000 * 1000 + 1, 1000)) for _ in range(n)]
    v = sum(c / (1 + k / 100) ** (t + 1) for t, c in enumerate(cfs)) - C0
    if v < 2000: return None
    flows = ', '.join(f'₹{inr(c)}' for c in cfs)
    return dict(q=f'A project costs ₹{inr(C0)} now and returns {flows} at the end of years 1 to {n}. At a cost of capital of {k}%, its NPV is:', a=money(v),
                w=[money(sum(cfs) - C0), money(sum(c / (1 + k / 100) ** t for t, c in enumerate(cfs)) - C0), money(v + C0), money(sum(c / (1 + k / 100) for c in cfs) - C0)],
                ex=f'NPV = Σ CFₜ/(1 + k)ᵗ − initial outlay. Discount factors at {k}%: ' + ', '.join(f'{(1 + k / 100) ** -(t + 1):.4f}' for t in range(n)) + f'. PV of inflows = ₹{numf(v + C0)}; NPV = ₹{numf(v)}. A {"positive NPV: accept" if v > 0 else "negative NPV: reject"}. Not discounting at all gives ₹{inr(sum(cfs) - C0)}.',
                fast='Multiply each flow by its discount factor (1 ÷ 1.k repeatedly on the calculator, using GT/M+ to add), then subtract the cost.', secs=90, d='hard', topic=C9,
                check='+'.join(f'{c}/(1+{k}/100)**{t + 1}' for t, c in enumerate(cfs)) + f'-{C0}', k='ch04.npv', data={'C0': C0, 'cfs': cfs, 'k': k})


def cagr(r):
    V0 = r.choice(range(10000, 1000001, 10000)); n = r.randint(3, 10); g = r.choice([5, 6, 7, 8, 9, 10, 12, 14, 15, 18, 20]) + r.choice([0, 0.5])
    Vn = round(V0 * (1 + g / 100) ** n, -2)
    c = ((Vn / V0) ** (1 / n) - 1) * 100
    return dict(q=f'An investment grew from ₹{inr(V0)} to ₹{inr(int(Vn))} in {n} years. Its compound annual growth rate (CAGR) is about:', a=pct(c),
                w=[pct((Vn / V0 - 1) * 100 / n), pct((Vn / V0 - 1) * 100), pct(((Vn / V0) ** (1 / (n - 1)) - 1) * 100), pct(((Vn / V0) ** (1 / (n + 1)) - 1) * 100)],
                ex=f'CAGR = (ending ÷ beginning)^(1/n) − 1 = ({inr(int(Vn))}/{inr(V0)})^(1/{n}) − 1 = {num(Vn / V0, 4)}^(1/{n}) − 1 ≈ {num(c)}%. The simple average {num((Vn / V0 - 1) * 100 / n)}% ignores compounding and overstates the yearly growth. CAGR is the steady yearly rate that would turn the starting value into the ending value.',
                fast=f'Back-substitute: (1 + option)^{n} should give the growth multiple {num(Vn / V0, 4)}. Rule of 72 gives a rough check.', secs=60, d='moderate', topic=C10,
                check=f'(({int(Vn)}/{V0})**(1/{n})-1)*100', k='ch04.cagr', data={'V0': V0, 'Vn': int(Vn), 'n': n})


def depreciation(r):
    C = r.choice(range(50000, 2000001, 25000)); R = r.choice([10, 12, 15, 20, 25]); n = r.randint(2, 6)
    v = C * (1 - R / 100) ** n
    return dict(q=f'A machine costs ₹{inr(C)} and depreciates at {R}% per annum on the reducing (written-down) balance. Its value after {n} years is:', a=money(v),
                w=[money(C * (1 - R * n / 100)) if R * n < 100 else money(C * (1 - R / 100) ** (n + 1)), money(C * (1 + R / 100) ** n), money(C * (1 - R / 100) ** (n - 1)), money(C - C * (1 - R / 100) ** n)],
                ex=f'Reducing-balance depreciation is compound interest in reverse: value = C × (1 − r)^n = {inr(C)} × (1 − {R / 100})^{n} = {inr(C)} × {num((1 - R / 100) ** n, 6)} = ₹{numf(v)}. Straight-line thinking (deducting {R}% of cost every year) gives a lower, wrong figure.',
                fast=f'Calculator: {keys(num(1 - R / 100, 2), n)}; then × {inr(C)}.', secs=40, d='core', topic=C3,
                check=f'{C}*(1-{R}/100)**{n}', k='ch04.dep', data={'C': C, 'R': R, 'n': n})


def doubling(r):
    R = r.choice([4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18]); k = r.choice([2, 2, 3])
    n = 1
    while (1 + R / 100) ** n < k: n += 1
    if abs((1 + R / 100) ** n - k) < 0.003: return None
    word = {2: 'double', 3: 'treble'}[k]
    return dict(q=f'At {R}% per annum compound interest (compounded annually), after how many complete years will a sum first become more than {word} itself?', a=f'{n} years',
                w=[f'{n - 1} years', f'{n + 1} years', f'{math.ceil((k - 1) * 100 / R)} years' if math.ceil((k - 1) * 100 / R) not in (n, n - 1, n + 1) else f'{n + 2} years', f'{n + 3} years'],
                ex=f'We need the smallest n with (1.{R:02d})^n > {k}. (1.{R:02d})^{n - 1} = {num((1 + R / 100) ** (n - 1), 4)} is still below {k}, while (1.{R:02d})^{n} = {num((1 + R / 100) ** n, 4)} exceeds it. So {n} years. Simple interest would need {num((k - 1) * 100 / R)} years — compounding is faster.',
                fast=f'Rule of {"72" if k == 2 else "114"}: about {num((72 if k == 2 else 114) / R, 1)} years; confirm with (1.{R:02d})^n on the calculator.', secs=40, d='moderate', topic=C3,
                check=str(n), k='ch04.double', data={'R': R, 'word': word})


BANKS = {U: [(si_rate, 2), (si_parts, 2), (ci_periodic, 2), (ci_si_diff, 2), (effective, 2), (real_rate, 2), (fv_annuity, 2), (annuity_due, 2), (sinking, 2),
             (pv_annuity, 2), (emi, 2), (lease, 2), (bond, 2), (perpetuity, 3), (npv, 2), (cagr, 2), (depreciation, 2), (doubling, 2)]}
