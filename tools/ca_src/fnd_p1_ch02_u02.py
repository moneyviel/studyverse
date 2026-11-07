"""CA Foundation · Paper 1 · Chapter 2 · Unit 2 Ledgers (original content)."""
from lib import *
from shared import kavya_entries

UID = 'fnd-p1-ch02-u02'


import copy
from ca_viva import VIVA, P, ALT


def viva():
    """Viva from ca_viva.py with key points re-tuned in the second review for the negation-aware matcher
    (swapped-term answers must score < 80%; natural paraphrases >= 80%)."""
    v = copy.deepcopy(VIVA[UID]); q = {x['id']: x for x in v}

    def put(vid, pt): q[vid]['points'] = [pt if p['id'] == pt['id'] else p for p in q[vid]['points']]
    put('v1', P('p1', 'Groups transactions account by account (classified record)', 4, 'account by account|account wise|each account|every account|classified|classifi|grouped|groups|group|separate account|under each'))
    put('v1', P('p3', 'Trial balance and final accounts are prepared from it', 4,
                ALT('{x} prepar', 'prepar {x}', '{x} drawn up from', '{x} made from', '{x} based on ledger', 'basis {x}', 'base {x}', 'basis for {x}', 'base for {x}',
                    x=('trial balance', 'final account', 'financial statement', 'balance sheet', 'profit loss')) + '|prepared from it|prepared from ledger|prepared from the ledger'))
    put('v4', P('p1', 'Personal and real accounts are balanced and carried forward', 5,
                ALT('{a} {x}', a=('personal real', 'real personal', 'personal and real', 'real and personal'), x=('balanc', 'carri forward', 'carry forward', 'carried down', 'carry down', 'continu', 'opening balanc'))))
    put('v4', P('p2', 'Nominal accounts are closed by transfer to Trading / Profit and Loss Account', 5, 'nominal',
                'clos|transfer|not carried|not carri forward|not carry forward|written off|write off|wiped|start zero|start from zero'))
    put('v2', P('p1', 'Debited account: entry on its debit side with "To" + name of the credited account', 4,
                'account debit debit side|debit account debit side|debited account debit side|account debit post debit|debit side account debit|debit side of account debit|account debited goes debit side',
                'name account credit|name credit account|name of account credited|credit account name|account credited name'))
    put('v2', P('p2', 'Credited account: entry on its credit side with "By" + name of the debited account', 4,
                'account credit credit side|credit account credit side|credited account credit side|account credit post credit|credit side account credit|credit side of account credit|account credited goes credit side',
                'name account debit|name debit account|name of account debited|debit account name|account debited name'))
    put('v5', P('p1', 'Debit balance: debit side heavier than the credit side', 4, 'debit balanc',
                ALT('debit {s} {m}', 'debit balanc mean debit {s}', s=('side', 'total', 'side total'), m=('more', 'great', 'exceed', 'heavier', 'bigger', 'larger', 'excess')) + '|debit balanc debit side|debit balanc mean debit|debit balanc debit exceed|debit balanc debit more',
                'more|heavier|greater|great|exceed|bigger|larger|excess'))
    put('v5', P('p2', 'Credit balance: credit side heavier than the debit side', 4, 'credit balanc',
                ALT('credit {s} {m}', 'credit balanc mean credit {s}', s=('side', 'total', 'side total'), m=('more', 'great', 'exceed', 'heavier', 'bigger', 'larger', 'excess')) + '|credit balanc credit side|credit balanc mean credit|credit balanc credit exceed|credit balanc credit more',
                'more|heavier|greater|great|exceed|bigger|larger|excess'))
    return v


