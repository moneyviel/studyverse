"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 2 Material Cost.
Scope follows the ICAI study material (May 2027 onwards); explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch02-u01'
T1 = 'Material control: aims, needs and elements'
T2 = 'Procurement procedure and the documents'
T3 = 'Stores, storage and records'
T4 = 'Economic order quantity'
T5 = 'Stock levels: re-order, minimum, maximum, average, danger'
T6 = 'Selective control: ABC, FSN, VED, HML and JIT'
T7 = 'Ratios, physical verification and discrepancies'
T8 = 'Pricing material issues: FIFO, LIFO, averages and others'
T9 = 'Returns, shortages and losses of material'


def build():
    ck = Checks()
    eoq = ck.add('(2*12000*600/10)**0.5', 'EOQ = √(2AO/C)')
    n_ord = ck.add('12000/((2*12000*600/10)**0.5)', 'number of orders a year')
    oc = ck.add('12000/((2*12000*600/10)**0.5)*600', 'annual ordering cost')
    cc = ck.add('((2*12000*600/10)**0.5)/2*10', 'annual carrying cost (average stock × C)')
    tvc = ck.add('12000/((2*12000*600/10)**0.5)*600+((2*12000*600/10)**0.5)/2*10', 'total ordering + carrying cost at EOQ')
    oc2 = ck.add('12000/2000*600', 'ordering cost if 2,000 units are ordered each time')
    cc2 = ck.add('2000/2*10', 'carrying cost if 2,000 units are ordered each time')
    tvc2 = ck.add('12000/2000*600+2000/2*10', 'total if 2,000 units are ordered each time')
    i1 = {'id': 'i1', 'title': 'EOQ and why it is the cheapest order size', 'difficulty': 'core', 'minutes': 8,
          'q': 'Annual requirement of a component is 12,000 units, purchase price ₹80, cost of placing an order ₹600 and carrying cost 12.5% of the unit price per annum. Compute the EOQ, the number of orders, and the annual ordering, carrying and total cost. Compare with ordering 2,000 units at a time.',
          'solution': [wn('Carrying cost per unit', 'C = 12.5% × ₹80 = ₹10 per unit per annum.'),
                       wn('EOQ', f'√(2 × 12,000 × 600 ÷ 10) = √14,40,000 = {inr(eoq)} units; orders a year = 12,000 ÷ {inr(eoq)} = {n_ord}.'),
                       table(['Order size', 'Ordering cost ₹', 'Carrying cost ₹', 'Total ₹'], [
                           [f'{inr(eoq)} (EOQ)', inr(oc), inr(cc), inr(tvc)], ['2,000', inr(oc2), inr(cc2), inr(tvc2)]], title='Cost comparison'),
                       note('At EOQ, ordering cost equals carrying cost; any other order size gives a higher total.')],
          'checks': list(ck)}

    ck2 = Checks()
    rol = ck2.add('400*7', 're-order level = max usage × max lead time')
    mn = ck2.add('400*7-300*6', 'minimum level = ROL − normal usage × normal lead time')
    mx = ck2.add('400*7+3000-200*5', 'maximum level = ROL + ROQ − min usage × min lead time')
    av1 = ck2.add('(400*7-300*6+400*7+3000-200*5)/2', 'average level = (min + max) ÷ 2')
    av2 = ck2.add('400*7-300*6+3000/2', 'average level = min + ½ ROQ')
    dl = ck2.add('300*2', 'danger level = normal usage × emergency lead time')
    i2 = {'id': 'i2', 'title': 'Setting the stock levels', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'For a raw material: usage — normal 300 units a week, minimum 200, maximum 400; lead time — 5 to 7 weeks, normally 6; re-order quantity 3,000 units; emergency purchases take 2 weeks. Compute the re-order level, minimum level, maximum level, average stock level (both ways) and danger level.',
          'solution': [table(['Level', 'Formula', 'Units'], [
              ['Re-order level', 'Maximum usage × maximum lead time = 400 × 7', inr(rol)],
              ['Minimum level', 'ROL − (normal usage × normal lead time) = 2,800 − 300 × 6', inr(mn)],
              ['Maximum level', 'ROL + ROQ − (minimum usage × minimum lead time) = 2,800 + 3,000 − 200 × 5', inr(mx)],
              ['Average level (i)', '(Minimum + Maximum) ÷ 2', inr(av1)],
              ['Average level (ii)', 'Minimum + ½ ROQ', inr(av2)],
              ['Danger level', 'Normal usage × emergency lead time = 300 × 2', inr(dl)],
          ], title='Stock levels'), note('Both formulas for average stock are accepted; state which one you use.')],
          'checks': list(ck2)}

    ck3 = Checks()
    f_i1 = ck3.add('600*40+100*45', 'FIFO: issue of 700 units'); f_i2 = ck3.add('300*45+300*50', 'FIFO: issue of 600 units'); f_cl = ck3.add('200*50', 'FIFO: closing stock')
    w_r1 = ck3.add('(600*40+400*45)/1000', 'weighted average rate after first purchase')
    w_i1 = ck3.add('700*(600*40+400*45)/1000', 'weighted average: issue of 700')
    w_r2 = ck3.add('(300*(600*40+400*45)/1000+500*50)/800', 'weighted average rate after second purchase')
    w_i2 = ck3.add('600*(300*(600*40+400*45)/1000+500*50)/800', 'weighted average: issue of 600')
    w_cl = ck3.add('200*(300*(600*40+400*45)/1000+500*50)/800', 'weighted average: closing stock')
    tot = ck3.add('600*40+400*45+500*50', 'total cost of stock available')
    i3 = {'id': 'i3', 'title': 'FIFO versus weighted average', 'difficulty': 'moderate', 'minutes': 12,
          'q': 'Stores ledger of material M for a month: 1st opening 600 units @ ₹40; 4th received 400 units @ ₹45; 9th issued 700 units; 16th received 500 units @ ₹50; 25th issued 600 units. Price the issues and value the closing stock under (a) FIFO and (b) weighted average (perpetual).',
          'solution': [table(['Date', 'FIFO — issue value ₹', 'Weighted average — issue value ₹'], [
              ['9th — 700 units', f'{inr(f_i1)} (600 @ 40 + 100 @ 45)', f'{inr(w_i1)} (700 @ {inr(w_r1)})'],
              ['25th — 600 units', f'{inr(f_i2)} (300 @ 45 + 300 @ 50)', f'{inr(w_i2)} (600 @ {inr(w_r2)})'],
              ['Closing 200 units', f'{inr(f_cl)} (200 @ 50)', f'{inr(w_cl)} (200 @ {inr(w_r2)})'],
          ], title='Issue pricing'),
              wn('Proof', f'Both methods account for the total cost of {R(tot)}: FIFO {inr(f_i1)} + {inr(f_i2)} + {inr(f_cl)}; weighted average {inr(w_i1)} + {inr(w_i2)} + {inr(w_cl)}.'),
              note('In rising prices FIFO charges older, cheaper costs to production and leaves closing stock at recent prices; weighted average smooths the effect.')],
          'checks': list(ck3)}

    levels = table(['Level', 'Formula'], [
        ['Re-order level (ROL)', 'Maximum consumption × maximum lead time  (or Minimum level + average consumption × average lead time)'],
        ['Minimum level', 'ROL − (average consumption × average lead time)'],
        ['Maximum level', 'ROL + ROQ − (minimum consumption × minimum lead time)'],
        ['Average level', '(Minimum + Maximum) ÷ 2   or   Minimum + ½ ROQ'],
        ['Danger level', 'Average consumption × lead time for emergency purchases'],
    ], title='Stock level formulas')
    pricing = table(['Group', 'Methods'], [
        ['Cost price methods', 'Specific price; First-in First-out (FIFO); Last-in First-out (LIFO); base stock'],
        ['Average price methods', 'Simple average; weighted average; periodic simple / periodic weighted average; moving average'],
        ['Market price methods', 'Replacement price; realisable price'],
        ['Notional price methods', 'Standard price; inflated price'],
    ], title='Methods of pricing issues')
    losses = table(['Form', 'Normal', 'Abnormal'], [
        ['Waste (lost or discarded, may have no value)', 'Absorbed by good units', 'Transferred to Costing P&L A/c'],
        ['Scrap (discarded residue, small value)', 'Cost borne by good units; realisable value credited to the job/process', 'Scrap A/c charged at full cost, job/process credited; profit or loss on sale to Costing P&L'],
        ['Spoilage (damaged beyond economical rectification)', 'Charged to the production order or to production overhead; realisation credited', 'Charged to Costing P&L A/c'],
        ['Defectives (can be reworked)', 'Rework cost charged to the order or to production overhead / department', 'Rework cost charged to Costing P&L A/c'],
        ['Obsolescence', '—', 'Loss on obsolete stock charged to Costing P&L A/c'],
    ], title='Treatment of material losses')

    concepts = [
        C('c1', T1, [
            'Material is usually the largest element of cost, so it needs systematic control — getting the right quality, in the right quantity, at the right time, from the right source, at the right price, and keeping it safe until used.',
            'Objectives of material control: uninterrupted supply for production; minimum investment in stock (neither excess nor shortage); purchase at the best terms; protection against theft, wastage and deterioration; and reliable records for costing and accounts.',
            'Requirements: coordination between purchase, stores, production and accounts; a clear purchase procedure; standard forms for ordering, receipt and issue; budgets for materials; classification and coding of materials; stock levels and periodic physical checks; and a system of internal audit and reports.',
            'Elements: a purchasing function, a stores function, inventory control (levels, EOQ, ABC) and material accounting (pricing of issues, records, reconciliation).'],
          'Material control is like running a kitchen pantry: buy what the menu needs, store it well, take out only what is requisitioned, and know exactly what is left.',
          'A CA in a factory reviews whether stock levels and purchase approvals actually match the documented policy — gaps here are a common audit finding.'),
        C('c2', T2, [
            'Bill of Materials (BOM): a list of all materials, parts and quantities needed for a job or product — prepared by the production or engineering department; it serves as the basis for requisitions and cost estimates.',
            'Material Requisition Note: an authorised request by a production department to stores to issue materials for a job or process.',
            'Purchase Requisition: a request by the storekeeper (or a department) to the purchase department to buy materials — usually when stock reaches the re-order level or for special items.',
            'Steps: inviting quotations or proposals; selecting the supplier (price, quality, delivery, terms, reliability); issuing a purchase order; receiving and inspecting the material and preparing a Goods Received Note (GRN); returning rejected goods with a Material Returned Note (or debit note to the supplier); and checking and passing the supplier\'s bill against the purchase order and GRN before payment.'],
          'The documents form a chain: BOM says what is needed, requisitions ask for it, the purchase order commits to buy it, the GRN proves it arrived, and only then is the bill paid.',
          'Three-way matching (purchase order, GRN and invoice) before payment is a key internal control that auditors test.'),
        C('c3', T3, [
            'Stores may be centralised (one store for the whole factory — better control and lower investment) or decentralised/departmental (closer to users — less handling), or a combination with sub-stores.',
            'Duties of the storekeeper: receive and check materials against orders; store them safely by location; issue only against authorised requisitions; keep bin cards up to date; initiate purchase requisitions at the re-order level; prevent theft, deterioration and obsolescence; and help in physical verification.',
            'Records: the bin card (kept by the storekeeper, quantities only, at the bin) and the stores ledger (kept by the costing department, quantities and values). Comparing the two helps detect errors and discrepancies.'],
          'The bin card is the label on the jar in the pantry; the stores ledger is the household account book that also shows what each jar cost.',
          'Differences between bin card balances, stores ledger and physical counts are investigated and written off only after approval.'),
        C('c4', T4, [
            'Economic Order Quantity (EOQ) is the order size at which the total of ordering cost and carrying cost is the least.',
            'Ordering costs: cost of inviting quotations, preparing purchase orders, the purchase staff, receiving and inspection — they rise with the number of orders. Carrying costs: interest on funds locked up, storage space, insurance, deterioration and obsolescence — they rise with the average stock held.',
            'EOQ = √(2AO ÷ C), where A = annual requirement (units), O = cost of placing one order, C = carrying cost per unit per year. Number of orders = A ÷ EOQ; average stock = EOQ ÷ 2.',
            'Assumptions: ordering cost per order and carrying cost per unit are constant; demand is known and even through the year; the purchase price per unit is constant (no quantity discounts); and material is received immediately on ordering (no lead time). When a bulk discount is offered, compare total cost (purchase cost + ordering + carrying) at EOQ and at the discount quantity.'],
          'EOQ is the sweet spot between going to the market every day (high ordering cost) and filling the whole house with groceries (high carrying cost).',
          'Procurement teams use EOQ as a starting point and then adjust for supplier minimum lots, price breaks and lead-time risk.'),
        C('c5', T5, [
            'Stock levels tell the storekeeper when to order and how much to hold.',
            'Re-order level: the stock at which a fresh order is placed so that, during the lead time, even maximum usage over the maximum lead time can be met. Re-order quantity is how much is ordered — usually the EOQ.',
            'Minimum level: the stock below which stock should not normally fall — a buffer. Maximum level: the ceiling above which stock should not rise, to avoid locking funds. Average stock: the stock normally held. Danger level: the level at which normal issues stop and only essential issues are made, while emergency purchases are arranged.',
            'Lead time (re-order period) is the time between placing an order and receiving the material.'],
          'The levels are markings on a water tank: refill at the red line (re-order), never let it drop below the bottom mark (minimum), never overflow (maximum), and switch to emergency rationing at the danger mark.',
          'ERP systems trigger purchase requisitions automatically when stock hits the re-order level.',
          blocks=[levels]),
        C('c6', T6, [
            'ABC analysis (selective control by value): A items — few items with large value (closely controlled, ordered frequently in small lots, strict levels); B items — moderate; C items — many items of small value (simple control, bulk orders). Advantages: continuity of production, less investment, saving of management time, systematic working and economy in storage.',
            'FSN analysis classifies by movement — fast moving, slow moving, non-moving — to locate fast items near issue points and to detect slow and non-moving items for disposal. Non-moving stock often arises from design changes, wrong buying or poor communication of production plans.',
            'VED analysis classifies spare parts by criticality — vital (stock-out stops production), essential, desirable. HML classifies by the unit price of an item — high, medium, low cost — unlike ABC, which uses annual consumption value.',
            'Just-in-Time (JIT): aims at near-zero inventory — buy and produce only when there is demand ("demand pull" or "pull through"). It needs reliable suppliers, short lead times and high quality; it cuts carrying costs and waste but raises stock-out risk.'],
          'ABC is like a bank locker policy: diamonds (A) under tight watch, silverware (B) checked sometimes, and kitchen utensils (C) simply kept on the shelf.',
          'Auto-component makers supplying car plants on JIT schedules deliver several times a day to the assembly line.'),
        C('c7', T7, [
            'Input-output ratio compares the quantity of material used with the standard for the output achieved — a higher than standard usage signals wastage or pilferage.',
            'Inventory turnover ratio = cost of materials consumed ÷ average stock (average of opening and closing). Days of stock holding = 365 ÷ turnover ratio. A high ratio shows fast-moving stock; a low ratio shows over-investment or slow-moving items.',
            'Physical verification: periodic (all items counted at the year-end — may disrupt work) or continuous stock-taking (a few items counted every day by a team independent of stores, so every item is checked several times a year). Continuous stock-taking detects discrepancies early, has a deterrent effect on stores staff and avoids year-end disruption.',
            'Discrepancies may be normal (evaporation, breaking bulk) or abnormal (theft, carelessness). Their causes are investigated and the loss treated accordingly.'],
          'Turnover ratio is the pantry\'s pulse — a quick pulse means fresh stock; a slow pulse means things are going stale on the shelf.',
          'Auditors use stock-days to spot obsolete inventory that may need write-down.'),
        C('c8', T8, [
            'Issues are priced by one of several methods (table). The choice affects product cost and closing stock.',
            'FIFO: issues at the price of the earliest lot in stock; closing stock reflects recent prices. In rising prices, production is charged with lower (older) costs — profit is higher.',
            'LIFO: issues at the price of the latest lot; product cost reflects current prices but closing stock is at old prices. (LIFO is not allowed for financial statements under AS 2, but it is studied as a costing method.)',
            'Simple average: average of the prices (not quantities) of lots in stock — ignores quantities. Weighted average: total cost of stock ÷ total units in stock, recalculated after every receipt — smooths price changes.',
            'Market-price methods use replacement or realisable price; notional methods use a standard price (useful for control) or an inflated price that covers normal losses in storage.'],
          'FIFO is a supermarket shelf where the oldest milk is sold first; LIFO is a pile of plates where the top (newest) plate is used first.',
          'Most Indian manufacturers use weighted average or FIFO because AS 2 allows only these cost formulas (apart from specific identification).',
          blocks=[pricing]),
        C('c9', T9, [
            'Returns to the vendor are credited at the price at which the material was received. Returns to stores from production are valued at the price at which they were issued (or as the method requires), and the job is credited.',
            'Shortages found on physical verification are priced at the current issue price under the method in use; normal shortages are absorbed as overhead, abnormal ones go to Costing P&L.',
            'Losses take five forms — waste, scrap, spoilage, defectives and obsolescence — each with a normal and an abnormal treatment (table). The principle: normal losses are part of the cost of good output; abnormal losses are kept out of product cost.',
            'Consumption of materials is identified through requisitions and returns, monitored against standards (input-output) and recorded in financial accounts on the same basis (issue price method) so that cost and financial books reconcile.'],
          'A bakery\'s crumbs (waste) are part of the cost of bread; a tray of cakes dropped on the floor (abnormal) is a one-off loss, not a reason to raise the price of every cake.',
          'Cost auditors examine whether abnormal losses have been kept out of the cost of production reported in cost records.',
          blocks=[losses]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Finding obsolete stock before the audit', 'role': 'Internal auditor at an engineering company',
         'situation': 'Inventory has grown 40% while sales grew 10%.',
         'steps': ['Run an FSN report: items with no issues in 12 months are non-moving.', 'Compute stock-days by item group and compare with norms.', 'Discuss non-moving items with production — design changes often make parts redundant.', 'Recommend disposal or write-down and tighten maximum levels for slow movers.'],
         'takeaway': 'Inventory ratios and FSN analysis turn a vague "too much stock" into an action list.'},
        {'id': 'j2', 'title': 'Should we take the bulk discount?', 'role': 'Purchase analyst',
         'situation': 'A supplier offers a 2% discount for orders of at least 4,000 units against an EOQ of 1,200.',
         'steps': ['Compute total annual cost at EOQ: purchase cost + ordering + carrying.', 'Compute total annual cost at 4,000 units with the discounted price (carrying cost recalculated at the lower price).', 'Choose the lower total; consider storage space and obsolescence risk.'],
         'takeaway': 'EOQ ignores discounts — compare total costs whenever a price break is offered.'},
    ]

    ck4 = Checks()
    itr = ck4.add('1440000/((160000+200000)/2)', 'inventory turnover ratio')
    days = ck4.add('round(365/(1440000/((160000+200000)/2)),1)', 'days of stock')
    mcqs = [
        Q('m1', 'The document prepared by the storekeeper asking the purchase department to buy material is:', ['Purchase requisition', 'Material requisition note', 'Purchase order', 'Goods received note'], 0,
          'A purchase requisition is the storekeeper\'s (or a department\'s) request to the purchase department to procure materials, usually when stock reaches the re-order level. A material requisition note is a request from production to stores for issue, which is the classic trap. The purchase order goes to the supplier and the GRN records receipt. In practice: ERP systems generate purchase requisitions automatically at re-order points.', 'c2', T2),
        Q('m2', 'A list of all materials and quantities needed for a job is called:', ['Bill of materials', 'Bin card', 'Stores ledger', 'Material returned note'], 0,
          'The bill of materials lists the materials and quantities required for a job or product; it is prepared by the production or engineering department and is the basis for requisitions and estimates. A bin card records quantities in stores, and the stores ledger records quantities and values in the costing department. In practice: BOMs feed material requirement planning in ERP.', 'c2', T2),
        Q('m3', 'The bin card is maintained by the:', ['Storekeeper, showing quantities only', 'Costing department, showing quantities and values', 'Purchase department', 'Accounts payable team'], 0,
          'Bin cards are kept by the storekeeper at the bin and record quantities received, issued and balance. The stores ledger, kept in the costing department, records both quantities and values — the usual trap. In practice: comparing bin cards with the stores ledger helps detect posting errors and pilferage.', 'c3', T3),
        Q('m4', 'Annual demand 12,000 units, cost per order ₹600, carrying cost ₹10 per unit per year. The EOQ is:', ['1,200 units', '1,440 units', '600 units', '2,400 units'], 0,
          'EOQ = √(2 × 12,000 × 600 ÷ 10) = √14,40,000 = 1,200 units. ₹14,40,000 is the figure under the root, and 600 units is half the EOQ (the average stock). In practice: at 1,200 units the company places 10 orders a year and ordering cost equals carrying cost at ₹6,000 each.', 'c4', T4, check='(2*12000*600/10)**0.5'),
        Q('m5', 'At the economic order quantity:', ['Total ordering cost equals total carrying cost', 'Ordering cost is zero', 'Carrying cost is maximum', 'Purchase price is minimum'], 0,
          'In the basic EOQ model the total of ordering and carrying costs is lowest where the two are equal. Ordering cost is never zero while orders are placed, and the purchase price is assumed constant, so EOQ does not minimise price. In practice: if annual ordering cost is far above carrying cost, the company is ordering too often.', 'c4', T4),
        Q('m6', 'Which is NOT an assumption of the basic EOQ model?', ['Quantity discounts are available on large orders', 'Demand is known and even', 'Ordering and carrying costs per unit are constant', 'Lead time is nil — orders are received immediately'], 0,
          'The basic model assumes constant price (no quantity discounts), known and uniform demand, constant ordering cost per order and carrying cost per unit, and immediate receipt. When discounts exist the model must be supplemented by a total-cost comparison. In practice: price breaks are common, so buyers always run that comparison.', 'c4', T4, 'moderate'),
        Q('m7', 'Maximum usage 400 units/week, maximum lead time 7 weeks. The re-order level is:', ['2,800 units', '2,100 units', '1,800 units', '4,800 units'], 0,
          'Re-order level = maximum consumption × maximum lead time = 400 × 7 = 2,800 units, so that even the worst-case usage during the longest lead time is covered. 1,800 units is normal usage × normal lead time (300 × 6), used for the minimum level. In practice: the ROL is the trigger for the purchase requisition.', 'c5', T5, check='400*7'),
        Q('m8', 'Minimum stock level is computed as:', ['Re-order level − (average consumption × average lead time)', 'Re-order level + re-order quantity − (minimum consumption × minimum lead time)', 'Maximum consumption × maximum lead time', '(Maximum + minimum) ÷ 2'], 0,
          'Minimum level = ROL − (average consumption × average lead time). The second option is the maximum level, the third is the re-order level and the fourth is one way of computing the average level. In practice: falling below the minimum level is an early warning that a delivery is late.', 'c5', T5),
        Q('m9', 'The level at which normal issues are stopped and only essential issues are made is the:', ['Danger level', 'Minimum level', 'Re-order level', 'Average level'], 0,
          'At the danger level normal issues are stopped, only essential needs are met and emergency purchases are made; it equals average consumption × the lead time for emergency purchases. Usually it lies below the minimum level. The trap is the minimum level, which is a buffer, not a trigger to stop issues. In practice: danger-level breaches are escalated to senior management.', 'c5', T5),
        Q('m10', 'Under ABC analysis, "A" items are:', ['Few in number but high in consumption value', 'Many in number and low in value', 'Items that are vital for production', 'Items that have not moved for a year'], 0,
          'ABC uses annual consumption value: A items are a small number of items accounting for most of the value and are controlled most closely. Vital items belong to VED analysis and non-moving items to FSN analysis, both common traps. In practice: A items get strict stock levels and frequent small orders.', 'c6', T6),
        Q('m11', 'Classifying spare parts as vital, essential and desirable is:', ['VED analysis', 'FSN analysis', 'HML analysis', 'ABC analysis'], 0,
          'VED classifies items by criticality — whether their absence would stop production (vital). FSN is by movement, HML by unit price and ABC by annual consumption value. In practice: hospitals and power plants use VED to ensure critical spares are never out of stock.', 'c6', T6),
        Q('m12', 'Just-in-Time inventory management is also called:', ['Demand-pull system', 'Push system', 'Two-bin system', 'Periodic review system'], 0,
          'JIT produces and buys only when there is demand — production is "pulled" by customer orders, hence demand pull or pull through. A push system produces to forecast and holds stock. The two-bin system is a simple re-ordering method. In practice: JIT needs reliable suppliers and short lead times.', 'c6', T6),
        Q('m13', 'Materials consumed ₹14,40,000; opening stock ₹1,60,000; closing stock ₹2,00,000. Inventory turnover ratio is:', ['8 times', '7.2 times', '9 times', '4 times'], 0,
          'Average stock = (1,60,000 + 2,00,000) ÷ 2 = ₹1,80,000; turnover = 14,40,000 ÷ 1,80,000 = 8 times, i.e. about 45.6 days of stock. 7.2 uses closing stock alone and 9 uses opening stock alone. In practice: falling turnover year on year flags slow-moving or excess stock.', 'c7', T7, check='1440000/((160000+200000)/2)'),
        Q('m14', 'A key advantage of continuous stock-taking is that it:', ['Detects discrepancies early without stopping work', 'Is done only once a year', 'Needs no independent staff', 'Removes the need for bin cards'], 0,
          'Under continuous stock-taking a few items are checked every day by a team independent of stores, so each item is checked several times a year, discrepancies surface quickly and work is not disrupted. Periodic verification is the once-a-year count — the trap. In practice: continuous counting also has a deterrent effect on stores staff.', 'c7', T7),
        Q('m15', 'In a period of rising prices, the method that charges production with the OLDEST (lowest) prices is:', ['FIFO', 'LIFO', 'Replacement price', 'Weighted average'], 0,
          'FIFO issues from the earliest lots, so in rising prices production is charged at older, lower prices and closing stock is valued near current prices. LIFO does the opposite and replacement price uses the current market price. In practice: FIFO therefore shows higher profit and higher closing stock when prices rise.', 'c8', T8),
        Q('m16', 'Stock: 300 units costing ₹12,600 in total; 500 units received at ₹50. The weighted average rate is:', ['₹47', '₹46', '₹48.50', '₹50'], 0,
          'Weighted average = total cost ÷ total units = (12,600 + 25,000) ÷ 800 = 37,600 ÷ 800 = ₹47. ₹46 is the simple average of ₹42 and ₹50, which ignores quantities — the classic trap. In practice: weighted average is recomputed after every receipt in a perpetual system.', 'c8', T8, 'moderate', check='(12600+500*50)/800'),
        Q('m17', 'Which method prices issues at a predetermined rate useful for control?', ['Standard price method', 'Specific price method', 'FIFO', 'Realisable price method'], 0,
          'The standard price method uses a predetermined price, so differences between actual and standard prices show up as variances for control. Specific price and FIFO are cost-price methods; realisable price is a market-price method. In practice: standard costing systems issue materials at standard and analyse price variances separately.', 'c8', T8),
        Q('m18', 'The cost of normal spoilage is:', ['Charged to the production order or production overhead', 'Charged to Costing Profit and Loss Account', 'Ignored', 'Charged to selling overhead'], 0,
          'Normal spoilage is inherent in operations, so it is part of the cost of production — charged to the specific order or spread through production overhead, with any realisation credited. Abnormal spoilage goes to Costing P&L, the main trap. In practice: setting a normal spoilage percentage in the cost sheet keeps product costs realistic.', 'c9', T9),
        Q('m19', 'Scrap arising normally in a process is treated by:', ['Crediting its realisable value to the job or process concerned', 'Charging it to Costing Profit and Loss', 'Adding its value to the cost of production', 'Ignoring it in all cases'], 0,
          'Normal scrap is borne by the good units, and its realisable value is credited to the job or process, reducing the cost. Charging Costing P&L is for abnormal scrap. In practice: metal turnings sold to dealers reduce the cost of the machining process.', 'c9', T9),
    ]

    ckq = Checks()
    qe = ckq.add('(2*9000*500/25)**0.5', 'q2 EOQ (C = 25% of ₹100)')
    qoc = ckq.add('9000/((2*9000*500/25)**0.5)*500', 'q2 ordering cost at EOQ'); qcc = ckq.add('((2*9000*500/25)**0.5)/2*25', 'q2 carrying cost at EOQ')
    qt1 = ckq.add('9000*100+9000/((2*9000*500/25)**0.5)*500+((2*9000*500/25)**0.5)/2*25', 'q2 total cost at EOQ')
    qt2 = ckq.add('9000*98+9000/3000*500+3000/2*98*0.25', 'q2 total cost at 3,000 units with 2% discount')
    questions = [
        W('q1', 5, 'Explain the following stock levels and how each is computed: re-order level, minimum level, maximum level and danger level.',
          [ul(['Re-order level: the stock at which a fresh order is placed so that usage during the lead time can be met. ROL = maximum consumption × maximum lead time (or minimum level + average consumption × average lead time).',
               'Minimum level: the stock below which stock should not normally fall. Minimum level = ROL − (average consumption × average lead time).',
               'Maximum level: the stock above which stock should not rise, to avoid excess investment. Maximum level = ROL + ROQ − (minimum consumption × minimum lead time).',
               'Danger level: the level at which normal issues are stopped and only essential issues are made, with emergency purchases. Danger level = average consumption × lead time for emergency purchases.'])],
          [S('s1', 'Re-order level meaning and formula', 1.5, 'concept', 're order level|reorder level|re-order level|rol', 'maximum consumption|maximum usage|max', 'lead time|re order period|reorder period'),
           S('s2', 'Minimum level', 1, 'concept', 'minimum level|minimum stock', 'average consumption|average usage|normal', 'lead time'),
           S('s3', 'Maximum level', 1.5, 'concept', 'maximum level|maximum stock', 'roq|re order quantity|reorder quantity|re-order quantity', 'minimum consumption|minimum usage'),
           S('s4', 'Danger level', 1, 'concept', 'danger', 'emergency')],
          ['Formulas without meaning lose half the marks.'], ['Using average consumption in the re-order level formula.', 'Forgetting the ROQ in the maximum level.'],
          ['Write each level as: meaning, then formula.']),
        W('q2', 6, 'Annual requirement of a part is 9,000 units at ₹100 each. Ordering cost is ₹500 per order and carrying cost is 25% per annum of the unit price. (a) Compute the EOQ and the total annual cost (purchase + ordering + carrying). (b) The supplier offers a 2% discount on orders of 3,000 units. Should it be accepted?',
          [wn('(a) EOQ', f'C = 25% × ₹100 = ₹25. EOQ = √(2 × 9,000 × 500 ÷ 25) = {inr(qe)} units. Ordering cost = {R(qoc)}; carrying cost = {R(qcc)}; purchase cost ₹9,00,000. Total = {R(qt1)}.'),
           wn('(b) Order of 3,000 units', f'Price ₹98; ordering cost = 3 orders × ₹500 = ₹1,500; carrying cost = 1,500 × ₹98 × 25% = ₹36,750; purchase cost ₹8,82,000. Total = {R(qt2)}.'),
           p(f'Decision: total cost at the discount quantity ({R(qt2)}) is lower than at EOQ ({R(qt1)}), so the discount offer should be accepted (subject to storage space and obsolescence risk).')],
          [S('s1', 'EOQ 600 units', 1.5, 'computation', nums=[qe]), S('s2', 'Total cost at EOQ ₹9,15,000', 1.5, 'computation', nums=[qt1]),
           S('s3', 'Total cost at 3,000 units ₹9,20,250', 2, 'computation', nums=[qt2]),
           S('s4', 'Decision on the offer', 1, 'conclusion', 'reject|not accept|not be accepted|should not|decline|eoq')],
          ['Many candidates compare only the discount saving with the extra carrying cost and forget the ordering cost saving.'],
          ['Carrying cost at the discount quantity should use the discounted price.'], ['Lay out both totals side by side before deciding.'],
          difficulty='moderate', checks=list(ckq)),
        W('q3', 5, 'Explain the treatment of normal and abnormal waste, scrap, spoilage and defectives in cost accounts.',
          [losses],
          [S('s1', 'Waste — normal absorbed, abnormal to Costing P&L', 1, 'concept', 'waste', 'absorb|good units|good production', 'costing profit|costing p&l|costing pl', n=2),
           S('s2', 'Scrap — realisable value credited; abnormal via scrap account', 1.5, 'concept', 'scrap', 'credit|realis'),
           S('s3', 'Spoilage — normal to order/overhead, abnormal to Costing P&L', 1.5, 'concept', 'spoil', 'overhead|production order', 'costing profit|costing p&l|costing pl', n=2),
           S('s4', 'Defectives — rework cost treatment', 1, 'concept', 'defective', 'rework|rectif')],
          ['A four-row table with normal/abnormal columns is ideal.'], ['Charging normal losses to Costing P&L.'], ['Use one row per form of loss.'], pad='table'),
    ]
    # q2 decision: correct the model conclusion to the computed result
    if qt2 > qt1:
        questions[1]['model'][2] = p(f'Decision: total cost at 3,000 units ({R(qt2)}) is higher than at EOQ ({R(qt1)}) by {R(qt2 - qt1)}, so the discount offer should not be accepted; continue ordering the EOQ of {inr(qe)} units.')

    viva = [
        V('v1', 'What is EOQ and how is it calculated?',
          'EOQ is the order size at which the total of ordering cost and carrying cost is minimum. It equals the square root of two times annual requirement times cost per order, divided by carrying cost per unit per year.',
          [P('p1', 'Order size where ordering + carrying cost is minimum', 5, 'ordering', 'carrying', 'minimum|lowest|least'), P('p2', 'Square root of 2AO/C', 5, 'square root|root', 'two|2', 'annual', min=2)], 'c4'),
        V('v2', 'Give the formulas for re-order level and maximum stock level.',
          'Re order level equals maximum consumption multiplied by maximum lead time. Maximum level equals re order level plus re order quantity minus minimum consumption multiplied by minimum lead time.',
          [P('p1', 'ROL = max consumption × max lead time', 5, 'maximum consumption|maximum usage', 'maximum lead time|maximum re order period'),
           P('p2', 'Max level = ROL + ROQ − min consumption × min lead time', 5, 're order quantity|reorder quantity|roq', 'minimum consumption|minimum usage', 'minimum lead time', min=2)], 'c5'),
        V('v3', 'Distinguish ABC, VED and FSN analysis.',
          'ABC analysis classifies items by annual consumption value, VED by how critical an item is for production, and FSN by how fast items move, as fast, slow or non moving.',
          [P('p1', 'ABC — consumption value', 4, 'abc', 'value'), P('p2', 'VED — criticality', 3, 'ved|vital', 'critical|essential|vital'), P('p3', 'FSN — movement', 3, 'fsn|fast', 'mov')], 'c6'),
        V('v4', 'Compare FIFO and weighted average pricing in rising prices.',
          'Under FIFO issues are priced at the oldest lower prices, so production cost is lower and closing stock is at recent prices. Weighted average recalculates the rate after every receipt by dividing total cost by total units, so it smooths price changes.',
          [P('p1', 'FIFO uses oldest prices; closing stock at recent prices', 5, 'fifo', 'oldest|earliest|older'), P('p2', 'Weighted average = total cost ÷ total units, smooths', 5, 'weighted', 'total cost|smooth|after every receipt|after each receipt')], 'c8'),
        V('v5', 'How are normal and abnormal losses of material treated?',
          'Normal losses are absorbed by the good units and become part of product cost, with any scrap value credited. Abnormal losses are kept out of product cost and transferred to the costing profit and loss account.',
          [P('p1', 'Normal — absorbed by good units', 5, 'normal', 'good units|absorb|product cost'), P('p2', 'Abnormal — Costing P&L', 5, 'abnormal', 'costing profit|costing p&l')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'Stores review at Nirmal Pumps', 'difficulty': 'moderate',
              'case': 'Nirmal Pumps uses 24,000 castings a year. Each order costs ₹750 to place and carrying cost is ₹20 per casting per year. Weekly usage is 400 normally (300 minimum, 600 maximum); lead time is 3 to 5 weeks (4 normally). During a stock count, 15 castings were found cracked due to a forklift accident.',
              'mcqs': [
                  M('k1a', 'The EOQ is:', ['1,342 castings (approx.)', '1,800 castings', '900 castings', '600 castings'], 0,
                    'EOQ = √(2 × 24,000 × 750 ÷ 20) = √18,00,000 ≈ 1,342 castings. 1,800 confuses the root with the figure inside it divided by 1,000. In practice: buyers would round to a practical lot, such as 1,350 or the supplier\'s pack size.', 'moderate', topic=T4),
                  M('k1b', 'The re-order level is:', ['3,000 castings', '1,600 castings', '2,000 castings', '2,400 castings'], 0,
                    'ROL = maximum usage × maximum lead time = 600 × 5 = 3,000 castings. 1,600 is normal usage × normal lead time, which is used to compute the minimum level (3,000 − 1,600 = 1,400). In practice: setting ROL on normal values risks stock-outs when demand peaks and deliveries are late.', 'moderate', check='600*5', topic=T5),
                  M('k1c', 'The minimum level is:', ['1,400 castings', '1,600 castings', '900 castings', '3,000 castings'], 0,
                    'Minimum level = ROL − (normal usage × normal lead time) = 3,000 − 400 × 4 = 1,400. 1,600 is the normal usage over the normal lead time itself. In practice: stock below 1,400 signals that a delivery is overdue.', 'moderate', check='600*5-400*4', topic=T5),
                  M('k1d', 'The cost of the 15 castings cracked in the forklift accident is:', ['Charged to Costing Profit and Loss as an abnormal loss', 'Absorbed into the cost of good pumps', 'Added to ordering cost', 'Ignored'], 0,
                    'An accident is not inherent in operations, so the loss is abnormal and kept out of product cost — charged to Costing Profit and Loss. Absorbing it into good pumps would overstate their cost. In practice: any insurance claim received is credited against this abnormal loss.', 'core', topic=T9),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch02', 1, 'Material Cost',
                ['Explain the objectives, requirements and elements of material control and the purchase procedure with its documents.',
                 'Compute EOQ and compare total costs when quantity discounts are offered.',
                 'Compute re-order, minimum, maximum, average and danger levels.',
                 'Apply ABC, FSN, VED, HML, JIT, turnover ratios and physical verification for inventory control.',
                 'Price issues under FIFO, LIFO and average methods and treat returns, shortages and normal/abnormal losses.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 60, 'practice': 50}, 'prereq': ['int-p4-ch01-u01'],
                 'exam_tip': 'EOQ with discounts, stock levels and FIFO/weighted-average stores ledgers are near-certain numericals; learn the formulas exactly and show workings.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Material control: right quality, quantity, time, source, price; safe storage; reliable records.', 'Documents: BOM → material requisition → purchase requisition → purchase order → GRN → bill passed.',
                             'EOQ = √(2AO/C); at EOQ ordering cost = carrying cost.', 'ROL = max use × max lead time; Min = ROL − avg use × avg lead time; Max = ROL + ROQ − min use × min lead time; Avg = (Min + Max)/2 or Min + ½ROQ; Danger = avg use × emergency lead time.',
                             'Selective control: ABC (value), FSN (movement), VED (criticality), HML (unit price); JIT = demand pull.', 'ITR = materials consumed ÷ average stock; days = 365 ÷ ITR.',
                             'Pricing: FIFO, LIFO, simple/weighted average, replacement, standard.', 'Normal losses → good units; abnormal → Costing P&L.'],
                 'remember': ['Bin card: storekeeper, quantity. Stores ledger: costing department, quantity and value.', 'Simple average ignores quantities.', 'Continuous stock-taking is done by an independent team.'],
                 'traps': ['EOQ ignores discounts — compare total cost.', 'ROL uses MAXIMUM usage and lead time.', 'Normal scrap value is credited to the job/process, not to Costing P&L.']},
                [('EOQ', '√(2AO ÷ C)'), ('Re-order level', 'Max consumption × max lead time'), ('Minimum level', 'ROL − (avg consumption × avg lead time)'),
                 ('Maximum level', 'ROL + ROQ − (min consumption × min lead time)'), ('Average level', '(Min + Max) ÷ 2 or Min + ½ ROQ'),
                 ('Danger level', 'Avg consumption × emergency lead time'), ('Inventory turnover', 'Materials consumed ÷ average stock')],
                viva, cases,
                topics=['Introduction', 'Material Control', 'Materials Procurement Procedure', 'Material Storage & Records', 'Inventory Control', 'Material Issue Procedure',
                        'Valuation of Material Issues', 'Valuation of Returns & Shortages', 'Treatment of Normal and Abnormal Loss of Materials', 'Consumption of Materials'])
