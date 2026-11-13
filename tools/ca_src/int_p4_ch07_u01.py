"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 7 Cost Accounting Systems.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch07-u01'
T1 = 'Non-integrated (cost ledger) accounting'
T2 = 'Integrated accounting'
T3 = 'Reconciling cost and financial profit'


def build():
    ck = Checks()
    fp = ck.add('412000+18000-25000+12000+9000-6000', 'Profit as per financial accounts')
    i1 = {'id': 'i1', 'title': 'Why do the two profits differ?', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Costing profit of Rana Ltd. is ₹4,12,000. Differences: (i) factory overheads under-absorbed in cost accounts ₹25,000; (ii) office overheads over-absorbed ₹12,000; (iii) dividend received ₹18,000 (financial books only); (iv) closing stock valued ₹9,000 higher in financial books than in cost books (opening stocks equal); (v) loss on sale of a machine ₹6,000 (financial books only). Prepare a reconciliation and find the financial profit.',
          'solution': [table(['Item', 'Add ₹', 'Less ₹'], [
              ['Profit as per cost accounts', inr(412000), ''],
              ['Dividend received (only in financial books)', inr(18000), ''],
              ['Office overheads over-absorbed in cost books', inr(12000), ''],
              ['Closing stock higher in financial books', inr(9000), ''],
              ['Factory overheads under-absorbed in cost books', '', inr(25000)],
              ['Loss on sale of machine (only in financial books)', '', inr(6000)],
              ['Profit as per financial accounts', inr(fp), '']], title='Reconciliation statement'),
              note('Rule of thumb: start from costing profit; add items that make financial profit higher, deduct those that make it lower.')],
          'checks': list(ck)}

    ck2 = Checks()
    wip = ck2.add('60000+240000+180000+150000-520000', 'Closing WIP control balance')
    i2 = {'id': 'i2', 'title': 'Work-in-progress control account', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Under non-integrated accounts: opening WIP ₹60,000; materials issued to production ₹2,40,000; direct wages charged ₹1,80,000; production overheads absorbed ₹1,50,000; cost of finished goods transferred ₹5,20,000. Prepare the WIP control account and find the closing balance.',
          'solution': [table(['Dr', '₹', 'Cr', '₹'], [
              ['Balance b/d', inr(60000), 'Finished goods control', inr(520000)],
              ['Stores ledger control', inr(240000), 'Balance c/d', inr(wip)],
              ['Wages control', inr(180000), '', ''],
              ['Production overhead control', inr(150000), '', ''],
              ['Total', inr(630000), 'Total', inr(630000)]], title='Work-in-progress control account')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'In non-integrated (cost ledger) accounting, cost records are kept separately from financial books. Only cost items (materials, labour, overheads, sales) enter the cost ledger; purely financial items such as interest received, dividends, profits or losses on fixed assets and income-tax are left out.',
            'Main accounts: Cost Ledger Control Account (also called General Ledger Adjustment Account) — the link with financial books, recording items whose double entry is in the financial ledger; Stores Ledger Control; Wages Control; Production, Administration and Selling Overhead Control; Work-in-Progress Control; Finished Goods Control; Cost of Sales; and Costing Profit and Loss Account.',
            'Typical entries: purchases — Dr Stores Ledger Control, Cr Cost Ledger Control; materials issued — Dr WIP Control, Cr Stores Ledger Control; wages paid — Dr Wages Control, Cr Cost Ledger Control; overheads absorbed — Dr WIP, Cr Overhead Control; completed output — Dr Finished Goods, Cr WIP; sales — Dr Cost Ledger Control, Cr Costing P&L.',
            'Under- or over-absorbed overheads are transferred to the Costing Profit and Loss Account (or carried forward if seasonal).'],
          'The cost ledger is a self-balancing mirror of the factory, linked to the main books through one control account.',
          'When wages of ₹50,000 are paid, the cost ledger shows Wages Control Dr and Cost Ledger Control Cr — the bank side lives in the financial books.'),
        C('c2', T2, [
            'Integrated accounting keeps one set of books that provides both financial and cost information; there is no need to reconcile two profits.',
            'Accounts like bank, debtors, creditors and fixed assets sit alongside stores control, WIP control and overhead control accounts; entries for cash and credit transactions go straight to the real accounts instead of a cost ledger control account.',
            'Pre-requisites: management decision on the extent of integration, suitable coding, agreed treatment of items such as stock valuation and overheads, and a well-designed system for periodic reports. Advantages: no duplication, lower cost, no reconciliation and quicker information.'],
          'One ledger, two uses: it closes the financial year and also tells managers what each product costs.',
          'Purchasing raw material on credit in integrated books: Dr Stores Ledger Control, Cr Creditors.'),
        C('c3', T3, [
            'When cost and financial books are separate, the two profits differ and are reconciled in a memorandum statement.',
            'Reasons: items only in financial books (interest, dividends, rent received, profit or loss on sale of assets, fines, income-tax, write-offs of goodwill or preliminary expenses); items only in cost books (notional rent or interest charged in costing); under- or over-absorption of overheads; and different stock valuation methods.',
            'Method: start with one profit, add items that increase the other profit, deduct items that decrease it. Over-absorption means cost profit is lower, so it is added when moving to financial profit; under-absorption the reverse.'],
          'Reconciliation explains every rupee of difference so both sets of books can be trusted.',
          'Notional rent of ₹30,000 charged in costing makes cost profit lower; add it back to reach financial profit.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Month-end reconciliation', 'role': 'Cost accountant trainee',
             'situation': 'The plant controller asks why cost profit exceeds book profit by ₹2 lakh.',
             'steps': ['List items only in financial books.', 'Compare overhead absorbed with actual overhead.', 'Compare stock values in both sets.', 'Prepare the reconciliation and investigate unexplained differences.'],
             'takeaway': 'Over- and under-absorption and stock valuation explain most differences.'}]

    mcqs = [
        Q('m1', 'In non-integrated accounts, the account that links cost and financial books is:', ['Cost Ledger Control Account', 'Stores Ledger Control Account', 'Work-in-Progress Control Account', 'Costing P&L Account'], 0,
          'The Cost Ledger Control (General Ledger Adjustment) Account records items whose other side lies in the financial books. In practice: it keeps the cost ledger self-balancing.', 'c1', T1),
        Q('m2', 'Materials issued to production are recorded as:', ['Dr WIP Control, Cr Stores Ledger Control', 'Dr Stores Ledger Control, Cr WIP Control', 'Dr Cost Ledger Control, Cr Stores', 'Dr Finished Goods, Cr Stores'], 0,
          'Issues move cost from stores into production. In practice: indirect materials go to overhead control instead.', 'c1', T1),
        Q('m3', 'Which item appears only in financial books?', ['Dividend received', 'Direct wages', 'Factory overheads absorbed', 'Materials consumed'], 0,
          'Dividends are financial income with no link to production cost. In practice: add it to costing profit to reach financial profit.', 'c3', T3),
        Q('m4', 'Factory overheads over-absorbed in cost accounts mean financial profit is:', ['Higher than costing profit', 'Lower than costing profit', 'Equal', 'Unaffected'], 0,
          'Over-absorption charges more cost in cost books than was actually incurred, so cost profit is lower. In practice: add it when going to financial profit.', 'c3', T3),
        Q('m5', 'In integrated accounts, a credit purchase of materials is recorded as:', ['Dr Stores Ledger Control, Cr Creditors', 'Dr Stores Ledger Control, Cr Cost Ledger Control', 'Dr Purchases, Cr Cash', 'Dr WIP, Cr Creditors'], 0,
          'Integrated books post directly to personal and real accounts; there is no cost ledger control account. In practice: one trial balance serves both needs.', 'c2', T2),
        Q('m6', 'Notional rent charged in cost accounts:', ['Makes cost profit lower than financial profit', 'Makes cost profit higher', 'Has no effect', 'Appears in both books'], 0,
          'Notional charges exist only in costing, reducing cost profit. In practice: add back to reach financial profit.', 'c3', T3),
        Q('m7', 'A key advantage of integrated accounts is:', ['No need to reconcile cost and financial profit', 'More ledgers to check errors', 'Separate staff for costing', 'Lower accuracy'], 0,
          'With one set of books, there is a single profit figure. In practice: requires agreed policies on stock and overheads.', 'c2', T2),
        Q('m8', 'Under-absorbed production overhead at year end is usually transferred to:', ['Costing Profit and Loss Account', 'WIP Control', 'Stores Ledger Control', 'Cost Ledger Control'], 0,
          'Abnormal or year-end under-absorption is written off to Costing P&L (or adjusted via supplementary rates). In practice: seasonal amounts may be carried forward.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Financial-only items', 2, 'concept', 'dividend|loss on sale'), S('s2', 'Over/under-absorption', 2, 'concept', 'absorbed'),
           S('s3', 'Stock difference', 1, 'concept', 'stock'), S('s4', 'Financial profit', 1, 'computation', 'financial', nums=[fp])],
          ['Explain the direction of each item.'], ['Reversing the sign of over-absorption.'], ['Statement.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Debits', 2, 'concept', 'stores|wages|overhead'), S('s2', 'Transfer to finished goods', 1, 'concept', 'finished'), S('s3', 'Closing balance', 1, 'computation', 'balance', nums=[wip])],
          ['Post each item to the correct side.'], ['Crediting overheads absorbed.'], ['T-account.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a cost ledger control account?', 'An account in the cost ledger that records the other side of entries whose double entry is in the financial books, making the cost ledger self-balancing.',
          [P('p1', 'Financial books link', 5, 'financial'), P('p2', 'Self-balancing', 5, 'self-balancing|balanc')], 'c1'),
        V('v2', 'Name items excluded from cost accounts.', 'Purely financial items such as interest received, dividends, profit or loss on sale of fixed assets, fines and income-tax.',
          [P('p1', 'Financial income', 5, 'interest|dividend'), P('p2', 'Appropriations or capital items', 5, 'tax|fixed asset|fine')], 'c3'),
        V('v3', 'What is integrated accounting?', 'A system with one set of books giving both financial and cost information, so no reconciliation is needed.',
          [P('p1', 'One set', 6, 'one set|single'), P('p2', 'Both purposes', 4, 'both|cost and financial')], 'c2'),
        V('v4', 'How does stock valuation cause a difference?', 'If closing stock is valued higher in financial books than in cost books, financial profit is higher by that amount; opening stock works the opposite way.',
          [P('p1', 'Closing stock', 5, 'closing'), P('p2', 'Opposite for opening', 5, 'opening')], 'c3'),
        V('v5', 'How are under-absorbed overheads treated?', 'They are transferred to the Costing Profit and Loss Account or recovered through supplementary rates.',
          [P('p1', 'Costing P&L', 6, 'profit and loss|p&l'), P('p2', 'Supplementary rate', 4, 'supplementary')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Sharma Castings', 'difficulty': 'moderate',
              'case': 'Sharma Castings keeps separate cost books. For the year: costing profit ₹6,50,000; administration overheads under-absorbed ₹20,000; interest on bank deposits ₹15,000 (financial only); goodwill written off ₹40,000; notional interest on capital charged in costing ₹30,000.',
              'mcqs': [
                  M('k1a', 'Effect of under-absorbed administration overheads on financial profit vs. cost profit:', ['Lower', 'Higher', 'No effect', 'Equal'], 0,
                    'Actual cost was higher than absorbed, so financial profit is lower. In practice: deduct it.', 'core', topic=T3),
                  M('k1b', 'Notional interest charged in costing is:', ['Added to cost profit to reach financial profit', 'Deducted', 'Ignored', 'Doubled'], 0,
                    'It reduced cost profit but never appears in financial books. In practice: add back.', 'core', topic=T3),
                  M('k1c', 'Financial profit:', ['₹6,35,000', '₹6,65,000', '₹6,45,000', '₹6,05,000'], 0,
                    '6,50,000 − 20,000 + 15,000 − 40,000 + 30,000 = 6,35,000. In practice: show each item.', 'moderate', check=635000, topic=T3),
                  M('k1d', 'Moving to integrated accounts would:', ['Remove the need for this reconciliation', 'Require two reconciliations', 'Remove overhead absorption', 'Remove stock records'], 0,
                    'One set of books produces one profit. In practice: overheads are still absorbed.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch07', 1, 'Cost Accounting Systems',
                ['Record transactions in non-integrated cost ledgers.',
                 'Explain integrated accounting and its pre-requisites.',
                 'Reconcile costing profit with financial profit.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 45}, 'prereq': ['int-p4-ch06-u01'],
                 'exam_tip': 'In reconciliation, write a one-word reason ("financial only", "over-absorbed") next to each item to fix its direction.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Non-integrated: separate cost ledger linked by Cost Ledger Control A/c.',
                             'Integrated: one set of books, no reconciliation.',
                             'Differences: financial-only items, notional costs, over/under-absorption, stock valuation.'],
                 'remember': ['Over-absorption → add to cost profit to reach financial profit.'],
                 'traps': ['Dividends and asset gains never enter cost books.']},
                [('Link account', 'Cost Ledger Control'), ('Over-absorbed OH', 'Add to cost profit'), ('Under-absorbed OH', 'Deduct'), ('Notional cost', 'Add')],
                viva, cases)