def build():
    E1 = kavya_entries()
    accs = ['Cash A/c', 'Bank A/c', 'Purchases A/c', 'Mehta & Co.', 'Rohan']
    L1 = ledgers_from(E1, accs, from_id='j1', year_end='Apr 30', next_day='May 1')
    c1 = Checks()
    c1.add('400000+44100-250000', 'Cash balance on 30 April')
    c1.add('250000-38000-70560-30000', 'Bank balance on 30 April')
    c1.add('72000-3500-2000', 'Purchases balance on 30 April')
    c1.add('72000-(70560+1440)', 'Mehta & Co. balance (nil)')
    c1.add('45000-(44100+900)', 'Rohan balance (nil)')

    # running-balance form of Bank account
    c2 = Checks()
    b1 = c2.add('250000', 'Balance after deposit')
    b2 = c2.add('250000-38000', 'Balance after computer')
    b3 = c2.add('212000-70560', 'Balance after paying Mehta & Co.')
    b4 = c2.add('141440-30000', 'Balance after salary and rent')
    run = table(['Date', 'Particulars', 'Dr (₹)', 'Cr (₹)', 'Balance (₹)', 'Dr/Cr'], [
        ['Apr 2', 'Cash A/c', '2,50,000', '', inr(b1), 'Dr'],
        ['Apr 10', 'Computer A/c', '', '38,000', inr(b2), 'Dr'],
        ['Apr 15', 'Mehta & Co.', '', '70,560', inr(b3), 'Dr'],
        ['Apr 30', 'Salaries A/c, Rent A/c', '', '30,000', inr(b4), 'Dr'],
    ], title='Bank Account — running balance form')

    # creditor with opening balance
    E3 = [
        je('Apr 8', [('Purchases A/c', 60000)], [('Patel Brothers', 60000)], 'Being goods bought on credit'),
        je('Apr 14', [('Patel Brothers', 4000)], [('Purchases Returns A/c', 4000)], 'Being goods returned to Patel Brothers'),
        je('Apr 20', [('Patel Brothers', 50000)], [('Bank A/c', 50000)], 'Being part payment made by cheque'),
    ]
    c3 = Checks()
    c3.add('35000+60000-4000-50000', 'Closing credit balance of Patel Brothers')
    L3 = ledgers_from(E3, ['Patel Brothers'], opening={'Patel Brothers': ('cr', 35000, 'Apr 1')}, from_id='j3', year_end='Apr 30', next_day='May 1')

    # Q1 model
    EQ1 = [
        je('Aug 1', [('Cash A/c', 200000)], [('Capital A/c', 200000)], 'Being business started with cash'),
        je('Aug 3', [('Purchases A/c', 50000)], [('Cash A/c', 50000)], 'Being goods bought for cash'),
        je('Aug 6', [('Anita', 36000)], [('Sales A/c', 36000)], 'Being goods sold on credit'),
        je('Aug 12', [('Cash A/c', 35000), ('Discount Allowed A/c', 1000)], [('Anita', 36000)], 'Being cash received from Anita, discount allowed'),
        je('Aug 18', [('Rent A/c', 8000)], [('Cash A/c', 8000)], 'Being rent paid in cash'),
        je('Aug 25', [('Cash A/c', 22000)], [('Sales A/c', 22000)], 'Being goods sold for cash'),
    ]
    q1c = Checks()
    q1c.add('200000+35000+22000-50000-8000', 'Cash balance on 31 August')
    q1c.add('36000+22000', 'Sales balance on 31 August')
    LQ1 = ledgers_from(EQ1, ['Cash A/c', 'Sales A/c', 'Anita'], from_id='jq1', year_end='Aug 31', next_day='Sep 1')

    # Q3: compound entry posting
    EQ3 = [je('Sep 9', [('Salaries A/c', 24000), ('Wages A/c', 16000), ('Electricity A/c', 5000)], [('Bank A/c', 45000)], 'Being salaries, wages and the electricity bill paid by one cheque')]
    q3c = Checks(); q3c.add('24000+16000+5000', 'Total cheque')
    LQ3 = [{'t': 'ledger', 'ac': 'Bank Account', 'open': True, 'from': 'jq3', 'dr': [], 'cr': [
        {'date': 'Sep 9', 'part': 'By Salaries A/c', 'amt': 24000}, {'date': 'Sep 9', 'part': 'By Wages A/c', 'amt': 16000}, {'date': 'Sep 9', 'part': 'By Electricity A/c', 'amt': 5000}]}]
    LQ3 += [dict(b, open=True) for b in ledgers_from(EQ3, ['Salaries A/c', 'Wages A/c', 'Electricity A/c'], from_id='jq3')]
    for b in LQ3[1:]:          # show just the posting (no balancing) for this question
        b['dr'] = [x for x in b['dr'] if not x.get('bal')]; b['cr'] = [x for x in b['cr'] if not x.get('bal')]; b.pop('next', None)

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 2, 'title': 'Ledgers',
        'outcomes': ['Explain what a ledger is and how it differs from the journal.', 'Post journal entries — simple and compound — into ledger accounts with the right "To" and "By" wording.',
                     'Balance an account and carry the balance down correctly to the next period.', 'Say which accounts are balanced and carried forward and which are closed by transfer at the year end.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 40}, 'prereq': ['fnd-p1-ch02-u01'],
                 'exam_tip': 'Ledger accounts are usually asked as part of a bigger question. Neat posting and correct balancing earn quick marks.'},
        'concepts': [
            {'id': 'c1', 'title': 'The ledger: the principal book', 'body': ['The journal records transactions in date order. The ledger regroups the same information account by account, so you can see the full story of Cash, Rohan or Rent in one place.',
                                                                            'Every account has a page (folio). The folio number is written in the L.F. column of the journal, and the journal page in the J.F. column of the ledger, so you can trace an entry both ways.'],
             'analogy': 'The journal is your phone\'s call log in time order; the ledger is the same calls grouped by contact.', 'work': 'When a client asks "how much does this customer owe us?", nobody reads the journal — you open the customer\'s ledger account. Auditors also send balance confirmations straight from ledger balances.'},
            {'id': 'c2', 'title': 'Posting rules', 'body': ['For the account debited in the journal: write on its debit side, "To" + the name of the account credited, with date, J.F. and amount.',
                                                           'For the account credited: write on its credit side, "By" + the name of the account debited.',
                                                           'Compound entry: each account is posted with its own amount. The single account on one side shows each of the other accounts separately (or the word "Sundries" for the total).'],
             'analogy': 'In each account you write where the money went to or came from — like writing the sender\'s name on a received parcel.', 'work': 'Software posts automatically, but you still read ledgers to find mistakes. If Rent Account shows "By Sales", something was posted to the wrong side.'},
            {'id': 'c3', 'title': 'Balancing an account', 'body': ['Total both sides. Write the difference on the lighter side as "Balance c/d" (carried down), so both totals become equal. Then bring it down on the opposite side as "Balance b/d" (brought down) at the start of the next period.',
                                                                  'A debit balance means the debit side was heavier (assets, expenses, debtors). A credit balance means the credit side was heavier (liabilities, capital, incomes, creditors). If both sides are equal, the account is simply closed.'],
             'analogy': 'Like closing a school notebook at term end: you write the final score, rule off, and start the next page with that score.', 'work': 'A debtor with a credit balance (customer has paid too much) or a cash account with a credit balance (impossible) is an instant warning sign during ledger scrutiny.'},
            {'id': 'c4', 'title': 'Balanced or closed at the year end?', 'body': ['Personal and real accounts (debtors, creditors, capital, cash, bank, assets) are balanced and their balances carried forward — they continue into next year.',
                                                                                 'Nominal accounts (expenses, losses, incomes, gains) are not carried forward. At the year end they are closed by transfer to the Trading or Profit and Loss Account, so next year starts with zero.'],
             'analogy': 'Your savings carry over to next year; your monthly phone bill does not — each year\'s bills are counted in that year only.', 'work': 'If a nominal account shows an opening balance on 1 April, the year-end closing entries were missed — a classic finding when you take over a new client\'s books.'},
            {'id': 'c5', 'title': 'Two common formats', 'body': ['T-form (traditional): two sides, Dr and Cr, each with Date, Particulars, J.F. and Amount. This is the exam format.',
                                                                'Running-balance form: one list with Dr, Cr and a Balance column after every entry. This is how accounting software and bank statements show an account.'],
             'blocks': [run],
             'analogy': 'The T-form is a two-team scoreboard; the running-balance form is a live score ticker.', 'work': 'You will read running-balance ledgers every day at work, but write T-form ledgers in the exam unless asked otherwise.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': "Posting Kavya Traders' April journal", 'difficulty': 'core', 'minutes': 15,
             'q': 'Using the journal of Kavya Traders for April 2026 (Unit 1), post the entries into the Cash, Bank, Purchases, Mehta & Co. and Rohan accounts and balance them on 30 April.',
             'given': [journal(E1, 'Journal of Kavya Traders (April 2026)', 'j1')],
             'solution': [journal(E1, 'Journal (for reference)', 'j1')] + L1 + [note('Mehta & Co. and Rohan have equal totals, so they close without a balance. Purchases is a nominal account: here it is balanced only for the month-end trial balance; at the year end it is closed to the Trading Account.')],
             'checks': c1},
            {'id': 'i2', 'title': 'The same Bank account in running-balance form', 'difficulty': 'core', 'minutes': 5,
             'q': 'Show the Bank Account of Kavya Traders for April in running-balance form.', 'solution': [run, p(f'Closing balance ₹{inr(b4)} Dr — the same as the T-form balance c/d.')], 'checks': c2},
            {'id': 'i3', 'title': 'A creditor with an opening balance', 'difficulty': 'core', 'minutes': 6,
             'q': 'On 1 April 2026 the business owed Patel Brothers ₹35,000. During April: bought goods on credit ₹60,000 (Apr 8); returned goods ₹4,000 (Apr 14); paid ₹50,000 by cheque (Apr 20). Prepare Patel Brothers\' account.',
             'solution': [journal(E3, 'Journal entries', 'j3')] + L3 + [p('The account has a credit balance of ₹41,000: the business still owes Patel Brothers this amount.')], 'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Ledger scrutiny before the audit', 'role': 'Articled assistant (audit team)', 'situation': 'The client\'s accountant sends the general ledger for the year. Your senior asks you to "scrutinise the ledger" and list anything unusual before fieldwork starts.',
             'steps': ['Scan each account for balances on the wrong side: debtors with credit balances, creditors with debit balances, cash with a credit balance.', 'Look for nominal accounts with opening balances — year-end closing entries may be missing.',
                       'Pick large or round-sum entries and odd narrations ("adjustment", "as per sir") for vouching.', 'Agree the ledger balances to the trial balance the client gave you.'],
             'takeaway': 'Knowing which side each kind of account normally balances on lets you spot errors in minutes.', 'think': 'A customer account shows a credit balance of ₹12,000. Give two possible reasons.',
             'answer': 'The customer paid in advance or paid twice, or a receipt was posted to the wrong customer, or a credit note was entered twice. Each needs checking with documents.'},
            {'id': 'j2', 'title': 'Sending balance confirmations', 'role': 'Accounts executive at a distribution company', 'situation': 'At the year end your company asks its top 20 customers and suppliers to confirm the balance they show for you.',
             'steps': ['Take each party\'s closing balance from its ledger account.', 'Send a statement of account (the ledger in running-balance form) and ask them to confirm or report differences.', 'For each difference, compare entry by entry — usually a payment in transit, a missing invoice or a credit note not yet recorded.'],
             'takeaway': 'Ledger accounts are not just for exams — they are the documents you share with outsiders.', 'think': 'Your books show the supplier is owed ₹80,000; the supplier says ₹95,000. What is the first thing to look for?',
             'answer': 'An invoice of ₹15,000 the supplier has raised but you have not yet recorded (or a payment you recorded that they have not received).'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Cash paid to Arun ₹5,000 is posted in Arun\'s account as:', 'options': ['To Cash A/c on the debit side', 'By Cash A/c on the credit side', 'To Arun A/c on the debit side', 'By Arun A/c on the debit side'], 'answer': 0, 'explain': 'Entry: Arun A/c Dr. To Cash A/c. Arun is debited, so his account shows "To Cash A/c" on the debit side.', 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'When the debit side of an account is heavier, the account has:', 'options': ['A debit balance', 'A credit balance', 'No balance', 'A suspense balance'], 'answer': 0, 'explain': 'The balance is named after the heavier side. The balance c/d is written on the lighter (credit) side.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Which of these accounts is closed by transfer to the Profit and Loss Account at the year end?', 'options': ['Rent Paid', 'Machinery', 'Bank', 'Capital'], 'answer': 0, 'explain': 'Rent is a nominal account — it is transferred to the Profit and Loss Account, not carried forward.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm4', 'q': 'An account shows: debit total ₹84,500, credit total ₹61,200. The balance is:', 'options': ['₹23,300 Dr', '₹23,300 Cr', '₹1,45,700 Dr', '₹61,200 Dr'], 'answer': 0, 'check': '84500-61200', 'explain': '84,500 − 61,200 = 23,300; the debit side is heavier, so it is a debit balance.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'The "L.F." column in the journal shows:', 'options': ['The ledger page where the entry is posted', 'The amount of the entry', 'The date of posting', 'The voucher number only'], 'answer': 0, 'explain': 'L.F. = ledger folio, the page of the account in the ledger, filled in at the time of posting.', 'concept': 'c1', 'difficulty': 'core'},
            {'id': 'm6', 'q': '"Balance c/d" is written on:', 'options': ['The side with the smaller total', 'The side with the larger total', 'Always the debit side', 'Always the credit side'], 'answer': 0, 'explain': 'It is the figure that makes the lighter side equal to the heavier side.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'A creditor had an opening balance of ₹20,000. Goods bought on credit ₹45,000; cash paid ₹38,000; goods returned ₹2,000. The closing balance is:', 'options': ['₹25,000 Cr', '₹25,000 Dr', '₹29,000 Cr', '₹21,000 Cr'], 'answer': 0, 'check': '20000+45000-38000-2000', 'explain': 'Credits 20,000 + 45,000 = 65,000; debits 38,000 + 2,000 = 40,000; balance 25,000 Cr.', 'concept': 'c3', 'difficulty': 'moderate'},
            {'id': 'm8', 'q': 'Salary ₹10,000 and wages ₹6,000 are paid by one cheque. In the Bank Account, the credit side shows:', 'options': ['By Salary A/c ₹10,000 and By Wages A/c ₹6,000', 'To Salary A/c ₹16,000', 'By Bank A/c ₹16,000', 'To Sundries ₹16,000'], 'answer': 0, 'explain': 'Bank is credited; its credit side names each account debited with its own amount ("By Sundries" for the total is also acceptable, but never "To").', 'concept': 'c2', 'difficulty': 'moderate'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'ledger',
             'q': 'Neel Stores passed the following journal entries in August 2026. Post them into the Cash, Sales and Anita accounts and balance the accounts on 31 August.',
             'given': [journal(EQ1, 'Journal of Neel Stores (August 2026)', 'jq1')],
             'model': [journal(EQ1, 'Journal (for reference)', 'jq1')] + LQ1 + [note('Anita\'s account closes without a balance. Sales is a nominal account: it is balanced here only for an interim (month-end) trial balance, so its balance is brought down on 1 September; at the year end it is not carried forward but closed by transfer to the Trading Account.')],
             'scheme': [{'id': 's1', 'pt': 'Cash account: receipts To Capital, To Anita, To Sales; payments By Purchases, By Rent', 'm': 2, 'skill': 'posting'},
                        {'id': 's2', 'pt': 'Cash balance c/d ₹1,99,000 and b/d on 1 September', 'm': 1, 'skill': 'balancing'},
                        {'id': 's3', 'pt': 'Sales account: By Anita, By Cash; balance ₹58,000', 'm': 1.5, 'skill': 'posting'},
                        {'id': 's4', 'pt': 'Anita account: To Sales; By Cash ₹35,000 and By Discount Allowed ₹1,000 — closed', 'm': 1.5, 'skill': 'posting'}],
             'checks': q1c,
             'remarks': ['Many candidates write "To" on the credit side or "By" on the debit side — this costs presentation marks in every account.', 'Anita\'s account is often left with a balance because the discount of ₹1,000 is forgotten.'],
             'mistakes': ['Posting the discount into Cash account.', 'Not bringing the balance down (b/d) on 1 September.', 'Balancing a closed account with a zero "balance c/d".'],
             'tips': ['Write the account name in the centre with Dr. and Cr. at the two corners.', 'Rule off totals on the same line on both sides.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'What is meant by balancing an account? Describe the steps, and state which accounts are not carried forward at the end of the year.',
             'model': [p('Balancing means finding the difference between the two sides of an account at the end of a period and recording it so that the account shows its net position.'),
                       ul(['Total both sides of the account.', 'Write the difference on the side with the smaller total as "Balance c/d", so both totals are equal.', 'Rule off and write the equal totals on the same line.', 'Bring the balance down on the opposite side as "Balance b/d" on the first day of the next period.']),
                       p('Nominal accounts (expenses, losses, incomes, gains) are not carried forward: they are closed by transfer to the Trading or Profit and Loss Account. Personal and real accounts are carried forward.')],
             'scheme': [{'id': 's1', 'pt': 'Meaning of balancing', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Steps: totalling, balance c/d on lighter side, ruling off', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Balance b/d on opposite side next period', 'm': 0.5, 'skill': 'concept'}, {'id': 's4', 'pt': 'Nominal accounts closed to Trading/P&L, not carried forward', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Answers that list the steps in order score well.', 'Many forget the second part of the question about nominal accounts.'],
             'mistakes': ['Saying the balance c/d goes on the heavier side.', 'Saying all accounts are carried forward.'], 'tips': ['Number the steps.', 'Answer every part of the question — look for the word "and".']},
            {'id': 'q3', 'marks': 3, 'minutes': minutes(3), 'difficulty': 'moderate', 'pad': 'ledger',
             'q': 'On 9 September 2026 a business paid salaries ₹24,000, wages ₹16,000 and the electricity bill ₹5,000 by a single cheque. Show the journal entry and post it to the ledger (no balancing needed).',
             'model': [journal(EQ3, 'Journal', 'jq3')] + LQ3,
             'scheme': [{'id': 's1', 'pt': 'Compound journal entry with total ₹45,000 and narration', 'm': 1, 'skill': 'classification'},
                        {'id': 's2', 'pt': 'Bank account credited with three separate "By" lines (or By Sundries ₹45,000)', 'm': 1, 'skill': 'posting'},
                        {'id': 's3', 'pt': 'Each expense account debited "To Bank A/c" with its own amount', 'm': 1, 'skill': 'posting'}],
             'checks': q3c,
             'remarks': ['Some candidates debit Bank — read whether money comes in or goes out.'], 'mistakes': ['Writing "To Sundries" in the expense accounts.', 'Posting the total ₹45,000 to every expense account.'],
             'tips': ['In a compound entry the single account lists the others; the others each name the single account.']},
        ],
        'revision': {'summary': ['The ledger groups journal entries account by account.', 'Debited account: debit side, "To" + other account. Credited account: credit side, "By" + other account.', 'Balance c/d on the lighter side; balance b/d on the opposite side next period.', 'Personal and real accounts are carried forward; nominal accounts are closed to Trading/P&L.'],
                     'remember': ['"To" always on the debit side, "By" always on the credit side.', 'Debit balance = debit side heavier.', 'J.F. in the ledger, L.F. in the journal.'],
                     'traps': ["Don't write the balance c/d on the heavier side.", "Don't carry forward nominal accounts.", "Don't post a compound entry's total to each account."]},
        'quickref': [{'k': 'Posting a debit', 'v': 'Debit side of that account: "To <account credited>"'}, {'k': 'Posting a credit', 'v': 'Credit side of that account: "By <account debited>"'},
                     {'k': 'Balancing', 'v': 'Difference on the lighter side as Balance c/d; Balance b/d on the opposite side next period'},
                     {'k': 'Usually debit balances', 'v': 'Assets, expenses, losses, drawings, debtors'}, {'k': 'Usually credit balances', 'v': 'Liabilities, capital, incomes, gains, creditors'}],
        'viva': viva(),
    }
