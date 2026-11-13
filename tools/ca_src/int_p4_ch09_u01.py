"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 9 Job Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch09-u01'
T1 = 'Meaning, suitability and process of job costing'
T2 = 'Job cost card and pricing a job'
T3 = 'Work-in-progress, spoilage and defectives in jobs'


def build():
    ck = Checks()
    mat = ck.add('62000-4000', 'Materials net of returns')
    lab = ck.add('120*150 + 40*150*1.5', 'Direct labour including overtime premium at the job\'s request')
    foh = ck.add('160*90', 'Factory overheads at ₹90 per labour hour')
    works = ck.add('58000+27000+14400+3000', 'Works cost')
    adm = ck.add('102400*10/100', 'Administration overheads at 10% of works cost')
    tot = ck.add('102400+10240', 'Total cost')
    price = ck.add('112640/0.8', 'Price for 20% profit on selling price')
    i1 = {'id': 'i1', 'title': 'Costing and pricing a custom order', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Job J-41 (a special conveyor for a client) required: materials issued ₹62,000, of which ₹4,000 was returned to stores; 120 normal labour hours and 40 overtime hours at ₹150 per hour, overtime at 150% being worked at the client\'s request for urgent delivery; direct expenses (hire of a crane) ₹3,000. Factory overheads are absorbed at ₹90 per labour hour; administration overheads at 10% of works cost. Prepare the job cost sheet and quote a price giving 20% profit on selling price.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Direct materials', '62,000 − 4,000 returned', inr(mat)],
              ['Direct labour', '120 × 150 + 40 × 225 (premium charged to job as requested by client)', inr(lab)],
              ['Direct expenses', 'Crane hire', inr(3000)],
              ['Factory overheads', '160 hours × ₹90', inr(foh)],
              ['Works cost', '', inr(works)],
              ['Administration overheads', '10% of works cost', inr(adm)],
              ['Total cost', '', inr(tot)],
              ['Price', 'Cost ÷ 80%', inr(price)]], title='Job cost sheet — J-41'),
              note('Overtime premium is charged to the job only when overtime is worked at the customer\'s request; otherwise it is a production overhead.')],
          'checks': list(ck)}

    ck2 = Checks()
    norm = ck2.add('500*30', 'Normal spoilage cost absorbed by good units (stays in job)')
    ab = ck2.add('200*30-1200', 'Abnormal spoilage loss to Costing P&L (net of scrap)')
    i2 = {'id': 'i2', 'title': 'Spoiled units in a job', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A job of 10,000 identical components costing ₹30 each to the point of inspection had 700 spoiled units. Normal spoilage is 5% of input. Abnormal spoiled units realise ₹1,200 as scrap. How are normal and abnormal spoilage treated?',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Normal spoilage (500 units)', 'Cost borne by good units in the job', inr(norm)],
              ['Abnormal spoilage (200 units)', 'Cost less scrap transferred to Costing P&L', inr(ab)]], title='Spoilage in job costing')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Job costing collects costs for each customer order (job) separately, because each job differs in specification, materials and time. It suits printing, furniture, repair workshops, interior decoration, machine tools and ship-building.',
            'Process: a production order (job number) is issued; materials are drawn by requisitions quoting the job number; labour is booked by job time cards; overheads are absorbed at predetermined rates; on completion, the job cost card is totalled and compared with the price.',
            'Work-in-progress at any date is the total of costs on all incomplete job cards.'],
          'Every job carries its own cost card, like a patient file in a hospital.',
          'A printer quoting for 500 wedding cards opens job no. 2207 and charges paper, printing hours and binding to it.'),
        C('c2', T2, [
            'The job cost card records direct materials (net of returns and transfers to other jobs), direct labour (hours × rate), direct expenses and overheads absorbed, often with an estimate column for comparison.',
            'Overtime premium is charged to the job only if overtime was at the customer\'s request; otherwise it is an overhead. Idle time and normal losses are overheads.',
            'Price is set by adding the desired profit: profit on cost (cost × (1 + markup)) or profit on selling price (cost ÷ (1 − margin)).'],
          'Get the cost right first; the price follows from the profit rule chosen.',
          'Cost ₹80,000 with 20% profit on cost gives ₹96,000; with 20% on sale price, ₹1,00,000.'),
        C('c3', T3, [
            'Normal spoilage in a job is absorbed by good units, raising their cost; if the job is for a customer who specified tolerances, its cost stays in the job.',
            'Abnormal spoilage is charged, after crediting scrap, to the Costing Profit and Loss Account.',
            'Defectives that can be rectified: normal rectification cost goes to the job (if specific) or to production overheads; abnormal rectification cost goes to Costing P&L.'],
          'Expected losses belong to the product; unexpected ones belong to the period.',
          'If a machine fault ruins 50 units in a job, their cost is written off, not loaded on the customer.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Tender pricing', 'role': 'Cost accountant trainee',
             'situation': 'Sales wants a quote for a non-standard machine in two days.',
             'steps': ['Estimate materials from the drawing.', 'Estimate labour hours by department.', 'Apply overhead rates.', 'Add profit on the required basis and check competitiveness.'],
             'takeaway': 'A good quotation starts with a realistic estimated job cost card.'}]

    mcqs = [
        Q('m1', 'Job costing is suitable where:', ['Each order is different and done to customer specification', 'Output is homogeneous and continuous', 'Products pass through processes', 'Services are standardised'], 0,
          'Job costing traces costs to individual orders that differ. In practice: printing and repair shops use it.', 'c1', T1),
        Q('m2', 'Overtime premium paid because of a customer\'s urgent request is:', ['Charged to that job', 'Treated as factory overhead', 'Written off to Costing P&L', 'Ignored'], 0,
          'When the customer causes the overtime, the job bears it. General overtime is an overhead. In practice: document the request.', 'c2', T2),
        Q('m3', 'Cost ₹60,000; profit 25% on selling price. Price:', ['₹80,000', '₹75,000', '₹85,000', '₹72,000'], 0,
          '60,000 ÷ 0.75 = 80,000. In practice: 25% on cost would give ₹75,000.', 'c2', T2, 'moderate', check=80000),
        Q('m4', 'Abnormal spoilage in a job is charged to:', ['Costing Profit and Loss Account', 'The job', 'Factory overheads', 'Customer'], 0,
          'Abnormal losses are not part of product cost; net of scrap they go to Costing P&L. In practice: investigate their cause.', 'c3', T3),
        Q('m5', 'Work-in-progress in job costing equals:', ['Total cost on incomplete job cards', 'Materials in stores', 'Cost of completed jobs', 'Overheads under-absorbed'], 0,
          'All costs booked to jobs not yet finished make up WIP. In practice: reconcile with WIP control.', 'c1', T1),
        Q('m6', 'Materials returned from a job to stores are:', ['Deducted from the job\'s material cost', 'Added to overheads', 'Ignored', 'Charged to another job automatically'], 0,
          'Returns reduce the job\'s material cost via a material return note. In practice: transfers to other jobs use a transfer note.', 'c2', T2),
        Q('m7', 'Normal rectification cost of defectives in a general production job is treated as:', ['Production overhead', 'Abnormal loss', 'Selling cost', 'Capital expenditure'], 0,
          'Where defects are normal and not job-specific, rectification is spread through overheads. In practice: job-specific rectification goes to that job.', 'c3', T3),
        Q('m8', 'Labour cost is booked to jobs using:', ['Job time cards', 'Material requisitions', 'Bin cards', 'Goods received notes'], 0,
          'Job time cards record hours worked on each job. In practice: idle time is booked separately.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Materials', 1, 'computation', 'material', nums=[mat]), S('s2', 'Labour with premium', 2, 'computation', 'overtime', nums=[lab]),
           S('s3', 'Overheads and works cost', 1, 'computation', 'works', nums=[works]), S('s4', 'Total cost and price', 2, 'computation', 'price', nums=[tot, price])],
          ['Show hours separately.'], ['Pricing 20% on cost instead of sale price.'], ['Cost sheet.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Normal spoilage', 1, 'computation', 'normal', nums=[norm]), S('s2', 'Abnormal spoilage', 2, 'computation', 'abnormal', nums=[ab])],
          ['Apply the normal rate to input.'], ['Charging all spoilage to P&L.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is job costing?', 'A specific order costing method in which costs are collected for each job or work order separately, as each differs from the others.',
          [P('p1', 'Each job separately', 6, 'each job|separate'), P('p2', 'Specific order', 4, 'order|customer')], 'c1'),
        V('v2', 'What documents feed a job cost card?', 'Material requisitions and return notes, job time cards and overhead absorption rates.',
          [P('p1', 'Materials', 5, 'requisition'), P('p2', 'Labour', 5, 'time card')], 'c1'),
        V('v3', 'How is overtime premium treated?', 'Charged to the job if worked at the customer\'s request; otherwise treated as production overhead.',
          [P('p1', 'Customer request', 5, 'customer'), P('p2', 'Overhead otherwise', 5, 'overhead')], 'c2'),
        V('v4', 'How is abnormal spoilage treated?', 'Its cost, less scrap value, is transferred to the Costing Profit and Loss Account.',
          [P('p1', 'Costing P&L', 6, 'profit and loss'), P('p2', 'Scrap credited', 4, 'scrap')], 'c3'),
        V('v5', 'Give examples of job costing industries.', 'Printing, furniture making, repair workshops, interior decoration and heavy engineering.',
          [P('p1', 'Printing or furniture', 5, 'printing|furniture'), P('p2', 'Repairs or engineering', 5, 'repair|engineering|interior')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Fine Prints', 'difficulty': 'moderate',
              'case': 'Fine Prints accepts job P-88: 1,000 brochures. Paper ₹18,000; ink ₹2,000; 30 labour hours at ₹200; machine overheads at ₹300 per machine hour for 12 hours; office overheads 20% of works cost. It wants 25% profit on cost.',
              'mcqs': [
                  M('k1a', 'Prime cost:', ['₹26,000', '₹20,000', '₹29,600', '₹32,000'], 0,
                    'Paper 18,000 + ink 2,000 + labour 6,000 = 26,000. In practice: ink is a direct material here.', 'core', check=26000, topic=T2),
                  M('k1b', 'Works cost:', ['₹29,600', '₹26,000', '₹35,520', '₹32,000'], 0,
                    '26,000 + 12 × 300 = 29,600. In practice: machine-hour rate suits printing.', 'core', check=29600, topic=T2),
                  M('k1c', 'Total cost:', ['₹35,520', '₹29,600', '₹37,000', '₹44,400'], 0,
                    '29,600 × 1.20 = 35,520. In practice: office overhead on works cost.', 'moderate', check=35520, topic=T2),
                  M('k1d', 'Quoted price:', ['₹44,400', '₹47,360', '₹42,624', '₹35,520'], 0,
                    '35,520 × 1.25 = 44,400 (25% on cost). In practice: per brochure ₹44.40.', 'moderate', check=44400, topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch09', 1, 'Job Costing',
                ['Explain the features and process of job costing.',
                 'Prepare a job cost card and price a job.',
                 'Treat spoilage and defectives in jobs.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 35}, 'prereq': ['int-p4-ch08-u01'],
                 'exam_tip': 'Read the profit basis carefully: "on cost" multiplies, "on selling price" divides.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Job costing: costs per order; job cost card.',
                             'Overtime premium to job only if customer requested.',
                             'Normal spoilage in job cost; abnormal to Costing P&L.',
                             'Price: cost × (1 + markup) or cost ÷ (1 − margin).'],
                 'remember': ['WIP = cost on incomplete job cards.'],
                 'traps': ['Material returns reduce job cost.']},
                [('Profit on cost', 'Cost × (1 + m)'), ('Profit on sale', 'Cost ÷ (1 − m)'), ('Abnormal loss', 'Costing P&L')],
                viva, cases)
