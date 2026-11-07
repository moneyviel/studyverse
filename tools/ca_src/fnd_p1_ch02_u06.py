"""CA Foundation · Paper 1 · Chapter 2 · Unit 6 Rectification of Errors (original content)."""
from lib import *

UID = 'fnd-p1-ch02-u06'


import copy
from ca_viva import VIVA, P, ALT


def viva():
    """Viva from ca_viva.py with key points re-tuned in the second review for the negation-aware matcher
    (swapped-term answers must score < 80%; natural paraphrases >= 80%)."""
    v = copy.deepcopy(VIVA[UID]); q = {x['id']: x for x in v}

    def put(vid, pt): q[vid]['points'] = [pt if p['id'] == pt['id'] else p for p in q[vid]['points']]
    put('v2', P('p1', 'One-sided error affects only one account', 3,
                ALT('{o} {x}', o=('one sid', 'one side', 'single sid', 'single side'), x=('one account', 'single account', 'only one', 'affect one', 'affect only', 'affect single', 'affect just', 'just one'))))
    put('v2', P('p3', 'Two-sided error affects two accounts; trial balance still agrees', 3,
                ALT('{t} {x}', t=('two sid', 'two side', 'both sid', 'double sid'), x=('two account', 'both account', 'affect two', 'affect both', 'still agre', 'agre', 'not affect', 'no effect', 'not disturb'))))
    return v


