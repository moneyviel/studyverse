"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 6 Accounting as a Measurement Discipline – Valuation Principles, Accounting Estimates.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u06'


def build():
    # ---------------- Illustration 1: four bases for a machine and a loan ----------------
    c1 = Checks()
    hc = c1.add('900000+60000', 'Historical cost of machine = price + installation')
    pv_rows = []
    pvs = []
    for t in range(1, 7):
        v = c1.add(f'round(200000/1.12**{t})', f'Present value of ₹2,00,000 receivable at end of year {t} @ 12%')
        pvs.append(v)
        pv_rows.append([f'End of year {t} (31 Mar {2026 + t})', '2,00,000', f'1/(1.12)^{t}', inr(v)])
    pv_m = c1.add('+'.join(str(x) for x in pvs), 'Present value of the machine (sum of six discounted inflows)')
    c1.add('round(200000*(1-1.12**-6)/0.12)', 'Same result by the annuity formula')
    loan_cc = c1.add('600000*102/100', 'Loan at current cost: settle today with 2% prepayment penalty')
    pv_int = c1.add('round(60000*(1-1.12**-5)/0.12)', 'PV of interest ₹60,000 a year for 5 years @ 12%')
    pv_prin = c1.add('round(600000/1.12**5)', 'PV of ₹6,00,000 repayable after 5 years @ 12%')
    pv_loan = c1.add('216287+340456', 'Present value of the loan')
    pv_tbl = table(['Cash inflow at', 'Amount (₹)', 'Discount factor', 'Present value (₹)'],
                   pv_rows + [['Total', '12,00,000', '', inr(pv_m)]], num=[1, 3], total=True,
                   title='Present value of the machine\'s expected net cash inflows (12%)')
    four_tbl = table(['Item', 'Historical cost (₹)', 'Current cost (₹)', 'Realisable value (₹)', 'Present value (₹)'], [
        ['Asset: Machine', inr(hc), '18,00,000', '11,00,000', inr(pv_m)],
        ['Liability: 10% Bank loan', '6,00,000', inr(loan_cc), '6,00,000', inr(pv_loan)],
    ], title='Four measurements on 1 April 2026 — Patel Plastics')

    # ---------------- Illustration 2: money as an unstable scale ----------------
    c2 = Checks()
    g_val = c2.add('round((1296000-1200000)/1200000*100, 2)', 'Growth in sales value %')
    g_qty = c2.add('round((7200-8000)/8000*100, 2)', 'Change in quantity sold %')
    p1_ = c2.add('1200000/8000', 'Price per unit, Year 1')
    p2_ = c2.add('1296000/7200', 'Price per unit, Year 2')
    usd1 = c2.add('10000*83', 'USD 10,000 loan at ₹83')
    usd2 = c2.add('10000*86', 'Same loan at ₹86')
    usd_d = c2.add('860000-830000', 'Increase in rupee amount of the same loan')
    scale_tbl = table(['', 'Year 1', 'Year 2', 'Change'], [
        ['Units sold', '8,000', '7,200', f'{g_qty}%'],
        ['Sales value (₹)', '12,00,000', '12,96,000', f'+{g_val}%'],
        ['Price per unit (₹)', inr(p1_), inr(p2_), '+20%'],
    ], title='Stable Co. — rupees say "growth", units say "decline"')

    # ---------------- Illustration 3: accounting estimates ----------------
    c3 = Checks()
    dep_old = c3.add('1200000/10', 'Annual depreciation on original estimate of 10 years')
    wdv4 = c3.add('1200000-120000*4', 'Carrying amount after 4 years')
    dep_new = c3.add('720000/3', 'Revised annual depreciation over remaining 3 years')
    pdd = c3.add('800000*5/100', 'Provision for doubtful debts @5% on ₹8,00,000')
    pdd_extra = c3.add('52000-40000', 'Additional amount charged next year when actual bad debts are ₹52,000')
    est_tbl = table(['Year', 'Depreciation (₹)', 'Basis'], [
        ['2022-23', inr(dep_old), '₹12,00,000 ÷ 10 years'],
        ['2023-24', inr(dep_old), 'same'],
        ['2024-25', inr(dep_old), 'same'],
        ['2025-26', inr(dep_old), 'same'],
        ['2026-27', inr(dep_new), 'Carrying amount ₹7,20,000 ÷ revised remaining life 3 years'],
        ['2027-28', inr(dep_new), 'same'],
        ['2028-29', inr(dep_new), 'same'],
        ['Total', '12,00,000', ''],
    ], num=[1], total=True, title='Machine of Arya Pharma — change in estimated useful life')

    bases_tbl = table(['Basis', 'Asset is carried at', 'Liability is carried at', 'Where commonly used'], [
        ['Historical cost', 'Cash or cash equivalent paid (or fair value of consideration) when acquired, including costs to make it usable', 'Proceeds received in exchange for the obligation (or, e.g. for income tax, the amount expected to be paid)', 'Long-term assets: machinery, furniture, licences'],
        ['Current cost', 'Cash needed today to buy an identical or equivalent asset', 'Undiscounted cash needed to settle the obligation now', 'Inflation-adjusted analysis, replacement decisions'],
        ['Realisable (settlement) value', 'Cash that could be obtained now by selling it in an orderly disposal', 'Undiscounted cash expected to be paid to settle it in the normal course of business', 'Inventories: lower of cost and net realisable value'],
        ['Present value', 'Discounted value of future net cash inflows it will generate in the normal course', 'Discounted value of future net cash outflows needed to settle it in the normal course', 'Investments and loans'],
    ], title='The four valuation principles (measurement bases)')

    concepts = [
        {'id': 'c1', 'title': 'Meaning of measurement and its three elements',
         'body': ['Measurement is a vital part of accounting; transactions and events are measured mainly in money. Prof. R. J. Chambers described measurement as assigning numbers to objects and events by rules that specify the property being measured, the scale used and the dimension of the unit. Kohler described it as assigning ordinal or cardinal numbers to the results of an inquiry or observation following logical or mathematical rules.',
                  'Ordinal numbers show position in a sequence (first, second, third); cardinal numbers show how many (one, two, three). Accountants use cardinal numbers — rupee amounts.',
                  'From Chambers\' definition, every measurement discipline has three elements: (1) identifying the objects and events to be measured, (2) selecting the standard or scale, and (3) evaluating the dimension (stability) of that standard or scale. These elements are used to judge how far accounting is a measurement discipline.'],
         'analogy': 'Measuring a room: decide what to measure (length of a wall), choose the scale (metres), and make sure the tape does not stretch (stable dimension).',
         'work': 'Before valuing anything — an inventory, a business, a claim — a CA asks the same three questions: what exactly is being valued, in what unit, and can that unit be trusted over time?'},
        {'id': 'c2', 'title': 'Objects or events to be measured',
         'body': ['Accounting identifies, measures and communicates economic information for decisions, so what it measures is information. Decision-makers need past, present and future information; external users are usually given past information.',
                  'There is no fixed set of objects and events: for cash management the relevant items are cash receipts and payments (past and projected); for a lender, the borrower\'s debt-servicing ability — past results, present position and projections.',
                  'Things that have already happened, or exist now, can be measured fairly accurately; future ones can only be predicted, not measured. Yet prediction is an essential part of accounting information because decisions concern the future.'],
         'analogy': 'A doctor uses your past reports (measured) and current tests (measured) to forecast your health next year (predicted).',
         'work': 'Bank appraisal notes combine audited past figures with projected cash flows. A CA preparing projections must make clear which figures are measured facts and which are predictions.'},
        {'id': 'c3', 'title': 'Money as the scale — and its weaknesses',
         'body': ['In accounting, money is the scale of measurement (money measurement concept); quantitative information is given only as a supplement.',
                  'Not universal: money has no single worldwide denomination — rupee in India, dollar in the USA, pound sterling in the UK — and exchange rates keep changing. A USD 10,000 loan recorded at ₹83 becomes ₹86 per dollar later; the same obligation now measures ₹8,60,000 instead of ₹8,30,000.',
                  'Not stable in dimension: an ideal scale does not change over time (a kilogram or a metre stays the same), but the purchasing power of money keeps changing with prices. Rupee figures of different years are therefore not strictly comparable — sales value may rise while the quantity sold falls.'],
         'blocks': [scale_tbl],
         'analogy': 'Money is like a rubber ruler: it measures, but it stretches with inflation and is a different ruler in every country.',
         'work': 'When presenting a five-year trend to a client, a CA often shows volumes alongside rupee figures, so that price rises are not mistaken for real growth.'},
        {'id': 'c4', 'title': 'Is accounting a measurement discipline?',
         'body': ['Accounting measures performance (profit or loss) and position (balance sheet), and a set of assumptions governs that measurement — going concern, consistency and accrual are taken for granted as fundamental assumptions, and various policies are adopted.',
                  'But accounting is not an exact measurement discipline: its scale (money) is neither universal nor stable in dimension, and much of accounting — recording, classifying, summarising and communicating — lies outside measurement altogether. So we cannot simply call accounting a measurement discipline, though measurement is an important part of it. For our study we take it as given that transactions are recorded in money, with quantities as supplementary information.'],
         'analogy': 'A journalist measures some things (votes counted, temperatures), but most of the job is reporting and explaining. Accounting is similar.',
         'work': 'Explaining to a client that accounts give "a" true and fair view, not "the" exact value of his business, is part of managing expectations — especially in disputes and valuations.'},
        {'id': 'c5', 'title': 'The four valuation principles',
         'body': ['Historical cost: acquisition price — e.g. machine price plus installation. Liabilities at the proceeds received (a ₹5 lakh bank loan at ₹5 lakh), or for items like income tax, at the amount expected to be paid. Commonly used for long-term assets.',
                  'Current cost: what it would cost to acquire the same or an equivalent asset now; liabilities at the undiscounted amount needed to settle them now (including, say, a prepayment penalty).',
                  'Realisable (settlement) value: what an asset would fetch now in an orderly disposal (a hurried sale may fetch less); liabilities at the undiscounted amount expected to be paid in the normal course. Commonly applied to inventories (lower of cost and net realisable value).',
                  'Present value: the discounted value of future net cash inflows (assets) or outflows (liabilities) in the normal course of business — used for investments and loans. Because of the time value of money, ₹100 receivable a year later is worth less than ₹100 today; discounting uses P = A ÷ (1 + i)^n, and for an equal annual amount, PV = A/i × [1 − 1/(1 + i)^n].',
                  'The traditional system is called historical cost accounting, but in later CA studies you will see that all four bases are used; most transactions are still measured at historical cost.'],
         'blocks': [bases_tbl],
         'analogy': 'Your old car: what you paid (historical cost), what a new one costs today (current cost), what a dealer would pay you (realisable value), and what the rides it will give you are worth in today\'s money (present value).',
         'work': 'Valuation reports for mergers, insurance claims and lender security use different bases for different purposes. A CA must state clearly which basis is used and why.'},
        {'id': 'c6', 'title': 'Measurement and valuation',
         'body': ['Value relates to the benefit to be derived from an object, ability or idea. To an economist, value is utility — the satisfaction a resource gives — often expressed on ordinal scales (more or less satisfying).',
                  'Accountants use a money surrogate and only cardinal scales: value is shown by measurement in money. When a car bought for ₹2,50,000 is recorded at that amount, it is only one kind of value — acquisition (historical) cost. So in accounting, valuation is always measurement in money terms using a chosen basis.'],
         'analogy': 'A painting may be "priceless" to its owner (economic value as satisfaction), but the accounts can only show a number in rupees — what was paid for it.',
         'work': 'Clients often say "this machine is worth much more to us". A CA explains that the accounts carry it on a measurement basis (usually cost), not its subjective worth.'},
        {'id': 'c7', 'title': 'Accounting estimates',
         'body': ['Some items have not yet happened and cannot be measured by a valuation principle, but must still be recorded — such as provision for doubtful debts. For them, reasonable estimates are made using the current situation and past experience, based on the latest information available.',
                  'Estimates are needed for depreciation and amortisation, impairment losses, accruals, provisions, employee benefit obligations, bad debts, useful life and residual value of plant, inventory obsolescence, the period of benefit from a patent, provisions for unforeseen contingencies on long-term contracts, and tax provisions where interpretations may differ.',
                  'An estimate may need revision when the circumstances on which it was based change, or new information, more experience or later developments become available. A change in accounting estimate is the difference between what was estimated earlier and what is re-estimated (or actually achieved) in the current period — e.g. a machine expected to last 10 years becomes obsolete after 3 and is now expected to last only 3 more years. The revised estimate is applied from the period of change; earlier figures are not reworked.'],
         'blocks': [est_tbl],
         'analogy': 'A weather forecast is revised as new data comes in; yesterday\'s forecast is not "wrong", it was the best estimate then.',
         'work': 'Auditors spend much of their time on estimates — they test the assumptions behind doubtful-debt provisions, useful lives and warranty provisions, because a small change in an estimate can swing profit significantly.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'One machine, one loan, four values', 'difficulty': 'hard', 'minutes': 18,
         'q': 'Patel Plastics bought a machine on 1 April 2016 for ₹9,00,000 and paid ₹60,000 for installation. On the same date it took a bank loan of ₹6,00,000 at 10% interest a year, repayable on 31 March 2031. On 1 April 2026: an equivalent new machine would cost ₹18,00,000; the old machine could fetch ₹11,00,000 in an orderly sale; it is expected to generate net cash inflows of ₹2,00,000 a year for 6 more years; the bank would accept immediate repayment of the loan with a 2% prepayment penalty; and the appropriate discount rate is 12%. Show the machine and the loan under each of the four valuation principles on 1 April 2026.',
         'solution': [wn('Historical cost', f'Machine: 9,00,000 + 60,000 = ₹{inr(hc)}. Loan: proceeds received ₹6,00,000.'),
                      wn('Current cost', f'Machine: cost of an equivalent asset now ₹18,00,000. Loan: amount needed to settle today 6,00,000 × 102% = ₹{inr(loan_cc)}.'),
                      wn('Realisable / settlement value', 'Machine: orderly-sale value ₹11,00,000. Loan: amount payable in the normal course ₹6,00,000.'),
                      pv_tbl,
                      wn('Present value of the loan', f'Interest ₹60,000 a year for 5 years: 60,000/0.12 × [1 − 1/(1.12)^5] = ₹{inr(pv_int)}. Principal after 5 years: 6,00,000/(1.12)^5 = ₹{inr(pv_prin)}. Total ₹{inr(pv_loan)}.'),
                      four_tbl,
                      note('The annuity formula 2,00,000/0.12 × [1 − 1/(1.12)^6] gives the same ₹8,22,281 as adding the six discounted amounts.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Why money is an imperfect measuring scale', 'difficulty': 'core', 'minutes': 8,
         'q': '(a) Stable Co. sold 8,000 units for ₹12,00,000 in Year 1 and 7,200 units for ₹12,96,000 in Year 2. Did the business grow? (b) An Indian importer owes a US supplier USD 10,000. It recorded the amount when USD 1 = ₹83; at the year end USD 1 = ₹86. What does this show about money as a scale?',
         'solution': [scale_tbl,
                      wn('(a)', f'Sales value rose by {g_val}% only because the price per unit rose from ₹{inr(p1_)} to ₹{inr(p2_)}. The quantity sold actually fell by {abs(g_qty)}%. Money is not stable in dimension, so rupee figures of different years are not truly comparable.'),
                      wn('(b)', f'The same debt measures ₹{inr(usd1)} at the first rate and ₹{inr(usd2)} at the second — ₹{inr(usd_d)} more with no change in what is owed in dollars. Money is not a universal scale across countries.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Revising accounting estimates', 'difficulty': 'moderate', 'minutes': 10,
         'q': '(a) Arya Pharma bought a machine on 1 April 2022 for ₹12,00,000, expecting a 10-year life with no residual value (straight-line). On 1 April 2026, because of new technology, the remaining useful life is re-estimated at 3 years. Show the depreciation for each year. (b) On 31 March 2026 it estimated doubtful debts at 5% of receivables of ₹8,00,000; in 2026-27 actual bad debts out of those receivables were ₹52,000. How are these handled?',
         'solution': [est_tbl,
                      wn('(a)', f'Original depreciation 12,00,000 ÷ 10 = ₹{inr(dep_old)} a year. After 4 years the carrying amount is ₹{inr(wdv4)}. The revised estimate is applied from 2026-27: {inr(wdv4)} ÷ 3 = ₹{inr(dep_new)} a year. The four earlier years are not reworked.'),
                      wn('(b)', f'Provision made on 31 March 2026: 8,00,000 × 5% = ₹{inr(pdd)}. Actual loss ₹52,000, so the extra ₹{inr(pdd_extra)} is charged in 2026-27, the period in which it becomes known.')],
         'checks': c3},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Which value goes into the report?', 'role': 'Article assistant helping with a valuation for a bank loan',
         'situation': 'A client wants a loan against his plant. He offers the original invoice (₹40 lakh, 8 years old), a supplier quote for a new plant (₹75 lakh) and a dealer\'s offer to buy the used plant (₹28 lakh).',
         'steps': ['Identify the bases: invoice = historical cost; supplier quote = current cost; dealer offer = realisable value.',
                   'Ask what the bank needs: security value if the loan goes bad — realisable value in an orderly sale is the relevant base.',
                   'Note that the client\'s books will still show the plant at historical cost less depreciation (going concern).',
                   'State the basis used and its source clearly in the report.'],
         'takeaway': 'There is no single "value" — each basis answers a different question. Always say which basis you used and why.',
         'think': 'Why would the bank ignore the ₹75 lakh figure?',
         'answer': 'Current cost tells what a new plant would cost to buy; the bank wants to know what it could recover by selling the existing plant, which is its realisable value.'},
        {'id': 'j2', 'title': 'Testing a doubtful-debt estimate', 'role': 'Audit assistant at a distribution company',
         'situation': 'Management has provided 2% of receivables as doubtful, the same as every year. This year two large customers are 9 months overdue and one has filed for insolvency.',
         'steps': ['Collect the ageing of receivables and recent recovery history.',
                   'Compare the estimate with the latest information — the insolvent customer and the long-overdue balances.',
                   'Recommend revising the estimate (specific provision for the insolvent customer plus a higher general rate if justified).',
                   'Record that the revision is a change in estimate, recognised in the current period.'],
         'takeaway': 'Estimates must use the latest information. "Same as last year" is not a reason when circumstances have changed.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'According to Chambers\' definition, the three elements of measurement are identification of objects and events, selection of a standard or scale, and:', 'options': ['Evaluation of the dimension of the measurement scale', 'Recording in the journal', 'Communication to users', 'Audit of the figures'], 'answer': 0, 'explain': 'The third element is evaluating the dimension (stability) of the standard or scale.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Numbers that indicate position in an ordered sequence (first, second, third) are called:', 'options': ['Ordinal numbers', 'Cardinal numbers', 'Prime numbers', 'Index numbers'], 'answer': 0, 'explain': 'Ordinal numbers show order; cardinal numbers show "how many". Accountants use cardinal numbers.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Money is not an ideal scale of measurement mainly because:', 'options': ['Its purchasing power changes and it differs across countries', 'It cannot be added or subtracted', 'It is not accepted by banks', 'It is too precise'], 'answer': 0, 'explain': 'Money lacks universal denomination and is not stable in dimension (prices change).', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'The valuation principle commonly applied to inventories (lower of cost and net realisable value) involves:', 'options': ['Realisable value', 'Present value', 'Current cost only', 'Replacement value only'], 'answer': 0, 'explain': 'Inventory is shown at cost or net realisable value, whichever is less — so the realisable-value basis comes into play.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Present value of ₹1,21,000 receivable after 2 years, discounted at 10% a year, is:', 'options': ['₹1,00,000', '₹1,10,000', '₹96,800', '₹1,21,000'], 'answer': 0, 'check': '121000/1.1**2', 'explain': 'P = A ÷ (1 + i)^n = 1,21,000 ÷ 1.21 = ₹1,00,000.', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'A machine was bought for ₹5,00,000 plus freight ₹20,000 and installation ₹30,000. Its historical cost is:', 'options': ['₹5,50,000', '₹5,00,000', '₹5,20,000', '₹5,30,000'], 'answer': 0, 'check': '500000+20000+30000', 'explain': 'Historical cost is the acquisition price including costs to bring the asset into use.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'A liability carried at the undiscounted amount of cash that would be required to settle it today is measured at:', 'options': ['Current cost', 'Historical cost', 'Present value', 'Realisable value'], 'answer': 0, 'explain': 'Under current cost, liabilities are carried at the undiscounted amount needed to settle the obligation currently.', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'A loan of USD 20,000 was recorded at ₹82 per dollar. At the year end the rate is ₹85. The rupee amount of the loan at the year-end rate is:', 'options': ['₹17,00,000', '₹16,40,000', '₹60,000', '₹33,40,000'], 'answer': 0, 'check': '20000*85', 'explain': '20,000 × 85 = ₹17,00,000 — ₹60,000 more than originally recorded, showing that money is not a universal, stable scale.', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'Which of these is an accounting estimate?', 'options': ['Useful life of a machine', 'Cash paid for rent', 'Share capital issued', 'Invoice value of goods sold'], 'answer': 0, 'explain': 'Useful life is an estimate based on judgement; the others are measured facts.', 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'Machine cost ₹9,00,000, life 10 years, straight-line, no residual value. After 3 years the remaining life is revised to 4 years. Revised annual depreciation is:', 'options': ['₹1,57,500', '₹90,000', '₹2,25,000', '₹1,28,571'], 'answer': 0, 'check': '(900000-90000*3)/4', 'explain': 'Carrying amount after 3 years = 9,00,000 − 2,70,000 = 6,30,000; ÷ 4 = ₹1,57,500 a year from the year of change.', 'concept': 'c7', 'difficulty': 'hard'},
        {'id': 'm11', 'q': 'The present value basis is most commonly used in accounting for:', 'options': ['Investments and loans', 'Inventories', 'Petty cash', 'Share capital'], 'answer': 0, 'explain': 'Present value is common in accounting for investments and loans.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'To an economist, value means utility (satisfaction). In accounting, value is:', 'options': ['Measured in money using a cardinal scale', 'Expressed on an ordinal scale of satisfaction', 'Always the current market price', 'Not measured at all'], 'answer': 0, 'explain': 'Accountants use a money surrogate and cardinal numbers; historical cost is one such value.', 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm13', 'q': 'Present value of ₹50,000 a year for 3 years at 10% (rounded to the nearest rupee) is:', 'options': ['₹1,24,343', '₹1,50,000', '₹1,36,364', '₹1,12,697'], 'answer': 0, 'check': 'round(50000*(1-1.1**-3)/0.1)', 'explain': 'PV = 50,000/0.10 × [1 − 1/(1.10)^3] = 5,00,000 × 0.24869 = ₹1,24,343.', 'concept': 'c5', 'difficulty': 'hard'},
    ]

    q1c = Checks()
    q1_hc = q1c.add('1500000+75000+25000', 'Historical cost: price + freight + installation')
    q1_pv = q1c.add('round(300000*(1-1.1**-4)/0.1)', 'PV of ₹3,00,000 a year for 4 years @ 10%')
    q1_l_cc = q1c.add('400000*101/100', 'Loan at current cost with 1% prepayment penalty')
    q1_l_pv = q1c.add('round(40000*(1-1.1**-3)/0.1)+round(400000/1.1**3)', 'PV of loan: interest ₹40,000 for 3 years + principal after 3 years @ 10%')
    q1_tbl = table(['Item', 'Historical cost (₹)', 'Current cost (₹)', 'Realisable value (₹)', 'Present value (₹)'], [
        ['Machine', inr(q1_hc), '22,00,000', '12,00,000', inr(q1_pv)],
        ['10% Loan', '4,00,000', inr(q1_l_cc), '4,00,000', inr(q1_l_pv)],
    ])

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
         'q': 'Meridian Ltd bought a machine some years ago for ₹15,00,000 and paid freight ₹75,000 and installation ₹25,000. It also has a 10% loan of ₹4,00,000 repayable in 3 years. Today: an equivalent machine would cost ₹22,00,000; the machine could be sold in an orderly sale for ₹12,00,000; it will generate net cash inflows of ₹3,00,000 a year for 4 years; the lender would accept immediate repayment with a 1% penalty; the discount rate is 10%. Value the machine and the loan under the four valuation principles.',
         'model': [wn('Historical cost', f'Machine 15,00,000 + 75,000 + 25,000 = ₹{inr(q1_hc)}; loan at proceeds ₹4,00,000.'),
                   wn('Current cost', f'Machine ₹22,00,000; loan 4,00,000 × 101% = ₹{inr(q1_l_cc)}.'),
                   wn('Realisable value', 'Machine ₹12,00,000 (orderly sale); loan settlement value in the normal course ₹4,00,000.'),
                   wn('Present value', f'Machine: 3,00,000/0.10 × [1 − 1/(1.10)^4] = ₹{inr(q1_pv)}. Loan: interest 40,000/0.10 × [1 − 1/(1.10)^3] + 4,00,000/(1.10)^3 = ₹{inr(q1_l_pv)}.'),
                   q1_tbl],
         'scheme': [
             {'id': 's1', 'pt': f'Historical cost ₹{inr(q1_hc)} and ₹4,00,000', 'm': 1, 'skill': 'computation'},
             {'id': 's2', 'pt': f'Current cost ₹22,00,000 and ₹{inr(q1_l_cc)}', 'm': 1, 'skill': 'computation'},
             {'id': 's3', 'pt': 'Realisable value ₹12,00,000 and ₹4,00,000', 'm': 1, 'skill': 'computation'},
             {'id': 's4', 'pt': f'PV of machine ₹{inr(q1_pv)}', 'm': 1, 'skill': 'computation'},
             {'id': 's5', 'pt': f'PV of loan ₹{inr(q1_l_pv)} (interest + principal discounted)', 'm': 1.5, 'skill': 'computation'},
             {'id': 's6', 'pt': 'Summary table', 'm': 0.5, 'skill': 'presentation'},
         ],
         'remarks': ['The present value of the loan is where most candidates lose marks — both the interest stream and the principal must be discounted.', 'Several candidates leave freight and installation out of historical cost.'],
         'mistakes': ['Discounting only the principal of the loan.', 'Using the realisable value ₹12,00,000 as current cost.'],
         'tips': ['Show the formula before substituting numbers; step marks follow the formula.', 'End with a four-column summary table.']},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': '"Accounting is not an exact measurement discipline." Discuss with reference to the elements of measurement.',
         'model': [p('Chambers defines measurement as assigning numbers to objects and events by rules that specify the property, the scale and the dimension of the unit. Its three elements are: identification of objects and events, selection of a standard or scale, and evaluation of the dimension of that scale.'),
                   ul(['Objects and events: accounting measures information for decisions. Past and present items can be measured with some accuracy, but future events, which decisions depend on, can only be predicted.',
                       'Scale: money is the scale, but it has no universal denomination (rupee, dollar, pound) and exchange rates fluctuate — a foreign-currency loan measures differently at different dates.',
                       'Dimension: an ideal scale is stable (a kilogram is always a kilogram); money\'s purchasing power changes with prices, so figures of different years are not truly comparable — sales value can rise while quantity falls.',
                       'Also, much of accounting — recording, classifying, summarising and communicating — is not measurement at all, and measurement rests on assumptions (going concern, consistency, accrual) and chosen policies.']),
                   p('Hence measurement is an important part of accounting, but accounting is not an exact measurement discipline.')],
         'scheme': [
             {'id': 's1', 'pt': 'Definition of measurement and the three elements', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Objects/events: future only predicted', 'm': 1, 'skill': 'analysis'},
             {'id': 's3', 'pt': 'Scale: money not universal; exchange-rate example', 'm': 1, 'skill': 'analysis'},
             {'id': 's4', 'pt': 'Dimension: money unstable; price-change example', 'm': 1, 'skill': 'analysis'},
             {'id': 's5', 'pt': 'Non-measurement functions and assumptions; conclusion', 'm': 1, 'skill': 'conclusion'},
         ],
         'remarks': ['Answers organised around the three elements score far better than a general essay.', 'A small numerical example for the instability of money makes the point convincingly.'],
         'mistakes': ['Arguing that accounting is exact because figures are accurate to the paisa.', 'Omitting the conclusion.'],
         'tips': ['Use the three elements as sub-headings and end with a one-line conclusion.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'What are accounting estimates? Give four situations where estimates are needed, and explain what a change in accounting estimate means.',
         'model': [p('Some items cannot be measured precisely because they depend on uncertain future events, yet they must be recorded. Management therefore makes reasonable estimates of assets, liabilities, income and expenses using the latest information, the existing situation and past experience — for example, provision for doubtful debts.'),
                   ul(['Useful life and residual value of plant (depreciation) and period of benefit of a patent (amortisation).', 'Provision for doubtful debts and inventory obsolescence.', 'Provisions for warranties, employee benefits and unforeseen contingencies on long-term contracts.', 'Provision for taxes where tax authorities may interpret items differently.']),
                   p('A change in accounting estimate is the difference between a figure estimated earlier and its re-estimate, or the actual result, in the current period — caused by changed circumstances, new information or more experience. Example: a machine expected to last 10 years becomes obsolete and is now expected to last only 3 more years; depreciation is revised from the period of change.')],
         'scheme': [
             {'id': 's1', 'pt': 'Meaning of accounting estimates', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Four valid situations', 'm': 2, 'skill': 'application'},
             {'id': 's3', 'pt': 'Change in estimate explained with example', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Examples carry half the marks — give four distinct ones.'],
         'mistakes': ['Calling a change in estimate an error or a change in accounting policy.'],
         'tips': ['Give the four situations as a numbered list.']},
    ]

    viva = [
        V('v1', 'What is measurement, and what are its three elements?',
          'Measurement means assigning numbers to objects and events according to rules that specify the property to be measured, the scale and the dimension of the unit. Its three elements are identifying the objects and events to be measured, selecting the standard or scale, and evaluating the dimension of that scale.',
          [P('p1', 'Assigning numbers to objects/events according to rules', 4, 'number|numeral|figure|quantif|value', 'object|event|thing|item|rule', min=2),
           P('p2', 'Identification of objects and events', 2, 'identif|object|what to measure|select item|events to be measured', min=1),
           P('p3', 'Selection of standard or scale', 2, 'scale|standard|unit|yardstick', min=1),
           P('p4', 'Evaluation of dimension of the scale', 2, 'dimension|stabil|stable')], 'c1'),
        V('v2', 'Why is money not a perfect scale of measurement?',
          'Money is not a perfect scale because it is not universal — every country has its own currency and exchange rates keep changing — and it is not stable in dimension, because its purchasing power changes with prices, so figures of different years are not comparable.',
          [P('p1', 'Not universal — different currencies, changing exchange rates', 5, 'not universal|isn t universal|no universal|lack universal|neither universal|different currenc|currenc differ|own currenc|each country|every country|different countr|exchange rate|dollar|pound', min=1),
           P('p2', 'Not stable — purchasing power changes with prices/inflation', 5, 'not stabl|isn t stabl|unstabl|no stabl|lack stabil|nor stabl|not constant|purchasing power chang|purchasing power fall|purchasing power vari|purchasing power declin|inflation|price chang|price rise|value chang|value of money chang|change in value|fluctuat|rubber', min=1)], 'c3'),
        V('v3', 'Name and explain the four valuation principles.',
          'The four valuation principles are historical cost, which is the acquisition price paid; current cost, which is what it would cost to acquire the same or an equivalent asset now; realisable value, which is what the asset would fetch now in an orderly sale; and present value, which is the discounted value of the future net cash flows.',
          [P('p1', 'Historical cost — acquisition price', 3, 'historical cost|historic cost|acquisition|original cost|cost paid|purchase price|price paid', min=1),
           P('p2', 'Current cost — cost to acquire now / replacement', 2, 'current cost|replacement|buy now|acquire now|today|currently', min=1),
           P('p3', 'Realisable value — amount obtainable by orderly sale', 2, 'realisable|realizable|sale|sell|selling|disposal|fetch', min=1),
           P('p4', 'Present value — discounted future cash flows', 3, 'present value|discount', 'future|cash flow|inflow|outflow', min=2)], 'c5'),
        V('v4', 'Explain the present value basis with the idea of time value of money.',
          'Under the present value basis, an asset is carried at the discounted value of the future net cash inflows it will generate, and a liability at the discounted value of the future cash outflows needed to settle it. It is based on the time value of money: a rupee received in future is worth less than a rupee today, so future amounts are discounted using P equals A divided by one plus i to the power n.',
          [P('p1', 'Asset at discounted value of future net cash inflows', 3, 'asset', 'discount|present value', 'inflow|future cash|cash flow|cash generat|earning', min=3),
           P('p2', 'Liability at discounted value of future outflows', 2, 'liabilit', 'outflow|pay|settle|repay', min=2),
           P('p3', 'Time value of money — future rupee worth less today', 3, 'time value|worth less|less than|less valuable|sacrifice|interest', min=1),
           P('p4', 'Formula P = A / (1 + i)^n', 2, 'divided|formula|power|1 plus|one plus|1 i|discounting|discount rate|rate', min=1)], 'c5'),
        V('v5', 'What are accounting estimates, and what is meant by a change in estimate?',
          'Accounting estimates are reasonable judgements made for items that cannot be measured precisely because they depend on uncertain future events, such as provision for doubtful debts, useful life of machinery or inventory obsolescence. A change in estimate arises when an earlier estimate is revised because of new information, changed circumstances or more experience, for example when the remaining useful life of a machine is reduced.',
          [P('p1', 'Judgements for items that cannot be measured precisely / uncertain future', 3, 'uncertain|cannot be measured|can t be measured|not measur|precis|exact|judg|approximat|reasonable', min=1),
           P('p2', 'Examples: doubtful debts, useful life, obsolescence, depreciation, provisions, tax', 3, 'doubtful|bad debt', 'useful life|life|depreciat|residual', 'obsolesc|warranty|provision|tax', min=2),
           P('p3', 'Change in estimate = revision due to new information / changed circumstances', 4, 'revis|re estimat|reestimat|change|updat', 'new information|new data|circumstance|experience|development|latest', min=2)], 'c7'),
        V('v6', 'Is accounting an exact measurement discipline?',
          'No, accounting is not an exact measurement discipline. Its scale, money, is neither universal nor stable in dimension, future events can only be predicted, and much of accounting such as recording, classifying, summarising and communicating is not measurement at all, although measurement is an important part of it.',
          [P('p1', 'No — not an exact measurement discipline', 4, ALT('{n} exact', '{n} an exact', '{n} perfect', '{n} pure', '{n} precise', '{n} fully', '{n} purely', 'inexact', 'no', n=('not', 'isn t', 'never', 'no', 'cannot', 'can t'))),
           P('p2', 'Money scale not universal / not stable', 3, 'money|currency|scale', 'stabl|universal|inflation|purchasing power|exchange|change|not stabl|not universal|unstabl|neither universal|nor stabl|not constant|fluctuat|vari', min=2),
           P('p3', 'Recording, summarising, communicating are not measurement; future only predicted', 3, 'record|classif|summar|communicat|predict|future|assumption', min=1)], 'c4'),
    ]

    c = Checks()
    k_hc = c.add('2400000+100000', 'Historical cost: price + installation')
    k_pv = c.add('round(500000*(1-1.1**-5)/0.1)', 'PV of ₹5,00,000 a year for 5 years @ 10%')
    k_dep_new = c.add('(2500000-250000*4)/3', 'Revised depreciation: carrying amount after 4 years ÷ 3 remaining years')
    cases = [{
        'id': 'k1', 'title': 'Harbour Logistics — valuing a crane', 'difficulty': 'hard',
        'case': ('Harbour Logistics bought a crane on 1 April 2022 for ₹24,00,000 and paid ₹1,00,000 for installation. It was depreciated on the straight-line basis over 10 years with no residual value. On 1 April 2026: a new equivalent crane costs ₹32,00,000; the old crane could be sold in an orderly sale for ₹17,00,000; '
                 'it is expected to produce net cash inflows of ₹5,00,000 a year for the next 5 years; and the discount rate is 10%. Engineers also say that, because of heavy use, the crane will last only 3 more years instead of 6.'),
        'mcqs': [
            M('k1a', 'What is the historical cost of the crane?', [R(k_hc), '₹24,00,000', '₹32,00,000', '₹17,00,000'], 0,
              'Acquisition price plus installation: 24,00,000 + 1,00,000.', 'core', '2400000+100000'),
            M('k1b', 'What is the present value of the expected inflows (to the nearest rupee)?', [R(k_pv), '₹25,00,000', '₹22,72,727', '₹15,52,303'], 0,
              f'5,00,000/0.10 × [1 − 1/(1.10)^5] = {R(k_pv)}.', 'hard', 'round(500000*(1-1.1**-5)/0.1)'),
            M('k1c', 'The ₹17,00,000 the crane could fetch in an orderly sale represents which basis?', ['Realisable value', 'Current cost', 'Historical cost', 'Present value'], 0,
              'Realisable value is the amount obtainable now by selling the asset in an orderly disposal.', 'core'),
            M('k1d', 'After revising the remaining life to 3 years, the annual depreciation from 2026-27 is:', [R(k_dep_new), '₹2,50,000', '₹3,75,000', '₹8,33,333'], 0,
              f'Carrying amount after 4 years = 25,00,000 − 4 × 2,50,000 = 15,00,000; ÷ 3 = {R(k_dep_new)}. This is a change in accounting estimate applied from the year of change.', 'hard', '(2500000-250000*4)/3'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 6,
        'title': 'Accounting as a Measurement Discipline – Valuation Principles, Accounting Estimates',
        'outcomes': [
            'Explain the meaning of measurement and its three elements, and judge how far accounting is a measurement discipline.',
            'Explain why money is an imperfect scale — not universal and not stable in dimension.',
            'Measure an asset and a liability under historical cost, current cost, realisable value and present value, including discounting.',
            'Distinguish measurement from valuation.',
            'Explain accounting estimates, give examples and account for a change in estimate.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['fnd-p1-ch01-u02'],
                 'exam_tip': 'Learn the four bases for both assets and liabilities, and practise one present-value computation with the annuity formula. Theory questions often ask "Is accounting a measurement discipline?".'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Measurement (Chambers): numbers assigned to objects/events by rules specifying property, scale and dimension. Elements: objects/events, standard or scale, dimension of the scale.',
                        'Money is the scale: not universal (currencies, exchange rates) and not stable in dimension (purchasing power) — accounting is not an exact measurement discipline.',
                        'Four bases: historical cost, current cost, realisable (settlement) value, present value — each defined for assets and for liabilities.',
                        'Value to the economist = utility (ordinal); to the accountant = money measure (cardinal).',
                        'Estimates (doubtful debts, useful life, obsolescence, warranties, tax) use latest information; changes in estimate are applied from the period of change.'],
            'remember': ['P = A ÷ (1 + i)^n; annuity PV = A/i × [1 − 1/(1 + i)^n].', 'Historical cost of an asset includes freight and installation.', 'Inventories — lower of cost and NRV; investments and loans — present value; long-term assets — historical cost.'],
            'traps': ['Current cost of a liability is undiscounted (includes any penalty to settle now).', 'Present value of a loan = PV of interest + PV of principal.', 'A change in useful life is a change in estimate, not in accounting policy.'],
        },
        'quickref': [
            {'k': 'Elements of measurement', 'v': 'Objects/events · Standard or scale · Dimension of the scale'},
            {'k': 'Historical cost', 'v': 'Acquisition price (assets); proceeds received (liabilities)'},
            {'k': 'Current cost', 'v': 'Cost to acquire equivalent now; undiscounted amount to settle now'},
            {'k': 'Realisable value', 'v': 'Orderly-sale proceeds; settlement value in normal course'},
            {'k': 'Present value', 'v': 'Discounted future net cash inflows / outflows'},
            {'k': 'Discounting', 'v': 'P = A ÷ (1 + i)^n · Annuity: A/i × [1 − 1/(1 + i)^n]'},
            {'k': 'Change in estimate', 'v': 'Revised figure applied from the period of change onwards'},
        ],
        'viva': viva, 'cases': cases,
    }
