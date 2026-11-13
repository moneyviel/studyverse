"""CA Final · Paper 1 Financial Reporting · Chapter 3 Unit 3 Ind AS 7 Statement of Cash Flows.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch03-u03'
T1 = 'Cash and cash equivalents'
T2 = 'Operating, investing and financing activities'
T3 = 'Direct and indirect methods'
T4 = 'Special items and disclosures'


def build():
    ck = Checks()
    before = ck.add('500+120+40-20-15', 'Operating profit before working capital changes')
    afterwc = ck.add('625-60+30+25', 'Cash generated from operations')
    net = ck.add('620-110', 'Net cash from operating activities')
    i1 = {'id': 'i1', 'title': 'Indirect method', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Sunbeam Ltd. (non-financial company), ₹ lakh: profit before tax 500; depreciation 120; finance cost 40; interest income 20; profit on sale of machinery 15; trade receivables up 60; inventories down 30; trade payables up 25; income tax paid 110. Compute net cash from operating activities.',
          'solution': [table(['Item', '₹ lakh'], [
              ['Profit before tax', inr(500)],
              ['Add: depreciation', inr(120)],
              ['Add: finance cost (financing activity)', inr(40)],
              ['Less: interest income (investing activity)', '(20)'],
              ['Less: profit on sale of machinery (investing activity)', '(15)'],
              ['Operating profit before working capital changes', inr(before)],
              ['Increase in receivables', '(60)'],
              ['Decrease in inventories', inr(30)],
              ['Increase in payables', inr(25)],
              ['Cash generated from operations', inr(afterwc)],
              ['Income tax paid', '(110)'],
              ['Net cash from operating activities', inr(net)]], title='Statement of cash flows — operating section')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Where does it go?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Classify for a manufacturing company: (a) interest paid on a term loan; (b) dividend received from an investee; (c) purchase of a 60-day treasury bill; (d) bank overdraft repayable on demand used in day-to-day cash management; (e) conversion of debentures into equity; (f) cash paid to buy shares in a subsidiary; (g) principal portion of lease payments.',
          'solution': [table(['Item', 'Treatment'], [
              ['(a)', 'Financing activity'],
              ['(b)', 'Investing activity'],
              ['(c)', 'Cash equivalent (maturity within three months from acquisition)'],
              ['(d)', 'Counted within cash and cash equivalents'],
              ['(e)', 'Non-cash — excluded, disclosed elsewhere'],
              ['(f)', 'Investing activity, net of cash acquired, presented separately'],
              ['(g)', 'Financing activity']], title='Ind AS 7 classification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Cash comprises cash on hand and demand deposits. Cash equivalents are near-cash holdings: short-dated, very liquid, easily turned into a known amount of cash and carrying only a tiny risk of value change — typically with a maturity of three months or less from the date of acquisition. Equity investments are generally excluded.',
            'Bank overdrafts repayable on demand that are used as an everyday part of cash management count within cash and cash equivalents.',
            'Movements between cash and cash equivalents are not cash flows. The components and a reconciliation to the balance sheet are disclosed, along with significant balances not available for use by the group.'],
          'Cash equivalents are near-cash with almost no price risk — not every short-term investment.',
          'A 3-year bond bought with 2 months left to maturity qualifies; one bought at issue does not become a cash equivalent later.'),
        C('c2', T2, [
            'Operating activities: principal revenue-producing activities and other activities that are not investing or financing — receipts from customers, payments to suppliers and employees, income taxes (unless specifically identified with investing or financing).',
            'Investing activities: acquisition and disposal of long-term assets and investments not included in cash equivalents — purchase and sale of property, plant and equipment, loans to others, purchase of investments.',
            'Financing activities: changes in the size and composition of contributed equity and borrowings — issue of shares, buy-back, borrowings and repayments, principal on leases.',
            'For entities other than financial institutions, interest paid and dividends paid are financing; interest and dividends received are investing. For financial institutions, interest paid and received and dividends received are usually operating.'],
          'Ask: does the flow arise from running the business, building its asset base, or funding it?',
          'Sale of an old machine is investing even though it arises during normal operations.'),
        C('c3', T3, [
            'Operating cash flows may be presented by the direct method (major classes of gross receipts and payments) or the indirect method (profit or loss adjusted for non-cash items, working capital changes and investing or financing items).',
            'Under the indirect method: add depreciation, amortisation, impairment, unrealised foreign exchange losses and finance costs; deduct investment income and gains on disposal of non-current assets; adjust for changes in inventories, operating receivables and payables; deduct taxes paid.',
            'Investing and financing activities are reported gross (major classes of receipts and payments), except where netting is permitted, such as items with quick turnover, large amounts and short maturities, or cash receipts and payments on behalf of customers.'],
          'The indirect method explains why profit is not the same as cash.',
          'A rise in receivables means sales were recognised but cash has not come in — deduct it.'),
        C('c4', T4, [
            'Foreign currency cash flows are translated at the rates on the dates of the cash flows (or an approximate average rate); the effect of exchange rate changes on cash held is shown separately in the reconciliation.',
            'Cash flows from obtaining or losing control of subsidiaries are presented separately as investing activities, net of cash acquired or disposed of. Changes in ownership that do not change control are financing activities.',
            'Non-cash investing and financing transactions (e.g. assets acquired by issuing shares, conversion of debt to equity, assets taken on lease) are excluded and disclosed elsewhere.',
            'Entities disclose changes in liabilities arising from financing activities, separating cash flows from non-cash changes (acquisitions, exchange differences, fair value changes), and the reconciliation of cash and cash equivalents.'],
          'What did not involve cash stays out of the statement but must still be explained.',
          'Buying a building by issuing shares appears only in the notes as a non-cash transaction.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Drafting the cash flow statement', 'role': 'Article assistant',
             'situation': 'The finance team gives you two balance sheets and a profit and loss account.',
             'steps': ['Compute movements in each balance sheet item.', 'Identify non-cash items and reclassifications.', 'Prepare the operating section by the indirect method.', 'Build investing and financing sections and reconcile closing cash.'],
             'takeaway': 'If the closing cash does not reconcile, a balance sheet movement has been missed.'}]

    mcqs = [
        Q('m1', 'A cash equivalent normally has a maturity, from the date of acquisition, of:', ['Three months or less', 'One year or less', 'Six months or less', 'Any period if listed'], 0,
          'Short maturity keeps value risk insignificant. In practice: equity shares are generally excluded.', 'c1', T1),
        Q('m2', 'For a non-financial company, interest paid is classified as:', ['Financing activity', 'Operating activity', 'Investing activity', 'Non-cash'], 0,
          'Ind AS 7 fixes this classification for entities other than financial institutions. In practice: interest received is investing.', 'c2', T2),
        Q('m3', 'Dividends received by a manufacturing company are:', ['Investing activity', 'Operating activity', 'Financing activity', 'Excluded'], 0,
          'Returns on investments are investing for non-financial entities. In practice: financial institutions show them as operating.', 'c2', T2),
        Q('m4', 'Under the indirect method, an increase in inventories is:', ['Deducted from profit', 'Added to profit', 'Shown in investing', 'Ignored'], 0,
          'Cash was spent on stock not yet expensed. In practice: decreases are added back.', 'c3', T3),
        Q('m5', 'Conversion of debentures into equity shares is:', ['A non-cash transaction excluded from the statement and disclosed', 'A financing inflow and outflow', 'An investing activity', 'An operating activity'], 0,
          'No cash moves, so it is excluded but disclosed. In practice: note it under non-cash transactions.', 'c4', T4),
        Q('m6', 'Cash paid to acquire a subsidiary is presented:', ['As investing, net of cash acquired, separately', 'As financing', 'As operating', 'Gross without netting'], 0,
          'Obtaining control is investing; cash held by the subsidiary is netted. In practice: disclose consideration details.', 'c4', T4),
        Q('m7', 'Bank overdrafts repayable on demand and part of cash management are:', ['Included in cash and cash equivalents', 'Financing activities', 'Investing activities', 'Operating liabilities'], 0,
          'Ind AS 7 counts such overdrafts within cash and cash equivalents. In practice: balances fluctuating between positive and overdrawn indicate this.', 'c1', T1),
        Q('m8', 'Profit ₹200; depreciation ₹50; increase in receivables ₹30; decrease in payables ₹10. Operating cash flow (ignore tax):', ['₹210', '₹290', '₹230', '₹270'], 0,
          '200 + 50 − 30 − 10 = 210. In practice: show each adjustment.', 'c3', T3, 'moderate', check=210),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Non-cash and reclassifications', 2, 'computation', 'depreciation|finance', nums=[before]), S('s2', 'Working capital', 2, 'computation', 'receivables|payables', nums=[afterwc]),
           S('s3', 'Tax and net', 2, 'computation', 'tax', nums=[net])],
          ['Explain each adjustment.'], ['Adding increase in receivables.'], ['Statement.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Interest and dividend', 1.5, 'concept', 'financing|investing'), S('s2', 'Cash equivalents', 1.5, 'concept', 'cash equivalent'), S('s3', 'Non-cash and subsidiary', 2, 'concept', 'non-cash|subsidiar')],
          ['Give a one-line reason.'], ['Treating conversion as a cash flow.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Define cash equivalents.', 'Short-term, highly liquid investments easily convertible into known amounts of cash with insignificant risk of value change, usually maturing within three months of acquisition.',
          [P('p1', 'Liquid and short-term', 5, 'liquid|short'), P('p2', 'Three months', 5, 'three months|3 months')], 'c1'),
        V('v2', 'How are interest and dividends classified by a non-financial entity?', 'Interest and dividends paid are financing; interest and dividends received are investing.',
          [P('p1', 'Paid financing', 5, 'financing'), P('p2', 'Received investing', 5, 'investing')], 'c2'),
        V('v3', 'Distinguish the direct and indirect methods.', 'The direct method shows gross operating receipts and payments; the indirect method adjusts profit for non-cash items, working capital changes and non-operating items.',
          [P('p1', 'Direct gross', 5, 'gross|receipts'), P('p2', 'Indirect adjusts profit', 5, 'adjust|profit')], 'c3'),
        V('v4', 'Give two non-cash transactions.', 'Acquiring assets by issuing shares and converting debt into equity, along with assets obtained under leases.',
          [P('p1', 'Shares for assets', 5, 'shares|issuing'), P('p2', 'Conversion or lease', 5, 'convert|lease')], 'c4'),
        V('v5', 'What reconciliation of financing liabilities is required?', 'A reconciliation of opening and closing liabilities from financing activities showing cash flows and non-cash changes such as acquisitions, exchange differences and fair value changes.',
          [P('p1', 'Opening to closing', 5, 'opening|closing'), P('p2', 'Non-cash changes', 5, 'non-cash')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Tejas Engineering Ltd.', 'difficulty': 'moderate',
              'case': 'Tejas Engineering Ltd. in 2026-27: bought a machine for ₹80 lakh, paying ₹30 lakh in cash and issuing shares for the rest; sold land for ₹45 lakh (book value ₹25 lakh); repaid a term loan of ₹50 lakh with interest of ₹6 lakh; and received a dividend of ₹4 lakh from an associate.',
              'mcqs': [
                  M('k1a', 'Cash outflow for the machine in investing activities:', ['₹30 lakh', '₹80 lakh', '₹50 lakh', 'Nil'], 0,
                    'Only the cash paid is shown; ₹50 lakh in shares is a non-cash transaction disclosed separately. In practice: note it.', 'moderate', check=30, topic=T4),
                  M('k1b', 'Sale of land appears as:', ['Investing inflow of ₹45 lakh; ₹20 lakh gain deducted in operating', 'Operating inflow of ₹45 lakh', 'Investing inflow of ₹20 lakh', 'Financing inflow'], 0,
                    'Sale proceeds are investing; the gain is removed from profit in the indirect method. In practice: gross proceeds are shown.', 'moderate', topic=T2),
                  M('k1c', 'Loan repayment and interest are:', ['Both financing outflows (₹56 lakh)', 'Repayment financing, interest operating', 'Both operating', 'Both investing'], 0,
                    'Principal and interest paid are financing for a non-financial entity. In practice: show separately.', 'core', topic=T2),
                  M('k1d', 'Dividend from the associate is:', ['Investing inflow', 'Operating inflow', 'Financing inflow', 'Non-cash'], 0,
                    'Dividends received are investing for non-financial entities. In practice: separate from operating income.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch03', 3, 'Ind AS 7 "Statement of Cash Flows"',
                ['Identify cash and cash equivalents.',
                 'Classify cash flows into operating, investing and financing activities.',
                 'Prepare operating cash flows by the indirect and direct methods.',
                 'Treat foreign currency, subsidiaries, non-cash transactions and required disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 40}, 'prereq': ['fin-p1-ch03-u02'],
                 'exam_tip': 'Reconcile your closing cash to the balance sheet — it is the best check of a cash flow answer.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Cash equivalents: ≤ 3 months from acquisition, insignificant risk.',
                             'Overdrafts in cash management form part of cash.',
                             'Non-financial: interest/dividends paid → financing; received → investing.',
                             'Indirect method: profit ± non-cash ± WC − tax.',
                             'Subsidiary acquisitions net of cash; non-cash transactions disclosed; financing liability reconciliation.'],
                 'remember': ['Lease principal is financing.'],
                 'traps': ['Gains on disposal are removed from operating, proceeds shown in investing.']},
                [('Cash equivalent', '≤ 3 months'), ('Interest paid', 'Financing'), ('Dividend received', 'Investing'), ('Non-cash', 'Disclose, exclude')],
                viva, cases)
