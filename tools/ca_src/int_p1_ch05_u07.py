"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 7 — AS 28 Impairment of Assets.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u07'
T1 = 'When to test: indications of impairment'
T2 = 'Recoverable amount: net selling price and value in use'
T3 = 'Recognising an impairment loss'
T4 = 'Cash-generating units, goodwill and corporate assets'
T5 = 'Reversal of impairment loss and disclosure'


def build():
    ck = Checks()
    viu = ck.add('15*(0.9091+0.8264+0.7513)', 'Value in use (₹ lakh)')
    rec = ck.add('max(38, 37.302)', 'Recoverable amount (₹ lakh)')
    loss = ck.add('50-38', 'Impairment loss (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Testing one machine', 'difficulty': 'core', 'minutes': 7,
          'q': 'A machine of Varsha Ltd. has a carrying amount of ₹50 lakh. Demand for its output has fallen. It could be sold for ₹40 lakh with disposal costs of ₹2 lakh. If kept, it will generate net cash inflows of ₹15 lakh a year for 3 years; discount rate 10% (factors 0.9091, 0.8264, 0.7513). Compute the impairment loss.',
          'solution': [table(['Step', 'Working', '₹ lakh'], [
              ['Net selling price', '40 − 2', R(38)],
              ['Value in use', '15 × 2.4868', R(viu)],
              ['Recoverable amount (higher)', '', R(rec)],
              ['Impairment loss', '50 − 38', R(loss)]], title='AS 28 test'),
              note('The loss is charged to profit and loss (the machine is carried at cost). Future depreciation is based on the new carrying amount of ₹38 lakh.')],
          'checks': list(ck)}

    ck2 = Checks()
    tot = ck2.add('10+60+40', 'Carrying amount of the unit (₹ lakh)')
    l2 = ck2.add('110-80', 'Impairment loss of the unit (₹ lakh)')
    mach = ck2.add('(30-10)*60/100', 'Loss allocated to machinery (₹ lakh)')
    bldg = ck2.add('(30-10)*40/100', 'Loss allocated to building (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Allocating a unit\'s loss', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A cash-generating unit of Ojas Ltd. carries goodwill ₹10 lakh, machinery ₹60 lakh and building ₹40 lakh. Its recoverable amount is ₹80 lakh. No individual asset\'s recoverable amount is determinable. Allocate the impairment loss.',
          'solution': [table(['Asset', 'Working', 'Loss ₹ lakh', 'Revised ₹ lakh'], [
              ['Unit total', f'{R(tot)} − 80', R(l2), '80'],
              ['Goodwill', 'First, in full', R(10), '0'],
              ['Machinery', '20 × 60/100', R(mach), R(60 - 12)],
              ['Building', '20 × 40/100', R(bldg), R(40 - 8)]], title='Allocation within a CGU'),
              note('After goodwill, the loss is spread over other assets in proportion to carrying amounts — but no asset goes below the highest of its net selling price, value in use (if determinable) and zero.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'An asset is impaired when its carrying amount is more than its recoverable amount. At each balance sheet date the enterprise checks for any indication of impairment; only if there is one does it estimate recoverable amount.',
            'External signs: a sharp fall in market value beyond normal use; adverse changes in technology, market, economy or law; rise in market interest rates that raises discount rates; net assets carried above market capitalisation.',
            'Internal signs: obsolescence or physical damage; plans to discontinue, restructure or dispose of the asset; internal reports showing worse economic performance than expected.',
            'AS 28 covers most assets, but not inventories, construction contract assets, deferred tax assets, financial assets within AS 13 and assets arising from employee benefits.'],
          'Look for warning signs every year; measure only when a sign appears.',
          'A new law banning diesel generators in the city signals impairment of a company\'s diesel gensets.'),
        C('c2', T2, [
            'Recoverable amount = whichever is greater: net selling price or value in use.',
            'Net selling price: the amount obtainable from selling the asset in an arm\'s length transaction, less costs of disposal (excluding finance costs and tax).',
            'Value in use: present value of estimated future cash flows from continuing use and disposal at the end of its life. Cash flows are pre-tax, based on reasonable and supportable assumptions, use budgets for up to five years normally, exclude financing and tax flows, and exclude future restructuring or improvements not yet committed. The discount rate is a pre-tax rate reflecting time value and asset-specific risks.',
            'If either measure exceeds the carrying amount, no impairment exists and the other need not be computed.'],
          'An asset is worth the better of selling it now or using it on.',
          'If an old truck can be sold for more than its book value, no value-in-use calculation is needed.'),
        C('c3', T3, [
            'Impairment loss = carrying amount − recoverable amount. It is recognised as an expense in profit and loss, unless the asset is carried at a revalued amount, in which case it is first set off against the revaluation surplus for that asset.',
            'After recognition, depreciation in future periods is based on the revised carrying amount over the remaining useful life.',
            'If the loss exceeds the carrying amount, a liability is recognised only if another standard requires it.'],
          'Write the asset down to what it can recover, and depreciate from there.',
          'A revalued building with ₹5 lakh surplus suffering a ₹7 lakh impairment: ₹5 lakh against surplus, ₹2 lakh to profit and loss.'),
        C('c4', T4, [
            'If recoverable amount cannot be estimated for an individual asset, it is estimated for the cash-generating unit (CGU) to which it belongs — the smallest identifiable group of assets producing cash inflows largely independent of other assets.',
            'Goodwill: a bottom-up test checks whether goodwill can be allocated reasonably to the CGU; if not, a top-down test applies to the smallest larger unit to which goodwill can be allocated. Corporate assets (head office, IT centre) are handled the same way.',
            'A CGU\'s impairment loss is allocated first to goodwill, then to other assets pro rata on carrying amounts. No asset is reduced below the highest of its net selling price, value in use (if determinable) and zero; any shortfall is spread over the other assets.'],
          'When assets earn only together, test them together.',
          'A bus route\'s buses, depot and permits form one CGU if the route\'s cash flows are independent.'),
        C('c5', T5, [
            'At each balance sheet date the enterprise checks whether an earlier impairment loss may no longer exist or may have decreased; if so, recoverable amount is re-estimated.',
            'A reversal increases the carrying amount, but not above what it would have been (net of depreciation) had no impairment been recognised. It is credited to profit and loss, unless the asset is revalued, when it goes to revaluation surplus (after reversing any loss earlier charged to profit and loss).',
            'An impairment loss on goodwill is reversed only if the loss came from an unusual one-off outside event not expected to recur, and later external events have reversed its effect.',
            'Disclose impairment losses and reversals by class and line item, losses against revaluation surplus, and for material losses the events, amount, nature of asset or CGU, segment, and whether recoverable amount is net selling price or value in use (with discount rate).'],
          'Reversals are allowed, but never above the "no-impairment" carrying amount.',
          'An asset written down to ₹40 lakh, which would now be ₹45 lakh without impairment, cannot be restored above ₹45 lakh.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end impairment review', 'role': 'Reporting analyst',
             'situation': 'A plant\'s output prices have fallen 25% and the company\'s market capitalisation is below book value.',
             'steps': ['Record the indications.', 'Identify the asset or CGU.', 'Estimate net selling price and value in use.', 'Allocate any loss and update depreciation.'],
             'takeaway': 'Indicators trigger the test; recoverable amount decides the loss.'}]

    mcqs = [
        Q('m1', 'Recoverable amount is:', ['The higher of net selling price and value in use', 'The lower of net selling price and value in use', 'Carrying amount less depreciation', 'Market value only'], 0,
          'Under AS 28, recoverable amount is whichever is greater — what the asset would sell for net of costs, or its value in use — because a rational owner would choose the better of selling or using. In practice: compute the easier one first.', 'c2', T2),
        Q('m2', 'Which is an external indication of impairment?', ['Carrying amount of net assets exceeds market capitalisation', 'Physical damage to the asset', 'A plan to restructure the division', 'Internal reports of worse performance'], 0,
          'Net assets above market capitalisation is an external sign; damage, restructuring plans and poor internal performance are internal signs. Both kinds trigger an estimate of recoverable amount. In practice: list signs every year end.', 'c1', T1),
        Q('m3', 'Cash flows used for value in use should:', ['Exclude financing and income tax flows', 'Include interest payments', 'Include planned future improvements not yet committed', 'Be after tax'], 0,
          'Value in use uses pre-tax operating cash flows from the asset in its current condition, discounted at a pre-tax rate. Financing, tax and uncommitted improvements or restructurings are excluded. In practice: avoid double counting interest.', 'c2', T2),
        Q('m4', 'Carrying amount ₹30 lakh; net selling price ₹24 lakh; value in use ₹27 lakh. Impairment loss:', ['₹3 lakh', '₹6 lakh', 'Nil', '₹27 lakh'], 0,
          'Recoverable amount is the higher of ₹24 lakh and ₹27 lakh, i.e. ₹27 lakh. Loss = ₹30 − 27 = ₹3 lakh, charged to profit and loss for an asset carried at cost. In practice: depreciate ₹27 lakh hereafter.', 'c3', T3, 'moderate', check=3),
        Q('m5', 'An impairment loss on a revalued asset is:', ['First set off against its revaluation surplus', 'Always charged to profit and loss', 'Ignored', 'Added to goodwill'], 0,
          'For an asset carried at revalued amount, the impairment loss is treated as a revaluation decrease — first against the surplus for that asset, with any excess in profit and loss. In practice: track surplus asset by asset.', 'c3', T3),
        Q('m6', 'A cash-generating unit is:', ['The smallest identifiable group of assets generating largely independent cash inflows', 'Any department', 'The whole company', 'All assets in one location'], 0,
          'A CGU is the smallest identifiable group of assets whose continuing use produces cash inflows largely independent of those from other assets or groups. It is used when individual recoverable amounts cannot be estimated. In practice: look at independent revenue streams.', 'c4', T4),
        Q('m7', 'An impairment loss of a CGU is allocated first to:', ['Goodwill allocated to the unit', 'Buildings', 'Machinery', 'Current assets'], 0,
          'AS 28 allocates the loss first to reduce goodwill of the unit, and then to other assets pro rata on carrying amounts, subject to floors. In practice: goodwill usually absorbs the first hit.', 'c4', T4),
        Q('m8', 'A reversal of impairment can increase the carrying amount up to:', ['What it would have been, net of depreciation, without the impairment', 'Original cost', 'Current market value', 'Value in use, without limit'], 0,
          'A reversal is capped at the carrying amount that would have existed, after depreciation, had no impairment loss been recognised earlier. Anything more would be a revaluation. In practice: keep a shadow depreciation schedule.', 'c5', T5),
        Q('m9', 'An impairment loss on goodwill can be reversed only if:', ['It was caused by an exceptional external event not expected to recur and later events reversed it', 'Market value rises', 'The company makes profits', 'Management decides'], 0,
          'Goodwill impairment reversals are allowed only where the loss arose from an unusual one-off outside event that is not likely to happen again, and later external events have reversed its effect. In practice: such reversals are rare.', 'c5', T5),
        Q('m10', 'Is an annual estimate of recoverable amount required for every asset?', ['No; only when there is an indication of impairment (with specified exceptions)', 'Yes, every asset every year', 'Only for land', 'Only every five years'], 0,
          'AS 28 requires an assessment of indications at each balance sheet date; recoverable amount is estimated only when an indication exists, except where other standards require annual testing, such as long-lived intangibles. In practice: document the assessment.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Net selling price', 1, 'computation', 'selling', nums=[38]),
           S('s2', 'Value in use', 2, 'computation', 'value in use', nums=[viu]),
           S('s3', 'Recoverable amount and loss', 2, 'computation', 'higher', nums=[rec, loss])],
          ['Compute both measures.'], ['Taking the lower of the two.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Unit loss', 1.5, 'computation', 'unit', nums=[l2]),
           S('s2', 'Goodwill first', 1.5, 'concept', 'goodwill'),
           S('s3', 'Pro rata to others', 2, 'computation', 'pro rata|proportion', nums=[mach, bldg])],
          ['Exhaust goodwill first.'], ['Spreading the loss over goodwill and assets together.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When is an asset impaired?', 'When its carrying amount exceeds its recoverable amount.',
          [P('p1', 'Carrying amount', 5, 'carrying'), P('p2', 'Exceeds recoverable amount', 5, 'recoverable')], 'c1'),
        V('v2', 'What is value in use?', 'The present value of estimated future cash flows while the asset keeps being used, plus what its final sale should bring.',
          [P('p1', 'Present value', 5, 'present value'), P('p2', 'Use and disposal cash flows', 5, 'cash')], 'c2'),
        V('v3', 'How is a CGU\'s impairment loss allocated?', 'First to goodwill of the unit, then to other assets pro rata to carrying amounts, without taking any asset below the highest of net selling price, value in use and zero.',
          [P('p1', 'Goodwill first', 5, 'goodwill'), P('p2', 'Pro rata with floor', 5, 'pro rata|proportion')], 'c4'),
        V('v4', 'What is the limit on reversing an impairment loss?', 'The increased carrying amount cannot exceed what it would have been, net of depreciation, had no impairment been recognised.',
          [P('p1', 'Cap', 6, 'would have been|cannot exceed'), P('p2', 'Net of depreciation', 4, 'depreciation')], 'c5'),
        V('v5', 'Give two internal indications of impairment.', 'Obsolescence or physical damage, plans to discontinue or restructure, and internal reports showing worse economic performance.',
          [P('p1', 'Damage or obsolescence', 5, 'damage|obsolescen'), P('p2', 'Plans or poor performance', 5, 'restructur|discontinu|performance')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Rohini Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Rohini Textiles Ltd. has a weaving unit (a CGU) carrying goodwill ₹5 crore, looms ₹30 crore and shed ₹15 crore. Cheap imports have cut demand. Recoverable amount of the unit is ₹38 crore. The shed alone can be sold for ₹14 crore net.',
              'mcqs': [
                  M('k1a', 'Impairment loss of the unit:', ['₹12 crore', '₹7 crore', '₹5 crore', '₹17 crore'], 0,
                    'Carrying amount of the unit is ₹5 + 30 + 15 = ₹50 crore; recoverable amount ₹38 crore; loss ₹12 crore. In practice: confirm the CGU boundaries first.', 'core', check=12, topic=T4),
                  M('k1b', 'Loss allocated to the shed (before applying its floor):', ['₹2.33 crore', '₹4 crore', '₹1 crore', '₹3.5 crore'], 0,
                    'After writing off goodwill of ₹5 crore, ₹7 crore remains, split 30:15 between looms and shed: shed ₹2.33 crore. In practice: then apply the floor.', 'hard', check=round(7*15/45, 2), topic=T4),
                  M('k1c', 'The shed\'s floor of ₹14 crore means its loss is limited to:', ['₹1 crore, with the rest moved to the looms', '₹2.33 crore', 'Nil', '₹15 crore'], 0,
                    'The shed cannot go below its net selling price of ₹14 crore, so it can absorb only ₹1 crore; the remaining ₹1.33 crore is reallocated to the looms. In practice: re-run the allocation.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 7, 'Accounting Standard 28 Impairment of Assets',
                ['Identify indications of impairment.',
                 'Measure recoverable amount using net selling price and value in use.',
                 'Recognise and allocate impairment losses for assets and CGUs.',
                 'Account for reversals and give disclosures.'],
                {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['int-p1-ch05-u06'],
                 'exam_tip': 'Recoverable amount is the higher of the two measures; allocate CGU losses to goodwill first and respect the floors.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Check indications every balance sheet date.', 'Recoverable = higher of NSP and value in use.',
                             'Loss = carrying − recoverable; P&L or revaluation surplus.', 'CGU: smallest independent cash-generating group; goodwill bottom-up/top-down.',
                             'Allocate: goodwill first, then pro rata with floors.', 'Reversal capped at no-impairment carrying amount; goodwill rarely.'],
                 'remember': ['Value in use uses pre-tax flows and rate.'],
                 'traps': ['Recoverable amount is the higher, not the lower.']},
                [('Recoverable amount', 'Higher of NSP and VIU'), ('CGU loss', 'Goodwill first, then pro rata'), ('Reversal cap', 'No-impairment carrying amount')],
                viva, cases)
