"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 9 Registration.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch09-u01'
T1 = 'Threshold and aggregate turnover (s. 22)'
T2 = 'Persons not liable (s. 23) and compulsory registration (s. 24)'
T3 = 'Procedure, special persons and effective date (ss. 25–27)'
T4 = 'Amendment, cancellation and revocation (ss. 28–30)'


def build():
    ck = Checks()
    at = ck.add('1200000+300000+250000+400000', 'Aggregate turnover')
    i1 = {'id': 'i1', 'title': 'Is registration needed?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Mr. Joseph of Kochi, Kerala, supplies services. In the year: taxable intra-State services ₹12 lakh; exempt services ₹3 lakh; export of services ₹2.5 lakh; taxable services from his Coimbatore (Tamil Nadu) branch under the same PAN ₹4 lakh; inward supplies on which he paid tax under reverse charge ₹1.5 lakh; GST collected ₹2.88 lakh. Is he liable to register?',
          'solution': [table(['Item', 'Include?', '₹'], [
              ['Taxable intra-State services', 'Yes', inr(1200000)],
              ['Exempt services', 'Yes', inr(300000)],
              ['Exports', 'Yes', inr(250000)],
              ['Supplies from Coimbatore branch (same PAN)', 'Yes — all-India basis', inr(400000)],
              ['Inward supplies under reverse charge', 'No', '—'],
              ['GST', 'No', '—'],
              ['Aggregate turnover', '', inr(at)]], title='Section 2(6) and section 22'),
              p('₹21.5 lakh exceeds ₹20 lakh, so he must register in Kerala and in Tamil Nadu (each State where he makes taxable supplies) within 30 days.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Compulsory or not?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Turnover of each person below is ₹8 lakh. Who must register? (a) A trader of garments making one inter-State sale of goods; (b) a person selling only handicraft goods inter-State; (c) a company paying reverse charge on legal fees; (d) a farmer selling his own wheat; (e) a person who comes to a Mumbai trade fair for 10 days and sells goods there.',
          'solution': [table(['Case', 'Register?', 'Reason'], [
              ['(a)', 'Yes', 's. 24: inter-State taxable supply of goods'],
              ['(b)', 'No (up to threshold)', 'Notified exemption for inter-State handicraft suppliers within the threshold'],
              ['(c)', 'Yes', 's. 24: persons liable under reverse charge'],
              ['(d)', 'No', 's. 23: agriculturist supplying produce from cultivation'],
              ['(e)', 'Yes', 's. 24: casual taxable person']], title='Sections 23 and 24')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 22: every supplier making taxable supplies must register in the State or UT from where he makes them if aggregate turnover in a financial year exceeds ₹20 lakh (₹10 lakh in Manipur, Mizoram, Nagaland and Tripura).',
            'For persons exclusively supplying goods, the limit is ₹40 lakh in most States (excluding a few special category States and notified goods such as ice cream, pan masala and tobacco).',
            'Aggregate turnover (s. 2(6)): taxable supplies, exempt supplies, exports and inter-State supplies of all persons with the same PAN across India — excluding inward supplies taxed under reverse charge and the GST itself. A person taking over a business of a registered person is liable from the date of transfer.'],
          'The threshold is tested on all-India turnover under one PAN, but registration is State-wise.',
          'A consultant with ₹15 lakh taxable and ₹8 lakh exempt services must register — exempt turnover counts.'),
        C('c2', T2, [
            'Section 23: not liable — persons exclusively supplying non-taxable or wholly exempt goods or services; agriculturists supplying produce from cultivation; and notified categories (persons making only reverse-charge supplies, inter-State service suppliers within the threshold, inter-State handicraft suppliers within the threshold, small suppliers of goods through e-commerce subject to conditions).',
            'Section 24: registration irrespective of turnover for inter-State taxable supply of goods; casual taxable persons; persons liable under reverse charge; ECOs liable under section 9(5); non-resident taxable persons; TDS deductors under section 51; agents supplying on behalf of others; input service distributors; persons supplying through ECOs that collect TCS (subject to exemptions); every ECO required to collect TCS; and suppliers of online information and database access services from outside India to unregistered persons in India.'],
          'Some activities are risky enough that the law demands registration from the first rupee.',
          'A ₹5 lakh trader who sells goods once to a buyer in another State must register.'),
        C('c3', T3, [
            'Section 25: apply within 30 days of becoming liable, in each State or UT where liable; a coastal supplier registers in the nearest State. A person may take separate registrations for each place of business in a State. Registration is PAN-based, with Aadhaar authentication or biometric verification. Voluntary registration is permitted; UN bodies and embassies get a Unique Identity Number.',
            'Casual and non-resident taxable persons apply at least 5 days before starting business; registration is valid for the period stated or 90 days (extendable by 90 days), and an advance deposit of estimated tax is required.',
            'Section 27 and Rule 10: effective date is the date of liability if applied within 30 days; otherwise the date of grant. A simplified, faster registration (Rule 14A) is available to small suppliers whose monthly output tax does not exceed ₹2.5 lakh.'],
          'Register within 30 days and the registration reaches back to the day liability began.',
          'Liable on 1 May, applied on 20 May, granted on 1 June: effective date is 1 May.'),
        C('c4', T4, [
            'Section 28: core fields (legal name, address of principal place, additional places, partners or directors) need the officer\'s approval; other fields are amended online; a change in PAN needs fresh registration.',
            'Section 29: the person may seek cancellation on discontinuance, transfer of business, change in constitution or no longer being liable. The officer may cancel for contravention, non-filing of returns (six continuous months; a financial year plus three months for composition), not starting business within six months of voluntary registration, or fraud. Cancellation can be retrospective; tax on stock and capital goods (ITC or tax on transaction value, whichever is higher) must be paid.',
            'Section 30: revocation may be sought within 90 days of the cancellation order (extendable up to 180 days more) after filing pending returns and paying dues.'],
          'Registration can be changed, surrendered or taken away — and, if taken away, often restored on compliance.',
          'A trader whose registration was cancelled for non-filing can apply for revocation after filing all returns.'),
    ]

    jobs = [{'id': 'j1', 'title': 'New client registration', 'role': 'Article assistant',
             'situation': 'A start-up expects to cross ₹20 lakh in its first year and will sell online across India.',
             'steps': ['Check section 24 triggers such as inter-State goods and ECO sales.', 'Collect PAN, Aadhaar, address proof and bank details.', 'Apply in each State with a place of business.', 'Calendar the effective date for invoicing.'],
             'takeaway': 'Section 24 often makes registration necessary long before the turnover threshold.'}]

    mcqs = [
        Q('m1', 'Registration threshold for a service provider in Gujarat:', ['₹20 lakh', '₹10 lakh', '₹40 lakh', '₹1.5 crore'], 0,
          'Service providers outside the four States with a ₹10 lakh limit have a ₹20 lakh threshold. ₹40 lakh is for exclusive goods suppliers. In practice: count all-India turnover under the PAN.', 'c1', T1, check=20),
        Q('m2', 'Aggregate turnover excludes:', ['Inward supplies on which tax is paid under reverse charge', 'Exempt supplies', 'Exports', 'Inter-State supplies to own branches'], 0,
          'Reverse charge inward supplies and GST are excluded; exempt, export and inter-branch supplies are included. In practice: watch exempt turnover.', 'c1', T1),
        Q('m3', 'Which person is NOT required to register?', ['An agriculturist selling produce from his own cultivation', 'A casual taxable person', 'An e-commerce operator collecting TCS', 'A TDS deductor'], 0,
          'Section 23 exempts agriculturists for produce from cultivation; the others are in section 24. In practice: a farmer who trades in others\' produce is not covered.', 'c2', T2),
        Q('m4', 'Registration must be applied for within how many days of becoming liable?', ['30 days', '60 days', '15 days', '90 days'], 0,
          'Section 25(1) gives 30 days; casual and non-resident persons apply 5 days before business. In practice: late application shifts the effective date.', 'c3', T3, check=30),
        Q('m5', 'A casual taxable person\'s registration is valid for:', ['The period specified or 90 days, extendable by 90 days', '1 year', '30 days', 'Unlimited'], 0,
          'Section 27 limits it to the period sought or 90 days from the effective date, with a further 90 days on request. In practice: deposit estimated tax in advance.', 'c3', T3),
        Q('m6', 'Applied 45 days after becoming liable; effective date of registration is:', ['Date of grant', 'Date of liability', 'Date of application', 'First day of the next month'], 0,
          'Only an application within 30 days relates back to the date of liability; otherwise the date of grant applies. In practice: interest and penalty may arise for the gap.', 'c3', T3),
        Q('m7', 'Which change needs the proper officer\'s approval?', ['Legal name of the business', 'Mobile number', 'E-mail address', 'Bank account details'], 0,
          'Core fields — legal name, principal place of business and additional places, partners or directors — need approval. In practice: others are self-amended.', 'c4', T4),
        Q('m8', 'Revocation of cancellation can be sought within:', ['90 days of the order, extendable', '30 days, not extendable', '1 year', '6 months only'], 0,
          'Section 30 and Rule 23 allow 90 days, which can be extended by up to 180 days by specified authorities. In practice: file all pending returns first.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Inclusions', 2, 'concept', 'exempt|export'), S('s2', 'Exclusions', 1, 'concept', 'reverse charge'), S('s3', 'Conclusion', 1, 'computation', '20 lakh', nums=[at])],
          ['Use all-India turnover.'], ['Excluding exempt services.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Inter-State goods', 1, 'concept', 'inter-state'), S('s2', 'Handicrafts', 1, 'concept', 'handicraft'), S('s3', 'RCM', 1, 'concept', 'reverse'),
           S('s4', 'Agriculturist', 1, 'concept', 'agricultur'), S('s5', 'Casual', 1, 'concept', 'casual')],
          ['Quote the section.'], ['Applying the threshold to section 24 cases.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is aggregate turnover?', 'The value of all taxable, exempt, export and inter-State supplies of persons with the same PAN across India, excluding reverse charge inward supplies and taxes.',
          [P('p1', 'Inclusions', 5, 'exempt|export'), P('p2', 'Same PAN', 5, 'pan')], 'c1'),
        V('v2', 'Name three section 24 cases.', 'Inter-State taxable supply of goods, casual taxable persons and persons liable under reverse charge, among others such as TDS deductors and ECOs.',
          [P('p1', 'Inter-State goods', 5, 'inter-state'), P('p2', 'Others', 5, 'casual|reverse|tds|e-commerce')], 'c2'),
        V('v3', 'When does registration take effect?', 'From the date of liability if applied within 30 days; otherwise from the date of grant.',
          [P('p1', 'Within 30 days', 6, '30 days'), P('p2', 'Date of grant', 4, 'grant')], 'c3'),
        V('v4', 'Can a person hold more than one registration in a State?', 'Yes, separate registrations may be obtained for each place of business in the same State.',
          [P('p1', 'Allowed', 5, 'yes|separate'), P('p2', 'Place of business', 5, 'place of business')], 'c3'),
        V('v5', 'What must be paid on cancellation?', 'An amount equal to the ITC on stock and capital goods held, or the tax on their transaction value, whichever is higher.',
          [P('p1', 'Stock and capital goods', 5, 'stock|capital goods'), P('p2', 'Higher of', 5, 'higher')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Crafts', 'difficulty': 'moderate',
              'case': 'Saffron Crafts, Jaipur, sells handmade quilts (handicraft goods) within Rajasthan and to buyers in Delhi. Turnover last year was ₹15 lakh. It plans a 7-day stall at a Goa expo and has started selling through an e-commerce site that collects TCS.',
              'mcqs': [
                  M('k1a', 'Inter-State sales of handicrafts within the threshold:', ['Do not by themselves require registration', 'Always require registration', 'Are prohibited', 'Need a TDS deduction'], 0,
                    'A notification exempts persons making inter-State supplies of handicraft goods from compulsory registration up to the threshold. In practice: an e-way bill may still be needed.', 'moderate', topic=T2),
                  M('k1b', 'If Saffron also sold machine-made carpets (not handicrafts) at the Goa stall, it must:', ['Register as a casual taxable person in Goa', 'Use its Rajasthan registration', 'Not register at all', 'Register as a non-resident taxable person'], 0,
                    'Occasional taxable supply in a State with no fixed place of business makes it a casual taxable person, who must register regardless of turnover (the handicraft relief would not cover carpets that are not handicrafts). In practice: apply 5 days before the expo.', 'hard', topic=T3),
                  M('k1c', 'Sales through an ECO collecting TCS:', ['Generally require registration under section 24', 'Never require registration', 'Need registration only above ₹40 lakh', 'Are exempt'], 0,
                    'Section 24 covers persons supplying through ECOs that collect TCS, except notified small sellers meeting conditions. In practice: check the current notification.', 'moderate', topic=T2),
                  M('k1d', 'Saffron\'s registration threshold for goods in Rajasthan:', ['₹40 lakh', '₹20 lakh', '₹10 lakh', '₹1.5 crore'], 0,
                    'Rajasthan applies the ₹40 lakh limit for exclusive goods suppliers. In practice: services would bring it to ₹20 lakh.', 'core', check=40, topic=T1),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch09', 1, 'Registration',
                ['Compute aggregate turnover and test the threshold.',
                 'Identify persons not liable and those who must register.',
                 'Apply the procedure, effective date and special persons rules.',
                 'Explain amendment, cancellation and revocation.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['int-p3-b-ch08-u01'],
                 'exam_tip': 'Check section 24 first — if it applies, the threshold is irrelevant.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Threshold ₹20 lakh (₹10 lakh in 4 States); ₹40 lakh for exclusive goods suppliers in most States.',
                             'Aggregate turnover: all-India under PAN incl. exempt and exports; excl. RCM inward and taxes.',
                             's. 23: exempt-only suppliers, agriculturists, notified; s. 24: compulsory list.',
                             'Apply in 30 days; casual/non-resident 5 days before; 90-day validity.',
                             'Cancellation s. 29; revocation within 90 days (extendable).'],
                 'remember': ['Separate registration per State; multiple per State allowed.', 'Core field changes need approval.'],
                 'traps': ['Exempt turnover counts in aggregate turnover.', 'Inter-State goods supply forces registration.']},
                [('Threshold', '₹20 lakh / ₹10 lakh'), ('Goods only', '₹40 lakh'), ('Apply within', '30 days'), ('Casual validity', '90 days')],
                viva, cases)
