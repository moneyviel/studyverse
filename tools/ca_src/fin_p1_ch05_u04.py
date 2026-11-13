"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 4 Ind AS 36 Impairment of Assets.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u04'
T1 = 'Scope and when to test for impairment'
T2 = 'Recoverable amount: FVLCD versus value in use'
T3 = 'Cash-generating units, goodwill and corporate assets'
T4 = 'Recognising and reversing impairment losses'


def build():
    ck = Checks()
    viu = ck.add('150*(0.909+0.826+0.751)', 'Value in use (₹ lakh)')
    ra = ck.add('max(420, 372.9)', 'Recoverable amount (₹ lakh)')
    loss = ck.add('500-420', 'Impairment loss (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Testing a single machine', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A machine with carrying amount ₹500 lakh shows signs of impairment after a competitor launches better technology. It could be sold for ₹440 lakh with disposal costs of ₹20 lakh. Expected net cash inflows are ₹150 lakh a year for 3 years; pre-tax discount rate 10% (factors 0.909, 0.826, 0.751). Compute the impairment loss.',
          'solution': [table(['Measure', 'Working', '₹ lakh'], [
              ['Fair value less costs of disposal', '440 − 20', inr(420)],
              ['Value in use', '150 × 2.486', str(round(viu, 1))],
              ['Recoverable amount (higher)', '', inr(ra)],
              ['Impairment loss', '500 − 420', inr(loss)]], title='Ind AS 36 test'),
              note('Recoverable amount is the higher of the two measures — the entity would choose the better of selling or using.')],
          'checks': list(ck)}

    ck2 = Checks()
    l = ck2.add('420-300', 'Impairment loss for the CGU (₹ crore)')
    p = ck2.add('60*240/360', 'Loss allocated to plant (₹ crore)')
    o = ck2.add('60*120/360', 'Loss allocated to other assets (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Spreading a CGU loss', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A CGU contains goodwill ₹60 crore, plant ₹240 crore and other non-current assets ₹120 crore. Its recoverable amount is ₹300 crore. No individual asset\'s fair value less costs of disposal is determinable. Allocate the impairment loss.',
          'solution': [table(['Asset', 'Carrying ₹ crore', 'Loss ₹ crore', 'After ₹ crore'], [
              ['Goodwill', '60', '60', '0'],
              ['Plant', '240', inr(p), inr(240 - p)],
              ['Other assets', '120', inr(o), inr(120 - o)],
              ['Total', '420', inr(l), '300']], title='Allocation of impairment loss'),
              note('Goodwill is written off first; the balance is spread pro rata on carrying amounts, but no asset goes below the highest of its FVLCD, value in use and zero.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 36 ensures assets are not carried above their recoverable amount. It applies to most non-financial assets (PPE, intangibles, goodwill, right-of-use assets, investments in subsidiaries, associates and joint ventures in separate statements); not to inventories, contract assets, deferred tax assets, employee benefit assets, financial assets under Ind AS 109, investment property at fair value, biological assets at fair value less costs to sell, or assets held for sale.',
            'At each reporting date the entity assesses indicators. External: significant fall in market value, adverse changes in technology, market, economic or legal environment, rise in market interest rates affecting discount rates, net assets above market capitalisation. Internal: obsolescence or physical damage, adverse changes in how an asset is used (idle, restructuring, disposal plans), and evidence that economic performance is or will be worse than expected.',
            'Regardless of indicators, test annually: goodwill acquired in a business combination, intangible assets with indefinite useful lives, and intangible assets not yet available for use.'],
          'Impairment testing asks whether the books promise more than the asset can deliver.',
          'A sharp rise in interest rates can trigger impairment tests because it lowers present values.'),
        C('c2', T2, [
            'Recoverable amount is the higher of FVLCD (fair value less costs of disposal) and VIU (value in use). If either exceeds carrying amount, no impairment; it is normally worked out asset by asset, moving to a group of assets only when one asset cannot produce cash inflows on its own.',
            'FVLCD: fair value under Ind AS 113 less incremental disposal costs (legal costs, stamp duty, removal costs) — not finance costs or tax.',
            'VIU: present value of future cash flows from continued use and ultimate disposal, based on reasonable and supportable assumptions and most recent approved budgets (normally up to five years, then extrapolated with steady or declining growth). Cash flows are for the asset in its current condition — excluding future restructurings not yet committed, enhancements, financing flows and income taxes. The discount rate is pre-tax and reflects current market time value and asset-specific risks.'],
          'Recoverable amount is the better of selling now or using to the end.',
          'Planned upgrades that would raise output are left out of VIU until the money is spent.'),
        C('c3', T3, [
            'A cash-generating unit (CGU) is the smallest identifiable group of assets generating cash inflows largely independent of other assets. If an active market exists for the output, the unit is a CGU even if the output is used internally.',
            'Goodwill is allocated to the CGUs (or groups) expected to benefit from the combination\'s synergies — no larger than an operating segment. A CGU with goodwill is tested annually and whenever indicators exist; if assets inside are tested at the same time, they are tested first.',
            'Corporate assets (head office, IT centre) do not generate separate inflows; they are allocated to CGUs on a reasonable and consistent basis, or tested at the smallest group of CGUs to which they can be allocated.',
            'Where goodwill relates to a subsidiary with non-controlling interest measured at proportionate share, goodwill is grossed up for the notional NCI share before testing; the loss is then allocated between parent and NCI.'],
          'When assets cannot be tested alone, test the smallest group that earns independent cash.',
          'Each hotel in a chain is usually a separate CGU; the reservation system is a corporate asset.'),
        C('c4', T4, [
            'An impairment loss hits profit or loss at once, except for a revalued asset, in which case it is a revaluation decrease (OCI to the extent of surplus). Depreciation is then based on the revised carrying amount.',
            'For a CGU, the loss first reduces goodwill and then other assets pro rata to carrying amounts — but each asset keeps a floor equal to the highest of its FVLCD, VIU and zero; any unallocated amount goes to other assets.',
            'At each reporting date, indications that a loss may have decreased are assessed. A reversal is recognised if the estimates used have changed; the increased carrying amount cannot exceed what it would have been (net of depreciation) without the impairment. Reversals go to profit or loss (or revaluation surplus for revalued assets). Impairment of goodwill is never reversed.'],
          'Losses go first to goodwill; recoveries never come back to goodwill.',
          'A plant written down two years ago can be written back up, but not beyond its depreciated original cost.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Annual goodwill test', 'role': 'Audit senior',
             'situation': 'A group with three CGUs carries goodwill from a past acquisition.',
             'steps': ['Check goodwill allocation to CGUs.', 'Review budgets, growth and discount rate assumptions.', 'Compare recoverable amount with carrying amount including goodwill.', 'Allocate any loss and check sensitivity disclosures.'],
             'takeaway': 'Assumptions in VIU models drive the answer — challenge them.'}]

    mcqs = [
        Q('m1', 'Recoverable amount is:', ['The higher of FVLCD and VIU', 'The lower of FVLCD and VIU', 'Fair value only', 'Carrying amount'], 0,
          'An entity would pick the better of selling or using. In practice: compute only one if it exceeds carrying amount.', 'c2', T2),
        Q('m2', 'Which asset must be tested annually regardless of indicators?', ['Goodwill', 'Freehold land', 'Machinery', 'Inventory'], 0,
          'Goodwill, indefinite-life intangibles and intangibles not yet available for use. In practice: same date each year allowed.', 'c1', T1),
        Q('m3', 'Value in use cash flows exclude:', ['Income tax and financing flows', 'Cash inflows from continuing use', 'Disposal proceeds at end of life', 'Maintenance costs'], 0,
          'VIU uses pre-tax, pre-financing cash flows. In practice: discount at a pre-tax rate.', 'c2', T2),
        Q('m4', 'Which is outside the scope of Ind AS 36?', ['Inventories', 'Goodwill', 'Right-of-use assets', 'Intangible assets'], 0,
          'Inventories follow Ind AS 2. In practice: deferred tax and financial assets are also excluded.', 'c1', T1),
        Q('m5', 'In a CGU, the impairment loss is first allocated to:', ['Goodwill', 'Plant', 'Inventory', 'Cash'], 0,
          'Goodwill absorbs the loss first, then other assets pro rata. In practice: respect individual floors.', 'c4', T4),
        Q('m6', 'An impairment loss on goodwill:', ['Is never reversed', 'Is reversed if conditions improve', 'Is reversed through OCI', 'Is reversed after 5 years'], 0,
          'Reversal would amount to recognising internally generated goodwill. In practice: other assets can be reversed.', 'c4', T4),
        Q('m7', 'Carrying amount ₹90; FVLCD ₹70; VIU ₹82. Impairment loss:', ['₹8', '₹20', '₹12', 'Nil'], 0,
          'Recoverable amount = 82 (higher); loss = 90 − 82 = 8. In practice: depreciate the revised amount.', 'c2', T2, 'moderate', check=8),
        Q('m8', 'A cash-generating unit is:', ['The smallest group of assets generating largely independent cash inflows', 'The whole company', 'Any group of assets chosen by management', 'Only goodwill'], 0,
          'Identified consistently period to period. In practice: active market for output makes a CGU.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'FVLCD', 1, 'computation', 'disposal'), S('s2', 'VIU', 2, 'computation', 'value in use', nums=[round(viu, 1)]), S('s3', 'Loss', 2, 'computation', 'loss', nums=[loss])],
          ['Take the higher measure.'], ['Taking the lower measure.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Total loss', 1, 'computation', 'loss', nums=[l]), S('s2', 'Goodwill first', 2, 'concept', 'goodwill'), S('s3', 'Pro rata', 3, 'computation', 'pro rata', nums=[p, o])],
          ['Show goodwill then pro rata.'], ['Allocating pro rata including goodwill.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Give two internal indicators of impairment.', 'Physical damage or obsolescence, and evidence that the asset\'s economic performance is worse than expected.',
          [P('p1', 'Damage or obsolescence', 5, 'damage|obsolescen'), P('p2', 'Poor performance', 5, 'performance|worse')], 'c1'),
        V('v2', 'What discount rate is used for value in use?', 'A pre-tax rate built from today\'s market view of the time value of money plus the particular risks of the asset.',
          [P('p1', 'Pre-tax', 5, 'pre-tax'), P('p2', 'Asset-specific risk', 5, 'risk')], 'c2'),
        V('v3', 'How is goodwill allocated for testing?', 'To the cash-generating units expected to benefit from the combination\'s synergies, kept at operating segment level or below.',
          [P('p1', 'CGUs benefiting', 5, 'synerg|benefit'), P('p2', 'Segment limit', 5, 'segment')], 'c3'),
        V('v4', 'What is the floor when allocating a CGU loss to an asset?', 'Each asset\'s floor is the highest of its FVLCD, its value in use and zero.',
          [P('p1', 'Highest of measures', 6, 'highest'), P('p2', 'Zero', 4, 'zero')], 'c4'),
        V('v5', 'What is the limit on reversing an impairment loss?', 'The carrying amount after reversal cannot exceed the depreciated amount that would have existed had no impairment been recognised.',
          [P('p1', 'Depreciated amount', 6, 'depreciat'), P('p2', 'No impairment', 4, 'had no|without')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Bharat Cement Ltd.', 'difficulty': 'hard',
              'case': 'Bharat Cement Ltd. bought a smaller cement company two years ago, recognising goodwill of ₹50 crore allocated to its Western CGU. The Western CGU\'s assets (excluding goodwill) are ₹400 crore. Due to a new competitor, recoverable amount is ₹380 crore. Market capitalisation of the group has fallen below net assets.',
              'mcqs': [
                  M('k1a', 'Market capitalisation below net assets is:', ['An external indicator of impairment', 'Irrelevant', 'An internal indicator only', 'Proof of impairment'], 0,
                    'It suggests the market values the net assets less than book. In practice: test all relevant CGUs.', 'core', topic=T1),
                  M('k1b', 'Impairment loss for the Western CGU (₹ crore):', ['70', '20', '50', '450'], 0,
                    'Carrying amount 450 (400 + 50) − 380 = 70. In practice: goodwill absorbs 50 first.', 'moderate', check=70, topic=T4),
                  M('k1c', 'Loss allocated to other assets after goodwill (₹ crore):', ['20', '70', '50', 'Nil'], 0,
                    '70 − 50 = 20, spread pro rata over the other assets. In practice: respect floors.', 'moderate', check=20, topic=T4),
                  M('k1d', 'If next year the CGU\'s recoverable amount recovers to ₹460 crore:', ['Only the ₹20 crore on other assets may be reversed (within limits); goodwill stays written off', 'All ₹70 crore is reversed', 'Nothing can be reversed', 'Goodwill is reinstated first'], 0,
                    'Goodwill impairment is never reversed; other assets can be, capped at depreciated amounts. In practice: assess estimate changes.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 4, 'Ind AS 36 "Impairment of Assets"',
                ['Identify assets in scope and indicators of impairment.',
                 'Measure recoverable amount using FVLCD and value in use.',
                 'Identify CGUs and allocate goodwill and corporate assets.',
                 'Recognise, allocate and reverse impairment losses.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['fin-p1-ch05-u03'],
                 'exam_tip': 'Write CA, FVLCD, VIU and RA in a line before concluding — it prevents mixing up "higher" and "lower".'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Assess indicators yearly; annual tests for goodwill and certain intangibles.',
                             'RA = higher of FVLCD and VIU.',
                             'VIU: pre-tax, current condition, no financing or tax flows.',
                             'CGU allocation: goodwill first, then pro rata with floors.',
                             'Reversals allowed except goodwill; capped at depreciated amount.'],
                 'remember': ['NCI gross-up for goodwill under proportionate method.'],
                 'traps': ['Inventories and financial assets are outside Ind AS 36.']},
                [('RA', 'Higher of FVLCD and VIU'), ('Annual test', 'Goodwill, indefinite intangibles'), ('CGU loss', 'Goodwill first'), ('Goodwill reversal', 'Never')],
                viva, cases)
