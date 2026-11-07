"""CA Foundation · Paper 3 Quantitative Aptitude · Chapter 4 Mathematics of Finance (single unit).
Original explanations, numbers and questions; scope follows the ICAI study material (May 2027 onwards).
Every figure is computed here and stored with a check expression that the validator re-evaluates."""
import math
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch04-u01'


class Checks(Checks):
    """lib.Checks (stored value rounded to 2 dp for the validator) that returns the unrounded value for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = eval(expr, {'__builtins__': {}}, {'round': round})
        return int(round(v)) if abs(v - round(v)) < 1e-9 else v


def num(v, dp=2):
    v = round(v, dp)
    if v == int(v): return str(int(v))
    return f'{v:.{dp}f}'.rstrip('0').rstrip('.')


def Rs(v, dp=2):
    """₹ with Indian grouping, rounded to paise (always two decimals when not a whole rupee); negatives as −₹."""
    v = round(v, dp)
    neg = v < 0; v = abs(v)
    whole = inr(int(v))
    paise = round((v - int(v)) * 100)
    s = '₹' + whole + (f'.{paise:02d}' if paise else '')
    return ('−' if neg else '') + s


def M(mid, q, options, answer, explain, concept, difficulty='moderate', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if topic: d['topic'] = topic
    if check is not None: d['check'] = check
    return d


# expression builders (strings the validator can evaluate)
def eA(n, i): return f'(((1+{i})**{n}-1)/{i})'          # A(n, i): future value of ₹1 per period, annuity regular
def eP(n, i): return f'((1-(1+{i})**(-{n}))/{i})'       # P(n, i): present value of ₹1 per period, annuity regular
def ev(e): return eval(e, {'__builtins__': {}}, {'round': round})


def build():
    # ---------- i1 Simple interest ----------
    c1 = Checks()
    si1 = c1.add('48000*9/100*2.5', 'SI on ₹48,000 at 9% for 2½ years')
    a1 = c1.add('48000+48000*9/100*2.5', 'amount')
    r1 = c1.add('(3-1)/16*100', 'rate % for a sum to triple in 16 years (SI)')

    # ---------- i2 Compound interest, different conversion periods ----------
    c2 = Checks()
    rows2 = []
    for lab, m in (('Annually', 1), ('Half-yearly', 2), ('Quarterly', 4), ('Monthly', 12)):
        i, n = 0.12 / m, 2 * m
        e = f'80000*(1+0.12/{m})**{2*m}'
        amt = c2.add(f'round({e},2)', f'amount, compounded {lab.lower()}')
        ci = c2.add(f'round({e},2)-80000', f'CI, compounded {lab.lower()}')
        rows2.append([lab, f'{num(i*100)}% × {n}', round(amt, 2), round(ci, 2)])
    t2 = table(['Compounding', 'Rate per period × periods', 'Amount (₹)', 'Compound interest (₹)'], rows2)

    # ---------- i3 CI − SI and depreciation ----------
    c3 = Checks()
    d3 = c3.add('250000*(1.08**2-1)-250000*0.08*2', 'CI − SI for 2 years')
    c3.add('250000*0.08**2', 'shortcut P × r²')
    w3 = c3.add('500000*(1-0.15)**3', 'WDV after 3 years at 15% reducing balance')

    # ---------- i4 Effective rate; real rate ----------
    c4 = Checks()
    e4q = c4.add('((1+0.10/4)**4-1)*100', 'effective rate, 10% compounded quarterly')
    e4h = c4.add('((1+0.102/2)**2-1)*100', 'effective rate, 10.2% compounded half-yearly')
    rr = c4.add('9-5.5', 'real rate = nominal − inflation')

    # ---------- i5 FV of annuity regular and due ----------
    c5 = Checks()
    fa5 = c5.add(eA(5, 0.08), 'A(5, 0.08)')
    fv5 = c5.add(f'round(20000*{eA(5, 0.08)},2)', 'FV of annuity regular')
    fvd5 = c5.add(f'round(20000*{eA(5, 0.08)}*1.08,2)', 'FV of annuity due')

    # ---------- i6 Sinking fund ----------
    c6 = Checks()
    fa6 = c6.add(eA(6, 0.09), 'A(6, 0.09)')
    sf6 = c6.add(f'round(1000000/{eA(6, 0.09)},2)', 'annual sinking-fund deposit')

    # ---------- i7 EMI and amortisation ----------
    c7 = Checks()
    pf7 = c7.add(eP(36, 0.01), 'P(36, 0.01)')
    emi = c7.add(f'round(600000/{eP(36, 0.01)},2)', 'monthly EMI')
    int1 = c7.add('600000*0.01', 'interest in month 1')
    pr1 = c7.add(f'round(600000/{eP(36, 0.01)},2)-6000', 'principal repaid in month 1')
    bal1 = c7.add(f'600000-(round(600000/{eP(36, 0.01)},2)-6000)', 'balance after month 1')
    int2 = c7.add(f'round((600000-(round(600000/{eP(36, 0.01)},2)-6000))*0.01,2)', 'interest in month 2')
    pr2 = round(emi - int2, 2); bal2 = round(bal1 - pr2, 2)
    c7.add(f'round(600000/{eP(36, 0.01)},2)-round((600000-(round(600000/{eP(36, 0.01)},2)-6000))*0.01,2)', 'principal repaid in month 2')
    sched = table(['Month', 'Opening balance (₹)', 'EMI (₹)', 'Interest @1% (₹)', 'Principal (₹)', 'Closing balance (₹)'],
                  [['1', 600000, round(emi, 2), round(int1, 2), round(pr1, 2), round(bal1, 2)], ['2', round(bal1, 2), round(emi, 2), round(int2, 2), pr2, bal2]],
                  title='First two lines of the amortisation schedule')
    assert abs(emi - 600000 / ((1 - 1.01 ** -36) / 0.01)) < 0.006 and abs(sf6 - 1e6 * 0.09 / (1.09 ** 6 - 1)) < 0.006 and abs(sum(600000 / ((1 - 1.01 ** -36) / 0.01) / 1.01 ** k for k in range(1, 37)) - 600000) < 0.01

    # ---------- i8 PV of annuity due ----------
    c8 = Checks()
    pf8 = c8.add(eP(3, 0.10), 'P(3, 0.10)')
    pvd8 = c8.add(f'round(120000*(1+{eP(3, 0.10)}),2)', 'PV of annuity due')
    c8.add(f'round(120000*{eP(4, 0.10)}*1.10,2)', 'cross-check: PV regular × (1 + i)')

    # ---------- i9 Leasing and capital expenditure ----------
    c9 = Checks()
    pf9 = c9.add(eP(5, 0.12), 'P(5, 0.12)')
    pvl = c9.add(f'round(140000*{eP(5, 0.12)},2)', 'PV of lease rentals')
    pf9b = c9.add(eP(5, 0.11), 'P(5, 0.11)')
    pvc = c9.add(f'round(55000*{eP(5, 0.11)},2)', 'PV of machine contributions')

    # ---------- i10 Bond ----------
    c10 = Checks()
    pf10 = c10.add(eP(4, 0.11), 'P(4, 0.11)')
    pvcpn = c10.add(f'round(90*{eP(4, 0.11)},2)', 'PV of coupons')
    pvred = c10.add('round(1000*1.11**(-4),2)', 'PV of redemption')
    bond = c10.add(f'round(90*{eP(4, 0.11)},2)+round(1000*1.11**(-4),2)', 'bond value')

    # ---------- i11 Perpetuities ----------
    c11 = Checks()
    pp = c11.add('60000/0.08', 'level perpetuity')
    ppd = c11.add('60000/0.08+60000', 'perpetuity due')
    gp = c11.add('round(40000/(0.12-0.05),2)', 'growing perpetuity')

    # ---------- i12 NPV ----------
    c12 = Checks()
    pv1 = c12.add('120000*0.893', 'PV year 1'); pv2 = c12.add('150000*0.797', 'PV year 2'); pv3 = c12.add('100000*0.712', 'PV year 3')
    npv = c12.add('120000*0.893+150000*0.797+100000*0.712-300000', 'NPV')
    npvt = table(['Year', 'Cash flow (₹)', 'PV factor @12%', 'Present value (₹)'],
                 [['0', '(3,00,000)', '1.000', -300000], ['1', '1,20,000', '0.893', pv1], ['2', '1,50,000', '0.797', pv2], ['3', '1,00,000', '0.712', pv3], ['Net present value', '', '', round(npv, 2)]],
                 num=[3], total=True)

    # ---------- i13 CAGR ----------
    c13 = Checks()
    cg = c13.add('((58.564/40)**(1/4)-1)*100', 'CAGR %')

    # ---------- Jobs ----------
    j1c = Checks()
    ea = j1c.add('((1+0.105/12)**12-1)*100', 'Bank A effective rate (10.5% monthly)')
    eb = j1c.add('((1+0.107/2)**2-1)*100', 'Bank B effective rate (10.7% half-yearly)')
    j2c = Checks()
    pvlease = j2c.add(f'round(1250000*{eP(4, 0.10)},2)', 'PV of lease rentals at 10%')
    j3c = Checks()
    pvin = j3c.add(f'round(260000*{eP(6, 0.13)},2)', 'PV of inflows at 13%')
    npvj = j3c.add(f'round(260000*{eP(6, 0.13)},2)-1000000', 'NPV')
    j4c = Checks()
    sfj = j4c.add(f'round(5000000/{eA(5, 0.07)},2)', 'annual DRR investment')

    # ---------- Questions ----------
    q1c = Checks()
    q1pf = q1c.add(eP(3, 0.10), 'P(3, 0.10)')
    q1e = q1c.add(f'round(300000/{eP(3, 0.10)},2)', 'annual instalment')
    q1i1 = q1c.add('300000*0.10', 'interest year 1')
    q1p1 = q1c.add(f'round(300000/{eP(3, 0.10)},2)-30000', 'principal year 1')
    q1b1 = q1c.add(f'300000-(round(300000/{eP(3, 0.10)},2)-30000)', 'balance after year 1')
    q1i2 = round(q1b1 * 0.10, 2); q1p2 = round(q1e - q1i2, 2); q1b2 = round(q1b1 - q1p2, 2)
    q1i3 = round(q1b2 * 0.10, 2); q1p3 = round(q1e - q1i3, 2); q1b3 = round(q1b2 - q1p3, 2)
    q1c.add(f'round((300000-(round(300000/{eP(3, 0.10)},2)-30000))*0.10,2)', 'interest year 2')
    assert abs(q1b3) < 0.05, q1b3
    q1t = table(['Year', 'Opening (₹)', 'Instalment (₹)', 'Interest @10% (₹)', 'Principal (₹)', 'Closing (₹)'], [
        ['1', 300000, round(q1e, 2), q1i1, round(q1p1, 2), round(q1b1, 2)],
        ['2', round(q1b1, 2), round(q1e, 2), q1i2, q1p2, q1b2],
        ['3', q1b2, round(q1e, 2), q1i3, q1p3, abs(round(q1b3, 0))]])
    q2c = Checks()
    q2pv = [q2c.add(f'{cf}*{f}', f'PV year {k}') for k, (cf, f) in enumerate([(60000, 0.909), (70000, 0.826), (80000, 0.751), (50000, 0.683)], 1)]
    q2n = q2c.add('60000*0.909+70000*0.826+80000*0.751+50000*0.683-200000', 'NPV')
    q2t = table(['Year', 'Cash flow (₹)', 'PV factor @10%', 'Present value (₹)'],
                [['0', '(2,00,000)', '1.000', -200000], ['1', '60,000', '0.909', q2pv[0]], ['2', '70,000', '0.826', q2pv[1]], ['3', '80,000', '0.751', q2pv[2]], ['4', '50,000', '0.683', q2pv[3]], ['NPV', '', '', round(q2n, 2)]],
                num=[3], total=True)
    q3c = Checks()
    q3cp = q3c.add(f'round(80*{eP(5, 0.10)},2)', 'PV of coupons (8% of ₹1,000)')
    q3rd = q3c.add('round(1050*1.10**(-5),2)', 'PV of redemption at ₹1,050')
    q3v = q3c.add(f'round(80*{eP(5, 0.10)},2)+round(1050*1.10**(-5),2)', 'value of the bond')

    # ---------- Case ----------
    kc = Checks()
    kpf = kc.add(eP(5, 0.12), 'P(5, 0.12)')
    kpvl = kc.add(f'round(660000*{eP(5, 0.12)},2)', 'PV of lease rentals')
    knpv = kc.add(f'round(700000*{eP(5, 0.12)},2)-2400000', 'NPV of buying')
    case = {
        'id': 'k1', 'title': 'Buy or lease a delivery truck', 'difficulty': 'hard',
        'case': ('Vardhan Logistics needs a truck for five years. It can buy the truck for ₹24,00,000 cash (no scrap value), or lease it for ₹6,60,000 a year payable at the end of each year. '
                 'The company can borrow at 12% a year compounded annually. The truck is expected to generate net cash inflows of ₹7,00,000 at the end of each year for five years.'),
        'mcqs': [
            M('k1a', 'The present value of ₹1 a year for 5 years at 12%, P(5, 0.12), is closest to:', ['3.6048', '6.3528', '4.1114', '3.0373'], 0,
              'P(5, 0.12) = [1 − (1.12)⁻⁵]/0.12 = (1 − 0.56743)/0.12 = 3.6048. It is the sum of the five yearly discount factors at 12%. The trap is 6.3528, which is the future-value factor A(5, 0.12) — compounding instead of discounting. In practice: finance teams keep such annuity factors in a spreadsheet to value any level five-year stream, such as lease rentals or loan EMIs.', 'c6', 'moderate', f'round({eP(5, 0.12)},4)', topic='Present value of annuities; loan amortisation (EMI)'),
            M('k1b', 'The present value of the lease rentals is:', [Rs(kpvl), R(3300000), Rs(round(660000 * ev(eA(5, 0.12)), 2)), Rs(round(660000 * ev(eP(5, 0.12)) * 1.12, 2))], 0,
              "Rentals are paid at the end of each year, so PV = 6,60,000 × P(5, 0.12) = 6,60,000 × 3.60478 = ₹23,79,152.29. The trap is ₹33,00,000, which adds the five rentals and ignores discounting; ₹26,64,650.57 treats the rentals as payable in advance. In practice: before signing a vehicle lease, a company's finance team discounts the rentals at its borrowing rate to compare with the cash price.", 'c7', 'hard', f'round(660000*{eP(5, 0.12)},2)', topic='Applications: leasing, capital expenditure, bond valuation'),
            M('k1c', 'On cost alone, which option should the company choose?', ['Lease — the PV of rentals is below the purchase price', 'Buy — the purchase price is below the PV of rentals', 'Indifferent — both cost the same', 'Buy — leasing never saves money'], 0,
              "Compare costs in present-value terms: the lease rentals are worth ₹23,79,152.29 today, which is below the ₹24,00,000 cash price, so leasing is cheaper. The trap is 'Buy', which would be right only if the PV of rentals exceeded the purchase price; comparing undiscounted rentals (₹33,00,000) with the price is the classic error. In practice: Indian logistics firms make lease-or-buy decisions this way, often adding tax effects like depreciation and GST later.", 'c7', 'moderate', topic='Applications: leasing, capital expenditure, bond valuation'),
            M('k1d', 'The NPV of buying the truck (inflows ₹7,00,000 a year) is:', [Rs(knpv), R(1100000), Rs(round(700000 * ev(eP(5, 0.12)), 2)), Rs(round(700000 * ev(eP(4, 0.12)) - 2400000, 2))], 0,
              'NPV = PV of inflows − cost = 7,00,000 × 3.60478 − 24,00,000 = 25,23,343.34 − 24,00,000 = ₹1,23,343.34. The positive NPV shows the truck is worth acquiring at a 12% cost of money. The trap is ₹25,23,343.34, which is the PV of inflows without deducting the cost; ₹11,00,000 ignores discounting. In practice: project reports submitted to banks for term loans include an NPV statement like this.', 'c9', 'hard', f'round(700000*{eP(5, 0.12)},2)-2400000', topic='Net present value (NPV) technique'),
            M('k1e', 'If the lessor quoted 12% a year compounded monthly instead, the effective annual rate would be:', ['12.68%', '12%', '12.36%', '1%'], 0,
              'Monthly compounding at 12% means 1% per month: effective rate = (1.01)¹² − 1 = 0.1268, i.e. 12.68%. The trap is 12%, the nominal quote itself; 12.36% is the effective rate for half-yearly compounding. In practice: a finance manager compares lease and loan quotes only after converting them to effective annual rates, since a monthly-compounded 12% costs more than an annual 12%.', 'c4', 'moderate', 'round(((1+0.01)**12-1)*100,2)', topic='Effective, nominal and real rates'),
        ]}

    # ---------- MCQs ----------
    mcqs = [
        M('m1', 'Simple interest on ₹15,000 at 8% p.a. for 3 years is:', ['₹3,600', '₹3,895.68', '₹1,200', '₹18,600'], 0, 'Simple interest = P × r × t = 15,000 × 8% × 3 = ₹3,600. Interest is charged on the original principal only, every year. The trap is ₹18,600, which is the amount (principal + interest), not the interest; ₹3,895.68 is compound interest, where interest also earns interest. In practice: many personal loans between relatives and some trade-credit arrangements in India still charge simple interest, and a CA computes interest income on them exactly this way for the income-tax return.', 'c2', 'core', '15000*0.08*3', topic='Simple interest'),
        M('m2', 'At what rate of simple interest does a sum double in 8 years?', ['12.5%', '8%', '9.05%', '25%'], 0, "A sum doubles when the interest equals the principal. Under simple interest, P × r × 8 = P, so r = 1/8 = 12.5% a year. The trap is 9.05%, which is the compound-interest rate that doubles money in 8 years; 8% simply copies the number of years. In practice: older 'money-doubling' deposit schemes in India were advertised this way, and an adviser must check whether the return is simple or compound.", 'c2', 'core', '100/8', topic='Simple interest'),
        M('m3', 'A sum doubles in 6 years at simple interest. In how many years will it become three times?', ['12 years', '9 years', '18 years', '10 years'], 0, 'Doubling in 6 years means simple interest equal to P accrues in 6 years. To become three times, the interest must be 2P, which takes 2 × 6 = 12 years, since simple interest grows in a straight line. The trap is 18 years, which multiplies 6 by 3 — but the original principal already counts as one of the three times. In practice: this linear growth is why simple-interest deposits fall well behind compounded ones over long horizons, a point financial planners stress to clients.', 'c2', 'moderate', '6*2', topic='Simple interest'),
        M('m4', 'Compound interest on ₹10,000 at 10% p.a. for 2 years (annual compounding) is:', ['₹2,100', '₹2,000', '₹12,100', '₹2,050'], 0, "Compound interest = P[(1 + i)ⁿ − 1] = 10,000 × (1.21 − 1) = ₹2,100: ₹1,000 in year 1 plus ₹1,100 in year 2, because year-2 interest is charged on ₹11,000. The trap is ₹2,000, which is simple interest; ₹12,100 is the amount, not the interest. In practice: bank fixed deposits in India compound interest (typically quarterly), so the depositor's interest grows each period as this calculation shows.", 'c3', 'core', '10000*(1.1**2-1)', topic='Compound interest and conversion period'),
        M('m5', 'The amount of ₹50,000 after 1 year at 8% p.a. compounded half-yearly is:', ['₹54,080', '₹54,000', '₹58,320', '₹54,121.61'], 0, "For half-yearly compounding, use half the rate per period and twice the periods: i = 8%/2 = 4%, n = 2. Amount = 50,000 × (1.04)² = ₹54,080. The trap is ₹54,000, which ignores compounding within the year; ₹54,121.61 uses quarterly compounding (2% for 4 periods). In practice: many Indian bonds and some savings instruments pay or compound interest half-yearly, so the conversion period must match the product's terms.", 'c3', 'core', '50000*1.04**2', topic='Compound interest and conversion period'),
        M('m6', 'The difference between CI and SI on ₹40,000 for 2 years at 5% p.a. is:', ['₹100', '₹200', '₹4,100', '₹50'], 0, "For 2 years, CI − SI = P × r², because the only extra is interest on the first year's interest. So 40,000 × (0.05)² = ₹100. Check: CI = ₹4,100 and SI = ₹4,000. The trap is ₹4,100, which is the compound interest itself, not the difference. In practice: this small 'interest on interest' gap widens rapidly over time, which is why borrowers should check whether a loan quote is simple or compound.", 'c3', 'moderate', '40000*0.05**2', topic='Compound interest and conversion period'),
        M('m7', 'The effective rate corresponding to a nominal 12% p.a. compounded monthly is:', ['12.68%', '12%', '12.36%', '12.55%'], 0, 'Effective rate = (1 + i/m)ᵐ − 1 = (1.01)¹² − 1 = 0.1268, i.e. 12.68%. Monthly compounding adds interest on interest within the year. The trap is 12%, which is the nominal rate itself; 12.36% is the effective rate for half-yearly compounding. In practice: credit-card and NBFC loans often quote monthly rates, and a CA converts them to an effective annual rate to compare offers fairly.', 'c4', 'moderate', 'round((1.01**12-1)*100,2)', topic='Effective, nominal and real rates'),
        M('m8', 'The effective rate corresponding to a nominal 8% p.a. compounded quarterly is:', ['8.24%', '8.16%', '8%', '8.32%'], 0, 'Quarterly compounding at 8% means 2% per quarter for 4 quarters. Effective rate = (1.02)⁴ − 1 = 0.0824, i.e. 8.24%. The trap is 8.16%, which is the effective rate for half-yearly compounding (1.04² − 1); 8% ignores compounding entirely. In practice: bank FDs in India typically compound quarterly, so the effective yield a depositor earns is slightly above the quoted rate.', 'c4', 'moderate', 'round((1.02**4-1)*100,2)', topic='Effective, nominal and real rates'),
        M('m9', 'A machine costing ₹1,00,000 depreciates at 10% p.a. on the reducing balance. Its value after 2 years is:', ['₹81,000', '₹80,000', '₹90,000', '₹1,21,000'], 0, 'Reducing-balance depreciation works like compound interest with a negative rate: value = 1,00,000 × (1 − 0.10)² = ₹81,000 (₹90,000 after year 1, then 10% of that). The trap is ₹80,000, which deducts ₹10,000 each year as in the straight-line method. In practice: the written-down value method of the Income-tax Act applies a fixed percentage to the falling block value in the same way.', 'c3', 'core', '100000*0.9**2', topic='Compound interest and conversion period'),
        M('m10', 'A town of 2,00,000 people grows at 2% a year. Its population after 3 years (nearest whole number) is:', ['2,12,242', '2,12,000', '2,08,080', '2,16,486'], 0, 'Population grows like compound interest: 2,00,000 × (1.02)³ = 2,12,241.6, which rounds to 2,12,242. The trap is 2,12,000, which adds 2% of the original each year (simple growth); 2,08,080 stops after 2 years. In practice: municipal planners and FMCG demand forecasters project population and household numbers with exactly this compound-growth formula.', 'c3', 'moderate', 'round(200000*1.02**3)', topic='Compound interest and conversion period'),
        M('m11', 'The annual rate (compounded annually) at which money doubles in 5 years is about:', ['14.87%', '20%', '15.87%', '12.25%'], 0, "Set (1 + i)⁵ = 2, so i = 2^(1/5) − 1 = 0.1487, i.e. about 14.87%. The trap is 20%, which is the simple-interest answer (100%/5); 15.87% adds a percentage point by mistake. The 'rule of 72' check gives 72/5 ≈ 14.4%, close to the exact figure. In practice: advisers use this to tell a client what annual return is needed to double a lump sum before, say, a child's college admission.", 'c3', 'hard', 'round((2**(1/5)-1)*100,2)', topic='Compound interest and conversion period'),
        M('m12', 'The future value of an annuity due equals the future value of the corresponding annuity regular:', ['Multiplied by (1 + i)', 'Divided by (1 + i)', 'Plus one payment', 'Minus one payment'], 0, "In an annuity due, each payment is made at the start of the period, so every payment earns interest for one extra period compared with a regular annuity. Hence FV(due) = FV(regular) × (1 + i). The trap is 'plus one payment' — that adds one cash flow rather than one period's interest on all of them. In practice: SIPs debited at the start of each month and rent paid in advance are annuities due, worth more than end-of-period equivalents.", 'c5', 'core', topic='Annuities — regular and due; future value; sinking fund'),
        M('m13', 'The future value of ₹5,000 paid at the end of each year for 3 years at 10% p.a. is:', ['₹16,550', '₹15,000', '₹18,205', '₹16,500'], 0, 'FV of a regular annuity = R × [(1 + i)ⁿ − 1]/i = 5,000 × 3.31 = ₹16,550. The payments grow to 6,050 + 5,500 + 5,000. The trap is ₹15,000, which simply adds the three payments and ignores interest; ₹18,205 is the annuity-due value. In practice: this is how one projects the maturity value of a recurring deposit or annual PPF contributions made at year-end.', 'c5', 'core', f'5000*{eA(3, 0.1)}', topic='Annuities — regular and due; future value; sinking fund'),
        M('m14', 'If the ₹5,000 in the previous question were paid at the beginning of each year, the future value would be:', ['₹18,205', '₹16,550', '₹16,640', '₹15,045'], 0, "When payments are made at the beginning of each year, each earns one extra year's interest: FV(due) = 16,550 × 1.10 = ₹18,205. The trap is ₹16,550, which is the regular (end-of-year) annuity value from the previous question. In practice: an investor who deposits in PPF early in April rather than at year-end earns this extra year of interest — a tip many CAs give clients.", 'c5', 'moderate', f'5000*{eA(3, 0.1)}*1.1', topic='Annuities — regular and due; future value; sinking fund'),
        M('m15', 'The present value of ₹10,000 received at the end of each year for 3 years at 10% is:', ['₹24,868.52', '₹27,355.37', '₹30,000', '₹33,100'], 0, 'PV of a regular annuity = R × [1 − (1 + i)⁻ⁿ]/i = 10,000 × 2.48685 = ₹24,868.52. Each receipt is discounted for 1, 2 and 3 years. The trap is ₹30,000, which ignores the time value of money; ₹27,355.37 is the value if receipts came at the start of each year. In practice: valuers and lenders discount expected rents or instalments this way to find what a stream of future receipts is worth today.', 'c6', 'core', f'round(10000*{eP(3, 0.1)},2)', topic='Present value of annuities; loan amortisation (EMI)'),
        M('m16', 'The present value of ₹10,000 received at the beginning of each year for 3 years at 10% is:', ['₹27,355.37', '₹24,868.52', '₹22,607.75', '₹30,000'], 0, 'With receipts at the start of each year, the first is not discounted: PV = 10,000 × [1 + P(2, 0.10)] = 10,000 × 2.73554 = ₹27,355.37 (equivalently the regular PV × 1.10). The trap is ₹24,868.52, which is the end-of-year (regular annuity) value. In practice: lease rentals and insurance premiums payable in advance are annuities due, and an accountant valuing them must use this higher present value.', 'c6', 'moderate', f'round(10000*(1+{eP(2, 0.1)}),2)', topic='Present value of annuities; loan amortisation (EMI)'),
        M('m17', 'How much must be invested at the end of each year at 10% p.a. to accumulate ₹1,00,000 in 4 years?', ['₹21,547.08', '₹25,000', '₹31,547.08', '₹19,588.25'], 0,
          'A sinking fund builds up a future sum: deposit = target ÷ A(4, 0.10) = 1,00,000 ÷ 4.641 = ₹21,547.08. The trap is ₹31,547.08, which divides by the present-value factor and gives the instalment to repay a ₹1,00,000 loan — a different problem; ₹25,000 ignores interest. In practice: companies set aside sinking-fund deposits to redeem debentures or replace machinery on a known future date.', 'c5', 'moderate', f'round(100000/{eA(4, 0.1)},2)', topic='Annuities — regular and due; future value; sinking fund'),
        M('m18', 'The present value of a perpetuity of ₹12,000 a year at 8% is:', ['₹1,50,000', '₹96,000', '₹1,62,000', '₹1,20,000'], 0, "A perpetuity pays forever, so its present value is R/i = 12,000/0.08 = ₹1,50,000. The trap is ₹96,000, which multiplies by the rate instead of dividing; ₹1,62,000 adds a year's payment to the right answer. In practice: an endowment that must pay a ₹12,000 scholarship every year forever needs a corpus of ₹1,50,000 invested at 8% — exactly how trusts size such funds.", 'c8', 'core', '12000/0.08', topic='Perpetuities — level and growing'),
        M('m19', 'A cash flow of ₹5,000 next year grows at 4% a year forever. At a 9% discount rate its present value is:', ['₹1,00,000', '₹55,556', '₹38,462', '₹1,25,000'], 0, "A growing perpetuity is valued at R/(i − g), where R is next year's cash flow: 5,000/(0.09 − 0.04) = 5,000/0.05 = ₹1,00,000. The trap is ₹55,556, which ignores growth (5,000/0.09); ₹38,462 adds g to i. In practice: equity analysts value a stable company's dividend stream with this formula (the Gordon growth model), and it requires the discount rate to exceed the growth rate.", 'c8', 'moderate', '5000/(0.09-0.04)', topic='Perpetuities — level and growing'),
        M('m20', 'The present value of ₹1 receivable after n years at rate i (compounded annually) is:', ['(1 + i)⁻ⁿ', '(1 + i)ⁿ', '1 + ni', '1/(1 + ni)'], 0, "Compounding ₹1 for n years gives (1 + i)ⁿ, so to find today's value of ₹1 received after n years we reverse it: PV = 1/(1 + i)ⁿ = (1 + i)⁻ⁿ. The trap is (1 + i)ⁿ, which is the future value, not the present value; 1/(1 + ni) is the simple-interest discount. In practice: every discounted cash-flow valuation, from bond pricing to project appraisal, is built from this discount factor.", 'c6', 'core', topic='Present value of annuities; loan amortisation (EMI)'),
        M('m21', 'Under the NPV technique, a project should be accepted when:', ['NPV is greater than zero', 'NPV is less than zero', 'PV of inflows is less than PV of outflows', 'The payback period is longest'], 0, "NPV = present value of inflows − present value of outflows, discounted at the cost of capital. A positive NPV means the project earns more than that cost and adds value, so it should be accepted. The trap is 'PV of inflows is less than PV of outflows', which describes a negative NPV — a project to reject. In practice: Indian companies use NPV in capital budgeting for new plants or machinery, and lenders often ask for the NPV workings in project reports.", 'c9', 'core', topic='Net present value (NPV) technique'),
        M('m22', 'If the nominal rate of return is 10% and inflation is 6%, the real rate of return (as used in the study material) is:', ['4%', '16%', '1.67%', '6%'], 0, 'As used in the study material, real rate ≈ nominal rate − inflation = 10% − 6% = 4%: it shows the growth in purchasing power after inflation. (The exact Fisher figure, 1.10/1.06 − 1, is about 3.77%.) The trap is 16%, which adds inflation instead of subtracting it; 1.67% divides the two rates. In practice: a 7% FD in a year of 6% CPI inflation leaves the saver barely 1% better off in real terms — before tax.', 'c4', 'core', topic='Effective, nominal and real rates'),
        M('m23', 'Revenue rises from ₹100 crore to ₹144 crore in 2 years. The CAGR is:', ['20%', '22%', '44%', '12%'], 0, "CAGR = (ending/beginning)^(1/n) − 1 = (144/100)^(1/2) − 1 = 1.2 − 1 = 20%. Check: 100 × 1.2 × 1.2 = 144. The trap is 22%, the simple average (44% ÷ 2), which ignores compounding; 44% is the total growth. In practice: listed companies' annual reports and equity research notes quote revenue and profit growth as CAGR, so analysts compute it this way.", 'c10', 'moderate', '((144/100)**0.5-1)*100', topic='Compound annual growth rate (CAGR) and rate of return'),
        M('m24', 'A zero-coupon bond pays ₹1,000 after 2 years. If the required yield is 10%, its price today is:', ['₹826.45', '₹800', '₹909.09', '₹1,210'], 0, 'A zero-coupon bond pays only the face value at maturity, so its price is the present value: 1,000 × (1.1)⁻² = 1,000/1.21 = ₹826.45. The trap is ₹800, which uses simple discounting (deducting 10% twice); ₹909.09 discounts for only one year. In practice: RBI Treasury Bills are zero-coupon instruments sold at a discount, priced exactly this way.', 'c7', 'moderate', 'round(1000*1.1**(-2),2)', topic='Applications: leasing, capital expenditure, bond valuation'),
        M('m25', 'A lessor finds that the present value of lease rentals exceeds the cost of the asset. The lease is:', ['Favourable to the lessor', 'Unfavourable to the lessor', 'Favourable to the lessee', 'Neither — PV is irrelevant'], 0, "If the present value of the lease rentals exceeds the cost of the asset, the lessor recovers more than the outlay in today's money, so the lease is favourable to the lessor. The trap is 'favourable to the lessee' — the lessee would pay more, in present-value terms, than buying the asset outright. In practice: leasing companies and NBFCs in India set rentals using this present-value test before quoting a lease.", 'c7', 'core', topic='Applications: leasing, capital expenditure, bond valuation'),
        M('m26', 'Which of the following is NOT a reason why lenders charge interest?', ['The going-concern assumption', 'Time value of money', 'Liquidity preference', 'Risk of default'], 0, "Interest is charged because of the time value of money, opportunity cost, inflation, liquidity preference and the risk of default. The going-concern assumption is an accounting concept — that a business will continue in the foreseeable future — and has nothing to do with why interest is charged. The tempting wrong pick is liquidity preference, which sounds technical but is a genuine reason. In practice: a bank's lending rate is built from these components, with a risk premium for weaker borrowers.", 'c1', 'core', topic='Interest — why it is charged and the basic terms'),
        M('m27', 'For a nominal rate of 12% p.a. compounded quarterly over 3 years, the rate per period and the number of periods are:', ['3% and 12', '4% and 9', '12% and 3', '3% and 4'], 0, "Divide the nominal rate by the number of conversions a year and multiply the years by it: i = 12%/4 = 3% per quarter, and n = 3 × 4 = 12 quarters. The trap is '3% and 4', which converts the rate but forgets to convert the time; '12% and 3' ignores quarterly compounding altogether. In practice: bank FD maturity calculators in India apply exactly this quarterly rate-and-period conversion.", 'c3', 'core', topic='Compound interest and conversion period'),
        M('m28', 'A loan of ₹1,00,000 at 10% p.a. is repaid in 2 equal annual instalments (end of year). Each instalment is:', ['₹57,619.05', '₹55,000', '₹60,500', '₹47,619.05'], 0, 'An equal instalment (EMI-type) repayment = loan ÷ P(2, 0.10) = 1,00,000 ÷ 1.73554 = ₹57,619.05. Each instalment covers the interest due plus part of the principal. The trap is ₹55,000, which adds simple interest of one year to half the loan; ₹60,500 uses 1.1² on half. In practice: home-loan and car-loan EMIs in India are calculated on exactly this present-value-of-annuity basis.', 'c6', 'moderate', f'round(100000/{eP(2, 0.1)},2)', topic='Present value of annuities; loan amortisation (EMI)'),
        M('m29', 'Given log 2 = 0.3010 and log 1.08 = 0.0334, the time for money to double at 8% p.a. compound interest is about:', ['9.01 years', '12.5 years', '8 years', '10.8 years'], 0, 'Set (1.08)ⁿ = 2 and take logs: n = log 2/log 1.08 = 0.3010/0.0334 ≈ 9.01 years. The trap is 12.5 years, which is the simple-interest doubling time (100%/8%). The rule of 72 gives 72/8 = 9 years — a quick check. In practice: advisers use doubling-time estimates to explain to clients how long a long-term investment such as an equity fund or PPF may take to double.', 'c3', 'hard', 'round(0.3010/0.0334,2)', topic='Compound interest and conversion period'),
        M('m30', '₹20,000 grows to ₹23,328 in 2 years with annual compounding. The rate of interest is:', ['8%', '8.32%', '16.64%', '7.5%'], 0, '(1 + i)² = 23,328/20,000 = 1.1664, so 1 + i = √1.1664 = 1.08 and i = 8%. Check: 20,000 × 1.08² = 23,328. The trap is 8.32%, which divides total growth (16.64%) by 2 — a simple-interest rate. In practice: finding the implied compound rate from start and end values is how an investor checks the real return on a maturity payout from an insurance or deposit scheme.', 'c3', 'moderate', '((23328/20000)**0.5-1)*100', topic='Compound interest and conversion period'),
    ]
    # independent checks of the distractor logic quoted in explanations
    assert abs(15000 * (1.08 ** 3 - 1) - 3895.68) < 0.01 and abs((2 ** (1 / 8) - 1) * 100 - 9.05) < 0.01
    assert abs(50000 * 1.02 ** 4 - 54121.61) < 0.01 and abs(((1.06 ** 2) - 1) * 100 - 12.36) < 0.01
    assert abs(100000 / ev(eP(4, 0.1)) - 31547.08) < 0.01

    unit = {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch04', 'n': 1, 'title': 'Mathematics of Finance',
        'outcomes': ['Explain why interest is charged and compute simple interest, compound interest (any conversion period), depreciation and growth.',
                     'Distinguish nominal, effective and real rates and compute the effective rate of interest.',
                     'Compute future and present values of annuities regular and annuities due, sinking-fund deposits and loan instalments (EMIs).',
                     'Apply present value to leasing, capital expenditure (NPV) and bond valuation, value level and growing perpetuities, and compute CAGR.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 100, 'practice': 120}, 'prereq': ['fnd-p3-ch01-u01'],
                 'exam_tip': 'Learn A(n, i) and P(n, i) by heart and always decide first whether payments are at the end (regular) or at the beginning (due) of each period. Convert the rate and the number of periods to the compounding period before using any formula.'},
        'concepts': [
            {'id': 'c1', 'title': 'Interest — why it is charged and the basic terms',
             'body': ['Interest is the price a borrower pays for using someone else’s money. Lenders charge it because of: time value of money (a rupee today is worth more than a rupee later); opportunity cost (lending gives up other uses of the money); inflation (money loses purchasing power); liquidity preference (people prefer cash in hand); and risk (the borrower may default — riskier borrowers pay a risk premium).',
                      'Principal (P): the sum borrowed or invested. Rate of interest: the charge per ₹100 per period, usually per annum. Accumulated amount (A): principal plus interest at the end of the term.'],
             'analogy': 'Interest is rent for money — just as you pay rent to use someone’s flat, you pay interest to use someone’s rupees.',
             'work': 'Every lending, deposit, lease and valuation file a CA reviews starts from these five reasons — they explain why one borrower pays 9% and another 14%.'},
            {'id': 'c2', 'title': 'Simple interest',
             'body': ['Simple interest is calculated on the original principal only: I = P × n × r (r as a decimal, n in years); A = P(1 + nr).',
                      'Rearranged: P = I/(nr), r = I/(Pn), n = I/(Pr). Time in months or days must be converted to years (e.g. 9 months = 0.75 year).',
                      'A sum becomes k times when interest = (k − 1)P, so n × r = k − 1. If it doubles in t years at SI, it triples in 2t years.'],
             'analogy': 'Simple interest is a fixed salary — the same amount every year, no matter how long you work.',
             'work': 'Interest on delayed payments, many short-term advances and statutory interest calculations follow simple interest.'},
            {'id': 'c3', 'title': 'Compound interest and conversion period',
             'body': ['In compound interest, interest is added to the principal at the end of each conversion period, so later interest is earned on earlier interest. A = P(1 + i)ⁿ and CI = A − P, where i = rate per conversion period and n = number of conversion periods.',
                      'Conversion period: annual (m = 1), half-yearly (m = 2), quarterly (m = 4), monthly (m = 12). For a nominal annual rate r compounded m times a year for t years: i = r/m and n = mt.',
                      'For two years, CI − SI = P r². For n = 1 conversion period CI = SI.',
                      'Same formula, other uses: depreciation on reducing balance V = P(1 − r)ⁿ; population or sales growth A = P(1 + r)ⁿ. When the unknown is n, use logarithms: n = log(A/P)/log(1 + i).'],
             'analogy': 'Compound interest is a snowball rolling downhill — it picks up snow on the snow it already carries.',
             'work': 'Fixed-deposit maturity values, loan balances, depreciation under the written-down value method and growth projections in business plans are all compound-interest calculations.'},
            {'id': 'c4', 'title': 'Effective, nominal and real rates',
             'body': ['The nominal (stated) rate is the annual rate quoted, ignoring how often interest is compounded.',
                      'The effective rate is the actual annual rate earned when interest is compounded more than once a year: E = (1 + r/m)ᵐ − 1. It is higher than the nominal rate whenever m > 1 and does not depend on the principal.',
                      'The real rate adjusts the nominal rate for inflation. The study material uses: real rate = nominal rate − inflation (so nominal = real + inflation). (The exact relation is (1 + nominal) = (1 + real)(1 + inflation), which gives a slightly lower real rate.)',
                      'Comparing offers: convert every quoted rate to its effective rate first. Lenders tend to advertise the nominal rate on loans; deposit schemes tend to advertise the effective yield.'],
             'analogy': 'The nominal rate is the price on the menu; the effective rate is the bill after service charges; the real rate is what that bill is worth after prices rise.',
             'work': 'When a client compares a bank loan at 10.5% monthly rests with another at 10.7% half-yearly, the effective rate settles which is cheaper.'},
            {'id': 'c5', 'title': 'Annuities — regular and due; future value; sinking fund',
             'body': ['An annuity is a series of equal payments (or receipts) made at equal intervals. In an annuity regular (ordinary annuity) each payment is at the end of the period; in an annuity due each payment is at the beginning. (Read every question for when the first payment falls — terminology differs between books.)',
                      'Future value of an annuity regular: FV = A × A(n, i), where A(n, i) = [(1 + i)ⁿ − 1]/i.',
                      'Future value of an annuity due = A × A(n, i) × (1 + i), because each payment earns one extra period of interest.',
                      'A sinking fund is money set aside by equal periodic deposits to build up a known sum at a future date (e.g. to replace an asset or repay debentures). Deposit = target ÷ A(n, i).'],
             'analogy': 'An annuity is a SIP: equal instalments at equal gaps. Paying at the start of each month (due) simply gives every instalment one more month to grow.',
             'work': 'Debenture redemption funds, asset replacement funds and retirement corpus planning are sinking-fund calculations.'},
            {'id': 'c6', 'title': 'Present value of annuities; loan amortisation (EMI)',
             'body': ['Present value of ₹1 due after n periods = (1 + i)⁻ⁿ (the discount factor).',
                      'Present value of an annuity regular: PV = A × P(n, i), where P(n, i) = [1 − (1 + i)⁻ⁿ]/i.',
                      'Present value of an annuity due = A × [1 + P(n − 1, i)] = A × P(n, i) × (1 + i): the first payment is already at today’s value.',
                      'A loan is amortised when equal instalments repay both interest and principal over its term. Instalment = Loan ÷ P(n, i). In each period, interest = rate × opening balance; principal repaid = instalment − interest. The interest part falls and the principal part rises over time.'],
             'analogy': 'Present value is looking at the future through the wrong end of a telescope — everything looks smaller, and the further away it is, the smaller it looks.',
             'work': 'EMI schedules, interest-versus-principal split for income-tax claims and the valuation of rental streams all use P(n, i).'},
            {'id': 'c7', 'title': 'Applications: leasing, capital expenditure, bond valuation',
             'body': ['Leasing: the owner (lessor) lets the user (lessee) use an asset for a period in return for lease rentals. For the lessor, compare the PV of rentals with the cost of the asset — a higher PV makes the lease favourable. For the lessee, compare the PV of rentals with the purchase price — a lower PV makes leasing preferable.',
                      'Capital expenditure (investment decision): compare the PV of the expected cash inflows with the PV of the outflows; invest if inflows are worth more.',
                      'Bond valuation: a bond’s value is the PV of its coupon payments (an annuity) plus the PV of the redemption amount, discounted at the investor’s required yield. If the yield is above the coupon rate, the bond sells below face value (at a discount), and vice versa.'],
             'analogy': 'All three questions are the same question in different clothes: "Is the stream of future rupees worth more than the rupees I give up today?"',
             'work': 'Lease-versus-buy advice, capital-budgeting proposals and investment valuation (including Ind AS fair-value work later in the course) use exactly this present-value logic.'},
            {'id': 'c8', 'title': 'Perpetuities — level and growing',
             'body': ['A perpetuity is an annuity whose payments continue for ever. Its future value cannot be computed, but its present value is finite, and because the capital itself is never paid back, nothing is added for a principal repayment.',
                      'Level perpetuity (payments at the end of each period): PV = R/i. If the first payment is made today (perpetuity due), PV = R/i + R.',
                      'Growing perpetuity (first payment R one period from now, growing at g per period, with g < i): PV = R/(i − g).',
                      'Rate and payment must match the period: monthly payments need a monthly rate.'],
             'analogy': 'A perpetuity is a fruit tree that never stops bearing: you pay for the tree, not for an infinite pile of fruit.',
             'work': 'Endowment funds, preference shares without a redemption date and the terminal value in business valuation use the perpetuity formulas.'},
            {'id': 'c9', 'title': 'Net present value (NPV) technique',
             'body': ['NPV is a discounted cash-flow method: all cash flows of a project are brought to their value at time 0 using a chosen discount rate, and the outflows are subtracted from the inflows.',
                      'NPV = PV of cash inflows − PV of cash outflows (when there is a single initial outlay: PV of net inflows − initial investment).',
                      'Discount rate: ideally the return available on the best alternative investment of the same risk; in practice organisations use a minimum required rate or the weighted average cost of capital (WACC).',
                      'Steps: estimate net cash flow each year → choose the rate → find the discount factor (1 + i)⁻ᵗ for each year → multiply → add. Decision: NPV > 0 accept; NPV < 0 reject.'],
             'analogy': 'NPV is a profit figure measured in "today’s rupees" after paying the investors their required return.',
             'work': 'Capital-budgeting proposals in companies and project-finance appraisals by banks are judged on NPV.'},
            {'id': 'c10', 'title': 'Compound annual growth rate (CAGR) and rate of return',
             'body': ['CAGR is the constant annual rate that would take a value from its beginning level V₀ to its ending level Vₙ over n years: CAGR = (Vₙ/V₀)^(1/n) − 1.',
                      'It smooths out year-to-year swings, so it is preferred to the simple average of yearly growth rates when comparing investments or business metrics (revenue, users, units).',
                      'Calculating the rate of return on past investments helps judge how good the investment decisions were and whether to change strategy.'],
             'analogy': 'CAGR is the steady speed that would have covered the same distance in the same time, however bumpy the actual drive was.',
             'work': 'Analysts and CAs quote revenue and profit CAGRs in project reports, valuation notes and equity research.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Simple interest: amount and rate', 'difficulty': 'core', 'minutes': 3,
             'q': '(a) Find the simple interest and amount on ₹48,000 at 9% p.a. for 2 years 6 months. (b) At what rate of simple interest will a sum become three times itself in 16 years?',
             'solution': [p(f'(a) n = 2.5 years. I = 48,000 × 0.09 × 2.5 = {Rs(si1)}; A = 48,000 + 10,800 = {Rs(a1)}.'),
                          p(f'(b) Tripling means interest = 2P. 2P = P × 16 × r → r = 2/16 = 0.125 = {num(r1)}% p.a.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Compound interest with different conversion periods', 'difficulty': 'core', 'minutes': 6,
             'q': 'Find the amount and compound interest on ₹80,000 for 2 years at 12% p.a. when interest is compounded annually, half-yearly, quarterly and monthly.',
             'solution': [p('Use A = P(1 + i)ⁿ with i = 12%/m and n = 2m.'), t2,
                          note('The more frequent the compounding, the larger the amount — but the gain shrinks each time the frequency rises.')],
             'checks': c2},
            {'id': 'i3', 'title': 'CI − SI shortcut and reducing-balance depreciation', 'difficulty': 'core', 'minutes': 4,
             'q': '(a) Find the difference between CI and SI on ₹2,50,000 for 2 years at 8% p.a. (b) A machine costing ₹5,00,000 depreciates at 15% p.a. on the reducing balance. Find its value after 3 years.',
             'solution': [p(f'(a) CI = 2,50,000(1.08² − 1) = ₹41,600; SI = 2,50,000 × 0.08 × 2 = ₹40,000. Difference = {Rs(d3)}. Shortcut: P r² = 2,50,000 × 0.0064 = ₹1,600.'),
                          p(f'(b) V = 5,00,000 × (1 − 0.15)³ = 5,00,000 × 0.614125 = {Rs(w3)}.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Effective rate and real rate', 'difficulty': 'moderate', 'minutes': 4,
             'q': '(a) Which is better for a depositor: 10% p.a. compounded quarterly or 10.2% p.a. compounded half-yearly? (b) A deposit yields 9% while inflation is 5.5%. What is the real rate of return?',
             'solution': [p(f'(a) E₁ = (1 + 0.025)⁴ − 1 = {num(e4q, 4)}%. E₂ = (1 + 0.051)² − 1 = {num(e4h, 4)}%.'),
                          p('The 10.2% half-yearly option has the higher effective rate, so it is better for the depositor, even though it compounds less often.'),
                          p(f'(b) Real rate = 9% − 5.5% = {num(rr)}% (the relation used in the study material).')],
             'checks': c4},
            {'id': 'i5', 'title': 'Future value of an annuity regular and an annuity due', 'difficulty': 'core', 'minutes': 4,
             'q': 'Kavita deposits ₹20,000 a year for 5 years in a scheme paying 8% p.a. compounded annually. Find the amount at the end of 5 years if the deposits are made (a) at the end of each year; (b) at the beginning of each year.',
             'solution': [p(f'A(5, 0.08) = (1.08⁵ − 1)/0.08 = {num(fa5, 5)}.'),
                          p(f'(a) Annuity regular: FV = 20,000 × {num(fa5, 5)} = {Rs(fv5)}.'),
                          p(f'(b) Annuity due: FV = {Rs(fv5)} × 1.08 = {Rs(fvd5)}.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Sinking fund', 'difficulty': 'core', 'minutes': 3,
             'q': 'A company must repay ₹10,00,000 of debentures after 6 years. How much should it invest at the end of each year at 9% p.a. compounded annually?',
             'solution': [p(f'A(6, 0.09) = (1.09⁶ − 1)/0.09 = {num(fa6, 5)}.'),
                          p(f'Annual deposit = 10,00,000 ÷ {num(fa6, 5)} = {Rs(sf6)}.')],
             'checks': c6},
            {'id': 'i7', 'title': 'EMI and amortisation schedule', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'A car loan of ₹6,00,000 at 12% p.a. is to be repaid in 36 equal monthly instalments starting one month from now. Find the EMI and prepare the first two lines of the amortisation schedule.',
             'solution': [p(f'Monthly rate i = 1%, n = 36. P(36, 0.01) = [1 − (1.01)⁻³⁶]/0.01 = {num(pf7, 5)}.'),
                          p(f'EMI = 6,00,000 ÷ {num(pf7, 5)} = {Rs(emi)}.'), sched,
                          note('Interest is always charged on the opening balance of the month; the principal part grows each month.')],
             'checks': c7},
            {'id': 'i8', 'title': 'Present value of an annuity due', 'difficulty': 'moderate', 'minutes': 4,
             'q': 'Office rent of ₹1,20,000 is payable at the beginning of each year for 4 years. Find its present value at 10% p.a.',
             'solution': [p(f'Annuity due for 4 years = first payment today + annuity regular for 3 years. P(3, 0.10) = {num(pf8, 5)}.'),
                          p(f'PV = 1,20,000 × (1 + {num(pf8, 5)}) = {Rs(pvd8)}.'),
                          note('Cross-check: 1,20,000 × P(4, 0.10) × 1.10 gives the same answer.')],
             'checks': c8},
            {'id': 'i9', 'title': 'Leasing and a capital-expenditure decision', 'difficulty': 'moderate', 'minutes': 6,
             'q': '(a) Sunrise Leasing buys equipment for ₹5,00,000 and leases it for 5 years at ₹1,40,000 a year, payable at the end of each year. Its money earns 12% p.a. Is the lease favourable to Sunrise? (b) A machine costing ₹2,00,000 will contribute ₹55,000 at the end of each year for 5 years. Borrowing costs 11% p.a. Should it be bought?',
             'solution': [p(f'(a) PV of rentals = 1,40,000 × P(5, 0.12) = 1,40,000 × {num(pf9, 5)} = {Rs(pvl)}. This exceeds the cost of ₹5,00,000, so the lease is favourable to the lessor (only just).'),
                          p(f'(b) PV of contributions = 55,000 × P(5, 0.11) = 55,000 × {num(pf9b, 5)} = {Rs(pvc)}. This exceeds ₹2,00,000, so the machine should be bought.')],
             'checks': c9},
            {'id': 'i10', 'title': 'Valuing a bond', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'A ₹1,000 bond pays a 9% coupon at the end of each year and is redeemed at par after 4 years. What price should an investor pay if she requires a yield of 11%?',
             'solution': [p(f'PV of coupons = 90 × P(4, 0.11) = 90 × {num(pf10, 5)} = {Rs(pvcpn)}.'),
                          p(f'PV of redemption = 1,000 × (1.11)⁻⁴ = {Rs(pvred)}.'),
                          p(f'Value = {Rs(pvcpn)} + {Rs(pvred)} = {Rs(bond)} — below par, because the required yield (11%) is above the coupon rate (9%).')],
             'checks': c10},
            {'id': 'i11', 'title': 'Perpetuities', 'difficulty': 'core', 'minutes': 4,
             'q': 'At 8% p.a., value (a) ₹60,000 a year for ever, first payment after one year; (b) the same with the first payment today. (c) At 12%, value ₹40,000 next year growing at 5% a year for ever.',
             'solution': [p(f'(a) PV = 60,000/0.08 = {Rs(pp)}.'), p(f'(b) Perpetuity due = 7,50,000 + 60,000 = {Rs(ppd)}.'), p(f'(c) Growing perpetuity = 40,000/(0.12 − 0.05) = {Rs(gp)}.')],
             'checks': c11},
            {'id': 'i12', 'title': 'Net present value of a project', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'A project costs ₹3,00,000 now and will return ₹1,20,000, ₹1,50,000 and ₹1,00,000 at the end of years 1, 2 and 3. The cost of capital is 12% (PV factors 0.893, 0.797, 0.712). Find the NPV and advise.',
             'solution': [npvt, p(f'NPV = {Rs(npv)}, which is negative: the project earns less than 12%, so it should be rejected — even though the undiscounted inflows (₹3,70,000) exceed the cost.')],
             'checks': c12},
            {'id': 'i13', 'title': 'CAGR of revenue', 'difficulty': 'core', 'minutes': 3,
             'q': 'A company’s revenue grew from ₹40 crore in 2022 to ₹58.564 crore in 2026. Find the CAGR.',
             'solution': [p('n = 2026 − 2022 = 4 years. CAGR = (58.564/40)^(1/4) − 1 = (1.4641)^(1/4) − 1.'),
                          p(f'1.4641 = 1.1⁴, so CAGR = 1.1 − 1 = {num(cg)}% a year.')],
             'checks': c13},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Comparing two loan offers', 'role': 'CA advising a small manufacturer',
             'situation': 'Bank A offers a term loan at 10.5% p.a. with monthly rests; Bank B offers 10.7% p.a. with half-yearly rests. The client assumes Bank A is cheaper because its quoted rate is lower.',
             'steps': [f'Effective rate A = (1 + 0.105/12)¹² − 1 = {num(ea)}%.', f'Effective rate B = (1 + 0.107/2)² − 1 = {num(eb)}%.',
                       'Bank B is actually slightly cheaper: Bank A’s lower quoted rate is more than offset by monthly compounding.', 'Also compare processing fees and prepayment charges before recommending.'],
             'takeaway': 'Always compare loans on effective, not nominal, rates — the lower quoted rate is not always the cheaper loan.', 'think': 'Why does monthly compounding raise the effective cost of Bank A’s loan?',
             'answer': 'Interest is added to the balance every month, so interest is charged on interest twelve times a year.', 'checks': j1c},
            {'id': 'j2', 'title': 'Lease or buy office equipment', 'role': 'Finance manager in a services company',
             'situation': 'A server room upgrade costs ₹40,00,000 to buy, or can be leased for ₹12,50,000 a year for 4 years, payable at year-end. The company can borrow at 10%.',
             'steps': ['Treat the rentals as an annuity regular: PV = 12,50,000 × P(4, 0.10).', f'PV of rentals = {Rs(pvlease)}.', 'Compare with the purchase price ₹40,00,000: leasing is cheaper in present-value terms.', 'Note qualitative factors — technology obsolescence favours leasing.'],
             'takeaway': 'For the lessee, lease if the PV of rentals is below the purchase price.', 'think': 'What if rentals were payable at the start of each year?',
             'answer': f'Then they form an annuity due: PV = {Rs(pvlease)} × 1.10 = {Rs(round(pvlease * 1.1, 2))}, which is more than ₹40,00,000 — buying becomes cheaper.', 'checks': j2c},
            {'id': 'j3', 'title': 'NPV for a capex proposal', 'role': 'Articled assistant helping in a project report',
             'situation': 'A client plans a ₹10,00,000 packaging line expected to save ₹2,60,000 a year for 6 years. Its cost of capital is 13%.',
             'steps': ['Equal annual savings form an annuity regular: PV = 2,60,000 × P(6, 0.13).', f'PV of savings = {Rs(pvin)}.', f'NPV = {Rs(npvj)} → positive, so the proposal is acceptable.', 'State assumptions (no scrap value, savings at year-end) in the report.'],
             'takeaway': 'With equal yearly inflows, NPV is just one annuity factor minus the outlay.', 'think': 'If the cost of capital rose to 16%, would the answer flip?',
             'answer': 'P(6, 0.16) ≈ 3.6847, so PV ≈ ₹9,58,000 — below the outlay; NPV turns negative and the proposal would be rejected.', 'checks': j3c},
            {'id': 'j4', 'title': 'Funding a debenture redemption', 'role': 'Company accountant',
             'situation': '₹50,00,000 of debentures fall due in 5 years. The board wants equal year-end investments in a fund earning 7%.',
             'steps': ['Target = ₹50,00,000; n = 5; i = 0.07.', f'Annual investment = 50,00,000 ÷ A(5, 0.07) = {Rs(sfj)}.', 'Set up a standing instruction and track the fund balance each year against the schedule.'],
             'takeaway': 'A sinking-fund deposit is a target divided by A(n, i) — not by P(n, i).', 'think': 'Why would using P(n, i) be wrong here?',
             'answer': 'P(n, i) values a stream today (used for loans); here we are building up a future sum, so the future-value factor A(n, i) is needed.', 'checks': j4c},
        ],
        'mcqs': mcqs,
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'A loan of ₹3,00,000 at 10% p.a. is to be repaid in 3 equal annual instalments, the first at the end of the first year. Find the instalment and prepare the complete repayment (amortisation) schedule.',
             'model': [p(f'P(3, 0.10) = [1 − (1.10)⁻³]/0.10 = {num(q1pf, 5)}. Instalment = 3,00,000 ÷ {num(q1pf, 5)} = {Rs(q1e)}.'), q1t,
                       note('The closing balance after year 3 is nil (any paise difference is rounding).')],
             'scheme': [{'id': 's1', 'pt': 'Recognises annuity regular and uses P(3, 0.10)', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Instalment ₹1,20,634.44', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Interest each year on opening balance', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Principal = instalment − interest; closing balance nil', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Neat schedule with headings', 'm': 0.5, 'skill': 'presentation'}],
             'remarks': ['Many candidates compute interest on the original loan every year — interest must be on the opening balance.', 'A closing balance of exactly nil is the best self-check.'],
             'mistakes': ['Dividing by A(3, 0.10) instead of P(3, 0.10).', 'Charging interest on the original ₹3,00,000 in years 2 and 3.'],
             'tips': ['Columns: Year | Opening | Instalment | Interest | Principal | Closing.', 'Carry paise through and round only the final figures.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'An investment of ₹2,00,000 is expected to generate ₹60,000, ₹70,000, ₹80,000 and ₹50,000 at the end of years 1 to 4. The cost of capital is 10% (PV factors 0.909, 0.826, 0.751, 0.683). Compute the NPV and advise.',
             'model': [q2t, p(f'NPV = {Rs(q2n)} > 0, so the investment should be accepted.')],
             'scheme': [{'id': 's1', 'pt': 'Discounts each year’s flow with the right factor', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Totals PV and deducts the outlay correctly', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Decision with reason (NPV > 0)', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Show the year-0 outflow in brackets in the table — it avoids sign errors in the total.'],
             'mistakes': ['Applying the year-1 factor to all years.', 'Forgetting to deduct the initial investment.'],
             'tips': ['Four columns: Year | Cash flow | PV factor | Present value.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
             'q': 'A ₹1,000 debenture carries an 8% coupon payable annually and will be redeemed at ₹1,050 at the end of 5 years. Find its value to an investor who requires 10% p.a.',
             'model': [p(f'Coupon = 8% of face value ₹1,000 = ₹80 a year for 5 years. PV = 80 × P(5, 0.10) = {Rs(q3cp)}.'),
                       p(f'PV of redemption = 1,050 × (1.10)⁻⁵ = {Rs(q3rd)}.'),
                       p(f'Value = {Rs(q3cp)} + {Rs(q3rd)} = {Rs(q3v)}.')],
             'scheme': [{'id': 's1', 'pt': 'Coupon on face value (₹80), treated as annuity', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'PV of coupons', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'PV of redemption at ₹1,050', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Adds to the value', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Coupon is on face value, not on the redemption value — a common slip.'],
             'mistakes': ['Discounting ₹1,000 instead of the redemption amount ₹1,050.', 'Using the coupon rate as the discount rate.'],
             'tips': ['Split the answer into two PVs and add — each line earns a step mark.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['SI = Pnr; A = P(1 + nr).', 'CI: A = P(1 + i)ⁿ with i = r/m and n = mt; CI − SI (2 years) = Pr².',
                        'Effective rate E = (1 + r/m)ᵐ − 1; real ≈ nominal − inflation.',
                        'A(n, i) = [(1 + i)ⁿ − 1]/i; P(n, i) = [1 − (1 + i)⁻ⁿ]/i. Due = regular × (1 + i).',
                        'Sinking fund deposit = target ÷ A(n, i); loan instalment = loan ÷ P(n, i).',
                        'Perpetuity R/i; due R/i + R; growing R/(i − g).',
                        'NPV = PV inflows − PV outflows; accept if positive. CAGR = (Vₙ/V₀)^(1/n) − 1.'],
            'remember': ['Lessor: lease favourable if PV of rentals > cost. Lessee: lease if PV of rentals < purchase price.', 'Bond value = PV of coupons + PV of redemption.', 'Depreciation on reducing balance: P(1 − r)ⁿ.'],
            'traps': ['Using the annual rate with monthly periods.', 'Dividing a sinking-fund target by P(n, i).', 'Treating beginning-of-period payments as an annuity regular.', 'Averaging yearly growth rates instead of computing CAGR.'],
        },
        'quickref': [
            {'k': 'Simple interest', 'v': 'I = Pnr; A = P(1 + nr)'},
            {'k': 'Compound amount', 'v': 'A = P(1 + r/m)^(mt)'},
            {'k': 'CI − SI (2 years)', 'v': 'P r²'},
            {'k': 'Effective rate', 'v': 'E = (1 + r/m)ᵐ − 1'},
            {'k': 'FV annuity regular', 'v': 'A × [(1 + i)ⁿ − 1]/i'},
            {'k': 'PV annuity regular', 'v': 'A × [1 − (1 + i)⁻ⁿ]/i'},
            {'k': 'Annuity due', 'v': 'Regular value × (1 + i)'},
            {'k': 'Perpetuity', 'v': 'R/i; growing R/(i − g)'},
            {'k': 'NPV', 'v': 'PV of inflows − PV of outflows'},
            {'k': 'CAGR', 'v': '(Vₙ/V₀)^(1/n) − 1'},
            {'k': 'Real rate (study material)', 'v': 'Nominal − inflation'},
        ],
        'viva': viva(),
        'cases': [case],
    }
    return unit


def viva():
    return [
        V('v1', 'Why do lenders charge interest? Give the reasons.',
          'Lenders charge interest because of the time value of money, since a rupee today is worth more than a rupee in future; opportunity cost, because they give up other uses of the money; inflation, which reduces purchasing power; liquidity preference, because people prefer to keep cash; and risk, because the borrower may default.',
          [P('p1', 'Time value of money', 2, 'time value'),
           P('p2', 'Opportunity cost', 2, 'opportunity cost|alternative use|other use|forgo|forego|give up other'),
           P('p3', 'Inflation (fall in purchasing power)', 2, 'inflation|purchasing power|price rise|prices rise'),
           P('p4', 'Liquidity preference', 2, 'liquidity|prefer cash|cash in hand|keep cash'),
           P('p5', 'Risk of default', 2, 'risk|default|bankrupt|not repay|not pay back')], 'c1'),
        V('v2', 'What is the difference between simple interest and compound interest?',
          'Simple interest is calculated only on the original principal, so it is the same every year. Compound interest is calculated on the principal plus the interest already added, so interest is earned on interest. For more than one period, compound interest is therefore higher than simple interest.',
          [P('p1', 'SI is on the original principal only', 4, ALT('simple {m} {k}', m=['', 'interest', 'interest calculat', 'interest charg', 'interest comput', 'interest calculat', 'interest paid', 'calculat'], k=['only principal', 'original principal', 'principal only', 'same every year', 'same each year', 'fixed', 'only initial', 'initial principal'])),
           P('p2', 'CI is on principal plus accumulated interest (interest on interest)', 4, ALT('compound {m} {k}', m=['', 'interest', 'interest calculat', 'interest charg', 'interest comput', 'calculat'], k=['interest on interest', 'principal plus interest', 'principal and interest', 'accumulated interest', 'interest added', 'added interest', 'previous interest', 'accumulated amount', 'principal plus accumulated', 'amount'])),
           P('p3', 'CI exceeds SI for more than one period', 2, ALT('compound {m} {k}', m=['', 'interest', 'interest is', 'is', 'therefore', 'interest therefore', 'interest will be'], k=['higher', 'more', 'greater', 'larger', 'exceed', 'bigger']))], 'c3'),
        V('v3', 'Distinguish an annuity regular from an annuity due.',
          'In an annuity regular each payment is made at the end of the period, so the first payment comes at the end of the first period. In an annuity due each payment is made at the beginning of the period, so the first payment is made immediately. The value of an annuity due equals the value of the annuity regular multiplied by one plus i.',
          [P('p1', 'Annuity regular: payments at the end of each period', 4, ALT('regular {x} end', 'ordinary {x} end', 'end {y} regular', x=['', 'payment', 'payments', 'payment at the', 'payments at the', 'paid at the', 'made at the', 'payment is made at the', 'each payment is made at the', 'annuity payment at the'], y=['of period', 'of each period', 'of the period', 'means'])),
           P('p2', 'Annuity due: payments at the beginning of each period', 4, ALT('due {x} {b}', '{b} {y} due', x=['', 'payment', 'payments', 'payment at the', 'payments at the', 'paid at the', 'made at the', 'payment is made at the', 'each payment is made at the', 'annuity payment at the'], b=['beginning', 'start', 'starting', 'immediately', 'in advance'], y=['of period', 'of each period', 'of the period', 'means'])),
           P('p3', 'Due value = regular value × (1 + i)', 2, 'multipli by 1 plus i|multiplied by one plus i|times 1 plus i|times one plus i|into 1 plus i|1 plus i|one plus i|one extra period|extra period|one more period')], 'c5'),
        V('v4', 'What is the effective rate of interest and how is it calculated?',
          'The effective rate is the actual annual rate earned when interest is compounded more than once a year. It equals one plus r by m, raised to the power m, minus one, where r is the nominal annual rate and m is the number of compounding periods in a year. It is higher than the nominal rate whenever compounding is more frequent than yearly, and it does not depend on the principal.',
          [P('p1', 'Actual annual rate when compounding is more than once a year', 4, 'actual|true|real annual|equivalent annual|annual equivalent', 'more than once|several times|more frequent|frequent|half yearly|quarterly|monthly|m times', min=2),
           P('p2', 'E = (1 + r/m)^m − 1', 4, '1 plus r by m|one plus r by m|1 plus r over m|one plus r over m|1 plus r m|one plus r m|r by m|r over m', 'power m|to the m|raised to m|raise to m|to power m|whole power m', 'minus 1|minus one|less one|less 1', min=3),
           P('p3', 'Higher than the nominal rate', 2, 'higher than nominal|more than nominal|greater than nominal|higher than the nominal|more than the nominal|greater than the nominal|exceeds the nominal|exceeds nominal|above the nominal|above nominal')], 'c4'),
        V('v5', 'Explain the net present value technique and its decision rule.',
          'Net present value discounts all the cash flows of a project to their value today, using the cost of capital or required rate of return as the discount rate. NPV equals the present value of cash inflows minus the present value of cash outflows. If NPV is positive the project is accepted; if NPV is negative it is rejected.',
          [P('p1', 'Discount all cash flows to present value at the cost of capital', 3, 'discount|present value|today', 'cost of capital|required rate|desired rate|wacc|discount rate|hurdle rate|rate of return', min=2),
           P('p2', 'NPV = PV of inflows − PV of outflows', 3, 'inflow', 'outflow', 'minus|less|subtract|deduct|difference', min=3),
           P('p3', 'Positive NPV → accept', 2, ALT('{p} {x} accept', 'accept {y} {p}', p=['positive', 'greater than zero', 'more than zero', 'above zero'], x=['', 'then', 'project', 'then project', 'then the project', 'project is', 'we', 'then we', 'is'], y=['if', 'when', 'if npv is', 'when npv is', 'if it is'])),
           P('p4', 'Negative NPV → reject', 2, ALT('{n} {x} reject', 'reject {y} {n}', n=['negative', 'less than zero', 'below zero'], x=['', 'then', 'project', 'then project', 'then the project', 'project is', 'we', 'then we', 'is', 'it is'], y=['if', 'when', 'if npv is', 'when npv is', 'if it is']))], 'c9'),
        V('v6', 'How do you value a perpetuity and a growing perpetuity?',
          'A perpetuity pays the same amount for ever, so its future value cannot be found but its present value is the payment divided by the interest rate, R by i. For a growing perpetuity, where payments grow at a constant rate g that is less than i, the present value is R divided by i minus g. The original capital is never paid back, so no principal is discounted.',
          [P('p1', 'Level perpetuity PV = R/i', 4, 'r by i|r over i|r divided by i|payment divided by the interest rate|payment divided by interest rate|payment divided by rate|payment by rate|cash flow divided by rate|amount divided by rate'),
           P('p2', 'Growing perpetuity PV = R/(i − g)', 4, 'i minus g|rate minus growth|interest rate minus growth|discount rate minus growth|i less g'),
           P('p3', 'Growth rate must be less than i; no PV of principal / no future value', 2, 'less than i|lower than i|smaller than i|less than the interest|g less than|never repaid|no present value of principal|no principal|future value cannot|no future value|cannot find future value|infinite future value', min=1)], 'c8'),
    ]

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
        's1': _K('annuity|p 3 0.10|2.48685|2.4869|2.487|pvaf|present value factor|present value'),
        's2': _N(120634.44),
        's3': _N(30000, 20936.56, 10966.77),
        's4': _N(90634.44, 99697.88, 109667.67, kw=['nil|zero|0']),
        's5': _K('year', 'opening', 'interest', 'principal|repayment', 'closing|balance', min=4),
    },
    'q2': {
        's1': _N(54540, 57820, 60080, 34150),
        's2': _N(6590),
        's3': _K('accept|undertak|go ahead|should invest|viable|worthwhile|recommend|take up', 'positive|0|greater|exceed|more than'),
    },
    'q3': {
        's1': _K('coupon|interest|annuity', nums=[80]),
        's2': _N(303.26),
        's3': _N(651.97),
        's4': _K('value|price|worth|pay|intrinsic', nums=[955.23]),
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
