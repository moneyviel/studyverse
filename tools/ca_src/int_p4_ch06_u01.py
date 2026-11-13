"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 6 Cost Sheet.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch06-u01'
T1 = 'Functional classification and cost heads'
T2 = 'Prime cost'
T3 = 'Works cost and cost of production'
T4 = 'Cost of goods sold and cost of sales'
T5 = 'Treatment of special items'
T6 = 'Cost sheet uses and estimated cost (quotations)'


def build():
    ck = Checks()
    rmc = ck.add('400000+2400000+60000-360000', 'Raw material consumed (GST with input credit excluded)')
    emp = ck.add('800000+96000+40000', 'Direct employee cost')
    dexp = ck.add('50000+120000+240000/2', 'Direct expenses (moulds: one year\'s share)')
    prime = ck.add('2500000+936000+290000', 'Prime cost')
    foh = ck.add('180000+200000+300000+64000', 'Factory overheads')
    gwc = ck.add('3726000+744000', 'Gross works cost')
    wc = ck.add('4470000+150000-210000', 'Works (factory) cost')
    cop = ck.add('4410000+80000+60000+120000-30000+90000', 'Cost of production')
    cpu = ck.add('4730000/10000', 'Cost of production per unit')
    cfg = ck.add('800*473', 'Closing finished goods at current cost')
    cogs = ck.add('4730000+230000-378400', 'Cost of goods sold')
    cos = ck.add('4581600+240000+310000+150000', 'Cost of sales before finance cost')
    tot = ck.add('5281600+100000', 'Cost of sales including interest shown separately')
    sales = ck.add('9700*620', 'Sales')
    prof = ck.add('6014000-5381600', 'Profit')
    i1 = {'id': 'i1', 'title': 'Full cost sheet for an auto-parts maker', 'difficulty': 'hard', 'minutes': 18,
          'q': 'Shivneri Auto Parts, year ended 31 March: raw materials — opening ₹4,00,000, purchases ₹24,00,000 (plus GST ₹4,32,000 with full input credit), freight inward ₹60,000, closing ₹3,60,000. Direct wages ₹8,00,000; employer PF/ESI ₹96,000; production bonus ₹40,000. Royalty on production ₹50,000; job-work charges ₹1,20,000; moulds costing ₹2,40,000 lasting 2 years\' production. Factory: power ₹1,80,000, plant depreciation ₹2,00,000, supervisor ₹3,00,000, stores ₹64,000. WIP: opening ₹1,50,000, closing ₹2,10,000. Quality control ₹80,000; R&D on process improvement ₹60,000; production-related administration ₹1,20,000; scrap sold ₹30,000; primary packing ₹90,000. Output 10,000 units. Finished goods: opening 500 units ₹2,30,000; closing 800 units (valued at this year\'s cost). Sales 9,700 units at ₹620. General administration ₹2,40,000; selling ₹3,10,000; distribution ₹1,50,000; interest on term loan ₹1,00,000; pollution penalty ₹25,000. Prepare a cost sheet and find profit.',
          'solution': [table(['Particulars', '₹'], [
              ['Opening raw material + purchases + freight – closing', inr(rmc)],
              ['Direct employee cost (wages + PF/ESI + production bonus)', inr(emp)],
              ['Direct expenses (royalty + job work + moulds 1,20,000)', inr(dexp)],
              ['Prime cost', inr(prime)],
              ['Factory overheads', inr(foh)],
              ['Gross works cost', inr(gwc)],
              ['Add opening WIP, less closing WIP', '1,50,000 – 2,10,000'],
              ['Works cost', inr(wc)],
              ['Add quality control, R&D (process), production administration', inr(260000)],
              ['Less scrap realised', '(30,000)'],
              ['Add primary packing', inr(90000)],
              ['Cost of production (10,000 units)', inr(cop)],
              ['Cost per unit', inr(cpu)],
              ['Add opening finished goods', inr(230000)],
              ['Less closing finished goods (800 × 473)', f'({inr(cfg)})'],
              ['Cost of goods sold', inr(cogs)],
              ['Add general administration, selling, distribution', inr(700000)],
              ['Cost of sales', inr(cos)],
              ['Interest and finance charges (shown separately)', inr(100000)],
              ['Total cost', inr(tot)],
              ['Sales (9,700 × 620)', inr(sales)],
              ['Profit', inr(prof)]], title='Cost sheet'),
              note('GST with input credit is not a cost. The pollution penalty is excluded from cost altogether. Interest is not part of cost of production but is shown as a separate item within cost of sales.')],
          'checks': list(ck)}

    ck2 = Checks()
    fohp = ck2.add('300000/400000*100', 'Factory overhead as % of direct wages')
    admp = ck2.add('260000/1300000*100', 'Administration as % of works cost')
    wc2 = ck2.add('40000+24000+24000*0.75', 'Works cost of the job')
    tc2 = ck2.add('82000*1.2', 'Total cost of the job')
    price = ck2.add('98400/0.8', 'Quoted price for 20% profit on selling price')
    i2 = {'id': 'i2', 'title': 'Pricing a tender from last year\'s cost sheet', 'difficulty': 'core', 'minutes': 7,
          'q': 'Last year Nandi Fabricators had materials ₹6,00,000, direct wages ₹4,00,000, factory overheads ₹3,00,000 and administration overheads ₹2,60,000. A new job needs materials ₹40,000 and direct wages ₹24,000. Quote a price that earns 20% profit on selling price, recovering factory overheads on direct wages and administration on works cost.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Factory overhead rate', '3,00,000 ÷ 4,00,000', f'{fohp}% of wages'],
              ['Administration rate', '2,60,000 ÷ 13,00,000', f'{admp}% of works cost'],
              ['Works cost of job', '40,000 + 24,000 + 75% × 24,000', inr(wc2)],
              ['Total cost', 'Works cost × 1.20', inr(tc2)],
              ['Quoted price', 'Total cost ÷ 0.80', inr(price)]], title='Estimated cost and quotation'),
              note('20% profit on selling price equals 25% on cost; dividing cost by 0.80 gets there directly.')],
          'checks': list(ck2)}

    fmt = table(['Line', 'Includes'], [
        ['Direct materials consumed', 'Opening + purchases (net of recoverable taxes) + freight inward – closing'],
        ['Direct employee cost', 'Wages, employer PF/ESI, production bonus of direct workers'],
        ['Direct expenses', 'Royalty on production, hire of special equipment, job-work, moulds/patterns written off'],
        ['= Prime cost', ''],
        ['+ Factory overheads', 'Indirect materials, indirect labour, power, depreciation, factory rent'],
        ['= Gross works cost; ± WIP', 'Opening WIP added, closing WIP deducted'],
        ['= Works cost', ''],
        ['+ Quality control, R&D (process), production administration; – scrap/by-product credits; + primary packing', ''],
        ['= Cost of production', ''],
        ['± Finished goods stock', 'Opening added, closing deducted'],
        ['= Cost of goods sold', ''],
        ['+ General administration, selling, distribution overheads', 'Secondary packing is a distribution cost'],
        ['= Cost of sales', 'Interest and finance charges shown separately']], title='Cost sheet format')

    concepts = [
        C('c1', T1, [
            'Costs are grouped by function — production, administration, selling and distribution — so that cost can be built up stage by stage.',
            'Cost heads: prime cost, works (factory) cost, cost of production, cost of goods sold and cost of sales (format table).'],
          'A cost sheet builds cost the way a product is made and sold: material in, factory, packing, warehouse, customer.',
          'Freight on materials belongs to prime cost; freight to customers belongs to distribution.',
          blocks=[fmt]),
        C('c2', T2, [
            'Prime cost = direct materials consumed + direct employee cost + direct expenses.',
            'Direct materials include purchase price, freight inward and non-recoverable taxes; recoverable GST is excluded; trade discounts reduce cost.',
            'Direct employee cost includes the employer\'s statutory contributions and production bonus for workers directly on the product.',
            'Direct expenses: royalty based on production, hire of special tools, job-work charges, and moulds or patterns written off over their useful production.'],
          'Prime cost is everything you can tie to the product without guesswork.',
          'Moulds lasting two years\' production are charged half each year.'),
        C('c3', T3, [
            'Works cost = prime cost + factory overheads, adjusted for opening and closing work-in-progress.',
            'Cost of production = works cost + quality control + research and development (process related) + administration relating to production – credits for scrap, by-products and recoveries + primary packing.'],
          'Cost of production is what it takes to bring a finished, packed unit to the factory gate.',
          'Scrap sold reduces cost of production because it recovers part of the material cost.'),
        C('c4', T4, [
            'Cost of goods sold = cost of production + opening finished goods – closing finished goods.',
            'Cost of sales = cost of goods sold + general administration + selling and distribution overheads.',
            'Profit = sales – cost of sales (including finance costs shown separately).'],
          'Stock adjustments decide which costs belong to what was actually sold this period.',
          'Units produced and units sold differ, so per-unit costs are computed on the right base.'),
        C('c5', T5, [
            'Abnormal costs that are material and quantifiable (for example costs of a pandemic lockdown) are excluded from cost of production.',
            'Subsidies, grants and incentives reduce the cost of the object they relate to.',
            'Penalties, fines, damages and demurrage are not part of cost.',
            'Interest and finance charges are excluded from cost of production but presented as a separate item in cost of sales.'],
          'Cost should show the normal, inevitable cost of making and selling — not accidents or punishments.',
          'A late-payment penalty to a supplier is a loss, not a cost of the product.'),
        C('c6', T6, [
            'A cost sheet gives total and per-unit cost, supports comparisons over time, helps prepare tenders and estimates, guides pricing and highlights inefficiency.',
            'Estimated cost sheets for quotations apply past overhead rates (e.g. factory overhead as % of wages, administration as % of works cost) to the job\'s estimated prime cost, then add the desired profit.',
            'Profit on selling price p% → price = cost ÷ (1 – p). Profit on cost p% → price = cost × (1 + p).'],
          'Yesterday\'s cost sheet is the template for tomorrow\'s quotation.',
          '25% on cost is the same as 20% on selling price.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Monthly cost statement', 'role': 'Cost accountant',
         'situation': 'The plant head wants a monthly cost sheet with per-unit figures.',
         'steps': ['Classify every expense by function and nature.', 'Exclude recoverable taxes, penalties and abnormal items.', 'Build up to cost of production and cost of sales with stock adjustments.', 'Report per-unit costs on units produced and sold.'],
         'takeaway': 'Correct classification matters more than arithmetic.'},
        {'id': 'j2', 'title': 'Tender pricing', 'role': 'Article assistant',
         'situation': 'A client is quoting for a government order.',
         'steps': ['Derive overhead rates from last year\'s cost sheet.', 'Estimate prime cost of the order.', 'Add overheads and the required margin on selling price.'],
         'takeaway': 'Distinguish profit on cost from profit on price.'},
    ]

    mcqs = [
        Q('m1', 'GST paid on raw material purchases with full input tax credit is:', ['Excluded from material cost', 'Added to prime cost', 'A factory overhead', 'A selling overhead'], 0,
          'Where input tax credit is available, the GST is recovered and is not a cost to the business, so it is excluded from material cost. Only non-recoverable taxes form part of cost. In practice: check eligibility for credit.', 'c2', T2),
        Q('m2', 'Royalty paid on the basis of units produced is a:', ['Direct expense', 'Selling overhead', 'Factory overhead', 'Administration overhead'], 0,
          'A royalty that varies with production can be traced directly to units made, so it is a direct expense and part of prime cost. A royalty on sales would be a selling cost. In practice: the basis of the royalty decides its class.', 'c2', T2),
        Q('m3', 'Primary packing material is part of:', ['Cost of production', 'Distribution overhead', 'Selling overhead', 'Administration overhead'], 0,
          'Primary packing is needed to make the product saleable (bottles, wrappers), so it is included in cost of production. Secondary packing for transport is a distribution cost. In practice: ask whether the product can be sold without it.', 'c3', T3),
        Q('m4', 'Prime cost ₹5,00,000; factory overheads ₹2,00,000; opening WIP ₹40,000; closing WIP ₹60,000. Works cost is:', ['₹6,80,000', '₹7,00,000', '₹7,20,000', '₹7,60,000'], 0,
          'Works cost = 5,00,000 + 2,00,000 + 40,000 – 60,000 = ₹6,80,000. Opening WIP adds cost brought into the period; closing WIP removes cost carried forward. In practice: adjust WIP before adding quality control and packing.', 'c3', T3, 'core', check=680000),
        Q('m5', 'Cost of production ₹9,00,000; opening finished goods ₹60,000; closing finished goods ₹1,10,000. Cost of goods sold is:', ['₹8,50,000', '₹9,50,000', '₹10,70,000', '₹7,30,000'], 0,
          'Cost of goods sold = 9,00,000 + 60,000 – 1,10,000 = ₹8,50,000. Finished stock adjustments move costs between periods according to what was sold. In practice: closing stock is often valued at current cost per unit.', 'c4', T4, 'core', check=850000),
        Q('m6', 'Interest on a term loan is shown in a cost sheet:', ['As a separate item of cost of sales, outside cost of production', 'In prime cost', 'In factory overheads', 'It is never shown'], 0,
          'Interest and finance charges are excluded from cost of production but presented separately within cost of sales, following the cost accounting standards. They are not a factory overhead. In practice: this keeps product cost free of financing choices.', 'c5', T5, 'moderate'),
        Q('m7', 'A penalty for late filing of a statutory return is:', ['Excluded from cost', 'An administration overhead', 'A direct expense', 'Part of cost of production'], 0,
          'Penalties, fines, damages and demurrage are not costs of making or selling the product, so they are kept out of the cost sheet and appear only in the financial accounts. In practice: this affects cost-to-financial reconciliation.', 'c5', T5),
        Q('m8', 'Total cost ₹80,000; profit should be 20% of selling price. Selling price is:', ['₹1,00,000', '₹96,000', '₹1,04,000', '₹84,000'], 0,
          'Profit of 20% on selling price means cost is 80% of price, so price = 80,000 ÷ 0.80 = ₹1,00,000. Adding 20% on cost would give only ₹96,000. In practice: confirm which base the margin uses.', 'c6', T6, 'core', check=100000),
        Q('m9', 'Salary of the factory supervisor is part of:', ['Factory overheads', 'Prime cost', 'Administration overheads', 'Selling overheads'], 0,
          'A supervisor\'s salary cannot be traced to particular units but is incurred in the factory, so it is an indirect cost of production — a factory overhead. Office manager salaries would be administration. In practice: location and purpose decide the class.', 'c3', T3),
    ]

    questions = [
        W('q1', 10, i1['q'], i1['solution'],
          [S('s1', 'Materials consumed (GST excluded)', 1.5, 'computation', 'material|gst', nums=[rmc]),
           S('s2', 'Direct employee and expenses', 1.5, 'computation', 'employee|royalty', nums=[emp, dexp]),
           S('s3', 'Prime and works cost', 2, 'computation', 'prime|works', nums=[prime, wc]),
           S('s4', 'Cost of production', 2, 'computation', 'cost of production', nums=[cop, cpu]),
           S('s5', 'COGS and cost of sales', 2, 'computation', 'goods sold|cost of sales', nums=[cogs, cos]),
           S('s6', 'Profit and exclusions', 1, 'computation', 'profit|penalty', nums=[prof])],
          ['Follow the standard order of the cost sheet.'], ['Including GST with credit or the penalty.'], ['Vertical cost sheet.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Overhead rates', 1.5, 'computation', 'wages|works cost', nums=[fohp, admp]),
           S('s2', 'Job cost', 1.5, 'computation', 'works cost|total cost', nums=[wc2, tc2]),
           S('s3', 'Price', 1, 'computation', 'price|0.80', nums=[price])],
          ['Profit is on selling price.'], ['Adding 20% to cost.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is included in prime cost?',
          'Direct materials consumed, direct employee cost and direct expenses such as royalty on production and job-work charges.',
          [P('p1', 'Direct materials', 3, 'material'), P('p2', 'Direct employee cost', 3, 'employee|wages|labour'), P('p3', 'Direct expenses', 4, 'expense|royalty')], 'c2'),
        V('v2', 'How is cost of goods sold derived from cost of production?',
          'Add the opening stock of finished goods and deduct the closing stock of finished goods.',
          [P('p1', 'Add opening finished goods', 5, 'opening'), P('p2', 'Deduct closing finished goods', 5, 'closing')], 'c4'),
        V('v3', 'Where do primary and secondary packing go in a cost sheet?',
          'Primary packing is part of cost of production because it is needed to sell the product; secondary packing for transport is a distribution overhead.',
          [P('p1', 'Primary in cost of production', 5, 'production'), P('p2', 'Secondary in distribution', 5, 'distribution')], 'c3'),
        V('v4', 'How are interest and penalties treated in cost accounts?',
          'Penalties are excluded from cost altogether; interest is excluded from cost of production but shown separately in cost of sales.',
          [P('p1', 'Penalties excluded', 5, 'excluded|not part'), P('p2', 'Interest separate', 5, 'separate')], 'c5'),
        V('v5', 'Give two uses of a cost sheet.',
          'It shows total and unit cost for comparison over periods, and it helps prepare estimates and quotations and fix selling prices.',
          [P('p1', 'Unit cost / comparison', 5, 'unit|compar'), P('p2', 'Quotations / pricing', 5, 'quotation|tender|price|estimate')], 'c6'),
    ]

    cases = [{'id': 'k1', 'title': 'Pashmina Weaves', 'difficulty': 'moderate',
              'case': 'Pashmina Weaves produced 4,000 shawls. Materials consumed ₹8,00,000; direct wages ₹4,00,000; factory overheads 60% of wages; quality control ₹40,000; scrap sold ₹20,000; no WIP. Opening stock nil; 3,600 shawls sold at ₹750. Administration (general) ₹1,20,000; selling ₹36 per shawl sold.',
              'mcqs': [
                  M('k1a', 'Cost of production is:', ['₹14,60,000', '₹14,40,000', '₹14,80,000', '₹12,00,000'], 0,
                    'Prime cost 12,00,000 + factory overheads 2,40,000 = 14,40,000; add quality control 40,000 and deduct scrap 20,000 = ₹14,60,000. Scrap realised reduces cost of production. In practice: QC is a production cost.', 'core', check=1460000, topic=T3),
                  M('k1b', 'Cost of production per shawl is:', ['₹365', '₹360', '₹405.56', '₹300'], 0,
                    'Per unit = 14,60,000 ÷ 4,000 = ₹365, computed on units produced, not sold. This rate also values the 400 shawls in closing stock. In practice: the denominator matters.', 'core', check=365, topic=T4),
                  M('k1c', 'Cost of sales is:', ['₹15,63,600', '₹15,80,000', '₹14,34,000', '₹15,20,000'], 0,
                    'COGS = 14,60,000 – 400 × 365 = 13,14,000; add administration 1,20,000 and selling 3,600 × 36 = 1,29,600 → ₹15,63,600. Selling overheads are charged on units sold. In practice: build step by step.', 'hard', check=1563600, topic=T4),
                  M('k1d', 'Profit is:', ['₹11,36,400', '₹12,36,400', '₹11,40,000', '₹10,36,400'], 0,
                    'Sales = 3,600 × 750 = ₹27,00,000; profit = 27,00,000 – 15,63,600 = ₹11,36,400. Closing stock carried at cost does not enter this period\'s profit. In practice: reconcile with financial accounts.', 'moderate', check=1136400, topic=T4),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch06', 1, 'Cost Sheet',
                ['Classify costs by function and identify the cost heads in a cost sheet.',
                 'Compute prime cost, works cost and cost of production.',
                 'Derive cost of goods sold, cost of sales and profit.',
                 'Treat special items: recoverable taxes, abnormal costs, subsidies, penalties and interest.',
                 'Prepare estimated cost sheets and quotations.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 50}, 'prereq': ['int-p4-ch05-u01'],
                 'exam_tip': 'Expect a full cost sheet from a list of expenses; classify each item carefully (GST credit, moulds, packing, penalties, interest) and show per-unit figures.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Prime cost = DM + DE + direct expenses.', 'Works cost = prime + FOH ± WIP.', 'Cost of production adds QC, R&D (process), production admin, primary packing, less scrap.',
                             'COGS = CoP ± finished goods; cost of sales adds admin, selling, distribution.', 'Exclude recoverable GST, penalties, abnormal costs; show interest separately.',
                             'Quotation: apply past rates, then margin (on price: ÷ (1 – p)).'],
                 'remember': ['Secondary packing is distribution.', 'Per-unit cost of production uses units produced.'],
                 'traps': ['Profit on price ≠ profit on cost.', 'Royalty on sales is a selling cost.']},
                [('Prime cost', 'DM + DE + DExp'), ('Works cost', 'Prime + FOH ± WIP'), ('COGS', 'CoP + op FG – cl FG'), ('20% on price', 'Cost ÷ 0.8')],
                viva, cases,
                topics=['Introduction', 'Functional Classification of Elements of Cost', 'Cost Heads in a Cost Sheet', 'Cost Sheet/Statement'])
