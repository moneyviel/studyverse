"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 1 Ind AS 2 Inventories.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u01'
T1 = 'Scope and measurement principle'
T2 = 'Cost of inventories: purchase, conversion and other costs'
T3 = 'Cost formulas'
T4 = 'Net realisable value and write-downs'


def build():
    ck = Checks()
    rate = ck.add('2400000/100000', 'Fixed overhead per unit at normal capacity (₹)')
    unitc = ck.add('150+60+24', 'Cost per unit (₹)')
    stock = ck.add('15000*234', 'Closing inventory at cost (₹)')
    unabs = ck.add('2400000-70000*24', 'Unallocated fixed overhead expensed (₹)')
    i1 = {'id': 'i1', 'title': 'Low production year', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Normal capacity is 1,00,000 units a year; this year only 70,000 units were produced and 55,000 sold. Material cost ₹150 per unit; direct labour and variable overheads ₹60 per unit; fixed production overheads ₹24,00,000. Compute cost per unit, closing inventory and the fixed overhead to be expensed.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Fixed overhead rate', '24,00,000 ÷ normal capacity 1,00,000', '₹' + inr(rate)],
              ['Cost per unit', '150 + 60 + 24', '₹' + inr(unitc)],
              ['Closing inventory', '15,000 units × ₹234', '₹' + inr(stock)],
              ['Unallocated fixed overhead (expense)', '24,00,000 − 70,000 × 24', '₹' + inr(unabs)]], title='Ind AS 2 — conversion costs'),
              note('Low production does not raise the overhead per unit; the unabsorbed amount is expensed. In abnormally high production, the rate is reduced so inventory is not above cost.')],
          'checks': list(ck)}

    ck2 = Checks()
    fg = ck2.add('2000*(500-480)', 'Write-down of finished goods (₹)')
    i2 = {'id': 'i2', 'title': 'NRV item by item', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'At year end: (a) 2,000 finished units cost ₹500 each; expected selling price ₹520 less selling costs ₹40. (b) Raw material A cost ₹1,00,000, replacement cost ₹80,000; it will be used in products expected to sell above cost. (c) Raw material B cost ₹50,000, replacement cost ₹42,000; the related finished product will sell below cost. Determine the carrying amounts.',
          'solution': [table(['Item', 'Treatment', 'Carrying amount ₹'], [
              ['(a) Finished goods', 'NRV ₹480 < cost ₹500: write down ₹' + inr(fg), inr(2000 * 480)],
              ['(b) Raw material A', 'Not written down — finished product sells above cost', inr(100000)],
              ['(c) Raw material B', 'Written down; replacement cost may be the best measure of NRV', inr(42000)]], title='Net realisable value')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 2 covers inventories: goods kept for normal sale, goods being made for such sale, and materials or supplies to be used up in production or in providing services.',
            'It does not cover financial instruments, living plants and animals in farming and farm produce up to the point of harvest (Ind AS 41), or work in progress under construction contracts accounted under Ind AS 115. Measurement rules do not apply to producers of agricultural and forest products and minerals measured at net realisable value under established industry practice, or to commodity broker-traders measuring at fair value less costs to sell (changes in profit or loss).',
            'The measurement rule: carry inventory at cost or, if lower, at net realisable value.'],
          'Stock is carried at what it cost, unless it can no longer be sold for that much.',
          'Harvested tea leaves enter inventory at fair value less costs to sell under Ind AS 41, which becomes their "cost".'),
        C('c2', T2, [
            'Cost of purchase: purchase price, import duties and non-recoverable taxes, transport, handling and other directly attributable costs, less trade discounts and rebates. Recoverable taxes like GST input credit are excluded.',
            'Cost of conversion: direct labour and a systematic allocation of fixed and variable production overheads. Fixed overheads are allocated on normal capacity; unallocated overheads in low-production periods are expensed; in abnormally high production, the allocation is reduced.',
            'Other costs are included only to bring inventories to their present location and condition (e.g. design costs for specific customers). Excluded: abnormal wastage, storage costs unless necessary in production before a further stage, administrative overheads not contributing to location and condition, and selling costs. Borrowing costs are included only in limited cases under Ind AS 23. Purchases on deferred settlement terms: the difference over normal credit price is interest expense.',
            'Joint products: costs are allocated on a rational and consistent basis (e.g. relative sales value); by-products of small value are measured at NRV and deducted from the main product\'s cost.'],
          'Cost includes everything needed to make the goods ready — and nothing that merely happens to coincide.',
          'Storage of whisky during maturation is part of cost; storage of finished cartons waiting for sale is not.'),
        C('c3', T3, [
            'Specific identification is used for items not ordinarily interchangeable and for goods or services produced and segregated for specific projects.',
            'Other inventories use first-in, first-out (FIFO) or weighted average cost. The same formula is used for all inventories of a similar nature and use; different formulas may be justified for inventories of different nature or use (but not merely different locations or tax rules). LIFO is not permitted.',
            'Short-cut techniques such as standard costing or the retail method are acceptable when they give results close to actual cost; standards need regular review.'],
          'The cost formula must reflect how goods are actually used, consistently across similar items.',
          'A jeweller with unique pieces uses specific identification; a cement maker uses weighted average.'),
        C('c4', T4, [
            'Net realisable value is what the entity expects to get when selling in the normal course, minus the further costs to finish the item and to sell it — an entity-specific value, unlike fair value.',
            'Write-downs are usually item by item, or by groups of similar or related items; not by broad classes like "finished goods". Estimates use the most reliable evidence at the time, considering events after the reporting date that confirm conditions at year end, and the purpose for which inventory is held (e.g. fixed sales contracts).',
            'Materials kept for production stay at cost so long as the products they go into are expected to sell at or above cost; if a decline in material price indicates the finished product\'s cost exceeds NRV, materials are written down — replacement cost may be the best available measure.',
            'Write-downs are expensed; reversals (when circumstances change) are limited to the original write-down and reduce the expense in the period of reversal. Carrying amount of inventory sold is expensed when revenue is recognised.'],
          'Net realisable value tests whether today\'s stock can still pay for itself.',
          'Stock held to fulfil a firm order uses the contract price for NRV, not the general market price.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end inventory valuation', 'role': 'Audit senior',
             'situation': 'A manufacturer had a strike, so production was 40% below normal.',
             'steps': ['Recompute fixed overhead absorption at normal capacity.', 'Expense unabsorbed overheads.', 'Test NRV item by item using post-year-end sales.', 'Check materials only where finished goods fall below cost.'],
             'takeaway': 'Low output must not inflate inventory values.'}]

    mcqs = [
        Q('m1', 'Inventories are measured at:', ['Lower of cost and net realisable value', 'Fair value', 'Replacement cost', 'Higher of cost and NRV'], 0,
          'The basic rule of Ind AS 2. In practice: NRV is entity-specific.', 'c1', T1),
        Q('m2', 'Fixed production overheads are allocated to inventory based on:', ['Normal capacity', 'Actual production always', 'Maximum capacity', 'Sales volume'], 0,
          'Normal capacity prevents low output inflating unit costs. In practice: actual may be used if close to normal.', 'c2', T2),
        Q('m3', 'Which cost is excluded from inventory?', ['Selling costs', 'Import duties', 'Direct labour', 'Inward freight'], 0,
          'Selling and most admin costs are expensed. In practice: storage between production stages may be included.', 'c2', T2),
        Q('m4', 'LIFO under Ind AS 2 is:', ['Not permitted', 'Permitted', 'Required for metals', 'Optional for traders'], 0,
          'Only specific identification, FIFO and weighted average are allowed. In practice: retail method may approximate cost.', 'c3', T3),
        Q('m5', 'Raw materials are written down below cost when:', ['The finished goods in which they are used will sell below cost', 'Their replacement cost falls', 'Prices fall slightly', 'Always at year end'], 0,
          'If the finished product still recovers cost, materials stay at cost. In practice: replacement cost can measure NRV.', 'c4', T4),
        Q('m6', 'Estimated selling price ₹900; costs to complete ₹150; selling costs ₹50; cost ₹750. Carrying amount:', ['₹700', '₹750', '₹900', '₹850'], 0,
          'NRV = 900 − 150 − 50 = 700, lower than cost. In practice: write down ₹50.', 'c4', T4, 'moderate', check=700),
        Q('m7', 'A reversal of an earlier inventory write-down is:', ['Limited to the amount of the original write-down', 'Unlimited', 'Not allowed', 'Credited to OCI'], 0,
          'Carrying amount is the lower of cost and revised NRV. In practice: reduces cost of sales.', 'c4', T4),
        Q('m8', 'Commodity broker-traders may measure inventories at:', ['Fair value less costs to sell, with changes in profit or loss', 'Cost only', 'Lower of cost and NRV only', 'Replacement cost'], 0,
          'They are outside the measurement rules of Ind AS 2. In practice: disclose the policy.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Overhead rate', 1.5, 'computation', 'normal', nums=[rate]), S('s2', 'Unit cost and stock', 2, 'computation', 'inventory', nums=[unitc, stock]),
           S('s3', 'Unallocated overhead', 2.5, 'computation', 'unallocated|expense', nums=[unabs])],
          ['Use normal capacity.'], ['Dividing fixed overhead by actual output.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Finished goods', 2, 'computation', 'NRV', nums=[fg]), S('s2', 'Material A', 1.5, 'concept', 'not written'), S('s3', 'Material B', 1.5, 'concept', 'replacement')],
          ['Test each item.'], ['Writing down material A.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is included in the cost of inventories?', 'Costs of purchase, costs of conversion and other costs incurred to bring the inventories to their present location and condition.',
          [P('p1', 'Purchase and conversion', 5, 'purchase|conversion'), P('p2', 'Location and condition', 5, 'location|condition')], 'c2'),
        V('v2', 'How are fixed overheads absorbed in a low-production year?', 'At the rate based on normal capacity, with the unabsorbed overhead recognised as an expense.',
          [P('p1', 'Normal capacity', 6, 'normal capacity'), P('p2', 'Expense excess', 4, 'expense|unabsorbed')], 'c2'),
        V('v3', 'Which cost formulas are allowed?', 'Specific identification for non-interchangeable items, and FIFO or weighted average for others; LIFO is prohibited.',
          [P('p1', 'FIFO and weighted', 5, 'fifo|weighted'), P('p2', 'Specific identification', 5, 'specific')], 'c3'),
        V('v4', 'Define net realisable value.', 'The price the entity expects to sell at in its normal business, minus the costs still needed to complete and sell the item.',
          [P('p1', 'Expected price', 5, 'price|sell'), P('p2', 'Less costs', 5, 'complete|costs')], 'c4'),
        V('v5', 'Can inventory write-downs be reversed?', 'Yes, when circumstances change, up to the original write-down, recognised as a reduction of expense in that period.',
          [P('p1', 'Allowed', 4, 'yes|revers'), P('p2', 'Limited', 6, 'original|limit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Shakti Steels Ltd.', 'difficulty': 'moderate',
              'case': 'Shakti Steels Ltd. bought iron ore for ₹2 crore plus non-refundable customs duty ₹20 lakh, GST ₹36 lakh (credit available) and freight ₹10 lakh. It paid ₹5 lakh for storing finished coils awaiting dispatch and ₹3 lakh for abnormal wastage in a furnace accident. Steel prices fell after year end below cost for one product line.',
              'mcqs': [
                  M('k1a', 'Cost of the iron ore (₹ lakh):', ['230', '266', '200', '236'], 0,
                    '200 + 20 duty + 10 freight; GST credit is recoverable and excluded. In practice: trade discounts would be deducted.', 'moderate', check=230, topic=T2),
                  M('k1b', 'Storage of finished coils awaiting dispatch is:', ['Expensed', 'Added to inventory', 'Capitalised to PPE', 'Deferred'], 0,
                    'Storage is included only if necessary in production before a further stage. In practice: warehouse rent for finished goods is an expense.', 'core', topic=T2),
                  M('k1c', 'The abnormal wastage of ₹3 lakh is:', ['Expensed', 'Included in inventory cost', 'Capitalised', 'Shown in OCI'], 0,
                    'Abnormal waste is excluded from cost. In practice: normal process losses are absorbed.', 'core', topic=T2),
                  M('k1d', 'The post-year-end price fall for one product line:', ['May evidence NRV below cost at year end, requiring write-down if it confirms year-end conditions', 'Is always ignored', 'Requires writing down all inventory', 'Is a change in policy'], 0,
                    'Post-year-end evidence is considered if it relates to conditions at year end; apply item by item. In practice: Ind AS 10 interplay.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 1, 'Ind AS 2 "Inventories"',
                ['Identify the scope of Ind AS 2 and the measurement rule.',
                 'Compute the cost of inventories, including overhead absorption.',
                 'Apply cost formulas.',
                 'Determine NRV and account for write-downs and reversals.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['fin-p1-ch04-u03'],
                 'exam_tip': 'Show the normal-capacity overhead rate and the unabsorbed amount separately — both earn marks.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Lower of cost and NRV.',
                             'Cost = purchase + conversion + other costs to location and condition.',
                             'Fixed overheads on normal capacity; unabsorbed expensed.',
                             'FIFO / weighted average / specific identification; no LIFO.',
                             'NRV item by item; materials written down only if product below cost; reversals capped.'],
                 'remember': ['Recoverable taxes excluded from cost.'],
                 'traps': ['Selling and abnormal costs never enter inventory.']},
                [('Measurement', 'Lower of cost and NRV'), ('Fixed OH', 'Normal capacity'), ('Formulas', 'FIFO, WAC, specific'), ('NRV', 'SP − completion − selling')],
                viva, cases)
