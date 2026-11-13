"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 2 Ind AS 16 Property, Plant and Equipment.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u02'
T1 = 'Recognition of PPE'
T2 = 'Initial measurement'
T3 = 'Subsequent measurement: cost and revaluation models'
T4 = 'Depreciation and derecognition'


def build():
    ck = Checks()
    cost = ck.add('50*0.95+2+3+1.5+4', 'Cost of the machine (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'What goes into cost?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Prism Ltd. buys a machine (₹ lakh): list price 50 less 5% trade discount; GST 9 (fully creditable); freight 2; installation 3; testing costs 1.5 (samples produced during testing sold for 0.5); general administration overhead allocated 1; staff training 0.8; present value of the obligation to dismantle and restore the site at the end of life 4. Compute the cost.',
          'solution': [table(['Item', 'Treatment', '₹ lakh'], [
              ['Purchase price net of trade discount', '50 × 95%', '47.5'],
              ['GST (creditable)', 'Exclude', '—'],
              ['Freight and installation', 'Include', '5.0'],
              ['Testing costs', 'Include', '1.5'],
              ['Sale of test samples', 'Recognise in profit or loss (not deducted from cost)', '—'],
              ['Admin overhead and training', 'Exclude — expense', '—'],
              ['Decommissioning obligation (PV)', 'Include; provision under Ind AS 37', '4.0'],
              ['Cost of the machine', '', str(cost)]], title='Initial measurement')],
          'checks': list(ck)}

    ck2 = Checks()
    sur = ck2.add('96-(100-2*10)', 'Revaluation surplus at end of year 2 (₹ crore)')
    dep3 = ck2.add('96/8', 'Depreciation from year 3 (₹ crore)')
    ca4 = ck2.add('96-2*12', 'Carrying amount end of year 4 before revaluation (₹ crore)')
    pl = ck2.add('(72-50)-16', 'Decrease charged to profit or loss (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Up and then down', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A building cost ₹100 crore (life 10 years, nil residual, straight-line) and is carried under the revaluation model. At the end of year 2 it is revalued to ₹96 crore (remaining life unchanged). At the end of year 4 it is revalued to ₹50 crore. The entity does not transfer surplus to retained earnings annually. Show the accounting.',
          'solution': [table(['Step', 'Working', '₹ crore'], [
              ['Carrying amount end of year 2', '100 − 2 × 10', inr(80)],
              ['Revaluation surplus (OCI)', '96 − 80', inr(sur)],
              ['Depreciation years 3–4', '96 ÷ 8 a year', inr(dep3) + ' each'],
              ['Carrying amount end of year 4', '96 − 24', inr(ca4)],
              ['Decrease on revaluation', '72 − 50', inr(22)],
              ['Charged to OCI (against surplus)', '', inr(16)],
              ['Charged to profit or loss', '22 − 16', inr(pl)]], title='Revaluation model')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'PPE are tangible items held for use in production or supply of goods or services, for rental, or for administrative purposes, expected to be used for more than one period.',
            'An item is recognised when future economic benefits are probable and its cost can be measured reliably. Spare parts, stand-by and servicing equipment are PPE if they meet the definition; otherwise inventory. Items may be aggregated where individually insignificant (e.g. moulds, tools).',
            'Safety or environmental equipment that does not directly raise benefits is still recognised if needed to obtain benefits from other assets. Bearer plants (e.g. tea bushes, fruit trees) are PPE.'],
          'Long-lived tangible items used in the business, not for sale, are PPE.',
          'An effluent treatment plant without which the factory cannot legally operate is PPE.'),
        C('c2', T2, [
            'Cost includes: purchase price (with non-refundable duties and taxes, net of trade discounts and rebates); costs needed to get the asset to where and how management intends to use it (site preparation, delivery, installation, professional fees, employee costs of construction, testing whether it functions properly); and the initial estimate of dismantling and restoration costs.',
            'Excluded: costs of opening a new facility, advertising, conducting business in a new location or with new customers (including staff training), administration and general overheads, costs after the asset is ready (initial operating losses, relocation). Proceeds from selling items produced while testing are recognised in profit or loss with related costs, not deducted from cost.',
            'Deferred payment beyond normal credit: cost is the cash price equivalent, with the difference as interest. Exchange of assets: measured at fair value unless the exchange lacks commercial substance or fair value is not reliably measurable, in which case at the carrying amount of the asset given up.'],
          'Cost stops accumulating once the asset is ready to use as intended.',
          'Start-up losses of a new plant running below capacity are expensed, not capitalised.'),
        C('c3', T3, [
            'After recognition, an entity chooses the cost model (cost less depreciation and impairment) or the revaluation model (fair value at revaluation date less later depreciation and impairment) for each class of PPE.',
            'Revaluations happen often enough to keep the book figure close to fair value at each reporting date, and the whole class is revalued together. Accumulated depreciation is either restated proportionately or eliminated against the gross amount.',
            'An increase goes to OCI (revaluation surplus), except to the extent it reverses a previous decrease recognised in profit or loss. A decrease goes to profit or loss, except to the extent of any surplus for that asset, which is debited in OCI. Surplus may be transferred directly to retained earnings as the asset is used or on derecognition — never through profit or loss.',
            'Subsequent costs: day-to-day servicing is expensed; replacement of significant parts and major inspections are capitalised when criteria are met, and the replaced part\'s carrying amount is derecognised.'],
          'Revaluation gains go to OCI; losses hit profit only after the asset\'s own surplus is used up.',
          'An aircraft\'s periodic heavy maintenance check is capitalised as a component and depreciated until the next check.'),
        C('c4', T4, [
            'Each part with a cost significant to the total is depreciated separately (component approach). Depreciation reflects the pattern of consumption — straight-line, diminishing balance or units of production — and begins when the asset is available for use.',
            'Depreciable amount is cost less residual value. Residual value, useful life and method are reviewed at least each year end; changes are changes in estimates (Ind AS 8). Land usually has an unlimited life and is not depreciated; buildings are. Revenue-based depreciation is not appropriate. Schedule II to the Companies Act provides indicative useful lives.',
            'Derecognition occurs on disposal or when no future benefits are expected. The gain or loss (net proceeds less carrying amount) goes to profit or loss — gains are not classified as revenue. Assets held for rental routinely sold are transferred to inventory when they cease to be rented.'],
          'Depreciation spreads cost over the period the asset is used, in a pattern that matches its consumption.',
          'A ship\'s hull, engines and interiors may have different lives and are depreciated separately.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Capitalisation review', 'role': 'Audit senior',
             'situation': 'A client capitalised ₹3 crore to "plant under construction" including training, inauguration and trial-run losses.',
             'steps': ['Classify each cost as directly attributable or not.', 'Check proceeds from testing are in profit or loss.', 'Confirm the date the plant was ready for use.', 'Reclassify non-qualifying costs to expense.'],
             'takeaway': 'Only costs that make the asset ready for its intended use belong in PPE.'}]

    mcqs = [
        Q('m1', 'Spare parts that meet the definition of PPE are:', ['Recognised as PPE', 'Always inventory', 'Expensed immediately', 'Intangible assets'], 0,
          'Ind AS 16 treats spares, stand-by and servicing equipment as PPE if they meet the definition. In practice: otherwise inventory.', 'c1', T1),
        Q('m2', 'Which cost is capitalised to PPE?', ['Site preparation', 'Staff training on the new machine', 'Advertising the new product', 'General administration overhead'], 0,
          'Site preparation is directly attributable. The others are excluded. In practice: keep supporting evidence.', 'c2', T2),
        Q('m3', 'Proceeds from selling samples produced during testing are:', ['Recognised in profit or loss', 'Deducted from the asset\'s cost', 'Credited to OCI', 'Ignored'], 0,
          'The amended Ind AS 16 requires recognising them in profit or loss with related costs. In practice: disclose amounts.', 'c2', T2),
        Q('m4', 'Under the revaluation model, revaluation is applied to:', ['The entire class of PPE', 'Only selected assets', 'Only land', 'Only assets with gains'], 0,
          'Revaluing the whole class prevents selective revaluation. In practice: rolling basis allowed if completed quickly.', 'c3', T3),
        Q('m5', 'A revaluation increase reversing an earlier decrease charged to profit or loss is:', ['Recognised in profit or loss to that extent', 'Recognised entirely in OCI', 'Ignored', 'Credited to retained earnings'], 0,
          'Reversals of prior losses go through profit or loss first. In practice: any excess goes to OCI.', 'c3', T3),
        Q('m6', 'Transfer of revaluation surplus to retained earnings is made:', ['Directly, not through profit or loss', 'Through profit or loss', 'Through OCI recycling', 'It is not allowed'], 0,
          'Surplus may move directly to retained earnings as the asset is used or derecognised. In practice: optional annual transfer.', 'c3', T3),
        Q('m7', 'A change in useful life of PPE is:', ['A change in accounting estimate', 'A change in accounting policy', 'An error', 'A revaluation'], 0,
          'Reviews of life, residual value and method are estimate changes. In practice: prospective.', 'c4', T4),
        Q('m8', 'Gain on sale of PPE is presented as:', ['Other income, not revenue', 'Revenue from operations', 'OCI', 'Equity'], 0,
          'Ind AS 16 prohibits classifying gains as revenue. In practice: rental fleet sales may be revenue via inventory transfer.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Price and taxes', 1.5, 'concept', 'discount|GST'), S('s2', 'Directly attributable', 1.5, 'concept', 'freight|installation|testing'),
           S('s3', 'Exclusions', 1, 'concept', 'exclude'), S('s4', 'Total cost', 2, 'computation', 'cost', nums=[cost])],
          ['Mark include/exclude for each.'], ['Deducting test sample proceeds from cost.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Surplus', 2, 'computation', 'surplus', nums=[sur]), S('s2', 'Revised depreciation', 1.5, 'computation', 'depreciation', nums=[dep3]),
           S('s3', 'Split of decrease', 3.5, 'computation', 'profit or loss', nums=[pl])],
          ['Use the surplus first.'], ['Charging the whole decrease to profit or loss.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When is an item of PPE recognised?', 'When the entity is likely to receive future economic benefits from it and can measure its cost reliably.',
          [P('p1', 'Likely benefits', 5, 'likely|benefit'), P('p2', 'Reliable cost', 5, 'reliabl')], 'c1'),
        V('v2', 'Name three costs excluded from PPE.', 'Costs of opening a new facility, staff training, and general administration overheads, along with initial operating losses.',
          [P('p1', 'Opening or training', 5, 'opening|training'), P('p2', 'Admin or losses', 5, 'administration|losses')], 'c2'),
        V('v3', 'How is a revaluation decrease treated?', 'Debited to OCI to the extent of any revaluation surplus for that asset, with the balance charged to profit or loss.',
          [P('p1', 'OCI first', 5, 'oci|surplus'), P('p2', 'Balance to P&L', 5, 'profit or loss')], 'c3'),
        V('v4', 'What is the component approach?', 'Depreciating separately each part of an asset whose cost is significant relative to the total, using its own useful life.',
          [P('p1', 'Significant parts', 5, 'significant|part'), P('p2', 'Separate lives', 5, 'separate|own')], 'c4'),
        V('v5', 'How often are residual value and useful life reviewed?', 'At least at each financial year end, with changes treated as changes in accounting estimates.',
          [P('p1', 'Each year end', 5, 'year end|annual'), P('p2', 'Estimate change', 5, 'estimate')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Skyline Airways Ltd.', 'difficulty': 'hard',
              'case': 'Skyline Airways Ltd. buys an aircraft for ₹600 crore: airframe ₹420 crore (life 20 years), engines ₹150 crore (life 10 years) and cabin interiors ₹30 crore (life 5 years). It must carry out a heavy maintenance check every 4 years costing ₹24 crore; the first check is included in the purchase price. Residual values are nil.',
              'mcqs': [
                  M('k1a', 'Annual depreciation of the engines (₹ crore):', ['15', '30', '21', '6'], 0,
                    '150 ÷ 10 = 15. In practice: engines are a separate component.', 'core', check=15, topic=T4),
                  M('k1b', 'The embedded first maintenance check is:', ['Identified as a component and depreciated over 4 years', 'Expensed on purchase', 'Ignored', 'Treated as inventory'], 0,
                    'A major inspection embedded in cost is a separate component until the next check. In practice: ₹6 crore a year.', 'hard', topic=T3),
                  M('k1c', 'Airframe depreciation after carving out the ₹24 crore check (₹ crore a year):', ['19.8', '21', '20', '24'], 0,
                    '(420 − 24) ÷ 20 = 19.8, assuming the check was embedded in the airframe value. In practice: allocate carefully.', 'hard', check=19.8, topic=T4),
                  M('k1d', 'When the next heavy check is done for ₹24 crore:', ['It is capitalised and any remaining carrying amount of the old check is derecognised', 'It is expensed', 'It is added to engines', 'It revalues the aircraft'], 0,
                    'Major inspections meeting recognition criteria are capitalised, replacing the previous one. In practice: depreciate over the next 4 years.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 2, 'Ind AS 16 "Property, Plant and Equipment"',
                ['Apply the recognition criteria for PPE, including spares.',
                 'Measure the cost of PPE at initial recognition.',
                 'Apply the cost and revaluation models.',
                 'Compute depreciation using components and account for derecognition.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['fin-p1-ch05-u01'],
                 'exam_tip': 'In revaluation questions, track the surplus asset by asset — decreases use the same asset\'s surplus first.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Recognise: probable benefits, reliable cost; spares as PPE if they qualify.',
                             'Cost: price + directly attributable + dismantling; testing proceeds to P&L.',
                             'Cost or revaluation model by class.',
                             'Increase → OCI (unless reversing P&L loss); decrease → OCI to extent of surplus, rest P&L.',
                             'Component depreciation; annual review; land not depreciated.'],
                 'remember': ['Surplus transfer to retained earnings bypasses P&L.'],
                 'traps': ['Gains on disposal are not revenue.']},
                [('Model choice', 'By class'), ('Revaluation gain', 'OCI'), ('Revaluation loss', 'OCI then P&L'), ('Review', 'Life, residual, method — yearly')],
                viva, cases)
