"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 2 Treasury and Cash Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u02'
T1 = 'Treasury management and motives for holding cash'
T2 = 'Cash budgets'
T3 = 'Optimum cash balance: Baumol and Miller–Orr'
T4 = 'Techniques of cash management'


def build():
    ck = Checks()
    c = ck.add('(2*2400000*300/0.10)**0.5', 'Optimum cash conversion size (Baumol)')
    n = ck.add('2400000/120000', 'Number of conversions a year')
    tc = ck.add('20*300 + 120000/2*0.10', 'Total cost = transaction + holding')
    i1 = {'id': 'i1', 'title': 'How much cash to draw each time?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A firm needs ₹24 lakh of cash evenly over the year. Each conversion of securities into cash costs ₹300; securities earn 10%. Using Baumol\'s model find the optimum conversion size, number of conversions and total cost.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Optimum cash (C)', '√(2 × 24,00,000 × 300 ÷ 0.10)', '₹' + inr(c)],
              ['Conversions a year', '24,00,000 ÷ 1,20,000', inr(n)],
              ['Transaction cost', '20 × 300', '₹6,000'],
              ['Holding cost', '1,20,000 ÷ 2 × 10%', '₹6,000'],
              ['Total cost', '', '₹' + inr(tc)]], title='Baumol model'),
              note('At the optimum, transaction cost equals holding (opportunity) cost.')],
          'checks': list(ck)}

    ck2 = Checks()
    spread = ck2.add('3*(0.75*50*4000000/0.00025)**(1/3)', 'Spread (Miller–Orr)')
    upper = ck2.add('10000+25303', 'Upper limit (approx.)')
    ret = ck2.add('10000+25303/3', 'Return point (approx.)')
    i2 = {'id': 'i2', 'title': 'Cash that swings daily', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Minimum cash balance ₹10,000; cost per transaction ₹50; variance of daily cash flows ₹40,00,000; daily interest rate 0.025%. Using Miller–Orr, find the spread, upper limit and return point.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Spread', '3 × (¾ × 50 × 40,00,000 ÷ 0.00025)^(1/3)', inr(round(spread))],
              ['Upper limit', 'Lower limit + spread', inr(round(upper))],
              ['Return point', 'Lower limit + spread ÷ 3', inr(round(ret))]], title='Miller–Orr model'),
              p('When cash hits the upper limit, buy securities to bring it down to the return point; when it hits the lower limit, sell securities to restore it to the return point.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Treasury management handles cash, liquidity, funding, investment of surplus funds, foreign exchange and interest-rate risks, and banking relationships.',
            'Motives for holding cash (Keynes): transaction (day-to-day payments), precautionary (unexpected needs) and speculative (taking advantage of opportunities). Banks may also require compensating balances.',
            'Objectives: meet payment obligations on time while minimising idle balances; invest surpluses in safe, liquid instruments such as treasury bills, commercial paper, certificates of deposit and liquid funds.'],
          'Cash is needed to pay bills, but idle cash earns nothing — treasury balances the two.',
          'A company parks month-end surpluses in an overnight liquid fund instead of a current account.'),
        C('c2', T2, [
            'A cash budget forecasts receipts and payments for each sub-period to show surpluses and shortages in advance. Methods: receipts and payments method (most common), adjusted profit and loss method, and balance sheet method.',
            'Receipts: cash sales, collections from debtors (by lag pattern), other income; payments: purchases (by credit terms), wages, overheads (cash part), capital expenditure, taxes, dividends. Depreciation and other non-cash items are excluded.',
            'Shortages are covered by arranging finance; surpluses are invested.'],
          'A cash budget is the calendar of money in and out.',
          'Sales in March collected in April appear as April receipts.'),
        C('c3', T3, [
            'Baumol model treats cash like inventory: optimum conversion size C = √(2U × P ÷ S), where U is annual cash requirement, P the cost per conversion and S the interest rate on securities. Total cost = (U ÷ C) × P + (C ÷ 2) × S.',
            'Miller–Orr model allows random daily cash flows: Spread = 3 × (¾ × transaction cost × variance ÷ interest rate per day)^(1/3); upper limit = lower limit + spread; return point = lower limit + spread ÷ 3.',
            'Other approaches: cash planning and cash budgets, and the Stone model (using forecasts to decide whether to act at limits).'],
          'Baumol suits steady cash use; Miller–Orr suits unpredictable swings.',
          'Higher interest rates lower the optimum cash balance in both models.'),
        C('c4', T4, [
            'Speeding collections: concentration banking, lock-box systems, electronic transfers (NEFT, RTGS, UPI), prompt billing, and cash discounts.',
            'Slowing payments ethically: pay on the due date, centralised payments, and using float (the gap between when a cheque is issued and when it is cleared).',
            'Managing float: disbursement float (helpful to payer) and collection float (harmful); net float = disbursement float − collection float. Electronic payments have reduced float in India. Virtual accounts and cash pooling help corporate groups.'],
          'Get money in faster and let it go out on time — not earlier.',
          'A dealer network paying through UPI cuts collection float to near zero.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Weekly cash forecast', 'role': 'Treasury trainee',
             'situation': 'The CFO wants to know if a ₹2 crore tax payment next week needs a borrowing.',
             'steps': ['List expected receipts by day.', 'List committed payments.', 'Find the lowest balance point.', 'Arrange a short-term line or liquidate investments if needed.'],
             'takeaway': 'Short-horizon forecasts prevent costly last-minute borrowing.'}]

    mcqs = [
        Q('m1', 'Cash held to meet unexpected needs is for the:', ['Precautionary motive', 'Transaction motive', 'Speculative motive', 'Compensating motive'], 0,
          'Precautionary balances act as a cushion. In practice: often held in liquid investments.', 'c1', T1),
        Q('m2', 'Which item is excluded from a cash budget?', ['Depreciation', 'Wages paid', 'Collections from debtors', 'Purchase of a machine'], 0,
          'Depreciation is non-cash. In practice: capital payments are included when paid.', 'c2', T2),
        Q('m3', 'Under Baumol, if interest rates rise, the optimum cash conversion size:', ['Falls', 'Rises', 'Is unchanged', 'Doubles'], 0,
          'Interest is in the denominator. In practice: higher returns on securities favour smaller balances.', 'c3', T3),
        Q('m4', 'U = ₹12 lakh, P = ₹100, S = 6%. Baumol optimum (approx.):', ['₹63,246', '₹40,000', '₹1,00,000', '₹20,000'], 0,
          '√(2 × 12,00,000 × 100 ÷ 0.06) = √4,00,00,00,000 ≈ ₹63,246. In practice: round to a practical figure.', 'c3', T3, 'moderate', check=63246),
        Q('m5', 'In Miller–Orr, the return point equals:', ['Lower limit + spread ÷ 3', 'Upper limit − spread ÷ 3', 'Lower limit + spread', 'Spread ÷ 2'], 0,
          'The return point is one-third of the spread above the lower limit. In practice: actions occur only at limits.', 'c3', T3),
        Q('m6', 'A lock-box system is used to:', ['Speed up collection of receivables', 'Delay payments', 'Store cash safely', 'Invest surplus funds'], 0,
          'Customers pay into post boxes cleared by banks, reducing mail and processing float. In practice: replaced largely by electronic collections.', 'c4', T4),
        Q('m7', 'Disbursement float is:', ['Time between issuing a cheque and its clearing', 'Time between sale and billing', 'Cash held for emergencies', 'Excess of receipts over payments'], 0,
          'It lets the payer use funds a little longer. In practice: electronic payments shrink it.', 'c4', T4),
        Q('m8', 'At Baumol\'s optimum:', ['Transaction cost equals holding cost', 'Holding cost is zero', 'Transaction cost is zero', 'Total cost is highest'], 0,
          'The square-root formula balances the two costs. In practice: use as a check.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Optimum C', 2, 'computation', 'optimum', nums=[c]), S('s2', 'Conversions', 1, 'computation', 'conversions', nums=[n]), S('s3', 'Total cost', 2, 'computation', 'total', nums=[tc])],
          ['Show both costs.'], ['Using monthly interest.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Spread', 3, 'computation', 'spread', nums=[round(spread)]), S('s2', 'Limits', 2, 'computation', 'upper|return', nums=[round(upper), round(ret)])],
          ['Use daily rate and variance.'], ['Using standard deviation instead of variance.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the three motives for holding cash.', 'Transaction, precautionary and speculative motives.',
          [P('p1', 'Transaction', 4, 'transaction'), P('p2', 'Precaution and speculation', 6, 'precaution|speculat')], 'c1'),
        V('v2', 'Why is a cash budget prepared?', 'To forecast surpluses and shortages period by period so that financing or investment can be arranged in advance.',
          [P('p1', 'Surplus and shortage', 5, 'surplus|shortage'), P('p2', 'Arrange in advance', 5, 'advance|arrange')], 'c2'),
        V('v3', 'State Baumol\'s formula.', 'Optimum cash equals the square root of two times annual cash need times cost per conversion, divided by the interest rate.',
          [P('p1', 'Square root', 4, 'square root'), P('p2', 'Variables', 6, 'conversion|interest')], 'c3'),
        V('v4', 'When does Miller–Orr suggest action?', 'Only when cash reaches the upper or lower limit, bringing it back to the return point by buying or selling securities.',
          [P('p1', 'At limits', 5, 'limit'), P('p2', 'Return point', 5, 'return point')], 'c3'),
        V('v5', 'What is concentration banking?', 'Collecting payments at local branches and transferring surpluses quickly to a central account to reduce collection time.',
          [P('p1', 'Local collection', 5, 'local|branch'), P('p2', 'Central account', 5, 'central')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Pinnacle Retail', 'difficulty': 'moderate',
              'case': 'Pinnacle Retail\'s sales: April ₹40 lakh, May ₹50 lakh, June ₹60 lakh; 25% cash, 75% collected the following month (March sales ₹36 lakh). Purchases are 60% of next month\'s sales, paid in the month of purchase. Opening cash on 1 April ₹5 lakh.',
              'mcqs': [
                  M('k1a', 'April collections (₹ lakh):', ['37', '40', '30', '27'], 0,
                    'Cash 25% × 40 = 10 + 75% × 36 = 27 → 37. In practice: track by month.', 'moderate', check=37, topic=T2),
                  M('k1b', 'April purchase payments (₹ lakh):', ['30', '24', '36', '40'], 0,
                    '60% of May sales 50 = 30. In practice: purchases lead sales.', 'moderate', check=30, topic=T2),
                  M('k1c', 'Closing cash on 30 April (₹ lakh), ignoring other items:', ['12', '7', '5', '17'], 0,
                    '5 + 37 − 30 = 12. In practice: add wages and other costs in reality.', 'moderate', check=12, topic=T2),
                  M('k1d', 'Surplus cash is best kept in:', ['Short-term liquid investments', 'Idle current account', 'Long-term equity', 'Land'], 0,
                    'Treasury invests surpluses safely and liquidly. In practice: liquid funds or T-bills.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 2, 'Treasury and Cash Management',
                ['Explain treasury functions and motives for holding cash.',
                 'Prepare a cash budget.',
                 'Apply Baumol and Miller–Orr models.',
                 'Explain techniques for managing collections, payments and float.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 40}, 'prereq': ['int-p6-a-ch09-u01'],
                 'exam_tip': 'In cash budgets, build a receipts table by month first; payments follow the same logic.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Motives: transaction, precautionary, speculative.',
                             'Cash budget: receipts and payments; no non-cash items.',
                             'Baumol: C = √(2UP/S).',
                             'Miller–Orr: spread = 3(¾ × b × σ² ÷ i)^(1/3); RP = L + spread/3.',
                             'Speed collections; manage float.'],
                 'remember': ['Use daily interest and variance in Miller–Orr.'],
                 'traps': ['Depreciation never appears in a cash budget.']},
                [('Baumol', '√(2UP/S)'), ('MO return point', 'L + Z/3'), ('MO upper limit', 'L + Z')],
                viva, cases)
