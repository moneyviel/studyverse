"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 6 Ind AS 40 Investment Property.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u06'
T1 = 'What counts as investment property'
T2 = 'Recognition and initial measurement'
T3 = 'Cost model and fair value disclosure'
T4 = 'Transfers and disposals'


def build():
    ck = Checks()
    dep = ck.add('(500-100)/40', 'Annual depreciation on building (₹ lakh)')
    cv = ck.add('500-(500-100)/40*3', 'Carrying amount after 3 years (₹ lakh)')
    gain = ck.add('620-(500-(500-100)/40*3)', 'Gain on disposal (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'An office tower held for rent', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Skyline Ltd. buys an office tower for ₹480 lakh plus ₹20 lakh of legal and registration costs, to let it to tenants. Land component is ₹100 lakh. The building has a 40-year life and nil residual value. Fair value after 3 years is ₹640 lakh, and the property is then sold for ₹620 lakh. Compute initial cost, annual depreciation, carrying amount at the end of year 3 and the gain on sale.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Initial cost', '480 + 20 transaction costs', inr(500)],
              ['Depreciable amount', '500 − land 100', inr(400)],
              ['Annual depreciation', '400 ÷ 40', inr(dep)],
              ['Carrying amount after 3 years', '500 − 3 × 10', inr(cv)],
              ['Fair value (disclosed only)', 'Not recognised under the cost model', inr(640)],
              ['Gain on sale to profit or loss', '620 − 470', inr(gain)]], title='Ind AS 40 cost model')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Investment property or not?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Classify: (a) land bought with no decided use; (b) the head office building; (c) flats being built for sale to buyers; (d) a building let to a subsidiary, in the separate accounts of the parent; (e) the same building in the consolidated accounts; (f) a hotel the company runs itself; (g) a building where 5% of floor space is used by the owner and the rest let, and portions cannot be sold separately.',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Investment property', 'Undecided future use is treated as held for appreciation'],
              ['(b)', 'PPE (Ind AS 16)', 'Owner-occupied'],
              ['(c)', 'Inventory (Ind AS 2)', 'Held for sale in ordinary business'],
              ['(d)', 'Investment property', 'Let to another entity of the group — separate accounts view'],
              ['(e)', 'PPE', 'Owner-occupied from the group\'s viewpoint'],
              ['(f)', 'PPE', 'Significant services provided — an owner-managed operation'],
              ['(g)', 'Investment property', 'Owner use is insignificant']], title='Classification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Investment property is land or a building (or part of one, or both) held by the owner or a lessee under a right-of-use asset to earn rentals, for capital appreciation, or both — not for use in production, supply or administration and not for sale in the normal course of trade.',
            'Examples: land held for long-term appreciation; land whose future use is not yet decided; a building let under operating leases; a vacant building held to be let; property being built for future use as investment property.',
            'Not investment property: property held for sale in ordinary business (inventory); owner-occupied property and property awaiting disposal from owner use (PPE); property let under a finance lease. Dual-use property is split if parts are separately saleable; otherwise it is investment property only if owner use is insignificant. Ancillary services are fine, but significant services (as in a hotel) make it owner-occupied.'],
          'Ask why the property is held: rent or appreciation means investment property; use or trade means something else.',
          'A building let to a fellow subsidiary is investment property in standalone accounts but PPE in the group\'s.'),
        C('c2', T2, [
            'Recognise when future benefits are probable and cost is reliably measurable. This applies both to initial costs and later costs of adding to, replacing part of, or servicing it; day-to-day servicing is expensed.',
            'Initial measurement is cost including transaction costs such as legal fees, property transfer taxes and other directly attributable costs. Start-up costs, initial operating losses before planned occupancy and abnormal waste are excluded.',
            'Deferred payment: cost is the cash price equivalent, with the difference treated as interest. Exchanges: fair value unless commercial substance is absent or fair value cannot be reliably measured. A right-of-use asset held as investment property follows Ind AS 116 initially.'],
          'Initial cost works like PPE: price plus costs to get it ready.',
          'Stamp duty and registration on a let building are capitalised.'),
        C('c3', T3, [
            'Ind AS 40 permits only the cost model after recognition: the asset is measured under the Ind AS 16 cost requirements (cost less accumulated depreciation and impairment), unless it meets held-for-sale criteria (Ind AS 105) or is a right-of-use asset (Ind AS 116).',
            'Land is not depreciated; buildings are depreciated over their useful lives, with significant components depreciated separately.',
            'Even though the cost model is used, the entity must disclose the fair value of investment property, the extent to which a qualified independent valuer was involved, and cases where fair value could not be reliably measured. Rental income, direct operating expenses and restrictions are also disclosed.'],
          'In India, the balance sheet shows cost; fair value appears only in the notes.',
          'A building bought for 500 and now worth 640 stays at its depreciated cost.'),
        C('c4', T4, [
            'Transfers to or from investment property occur only when there is a change in use, supported by evidence — e.g. start of owner occupation (to PPE), start of development with a view to sale (to inventory), end of owner occupation (from PPE), or inception of an operating lease to another party (from inventory). A change in management intention alone is not evidence.',
            'Under the cost model, transfers do not change the carrying amount or the cost for measurement or disclosure purposes.',
            'Derecognise on disposal or when permanently withdrawn with no expected benefits. The gain or loss is net disposal proceeds less carrying amount, recognised in profit or loss. Compensation from third parties for impaired or lost property is recognised in profit or loss when receivable.'],
          'A transfer needs actual change in use, not just a board decision.',
          'Moving staff into a let building moves it to PPE at the same carrying amount.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reviewing a property portfolio', 'role': 'Financial controller',
             'situation': 'A real estate group holds let buildings, land banks and projects under construction.',
             'steps': ['Classify each property by purpose.', 'Depreciate buildings under the cost model.', 'Obtain fair values for disclosure.', 'Document any change in use with evidence.'],
             'takeaway': 'Purpose drives classification; fair value drives disclosure, not measurement.'}]

    mcqs = [
        Q('m1', 'Under Ind AS 40, investment property after initial recognition is measured using:', ['The cost model only', 'Fair value model only', 'Either model', 'Revaluation model'], 0,
          'Ind AS 40 removed the fair value option. In practice: fair value is disclosed.', 'c3', T3),
        Q('m2', 'Land held for an undecided future use is:', ['Investment property', 'Inventory', 'PPE', 'Not recognised'], 0,
          'Treated as held for capital appreciation. In practice: classification may change when use is decided.', 'c1', T1),
        Q('m3', 'A hotel operated by its owner is:', ['Property, plant and equipment', 'Investment property', 'Inventory', 'A financial asset'], 0,
          'Significant services make it owner-occupied. In practice: a leased-out hotel may differ.', 'c1', T1),
        Q('m4', 'A transfer from investment property to PPE requires:', ['Evidence of a change in use', 'A board resolution only', 'A fair value report', 'Auditor approval'], 0,
          'Intention alone is not enough. In practice: start of owner occupation is evidence.', 'c4', T4),
        Q('m5', 'Property being built for sale in the ordinary course of business is:', ['Inventory', 'Investment property', 'PPE', 'An intangible'], 0,
          'Ind AS 2 applies. In practice: real estate developers hold such stock.', 'c1', T1),
        Q('m6', 'Which cost is excluded from the initial cost of investment property?', ['Operating losses before planned occupancy', 'Legal fees', 'Property transfer taxes', 'Purchase price'], 0,
          'Start-up and early losses are expensed. In practice: capitalise transaction costs only.', 'c2', T2),
        Q('m7', 'Under the cost model, the fair value of investment property is:', ['Disclosed in the notes', 'Recognised in profit or loss', 'Recognised in OCI', 'Ignored entirely'], 0,
          'Disclosure is mandatory. In practice: state the valuer\'s involvement.', 'c3', T3),
        Q('m8', 'A building let to a subsidiary is, in consolidated statements:', ['Owner-occupied property (PPE)', 'Investment property', 'Inventory', 'A finance lease receivable'], 0,
          'The group occupies it. In practice: reclassify on consolidation.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Cost', 1, 'computation', 'cost', nums=[500]), S('s2', 'Depreciation', 1.5, 'computation', 'depreciation', nums=[dep]), S('s3', 'Carrying amount', 1.5, 'computation', 'carrying', nums=[cv]), S('s4', 'Gain', 2, 'computation', 'gain', nums=[gain])],
          ['Exclude land from depreciation.'], ['Recognising the fair value gain.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Investment property items', 3, 'concept', 'investment'), S('s2', 'PPE items', 3, 'concept', 'ppe|owner'), S('s3', 'Inventory', 1, 'concept', 'inventory')],
          ['Reason each item.'], ['Treating group lets as investment property in consolidated accounts.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is investment property?', 'Land or buildings held to earn rentals, for capital appreciation, or both, rather than for own use or sale in the ordinary course.',
          [P('p1', 'Rentals or appreciation', 6, 'rental|appreciation'), P('p2', 'Excludes own use and trade', 4, 'own use|sale')], 'c1'),
        V('v2', 'Which measurement model applies under Ind AS 40?', 'The cost model, applying Ind AS 16 requirements, with fair value disclosed in the notes.',
          [P('p1', 'Cost model', 6, 'cost'), P('p2', 'Fair value disclosed', 4, 'disclos')], 'c3'),
        V('v3', 'When can property be transferred to or from investment property?', 'Only on a change in use evidenced by events such as starting owner occupation or beginning development for sale.',
          [P('p1', 'Change in use', 6, 'change in use'), P('p2', 'Evidence', 4, 'evidenc')], 'c4'),
        V('v4', 'How is dual-use property classified?', 'Portions are accounted for separately if they can be sold separately; otherwise it is investment property only when the owner-occupied part is insignificant.',
          [P('p1', 'Separate portions', 5, 'separately'), P('p2', 'Insignificant own use', 5, 'insignificant')], 'c1'),
        V('v5', 'What is the gain on derecognition?', 'Net disposal proceeds minus the carrying amount, taken to profit or loss.',
          [P('p1', 'Proceeds less carrying amount', 6, 'carrying'), P('p2', 'Profit or loss', 4, 'profit or loss')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Harbour Estates Ltd.', 'difficulty': 'moderate',
              'case': 'Harbour Estates Ltd. owns: a mall let to retailers (cost ₹900 lakh, land ₹300 lakh, life 50 years); a plot bought for future appreciation; and an apartment block under construction for sale. In year 4 it moves its head office into one floor of the mall that cannot be sold separately; the floor is 3% of the mall.',
              'mcqs': [
                  M('k1a', 'Annual depreciation on the mall (₹ lakh):', ['12', '18', '6', 'Nil'], 0,
                    '(900 − 300) ÷ 50 = 12. In practice: land is never depreciated.', 'core', check=12, topic=T3),
                  M('k1b', 'The apartment block under construction is:', ['Inventory', 'Investment property', 'PPE', 'Capital work in progress of IP'], 0,
                    'Being built for sale in ordinary business. In practice: Ind AS 2 applies.', 'core', topic=T1),
                  M('k1c', 'After the head office moves in, the mall is:', ['Still investment property, as own use is insignificant', 'Reclassified wholly to PPE', 'Split into two assets', 'Inventory'], 0,
                    'Three percent use is insignificant and the floor is not separable. In practice: reassess if use grows.', 'moderate', topic=T4),
                  M('k1d', 'The plot held for appreciation is measured at:', ['Cost, with fair value disclosed', 'Fair value through profit or loss', 'Revalued amount', 'Net realisable value'], 0,
                    'Cost model only. In practice: valuer\'s report supports disclosure.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 6, 'Ind AS 40 "Investment Property"',
                ['Identify investment property and distinguish it from PPE and inventory.',
                 'Measure investment property at initial recognition.',
                 'Apply the cost model and the fair value disclosures.',
                 'Account for transfers and disposals.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch05-u05'],
                 'exam_tip': 'Ind AS 40 allows only the cost model — never book fair value gains, but always disclose fair value.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Held for rent or appreciation.',
                             'Initial: cost including transaction costs.',
                             'Subsequent: cost model only; disclose fair value.',
                             'Transfers need evidence of change in use.',
                             'Disposal gain: proceeds less carrying amount.'],
                 'remember': ['Group lets are PPE in consolidated accounts.'],
                 'traps': ['Recognising fair value increases in profit.']},
                [('Investment property', 'Rent or appreciation'), ('Model', 'Cost only'), ('Fair value', 'Disclosed'), ('Transfer', 'Change in use')],
                viva, cases)
