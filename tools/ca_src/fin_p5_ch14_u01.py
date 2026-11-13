"""CA Final · Paper 5 · Chapter 14 Import and Export under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch14-u01'
T1 = 'Import of goods and services'
T2 = 'Export of goods and services'
T3 = 'Zero-rated supplies and LUT'
T4 = 'Deemed exports, merchant exports and SEZ'


def build():
    ck = Checks()
    bcd = ck.add('1000000*0.10', 'Basic customs duty at 10% (₹)')
    sws = ck.add('1000000*0.10*0.10', 'Social welfare surcharge at 10% of BCD (₹)')
    ig = ck.add('(1000000+1000000*0.10+1000000*0.10*0.10)*0.18', 'IGST at 18% (₹)')
    tot = ck.add('1000000*0.10+1000000*0.10*0.10+(1000000+1000000*0.10+1000000*0.10*0.10)*0.18', 'Total payable at import (₹)')
    i1 = {'id': 'i1', 'title': 'IGST on imported goods', 'difficulty': 'core', 'minutes': 7,
          'q': 'Rhea Electronics imports components with an assessable value of ₹10,00,000. BCD is 10%, social welfare surcharge 10% of BCD, IGST 18%. Compute duties and IGST and state whether ITC is available.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['BCD', '10% × 10,00,000', inr(bcd)],
              ['SWS', '10% × BCD', inr(sws)],
              ['IGST', '18% × (AV + BCD + SWS)', inr(ig)],
              ['Total', '', inr(tot)],
              ['ITC', 'IGST available as credit; BCD and SWS are costs', '—']], title='Section 3(7) Customs Tariff Act')],
          'checks': list(ck)}

    c2 = Checks()
    m = c2.add('5000000*0.001', 'GST on supply to merchant exporter at 0.1% (₹)')
    i2 = {'id': 'i2', 'title': 'Export under LUT and merchant exports', 'difficulty': 'moderate', 'minutes': 6,
          'q': '(a) Swati Textiles issues an export invoice under LUT on 10 January 2027. By when must the goods be exported? (b) It supplies goods worth ₹50,00,000 to a registered merchant exporter, who exports them within 90 days. Compute GST at the concessional rate.',
          'solution': [table(['Case', 'Rule', 'Result'], [
              ['(a) LUT export of goods', 'Export within 3 months of invoice; else pay IGST with interest within 15 days after', 'By 10 April 2027 (tax by 25 April if not)'],
              ['(b) Merchant export', '0.1% on supply; exporter must export within 90 days', f'₹{inr(m)}']], title='Section 16 IGST and notifications')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Import of goods is an inter-State supply; IGST is levied under section 3(7) of the Customs Tariff Act at the time of import, on assessable value plus BCD and other duties (excluding IGST and compensation cess). The place of supply is the importer\'s location.',
            'Import of services for consideration is a supply even outside business and attracts IGST under reverse charge in the recipient\'s hands (except OIDAR to non-taxable online recipients, where the foreign supplier pays). Import of services from related persons without consideration is a supply under Schedule I.',
            'High-sea sales and in-bond sales from customs warehouses are not supplies (Schedule III); IGST is collected once at clearance for home consumption on the value including high-sea sale premium.'],
          'Imports are taxed at the border or under reverse charge.',
          'IGST on imports of ₹10 lakh at 18% is ₹1,99,800 after BCD and SWS.'),
        C('c2', T2, [
            'Export of goods is taking goods out of India (section 2(5) IGST). Export of services (section 2(6)) requires: supplier in India, recipient outside India, place of supply outside India, payment received in convertible foreign exchange or permitted INR, and the supplier and recipient not being mere establishments of one person.',
            'Since 30 March 2026, intermediary services follow the recipient-location rule, so they can qualify as exports.',
            'Exports are zero-rated: ITC is allowed even if the supply is exempt, and either refund of IGST paid or refund of unutilised ITC is available.'],
          'Five conditions make a service an export.',
          'Consultancy to a US client paid in dollars is an export.'),
        C('c3', T3, [
            'Section 16 IGST: zero-rated supply means export of goods or services and supplies to SEZ units or developers for authorised operations. The exporter may (a) export under bond or LUT without IGST and claim refund of unutilised ITC, or (b) pay IGST and claim refund (only notified persons or goods may use option (b) for goods).',
            'Under LUT, goods must be exported within three months of the invoice and payment for services received within one year (extendable); otherwise tax is paid with interest within 15 days after those periods.',
            'If export proceeds are not realised within the FEMA time limit, refund received must be repaid with interest within 30 days after expiry.'],
          'Zero-rated supplies are taxed at zero with credit retained.',
          'Goods invoiced under LUT on 10 January must leave India by 10 April.'),
        C('c4', T4, [
            'Deemed exports (section 147 CGST) are notified supplies of goods manufactured in India that do not leave India — supplies against Advance Authorisation, to EOUs, of capital goods against EPCG authorisation, and of gold by banks against Advance Authorisation. Tax is paid and refund can be claimed by recipient or supplier.',
            'Supplies to registered merchant exporters are taxed at 0.1% (0.05% CGST + 0.05% SGST or 0.1% IGST), provided goods are exported within 90 days and other conditions are met.',
            'Supplies to SEZ units/developers are inter-State and zero-rated for authorised operations; goods imported by SEZ units are exempt from IGST; supplies by SEZ units to the DTA are treated as imports.'],
          'Special regimes relieve tax on supplies linked to exports.',
          'Goods worth ₹50 lakh to a merchant exporter carry only ₹5,000 of GST.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Export refund planning', 'role': 'GST consultant',
             'situation': 'An exporter accumulates ITC every month.',
             'steps': ['File LUT at the start of the year.', 'Track shipping bills and export within timelines.', 'Claim refund of unutilised ITC.', 'Monitor realisation of proceeds.'],
             'takeaway': 'LUT preserves cash flow for regular exporters.'}]

    mcqs = [
        Q('m1', 'IGST on imported goods is levied under:', ['Section 3(7) of the Customs Tariff Act', 'Section 9 CGST Act', 'Section 5 IGST Act at destination', 'Section 12 Customs Act'], 0,
          'Collected at customs. In practice: ITC available.', 'c1', T1),
        Q('m2', 'Import of services by an individual for personal use for consideration is:', ['A supply taxable under RCM', 'Not a supply', 'Exempt', 'Zero-rated'], 0,
          'Section 7(1)(b). In practice: OIDAR exception.', 'c1', T1),
        Q('m3', 'A high-sea sale before clearance is:', ['Neither supply of goods nor services', 'Taxable supply', 'Export', 'Zero-rated supply'], 0,
          'Schedule III. In practice: IGST once at clearance.', 'c1', T1),
        Q('m4', 'Which is NOT a condition for export of services?', ['Supplier registered in SEZ', 'Recipient outside India', 'Place of supply outside India', 'Payment in convertible foreign exchange'], 0,
          'Section 2(6). In practice: five conditions.', 'c2', T2),
        Q('m5', 'Under LUT, goods must be exported within:', ['Three months of invoice', 'One year', 'Six months', 'Thirty days'], 0,
          'Rule 96A. In practice: else pay tax.', 'c3', T3),
        Q('m6', 'Supplies to an SEZ unit for authorised operations are:', ['Zero-rated', 'Exempt', 'Intra-State taxable', 'Not supplies'], 0,
          'Section 16 IGST. In practice: LUT or IGST refund.', 'c4', T4),
        Q('m7', 'Concessional GST on supplies to merchant exporters is:', ['Zero point one percent', 'Zero point five percent', 'Five percent', 'Nil'], 0,
          'Notification. In practice: export within 90 days.', 'c4', T4),
        Q('m8', 'Supplies to EOUs are treated as:', ['Deemed exports', 'Exports', 'Imports', 'Exempt supplies'], 0,
          'Section 147. In practice: refund available.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Duties', 2, 'computation', 'BCD', nums=[bcd, sws]), S('s2', 'IGST and total', 3, 'computation', 'IGST', nums=[ig, tot])],
          ['Show base for IGST.'], ['Charging IGST on assessable value only.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'LUT timeline', 2, 'analysis', 'three months'), S('s2', 'Merchant export', 2, 'computation', '0.1%', nums=[m])],
          ['State conditions.'], ['Applying 5% to merchant export supplies.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is a zero-rated supply?', 'Exports of goods or services and supplies to SEZ units or developers for authorised operations.',
          [P('p1', 'Exports', 5, 'export'), P('p2', 'SEZ', 5, 'sez')], 'c3'),
        V('v2', 'What are the two routes for zero-rated supplies?', 'Supply under bond or LUT without IGST with refund of ITC, or pay IGST and claim refund.',
          [P('p1', 'LUT', 5, 'lut'), P('p2', 'Refund', 5, 'refund')], 'c3'),
        V('v3', 'What happens if export proceeds are not realised?', 'The refund must be repaid with interest within 30 days after the FEMA time limit.',
          [P('p1', 'Repaid', 5, 'repaid'), P('p2', 'FEMA', 5, 'fema')], 'c3'),
        V('v4', 'Name two deemed export categories.', 'Supplies to EOUs and supplies against Advance Authorisation.',
          [P('p1', 'EOU', 5, 'eou'), P('p2', 'Advance Authorisation', 5, 'advance authorisation')], 'c4'),
        V('v5', 'How are SEZ supplies into the DTA treated?', 'As imports, attracting customs duty and IGST.',
          [P('p1', 'Imports', 5, 'import'), P('p2', 'IGST', 5, 'igst')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Agastya Software', 'difficulty': 'core',
              'case': 'Agastya Software (Bengaluru) provides development services to its wholly owned subsidiary in Singapore (a separate company) for USD 1,00,000, received in foreign exchange. It also provides services to its own branch in Dubai.',
              'mcqs': [
                  M('k1a', 'Services to the Singapore subsidiary are:', ['Export of services', 'Domestic supply', 'Exempt', 'Not a supply'], 0,
                    'Separate legal entity. In practice: all conditions met.', 'core', topic=T2),
                  M('k1b', 'Services to its own Dubai branch are:', ['Not an export — establishments of the same person', 'Export', 'Exempt', 'Deemed export'], 0,
                    'Section 2(6)(v). In practice: Explanation to section 8.', 'core', topic=T2),
                  M('k1c', 'Under LUT, payment for exports should be received within (years):', ['1', '3', '2', '5'], 0,
                    'Rule 96A. In practice: extendable.', 'core', check=1, topic=T3),
                  M('k1d', 'Agastya can claim refund of:', ['Unutilised ITC on exports', 'Customs duty', 'Income-tax', 'Nothing'], 0,
                    'Section 54. In practice: RFD-01.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch14', 1, 'Import and Export Under GST',
                ['Apply GST on import of goods and services.',
                 'Determine export of goods and services.',
                 'Apply zero-rating and LUT provisions.',
                 'Apply deemed exports, merchant exports and SEZ rules.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch13-u01'],
                 'exam_tip': 'For exports of services, test all five conditions in order.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Import of goods: IGST under CTA 3(7) on AV + duties.', 'Import of services: RCM; OIDAR exception.', 'Export of services: five conditions.',
                             'Zero-rating: LUT or IGST refund; 3 months / 1 year.', 'Deemed exports; merchant export 0.1%; SEZ.'],
                 'remember': ['Branch abroad is not a separate person.'],
                 'traps': ['Treating services to own foreign branch as exports.']},
                [('Zero-rated', 'IGST section 16'), ('Export of services', 'IGST section 2(6)'), ('Deemed exports', 'CGST section 147')],
                viva, cases)
