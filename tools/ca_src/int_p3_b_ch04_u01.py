"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 4 Place of Supply.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch04-u01'
T1 = 'Why place of supply matters: inter-State v. intra-State (IGST ss. 7–9)'
T2 = 'Place of supply of goods (IGST ss. 10–11)'
T3 = 'Place of supply of services within India (IGST s. 12)'
T4 = 'Cross-border services (IGST s. 13) and export of services'


def build():
    ck = Checks()
    a = ck.add('200000*18/100', 'IGST on bill-to-ship-to supply')
    i1 = {'id': 'i1', 'title': 'Bill to one, ship to another', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Kiran Traders, Mumbai (Maharashtra), receives an order from Delta Ltd., Chennai (Tamil Nadu), to deliver goods worth ₹2,00,000 (18%) directly to Delta\'s customer in Pune (Maharashtra). Determine the place of supply and the tax on Kiran\'s invoice to Delta.',
          'solution': [table(['Point', 'Answer'], [
              ['Rule', 'Section 10(1)(b): goods delivered to a recipient or another person on the direction of a third person — place of supply is the principal place of business of that third person'],
              ['Third person', 'Delta Ltd., whose principal place of business is in Tamil Nadu'],
              ['Place of supply', 'Tamil Nadu'],
              ['Nature', 'Supplier in Maharashtra, place of supply Tamil Nadu: inter-State'],
              ['Tax', 'IGST 18% = ' + inr(a)]], title='Bill-to-ship-to'),
              note('Delta\'s own sale to its Pune customer is a separate supply: Tamil Nadu to Maharashtra, again inter-State.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Where is the service supplied?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Determine the place of supply: (a) an architect in Delhi designs a house in Jaipur for an unregistered individual living in Delhi; (b) a Kolkata hotel lodges a registered company from Bengaluru; (c) a Hyderabad institute trains staff of a registered company located in Pune; (d) a courier in Lucknow picks up a parcel from an unregistered person for delivery in Bhopal.',
          'solution': [table(['Case', 'Place of supply', 'Rule'], [
              ['(a)', 'Rajasthan (Jaipur)', 's. 12(3): services directly in relation to immovable property — location of the property'],
              ['(b)', 'West Bengal (Kolkata)', 's. 12(3): lodging — location of the hotel'],
              ['(c)', 'Maharashtra (Pune)', 's. 12(5): training to a registered person — location of the recipient'],
              ['(d)', 'Uttar Pradesh (Lucknow)', 's. 12(8): transport of goods for an unregistered person — where goods are handed over for transport']], title='Section 12')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 7 of the IGST Act: a supply is inter-State when the location of the supplier and the place of supply are in different States or Union Territories; imports, exports, supplies to or by SEZ units and supplies by non-tax-territory persons are also inter-State. Section 8: intra-State when both are in the same State or UT (supplies to SEZs excepted).',
            'Place of supply decides whether IGST or CGST + SGST/UTGST is charged and which State gets the revenue. Tax wrongly charged as intra-State instead of inter-State (or vice versa) must be paid correctly, with a refund of the wrong tax — no interest is payable on the correct tax.',
            'Location of supplier/recipient of services: the registered place of business, a fixed establishment, the most directly concerned establishment if several, or else the usual place of residence.'],
          'Compare two points on the map — supplier location and place of supply — and the type of tax follows.',
          'A Gurugram firm supplying to a Gurugram client charges CGST + SGST of Haryana; to a Noida client, IGST.'),
        C('c2', T2, [
            'Section 10(1): (a) where goods move, the location where movement ends for delivery; (b) bill-to-ship-to on a third person\'s direction — the principal place of business of that third person; (c) no movement — location of goods at delivery; (d) goods installed or assembled at site — the place of installation; (e) goods supplied on board a vessel, aircraft, train or vehicle — the place where taken on board.',
            'Section 11: imported goods — location of the importer; exported goods — the location outside India.'],
          'For goods, follow where the goods end up — unless someone else directed the delivery.',
          'A lift supplied by a Chennai company and installed in a Kochi mall: place of supply is Kerala.'),
        C('c3', T3, [
            'Section 12(2) general rule: to a registered person — location of that person; to an unregistered person — his address on record, or else the location of the supplier.',
            'Exceptions: immovable property, lodging, events at such property — location of the property (section 12(3)); restaurant, catering, beauty, fitness and health services — where performed (12(4)); training and performance appraisal — registered recipient\'s location, else where performed (12(5)); admission to events or amusement parks — where held (12(6)); organising events — registered recipient\'s location, else where held (12(7)).',
            'Transport of goods including courier — registered recipient\'s location, else where goods are handed over (12(8)); passenger transport — registered recipient\'s location, else where the passenger boards for a continuous journey (12(9)); services on board a conveyance — first scheduled departure point (12(10)); banking and financial services — recipient\'s location on the supplier\'s records (12(12)); insurance — registered recipient\'s location, else on records (12(13)).'],
          'Services have no physical journey, so the law uses proxies: recipient, property, performance or event.',
          'A beauty parlour in Goa serving a tourist from Punjab: place of supply is Goa, where performed.'),
        C('c4', T4, [
            'Section 13 applies when supplier or recipient is outside India. General rule: location of the recipient; if unknown, location of the supplier.',
            'Exceptions: services on goods physically made available (e.g. repairs) and services needing the recipient\'s physical presence — where performed; services relating to immovable property — location of the property; admission to or organising events — where held; banking to account holders and hiring of means of transport up to one month — location of the supplier; transport of goods (other than mail or courier) — destination; passenger transport — where the passenger boards; online information and database access — location of the recipient.',
            'Intermediary services: the Finance Act, 2026 removed them from the supplier-location rule, so from the notified date they follow the general rule (location of the recipient), allowing such services to foreign principals to qualify as exports.',
            'Export of services (IGST s. 2(6)): supplier in India, recipient outside India, place of supply outside India, payment in convertible foreign exchange (or Indian rupees where RBI permits), and supplier and recipient not merely establishments of the same person.'],
          'For cross-border services, the recipient\'s location usually wins — the exceptions follow physical performance or property.',
          'A Bengaluru firm writing software for a US client, paid in dollars: place of supply is the USA, so it is an export.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Invoice tax-type check', 'role': 'Article assistant',
             'situation': 'A services firm finds IGST and CGST/SGST charged inconsistently on similar invoices.',
             'steps': ['List supplier location and recipient status for each invoice.', 'Apply section 12 or 13 to each service type.', 'Correct the tax type and issue credit and fresh invoices.', 'Claim refund of tax wrongly paid.'],
             'takeaway': 'Wrong tax type is fixed by paying the right one and refunding the wrong one.'}]

    mcqs = [
        Q('m1', 'Goods are sold by a Surat dealer to a Surat buyer but delivered in Indore at the buyer\'s request; the buyer is the recipient. Place of supply:', ['Madhya Pradesh', 'Gujarat', 'Location of the transporter', 'Either State'], 0,
          'Where goods move, place of supply is where movement terminates for delivery to the recipient — Indore. The supply is inter-State. In practice: charge IGST.', 'c2', T2),
        Q('m2', 'Place of supply of imported goods is:', ['Location of the importer', 'Port of import', 'Location of the foreign supplier', 'Customs station'], 0,
          'Section 11(a) uses the location of the importer. IGST is collected at import with customs duty. In practice: credit goes to the importer\'s GSTIN.', 'c2', T2),
        Q('m3', 'A Delhi consultant advises a registered company in Lucknow. Place of supply:', ['Uttar Pradesh', 'Delhi', 'Either', 'Where the advice is given'], 0,
          'General rule u/s 12(2): service to a registered person — location of the recipient. In practice: check the GSTIN on the purchase order.', 'c3', T3),
        Q('m4', 'Services of a hotel in Shimla to a guest from Chandigarh: place of supply is:', ['Himachal Pradesh', 'Chandigarh', 'Location of the travel agent', 'Delhi'], 0,
          'Lodging is linked to immovable property, so the location of the hotel decides it. In practice: the hotel charges CGST + SGST of Himachal Pradesh.', 'c3', T3),
        Q('m5', 'Transport of goods by road for an unregistered person: place of supply is:', ['Where goods are handed over for transport', 'Destination of goods', 'Location of the transporter', 'Location of the recipient'], 0,
          'Section 12(8): for registered recipients, their location; otherwise where the goods are handed over. In practice: GTAs usually serve registered persons.', 'c3', T3),
        Q('m6', 'An Indian firm repairs a machine temporarily brought into India by a German client. Place of supply:', ['India, where the service is performed', 'Germany', 'Location of the supplier', 'Both'], 0,
          'Section 13(3): services on goods physically made available by the recipient — where performed. In practice: such repairs are not exports.', 'c4', T4),
        Q('m7', 'Which is NOT a condition for export of services?', ['Payment must be received before the supply', 'Supplier is in India', 'Recipient is outside India', 'Place of supply is outside India'], 0,
          'Payment must be in convertible foreign exchange (or rupees where RBI allows), but there is no rule that it must come in advance. In practice: keep FIRC/BRC evidence.', 'c4', T4),
        Q('m8', 'A supply by a supplier in Gujarat to an SEZ unit in Gujarat is:', ['Inter-State', 'Intra-State', 'Exempt', 'Export of goods'], 0,
          'Section 7(5)(b) treats supplies to an SEZ developer or unit as inter-State, so IGST (usually zero-rated) applies. In practice: supply under LUT without paying tax.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Rule cited', 1, 'concept', '10(1)(b)|third person'), S('s2', 'Place of supply', 1, 'concept', 'tamil nadu'),
           S('s3', 'Inter-State', 1, 'concept', 'inter-state'), S('s4', 'IGST', 1, 'computation', 'IGST', nums=[a])],
          ['Name the third person.'], ['Treating the Pune delivery as the place of supply.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Immovable property', 1, 'concept', 'property|12(3)'), S('s2', 'Hotel', 1, 'concept', 'hotel|bengal'),
           S('s3', 'Training', 1, 'concept', '12(5)|registered'), S('s4', 'Courier', 1, 'concept', 'handed over|12(8)')],
          ['Quote the sub-section.'], ['Using the general rule for property services.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'When is a supply inter-State?', 'When the location of the supplier and the place of supply are in different States or Union Territories, and in specified cases such as imports, exports and supplies to SEZs.',
          [P('p1', 'Different States', 6, 'different'), P('p2', 'Special cases', 4, 'import|export|sez')], 'c1'),
        V('v2', 'What is the general rule for services within India?', 'Location of the recipient if registered; for an unregistered recipient, his address on record or else the location of the supplier.',
          [P('p1', 'Registered recipient', 5, 'registered'), P('p2', 'Fallback', 5, 'record|supplier')], 'c3'),
        V('v3', 'What is the place of supply in a bill-to-ship-to case?', 'The principal place of business of the third person on whose direction the goods are delivered to another person.',
          [P('p1', 'Third person', 6, 'third person|direction'), P('p2', 'Principal place', 4, 'principal place')], 'c2'),
        V('v4', 'What is the general rule for cross-border services?', 'The location of the recipient, or, where that is not available in the ordinary course, the location of the supplier.',
          [P('p1', 'Recipient', 6, 'recipient'), P('p2', 'Fallback', 4, 'supplier')], 'c4'),
        V('v5', 'What changed for intermediary services in 2026?', 'The Finance Act, 2026 removed them from the supplier-location rule, so their place of supply follows the location of the recipient once notified.',
          [P('p1', 'Recipient location', 6, 'recipient'), P('p2', 'Finance Act 2026', 4, '2026|finance act')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Eventix Pvt. Ltd.', 'difficulty': 'moderate',
              'case': 'Eventix Pvt. Ltd., Mumbai, (i) organises a product launch in Goa for a registered client based in Ahmedabad; (ii) sells tickets to individuals for a concert in Mumbai; (iii) organises a seminar in Dubai for an unregistered Indian association based in Pune; (iv) provides event software to a client in Singapore, paid in dollars.',
              'mcqs': [
                  M('k1a', 'Place of supply in (i):', ['Gujarat', 'Goa', 'Maharashtra', 'Any'], 0,
                    'Organising an event for a registered person: location of that person (Ahmedabad, Gujarat). In practice: IGST applies from Mumbai.', 'moderate', topic=T3),
                  M('k1b', 'Place of supply in (ii):', ['Maharashtra', 'Location of each buyer', 'Delhi', 'Outside India'], 0,
                    'Admission to an event: where the event is held — Mumbai. In practice: CGST + SGST apply.', 'core', topic=T3),
                  M('k1c', 'Place of supply in (iii):', ['Maharashtra, location of the recipient', 'Dubai', 'Location of the supplier', 'Not taxable'], 0,
                    'For an unregistered recipient where the event is held outside India, section 12(7) uses the recipient\'s location. In practice: tax is CGST + SGST as both are in Maharashtra.', 'hard', topic=T3),
                  M('k1d', 'Supply (iv) is:', ['Export of services', 'Inter-State supply in India', 'Exempt supply', 'Import of services'], 0,
                    'Recipient outside India, place of supply its location, payment in convertible foreign exchange — an export, zero-rated. In practice: supply under LUT.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch04', 1, 'Place of Supply',
                ['Classify a supply as inter-State or intra-State.',
                 'Determine the place of supply of goods.',
                 'Determine the place of supply of services within India and across borders.',
                 'Identify an export of services.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 40}, 'prereq': ['int-p3-b-ch03-u01'],
                 'exam_tip': 'Write the sub-section for each answer; check the recipient\'s registration before applying section 12.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Inter-State: supplier location ≠ place of supply; SEZ and imports always inter-State.',
                             'Goods: end of movement; bill-to-ship-to → third person; installation → site.',
                             'Services in India: registered recipient; exceptions for property, performance, events, transport.',
                             'Cross-border: recipient\'s location; exceptions for performance, property, events, specified services.'],
                 'remember': ['Import of goods: location of importer.', 'Wrong tax type: pay right tax, refund wrong one, no interest.'],
                 'traps': ['Supplies to SEZ in the same State are inter-State.', 'Event outside India for unregistered recipient → recipient location.']},
                [('s. 10', 'Goods in India'), ('s. 11', 'Import/export of goods'), ('s. 12', 'Services in India'), ('s. 13', 'Cross-border services')],
                viva, cases)
