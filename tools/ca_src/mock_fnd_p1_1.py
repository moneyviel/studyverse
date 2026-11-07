"""StudyVerse practice paper 1 for CA Foundation Paper 1 (Accounting) in the ICAI pattern — NOT an ICAI paper.
Pilot scope: Chapter 2 Accounting Process (the built units). Pattern (from ICAI model test papers): 3 hours, 100 marks,
six questions of 20 marks, Question 1 compulsory, any four of the remaining five; Q1(a) is a set of true/false
statements with reasons.
Schema "ca-mock/1" — parts are: tf (statements), ref (a question from a unit's bank, "unit#qid"), q (a new question,
same fields as a unit question). Every figure in new questions is computed and re-checked by tools/ca_validate.py."""
from lib import *

MID = 'fnd-p1-m1'


def build():
    # ---------- new question: journal → ledger → trial balance (12 marks) ----------
    c6 = Checks()
    E = [
        je('Mar 1', [('Cash A/c', 150000)], [('Capital A/c', 150000)], 'Being business started with cash'),
        je('Mar 3', [('Purchases A/c', 60000)], [('Cash A/c', 60000)], 'Being goods bought for cash'),
        je('Mar 8', [('Cash A/c', 45000)], [('Sales A/c', 45000)], 'Being goods sold for cash'),
        je('Mar 12', [('Arun', 28000)], [('Sales A/c', 28000)], 'Being goods sold to Arun on credit'),
        je('Mar 18', [('Rent A/c', 8000)], [('Cash A/c', 8000)], 'Being rent for March paid'),
        je('Mar 25', [('Cash A/c', 20000)], [('Arun', 20000)], 'Being part payment received from Arun'),
        je('Mar 31', [('Drawings A/c', 5000)], [('Cash A/c', 5000)], 'Being cash withdrawn for personal use'),
    ]
    cash = c6.add('150000-60000+45000-8000+20000-5000', 'Cash balance on 31 March')
    sales = c6.add('45000+28000', 'Sales for March')
    arun = c6.add('28000-20000', 'Arun owes')
    c6.add(f'{cash}+{arun}+60000+8000+5000', 'Trial balance — debit total')
    c6.add(f'150000+{sales}', 'Trial balance — credit total')
    accts = ['Cash A/c', 'Capital A/c', 'Purchases A/c', 'Sales A/c', 'Arun', 'Rent A/c', 'Drawings A/c']
    TB = tb([(a.replace(' A/c', ''), ledger_balance(E, a)) for a in accts], '31 March 2027', 'Trial Balance of Dev Traders as at 31 March 2027')
    q6a = {'id': 'n1', 'marks': 12, 'minutes': minutes(12), 'difficulty': 'moderate', 'pad': 'journal',
           'q': ('Dev started Dev Traders on 1 March 2027. Transactions for March: Mar 1 — brought in cash ₹1,50,000 as capital; Mar 3 — bought goods for cash ₹60,000; '
                 'Mar 8 — sold goods for cash ₹45,000; Mar 12 — sold goods to Arun on credit ₹28,000; Mar 18 — paid rent ₹8,000; Mar 25 — received ₹20,000 from Arun; '
                 'Mar 31 — withdrew ₹5,000 for personal use. (i) Journalise the transactions. (ii) Post them to the Cash Account, Sales Account and Arun\'s Account and balance them. '
                 '(iii) Prepare the trial balance as at 31 March 2027.'),
           'model': [journal(E, 'Journal of Dev Traders (March 2027)', 'jn1')] + ledgers_from(E, ['Cash A/c', 'Sales A/c', 'Arun'], from_id='jn1') + [TB],
           'scheme': [
               {'id': 's1', 'pt': 'Seven journal entries with correct accounts debited and credited', 'm': 3, 'skill': 'classification'},
               {'id': 's2', 'pt': 'Narrations for the entries', 'm': 1, 'skill': 'presentation'},
               {'id': 's3', 'pt': f'Cash Account posted and balanced — {R(cash)} Dr', 'm': 2, 'skill': 'posting'},
               {'id': 's4', 'pt': f'Sales Account — {R(sales)} Cr; Arun\'s Account — {R(arun)} Dr', 'm': 2, 'skill': 'balancing'},
               {'id': 's5', 'pt': 'Trial balance lists every account on the correct side', 'm': 2, 'skill': 'classification'},
               {'id': 's6', 'pt': 'Trial balance totals agree at ₹2,23,000', 'm': 2, 'skill': 'computation'},
           ],
           'remarks': ['The trial balance must include every account, including capital, rent and drawings, not only the three accounts posted.',
                       'Sales Account shows both cash and credit sales; a few candidates leave out the cash sale because it is "already in cash".'],
           'mistakes': ['Treating drawings as an expense like rent.', 'Balancing Sales Account with a debit balance.', 'Writing "To" on the credit side of a ledger.'],
           'tips': ['Prepare the ledger in T-form with Date, Particulars, J.F. and Amount on each side.', 'Head the trial balance with the business name and the date.'],
           'checks': c6}

    # ---------- new question: analytical petty cash book (5 marks) ----------
    c5 = Checks()
    pays = [('May 3', 'Postage', 'Postage', 420), ('May 6', 'Printer paper and pens', 'Stationery', 860), ('May 10', 'Cartage on goods sold', 'Cartage', 1250),
            ('May 14', 'Auto fare to bank', 'Travel', 690), ('May 21', 'Courier charges', 'Postage', 310), ('May 28', 'Tea for staff meeting', 'Sundry', 540)]
    cols = ['Postage', 'Stationery', 'Cartage', 'Travel', 'Sundry']
    spent = c5.add('+'.join(str(x[3]) for x in pays), 'Total spent in May')
    left = c5.add(f'5000-{spent}', 'Balance in hand on 31 May')
    col_tot = {k: sum(x[3] for x in pays if x[2] == k) for k in cols}
    for k in cols: c5.add('+'.join(str(x[3]) for x in pays if x[2] == k) or '0', f'{k} column total')
    rows = [[d, part, inr(a)] + [inr(a) if h == k else '' for k in cols] for d, part, h, a in pays]
    rows.append(['', 'Total', inr(spent)] + [inr(col_tot[k]) for k in cols])
    pcb = table(['Date', 'Particulars', 'Total (₹)'] + [f'{k} (₹)' for k in cols], rows, num=[2, 3, 4, 5, 6, 7], total=True,
                title='Petty Cash Book (payments side) — May 2027')
    q5d = {'id': 'n2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
           'q': ('A business keeps its petty cash on the imprest system with an imprest of ₹5,000, received on 1 May 2027. Payments in May: May 3 postage ₹420; '
                 'May 6 printer paper and pens ₹860; May 10 cartage on goods sold ₹1,250; May 14 auto fare to the bank ₹690; May 21 courier charges ₹310; '
                 'May 28 tea for a staff meeting ₹540. Prepare an analytical petty cash book with columns for postage, stationery, cartage, travel and sundry expenses, '
                 'and show the balance and the reimbursement.'),
           'model': [pcb, wn('Balance and reimbursement', f'Imprest ₹5,000 − spent {R(spent)} = balance in hand {R(left)} (carried down). On 1 June the main cashier reimburses {R(spent)}, restoring the imprest to ₹5,000.')],
           'scheme': [
               {'id': 's1', 'pt': 'Each payment entered in the total column and the right analysis column', 'm': 2, 'skill': 'classification'},
               {'id': 's2', 'pt': f'Column totals, total spent {R(spent)}', 'm': 1, 'skill': 'computation'},
               {'id': 's3', 'pt': f'Balance in hand {R(left)} carried down', 'm': 1, 'skill': 'balancing'},
               {'id': 's4', 'pt': f'Reimbursement of {R(spent)} shown', 'm': 1, 'skill': 'presentation'},
           ],
           'remarks': ['Postage and courier charges belong in the same column.', 'Reimbursement equals the amount spent, not the balance in hand.'],
           'mistakes': ['Reimbursing the closing balance instead of the amount spent.', 'Putting cartage on goods sold under sundry expenses.'],
           'tips': ['Total every analysis column and check that they add up to the total column.'],
           'checks': c5}

    tf = [
        {'id': 't1', 's': 'Trade discount allowed on a purchase is debited to Discount Account in the books of the buyer.', 'answer': False,
         'reason': 'False. Trade discount is deducted on the invoice itself and is never recorded; the purchase is entered at the net price.'},
        {'id': 't2', 's': 'A contra entry in the cash book is not posted to the ledger.', 'answer': True,
         'reason': 'True. Both accounts affected — cash and bank — are already in the cash book, so no ledger posting is needed.'},
        {'id': 't3', 's': 'If the trial balance agrees, the books of account are free from errors.', 'answer': False,
         'reason': 'False. Errors of complete omission, principle, compensating errors and posting to a wrong account on the correct side do not affect agreement.'},
        {'id': 't4', 's': 'Goods taken by the proprietor for personal use are credited to Sales Account.', 'answer': False,
         'reason': 'False. Drawings Account is debited and Purchases Account is credited, at cost, because no sale has taken place.'},
        {'id': 't5', 's': 'Nominal accounts are not carried forward to the next year.', 'answer': True,
         'reason': 'True. Expenses, losses, incomes and gains are closed by transfer to the Trading or Profit and Loss Account at the year end.'},
        {'id': 't6', 's': 'A trader who deals in groceries records the credit purchase of a computer for office use in the purchases book.', 'answer': False,
         'reason': 'False. The purchases book records only credit purchases of goods dealt in; a credit purchase of an asset is recorded in the journal proper.'},
    ]
    ref = lambda u, q, m: {'kind': 'ref', 'ref': f'fnd-p1-ch02-u0{u}#{q}', 'marks': m}
    return {
        'schema': 'ca-mock/1', 'id': MID, 'level': 'foundation', 'paper': 'fnd-p1',
        'title': 'Accounting — Practice Paper 1', 'label': 'StudyVerse practice paper in ICAI pattern (not an ICAI paper)',
        'scope': 'Chapter 2 — Accounting Process (Units 1 to 6). More papers follow as more chapters are built.',
        'hours': 3, 'marks': 100, 'compulsory': ['Q1'], 'choose': 4,
        'rules': ['Question No. 1 is compulsory.', 'Answer any four questions from the remaining five questions.', 'Working notes should form part of the answer.',
                  'In this practice paper, each true/false statement carries 2 marks, given only for a correct verdict with a correct reason — as in ICAI marking, a bare True/False without a reason earns no marks.'],
        'questions': [
            {'id': 'Q1', 'marks': 20, 'parts': [
                {'id': 'a', 'kind': 'tf', 'marks': 12, 'q': 'Say whether each statement below is true or false, giving a reason for your answer.', 'items': tf},
                dict(ref(1, 'q2', 4), id='b'), dict(ref(4, 'q2', 4), id='c')]},
            {'id': 'Q2', 'marks': 20, 'parts': [dict(ref(1, 'q1', 6), id='a'), dict(ref(1, 'q3', 5), id='b'), dict(ref(2, 'q1', 6), id='c'), dict(ref(2, 'q3', 3), id='d')]},
            {'id': 'Q3', 'marks': 20, 'parts': [dict(ref(4, 'q1', 8), id='a'), dict(ref(4, 'q3', 4), id='b'), dict(ref(5, 'q1', 8), id='c')]},
            {'id': 'Q4', 'marks': 20, 'parts': [dict(ref(6, 'q1', 8), id='a'), dict(ref(6, 'q3', 5), id='b'), dict(ref(6, 'q2', 4), id='c'), dict(ref(5, 'q3', 3), id='d')]},
            {'id': 'Q5', 'marks': 20, 'parts': [dict(ref(3, 'q1', 6), id='a'), dict(ref(3, 'q3', 5), id='b'), dict(ref(3, 'q2', 4), id='c'), {'id': 'd', 'kind': 'q', 'marks': 5, 'question': q5d}]},
            {'id': 'Q6', 'marks': 20, 'parts': [{'id': 'a', 'kind': 'q', 'marks': 12, 'question': q6a}, dict(ref(2, 'q2', 4), id='b'), dict(ref(5, 'q2', 4), id='c')]},
        ],
    }


