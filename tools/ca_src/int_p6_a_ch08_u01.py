"""CA Intermediate · Paper 6A Financial Management · Chapter 8 Dividend Decision.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch08-u01'
T1 = 'Dividend decision, forms of dividend and determinants'
T2 = 'Relevance theories: Walter, Gordon, traditional'
T3 = 'Irrelevance: Modigliani–Miller'
T4 = 'Dividend policy in practice: stability and Lintner'


def build():
    ck = Checks()
    p40 = ck.add('(4+0.15/0.10*(10-4))/0.10', 'Walter price at 40% payout (r = 15%)')
    p100 = ck.add('10/0.10', 'Walter price at 100% payout')
    p40b = ck.add('(4+0.08/0.10*(10-4))/0.10', 'Walter price at 40% payout (r = 8%)')
    i1 = {'id': 'i1', 'title': 'Should a growth firm pay out?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'EPS ₹10; cost of equity 10%. Using Walter\'s model, find the share price at 40% and 100% payout when (a) return on investment r = 15% and (b) r = 8%. What is the optimal payout in each case?',
          'solution': [table(['Case', '40% payout ₹', '100% payout ₹', 'Optimal'], [
              ['(a) r = 15% > Ke', inr(p40), inr(p100), 'Retain all (0% payout)'],
              ['(b) r = 8% < Ke', inr(p40b), inr(p100), 'Distribute all (100% payout)']], title='Walter: P = [D + (r/Ke)(E − D)] ÷ Ke'),
              note('When r = Ke the price is the same at any payout — dividend policy does not matter.')],
          'checks': list(ck)}

    ck2 = Checks()
    p1d = ck2.add('100*1.10-5', 'Price at year end if dividend is paid')
    newsh = ck2.add('(2000000-(1000000-500000))/105', 'New shares to be issued')
    vf = ck2.add('((100000+14285.714)*105 - 2000000 + 1000000)/1.10', 'Value of the firm today')
    i2 = {'id': 'i2', 'title': 'Testing MM', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A firm has 1,00,000 shares at ₹100 each; cost of equity 10%. It expects net income of ₹10 lakh, plans investment of ₹20 lakh and is considering a dividend of ₹5 per share. Under MM, find the year-end price if the dividend is paid, the number of new shares needed, and show the firm\'s value is unchanged.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Year-end price (dividend paid)', '100 × 1.10 − 5', '₹' + inr(p1d)],
              ['Funds needed from new shares', '20,00,000 − (10,00,000 − 5,00,000)', '₹' + inr(1500000)],
              ['New shares', '15,00,000 ÷ 105', str(round(newsh, 2))],
              ['Value of firm today', '[(1,00,000 + 14,285.71) × 105 − 20,00,000 + 10,00,000] ÷ 1.10', '₹' + inr(round(vf))]], title='Modigliani–Miller'),
              p('Without a dividend the year-end price would be ₹110, fewer shares would be issued, and the value is still ₹1,00,00,000 — so dividend policy is irrelevant under MM\'s assumptions.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'The dividend decision splits earnings between distribution and retention; it affects shareholder wealth, financing needs and signalling.',
            'Forms: cash dividend; stock dividend (bonus shares — no cash outflow, more shares); share buy-back as an alternative way of returning cash; interim and final dividends.',
            'Determinants: legal restrictions (dividend out of profits, Companies Act rules), liquidity, growth needs and access to capital, stability of earnings, shareholders\' preference and tax, inflation, and covenants in loan agreements.'],
          'Dividend policy is a trade-off between cash in shareholders\' hands today and growth tomorrow.',
          'A start-up with high-return projects usually retains all earnings.'),
        C('c2', T2, [
            'Walter: P = [D + (r/Ke)(E − D)] ÷ Ke. If r > Ke (growth firm), retention raises price — optimal payout 0%; if r < Ke (declining firm), full payout is optimal; if r = Ke (normal firm), payout does not matter. Assumes all financing from retention, constant r and Ke, infinite life.',
            'Gordon: P = E(1 − b) ÷ (Ke − br), where b is retention ratio and br is growth. Conclusions mirror Walter\'s; with uncertainty, investors value near dividends more ("bird in hand").',
            'Traditional (Graham and Dodd): P = m(D + E/3), giving dividends more weight than retained earnings.'],
          'Relevance theories link the best payout to whether the firm earns more than shareholders require.',
          'Under Gordon, EPS ₹20, b = 0.6, r = 15%, Ke = 12% gives g = 9% and P = ₹8 ÷ 3% = ₹266.67.'),
        C('c3', T3, [
            'Modigliani and Miller argue that, in perfect markets with no taxes, no transaction or flotation costs and fixed investment policy, dividend policy does not affect firm value; value depends on earnings power and investment decisions.',
            'P0 = (D1 + P1) ÷ (1 + Ke); shares issued to finance investment: Δn = [I − (E − nD1)] ÷ P1. Paying a dividend lowers P1 by exactly the dividend, and the new issue offsets the cash paid.',
            'Criticisms: taxes on dividends and gains differ, flotation costs exist, investors face transaction costs, information asymmetry gives dividends a signalling role, and markets are not perfect.'],
          'MM: what you get as dividend you lose in share price, when markets are perfect.',
          'A ₹5 dividend on a share that would be worth ₹110 leaves the share at ₹105 — the holder\'s wealth is unchanged.'),
        C('c4', T4, [
            'Stable dividend policies (constant dividend per share, constant payout ratio, or a small regular dividend plus extra) are popular because investors value predictability and signals.',
            'Lintner\'s model: firms have a target payout ratio and adjust dividends gradually towards it: D1 = D0 + [(EPS × target payout) − D0] × adjustment factor.',
            'Stock dividends and splits do not change wealth directly but improve marketability and may signal confidence.'],
          'Managers smooth dividends because cutting them sends a bad signal.',
          'Target payout 50%, EPS rises from ₹8 to ₹12, previous dividend ₹4, adjustment 0.5: new dividend ₹5.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Board note on dividend', 'role': 'Finance analyst trainee',
             'situation': 'The CFO asks whether to raise the dividend or fund a new plant from profits.',
             'steps': ['Compare expected project return with the cost of equity.', 'Check legal and covenant limits.', 'Assess cash and access to external funds.', 'Consider signalling and shareholder expectations.'],
             'takeaway': 'If retained profits earn more than shareholders\' required return, retention usually adds value.'}]

    mcqs = [
        Q('m1', 'Under Walter\'s model, a growth firm (r > Ke) should:', ['Retain all earnings', 'Pay all earnings as dividend', 'Pay 50%', 'Issue bonus shares only'], 0,
          'Each rupee retained earns more than shareholders require, raising price. In practice: high-growth tech firms pay little dividend.', 'c2', T2),
        Q('m2', 'Walter: E = ₹8, D = ₹8, Ke = 10%. Price:', ['₹80', '₹8', '₹100', '₹64'], 0,
          'With full payout P = 8 ÷ 0.10 = ₹80. In practice: r does not matter at 100% payout.', 'c2', T2, check=80),
        Q('m3', 'In Gordon\'s model, growth g equals:', ['b × r', 'Ke − r', 'D ÷ E', '1 − b'], 0,
          'Growth comes from retained earnings reinvested at r. In practice: requires Ke > g.', 'c2', T2),
        Q('m4', 'Gordon: E = ₹10, b = 0.4, r = 10%, Ke = 12%. Price:', ['₹75', '₹60', '₹83.33', '₹50'], 0,
          'D = 6; g = 4%; P = 6 ÷ (0.12 − 0.04) = ₹75. In practice: sensitive to Ke − g.', 'c2', T2, 'moderate', check=75),
        Q('m5', 'MM dividend irrelevance assumes:', ['Perfect capital markets with no taxes', 'High flotation costs', 'Different tax on dividends and gains', 'Uncertain investment policy'], 0,
          'MM rely on perfect markets, no taxes and fixed investment policy. In practice: real markets violate these.', 'c3', T3),
        Q('m6', 'Under MM, P0 ₹50, Ke 10%, D1 ₹2. P1:', ['₹53', '₹55', '₹50', '₹48'], 0,
          'P1 = 50 × 1.10 − 2 = ₹53. In practice: without dividend P1 = ₹55.', 'c3', T3, check=53),
        Q('m7', 'The traditional model of Graham and Dodd is:', ['P = m(D + E/3)', 'P = D/Ke', 'P = E/Ke', 'P = (D1 + P1)/(1 + Ke)'], 0,
          'It weights dividends three times as heavily as retained earnings. In practice: reflects investor preference for dividends.', 'c2', T2),
        Q('m8', 'Lintner\'s model suggests that firms:', ['Adjust dividends gradually towards a target payout', 'Change dividends every year with earnings', 'Never pay dividends', 'Pay all earnings'], 0,
          'Dividends are smoothed using an adjustment factor. In practice: explains sticky dividends.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Walter formula', 1, 'concept', 'walter'), S('s2', 'Prices at r = 15%', 2, 'computation', '15%', nums=[p40, p100]),
           S('s3', 'Price at r = 8%', 1, 'computation', '8%', nums=[p40b]), S('s4', 'Optimal payout', 1, 'concept', 'retain|distribute')],
          ['State r vs Ke first.'], ['Using r in the denominator.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Year-end price', 2, 'computation', 'price', nums=[p1d]), S('s2', 'New shares', 2, 'computation', 'shares', nums=[newsh]), S('s3', 'Value of firm', 3, 'computation', 'value', nums=[vf])],
          ['Follow the MM equations.'], ['Forgetting to subtract investment.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What does Walter say about a normal firm?', 'When the return on investment equals the cost of equity, the share price is the same at every payout, so dividend policy is irrelevant.',
          [P('p1', 'r equals Ke', 5, 'equal'), P('p2', 'Same price', 5, 'same|irrelevant')], 'c2'),
        V('v2', 'State Gordon\'s formula.', 'Price equals earnings times one minus retention ratio, divided by cost of equity minus retention ratio times return.',
          [P('p1', 'Payout numerator', 5, 'one minus|1 − b|earnings'), P('p2', 'Ke − br', 5, 'cost of equity minus|ke')], 'c2'),
        V('v3', 'What is the MM argument?', 'In perfect markets the value of a firm depends on its earning power and investment policy; the dividend paid is offset by a fall in share price, so payout does not matter.',
          [P('p1', 'Perfect markets', 5, 'perfect'), P('p2', 'Offset', 5, 'offset|fall')], 'c3'),
        V('v4', 'Give two criticisms of MM.', 'Taxes treat dividends and capital gains differently, and flotation and transaction costs exist.',
          [P('p1', 'Taxes', 5, 'tax'), P('p2', 'Costs', 5, 'flotation|transaction')], 'c3'),
        V('v5', 'Why do companies keep dividends stable?', 'Because investors value predictable income and a cut sends a negative signal about future earnings.',
          [P('p1', 'Predictability', 5, 'predict|stable'), P('p2', 'Signal', 5, 'signal')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Aarohi Tech Ltd.', 'difficulty': 'moderate',
              'case': 'Aarohi Tech Ltd.: EPS ₹20; cost of equity 12%; return on investment 18%. The board debates a 30% or 70% payout. Use Walter\'s model.',
              'mcqs': [
                  M('k1a', 'Price at 30% payout:', ['₹225.00', '₹191.67', '₹250.00', '₹166.67'], 0,
                    'D = 6; P = [6 + (0.18 ÷ 0.12) × 14] ÷ 0.12 = 27 ÷ 0.12 = ₹225. In practice: retention adds value here.', 'moderate', check=225, topic=T2),
                  M('k1b', 'Price at 70% payout:', ['₹191.67', '₹225.00', '₹166.67', '₹250.00'], 0,
                    'D = 14; P = [14 + 1.5 × 6] ÷ 0.12 = 23 ÷ 0.12 = ₹191.67. In practice: higher payout lowers price for a growth firm.', 'moderate', check=191.67, topic=T2),
                  M('k1c', 'Optimal payout under Walter:', ['0%', '100%', '50%', 'Any payout'], 0,
                    'Since r (18%) exceeds Ke (12%), retaining everything maximises price (₹250). In practice: consider shareholder cash needs.', 'core', topic=T2),
                  M('k1d', 'Under MM, the choice of payout would:', ['Not affect firm value', 'Raise value at 70%', 'Raise value at 30%', 'Make value zero'], 0,
                    'MM hold dividend policy irrelevant in perfect markets. In practice: taxes and signalling make it relevant.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch08', 1, 'Dividend Decision',
                ['Explain forms and determinants of dividend policy.',
                 'Apply Walter, Gordon and traditional models.',
                 'Apply the MM irrelevance model.',
                 'Explain stable dividend policies and Lintner\'s model.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 45}, 'prereq': ['int-p6-a-ch07-u01'],
                 'exam_tip': 'Compare r with Ke before any calculation — it tells you the answer to "optimal payout".'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Walter: P = [D + (r/Ke)(E − D)] ÷ Ke.',
                             'Gordon: P = E(1 − b) ÷ (Ke − br).',
                             'r > Ke retain; r < Ke distribute; r = Ke irrelevant.',
                             'MM: P0 = (D1 + P1) ÷ (1 + Ke); Δn = [I − (E − nD1)] ÷ P1.',
                             'Lintner: gradual adjustment to target payout.'],
                 'remember': ['Gordon needs Ke > g.'],
                 'traps': ['Bonus shares do not change shareholder wealth by themselves.']},
                [('Walter', '[D + r/Ke(E − D)]/Ke'), ('Gordon', 'E(1 − b)/(Ke − br)'), ('MM P1', 'P0(1 + Ke) − D1'), ('Growth', 'g = br')],
                viva, cases)
