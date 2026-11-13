"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 11 Unit 2 — Cash Flow Statements (preparation).
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch11-u02'
T1 = 'Why prepare a cash flow statement; sources and uses'
T2 = 'Direct method: receipts and payments'
T3 = 'Indirect method: from profit to operating cash'
T4 = 'Reconstructing accounts for hidden cash flows'
T5 = 'Investing and financing items in company questions'


def build():
    ck = Checks()
    rec = ck.add('5000000+600000-800000', 'Cash received from customers (₹)')
    pur = ck.add('3000000+500000-400000', 'Purchases (₹)')
    pay = ck.add('3100000+300000-350000', 'Cash paid to suppliers (₹)')
    i1 = {'id': 'i1', 'title': 'Direct method figures', 'difficulty': 'core', 'minutes': 8,
          'q': 'Maitri Ltd.: sales ₹50,00,000 (all credit); trade receivables ₹6,00,000 opening and ₹8,00,000 closing; cost of goods sold ₹30,00,000; inventory ₹4,00,000 opening and ₹5,00,000 closing; trade payables ₹3,00,000 opening and ₹3,50,000 closing (all purchases on credit). Compute cash received from customers and cash paid to suppliers.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Cash from customers', 'Sales + opening receivables − closing receivables', inr(rec)],
              ['Purchases', 'Cost of goods sold + closing inventory − opening inventory', inr(pur)],
              ['Cash to suppliers', 'Purchases + opening payables − closing payables', inr(pay)]], title='Direct method workings')],
          'checks': list(ck)}

    ck2 = Checks()
    buy = ck2.add('2600000+300000+150000-2000000', 'Machinery purchased (₹)')
    lossv = ck2.add('150000-120000', 'Loss on sale of machinery (₹)')
    tax = ck2.add('200000+350000-250000', 'Income tax paid (₹)')
    i2 = {'id': 'i2', 'title': 'Finding the hidden figures', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Nupur Ltd.\'s machinery (at written-down value) was ₹20,00,000 at the start and ₹26,00,000 at the end. Depreciation for the year was ₹3,00,000. A machine with WDV ₹1,50,000 was sold for ₹1,20,000. Provision for tax was ₹2,00,000 at the start and ₹2,50,000 at the end; the tax charge for the year was ₹3,50,000. Compute machinery bought, the loss on sale and tax paid, and show where each appears.',
          'solution': [table(['Item', 'Working', '₹', 'Where'], [
              ['Machinery bought', 'Closing + depreciation + WDV sold − opening', inr(buy), 'Investing outflow'],
              ['Sale proceeds', '', inr(120000), 'Investing inflow'],
              ['Loss on sale', '1,50,000 − 1,20,000', inr(lossv), 'Added back in operating (indirect)'],
              ['Tax paid', 'Opening provision + charge − closing provision', inr(tax), 'Operating outflow']], title='Account reconstruction')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A cash flow statement explains how cash and cash equivalents changed between two balance sheet dates, helping users judge liquidity, solvency and the quality of earnings.',
            'Sources of cash include issue of shares or debentures, long-term borrowing, sale of investments and fixed assets, and cash from operations. Uses include redemption of shares or debentures, repayment of loans, purchase of fixed assets and investments, payment of tax and dividends, and operating losses.',
            'Every change in each balance sheet item must be explained separately; the net result reconciles opening and closing cash and cash equivalents.'],
          'Each balance sheet movement tells part of the cash story.',
          'An increase in share capital by a cash issue is a financing inflow.'),
        C('c2', T2, [
            'The direct method lists major classes of gross cash receipts and payments from operations.',
            'Cash from customers = sales (credit and cash) + opening receivables − closing receivables (adjusting for bills receivable and write-offs).',
            'Purchases = cost of goods sold + closing inventory − opening inventory; cash to suppliers = purchases + opening payables − closing payables.',
            'Cash paid for expenses = expense charged + opening outstanding − closing outstanding − opening prepaid + closing prepaid. Non-cash expenses such as depreciation are left out.'],
          'Turn each accrual figure into cash by adjusting for opening and closing balances.',
          'Rent expense ₹1,20,000 with outstanding rent rising by ₹10,000 means ₹1,10,000 was paid.'),
        C('c3', T3, [
            'The indirect method starts with net profit before tax and extraordinary items and adjusts for: non-cash items (depreciation, amortisation, provisions); non-operating items (gains or losses on sale of assets or investments, interest and dividend income, finance costs); and changes in working capital (current assets and current liabilities other than cash and short-term borrowings).',
            'Increase in current assets reduces cash; increase in current liabilities increases cash, and vice versa.',
            'Income tax paid is deducted to arrive at net cash from operating activities; extraordinary items are shown separately under the relevant head.'],
          'Profit is reconciled to cash by removing what is not cash and not operating.',
          'Goodwill written off is added back because no cash left the business.'),
        C('c4', T4, [
            'Many cash flows are not given directly and must be found by preparing ledger accounts from opening and closing balances.',
            'Fixed asset (at WDV): purchases = closing + depreciation + WDV of assets sold − opening. With gross block and accumulated depreciation given separately, both accounts are reconstructed.',
            'Provision for tax: tax paid = opening provision + current year charge − closing provision. Dividend paid = dividends declared during the year (proposed dividends of last year, declared this year).',
            'Investments: purchases or sales are worked out from opening and closing balances adjusted for profit or loss on sale.'],
          'When a cash figure is missing, rebuild the account and solve for it.',
          'Closing investments ₹8 lakh, opening ₹5 lakh, sold at cost ₹2 lakh — so ₹5 lakh was bought.'),
        C('c5', T5, [
            'Investing activities include purchase and sale of fixed assets and investments and interest and dividends received (for non-financial companies).',
            'Financing activities include proceeds from issue of shares and debentures (with premium), redemption of preference shares and debentures (with premium), long-term borrowing and repayment, interest and dividends paid.',
            'Non-cash transactions — bonus shares, conversion of debentures, assets bought by issuing shares — are excluded and disclosed. Bank overdraft or short-term borrowings may be treated as part of financing or of cash, as the question indicates.'],
          'Ask whether each item is about long-term assets (investing) or about owners and lenders (financing).',
          'Premium paid on redeeming debentures is a financing outflow along with the face value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Annual report cash flow statement', 'role': 'Accounts executive',
             'situation': 'You have two years\' balance sheets, the profit and loss and notes on asset sales, tax and dividends.',
             'steps': ['Reconstruct fixed asset, investment and tax accounts.', 'Compute operating cash by the indirect method.', 'List investing and financing flows with sources.', 'Reconcile to the change in cash.'],
             'takeaway': 'The reconciliation proves the statement.'}]

    mcqs = [
        Q('m1', 'Sales ₹40 lakh; opening debtors ₹5 lakh; closing debtors ₹7 lakh. Cash received from customers:', ['₹38 lakh', '₹42 lakh', '₹40 lakh', '₹45 lakh'], 0,
          'Receipts = sales + opening debtors − closing debtors = 40 + 5 − 7 = ₹38 lakh; the rise in debtors means some sales are still uncollected. In practice: adjust for bad debts too.', 'c2', T2, 'core', check=38),
        Q('m2', 'Cost of goods sold ₹60 lakh; opening stock ₹8 lakh; closing stock ₹11 lakh. Purchases:', ['₹63 lakh', '₹57 lakh', '₹60 lakh', '₹79 lakh'], 0,
          'Purchases = COGS + closing stock − opening stock = 60 + 11 − 8 = ₹63 lakh. This is then adjusted for creditors to find cash paid. In practice: watch for cash purchases.', 'c2', T2, 'moderate', check=63),
        Q('m3', 'Under the indirect method, a decrease in trade receivables is:', ['Added to profit', 'Deducted from profit', 'Shown under investing', 'Ignored'], 0,
          'A fall in receivables means more cash was collected than the year\'s sales, so it adds to operating cash. A rise would be deducted. In practice: watch the sign of each change.', 'c3', T3),
        Q('m4', 'Opening tax provision ₹4 lakh; tax charged ₹9 lakh; closing provision ₹5 lakh. Tax paid:', ['₹8 lakh', '₹9 lakh', '₹10 lakh', '₹5 lakh'], 0,
          'Tax paid = opening provision + charge − closing provision = 4 + 9 − 5 = ₹8 lakh, shown as an operating outflow unless specifically identified elsewhere. In practice: rebuild the tax account.', 'c4', T4, 'moderate', check=8),
        Q('m5', 'Machinery WDV: opening ₹30 lakh, closing ₹34 lakh; depreciation ₹5 lakh; WDV of machinery sold ₹2 lakh. Purchases of machinery:', ['₹11 lakh', '₹9 lakh', '₹4 lakh', '₹7 lakh'], 0,
          'Purchases = closing + depreciation + WDV sold − opening = 34 + 5 + 2 − 30 = ₹11 lakh, an investing outflow. In practice: the sale proceeds are a separate inflow.', 'c4', T4, 'hard', check=11),
        Q('m6', 'Profit on sale of an investment under the indirect method is:', ['Deducted from profit; proceeds shown under investing', 'Added to profit', 'Shown under financing', 'Ignored'], 0,
          'The gain is not operating cash, so it is removed from profit; the whole sale proceeds appear as an investing inflow. In practice: avoid counting the gain twice.', 'c3', T3),
        Q('m7', 'Redemption of debentures at a premium is shown as:', ['A financing outflow including the premium', 'An investing outflow', 'An operating outflow', 'A non-cash item'], 0,
          'Repaying debentures is a financing activity; the cash paid, including any premium, is a financing outflow. In practice: show it on one line.', 'c5', T5),
        Q('m8', 'Issue of bonus shares is:', ['Excluded, as it involves no cash', 'A financing inflow', 'A financing outflow', 'An investing item'], 0,
          'Bonus shares only capitalise reserves; no cash moves, so they are excluded from the cash flow statement and may be disclosed. In practice: check share capital movements carefully.', 'c5', T5),
        Q('m9', 'Rent charged ₹2,40,000; outstanding rent rose from ₹20,000 to ₹30,000. Rent paid:', ['₹2,30,000', '₹2,50,000', '₹2,40,000', '₹2,10,000'], 0,
          'Rent paid = charge + opening outstanding − closing outstanding = 2,40,000 + 20,000 − 30,000 = ₹2,30,000; the rise in outstanding rent means less was paid. In practice: adjust prepaid amounts the other way.', 'c2', T2, 'moderate', check=230000),
        Q('m10', 'Dividend received by a manufacturing company is shown under:', ['Investing activities', 'Operating activities', 'Financing activities', 'Not shown'], 0,
          'For non-financial enterprises, interest and dividends received are investing inflows; interest and dividends paid are financing outflows. In practice: deduct dividend income from profit first.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Receipts from customers', 2, 'computation', 'customers', nums=[rec]),
           S('s2', 'Purchases', 1.5, 'computation', 'purchases', nums=[pur]),
           S('s3', 'Payments to suppliers', 1.5, 'computation', 'suppliers', nums=[pay])],
          ['Work through purchases first.'], ['Using COGS as cash paid.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Machinery purchased', 2, 'computation', 'bought', nums=[buy]),
           S('s2', 'Loss on sale', 1, 'computation', 'loss', nums=[lossv]),
           S('s3', 'Tax paid', 2, 'computation', 'tax', nums=[tax])],
          ['Rebuild each account.'], ['Treating the tax charge as tax paid.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'How is cash received from customers computed?', 'Sales plus opening receivables less closing receivables, adjusted for bad debts and bills receivable.',
          [P('p1', 'Sales adjusted', 5, 'sales'), P('p2', 'Opening and closing receivables', 5, 'receivable|debtor')], 'c2'),
        V('v2', 'How is tax paid found?', 'Opening provision for tax plus the year\'s tax charge less the closing provision.',
          [P('p1', 'Opening plus charge', 5, 'opening', 'charge'), P('p2', 'Less closing', 5, 'closing')], 'c4'),
        V('v3', 'How are working capital changes treated in the indirect method?', 'Increases in current assets and decreases in current liabilities reduce cash; decreases in current assets and increases in current liabilities add to it.',
          [P('p1', 'Current assets', 5, 'current assets'), P('p2', 'Current liabilities', 5, 'current liabilities')], 'c3'),
        V('v4', 'How do you find fixed assets purchased from WDV balances?', 'Closing WDV plus depreciation plus WDV of assets sold less opening WDV.',
          [P('p1', 'Closing plus depreciation plus sold', 6, 'depreciation'), P('p2', 'Less opening', 4, 'opening')], 'c4'),
        V('v5', 'Give two non-cash transactions excluded from the statement.', 'Issue of bonus shares, conversion of debentures into shares, and acquisition of assets by issuing shares.',
          [P('p1', 'Bonus shares', 5, 'bonus'), P('p2', 'Conversion or assets for shares', 5, 'conversion|issuing shares|for shares')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Pallavi Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Pallavi Textiles Ltd. reports profit before tax ₹24 lakh after depreciation ₹6 lakh, profit on sale of land ₹4 lakh and interest on debentures ₹2 lakh. Inventory rose by ₹3 lakh and payables rose by ₹1 lakh. Tax paid was ₹5 lakh. It also redeemed debentures of ₹10 lakh at a 5% premium.',
              'mcqs': [
                  M('k1a', 'Operating profit before working capital changes:', ['₹28 lakh', '₹24 lakh', '₹32 lakh', '₹30 lakh'], 0,
                    'Add depreciation ₹6 lakh and interest ₹2 lakh, deduct profit on land ₹4 lakh: 24 + 6 + 2 − 4 = ₹28 lakh. In practice: interest goes to financing.', 'moderate', check=28, topic=T3),
                  M('k1b', 'Net cash from operating activities:', ['₹21 lakh', '₹26 lakh', '₹23 lakh', '₹28 lakh'], 0,
                    'From ₹28 lakh, deduct the inventory rise ₹3 lakh, add the payables rise ₹1 lakh = ₹26 lakh, less tax ₹5 lakh = ₹21 lakh. In practice: show cash generated before tax as a subtotal.', 'hard', check=21, topic=T3),
                  M('k1c', 'Financing outflow on redemption of debentures:', ['₹10.5 lakh', '₹10 lakh', '₹0.5 lakh', '₹9.5 lakh'], 0,
                    'Cash paid is the face value ₹10 lakh plus 5% premium ₹0.5 lakh = ₹10.5 lakh, a financing outflow. In practice: interest paid is another financing line.', 'core', check=10.5, topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch11', 2, 'Cash Flow Statement',
                ['Explain the purpose of a cash flow statement and identify sources and uses of cash.',
                 'Compute operating cash flows by the direct and indirect methods.',
                 'Reconstruct accounts to find hidden cash flows.',
                 'Classify investing and financing flows in company problems.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 50}, 'prereq': ['int-p1-ch11-u01'],
                 'exam_tip': 'Prepare the working accounts (fixed assets, investments, tax, dividends) before drafting the statement.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Explain every balance sheet change.', 'Direct: receipts and payments from accrual figures adjusted for balances.',
                             'Indirect: profit + non-cash − non-operating ± working capital − tax.', 'Rebuild fixed asset, investment and tax accounts.',
                             'Investing: assets and investments; financing: owners and lenders.', 'Exclude non-cash transactions.'],
                 'remember': ['Purchases = COGS + closing stock − opening stock.'],
                 'traps': ['Tax charged is not tax paid.']},
                [('Receipts', 'Sales + opening − closing debtors'), ('Tax paid', 'Opening + charge − closing'), ('Assets bought (WDV)', 'Closing + dep + sold − opening')],
                viva, cases)
