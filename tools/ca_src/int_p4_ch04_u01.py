"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 4 Overheads – Absorption Costing Method.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch04-u01'
T1 = 'Meaning and classification of overheads'
T2 = 'Collection, allocation and apportionment (primary distribution)'
T3 = 'Re-apportionment of service department costs (secondary distribution)'
T4 = 'Methods of absorbing overheads; machine hour rate'
T5 = 'Types of overhead rates'
T6 = 'Under- and over-absorption'
T7 = 'Administrative, selling and distribution overheads'
T8 = 'Capacity concepts and special items'


def build():
    # i1 — secondary distribution by simultaneous equations
    ck = Checks()
    s1 = ck.add('round(116000/0.96,2)', 'S1 = 1,00,000 + 0.20 S2 and S2 = 80,000 + 0.20 S1 → S1')
    s2 = ck.add('round(80000+0.2*120833.33,2)', 'S2')
    p1 = ck.add('round(400000+0.4*120833.33+0.5*104166.67,2)', 'Total overhead of P1')
    p2 = ck.add('round(300000+0.4*120833.33+0.3*104166.67,2)', 'Total overhead of P2')
    tot = ck.add('round(500416.67+379583.33,2)', 'Check: total equals 8,80,000')
    i1 = {'id': 'i1', 'title': 'Two service departments that serve each other', 'difficulty': 'hard', 'minutes': 12,
          'q': 'After primary distribution, Vindhya Castings has overheads: production departments P1 ₹4,00,000 and P2 ₹3,00,000; service departments S1 (maintenance) ₹1,00,000 and S2 (stores) ₹80,000. S1 serves P1 40%, P2 40%, S2 20%. S2 serves P1 50%, P2 30%, S1 20%. Re-apportion service costs by the simultaneous equation method.',
          'solution': [p('Let S1 and S2 be the total costs after receiving each other\'s share: S1 = 1,00,000 + 0.20 S2; S2 = 80,000 + 0.20 S1. Substituting: S1 = 1,00,000 + 16,000 + 0.04 S1, so 0.96 S1 = 1,16,000.'),
                       table(['Item', 'Working', '₹'], [
                           ['S1', '1,16,000 ÷ 0.96', inr(s1)],
                           ['S2', '80,000 + 0.20 × S1', inr(s2)],
                           ['P1', '4,00,000 + 40% S1 + 50% S2', inr(p1)],
                           ['P2', '3,00,000 + 40% S1 + 30% S2', inr(p2)],
                           ['Total (unchanged)', 'P1 + P2', inr(tot)]], title='Secondary distribution'),
                       note('The repeated distribution and trial-and-error methods reach the same totals; the direct method would ignore the services S1 and S2 give each other.')],
          'checks': list(ck)}

    # i2 — machine hour rate
    ck2 = Checks()
    stand = ck2.add('(24000+60000+0.01*1200000)/2000', 'Standing charges per hour')
    dep = ck2.add('(1200000-200000)/10/2000', 'Depreciation per hour')
    rep = ck2.add('40000/2000', 'Repairs per hour')
    power = ck2.add('15*8', 'Power per hour')
    mhr = ck2.add('48+50+20+120', 'Machine hour rate')
    i2 = {'id': 'i2', 'title': 'Building a machine hour rate', 'difficulty': 'core', 'minutes': 8,
          'q': 'A CNC machine costs ₹12,00,000, scrap value ₹2,00,000, life 10 years, working 2,000 hours a year. It uses 15 units of power an hour at ₹8. Annual repairs ₹40,000; share of rent ₹24,000; share of supervisor\'s salary ₹60,000; insurance 1% of cost. Compute the machine hour rate.',
          'solution': [table(['Item', 'Working', '₹ per hour'], [
              ['Standing charges', '(24,000 + 60,000 + 12,000) ÷ 2,000', inr(stand)],
              ['Depreciation', '(12,00,000 – 2,00,000) ÷ 10 ÷ 2,000', inr(dep)],
              ['Repairs', '40,000 ÷ 2,000', inr(rep)],
              ['Power', '15 × 8', inr(power)],
              ['Machine hour rate', '', inr(mhr)]], title='Machine hour rate'),
              note('Standing charges accrue whether or not the machine runs; machine expenses (depreciation, repairs, power) vary with running hours.')],
          'checks': list(ck2)}

    # i3 — under-absorption and supplementary rate
    ck3 = Checks()
    rate = ck3.add('1200000/60000', 'Pre-determined rate per labour hour')
    absd = ck3.add('62000*20', 'Overheads absorbed')
    under = ck3.add('1320000-1240000', 'Under-absorbed overheads')
    normal = ck3.add('80000-20000', 'Normal part to be spread by supplementary rate')
    wip = ck3.add('60000*0.10', 'Share of work-in-progress (10%)')
    fg = ck3.add('60000*0.20', 'Share of finished goods (20%)')
    cogs = ck3.add('60000*0.70', 'Share of cost of sales (70%)')
    i3 = {'id': 'i3', 'title': 'Disposing of under-absorbed overheads', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Budgeted overheads ₹12,00,000 for 60,000 labour hours. Actual overheads ₹13,20,000; actual hours 62,000. ₹20,000 of the actual overheads relates to idle time caused by a strike. Overheads absorbed are lying 10% in work-in-progress, 20% in finished goods and 70% in cost of sales. Compute and dispose of the under-absorption.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Pre-determined rate', '12,00,000 ÷ 60,000', inr(rate) + ' per hour'],
              ['Absorbed', '62,000 × 20', inr(absd)],
              ['Under-absorbed', '13,20,000 – 12,40,000', inr(under)],
              ['Abnormal (strike) → costing P&L', '', inr(20000)],
              ['Normal balance → supplementary rate', '', inr(normal)],
              ['To work-in-progress', '10%', inr(wip)],
              ['To finished goods', '20%', inr(fg)],
              ['To cost of sales', '70%', inr(cogs)]], title='Disposal'),
              note('Abnormal amounts are never loaded on products; normal under-absorption is spread over the units still in stock and those sold.')],
          'checks': list(ck3)}

    cls = table(['Basis', 'Classes'], [
        ['Function', 'Factory (production), administration, selling, distribution, research and development'],
        ['Behaviour', 'Fixed, variable, semi-variable (split by high-low or similar methods)'],
        ['Controllability', 'Controllable and uncontrollable at a given level of management'],
        ['Normality', 'Normal (part of cost) and abnormal (to costing P&L)'],
        ['Element', 'Indirect materials, indirect employee cost, indirect expenses']], title='Classification of overheads')
    rates = table(['Rate', 'Meaning'], [
        ['Actual rate', 'Actual overheads ÷ actual base, known only after the period — too late for pricing'],
        ['Pre-determined rate', 'Budgeted overheads ÷ budgeted base; used through the year'],
        ['Blanket rate', 'One rate for the whole factory — suits a single product or uniform departments'],
        ['Departmental rate', 'Separate rate for each production department — more accurate'],
        ['Normal rate', 'Based on normal capacity, so idle-capacity cost stays out of product cost'],
        ['Supplementary rate', 'Extra (or negative) rate to adjust normal under- or over-absorption']], title='Overhead rates')

    concepts = [
        C('c1', T1, [
            'Overheads are indirect costs — materials, employee cost and expenses that cannot be traced to a cost object economically.',
            'Classified by function, behaviour, controllability, normality and element (table). Separating fixed and variable parts helps in budgeting, marginal costing and control.'],
          'Overheads are the rent, power and supervision that every product shares but none owns.',
          'Factory canteen costs are indirect employee costs shared by all products.',
          blocks=[cls]),
        C('c2', T2, [
            'Steps: estimate and collect overheads; allocate costs wholly identified with a department (allocation); apportion common costs on a fair basis (apportionment) — the primary distribution.',
            'Typical bases: rent and building costs — floor area; power — HP × hours or meter readings; lighting — number of points or floor area; supervision and canteen — number of employees; insurance on plant — value of plant; material handling — weight or value of material.'],
          'Allocate what clearly belongs to one department; share the rest fairly.',
          'A department occupying 30% of the floor area bears 30% of factory rent.'),
        C('c3', T3, [
            'Service department costs are re-apportioned to production departments (secondary distribution) because products pass only through production departments.',
            'Direct redistribution: ignores services between service departments. Step (ladder) method: close service departments one by one, starting with the one serving most others; costs do not flow back.',
            'Reciprocal service methods recognise mutual service: simultaneous equations, repeated distribution, or trial and error. The totals for production departments are the same under all three.'],
          'Service departments are the stage crew; their cost ends up in the price of the show.',
          'Maintenance and stores that serve each other need the reciprocal method for accurate costs.'),
        C('c4', T4, [
            'Absorption charges overheads to products using a rate per unit of a base: percentage of direct material, prime cost or direct labour cost; labour hour rate; machine hour rate; or rate per unit of output.',
            'Choose the base that best reflects how the department incurs overheads — machine hours in machine-intensive departments, labour hours where work is manual, units where output is uniform.',
            'Machine hour rate = (standing charges + machine expenses) ÷ running hours. Standing charges (rent, supervision, insurance) are fixed per period; machine expenses (depreciation, repairs, power) vary with running time.'],
          'The absorption base is the meter that decides how much overhead each job pays.',
          'In an automated press shop, machine hours track power and depreciation far better than wages do.'),
        C('c5', T5, [
            'Rates may be actual or pre-determined, blanket or departmental, normal or supplementary (table). Pre-determined departmental rates based on normal capacity are generally preferred.'],
          'Use a forecast rate during the year; correct for the gap afterwards.',
          'A company quoting for tenders in June needs a pre-determined rate, not one known only in March.',
          blocks=[rates]),
        C('c6', T6, [
            'Under-absorption: overheads absorbed < actual overheads; over-absorption: absorbed > actual. Causes: errors in estimating overheads or base, idle capacity, seasonal swings, changes in methods.',
            'Disposal: (i) supplementary rate charged to stock in process, finished stock and goods sold when the difference is normal and significant; (ii) write off to costing profit and loss account when abnormal or small; (iii) carry forward to the next period in seasonal businesses where it will reverse.'],
          'Correct the bill if the estimate was off; send the cost of unusual events straight to the P&L.',
          'A sugar mill may carry under-absorption from the off-season to the crushing season.'),
        C('c7', T7, [
            'Administrative overheads relate to formulating policy, directing and controlling — office rent, salaries of office staff, audit fees. They may be treated as part of production cost (where related to production), charged to costing P&L, or apportioned between production and selling. They are controlled through budgets and standards.',
            'Selling overheads relate to creating and stimulating demand (advertising, salesmen, showrooms); distribution overheads relate to delivering goods (warehousing, packing for transport, carriage outward). They are absorbed as a rate per unit, a percentage of selling price or of factory cost, and controlled through budgets, standards and territory or product analysis.'],
          'Office and sales costs are real costs, but they do not belong in the cost of making the product.',
          'Secondary packing for transport is a distribution cost; primary packing is part of production cost.'),
        C('c8', T8, [
            'Capacity: installed (rated) capacity is the maximum possible; practical capacity is installed less unavoidable interruptions (commonly 10–25%); normal capacity is the average expected over several periods; actual capacity is what is achieved. Idle capacity = practical or normal less actual; its cost is usually charged to costing P&L if abnormal.',
            'Special items: interest on capital is generally excluded from cost; abnormal losses, penalties and fines are excluded; packing, research and development, and training costs are classified by the purpose they serve.'],
          'Plan on what you can normally do, not on what the machine label says.',
          'Cost of a plant idle for a month due to a power cut is not loaded on that year\'s products.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Setting departmental rates', 'role': 'Cost accountant',
         'situation': 'A factory with two machine shops and an assembly line uses one blanket rate.',
         'steps': ['Collect budgeted overheads by department.', 'Apportion common costs on suitable bases.', 'Re-apportion service departments (reciprocal method).', 'Set machine hour rates for machine shops and labour hour rate for assembly.'],
         'takeaway': 'Departmental rates stop simple products subsidising complex ones.'},
        {'id': 'j2', 'title': 'Year-end absorption review', 'role': 'Article assistant',
         'situation': 'Overheads are under-absorbed by 9%.',
         'steps': ['Split the difference into normal and abnormal causes.', 'Charge abnormal items to costing P&L.', 'Spread the normal part over WIP, finished goods and cost of sales.'],
         'takeaway': 'Explain the cause before choosing the disposal method.'},
    ]

    mcqs = [
        Q('m1', 'Rent of a factory building is best apportioned on the basis of:', ['Floor area', 'Number of employees', 'Direct wages', 'Value of plant'], 0,
          'Rent is a cost of space, so the share of floor area occupied by each department is the fairest basis. Employee numbers suit canteen and welfare costs; plant value suits insurance and depreciation of plant. In practice: use the basis that reflects the benefit received.', 'c2', T2),
        Q('m2', 'Which method of re-apportionment ignores services rendered by one service department to another?', ['Direct redistribution', 'Simultaneous equation', 'Repeated distribution', 'Trial and error'], 0,
          'The direct method sends service costs straight to production departments and ignores inter-service flows. The other three are reciprocal methods that recognise mutual services and give more accurate costs. In practice: direct is simple but less precise.', 'c3', T3),
        Q('m3', 'In the step method, the service department closed first is usually the one that:', ['Serves the largest number of other departments', 'Has the smallest cost', 'Is a production department', 'Serves no other department'], 0,
          'The step (ladder) method starts with the service department that renders service to the most other departments; once closed it receives nothing back. This limits the error from ignoring reverse flows. In practice: order matters for the result.', 'c3', T3, 'moderate'),
        Q('m4', 'Machine hour rate is most suitable where:', ['Work is done mainly by machines', 'Work is mainly manual', 'Only one product is made', 'Material cost dominates'], 0,
          'When machines do most of the work, overheads such as power, depreciation and repairs vary with machine running time, so machine hours are the best base. Manual work suits labour hour rates. In practice: compute separate rates per machine group.', 'c4', T4),
        Q('m5', 'Budgeted overheads ₹6,00,000; budgeted machine hours 24,000; actual hours 25,000; actual overheads ₹6,10,000. The result is:', ['Over-absorption of ₹15,000', 'Under-absorption of ₹15,000', 'Over-absorption of ₹10,000', 'Under-absorption of ₹25,000'], 0,
          'Rate = 6,00,000 ÷ 24,000 = ₹25 per hour; absorbed = 25,000 × 25 = ₹6,25,000; actual = ₹6,10,000; so overheads are over-absorbed by ₹15,000. Comparing budgets with actuals directly would mislead. In practice: compute the rate first.', 'c6', T6, 'hard'),
        Q('m6', 'Under-absorbed overheads caused by a fire in the factory should be:', ['Written off to costing profit and loss account', 'Spread by a supplementary rate', 'Carried forward', 'Added to selling price'], 0,
          'Abnormal causes such as fire, strikes or idle capacity due to breakdowns must not inflate product cost; they are charged to costing P&L. Supplementary rates are for normal differences; carry-forward suits seasonal patterns. In practice: identify the cause first.', 'c6', T6),
        Q('m7', 'A supplementary overhead rate is used to:', ['Adjust normal under- or over-absorption across units in stock and units sold', 'Absorb selling overheads', 'Replace the pre-determined rate', 'Charge abnormal costs'], 0,
          'It is an extra (or negative) rate computed as difference ÷ base actually used, and applied to units in WIP, finished goods and cost of sales so that they carry actual overheads. Abnormal items go to costing P&L instead. In practice: used when the difference is large.', 'c5', T5),
        Q('m8', 'Normal capacity is:', ['The average capacity expected over a number of periods', 'The maximum possible output', 'Output actually achieved', 'Installed capacity less 50%'], 0,
          'Normal capacity reflects the average expected utilisation over several periods, allowing for seasonal and cyclical swings. Installed capacity is the maximum; actual is what was achieved. In practice: rates based on normal capacity keep idle-capacity cost out of products.', 'c8', T8),
        Q('m9', 'Advertising is classified as:', ['Selling overhead', 'Distribution overhead', 'Factory overhead', 'Administrative overhead'], 0,
          'Selling overheads relate to creating and stimulating demand — advertising, salesmen\'s salaries and commission, showrooms. Distribution overheads relate to delivering goods, such as warehousing and carriage outward. In practice: the purpose decides the class.', 'c7', T7),
        Q('m10', 'A blanket overhead rate is suitable when:', ['The factory makes one product or all departments are uniform', 'There are many dissimilar departments', 'Products use departments unequally', 'Machine hours differ widely'], 0,
          'One rate for the whole factory gives fair costs only if products pass through departments in similar proportions, or there is a single product. Otherwise departmental rates are needed to avoid cross-subsidy. In practice: most multi-product factories use departmental rates.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Equations set up', 1.5, 'concept', 'equation|s1 ='),
           S('s2', 'Solve S1, S2', 2, 'computation', 's1', nums=[s1, s2]),
           S('s3', 'Totals for P1, P2', 2, 'computation', 'p1', nums=[p1, p2]),
           S('s4', 'Check total', 0.5, 'computation', 'total', nums=[tot])],
          ['Write both equations first.'], ['Using the direct method by mistake.'], ['Equations + table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Standing charges', 1.5, 'computation', 'standing', nums=[stand]),
           S('s2', 'Machine expenses', 1.5, 'computation', 'depreciation|power', nums=[dep, power]),
           S('s3', 'MHR', 1, 'computation', 'machine hour rate|rate', nums=[mhr])],
          ['Separate fixed and running costs.'], ['Ignoring scrap value in depreciation.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 5, i3['q'], i3['solution'],
          [S('s1', 'Rate and absorbed', 1.5, 'computation', 'rate|absorbed', nums=[rate, absd]),
           S('s2', 'Under-absorption', 1, 'computation', 'under', nums=[under]),
           S('s3', 'Abnormal to costing P&L', 1, 'concept', 'abnormal|costing p&l|profit and loss'),
           S('s4', 'Supplementary split', 1.5, 'computation', 'work-in-progress|supplementary', nums=[wip, fg, cogs])],
          ['Isolate abnormal items first.'], ['Spreading strike costs to stock.'], ['Table.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'Differentiate allocation and apportionment of overheads.',
          'Allocation charges a whole item of overhead to the one department that caused it; apportionment shares a common overhead among departments on a fair basis.',
          [P('p1', 'Allocation whole to one', 5, 'whole|one department|entire'), P('p2', 'Apportionment shares', 5, 'share|basis|common')], 'c2'),
        V('v2', 'Name the three methods of disposing of under-absorbed overheads.',
          'Using a supplementary rate, writing off to costing profit and loss account, and carrying forward to the next period.',
          [P('p1', 'Supplementary rate', 4, 'supplementary'), P('p2', 'Costing P&L', 3, 'profit and loss|p&l'), P('p3', 'Carry forward', 3, 'carry')], 'c6'),
        V('v3', 'Why are pre-determined rates preferred to actual rates?',
          'Actual rates are known only after the period ends, too late for pricing and quotations, and they swing with seasonal output; pre-determined rates are available in advance and stable.',
          [P('p1', 'Known only later', 5, 'after|late|end'), P('p2', 'Available in advance / stable', 5, 'advance|stable|quotation|pricing')], 'c5'),
        V('v4', 'What are standing charges in a machine hour rate?',
          'Fixed costs of the machine\'s department such as rent, supervision and insurance, which accrue per period whether or not the machine runs.',
          [P('p1', 'Fixed per period', 6, 'fixed|per period|whether'), P('p2', 'Examples', 4, 'rent|supervis|insurance')], 'c4'),
        V('v5', 'Distinguish practical capacity from normal capacity.',
          'Practical capacity is installed capacity less unavoidable interruptions such as maintenance and holidays; normal capacity is the average utilisation expected over several periods considering demand.',
          [P('p1', 'Practical = installed less interruptions', 5, 'interruption|installed'), P('p2', 'Normal = average over periods', 5, 'average|several|demand')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Tungabhadra Engineering', 'difficulty': 'moderate',
              'case': 'Tungabhadra Engineering budgets factory overheads of ₹18,00,000 and 90,000 machine hours for the year. Actual machine hours were 84,000 and actual overheads ₹17,40,000; ₹60,000 of the shortfall in hours was due to a three-week lockout.',
              'mcqs': [
                  M('k1a', 'The pre-determined machine hour rate is:', ['₹20', '₹20.71', '₹19.33', '₹21.43'], 0,
                    'Rate = budgeted overheads ÷ budgeted base = 18,00,000 ÷ 90,000 = ₹20 per machine hour. Actual figures are not used to set the rate. In practice: rates are fixed at the start of the year.', 'core', check=20, topic=T5),
                  M('k1b', 'Overheads absorbed are:', ['₹16,80,000', '₹17,40,000', '₹18,00,000', '₹16,20,000'], 0,
                    'Absorbed = actual hours × rate = 84,000 × 20 = ₹16,80,000. This is compared with actual overheads to find under- or over-absorption. In practice: absorption follows the actual base.', 'core', check=1680000, topic=T6),
                  M('k1c', 'Under-absorption is:', ['₹60,000', '₹1,20,000', '₹40,000', 'Nil'], 0,
                    'Actual ₹17,40,000 less absorbed ₹16,80,000 = ₹60,000 under-absorbed. The lockout explains it. In practice: always separate the cause.', 'moderate', check=60000, topic=T6),
                  M('k1d', 'The under-absorption caused by the lockout should be:', ['Charged to costing P&L', 'Spread over stock and cost of sales', 'Carried forward', 'Ignored'], 0,
                    'A lockout is abnormal, so the unabsorbed cost of idle capacity is written off to costing profit and loss account rather than loaded on products. Supplementary rates apply only to normal differences. In practice: show it separately in the reconciliation.', 'moderate', topic=T6),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch04', 1, 'Overheads – Absorption Costing Method',
                ['Classify overheads by function, behaviour, controllability, normality and element.',
                 'Allocate and apportion overheads, and re-apportion service department costs by direct, step and reciprocal methods.',
                 'Absorb overheads using suitable bases, including machine hour rates.',
                 'Identify overhead rate types and dispose of under- or over-absorption.',
                 'Account for administrative, selling and distribution overheads and apply capacity concepts.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['int-p4-ch03-u01'],
                 'exam_tip': 'Expect primary and secondary distribution (simultaneous equations or repeated distribution), a machine hour rate, and treatment of under-absorption with a supplementary rate.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Overheads are indirect costs; classify by function, behaviour, control, normality, element.', 'Primary distribution: allocate, then apportion on fair bases.',
                             'Secondary distribution: direct, step, or reciprocal (simultaneous, repeated, trial and error).', 'Absorption bases: % of material/prime/labour cost, labour hour, machine hour, per unit.',
                             'MHR = (standing charges + machine expenses) ÷ hours.', 'Under/over-absorption: supplementary rate, costing P&L, or carry forward.',
                             'Use normal capacity so idle-capacity cost stays out of products.'],
                 'remember': ['Reciprocal methods give identical production totals.', 'Abnormal costs always go to costing P&L.'],
                 'traps': ['Rate uses budgeted, absorption uses actual base.', 'Blanket rates distort multi-department costs.']},
                [('Rate', 'Budgeted OH ÷ budgeted base'), ('Absorbed', 'Actual base × rate'), ('MHR', '(Standing + running) ÷ hours'),
                 ('Rent', 'Floor area'), ('Canteen', 'No. of employees')],
                viva, cases,
                topics=['Introduction', 'Classification of Overheads', 'Accounting of Overheads', 'Steps for Distribution of Overheads', 'Methods of Absorbing Overheads to Various Products or Jobs',
                        'Types of Overhead Rates', 'Treatment of Under-Absorbed and Over-Absorbed Overheads', 'Accounting and Control of Administrative Overheads',
                        'Accounting and Control of Selling and Distribution Overheads', 'Concepts Related to Capacity', 'Treatment of Certain Items in Costing'])
