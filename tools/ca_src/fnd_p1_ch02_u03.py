"""CA Foundation · Paper 1 · Chapter 2 · Unit 3 Trial Balance (original content)."""
from lib import *
from shared import kavya_entries

UID = 'fnd-p1-ch02-u03'


import copy
from ca_viva import VIVA, P, ALT


def viva():
    """Viva from ca_viva.py with key points re-tuned in the second review for the negation-aware matcher
    (swapped-term answers must score < 80%; natural paraphrases >= 80%)."""
    v = copy.deepcopy(VIVA[UID]); q = {x['id']: x for x in v}

    def put(vid, pt): q[vid]['points'] = [pt if p['id'] == pt['id'] else p for p in q[vid]['points']]
    # "total-cum-balance method is the most popular" contains every word of "balance method is the most popular",
    # so the key point alone cannot separate them: the question now also asks why, and the reason (or that the
    # other methods are used less) is a separate point the swapped answer cannot hit.
    q['v2']['q'] = 'Name the methods of preparing a trial balance. Which one is used most, and why?'
    q['v2']['model'] = ('There are three methods: the total method, the balance method, and the total-cum-balance method. '
                        'The balance method is the most commonly used, because final accounts are prepared from balances; the other two are lengthier and used less.')
    for pid, w in (('p1', 1), ('p2', 1), ('p3', 1)):
        for p in q['v2']['points']:
            if p['id'] == pid: p['w'] = w
    q['v2']['points'].append(P('p5', 'Why: final accounts are prepared from balances (the other methods are lengthier, used less)', 3,
        'final account prepar balanc|final account prepar from balanc|final account need balanc|final account based balanc|'
        'final account made from balanc|final statement prepar balanc|balanc need final account|balanc needed final account|balanc used final account|'
        'total method lengthy|total method long|total method less|total method rarely|other less|other two less|other method less|rarely used|seldom used|'
        'lengthy|lengthier|less used|used less|less common|less popular|time consuming'))
    put('v2', P('p4', 'Balance method is used most / for final accounts', 4,
                'balanc most|balanc common|balanc popular|balanc wide|balanc general|balanc usual|balanc prefer|balanc used most|balanc use most|balanc normal|balanc mainly|balanc frequent|most balanc|most common balanc|commonly used balanc|commonly use balanc|usual balanc|popular balanc|prefer balanc|general balanc'))
    put('v5', P('p1', 'Sales returns — debit', 3, 'sales return debit|sale return debit|return inward debit|returns inward debit|debit sales return|debit side sales return|debit side show sale return|debit sale return drawing|sale return drawing debit|sale return drawing go debit'))
    put('v5', P('p2', 'Bank overdraft — credit', 3, 'overdraft credit|overdraft outstand credit|overdraft outstand expens credit|overdraft outstand expens go credit|overdraft outstand go credit|credit bank overdraft|credit side bank overdraft|credit side show bank overdraft|credit overdraft'))
    put('v5', P('p3', 'Drawings — debit', 2, 'drawing debit|debit drawing|debit side drawing|debit side sale return drawing|debit sale return drawing|return drawing debit|drawing go debit'))
    put('v5', P('p4', 'Outstanding expenses — credit', 2, 'outstanding expense credit|outstanding credit|credit outstanding|credit side outstanding|credit side bank overdraft outstand|credit bank overdraft outstand|outstand expens go credit'))
    return v


def tb_block(rows, date, title=None, diff=None):
    """rows: (account, 'dr'|'cr', amount)"""
    b = {'t': 'tb', 'date': date, 'rows': [{'ac': a, s: v} for a, s, v in rows]}
    if title: b['title'] = title
    if diff is not None: b['diff'] = diff
    return b


