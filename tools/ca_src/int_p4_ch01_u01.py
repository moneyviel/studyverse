"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 1 Introduction to Cost and Management Accounting.
Scope follows the ICAI study material (May 2027 onwards); all explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch01-u01'
T1 = 'Cost, costing and cost accounting: the vocabulary'
T2 = 'Objectives and scope; cost control vs cost reduction'
T3 = 'Cost, management and financial accounting compared'
T4 = 'A good costing system and how to install it'
T5 = 'Cost objects, cost units and cost drivers'
T6 = 'Responsibility centres'
T7 = 'Classifying costs: nature, function, behaviour'
T8 = 'Separating semi-variable costs'
T9 = 'Costs for decisions, control and normality'
T10 = 'Methods and techniques of costing'


def build():
    ck = Checks()
    vc = ck.add('(305000-230000)/(6500-4000)', 'high-low: variable cost per unit')
    fc = ck.add('230000-4000*(305000-230000)/(6500-4000)', 'high-low: fixed cost')
    est = ck.add('230000-4000*(305000-230000)/(6500-4000)+5800*(305000-230000)/(6500-4000)', 'estimated cost at 5,800 units')
    ck2 = Checks()
    sxy = ck2.add('1*12+2*15+3*19+4*22+5*27', 'Σxy'); sx2 = ck2.add('1+4+9+16+25', 'Σx²')
    m = ck2.add('(5*(1*12+2*15+3*19+4*22+5*27)-15*95)/(5*(1+4+9+16+25)-15**2)', 'slope m (₹\'000 per thousand units)')
    c = ck2.add('(95-15*(5*(1*12+2*15+3*19+4*22+5*27)-15*95)/(5*(1+4+9+16+25)-15**2))/5', 'intercept c (fixed cost, ₹\'000)')
    est2 = ck2.add('(95-15*(5*(1*12+2*15+3*19+4*22+5*27)-15*95)/(5*(1+4+9+16+25)-15**2))/5+6*(5*(1*12+2*15+3*19+4*22+5*27)-15*95)/(5*(1+4+9+16+25)-15**2)', 'estimated cost at 6 thousand units (₹\'000)')

    centres = table(['Centre', 'Manager is answerable for', 'Typical example'], [
        ['Cost centre — standard', 'Costs, where output is measurable and standard inputs can be set', 'Machining shop of a factory'],
        ['Cost centre — discretionary', 'Costs where output cannot be measured in money (budget-based control)', 'HR, legal, R&D, advertising'],
        ['Revenue centre', 'Revenue (and its own selling costs)', 'Regional sales office'],
        ['Profit centre', 'Both revenue and costs — profit', 'A product division or branch'],
        ['Investment centre', 'Profit and the capital invested — return on investment', 'A strategic business unit or subsidiary'],
    ], title='Types of responsibility centres')
    compare = table(['Basis', 'Financial accounting', 'Cost accounting', 'Management accounting'], [
        ['Main users', 'Outsiders — shareholders, lenders, government', 'Internal management', 'Internal management'],
        ['Focus', 'Whole business, past period', 'Products, jobs, processes, departments', 'Planning, control and decisions — past and future'],
        ['Rules', 'Statutes and Accounting Standards', 'Cost accounting principles; cost audit rules where applicable', 'No fixed format — whatever helps the decision'],
        ['Data', 'Monetary, actual', 'Monetary and physical, actual and standard', 'Monetary and non-monetary, actual and estimated'],
        ['Periodicity', 'Usually annual (quarterly for listed)', 'Frequent — as needed', 'As and when management needs it'],
    ], title='Three accounting branches')
    methods = table(['Method', 'Suits', 'Example'], [
        ['Single / output / unit costing', 'One standardised product made continuously', 'Bricks, coal, cement'],
        ['Job costing', 'Work done to each customer\'s order', 'Printing press, repair workshop'],
        ['Batch costing', 'Identical items made in lots (extension of job costing)', 'Medicines, biscuits, toys'],
        ['Contract costing', 'Large jobs over long periods, often at site', 'Bridges, buildings, ships'],
        ['Process costing', 'Output passing through successive processes', 'Sugar, chemicals, textiles, oil refining'],
        ['Operating / service costing', 'Services rather than goods', 'Transport, hospitals, hotels, power'],
        ['Multiple / composite costing', 'Products assembled from many separately made parts', 'Cars, aircraft, radios'],
    ], title='Methods of costing')

    concepts = [
        C('c1', T1, [
            'Cost: the resource given up to obtain goods or services. As a noun it is the spending — real or notional — that can be traced to a product, service or activity; as a verb, "to cost" means to work out the cost of something.',
            'Costing: the technique and process of ascertaining costs. Cost accounting: the process of accounting for costs — from recording expenditure (or the bases on which it is calculated) through to periodic statements and reports that ascertain and control costs. Cost accountancy: applying costing and cost accounting principles, methods and techniques to cost control and the ascertainment of profitability, including presenting information for decisions.',
            'Management accounting (CIMA view): applying accounting and financial management principles to create, protect, preserve and increase value for stakeholders of profit-making and not-for-profit enterprises, public or private. It supplies information for planning, organising, controlling and decision-making.',
            'Cost management: using management accounting concepts and data collection, analysis and presentation to plan, monitor and control costs.'],
          'Costing is the kitchen scale, cost accounting is the recipe book that records every weighing, and cost accountancy is the head chef deciding how to cut waste and price the menu.',
          'A CA in industry builds product costs that drive pricing, make-or-buy and cost-reduction programmes.'),
        C('c2', T2, [
            'Objectives: ascertaining cost; determining selling price and profitability; cost control; cost reduction; and helping management take decisions (make or buy, accept or reject an order, shut down or continue).',
            'Scope: cost ascertainment, cost accounting (recording and classifying), cost analysis, cost comparison, cost control, cost reports and statutory compliance such as cost records and cost audit where required.',
            'Cost control keeps actual costs within set standards or budgets — it accepts the standard and corrects deviations; it is preventive, works on the present, and its process ends once targets are achieved.',
            'Cost reduction achieves a real and permanent fall in unit cost without impairing quality or suitability for use — it challenges the standard itself; it is corrective and continuous, using tools such as value analysis, job evaluation, design improvement and work study.'],
          'Cost control is keeping the car within the speed limit; cost reduction is redesigning the engine so it uses less fuel at the same speed.',
          'Budget-vs-actual variance reports are cost control; a value-engineering project that redesigns packaging to save 8% per unit is cost reduction.'),
        C('c3', T3, [
            'Cost accounting and management accounting: cost accounting supplies the data (product and process costs, standards, variances); management accounting uses this data with other financial and non-financial information for planning, control and decisions. Management accounting is wider in scope.',
            'Cost accounting and financial accounting: financial accounting records transactions to show the true and fair profit and position to outsiders under statute and standards; cost accounting analyses costs by product, job, process or department for internal use, with physical as well as monetary data and standards as well as actuals.',
            'The three branches complement each other: financial accounts give the overall result; cost accounts explain where it came from; management accounting helps decide what to do next. Cost and financial profits are periodically reconciled.'],
          'Financial accounting is the scoreboard after the match, cost accounting is the player-by-player statistics, management accounting is the coach\'s game plan for the next match.',
          'A plant controller reconciles cost-book profit with the financial-book profit every month, explaining differences such as notional costs and items excluded from costing.',
          blocks=[compare]),
        C('c4', T4, [
            'A good costing system is tailor-made for the business, simple and economical (its benefit should exceed its cost), supported by management and staff, built on reliable data and a sound material and labour control, uses uniform forms, and gives timely reports that can be reconciled with financial accounts.',
            'Installing a system: first study the business — product, technical process, organisation and how costs arise; decide the objective of the system; fix the cost units, cost centres and method suited to the product; decide the elements of cost and how overheads will be collected and absorbed; set up material, labour and overhead control procedures and forms; plan reports — what, to whom and how often; and win the cooperation of staff by explaining the system.',
            'Typical practical difficulties: lack of top-management support, resistance from staff who see it as interference, cost of running the system, and shortage of trained staff. These are overcome by involving staff early, keeping the system simple and showing its benefits.',
            'Digital costing: ERP data, AI and machine learning can analyse large data sets to ascertain cost on each cost object with more certainty, study time spent on activities, plan material purchases (JIT, zero wastage), spot non-value-added activities, set standards and measure variances in real time, mark material standards to current prices and forecast demand.'],
          'Installing a costing system is like fitting a car with instruments: decide what you need to watch, put sensors in the right places, and make sure the driver actually reads the dashboard.',
          'Many CAs in industry lead ERP costing implementations — mapping cost centres, activities and drivers into the system.'),
        C('c5', T5, [
            'Cost object: anything for which costs are measured separately — a product (a smartphone), a service (a Delhi–Mumbai flight), a project (a metro line), an activity (quality inspection), a process (crude refining) or a department. Whether a cost is direct or indirect, fixed or variable, is judged relative to the cost object.',
            'Cost unit: the unit of product, service or time in which costs are expressed — per tonne of steel, per kWh of power, per passenger-km of transport, per 1,000 bricks, per patient-day in a hospital, per chargeable hour in a professional firm. A whole job, contract or batch can itself be a cost unit.',
            'Cost driver: a factor that causes cost to change — number of set-ups, purchase orders, inspection hours or tests. CIMA links cost drivers to Activity Based Costing, where they connect the consumption of activities to products.'],
          'The cost object is the thing you are pricing, the cost unit is the measuring cup, and the cost driver is the tap that controls how fast cost flows.',
          'Choosing the right driver (number of purchase orders rather than value of purchases) can completely change which product looks profitable.'),
        C('c6', T6, [
            'As an organisation grows, authority is delegated to departments or persons — responsibility centres — whose performance is measured against standards or budgets in terms of cost, revenue, profit or return on investment.',
            'Cost centre: answerable for costs under its control. Standard cost centres have measurable output and standard inputs (variances analysed into controllable and uncontrollable); discretionary cost centres have output that cannot be measured in money, so they are controlled through budgets (advertising, R&D, HR).',
            'Revenue centre: answerable for revenue — a sales office; profit centre: answerable for revenue and costs; investment centre: answerable for profit relative to the capital employed (ROI, residual income).',
            'Cost centres are also classified as personal (a person or group) or impersonal (a location or item of equipment), and production or service cost centres.'],
          'Responsibility centres are like a cricket team\'s roles: the bowler is judged on runs conceded (cost), the batter on runs scored (revenue), the all-rounder on both (profit), and the captain on results relative to the squad he was given (investment).',
          'Divisional managers of a conglomerate are often evaluated as investment centres on return on capital employed.',
          blocks=[centres]),
        C('c7', T7, [
            'By nature or element: material, employee (labour) and other expenses, each split into direct (identifiable with the cost object economically) and indirect (overheads). Direct material + direct employee cost + direct expenses = prime cost.',
            'By function: production (manufacturing), administration, selling, distribution, and research and development costs.',
            'By behaviour or variability: fixed costs stay constant in total within a relevant range and time (rent, salaries) — per unit they fall as output rises; variable costs change in total in direct proportion to output (direct material) — per unit they stay constant; semi-variable costs have both parts (electricity with a fixed charge plus usage); step costs stay fixed over a range and then jump (one supervisor per 20 workers).',
            'Classification depends on the cost object and the decision: the same supervisor\'s salary is direct to the department but indirect to each product.'],
          'Fixed cost is the monthly gym fee, variable cost is the per-session coaching fee, and a semi-variable cost is a phone plan with a fixed rental plus per-minute charges.',
          'Break-even analysis, pricing and budgeting all start from splitting costs into fixed and variable parts.'),
        C('c8', T8, [
            'Methods to split semi-variable costs: (a) graphical — plot cost against output, draw a line of best fit; where it cuts the cost axis is the fixed cost; (b) high-low — take the highest and lowest activity levels: variable cost per unit = change in cost ÷ change in activity, the balance at either level is fixed; (c) analytical — an experienced cost accountant judges the degree of variability of each item; (d) comparison by period or level of activity — compare costs of two periods or levels and treat the change as variable; (e) least squares — fit y = mx + c to all observations, the most accurate method.',
            'Least squares: m = (nΣxy − ΣxΣy) ÷ (nΣx² − (Σx)²) and c = (Σy − mΣx) ÷ n, where y is total cost, x is activity, m the variable cost per unit and c the fixed cost.',
            'High-low is quick but uses only two observations, which may be untypical; least squares uses every observation.'],
          'High-low draws a line through two stars; least squares draws the line that sits closest to the whole constellation.',
          'Plant controllers use regression in a spreadsheet (the least-squares method) to estimate the fixed part of power and maintenance costs for budgets.'),
        C('c9', T9, [
            'By controllability: controllable costs can be influenced by the manager of a responsibility centre within a period (raw-material usage by the shop-floor manager); uncontrollable costs cannot be influenced by that manager (rent fixed by head office). Controllability depends on the level of management and the time span.',
            'By normality: normal costs arise at a given level of output under normal conditions and are part of product cost (normal process loss); abnormal costs are unusual — fire, strike, abnormal loss — and are charged to Costing Profit and Loss, not to products.',
            'Costs for decision-making: marginal cost (variable cost of one more unit); differential cost (change in total cost between two alternatives — incremental or decremental); opportunity cost (benefit forgone from the next-best alternative); sunk cost (already incurred and irrecoverable — irrelevant to decisions); relevant cost (future cost that differs between alternatives); imputed or notional cost (not paid in cash but considered — interest on own capital, rent of owned premises); out-of-pocket cost (involving a cash payment); shut-down cost (incurred even when operations are suspended); discretionary cost (management chooses the amount — advertising, R&D); avoidable and unavoidable costs; replacement cost (current price to replace an item); and engineered cost (input-output relationship can be measured).'],
          'Sunk cost is milk already spilt — no decision can bring it back, so leave it out of the calculation.',
          'In a make-or-buy decision a CA ignores sunk development costs but includes opportunity cost of the factory space freed.'),
        C('c10', T10, [
            'Methods of costing decide how the cost of the output is ascertained, depending on the nature of production (see table). Activity Based Costing (assigning costs to activities and then to products) is also widely used.',
            'Techniques of costing are ways of presenting and controlling cost and can be used with any method: uniform costing (several firms in an industry follow the same costing principles — enabling comparison and fair pricing), marginal costing (separates fixed and variable costs; only variable costs are charged to products), standard costing (predetermined costs compared with actuals and variances analysed), historical costing (costs ascertained after they are incurred — post costing — or as soon as a job is finished — continuous costing; limited usefulness) and absorption costing (all costs, fixed and variable, charged to products).'],
          'The method is the type of vehicle (car, bus, truck) chosen for the road; the technique is the driving style (economical, sporty) that can be used in any vehicle.',
          'A cement company may use process costing as its method while applying standard costing and marginal costing as techniques for control and decisions.',
          blocks=[methods]),
    ]

    illustrations = [
        {'id': 'i1', 'title': 'High-low method for power cost', 'difficulty': 'core', 'minutes': 6,
         'q': 'A factory\'s power cost was ₹2,30,000 when output was 4,000 units and ₹3,05,000 when output was 6,500 units (the lowest and highest levels of the year). Using the high-low method, find the variable cost per unit, the fixed cost and the estimated power cost at 5,800 units.',
         'solution': [table(['Level', 'Output (units)', 'Power cost ₹'], [['High', '6,500', '3,05,000'], ['Low', '4,000', '2,30,000'], ['Difference', '2,500', '75,000']], title='High-low working'),
                      wn('Variable cost per unit', f'₹75,000 ÷ 2,500 units = {R(vc)} per unit.'),
                      wn('Fixed cost', f'₹2,30,000 − (4,000 × {R(vc)}) = {R(fc)}. Check at 6,500 units: {R(fc)} + 6,500 × {R(vc)} = ₹3,05,000.'),
                      wn('Estimate at 5,800 units', f'{R(fc)} + 5,800 × {R(vc)} = {R(est)}.')],
         'checks': list(ck)},
        {'id': 'i2', 'title': 'Least squares for maintenance cost', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Maintenance cost (₹\'000) and output (\'000 units) for five months were: (1, 12), (2, 15), (3, 19), (4, 22), (5, 27). Fit the line y = mx + c by the method of least squares and estimate the cost at an output of 6 thousand units.',
         'solution': [table(['x', 'y', 'xy', 'x²'], [['1', '12', '12', '1'], ['2', '15', '30', '4'], ['3', '19', '57', '9'], ['4', '22', '88', '16'], ['5', '27', '135', '25'], ['15', '95', inr(sxy), inr(sx2)]], num=[0, 1, 2, 3], total=True, title='Working table (n = 5)'),
                      wn('Slope', f'm = (5 × {sxy} − 15 × 95) ÷ (5 × {sx2} − 15²) = 185 ÷ 50 = {m} (₹\'000 per thousand units, i.e. ₹{inr(m)} per unit).'),
                      wn('Intercept', f'c = (95 − {m} × 15) ÷ 5 = {c}, i.e. fixed cost ₹{inr(c * 1000)} per month.'),
                      wn('Estimate', f'At 6 thousand units: y = {c} + {m} × 6 = {est2} (₹\'000), i.e. ₹{inr(est2 * 1000)}.')],
         'checks': list(ck2)},
        {'id': 'i3', 'title': 'Pick the relevant costs', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Asha Plastics must decide whether to accept a special order. Classify each item: (a) ₹1,80,000 already spent on a mould last year that can be used for the order; (b) material to be bought at ₹95 per kg; (c) a machine that would otherwise be rented out for ₹40,000 during the order period; (d) factory rent of ₹60,000 per month payable anyway; (e) interest on the owner\'s capital considered in costing but not paid.',
         'solution': [table(['Item', 'Classification', 'Relevant to the decision?'], [
             ['(a) Mould cost', 'Sunk cost', 'No — already incurred and unaffected by the decision'],
             ['(b) Material', 'Out-of-pocket, variable, relevant cost', 'Yes'],
             ['(c) Rent forgone', 'Opportunity cost', 'Yes — benefit given up'],
             ['(d) Factory rent', 'Fixed, committed (unavoidable) cost', 'No — same under both alternatives'],
             ['(e) Interest on own capital', 'Imputed / notional cost', 'Only if the capital has an alternative use; usually excluded from cash decisions'],
         ])]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Designing cost centres for a new plant', 'role': 'Cost accountant at a packaging company',
         'situation': 'A new plant with extrusion, printing, lamination and slitting lines plus maintenance, stores and quality control is being commissioned.',
         'steps': ['Treat each production line as a production (standard) cost centre with machine hours as the cost unit for overheads.', 'Treat maintenance, stores and QC as service cost centres whose costs will be apportioned to production centres.', 'Identify cost drivers: maintenance hours, number of requisitions, number of tests.', 'Agree responsibility: line managers answer for controllable costs; the plant head as a profit centre.'],
         'takeaway': 'Cost centres, cost units and drivers must mirror how work actually flows.'},
        {'id': 'j2', 'title': 'Cost control or cost reduction?', 'role': 'Management accountant presenting to the CFO',
         'situation': 'Packaging cost per unit has risen. Two proposals: tighter monitoring of wastage against the standard, and redesigning the carton to use 12% less board.',
         'steps': ['The first keeps actuals within the standard — cost control.', 'The second permanently lowers the cost per unit without hurting quality — cost reduction.', 'Recommend both: control now, reduction for the next budget.'],
         'takeaway': 'Control guards the standard; reduction lowers the standard.'},
    ]

    mcqs = [
        Q('m1', 'Costing is best defined as:', ['The technique and process of ascertaining costs', 'Preparation of financial statements for shareholders', 'Recording of all transactions under double entry', 'Auditing of cost records'], 0,
          'Costing is the technique and process of finding out costs. Cost accounting goes further — recording, classifying and reporting costs — and cost accountancy applies these principles to control and decision-making. Preparing statements for shareholders is financial accounting, the usual trap. In practice: costing answers "what did this product cost?"; cost accounting builds the system that keeps answering it.', 'c1', T1),
        Q('m2', 'Which statement about cost reduction is correct?', ['It aims at a real and permanent fall in unit cost without impairing quality', 'It accepts the standard and keeps actuals within it', 'It is a one-time exercise that ends once targets are met', 'It is the same as cost control'], 0,
          'Cost reduction challenges standards and seeks a permanent fall in unit cost without impairing quality or suitability for use; it is continuous and corrective. Keeping actuals within standards is cost control, which is the tempting trap. In practice: redesigning a product to use less material is reduction; monitoring wastage against the standard is control.', 'c2', T2),
        Q('m3', 'Which is a technique of cost REDUCTION rather than cost control?', ['Value analysis', 'Budgetary control', 'Standard costing variance reports', 'Material control through stock levels'], 0,
          'Value analysis examines each feature of a product to cut cost without reducing value — a cost-reduction tool. Budgetary control, variance reports and stock-level control keep actuals within set norms, so they are cost-control tools. In practice: value analysis often replaces costly materials or simplifies designs.', 'c2', T2, 'moderate'),
        Q('m4', 'A responsibility centre whose manager is evaluated on profit relative to the capital employed is:', ['An investment centre', 'A profit centre', 'A revenue centre', 'A discretionary cost centre'], 0,
          'An investment centre is answerable for profit and for the investment used to earn it, so it is judged by return on investment or residual income. A profit centre is judged on profit alone without reference to capital, which is the closest trap. In practice: a subsidiary\'s CEO is often measured on return on capital employed.', 'c6', T6),
        Q('m5', 'An R&D department, whose output cannot be measured in money, is best treated as:', ['A discretionary cost centre', 'A standard cost centre', 'A revenue centre', 'An investment centre'], 0,
          'Where outputs cannot be measured in financial terms, control is through budgets — a discretionary cost centre (R&D, advertising, HR). A standard cost centre needs measurable output and standard inputs, as on a production line. In practice: R&D managers are held to an approved budget rather than a cost per unit.', 'c6', T6, 'moderate'),
        Q('m6', 'The cost unit for a hospital is generally:', ['Patient-day', 'Kilowatt-hour', 'Passenger-kilometre', 'Tonne-kilometre'], 0,
          'Hospitals express costs per patient-day (or per bed-day). Kilowatt-hour is used in power generation, passenger-kilometre in passenger transport and tonne-kilometre in goods transport. In practice: choosing the right cost unit lets a hospital compare its cost per patient-day across wards and with peers.', 'c5', T5),
        Q('m7', 'The number of purchase orders placed, used to assign procurement costs, is an example of:', ['A cost driver', 'A cost unit', 'A cost centre', 'A cost object'], 0,
          'A cost driver is a factor that causes the level of a cost to change; the number of purchase orders drives procurement cost and is used in Activity Based Costing to assign it. The trap is "cost unit", which is the measure in which cost is expressed for output. In practice: ABC uses such drivers to show which products truly consume support activities.', 'c5', T5),
        Q('m8', 'Total fixed cost within the relevant range, as output increases:', ['Remains constant in total; falls per unit', 'Rises in total; constant per unit', 'Falls in total; rises per unit', 'Rises in total and per unit'], 0,
          'Fixed costs stay the same in total within a relevant range and period, so spreading them over more units lowers the fixed cost per unit. "Rises in total, constant per unit" describes variable cost, which is the trap. In practice: higher capacity utilisation lowers unit cost mainly through this effect.', 'c7', T7),
        Q('m9', 'Prime cost consists of:', ['Direct material + direct employee cost + direct expenses', 'All factory costs', 'Direct material + all overheads', 'Total cost less selling costs'], 0,
          'Prime cost is the total of all direct costs — direct material, direct employee (labour) cost and direct expenses. Adding production overheads gives factory or works cost, which is the trap. In practice: prime cost is often the base for absorbing overheads in some job shops.', 'c7', T7),
        Q('m10', 'Under the high-low method, cost was ₹2,30,000 at 4,000 units and ₹3,05,000 at 6,500 units. Variable cost per unit is:', ['₹30', '₹57.50', '₹46.92', '₹46.90'], 0,
          'Variable cost per unit = change in cost ÷ change in output = (3,05,000 − 2,30,000) ÷ (6,500 − 4,000) = 75,000 ÷ 2,500 = ₹30. The trap ₹57.50 divides the low-level total cost by its output, mixing fixed cost in. In practice: high-low gives a quick split but relies on two points only.', 'c8', T8, check='(305000-230000)/(6500-4000)'),
        Q('m11', 'Which method of segregating semi-variable costs is considered the most accurate?', ['Least squares method', 'High-low method', 'Analytical method', 'Graphical method'], 0,
          'The least squares method fits the line y = mx + c using all observations mathematically, so it is the best method of segregation. High-low uses only two extreme points, analytical relies on judgement, and graphical depends on a hand-drawn line of best fit. In practice: spreadsheet regression functions apply least squares instantly.', 'c8', T8),
        Q('m12', 'Cost already incurred and irrecoverable, which should be ignored in decisions, is:', ['Sunk cost', 'Opportunity cost', 'Imputed cost', 'Differential cost'], 0,
          'Sunk costs have already been incurred and cannot be changed by any future decision, so they are irrelevant. Opportunity cost is a benefit forgone and is relevant, which is why it is the trap. In practice: money already spent on a failed prototype should not sway the decision to continue or stop the project.', 'c9', T9),
        Q('m13', 'Interest on the proprietor\'s own capital, considered for decisions but not actually paid, is a:', ['Notional (imputed) cost', 'Sunk cost', 'Out-of-pocket cost', 'Shut-down cost'], 0,
          'Imputed or notional costs do not involve cash payment but are considered to make comparisons fair — interest on own capital or rent of owned premises. Out-of-pocket cost involves cash payment, which is the trap. In practice: notional items are excluded from financial accounts and so appear in the reconciliation of cost and financial profit.', 'c9', T9),
        Q('m14', 'Losses due to a fire in the stores are treated in cost accounts as:', ['Abnormal cost charged to Costing Profit and Loss Account', 'Part of product cost', 'Selling overhead', 'Direct expense'], 0,
          'Abnormal costs arise from unusual events such as fire, flood or strikes; including them in product cost would distort it, so they go to Costing Profit and Loss Account. Normal costs, such as normal process loss, are included in product cost — the trap. In practice: insurance claims are set off against the abnormal loss account.', 'c9', T9, 'moderate'),
        Q('m15', 'The method of costing suitable for a sugar mill is:', ['Process costing', 'Job costing', 'Contract costing', 'Batch costing'], 0,
          'Sugar passes through successive processes (crushing, clarification, evaporation, crystallisation), so the cost of each process is ascertained — process costing. Job costing suits customer-specific orders, contract costing large site projects, and batch costing identical items made in lots. In practice: chemicals, textiles and oil refining also use process costing.', 'c10', T10),
        Q('m16', 'Which is a TECHNIQUE of costing rather than a method?', ['Marginal costing', 'Job costing', 'Process costing', 'Operating costing'], 0,
          'Techniques — uniform, marginal, standard, historical and absorption costing — can be used with any method to present and control costs. Job, process and operating costing are methods, chosen according to the nature of production. In practice: a refinery uses process costing (method) with standard costing (technique).', 'c10', T10, 'moderate'),
        Q('m17', 'Ticket counters at a railway station, held responsible for collections, are best described as:', ['Revenue centres', 'Investment centres', 'Standard cost centres', 'Profit centres'], 0,
          'A ticket counter is answerable for the revenue it collects, not for the cost of running trains or for capital invested, so it is a revenue centre. Profit centres answer for both revenue and costs, which is the trap. In practice: booking offices are evaluated on collection targets and cash accuracy.', 'c6', T6),
        Q('m18', 'Cost accounting differs from financial accounting mainly because cost accounting:', ['Is meant primarily for internal management and analyses cost by product, job or process', 'Must follow Accounting Standards for publication', 'Deals only with monetary transactions of the past year', 'Is prepared mainly for the tax authorities'], 0,
          'Cost accounting serves internal management, analysing costs by product, job, process or department, using physical and standard data as well as actuals. Following Accounting Standards for published statements describes financial accounting, the trap. In practice: management reports from cost accounts are prepared weekly or monthly, not just annually.', 'c3', T3),
    ]

    ckq = Checks()
    qv = ckq.add('(186000-150000)/(9000-6000)', 'q2 variable cost per unit')
    qf = ckq.add('150000-6000*(186000-150000)/(9000-6000)', 'q2 fixed cost')
    qe = ckq.add('150000-6000*(186000-150000)/(9000-6000)+8200*(186000-150000)/(9000-6000)', 'q2 cost at 8,200 units')
    questions = [
        W('q1', 5, 'Distinguish between cost control and cost reduction.',
          [table(['Basis', 'Cost control', 'Cost reduction'], [
              ['Meaning', 'Keeping actual costs within set standards or budgets', 'Achieving a real and permanent fall in unit cost without lowering quality'],
              ['View of standards', 'Accepts the standard and corrects deviations', 'Challenges and lowers the standard itself'],
              ['Nature', 'Preventive — acts before and while costs arise', 'Corrective — improves the way things are done'],
              ['Time span', 'Ends when the target is achieved', 'Continuous process'],
              ['Tools', 'Budgetary control, standard costing, stock levels', 'Value analysis, work study, job evaluation, design improvement'],
          ])],
          [S('s1', 'Meaning of each', 1.5, 'concept', 'within|budget|standard', 'permanent|real', 'quality', n=2),
           S('s2', 'Standards accepted vs challenged', 1, 'concept', 'accept|achieve', 'challeng|lower|question|reduc'),
           S('s3', 'Preventive vs corrective', 1, 'concept', 'preventive', 'corrective'),
           S('s4', 'Tools of each', 1.5, 'concept', 'budget|standard costing|stock level', 'value analysis|work study|job evaluation|value engineering|design')],
          ['A table with a "Basis" column is the expected format.'], ['Treating cost reduction as a one-time exercise.', 'Listing budgetary control as a cost-reduction tool.'],
          ['Five rows: meaning, standards, nature, time span, tools.'], pad='table'),
        W('q2', 5, 'The maintenance cost of a plant was ₹1,50,000 for 6,000 machine hours (lowest) and ₹1,86,000 for 9,000 machine hours (highest). Using the high-low method, find the variable cost per hour and the fixed cost, and estimate the cost for 8,200 hours.',
          [table(['Level', 'Hours', 'Cost ₹'], [['Highest', '9,000', '1,86,000'], ['Lowest', '6,000', '1,50,000'], ['Difference', '3,000', '36,000']]),
           wn('Variable cost per hour', f'₹36,000 ÷ 3,000 hours = {R(qv)}.'), wn('Fixed cost', f'₹1,50,000 − 6,000 × {R(qv)} = {R(qf)}.'),
           wn('Estimate for 8,200 hours', f'{R(qf)} + 8,200 × {R(qv)} = {R(qe)}.')],
          [S('s1', 'Differences in cost and hours', 1, 'computation', nums=[36000, 3000]), S('s2', 'Variable cost ₹12 per hour', 1.5, 'computation', nums=[qv]),
           S('s3', 'Fixed cost ₹78,000', 1.5, 'computation', nums=[qf]), S('s4', 'Estimate ₹1,76,400', 1, 'computation', nums=[qe])],
          ['Show the difference row — it carries a mark.'], ['Dividing total cost by hours at one level.'], ['Always check the fixed cost at the other level.'], pad='table', checks=list(ckq)),
        W('q3', 5, 'What are responsibility centres? Explain the different types with an example of each.',
          [p('Responsibility centres are units of an organisation — departments, divisions or persons — to whom authority is delegated and who are held accountable for performance in terms of cost, revenue, profit or return on investment, measured against standards or budgets.'),
           ul(['Cost centre: accountable for costs under its control. A standard cost centre has measurable output and standard inputs (a machining shop); a discretionary cost centre has output not measurable in money and is controlled by budgets (R&D).',
               'Revenue centre: accountable for revenue — e.g. a regional sales office or a ticket counter.',
               'Profit centre: accountable for both revenue and costs — e.g. a product division or branch.',
               'Investment centre: accountable for profit in relation to capital employed — e.g. a subsidiary or strategic business unit judged on ROI.'])],
          [S('s1', 'Meaning', 1, 'concept', 'accountab|responsib', 'cost|revenue|profit|investment'),
           S('s2', 'Cost centre (standard / discretionary)', 1.5, 'concept', 'cost centre|cost center', 'standard|discretionary'),
           S('s3', 'Revenue centre', 0.5, 'concept', 'revenue centre|revenue center'),
           S('s4', 'Profit centre', 1, 'concept', 'profit centre|profit center', 'revenue and cost|revenue and costs|both'),
           S('s5', 'Investment centre — ROI', 1, 'concept', 'investment centre|investment center', 'capital|roi|return on investment')],
          ['Examples earn marks — give one for each type.'], ['Confusing a profit centre with an investment centre.'], ['Use four sub-headings.']),
    ]

    viva = [
        V('v1', 'Distinguish cost control from cost reduction.',
          'Cost control keeps actual costs within the standards or budgets and accepts the standard. Cost reduction aims at a real and permanent fall in unit cost without affecting quality, and it challenges the standard itself.',
          [P('p1', 'Control keeps costs within standards', 4, 'within|keep|budget|standard'), P('p2', 'Reduction — permanent fall in unit cost', 4, 'permanent|real'), P('p3', 'Without affecting quality', 2, 'without affecting quality|without hurting quality|without lowering quality|maintain quality')], 'c2'),
        V('v2', 'Name the types of responsibility centres.',
          'There are cost centres, revenue centres, profit centres and investment centres.',
          [P('p1', 'Cost centre', 2, 'cost centre|cost center'), P('p2', 'Revenue centre', 2, 'revenue centre|revenue center'), P('p3', 'Profit centre', 3, 'profit centre|profit center'), P('p4', 'Investment centre', 3, 'investment centre|investment center')], 'c6'),
        V('v3', 'What is the difference between a cost unit and a cost driver?',
          'A cost unit is the unit of product, service or time in which costs are expressed, such as per tonne or per patient day. A cost driver is a factor that causes the level of cost to change, such as the number of purchase orders or machine set ups.',
          [P('p1', 'Cost unit — unit in which costs are expressed', 5, 'cost unit', 'unit|express|measure'), P('p2', 'Cost driver — factor causing cost to change', 5, 'driver', 'factor|cause|influenc|change')], 'c5'),
        V('v4', 'Name the methods of segregating semi-variable costs.',
          'The methods are the graphical method, the high low method, the analytical method, comparison by period or level of activity, and the least squares method, which is the most accurate.',
          [P('p1', 'Graphical', 2, 'graph'), P('p2', 'High-low', 2, 'high low|high-low'), P('p3', 'Analytical', 2, 'analytical'), P('p4', 'Comparison by period / level', 2, 'comparison|period|level of activ'), P('p5', 'Least squares', 2, 'least square')], 'c8'),
        V('v5', 'Distinguish methods of costing from techniques of costing with examples.',
          'Methods depend on the nature of production, such as job, batch, contract, process and operating costing. Techniques such as marginal, standard, uniform and absorption costing are ways of presenting and controlling costs and can be used with any method.',
          [P('p1', 'Methods depend on nature of production', 3, 'method', 'nature|production|industr'), P('p2', 'Method examples', 2, 'job|process|contract|batch|operating'),
           P('p3', 'Techniques usable with any method', 3, 'technique', 'any method|presenting|control|with any'), P('p4', 'Technique examples', 2, 'marginal|standard|uniform|absorption')], 'c10'),
    ]

    cases = [{'id': 'k1', 'title': 'Setting up costing at Saral Foods', 'difficulty': 'moderate',
              'case': 'Saral Foods makes biscuits in batches of 10,000 packets, runs a delivery fleet and a canteen. Its power cost was ₹96,000 at 2,000 machine hours and ₹1,32,000 at 3,200 machine hours. Management is considering buying packaging instead of making it in-house; ₹5,00,000 was spent last year on the in-house packaging machine.',
              'mcqs': [
                  M('k1a', 'The most suitable method of costing for the biscuits is:', ['Batch costing', 'Contract costing', 'Single costing', 'Operating costing'], 0,
                    'Biscuits are identical items produced in lots of 10,000 packets, so each batch is the cost unit — batch costing, an extension of job costing. Contract costing is for large site projects; operating costing is for services such as the delivery fleet. In practice: cost per packet = batch cost ÷ packets in the batch.', 'core', topic=T10),
                  M('k1b', 'The variable power cost per machine hour is:', ['₹30', '₹48', '₹41.25', '₹36'], 0,
                    'Variable cost per hour = (1,32,000 − 96,000) ÷ (3,200 − 2,000) = 36,000 ÷ 1,200 = ₹30. ₹48 is 96,000 ÷ 2,000, which wrongly includes fixed cost; ₹41.25 is 1,32,000 ÷ 3,200. In practice: the fixed part, 96,000 − 60,000 = ₹36,000, is budgeted separately.', 'moderate', check='(132000-96000)/(3200-2000)', topic=T8),
                  M('k1c', 'For the make-or-buy decision on packaging, the ₹5,00,000 already spent on the machine is:', ['A sunk cost — irrelevant', 'A relevant cost', 'An opportunity cost', 'An out-of-pocket cost'], 0,
                    'The money has already been spent and the decision cannot change it, so it is a sunk cost and irrelevant. Only future costs that differ between making and buying matter. In practice: any resale value of the machine, however, is relevant as an opportunity cost.', 'core', topic=T9),
                  M('k1d', 'The delivery fleet would best be costed using:', ['Operating (service) costing with a cost unit like tonne-km', 'Process costing', 'Batch costing per packet', 'Uniform costing only'], 0,
                    'A transport service is costed by operating or service costing, using a composite unit such as tonne-kilometre. Process and batch costing apply to manufacturing; uniform costing is a technique for industry-wide comparison. In practice: cost per tonne-km lets Saral compare its own fleet with outsourced transport.', 'moderate', topic=T10),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch01', 1, 'Introduction to Cost and Management Accounting',
                ['Explain cost, costing, cost accounting, cost accountancy and management accounting.',
                 'Distinguish cost control from cost reduction, and cost, management and financial accounting.',
                 'Describe the essentials and installation of a costing system, including digital costing.',
                 'Identify cost objects, units, drivers and the types of responsibility centres.',
                 'Classify costs and segregate semi-variable costs by the high-low and least squares methods; distinguish methods from techniques of costing.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': [],
                 'exam_tip': 'Theory questions on cost control vs reduction, responsibility centres and installation of a costing system are frequent; MCQs test cost units, cost classification and high-low arithmetic.'},
                concepts, illustrations, jobs, mcqs, questions,
                {'summary': ['Costing = ascertaining cost; cost accounting records and reports; cost accountancy applies them to control and decisions.', 'Objectives: ascertain cost, fix price, control, reduce, support decisions.',
                             'Control keeps to standards; reduction lowers them permanently without hurting quality.', 'Good system: tailor-made, simple, economical, accepted, reconcilable; install after studying the business.',
                             'Cost object, cost unit (e.g. per tonne, kWh, patient-day), cost driver (e.g. number of orders).', 'Responsibility centres: cost (standard/discretionary), revenue, profit, investment.',
                             'Classification: nature, function, behaviour, controllability, normality, decision-making.', 'Semi-variable split: graphical, high-low, analytical, comparison, least squares (best).',
                             'Methods: single, job, batch, contract, process, operating, multiple. Techniques: uniform, marginal, standard, historical, absorption.'],
                 'remember': ['High-low: VC = Δcost ÷ Δactivity.', 'Least squares: m = (nΣxy − ΣxΣy)/(nΣx² − (Σx)²); c = (Σy − mΣx)/n.', 'Abnormal costs → Costing P&L, not product cost.'],
                 'traps': ['Sunk cost is never relevant.', 'Techniques work with any method.', 'Fixed cost per unit falls as output rises.']},
                [('Prime cost', 'Direct material + direct employee cost + direct expenses'), ('High-low', 'VC per unit = Δ total cost ÷ Δ activity'),
                 ('Least squares', 'y = mx + c'), ('Responsibility centres', 'Cost · Revenue · Profit · Investment'),
                 ('Methods', 'Single · Job · Batch · Contract · Process · Operating · Multiple'), ('Techniques', 'Uniform · Marginal · Standard · Historical · Absorption')],
                viva, cases,
                topics=['Introduction', 'Objectives of Cost Accounting', 'Scope of Cost Accounting', 'Relationship with Management and Financial Accounting', 'Essentials of a Good Cost Accounting System',
                        'Installation of Costing System', 'Cost Objects', 'Responsibility Centres', 'Limitations of Cost Accounting', 'Classification of Costs', 'Methods of Costing', 'Techniques of Costing'])
