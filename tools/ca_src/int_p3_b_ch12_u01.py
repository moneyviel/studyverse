"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 12 E-Way Bill.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch12-u01'
T1 = 'When an e-way bill is required (s. 68, Rule 138)'
T2 = 'Who generates it, Parts A and B, and validity'
T3 = 'Exemptions, verification and consequences'


def build():
    ck = Checks()
    v1 = ck.add('-(-450//200)', 'Validity in days for 450 km (normal cargo)')
    v2 = ck.add('-(-70//20)', 'Validity in days for 70 km (over-dimensional cargo)')
    i1 = {'id': 'i1', 'title': 'How long is it valid?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Compute e-way bill validity: (a) normal cargo moving 450 km; (b) over-dimensional cargo moving 70 km. The bill for (a) was generated at 10:00 am on 3 June. When does day one end?',
          'solution': [table(['Case', 'Rule', 'Days'], [
              ['(a) Normal cargo, 450 km', '1 day per 200 km or part', str(int(v1))],
              ['(b) ODC, 70 km', '1 day per 20 km or part', str(int(v2))]], title='Rule 138(10)'),
              note('A "day" ends at midnight of the next day after generation: the first day for (a) expires at midnight of 4 June, so validity of 3 days ends at midnight of 6 June.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Required or not?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Is an e-way bill needed? (a) A Delhi trader sends goods worth ₹45,000 to Noida; (b) a Pune company sends moulds worth ₹20,000 to a job worker in Gujarat; (c) a farmer moves fresh vegetables worth ₹2 lakh to a mandi; (d) goods worth ₹1,20,000 move on a hand cart within the city; (e) goods worth ₹80,000 move 40 km within Maharashtra from the supplier to a transporter\'s godown for onward inter-State dispatch.',
          'solution': [table(['Case', 'Needed?', 'Reason'], [
              ['(a)', 'No', 'Consignment value does not exceed ₹50,000'],
              ['(b)', 'Yes', 'Inter-State movement to a job worker needs an e-way bill whatever the value'],
              ['(c)', 'No', 'Fresh vegetables are listed in the Annexure to Rule 138(14)'],
              ['(d)', 'No', 'Non-motorised conveyance'],
              ['(e)', 'Part A only; Part B not needed for the first leg', 'Movement up to 50 km within the State from consignor to transporter — Part B can be filled before the onward journey']], title='Rule 138')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 68 and Rule 138: an e-way bill is generated before movement of goods of consignment value exceeding ₹50,000 — in relation to a supply, for reasons other than supply (for example, sales returns), or due to inward supply from an unregistered person.',
            'Consignment value is the invoice value including tax, excluding the value of exempt goods supplied on the same invoice.',
            'Even below ₹50,000, it is required for inter-State movement by a principal to a job worker and inter-State movement of handicraft goods by persons exempt from registration.'],
          'The e-way bill is the electronic travel document that tells the tax system what is on the road.',
          'A ₹60,000 invoice with ₹15,000 of exempt goods has a consignment value of ₹45,000 — no e-way bill.'),
        C('c2', T2, [
            'Part A (invoice details, GSTINs, HSN, value) is filled by the registered supplier or recipient who causes the movement; Part B (vehicle or transport document number) by whoever transports. Where the goods are handed to a transporter, he may fill Part B; the registered person may authorise the transporter to fill Part A too.',
            'Validity: 1 day for each 200 km or part for normal cargo; 1 day for each 20 km for over-dimensional cargo. The first day runs till midnight of the following day. Validity can be extended within 8 hours before or after expiry if the goods could not reach in time due to exceptional circumstances.',
            'An e-way bill may be cancelled within 24 hours if not verified in transit; the recipient may accept or reject it within 72 hours or before delivery, failing which it is deemed accepted. Transhipment needs Part B updated for each new vehicle.'],
          'Part A describes the goods; Part B tells where they are travelling and on what.',
          'A truck that breaks down en route has its new vehicle number updated in Part B.'),
        C('c3', T3, [
            'Not required: goods in the Annexure (fresh fruits and vegetables, LPG for households, kerosene through PDS, jewellery and similar items); non-motorised conveyance; movement from port, airport, air cargo complex or land customs station to an inland container depot or container freight station for clearance, or under customs bond or seal; transit to or from Nepal or Bhutan; empty cargo containers; goods treated as no supply under Schedule III; movement of up to 20 km for weighment with a delivery challan; goods moved by defence formations.',
            'Part B is not required where movement within the State is up to 50 km from the consignor\'s place to the transporter\'s place (or from the transporter\'s place to the consignee).',
            'Rule 138B–138D and section 68(3): officers may intercept and verify; findings are uploaded within 24 hours (Part A) and the final report within 3 days. A transporter detained for over 30 minutes may report it on the portal.',
            'Section 129: goods moving without valid documents may be detained or seized; they are released on payment of penalty — for the owner who comes forward, 200% of the tax payable (2% of value or ₹25,000, whichever is lower, for exempt goods); for others, the higher of 50% of the value and 200% of the tax (or 5% of value or ₹25,000 for exempt goods).'],
          'Exemptions cover low-risk goods and movements; missing paperwork on taxable goods is expensive.',
          'Goods worth ₹2 lakh with tax of ₹36,000 caught without an e-way bill: the owner pays ₹72,000 penalty to release them.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Dispatch desk checklist', 'role': 'Article assistant',
             'situation': 'A factory\'s dispatch team asks when to generate e-way bills.',
             'steps': ['Check consignment value excluding exempt goods.', 'Check special cases like job work and handicrafts.', 'Fill Part A; fill or delegate Part B.', 'Track validity and extend in time if delayed.'],
             'takeaway': 'Generate before movement; a late e-way bill does not cure detention.'}]

    mcqs = [
        Q('m1', 'E-way bill is required where consignment value exceeds:', ['₹50,000', '₹1,00,000', '₹25,000', '₹2,00,000'], 0,
          'Rule 138(1) sets ₹50,000, measured on invoice value including tax but excluding exempt goods. In practice: special cases need it below this.', 'c1', T1, check=50000),
        Q('m2', 'Inter-State movement of goods worth ₹15,000 to a job worker:', ['Needs an e-way bill', 'Does not need one', 'Needs one only within the State', 'Needs a tax invoice instead'], 0,
          'The principal or registered job worker must generate one for inter-State job-work movement regardless of value. In practice: use a delivery challan as the document.', 'c1', T1),
        Q('m3', 'Validity for normal cargo travelling 250 km:', ['2 days', '1 day', '3 days', '5 days'], 0,
          'One day for every 200 km or part: 250 km needs 2 days. In practice: plan extensions for longer delays.', 'c2', T2, check=2),
        Q('m4', 'Part B of the e-way bill contains:', ['Vehicle or transport document details', 'HSN and value', 'GSTIN of recipient', 'Invoice number'], 0,
          'Part A has supply details; Part B has vehicle or transport document details. In practice: update Part B on transhipment.', 'c2', T2),
        Q('m5', 'An e-way bill can be cancelled within:', ['24 hours of generation', '72 hours', '8 hours', '7 days'], 0,
          'Cancellation is allowed within 24 hours if it has not been verified in transit. In practice: recipients have 72 hours to reject.', 'c2', T2, check=24),
        Q('m6', 'Which movement does NOT need an e-way bill?', ['Goods carried by bullock cart', 'Machinery in a truck worth ₹3 lakh', 'Inter-State handicrafts by an unregistered artisan', 'Sales return by truck worth ₹70,000'], 0,
          'Non-motorised conveyance is exempt. The others need one. In practice: hand carts and bicycles are also non-motorised.', 'c3', T3),
        Q('m7', 'Penalty to release taxable goods detained without documents, where the owner comes forward:', ['200% of tax payable', '100% of tax payable', '50% of value', '10% of tax'], 0,
          'Section 129(1)(a) fixes 200% of the tax for an owner who comes forward; others pay the higher of 50% of value and 200% of tax. In practice: tax is paid separately.', 'c3', T3),
        Q('m8', 'Part B need not be filled where movement within the State from consignor to transporter is up to:', ['50 km', '10 km', '100 km', '20 km'], 0,
          'Rule 138(3) proviso exempts Part B for intra-State movement up to 50 km between consignor or consignee and transporter. In practice: Part A is still needed.', 'c3', T3, check=50),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Normal cargo', 1, 'computation', '200', nums=[v1]), S('s2', 'ODC', 1, 'computation', '20 km', nums=[v2]), S('s3', 'Day definition', 1, 'concept', 'midnight')],
          ['Round up part distances.'], ['Counting the first day as 24 hours.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Value test', 1, 'concept', '50,000'), S('s2', 'Job work', 1, 'concept', 'job work'), S('s3', 'Annexure', 1, 'concept', 'annexure|vegetable'),
           S('s4', 'Non-motorised', 1, 'concept', 'non-motorised'), S('s5', '50 km rule', 1, 'concept', '50 km')],
          ['Give the reason each time.'], ['Ignoring the job-work rule.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is consignment value?', 'Invoice value including GST, excluding the value of exempt goods on the same invoice.',
          [P('p1', 'Including tax', 5, 'including|tax'), P('p2', 'Excluding exempt', 5, 'exempt')], 'c1'),
        V('v2', 'Who fills Part B?', 'The person who transports the goods — the registered supplier or recipient if using own conveyance, or the transporter.',
          [P('p1', 'Transporter', 5, 'transport'), P('p2', 'Vehicle details', 5, 'convey|vehicle|own')], 'c2'),
        V('v3', 'How is validity extended?', 'By the generator within 8 hours before or after expiry, if goods cannot reach in time due to exceptional circumstances.',
          [P('p1', '8 hours', 6, '8 hours'), P('p2', 'Exceptional', 4, 'exceptional')], 'c2'),
        V('v4', 'Name two exempt movements.', 'Goods moved by non-motorised conveyance and goods listed in the Annexure such as fresh vegetables, among others like customs-sealed movements.',
          [P('p1', 'Non-motorised', 5, 'non-motorised'), P('p2', 'Annexure or customs', 5, 'annexure|vegetable|customs')], 'c3'),
        V('v5', 'What happens if goods move without an e-way bill?', 'They may be detained or seized under section 129 and released on payment of penalty, 200% of tax for an owner who comes forward.',
          [P('p1', 'Detention', 5, 'detain|seiz'), P('p2', 'Penalty', 5, '200%|penalty')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Swift Movers', 'difficulty': 'moderate',
              'case': 'Swift Movers, a transporter, carries for a Bhopal manufacturer goods invoiced at ₹55,000 (including GST) plus exempt items of ₹10,000 on the same invoice, over 410 km to Jaipur. Midway the truck breaks down and the goods are shifted to another truck.',
              'mcqs': [
                  M('k1a', 'Is an e-way bill required?', ['Yes, consignment value is ₹55,000', 'No, value after exempt goods is below ₹50,000', 'No, transporters are exempt', 'Only for the exempt part'], 0,
                    'Consignment value excludes exempt goods: ₹55,000 of taxable goods including tax exceeds ₹50,000. In practice: show exempt goods separately.', 'moderate', topic=T1),
                  M('k1b', 'Validity for 410 km:', ['3 days', '2 days', '4 days', '1 day'], 0,
                    '410 km needs three 200-km blocks (200 + 200 + 10). In practice: count part blocks as full days.', 'core', check=3, topic=T2),
                  M('k1c', 'After shifting trucks, Swift must:', ['Update Part B with the new vehicle number', 'Generate a fresh invoice', 'Cancel the e-way bill', 'Do nothing'], 0,
                    'Part B is updated whenever the conveyance changes. In practice: a new e-way bill is not needed.', 'core', topic=T2),
                  M('k1d', 'If caught without a valid e-way bill and the owner comes forward, penalty is:', ['200% of tax on the goods', '50% of value', '₹10,000 flat', '25% of tax'], 0,
                    'Section 129(1)(a): 200% of tax payable on the goods. In practice: pay to secure release.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch12', 1, 'E-Way Bill',
                ['Determine when an e-way bill is required.',
                 'Explain Parts A and B, generation and validity.',
                 'Apply exemptions and consequences of non-compliance.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['int-p3-b-ch11-u01'],
                 'exam_tip': 'Compute consignment value first (exclude exempt goods), then check special cases and exemptions.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Required above ₹50,000 consignment value (incl. tax, excl. exempt goods).',
                             'Below ₹50,000 still needed for inter-State job work and handicrafts by exempt persons.',
                             'Validity: 200 km/day; ODC 20 km/day; extension within 8 hours.',
                             'Cancel within 24 hours; recipient rejects within 72 hours.',
                             'Exemptions: Annexure goods, non-motorised, customs movements; Part B not needed up to 50 km.'],
                 'remember': ['Update Part B on transhipment.', 's. 129: 200% of tax for owner.'],
                 'traps': ['First day ends at midnight of the next day.', 'Exempt goods excluded from consignment value.']},
                [('Threshold', '₹50,000'), ('Validity', '1 day / 200 km'), ('Cancellation', '24 hours'), ('Part B relief', '50 km')],
                viva, cases)
