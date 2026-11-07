"""CA Foundation · Paper 1 Accounting · Chapter 10 Partnership and LLP Accounts · Unit 5 Death of a Partner.
Original explanations, names and numbers (structure and scope follow the ICAI study material).
Law: Section 37, Indian Partnership Act, 1932 (outgoing partner's share of subsequent profits or interest @6% p.a.)."""
from fractions import Fraction as F
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M
from fnd_p1_ch10_u03 import tacc, capacc, split, ratio
from fnd_p1_ch10_u04 import loan_schedule, loan_ledgers

UID = 'fnd-p1-ch10-u05'


def build():
    # ============ Illustration 1: Section 37 option ============
    c1 = Checks()
    opt_a = c1.add('66000*240000/550000', "Share of profit attributable to use of S's share of property")
    opt_b = c1.add('240000*6/100*6/12', 'Interest @6% p.a. for 6 months')
    c1.add('28800-7200', 'Advantage of option (a)')
    s37 = table(['Option under Section 37', 'Working', 'Amount (₹)'], [
        ['(a) Share of profits earned since death, attributable to the use of his share of the firm\'s property', '66,000 × 2,40,000 ÷ 5,50,000', inr(opt_a)],
        ['(b) Interest @6% p.a. on his share in the property of the firm', '2,40,000 × 6% × 6/12', inr(opt_b)],
    ], title='Amount payable to Sameer\'s legal representatives for 1 October 2026 – 31 March 2027',
        note='The representatives will choose (a). They need not choose until the profit figure for option (a) is known. If the deed had given the surviving partners an option to buy out the deceased\'s share and that option had been duly exercised, no further share of profit would be payable.')
    E1 = [je('2027 Mar 31', [('Profit and Loss A/c', opt_a)], [("Sameer's Executor A/c", opt_a)], "Being share of post-death profit credited to Sameer's executor under Section 37 (option chosen by the executor)")]

    # ============ Illustration 2: profit up to date of death ============
    c2 = Checks()
    t_firm = c2.add('360000*4/12', 'Time basis: profit for 4 months (1 April – 31 July)')
    t_u = c2.add('120000*3/10', "Time basis: Uday's 3/10 share")
    rate = c2.add('360000/2400000*100', 'Turnover basis: profit as % of last year\'s sales')
    s_firm = c2.add('900000*15/100', 'Turnover basis: profit on sales up to death')
    s_u = c2.add('135000*3/10', "Turnover basis: Uday's share")
    pt = table(['Basis', 'Working', 'Profit of firm to date of death (₹)', "Uday's share 3/10 (₹)"], [
        ['Time basis (profit assumed to accrue evenly)', '3,60,000 × 4/12', inr(t_firm), inr(t_u)],
        ['Turnover basis (same profit margin as last year)', f'9,00,000 × {rate:g}%', inr(s_firm), inr(s_u)],
    ], title='Uday\'s share of profit from 1 April 2026 to 31 July 2026')
    E2 = [je('2026 Jul 31', [('Profit and Loss Suspense A/c', s_u)], [("Uday's Capital A/c", s_u)], "Being Uday's share of profit up to the date of death (turnover basis) credited to his capital")]

    # ============ Illustration 3: full settlement of a deceased partner ============
    c3 = Checks()
    oldW = {'Vikram': F(3, 6), 'Wasim': F(2, 6), 'Yash': F(1, 6)}
    res = split(60000, oldW); rv = split(18000, oldW)
    gw_W = c3.add('180000*2/6', "Wasim's share of goodwill")
    gV = c3.add('60000*3/4', 'Debited to Vikram (gaining ratio 3:1)'); gY = c3.add('60000*1/4', 'Debited to Yash')
    ioc = c3.add('160000*10/100*3/12', 'Interest on capital @10% p.a. for 3 months')
    pls = c3.add('240000*3/12*2/6', 'Share of profit to date of death (time basis)')
    jlp = split(300000, oldW)
    c3.add('300000*2/6', "Wasim's share of JLP")
    due = c3.add('160000+20000+6000+60000+4000+20000+100000-12000', 'Amount transferred to executor')
    c3.add('358000-158000', 'Balance left with the firm as loan')
    E3 = [
        je('2026 Jun 30', [('General Reserve A/c', 60000)], [("Vikram's Capital A/c", res['Vikram']), ("Wasim's Capital A/c", res['Wasim']), ("Yash's Capital A/c", res['Yash'])], 'Being reserve distributed in 3:2:1'),
        je('Jun 30', [('Revaluation A/c', 18000)], [("Vikram's Capital A/c", rv['Vikram']), ("Wasim's Capital A/c", rv['Wasim']), ("Yash's Capital A/c", rv['Yash'])], 'Being revaluation profit distributed in 3:2:1'),
        je('Jun 30', [("Vikram's Capital A/c", gV), ("Yash's Capital A/c", gY)], [("Wasim's Capital A/c", gw_W)], "Being Wasim's share of goodwill debited to the gaining partners in 3:1"),
        je('Jun 30', [('Interest on Capital A/c', ioc)], [("Wasim's Capital A/c", ioc)], 'Being interest on capital up to the date of death'),
        je('Jun 30', [('Profit and Loss Suspense A/c', pls)], [("Wasim's Capital A/c", pls)], 'Being share of profit for 3 months up to death'),
        je('Jun 30', [('Bank A/c', 300000)], [('Joint Life Policy A/c', 300000)], 'Being policy money received from the insurer'),
        je('Jun 30', [('Joint Life Policy A/c', 300000)], [("Vikram's Capital A/c", jlp['Vikram']), ("Wasim's Capital A/c", jlp['Wasim']), ("Yash's Capital A/c", jlp['Yash'])], 'Being policy amount credited to all partners in 3:2:1'),
        je('Jun 30', [("Wasim's Capital A/c", 12000)], [("Wasim's Drawings A/c", 12000)], 'Being drawings transferred to capital'),
        je('Jun 30', [("Wasim's Capital A/c", due)], [("Wasim's Executor A/c", due)], "Being balance due transferred to the executor's account"),
        je('Jul 1', [("Wasim's Executor A/c", 158000)], [('Bank A/c', 158000)], 'Being part payment made to the executor'),
    ]
    wcap = {'t': 'ledger', 'ac': "Wasim's Capital Account", 'from': 'j3',
            'dr': [{'date': 'Jun 30', 'part': "To Wasim's Drawings A/c", 'amt': 12000}, {'date': 'Jun 30', 'part': "To Wasim's Executor A/c", 'amt': due}],
            'cr': [{'date': 'Apr 1', 'part': 'By Balance b/d', 'amt': 160000, 'ob': True}, {'date': 'Jun 30', 'part': 'By General Reserve A/c', 'amt': res['Wasim']},
                   {'date': 'Jun 30', 'part': 'By Revaluation A/c', 'amt': rv['Wasim']}, {'date': 'Jun 30', 'part': 'By Vikram and Yash (goodwill)', 'amt': gw_W},
                   {'date': 'Jun 30', 'part': 'By Interest on Capital A/c', 'amt': ioc}, {'date': 'Jun 30', 'part': 'By Profit and Loss Suspense A/c', 'amt': pls},
                   {'date': 'Jun 30', 'part': 'By Joint Life Policy A/c', 'amt': jlp['Wasim']}]}
    rows3, ti3, pays3, c3b = loan_schedule(200000, 2, 6, "Executor's balance")
    c3.extend(c3b)
    sched3 = table(['Year to 30 June', 'Opening balance (₹)', 'Interest @6% (₹)', 'Principal instalment (₹)', 'Total paid (₹)', 'Closing balance (₹)'], rows3, num=[2, 3, 4], total=True, title='Payment of the balance to Wasim\'s executor')
    exe = {'t': 'ledger', 'ac': "Wasim's Executor Account (to 30 June 2027)",
           'dr': [{'date': '2026 Jul 1', 'part': 'To Bank A/c', 'amt': 158000}, {'date': '2027 Jun 30', 'part': 'To Bank A/c (1,00,000 + 12,000)', 'amt': 112000}, {'date': '2027 Jun 30', 'part': 'To Balance c/d', 'amt': 100000, 'bal': True}],
           'cr': [{'date': '2026 Jun 30', 'part': "By Wasim's Capital A/c", 'amt': due}, {'date': '2027 Jun 30', 'part': 'By Interest A/c (6% on 2,00,000)', 'amt': 12000}],
           'next': {'date': '2027 Jul 1', 'side': 'cr', 'amt': 100000}}

    # ============ Illustration 4: JLP methods and separate policies on death ============
    c4 = Checks()
    oldK = {'Kiran': F(2, 5), 'Leela': F(2, 5), 'Mohan': F(1, 5)}
    m1 = split(200000, oldK); g2 = c4.add('200000-30000', 'Method 2/3: gain over surrender value carried in books'); m2 = split(g2, oldK); m3r = split(30000, oldK)
    c4.add('170000*2/5', "Leela's share of the gain (methods 2 and 3)")
    c4.add('68000+12000', "Leela's total under method 3 (gain + reserve)")
    jt = table(['Method', 'In the books before death', 'Entries on Leela\'s death (policy ₹2,00,000 received)', "Credit to Leela (₹)"], [
        ['1. Premium charged to P&L', 'Nothing', 'Bank Dr ₹2,00,000 To JLP; JLP Dr ₹2,00,000 To capitals 80,000 : 80,000 : 40,000', inr(m1['Leela'])],
        ['2. Policy kept at surrender value', 'JLP ₹30,000', 'Bank Dr ₹2,00,000 To JLP; JLP Dr ₹1,70,000 (balance) To capitals 68,000 : 68,000 : 34,000', inr(m2['Leela'])],
        ['3. Policy at surrender value + JLP Reserve', 'JLP ₹30,000; JLP Reserve ₹30,000', 'As in method 2, plus JLP Reserve Dr ₹30,000 To capitals 12,000 : 12,000 : 6,000', '80,000 (68,000 + 12,000)'],
    ], title='(a) Joint life policy — Kiran, Leela and Mohan share 2:2:1', note='Under method 2 Leela gets only ₹68,000 extra because her share of the ₹30,000 already in the books was credited to partners in earlier years through lower charges to profit.')
    sep_total = c4.add('150000+30000+15000', 'Policy value of Leela + surrender values of the others')
    sp = split(sep_total, oldK)
    c4.add('195000*2/5', "Leela's executor's share")
    E4 = [
        je('(b)', [("Separate Life Policy (Leela) A/c", 150000), ("Separate Life Policy (Kiran) A/c", 30000), ("Separate Life Policy (Mohan) A/c", 15000)],
           [("Leela's Executor A/c", sp['Leela']), ("Kiran's Capital A/c", sp['Kiran']), ("Mohan's Capital A/c", sp['Mohan'])],
           "Being Leela's policy amount and the surrender values of the surviving partners' policies credited in 2:2:1"),
        je('(b)', [('Bank A/c', 150000)], [("Separate Life Policy (Leela) A/c", 150000)], "Being the amount received on Leela's policy"),
    ]

    # ============ Questions ============
    qc1 = Checks()
    q1a = qc1.add('48000*250000/500000', 'Share of profits attributable to use of his share of property')
    q1b = qc1.add('250000*6/100*3/12', 'Interest @6% p.a. for 3 months')
    qc2 = Checks()
    q2p = qc2.add('2000000*450000/3000000*2/5', "Esha's share of profit to death (turnover basis, 15%)")
    q2i = qc2.add('200000*9/100*7/12', 'Interest on capital @9% for 7 months')
    q2g = qc2.add('250000*2/5', "Esha's share of goodwill")
    qc2.add('3/5-2/5', 'Dinesh gains 1/5'); qc2.add('2/5-1/5', 'Fatima gains 1/5 → gaining ratio 1:1')
    q2j = qc2.add('(250000-45000)*2/5', "Esha's share of JLP gain over book value")
    q2jr = qc2.add('45000*2/5', "Esha's share of JLP reserve")
    q2rl = qc2.add('15000*2/5', "Esha's share of revaluation loss")
    q2due = qc2.add('200000+16000+100000+10500+120000+82000+18000-21000-6000', 'Amount transferred to executor')
    q2int = qc2.add('300000*6/100*5/12', 'Interest to executor 1 Nov – 31 Mar @6%')
    ecap = {'t': 'ledger', 'ac': "Esha's Capital Account",
            'dr': [{'date': 'Oct 31', 'part': "To Esha's Drawings A/c", 'amt': 21000}, {'date': 'Oct 31', 'part': 'To Revaluation A/c (loss)', 'amt': q2rl}, {'date': 'Oct 31', 'part': "To Esha's Executor A/c", 'amt': q2due}],
            'cr': [{'date': 'Apr 1', 'part': 'By Balance b/d', 'amt': 200000, 'ob': True}, {'date': 'Oct 31', 'part': 'By General Reserve A/c', 'amt': 16000},
                   {'date': 'Oct 31', 'part': 'By Dinesh and Fatima (goodwill)', 'amt': q2g}, {'date': 'Oct 31', 'part': 'By Interest on Capital A/c', 'amt': q2i},
                   {'date': 'Oct 31', 'part': 'By Profit and Loss Suspense A/c', 'amt': q2p}, {'date': 'Oct 31', 'part': 'By Joint Life Policy A/c', 'amt': q2j},
                   {'date': 'Oct 31', 'part': 'By Joint Life Policy Reserve A/c', 'amt': q2jr}]}
    eexe = {'t': 'ledger', 'ac': "Esha's Executor Account",
            'dr': [{'date': '2026 Oct 31', 'part': 'To Bank A/c', 'amt': 219500}, {'date': '2027 Mar 31', 'part': 'To Balance c/d', 'amt': 300000 + q2int, 'bal': True}],
            'cr': [{'date': '2026 Oct 31', 'part': "By Esha's Capital A/c", 'amt': q2due}, {'date': '2027 Mar 31', 'part': 'By Interest A/c (6% on 3,00,000 for 5 months)', 'amt': q2int}],
            'next': {'date': '2027 Apr 1', 'side': 'cr', 'amt': 300000 + q2int}}
    assert q2due == 519500
    qc4 = Checks()
    q4t = qc4.add('288000*5/12*1/4', "Gita's share — time basis")
    q4r = qc4.add('288000/1920000*100', 'Profit as % of sales')
    q4s = qc4.add('960000*15/100*1/4', "Gita's share — turnover basis")

    # ============ Case ============
    kc = Checks()
    k_p = kc.add('180000*5/12*1/4', "Pia's share of profit to death (time basis)")
    k_j = kc.add('(400000-60000)*1/4', "Pia's share of JLP gain")
    k_due = kc.add('120000+18750+85000', 'Total due to Pia')
    k_int = kc.add('223750*6/100*4/12', 'Interest @6% for 4 months')

    concepts = [
        {'id': 'c1', 'title': 'Death of a partner — like retirement, with a few extra steps',
         'body': ['On the death of a partner the surviving partners usually continue the business (reconstitution). The accounting is close to retirement: revalue assets and liabilities, distribute reserves, adjust goodwill and deal with the joint life policy — all in the old ratio up to the date of death, with goodwill borne by the gaining partners.',
                  'Three things are special to death: (1) death can happen on any day, so the deceased partner\'s share of profit from the last balance sheet date to the date of death must be estimated; (2) a joint life policy actually matures and the full policy amount is received; (3) the amount due is paid to the legal representatives (executors), not to the partner, and the deceased\'s capital is transferred to an Executor\'s Account.'],
         'analogy': 'Retirement is a planned exit with notice; death is a sudden exit, so the accountant must also work out "profit till today" on an estimate.',
         'work': 'Families of a deceased partner often depend on the settlement. Accountants must be fair, prompt and able to explain every figure to people who are not accountants.'},
        {'id': 'c2', 'title': 'Section 37: share of subsequent profits or 6% interest',
         'body': ['Provision: under Section 37 of the Indian Partnership Act, 1932, if a partner dies or leaves the firm in any other way and the others carry on the business with the firm\'s property without settling his account, then — unless there is a contract to the contrary — he or his estate may choose either (a) the share of profits made since he ceased to be a partner that is attributable to the use of his share of the firm\'s property, or (b) interest at 6% per annum on his share of the property.',
                  'The choice is with the outgoing partner or his representatives, and they need not decide until the profit figure is known.',
                  'Exception: if the deed gives the continuing partners an option to buy the outgoing partner\'s interest and they exercise it properly, no further share of profits is due. If they do not comply with its terms in all material respects, Section 37 applies.',
                  'In exam questions the share of profit "attributable to the use of his share of property" is usually taken as profit × his capital ÷ total capital.'],
         'analogy': 'If someone keeps using your share of a shop without paying you, the law lets you take either your fair share of what the shop earned or simple interest — whichever is better for you.',
         'work': 'Delays in settling a deceased partner\'s dues are common (probate, disputes). The firm should provide for the Section 37 liability every year until settlement, or it understates its liabilities.'},
        {'id': 'c3', 'title': 'What the legal representatives receive — and what they bear',
         'body': ['Entitled to: balance of the deceased\'s capital (and current) account; interest on capital up to the date of death if the deed allows; share of goodwill; share of reserves and undistributed profits; share of revaluation profit; share of profit up to the date of death; share of the joint life policy (or separate policies).',
                  'Liable for: drawings; interest on drawings; share of revaluation loss; share of any loss up to the date of death.',
                  'After these adjustments the balance of the capital account is transferred to the Executor\'s Account (Deceased Partner\'s Capital A/c Dr. To His Executor\'s A/c). Payment follows the agreement — lump sum or instalments; if there is no agreement, the representatives are entitled to interest at 6% p.a. from the date of death till payment (or the Section 37 option).'],
         'analogy': 'A closing statement for the family: every right of the partner is added, every advance he took is subtracted.',
         'work': 'Accountants usually prepare this statement in a simple "amount due to the estate" format so the family\'s lawyer can verify it quickly.'},
        {'id': 'c4', 'title': 'Profit up to the date of death and the Profit and Loss Suspense Account',
         'body': ['Time basis: assume profit accrues evenly through the year. Profit to death = last year\'s (or average) profit × months up to death ÷ 12; deceased\'s share = that × his ratio.',
                  'Turnover (sales) basis: assume the same profit margin as last year. Rate = last year\'s profit ÷ last year\'s sales; profit to death = sales up to death × rate.',
                  'Because the year\'s accounts are not closed yet, the share is credited through a Profit and Loss Suspense Account: P&L Suspense A/c Dr. To Deceased Partner\'s Capital A/c. At year end the suspense account is closed to the Profit and Loss (Appropriation) Account, so the surviving partners finally bear it out of the year\'s profit.'],
         'analogy': 'Paying a share of a season\'s earnings half-way through the season: either pro-rata by time, or by how many tickets have been sold so far.',
         'work': 'The basis must come from the deed. If the business is seasonal, time basis can be badly unfair — accountants often recommend the turnover basis in such deeds.'},
        {'id': 'c5', 'title': 'Joint life policy on death',
         'body': ['On death the insurer pays the full policy amount to the firm. Bank A/c Dr. To Joint Life Policy A/c.',
                  'Method 1 (premium charged to P&L; policy not in books): the whole amount received is a gain, credited to ALL partners including the deceased in the old ratio.',
                  'Method 2 (policy at surrender value): only the amount received in excess of the book value is a gain, credited in the old ratio.',
                  'Method 3 (policy and JLP Reserve at surrender value): as in method 2, and the JLP Reserve is also transferred to all partners in the old ratio.'],
         'analogy': 'A group insurance cheque arrives after one member\'s death: it is shared among all members (the deceased\'s share going to his family) in the agreed proportion.',
         'work': 'The JLP claim is often the main source of cash to pay the executor. Accountants follow up the claim papers with the insurer alongside the settlement.'},
        {'id': 'c6', 'title': 'Separate life policies on death',
         'body': ['Where each partner\'s life is insured separately (premium charged to P&L), only the deceased partner\'s policy pays out — the full policy amount. The surviving partners\' policies continue, but their surrender values are counted too.',
                  'The total of (deceased\'s policy amount + surrender values of the other policies) is credited to all partners in the profit sharing ratio — the deceased\'s share to his Executor\'s Account.'],
         'blocks': [p('Example: partners 3:2; policy on the deceased ₹1,00,000; surrender value of the other partner\'s policy ₹20,000. Total ₹1,20,000 → executor ₹48,000 (2/5) if the deceased held 2/5.')],
         'analogy': 'One umbrella paid out a big claim, the others still have a resale value: the family gets its share of everything.',
         'work': 'The accountant obtains a surrender value certificate for each surviving partner\'s policy as at the date of death.'},
        {'id': 'c7', 'title': 'Paying the deceased partner\'s share',
         'body': ['The executor may be paid at once (Executor\'s A/c Dr. To Bank A/c), or the balance may be kept in the firm and paid in instalments with interest, exactly like a retiring partner\'s loan.',
                  'The basic difference from retirement is the finalisation of the amount: besides goodwill and revaluation (done as on retirement), the executor gets the share of profit up to the date of death and the share of the actual JLP proceeds.'],
         'analogy': 'Settling an estate: the amount is fixed first, then the family and the firm agree on a payment plan.',
         'work': 'Interest on the executor\'s balance is a charge against profit; the firm must also deduct and deposit tax at source on such interest where the law requires — a practical point many small firms forget.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Section 37 — profit share or 6% interest?', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Rohit, Sameer and Tanya are partners. Sameer died on 30 September 2026. After all adjustments the capitals stood at Rohit ₹1,80,000, Sameer ₹2,40,000 and Tanya ₹1,30,000. Rohit and Tanya carried on the business with the firm\'s property without settling Sameer\'s account until 31 March 2027. Profit for these six months was ₹66,000. There is no contract on this point. What can Sameer\'s representatives claim?',
         'solution': [s37, journal(E1, 'Journal', 'j1')], 'checks': c1},
        {'id': 'i2', 'title': 'Profit up to the date of death — time and turnover basis', 'difficulty': 'core', 'minutes': 8,
         'q': 'Uday holds a 3/10 share in a firm that closes its accounts on 31 March. He died on 31 July 2026. Last year the firm earned a profit of ₹3,60,000 on sales of ₹24,00,000. Sales from 1 April 2026 to 31 July 2026 were ₹9,00,000. Compute Uday\'s share of profit up to his death on the time basis and on the turnover basis, and pass the entry on the turnover basis.',
         'solution': [pt, journal(E2, 'Journal', 'j2')], 'checks': c2},
        {'id': 'i3', 'title': "Settling a deceased partner's account", 'difficulty': 'hard', 'minutes': 25,
         'q': ('Vikram, Wasim and Yash share profits 3:2:1; accounts are closed on 31 March. Wasim died on 30 June 2026. His capital on 1 April 2026 was ₹1,60,000 and his drawings up to death ₹12,000. The deed provides: interest on capital at 10% p.a.; '
               'profit up to death on the basis of last year\'s profit (₹2,40,000); goodwill at the value agreed (₹1,80,000) — not to appear in the books, Vikram and Yash continuing 3:1. General Reserve ₹60,000; revaluation profit ₹18,000. '
               'The firm had a joint life policy of ₹3,00,000 whose premium was charged to P&L each year; the claim was received on 30 June. The executor was paid ₹1,58,000 on 1 July 2026 and the balance is payable in two equal annual instalments with interest at 6% p.a. '
               "Pass journal entries and prepare Wasim's Capital Account and his Executor's Account up to 30 June 2027."),
         'solution': [wn('Workings', f'Goodwill: 1,80,000 × 2/6 = ₹{inr(gw_W)}, debited 3:1 → Vikram ₹{inr(gV)}, Yash ₹{inr(gY)}. Interest on capital: 1,60,000 × 10% × 3/12 = ₹{inr(ioc)}. Profit to death: 2,40,000 × 3/12 × 2/6 = ₹{inr(pls)}. JLP: 3,00,000 × 2/6 = ₹{inr(jlp["Wasim"])}.'),
                      journal(E3, 'Journal', 'j3'), wcap, sched3, exe],
         'checks': c3},
        {'id': 'i4', 'title': 'Joint life policy methods and separate life policies on death', 'difficulty': 'moderate', 'minutes': 12,
         'q': '(a) Kiran, Leela and Mohan share 2:2:1. They hold a joint life policy of ₹2,00,000. Leela dies and the policy amount is received. Show the treatment if (1) premiums were charged to P&L, (2) the policy was carried at surrender value ₹30,000, (3) the policy and a JLP Reserve were both carried at ₹30,000. (b) If instead the firm had separate policies — Leela ₹1,50,000 (on her death), Kiran surrender value ₹30,000, Mohan surrender value ₹15,000 — pass the entries.',
         'solution': [jt, wn('(b) Separate policies', f'Total = 1,50,000 + 30,000 + 15,000 = ₹{inr(sep_total)}, shared 2:2:1 → Leela\'s executor ₹{inr(sp["Leela"])}, Kiran ₹{inr(sp["Kiran"])}, Mohan ₹{inr(sp["Mohan"])}.'), journal(E4, 'Journal', 'j4')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': "Preparing the estate's claim after a partner's death", 'role': 'Accountant of a family partnership firm',
         'situation': 'A senior partner has died mid-year. His children (the legal heirs) ask the firm how much is due and when it will be paid. The surviving partners want to continue the business.',
         'steps': ['Read the deed: basis for profit up to death, goodwill, interest on capital, and payment terms.',
                   'Lodge the joint life policy claim with the insurer and track it.',
                   'Compute profit up to death (time or turnover basis), revaluation, reserves, goodwill and JLP share; deduct drawings.',
                   'Transfer the balance to the Executor\'s Account and agree a payment plan; if payment is delayed without agreement, provide for interest at 6% p.a. or the Section 37 option.',
                   'Obtain the legal representative documents (will/probate or succession certificate) before paying out.'],
         'takeaway': 'Death settlements combine accounting with law and sensitivity: correct figures, the right payee, and clear explanations.',
         'think': 'The business is seasonal — 70% of sales happen between October and March. The partner died on 30 September. Which basis is fairer for profit to death?',
         'answer': 'The turnover basis, because time basis would credit half the year\'s profit although much less than half was actually earned by 30 September.'},
        {'id': 'j2', 'title': 'Section 37 claim during a delayed settlement', 'role': 'Article assistant reviewing a firm\'s year-end accounts',
         'situation': 'A partner died eight months ago; his estate has not been paid because of a family dispute, and the firm is using the money.',
         'steps': ['Check whether the deed excludes Section 37 or gives the partners a purchase option that was exercised.',
                   'If not, compute both options (share of profit attributable to his share of property, and 6% interest) for the period since death.',
                   'Recommend providing for the higher amount, since the representatives may choose it.'],
         'takeaway': 'Until the estate is settled, the firm carries a liability that grows with time — and the law lets the estate pick the better option.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Under Section 37 of the Indian Partnership Act, if the business is continued without settling a deceased partner\'s account, his estate may claim, at its option, interest on his share of the property at:', 'options': ['6% p.a.', '9% p.a.', '12% p.a.', 'The bank rate'], 'answer': 0, 'explain': 'Section 37 gives the option of a share of subsequent profits or interest at 6% per annum.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'A partner with a 1/5 share dies 3 months after the year end. Last year\'s profit was ₹2,40,000. On the time basis his share of profit to death is:', 'options': ['₹12,000', '₹60,000', '₹48,000', '₹15,000'], 'answer': 0, 'check': '240000*3/12*1/5', 'explain': '2,40,000 × 3/12 = 60,000 for the firm; × 1/5 = ₹12,000.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm3', 'q': "The deceased partner's share of profit up to the date of death is credited to his capital account by debiting:", 'options': ['Profit and Loss Suspense Account', 'Profit and Loss Appropriation Account of last year', 'Surviving partners in the gaining ratio', 'Executor\'s Account'], 'answer': 0, 'explain': 'The current year\'s accounts are not yet prepared, so a suspense account is used and closed at year end.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Last year a firm earned ₹1,50,000 on sales of ₹10,00,000. Sales up to the date of a partner\'s death were ₹4,00,000. Profit to the date of death on the turnover basis is:', 'options': ['₹60,000', '₹40,000', '₹1,50,000', '₹6,000'], 'answer': 0, 'check': '400000*150000/1000000', 'explain': 'Margin 15%; 4,00,000 × 15% = ₹60,000.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Premiums on a joint life policy of ₹5,00,000 have always been charged to P&L. On the death of a partner the amount received is:', 'options': ['Credited to all partners including the deceased in the old ratio', 'Credited only to the deceased partner', 'Credited to the surviving partners in the gaining ratio', 'Credited to Profit and Loss Suspense'], 'answer': 0, 'explain': 'The whole amount is a gain of the firm and belongs to all partners in their old ratio — the deceased\'s share goes to his estate.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'JLP ₹3,00,000 is carried at its surrender value of ₹45,000. On a partner\'s death the gain credited to partners is:', 'options': ['₹2,55,000', '₹3,00,000', '₹45,000', '₹3,45,000'], 'answer': 0, 'check': '300000-45000', 'explain': 'Only the excess of the amount received over the book value is a gain.', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'Which of the following is NOT payable to the legal representatives of a deceased partner?', 'options': ['His share of profit earned by the firm after final settlement of accounts', 'His share of goodwill', 'His share of profit up to the date of death', 'His share of revaluation profit'], 'answer': 0, 'explain': 'After the account is settled the estate has no claim on later profits; Section 37 applies only while the account is unsettled.', 'concept': 'c3', 'difficulty': 'moderate'},
        None,  # m8 set below
        {'id': 'm9', 'q': "Once all adjustments are made, the balance of a deceased partner's capital account is transferred to:", 'options': ["His Executor's (legal representative's) Account", 'Surviving partners\' capital accounts', 'Profit and Loss Suspense Account', 'General Reserve'], 'answer': 0, 'explain': 'The amount is now owed to his estate, so it is shown as a liability to the executor.', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'A deceased partner\'s share in the firm\'s property is ₹1,80,000. The business is continued for 4 months without settlement and the estate opts for interest. The amount is:', 'options': ['₹3,600', '₹10,800', '₹7,200', '₹5,400'], 'answer': 0, 'check': '180000*6/100*4/12', 'explain': '1,80,000 × 6% × 4/12 = ₹3,600.', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': 'The Profit and Loss Suspense Account debited on a partner\'s death is closed at the end of the year by transfer to:', 'options': ['Profit and Loss (Appropriation) Account', "Deceased partner's executor", 'General Reserve', 'Surviving partners\' current accounts directly'], 'answer': 0, 'explain': 'It is a temporary account; at year end it is closed to P&L (Appropriation), so the year\'s profit bears it.', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm12', 'q': 'The deed gives surviving partners an option to purchase a deceased partner\'s share, and they duly exercise it. Under Section 37 the estate is:', 'options': ['Not entitled to any further share of profits', 'Entitled to 6% interest anyway', 'Entitled to a share of all future profits', 'Entitled to double interest'], 'answer': 0, 'explain': 'The proviso to Section 37: when the purchase option is duly exercised, no further share of profits is due.', 'concept': 'c2', 'difficulty': 'moderate'},
    ]
    mcqs[7] = {'id': 'm8', 'q': 'A, B and C share 3:1:1 and hold separate policies (premiums charged to P&L): A — surrender value ₹12,000; B — surrender value ₹10,000; C — policy amount ₹60,000. C dies. The amount credited to C\'s executor in respect of the policies is:', 'options': ['₹16,400', '₹60,000', '₹12,000', '₹82,000'], 'answer': 0, 'check': '(60000+12000+10000)*1/5',
               'explain': 'Total = C\'s policy ₹60,000 + surrender values of A and B (12,000 + 10,000) = ₹82,000; C\'s 1/5 share = ₹16,400.', 'concept': 'c6', 'difficulty': 'hard'}

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Arjun, Bhavna and Chetan were equal partners. Chetan died on 31 August 2026. After all adjustments the capitals were Arjun ₹1,00,000, Bhavna ₹1,50,000 and Chetan ₹2,50,000. Arjun and Bhavna continued the business with the firm\'s assets and paid Chetan\'s executor only on 30 November 2026. Profit for September to November was ₹48,000. The deed is silent. Advise the executor, with reference to the law, and compute the amount.',
         'model': [legal('Section 37 of the Indian Partnership Act, 1932: where the surviving partners carry on the business with the firm\'s property without final settlement with the estate of a deceased partner, the estate may, unless otherwise agreed, claim at its option either the share of profits since death attributable to the use of the deceased\'s share of the property, or interest at 6% p.a. on that share. No further share is due if a purchase option in the deed is duly exercised.',
                         'Chetan\'s share in the firm\'s property is ₹2,50,000 out of ₹5,00,000. The business was carried on for 3 months without settlement and earned ₹48,000. The deed is silent, so no purchase option exists.',
                         f'Option (a): 48,000 × 2,50,000 ÷ 5,00,000 = ₹{inr(q1a)}. Option (b): 2,50,000 × 6% × 3/12 = ₹{inr(q1b)}. The executor may wait until the profit is known before choosing.',
                         f'The executor should choose the share of profits, ₹{inr(q1a)}, in addition to the amount already due on Chetan\'s capital account.')],
         'scheme': [{'id': 's1', 'pt': 'Section 37 stated correctly with both options', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Facts identified: business continued with firm property, no settlement, deed silent', 'm': 0.5, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Profit option ₹24,000 computed on capital ratio', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Interest option ₹3,750 computed for 3 months', 'm': 1, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'Conclusion: choose ₹24,000', 'm': 1, 'skill': 'conclusion'}],
         'checks': qc1,
         'remarks': ['Many candidates compute interest for a full year instead of the three months of delay.', 'Answers that give only one option score half marks at best — the essence of Section 37 is the choice.'],
         'mistakes': ['Taking the profit share in the profit sharing ratio (1/3) instead of the share in property.', 'Quoting the interest rate as 12% or 9%.'],
         'tips': ['Use Provision → Facts → Analysis → Conclusion even in an accounting paper when law is asked.', 'Always compute both options and say which one the estate will choose.']},
        {'id': 'q2', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'ledger',
         'q': ('Dinesh, Esha and Fatima share profits 2:2:1; accounts close on 31 March. Esha died on 31 October 2026. Her capital on 1 April 2026 was ₹2,00,000 and drawings to the date of death ₹21,000. The deed provides: '
               '(i) interest on capital at 9% p.a.; (ii) profit up to death on the basis of sales — last year\'s sales ₹30,00,000 and profit ₹4,50,000; sales from 1 April to 31 October 2026 were ₹20,00,000; '
               '(iii) goodwill valued at ₹2,50,000, not to be shown in the books; Dinesh and Fatima will share 3:2 in future. General Reserve stood at ₹40,000; revaluation resulted in a loss of ₹15,000. '
               'The firm\'s joint life policy of ₹2,50,000 appeared at ₹45,000 with a JLP Reserve of equal amount; the policy amount was received. ₹2,19,500 was paid to the executor on 31 October; the balance carries interest at 6% p.a. '
               "Prepare Esha's Capital Account and her Executor's Account up to 31 March 2027."),
         'model': [wn('Workings', f'Profit to death: 20,00,000 × 15% = ₹3,00,000 × 2/5 = ₹{inr(q2p)}. Interest on capital: 2,00,000 × 9% × 7/12 = ₹{inr(q2i)}. Goodwill: 2,50,000 × 2/5 = ₹{inr(q2g)}, borne 1:1 by Dinesh and Fatima (each gains 1/5). '
                                f'JLP gain: (2,50,000 − 45,000) × 2/5 = ₹{inr(q2j)}; JLP Reserve 45,000 × 2/5 = ₹{inr(q2jr)}. Reserve 40,000 × 2/5 = ₹16,000. Revaluation loss 15,000 × 2/5 = ₹{inr(q2rl)}.'),
                   ecap, eexe],
         'scheme': [{'id': 's1', 'pt': 'Profit to death ₹1,20,000 on turnover basis', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Interest on capital ₹10,500 for 7 months', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Goodwill ₹1,00,000 credited (gaining ratio 1:1 noted)', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's4', 'pt': 'JLP gain ₹82,000 and JLP Reserve ₹18,000 credited', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'Reserve credited; drawings and revaluation loss debited', 'm': 1, 'skill': 'posting'},
                    {'id': 's6', 'pt': 'Capital account closed by transfer of ₹5,19,500 to executor', 'm': 1.5, 'skill': 'balancing'},
                    {'id': 's7', 'pt': "Executor's account: payment, interest ₹7,500, balance c/d ₹3,07,500", 'm': 2, 'skill': 'presentation'}],
         'checks': qc2,
         'remarks': ['Candidates frequently credit the full policy amount of ₹2,50,000 × 2/5 and also the reserve — double counting the ₹45,000 already in the books.',
                     'Interest to the executor is often charged on ₹5,19,500 instead of the unpaid ₹3,00,000.'],
         'mistakes': ['Using the time basis when the deed says sales basis.', 'Debiting goodwill to the surviving partners in the old ratio 2:1.', 'Forgetting to debit the revaluation loss.'],
         'tips': ['Do every computation as a numbered working note first, then post them into the capital account.', 'Close the deceased partner\'s capital account to the executor — never carry it forward.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'State the amounts to which the legal representatives of a deceased partner are entitled, and the amounts for which they are liable.',
         'model': [table(['Entitled to', 'Liable for'], [
             ['Balance of capital (and current) account', 'Drawings of the deceased'],
             ['Interest on capital up to death, if allowed', 'Interest on drawings, if charged'],
             ['Share of goodwill', 'Share of revaluation loss'],
             ['Share of reserves and undistributed profits', 'Share of loss up to the date of death'],
             ['Share of revaluation profit', ''],
             ['Share of profit up to the date of death', ''],
             ['Share of joint life policy / separate policies', ''],
         ])],
         'scheme': [{'id': 's1', 'pt': 'Capital balance, interest on capital and share of goodwill', 'm': 1, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'Reserves, revaluation profit, profit to death, JLP', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Drawings and interest on drawings', 'm': 0.5, 'skill': 'concept'},
                    {'id': 's4', 'pt': 'Revaluation loss and loss to date of death', 'm': 1, 'skill': 'concept'}],
         'remarks': ['A two-column answer is the clearest; examiners look for at least six entitlements and three liabilities.'],
         'mistakes': ['Listing profits after the settlement as an entitlement.', 'Missing the joint life policy.'],
         'tips': ['Write "Entitled to" and "Liable for" as two columns.']},
        {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'journal',
         'q': 'Gita holds a 1/4 share in a firm whose accounts close on 31 December. She died on 31 May 2026. For the year 2025 the firm earned a profit of ₹2,88,000 on sales of ₹19,20,000; sales from 1 January to 31 May 2026 were ₹9,60,000. Compute her share of profit up to death on (a) the time basis and (b) the sales basis, and pass the journal entry on the sales basis.',
         'model': [table(['Basis', 'Working', "Gita's share (₹)"], [
             ['(a) Time', '2,88,000 × 5/12 × 1/4', inr(q4t)],
             ['(b) Sales', f'9,60,000 × {q4r:g}% (2,88,000 ÷ 19,20,000) × 1/4', inr(q4s)],
         ]), journal([je('2026 May 31', [('Profit and Loss Suspense A/c', q4s)], [("Gita's Capital A/c", q4s)], "Being Gita's share of profit up to death on the sales basis")], 'Journal', 'jq4')],
         'scheme': [{'id': 's1', 'pt': 'Time basis ₹30,000', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Profit margin 15% worked out', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Sales basis ₹36,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Entry: P&L Suspense Dr, Gita\'s Capital Cr, with narration', 'm': 1.5, 'skill': 'presentation'}],
         'checks': qc4,
         'remarks': ['Counting months wrongly (4 instead of 5) is the most common slip.', 'Some candidates debit the surviving partners directly — the suspense account is expected.'],
         'mistakes': ['Taking 9,60,000 × 15% as Gita\'s share without applying 1/4.', 'Crediting the executor instead of Gita\'s capital account at this stage.'],
         'tips': ['Write the period explicitly: 1 January – 31 May = 5 months.']},
    ]

    viva = [
        V('v1', 'What right does Section 37 of the Partnership Act give to the estate of a deceased partner?',
          'If the surviving partners carry on the business with the firm\'s property without settling the deceased partner\'s account, his estate can choose either the share of profits made since his death that can be traced to the use of his share in the property, or interest at six per cent per annum on his share. This applies unless there is a contract to the contrary, and no further profit is due if a purchase option in the deed is duly exercised.',
          [P('p1', 'Applies when business is carried on with firm property without settlement', 2, 'without settl|not settled|before settlement|no settlement|without final settlement|unsettled|carry on|continue|using the firm|use of', min=1),
           P('p2', 'Option 1: share of profits attributable to use of his share of property', 4, 'share of profit|share of the profit|share in profit|profits made|profit earned|profit attributable|proportion of profit|profits since'),
           P('p3', 'Option 2: interest at 6% p.a.', 4, '6 percent|6 per cent|6%|six percent|six per cent|6 p|interest at 6|interest of 6', 'interest', min=2)], 'c2'),
        V('v2', 'How is a deceased partner\'s share of profit up to the date of death calculated?',
          'It can be calculated on the time basis, assuming profit is earned evenly, by taking last year\'s profit for the months up to death; or on the turnover basis, by applying last year\'s rate of profit on sales to the sales up to the date of death. His share is then credited to his capital account by debiting the Profit and Loss Suspense Account.',
          [P('p1', 'Time basis — profit for the months up to death', 3, 'time basis|time|months|period|evenly|uniform', min=1),
           P('p2', 'Turnover / sales basis — last year\'s margin on sales to date', 4, 'turnover|sales basis|sale basis|on sales|on the sales|rate of profit|percentage of sales|profit margin|gross profit ratio|ratio of profit', min=1),
           P('p3', 'Credited via Profit and Loss Suspense Account', 3, 'suspense')], 'c4'),
        V('v3', 'What happens to the joint life policy on the death of a partner when the premium has been charged to profit and loss account?',
          'The firm receives the full policy amount from the insurer. Since the policy was not shown in the books, the whole amount is a gain, and it is credited to all the partners including the deceased partner in their old profit sharing ratio. The deceased partner\'s share goes to his executor.',
          [P('p1', 'Firm receives the full policy amount', 3, 'full|whole|policy amount|sum assured|entire|policy value|policy money|amount received|insurer pays|insurance company pays', min=1),
           P('p2', 'Credited to all partners including the deceased', 4, 'all partner|all the partner|including the deceased|including deceased|including the dead|every partner|including him', min=1),
           P('p3', 'In the old profit sharing ratio', 3, 'old ratio|old profit sharing|profit sharing ratio|existing ratio|original ratio')], 'c5'),
        V('v4', 'Name the items to which the legal representatives of a deceased partner are entitled.',
          'They are entitled to the balance of his capital account, interest on capital up to the date of death if allowed, his share of goodwill, his share of reserves and undistributed profits, his share of revaluation profit, his share of profit up to the date of death and his share of the joint life policy.',
          [P('p1', 'Capital balance', 2, 'capital'),
           P('p2', 'Share of goodwill', 2, 'goodwill'),
           P('p3', 'Share of reserves / undistributed profits', 2, 'reserve|undistributed|accumulated profit'),
           P('p4', 'Share of profit up to the date of death', 2, 'up to the date of death|up to death|till death|till the date of death|until death|before death|to the date of death|profit to death|date of death'),
           P('p5', 'Share of joint life policy / revaluation profit (any one)', 2, 'joint life|life policy|policy|revaluation', min=1)], 'c3'),
        V('v5', 'How are separate life policies treated on the death of a partner?',
          'Only the policy on the deceased partner\'s life pays out, and the full policy amount is received. The policies of the surviving partners continue, but their surrender values are added. The total of the deceased partner\'s policy amount and the surrender values of the other policies is credited to all partners in the profit sharing ratio, the deceased\'s share going to his executor.',
          [P('p1', 'Deceased partner\'s policy — full amount received', 3, 'deceased|dead partner|his own policy|policy on the deceased|policy of the deceased|dying partner|his policy', 'full|policy amount|sum assured|whole|entire|policy value|amount received|received', min=2),
           P('p2', 'Surviving partners\' policies at surrender value', 4, 'surrender'),
           P('p3', 'Total shared by all partners in profit sharing ratio', 3, 'all partner|all the partner|profit sharing|ratio', min=1)], 'c6'),
        V('v6', 'What is the main difference between accounting for the death of a partner and for retirement?',
          'The adjustments are mostly the same — revaluation, reserves, goodwill and life policy. The differences are that on death the partner\'s share of profit from the last balance sheet date to the date of death has to be estimated through a profit and loss suspense account, the joint life policy actually matures so the full amount is received instead of the surrender value, and the amount due is paid to his executor or legal representatives.',
          [P('p1', 'Share of profit up to the date of death must be estimated (P&L suspense)', 4, 'profit up to|profit till|profit to the date|up to the date of death|till death|suspense|profit until|date of death', min=1),
           P('p2', 'JLP matures — full amount received, not surrender value', 3, 'full amount|policy amount|sum assured|matures|whole amount|policy value|not surrender|instead of surrender|rather than surrender|full policy', min=1),
           P('p3', 'Amount paid to executor / legal representatives', 3, 'executor|legal representative|legal heir|heirs|family|estate|representative', min=1)], 'c1'),
    ]

    kcase = [{'id': 'k1', 'title': "Pia's estate", 'difficulty': 'hard',
              'case': ('Om, Pia and Raj share profits 2:1:1; accounts close on 31 March. Pia died on 31 August 2026. Her capital (after reserves and revaluation) was ₹1,20,000. Profit up to death is to be taken on the time basis using last year\'s profit of ₹1,80,000. '
                       'The firm\'s joint life policy of ₹4,00,000 was carried at its surrender value of ₹60,000, and the policy amount was received. Pia\'s estate was paid only four months after her death, with no agreement on interest; assume the estate opts for interest on the full amount due.'),
              'mcqs': [
                  M('k1a', "Pia's share of profit up to the date of death is:", [R(k_p), R(75000), R(15000), R(45000)], 0, f'1,80,000 × 5/12 = ₹75,000 for the firm; × 1/4 = {R(k_p)}.', 'moderate', '180000*5/12*1/4'),
                  M('k1b', "Pia's share of the joint life policy credited to her capital is:", [R(k_j), R(100000), R(15000), R(115000)], 0, f'Gain = 4,00,000 − 60,000 = 3,40,000; × 1/4 = {R(k_j)}.', 'hard', '(400000-60000)*1/4'),
                  M('k1c', 'The total amount transferred to Pia\'s executor is:', [R(k_due), R(238750), R(205000), R(258750)], 0, f'1,20,000 + 18,750 + 85,000 = {R(k_due)}.', 'hard', '120000+18750+85000'),
                  M('k1d', 'Interest payable to the estate for the four months of delay is:', [R(k_int), R(13425), R(7200), R(2238)], 0, f'2,23,750 × 6% × 4/12 = {R(k_int)} (the 6% rate applies in the absence of agreement).', 'hard', '223750*6/100*4/12'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch10', 'n': 5,
        'title': 'Death of a Partner',
        'outcomes': [
            'Explain how accounting for the death of a partner differs from retirement.',
            'Apply Section 37 of the Indian Partnership Act to compute the estate\'s claim when settlement is delayed.',
            'List what the legal representatives are entitled to and liable for, and close the deceased partner\'s account to the Executor\'s Account.',
            'Estimate profit up to the date of death on the time and turnover bases and record it through a Profit and Loss Suspense Account.',
            'Account for joint life and separate life policies on death and for payment of the executor in instalments.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 70}, 'prereq': ['fnd-p1-ch10-u04'],
                 'exam_tip': 'Death questions usually ask only for the deceased partner\'s capital account and the executor\'s account — show every computation as a working note so that step marks survive an arithmetic slip.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Death = retirement adjustments + profit to date of death + actual JLP proceeds + payment to the executor.',
                        'Section 37: if business continues with firm property without settlement, the estate chooses share of profits attributable to its share of property or 6% p.a. interest.',
                        'Profit to death: time basis (months/12) or turnover basis (sales to date × last year\'s margin); P&L Suspense Dr, Deceased\'s Capital Cr.',
                        'JLP on death: full amount received; gain over book value credited to all partners in old ratio; JLP reserve also distributed.',
                        'Separate policies: deceased\'s policy amount + surrender values of the others, shared in profit ratio.',
                        'Balance of capital → Executor\'s A/c; paid at once or in instalments with interest.'],
            'remember': ['Section 37 interest rate: 6% p.a.', 'P&L Suspense is closed to P&L Appropriation at year end.', 'Without agreement, the executor gets 6% p.a. from death till payment.'],
            'traps': ["Don't give the executor profits earned after the account is settled.", "Don't double count the JLP book value — credit only the excess, plus any reserve.", "Don't use time basis if the deed says sales basis."],
        },
        'quickref': [
            {'k': 'Section 37 (IPA 1932)', 'v': 'Share of post-death profits attributable to use of his share of property, or 6% p.a. interest — at the estate\'s option'},
            {'k': 'Time basis', 'v': 'Profit × months to death ÷ 12 × his share'},
            {'k': 'Turnover basis', 'v': 'Sales to death × (last year\'s profit ÷ last year\'s sales) × his share'},
            {'k': 'Profit to death entry', 'v': "P&L Suspense A/c Dr. To Deceased Partner's Capital A/c"},
            {'k': 'Transfer to executor', 'v': "Deceased Partner's Capital A/c Dr. To His Executor's A/c"},
            {'k': 'JLP on death', 'v': 'Bank Dr. To JLP; JLP Dr. To all partners (old ratio) — gain over book value'},
            {'k': 'Separate policies', 'v': "(Deceased's policy amount + others' surrender values) × profit ratio"},
        ],
        'viva': viva, 'cases': kcase,
    }
