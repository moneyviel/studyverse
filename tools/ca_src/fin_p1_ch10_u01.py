"""CA Final · Paper 1 Financial Reporting · Chapter 10 Unit 1 Ind AS 41 Agriculture.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch10-u01'
T1 = 'Scope: biological assets, produce and bearer plants'
T2 = 'Recognition and measurement at fair value less costs to sell'
T3 = 'Gains, losses and agricultural produce'
T4 = 'Government grants and disclosure'


def build():
    ck = Checks()
    open_ = ck.add('100*(20000-500)/100000', 'Herd at start: 100 cows (₹ lakh)')
    close = ck.add('(100+20)*(23000-500)/100000', 'Herd at year end: 120 cows (₹ lakh)')
    birth = ck.add('20*(23000-500)/100000', 'Gain on initial recognition of calves (₹ lakh)')
    chg = ck.add('100*(23000-500)/100000-100*(20000-500)/100000', 'Fair value gain on existing herd (₹ lakh)')
    milk = ck.add('5000*40/100000', 'Milk recognised as inventory (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A dairy herd for one year', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Green Pastures Dairy starts the year with 100 cows (fair value ₹20,000 each); 20 calves are born during the year. At year end, fair value is ₹23,000 per animal for all 120 animals. Costs to sell are ₹500 per animal throughout. During the year, 5,000 litres of milk were harvested when fair value less costs to sell was ₹40 per litre. Compute the amounts.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Opening herd', '100 × (20,000 − 500)', inr(open_)],
              ['Gain on calves born', '20 × 22,500', inr(birth)],
              ['Fair value change on existing cows', '100 × (22,500 − 19,500)', inr(chg)],
              ['Closing herd', '120 × 22,500', inr(close)],
              ['Milk harvested (to inventory, Ind AS 2 thereafter)', '5,000 × 40', inr(milk)]], title='Ind AS 41')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Ind AS 41 or another standard?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Classify: (a) tea bushes; (b) tea leaves on the bushes; (c) plucked tea leaves; (d) processed tea; (e) sheep reared for wool; (f) wool shorn; (g) land on which a plantation stands; (h) a forest of timber trees grown for logs.',
          'solution': [table(['Item', 'Standard', 'Reason'], [
              ['(a) Tea bushes', 'Ind AS 16', 'Bearer plants'],
              ['(b) Leaves on bushes', 'Ind AS 41', 'Produce growing on a bearer plant'],
              ['(c) Plucked leaves', 'Ind AS 41 at harvest, then Ind AS 2', 'Agricultural produce'],
              ['(d) Processed tea', 'Ind AS 2', 'Product of processing after harvest'],
              ['(e) Sheep', 'Ind AS 41', 'Living animals (not bearer plants)'],
              ['(f) Wool', 'Ind AS 41 at harvest, then Ind AS 2', 'Agricultural produce'],
              ['(g) Land', 'Ind AS 16 or 40', 'Not a biological asset'],
              ['(h) Timber trees', 'Ind AS 41', 'Grown to be harvested as produce — not bearer plants']], title='Scope')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 41 covers biological assets (living animals and plants), agricultural produce at the point of harvest, and related government grants, when they relate to agricultural activity — the managed growth, change and harvesting of living assets with a view to selling or converting them.',
            'Excluded: land (Ind AS 16/40), bearer plants (Ind AS 16), intangible assets, and produce after harvest (Ind AS 2). The produce growing on bearer plants is still within Ind AS 41.',
            'A bearer plant is a living plant used to produce or supply agricultural produce, expected to bear produce for more than one period, with a remote chance of being sold as produce except for incidental scrap sales. Animals are never bearer plants.'],
          'Ind AS 41 is about living things that grow, and the crop at the moment it is picked.',
          'Mango trees are bearer plants; mangoes on the tree are biological assets.'),
        C('c2', T2, [
            'A biological asset or produce is recognised when the entity controls it from past events, future benefits are probable and fair value or cost can be reliably measured.',
            'Biological assets are measured at initial recognition and at each reporting date at fair value less costs to sell. Costs to sell are incremental costs directly attributable to disposal (commissions, levies), excluding finance costs and income taxes. Transport costs to market are reflected in fair value itself.',
            'The standard assumes fair value is reliably measurable. It can be rebutted only on initial recognition when quoted prices are unavailable and alternative estimates are clearly unreliable; then cost less depreciation and impairment is used until fair value becomes reliable.'],
          'Value the living asset at what it would fetch, minus selling costs, every year end.',
          'A young plantation without market prices may be held at cost initially.'),
        C('c3', T3, [
            'Gains or losses on initial recognition (e.g. birth of a calf, which produces a gain; or a loss because costs to sell are deducted) and from changes in fair value less costs to sell are included in profit or loss for the period.',
            'Agricultural produce harvested is measured, when picked, at its fair value minus selling costs; this becomes its cost for Ind AS 2. Gains on initial recognition of produce are in profit or loss.',
            'Subsequent processing (wine from grapes, cheese from milk, sawn timber from logs) is outside Ind AS 41.'],
          'Growth shows up as profit before the crop is sold.',
          'Milk harvested enters inventory at fair value less costs to sell.'),
        C('c4', T4, [
            'An unconditional government grant for a living asset carried at fair value minus selling costs is recognised in profit or loss when it becomes receivable. A conditional grant is recognised when the conditions are met (e.g. farming in an area for a set period).',
            'If the asset is measured at cost (fair value unreliable), Ind AS 20 applies to the grant instead.',
            'Disclosures include the aggregate gain or loss, a description of each group of biological assets, a reconciliation of carrying amounts, restrictions on title, commitments, and financial risk management strategies.'],
          'Grants on fair-valued biological assets go straight to profit when unconditional.',
          'A subsidy to keep sheep for five years is recognised only after five years if forfeitable.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end valuation at a plantation', 'role': 'Plantation accountant',
             'situation': 'The estate holds tea bushes, standing leaves, cattle and a timber block.',
             'steps': ['Separate bearer plants from biological assets.', 'Obtain market prices and deduct costs to sell.', 'Record harvested produce at fair value less costs to sell.', 'Prepare the reconciliation of carrying amounts.'],
             'takeaway': 'Scope decisions come before measurement.'}]

    mcqs = [
        Q('m1', 'Bearer plants are accounted for under:', ['Ind AS 16', 'Ind AS 41', 'Ind AS 2', 'Ind AS 38'], 0,
          'They behave like machinery. In practice: produce on them stays in Ind AS 41.', 'c1', T1),
        Q('m2', 'Biological assets are measured at:', ['Fair value less costs to sell', 'Cost', 'Net realisable value', 'Replacement cost'], 0,
          'At initial recognition and each reporting date. In practice: reliable-measurement presumption.', 'c2', T2),
        Q('m3', 'Agricultural produce after harvest is accounted for under:', ['Ind AS 2', 'Ind AS 41', 'Ind AS 16', 'Ind AS 115'], 0,
          'Ind AS 41 measures it at harvest only. In practice: that value becomes cost.', 'c3', T3),
        Q('m4', 'A gain on the birth of a calf is recognised in:', ['Profit or loss', 'OCI', 'Equity directly', 'Deferred income'], 0,
          'All changes go to profit or loss. In practice: disclose the aggregate.', 'c3', T3),
        Q('m5', 'Transport costs to get animals to market are:', ['Reflected in determining fair value', 'Costs to sell', 'Capitalised', 'Ignored'], 0,
          'Fair value is net of transport to the principal market. In practice: commissions are costs to sell.', 'c2', T2),
        Q('m6', 'Is a dairy cow a bearer plant?', ['No — animals are never bearer plants', 'Yes', 'Only if milked', 'Only if older than one year'], 0,
          'The definition covers plants only. In practice: cows stay in Ind AS 41.', 'c1', T1),
        Q('m7', 'A conditional grant on a fair-valued biological asset is recognised:', ['When conditions are met', 'When received', 'Over the asset life', 'Never'], 0,
          'Forfeitable grants wait. In practice: partial recognition if conditions allow.', 'c4', T4),
        Q('m8', 'If fair value cannot be measured reliably on initial recognition, the asset is measured at:', ['Cost less depreciation and impairment', 'Zero', 'Net realisable value', 'Fair value anyway'], 0,
          'Until fair value becomes reliable. In practice: rare.', 'c2', T2),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Opening', 1, 'computation', 'opening', nums=[open_]), S('s2', 'Calves', 1.5, 'computation', 'calves|birth', nums=[birth]), S('s3', 'Fair value change', 1.5, 'computation', 'fair value', nums=[chg]), S('s4', 'Closing', 1.5, 'computation', 'closing', nums=[close]), S('s5', 'Milk', 1.5, 'computation', 'milk', nums=[milk])],
          ['Reconcile opening to closing.'], ['Measuring milk at cost.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Bearer plants', 1.5, 'concept', 'bearer'), S('s2', 'Produce', 2, 'concept', 'produce|harvest'), S('s3', 'Others', 1.5, 'concept', 'land|ind as 2')],
          ['Name the standard.'], ['Treating timber trees as bearer plants.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is agricultural activity?', 'Managing the biological transformation and harvest of living animals or plants for sale or conversion into produce or more biological assets.',
          [P('p1', 'Biological transformation', 6, 'transformation'), P('p2', 'Harvest', 4, 'harvest')], 'c1'),
        V('v2', 'Define a bearer plant.', 'A living plant used to produce agricultural produce, expected to bear for more than one period, with only a remote likelihood of being sold as produce.',
          [P('p1', 'Bears for more than one period', 5, 'more than one'), P('p2', 'Remote sale as produce', 5, 'remote')], 'c1'),
        V('v3', 'How are biological assets measured?', 'At fair value less costs to sell at initial recognition and at each reporting date.',
          [P('p1', 'Fair value less costs to sell', 6, 'costs to sell'), P('p2', 'Each reporting date', 4, 'reporting date')], 'c2'),
        V('v4', 'Where do fair value changes go?', 'Into profit or loss for the period in which they arise.',
          [P('p1', 'Profit or loss', 6, 'profit or loss'), P('p2', 'Period', 4, 'period')], 'c3'),
        V('v5', 'How is a conditional grant on a biological asset treated?', 'It is recognised in profit or loss only when the attached conditions are met.',
          [P('p1', 'Conditions met', 6, 'conditions'), P('p2', 'Profit or loss', 4, 'profit or loss')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Orchard Valley Ltd.', 'difficulty': 'moderate',
              'case': 'Orchard Valley Ltd. owns apple trees (bearer plants) and apples growing on them, which have a fair value less costs to sell of ₹12 lakh at year end. It also grows eucalyptus for pulp. The state grants ₹5 lakh if the orchard stays productive for 3 years; one year has passed. Harvested apples worth ₹30 lakh (fair value less costs to sell) were moved to the cold store.',
              'mcqs': [
                  M('k1a', 'The apple trees are measured under:', ['Ind AS 16 at cost or revaluation', 'Ind AS 41 at fair value', 'Ind AS 2', 'Ind AS 40'], 0,
                    'Bearer plants follow Ind AS 16. In practice: depreciate over productive life.', 'core', topic=T1),
                  M('k1b', 'Apples on the trees are carried at (₹ lakh):', ['12', '30', 'Nil', '42'], 0,
                    'Produce still growing is a biological asset, carried at fair value minus selling costs. In practice: change goes to P&L.', 'moderate', check=12, topic=T2),
                  M('k1c', 'The eucalyptus plantation is:', ['A biological asset under Ind AS 41', 'A bearer plant', 'Inventory', 'Investment property'], 0,
                    'Grown to be harvested as produce. In practice: fair value at each year end.', 'core', topic=T1),
                  M('k1d', 'The ₹5 lakh grant after one year is:', ['Not yet recognised, as conditions are unmet', 'Recognised in full', 'One-third recognised', 'Credited to equity'], 0,
                    'Recognise when conditions are met, unless partly earned. In practice: read terms.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch10', 1, 'Ind AS 41 "Agriculture"',
                ['Define the scope of Ind AS 41 and distinguish bearer plants.',
                 'Measure biological assets at fair value less costs to sell.',
                 'Account for gains, losses and harvested produce.',
                 'Treat government grants and prepare disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p1-ch09-u01'],
                 'exam_tip': 'Split the scope first: bearer plant (Ind AS 16), growing produce (Ind AS 41), harvested produce (Ind AS 2).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Biological assets at fair value less costs to sell.',
                             'Bearer plants under Ind AS 16.',
                             'Produce at harvest: fair value less costs to sell, then Ind AS 2.',
                             'All changes in profit or loss.',
                             'Conditional grants when conditions met.'],
                 'remember': ['Animals are never bearer plants.'],
                 'traps': ['Treating transport costs as costs to sell.']},
                [('Measure', 'FV less costs to sell'), ('Bearer plants', 'Ind AS 16'), ('Harvested produce', 'Ind AS 2'), ('Gains', 'Profit or loss')],
                viva, cases)
