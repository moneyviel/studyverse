"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 14 Marginal Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch14-u01'
T1 = 'Marginal costing and contribution'
T2 = 'Cost-volume-profit analysis'
T3 = 'Decisions using marginal costing'
T4 = 'Absorption versus marginal costing'


def build():
    ck = Checks()
    pv = ck.add('(100-60)/100*100', 'P/V ratio %')
    bep = ck.add('400000/40', 'Break-even units')
    profit = ck.add('15000*40-400000', 'Profit at 15,000 units')
    mos = ck.add('(15000-10000)/15000*100', 'Margin of safety %')
    tgt = ck.add('(400000+300000)/40', 'Units for profit of ₹3,00,000')
    i1 = {'id': 'i1', 'title': 'Break-even and beyond', 'difficulty': 'core', 'minutes': 9,
          'q': 'A product sells at ₹100; variable cost ₹60; fixed costs ₹4,00,000 a year; current sales 15,000 units. Compute P/V ratio, break-even units and sales, profit, margin of safety, and units needed for a profit of ₹3,00,000.',
          'solution': [table(['Measure', 'Working', 'Answer'], [
              ['Contribution per unit', '100 − 60', '₹40'],
              ['P/V ratio', '40 ÷ 100', str(int(pv)) + '%'],
              ['Break-even units', '4,00,000 ÷ 40', inr(bep)],
              ['Break-even sales', '10,000 × 100', '₹' + inr(1000000)],
              ['Profit', '15,000 × 40 − 4,00,000', '₹' + inr(profit)],
              ['Margin of safety', '(15,000 − 10,000) ÷ 15,000', str(round(mos, 2)) + '%'],
              ['Units for ₹3,00,000 profit', '(4,00,000 + 3,00,000) ÷ 40', inr(tgt)]], title='CVP analysis'),
              note('Check: profit = margin of safety sales × P/V ratio = ₹5,00,000 × 40% = ₹2,00,000.')],
          'checks': list(ck)}

    ck2 = Checks()
    cpb = ck2.add('50/2', 'Contribution per hour — B')
    cpa = ck2.add('60/4', 'Contribution per hour — A')
    tot = ck2.add('3000*50 + (10000-6000)/4*60', 'Maximum contribution')
    i2 = {'id': 'i2', 'title': 'Too few machine hours', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Machine hours are limited to 10,000. Product A: contribution ₹60/unit, 4 hours/unit, demand 2,000 units. Product B: contribution ₹50/unit, 2 hours/unit, demand 3,000 units. Find the best product mix and contribution.',
          'solution': [table(['Step', 'A', 'B'], [
              ['Contribution per machine hour', '₹' + inr(cpa), '₹' + inr(cpb)],
              ['Rank', 'II', 'I'],
              ['Units made', '1,000 (4,000 hours left ÷ 4)', '3,000 (6,000 hours)'],
              ['Contribution', '₹60,000', '₹1,50,000']], title='Key factor'),
              p('Total contribution ₹' + inr(tot) + '. Ranking by contribution per unit (A first) would give less.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Marginal costing charges only variable costs to products; fixed costs are treated as period costs and written off in full against contribution.',
            'Contribution = sales − variable cost; it first covers fixed costs and then gives profit. Profit = contribution − fixed costs.',
            'Marginal cost is the change in total cost from producing one more unit; in practice it equals variable cost per unit. Stocks are valued at variable cost under marginal costing.'],
          'Each unit sold adds its contribution to a pot that pays fixed costs first and then becomes profit.',
          'If a pen sells for ₹20 with variable cost ₹12, each pen contributes ₹8 towards fixed costs.'),
        C('c2', T2, [
            'P/V ratio = contribution ÷ sales × 100; it also equals change in profit ÷ change in sales.',
            'Break-even point (units) = fixed cost ÷ contribution per unit; (sales) = fixed cost ÷ P/V ratio.',
            'Margin of safety = actual sales − break-even sales; profit = margin of safety × P/V ratio. Sales for a target profit = (fixed cost + target profit) ÷ P/V ratio.',
            'Assumptions: costs divide cleanly into fixed and variable; selling price and variable cost per unit are constant; one product or a constant mix; no change in stock levels. A break-even chart and a profit-volume graph show these relations visually; the angle of incidence reflects the profit-earning rate.'],
          'CVP answers "how much must we sell" questions with three numbers: fixed cost, contribution and sales.',
          'Two periods with sales ₹10 lakh and ₹12 lakh and profits ₹1 lakh and ₹1.6 lakh give P/V ratio 30%.'),
        C('c3', T3, [
            'Key (limiting) factor: when a resource is scarce, rank products by contribution per unit of that factor, not by contribution per unit.',
            'Make or buy: buy if the purchase price is less than the variable cost of making (plus any avoidable fixed cost), considering capacity use.',
            'Accept a special order below normal price if it covers variable cost, does not displace regular sales and spare capacity exists. Shut down temporarily if contribution does not cover avoidable fixed costs (shutdown point = avoidable fixed cost ÷ contribution per unit).',
            'Other uses: pricing in recession, choosing between alternatives, and evaluating discounts.'],
          'Short-term decisions turn on contribution, because fixed costs often stay unchanged.',
          'An order at ₹70 for a product with variable cost ₹60 adds ₹10 per unit if there is idle capacity.'),
        C('c4', T4, [
            'Absorption costing includes fixed production overheads in product cost and stock; marginal costing does not.',
            'When production exceeds sales (stock increases), absorption profit is higher, because part of fixed overhead is carried in closing stock; when sales exceed production, marginal profit is higher; when equal, both profits match.',
            'Difference in profit = change in stock units × fixed overhead per unit.'],
          'The two methods differ only in when fixed production overhead hits profit.',
          'Producing 10,000 and selling 8,000 with fixed overhead of ₹20 a unit makes absorption profit ₹40,000 higher.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Special order evaluation', 'role': 'Cost accountant trainee',
             'situation': 'An export buyer offers ₹75 per unit for 5,000 units; normal price ₹100, variable cost ₹62.',
             'steps': ['Check spare capacity.', 'Compute extra contribution: 5,000 × (75 − 62).', 'Identify any extra fixed costs.', 'Consider effect on domestic prices.'],
             'takeaway': 'With spare capacity, any price above variable cost adds profit.'}]

    mcqs = [
        Q('m1', 'Contribution is:', ['Sales minus variable cost', 'Sales minus total cost', 'Fixed cost plus variable cost', 'Profit minus fixed cost'], 0,
          'Contribution covers fixed costs and then gives profit. In practice: compute per unit and in total.', 'c1', T1),
        Q('m2', 'Fixed cost ₹3,00,000; P/V ratio 25%. Break-even sales:', ['₹12,00,000', '₹7,50,000', '₹75,000', '₹4,00,000'], 0,
          '3,00,000 ÷ 25% = 12,00,000. In practice: use for sales targets.', 'c2', T2, check=1200000),
        Q('m3', 'Sales ₹8,00,000; profit ₹80,000; P/V ratio 40%. Margin of safety:', ['₹2,00,000', '₹3,20,000', '₹80,000', '₹6,00,000'], 0,
          'MOS = profit ÷ P/V = 80,000 ÷ 40% = 2,00,000. In practice: 25% of sales.', 'c2', T2, 'moderate', check=200000),
        Q('m4', 'Sales ₹5 lakh, profit ₹50,000; sales ₹7 lakh, profit ₹1,10,000. P/V ratio:', ['30%', '20%', '15%', '25%'], 0,
          'Change in profit 60,000 ÷ change in sales 2,00,000 = 30%. In practice: fixed cost = 1,50,000 − 50,000 = 1,00,000.', 'c2', T2, 'moderate', check=30),
        Q('m5', 'With a scarce resource, products are ranked by:', ['Contribution per unit of the scarce resource', 'Contribution per unit', 'Selling price', 'Profit per unit'], 0,
          'The key factor rule maximises total contribution. In practice: also meet minimum demand commitments.', 'c3', T3),
        Q('m6', 'A component costs ₹45 to buy; variable cost to make ₹40; fixed costs unaffected. Decision:', ['Make', 'Buy', 'Indifferent', 'Shut down'], 0,
          'Making saves ₹5 a unit since fixed costs do not change. In practice: consider capacity for other products.', 'c3', T3),
        Q('m7', 'When closing stock exceeds opening stock, absorption profit is:', ['Higher than marginal profit', 'Lower', 'Equal', 'Zero'], 0,
          'Fixed overhead carried forward in stock reduces absorption costing\'s period charge. In practice: difference = stock change × fixed OH per unit.', 'c4', T4),
        Q('m8', 'Under marginal costing, closing stock is valued at:', ['Variable production cost', 'Total cost', 'Selling price', 'Prime cost only'], 0,
          'Only variable production costs are inventoried. In practice: financial reporting needs absorption cost.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'P/V and BEP', 2, 'computation', 'break-even', nums=[pv, bep]), S('s2', 'Profit', 1, 'computation', 'profit', nums=[profit]),
           S('s3', 'MOS', 1, 'computation', 'margin', nums=[mos]), S('s4', 'Target units', 2, 'computation', 'target|3,00,000', nums=[tgt])],
          ['State formulas.'], ['Dividing fixed cost by selling price.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Per-hour contribution', 2, 'computation', 'per hour', nums=[cpa, cpb]), S('s2', 'Ranking and mix', 2, 'concept', 'rank'), S('s3', 'Total', 1, 'computation', 'total', nums=[tot])],
          ['Rank by key factor.'], ['Ranking by contribution per unit.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is marginal costing?', 'A technique that charges only variable costs to products and treats fixed costs as period costs written off against contribution.',
          [P('p1', 'Variable to products', 5, 'variable'), P('p2', 'Fixed as period cost', 5, 'period|fixed')], 'c1'),
        V('v2', 'How is the break-even point found?', 'By dividing fixed costs by contribution per unit for units, or by the P/V ratio for sales value.',
          [P('p1', 'Fixed costs', 5, 'fixed'), P('p2', 'Contribution or P/V', 5, 'contribution|p/v')], 'c2'),
        V('v3', 'What is margin of safety?', 'The excess of actual or budgeted sales over break-even sales; profit equals margin of safety times P/V ratio.',
          [P('p1', 'Excess over BEP', 6, 'excess|break-even'), P('p2', 'Profit link', 4, 'profit')], 'c2'),
        V('v4', 'What is a key factor?', 'A resource in short supply that limits output, such as machine hours or materials, used to rank products by contribution per unit of it.',
          [P('p1', 'Limiting resource', 5, 'limit|short'), P('p2', 'Ranking', 5, 'rank|per unit')], 'c3'),
        V('v5', 'Why do absorption and marginal profits differ?', 'Because absorption costing carries fixed production overhead in stock, so profit differs by the change in stock times fixed overhead per unit.',
          [P('p1', 'Fixed OH in stock', 6, 'stock'), P('p2', 'Formula', 4, 'change|per unit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Bright Lamps', 'difficulty': 'moderate',
              'case': 'Bright Lamps: price ₹500, variable cost ₹300 per lamp, fixed costs ₹6,00,000. Expected sales 4,500 lamps. A retailer offers to buy 500 extra lamps at ₹350; capacity is 6,000 lamps.',
              'mcqs': [
                  M('k1a', 'Break-even lamps:', ['3,000', '2,000', '4,500', '1,200'], 0,
                    '6,00,000 ÷ 200 = 3,000. In practice: sales of 4,500 give comfortable cover.', 'core', check=3000, topic=T2),
                  M('k1b', 'Expected profit:', ['₹3,00,000', '₹9,00,000', '₹6,00,000', '₹1,50,000'], 0,
                    '4,500 × 200 − 6,00,000 = 3,00,000. In practice: MOS 1,500 lamps.', 'core', check=300000, topic=T2),
                  M('k1c', 'Extra profit from the special order:', ['₹25,000', '₹1,75,000', 'A loss of ₹75,000', '₹50,000'], 0,
                    '500 × (350 − 300) = 25,000 with spare capacity and no extra fixed cost. In practice: protect regular prices.', 'moderate', check=25000, topic=T3),
                  M('k1d', 'Margin of safety ratio at expected sales:', ['33.33%', '50%', '25%', '66.67%'], 0,
                    '(4,500 − 3,000) ÷ 4,500 = 33.33%. In practice: higher is safer.', 'core', check=33.33, topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch14', 1, 'Marginal Costing',
                ['Explain marginal costing and contribution.',
                 'Apply CVP analysis: P/V ratio, break-even, margin of safety and target profit.',
                 'Use marginal costing for key factor and other short-term decisions.',
                 'Reconcile absorption and marginal costing profits.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 50}, 'prereq': ['int-p4-ch13-u01'],
                 'exam_tip': 'If two periods\' sales and profits are given, find P/V ratio from the changes first; everything else follows.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Contribution = sales − variable cost; profit = contribution − fixed cost.',
                             'P/V = C/S; BEP = F ÷ C per unit or F ÷ P/V.',
                             'MOS = sales − BEP sales; profit = MOS × P/V.',
                             'Key factor: rank by contribution per unit of scarce resource.',
                             'Absorption vs marginal: stock change × fixed OH per unit.'],
                 'remember': ['P/V = Δprofit ÷ Δsales.'],
                 'traps': ['Do not rank by contribution per unit when a resource is limited.']},
                [('BEP units', 'F ÷ C per unit'), ('BEP sales', 'F ÷ P/V'), ('Target sales', '(F + P) ÷ P/V'), ('Profit', 'MOS × P/V')],
                viva, cases)
