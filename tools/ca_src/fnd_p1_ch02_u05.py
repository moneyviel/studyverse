"""CA Foundation · Paper 1 · Chapter 2 · Unit 5 Cash Book (original content)."""
from lib import *

UID = 'fnd-p1-ch02-u05'


import copy
from ca_viva import VIVA, P, ALT


def viva():
    """Viva from ca_viva.py with key points re-tuned in the second review for the negation-aware matcher."""
    v = copy.deepcopy(VIVA[UID]); q = {x['id']: x for x in v}

    def put(vid, pt): q[vid]['points'] = [pt if p['id'] == pt['id'] else p for p in q[vid]['points']]
    put('v2', P('p4', 'Not posted to the ledger', 4, 'not posted|no posting|no ledger posting|not post|never post|isn t post|need not post|no need post|without posting|nothing is posted|not taken to ledger|not carried to ledger', min=1))
    return v


def cashbook(title, dr, cr, end, nxt, cols=('Discount', 'Cash', 'Bank'), balanced=(1, 2)):
    """dr/cr rows: (date, particulars, lf, [disc, cash, bank]). Adds balance c/d to balanced columns."""
    D = [{'date': d, 'part': p_, 'lf': lf, 'v': list(v)} for d, p_, lf, v in dr]
    C = [{'date': d, 'part': p_, 'lf': lf, 'v': list(v)} for d, p_, lf, v in cr]
    bal = [0] * len(cols); nxt_bal = [0] * len(cols)
    for i in balanced:
        sd = sum(r['v'][i] for r in D); sc = sum(r['v'][i] for r in C)
        bal[i] = sd - sc
    crow = [None] * len(cols); drow = [None] * len(cols)
    for i in balanced:
        if bal[i] >= 0: crow[i] = bal[i]
        else: drow[i] = -bal[i]
    if any(x for x in crow if x): C.append({'date': end, 'part': 'By Balance c/d', 'lf': '', 'v': [x or 0 for x in crow], 'bal': True})
    if any(x for x in drow if x): D.append({'date': end, 'part': 'To Balance c/d', 'lf': '', 'v': [x or 0 for x in drow], 'bal': True})
    return {'t': 'cashbook', 'title': title, 'cols': list(cols), 'balanced': list(balanced), 'dr': D, 'cr': C, 'next': {'date': nxt, 'v': bal}}


