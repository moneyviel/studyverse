"""CA Foundation · Paper 1 Accounting · Chapter 7 Final Accounts of Sole Proprietors · Unit 2 Manufacturing entities.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M
from fnd_p1_ch07_u01 import tacc, bsheet

UID = 'fnd-p1-ch07-u02'


def build():
    # =============== Illustration 1: cost build-up per unit ===============
    c1 = Checks()
    u1 = 40000
    rm1 = c1.add('40000*25', 'Direct material @ ₹25 per unit')
    dw1 = c1.add('40000*12', 'Direct wages @ ₹12 per unit')
    de1 = c1.add('40000*4', 'Royalty @ ₹4 per unit produced (direct expense)')
    pc1 = c1.add('1000000+480000+160000', 'Prime cost')
    fc1 = c1.add('1640000+240000', 'Factory (works) cost after overheads ₹2,40,000')
    pu1 = c1.add('1880000/40000', 'Manufacturing cost per unit')
    t1 = table(['Element', 'Basis', '₹'], [
        ['Direct material', '40,000 × ₹25', inr(rm1)], ['Direct wages', '40,000 × ₹12', inr(dw1)], ['Direct expenses — royalty', '40,000 × ₹4', inr(de1)],
        ['Factory overheads', 'Given', '2,40,000'], ['Total manufacturing cost', '', inr(fc1)]], num=[2], total=True, title='Manufacturing cost of Zenith Tools',
        note=f'Prime cost = {R(pc1)}; manufacturing cost per unit = 18,80,000 ÷ 40,000 = {R(pu1)}.')

    # =============== Illustration 2: Manufacturing + Trading with quantities ===============
    c2 = Checks()
    rmc = c2.add('140000+960000+20000-160000', 'Raw materials consumed (carriage on raw materials included)')
    roy = c2.add('80000*2', 'Royalty @ ₹2 per unit produced')
    prime = c2.add('960000+320000+160000', 'Prime cost')
    ovh = c2.add('120000+90000+60000', 'Factory overheads: rent, power, depreciation of plant')
    cop = c2.add('1440000+270000+45000-55000-20000', 'Cost of production (after WIP and scrap)')
    cpu = c2.add('1680000/80000', 'Cost per unit produced')
    sold = c2.add('10000+80000-12000', 'Units sold')
    salesv = c2.add('78000*30', 'Sales @ ₹30')
    cfg = c2.add('12000*21', 'Closing finished goods (FIFO: from this year\'s output @ ₹21)')
    gp2 = c2.add('2340000+252000-(200000+1680000)', 'Gross profit')
    mfg2 = tacc('Manufacturing Account of Arora Plastics for the year ended 31 March 2027', [
        ('To Opening work-in-progress', 45000),
        ('To Raw materials consumed: opening 1,40,000 + purchases 9,60,000 + carriage 20,000 − closing 1,60,000', rmc),
        ('To Direct wages', 320000), ('To Direct expenses — royalty (80,000 units × ₹2)', roy),
        ('To Factory overheads: rent 1,20,000; power 90,000; depreciation of plant 60,000', ovh)],
        [('By Sale of scrap', 20000), ('By Closing work-in-progress', 55000), ('By Cost of production transferred to Trading A/c (80,000 units)', cop)])
    trd2 = tacc('Trading Account of Arora Plastics for the year ended 31 March 2027', [
        ('To Opening stock of finished goods (10,000 units)', 200000), ('To Cost of production b/d (80,000 units)', cop), ('To Gross profit c/d', gp2)],
        [('By Sales (78,000 units × ₹30)', salesv), ('By Closing stock of finished goods (12,000 units × ₹21)', cfg)])

    # =============== Illustration 3: full set with apportionment ===============
    c3 = Checks()
    TB3 = [('Capital', -500000), ('Opening stock — raw materials', 60000), ('Opening stock — work-in-progress', 25000), ('Opening stock — finished goods', 70000),
           ('Purchases of raw materials', 480000), ('Carriage inwards', 12000), ('Direct wages', 150000), ('Factory power', 36000), ('Repairs to plant', 9000),
           ('Rent (factory and office)', 80000), ('Lighting', 24000), ('Office salaries', 72000), ('Selling expenses', 28000), ('Sales', -1050000), ('Sale of scrap', -6000),
           ('Trade receivables', 160000), ('Trade payables', -110000), ('Plant and machinery', 300000), ('Office furniture', 50000), ('Cash at bank', 70000), ('Drawings', 40000)]
    assert sum(v for _, v in TB3) == 0
    c3.add('60000+25000+70000+480000+12000+150000+36000+9000+80000+24000+72000+28000+160000+300000+50000+70000+40000', 'Debit total of trial balance')
    c3.add('500000+1050000+6000+110000', 'Credit total of trial balance')
    rmc3 = c3.add('60000+480000+12000-70000', 'Raw materials consumed')
    wg3 = c3.add('150000+10000', 'Direct wages including outstanding')
    rf3 = c3.add('80000*3/4', 'Factory share of rent (3/4)')
    lf3 = c3.add('24000*2/3', 'Factory share of lighting (2/3)')
    dp3 = c3.add('300000*10/100', 'Depreciation on plant @10%')
    cop3 = c3.add('25000+482000+160000+36000+9000+60000+16000+30000-30000-6000', 'Cost of production')
    gp3 = c3.add('1050000+90000-(70000+782000)', 'Gross profit')
    df3 = c3.add('50000*10/100', 'Depreciation on office furniture @10%')
    np3 = c3.add('288000-(72000+20000+8000+28000+5000)', 'Net profit')
    cap3 = c3.add('500000+155000-40000', 'Closing capital')
    c3.add('615000+110000+10000', 'Balance sheet total (liabilities)')
    c3.add('270000+45000+70000+30000+90000+160000+70000', 'Balance sheet total (assets)')
    mfg3 = tacc('Manufacturing Account of Sharma Industries for the year ended 31 March 2027', [
        ('To Opening work-in-progress', 25000), ('To Raw materials consumed: 60,000 + 4,80,000 + carriage 12,000 − 70,000', rmc3),
        ('To Direct wages 1,50,000 + outstanding 10,000', wg3), ('To Factory power', 36000), ('To Repairs to plant', 9000),
        ('To Rent — factory share (3/4 of 80,000)', rf3), ('To Lighting — factory share (2/3 of 24,000)', lf3), ('To Depreciation on plant', dp3)],
        [('By Sale of scrap', 6000), ('By Closing work-in-progress', 30000), ('By Cost of production transferred to Trading A/c', cop3)])
    trd3 = tacc('Trading Account of Sharma Industries for the year ended 31 March 2027', [('To Opening stock of finished goods', 70000), ('To Cost of production b/d', cop3), ('To Gross profit c/d', gp3)],
                [('By Sales', 1050000), ('By Closing stock of finished goods', 90000)])
    pl3 = tacc('Profit and Loss Account of Sharma Industries for the year ended 31 March 2027', [('To Office salaries', 72000), ('To Rent — office share (1/4)', 20000), ('To Lighting — office share (1/3)', 8000),
               ('To Selling expenses', 28000), ('To Depreciation on office furniture', df3), ('To Net profit transferred to Capital A/c', np3)], [('By Gross profit b/d', gp3)])
    bs3 = bsheet('Balance Sheet of Sharma Industries as at 31 March 2027', [('Capital 5,00,000 + net profit 1,55,000 − drawings 40,000', cap3), ('Trade payables', 110000), ('Outstanding wages', 10000)],
                 [('Plant and machinery 3,00,000 − depreciation 30,000', 270000), ('Office furniture 50,000 − depreciation 5,000', 45000), ('Stock — raw materials', 70000),
                  ('Stock — work-in-progress', 30000), ('Stock — finished goods', 90000), ('Trade receivables', 160000), ('Cash at bank', 70000)])

    # =============== Question 1: Neha Plastics ===============
    q1 = Checks()
    qrm = q1.add('80000+620000+15000-95000', 'Raw materials consumed')
    qhire = q1.add('50000*1.5', 'Machine hire @ ₹1.50 per unit produced')
    qprime = q1.add('620000+210000+75000', 'Prime cost')
    qovh = q1.add('60000+45000+25000', 'Factory overheads')
    qcop = q1.add('905000+130000+30000-40000-5000', 'Cost of production')
    qcpu = q1.add('1020000/50000', 'Cost per unit')
    qcl = q1.add('6000+50000-52000', 'Closing finished units')
    qcfg = q1.add('4000*20.4', 'Closing finished goods @ ₹20.40 (FIFO)')
    qsales = q1.add('52000*28', 'Sales')
    qgp = q1.add('1456000+81600-(114000+1020000)', 'Gross profit')
    mfgq = tacc('Manufacturing Account of Neha Plastics for the year ended 31 March 2027', [
        ('To Opening work-in-progress', 30000), ('To Raw materials consumed: 80,000 + 6,20,000 + freight 15,000 − 95,000', qrm), ('To Direct wages', 210000),
        ('To Direct expenses — machine hire (50,000 × ₹1.50)', qhire), ('To Factory overheads: rent 60,000; depreciation 45,000; indirect wages 25,000', qovh)],
        [('By By-product at net realisable value', 5000), ('By Closing work-in-progress', 40000), ('By Cost of production — 50,000 units @ ₹20.40', qcop)])
    trdq = tacc('Trading Account of Neha Plastics for the year ended 31 March 2027', [('To Opening finished goods (6,000 units)', 114000), ('To Cost of production b/d (50,000 units)', qcop), ('To Gross profit c/d', qgp)],
                [('By Sales (52,000 units × ₹28)', qsales), ('By Closing finished goods (4,000 units × ₹20.40)', qcfg)])

    # =============== MCQ figures ===============
    mc = Checks()
    m_rm = mc.add('30000+200000-5000-40000', 'RM consumed')
    m_cop = mc.add('500000+120000+20000-35000', 'cost of production')
    m_rent = mc.add('90000*2/3', 'factory rent')
    m_units = mc.add('2000+50000-4000', 'units sold')
    m_cpu = mc.add('720000/24000', 'cost per unit')
    m_prime = mc.add('300000+150000+30000', 'prime cost')

    # =============== Case ===============
    kc = Checks()
    k_rm = kc.add('50000+400000-60000', 'RM consumed')
    k_roy = kc.add('60000*2', 'royalty')
    k_prime = kc.add('390000+180000+120000', 'prime cost')
    k_cop = kc.add('690000+110000+30000-20000-10000', 'cost of production')
    k_cpu = kc.add('round(800000/60000,2)', 'per unit')
    cases = [{
        'id': 'k1', 'title': 'Nova Footwear — one year in the factory', 'difficulty': 'hard',
        'case': ('Nova Footwear produced 60,000 pairs in 2026-27. Raw materials: opening stock ₹50,000, purchases ₹4,00,000, closing stock ₹60,000. Direct wages ₹1,80,000. '
                 'Design royalty is paid at ₹2 for every pair produced. Factory overheads ₹1,10,000; office expenses ₹70,000. Work-in-progress: opening ₹30,000, closing ₹20,000. '
                 'Leather off-cuts (a by-product) were sold for ₹10,000.'),
        'mcqs': [
            M('k1a', 'What is the cost of raw materials consumed?', [R(k_rm), '₹4,50,000', '₹4,10,000', '₹3,40,000'], 0,
              "Raw materials consumed = opening stock 50,000 + purchases 4,00,000 − closing stock 60,000 = ₹3,90,000. The trap ₹4,50,000 adds opening stock to purchases but forgets to deduct closing stock; ₹4,10,000 adds the stock change the wrong way. In practice: a footwear factory's stores ledger records every issue of leather and soles so that consumption can be matched with production.", 'core', '50000+400000-60000') | {'topic': "Manufacturing Costs"},
            M('k1b', 'What is the prime cost?', [R(k_prime), '₹5,70,000', '₹8,00,000', '₹6,30,000'], 0,
              "Design royalty at ₹2 per pair produced is a direct expense: 60,000 × 2 = ₹1,20,000. Prime cost = materials consumed 3,90,000 + direct wages 1,80,000 + royalty 1,20,000 = ₹6,90,000. The trap ₹5,70,000 leaves out the royalty, treating it as an overhead or ignoring it. In practice: brands licensing designs to manufacturers charge royalty per unit, and the manufacturer includes it in the direct cost of every pair.", 'moderate', '390000+180000+120000') | {'topic': "Manufacturing Costs"},
            M('k1c', 'What is the cost of production transferred to the Trading Account?', [R(k_cop), '₹8,70,000', '₹8,10,000', '₹7,90,000'], 0,
              "Cost of production = prime cost 6,90,000 + factory overheads 1,10,000 + opening WIP 30,000 − closing WIP 20,000 − by-product sale 10,000 = ₹8,00,000. Office expenses of ₹70,000 belong to Profit and Loss. The trap ₹8,10,000 forgets to reduce the by-product sale; ₹8,70,000 wrongly loads office expenses. In practice: leather off-cuts sold to small-goods makers reduce the cost of the main footwear production.", 'hard', '690000+110000+30000-20000-10000') | {'topic': "Manufacturing Costs"},
            M('k1d', 'What is the cost of production per pair?', ['₹13.33', '₹12.00', '₹14.50', '₹13.50'], 0,
              "Cost per pair = cost of production ÷ pairs produced = 8,00,000 ÷ 60,000 = ₹13.33 (rounded). The trap ₹14.50 divides ₹8,70,000, which wrongly includes office expenses; ₹12.00 uses the cost before overheads or misses an item. In practice: Nova's management would compare this ₹13.33 with wholesale prices to set margins for retailers and distributors.", 'moderate', 'round(800000/60000,2)') | {'topic': "Design of a Manufacturing Account"},
        ]}]

    viva = [
        V('v1', 'Explain prime cost, factory cost and cost of production.',
          'Prime cost is the total of direct costs: raw materials consumed, direct wages and direct expenses. Factory cost, also called works cost, is prime cost plus factory overheads, that is indirect material, indirect wages and indirect factory expenses. Cost of production is factory cost adjusted for work-in-progress — add opening work-in-progress, deduct closing work-in-progress — and less the value of scrap or by-products.',
          [P('p1', 'Prime cost = direct materials + direct wages + direct expenses', 4, 'prime', 'direct', 'material|raw', 'wage|labour|labor', min=3),
           P('p2', 'Factory (works) cost = prime cost + factory overheads', 3, 'factory cost|works cost|work cost|factory', 'overhead|indirect', min=2),
           P('p3', 'Cost of production = factory cost + opening WIP − closing WIP − scrap', 3, 'cost of production|production cost|cost of goods manufactured|manufacturing cost', 'work in progress|work in process|wip|unfinished|semi finished', min=2)], 'c2'),
        V('v2', 'How is work-in-progress treated in the Manufacturing Account?',
          'Work-in-progress means goods that are partly finished. Opening work-in-progress is shown on the debit side of the Manufacturing Account because it is completed this year, and closing work-in-progress is shown on the credit side because it is carried to next year. Closing work-in-progress also appears as a current asset in the Balance Sheet.',
          [P('p1', 'WIP = partly finished / semi-finished goods', 2, 'partly finished|partially finished|semi finished|unfinished|incomplete|half finished|not complete|not fully finished|not yet finished'),
           P('p2', 'Opening WIP on the debit side', 3, ALT('opening {w} debit', 'debit {w} opening', 'opening debit', 'opening work in progress debit', 'opening wip debit', 'opening is debit', 'opening on the debit', w=['', 'work in progress', 'wip', 'work in process'])),
           P('p3', 'Closing WIP on the credit side', 3, ALT('closing {w} credit', 'credit {w} closing', 'closing credit', 'closing is credit', 'closing on the credit', w=['', 'work in progress', 'wip', 'work in process'])),
           P('p4', 'Closing WIP is a current asset in the Balance Sheet', 2, 'balance sheet|current asset|asset')], 'c4'),
        V('v3', 'What is a by-product and how should its sale value be treated?',
          'A by-product is a secondary product that comes out of the same process and raw materials as the main product, without any special effort, and usually has a small value — for example molasses in sugar making. Its sale value or net realisable value should be credited to the Manufacturing Account, reducing the cost of production of the main product, rather than being shown as miscellaneous income.',
          [P('p1', 'Secondary product from the same process / materials, small value', 3, 'secondary|subsidiary|incidental|side product|along with|same process|same raw|same material|minor', min=1),
           P('p2', 'Credited to the Manufacturing Account (net realisable / sale value)', 4, 'credit manufactur|manufactur credit|credit side manufactur|credited to the manufactur|manufactur account credit|credited in manufactur|credit of manufactur'),
           P('p3', 'Reduces the cost of production of the main product', 3, 'reduc|lower|less|deduct|decreas', 'cost', min=2)], 'c4'),
        V('v4', 'Distinguish between direct expenses and factory overheads, with examples.',
          'Direct expenses are costs other than materials and wages that can be traced to a particular product, such as royalty or hire charges of a machine paid per unit produced. Factory overheads are indirect costs of the factory that cannot be linked to specific units — indirect material like lubricants and small tools, indirect wages like maintenance staff wages, and indirect expenses like factory rent, depreciation and insurance of plant.',
          [P('p1', 'Direct expenses are traceable to the product (other than material and wages)', 3, 'direct', 'trace|identif|link|specific|particular|directly|per unit|vary with', min=2),
           P('p2', 'Examples of direct expenses: royalty / hire charges per unit produced', 2, 'royalt|hire'),
           P('p3', 'Overheads cannot be traced to units — indirect material, wages, expenses', 3, 'overhead|indirect', 'cannot|not|can t|no direct|indirect', min=2),
           P('p4', 'Examples of overheads: factory rent, depreciation, lubricants, maintenance wages', 2, 'factory rent|rent|depreciat|lubricant|oil|small tool|maintenance|insurance|power|fuel|repair', min=1)], 'c3'),
        V('v5', 'What purposes does a Manufacturing Account serve?',
          'A Manufacturing Account shows the total cost of producing the finished goods, with each element of cost set out separately. It gives the factory cost, which helps reconcile the financial books with the cost records and compare manufacturing efficiency from period to period. If the output is transferred to the Trading Account at market price, it also shows the profit or loss on manufacturing, and it can be used to fix production-linked bonus.',
          [P('p1', 'Shows the total cost of production with its elements', 4, 'cost of production|cost of producing|manufacturing cost|production cost|total cost|cost of manufactur|cost of finished|cost of goods manufactured'),
           P('p2', 'Helps reconcile with cost records / compare periods', 3, 'reconcil|compar|period to period|year to year|control|efficien', min=1),
           P('p3', 'Can show manufacturing profit (transfer at market price) or fix production bonus', 3, 'market price|manufacturing profit|profit on manufactur|profit or loss on manufactur|bonus', min=1)], 'c1'),
        V('v6', 'In a question with quantities, how do you value the closing stock of finished goods?',
          'Use quantity columns: units sold equal opening units plus units produced minus closing units, so the quantities on both sides agree. Unless told otherwise, assume first in first out, so the opening stock is treated as sold first and the closing stock comes from this year\'s production. Closing finished goods are therefore valued at this year\'s cost of production per unit.',
          [P('p1', 'Quantity columns: opening + produced − closing = sold', 3, 'quantit|unit', 'opening|produc|manufactur|sold|closing', min=2),
           P('p2', 'Assume FIFO — opening stock sold first', 3, 'first in first out|fifo|opening stock sold first|old stock sold first|opening sold first|earlier stock sold first'),
           P('p3', "Closing stock valued at this year's cost of production per unit", 4, 'current year|this year|year s production|current production|this year s cost|cost of production per unit|current cost|latest cost|cost per unit', min=1)], 'c5'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch07', 'n': 2,
        'title': 'Final Accounts of Manufacturing Entities',
        'outcomes': [
            'Explain why a manufacturing business prepares a Manufacturing Account and how it links to the Trading Account, Profit and Loss Account and Balance Sheet.',
            'Classify costs into raw materials consumed, direct wages, direct expenses and factory overheads, and build prime cost, factory cost and cost of production.',
            'Treat opening and closing work-in-progress, scrap and by-products correctly.',
            'Apportion shared expenses (rent, lighting) between factory and office, and prepare the full set of final accounts of a manufacturer.',
            'Use quantity columns and the first-in-first-out assumption to value closing finished goods.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 60}, 'prereq': ['fnd-p1-ch07-u01'],
                 'exam_tip': 'Label every subtotal — raw materials consumed, prime cost, factory cost, cost of production. Examiners award marks for each, and an unlabelled lump loses them even if the final figure is right.'},
        'concepts': [
            {'id': 'c1', 'title': 'Why a Manufacturing Account, and what it does',
             'body': ['A manufacturer converts raw materials into finished goods. Besides the Trading Account, Profit and Loss Account and Balance Sheet, it may prepare a Manufacturing Account to find the cost of the goods it produced during the year. That cost is transferred to the debit of the Trading Account, which then deals only with finished goods.',
                      'Purposes: (1) shows the total cost of production with each element listed — materials, wages, direct expenses, overheads; (2) gives the factory cost, which helps reconcile the financial books with cost records and compare manufacturing performance from year to year; (3) if output is transferred to Trading at market price, it shows a separate profit or loss on manufacturing, and it can also be the base for a production-linked bonus.',
                      'Difference from the Trading Account: the Manufacturing Account ends with cost of production (no profit figure unless transfer is at market price) and deals with raw materials and work-in-progress; the Trading Account ends with gross profit and deals with finished goods only.',
                      'In practice, few businesses now prepare a separate Manufacturing Account; non-corporate entities show these items in the Trading Account and companies in the Statement of Profit and Loss. The exam still tests the format.'],
             'analogy': 'The Manufacturing Account is the kitchen; the Trading Account is the dining hall. The kitchen tells you what it cost to cook the food; the dining hall tells you what you made by selling it.',
             'work': 'Cost accountants in factories reconcile the cost of production in the financial books with the costing system every month. A large difference points to wastage, wrong overhead absorption or recording errors.'},
            {'id': 'c2', 'title': 'Building up manufacturing cost',
             'body': ['Raw materials consumed = opening stock of raw materials + purchases (net of returns, plus carriage/freight on materials) − closing stock of raw materials.',
                      'Prime cost = raw materials consumed + direct wages + direct expenses.',
                      'Factory (works) cost = prime cost + factory overheads (indirect materials + indirect wages + indirect factory expenses).',
                      'Cost of production = factory cost + opening work-in-progress − closing work-in-progress − sale value (or NRV) of scrap/by-products. Cost per unit = cost of production ÷ units produced.'],
             'blocks': [t1],
             'analogy': 'Like a recipe card: ingredients (materials), the cook\'s time (direct wages), a fee per dish to the recipe owner (royalty) — that is the prime cost; add the kitchen\'s gas, rent and utensils wearing out (overheads) and you get the factory cost.',
             'work': 'Pricing decisions start from cost per unit. When a client asks "what should I quote for 10,000 units?", the CA builds exactly this ladder before adding office costs and margin.'},
            {'id': 'c3', 'title': 'Direct expenses versus factory overheads; apportionment',
             'body': ['Direct expenses: costs other than materials and wages incurred for a specific product, varying with output — royalty payable per unit produced, hire charges of a machine paid per unit produced, special moulds or designs for one job.',
                      'Factory overheads: indirect costs that cannot be traced to particular units. Indirect material — lubricating oil, cotton waste, small tools, stores used for repairs. Indirect wages — maintenance staff, supervisors, idle-time (holding) pay. Indirect expenses — factory rent, power, depreciation and insurance of plant and factory shed, training of workers.',
                      'Shared expenses are apportioned on a fair basis — rent and rates by floor area, lighting by number of points or as stated. The factory share goes to the Manufacturing Account; the office share to the P&L. Office and selling expenses never enter the Manufacturing Account.'],
             'analogy': 'Royalty per pair of shoes is like a toll paid per car that crosses a bridge (direct, changes with the number of cars). Factory rent is like the bridge\'s maintenance — paid whether 10 or 10,000 cars cross.',
             'work': 'Closing stock is valued using production costs only. If office salaries are wrongly loaded into the Manufacturing Account, closing stock is overvalued and profit overstated — auditors test this classification.'},
            {'id': 'c4', 'title': 'Work-in-progress, scrap and by-products',
             'body': ['Work-in-progress (work-in-process, semi-finished goods): goods on which work has started but is not complete at a date. Opening WIP is debited to the Manufacturing Account (it is finished this year); closing WIP is credited (it is carried forward) and shown as a current asset.',
                      'By-product: a secondary product obtained from the same raw materials and process as the main product without extra effort, usually of small value — molasses in sugar making, buttermilk in a dairy, scrap in steel. Its cost usually cannot be separated, so it is valued at net realisable value.',
                      'Treatment: crediting the sale value (or NRV) of the by-product or scrap to the Manufacturing Account is the correct method, as it lowers the cost of the main product. Showing it as miscellaneous income in P&L is seen in practice but is not preferred.'],
             'analogy': 'WIP is a half-built Lego model left on the table at bedtime — it is carried into tomorrow. A by-product is the pile of wood shavings from a carpenter\'s work that he sells as fuel.',
             'work': 'Physical verification of WIP is tricky — the auditor relies on the production supervisor\'s stage-of-completion estimates and checks them against job cards.'},
            {'id': 'c5', 'title': 'Design of the Manufacturing Account and quantity columns',
             'body': ['There is no fixed format. A common layout — Debit: opening WIP; raw materials consumed (opening + purchases − closing); direct wages; direct expenses (subtotal: prime cost); factory overheads (subtotal: factory cost). Credit: scrap/by-product at NRV; closing WIP; cost of production transferred to the Trading Account (balancing figure).',
                      'Quantity columns help when questions give units instead of all values. The Manufacturing Account carries raw-material quantities (opening, purchased, closing) and the quantity produced; the Trading Account carries finished-goods units (opening, produced, sold, closing). Units sold = opening units + units produced − closing units.',
                      'Unless told otherwise, assume first-in-first-out: the opening stock of finished goods is sold first, so closing stock comes from this year\'s output and is valued at this year\'s cost per unit (or net realisable value, if lower).'],
             'analogy': 'Quantity columns are like a bus conductor\'s count: people on board at the start + those who boarded − those who got off = people still on board.',
             'work': 'Stock registers maintained in units are reconciled with the accounts at year end. A shortage in units that the books do not explain is a red flag for theft or unrecorded sales.'},
            {'id': 'c6', 'title': 'Linking to Trading, P&L and Balance Sheet',
             'body': ['Trading Account: opening finished goods + cost of production vs sales + closing finished goods → gross profit.',
                      'Profit and Loss Account: office and administration expenses, selling and distribution expenses, finance costs, the office share of shared expenses, depreciation on office assets → net profit.',
                      'Balance Sheet: three separate stocks — raw materials, work-in-progress and finished goods — under current assets, plus outstanding factory wages and other year-end items.'],
             'analogy': 'Three rooms of the same house — workshop, showroom, office — each with its own bills, all under one roof (the Balance Sheet).',
             'work': 'Banks often lend against stock with different margins for raw materials, WIP and finished goods. Showing the three stocks separately and correctly matters for the client\'s drawing power.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Building cost per unit', 'difficulty': 'core', 'minutes': 6,
             'q': 'Zenith Tools produced 40,000 units. Direct material cost ₹25 per unit, direct labour ₹12 per unit, and royalty of ₹4 per unit produced is payable to the design owner. Factory overheads for the year were ₹2,40,000. Find prime cost, total manufacturing cost and cost per unit.',
             'solution': [t1, wn('Why royalty is direct', 'Royalty here is paid for every unit produced, so it rises and falls with output and can be traced to each unit — a direct expense, part of prime cost.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Manufacturing and Trading Accounts with quantities', 'difficulty': 'moderate', 'minutes': 18,
             'q': 'Arora Plastics, year ended 31 March 2027: raw materials — opening ₹1,40,000, purchases ₹9,60,000, carriage on purchases ₹20,000, closing ₹1,60,000; direct wages ₹3,20,000; royalty ₹2 per unit produced; factory rent ₹1,20,000; factory power ₹90,000; depreciation of plant ₹60,000; work-in-progress — opening ₹45,000, closing ₹55,000; scrap sold ₹20,000. Units produced 80,000. Finished goods: opening 10,000 units valued at ₹2,00,000; closing 12,000 units; selling price ₹30 per unit. Prepare the Manufacturing Account and Trading Account (assume FIFO; net realisable value exceeds cost).',
             'solution': [mfg2, trd2, wn('Working notes', f'Raw materials consumed {R(rmc)}; prime cost {R(prime)}; factory overheads {R(ovh)}; cost of production {R(cop)} ÷ 80,000 = {R(cpu)} per unit. Units sold = 10,000 + 80,000 − 12,000 = {inr(sold)}. Closing stock 12,000 × ₹21 = {R(cfg)} (FIFO — opening units sold first).')],
             'checks': c2},
            {'id': 'i3', 'title': 'Full final accounts of a manufacturer with apportionment', 'difficulty': 'hard', 'minutes': 35,
             'q': 'From the trial balance of Sharma Industries and the information below, prepare for the year ended 31 March 2027 the Manufacturing Account, the Trading Account and the Profit and Loss Account, and the Balance Sheet on that date. (1) Closing stocks: raw materials ₹70,000; work-in-progress ₹30,000; finished goods ₹90,000. (2) Direct wages outstanding ₹10,000. (3) Depreciate plant and office furniture at 10%. (4) The factory occupies three-fourths of the rented premises. (5) Lighting is to be charged two-thirds to the factory and one-third to the office.',
             'given': [tb(TB3, '31 March 2027', 'Trial Balance of Sharma Industries as at 31 March 2027')],
             'solution': [mfg3, trd3, pl3, bs3,
                          wn('Working notes', f'Raw materials consumed = 60,000 + 4,80,000 + 12,000 − 70,000 = {R(rmc3)}. Prime cost = {inr(rmc3)} + {inr(wg3)} = ₹6,42,000. Overheads = power 36,000 + repairs 9,000 + rent {inr(rf3)} + lighting {inr(lf3)} + depreciation {inr(dp3)} = ₹1,51,000. Cost of production = 6,42,000 + 1,51,000 + 25,000 − 30,000 − 6,000 = {R(cop3)}.')],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Pricing a bulk order from the Manufacturing Account', 'role': 'Cost and finance executive at a small-scale manufacturer',
             'situation': 'A distributor wants a quote for 20,000 units. The owner looks at last year\'s Manufacturing Account (cost of production ₹21 per unit) and wants to quote ₹23.',
             'steps': ['Split last year\'s cost into variable elements (materials, direct wages, royalty per unit) and fixed factory overheads.',
                       'Check current raw-material prices and wage rates — historical figures may be stale.',
                       'Remember that office and selling costs are not in the Manufacturing Account; they also need to be covered.',
                       'Present the owner with variable cost per unit, share of fixed overheads and expected margin at ₹23.'],
             'takeaway': 'The Manufacturing Account gives the factory view of cost; pricing also needs the office and selling costs that sit in P&L.',
             'think': 'Why might quoting on the basis of cost of production alone lead to a loss?',
             'answer': 'Because administration, selling and finance costs (in P&L) are not included in cost of production; if the price only just covers factory cost, these costs remain unrecovered.'},
            {'id': 'j2', 'title': 'Checking stock valuation in a factory audit', 'role': 'Audit senior on a manufacturing client',
             'situation': 'The client values closing finished goods at ₹48 per unit. You notice that the cost sheet includes a share of office salaries and selling commission.',
             'steps': ['Rebuild cost per unit from the Manufacturing Account: materials, direct wages, direct expenses, factory overheads, WIP adjustment and by-product credit.',
                       'Remove office salaries and selling commission — they are period costs charged to P&L, not inventory costs.',
                       'Compare the corrected cost with net realisable value and take the lower.',
                       'Quantify the effect on closing stock and profit and propose the adjustment.'],
             'takeaway': 'Only production costs belong in stock; loading office or selling costs overstates stock and profit.',
             'think': 'If office costs of ₹3 per unit are wrongly included in 10,000 closing units, by how much is profit overstated?',
             'answer': 'By ₹30,000 (10,000 × ₹3), because closing stock (a credit to Trading) is overstated by that amount.',
             'checks': [{'expr': '10000*3', 'value': 30000, 'label': 'Overstatement of closing stock and profit'}]},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Opening raw materials ₹30,000; purchases ₹2,00,000; purchase returns ₹5,000; closing raw materials ₹40,000. Raw materials consumed:', 'options': [R(m_rm), '₹1,95,000', '₹1,90,000', '₹2,25,000'], 'answer': 0, 'check': '30000+200000-5000-40000', 'explain': "Raw materials consumed = opening stock + net purchases − closing stock = 30,000 + (2,00,000 − 5,000) − 40,000 = ₹1,85,000. The trap ₹1,90,000 forgets to deduct purchase returns; ₹1,95,000 is just net purchases, ignoring both stocks. In practice: a factory's stores department reports opening and closing stock each month so that costing can measure materials actually consumed, not merely bought.", 'topic': "Manufacturing Costs", 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'Prime cost is the total of:', 'options': ['Direct materials, direct wages and direct expenses', 'Direct materials and factory overheads', 'Factory cost and office overheads', 'Direct wages and all overheads'], 'answer': 0, 'explain': "Prime cost is the total of all direct costs — direct materials, direct wages and direct expenses — that can be traced to the units produced. Factory overheads are added afterwards to reach factory (works) cost, and office overheads later still. The trap is 'direct materials and factory overheads', which mixes a direct cost with an indirect one. In practice: cost accountants in a pharma plant report prime cost separately because it moves directly with production volume.", 'topic': "Manufacturing Costs", 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Royalty payable at a fixed rate per unit produced is a:', 'options': ['Direct expense', 'Factory overhead', 'Office expense', 'Selling expense'], 'answer': 0, 'explain': "Royalty at a fixed rate per unit produced rises and falls exactly with output and can be traced to each unit, so it is a direct expense and part of prime cost. The trap is 'factory overhead' — overheads are indirect costs that cannot be traced to particular units, such as factory rent. In practice: a garment maker paying a brand licence fee per piece manufactured includes it in the direct cost of every piece when pricing orders.", 'topic': "Manufacturing Costs", 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm4', 'q': 'Closing work-in-progress is shown:', 'options': ['On the credit side of the Manufacturing Account and as a current asset', 'On the debit side of the Manufacturing Account', 'On the credit side of the Trading Account only', 'In the Profit and Loss Account'], 'answer': 0, 'explain': "Closing work-in-progress consists of units started but not finished at year-end. Their cost is deducted from this year's production cost by crediting it to the Manufacturing Account, and it is carried forward as a current asset (part of inventories). The trap is the debit side, which is where opening WIP goes. In practice: auditors of an engineering company physically verify partly-built machines on the shop floor at year-end and check how their stage of completion was costed.", 'topic': "Manufacturing Costs", 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'The preferred treatment of the sale value of a by-product is to:', 'options': ['Credit it to the Manufacturing Account', 'Credit it to the P&L Account as miscellaneous income', 'Add it to closing stock', 'Debit it to the Trading Account'], 'answer': 0, 'explain': "A by-product arises incidentally while making the main product. The preferred treatment is to credit its sale value to the Manufacturing Account, which reduces the cost of producing the main product. The trap is crediting it to Profit and Loss as miscellaneous income — that overstates the main product's cost and understates gross margin. In practice: sugar mills sell molasses and bagasse as by-products, and their realisation is used to reduce the cost of sugar produced.", 'topic': "Manufacturing Costs", 'concept': 'c4', 'difficulty': 'moderate'},
            {'id': 'm6', 'q': 'Prime cost ₹5,00,000; factory overheads ₹1,20,000; opening WIP ₹20,000; closing WIP ₹35,000. Cost of production is:', 'options': [R(m_cop), '₹6,35,000', '₹6,20,000', '₹6,75,000'], 'answer': 0, 'check': '500000+120000+20000-35000', 'explain': "Cost of production = prime cost 5,00,000 + factory overheads 1,20,000 + opening WIP 20,000 − closing WIP 35,000 = ₹6,05,000. Opening WIP is added because those units are finished this year; closing WIP is deducted because they are not yet finished. The trap ₹6,35,000 reverses the two WIP signs. In practice: plant controllers reconcile WIP movements every month so that cost per finished unit is not distorted.", 'topic': "Manufacturing Costs", 'concept': 'c2', 'difficulty': 'moderate'},
            {'id': 'm7', 'q': 'Rent ₹90,000 is shared between factory and office; the factory occupies two-thirds of the area. The amount debited to the Manufacturing Account is:', 'options': [R(m_rent), '₹30,000', '₹90,000', '₹45,000'], 'answer': 0, 'check': '90000*2/3', 'explain': "Rent shared between factory and office is apportioned on a fair basis — here floor area. Factory share = 90,000 × 2/3 = ₹60,000, debited to the Manufacturing Account; the office share of ₹30,000 goes to Profit and Loss. The trap is debiting the whole ₹90,000 to manufacturing, which overstates production cost. In practice: a manufacturer renting one building splits rent, electricity and insurance between plant and office using area, metered usage or headcount.", 'topic': "Manufacturing Costs", 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'Opening finished goods 2,000 units; produced 50,000 units; closing finished goods 4,000 units. Units sold:', 'options': [f'{inr(m_units)} units', '52,000 units', '56,000 units', '46,000 units'], 'answer': 0, 'check': '2000+50000-4000', 'explain': "Units sold = opening finished goods + units produced − closing finished goods = 2,000 + 50,000 − 4,000 = 48,000 units. The trap 52,000 adds both stocks or ignores the closing stock; 56,000 adds the closing stock instead of deducting it. In practice: quantity columns in the Manufacturing and Trading Accounts let a factory accountant reconcile units produced, sold and in stock with the excise-style stock register kept at the plant.", 'topic': "Design of a Manufacturing Account", 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm9', 'q': 'Depreciation on office furniture of a manufacturer is debited to:', 'options': ['Profit and Loss Account', 'Manufacturing Account', 'Trading Account', 'Capital Account'], 'answer': 0, 'explain': "Only depreciation on factory assets such as plant and machinery is a production cost. Office furniture is used for administration, so its depreciation is an office expense debited to Profit and Loss. The trap is the Manufacturing Account, which would overstate the cost of production and closing stock. In practice: when valuing inventory under AS 2, auditors check that administrative costs like office depreciation are not loaded into the stock value.", 'topic': "Manufacturing Costs", 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm10', 'q': 'In the absence of instructions, closing stock of finished goods is assumed to consist of:', 'options': ['Goods produced during the current year (FIFO)', 'The opening stock carried forward', 'An average of opening stock and current production', 'Goods valued at selling price'], 'answer': 0, 'explain': "Unless told otherwise, finished goods are assumed to move on a first-in, first-out basis: opening stock is sold first, so closing stock comes from this year's production and is valued at this year's cost of production per unit. The trap is assuming the opening stock is still lying unsold. In practice: FMCG companies with expiry-dated products physically follow FIFO in their warehouses, so the assumption matches what actually happens.", 'topic': "Design of a Manufacturing Account", 'concept': 'c5', 'difficulty': 'moderate'},
            {'id': 'm11', 'q': 'Lubricating oil used for factory machines is:', 'options': ['Indirect material — a factory overhead', 'Direct material', 'A direct expense', 'A selling expense'], 'answer': 0, 'explain': "Lubricating oil keeps factory machines running but cannot be traced to particular units of output, so it is indirect material and part of factory overheads. The trap is 'direct material' — direct materials, such as steel in a cycle, become part of the product itself. In practice: consumables like lubricants, cotton waste and small tools are booked to factory overheads in a plant's cost records.", 'topic': "Manufacturing Costs", 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm12', 'q': 'Cost of production ₹7,20,000 for 24,000 units. Cost per unit is:', 'options': [R(m_cpu), '₹3', '₹33', '₹24'], 'answer': 0, 'check': '720000/24000', 'explain': "Cost per unit = cost of production ÷ units produced = 7,20,000 ÷ 24,000 = ₹30. The trap ₹3 is a decimal slip (dividing by 2,40,000), and ₹24 confuses the number of units with the cost. In practice: production managers compare cost per unit month by month and with selling price to decide whether a product line is still profitable.", 'topic': "Manufacturing Costs", 'concept': 'c2', 'difficulty': 'core'},
            {'id': 'm13', 'q': 'Raw materials consumed ₹3,00,000; direct wages ₹1,50,000; hire of a special machine at ₹1 per unit for 30,000 units; factory rent ₹40,000. Prime cost is:', 'options': [R(m_prime), '₹5,20,000', '₹4,50,000', '₹4,90,000'], 'answer': 0, 'check': '300000+150000+30000', 'explain': "Prime cost includes only direct costs: materials 3,00,000 + direct wages 1,50,000 + hire of a special machine charged per unit produced, 30,000 × ₹1 = 30,000, giving ₹4,80,000. Factory rent is an overhead, added only when moving to factory cost. The trap ₹5,20,000 includes the rent; ₹4,50,000 leaves out the per-unit hire charge. In practice: job-work and machine-hire charges paid per piece are treated as direct expenses in a factory's cost sheet.", 'topic': "Manufacturing Costs", 'concept': 'c2', 'difficulty': 'moderate'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'ledger',
             'q': 'Neha Plastics, year ended 31 March 2027. Units produced 50,000. Raw materials: opening ₹80,000; purchases ₹6,20,000; freight on purchases ₹15,000; closing ₹95,000. Direct wages ₹2,10,000. Hire of moulding machine at ₹1.50 per unit produced. Factory rent ₹60,000; depreciation of factory plant ₹45,000; indirect wages ₹25,000. Work-in-progress: opening ₹30,000; closing ₹40,000. A by-product was realised for ₹5,000. Finished goods: opening 6,000 units valued at ₹1,14,000; 52,000 units sold at ₹28 each. Prepare the Manufacturing Account and the Trading Account showing cost per unit (assume FIFO; net realisable value is above cost).',
             'model': [mfgq, trdq, wn('Working notes', f'Raw materials consumed {R(qrm)}; prime cost {R(qprime)}; overheads {R(qovh)}; cost of production {R(qcop)}; per unit 10,20,000 ÷ 50,000 = ₹20.40. Closing finished units = 6,000 + 50,000 − 52,000 = {inr(qcl)}; value 4,000 × ₹20.40 = {R(qcfg)}.')],
             'scheme': [{'id': 's1', 'pt': 'Raw materials consumed ₹6,20,000 (freight included)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Direct wages and machine hire as direct expense — prime cost ₹9,05,000', 'm': 1.5, 'skill': 'classification'},
                        {'id': 's3', 'pt': 'Factory overheads ₹1,30,000', 'm': 1, 'skill': 'classification'},
                        {'id': 's4', 'pt': 'WIP adjusted correctly and by-product credited', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's5', 'pt': 'Cost of production ₹10,20,000 and ₹20.40 per unit', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's6', 'pt': 'Closing finished goods 4,000 units at ₹20.40 (FIFO)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's7', 'pt': 'Trading Account with gross profit ₹4,03,600', 'm': 1.5, 'skill': 'presentation'}],
             'remarks': ['Many candidates value closing finished goods at the opening rate (₹19) — FIFO means this year\'s cost applies.', 'Machine hire per unit is frequently placed under overheads, which loses the prime-cost mark.'],
             'mistakes': ['Debiting closing WIP instead of crediting it.', 'Showing the by-product in P&L.', 'Leaving freight on purchases out of raw materials consumed.'],
             'tips': ['Show subtotals: raw materials consumed, prime cost, factory cost, cost of production.', 'Keep a units column in both accounts so the quantities visibly balance.'],
             'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'Classify each item as direct material, direct wages, direct expense, factory overhead, or office/selling expense (to P&L): (1) carriage on raw materials; (2) wages of machine operators; (3) royalty per unit produced; (4) depreciation of factory building; (5) salary of the factory supervisor; (6) advertisement; (7) cotton waste and lubricants; (8) hire charges of a machine per unit produced; (9) office rent; (10) insurance of plant.',
             'model': [table(['Item', 'Classification', 'Where shown'], [
                 ['(1) Carriage on raw materials', 'Direct material (part of cost of materials)', 'Manufacturing A/c'],
                 ['(2) Wages of machine operators', 'Direct wages', 'Manufacturing A/c'],
                 ['(3) Royalty per unit produced', 'Direct expense', 'Manufacturing A/c'],
                 ['(4) Depreciation of factory building', 'Factory overhead', 'Manufacturing A/c'],
                 ['(5) Factory supervisor\'s salary', 'Factory overhead (indirect wages)', 'Manufacturing A/c'],
                 ['(6) Advertisement', 'Selling expense', 'P&L A/c'],
                 ['(7) Cotton waste and lubricants', 'Factory overhead (indirect material)', 'Manufacturing A/c'],
                 ['(8) Machine hire per unit produced', 'Direct expense', 'Manufacturing A/c'],
                 ['(9) Office rent', 'Office (administration) expense', 'P&L A/c'],
                 ['(10) Insurance of plant', 'Factory overhead', 'Manufacturing A/c']])],
             'scheme': [{'id': f's{i}', 'pt': f'Item ({i}) correctly classified', 'm': 0.5, 'skill': 'classification'} for i in range(1, 11)],
             'remarks': ['Supervisor\'s salary and lubricants are the usual traps — they are factory overheads, not direct costs.'],
             'mistakes': ['Treating royalty per unit as an overhead.', 'Putting office rent into the Manufacturing Account.'],
             'tips': ['Ask: can it be traced to each unit? Is it incurred in the factory?']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'State the purposes of preparing a Manufacturing Account.',
             'model': [ul(['It shows the total cost of producing the finished goods, with each element — materials, wages, direct expenses and overheads — shown separately.',
                           'It gives the factory cost, which helps reconcile the financial accounts with the cost records.',
                           'It allows comparison of manufacturing costs and efficiency from one period to another.',
                           'If finished output is transferred to the Trading Account at market price, it shows the profit or loss on manufacturing; it can also be used to fix production-linked bonus.'])],
             'scheme': [{'id': f's{i}', 'pt': t, 'm': 1, 'skill': 'concept'} for i, t in enumerate(['Total cost with elements', 'Reconciliation with cost records', 'Period-to-period comparison', 'Manufacturing profit / bonus'], 1)],
             'remarks': ['Answers that only say "to find cost" score one mark; examiners expect the reconciliation and comparison points.'],
             'mistakes': ['Saying the Manufacturing Account shows gross profit.'],
             'tips': ['Four numbered points, one line each.']},
        ],
        'revision': {
            'summary': ['Raw materials consumed = opening + net purchases (+ carriage) − closing.', 'Prime cost = materials consumed + direct wages + direct expenses.',
                        'Factory cost = prime cost + factory overheads (indirect material, wages, expenses).', 'Cost of production = factory cost + opening WIP − closing WIP − scrap/by-product.',
                        'Cost of production goes to the Trading Account; office and selling costs go to P&L; three stocks appear in the Balance Sheet.',
                        'Quantities: units sold = opening + produced − closing; closing stock at current-year cost (FIFO) unless NRV is lower.'],
            'remember': ['Royalty/hire per unit produced = direct expense.', 'Opening WIP debit; closing WIP credit.', 'Apportion rent and lighting between factory and office as instructed.'],
            'traps': ["Don't put office salaries or selling costs in the Manufacturing Account.", "Don't value closing finished goods at the opening stock rate.", "Don't show by-product sales as miscellaneous income when the question asks for the correct treatment."],
        },
        'quickref': [
            {'k': 'Raw materials consumed', 'v': 'Opening RM + purchases − returns + carriage inwards − closing RM'},
            {'k': 'Prime cost', 'v': 'RM consumed + direct wages + direct expenses'},
            {'k': 'Overheads', 'v': 'Indirect material + indirect wages + indirect expenses'},
            {'k': 'Factory (works) cost', 'v': 'Prime cost + factory overheads'},
            {'k': 'Cost of production', 'v': 'Factory cost + opening WIP − closing WIP − scrap/by-product (NRV)'},
            {'k': 'Cost per unit', 'v': 'Cost of production ÷ units produced'},
            {'k': 'Units sold', 'v': 'Opening finished units + units produced − closing finished units'},
            {'k': 'Closing finished goods', 'v': 'FIFO: closing units × current-year cost per unit (or NRV if lower)'},
        ],
        'viva': viva, 'cases': cases,
    }
