"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 4 Management of Receivables.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u04'
T1 = 'Objectives and costs of receivables'
T2 = 'Credit policy: standards, terms and evaluation'
T3 = 'Monitoring receivables and factoring'


def build():
    ck = Checks()
    cur = ck.add('50*0.40 - 50*0.60*30/360*0.15 - 50*1/100', 'Net benefit — current policy (₹ lakh)')
    prop = ck.add('60*0.40 - 60*0.60*60/360*0.15 - 60*2/100', 'Net benefit — proposed policy (₹ lakh)')
    gain = ck.add('21.9-19.125', 'Increase in net benefit (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Loosening credit terms', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Current credit sales ₹50 lakh with 30 days\' credit and bad debts 1%. Extending credit to 60 days is expected to raise sales to ₹60 lakh with bad debts of 2%. Variable cost is 60% of sales; required return 15%; use 360 days and value receivables at variable cost. Should the firm extend credit?',
          'solution': [table(['Item (₹ lakh)', 'Current', 'Proposed'], [
              ['Contribution (40%)', '20.00', '24.00'],
              ['Receivables at cost', '50 × 60% × 30/360 = 2.50', '60 × 60% × 60/360 = 6.00'],
              ['Cost of funds @15%', '(0.375)', '(0.90)'],
              ['Bad debts', '(0.50)', '(1.20)'],
              ['Net benefit', str(round(cur, 3)), str(round(prop, 3))]], title='Credit policy evaluation'),
              p('Proposed policy adds ₹' + str(round(gain, 3)) + ' lakh — extend credit.')],
          'checks': list(ck)}

    ck2 = Checks()
    comm = ck2.add('120*2/100', 'Factoring commission (₹ lakh)')
    save = ck2.add('120*1/100 + 1.5', 'Savings: bad debts + administration (₹ lakh)')
    net = ck2.add('2.7-2.4', 'Net benefit of factoring before finance effects (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Should we factor?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Annual credit sales ₹120 lakh. A without-recourse factor charges 2% commission and takes over collection. This saves bad debts of 1% of sales and administration cost of ₹1.5 lakh. Ignoring finance charges, is factoring worthwhile?',
          'solution': [table(['Item', '₹ lakh'], [
              ['Commission (2%)', str(comm)],
              ['Savings: bad debts 1.2 + admin 1.5', str(save)],
              ['Net benefit', str(round(net, 2))]], title='Factoring'),
              p('Factoring is marginally beneficial; any advance at an interest cost below the firm\'s cost of funds would add further benefit.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Receivables arise from credit sales; they boost sales and customer relationships but tie up funds and carry risk.',
            'Costs of receivables: capital cost (funds locked), administrative cost (credit checks, collection), collection cost, and default cost (bad debts). Benefits: higher sales and contribution.',
            'The objective is to optimise investment in receivables so that the incremental benefit of extra sales exceeds the incremental costs.'],
          'Credit is a sales tool with a price tag.',
          'Extending credit to a new dealer network can add sales but also overdue risk.'),
        C('c2', T2, [
            'Credit standards decide which customers get credit, using the 5 Cs — character, capacity, capital, collateral and conditions — and sources like bank references, credit rating agencies and trade references.',
            'Credit terms: credit period, cash discount (e.g. "2/10, net 30") and collection policy. Longer credit and laxer standards raise sales and receivables and bad debts; discounts speed collections at a cost.',
            'Evaluation (incremental or total approach): compare contribution gained with added cost of funds on receivables (valued at cost or at sales), bad debts, discounts and collection costs. Adopt the policy with the highest net benefit.'],
          'Change credit only if the extra contribution beats the extra costs.',
          'Offering 2% for payment in 10 days may shrink receivables enough to pay for itself.'),
        C('c3', T3, [
            'Monitoring: days sales outstanding (receivables ÷ average daily credit sales), ageing schedules (buckets like 0–30, 31–60, 61–90, over 90 days), and collection matrix.',
            'Factoring: a factor buys receivables and manages collection; with recourse (firm bears bad debts) or without recourse (factor bears them). Benefits: quicker cash, reduced collection effort; costs: commission and interest on advances. Forfaiting applies to export receivables, typically medium-term and without recourse.',
            'Other tools: securitisation, bill discounting, credit insurance and electronic platforms like TReDS for MSME receivables.'],
          'Watch the age of receivables, not just the total.',
          'A rise in the "over 90 days" bucket is an early warning of bad debts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Collections review', 'role': 'Finance analyst trainee',
             'situation': 'DSO has risen from 45 to 70 days.',
             'steps': ['Prepare an ageing schedule.', 'Identify customers responsible for overdue amounts.', 'Review credit limits and terms.', 'Consider discounts or factoring for slow payers.'],
             'takeaway': 'A few large overdue accounts usually explain a rising DSO.'}]

    mcqs = [
        Q('m1', 'Which is NOT one of the 5 Cs of credit?', ['Competition', 'Character', 'Capacity', 'Collateral'], 0,
          'The 5 Cs are character, capacity, capital, collateral and conditions. In practice: use credit reports.', 'c2', T2),
        Q('m2', 'Credit terms "2/10, net 30" mean:', ['2% discount if paid in 10 days; otherwise full amount in 30 days', '10% discount in 2 days', '2% interest after 30 days', 'Pay in 10 or 30 instalments'], 0,
          'The discount rewards early payment within 10 days; the net amount is due in 30. In practice: cost of forgoing is high.', 'c2', T2),
        Q('m3', 'Annual credit sales ₹36 lakh; receivables ₹6 lakh; 360 days. DSO:', ['60 days', '30 days', '90 days', '45 days'], 0,
          '6 ÷ (36 ÷ 360) = 6 ÷ 0.1 = 60 days. In practice: compare with credit terms.', 'c3', T3, check=60),
        Q('m4', 'In factoring without recourse, bad debts are borne by:', ['The factor', 'The seller', 'The customer\'s bank', 'Shared equally'], 0,
          'Without recourse the factor takes the credit risk, charging more. In practice: with recourse the seller bears it.', 'c3', T3),
        Q('m5', 'Extending the credit period usually:', ['Increases sales and receivables', 'Reduces bad debts', 'Reduces receivables', 'Has no effect'], 0,
          'More generous terms attract sales but lengthen collection. In practice: evaluate incremental costs.', 'c2', T2),
        Q('m6', 'An ageing schedule shows:', ['Receivables classified by how long they have been outstanding', 'Customers by age', 'Stock by age', 'Creditors by size'], 0,
          'It highlights overdue amounts. In practice: prepare monthly.', 'c3', T3),
        Q('m7', 'Cost of funds on receivables (₹40 lakh sales, 45 days, variable cost 75%, return 12%, 360 days):', ['₹45,000', '₹60,000', '₹5,00,000', '₹3,75,000'], 0,
          'Receivables at cost = 40 × 0.75 × 45/360 = ₹3.75 lakh × 12% = ₹45,000. In practice: state the valuation basis.', 'c2', T2, 'moderate', check=45000),
        Q('m8', 'Forfaiting is mainly used for:', ['Export receivables', 'Domestic retail sales', 'Payables', 'Inventory'], 0,
          'Forfaiting buys export receivables, usually without recourse. In practice: often backed by bank guarantees.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Contribution', 1, 'computation', 'contribution'), S('s2', 'Cost of receivables', 2, 'computation', 'receivables'),
           S('s3', 'Bad debts', 1, 'computation', 'bad'), S('s4', 'Decision', 2, 'computation', 'net', nums=[cur, prop])],
          ['State the valuation basis.'], ['Valuing receivables at sales when cost is asked.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Commission', 1, 'computation', 'commission', nums=[comm]), S('s2', 'Savings and net', 2, 'computation', 'saving', nums=[save, net])],
          ['List savings separately.'], ['Ignoring admin savings.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the costs of holding receivables?', 'Capital cost of funds tied up, administration and collection costs, and losses from bad debts.',
          [P('p1', 'Capital cost', 5, 'capital|funds'), P('p2', 'Collection or bad debts', 5, 'collection|bad debt')], 'c1'),
        V('v2', 'How is a change in credit policy evaluated?', 'By comparing the incremental contribution with incremental costs of funds on receivables, bad debts, discounts and collection.',
          [P('p1', 'Incremental contribution', 5, 'contribution'), P('p2', 'Incremental costs', 5, 'cost|bad debt')], 'c2'),
        V('v3', 'What is DSO?', 'Days sales outstanding: receivables divided by average daily credit sales, showing how long customers take to pay.',
          [P('p1', 'Formula', 5, 'divided|daily'), P('p2', 'Meaning', 5, 'how long|days')], 'c3'),
        V('v4', 'Distinguish factoring with and without recourse.', 'With recourse the seller bears bad debts; without recourse the factor bears them.',
          [P('p1', 'With recourse', 5, 'with recourse'), P('p2', 'Without recourse', 5, 'without recourse')], 'c3'),
        V('v5', 'What is TReDS?', 'An electronic platform where invoices of MSME suppliers on large buyers are discounted by financiers.',
          [P('p1', 'Platform', 5, 'platform|electronic'), P('p2', 'MSME invoices', 5, 'msme|invoice')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Textiles', 'difficulty': 'moderate',
              'case': 'Delta Textiles has credit sales of ₹72 lakh a year (360 days) and receivables of ₹18 lakh. It considers offering "2/10, net 45"; 50% of customers would take the discount, cutting DSO to 25 days.',
              'mcqs': [
                  M('k1a', 'Current DSO:', ['90 days', '60 days', '45 days', '30 days'], 0,
                    '18 ÷ (72 ÷ 360) = 18 ÷ 0.2 = 90 days. In practice: far above terms.', 'core', check=90, topic=T3),
                  M('k1b', 'New receivables at 25 days DSO (₹ lakh):', ['5', '18', '7.2', '3.6'], 0,
                    '72 ÷ 360 × 25 = 5. In practice: frees ₹13 lakh.', 'moderate', check=5, topic=T3),
                  M('k1c', 'Annual discount cost (₹ lakh):', ['0.72', '1.44', '0.36', '2.16'], 0,
                    '50% × 72 × 2% = 0.72. In practice: compare with interest saved.', 'moderate', check=0.72, topic=T2),
                  M('k1d', 'At a 12% cost of funds, interest saved on ₹13 lakh released (₹ lakh):', ['1.56', '0.72', '2.16', '1.08'], 0,
                    '13 × 12% = 1.56 > 0.72 discount cost — the discount pays. In practice: also check bad debt effects.', 'moderate', check=1.56, topic=T2),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 4, 'Management of Receivables',
                ['Explain the costs and benefits of receivables.',
                 'Evaluate credit standards, terms and policy changes.',
                 'Monitor receivables and evaluate factoring.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 40}, 'prereq': ['int-p6-a-ch09-u03'],
                 'exam_tip': 'Use a columnar statement for each policy; compare net benefit, not just sales.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Costs: capital, admin, collection, bad debts.',
                             '5 Cs; credit terms; incremental evaluation.',
                             'DSO, ageing schedule.',
                             'Factoring with/without recourse; forfaiting; TReDS.'],
                 'remember': ['Receivables at cost exclude profit.'],
                 'traps': ['Contribution, not sales, is the benefit of extra credit.']},
                [('DSO', 'Receivables ÷ daily credit sales'), ('Policy test', 'ΔContribution > ΔCosts'), ('Without recourse', 'Factor bears risk')],
                viva, cases)
