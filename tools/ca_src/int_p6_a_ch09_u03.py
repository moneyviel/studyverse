"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 3 Management of Inventory.
Scope follows the ICAI study material (which cross-refers to Paper 4, Material Cost); explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u03'
T1 = 'Objectives of inventory management'
T2 = 'EOQ, quantity discounts and stock levels'
T3 = 'Selective control and modern techniques'


def build():
    ck = Checks()
    eoq = ck.add('(2*25000*400/20)**0.5', 'EOQ (units)')
    tc = ck.add('25000/1000*400 + 1000/2*20', 'Ordering + carrying cost at EOQ')
    t_eoq = ck.add('25000*100 + 20000', 'Total cost at EOQ including purchases')
    t_disc = ck.add('25000*98 + 25000/2500*400 + 2500/2*98*20/100', 'Total cost with 2% discount at 2,500 units')
    sav = ck.add('2520000-2478500', 'Saving from taking the discount')
    i1 = {'id': 'i1', 'title': 'EOQ versus a bulk discount', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Annual demand 25,000 units; price ₹100; ordering cost ₹400 per order; carrying cost 20% of price a year. Compute EOQ and total relevant cost. The supplier offers a 2% discount on orders of 2,500 units. Should it be accepted?',
          'solution': [table(['Item', 'At EOQ (1,000 units) ₹', 'At 2,500 units ₹'], [
              ['Purchase cost', inr(2500000), inr(2450000)],
              ['Ordering cost', '25 × 400 = 10,000', '10 × 400 = 4,000'],
              ['Carrying cost', '500 × 20 = 10,000', '1,250 × 19.60 = 24,500'],
              ['Total', inr(t_eoq), inr(t_disc)]], title='Quantity discount decision'),
              p('EOQ = √(2 × 25,000 × 400 ÷ 20) = ' + inr(eoq) + ' units. Accept the discount: it saves ₹' + inr(sav) + ' a year.')],
          'checks': list(ck)}

    ck2 = Checks()
    rol = ck2.add('120*12', 'Re-order level')
    mn = ck2.add('1440-80*10', 'Minimum level')
    mx = ck2.add('1440+1000-60*8', 'Maximum level')
    avg = ck2.add('(640+1960)/2', 'Average stock level (min + max) ÷ 2')
    i2 = {'id': 'i2', 'title': 'Setting stock levels', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Daily usage: maximum 120, normal 80, minimum 60 units. Lead time: maximum 12, normal 10, minimum 8 days. Re-order quantity 1,000 units. Compute re-order level, minimum, maximum and average stock levels.',
          'solution': [table(['Level', 'Formula', 'Units'], [
              ['Re-order level', 'Max usage × max lead time', inr(rol)],
              ['Minimum level', 'ROL − normal usage × normal lead time', inr(mn)],
              ['Maximum level', 'ROL + ROQ − min usage × min lead time', inr(mx)],
              ['Average stock', '(Minimum + maximum) ÷ 2', inr(avg)]], title='Stock levels')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Inventory (raw materials, WIP, finished goods, stores) is often the largest current asset. Management aims to keep enough to avoid stock-outs and production stoppages while minimising holding and ordering costs and the risk of obsolescence.',
            'Costs: ordering costs (placing orders, receiving, inspection), carrying costs (storage, insurance, interest on funds, obsolescence), and stock-out costs (lost sales, idle time).',
            'Inventory policy affects working capital, liquidity and profitability; it is linked to production planning and purchasing.'],
          'The right stock is enough to keep the wheels turning — and no more.',
          'Overstocking fashion goods risks markdowns; understocking spare parts risks downtime.'),
        C('c2', T2, [
            'EOQ = √(2AO ÷ C): A stands for yearly demand, O for the cost of placing one order, and C for the yearly cost of holding one unit. At EOQ, ordering cost equals carrying cost and their total is minimum.',
            'Quantity discounts: compare total cost (purchase + ordering + carrying) at EOQ with that at each discount quantity; accept the lowest.',
            'Stock levels: re-order level = maximum usage × maximum lead time; minimum = ROL − normal usage × normal lead time; maximum = ROL + ROQ − minimum usage × minimum lead time; danger level = normal usage × lead time for emergency purchase; average stock = (min + max) ÷ 2 or min + ½ ROQ. Safety stock buffers uncertainty in usage and lead time.'],
          'EOQ balances two costs; stock levels translate it into signals for the stores.',
          'If EOQ is 1,000 and annual demand 25,000, the firm places 25 orders a year.'),
        C('c3', T3, [
            'ABC analysis classifies items by value: A items (few, high value — tight control), B items (moderate), C items (many, low value — simple control). VED (vital, essential, desirable) and FSN (fast, slow, non-moving) classify by criticality and movement.',
            'Just-in-time (JIT) aims to receive materials only when needed, cutting holding costs but requiring reliable suppliers. Inventory turnover ratio and days of inventory monitor efficiency.',
            'Perpetual inventory and periodic physical verification detect discrepancies; obsolete and slow-moving stock is reviewed for disposal.'],
          'Control effort should follow value and criticality, not item count.',
          'A pharma maker keeps vital active ingredients under VED "vital" status even if low value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Stock review', 'role': 'Finance analyst trainee',
             'situation': 'A distributor\'s inventory days have risen from 45 to 75.',
             'steps': ['Run an ABC and FSN analysis.', 'Identify slow and non-moving items.', 'Recompute EOQ and re-order levels for A items.', 'Propose disposal of obsolete stock.'],
             'takeaway': 'Rising inventory days usually hide a few slow-moving high-value items.'}]

    mcqs = [
        Q('m1', 'EOQ with A = 3,600, O = ₹50, C = ₹4:', ['300 units', '150 units', '600 units', '90 units'], 0,
          '√(2 × 3,600 × 50 ÷ 4) = √90,000 = 300. In practice: 12 orders a year.', 'c2', T2, check=300),
        Q('m2', 'At EOQ:', ['Ordering cost equals carrying cost', 'Ordering cost is zero', 'Carrying cost is double ordering cost', 'Purchase cost is minimum'], 0,
          'The minimum of total ordering and carrying cost is where they are equal. In practice: use to check answers.', 'c2', T2),
        Q('m3', 'Re-order level is:', ['Maximum usage × maximum lead time', 'Minimum usage × minimum lead time', 'EOQ ÷ 2', 'Average usage × average lead time'], 0,
          'It ensures stock lasts even in the worst case before a new order arrives. In practice: add safety stock thinking.', 'c2', T2),
        Q('m4', 'In ABC analysis, "A" items are:', ['Few in number but high in value', 'Many and low value', 'Obsolete', 'Fast moving only'], 0,
          'A items typically form a small share of items but most of the value. In practice: control tightly.', 'c3', T3),
        Q('m5', 'JIT inventory requires:', ['Reliable suppliers and short lead times', 'Large safety stocks', 'Infrequent orders', 'High carrying costs'], 0,
          'JIT minimises stock, so supply reliability is critical. In practice: works best with nearby vendors.', 'c3', T3),
        Q('m6', 'Carrying cost includes:', ['Interest on funds tied in stock', 'Cost of placing orders', 'Freight on purchases', 'Lost sales'], 0,
          'Holding stock ties up funds, space and insurance. In practice: often expressed as % of value.', 'c1', T1),
        Q('m7', 'FSN analysis classifies stock by:', ['Rate of movement', 'Value', 'Criticality', 'Supplier'], 0,
          'Fast, slow and non-moving items. In practice: non-moving stock is reviewed for disposal.', 'c3', T3),
        Q('m8', 'When evaluating a quantity discount, compare:', ['Total purchase, ordering and carrying costs', 'Only ordering costs', 'Only purchase price', 'Only carrying costs'], 0,
          'All relevant costs change with order size. In practice: carrying cost per unit may fall with the price.', 'c2', T2),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'EOQ', 2, 'computation', 'EOQ', nums=[eoq]), S('s2', 'Costs at EOQ', 1, 'computation', 'ordering|carrying', nums=[tc]),
           S('s3', 'Cost with discount', 2, 'computation', 'discount', nums=[t_disc]), S('s4', 'Decision', 1, 'computation', 'saving', nums=[sav])],
          ['Include purchase cost in both.'], ['Ignoring carrying cost increase.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'ROL', 1, 'computation', 're-order', nums=[rol]), S('s2', 'Min and max', 2, 'computation', 'minimum|maximum', nums=[mn, mx]), S('s3', 'Average', 1, 'computation', 'average', nums=[avg])],
          ['Use the right usage and lead time in each formula.'], ['Using normal usage for ROL.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State the EOQ formula.', 'The square root of two times annual demand times ordering cost per order, divided by carrying cost per unit per year.',
          [P('p1', 'Square root', 4, 'square root'), P('p2', 'Variables', 6, 'demand|ordering|carrying')], 'c2'),
        V('v2', 'What is safety stock?', 'Extra stock held to protect against uncertainty in demand or lead time.',
          [P('p1', 'Extra stock', 5, 'extra|buffer'), P('p2', 'Uncertainty', 5, 'uncertain')], 'c2'),
        V('v3', 'Explain ABC analysis.', 'Classifying inventory into high, medium and low value groups so that control effort is concentrated on high-value A items.',
          [P('p1', 'Value groups', 5, 'value'), P('p2', 'Control focus', 5, 'control')], 'c3'),
        V('v4', 'Name two inventory carrying costs.', 'Interest on funds blocked and storage and insurance costs, along with obsolescence.',
          [P('p1', 'Interest', 5, 'interest'), P('p2', 'Storage or insurance', 5, 'storage|insurance|obsolesc')], 'c1'),
        V('v5', 'What is the main risk of JIT?', 'Production may stop if suppliers fail to deliver on time, since little buffer stock is held.',
          [P('p1', 'Supplier failure', 5, 'supplier|deliver'), P('p2', 'No buffer', 5, 'buffer|stop')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Sunrise Bakery', 'difficulty': 'core',
              'case': 'Sunrise Bakery uses 7,200 kg of flour a year; each order costs ₹250; flour costs ₹40/kg; carrying cost is 25% of price a year. Lead time is 5 days; daily usage averages 20 kg and peaks at 30 kg.',
              'mcqs': [
                  M('k1a', 'EOQ:', ['600 kg', '424 kg', '720 kg', '1,200 kg'], 0,
                    'Carrying cost ₹10 a kg; √(2 × 7,200 × 250 ÷ 10) = √3,60,000 = 600 kg. In practice: round to bag sizes.', 'moderate', check=600, topic=T2),
                  M('k1b', 'Orders per year:', ['12', '6', '24', '10'], 0,
                    '7,200 ÷ 600 = 12 orders. In practice: about one a month.', 'core', check=12, topic=T2),
                  M('k1c', 'Re-order level:', ['150 kg', '100 kg', '600 kg', '200 kg'], 0,
                    'Maximum usage 30 × lead time 5 = 150 kg. In practice: order when stock falls to this.', 'core', check=150, topic=T2),
                  M('k1d', 'Under VED analysis flour for a bakery is:', ['Vital', 'Desirable', 'Essential only for festivals', 'Non-moving'], 0,
                    'Without flour production stops, so it is vital. In practice: keep a safety buffer.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 3, 'Management of Inventory',
                ['Explain the objectives and costs of inventory.',
                 'Compute EOQ, evaluate discounts and set stock levels.',
                 'Apply ABC, VED, FSN and JIT ideas.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 30}, 'prereq': ['int-p6-a-ch09-u02'],
                 'exam_tip': 'For discount questions, put EOQ and each discount quantity side by side with all three costs.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['EOQ = √(2AO/C); ordering cost = carrying cost at EOQ.',
                             'Discounts: compare total costs including purchases.',
                             'ROL, minimum, maximum, average and danger levels.',
                             'ABC, VED, FSN; JIT needs reliable supply.'],
                 'remember': ['Carrying cost per unit = price × carrying %.'],
                 'traps': ['ROL uses maximum usage and maximum lead time.']},
                [('EOQ', '√(2AO/C)'), ('ROL', 'Max usage × max lead time'), ('Max level', 'ROL + ROQ − min usage × min lead time')],
                viva, cases)
