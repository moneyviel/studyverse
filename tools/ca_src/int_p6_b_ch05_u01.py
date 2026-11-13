"""CA Intermediate · Paper 6B Strategic Management · Chapter 5 Strategy Implementation and Evaluation.
Scope follows the ICAI study material; explanations, names and examples are original."""
from ikit import *

UID = 'int-p6-b-ch05-u01'
T1 = 'From formulation to implementation'
T2 = 'Structure and culture'
T3 = 'Strategic leadership and change, including digital transformation'
T4 = 'Strategic control and performance measures'


def build():
    i1 = {'id': 'i1', 'title': 'Choosing a structure', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Suggest a suitable organisation structure for each and give a reason: (a) a single-product start-up with 40 staff; (b) a company selling FMCG, paints and pharma; (c) an engineering firm running several large client projects that need specialists from many departments; (d) a group with dozens of businesses that wants each unit to plan like an independent company.',
          'solution': [table(['Case', 'Structure', 'Reason'], [
              ['(a)', 'Functional', 'Simple, specialised departments; efficient for one product'],
              ['(b)', 'Divisional (by product)', 'Each division focuses on its own market and is accountable for results'],
              ['(c)', 'Matrix', 'Project managers and functional heads share authority, pooling specialists across projects'],
              ['(d)', 'Strategic business units (SBUs)', 'Related businesses grouped into units with their own strategy and profit responsibility']], title='Organisation structures')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Is the strategy still on track?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'An airline\'s strategy assumed stable fuel prices and steady business travel. Explain how each type of strategic control would help: premise control, strategic surveillance, special alert control and implementation control.',
          'solution': [table(['Control', 'How it helps the airline'], [
              ['Premise control', 'Tracks key assumptions — fuel prices, business-travel demand — and flags when they no longer hold'],
              ['Strategic surveillance', 'Broad scanning of news, trends and industry developments for unexpected threats'],
              ['Special alert control', 'Rapid, crisis-team response to sudden events such as a pandemic or a major accident'],
              ['Implementation control', 'Checks milestones — new routes launched, cost targets met — and decides whether to continue or adjust']], title='Strategic control')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Strategy formulation decides what to do; implementation turns plans into action through structure, resources, policies, systems, leadership and culture. Good formulation fails without effective implementation, and vice versa.',
            'Implementation tasks: building an organisation capable of execution, allocating resources to strategy-critical activities, setting supportive policies, installing information and reward systems, and leading change.',
            'Formulation is mostly analytical and done by a few top managers; implementation is operational and involves the whole organisation.'],
          'A brilliant strategy on paper is worthless until people and systems act on it.',
          'A bank deciding to go digital must retrain staff, change branch roles and invest in IT — that is implementation.'),
        C('c2', T2, [
            'Structure (the "hard" side) follows strategy: functional (by function, suits single-product firms), divisional (by product, region or customer), matrix (dual reporting for projects), SBU (grouping related businesses), network or virtual (outsourced partners), and hourglass (fewer middle levels, enabled by technology).',
            'Culture (the "soft" side) is the shared values, beliefs and norms that shape behaviour; a strategy-supportive culture eases implementation, while a mismatched culture resists change.',
            'Leaders align structure and culture with strategy through communication, role models, rewards and selection.'],
          'Structure says who does what; culture decides how willingly they do it.',
          'A conservative, rule-bound culture struggles to execute a fast-innovation strategy.'),
        C('c3', T3, [
            'Strategic leadership provides vision, builds commitment and manages change. Transformational leaders inspire change and innovation; transactional leaders work through rewards and established systems — each suits different situations.',
            'Kurt Lewin\'s change model: unfreezing (making people ready for change), changing (introducing new behaviours and systems) and refreezing (making the new ways stable).',
            'Digital transformation uses technologies such as cloud, analytics, automation and AI to change business models, processes and customer experiences; it needs leadership support, new skills, data governance and attention to cyber risks.'],
          'Change sticks only when people are prepared, supported and the new way is locked in.',
          'A retailer adopting app-based ordering trains staff, revises incentives and phases out old processes.'),
        C('c4', T4, [
            'Control types: operational (individual tasks — stock, quality, cost), management (overall resource use in departments), and strategic (whether the strategy is being implemented as planned and delivering intended results).',
            'Strategic control types: premise control (checks assumptions), strategic surveillance (broad, unfocused monitoring), special alert control (rapid response to sudden events) and implementation control (milestones and step-wise review).',
            'Strategic performance measures track progress on financial and non-financial dimensions — e.g. the balanced scorecard\'s financial, customer, internal process and learning-and-growth perspectives — along with benchmarking against best performers.'],
          'Control closes the loop: are we doing what we planned, and is it working?',
          'Customer retention and employee skills are as important to track as profit.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Implementation roadmap', 'role': 'Strategy analyst trainee',
             'situation': 'A manufacturer has decided to enter export markets.',
             'steps': ['Define structural changes, such as an export division.', 'Allocate resources and set KPIs.', 'Plan communication and training for change.', 'Set premise and implementation controls.'],
             'takeaway': 'Every strategic decision needs an owner, a budget, a timeline and a measure.'}]

    mcqs = [
        Q('m1', 'Strategy implementation is primarily:', ['An operational, organisation-wide process', 'An analytical task of a few planners', 'Only budgeting', 'Only marketing'], 0,
          'Implementation involves people and systems across the organisation. In practice: needs leadership.', 'c1', T1),
        Q('m2', 'A structure with dual reporting to project and functional managers is:', ['Matrix', 'Functional', 'Divisional', 'Hourglass'], 0,
          'Matrix structures combine project and functional lines. In practice: risk of conflicting authority.', 'c2', T2),
        Q('m3', 'Culture is described as the:', ['Soft side of implementation', 'Hard side of implementation', 'Financial plan', 'Legal form'], 0,
          'Structure is hard; culture is soft. In practice: both must fit strategy.', 'c2', T2),
        Q('m4', 'In Lewin\'s model, making new behaviours stable is:', ['Refreezing', 'Unfreezing', 'Changing', 'Benchmarking'], 0,
          'Refreezing locks in the change. In practice: through rewards and policies.', 'c3', T3),
        Q('m5', 'Checking whether planning assumptions are still valid is:', ['Premise control', 'Special alert control', 'Implementation control', 'Operational control'], 0,
          'Premise control monitors key environmental and industry assumptions. In practice: focus on critical premises.', 'c4', T4),
        Q('m6', 'A rapid response to a sudden crisis is handled by:', ['Special alert control', 'Strategic surveillance', 'Premise control', 'Budgetary control'], 0,
          'Special alert control uses crisis teams for unexpected events. In practice: pandemic response.', 'c4', T4),
        Q('m7', 'The balanced scorecard includes which perspective?', ['Learning and growth', 'Political', 'Legal', 'Environmental only'], 0,
          'It covers financial, customer, internal process and learning-and-growth perspectives. In practice: links strategy to measures.', 'c4', T4),
        Q('m8', 'A leader who inspires followers to pursue a new vision is:', ['Transformational', 'Transactional', 'Laissez-faire', 'Bureaucratic'], 0,
          'Transformational leaders drive change through inspiration. In practice: suited to turbulent environments.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Functional', 1, 'concept', 'functional'), S('s2', 'Divisional', 1, 'concept', 'divisional'), S('s3', 'Matrix', 1, 'concept', 'matrix'), S('s4', 'SBU', 1, 'concept', 'sbu|business unit')],
          ['Give a reason each time.'], ['Suggesting matrix for a small start-up.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Premise', 1, 'concept', 'premise|assumption'), S('s2', 'Surveillance', 1, 'concept', 'surveillance|scanning'), S('s3', 'Special alert', 1, 'concept', 'special alert|crisis'), S('s4', 'Implementation', 1, 'concept', 'milestone|implementation')],
          ['Tie each to the airline.'], ['Defining controls without application.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'How do formulation and implementation differ?', 'Formulation decides what to do through analysis by top managers; implementation puts it into action through people, structure and systems across the organisation.',
          [P('p1', 'Formulation analysis', 5, 'analys|decide'), P('p2', 'Implementation action', 5, 'action|people')], 'c1'),
        V('v2', 'What is an SBU structure?', 'Grouping related divisions into strategic business units, each with its own strategy, managers and profit responsibility.',
          [P('p1', 'Grouping related', 5, 'related|group'), P('p2', 'Own strategy and profit', 5, 'strategy|profit')], 'c2'),
        V('v3', 'Explain Lewin\'s three stages.', 'Unfreezing prepares people for change, changing introduces new ways, and refreezing makes them stable.',
          [P('p1', 'Unfreezing', 4, 'unfreez'), P('p2', 'Changing and refreezing', 6, 'refreez')], 'c3'),
        V('v4', 'What is strategic surveillance?', 'A broad, unfocused monitoring of many information sources to detect unexpected developments affecting strategy.',
          [P('p1', 'Broad monitoring', 5, 'broad|unfocused'), P('p2', 'Unexpected developments', 5, 'unexpected|unanticipated')], 'c4'),
        V('v5', 'Name the four balanced scorecard perspectives.', 'Financial, customer, internal business process, and learning and growth.',
          [P('p1', 'Financial and customer', 5, 'financial|customer'), P('p2', 'Process and learning', 5, 'process|learning')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'NovaBank goes digital', 'difficulty': 'moderate',
              'case': 'NovaBank decides to move most services online. Branch staff fear job losses; the bank is organised by region with many management layers; the CEO holds town halls to explain the vision; a sudden cyber-attack disrupts services for a day.',
              'mcqs': [
                  M('k1a', 'The CEO\'s town halls mainly support:', ['Unfreezing in Lewin\'s model', 'Refreezing', 'Liquidation', 'Premise control'], 0,
                    'Explaining the need for change prepares people. In practice: address fears openly.', 'core', topic=T3),
                  M('k1b', 'Reducing management layers with technology moves the bank towards:', ['An hourglass structure', 'A matrix structure', 'A functional structure', 'A conglomerate'], 0,
                    'Hourglass structures shrink middle management through IT. In practice: redeploy staff.', 'moderate', topic=T2),
                  M('k1c', 'Responding to the cyber-attack calls for:', ['Special alert control', 'Strategic surveillance', 'Premise control', 'Stability strategy'], 0,
                    'A sudden crisis needs rapid, planned response. In practice: crisis teams and backup systems.', 'core', topic=T4),
                  M('k1d', 'This change is an example of:', ['Digital transformation', 'Divestment', 'Backward integration', 'Market penetration'], 0,
                    'Using technology to change processes and customer experience. In practice: needs new skills and cyber security.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-b-ch05', 1, 'Strategy Implementation and Evaluation',
                ['Distinguish formulation and implementation.',
                 'Choose structures and align culture with strategy.',
                 'Explain strategic leadership, change and digital transformation.',
                 'Apply strategic control types and performance measures.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['int-p6-b-ch04-u01'],
                 'exam_tip': 'Link each implementation tool to a fact in the case — structure, culture, leadership or control.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Formulation (what) vs implementation (how).',
                             'Structures: functional, divisional, matrix, SBU, network, hourglass.',
                             'Culture aligns behaviour; leadership drives change.',
                             'Lewin: unfreeze, change, refreeze; digital transformation.',
                             'Controls: premise, surveillance, special alert, implementation; balanced scorecard.'],
                 'remember': ['Structure follows strategy.'],
                 'traps': ['Surveillance is broad; premise control is focused on assumptions.']},
                [('Matrix', 'Dual reporting'), ('Lewin', 'Unfreeze–change–refreeze'), ('Premise control', 'Check assumptions'), ('BSC', 'Four perspectives')],
                viva, cases)
