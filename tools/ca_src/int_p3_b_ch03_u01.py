"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 3 Charge of GST.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch03-u01'
T1 = 'Levy under section 9(1)–(2) and section 5 of the IGST Act'
T2 = 'Reverse charge (s. 9(3) and 9(4))'
T3 = 'Tax payable by electronic commerce operators (s. 9(5))'
T4 = 'Composition levy (s. 10)'


def build():
    ck = Checks()
    tr = ck.add('9000000*1/100', 'Composition tax for a trader (1% of turnover of taxable supplies)')
    rs = ck.add('6000000*5/100', 'Composition tax for a restaurant (5%)')
    sv = ck.add('4500000*6/100', 'Section 10(2A) service provider (6%)')
    i1 = {'id': 'i1', 'title': 'Three small businesses', 'difficulty': 'core', 'minutes': 6,
          'q': 'Compute composition tax for the year (all in Gujarat, preceding-year turnover within limits): (a) a trader with turnover of taxable supplies of ₹90 lakh; (b) a restaurant (not serving alcohol) with turnover ₹60 lakh; (c) an interior designer who opted under section 10(2A), with turnover ₹45 lakh.',
          'solution': [table(['Person', 'Rate (CGST + SGST)', 'Tax ₹'], [
              ['(a) Trader', '1% of turnover of taxable supplies', inr(tr)],
              ['(b) Restaurant', '5%', inr(rs)],
              ['(c) Service provider u/s 10(2A)', '6%', inr(sv)]], title='Composition tax'),
              note('No ITC is available, tax cannot be collected from customers, and a bill of supply is issued instead of a tax invoice.')],
          'checks': list(ck)}

    ck2 = Checks()
    leg = ck2.add('100000*18/100', 'RCM on advocate\'s fees payable by the company')
    i2 = {'id': 'i2', 'title': 'Who pays the tax?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Determine who pays GST: (a) an individual advocate charges Alpha Pvt. Ltd. (turnover ₹30 crore) ₹1,00,000 (18%); (b) Mr. Dev, an independent director, gets sitting fees from Alpha; (c) a cab aggregator app books a ride by an unregistered driver; (d) an insurance agent earns commission from an insurer.',
          'solution': [table(['Case', 'Liable person', 'Basis'], [
              ['(a)', 'Alpha Pvt. Ltd. — tax ' + inr(leg), 'Reverse charge: legal services by an advocate to a business entity'],
              ['(b)', 'Alpha Pvt. Ltd.', 'Reverse charge: services by a director to the company'],
              ['(c)', 'The app (e-commerce operator)', 'Section 9(5): passenger transport through an ECO'],
              ['(d)', 'The insurer', 'Reverse charge: insurance agent to insurance business']], title='Section 9(3) and 9(5)'),
              note('Under reverse charge the recipient pays in cash; it cannot use ITC for this payment, though it may take ITC of the tax so paid if otherwise eligible.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 9(1) of the CGST Act levies central tax on all intra-State supplies of goods or services, except alcoholic liquor for human consumption, on the value under section 15, at notified rates (up to 20% CGST), collected and paid by the taxable person. Section 5(1) of the IGST Act does the same for inter-State supplies (up to 40%), with IGST on imported goods collected under the Customs Tariff Act.',
            'Section 9(2): GST on crude, petrol, high-speed diesel, natural gas and aviation turbine fuel applies only from a notified date.',
            'Ordinarily the supplier pays (forward charge). Rates are notified by HSN/SAC on the Council\'s recommendation.'],
          'The charging section names the event (supply), the base (value), the rate and the person who pays.',
          'Petrol remains outside GST until notified, though it is within the Constitutional definition.'),
        C('c2', T2, [
            'Section 9(3): for notified goods and services, the recipient pays tax instead of the supplier. Key services: goods transport agency services to specified recipients (factories, societies, registered persons, body corporates, firms, casual taxable persons) unless the GTA opts for forward charge; legal services by an advocate or firm of advocates to a business entity; arbitral tribunal services; sponsorship to a body corporate or firm; most services by Government to business entities; services by a director to the company; insurance agent to insurer; recovery agent to a bank or NBFC; author or music composer transferring copyright (unless the author opts to pay); security services by a non-body corporate to registered persons; business facilitator to banks; and renting of residential dwelling to a registered person.',
            'Renting of other immovable property by an unregistered person to a registered person (other than a composition taxpayer) is also under reverse charge.',
            'Section 9(4): for notified classes of registered persons, supplies received from unregistered suppliers of notified goods or services are under reverse charge — mainly promoters of real estate projects who fall short of the required purchases from registered persons.',
            'The recipient must pay reverse charge tax in cash, issue a self-invoice where the supplier is unregistered and a payment voucher, and may take ITC if eligible.'],
          'Reverse charge moves the tax duty to the business side of the deal where the supplier is hard to police.',
          'A small advocate need not register just because he advises companies — the companies pay the GST.'),
        C('c3', T3, [
            'Section 9(5): for notified services supplied through an e-commerce operator, the operator is liable as if it were the supplier. Notified services include passenger transport by radio taxi, motor cab, maxi cab, motor cycle and similar; accommodation in hotels, inns, guest houses and similar places (unless the supplier is registered); housekeeping such as plumbing and carpentry (unless the supplier is registered); and restaurant services.',
            'An ECO without physical presence in the taxable territory acts through a representative or appoints one.',
            'This differs from TCS under section 52, where the operator collects a small amount on supplies made by others through it.'],
          'For these services the platform steps into the supplier\'s shoes for GST.',
          'A food delivery app pays GST on restaurant food ordered through it; the restaurant does not pay again on those orders.'),
        C('c4', T4, [
            'Section 10(1): a registered person whose aggregate turnover in the preceding financial year did not exceed ₹1.5 crore (₹75 lakh in specified north-eastern and hill States) may pay a fixed percentage of turnover: manufacturers 1%, traders 1% of turnover of taxable supplies, restaurants (not serving alcohol) 5% — each split equally between CGST and SGST. Other services up to 10% of turnover or ₹5 lakh, whichever is higher, are allowed.',
            'Section 10(2A): a person who supplies services (or mixed goods and services) not eligible under section 10(1) may opt for a 6% composition if preceding-year turnover did not exceed ₹50 lakh.',
            'Not eligible: suppliers of non-taxable goods or services, inter-State outward suppliers, casual and non-resident taxable persons, suppliers of services through ECOs, and manufacturers of notified goods (ice cream, pan masala, tobacco products, aerated waters, fly-ash bricks, building stones and similar).',
            'Conditions: no ITC; no tax collected from customers; "composition taxable person" displayed at the business place and on bills of supply; all registrations under the same PAN must opt together. Exceeding the limit during the year ends the option from that day.'],
          'Composition trades input tax credit and full invoicing for low, simple tax.',
          'A sweet shop with ₹1.2 crore turnover that also caters at weddings (services up to 10%) can stay in composition.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reverse charge check-list', 'role': 'Article assistant',
             'situation': 'A company\'s expense ledger has legal, transport, director and rent payments.',
             'steps': ['Match each payment to the notified reverse charge list.', 'Check supplier and recipient conditions.', 'Pay RCM tax in cash by the due date.', 'Claim ITC in the same return if eligible.'],
             'takeaway': 'RCM tax is paid in cash, but often comes back as credit.'}]

    mcqs = [
        Q('m1', 'GST is not levied on:', ['Alcoholic liquor for human consumption', 'Tobacco', 'Medicines', 'Gold'], 0,
          'Section 9(1) excludes only alcoholic liquor for human consumption; the others are taxable at notified rates. In practice: alcohol bears State excise and VAT.', 'c1', T1),
        Q('m2', 'Legal services by an individual advocate to a business entity are taxed under:', ['Reverse charge — the business entity pays', 'Forward charge — the advocate pays', 'Exempt in all cases', 'Section 9(5)'], 0,
          'Notified under section 9(3): the business entity recipient pays. Services to individuals not in business are exempt. In practice: check the recipient\'s turnover for exemptions.', 'c2', T2),
        Q('m3', 'Services by a director to the company are taxed:', ['Under reverse charge', 'Under forward charge', 'Not at all, being Schedule III', 'Only above ₹20 lakh'], 0,
          'Non-employee director services are under reverse charge; services as an employee (whole-time director on salary) are in Schedule III. In practice: sitting fees attract RCM.', 'c2', T2),
        Q('m4', 'A registered company rents an office from an unregistered landlord. GST is payable by:', ['The company under reverse charge', 'The landlord', 'No one', 'The ECO'], 0,
          'Renting of non-residential property by an unregistered person to a registered person (other than a composition taxpayer) is under reverse charge. In practice: the company issues a self-invoice.', 'c2', T2),
        Q('m5', 'Under section 9(5), GST on hotel accommodation booked through an app is paid by the app when the hotel is:', ['Not registered', 'Registered', 'Under composition', 'Charging above ₹7,500'], 0,
          'For accommodation and housekeeping services, the ECO is liable unless the actual supplier is registered. In practice: registered hotels pay their own tax.', 'c3', T3),
        Q('m6', 'Composition turnover limit for a trader in Kerala (preceding year):', ['₹1.5 crore', '₹75 lakh', '₹50 lakh', '₹2 crore'], 0,
          'Kerala is not among the specified States with a ₹75 lakh limit, so ₹1.5 crore applies. The ₹50 lakh limit is for section 10(2A) service providers. In practice: limits are on aggregate turnover across India under the PAN.', 'c4', T4, check=1.5),
        Q('m7', 'Composition rate for a restaurant not serving alcohol:', ['5%', '1%', '6%', '2%'], 0,
          'Restaurants pay 5% (2.5% CGST + 2.5% SGST) under composition; manufacturers and traders pay 1%; section 10(2A) service providers 6%. In practice: no ITC is available.', 'c4', T4, check=5),
        Q('m8', 'Which person is NOT eligible for composition?', ['A trader making inter-State outward supplies', 'A small manufacturer of furniture', 'A restaurant', 'A trader with ₹1 crore turnover'], 0,
          'Inter-State outward supply disqualifies a person from composition. In practice: inter-State purchases are allowed.', 'c4', T4),
        Q('m9', 'A section 10(2A) service provider can opt in if preceding-year turnover did not exceed:', ['₹50 lakh', '₹1.5 crore', '₹20 lakh', '₹75 lakh'], 0,
          'Section 10(2A) is for service providers and mixed suppliers with preceding-year turnover up to ₹50 lakh, paying 6%. In practice: it also needs no inter-State outward supply.', 'c4', T4, check=50),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Trader rate', 1, 'computation', '1%', nums=[tr]), S('s2', 'Restaurant rate', 1, 'computation', '5%', nums=[rs]), S('s3', 'Service provider rate', 1, 'computation', '6%', nums=[sv])],
          ['State the rate first.'], ['Using 1% for restaurants.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Advocate RCM', 1, 'computation', 'reverse', nums=[leg]), S('s2', 'Director RCM', 1, 'concept', 'director'),
           S('s3', 'ECO liability', 1, 'concept', '9(5)|operator'), S('s4', 'Insurance agent', 1, 'concept', 'insurer')],
          ['Name the liable person.'], ['Making the cab driver liable.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is reverse charge?', 'A mechanism under which the recipient, not the supplier, is liable to pay tax on notified supplies or on supplies from unregistered persons where notified.',
          [P('p1', 'Recipient pays', 6, 'recipient'), P('p2', 'Notified', 4, 'notified')], 'c2'),
        V('v2', 'Can reverse charge tax be paid using ITC?', 'No, it must be paid in cash through the electronic cash ledger, though the recipient may then take ITC of it if eligible.',
          [P('p1', 'Cash only', 6, 'cash'), P('p2', 'ITC later', 4, 'itc|credit')], 'c2'),
        V('v3', 'Name two services covered by section 9(5).', 'Passenger transport by cab or motorcycle and restaurant services supplied through an e-commerce operator; accommodation and housekeeping too where the supplier is unregistered.',
          [P('p1', 'Transport', 5, 'transport|cab'), P('p2', 'Restaurant or other', 5, 'restaurant|accommodation|housekeeping')], 'c3'),
        V('v4', 'What is the composition limit for a manufacturer?', 'Aggregate turnover up to ₹1.5 crore in the preceding financial year, or ₹75 lakh in the specified States, with tax at 1% of turnover.',
          [P('p1', '₹1.5 crore', 6, '1.5 crore'), P('p2', 'Rate', 4, '1%')], 'c4'),
        V('v5', 'What restrictions apply to a composition taxpayer?', 'He cannot take input tax credit, cannot collect tax from customers, must issue bills of supply and must show that he is a composition taxable person.',
          [P('p1', 'No ITC', 5, 'credit|itc'), P('p2', 'No tax collection', 5, 'collect|bill of supply')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Hilltop Bakers', 'difficulty': 'moderate',
              'case': 'Hilltop Bakers of Dehradun, Uttarakhand, had preceding-year turnover of ₹1.1 crore from intra-State sales of bakery products, plus ₹6 lakh from a small catering service. It hires a goods transport agency for deliveries and rents its shop from an unregistered owner. It wants to opt for composition.',
              'mcqs': [
                  M('k1a', 'Is Hilltop eligible for composition?', ['Yes, turnover is within ₹1.5 crore and services are within 10%', 'No, because it supplies services', 'No, Uttarakhand\'s limit is ₹75 lakh', 'Only under section 10(2A)'], 0,
                    'Uttarakhand has the ₹1.5 crore limit; catering of ₹6 lakh is below 10% of turnover or ₹5 lakh, whichever is higher (10% of ₹1.16 crore = ₹11.6 lakh). In practice: watch turnover during the year.', 'moderate', topic=T4),
                  M('k1b', 'As a composition dealer, can Hilltop take ITC on ovens?', ['No', 'Yes, fully', 'Yes, 50%', 'Only for capital goods'], 0,
                    'Composition taxpayers cannot take any ITC. In practice: consider this before opting if capital purchases are large.', 'core', topic=T4),
                  M('k1c', 'Rent paid to the unregistered owner, once Hilltop is under composition:', ['Not taxed under reverse charge in Hilltop\'s hands', 'Taxed under reverse charge at 18%', 'Taxed at 1%', 'Taxed under section 9(5)'], 0,
                    'Reverse charge on renting of non-residential property by an unregistered person excludes recipients under composition. In practice: check the landlord\'s status every year.', 'hard', topic=T2),
                  M('k1d', 'Hilltop\'s invoices must be:', ['Bills of supply marked as composition taxable person', 'Tax invoices showing CGST and SGST', 'E-invoices', 'Export invoices'], 0,
                    'A composition taxpayer issues bills of supply without charging tax and declares his status. In practice: also display it at the shop.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch03', 1, 'Charge of GST',
                ['Explain the levy under the CGST and IGST Acts.',
                 'Identify supplies taxed under reverse charge and the ECO\'s liability.',
                 'Apply the eligibility, rates and conditions of composition levy.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['int-p3-b-ch02-u01'],
                 'exam_tip': 'For reverse charge questions, check both the supplier\'s and the recipient\'s description — the entry applies only if both match.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['s. 9(1)/IGST s. 5: levy on supply, except alcohol for human consumption.',
                             's. 9(3)/(4): reverse charge on notified supplies; pay in cash.',
                             's. 9(5): ECO pays for cab, accommodation, housekeeping and restaurant services.',
                             'Composition: ₹1.5 crore (₹75 lakh special States); 1%/1%/5%; s. 10(2A) ₹50 lakh at 6%.'],
                 'remember': ['Composition: no ITC, no tax collection, bill of supply.', 'Services up to 10% of turnover or ₹5 lakh allowed under s. 10(1).'],
                 'traps': ['Inter-State outward supply bars composition.', 'Rent from unregistered landlord not RCM for composition dealers.']},
                [('Composition limit', '₹1.5 crore / ₹75 lakh'), ('Restaurant composition', '5%'), ('s. 10(2A)', '₹50 lakh; 6%'), ('RCM payment', 'Cash only')],
                viva, cases)
