"""CA Final · Paper 5 · Chapter 4 Exemptions from GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch04-u01'
T1 = 'Power to exempt and nature of exemptions'
T2 = 'Health care, education and charitable exemptions'
T3 = 'Agriculture, transport, insurance and financial exemptions'
T4 = 'Renting, RWA and other common exemptions'


def build():
    ck = Checks()
    pm = ck.add('9000*0.18', 'GST per member per month at 18% (₹)')
    yr = ck.add('9000*0.18*12*100', 'Annual GST for 100 members (₹)')
    i1 = {'id': 'i1', 'title': 'Resident welfare association', 'difficulty': 'core', 'minutes': 6,
          'q': 'Green Meadows RWA (aggregate turnover ₹1.08 crore, registered) collects ₹9,000 per month from each of its 100 members for maintenance. Compute GST.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Exemption test', 'Up to ₹7,500 per member per month and turnover ₹20 lakh or less', 'Fails'],
              ['GST per member per month', '18% on the full ₹9,000 (not only the excess)', inr(pm)],
              ['Annual GST', '× 12 months × 100 members', inr(yr)]], title='Exemption notification — RWA entry')],
          'checks': list(ck)}

    c2 = Checks()
    d = c2.add('900*3', 'Rent for a ₹900 room for 3 days (exempt) (₹)')
    t = c2.add('1200*3', 'Rent for a ₹1,200 room for 3 days (taxable) (₹)')
    i2 = {'id': 'i2', 'title': 'Hospitals, religious places and insurance', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Examine: (a) a dharamshala run by a registered charitable trust rents a room at ₹900 per day and another at ₹1,200 per day, each for 3 days; (b) a hospital charges an in-patient non-ICU room rent of ₹4,500 per day; (c) an insurer sells an individual family-floater health policy; (d) a company buys a group health policy for staff.',
          'solution': [table(['Case', 'Treatment'], [
              ['(a)', f'₹{inr(d)} exempt (below ₹1,000/day); ₹{inr(t)} taxable'],
              ['(b)', 'Exempt — room rent up to ₹5,000 per day for in-patients'],
              ['(c)', 'Exempt — individual (incl. family) health insurance, entry 36D'],
              ['(d)', 'Taxable — group policy outside the individual exemption']], title='Exemptions')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Under the CGST Act (section 11) and its IGST counterpart (section 6), the Government may, on GST Council recommendations and in public interest, exempt goods or services generally by notification — absolutely or subject to conditions — or by special order in exceptional cases.',
            'Where a supply is absolutely exempt, the supplier cannot collect tax on it. An exempt supply includes nil-rated, wholly exempt and non-taxable supplies (section 2(47)); ITC attributable to exempt supplies is not available.',
            'Explanations may be inserted to clarify the scope of exemption notifications retrospectively, and exemptions are construed strictly, with the benefit of ambiguity going to the revenue.'],
          'Exemption is a policy choice notified on Council advice.',
          'A supplier of an absolutely exempt service cannot charge GST even if the buyer wants credit.'),
        C('c2', T2, [
            'Health care: services by clinical establishments, authorised medical practitioners and paramedics are exempt; in-patient room rent up to ₹5,000 per day (non-ICU) is exempt. Cosmetic or plastic surgery (other than to restore anatomy or functions) is not exempt.',
            'Education: services that an educational institution renders to its own students, staff and faculty, and services to institutions up to higher secondary (transport, catering including mid-day meals, security, cleaning, admission and exam services) are exempt; services for examinations and supply of online educational journals to institutions have specific entries.',
            'Charitable and religious: services by registered entities by way of charitable activities; renting of precincts of religious places with rooms below ₹1,000 per day, halls below ₹10,000 per day and shops below ₹10,000 per month; conduct of religious ceremonies.'],
          'Health, school education and charity are largely outside GST.',
          'A dharamshala room at ₹900 a day is exempt; one at ₹1,200 is taxable.'),
        C('c3', T3, [
            'Agriculture: cultivation, harvesting, supply of farm labour, warehousing of agricultural produce, renting of agro machinery, and services by APMCs are exempt; processing that alters essential characteristics is not.',
            'Transport: passengers by metro, local trains, non-AC stage carriages and (non-air-conditioned) railway classes; goods by road (except GTA and courier), and specified goods by rail or vessel, are exempt in specified cases.',
            'Insurance and finance: individual life and health insurance (including family policies) are exempt under entries 36C and 36D; specified government schemes are exempt; interest on loans and deposits, RBI services and foreign exchange between banks are exempt.'],
          'Farm, mass transport and individual insurance are relieved.',
          'A family floater health policy bought by an individual is exempt.'),
        C('c4', T4, [
            'Renting of residential dwelling for use as residence is exempt, except where rented to a registered person — though even then it remains exempt if the registered person is a proprietor renting it in his personal capacity for his own residence and the rent is booked on his personal account.',
            'RWA services to members are exempt only if contribution does not exceed ₹7,500 per member per month and, where it does, GST applies to the full amount; RWAs with aggregate turnover up to ₹20 lakh are exempt from registration anyway.',
            'Other exemptions include old-age homes run by government or registered charities for residents aged 60 or more at up to ₹25,000 per member per month (inclusive of boarding and lodging), services of arbitral tribunals and advocates to persons other than business entities or to small business entities, and sponsorship of specified sporting events.'],
          'Thresholds decide many common exemptions.',
          'A ₹9,000 monthly RWA contribution is taxed in full at 18%.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Exemption review for a trust hospital', 'role': 'GST consultant',
             'situation': 'A charitable hospital runs pharmacies, rooms and a guest house.',
             'steps': ['Classify each service against health care entries.', 'Check room rent and guest house thresholds.', 'Identify taxable activities.', 'Reverse ITC for exempt supplies.'],
             'takeaway': 'One entity can have exempt and taxable supplies side by side.'}]

    mcqs = [
        Q('m1', 'Exemption under section 11 is granted on the recommendation of:', ['The GST Council', 'The CBIC alone', 'The Parliament', 'The State Assembly'], 0,
          'Public interest. In practice: notification.', 'c1', T1),
        Q('m2', 'In-patient non-ICU room rent is exempt up to:', ['Five thousand rupees per day', 'One thousand rupees per day', 'Ten thousand rupees per day', 'Seven thousand five hundred rupees per day'], 0,
          'Health care entry. In practice: above it, taxable.', 'c2', T2),
        Q('m3', 'Transport of students by a contractor for a higher secondary school is:', ['Exempt', 'Taxable at 18%', 'Taxable at 5%', 'Zero-rated'], 0,
          'Services to institutions up to HS. In practice: colleges excluded.', 'c2', T2),
        Q('m4', 'An individual health insurance policy is:', ['Exempt', 'Taxable at 18%', 'Taxable at 5%', 'Outside GST'], 0,
          'Entry 36D. In practice: group policies taxable.', 'c3', T3),
        Q('m5', 'Renting of a residential flat to a registered company for its guest house is:', ['Taxable', 'Exempt', 'Outside GST', 'Zero-rated'], 0,
          'Not use as residence of an individual. In practice: RCM may apply.', 'c4', T4),
        Q('m6', 'RWA maintenance is exempt if contribution per member per month does not exceed:', ['Seven thousand five hundred rupees', 'Five thousand rupees', 'Ten thousand rupees', 'Twenty-five thousand rupees'], 0,
          'Threshold. In practice: whole amount taxable if exceeded.', 'c4', T4),
        Q('m7', 'Renting a community hall of a religious place at ₹12,000 per day is:', ['Taxable', 'Exempt', 'Outside GST', 'Exempt up to ₹10,000 only'], 0,
          'Limit ₹10,000 per day. In practice: whole amount taxable.', 'c2', T2),
        Q('m8', 'Interest on loans is:', ['Exempt', 'Taxable at 18%', 'Outside GST as money', 'Zero-rated'], 0,
          'Financial services entry. In practice: processing fees taxable.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Exemption test', 2, 'analysis', '7,500'), S('s2', 'Tax computation', 2, 'computation', 'full', nums=[pm, yr])],
          ['Explain full-amount rule.'], ['Taxing only the excess over ₹7,500.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Religious rooms', 2, 'analysis', '1,000', nums=[d, t]), S('s2', 'Hospital and insurance', 4, 'analysis', 'individual')],
          ['Cite entries.'], ['Exempting group policies.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can a supplier charge GST on an absolutely exempt supply?', 'Charging is barred; the supplier must supply without tax.',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'Without tax', 5, 'without tax')], 'c1'),
        V('v2', 'Is cosmetic surgery exempt health care?', 'It is taxable unless undertaken to restore anatomy or functions affected by congenital defects, injury, disease or trauma.',
          [P('p1', 'Taxable', 5, 'taxable'), P('p2', 'Restore', 5, 'restore')], 'c2'),
        V('v3', 'When is renting a residence to a registered person exempt?', 'When the registered person is a proprietor renting in personal capacity for own residence and on personal account.',
          [P('p1', 'Proprietor', 5, 'proprietor'), P('p2', 'Personal capacity', 5, 'personal capacity')], 'c4'),
        V('v4', 'Which entries exempt individual life and health insurance?', 'Entries 36C and 36D, covering individuals and their families but not groups.',
          [P('p1', '36C and 36D', 5, '36c'), P('p2', 'Families', 5, 'famil')], 'c3'),
        V('v5', 'Is processing of agricultural produce exempt?', 'Only processes that keep the essential characteristics and make it marketable are covered; others are taxable.',
          [P('p1', 'Essential characteristics', 5, 'essential characteristics'), P('p2', 'Marketable', 5, 'marketable')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Sunrise Public School', 'difficulty': 'core',
              'case': 'Sunrise Public School (classes nursery to XII) pays a contractor ₹6,00,000 a year for student transport and ₹4,00,000 for canteen catering, and rents its auditorium to a company for a seminar for ₹50,000.',
              'mcqs': [
                  M('k1a', 'Transport services to the school are:', ['Exempt', 'Taxable', 'Zero-rated', 'Outside GST'], 0,
                    'Up to higher secondary. In practice: contractor charges no GST.', 'core', topic=T2),
                  M('k1b', 'Catering services to the school are:', ['Exempt', 'Taxable at 18%', 'Taxable at 5%', 'RCM'], 0,
                    'Covered entry. In practice: includes mid-day meals.', 'core', topic=T2),
                  M('k1c', 'GST on auditorium rent at 18% (₹):', ['9,000', '4,500', 'Nil', '18,000'], 0,
                    'Not education service. In practice: school may need registration.', 'core', check=9000, topic=T2),
                  M('k1d', 'Total exempt inward services value (₹):', ['10,00,000', '6,00,000', '4,00,000', '10,50,000'], 0,
                    '6 lakh + 4 lakh. In practice: no ITC needed.', 'core', check=1000000, topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch04', 1, 'Exemptions from GST',
                ['Explain the power to grant exemptions.',
                 'Apply health care, education and charitable exemptions.',
                 'Apply agriculture, transport, insurance and finance exemptions.',
                 'Apply renting, RWA and other exemptions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 25}, 'prereq': ['fin-p5-ch03-u01'],
                 'exam_tip': 'Quote the threshold and test it — many exemptions fail on the limit.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 11: exemption by notification or special order.', 'Health care; room rent ≤ ₹5,000/day.', 'Education up to higher secondary.',
                             'Religious rooms < ₹1,000/day; halls < ₹10,000/day.', 'Individual life/health insurance exempt (36C/36D).', 'RWA ≤ ₹7,500/member/month.'],
                 'remember': ['Exceeding a threshold taxes the whole amount.'],
                 'traps': ['Exempting group insurance policies.']},
                [('Power to exempt', 'Section 11'), ('Exempt supply', 'Section 2(47)'), ('Insurance', 'Entries 36C/36D')],
                viva, cases)
