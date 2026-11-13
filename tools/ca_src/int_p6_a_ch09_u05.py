"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 5 Management of Payables (Creditors).
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u05'
T1 = 'Trade credit as a source of finance'
T2 = 'Cost of forgoing cash discounts'
T3 = 'Managing payables in practice'


def build():
    ck = Checks()
    simple = ck.add('3/97*365/45*100', 'Simple annual cost of not taking the discount (%)')
    comp = ck.add('((100/97)**(365/45)-1)*100', 'Effective (compound) annual cost (%)')
    i1 = {'id': 'i1', 'title': 'Is the discount worth taking?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A supplier offers "3/15, net 60". Compute the simple and compound annual cost of not taking the discount. The firm can borrow from its bank at 14%. Advise.',
          'solution': [table(['Measure', 'Working', 'Cost'], [
              ['Days gained by not paying early', '60 − 15', '45 days'],
              ['Simple annual cost', '3/97 × 365/45', str(round(simple, 2)) + '%'],
              ['Effective annual cost', '(100/97)^(365/45) − 1', str(round(comp, 2)) + '%']], title='Cost of trade credit'),
              p('Forgoing the discount costs about 25–28% a year, far above the 14% bank rate. Borrow from the bank and pay on day 15.')],
          'checks': list(ck)}

    ck2 = Checks()
    days = ck2.add('6/(48.67/365)', 'Creditors days')
    i2 = {'id': 'i2', 'title': 'How long do we take to pay?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Average trade creditors ₹6 lakh; annual credit purchases ₹48.67 lakh. Compute creditors\' days (365-day year) and comment if supplier terms are 45 days.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Creditors\' days', '6 ÷ (48.67 ÷ 365)', str(round(days)) + ' days']], title='Payables period'),
              p('The firm pays in about 45 days — in line with terms. Stretching further could strain supplier relations and lose discounts.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Trade credit is a spontaneous short-term source of finance arising from normal purchases; it grows automatically with business volume and needs no formal agreement.',
            'Costs of using it: discounts forgone, loss of goodwill if terms are overstepped, administrative costs and conditions such as minimum order sizes.',
            'Costs of not using it: interest cost of paying early (trade credit is otherwise interest-free), and with inflation, paying later in money of lower value is beneficial.'],
          'Supplier credit is cheap money — until you give up a discount for it.',
          'A retailer taking 30 days\' credit on ₹10 lakh of monthly purchases effectively borrows ₹10 lakh interest-free.'),
        C('c2', T2, [
            'Simple annual cost of forgoing a discount = [d ÷ (100 − d)] × (365 ÷ t), where d is the discount % and t the extra days of credit obtained (credit period − discount period).',
            'Effective annual cost, allowing for compounding = (100 ÷ (100 − d))^(365 ÷ t) − 1.',
            'Decision: if the cost of forgoing exceeds the firm\'s cost of borrowing (or return on alternative investment), take the discount; otherwise use the full credit period.'],
          'A small discount for a short wait can carry a very high annual cost.',
          '"1/10, net 30" costs about 18.4% a year if forgone.'),
        C('c3', T3, [
            'Good practice: pay on the due date (not earlier, not later), negotiate better terms with key suppliers, centralise payments, and use electronic payments.',
            'Monitor creditors\' days and ageing; avoid stretching payables, which damages reputation and supply.',
            'Small suppliers (MSMEs) must be paid within the agreed period subject to a maximum of 45 days under the MSMED Act, with interest at three times the bank rate on delays, and companies report MSME dues; delayed MSME payments also affect tax deductibility of the expense.'],
          'Payables management is about timing and trust, not just delay.',
          'A firm that delays MSME payments beyond 45 days faces penal interest and disclosure.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Discount policy', 'role': 'Finance analyst trainee',
             'situation': 'Procurement wants to know which supplier discounts to take.',
             'steps': ['List suppliers with discount terms.', 'Compute the annual cost of forgoing each.', 'Compare with the bank borrowing rate.', 'Recommend which discounts to take.'],
             'takeaway': 'Take any discount whose forgone cost exceeds the cost of borrowing.'}]

    mcqs = [
        Q('m1', 'Trade credit is called a spontaneous source because it:', ['Arises automatically from normal purchases', 'Needs a formal loan agreement', 'Is long-term', 'Is from banks'], 0,
          'It rises and falls with purchases without negotiation each time. In practice: grows with sales.', 'c1', T1),
        Q('m2', 'Simple annual cost of forgoing "2/10, net 30" (365 days):', ['37.24%', '24.83%', '18.43%', '2%'], 0,
          '2/98 × 365/20 = 37.24%. In practice: almost always worth taking.', 'c2', T2, 'moderate', check=37.24),
        Q('m3', 'In the formula, t equals:', ['Credit period minus discount period', 'Discount period', 'Credit period', '365 minus credit period'], 0,
          't is the extra days gained by not taking the discount. In practice: 30 − 10 = 20 for "2/10, net 30".', 'c2', T2),
        Q('m4', 'If the cost of forgoing a discount is 20% and bank interest is 12%, the firm should:', ['Take the discount using bank funds', 'Forgo the discount', 'Pay after the due date', 'Ignore the supplier'], 0,
          'Borrowing at 12% to save 20% is profitable. In practice: check bank limits.', 'c2', T2),
        Q('m5', 'Stretching payables beyond terms may cause:', ['Loss of supplier goodwill and discounts', 'Lower inventory', 'Higher sales', 'Lower interest cost always'], 0,
          'Suppliers may restrict supply or credit. In practice: reputation matters.', 'c3', T3),
        Q('m6', 'Under the MSMED Act the maximum agreed payment period to MSME suppliers is:', ['45 days', '90 days', '30 days', '120 days'], 0,
          'Payment must be within the agreed period, not beyond 45 days. In practice: interest at three times bank rate applies on delay.', 'c3', T3, check=45),
        Q('m7', 'Average creditors ₹4 lakh; credit purchases ₹36.5 lakh (365 days). Creditors\' days:', ['40 days', '36 days', '45 days', '30 days'], 0,
          '4 ÷ (36.5 ÷ 365) = 4 ÷ 0.1 = 40 days. In practice: compare with supplier terms.', 'c3', T3, check=40),
        Q('m8', 'The compound cost of forgoing a discount is:', ['Higher than the simple cost', 'Lower than the simple cost', 'Equal to it', 'Zero'], 0,
          'Compounding over multiple periods in a year raises the effective cost. In practice: use for precise comparisons.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Days t', 1, 'computation', '45'), S('s2', 'Simple cost', 1.5, 'computation', 'simple', nums=[simple]),
           S('s3', 'Compound cost', 1.5, 'computation', 'effective', nums=[comp]), S('s4', 'Advice', 1, 'concept', 'borrow|bank')],
          ['Show both formulas.'], ['Using 60 days for t.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Days', 2, 'computation', 'days', nums=[days]), S('s2', 'Comment', 1, 'concept', 'terms|supplier')],
          ['Use credit purchases.'], ['Using sales instead of purchases.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Why is trade credit not free?', 'Because using the full credit period often means forgoing a cash discount, and overstepping terms damages goodwill.',
          [P('p1', 'Discount forgone', 6, 'discount'), P('p2', 'Goodwill', 4, 'goodwill')], 'c1'),
        V('v2', 'State the simple cost formula.', 'Discount divided by one hundred minus discount, multiplied by 365 divided by the extra days of credit.',
          [P('p1', 'd/(100 − d)', 5, 'hundred minus|100 −'), P('p2', '365/t', 5, '365')], 'c2'),
        V('v3', 'When should a discount be taken?', 'When the annual cost of forgoing it is higher than the firm\'s cost of borrowing or its return on surplus funds.',
          [P('p1', 'Compare costs', 5, 'higher|compare'), P('p2', 'Borrowing rate', 5, 'borrow')], 'c2'),
        V('v4', 'What is the MSMED Act requirement on payments?', 'Payments to micro and small suppliers must be made within the agreed period, not exceeding 45 days, with penal interest on delays.',
          [P('p1', '45 days', 6, '45'), P('p2', 'Penal interest', 4, 'interest')], 'c3'),
        V('v5', 'Name one good practice in managing payables.', 'Paying on the due date rather than early or late, while negotiating better terms with key suppliers.',
          [P('p1', 'Due date', 5, 'due date'), P('p2', 'Negotiation', 5, 'negotiat|terms')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Metro Electricals', 'difficulty': 'moderate',
              'case': 'Metro Electricals buys ₹1.2 crore a year from a supplier offering "1/10, net 40". Its overdraft rate is 11%. It currently pays on day 40.',
              'mcqs': [
                  M('k1a', 'Simple annual cost of forgoing the discount:', ['12.29%', '9.09%', '18.43%', '1.01%'], 0,
                    '1/99 × 365/30 = 12.29%. In practice: slightly above overdraft cost.', 'moderate', check=12.29, topic=T2),
                  M('k1b', 'Should Metro take the discount?', ['Yes, as 12.29% exceeds the 11% overdraft rate', 'No', 'Only in March', 'Only if it has surplus cash'], 0,
                    'Borrowing at 11% to avoid a 12.29% cost is beneficial. In practice: margin is thin, so check limits.', 'moderate', topic=T2),
                  M('k1c', 'Annual discount saved (₹):', ['1,20,000', '12,000', '2,40,000', '60,000'], 0,
                    '1% of ₹1.2 crore = ₹1,20,000. In practice: offset extra interest on 30 days\' funds.', 'core', check=120000, topic=T2),
                  M('k1d', 'Extra interest from paying 30 days earlier (₹, approx.):', ['1,07,000', '1,32,000', '33,000', '12,000'], 0,
                    'Average extra borrowing ≈ 1.19 crore × 30/365 ≈ ₹9.8 lakh × 11% ≈ ₹1.07 lakh — less than ₹1.2 lakh saved. In practice: net gain about ₹13,000.', 'hard', check=107000, topic=T2),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 5, 'Management of Payables (Creditors)',
                ['Explain trade credit and its costs and benefits.',
                 'Compute the cost of forgoing cash discounts.',
                 'Apply good payables practices including MSME rules.'],
                {'difficulty': 'core', 'minutes': {'learn': 15, 'practice': 25}, 'prereq': ['int-p6-a-ch09-u04'],
                 'exam_tip': 'Always compare the cost of forgoing a discount with the borrowing rate given.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Trade credit: spontaneous, interest-free unless discounts are forgone.',
                             'Simple cost = d/(100 − d) × 365/t; compound = (100/(100 − d))^(365/t) − 1.',
                             'Take discount if its cost exceeds borrowing cost.',
                             'Pay on due date; MSME limit 45 days.'],
                 'remember': ['t = credit period − discount period.'],
                 'traps': ['Using the full credit period as t.']},
                [('Simple cost', 'd/(100 − d) × 365/t'), ('Compound', '(100/(100 − d))^(365/t) − 1'), ('MSME', '45 days')],
                viva, cases)
