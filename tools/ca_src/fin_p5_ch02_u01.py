"""CA Final · Paper 5 · Chapter 2 Charge of GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch02-u01'
T1 = 'Levy and rates of GST'
T2 = 'Reverse charge'
T3 = 'Tax on supplies through e-commerce operators'
T4 = 'Composition levy'


def build():
    ck = Checks()
    t = ck.add('9000000*0.01', 'Composition tax on taxable turnover at 1% (₹)')
    r = ck.add('8000000*0.05', 'Composition tax for a restaurant at 5% (₹)')
    i1 = {'id': 'i1', 'title': 'Composition levy', 'difficulty': 'core', 'minutes': 6,
          'q': '(a) Kishan Traders in Rajasthan had turnover of ₹1.2 crore last year and opts for composition. This year its turnover of taxable goods is ₹90,00,000 and exempt goods ₹10,00,000. (b) A restaurant (not serving alcohol) under composition has turnover of ₹80,00,000. Compute composition tax.',
          'solution': [table(['Case', 'Working', '₹'], [
              ['(a) Trader', '1% (0.5% CGST + 0.5% SGST) on taxable supplies', inr(t)],
              ['(b) Restaurant', '5% (2.5% + 2.5%) on turnover', inr(r)]], title='Section 10')],
          'checks': list(ck)}

    c2 = Checks()
    g = c2.add('100000*0.05', 'GST on GTA service under reverse charge at 5% (₹)')
    d = c2.add('50000*0.18', 'GST on director\'s sitting fee under reverse charge at 18% (₹)')
    i2 = {'id': 'i2', 'title': 'Who pays the tax?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Vardhan Steel Ltd (registered) receives: (a) goods transport by a GTA for freight of ₹1,00,000, where the GTA has not opted to pay tax itself; (b) sitting fees of ₹50,000 paid to an independent director; (c) legal services from a senior advocate. Determine who pays GST and compute (a) and (b).',
          'solution': [table(['Service', 'Liability', '₹'], [
              ['(a) GTA', 'Recipient under reverse charge at 5%', inr(g)],
              ['(b) Director', 'Company under reverse charge at 18%', inr(d)],
              ['(c) Advocate', 'Business entity recipient under reverse charge', '—']], title='Section 9(3)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 9(1) of the CGST Act levies CGST on intra-State supplies (and the SGST/UTGST Acts levy the State or UT share); section 5 of the IGST Act levies IGST on inter-State supplies and imports — except alcoholic liquor for human consumption. Petroleum crude, diesel, petrol, natural gas and ATF are within GST but taxable only from a notified date.',
            'The value is determined under section 15 and tax is collected at notified rates. After the 2025 rationalisation, the main goods rates are 5% and 18%, with 40% for specified luxury and sin goods and lower rates (0.25%, 1.5%, 3%) for specific items; most services are at 5% or 18%, with 40% for items like betting, casinos and online money gaming.',
            'Supplies of specified actionable claims are taxed at the highest rate on the full face value.'],
          'IGST for inter-State; CGST + SGST for intra-State.',
          'A ₹1,000 supply at 18% within a State carries ₹90 CGST and ₹90 SGST.'),
        C('c2', T2, [
            'Section 9(3) makes the recipient liable for notified services and goods — e.g. GTA services (where GTA charges 5%), legal services by advocates to business entities, sponsorship to bodies corporate or firms, services by directors to companies, insurance agents\' services to insurers, recovery agents, security services by non-body-corporate to registered persons, renting of residential dwellings to registered persons, and specified goods like cashew nuts and raw cotton from agriculturists.',
            'Section 9(4) lets the Government notify specified categories of supplies received by specified registered persons (e.g. promoters) from unregistered suppliers to be taxed under reverse charge.',
            'The recipient pays tax in cash (ITC cannot discharge RCM liability), can then claim ITC if otherwise eligible, and must issue a self-invoice where the supplier is unregistered.'],
          'Under RCM the buyer, not the seller, pays.',
          'A company paying ₹50,000 sitting fees owes ₹9,000 GST under RCM.'),
        C('c3', T3, [
            'Section 9(5) makes the electronic commerce operator liable to pay tax on notified services supplied through it, as if it were the supplier — passenger transport by cabs and motorcycles, hotel and similar accommodation, housekeeping services, and restaurant services supplied through ECOs.',
            'Where the ECO has no physical presence in the taxable territory, its representative or a person appointed by it pays the tax.',
            'Supplies of specified actionable claims are deemed supplied by the operator who owns, operates or manages the platform.'],
          'Platforms pay tax on certain services they enable.',
          'A food delivery app pays GST on restaurant supplies made through it.'),
        C('c4', T4, [
            'Section 10 composition: registered persons with turnover up to ₹1.5 crore in the previous year (₹75 lakh in specified special category States) may pay tax at 1% for manufacturers (other than notified goods), 5% for restaurant services, and 1% of taxable supplies for others — with incidental services up to 10% of turnover or ₹5 lakh allowed. Section 10(2A) gives a 6% scheme to service providers with turnover up to ₹50 lakh.',
            'Composition dealers cannot make inter-State outward supplies, supply through ECOs that collect TCS, supply non-taxable goods or manufacture notified goods; they cannot collect tax or claim ITC, and must issue a bill of supply and mention "composition taxable person".',
            'Recipients of their supplies cannot claim ITC; composition dealers pay reverse charge tax at normal rates. Eligibility is tested on aggregate turnover across PAN.'],
          'Small businesses can pay a flat percentage, with restrictions.',
          'A trader with ₹90 lakh taxable turnover pays ₹90,000 under composition.'),
    ]

    jobs = [{'id': 'j1', 'title': 'RCM checklist', 'role': 'GST accountant',
             'situation': 'A manufacturer wants to ensure all reverse-charge liabilities are paid.',
             'steps': ['List payments to GTAs, advocates, directors and agents.', 'Check unregistered supplier cases.', 'Pay tax in cash and self-invoice.', 'Claim ITC in the same return where eligible.'],
             'takeaway': 'RCM must be paid in cash before ITC can be taken.'}]

    mcqs = [
        Q('m1', 'IGST is levied on:', ['Inter-State supplies and imports', 'Intra-State supplies', 'Exports only', 'Alcoholic liquor'], 0,
          'Section 5 IGST Act. In practice: place of supply decides.', 'c1', T1),
        Q('m2', 'Which is outside GST levy?', ['Alcoholic liquor for human consumption', 'Petrol', 'Tobacco', 'Online money gaming'], 0,
          'Excluded from levy. In practice: State excise.', 'c1', T1),
        Q('m3', 'Liability for GST on sitting fees paid to a director lies on:', ['The company', 'The director', 'Both equally', 'Nobody'], 0,
          'Reverse charge. In practice: pay in cash.', 'c2', T2),
        Q('m4', 'RCM liability can be paid using:', ['Cash only', 'ITC only', 'ITC or cash', 'Credit notes'], 0,
          'Electronic cash ledger. In practice: then claim ITC.', 'c2', T2),
        Q('m5', 'Under section 9(5), the ECO pays tax on:', ['Restaurant services supplied through it', 'All goods sold on it', 'Its own commission only', 'Exports'], 0,
          'Notified services. In practice: cab, hotel, housekeeping too.', 'c3', T3),
        Q('m6', 'Composition turnover limit in most States is:', ['One crore fifty lakh rupees', 'Seventy-five lakh rupees', 'Fifty lakh rupees', 'Two crore rupees'], 0,
          'Section 10. In practice: special States ₹75 lakh.', 'c4', T4),
        Q('m7', 'Composition rate for restaurant services is:', ['Five percent', 'One percent', 'Six percent', 'Eighteen percent'], 0,
          'Section 10. In practice: no ITC.', 'c4', T4),
        Q('m8', 'A composition dealer can:', ['Make intra-State supplies', 'Make inter-State outward supplies', 'Collect tax from customers', 'Claim ITC'], 0,
          'Restrictions. In practice: bill of supply.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Trader', 2, 'computation', 'taxable', nums=[t]), S('s2', 'Restaurant', 2, 'computation', 'restaurant', nums=[r])],
          ['State eligibility.'], ['Including exempt supplies in base.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'GTA', 2, 'computation', 'GTA', nums=[g]), S('s2', 'Director and advocate', 3, 'analysis', 'reverse charge', nums=[d])],
          ['Name the liable person.'], ['Charging forward on director fees.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'When is GST on petrol leviable?', 'From a date to be notified by the Government on the Council\'s recommendation.',
          [P('p1', 'Notified date', 5, 'notified'), P('p2', 'Council', 5, 'council')], 'c1'),
        V('v2', 'What does section 9(4) provide?', 'Notified categories of supplies from unregistered suppliers to specified registered persons are taxed under reverse charge.',
          [P('p1', 'Unregistered suppliers', 5, 'unregistered'), P('p2', 'Reverse charge', 5, 'reverse charge')], 'c2'),
        V('v3', 'Who pays tax if an ECO has no presence in India?', 'Its representative in India or a person it appoints to pay tax.',
          [P('p1', 'Representative', 5, 'representative'), P('p2', 'Appoints', 5, 'appoint')], 'c3'),
        V('v4', 'What is the 6% composition scheme?', 'An option for suppliers of services or mixed suppliers with turnover up to ₹50 lakh to pay tax at 6%.',
          [P('p1', 'Fifty lakh', 5, '50 lakh'), P('p2', 'Six percent', 5, '6%')], 'c4'),
        V('v5', 'What document does a composition dealer issue?', 'A bill of supply, carrying the words composition taxable person.',
          [P('p1', 'Bill of supply', 5, 'bill of supply'), P('p2', 'Composition taxable person', 5, 'composition taxable person')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'CityRide app', 'difficulty': 'core',
              'case': 'CityRide, an app-based platform, connects unregistered drivers with passengers in Pune. In October 2026 rides worth ₹40,00,000 were booked through it at 5% GST.',
              'mcqs': [
                  M('k1a', 'Who pays GST on the rides?', ['CityRide as e-commerce operator', 'The drivers', 'The passengers', 'No one'], 0,
                    'Section 9(5). In practice: deemed supplier.', 'core', topic=T3),
                  M('k1b', 'GST payable on rides (₹):', ['2,00,000', '7,20,000', '40,000', '4,00,000'], 0,
                    '5% × 40 lakh. In practice: monthly return.', 'core', check=200000, topic=T3),
                  M('k1c', 'Do the drivers need to register only for these rides?', ['No, the operator is liable', 'Yes, always', 'Only above ₹20 lakh', 'Only if inter-State'], 0,
                    'Deemed supplier. In practice: exemption from registration.', 'core', topic=T3),
                  M('k1d', 'CityRide\'s own commission is taxed:', ['Separately as its own supply', 'Not at all', 'Under composition', 'Only if exported'], 0,
                    'Platform service. In practice: forward charge.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch02', 1, 'Charge of GST',
                ['Explain the levy of CGST, SGST/UTGST and IGST.',
                 'Apply reverse charge provisions.',
                 'Apply tax liability of e-commerce operators.',
                 'Apply the composition levy.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch01-u01'],
                 'exam_tip': 'First decide who is liable (supplier, recipient, or ECO), then the rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 9(1) CGST; IGST section 5; alcohol excluded; petroleum from notified date.', 'Rates mainly 5%/18%/40%.', 'Section 9(3)/(4) RCM; pay in cash.',
                             'Section 9(5) ECO liability.', 'Section 10: ₹1.5 crore; 1%/5%/1%; 6% scheme ₹50 lakh.'],
                 'remember': ['Composition dealers cannot make inter-State outward supplies.'],
                 'traps': ['Using ITC to pay RCM.']},
                [('Levy', 'Section 9'), ('RCM', 'Section 9(3)/(4)'), ('ECO', 'Section 9(5)'), ('Composition', 'Section 10')],
                viva, cases)