def build():
    # ---------- Illustration 1: three-column cash book ----------
    dr = [('Dec 1', 'To Balance b/d', '', (0, 25000, 120000)), ('Dec 3', 'To Ajit', '', (400, 0, 19600)), ('Dec 8', 'To Bank (C)', 'C', (0, 15000, 0)),
          ('Dec 14', 'To Sales', '', (0, 22000, 0)), ('Dec 17', 'To Cash (C)', 'C', (0, 0, 30000)), ('Dec 20', 'To Vikas', '', (300, 9700, 0))]
    cr = [('Dec 5', 'By Wages', '', (0, 8000, 0)), ('Dec 8', 'By Cash (C)', 'C', (0, 0, 15000)), ('Dec 11', 'By Sunita', '', (600, 0, 29400)),
          ('Dec 17', 'By Bank (C)', 'C', (0, 30000, 0)), ('Dec 24', 'By Rent', '', (0, 0, 12000)), ('Dec 28', 'By Bank Charges', '', (0, 0, 250)), ('Dec 31', 'By Drawings', '', (0, 5000, 0))]
    cb1 = cashbook('Three-column Cash Book of Meera Enterprises (December 2026)', dr, cr, 'Dec 31', 'Jan 1')
    c1 = Checks()
    c1.add('25000+15000+22000+9700-(8000+30000+5000)', 'Cash balance c/d')
    c1.add('120000+19600+30000-(15000+29400+12000+250)', 'Bank balance c/d')
    c1.add('20000-19600', 'Discount allowed to Ajit')
    c1.add('30000-29400', 'Discount received from Sunita')
    c1.add('400+300', 'Discount allowed total (debited to Discount Allowed A/c)')

    # ---------- Illustration 2: analytical petty cash book (imprest) ----------
    items = [('Jan 2', 'Postage stamps', 'PV1', 'post', 320), ('Jan 3', 'Auto fare to bank', 'PV2', 'conv', 450), ('Jan 4', 'Printing paper', 'PV3', 'stat', 780),
             ('Jan 5', 'Tea and snacks for staff meeting', 'PV4', 'welf', 640), ('Jan 6', 'Courier charges', 'PV5', 'post', 280), ('Jan 7', 'Bus fare', 'PV6', 'conv', 160), ('Jan 8', 'Cartridge refill', 'PV7', 'stat', 900)]
    keys = ['post', 'conv', 'stat', 'welf']
    rows = []
    T = {k: 0 for k in keys}; tot = 0
    for d, part, v, k, a in items:
        T[k] += a; tot += a
        rows.append([d, part, v, inr(a)] + [inr(a) if k == kk else '' for kk in keys])
    rows.append(['', 'Total payments', '', inr(tot)] + [inr(T[k]) for k in keys])
    pcb = table(['Date', 'Particulars', 'Voucher', 'Total (₹)', 'Postage & courier (₹)', 'Conveyance (₹)', 'Stationery (₹)', 'Staff welfare (₹)'], rows, num=[3, 4, 5, 6, 7], total=True,
                title='Analytical Petty Cash Book (imprest ₹5,000), week ending 8 January 2027', note='Received from the main cashier on 1 January: ₹5,000 (imprest).')
    c2 = Checks()
    c2.add('320+450+780+640+280+160+900', 'Total petty payments')
    bal2 = c2.add('5000-3530', 'Petty cash balance before reimbursement')
    c2.add('1470+3530', 'Balance after reimbursement = imprest')
    summ = table(['Step', 'Amount (₹)'], [['Imprest received on 1 January', '5,000'], ['Less: payments during the week', '3,530'], ['Balance in hand on 8 January (balance c/d)', inr(bal2)],
                                          ['Reimbursement from main cashier on 9 January', '3,530'], ['Petty cash available again', '5,000']], title='Balancing the petty cash book')

    # ---------- Illustration 3: card sales ----------
    c3 = Checks()
    com = c3.add('80000*1.5/100', 'Bank commission @1.5% on card sales of 80,000')
    c3.add('80000-1200', 'Net credit to bank account')
    j3 = journal([je('Feb 6', [('Bank A/c', 80000)], [('Sales A/c', 80000)], 'Being goods sold through debit and credit cards'),
                  je('Feb 6', [('Commission A/c', com)], [('Bank A/c', com)], 'Being commission charged by the bank on card sales')], 'Journal entries for card sales', 'j3')

    # ---------- Q1 ----------
    qdr = [('Jan 1', 'To Balance b/d', '', (0, 8400, 65000)), ('Jan 4', 'To Sales', '', (0, 14500, 0)), ('Jan 7', 'To Kapoor & Sons', '', (500, 0, 24500)),
           ('Jan 12', 'To Bank (C)', 'C', (0, 10000, 0)), ('Jan 18', 'To Nisha', '', (250, 9750, 0)), ('Jan 25', 'To Cash (C)', 'C', (0, 0, 12000))]
    qcr = [('Jan 3', 'By Purchases', '', (0, 6200, 0)), ('Jan 9', 'By Joshi Traders', '', (400, 0, 15600)), ('Jan 12', 'By Cash (C)', 'C', (0, 0, 10000)),
           ('Jan 15', 'By Salaries', '', (0, 0, 21000)), ('Jan 22', 'By Electricity', '', (0, 3300, 0)), ('Jan 25', 'By Bank (C)', 'C', (0, 12000, 0)), ('Jan 31', 'By Drawings', '', (0, 4000, 0))]
    qcb = cashbook('Three-column Cash Book of Tanvi Traders (January 2027)', qdr, qcr, 'Jan 31', 'Feb 1')
    q1c = Checks()
    qcash = q1c.add('8400+14500+10000+9750-(6200+3300+12000+4000)', 'Cash balance c/d')
    qbank = q1c.add('65000+24500+12000-(15600+10000+21000)', 'Bank balance c/d')
    q1c.add('25000-24500', 'Discount allowed to Kapoor & Sons')
    q1c.add('16000-15600', 'Discount received from Joshi Traders')

    q3c = Checks()
    q3com = q3c.add('120000*1.5/100', 'Commission @1.5% on 1,20,000')
    jq3 = journal([je('Mar 10', [('Bank A/c', 120000)], [('Sales A/c', 120000)], 'Being sales made through debit/credit cards'),
                   je('Mar 10', [('Commission A/c', q3com)], [('Bank A/c', q3com)], 'Being commission charged by the bank on card sales')], 'Journal', 'jq3')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 5, 'title': 'Cash Book',
        'outcomes': ['Explain why the cash book is both a book of original entry and a ledger account.', 'Prepare simple, double-column and three-column cash books, including contra entries and discount columns.',
                     'Post discount column totals and explain why discount columns are not balanced.', 'Maintain an analytical petty cash book on the imprest system.', 'Record sales made through debit and credit cards, including the bank\'s commission.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 50}, 'prereq': ['fnd-p1-ch02-u04'],
                 'exam_tip': 'In three-column cash books, marks are lost mostly on contra entries and on balancing the discount columns (which should only be totalled).'},
        'concepts': [
            {'id': 'c1', 'title': 'The cash book: journal and ledger in one', 'body': ['All cash and bank receipts and payments are first recorded in the cash book — so it is a book of original entry.',
                                                                                     'It also replaces the Cash Account and Bank Account in the ledger: its balances are the cash and bank balances. So it is a principal book too.',
                                                                                     'Receipts on the left (debit) side with "To …", payments on the right (credit) side with "By …" — exactly like a ledger account.'],
             'analogy': 'A wallet with a diary inside — every rupee in or out is written the moment it moves, and the wallet always tells you how much is left.', 'work': 'A surprise cash count compares the physical cash with the cash book balance. It is one of the oldest audit procedures and still used in branches and retail shops.'},
            {'id': 'c2', 'title': 'Kinds of cash book', 'body': ['Simple cash book — one amount column on each side (cash only).',
                                                                 'Double-column cash book — two columns each side: cash and discount, or cash and bank.',
                                                                 'Three-column cash book — discount, cash and bank columns on each side. This is the most common exam format.'],
             'analogy': 'Simple = one pocket. Double = two pockets. Three-column = two pockets plus a notepad for discounts.', 'work': 'Software keeps a separate "cash book" and "bank book" for every bank account — the three-column idea, stretched to as many columns as there are accounts.'},
            {'id': 'c3', 'title': 'Discount columns are only totalled', 'body': ['Discount allowed (debit side) and discount received (credit side) are not cash, so they are not balanced.',
                                                                                'The debit-side total is debited to Discount Allowed Account; the credit-side total is credited to Discount Received Account. Each customer or supplier is posted with cash plus discount.',
                                                                                'Only cash discount is entered here — trade discount never appears in any book.'],
             'analogy': 'The discount column is a memo — it keeps the details handy for posting later, like a sticky note on a page.', 'work': 'Large or unusual discounts allowed are a classic area for audit testing, because they can hide misappropriation of customer receipts.'},
            {'id': 'c4', 'title': 'Contra entries', 'body': ['When a transaction affects both the cash column and the bank column, it is recorded on both sides and marked "C" in the L.F. column.',
                                                            'Cash deposited into bank: debit side bank column "To Cash (C)" and credit side cash column "By Bank (C)". Cash withdrawn for office use: the reverse.',
                                                            'Contra entries are not posted to the ledger — both accounts are already in the cash book.'],
             'analogy': 'Moving money from your left pocket to your right pocket: both pockets change, you are not richer.', 'work': 'Unusual contra entries (large cash withdrawals and immediate re-deposits) can be a sign of window-dressing near the year end.'},
            {'id': 'c5', 'title': 'Petty cash and the imprest system', 'body': ['Small, frequent payments (postage, local travel, tea) are made by a petty cashier from a fixed amount called the imprest.',
                                                                              'At the end of the period the petty cashier shows vouchers for what was spent, and the main cashier reimburses exactly that amount — so the petty cashier starts again with the full imprest.',
                                                                              'An analytical petty cash book has a column for each type of expense; the column totals are posted to the expense accounts. The petty cash balance in hand is an asset.'],
             'analogy': 'Pocket money from your parents: they top you up to the same amount every week, but only after you show where the last week\'s money went.', 'work': 'Missing vouchers, many bills just below the approval limit and frequent "miscellaneous" items are red flags in petty cash reviews.'},
            {'id': 'c6', 'title': 'Sales through debit and credit cards', 'body': ['For the seller, a card sale works like a cash sale received in the bank: Bank A/c Dr, To Sales A/c, with the full sale value.',
                                                                                  'The bank\'s commission (a selling expense) is recorded separately: Commission A/c Dr, To Bank A/c. The commission rate depends on the bank\'s agreement — it is given in each question.'],
             'analogy': 'A delivery app that pays the restaurant the full bill and then deducts its fee — the restaurant records both.', 'work': 'Card settlement reports must be reconciled with the bank statement daily; differences usually come from commission, chargebacks or settlements arriving the next day.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Three-column cash book with contra entries', 'difficulty': 'moderate', 'minutes': 18,
             'q': 'Meera Enterprises, December 2026. Dec 1 — cash in hand ₹25,000, bank balance ₹1,20,000. Dec 3 — received a cheque from Ajit for ₹19,600 in full settlement of ₹20,000 and deposited it the same day. Dec 5 — paid wages in cash ₹8,000. Dec 8 — withdrew ₹15,000 from bank for office use. Dec 11 — paid Sunita ₹29,400 by cheque in full settlement of ₹30,000. Dec 14 — cash sales ₹22,000. Dec 17 — deposited ₹30,000 cash into bank. Dec 20 — received cash ₹9,700 from Vikas, discount allowed ₹300. Dec 24 — paid rent by cheque ₹12,000. Dec 28 — bank charges ₹250. Dec 31 — withdrew ₹5,000 cash for personal use. Prepare the three-column cash book.',
             'solution': [cb1, ul(['Discount allowed total ₹700 is debited to Discount Allowed A/c; discount received ₹600 is credited to Discount Received A/c.', 'Ajit is credited ₹20,000 (₹19,600 + ₹400) and Sunita debited ₹30,000 (₹29,400 + ₹600).', 'Contra entries (C) on 8 and 17 December are not posted to the ledger.'])],
             'checks': c1},
            {'id': 'i2', 'title': 'Analytical petty cash book on the imprest system', 'difficulty': 'core', 'minutes': 10,
             'q': 'The petty cashier of Orbit Solutions receives an imprest of ₹5,000 on 1 January 2027. Payments: Jan 2 postage stamps ₹320; Jan 3 auto fare to bank ₹450; Jan 4 printing paper ₹780; Jan 5 tea and snacks for a staff meeting ₹640; Jan 6 courier ₹280; Jan 7 bus fare ₹160; Jan 8 cartridge refill ₹900. Prepare the analytical petty cash book and show the reimbursement.',
             'solution': [pcb, summ, p('The column totals are posted to Postage & Courier ₹600, Conveyance ₹610, Stationery ₹1,680 and Staff Welfare ₹640 accounts.')], 'checks': c2},
            {'id': 'i3', 'title': 'Card sales and bank commission', 'difficulty': 'core', 'minutes': 5,
             'q': 'On 6 February 2027 a shop sold goods for ₹80,000 through debit and credit cards. The bank charges commission of 1.5% on card sales. Pass the journal entries.',
             'solution': [j3, p(f'The bank account finally increases by ₹{inr(80000 - com)}: ₹80,000 debited for the sales and ₹{inr(com)} credited for the commission.')], 'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Surprise cash count at a client\'s branch', 'role': 'Articled assistant (audit)', 'situation': 'You arrive unannounced at a retail branch at 10 a.m. Your senior asks you to count the cash and agree it with the cash book.',
             'steps': ['Ask the cashier to be present and count all cash, including the petty cash box, in front of them.', 'Write a denomination-wise count sheet and get it signed by the cashier.', 'Update the cash book up to the moment of the count and compare.',
                       'List IOUs or slips (staff advances not recorded) — they are not cash.', 'Report any difference immediately to your senior.'],
             'takeaway': 'The cash book balance is a claim; the counted cash is the evidence.', 'think': 'The cash book shows ₹48,500; you count ₹43,000 and find an unrecorded staff advance slip of ₹5,000. What is the position?',
             'answer': 'There is a shortage of ₹500, and an unrecorded advance of ₹5,000 that should be entered (Staff Advance Dr, To Cash). Both are reported.'},
            {'id': 'j2', 'title': 'Running an office petty cash box', 'role': 'Office administrator in a CA firm', 'situation': 'You hold an imprest of ₹10,000 and are asked for reimbursement every fortnight.',
             'steps': ['Pay only against a bill or a signed voucher showing the purpose.', 'Record each payment in the analytical columns the same day.', 'At the fortnight end, total the columns, count the cash and confirm cash + vouchers = imprest.', 'Submit the vouchers for approval and receive the exact amount spent.'],
             'takeaway': 'Imprest makes control simple: at any moment, cash in the box plus vouchers must equal the fixed imprest.', 'think': 'Imprest ₹10,000, vouchers ₹6,850, cash in box ₹3,050. Is there a problem?',
             'answer': 'Yes — vouchers plus cash = ₹9,900, so ₹100 is unaccounted for. It must be traced or reported.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'The cash book is treated as:', 'options': ['Both a book of original entry and a ledger', 'Only a book of original entry', 'Only a ledger account', 'A memorandum book not part of the accounts'], 'answer': 0, 'explain': 'Entries are first written in it and its balances replace the Cash and Bank accounts in the ledger.', 'concept': 'c1', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'Cash deposited into the bank is recorded in a three-column cash book as:', 'options': ['A contra entry on both sides', 'Only on the debit side in the cash column', 'Only on the credit side in the bank column', 'In the journal proper'], 'answer': 0, 'explain': 'It affects both the bank column (debit) and the cash column (credit) and is marked "C".', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'In a three-column cash book, the receipts-side discount column records:', 'options': ['Cash discount allowed to customers', 'Cash discount received from suppliers', 'Trade discount allowed', 'Trade discount received'], 'answer': 0, 'explain': 'Receipts from customers are on the debit side; any discount given to them is discount allowed.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm4', 'q': 'A customer owing ₹15,000 pays by cheque after deducting 2% cash discount. The bank column will show:', 'options': ['₹14,700', '₹15,000', '₹300', '₹15,300'], 'answer': 0, 'check': '15000*98/100', 'explain': 'Discount 2% of 15,000 = 300; cheque = ₹14,700. ₹300 goes to the discount column.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'Under the imprest system, the petty cashier is reimbursed:', 'options': ['The amount actually spent during the period', 'A fixed amount every period regardless of spending', 'The balance in hand', 'Double the amount spent'], 'answer': 0, 'explain': 'Reimbursing exactly what was spent restores the fixed imprest.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'Imprest ₹6,000. Payments during the week ₹4,275. The amount reimbursed at the week end is:', 'options': ['₹4,275', '₹1,725', '₹6,000', '₹10,275'], 'answer': 0, 'check': '4275', 'explain': 'The petty cashier is given back what was spent, ₹4,275, restoring ₹6,000.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'Commission charged by the bank on card sales is recorded as:', 'options': ['Commission A/c Dr. To Bank A/c', 'Bank A/c Dr. To Commission A/c', 'Sales A/c Dr. To Bank A/c', 'Commission A/c Dr. To Sales A/c'], 'answer': 0, 'explain': 'Commission is a selling expense deducted from the bank balance.', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'A credit balance in the bank column of the cash book means:', 'options': ['A bank overdraft', 'Cash at bank', 'Discount received', 'An error that must be corrected'], 'answer': 0, 'explain': 'More has been paid out of the bank than deposited — an overdraft, which is allowed. (A credit balance in the cash column is impossible.)', 'concept': 'c2', 'difficulty': 'moderate'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Prepare a three-column cash book of Tanvi Traders for January 2027: Jan 1 — cash in hand ₹8,400, bank balance ₹65,000. Jan 3 — bought goods for cash ₹6,200. Jan 4 — cash sales ₹14,500. Jan 7 — received a cheque from Kapoor & Sons for ₹24,500 in full settlement of ₹25,000, deposited the same day. Jan 9 — paid Joshi Traders ₹15,600 by cheque in full settlement of ₹16,000. Jan 12 — withdrew ₹10,000 from bank for office use. Jan 15 — paid salaries by cheque ₹21,000. Jan 18 — received cash ₹9,750 from Nisha, discount allowed ₹250. Jan 22 — paid the electricity bill in cash ₹3,300. Jan 25 — deposited ₹12,000 cash into bank. Jan 31 — withdrew ₹4,000 cash for personal use.',
             'model': [qcb, ul(['Discount allowed total ₹750 → Discount Allowed A/c (debit); discount received ₹400 → Discount Received A/c (credit).', 'Entries of 12 and 25 January are contra entries.'])],
             'scheme': [{'id': 's1', 'pt': 'Opening balances and receipts on the debit side in the right columns', 'm': 2, 'skill': 'posting'},
                        {'id': 's2', 'pt': 'Payments on the credit side in the right columns', 'm': 2, 'skill': 'posting'},
                        {'id': 's3', 'pt': 'Both contra entries on both sides, marked C', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's4', 'pt': 'Discounts ₹500, ₹250 (allowed) and ₹400 (received) in discount columns, totalled not balanced', 'm': 1, 'skill': 'concept'},
                        {'id': 's5', 'pt': f'Closing balances: cash ₹{inr(qcash)}, bank ₹{inr(qbank)}', 'm': 1.5, 'skill': 'balancing'}],
             'checks': q1c,
             'remarks': ['Many candidates record a contra entry on only one side.', 'Balancing the discount columns is a sign the concept is not clear — they should only be totalled.'],
             'mistakes': ['Entering the cheque from Kapoor & Sons in the cash column.', 'Writing the discount as a payment.', 'Forgetting to bring balances down on 1 February.'],
             'tips': ['Draw all six amount columns before you begin.', 'Tick each contra entry once you have written both sides.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Explain the imprest system of petty cash. State its advantages.',
             'model': [p('Under the imprest system a fixed sum (the imprest) is given to the petty cashier at the start of a period for small payments. At the end of the period the petty cashier submits the vouchers, and the main cashier reimburses the exact amount spent, so the imprest is restored.'),
                       ul(['Control: cash in hand plus vouchers must always equal the imprest.', 'Saves the main cashier\'s time and keeps the main cash book free of small items.', 'Analytical columns make posting to expense accounts easy (only totals are posted).', 'Regular review of vouchers discourages misuse; the imprest limits the amount at risk.'])],
             'scheme': [{'id': 's1', 'pt': 'Fixed amount advanced at the start', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Reimbursement of actual spending against vouchers', 'm': 1, 'skill': 'concept'}, {'id': 's3', 'pt': 'Any two advantages', 'm': 2, 'skill': 'concept'}],
             'remarks': ['Good answers mention that cash plus vouchers equals the imprest at any time.'], 'mistakes': ['Saying a fixed amount is reimbursed every period.'], 'tips': ['Define, then list advantages as bullets.']},
            {'id': 'q3', 'marks': 3, 'minutes': minutes(3), 'difficulty': 'core', 'pad': 'journal',
             'q': 'On 10 March 2027 a retailer sold goods for ₹1,20,000 through debit and credit cards. The bank charges commission at 1.5%. Pass the journal entries.',
             'model': [jq3], 'scheme': [{'id': 's1', 'pt': 'Bank debited and Sales credited with the full ₹1,20,000', 'm': 1.5, 'skill': 'classification'}, {'id': 's2', 'pt': 'Commission ₹1,800 debited, Bank credited', 'm': 1.5, 'skill': 'computation'}],
             'checks': q3c, 'remarks': ['Some candidates record sales net of commission — the sale is the full value; commission is an expense.'], 'mistakes': ['Debiting the customer instead of Bank.', 'Ignoring the commission.'], 'tips': ['Two entries: one for the sale, one for the commission.']},
        ],
        'revision': {'summary': ['The cash book records all cash and bank transactions and also acts as the Cash and Bank accounts.', 'Simple (cash), double-column (cash + discount or cash + bank), three-column (discount, cash, bank).',
                                 'Contra entries (C) affect cash and bank together; they are not posted to the ledger.', 'Discount columns are totalled and posted, never balanced.', 'Petty cash on imprest: reimburse exactly what was spent.', 'Card sales: Bank Dr To Sales (full value); Commission Dr To Bank.'],
                     'remember': ['Debit side = receipts ("To"); credit side = payments ("By").', 'Cash column can never have a credit balance; bank column can (overdraft).', 'Petty cash balance in hand is an asset.'],
                     'traps': ["Don't balance discount columns.", "Don't record trade discount in the cash book.", "Don't post contra entries to the ledger."]},
        'quickref': [{'k': 'Contra: cash into bank', 'v': 'Dr side bank column "To Cash (C)"; Cr side cash column "By Bank (C)"'}, {'k': 'Discount allowed total', 'v': 'Debited to Discount Allowed A/c'},
                     {'k': 'Discount received total', 'v': 'Credited to Discount Received A/c'}, {'k': 'Imprest', 'v': 'Reimbursement = amount spent; cash + vouchers = imprest'},
                     {'k': 'Card sale', 'v': 'Bank A/c Dr. To Sales A/c; Commission A/c Dr. To Bank A/c'}],
        'viva': viva(),
    }
