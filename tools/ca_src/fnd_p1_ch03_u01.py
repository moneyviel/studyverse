"""CA Foundation · Paper 1 Accounting · Chapter 3 Bank Reconciliation Statement (single unit).
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *

UID = 'fnd-p1-ch03-u01'


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


def ledger(ac, dr, cr, close_date, next_date):
    """Manual ledger: dr/cr = [(date, particulars, amount, opening?)]; closes with Balance c/d on the lighter side."""
    D = [{'date': d, 'part': p, 'amt': a, **({'ob': True} if len(x) > 3 and x[3] else {})} for x in dr for d, p, a in [x[:3]]]
    C = [{'date': d, 'part': p, 'amt': a, **({'ob': True} if len(x) > 3 and x[3] else {})} for x in cr for d, p, a in [x[:3]]]
    sd, sc = sum(x['amt'] for x in D), sum(x['amt'] for x in C)
    b = {'t': 'ledger', 'ac': ac, 'dr': D, 'cr': C}
    if sd > sc:
        C.append({'date': close_date, 'part': 'By Balance c/d', 'amt': sd - sc, 'bal': True}); b['next'] = {'date': next_date, 'side': 'dr', 'amt': sd - sc}
    elif sc > sd:
        D.append({'date': close_date, 'part': 'To Balance c/d', 'amt': sc - sd, 'bal': True}); b['next'] = {'date': next_date, 'side': 'cr', 'amt': sc - sd}
    return b


def plusminus(start_label, start_side, items, end_label, title):
    """Plus/Minus BRS. start_side 'plus' when the opening figure is favourable. items: (label, signed effect).
    The closing figure goes in whichever column makes both columns equal -> table total proves the arithmetic."""
    rows = []
    start_amt = start_label[1]
    rows.append([start_label[0], inr(start_amt) if start_side == 'plus' else '', inr(start_amt) if start_side == 'minus' else ''])
    plus = start_amt if start_side == 'plus' else 0
    minus = start_amt if start_side == 'minus' else 0
    for lab, eff in items:
        if eff > 0: rows.append([lab, inr(eff), '']); plus += eff
        else: rows.append([lab, '', inr(-eff)]); minus += -eff
    diff = plus - minus
    if diff > 0: rows.append([end_label + ' (favourable)', '', inr(diff)]); minus += diff
    elif diff < 0: rows.append([end_label + ' (overdraft)', inr(-diff), '']); plus += -diff
    rows.append(['Total', inr(plus), inr(minus)])
    return table(['Particulars', 'Plus (₹)', 'Minus (₹)'], rows, num=[1, 2], total=True, title=title), diff


def build():
    # =============== Illustration 1: favourable cash book balance, both presentations ===============
    c1 = Checks()
    cb1 = 184500
    up1 = c1.add('42000+18600', 'Cheques issued but not yet presented (Kiran & Co. + Patel Bros.)')
    unc1 = 75000
    int1 = 2150
    dp1 = c1.add('850+12000', 'Bank charges + insurance premium paid by standing instruction')
    neft1 = 26400
    pb1 = c1.add('184500+60600+2150+26400-75000-12850', 'Balance as per pass book')
    c1.add('184500+60600+2150+26400', 'Sub-total after additions')
    i1_bal = table(['Particulars', 'Details (₹)', 'Amount (₹)'], [
        ['Balance as per Cash Book (Dr.)', '', inr(cb1)],
        ['Add: Cheques issued but not yet presented — Kiran & Co.', '42,000', ''],
        ['            — Patel Bros.', '18,600', inr(up1)],
        ['Add: Interest credited by the bank, not yet in Cash Book', '', inr(int1)],
        ['Add: Amount received by NEFT from a customer, not yet in Cash Book', '', inr(neft1)],
        ['', '', inr(cb1 + up1 + int1 + neft1)],
        ['Less: Cheques deposited but not yet credited by the bank', '', '(' + inr(unc1) + ')'],
        ['Less: Bank charges ₹850 and insurance premium ₹12,000 debited by the bank only', '', '(' + inr(dp1) + ')'],
        ['Balance as per Pass Book (Cr.)', '', inr(pb1)],
    ], title='Bank Reconciliation Statement of Shreya Fabrics as on 31 March 2027 ("balance" presentation)')
    i1_pm, d1 = plusminus(('Balance as per Cash Book (Dr.)', cb1), 'plus', [
        ('Cheques issued but not yet presented', up1), ('Interest credited by the bank only', int1), ('NEFT receipt credited by the bank only', neft1),
        ('Cheques deposited but not yet credited', -unc1), ('Bank charges and insurance premium debited by the bank only', -dp1)],
        'Balance as per Pass Book', 'Same statement in "Plus & Minus" presentation')
    assert d1 == pb1

    # =============== Illustration 2: starting from an overdraft ===============
    c2 = Checks()
    od2 = 235600
    pb2 = c2.add('-235600+148000-96500-7800+15000-12400', 'Pass book balance (negative = overdraft)')
    c2.add('235600+96500+7800+12400', 'Overdraft after additions')
    c2.add('148000+15000', 'Total deductions from overdraft')
    c2.add('352300-163000', 'Overdraft as per pass book')
    i2_tab = table(['Particulars', 'Amount (₹)'], [
        ['Overdraft as per Cash Book (Cr. balance)', inr(od2)],
        ['Add: Cheques deposited but not yet credited by the bank', '96,500'],
        ['Add: Interest on overdraft debited by the bank only', '7,800'],
        ['Add: Customer\'s cheque dishonoured, debited by the bank only', '12,400'],
        ['', '3,52,300'],
        ['Less: Cheques issued but not yet presented for payment', '(1,48,000)'],
        ['Less: Dividend collected and credited by the bank only', '(15,000)'],
        ['Overdraft as per Pass Book (Dr. balance)', inr(-pb2)],
    ], title='Bank Reconciliation Statement of Vikram Engineering as on 30 September 2026')
    i2_pm, d2 = plusminus(('Overdraft as per Cash Book', od2), 'minus', [
        ('Cheques issued but not yet presented', 148000), ('Dividend collected by the bank only', 15000),
        ('Cheques deposited but not yet credited', -96500), ('Interest on overdraft charged by the bank only', -7800), ('Cheque dishonoured, not in Cash Book', -12400)],
        'Balance as per Pass Book', 'Plus & Minus check')
    assert d2 == pb2

    # =============== Illustration 3: adjusted cash book then BRS ===============
    c3 = Checks()
    adj3 = c3.add('312480+48000+15500+1000-1240-22500-1200-2700', 'Adjusted (corrected) cash book balance')
    c3.add('60000*2/100', 'Cash discount wrongly included in the bank column (2% of 60,000)')
    c3.add('9630-6930', 'Cheque issued recorded short (9,630 written as 6,930)')
    pb3 = c3.add('349340+84300-126000-5000', 'Balance as per pass book')
    acb3 = ledger('Cash Book (Bank Column) — adjusted, Neelam Traders',
                  [('2027 Mar 31', 'To Balance b/d', 312480, True), ('Mar 31', 'To Debtor (NEFT received directly)', 48000), ('Mar 31', 'To Dividend A/c (collected by bank)', 15500),
                   ('Mar 31', 'To Undercasting of debit side', 1000)],
                  [('Mar 31', 'By Bank Charges A/c', 1240), ('Mar 31', 'By Rao (cheque dishonoured)', 22500), ('Mar 31', 'By Discount Allowed A/c (bank column overstated)', 1200),
                   ('Mar 31', 'By Creditor (cheque recorded short)', 2700)], 'Mar 31', 'Apr 1')
    assert acb3['next']['amt'] == adj3
    brs3 = table(['Particulars', 'Amount (₹)'], [
        ['Balance as per adjusted Cash Book (Dr.)', inr(adj3)],
        ['Add: Cheques issued but not yet presented', '84,300'],
        ['', inr(adj3 + 84300)],
        ['Less: Cheques deposited but not yet credited', '(1,26,000)'],
        ['Less: Amount wrongly debited by the bank (bank\'s error)', '(5,000)'],
        ['Balance as per Pass Book (Cr.)', inr(pb3)],
    ], title='Bank Reconciliation Statement as on 31 March 2027')

    # =============== Illustration 4: find the differences from the two records ===============
    c4 = Checks()
    cb4 = c4.add('50000+120000+36000+24500+18000-15000-42000-55000-27500', 'Cash book balance on 31 March')
    pbk4 = c4.add('50000-15000+120000-42000+36000-55000+1800-450', 'Pass book balance on 31 March')
    c4.add('109000+27500+1800-24500-18000-450', 'Reconciled: cash book to pass book')
    given4 = [
        table(['Date', 'Receipts (Dr.)', '₹', 'Date', 'Payments (Cr.)', '₹'], [
            ['Mar 1', 'To Balance b/d', '50,000', 'Mar 3', 'By Rent', '15,000'],
            ['Mar 5', 'To Sales', '1,20,000', 'Mar 10', 'By Joshi', '42,000'],
            ['Mar 14', 'To Nair', '36,000', 'Mar 22', 'By Salaries', '55,000'],
            ['Mar 28', 'To Gill', '24,500', 'Mar 29', 'By Mehra', '27,500'],
            ['Mar 30', 'To Bose', '18,000', 'Mar 31', 'By Balance c/d', inr(cb4)],
        ], title='Cash Book (bank column) of Arya Stores — March 2027'),
        table(['Date', 'Particulars', 'Withdrawals (₹)', 'Deposits (₹)', 'Balance (₹)'], [
            ['Mar 1', 'Opening balance', '', '', '50,000 Cr'],
            ['Mar 3', 'Rent', '15,000', '', '35,000 Cr'],
            ['Mar 6', 'Cash/cheques deposited (sales)', '', '1,20,000', '1,55,000 Cr'],
            ['Mar 12', 'Joshi', '42,000', '', '1,13,000 Cr'],
            ['Mar 15', 'Nair', '', '36,000', '1,49,000 Cr'],
            ['Mar 22', 'Salaries', '55,000', '', '94,000 Cr'],
            ['Mar 25', 'Interest on savings', '', '1,800', '95,800 Cr'],
            ['Mar 31', 'Service charges', '450', '', inr(pbk4) + ' Cr'],
        ], title='Bank statement of Arya Stores — March 2027'),
    ]
    i4_pm, d4 = plusminus(('Balance as per Cash Book (Dr.)', cb4), 'plus', [
        ('Cheque issued to Mehra, not yet presented', 27500), ('Interest credited by the bank only', 1800),
        ('Cheque from Gill deposited, not yet credited', -24500), ('Cheque from Bose deposited, not yet credited', -18000), ('Service charges debited by the bank only', -450)],
        'Balance as per Pass Book', 'Bank Reconciliation Statement of Arya Stores as on 31 March 2027')
    assert d4 == pbk4

    # =============== Questions ===============
    q1c = Checks()
    q1_up = q1c.add('110000-64000', 'Cheques issued but not presented')
    q1_unc = q1c.add('92000-61500', 'Cheques deposited but not credited by 31 December')
    q1_cb = q1c.add('246300+30500+8000+650-46000-25000-1900', 'Balance as per cash book')
    q1_model = table(['Particulars', 'Amount (₹)'], [
        ['Balance as per Pass Book (Cr.)', '2,46,300'],
        ['Add: Cheques deposited but not yet credited (92,000 − 61,500)', inr(q1_unc)],
        ['Add: Cheque recorded in Cash Book but not sent to the bank', '8,000'],
        ['Add: Bank charges debited in the Pass Book only', '650'],
        ['', inr(246300 + 30500 + 8000 + 650)],
        ['Less: Cheques issued but not yet presented (1,10,000 − 64,000)', '(' + inr(q1_up) + ')'],
        ['Less: Bill collected directly by the bank', '(25,000)'],
        ['Less: Interest allowed by the bank', '(1,900)'],
        ['Balance as per Cash Book (Dr.)', inr(q1_cb)],
    ], title='Bank Reconciliation Statement of Kapoor Electronics as on 31 December 2026')

    q3c = Checks()
    q3_adj = q3c.add('-152750+36000+7400+4200-9850-21300-1800', 'Adjusted cash book balance (negative = overdraft)')
    q3_up = q3c.add('218400-174000', 'Cheques issued but not presented')
    q3_unc = q3c.add('305000-240000', 'Cheques deposited but not cleared')
    q3_pb = q3c.add('-138100+44400-65000+12000', 'Pass book balance (negative = overdraft)')
    q3c.add('17550-15750', 'Deposit recorded excess in cash book')
    q3_acb = ledger('Cash Book (Bank Column) — adjusted, Hari Om Industries',
                    [('2027 Mar 31', 'To Customer (direct deposit)', 36000), ('Mar 31', 'To Supplier (payment entered twice — reversed)', 7400), ('Mar 31', 'To Interest on Fixed Deposit A/c', 4200)],
                    [('2027 Mar 31', 'By Balance b/d (overdraft)', 152750, True), ('Mar 31', 'By Interest on Overdraft A/c', 9850), ('Mar 31', 'By Vehicle Loan A/c (EMI)', 21300),
                     ('Mar 31', 'By Debtor (deposit recorded ₹1,800 excess)', 1800)], 'Mar 31', 'Apr 1')
    assert q3_acb['next']['amt'] == -q3_adj and q3_acb['next']['side'] == 'cr'
    q3_brs = table(['Particulars', 'Amount (₹)'], [
        ['Overdraft as per adjusted Cash Book', inr(-q3_adj)],
        ['Add: Cheques deposited but not yet credited (3,05,000 − 2,40,000)', inr(q3_unc)],
        ['', inr(-q3_adj + q3_unc)],
        ['Less: Cheques issued but not yet presented (2,18,400 − 1,74,000)', '(' + inr(q3_up) + ')'],
        ['Less: Amount wrongly credited by the bank', '(12,000)'],
        ['Overdraft as per Pass Book', inr(-q3_pb)],
    ], title='Bank Reconciliation Statement as on 31 March 2027')

    q4c = Checks()
    q4_cb = q4c.add('-58200-2000-500+380-12000+2140-27300+41500', 'Cash book balance (negative = overdraft)')
    q4c.add('58200+27300+2000+500+12000', 'Overdraft after additions')
    q4c.add('41500+380+2140', 'Total deductions')
    q4c.add('6000*2', 'Effect of recording a deposit on the wrong side')
    q4_model = table(['Particulars', 'Amount (₹)'], [
        ['Overdraft as per Pass Book', '58,200'],
        ['Add: Cheques issued but not yet presented', '27,300'],
        ['Add: Credit side of the bank column overcast', '2,000'],
        ['Add: Debit side of the bank column undercast', '500'],
        ['Add: Deposit of ₹6,000 entered on the credit side instead of the debit side (6,000 × 2)', '12,000'],
        ['', '1,00,000'],
        ['Less: Cheques deposited but not yet credited', '(41,500)'],
        ['Less: Bank charges debited in the Pass Book only', '(380)'],
        ['Less: Interest on overdraft debited in the Pass Book only', '(2,140)'],
        ['Overdraft as per Cash Book', inr(-q4_cb)],
    ], title='Bank Reconciliation Statement of Rhea & Sons as on 30 June 2026')

    # =============== Case ===============
    kc = Checks()
    k_adj = kc.add('265000+30000-1500-18000', 'Adjusted cash book balance')
    k_pb = kc.add('275500+52000-70000', 'Pass book balance')

    rules = table(['Item', 'Start: Cash Book Dr. (favourable)', 'Start: Pass Book Cr. (favourable)'], [
        ['Cheques issued, not yet presented', 'Add', 'Less'],
        ['Cheques deposited, not yet credited / cleared', 'Less', 'Add'],
        ['Interest, dividend, bills collected or direct deposits credited by bank only', 'Add', 'Less'],
        ['Bank charges, interest on overdraft, standing-instruction payments debited by bank only', 'Less', 'Add'],
        ['Cheque deposited and dishonoured (not yet in Cash Book)', 'Less', 'Add'],
        ['Debit side of bank column overcast / a receipt wrongly recorded', 'Less', 'Add'],
        ['Credit side of bank column overcast / a payment recorded in excess', 'Add', 'Less'],
        ['Bank wrongly debits the account', 'Less', 'Add'],
        ['Bank wrongly credits the account', 'Add', 'Less'],
    ], title='Add or less? (When you start from an overdraft, every sign flips.)',
        note='Shortcut: ask "which record shows MORE money right now because of this item?" If the starting record shows more, deduct; if it shows less, add. A negative final answer means the other record shows an overdraft.')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch03', 'n': 1,
        'title': 'Bank Reconciliation Statement',
        'outcomes': [
            'Read a pass book or bank statement and explain why its balance is the mirror image of the bank column of the cash book.',
            'Identify every reason why the two balances differ — timing gaps, items the bank records first, and errors by either side.',
            'Prepare a Bank Reconciliation Statement starting from any of the four balances (favourable or overdraft, cash book or pass book), in both the "balance" and the "plus & minus" layouts.',
            'Prepare an adjusted (amended) cash book first and then reconcile, and state which bank balance goes to the balance sheet.',
            'Explain why regular reconciliation is a core internal control against errors and fraud.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 60}, 'prereq': ['fnd-p1-ch02-u05'],
                 'exam_tip': 'BRS is a regular 4–10 mark question. The marks go to correct add/less signs, correct treatment of an overdraft and a clean statement with a proper heading "as on <date>". Practise starting from all four balances.'},
        'concepts': [
            {'id': 'c1', 'title': 'Pass book versus the cash book\'s bank column',
             'body': ['Every bank transaction is written in two places: in the bank column of the cash book, kept by the business, and in the business\'s account in the bank\'s own books. The pass book (or the bank statement — loose sheets, a PDF or a net-banking download) is simply a copy of that account as kept by the bank.',
                      'The two records look at the same money from opposite ends. For the business, money lying in the bank is an asset — the bank owes it — so the cash book shows a debit balance. For the bank, the same money is a liability owed to its customer, so the pass book shows a credit balance. A credit balance in the pass book is therefore "favourable", and a debit balance in the pass book means an overdraft (the customer owes the bank), which appears as a credit balance in the cash book.',
                      'Banks also do many things for customers that later appear in the pass book: collecting cheques, bills, dividends and interest; paying premiums, EMIs and utility bills on standing instructions; discounting bills; granting overdrafts and loans; and charging fees for these services.'],
             'analogy': 'Two friends keep a note of a loan between them. The lender writes "Ravi owes me ₹500" and Ravi writes "I owe ₹500". Same fact, opposite sides — exactly like the cash book and the pass book.',
             'work': 'At year-end every auditor obtains a bank balance confirmation directly from the bank. The first thing checked is whether the balance in the client\'s books can be reconciled to that confirmation.'},
            {'id': 'c2', 'title': 'What a Bank Reconciliation Statement is — and why it matters',
             'body': ['A Bank Reconciliation Statement (BRS) is a working statement, prepared by the account holder on a particular date, that starts from the bank balance in one record, lists every cause of difference, and arrives at the balance in the other record. It is not a ledger account and it does not by itself correct anything.',
                      'Why bother? (i) It throws up errors made in the cash book or by the bank. (ii) It shows cheques that are taking unusually long to clear. (iii) It is an internal control: a cashier who records deposits in the cash book but pockets the money is caught quickly when someone independent reconciles every month. (iv) It reveals the true bank position after allowing for items still in the pipeline, and makes sure every bank transaction for the period is actually recorded.',
                      'Many past corporate frauds involved manipulated bank balances or fake bank statements, which is why reconciliation is now a routine part of internal control. Frequency depends on size and volume — large businesses reconcile daily or weekly, small ones monthly or quarterly.'],
             'analogy': 'A BRS is like checking your phone\'s expense app against your bank SMS alerts at the end of the month — any gap is either a delay, something you forgot to note, or a mistake somebody made.',
             'work': 'In an audit, an old "cheque deposited but not credited" that never clears is a classic red flag for teeming and lading or a fictitious receipt. Seniors often ask articled assistants to trace every reconciling item to the next month\'s bank statement.'},
            {'id': 'c3', 'title': 'Why the two balances differ',
             'body': ['Timing gaps: a transaction is recorded by the business and the bank on different dates. Cheques issued are written in the cash book on the day of issue, but the bank records them only when the payee presents them. Cheques deposited are written in the cash book immediately, but the bank credits them only after collection (clearing).',
                      'Transactions the bank records first: interest credited, dividends or interest on investments collected, bills collected, direct deposits by customers through NEFT/RTGS/UPI, bank charges, locker rent, interest on overdraft, payments made under standing instructions (insurance, EMIs), and cheques or discounted bills dishonoured. The business learns of these only when it sees the statement.',
                      'Errors: by the business (amount written wrongly, entry made twice or omitted, totals overcast or undercast, entry on the wrong side, a receipt written in the bank column instead of the cash column) or by the bank (crediting or debiting the wrong customer\'s account).'],
             'blocks': [rules],
             'analogy': 'A parcel booked today is in your "sent" list at once but appears in the receiver\'s "received" list only after delivery — the gap is timing, not a mistake.',
             'work': 'In accounting software, the "bank reconciliation" screen lets you tick each cash-book entry with its bank date; whatever stays unticked is exactly the list of reconciling items for the BRS.'},
            {'id': 'c4', 'title': 'Add or less — the logic, and the four starting points',
             'body': ['You may start from any of four balances: debit (favourable) balance as per cash book, credit (overdraft) balance as per cash book, credit (favourable) balance as per pass book, or debit (overdraft) balance as per pass book. The answer is the balance in the other record.',
                      'Do not memorise a list — reason it out. Take each item and ask: because of this item, does the record I started from show more money or less money than the other record? If it shows more, deduct; if it shows less, add. Example: a cheque issued but not presented has already reduced the cash book but not the bank — the cash book shows less — so starting from the cash book you add it.',
                      'When you start from an overdraft, treat the overdraft as a negative balance: every add becomes less and every less becomes add. If you start from a favourable balance and the answer comes out negative, the other record shows an overdraft of that amount (and vice versa).'],
             'analogy': 'Two thermometers that should read the same: if one reads higher because of a known reason, you subtract that reason from it to get the other reading.',
             'work': 'Reviewers in practice check the sign of each reconciling item against this "which shows more?" logic — the most common error in a client-prepared BRS is a sign error on an overdraft account.'},
            {'id': 'c5', 'title': 'Two layouts: "balance" and "plus & minus"',
             'body': ['Balance presentation: start with the balance, show "Add:" items, a sub-total, then "Less:" items, and end with the balance as per the other record. A negative figure is shown in brackets.',
                      'Plus & minus presentation: two amount columns. The starting balance goes in the plus column if favourable and in the minus column if it is an overdraft; each item goes in the plus or minus column; the closing balance is the figure that makes both columns equal. Both columns are then totalled — a built-in arithmetic check.',
                      'Whichever layout you use, write a heading with the name and "Bank Reconciliation Statement as on <date>" — a BRS is always as on a date, not for a period.'],
             'blocks': [i1_bal],
             'analogy': 'Balance presentation reads like a story; plus & minus is like a scale where both pans must weigh the same.',
             'work': 'Audit working papers usually show the BRS in balance form, with each reconciling item cross-referenced to the next month\'s bank statement where it finally cleared.'},
            {'id': 'c6', 'title': 'Adjusted (amended) cash book method',
             'body': ['Here the cash book is first corrected for everything that is the business\'s own omission or error — bank charges, interest, direct deposits and payments, collections, dishonoured cheques or bills, and mistakes in the cash book itself (wrong amounts, double entries, casting errors). The corrected figure is the adjusted cash book balance.',
                      'Only the items that remain — timing gaps (cheques issued but not presented, cheques deposited but not cleared) and errors made by the bank — are taken to the BRS, which then starts from the adjusted balance. An item adjusted in the cash book is never repeated in the BRS, and the bank\'s errors are never put in the cash book.',
                      'For a monthly reconciliation the adjusted cash book is optional. At the year-end it should be prepared, because the balance sheet must show the correct bank balance as per the business\'s books — that is, the adjusted cash book balance, not the pass book balance.'],
             'analogy': 'Before comparing your notes with a friend\'s, you first fix your own spelling mistakes; only then do you list the differences that are genuinely "theirs" or "not yet".',
             'work': 'At the year-end the accountant passes journal entries for bank charges, interest, direct receipts and dishonoured cheques before finalising accounts — this is the adjusted cash book in practice.'},
            {'id': 'c7', 'title': 'Working from the actual cash book and bank statement',
             'body': ['In practice you are not handed a list of differences — you must find them. Tick each entry in the cash book against the bank statement (receipts against deposits, payments against withdrawals). Unticked cash-book receipts are deposits not yet credited; unticked cash-book payments are cheques not yet presented; unticked bank-statement entries are items the bank recorded first.',
                      'If the BRS is for an earlier date (say 31 March) and you are also given the next month\'s statement, the March items that appear in April\'s statement confirm the timing differences as on 31 March.'],
             'blocks': [i4_pm],
             'analogy': 'Like matching socks after laundry: pair off what matches; the odd ones out tell you what is missing.',
             'work': 'Bank feeds in modern software auto-match most entries; the accountant\'s real job is investigating the unmatched few — duplicate payments, missed receipts and charges.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Favourable cash book balance — both layouts', 'difficulty': 'core', 'minutes': 12,
             'q': 'The bank column of the cash book of Shreya Fabrics showed a debit balance of ₹1,84,500 on 31 March 2027. On comparing it with the bank statement: (1) cheques issued to Kiran & Co. ₹42,000 and Patel Bros. ₹18,600 had not been presented; (2) cheques of ₹75,000 deposited on 30 March were credited by the bank only on 2 April; (3) the bank credited interest of ₹2,150; (4) the bank debited charges of ₹850 and paid an insurance premium of ₹12,000 under a standing instruction; (5) a customer paid ₹26,400 directly by NEFT. None of (3)–(5) has been recorded in the cash book. Prepare a BRS.',
             'solution': [i1_bal, i1_pm,
                          wn('Reasoning', 'Unpresented cheques have already reduced the cash book but not the bank, so the cash book shows less — add. Uncleared deposits have already increased the cash book — the cash book shows more — deduct. Credits made only by the bank are added; debits made only by the bank are deducted.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Starting from an overdraft', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'The cash book of Vikram Engineering showed an overdraft of ₹2,35,600 on 30 September 2026. Find the balance as per the pass book: (1) cheques issued ₹1,48,000 not yet presented; (2) cheques deposited ₹96,500 not yet credited; (3) interest on overdraft ₹7,800 charged by the bank; (4) the bank collected a dividend of ₹15,000; (5) a customer\'s cheque of ₹12,400 deposited earlier was dishonoured. Items (3)–(5) are not yet in the cash book.',
             'solution': [i2_tab, i2_pm,
                          wn('Signs flip for an overdraft', 'An unpresented cheque means the bank has not yet paid it, so the bank\'s overdraft is smaller — deduct from the overdraft. An uncleared deposit means the bank has not yet reduced the overdraft — add. Interest and the dishonoured cheque increase the bank\'s overdraft — add. The dividend reduces it — deduct.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Adjusted cash book, then BRS', 'difficulty': 'hard', 'minutes': 20,
             'q': 'On 31 March 2027 the bank column of Neelam Traders\' cash book showed a debit balance of ₹3,12,480. Examination revealed: (1) bank charges ₹1,240 not entered in the cash book; (2) a customer paid ₹48,000 directly into the bank by NEFT — not recorded; (3) a cheque from Rao for ₹22,500 deposited earlier was dishonoured on 29 March — not recorded; (4) a debtor who owed ₹60,000 paid by cheque after a 2% cash discount, but the cashier entered ₹60,000 in the bank column; (5) a cheque of ₹9,630 issued to a supplier was entered as ₹6,930; (6) the bank collected a dividend of ₹15,500 — not recorded; (7) the debit side of the bank column was undercast by ₹1,000; (8) cheques issued ₹84,300 were not presented by 31 March; (9) cheques deposited ₹1,26,000 were not credited by 31 March; (10) the bank wrongly debited ₹5,000 relating to another customer. Prepare the adjusted cash book and the BRS. What bank balance appears in the balance sheet?',
             'solution': [acb3, brs3,
                          wn('What went where', 'Items (1)–(7) are the business\'s own omissions or errors, so they correct the cash book. Items (8)–(9) are timing differences and (10) is the bank\'s error, so they go to the BRS only.'),
                          p(f'The balance sheet shows the adjusted cash book balance, {R(adj3)} (cash at bank), not the pass book figure of {R(pb3)}.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Find the differences yourself', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'From the cash book (bank column) and the bank statement of Arya Stores for March 2027 given below, prepare a Bank Reconciliation Statement as on 31 March 2027.',
             'given': given4,
             'solution': [i4_pm,
                          wn('Matching', 'Matched both sides: opening balance, rent, sales deposit, Joshi, Nair and salaries. Unmatched in the cash book: Gill ₹24,500 and Bose ₹18,000 (deposited, not yet credited) and Mehra ₹27,500 (issued, not yet presented). Unmatched in the bank statement: interest ₹1,800 and service charges ₹450.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Year-end bank audit at a distributor', 'role': 'Articled assistant on a statutory audit',
             'situation': 'The client\'s BRS as on 31 March shows ₹4.6 lakh of "cheques deposited but not credited", including a ₹1.2 lakh cheque dated 12 January. There is also an "unpresented" cheque of ₹80,000 issued in September.',
             'steps': ['Obtain the bank\'s balance confirmation directly and agree the pass-book figure in the BRS to it.',
                       'Trace each "deposited but not credited" item to the April bank statement. A deposit made in March should clear within a few days; one dated January that is still uncleared is not a timing difference.',
                       'Ask for the deposit slip and the customer\'s ledger for the January cheque — a receipt recorded in the books but never banked can hide misappropriation (teeming and lading).',
                       'For the September cheque: a cheque not presented for months may be stale (cheques are generally valid for three months). It may need to be written back to the supplier\'s account.',
                       'Record findings with cross-references and propose adjustments to the senior.'],
             'takeaway': 'A BRS is only as good as its reconciling items. Every item should clear in the next statement — old items are the auditor\'s first lead.',
             'think': 'Why is a deposit that never clears more dangerous than a cheque that is never presented?',
             'answer': 'An uncleared deposit means the books show money that may never have reached the bank — the asset may be fictitious or stolen. An unpresented cheque at worst means a liability is still owed.'},
            {'id': 'j2', 'title': 'Monthly reconciliation with a UPI-heavy bank account', 'role': 'Accounts executive in a retail chain',
             'situation': 'Your store account receives hundreds of UPI credits a day. The bank statement for June shows ₹38,400 of credits that nobody has recorded, plus payment-gateway charges of ₹2,150.',
             'steps': ['Import the bank statement into the accounting software and run auto-matching against the cash book.',
                       'For the unmatched credits, download the UPI settlement report and identify the customers or stores.',
                       'Pass entries for the gateway charges and the identified receipts — these belong in the adjusted cash book.',
                       'Keep genuinely unidentified credits in a suspense account and follow up; do not simply leave them out.',
                       'Prepare the BRS showing only timing items and file it with the month-end pack.'],
             'takeaway': 'Items the bank records first must be brought into the books promptly; otherwise both profit and receivables are misstated.'},
        ],
        'mcqs': [
            M('m1', 'A pass book is a copy of:', ['The customer\'s account in the books of the bank', 'The bank account in the customer\'s books', 'The cash book of the customer', 'The bank\'s cash book'], 0,
              'The bank prepares it from its own ledger; it shows the customer\'s account as the bank sees it.', 'c1'),
            M('m2', 'A credit balance in the pass book indicates:', ['A favourable balance, equal to a debit balance in the cash book', 'An overdraft', 'A credit balance in the cash book', 'An error by the bank'], 0,
              'For the bank, a customer\'s deposit is a liability (credit); for the customer, it is an asset (debit).', 'c1'),
            M('m3', 'Starting with the debit balance as per cash book, cheques issued but not yet presented are:', ['Added', 'Deducted', 'Ignored', 'Adjusted in the cash book'], 0,
              'The cash book has already been reduced by these cheques, the bank has not — so the cash book shows less and the amount is added.', 'c4'),
            M('m4', 'Starting with the overdraft as per pass book, cheques deposited but not yet credited are:', ['Deducted', 'Added', 'Ignored', 'Shown in the adjusted cash book'], 0,
              'The cash book has already reduced the overdraft by these deposits, the bank has not. So the pass book shows a bigger overdraft — deduct to reach the cash book overdraft.', 'c4', 'moderate'),
            M('m5', 'Cash book debit balance ₹40,000; cheques issued not presented ₹6,000; cheques deposited not credited ₹9,000; bank charges in pass book only ₹500. Balance as per pass book:', ['₹36,500', '₹43,500', '₹37,500', '₹55,500'], 0,
              '40,000 + 6,000 − 9,000 − 500 = ₹36,500.', 'c4', 'core', '40000+6000-9000-500'),
            M('m6', 'Which of these is taken to the adjusted cash book rather than to the BRS?', ['Bank charges not yet recorded in the cash book', 'Cheques issued but not presented', 'Cheques deposited but not cleared', 'An amount wrongly debited by the bank'], 0,
              'Bank charges are the business\'s omission and must be recorded. Timing differences and the bank\'s own errors stay in the BRS.', 'c6'),
            M('m7', 'Overdraft as per cash book ₹25,000; cheques issued not presented ₹8,000; interest on overdraft ₹1,200 debited by the bank only. Overdraft as per pass book:', ['₹18,200', '₹34,200', '₹31,800', '₹15,800'], 0,
              'Unpresented cheques mean the bank\'s overdraft is smaller (−8,000); interest makes it bigger (+1,200): 25,000 − 8,000 + 1,200 = ₹18,200.', 'c4', 'moderate', '25000-8000+1200'),
            M('m8', 'Starting with the debit balance as per cash book, overcasting of the debit side of the bank column is:', ['Deducted', 'Added', 'Ignored', 'Doubled and added'], 0,
              'Overcasting receipts makes the cash book show more than it should — deduct.', 'c3'),
            M('m9', 'The bank balance shown in the balance sheet at the year-end is:', ['The adjusted cash book balance', 'The pass book balance', 'The unadjusted cash book balance', 'The average of the two'], 0,
              'The balance sheet shows the correct balance as per the business\'s books after recording all omissions and correcting errors.', 'c6'),
            M('m10', 'Starting from the credit balance as per pass book, a cheque deposited and dishonoured (not yet entered in the cash book) is:', ['Added', 'Deducted', 'Ignored', 'Shown as a note only'], 0,
              'The cash book still shows the deposit, the bank has reversed it — so the pass book shows less; add to reach the cash book.', 'c4', 'moderate'),
            M('m11', 'Pass book credit balance ₹80,000. A customer\'s direct deposit of ₹12,000 is not yet in the cash book; there is no other difference. Balance as per cash book:', ['₹68,000', '₹92,000', '₹80,000', '₹12,000'], 0,
              'The pass book includes the deposit, the cash book does not: 80,000 − 12,000 = ₹68,000.', 'c4', 'core', '80000-12000'),
            M('m12', 'A Bank Reconciliation Statement is:', ['A statement prepared by the account holder as on a date', 'A ledger account prepared by the bank', 'Part of the double entry system', 'Prepared for a period, like a profit and loss account'], 0,
              'A BRS is a working statement, outside the double entry, prepared by the business as on a particular date.', 'c2'),
            M('m13', 'A cheque of ₹4,000 deposited was wrongly entered on the credit side of the bank column. Starting from the debit balance as per cash book, you should:', ['Add ₹8,000', 'Add ₹4,000', 'Deduct ₹8,000', 'Deduct ₹4,000'], 0,
              'The cash book should have gone up by 4,000 but went down by 4,000 — it is understated by 8,000, so add 8,000.', 'c3', 'hard'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'On 31 December 2026 the pass book of Kapoor Electronics showed a credit balance of ₹2,46,300. Prepare a Bank Reconciliation Statement from the following: (1) cheques issued during December ₹1,10,000, of which only ₹64,000 were presented before 31 December; (2) cheques deposited ₹92,000, of which ₹61,500 were credited by 31 December; (3) a cheque of ₹8,000 received was recorded in the bank column but not sent to the bank; (4) the bank collected a bill receivable of ₹25,000 directly; (5) interest allowed ₹1,900 and bank charges ₹650 appear only in the pass book.',
             'model': [q1_model, wn('Working', f'Unpresented = 1,10,000 − 64,000 = {R(q1_up)}. Not yet credited = 92,000 − 61,500 = {R(q1_unc)}. A cheque recorded but not banked is treated like a deposit not yet credited.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Correct heading with name and "as on 31 December 2026"; starts from pass book ₹2,46,300', 'm': 0.5, 'skill': 'presentation'},
                 {'id': 's2', 'pt': 'Uncleared ₹30,500 and unbanked ₹8,000 added', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Bank charges ₹650 added', 'm': 0.5, 'skill': 'application'},
                 {'id': 's4', 'pt': 'Unpresented ₹46,000 deducted', 'm': 1, 'skill': 'computation'},
                 {'id': 's5', 'pt': 'Bill collected ₹25,000 and interest ₹1,900 deducted', 'm': 1, 'skill': 'application'},
                 {'id': 's6', 'pt': f'Correct cash book balance {R(q1_cb)}', 'm': 0.5, 'skill': 'computation'},
             ],
             'remarks': ['Many candidates take the total cheques issued (₹1,10,000) instead of only the unpresented part.', 'The cheque that was never sent to the bank confused many — it behaves exactly like an uncleared deposit.'],
             'mistakes': ['Using cash-book signs while starting from the pass book.', 'Deducting bank charges when starting from the pass book.', 'Omitting the date in the heading.'],
             'tips': ['Write the starting balance with (Cr.) or (Dr.) beside it so the signs stay clear.', 'Show partial figures (1,10,000 − 64,000) inside the particulars — they earn step marks.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'What is a Bank Reconciliation Statement? Why may the bank balance in the cash book not agree with the pass book? Give one example for each reason.',
             'model': [p('A Bank Reconciliation Statement is a statement prepared by the account holder, as on a given date, that starts from the bank balance in one record (cash book or pass book), lists every reason for the gap and arrives at the balance in the other record.'),
                       ul(['Timing differences — the same transaction is recorded by the two parties on different dates; e.g. a cheque issued on 30 March is in the cash book at once but reaches the bank only when presented on 3 April.',
                           'Transactions recorded first by the bank — e.g. bank charges, interest credited, dividends collected, payments under standing instructions or direct deposits by customers, which the business records only after seeing the statement.',
                           'Errors by the business — e.g. a receipt entered twice in the bank column, or casting errors.',
                           'Errors by the bank — e.g. a cheque of another customer wrongly debited to the account.'])],
             'scheme': [
                 {'id': 's1', 'pt': 'Meaning of BRS — prepared by the account holder, as on a date, reconciles the two balances', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Timing differences with example', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': 'Items recorded by the bank first, with example', 'm': 1, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Errors by either party, with example', 'm': 1, 'skill': 'concept'},
             ],
             'remarks': ['Good answers classify the causes; weaker ones list random items without grouping them.', 'An example for each cause is expected — the question asks for it.'],
             'mistakes': ['Saying the BRS is prepared by the bank.', 'Calling a BRS a ledger account.'],
             'tips': ['Use three or four headings — one per cause — with a one-line example under each.']},
            {'id': 'q3', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'ledger',
             'q': 'On 31 March 2027 the cash book of Hari Om Industries showed an overdraft of ₹1,52,750. Prepare (a) the adjusted cash book and (b) a Bank Reconciliation Statement as on that date: (1) cheques issued ₹2,18,400, of which ₹1,74,000 were presented by 31 March; (2) cheques deposited ₹3,05,000, of which ₹2,40,000 were credited by 31 March; (3) interest on overdraft ₹9,850 charged by the bank — not recorded; (4) vehicle-loan EMI ₹21,300 paid by the bank under a standing instruction — not recorded; (5) a customer deposited ₹36,000 directly — not recorded; (6) a payment of ₹7,400 to a supplier was entered twice in the cash book; (7) a deposit of ₹15,750 was entered in the cash book as ₹17,550; (8) the bank wrongly credited ₹12,000 belonging to another customer; (9) interest on a fixed deposit ₹4,200 was credited by the bank — not recorded.',
             'model': [q3_acb, q3_brs,
                       wn('Classification', 'Adjusted cash book: (3), (4), (5), (6), (7), (9) — the business\'s omissions and errors. BRS: (1), (2) — timing; (8) — the bank\'s error.'),
                       p(f'The balance sheet shows a bank overdraft of {R(-q3_adj)} (adjusted cash book) under current liabilities.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Adjusted cash book opened with overdraft ₹1,52,750 on the credit side', 'm': 1, 'skill': 'posting'},
                 {'id': 's2', 'pt': 'Direct deposit, double-entered payment and FD interest debited', 'm': 1.5, 'skill': 'rectification'},
                 {'id': 's3', 'pt': 'Interest on overdraft, EMI and excess deposit ₹1,800 credited', 'm': 1.5, 'skill': 'rectification'},
                 {'id': 's4', 'pt': f'Adjusted overdraft {R(-q3_adj)} correctly balanced', 'm': 1, 'skill': 'balancing'},
                 {'id': 's5', 'pt': 'BRS starts from the adjusted overdraft; uncleared ₹65,000 added', 'm': 1.5, 'skill': 'application'},
                 {'id': 's6', 'pt': 'Unpresented ₹44,400 and bank\'s wrong credit ₹12,000 deducted', 'm': 1.5, 'skill': 'application'},
                 {'id': 's7', 'pt': f'Correct pass book overdraft {R(-q3_pb)}', 'm': 1, 'skill': 'computation'},
                 {'id': 's8', 'pt': 'No item repeated in both; headings and dates proper', 'm': 1, 'skill': 'presentation'},
             ],
             'remarks': ['The commonest error was putting the bank\'s wrong credit into the adjusted cash book — the bank\'s errors never go there.', 'Many candidates repeated adjusted items again in the BRS, double counting them.', 'Overdraft signs were reversed in a large number of scripts.'],
             'mistakes': ['Opening the overdraft on the debit side of the cash book.', 'Treating the ₹7,400 double entry as ₹14,800.', 'Taking total cheques instead of the unpresented / uncleared balance.'],
             'tips': ['First classify each item: "CB" (own error/omission) or "BRS" (timing or bank error). Then write.', 'Label the final figure clearly as "Overdraft as per Pass Book".']},
            {'id': 'q4', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'On 30 June 2026 the pass book of Rhea & Sons showed an overdraft of ₹58,200. Find the balance as per cash book: (1) cheques deposited ₹41,500 were not credited; (2) cheques issued ₹27,300 were not presented; (3) the credit side of the bank column was overcast by ₹2,000; (4) the debit side of the bank column was undercast by ₹500; (5) bank charges ₹380 appear only in the pass book; (6) a cheque of ₹6,000 deposited was entered on the credit side of the bank column; (7) interest on overdraft ₹2,140 appears only in the pass book.',
             'model': [q4_model, wn('Reasoning', 'Each cash-book error made the cash book show less money (a bigger overdraft) than the bank, so starting from the pass-book overdraft they are added. The ₹6,000 deposit should have reduced the overdraft but increased it instead — a double effect of ₹12,000.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Starts from pass book overdraft with heading and date', 'm': 0.5, 'skill': 'presentation'},
                 {'id': 's2', 'pt': 'Unpresented cheques added to the overdraft', 'm': 1, 'skill': 'application'},
                 {'id': 's3', 'pt': 'Casting errors ₹2,000 and ₹500 added', 'm': 1, 'skill': 'rectification'},
                 {'id': 's4', 'pt': 'Wrong-side entry treated as ₹12,000', 'm': 1.5, 'skill': 'rectification'},
                 {'id': 's5', 'pt': 'Uncleared cheques, charges and interest deducted', 'm': 1.5, 'skill': 'application'},
                 {'id': 's6', 'pt': f'Correct cash book overdraft {R(-q4_cb)}', 'm': 0.5, 'skill': 'computation'},
             ],
             'remarks': ['Wrong-side entries were usually taken at single value; the effect is double.', 'Candidates who reasoned "which book shows more?" got the signs right.'],
             'mistakes': ['Applying favourable-balance signs to an overdraft.', 'Taking the wrong-side entry at ₹6,000.'],
             'tips': ['Write "Overdraft" in the particulars each time so the reader knows the direction.']},
        ],
        'revision': {
            'summary': ['Pass book = the bank\'s copy of your account; its credit balance = your debit (favourable) balance.',
                        'BRS: prepared by the account holder, as on a date, from one balance to the other, listing every cause of difference.',
                        'Causes: timing gaps, items recorded first by the bank, errors by either party.',
                        'Reason each item: does my starting record show more (deduct) or less (add)? Overdraft → signs flip.',
                        'Adjusted cash book: correct own errors and omissions first; BRS keeps only timing items and bank errors; balance sheet uses the adjusted cash book balance.'],
            'remember': ['Unpresented cheques: add to cash book balance. Uncleared deposits: deduct from cash book balance.',
                         'Bank charges, interest on overdraft, standing-instruction payments, dishonour: deduct from cash book balance.',
                         'Interest credited, collections, direct deposits: add to cash book balance.',
                         'Wrong-side entry: double the amount.'],
            'traps': ["Don't put the bank's errors into the adjusted cash book.", "Don't repeat an item in both the adjusted cash book and the BRS.", "Don't take the total cheques issued — take only those not presented.", "A negative answer is an overdraft in the other record — say so."],
        },
        'quickref': [
            {'k': 'Pass book Cr. balance', 'v': 'Favourable = Cash book Dr. balance'},
            {'k': 'Pass book Dr. balance', 'v': 'Overdraft = Cash book Cr. balance'},
            {'k': 'Golden question', 'v': 'Does the starting record show more because of this item? More → deduct; less → add'},
            {'k': 'From CB Dr.', 'v': '+ unpresented cheques, + bank credits only; − uncleared deposits, − bank debits only'},
            {'k': 'From PB Cr.', 'v': 'Opposite of the CB Dr. signs'},
            {'k': 'Overdraft start', 'v': 'All signs reverse; label answer as overdraft'},
            {'k': 'Adjusted cash book', 'v': 'Own errors and omissions only; balance goes to the balance sheet'},
            {'k': 'Wrong-side entry', 'v': 'Effect = 2 × amount'},
        ],
        'viva': [
            V('v1', 'What is a bank reconciliation statement, and why is it prepared?',
              'A bank reconciliation statement is a statement prepared by the account holder on a particular date which starts from the cash book bank balance, lists every cause of difference and arrives at the pass book balance, so the two are reconciled. It is prepared to detect errors and frauds, as an internal control, to find out delays in clearing of cheques, and to know the true bank balance.',
              [P('p1', 'Statement that reconciles / explains the difference between cash book and pass book balances', 4, 'cash book', 'pass book|bank statement', 'reconcil|explain difference|differenc|agree|match', min=3),
               P('p2', 'Prepared by the account holder, as on a particular date', 2, 'account holder|business|customer|firm|ourselves|depositor', 'particular date|on a date|given date|specific date|certain date|date', min=1),
               P('p3', 'Purpose: detect errors and frauds / internal control', 2, 'error|fraud|mistake|embezzl|internal control|misappropriat', min=1),
               P('p4', 'Purpose: show delays in clearing and the true bank balance', 2, 'delay|true balance|correct balance|actual balance|real balance|true position|clearing|clearance', min=1)], 'c2'),
            V('v2', 'Why does a credit balance in the pass book mean the same thing as a debit balance in the cash book?',
              'Because the two records are kept by opposite parties. The pass book is the bank\'s copy of the customer\'s account; for the bank the customer\'s money is a liability, so it shows a credit balance. In the customer\'s cash book the bank owes that money, so the bank is like a debtor, an asset, and the balance is a debit.',
              [P('p1', 'Pass book is the bank\'s record / copy of the customer\'s account', 3, 'bank record|bank copy|bank book|bank s book|kept by bank|prepared by bank|maintained by bank|copy customer account|bank ledger|books of bank|bank side|bank view'),
               P('p2', 'For the bank the deposit is a liability — credit', 3, 'bank liability|liability for bank|liability to bank|liability of bank|liability in bank|bank owe|owes customer|owe customer|customer creditor|customer is a creditor|creditor of bank|credits us|bank payable|bank credit'),
               P('p3', 'For the customer the bank is a debtor / asset — debit', 4, 'bank debtor|bank like debtor|bank is a debtor|bank owe|owes us|owe us|customer asset|business asset|our asset|asset for us|asset for customer|asset for business|asset to us|asset to customer|asset to business|debtor asset|bank receivable')], 'c1'),
            V('v3', 'Starting with the debit balance as per cash book, how do you treat cheques issued but not presented, and cheques deposited but not cleared?',
              'Starting with the debit balance as per cash book, we add cheques issued but not yet presented, because the cash book has already been reduced by them but the bank has not paid them. We deduct cheques deposited but not yet cleared, because the cash book has already been increased but the bank has not credited them.',
              [P('p1', 'Cheques issued but not presented are added', 4, 'add cheque issu|add issu|issu not present add|issu not present ad|issu yet present add|issu but not present add|add unpresent|unpresent add|unpresent cheque add|add back cheque issu|added back issu|issu not present plus|plus issu|issu add'),
               P('p2', 'Cheques deposited but not cleared are deducted', 4, 'deduct cheque deposit|deduct deposit|subtract cheque deposit|subtract deposit|less cheque deposit|minus cheque deposit|deposit not clear deduct|deposit not clear subtract|deposit not clear less|deposit yet clear deduct|deposit yet clear subtract|deduct uncleared|subtract uncleared|uncleared deduct|uncleared subtract|uncleared cheque deduct|uncleared cheque subtract|deposit not credit deduct|deposit not credit subtract|deposit deduct|deposit subtract|less uncleared|minus uncleared'),
               P('p3', 'Reason: the cash book has already recorded them; the bank has not', 2, 'already|not yet record|not paid|bank not|bank has not|bank hasn t|bank hasnt|bank yet|not credit|not debit|not record', min=1)], 'c4'),
            V('v4', 'What are the main causes of difference between the cash book and the pass book balance?',
              'There are three groups of causes. First, timing differences, such as cheques issued but not presented and cheques deposited but not cleared. Second, transactions recorded by the bank first, like bank charges, interest, dividends collected, direct deposits and standing instruction payments. Third, errors made either in the cash book or by the bank.',
              [P('p1', 'Timing differences (unpresented cheques, uncleared deposits)', 4, 'timing|time gap|time lag|different time|different date|delay|unpresent|not present|uncleared|not clear', min=1),
               P('p2', 'Items recorded by the bank first (charges, interest, collections, direct deposits, standing instructions)', 3, 'bank charg|interest|dividend|direct deposit|direct payment|standing instruct|collect|emi|bank record first|bank first|recorded by bank|only in pass book', min=1),
               P('p3', 'Errors in the cash book or by the bank', 3, 'error|mistake|wrong|omission|omitted|casting|overcast|undercast', min=1)], 'c3'),
            V('v5', 'In the adjusted cash book method, which items go into the adjusted cash book and which remain in the bank reconciliation statement?',
              'The adjusted cash book takes the business\'s own errors and omissions — bank charges, interest, direct deposits and payments, dishonoured cheques and mistakes in the cash book. The bank reconciliation statement then keeps only timing differences, that is cheques issued but not presented and cheques deposited but not cleared, and errors made by the bank. The adjusted cash book balance is shown in the balance sheet.',
              [P('p1', 'Adjusted cash book: own errors and omissions (charges, interest, direct items, dishonour, cash-book mistakes)', 4, 'adjusted cash book|amended cash book|corrected cash book|cash book adjust|cash book corrected|correct cash book|correct the cash book', 'omission|omitted|business own|business s own|business error|errors of the business|mistakes in the cash book|errors in the cash book|cash book mistake|cash book error'),
               P('p2', 'BRS keeps timing differences and the bank\'s own errors', 4, 'timing|unpresent|not present|uncleared|not clear|not yet present|not yet clear|time gap', 'bank error|bank s error|error by bank|errors by bank|bank mistake|mistake by bank|bank wrong|wrongly by bank|bank s own|bank own|errors made by the bank|error made by the bank|errors of the bank|error of the bank', 'brs|reconciliation statement|remain|stay|keep|left|kept'),
               P('p3', 'Adjusted balance goes to the balance sheet', 2, 'balance sheet', 'adjusted balance|adjusted cash book balance|amended balance|amended cash book balance|corrected balance|corrected cash book balance|adjusted figure|corrected figure')], 'c6'),
            V('v6', 'You start a reconciliation from an overdraft as per cash book. How do the signs change, and how would you treat an unpresented cheque?',
              'When we start from an overdraft, the overdraft is like a negative balance, so all the signs reverse compared with a favourable balance. An unpresented cheque is deducted from the cash book overdraft, because the bank has not yet paid it and so the bank\'s overdraft is smaller.',
              [P('p1', 'All signs reverse when starting from an overdraft', 4, 'revers|opposite|flip|interchang|swap|change|negative', min=1),
               P('p2', 'Unpresented cheque is deducted from the overdraft', 4, 'unpresent cheque deduct|unpresent deduct|deduct unpresent|unpresent cheque subtract|subtract unpresent|unpresent subtract|unpresent cheque less|cheque deduct|deduct cheque|deducted from the overdraft|deduct from overdraft|subtract from overdraft|reduce overdraft|reduces overdraft|less from overdraft|subtracted from the overdraft|not present deduct|not present subtract|not presented is deducted|not presented is subtracted|unpresent cheque minus|minus unpresent'),
               P('p3', 'Reason: bank has not paid it, so the bank\'s overdraft is smaller', 2, 'smaller|less overdraft|lower overdraft|overdraft less|overdraft lower|not paid|not yet paid|bank not paid|bank hasn t paid|bank has not paid|not yet debit|not debit', min=1)], 'c4'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Shinde Motors — year-end reconciliation', 'difficulty': 'hard',
            'case': ('Shinde Motors closes its books on 31 March 2027. On that date its cash book shows a debit bank balance of ₹2,65,000, while the bank statement shows a credit balance of ₹2,57,500. '
                     'On checking: (a) a customer paid ₹30,000 directly into the bank — not yet recorded; (b) bank charges ₹1,500 appear only in the statement; (c) a customer\'s cheque of ₹18,000 deposited in March was dishonoured — not yet recorded; '
                     '(d) cheques issued ₹52,000 had not been presented; (e) cheques deposited ₹70,000 had not been credited.'),
            'mcqs': [
                M('k1a', 'Which items should be passed through the adjusted cash book?', ['(a), (b) and (c)', '(d) and (e)', '(a) to (e)', '(b) only'], 0,
                  'Direct deposit, bank charges and dishonour are the business\'s own omissions; (d) and (e) are timing differences that stay in the BRS.', 'c6', 'moderate'),
                M('k1b', 'What is the adjusted cash book balance?', [R(k_adj), '₹2,93,500', '₹2,77,000', '₹2,45,500'], 0,
                  f'2,65,000 + 30,000 − 1,500 − 18,000 = {R(k_adj)}.', 'c6', 'hard', '265000+30000-1500-18000'),
                M('k1c', 'Starting from the adjusted balance, what is the pass book balance as per the BRS?', [R(k_pb), '₹2,93,500', '₹2,75,500', '₹2,23,500'], 0,
                  f'{R(k_adj)} + unpresented 52,000 − uncleared 70,000 = {R(k_pb)}, which agrees with the bank statement.', 'c4', 'hard', '275500+52000-70000'),
                M('k1d', 'At what figure is the bank balance shown in the balance sheet on 31 March 2027?', [R(k_adj), '₹2,57,500', '₹2,65,000', '₹2,95,000'], 0,
                  'The balance sheet shows the adjusted cash book balance — the correct balance as per the books, not the bank statement figure.', 'c6', 'moderate', '265000+30000-1500-18000'),
            ]}],
    }
