"""CA Foundation · Paper 1 Accounting · Chapter 6 Bills of Exchange and Promissory Notes (single unit).
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from datetime import date, timedelta
from calendar import monthrange
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch06-u01'


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year; m += 1
    return date(y, m, min(d.day, monthrange(y, m)[1]))


def ds(d): return f'{d.day} {d.strftime("%B")} {d.year}'


GRACE = timedelta(days=3)


def build():
    # ---------------- Illustration 1: due dates and maturity ----------------
    c1 = Checks()
    a_due = add_months(date(2027, 1, 14), 3); a_mat = a_due + GRACE
    b_due = add_months(date(2026, 11, 30), 3); b_mat = b_due + GRACE
    c_due = date(2026, 6, 10) + timedelta(days=60); c_mat = c_due + GRACE
    c1.add('20+31+9', 'Days counted for the 60-day bill: 20 left in June (11th-30th) + 31 in July + 9 in August')
    d_due = add_months(date(2026, 7, 9), 2); d_mat = d_due + GRACE
    e_due = add_months(date(2026, 7, 5), 2); e_mat = e_due + GRACE
    f_due = add_months(date(2026, 10, 23), 3); f_mat = f_due + GRACE
    f_hol = f_mat - timedelta(days=1); f_emg = f_mat + timedelta(days=1)
    c1.add('28+3', 'February 2027 has 28 days; expiry 28 February + 3 days of grace = 3 March')
    assert (a_mat, b_mat, c_mat, d_mat, e_mat, f_mat) == (date(2027, 4, 17), date(2027, 3, 3), date(2026, 8, 12), date(2026, 9, 12), date(2026, 9, 8), date(2027, 1, 26))
    due_tbl = table(['Bill', 'Term runs from', 'Expiry (due) date', 'Date of maturity'], [
        ['(a) Dated 14 January 2027, 3 months after date', 'Date of drawing', ds(a_due), ds(a_mat)],
        ['(b) Dated 30 November 2026, 3 months after date', 'Date of drawing; February has no 30th, so the last day of February is used', ds(b_due), ds(b_mat)],
        ['(c) Dated 10 June 2026, 60 days after date', 'Date of drawing (the date of the bill itself is excluded)', ds(c_due), ds(c_mat)],
        ['(d) Drawn 5 July 2026, accepted 9 July 2026, 2 months after sight', 'Date of acceptance (sight)', ds(d_due), ds(d_mat)],
        ['(e) Drawn 5 July 2026, accepted 9 July 2026, 2 months after date', 'Date of drawing (acceptance date is irrelevant)', ds(e_due), ds(e_mat)],
        ['(f) Dated 23 October 2026, 3 months after date', 'Date of drawing', ds(f_due), f'{ds(f_mat)} is Republic Day (public holiday), so the bill matures on the preceding business day, {ds(f_hol)}'],
        ['(g) Payable at sight / on demand', 'No term', 'Not applicable', 'Payable when presented; no days of grace'],
    ], title='Due dates and maturity dates')

    # ---------------- Illustration 2: discounting, dishonour, renewal (both books) ----------------
    c2 = Checks()
    disc = c2.add('240000*12/100*3/12', 'Discount charged by the bank: 12% p.a. for 3 months (4 Jan to 4 Apr) on 2,40,000')
    proceeds = c2.add('240000-7200', 'Amount credited by the bank')
    owed = c2.add('240000+400', 'Amount due from Prakash on dishonour (bill + noting charges)')
    paid_now = c2.add('400+40000', 'Cash paid by Prakash on 4 April (noting charges + part of the bill)')
    bal = c2.add('240400-40400', 'Balance carried into the new bill before interest')
    intr = c2.add('200000*15/100*2/12', 'Interest @15% p.a. for 2 months on 2,00,000')
    newbill = c2.add('200000+5000', 'Amount of the new bill')
    c2.add('40400+205000', 'Total credited to Prakash on 4 April (cash + new bill)')
    EN = [
        je('2027 Jan 1', [('Prakash', 240000)], [('Sales A/c', 240000)], 'Being goods sold on credit to Prakash'),
        je('Jan 1', [('Bills Receivable A/c', 240000)], [('Prakash', 240000)], "Being Prakash's 3-month acceptance received, maturing on 4 April 2027"),
        je('Jan 4', [('Bank A/c', proceeds), ('Discount on Bills A/c', disc)], [('Bills Receivable A/c', 240000)], 'Being the bill discounted with the bank at 12% p.a. for 3 months'),
        je('Apr 4', [('Prakash', owed)], [('Bank A/c', owed)], 'Being the discounted bill dishonoured; bank debited the bill amount and ₹400 noting charges'),
        je('Apr 4', [('Prakash', intr)], [('Interest A/c', intr)], 'Being interest @15% p.a. for 2 months on ₹2,00,000 charged for renewal'),
        je('Apr 4', [('Cash A/c', paid_now), ('Bills Receivable A/c', newbill)], [('Prakash', paid_now + newbill)], 'Being cash received and a new 2-month acceptance (bill + interest) received in renewal'),
        je('Jun 7', [('Bank A/c', newbill)], [('Bills Receivable A/c', newbill)], 'Being the renewed bill met on maturity'),
    ]
    EP = [
        je('2027 Jan 1', [('Purchases A/c', 240000)], [('Neel Traders', 240000)], 'Being goods bought on credit from Neel Traders'),
        je('Jan 1', [('Neel Traders', 240000)], [('Bills Payable A/c', 240000)], 'Being 3-month bill drawn by Neel Traders accepted'),
        je('Apr 4', [('Bills Payable A/c', 240000), ('Noting Charges A/c', 400)], [('Neel Traders', owed)], 'Being own acceptance dishonoured; noting charges payable to the drawer'),
        je('Apr 4', [('Interest A/c', intr)], [('Neel Traders', intr)], 'Being interest payable for the extension of 2 months'),
        je('Apr 4', [('Neel Traders', paid_now + newbill)], [('Cash A/c', paid_now), ('Bills Payable A/c', newbill)], 'Being cash paid and a new 2-month bill accepted for the balance with interest'),
        je('Jun 7', [('Bills Payable A/c', newbill)], [('Bank A/c', newbill)], 'Being the renewed bill paid on maturity'),
    ]
    LP = ledgers_from(EN, ['Prakash'], from_id='jn2', year_end='Jun 7', next_day='Jun 8')

    # ---------------- Illustration 3: bill for collection and retirement ----------------
    c3 = Checks()
    reb = c3.add('90000*10/100*2/12', 'Rebate @10% p.a. for the unexpired 2 months (4 July to 4 September)')
    cash_ret = c3.add('90000-1500', 'Cash paid by Sohan on retiring Bill B')
    ER = [
        je('2026 May 1', [('Bills Receivable A/c', 150000)], [('Sohan', 150000)], 'Being two acceptances received from Sohan: Bill A ₹60,000 (3 months) and Bill B ₹90,000 (4 months)'),
        je('May 10', [('Bills for Collection A/c', 60000)], [('Bills Receivable A/c', 60000)], 'Being Bill A sent to the bank for collection on maturity'),
        je('Jul 4', [('Bank A/c', cash_ret), ('Rebate on Bills A/c', reb)], [('Bills Receivable A/c', 90000)], 'Being Bill B retired by Sohan two months before maturity under rebate @10% p.a.'),
        je('Aug 4', [('Bank A/c', 60000)], [('Bills for Collection A/c', 60000)], 'Being Bill A collected by the bank on maturity'),
    ]
    ES = [
        je('2026 May 1', [('Ritu', 150000)], [('Bills Payable A/c', 150000)], 'Being two bills drawn by Ritu accepted'),
        je('Jul 4', [('Bills Payable A/c', 90000)], [('Bank A/c', cash_ret), ('Rebate on Bills A/c', reb)], 'Being Bill B retired two months early; rebate @10% p.a. earned'),
        je('Aug 4', [('Bills Payable A/c', 60000)], [('Bank A/c', 60000)], 'Being Bill A paid on maturity'),
    ]

    # ---------------- Illustration 4: accommodation bill with insolvency ----------------
    c4 = Checks()
    a_disc = c4.add('120000-117000', 'Discount charged by the bank')
    a_half = c4.add('117000/2', "Bimal's half share of the proceeds")
    a_dh = c4.add('3000/2', "Bimal's half share of the discount")
    a_net = c4.add('120000-60000', 'Amount Asha owes Bimal after he meets the bill')
    a_rec = c4.add('60000*40/100', 'Recovered from Asha\'s estate (40 paise in the rupee)')
    a_bad = c4.add('60000-24000', 'Irrecoverable balance')
    EA = [
        je('2026 Jun 1', [('Bills Receivable A/c', 120000)], [('Bimal', 120000)], "Being Bimal's acceptance received for mutual accommodation"),
        je('Jun 1', [('Bank A/c', 117000), ('Discount on Bills A/c', a_disc)], [('Bills Receivable A/c', 120000)], 'Being the bill discounted with the bank'),
        je('Jun 1', [('Bimal', a_half + a_dh)], [('Bank A/c', a_half), ('Discount on Bills A/c', a_dh)], "Being half the proceeds remitted to Bimal and half the discount charged to him"),
        je('Sep 4', [('Bimal', a_net)], [('Bank A/c', a_rec), ('Deficiency A/c', a_bad)], "Being 40% of the amount due to Bimal paid by the official assignee; the unpaid 60% credited to Deficiency Account"),
    ]
    EB = [
        je('2026 Jun 1', [('Asha', 120000)], [('Bills Payable A/c', 120000)], 'Being bill drawn by Asha accepted for mutual accommodation'),
        je('Jun 1', [('Bank A/c', a_half), ('Discount on Bills A/c', a_dh)], [('Asha', a_half + a_dh)], 'Being half the proceeds received; half the discount borne'),
        je('Sep 4', [('Bills Payable A/c', 120000)], [('Bank A/c', 120000)], 'Being own acceptance met on maturity'),
        je('Sep 4', [('Bank A/c', a_rec), ('Bad Debts A/c', a_bad)], [('Asha', a_net)], "Being 40 paise in the rupee received from Asha's estate; the balance written off"),
    ]

    # ---------------- Question 1 (Lalit's books) ----------------
    q1c = Checks()
    q_dr = q1c.add('152000-150000', 'Discount received from Nikhil on endorsement in full settlement')
    q_owed = q1c.add('150000+300', 'Due from Mohan on dishonour')
    q_int = q1c.add('120000*12/100*3/12', 'Interest @12% p.a. for 3 months on 1,20,000')
    q_new = q1c.add('120000+3600', 'New bill')
    q_cash = q1c.add('300+30000', 'Cash paid by Mohan on renewal')
    q_rec = q1c.add('123600*60/100', 'Recovered at 60 paise in the rupee')
    q_bad = q1c.add('123600-74160', 'Bad debt written off')
    Q1 = [
        je('2026 Aug 1', [('Mohan', 150000)], [('Sales A/c', 150000)], 'Being goods sold to Mohan on credit'),
        je('Aug 1', [('Bills Receivable A/c', 150000)], [('Mohan', 150000)], "Being Mohan's 3-month acceptance received (maturity 4 November 2026)"),
        je('Aug 5', [('Nikhil', 152000)], [('Bills Receivable A/c', 150000), ('Discount Received A/c', q_dr)], "Being Mohan's acceptance endorsed to Nikhil in full settlement of ₹1,52,000"),
        je('Nov 4', [('Mohan', q_owed)], [('Nikhil', q_owed)], 'Being the endorsed bill dishonoured; Nikhil paid ₹300 noting charges'),
        je('Nov 4', [('Nikhil', q_owed)], [('Bank A/c', q_owed)], 'Being Nikhil paid by cheque for the dishonoured bill and noting charges'),
        je('Nov 4', [('Mohan', q_int)], [('Interest A/c', q_int)], 'Being interest @12% p.a. for 3 months on ₹1,20,000 charged for renewal'),
        je('Nov 4', [('Cash A/c', q_cash), ('Bills Receivable A/c', q_new)], [('Mohan', q_cash + q_new)], 'Being cash and a new 3-month acceptance received from Mohan'),
        je('2027 Feb 7', [('Mohan', q_new)], [('Bills Receivable A/c', q_new)], "Being Mohan's renewed acceptance dishonoured on his insolvency"),
        je('Feb 7', [('Bank A/c', q_rec), ('Bad Debts A/c', q_bad)], [('Mohan', q_new)], 'Being 60 paise in the rupee received from his estate and the balance written off'),
    ]

    # ---------------- Question 4 (accommodation, both books) ----------------
    q4c = Checks()
    g_prc = q4c.add('78000/4', "Gita's one-fourth share of the proceeds")
    g_dsc = q4c.add('2000/4', "Gita's one-fourth share of the discount")
    g_due = q4c.add('80000-19500-500', 'Farhan owes Gita on maturity')
    Q4F = [
        je('2026 Sep 1', [('Bills Receivable A/c', 80000)], [('Gita', 80000)], "Being Gita's accommodation acceptance received"),
        je('Sep 1', [('Bank A/c', 78000), ('Discount on Bills A/c', 2000)], [('Bills Receivable A/c', 80000)], 'Being the bill discounted'),
        je('Sep 1', [('Gita', g_prc + g_dsc)], [('Bank A/c', g_prc), ('Discount on Bills A/c', g_dsc)], 'Being one-fourth of the proceeds remitted to Gita and one-fourth of the discount charged to her'),
        je('Dec 4', [('Gita', g_due)], [('Bank A/c', g_due)], 'Being amount remitted to Gita to meet the bill'),
    ]
    Q4G = [
        je('2026 Sep 1', [('Farhan', 80000)], [('Bills Payable A/c', 80000)], 'Being accommodation bill accepted'),
        je('Sep 1', [('Bank A/c', g_prc), ('Discount on Bills A/c', g_dsc)], [('Farhan', g_prc + g_dsc)], 'Being one-fourth of the proceeds received, bearing one-fourth of the discount'),
        je('Dec 4', [('Bank A/c', g_due)], [('Farhan', g_due)], "Being Farhan's remittance received"),
        je('Dec 4', [('Bills Payable A/c', 80000)], [('Bank A/c', 80000)], 'Being own acceptance met on maturity'),
    ]

    # ---------------- Question 3 (due dates) ----------------
    q3 = [(date(2026, 4, 18), 3, 'months after date'), (date(2026, 8, 31), 6, 'months after date'), (date(2026, 9, 20), 45, 'days after date')]
    q3a = add_months(*q3[0][:2]) + GRACE; q3b = add_months(*q3[1][:2]) + GRACE; q3c_ = q3[2][0] + timedelta(days=45) + GRACE
    q3d = add_months(date(2026, 12, 2), 1) + GRACE
    q3e = add_months(date(2026, 5, 29), 2) + GRACE
    assert (q3a, q3b, q3c_, q3d, q3e) == (date(2026, 7, 21), date(2027, 3, 3), date(2026, 11, 7), date(2027, 1, 5), date(2026, 8, 1))
    q3ck = Checks()
    q3ck.add('10+31+4', '45 days after 20 September: 10 left in September + 31 in October + 4 in November = 45 → 4 November, +3 days = 7 November')
    q3tbl = table(['Bill', 'Working', 'Date of maturity'], [
        ['(i) Dated 18 April 2026, 3 months after date', 'Expires 18 July; add 3 days of grace', ds(q3a)],
        ['(ii) Dated 31 August 2026, 6 months after date', 'February 2027 has no 31st, so it expires on 28 February; add 3 days', ds(q3b)],
        ['(iii) Dated 20 September 2026, 45 days after date', 'Exclude 20 September: 10 + 31 + 4 = 45, so it expires on 4 November; add 3 days', ds(q3c_)],
        ['(iv) Drawn 25 November 2026, accepted 2 December 2026, 1 month after sight', 'Term runs from acceptance: expires 2 January 2027; add 3 days', ds(q3d)],
        ['(v) Drawn 29 May 2026, accepted 1 June 2026, 2 months after date', 'Term runs from drawing: expires 29 July; add 3 days', ds(q3e)],
    ])

    # ---------------- MCQ numbers ----------------
    mc = Checks()
    m_reb = mc.add('180000*12/100*2/12', 'rebate')
    m_prc = mc.add('75000-75000*16/100*3/12', 'proceeds')
    m_acc = mc.add('6000*1/4', "drawee's share of discount")
    m_ren = mc.add('80000+80000*12/100*3/12', 'renewed bill')

    # ---------------- Case set ----------------
    kc = Checks()
    k_disc = kc.add('300000*10/100*3/12', 'discount')
    k_prc = kc.add('300000-7500', 'proceeds')
    k_dh = kc.add('300000+600', 'debited on dishonour')
    k_int = kc.add('150000*12/100*2/12', 'interest')
    k_new = kc.add('150000+3000', 'new bill')
    cases = [{
        'id': 'k1', 'title': 'Om Electricals — a bill that went wrong', 'difficulty': 'hard',
        'case': ('On 1 October 2026 Om Electricals sold goods for ₹3,00,000 to Varun and drew on him a bill for 3 months, which Varun accepted the same day. On 4 October '
                 'Om Electricals discounted the bill with its bank at 10% per annum. On the date of maturity the bill was dishonoured and the bank paid noting charges of ₹600. '
                 'Varun then paid ₹1,50,600 in cash and, for the balance, accepted a new bill for 2 months carrying interest at 12% per annum, included in the bill.'),
        'mcqs': [
            M('k1a', 'On what date does the original bill mature?', ['4 January 2027', '1 January 2027', '4 October 2026', '7 January 2027'], 0,
              'Three months after 1 October is 1 January 2027; adding three days of grace gives 4 January 2027.', 'moderate'),
            M('k1b', 'How much does the bank credit to Om Electricals on 4 October?', [R(k_prc), R(300000), '₹2,70,000', '₹2,92,000'], 0,
              f'Discount = 3,00,000 × 10% × 3/12 = {R(k_disc)}; proceeds = {R(k_prc)}. The bank charges for the 3 months up to maturity.', 'moderate', '300000-300000*10/100*3/12'),
            M('k1c', 'On dishonour, what entry does Om Electricals pass?', [f'Varun Dr. {R(k_dh)} To Bank A/c {R(k_dh)}', f'Varun Dr. {R(k_dh)} To Bills Receivable A/c {R(k_dh)}', 'Bank A/c Dr. ₹3,00,600 To Varun ₹3,00,600', 'Varun Dr. ₹3,00,000 To Bank A/c ₹3,00,000'], 0,
              'The bill was discounted, so the bank recovers the bill amount and the noting charges from Om Electricals; Varun becomes liable for both. Bills Receivable is not credited — it was already closed on discounting.'),
            M('k1d', 'What is the amount of the new bill?', [R(k_new), R(150000), '₹1,53,600', '₹1,50,600'], 0,
              f'Cash ₹1,50,600 covers the noting charges ₹600 and ₹1,50,000 of the bill. Balance ₹1,50,000 + interest at 12% for 2 months {R(k_int)} = {R(k_new)}.', 'hard', '150000+150000*12/100*2/12'),
        ]}]

    viva = [
        V('v1', 'How does a bill of exchange differ from a promissory note?',
          'A bill of exchange contains an order to pay, while a promissory note contains a promise to pay. A bill is drawn by the creditor and normally has three parties: drawer, drawee and payee. A promissory note is made by the debtor and has only two parties, the maker and the payee. A bill must be accepted by the drawee, but a promissory note does not need acceptance. A promissory note cannot be made payable to bearer.',
          [P('p1', 'Bill = order to pay; promissory note = promise to pay', 4, ALT('bill {x} order', 'order bill', 'bill order', x=['contains an', 'is an', 'has an', 'gives an', 'an']), 'note promise|promissory promise|promise note|note contains a promise|note is a promise|note has a promise'),
           P('p2', 'Bill has three parties (drawer, drawee, payee); note has two (maker, payee)', 3, 'three part|3 part|three parties|3 parties|drawer drawee payee|drawer drawee and payee', 'two part|2 part|two parties|2 parties|only two|maker and payee|maker payee', min=1),
           P('p3', 'Bill needs acceptance; promissory note needs no acceptance', 2, 'not need accept|no accept|not require accept|without accept|not accepted|need not be accepted|needn t be accepted|doesn t need accept|doesn t require accept|accept not need|accept not requir|acceptance is not needed|acceptance is not required'),
           P('p4', 'A promissory note cannot be payable to bearer', 1, 'cannot bearer|not bearer|can t bearer|cant bearer|never bearer|no bearer|cannot be made payable to bearer|cannot be payable to bearer|not payable to bearer')], 'c2'),
        V('v2', 'What are days of grace, and how do you find the date of maturity of a bill?',
          'Days of grace are three extra days allowed to the acceptor. The due date is found from the term of the bill, and three days of grace are added to it to get the date of maturity. Days of grace are not added for a bill payable on demand or at sight. If the date of maturity is a public holiday, the bill matures on the preceding business day.',
          [P('p1', 'Three days of grace added to the due date gives the date of maturity', 5, 'three day|3 day', 'add|plus|after|extra', 'maturity|mature', min=2),
           P('p2', 'No days of grace for bills payable on demand / at sight', 3, 'not for|no grace|not added|not allowed|not given|no days of grace|without grace|not apply|don t get|do not get|not available', 'demand|sight|presentment', min=2),
           P('p3', 'Public holiday: matures on the preceding business day', 2, 'holiday', 'preceding|previous|day before|earlier|prior', min=2)], 'c4'),
        V('v3', 'A trader has received an accepted bill. What can he do with it, and what entry is passed in each case?',
          'He has three options. He can hold the bill till maturity and collect the money, passing Bank Account debit and Bills Receivable credit on payment. He can endorse it to a creditor, debiting the creditor and crediting Bills Receivable. Or he can discount it with a bank, debiting Bank with the proceeds and Discount Account with the discount, and crediting Bills Receivable.',
          [P('p1', 'Hold till maturity — Bank Dr, To Bills Receivable on payment', 3, 'hold|keep|retain|wait', 'maturity|due date|until it matures|till it matures', min=2),
           P('p2', 'Endorse to a creditor — Creditor Dr, To Bills Receivable', 3, 'endors|transfer|pass it on|pass on|hand it over', 'creditor|supplier|another party|third party|someone', min=1),
           P('p3', 'Discount with a bank — Bank Dr (proceeds), Discount Dr, To Bills Receivable', 4, 'discount', 'bank', min=2)], 'c3'),
        V('v4', 'What are noting charges, and who finally bears them?',
          'Noting charges are the fee paid to a notary public for recording the fact and reason of dishonour of a bill. They are paid by the holder, but they are recoverable from the drawee or acceptor who caused the dishonour, so in the drawer\'s books the drawee\'s account is debited with the bill amount plus noting charges.',
          [P('p1', 'Fee paid to a notary public for noting / recording the dishonour', 5, 'notary|notar|official|noting charges notary|noting charges are paid to the notary|noting notary', 'dishonour|dishonor|not paid|non payment|refus', min=2),
           P('p2', 'Recoverable from the drawee / acceptor who caused the dishonour', 5, ALT('{v} {r}', '{r} {w}', v=['recover', 'recoverable', 'borne by', 'charged to', 'debited to', 'paid by', 'collected from', 'claimed from', 'bear by'], r=['drawee', 'acceptor', 'debtor', 'customer'], w=['liable', 'bears', 'bear', 'pays', 'responsible', 'account debited', 'is debited', 'has to pay']))], 'c5'),
        V('v5', 'When an acceptor retires a bill before maturity, how is the rebate treated in the books of the two parties?',
          'Retiring a bill means paying it before its maturity date. The holder allows a rebate, calculated at the agreed rate for the unexpired period from the date of payment to the date of maturity. So the rebate is an income for the acceptor, credited in his books, and an expense for the drawer or holder, debited to Rebate on Bills Account.',
          [P('p1', 'Retirement = payment before maturity', 2, 'before maturity|before due|early|premature|before the due date|before it matures|ahead'),
           P('p2', 'Rebate calculated for the unexpired period (payment date to maturity)', 2, 'unexpired|remaining|left|balance period|till maturity|to maturity|up to maturity|until maturity'),
           P('p3', 'Rebate is income (credit) for the acceptor/drawee and an expense (debit) for the drawer/holder', 6,
             ALT('{a} {i} {d} {e}', '{i} {a} {e} {d}', '{d} {e} {a} {i}', '{e} {d} {i} {a}', '{a} s {i} {d} s {e}', '{d} s {e} {a} s {i}', a=['acceptor', 'drawee'], i=['income', 'gain', 'credit'], d=['drawer', 'holder'], e=['expense', 'loss', 'debit']))
          ], 'c7'),
        V('v6', 'What is an accommodation bill, and how is the discount shared?',
          'An accommodation bill is drawn and accepted only to help one or both parties raise funds, not for any trade transaction. The bill is discounted with a bank and the proceeds are shared as agreed. The discount is borne by the parties in the same ratio in which they share the proceeds, and on maturity each party sends the acceptor his share so the bill can be met.',
          [P('p1', 'Drawn to raise funds / financial help, not for a trade transaction', 4, 'fund|financ|money|cash|help|accommodat', 'no trade|not trade|not for trade|without trade|no sale|not for goods|no goods|no transaction|not for a trade|not for any trade|not because of trade|without sale|without any sale|not for sale|without goods|without any trade|not backed by trade|not related to trade|no actual trade|not arising from trade|no real trade|no underlying', min=2),
           P('p2', 'Discount shared in the ratio in which proceeds are shared', 4, 'discount', 'ratio|proportion|same share|share', 'proceeds|proceed|amount received|money received|share the money|money raised', min=3),
           P('p3', 'On maturity the other party remits his share to the acceptor', 2, 'maturity|due date', 'remit|send|pay|give', min=2)], 'c9'),
        V('v7', 'How is the insolvency of an acceptor recorded in the books of the drawer and the drawee?',
          'In the drawer\'s books the acceptance is first treated as dishonoured, so the drawee\'s account is debited. Whatever is received from his estate is debited to Bank, and the unrecovered amount is written off as bad debts. In his own books the insolvent drawee credits Deficiency Account with the amount he is unable to pay.',
          [P('p1', 'Drawer: first record dishonour (drawee debited)', 3, 'dishonour|dishonor|not met|unpaid'),
           P('p2', 'Drawer: amount received from the estate debited to Bank/Cash', 2, 'estate|official assignee|receiver|recover|received'),
           P('p3', 'Drawer: unrecovered balance written off as bad debts', 3, 'balance bad debt|rest bad debt|remaining bad debt|unrecovered bad debt|irrecoverable bad debt|balance written off|rest written off|remaining written off|unrecovered written off|unrecovered amount is written off|irrecoverable written off'),
           P('p4', "Drawee: unpaid amount credited to Deficiency Account", 2, 'insolvent credit deficiency|insolvent credits deficiency|insolvent deficiency|insolvent book deficiency|insolvent s book deficiency|insolvent book go deficiency|acceptor credit deficiency|acceptor deficiency|acceptor book deficiency|debtor credit deficiency|debtor book deficiency')], 'c8'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch06', 'n': 1,
        'title': 'Bills of Exchange and Promissory Notes',
        'outcomes': [
            'Explain what a bill of exchange and a promissory note are, list their essential features and parties, and tell the two apart.',
            'Work out the due date and the date of maturity of any bill — after date, after sight, in months or days, at month-end and on holidays.',
            'Journalise drawing, acceptance, holding, endorsement, discounting, collection, honour and dishonour (with noting charges) in the books of the drawer, drawee and endorsee.',
            'Record renewal with interest, retirement under rebate, and insolvency of the acceptor in both sets of books.',
            'Account for accommodation bills, sharing proceeds and discount correctly, and describe bills receivable and bills payable books.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 70}, 'prereq': ['fnd-p1-ch02-u01'],
                 'exam_tip': 'Examiners ask for entries "in the books of" a named party — read that line twice. Draw a quick time-line of dates (drawing, discounting, maturity) before you journalise; most lost marks come from wrong maturity dates and from debiting the wrong account on dishonour.'},
        'concepts': [
            {'id': 'c1', 'title': 'Bill of exchange: a written order to pay',
             'body': ['A bill of exchange is a signed, written instrument in which one person (the drawer, usually the seller) orders another (the drawee, usually the buyer) to pay a fixed sum of money to a named person, to his order, or to the bearer. Once the drawee signs his acceptance on it, he becomes the acceptor and the bill becomes a binding credit instrument.',
                      'Essentials: it is in writing and dated; it contains an order (not a request) to pay; the order is unconditional; the amount is certain and in the legal currency of the country; the payee is certain; it is accepted by the drawee; and it carries the stamp duty required (bills payable on demand are an exception).',
                      'Parties: drawer (makes the order), drawee/acceptor (who must pay), payee (who receives the money — often the drawer himself). A holder can transfer the bill by endorsement; the acceptor is primarily liable, and if he fails, the holder can claim from the drawer and earlier endorsers.',
                      'Foreign bill: under Section 12 of the Negotiable Instruments Act, any instrument that is not an inland instrument is foreign — for example, a bill drawn in India on a person abroad and payable abroad. Foreign bills are usually drawn in a set of three copies sent separately; once one copy is paid the others are of no use.'],
             'analogy': 'A bill is like a written IOU that the seller writes and the buyer signs — "Pay ₹50,000 in three months" — which the seller can then sell to a bank or pass on to his own supplier like money.',
             'work': 'Exporters still draw bills on foreign buyers, and banks finance them. Treasury and accounts teams track every bill receivable by maturity date so that cash planning and follow-up of dues are on time.'},
            {'id': 'c2', 'title': 'Promissory note and how it differs from a bill',
             'body': ['A promissory note is a signed written instrument (not a bank note or currency note) in which the maker unconditionally promises to pay a fixed amount of money to a named person or as that person directs. Section 31(2) of the RBI Act forbids anyone other than the authorities named there from issuing a promissory note payable to bearer.',
                      'Essentials: written; a clear promise (merely admitting a debt is not enough); unconditional ("I will pay when I can" fails); signed by a definite maker to a definite payee; certain amount in legal currency; properly stamped; no acceptance needed.'],
             'blocks': [table(['Basis', 'Bill of exchange', 'Promissory note'], [
                 ['Nature', 'Order to pay', 'Promise to pay'],
                 ['Parties', 'Usually three — drawer, drawee, payee', 'Two — maker and payee'],
                 ['Who prepares it', 'The creditor draws it', 'The debtor makes it'],
                 ['Who pays', 'The acceptor', 'The maker'],
                 ['Drawer / maker as payee', 'Drawer and payee can be the same person', 'Maker and payee cannot be the same person'],
                 ['Liability of the person who prepares it', "Drawer's liability is secondary — only if the acceptor fails", "Maker's liability is primary and absolute"],
                 ['Acceptance', 'Required; may even be conditional', 'Not required; cannot be conditional'],
                 ['On dishonour', 'Notice of dishonour needed; noting and protest required', 'No notice of dishonour; no noting or protest needed'],
             ], title='Bill of exchange vs promissory note')],
             'analogy': 'Bill: "I tell you to pay." Note: "I promise I will pay." The first needs the other person to say yes (accept); the second needs only your own signature.',
             'work': 'Lenders often take a demand promissory note from a borrower as extra security. When you audit loans given, you check that such notes exist, are signed by the borrower and are properly stamped.'},
            {'id': 'c3', 'title': 'Recording bills: Bills Receivable and Bills Payable',
             'body': ['The party who receives an accepted bill (or a promissory note) records a new asset — Bills Receivable: Bills Receivable A/c Dr, To Drawee (customer). The party who accepts a bill (or makes a note) records a new liability — Bills Payable: Creditor A/c Dr, To Bills Payable A/c. The bill does not create a new sale or purchase; it only converts a book debt into a written one.',
                      'The holder of a bill receivable has three choices: (1) hold it till maturity — on payment, Bank Dr, To Bills Receivable; (2) endorse it to a creditor — Creditor Dr, To Bills Receivable; (3) discount it with a bank — Bank Dr (net proceeds), Discount on Bills Dr (bank\'s charge), To Bills Receivable.',
                      'On maturity, if the bill is honoured, only the person holding it at that time records receipt. If the drawer had endorsed or discounted it, he passes no entry when it is met. The acceptor always passes: Bills Payable Dr, To Bank.'],
             'analogy': 'Converting a debtor into a bill receivable is like turning a verbal promise into a signed cheque-like paper — the amount is the same, but now it can be sold (discounted) or handed over (endorsed).',
             'work': 'In practice, bank statements show "bills discounted" and "bills returned unpaid". Matching these with the bills register is a routine month-end task in a distributor\'s accounts department.'},
            {'id': 'c4', 'title': 'Term, due date, days of grace and maturity',
             'body': ['Term: the period for which the bill runs (usually up to about 90 days). For a bill "after date" the term starts from the date of drawing; for a bill "after sight" it starts from the date of acceptance (sight).',
                      'Due date (expiry): the day the term ends. Months: the same date in the later month; if that month has no such date, its last day (a bill dated 31 August for 6 months expires on 28 February in a non-leap year). Days: count forward excluding the date of the bill.',
                      'Days of grace: every instrument not payable on demand gets three days of grace. Date of maturity = due date + 3 days. No grace is added for bills payable on demand, at sight or on presentment — these are payable whenever presented. A cheque is always payable on demand and so can never be a time instrument.',
                      'Holidays: if the date of maturity is a public holiday, the bill matures on the preceding business day; if it is an emergency (unforeseen) holiday declared later, the next following business day. In exam questions treat a date as a holiday only when the question says so — weekdays are normally ignored, although strictly Section 25 of the Negotiable Instruments Act counts Sundays as public holidays.'],
             'blocks': [due_tbl],
             'analogy': 'Think of a library book: the due date is stamped inside, but the library lets you return it up to three days late without a fine. Those three days are the days of grace.',
             'work': 'Wrong maturity dates lead to wrong discount, interest and rebate figures. Trade-finance desks and accounts teams keep a maturity diary so that bills are presented on time — missing presentment can weaken the right to recover.'},
            {'id': 'c5', 'title': 'Dishonour and noting charges',
             'body': ['A bill is dishonoured when the acceptor fails to pay on maturity. The bill becomes worthless as an asset, and the acceptor again owes the amount plus any expenses.',
                      'Noting: to prove dishonour, the holder gets a notary public to present the bill again and record (note) the fact and reason of dishonour. The notary\'s fee is noting charges, paid by the holder but recoverable from the party responsible for the dishonour — ultimately the acceptor.',
                      'Drawer\'s entry depends on where the bill is: still held — Drawee Dr (bill + noting), To Bills Receivable and To Bank (noting paid); endorsed — Drawee Dr, To Endorsee (who claims from the drawer); discounted — Drawee Dr, To Bank (the bank debits the drawer). Acceptor\'s entry: Bills Payable Dr, Noting Charges Dr, To Drawer.'],
             'analogy': 'If a cheque you deposit bounces, your bank reverses the credit and charges you; you then chase the person who gave it to you for the amount plus the charges. Dishonour of a discounted bill works the same way.',
             'work': 'When a customer\'s bill is returned unpaid, accounts must reverse the receipt, recover noting charges and alert the credit team. Auditors check that dishonoured bills are not still shown as bills receivable.'},
            {'id': 'c6', 'title': 'Renewal of a bill',
             'body': ['When the acceptor cannot pay on maturity, he may request more time and agree to pay interest for the extension. The old bill is cancelled (recorded exactly like a dishonour) and a new bill is drawn and accepted.',
                      'Amount of the new bill: (i) if nothing is paid — old amount + interest; (ii) if interest is paid in cash — old amount only; (iii) if part of the amount (and/or interest) is paid — the unpaid amount plus interest on that unpaid amount for the extended period.',
                      'Interest for renewal: Drawer — Drawee Dr, To Interest; Acceptor — Interest Dr, To Drawer.'],
             'analogy': 'Renewal is like rolling over a fixed-term loan: you close the old contract, add interest for the extra time, and sign a fresh one.',
             'work': 'Frequent renewals by the same customer are an early-warning sign of credit stress. A CA reviewing receivables flags them for provisioning discussion with management.'},
            {'id': 'c7', 'title': 'Retirement of a bill under rebate',
             'body': ['Retiring a bill means the acceptor pays it before the date of maturity. The holder allows a rebate (discount) for the unexpired period — from the date of payment to the date of maturity — at the agreed rate.',
                      'Rebate = Amount of bill × rate × unexpired period. For the drawer/holder the rebate is an expense: Bank Dr, Rebate on Bills Dr, To Bills Receivable. For the acceptor it is an income: Bills Payable Dr, To Bank, To Rebate on Bills.',
                      'Do not confuse retirement (paying early, earning rebate) with renewal (paying late, bearing interest).'],
             'analogy': 'Paying your credit card bill before the statement date and getting cash-back for it — early payment earns you a small reward.',
             'work': 'Businesses with surplus cash compare the rebate offered with what the money would earn elsewhere. If the rebate rate beats the bank deposit rate, retiring bills early is a sensible treasury decision.'},
            {'id': 'c8', 'title': 'Insolvency of the acceptor',
             'body': ['If the acceptor becomes insolvent, his acceptance will not be met, so the holder records the dishonour at once (it need not wait for maturity in exams if insolvency is announced). Later, whatever the official assignee pays from the estate is debited to Bank, and the unrecovered balance is written off as Bad Debts.',
                      'Work out the amount due from the insolvent first (including any noting charges or interest debited to him), then apply the rate — "40 paise in the rupee" means 40% of the amount due.',
                      'In the insolvent acceptor\'s books, the amount he cannot pay is credited to Deficiency Account (the creditor is debited with the full amount, Bank credited with what is paid).'],
             'analogy': 'If a friend who owes you ₹1,000 goes bankrupt and the court pays creditors 40 paise per rupee, you get ₹400 and must accept that ₹600 is lost.',
             'work': 'When a customer is admitted into insolvency proceedings, the finance team files its claim, stops further credit, and the auditor checks whether the receivable has been written off or provided for.'},
            {'id': 'c9', 'title': 'Accommodation bills',
             'body': ['An accommodation bill is drawn and accepted without any trade transaction behind it, only to raise funds for one or both parties. The drawer discounts the accepted bill with his bank and uses the money; before maturity he sends the acceptor the amount so the bill can be met.',
                      'When both parties need money, the proceeds are shared in an agreed ratio and the discount is borne in the same ratio. Entries are the ordinary bill entries plus: remitting the other party\'s share of proceeds and charging him his share of discount; and the remittance on maturity.',
                      'If one party becomes insolvent, the other must bear the loss: the solvent party writes off the unrecovered amount as bad debts; the insolvent party credits the unpaid amount to Deficiency Account.'],
             'analogy': 'Two friends each need a short loan. One signs a paper promising to pay; the other takes it to a moneylender, gets cash and splits it. Both share the moneylender\'s fee in the same ratio as they shared the cash.',
             'work': 'Accommodation paper between related parties can be used to window-dress liquidity. Auditors look for bills with no matching sales invoice and for circular bills between group concerns.'},
            {'id': 'c10', 'title': 'Bills sent for collection; bills receivable and payable books',
             'body': ['Bill for collection: the holder hands the bill to his bank only for safe custody and collection on maturity — not for discounting. The bank credits the account only when it collects. Entries: Bills for Collection Dr, To Bills Receivable; on collection Bank Dr, To Bills for Collection; on dishonour Drawee Dr, To Bills for Collection.',
                      'Where bills are many, a Bills Receivable Book and a Bills Payable Book are kept as subsidiary day books. They record each bill\'s date, party, term, due date, place of payment, amount and how it was disposed of (held, endorsed, discounted, collected). Personal accounts are posted individually; periodic totals go to the Bills Receivable and Bills Payable accounts.'],
             'analogy': 'Sending a bill for collection is like giving a parcel to a courier for delivery against payment — the courier pays you only after the customer pays it.',
             'work': 'A bills register is the first document an auditor asks for when testing bills receivable: bills in hand should agree with the ledger balance, and discounted bills not yet matured are disclosed as a contingent liability.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Finding due dates and dates of maturity', 'difficulty': 'core', 'minutes': 10,
             'q': 'Find the date of maturity of each bill: (a) dated 14 January 2027, payable 3 months after date; (b) dated 30 November 2026, payable 3 months after date; (c) dated 10 June 2026, payable 60 days after date; (d) drawn 5 July 2026 and accepted 9 July 2026, payable 2 months after sight; (e) the same bill payable 2 months after date; (f) dated 23 October 2026, payable 3 months after date; (g) a bill payable at sight.',
             'solution': [due_tbl, wn('Points to watch', f'In (c) the date of the bill is excluded: 20 days left in June + 31 in July + 9 in August = 60, so the bill expires on {ds(c_due)}. In (f), if the government had instead declared 26 January an emergency holiday at short notice, the bill would mature on the next business day, {ds(f_emg)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Discounting, dishonour and renewal — books of both parties', 'difficulty': 'hard', 'minutes': 20,
             'q': 'On 1 January 2027 Neel Traders sold goods for ₹2,40,000 to Prakash and drew on him a bill at 3 months, which he accepted. On 4 January Neel Traders discounted the bill with its bank at 12% p.a. On maturity the bill was dishonoured and the bank paid ₹400 as noting charges. On the same day Prakash paid ₹40,400 in cash and accepted a new bill at 2 months for the balance plus interest at 15% p.a. The new bill was met on maturity. Journalise in the books of Neel Traders and of Prakash, and show Prakash\'s account in the books of Neel Traders.',
             'solution': [journal(EN, 'Books of Neel Traders — Journal', 'jn2'), *LP, journal(EP, 'Books of Prakash — Journal', 'jp2'),
                          wn('Working notes', f'Maturity of first bill: 1 April + 3 days = 4 April 2027. Discount = 2,40,000 × 12% × 3/12 = {R(disc)}; proceeds {R(proceeds)}. On dishonour Prakash owes {R(owed)}. Cash {R(paid_now)} clears the noting charges and ₹40,000 of the bill, leaving {R(bal)}; interest {R(bal)} × 15% × 2/12 = {R(intr)}; new bill {R(newbill)}, maturing 4 June + 3 = 7 June 2027.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Bill sent for collection and a bill retired early', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Sohan owed Ritu ₹1,50,000. On 1 May 2026 Ritu drew two bills on him, which he accepted: Bill A for ₹60,000 at 3 months and Bill B for ₹90,000 at 4 months. On 10 May Ritu sent Bill A to her bank for collection; the bank collected it on maturity. On 4 July Sohan retired Bill B, Ritu allowing a rebate at 10% p.a. Journalise in the books of Ritu and Sohan.',
             'solution': [journal(ER, 'Books of Ritu — Journal', 'jr3'), journal(ES, 'Books of Sohan — Journal', 'js3'),
                          wn('Working notes', f'Bill A matures 1 August + 3 = 4 August 2026; Bill B matures 1 September + 3 = 4 September 2026. On 4 July, 2 months remain for Bill B: rebate = 90,000 × 10% × 2/12 = {R(reb)}; cash {R(cash_ret)}. Sending a bill for collection is not discounting — no discount arises and the bank credits Ritu only on 4 August.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Accommodation bill ending in insolvency', 'difficulty': 'hard', 'minutes': 15,
             'q': 'On 1 June 2026 Asha drew a 3-month bill for ₹1,20,000 on Bimal for their mutual accommodation; Bimal accepted it. Asha discounted it the same day for ₹1,17,000 and remitted half the proceeds to Bimal, the discount to be shared equally. Before maturity Asha became insolvent, so Bimal met the bill himself on maturity. Asha\'s estate paid 40 paise in the rupee on 4 September. Journalise in both books.',
             'solution': [journal(EA, 'Books of Asha — Journal', 'ja4'), journal(EB, 'Books of Bimal — Journal', 'jb4'),
                          wn('Working notes', f'Discount {R(a_disc)}; each bears {R(a_dh)}. Bimal receives {R(a_half)} cash and is charged {R(a_dh)} discount, so ₹60,000 of the bill is his own. He meets ₹1,20,000, so Asha owes him {R(a_net)}. Recovery 40% = {R(a_rec)}; loss {R(a_bad)} — bad debts for Bimal, deficiency for Asha.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'A discounted bill comes back unpaid', 'role': 'Accounts executive at a building-materials distributor',
             'situation': 'The bank statement shows a debit of ₹3,00,750 marked "bill returned unpaid — incl. charges ₹750" against a dealer\'s bill you had discounted last quarter. The dealer phones asking for a 60-day extension.',
             'steps': ['Pass the dishonour entry: Dealer Dr ₹3,00,750, To Bank ₹3,00,750 — the bank has already recovered the money from you.',
                       'Tell sales and credit control; stop further supplies on credit until the matter is settled.',
                       'If management agrees to renew, get a fresh acceptance for the agreed amount including interest for 60 days, and record the interest income.',
                       'Update the bills register: original bill marked "dishonoured/renewed", new bill entered with its maturity date.',
                       'At year end, judge whether a provision is needed if the dealer has a history of renewals.'],
             'takeaway': 'A discounted bill is not "money in the bank" until it is met — the drawer stays liable to the bank until maturity.',
             'think': 'Why do auditors want discounted but unmatured bills disclosed in the notes to accounts?',
             'answer': 'Because if any of them is dishonoured, the bank will recover the money from the business — a contingent liability that readers must know about.'},
            {'id': 'j2', 'title': 'Year-end verification of bills receivable', 'role': 'Articled assistant on a statutory audit',
             'situation': 'The client\'s ledger shows Bills Receivable of ₹8,40,000 at 31 March. You are asked to verify it.',
             'steps': ['Get the bills receivable book and list bills not disposed of at 31 March.',
                       'Physically inspect bills in hand; for bills with the bank for collection, obtain the bank\'s confirmation.',
                       'Check that bills discounted or endorsed have been removed from the balance and are listed for contingent-liability disclosure.',
                       'Look at April receipts: bills met after the year end support the balance; bills dishonoured in April may need a provision.',
                       'Recompute a sample of maturity dates and discount amounts.'],
             'takeaway': 'The bills register, physical bills, bank confirmations and post-year-end receipts together prove the balance.',
             'think': 'A bill for ₹50,000 sent for collection on 25 March is shown as "Bank" instead of "Bills Receivable" at 31 March. What is wrong?',
             'answer': 'A bill sent for collection is not cash until the bank collects it. Until then it remains an asset (Bills for Collection / Bills Receivable), not a bank balance.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'A bill dated 20 January 2027 is payable 3 months after date. Its date of maturity is:', 'options': ['23 April 2027', '20 April 2027', '22 April 2027', '23 May 2027'], 'answer': 0, 'explain': 'Three months after 20 January expires on 20 April; add 3 days of grace → 23 April 2027.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'A bill dated 15 February 2027 is payable 90 days after date. It matures on:', 'options': ['19 May 2027', '16 May 2027', '18 May 2027', '17 May 2027'], 'answer': 0, 'explain': 'Exclude 15 February: 13 (Feb) + 31 (Mar) + 30 (Apr) + 16 (May) = 90 → expires 16 May; + 3 days = 19 May 2027.', 'concept': 'c4', 'difficulty': 'moderate'},
            {'id': 'm3', 'q': 'A bill dated 31 October 2026 is drawn for 4 months after date. The date of maturity is:', 'options': ['3 March 2027', '28 February 2027', '3 February 2027', '4 March 2027'], 'answer': 0, 'explain': 'February 2027 has no 31st, so the bill expires on 28 February; adding 3 days gives 3 March 2027.', 'concept': 'c4', 'difficulty': 'moderate'},
            {'id': 'm4', 'q': 'A bill of ₹1,80,000 is retired 2 months before maturity under a rebate of 12% p.a. The rebate is:', 'options': [R(m_reb), '₹21,600', '₹1,800', '₹5,400'], 'answer': 0, 'check': '180000*12/100*2/12', 'explain': f'1,80,000 × 12% × 2/12 = {R(m_reb)}. Rebate is only for the unexpired period, not a full year (₹21,600).', 'concept': 'c7', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'A 4-month bill of ₹75,000 is discounted one month after drawing at 16% p.a. The bank pays:', 'options': [R(m_prc), '₹71,000', '₹63,000', '₹74,000'], 'answer': 0, 'check': '75000-75000*16/100*3/12', 'explain': f'Discount is for the remaining 3 months: 75,000 × 16% × 3/12 = ₹3,000; proceeds {R(m_prc)}. Charging for 4 months gives ₹71,000 (a common error).', 'concept': 'c3', 'difficulty': 'moderate'},
            {'id': 'm6', 'q': 'A bill discounted with the bank is dishonoured on maturity. In the drawer\'s books the entry is:', 'options': ['Drawee A/c Dr. To Bank A/c', 'Drawee A/c Dr. To Bills Receivable A/c', 'Bills Receivable A/c Dr. To Bank A/c', 'Bank A/c Dr. To Drawee A/c'], 'answer': 0, 'explain': 'Bills Receivable was closed on discounting. The bank recovers the amount from the drawer (credit Bank) and the drawee becomes liable again (debit Drawee).', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'As per Section 31(2) of the RBI Act, a promissory note made by a trader:', 'options': ['Cannot be made payable to bearer', 'Must be payable to bearer', 'Needs acceptance by the payee', 'Must be drawn in triplicate'], 'answer': 0, 'explain': 'Ordinary persons cannot issue promissory notes payable to bearer — that would compete with currency. A note needs no acceptance; triplicate sets are a feature of foreign bills.', 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'In the books of the acceptor, rebate received on retiring a bill is:', 'options': ['An income, credited to Rebate on Bills', 'An expense, debited to Rebate on Bills', 'Deducted from Purchases', 'Credited to Bills Payable'], 'answer': 0, 'explain': 'The acceptor pays less than the face value; the saving is his income. For the holder the same rebate is an expense.', 'concept': 'c7', 'difficulty': 'core'},
            {'id': 'm9', 'q': 'In the books of an insolvent acceptor, the part of a bill he is unable to pay is credited to:', 'options': ['Deficiency Account', 'Bad Debts Account', 'Bills Payable Account', 'Capital Account'], 'answer': 0, 'explain': 'Bad debts is used by the creditor (drawer). The insolvent debtor credits the unpaid portion to Deficiency Account.', 'concept': 'c8', 'difficulty': 'moderate'},
            {'id': 'm10', 'q': 'Days of grace are NOT added in the case of a bill:', 'options': ['Payable at sight', 'Payable 3 months after date', 'Payable 60 days after sight', 'Payable 2 months after acceptance'], 'answer': 0, 'explain': 'Bills payable on demand, at sight or on presentment have no days of grace. All time bills get three days.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm11', 'q': 'An accommodation bill of ₹2,00,000 is discounted for ₹1,94,000; the drawer and drawee share the proceeds 3 : 1. The drawee\'s share of discount is:', 'options': [R(m_acc), '₹3,000', '₹4,500', '₹6,000'], 'answer': 0, 'check': '6000*1/4', 'explain': f'Discount ₹6,000 is borne in the ratio of proceeds: drawee 1/4 = {R(m_acc)}; drawer ₹4,500.', 'concept': 'c9', 'difficulty': 'moderate'},
            {'id': 'm12', 'q': 'A ₹1,00,000 bill is renewed: the acceptor pays ₹20,000 in cash and accepts a new 3-month bill for the balance with interest at 12% p.a. The new bill is for:', 'options': [R(m_ren), '₹83,000', '₹80,000', '₹1,03,000'], 'answer': 0, 'check': '80000+80000*12/100*3/12', 'explain': f'Interest is charged only on the unpaid ₹80,000: 80,000 × 12% × 3/12 = ₹2,400 → {R(m_ren)}.', 'concept': 'c6', 'difficulty': 'moderate'},
            {'id': 'm13', 'q': 'A bill endorsed by A to his creditor C is dishonoured and C pays noting charges. In A\'s books the entry is:', 'options': ['Drawee A/c Dr. To C', 'C Dr. To Drawee A/c', 'Drawee A/c Dr. To Bills Receivable A/c', 'Bills Receivable A/c Dr. To C'], 'answer': 0, 'explain': 'C will claim the bill amount and noting charges from A (credit C), and A recovers them from the drawee (debit Drawee).', 'concept': 'c5', 'difficulty': 'moderate'},
            {'id': 'm14', 'q': 'A bill is sent to the bank "for collection". The entry is:', 'options': ['Bills for Collection A/c Dr. To Bills Receivable A/c', 'Bank A/c Dr. To Bills Receivable A/c', 'Bank A/c Dr. Discount A/c Dr. To Bills Receivable A/c', 'No entry until maturity'], 'answer': 0, 'explain': 'The bill leaves the drawer\'s hands but is not yet cash; it is transferred to Bills for Collection until the bank collects it.', 'concept': 'c10', 'difficulty': 'core'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'hard', 'pad': 'journal',
             'q': 'On 1 August 2026 Lalit sold goods to Mohan for ₹1,50,000 and drew on him a 3-month bill, which Mohan accepted. On 5 August Lalit endorsed the bill to his creditor Nikhil in full settlement of ₹1,52,000 due to him. On maturity the bill was dishonoured and Nikhil paid ₹300 as noting charges; Lalit settled Nikhil\'s claim by cheque. On the same day Mohan paid ₹30,300 in cash and accepted a new 3-month bill for the balance plus interest at 12% p.a. Before the new bill matured Mohan became insolvent and 60 paise in the rupee was received from his estate on its maturity date. Pass journal entries in the books of Lalit.',
             'model': [journal(Q1, 'Books of Lalit — Journal', 'jq1'),
                       wn('Working notes', f'First bill matures 4 November 2026. Cash ₹30,300 covers noting ₹300 + ₹30,000 of the bill; balance ₹1,20,000. Interest 1,20,000 × 12% × 3/12 = {R(q_int)}; new bill {R(q_new)} maturing 7 February 2027. Recovery 60% = {R(q_rec)}; bad debts {R(q_bad)}.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Sale and receipt of acceptance', 'm': 1, 'skill': 'posting'},
                 {'id': 's2', 'pt': 'Endorsement with discount received ₹2,000', 'm': 1, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Dishonour: Mohan Dr ₹1,50,300, To Nikhil; Nikhil paid by cheque', 'm': 1.5, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Interest ₹3,600 on renewal (on unpaid ₹1,20,000 only)', 'm': 1, 'skill': 'computation'},
                 {'id': 's5', 'pt': 'Cash ₹30,300 and new bill ₹1,23,600 received', 'm': 1, 'skill': 'posting'},
                 {'id': 's6', 'pt': 'Dishonour of new bill on insolvency', 'm': 0.5, 'skill': 'concept'},
                 {'id': 's7', 'pt': 'Recovery ₹74,160 and bad debts ₹49,440', 'm': 1, 'skill': 'computation'},
                 {'id': 's8', 'pt': 'Dates and narrations', 'm': 1, 'skill': 'presentation'},
             ],
             'remarks': ['Many candidates credit Bills Receivable on dishonour of an endorsed bill — the bill left the books on 5 August, so the endorsee (Nikhil) is credited.',
                         'Interest is frequently charged on ₹1,50,300 instead of the unpaid ₹1,20,000.',
                         'Good answers show maturity dates in narrations and a short working note for interest and recovery.'],
             'mistakes': ['Ignoring the discount received of ₹2,000 on endorsement.', 'Writing off 60% instead of 40% as bad debts.', 'Debiting Noting Charges Account in Lalit\'s books instead of charging them to Mohan.'],
             'tips': ['Draw a dated time-line before writing entries.', 'Mention "in full settlement" items explicitly — they usually hide a discount.', 'Show the percentage recovery working separately.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between a bill of exchange and a promissory note (any five points).',
             'model': [table(['Basis', 'Bill of exchange', 'Promissory note'], [
                 ['Nature of instrument', 'Contains an unconditional order to pay', 'Contains an unconditional promise to pay'],
                 ['Number of parties', 'Three — drawer, drawee and payee (drawer and payee may be the same)', 'Two — maker and payee (they cannot be the same person)'],
                 ['Acceptance', 'Must be accepted by the drawee before it binds him', 'No acceptance is needed'],
                 ['Liability', "Acceptor is primarily liable; drawer's liability is secondary and conditional", "Maker's liability is primary and absolute"],
                 ['Dishonour formalities', 'Notice of dishonour must be given; noting and protest are needed', 'No notice of dishonour; noting and protest not needed'],
                 ['Bearer', 'May be payable to bearer, but not to bearer on demand — Section 31(1) of the RBI Act', 'Can never be made payable to bearer — Section 31(2) of the RBI Act'],
             ])],
             'scheme': [{'id': 's1', 'pt': 'Order vs promise', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Parties', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Acceptance', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Liability of drawer vs maker', 'm': 1, 'skill': 'concept'},
                        {'id': 's5', 'pt': 'Any other valid point (dishonour formalities / bearer)', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Answers in a two-column table with a stated basis score well and are quick to mark.', 'Writing only definitions without contrasting points earns very little.'],
             'mistakes': ['Saying a promissory note has three parties.', 'Saying the drawer of a bill is primarily liable.'],
             'tips': ['One line per basis; keep the two columns parallel.', 'Quote the RBI Act section correctly if you use the bearer point.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Calculate the date of maturity of each bill: (i) dated 18 April 2026, 3 months after date; (ii) dated 31 August 2026, 6 months after date; (iii) dated 20 September 2026, 45 days after date; (iv) drawn 25 November 2026, accepted 2 December 2026, 1 month after sight; (v) drawn 29 May 2026, accepted 1 June 2026, 2 months after date.',
             'model': [q3tbl],
             'scheme': [{'id': f's{i}', 'pt': f'Bill ({r}) — correct maturity with working', 'm': 1, 'skill': 'computation'} for i, r in enumerate(['i', 'ii', 'iii', 'iv', 'v'], 1)],
             'remarks': ['Bill (ii) tests the month-end rule and bill (iv) vs (v) tests "after sight" vs "after date" — these separate good answers from average ones.', 'Show the expiry date before adding grace so the examiner can award part marks.'],
             'mistakes': ['Counting the date of the bill in day-based terms.', 'Starting an "after date" bill from the date of acceptance.', 'Forgetting days of grace.'],
             'tips': ['Write "Expiry + 3 days of grace = maturity" for each line.', 'Check whether the year is a leap year when February is involved.'],
             'checks': q3ck},
            {'id': 'q4', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'journal',
             'q': 'On 1 September 2026 Farhan drew a 3-month bill for ₹80,000 on Gita for their mutual accommodation. Gita accepted it and Farhan discounted it for ₹78,000, remitting one-fourth of the proceeds to Gita. The discount is to be borne in the ratio of the proceeds. On maturity Farhan remitted the amount due to Gita, who met the bill. Journalise in the books of Farhan and Gita.',
             'model': [journal(Q4F, 'Books of Farhan — Journal', 'jq4f'), journal(Q4G, 'Books of Gita — Journal', 'jq4g'),
                       wn('Working notes', f'Discount ₹2,000: Gita bears 1/4 = {R(g_dsc)}; proceeds to Gita {R(g_prc)}. Gita has used ₹20,000 of the bill, so Farhan must provide {R(g_due)} on maturity (4 December 2026).')],
             'scheme': [{'id': 's1', 'pt': 'Acceptance entries in both books', 'm': 1, 'skill': 'posting'},
                        {'id': 's2', 'pt': 'Discounting in Farhan\'s books', 'm': 1, 'skill': 'posting'},
                        {'id': 's3', 'pt': 'Remittance ₹19,500 and discount ₹500 shared (both books)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Remittance of ₹60,000 on maturity (both books)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Gita meets the bill: Bills Payable Dr, To Bank', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Most errors come from charging the drawee a share of discount based on the bill amount instead of the proceeds ratio — here both give the same 1/4, but read the question.', 'Candidates who forget Gita\'s final payment entry lose a full mark.'],
             'mistakes': ['Remitting ₹20,000 (one-fourth of the bill) instead of ₹19,500.', 'Farhan recording payment of the bill — he is not the acceptor.'],
             'tips': ['Prepare the two journals side by side so every entry has its mirror.', 'Write the sharing ratio in a working note.']},
        ],
        'revision': {
            'summary': ['Bill = order to pay (drawer, drawee, payee; needs acceptance). Promissory note = promise to pay (maker, payee; no acceptance; never to bearer — s.31(2) RBI Act).',
                        'Receiver records Bills Receivable (asset); acceptor records Bills Payable (liability).',
                        'Holder may hold, endorse or discount the bill; on dishonour the drawee is debited and the account that "has" the bill (B/R, endorsee or bank) is credited.',
                        'Maturity = due date + 3 days of grace (none for demand/sight bills). After date runs from drawing; after sight from acceptance. Public holiday → preceding business day.',
                        'Renewal: cancel old bill like dishonour, charge interest, take new bill. Retirement: early payment, rebate is the acceptor\'s income and the holder\'s expense.',
                        'Insolvency: drawer writes off unrecovered amount as bad debts; insolvent drawee credits Deficiency A/c. Accommodation bills share discount in the ratio of proceeds.'],
            'remember': ['Noting charges always end up on the drawee.', 'Interest on renewal is on the unpaid amount for the extended period only.', 'Bills for collection ≠ discounting — no discount, no cash until collected.'],
            'traps': ["Don't credit Bills Receivable on dishonour of a bill that was endorsed or discounted.", "Don't count the date of the bill when the term is in days.", "Don't charge discount for the full term if the bill is discounted after some days have passed."],
        },
        'quickref': [
            {'k': 'Receipt of bill', 'v': 'Bills Receivable A/c Dr. To Drawee'},
            {'k': 'Acceptance of bill', 'v': 'Drawer A/c Dr. To Bills Payable A/c'},
            {'k': 'Discounting', 'v': 'Bank A/c Dr. + Discount on Bills A/c Dr. To Bills Receivable A/c'},
            {'k': 'Endorsement', 'v': 'Creditor A/c Dr. To Bills Receivable A/c'},
            {'k': 'Dishonour (held / endorsed / discounted)', 'v': 'Drawee Dr. To Bills Receivable (+ Bank for noting) / To Endorsee / To Bank'},
            {'k': 'Dishonour in acceptor\'s books', 'v': 'Bills Payable A/c Dr. + Noting Charges A/c Dr. To Drawer'},
            {'k': 'Date of maturity', 'v': 'Expiry date + 3 days of grace (Negotiable Instruments Act, ss. 22–25); none for on-demand / at-sight bills'},
            {'k': 'Rebate / discount', 'v': 'Amount × rate × unexpired (or remaining) period ÷ 12 months'},
            {'k': 'Renewal interest', 'v': 'Unpaid amount × rate × extended period'},
            {'k': 'Insolvency', 'v': 'Drawer: Bank Dr + Bad Debts Dr To Drawee. Drawee: Drawer Dr To Bank + To Deficiency A/c'},
            {'k': 'Foreign instrument', 'v': 'Any instrument that is not inland — Section 12, Negotiable Instruments Act'},
        ],
        'viva': viva, 'cases': cases,
    }
