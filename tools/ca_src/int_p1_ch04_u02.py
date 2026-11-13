"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 2 — AS 3 Cash Flow Statement.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u02'
T1 = 'Purpose of a cash flow statement; cash and cash equivalents'
T2 = 'Operating, investing and financing activities'
T3 = 'Direct and indirect methods for operating cash flow'
T4 = 'Interest, dividends, taxes and special items'
T5 = 'Non-cash transactions and disclosures'


def build():
    ck = Checks()
    op = ck.add('840000+120000+30000+60000-25000', 'Operating profit before working capital changes')
    wc = ck.add('-90000+40000+35000-10000', 'Net working capital change')
    gen = ck.add('1025000-25000', 'Cash generated from operations')
    cfo = ck.add('1000000-180000', 'Net cash from operating activities')
    i1 = {'id': 'i1', 'title': 'Indirect method, step by step', 'difficulty': 'core', 'minutes': 10,
          'q': 'Tapti Industries Ltd. (non-financial) reports profit before tax ₹8,40,000 after charging depreciation ₹1,20,000, loss on sale of a machine ₹30,000 and interest on loans ₹60,000, and after crediting dividend from investments ₹25,000. Debtors rose by ₹90,000, inventory fell by ₹40,000, creditors rose by ₹35,000 and outstanding expenses fell by ₹10,000. Income tax paid was ₹1,80,000. Compute net cash from operating activities.',
          'solution': [table(['Particulars', '₹'], [
              ['Profit before tax', inr(840000)],
              ['Add: depreciation', inr(120000)],
              ['Add: loss on sale of machine (investing item)', inr(30000)],
              ['Add: interest on loans (financing item)', inr(60000)],
              ['Less: dividend received (investing item)', '(25,000)'],
              ['Operating profit before working capital changes', inr(op)],
              ['Increase in debtors', '(90,000)'],
              ['Decrease in inventory', inr(40000)],
              ['Increase in creditors', inr(35000)],
              ['Decrease in outstanding expenses', '(10,000)'],
              ['Cash generated from operations', inr(gen)],
              ['Less: income tax paid', '(1,80,000)'],
              ['Net cash from operating activities', inr(cfo)]], title='Indirect method')],
          'checks': list(ck)}

    ck2 = Checks()
    cfi = ck2.add('-600000+110000+25000-200000', 'Net cash from investing activities')
    cff = ck2.add('500000-150000-60000-100000', 'Net cash from financing activities')
    net = ck2.add('820000-665000+190000', 'Net increase in cash and cash equivalents')
    i2 = {'id': 'i2', 'title': 'Investing and financing for Tapti', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Continuing Tapti: it bought machinery for ₹6,00,000, sold a machine for ₹1,10,000, received dividend ₹25,000, bought investments for ₹2,00,000, issued shares for ₹5,00,000 cash, repaid a loan of ₹1,50,000, paid interest ₹60,000 and paid dividend ₹1,00,000. It also acquired a building worth ₹8,00,000 by issuing shares to the seller. Compute investing and financing cash flows and the net change in cash.',
          'solution': [table(['Activity', 'Items', '₹'], [
              ['Investing', '−6,00,000 + 1,10,000 + 25,000 − 2,00,000', inr(cfi)],
              ['Financing', '5,00,000 − 1,50,000 − 60,000 − 1,00,000', inr(cff)],
              ['Operating (from i1)', '', inr(820000)],
              ['Net increase in cash and cash equivalents', '', inr(net)]], title='Cash flow summary'),
              note('The building bought for shares involves no cash, so it is left out of the statement and disclosed elsewhere in the financial statements.')],
          'checks': list(ck2)}

    act = table(['Activity', 'Examples'], [
        ['Operating', 'Cash from customers; payments to suppliers and employees; taxes (unless clearly investing or financing); royalties; trading securities'],
        ['Investing', 'Buying or selling fixed assets and long-term investments; loans to others (non-financial firms); interest and dividends received'],
        ['Financing', 'Issuing shares or debentures; borrowing and repaying loans; interest and dividends paid']], title='Classifying cash flows (non-financial enterprise)')

    concepts = [
        C('c1', T1, [
            'A cash flow statement shows how an enterprise generated and used cash during the period, helping users judge its ability to produce cash and its need for cash. It also improves comparability, since cash flows do not depend on accounting policies.',
            'Cash means cash on hand and demand deposits with banks. Cash equivalents are short-term, highly liquid investments readily convertible into known amounts of cash with insignificant risk of value change — normally with a maturity of three months or less from the date of acquisition.',
            'Equity shares are not cash equivalents. Movements between cash and cash equivalents are part of cash management, not cash flows.'],
          'Profit is an opinion; cash is a fact.',
          'A 90-day treasury bill bought on the day is a cash equivalent; a 1-year deposit is not.'),
        C('c2', T2, [
            'Operating activities are the principal revenue-producing activities and other activities that are not investing or financing.',
            'Investing activities are buying and selling long-term assets and investments not included in cash equivalents.',
            'Financing activities change the size and composition of owners\' capital and borrowings.',
            'The same item can belong to different heads for different enterprises — for a bank, loans to customers are operating.'],
          'Ask: does it run the business, build the business, or fund the business?',
          'Purchase of a delivery van is investing; the fuel it uses is operating; the loan to buy it is financing.',
          blocks=[act]),
        C('c3', T3, [
            'Operating cash flow may be reported by the direct method (major classes of gross receipts and payments) or the indirect method (profit adjusted for non-cash items, investing or financing items, and working capital changes).',
            'Indirect method adjustments: add back depreciation, amortisation and losses on sale of assets; deduct gains on sale and investment income; adjust for increases or decreases in current assets and current liabilities.',
            'Both methods give the same net operating cash flow; the direct method gives more information for estimating future cash flows.'],
          'The direct method lists the cash; the indirect method reconciles profit to cash.',
          'An increase in debtors means sales were booked but cash not yet collected, so it reduces operating cash.'),
        C('c4', T4, [
            'Interest and dividends received or paid are shown separately and classified consistently. For a financial enterprise, interest paid and interest and dividends received are operating. For others, interest and dividends paid are financing, and interest and dividends received are investing.',
            'Taxes on income are operating unless they can be specifically identified with investing or financing activities.',
            'Cash flows from extraordinary items are classified as operating, investing or financing as appropriate and shown separately.',
            'Foreign currency cash flows are recorded at the rate on the date of the flow; unrealised exchange differences are not cash flows but are shown in reconciling cash balances.',
            'Investments in subsidiaries, associates and joint ventures, and acquisitions or disposals of business units, are investing activities, shown separately.'],
          'Classify interest and dividends by what the enterprise does for a living.',
          'For a finance company, interest received on loans is operating cash flow.'),
        C('c5', T5, [
            'Investing and financing transactions that do not use cash — for example acquiring assets by issuing shares, or converting debt into equity — are excluded from the statement and disclosed elsewhere.',
            'The components of cash and cash equivalents are disclosed and reconciled with the balance sheet.',
            'Significant cash balances not available for use by the group, such as those under exchange restrictions, are disclosed with a management commentary.'],
          'If no cash moved, it does not belong in the cash flow statement.',
          'Bonus shares issued from reserves involve no cash and do not appear.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing a cash flow statement', 'role': 'Accounts executive',
             'situation': 'You have two balance sheets and a profit and loss account and must prepare the statement for the annual report.',
             'steps': ['Start with profit before tax and adjust non-cash and non-operating items.', 'Work out working capital changes.', 'Reconstruct fixed asset and loan accounts for investing and financing flows.', 'Reconcile closing cash with the balance sheet.'],
             'takeaway': 'Ledger reconstructions reveal the hidden cash flows.'}]

    mcqs = [
        Q('m1', 'Which is a cash equivalent?', ['A treasury bill with three months\' maturity when bought', 'Equity shares of a listed company', 'A fixed deposit of 2 years', 'Trade receivables'], 0,
          'Cash equivalents are short-term, highly liquid investments readily convertible into known amounts of cash with insignificant risk of changes in value — usually maturing within three months of acquisition. Shares do not qualify. In practice: check maturity at the purchase date.', 'c1', T1),
        Q('m2', 'Purchase of machinery for cash is classified as:', ['Investing activity', 'Operating activity', 'Financing activity', 'Not a cash flow'], 0,
          'Acquiring long-term assets is an investing activity because it builds productive capacity. Running costs of the machine would be operating, and a loan to fund it financing. In practice: capital expenditure appears under investing.', 'c2', T2),
        Q('m3', 'For a manufacturing company, dividend paid to its shareholders is:', ['Financing activity', 'Operating activity', 'Investing activity', 'Excluded'], 0,
          'For a non-financial enterprise, dividends and interest paid are financing cash flows because they are costs of obtaining finance. Dividends received would be investing. In practice: AS 3 asks for consistent classification.', 'c4', T4),
        Q('m4', 'For a finance company, interest received on loans given is:', ['Operating activity', 'Investing activity', 'Financing activity', 'Not a cash flow'], 0,
          'In a financial enterprise, lending is the main revenue-producing activity, so interest received (and interest paid) are operating cash flows. For other enterprises interest received is investing. In practice: look at the nature of business.', 'c4', T4),
        Q('m5', 'Under the indirect method, an increase in trade creditors is:', ['Added to profit', 'Deducted from profit', 'Shown under financing', 'Ignored'], 0,
          'A rise in creditors means expenses were charged but not paid in cash, so cash is higher than profit suggests; the increase is added back. A rise in debtors would be deducted. In practice: watch the direction of each change.', 'c3', T3),
        Q('m6', 'Profit before tax ₹5,00,000, depreciation ₹80,000, profit on sale of investment ₹20,000, increase in inventory ₹60,000. Cash generated from operations:', ['₹5,00,000', '₹5,60,000', '₹6,00,000', '₹4,40,000'], 0,
          'Add depreciation and deduct the profit on sale (an investing item) to get ₹5,60,000 before working capital; then deduct the increase in inventory of ₹60,000 to get ₹5,00,000. In practice: compute in two stages.', 'c3', T3, 'hard', check=500000),
        Q('m7', 'Income tax paid is generally classified as:', ['Operating, unless specifically identified with investing or financing', 'Always financing', 'Always investing', 'Excluded'], 0,
          'AS 3 treats taxes on income as operating cash flows unless they can be specifically linked with investing or financing activities, in which case they follow those activities. In practice: tax on capital gains could be investing if identifiable.', 'c4', T4),
        Q('m8', 'Acquisition of land by issuing equity shares to the seller:', ['Is excluded from the cash flow statement and disclosed elsewhere', 'Is an investing outflow and financing inflow', 'Is an operating flow', 'Is shown net'], 0,
          'Non-cash investing and financing transactions are left out of the statement because no cash moves; they are disclosed elsewhere in the financial statements. In practice: mention them in a note.', 'c5', T5),
        Q('m9', 'Which method of reporting operating cash flow shows gross cash receipts and gross cash payments?', ['Direct method', 'Indirect method', 'Net method', 'Balance sheet method'], 0,
          'The direct method lists major classes of gross receipts, like cash from customers, and gross payments, like cash to suppliers and staff. The indirect method starts from profit and adjusts it. In practice: both give the same net figure.', 'c3', T3),
        Q('m10', 'Unrealised exchange gain on foreign currency cash held at the year end:', ['Is not a cash flow, but is shown to reconcile opening and closing cash', 'Is an operating inflow', 'Is a financing inflow', 'Is ignored entirely'], 0,
          'Unrealised exchange differences are not cash flows, but the effect on cash held in foreign currency is reported in the statement to reconcile cash at the beginning and end of the period. In practice: show it as a separate line.', 'c4', T4, 'moderate'),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Non-cash and non-operating adjustments', 2, 'computation', 'depreciation', nums=[op]),
           S('s2', 'Working capital changes', 2, 'computation', 'debtors', nums=[gen]),
           S('s3', 'Tax and net operating cash', 2, 'computation', 'tax', nums=[cfo])],
          ['Show both subtotals.'], ['Leaving interest inside operating cash flow.'], ['Statement format.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Investing total', 2, 'computation', 'investing', nums=[cfi]),
           S('s2', 'Financing total', 2, 'computation', 'financing', nums=[cff]),
           S('s3', 'Non-cash item excluded', 1, 'concept', 'no cash|non-cash|left out')],
          ['Group by activity.'], ['Including the building bought for shares.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are cash equivalents?', 'Short-term, highly liquid investments readily convertible into known amounts of cash with insignificant risk of value change, usually maturing within three months of acquisition.',
          [P('p1', 'Highly liquid, insignificant risk', 6, 'liquid|risk'), P('p2', 'Three months', 4, 'three months|3 months')], 'c1'),
        V('v2', 'Name the three heads of a cash flow statement.', 'Operating activities, investing activities and financing activities.',
          [P('p1', 'Operating', 3, 'operating'), P('p2', 'Investing', 3, 'investing'), P('p3', 'Financing', 4, 'financing')], 'c2'),
        V('v3', 'How does the indirect method work?', 'It starts with profit and adjusts for non-cash items like depreciation, for investing and financing items like gains on sale and interest, and for changes in working capital.',
          [P('p1', 'Start from profit', 4, 'profit'), P('p2', 'Adjust non-cash and working capital', 6, 'depreciation|working capital|non-cash')], 'c3'),
        V('v4', 'How are interest and dividends classified by a non-financial company?', 'Interest and dividends paid are financing; interest and dividends received are investing.',
          [P('p1', 'Paid financing', 5, 'financing'), P('p2', 'Received investing', 5, 'investing')], 'c4'),
        V('v5', 'How are non-cash transactions treated?', 'They are excluded from the cash flow statement and disclosed elsewhere in the financial statements.',
          [P('p1', 'Excluded', 6, 'exclud|left out'), P('p2', 'Disclosed elsewhere', 4, 'disclos')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Prakash Finance Ltd. and Prakash Motors Ltd.', 'difficulty': 'moderate',
              'case': 'Two group companies: Prakash Finance Ltd. (an NBFC) received interest of ₹40 lakh on loans to customers and paid interest of ₹25 lakh on borrowings. Prakash Motors Ltd. (a manufacturer) received interest of ₹4 lakh on a deposit and paid interest of ₹9 lakh on a term loan; it also converted ₹50 lakh of debentures into equity shares.',
              'mcqs': [
                  M('k1a', 'In Prakash Finance, interest received and paid are:', ['Both operating', 'Investing and financing', 'Both financing', 'Both investing'], 0,
                    'For a financial enterprise lending and borrowing are its main operations, so interest received and paid are operating cash flows. In practice: the classification follows the business model.', 'core', topic=T4),
                  M('k1b', 'Net financing cash outflow on interest for Prakash Motors:', ['₹9 lakh', '₹5 lakh', '₹13 lakh', '₹4 lakh'], 0,
                    'For a manufacturer, interest paid of ₹9 lakh is a financing outflow, while interest received of ₹4 lakh is an investing inflow; they are not netted. In practice: show receipts and payments separately.', 'moderate', check=9, topic=T4),
                  M('k1c', 'The conversion of debentures into equity is:', ['Excluded and disclosed as a non-cash transaction', 'A financing inflow and outflow of ₹50 lakh', 'An investing flow', 'An operating flow'], 0,
                    'Converting debt into equity involves no cash and is therefore left out of the statement, with disclosure elsewhere in the financial statements. In practice: describe it in the notes.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 2, 'Accounting Standard 3 Cash Flow Statement',
                ['Explain the purpose of a cash flow statement and identify cash equivalents.',
                 'Classify cash flows into operating, investing and financing activities.',
                 'Prepare operating cash flow by the indirect method and understand the direct method.',
                 'Apply the rules for interest, dividends, taxes and non-cash transactions.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 40}, 'prereq': ['int-p1-ch04-u01'],
                 'exam_tip': 'Strip investing and financing items out of profit first, then do working capital; keep a running list of non-cash items to disclose.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Cash equivalents: liquid, insignificant risk, ≤ 3 months from acquisition.', 'Three heads: operating, investing, financing.',
                             'Direct or indirect method for operating cash.', 'Interest/dividends: financial firm → operating; others → paid financing, received investing.',
                             'Taxes operating unless identifiable.', 'Non-cash transactions excluded, disclosed elsewhere.'],
                 'remember': ['Increase in current asset reduces cash; increase in current liability adds.'],
                 'traps': ['Profit on sale of an asset is deducted, not added.']},
                [('Cash equivalent', '≤ 3 months'), ('Interest paid (non-financial)', 'Financing'), ('Dividend received (non-financial)', 'Investing'), ('Taxes', 'Operating (usually)')],
                viva, cases)
