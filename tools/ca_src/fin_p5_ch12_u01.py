"""CA Final · Paper 5 · Chapter 12 Electronic Commerce Transactions.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch12-u01'
T1 = 'E-commerce operators and registration'
T2 = 'Tax payable by ECO under section 9(5)'
T3 = 'Tax collection at source by ECO'
T4 = 'OIDAR and online services from abroad'


def build():
    ck = Checks()
    nv = ck.add('1000000-100000', 'Net value of taxable supplies (₹)')
    tcs = ck.add('(1000000-100000)*0.005', 'TCS at 0.5% (₹)')
    half = ck.add('(1000000-100000)*0.0025', 'CGST (and equal SGST) component (₹)')
    i1 = {'id': 'i1', 'title': 'TCS by an e-commerce operator', 'difficulty': 'core', 'minutes': 6,
          'q': 'ShopKart, an ECO in Karnataka, facilitated intra-State sales by registered sellers of ₹10,00,000 in November 2026; goods worth ₹1,00,000 were returned in the same month. It also facilitated restaurant services of ₹2,00,000 on which it pays tax under section 9(5). Compute TCS.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Net value', '10,00,000 − 1,00,000 (section 9(5) supplies excluded)', inr(nv)],
              ['TCS @ 0.5%', 'Intra-State: 0.25% CGST + 0.25% SGST', inr(tcs)],
              ['Each component', '', inr(half)],
              ['Statement', 'GSTR-8 by 10th of next month', '—']], title='Section 52')],
          'checks': list(ck)}

    c2 = Checks()
    t = c2.add('5000000*0.18', 'IGST on OIDAR supplies to unregistered Indians at 18% (₹)')
    i2 = {'id': 'i2', 'title': 'Foreign streaming service', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'StreamWave Inc. (USA) earns ₹50,00,000 in a quarter from subscriptions sold to unregistered individuals in India, and ₹20,00,000 from registered Indian businesses. Determine tax implications.',
          'solution': [table(['Customer', 'Treatment', '₹'], [
              ['Unregistered individuals', 'OIDAR to non-taxable online recipients — StreamWave registers (simplified scheme) and pays IGST', inr(t)],
              ['Registered businesses', 'Recipients pay IGST under reverse charge', '—']], title='IGST section 14')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'An e-commerce operator (ECO) is whoever runs — by owning, operating or managing — a digital platform used for e-commerce. ECOs liable under section 9(5) or required to collect TCS must register irrespective of turnover.',
            'Suppliers through ECOs that collect TCS must register irrespective of turnover, except (i) suppliers of services with aggregate turnover up to ₹20 lakh (₹10 lakh in special States) and (ii) notified suppliers of goods meeting conditions (intra-State, PAN-linked enrolment, etc.).',
            'Composition dealers may supply goods through ECOs under a special procedure; the ECO collects TCS and does not allow inter-State supplies by them.'],
          'Platforms and many sellers on them must register from the first rupee.',
          'A home-décor seller on a marketplace must register even with ₹5 lakh sales.'),
        C('c2', T2, [
            'Section 9(5) makes the ECO liable for tax on notified services supplied through it: passenger transport by radio taxi, motor cab, maxi cab, motorcycle, omnibus or other motor vehicle; hotel, inn, guest house, club and campsite accommodation (with exceptions where supplier is registered); housekeeping services such as plumbing and carpentry (unless supplier is registered); and restaurant services (except from specified premises).',
            'The ECO pays the tax as if it were the supplier and issues the invoice; the underlying suppliers need not register only because of these services.',
            'Supplies covered by section 9(5) are excluded from TCS computation.'],
          'For notified services the platform is the taxpayer.',
          'A cab aggregator pays GST on rides by unregistered drivers.'),
        C('c3', T3, [
            'Section 52: an ECO (not being an agent) collects TCS at 0.5% (0.25% CGST + 0.25% SGST/UTGST, or 0.5% IGST) on the net taxable value of other suppliers\' sales routed through its platform where it collects the consideration — gross value less returns, excluding section 9(5) supplies.',
            'The ECO pays TCS by the 10th of the next month and files GSTR-8 by then; an annual statement is due by 31 December after the year. The supplier claims the amount in its cash ledger after acceptance.',
            'Officers can seek details of supplies, stock and warehouses from the ECO; failure attracts penalty. Mismatches between the ECO\'s statement and the supplier\'s returns are communicated and, if not rectified, added to the supplier\'s liability.'],
          'Platforms withhold half a percent on net sales of sellers.',
          'Net sales of ₹9 lakh through a platform carry TCS of ₹4,500.'),
        C('c4', T4, [
            'Online information and database access or retrieval (OIDAR) services — such as streaming, cloud services, online advertising, e-books, digital data storage and online gaming — supplied with minimal human intervention through the internet are covered by special provisions. Place of supply follows where the recipient is located.',
            'A foreign OIDAR supplier selling to non-taxable online recipients (unregistered persons, including those registered only for TDS or Government bodies not engaged in business) in India must register under a simplified scheme and pay IGST; where an intermediary arranges the supply, the intermediary is deemed the supplier.',
            'For supplies to registered persons in India, the recipient pays IGST under reverse charge. Online money gaming suppliers from abroad must register and pay tax regardless of OIDAR status.'],
          'Foreign digital services to Indian consumers are taxed in India.',
          'A US streaming service selling to Indian households pays 18% IGST.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Marketplace seller onboarding', 'role': 'GST consultant',
             'situation': 'A small artisan wants to sell on a marketplace.',
             'steps': ['Check if registration exemption applies.', 'Explain TCS deduction and claiming.', 'Reconcile monthly TCS with sales.', 'Handle returns in net value.'],
             'takeaway': 'TCS is not a cost if claimed properly.'}]

    mcqs = [
        Q('m1', 'Rate of TCS under section 52 on intra-State supplies is:', ['0.25% CGST + 0.25% SGST', '1% CGST + 1% SGST', '0.5% CGST + 0.5% SGST', '2% IGST'], 0,
          'Total 0.5%. In practice: on net value.', 'c3', T3),
        Q('m2', 'Net value for TCS excludes:', ['Supplies under section 9(5)', 'Taxable supplies', 'Inter-State supplies', 'Supplies by registered sellers'], 0,
          'Explanation to section 52(1). In practice: also returns.', 'c3', T3),
        Q('m3', 'GSTR-8 must be filed by:', ['Tenth of the next month', 'Twentieth of next month', 'Last day of quarter', 'Thirty-first December'], 0,
          'Section 52(4). In practice: with payment.', 'c3', T3),
        Q('m4', 'Under section 9(5), the ECO pays tax on:', ['Passenger transport by motor cabs through it', 'All goods sold on it', 'Its own advertising', 'Exports by sellers'], 0,
          'Notified services. In practice: deemed supplier.', 'c2', T2),
        Q('m5', 'A service supplier through an ECO with turnover up to ₹20 lakh:', ['Need not register', 'Must register', 'Must opt composition', 'Must pay TCS'], 0,
          'Exemption notification. In practice: special States ₹10 lakh.', 'c1', T1),
        Q('m6', 'Place of supply of OIDAR services to Indian recipients is:', ['Location of recipient', 'Location of supplier', 'Server location', 'Port of entry'], 0,
          'Section 13(12) IGST. In practice: IGST payable.', 'c4', T4),
        Q('m7', 'For OIDAR supplied to a registered Indian business, tax is paid by:', ['The recipient under reverse charge', 'The foreign supplier', 'The intermediary', 'No one'], 0,
          'RCM. In practice: ITC available.', 'c4', T4),
        Q('m8', 'Composition dealers supplying goods through ECOs:', ['Are allowed under a special procedure', 'Are prohibited', 'Must switch to regular scheme', 'Pay TCS themselves'], 0,
          'Section 148 procedure. In practice: intra-State only.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Net value', 2, 'computation', 'net value', nums=[nv]), S('s2', 'TCS', 2, 'computation', '0.5%', nums=[tcs, half])],
          ['Exclude 9(5) supplies.'], ['Including restaurant supplies.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'B2C OIDAR', 2, 'computation', 'IGST', nums=[t]), S('s2', 'B2B OIDAR', 2, 'analysis', 'reverse charge')],
          ['Define non-taxable online recipient.'], ['Making Indian individuals pay RCM.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Who is a non-taxable online recipient?', 'An unregistered person (including those registered only for TDS or Government bodies not in business) receiving OIDAR services in India.',
          [P('p1', 'Unregistered', 5, 'unregistered'), P('p2', 'OIDAR', 5, 'oidar')], 'c4'),
        V('v2', 'How does a supplier claim TCS?', 'By accepting the amount on the portal, after which it is credited to the electronic cash ledger.',
          [P('p1', 'Accept', 5, 'accept'), P('p2', 'Cash ledger', 5, 'cash ledger')], 'c3'),
        V('v3', 'When is an ECO not required to collect TCS?', 'For supplies on which it itself pays tax under section 9(5), and for exempt supplies.',
          [P('p1', 'Section 9(5)', 5, '9(5)'), P('p2', 'Exempt supplies', 5, 'exempt')], 'c3'),
        V('v4', 'Who pays tax if the ECO has no presence in India?', 'A representative in India, or an appointed person, pays on its behalf.',
          [P('p1', 'Representative', 5, 'representative'), P('p2', 'Appointed', 5, 'appoint')], 'c2'),
        V('v5', 'What happens to mismatches between GSTR-8 and the seller\'s return?', 'They are communicated and, if not rectified, added to the seller\'s output liability.',
          [P('p1', 'Communicated', 5, 'communicat'), P('p2', 'Added to liability', 5, 'added')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'StayEasy app', 'difficulty': 'core',
              'case': 'StayEasy, a booking app, lists rooms of unregistered homestay owners in Goa. Bookings of ₹30,00,000 (taxable at 5% without ITC for this example) were made in a month.',
              'mcqs': [
                  M('k1a', 'Who pays GST on the stays?', ['StayEasy under section 9(5)', 'The homestay owners', 'The guests', 'No one'], 0,
                    'Accommodation notified. In practice: owners unregistered.', 'core', topic=T2),
                  M('k1b', 'GST payable (₹):', ['1,50,000', '5,40,000', '15,000', '3,00,000'], 0,
                    '5% × 30 lakh. In practice: invoice by ECO.', 'core', check=150000, topic=T2),
                  M('k1c', 'Is TCS collected on these bookings?', ['No, section 9(5) supplies are excluded', 'Yes at 0.5%', 'Yes at 1%', 'Only inter-State'], 0,
                    'Explanation to section 52. In practice: avoid double levy.', 'core', topic=T3),
                  M('k1d', 'Must StayEasy register?', ['Yes, irrespective of turnover', 'Only above ₹20 lakh', 'No', 'Only in Goa if office exists'], 0,
                    'Section 24. In practice: in each State as required.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch12', 1, 'Electronic Commerce Transactions',
                ['Apply registration rules for ECOs and sellers.',
                 'Apply ECO liability under section 9(5).',
                 'Compute TCS under section 52.',
                 'Apply OIDAR provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ch11-u01'],
                 'exam_tip': 'First decide whether the supply is under section 9(5); if so, no TCS.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['ECO registration compulsory; seller exemptions.', 'Section 9(5): cabs, accommodation, housekeeping, restaurants.', 'Section 52: TCS 0.5% on net value; GSTR-8 by 10th.',
                             'OIDAR: POS recipient; foreign supplier registers for B2C; RCM for B2B.'],
                 'remember': ['Returns reduce net value for TCS.'],
                 'traps': ['Collecting TCS on section 9(5) supplies.']},
                [('ECO liability', 'Section 9(5)'), ('TCS', 'Section 52'), ('OIDAR', 'IGST section 14')],
                viva, cases)