def write():
    import json, os
    path = os.path.join(ROOT, 'content', 'ca', 'foundation', 'mocks', MID + '.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(build(), f, ensure_ascii=False, indent=1)
    return path


# ---------- Auto-check data for the Write tab / paper marking ----------
# New questions (n1, n2): per scheme point kw (viva-matcher keyword groups, "|" = alternatives) + min, nums (figures that
# must appear), rows ([particular keywords, side, amount]: journal/trial balance dr|cr = column, ledger dr|cr = side of the
# account, analysis-column side = the column header, e.g. "postage"), wrong (common wrong statement → remark). extra_ok per question.
# True/false items: the verdict is checked exactly; kw/min check the reason (2 marks only for verdict + reason).
AUTO = {
    'n1': {'extra_ok': False,
           's1': {'rows': [['cash', 'dr', 150000], ['capital', 'cr', 150000], ['purchase', 'dr', 60000], ['cash', 'cr', 60000], ['cash', 'dr', 45000], ['sale', 'cr', 45000],
                           ['arun', 'dr', 28000], ['sale', 'cr', 28000], ['rent', 'dr', 8000], ['cash', 'cr', 8000], ['cash', 'dr', 20000], ['arun', 'cr', 20000], ['drawing', 'dr', 5000], ['cash', 'cr', 5000]],
                  'wrong': [{'kw': ['drawings expense|drawing expense|drawings profit loss'], 'say': 'Drawings reduce capital; they are not a business expense like rent.'}]},
           's2': {'kw': ['started|commenced|brought|introduced', 'bought|purchased', 'sold', 'paid|payment', 'received|receipt', 'withdrawn|personal|drawn|private'], 'min': 4},
           's3': {'rows': [['capital', 'dr', 150000], ['sale', 'dr', 45000], ['arun', 'dr', 20000], ['purchase', 'cr', 60000], ['rent', 'cr', 8000], ['drawing', 'cr', 5000], ['balance', 'cr', 142000]]},
           's4': {'rows': [['balance', 'dr', 73000], ['cash', 'cr', 45000], ['arun', 'cr', 28000], ['sale', 'dr', 28000], ['cash', 'cr', 20000], ['balance', 'cr', 8000]]},
           's5': {'rows': [['cash', 'dr', 142000], ['capital', 'cr', 150000], ['purchase', 'dr', 60000], ['sale', 'cr', 73000], ['arun', 'dr', 8000], ['rent', 'dr', 8000], ['drawing', 'dr', 5000]]},
           's6': {'nums': [223000]}},
    'n2': {'extra_ok': False,
           's1': {'rows': [['postage', 'postage', 420], ['paper|pen|stationery|printer', 'stationery', 860], ['cartage', 'cartage', 1250], ['auto|fare|travel|bank', 'travel', 690],
                           ['courier', 'postage', 310], ['tea|staff|meeting|sundry', 'sundry', 540]]},
           's2': {'nums': [4070, 730]},
           's3': {'nums': [930], 'kw': ['balance|c d|carried|in hand'], 'min': 1},
           's4': {'kw': ['|'.join([f'{w} 4070' for w in ('reimburs', 'reimbursement', 'restor', 'replenish', 'received', 'receive', 'top up', 'paid')] + [f'4070 {w}' for w in ('reimburs', 'reimbursed', 'received', 'restor', 'replenish')])], 'min': 1,
                  'wrong': [{'kw': ['reimburse 930|reimbursed 930|reimbursement 930|930 reimburs'], 'say': 'The reimbursement equals the amount spent (₹4,070), not the balance in hand.'}]}},
    'tf': {
        't1': {'kw': ['not recorded|never recorded|net price|net amount|deducted invoice|no entry|not entered|not passed|net invoice|not accounted|not shown books|not debited'], 'min': 1},
        't2': {'kw': ['cash bank|both cash|both account|both side|cash book itself|already cash book|already recorded|already appear|both appear|both affected|both recorded|same book|within cash book'], 'min': 1},
        't3': {'kw': ['omission|principle|compensat|commission|errors not revealed|not disclosed|undisclosed|not affect agreement|arithmetical|arithmetic|wrong account|still errors|errors remain'], 'min': 1},
        't4': {'kw': ['drawing', 'purchase|cost|no sale|not sale|not sold'], 'min': 2},
        't5': {'kw': ['trading|profit loss|p l|closed|transfer|written off'], 'min': 1},
        't6': {'kw': ['journal proper|journal', 'asset|computer|not goods|goods dealt|only goods|not dealt|not stock|fixed asset'], 'min': 2}},
}


def _attach_auto(m):
    for Q in m['questions']:
        for part in Q['parts']:
            if part.get('kind') == 'q':
                q = part['question']; a = AUTO[q['id']]
                q['extra_ok'] = a.get('extra_ok', False)
                for s in q['scheme']: s.update(a[s['id']])
            elif part.get('kind') == 'tf':
                for it in part['items']: it.update(AUTO['tf'][it['id']])
    return m


_build_core = build


def build(): return _attach_auto(_build_core())
