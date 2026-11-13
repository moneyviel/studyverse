"""CA Intermediate · Paper 6B Strategic Management · Chapter 2 Strategic Analysis: External Environment.
Scope follows the ICAI study material; explanations, names and examples are original."""
from ikit import *

UID = 'int-p6-b-ch02-u01'
T1 = 'Business environment and PESTLE analysis'
T2 = 'Product, industry and the industry life cycle'
T3 = 'Porter\'s five forces'
T4 = 'Key success factors, strategic groups and competitor analysis'


def build():
    i1 = {'id': 'i1', 'title': 'PESTLE for electric two-wheelers', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'An Indian company plans to launch electric two-wheelers. Give one factor under each PESTLE head and its likely effect.',
          'solution': [table(['Head', 'Factor', 'Effect'], [
              ['Political', 'Government push for clean mobility and local manufacturing', 'Supportive policies and incentives'],
              ['Economic', 'Fuel price levels and consumer credit availability', 'Running-cost savings drive demand; EMIs make purchase easier'],
              ['Social', 'Young urban buyers\' interest in sustainability and app-based services', 'Positive acceptance; need for digital features'],
              ['Technological', 'Falling battery costs and better charging infrastructure', 'Lower prices, longer range'],
              ['Legal', 'Battery safety standards and vehicle certification rules', 'Higher compliance cost; safer products'],
              ['Environmental', 'Urban air pollution concerns and battery disposal issues', 'Demand boost; need for recycling plans']], title='PESTLE analysis')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'How attractive is the industry?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Apply Porter\'s five forces to the Indian quick-commerce grocery delivery industry and conclude on its attractiveness.',
          'solution': [table(['Force', 'Assessment'], [
              ['Threat of new entrants', 'High — well-funded players can enter, though dark-store networks and brand recall create some barriers'],
              ['Bargaining power of buyers', 'High — customers switch apps easily and compare prices'],
              ['Bargaining power of suppliers', 'Moderate — big brands have power; local suppliers have little'],
              ['Threat of substitutes', 'High — neighbourhood stores, supermarkets and e-commerce'],
              ['Rivalry among existing firms', 'Intense — heavy discounting and fast expansion']], title='Five forces'),
              p('With most forces strong, average profitability is likely to be low unless a firm builds scale, efficiency and loyalty.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The business environment comprises forces outside the firm that affect its performance: the micro environment (customers, suppliers, competitors, intermediaries, public) and the macro environment (broad forces).',
            'PESTLE examines political, economic, social, technological, legal and environmental factors to spot opportunities and threats.',
            'Environmental analysis must be continuous, because changes in regulation, technology or consumer behaviour can quickly reshape an industry.'],
          'Scanning the environment is like checking the weather before a voyage.',
          'A change in data-protection law affects every app-based business — a legal factor.'),
        C('c2', T2, [
            'A product is anything offered to satisfy a need; an industry is a group of firms offering close substitutes. Dominant economic features include market size and growth, number of rivals, scale economies, technology change and capital needs.',
            'Industries and products pass through a life cycle: introduction (low sales, high costs), growth (rising sales, new entrants), maturity (slow growth, intense competition) and decline (falling demand, exits). Strategies differ by stage.',
            'Understanding the market and customers — segments, needs, buying behaviour — is essential for positioning.'],
          'Where an industry is in its life cycle shapes what strategies make sense.',
          'Landline phones are in decline; EV charging is in growth.'),
        C('c3', T3, [
            'Porter\'s five forces explain industry profitability: threat of new entrants (barriers such as scale, capital, brand, regulation), bargaining power of buyers, bargaining power of suppliers, threat of substitutes, and rivalry among existing competitors.',
            'Strong forces squeeze average profits; weak forces allow higher returns. Firms use the analysis to position themselves where forces are weakest or to influence them.',
            'Rivalry is intense when competitors are many and equal, growth is slow, fixed costs are high, products are similar and exit barriers are high.'],
          'Profitability depends not just on rivals but on five pressures around the industry.',
          'Airlines face strong buyers, powerful suppliers (aircraft makers), substitutes (trains) and fierce rivalry.'),
        C('c4', T4, [
            'Key success factors (KSFs) are the few things a firm must do well to succeed in an industry, such as distribution reach in FMCG or technology in software.',
            'Strategic groups cluster firms that follow similar strategies (price, quality, geographic scope); rivalry is strongest within a group.',
            'Competitor analysis studies rivals\' objectives, strategies, strengths and likely moves. Together with KSFs, this helps choose competitive strategy.'],
          'Know what wins in your industry and who you are really competing with.',
          'Luxury car makers form a strategic group distinct from budget car makers.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Industry note for a lender', 'role': 'Strategy analyst trainee',
             'situation': 'A bank asks for an industry view before lending to a cement maker.',
             'steps': ['Run PESTLE for the industry.', 'Assess five forces.', 'Identify KSFs and the client\'s strategic group.', 'Conclude on risks and prospects.'],
             'takeaway': 'Industry structure often explains more about future profits than the firm\'s own past.'}]

    mcqs = [
        Q('m1', 'In PESTLE, a change in consumer lifestyles falls under:', ['Social', 'Political', 'Legal', 'Technological'], 0,
          'Lifestyles, demographics and culture are social factors. In practice: affect product design.', 'c1', T1),
        Q('m2', 'Which force is weakened by high capital requirements?', ['Threat of new entrants', 'Buyer power', 'Supplier power', 'Rivalry'], 0,
          'High capital needs are an entry barrier. In practice: steel and telecom have such barriers.', 'c3', T3),
        Q('m3', 'Rivalry is intense when:', ['Industry growth is slow and products are similar', 'There are few unequal rivals', 'Exit is easy', 'Products are highly differentiated'], 0,
          'Slow growth and commoditised products push firms to fight for share. In practice: price wars follow.', 'c3', T3),
        Q('m4', 'Buyers are powerful when:', ['Switching costs are low and buyers are concentrated', 'Products are unique', 'Buyers are scattered', 'Information is scarce'], 0,
          'Easy switching and big buyers raise bargaining power. In practice: large retailers squeeze suppliers.', 'c3', T3),
        Q('m5', 'During the maturity stage of the industry life cycle:', ['Growth slows and competition intensifies', 'Sales are very low', 'Many new entrants arrive', 'Demand collapses'], 0,
          'Maturity brings saturation and share battles. In practice: cost efficiency matters.', 'c2', T2),
        Q('m6', 'Key success factors are:', ['Things a firm must do well to succeed in an industry', 'Financial ratios only', 'Government incentives', 'Personal goals of managers'], 0,
          'KSFs vary by industry. In practice: distribution, technology or brand.', 'c4', T4),
        Q('m7', 'A strategic group is:', ['Firms in an industry following similar strategies', 'A board committee', 'A trade union', 'All firms in the economy'], 0,
          'Mapping strategic groups shows closest rivals. In practice: use price and scope axes.', 'c4', T4),
        Q('m8', 'The threat of substitutes refers to:', ['Products from other industries meeting the same need', 'New firms in the same industry', 'Suppliers raising prices', 'Buyers demanding discounts'], 0,
          'Substitutes cap prices. In practice: video calls substitute business travel.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Political and economic', 2, 'concept', 'political|economic'), S('s2', 'Social and technological', 2, 'concept', 'social|technolog'), S('s3', 'Legal and environmental', 2, 'concept', 'legal|environment')],
          ['One clear factor per head.'], ['Mixing legal with political.'], ['Table.'], pad='table'),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Entry and substitutes', 2, 'concept', 'entrant|substitut'), S('s2', 'Buyers and suppliers', 2, 'concept', 'buyer|supplier'), S('s3', 'Rivalry and conclusion', 1, 'concept', 'rivalry|profit')],
          ['End with a conclusion.'], ['Listing forces without assessment.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is PESTLE analysis?', 'A tool for scanning the macro environment under political, economic, social, technological, legal and environmental factors.',
          [P('p1', 'Macro environment', 5, 'macro|environment'), P('p2', 'Six factors', 5, 'political|economic|social')], 'c1'),
        V('v2', 'Name Porter\'s five forces.', 'Threat of new entrants, bargaining power of buyers, bargaining power of suppliers, threat of substitutes and rivalry among existing competitors.',
          [P('p1', 'Entrants and substitutes', 5, 'entrant|substitut'), P('p2', 'Buyers, suppliers, rivalry', 5, 'buyer|supplier|rivalry')], 'c3'),
        V('v3', 'What happens in the growth stage of an industry?', 'Sales rise rapidly, new competitors enter and firms invest in capacity and brand building.',
          [P('p1', 'Rising sales', 5, 'rise|rapid'), P('p2', 'New entrants', 5, 'enter|competitor')], 'c2'),
        V('v4', 'Why identify key success factors?', 'To focus resources on the few capabilities that decide success in the industry.',
          [P('p1', 'Focus', 5, 'focus'), P('p2', 'Decisive capabilities', 5, 'capabilit|success')], 'c4'),
        V('v5', 'Give two entry barriers.', 'Economies of scale and high capital requirements, along with brand loyalty and regulation.',
          [P('p1', 'Scale or capital', 5, 'scale|capital'), P('p2', 'Brand or regulation', 5, 'brand|regulat|licen')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'BrewCraft Coffee', 'difficulty': 'moderate',
              'case': 'BrewCraft runs premium cafés in metro cities. Coffee bean prices are rising due to poor harvests, many new cafés are opening, customers easily switch to rivals or make coffee at home, and the Government is considering higher taxes on packaged beverages.',
              'mcqs': [
                  M('k1a', 'Rising bean prices relate to:', ['Bargaining power of suppliers', 'Threat of substitutes', 'Buyer power', 'Rivalry'], 0,
                    'Input scarcity strengthens suppliers. In practice: consider long-term contracts.', 'core', topic=T3),
                  M('k1b', 'Home-brewed coffee is a:', ['Substitute', 'New entrant', 'Supplier', 'Strategic group'], 0,
                    'It meets the same need from outside the café industry. In practice: limits pricing power.', 'core', topic=T3),
                  M('k1c', 'Possible higher beverage taxes are a(n):', ['Political/legal factor in PESTLE', 'Social factor', 'Technological factor', 'Environmental factor'], 0,
                    'Government policy and law fall under political and legal. In practice: monitor budget announcements.', 'core', topic=T1),
                  M('k1d', 'Many new cafés opening indicates:', ['Low entry barriers and rising rivalry', 'High entry barriers', 'Decline stage', 'Strong buyer loyalty'], 0,
                    'Easy entry increases competition. In practice: differentiate through experience.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-b-ch02', 1, 'Strategic Analysis: External Environment',
                ['Explain the business environment and apply PESTLE.',
                 'Analyse products, industries and life cycles.',
                 'Apply Porter\'s five forces.',
                 'Identify KSFs and strategic groups.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p6-b-ch01-u01'],
                 'exam_tip': 'Always end a five-forces or PESTLE answer with an overall conclusion about the industry.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Micro and macro environment; PESTLE.',
                             'Industry life cycle: introduction, growth, maturity, decline.',
                             'Five forces: entrants, buyers, suppliers, substitutes, rivalry.',
                             'KSFs, strategic groups, competitor analysis.'],
                 'remember': ['Strong forces mean lower average profits.'],
                 'traps': ['Substitutes come from other industries, not rivals.']},
                [('PESTLE', 'Six macro factors'), ('Five forces', 'Industry profitability'), ('KSF', 'Must-do-well factors')],
                viva, cases)
