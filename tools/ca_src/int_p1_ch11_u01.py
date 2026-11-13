"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 11 Unit 1 — Preparation of Financial Statements of Companies.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch11-u01'
T1 = 'Kinds of companies and books of account'
T2 = 'Financial statements and their requisites'
T3 = 'Schedule III: balance sheet and current/non-current split'
T4 = 'Schedule III: statement of profit and loss and notes'
T5 = 'Distributable profits and dividends'


def build():
    ck = Checks()
    rate = ck.add('(10+12+14)/3', 'Maximum rate: average of the last three years (%)')
    cap = ck.add('(5000000+3000000)/10', 'Maximum amount drawable from reserves (₹)')
    net = ck.add('800000-200000', 'Available after setting off current year loss (₹)')
    div = ck.add('5000000*12/100', 'Dividend at 12% on paid-up capital (₹)')
    i1 = {'id': 'i1', 'title': 'Dividend out of accumulated profits', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Kirti Ltd. has a loss of ₹2,00,000 this year and wants to pay equity dividend out of accumulated profits. Paid-up equity capital is ₹50,00,000 and free reserves ₹30,00,000. Dividends in the last three years were 10%, 12% and 14%. What is the maximum dividend it can declare?',
          'solution': [table(['Test', 'Working', 'Result'], [
              ['Maximum rate', 'Average of 10%, 12%, 14%', f'{R(rate)}%'],
              ['Maximum withdrawal', '1/10 × (50,00,000 + 30,00,000)', inr(cap)],
              ['Less: current year loss set off first', '8,00,000 − 2,00,000', inr(net)],
              ['Dividend at 12%', '12% × 50,00,000', inr(div)]], title='Declaring dividend out of reserves'),
              p('The 12% dividend (₹6,00,000) uses exactly the amount available after the loss is absorbed, so it can be declared. The dividend must be deposited in a separate bank account within five days of declaration.')],
          'checks': list(ck)}

    ck2 = Checks()
    oc = ck2.add('12', 'Operating cycle assumed when not identifiable (months)')
    i2 = {'id': 'i2', 'title': 'Current or non-current?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Classify under Schedule III for a company with a normal 12-month operating cycle: (a) a term loan instalment due in 8 months; (b) the balance of the same loan due after 3 years; (c) trade receivables due in 60 days; (d) a fixed deposit maturing in 15 months; (e) inventory of a whisky maker that matures over 3 years (its normal operating cycle).',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Current liability (current maturities of long-term debt)', 'Due within 12 months'],
              ['(b)', 'Non-current borrowing', 'Due after 12 months'],
              ['(c)', 'Current asset', 'Realised within the operating cycle'],
              ['(d)', 'Non-current asset (other bank balance / investment)', 'Matures after 12 months'],
              ['(e)', 'Current asset', 'Held for sale in the normal operating cycle, even if longer than 12 months']], title='Schedule III classification'),
              note(f'Where the operating cycle cannot be identified, it is taken as {R(oc)} months.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'The Companies Act, 2013 recognises several kinds of companies: limited by shares, limited by guarantee and unlimited; private (restricts share transfer, up to 200 members, no public invitation), public, one person company, small company, government company (at least 51% capital held by governments), holding and subsidiary companies, and foreign companies.',
            'Section 128: every company keeps books of account at its registered office (or elsewhere in India as the Board decides, with notice to the Registrar) on an accrual basis and by double entry, giving a true and fair view; they may be kept electronically. Books are preserved for at least eight years.',
            'Statutory registers include registers of members, debenture holders, charges, contracts with related parties, directors and KMP, and minutes books. An annual return is filed each year.'],
          'The Act fixes both what kind of company you are and how you keep your books.',
          'A private company limits members to 200 and cannot invite the public to subscribe.'),
        C('c2', T2, [
            'Under section 2(40), financial statements include a balance sheet, a statement of profit and loss (income and expenditure account for not-for-profit companies), a cash flow statement, a statement of changes in equity (where applicable) and explanatory notes. A one person company, small company and dormant company may omit the cash flow statement.',
            'Financial statements must give a true and fair view, comply with notified accounting standards and be in the form in Schedule III. They are approved by the Board and signed as required before audit and adoption.',
            'Listed companies also prepare periodic (quarterly) results, approved by the Board and filed as SEBI requires.'],
          'The set of statements, its form and its true-and-fair quality are all laid down by law.',
          'A small company may present its accounts without a cash flow statement.'),
        C('c3', T3, [
            'Schedule III Division I (for companies following notified Accounting Standards) presents the balance sheet in vertical form: Equity and Liabilities (shareholders\' funds, share application money pending allotment, non-current liabilities, current liabilities) and Assets (non-current and current).',
            'An asset is current if it is expected to be realised, sold or consumed in the normal operating cycle; held mainly for trading; expected to be realised within twelve months after the reporting date; or is cash or cash equivalent not restricted for at least twelve months. A liability is current if it is expected to be settled in the operating cycle, held for trading, due within twelve months, or the company lacks an unconditional right to defer settlement for at least twelve months.',
            'The operating cycle is the time between acquiring assets for processing and their realisation in cash; where it cannot be identified, it is taken as twelve months.',
            'Notes give details such as share capital (authorised, issued, subscribed, reconciliation of shares, shareholders holding over 5%, promoter holdings), reserves, borrowings with terms, ageing of trade payables and receivables, and specified ratios.'],
          'The balance sheet follows a fixed shape with a current/non-current split based on the operating cycle.',
          'The portion of a term loan repayable within the year moves to current liabilities.'),
        C('c4', T4, [
            'The statement of profit and loss shows revenue from operations, other income, total income; expenses by nature (cost of materials consumed, purchases of stock-in-trade, changes in inventories, employee benefits, finance costs, depreciation and amortisation, other expenses); profit before exceptional and extraordinary items and tax; tax expense (current and deferred); profit from continuing and discontinuing operations; and earnings per share.',
            'Additional information in notes includes the break-up of revenue, other income, finance costs, payments to auditors, and details of items exceeding prescribed thresholds.',
            'Figures may be rounded off as permitted by Schedule III depending on turnover, and corresponding figures of the previous period are given.'],
          'Expenses in the profit and loss follow their nature, not their function.',
          'Salaries of production staff appear under "Employee benefits expense", not cost of goods.'),
        C('c5', T5, [
            'Section 123: dividend may be declared out of profits of the year after providing depreciation under Schedule II, out of undistributed profits of earlier years after depreciation, or both, and out of money provided by government for the purpose under a guarantee. Transfer of a part of profits to reserves before declaring dividend is optional.',
            'Dividend out of accumulated profits when the year\'s profits are inadequate: the rate cannot exceed the average of the three preceding years (unless no dividend was declared in any of them); the amount drawn cannot exceed one-tenth of paid-up share capital plus free reserves per the latest audited statements; and the amount drawn is first used to set off the current year\'s losses before any equity dividend.',
            'Interim dividend may be declared by the Board out of surplus in profit and loss and profits of the current period; if there is a loss up to the quarter before declaration, its rate cannot exceed the average of the three preceding years.',
            'Dividend is deposited in a separate scheduled bank account within five days of declaration and paid within 30 days; amounts unpaid are moved to an Unpaid Dividend Account, and sums unclaimed for seven years go to the Investor Education and Protection Fund. Dividend is paid only in cash (including cheque or electronic modes) to registered shareholders.'],
          'Dividends come only from genuine profits, with strict limits when reserves are tapped.',
          'Bonus shares are not dividend — they only capitalise profits.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing Schedule III accounts', 'role': 'Accounts executive',
             'situation': 'You have a trial balance of a private company and must prepare its balance sheet, profit and loss and notes.',
             'steps': ['Map ledger heads to Schedule III line items.', 'Split each asset and liability into current and non-current.', 'Prepare the share capital and reserves notes.', 'Check dividend limits before the Board proposes a dividend.'],
             'takeaway': 'Mapping and classification come before arithmetic.'}]

    mcqs = [
        Q('m1', 'Books of account under section 128 must be preserved for at least:', ['Eight years', 'Five years', 'Ten years', 'Six years'], 0,
          'Companies must keep books of account and relevant vouchers for at least eight financial years immediately preceding the current year, on accrual basis and double entry, at the registered office or another place notified. In practice: electronic records are allowed.', 'c1', T1),
        Q('m2', 'A government company is one in which governments together hold paid-up share capital of at least:', ['51%', '26%', '50%', '75%'], 0,
          'A government company has at least 51% of its paid-up share capital held by the Central Government, State Governments or both, and includes its subsidiaries. In practice: check the shareholding pattern.', 'c1', T1, 'core', check=51),
        Q('m3', 'Which company may omit the cash flow statement from its financial statements?', ['A one person company', 'A listed company', 'A public unlisted company', 'A government company'], 0,
          'One person companies, small companies and dormant companies may present financial statements without a cash flow statement. Other companies must include it. In practice: confirm the company category.', 'c2', T2),
        Q('m4', 'Where the operating cycle cannot be identified, it is assumed to be:', ['Twelve months', 'Six months', 'Twenty-four months', 'The financial year'], 0,
          'Schedule III assumes an operating cycle of twelve months where the normal cycle cannot be identified, for classifying assets and liabilities as current or non-current. In practice: long-cycle businesses state their cycle.', 'c3', T3),
        Q('m5', 'The part of a long-term loan repayable within twelve months is shown under:', ['Current liabilities (current maturities of long-term borrowings)', 'Non-current borrowings', 'Shareholders\' funds', 'Contingent liabilities'], 0,
          'Amounts due within twelve months after the reporting date are current liabilities; Schedule III shows current maturities of long-term debt as part of short-term borrowings or current liabilities. In practice: split each loan.', 'c3', T3),
        Q('m6', 'In the Schedule III statement of profit and loss, expenses are classified by:', ['Nature', 'Function', 'Department', 'Product'], 0,
          'Schedule III Division I lists expenses by nature — materials, purchases, inventory changes, employee benefits, finance costs, depreciation and other expenses. In practice: map ledgers accordingly.', 'c4', T4),
        Q('m7', 'Dividend declared must be deposited in a separate bank account within:', ['Five days of declaration', 'Thirty days', 'Seven days', 'Fifteen days'], 0,
          'Section 123 requires the dividend amount, including interim dividend, to be placed in a separate account with a scheduled bank no later than five days after it is declared. Payment follows within thirty days. In practice: plan the cash.', 'c5', T5),
        Q('m8', 'Paid-up capital ₹40 lakh, free reserves ₹20 lakh. The maximum that can be drawn from accumulated profits for dividend in a loss year:', ['₹6 lakh', '₹4 lakh', '₹2 lakh', '₹12 lakh'], 0,
          'The cap is one-tenth of paid-up capital plus free reserves: 10% × ₹60 lakh = ₹6 lakh, and any current year loss must be set off from it first. In practice: also apply the rate cap.', 'c5', T5, 'moderate', check=6),
        Q('m9', 'Unclaimed dividend lying in the Unpaid Dividend Account for seven years is transferred to:', ['The Investor Education and Protection Fund', 'General reserve', 'Profit and loss', 'The shareholders\' bank'], 0,
          'Amounts unpaid or unclaimed for seven years from transfer to the Unpaid Dividend Account are transferred, with interest, to the Investor Education and Protection Fund. In practice: notify shareholders first.', 'c5', T5),
        Q('m10', 'Transfer of a part of profits to reserves before declaring a dividend is:', ['Optional under the Companies Act, 2013', 'Mandatory at 10%', 'Mandatory at 5%', 'Prohibited'], 0,
          'The 2013 Act lets a company transfer such percentage of profits to reserves as it thinks appropriate; it is not compulsory. In practice: Board decides based on needs.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Rate cap', 1.5, 'computation', 'average', nums=[rate]),
           S('s2', 'Amount cap', 1.5, 'computation', '1/10|one-tenth', nums=[cap]),
           S('s3', 'Loss set-off and conclusion', 2, 'computation', 'loss', nums=[net, div])],
          ['Apply all three conditions.'], ['Ignoring the current year loss.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Loan split', 2, 'concept', 'current maturities|12 months'),
           S('s2', 'Assets classification', 2, 'concept', 'operating cycle'),
           S('s3', 'Long operating cycle', 1, 'concept', 'longer')],
          ['Give a reason for each.'], ['Treating 3-year whisky stock as non-current.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What do financial statements include under section 2(40)?', 'A balance sheet, statement of profit and loss, cash flow statement, statement of changes in equity where applicable, and explanatory notes.',
          [P('p1', 'Balance sheet and profit and loss', 5, 'balance sheet', 'profit'), P('p2', 'Cash flow and notes', 5, 'cash flow|notes')], 'c2'),
        V('v2', 'When is an asset classified as current?', 'When it is expected to be realised or consumed in the normal operating cycle, held mainly for trading, expected to be realised within twelve months, or is unrestricted cash.',
          [P('p1', 'Operating cycle', 5, 'operating cycle'), P('p2', 'Twelve months or trading', 5, 'twelve|12|trading')], 'c3'),
        V('v3', 'From what profits may dividend be declared?', 'From the current year\'s profits after depreciation, from undistributed profits of earlier years after depreciation, or both, and from government money provided under a guarantee.',
          [P('p1', 'Profits after depreciation', 6, 'depreciation'), P('p2', 'Current or past', 4, 'current|earlier|previous')], 'c5'),
        V('v4', 'State the limits on dividend out of accumulated profits.', 'The rate cannot exceed the three-year average, the amount drawn cannot exceed one-tenth of paid-up capital plus free reserves, and current year losses are set off first.',
          [P('p1', 'Average rate', 4, 'average'), P('p2', 'One-tenth and losses first', 6, 'one-tenth|1/10|10%')], 'c5'),
        V('v5', 'Where are books of account kept?', 'At the registered office, or at another place in India decided by the Board with notice to the Registrar, possibly in electronic form.',
          [P('p1', 'Registered office', 6, 'registered office'), P('p2', 'Other place or electronic', 4, 'board|electronic')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Navratna Paints Ltd.', 'difficulty': 'moderate',
              'case': 'Navratna Paints Ltd. has a 5-year term loan of ₹60 lakh repayable in equal annual instalments starting next year, trade receivables of ₹45 lakh (all within 90 days) and a security deposit of ₹5 lakh paid for a factory lease running 10 years. It earned profit of ₹30 lakh after depreciation and proposes an equity dividend.',
              'mcqs': [
                  M('k1a', 'Amount of the term loan shown as current:', ['₹12 lakh', '₹60 lakh', '₹48 lakh', 'Nil'], 0,
                    'One instalment of ₹60 lakh ÷ 5 = ₹12 lakh falls due within twelve months and is current; ₹48 lakh is non-current borrowing. In practice: show current maturities separately.', 'core', check=12, topic=T3),
                  M('k1b', 'The ₹5 lakh lease security deposit is:', ['A non-current asset', 'A current asset', 'Inventory', 'A liability'], 0,
                    'It will not be realised within twelve months or the operating cycle, so it is shown under non-current assets (long-term loans and advances or other non-current assets). In practice: classify by expected realisation.', 'core', topic=T3),
                  M('k1c', 'The dividend may be paid out of the year\'s profit of ₹30 lakh because:', ['It is profit after providing depreciation', 'It is before depreciation', 'Reserves must be transferred first', 'It needs government approval'], 0,
                    'Section 123 allows dividend from the year\'s profits arrived at after providing depreciation; transfer to reserves is optional. In practice: the Board recommends and members approve the final dividend.', 'moderate', topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch11', 1, 'Preparation of Financial Statements',
                ['Identify kinds of companies and the rules for books of account.',
                 'State the components and requisites of financial statements.',
                 'Prepare the balance sheet and profit and loss as per Schedule III.',
                 'Apply the rules on distributable profits and dividends.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['int-p1-ch10-u03'],
                 'exam_tip': 'In Schedule III questions, prepare notes first (share capital, reserves, borrowings), then the face of the statements.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Books at registered office, accrual and double entry, kept 8 years.', 'FS = BS + P&L + CFS (+ SOCE) + notes; OPC, small and dormant may skip CFS.',
                             'Schedule III vertical format; current/non-current by operating cycle (default 12 months).', 'P&L expenses by nature; EPS on face.',
                             'Dividend from profits after depreciation; reserves transfer optional.', 'From reserves: average rate, 1/10 cap, losses first; deposit in 5 days; IEPF after 7 years.'],
                 'remember': ['Interim dividend may be declared by the Board.'],
                 'traps': ['Current maturities of long-term loans are current liabilities.']},
                [('Books kept', '8 years'), ('Operating cycle default', '12 months'), ('Dividend deposit', '5 days'), ('From reserves', '≤ 1/10 of capital + free reserves')],
                viva, cases)
