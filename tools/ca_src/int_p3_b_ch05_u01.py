"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 5 Exemptions from GST.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch05-u01'
T1 = 'Power to grant exemption (s. 11)'
T2 = 'Exempt goods'
T3 = 'Exempt services: health, education, charity, legal and housing'
T4 = 'Exempt services: transport, agriculture, Government and others'


def build():
    ck = Checks()
    hosp = ck.add('(6000*4)*5/100', 'GST on non-ICU room charges above ₹5,000 a day (5% for 4 days)')
    i1 = {'id': 'i1', 'title': 'A hospital bill', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'City Hospital bills a patient for: doctor\'s fees ₹20,000; medicines and consumables used in treatment ₹15,000; ICU charges ₹30,000 for 2 days; and a deluxe (non-ICU) room at ₹6,000 a day for 4 days. Room charges above ₹5,000 a day (other than ICU) are taxable at 5% without ITC. Determine the GST.',
          'solution': [table(['Item', 'Treatment', 'GST ₹'], [
              ['Doctor\'s fees', 'Health care by clinical establishment — exempt', '0'],
              ['Medicines used in treatment', 'Part of composite health care — exempt', '0'],
              ['ICU charges', 'ICU/CCU/ICCU/NICU rooms are never taxed', '0'],
              ['Deluxe room (₹6,000 a day)', 'Above ₹5,000 a day, non-ICU — taxable at 5%', inr(hosp)]], title='Health care exemption'),
              note('The whole room charge (not just the excess over ₹5,000) is taxed once the per-day threshold is crossed.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Taxable or exempt?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Examine: (a) Adv. Rao, an individual, advises Mr. Lal on his personal property dispute; (b) a registered charitable trust runs a free yoga camp; (c) a private school charges fees and provides a bus to its students; (d) a GTA carries a truckload of wheat for a registered trader; (e) a residents\' welfare association collects ₹6,000 a month from each member for maintenance.',
          'solution': [table(['Case', 'Answer', 'Reason'], [
              ['(a)', 'Exempt', 'Legal services by an individual advocate to a person other than a business entity'],
              ['(b)', 'Exempt', 'Charitable activity (advancement of yoga) by a trust registered under the Income-tax Act'],
              ['(c)', 'Exempt', 'Services by an educational institution to its students, including transport of students'],
              ['(d)', 'Exempt', 'GTA transport of agricultural produce and food grains'],
              ['(e)', 'Exempt', 'Contribution of up to ₹7,500 per member per month to an RWA for common use']], title='Exemption notification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 11(1): on the GST Council\'s recommendation, the Government may, by notification in public interest, exempt goods or services generally, absolutely or subject to conditions.',
            'Section 11(2): in exceptional circumstances it may, by special order, exempt a particular supply; the reasons must be stated.',
            'Where an exemption is absolute, the supplier cannot collect tax above the exempt price. Exempt supplies include nil-rated supplies and non-taxable supplies; ITC on inputs used for them is not available.'],
          'An exemption is a deliberate "zero" chosen by the Council — it also switches off credit.',
          'A farmer-producer company selling fresh vegetables charges no GST and takes no ITC on its crates.'),
        C('c2', T2, [
            'Exempt goods are mostly basic necessities and items of social importance: fresh fruits and vegetables, fresh milk and curd (not pre-packaged in the notified manner), eggs, unbranded cereals in loose form, salt, human blood, contraceptives, printed books and newspapers, and handloom raw silk among others.',
            'Goods are classified by HSN code, and the exemption applies only to the exact description and condition in the notification — a pre-packaged and labelled form of the same item may be taxed.',
            'Supplies of exempt goods remain supplies; they count in aggregate turnover for registration and composition limits.'],
          'For goods, the exemption hangs on the precise description, packaging and HSN entry.',
          'Loose rice from a sack is exempt; the same rice in a labelled, pre-packaged bag of 10 kg is taxed at 5%.'),
        C('c3', T3, [
            'Health: services by a clinical establishment, an authorised medical practitioner or paramedics for diagnosis or treatment are exempt, except room charges above ₹5,000 a day (other than intensive-care rooms). Cosmetic and plastic surgery is not exempt unless it restores or reconstructs.',
            'Education: services by an educational institution to students, faculty and staff; and services received by school-level institutions such as student transport, mid-day catering, security, cleaning and conduct of examinations.',
            'Charity: services by an entity registered under the Income-tax Act by way of charitable activities — public health, religion and spirituality, yoga, education and skill development relating to specified persons, and preservation of environment.',
            'Legal: services by an individual advocate or firm of advocates to another advocate or firm, to a person other than a business entity, or to a business entity with preceding-year aggregate turnover up to the registration threshold. Housing: renting a residential dwelling for use as a residence is exempt unless it is let to a registered person (a proprietor renting in his personal capacity for his own residence is still exempt). Insurance: individual life and health insurance policies were exempted from 22 September 2025.'],
          'Social sectors — health, learning, charity, justice and housing — get the widest service exemptions.',
          'A coaching centre for a professional exam is not an "educational institution" as defined, so its fees are taxable.'),
        C('c4', T4, [
            'Transport: passengers by non-AC contract carriage (not for tourism), stage carriage, metro, monorail, public ferries, railways in non-AC classes, metered cabs and auto-rickshaws; goods by road (other than GTA or courier), and GTA transport of agricultural produce, milk, salt, food grains, organic manure, newspapers and relief materials, or where freight is up to ₹1,500 per carriage or ₹750 per consignee.',
            'Agriculture: cultivation, supply of farm labour, harvesting, warehousing of agricultural produce and renting of agricultural machinery relating to agriculture.',
            'Government: most services by Government to individuals; services to business entities up to ₹5,000 a supply (with exclusions); pure services to Government relating to functions of panchayats or municipalities.',
            'Others: services by RBI; admission to museums, zoos, national parks and protected monuments; contribution up to ₹7,500 per member per month to a residents\' welfare association; hotel accommodation with value up to ₹1,000 a day; services to the United Nations and specified international organisations.'],
          'Exemptions follow essentials — moving people cheaply, growing food, and basic civic services.',
          'An AC luxury bus hired for a tour group is taxable; an ordinary non-AC city bus is exempt.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Exemption audit', 'role': 'Article assistant',
             'situation': 'A client claims all its income is exempt "because it is a trust".',
             'steps': ['List each activity and receipt.', 'Match each to an exemption entry and its conditions.', 'Treat non-charitable activities (rent, sale of goods) separately.', 'Check registration need on taxable turnover.'],
             'takeaway': 'Exemption is for the activity, not for the entity.'}]

    mcqs = [
        Q('m1', 'Under section 11, exemptions are granted by the Government on the recommendation of:', ['GST Council', 'GSTN', 'Parliament', 'CBIC'], 0,
          'Section 11 allows exemption by notification only on the Council\'s recommendation, in public interest. In practice: read the notification\'s conditions.', 'c1', T1),
        Q('m2', 'Health care room charges are taxable when:', ['Non-ICU room charge exceeds ₹5,000 a day', 'Any room is charged', 'ICU charge exceeds ₹5,000 a day', 'The patient is insured'], 0,
          'Only non-ICU room charges above ₹5,000 a day are carved out; ICU, CCU, ICCU and NICU rooms stay exempt. In practice: tax is 5% without ITC.', 'c3', T3),
        Q('m3', 'Legal services by an advocate are exempt when supplied to:', ['A business entity with preceding-year turnover within the registration threshold', 'Any company', 'A business entity with turnover of ₹5 crore', 'A foreign company only'], 0,
          'Exemption covers services to advocates, to non-business persons and to small business entities within the threshold. Others pay under reverse charge. In practice: ask for turnover proof.', 'c3', T3),
        Q('m4', 'Renting of a residential flat to a registered company for its staff is:', ['Taxable (reverse charge by the company)', 'Exempt', 'Not a supply', 'Taxable at 1%'], 0,
          'The residential-dwelling exemption does not apply when let to a registered person (except a proprietor using it as own residence); the company pays under reverse charge. In practice: check the tenant\'s GSTIN.', 'c3', T3),
        Q('m5', 'GTA services for transporting which goods are exempt?', ['Agricultural produce', 'Electronic goods', 'Cement', 'Cars'], 0,
          'GTA transport of agricultural produce, milk, salt, food grains, organic manure, newspapers and relief materials is exempt. In practice: mixed loads need careful invoices.', 'c4', T4),
        Q('m6', 'Monthly contribution to an RWA is exempt up to:', ['₹7,500 per member', '₹5,000 per member', '₹10,000 per flat', '₹20 lakh a year'], 0,
          'Up to ₹7,500 per month per member for common use services is exempt; above that the whole amount is taxable if the RWA\'s turnover exceeds the registration limit. In practice: limits are per member, per month.', 'c4', T4, check=7500),
        Q('m7', 'Which passenger transport is exempt?', ['Metered taxi', 'AC contract carriage for tourism', 'Air travel in business class', 'Chartered helicopter'], 0,
          'Metered cabs, auto-rickshaws and non-AC public transport are exempt; tourism and luxury transport is taxed. In practice: cab aggregators are taxed through section 9(5).', 'c4', T4),
        Q('m8', 'An absolute exemption means the supplier:', ['Cannot collect tax on that supply', 'May choose to pay tax', 'Pays tax at concessional rate', 'Pays tax and claims refund'], 0,
          'Where an exemption is unconditional, the supplier cannot charge tax over the exempt price, and ITC on related inputs is not available. In practice: invoice as exempt.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Fees exempt', 1, 'concept', 'exempt'), S('s2', 'ICU exempt', 1, 'concept', 'icu'), S('s3', 'Room taxable', 2, 'computation', '5%', nums=[hosp])],
          ['Check the per-day threshold.'], ['Taxing only the excess over ₹5,000.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Legal', 1, 'concept', 'advocate'), S('s2', 'Charity', 1, 'concept', 'charitable'), S('s3', 'Education', 1, 'concept', 'educational'),
           S('s4', 'GTA', 1, 'concept', 'agricultural|food grain'), S('s5', 'RWA', 1, 'concept', '7,500')],
          ['Name the entry.'], ['Assuming all school purchases are exempt.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What does section 11(2) allow?', 'A special order exempting a particular supply in exceptional circumstances, with reasons recorded in the order.',
          [P('p1', 'Special order', 6, 'special order'), P('p2', 'Exceptional', 4, 'exceptional')], 'c1'),
        V('v2', 'Who is an educational institution for the exemption?', 'An institution providing pre-school to higher secondary education, education leading to a recognised qualification under law, or approved vocational courses.',
          [P('p1', 'School level', 5, 'school|secondary'), P('p2', 'Recognised qualification', 5, 'recognised|law')], 'c3'),
        V('v3', 'When is renting of a residential dwelling taxable?', 'When it is let to a registered person, who pays under reverse charge, unless he is a proprietor renting it for his own residence in his personal capacity.',
          [P('p1', 'Registered tenant', 6, 'registered'), P('p2', 'Reverse charge', 4, 'reverse')], 'c3'),
        V('v4', 'Name two exempt agricultural services.', 'Cultivation and supply of farm labour, as well as warehousing of agricultural produce and renting of agricultural machinery.',
          [P('p1', 'Cultivation or labour', 5, 'cultivation|labour'), P('p2', 'Warehousing or machinery', 5, 'warehous|machinery')], 'c4'),
        V('v5', 'Can ITC be taken on inputs used for exempt supplies?', 'Credit on inputs and services used for exempt supplies is barred; where inputs are common to taxable and exempt supplies, the share for exempt supplies is reversed.',
          [P('p1', 'Credit barred', 6, 'barred|disallow'), P('p2', 'Reversal', 4, 'revers')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Sunrise Foundation', 'difficulty': 'moderate',
              'case': 'Sunrise Foundation, a trust registered under the Income-tax Act, runs (i) free medical camps; (ii) a school up to Class XII with bus service; (iii) rents part of its building to a bank at ₹1 lakh a month; (iv) organises yoga workshops for a fee.',
              'mcqs': [
                  M('k1a', 'Medical camps (i) are:', ['Exempt', 'Taxable at 18%', 'Not a supply', 'Taxable at 5%'], 0,
                    'Health care services and charitable activities relating to public health are exempt. In practice: no fee often means no consideration at all.', 'core', topic=T3),
                  M('k1b', 'Bus service to students (ii):', ['Exempt', 'Taxable', 'Exempt only if free', 'Taxable under RCM'], 0,
                    'Services by an educational institution to its students, including transport, are exempt. In practice: a third-party bus operator\'s service to the school is also exempt up to higher secondary.', 'core', topic=T3),
                  M('k1c', 'Rent from the bank (iii):', ['Taxable', 'Exempt as the trust is charitable', 'Not a supply', 'Exempt up to ₹20 lakh'], 0,
                    'Renting commercial space is not a charitable activity, so it is taxable; the trust must register if taxable turnover exceeds the threshold. In practice: ₹12 lakh a year rent is below ₹20 lakh.', 'moderate', topic=T1),
                  M('k1d', 'Yoga workshops for a fee (iv):', ['Exempt as a charitable activity', 'Taxable at 18%', 'Not a supply', 'Taxable under RCM'], 0,
                    'Advancement of yoga by a registered trust is a charitable activity and exempt, even if fees are charged. In practice: keep the registration current.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch05', 1, 'Exemptions from GST',
                ['Explain the power to grant exemptions.',
                 'Identify important exempt goods.',
                 'Apply the main service exemptions and their conditions.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['int-p3-b-ch04-u01'],
                 'exam_tip': 'Exemptions are condition-heavy: underline who supplies, to whom, and any value limit in the question.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['s. 11(1) general exemption; s. 11(2) special order.',
                             'Goods: fresh produce, milk, eggs, books etc. — exact HSN and packaging matter.',
                             'Health (room > ₹5,000 non-ICU taxable), education, charity, legal, residential renting.',
                             'Transport, agriculture, Government, RWA (₹7,500), hotel ≤ ₹1,000.'],
                 'remember': ['Exemption is activity-based.', 'No ITC on exempt supplies.'],
                 'traps': ['Residential flat to registered company is taxable (RCM).', 'Coaching for exams is not an educational institution.']},
                [('Hospital room', 'Taxable if > ₹5,000/day (non-ICU)'), ('RWA', '₹7,500 per member/month'), ('Hotel', 'Exempt up to ₹1,000/day'), ('Govt to business', '₹5,000 per supply')],
                viva, cases)
