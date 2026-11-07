"""CA Foundation · Paper 1 Accounting · Chapter 5 Depreciation and Amortisation (single unit).
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *

UID = 'fnd-p1-ch05-u01'


def P(pid, pt, w, *kw, min=None):
    d = {'id': pid, 'pt': pt, 'w': w, 'kw': list(kw)}
    if min is not None: d['min'] = min
    return d


def V(vid, q, model, points, concept=None):
    d = {'id': vid, 'q': q, 'model': model, 'points': points}
    if concept: d['concept'] = concept
    return d


def M(mid, q, options, answer, explain, concept=None, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'difficulty': difficulty}
    if concept: d['concept'] = concept
    if check: d['check'] = check
    return d


def ledger(ac, dr, cr, close_date=None, next_date=None):
    """dr/cr = [(date, particulars, amount[, opening])]; closes with Balance c/d on the lighter side if close_date given."""
    mk = lambda x: {'date': x[0], 'part': x[1], 'amt': x[2], **({'ob': True} if len(x) > 3 and x[3] else {})}
    D, C = [mk(x) for x in dr], [mk(x) for x in cr]
    sd, sc = sum(x['amt'] for x in D), sum(x['amt'] for x in C)
    b = {'t': 'ledger', 'ac': ac, 'dr': D, 'cr': C}
    if close_date and sd != sc:
        bal = abs(sd - sc)
        if sd > sc: C.append({'date': close_date, 'part': 'By Balance c/d', 'amt': bal, 'bal': True}); b['next'] = {'date': next_date, 'side': 'dr', 'amt': bal}
        else: D.append({'date': close_date, 'part': 'To Balance c/d', 'amt': bal, 'bal': True}); b['next'] = {'date': next_date, 'side': 'cr', 'amt': bal}
    return b


def build():
    # ============ Illustration 1: SLM vs WDV, part-year ============
    c1 = Checks()
    cost1 = c1.add('840000+60000', 'Cost including installation')
    slm = c1.add('(900000-60000)/7', 'SLM depreciation per year')
    s1 = c1.add('120000*6/12', 'SLM 2026-27 (6 months)')
    w1 = c1.add('900000*20/100*6/12', 'WDV 2026-27 (6 months @ 20%)')
    w2 = c1.add('(900000-90000)*20/100', 'WDV 2027-28')
    c1.add('900000-60000-120000', 'SLM carrying amount on 31 March 2028')
    c1.add('900000-90000-162000', 'WDV carrying amount on 31 March 2028')
    m1a = ledger('Machinery Account (SLM — depreciation credited to the asset)',
                 [('2026 Oct 1', 'To Bank A/c (cost)', 840000), ('Oct 1', 'To Bank A/c (installation)', 60000)],
                 [('2027 Mar 31', 'By Depreciation A/c', s1)], '2027 Mar 31', '2027 Apr 1')
    m1b = ledger('Machinery Account (SLM) — 2027-28', [('2027 Apr 1', 'To Balance b/d', 840000, True)], [('2028 Mar 31', 'By Depreciation A/c', slm)], '2028 Mar 31', '2028 Apr 1')
    d1 = ledger('Depreciation Account', [('2027 Mar 31', 'To Machinery A/c', s1)], [('2027 Mar 31', 'By Profit and Loss A/c', s1)])
    cmp1 = table(['Year', 'SLM depreciation (₹)', 'SLM closing value (₹)', 'WDV @20% depreciation (₹)', 'WDV closing value (₹)'], [
        ['2026-27 (6 months)', inr(s1), inr(cost1 - s1), inr(w1), inr(cost1 - w1)],
        ['2027-28', inr(slm), inr(cost1 - s1 - slm), inr(w2), inr(cost1 - w1 - w2)],
    ], title='SLM vs WDV for the same machine')

    # ============ Illustration 2: provision for depreciation + disposal ============
    c2 = Checks()
    dA = c2.add('500000*10/100', 'Annual depreciation on Machine A (10% of cost)')
    dA27 = c2.add('50000*9/12', 'Machine A, 1 Apr 2026 to 1 Jan 2027 (9 months)')
    accA = c2.add('50000+50000+37500', 'Accumulated depreciation on Machine A at sale')
    bvA = c2.add('500000-137500', 'Book value of A on 1 Jan 2027')
    lossA = c2.add('362500-340000', 'Loss on sale of A')
    dB26 = c2.add('300000*10/100*6/12', 'Machine B 2025-26 (6 months)')
    dB27 = c2.add('300000*10/100', 'Machine B 2026-27')
    ob_prov = c2.add('50000+50000+15000', 'Provision balance on 1 April 2026')
    c2.add('37500+30000', 'Depreciation for 2026-27')
    J2 = [je('2027 Jan 1', [('Depreciation A/c', dA27)], [('Provision for Depreciation A/c', dA27)], 'Being depreciation on Machine A up to the date of sale'),
          je('Jan 1', [('Machinery Disposal A/c', 500000)], [('Machinery A/c', 500000)], 'Being original cost of Machine A transferred on sale'),
          je('Jan 1', [('Provision for Depreciation A/c', accA)], [('Machinery Disposal A/c', accA)], 'Being accumulated depreciation on Machine A transferred'),
          je('Jan 1', [('Bank A/c', 340000)], [('Machinery Disposal A/c', 340000)], 'Being sale proceeds of Machine A received'),
          je('Jan 1', [('Profit and Loss A/c', lossA)], [('Machinery Disposal A/c', lossA)], 'Being loss on sale of Machine A written off'),
          je('Mar 31', [('Depreciation A/c', dB27)], [('Provision for Depreciation A/c', dB27)], 'Being depreciation on Machine B for the year'),
          je('Mar 31', [('Profit and Loss A/c', dA27 + dB27)], [('Depreciation A/c', dA27 + dB27)], 'Being depreciation for the year transferred')]
    mach2 = ledger('Machinery Account (at original cost)', [('2026 Apr 1', 'To Balance b/d (A 5,00,000 + B 3,00,000)', 800000, True)],
                   [('2027 Jan 1', 'By Machinery Disposal A/c', 500000)], '2027 Mar 31', '2027 Apr 1')
    prov2 = ledger('Provision for Depreciation Account', [('2027 Jan 1', 'To Machinery Disposal A/c', accA)],
                   [('2026 Apr 1', 'By Balance b/d', ob_prov, True), ('2027 Jan 1', 'By Depreciation A/c (A)', dA27), ('Mar 31', 'By Depreciation A/c (B)', dB27)], '2027 Mar 31', '2027 Apr 1')
    disp2 = ledger('Machinery Disposal Account', [('2027 Jan 1', 'To Machinery A/c', 500000)],
                   [('Jan 1', 'By Provision for Depreciation A/c', accA), ('Jan 1', 'By Bank A/c', 340000), ('Jan 1', 'By Profit and Loss A/c (loss)', lossA)])
    assert prov2['next']['amt'] == dB26 + dB27

    # ============ Illustration 3: other methods ============
    c3 = Checks()
    syd_base = c3.add('650000-50000', 'Depreciable amount')
    c3.add('5*6/2', 'Sum of years digits for 5 years')
    sy = [c3.add(f'600000*{k}/15', f'SYD year {6 - k}') for k in (5, 4, 3, 2, 1)]
    sydt = table(['Year', 'Fraction', 'Depreciation (₹)'], [[str(i + 1), f'{5 - i}/15', inr(v)] for i, v in enumerate(sy)] + [['Total', '', inr(sum(sy))]], num=[2], total=True, title='(a) Sum of years\' digits')
    mh_rate = c3.add('(1800000-200000)/20000', 'Machine hour rate')
    mh1 = c3.add('80*4800', 'Machine hour depreciation, year 1')
    pu1 = c3.add('(1800000-200000)*30000/160000', 'Production units depreciation, year 1')
    dep_rate = c3.add('9000000/300000', 'Depletion rate per tonne')
    dep1 = c3.add('30*18000', 'Depletion, year 1')

    # ============ Illustration 4: change in estimate / method / revaluation ============
    c4 = Checks()
    e_wdv = c4.add('1200000-1200000/10*4', 'Carrying amount after 4 years (SLM, 10-year life)')
    e_new = c4.add('720000/4', 'Revised annual depreciation over remaining 4 years')
    m_slm = c4.add('(1000000-100000)/9', 'SLM depreciation per year')
    m_wdv = c4.add('1000000-100000*3', 'Carrying amount after 3 years')
    m_new = c4.add('700000*20/100', 'Year 4 depreciation at 20% WDV')
    r_sur = c4.add('840000-700000', 'Revaluation surplus')
    r_dep = c4.add('840000/7', 'Depreciation after revaluation')

    # ============ Illustration 5: amortisation ============
    c5 = Checks()
    pat = c5.add('2400000+120000', 'Cost of patent including legal fees')
    am_y = c5.add('2520000/8', 'Annual amortisation over 8 years')
    am1 = c5.add('315000*8/12', 'Amortisation 2026-27 (1 Aug to 31 Mar = 8 months)')
    pat1 = ledger('Patent Account', [('2026 Aug 1', 'To Bank A/c (purchase price)', 2400000), ('Aug 1', 'To Bank A/c (legal and registration fees)', 120000)],
                  [('2027 Mar 31', 'By Amortisation A/c', am1)], '2027 Mar 31', '2027 Apr 1')
    pat2 = ledger('Patent Account — 2027-28', [('2027 Apr 1', 'To Balance b/d', pat - am1, True)], [('2028 Mar 31', 'By Amortisation A/c', am_y)], '2028 Mar 31', '2028 Apr 1')
    amo = ledger('Amortisation Account', [('2027 Mar 31', 'To Patent A/c', am1)], [('2027 Mar 31', 'By Profit and Loss A/c', am1)])

    # ============ Question 1: WDV machinery account with sale ============
    q1c = Checks()
    X0 = q1c.add('640000+40000', 'Machine X cost with erection')
    dX1 = q1c.add('680000*15/100', 'X 2024-25')
    dY1 = q1c.add('300000*15/100*6/12', 'Y 2024-25 (6 months)')
    cd1 = q1c.add('680000+300000-102000-22500', 'Balance c/d 31 Mar 2025')
    dX2 = q1c.add('(680000-102000)*15/100*6/12', 'X 1 Apr to 1 Oct 2025')
    wX = q1c.add('578000-43350', 'WDV of X on 1 Oct 2025')
    lX = q1c.add('534650-450000', 'Loss on sale of X')
    dY2 = q1c.add('(300000-22500)*15/100', 'Y 2025-26')
    dZ2 = q1c.add('500000*15/100*6/12', 'Z 2025-26 (6 months)')
    cd2 = q1c.add('(277500-41625)+(500000-37500)', 'Balance c/d 31 Mar 2026')
    q1a = ledger('Machinery Account — 2024-25', [('2024 Apr 1', 'To Bank A/c (Machine X)', 640000), ('Apr 1', 'To Bank A/c (erection of X)', 40000), ('Oct 1', 'To Bank A/c (Machine Y)', 300000)],
                 [('2025 Mar 31', 'By Depreciation A/c (X 1,02,000 + Y 22,500)', dX1 + dY1)], '2025 Mar 31', '2025 Apr 1')
    q1b = ledger('Machinery Account — 2025-26', [('2025 Apr 1', 'To Balance b/d', cd1, True), ('Oct 1', 'To Bank A/c (Machine Z)', 500000)],
                 [('2025 Oct 1', 'By Depreciation A/c (X, 6 months)', dX2), ('Oct 1', 'By Bank A/c (sale of X)', 450000), ('Oct 1', 'By Profit and Loss A/c (loss on sale)', lX),
                  ('2026 Mar 31', 'By Depreciation A/c (Y 41,625 + Z 37,500)', dY2 + dZ2)], '2026 Mar 31', '2026 Apr 1')
    assert q1a['next']['amt'] == cd1 and q1b['next']['amt'] == cd2
    q1wn = table(['Particulars', 'Machine X (₹)', 'Machine Y (₹)', 'Machine Z (₹)'], [
        ['Cost', inr(X0), '3,00,000', ''],
        ['Depreciation 2024-25', '(1,02,000)', '(22,500)', ''],
        ['WDV 31 March 2025', '5,78,000', '2,77,500', ''],
        ['Additions 1 Oct 2025', '', '', '5,00,000'],
        ['Depreciation 2025-26', '(43,350)', '(41,625)', '(37,500)'],
        ['WDV at sale / year-end', inr(wX), '2,35,875', '4,62,500'],
        ['Sale proceeds', '(4,50,000)', '', ''],
        ['Loss on sale', inr(lX), '', ''],
    ], title='Working note — asset-wise WDV')

    # ============ Question 3: capitalisation ============
    q3c = Checks()
    q3_cost = q3c.add('1500000-75000+60000+45000+30000+25000-5000+20000', 'Cost of the machine')
    q3_dep = q3c.add('(1600000-100000)/10*6/12', 'Depreciation for 2026-27 (6 months, SLM)')
    q3t = table(['Item', 'Amount (₹)', 'Treatment'], [
        ['List price ₹15,00,000 less trade discount 5% (₹75,000)', '14,25,000', 'Capitalise net price'],
        ['GST ₹2,56,500 (input credit available)', '—', 'Recoverable — not cost'],
        ['Freight and transit insurance', '60,000', 'Capitalise — delivery'],
        ['Foundation and site preparation', '45,000', 'Capitalise'],
        ['Installation by supplier\'s engineers', '30,000', 'Capitalise'],
        ['Trial run: materials ₹25,000 less sale of test output ₹5,000', '20,000', 'Capitalise net cost of testing'],
        ['Consulting engineer\'s fee', '20,000', 'Capitalise — professional fee'],
        ['Inauguration ceremony ₹18,000', '—', 'Expense'],
        ['Training of operators ₹12,000', '—', 'Expense'],
        ['Advertisement of the new product ₹40,000', '—', 'Expense'],
        ['Cost of the machine', inr(q3_cost), ''],
    ], num=[1], total=True, title='What is capitalised')

    # ============ Question 4: estimates ============
    q4c = Checks()
    q4a = q4c.add('(900000-900000/10*3)/5', '(a) revised SLM depreciation from year 4')
    q4b = q4c.add('(1500000-1500000/10*2+90000)/8', '(b) depreciation after upward revaluation over remaining 8 years')
    q4c_ = q4c.add('(1800000-1800000/12*3)/6', '(c) amortisation after revised life')

    # ============ Case ============
    kc = Checks()
    k_c = kc.add('1150000+50000', 'Cost')
    k_y1 = kc.add('1200000*20/100*9/12', 'Year 1 depreciation (9 months)')
    k_y2 = kc.add('(1200000-180000)*20/100', 'Year 2 depreciation')
    k_bv = kc.add('1200000-180000-204000', 'Carrying amount at end of year 2')
    k_pl = kc.add('900000-816000', 'Profit on sale at start of year 3')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch05', 'n': 1,
        'title': 'Depreciation and Amortisation',
        'outcomes': [
            'Explain what depreciation is (and is not), why it is charged and what causes it.',
            'Work out the cost of an item of property, plant and equipment (PPE), its depreciable amount and useful life, including component accounting.',
            'Compute depreciation under the straight line, written down value, sum of years\' digits, machine hour, production units and depletion methods, with part-year periods.',
            'Record depreciation with and without a provision for depreciation account, and compute profit or loss on disposal using an asset disposal account.',
            'Account for a change in method, useful life or residual value (as a change in estimate) and for revaluation of PPE.',
            'Define intangible assets, apply the recognition conditions and compute amortisation.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 75}, 'prereq': ['fnd-p1-ch02-u02'],
                 'exam_tip': 'A 10-mark machinery account with additions and a sale is a favourite. Keep an asset-wise working note, charge part-year depreciation by months, and depreciate the sold asset up to the date of sale before working out the profit or loss.'},
        'concepts': [
            {'id': 'c1', 'title': 'What depreciation is',
             'body': ['Property, plant and equipment (PPE) are tangible items held for use in producing or supplying goods or services, for renting to others or for administration, and expected to be used for more than twelve months — machinery, buildings, vehicles, furniture. They are recorded at cost and help earn revenue (or save cost) over many years.',
                      'Depreciation spreads the depreciable amount of such an asset — its cost (or revalued amount) less its residual value — over its useful life in a systematic way. Schedule II to the Companies Act, 2013 describes it in these terms. Useful life is the period over which the entity expects to use the asset, or the number of units it expects to produce with it.',
                      'Causes of fall in value: wear and tear from use; passage of time even when idle; obsolescence (technology or demand changes); fall in market value; and depletion of natural resources such as mines.',
                      'Depreciation begins when the asset is available for use — in place and in the condition management intends — even if it is not yet actually used. Each year the expired part of the cost is charged as depreciation (matching), and the unexpired part stays in the balance sheet as the carrying amount (written down value). Depreciation is an allocation of cost, not a measure of current market value.'],
             'analogy': 'You buy a ₹60,000 phone you expect to use for 3 years. Its "cost per year" is about ₹20,000 — that yearly share is depreciation, whatever the resale price happens to be.',
             'work': 'Every company maintains a fixed asset register — asset-wise cost, date put to use, life, method, accumulated depreciation. Without it, depreciation and profit or loss on disposal cannot be computed reliably, and it is one of the first registers an auditor asks for.'},
            {'id': 'c2', 'title': 'Why depreciation is charged',
             'body': ['Correct profit: the use of the asset is a real cost of earning the year\'s revenue; ignoring it overstates profit.',
                      'True financial position: the asset should appear at its unexpired cost, not at its original cost.',
                      'Retention of funds for replacement: depreciation reduces divisible profit, so the money is kept in the business rather than distributed — though replacement may cost more due to inflation or technology.',
                      'Correct cost of production: depreciation of factory assets is part of product cost.',
                      'Depreciation is a non-cash expense — no money leaves the business when it is charged. It does not itself create funds; it only stops profits being over-distributed. It must be charged even in a loss year.'],
             'analogy': 'Setting aside part of your salary each month for the next phone does not create money — it just stops you spending all of it now.',
             'work': 'Lenders and analysts add depreciation back to profit to estimate cash generation (EBITDA). Understanding that depreciation is non-cash is basic to cash-flow work.'},
            {'id': 'c3', 'title': 'Measuring depreciation: cost, useful life, residual value',
             'body': ['Three estimates drive the charge: cost, useful life (in years or units, based on experience, expected usage, shifts, repairs policy, technology) and residual value (what the asset is expected to fetch at the end of its life after disposal costs; treated as nil if insignificant). Depreciable amount = cost (or revalued amount) − residual value.',
                      'Cost of PPE = the price paid to the supplier, plus import duties and purchase taxes that cannot be recovered, minus trade discounts and rebates; plus costs directly attributable to bringing the asset to the location and condition needed for its intended use; plus the initial estimate of dismantling, removal and site-restoration costs.',
                      'Directly attributable costs include employee costs arising directly from acquiring or building the asset, site preparation, initial delivery and handling, installation and assembly, testing (less the net sale proceeds of samples produced while testing), and professional fees such as engineers\' charges.',
                      'Not part of cost: opening a new facility (inauguration), introducing a new product (advertising), doing business in a new place or with a new class of customers (including staff training), administration and general overheads, costs incurred while the asset is ready but idle or running below capacity, and relocation costs. Later expenditure is capitalised only if it increases life or capacity; additions are depreciated over the remaining life, and an addition with a separate identity is accounted for as a separate asset.'],
             'blocks': [q3t],
             'analogy': 'Cost is everything you spent to get the machine standing in the factory and working — not the party to celebrate it, nor the advertisements for what it will make.',
             'work': 'Capitalisation reviews are routine in audits: capitalising revenue items (like training or inauguration) inflates profit and assets, so each addition is vouched to invoices and the "date ready for use" is checked.'},
            {'id': 'c4', 'title': 'Component accounting',
             'body': ['Both the accounting standards and Schedule II require each significant part of an asset to be depreciated separately when its cost is significant relative to the whole and its useful life or method differs from the rest.',
                      'An aircraft is the classic case: the airframe, the engines and the interiors have different lives. Parts with the same life and method may be grouped. Small parts replaced frequently can be expensed when replaced.'],
             'analogy': 'A car\'s body may last 15 years but its tyres only 3 — you would not spread the tyres\' cost over 15 years.',
             'work': 'When a large plant is commissioned, engineers and accountants together split the cost into components (civil works, main machinery, electricals, moulds) with separate lives in the fixed asset register.'},
            {'id': 'c5', 'title': 'Straight line and written down value methods',
             'body': ['Straight line method (SLM, fixed instalment): the same amount every year. Depreciation = (cost − residual value) ÷ useful life; rate = annual depreciation ÷ cost × 100. Simple and suited to assets that give equal benefit every year (leases, many plants). Weakness: repairs rise as the asset ages, so total charge (depreciation + repairs) rises over time.',
                      'Written down value method (WDV, reducing / diminishing balance): a fixed percentage of the opening carrying amount each year, so the charge falls every year. Rate = [1 − (residual value ÷ cost)^(1/n)] × 100. Heavy charge early when repairs are low, light charge later when repairs are high — roughly even total burden. The asset never reaches zero. Risks: too low a rate may leave the asset under-depreciated; residues of scrapped assets can linger if no plant register is kept. Income-tax rules use WDV (block of assets) except for certain power undertakings.',
                      'Under both methods, depreciation in the year of purchase or sale is only for the months the asset was available for use.',
                      'Recording: either credit the asset account each year (Depreciation A/c Dr, To Asset A/c), or keep the asset at cost and credit a Provision for Depreciation (accumulated depreciation) account (Depreciation A/c Dr, To Provision for Depreciation A/c). The second shows both the original investment and its carrying amount, and is preferred. In both cases Depreciation A/c is closed to the profit and loss account.'],
             'blocks': [cmp1],
             'analogy': 'SLM is paying the same EMI every month; WDV is like a battery that loses a fixed percentage of whatever charge is left.',
             'work': 'Companies often use SLM in their books (lives per Schedule II) but WDV for income tax, which creates deferred tax — a topic you will meet later. Explaining why "book depreciation" and "tax depreciation" differ is a common client conversation.'},
            {'id': 'c6', 'title': 'Other methods: SYD, machine hour, production units, depletion',
             'body': ['Sum of years\' digits (SYD): a variant of the reducing charge. Depreciation = depreciable amount × (remaining life at the start of the year, including that year) ÷ (sum of the digits 1 to n). For n years the sum is n(n + 1)/2. Not widely used.',
                      'Machine hour method: rate per hour = depreciable amount ÷ total estimated working hours; annual charge = hours worked × rate. It is the straight line idea applied per hour. Schedule II reflects it partly through extra depreciation for double or triple shift working of certain plant.',
                      'Production units method: depreciable amount × units produced this year ÷ total estimated units. Suitable for machines producing a uniform product.',
                      'Depletion method: for wasting assets such as mines, quarries, oil wells. Rate per unit = cost ÷ estimated total quantity extractable; charge = quantity extracted × rate.'],
             'blocks': [sydt],
             'analogy': 'Machine hour and production units charge "per use", like paying for a taxi by the kilometre rather than a fixed monthly rent.',
             'work': 'Mining and oil companies report depletion as a major expense; reserve estimates from geologists directly change the profit for the year.'},
            {'id': 'c7', 'title': 'Disposal of an asset — profit or loss',
             'body': ['When an asset is sold, first charge depreciation for the part of the year up to the date of sale. Then profit or loss = sale proceeds − carrying amount on that date. This goes to the profit and loss account.',
                      'All entries can be made in the asset account itself, or an Asset Disposal Account can be opened: transfer the asset\'s cost to it, transfer the accumulated depreciation (if a provision account is kept), credit the sale proceeds, and the balance is the profit or loss.',
                      'Keep an asset-wise working note — in an exam with several machines, it is the only safe way to get the right figures.'],
             'blocks': [disp2],
             'analogy': 'Selling your two-year-old phone: compare the price you get with the "unused" part of its cost, not with what you paid originally.',
             'work': 'In software, an asset sale voucher must remove both the gross cost and the accumulated depreciation; forgetting the second leaves ghost balances in the fixed asset schedule.'},
            {'id': 'c8', 'title': 'Changes in method, useful life and residual value',
             'body': ['Method, useful life and residual value are estimates and must be reviewed at least at each financial year-end.',
                      'A change in the depreciation method (made because the pattern in which the asset\'s benefits are consumed has changed significantly) is treated as a change in accounting estimate: the carrying amount on the date of change is depreciated under the new method from then on. Its effect is quantified and disclosed.',
                      'A change in useful life or residual value is also a change in estimate: the remaining depreciable amount (carrying amount − revised residual value) is spread over the revised remaining life. Past depreciation is not recalculated — the change is prospective.'],
             'analogy': 'If halfway through a road trip you learn the destination is closer, you change your speed from here on — you don\'t re-drive the part already covered.',
             'work': 'IT companies regularly shorten laptop and server lives because of faster obsolescence; the accountant computes the higher future charge and the note on change in estimate.'},
            {'id': 'c9', 'title': 'Revaluation of PPE',
             'body': ['After initial recognition, an entity may choose (it is an accounting policy, not compulsory) to carry PPE at a revalued amount — fair value at the revaluation date less later accumulated depreciation and impairment — if fair value can be measured reliably.',
                      'Rules: revalue regularly enough that carrying amounts stay close to fair value; revalue the entire class of assets, not selected items; an increase is credited to Revaluation Surplus in owners\' equity — except that it goes to profit and loss to the extent it reverses an earlier decrease of the same asset charged to profit and loss; a decrease is charged to profit and loss — except that it is debited to Revaluation Surplus to the extent of any surplus already existing for that asset.',
                      'The surplus can be moved straight to retained earnings once the asset is derecognised (retired or sold), or gradually as the extra depreciation on the revalued amount is charged — never through the profit and loss account. After revaluation, depreciation is based on the revalued amount over the remaining life.'],
             'analogy': 'Re-pricing every flat in a building, not just the one with the best view — otherwise the picture is selective.',
             'work': 'Real-estate-heavy companies that revalue land and buildings get valuers\' reports; auditors check that the whole class was revalued and that the surplus did not pass through profit.'},
            {'id': 'c10', 'title': 'Intangible assets',
             'body': ['An intangible asset is a non-monetary asset that can be identified separately and has no physical form, held for use in producing or supplying goods or services, for rental to others or for administration. Examples: patents, trademarks, copyrights, computer software, streaming and broadcasting rights, airport landing slots, film distribution rights, long-term customer contracts, customer databases and purchased goodwill.',
                      'It is recognised only if: it is identifiable (it could be sold, rented, licensed or exchanged separately); the entity controls it (can obtain its benefits and restrict others); future economic benefits are probable; and its cost can be measured reliably.',
                      'Cost of a separately acquired intangible = purchase price + non-recoverable duties and taxes + directly attributable costs of preparing it for use (for example legal fees), less trade discounts and rebates. It is removed from the balance sheet on disposal or when no further benefits are expected; the gain or loss (net proceeds − carrying amount) goes to profit and loss.',
                      'Tangible vs intangible: tangible assets have physical form and a life based on expected usage, and are depreciated; intangibles lack physical form, often have lives set by contract or law (purchased goodwill may even have an indefinite life), are presumed not to exceed ten years unless there is evidence otherwise, and are amortised.'],
             'analogy': 'A trademark is like a famous restaurant\'s name on the door — you can\'t touch its value, but you can sell or license it, and it brings customers in.',
             'work': 'Valuing customer contracts, brands and software on acquisitions is a big advisory area; at Foundation level, focus on the recognition tests and amortisation.'},
            {'id': 'c11', 'title': 'Amortisation',
             'body': ['Amortisation is depreciation of an intangible asset: its depreciable amount (cost − residual value) is spread systematically over the best estimate of its useful life, starting when the asset is available for use.',
                      'Useful life is presumed not to exceed ten years from the date of availability unless there is evidence to the contrary — software and similar assets may have much shorter lives; contractual rights for longer periods can be amortised over that longer period where evidence supports it.',
                      'Method should follow the pattern in which benefits are consumed; if that pattern cannot be determined reliably, use the straight line method. Residual value is assumed to be zero unless a third party has committed to buy the asset at the end of its life, or an active market exists that will give a residual value and is likely to exist at that time.',
                      'The period and method are reviewed at least at each year-end; significant changes are reflected prospectively.'],
             'blocks': [pat1],
             'analogy': 'A 5-year movie streaming licence is used up a little every year — amortisation records that using-up.',
             'work': 'Software licences and ERP implementation costs are common intangibles in client books; auditors check the start date (available for use) and the life chosen.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'SLM and WDV with a mid-year purchase', 'difficulty': 'core', 'minutes': 14,
             'q': 'Rahul Packaging bought a machine on 1 October 2026 for ₹8,40,000 and paid ₹60,000 for installation. Useful life 7 years, residual value ₹60,000. Books close on 31 March. (a) Prepare the Machinery Account for 2026-27 and 2027-28 under SLM (depreciation credited to the asset) and the Depreciation Account for 2026-27. (b) Compare with WDV at 20% p.a.',
             'solution': [wn('SLM charge', f'Cost = 8,40,000 + 60,000 = {R(cost1)}. Depreciation = (9,00,000 − 60,000) ÷ 7 = {R(slm)} a year; for 6 months in 2026-27 = {R(s1)}.'),
                          m1a, m1b, d1, cmp1,
                          note('Installation is part of cost, so depreciation is charged on ₹9,00,000. The machine was available for use for 6 months in 2026-27.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Provision for depreciation and a sale through the disposal account', 'difficulty': 'hard', 'minutes': 20,
             'q': 'Kiran Foods keeps machinery at cost with a Provision for Depreciation Account and charges 10% p.a. on original cost (SLM). Machine A was bought on 1 April 2024 for ₹5,00,000 and Machine B on 1 October 2025 for ₹3,00,000. Machine A was sold on 1 January 2027 for ₹3,40,000. Show the journal entries for 2026-27 relating to the sale and depreciation, and the Machinery, Provision for Depreciation and Machinery Disposal Accounts for 2026-27.',
             'solution': [wn('Accumulated depreciation on A', f'2024-25 {R(dA)} + 2025-26 {R(dA)} + 9 months of 2026-27 {R(dA27)} = {R(accA)}. Book value = 5,00,000 − {inr(accA)} = {R(bvA)}; sold for ₹3,40,000, loss {R(lossA)}.'),
                          journal(J2, 'Journal of Kiran Foods (2026-27)', 'j2'), mach2, prov2, disp2],
             'checks': c2},
            {'id': 'i3', 'title': 'SYD, machine hour, production units and depletion', 'difficulty': 'moderate', 'minutes': 14,
             'q': '(a) A machine costs ₹6,50,000, residual value ₹50,000, life 5 years — depreciation for each year by sum of years\' digits. (b) A press costs ₹18,00,000, residual value ₹2,00,000, estimated working life 20,000 hours or 1,60,000 units. In year 1 it worked 4,800 hours and produced 30,000 units — depreciation by machine hour and by production units. (c) A quarry lease costs ₹90,00,000 for an estimated 3,00,000 tonnes; 18,000 tonnes were extracted in year 1 — depletion charge.',
             'solution': [sydt,
                          wn('(b) Machine hour', f'Rate = (18,00,000 − 2,00,000) ÷ 20,000 = ₹{mh_rate} per hour; year 1 = 4,800 × {mh_rate} = {R(mh1)}.'),
                          wn('(b) Production units', f'16,00,000 × 30,000 ÷ 1,60,000 = {R(pu1)}.'),
                          wn('(c) Depletion', f'Rate = 90,00,000 ÷ 3,00,000 = ₹{dep_rate} per tonne; year 1 = 18,000 × {dep_rate} = {R(dep1)}.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Change in useful life, change in method, revaluation', 'difficulty': 'hard', 'minutes': 14,
             'q': '(a) A machine costing ₹12,00,000 was depreciated on SLM over 10 years (nil residual value) for 4 years. Its remaining life is now estimated at 4 years. Depreciation for year 5? (b) An asset costing ₹10,00,000 (residual value ₹1,00,000, life 9 years) was depreciated on SLM for 3 years; from year 4 the entity switches to WDV at 20%. Depreciation for year 4? (c) Another asset with a carrying amount of ₹7,00,000 is revalued at ₹8,40,000 at the end of a year; remaining life 7 years. Treatment and next year\'s depreciation?',
             'solution': [wn('(a) Change in useful life', f'Carrying amount after 4 years = 12,00,000 − 4 × 1,20,000 = {R(e_wdv)}. Spread over the revised remaining life of 4 years: {R(e_new)} a year. Past depreciation is not changed.'),
                          wn('(b) Change in method', f'SLM charge was {R(m_slm)} a year; carrying amount after 3 years = {R(m_wdv)}. Year 4 under WDV = 20% × {inr(m_wdv)} = {R(m_new)}. It is a change in estimate, applied from year 4 onwards.'),
                          wn('(c) Revaluation', f'Increase {R(r_sur)} is credited to Revaluation Surplus (equity), not to profit and loss. Next year\'s depreciation = 8,40,000 ÷ 7 = {R(r_dep)}.'),
                          journal([je('Year end', [('Machinery A/c', r_sur)], [('Revaluation Surplus A/c', r_sur)], 'Being upward revaluation of machinery credited to revaluation surplus')], 'Entry for (c)')],
             'checks': c4},
            {'id': 'i5', 'title': 'Amortisation of a patent', 'difficulty': 'core', 'minutes': 10,
             'q': 'Kavach Tech bought a patent on 1 August 2026 for ₹24,00,000 and paid ₹1,20,000 in legal and registration fees. The patent has a legal life of 15 years, but the company expects to benefit from it for 8 years; no residual value. Books close on 31 March. Show the Patent Account for 2026-27 and 2027-28 and the Amortisation Account for 2026-27.',
             'solution': [wn('Amortisation', f'Cost = {R(pat)}. Useful life is the shorter of the legal life and the expected period of benefit — 8 years. Annual charge = {R(am_y)}; 2026-27 (8 months) = {R(am1)}.'),
                          pat1, pat2, amo],
             'checks': c5},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Reviewing capital additions in an audit', 'role': 'Articled assistant on the audit of a manufacturer',
             'situation': 'The client capitalised ₹42 lakh for a new bottling line, including the inauguration function, operator training and three months of electricity while the line stood ready but waiting for orders.',
             'steps': ['Vouch the supplier invoice, freight, installation and commissioning bills — these belong in cost.',
                       'Remove the inauguration, training and idle-period electricity — these are expenses of the year.',
                       'Check the "available for use" date from commissioning reports; depreciation starts from that date even if production started later.',
                       'Check whether major parts (moulds, filling heads) need separate component lives.',
                       'Agree the corrected figure to the fixed asset register and recompute depreciation.'],
             'takeaway': 'What goes into cost decides depreciation for years to come — errors in capitalisation repeat every year until the asset is sold.',
             'think': 'If ₹3 lakh of training cost stays capitalised in a 10-year asset (SLM, nil residual), by how much is the current year\'s profit overstated?',
             'answer': 'Expense of ₹3,00,000 is avoided and only ₹30,000 depreciation is charged on it, so profit is overstated by ₹2,70,000.',
             'checks': [{'expr': '300000-300000/10', 'value': 270000, 'label': 'Profit overstated in year 1'}]},
            {'id': 'j2', 'title': 'Laptops wear out faster than planned', 'role': 'Finance executive at an IT services company',
             'situation': 'Laptops costing ₹60 lakh were being depreciated on SLM over 5 years with nil residual value. After 2 years, the IT head says they will last only 1 more year.',
             'steps': ['Carrying amount after 2 years = 60 − 24 = ₹36 lakh.',
                       'Treat the revised life as a change in estimate: ₹36 lakh over the remaining 1 year.',
                       'Do not restate the previous two years.',
                       'Disclose the nature and amount of the change in the notes.'],
             'takeaway': 'Changes in life, residual value or method are prospective: re-spread the carrying amount from now on.',
             'checks': [{'expr': '6000000-6000000/5*2', 'value': 3600000, 'label': 'Carrying amount after 2 years'}]},
        ],
        'mcqs': [
            M('m1', 'Depreciation is best described as:', ['Spreading an asset\'s cost less residual value over its useful life in a systematic way', 'Fall in the market value of an asset', 'A fund created to replace an asset', 'A cash expense of the year'], 0,
              'Depreciation allocates cost; it is not a valuation, does not create a fund and involves no cash outflow.', 'c1'),
            M('m2', 'Which of the following is NOT included in the cost of a machine?', ['Cost of the inauguration ceremony', 'Installation charges', 'Freight to bring it to the factory', 'Net cost of trial runs'], 0,
              'Opening a new facility is not a cost of bringing the asset to working condition.', 'c3'),
            M('m3', 'Cost ₹5,40,000; residual value ₹40,000; life 5 years. SLM depreciation per year:', ['₹1,00,000', '₹1,08,000', '₹1,16,000', '₹96,000'], 0,
              '(5,40,000 − 40,000) ÷ 5 = ₹1,00,000.', 'c5', 'core', '(540000-40000)/5'),
            M('m4', 'A machine costing ₹4,00,000 is depreciated at 10% WDV. Depreciation for the second year:', ['₹36,000', '₹40,000', '₹32,400', '₹44,000'], 0,
              'Year 1: 40,000; WDV 3,60,000; year 2: 10% × 3,60,000 = ₹36,000.', 'c5', 'core', '400000*0.9*0.1'),
            M('m5', 'Cost ₹5,00,000, residual value ₹2,04,800, life 4 years. The WDV rate that writes it down to residual value is:', ['20%', '25%', '14.76%', '18%'], 0,
              'Rate = 1 − (2,04,800 ÷ 5,00,000)^(1/4) = 1 − 0.8 = 20%.', 'c5', 'hard', '(1-(204800/500000)**0.25)*100'),
            M('m6', 'Under the sum of years\' digits method for a 4-year life, first-year depreciation is what fraction of the depreciable amount?', ['4/10', '1/4', '1/10', '4/16'], 0,
              'Sum of digits = 4 × 5 ÷ 2 = 10; first year uses the remaining life 4, so 4/10.', 'c6'),
            M('m7', 'Depreciable amount ₹24,00,000; estimated 60,000 hours; machine worked 7,500 hours this year. Depreciation:', ['₹3,00,000', '₹4,00,000', '₹2,40,000', '₹3,20,000'], 0,
              'Rate = ₹40 per hour; 7,500 × 40 = ₹3,00,000.', 'c6', 'core', '2400000/60000*7500'),
            M('m8', 'A mine is acquired for ₹1,20,00,000 with 4,00,000 tonnes extractable. 25,000 tonnes are extracted this year. Depletion:', ['₹7,50,000', '₹30,00,000', '₹4,80,000', '₹12,00,000'], 0,
              'Rate = ₹30 per tonne; 25,000 × 30 = ₹7,50,000.', 'c6', 'core', '12000000/400000*25000'),
            M('m9', 'An asset with a carrying amount of ₹2,40,000 on 1 April is sold on 1 October for ₹2,00,000. Depreciation is 10% WDV. Loss on sale:', ['₹28,000', '₹40,000', '₹16,000', '₹52,000'], 0,
              'Depreciation for 6 months = 12,000; carrying amount 2,28,000; loss = 2,28,000 − 2,00,000 = ₹28,000.', 'c7', 'moderate', '240000-240000*0.1*6/12-200000'),
            M('m10', 'A change in the estimated useful life of an asset is treated as:', ['A change in accounting estimate, applied prospectively', 'A change in accounting policy, applied retrospectively', 'A prior period item', 'An extraordinary item'], 0,
              'The remaining carrying amount is spread over the revised remaining life; past figures are not restated.', 'c8'),
            M('m11', 'Cost ₹6,00,000, SLM over 10 years with nil residual value, for 3 years; remaining life is then revised to 5 years. Depreciation for year 4:', ['₹84,000', '₹60,000', '₹1,20,000', '₹70,000'], 0,
              'Carrying amount 4,20,000 ÷ 5 = ₹84,000.', 'c8', 'moderate', '(600000-60000*3)/5'),
            M('m12', 'On the first revaluation of an asset, a decrease in its carrying amount is:', ['Charged to the profit and loss account', 'Debited to revaluation surplus', 'Ignored until the asset is sold', 'Debited to capital directly'], 0,
              'With no existing surplus for that asset, a revaluation decrease is an expense.', 'c9', 'moderate'),
            M('m13', 'If an entity revalues one item of plant, it must:', ['Revalue the entire class of plant', 'Revalue only that item', 'Revalue all its assets of every class', 'Revalue it only once in its life'], 0,
              'Revaluation applies to the whole class to avoid selective revaluation.', 'c9'),
            M('m14', 'Which of these is NOT an intangible asset?', ['Trade receivables', 'Patent', 'Computer software', 'Airport landing slots'], 0,
              'Receivables are monetary assets; an intangible asset is non-monetary.', 'c10'),
            M('m15', 'Unless there is evidence to the contrary, the useful life of an intangible asset is presumed not to exceed:', ['10 years', '5 years', '20 years', '15 years'], 0,
              'The presumption is ten years from the date the asset is available for use.', 'c11', 'core', '10'),
            M('m16', 'Streaming rights cost ₹18,00,000 for 10 years (SLM). At the start of year 4 the remaining life is revised to 6 years. Amortisation for year 4:', ['₹2,10,000', '₹1,80,000', '₹3,00,000', '₹1,26,000'], 0,
              'Carrying amount = 18,00,000 − 3 × 1,80,000 = 12,60,000; ÷ 6 = ₹2,10,000.', 'c11', 'moderate', '(1800000-180000*3)/6'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'ledger',
             'q': 'Bhavya Plastics closes its books on 31 March and charges depreciation at 15% p.a. on the written down value. On 1 April 2024 it bought Machine X for ₹6,40,000 and spent ₹40,000 on its erection. On 1 October 2024 it bought Machine Y for ₹3,00,000. On 1 October 2025 Machine X was sold for ₹4,50,000 and Machine Z was bought for ₹5,00,000 on the same date. Prepare the Machinery Account for 2024-25 and 2025-26 (no provision for depreciation account is kept).',
             'model': [q1a, q1b, q1wn],
             'scheme': [
                 {'id': 's1', 'pt': 'Erection capitalised — X at ₹6,80,000', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Depreciation 2024-25: X ₹1,02,000 and Y ₹22,500 (6 months)', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Account for 2024-25 balanced at ₹8,55,500', 'm': 1, 'skill': 'balancing'},
                 {'id': 's4', 'pt': 'Depreciation on X up to date of sale ₹43,350', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's5', 'pt': 'Loss on sale ₹84,650 transferred to P&L', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's6', 'pt': 'Year-end depreciation Y ₹41,625 and Z ₹37,500 (6 months)', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's7', 'pt': 'Account for 2025-26 balanced at ₹6,98,375', 'm': 1, 'skill': 'balancing'},
                 {'id': 's8', 'pt': 'Asset-wise working note and proper ledger format', 'm': 1, 'skill': 'presentation'},
             ],
             'remarks': ['The best scripts had an asset-wise working note; most errors came from scripts without one.', 'Many candidates forgot to depreciate Machine X for six months before computing the loss.', 'Full-year depreciation on Y in 2024-25 and on Z in 2025-26 was a common slip.'],
             'mistakes': ['Not capitalising erection charges.', 'Computing the loss on sale from the opening WDV.', 'Applying 15% to original cost (SLM) instead of WDV.'],
             'tips': ['Prepare the working note first, then copy the figures into the ledger.', 'Show the months (× 6/12) in the particulars column.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between the straight line method and the written down value method of depreciation.',
             'model': [table(['Basis', 'Straight line method', 'Written down value method'], [
                 ['Base for charge', 'Original cost (less residual value)', 'Opening carrying amount of each year'],
                 ['Annual charge', 'Same every year', 'Falls every year'],
                 ['Asset value at end', 'Can be reduced to nil or residual value', 'Never becomes nil'],
                 ['Total burden with repairs', 'Rises over time as repairs increase', 'Roughly even — high depreciation early, high repairs later'],
                 ['Suitability / use', 'Assets giving equal benefit (leases, many plants); common in books under Schedule II', 'Plant subject to rising repairs; used for income tax'],
             ])],
             'scheme': [
                 {'id': 's1', 'pt': 'Base of charge', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Constant vs falling charge', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': 'Value at end of life', 'm': 1, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Effect with repairs / suitability', 'm': 1, 'skill': 'concept'},
             ],
             'remarks': ['Good answers used a table; formulas alone did not earn marks.'],
             'mistakes': ['Saying WDV reduces the asset to zero.', 'Mixing up which method has a constant charge.'],
             'tips': ['Four clear bases are enough; add the formula only as a bonus line.']},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Sona Textiles bought a machine on 1 October 2026: list price ₹15,00,000, trade discount 5%, GST ₹2,56,500 (input credit available). It also paid freight and transit insurance ₹60,000, foundation and site preparation ₹45,000, installation by the supplier\'s engineers ₹30,000, trial-run materials ₹25,000 (test output sold for ₹5,000), consulting engineer\'s fee ₹20,000, inauguration ceremony ₹18,000, training of operators ₹12,000 and advertisement of the new product ₹40,000. The machine was ready for use on 1 October 2026. Useful life 10 years, residual value ₹1,00,000, SLM. Compute the cost of the machine and depreciation for the year ended 31 March 2027.',
             'model': [q3t, wn('Depreciation', f'(₹{inr(q3_cost)} − 1,00,000) ÷ 10 × 6/12 = {R(q3_dep)}.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Trade discount deducted; GST excluded', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Freight, site preparation, installation and engineer\'s fee capitalised', 'm': 1.5, 'skill': 'application'},
                 {'id': 's3', 'pt': 'Trial run capitalised net of sale of test output', 'm': 1, 'skill': 'application'},
                 {'id': 's4', 'pt': 'Inauguration, training and advertisement expensed', 'm': 1, 'skill': 'application'},
                 {'id': 's5', 'pt': f'Cost {R(q3_cost)} and depreciation {R(q3_dep)} (6 months)', 'm': 1.5, 'skill': 'computation'},
             ],
             'remarks': ['Many capitalised training cost; it is a cost of doing business with new equipment, not of the equipment.', 'Some forgot the six-month period.'],
             'mistakes': ['Adding recoverable GST to cost.', 'Capitalising the gross trial-run cost without deducting test-output sales.'],
             'tips': ['Use a three-column table: item | amount | treatment — it shows your reasoning.']},
            {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Compute the charge for the year in each case: (a) A machine costing ₹9,00,000, SLM over 10 years (nil residual value), was depreciated for 3 years; its remaining life is then estimated at 5 years — depreciation for year 4. (b) Plant costing ₹15,00,000, SLM over 10 years (nil residual value), was depreciated for 2 years and then revalued upwards by ₹90,000; remaining life unchanged — depreciation for year 3 and treatment of the increase. (c) Software rights costing ₹18,00,000 were amortised on SLM over 12 years for 3 years; the remaining life is then revised to 6 years — amortisation for year 4.',
             'model': [wn('(a)', f'Carrying amount = 9,00,000 − 3 × 90,000 = 6,30,000; ÷ 5 = {R(q4a)}.'),
                       wn('(b)', f'Carrying amount = 15,00,000 − 2 × 1,50,000 = 12,00,000; revalued amount 12,90,000. The ₹90,000 increase is credited to Revaluation Surplus. Year 3 depreciation = 12,90,000 ÷ 8 remaining years = {R(q4b)}.'),
                       wn('(c)', f'Carrying amount = 18,00,000 − 3 × 1,50,000 = 13,50,000; ÷ 6 = {R(q4c_)}.')],
             'checks': q4c,
             'scheme': [
                 {'id': 's1', 'pt': f'(a) {R(q4a)} — carrying amount over revised life', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's2', 'pt': '(b) increase credited to revaluation surplus, not P&L', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': '(b) ₹1,61,250 — revalued amount over remaining 8 years', 'm': 1, 'skill': 'computation'},
                 {'id': 's4', 'pt': f'(c) {R(q4c_)}', 'm': 1.5, 'skill': 'computation'},
             ],
             'remarks': ['Some candidates recomputed past depreciation — changes in estimate are prospective.', 'In (b), several credited the increase to profit and loss.'],
             'mistakes': ['Dividing the carrying amount by the original remaining life.', 'Spreading the revalued amount over 10 years instead of the remaining 8.'],
             'tips': ['Write "carrying amount ÷ remaining life" as a formula line first; it earns a step mark.']},
        ],
        'revision': {
            'summary': ['Depreciation = systematic spreading of (cost − residual value) over useful life; an allocation, not a valuation; non-cash.',
                        'Causes: wear and tear, passage of time, obsolescence, fall in market value, depletion. Starts when available for use.',
                        'Cost of PPE: price less trade discount + non-refundable taxes + directly attributable costs + dismantling estimate. Not: inauguration, advertising, training, admin, idle-time costs, relocation.',
                        'Methods: SLM (constant), WDV (falling), SYD, machine hour, production units, depletion.',
                        'Disposal: depreciate to date of sale; profit/loss = proceeds − carrying amount.',
                        'Change in method / life / residual value = change in estimate — prospective.',
                        'Revaluation: whole class; increase → revaluation surplus; decrease → P&L (subject to reversals).',
                        'Intangibles: identifiable, control, probable benefits, reliable cost; amortise, presumed life ≤ 10 years, SLM if pattern unclear, residual nil normally.'],
            'remember': ['SLM = (Cost − RV) ÷ life. WDV rate = 1 − (RV/Cost)^(1/n).', 'SYD denominator = n(n + 1)/2.', 'Part-year: count months available for use.', 'Provision method: asset stays at cost; accumulated depreciation is transferred to the disposal account on sale.'],
            'traps': ["Don't skip depreciation for the part-year before a sale.", "Don't capitalise training or inauguration costs.", "Don't restate past years for a change in estimate.", "Don't credit a revaluation increase to profit (unless it reverses an earlier charge)."],
        },
        'quickref': [
            {'k': 'Depreciable amount', 'v': 'Cost (or revalued amount) − Residual value'},
            {'k': 'SLM', 'v': '(Cost − Residual value) ÷ Useful life'},
            {'k': 'WDV rate', 'v': '[1 − (Residual value ÷ Cost)^(1/n)] × 100'},
            {'k': 'SYD', 'v': 'Depreciable amount × remaining life ÷ [n(n + 1)/2]'},
            {'k': 'Machine hour / units', 'v': 'Depreciable amount × hours (units) this year ÷ total hours (units)'},
            {'k': 'Depletion', 'v': 'Cost ÷ total quantity × quantity extracted'},
            {'k': 'Provision method entry', 'v': 'Depreciation A/c Dr. To Provision for Depreciation A/c'},
            {'k': 'Change in estimate', 'v': 'Carrying amount (− revised RV) ÷ revised remaining life'},
            {'k': 'Intangible life', 'v': 'Presumed ≤ 10 years from availability unless evidence otherwise'},
        ],
        'viva': [
            V('v1', 'What is depreciation? Is it a method of valuing an asset?',
              'Depreciation means spreading the depreciable amount of an asset, that is its cost less residual value, systematically over its useful life. It is a process of allocation of cost, not of valuation, so it does not show the market value of the asset. It is a non-cash expense.',
              [P('p1', 'Systematic allocation / spreading of cost over useful life', 4, 'allocat|spread|distribut|charg|writ off|write off|writing off', 'useful life|life of the asset|life of asset|working life|economic life|life', min=2),
               P('p2', 'Depreciable amount = cost less residual value', 2, 'cost less residual|cost minus residual|cost less scrap|cost minus scrap|depreciable amount|less residual|minus residual|less scrap|minus scrap|less salvage|minus salvage', min=1),
               P('p3', 'Not a valuation — does not show market value', 3, 'not valuation|not a valuation|not of valuation|not a method of valuation|not a method of valuing|not valu|isn t valu|is not valu|not market value|not show market|not the market|no relation market|not a process of valuation|allocation not valuation|not valuing|nothing to do with market|not about market'),
               P('p4', 'Non-cash expense', 1, 'non cash|noncash|no cash|without cash|not involve cash|not a cash|no outflow|no cash outflow')], 'c1'),
            V('v2', 'What factors are considered in measuring depreciation?',
              'Three factors: the cost of the asset including installation and other costs to make it ready for use, the estimated useful life in years or in units of production, and the estimated residual or scrap value at the end of its life.',
              [P('p1', 'Cost of the asset (incl. installation etc.)', 3, 'cost|not just the cost|not only the cost|not just cost'),
               P('p2', 'Estimated useful life (years or units)', 4, 'useful life|life of the asset|working life|economic life|expected life|estimated life|life'),
               P('p3', 'Estimated residual / scrap value', 3, 'residual|scrap|salvage|realisable at end|break up')], 'c3'),
            V('v3', 'Distinguish between the straight line method and the written down value method.',
              'Under the straight line method depreciation is charged at the same amount every year on the original cost, and the asset can be written down to nil or its residual value. Under the written down value method a fixed percentage is charged on the reducing opening balance, so the charge falls every year and the asset never becomes nil.',
              [P('p1', 'SLM: same/fixed amount every year on original cost', 5, 'straight line same|straight line equal|straight line fixed amount|straight line constant|straight line uniform|straight line charg same|straight line charg equal|straight line charg constant|slm same|slm equal|slm constant|slm fixed amount|slm uniform|slm give constant|slm charg same|fixed instalment same|fixed instalment equal|fixed instalment constant'),
               P('p2', 'WDV: fixed % on reducing balance — charge falls every year', 5, 'written down fixed|written down rate|written down percent|written down reduc|written down fall|written down decreas|written down declin|wdv fixed|wdv rate|wdv percent|wdv reduc|wdv fall|wdv decreas|wdv appl|reducing balance|diminishing balance|reducing opening balance')], 'c5'),
            V('v4', 'How do you account for a change in the estimated useful life of an asset?',
              'A change in useful life is a change in accounting estimate. It is applied prospectively: the carrying amount on the date of the change, less any residual value, is spread over the revised remaining useful life. Depreciation of past years is not recalculated.',
              [P('p1', 'Change in accounting estimate', 3, 'change in estimate|change in accounting estimate|accounting estimate|estimate change|revision of estimate|change of estimate'),
               P('p2', 'Carrying amount spread over revised remaining life', 4, 'carrying amount|written down value|wdv|book value|remaining depreciable amount|balance amount|unamortised|undepreciated|net book value', 'remaining life|revised life|revised remaining|remaining useful|balance life|new life|rest of the life|remaining period|remaining years', min=2),
               P('p3', 'Prospective — past depreciation not recalculated', 3, 'prospective|future only|from now on|going forward|onwards|past not|not recalculat|not restat|no restat|not change past|not revise past|past depreciation unchanged|past depreciation is not|past years are not|previous years not|not retrospective|not retrospectively|never retrospective|never restat|never recalculat|no retrospective', min=1)], 'c8'),
            V('v5', 'On revaluation of property, plant and equipment, how are an increase and a decrease in carrying amount treated?',
              'An increase is credited to revaluation surplus in owners\' equity, except to the extent it reverses an earlier decrease of the same asset charged to profit and loss. A decrease is charged to profit and loss, except to the extent there is an existing revaluation surplus for that asset, which is debited first. The whole class of assets must be revalued.',
              [P('p1', 'Increase → revaluation surplus (equity)', 4, 'increase credit revaluation surplus|increase revaluation surplus|increase to revaluation surplus|increase go revaluation surplus|increase goes to revaluation surplus|increase is credited to revaluation surplus|increase is credited to the revaluation surplus|upward revaluation surplus|upward to revaluation surplus|surplus for increase|increase credited to revaluation reserve|increase revaluation reserve|increase to revaluation reserve|gain revaluation surplus|gain to revaluation surplus|increase equity'),
               P('p2', 'Decrease → profit and loss', 4, 'decrease charg profit loss|decrease profit loss|decrease to profit|decrease is charged to profit|decrease is charged to the profit|decrease debit profit|decrease expense|decrease go profit|decrease goes to profit|downward profit loss|downward to profit|downward charg profit|decrease to the statement of profit|decrease recognis profit|decrease recognised in profit|loss profit loss|decrease p and l'),
               P('p3', 'Exceptions: reversals of earlier movements of the same asset; whole class revalued', 2, 'revers|existing surplus|earlier|previous|whole class|entire class|all assets of the class|same class', min=1)], 'c9'),
            V('v6', 'What is an intangible asset, and when can it be recognised?',
              'An intangible asset is a non-monetary asset that can be identified separately and has no physical substance; it is held for use in production or supply of goods or services, for rental or for administration. It is recognised only when it is identifiable, the enterprise controls it, future economic benefits are probable, and its cost can be measured reliably.',
              [P('p1', 'Identifiable, non-monetary, without physical substance', 4, 'without physical|no physical|not physical|lack physical|cannot be touched|can t be touched|cannot touch|cannot see|intangible', 'non monetary|nonmonetary|not monetary|identifiable|no physical form identifiable|no physical substance identifiable|no physical existence identifiable', min=2),
               P('p2', 'Recognition: control + probable future benefits', 3, 'control', 'future economic benefit|future benefit|economic benefit|probable', min=2),
               P('p3', 'Recognition: cost measurable reliably', 3, 'measur reliabl|reliably measur|reliable measur|measured reliably|cost reliabl|cost can be measured|reliable cost|reliably')], 'c10'),
            V('v7', 'What is amortisation, and what useful life is presumed for an intangible asset?',
              'Amortisation means spreading the depreciable amount of an intangible asset systematically over its useful life, starting when it is available for use. The useful life is presumed not to exceed ten years unless there is evidence to the contrary, and the straight line method is used if the pattern of benefits cannot be determined reliably.',
              [P('p1', 'Amortisation = depreciation of an intangible / allocation over useful life', 4, 'intangible', 'allocat|spread|writ off|write off|depreciation|charg', min=2),
               P('p2', 'Presumed life not more than 10 years unless evidence otherwise', 4, 'not exceed 10|not more than 10|10 years|maximum 10|up to 10|upto 10|within 10|ten year'),
               P('p3', 'Straight line if pattern not reliably determinable', 2, 'straight line|slm|evidence|available for use', min=1)], 'c11'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Nova Prints — a press bought, used and sold', 'difficulty': 'hard',
            'case': ('Nova Prints (year-end 31 March) bought a printing press on 1 July 2025 for ₹11,50,000 and paid ₹50,000 for installation. It charges depreciation at 20% p.a. on the written down value. '
                     'On 1 April 2027 the press was sold for ₹9,00,000. No provision for depreciation account is kept.'),
            'mcqs': [
                M('k1a', 'Depreciation for 2025-26 is:', [R(k_y1), '₹2,40,000', '₹1,72,500', '₹2,30,000'], 0,
                  f'Cost {R(k_c)} × 20% × 9/12 = {R(k_y1)} (July to March).', 'c5', 'moderate', '1200000*20/100*9/12'),
                M('k1b', 'Depreciation for 2026-27 is:', [R(k_y2), '₹2,40,000', '₹1,80,000', '₹1,92,000'], 0,
                  f'WDV 10,20,000 × 20% = {R(k_y2)}.', 'c5', 'moderate', '(1200000-180000)*20/100'),
                M('k1c', 'The carrying amount on 1 April 2027 is:', [R(k_bv), '₹7,68,000', '₹8,40,000', '₹7,80,000'], 0,
                  f'12,00,000 − 1,80,000 − 2,04,000 = {R(k_bv)}.', 'c7', 'hard', '1200000-180000-204000'),
                M('k1d', 'The result of the sale is:', [f'Profit {R(k_pl)}', 'Loss ₹84,000', 'Profit ₹1,32,000', 'Loss ₹3,00,000'], 0,
                  f'Proceeds 9,00,000 − carrying amount {R(k_bv)} = profit {R(k_pl)}, credited to profit and loss. No depreciation is charged for 2027-28 because the press was sold on the first day.', 'c7', 'hard'),
            ]}],
    }
