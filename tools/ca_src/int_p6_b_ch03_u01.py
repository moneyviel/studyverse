"""CA Intermediate · Paper 6B Strategic Management · Chapter 3 Strategic Analysis: Internal Environment.
Scope follows the ICAI study material; explanations, names and examples are original."""
from ikit import *

UID = 'int-p6-b-ch03-u01'
T1 = 'Stakeholders and Mendelow\'s matrix'
T2 = 'Strategic drivers, resources and core competencies'
T3 = 'Value chain analysis'
T4 = 'SWOT, TOWS and generic business strategies'


def build():
    i1 = {'id': 'i1', 'title': 'Mapping stakeholders', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A company plans to build a factory near a village. Place these stakeholders in Mendelow\'s matrix and state how to manage each: (a) the State pollution control board; (b) villagers living nearby; (c) a large institutional shareholder; (d) suppliers of stationery.',
          'solution': [table(['Stakeholder', 'Power / Interest', 'Approach'], [
              ['(a) Pollution control board', 'High power, high interest', 'Key player — manage closely, involve early'],
              ['(b) Villagers', 'Low to moderate power, high interest', 'Keep informed; consult on concerns (power can rise through protests)'],
              ['(c) Institutional shareholder', 'High power, low interest in day-to-day', 'Keep satisfied'],
              ['(d) Stationery suppliers', 'Low power, low interest', 'Minimal effort']], title='Mendelow\'s matrix')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'From SWOT to strategy', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A regional sweets brand has a loyal customer base and secret recipes (strengths), weak online presence (weakness), rising demand for gifting boxes online (opportunity) and entry of national brands (threat). Suggest one strategy for each TOWS cell.',
          'solution': [table(['TOWS cell', 'Strategy'], [
              ['SO (use strengths to seize opportunities)', 'Launch premium online gift boxes built on signature recipes'],
              ['WO (fix weaknesses to seize opportunities)', 'Partner with e-commerce platforms to build online sales'],
              ['ST (use strengths against threats)', 'Emphasise heritage and authenticity in branding against national brands'],
              ['WT (minimise weaknesses and avoid threats)', 'Focus on core local markets while building digital skills gradually']], title='TOWS matrix')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Stakeholders are groups that affect or are affected by the organisation: shareholders, employees, customers, suppliers, lenders, Government, community and others. Their expectations may conflict.',
            'Mendelow\'s matrix maps stakeholders by power and interest: low power–low interest (minimal effort); low power–high interest (keep informed); high power–low interest (keep satisfied); high power–high interest (key players — manage closely).',
            'Positions change over time, so stakeholder mapping is repeated as strategies evolve.'],
          'Not every stakeholder needs the same attention — power and interest decide the approach.',
          'A regulator reviewing a licence is a key player during that period.'),
        C('c2', T2, [
            'Strategic drivers are the main internal and external factors shaping strategy: industry and markets, customers, products and services, channels and competition.',
            'Resources (tangible — physical, financial; intangible — brand, patents, culture; human) and capabilities (the ability to use them) form the basis of competitive advantage. Resources that are valuable, rare, hard to imitate and well organised give sustainable advantage.',
            'Core competencies are distinctive capabilities that give access to many markets, add significant customer value and are hard to imitate; they should be built and protected.'],
          'Advantage comes from what the firm has and, more importantly, what it can do with it.',
          'A two-wheeler maker\'s engine design skill is a core competence used across scooters and motorcycles.'),
        C('c3', T3, [
            'Porter\'s value chain divides activities into primary ones (getting inputs in, making the product, getting it out to buyers, selling and marketing it, and after-sales service) and support ones — firm infrastructure, human resource management, technology development and procurement.',
            'Analysing costs and value at each step shows where the firm can lower cost or add distinctiveness; linkages between activities and with suppliers and buyers (the value system) also matter.',
            'Outsourcing non-core activities and strengthening core ones follows from value chain analysis.'],
          'Each activity in the chain should either cut cost or add value the customer pays for.',
          'An e-retailer\'s fast delivery (outbound logistics) is a key source of value.'),
        C('c4', T4, [
            'SWOT lists internal strengths and weaknesses and external opportunities and threats; the TOWS matrix converts them into SO, WO, ST and WT strategies.',
            'Porter\'s generic business strategies: cost leadership (lowest cost producer, broad market), differentiation (unique features customers value, premium price) and focus (cost focus or differentiation focus on a narrow segment). Best-cost provider combines good quality with lower cost.',
            'Each strategy has risks: cost leaders may be undercut by technology change; differentiators may lose uniqueness through imitation; focusers may see the niche disappear.'],
          'SWOT describes the situation; TOWS turns it into options; generic strategies define the competitive position.',
          'A budget airline follows cost leadership; a boutique resort follows differentiation focus.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Internal capability audit', 'role': 'Strategy analyst trainee',
             'situation': 'A mid-size manufacturer wants to know what gives it an edge.',
             'steps': ['List resources and capabilities.', 'Test them for value, rarity and imitability.', 'Map the value chain and costs.', 'Summarise in SWOT and TOWS.'],
             'takeaway': 'True advantages are scarce — most capabilities are simply necessary to compete.'}]

    mcqs = [
        Q('m1', 'In Mendelow\'s matrix, high power and high interest stakeholders are:', ['Key players', 'Minimal effort', 'Keep informed', 'Keep satisfied'], 0,
          'They need close management and involvement. In practice: regulators or major investors.', 'c1', T1),
        Q('m2', 'Low power, high interest stakeholders should be:', ['Kept informed', 'Ignored', 'Kept satisfied', 'Managed closely'], 0,
          'They may influence others and gain power. In practice: community groups.', 'c1', T1),
        Q('m3', 'A core competence:', ['Gives access to many markets and is hard to imitate', 'Is any routine activity', 'Is easily copied', 'Is only a physical asset'], 0,
          'Core competencies are distinctive and widely applicable. In practice: protect and build them.', 'c2', T2),
        Q('m4', 'Which is a primary activity in Porter\'s value chain?', ['Outbound logistics', 'Procurement', 'Human resource management', 'Technology development'], 0,
          'Primary activities: inbound, operations, outbound, marketing and sales, service. In practice: support activities enable them.', 'c3', T3),
        Q('m5', 'A WO strategy:', ['Overcomes weaknesses by using opportunities', 'Uses strengths against threats', 'Uses strengths to exploit opportunities', 'Minimises weaknesses and avoids threats'], 0,
          'TOWS cells match internal and external factors. In practice: partnerships often fill weaknesses.', 'c4', T4),
        Q('m6', 'Charging a premium for unique features is:', ['Differentiation', 'Cost leadership', 'Cost focus', 'Retrenchment'], 0,
          'Differentiation relies on attributes customers value. In practice: risk of imitation.', 'c4', T4),
        Q('m7', 'A risk of cost leadership is:', ['Technology change that lets rivals cut costs further', 'Customers paying too much', 'Too much uniqueness', 'Niche disappearing'], 0,
          'Cost advantages can be eroded by new technology or imitation. In practice: keep improving efficiency.', 'c4', T4),
        Q('m8', 'Brand reputation is a(n):', ['Intangible resource', 'Tangible resource', 'Primary activity', 'Threat'], 0,
          'Intangible resources include brands, patents and culture. In practice: often hardest to copy.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Key player', 1, 'concept', 'key player'), S('s2', 'Keep informed', 1, 'concept', 'informed'), S('s3', 'Keep satisfied', 1, 'concept', 'satisfied'), S('s4', 'Minimal effort', 1, 'concept', 'minimal')],
          ['Justify power and interest.'], ['Treating all stakeholders alike.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'SO and WO', 2, 'concept', 'opportunit'), S('s2', 'ST and WT', 2, 'concept', 'threat')],
          ['Link each strategy to the factors.'], ['Repeating SWOT instead of strategies.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is Mendelow\'s matrix?', 'A tool that maps stakeholders by their power and interest to decide how closely to manage each group.',
          [P('p1', 'Power and interest', 6, 'power|interest'), P('p2', 'Management approach', 4, 'manage')], 'c1'),
        V('v2', 'What are the tests of a core competence?', 'It gives access to a wide range of markets, contributes significantly to customer benefits and is difficult for competitors to imitate.',
          [P('p1', 'Markets and value', 5, 'market|customer'), P('p2', 'Hard to imitate', 5, 'imitate')], 'c2'),
        V('v3', 'Name the support activities in the value chain.', 'Firm infrastructure, human resource management, technology development and procurement.',
          [P('p1', 'Infrastructure and HR', 5, 'infrastructure|human'), P('p2', 'Technology and procurement', 5, 'technology|procurement')], 'c3'),
        V('v4', 'How does TOWS differ from SWOT?', 'SWOT lists factors; TOWS matches them to generate SO, WO, ST and WT strategies.',
          [P('p1', 'Matching', 5, 'match'), P('p2', 'Strategies', 5, 'strateg')], 'c4'),
        V('v5', 'What is a focus strategy?', 'Concentrating on a narrow segment and serving it with either lower cost or differentiation better than broad competitors.',
          [P('p1', 'Narrow segment', 6, 'narrow|segment'), P('p2', 'Cost or differentiation', 4, 'cost|different')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Pristine Water Purifiers', 'difficulty': 'moderate',
              'case': 'Pristine sells water purifiers. It has a patented filter, a strong service network and an old ERP system. Demand is growing in small towns, while cheap imports are rising. It wants to keep prices premium.',
              'mcqs': [
                  M('k1a', 'The patented filter is best described as:', ['A strength and potential core competence', 'A weakness', 'An opportunity', 'A threat'], 0,
                    'It is internal, valuable and hard to imitate. In practice: protect the patent.', 'core', topic=T2),
                  M('k1b', 'The service network belongs in the value chain under:', ['Service (primary activity)', 'Procurement', 'Firm infrastructure', 'Inbound logistics'], 0,
                    'After-sales service is a primary activity. In practice: a differentiator here.', 'core', topic=T3),
                  M('k1c', 'Using the strong service network to grow in small towns is a(n):', ['SO strategy', 'WT strategy', 'ST strategy', 'WO strategy'], 0,
                    'A strength used to exploit an opportunity. In practice: add local partners.', 'moderate', topic=T4),
                  M('k1d', 'Keeping premium prices with unique features reflects:', ['Differentiation strategy', 'Cost leadership', 'Cost focus', 'Liquidation'], 0,
                    'Premium price requires features customers value. In practice: guard against cheap imports through brand.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p6', 'int-p6-b-ch03', 1, 'Strategic Analysis: Internal Environment',
                ['Analyse stakeholders with Mendelow\'s matrix.',
                 'Identify strategic drivers, resources and core competencies.',
                 'Apply value chain analysis.',
                 'Use SWOT/TOWS and choose generic business strategies.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p6-b-ch02-u01'],
                 'exam_tip': 'When asked for strategies from a SWOT, use the TOWS cells explicitly.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Mendelow: power × interest → four approaches.',
                             'Resources, capabilities, core competencies.',
                             'Value chain: 5 primary + 4 support activities.',
                             'SWOT → TOWS; cost leadership, differentiation, focus, best-cost.'],
                 'remember': ['Core competencies are hard to imitate.'],
                 'traps': ['SWOT strengths/weaknesses are internal only.']},
                [('Key players', 'High power, high interest'), ('Value chain', 'Primary + support'), ('Generic strategies', 'Cost, differentiation, focus')],
                viva, cases)
