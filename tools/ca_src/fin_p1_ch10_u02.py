"""CA Final · Paper 1 Financial Reporting · Chapter 10 Unit 2 Ind AS 20 Accounting for Government Grants and Disclosure of Government Assistance.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch10-u02'
T1 = 'Grants, assistance and recognition conditions'
T2 = 'Income approach and matching'
T3 = 'Presenting asset and income grants'
T4 = 'Below-market loans, non-monetary grants and repayment'


def build():
    ck = Checks()
    di = ck.add('30/5', 'Annual grant income — deferred income method (₹ lakh)')
    dep = ck.add('(100-30)/5', 'Annual depreciation — deduction method (₹ lakh)')
    rep_cv = ck.add('100-30-(100-30)/5*2', 'Carrying amount after 2 years, deduction method (₹ lakh)')
    rep = ck.add('100/5*2-(100-30)/5*2', 'Cumulative extra depreciation charged on repayment (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A capital subsidy on a machine', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Sunrise Agro buys a machine for ₹100 lakh (life 5 years, nil residual) and receives a grant of ₹30 lakh. (a) Show annual amounts under the deferred income and the deduction-from-asset presentations. (b) Under the deduction method, the grant becomes repayable at the end of year 2. What extra depreciation is recognised immediately?',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Deferred income: depreciation', '100 ÷ 5', inr(20)],
              ['Deferred income: grant income per year', '30 ÷ 5', inr(di)],
              ['Deduction method: depreciation', '70 ÷ 5', inr(dep)],
              ['Carrying amount after 2 years (deduction)', '70 − 28', inr(rep_cv)],
              ['Repayment: add 30 back to asset', '42 + 30 = 72', inr(72)],
              ['Extra depreciation charged now', 'Would-have-been 40 − charged 28; asset becomes 72 − 12 = 60', inr(rep)]], title='Ind AS 20')],
          'checks': list(ck)}

    ck2 = Checks()
    fv = ck2.add('2*2.4869+100*0.7513', 'Fair value of loan at 10% (₹ lakh)')
    gr = ck2.add('100-(2*2.4869+100*0.7513)', 'Grant element (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'A cheap government loan', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A state agency lends Sunrise Agro ₹100 lakh for 3 years at 2% (interest paid yearly) to fund a research project. Market rate is 10% (3-year annuity factor 2.4869; discount factor for year 3 0.7513). Compute the loan\'s initial carrying amount and the grant.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Fair value of loan (Ind AS 109)', '2 × 2.4869 + 100 × 0.7513', inr(fv)],
              ['Grant = proceeds − fair value', '100 − 80.10', inr(gr)],
              ['Treatment', 'Deferred income recognised as research costs are incurred', '—']], title='Below-market loan')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Government grants are resources handed over by government to a business because it has met, or will meet, conditions linked to how it operates. Government assistance is wider: action to give an economic benefit to a qualifying entity, including help that cannot reasonably be valued (free technical advice) — only disclosed.',
            'A grant, including a non-monetary grant at fair value, is booked only once it is reasonably assured both that the conditions will be met and that the money (or asset) will actually arrive. Receiving a grant is not itself proof of compliance.',
            'A forgivable loan is treated as a grant when there is reasonable assurance the entity will meet the terms for forgiveness. Grants received as compensation for past losses or immediate financial support with no future costs are recognised in profit or loss when receivable.'],
          'Two assurances — comply and receive — must both exist before recognition.',
          'A subsidy promised for setting up in a backward area is recognised once compliance is reasonably assured.'),
        C('c2', T2, [
            'Ind AS 20 uses the income approach: grants reach profit or loss in a systematic pattern, across the same periods that bear the costs the grant is meant to cover. Crediting grants directly to equity is not allowed.',
            'Grants for depreciable assets are recognised over the periods and in proportion to depreciation. Grants for non-depreciable assets (land) that require fulfilment of obligations are recognised over the periods bearing those costs (e.g. building a factory on it).',
            'A grant may come with a package of conditions; the conditions creating the costs determine the recognition pattern.'],
          'Match the grant with the cost it pays for.',
          'A grant for a 10-year asset is spread over 10 years.'),
        C('c3', T3, [
            'Asset-related grants (non-monetary ones included, at fair value) appear in the balance sheet either as deferred income, or by deducting the grant from the asset\'s carrying amount (reduced depreciation).',
            'Income-related grants appear within profit or loss, either separately or under "other income", or deducted in reporting the related expense.',
            'Cash flow statements show the grant and asset purchase as separate items regardless of balance sheet presentation.'],
          'Two presentation choices each for asset and income grants; both give the same profit.',
          'A wage subsidy may be shown as other income or netted against salaries.'),
        C('c4', T4, [
            'The benefit of a government loan below market rate is treated as a grant: the loan is recognised and measured under Ind AS 109 at fair value, and the difference from proceeds is the grant, accounted for under Ind AS 20.',
            'A non-monetary grant (land, other resources) is measured at fair value.',
            'A grant becoming repayable is a change in estimate. Repayment of an income-related grant is applied first against any unamortised deferred credit, with the excess expensed. For an asset grant, the carrying amount is increased (or deferred income reduced); cumulative extra depreciation that would have been charged without the grant is recognised immediately in profit or loss.'],
          'Cheap loans hide a grant; repayment is a prospective change in estimate.',
          'Land received free from government is booked at fair value with deferred income.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Grant compliance tracker', 'role': 'Plant accountant',
             'situation': 'A new plant received capital subsidy, power subsidy and an interest-free loan.',
             'steps': ['Confirm reasonable assurance for each grant.', 'Choose presentation for the capital subsidy.', 'Measure the loan at fair value.', 'Monitor conditions for repayment risk.'],
             'takeaway': 'Every grant needs a recognition basis and a compliance check.'}]

    mcqs = [
        Q('m1', 'Besides reasonable assurance of meeting the conditions, recognising a grant needs reasonable assurance that:', ['The grant will be received', 'Cash is in the bank', 'The board approves', 'The asset is used'], 0,
          'Both assurances are needed. In practice: receipt alone is not enough.', 'c1', T1),
        Q('m2', 'Crediting a capital grant directly to shareholders\' equity is:', ['Not permitted', 'Required', 'Optional', 'Required for land'], 0,
          'Ind AS 20 follows the income approach. In practice: use deferred income.', 'c2', T2),
        Q('m3', 'A grant for a depreciable asset is recognised in profit or loss:', ['In proportion to depreciation', 'When received', 'In full in year one', 'On disposal'], 0,
          'Matching with related costs. In practice: deferred income released yearly.', 'c2', T2),
        Q('m4', 'The benefit of a below-market government loan is measured as:', ['Proceeds minus fair value under Ind AS 109', 'Interest saved each year', 'Nil', 'Face value'], 0,
          'It is treated as a grant. In practice: use market rate to discount.', 'c4', T4),
        Q('m5', 'Non-monetary grants are measured at:', ['Fair value', 'Nominal value only', 'Zero', 'Cost to government'], 0,
          'Ind AS 20 requires fair value. In practice: land received free.', 'c4', T4),
        Q('m6', 'Repayment of a grant is accounted for as:', ['A change in accounting estimate', 'A prior period error', 'A change in policy', 'An equity adjustment'], 0,
          'Prospective treatment. In practice: catch-up depreciation for asset grants.', 'c4', T4),
        Q('m7', 'Free technical advice from government that cannot be valued is:', ['Disclosed as government assistance', 'Recognised as income', 'Ignored entirely', 'Deferred'], 0,
          'Only disclosure is required. In practice: describe nature and extent.', 'c1', T1),
        Q('m8', 'Grants related to assets may be presented as:', ['Deferred income or a deduction from the asset', 'Equity only', 'Revenue', 'Liabilities only'], 0,
          'Two choices. In practice: cash flows show gross.', 'c3', T3),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Deferred income', 2, 'computation', 'deferred', nums=[di]), S('s2', 'Deduction', 2, 'computation', 'deduction', nums=[dep]), S('s3', 'Repayment', 3, 'computation', 'extra|repay', nums=[rep])],
          ['Show both methods.'], ['Crediting equity.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Fair value', 2.5, 'computation', 'fair value', nums=[fv]), S('s2', 'Grant', 2.5, 'computation', 'grant', nums=[gr])],
          ['Use market rate.'], ['Ignoring the grant element.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the recognition conditions for a grant?', 'Reasonable assurance that the entity will meet the attached conditions and that the grant will be received.',
          [P('p1', 'Comply with conditions', 5, 'condition'), P('p2', 'Will be received', 5, 'received')], 'c1'),
        V('v2', 'Why does Ind AS 20 use the income approach?', 'Because grants come from a source other than shareholders and are earned by meeting obligations, so they should be matched with related costs in profit or loss.',
          [P('p1', 'Not from shareholders', 5, 'shareholder'), P('p2', 'Matched with costs', 5, 'match')], 'c2'),
        V('v3', 'How are grants related to income presented?', 'Either as separate or other income in profit or loss, or deducted from the related expense.',
          [P('p1', 'Other income', 5, 'income'), P('p2', 'Deducted from expense', 5, 'expense')], 'c3'),
        V('v4', 'How is repayment of an asset-related grant treated?', 'The asset is increased or deferred income reduced, and the cumulative additional depreciation is charged to profit or loss immediately.',
          [P('p1', 'Increase asset or reduce deferred income', 5, 'increase|reduce'), P('p2', 'Cumulative depreciation', 5, 'cumulative')], 'c4'),
        V('v5', 'How is a forgivable loan treated?', 'As a grant once there is reasonable assurance the entity will meet the terms for forgiveness.',
          [P('p1', 'Treated as grant', 5, 'grant'), P('p2', 'Terms for forgiveness', 5, 'forgive')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Pharma Ltd.', 'difficulty': 'moderate',
              'case': 'Delta Pharma Ltd. receives: (1) land worth ₹50 lakh free from the state, on condition it builds a plant within 2 years (plant life 20 years); (2) ₹12 lakh to cover salaries of trainees in the current year; (3) ₹8 lakh as compensation for flood losses of the previous year.',
              'mcqs': [
                  M('k1a', 'The land is recognised at (₹ lakh):', ['50', 'Nil', '25', '2.5'], 0,
                    'Non-monetary grants at fair value. In practice: deferred income.', 'core', check=50, topic=T4),
                  M('k1b', 'The land grant is released to profit or loss:', ['Over the life of the plant built on it', 'Immediately', 'Never', 'On sale of land'], 0,
                    'Costs of meeting obligations — plant depreciation — determine the pattern. In practice: 20 years.', 'moderate', topic=T2),
                  M('k1c', 'The trainee salary grant is recognised in:', ['Profit or loss this year', 'Deferred income for 5 years', 'Equity', 'Capital reserve'], 0,
                    'Matched with the salary cost. In practice: show as other income or reduce expense.', 'core', topic=T3),
                  M('k1d', 'Compensation for past flood losses is recognised:', ['In profit or loss when receivable', 'Over 5 years', 'In OCI', 'Against retained earnings'], 0,
                    'No future costs to match. In practice: disclose if material.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch10', 2, 'Ind AS 20 "Accounting for Government Grants and Disclosure of Government Assistance"',
                ['Apply the recognition conditions for government grants.',
                 'Recognise grants in profit or loss using the income approach.',
                 'Present grants related to assets and income.',
                 'Account for below-market loans, non-monetary grants and repayments.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['fin-p1-ch10-u01'],
                 'exam_tip': 'Ask "which cost does this grant pay for?" — that decides when it hits profit.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Recognise when compliance and receipt are reasonably assured.',
                             'Income approach; no direct credit to equity.',
                             'Asset grants: deferred income or deduct from asset.',
                             'Below-market loans: grant = proceeds − fair value.',
                             'Repayment: change in estimate.'],
                 'remember': ['Non-monetary grants at fair value.'],
                 'traps': ['Recognising the grant when cash arrives.']},
                [('Conditions', 'Comply + receive'), ('Approach', 'Income'), ('Asset grants', 'Deferred income or deduction'), ('Cheap loan', 'Proceeds − FV')],
                viva, cases)
