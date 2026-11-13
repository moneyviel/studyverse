"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 11 Joint Products and By-Products.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch11-u01'
T1 = 'Joint products, by-products and the split-off point'
T2 = 'Apportioning joint costs'
T3 = 'Accounting for by-products'
T4 = 'Sell at split-off or process further?'


def build():
    ck = Checks()
    pa = ck.add('300000*4000/10000', 'Physical units — A')
    pb = ck.add('300000*6000/10000', 'Physical units — B')
    sa = ck.add('300000*240000/480000', 'Sales value at split-off — A')
    sb = ck.add('300000*240000/480000', 'Sales value at split-off — B')
    i1 = {'id': 'i1', 'title': 'Sharing a joint cost', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A joint process costing ₹3,00,000 yields 4,000 kg of A (sale price at split-off ₹60/kg) and 6,000 kg of B (₹40/kg). Apportion the joint cost by (a) physical units and (b) sales value at split-off. Comment.',
          'solution': [table(['Product', 'Physical units ₹', 'Sales value ₹'], [
              ['A', inr(pa), inr(sa)],
              ['B', inr(pb), inr(sb)],
              ['Total', inr(300000), inr(300000)]], title='Joint cost apportionment'),
              p('Physical units give both products ₹30/kg, so A shows a 50% margin and B only 25%. The sales value method gives A ₹37.50/kg and B ₹25/kg — an equal 37.5% margin on each, matching cost with earning power.')],
          'checks': list(ck)}

    ck2 = Checks()
    inc_rev = ck2.add('6000*(52-40)', 'Incremental revenue from processing B further')
    gain = ck2.add('72000-50000', 'Net gain from further processing')
    i2 = {'id': 'i2', 'title': 'Refine or sell now?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'In the case above, B can be processed further at an additional cost of ₹50,000 and sold at ₹52/kg. Should it be processed further?',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Incremental revenue', '6,000 × (52 − 40)', inr(inc_rev)],
              ['Incremental cost', '', inr(50000)],
              ['Net gain', '', inr(gain)]], title='Further processing decision'),
              p('Process further: incremental revenue exceeds incremental cost. The joint cost is sunk and irrelevant to this decision.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Joint products are two or more products of significant value produced simultaneously from the same raw material and process, none being clearly the main product (e.g. petrol, diesel and kerosene from crude oil).',
            'By-products are products of small value produced incidentally with the main product (e.g. molasses in sugar, bran in flour milling).',
            'The split-off point is the stage at which joint products become separately identifiable; costs before it are joint costs, and costs after it are separable (further processing) costs.'],
          'One input, several outputs: the question is how much of the shared cost each output should carry.',
          'Dairy processing gives cream and skimmed milk as joint products and whey as a by-product.'),
        C('c2', T2, [
            'Physical units method: joint cost shared by weight or volume — simple, but ignores value.',
            'Average unit cost method: total joint cost ÷ total units, used where units are comparable.',
            'Survey or point value method: products given weights or points based on technical surveys.',
            'Sales value at split-off: in proportion to sales value at the split-off point. Net realisable value: final sales value minus further processing and selling costs, used when products cannot be sold at split-off. Constant gross margin: overall gross margin % is applied to each product\'s final sales, and joint cost is the balancing figure after deducting separable costs.'],
          'Value-based methods share cost according to what each product can earn.',
          'A product with half the weight but three-quarters of the value carries three-quarters of joint cost under the sales value method.'),
        C('c3', T3, [
            'By-product accounting: (a) sales of by-product treated as other income in P&L; (b) net realisable value of by-product credited to the main product\'s cost; (c) standard or comparative price credited to the joint process; (d) re-use price where the by-product is used internally.',
            'Where by-products are of small value, method (a) is common; where significant, the NRV reduces main product cost.',
            'Waste that has no value or disposal cost is treated differently — its disposal cost adds to main product cost.'],
          'By-products reduce the main product\'s cost or add to income — they are not allotted a share of joint cost.',
          'Molasses worth ₹2 lakh credited to sugar processing reduces the cost of sugar.'),
        C('c4', T4, [
            'Decision to process further: compare incremental revenue (final value − split-off value) with incremental (separable) cost. Process further only if incremental revenue exceeds incremental cost.',
            'Joint costs are sunk at split-off and irrelevant to the decision; the apportionment method does not change the answer.',
            'Non-financial points: capacity, demand for the refined product, and risk.'],
          'Look only at what changes after split-off; the past shared cost does not.',
          'If refining costs ₹10 per unit and adds ₹8 of price, sell at split-off.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Product profitability review', 'role': 'Cost accountant trainee',
             'situation': 'Sales wants to drop a joint product that "shows a loss" in management accounts.',
             'steps': ['Check the joint cost apportionment method.', 'Recompute using sales value or NRV.', 'Note that joint costs continue even if one product is dropped.', 'Advise on contribution after separable costs.'],
             'takeaway': 'A loss created by an arbitrary allocation is not a reason to drop a product.'}]

    mcqs = [
        Q('m1', 'Joint products are:', ['Two or more products of significant value from one process', 'Products of small value incidentally produced', 'Waste materials', 'Products from different processes'], 0,
          'They share a common input and process and each has substantial value. In practice: oil refining is the classic example.', 'c1', T1),
        Q('m2', 'Costs incurred after the split-off point are:', ['Separable costs', 'Joint costs', 'Sunk costs only', 'Fixed costs only'], 0,
          'After split-off, costs can be traced to each product. In practice: they are relevant to further processing decisions.', 'c1', T1),
        Q('m3', 'Joint cost ₹1,20,000; X sales value ₹90,000, Y ₹60,000 at split-off. Cost to X:', ['₹72,000', '₹60,000', '₹90,000', '₹48,000'], 0,
          '1,20,000 × 90/150 = 72,000. In practice: Y gets ₹48,000.', 'c2', T2, 'moderate', check=72000),
        Q('m4', 'The NRV method deducts from final sales value:', ['Further processing and selling costs', 'Joint costs', 'Profit margin', 'Material cost'], 0,
          'NRV = final sales value − separable costs. In practice: used when no split-off market exists.', 'c2', T2),
        Q('m5', 'Under the constant gross margin method, joint cost for each product is:', ['A balancing figure after deducting margin and separable cost from sales', 'Physical units × rate', 'Sales value × margin', 'NRV × margin'], 0,
          'The overall gross margin % is applied to each product; joint cost is what remains after separable costs. In practice: may produce negative allocations.', 'c2', T2),
        Q('m6', 'A by-product\'s net realisable value is often:', ['Credited to the main product\'s cost', 'Added to joint cost', 'Ignored', 'Debited to P&L'], 0,
          'It reduces the cost of the main product. In practice: small by-product sales may be other income.', 'c3', T3),
        Q('m7', 'In a further processing decision, joint costs are:', ['Irrelevant', 'The main factor', 'Added to separable costs', 'Doubled'], 0,
          'They are incurred whether or not further processing happens. In practice: compare incremental figures only.', 'c4', T4),
        Q('m8', 'Split-off value ₹50/unit; after processing ₹65/unit; processing cost ₹12/unit. Decision:', ['Process further — gain ₹3 per unit', 'Sell at split-off', 'Indifferent', 'Process further — gain ₹15 per unit'], 0,
          'Incremental revenue ₹15 > incremental cost ₹12, so a ₹3 gain. In practice: check capacity.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Physical units', 2, 'computation', 'physical', nums=[pa, pb]), S('s2', 'Sales value', 2, 'computation', 'sales value', nums=[sa]), S('s3', 'Comment', 1, 'concept', 'value|ability')],
          ['Show ratios.'], ['Including separable costs.'], ['Table and comment.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Incremental revenue', 1, 'computation', 'incremental', nums=[inc_rev]), S('s2', 'Net gain', 1, 'computation', 'gain', nums=[gain]), S('s3', 'Joint cost sunk', 1, 'concept', 'sunk|irrelevant')],
          ['Ignore joint cost.'], ['Comparing total profits after allocation.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Distinguish joint products and by-products.', 'Joint products have significant value and are equally important, while by-products have small value and arise incidentally with the main product.',
          [P('p1', 'Significant value', 5, 'significant'), P('p2', 'Small and incidental', 5, 'small|incidental')], 'c1'),
        V('v2', 'What is the split-off point?', 'The stage in production at which joint products become separately identifiable.',
          [P('p1', 'Stage', 4, 'stage|point'), P('p2', 'Separately identifiable', 6, 'separate|identif')], 'c1'),
        V('v3', 'Why prefer the sales value method?', 'It matches joint cost with each product\'s ability to bear it, avoiding misleading losses on low-value products.',
          [P('p1', 'Ability to bear', 6, 'ability|bear'), P('p2', 'Avoids distortion', 4, 'mislead|loss|distort')], 'c2'),
        V('v4', 'How is a by-product treated under the NRV method?', 'The by-product\'s net realisable value is credited against, and so lowers, the main product\'s cost.',
          [P('p1', 'NRV', 5, 'realisable|nrv'), P('p2', 'Reduces main cost', 5, 'main product|deduct')], 'c3'),
        V('v5', 'When should a product be processed further?', 'When the incremental revenue from further processing is greater than the incremental cost, ignoring joint costs.',
          [P('p1', 'Incremental comparison', 6, 'incremental'), P('p2', 'Joint cost ignored', 4, 'joint')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Agro Mills', 'difficulty': 'moderate',
              'case': 'Agro Mills crushes oilseed (joint cost ₹5,00,000) into oil (8,000 litres, sold after refining at ₹90/litre, refining cost ₹1,20,000) and cake (20,000 kg, sold at ₹12/kg after packing costing ₹40,000). Husk, a by-product, is sold for ₹10,000.',
              'mcqs': [
                  M('k1a', 'NRV of oil:', ['₹6,00,000', '₹7,20,000', '₹5,00,000', '₹8,40,000'], 0,
                    '8,000 × 90 = 7,20,000 − 1,20,000 = 6,00,000. In practice: refining is separable.', 'core', check=600000, topic=T2),
                  M('k1b', 'NRV of cake:', ['₹2,00,000', '₹2,40,000', '₹2,80,000', '₹1,60,000'], 0,
                    '20,000 × 12 = 2,40,000 − 40,000 = 2,00,000. In practice: packing is a selling cost.', 'core', check=200000, topic=T2),
                  M('k1c', 'Joint cost to oil if husk sales reduce joint cost first:', ['₹3,67,500', '₹3,75,000', '₹4,90,000', '₹3,00,000'], 0,
                    'Net joint cost 4,90,000 × 6/8 = 3,67,500. In practice: cake gets ₹1,22,500.', 'hard', check=367500, topic=T3),
                  M('k1d', 'If cake could be sold unpacked at ₹10/kg, packing should be:', ['Continued — it adds ₹40,000 revenue for ₹40,000 cost (indifferent), so judge on other factors', 'Stopped — loss of ₹40,000', 'Continued — gain of ₹2,40,000', 'Stopped — gain of ₹2,00,000'], 0,
                    'Incremental revenue 20,000 × 2 = 40,000 equals incremental cost, so financially indifferent. In practice: consider brand value.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch11', 1, 'Joint Products and By Products',
                ['Distinguish joint products and by-products.',
                 'Apportion joint costs by physical and value methods.',
                 'Account for by-products and decide on further processing.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 35}, 'prereq': ['int-p4-ch10-u01'],
                 'exam_tip': 'Label each figure as joint or separable before you start; it prevents the most common error.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Joint products: significant value; by-products: small, incidental.',
                             'Methods: physical units, average, survey, sales value, NRV, constant gross margin.',
                             'By-product: other income, NRV credit, standard price, re-use price.',
                             'Further processing: incremental revenue vs incremental cost.'],
                 'remember': ['Joint costs are sunk for further-processing decisions.'],
                 'traps': ['Physical units can make valuable products look cheap.']},
                [('Sales value method', 'Share by split-off value'), ('NRV', 'Final value − separable cost'), ('Process further if', 'ΔRevenue > ΔCost')],
                viva, cases)
