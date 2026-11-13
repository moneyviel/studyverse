"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 8 Disclosures (Ind AS 112 and group disclosures).
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u08'
T1 = 'Objective and significant judgements'
T2 = 'Interests in subsidiaries'
T3 = 'Interests in joint arrangements and associates'
T4 = 'Unconsolidated structured entities and Schedule III'


def build():
    ck = Checks()
    p = ck.add('0.3*50', 'Profit allocated to NCI (₹ crore)')
    d = ck.add('0.3*20', 'Dividends paid to NCI (₹ crore)')
    acc = ck.add('90+0.3*50-0.3*20', 'Accumulated NCI at year end (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Material NCI disclosure', 'difficulty': 'core', 'minutes': 7,
          'q': 'Quartz Ltd. owns 70% of Ruby Ltd., which has material NCI. Opening NCI ₹90 crore; Ruby\'s profit ₹50 crore; dividends ₹20 crore. Compute the NCI figures disclosed and list other required items.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Profit allocated to NCI', '30% × 50', inr(p)],
              ['Dividends paid to NCI', '30% × 20', inr(d)],
              ['Accumulated NCI', '90 + 15 − 6', inr(acc)],
              ['Also disclose', 'Name, principal place of business, NCI ownership and voting %, summarised financial information', '—']], title='Ind AS 112 NCI')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Judgements to disclose', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Quartz holds 45% of Sapphire Ltd. and consolidates it (de facto control); holds 55% of Topaz Ltd. but does not consolidate (another party has rights to direct activities); and holds 18% of Onyx Ltd., treated as an associate. What judgements must be disclosed?',
          'solution': [table(['Investee', 'Judgement to disclose'], [
              ['Sapphire', 'Why it controls despite holding under half the votes'],
              ['Topaz', 'Why it lacks control despite holding more than half the votes'],
              ['Onyx', 'Why it has significant influence below 20%']], title='Significant judgements')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 112 aims for disclosures that help users evaluate the nature of, and risks associated with, interests in other entities, and the effects of those interests on the financial position, performance and cash flows.',
            'Entities disclose significant judgements and assumptions in deciding: whether they control another entity; have joint control or significant influence; and the type of joint arrangement when structured through a separate vehicle.',
            'Typical examples: control with less than half the votes, no control with more than half, significant influence below 20%, and being an agent or principal. Investment entities disclose judgements about that status.'],
          'Explain the hard calls behind the group structure.',
          'Consolidating a 45% investee needs a stated reason.'),
        C('c2', T2, [
            'For subsidiaries: the composition of the group; for each subsidiary with material NCI — name, principal place of business, NCI ownership and voting shares, profit allocated to NCI, accumulated NCI and summarised financial information (including dividends to NCI).',
            'Significant restrictions on access to or use of group assets and settling liabilities (e.g. regulatory limits on dividends); risks from consolidated structured entities (e.g. support commitments).',
            'Consequences of changes in ownership without loss of control (schedule of effects on parent equity), and gains or losses on loss of control with the portion from remeasuring retained interest.'],
          'Show outsiders\' stakes and the strings on group assets.',
          'A foreign subsidiary unable to remit cash must disclose the restriction.'),
        C('c3', T3, [
            'For each material joint arrangement and associate: name, nature of relationship, principal place of business, ownership interest, and measurement method (equity method or fair value).',
            'For each material joint venture and associate: dividends received and summarised financial information; for joint ventures, more detail (cash, current financial liabilities, depreciation, interest, tax). Fair value if quoted prices exist.',
            'Aggregate information for individually immaterial ones; commitments and contingent liabilities relating to joint ventures and associates; unrecognised share of losses.'],
          'Material investees get their own summary figures.',
          'Unrecognised losses in an associate are disclosed.'),
        C('c4', T4, [
            'A structured entity is designed so that voting rights are not the dominant factor in deciding who controls it (e.g. securitisation vehicles, certain funds). For unconsolidated structured entities in which an entity has interests: nature, purpose, size, activities, financing; carrying amounts of assets and liabilities recognised; maximum exposure to loss and how it is determined; and support provided.',
            'Sponsored structured entities with no interest at year end: how the entity decides which it sponsors, income earned and assets transferred.',
            'Division II of Schedule III to the Companies Act also requires, in consolidated statements, a table showing each entity\'s share of net assets and profit or loss (and OCI and total comprehensive income) as a percentage of consolidated amounts, including NCI, associates and joint ventures.'],
          'Off-balance-sheet vehicles need risk disclosures; Schedule III adds an entity-wise table.',
          'A bank sponsoring a securitisation trust discloses its maximum exposure.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing Ind AS 112 notes', 'role': 'Reporting analyst',
             'situation': 'Group has 20 subsidiaries, 3 JVs, 5 associates and 2 securitisation trusts.',
             'steps': ['List significant judgements on control and influence.', 'Identify subsidiaries with material NCI.', 'Prepare summarised financial information for material JVs and associates.', 'Disclose exposure to unconsolidated structured entities.'],
             'takeaway': 'Materiality decides which investees get individual disclosure.'}]

    mcqs = [
        Q('m1', 'Ind AS 112 requires disclosure of significant judgements about:', ['Control, joint control and significant influence', 'Tax rates', 'Revenue recognition', 'Lease terms'], 0,
          'Judgements behind the structure. In practice: unusual percentages.', 'c1', T1),
        Q('m2', 'For subsidiaries with material NCI, the entity discloses:', ['Summarised financial information and NCI share of profit', 'Nothing', 'Only names', 'Only dividends'], 0,
          'Detailed NCI information. In practice: by subsidiary.', 'c2', T2),
        Q('m3', 'A structured entity is one where:', ['Voting rights are not the dominant factor in control', 'Voting decides control', 'Shares are listed', 'It is a branch'], 0,
          'Contracts usually decide. In practice: securitisation vehicles.', 'c4', T4),
        Q('m4', 'For unconsolidated structured entities, the entity discloses:', ['Maximum exposure to loss', 'Nothing', 'Only names', 'Only revenue'], 0,
          'Risk-focused disclosure. In practice: explain how determined.', 'c4', T4),
        Q('m5', 'Significant restrictions on using group assets are disclosed under:', ['Interests in subsidiaries', 'Ind AS 7', 'Ind AS 16', 'Ind AS 37'], 0,
          'Part of Ind AS 112. In practice: regulatory capital.', 'c2', T2),
        Q('m6', 'Unrecognised share of losses of an associate is:', ['Disclosed', 'Recognised', 'Ignored', 'Deferred'], 0,
          'Users need the exposure. In practice: for the period and cumulatively.', 'c3', T3),
        Q('m7', 'Schedule III Division II requires, in consolidated statements:', ['Each entity\'s share of net assets and profit as a percentage', 'Only parent figures', 'Tax computations', 'Segment data'], 0,
          'Additional Indian requirement. In practice: include associates and JVs.', 'c4', T4),
        Q('m8', 'Effects of changes in ownership without loss of control are disclosed as:', ['A schedule of effects on parent\'s equity', 'A P&L gain', 'Goodwill movement', 'OCI'], 0,
          'Equity transactions are visible. In practice: show consideration and NCI change.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Profit to NCI', 1.5, 'computation', 'profit', nums=[p]), S('s2', 'Dividends', 1.5, 'computation', 'dividend', nums=[d]), S('s3', 'Accumulated', 2, 'computation', 'accumulated', nums=[acc])],
          ['List other items.'], ['Omitting dividends.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Control judgements', 2.5, 'concept', 'control'), S('s2', 'Influence judgement', 1.5, 'concept', 'influence')],
          ['Explain each.'], ['Not disclosing Topaz.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the objective of Ind AS 112?', 'To help users evaluate the nature and risks of interests in other entities and their effects on position, performance and cash flows.',
          [P('p1', 'Nature and risks', 5, 'risk'), P('p2', 'Effects on position', 5, 'position|performance')], 'c1'),
        V('v2', 'What is disclosed for material NCI?', 'Name, place of business, NCI share of ownership and votes, profit allocated, accumulated NCI and summarised financial information.',
          [P('p1', 'Profit and accumulated NCI', 5, 'profit|accumulated'), P('p2', 'Summarised information', 5, 'summarised')], 'c2'),
        V('v3', 'What is a structured entity?', 'One designed so that voting or similar rights are not what decides who controls it, with relevant activities directed by contracts.',
          [P('p1', 'Voting rights not decisive', 6, 'voting'), P('p2', 'Contracts', 4, 'contract')], 'c4'),
        V('v4', 'What is disclosed for material joint ventures?', 'Name, relationship, ownership, method, dividends received and summarised financial information with extra detail like cash and depreciation.',
          [P('p1', 'Summarised information', 5, 'summarised'), P('p2', 'Dividends', 5, 'dividend')], 'c3'),
        V('v5', 'What does Schedule III add for groups?', 'A table of each entity\'s share of consolidated net assets and profit as percentages and amounts.',
          [P('p1', 'Each entity', 5, 'each entity'), P('p2', 'Net assets and profit', 5, 'net assets|profit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Granite Group', 'difficulty': 'core',
              'case': 'Granite Ltd. has a 60% subsidiary in a country with currency controls limiting dividends, a 50% joint venture with summarised net assets of ₹400 crore, and has sponsored a securitisation trust (unconsolidated) in which it holds a ₹15 crore subordinated note.',
              'mcqs': [
                  M('k1a', 'The currency controls are disclosed as:', ['Significant restrictions', 'Contingent liabilities', 'Segment information', 'Not disclosed'], 0,
                    'They limit access to group assets. In practice: quantify where possible.', 'core', topic=T2),
                  M('k1b', 'Granite\'s share of the JV\'s net assets (₹ crore):', ['200', '400', '100', '50'], 0,
                    '50% × 400, reconciled to carrying amount. In practice: summarised information.', 'core', check=200, topic=T3),
                  M('k1c', 'Maximum exposure to loss from the trust, with no guarantees given (₹ crore):', ['15', 'Nil', '30', 'Unknown'], 0,
                    'The carrying amount of the note. In practice: add any guarantees or commitments.', 'moderate', check=15, topic=T4),
                  M('k1d', 'The trust is a:', ['Structured entity', 'Joint operation', 'Associate', 'Branch'], 0,
                    'Control is not via votes. In practice: Ind AS 112 risk disclosures.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 8, 'Disclosures',
                ['State the objective and significant judgement disclosures.',
                 'Prepare disclosures about subsidiaries and NCI.',
                 'Prepare disclosures about joint arrangements and associates.',
                 'Disclose unconsolidated structured entities and Schedule III requirements.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['fin-p1-ch13-u07'],
                 'exam_tip': 'Group disclosure answers should cover judgements, NCI, restrictions, and structured entity exposure.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Disclose judgements on control and influence.',
                             'Material NCI: summarised information.',
                             'Restrictions and structured entity risks.',
                             'Material JVs and associates: summary data.',
                             'Schedule III entity-wise table.'],
                 'remember': ['Maximum exposure to loss for structured entities.'],
                 'traps': ['Forgetting judgements where holding is above 50% but no control.']},
                [('Judgements', 'Control, JC, SI'), ('NCI', 'Summary info'), ('Structured', 'Max exposure'), ('Schedule III', 'Entity-wise %')],
                viva, cases)