def build():
    E = kavya_entries()
    accs = []
    for e in E:
        for l in e['lines']:
            if l['ac'] not in accs: accs.append(l['ac'])
    # balance method
    c1 = Checks()
    bal_rows = []
    for a in accs:
        b = ledger_balance(E, a)
        if b: bal_rows.append((a, 'dr' if b > 0 else 'cr', abs(b)))
    tdr = sum(v for _, s, v in bal_rows if s == 'dr'); tcr = sum(v for _, s, v in bal_rows if s == 'cr')
    c1.add('194100+111440+66500+38000+900+3500+2000+18000+12000', 'Total of debit balances')
    c1.add('400000+45000+1440', 'Total of credit balances')
    # total method
    tot_rows = []
    for a in accs:
        d = sum(l.get('dr', 0) for e in E for l in e['lines'] if l['ac'] == a)
        c = sum(l.get('cr', 0) for e in E for l in e['lines'] if l['ac'] == a)
        tot_rows.append([a, inr(d) if d else '', inr(c) if c else ''])
    gt = sum(l.get('dr', 0) for e in E for l in e['lines'])
    tot_rows.append(['Total', inr(gt), inr(gt)])
    c1.add('400000+250000+72000+45000+38000+72000+45000+3500+2000+30000', 'Total of all journal debits = total method column total')
    tot_tbl = table(['Account', 'Dr total (₹)', 'Cr total (₹)'], tot_rows, num=[1, 2], total=True, title='Total method (each side of every account)')

    # Illustration 2: capital as balancing figure
    bal2 = [('Cash in hand', 'dr', 18500), ('Bank', 'dr', 142000), ('Opening stock', 'dr', 65000), ('Purchases', 'dr', 480000), ('Sales', 'cr', 720000),
            ('Sales returns', 'dr', 12000), ('Purchase returns', 'cr', 9000), ('Wages', 'dr', 38000), ('Salaries', 'dr', 96000), ('Rent', 'dr', 60000),
            ('Furniture', 'dr', 75000), ('Machinery', 'dr', 240000), ('Sundry debtors', 'dr', 115000), ('Sundry creditors', 'cr', 88000), ('Bank loan', 'cr', 150000),
            ('Interest on bank loan', 'dr', 13500), ('Drawings', 'dr', 36000), ('Commission received', 'cr', 7500), ('Insurance', 'dr', 9000)]
    c2 = Checks()
    d2 = c2.add('18500+142000+65000+480000+12000+38000+96000+60000+75000+240000+115000+13500+36000+9000', 'Total debit balances')
    k2 = c2.add('720000+9000+88000+150000+7500', 'Credit balances other than capital')
    cap2 = c2.add('1400000-974500', 'Capital (balancing figure)')
    tb2 = tb_block(bal2 + [('Capital (balancing figure)', 'cr', cap2)], '31 March 2027', 'Trial Balance of Sunrise Traders as at 31 March 2027')

    # Illustration 3 / Q3: redraft a wrong trial balance
    correct = [('Capital', 'cr', 200000), ('Drawings', 'dr', 24000), ('Machinery', 'dr', 120000), ('Furniture', 'dr', 60000), ('Opening stock', 'dr', 40000),
               ('Purchases', 'dr', 250000), ('Sales', 'cr', 410000), ('Sales returns', 'dr', 8000), ('Purchase returns', 'cr', 5000), ('Sundry debtors', 'dr', 120000),
               ('Sundry creditors', 'cr', 70000), ('Bank overdraft', 'cr', 35000), ('Wages', 'dr', 30000), ('Outstanding wages', 'cr', 4000), ('Rent', 'dr', 24000),
               ('Prepaid rent', 'dr', 2000), ('Discount received', 'cr', 3000)]
    cash = sum(v for _, s, v in correct if s == 'cr') - sum(v for _, s, v in correct if s == 'dr')
    correct.insert(0, ('Cash in hand', 'dr', cash))
    wrong_side = {'Drawings', 'Sales returns', 'Bank overdraft', 'Outstanding wages', 'Prepaid rent', 'Discount received'}
    flip = {'dr': 'cr', 'cr': 'dr'}
    wrong = [(a, flip[s] if a in wrong_side else s, v) for a, s, v in correct]
    wd = sum(v for _, s, v in wrong if s == 'dr'); wc = sum(v for _, s, v in wrong if s == 'cr')
    c3 = Checks()
    c3.add('727000-(24000+120000+60000+40000+250000+8000+120000+30000+24000+2000)', 'Cash in hand (makes the corrected trial balance agree)')
    c3.add('727000', 'Corrected trial balance total (each side)')
    c3.add(f'{wc}-{wd}', "Difference in the junior's trial balance")
    wrong_tb = tb_block(wrong, '31 March 2027', "Trial balance as prepared by the junior (does not agree)", diff=abs(wd - wc))
    right_tb = tb_block(correct, '31 March 2027', 'Corrected Trial Balance as at 31 March 2027')

    # Q3: a different wrong trial balance (Pooja Traders), so the question is not the worked illustration
    q_correct = [('Cash in hand', 'dr', 91000), ('Capital', 'cr', 250000), ('Drawings', 'dr', 30000), ('Building', 'dr', 150000),
                 ('Furniture', 'dr', 45000), ('Opening stock', 'dr', 55000), ('Purchases', 'dr', 310000), ('Sales', 'cr', 460000),
                 ('Sales returns', 'dr', 6000), ('Purchase returns', 'cr', 7000), ('Sundry debtors', 'dr', 95000), ('Sundry creditors', 'cr', 82000),
                 ('Bank overdraft', 'cr', 28000), ('Salaries', 'dr', 42000), ('Outstanding salaries', 'cr', 3500), ('Insurance', 'dr', 9000),
                 ('Prepaid insurance', 'dr', 1500), ('Commission received', 'cr', 4000)]
    q_wrong_side = {'Drawings', 'Sales returns', 'Purchase returns', 'Bank overdraft', 'Outstanding salaries', 'Prepaid insurance', 'Commission received'}
    q_wrong = [(a, flip[s] if a in q_wrong_side else s, v) for a, s, v in q_correct]
    qd = sum(v for _, s, v in q_wrong if s == 'dr'); qc = sum(v for _, s, v in q_wrong if s == 'cr')
    q_total = sum(v for _, s, v in q_correct if s == 'cr')
    assert q_total == sum(v for _, s, v in q_correct if s == 'dr')
    c4 = Checks()
    c4.add(f"{q_total}-(" + '+'.join(str(v) for a, s, v in q_correct if s == 'dr' and a != 'Cash in hand') + ")", 'Cash in hand (makes the corrected trial balance agree)')
    c4.add('+'.join(str(v) for _, s, v in q_correct if s == 'cr'), 'Corrected trial balance total (each side)')
    c4.add(f'{qc}-{qd}', "Difference in the junior's trial balance")
    q_wrong_tb = tb_block(q_wrong, '31 March 2027', "Trial balance as prepared by the junior (does not agree)", diff=abs(qd - qc))
    q_right_tb = tb_block(q_correct, '31 March 2027', 'Corrected Trial Balance as at 31 March 2027')

    # Q1
    bal_q1 = [('Cash', 'dr', 12400), ('Bank', 'dr', 86600), ('Purchases', 'dr', 315000), ('Sales', 'cr', 498000), ('Carriage inwards', 'dr', 7200), ('Salaries', 'dr', 54000),
              ('Office rent', 'dr', 36000), ('Electricity', 'dr', 8400), ('Debtors', 'dr', 72000), ('Creditors', 'cr', 41000), ('Computers', 'dr', 90000),
              ('Opening stock', 'dr', 28000), ('Interest received', 'cr', 2600), ('Drawings', 'dr', 30000), ('Loan from Ms. Sen', 'cr', 60000)]
    q1c = Checks()
    q1c.add('12400+86600+315000+7200+54000+36000+8400+72000+90000+28000+30000', 'Total debit balances')
    q1c.add('498000+41000+2600+60000', 'Credit balances other than capital')
    capq1 = q1c.add('739600-601600', 'Capital (balancing figure)')
    tbq1 = tb_block(bal_q1 + [('Capital (balancing figure)', 'cr', capq1)], '31 March 2027', 'Trial Balance of Raghav & Co. as at 31 March 2027')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 3, 'title': 'Trial Balance',
        'outcomes': ['State what a trial balance is, why it is prepared and why it is a statement, not an account.', 'Prepare a trial balance by the total method, the balance method and the combined method.',
                     'Place each kind of balance on the correct side, including tricky items like returns, outstanding and prepaid expenses.', 'Explain which errors a trial balance cannot reveal and how a suspense account is used when it does not agree.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 40}, 'prereq': ['fnd-p1-ch02-u02'],
                 'exam_tip': '"Redraft the trial balance" and "prepare a trial balance with capital as the balancing figure" are favourite short questions.'},
        'concepts': [
            {'id': 'c1', 'title': 'What a trial balance is', 'body': ['A list of all ledger accounts with their debit and credit totals or balances, prepared on a particular date. Because every debit has an equal credit, the two columns must agree.',
                                                                    'Objectives: test the arithmetical accuracy of posting and balancing; give a summary of the ledger; and provide the base for preparing the financial statements.',
                                                                    'It is a statement, not an account — it has no "To" and "By" and is not part of the double entry.'],
             'analogy': 'A class register check at the end of the day: if the boys plus girls do not equal the total, someone was counted wrongly. If it does match, it still does not prove everyone sat in the right seat.',
             'work': 'In audit and accounting work the trial balance is the starting document. Each line is "mapped" to a line in the balance sheet or the profit and loss statement.'},
            {'id': 'c2', 'title': 'Three methods', 'body': ['Total method — write the total of each side of every account. Quick (no balancing needed), but long.',
                                                           'Balance method — write only the balance of each account on its side. This is the method used for preparing final accounts and in most exam questions.',
                                                           'Total-cum-balance method — show both totals and balances in four columns. Rarely used in practice because it is lengthy.'],
             'blocks': [tot_tbl], 'analogy': 'Total method shows every ball bowled; balance method shows only the final score.', 'work': 'Software prints the trial balance in the balance method by default; some also offer an "opening + Dr + Cr + closing" view, which is the combined method in a modern form.'},
            {'id': 'c3', 'title': 'Which side does it go on?', 'body': ['Debit side: assets, expenses, losses, drawings, debtors, purchases, sales returns, opening stock, prepaid expenses, accrued income.',
                                                                      'Credit side: capital, liabilities, incomes, gains, creditors, sales, purchase returns, bank overdraft, outstanding expenses, income received in advance, provisions.',
                                                                      'Closing stock normally appears outside the trial balance as an adjustment — unless it has already been adjusted (then it is shown on the debit side and purchases are reduced).'],
             'analogy': 'Ask: does the business own it or spend on it (debit), or does it owe it or earn it (credit)?', 'work': 'A prepaid rent shown on the credit side or a bank overdraft shown as an asset will make the balance sheet wrong even if totals somehow agree.'},
            {'id': 'c4', 'title': 'Limitations: agreement is not proof', 'body': ['These errors do not disturb the agreement: a transaction completely omitted; a wrong amount written in the journal and posted on both sides; posting to the wrong account but on the correct side (error of commission); wrong classification such as an asset debited to an expense (error of principle); and errors that cancel each other (compensating errors).',
                                                                                 'Errors that do cause a difference: posting on the wrong side, posting only one side, wrong totalling or balancing of an account, or omitting a balance from the trial balance.'],
             'analogy': 'A balanced scale tells you both pans weigh the same — not that you weighed the right things.', 'work': 'Auditors never rely on an agreed trial balance alone; they still test transactions with documents for exactly these hidden errors.'},
            {'id': 'c5', 'title': 'Suspense account', 'body': ['If the trial balance does not agree and the accounts must still be prepared, the difference is put to a Suspense Account so the totals agree temporarily.',
                                                             'As errors are found, rectifying entries are passed through the suspense account until it closes (Unit 6). A suspense balance left at the year end is shown in the balance sheet but should be investigated.'],
             'analogy': 'A "lost and found" box: you park the unexplained amount there until you find where it belongs.', 'work': 'An unexplained suspense balance is a serious audit observation — it means the books contain unidentified errors.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Kavya Traders: balance method', 'difficulty': 'core', 'minutes': 10,
             'q': 'Prepare the trial balance of Kavya Traders as at 30 April 2026 from the ledger balances (Units 1 and 2), using the balance method. Also show the total method.',
             'solution': [tb_block(bal_rows, '30 April 2026', 'Trial Balance of Kavya Traders as at 30 April 2026 (balance method)'), tot_tbl,
                          p(f'Both methods agree: balances ₹{inr(tdr)} on each side; totals ₹{inr(gt)} on each side. Mehta & Co. and Rohan have no balance, so they do not appear in the balance method.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Capital as the balancing figure', 'difficulty': 'core', 'minutes': 10,
             'q': 'From the following balances of Sunrise Traders on 31 March 2027, prepare a trial balance, taking capital as the balancing figure: Cash in hand ₹18,500; Bank ₹1,42,000; Opening stock ₹65,000; Purchases ₹4,80,000; Sales ₹7,20,000; Sales returns ₹12,000; Purchase returns ₹9,000; Wages ₹38,000; Salaries ₹96,000; Rent ₹60,000; Furniture ₹75,000; Machinery ₹2,40,000; Sundry debtors ₹1,15,000; Sundry creditors ₹88,000; Bank loan ₹1,50,000; Interest on bank loan ₹13,500; Drawings ₹36,000; Commission received ₹7,500; Insurance ₹9,000.',
             'solution': [tb2, wn('Capital', f'Total debits ₹{inr(d2)} − other credits ₹{inr(k2)} = ₹{inr(cap2)}.')], 'checks': c2},
            {'id': 'i3', 'title': 'Redrafting a wrong trial balance', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'A junior prepared the trial balance below and it does not agree. Redraft it correctly.',
             'given': [wrong_tb],
             'solution': [right_tb, ul(['Drawings reduce capital — debit.', 'Sales returns reduce sales — debit.', 'Bank overdraft is a liability — credit.', 'Outstanding wages is a liability — credit.', 'Prepaid rent is an asset — debit.', 'Discount received is a gain — credit.'])],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Mapping the trial balance for the audit file', 'role': 'Articled assistant (audit)', 'situation': 'The client sends a trial balance with 240 ledger accounts. Your senior asks you to map each line to the financial statement heads and to flag anything odd.',
             'steps': ['Check that the trial balance totals agree and that the opening balances match last year\'s audited figures.', 'Map each ledger to a statement line (e.g. Sundry debtors → Trade receivables).',
                       'Flag balances on the "wrong" side: debit balances in creditors, credit balances in expenses, any suspense balance.', 'Prepare a lead schedule for each head that the audit team will test.'],
             'takeaway': 'Knowing the normal side of every balance is the fastest way to spot problems in a real trial balance.', 'think': 'An expense account like Repairs shows a credit balance. What could have happened?',
             'answer': 'A refund or reversal was larger than the expenses recorded, an income was posted to Repairs, or an entry was posted on the wrong side — each needs checking.'},
            {'id': 'j2', 'title': 'Month-end close in a company', 'role': 'Junior accountant in a finance team', 'situation': 'Your team closes the books on the third working day. The controller asks for the trial balance and an explanation of any suspense balance.',
             'steps': ['Run the trial balance from the system and confirm it agrees.', 'Review suspense or "clearing" accounts and trace every open item to its source.', 'Pass correcting entries and rerun the trial balance before reporting.'],
             'takeaway': 'Suspense accounts should be cleared every month — old unexplained items become very hard to trace.', 'think': 'Why is it risky to leave a small suspense balance of ₹300 unexplained?',
             'answer': 'It may be the net of two large errors that almost cancel each other — for example ₹50,300 and ₹50,000 — so the real misstatement could be much bigger.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'A trial balance is:', 'options': ['A statement', 'An account', 'A subsidiary book', 'A ledger'], 'answer': 0, 'explain': 'It lists balances to test accuracy; it is not part of the double entry.', 'concept': 'c1', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'Which item appears on the credit side of a trial balance?', 'options': ['Outstanding salary', 'Prepaid insurance', 'Sales returns', 'Drawings'], 'answer': 0, 'explain': 'Outstanding salary is a liability. The other three are debits.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Which error will NOT affect the agreement of the trial balance?', 'options': ['Credit sale to Mohan posted to Sohan\'s account', 'Purchases book under-cast by ₹500', 'Cash received from a debtor posted only to Cash account', 'Rent paid posted to the credit of Rent account'], 'answer': 0, 'explain': 'Posting to the wrong account on the correct side (error of commission) keeps debits equal to credits.', 'concept': 'c4', 'difficulty': 'moderate'},
            {'id': 'm4', 'q': 'Total debit balances are ₹6,48,000 and credit balances other than capital are ₹4,12,500. Capital is:', 'options': ['₹2,35,500', '₹10,60,500', '₹2,53,500', '₹4,12,500'], 'answer': 0, 'check': '648000-412500', 'explain': 'Capital = 6,48,000 − 4,12,500 = ₹2,35,500 (credit).', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'If the trial balance does not agree, the difference is temporarily placed in:', 'options': ['Suspense Account', 'Capital Account', 'Profit and Loss Account', 'Drawings Account'], 'answer': 0, 'explain': 'A suspense account holds the difference until the errors are located.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'Under which method of preparing a trial balance is balancing of accounts NOT needed?', 'options': ['Total method', 'Balance method', 'Total-cum-balance method', 'All methods need balancing'], 'answer': 0, 'explain': 'The total method uses each side\'s total; balances are not required.', 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'A trial balance shows debit total ₹5,62,300 and credit total ₹5,58,800. The suspense account will show:', 'options': ['₹3,500 credit balance', '₹3,500 debit balance', '₹11,21,100 credit balance', 'No balance'], 'answer': 0, 'check': '562300-558800', 'explain': 'The credit side is short by ₹3,500, so suspense is credited with ₹3,500 to make the totals agree.', 'concept': 'c5', 'difficulty': 'moderate'},
            {'id': 'm8', 'q': 'Closing stock usually appears in the trial balance:', 'options': ['Only when it has already been adjusted against purchases', 'Always on the credit side', 'Always on the debit side', 'Never, under any circumstances'], 'answer': 0, 'explain': 'Normally closing stock is an adjustment outside the trial balance. If it has been adjusted through purchases, it appears on the debit side.', 'concept': 'c3', 'difficulty': 'hard'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'tb',
             'q': 'Prepare the trial balance of Raghav & Co. as at 31 March 2027, taking capital as the balancing figure: Cash ₹12,400; Bank ₹86,600; Purchases ₹3,15,000; Sales ₹4,98,000; Carriage inwards ₹7,200; Salaries ₹54,000; Office rent ₹36,000; Electricity ₹8,400; Debtors ₹72,000; Creditors ₹41,000; Computers ₹90,000; Opening stock ₹28,000; Interest received ₹2,600; Drawings ₹30,000; Loan from Ms. Sen ₹60,000.',
             'model': [tbq1, wn('Capital', f'₹7,39,600 − ₹6,01,600 = ₹{inr(capq1)}')],
             'scheme': [{'id': 's1', 'pt': 'All assets and expenses (incl. drawings, carriage, opening stock) on the debit side', 'm': 2, 'skill': 'classification'},
                        {'id': 's2', 'pt': 'Sales, creditors, interest received and loan on the credit side', 'm': 2, 'skill': 'classification'},
                        {'id': 's3', 'pt': 'Capital ₹1,38,000 as balancing figure with working', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Proper heading with date; totals agree at ₹7,39,600', 'm': 1, 'skill': 'presentation'}],
             'checks': q1c,
             'remarks': ['A frequent slip is putting the loan on the debit side because the money came into the bank — the loan itself is a liability.', 'Write the date in the heading: "Trial Balance as at …". Missing headings lose presentation marks.'],
             'mistakes': ['Showing interest received as a debit.', 'Forgetting drawings, which then inflates capital.', 'Calling the statement "Trial Balance for the year ended".'], 'tips': ['List debits and credits in two passes so nothing is missed.', 'Show the capital working below the table.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': '"Agreement of the trial balance is not a conclusive proof of accuracy of the books." Explain with examples.',
             'model': [p('A trial balance only proves that total debits equal total credits. Several errors keep this equality and therefore stay hidden:'),
                       ul(['Error of complete omission — a credit purchase never recorded: neither side is affected.', 'Wrong amount in the journal — ₹5,400 written as ₹4,500 and posted to both accounts.',
                           'Error of commission — cash received from Ajay credited to Vijay\'s account.', 'Error of principle — purchase of machinery debited to Purchases account.',
                           'Compensating errors — Sales account over-cast by ₹1,000 and Wages account over-cast by ₹1,000.']),
                       p('Hence an agreed trial balance shows arithmetical accuracy only; it does not prove that transactions were recorded correctly.')],
             'scheme': [{'id': 's1', 'pt': 'Trial balance proves only arithmetical accuracy', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'At least three types of undisclosed errors named', 'm': 1.5, 'skill': 'concept'}, {'id': 's3', 'pt': 'An example for each type', 'm': 1.5, 'skill': 'application'}],
             'remarks': ['Examples carry half the marks — a list of names without examples scores poorly.'], 'mistakes': ['Including one-sided errors (which do affect the trial balance) in the list.'], 'tips': ['Use "Error type — example" on each line.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'tb',
             'q': 'The trial balance of Pooja Traders below was prepared by a junior and does not agree. Redraft it in the correct form.',
             'given': [q_wrong_tb], 'model': [q_right_tb],
             'scheme': [{'id': 's1', 'pt': 'Drawings, sales returns and prepaid insurance moved to debit', 'm': 1.5, 'skill': 'classification'},
                        {'id': 's2', 'pt': 'Purchase returns, bank overdraft, outstanding salaries and commission received moved to credit', 'm': 1.5, 'skill': 'classification'},
                        {'id': 's3', 'pt': 'Corrected totals agree at ₹8,34,500', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Heading and format', 'm': 1, 'skill': 'presentation'}],
             'checks': c4,
             'remarks': ['Strong answers redraw the whole trial balance rather than listing changes.'], 'mistakes': ['Changing amounts instead of sides.', 'Treating bank overdraft as cash at bank.', 'Leaving purchase returns on the debit side because purchases are a debit.'], 'tips': ['Tick each item as you place it so none is missed.']},
        ],
        'revision': {'summary': ['A trial balance lists ledger totals or balances on a date; the two columns must agree.', 'Methods: total, balance (most used), total-cum-balance.', 'Debit: assets, expenses, losses, drawings. Credit: capital, liabilities, incomes, gains.', 'Agreement does not prove accuracy: omission, commission, principle and compensating errors stay hidden.', 'Unexplained differences go to suspense until rectified.'],
                     'remember': ['It is a statement, not an account.', 'Outstanding expenses = credit; prepaid expenses = debit.', 'Closing stock is usually an adjustment outside the trial balance.'],
                     'traps': ["Don't put a bank overdraft on the debit side.", "Don't treat sales returns as income.", "Don't say an agreed trial balance proves the books are correct."]},
        'quickref': [{'k': 'Heading', 'v': 'Trial Balance of <name> as at <date>'}, {'k': 'Debit side', 'v': 'Assets, expenses, losses, drawings, purchases, sales returns, opening stock, prepaid expenses'},
                     {'k': 'Credit side', 'v': 'Capital, liabilities, incomes, gains, sales, purchase returns, outstanding expenses, bank overdraft'},
                     {'k': 'Errors not revealed', 'v': 'Omission, commission, principle, compensating'}, {'k': 'Capital (balancing figure)', 'v': 'Total debits − credits other than capital'}],
        'viva': viva(),
    }
