"""CA Foundation · Paper 1 Accounting · Chapter 10 Partnership and LLP Accounts · Unit 6 Dissolution of Partnership Firms and LLPs.
Original explanations, names and numbers (structure and scope follow the ICAI study material).
Law referred to: Indian Partnership Act, 1932 — ss. 34, 39–44, 48, 51; Garner v. Murray (1904) for insolvency of a partner; LLP Act, 2008 on winding up."""
from fractions import Fraction as F
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M
from fnd_p1_ch10_u03 import tacc, capacc, split, ratio

UID = 'fnd-p1-ch10-u06'


def hrc_steps(caps, shares, names):
    """Highest relative capital method: returns list of (stage description, {partner: amount}) payment tranches before the final ratio applies."""
    caps = dict(caps); stages = []
    active = list(names)
    while len(active) > 1:
        per = {p: F(caps[p]) / shares[p] for p in active}
        base = min(per.values())
        excess = {p: caps[p] - base * shares[p] for p in active}
        if all(v == 0 for v in excess.values()): break
        stages.append(excess)
        for p in active: caps[p] = base * shares[p]
        active = [p for p in active if excess[p] > 0]
        # recurse among those with excess: work on their excess only
        caps = {p: excess[p] for p in active}
    return stages


def build():
    # ============ Illustration 1: closing the books — Ajay and Bina ============
    c1 = Checks()
    cred_paid = c1.add('48000*97.5/100', 'Creditors paid at 2.5% discount')
    realised = c1.add('68000+12000+36000+46000+5000', 'Cash realised from assets incl. unrecorded computer')
    drs = c1.add('75000+18000+22000+40000+50000+46800+12000+3000', 'Debit side of Realisation before loss')
    crs = c1.add('48000+12000+2500+167000+25000', 'Credit side of Realisation before loss')
    loss = c1.add('266800-254500', 'Loss on realisation')
    lA = c1.add('12300*3/5', "Ajay's share of loss"); lB = c1.add('12300*2/5', "Bina's share of loss")
    capA = c1.add('90000+9000-25000-7380', "Final payment to Ajay")
    capB = c1.add('60000+6000-4920', "Final payment to Bina")
    c1.add('42500+167000-46800-12000-3000-20000', 'Cash left for partners = total of their capitals')
    E1 = [
        je('2026 Dec 31', [('Realisation A/c', 205000)], [('Machinery A/c', 75000), ('Furniture A/c', 18000), ('Investments A/c', 22000), ('Stock A/c', 40000), ('Debtors A/c', 50000)], 'Being assets (other than bank) transferred to Realisation at book value'),
        je('Dec 31', [('Creditors A/c', 48000), ('Bills Payable A/c', 12000), ('Provision for Doubtful Debts A/c', 2500)], [('Realisation A/c', 62500)], 'Being outside liabilities and the provision transferred to Realisation'),
        je('Dec 31', [('Bank A/c', realised)], [('Realisation A/c', realised)], 'Being assets sold, including an unrecorded computer realising ₹5,000'),
        je('Dec 31', [("Ajay's Capital A/c", 25000)], [('Realisation A/c', 25000)], 'Being investments taken over by Ajay at the agreed value'),
        je('Dec 31', [('Realisation A/c', cred_paid + 12000)], [('Bank A/c', cred_paid + 12000)], 'Being creditors paid at 2.5% discount and bills payable paid in full'),
        je('Dec 31', [('Realisation A/c', 3000)], [('Bank A/c', 3000)], 'Being realisation expenses paid'),
        je('Dec 31', [("Ajay's Capital A/c", lA), ("Bina's Capital A/c", lB)], [('Realisation A/c', loss)], 'Being loss on realisation shared 3:2'),
        je('Dec 31', [("Bina's Loan A/c", 20000)], [('Bank A/c', 20000)], "Being partner's loan repaid"),
        je('Dec 31', [('General Reserve A/c', 15000)], [("Ajay's Capital A/c", 9000), ("Bina's Capital A/c", 6000)], 'Being reserve distributed 3:2'),
        je('Dec 31', [("Ajay's Capital A/c", capA), ("Bina's Capital A/c", capB)], [('Bank A/c', capA + capB)], 'Being final payments made to partners'),
    ]
    real1 = tacc([('To Machinery A/c', 75000), ('To Furniture A/c', 18000), ('To Investments A/c', 22000), ('To Stock A/c', 40000), ('To Debtors A/c', 50000),
                  ('To Bank A/c — creditors', cred_paid), ('To Bank A/c — bills payable', 12000), ('To Bank A/c — expenses', 3000)],
                 [('By Creditors A/c', 48000), ('By Bills Payable A/c', 12000), ('By Provision for Doubtful Debts A/c', 2500), ('By Bank A/c — assets realised', realised),
                  ("By Ajay's Capital A/c — investments", 25000), ("By Ajay's Capital A/c — loss 3/5", lA), ("By Bina's Capital A/c — loss 2/5", lB)], title='Realisation Account')
    cap1, b1 = capacc(['Ajay', 'Bina'], [('To Realisation A/c — investments', {'Ajay': 25000}), ('To Realisation A/c — loss', {'Ajay': lA, 'Bina': lB}), ('To Bank A/c — final payment', {'Ajay': capA, 'Bina': capB})],
                      [('By Balance b/d', {'Ajay': 90000, 'Bina': 60000}), ('By General Reserve A/c', {'Ajay': 9000, 'Bina': 6000})])
    assert all(abs(v) < 0.01 for v in b1.values()), b1
    bank1 = tacc([('To Balance b/d', 42500), ('To Realisation A/c — assets', realised)],
                 [('By Realisation A/c — creditors', cred_paid), ('By Realisation A/c — bills payable', 12000), ('By Realisation A/c — expenses', 3000), ("By Bina's Loan A/c", 20000),
                  ("By Ajay's Capital A/c", capA), ("By Bina's Capital A/c", capB)], title='Bank Account')

    # ============ Illustration 2: Garner v Murray ============
    c2 = Checks()
    loss2 = c2.add('180000-157000+2000', 'Loss on realisation (assets 1,80,000 − realised 1,57,000 + expenses 2,000)')
    l2 = split(loss2, {'Dhruv': F(2, 5), 'Ela': F(2, 5), 'Faiz': F(1, 5)})
    defi = c2.add('5000-3000-600', "Faiz's deficiency after his estate pays ₹600 (30% of ₹2,000)")
    c2.add('2000*30/100', 'Amount recovered from Faiz\'s estate')
    dD = c2.add('1400*90000/150000', 'Borne by Dhruv (capital ratio 90,000 : 60,000)')
    dE = c2.add('1400*60000/150000', 'Borne by Ela')
    payD = c2.add('90000+10000-10000-840', 'Final payment to Dhruv')
    payE = c2.add('60000+10000-10000-560', 'Final payment to Ela')
    real2 = tacc([('To Sundry Assets', 180000), ('To Bank A/c — creditors', 40000), ('To Bank A/c — expenses', 2000)],
                 [('By Creditors A/c', 40000), ('By Bank A/c — assets realised', 157000), ("By Dhruv's Capital A/c — loss 2/5", l2['Dhruv']), ("By Ela's Capital A/c — loss 2/5", l2['Ela']), ("By Faiz's Capital A/c — loss 1/5", l2['Faiz'])],
                 title='Realisation Account (summary)')
    cap2, b2 = capacc(['Dhruv', 'Ela', 'Faiz'],
                      [('To Realisation A/c — loss', l2), ("To Faiz's Capital A/c — deficiency", {'Dhruv': dD, 'Ela': dE}), ('To Bank A/c — final payment', {'Dhruv': payD, 'Ela': payE})],
                      [('By Balance b/d', {'Dhruv': 90000, 'Ela': 60000, 'Faiz': 3000}), ('By Bank A/c — cash for realisation loss', {'Dhruv': l2['Dhruv'], 'Ela': l2['Ela']}),
                       ("By Bank A/c — from Faiz's estate", {'Faiz': 600}), ('By Dhruv and Ela — deficiency', {'Faiz': defi})])
    assert all(abs(v) < 0.01 for v in b2.values()), b2
    bank2 = tacc([('To Balance b/d', 13000), ('To Realisation A/c — assets', 157000), ("To Dhruv's Capital A/c", 10000), ("To Ela's Capital A/c", 10000), ("To Faiz's Capital A/c", 600)],
                 [('By Realisation A/c — expenses', 2000), ('By Realisation A/c — creditors', 40000), ("By Dhruv's Capital A/c", payD), ("By Ela's Capital A/c", payE)], title='Bank Account')

    # ============ Illustration 3: piecemeal — highest relative capital ============
    c3 = Checks()
    names = ['X', 'Y', 'Z']; sh = {'X': 3, 'Y': 2, 'Z': 1}
    caps = {'X': 48000, 'Y': 44000, 'Z': 28000}
    stages = hrc_steps(caps, sh, names)
    assert stages == [{'X': 0, 'Y': 12000, 'Z': 12000}, {'Y': 0, 'Z': 6000}], stages
    c3.add('48000/3', 'X: capital per unit of profit share (lowest = base)')
    c3.add('16000*2', "Y's proportionate capital on X's base"); c3.add('44000-32000', "Y's excess")
    c3.add('28000-16000', "Z's excess")
    c3.add('12000/2', "Second round: Y's excess per unit (base)"); c3.add('12000-6000*1', "Z's remaining excess")
    hrc = table(['Step', 'X (₹)', 'Y (₹)', 'Z (₹)'], [
        ['Capitals after paying outsiders', '48,000', '44,000', '28,000'],
        ['Profit-sharing ratio', '3', '2', '1'],
        ['Capital ÷ ratio', '16,000', '22,000', '28,000'],
        ['Proportionate capital on X\'s base (16,000 per unit)', '48,000', '32,000', '16,000'],
        ['Excess capital (round 1)', 'nil', '12,000', '12,000'],
        ['Round 2 — excess ÷ ratio (Y 2, Z 1)', '—', '6,000', '12,000'],
        ['Proportionate excess on Y\'s base (6,000 per unit)', '—', '12,000', '6,000'],
        ['Excess capital (round 2)', '—', 'nil', '6,000'],
    ], title='Highest relative capital method — order of payment',
        note='Pay order: first ₹6,000 to Z alone; next ₹18,000 to Y and Z in 2:1; after that every rupee goes to X, Y and Z in 3:2:1.')
    dist = [['Instalment 1 — Z alone', '9,000', '', '', '6,000'], ['Instalment 1 — balance to Y and Z 2:1', '', '', '2,000', '1,000'],
            ['Instalment 2 — rest of the Y/Z stage (2:1)', '27,000', '', '10,000', '5,000'], ['Instalment 2 — balance 3:2:1', '', '6,000', '4,000', '2,000'],
            ['Instalment 3 — all 3:2:1', '54,000', '27,000', '18,000', '9,000']]
    tX = c3.add('6000+27000', 'Total paid to X'); tY = c3.add('2000+10000+4000+18000', 'Total paid to Y'); tZ = c3.add('6000+1000+5000+2000+9000', 'Total paid to Z')
    c3.add('9000+27000+54000', 'Total distributed')
    dist.append(['Total', '90,000', inr(tX), inr(tY), inr(tZ)])
    dist_t = table(['Distribution', 'Cash available (₹)', 'X (₹)', 'Y (₹)', 'Z (₹)'], dist, num=[1, 2, 3, 4], total=True, title='Distribution of instalments')
    loss3 = c3.add('120000-90000', 'Total loss'); c3.add('48000-30000*3/6', 'Check: X = capital − 3/6 of loss')
    c3.add('44000-30000*2/6', 'Check: Y'); c3.add('28000-30000*1/6', 'Check: Z')
    c3.add('(120000-9000)*3/6-48000', 'Max-loss check on instalment 1: X\'s notional deficiency')
    mlc = wn('Cross-check with the maximum loss method (instalment 1)', 'Treat everything not yet realised as lost: maximum loss = 1,20,000 − 9,000 = ₹1,11,000, shared 3:2:1 → X 55,500, Y 37,000, Z 18,500. X would be ₹7,500 short; that shortfall is shared by Y and Z (profit-ratio rule) 2:1 → 5,000 and 2,500. Y: 44,000 − 37,000 − 5,000 = ₹2,000; Z: 28,000 − 18,500 − 2,500 = ₹7,000. Same answer as the highest relative capital method (Z 6,000 + 1,000; Y 2,000).')

    # ============ Illustration 4: premium refund on premature dissolution (s. 51) ============
    c4 = Checks()
    refund = c4.add('60000*3/5', 'Reasonable refund: unexpired 3 of 5 years')
    rH = c4.add('36000*2/3', 'Borne by Hema'); rI = c4.add('36000*1/3', 'Borne by Ishan')
    E4 = [je('(a)', [("Hema's Capital A/c", rH), ("Ishan's Capital A/c", rI)], [("Gopal's Capital A/c", refund)], 'Being refund of premium to Gopal on dissolution of the firm before the agreed term')]

    # ============ Questions ============
    qc1 = Checks()
    qreal = qc1.add('38000+24000+27500', 'Cash from assets sold')
    qcred = qc1.add('36000*95/100', 'Creditors paid at 5% discount')
    qdr = qc1.add('60000+45000+27000+30000+34200+1200+1900', 'Debit side of Realisation')
    qcr = qc1.add('36000+72000+89500', 'Credit side of Realisation')
    qloss = qc1.add('199300-197500', 'Loss on realisation')
    qK = qc1.add('75000+6000+1900-72000-1200', 'Final payment to Kavi')
    qL = qc1.add('45000+3000-600', 'Final payment to Lata')
    qc1.add('18000+89500-34200-1200-15000', 'Bank available for partners')
    qreal1 = tacc([('To Land A/c', 60000), ('To Machinery A/c', 45000), ('To Stock A/c', 27000), ('To Debtors A/c', 30000), ('To Bank A/c — creditors', qcred),
                   ('To Bank A/c — outstanding repairs (unrecorded)', 1200), ("To Kavi's Capital A/c — expenses paid by him", 1900)],
                  [('By Creditors A/c', 36000), ("By Kavi's Capital A/c — land", 72000), ('By Bank A/c — assets realised', qreal), ("By Kavi's Capital A/c — loss 2/3", 1200), ("By Lata's Capital A/c — loss 1/3", 600)], title='Realisation Account')
    qcap1, qb1 = capacc(['Kavi', 'Lata'], [('To Realisation A/c — land', {'Kavi': 72000}), ('To Realisation A/c — loss', {'Kavi': 1200, 'Lata': 600}), ('To Bank A/c', {'Kavi': qK, 'Lata': qL})],
                        [('By Balance b/d', {'Kavi': 75000, 'Lata': 45000}), ('By Profit and Loss A/c', {'Kavi': 6000, 'Lata': 3000}), ('By Realisation A/c — expenses', {'Kavi': 1900})])
    assert all(abs(v) < 0.01 for v in qb1.values()), qb1
    qbank1 = tacc([('To Balance b/d', 18000), ('To Realisation A/c — assets', qreal)],
                  [('By Realisation A/c — creditors', qcred), ('By Realisation A/c — repairs', 1200), ("By Lata's Loan A/c", 15000), ("By Kavi's Capital A/c", qK), ("By Lata's Capital A/c", qL)], title='Bank Account')

    qc2 = Checks()
    oD = qc2.add('20000-23000-4000+2000', "Om's balance after estate pays ₹2,000 (negative = deficiency)")
    qdM = qc2.add('5000*60000/100000', 'Deficiency borne by Mohan (fixed capitals 60:40)')
    qdN = qc2.add('5000*40000/100000', 'Deficiency borne by Naveen')
    Q2 = [
        je('(1)', [("Mohan's Current A/c", 5000)], [("Mohan's Capital A/c", 5000)], 'Being current account balance transferred to capital'),
        je('(2)', [("Naveen's Capital A/c", 2000), ("Om's Capital A/c", 23000)], [("Naveen's Current A/c", 2000), ("Om's Current A/c", 23000)], 'Being debit balances of current accounts transferred to capital'),
        je('(3)', [("Mohan's Capital A/c", 12000), ("Naveen's Capital A/c", 8000), ("Om's Capital A/c", 4000)], [('Realisation A/c', 24000)], 'Being realisation loss shared 3:2:1'),
        je('(4)', [('Bank A/c', 20000)], [("Mohan's Capital A/c", 12000), ("Naveen's Capital A/c", 8000)], 'Being solvent partners bringing cash equal to their share of realisation loss (Garner v. Murray)'),
        je('(5)', [('Bank A/c', 2000)], [("Om's Capital A/c", 2000)], "Being amount recovered from Om's estate"),
        je('(6)', [("Mohan's Capital A/c", qdM), ("Naveen's Capital A/c", qdN)], [("Om's Capital A/c", -oD)], "Being Om's deficiency borne by solvent partners in their fixed capital ratio 3:2"),
    ]

    qc3 = Checks()
    st3 = hrc_steps({'P': 30000, 'Q': 40000, 'R': 26000}, {'P': 2, 'Q': 2, 'R': 1}, ['P', 'Q', 'R'])
    assert st3 == [{'P': 0, 'Q': 10000, 'R': 11000}, {'Q': 0, 'R': 6000}], st3
    qc3.add('30000/2', "P's capital per unit (base)"); qc3.add('40000-15000*2', "Q's excess"); qc3.add('26000-15000*1', "R's excess")
    qc3.add('11000-(10000/2)*1', "R's excess after round 2")
    qP = qc3.add('6000+12000', 'Total to P'); qQ = qc3.add('4000+6000+6000+12000', 'Total to Q'); qR = qc3.add('6000+2000+3000+3000+6000', 'Total to R')
    qc3.add('30000-30000*2/5', 'Check P = capital − 2/5 of loss ₹30,000'); qc3.add('40000-30000*2/5', 'Check Q'); qc3.add('26000-30000*1/5', 'Check R')
    q3d = table(['Distribution', 'Cash (₹)', 'P (₹)', 'Q (₹)', 'R (₹)'], [
        ['1st — R alone', '12,000', '', '', '6,000'], ['1st — balance Q and R 2:1', '', '', '4,000', '2,000'],
        ['2nd — rest of Q/R stage 2:1', '24,000', '', '6,000', '3,000'], ['2nd — balance 2:2:1', '', '6,000', '6,000', '3,000'],
        ['3rd — all 2:2:1', '30,000', '12,000', '12,000', '6,000'], ['Total', '66,000', inr(qP), inr(qQ), inr(qR)]], num=[1, 2, 3, 4], total=True, title='Distribution of instalments')

    # ============ Case ============
    kc = Checks()
    k_def = kc.add('5000-4000', "Usha's deficiency")
    k_s = kc.add('1000*50000/80000', "Sonu's share of deficiency (capital ratio 5:3)")
    k_t = kc.add('1000*30000/80000', "Tina's share")
    k_pay = kc.add('30000-10000+10000-375', 'Final payment to Tina')

    concepts = [
        {'id': 'c1', 'title': 'Dissolution of partnership vs dissolution of the firm',
         'body': ['Dissolution of the partnership means the relation among the partners changes — a partner is admitted, retires or dies, or the ratio changes — but the business goes on under a reconstituted partnership. Assets are revalued (Revaluation Account) and the books continue.',
                  'Dissolution of the firm (Section 39) means the relation among ALL the partners ends and the business is closed. Assets are sold, liabilities paid, a Realisation Account is prepared and the books are closed. Courts can order it.',
                  'Every dissolution of a firm involves dissolution of the partnership, but not every dissolution of the partnership dissolves the firm.'],
         'blocks': [table(['Point', 'Dissolution of partnership', 'Dissolution of firm'], [
             ['Business', 'Continues', 'Comes to an end'], ['Account prepared', 'Revaluation Account', 'Realisation Account'], ['Books', 'Not closed', 'Closed'],
             ['Court', 'No role', 'May order it (s. 44)'], ['Assets and liabilities', 'Revalued', 'Realised and paid off']])],
         'analogy': 'Changing the line-up of a band (the band plays on) vs the band breaking up for good (instruments sold, debts paid, money divided).',
         'work': 'Clients often say "we are dissolving" when they only mean a partner is leaving. The accountant must ask which one it is — the accounting and tax consequences are very different.'},
        {'id': 'c2', 'title': 'When is a firm dissolved?',
         'body': ['By agreement (s. 40): all partners agree, or as per the contract.',
                  'Compulsory (s. 41): all partners, or all but one, become insolvent; or the business becomes unlawful.',
                  'On contingencies (s. 42), subject to contract: expiry of the fixed term; completion of the venture; death of a partner; insolvency of a partner.',
                  'By notice (s. 43): in a partnership at will, any partner may give written notice of his intention to dissolve.',
                  'By the court (s. 44), on a partner\'s suit, where a partner becomes of unsound mind, is permanently incapable, is guilty of misconduct affecting the business, persistently breaches the agreement, or transfers his whole interest to a third party; where the business can be carried on only at a loss; or on any other just and equitable ground.'],
         'analogy': 'A contract can end because both sides agree, because the law forbids it, because its time is up, because one side walks away (if allowed), or because a judge ends it.',
         'work': 'Before drafting a dissolution deed the CA checks which ground applies — the date of dissolution (and therefore the date to which accounts are drawn up) depends on it.'},
        {'id': 'c3', 'title': 'Settlement of accounts — Section 48 order, and refund of premium',
         'body': ['Losses, including deficiencies of capital, are met first out of profits, then out of capital, and lastly by the partners individually in their profit-sharing ratio.',
                  'The assets of the firm (including amounts contributed by partners to make good deficiencies) are applied in this order: (i) debts to third parties; (ii) partners\' advances (loans), rateably; (iii) partners\' capital, rateably; (iv) any surplus divided in the profit-sharing ratio.',
                  'Section 51: a partner who paid a premium on joining for a fixed term is entitled to a reasonable refund if the firm is dissolved before that term ends — unless the dissolution is due to death, or mainly due to his own misconduct, or under an agreement containing no provision for refund. The refund is borne by the other partners in their profit-sharing ratio.'],
         'analogy': 'Unwinding a shared purchase: first repay outsiders, then repay friends who lent extra, then return everyone\'s contribution, and split whatever is left.',
         'work': 'Liquidators and accountants winding up a firm prepare a statement of affairs in exactly the Section 48 order to show creditors and partners where every rupee went.'},
        {'id': 'c4', 'title': 'Realisation Account — closing the books',
         'body': ['Debit Realisation with all assets at book value except cash/bank, fictitious assets (debit balance of P&L) and partners\' accounts. Gross debtors go across; the provision is credited separately.',
                  'Credit Realisation with all outside liabilities at book value and with provisions against assets. Partners\' capital, current and loan accounts, reserves and P&L balances are NOT transferred.',
                  'Credit Realisation with cash from assets sold (including unrecorded assets) and with the agreed value of assets taken over by partners (debit their capitals). Debit Realisation with cash paid to settle liabilities (including unrecorded ones), with liabilities taken over by partners (credit their capitals) and with realisation expenses (credit Bank, or the partner who paid them).',
                  'Balance = profit or loss on realisation, shared in the profit-sharing ratio. Then repay partners\' loans, distribute reserves/accumulated profits (or losses), and settle the capital accounts — the bank balance left equals the total of the partners\' credit balances.',
                  'Goodwill: if it appears in the books it is treated like any asset (to Realisation); if not, no entry, but any amount realised for it is credited to Realisation.'],
         'blocks': [table(['Item', 'Entry'], [
             ['Assets at book value', 'Realisation A/c Dr. To Asset A/cs'], ['Liabilities and provisions', 'Liability/Provision A/cs Dr. To Realisation A/c'],
             ['Assets sold', 'Bank A/c Dr. To Realisation A/c'], ['Asset taken by a partner', "Partner's Capital A/c Dr. To Realisation A/c"],
             ['Liabilities paid', 'Realisation A/c Dr. To Bank A/c'], ['Expenses (paid by firm / by a partner)', 'Realisation A/c Dr. To Bank A/c / Partner\'s Capital A/c'],
             ['Loss shared', "Partners' Capital A/cs Dr. To Realisation A/c"], ['Final settlement', "Partners' Capital A/cs Dr. To Bank A/c"]])],
         'analogy': 'A garage sale ledger: list everything at what you paid, note what it actually fetched and what you paid off, and the difference is the gain or loss to share.',
         'work': 'In practice the "realisation" may take months; the accountant keeps the Realisation Account open, records each sale, and gives partners interim statements.'},
        {'id': 'c5', 'title': 'Insolvency of a partner and the rule in Garner v. Murray',
         'body': ['Consequences of insolvency (s. 34): the insolvent partner ceases to be a partner on the date of the order of adjudication; the firm is dissolved on that date unless the partners have agreed otherwise; his estate is not liable for acts of the firm after that date; and the firm is not liable for his acts after that date.',
                  'If, on dissolution, a partner\'s capital shows a debit balance and he is insolvent, the shortfall (after whatever his estate pays) is a loss to the other partners.',
                  'Garner v. Murray (an English case followed in India unless the deed provides otherwise): (1) the ordinary realisation loss is shared by ALL partners, including the insolvent one, in the profit-sharing ratio, and the solvent partners bring in cash for their share of it (in practice a notional entry); (2) the insolvent partner\'s deficiency is borne by the solvent partners in the ratio of their capitals; (3) a solvent partner whose capital is in debit bears no part of the deficiency.'],
         'analogy': 'If one member of a group cannot pay his share of a bill, the others cover it in proportion to how much they had put into the kitty — not in proportion to how much they ate.',
         'work': 'Partners are often surprised that the deficiency is shared in the capital ratio. A CA must check the deed first — it may override Garner v. Murray.'},
        {'id': 'c6', 'title': 'Capital ratio for Garner v. Murray; when all partners are insolvent',
         'body': ['Fixed capitals: the deficiency is shared in the ratio of the fixed capitals; current account balances are ignored for this purpose.',
                  'Fluctuating capitals: use the capitals as they stand just before dissolution after adjusting reserves, accumulated profits/losses, drawings, interest on capital and on drawings up to that date — but BEFORE the realisation profit or loss.',
                  'All partners insolvent: the firm\'s assets and the partners\' private contributions are not enough to pay creditors in full. Creditors are then not passed through the Realisation Account; they are paid what is available, and the unpaid balance is transferred to a Deficiency Account and closed to the partners\' capital accounts. Close the account of the partner in the worst position first; the last account closes automatically.'],
         'analogy': 'The kitty shares are measured on the day the trip ended, before anyone counts the losses on selling the leftover gear.',
         'work': 'An examiner\'s favourite trap is to use capitals after the realisation loss. Write "capital ratio before realisation loss" in your working note.'},
        {'id': 'c7', 'title': 'Piecemeal distribution — maximum loss method',
         'body': ['Assets are often sold over months. Partners want cash as it comes, but each payment must be safe: no partner should be paid an amount he might later have to return.',
                  'Maximum loss method: treat each instalment as if it were the last — assume all unsold assets are worthless. Share this "maximum possible loss" in the profit-sharing ratio; if any partner\'s balance turns negative, share his notional shortfall among the others (by Garner v. Murray or the profit ratio, as the question says). Pay each partner his remaining positive balance.',
                  'The order of payment is always: realisation expenses → outside liabilities → partners\' loans → partners\' capitals.'],
         'analogy': 'Sharing money from a pile of lottery tickets as each one is checked: pay out only what you would still owe even if every unchecked ticket were a blank.',
         'work': 'Liquidators of firms use exactly this safety logic before making any interim payment to partners.'},
        {'id': 'c8', 'title': 'Piecemeal distribution — highest relative capital (proportionate capital) method',
         'body': ['Divide each partner\'s capital by his profit-sharing ratio; the smallest figure is the base. Multiply the base by each partner\'s ratio to get his proportionate capital; actual minus proportionate = excess capital. Repeat among the partners who still have excess until their excesses are in their mutual profit ratio.',
                  'Pay the partner with the largest relative excess first, then the next group in their ratio, until all capitals are in the profit-sharing ratio; from then on every instalment is paid in the profit-sharing ratio.',
                  'Both methods give the same total to each partner; the highest relative capital method decides the order of payment in advance.'],
         'analogy': 'Before sharing equally, first top up those who had put in more than their fair share, until everyone stands level.',
         'work': 'A one-page "payment order" schedule prepared at the start lets the accountant release cash immediately as each asset is sold.'},
        {'id': 'c9', 'title': 'Winding up of a Limited Liability Partnership',
         'body': ['An LLP may be wound up voluntarily or by the Tribunal, and an LLP so wound up may then be dissolved.',
                  'The Tribunal may order winding up where: the LLP itself decides so; it has had fewer than two partners for more than six months; it cannot pay its debts; it has acted against the sovereignty and integrity of India, the security of the State or public order; it has not filed its statement of account and solvency or annual return for any five consecutive financial years; or the Tribunal thinks it just and equitable.',
                  'The Central Government may make rules for winding up and dissolution. In the books, the realisation of assets and payment of liabilities are recorded much as for a firm, but partners\' liability is limited to their agreed contribution.'],
         'analogy': 'A company-style exit for a partnership-style business: the process is formal and supervised, and members lose only what they agreed to put in.',
         'work': 'Many small LLPs stop business but forget their annual filings; five years of default is itself a ground for winding up — a common compliance point raised by CAs with clients.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Closing the books of a dissolved firm', 'difficulty': 'moderate', 'minutes': 25,
         'q': ('Ajay and Bina share profits 3:2. Balance Sheet at 31 December 2026: Creditors ₹48,000; Bills payable ₹12,000; Bina\'s loan ₹20,000; General Reserve ₹15,000; Capitals — Ajay ₹90,000, Bina ₹60,000 (total ₹2,45,000). '
               'Assets: Machinery ₹75,000; Furniture ₹18,000; Investments ₹22,000; Stock ₹40,000; Debtors ₹50,000 less provision ₹2,500; Bank ₹42,500. The firm is dissolved on that date. '
               'Ajay takes the investments at ₹25,000. Machinery realises ₹68,000, furniture ₹12,000, stock ₹36,000 and debtors ₹46,000. An old computer not shown in the books is sold for ₹5,000. Creditors are paid less 2.5% discount; bills payable in full. Realisation expenses ₹3,000. '
               'Pass journal entries and prepare the Realisation Account, Partners\' Capital Accounts and Bank Account.'),
         'solution': [journal(E1, 'Journal', 'j1'), real1, cap1, bank1,
                      note('Bina\'s loan is paid before capitals (s. 48 order) and is not passed through Realisation. The general reserve goes straight to the capital accounts.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Insolvency of a partner — Garner v. Murray', 'difficulty': 'hard', 'minutes': 20,
         'q': ('Dhruv, Ela and Faiz share profits 2:2:1 (fluctuating capitals). On dissolution: Creditors ₹40,000; Capitals — Dhruv ₹90,000, Ela ₹60,000, Faiz ₹3,000; Sundry assets ₹1,80,000; Bank ₹13,000. '
               'Assets realised ₹1,57,000; creditors paid in full; expenses ₹2,000. Faiz is insolvent and his estate pays 30 paise in the rupee on what he owes. Apply Garner v. Murray and prepare the Realisation Account, Capital Accounts and Bank Account.'),
         'solution': [wn('Deficiency', f'Loss on realisation ₹{inr(loss2)} → Dhruv ₹10,000, Ela ₹10,000, Faiz ₹5,000. Faiz owes 5,000 − 3,000 = ₹2,000; estate pays 30% = ₹600; deficiency ₹{inr(defi)}. Solvent partners\' capitals before the realisation loss: 90,000 : 60,000 = 3:2 → Dhruv ₹{inr(dD)}, Ela ₹{inr(dE)}.'),
                      real2, cap2, bank2,
                      note('Dhruv and Ela bring in cash equal to their realisation loss (₹10,000 each). In practice this is only a book entry, since the same cash is paid back to them at once.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Piecemeal distribution — highest relative capital method', 'difficulty': 'hard', 'minutes': 20,
         'q': 'X, Y and Z share profits 3:2:1. After paying all outside liabilities and expenses, their capitals stand at X ₹48,000, Y ₹44,000 and Z ₹28,000. The remaining assets are realised in three instalments that leave ₹9,000, ₹27,000 and ₹54,000 available for the partners. Show how each instalment should be distributed using the highest relative capital method, and cross-check the first instalment by the maximum loss method.',
         'solution': [hrc, dist_t, mlc, p(f'Final check: total loss = 1,20,000 − 90,000 = ₹{inr(loss3)}, shared 3:2:1 → X receives 48,000 − 15,000 = ₹33,000, Y 44,000 − 10,000 = ₹34,000, Z 28,000 − 5,000 = ₹23,000 — matching the distribution.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Refund of premium on premature dissolution', 'difficulty': 'core', 'minutes': 6,
         'q': 'Gopal joined Hema and Ishan for a fixed term of five years, paying them a premium of ₹60,000. Hema and Ishan share between themselves 2:1. After two years the court dissolves the firm on Hema\'s petition because Ishan persistently breached the partnership agreement. (a) Is Gopal entitled to a refund? Pass the entry. (b) What if the dissolution had been caused mainly by Gopal\'s own misconduct?',
         'solution': [legal('Section 51 of the Indian Partnership Act, 1932: a partner who has paid a premium on entering a partnership for a fixed term is entitled, on dissolution before the term expires, to a reasonable refund — except where dissolution is due to the death of a partner, is mainly due to his own misconduct, or is under an agreement that contains no provision for return of the premium.',
                            'Gopal paid ₹60,000 for a 5-year term; the court dissolves the firm after 2 years because of Ishan\'s conduct — not because of death, not because of Gopal\'s misconduct, and not under an agreement.',
                            f'A reasonable refund is in proportion to the unexpired term: 60,000 × 3/5 = ₹{inr(refund)}, borne by Hema and Ishan 2:1 (₹{inr(rH)} and ₹{inr(rI)}). Had the partners dissolved the firm by an agreement with no provision for returning the premium, no refund would be due.',
                            f'(a) Gopal gets ₹{inr(refund)}. (b) If the dissolution were mainly due to his own misconduct, he would get nothing.'),
                      journal(E4, 'Journal', 'j4')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Winding up a family firm', 'role': 'CA in practice appointed by the partners',
         'situation': 'Three brothers have decided to close their wholesale business. Stock and debtors will be realised over six months; one brother wants to take the delivery van.',
         'steps': ['Draft the dissolution deed stating the date, the ground (agreement) and who will realise the assets.',
                   'Open a Realisation Account: transfer assets and outside liabilities at book value; record each sale as it happens.',
                   'Record the van taken over at an agreed value by debiting that brother\'s capital.',
                   'Pay outsiders first, then partners\' loans, following Section 48; distribute interim cash using the highest relative capital method so nobody is overpaid.',
                   'Close the books, file the final returns and keep the working papers — partners often come back with questions years later.'],
         'takeaway': 'Dissolution is a sequence: realise, pay outsiders, repay partners\' loans, then settle capitals — and document every step.',
         'think': 'One brother is personally insolvent and his capital account ends in debit. The deed is silent. How is his deficiency shared?',
         'answer': 'By the other two brothers in the ratio of their capitals just before dissolution (Garner v. Murray), after each has made good his own share of the realisation loss.'},
        {'id': 'j2', 'title': 'An inactive LLP', 'role': 'Compliance manager at a CA firm',
         'situation': 'A client\'s LLP stopped business four years ago and has filed nothing since. One of its two partners has resigned.',
         'steps': ['Point out the risks: an LLP with fewer than two partners for more than six months, and five consecutive years of non-filing, are both grounds on which the Tribunal may order winding up.',
                   'Advise either admitting a second partner and bringing filings up to date, or closing the LLP through the proper process.',
                   'If closing, prepare final accounts: realise assets, settle liabilities and distribute the balance to partners per the LLP agreement.'],
         'takeaway': 'An LLP cannot simply be abandoned; it has to be wound up and dissolved through the legal process.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'On dissolution, which of the following is NOT transferred to the Realisation Account?', 'options': ["A partner's loan to the firm", 'Bills payable', 'Provision for doubtful debts', 'Stock'], 'answer': 0, 'explain': "On dissolution, all assets (except cash) and all outside liabilities, along with provisions against assets, are transferred to the Realisation Account. A partner's loan is not an outside liability; under Section 48 it is repaid separately after outsiders, through its own account. The trap is 'provision for doubtful debts' — provisions are transferred, because they reduce the related asset. In practice: when a firm closes, the accountant settles creditors through realisation and pays partners' loans afterwards from the remaining cash.", 'topic': "Consequences of Dissolution", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'An unrecorded asset realised for cash on dissolution is credited to:', 'options': ['Realisation Account', "Partners' Capital Accounts", 'Cash Account', 'Profit and Loss Account'], 'answer': 0, 'explain': "An asset not recorded in the books, when sold on dissolution, brings in cash that was not expected. It is a gain on realisation: Bank A/c Dr, To Realisation A/c. The trap is crediting partners' capitals directly, which bypasses the Realisation Account and hides the realisation result. In practice: on closure, fully depreciated equipment or old scrap written off years ago often fetches some value and is recorded this way.", 'topic': "Consequences of Dissolution", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Under Section 48, after paying third-party debts, the next payment out of the firm\'s assets is to:', 'options': ['Partners for their advances (loans), rateably', 'Partners for capital', 'Partners in the profit-sharing ratio', 'The partner with the largest capital'], 'answer': 0, 'explain': "Section 48 of the Partnership Act lays down the order of applying assets: first, debts to third parties; next, partners' advances (loans) rateably; then, partners' capital rateably; finally, any surplus in profit-sharing ratio. The trap is 'partners for capital', which comes only after loans are repaid. In practice: a CA settling a dissolved firm's accounts follows this order strictly to avoid disputes among partners and claims from creditors.", 'topic': "Consequences of Dissolution", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Under Garner v. Murray, the deficiency of an insolvent partner is borne by the solvent partners in the ratio of their:', 'options': ['Capitals just before dissolution (before realisation loss)', 'Profit-sharing ratio', 'Capitals after the realisation loss', 'Drawings'], 'answer': 0, 'explain': "Under the rule in Garner v. Murray, solvent partners bear an insolvent partner's deficiency in the ratio of their capitals just before dissolution — after adjusting reserves, drawings and past profits, but before the realisation profit or loss. The trap is the profit-sharing ratio, which applies only if the deed says so. In practice: partnership deeds often override Garner v. Murray to share any deficiency in the profit ratio, which is simpler.", 'topic': "Loss Arising From Insolvency of a Partner", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Which of these leads to compulsory dissolution of a firm under Section 41?', 'options': ['The business becoming unlawful', 'Death of a partner', 'Expiry of the fixed term', 'A partner becoming of unsound mind'], 'answer': 0, 'explain': "Section 41 provides for compulsory dissolution when all partners, or all but one, become insolvent, or when the business becomes unlawful. The trap is death of a partner, which dissolves the firm under Section 42 only subject to any contract between the partners; a partner of unsound mind is a ground for the court to dissolve under Section 44. In practice: if a firm's licensed activity is banned by law, the firm stands dissolved, regardless of the partners' wishes.", 'topic': "Circumstances Leading to Dissolution of Partnership", 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'Realisation expenses of ₹4,000 are paid by partner A on behalf of the firm. The entry is:', 'options': ["Realisation A/c Dr. To A's Capital A/c", "A's Capital A/c Dr. To Realisation A/c", 'Realisation A/c Dr. To Bank A/c', 'No entry'], 'answer': 0, 'explain': "Realisation expenses are a cost of closing the firm, so they are debited to the Realisation Account. Because partner A paid them personally, the firm owes him that amount, so his capital account is credited. Entry: Realisation A/c Dr, To A's Capital A/c. The trap 'Realisation Dr, To Bank' applies only when the firm pays from its own funds. In practice: partners often pay closure costs like legal fees themselves, and these are adjusted in the final settlement.", 'topic': "Consequences of Dissolution", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'Creditors of ₹50,000 accept ₹46,000 in full settlement. The amount debited to Realisation Account for this payment is:', 'options': ['₹46,000', '₹50,000', '₹4,000', '₹96,000'], 'answer': 0, 'check': '46000', 'explain': "Creditors were transferred to the credit of the Realisation Account at their book value of ₹50,000. When they accept ₹46,000 in full settlement, the cash paid of ₹46,000 is debited to Realisation. The ₹4,000 saving automatically shows up in the realisation result. The trap ₹50,000 debits the book value, which would wipe out the saving. In practice: suppliers often accept a discount for quick settlement when a firm closes.", 'topic': "Consequences of Dissolution", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'A, B and C share 2:2:1. Capitals: A ₹40,000, B ₹30,000, C ₹25,000. Under the highest relative capital method, the partner to be paid first is:', 'options': ['C', 'A', 'B', 'A and B equally'], 'answer': 0, 'explain': "Relative capital = capital ÷ profit-sharing ratio. A: 40,000 ÷ 2 = 20,000; B: 30,000 ÷ 2 = 15,000; C: 25,000 ÷ 1 = 25,000. C has the highest relative capital, so C is paid first until his capital falls into line with the others. The trap is A, who has the highest absolute capital. In practice: liquidators distribute cash in instalments this way so that no partner later has to refund money.", 'topic': "Piecemeal Payments", 'concept': 'c8', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'Under the maximum loss method, each instalment realised is treated as:', 'options': ['The final amount, with all unsold assets assumed worthless', 'Payable in the capital ratio', 'Payable only to the partner with the largest capital', 'Payable equally'], 'answer': 0, 'explain': "Under the maximum loss method, each instalment is treated as if it were the final amount and all remaining assets are worthless. The possible loss is shared in the profit ratio, and only the surplus is paid. This makes every payment safe — no partner will be asked to refund later. The trap 'payable in capital ratio' ignores that losses are shared in the profit ratio. In practice: when assets of a closing firm sell slowly, partners receive cash in safe instalments.", 'topic': "Piecemeal Payments", 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'An LLP may be wound up by the Tribunal if the number of its partners is reduced below two for a period of more than:', 'options': ['Six months', 'Three months', 'One year', 'Thirty days'], 'answer': 0, 'explain': "Under Section 64 of the LLP Act, 2008, the Tribunal may wind up an LLP if the number of partners falls below two for more than six months, among other grounds. The trap is three months, which is too short. In practice: when one of two partners of an LLP dies or exits, the remaining partner must bring in a new partner within six months, or the LLP risks being wound up.", 'topic': "Winding Up of a Limited Liability Partnership (LLP)", 'concept': 'c9', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'Capitals: P ₹30,000, Q ₹20,000 (solvent); R is insolvent with a deficiency of ₹5,000. Under Garner v. Murray, P bears:', 'options': ['₹3,000', '₹2,500', '₹2,000', '₹5,000'], 'answer': 0, 'check': '5000*30000/50000', 'explain': "Under Garner v. Murray, solvent partners bear the deficiency in the ratio of their capitals just before dissolution. P : Q = 30,000 : 20,000 = 3 : 2. P bears 5,000 × 3/5 = ₹3,000 and Q ₹2,000. The trap ₹2,500 splits the deficiency equally, ignoring capitals. In practice: partners with larger capitals bear more of a co-partner's insolvency loss, which is why deeds often specify the sharing ratio.", 'topic': "Loss Arising From Insolvency of a Partner", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm12', 'q': 'A partner who paid a premium for a fixed-term partnership is NOT entitled to any refund on premature dissolution when:', 'options': ['The dissolution is mainly due to his own misconduct', 'The court dissolves the firm because of another partner\'s misconduct', 'Two years of the term remain', 'The other partners agree to dissolve'], 'answer': 0, 'explain': "Section 51 of the Partnership Act lets a partner who paid a premium for a fixed-term partnership claim a refund on early dissolution, except when dissolution is due to death, mainly due to his own misconduct, or under an agreement with no provision for refund. The trap is 'court dissolves because of another partner's misconduct' — there he is entitled to a refund. In practice: deeds with entry premiums often specify refund terms to prevent disputes.", 'topic': "Consequences of Dissolution", 'concept': 'c3', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'table',
         'q': ('Kavi and Lata share profits 2:1. On 30 September 2026, when they dissolve the firm, the Balance Sheet shows: Creditors ₹36,000; Lata\'s loan ₹15,000; Profit and Loss Account (credit) ₹9,000; Capitals — Kavi ₹75,000, Lata ₹45,000 (total ₹1,80,000). '
               'Assets: Land ₹60,000; Machinery ₹45,000; Stock ₹27,000; Debtors ₹30,000; Bank ₹18,000. Kavi takes over the land at ₹72,000. Machinery realises ₹38,000, stock ₹24,000 and debtors ₹27,500. Creditors accept 5% less. '
               'A bill for repairs of ₹1,200, not recorded, is paid. Realisation expenses of ₹1,900 are paid by Kavi. Prepare the Realisation Account, Partners\' Capital Accounts and Bank Account.'),
         'model': [qreal1, qcap1, qbank1],
         'scheme': [{'id': 's1', 'pt': 'Assets and creditors transferred at book value to the correct sides', 'm': 1.5, 'skill': 'posting'},
                    {'id': 's2', 'pt': 'Realisations ₹89,500 and land to Kavi ₹72,000 credited', 'm': 1.5, 'skill': 'posting'},
                    {'id': 's3', 'pt': 'Creditors paid ₹34,200, unrecorded repairs ₹1,200, expenses ₹1,900 credited to Kavi', 'm': 1.5, 'skill': 'application'},
                    {'id': 's4', 'pt': 'Loss on realisation ₹1,800 shared 2:1', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'P&L credit balance and loan treated outside Realisation', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's6', 'pt': 'Capital accounts closed: Kavi ₹9,700, Lata ₹47,400', 'm': 1.5, 'skill': 'balancing'},
                    {'id': 's7', 'pt': 'Bank account balances to nil', 'm': 1, 'skill': 'presentation'}],
         'checks': qc1,
         'remarks': ['Many candidates transfer Lata\'s loan to Realisation — it must be paid directly from the bank after outsiders.',
                     'Expenses paid by a partner are frequently credited to Bank; the partner who paid must be credited.',
                     'If the bank account does not close at nil, there is an error in the capital accounts — check before finishing.'],
         'mistakes': ['Transferring the P&L credit balance to Realisation.', 'Debiting Realisation with ₹36,000 (book value) for creditors instead of the ₹34,200 paid.', 'Ignoring the unrecorded repairs bill.'],
         'tips': ['Prepare Realisation, Capital and Bank accounts side by side; the bank must end at nil.', 'Label each Realisation entry with a short description (e.g. "Bank — creditors").']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'journal',
         'q': ('Mohan, Naveen and Om share profits 3:2:1 and maintain fixed capitals of ₹60,000, ₹40,000 and ₹20,000. On dissolution their current accounts show: Mohan ₹5,000 (Cr), Naveen ₹2,000 (Dr), Om ₹23,000 (Dr). '
               'The loss on realisation is ₹24,000. Om is insolvent and only ₹2,000 can be recovered from his estate. Applying Garner v. Murray, pass journal entries to close Om\'s account and record the related adjustments.'),
         'model': [wn('Om\'s deficiency', f'Om: capital 20,000 − current 23,000 − loss 4,000 = ₹7,000 Dr; estate pays ₹2,000; deficiency ₹{inr(-oD)}. Fixed capitals of solvent partners 60,000 : 40,000 = 3:2 → Mohan ₹{inr(qdM)}, Naveen ₹{inr(qdN)}.'),
                   journal(Q2, 'Journal', 'jq2')],
         'scheme': [{'id': 's1', 'pt': 'Current account balances transferred to capitals', 'm': 1, 'skill': 'posting'},
                    {'id': 's2', 'pt': 'Realisation loss ₹24,000 shared 3:2:1 including Om', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Solvent partners bring cash for their share of loss', 'm': 1, 'skill': 'concept'},
                    {'id': 's4', 'pt': "Om's deficiency ₹5,000 computed after estate's ₹2,000", 'm': 1, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'Deficiency borne 3:2 in fixed capital ratio (₹3,000 / ₹2,000)', 'm': 2, 'skill': 'application'}],
         'checks': qc2,
         'remarks': ['The commonest error is sharing Om\'s deficiency in the profit ratio 3:2 between Mohan and Naveen "by coincidence" — here the fixed capital ratio is also 3:2, but the working must say capital ratio.',
                     'Candidates often exclude Om from the realisation loss; under Garner v. Murray he bears his share like everyone else.'],
         'mistakes': ['Using capitals after adjusting current accounts as the ratio when capitals are fixed.', 'Forgetting the cash brought in by solvent partners for the realisation loss.'],
         'tips': ['State the rule in one line before the entries: "loss on realisation in profit ratio; insolvency loss in capital ratio".']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
         'q': 'P, Q and R share profits 2:2:1. After paying creditors, their capitals are P ₹30,000, Q ₹40,000 and R ₹26,000. The remaining assets realise, net of expenses, ₹12,000, ₹24,000 and ₹30,000 in three instalments. Show the distribution using the highest relative capital method.',
         'model': [table(['Step', 'P (₹)', 'Q (₹)', 'R (₹)'], [
             ['Capitals', '30,000', '40,000', '26,000'], ['Ratio', '2', '2', '1'], ['Capital ÷ ratio', '15,000', '20,000', '26,000'],
             ['Proportionate capital on P\'s base', '30,000', '30,000', '15,000'], ['Excess (round 1)', 'nil', '10,000', '11,000'],
             ['Round 2: excess ÷ ratio', '—', '5,000', '11,000'], ['Proportionate on Q\'s base', '—', '10,000', '5,000'], ['Excess (round 2)', '—', 'nil', '6,000']], title='Order of payment'),
                   p('Pay ₹6,000 to R first; then ₹15,000 to Q and R in 2:1; thereafter 2:2:1.'), q3d],
         'scheme': [{'id': 's1', 'pt': 'Base capital and proportionate capitals (round 1)', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Round 2 between Q and R; R\'s excess ₹6,000', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'First two instalments distributed in the correct order', 'm': 2, 'skill': 'application'},
                    {'id': 's4', 'pt': 'Third instalment 2:2:1; totals P ₹18,000, Q ₹28,000, R ₹20,000', 'm': 1, 'skill': 'presentation'}],
         'checks': qc3,
         'remarks': ['Most candidates stop after round 1 and pay Q and R in 10:11 — the second round is essential.', 'A final total check against "capital minus share of total loss" earns credibility and catches errors.'],
         'mistakes': ['Paying R and Q in the capital ratio.', 'Paying P something in the first instalment.'],
         'tips': ['Always finish with the loss check: total loss shared in profit ratio must explain each partner\'s total receipt.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Explain the order in which the assets of a firm are applied on dissolution under the Indian Partnership Act, 1932, and how losses (including deficiency of capital) are met.',
         'model': [legal('Section 48 of the Indian Partnership Act, 1932 lays down the mode of settling accounts between partners after dissolution, subject to any agreement among them.',
                         'On dissolution a firm realises its assets; the proceeds and any amounts partners contribute to make good deficiencies must be applied in a fixed order.',
                         "Any loss, a shortfall of capital included, is met from profits first, then from capital, and finally by the partners personally in their profit-sharing ratio. Assets are applied: (i) outsiders — the firm's debts to third parties; (ii) partners' loans or advances (as distinct from capital), rateably; (iii) partners' capital, rateably; (iv) whatever remains, shared in the profit-sharing ratio.",
                         'Outsiders are always paid first, partners\' loans rank before capital, and only a true surplus is shared in the profit-sharing ratio.')],
         'scheme': [{'id': 's1', 'pt': 'Section 48 cited', 'm': 0.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Losses: profits → capital → partners individually in profit ratio', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Order of application: outsiders → advances → capital → residue', 'm': 2, 'skill': 'provision'}],
         'remarks': ['Many answers reverse advances and capital — partners\' loans are repaid before capital.'],
         'mistakes': ['Saying surplus is divided in the capital ratio.', 'Omitting the treatment of losses.'],
         'tips': ['Number the four steps of application exactly in order.']},
    ]

    viva = [
        V('v1', 'In what order are the assets of a firm applied on dissolution under Section 48?',
          'First the debts of the firm to third parties are paid. Next, partners\' loans or advances are repaid rateably, then partners\' capital rateably. Finally, any surplus left is divided among the partners in their profit sharing ratio.',
          [P('p1', 'First: outside / third-party debts', 3, ALT('first {c}', '{c} first', '{c} are paid first', '{c} come first', c=('third party', 'third parties', 'debt', 'debts', 'outside liability', 'outside liabilities', 'outsider', 'outsiders', 'creditor', 'creditors', 'outside creditor', 'outside creditors', 'external', 'firm debt', 'firm s debts'))),
           P('p2', 'Next: partners\' loans / advances', 3, 'loan|advance'),
           P('p3', 'Then: capital (after loans)', 2, ALT('{l} then {k}', '{l} {k}', '{k} after {l}', l=('loan', 'loans', 'advance', 'advances'), k=('capital', 'capitals'))),
           P('p4', 'Surplus in profit sharing ratio', 2, 'surplus|residue|balance|remaining|left', 'profit sharing|profit ratio|ratio', min=2)], 'c3'),
        V('v2', 'State the rule in Garner versus Murray.',
          'Under Garner versus Murray, the solvent partners bring in cash equal to their share of the loss on realisation, and the realisation loss is shared by all partners including the insolvent one in the profit sharing ratio. The solvent partners bear the insolvent partner\'s deficiency in their capital ratio, taking capitals just before dissolution, not in the profit sharing ratio. A solvent partner with a debit capital bears nothing.',
          [P('p1', 'Solvent partners bring cash for their share of realisation loss', 3, 'bring|brought|contribute|put in|introduce|pay in', 'realisation loss|realization loss|loss on realisation|loss on realization|their share of loss|share of the loss', min=1),
           P('p2', 'Insolvent partner\'s deficiency borne by solvent partners', 3, 'solvent partner|other partner|remaining partner|solvent'),
           P('p3', 'Deficiency in the capital ratio (not profit ratio)', 4, ALT('{d} {c}', '{d} borne by solvent partners {c}', '{d} borne by the solvent partners {c}', '{d} borne {c}', '{d} shared {c}', '{d} is shared {c}', '{d} bear {c}', d=('deficiency', 'deficit', 'shortfall', 'insolvency loss'), c=('capital ratio', 'ratio of their capital', 'ratio of their capitals', 'ratio of capital', 'ratio of capitals', 'proportion to their capital', 'proportion to their capitals', 'proportion of capital', 'capitals ratio', 'ratio of the capital')))], 'c5'),
        V('v3', 'Which items are transferred to the Realisation Account and which are not?',
          'All assets except cash and bank, at book value, are debited to the Realisation Account, and all outside liabilities and provisions against assets are credited to it. Partners\' capital, current and loan accounts, reserves, accumulated profits or losses, and cash or bank balances are not transferred to it.',
          [P('p1', 'Assets (except cash/bank) debited at book value', 3, 'asset', 'except cash|other than cash|excluding cash|not cash|except bank|except the cash|apart from cash|book value', min=2),
           P('p2', 'Outside liabilities and provisions credited', 3, 'liabilit|provision', min=1),
           P('p3', 'Partners\' accounts (capital/loan) not transferred', 2, 'partner loan|partners loan|loan of partner|partner s loan|capital|current account', min=1),
           P('p4', 'Reserves / accumulated profits not transferred', 2, 'reserve|accumulated|profit and loss|profit loss|undistributed', min=1)], 'c4'),
        V('v4', 'How does the highest relative capital method of piecemeal distribution work?',
          'Each partner\'s capital is divided by his profit sharing ratio, and the smallest figure is taken as the base. Proportionate capitals are worked out on that base and the excess of actual over proportionate capital is found, repeating among those with excess. The partner with the highest relative excess is paid first, then the next, until capitals are in the profit sharing ratio; after that cash is paid in the profit sharing ratio.',
          [P('p1', 'Capital divided by profit ratio; smallest as base', 3, 'divide|divided|per unit|capital ratio|base|basic capital|smallest|lowest', min=1),
           P('p2', 'Excess of actual over proportionate capital', 3, 'excess|surplus capital|extra capital|proportionate capital|hypothetical'),
           P('p3', 'Highest relative excess paid first', 2, 'paid first|pay first|first paid|first be paid|highest|largest|greatest|most', min=1),
           P('p4', 'Afterwards in profit sharing ratio', 2, 'profit sharing|profit ratio|ratio')], 'c8'),
        V('v5', 'What is the maximum loss method of piecemeal distribution?',
          'Under the maximum loss method each instalment is treated as if it were the final one, so all unsold assets are assumed to be worthless. The maximum possible loss is shared among partners in the profit sharing ratio, any notional deficiency of a partner is borne by the others, and each partner is paid his remaining positive balance.',
          [P('p1', 'Each instalment treated as the final / last', 3, 'final|last'),
           P('p2', 'Remaining assets assumed worthless', 4, 'worthless|nothing|zero|nil|no value|valueless|total loss|lost', min=1),
           P('p3', 'Maximum loss shared in profit ratio, balances paid', 3, 'profit sharing|profit ratio|ratio|balance', min=1)], 'c7'),
        V('v6', 'When may a firm be dissolved compulsorily, and on what grounds can the court dissolve it?',
          'A firm is compulsorily dissolved when all the partners or all but one become insolvent, or when the business becomes unlawful. The court may dissolve it when a partner becomes of unsound mind or permanently incapable, is guilty of misconduct, persistently breaches the agreement, or transfers his whole interest, when the business can only be carried on at a loss, or on just and equitable grounds.',
          [P('p1', 'Compulsory: insolvency of all / all but one partner', 3, 'insolven|bankrupt'),
           P('p2', 'Compulsory: business becomes unlawful', 3, 'unlawful|illegal|against the law|not legal'),
           P('p3', 'Court grounds (any two)', 4, 'unsound|insane|mental', 'incapab|incapacity', 'misconduct', 'breach|disregard|violat', 'transfer', 'loss', 'just and equitable|just equitable|fair', min=2)], 'c2'),
        V('v7', 'On what grounds may the Tribunal wind up a Limited Liability Partnership?',
          'The Tribunal may wind up an LLP if the LLP itself decides so; if it has fewer than two partners for more than six months; if it is unable to pay its debts; if it acts against the sovereignty and integrity of India; if it fails to file its statement of account and solvency or annual return for five consecutive financial years; or if the Tribunal thinks it just and equitable.',
          [P('p1', 'Fewer than two partners for more than six months', 3, 'less than two|fewer than two|below two|less than 2|fewer than 2|below 2|one partner|single partner', '6 month|six month|half year', min=2),
           P('p2', 'Unable to pay debts', 2, 'unable to pay|cannot pay|can not pay|not able to pay|insolven|debts'),
           P('p3', 'Default in filing for five consecutive years', 3, 'five|5|not file|not filed|not filing|failed to file|fails to file|failure to file|default|non filing', 'year|filing|return|statement', min=2),
           P('p4', 'LLP decides / just and equitable / against sovereignty (any one)', 2, 'wish|decide|resolve|resolution|just and equitable|just equitable|sovereignty|integrity|security', min=1)], 'c9'),
    ]

    kcase = [{'id': 'k1', 'title': 'Sonu, Tina & Usha close shop', 'difficulty': 'hard',
              'case': ('Sonu, Tina and Usha share profits 2:2:1 with fluctuating capitals. Just before dissolution (after adjusting reserves and drawings) their capitals are Sonu ₹50,000, Tina ₹30,000 and Usha ₹4,000. '
                       'The loss on realisation is ₹25,000. Usha is insolvent and nothing can be recovered from her estate. The deed is silent about insolvency.'),
              'mcqs': [
                  M('k1a', "What is Usha's deficiency?", [R(k_def), R(5000), R(4000), R(9000)], 0, "Usha's share of realisation loss = 25,000 × 1/5 = ₹5,000. Her capital is only ₹4,000, so after absorbing the loss she has a debit balance (deficiency) of 5,000 − 4,000 = ₹1,000, which she cannot pay. The trap ₹5,000 is her share of loss, not her deficiency. In practice: when a partner of a closing firm is insolvent, the remaining partners must absorb the shortfall.", 'moderate', '5000-4000') | {'topic': "Consequences of Insolvency of a Partner"},
                  M('k1b', "How much of Usha's deficiency does Sonu bear?", [R(k_s), R(500), R(400), R(1000)], 0, "With the deed silent, Garner v. Murray applies: solvent partners bear the deficiency in the ratio of their capitals just before dissolution. Sonu : Tina = 50,000 : 30,000 = 5 : 3. Sonu bears 1,000 × 5/8 = ₹625; Tina ₹375. The trap ₹500 uses the profit ratio 2 : 2. In practice: partners with larger capitals bear more of a co-partner's insolvency loss.", 'hard', '1000*50000/80000') | {'topic': "Loss Arising From Insolvency of a Partner"},
                  M('k1c', 'Which capitals decide the ratio for sharing the deficiency?', ['Capitals just before dissolution, before the realisation loss', 'Capitals after the realisation loss', 'Original capitals introduced', 'Profit-sharing ratio'], 0, "Garner v. Murray uses capitals just before dissolution — after adjusting reserves, drawings and past profits, but before the realisation profit or loss. Since capitals are fluctuating, those are the balances given: Sonu 50,000 and Tina 30,000. The trap is capitals after realisation loss, which would mix up the loss-sharing with the deficiency-sharing. In practice: accountants extract capitals at the point of dissolution to apply this rule correctly.", 'moderate') | {'topic': "Loss Arising From Insolvency of a Partner"},
                  M('k1d', 'What is the final amount paid to Tina?', [R(k_pay), R(20000), R(19625), R(30000)], 0, "Tina's capital 30,000 − share of realisation loss (25,000 × 2/5 = 10,000) + cash brought in for her loss share 10,000 (required by Garner v. Murray) − share of Usha's deficiency 375 = ₹29,625. The trap ₹19,625 forgets that solvent partners bring in cash equal to their share of realisation loss. In practice: this rule ensures solvent partners bear the insolvent partner's deficiency only from their capitals.", 'hard', '30000-10000+10000-375') | {'topic': "Loss Arising From Insolvency of a Partner"},
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch10', 'n': 6,
        'title': 'Dissolution of Partnership Firms and LLPs',
        'outcomes': [
            'Distinguish dissolution of a partnership from dissolution of a firm and list the circumstances in which a firm is dissolved.',
            'Apply the Section 48 order of settlement and the Section 51 rule on refund of premium.',
            'Close the books of a dissolved firm through Realisation, Capital and Bank Accounts.',
            'Apply the rule in Garner v. Murray when a partner is insolvent, and handle insolvency of all partners.',
            'Distribute cash realised in instalments by the maximum loss and highest relative capital methods.',
            'State the grounds on which an LLP may be wound up.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 80}, 'prereq': ['fnd-p1-ch10-u01'],
                 'exam_tip': 'A dissolution answer is self-checking: the bank account must close at nil and every capital account must close. If they do not, look first at partners\' loans, reserves and expenses paid by a partner.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Dissolution of firm (s. 39) ends the business; dissolution of partnership only reconstitutes it.',
                        'Grounds: agreement (s. 40), compulsory (s. 41), contingencies (s. 42), notice — at will (s. 43), court (s. 44).',
                        'Section 48: losses from profits → capital → partners; assets to outsiders → partners\' advances → capital → surplus in profit ratio.',
                        'Realisation Account: assets (not cash) and outside liabilities at book value; actual realisations and payments; balance in profit ratio.',
                        'Garner v. Murray: realisation loss in profit ratio (solvent partners bring cash); insolvency deficiency in capital ratio (before realisation loss).',
                        'Piecemeal: maximum loss (each instalment is final) or highest relative capital (pay excess capitals first).',
                        'LLP: wound up voluntarily or by the Tribunal (e.g. fewer than two partners for over six months, inability to pay debts, five years\' filing default).'],
            'remember': ['Partners\' loans, reserves and P&L balances do not go to Realisation.', 'Expenses paid by a partner: Realisation Dr, Partner\'s Capital Cr.', 'Section 51: no premium refund on death, own misconduct, or agreement without provision for refund.'],
            'traps': ["Don't share the insolvency deficiency in the profit ratio unless the deed says so.", "Don't use capitals after the realisation loss for Garner v. Murray.", "Don't stop the highest relative capital working after only one round."],
        },
        'quickref': [
            {'k': 's. 39 / 40 / 41', 'v': 'Dissolution of firm defined / by agreement / compulsory (insolvency of all or all but one; business unlawful)'},
            {'k': 's. 42 / 43 / 44', 'v': 'Contingencies (term, venture, death, insolvency) / notice in partnership at will / by court'},
            {'k': 's. 48', 'v': 'Outsiders → partners\' advances → capital → surplus in profit ratio'},
            {'k': 's. 51', 'v': 'Reasonable refund of premium on premature dissolution (none if dissolution is by death, mainly by his own misconduct, or under an agreement with no provision for refund)'},
            {'k': 'Garner v. Murray', 'v': 'Insolvency loss borne by solvent partners in capital ratio'},
            {'k': 'Max loss method', 'v': 'Each instalment = final; unsold assets = nil'},
            {'k': 'HRC method', 'v': 'Capital ÷ ratio → base → excess → pay largest relative excess first'},
            {'k': 'LLP winding up', 'v': 'Voluntary or by Tribunal (< 2 partners > 6 months; cannot pay debts; 5 years non-filing; just & equitable)'},
        ],
        'viva': viva, 'cases': kcase,
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'rows': [['land', 'dr', 60000], ['machinery|plant', 'dr', 45000], ['stock|inventory', 'dr', 27000], ['debtor|receivable', 'dr', 30000], ['creditor|payable', 'cr', 36000]]},
           's2': {'kw': ['89500|38000'], 'rows': [['kavi|land', 'cr', 72000]]},
           's3': {'rows': [['creditor|bank|cash', 'dr', 34200], ['repair|outstanding|unrecorded', 'dr', 1200], ['kavi|expense', 'dr', 1900]]},
           's4': {'rows': [['kavi|loss', 'cr', 1200], ['lata|loss', 'cr', 600]]},
           's5': {'kw': ['profit loss|p l|accumulated profit', 'loan'], 'min': 2, 'nums': [6000, 3000]},
           's6': {'nums': [9700, 47400]},
           's7': {'nums': [107500]}},
    'q2': {'extra_ok': False,
           's1': {'rows': [['mohan current', 'dr', 5000], ['mohan capital|mohan', 'cr', 5000], ['om capital|om', 'dr', 23000], ['om current', 'cr', 23000], ['naveen current', 'cr', 2000]]},
           's2': {'rows': [['mohan', 'dr', 12000], ['naveen', 'dr', 8000], ['om', 'dr', 4000], ['realisation|realization', 'cr', 24000]]},
           's3': {'kw': ['bank|cash'], 'rows': [['mohan', 'cr', 12000], ['naveen', 'cr', 8000]]},
           's4': {'rows': [['om', 'cr', 2000], ['om', 'cr', 5000]]},
           's5': {'kw': ['capital ratio|fixed capital|garner|3 2|60000 40000'], 'rows': [['mohan', 'dr', 3000], ['om', 'cr', 5000]],
                  'wrong': [{'kw': ['profit sharing ratio 3 2 1|3 2 1 deficiency|deficiency 3 2 1'], 'say': "Under Garner v. Murray the insolvent partner's deficiency is borne by solvent partners in their (fixed) capital ratio, not in the profit-sharing ratio."}]}},
    'q3': {'extra_ok': False,
           's1': {'nums': [15000, 10000, 11000]},
           's2': {'kw': ['r first|first r|r alone|excess 6000|nil 6000|6000 r first|r only'], 'nums': [6000]},
           's3': {'kw': ['4000 2000', '6000 3000', '6000 6000 3000'], 'min': 3},
           's4': {'kw': ['12000 12000 6000'], 'nums': [18000, 28000, 20000]}},
    'q4': {'extra_ok': False,
           's1': {'kw': ['section 48|sec 48|s 48|48']},
           's2': {'kw': ['loss|deficien', 'profit capital|out of profit|from profit|profits first|first profit', 'individual|personal|partners contribute|contributed by partners|contribution partners|partners bear|borne by partners'], 'min': 3},
           's3': {'kw': ['outsider|third part|outside liabilit|creditor|external|debts of firm|firm debts', 'loan|advance', 'capital', 'surplus|residue|remain|balance|residual'], 'min': 4,
                  'wrong': [{'kw': ['loans before outsiders|partners loans first|capital before loan|capital first'], 'say': "Outsiders are paid first, then partners' loans, then capital; only the residue is shared in the profit-sharing ratio."}]}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
