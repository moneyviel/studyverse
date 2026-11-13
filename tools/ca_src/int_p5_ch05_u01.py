"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 5 Audit of Items of Financial Statements.
Scope follows the ICAI study material; explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch05-u01'
T1 = 'Assertions for income statement and balance sheet captions'
T2 = 'Equity: share capital and reserves'
T3 = 'Borrowings, trade payables and other liabilities'
T4 = 'Trade receivables, cash and bank, loans and advances'
T5 = 'Inventories'
T6 = 'Property, plant and equipment and intangible assets'
T7 = 'Provisions and contingent liabilities'
T8 = 'Revenue and other income'
T9 = 'Purchases, employee benefits, depreciation and other expenses'


def build():
    # i1 — recomputing depreciation as a substantive test
    ck = Checks()
    full = ck.add('(4800000-300000)*0.10', 'Depreciation on opening asset (straight line, 10 years)')
    add = ck.add('round(1200000*0.10*5/12)', 'Depreciation on addition used 5 months')
    expd = ck.add('450000+50000', 'Expected depreciation')
    gap = ck.add('620000-500000', 'Excess charged')
    i1 = {'id': 'i1', 'title': 'Recomputing depreciation', 'difficulty': 'core', 'minutes': 7,
          'q': 'At Sutlej Polymers, plant costing ₹48,00,000 (residual value ₹3,00,000, useful life 10 years, straight line) was held all year. A new machine of ₹12,00,000 (no residual value, 10-year life) was put to use on 1 November. The books show depreciation of ₹6,20,000 for the year ended 31 March. Recompute and comment.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Existing plant', '(48,00,000 – 3,00,000) × 10%', inr(full)],
              ['New machine', '12,00,000 × 10% × 5/12', inr(add)],
              ['Expected depreciation', '', inr(expd)],
              ['Recorded', '', inr(620000)],
              ['Excess charged', '', inr(gap)]], title='Recalculation'),
              p('The excess suggests depreciation was charged on the new machine for the full year or residual value was ignored. The auditor should obtain the fixed asset register, check put-to-use dates (commissioning reports), useful lives against Schedule II and policy, and propose a correction if the difference is material.')],
          'checks': list(ck)}

    # i2 — sales cut-off test
    i2 = {'id': 'i2', 'title': 'Testing sales cut-off', 'difficulty': 'core', 'minutes': 6,
          'q': 'At Kosi Electricals (year end 31 March), CA Meera reviews invoices dated 28 March to 4 April. She finds: (a) an invoice dated 30 March for goods dispatched on 2 April; (b) goods dispatched on 31 March, invoiced on 1 April; (c) a credit note dated 3 April for goods returned on 29 March. What adjustments does each suggest?',
          'solution': [table(['Item', 'Issue', 'Adjustment'], [
              ['(a)', 'Goods left on 2 April — risks and rewards passed in the next year', 'Reverse from current-year sales; include goods in closing inventory'],
              ['(b)', 'Dispatched on 31 March — sale belongs to the current year', 'Record the sale in the current year; remove from closing inventory'],
              ['(c)', 'Return happened before year-end', 'Record the sales return and inventory in the current year']], title='Cut-off findings'),
              p('She tests both directions around the year-end using dispatch notes, gate registers and delivery acknowledgements, because invoice dates alone can be manipulated to shift revenue.')]}

    caps = table(['Caption', 'Key assertions', 'Main procedures'], [
        ['Share capital', 'Existence, accuracy, presentation', 'Memorandum and articles (authorised capital), board and shareholder resolutions, prospectus or offer document, bank statements for money received, allotment returns filed with the Registrar, share register'],
        ['Reserves and surplus', 'Accuracy, classification', 'Movements traced to resolutions; securities premium used only for permitted purposes; statutory reserves as required'],
        ['Borrowings', 'Completeness, obligations, disclosure', 'Loan agreements and sanction letters, lender confirmations, charges registered with the Registrar, compliance with borrowing limits (s. 180), interest recomputation, current maturities'],
        ['Trade receivables', 'Existence, valuation', 'Confirmations, ageing analysis, after-date receipts, provision for doubtful debts, cut-off'],
        ['Cash and bank', 'Existence, completeness', 'Surprise cash count, bank confirmations, review of bank reconciliation and old reconciling items, fixed deposit receipts'],
        ['Inventories', 'Existence, valuation, rights', 'Attend counts, cost and NRV tests (AS 2), slow-moving items, consignment stock excluded, third-party stock confirmed'],
        ['PPE', 'Existence, rights, valuation', 'Physical verification, title deeds, capitalisation of additions, depreciation, impairment indicators, disposals'],
        ['Intangibles', 'Valuation, rights', 'Recognition criteria (AS 26), amortisation, impairment, agreements for licences'],
        ['Trade payables', 'Completeness, cut-off', 'Supplier statements reconciliation, search for unrecorded liabilities (after-date payments), GRN cut-off'],
        ['Loans and advances', 'Existence, valuation, compliance', 'Agreements, confirmations, recoverability, related-party approvals, s. 185/186 compliance'],
        ['Provisions and contingent liabilities', 'Completeness, valuation, disclosure', 'AS 29 criteria, legal letters, minutes, warranty history, management estimates']], title='Audit of balance sheet captions')
    pl = table(['Caption', 'Key assertions', 'Main procedures'], [
        ['Revenue', 'Occurrence, cut-off, accuracy', 'Order–dispatch–invoice trail, price lists and discounts, cut-off, analytical review of margins, credit notes after year-end'],
        ['Other income', 'Completeness, accuracy', 'Recompute interest and dividend, TDS certificates, rental agreements'],
        ['Purchases', 'Occurrence, accuracy, cut-off', 'Purchase orders, goods received notes, invoices, approvals, returns, related-party prices'],
        ['Employee benefits', 'Occurrence, accuracy', 'Payroll vs attendance and HR records, statutory dues deposits, actuarial valuation for gratuity and leave (AS 15), ghost-employee checks'],
        ['Depreciation', 'Accuracy', 'Recompute; check useful lives, residual values and put-to-use dates'],
        ['Other expenses', 'Occurrence, classification', 'Vouching for approval and business purpose, prepaid and outstanding adjustments, analytical review']], title='Audit of profit and loss captions')

    concepts = [
        C('c1', T1, [
            'Each caption carries assertions. For income and expenses: occurrence, completeness, cut-off, accuracy (measurement), and presentation and disclosure. For assets, liabilities and equity: existence, completeness, cut-off, valuation and allocation, rights and obligations, and presentation and disclosure.',
            'The auditor plans procedures for the assertions most at risk for each caption, and checks disclosures required by the applicable framework and Schedule III.'],
          'Every line in the accounts makes promises; the audit programme lists how to check each promise.',
          'A building shown at ₹50 lakh asserts that it exists, is owned, is complete and is correctly valued.'),
        C('c2', T2, [
            'Share capital: verify authorised capital in the memorandum, approvals for each issue, receipt of money through the bank, allotment and return filings, the register of members, and disclosure of the reconciliation of shares outstanding.',
            'Reserves: trace each movement to approvals and check that restricted reserves (e.g. securities premium) are used only as law permits.'],
          'Equity changes need paperwork from the board and shareholders, and cash in the bank.',
          'A rights issue is checked from the letter of offer to the bank credit and the allotment return.',
          blocks=[caps]),
        C('c3', T3, [
            'Borrowings: examine agreements, confirm balances with lenders, check that charges are registered, verify limits and approvals, recompute interest, and split current maturities.',
            'Trade payables and other liabilities: completeness is the main risk, so search for unrecorded liabilities through payments made after year-end, supplier statements and goods received near the year-end.'],
          'For liabilities the danger is what is missing, so the auditor looks for what is not recorded.',
          'An April payment for March deliveries points to a liability missing at year-end.'),
        C('c4', T4, [
            'Trade receivables: confirm balances, review ageing and after-date collections, assess the provision for doubtful debts, and test cut-off.',
            'Cash and bank: count cash by surprise in the presence of the cashier, obtain bank confirmations directly, scrutinise the bank reconciliation for old or unusual items, and verify fixed deposit receipts.',
            'Loans and advances: agreements, confirmations, recoverability, and compliance with the Companies Act for loans to directors and related parties.'],
          'For assets the danger is overstatement, so the auditor demands proof that they exist and can be realised.',
          'A cheque deposited on 31 March but not credited until 10 April deserves a closer look.'),
        C('c5', T5, [
            'Attend physical counts (SA 501), test valuation at the lower of cost and net realisable value (AS 2), exclude abnormal wastage and general overheads from cost, check slow-moving and obsolete items, include goods with third parties and exclude goods held on consignment for others.'],
          'Inventory is counted, owned and priced — the auditor checks all three.',
          'Goods held as consignee belong to the consignor, not to the client.'),
        C('c6', T6, [
            'PPE: verify additions against invoices and capitalisation policy, title deeds for land and buildings, physical existence, depreciation per Schedule II and policy, disposals and impairment indicators.',
            'Intangibles: check recognition criteria (identifiability, control, future benefits, reliable cost) under AS 26; research costs are expensed; amortisation and impairment are reviewed.'],
          'An asset on paper must also stand on the ground and belong to the company.',
          'Repairs that do not extend useful life should not be capitalised.'),
        C('c7', T7, [
            'Provisions require a present obligation, probable outflow and reliable estimate (AS 29); contingent liabilities are disclosed, not recognised.',
            'Procedures: inquire of management, read minutes, review legal correspondence and lawyer letters, examine warranty claim history, and evaluate the reasonableness of estimates.'],
          'Promises and pending disputes must surface in the accounts, either as a provision or as a note.',
          'A pending tax demand that is possible but not probable is disclosed as a contingent liability.'),
        C('c8', T8, [
            'Revenue: test occurrence by tracing from orders to dispatch and invoices, check prices and discounts, perform cut-off tests both sides of the year-end, review post year-end credit notes, and use analytical procedures on margins and trends.',
            'Other income: recompute interest and dividends, match TDS certificates, and check rental agreements.'],
          'Revenue is where pressure to meet targets shows up, so cut-off and occurrence get extra attention.',
          'A spike in sales in the last week followed by April returns is a warning sign.',
          blocks=[pl]),
        C('c9', T9, [
            'Purchases: verify orders, receipts and invoices, approvals and returns; check related-party pricing.',
            'Employee benefits: compare payroll with attendance and HR records, test statutory deposits, check actuarial valuations for gratuity and leave, and watch for fictitious employees.',
            'Depreciation: recompute and check useful lives, residual values and put-to-use dates.',
            'Other expenses (power, rent, repairs, insurance, legal fees): vouch for authorisation and business purpose and check accruals and prepayments.'],
          'Expenses are tested for whether they really happened, for the business, in this year.',
          'Repairs vouched to a director\'s residence are not business expenses.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Year-end cut-off programme', 'role': 'Audit assistant',
         'situation': 'Your senior asks you to test sales and purchase cut-off.',
         'steps': ['List the last five dispatch notes before and first five after year-end.', 'Match each to invoices and the period recorded.', 'Do the same for goods received notes and purchase invoices.', 'Report errors with proposed adjustments.'],
         'takeaway': 'Test both directions around the year-end.'},
        {'id': 'j2', 'title': 'Search for unrecorded liabilities', 'role': 'Audit senior',
         'situation': 'Payables look low compared with last year.',
         'steps': ['Review payments in the first weeks after year-end.', 'Obtain supplier statements and reconcile.', 'Check goods received but not invoiced.', 'Read legal and board correspondence for claims.'],
         'takeaway': 'Completeness evidence comes from outside the payables ledger.'},
    ]

    mcqs = [
        Q('m1', 'The main risk the auditor addresses for trade payables is:', ['Completeness (understatement)', 'Existence (overstatement)', 'Rights', 'Classification'], 0,
          'Entities under pressure may leave liabilities out to improve results, so the key assertion for payables is completeness. Assets, by contrast, are mainly tested for existence and valuation. In practice: search for unrecorded liabilities after year-end.', 'c3', T3),
        Q('m2', 'Checking that sales invoiced on 31 March were dispatched on or before that date tests:', ['Cut-off', 'Valuation', 'Rights and obligations', 'Existence of inventory only'], 0,
          'Cut-off ensures transactions are recorded in the correct period; dispatch documents show when the sale took place. Valuation and rights relate to balances. In practice: use gate registers and delivery acknowledgements.', 'c8', T8),
        Q('m3', 'Goods held by the client as consignee should be:', ['Excluded from the client\'s inventory', 'Included at cost', 'Included at selling price', 'Shown as a contingent liability'], 0,
          'The consignor still owns consigned goods, so they fail the rights assertion for the consignee and must be excluded. Goods held by third parties on the client\'s behalf are included. In practice: read consignment agreements.', 'c5', T5),
        Q('m4', 'Title deeds of land mainly provide evidence of:', ['Rights (ownership)', 'Existence', 'Valuation', 'Cut-off'], 0,
          'Title deeds show the entity\'s legal right to the property; physical inspection shows existence, and cost records support valuation. In practice: check that deeds are in the company\'s name and note any charges.', 'c6', T6),
        Q('m5', 'A surprise cash count is performed mainly to verify:', ['Existence of cash', 'Completeness of sales', 'Valuation of inventory', 'Accuracy of payroll'], 0,
          'Counting cash unannounced, in the cashier\'s presence, shows whether recorded cash actually exists and reduces the chance of short-term borrowing to cover shortages. In practice: count all cash points at the same time.', 'c4', T4),
        Q('m6', 'Payments made after the year-end are reviewed mainly to detect:', ['Unrecorded liabilities', 'Fictitious assets', 'Overstated revenue', 'Excess depreciation'], 0,
          'A payment in April may settle an obligation that existed at 31 March but was not recorded, so after-date payments are a completeness test for liabilities. In practice: read the narration and supporting invoices.', 'c3', T3),
        Q('m7', 'A pending lawsuit where an outflow is possible but not probable should be:', ['Disclosed as a contingent liability', 'Provided for in full', 'Ignored', 'Shown as a reduction of revenue'], 0,
          'AS 29 requires a provision only when an outflow is probable and can be estimated reliably; a possible outflow is disclosed as a contingent liability unless remote. In practice: obtain the lawyer\'s view on likelihood.', 'c7', T7),
        Q('m8', 'Depreciation recorded ₹4,20,000; expected ₹3,60,000. The difference is:', ['₹60,000 over-charged', '₹60,000 under-charged', '₹7,80,000', 'Nil'], 0,
          'Recorded exceeds the auditor\'s expectation by 4,20,000 – 3,60,000 = ₹60,000, so depreciation appears over-charged. The cause must be found before proposing an adjustment. In practice: check put-to-use dates and residual values.', 'c9', T9, 'core'),
        Q('m9', 'Comparing payroll with attendance records helps detect:', ['Fictitious (ghost) employees', 'Unrecorded sales', 'Inventory obsolescence', 'Unregistered charges'], 0,
          'Wages paid to people who do not appear in attendance or HR records may indicate ghost employees and misappropriation. It is an occurrence test for employee benefit expense. In practice: also check bank accounts receiving salaries.', 'c9', T9),
        Q('m10', 'For a new share issue, money received should be traced to:', ['Bank statements of the company', 'The share certificates only', 'The directors\' report', 'Cash book of shareholders'], 0,
          'The bank statement is independent evidence that the issue money was actually received in the company\'s account. Share certificates and reports are internal or derived documents. In practice: match with the allotment list.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Existing plant', 1, 'computation', 'residual|existing', nums=[full]),
           S('s2', 'Addition time-apportioned', 1, 'computation', '5/12|five months', nums=[add]),
           S('s3', 'Excess', 1, 'computation', 'excess', nums=[gap]),
           S('s4', 'Follow-up', 1, 'concept', 'register|schedule ii|put-to-use|put to use')],
          ['Time-apportion additions.'], ['Charging a full year on additions.'], ['Table + comment.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', '(a) reverse', 1, 'concept', 'reverse|next year'),
           S('s2', '(b) record', 1, 'concept', 'current year|record'),
           S('s3', '(c) return', 1, 'concept', 'return')],
          ['Use dispatch dates, not invoice dates.'], ['Treating invoice date as decisive.'], ['Table.'], pad='table'),
        W('q3', 5, 'How would you verify trade receivables of a company? Give at least five procedures.',
          [ul(['Obtain the receivables ledger and agree the total with the trial balance.', 'Send confirmations (positive for large balances) and follow up non-replies with alternative procedures.', 'Review the ageing analysis and test it for accuracy.', 'Check collections after the year-end.', 'Assess the adequacy of the provision for doubtful debts, including disputed and old balances.', 'Test cut-off of sales and credit notes around the year-end.', 'Check classification (secured, unsecured, doubtful) and related-party disclosures as per Schedule III.'])],
          [S('s1', 'Agree to trial balance', 0.5, 'concept', 'trial balance|ledger'),
           S('s2', 'Confirmations', 1, 'concept', 'confirm'),
           S('s3', 'Ageing', 1, 'concept', 'ageing|aging'),
           S('s4', 'After-date collections', 1, 'concept', 'collection|after'),
           S('s5', 'Provision and disclosure', 1.5, 'concept', 'provision|doubtful', 'schedule iii|disclos|classif')],
          ['List procedures by assertion.'], ['Forgetting the provision for doubtful debts.'], ['Bulleted list.']),
    ]

    viva = [
        V('v1', 'Which assertion is most important for liabilities and why?',
          'Completeness, because entities may understate liabilities to show a better position, so the auditor searches for unrecorded obligations.',
          [P('p1', 'Completeness', 6, 'completeness'), P('p2', 'Understatement risk', 4, 'understat|unrecorded|omit')], 'c3'),
        V('v2', 'How do you verify the existence of cash in hand?',
          'By a surprise physical count of cash in the presence of the cashier, covering all cash points at the same time and agreeing it with the cash book.',
          [P('p1', 'Surprise count', 6, 'surprise|count'), P('p2', 'Agree with cash book', 4, 'cash book|agree')], 'c4'),
        V('v3', 'How is inventory valued under AS 2?',
          'At the lower of cost and net realisable value, excluding abnormal wastage and general administrative overheads from cost.',
          [P('p1', 'Lower of cost and NRV', 7, 'lower|net realisable|nrv'), P('p2', 'Exclusions', 3, 'abnormal|administrative')], 'c5'),
        V('v4', 'What evidence supports ownership of land?',
          'Title deeds in the company\'s name, supported by registration records and, where relevant, records of charges created on the property.',
          [P('p1', 'Title deeds', 6, 'title deed|deed'), P('p2', 'Company name / registration', 4, 'name|registr')], 'c6'),
        V('v5', 'How does a sales cut-off test work?',
          'By examining dispatch documents and invoices for a few days before and after the year-end to see that sales are recorded in the period in which goods were dispatched.',
          [P('p1', 'Before and after year-end', 5, 'before|after|year-end|year end'), P('p2', 'Dispatch documents', 5, 'dispatch|delivery')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Damodar Engineering audit', 'difficulty': 'moderate',
              'case': 'At Damodar Engineering, CA Ishaan finds: a loan of ₹2 crore from a bank whose charge is not registered with the Registrar; a ₹40 lakh advance to a director\'s firm without board approval; a cheque of ₹5 lakh shown as deposited on 31 March but credited on 18 April; and a tax demand of ₹30 lakh that the company\'s lawyer thinks it will probably lose.',
              'mcqs': [
                  M('k1a', 'For the bank loan, Ishaan should:', ['Obtain the lender\'s confirmation and check the registration of charge and its implications', 'Ignore the charge as it is the bank\'s concern', 'Treat the loan as equity', 'Remove the loan'], 0,
                    'He confirms the balance and terms directly with the lender and checks whether the charge is registered, since non-registration has legal consequences and affects disclosure of secured borrowings. In practice: review the register of charges.', 'moderate', topic=T3),
                  M('k1b', 'The advance to the director\'s firm calls for:', ['Checking compliance with Companies Act provisions on loans and related-party approvals', 'No action, as it is an advance', 'Treating it as revenue', 'Writing it off immediately'], 0,
                    'Loans and advances to entities in which directors are interested are restricted by the Companies Act and need approvals; they are also related-party transactions needing disclosure. In practice: obtain board and shareholder resolutions.', 'moderate', topic=T4),
                  M('k1c', 'The cheque credited on 18 April suggests:', ['Possible window-dressing or a cheque issued after year-end; investigate', 'Normal timing only', 'An unrecorded liability', 'A sales cut-off error'], 0,
                    'A long delay between the recorded deposit and bank credit can indicate that the cheque was not actually in hand at year-end, inflating cash and reducing receivables. It needs investigation with deposit slips and the payer. In practice: examine the bank reconciliation carefully.', 'hard', topic=T4),
                  M('k1d', 'The tax demand of ₹30 lakh should be:', ['Provided for, as the outflow is probable and estimable', 'Only disclosed as a contingent liability', 'Ignored until final order', 'Shown as an asset'], 0,
                    'Because the lawyer considers the loss probable and the amount can be estimated, AS 29 requires a provision. Disclosure alone is for possible outflows. In practice: evaluate the lawyer\'s reasoning.', 'core', topic=T7),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch05', 1, 'Audit of Items of Financial Statements',
                ['Apply assertions to income statement and balance sheet captions.',
                 'Design procedures for equity, borrowings, payables and other liabilities.',
                 'Design procedures for receivables, cash and bank, loans and advances, inventories, PPE and intangibles.',
                 'Audit provisions and contingent liabilities.',
                 'Audit revenue, other income, purchases, employee benefits, depreciation and other expenses.'],
                {'difficulty': 'core', 'minutes': {'learn': 70, 'practice': 40}, 'prereq': ['int-p5-ch04-u01'],
                 'exam_tip': 'Answer "how would you verify X" by listing procedures under each relevant assertion and ending with Schedule III disclosure checks.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Assets: existence, rights, valuation; liabilities: completeness.', 'Revenue: occurrence and cut-off.', 'Receivables: confirmations, ageing, after-date receipts, provision.',
                             'Cash: surprise count, bank confirmation, reconciliation.', 'Inventory: count, cost vs NRV, ownership.', 'PPE: title deeds, physical verification, depreciation.',
                             'Provisions vs contingent liabilities under AS 29.', 'Expenses: vouching, payroll tests, depreciation recomputation.'],
                 'remember': ['Search for unrecorded liabilities after year-end.', 'Consigned-in goods are not inventory.'],
                 'traps': ['Invoice date alone does not prove cut-off.', 'Inspection proves existence, not ownership.']},
                [('Payables', 'Completeness'), ('Receivables', 'Existence + valuation'), ('Revenue', 'Occurrence + cut-off'), ('Land', 'Title deeds')],
                viva, cases,
                topics=['Assertions', 'Balance Sheet Captions', 'Statement of Profit and Loss Captions'])
