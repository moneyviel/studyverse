"""CA Intermediate · Paper 6B Strategic Management · Chapter 4 Strategic Choices.
Scope follows the ICAI study material; explanations, names and examples are original."""
from ikit import *

UID = 'int-p6-b-ch04-u01'
T1 = 'Broad corporate strategies: stability, growth, retrenchment, combination'
T2 = 'Routes to growth: Ansoff, integration, diversification, M&A and alliances'
T3 = 'Retrenchment: turnaround, divestment and liquidation'
T4 = 'Portfolio analysis: BCG and GE matrices'


def build():
    i1 = {'id': 'i1', 'title': 'Choosing a growth path', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A spices company considers four moves: (a) more advertising to sell its masalas to existing customers; (b) selling its masalas in the Gulf; (c) launching ready-to-eat curries for its current customers; (d) buying a paper mill. Classify each using Ansoff\'s matrix or diversification type.',
          'solution': [table(['Move', 'Strategy', 'Risk'], [
              ['(a)', 'Market penetration — existing product, existing market', 'Lowest'],
              ['(b)', 'Market development — existing product, new market', 'Moderate'],
              ['(c)', 'Product development — new product, existing market', 'Moderate'],
              ['(d)', 'Conglomerate (unrelated) diversification — new product, new market', 'Highest']], title='Ansoff and diversification')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Reading a BCG matrix', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A consumer group has four businesses: (a) detergent — high share in a slow-growing market; (b) plant-based milk — low share in a fast-growing market; (c) premium shampoo — high share in a fast-growing market; (d) carbon paper — low share in a declining market. Classify each in the BCG matrix and suggest a strategy.',
          'solution': [table(['Business', 'BCG cell', 'Suggested strategy'], [
              ['(a) Detergent', 'Cash cow', 'Hold; use cash to fund stars and question marks'],
              ['(b) Plant-based milk', 'Question mark', 'Invest selectively to build share, or exit'],
              ['(c) Premium shampoo', 'Star', 'Invest to sustain growth and share'],
              ['(d) Carbon paper', 'Dog', 'Harvest or divest']], title='BCG growth–share matrix')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Stability: continue with the present business and approach, making incremental improvements — suitable when the environment is stable and the firm is performing satisfactorily.',
            'Growth (expansion): increase scope or scale through new products, markets or functions; it brings higher risk and resource needs.',
            'Retrenchment: reduce scope — cut costs, sell units or exit — when performance is poor. Combination: pursue different strategies for different businesses at the same time (e.g. expanding one, divesting another).'],
          'Corporate strategy chooses whether to stay, grow, shrink or do a mix.',
          'A conglomerate expanding renewables while selling its tyre unit follows a combination strategy.'),
        C('c2', T2, [
            'Ansoff\'s product-market matrix: market penetration (existing product, existing market), market development (existing product, new market), product development (new product, existing market) and diversification (new product, new market).',
            'Integration: vertical — backward (towards suppliers) or forward (towards customers); horizontal — acquiring or merging with competitors. Diversification: related (concentric) — linked by technology, markets or skills; unrelated (conglomerate).',
            'Growth may be organic, through mergers and acquisitions, or through strategic alliances and joint ventures, which share risks and resources but require trust and careful partner choice.'],
          'Growth options differ by how far they move from what the firm already knows.',
          'A carmaker setting up its own battery plant is backward integration.'),
        C('c3', T3, [
            'Turnaround strategy reverses decline through cost cutting, asset sales, new leadership, refocusing on core businesses and restoring cash flow; warning signs include persistent losses, falling market share, high debt and low morale.',
            'Divestment sells or spins off a part of the business that no longer fits or performs, freeing resources for core activities.',
            'Liquidation closes the business and sells its assets — the last resort when nothing else will work; it may be voluntary or compulsory.'],
          'Retrenchment is about surviving to fight another day — or exiting with the least damage.',
          'A telecom company selling its tower assets to cut debt is divesting.'),
        C('c4', T4, [
            'BCG growth–share matrix places businesses by market growth rate and relative market share: stars (high growth, high share), cash cows (low growth, high share), question marks (high growth, low share) and dogs (low growth, low share). Cash from cows funds stars and selected question marks.',
            'The GE (McKinsey) nine-cell matrix uses industry attractiveness and business strength, each rated high, medium or low, suggesting invest/grow, selectivity or harvest/divest.',
            'Other tools include the ADL matrix (industry maturity versus competitive position). Portfolio tools simplify decisions but rely on judgement about measures and ignore synergies.'],
          'Portfolio matrices help a group decide where to put its money.',
          'A star today becomes a cash cow when its market matures.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Portfolio review', 'role': 'Strategy analyst trainee',
             'situation': 'A group CEO wants a one-page view of which businesses to grow or sell.',
             'steps': ['Gather market growth and relative share data.', 'Plot businesses on BCG and GE grids.', 'Assess cash needs and synergies.', 'Recommend invest, hold, harvest or divest.'],
             'takeaway': 'Matrices start the discussion; judgement on synergies finishes it.'}]

    mcqs = [
        Q('m1', 'Selling an existing product in a new geographic market is:', ['Market development', 'Market penetration', 'Product development', 'Diversification'], 0,
          'Ansoff: existing product, new market. In practice: exports are an example.', 'c2', T2),
        Q('m2', 'A dairy acquiring its milk-collection network is:', ['Backward integration', 'Forward integration', 'Horizontal integration', 'Conglomerate diversification'], 0,
          'Moving towards suppliers is backward integration. In practice: secures inputs.', 'c2', T2),
        Q('m3', 'A business with high market share in a low-growth market is a:', ['Cash cow', 'Star', 'Question mark', 'Dog'], 0,
          'It generates more cash than it needs. In practice: fund other units from it.', 'c4', T4),
        Q('m4', 'The GE matrix uses:', ['Industry attractiveness and business strength', 'Market growth and relative share', 'Product and market newness', 'Cost and differentiation'], 0,
          'GE uses multi-factor measures on a 3×3 grid. In practice: more nuanced than BCG.', 'c4', T4),
        Q('m5', 'Selling a non-core business unit is:', ['Divestment', 'Liquidation', 'Stability', 'Market penetration'], 0,
          'Divestment exits part of the business. In practice: frees capital.', 'c3', T3),
        Q('m6', 'A strategy to reverse persistent losses through restructuring is:', ['Turnaround', 'Stability', 'Diversification', 'Market development'], 0,
          'Turnaround aims to restore profitability. In practice: often needs new leadership.', 'c3', T3),
        Q('m7', 'Pursuing growth in one business and retrenchment in another simultaneously is:', ['Combination strategy', 'Stability strategy', 'Liquidation', 'Horizontal integration'], 0,
          'Different strategies for different units form a combination. In practice: common in conglomerates.', 'c1', T1),
        Q('m8', 'A strategic alliance:', ['Lets firms share resources while remaining independent', 'Merges two firms into one', 'Is always permanent', 'Requires 100% acquisition'], 0,
          'Alliances are cooperative arrangements without full merger. In practice: joint ventures are one form.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Penetration', 1, 'concept', 'penetration'), S('s2', 'Market development', 1, 'concept', 'market development'),
           S('s3', 'Product development', 1, 'concept', 'product development'), S('s4', 'Diversification', 1, 'concept', 'conglomerate|diversification')],
          ['Name the Ansoff cell.'], ['Calling (d) related diversification.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Cash cow', 1, 'concept', 'cash cow'), S('s2', 'Question mark', 1, 'concept', 'question mark'), S('s3', 'Star', 1, 'concept', 'star'), S('s4', 'Dog', 1, 'concept', 'dog')],
          ['Add a strategy for each.'], ['Mixing up star and question mark.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is a stability strategy?', 'Continuing in the same business and markets with incremental improvements, suitable when performance is satisfactory and the environment steady.',
          [P('p1', 'Same business', 5, 'same|continu'), P('p2', 'Incremental', 5, 'incremental')], 'c1'),
        V('v2', 'Distinguish related and unrelated diversification.', 'Related diversification enters businesses linked by technology, markets or skills; unrelated diversification enters businesses with no such link.',
          [P('p1', 'Related links', 5, 'linked|technology|skills'), P('p2', 'Unrelated', 5, 'unrelated|no such')], 'c2'),
        V('v3', 'When is liquidation chosen?', 'As a last resort when the business cannot be turned around or sold profitably, so assets are sold and the business closed.',
          [P('p1', 'Last resort', 5, 'last resort'), P('p2', 'Assets sold', 5, 'assets|close')], 'c3'),
        V('v4', 'What are the BCG matrix axes?', 'Market growth rate on one axis and relative market share on the other.',
          [P('p1', 'Market growth', 5, 'growth'), P('p2', 'Relative share', 5, 'share')], 'c4'),
        V('v5', 'Give two advantages of strategic alliances.', 'They let partners share costs and risks and gain access to new markets, technologies or skills.',
          [P('p1', 'Share risk', 5, 'risk|cost'), P('p2', 'Access', 5, 'access|market|technolog')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Horizon Industries', 'difficulty': 'moderate',
              'case': 'Horizon Industries owns a cement business (market leader, slow growth), a solar panel unit (small share, fast-growing market) and a loss-making textile mill. It plans to buy a rival cement firm, invest in solar, and sell the mill.',
              'mcqs': [
                  M('k1a', 'Buying a rival cement firm is:', ['Horizontal integration', 'Backward integration', 'Conglomerate diversification', 'Liquidation'], 0,
                    'Acquiring a competitor at the same stage is horizontal. In practice: check competition law.', 'core', topic=T2),
                  M('k1b', 'The solar unit is a BCG:', ['Question mark', 'Star', 'Cash cow', 'Dog'], 0,
                    'Low share in a high-growth market. In practice: invest selectively to build share.', 'core', topic=T4),
                  M('k1c', 'Selling the textile mill is:', ['Divestment', 'Turnaround', 'Stability', 'Market development'], 0,
                    'Exiting a business unit is divestment. In practice: frees cash for solar.', 'core', topic=T3),
                  M('k1d', 'The overall plan is a:', ['Combination strategy', 'Pure stability strategy', 'Pure retrenchment', 'Liquidation'], 0,
                    'Growth in some units and exit from another together form a combination. In practice: aligned with a portfolio view.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p6', 'int-p6-b-ch04', 1, 'Strategic Choices',
                ['Distinguish stability, growth, retrenchment and combination strategies.',
                 'Apply Ansoff\'s matrix and classify integration and diversification.',
                 'Explain turnaround, divestment and liquidation.',
                 'Use BCG and GE portfolio matrices.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p6-b-ch03-u01'],
                 'exam_tip': 'Name the exact strategy (e.g. "backward vertical integration") — vague labels lose marks.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Stability, growth, retrenchment, combination.',
                             'Ansoff: penetration, market development, product development, diversification.',
                             'Integration: backward, forward, horizontal; related vs conglomerate diversification.',
                             'Retrenchment: turnaround, divestment, liquidation.',
                             'BCG: stars, cash cows, question marks, dogs; GE nine-cell.'],
                 'remember': ['Cash cows fund stars and question marks.'],
                 'traps': ['Horizontal integration is with competitors, not suppliers.']},
                [('Ansoff', 'Product × market'), ('BCG', 'Growth × share'), ('GE', 'Attractiveness × strength')],
                viva, cases)
