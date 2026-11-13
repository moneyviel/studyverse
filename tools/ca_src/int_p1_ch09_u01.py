"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 9 Unit 1 — AS 12 Accounting for Government Grants.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch09-u01'
T1 = 'Meaning of government grants and when to recognise them'
T2 = 'Capital approach and income approach'
T3 = 'Grants related to specific fixed assets'
T4 = 'Revenue grants, promoters\' contribution and non-monetary grants'
T5 = 'Refund of grants and disclosure'


def build():
    ck = Checks()
    a1 = ck.add('5000000-1000000', 'Asset cost net of grant — method 1 (₹)')
    d1 = ck.add('4000000/5', 'Annual depreciation — method 1 (₹)')
    d2 = ck.add('5000000/5', 'Annual depreciation — method 2 (₹)')
    inc = ck.add('1000000/5', 'Deferred grant income released each year — method 2 (₹)')
    net = ck.add('1000000-200000', 'Net annual charge — method 2 (₹)')
    i1 = {'id': 'i1', 'title': 'Two ways to show an asset grant', 'difficulty': 'core', 'minutes': 7,
          'q': 'Prisha Ltd. bought a machine for ₹50,00,000 with a government grant of ₹10,00,000. Life 5 years, no residual value, straight-line. Show both methods allowed by AS 12.',
          'solution': [table(['Method', 'Asset shown at', 'Annual depreciation', 'Grant income', 'Net charge'], [
              ['Deduct grant from cost', inr(a1), inr(d1), '—', inr(d1)],
              ['Deferred income', inr(5000000), inr(d2), inr(inc), inr(net)]], title='AS 12 — depreciable asset grants'),
              note('Both give the same profit effect each year; they differ only in presentation.')],
          'checks': list(ck)}

    ck2 = Checks()
    bv = ck2.add('4000000-800000', 'Book value after 1 year (net method) (₹)')
    rev = ck2.add('3200000+1000000', 'Book value after refund (₹)')
    nd = ck2.add('4200000/4', 'Revised annual depreciation over 4 years (₹)')
    i2 = {'id': 'i2', 'title': 'The grant has to be repaid', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Continuing Prisha Ltd. (net method): after one year the conditions are breached and the whole ₹10,00,000 grant becomes refundable. Show the treatment.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Book value after 1 year', '40,00,000 − 8,00,000', inr(bv)],
              ['Increase by grant refundable', '+ 10,00,000', inr(rev)],
              ['Depreciation for remaining 4 years', '42,00,000 ÷ 4', inr(nd)]], title='Refund of an asset grant'),
              note('Depreciation on the increased book value is provided prospectively over the remaining life; no catch-up is made for the past year.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Government grants are government help, in cash or kind, given because the enterprise has met or will meet stated conditions. Not included is help that cannot be valued and normal transactions with government.',
            'A grant is booked only once it is reasonably assured both that its conditions will be met and that the money (or asset) will actually come. Receipt alone is not proof that conditions have been or will be met.',
            'AS 12 does not deal with tax holidays, investment allowances, or government participation in ownership.'],
          'Book a grant only when you are reasonably sure of keeping and getting it.',
          'A subsidy sanctioned in March but conditional on hiring 100 local workers by June needs reasonable assurance of that hiring.'),
        C('c2', T2, [
            'Under the capital approach, a grant is credited directly to shareholders\' funds; under the income approach, it is taken to income over one or more periods.',
            'AS 12 uses the capital approach for grants in the nature of promoters\' contribution and grants for non-depreciable assets without conditions; it uses the income approach for most other grants, matching them with related costs.'],
          'Owner-like help goes to reserves; cost-related help goes to income as the costs arise.',
          'A grant to set up a unit in a backward area based on total investment is in the nature of promoters\' contribution.'),
        C('c3', T3, [
            'Grants for specific depreciable fixed assets may either be subtracted from the asset\'s gross cost (depreciation then runs on the reduced amount) or as deferred income recognised in profit and loss over the useful life in proportion to depreciation.',
            'If the grant equals the whole cost of the asset, the asset is shown at a nominal value.',
            'Grants for non-depreciable assets (such as land) are credited to capital reserve. If the grant requires certain obligations to be fulfilled, it is credited to income over the periods in which the cost of meeting those obligations is charged.'],
          'An asset grant either shrinks the asset or becomes income in step with depreciation.',
          'Free land granted on condition of building a factory on it is matched with the building\'s depreciation.'),
        C('c4', T4, [
            'Grants in the nature of promoters\' contribution — given with reference to total investment or capital outlay, with no repayment expected — are credited to capital reserve and treated as part of shareholders\' funds.',
            'Revenue grants are recognised in profit and loss on a systematic basis over the periods needed to match them with the costs they compensate; they are shown separately under "other income" or deducted from the related expense.',
            'Grants receivable as compensation for losses or expenses already incurred, or for immediate financial support with no future costs, are recognised in profit and loss of the period they become receivable, as extraordinary items if appropriate.',
            'Non-monetary grants given at a concessional rate are recorded at acquisition cost; those received free are shown at a token (nominal) amount.'],
          'Match revenue grants with the costs they cover; record free assets at a nominal amount.',
          'A wage subsidy for apprentices is credited to profit and loss as the wages are paid.'),
        C('c5', T5, [
            'A refundable revenue grant is applied first against any unamortised deferred credit; any excess is charged to profit and loss immediately.',
            'A refundable grant related to a specific fixed asset increases the book value of the asset or reduces the deferred income or capital reserve by the amount refundable. Where the asset\'s book value is increased, depreciation on the revised amount is provided prospectively over the remaining useful life.',
            'Refunds may be extraordinary items where appropriate. Disclose the accounting policy for grants, including presentation method, and the nature and extent of grants recognised.'],
          'Repaying a grant undoes its earlier treatment, without restating past years.',
          'Repaying a ₹2 lakh revenue grant with ₹50,000 still deferred: ₹50,000 against the deferral, ₹1.5 lakh to profit and loss.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Grant accounting for a new plant', 'role': 'Accounts executive',
             'situation': 'A company has received a capital subsidy based on total project cost, a grant for specific machinery and a power-cost subsidy.',
             'steps': ['Classify each grant by its nature.', 'Credit promoters\'-contribution grants to capital reserve.', 'Choose the presentation for the machinery grant.', 'Match the power subsidy with power costs.'],
             'takeaway': 'The purpose of the grant decides its accounting.'}]

    mcqs = [
        Q('m1', 'Government grants are recognised when there is:', ['Reasonable assurance of complying with conditions and of receiving the grant', 'A sanction letter only', 'Cash received', 'A board resolution'], 0,
          'AS 12 needs reasonable assurance on both counts: that conditions will be met and that the grant will be received. Receipt alone does not prove compliance. In practice: review the conditions carefully.', 'c1', T1),
        Q('m2', 'A grant related to a specific depreciable asset may be shown as:', ['Deduction from the asset\'s gross value or deferred income', 'Capital reserve only', 'Revenue on receipt', 'A liability forever'], 0,
          'AS 12 offers two presentations: reduce the asset\'s gross value, or treat the grant as deferred income released in proportion to depreciation. Both give the same profit effect. In practice: apply one consistently.', 'c3', T3),
        Q('m3', 'A grant equal to the entire cost of an asset is shown:', ['By recording the asset at a nominal value', 'At full cost with a liability', 'As revenue', 'Not at all'], 0,
          'When the grant covers the whole cost and is deducted from it, the asset is shown at a nominal value so that it still appears in the books. In practice: ₹1 is common.', 'c3', T3),
        Q('m4', 'A grant in the nature of promoters\' contribution is credited to:', ['Capital reserve', 'Profit and loss', 'Deferred income', 'The asset account'], 0,
          'Grants given with reference to total investment, with no repayment expected, are treated as promoters\' contribution and credited to capital reserve as part of shareholders\' funds. In practice: they are not distributed.', 'c4', T4),
        Q('m5', 'A revenue grant is recognised:', ['In profit and loss, matched with the related costs', 'In capital reserve', 'Only on receipt', 'Against fixed assets'], 0,
          'Revenue grants are taken to profit and loss on a systematic basis over the periods needed to match the costs they compensate, shown separately or deducted from the expense. In practice: accrue with the costs.', 'c4', T4),
        Q('m6', 'Machine cost ₹30 lakh; grant ₹6 lakh; life 6 years; deferred income method. Annual grant income:', ['₹1 lakh', '₹6 lakh', '₹5 lakh', '₹4 lakh'], 0,
          'Under the deferred income method, the ₹6 lakh grant is released in proportion to depreciation over 6 years: ₹1 lakh a year, offsetting depreciation of ₹5 lakh. In practice: show it as other income.', 'c3', T3, 'moderate', check=1),
        Q('m7', 'A grant received for land, with no further conditions, is credited to:', ['Capital reserve', 'Profit and loss', 'Deferred income over 10 years', 'The land account at nil'], 0,
          'Grants for non-depreciable assets are credited to capital reserve. Only if conditions require future obligations is the grant spread over the periods bearing those costs. In practice: check for conditions.', 'c3', T3),
        Q('m8', 'A refund of a revenue grant is:', ['Applied first against any unamortised deferred credit, excess to profit and loss', 'Added to fixed assets', 'Debited to capital reserve', 'Ignored'], 0,
          'AS 12 applies a revenue grant refund first to any balance still deferred; the remainder is charged to profit and loss immediately. In practice: it may be an extraordinary item.', 'c5', T5),
        Q('m9', 'Non-monetary assets given free by the government are recorded at:', ['A nominal value', 'Fair value', 'Nil', 'Replacement cost'], 0,
          'AS 12 records non-monetary grants at acquisition cost if concessional, and at a nominal value if received free of cost. Fair value is not used. In practice: disclose the grant.', 'c4', T4),
        Q('m10', 'A grant received as compensation for losses already incurred is recognised:', ['In profit and loss when it becomes receivable', 'Over five years', 'In capital reserve', 'Against the related asset'], 0,
          'Grants compensating past losses or providing immediate support with no future costs are income of the period in which they become receivable, as an extraordinary item if appropriate. In practice: disclose its nature.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Net cost method', 2, 'computation', 'deduct', nums=[a1, d1]),
           S('s2', 'Deferred income method', 2, 'computation', 'deferred', nums=[d2, inc]),
           S('s3', 'Same net charge', 1, 'computation', 'net', nums=[net])],
          ['Show both columns.'], ['Crediting the full grant to income at once.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Book value increased', 2, 'computation', 'book value', nums=[bv, rev]),
           S('s2', 'Prospective depreciation', 2, 'computation', 'prospective|remaining', nums=[nd])],
          ['No catch-up depreciation.'], ['Charging the refund to profit and loss.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When is a government grant recognised?', 'Once it is reasonably assured that its conditions will be met and that the grant will actually be received.',
          [P('p1', 'Reasonable assurance', 5, 'reasonable'), P('p2', 'Conditions and receipt', 5, 'condition|receiv')], 'c1'),
        V('v2', 'What are the two approaches to grants?', 'The capital approach, crediting grants to shareholders\' funds, and the income approach, taking them to income over periods.',
          [P('p1', 'Capital approach', 5, 'capital'), P('p2', 'Income approach', 5, 'income')], 'c2'),
        V('v3', 'How are grants in the nature of promoters\' contribution treated?', 'They are credited to capital reserve and treated as part of shareholders\' funds.',
          [P('p1', 'Capital reserve', 6, 'capital reserve'), P('p2', 'Shareholders\' funds', 4, 'shareholders')], 'c4'),
        V('v4', 'How is a refundable asset-related grant treated?', 'By increasing the asset\'s book value or reducing deferred income or capital reserve; depreciation on a revised book value is provided prospectively.',
          [P('p1', 'Increase book value or reduce deferred income', 6, 'book value|deferred'), P('p2', 'Prospective depreciation', 4, 'prospective')], 'c5'),
        V('v5', 'How are free non-monetary grants recorded?', 'At a nominal value.',
          [P('p1', 'Nominal', 6, 'nominal'), P('p2', 'Value', 4, 'value')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Nirmal Agro Industries Ltd.', 'difficulty': 'moderate',
              'case': 'Nirmal Agro Industries Ltd. received: a ₹50 lakh subsidy at 10% of total project investment for setting up in a notified area; ₹12 lakh towards a cold-storage plant (life 6 years); and ₹3 lakh to reimburse electricity costs of the current year.',
              'mcqs': [
                  M('k1a', 'The ₹50 lakh project subsidy is credited to:', ['Capital reserve', 'Profit and loss', 'Cold-storage plant', 'Deferred income'], 0,
                    'A subsidy based on total project investment is in the nature of promoters\' contribution, so it goes to capital reserve under the capital approach. In practice: it is not distributable.', 'core', topic=T4),
                  M('k1b', 'Annual income from the cold-storage grant under the deferred income method:', ['₹2 lakh', '₹12 lakh', '₹1 lakh', '₹6 lakh'], 0,
                    'The ₹12 lakh grant is released over the plant\'s 6-year life in step with depreciation: ₹2 lakh a year. In practice: alternatively reduce the plant cost.', 'moderate', check=2, topic=T3),
                  M('k1c', 'The ₹3 lakh electricity grant is:', ['Recognised in profit and loss this year', 'Credited to capital reserve', 'Deducted from the plant', 'Deferred over 6 years'], 0,
                    'It is a revenue grant matching current-year electricity costs, so it is recognised in profit and loss this year, shown as other income or deducted from power cost. In practice: disclose it.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch09', 1, 'Accounting Standard 12 Accounting for Government Grants',
                ['Define government grants and apply the recognition test.',
                 'Distinguish the capital and income approaches.',
                 'Account for grants related to assets, revenue, promoters\' contribution and non-monetary grants.',
                 'Account for refunds and give disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p1-ch08-u02'],
                 'exam_tip': 'First identify the purpose of each grant — asset, revenue, promoters\' contribution or compensation — then apply its treatment.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Recognise with reasonable assurance of conditions and receipt.', 'Asset grants: deduct from cost or deferred income.',
                             'Non-depreciable asset grants: capital reserve (unless conditional).', 'Promoters\' contribution: capital reserve.',
                             'Revenue grants: matched with costs; past losses: income when receivable.', 'Refunds: reverse earlier treatment; prospective depreciation.'],
                 'remember': ['Free assets at nominal value.'],
                 'traps': ['Receipt alone does not prove compliance.']},
                [('Asset grant', 'Deduct or defer'), ('Promoters\' contribution', 'Capital reserve'), ('Free asset', 'Nominal value')],
                viva, cases)
