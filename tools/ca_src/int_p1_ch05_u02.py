"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 2 — AS 10 Property, Plant and Equipment.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u02'
T1 = 'Definition and recognition of PPE'
T2 = 'Elements of cost and costs not capitalised'
T3 = 'Cost model and revaluation model'
T4 = 'Depreciation: components, residual value, life and method'
T5 = 'Derecognition and disclosure'


def build():
    ck = Checks()
    pp = ck.add('5000000-200000', 'Purchase price net of trade discount (₹)')
    test = ck.add('80000-30000', 'Testing cost net of sample sales (₹)')
    cost = ck.add('4800000+60000+140000+50000+150000', 'Cost of the machine (₹)')
    i1 = {'id': 'i1', 'title': 'Building up the cost of a machine', 'difficulty': 'core', 'minutes': 8,
          'q': 'Arjun Polymers Ltd. bought a machine: list price ₹50,00,000, trade discount ₹2,00,000, GST ₹9,00,000 (input credit available), freight ₹60,000, installation ₹1,40,000, testing ₹80,000 (samples produced during testing sold for ₹30,000), general administration allocated ₹50,000, inauguration ceremony ₹40,000, and present value of estimated dismantling cost ₹1,50,000. Compute the cost.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Purchase price less trade discount', 'Include', inr(pp)],
              ['GST with input credit', 'Exclude — recoverable', '—'],
              ['Freight and installation', 'Include', inr(200000)],
              ['Testing less sample proceeds', 'Include net', inr(test)],
              ['General administration', 'Exclude', '—'],
              ['Inauguration ceremony', 'Exclude', '—'],
              ['Dismantling cost (present value)', 'Include', inr(150000)],
              ['Cost of the machine', '', inr(cost)]], title='AS 10 cost')],
          'checks': list(ck)}

    ck2 = Checks()
    up = ck2.add('1200000-800000', 'Revaluation surplus on upward revaluation (₹)')
    pl = ck2.add('(900000-400000)-400000', 'Excess decrease charged to profit and loss (₹)')
    i2 = {'id': 'i2', 'title': 'Up and then down', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Kirti Ltd. revalued its land (carrying amount ₹8,00,000) to ₹12,00,000 in year 1. In year 4, with carrying amount ₹9,00,000 and the full surplus still in revaluation reserve, it is revalued to ₹4,00,000. (For simplicity, the year-4 carrying amount is taken as given.) Show the treatment in both years.',
          'solution': [table(['Year', 'Change', 'Treatment', '₹'], [
              ['1', 'Increase 8,00,000 → 12,00,000', 'Credit revaluation surplus (other equity)', inr(up)],
              ['4', 'Decrease 9,00,000 → 4,00,000 = 5,00,000', 'First debit revaluation surplus', inr(400000)],
              ['4', '', 'Balance to profit and loss', inr(pl)]], title='Revaluation model')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Property, plant and equipment (PPE) are physical assets that an enterprise keeps to make goods, provide services, rent out or run its offices, and that it expects to use for longer than one period.',
            'An item is recognised as an asset if it is probable that future economic benefits will flow to the enterprise and its cost can be measured reliably.',
            'Spare parts, stand-by equipment and servicing equipment are PPE when they meet the definition; otherwise they are inventory.',
            'Items such as safety or environmental equipment may be recognised even if they do not directly increase benefits, because they are needed to obtain benefits from other assets. Major inspections and replaced parts are recognised in the carrying amount, with the old part derecognised.'],
          'If you will use it for more than a year and can measure what it cost, it belongs on the balance sheet.',
          'A pollution filter required by law is PPE even though it makes nothing.'),
        C('c2', T2, [
            'Cost comprises purchase price (including import duties and non-refundable taxes, after trade discounts and rebates), any cost needed to get the asset to its site and working state as management intends, and the initial estimate of dismantling, removal and site restoration obligations.',
            'Directly attributable costs include employee costs of construction or acquisition, site preparation, delivery and handling, installation and assembly, professional fees and testing whether the asset functions properly (net of proceeds from items produced while testing).',
            'Not capitalised: opening a new facility, introducing a new product (advertising), conducting business in a new location or with new customers (including training), administration and general overheads, costs incurred after the asset is ready but not yet used, initial operating losses, and relocation or reorganisation costs.',
            'An asset acquired in exchange for another is measured at fair value unless the exchange lacks commercial substance or fair values cannot be reliably measured, in which case the carrying amount of the asset given up is used.'],
          'Capitalise only what it takes to get the asset ready for its job.',
          'Salary of engineers installing a machine is capitalised; salary of the sales team launching its product is not.'),
        C('c3', T3, [
            'After recognition an enterprise chooses the cost model (cost less accumulated depreciation and impairment) or the revaluation model (fair value at revaluation date less later depreciation and impairment) for an entire class of PPE.',
            'Revaluations are made regularly enough that the carrying amount does not differ materially from fair value.',
            'An increase is credited to revaluation surplus, except to the extent it reverses an earlier decrease recognised in profit and loss. A decrease is charged to profit and loss, except to the extent of any credit balance in revaluation surplus for that asset.',
            'Revaluation surplus may be transferred directly to retained earnings when realised — on retirement or disposal, or progressively as the asset is used (difference between depreciation on revalued amount and on cost). It is not routed through profit and loss.'],
          'Choose cost or fair value for a whole class, not item by item.',
          'Revaluing one office building while keeping another at cost is not allowed if both are in the same class.'),
        C('c4', T4, [
            'Each part of an item with a cost significant in relation to the total is depreciated separately (component approach).',
            'Depreciable amount = cost (or revalued amount) less residual value; it is allocated systematically over the useful life. Depreciation starts when the asset is available for use and stops when it is derecognised; it continues while idle unless fully depreciated (usage methods may give nil).',
            'Residual value and useful life are reviewed at least at each financial year end; changes are changes in estimates.',
            'The method (straight-line, diminishing balance, units of production) reflects the pattern of consumption of benefits; it is reviewed annually and a change is a change in accounting estimate, applied prospectively. Land usually has unlimited life and is not depreciated.'],
          'Depreciate each significant part over its own life, and revisit the estimates every year.',
          'An aircraft\'s engines and its body are depreciated separately because their lives differ.'),
        C('c5', T5, [
            'An item is derecognised on disposal or when no future benefits are expected from its use or disposal.',
            'The gain or loss on derecognition = net disposal proceeds − carrying amount, recognised in profit and loss; gains are not classified as revenue.',
            'PPE retired from use and held for sale is shown separately, valued at its carrying amount or NRV, whichever is less.',
            'Disclosures for each class include measurement bases, depreciation methods, useful lives or rates, gross carrying amount and accumulated depreciation at beginning and end, and a reconciliation of movements; for revalued classes, the date, valuer involvement and surplus movements.'],
          'When the asset leaves, compare what you got with what it was carried at.',
          'A truck with carrying amount ₹3 lakh sold for ₹3.5 lakh gives a gain of ₹50,000, not sales revenue.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Capitalisation review', 'role': 'Audit assistant',
             'situation': 'A client capitalised a new plant along with launch advertising, staff training and three months of start-up losses.',
             'steps': ['List each cost and test it against AS 10.', 'Remove launch, training and losses.', 'Check dismantling obligations.', 'Set depreciation start date and components.'],
             'takeaway': 'Only costs to make the asset ready for use are capitalised.'}]

    mcqs = [
        Q('m1', 'Which cost is capitalised as part of PPE?', ['Site preparation', 'Advertising for the new product', 'Staff training for the new location', 'Initial operating losses'], 0,
          'Site preparation is directly attributable to bringing the asset to working condition. Advertising, training and start-up losses relate to running the business and are expensed. In practice: separate project and launch costs.', 'c2', T2),
        Q('m2', 'Proceeds from selling samples produced while testing a machine are:', ['Deducted from the cost of testing', 'Treated as revenue', 'Credited to capital reserve', 'Ignored'], 0,
          'Testing costs to check that an asset works properly are capitalised net of the proceeds from items produced during testing. This keeps the asset at its true cost. In practice: track test-run sales separately.', 'c2', T2),
        Q('m3', 'Under the revaluation model, revaluation applies to:', ['The entire class of PPE to which the asset belongs', 'Only the asset chosen', 'Only land', 'Only assets with increased values'], 0,
          'If an item is revalued, the entire class to which it belongs must be revalued, to avoid selective revaluation and mixing of measurement bases. In practice: classes include land, buildings, plant and so on.', 'c3', T3),
        Q('m4', 'An upward revaluation that reverses an earlier downward revaluation charged to profit and loss is:', ['Credited to profit and loss to that extent', 'Credited wholly to revaluation surplus', 'Ignored', 'Credited to capital reserve'], 0,
          'An increase is recognised in profit and loss to the extent it reverses a decrease of the same asset previously recognised there; any excess goes to revaluation surplus. In practice: track each asset\'s history.', 'c3', T3, 'moderate'),
        Q('m5', 'A change in depreciation method under AS 10 is treated as:', ['A change in accounting estimate, applied prospectively', 'A change in accounting policy with retrospective effect', 'A prior period item', 'An extraordinary item'], 0,
          'AS 10 requires the method to be reviewed at least annually; a change to reflect a changed pattern of consumption is a change in estimate under AS 5 and is applied prospectively. In practice: disclose the effect.', 'c4', T4),
        Q('m6', 'Cost ₹12,00,000; residual value ₹2,00,000; useful life 8 years; straight-line. Annual depreciation:', ['₹1,25,000', '₹1,50,000', '₹1,00,000', '₹1,75,000'], 0,
          'Depreciable amount is cost less residual value, ₹10,00,000, spread over 8 years = ₹1,25,000 a year. Residual value and life are reviewed every year. In practice: start from the date available for use.', 'c4', T4, 'core', check=125000),
        Q('m7', 'Depreciation of an asset begins when:', ['It is available for use', 'It is first used to full capacity', 'It is paid for', 'The financial year begins'], 0,
          'Depreciation starts when the asset is in the location and condition needed to operate as management intends, even if not yet used. It continues while idle unless a usage method gives nil. In practice: record the ready-for-use date.', 'c4', T4),
        Q('m8', 'Gain on sale of an item of PPE is:', ['Recognised in profit and loss but not as revenue', 'Credited to revaluation surplus', 'Treated as revenue from operations', 'Credited to capital reserve'], 0,
          'The difference between net disposal proceeds and carrying amount is recognised in profit and loss, but AS 10 states that gains are not classified as revenue. In practice: show it under other income.', 'c5', T5),
        Q('m9', 'Spare parts used for more than one period that meet the PPE definition are:', ['Recognised as PPE', 'Always inventory', 'Expensed when bought', 'Shown as investments'], 0,
          'Major spare parts and stand-by equipment qualify as PPE when they meet the definition — expected to be used for more than a period. Otherwise they are carried as inventory and expensed on use. In practice: classify by expected usage.', 'c1', T1),
        Q('m10', 'Residual value and useful life of PPE are reviewed:', ['At least at each financial year end', 'Once every five years', 'Only when the asset is revalued', 'Never after recognition'], 0,
          'AS 10 requires residual value and useful life to be reviewed at least at each financial year end; differences from previous estimates are accounted for as changes in estimate. In practice: document the review.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Net purchase price and recoverable GST', 1.5, 'computation', 'discount', nums=[pp]),
           S('s2', 'Net testing and dismantling', 1.5, 'computation', 'testing|dismantling', nums=[test]),
           S('s3', 'Exclusions and total', 2, 'computation', 'exclude', nums=[cost])],
          ['Mark each item include/exclude.'], ['Capitalising the inauguration.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Upward to surplus', 1.5, 'computation', 'surplus', nums=[up]),
           S('s2', 'Downward first against surplus', 1.5, 'concept', 'first'),
           S('s3', 'Excess to profit and loss', 1, 'computation', 'profit and loss', nums=[pl])],
          ['Use the surplus first.'], ['Charging the whole fall to profit and loss.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When is an item of PPE recognised?', 'When it is probable that future economic benefits from it will flow to the enterprise and its cost can be measured reliably.',
          [P('p1', 'Probable benefits', 5, 'benefit'), P('p2', 'Reliable cost', 5, 'reliab')], 'c1'),
        V('v2', 'Name some costs that are not capitalised.', 'Costs of opening a new facility, advertising a new product, training staff for a new location, general administration, initial operating losses and relocation costs.',
          [P('p1', 'Launch and advertising', 5, 'advertis|new product|facility'), P('p2', 'Admin and losses', 5, 'administration|losses|relocation')], 'c2'),
        V('v3', 'What is the component approach?', 'Each part of an item whose cost is significant relative to the total is depreciated separately over its own useful life.',
          [P('p1', 'Significant parts', 5, 'significant|part'), P('p2', 'Separately', 5, 'separate')], 'c4'),
        V('v4', 'How is a revaluation decrease treated?', 'It is charged to profit and loss, except to the extent of any credit balance in the revaluation surplus for that asset, which is reduced first.',
          [P('p1', 'Against surplus first', 5, 'surplus'), P('p2', 'Excess to profit and loss', 5, 'profit and loss')], 'c3'),
        V('v5', 'How is the gain or loss on derecognition computed?', 'As the difference between net disposal proceeds and the carrying amount, recognised in profit and loss and shown apart from revenue.',
          [P('p1', 'Proceeds less carrying amount', 6, 'proceeds', 'carrying'), P('p2', 'Not revenue', 4, 'revenue')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Pavan Logistics Ltd.', 'difficulty': 'moderate',
              'case': 'Pavan Logistics Ltd. bought a crane for ₹80 lakh. The crane\'s engine (₹20 lakh) lasts 5 years and the body (₹60 lakh) 15 years; residual values are nil. It also bought two identical warehouses; it wants to revalue only one.',
              'mcqs': [
                  M('k1a', 'First-year depreciation using the component approach (straight-line):', ['₹8 lakh', '₹5.33 lakh', '₹16 lakh', '₹4 lakh'], 0,
                    'Engine: ₹20 lakh ÷ 5 = ₹4 lakh; body: ₹60 lakh ÷ 15 = ₹4 lakh; total ₹8 lakh. Depreciating the whole crane over 15 years would give only ₹5.33 lakh. In practice: identify significant parts.', 'moderate', check=8, topic=T4),
                  M('k1b', 'Revaluing only one warehouse is:', ['Not permitted; the whole class must be revalued', 'Permitted', 'Permitted with disclosure', 'Required'], 0,
                    'AS 10 requires the revaluation model to be applied to the entire class of PPE. Both warehouses are in the same class, so both must be revalued or neither. In practice: define classes clearly.', 'core', topic=T3),
                  M('k1c', 'When the engine is replaced after 5 years, the new engine cost is:', ['Capitalised and the old engine derecognised', 'Expensed as repairs', 'Added to the body', 'Charged to revaluation surplus'], 0,
                    'Replacement of a significant part that meets recognition criteria is capitalised, and the carrying amount of the replaced part is derecognised. In practice: the old engine is fully depreciated by then.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 2, 'Accounting Standard 10 Property, Plant and Equipment',
                ['Recognise PPE and determine its cost.',
                 'Apply the cost and revaluation models.',
                 'Compute depreciation using components, residual values and useful lives.',
                 'Account for derecognition and give the disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['int-p1-ch05-u01'],
                 'exam_tip': 'Prepare an include/exclude table for cost questions; for revaluation, track each asset\'s past surplus and losses.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Recognise if benefits probable and cost reliable.', 'Cost: price + directly attributable + dismantling estimate; recoverable taxes excluded.',
                             'No capitalisation of launch, training, admin, start-up losses.', 'Cost or revaluation model by class; surplus in equity.',
                             'Component depreciation; review life, residual value and method yearly (estimate changes).', 'Derecognition gain/loss in P&L, not revenue.'],
                 'remember': ['Depreciation starts when available for use.'],
                 'traps': ['Method change is an estimate change, applied prospectively.']},
                [('Recognition', 'Probable benefits + reliable cost'), ('Models', 'Cost or revaluation (whole class)'), ('Method change', 'Change in estimate')],
                viva, cases)
