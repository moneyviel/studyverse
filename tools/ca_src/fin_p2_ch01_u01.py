"""CA Final · Paper 2 Advanced Financial Management · Chapter 1 Financial Policy and Corporate Strategy.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch01-u01'
T1 = 'The strategic role of the CFO'
T2 = 'Strategy levels and financial planning'
T3 = 'Linking financial policy and corporate strategy'
T4 = 'Sustainable growth and external funding needs'


def build():
    ck = Checks()
    roe = ck.add('30/150*100', 'Return on equity (%)')
    sgr = ck.add('30/150*(1-12/30)*100', 'Sustainable growth rate (%)')
    i1 = {'id': 'i1', 'title': 'How fast can we grow without new equity?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Nimbus Ltd. earns profit after tax of ₹30 crore on equity of ₹150 crore and pays dividends of ₹12 crore. It wants to keep its debt-equity ratio and payout ratio unchanged and issue no new shares. Compute its sustainable growth rate. Sales are expected to grow 15% next year — what does that imply?',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Return on equity', '30 ÷ 150', inr(roe) + '%'],
              ['Retention ratio', '1 − 12/30', '60%'],
              ['Sustainable growth rate', '20% × 60%', inr(sgr) + '%'],
              ['Planned growth 15%', 'Exceeds 12%', 'Needs more debt, new equity, lower payout or better margins/turnover']], title='SGR = ROE × retention')],
          'checks': list(ck)}

    ck2 = Checks()
    a = ck2.add('800/1000*200', 'Extra assets needed (₹ crore)')
    l = ck2.add('200/1000*200', 'Spontaneous liabilities generated (₹ crore)')
    r = ck2.add('0.1*1200*0.6', 'Retained earnings next year (₹ crore)')
    efr = ck2.add('800/1000*200-200/1000*200-0.1*1200*0.6', 'External funding requirement (₹ crore)')
    i2 = {'id': 'i2', 'title': 'External funding requirement', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Sales of Orchid Ltd. are ₹1,000 crore and will rise to ₹1,200 crore. Assets of ₹800 crore and spontaneous liabilities (creditors, accruals) of ₹200 crore move in line with sales. Net margin is 10% and 60% of profit is retained. Compute the external funding requirement.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Increase in assets', '(800/1,000) × 200', inr(a)],
              ['Less increase in spontaneous liabilities', '(200/1,000) × 200', inr(l)],
              ['Less retained earnings', '10% × 1,200 × 60%', inr(r)],
              ['External funding requirement', '160 − 40 − 72', inr(efr)]], title='EFR = (A/S)ΔS − (L/S)ΔS − m·S₁·b')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'The modern CFO is a strategic partner, not just a record keeper: involved in capital allocation, risk management, investor relations, funding strategy, mergers and restructuring, technology and data in finance, and governance and compliance.',
            'The CFO links business plans to their financial consequences — testing whether strategies create value, whether they can be funded, and how they affect risk and returns.',
            'Strategic financial management means managing finance with long-term goals in mind: deciding investments, financing and dividend policy so as to maximise shareholder wealth while handling uncertainty.'],
          'The CFO turns strategy into numbers and numbers into strategy.',
          'A CFO tests whether an expansion plan earns more than its cost of capital before funding it.'),
        C('c2', T2, [
            'Strategy works at three levels: corporate (which businesses to be in and how to allocate resources across them), business unit (how to compete in a given market — cost leadership, differentiation, focus) and functional (how finance, marketing, operations and HR support the business strategy).',
            'Financial planning translates strategy into money terms: forecasting sales, assets, funds needed and sources, with targets for profitability, liquidity and solvency.',
            'Good financial plans set clear objectives, consider alternative scenarios, stay flexible, and are reviewed regularly against actual results.'],
          'Corporate picks the field, business unit picks the game plan, functions carry it out.',
          'Finance at the functional level arranges working capital for a new product launch.'),
        C('c3', T3, [
            'Financial policy covers the investment, financing and dividend decisions, plus policies on liquidity, risk and capital structure. These must fit the corporate strategy: an aggressive growth strategy needs funding and risk policies that support it.',
            'Strategy often depends on finance: limited funds can force a firm to grow slower, sell non-core assets, form alliances or raise outside capital. Conversely, financial policy should be shaped by strategic priorities, not the other way round.',
            'Key interface areas include the sources and cost of finance, investment selection, dividend and retention policy, and managing financial risks so that strategic plans are not derailed.'],
          'Strategy and finance must agree — or the plan fails on paper or on the ground.',
          'A firm planning acquisitions keeps borrowing capacity in reserve.'),
        C('c4', T4, [
            'The sustainable growth rate (SGR) is the fastest sales growth a firm can achieve without issuing new equity, while keeping its capital structure and payout ratio constant: SGR = ROE × retention ratio (1 − payout). ROE itself depends on profit margin, asset turnover and leverage.',
            'If planned growth exceeds the SGR, the firm must raise equity, increase leverage, cut dividends, or improve margins and asset efficiency — or slow growth. If actual growth is below SGR, surplus cash can be returned to shareholders, used to reduce debt or deployed in acquisitions. Inflation raises funding needs and so lowers effective sustainable growth.',
            'External funding requirement (EFR) = increase in assets needed − increase in spontaneous liabilities − retained earnings, assuming assets and spontaneous liabilities move with sales. A negative EFR indicates surplus funds.'],
          'SGR tells you how fast you can grow on your own; EFR tells you how much money you will need.',
          'At 20% ROE and 60% retention, a firm can grow 12% a year without new shares.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Funding a five-year plan', 'role': 'Assistant to the CFO',
             'situation': 'The board wants 18% annual sales growth; current SGR is 11%.',
             'steps': ['Compute SGR and its drivers.', 'Estimate EFR year by year.', 'Model options: more debt, rights issue, lower payout, margin improvement.', 'Recommend a mix consistent with the risk appetite.'],
             'takeaway': 'Growth ambitions must be matched by a funding plan.'}]

    mcqs = [
        Q('m1', 'Sustainable growth rate equals:', ['ROE × retention ratio', 'ROA × payout ratio', 'Net margin × payout', 'Debt ÷ equity'], 0,
          'Growth funded by retained earnings at constant leverage. In practice: link to DuPont analysis.', 'c4', T4),
        Q('m2', 'If planned growth exceeds the SGR, the firm can:', ['Raise equity, raise leverage, cut payout or improve efficiency', 'Do nothing', 'Only cut prices', 'Only reduce sales'], 0,
          'Something must give. In practice: model each option.', 'c4', T4),
        Q('m3', 'Deciding which industries a group should operate in is:', ['Corporate-level strategy', 'Business-unit strategy', 'Functional strategy', 'Operational planning'], 0,
          'Portfolio choices are corporate. In practice: capital allocation follows.', 'c2', T2),
        Q('m4', 'Spontaneous liabilities include:', ['Trade creditors and accrued expenses', 'Term loans', 'Debentures', 'Equity'], 0,
          'They rise automatically with sales. In practice: reduce EFR.', 'c4', T4),
        Q('m5', 'The three main financial decisions are:', ['Investment, financing and dividend', 'Pricing, marketing and HR', 'Audit, tax and law', 'Production, sales and HR'], 0,
          'Core of financial policy. In practice: interlinked.', 'c3', T3),
        Q('m6', 'A negative EFR means:', ['Surplus funds available', 'More borrowing needed', 'Loss', 'Lower sales'], 0,
          'Internal funds exceed needs. In practice: return cash or invest.', 'c4', T4),
        Q('m7', 'The strategic CFO role mainly involves:', ['Linking strategy to value creation and funding', 'Only bookkeeping', 'Only tax filing', 'Only payroll'], 0,
          'Partner to the CEO. In practice: capital allocation.', 'c1', T1),
        Q('m8', 'Inflation generally causes the external funding requirement to:', ['Increase', 'Decrease', 'Stay unchanged', 'Become negative'], 0,
          'Nominal assets rise. In practice: lowers sustainable growth.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'ROE', 1, 'computation', 'roe|return on equity', nums=[roe]), S('s2', 'SGR', 2, 'computation', 'sustainable', nums=[sgr]), S('s3', 'Implication', 1, 'concept', 'exceed|debt|equity')],
          ['State assumptions.'], ['Using payout instead of retention.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Assets', 1.5, 'computation', 'assets', nums=[a]), S('s2', 'Liabilities', 1.5, 'computation', 'spontaneous', nums=[l]), S('s3', 'Retention', 1.5, 'computation', 'retained', nums=[r]), S('s4', 'EFR', 1.5, 'computation', 'external', nums=[efr])],
          ['Use next year sales for retention.'], ['Using current sales for retained earnings.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Define the sustainable growth rate.', 'The highest sales growth a firm can fund using retained earnings alone, with no fresh share issue, keeping its leverage and payout ratio constant; it equals ROE times the retention ratio.',
          [P('p1', 'Retained earnings only', 5, 'retained earnings'), P('p2', 'ROE times retention', 5, 'retention')], 'c4'),
        V('v2', 'State the EFR formula.', 'Increase in assets needed minus increase in spontaneous liabilities minus retained earnings of the year.',
          [P('p1', 'Assets less spontaneous liabilities', 5, 'spontaneous'), P('p2', 'Less retained earnings', 5, 'retained')], 'c4'),
        V('v3', 'What are the three levels of strategy?', 'Corporate, business unit and functional level strategy.',
          [P('p1', 'Corporate and business unit', 5, 'corporate|business unit'), P('p2', 'Functional', 5, 'functional')], 'c2'),
        V('v4', 'How should financial policy relate to corporate strategy?', 'It should support and fit the strategy, while finance constraints also shape what strategies are feasible.',
          [P('p1', 'Support strategy', 5, 'support|fit'), P('p2', 'Constraints', 5, 'constraint|feasib')], 'c3'),
        V('v5', 'What can a firm do when growth is below its SGR?', 'Return surplus cash through dividends or buybacks, repay debt, or invest in acquisitions.',
          [P('p1', 'Return cash', 5, 'dividend|buyback'), P('p2', 'Debt or acquisitions', 5, 'debt|acquisition')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Saral Foods Ltd.', 'difficulty': 'moderate',
              'case': 'Saral Foods Ltd. has net margin 8%, asset turnover 1.5 and assets-to-equity 2. It pays out 50% of profits. Management targets 15% sales growth and refuses to issue new shares or raise its leverage.',
              'mcqs': [
                  M('k1a', 'ROE of Saral (%):', ['24', '12', '16', '8'], 0,
                    '8% × 1.5 × 2 = 24%. In practice: DuPont identity.', 'core', check=24, topic=T4),
                  M('k1b', 'Sustainable growth rate (%):', ['12', '24', '6', '15'], 0,
                    '24% × 50% = 12%. In practice: below the 15% target.', 'core', check=12, topic=T4),
                  M('k1c', 'Payout ratio needed to reach 15% SGR at the same ROE (%):', ['37.5', '50', '62.5', '25'], 0,
                    'Retention = 15/24 = 62.5%, so payout 37.5%. In practice: dividend policy as a growth lever.', 'moderate', check=37.5, topic=T4),
                  M('k1d', 'Which change does not raise SGR?', ['Increasing the dividend payout', 'Raising net margin', 'Improving asset turnover', 'Higher retention'], 0,
                    'Higher payout reduces retention. In practice: trade-off with investors.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch01', 1, 'Financial Policy and Corporate Strategy',
                ['Describe the strategic role of the CFO.',
                 'Relate strategy levels to financial planning.',
                 'Explain the interface of financial policy and strategy.',
                 'Compute sustainable growth and external funding requirements.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': [],
                 'exam_tip': 'For growth questions, compute SGR first, then EFR, then suggest the levers.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['CFO: strategic partner in value creation.',
                             'Strategy: corporate, business unit, functional.',
                             'Financial policy must fit strategy.',
                             'SGR = ROE × retention.',
                             'EFR = ΔA − ΔL(spontaneous) − retained earnings.'],
                 'remember': ['ROE = margin × turnover × leverage.'],
                 'traps': ['Using current-year sales for next year\'s retained earnings.']},
                [('SGR', 'ROE × b'), ('EFR', 'ΔA − ΔL − RE'), ('ROE', 'Margin × turnover × equity multiplier'), ('Growth > SGR', 'Need funding or efficiency')],
                viva, cases)
