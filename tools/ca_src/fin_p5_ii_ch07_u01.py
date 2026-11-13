"""CA Final · Paper 5 · Part II Customs · Chapter 7 Refund.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch07-u01'
T1 = 'Claiming refund under section 27'
T2 = 'Unjust enrichment and the Consumer Welfare Fund'
T3 = 'Interest on delayed refund'
T4 = 'Refund of export and import duty in special cases'


def build():
    ck = Checks()
    days = ck.add('25+31+15', 'Days from 6 April to 15 June (interest period)')
    intr = ck.add('365000*0.06*71/365', 'Interest at 6% p.a. on delayed refund (₹)')
    i1 = {'id': 'i1', 'title': 'Interest on delayed refund', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Indus Pharma filed a complete refund application on 5 January, acknowledged the same day. Refund of ₹3,65,000 was sanctioned and paid on 15 June. Compute interest under section 27A, treating the three-month window as ending on 5 April.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Interest-free window', '3 months from receipt of application', 'Up to 5 April'],
              ['Interest days', '6 April to 15 June', f'{inr(days)} days'],
              ['Interest', '₹3,65,000 × 6% × 71/365', f'₹{inr(intr)}']], title='Section 27A')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is the refund claim in time?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Determine whether these claims are within time: (a) duty paid on 10 February of year 1, claim filed 20 February of year 2; (b) duty paid under protest in year 1, claim in year 3; (c) provisional assessment finalised on 1 August of year 2, claim filed 15 March of year 3 for duty paid in year 1.',
          'solution': [table(['Case', 'Rule', 'Result'], [
              ['(a)', 'One year from date of payment', 'Time-barred'],
              ['(b)', 'No limitation for duty paid under protest', 'In time'],
              ['(c)', 'One year from adjustment on final assessment', 'In time']], title='Section 27(1)')]}

    concepts = [
        C('c1', T1, [
            'Section 27: a person who paid or bore duty or interest may apply for refund within one year from the date of payment; a buyer who bore the duty counts from the date of purchase. Where duty was paid under protest, no limitation applies. No refund is paid where the amount is below ₹100.',
            'The one-year period runs from special dates in some cases: from the date of the appellate order or judgment where refund follows it, from adjustment of duty after final assessment where duty was provisionally paid, and from payment of duty on a revised entry under section 149 or 46.',
            'The application must be accompanied by documents showing the duty was paid and the incidence was not passed on. Section 27 is a complete code; refund outside it cannot be sought through civil suits.'],
          'One year, unless paid under protest.',
          'Excess duty paid due to a wrong rate can be claimed within twelve months.'),
        C('c2', T2, [
            'Unjust enrichment: a refund should go only to the person who actually bore the duty. Section 28D presumes that every person who paid duty has passed on its incidence to the buyer, unless proved otherwise.',
            'If the applicant cannot rebut the presumption, the refundable amount is credited to the Consumer Welfare Fund. It is paid to the applicant where: the importer or exporter had not passed it on; an individual imported for personal use; the buyer bore it without passing it on; it relates to export duty refunded under section 26; it relates to drawback under sections 74 and 75; it was borne by a notified class; or excess duty was paid before the home-clearance order and is evident from the self-assessed or reassessed bill of entry.',
            'The Supreme Court upheld the doctrine as valid (Mafatlal Industries) and held it applies even to duty paid under protest; an unchanged selling price alone does not prove that the burden was absorbed (Allied Photographics).'],
          'No windfall: refund follows the burden.',
          'An importer who priced duty into its sales gets no refund; the money goes to the Fund.'),
        C('c3', T3, [
            'Section 27A: if refund is not paid within 3 months of receipt of a complete application, interest is payable from the day after those 3 months till the refund date. The rate may be fixed between 5% and 30%; currently 6% per annum.',
            'Where refund arises from an order of the Commissioner (Appeals), Tribunal or court, that order is treated as the refund order and the 3-month clock runs from it.',
            'Excess duty found on final assessment of a provisional assessment must be refunded within 3 months; otherwise interest at the section 27A rate is payable under section 18(4). Deposits like project-import security carry no interest.'],
          'Three months to pay, then six percent.',
          'Refund paid five months after application earns about two months\' interest.'),
        C('c4', T4, [
            'Section 26: export duty is refunded where goods are returned to the exporter otherwise than by resale, re-imported within one year of export, and the claim is made within 6 months of the clearance order on re-import.',
            'Section 26A: import duty is refunded where goods are defective or not to specification, not worked on or used (except to discover the defect), identifiable, no drawback is claimed, and the goods are exported, abandoned to customs, or destroyed or rendered commercially valueless within 30 days of the clearance order (extendable by up to 3 months).',
            'The 26A claim is due within 6 months of the relevant date (e.g. the export order or relinquishment). It is unavailable for perishables, goods whose shelf life expired, notified goods, or goods involved in an offence.'],
          'Special refunds for returned exports and rejected imports.',
          'A defective imported analyser re-exported within 30 days earns a refund of import duty.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Refund documentation', 'role': 'Customs refund executive',
             'situation': 'Excess duty was paid on a shipment due to wrong classification.',
             'steps': ['Check the one-year limit.', 'Gather proof that duty was not passed on.', 'File complete application.', 'Track 3-month window for interest.'],
             'takeaway': 'Without unjust-enrichment proof the refund goes to the Fund.'}]

    mcqs = [
        Q('m1', 'Time limit for a refund claim under section 27 is:', ['One year from the date of payment', 'Six months', 'Two years', 'Three months'], 0,
          'Section 27(1). In practice: special dates.', 'c1', T1),
        Q('m2', 'Limitation does not apply when duty was paid:', ['Under protest', 'By cheque', 'Online', 'In instalments'], 0,
          'Second proviso. In practice: record protest.', 'c1', T1),
        Q('m3', 'Minimum refund amount is:', ['One hundred rupees', 'One thousand rupees', 'Fifty rupees', 'Five hundred rupees'], 0,
          'Third proviso. In practice: small claims dropped.', 'c1', T1),
        Q('m4', 'Section 28D presumes that the duty incidence:', ['Has been passed on to the buyer', 'Was borne by the importer', 'Was refunded', 'Was waived'], 0,
          'Statutory presumption. In practice: rebut with evidence.', 'c2', T2),
        Q('m5', 'Refund not payable to the applicant is credited to:', ['Consumer Welfare Fund', 'Consolidated Fund', 'Contingency Fund', 'PM Relief Fund'], 0,
          'Section 27(2). In practice: unjust enrichment.', 'c2', T2),
        Q('m6', 'Current rate of interest on delayed refund is:', ['Six percent per annum', 'Fifteen percent', 'Nine percent', 'Twelve percent'], 0,
          'Section 27A. In practice: after 3 months.', 'c3', T3),
        Q('m7', 'Under section 26A, defective goods must be exported or destroyed within:', ['Thirty days of the clearance order, extendable', 'One year', 'Six months', 'Ninety days fixed'], 0,
          'Extension up to 3 months. In practice: plan quickly.', 'c4', T4),
        Q('m8', 'Export duty refund under section 26 requires re-import within:', ['One year of export', 'Six months', 'Two years', 'Three years'], 0,
          'Section 26(b). In practice: not by resale.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Interest period', 2, 'computation', '3 months', nums=[days]), S('s2', 'Interest', 2, 'computation', '6%', nums=[intr])],
          ['Show dates.'], ['Counting from sanction date.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Ordinary limitation', 1, 'analysis', 'one year'), S('s2', 'Protest', 1, 'analysis', 'protest'), S('s3', 'Provisional', 2, 'analysis', 'final assessment')],
          ['Cite provisos.'], ['Ignoring protest exception.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Who may claim refund besides the importer?', 'A buyer who bore the duty, within one year from the date of purchase.',
          [P('p1', 'Buyer', 5, 'buyer'), P('p2', 'Purchase', 5, 'purchase')], 'c1'),
        V('v2', 'When is refund of excess duty paid to the importer despite the presumption?', 'When excess payment before the clearance order is evident from the bill of entry.',
          [P('p1', 'Bill of entry', 5, 'bill of entry'), P('p2', 'Evident', 5, 'evident')], 'c2'),
        V('v3', 'From when does interest run on a refund ordered in appeal?', 'Three months after the appellate order, which is treated as the refund order.',
          [P('p1', 'Appellate order', 5, 'appellate order'), P('p2', 'Three months', 5, 'three months')], 'c3'),
        V('v4', 'Can goods used after import get section 26A refund?', 'Only where use was indispensable to discover the defect.',
          [P('p1', 'Indispensable', 5, 'indispensable'), P('p2', 'Discover the defect', 5, 'discover')], 'c4'),
        V('v5', 'Is interest payable on security deposits?', 'Section 27A covers delayed refunds of duty only, so deposits like provisional-release security carry no interest.',
          [P('p1', 'Duty only', 5, 'duty only'), P('p2', 'Deposits', 5, 'deposits')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Rejected export consignment', 'difficulty': 'core',
              'case': 'Yamuna Minerals paid export duty on ore shipped in May of year 1. The buyer rejected it, and the ore was re-imported in March of year 2 (cleared 10 March).',
              'mcqs': [
                  M('k1a', 'Is the re-import within the permitted time?', ['Yes, within one year', 'No', 'Only with extension', 'Only for ore'], 0,
                    'Section 26(b). In practice: count from export.', 'core', topic=T4),
                  M('k1b', 'Refund claim must be filed by:', ['Six months from 10 March', 'One year from export', 'Thirty days', 'Three months'], 0,
                    'Section 26(c). In practice: clearance order date.', 'core', topic=T4),
                  M('k1c', 'Does unjust enrichment block this refund?', ['No, export duty refund under section 26 is excepted', 'Yes', 'Only partly', 'Only if sold'], 0,
                    'Section 27(2) exception. In practice: paid to exporter.', 'core', topic=T2),
                  M('k1d', 'If goods were returned by way of resale, refund is:', ['Not available', 'Available', 'Half', 'Doubled'], 0,
                    'Section 26(a). In practice: genuine return.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch07', 1, 'Refund',
                ['Apply the refund procedure and time limits under section 27.',
                 'Apply the doctrine of unjust enrichment.',
                 'Compute interest on delayed refunds.',
                 'Apply refund of export and import duty in special cases.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ii-ch06-u01'],
                 'exam_tip': 'Check limitation first, then unjust enrichment, then interest.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 27: one year; none if under protest; minimum ₹100.', 'Section 28D presumption; Consumer Welfare Fund.', 'Section 27A: 6% after 3 months.',
                             'Section 26: export duty, re-import within one year, claim in 6 months.', 'Section 26A: defective imports, 30 days + 3 months, claim in 6 months.'],
                 'remember': ['Section 18(4): interest on refund after final assessment.'],
                 'traps': ['Counting interest from sanction instead of application date.']},
                [('Refund', 'Section 27'), ('Interest', 'Section 27A'), ('Presumption', 'Section 28D'), ('Export duty', 'Section 26'), ('Import duty', 'Section 26A')],
                viva, cases)
