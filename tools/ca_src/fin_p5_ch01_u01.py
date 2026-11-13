"""CA Final · Paper 5 Indirect Tax Laws · Chapter 1 Supply under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch01-u01'
T1 = 'Scope of supply under section 7'
T2 = 'Supplies without consideration — Schedule I'
T3 = 'Goods or services — Schedule II'
T4 = 'Non-supplies — Schedule III and notified activities'
T5 = 'Composite and mixed supplies'


def build():
    ck = Checks()
    mx = ck.add('1000*0.18', 'GST on mixed supply at highest rate 18% (₹)')
    cp = ck.add('(50000+2000)*0.18', 'GST on composite supply at principal-supply rate 18% (₹)')
    i1 = {'id': 'i1', 'title': 'Composite or mixed?', 'difficulty': 'core', 'minutes': 6,
          'q': '(a) A shop sells a festive box containing items individually taxable at 5% and 18% for a single price of ₹1,000. (b) A dealer sells a refrigerator (18%) for ₹50,000 and charges ₹2,000 for delivery and transit insurance in the same invoice. Determine the nature of supply and GST (assume the rates given).',
          'solution': [table(['Case', 'Nature', 'GST (₹)'], [
              ['(a) Festive box', 'Mixed supply — not naturally bundled; highest rate applies', inr(mx)],
              ['(b) Refrigerator with delivery', 'Composite supply — principal supply is the refrigerator', inr(cp)]], title='Section 8')],
          'checks': list(ck)}

    c2 = Checks()
    g = c2.add('60000', 'Value of gift exceeding ₹50,000 limit (₹)')
    i2 = {'id': 'i2', 'title': 'Is it a supply without consideration?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Examine: (a) an employer gives an employee a gold coin worth ₹60,000 on Diwali; (b) another employee gets a gift worth ₹30,000; (c) a manufacturer transfers stock free of cost to its branch registered in another State; (d) a company disposes of old office furniture (ITC availed) to a charity free of cost; (e) an Indian company receives free consultancy from its foreign holding company.',
          'solution': [table(['Case', 'Treatment'], [
              ['(a)', f'Gift of ₹{inr(g)} exceeds ₹50,000 — supply under Schedule I'],
              ['(b)', 'Within ₹50,000 — not a supply'],
              ['(c)', 'Distinct persons — supply even without consideration'],
              ['(d)', 'Permanent disposal of business assets with ITC availed — supply'],
              ['(e)', 'Import of services from related person in course of business — supply']], title='Schedule I')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 7(1) defines supply to include every form of supplying goods or services (such as sale, barter, exchange, rental, lease, licence, transfer or disposal), actual or agreed, made for consideration while carrying on or furthering a business; import of services for consideration, whether or not in the course of business; and Schedule I activities without consideration.',
            'Section 7(1)(aa) brings in dealings of a non-individual person, such as a club or association, with its own members or constituents, where consideration is paid, — so clubs and associations supplying to members are covered.',
            'Key elements: goods (movable property other than money and securities, including actionable claims), services (anything other than goods, money and securities, including activities relating to money for a fee), consideration (including payments by third parties), and business (including activities incidental or ancillary, even without profit motive).'],
          'Supply = a business transaction for consideration, plus listed exceptions.',
          'A club charging its members for an annual dinner makes a supply.'),
        C('c2', T2, [
            'Schedule I treats four categories as supply even without consideration: (1) permanent transfer or disposal of business assets where ITC has been availed; (2) supplies between related persons or distinct persons (section 25) in the course of business — gifts by an employer to an employee up to ₹50,000 a year are excluded; (3) supplies by principal to agent or agent to principal where the agent supplies or receives goods on the principal\'s behalf; (4) import of services from a related person or own establishment outside India in the course of business.',
            'Distinct persons include establishments of the same entity with separate registrations, typically in different States.',
            'Valuation of such supplies follows the valuation rules (open market value, comparable supplies, or cost-plus).'],
          'Four situations make even free supplies taxable.',
          'Free stock transfer to an out-of-State branch is a supply.'),
        C('c3', T3, [
            'Schedule II classifies certain activities: transfer of title in goods is supply of goods; transfer of right in goods without title is supply of services; transfer of title on a future date upon full payment (hire purchase) is supply of goods.',
            'Lease or letting of land or building, job work treatment, renting of immovable property, construction of complexes (except where entire consideration is received after completion certificate), temporary transfer of IPR, works contracts and restaurant services are supplies of services. Supply of goods by unincorporated associations to members and transfer of business assets for private use are also covered.',
            'Goods forming part of business assets put to private use or made available for non-business purposes, without consideration, are supply of services.'],
          'Title passes → goods; only use passes → services.',
          'Renting a machine without transferring title is a supply of services.'),
        C('c4', T4, [
            'Schedule III lists activities that are neither goods nor services: services by an employee to an employer; services of courts and tribunals; functions of MPs, MLAs, panchayat and municipal members and constitutional post-holders; funeral, burial and mortuary services; sale of land and (subject to construction rules) sale of buildings; actionable claims other than specified actionable claims (lottery, betting, gambling, horse racing, casinos, online money gaming).',
            'Also excluded: supply of goods from one place to another outside India without entering India (merchant trade); supply of warehoused goods before clearance for home consumption, and goods in SEZ or FTWZ warehouses before clearance; high-sea sales by endorsement of title documents before clearance; apportionment of co-insurance premium by the lead insurer; and ceding commission between insurer and reinsurer where GST is paid on gross premium.',
            'Section 7(2)(b) allows notified activities of governments and local authorities as public authorities to be treated as non-supplies.'],
          'Some activities are kept out of GST entirely.',
          'Selling bonded warehouse goods before clearance is not a supply.'),
        C('c5', T5, [
            'A composite supply consists of two or more taxable supplies that are naturally bundled as business is normally done, with one of them being the principal supply; it is taxed as the principal supply (section 8(a)). Indicators: customer perception, industry practice, a single price, and whether elements are integral.',
            'A mixed supply consists of two or more individual supplies made together for a single price where they are not naturally bundled; it is taxed at the rate of the supply attracting the highest rate (section 8(b)).',
            'Works contracts and restaurant services are specifically services under Schedule II, overriding the composite analysis.'],
          'Natural bundling decides composite; otherwise the highest rate applies.',
          'A gift box of mixed items at one price is a mixed supply.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Supply mapping for a new client', 'role': 'GST associate',
             'situation': 'A multi-state company asks which transactions attract GST.',
             'steps': ['List business transactions for consideration.', 'Identify Schedule I free supplies.', 'Exclude Schedule III items.', 'Classify bundles as composite or mixed.'],
             'takeaway': 'Supply analysis is the foundation of every GST question.'}]

    mcqs = [
        Q('m1', 'Gifts by an employer to an employee are not a supply if their value in a year does not exceed:', ['Fifty thousand rupees', 'Twenty thousand rupees', 'One lakh rupees', 'Ten thousand rupees'], 0,
          'Schedule I para 2. In practice: track per employee.', 'c2', T2),
        Q('m2', 'Permanent disposal of business assets without consideration is a supply only if:', ['ITC was availed on them', 'They are sold to a relative', 'They exceed ₹50,000', 'They are immovable'], 0,
          'Schedule I para 1. In practice: check ITC records.', 'c2', T2),
        Q('m3', 'Transfer of right in goods without transfer of title is:', ['Supply of services', 'Supply of goods', 'Not a supply', 'Exempt'], 0,
          'Schedule II. In practice: leasing.', 'c3', T3),
        Q('m4', 'Which is in Schedule III?', ['Sale of land', 'Renting of building', 'Works contract', 'Hire purchase'], 0,
          'Neither goods nor services. In practice: buildings subject to rules.', 'c4', T4),
        Q('m5', 'Online money gaming is:', ['A specified actionable claim taxable under GST', 'Outside GST as Schedule III', 'Exempt', 'Supply of goods at nil rate'], 0,
          'Specified actionable claims are excluded from Schedule III. In practice: highest rate.', 'c4', T4),
        Q('m6', 'A mixed supply is taxed at:', ['The highest rate among its components', 'The principal supply rate', 'The lowest rate', 'Average rate'], 0,
          'Section 8(b). In practice: single price.', 'c5', T5),
        Q('m7', 'Supply by a club to its members for consideration is covered by:', ['Section 7(1)(aa)', 'Schedule III', 'Section 9(4)', 'Section 25'], 0,
          'Members and constituents. In practice: clubs and associations.', 'c1', T1),
        Q('m8', 'High-sea sale by endorsement of documents before clearance is:', ['Neither supply of goods nor services', 'Supply of goods', 'Supply of services', 'Import of services'], 0,
          'Schedule III. In practice: IGST at import.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Mixed supply', 2.5, 'analysis', 'mixed', nums=[mx]), S('s2', 'Composite supply', 2.5, 'analysis', 'principal', nums=[cp])],
          ['Explain natural bundling.'], ['Applying principal rate to mixed supply.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Gifts', 2, 'analysis', '50,000', nums=[g]), S('s2', 'Transfers and imports', 4, 'analysis', 'distinct')],
          ['Cite Schedule I paras.'], ['Treating all gifts as supply.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is a composite supply?', 'Two or more taxable supplies that are naturally bundled in normal business practice, with one acting as the principal supply.',
          [P('p1', 'Naturally bundled', 5, 'naturally bundled'), P('p2', 'Principal supply', 5, 'principal')], 'c5'),
        V('v2', 'Who are distinct persons?', 'Establishments of the same person with separate registrations, such as units in different States.',
          [P('p1', 'Separate registrations', 5, 'registration'), P('p2', 'Same person', 5, 'same person')], 'c2'),
        V('v3', 'Is import of services without consideration a supply?', 'Yes, if from a related person or own establishment outside India in the course of business.',
          [P('p1', 'Related person', 5, 'related'), P('p2', 'Course of business', 5, 'business')], 'c2'),
        V('v4', 'Is a hire purchase transaction goods or services?', 'Supply of goods, as title passes on a future date upon full payment.',
          [P('p1', 'Goods', 5, 'goods'), P('p2', 'Title', 5, 'title')], 'c3'),
        V('v5', 'Name two specified actionable claims.', 'Lottery and betting; others include gambling, horse racing, casinos and online money gaming.',
          [P('p1', 'Lottery', 5, 'lottery'), P('p2', 'Betting', 5, 'betting')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Saraswati Enterprises', 'difficulty': 'core',
              'case': 'Saraswati Enterprises, registered in Gujarat and Maharashtra, gives Diwali gifts worth ₹45,000 to Ravi and ₹75,000 to Meera (employees), sends goods worth ₹4,00,000 from Gujarat to its Maharashtra unit without charge, and sells goods lying in a customs bonded warehouse to a buyer before clearance.',
              'mcqs': [
                  M('k1a', 'Gift to Ravi is:', ['Not a supply', 'A supply', 'Exempt supply', 'Zero-rated'], 0,
                    'Within ₹50,000. In practice: annual limit.', 'core', topic=T2),
                  M('k1b', 'Value of Meera\'s gift (₹) that makes it a supply:', ['75,000', '25,000', '50,000', 'Nil'], 0,
                    'Exceeds ₹50,000 — whole value. In practice: per employee.', 'core', check=75000, topic=T2),
                  M('k1c', 'The Gujarat-to-Maharashtra transfer is:', ['A supply between distinct persons', 'Not a supply', 'Exempt', 'A Schedule III item'], 0,
                    'Schedule I para 2. In practice: IGST applies.', 'core', topic=T2),
                  M('k1d', 'Sale of warehoused goods before clearance is:', ['Neither goods nor services', 'Supply of goods', 'Export', 'Supply of services'], 0,
                    'Schedule III para 8. In practice: duty paid on clearance.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch01', 1, 'Supply under GST',
                ['Explain the scope of supply under section 7.',
                 'Apply Schedule I to supplies without consideration.',
                 'Classify activities as goods or services under Schedule II.',
                 'Identify non-supplies under Schedule III.',
                 'Determine tax on composite and mixed supplies.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': [],
                 'exam_tip': 'Test in order: is it supply, is it Schedule III, then goods or services, then composite or mixed.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 7(1): supply for consideration in business; import of services; Schedule I.', 'Schedule I: assets with ITC, related/distinct persons (₹50,000 gift limit), agents, related-party imports.',
                             'Schedule II: goods vs services.', 'Schedule III: non-supplies incl. warehoused and high-sea sales.', 'Section 8: composite vs mixed.'],
                 'remember': ['Specified actionable claims are taxable.'],
                 'traps': ['Treating a mixed supply as composite.']},
                [('Supply', 'Section 7'), ('Composite/mixed', 'Section 8'), ('Without consideration', 'Schedule I'), ('Non-supply', 'Schedule III')],
                viva, cases)
