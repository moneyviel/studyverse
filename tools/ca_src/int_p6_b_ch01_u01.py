"""CA Intermediate · Paper 6B Strategic Management · Chapter 1 Introduction to Strategic Management.
Scope follows the ICAI study material; explanations, names and examples are original."""
from ikit import *

UID = 'int-p6-b-ch01-u01'
T1 = 'Strategy and strategic management'
T2 = 'Importance and limitations of strategic management'
T3 = 'Strategic intent: vision, mission, goals, objectives and values'
T4 = 'Levels of strategy'


def build():
    i1 = {'id': 'i1', 'title': 'Writing strategic intent', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'GreenRide is an Indian start-up that rents electric scooters in cities. Draft a vision, a mission, two goals, two measurable objectives and two values for it, and explain how each differs.',
          'solution': [table(['Element', 'Example for GreenRide', 'What it does'], [
              ['Vision', 'Cities where every short trip is clean, cheap and quick', 'Describes the desired long-term future; inspiring, not measurable'],
              ['Mission', 'We provide affordable, app-based electric scooter rentals that make urban commuting greener', 'States purpose, customers and business scope today'],
              ['Goals', 'Become the most trusted e-mobility brand in tier-2 cities; build a profitable charging network', 'Broad results to aim for'],
              ['Objectives', 'Reach 50,000 monthly riders by March 2028; cut cost per ride by 15% in two years', 'Specific, measurable and time-bound targets'],
              ['Values', 'Safety first; honesty with riders and partners', 'Beliefs guiding behaviour and decisions']], title='Strategic intent')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Which level decides?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Classify each decision of a diversified group by strategy level: (a) whether to enter the insurance business; (b) how its hotel division competes against luxury chains; (c) the HR department\'s plan for training front-office staff; (d) whether to sell the loss-making textiles business.',
          'solution': [table(['Decision', 'Level', 'Reason'], [
              ['(a)', 'Corporate', 'Choice of businesses the group will be in'],
              ['(b)', 'Business', 'How one business competes in its market'],
              ['(c)', 'Functional', 'Supports business strategy within one function'],
              ['(d)', 'Corporate', 'Portfolio decision about exiting a business']], title='Levels of strategy')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Strategy is a long-range, integrated plan that sets the direction and scope of an organisation and positions it to gain advantage in a changing environment. It is partly planned (deliberate) and partly emerging from responses to events.',
            'Strategic management is the continuous process of analysing the environment, setting direction, choosing strategies, implementing them and evaluating results to achieve long-term objectives.',
            'Strategic decisions are future-oriented, involve large commitments of resources, affect the whole organisation, are taken by top management, and are often hard to reverse.'],
          'Strategy is the game plan; strategic management is coaching the team through the whole season.',
          'A mobile phone maker deciding to manufacture in India rather than import is a strategic decision.'),
        C('c2', T2, [
            'Importance: gives a clear direction; helps anticipate change; allocates resources to priorities; builds sustainable competitive advantage; improves coordination; and prepares the firm to handle risks and opportunities.',
            'Limitations: environment is complex and fast-changing, so plans can become outdated; strategic planning is time-consuming and costly; long-term predictions are uncertain; and success depends on implementation, which plans alone cannot guarantee.',
            'Strategic management works best when combined with flexibility and learning.'],
          'A strategy is useful only if the organisation can adapt it as the world changes.',
          'Many retailers had to rewrite plans quickly when online shopping surged.'),
        C('c3', T3, [
            'Strategic intent is the leveraging of resources and capabilities to achieve a desired future; it is expressed through vision, mission, goals and objectives, and values.',
            'Vision describes what the organisation aspires to become; mission defines its purpose, customers, products and philosophy; goals are broad results; objectives are specific, measurable and time-bound targets that operationalise goals.',
            'Values are the shared beliefs that guide behaviour. A good mission is clear, feasible, motivating and distinctive; objectives should be SMART and consistent with each other.'],
          'Vision points to the destination; mission explains the journey; objectives mark the milestones.',
          '"Clean energy for every home" is a vision; "install 10 lakh solar roofs by 2030" is an objective.'),
        C('c4', T4, [
            'Corporate-level strategy decides which businesses to be in and how to allocate resources among them (growth, stability, retrenchment, diversification).',
            'Business-level strategy decides how each business unit competes in its market (cost leadership, differentiation, focus).',
            'Functional-level strategy covers marketing, finance, operations, HR and R&D plans supporting business strategy. The three levels form a network: corporate sets the frame, business adapts it to markets, functions execute — with feedback flowing upward.'],
          'Corporate asks "where?", business asks "how?", functions ask "with what actions?".',
          'A group choosing to exit cement is corporate; its cement unit\'s pricing plan is business; the plant\'s maintenance plan is functional.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Board strategy workshop', 'role': 'Strategy analyst trainee',
             'situation': 'A family business asks for help writing its first vision and mission.',
             'steps': ['Interview founders about long-term aspirations.', 'Identify customers, offerings and values.', 'Draft vision and mission statements.', 'Convert goals into SMART objectives.'],
             'takeaway': 'Strategic intent turns family ambitions into shared, measurable direction.'}]

    mcqs = [
        Q('m1', 'Strategic decisions are generally:', ['Long-term and resource-intensive', 'Routine and short-term', 'Taken by junior staff', 'Easily reversible'], 0,
          'They commit significant resources and shape the future. In practice: made by top management.', 'c1', T1),
        Q('m2', 'Which statement describes "what we want to become"?', ['Vision', 'Mission', 'Objective', 'Policy'], 0,
          'Vision expresses the desired future state. In practice: mission explains present purpose.', 'c3', T3),
        Q('m3', 'Objectives differ from goals because they are:', ['Specific, measurable and time-bound', 'Broad and inspiring', 'Unwritten', 'Only financial'], 0,
          'Objectives make goals operational. In practice: use SMART criteria.', 'c3', T3),
        Q('m4', 'Deciding which industries a group should operate in is:', ['Corporate-level strategy', 'Business-level strategy', 'Functional strategy', 'Operational tactic'], 0,
          'Portfolio scope is a corporate decision. In practice: involves acquisitions and exits.', 'c4', T4),
        Q('m5', 'A limitation of strategic management is:', ['Plans may become outdated in a fast-changing environment', 'It gives direction', 'It aids resource allocation', 'It builds competitive advantage'], 0,
          'Uncertainty and change can make plans obsolete. In practice: review strategies periodically.', 'c2', T2),
        Q('m6', 'How a business unit competes against rivals is decided at the:', ['Business level', 'Corporate level', 'Functional level', 'Board level only'], 0,
          'Business strategy addresses competitive positioning. In practice: cost leadership or differentiation choices.', 'c4', T4),
        Q('m7', 'Strategic intent refers to:', ['Leveraging resources and capabilities to reach a desired future', 'Annual budget targets', 'Daily operating rules', 'Financial statements'], 0,
          'It is expressed through vision, mission, goals, objectives and values. In practice: aligns the organisation.', 'c3', T3),
        Q('m8', 'An emergent strategy is one that:', ['Develops from responses to unforeseen events', 'Is fully planned in advance', 'Is imposed by law', 'Never changes'], 0,
          'Realised strategy often blends deliberate plans and emergent responses. In practice: stay adaptable.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Vision and mission', 2, 'concept', 'vision|mission'), S('s2', 'Goals and objectives', 2, 'concept', 'objective|measurable'), S('s3', 'Values', 1, 'concept', 'values')],
          ['Make objectives measurable.'], ['Writing vision as a target.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Corporate', 2, 'concept', 'corporate'), S('s2', 'Business', 1, 'concept', 'business'), S('s3', 'Functional', 1, 'concept', 'functional')],
          ['Give a reason for each.'], ['Treating divestment as business-level.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is strategic management?', 'A continuous process of analysing the environment, setting direction, choosing and implementing strategies and evaluating results to achieve long-term objectives.',
          [P('p1', 'Analysis and choice', 5, 'analys|choos'), P('p2', 'Implementation and evaluation', 5, 'implement|evaluat')], 'c1'),
        V('v2', 'Distinguish vision and mission.', 'Vision describes the desired future the organisation aspires to; mission states its current purpose, customers and scope.',
          [P('p1', 'Vision future', 5, 'future|aspire'), P('p2', 'Mission purpose', 5, 'purpose|customers')], 'c3'),
        V('v3', 'Give two limitations of strategic management.', 'The environment changes quickly so plans may become outdated, and the process is time-consuming and costly.',
          [P('p1', 'Change', 5, 'change|outdated'), P('p2', 'Cost or time', 5, 'cost|time')], 'c2'),
        V('v4', 'Name the three levels of strategy.', 'Corporate level, business level and functional level.',
          [P('p1', 'Corporate', 4, 'corporate'), P('p2', 'Business and functional', 6, 'business|functional')], 'c4'),
        V('v5', 'What makes an objective useful?', 'It should be specific, measurable, achievable, relevant and time-bound, and consistent with the mission.',
          [P('p1', 'SMART', 6, 'specific|measurable'), P('p2', 'Time-bound', 4, 'time')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Foods Group', 'difficulty': 'core',
              'case': 'Saffron Foods Group runs packaged snacks, a restaurant chain and a dairy. The board plans to sell the dairy, the snacks business wants to compete on low prices, and the restaurant chain\'s HR team designs a new training programme. The group\'s statement reads: "To bring healthy Indian flavours to every family."',
              'mcqs': [
                  M('k1a', 'Selling the dairy is a:', ['Corporate-level decision', 'Business-level decision', 'Functional decision', 'Operational decision'], 0,
                    'Exiting a business changes the group\'s portfolio. In practice: decided by the board.', 'core', topic=T4),
                  M('k1b', 'Competing on low prices in snacks is a:', ['Business-level strategy', 'Corporate strategy', 'Functional strategy', 'Vision'], 0,
                    'It concerns how one business competes. In practice: requires cost efficiency.', 'core', topic=T4),
                  M('k1c', 'The HR training programme is a:', ['Functional-level strategy', 'Corporate strategy', 'Business strategy', 'Mission'], 0,
                    'It supports the restaurant business through one function. In practice: linked to service quality.', 'core', topic=T4),
                  M('k1d', '"To bring healthy Indian flavours to every family" is best described as a:', ['Vision or mission statement', 'SMART objective', 'Functional policy', 'Budget'], 0,
                    'It is broad and inspirational, not measurable. In practice: needs objectives to measure progress.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-b-ch01', 1, 'Introduction to Strategic Management',
                ['Explain strategy, strategic decisions and strategic management.',
                 'Discuss the importance and limitations of strategic management.',
                 'Formulate vision, mission, goals, objectives and values.',
                 'Distinguish corporate, business and functional strategy.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['int-p6-a-ch09-u06'],
                 'exam_tip': 'In case questions, quote the fact from the case and tie it to the concept — examiners reward application.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Strategy: long-term direction and scope; deliberate plus emergent.',
                             'Strategic decisions: long-term, resource-heavy, top-level, hard to reverse.',
                             'Importance vs limitations.',
                             'Vision → mission → goals → SMART objectives; values guide conduct.',
                             'Corporate (where), business (how to compete), functional (actions).'],
                 'remember': ['Objectives must be measurable.'],
                 'traps': ['Divestment is corporate-level, not business-level.']},
                [('Vision', 'Desired future'), ('Mission', 'Purpose today'), ('Corporate level', 'Which businesses'), ('Business level', 'How to compete')],
                viva, cases)
