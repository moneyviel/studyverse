"""CA Foundation · Paper 1 Accounting · Chapter 10 Partnership and LLP Accounts · Unit 3 Admission of a New Partner.
Original explanations, names and numbers (structure and scope follow the ICAI study material).
Also holds small table helpers (T-accounts, columnar capital accounts) reused by units 4–6 of this chapter."""
from fractions import Fraction as F
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch10-u03'


# ------------------------------------------------------------------ helpers shared by ch10 units
def amt(x):
    return '' if x in (None, '', 0) else inr(x)


def fr(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def ratio(*xs):
    """Fractions -> smallest whole-number ratio string, e.g. (9/20, 6/20, 5/20) -> '9:6:5'."""
    from math import gcd
    from functools import reduce
    xs = [F(x) for x in xs]
    den = reduce(lambda a, b: a * b // gcd(a, b), [x.denominator for x in xs])
    ints = [int(x * den) for x in xs]
    g = reduce(gcd, ints)
    return ':'.join(str(i // g) for i in ints)


def tacc(left, right, lh='Particulars', rh='Particulars', title=None, note=None, ltot='Total', rtot='Total'):
    """Two-sided account / balance sheet as a table. left/right: [(text, amount or None)]. Both sides must agree."""
    tl = sum(a for _, a in left if isinstance(a, (int, float)))
    tr = sum(a for _, a in right if isinstance(a, (int, float)))
    assert abs(tl - tr) < 0.01, (title, tl, tr)
    n = max(len(left), len(right))
    rows = []
    for i in range(n):
        l = left[i] if i < len(left) else ('', None)
        r = right[i] if i < len(right) else ('', None)
        rows.append([l[0], amt(l[1]), r[0], amt(r[1])])
    rows.append([ltot, inr(tl), rtot, inr(tr)])
    return table([lh, '₹', rh, '₹'], rows, num=[1, 3], total=True, title=title, note=note)


def capacc(partners, dr, cr, title="Partners' Capital Accounts", close_label='Balance c/d', note=None):
    """Columnar capital accounts. dr/cr: [(particulars, {partner: amount})]. Closing balance worked out per partner.
    Returns (table block, {partner: closing credit balance})."""
    bal = {p: sum(d.get(p, 0) for _, d in cr) - sum(d.get(p, 0) for _, d in dr) for p in partners}
    dr = list(dr); cr = list(cr)
    if any(v > 0 for v in bal.values()): dr.append(('To ' + close_label, {p: v for p, v in bal.items() if v > 0}))
    if any(v < 0 for v in bal.values()): cr.append(('By ' + close_label, {p: -v for p, v in bal.items() if v < 0}))
    n = max(len(dr), len(cr))
    rows = []
    for i in range(n):
        l = dr[i] if i < len(dr) else ('', {})
        r = cr[i] if i < len(cr) else ('', {})
        rows.append([l[0]] + [amt(l[1].get(p)) for p in partners] + [r[0]] + [amt(r[1].get(p)) for p in partners])
    td = [sum(d.get(p, 0) for _, d in dr) for p in partners]
    tc = [sum(d.get(p, 0) for _, d in cr) for p in partners]
    assert all(abs(a - b) < 0.01 for a, b in zip(td, tc))
    rows.append(['Total'] + [inr(x) for x in td] + ['Total'] + [inr(x) for x in tc])
    k = len(partners)
    head = ['Particulars'] + [f'{p} (₹)' for p in partners] + ['Particulars'] + [f'{p} (₹)' for p in partners]
    num_cols = list(range(1, k + 1)) + list(range(k + 2, 2 * k + 2))
    return table(head, rows, num=num_cols, total=True, title=title, note=note), bal


def split(total, shares):
    """Split an amount in fractional shares {name: Fraction}; amounts rounded to rupees."""
    return {k: round(total * F(v)) if total * F(v) == int(total * F(v)) else round(float(total * F(v)), 2) for k, v in shares.items()}


# ------------------------------------------------------------------ unit
def build():
    # ============ Illustration 1: Arora & Bhat admit Chopra (revaluation shown in books, reserve, premium) ============
    c1 = Checks()
    old = {'Arora': F(3, 5), 'Bhat': F(2, 5)}
    cshare = F(1, 4)
    new = {'Arora': (1 - cshare) * F(3, 5), 'Bhat': (1 - cshare) * F(2, 5), 'Chopra': cshare}
    c1.add('(1-1/4)*3/5', "Arora's new share = 9/20")
    c1.add('(1-1/4)*2/5', "Bhat's new share = 6/20")
    sac = {p: old[p] - new[p] for p in old}
    c1.add('3/5-9/20', "Arora's sacrifice = 3/20")
    c1.add('2/5-6/20', "Bhat's sacrifice = 2/20")
    bld_up = c1.add('144000-120000', 'Increase in building')
    mach_dn = c1.add('80000*10/100', 'Depreciation on machinery @10%')
    inv_dn = 4000
    pdd = c1.add('55000*5/100', 'Provision for doubtful debts @5%')
    wages = 3250
    rev = c1.add('24000-8000-4000-2750-3250', 'Profit on revaluation')
    rv = split(rev, old)
    c1.add('6000*3/5', "Arora's share of revaluation profit")
    res = split(25000, old)
    prem = split(40000, {p: sac[p] / sum(sac.values()) for p in sac})
    c1.add('40000*3/5', "Arora's share of premium (sacrificing ratio 3:2)")
    capA = c1.add('150000+15000+3600+24000', "Arora's closing capital")
    capB = c1.add('100000+10000+2400+16000', "Bhat's closing capital")
    bank = c1.add('30000+120000+40000', 'Bank after Chopra pays in')
    c1.add('60000+3250+192600+128400+120000', 'Balance sheet total (liabilities side)')
    c1.add('144000+72000+46000+(55000-2750)+190000', 'Balance sheet total (assets side)')
    E1 = [
        je('2026 Apr 1', [('Bank A/c', 160000)], [("Chopra's Capital A/c", 120000), ('Premium for Goodwill A/c', 40000)], 'Being capital and premium for goodwill brought in by Chopra for a 1/4 share'),
        je('Apr 1', [('Premium for Goodwill A/c', 40000)], [("Arora's Capital A/c", prem['Arora']), ("Bhat's Capital A/c", prem['Bhat'])], 'Being premium credited to the sacrificing partners in their sacrificing ratio 3:2'),
        je('Apr 1', [('General Reserve A/c', 25000)], [("Arora's Capital A/c", res['Arora']), ("Bhat's Capital A/c", res['Bhat'])], 'Being reserve transferred to the old partners in the old ratio 3:2'),
        je('Apr 1', [('Building A/c', bld_up)], [('Revaluation A/c', bld_up)], 'Being increase in the value of building'),
        je('Apr 1', [('Revaluation A/c', mach_dn + inv_dn + pdd + wages)], [('Machinery A/c', mach_dn), ('Inventory A/c', inv_dn), ('Provision for Doubtful Debts A/c', pdd), ('Outstanding Wages A/c', wages)], 'Being decrease in assets, provision created and unrecorded wages brought into the books'),
        je('Apr 1', [('Revaluation A/c', rev)], [("Arora's Capital A/c", rv['Arora']), ("Bhat's Capital A/c", rv['Bhat'])], 'Being revaluation profit shared by the old partners in the old ratio'),
    ]
    rev1 = tacc([('To Machinery A/c', mach_dn), ('To Inventory A/c', inv_dn), ('To Provision for Doubtful Debts A/c', pdd), ('To Outstanding Wages A/c', wages),
                 ("To Arora's Capital A/c (3/5 of profit)", rv['Arora']), ("To Bhat's Capital A/c (2/5 of profit)", rv['Bhat'])],
                [('By Building A/c', bld_up)], title='Revaluation Account')
    cap1, bal1 = capacc(['Arora', 'Bhat', 'Chopra'],
                        [],
                        [('By Balance b/d', {'Arora': 150000, 'Bhat': 100000}), ('By Bank A/c', {'Chopra': 120000}),
                         ('By Premium for Goodwill A/c', prem), ('By General Reserve A/c', res), ('By Revaluation A/c', rv)])
    assert bal1 == {'Arora': capA, 'Bhat': capB, 'Chopra': 120000}
    bs1 = tacc([('Trade payables', 60000), ('Outstanding wages', wages), ("Arora's capital", capA), ("Bhat's capital", capB), ("Chopra's capital", 120000)],
               [('Building', 144000), ('Machinery (80,000 − 8,000)', 72000), ('Inventory (50,000 − 4,000)', 46000),
                ('Trade receivables 55,000 less provision 2,750', 52250), ('Bank', bank)],
               lh='Liabilities', rh='Assets', title='Balance Sheet of Arora, Bhat and Chopra as at 1 April 2026')

    # ============ Illustration 2: new ratio — five situations ============
    c2 = Checks()
    p_, q_ = F(5, 8), F(3, 8)
    cases_ = []
    # I silent
    n1 = ((1 - F(1, 4)) * p_, (1 - F(1, 4)) * q_, F(1, 4)); c2.add('3/4*5/8', 'Case I: P new share 15/32'); c2.add('3/4*3/8', 'Case I: Q new share 9/32')
    cases_.append(['I. R gets 1/4; nothing said about who gives it', 'Remaining 3/4 split 5:3 → P 15/32, Q 9/32, R 8/32', ratio(*n1), ratio(p_ - n1[0], q_ - n1[1])])
    # II specific fractions
    n2 = (p_ - F(3, 16), q_ - F(1, 16), F(1, 4)); c2.add('5/8-3/16', 'Case II: P new share 7/16'); c2.add('3/8-1/16', 'Case II: Q new share 5/16')
    cases_.append(['II. R gets 3/16 from P and 1/16 from Q', 'P 10/16 − 3/16 = 7/16; Q 6/16 − 1/16 = 5/16; R 4/16', ratio(*n2), ratio(F(3, 16), F(1, 16))])
    # III surrender fraction of own share
    s3p, s3q = p_ * F(1, 5), q_ * F(1, 3); c2.add('5/8*1/5', 'Case III: P surrenders 1/8'); c2.add('3/8*1/3', 'Case III: Q surrenders 1/8')
    n3 = (p_ - s3p, q_ - s3q, s3p + s3q)
    cases_.append(['III. P gives up 1/5 of his share, Q gives up 1/3 of his share', 'P gives 5/8 × 1/5 = 1/8; Q gives 3/8 × 1/3 = 1/8; R = 1/8 + 1/8 = 2/8', ratio(*n3), ratio(s3p, s3q)])
    # IV entirely from one
    n4 = (p_ - F(1, 4), q_, F(1, 4)); c2.add('5/8-1/4', 'Case IV: P new share 3/8')
    cases_.append(['IV. R takes his whole 1/4 from P', 'P 5/8 − 2/8 = 3/8; Q stays 3/8; R 2/8', ratio(*n4), 'P alone (1:0)'])
    # V given ratio
    s5p, s5q = F(1, 4) * F(2, 5), F(1, 4) * F(3, 5); c2.add('5/8-1/4*2/5', 'Case V: P new share 21/40'); c2.add('3/8-1/4*3/5', 'Case V: Q new share 9/40')
    n5 = (p_ - s5p, q_ - s5q, F(1, 4))
    cases_.append(['V. R takes 1/4 from P and Q in the ratio 2:3', 'P gives 1/10, Q gives 3/20 → P 21/40, Q 9/40, R 10/40', ratio(*n5), ratio(s5p, s5q)])
    assert [c[2] for c in cases_] == ['15:9:8', '7:5:4', '2:1:1', '3:3:2', '21:9:10']
    ratio_tbl = table(['Situation (P:Q = 5:3, R admitted)', 'Working', 'New ratio P:Q:R', 'Sacrificing ratio P:Q'], cases_,
                      title='New profit sharing ratio and sacrificing ratio',
                      note='Case I: when nothing is said, the old partners keep their old ratio between themselves, so they sacrifice in the old ratio (5:3). Case III: R\'s share is not given — it is the total of what the old partners surrender.')

    # ============ Illustration 3: memorandum revaluation ============
    c3 = Checks()
    oldD = {'Dev': F(3, 5), 'Esha': F(2, 5)}
    newD = {'Dev': F(4, 5) * F(3, 5), 'Esha': F(4, 5) * F(2, 5), 'Farah': F(1, 5)}
    c3.add('4/5*3/5', "Dev's new share 12/25")
    mprofit = c3.add('30000-6000-3000', 'Net gain on revaluation (part I)')
    part1 = split(mprofit, oldD)
    part2 = split(mprofit, newD)
    c3.add('21000*3/5', "Dev's share of part I gain (old ratio)")
    c3.add('21000*12/25', "Dev's share of part II reversal (new ratio)")
    c3.add('21000*5/25', "Farah's share of part II reversal")
    netD = c3.add('12600-10080', 'Net credit to Dev')
    netE = c3.add('8400-6720', 'Net credit to Esha')
    c3.add('2520+1680', 'Net debit to Farah equals the old partners\' net credit')
    m1 = tacc([('To Furniture A/c', 6000), ('To Provision for Doubtful Debts A/c', 3000), ("To Dev's Capital A/c (3/5)", part1['Dev']), ("To Esha's Capital A/c (2/5)", part1['Esha'])],
              [('By Land A/c', 30000)], title='Memorandum Revaluation Account — Part I (old partners, old ratio 3:2)')
    m2 = tacc([('To Land A/c (reversal)', 30000)],
              [('By Furniture A/c (reversal)', 6000), ('By Provision for Doubtful Debts A/c (reversal)', 3000), ("By Dev's Capital A/c (12/25)", part2['Dev']),
               ("By Esha's Capital A/c (8/25)", part2['Esha']), ("By Farah's Capital A/c (5/25)", part2['Farah'])],
              title='Memorandum Revaluation Account — Part II (all partners, new ratio 12:8:5)')
    net_tbl = table(['Partner', 'Part I credit (₹)', 'Part II debit (₹)', 'Net effect (₹)'], [
        ['Dev', inr(part1['Dev']), inr(part2['Dev']), f'{inr(netD)} Cr'],
        ['Esha', inr(part1['Esha']), inr(part2['Esha']), f'{inr(netE)} Cr'],
        ['Farah', '—', inr(part2['Farah']), f"{inr(part2['Farah'])} Dr"],
    ], title='Net effect on capital accounts', note='The net figures equal Farah paying the old partners 5/25 of the gain in their sacrificing ratio 3:2 — one short entry (Farah\'s Capital Dr ₹4,200; To Dev ₹2,520; To Esha ₹1,680) gives the same capitals.')

    # ============ Illustration 4: hidden goodwill ============
    c4 = Checks()
    implied = c4.add('150000*4', 'Total capital implied by Isha’s contribution for 1/4 share')
    actual = c4.add('160000+120000+40000+150000', 'Actual capital incl. reserve and Isha’s capital')
    hg = c4.add('600000-470000', 'Hidden goodwill of the firm')
    ishare = c4.add('130000*1/4', "Isha's share of goodwill")
    c4.add('32500/2', 'Credited to each old partner (equal sacrifice)')
    E4 = [
        je('2026 Jul 1', [('Bank A/c', 150000)], [("Isha's Capital A/c", 150000)], 'Being capital brought in by Isha for a 1/4 share'),
        je('Jul 1', [('General Reserve A/c', 40000)], [("Gita's Capital A/c", 20000), ("Hari's Capital A/c", 20000)], 'Being reserve transferred to the old partners equally'),
        je('Jul 1', [("Isha's Capital A/c", ishare)], [("Gita's Capital A/c", ishare / 2), ("Hari's Capital A/c", ishare / 2)], "Being Isha's share of the hidden goodwill credited to the sacrificing partners"),
    ]

    # ============ Questions ============
    # Q1 ratio
    qc1 = Checks()
    qa = {'Jay': F(4, 7), 'Kunal': F(3, 7)}
    q1a = (qa['Jay'] * F(5, 6), qa['Kunal'] * F(5, 6), F(1, 6))
    qc1.add('4/7*5/6', '(a) Jay new share 20/42'); qc1.add('3/7*5/6', '(a) Kunal new share 15/42')
    q1b_j, q1b_k = qa['Jay'] - F(1, 6) * F(1, 2), qa['Kunal'] - F(1, 6) * F(1, 2)
    qc1.add('4/7-1/12', '(b) Jay new share 41/84'); qc1.add('3/7-1/12', '(b) Kunal new share 29/84')
    q1c_j, q1c_k = qa['Jay'] * F(3, 4), qa['Kunal'] * F(5, 6)
    lj, lk = qa['Jay'] - q1c_j, qa['Kunal'] - q1c_k
    qc1.add('4/7*1/4', '(c) Jay surrenders 1/7'); qc1.add('3/7*1/6', '(c) Kunal surrenders 1/14')
    q1_rat = [ratio(*q1a), ratio(q1b_j, q1b_k, F(1, 6)), ratio(q1c_j, q1c_k, lj + lk)]
    assert q1_rat == ['20:15:7', '41:29:14', '6:5:3'], q1_rat
    q1_sac = [ratio(qa['Jay'] - q1a[0], qa['Kunal'] - q1a[1]), '1:1', ratio(lj, lk)]
    assert q1_sac == ['4:3', '1:1', '2:1'], q1_sac

    # Q2 full admission
    qc2 = Checks()
    oldQ = {'Rao': F(1, 2), 'Sen': F(1, 2)}
    tsh = F(1, 3)
    newQ = {'Rao': F(1, 3), 'Sen': F(1, 3), 'Tara': F(1, 3)}
    qrev = qc2.add('36000-9000-2400-1600', 'Profit on revaluation (land up, plant down, provision, claim)')
    qrv = split(qrev, oldQ)
    qprem = qc2.add('90000*1/3', "Tara's share of goodwill (premium)")
    qpl = split(18000, oldQ)
    qcapR = qc2.add('180000+11500+9000+15000', "Rao's closing capital")
    qcapS = qc2.add('120000+11500+9000+15000', "Sen's closing capital")
    Q2rev = tacc([('To Plant A/c', 9000), ('To Provision for Doubtful Debts A/c', 2400), ('To Outstanding Claim (damages) A/c', 1600),
                  ("To Rao's Capital A/c (1/2)", qrv['Rao']), ("To Sen's Capital A/c (1/2)", qrv['Sen'])],
                 [('By Land and Building A/c', 36000)], title='Revaluation Account')
    Q2cap, qbal = capacc(['Rao', 'Sen', 'Tara'], [],
                         [('By Balance b/d', {'Rao': 180000, 'Sen': 120000}), ('By Bank A/c', {'Tara': 150000}), ('By Profit and Loss A/c (balance)', qpl),
                          ('By Premium for Goodwill A/c', {'Rao': qprem / 2, 'Sen': qprem / 2}), ('By Revaluation A/c', qrv)])
    assert qbal == {'Rao': qcapR, 'Sen': qcapS, 'Tara': 150000}, qbal

    # Q4 hidden goodwill
    qc4 = Checks()
    q4hg = qc4.add('150000*3-(140000+100000+20000+150000)', 'Hidden goodwill: 1,50,000 × 3 − 4,10,000')
    q4us = qc4.add('40000*1/3', "Usha's share of goodwill")
    q4sac = {'Uday': F(3, 5) - F(2, 5), 'Vani': F(2, 5) - F(4, 15)}
    qc4.add('3/5-2/5', "Uday's sacrifice 1/5 (new ratio given 6:4:5 → 2/5, 4/15, 1/3)")
    qc4.add('2/5-4/15', "Vani's sacrifice 2/15")
    q4u = qc4.add('40000/3*3/5', 'Credited to Uday (sacrificing ratio 3:2)')
    q4v = qc4.add('40000/3*2/5', 'Credited to Vani')
    Q4 = [
        je('(1)', [('Bank A/c', 150000)], [("Usha's Capital A/c", 150000)], 'Being capital brought in by Usha for a 1/3 share'),
        je('(2)', [('Profit and Loss A/c', 20000)], [("Uday's Capital A/c", 12000), ("Vani's Capital A/c", 8000)], 'Being undistributed profit transferred to old partners in the old ratio 3:2'),
        je('(3)', [("Usha's Capital A/c", round(q4us, 2))], [("Uday's Capital A/c", round(q4u, 2)), ("Vani's Capital A/c", round(q4v, 2))], "Being Usha's share of hidden goodwill credited to sacrificing partners in 3:2"),
    ]

    # ============ Case set ============
    kc = Checks()
    k_new = (F(2, 3) * F(1, 2), F(2, 3) * F(1, 2), F(1, 3))
    k_rev = kc.add('48000-12000-6000', 'Revaluation gain')
    k_hg = kc.add('300000*3-(250000+200000+30000+30000+300000)', 'Hidden goodwill after reserve and revaluation gain')
    k_sh = kc.add('90000/3', "Neel's share of goodwill")

    concepts = [
        {'id': 'c1', 'title': 'Why a firm admits a partner — and what must be settled first',
         'body': ['A firm brings in a new partner mainly for two reasons: it needs more capital, or it needs a person with skill, contacts or management ability. Legally the old partnership ends and a new one begins (reconstitution), but the firm and its business carry on.',
                  'Before the newcomer joins, the old partners must be given everything that belongs to the period before the admission: changes in the value of assets and liabilities, reserves and undistributed profits, and the goodwill they built. Only then will the profits and losses after the admission be shared fairly in the new ratio.',
                  'So an admission question always runs through the same checklist: (1) new ratio and sacrificing ratio, (2) goodwill (Unit 2), (3) revaluation of assets and liabilities, (4) reserves and accumulated profits or losses, (5) capital brought in and any capital adjustment, (6) new balance sheet.'],
         'analogy': 'Joining a group trip half-way: before the newcomer chips in, the group settles what was already spent and earned so far. From then on, everyone shares costs in the new proportion.',
         'work': 'When a CA firm or a family business adds a partner, the accountant prepares an "admission statement" with exactly this checklist and gets every partner to sign it before the supplementary deed is executed.'},
        {'id': 'c2', 'title': 'Revaluation Account (Profit and Loss Adjustment Account)',
         'body': ['Book values are usually out of date: buildings may be worth more, machines less, some debts doubtful, and some liabilities (or assets) may never have been recorded. On admission these are corrected through a Revaluation Account — also called a Profit and Loss Adjustment Account.',
                  'Debit side: every fall in an asset, every rise in a liability, and any unrecorded liability now brought in. Credit side: every rise in an asset, every fall in a liability, and any unrecorded asset now brought in.',
                  'The balance is the gain or loss that arose while only the old partners owned the business, so it goes to the OLD partners in the OLD ratio. The new partner gets nothing from it. Assets and liabilities then appear in the new balance sheet at the revised figures.'],
         'blocks': [table(['Change', 'Entry'], [['Asset value increases', 'Asset A/c Dr. To Revaluation A/c'], ['Asset value decreases / provision created', 'Revaluation A/c Dr. To Asset (or Provision) A/c'],
                                               ['Liability increases / unrecorded liability', 'Revaluation A/c Dr. To Liability A/c'], ['Liability decreases', 'Liability A/c Dr. To Revaluation A/c'],
                                               ['Gain on revaluation', "Revaluation A/c Dr. To Old Partners' Capital A/cs (old ratio)"], ['Loss on revaluation', "Old Partners' Capital A/cs Dr. To Revaluation A/c (old ratio)"]])],
         'analogy': 'Re-pricing the shelf before a new co-owner joins: whatever the stock is really worth today belongs to the people who owned it yesterday.',
         'work': 'In practice a valuer certifies the property, the accountant reviews ageing of debtors for the provision and searches for unrecorded bills. The revaluation figures are agreed in writing because they move partners\' capitals directly.'},
        {'id': 'c3', 'title': 'Memorandum Revaluation Account — when book values must not change',
         'body': ['Sometimes the partners agree to revalue for fairness but want the balance sheet to keep the old figures. Then a Memorandum Revaluation Account is used, in two parts.',
                  'Part I records the increases and decreases exactly as in a normal revaluation account; its balance goes to the OLD partners in the OLD ratio. Part II reverses every item of Part I; its balance (always the opposite of Part I) goes to ALL partners, including the new one, in the NEW ratio.',
                  'The asset and liability accounts themselves are not touched — only the capital accounts change. The net effect is that the new partner bears, through his capital, his share of the hidden gain (or receives his share of the hidden loss). The same result can be reached by adjusting the partners\' capital accounts directly without opening any revaluation account.'],
         'blocks': [table(['Point', 'Revaluation Account', 'Memorandum Revaluation Account'], [
             ['Book values afterwards', 'Assets and liabilities shown at revised values', 'Old values retained in the balance sheet'],
             ['Parts', 'One', 'Two — Part I (changes) and Part II (reversal)'],
             ['Who shares the balance', 'Old partners, old ratio', 'Part I: old partners, old ratio; Part II: all partners, new ratio']])],
         'analogy': 'Pencil marks in the margin: you work out what the change would be, credit the right people, and then rub out the effect on the figures themselves.',
         'work': 'Partners often prefer memorandum treatment to avoid showing a revalued building (and the questions banks ask about it). The accountant must still record the capital effect correctly, or the old partners lose part of their gain to the newcomer.'},
        {'id': 'c4', 'title': 'Reserves and accumulated profits or losses',
         'body': ['General reserve, workmen-type reserves no longer needed, and a credit balance of Profit and Loss Account were all earned before the admission. They are transferred to the OLD partners\' capital (or current) accounts in the OLD ratio: Reserve A/c (or P&L A/c) Dr. To Old Partners\' Capital A/cs.',
                  'An accumulated loss — a debit balance of Profit and Loss Account or deferred revenue expenditure shown on the assets side — is the reverse: Old Partners\' Capital A/cs Dr. To Profit and Loss A/c, in the old ratio.',
                  'If the partners decide to keep the reserve in the books, the newcomer would otherwise get a share of something he did not earn; an adjusting entry is then passed debiting the new partner\'s capital with his share and crediting the old partners in their sacrificing ratio.'],
         'analogy': 'Savings in the family piggy bank before a cousin moves in belong to the family that saved them.',
         'work': 'Auditors check that the reserve has actually been credited to the old partners before the admission date — a common slip is to leave it in the books and later distribute it in the new ratio.'},
        {'id': 'c5', 'title': 'Computing the new profit sharing ratio — five situations',
         'body': ['I. Only the new partner\'s share is given: unless agreed otherwise, the old partners continue in their old ratio between themselves. New share of an old partner = (1 − new partner\'s share) × his old share.',
                  'II. The new partner takes stated fractions from each old partner: new share = old share − fraction given.',
                  'III. Each old partner surrenders a fraction OF HIS OWN share: amount surrendered = old share × that fraction; the new partner\'s share is the total surrendered.',
                  'IV. The new partner takes his whole share from one partner: only that partner\'s share is reduced.',
                  'V. The new partner takes his share from the old partners in a given ratio: each gives (new partner\'s share × his part of that ratio).',
                  'Always convert to a common denominator at the end and reduce the ratio to its simplest whole numbers.'],
         'analogy': 'A pizza already cut 5:3 between two friends. A third friend arrives — either both trim their slices in proportion, or one gives up more, or they each cut off a stated piece.',
         'work': 'Ratios go into the supplementary partnership deed and into the tax computation of each partner\'s share. A wrong fraction here silently mis-states every year\'s profit distribution until someone notices.'},
        {'id': 'c6', 'title': 'Sacrificing ratio (and gaining partners)',
         'body': ['Sacrifice of an old partner = old share − new share. The ratio of these sacrifices is the sacrificing ratio. It is used to credit the old partners with the new partner\'s share of goodwill (premium).',
                  'In situation I the sacrificing ratio equals the old ratio. In every other situation it must be worked out — never assume it.',
                  'If an old partner\'s new share is larger than his old share, he is a gaining partner for that change; a gain is new share − old share.'],
         'analogy': 'If you give up part of your slice, you are the one who should be paid for it — and in proportion to how much you gave up.',
         'work': 'Premium for goodwill is a real cash receipt shared between partners. Crediting it in the old ratio instead of the sacrificing ratio is one of the most frequent errors found when reviewing admission entries.'},
        {'id': 'c7', 'title': 'Hidden goodwill',
         'body': ['Sometimes no value of goodwill is stated, but the capital the newcomer brings is more than his fair share of the net worth. The difference is goodwill "hidden" in the deal.',
                  'Hidden goodwill = (new partner\'s capital × reciprocal of his share) − (old partners\' capitals + reserves and undistributed profits + any revaluation gain − accumulated losses + new partner\'s capital).',
                  'The new partner\'s share of this goodwill is debited to his capital account and credited to the old partners in their sacrificing ratio (goodwill is not raised in the books, as only purchased goodwill may be recorded).'],
         'blocks': [p('Example: X and Y have capitals of ₹50,000 each. Z brings ₹60,000 for a 1/3 share. Implied total capital = 60,000 × 3 = ₹1,80,000; actual capital = 50,000 + 50,000 + 60,000 = ₹1,60,000; hidden goodwill = ₹20,000; Z\'s share ₹20,000 × 1/3 = ₹6,667 (rounded).')],
         'analogy': 'If someone pays ₹40 for a quarter share of a box of chocolates whose contents are worth only ₹120 in all, they are paying ₹10 extra for something you cannot see — the box\'s reputation.',
         'work': 'When a professional joins a well-known firm, the deal is often framed only as "bring ₹X for one-third". An accountant must spot the implied goodwill, or the old partners are under-credited.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Admission with revaluation, reserve and premium for goodwill', 'difficulty': 'moderate', 'minutes': 25,
         'q': ('Arora and Bhat share profits 3:2. Their Balance Sheet at 31 March 2026: Trade payables ₹60,000; General Reserve ₹25,000; Capitals — Arora ₹1,50,000, Bhat ₹1,00,000 (total ₹3,35,000). '
               'Assets: Building ₹1,20,000; Machinery ₹80,000; Inventory ₹50,000; Trade receivables ₹55,000; Bank ₹30,000. On 1 April 2026 Chopra is admitted for a 1/4 share. She brings ₹1,20,000 as capital and ₹40,000 as premium for goodwill. '
               'Agreed: building to be valued at ₹1,44,000; machinery depreciated by 10%; inventory written down by ₹4,000; provision for doubtful debts at 5% of receivables; outstanding wages of ₹3,250 not yet recorded. '
               'Pass journal entries, prepare the Revaluation Account, Partners\' Capital Accounts and the new Balance Sheet.'),
         'solution': [wn('New and sacrificing ratio', 'Chopra 1/4; the remaining 3/4 is shared 3:2 → Arora 9/20, Bhat 6/20, Chopra 5/20 = 9:6:5. Sacrifice: Arora 12/20 − 9/20 = 3/20; Bhat 8/20 − 6/20 = 2/20 → 3:2.'),
                      journal(E1, 'Journal (1 April 2026)', 'j1'), rev1, cap1, bs1,
                      note('Premium for goodwill goes to the sacrificing partners; reserve and revaluation profit go to the old partners in the old ratio. Here the two ratios happen to coincide because the question is silent about sacrifice.')],
         'checks': c1},
        {'id': 'i2', 'title': 'New ratio and sacrificing ratio in five situations', 'difficulty': 'core', 'minutes': 12,
         'q': 'P and Q share profits 5:3. R is admitted. Find the new ratio and the sacrificing ratio if: (I) R gets 1/4 and nothing else is stated; (II) R gets 3/16 from P and 1/16 from Q; (III) P surrenders 1/5 of his share and Q 1/3 of his share in R\'s favour; (IV) R takes his 1/4 share entirely from P; (V) R takes 1/4 from P and Q in the ratio 2:3.',
         'solution': [ratio_tbl], 'checks': c2},
        {'id': 'i3', 'title': 'Memorandum Revaluation Account — old values retained', 'difficulty': 'moderate', 'minutes': 14,
         'q': 'Dev and Esha share profits 3:2. Farah is admitted for a 1/5 share (old partners keep 3:2 between themselves). Land is worth ₹30,000 more than book value, furniture is overvalued by ₹6,000 and a provision for doubtful debts of ₹3,000 is needed. The partners want assets and liabilities to remain at their old book values. Prepare the Memorandum Revaluation Account and show the net effect on capitals.',
         'solution': [wn('New ratio', 'Remaining 4/5 split 3:2 → Dev 12/25, Esha 8/25, Farah 5/25.'), m1, m2, net_tbl], 'checks': c3},
        {'id': 'i4', 'title': 'Hidden goodwill', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Gita and Hari share profits equally, with capitals of ₹1,60,000 and ₹1,20,000 and a General Reserve of ₹40,000. On 1 July 2026 Isha is admitted for a 1/4 share and brings ₹1,50,000 as capital. Nothing is said about goodwill or about the old partners\' future ratio. Calculate hidden goodwill and pass the journal entries.',
         'solution': [wn('Hidden goodwill', f'Implied total capital = 1,50,000 × 4 = ₹{inr(implied)}. Actual = 1,60,000 + 1,20,000 + 40,000 (reserve) + 1,50,000 = ₹{inr(actual)}. Hidden goodwill = ₹{inr(hg)}; Isha\'s 1/4 share = ₹{inr(ishare)}, credited to Gita and Hari equally (they sacrifice in their old ratio 1:1).'),
                      journal(E4, 'Journal', 'j4')], 'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Admission statement for a growing consultancy firm', 'role': 'Article assistant helping the accounts partner of a client firm',
         'situation': 'A two-partner engineering consultancy is bringing in a third partner for a one-fourth share. The partners send you last year\'s balance sheet, a valuer\'s report on their office, and an e-mail saying "the newcomer brings ₹25 lakh, that covers everything".',
         'steps': ['Fix the new ratio and the sacrificing ratio first — confirm in writing whether the old partners keep their old ratio between themselves.',
                   'Ask whether ₹25 lakh is only capital or also includes goodwill. If no goodwill figure is agreed, work out the hidden goodwill from the net worth.',
                   'Prepare a revaluation working: office per valuer, provision on old debtors, unrecorded expenses and any claims pending.',
                   'Transfer the general reserve and undistributed profit to the old partners in the old ratio.',
                   'Draft the capital accounts and the opening balance sheet of the new firm, and have every partner sign the statement before the supplementary deed is drafted.'],
         'takeaway': 'An admission is a settlement of the past before a sharing of the future; every adjustment has to be agreed in writing because it moves partners\' capitals.',
         'think': 'The old partners want the revalued office to stay at its old book value in the balance sheet. Which account do you use?',
         'answer': 'A Memorandum Revaluation Account (or direct capital adjustments): Part I credited to old partners in the old ratio, Part II reversed among all partners in the new ratio. Book values stay unchanged.'},
        {'id': 'j2', 'title': 'Admitting a partner into an LLP', 'role': 'Accountant of a small LLP',
         'situation': 'An LLP is admitting a new partner who will contribute ₹10 lakh. The accounting is the same as for a firm, but there are LLP formalities too.',
         'steps': ['Check what the LLP agreement says about admission, contribution, profit share and goodwill.',
                   'Record the contribution, revaluation and reserve transfers exactly as for a partnership firm.',
                   'Get the supplementary LLP agreement signed and file the prescribed notice of change in partners with the Registrar (Form 4) within 30 days.',
                   'Update the partners\' contribution figures shown in the next annual filings.'],
         'takeaway': 'Partners\' capital in an LLP is called contribution, but revaluation, reserves and goodwill on admission follow the same accounting logic as a firm.'},
    ]

    mcqs = [
        None,
        {'id': 'm2', 'q': 'On admission, a decrease in the value of machinery is:', 'options': ['Debited to Revaluation Account', 'Credited to Revaluation Account', 'Debited to the new partner\'s capital', 'Credited to General Reserve'], 'answer': 0, 'explain': "A decrease in the value of an asset is a loss on revaluation. It is debited to the Revaluation Account and credited to the asset: Revaluation A/c Dr, To Machinery A/c. The trap 'credited to Revaluation Account' is the treatment for an increase in asset value, which is a gain. In practice: before a new partner joins, a valuer's report on plant and property is used so that old partners bear losses arising before the admission.", 'topic': "Revaluation Account or Profit and Loss Adjustment Account", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Profit on revaluation at the time of admission is credited to:', 'options': ['Old partners in the old ratio', 'All partners in the new ratio', 'Old partners in the sacrificing ratio', 'The new partner only'], 'answer': 0, 'explain': "Changes in asset and liability values arose while the old partners ran the firm, so revaluation profit belongs to them and is credited in their old ratio. The trap 'all partners in the new ratio' would give the newcomer a share of gains he had no part in. In practice: when a family firm admits an outsider, land often has a large unrecorded appreciation, and revaluation ensures the old partners get credit for it first.", 'topic': "Revaluation Account or Profit and Loss Adjustment Account", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'X and Y share 5:3. Z is admitted and the new ratio is 3:2:1. The sacrificing ratio of X and Y is:', 'options': ['3:1', '5:3', '1:1', '3:2'], 'answer': 0, 'explain': "Sacrifice = old share − new share. X: 5/8 − 3/6 = 15/24 − 12/24 = 3/24. Y: 3/8 − 2/6 = 9/24 − 8/24 = 1/24. Sacrificing ratio = 3 : 1. The trap 5 : 3 assumes sacrifice is always in the old ratio, which is true only when the new partner takes his share proportionately from both. In practice: the sacrificing ratio decides how a newcomer's goodwill premium is shared, so accountants work it out carefully.", 'topic': "Computation of New Profit Sharing Ratio", 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'In a Memorandum Revaluation Account, the balance of the second part is shared by:', 'options': ['All partners including the new partner in the new ratio', 'Old partners in the old ratio', 'The new partner alone', 'Old partners in the sacrificing ratio'], 'answer': 0, 'explain': "A Memorandum Revaluation Account is used when assets and liabilities must stay at book values. Part I records the revaluation changes and its result goes to the old partners in the old ratio. Part II reverses every change, and its balance is divided among the old and new partners in the new ratio — so the books end where they started. The trap 'old partners in the old ratio' applies to Part I, not Part II. In practice: firms use this to adjust capitals fairly without changing recorded values.", 'topic': "Revaluation Account or Profit and Loss Adjustment Account", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'General Reserve of ₹30,000 appears in the books of A and B (2:1) when C is admitted. A\'s capital is credited with:', 'options': ['₹20,000', '₹10,000', '₹15,000', '₹12,000'], 'answer': 0, 'check': '30000*2/3', 'explain': "Reserves accumulated before the admission belong to the old partners. They are distributed to them in their old ratio: A gets 30,000 × 2/3 = ₹20,000 and B ₹10,000. The trap ₹10,000 is B's share, and ₹15,000 splits the reserve equally. In practice: reserves represent past undistributed profits, so the accountant credits them to old partners before a new partner gets any share of future profits.", 'topic': "Reserves in the Balance Sheet", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'A and B have capitals of ₹60,000 and ₹40,000. C brings ₹50,000 for a 1/4 share. Hidden goodwill of the firm is:', 'options': ['₹50,000', '₹2,00,000', '₹1,50,000', '₹12,500'], 'answer': 0, 'check': '50000*4-(60000+40000+50000)', 'explain': "C's ₹50,000 for 1/4 share implies the firm's total capital should be 50,000 × 4 = ₹2,00,000. Actual capital = A 60,000 + B 40,000 + C 50,000 = ₹1,50,000. Hidden goodwill = 2,00,000 − 1,50,000 = ₹50,000. The trap ₹12,500 is C's 1/4 share of goodwill, not the firm's goodwill. In practice: when a new partner pays more than the firm's book value for a share, the extra reflects goodwill the old partners have built.", 'topic': "Hidden Goodwill", 'concept': 'c7', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'P and Q share 3:2. R gets 1/5 share entirely from P. The new ratio is:', 'options': ['2:2:1', '3:2:1', '12:8:5', '1:1:1'], 'answer': 0, 'explain': "R takes his full 1/5 from P. P: 3/5 − 1/5 = 2/5. Q keeps 2/5. R gets 1/5. New ratio = 2 : 2 : 1. The trap 12 : 8 : 5 assumes P and Q sacrifice proportionately in their old ratio, but here only P gives up his share. In practice: a senior partner planning retirement often gives his share to an incoming partner directly, so others' shares stay untouched.", 'topic': "Computation of New Profit Sharing Ratio", 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'An unrecorded liability discovered at the time of admission is:', 'options': ['Debited to Revaluation Account', 'Credited to Revaluation Account', 'Ignored', 'Debited to the new partner\'s capital account'], 'answer': 0, 'explain': "An unrecorded liability, once brought into the books, reduces the firm's net worth. It is a loss on revaluation: Revaluation A/c Dr, To Liability A/c. The trap 'credited to Revaluation Account' would treat a new obligation as a gain. In practice: due diligence before admission often uncovers pending supplier claims or unpaid statutory dues, which are recorded before the new partner joins.", 'topic': "Revaluation Account or Profit and Loss Adjustment Account", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'M and N share 2:1. M surrenders 1/4 of his share and N surrenders 1/2 of his share in favour of O. O\'s share is:', 'options': ['1/3', '1/6', '1/2', '1/4'], 'answer': 0, 'explain': "M's share is 2/3; he gives up 1/4 of it: 2/3 × 1/4 = 1/6. N's share is 1/3; he gives up 1/2 of it: 1/3 × 1/2 = 1/6. O's share = 1/6 + 1/6 = 1/3. The trap 1/6 counts only one partner's contribution. In practice: when existing partners agree to surrender fractions of their own shares, the accountant converts each fraction of a share into a fraction of the whole.", 'topic': "Computation of New Profit Sharing Ratio", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': 'A debit balance of Profit and Loss Account of ₹16,000 appears when C is admitted into the firm of A and B (equal partners). The entry is:', 'options': ["Debit A and B ₹8,000 each; credit Profit and Loss A/c ₹16,000", "Debit Profit and Loss A/c ₹16,000; credit A, B and C equally", "Debit C ₹5,333; credit Profit and Loss A/c", 'No entry is needed'], 'answer': 0, 'explain': "An accumulated loss (debit balance of Profit and Loss) belongs to the old partners. It is written off to their capitals in the old ratio: debit A and B ₹8,000 each, credit Profit and Loss A/c ₹16,000. The trap is charging the new partner C, who was not there when the loss was made. In practice: before admission, the accountant clears accumulated losses so that the new partner's capital is not burdened by past losses.", 'topic': "Reserves in the Balance Sheet", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Premium for goodwill brought in cash by a new partner is credited to the old partners in the:', 'options': ['Sacrificing ratio', 'Old ratio always', 'New ratio', 'Capital ratio'], 'answer': 0, 'explain': "Premium for goodwill compensates the old partners for the share of future profits they give up. So it is credited to them in their sacrificing ratio. The trap 'old ratio always' is correct only when sacrifices happen to be in the old ratio. In practice: if only one partner reduces his share to make room for a newcomer, he alone receives the goodwill premium.", 'topic': "Computation of New Profit Sharing Ratio", 'concept': 'c6', 'difficulty': 'core'},
    ]
    mcqs[0] = {'id': 'm1', 'q': 'A and B share profits 3:1. C is admitted for a 1/5 share and nothing is said about the sacrifice. The new ratio is:', 'options': ['3:1:1', '12:4:5', '3:1:4', '15:5:4'], 'answer': 0,
               'explain': "When nothing is said about the sacrifice, the old partners keep their old ratio over the remaining share. C takes 1/5, leaving 4/5 to be split 3 : 1: A = 4/5 × 3/4 = 12/20, B = 4/5 × 1/4 = 4/20, C = 1/5 = 4/20. Ratio 12 : 4 : 4 = 3 : 1 : 1. The trap 12 : 4 : 5 writes C's share as 5/20 instead of converting 1/5 to 4/20. In practice: partnership deeds for new admissions state the new ratio explicitly to avoid such confusion.", 'topic': "Computation of New Profit Sharing Ratio", 'concept': 'c5', 'difficulty': 'core'}
    assert ratio(F(4, 5) * F(3, 4), F(4, 5) * F(1, 4), F(1, 5)) == '3:1:1'

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
         'q': 'Jay and Kunal share profits 4:3. Kiran is admitted. Calculate the new ratio and the sacrificing ratio in each case: (a) Kiran gets 1/6 share and nothing else is agreed; (b) Kiran gets 1/6 share, contributed equally by Jay and Kunal; (c) Jay surrenders 1/4 of his share and Kunal surrenders 1/6 of his share in Kiran\'s favour.',
         'model': [table(['Case', 'Working', 'New ratio J:K:Kiran', 'Sacrificing ratio J:K'], [
             ['(a)', 'Remaining 5/6 split 4:3 → Jay 20/42, Kunal 15/42, Kiran 7/42', q1_rat[0], q1_sac[0] + ' (old ratio)'],
             ['(b)', 'Each gives 1/12 → Jay 4/7 − 1/12 = 41/84; Kunal 3/7 − 1/12 = 29/84; Kiran 14/84', q1_rat[1], q1_sac[1]],
             ['(c)', 'Jay gives 4/7 × 1/4 = 1/7 (= 2/14) → 3/7; Kunal gives 3/7 × 1/6 = 1/14 → 5/14; Kiran 3/14', q1_rat[2], q1_sac[2]],
         ])],
         'scheme': [{'id': 's1', 'pt': '(a) New ratio 20:15:7 with working', 'm': 1, 'skill': 'computation'},
                    {'id': 's2', 'pt': '(a) Sacrificing ratio = old ratio 4:3', 'm': 0.5, 'skill': 'concept'},
                    {'id': 's3', 'pt': '(b) New ratio 41:29:14 with working', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's4', 'pt': '(b) Sacrificing ratio 1:1', 'm': 0.5, 'skill': 'concept'},
                    {'id': 's5', 'pt': '(c) Surrender worked on own share; new ratio 6:5:3', 'm': 1, 'skill': 'computation'},
                    {'id': 's6', 'pt': '(c) Sacrificing ratio 2:1', 'm': 0.5, 'skill': 'computation'}],
         'checks': qc1,
         'remarks': ['Case (c) separates good answers from average ones: the fraction surrendered is a fraction of the partner\'s own share, not of the whole firm.',
                     'Many candidates stop at fractions; the examiner expects the ratio reduced to whole numbers.'],
         'mistakes': ['Taking Kiran\'s share in (c) as 1/4 + 1/6.', 'Assuming the sacrificing ratio is always the old ratio.', 'Leaving 20/42 : 15/42 : 7/42 unreduced.'],
         'tips': ['Lay the three cases out in one table — working, new ratio, sacrificing ratio.', 'Convert all shares to a common denominator before writing the ratio.']},
        {'id': 'q2', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'table',
         'q': '', 'model': [], 'scheme': [], 'remarks': [], 'mistakes': [], 'tips': []},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Distinguish between a Revaluation Account and a Memorandum Revaluation Account.',
         'model': [table(['Basis', 'Revaluation Account', 'Memorandum Revaluation Account'], [
             ['Purpose', 'Records revised values that will appear in the new balance sheet', 'Records the effect of revision while the old values stay in the balance sheet'],
             ['Structure', 'A single account', 'Two parts — Part I records the changes, Part II reverses them'],
             ['Sharing the balance', 'Old partners in the old ratio', 'Part I: old partners, old ratio; Part II: all partners including the new one, new ratio'],
             ['Effect on asset and liability accounts', 'They are changed to the revised figures', 'They are not changed; only capital accounts are affected'],
         ])],
         'scheme': [{'id': 's1', 'pt': 'Purpose / effect on balance sheet values', 'm': 1, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'One account vs two parts', 'm': 1, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Who shares the balance in each case and in what ratio', 'm': 1, 'skill': 'concept'},
                    {'id': 's4', 'pt': 'Asset/liability accounts changed vs unchanged', 'm': 1, 'skill': 'concept'}],
         'remarks': ['The ratio in which Part II is shared is the point most often missed.', 'A tabular answer with four clear bases scores full marks quickly.'],
         'mistakes': ['Saying Part II is shared in the old ratio.', 'Saying memorandum revaluation changes the book values.'],
         'tips': ['Use a three-column table: Basis | Revaluation A/c | Memorandum Revaluation A/c.']},
        {'id': 'q4', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'journal',
         'q': 'Uday and Vani share profits 3:2 with capitals of ₹1,40,000 and ₹1,00,000. Profit and Loss Account shows a credit balance of ₹20,000. Usha is admitted for a 1/3 share and brings ₹1,50,000 as capital. The new ratio is 6:4:5. Calculate hidden goodwill and pass journal entries.',
         'model': [wn('Hidden goodwill', f'Implied capital = 1,50,000 × 3 = ₹4,50,000. Actual = 1,40,000 + 1,00,000 + 20,000 (P&L) + 1,50,000 = ₹4,10,000. Hidden goodwill = ₹{inr(q4hg)}; Usha\'s share 1/3 = ₹{inr(round(q4us, 2))}.'),
                   wn('Sacrificing ratio', 'New shares 6/15, 4/15, 5/15. Uday 9/15 − 6/15 = 3/15; Vani 6/15 − 4/15 = 2/15 → 3:2.'),
                   journal(Q4, 'Journal', 'jq4'),
                   note('Amounts in entry (3) are ₹13,333.33 split 3:2; in the exam, rounding to the nearest rupee (₹13,333 → ₹8,000 and ₹5,333) is accepted if stated.')],
         'scheme': [{'id': 's1', 'pt': 'Implied total capital ₹4,50,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Actual capital includes P&L credit balance → hidden goodwill ₹40,000', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Sacrificing ratio 3:2 from the new ratio', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Capital brought in and P&L transferred in old ratio', 'm': 1, 'skill': 'posting'},
                    {'id': 's5', 'pt': "Usha's capital debited with her share, old partners credited", 'm': 1.5, 'skill': 'concept'}],
         'checks': qc4,
         'remarks': ['Candidates who leave out the P&L balance from the actual capital overstate goodwill.', 'Raising goodwill in the books instead of adjusting through capitals is not acceptable.'],
         'mistakes': ['Forgetting to include the new partner\'s own capital in the actual capital.', 'Crediting the goodwill share in the old ratio without checking the sacrifice.'],
         'tips': ['Write the hidden-goodwill formula first, then substitute — method marks are given even if a figure slips.']},
    ]
    # Q2 full answer (built after the table helpers above)
    q2 = questions[1]
    q2['q'] = ('Rao and Sen share profits equally. Their Balance Sheet at 30 September 2026 shows: Trade payables ₹48,000; Profit and Loss Account (credit balance) ₹18,000; Capitals — Rao ₹1,80,000, Sen ₹1,20,000 (total ₹3,66,000). '
               'Assets: Land and building ₹1,50,000; Plant ₹90,000; Inventory ₹60,000; Trade receivables ₹52,000; Bank ₹14,000. On 1 October 2026 Tara is admitted for a 1/3 share; the new ratio is equal. She brings ₹1,50,000 as capital and her share of goodwill in cash; the firm\'s goodwill is valued at ₹90,000. '
               'Land and building is to be increased by ₹36,000, plant reduced by 10%, a provision for doubtful debts of ₹2,400 created, and an unrecorded claim for damages of ₹1,600 is to be provided for. Prepare the Revaluation Account, the capital accounts of the partners and the new firm\'s Balance Sheet.')
    q2['model'] = [wn('Ratios', 'Old 1:1; new 1:1:1. Sacrifice: Rao 1/2 − 1/3 = 1/6; Sen 1/6 → 1:1. Tara\'s goodwill = 90,000 × 1/3 = ₹30,000, credited ₹15,000 each.'),
                   Q2rev, Q2cap, None]
    qbank_fix = 14000 + 150000 + 30000
    q2['model'][-1] = tacc([('Trade payables', 48000), ('Outstanding claim for damages', 1600), ("Rao's capital", qcapR), ("Sen's capital", qcapS), ("Tara's capital", 150000)],
                           [('Land and building (1,50,000 + 36,000)', 186000), ('Plant (90,000 − 9,000)', 81000), ('Inventory', 60000),
                            ('Trade receivables 52,000 less provision 2,400', 49600), ('Bank (14,000 + 1,50,000 + 30,000)', qbank_fix)], lh='Liabilities', rh='Assets',
                           title='Balance Sheet of Rao, Sen and Tara as at 1 October 2026')
    qc2b = Checks()
    qc2b.add('36000-9000-2400-1600', 'Profit on revaluation')
    qc2b.add('90000*1/3', "Tara's share of goodwill")
    qc2b.add('180000+9000+15000+11500', "Rao's closing capital")
    qc2b.add('120000+9000+15000+11500', "Sen's closing capital")
    qc2b.add('14000+150000+30000', 'Bank balance')
    qc2b.add('48000+1600+215500+155500+150000', 'Balance sheet total')
    qc2b.add('186000+81000+60000+49600+194000', 'Assets total')
    assert qcapR == 215500 and qcapS == 155500
    q2['checks'] = qc2b
    q2['scheme'] = [{'id': 's1', 'pt': 'Revaluation profit ₹23,000 with each item on the correct side', 'm': 2, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Revaluation profit and P&L balance shared 1:1 by old partners', 'm': 1.5, 'skill': 'posting'},
                    {'id': 's3', 'pt': 'Goodwill ₹30,000 credited to Rao and Sen in sacrificing ratio 1:1', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's4', 'pt': 'Capital accounts balanced: Rao ₹2,15,500, Sen ₹1,55,500, Tara ₹1,50,000', 'm': 2, 'skill': 'balancing'},
                    {'id': 's5', 'pt': 'Balance sheet with revised values, provision deducted, claim shown, bank ₹1,94,000', 'm': 2, 'skill': 'presentation'},
                    {'id': 's6', 'pt': 'Working notes for ratios', 'm': 1, 'skill': 'presentation'}]
    q2['remarks'] = ['Most errors come from the unrecorded claim: it is a new liability, so it is debited to Revaluation and shown on the liabilities side.',
                     'Some candidates share the P&L credit balance with Tara — it was earned before her admission.',
                     'A balance sheet that does not agree loses presentation marks even when the accounts are right; total both sides before moving on.']
    q2['mistakes'] = ['Showing goodwill as an asset in the new balance sheet.', 'Crediting revaluation profit in the new ratio 1:1:1.', 'Forgetting to add Tara\'s goodwill cash to the bank balance.']
    q2['tips'] = ['Prepare the Revaluation Account first; its balance feeds the capital accounts.', 'Use columnar capital accounts — one column per partner.', 'Show provision as a deduction from receivables in the balance sheet.']
    for qq in questions:
        assert abs(sum(s['m'] for s in qq['scheme']) - qq['marks']) < 0.01, qq['id']

    viva = [
        V('v1', 'Why are assets and liabilities revalued when a new partner is admitted, and who gets the profit or loss on revaluation?',
          'Book values are often out of date, so assets and liabilities are revalued to bring them to their fair value on the date of admission. The gain or loss arose while only the old partners owned the firm, so the profit or loss on revaluation is transferred to the old partners in their old profit sharing ratio. The new partner gets no share of it.',
          [P('p1', 'Values brought to current/fair value so the past change is settled before admission', 3, 'not the real|not real|not the true|not true|not correct|not up to date|not current|not the current|fair value|current value|true value|real value|present value|market value|out of date|outdated|updated|correct value|actual value|realistic'),
           P('p2', 'Profit/loss goes to the old partners', 4, 'old partner|existing partner|original partner'),
           P('p3', 'In the old profit sharing ratio', 3, 'old ratio|old profit sharing|old profit ratio|existing ratio|original ratio|previous ratio'),
           ], 'c2'),
        V('v2', 'How do you calculate the new profit sharing ratio when only the new partner\'s share is given?',
          'When only the new partner\'s share is given, it is assumed that the old partners continue to share among themselves in their old ratio. So I subtract the new partner\'s share from one, and divide the balance between the old partners in their old ratio. Each old partner\'s new share is the remaining share multiplied by his old share. In this case the sacrificing ratio is the same as the old ratio.',
          [P('p1', 'Subtract the new partner\'s share from 1 (whole)', 3, 'share from one|share from 1|from the whole|subtract from one|deduct from one|one minus|1 minus|less from one|minus the new partner|subtract new partner|deduct new partner|remaining share|balance share|balance of the share|remaining profit', min=1),
           P('p2', 'Balance divided among old partners in the old ratio', 4, 'old ratio|old profit sharing ratio|existing ratio|same ratio as before|original ratio'),
           P('p3', 'Sacrificing ratio equals the old ratio here', 3, 'sacrific', 'same as old|equal to old|old ratio|same as the old|equals the old')], 'c5'),
        V('v3', 'What is a sacrificing ratio and where is it used on admission?',
          'Sacrificing ratio is the ratio in which the old partners give up their share of profit in favour of the new partner. Each partner\'s sacrifice is his old share minus his new share. It is used to credit the old partners with the new partner\'s share of goodwill or premium.',
          [P('p1', 'Ratio in which old partners give up / surrender share to the new partner', 3, 'give up|gave up|giving up|surrender|forgo|forego|part with|let go|in favour of the new|in favor of the new'),
           P('p2', 'Sacrifice = old share − new share', 4, ALT('{o} minus {n}', '{o} less {n}', 'difference between {o} and {n}', 'subtract {n} from {o}', '{n} deducted from {o}', '{n} subtracted from {o}', 'deduct {n} from {o}',
                                                              o=('old share', 'old ratio', 'old profit share'), n=('new share', 'new ratio', 'new profit share'))),
           P('p3', 'Used to distribute the new partner\'s goodwill/premium among old partners', 3, 'goodwill|premium')], 'c6'),
        V('v4', 'How is a general reserve shown in the old balance sheet treated on the admission of a partner?',
          'The general reserve was built from profits earned before the admission, so it belongs to the old partners. It is credited to the old partners, in their old ratio, by debiting General Reserve Account and crediting their capital accounts. The new partner does not get any share of it.',
          [P('p1', 'Transferred to old partners\' capital/current accounts', 4, 'old partner|existing partner', 'capital|current|transfer|credit', min=2),
           P('p2', 'In the old ratio', 3, 'old ratio|old profit sharing ratio|existing ratio|original ratio'),
           P('p3', 'General Reserve debited (the newcomer gets nothing)', 3, 'reserve account debit|debit general reserve|debit reserve|general reserve debit|reserve debit|new partner does not|new partner not|no share|nothing to the new|not to the new|newcomer does not', min=1)], 'c4'),
        V('v5', 'What is a Memorandum Revaluation Account and how is it different from an ordinary Revaluation Account?',
          'A Memorandum Revaluation Account is used when the partners want the assets and liabilities to stay at their old book values. It has two parts. The first part, which records the changes, goes to the old partners in the old ratio. The second part, which reverses the same items, is shared by every partner, the newcomer included, in the new ratio. An ordinary revaluation account has one part and the revised values appear in the balance sheet.',
          [P('p1', 'Used when book values are to remain unchanged', 3, 'old value|book value|old figure|not change|unchanged|remain same|remain the same|without changing|same value|old book', min=1),
           P('p2', 'Two parts', 2, 'two part|2 part|two half|two section|second part|first part'),
           P('p3', 'First part: old partners, old ratio', 2, ALT('{p} {o}', '{p} which records the changes {o}', '{p} records the changes {o}', p=('first part', 'part one', 'part 1', 'part i', 'first half'), o=('old partner', 'old partners', 'old ratio', 'existing partners'))),
           P('p4', 'Second part: all partners incl. new, new ratio', 3, ALT('{p} {a}', '{p} which reverses the same items {a}', '{p} reverses {a}', p=('second part', 'part two', 'part 2', 'part ii', 'second half'), a=('all partner', 'all partners', 'all the partners', 'new ratio', 'including the new', 'everyone', 'every partner')))], 'c3'),
        V('v6', 'How do you find hidden goodwill when the value of goodwill is not given?',
          'Multiply the new partner\'s capital by the reciprocal of his share to get the total capital the firm should have. From this deduct the actual capital, which is the old partners\' capitals plus reserves and undistributed profits plus the new partner\'s capital. The difference is the hidden goodwill. The new partner\'s share of it is debited to his capital and credited to the old partners in the sacrificing ratio.',
          [P('p1', 'New partner\'s capital × reciprocal of his share = implied total capital', 4, 'reciprocal|inverse|multiply|multiplied|times|divided by his share|divide by his share|total capital of the firm|implied capital|implied total', min=1),
           P('p2', 'Less actual capital (old capitals + reserves + new partner\'s capital)', 3, 'deduct|less|minus|subtract|difference', 'actual capital|old partners capital|existing capital|combined capital|total of capitals|capitals of all|all capitals|capital of old', min=2),
           P('p3', 'New partner\'s share credited to old partners in sacrificing ratio', 3, 'sacrific')], 'c7'),
    ]

    kcase = [{'id': 'k1', 'title': 'Neel joins Mira & Om', 'difficulty': 'hard',
              'case': ('Mira and Om share profits equally, with capitals of ₹2,50,000 and ₹2,00,000 and a General Reserve of ₹30,000. On admitting Neel for a 1/3 share (new ratio equal), they find that land is worth ₹48,000 more than book value, '
                       'machinery is overvalued by ₹12,000 and a provision for doubtful debts of ₹6,000 is required. Revised values are to be shown in the books. Neel brings ₹3,00,000 as capital; nothing is said about goodwill.'),
              'mcqs': [
                  M('k1a', 'What is the profit on revaluation?', [R(k_rev), R(66000), R(48000), R(42000)], 0, "Revaluation: land increases by ₹48,000 (gain); machinery is overvalued by ₹12,000 (loss); new provision for doubtful debts ₹6,000 (loss). Profit = 48,000 − 12,000 − 6,000 = ₹30,000, credited to Mira and Om equally. The trap ₹66,000 adds all three changes; ₹42,000 forgets the provision. In practice: a valuer's report and debtor ageing are used to restate assets before admission.", 'moderate', '48000-12000-6000') | {'topic': "Revaluation Account or Profit and Loss Adjustment Account"},
                  M('k1b', 'What is the hidden goodwill of the firm?', [R(k_hg), R(120000), R(150000), R(60000)], 0,
                    "Neel's ₹3,00,000 for 1/3 implies total capital of 3,00,000 × 3 = ₹9,00,000. Actual capitals after adjustments: Mira 2,50,000 + Om 2,00,000 + reserve 30,000 + revaluation gain 30,000 + Neel 3,00,000 = ₹8,10,000. Hidden goodwill = 9,00,000 − 8,10,000 = ₹90,000. The trap ₹1,20,000 forgets the revaluation gain; ₹1,50,000 forgets both reserve and revaluation gain. In practice: partners compute this to see what extra the newcomer is paying for the firm's reputation.", 'hard', '300000*3-(250000+200000+30000+30000+300000)') | {'topic': "Hidden Goodwill"},
                  M('k1c', "How much is debited to Neel's capital account for goodwill?", [R(k_sh), R(45000), R(90000), R(15000)], 0, "Neel's share of the firm's goodwill = 90,000 × 1/3 = ₹30,000, debited to his capital account. Mira and Om each go from 1/2 to 1/3, a sacrifice of 1/6 each, so each is credited ₹15,000. The trap ₹90,000 debits the whole firm's goodwill to Neel; ₹15,000 is one partner's credit. In practice: goodwill adjustments are passed through capital accounts so that no goodwill asset appears in the books.", 'hard', '90000/3') | {'topic': "Hidden Goodwill"},
                  M('k1d', 'In what ratio is the General Reserve transferred?', ['1:1 to Mira and Om only', '1:1:1 to all three partners', 'Capital ratio 5:4', 'Not transferred; it stays in the books'], 0,
                    "The General Reserve was built from profits earned before Neel joined, so it belongs to Mira and Om and is credited to them in their old ratio, which is equal (1 : 1). The trap 1 : 1 : 1 shares the reserve with Neel, who had no part in earning it. In practice: before a partner joins, the accountant transfers accumulated reserves to old partners so that the newcomer's share starts afresh.", 'core') | {'topic': "Reserves in the Balance Sheet"},
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch10', 'n': 3,
        'title': 'Admission of a New Partner',
        'outcomes': [
            'Explain why a firm admits a partner and list every adjustment needed on the date of admission.',
            'Prepare a Revaluation (Profit and Loss Adjustment) Account, and a two-part Memorandum Revaluation Account when book values are to stay unchanged.',
            'Transfer reserves and accumulated profits or losses to the old partners in the correct ratio.',
            'Work out the new ratio and the sacrificing ratio in every standard situation.',
            'Infer hidden goodwill from the capital brought in and adjust it through capital accounts.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 70}, 'prereq': ['fnd-p1-ch10-u01', 'fnd-p1-ch10-u02'],
                 'exam_tip': 'Admission questions usually carry 10 marks: revaluation account, capital accounts and balance sheet. Ratios and goodwill are where step marks are won or lost — always show them as working notes.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Admission = reconstitution: settle the past (revaluation, reserves, goodwill) before sharing the future in the new ratio.',
                        'Revaluation Account: Dr decreases in assets and increases in liabilities; Cr increases in assets and decreases in liabilities; balance to old partners in old ratio.',
                        'Memorandum Revaluation: Part I old partners old ratio; Part II reversal, all partners new ratio; book values unchanged.',
                        'Reserves / P&L credit to old partners in old ratio; accumulated losses debited to them in old ratio.',
                        'New ratio — five situations; sacrificing ratio = old share − new share.',
                        'Hidden goodwill = new capital × reciprocal of share − (old capitals + reserves + new capital).'],
            'remember': ['If only the new share is given, old partners keep their old ratio and sacrifice in it.', 'Premium for goodwill → sacrificing ratio; revaluation and reserves → old ratio.', 'Unrecorded liability = loss on revaluation; unrecorded asset = gain.'],
            'traps': ["Don't give the new partner a share of revaluation profit or reserves.", "Don't compute surrender in Case III on the whole firm — it is a fraction of the partner's own share.", "Don't raise goodwill as an asset when it is only hidden in the capital brought in."],
        },
        'quickref': [
            {'k': 'New share (silent case)', 'v': 'Old share × (1 − new partner\'s share)'},
            {'k': 'Sacrifice', 'v': 'Old share − New share'},
            {'k': 'Revaluation balance', 'v': 'Old partners, old ratio'},
            {'k': 'Memorandum revaluation', 'v': 'Part I: old partners, old ratio · Part II: all partners, new ratio'},
            {'k': 'Reserves / P&L credit', 'v': 'Reserve A/c Dr. To Old Partners\' Capital A/cs (old ratio)'},
            {'k': 'Premium for goodwill', 'v': 'Premium for Goodwill A/c Dr. To Sacrificing Partners\' Capital A/cs (sacrificing ratio)'},
            {'k': 'Hidden goodwill', 'v': 'New capital × 1/share − (old capitals + reserves + revaluation gain − losses + new capital)'},
        ],
        'viva': viva, 'cases': kcase,
    }
