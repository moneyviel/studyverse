"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 15 Budgets and Budgetary Control.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch15-u01'
T1 = 'Budgets, budgetary control and the budget process'
T2 = 'Functional budgets'
T3 = 'Fixed and flexible budgets; budget ratios'
T4 = 'Zero-based and performance budgeting'


def build():
    ck = Checks()
    prod = ck.add('12000+2500-2000', 'Production budget (units)')
    mreq = ck.add('12500*3', 'Material required (kg)')
    purch = ck.add('37500+6000-5000', 'Material purchases (kg)')
    pval = ck.add('38500*20', 'Material purchases (₹)')
    i1 = {'id': 'i1', 'title': 'From sales to purchases', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Budgeted sales 12,000 units. Finished goods: opening 2,000, desired closing 2,500. Each unit needs 3 kg of material at ₹20/kg; material stock: opening 5,000 kg, desired closing 6,000 kg. Prepare the production budget and the material purchase budget.',
          'solution': [table(['Budget', 'Working', 'Answer'], [
              ['Production (units)', 'Sales 12,000 + closing 2,500 − opening 2,000', inr(prod)],
              ['Material required (kg)', '12,500 × 3', inr(mreq)],
              ['Material purchases (kg)', '37,500 + closing 6,000 − opening 5,000', inr(purch)],
              ['Material purchases (₹)', '38,500 × 20', inr(pval)]], title='Functional budgets')],
          'checks': list(ck)}

    ck2 = Checks()
    t80 = ck2.add('8000*50 + 40000 + 60000*0.8 + 200000', 'Total cost at 80%')
    t60 = ck2.add('6000*50 + 40000 + 60000*0.6 + 200000', 'Total cost at 60%')
    u80 = ck2.add('688000/8000', 'Cost per unit at 80%')
    u60 = ck2.add('576000/6000', 'Cost per unit at 60%')
    i2 = {'id': 'i2', 'title': 'Flexing the budget', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'At 100% capacity (10,000 units): variable cost ₹50/unit; semi-variable overheads ₹1,00,000 (40% fixed); fixed overheads ₹2,00,000. Prepare a flexible budget at 60% and 80% capacity, with cost per unit.',
          'solution': [table(['Item', '60% (6,000 units) ₹', '80% (8,000 units) ₹'], [
              ['Variable cost @ ₹50', inr(300000), inr(400000)],
              ['Semi-variable: fixed part', inr(40000), inr(40000)],
              ['Semi-variable: variable part (₹6 a unit)', inr(36000), inr(48000)],
              ['Fixed overheads', inr(200000), inr(200000)],
              ['Total', inr(t60), inr(t80)],
              ['Cost per unit', inr(u60), inr(u80)]], title='Flexible budget'),
              note('Cost per unit falls as volume rises because fixed costs are spread over more units.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A budget is a quantitative plan, prepared in advance for a defined period, of income, expenditure and resources needed to achieve objectives. Budgetary control sets budgets for responsibility centres, compares actuals continuously and acts on deviations.',
            'The process: set objectives; identify the principal budget factor (key factor) that limits activity — often sales, sometimes materials, labour or capacity; prepare functional budgets in sequence; consolidate into the master budget; monitor and revise.',
            'Organisation: a budget committee coordinates, a budget officer manages, and a budget manual sets procedures. Benefits: planning, coordination, control and motivation; limitations: estimates may be inaccurate, rigidity, and cost of the system.'],
          'A budget is a plan in numbers; budgetary control is using it to steer.',
          'If a factory can sell more than it can make, capacity — not sales — is the principal budget factor.'),
        C('c2', T2, [
            'Sales budget (quantity and value by product and region) leads to the production budget: production = sales + closing finished stock − opening finished stock.',
            'Materials: requirement = production × usage per unit; purchases = requirement + closing material stock − opening material stock. Labour budget = production × hours per unit × rate. Overhead budgets for production, administration, selling.',
            'The cash budget lists expected receipts and payments month by month to show surpluses or shortages; it excludes non-cash items like depreciation. All functional budgets feed the master budget (budgeted P&L and balance sheet).'],
          'Each budget is built from the one before, starting from sales.',
          'Selling 5,000 units with stock rising by 500 means producing 5,500 units.'),
        C('c3', T3, [
            'A fixed budget is set for one level of activity; it is fine where activity is stable but misleading for control when actual output differs.',
            'A flexible budget adjusts costs to the actual level of activity by separating fixed, variable and semi-variable costs; it allows like-for-like comparison.',
            'Ratios: efficiency ratio = standard hours for actual output ÷ actual hours × 100; activity ratio = standard hours for actual output ÷ budgeted hours × 100; capacity ratio = actual hours ÷ budgeted hours × 100. Activity = efficiency × capacity. The calendar ratio compares available working days with budgeted days.'],
          'Compare actual cost with what cost should have been at the actual level, not at the planned level.',
          'Budgeted 10,000 hours; worked 9,000; standard hours for output 9,900: efficiency 110%, capacity 90%, activity 99%.'),
        C('c4', T4, [
            'Zero-based budgeting (ZBB) builds every budget from zero each period: each activity is identified as a decision package, evaluated on cost and benefit, ranked and funded by priority — rather than adding a percentage to last year\'s figure.',
            'ZBB avoids carrying forward inefficiency but is time-consuming; it suits service and support functions and Government programmes.',
            'Performance budgeting links spending with physical outputs and results (programmes, activities, targets) — widely used in the public sector; outcome budgeting goes further to measure results achieved.'],
          'ZBB asks "why spend at all?", not "how much more than last year?".',
          'A training department under ZBB must justify each programme instead of receiving last year\'s budget plus 10%.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Cash budget for a festive season', 'role': 'Cost accountant trainee',
             'situation': 'A retailer expects heavy purchases in September and collections in November.',
             'steps': ['Estimate monthly sales and collection pattern.', 'Estimate purchases and payment terms.', 'List other cash payments.', 'Identify months needing borrowing.'],
             'takeaway': 'Profitable businesses can still run out of cash — the cash budget shows when.'}]

    mcqs = [
        Q('m1', 'The principal budget factor is:', ['The factor that limits the organisation\'s activity', 'The largest expense', 'The budget officer', 'The cash balance'], 0,
          'Also called key or limiting factor; often sales, but may be materials, labour or capacity. In practice: identify it first.', 'c1', T1),
        Q('m2', 'Sales 10,000 units; opening FG 1,500; closing FG 1,000. Production:', ['9,500 units', '10,500 units', '11,500 units', '8,500 units'], 0,
          '10,000 + 1,000 − 1,500 = 9,500. In practice: stock reduction lowers production.', 'c2', T2, check=9500),
        Q('m3', 'A cash budget does NOT include:', ['Depreciation', 'Collections from debtors', 'Payment of wages', 'Purchase of a machine'], 0,
          'Depreciation is non-cash. In practice: capital purchases do appear when paid.', 'c2', T2),
        Q('m4', 'A flexible budget is useful because it:', ['Adjusts costs to the actual level of activity', 'Is set for one level only', 'Ignores fixed costs', 'Needs no cost classification'], 0,
          'It compares actual cost with allowed cost for the same activity. In practice: it needs fixed/variable split.', 'c3', T3),
        Q('m5', 'Standard hours for actual output 4,400; actual hours 4,000. Efficiency ratio:', ['110%', '90.9%', '100%', '88%'], 0,
          '4,400 ÷ 4,000 × 100 = 110%. In practice: above 100% means better than standard.', 'c3', T3, check=110),
        Q('m6', 'Activity ratio equals:', ['Efficiency ratio × capacity ratio', 'Capacity ratio ÷ efficiency ratio', 'Efficiency + capacity', 'Calendar ratio'], 0,
          'Activity = (SH/BH) = (SH/AH) × (AH/BH). In practice: use to check workings.', 'c3', T3),
        Q('m7', 'Zero-based budgeting:', ['Requires each activity to be justified from zero', 'Adds inflation to last year\'s budget', 'Uses only fixed costs', 'Is the same as a fixed budget'], 0,
          'ZBB evaluates decision packages afresh. In practice: costly but sharpens spending.', 'c4', T4),
        Q('m8', 'Semi-variable cost ₹80,000 at 100% (25% fixed). At 75% activity it is:', ['₹65,000', '₹60,000', '₹80,000', '₹45,000'], 0,
          'Fixed 20,000 + variable 60,000 × 75% = 45,000 → total 65,000. In practice: split semi-variable costs first.', 'c3', T3, 'moderate', check=65000),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Production', 1, 'computation', 'production', nums=[prod]), S('s2', 'Material required', 1, 'computation', 'required', nums=[mreq]),
           S('s3', 'Purchases', 2, 'computation', 'purchases', nums=[purch, pval])],
          ['Show stock adjustments.'], ['Reversing opening and closing stock.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Split semi-variable', 2, 'concept', 'semi-variable'), S('s2', 'Totals', 2, 'computation', 'total', nums=[t60, t80]), S('s3', 'Per unit', 2, 'computation', 'per unit', nums=[u60, u80])],
          ['Keep fixed costs constant.'], ['Flexing fixed costs.'], ['Columnar budget.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is budgetary control?', 'Setting budgets for responsibility centres, comparing actual results with them continuously and taking corrective action on deviations.',
          [P('p1', 'Compare', 5, 'compar'), P('p2', 'Corrective action', 5, 'correct|action')], 'c1'),
        V('v2', 'How is the production budget derived?', 'Budgeted sales plus desired closing finished stock minus opening finished stock.',
          [P('p1', 'Sales', 4, 'sales'), P('p2', 'Stock adjustment', 6, 'closing|opening')], 'c2'),
        V('v3', 'Why is a flexible budget better for control?', 'Because it shows the cost allowed at the actual level of activity, so variances reflect efficiency rather than volume changes.',
          [P('p1', 'Actual level', 6, 'actual level|activity'), P('p2', 'Fair comparison', 4, 'efficiency|variance')], 'c3'),
        V('v4', 'Define capacity ratio.', 'Actual hours worked divided by budgeted hours, expressed as a percentage.',
          [P('p1', 'Actual hours', 5, 'actual hours'), P('p2', 'Budgeted hours', 5, 'budgeted')], 'c3'),
        V('v5', 'What is a decision package in ZBB?', 'A description of an activity with its costs, benefits and alternatives, used to rank and fund activities from zero.',
          [P('p1', 'Activity with cost and benefit', 6, 'cost|benefit'), P('p2', 'Ranking', 4, 'rank')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Shine Detergents', 'difficulty': 'moderate',
              'case': 'Shine Detergents budgets for Q1: sales Jan 8,000, Feb 10,000, Mar 12,000 packs at ₹50. Customers pay 60% in the month of sale and 40% next month (December sales ₹3,00,000). Closing stock of finished goods is to be 20% of next month\'s sales; opening stock on 1 January is 1,600 packs.',
              'mcqs': [
                  M('k1a', 'January production:', ['8,400 packs', '8,000 packs', '9,600 packs', '7,600 packs'], 0,
                    'Sales 8,000 + closing 2,000 (20% of 10,000) − opening 1,600 = 8,400. In practice: link months.', 'moderate', check=8400, topic=T2),
                  M('k1b', 'January cash collections:', ['₹3,60,000', '₹4,00,000', '₹2,40,000', '₹5,40,000'], 0,
                    '60% × 4,00,000 = 2,40,000 + 40% × 3,00,000 = 1,20,000 → 3,60,000. In practice: track debtor ageing.', 'moderate', check=360000, topic=T2),
                  M('k1c', 'February collections:', ['₹4,60,000', '₹5,00,000', '₹4,00,000', '₹3,00,000'], 0,
                    '60% × 5,00,000 + 40% × 4,00,000 = 3,00,000 + 1,60,000 = 4,60,000. In practice: lag creates working capital need.', 'moderate', check=460000, topic=T2),
                  M('k1d', 'If actual sales differ from budget, the best control tool is:', ['A flexible budget', 'A fixed budget', 'A cash budget only', 'No budget'], 0,
                    'Flexible budgets restate allowed costs at actual volume. In practice: revise monthly.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch15', 1, 'Budgets and Budgetary Control',
                ['Explain budgets, budgetary control and the budget process.',
                 'Prepare functional and cash budgets.',
                 'Prepare flexible budgets and compute budget ratios.',
                 'Explain zero-based and performance budgeting.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 50}, 'prereq': ['int-p4-ch14-u01'],
                 'exam_tip': 'Start every budget question with the principal budget factor and the sequence of budgets.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Principal budget factor drives the sequence.',
                             'Production = sales + closing FG − opening FG; purchases = usage + closing − opening material.',
                             'Cash budget: cash items only.',
                             'Flexible budget: split fixed, variable, semi-variable.',
                             'Efficiency = SH/AH; capacity = AH/BH; activity = SH/BH.'],
                 'remember': ['Activity = efficiency × capacity.'],
                 'traps': ['Depreciation never appears in a cash budget.']},
                [('Efficiency ratio', 'SH ÷ AH'), ('Capacity ratio', 'AH ÷ BH'), ('Activity ratio', 'SH ÷ BH'), ('Production', 'Sales + CS − OS')],
                viva, cases)
