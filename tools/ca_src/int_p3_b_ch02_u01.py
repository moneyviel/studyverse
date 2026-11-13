"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 2 Supply under GST.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch02-u01'
T1 = 'Meaning and scope of supply (s. 7(1)) and Schedule I'
T2 = 'Schedule II: goods or services?'
T3 = 'Schedule III and notified non-supplies'
T4 = 'Composite and mixed supply (s. 8)'


def build():
    ck = Checks()
    comp = ck.add('120000*18/100', 'Composite supply taxed at the rate of the principal supply (18%)')
    mix = ck.add('(400+300+500)*18/100', 'Mixed supply taxed at the highest rate in the pack (18%)')
    i1 = {'id': 'i1', 'title': 'One price, many items', 'difficulty': 'moderate', 'minutes': 7,
          'q': '(a) Zenith Ltd. sells a laptop (18%) for ₹1,20,000 including a carry case, charger and one-year warranty, invoiced as one price. (b) A shop sells a festive hamper for ₹1,200 containing sweets (5%), dry fruits (5%) and a decorative lamp (18%) at a single price. Determine the nature of each supply and the tax.',
          'solution': [table(['Case', 'Nature', 'Rate applied', 'Tax ₹'], [
              ['(a) Laptop pack', 'Composite: items are naturally bundled; the laptop is the principal supply', '18% (laptop)', inr(comp)],
              ['(b) Hamper', 'Mixed: items can be sold separately and are not naturally bundled; single price', '18% (highest in the pack)', inr(mix)]], title='Section 8'),
              note('Ask: would a buyer expect these items together in the ordinary course of business? If yes, composite; if they are merely combined for a single price, mixed.')],
          'checks': list(ck)}

    ck2 = Checks()
    sch1 = ck2.add('80000*18/100', 'Tax on transfer of a car to a branch in another State at open market value')
    i2 = {'id': 'i2', 'title': 'Supply without consideration', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Examine whether these are supplies: (a) Hari Ltd., Mumbai sends goods to its own registered branch in Bengaluru free of cost; open market value ₹80,000 (18%). (b) A trader gives his son a television from stock on which ITC was taken, as a birthday gift. (c) A company gives its employee gifts worth ₹40,000 in the year. (d) Mr. Sen sells his personal car to a dealer.',
          'solution': [table(['Case', 'Answer', 'Reason'], [
              ['(a)', 'Supply; tax ' + inr(sch1), 'Schedule I: supply between distinct persons (separately registered branches) even without consideration'],
              ['(b)', 'Supply', 'Schedule I: permanent disposal of business assets on which ITC was availed'],
              ['(c)', 'Not a supply', 'Schedule I: gifts by employer to employee are deemed supply only above ₹50,000 a year per employee'],
              ['(d)', 'Not a supply', 'Not in the course or furtherance of business']], title='Section 7 read with Schedule I')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 7(1): supply includes every form of supply of goods or services — sale, transfer, barter, exchange, licence, rental, lease or disposal — made or agreed to be made for a consideration by a person in the course or furtherance of business; import of services for consideration, even if not for business; and the activities in Schedule I made without consideration.',
            'Activities of a person (other than an individual) to its members or constituents for consideration are also supply; so a club supplying to its members is covered.',
            'Schedule I (supply even without consideration): permanent transfer or disposal of business assets where ITC was availed; supply between related persons or distinct persons in the course of business (gifts up to ₹50,000 a year by an employer to an employee excluded); supply of goods by a principal to his agent or by the agent to the principal where the agent supplies on the principal\'s behalf; and import of services from a related person or own establishment outside India in the course of business.',
            '"Business" is wide: trade, commerce, profession, vocation and adventure in the nature of trade, whether or not for profit, including connected activities and the activities of a club to its members.'],
          'Supply is the taxable event — first ask "is this a supply?", then "of what?", then "where?" and "when?".',
          'Free samples to dealers on which ITC was claimed: no Schedule I entry covers them, so no tax, but the ITC must be reversed.'),
        C('c2', T2, [
            'Schedule II settles whether an activity is goods or services: transfer of title in goods is goods; transfer of right in goods without title (e.g. hire) is services; transfer of title in goods where property passes later on full payment (hire purchase) is goods.',
            'Lease, tenancy or licence to occupy land or building is services; job work on another person\'s goods is services; goods forming part of business assets put to private use or used by another person without consideration — services.',
            'Construction of a complex or building for sale before completion certificate is services; works contracts and supply of food or drink as part of a service (restaurants) are services; renting of goods and agreeing to tolerate an act are services.',
            'Supply of goods by an unincorporated association or body of persons to a member for consideration is goods.'],
          'Schedule II answers one question only — goods or services — not whether tax is payable.',
          'Restaurant meals are services, even though food is goods, because Schedule II treats them as part of a service.'),
        C('c3', T3, [
            'Schedule III lists activities that are neither goods nor services: services by an employee to the employer in employment; services of courts and tribunals; functions of MPs, MLAs and other elected or constitutional office-holders; funeral, burial and crematorium services; sale of land and, subject to the construction rule, sale of a completed building; actionable claims other than specified actionable claims (lottery, betting, gambling, horse racing and online money gaming).',
            'Also covered: supply of goods from a place outside India to another place outside India without entering India; high-sea sales before goods are cleared for home consumption; and sale of warehoused goods before clearance for home consumption.',
            'Section 7(2)(b): activities of the Central or State Government or local authorities as public authorities that are notified on the Council\'s recommendation are also non-supplies.'],
          'Schedule III lifts certain activities out of GST altogether.',
          'Selling a plot of land is outside GST; selling a flat under construction before completion is a taxable service.'),
        C('c4', T4, [
            'A composite supply is two or more supplies naturally bundled and supplied together in the ordinary course of business, one being the principal supply; it is taxed at the rate of the principal supply.',
            'A mixed supply is two or more individual supplies made together for a single price where the items are not naturally bundled and can be supplied separately; it is taxed at the highest rate among them.',
            'Indicators of natural bundling: consumers usually expect them together, a single price, elements usually advertised as a package and the main element being the reason for purchase.'],
          'Composite follows the main item; mixed follows the most heavily taxed item.',
          'A hotel room with breakfast is composite (accommodation is principal); a gift box of chocolates and a toy at one price is mixed.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Billing review', 'role': 'Article assistant',
             'situation': 'A retailer bundles products into combo offers and asks what rate to charge.',
             'steps': ['List each combo and its contents.', 'Ask whether items are naturally bundled.', 'Apply principal-supply rate or highest rate.', 'Consider pricing items separately to avoid the highest rate.'],
             'takeaway': 'Pricing items separately avoids mixed-supply treatment altogether.'}]

    mcqs = [
        Q('m1', 'Which is a supply even without consideration under Schedule I?', ['Goods sent to a branch registered in another State', 'Free samples to customers on which ITC was not taken', 'Personal car sold by an individual', 'Gift of ₹20,000 by employer to employee'], 0,
          'Branches with separate registrations are distinct persons, so stock transfers between them are supply even without consideration. Gifts up to ₹50,000 to an employee are excluded. In practice: value at open market value.', 'c1', T1),
        Q('m2', 'Import of services without consideration is a supply when received:', ['From a related person abroad in the course of business', 'From any person for personal use', 'From an unrelated person for business', 'Never'], 0,
          'Schedule I covers import of services from a related person or from one\'s own establishment outside India in the course of business, even without consideration. In practice: tax is paid under reverse charge.', 'c1', T1),
        Q('m3', 'Under Schedule II, hire purchase of goods is a supply of:', ['Goods', 'Services', 'Neither', 'Both'], 0,
          'Where title in goods passes at a future date on payment of the full consideration, it is a supply of goods. Hire without title is services. In practice: check the agreement.', 'c2', T2),
        Q('m4', 'Which is in Schedule III?', ['Services by an employee to the employer in employment', 'Renting of residential property', 'Job work', 'Works contract'], 0,
          'Employee services in the course of employment are neither goods nor services. The others are services under Schedule II. In practice: consultants are not employees.', 'c3', T3),
        Q('m5', 'Which actionable claim is taxable under GST?', ['Online money gaming', 'Debt receivable', 'Right to claim insurance money', 'Bank deposit'], 0,
          'Only specified actionable claims — lottery, betting, gambling, horse racing and online money gaming — are taxable; other actionable claims are in Schedule III. In practice: value rules for these are special.', 'c3', T3),
        Q('m6', 'Goods shipped from China directly to Brazil by an Indian trader, never entering India, are:', ['Neither supply of goods nor services', 'Export of goods', 'Inter-State supply', 'Import of goods'], 0,
          'Supply of goods from a non-taxable territory to another non-taxable territory without entering India is in Schedule III. In practice: such turnover is still reported in returns where required.', 'c3', T3),
        Q('m7', 'A mixed supply is taxed at:', ['The highest rate among its components', 'The rate of the principal supply', 'The lowest rate', 'The average rate'], 0,
          'Section 8(b) applies the highest rate to a mixed supply. Composite supplies take the principal supply\'s rate. In practice: separate pricing avoids this.', 'c4', T4),
        Q('m8', 'Which is a composite supply?', ['Goods packed, insured and transported by the supplier to the buyer', 'A pack of shampoo and a free toy at one price', 'Diwali gift box of sweets and crockery', 'A combo of soap and a bucket'], 0,
          'Packing, transport and insurance are naturally bundled with the supply of goods, the goods being the principal supply. The others are merely combined for a single price. In practice: tax at the goods\' rate.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Composite identified', 1, 'concept', 'composite'), S('s2', 'Tax on laptop pack', 1, 'computation', '18%', nums=[comp]),
           S('s3', 'Mixed identified', 1, 'concept', 'mixed'), S('s4', 'Tax on hamper', 1, 'computation', 'highest', nums=[mix])],
          ['Name the principal supply.'], ['Taxing the hamper at 5%.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Distinct persons', 1, 'concept', 'distinct', nums=[sch1]), S('s2', 'Business assets with ITC', 1, 'concept', 'itc|business assets'),
           S('s3', 'Gift limit', 1, 'concept', '50,000'), S('s4', 'Personal sale', 1, 'concept', 'not in the course|furtherance')],
          ['Quote the Schedule I entry.'], ['Treating every gift to employees as supply.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the essentials of a supply under section 7(1)(a)?', 'Supply of goods or services, for consideration, by a person, in the course or furtherance of business — any form such as sale, barter, exchange, lease or disposal.',
          [P('p1', 'Consideration', 5, 'consideration'), P('p2', 'Course of business', 5, 'business')], 'c1'),
        V('v2', 'When are gifts to employees taxable?', 'When the value of gifts given by an employer to an employee exceeds ₹50,000 in a financial year, as Schedule I treats them as supply between related persons.',
          [P('p1', '₹50,000', 6, '50,000'), P('p2', 'Related persons', 4, 'related|schedule i')], 'c1'),
        V('v3', 'What does Schedule II decide?', 'Whether a particular activity is a supply of goods or a supply of services, such as treating job work and leasing as services and hire purchase as goods.',
          [P('p1', 'Goods or services', 6, 'goods or|services'), P('p2', 'Example', 4, 'job work|lease|hire')], 'c2'),
        V('v4', 'Name two Schedule III activities.', 'Services of an employee to the employer in employment and sale of land, among others such as funeral services and high-sea sales.',
          [P('p1', 'Employee', 5, 'employee'), P('p2', 'Land or other', 5, 'land|funeral|high-sea|court')], 'c3'),
        V('v5', 'How is a composite supply taxed?', 'At the rate applicable to its principal supply, because the elements are naturally bundled with that main supply.',
          [P('p1', 'Principal supply', 6, 'principal'), P('p2', 'Naturally bundled', 4, 'natural|bundl')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Spark Electricals', 'difficulty': 'moderate',
              'case': 'Spark Electricals, a registered dealer in Lucknow, (i) moves a generator from its Lucknow office to its separately registered Kanpur warehouse; (ii) gives its accountant Diwali gifts worth ₹60,000 in the year; (iii) sells a fan-and-light combo at one price; (iv) sells an old office building after completion certificate.',
              'mcqs': [
                  M('k1a', 'Movement of the generator (i) is:', ['A supply between distinct persons', 'Not a supply, as both places are in one State', 'An export', 'Exempt'], 0,
                    'Each separate registration, even within the same State, is a distinct person, so the transfer is a Schedule I supply without consideration. In practice: value it at open market value.', 'moderate', topic=T1),
                  M('k1b', 'The Diwali gifts (ii):', ['Are a supply, as they exceed ₹50,000', 'Are not a supply', 'Are in Schedule III', 'Are exempt'], 0,
                    'Gifts to an employee above ₹50,000 in a year are a supply under Schedule I. In practice: value at open market value.', 'core', topic=T1),
                  M('k1c', 'The fan-and-light combo (iii) is taxed as:', ['A mixed supply at the higher rate', 'A composite supply at the fan\'s rate', 'Two separate supplies', 'Exempt'], 0,
                    'The items are not naturally bundled but are sold at one price, so the highest rate applies. In practice: price them separately.', 'core', topic=T4),
                  M('k1d', 'Sale of the completed building (iv) is:', ['Neither supply of goods nor services', 'A taxable service', 'Taxable at 18%', 'Exempt supply'], 0,
                    'Sale of a building after the completion certificate is in Schedule III. In practice: ITC on related inputs may need reversal.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch02', 1, 'Supply under GST',
                ['Determine whether a transaction is a supply under section 7.',
                 'Apply Schedules I, II and III.',
                 'Identify composite and mixed supplies and their tax treatment.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['int-p3-b-ch01-u01'],
                 'exam_tip': 'For each fact, cite the exact Schedule entry; examiners award marks for the reason, not just yes/no.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Supply: for consideration, in course of business; plus import of services and Schedule I.',
                             'Schedule I: no consideration needed (assets with ITC, related/distinct persons, principal-agent, related import of services).',
                             'Schedule II: goods v. services; Schedule III: neither.',
                             'Composite → principal rate; mixed → highest rate.'],
                 'remember': ['Employer gifts up to ₹50,000 a year are not supply.', 'Only five specified actionable claims are taxable.'],
                 'traps': ['Separate registrations make branches distinct persons.', 'Sale of land is outside GST.']},
                [('Schedule I', 'Supply without consideration'), ('Schedule II', 'Goods or services'), ('Schedule III', 'Neither'), ('s. 8', 'Composite / mixed')],
                viva, cases)
