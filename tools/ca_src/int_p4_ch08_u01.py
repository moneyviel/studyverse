"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 8 Unit & Batch Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch08-u01'
T1 = 'Unit (output/single) costing'
T2 = 'Batch costing and economic batch quantity'


def build():
    ck = Checks()
    prime = ck.add('480000+320000+40000', 'Prime cost')
    works = ck.add('840000+200000', 'Works cost')
    cop = ck.add('1040000+80000', 'Cost of production')
    cos = ck.add('1120000+60000', 'Cost of sales')
    pu = ck.add('1180000/20000', 'Cost per unit')
    i1 = {'id': 'i1', 'title': 'Cost per brick', 'difficulty': 'core', 'minutes': 8,
          'q': 'Kiln Bricks produced and sold 20,000 units of a single product. Costs: direct materials ₹4,80,000; direct wages ₹3,20,000; direct expenses ₹40,000; factory overheads ₹2,00,000; administration overheads (production-related) ₹80,000; selling overheads ₹60,000. Prepare a cost sheet and find cost per unit.',
          'solution': [table(['Item', 'Total ₹', 'Per unit ₹'], [
              ['Prime cost', inr(prime), '42.00'],
              ['Factory overheads', inr(200000), '10.00'],
              ['Works cost', inr(works), '52.00'],
              ['Administration overheads', inr(80000), '4.00'],
              ['Cost of production', inr(cop), '56.00'],
              ['Selling overheads', inr(60000), '3.00'],
              ['Cost of sales', inr(cos), inr(pu)]], title='Unit cost sheet')],
          'checks': list(ck)}

    ck2 = Checks()
    ebq = ck2.add('(2*60000*1200/4)**0.5', 'Economic batch quantity')
    nb = ck2.add('60000/6000', 'Number of batches at EBQ')
    tc_ebq = ck2.add('10*1200 + 6000/2*4', 'Set-up + carrying cost at EBQ')
    tc_cur = ck2.add('20*1200 + 3000/2*4', 'Set-up + carrying cost at current batch of 3,000')
    sav = ck2.add('30000-24000', 'Annual saving')
    i2 = {'id': 'i2', 'title': 'How big should a batch be?', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'A toy maker needs 60,000 units a year. Each production set-up costs ₹1,200 and the carrying cost is ₹4 per unit per year. It currently produces in batches of 3,000. Compute the economic batch quantity and the annual saving from switching to it.',
          'solution': [table(['Item', 'Working', 'Value'], [
              ['EBQ', '√(2 × 60,000 × 1,200 ÷ 4)', inr(ebq) + ' units'],
              ['Batches at EBQ', '60,000 ÷ 6,000', str(int(nb))],
              ['Cost at EBQ', 'Set-up 10 × 1,200 + carrying 3,000 × 4', '₹' + inr(tc_ebq)],
              ['Cost at 3,000 per batch', 'Set-up 20 × 1,200 + carrying 1,500 × 4', '₹' + inr(tc_cur)],
              ['Saving', '', '₹' + inr(sav)]], title='Economic batch quantity'),
              note('At EBQ, total set-up cost equals total carrying cost — a quick check of the arithmetic.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Unit costing (output or single costing) suits industries producing one product, or a few grades of it, in a continuous flow — bricks, cement, sugar, mining, dairies.',
            'All costs for the period are collected and divided by the units produced to get cost per unit; a cost sheet shows prime cost, works cost, cost of production, cost of goods sold and cost of sales, each in total and per unit.',
            'Opening and closing finished stock and work-in-progress adjustments are made at the appropriate levels; a statement of profit follows from sales less cost of sales. Tenders and quotations are prepared from the cost sheet with expected changes in prices and volumes.'],
          'When every unit is alike, one division — total cost ÷ units — tells you what each costs.',
          'A dairy producing 5 lakh litres of milk at a total cost of ₹2 crore has a unit cost of ₹40 a litre.'),
        C('c2', T2, [
            'Batch costing treats a group of identical units made together as the cost unit; batch cost ÷ units in the batch gives unit cost. It suits medicines, toys, shoes, spare parts and readymade garments.',
            'Each batch gets a batch number; costs are collected on a batch cost sheet just as in job costing.',
            'Economic batch quantity balances set-up cost (falls as batches get bigger) and carrying cost (rises with batch size): EBQ = √(2DS ÷ C), where D is annual demand, S set-up cost per batch and C carrying cost per unit per year.'],
          'Batch costing is job costing for a group of identical items; EBQ is EOQ applied to production runs.',
          'A pharma firm making tablets in lots of 50,000 records each lot\'s costs separately and divides by good tablets produced.'),
        C('c3', 'Comparing unit, batch and job costing', [
            'Unit costing: continuous, identical output; cost per period ÷ units. Job costing: customer-specific orders; costs per job. Batch costing: identical items made in lots; costs per batch.',
            'All three are methods within the same cost accounting principles; the choice depends on how production is organised.',
            'Common errors: averaging costs across different products in unit costing, and ignoring set-up costs when deciding batch sizes.'],
          'Match the method to the production pattern — product, order or lot.',
          'A garment exporter making 2,000 identical shirts for one order may use batch costing within a job.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Batch size review', 'role': 'Cost accountant trainee',
             'situation': 'The production head runs small batches to keep stock low; set-up costs keep rising.',
             'steps': ['Estimate annual demand, set-up cost and carrying cost.', 'Compute EBQ.', 'Compare total cost at current size and at EBQ.', 'Recommend a size and number of runs.'],
             'takeaway': 'Smaller is not always cheaper — set-ups cost money too.'}]

    mcqs = [
        Q('m1', 'Unit costing is most suitable for:', ['A cement plant', 'A shipbuilder', 'An interior decorator', 'A printing press taking orders'], 0,
          'Single, homogeneous product in continuous production — cement — fits unit costing. The others are order-based. In practice: cost per tonne is the key figure.', 'c1', T1),
        Q('m2', 'In batch costing, the cost unit is:', ['A batch', 'A single item', 'A job', 'A process'], 0,
          'Costs are collected per batch and divided by units in it. In practice: each batch gets a number.', 'c2', T2),
        Q('m3', 'EBQ with D = 18,000, S = ₹400, C = ₹4:', ['1,897 units', '3,600 units', '1,200 units', '6,000 units'], 0,
          '√(2 × 18,000 × 400 ÷ 4) = √3,600,000 ≈ 1,897. In practice: round to a practical size.', 'c2', T2, 'moderate', check=1897),
        Q('m4', 'At EBQ:', ['Total set-up cost equals total carrying cost', 'Set-up cost is zero', 'Carrying cost is the highest', 'Batches are fewest possible'], 0,
          'The square-root formula minimises total cost where the two costs are equal. In practice: use this to check workings.', 'c2', T2),
        Q('m5', 'If set-up cost per batch rises, EBQ:', ['Increases', 'Decreases', 'Remains same', 'Becomes zero'], 0,
          'S is in the numerator, so higher set-up cost means larger, fewer batches. In practice: automation lowers S and EBQ.', 'c2', T2),
        Q('m6', 'Cost of sales in a unit cost sheet = cost of goods sold plus:', ['Selling and distribution overheads', 'Factory overheads', 'Direct materials', 'Administration overheads relating to production'], 0,
          'Selling and distribution overheads are added last. In practice: production-related administration is in cost of production.', 'c1', T1),
        Q('m7', 'Total cost ₹9,00,000 for 30,000 identical units; unit cost is:', ['₹30', '₹27', '₹33', '₹300'], 0,
          '₹9,00,000 ÷ 30,000 = ₹30. In practice: compare with selling price per unit.', 'c1', T1, check=30),
        Q('m8', 'Which industry typically uses batch costing?', ['Pharmaceuticals', 'Mining', 'Construction', 'Electricity generation'], 0,
          'Medicines are made in identical lots. Mining and power fit unit costing; construction fits contract costing. In practice: batch records support quality control too.', 'c3', 'Comparing unit, batch and job costing'),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Prime cost', 1, 'computation', 'prime', nums=[prime]), S('s2', 'Works cost', 1, 'computation', 'works', nums=[works]),
           S('s3', 'Cost of production', 1, 'computation', 'production', nums=[cop]), S('s4', 'Cost per unit', 2, 'computation', 'per unit', nums=[pu])],
          ['Show per-unit column.'], ['Adding selling overheads to cost of production.'], ['Cost sheet.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'EBQ', 2, 'computation', 'EBQ', nums=[ebq]), S('s2', 'Costs compared', 2, 'computation', 'set-up', nums=[tc_ebq, tc_cur]), S('s3', 'Saving', 1, 'computation', 'saving', nums=[sav])],
          ['Use average stock = batch ÷ 2.'], ['Using whole batch for carrying cost.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Where is unit costing used?', 'In industries producing a single homogeneous product continuously, such as cement, bricks, sugar and mining.',
          [P('p1', 'Single product', 5, 'single|homogeneous'), P('p2', 'Examples', 5, 'cement|brick|sugar|mining')], 'c1'),
        V('v2', 'What is batch costing?', 'A method where a lot of identical units is the cost unit; batch cost divided by units gives unit cost.',
          [P('p1', 'Lot as cost unit', 6, 'batch|lot'), P('p2', 'Divide by units', 4, 'divid|units')], 'c2'),
        V('v3', 'State the EBQ formula.', 'The square root of two times annual demand times set-up cost per batch, divided by carrying cost per unit per year.',
          [P('p1', 'Square root', 4, 'square root'), P('p2', 'Variables', 6, 'demand|set-up|carrying')], 'c2'),
        V('v4', 'Why does EBQ minimise cost?', 'Because larger batches cut set-up cost but raise carrying cost; EBQ is the size where their total is lowest, where the two are equal.',
          [P('p1', 'Trade-off', 5, 'set-up|carrying'), P('p2', 'Equal', 5, 'equal|lowest')], 'c2'),
        V('v5', 'What does a unit cost sheet show?', 'Prime cost, works cost, cost of production, cost of goods sold and cost of sales, in total and per unit.',
          [P('p1', 'Cost stages', 6, 'prime|works|production'), P('p2', 'Per unit', 4, 'per unit')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Glow Candles', 'difficulty': 'moderate',
              'case': 'Glow Candles makes scented candles in batches. Annual demand is 1,00,000 candles; set-up cost ₹2,000 per batch; carrying cost ₹1 per candle per year. It currently runs 50 batches a year.',
              'mcqs': [
                  M('k1a', 'Current batch size:', ['2,000 candles', '5,000 candles', '1,000 candles', '20,000 candles'], 0,
                    '1,00,000 ÷ 50 = 2,000. In practice: start from current practice.', 'core', check=2000, topic=T2),
                  M('k1b', 'EBQ:', ['20,000 candles', '10,000 candles', '14,142 candles', '2,000 candles'], 0,
                    '√(2 × 1,00,000 × 2,000 ÷ 1) = √400,000,000 = 20,000. In practice: 5 runs a year.', 'moderate', check=20000, topic=T2),
                  M('k1c', 'Total set-up + carrying cost at current size:', ['₹1,01,000', '₹20,000', '₹40,000', '₹1,00,000'], 0,
                    'Set-up 50 × 2,000 = 1,00,000; carrying 2,000 ÷ 2 × 1 = 1,000; total ₹1,01,000. In practice: set-up dominates.', 'moderate', check=101000, topic=T2),
                  M('k1d', 'Total cost at EBQ:', ['₹20,000', '₹10,000', '₹40,000', '₹1,01,000'], 0,
                    'Set-up 5 × 2,000 = 10,000; carrying 20,000 ÷ 2 × 1 = 10,000; total ₹20,000. In practice: saving of ₹81,000.', 'moderate', check=20000, topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch08', 1, 'Unit & Batch Costing',
                ['Prepare a unit cost sheet.',
                 'Apply batch costing and compute economic batch quantity.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 35}, 'prereq': ['int-p4-ch07-u01'],
                 'exam_tip': 'Always show total and per-unit columns; in EBQ, verify that set-up and carrying costs are equal.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Unit costing: total cost ÷ units for homogeneous output.',
                             'Batch costing: batch is the cost unit.',
                             'EBQ = √(2DS/C); at EBQ, set-up cost = carrying cost.'],
                 'remember': ['Average stock = batch size ÷ 2.'],
                 'traps': ['Selling overheads come after cost of production.']},
                [('EBQ', '√(2DS/C)'), ('Unit cost', 'Total cost ÷ units'), ('Average inventory', 'Q/2')],
                viva, cases)
