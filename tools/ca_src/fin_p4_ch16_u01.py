"""CA Final · Paper 4 · Chapter 16 Appeals and Revision.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch16-u01'
T1 = 'First appeal before CIT(A) and JCIT(A)'
T2 = 'Appeal to the Appellate Tribunal'
T3 = 'Appeals to High Court and Supreme Court'
T4 = 'Revision by the Commissioner'


def build():
    ck = Checks()
    f1 = ck.add('min(1500000*0.01,10000)', 'ITAT fee where assessed income is ₹15 lakh (₹)')
    f2 = ck.add('1000', 'CIT(A) fee where assessed income exceeds ₹2 lakh (₹)')
    f3 = ck.add('1500', 'ITAT fee where assessed income is ₹1.5 lakh (₹)')
    f4 = ck.add('500', 'CIT(A) fee where assessed income is ₹1.5 lakh (₹)')
    i1 = {'id': 'i1', 'title': 'Appeal fees', 'difficulty': 'core', 'minutes': 5,
          'q': 'Compute the fees payable for (a) an appeal to the Commissioner (Appeals) and (b) an appeal to the Appellate Tribunal where the total income assessed by the AO is (i) ₹15,00,000 and (ii) ₹1,50,000.',
          'solution': [table(['Assessed income', 'CIT(A) fee (₹)', 'ITAT fee (₹)'], [
              ['₹15,00,000', inr(f2), f'{inr(f1)} (1% capped at ₹10,000)'],
              ['₹1,50,000', inr(f4), inr(f3)]], title='Sections 358(2) and 362')],
          'checks': list(ck)}

    c2 = Checks()
    dep = c2.add('4000000*0.20', 'Minimum deposit for stay (₹)')
    i2 = {'id': 'i2', 'title': 'Stay of demand by the Tribunal', 'difficulty': 'core', 'minutes': 4,
          'q': 'Kirti Exports has an outstanding demand of ₹40,00,000 under appeal before the Tribunal. What must it deposit for a stay, and how long can the stay last?',
          'solution': [table(['Item', 'Rule', 'Value'], [
              ['Deposit or security', '20% of tax, interest, fee, penalty or other sum', inr(dep)],
              ['Stay period', 'Up to 180 days; extension only if delay not attributable to assessee', '180 days'],
              ['Duty of Tribunal', 'Dispose of the appeal within the stay period', '—']], title='Section 363(6)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 357 lists appealable orders — assessment and reassessment orders (objecting to income, tax or status), rectification orders, penalty orders, orders treating a person as assessee in default, and others. Appeals against orders of a Deputy Commissioner or lower authority may lie to the Joint Commissioner (Appeals), except where the order was passed by or with approval of a higher authority; the CBDT may transfer appeals between JCIT(A) and CIT(A) (section 356), with a rehearing.',
            'The appeal is filed in the prescribed form within 30 days of service of the order or notice of demand, with a fee of ₹250 (assessed income up to ₹1 lakh), ₹500 (up to ₹2 lakh) or ₹1,000 (above ₹2 lakh). Tax due on the returned income must be paid before filing. Delay can be condoned for sufficient cause.',
            'The appellate authority may confirm, reduce, enhance (after giving a hearing) or annul an assessment, can consider matters not raised, and should decide within one year after the close of the financial year of filing. Faceless appeal schemes may be notified.'],
          'First appeal: 30 days, small fee, wide powers including enhancement.',
          'An appeal against an order dated 10 August 2026 should be filed by 9 September 2026.'),
        C('c2', T2, [
            'The Income-tax Appellate Tribunal (section 361) is the final fact-finding authority. Appeals lie against orders of CIT(A)/JCIT(A), revision orders, penalty orders and others (section 362), within two months after the close of the month in which the order is communicated; the respondent may file cross-objections within 30 days of notice.',
            'Fees: ₹500 (assessed income up to ₹1 lakh), ₹1,500 (up to ₹2 lakh), 1% of assessed income capped at ₹10,000 (above ₹2 lakh), and ₹500 for other matters; no fee for departmental appeals. A single member may hear cases where income assessed does not exceed ₹50 lakh.',
            'The Tribunal should decide within four years after the close of the financial year of filing; it may grant stay for up to 180 days if the assessee deposits at least 20% of the demand or furnishes equivalent security. The CBDT sets monetary limits for departmental appeals (section 373); not appealing one year does not mean acceptance for other years.'],
          'The Tribunal settles facts; stay needs a 20% deposit.',
          'Assessed income of ₹15 lakh means a Tribunal fee of ₹10,000.'),
        C('c3', T3, [
            'Section 365: an appeal lies to the High Court from Tribunal orders only on a substantial question of law, filed within 120 days of receipt of the order (delay condonable). The High Court formulates the question and hears it with a bench of at least two judges.',
            'Section 367: appeals to the Supreme Court lie from High Court judgments in cases it certifies as fit; tax is payable as assessed despite pending references or appeals (section 369), and assessments are amended to give effect to final orders (section 371).',
            'Time taken to obtain a certified copy of the order is excluded in computing limitation (section 372).'],
          'Higher courts deal only with questions of law.',
          'Valuation disputes generally end at the Tribunal unless a legal question arises.'),
        C('c4', T4, [
            'Section 377: the PCIT/CIT may revise an AO\'s or TPO\'s order that is erroneous and prejudicial to revenue, after a hearing. An order is deemed erroneous where it was passed without proper enquiries, allowed relief without enquiring into the claim, was not according to CBDT directions or a binding jurisdictional decision. Revision must be within two years after the close of the financial year in which the order was passed, excluding specified periods.',
            'Section 378: the PCIT/CIT may, on his own or on the assessee\'s application (within one year of communication, with a ₹500 fee), revise other orders, usually in favour of the assessee. It cannot be used where an appeal is pending or the time to appeal has not expired without waiver, or where the order has been subject of appeal.',
            'An order under section 378 must be passed within one year after the close of the financial year in which the application is made; an order prejudicial to the assessee cannot be passed under it.'],
          'Section 377 protects revenue; section 378 offers relief.',
          'An assessment passed without verifying a large deduction can be revised under section 377.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Appeal strategy note', 'role': 'Tax litigation associate',
             'situation': 'A client receives an assessment with large additions.',
             'steps': ['Check limitation for first appeal.', 'Pay tax on returned income.', 'Draft grounds and seek stay if needed.', 'Plan Tribunal and legal questions.'],
             'takeaway': 'Missing a deadline can lose the appeal before it starts.'}]

    mcqs = [
        Q('m1', 'An appeal to the Commissioner (Appeals) must be filed within:', ['Thirty days', 'Sixty days', 'Two months', 'One hundred twenty days'], 0,
          'Section 358. In practice: from service of order.', 'c1', T1),
        Q('m2', 'Fee for a CIT(A) appeal where assessed income exceeds ₹2 lakh is:', ['One thousand rupees', 'Five hundred rupees', 'Two hundred fifty rupees', 'Ten thousand rupees'], 0,
          'Section 358(2). In practice: online payment.', 'c1', T1),
        Q('m3', 'Appeal to the Tribunal is filed within:', ['Two months from end of month of communication', 'Thirty days of order', 'One hundred twenty days', 'Six months'], 0,
          'Section 362. In practice: cross-objections 30 days.', 'c2', T2),
        Q('m4', 'Stay by the Tribunal requires a deposit of at least:', ['Twenty percent of the demand', 'Ten percent', 'Fifty percent', 'Full demand'], 0,
          'Section 363(6). In practice: or equal security.', 'c2', T2),
        Q('m5', 'A single member of the Tribunal can hear cases where assessed income does not exceed:', ['Fifty lakh rupees', 'One crore rupees', 'Ten lakh rupees', 'Five crore rupees'], 0,
          'Section 364. In practice: faster disposal.', 'c2', T2),
        Q('m6', 'An appeal to the High Court lies only on:', ['A substantial question of law', 'Any question of fact', 'Penalty quantum', 'Valuation disputes'], 0,
          'Section 365. In practice: 120 days.', 'c3', T3),
        Q('m7', 'Revision under section 377 must be made within:', ['Two years from end of FY of the order', 'One year', 'Four years', 'Six months'], 0,
          'Time limit. In practice: exclusions apply.', 'c4', T4),
        Q('m8', 'Fee for an assessee\'s revision application under section 378 is:', ['Five hundred rupees', 'One thousand rupees', 'Nil', 'Ten thousand rupees'], 0,
          'Section 378. In practice: within one year.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'CIT(A) fees', 2, 'computation', 'CIT', nums=[f2, f4]), S('s2', 'ITAT fees', 2, 'computation', 'Tribunal', nums=[f1, f3])],
          ['Cite sections.'], ['Ignoring the ₹10,000 cap.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Deposit', 2, 'computation', 'deposit', nums=[dep]), S('s2', 'Stay period', 2, 'analysis', '180 days')],
          ['Mention extension rule.'], ['Assuming indefinite stay.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can the CIT(A) enhance an assessment?', 'Yes, after giving the assessee a reasonable opportunity of showing cause.',
          [P('p1', 'Enhance', 5, 'enhance|yes'), P('p2', 'Opportunity', 5, 'opportunity')], 'c1'),
        V('v2', 'Which orders are not appealable before the JCIT(A)?', 'Orders passed by or with prior approval of an authority above Deputy Commissioner.',
          [P('p1', 'Above Deputy Commissioner', 5, 'above'), P('p2', 'Prior approval', 5, 'approval')], 'c1'),
        V('v3', 'When is an order deemed erroneous for section 377?', 'When the AO made inadequate enquiries, allowed relief without verifying the claim, or acted contrary to CBDT directions or a binding decision.',
          [P('p1', 'Inadequate enquiries', 5, 'inadequate enquiries'), P('p2', 'CBDT directions', 5, 'cbdt|direction')], 'c4'),
        V('v4', 'Does non-filing of a departmental appeal due to monetary limits bind future years?', 'It does not; the department can appeal on the same issue for other years or assessees.',
          [P('p1', 'Other years', 5, 'other years'), P('p2', 'Same issue', 5, 'same issue')], 'c2'),
        V('v5', 'What is excluded in computing limitation for appeals?', 'The time taken to obtain a certified copy of the order.',
          [P('p1', 'Certified copy', 5, 'certified copy'), P('p2', 'Time taken', 5, 'time')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Orchid Builders', 'difficulty': 'core',
              'case': 'Orchid Builders receives an assessment order on 10 August 2026 with additions; total income assessed is ₹2,40,00,000. It plans to appeal and, if needed, go to the Tribunal.',
              'mcqs': [
                  M('k1a', 'Fee for the first appeal (₹):', ['1,000', '250', '500', '10,000'], 0,
                    'Above ₹2 lakh. In practice: CIT(A).', 'core', check=1000, topic=T1),
                  M('k1b', 'Fee for a later Tribunal appeal (₹):', ['10,000', '2,40,000', '1,500', '500'], 0,
                    '1% capped at ₹10,000. In practice: per appeal.', 'core', check=10000, topic=T2),
                  M('k1c', 'Can a single member hear its Tribunal appeal?', ['No, income exceeds fifty lakh rupees', 'Yes', 'Only by consent', 'Only for penalty'], 0,
                    'Threshold ₹50 lakh. In practice: division bench.', 'core', topic=T2),
                  M('k1d', 'Days allowed for the first appeal:', ['30', '60', '45', '120'], 0,
                    'Section 358. In practice: from service.', 'core', check=30, topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch16', 1, 'Appeals and Revision',
                ['Apply provisions for first appeals before CIT(A) and JCIT(A).',
                 'Apply Tribunal appeal, fee and stay provisions.',
                 'Identify appeals to High Court and Supreme Court.',
                 'Apply revision provisions under sections 377 and 378.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p4-ch15-u01'],
                 'exam_tip': 'For each forum state the order appealable, time limit, fee and power.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['CIT(A)/JCIT(A): 30 days; ₹250/₹500/₹1,000.', 'ITAT: two months; ₹500/₹1,500/1% max ₹10,000; stay 180 days with 20%.', 'High Court: substantial question of law; 120 days.',
                             'Section 377: erroneous and prejudicial; 2 years.', 'Section 378: other orders; ₹500 fee; 1 year.'],
                 'remember': ['Single member bench up to ₹50 lakh.'],
                 'traps': ['Taking facts to the High Court.']},
                [('First appeal', 'Sections 356–360'), ('Tribunal', 'Sections 361–364'), ('High Court', 'Section 365'), ('Revision', 'Sections 377–378')],
                viva, cases)
