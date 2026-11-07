"""CA Foundation · Paper 1 Accounting · Chapter 4 Inventories (single unit).
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *

UID = 'fnd-p1-ch04-u01'


def P(pid, pt, w, *kw, min=None):
    d = {'id': pid, 'pt': pt, 'w': w, 'kw': list(kw)}
    if min is not None: d['min'] = min
    return d


def V(vid, q, model, points, concept=None):
    d = {'id': vid, 'q': q, 'model': model, 'points': points}
    if concept: d['concept'] = concept
    return d


def M(mid, q, options, answer, explain, concept=None, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'difficulty': difficulty}
    if concept: d['concept'] = concept
    if check: d['check'] = check
    return d


def money(x):
    """2 decimals only when needed."""
    x = round(x, 2)
    return inr(int(x)) if x == int(x) else inr(x)


def fifo(events):
    """events: ('r', date, qty, rate) or ('i', date, qty). Returns stores-ledger rows, closing layers, cost of issues."""
    layers, rows, issued = [], [], 0
    for e in events:
        if e[0] == 'r':
            _, d, q, r = e
            layers.append([q, r])
            rows.append([d, str(q), money(r), money(q * r), '', '', '', ' + '.join(f'{a}@{money(b)}' for a, b in layers), money(sum(a * b for a, b in layers))])
        else:
            _, d, q = e
            need, parts, cost = q, [], 0
            while need:
                take = min(need, layers[0][0])
                parts.append(f'{take}@{money(layers[0][1])}'); cost += take * layers[0][1]
                layers[0][0] -= take; need -= take
                if not layers[0][0]: layers.pop(0)
            issued += cost
            rows.append([d, '', '', '', str(q), ' + '.join(parts), money(cost), ' + '.join(f'{a}@{money(b)}' for a, b in layers), money(sum(a * b for a, b in layers))])
    return rows, layers, issued


def wavg(events):
    """Perpetual weighted average: new rate after each receipt (rate kept to 2 decimals, value carried exactly)."""
    qty, val, rows, issued = 0, 0.0, [], 0.0
    for e in events:
        if e[0] == 'r':
            _, d, q, r = e
            qty += q; val += q * r
            rows.append([d, str(q), money(r), money(q * r), '', '', '', str(qty), money(val / qty), money(val)])
        else:
            _, d, q = e
            rate = val / qty
            cost = round(q * rate, 2)
            qty -= q; val = round(val - cost, 2); issued += cost
            rows.append([d, '', '', '', str(q), money(rate), money(cost), str(qty), money(val / qty) if qty else '', money(val)])
    return rows, qty, round(val, 2), round(issued, 2)


FH = ['Date', 'Recd qty', 'Rate (₹)', 'Amount (₹)', 'Issued qty', 'Layers issued', 'Cost of issue (₹)', 'Balance (layers)', 'Balance (₹)']
WH = ['Date', 'Recd qty', 'Rate (₹)', 'Amount (₹)', 'Issued qty', 'Rate (₹)', 'Cost of issue (₹)', 'Balance qty', 'Avg rate (₹)', 'Balance (₹)']


def build():
    # ============ Illustration 1: cost formulas ============
    ev1 = [('r', 'Apr 1 (opening)', 200, 150), ('r', 'Apr 5', 300, 160), ('i', 'Apr 9', 350), ('r', 'Apr 15', 250, 172), ('i', 'Apr 22', 200), ('r', 'Apr 28', 100, 180)]
    c1 = Checks()
    f_rows, f_layers, f_iss = fifo(ev1)
    f_close = c1.add('200*172+100*180', 'FIFO closing inventory: 200 @ 172 + 100 @ 180')
    c1.add('(200*150+150*160)+(150*160+50*172)', 'FIFO cost of issues')
    avail = c1.add('200*150+300*160+250*172+100*180', 'Cost of goods available for sale')
    assert f_close == sum(a * b for a, b in f_layers) and f_iss + f_close == avail
    w_rows, w_q, w_close, w_iss = wavg(ev1)
    c1.add('(30000+48000)/500', 'Average after 5 April')
    c1.add('(150*156+250*172)/400', 'Average after 15 April')
    c1.add('200*166+100*180', 'Weighted average (perpetual) closing value')
    assert w_close == 51200
    p_rate = c1.add('139000/850', 'Periodic weighted average rate')
    p_close = c1.add('round(139000*300/850)', 'Periodic weighted average closing (rounded to rupee)')
    s_rate = c1.add('(150+160+172+180)/4', 'Simple average of the four prices')
    s_close = c1.add('300*165.5', 'Simple average closing')
    l_close = c1.add('200*150+100*160', 'Periodic LIFO closing (for comparison only)')
    compare = table(['Cost formula', 'Closing inventory 300 units (₹)', 'Cost of goods sold (₹)'], [
        ['FIFO (perpetual = periodic)', inr(f_close), inr(avail - f_close)],
        ['Weighted average — perpetual', inr(w_close), inr(avail - w_close)],
        ['Weighted average — periodic', inr(p_close), inr(avail - p_close)],
        ['Simple average', inr(s_close), inr(avail - s_close)],
        ['LIFO — periodic (not permitted, comparison only)', inr(l_close), inr(avail - l_close)],
    ], title='Same goods, different cost formulas (goods available ₹1,39,000)')

    # ============ Illustration 2: cost and lower of cost or NRV ============
    c2 = Checks()
    td = c2.add('40000*5/100', 'Trade discount 5% on 40,000')
    costA = c2.add('40000-2000+3000+500+4000+2500', 'Cost of finished product A')
    nrvB = c2.add('34000-2000-1500', 'NRV of product B')
    tot_cost = c2.add('48000+36000+25000', 'Total cost')
    tot_nrv = c2.add('52000+30500+27800', 'Total NRV')
    item = c2.add('48000+30500+25000', 'Item-by-item lower of cost and NRV')
    costtab = table(['Element', 'Amount (₹)', 'Treatment'], [
        ['Purchase price of 400 units @ ₹100', '40,000', 'Included'],
        ['Less: trade discount 5%', '(2,000)', 'Deducted'],
        ['GST paid ₹6,840 (input credit available)', '—', 'Excluded — recoverable'],
        ['Freight inward', '3,000', 'Included'],
        ['Unloading into factory store', '500', 'Included'],
        ['Direct labour for conversion', '4,000', 'Included'],
        ['Production overheads (normal capacity)', '2,500', 'Included'],
        ['Abnormal spoilage after a power failure ₹1,200', '—', 'Excluded — charged to P&L'],
        ['Rent of finished-goods warehouse ₹900', '—', 'Excluded — routine storage'],
        ['Sales commission ₹1,800', '—', 'Excluded — selling cost'],
        ['Cost of product A', inr(costA), ''],
    ], title='Step 1 — cost of finished product A')
    lcnrv = table(['Product', 'Cost (₹)', 'NRV (₹)', 'Value taken (₹)'], [
        ['A', '48,000', '52,000', '48,000'],
        ['B', '36,000', '30,500', '30,500'],
        ['C', '25,000', '27,800', '25,000'],
        ['Total', inr(tot_cost), inr(tot_nrv), inr(item)],
    ], num=[1, 2, 3], total=True, title='Step 2 — lower of cost and NRV, item by item')

    # ============ Illustration 3: adjusted selling price (retail) method ============
    c3 = Checks()
    cga = c3.add('960000+40000', 'Cost of goods available')
    sva = c3.add('1100000+150000', 'Selling value of goods available')
    gm = c3.add('(1250000-1000000)/1250000*100', 'Gross margin % on selling price')
    cl3 = c3.add('150000*(100-20)/100', 'Closing inventory at cost')
    retail = table(['Particulars', 'Amount (₹)'], [
        ['Sales during the year', '11,00,000'],
        ['Add: closing inventory at selling price', '1,50,000'],
        ['Selling value of goods available', inr(sva)],
        ['Less: cost of goods available (9,60,000 + 40,000)', '(' + inr(cga) + ')'],
        ['Gross margin', '2,50,000'],
        ['Gross margin % = 2,50,000 ÷ 12,50,000', '20%'],
        ['Closing inventory at selling price', '1,50,000'],
        ['Less: gross margin 20%', '(30,000)'],
        ['Closing inventory (cost) under adjusted selling price method', inr(cl3)],
    ], title='Shubh Mart — adjusted selling price method')

    # ============ Illustration 4: count after year-end ============
    c4 = Checks()
    cos4 = c4.add('(90000-4000)*80/100', 'Cost of net sales 1–9 April (25% on cost = 20% on sales)')
    pur4 = c4.add('52000-7000', 'Purchases actually received 1–9 April')
    app4 = c4.add('15000*80/100', 'Goods on approval at cost')
    inv4 = c4.add('426000+68800-45000+12000-20000', 'Inventory on 31 March 2027')
    inv4t = table(['Particulars', 'Amount (₹)'], [
        ['Inventory physically counted on 9 April 2027 (at cost)', '4,26,000'],
        ['Add: cost of goods sold 1–9 April: (90,000 − 4,000) × 100/125', inr(cos4)],
        ['Add: goods sent on approval (not yet approved) at cost: 15,000 × 100/125', inr(app4)],
        ['', inr(426000 + cos4 + app4)],
        ['Less: purchases received 1–9 April (52,000 − 7,000 still in transit)', '(' + inr(pur4) + ')'],
        ['Less: goods held for a principal on consignment', '(20,000)'],
        ['Inventory as on 31 March 2027', inr(inv4)],
    ], title='Gupta Hardware — statement of inventory as on 31 March 2027')

    # ============ Questions ============
    ev_q1 = [('r', 'Jan 1 (opening)', 120, 50), ('r', 'Jan 10', 180, 55), ('i', 'Jan 20', 200), ('r', 'Feb 8', 300, 58), ('i', 'Feb 25', 250), ('i', 'Mar 15', 100)]
    q1c = Checks()
    q1f_rows, q1f_layers, q1f_iss = fifo(ev_q1)
    q1_fifo = q1c.add('50*58', 'FIFO closing: 50 units @ 58')
    q1w_rows, q1w_q, q1w_close, q1w_iss = wavg(ev_q1)
    q1c.add('(6000+9900)/300', 'Average after 10 Jan')
    q1c.add('(100*53+17400)/400', 'Average after 8 Feb')
    q1_wa = q1c.add('50*56.75', 'Weighted average closing: 50 units @ 56.75')
    q1c.add('6000+9900+17400', 'Cost of goods available')
    assert q1f_layers == [[50, 58]] and abs(q1w_close - q1_wa) < 0.01

    q3c = Checks()
    q3_cos = q3c.add('(60000-5000)*75/100', 'Cost of net sales 26–31 March (GP 25% on sales)')
    q3_inv = q3c.add('312000+38000-2000-41250-5000', 'Inventory on 31 March')
    q3t = table(['Particulars', 'Amount (₹)'], [
        ['Inventory counted on 25 March (at cost)', '3,12,000'],
        ['Add: purchases 26–31 March', '38,000'],
        ['Less: purchase returns 26–31 March', '(2,000)'],
        ['Less: cost of net sales 26–31 March: (60,000 − 5,000) × 75%', '(' + inr(q3_cos) + ')'],
        ['Less: write-down of damaged item to NRV (14,000 − 9,000)', '(5,000)'],
        ['Inventory as on 31 March 2027', inr(q3_inv)],
    ], title='Statement of inventory as on 31 March 2027')

    q4c = Checks()
    q4_cost = q4c.add('190000+6000+48000-3000+22000', 'Cost of 1,000 units')
    q4_nrv = q4c.add('1000*(300-20)', 'NRV of 1,000 units')
    q4t = table(['Element', 'Amount (₹)', 'Reason'], [
        ['Materials (net of trade discount)', '1,90,000', 'Cost of purchase'],
        ['GST ₹34,200 — credit available', '—', 'Recoverable, excluded'],
        ['Freight inward', '6,000', 'Brings goods to present location'],
        ['Direct labour ₹48,000 less abnormal idle time ₹3,000', '45,000', 'Abnormal amount excluded'],
        ['Production overheads', '22,000', 'Cost of conversion'],
        ['Finished-goods storage ₹2,500, office administration ₹7,000, sales commission ₹5,000', '—', 'Excluded'],
        ['Cost of 1,000 units', inr(q4_cost), ''],
    ], num=[1], total=True, title='Cost of inventory')

    kc = Checks()
    k_f = kc.add('150*44+50*42', 'FIFO closing')
    k_av = kc.add('(100*40+300*42+150*44)/550', 'Periodic weighted average rate')
    k_cogs = kc.add('(100*40+300*42+150*44)-8700', 'FIFO cost of goods sold')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch04', 'n': 1,
        'title': 'Inventories',
        'outcomes': [
            'Explain what counts as inventory for a trader and a manufacturer, and what does not.',
            'Explain why the inventory figure affects profit, the balance sheet, liquidity ratios and statutory disclosure.',
            'Apply "lower of cost and net realisable value" — working out cost (what to include and exclude) and NRV, item by item.',
            'Distinguish the periodic and perpetual inventory systems.',
            'Value inventory by specific identification, FIFO, simple and weighted average, adjusted selling price and standard cost, and explain why LIFO is not allowed.',
            'Work back or forward from a physical count taken on a date other than the balance sheet date, dealing with goods on approval and goods held on consignment.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 60}, 'prereq': ['fnd-p1-ch02-u01'],
                 'exam_tip': 'Expect a 4–6 mark computation (FIFO / weighted average stores ledger or inventory on the balance sheet date) and short theory on cost vs NRV or periodic vs perpetual. Always state the basis — "lower of cost and NRV".'},
        'concepts': [
            {'id': 'c1', 'title': 'What inventory is',
             'body': ['Inventory means assets that are (a) held for sale in the normal course of business, (b) in the process of being produced for such sale, or (c) materials and supplies to be used up in producing goods or rendering services. Maintenance supplies and consumables are included.',
                      'A trader\'s inventory is mainly goods bought for resale in the same form, plus small supplies such as cartons and wrapping material. A manufacturer holds raw materials, work-in-progress (partly finished goods), finished goods, stores and spares, loose tools and packing material. For a construction business, projects under construction are inventory too.',
                      'Not inventory: machinery spares, servicing equipment and standby equipment that can be used only with a particular item of plant and whose use is irregular — these are treated as fixed assets (property, plant and equipment). Goods held for someone else (for example on consignment) are not your inventory either.'],
             'analogy': 'Think of a bakery: flour in the store (raw material), dough in the oven (WIP), bread on the shelf (finished goods). The oven itself is not inventory — it is a fixed asset.',
             'work': 'In a stock audit, the first question is ownership: are the goods in the godown really the client\'s? Third-party goods are a common source of overstated inventory.'},
            {'id': 'c2', 'title': 'Why the inventory figure matters so much',
             'body': ['Profit: cost of goods sold is worked out as opening inventory plus purchases and direct expenses, minus closing inventory. Closing inventory overstated → profit overstated; closing understated → profit understated. Opening inventory overstated → profit understated; opening understated → profit overstated. The error always flows through cost of goods sold, and this year\'s closing becomes next year\'s opening, so an error reverses next year.',
                      'Financial position and liquidity: inventory is usually the largest current asset. A wrong figure distorts the balance sheet, working capital and the current ratio (current assets ÷ current liabilities) that bankers rely on. Slow-moving or non-moving items are often the hidden cause of weak results.',
                      'Statutory disclosure: Schedule III to the Companies Act, 2013 requires inventories to be shown class-wise (raw materials, work-in-progress, finished goods, stock-in-trade, stores and spares, loose tools), and accounting standards require disclosure of the accounting policy and the cost formula used.'],
             'blocks': [table(['If this is overstated…', 'Profit for the year is…'], [['Closing inventory', 'Overstated'], ['Opening inventory', 'Understated']], note='Understatement has exactly the opposite effects.')],
             'analogy': 'Closing inventory is the bridge between two years — if you shift the bridge, one bank of the river looks bigger and the other smaller.',
             'work': 'Inflating closing stock is one of the oldest ways to dress up profit. That is why auditors attend the physical count and banks insist on monthly stock statements for working-capital loans.'},
            {'id': 'c3', 'title': 'Basis: lower of cost and net realisable value',
             'body': ['Inventories are measured at cost or net realisable value (NRV), whichever is lower. This follows prudence (conservatism): an expected loss is recognised at once, while an expected profit is not recognised until the goods are sold.',
                      'If selling prices have fallen below cost, writing the goods down to NRV books the loss in the year it becomes evident, not in the year of sale.',
                      'The comparison is normally made item by item. Similar or related items that cannot practically be valued separately may be grouped. Comparing total cost with total NRV is not the normal approach, because a gain on one item would hide a loss on another.'],
             'blocks': [lcnrv],
             'analogy': 'A shopkeeper prices yesterday\'s bread at what it will actually fetch today, if that is less than what it cost — but never marks fresh bread up to its selling price before it is sold.',
             'work': 'At year-end, accountants run an "NRV test": compare each item\'s cost with recent or expected selling prices less selling costs, and provide for expired, damaged or obsolete stock.'},
            {'id': 'c4', 'title': 'What goes into cost — and what stays out',
             'body': ['Cost = costs of purchase + costs of conversion + other costs incurred to bring the goods to their present location and condition.',
                      'Costs of purchase: purchase price, import duties and taxes that cannot be recovered later, freight inward, handling and other costs directly linked to acquiring the goods, less trade discounts, rebates and duty drawbacks. GST for which input credit is available is not cost.',
                      'Costs of conversion: direct labour and a systematic share of fixed and variable production overheads. Other costs: for example design cost for a specific customer, or administrative overheads that clearly help bring goods to their present condition. Interest is generally excluded, but may be included where goods need a long time to get ready for sale (wine, rice, timber).',
                      'Excluded: abnormal wastage of material, labour or overheads (normal wastage stays in cost); storage costs, unless storage is a necessary step in production (for example ageing wine); administrative overheads that do not help bring goods to their present location and condition; selling and distribution costs.'],
             'blocks': [costtab],
             'analogy': 'Cost is everything you spent to get the product onto your shelf, ready to sell — not what you spend afterwards to sell it, and not what you lost through an accident.',
             'work': 'Cost-accounting teams prepare "inventory costing sheets" every quarter. Auditors test whether abnormal scrap or idle time has been wrongly loaded into stock values, which would inflate profit.'},
            {'id': 'c5', 'title': 'Net realisable value',
             'body': ['NRV = the selling price you expect to get in the ordinary course of business, minus the further costs needed to complete the goods, minus the costs needed to make the sale.',
                      'Finished and traded goods: expected selling price less selling and distribution expenses. Work-in-progress: expected selling price of the finished product less costs to complete and costs to sell. Raw materials: replacement cost is generally used as the measure. (Under the accounting standard, materials are not written down at all if the finished goods they go into are expected to sell at or above cost — you will study this at the Intermediate level.)',
                      'NRV is assessed afresh at each balance sheet date.'],
             'analogy': 'NRV is the cash the item will actually bring home: price tag minus whatever you still have to spend to finish it and sell it.',
             'work': 'In seasonal businesses (garments, electronics) NRV write-downs at year-end can be large; management estimates are reviewed against post-year-end sales.'},
            {'id': 'c6', 'title': 'Periodic and perpetual inventory systems',
             'body': ['Periodic system: quantities are found by an actual physical count (or weighing/measuring) on the valuation date; cost of goods sold is the balancing figure: opening + purchases − closing. Simple and cheap, used by small businesses. Limitations: counting more than once a year is costly; operations may have to stop during counting; losses from theft, damage or fraud are hidden in cost of goods sold; no continuous control; the books do not tell you what is in stock at any moment.',
                      'Perpetual system: a stores ledger is updated after every receipt and issue, so cost of goods sold is known directly and closing inventory is the balancing figure in the books. It is costlier but gives continuous information and control. Physical checks are still needed to confirm the book balances; any shortage then shows up.',
                      'The two are complementary, not exclusive — most businesses keep perpetual records and verify them by periodic counts.'],
             'blocks': [table(['Basis', 'Periodic', 'Perpetual'], [
                 ['Based on', 'Physical count', 'Book records (stores ledger)'],
                 ['Information', 'Only at the count date', 'Continuous'],
                 ['Balancing figure', 'Cost of goods sold', 'Closing inventory'],
                 ['Loss of goods', 'Hidden in cost of goods sold', 'Revealed on physical check (book balance includes it until then)'],
                 ['Control', 'Not possible', 'Possible'],
                 ['Cost / disruption', 'Cheaper; business may stop for counting', 'Costlier; no stoppage needed'],
             ])],
             'analogy': 'Periodic is checking how much milk is left by opening the fridge on Sunday; perpetual is writing down every glass you pour.',
             'work': 'ERP systems (Tally, SAP) run perpetual inventory. Auditors still perform test counts and investigate book-vs-physical differences.'},
            {'id': 'c7', 'title': 'Cost formulas based on historical cost',
             'body': ['Specific identification: the actual cost of each item is tracked. Used for items that are not ordinarily interchangeable or are made for specific projects — cars by chassis number, jewellery, custom machines.',
                      'FIFO (first in, first out): the earliest goods are assumed to be issued first, so closing inventory consists of the latest purchases. Same answer under periodic and perpetual records.',
                      'LIFO (last in, first out): the latest goods are assumed to be issued first, so closing inventory is valued at the oldest prices. It rarely matches the physical flow, gives different results under periodic and perpetual records, and leaves very old costs in the balance sheet. Accounting standards do not permit LIFO.',
                      'Simple average: the average of the different purchase prices, ignoring quantities — easy, but unrealistic when lot sizes differ. Weighted average: total cost of goods available ÷ total units available. Under periodic records one rate is worked out for the period; under perpetual records a new average is calculated after each receipt and used for the issues that follow. FIFO and weighted average are the formulas generally used in practice.'],
             'blocks': [compare],
             'analogy': 'FIFO is a queue at a ticket counter; LIFO is a stack of plates — you take the top one, the one placed last.',
             'work': 'A change in cost formula changes profit, so it is a change in accounting policy that must be justified and disclosed. Clients choosing between FIFO and weighted average in software need to understand this before the first entry.'},
            {'id': 'c8', 'title': 'Non-historical methods: adjusted selling price and standard cost',
             'body': ['Adjusted selling price (retail) method: used by retailers with many fast-moving items with similar margins, where tracking individual cost is impractical. Closing inventory is counted at selling price and the gross margin percentage is deducted. Margin % = (selling value of goods available − cost of goods available) ÷ selling value of goods available. The percentage should allow for goods marked down below their original price; an average rate per department is common.',
                      'Standard cost method: inventory is valued at a pre-set standard cost per unit, based on experience, where prices change very frequently (for example crude oil). Standards must be reviewed regularly so that they stay close to actual cost.'],
             'blocks': [retail],
             'analogy': 'A supermarket counts tins by their price stickers and then knocks off its usual margin to get back to cost.',
             'work': 'Large retail chains value stock this way at store level; auditors test the margin percentage used and the effect of markdowns and promotions.'},
            {'id': 'c9', 'title': 'Inventory taking and adjusting to the balance sheet date',
             'body': ['Physical counting is ideally done on the last day of the year. Often it is done a few days before or after; the counted figure is then adjusted to the balance sheet date for goods that came in or went out in between.',
                      'Count after the year-end: add back the cost of goods sold in the gap (net of sales returns, converted to cost) and deduct purchases received (and add back purchase returns). Count before the year-end: the reverse — add purchases, deduct purchase returns and the cost of net sales.',
                      'Goods sent on sale-or-return (approval) basis remain the sender\'s inventory, at cost, until the customer approves or the approval period ends — even though they are not in the godown. Goods received on consignment belong to the consignor (principal); the consignee (agent) holds them but must exclude them from its own inventory. Every item is still measured at the lower of cost and NRV.'],
             'blocks': [inv4t],
             'analogy': 'If you count your wallet on Tuesday but need Sunday\'s balance, you add back what you spent since Sunday and remove what you received since Sunday.',
             'work': 'Auditors attending a count carry out "cut-off" tests: the last goods received note and dispatch note before the year-end are matched to the books so that goods in transit are neither counted twice nor missed.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'FIFO, weighted average and simple average on the same data', 'difficulty': 'moderate', 'minutes': 20,
             'q': 'Ananya Lighting deals in LED panels. April 2026: Apr 1 opening 200 units @ ₹150; Apr 5 purchased 300 @ ₹160; Apr 9 issued 350; Apr 15 purchased 250 @ ₹172; Apr 22 issued 200; Apr 28 purchased 100 @ ₹180. Find closing inventory under (a) FIFO, (b) weighted average with perpetual records, (c) weighted average with periodic records, (d) simple average. Show how LIFO would differ.',
             'solution': [table(FH, f_rows, title='(a) Stores ledger — FIFO'),
                          table(WH, w_rows, title='(b) Stores ledger — weighted average (perpetual)'),
                          wn('(c) Periodic weighted average', f'Goods available = 850 units costing {R(avail)}. Rate = 1,39,000 ÷ 850 = ₹{p_rate}. Closing 300 units × ₹{p_rate} ≈ {R(p_close)}.'),
                          wn('(d) Simple average', f'(150 + 160 + 172 + 180) ÷ 4 = ₹{s_rate}; 300 × {s_rate} = {R(s_close)}. Quantities are ignored, which is why this method is rarely acceptable when lot sizes differ.'),
                          compare,
                          note('Prices are rising, so FIFO gives the highest closing inventory (and the highest profit) and LIFO the lowest. LIFO is shown only to understand the effect — it is not permitted.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Working out cost, then applying lower of cost and NRV', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Prakash Chemicals has three finished products at the year-end. For product A (400 units) the records show: purchase of materials 400 units @ ₹100 less 5% trade discount, GST ₹6,840 (input credit available), freight inward ₹3,000, unloading ₹500, direct labour ₹4,000, production overheads ₹2,500, abnormal spoilage after a power failure ₹1,200, finished-goods warehouse rent ₹900 and sales commission ₹1,800. NRV of A is ₹52,000. Product B cost ₹36,000; it is expected to sell for ₹34,000 after further processing of ₹2,000 and selling costs of ₹1,500. Product C cost ₹25,000 and its NRV is ₹27,800. Value the inventory.',
             'solution': [costtab, wn('NRV of B', f'34,000 − 2,000 (to complete) − 1,500 (to sell) = {R(nrvB)}.'), lcnrv,
                          p(f'Inventory is shown at {R(item)}. Comparing totals ({R(tot_cost)} cost vs {R(tot_nrv)} NRV) would wrongly show {R(tot_cost)} — the gain on A and C would hide the loss of ₹5,500 on B.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Adjusted selling price (retail) method', 'difficulty': 'core', 'minutes': 8,
             'q': 'Shubh Mart, a retailer, had no opening inventory. Purchases during the year cost ₹9,60,000 (net of trade discount and recoverable GST) and freight inward was ₹40,000. Sales were ₹11,00,000 and the closing inventory, counted at selling price, was ₹1,50,000. Value the closing inventory under the adjusted selling price method.',
             'solution': [retail],
             'checks': c3},
            {'id': 'i4', 'title': 'Count taken after the year-end', 'difficulty': 'hard', 'minutes': 14,
             'q': 'Gupta Hardware closes its books on 31 March 2027 but counted inventory only on 9 April 2027: ₹4,26,000 at cost. Between 1 and 9 April: sales ₹90,000; sales returns ₹4,000; purchases ₹52,000, of which goods worth ₹7,000 were still in transit on 9 April. On 25 March goods with a selling price of ₹15,000 were sent to a customer on approval; the customer had not yet decided by 9 April. The count includes goods costing ₹20,000 received from a principal on consignment. The firm earns 25% on cost. Find the inventory as on 31 March 2027.',
             'solution': [inv4t, wn('Notes', '25% on cost = 20% on sales, so cost = sales × 100/125. Goods in transit were never counted, so only ₹45,000 of April purchases is deducted. Approval goods were owned on 31 March but not in the godown — add at cost. Consignment goods are in the godown but never owned — deduct.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Attending a year-end stock count', 'role': 'Articled assistant on a statutory audit of a manufacturer',
             'situation': 'The client counts stock on 3 April. While observing, you notice (i) a stack of cartons marked with another company\'s name, (ii) dusty finished goods of a discontinued model, and (iii) a truck being unloaded in the middle of the count.',
             'steps': ['Note the last goods received note and dispatch note numbers before the year-end and before the count (cut-off).',
                       'Ask about the third-party cartons — if held for a principal or on job work, they must be excluded from the client\'s inventory.',
                       'Record the discontinued model separately; later compare its cost with recent selling prices to see whether a write-down to NRV is needed.',
                       'Make sure goods unloaded during the count are either kept aside or counted and the receipt is excluded when rolling the count back to 31 March.',
                       'Perform test counts in both directions — floor to records and records to floor.'],
             'takeaway': 'Existence, ownership, cut-off and valuation — the four questions behind every inventory figure.',
             'think': 'The count on 3 April shows ₹10.4 lakh. Purchases received 1–3 April are ₹0.9 lakh and sales 1–3 April are ₹1.2 lakh at a 20% margin on sales. What is the inventory on 31 March?',
             'answer': '10.4 − 0.9 + (1.2 × 80%) = ₹10.46 lakh.'},
            {'id': 'j2', 'title': 'Setting up inventory valuation for a pharmacy', 'role': 'Accountant helping a client move to accounting software',
             'situation': 'A pharmacy owner wants to "value stock at MRP because that is what is printed on the box". Some medicines expire within three months.',
             'steps': ['Explain that inventory is carried at the lower of cost and NRV — never at selling price (MRP) before sale.',
                       'Set the software to weighted average (or FIFO); batch-wise tracking is useful because expiry follows batches.',
                       'Exclude GST for which input credit is available from cost; include freight inward.',
                       'At each month-end, run an expiry report and write down near-expiry or expired stock to its realisable value (often nil).',
                       'Disclose the cost formula used in the accounts.'],
             'takeaway': 'Valuing stock at selling price books profit before the sale happens — exactly what prudence forbids.'},
        ],
        'mcqs': [
            dict(M('m1', 'Which of the following is NOT inventory?', ['Standby equipment usable only with a particular machine and used irregularly', 'Raw materials in the factory store', 'Work-in-progress', 'Packing material'], 0,
              'Inventory consists of goods held for sale, in production for sale, or materials to be consumed in production. Standby equipment usable only with a particular machine and used irregularly is not consumed in the ordinary way; it meets the definition of property, plant and equipment and is depreciated. The tempting option, packing material, is inventory because it is consumed in getting goods ready for sale. In practice: factories keep machine-specific critical spares in the fixed asset register, not in the stores ledger.', 'c1'), topic='What inventory is'),
            dict(M('m2', 'Inventories are valued at:', ['Lower of cost and net realisable value', 'Cost or market price, whichever is higher', 'Net realisable value always', 'Selling price less trade discount'], 0,
              "AS 2 requires each item of inventory to be carried at its cost or its net realisable value, whichever is smaller. This follows prudence: if goods are expected to sell below cost, the loss is recognised now, but an expected profit is not recognised until the sale. The tempting option, 'cost or market price, whichever is higher', would anticipate unrealised gains. In practice: at every year end, companies compare cost with expected selling price less selling costs, item by item.", 'c3'), topic='Basis: lower of cost and net realisable value'),
            dict(M('m3', 'Which cost is included in the cost of inventory?', ['Freight inward', 'Selling commission', 'Abnormal wastage', 'Rent of the warehouse for finished goods (routine storage)'], 0,
              'Cost of inventory includes purchase price and all costs of bringing the goods to their present location and condition. Freight inward does exactly that, so it is included. Selling commission is a selling cost, abnormal wastage is a loss, and routine storage of finished goods happens after production — all are expensed. The tempting option is warehouse rent, which sounds like a cost of holding goods but is excluded. In practice: landed cost in ERP systems adds freight, duty and handling to the invoice price.', 'c4'), topic='What goes into cost — and what stays out'),
            dict(M('m4', 'Goods bought for ₹50,000 plus GST ₹9,000 (input credit available) and freight inward ₹1,500. Cost of inventory is:', ['₹51,500', '₹60,500', '₹59,000', '₹50,000'], 0,
              'Cost includes the purchase price and freight inward, but excludes taxes that the business can recover. GST of ₹9,000 is available as input tax credit, so it is not a cost. Cost = ₹50,000 + freight ₹1,500 = ₹51,500. The tempting ₹60,500 adds the GST, which will be recovered from the government by set-off. In practice: a GST-registered trader records input tax in the electronic credit ledger, not in the stock value; an unregistered dealer would include it.', 'c4', 'core', '50000+1500'), topic='What goes into cost — and what stays out'),
            dict(M('m5', 'Expected selling price ₹80,000; cost to complete ₹6,000; selling costs ₹4,000. NRV is:', ['₹70,000', '₹76,000', '₹74,000', '₹80,000'], 0,
              'Net realisable value = estimated selling price − estimated cost to complete − estimated costs to sell = ₹80,000 − ₹6,000 − ₹4,000 = ₹70,000. The tempting ₹76,000 deducts only the completion cost and forgets selling costs; the goods must be both finished and sold to realise cash. In practice: manufacturers with slow-moving or damaged stock compute NRV at year end, and auditors test these estimates against post-year-end sale prices.', 'c5', 'core', '80000-6000-4000'), topic='Net realisable value'),
            dict(M('m6', 'Item X: cost ₹20,000, NRV ₹24,000. Item Y: cost ₹15,000, NRV ₹11,000. Inventory value is:', ['₹31,000', '₹35,000', '₹39,000', '₹26,000'], 0,
              "Lower of cost and NRV is applied item by item. Item X: cost ₹20,000 is below NRV ₹24,000, so ₹20,000. Item Y: NRV ₹11,000 is below cost ₹15,000, so ₹11,000. Inventory = ₹31,000. The tempting ₹35,000 compares total cost (₹35,000) with total NRV (₹35,000), which lets X's gain hide Y's loss. In practice: retailers write down specific slow-moving lines rather than comparing totals for the whole store.", 'c3', 'moderate', '20000+11000'), topic='Basis: lower of cost and net realisable value'),
            dict(M('m7', 'Which cost formula is NOT permitted by the accounting standards?', ['LIFO', 'FIFO', 'Weighted average', 'Specific identification'], 0,
              'AS 2 permits FIFO and weighted average for interchangeable items and specific identification for items not ordinarily interchangeable. LIFO is not permitted, because it leaves old, outdated costs in the balance sheet and rarely reflects the actual flow of goods. The tempting option, specific identification, is permitted — but only for unique items. In practice: Indian companies cannot use LIFO in their financial statements, even though it is allowed in some other countries such as the USA.', 'c7'), topic='Cost formulas based on historical cost'),
            dict(M('m8', 'If closing inventory of the current year is overstated, the current year\'s profit is:', ['Overstated', 'Understated', 'Unaffected', 'Overstated only if opening inventory is also overstated'], 0,
              "Cost of goods sold = Opening inventory + Purchases − Closing inventory. If closing inventory is overstated, cost of goods sold is understated and current-year profit is overstated by the same amount. The tempting option, 'understated', reverses the link. Because this year's closing inventory becomes next year's opening inventory, next year's profit will be understated. In practice: overstating inventory is a well-known way of inflating profit, so auditors attend physical stock counts at year end.", 'c2'), topic='Why the inventory figure matters so much'),
            dict(M('m9', 'If opening inventory is understated, profit for the year is:', ['Overstated', 'Understated', 'Unaffected', 'Equal to gross profit'], 0,
              "Cost of goods sold = Opening inventory + Purchases − Closing inventory. If opening inventory is understated, cost of goods sold is understated and profit for the year is overstated. The tempting option, 'understated', applies the closing inventory logic in reverse — opening and closing inventory affect profit in opposite directions. In practice: an error in last year's closing stock automatically affects this year's profit, so auditors check opening balances in the first year of an audit.", 'c2', 'moderate'), topic='Why the inventory figure matters so much'),
            dict(M('m10', 'Under the periodic inventory system, loss of goods by theft is:', ['Hidden in cost of goods sold', 'Shown separately in the stores ledger', 'Included in closing inventory', 'Recorded as a separate asset'], 0,
              "Under the periodic system, closing inventory is found by physical count and cost of goods sold is a balancing figure: opening + purchases − closing. Anything missing, including goods stolen, is therefore treated as sold and hidden in cost of goods sold. The tempting option, 'shown separately in the stores ledger', describes the perpetual system, which keeps running records that reveal shortages. In practice: large retailers use perpetual systems linked to billing software to spot pilferage.", 'c6'), topic='Periodic and perpetual inventory systems'),
            dict(M('m11', 'Opening 100 units @ ₹10; purchased 200 @ ₹13; 180 units sold. Closing inventory under FIFO is:', ['₹1,560', '₹1,200', '₹1,320', '₹1,440'], 0,
              'Under FIFO, the oldest units are issued first. The 180 units sold come from 100 opening units at ₹10 and 80 purchased units at ₹13, leaving 120 units from the purchase at ₹13: closing inventory = 120 × ₹13 = ₹1,560. The tempting ₹1,440 is the weighted average figure (120 × ₹12). In practice: FIFO suits goods with expiry dates, such as medicines and dairy products, where older stock must move first.', 'c7', 'moderate', '120*13'), topic='Cost formulas based on historical cost'),
            dict(M('m12', 'Opening 100 units @ ₹10; purchased 200 @ ₹13; 180 units sold. Closing inventory under periodic weighted average is:', ['₹1,440', '₹1,560', '₹1,380', '₹1,320'], 0,
              'Periodic weighted average cost = total cost of goods available ÷ total units = (100 × ₹10 + 200 × ₹13) ÷ 300 = ₹3,600 ÷ 300 = ₹12. Closing inventory = 120 × ₹12 = ₹1,440. The tempting ₹1,560 values all 120 units at the latest price of ₹13, which is FIFO. A simple average of ₹11.50 would be wrong because the lots are of different sizes. In practice: weighted average is widely used for commodities stored together, such as grain or chemicals.', 'c7', 'moderate', '120*(1000+2600)/300'), topic='Cost formulas based on historical cost'),
            dict(M('m13', 'Sales ₹4,00,000; closing inventory at selling price ₹1,00,000; cost of goods available ₹3,75,000. Closing inventory under the adjusted selling price method:', ['₹75,000', '₹1,00,000', '₹80,000', '₹93,750'], 0,
              "Goods available at selling price = sales ₹4,00,000 + closing inventory at selling price ₹1,00,000 = ₹5,00,000, against cost ₹3,75,000. Gross margin = (5,00,000 − 3,75,000) ÷ 5,00,000 = 25%. Closing inventory at cost = ₹1,00,000 × 75% = ₹75,000. The tempting ₹80,000 assumes a 20% margin. In practice: supermarkets with thousands of fast-moving items use this retail method, because tracking each item's cost is impractical.", 'c8', 'hard', '100000*375000/500000'), topic='Non-historical methods: adjusted selling price and standard cost'),
            dict(M('m14', 'Goods sent on sale-or-return basis and not yet approved at the year-end are:', ['Included in the sender\'s inventory at cost', 'Treated as sales at selling price', 'Included in the customer\'s inventory', 'Ignored by both parties'], 0,
              "Goods sent on sale-or-return basis remain the sender's property until the customer approves them or the return period expires. So, at year end, unapproved goods are included in the sender's inventory at cost (or NRV if lower), and any sale recorded is reversed. The tempting option, treating them as sales at selling price, would recognise revenue before ownership passes. In practice: publishers and FMCG distributors adjust year-end stock for goods lying with dealers on approval.", 'c9'), topic='Inventory taking and adjusting to the balance sheet date'),
            dict(M('m15', 'Specific identification is the appropriate method for:', ['Items not ordinarily interchangeable, such as custom-built machines', 'Large numbers of identical items', 'Retail stores with thousands of items', 'Crude oil with frequently changing prices'], 0,
              'Specific identification assigns actual costs to identified items, so it suits items that are not ordinarily interchangeable, such as custom-built machines or goods made for a specific project. The tempting option, large numbers of identical items, is where specific identification would be impractical and open to manipulation; FIFO or weighted average is used instead. In practice: jewellers selling unique pieces and builders of custom machinery track the actual cost of each item.', 'c7'), topic='Cost formulas based on historical cost'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'The following relate to a spare part at Sanjay Mills for the quarter ended 31 March 2027: Jan 1 opening 120 units @ ₹50; Jan 10 purchased 180 units @ ₹55; Jan 20 issued 200 units; Feb 8 purchased 300 units @ ₹58; Feb 25 issued 250 units; Mar 15 issued 100 units. Prepare the stores ledger and find the value of closing inventory under (a) FIFO and (b) weighted average (perpetual).',
             'model': [table(FH, q1f_rows, title='(a) FIFO'), table(WH, q1w_rows, title='(b) Weighted average (perpetual)'),
                       wn('Answer', f'Closing inventory: FIFO 50 units @ ₹58 = {R(q1_fifo)}; weighted average 50 units @ ₹56.75 = ₹{money(q1_wa)}.')],
             'scheme': [
                 {'id': 's1', 'pt': 'FIFO: issue of 20 Jan split 120 @ 50 + 80 @ 55', 'm': 1, 'skill': 'computation'},
                 {'id': 's2', 'pt': 'FIFO: issues of 25 Feb and 15 Mar priced correctly', 'm': 1, 'skill': 'computation'},
                 {'id': 's3', 'pt': f'FIFO closing {R(q1_fifo)}', 'm': 0.5, 'skill': 'computation'},
                 {'id': 's4', 'pt': 'Weighted average: new rates ₹53 and ₹56.75 after each receipt', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's5', 'pt': 'Weighted average closing ₹2,837.50', 'm': 1, 'skill': 'computation'},
                 {'id': 's6', 'pt': 'Proper stores-ledger columns (receipts, issues, balance)', 'm': 1, 'skill': 'presentation'},
             ],
             'remarks': ['Many candidates worked out a single periodic average for the whole quarter although perpetual records were asked for.', 'Stores ledgers without a running balance column lost presentation marks.'],
             'mistakes': ['Recomputing the weighted average after an issue — the rate changes only after a receipt.', 'Under FIFO, issuing from the latest lot.'],
             'tips': ['Keep three blocks of columns: Receipts | Issues | Balance.', 'Write FIFO balances as layers (e.g. 100 @ 55) so the next issue is easy to price.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between the periodic inventory system and the perpetual inventory system.',
             'model': [table(['Basis', 'Periodic system', 'Perpetual system'], [
                 ['Basis of figures', 'Physical count at the valuation date', 'Continuous book records in a stores ledger'],
                 ['What is the balancing figure', 'Cost of goods sold', 'Closing inventory'],
                 ['Loss of goods', 'Treated as sold — hidden in cost of goods sold', 'Comes to light when the book balance is compared with a physical check'],
                 ['Control and information', 'No continuous information or control', 'Continuous information; control possible'],
                 ['Cost and disruption', 'Simple and cheap; counting may stop operations', 'Costlier; inventory known without stopping work'],
             ])],
             'scheme': [
                 {'id': 's1', 'pt': 'Physical count vs book records', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Balancing figure — COGS vs closing inventory', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': 'Treatment of loss of goods / control', 'm': 1, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Cost and disruption', 'm': 1, 'skill': 'concept'},
             ],
             'remarks': ['Tabular answers with a clear basis scored well; essays mixing both systems in one paragraph did not.'],
             'mistakes': ['Saying the perpetual system needs no physical verification.', 'Reversing the balancing figures.'],
             'tips': ['Four bases are enough for 4 marks; do not write eight.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Mehta Traders closes its accounts on 31 March 2027. Inventory was counted on 25 March 2027 at a cost of ₹3,12,000. From 26 to 31 March: purchases ₹38,000; purchase returns ₹2,000; sales ₹60,000; sales returns ₹5,000. The firm earns a gross profit of 25% on sales. One item in the count, costing ₹14,000, was damaged and can be sold for only ₹9,000 (net). Compute the value of inventory as on 31 March 2027.',
             'model': [q3t, wn('Working', f'Net sales = 60,000 − 5,000 = 55,000; cost = 55,000 × 75% = {R(q3_cos)}. A count before the year-end is rolled forward: add what came in, deduct what went out.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Starts from the count and rolls forward (direction correct)', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Purchases added and purchase returns deducted', 'm': 1, 'skill': 'application'},
                 {'id': 's3', 'pt': f'Cost of net sales {R(q3_cos)} deducted', 'm': 1.5, 'skill': 'computation'},
                 {'id': 's4', 'pt': 'Damaged item written down by ₹5,000', 'm': 1, 'skill': 'application'},
                 {'id': 's5', 'pt': f'Correct inventory {R(q3_inv)}', 'm': 0.5, 'skill': 'computation'},
             ],
             'remarks': ['Candidates often used the "count after year-end" signs mechanically for a count taken before the year-end.', 'Sales were frequently deducted at selling price instead of cost.'],
             'mistakes': ['Deducting sales at ₹60,000 instead of cost of net sales.', 'Ignoring the NRV write-down.', 'Taking 25% on cost instead of on sales.'],
             'tips': ['Write one line per adjustment with the working inside the particulars.']},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Arora Industries produced 1,000 units of a product during the year, all in stock at the year-end. Costs: materials ₹1,90,000 (net of trade discount) plus GST ₹34,200 (input credit available); freight inward ₹6,000; direct labour ₹48,000, of which ₹3,000 was paid for abnormal idle time during a strike; production overheads ₹22,000; storage of finished goods ₹2,500; office administration ₹7,000; sales commission ₹5,000. The product sells at ₹300 per unit with selling costs of ₹20 per unit. At what value should the inventory be shown?',
             'model': [q4t, p(f'NRV = 1,000 × (300 − 20) = {R(q4_nrv)}. Cost {R(q4_cost)} is lower, so inventory is shown at {R(q4_cost)} (₹263 per unit).')],
             'scheme': [
                 {'id': 's1', 'pt': 'GST excluded; freight inward included', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Abnormal idle time excluded from labour', 'm': 1, 'skill': 'application'},
                 {'id': 's3', 'pt': 'Storage, administration and selling costs excluded', 'm': 1, 'skill': 'application'},
                 {'id': 's4', 'pt': 'NRV ₹2,80,000 computed; value = lower = ₹2,63,000', 'm': 1, 'skill': 'computation'},
             ],
             'remarks': ['Most candidates excluded selling costs but many left the strike wages in cost.'],
             'mistakes': ['Adding GST to cost although credit is available.', 'Comparing cost with gross selling price instead of NRV.'],
             'tips': ['Show excluded items in the table with "—" and a reason; examiners give marks for the reasoning.']},
        ],
        'revision': {
            'summary': ['Inventory = held for sale, in production for sale, or materials/supplies to be consumed in production or services.',
                        'Valued at the lower of cost and NRV, normally item by item (prudence).',
                        'Cost = purchase + conversion + other costs to bring goods to present location and condition; exclude abnormal waste, routine storage, unrelated admin, selling and distribution, recoverable taxes.',
                        'NRV = expected selling price − costs to complete − costs to sell.',
                        'Periodic: COGS is the balancing figure. Perpetual: closing inventory is the balancing figure.',
                        'Formulas: specific identification, FIFO, weighted average (allowed); simple average (crude); LIFO (not permitted); adjusted selling price and standard cost (non-historical).'],
            'remember': ['Closing inventory overstated → profit overstated; opening overstated → profit understated.',
                         'Perpetual weighted average: recompute the rate after every receipt, not after issues.',
                         'Count after year-end: + cost of net sales, − purchases received. Count before: the reverse.',
                         'Goods on approval stay with the sender; consignment goods belong to the consignor.'],
            'traps': ["Don't value stock at selling price or MRP.", "Don't add recoverable GST to cost.", "Don't compare total cost with total NRV.", "Don't forget to convert sales to cost (mark-up on cost vs margin on sales)."],
        },
        'quickref': [
            {'k': 'Basis', 'v': 'Lower of cost and NRV, item by item'},
            {'k': 'COGS', 'v': 'Opening inventory + Purchases + Direct expenses − Closing inventory'},
            {'k': 'NRV', 'v': 'Expected selling price − Cost to complete − Cost to sell'},
            {'k': 'Weighted average rate', 'v': 'Cost of goods available ÷ Units available'},
            {'k': 'Retail method margin %', 'v': '(Selling value of goods available − Cost of goods available) ÷ Selling value of goods available'},
            {'k': 'Mark-up ↔ margin', 'v': '25% on cost = 20% on sales; 33⅓% on cost = 25% on sales'},
            {'k': 'Schedule III', 'v': 'Disclose inventories class-wise; disclose cost formula used'},
        ],
        'viva': [
            V('v1', 'What is meant by inventory? Give the types of inventory in a manufacturing concern.',
              'Inventory means assets kept for selling in the normal course of business, assets in the process of production for such sale, and materials or supplies to be consumed in production or in rendering services. A manufacturer holds raw materials, work in progress, finished goods, and stores, spares and loose tools.',
              [P('p1', 'Held for sale in the ordinary course of business', 3, 'held for sale|for sale|for resale|to be sold|meant for sale|sell'),
               P('p2', 'In the process of production for sale', 2, 'process of production|in production|being produced|under production|work in progress|semi finished|partly finished|partially finished', min=1),
               P('p3', 'Materials / supplies to be consumed in production or services', 2, 'consum|used up|use in production|used in production|supplies|material', min=1),
               P('p4', 'Types: raw materials, WIP, finished goods, stores and spares', 3, 'raw material', 'work in progress|wip|work in process|semi finished|partly finished', 'finished good|finished product', min=2)], 'c1'),
            V('v2', 'On what basis are inventories valued, and why?',
              'We take inventories at cost or net realisable value, whichever is lower. This follows the principle of prudence or conservatism: an expected loss is recognised immediately, but an expected profit is not recognised until the goods are sold. The comparison is normally made item by item.',
              [P('p1', 'Lower of cost and net realisable value', 5, 'lower of cost|cost or net realisable value whichever is lower|cost or nrv whichever is lower|whichever is lower|whichever lower|lower of the two|lesser of cost|cost or nrv whichever less|whichever is less', 'net realisable|net realizable|nrv|realisable value|realizable value', min=2),
               P('p2', 'Prudence / conservatism — losses recognised, profits not anticipated', 3, 'prudence|prudent|conservat|loss recognis|loss immediately|not anticipat|not recognise profit|profit not recognis|unrealised profit|unrealized profit|losses recognised|losses are recognised', min=1),
               P('p3', 'Normally item by item', 2, 'item by item|item wise|itemwise|each item|individual item|separately for each', min=1)], 'c3'),
            V('v3', 'Which costs are included in the cost of inventory, and which are excluded?',
              'Cost includes the cost of purchase, such as purchase price, non-recoverable taxes and freight inward, less trade discounts; costs of conversion such as direct labour and production overheads; and other costs to bring the goods to their present location and condition. Excluded are abnormal wastage, storage costs unless needed in production, administrative overheads not related to production, selling and distribution costs, and taxes that are recoverable like GST credit.',
              [P('p1', 'Included: purchase cost (price, non-recoverable taxes, freight inward, less trade discount)', 3, 'purchase|freight inward|carriage inward|freight in', min=1),
               P('p2', 'Included: conversion cost (direct labour, production overheads) and costs to bring to present location and condition', 3, 'conversion|direct labour|direct labor|labour|wages|production overhead|factory overhead|present location|location and condition', min=1),
               P('p3', 'Excluded: abnormal wastage, storage, admin overheads, selling and distribution, recoverable taxes', 4, 'exclud|not include|not part|kept out|leave out|left out|not form part|outside', 'abnormal|selling|distribution|storage|administrat|recoverable|gst credit|input credit', min=2)], 'c4'),
            V('v4', 'What is net realisable value?',
              'Net realisable value is the expected selling price in the normal course of business, less the estimated costs needed to complete the goods and the estimated costs needed to make the sale. For raw materials, replacement cost is generally taken as the measure.',
              [P('p1', 'Estimated selling price', 4, 'selling price|sale price|price it will fetch|price we expect|realis|realiz', min=1),
               P('p2', 'Less costs to complete', 3, 'complet|finish|further process|conversion', min=1),
               P('p3', 'Less costs to sell', 3, 'cost to sell|costs to sell|selling cost|selling expense|cost of selling|make the sale|distribution|cost to make sale|costs necessary to sell|costs to make the sale', min=1)], 'c5'),
            V('v5', 'Explain FIFO and the weighted average method. Why is LIFO not permitted?',
              'Under FIFO the goods received first are issued first, so closing inventory is made up of the latest purchases. Under the weighted average method, the total cost of goods available is divided by the total units available, and under perpetual records a new average is worked out after every receipt. LIFO is not permitted because it rarely matches the actual flow of goods and leaves old outdated costs in the balance sheet.',
              [P('p1', 'FIFO: first received issued first; closing = latest purchases', 3, 'first in first out|first received first issued|earliest issued first|oldest issued first|first come first|old stock issued first|earliest goods issued first|first purchased first sold', 'closing latest|latest purchase|recent purchase|latest price|recent price|closing recent|closing newest|newest|latest lot', min=1),
               P('p2', 'Weighted average: total cost ÷ total units (recomputed after each receipt in perpetual)', 3, 'total cost', 'total unit|total quantit|number of unit|units available|quantity available', min=2),
               P('p3', 'LIFO not permitted — unrealistic flow / outdated costs in balance sheet', 4, 'lifo', 'not permit|not allow|prohibit|not accept|banned|disallow|not used|cannot be used|not be used', 'actual flow|physical flow|outdated|old cost|old price|irrational|unrealistic|does not match|doesn t match|not match|stale', min=3)], 'c7'),
            V('v6', 'Distinguish between the periodic and the perpetual inventory systems.',
              'In the periodic system inventory is found by physical count at the end of the period, and cost of goods sold is the balancing figure, so losses are hidden in cost of goods sold. In the perpetual system a stores ledger records every receipt and issue continuously, cost of goods sold is known directly and closing inventory is the balancing figure, which allows inventory control.',
              [P('p1', 'Periodic: physical count; COGS is the balancing figure', 4, 'periodic physical|periodic count|periodic reli count|periodic reli physical|periodic method count|periodic method physical|periodic system count|periodic system physical|periodic system reli|periodic based physical|periodic based count|periodic inventory physical|periodic inventory count|periodic stock count|periodic stock physical', 'cost of goods sold balanc|cogs balanc|cost of goods sold residual|cost of goods sold as balanc|cogs residual|balancing figure is cost of goods sold|cost of goods sold is the balancing|cost of goods sold is balancing|cost of sales balanc'),
               P('p2', 'Perpetual: continuous stores-ledger records; closing inventory is the balancing figure', 4, 'perpetual continuous|perpetual keep continuous|perpetual maintain|perpetual stores ledger|perpetual system stores ledger|perpetual stock ledger|perpetual inventory ledger|perpetual record each|perpetual record every|perpetual system record|perpetual method record|perpetual each receipt|perpetual every receipt|perpetual book record|perpetual based book|perpetual system continuous|perpetual method continuous', 'closing inventory balanc|closing stock balanc|closing inventory residual|closing stock residual|inventory balancing figure|closing inventory is the balancing|closing stock is the balancing|closing inventory as balanc|closing stock as balanc'),
               P('p3', 'Losses hidden under periodic / control possible under perpetual', 2, 'hidden|loss|control|theft|pilferage|shortage', min=1)], 'c6'),
            V('v7', 'What is the effect on profit if closing inventory is overstated, and if opening inventory is overstated?',
              'If closing inventory is overstated, cost of goods sold falls and profit is overstated. If opening inventory is overstated, cost of goods sold rises and profit is understated.',
              [P('p1', 'Closing overstated → profit overstated', 5, 'overstat closing profit go up|overstat closing profit up|overstat closing profit increas|overstat closing profit higher|overstat closing profit overstat|overstat closing cost goods sold fall profit|overstat closing cost of goods sold fall|closing overstat profit go up|closing inventory overstat profit overstat|closing stock overstat profit overstat|closing overstat profit overstat|closing overstat profit increas|closing overstat profit higher|closing inventory overstat profit increas|closing inventory overstat profit higher|closing stock overstat profit higher|closing stock overstat profit increas|closing inventory overstat cost of goods sold fall profit overstat|closing overstat cost goods sold fall profit overstat|closing inventory overstat cost goods sold decreas profit overstat|closing overstat cogs fall profit overstat|closing inventory overstat cost goods sold fall profit overstat|closing inventory higher profit higher|overstat closing inventory increas profit|overstat closing stock increas profit|overstat closing inventory raise profit|overstat closing stock raise profit|closing inventory overstat increas profit|closing stock overstat increas profit|cost goods sold fall profit|cost goods sold decreas profit|cost goods sold lower profit|cost goods sold reduc profit|cogs fall profit|cogs decreas profit'),
               P('p2', 'Opening overstated → profit understated', 5, 'overstat opening profit lower|overstat opening profit down|overstat opening profit understat|overstat opening profit decreas|overstat opening profit fall|overstat opening cost goods sold rise profit|opening overstat profit go down|opening inventory overstat profit understat|opening stock overstat profit understat|opening overstat profit understat|opening overstat profit decreas|opening overstat profit lower|opening overstat profit reduc|opening inventory overstat profit decreas|opening inventory overstat profit lower|opening stock overstat profit lower|opening inventory overstat cost goods sold rise profit understat|opening overstat cost goods sold rise profit understat|opening inventory overstat cost goods sold increas profit understat|opening overstat cogs rise profit understat|opening inventory higher profit lower|overstat opening inventory reduc profit|overstat opening stock reduc profit|overstat opening inventory decreas profit|overstat opening stock decreas profit|overstat opening inventory lower profit|opening inventory overstat reduc profit|opening stock overstat reduc profit|cost goods sold rise profit|cost goods sold rising profit|cost goods sold increas profit|cost goods sold higher profit|cogs rise profit|cogs increas profit')], 'c2'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Hira Stationers — choosing a cost formula', 'difficulty': 'hard',
            'case': ('Hira Stationers keeps periodic records for its premium notebooks. Opening inventory on 1 April 2026: 100 units @ ₹40. Purchases: June 300 units @ ₹42; October 150 units @ ₹44. '
                     'Sales during the year were 350 units at ₹60 each. On 31 March 2027, 200 units are in stock; their net realisable value is ₹45 each.'),
            'mcqs': [
                dict(M('k1a', 'Closing inventory under FIFO is:', [R(k_f), '₹8,400', '₹8,200', '₹8,800'], 0,
                  'Under FIFO, the earliest units are sold first, so the 200 units left come from the latest purchases: 150 units from October at ₹44 = ₹6,600, plus 50 units from June at ₹42 = ₹2,100, totalling ₹8,700. The tempting ₹8,400 values all 200 units at ₹42, ignoring that the latest batch cost ₹44. In practice: stationery shops often follow FIFO, since older stock should be sold before it becomes outdated.', 'c7', 'moderate', '150*44+50*42'), topic='Cost formulas based on historical cost'),
                dict(M('k1b', 'The periodic weighted average cost per unit (to two decimals) is:', ['₹42.18', '₹42.00', '₹42.67', '₹44.00'], 0,
                  'Weighted average cost = total cost of goods available ÷ total units. Cost = 100 × ₹40 + 300 × ₹42 + 150 × ₹44 = ₹23,200 for 550 units, so average = ₹42.18. The tempting ₹42.00 is a simple average of the three prices, ignoring quantities; ₹42.67 leaves out the opening inventory. In practice: accounting software computes weighted average automatically from all receipts in the period.', 'c7', 'hard', 'round(23200/550,2)'), topic='Cost formulas based on historical cost'),
                dict(M('k1c', 'Cost of goods sold under FIFO is:', [R(k_cogs), '₹14,800', '₹15,000', '₹23,200'], 0,
                  'Cost of goods sold = cost of goods available − closing inventory = ₹23,200 − ₹8,700 (FIFO) = ₹14,500. As a check, the 350 units sold are 100 × ₹40 + 250 × ₹42 = ₹4,000 + ₹10,500 = ₹14,500. The tempting ₹14,800 uses the ₹8,400 closing figure. In practice: gross profit = sales 350 × ₹60 = ₹21,000 − ₹14,500 = ₹6,500, which the owner would compare with prior years.', 'c7', 'hard', '23200-8700'), topic='Cost formulas based on historical cost'),
                dict(M('k1d', 'Applying lower of cost and NRV to the FIFO figure, inventory is shown at:', [R(k_f), '₹9,000', '₹12,000', '₹8,400'], 0,
                  'Inventory is shown at the lower of cost and NRV. FIFO cost = ₹8,700; NRV = 200 × ₹45 = ₹9,000. Cost is lower, so inventory is shown at ₹8,700. The tempting ₹9,000 uses NRV even though it is higher, which would recognise an unrealised profit of ₹300. In practice: a write-down is needed only when NRV falls below cost — for example, if a new model makes old notebooks hard to sell.', 'c3', 'moderate', '150*44+50*42'), topic='Basis: lower of cost and net realisable value'),
            ]}],
    }


# ---------- Auto-check data for the Write tab ----------
# Per scheme point: kw (viva-matcher keyword groups, "|" = alternatives) + min (groups needed), nums (figures that must
# appear), rows ([particular keywords, side, amount] — the student's table lines: journal/trial balance dr|cr = debit or
# credit column, ledger dr|cr = debit or credit side of the account; account names fuzzy, amount exact), wrong (common
# wrong statements → remark), ai_only (not checkable offline). Per question: extra_ok (may points beyond the model earn credit).
# BRS / statement tables: side add|less = the Add or Less part of the statement ('' = any).
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'nums': [10400]},
           's2': {'nums': [14200, 5800]},
           's3': {'nums': [2900]},
           's4': {'nums': [53, 56.75]},
           's5': {'nums': [2837.5]},
           's6': {'kw': ['receipt|received|recd|purchase', 'issue', 'balance'], 'min': 3}},
    'q2': {'extra_ok': True,
           's1': {'kw': ['physical count|physical verification|stock taking|counting|physical|stocktaking', 'book record|stores ledger|continuous record|record|stock ledger|bin card|continuous|perpetual'], 'min': 2},
           's2': {'kw': ['cost goods sold|cogs|cost sales|cost of sales', 'closing inventory|closing stock'], 'min': 2},
           's3': {'kw': ['loss|shortage|theft|pilferage|abnormal|wastage', 'control|hidden|come light|detect|reveal|identif|conceal|absorb|known|unknown|discover'], 'min': 2},
           's4': {'kw': ['cost|costly|expensive|cheap|simple|economical', 'disrupt|stop|closure|interrupt|halt|suspend|without stopping|operation|work|business'], 'min': 2}},
    'q3': {'extra_ok': False,
           's1': {'kw': ['count|counted|physical|25 march|stock taking|stocktaking', 'add|plus'], 'min': 2},
           's2': {'rows': [['purchase', 'add', 38000], ['return', 'less', 2000]]},
           's3': {'rows': [['sale|cost', 'less', 41250]]},
           's4': {'rows': [['damage|nrv|write|written|loss|realisable|realizable', 'less', 5000]]},
           's5': {'nums': [301750]}},
    'q4': {'extra_ok': False,
           's1': {'kw': ['|'.join(f'{a} {b}' for a in ('gst', 'input tax', 'tax', '34200') for b in ('excluded', 'exclude', 'not included', 'recoverable', 'not part', 'ignored', 'input credit', 'credit available', 'not added', 'not cost', 'not considered'))
                         + '|' + '|'.join(f'{b} {a}' for a in ('gst', 'tax') for b in ('excluded', 'exclude', 'excluding', 'not include', 'recoverable', 'ignore'))], 'min': 1, 'rows': [['freight|carriage', '', 6000]],
                  'wrong': [{'kw': ['224200|gst included|including gst'], 'say': 'GST for which input credit is available is recoverable and is not part of the cost of inventory.'}]},
           's2': {'rows': [['labour|labor|wages', '', 45000]]},
           's3': {'kw': ['storage|administration|selling|commission', 'exclud|not included|not part|ignored|period cost|expense|not added|not cost|charged'], 'min': 2},
           's4': {'nums': [280000, 263000]}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
