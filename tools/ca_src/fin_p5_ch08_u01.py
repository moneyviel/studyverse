"""CA Final · Paper 5 · Chapter 8 Registration.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch08-u01'
T1 = 'Threshold-based registration'
T2 = 'Compulsory registration and persons not liable'
T3 = 'Procedure, deemed approval and special categories'
T4 = 'Amendment, cancellation and revocation'


def build():
    ck = Checks()
    a = ck.add('3500000+2000000', 'Aggregate turnover of Nirmal (₹)')
    i1 = {'id': 'i1', 'title': 'Is registration required?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Examine registration liability for 2026-27: (a) Nirmal in Uttar Pradesh supplies taxable goods worth ₹35 lakh and taxable services worth ₹20 lakh; (b) Leela in Gujarat exclusively supplies taxable goods worth ₹38 lakh; (c) Tenzin in Mizoram supplies services worth ₹12 lakh; (d) Rahul in Delhi supplies goods worth ₹5 lakh, all inter-State.',
          'solution': [table(['Person', 'Analysis', 'Liable?'], [
              ['Nirmal', f'Goods and services — limit ₹20 lakh; turnover ₹{inr(a)}', 'Yes'],
              ['Leela', 'Exclusively goods — limit ₹40 lakh; ₹38 lakh', 'No'],
              ['Tenzin', 'Special category State — ₹10 lakh; ₹12 lakh', 'Yes'],
              ['Rahul', 'Inter-State taxable goods — compulsory under section 24', 'Yes']], title='Sections 22 and 24')],
          'checks': list(ck)}

    c2 = Checks()
    d = c2.add('90+180', 'Maximum days available to seek revocation with extension')
    i2 = {'id': 'i2', 'title': 'Casual taxable person and revocation', 'difficulty': 'moderate', 'minutes': 6,
          'q': '(a) A Mumbai jeweller plans a 10-day exhibition in Jaipur. What must it do? (b) Kiran\'s registration was cancelled by the officer on 10 January 2027 for non-filing of returns. What is the time limit to apply for revocation?',
          'solution': [table(['Case', 'Rule', 'Result'], [
              ['(a) Casual taxable person', 'Apply at least 5 days before business; pay advance tax on estimated liability; validity up to 90 days', 'Register in Rajasthan'],
              ['(b) Revocation', f'90 days from service of order, extendable by up to 180 days (total {d} days)', 'File returns and pay dues first']], title='Sections 24, 27 and 30')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 22: every supplier must register in each State or UT from which it makes taxable supplies if aggregate turnover in a financial year exceeds ₹20 lakh (₹10 lakh in special category States — Manipur, Mizoram, Nagaland and Tripura).',
            'Suppliers exclusively of goods may enjoy ₹40 lakh in most States (not in Telangana, Puducherry and some north-eastern and hill States, where ₹20 lakh applies), provided they do not supply ice cream, pan masala or tobacco and are not required to register compulsorily.',
            'Aggregate turnover is computed on an all-India PAN basis and includes taxable, exempt, export and inter-State supplies but excludes inward RCM supplies, taxes and supplies of non-taxable goods like alcohol; supplies of an agent on behalf of principals are included in the agent\'s turnover.'],
          'Turnover thresholds: ₹20 lakh generally, ₹40 lakh for goods-only, ₹10 lakh in special States.',
          'A UP supplier of goods and services with ₹55 lakh turnover must register.'),
        C('c2', T2, [
            'Section 24 requires registration irrespective of turnover for: inter-State taxable suppliers of goods (with exemptions for certain handicrafts and small sellers via ECOs); casual taxable persons; persons liable under reverse charge; ECOs liable under section 9(5); non-resident taxable persons; TDS deductors and TCS collectors; agents and ISDs; suppliers through ECOs that collect TCS (with exceptions for small service suppliers and notified goods suppliers); OIDAR suppliers from abroad to unregistered persons; and others notified.',
            'Section 23 excludes persons engaged only in exempt or non-taxable supplies, agriculturists for produce from cultivation, and persons notified (e.g. suppliers liable only under RCM as recipients may still need to register).',
            'Voluntary registration is allowed under section 25(3), with all obligations of a registered person.'],
          'Some activities need registration from the first rupee.',
          'A Delhi trader making ₹5 lakh of inter-State sales must register.'),
        C('c3', T3, [
            'Section 25: apply within 30 days of becoming liable (casual and non-resident taxable persons at least 5 days before starting business) in Form GST REG-01, with PAN (except non-residents) and Aadhaar authentication; one registration per State, with separate registrations allowed for multiple places.',
            'If Aadhaar authentication is done and no notice is issued, the application is deemed approved within 7 working days; with biometric verification or physical verification, deemed approval comes within 30 days if no notice is issued. Registration is effective from the date of liability if applied within 30 days.',
            'Casual and non-resident taxable persons get registration valid up to 90 days (extendable by 90 days) and must deposit advance tax equal to estimated liability. A Unique Identity Number is given to UN bodies and embassies (section 25(9)).'],
          'Apply within 30 days; Aadhaar authentication speeds approval.',
          'An exhibitor from another State registers as a casual taxable person 5 days before the fair.'),
        C('c4', T4, [
            'Section 28: core field changes (name, place of business, partners) need approval within 15 days; non-core fields are updated online.',
            'Section 29: cancellation may be sought by the person (business discontinued, transferred, change of constitution, no longer liable) or ordered by the officer for contravention, non-filing of returns (composition: beyond three months of the annual return due date; others: specified continuous periods), failure to start business within six months of voluntary registration, or registration obtained by fraud. Suspension may apply pending cancellation. On cancellation, tax equal to ITC on stock and capital goods (or output tax, if higher) must be paid.',
            'Section 30: revocation of an officer-initiated cancellation can be sought within 90 days of service of the order, extendable by up to 180 days, after filing pending returns and paying dues.'],
          'Cancellation has a cost; revocation has strict time limits.',
          'A cancelled dealer has up to 270 days in all to seek revocation.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Registration health check', 'role': 'GST consultant',
             'situation': 'A start-up selling online across India asks if and where to register.',
             'steps': ['Compute aggregate turnover on PAN basis.', 'Check section 24 triggers like inter-State supply and ECO TCS.', 'Register in each State of supply.', 'Plan Aadhaar authentication for fast approval.'],
             'takeaway': 'Section 24 often overrides turnover thresholds.'}]

    mcqs = [
        Q('m1', 'Threshold for a supplier exclusively of goods in Maharashtra is:', ['Forty lakh rupees', 'Twenty lakh rupees', 'Ten lakh rupees', 'Fifty lakh rupees'], 0,
          'Notification under section 22. In practice: conditions apply.', 'c1', T1),
        Q('m2', 'Aggregate turnover is computed on:', ['All-India PAN basis', 'Per State basis', 'Per branch basis', 'Per invoice basis'], 0,
          'Section 2(6). In practice: include exempt supplies.', 'c1', T1),
        Q('m3', 'A casual taxable person must apply for registration at least:', ['Five days before starting business', 'Thirty days before', 'On the first day', 'Within seven days after'], 0,
          'Section 25(1). In practice: advance tax deposit.', 'c3', T3),
        Q('m4', 'Registration of a casual taxable person is valid up to:', ['Ninety days, extendable by ninety days', 'One year', 'Thirty days', 'One hundred eighty days only'], 0,
          'Section 27. In practice: extend before expiry.', 'c3', T3),
        Q('m5', 'Which person is not liable to register?', ['An agriculturist supplying own produce', 'An inter-State supplier of taxable goods', 'An ISD', 'A non-resident taxable person'], 0,
          'Section 23. In practice: only cultivation produce.', 'c2', T2),
        Q('m6', 'With Aadhaar authentication and no notice, registration is deemed approved within:', ['Seven working days', 'Thirty days', 'Three days', 'Fifteen days'], 0,
          'Rule 9. In practice: else 30 days.', 'c3', T3),
        Q('m7', 'Revocation of cancellation must be sought within ninety days, extendable by up to:', ['One hundred eighty days', 'Thirty days', 'Ninety days', 'One year'], 0,
          'Section 30. In practice: file pending returns.', 'c4', T4),
        Q('m8', 'Voluntary registrants who do not start business within six months may face:', ['Cancellation', 'Penalty only', 'Nothing', 'Revocation'], 0,
          'Section 29(2)(d). In practice: officer action.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Thresholds', 3, 'analysis', '20 lakh', nums=[a]), S('s2', 'Compulsory registration', 3, 'analysis', 'section 24')],
          ['State applicable limit.'], ['Applying ₹40 lakh to mixed suppliers.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Casual taxable person', 2, 'analysis', 'advance tax'), S('s2', 'Revocation', 2, 'analysis', '90 days', nums=[d])],
          ['Cite time limits.'], ['Applying after expiry.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Which States have a ₹10 lakh threshold?', 'Manipur, Mizoram, Nagaland and Tripura.',
          [P('p1', 'Manipur and Mizoram', 5, 'manipur'), P('p2', 'Nagaland and Tripura', 5, 'tripura')], 'c1'),
        V('v2', 'A trader crossed the threshold on 1 June and applied on 20 June. From when is the registration effective?', 'From 1 June, the date of liability, because the application was within thirty days.',
          [P('p1', 'Date of liability', 5, 'liability'), P('p2', 'Thirty days', 5, 'thirty days')], 'c3'),
        V('v3', 'What tax is payable on cancellation of registration?', 'An amount equal to ITC on stock, semi-finished and finished goods and capital goods, or output tax on them, whichever is higher.',
          [P('p1', 'ITC on stock', 5, 'stock'), P('p2', 'Whichever higher', 5, 'higher')], 'c4'),
        V('v4', 'Who receives a Unique Identity Number?', 'UN bodies, embassies and other notified persons for refund of taxes on inward supplies.',
          [P('p1', 'UN bodies', 5, 'un bodies'), P('p2', 'Embassies', 5, 'embass')], 'c3'),
        V('v5', 'Is a person making only exempt supplies liable to register?', 'Such a person falls outside the liability under section 23.',
          [P('p1', 'Outside liability', 5, 'outside'), P('p2', 'Section 23', 5, '23')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Asha Crafts', 'difficulty': 'core',
              'case': 'Asha Crafts, Rajasthan, sells handmade décor only within the State through its shop (₹18 lakh) and also through an e-commerce operator that collects TCS (₹4 lakh, intra-State).',
              'mcqs': [
                  M('k1a', 'Aggregate turnover (₹ lakh):', ['22', '18', '4', '40'], 0,
                    '18 + 4. In practice: PAN basis.', 'core', check=22, topic=T1),
                  M('k1b', 'Is Asha liable on threshold basis if it supplies only goods (limit ₹40 lakh)?', ['No', 'Yes', 'Only for ECO sales', 'Only above ₹20 lakh'], 0,
                    'Below ₹40 lakh. In practice: check State.', 'core', topic=T1),
                  M('k1c', 'Selling through an ECO that collects TCS generally triggers:', ['Compulsory registration unless exempted', 'No registration', 'Composition only', 'Cancellation'], 0,
                    'Section 24(ix). In practice: notified exemptions exist.', 'core', topic=T2),
                  M('k1d', 'Days within which to apply after becoming liable:', ['30', '90', '5', '180'], 0,
                    'Section 25. In practice: online REG-01.', 'core', check=30, topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch08', 1, 'Registration',
                ['Determine threshold-based registration liability.',
                 'Identify compulsory registration and exempt persons.',
                 'Apply procedure, deemed approval and special categories.',
                 'Apply amendment, cancellation and revocation provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch07-u01'],
                 'exam_tip': 'Check section 24 first; if not triggered, test the threshold.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 22: ₹20 lakh / ₹40 lakh / ₹10 lakh.', 'Section 24 compulsory registration.', 'Section 23 persons not liable.',
                             'Section 25: 30 days; CTP/NRTP 5 days before; deemed approval 7 working days.', 'Sections 29–30: cancellation; revocation 90 + 180 days.'],
                 'remember': ['CTP/NRTP: 90-day validity, advance tax.'],
                 'traps': ['Using ₹40 lakh for suppliers of services.']},
                [('Threshold', 'Section 22'), ('Not liable', 'Section 23'), ('Compulsory', 'Section 24'), ('Cancellation', 'Section 29'), ('Revocation', 'Section 30')],
                viva, cases)
