"""CA Final · Paper 5 · Chapter 3 Place of Supply.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch03-u01'
T1 = 'Inter-State and intra-State supply'
T2 = 'Place of supply of goods'
T3 = 'Place of supply of services within India'
T4 = 'Place of supply in cross-border services'


def build():
    ck = Checks()
    ig = ck.add('500000*0.18', 'IGST on inter-State supply at 18% (₹)')
    cg = ck.add('500000*0.09', 'CGST (and equal SGST) on intra-State supply (₹)')
    i1 = {'id': 'i1', 'title': 'Bill-to-ship-to and movement of goods', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Anant Ltd (Haryana) sells goods worth ₹5,00,000 (18%) to Brijesh & Co (Punjab), who asks Anant to deliver them to its customer Chhavi in Haryana. Separately, Anant sells goods worth ₹5,00,000 to a Haryana buyer, delivered within Haryana. Determine place of supply and tax.',
          'solution': [table(['Supply', 'Place of supply', 'Tax (₹)'], [
              ['Anant to Brijesh (bill-to-ship-to)', 'Principal place of business of Brijesh — Punjab (section 10(1)(b)); inter-State', f'IGST {inr(ig)}'],
              ['Brijesh to Chhavi', 'Where movement terminates for Chhavi — Haryana; inter-State from Punjab', '—'],
              ['Anant to Haryana buyer', 'Haryana — intra-State', f'CGST {inr(cg)} + SGST {inr(cg)}']], title='IGST Act section 10')],
          'checks': list(ck)}

    c2 = Checks()
    v = c2.add('2000000*0.18', 'GST that would apply if the service were not an export (₹)')
    i2 = {'id': 'i2', 'title': 'Intermediary after the 2026 amendment', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Nikhil, a commission agent in Mumbai, arranges sales of Indian handicrafts for a US buyer and earns commission of ₹20,00,000 in foreign currency in October 2026. Determine the place of supply and whether it is an export of services.',
          'solution': [table(['Point', 'Analysis', 'Result'], [
              ['Nature', 'Intermediary (broker) service', '—'],
              ['Law', 'Section 13(8)(b) omitted w.e.f. 30 March 2026; default rule section 13(2)', 'Location of recipient — USA'],
              ['Export test', 'Supplier in India, recipient outside, POS outside, paid in convertible foreign exchange, not merely establishments of one person', 'Export — zero-rated'],
              ['Tax saved', f'18% on ₹20 lakh would have been ₹{inr(v)}', 'Nil with LUT']], title='IGST Act section 13')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'A supply is inter-State if the supplier sits in one State or UT and the place of supply falls in another (section 7 of the IGST Act); intra-State where both are in the same State (section 8). Imports, exports and supplies to or by SEZ units or developers are inter-State.',
            'Supplies to international tourists leaving India and supplies in the taxable territory not otherwise intra-State are also inter-State. An establishment in a State and another in another State are treated as establishments of distinct persons.',
            'Wrongly paying IGST instead of CGST + SGST (or vice versa) does not attract interest: the taxpayer pays the correct tax and claims refund of the wrong tax.'],
          'Supplier location vs place of supply decides the tax type.',
          'A Mumbai supplier billing a Pune buyer charges CGST + SGST.'),
        C('c2', T2, [
            'Section 10: where goods move, place of supply is where movement terminates for delivery; in bill-to-ship-to cases where goods are delivered to a third person on a person\'s direction, it is the principal place of business of the person directing; where goods do not move, the location at the time of delivery; goods assembled or installed — place of installation; goods on board a conveyance — place where taken on board.',
            'Section 10(1)(ca): for goods supplied to unregistered persons, place of supply is the address recorded in the invoice (naming the State suffices), else the supplier\'s location.',
            'Section 11 for imports and exports: imported goods — location of the importer; exported goods — location outside India.'],
          'Follow the goods, except where a buyer directs delivery to someone else.',
          'Goods sold to a Punjab dealer but shipped to Haryana have place of supply in Punjab.'),
        C('c3', T3, [
            'Section 12(2) default: to a registered person — location of recipient; to others — address on record, otherwise location of supplier. Specific rules: immovable property and hotel accommodation — location of property; restaurant, beauty, health and fitness services — where performed; training — recipient\'s location if registered, else where performed; admission to events — where event held.',
            'Organising events: registered recipient\'s location, else event location; transport of goods and passengers — registered recipient\'s location, else where goods handed over or journey begins; telecommunication — by connection type; banking and insurance — recipient\'s address on record; advertising to government — each State in proportion.',
            'Where both supplier and recipient are in India, these rules apply even if services are performed abroad (with specific exceptions).'],
          'Domestic services: mostly recipient-based, with property and event exceptions.',
          'A Delhi firm training a registered Bengaluru client has place of supply in Karnataka.'),
        C('c4', T4, [
            'Section 13 applies where either the supplier or recipient is outside India. Default — location of recipient (or supplier if recipient location is unknown). Performance-based services on goods physically made available or requiring physical presence — where performed; immovable property — location of property; events — where held.',
            'Specific rules: banking services to account holders, transport of goods other than by mail, and hiring of conveyances up to a month — location of supplier; online information and database access (OIDAR) — location of recipient; passenger transportation — where passenger embarks.',
            'Intermediary services: section 13(8)(b) was omitted by the Finance Act 2026 from 30 March 2026, so such services now follow the default rule — location of recipient — and services to foreign recipients can qualify as exports.'],
          'Cross-border services: recipient-based by default, with key exceptions.',
          'Commission earned from a US principal is now an export of services.'),
    ]

    jobs = [{'id': 'j1', 'title': 'POS review of invoices', 'role': 'GST consultant',
             'situation': 'A company is unsure whether to charge IGST or CGST + SGST on several contracts.',
             'steps': ['Identify supplier location and recipient registration.', 'Apply goods or services rules.', 'Check cross-border rules where needed.', 'Correct tax type and seek refunds of wrong tax.'],
             'takeaway': 'Wrong tax type means paying again and claiming refund.'}]

    mcqs = [
        Q('m1', 'A supply to an SEZ unit in the same State is:', ['Inter-State supply', 'Intra-State supply', 'Exempt supply', 'Not a supply'], 0,
          'IGST section 7(5). In practice: zero-rated.', 'c1', T1),
        Q('m2', 'In a bill-to-ship-to transaction, place of supply for the first supplier is:', ['Principal place of business of the person directing delivery', 'Delivery location', 'Supplier location', 'Port of loading'], 0,
          'Section 10(1)(b). In practice: IGST often.', 'c2', T2),
        Q('m3', 'Place of supply of imported goods is:', ['Location of the importer', 'Port of entry', 'Country of origin', 'Customs station'], 0,
          'Section 11. In practice: IGST at customs.', 'c2', T2),
        Q('m4', 'Place of supply of hotel accommodation in Goa for a Delhi guest is:', ['Goa', 'Delhi', 'Location of booking agent', 'Supplier\'s head office'], 0,
          'Section 12(3). In practice: CGST + SGST in Goa.', 'c3', T3),
        Q('m5', 'Default place of supply for services to a registered person in India is:', ['Location of recipient', 'Location of supplier', 'Place of performance', 'Location of bank'], 0,
          'Section 12(2). In practice: GSTIN address.', 'c3', T3),
        Q('m6', 'From 30 March 2026, place of supply of intermediary services in cross-border cases is:', ['Location of recipient', 'Location of supplier', 'Place of performance', 'India always'], 0,
          'Section 13(8)(b) omitted. In practice: exports possible.', 'c4', T4),
        Q('m7', 'OIDAR services to a person in India from abroad have place of supply at:', ['Location of recipient', 'Location of supplier', 'Server location', 'Nil'], 0,
          'Section 13(12). In practice: supplier registers.', 'c4', T4),
        Q('m8', 'If IGST is wrongly paid instead of CGST and SGST, the taxpayer:', ['Pays correct tax and claims refund without interest', 'Pays interest', 'Can adjust automatically', 'Loses the amount'], 0,
          'Section 77 CGST / 19 IGST. In practice: refund claim.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Bill-to-ship-to', 3, 'analysis', 'principal place', nums=[ig]), S('s2', 'Intra-State sale', 3, 'computation', 'CGST', nums=[cg])],
          ['Cite section 10.'], ['Using delivery location for the first leg.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Place of supply', 3, 'analysis', 'recipient'), S('s2', 'Export conditions', 2, 'analysis', 'export', nums=[v])],
          ['Mention amendment date.'], ['Applying the omitted clause.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'When is a supply inter-State?', 'When the supplier is located in one State or UT and the place of supply lies in a different one.',
          [P('p1', 'Supplier located', 5, 'supplier is located'), P('p2', 'Different States', 5, 'different')], 'c1'),
        V('v2', 'A machine is sold by a Gujarat firm and erected at a Kerala factory. Where is the place of supply?', 'Kerala, because the goods are assembled or installed at site there.',
          [P('p1', 'Kerala', 5, 'kerala'), P('p2', 'Assembled at site', 5, 'assembled')], 'c2'),
        V('v3', 'What is the place of supply of admission to a concert?', 'The place where the event is actually held.',
          [P('p1', 'Event', 5, 'event'), P('p2', 'Held', 5, 'held')], 'c3'),
        V('v4', 'What is the place of supply of performance-based services on goods abroad?', 'The place where the services are actually performed.',
          [P('p1', 'Performed', 5, 'performed'), P('p2', 'Actually', 5, 'actually')], 'c4'),
        V('v5', 'How did the Finance Act 2026 affect intermediaries?', 'It omitted section 13(8)(b), so the default recipient-location rule now applies.',
          [P('p1', 'Omitted', 5, 'omitted'), P('p2', 'Recipient location', 5, 'recipient')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Skyline Events', 'difficulty': 'core',
              'case': 'Skyline Events (Delhi) organises a product launch in Jaipur for Orion Ltd, registered in Maharashtra, for ₹10,00,000 at 18%. It also sells admission tickets to the public for a music show in Jaipur.',
              'mcqs': [
                  M('k1a', 'Place of supply for organising the launch for Orion:', ['Maharashtra', 'Rajasthan', 'Delhi', 'Any State'], 0,
                    'Registered recipient. In practice: section 12(7).', 'core', topic=T3),
                  M('k1b', 'Tax on the launch (₹):', ['1,80,000 IGST', '90,000 CGST + 90,000 SGST', 'Nil', '50,000 IGST'], 0,
                    'Delhi to Maharashtra is inter-State. In practice: 18%.', 'core', check=180000, topic=T3),
                  M('k1c', 'Place of supply for admission tickets:', ['Rajasthan', 'Delhi', 'Buyer\'s State', 'Maharashtra'], 0,
                    'Where event held. In practice: Skyline registers in Rajasthan if needed.', 'core', topic=T3),
                  M('k1d', 'Supply of admission tickets from Delhi supplier to Jaipur event is:', ['Inter-State', 'Intra-State', 'Export', 'Exempt'], 0,
                    'Supplier location Delhi. In practice: IGST.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch03', 1, 'Place of Supply',
                ['Distinguish inter-State and intra-State supplies.',
                 'Determine place of supply of goods.',
                 'Determine place of supply of services within India.',
                 'Determine place of supply in cross-border services.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p5-ch02-u01'],
                 'exam_tip': 'Identify whether section 12 or 13 applies before choosing the specific rule.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['IGST sections 7 and 8: inter vs intra-State.', 'Section 10 goods; bill-to-ship-to rule.', 'Section 11 imports/exports.',
                             'Section 12 domestic services; section 13 cross-border.', 'Section 13(8)(b) omitted from 30 March 2026.'],
                 'remember': ['SEZ supplies are inter-State.'],
                 'traps': ['Treating intermediary services as taxable in India after the 2026 change.']},
                [('Inter/intra-State', 'IGST sections 7–8'), ('Goods', 'Sections 10–11'), ('Domestic services', 'Section 12'), ('Cross-border services', 'Section 13')],
                viva, cases)
