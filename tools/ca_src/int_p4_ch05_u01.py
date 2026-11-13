"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 5 Activity Based Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch05-u01'
T1 = 'Why ABC developed and where it suits'
T2 = 'Meaning and terms: activities, cost pools, cost drivers'
T3 = 'Traditional costing versus ABC'
T4 = 'Cost hierarchy (unit, batch, product, facility)'
T5 = 'Stages of ABC'
T6 = 'Advantages, limitations and implementation'
T7 = 'Activity Based Management and Activity Based Budgeting'


def build():
    # i1 — traditional versus ABC
    ck = Checks()
    trad = ck.add('600000/12000', 'Traditional rate per machine hour')
    r_mach = ck.add('360000/12000', 'Machining: rate per machine hour')
    r_set = ck.add('120000/40', 'Set-ups: rate per set-up')
    r_po = ck.add('80000/80', 'Purchasing: rate per order')
    r_ins = ck.add('40000/100', 'Inspection: rate per inspection')
    a_tot = ck.add('10000*30+10*3000+20*1000+30*400', 'Alpha: overheads under ABC')
    b_tot = ck.add('2000*30+30*3000+60*1000+70*400', 'Beta: overheads under ABC')
    a_u = ck.add('362000/10000', 'Alpha: overhead per unit (ABC)')
    b_u = ck.add('238000/2000', 'Beta: overhead per unit (ABC)')
    i1 = {'id': 'i1', 'title': 'The low-volume product was being subsidised', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Sona Ceramics makes Alpha (10,000 units) and Beta (2,000 units); each unit needs 1 machine hour. Overheads: machining ₹3,60,000; set-ups ₹1,20,000 (Alpha 10, Beta 30 set-ups); purchasing ₹80,000 (Alpha 20, Beta 60 orders); inspection ₹40,000 (Alpha 30, Beta 70 inspections). Compute overhead per unit under a single machine hour rate and under ABC.',
          'solution': [table(['Activity (driver)', 'Cost ₹', 'Driver volume', 'Rate ₹'], [
              ['Machining (machine hours)', inr(360000), '12,000', inr(r_mach)],
              ['Set-ups (number of set-ups)', inr(120000), '40', inr(r_set)],
              ['Purchasing (orders)', inr(80000), '80', inr(r_po)],
              ['Inspection (inspections)', inr(40000), '100', inr(r_ins)]], title='Activity rates'),
              table(['Product', 'Machining', 'Set-ups', 'Purchasing', 'Inspection', 'Total ₹', 'Per unit ₹'], [
                  ['Alpha', inr(300000), inr(30000), inr(20000), inr(12000), inr(a_tot), inr(a_u)],
                  ['Beta', inr(60000), inr(90000), inr(60000), inr(28000), inr(b_tot), inr(b_u)]], title='Overheads under ABC'),
              p(f'Traditional: 6,00,000 ÷ 12,000 = ₹{inr(trad)} per hour, so both products carry ₹{inr(trad)} a unit. ABC shows Alpha really costs ₹{inr(a_u)} and Beta ₹{inr(b_u)} — the volume-based rate made the high-volume product carry the batch costs of the low-volume one.')],
          'checks': list(ck)}

    # i2 — activity based budgeting
    ck2 = Checks()
    budget = ck2.add('45*3000+90*1000+110*400', 'Budget for batch-level support activities')
    i2 = {'id': 'i2', 'title': 'Turning ABC around: an activity based budget', 'difficulty': 'core', 'minutes': 5,
          'q': 'Using the activity rates of Sona Ceramics (set-up ₹3,000, order ₹1,000, inspection ₹400), next year\'s plan needs 45 set-ups, 90 purchase orders and 110 inspections. Prepare the budget for these three activities and state what management should watch.',
          'solution': [table(['Activity', 'Planned volume', 'Rate ₹', 'Budget ₹'], [
              ['Set-ups', '45', inr(3000), inr(135000)],
              ['Purchase orders', '90', inr(1000), inr(90000)],
              ['Inspections', '110', inr(400), inr(44000)],
              ['Total', '', '', inr(budget)]], title='Activity based budget'),
              p('ABB starts from the work to be done (type and quantity) and costs it at activity rates. Management can now question the volume of each activity — for example, larger batches would cut set-ups and orders — instead of simply adding a percentage to last year\'s overheads.')],
          'checks': list(ck2)}

    hier = table(['Level', 'Cost varies with', 'Examples', 'Typical driver'], [
        ['Unit level', 'Each unit produced', 'Power for machines, indirect consumables', 'Machine hours, units'],
        ['Batch level', 'Number of batches', 'Machine set-ups, purchase orders, batch inspection', 'Number of set-ups/orders'],
        ['Product level', 'Each product line', 'Product design, engineering changes, maintaining specifications', 'Number of products, design changes'],
        ['Facility level', 'Sustaining the whole plant', 'Factory rent, security, plant management', 'Floor area, or not traced']],
        title='Cost hierarchy')
    vs = table(['Point', 'Traditional absorption', 'ABC'], [
        ['Cost pools', 'Few departments or cost centres', 'Many activities'],
        ['Bases', 'Volume-based (hours, units)', 'Cause-based cost drivers, including non-volume drivers'],
        ['Accuracy for diverse products', 'Low — high-volume products over-costed', 'High'],
        ['Cost of system', 'Low', 'Higher']], title='Traditional versus ABC')

    concepts = [
        C('c1', T1, [
            'ABC grew because overheads became a larger share of cost with automation, competition demanded accurate costs, product ranges widened, and information processing became cheap.',
            'It suits firms with high overheads, many diverse products, significant non-volume activities (set-ups, inspection, material handling), stiff competition and where traditional costs give misleading results.'],
          'When overheads are a big slice of the pie, the way you slice them decides which product looks profitable.',
          'A firm making hundreds of small custom batches benefits most from ABC.'),
        C('c2', T2, [
            'ABC assigns overheads to activities first, then to cost objects according to how much of each activity they consume.',
            'Terms: activity — an event or task that consumes resources; cost object — anything for which cost is measured (product, customer, service); cost pool — the overhead collected for one activity; resource cost driver — the measure used to assign resources to activities; activity cost driver — the measure of an activity\'s output used to charge cost objects (e.g. number of set-ups).'],
          'Products consume activities; activities consume resources.',
          'Purchasing cost is charged per purchase order, not per machine hour.'),
        C('c3', T3, [
            'Traditional systems use a few volume-based rates; high-volume, simple products then carry costs actually caused by low-volume, complex products.',
            'ABC uses many activity pools and cause-based drivers, giving more accurate product costs, especially where batch and product-level costs are large.'],
          'A single rate is like splitting a restaurant bill equally — fair only if everyone ate the same.',
          'Dropping a "loss-making" mass product on traditional numbers could be a costly mistake.',
          blocks=[vs]),
        C('c4', T4, [
            'Activities are grouped by level: unit, batch, product (product-sustaining) and facility (facility-sustaining) — a classification first set out by Cooper.',
            'Batch costs are fixed for every unit within a batch; product-level costs support a product line regardless of volume; facility costs cannot be traced to products easily and are often treated as period costs.'],
          'Ask: does this cost move with units, with batches, with product lines, or with keeping the factory open?',
          'Machine set-up cost is the same whether the batch has 100 or 1,000 units.',
          blocks=[hier]),
        C('c5', T5, [
            'Stages: (1) identify activities (a manageable number, often 20–40 in practice); (2) assign overheads to activity cost pools using resource drivers; (3) spread support activities over primary activities; (4) choose an activity cost driver for each primary activity; (5) compute the rate per unit of driver; (6) charge cost objects according to their use of each driver.'],
          'Trace the money: resource → activity → product.',
          'Inspection cost ₹40,000 ÷ 100 inspections = ₹400 per inspection charged to each product.'),
        C('c6', T6, [
            'Advantages: more accurate costs; logical overhead assignment; better pricing; unit costs for decisions; highlights non-value-added activities; useful for multi-product firms; spotlights problem areas.',
            'Limitations: costly to set up and run; less useful for small or single-product firms; choosing drivers can be difficult.',
            'Implementation: staff training, process specification through interviews, clear activity definitions, driver selection, and assigning costs with a representative driver per pool.'],
          'Better information costs money; ABC pays off where costing errors are expensive.',
          'A single-product cement plant gains little from ABC.'),
        C('c7', T7, [
            'ABC as a decision tool: pricing, product mix, make-or-buy, customer profitability.',
            'Activity Based Management (ABM) uses ABC information to manage activities: cost driver analysis, activity analysis (value-added activities that customers pay for versus non-value-added ones like moving, waiting, rework), and performance analysis. Uses include cost reduction, business process re-engineering, benchmarking and performance measurement.',
            'Activity Based Budgeting (ABB) reverses ABC: decide the type and quantity of work and cost it at activity rates. It improves forecast accuracy, links budgets to workload and highlights excess resources.'],
          'ABC tells you what things cost; ABM and ABB tell you what to do about it.',
          'Cutting the number of material moves between shops removes a non-value-added activity.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Product profitability review', 'role': 'Cost analyst',
         'situation': 'Sales want to drop a high-volume product that looks unprofitable.',
         'steps': ['Map main activities and collect their costs.', 'Choose drivers and compute activity rates.', 'Recost each product and compare with traditional figures.', 'Recommend on pricing and product mix.'],
         'takeaway': 'Check costs with ABC before dropping a product.'},
        {'id': 'j2', 'title': 'Cost reduction drive', 'role': 'Operations accountant',
         'situation': 'The plant wants to cut overheads by 10%.',
         'steps': ['List activities and classify value-added or not.', 'Find drivers of non-value-added work (moves, waits, rework).', 'Propose changes (larger batches, layout) and budget the new activity levels.'],
         'takeaway': 'Cut the work, not just the budget line.'},
    ]

    mcqs = [
        Q('m1', 'Under ABC, overheads are first traced to:', ['Activities', 'Products', 'Departments only', 'Customers'], 0,
          'ABC collects overheads in activity cost pools using resource drivers and only then charges products and other cost objects using activity drivers. Traditional systems go via departments. In practice: products consume activities, activities consume resources.', 'c2', T2),
        Q('m2', 'Machine set-up cost is an example of a:', ['Batch-level activity', 'Unit-level activity', 'Product-level activity', 'Facility-level activity'], 0,
          'A set-up is performed once for each batch, so its cost varies with the number of batches, not with units within a batch. Unit-level costs vary with each unit; product-level costs support a line; facility costs sustain the plant. In practice: larger batches reduce set-up cost per unit.', 'c4', T4),
        Q('m3', 'Plant security and factory rent are:', ['Facility-level costs', 'Batch-level costs', 'Unit-level costs', 'Product-level costs'], 0,
          'They sustain the whole facility and do not vary with units, batches or product lines, so they are facility-sustaining costs, often treated as period costs or apportioned on a broad basis. In practice: avoid over-precise tracing of such costs.', 'c4', T4),
        Q('m4', 'Purchasing costs ₹1,50,000; 300 purchase orders; Product P uses 45 orders. ABC charges P:', ['₹22,500', '₹15,000', '₹45,000', '₹30,000'], 0,
          'Rate = 1,50,000 ÷ 300 = ₹500 per order; P is charged 45 × 500 = ₹22,500. A machine-hour rate would ignore how many orders P actually needs. In practice: driver volumes come from operational records.', 'c5', T5, 'core', check=22500),
        Q('m5', 'Under traditional volume-based absorption, compared with ABC, high-volume simple products are usually:', ['Over-costed', 'Under-costed', 'Correctly costed', 'Not costed'], 0,
          'Volume-based rates spread batch and product-level costs in proportion to volume, so high-volume products absorb costs actually caused by low-volume, complex products. ABC corrects this cross-subsidy. In practice: low-volume specialties often look more profitable than they are.', 'c3', T3, 'moderate'),
        Q('m6', 'Which is a limitation of ABC?', ['It is expensive to set up and maintain', 'It ignores overheads', 'It cannot be used for services', 'It uses only one cost pool'], 0,
          'ABC needs detailed activity analysis and data collection, which costs time and money and may not pay off for small or single-product firms. Selecting drivers can also be difficult. It works well for services too. In practice: weigh benefit against cost.', 'c6', T6),
        Q('m7', 'Moving materials between distant shops is generally a:', ['Non-value-added activity', 'Value-added activity', 'Unit-level driver', 'Facility cost driver'], 0,
          'Customers do not pay more because materials travel further; such moves add cost but no value, so ABM targets them for reduction through layout changes. Polishing a product the customer values is value-added. In practice: waiting, rework and storage are similar.', 'c7', T7),
        Q('m8', 'Activity Based Budgeting is built on:', ['Type, quantity and cost of work to be done', 'Last year\'s budget plus inflation', 'Sales value only', 'Machine hours only'], 0,
          'ABB estimates the activities required for planned output, their volumes, and their cost at activity rates — the reverse of ABC. Incremental budgeting simply adds a percentage. In practice: it highlights surplus resources.', 'c7', T7),
        Q('m9', 'ABC is LEAST useful for:', ['A single-product firm with low overheads', 'A firm with many diverse products', 'A firm with large set-up costs', 'A firm facing stiff competition'], 0,
          'With one product all overheads go to that product anyway, and low overheads make the extra cost of ABC hard to justify. Diversity, large batch costs and competition are exactly where ABC helps. In practice: match the system to complexity.', 'c1', T1),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Traditional rate', 1, 'computation', 'machine hour|traditional', nums=[trad]),
           S('s2', 'Activity rates', 2, 'computation', 'rate', nums=[r_mach, r_set, r_po, r_ins]),
           S('s3', 'ABC totals', 2.5, 'computation', 'alpha', nums=[a_tot, b_tot]),
           S('s4', 'Per unit and comment', 2.5, 'computation', 'per unit|subsid', nums=[a_u, b_u])],
          ['Compute rates before charging products.'], ['Charging set-ups by machine hours.'], ['Two tables + comment.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Budget lines', 2, 'computation', 'set-up|order', nums=[budget]),
           S('s2', 'Control point', 1, 'concept', 'volume|batch|resources')],
          ['Start from activity volumes.'], ['Adding inflation to last year instead.'], ['Table + note.'], pad='table', checks=list(ck2)),
        W('q3', 4, 'Explain the cost hierarchy used in ABC with one example of each level.',
          [table(['Level', 'Meaning', 'Example'], [
              ['Unit level', 'Cost rises with every unit made', 'Machine power, indirect consumables'],
              ['Batch level', 'Cost incurred per batch, common to units in it', 'Machine set-up, purchase order'],
              ['Product level', 'Cost of supporting a product line', 'Product design, engineering changes'],
              ['Facility level', 'Cost of sustaining the plant', 'Factory rent, plant security']])],
          [S('s1', 'Unit', 1, 'concept', 'unit'), S('s2', 'Batch', 1, 'concept', 'batch'),
           S('s3', 'Product', 1, 'concept', 'product'), S('s4', 'Facility', 1, 'concept', 'facility')],
          ['One line each.'], ['Calling set-up a unit-level cost.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is a cost driver in ABC?',
          'A factor that causes the cost of an activity to change; the activity driver measures how much of the activity each product uses, such as each machine set-up or purchase order.',
          [P('p1', 'Causes cost', 6, 'cause'), P('p2', 'Example', 4, 'set-up|order|inspection')], 'c2'),
        V('v2', 'Why do traditional systems distort product costs?',
          'They spread all overheads on volume-based rates, so high-volume products absorb batch and product-level costs caused by low-volume products.',
          [P('p1', 'Volume-based rates', 5, 'volume'), P('p2', 'Cross-subsidy', 5, 'high-volume|low-volume|subsid')], 'c3'),
        V('v3', 'What is Activity Based Management?',
          'Using ABC information to manage activities efficiently, for example by reducing non-value-added work, re-engineering processes and benchmarking.',
          [P('p1', 'Uses ABC information', 4, 'abc'), P('p2', 'Manage activities / cut NVA', 6, 'non-value|reduc|re-engineer|benchmark')], 'c7'),
        V('v4', 'Name two situations where ABC is most useful.',
          'Where overheads form a large share of cost and where the firm makes many diverse products with significant set-up or handling activity.',
          [P('p1', 'High overheads', 5, 'high overhead|large share|overhead'), P('p2', 'Diverse products', 5, 'diverse|many products|multiple')], 'c1'),
        V('v5', 'What are the key elements of activity based budgeting?',
          'The type of work to be done, the quantity of that work and the cost of doing it.',
          [P('p1', 'Type of work', 3, 'type'), P('p2', 'Quantity', 4, 'quantity'), P('p3', 'Cost', 3, 'cost')], 'c7'),
    ]

    cases = [{'id': 'k1', 'title': 'Kesar Packaging', 'difficulty': 'moderate',
              'case': 'Kesar Packaging makes standard cartons (50,000 units, 5 batches) and printed gift boxes (5,000 units, 45 batches). Set-up costs total ₹2,50,000; all other overheads are absorbed on machine hours. Each product uses 1 machine minute per unit.',
              'mcqs': [
                  M('k1a', 'Set-up cost per batch is:', ['₹5,000', '₹50,000', '₹4,545', '₹2,500'], 0,
                    'There are 5 + 45 = 50 batches; rate = 2,50,000 ÷ 50 = ₹5,000 per set-up. This is a batch-level activity rate. In practice: the number of batches, not units, drives it.', 'core', check=5000, topic=T5),
                  M('k1b', 'Set-up cost per gift box under ABC is:', ['₹45', '₹4.55', '₹5', '₹50'], 0,
                    'Gift boxes take 45 batches × ₹5,000 = ₹2,25,000, spread over 5,000 units = ₹45 per box. Under a machine-minute basis they would bear only about ₹4.55 each. In practice: small custom runs carry heavy set-up cost.', 'moderate', check=45, topic=T3),
                  M('k1c', 'Under machine-minute absorption, set-up cost per standard carton would be about:', ['₹4.55', '₹0.50', '₹5', '₹45'], 0,
                    'Total machine minutes = 55,000; rate = 2,50,000 ÷ 55,000 ≈ ₹4.55 per minute, so each carton bears about ₹4.55, against only ₹0.50 under ABC (5 × 5,000 ÷ 50,000). Cartons subsidise gift boxes. In practice: this misprices both lines.', 'hard', check=4.55, topic=T3),
                  M('k1d', 'A sensible ABM action is to:', ['Increase gift box batch sizes or charge set-up fees', 'Absorb set-ups on labour hours', 'Stop making cartons', 'Ignore set-up costs'], 0,
                    'Set-up cost is driven by the number of batches, so larger batches or a separate set-up charge to customers tackles the driver directly. Changing the absorption base does not reduce cost. In practice: manage the driver, not the allocation.', 'moderate', topic=T7),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch05', 1, 'Activity Based Costing',
                ['Explain why ABC developed and where it suits.',
                 'Define activities, cost pools, cost objects and cost drivers.',
                 'Compare ABC with traditional absorption and apply the cost hierarchy.',
                 'Compute product costs using ABC stages.',
                 'Explain advantages, limitations, implementation, ABM and ABB.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['int-p4-ch04-u01'],
                 'exam_tip': 'Expect a two- or three-product ABC computation compared with a single-rate result, plus theory on cost hierarchy, ABM (value-added vs non-value-added) and ABB.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['ABC: resources → activities → cost objects.', 'Cost pool per activity; driver per pool; rate = pool ÷ driver volume.',
                             'Hierarchy: unit, batch, product, facility.', 'Traditional volume rates over-cost high-volume products.',
                             'ABM: value-added vs non-value-added; ABB: type, quantity, cost of work.'],
                 'remember': ['Set-ups and orders are batch-level.', 'Facility costs are hard to trace.'],
                 'traps': ['ABC is not cost-free.', 'Changing the base does not reduce cost.']},
                [('Activity rate', 'Pool ÷ driver volume'), ('Set-up', 'Batch level'), ('Design', 'Product level'), ('Rent', 'Facility level')],
                viva, cases,
                topics=['Introduction', 'Meaning and Definition', 'Meaning of Terms Used in ABC', 'Cost Allocation under ABC', 'Traditional Absorption Costing and ABC',
                        'Level of Activities under ABC Methodology', 'Stages in Activity Based Costing', 'Advantages of Activity Based Costing', 'Limitations of Activity Based Costing',
                        'Requirements in ABC Implementation', 'Practical Applications of Activity Based Costing'])