def build():
    # ---------- Illustration 1: before trial balance ----------
    E1 = [
        je('(a)', [('Machinery A/c', 45000)], [('Purchases A/c', 45000)], 'Being machinery wrongly debited to Purchases account, now corrected'),
        je('(b)', [('Amit', 12000)], [('Sumit', 12000)], "Being credit sale to Amit wrongly posted to Sumit's account, now corrected"),
        je('(c)', [('Rent A/c', 9000)], [("Landlord's A/c", 9000)], "Being rent paid wrongly debited to the landlord's personal account, now corrected"),
        je('(f)', [('Machinery A/c', 3000)], [('Wages A/c', 3000)], 'Being wages for installing the new machine capitalised'),
    ]
    c1 = Checks()
    c1.add('6500-5600', 'Excess credit to Rani, to be reversed by a debit')
    one_sided = table(['Error', 'Rectification (no journal entry — corrected in the ledger account)'], [
        ['(d) Sales book under-cast by ₹1,000', 'Sales Account: credit side "By Under-casting of Sales Book for <month> ₹1,000"'],
        ['(e) ₹5,600 received from Rani posted to her account as ₹6,500', "Rani's Account: debit side \"To Wrong posting ₹900\""],
    ], title='One-sided errors found before the trial balance')

    # ---------- Illustration 2: after trial balance, suspense account ----------
    E2 = [
        je('(i)', [('Suspense A/c', 2000)], [('Purchases A/c', 2000)], 'Being purchases book over-cast, now corrected'),
        je('(ii)', [('Suspense A/c', 7000)], [('Gopal', 7000)], "Being return of ₹3,500 posted to the debit instead of the credit of Gopal's account, now corrected"),
        je('(iii)', [('Discount Allowed A/c', 800)], [('Suspense A/c', 800)], 'Being discount allowed not posted to Discount Allowed account, now corrected'),
        je('(iv)', [('Repairs A/c', 4500)], [('Building A/c', 4500)], 'Being repairs wrongly debited to Building account, now corrected'),
        je('(v)', [('Suspense A/c', 3600)], [('Harsh', 3600)], "Being cheque of ₹6,200 from Harsh posted as ₹2,600, now corrected"),
        je('(vi)', [('Salary A/c', 13500)], [('Suspense A/c', 13500)], 'Being salary of ₹15,000 posted as ₹1,500, now corrected'),
    ]
    c2 = Checks()
    opening = c2.add('(800+13500)-(2000+7000+3600)', 'Opening debit balance in Suspense (difference in trial balance)')
    c2.add('2000+2*3500-800+(6200-2600)-(15000-1500)', 'Net (debit total minus credit total) error in trial balance = minus the suspense debit')
    c2.add('3500*2', 'Gopal: wrong-side posting is corrected with double the amount')
    L2 = ledgers_from(E2, ['Suspense A/c'], opening={'Suspense A/c': ('dr', opening, 'Apr 1')}, from_id='j2', year_end='—', next_day='—')
    L2[0]['dr'][0]['part'] = 'To Difference in Trial Balance'
    L2[0]['dr'][0]['date'] = ''
    for side in ('dr', 'cr'):
        for x in L2[0][side]:
            if x['date'] not in ('',): x['date'] = ''
    eff = table(['Error', 'Increase in profit (₹)', 'Decrease in profit (₹)'], [
        ['(i) Purchases over-cast, now reduced', '2,000', ''], ['(ii) Personal account only', '', ''], ['(iii) Discount allowed now charged', '', '800'],
        ['(iv) Repairs now charged as expense', '', '4,500'], ['(v) Personal account only', '', ''], ['(vi) Salary now charged in full', '', '13,500'], ['Total', '2,000', '18,800']],
        num=[1, 2], total=True, title='Effect of rectification on net profit')
    net = c2.add('2000-18800', 'Net effect of rectification on profit (negative = profit decreases)')

    # ---------- Illustration 3: next accounting period ----------
    E3 = [
        je('Apr 10', [('Suspense A/c', 5000)], [('Profit & Loss Adjustment A/c', 5000)], "Being last year's purchases book over-cast, now corrected"),
        je('Apr 10', [('Furniture A/c', 20000)], [('Profit & Loss Adjustment A/c', 20000)], 'Being furniture bought last year wrongly debited to Purchases, now corrected'),
        je('Apr 10', [('Bina', 6000)], [('Profit & Loss Adjustment A/c', 6000)], 'Being a credit sale of last year omitted, now recorded'),
        je('Apr 10', [('Profit & Loss Adjustment A/c', 31000)], [('Capital A/c', 31000)], "Being balance of Profit & Loss Adjustment account (last year's profit understated) transferred to capital"),
    ]
    c3 = Checks()
    c3.add('5000+20000+6000', "Last year's profit understated by")
    L3 = ledgers_from(E3, ['Profit & Loss Adjustment A/c'], from_id='j3', year_end='Apr 10', next_day='—')

    # ---------- Q1 ----------
    EQ = [
        je('(a)', [('Suspense A/c', 1200)], [('Sales A/c', 1200)], 'Being sales book under-cast, now corrected'),
        je('(b)', [('Purchases A/c', 5000), ('Sales A/c', 5000)], [('Dinesh', 10000)], 'Being credit purchase from Dinesh wrongly entered in the sales book, now corrected'),
        je('(c)', [('Kamal', 4800)], [('Suspense A/c', 4800)], "Being return of ₹2,400 posted to the credit instead of the debit of Kamal's account, now corrected"),
        je('(d)', [('Suspense A/c', 3600)], [('Interest Received A/c', 3600)], 'Being interest received of ₹1,800 posted to the debit instead of the credit, now corrected'),
        je('(e)', [('Furniture A/c', 7000)], [('Purchases A/c', 7000)], 'Being furniture wrongly debited to Purchases account, now corrected'),
        je('(f)', [('Leela', 900)], [('Suspense A/c', 900)], 'Being payment of ₹4,300 to Leela posted as ₹3,400, now corrected'),
    ]
    q1c = Checks()
    qop = q1c.add('(4800+900)-(1200+3600)', 'Opening debit balance of Suspense (difference in trial balance)')
    q1c.add('1200-2*2400+2*1800-(4300-3400)', 'Net (Dr - Cr) trial balance error = minus suspense debit')
    LQ = ledgers_from(EQ, ['Suspense A/c'], opening={'Suspense A/c': ('dr', qop, '')}, from_id='jq1', year_end='', next_day='—')
    LQ[0]['dr'][0]['part'] = 'To Difference in Trial Balance'

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 6, 'title': 'Rectification of Errors',
        'outcomes': ['Name the stages at which errors arise and classify errors as omission, commission, principle or compensating.', 'Tell one-sided errors from two-sided errors and predict which ones disturb the trial balance.',
                     'Rectify errors found before the trial balance, after the trial balance (through a suspense account) and in the next accounting period (through a Profit & Loss Adjustment account).', 'Work out the effect of each error and its rectification on net profit.'],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 60}, 'prereq': ['fnd-p1-ch02-u03'],
                 'exam_tip': 'Rectification with a suspense account is a regular 5–10 mark question. Write the correct entry, the wrong entry, then the rectifying entry in your head for every item.'},
        'concepts': [
            {'id': 'c1', 'title': 'Where errors creep in', 'body': ['Errors can happen while recording in the journal or subsidiary books, while posting to the ledger, while totalling (casting) or carrying forward a total, while balancing an account, or while copying balances into the trial balance.',
                                                                  'Over-casting means adding up a column to more than its true total; under-casting means less.'],
             'analogy': 'Like a relay race: the baton (the amount) can be dropped at any hand-over — book, ledger, total, trial balance.', 'work': 'When a difference appears, accountants retrace these stages in order: re-add the books, check postings, re-balance accounts and re-copy the trial balance.'},
            {'id': 'c2', 'title': 'Four kinds of errors', 'body': ['Errors of omission — a transaction is left out completely (both sides) or partly (only one side posted).',
                                                                 'Errors of commission — wrong amount, wrong account of the same class (posting to Sumit instead of Amit), wrong side, wrong total, wrong balance.',
                                                                 'Errors of principle — the accounting rule is broken: capital expenditure treated as revenue (machinery debited to Purchases) or the reverse (repairs debited to Building).',
                                                                 'Compensating errors — two or more errors that cancel each other\'s effect on the trial balance.'],
             'analogy': 'Omission = forgot to write it; commission = wrote it wrongly; principle = did not know the rule; compensating = two wrongs that hide each other.', 'work': 'Errors of principle matter most to auditors because they misstate both profit and assets — the trial balance never catches them.'},
            {'id': 'c3', 'title': 'One-sided and two-sided errors', 'body': ['A one-sided error affects only one account (a wrong total, a posting on one side only, a wrong amount posted to one account). It disturbs the trial balance.',
                                                                           'A two-sided error affects two accounts equally (both sides wrong in the same way). It does not disturb the trial balance and is corrected by a journal entry between the two accounts.'],
             'analogy': 'One-sided: one shoe is missing. Two-sided: both shoes are on the wrong feet — still a pair, but wrong.', 'work': 'A trial balance difference tells you that at least one one-sided error exists. Its amount is a clue: a difference divisible by 9 often points to transposed digits (₹5,600 written as ₹6,500).'},
            {'id': 'c4', 'title': 'Rectifying before the trial balance', 'body': ['Two-sided errors: pass a journal entry that cancels the wrong part and records the right part. Method: write the correct entry, write the wrong entry that was made, and pass the entry that turns one into the other.',
                                                                                'One-sided errors: no journal entry. Make a correcting posting in the affected account only, with an explanatory narration ("By Under-casting of Sales Book").'],
             'analogy': 'Correct entry − wrong entry = rectifying entry.', 'work': 'In software you cannot write "one-sided" corrections — every voucher must balance. That is why companies use a suspense or "errors" account and journal vouchers for every correction.'},
            {'id': 'c5', 'title': 'After the trial balance: the suspense account', 'body': ['If final accounts must be prepared before errors are found, the trial balance difference is placed in a Suspense Account.',
                                                                                          'When errors are found, one-sided errors are rectified through the Suspense Account (it takes the other side of the entry); two-sided errors are rectified as usual between the two accounts.',
                                                                                          'When all errors are found, the suspense account closes automatically. Wrong-side postings are corrected with double the amount.'],
             'analogy': 'The suspense account is a "lost and found" box — every one-sided error you fix takes its amount out of (or puts it into) the box until the box is empty.', 'work': 'Auditors ask for a list of all items cleared from suspense with the evidence for each — a balance written off without explanation is a red flag.'},
            {'id': 'c6', 'title': 'Next accounting period and the effect on profit', 'body': ['Once last year\'s books are closed, nominal accounts of that year no longer exist. Errors affecting last year\'s profit are corrected through a Profit & Loss Adjustment Account; its balance is then transferred to Capital (or partners\' capital).',
                                                                                         'Errors affecting only real or personal accounts are corrected directly in those accounts.',
                                                                                         'Effect on profit: correcting an expense or loss upward, or an income downward, reduces profit; the opposite increases it. Corrections between personal or real accounts do not affect profit.'],
             'analogy': 'You cannot rewrite last year\'s report card, but you can add a note to this year\'s file saying last year\'s marks were understated.', 'work': 'Prior-period errors are reported carefully in financial statements; at Intermediate level you will meet the accounting standard that deals with them.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Before the trial balance', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Sagar Traders found these errors before preparing the trial balance. Rectify them: (a) machinery bought for ₹45,000 was debited to Purchases account; (b) a credit sale to Amit of ₹12,000 was posted to Sumit\'s account; (c) rent paid ₹9,000 was debited to the landlord\'s personal account; (d) the sales book was under-cast by ₹1,000; (e) cash of ₹5,600 received from Rani was posted to her account as ₹6,500; (f) wages of ₹3,000 paid for installing the new machine were debited to Wages account.',
             'solution': [journal(E1, 'Rectifying journal entries (two-sided errors)', 'j1'), one_sided,
                          wn('Method for (a)', 'Correct entry: Machinery Dr ₹45,000. Wrong entry made: Purchases Dr ₹45,000. Rectify: Machinery Dr, To Purchases — removes the wrong debit and records the right one.')],
             'checks': c1},
            {'id': 'i2', 'title': 'After the trial balance: suspense account', 'difficulty': 'hard', 'minutes': 20,
             'q': 'The trial balance of Lakshya Stores on 31 March 2027 did not agree and the difference was put to a suspense account. Later these errors were found: (i) the purchases book was over-cast by ₹2,000; (ii) a sales return of ₹3,500 from Gopal was posted to the debit of his account; (iii) a discount of ₹800 allowed to a customer was not posted to Discount Allowed account; (iv) repairs of ₹4,500 were debited to Building account; (v) a cheque of ₹6,200 received from Harsh was posted to his account as ₹2,600; (vi) salary of ₹15,000 was posted to Salary account as ₹1,500. Pass rectifying entries, prepare the suspense account and show the effect on profit.',
             'solution': [journal(E2, 'Rectifying journal entries', 'j2')] + L2 + [p(f'The suspense account had a debit balance of ₹{inr(opening)} — the debit side of the trial balance was short by that amount.'), eff,
                          p(f'Net effect: profit decreases by ₹{inr(-net)} after rectification (it was overstated by that amount).')],
             'checks': c2},
            {'id': 'i3', 'title': 'Errors found in the next year', 'difficulty': 'hard', 'minutes': 12,
             'q': 'After closing the books for 2026-27, the following errors were found on 10 April 2027: (a) the purchases book was over-cast by ₹5,000 (the difference had been put to suspense); (b) furniture bought for ₹20,000 was debited to Purchases account; (c) a credit sale of ₹6,000 to Bina was not recorded at all. Rectify the errors through a Profit & Loss Adjustment Account (ignore depreciation).',
             'solution': [journal(E3, 'Rectifying entries in 2027-28', 'j3')] + L3 + [p('All three errors had understated last year\'s profit, so the balance (₹31,000) is credited to Capital.')], 'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Clearing a suspense account before the audit', 'role': 'Accounts assistant at a CA firm (accounting outsourcing)', 'situation': 'A client\'s books show a suspense balance of ₹18,450 at the year end. The partner wants it cleared or explained before the books go to the auditor.',
             'steps': ['Check the arithmetic of every subsidiary book total and carry-forward.', 'Compare the cash book with the bank statement for amounts posted differently.', 'Look for differences divisible by 9 (transposed digits) and by 2 (wrong-side postings).',
                       'For every error found, pass a rectifying entry through suspense and keep a working paper listing each one.', 'Explain any small residual balance to the partner rather than writing it off quietly.'],
             'takeaway': 'Rectification is detective work: the size of the difference often tells you where to look.', 'think': 'The difference is ₹1,800. Why might you look for a posting of ₹900 on the wrong side?',
             'answer': 'A wrong-side posting moves the trial balance by double the amount: ₹900 on the wrong side creates a difference of ₹1,800.'},
            {'id': 'j2', 'title': 'An error of principle that changes profit', 'role': 'Junior auditor reviewing fixed asset additions', 'situation': 'While vouching additions to Building account you find invoices for painting and leak repairs totalling ₹2,40,000.',
             'steps': ['Check whether the work improves the building (capital) or only maintains it (revenue).', 'Painting and leak repairs maintain the building — revenue expenditure.', 'Propose the rectification: Repairs A/c Dr, To Building A/c ₹2,40,000.', 'Note the effect: profit is overstated by ₹2,40,000 (and so is the building) until corrected.'],
             'takeaway': 'Errors of principle never show up in the trial balance — only judgement and documents reveal them.', 'think': 'Will this error affect the trial balance agreement?', 'answer': 'No. Both the debit and the credit were recorded equally; only the classification is wrong.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Purchase of a computer for office use debited to Purchases account is an error of:', 'options': ['Principle', 'Commission', 'Omission', 'Compensation'], 'answer': 0, 'explain': 'A capital item treated as revenue (goods) breaks an accounting principle.', 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'Which error affects the agreement of the trial balance?', 'options': ['Sales book under-cast by ₹500', 'Credit sale to Ravi posted to Rahul\'s account', 'Repairs debited to Machinery account', 'A credit purchase not recorded at all'], 'answer': 0, 'explain': 'Under-casting affects only Sales account (one-sided), so the trial balance will not agree. Posting to the wrong customer and repairs debited to Machinery are two-sided errors, and a transaction omitted completely affects neither side — none of these disturbs the agreement.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Cash received from Anu ₹3,000 was posted to the debit of her account. The rectifying entry (after the trial balance) is:', 'options': ['Suspense A/c Dr. To Anu ₹6,000', 'Anu Dr. To Suspense A/c ₹6,000', 'Suspense A/c Dr. To Anu ₹3,000', 'Cash A/c Dr. To Anu ₹3,000'], 'answer': 0, 'explain': 'Anu should have been credited ₹3,000 but was debited ₹3,000 — she must now be credited ₹6,000; suspense takes the debit.', 'concept': 'c5', 'difficulty': 'moderate'},
            {'id': 'm4', 'q': 'A suspense account opened to agree the trial balance has a credit balance of ₹2,400. The trial balance had:', 'options': ['The debit side ₹2,400 more than the credit side', 'The credit side ₹2,400 more than the debit side', 'Both sides equal', 'A difference of ₹4,800'], 'answer': 0, 'explain': 'A credit to suspense is needed only when the credit side is short — i.e. the debit side was larger.', 'concept': 'c5', 'difficulty': 'moderate'},
            {'id': 'm5', 'q': 'Salary of ₹12,000 was posted to the Salary account as ₹1,200. Rectification will reduce profit by:', 'options': ['₹10,800', '₹12,000', '₹1,200', '₹13,200'], 'answer': 0, 'check': '12000-1200', 'explain': 'Salary account must be debited with the missing ₹10,800, so expenses rise and profit falls by ₹10,800.', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'Errors relating to last year\'s nominal accounts are corrected in the current year through:', 'options': ['Profit & Loss Adjustment Account', 'Trading Account of the current year', 'Suspense Account only', 'Capital Account directly, item by item'], 'answer': 0, 'explain': 'The Profit & Loss Adjustment Account collects them; its net balance goes to Capital.', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'A trial balance difference of ₹2,700 is most likely caused by:', 'options': ['Transposing the digits of an amount (e.g. ₹4,100 as ₹1,400)', 'Omitting a transaction completely', 'Posting to the wrong customer', 'An error of principle'], 'answer': 0, 'explain': '4,100 − 1,400 = 2,700, which is divisible by 9 — typical of transposed digits. The other errors do not disturb the trial balance at all.', 'concept': 'c3', 'difficulty': 'hard'},
            {'id': 'm8', 'q': 'Two errors — Wages account over-cast by ₹700 and Commission Received account over-cast by ₹700 — are:', 'options': ['Compensating errors', 'Errors of principle', 'Errors of omission', 'Two-sided errors that need a suspense entry'], 'answer': 0, 'explain': 'An extra debit and an extra credit of the same amount cancel each other in the trial balance.', 'concept': 'c2', 'difficulty': 'moderate'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'hard', 'pad': 'journal',
             'q': 'Mohan Traders could not agree the trial balance on 31 March 2027 and put the difference to a suspense account. The following errors were found: (a) the sales book was under-cast by ₹1,200; (b) a credit purchase of ₹5,000 from Dinesh was entered in the sales book; (c) goods returned to Kamal ₹2,400 were posted to the credit of his account; (d) interest received ₹1,800 was posted to the debit of Interest Received account; (e) furniture bought for ₹7,000 was debited to Purchases account; (f) cash paid to Leela ₹4,300 was posted to her account as ₹3,400. Pass the rectifying entries and prepare the suspense account.',
             'model': [journal(EQ, 'Rectifying journal entries', 'jq1')] + LQ + [p(f'The opening (debit) balance of suspense — the trial balance difference — was ₹{inr(qop)}.')],
             'scheme': [{'id': 's1', 'pt': '(a) Suspense Dr, To Sales ₹1,200', 'm': 1, 'skill': 'rectification'},
                        {'id': 's2', 'pt': '(b) Purchases Dr and Sales Dr ₹5,000 each, To Dinesh ₹10,000', 'm': 1.5, 'skill': 'rectification'},
                        {'id': 's3', 'pt': '(c) Kamal Dr, To Suspense ₹4,800 (double)', 'm': 1, 'skill': 'rectification'},
                        {'id': 's4', 'pt': '(d) Suspense Dr, To Interest Received ₹3,600 (double)', 'm': 1, 'skill': 'rectification'},
                        {'id': 's5', 'pt': '(e) Furniture Dr, To Purchases ₹7,000', 'm': 0.5, 'skill': 'rectification'},
                        {'id': 's6', 'pt': '(f) Leela Dr, To Suspense ₹900', 'm': 1, 'skill': 'rectification'},
                        {'id': 's7', 'pt': 'Suspense account with opening difference ₹900 (Dr) and closing to nil', 'm': 2, 'skill': 'presentation'}],
             'checks': q1c,
             'remarks': ['Item (b) separates good answers from average ones: both Purchases and Sales must be debited and Dinesh credited with double the amount.', 'Wrong-side postings rectified with the single amount are the most common error.'],
             'mistakes': ['Passing (e) through suspense although it is two-sided.', 'Rectifying (c) with ₹2,400 only.', 'Leaving the suspense account unbalanced instead of finding the opening difference.'],
             'tips': ['For each item write: correct entry → wrong entry → difference.', 'Prepare the suspense account last; the balancing figure is the original difference.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Explain errors of omission, commission, principle and compensating errors with one example each.',
             'model': [ul(['Omission — a transaction left out wholly or partly. Example: a credit sale to Geeta not entered in the sales book.', 'Commission — wrong amount, account, side or total within the right class. Example: cash received from Tarun credited to Varun.',
                           'Principle — violation of an accounting principle, usually capital vs revenue. Example: purchase of a delivery van debited to Purchases.', 'Compensating — errors that cancel each other. Example: Rent account over-cast by ₹500 and Sales account over-cast by ₹500.'])],
             'scheme': [{'id': 's1', 'pt': 'Omission — meaning and example', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Commission — meaning and example', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Principle — meaning and example', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Compensating — meaning and example', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Examples should be specific (names and amounts) — generic examples earn less.'], 'mistakes': ['Giving an error of commission as an example of principle.'], 'tips': ['One line meaning + one line example for each.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'State the effect of rectifying each of the following errors on net profit: (a) wages of ₹6,000 paid for erecting a new machine debited to Wages account; (b) a credit sale of ₹9,000 to Pooja posted to Puja\'s account; (c) commission received ₹2,500 not posted to Commission account; (d) purchases book over-cast by ₹1,500; (e) closing stock under-valued by ₹4,000.',
             'model': [table(['Error', 'Effect of rectification on profit'], [['(a) Wages capitalised to Machinery', 'Increase ₹6,000 (wages expense reduced)'], ['(b) Wrong customer', 'No effect (personal accounts)'],
                                                                              ['(c) Commission received now credited', 'Increase ₹2,500'], ['(d) Purchases reduced', 'Increase ₹1,500'], ['(e) Closing stock increased', 'Increase ₹4,000']]),
                       p('Total: profit increases by ₹14,000 on rectification (ignoring depreciation on the machine).')],
             'checks': [{'expr': '6000+2500+1500+4000', 'value': 14000, 'label': 'Total increase in profit'}],
             'scheme': [{'id': f's{i+1}', 'pt': f'({x}) correct direction and amount', 'm': 1, 'skill': 'application'} for i, x in enumerate('abcde')],
             'remarks': ['Many candidates say (b) increases profit — transfers between personal accounts never affect profit.'], 'mistakes': ['Getting the direction wrong for (a): removing an expense increases profit.'], 'tips': ['Ask for each item: does a nominal account (or stock) change?']},
        ],
        'revision': {'summary': ['Errors arise in recording, posting, casting, balancing or copying to the trial balance.', 'Types: omission, commission, principle, compensating.', 'One-sided errors disturb the trial balance; two-sided errors do not.',
                                 'Before trial balance: journal for two-sided, ledger note for one-sided. After: one-sided go through suspense.', 'Next year: nominal items through Profit & Loss Adjustment A/c, balance to capital.'],
                     'remember': ['Correct entry − wrong entry = rectifying entry.', 'Wrong-side posting is corrected with double the amount.', 'A difference divisible by 9 hints at transposed digits.'],
                     'traps': ["Don't route two-sided errors through suspense.", "Don't forget that personal-account corrections have no effect on profit.", "Don't debit last year's nominal accounts in the new year — use P&L Adjustment."]},
        'quickref': [{'k': 'Error of principle', 'v': 'Capital ↔ revenue mix-up; never shown by the trial balance'}, {'k': 'Suspense opening Dr', 'v': 'Debit side of the trial balance was short'},
                     {'k': 'Wrong-side posting', 'v': 'Rectify with twice the amount'}, {'k': 'Next year (nominal items)', 'v': 'Profit & Loss Adjustment A/c → Capital'},
                     {'k': 'Effect on profit', 'v': 'Expense up / income down → profit down; personal-account fixes → no effect'}],
        'viva': viva(),
    }
