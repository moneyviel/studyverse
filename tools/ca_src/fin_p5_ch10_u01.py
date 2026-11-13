"""CA Final · Paper 5 · Chapter 10 Accounts and Records; E-way Bill.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch10-u01'
T1 = 'Accounts and records'
T2 = 'When an e-way bill is required'
T3 = 'Generation, Part A and Part B'
T4 = 'Validity, cancellation and acceptance'


def build():
    ck = Checks()
    d1 = ck.add('-(-650//200)', 'Validity for 650 km normal cargo (days)')
    d2 = ck.add('-(-45//20)', 'Validity for 45 km over-dimensional cargo (days)')
    i1 = {'id': 'i1', 'title': 'Validity of e-way bills', 'difficulty': 'core', 'minutes': 6,
          'q': 'Compute e-way bill validity for: (a) normal goods moved 650 km by road; (b) an over-dimensional machine moved 45 km.',
          'solution': [table(['Case', 'Rule', 'Days'], [
              ['(a) Normal cargo', 'One day up to 200 km and one more day per 200 km or part', inr(d1)],
              ['(b) Over-dimensional cargo', 'One day up to 20 km and one more day per 20 km or part', inr(d2)]], title='Rule 138(10)')],
          'checks': list(ck)}

    c2 = Checks()
    v = c2.add('30000+25000', 'Value of two invoices moved together by the transporter (₹)')
    i2 = {'id': 'i2', 'title': 'Is an e-way bill needed?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Examine: (a) a registered dealer sends goods worth ₹45,000 by road to a customer; (b) a transporter carries two consignments of ₹30,000 and ₹25,000 for different consignors in one truck; (c) a manufacturer sends inputs worth ₹70,000 to a job worker in another State; (d) a supplier moves goods worth ₹80,000 by a non-motorised conveyance.',
          'solution': [table(['Case', 'Treatment'], [
              ['(a)', 'Value ≤ ₹50,000 — not required'],
              ['(b)', f'Each invoice ≤ ₹50,000 — not required for consignors; transporter generally needs EWB when total ₹{inr(v)} exceeds ₹50,000 unless exempt'],
              ['(c)', 'Inter-State job work — required irrespective of value'],
              ['(d)', 'Non-motorised conveyance — exempt']], title='Rule 138')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 35 requires every registered person to keep at its principal place of business true and correct accounts of production, inward and outward supplies, stock, ITC, output tax and prescribed records; electronic records are allowed with audit trail. Additional places of business must keep relevant records too.',
            'Rule 56 prescribes registers, including separate accounts for advances, stock (with goods lost, stolen or gifted) and details of suppliers and recipients; entries must not be erased or overwritten, and corrections must be traceable.',
            'Section 36 requires records to be retained for 72 months from the due date of the annual return for that year; where proceedings are pending, until one year after their final disposal or 72 months, whichever later. Unaccounted goods found at the place of business are deemed supplied.'],
          'Keep complete records for six years after the annual return.',
          'Records for 2026-27 must be kept until December 2033.'),
        C('c2', T2, [
            'Rule 138: an e-way bill is needed when goods of consignment value above ₹50,000 move by a conveyance, in relation to a supply, for reasons other than supply (e.g. stock transfer), or on inward supply from an unregistered person.',
            'It is needed irrespective of value for inter-State movement to a job worker by a principal or registered job worker, and for inter-State movement of handicraft goods by persons exempt from registration.',
            'Exemptions include non-motorised conveyance, goods from port or airport to ICD or customs station for clearance, goods specified in the annexure (e.g. LPG to households, fresh produce, currency), transit to or from Nepal and Bhutan, movement under customs seal, empty cargo containers, and movement within notified distances in some cases.'],
          'Value above ₹50,000 by conveyance triggers an e-way bill.',
          'Inputs sent to an out-of-State job worker need an e-way bill even for ₹10,000.'),
        C('c3', T3, [
            'Part A (supplier, recipient, place of delivery, document, value, HSN, reason) is filled by the registered consignor, consignee or an authorised transporter; Part B (vehicle number or transport document) is completed before movement. Part B is not needed where goods move up to 50 km within the State between the business place and a transporter\'s place.',
            'Where goods are handed to a transporter, the transporter may generate the EWB on authorisation; ECOs and courier agencies can also furnish Part A. Unregistered transporters enrol to get a TRANSIN.',
            'A transporter carrying multiple consignments may generate a consolidated e-way bill; vehicle changes in transit are updated in Part B.'],
          'Part A is about the goods; Part B is about the vehicle.',
          'Goods taken 30 km within the State to a transporter\'s godown need no Part B for that leg.'),
        C('c4', T4, [
            'Validity: one day up to 200 km and one extra day per 200 km or part (for over-dimensional cargo and multimodal shipments involving ships: one day per 20 km); counted to midnight of the day following generation. Validity may be extended within eight hours before or after expiry if goods cannot reach in time.',
            'An e-way bill may be cancelled within 24 hours of generation if goods are not moved, but not once verified in transit. The recipient may accept or reject it within 72 hours of details being made available (or before delivery, if earlier); otherwise it is deemed accepted.',
            'Rule 138B and 138C empower officers to intercept and verify; a summary report is recorded within 24 hours and a final report within three days. Detention and penalty under section 129 can follow for movement without valid documents.'],
          'Validity is distance-based; cancellation must be within 24 hours.',
          'A 650 km road journey gets four days of validity.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Logistics compliance', 'role': 'Supply chain tax analyst',
             'situation': 'A distributor ships goods daily across States.',
             'steps': ['Identify consignments needing EWB.', 'Plan Part B updates for transhipment.', 'Monitor validity and extensions.', 'Cancel unused EWBs within 24 hours.'],
             'takeaway': 'Missing or expired EWBs lead to detention.'}]

    mcqs = [
        Q('m1', 'Records must be retained until expiry of how long from the annual return due date?', ['Seventy-two months', 'Thirty-six months', 'Sixty months', 'Ninety-six months'], 0,
          'Section 36. In practice: longer if proceedings pending.', 'c1', T1),
        Q('m2', 'E-way bill is generally required when consignment value exceeds:', ['Fifty thousand rupees', 'One lakh rupees', 'Twenty-five thousand rupees', 'Ten thousand rupees'], 0,
          'Rule 138. In practice: per invoice.', 'c2', T2),
        Q('m3', 'Inter-State movement to a job worker needs an e-way bill:', ['Irrespective of value', 'Only above ₹50,000', 'Only above ₹1 lakh', 'Never'], 0,
          'Proviso to rule 138(1). In practice: principal generates.', 'c2', T2),
        Q('m4', 'Part B is not needed for movement within the State up to:', ['Fifty km to or from a transporter', 'Ten km', 'One hundred km', 'Two hundred km'], 0,
          'Rule 138(3). In practice: Part A still needed.', 'c3', T3),
        Q('m5', 'Validity for normal cargo up to 200 km is:', ['One day', 'Two days', 'Three days', 'Twelve hours'], 0,
          'Rule 138(10). In practice: per 200 km extra day.', 'c4', T4),
        Q('m6', 'An e-way bill can be cancelled within:', ['Twenty-four hours of generation', 'Seventy-two hours', 'Eight hours', 'Seven days'], 0,
          'Rule 138(9). In practice: not after verification.', 'c4', T4),
        Q('m7', 'Recipient\'s silence beyond 72 hours means the e-way bill is:', ['Deemed accepted', 'Deemed rejected', 'Cancelled', 'Extended'], 0,
          'Rule 138(12). In practice: or before delivery.', 'c4', T4),
        Q('m8', 'Which movement is exempt from e-way bill?', ['By non-motorised conveyance', 'Stock transfer by truck above ₹50,000', 'Sale above ₹1 lakh', 'Inter-State job work'], 0,
          'Rule 138(14). In practice: check annexure.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Normal cargo', 2, 'computation', '200 km', nums=[d1]), S('s2', 'ODC', 2, 'computation', '20 km', nums=[d2])],
          ['Round up parts.'], ['Using 100 km slabs.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Value-based cases', 3, 'analysis', '50,000', nums=[v]), S('s2', 'Special cases', 2, 'analysis', 'job work')],
          ['Cite rule 138.'], ['Requiring EWB for non-motorised movement.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What happens to goods found unaccounted at the place of business?', 'They are deemed supplied and tax is determined as for supplies.',
          [P('p1', 'Deemed supplied', 5, 'deemed supplied'), P('p2', 'Tax determined', 5, 'determined')], 'c1'),
        V('v2', 'What is a consolidated e-way bill?', 'A single bill generated by a transporter for multiple consignments in one conveyance, using individual EWB numbers.',
          [P('p1', 'Transporter', 5, 'transporter'), P('p2', 'Multiple consignments', 5, 'multiple')], 'c3'),
        V('v3', 'When can validity be extended?', 'Within eight hours before or after expiry when goods cannot reach in time due to exceptional circumstances.',
          [P('p1', 'Eight hours', 5, 'eight hours'), P('p2', 'Exceptional', 5, 'exceptional')], 'c4'),
        V('v4', 'Who fills Part B?', 'The person causing movement or the transporter, with vehicle or transport document details.',
          [P('p1', 'Transporter', 5, 'transporter'), P('p2', 'Vehicle', 5, 'vehicle')], 'c3'),
        V('v5', 'Can corrections in accounts overwrite earlier entries?', 'Corrections are made by fresh, attested entries so that the original entry stays visible and traceable.',
          [P('p1', 'Fresh entries', 5, 'fresh'), P('p2', 'Traceable', 5, 'traceable')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Delhi to Kolkata dispatch', 'difficulty': 'core',
              'case': 'Arora Traders sends goods worth ₹4,00,000 from Delhi to Kolkata, a distance of 1,500 km, generating the e-way bill at 10:00 a.m. on 1 December 2026.',
              'mcqs': [
                  M('k1a', 'Validity in days:', ['8', '7', '15', '5'], 0,
                    '1,500 ÷ 200 = 7.5 → 8. In practice: part counts.', 'core', check=8, topic=T4),
                  M('k1b', 'Validity ends at midnight of:', ['9 December 2026', '8 December 2026', '10 December 2026', '7 December 2026'], 0,
                    'Day 1 ends midnight of 2 Dec; day 8 ends midnight of 9 Dec. In practice: plan route.', 'core', topic=T4),
                  M('k1c', 'If the order is cancelled before dispatch, Arora can cancel the EWB within (hours):', ['24', '72', '8', '48'], 0,
                    'Rule 138(9). In practice: portal.', 'core', check=24, topic=T4),
                  M('k1d', 'Is an e-way bill required here?', ['Yes, value exceeds ₹50,000', 'No', 'Only inside Delhi', 'Only for rail'], 0,
                    'Rule 138(1). In practice: Part A and Part B.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch10', 1, 'Accounts and Records; E-way Bill',
                ['Apply provisions on accounts and records.',
                 'Determine when an e-way bill is required.',
                 'Apply generation rules for Part A and Part B.',
                 'Compute validity and apply cancellation and acceptance rules.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ch09-u01'],
                 'exam_tip': 'For validity, divide distance by 200 (or 20 for ODC) and round up.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 35 accounts; section 36 retention 72 months.', 'Rule 138: ₹50,000; job work and handicrafts irrespective of value.', 'Part A/Part B; 50 km exception.',
                             'Validity 200 km/day; ODC 20 km/day.', 'Cancel within 24 hours; accept within 72 hours.'],
                 'remember': ['Verified EWBs cannot be cancelled.'],
                 'traps': ['Forgetting the job work exception.']},
                [('Accounts', 'Section 35'), ('Retention', 'Section 36'), ('E-way bill', 'Rule 138')],
                viva, cases)
