"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 1 — AS 2 Valuation of Inventories.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u01'
T1 = 'Meaning and scope of inventories'
T2 = 'Cost of purchase and cost of conversion'
T3 = 'Fixed overheads, joint products and costs excluded'
T4 = 'Cost formulas and techniques'
T5 = 'Net realisable value and disclosure'


def build():
    ck = Checks()
    fo = ck.add('600000/20000', 'Fixed overhead per unit at normal capacity (₹)')
    cpu = ck.add('50+30', 'Cost per unit (₹)')
    un = ck.add('600000-15000*30', 'Unallocated fixed overhead expensed (₹)')
    val = ck.add('3000*min(80,75)', 'Closing inventory at lower of cost and NRV (₹)')
    i1 = {'id': 'i1', 'title': 'Low production year', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Jyoti Ltd.\'s normal capacity is 20,000 units a year. This year it produced 15,000 units. Variable cost is ₹50 per unit and fixed production overheads are ₹6,00,000. 3,000 units remain unsold; their net realisable value is ₹75 per unit. Value the closing inventory and state the treatment of fixed overheads.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Fixed overhead per unit', '6,00,000 ÷ 20,000 (normal capacity)', R(fo)],
              ['Cost per unit', '50 + 30', R(cpu)],
              ['Unallocated fixed overhead (expense)', '6,00,000 − 15,000 × 30', inr(un)],
              ['Closing inventory', '3,000 × lower of 80 and 75', inr(val)]], title='AS 2 valuation'),
              note('Using actual production (₹40 a unit) would load idle-capacity cost into inventory, which AS 2 does not allow.')],
          'checks': list(ck)}

    ck2 = Checks()
    a = ck2.add('1000*200', 'Raw material at cost — case (a) (₹)')
    b = ck2.add('1000*180', 'Raw material at replacement cost — case (b) (₹)')
    i2 = {'id': 'i2', 'title': 'Should raw material be written down?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Rupa Ltd. holds 1,000 kg of raw material bought at ₹200 per kg; replacement cost has fallen to ₹180. The finished product using it costs ₹900 per unit. Value the raw material if the finished product\'s NRV is (a) ₹950 and (b) ₹850.',
          'solution': [table(['Case', 'Reasoning', '₹'], [
              ['(a) NRV ₹950 > cost ₹900', 'Finished goods sell above cost — no write-down of material', inr(a)],
              ['(b) NRV ₹850 < cost ₹900', 'Material written down; replacement cost is the best measure of NRV', inr(b)]], title='Materials and NRV')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Inventories are assets kept for selling in normal trade, goods still being made for such sale, and materials or supplies that will be used up in making goods or providing services.',
            'AS 2 does not cover work in progress under construction contracts (AS 7), work in progress of service providers, shares and other financial instruments held as stock-in-trade, and producers\' livestock, agricultural and forest products, mineral oils, ores and gases measured at net realisable value by established trade practice.',
            'Machinery spares used only with a particular fixed asset and used irregularly are accounted for under AS 10, not as inventory.',
            'Inventories are measured at the lower of cost and net realisable value.'],
          'Inventory is what you will sell, are making, or will use up in making.',
          'A car dealer\'s cars are inventory; its showroom furniture is not.'),
        C('c2', T2, [
            'Cost of inventories comprises cost of purchase, cost of conversion and other costs incurred to bring them to their present location and condition.',
            'Cost of purchase: purchase price, import duties and other non-recoverable taxes, freight inwards, handling and other directly attributable costs, less trade discounts, rebates and duty drawbacks. Recoverable taxes such as GST input credit are excluded.',
            'Cost of conversion: direct labour and a systematic allocation of fixed and variable production overheads.',
            'Other costs are included only if they bring inventory to its present location and condition — for example design costs for a specific customer. Interest is normally excluded (see AS 16).'],
          'Cost is everything spent to get the goods where they are, in the state they are in.',
          'Freight to bring raw cotton to the mill is cost; freight to deliver cloth to customers is not.'),
        C('c3', T3, [
            'Fixed production overheads are allocated on the basis of normal capacity — the production expected on average over several periods under normal conditions. Actual production may be used if close to normal.',
            'In a low-production year the fixed overhead per unit is not increased; unallocated overheads are expensed. In an abnormally high-production year, the amount per unit is reduced so inventories are not measured above cost. Variable overheads are allocated on actual use.',
            'Joint products are costed on a rational and consistent basis, such as relative sales value; immaterial by-products are measured at NRV and deducted from the cost of the main product.',
            'Excluded from cost: abnormal waste of materials, labour or overheads; storage costs (unless necessary between production stages); administrative overheads not related to bringing inventory to its present location and condition; and selling and distribution costs.'],
          'Idle capacity is a cost of the period, not of the stock.',
          'Storing whisky to mature is part of production; storing finished bottles in a warehouse is not.'),
        C('c4', T4, [
            'Specific identification is used for items that are not ordinarily interchangeable or are made for specific projects.',
            'Other items use FIFO or weighted average cost; the formula chosen should fairly reflect the cost of bringing items to their present location and condition, applied consistently.',
            'Standard cost or the retail method may be used if results approximate actual cost. Standard costs are regularly reviewed; the retail method reduces sales value by the appropriate gross margin, used where many rapidly changing items with similar margins are held.'],
          'Use the formula that best mirrors how goods actually flow and cost.',
          'A jeweller tracks each custom necklace by specific identification; a grocer uses FIFO.'),
        C('c5', T5, [
            'Net realisable value (NRV) is what the item is expected to fetch in normal trading, minus the expected cost to finish it and the costs needed to sell it.',
            'Inventories are written down to NRV usually item by item; groups of similar or related items may be combined. Writing down a whole class (for example all finished goods) is not appropriate.',
            'Materials held for production keep their cost value so long as the goods made from them are expected to fetch at least their cost. If a fall in material prices shows that finished goods cost more than NRV, the materials are written down; replacement cost may be the best measure.',
            'NRV is reassessed each period. Disclose the accounting policies including cost formula, total carrying amount and its classification into suitable heads, such as materials, partly made goods, finished output, goods bought for resale, stores and tools.'],
          'Never carry stock at more than you expect to get for it.',
          'Damaged stock costing ₹10,000 that can be sold for ₹7,000 after ₹1,000 repair costs is valued at ₹6,000.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end stock valuation', 'role': 'Audit assistant',
             'situation': 'A factory ran at 60% capacity due to a strike and includes all fixed overheads in closing stock.',
             'steps': ['Find normal capacity from past years.', 'Recompute fixed overhead per unit.', 'Expense the unallocated overhead.', 'Compare cost with NRV item by item.'],
             'takeaway': 'Abnormal idle time cannot inflate inventory.'}]

    mcqs = [
        Q('m1', 'Which is NOT covered by AS 2?', ['Shares held as stock-in-trade', 'Raw materials of a manufacturer', 'Finished goods of a trader', 'Stores and spares for consumption'], 0,
          'Shares and other financial instruments held as stock-in-trade are outside AS 2, as are construction work in progress and some producers\' agricultural and mineral products. Ordinary trading and manufacturing inventories are covered. In practice: check the exclusions.', 'c1', T1),
        Q('m2', 'Which cost is included in the cost of inventory?', ['Freight inwards on raw materials', 'Selling commission', 'Abnormal wastage', 'General administration not related to production'], 0,
          'Cost of purchase includes freight and handling to bring goods to their present location. Selling costs, abnormal waste and unrelated administration are excluded and expensed. In practice: separate inward and outward freight.', 'c2', T2),
        Q('m3', 'GST paid on purchases for which input credit is available is:', ['Excluded from the cost of inventory', 'Included in cost', 'Added to NRV', 'Shown as a separate inventory'], 0,
          'Only non-recoverable taxes form part of cost of purchase. GST for which input credit is available is recoverable from the authorities and is therefore excluded. In practice: record it as a receivable or credit.', 'c2', T2),
        Q('m4', 'Normal capacity 50,000 units; fixed overheads ₹10,00,000; actual production 40,000 units. Fixed overhead absorbed per unit:', ['₹20', '₹25', '₹10', '₹30'], 0,
          'Fixed production overheads are allocated on normal capacity: ₹10,00,000 ÷ 50,000 = ₹20 a unit. The unabsorbed ₹2,00,000 is expensed. Actual production is used only if close to normal. In practice: document normal capacity.', 'c3', T3, 'moderate', check=20),
        Q('m5', 'A by-product of immaterial value is usually:', ['Measured at NRV and deducted from the cost of the main product', 'Valued at full cost', 'Ignored', 'Valued at selling price'], 0,
          'Where by-products are immaterial, AS 2 allows them to be measured at net realisable value, which is then deducted from the cost of the main product, so the main product carries the joint cost. In practice: material by-products are costed separately.', 'c3', T3),
        Q('m6', 'Which cost formula is required for items made for a specific project?', ['Specific identification', 'FIFO', 'Weighted average', 'Retail method'], 0,
          'Items not ordinarily interchangeable, and goods or services produced and segregated for specific projects, are assigned their individual costs by specific identification. Other items use FIFO or weighted average. In practice: keep job records.', 'c4', T4),
        Q('m7', 'LIFO for valuing inventories under AS 2 is:', ['Not permitted', 'Permitted if consistent', 'Required for traders', 'Permitted with disclosure'], 0,
          'AS 2 allows specific identification, FIFO or weighted average, with standard cost or retail method as approximations. LIFO is not an allowed formula. In practice: auditors will object to LIFO.', 'c4', T4),
        Q('m8', 'Estimated selling price ₹500, cost to complete ₹60, selling costs ₹40, cost ₹420. Inventory is valued at:', ['₹400', '₹420', '₹440', '₹500'], 0,
          'NRV = 500 − 60 − 40 = ₹400, which is below cost of ₹420, so the item is written down to ₹400. Inventory is always carried at the lower of cost and NRV. In practice: compare item by item.', 'c5', T5, 'moderate', check=400),
        Q('m9', 'Raw materials are not written down below cost when:', ['Finished products in which they are used will sell at or above cost', 'Their replacement cost falls', 'Their market price falls', 'They are imported'], 0,
          'A fall in raw material price alone does not justify a write-down if the finished products are expected to be sold at or above cost. Only when finished goods cost exceeds NRV are materials written down. In practice: check finished goods margins.', 'c5', T5),
        Q('m10', 'Writing inventories down to NRV is normally done:', ['Item by item, or for groups of similar items', 'For all inventory as one class', 'For all finished goods together', 'Only for raw materials'], 0,
          'AS 2 requires write-downs on an item-by-item basis, though similar or related items may be grouped. Writing down a whole classification such as all finished goods is not appropriate. In practice: identify slow-moving items.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Normal capacity rate', 1.5, 'computation', 'normal', nums=[fo]),
           S('s2', 'Unallocated overhead expensed', 1.5, 'computation', 'unallocated|expense', nums=[un]),
           S('s3', 'Lower of cost and NRV', 2, 'computation', 'lower', nums=[val])],
          ['Use normal capacity.'], ['Dividing fixed overheads by actual output.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'No write-down when FG above cost', 2, 'concept', 'above cost', nums=[a]),
           S('s2', 'Replacement cost when FG below cost', 2, 'computation', 'replacement', nums=[b])],
          ['Test the finished product first.'], ['Writing down because replacement cost fell.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'How are inventories measured under AS 2?', 'At the lower of cost and net realisable value.',
          [P('p1', 'Lower of', 5, 'lower'), P('p2', 'Cost and NRV', 5, 'net realisable|nrv')], 'c1'),
        V('v2', 'What does cost of inventories include?', 'Cost of purchase, cost of conversion and other costs incurred to bring the inventories to their present location and condition.',
          [P('p1', 'Purchase and conversion', 6, 'purchase', 'conversion'), P('p2', 'Location and condition', 4, 'location|condition')], 'c2'),
        V('v3', 'How are fixed production overheads allocated?', 'On the basis of the normal capacity of the production facilities; unallocated overheads in low-production years are expensed.',
          [P('p1', 'Normal capacity', 6, 'normal capacity'), P('p2', 'Unallocated expensed', 4, 'expens|unallocated')], 'c3'),
        V('v4', 'What is net realisable value?', 'The price the item is expected to fetch in normal trade, after deducting the expected cost to complete it and the costs needed to sell it.',
          [P('p1', 'Expected price', 4, 'price|fetch'), P('p2', 'Less completion and selling costs', 6, 'complete|completion', 'sell')], 'c5'),
        V('v5', 'Which cost formulas are allowed?', 'Specific identification for non-interchangeable items; otherwise FIFO or weighted average, with standard cost or retail method as approximations.',
          [P('p1', 'FIFO / weighted average', 6, 'fifo|weighted'), P('p2', 'Specific identification', 4, 'specific')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Swarna Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Swarna Textiles Ltd. includes in closing stock: ₹40,000 of showroom rent, ₹25,000 of freight to customers, ₹15,000 of abnormal wastage, and ₹30,000 of factory supervisor salary relating to the stock. A batch of fabric costing ₹2,00,000 can be sold for ₹1,90,000 after ₹6,000 selling costs.',
              'mcqs': [
                  M('k1a', 'Which item may remain in inventory cost?', ['Factory supervisor salary', 'Showroom rent', 'Freight to customers', 'Abnormal wastage'], 0,
                    'Production overheads like factory supervision are part of conversion cost. Showroom rent and outward freight are selling costs and abnormal waste is expensed, so all three must be removed. In practice: review overhead pools.', 'core', topic=T3),
                  M('k1b', 'Total amount to be removed from inventory cost:', ['₹80,000', '₹1,10,000', '₹55,000', '₹40,000'], 0,
                    'Showroom rent ₹40,000, outward freight ₹25,000 and abnormal wastage ₹15,000 total ₹80,000, all of which are expensed rather than carried in stock. In practice: adjust before the NRV test.', 'moderate', check=80000, topic=T3),
                  M('k1c', 'The fabric batch is valued at:', ['₹1,84,000', '₹1,90,000', '₹2,00,000', '₹1,96,000'], 0,
                    'NRV is ₹1,90,000 less ₹6,000 selling costs = ₹1,84,000, which is below cost of ₹2,00,000, so the batch is written down to ₹1,84,000. In practice: record the write-down as an expense.', 'moderate', check=184000, topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 1, 'Accounting Standard 2 Valuation of Inventory',
                ['Identify inventories and the scope of AS 2.',
                 'Compute cost of purchase and conversion, including fixed overheads on normal capacity.',
                 'Apply cost formulas and techniques.',
                 'Measure net realisable value and value inventories at the lower of cost and NRV.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['int-p1-ch04-u07'],
                 'exam_tip': 'Always compute fixed overheads on normal capacity, then compare cost with NRV item by item.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Lower of cost and NRV.', 'Cost = purchase + conversion + other costs to present location and condition.',
                             'Fixed overheads on normal capacity; unabsorbed expensed.', 'Exclude abnormal waste, storage, unrelated admin, selling costs.',
                             'Specific identification, FIFO, weighted average; standard cost/retail as approximations.', 'Materials not written down if finished goods sell above cost.'],
                 'remember': ['GST input credit is not cost.'],
                 'traps': ['LIFO is not allowed.', 'Do not write down a whole class at once.']},
                [('Valuation', 'Lower of cost and NRV'), ('Fixed overheads', 'Normal capacity'), ('Formulas', 'Specific ID · FIFO · weighted average')],
                viva, cases)
