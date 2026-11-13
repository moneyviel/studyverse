"""CA Final · Paper 4 · Chapter 17 Dispute Resolution.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch17-u01'
T1 = 'Constitution and purpose of the DRC'
T2 = 'Specified order and specified person'
T3 = 'Procedure before the DRC'
T4 = 'Orders of the DRC and their effect'


def build():
    ck = Checks()
    v = ck.add('800000', 'Aggregate variation in Mira\'s order (₹)')
    r = ck.add('4200000', 'Returned income of Mira (₹)')
    i1 = {'id': 'i1', 'title': 'Is the order a specified order?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Test DRC eligibility: (a) Mira returned income of ₹42,00,000; the assessment adds ₹8,00,000, not based on any search, survey or treaty information. (b) Anand returned ₹55,00,000 with an addition of ₹3,00,000. (c) Bela returned ₹20,00,000; an addition of ₹6,00,000 arises from survey findings.',
          'solution': [table(['Case', 'Tests', 'Eligible?'], [
              ['(a) Mira', f'Variation ₹{inr(v)} ≤ ₹10 lakh; returned ₹{inr(r)} ≤ ₹50 lakh; no search/survey', 'Yes'],
              ['(b) Anand', 'Returned income exceeds ₹50 lakh', 'No'],
              ['(c) Bela', 'Order based on survey', 'No']], title='Section 379(4)')],
          'checks': list(ck)}

    c2 = Checks()
    m = c2.add('6', 'Months available to the DRC after month of admission')
    i2 = {'id': 'i2', 'title': 'DRC timeline', 'difficulty': 'core', 'minutes': 5,
          'q': 'Mira receives the specified order on 20 January 2027 and has not appealed. Her application is admitted on 10 March 2027. Outline the key dates.',
          'solution': [table(['Step', 'Rule', 'Date'], [
              ['Application', 'Within one month of receipt of order', '20 February 2027'],
              ['Proof of withdrawal of any appeal', 'Within 30 days of admission communication', 'About 9 April 2027'],
              ['DRC order', f'Within {m} months from end of month of admission', '30 September 2027'],
              ['AO\'s modified order', 'Within one month from end of month of receipt of DRC order', '—']], title='Section 379 and e-DRS 2022')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 379 provides Dispute Resolution Committees (DRCs) to resolve disputes of small and medium taxpayers quickly and reduce litigation. The CBDT constitutes DRCs under rules, and the e-Dispute Resolution Scheme, 2022 makes the process faceless.',
            'Each DRC has three members: two retired Indian Revenue Service officers and one serving officer of the rank of Principal Commissioner or Commissioner, for the PCCIT region. Retired members serve fixed terms; decisions are by majority.',
            'The DRC can reduce or waive penalty and grant immunity from prosecution for offences under the Act, subject to conditions under Rule 198.'],
          'A small panel replaces a long appeal for modest disputes.',
          'A shop owner with a ₹6 lakh addition can seek DRC resolution instead of a first appeal.'),
        C('c2', T2, [
            'Specified order (section 379(4)): a draft order, intimation, assessment or reassessment order, rectification order or TDS default order where the aggregate variation does not exceed ₹10 lakh, the returned income (if a return was filed) does not exceed ₹50 lakh, and the order is not based on a search, requisition, survey or treaty information exchange.',
            'Specified person: one not subject to detention under COFEPOSA, not prosecuted under laws such as the IPC/BNS for tax-related offences, UAPA, NDPS, the Benami Act, the Black Money Act or PMLA, and not convicted in income-tax prosecutions.',
            'Both conditions — specified order and specified person — must be satisfied for an application to be valid.'],
          'Small variation, modest income, no search or survey, clean record.',
          'An addition based on survey findings cannot go to the DRC.'),
        C('c3', T3, [
            'The application is filed electronically with a fee of ₹1,000 and proof of tax paid on returned income, within one month of receipt of the specified order (or within the time specified by the Board where an appeal is already pending before the CIT(A)).',
            'The DRC may reject an ineligible application after a show-cause notice; the time taken for admission is excluded in computing the time to appeal. If admitted, the assessee must furnish proof of withdrawal of any appeal or DRP objection within 30 days.',
            'The DRC may call for records, seek reports and hear the assessee; communications are electronic and the assessee responds within specified times.'],
          'Apply within a month, pay ₹1,000, withdraw other proceedings once admitted.',
          'An application against an order received on 20 January 2027 is due by 20 February 2027.'),
        C('c4', T4, [
            'The DRC must pass its order within six months after the close of the month in which the application is admitted. It may modify the variations, decline to modify, and in either case reduce or waive penalty and grant immunity from prosecution, or simply dispose of the application.',
            'The AO gives effect to the DRC order by passing a modified order within one month after the close of the month in which it is received, with a notice of demand.',
            'No appeal or revision lies against the modified order, and an eligible assessee cannot then go to the DRP or first appellate authority against it.'],
          'The DRC\'s outcome is final for that order.',
          'Once a modified order is passed, the matter cannot be taken to the CIT(A).'),
    ]

    jobs = [{'id': 'j1', 'title': 'Choosing DRC or appeal', 'role': 'Tax consultant',
             'situation': 'A client with a ₹7 lakh addition asks whether to appeal or use the DRC.',
             'steps': ['Test specified order and person conditions.', 'Weigh finality against appeal rights.', 'File within one month with fee.', 'Withdraw any appeal after admission.'],
             'takeaway': 'DRC trades appeal rights for speed and penalty relief.'}]

    mcqs = [
        Q('m1', 'A DRC consists of:', ['Three members', 'Five members', 'Two members', 'One member'], 0,
          'Two retired IRS and one serving officer. In practice: majority decision.', 'c1', T1),
        Q('m2', 'Aggregate variation in a specified order must not exceed:', ['Ten lakh rupees', 'Fifty lakh rupees', 'Five lakh rupees', 'One crore rupees'], 0,
          'Section 379(4). In practice: returned income cap too.', 'c2', T2),
        Q('m3', 'Returned income for DRC eligibility must not exceed:', ['Fifty lakh rupees', 'Ten lakh rupees', 'One crore rupees', 'Twenty lakh rupees'], 0,
          'Section 379(4). In practice: where return filed.', 'c2', T2),
        Q('m4', 'An order based on which of these is excluded from DRC?', ['A survey', 'A routine scrutiny', 'Processing of return', 'Rectification'], 0,
          'Search, survey and treaty information excluded. In practice: check basis.', 'c2', T2),
        Q('m5', 'Fee for a DRC application is:', ['One thousand rupees', 'Five hundred rupees', 'Ten thousand rupees', 'Nil'], 0,
          'e-DRS 2022. In practice: with proof of tax paid.', 'c3', T3),
        Q('m6', 'Proof of withdrawal of appeal must be filed within how long of admission?', ['Thirty days', 'Sixty days', 'Fifteen days', 'Six months'], 0,
          'Procedure. In practice: else rejection.', 'c3', T3),
        Q('m7', 'The DRC must pass its order within:', ['Six months from end of month of admission', 'One year', 'Three months', 'Thirty days'], 0,
          'Time limit. In practice: electronic.', 'c4', T4),
        Q('m8', 'Against the AO\'s modified order after DRC:', ['No appeal or revision lies', 'Appeal lies to CIT(A)', 'Appeal lies to ITAT', 'Revision under section 378 lies'], 0,
          'Finality. In practice: choose carefully.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Thresholds', 3, 'analysis', '10 lakh', nums=[v, r]), S('s2', 'Exclusions', 2, 'analysis', 'survey')],
          ['Check each test.'], ['Ignoring the returned income cap.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Application and withdrawal', 2, 'analysis', 'one month'), S('s2', 'DRC and AO orders', 2, 'analysis', 'six months', nums=[m])],
          ['Use end-of-month rules.'], ['Counting six months from date of application.'], ['Timeline.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What relief can the DRC grant besides modifying variations?', 'It can reduce or waive penalty and grant immunity from prosecution under Rule 198.',
          [P('p1', 'Penalty', 5, 'penalty'), P('p2', 'Immunity', 5, 'immunity')], 'c1'),
        V('v2', 'Who is a specified person for DRC?', 'A person free from specified detention orders, prosecutions under listed laws and income-tax convictions.',
          [P('p1', 'Detention', 5, 'detention'), P('p2', 'Prosecution', 5, 'prosecution')], 'c2'),
        V('v3', 'What happens if an application is found ineligible?', 'It is rejected after a show-cause notice, and the time taken is excluded for filing an appeal.',
          [P('p1', 'Rejected', 5, 'reject'), P('p2', 'Excluded time', 5, 'excluded')], 'c3'),
        V('v4', 'Within what time does the AO give effect to a DRC order?', 'Within one month after the close of the month in which the order is received.',
          [P('p1', 'One month', 5, 'one month'), P('p2', 'Close of month', 5, 'close of the month')], 'c4'),
        V('v5', 'Can an eligible assessee approach the DRP after a DRC-modified draft order?', 'The DRP route closes; the modified order stands and only payment of the demand follows.',
          [P('p1', 'DRP closes', 5, 'drp'), P('p2', 'Modified order stands', 5, 'stands')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Tejas Traders', 'difficulty': 'core',
              'case': 'Tejas Traders returned income of ₹38,00,000 for T.Y. 2026-27. Scrutiny resulted in additions of ₹5,00,000 and ₹4,00,000 under two heads, with penalty proceedings initiated. No search or survey was involved.',
              'mcqs': [
                  M('k1a', 'Aggregate variation (₹):', ['9,00,000', '5,00,000', '4,00,000', '1,00,000'], 0,
                    '5,00,000 + 4,00,000. In practice: within ₹10 lakh.', 'core', check=900000, topic=T2),
                  M('k1b', 'Is the order a specified order?', ['Yes', 'No, variation too high', 'No, returned income too high', 'Only partly'], 0,
                    'Both thresholds met. In practice: check person conditions.', 'core', topic=T2),
                  M('k1c', 'Fee payable for the DRC application (₹):', ['1,000', '500', '250', '10,000'], 0,
                    'e-DRS. In practice: online.', 'core', check=1000, topic=T3),
                  M('k1d', 'Can the DRC waive the penalty?', ['Yes, subject to Rule 198', 'No', 'Only the CIT(A) can', 'Only the court can'], 0,
                    'Penalty relief. In practice: conditions apply.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch17', 1, 'Dispute Resolution',
                ['Explain the constitution and purpose of the DRC.',
                 'Test whether an order and a person qualify.',
                 'Apply the DRC application procedure and timelines.',
                 'Explain DRC orders and their finality.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['fin-p4-ch16-u01'],
                 'exam_tip': 'Check the ₹10 lakh and ₹50 lakh limits and the search/survey exclusion before anything else.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 379 DRC; three members.', 'Specified order: variation ≤ ₹10 lakh, returned income ≤ ₹50 lakh, no search/survey.', 'Application within one month; fee ₹1,000.',
                             'Order within six months; AO gives effect in one month.', 'No appeal against modified order.'],
                 'remember': ['DRC can waive penalty and grant immunity.'],
                 'traps': ['Assuming appeal is still available after DRC.']},
                [('DRC', 'Section 379'), ('Specified order', 'Section 379(4)'), ('Procedure', 'e-DRS 2022')],
                viva, cases)
