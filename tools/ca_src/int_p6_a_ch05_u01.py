"""CA Intermediate · Paper 6A Financial Management · Chapter 5 Financing Decisions – Capital Structure.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch05-u01'
T1 = 'Meaning and goals of capital structure'
T2 = 'Net Income and Traditional approaches'
T3 = 'Net Operating Income approach'
T4 = 'Modigliani–Miller approach (without and with tax)'
T5 = 'Trade-off and pecking order theories'
T6 = 'Factors and optimal capital structure'
T7 = 'EBIT–EPS–MPS analysis, financial break-even and indifference point'
T8 = 'Over- and under-capitalisation'


def build():
    # i1 — NI vs NOI on the same firm
    ck = Checks()
    eq_ni = ck.add('round((600000-200000)/0.15)', 'NI: market value of equity = NI ÷ Ke')
    v_ni = ck.add('2666667+2000000', 'NI: value of firm = E + D')
    ko_ni = ck.add('round(600000/4666667*100,2)', 'NI: overall cost Ko = EBIT ÷ V, %')
    v_noi = ck.add('600000/0.12', 'NOI: V = EBIT ÷ Ko')
    eq_noi = ck.add('5000000-2000000', 'NOI: E = V – D')
    ke_noi = ck.add('round((600000-200000)/3000000*100,2)', 'NOI: implied Ke, %')
    i1 = {'id': 'i1', 'title': 'One firm, two theories', 'difficulty': 'core', 'minutes': 10,
          'q': 'Meghna Tools Ltd. has EBIT of ₹6,00,000 and ₹20,00,000 of 10% debt; ignore tax. (a) Under the Net Income approach with Ke = 15%, find the value of equity, the value of the firm and Ko. (b) Under the NOI approach with Ko = 12%, find the value of the firm, the value of equity and the implied Ke.',
          'solution': [table(['Item', 'NI approach', 'NOI approach'], [
              ['EBIT', inr(600000), inr(600000)],
              ['Interest (10% of 20,00,000)', inr(200000), inr(200000)],
              ['Equity value', f'4,00,000 ÷ 0.15 = {inr(eq_ni)}', f'V – D = {inr(eq_noi)}'],
              ['Firm value', inr(v_ni), f'6,00,000 ÷ 0.12 = {inr(v_noi)}'],
              ['Overall cost Ko', f'{ko_ni}%', '12% (given, constant)'],
              ['Cost of equity Ke', '15% (given, constant)', f'{ke_noi}%']], title='NI versus NOI'),
              note('Under NI, adding cheap debt raises value and lowers Ko. Under NOI, Ko and value stay fixed and Ke rises to absorb the extra risk.')],
          'checks': list(ck)}

    # i2 — MM with corporate tax
    ck2 = Checks()
    vu = ck2.add('1000000*(1-0.25)/0.15', 'Value of unlevered firm = EBIT(1 – t) ÷ Ke(u)')
    shield = ck2.add('0.25*2000000', 'PV of tax shield on perpetual debt = t × D')
    vl = ck2.add('5000000+500000', 'Value of levered firm = Vu + tD')
    el = ck2.add('5500000-2000000', 'Equity of levered firm = VL – D')
    i2 = {'id': 'i2', 'title': 'MM with tax: the value of the tax shield', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Two firms, Uday Ltd. (no debt) and Lata Ltd. (₹20,00,000 of perpetual 9% debt), are identical except for financing. Each earns EBIT of ₹10,00,000; tax 25%; the cost of equity of the unlevered firm is 15%. Using MM with corporate tax, find the value of each firm and of Lata Ltd.\'s equity.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Value of Uday Ltd. (Vu)', '10,00,000 × 0.75 ÷ 0.15', inr(vu)],
              ['Tax shield (t × D)', '0.25 × 20,00,000', inr(shield)],
              ['Value of Lata Ltd. (VL)', 'Vu + tD', inr(vl)],
              ['Equity of Lata Ltd.', 'VL – D', inr(el)]], title='MM with tax'),
              note('Without tax, MM says both firms would be worth the same. With tax, debt adds value equal to the present value of the tax saved on interest.')],
          'checks': list(ck2)}

    # i3 — EBIT–EPS indifference and financial break-even
    ck3 = Checks()
    ind = ck3.add('(360000*450000)/(450000-300000)', 'Indifference EBIT: EBIT/4,50,000 = (EBIT – 3,60,000)/3,00,000')
    eps_ind = ck3.add('round(1080000*0.75/450000,2)', 'EPS at indifference point')
    fbep = ck3.add('3000000*0.12', 'Financial break-even of debt plan = interest')
    eps_a = ck3.add('round(1500000*0.75/450000,2)', 'EPS at EBIT ₹15 lakh — equity plan')
    eps_b = ck3.add('round((1500000-360000)*0.75/300000,2)', 'EPS at EBIT ₹15 lakh — debt plan')
    i3 = {'id': 'i3', 'title': 'Equity or debt? The indifference point', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Sabari Mills Ltd. has 3,00,000 equity shares and no debt. It needs ₹30,00,000: Plan A — issue 1,50,000 shares at ₹20; Plan B — 12% debentures. Tax 25%. Find (a) the EBIT at which EPS is equal under both plans, (b) the financial break-even of Plan B, and (c) EPS under each plan if EBIT is ₹15,00,000.',
          'solution': [p('Set EPS equal: EBIT(1 – 0.25) ÷ 4,50,000 = (EBIT – 3,60,000)(1 – 0.25) ÷ 3,00,000. The tax factor cancels: 3,00,000 × EBIT = 4,50,000 × (EBIT – 3,60,000), so 1,50,000 × EBIT = 4,50,000 × 3,60,000.'),
                       table(['Result', '₹'], [
                           ['Indifference EBIT', inr(ind)],
                           ['EPS at that EBIT (both plans)', R(eps_ind)],
                           ['Financial break-even, Plan B (EBIT that just covers interest)', inr(fbep)],
                           ['EPS at EBIT ₹15,00,000 — Plan A', R(eps_a)],
                           ['EPS at EBIT ₹15,00,000 — Plan B', R(eps_b)]], title='Results'),
                       note('Above the indifference EBIT the debt plan gives higher EPS; below it, equity is better. Plan A\'s financial break-even is nil because it has no fixed financial charge.')],
          'checks': list(ck3)}

    th = table(['Approach', 'Does capital structure affect value?', 'What happens as debt rises'], [
        ['Net Income (NI)', 'Yes', 'Kd and Ke constant → Ko falls, value rises; 100% debt is best'],
        ['Traditional', 'Yes, up to a point', 'Ko falls, then rises; an optimum exists'],
        ['Net Operating Income (NOI)', 'No', 'Ko constant; Ke rises linearly with D/E'],
        ['MM without tax', 'No', 'Arbitrage keeps VL = Vu'],
        ['MM with tax', 'Yes', 'VL = Vu + tD; debt adds the tax-shield value'],
        ['Trade-off', 'Yes', 'Tax benefit balanced against bankruptcy and agency costs'],
        ['Pecking order', 'Preference, not optimum', 'Internal funds → debt → equity, last']],
        title='Capital structure theories at a glance')

    concepts = [
        C('c1', T1, [
            'Capital structure is the mix of long-term sources — equity, preference capital and long-term debt — used to finance the business.',
            'A finance manager balances three aims: keep control with existing shareholders, keep financial risk within tolerable limits, and keep the overall cost of capital low. The guiding objective is to maximise the value of the firm.',
            'Value of firm V = EBIT ÷ Ko, where Ko = Kd × D/(D + S) + Ke × S/(D + S). Lowering Ko raises value.'],
          'Choosing a capital structure is like choosing how much of a house to finance with a loan — cheaper money, but more risk.',
          'A promoter who wants to keep 51% may prefer debt to a new share issue.'),
        C('c2', T2, [
            'Net Income approach (Durand): Kd and Ke stay constant whatever the leverage. Because debt is cheaper, adding debt lowers Ko and raises value; the optimum is maximum debt.',
            'Equity value = net income for equity ÷ Ke; firm value = E + D; Ko = EBIT ÷ V.',
            'Traditional approach: debt is cheap at first, so Ko falls; beyond a point, both lenders and shareholders demand more, Ko rises. The lowest point of Ko (highest value) is the optimal structure.'],
          'NI assumes investors never notice extra risk; the traditional view says they notice only after a point.',
          'A firm moving from no debt to moderate debt may see its WACC fall before it starts climbing.'),
        C('c3', T3, [
            'NOI approach: the market values the firm as a whole by capitalising EBIT at a constant Ko. Value is unaffected by the debt–equity mix.',
            'Equity value = V – D, and Ke = (EBIT – interest) ÷ E. As cheap debt is added, Ke rises exactly enough to keep Ko constant.',
            'So capital structure is irrelevant; there is no optimum.'],
          'Slicing a pizza differently does not change the size of the pizza.',
          'Doubling debt in an NOI world leaves value unchanged but pushes shareholders\' required return up.',
          blocks=[th]),
        C('c4', T4, [
            'MM without tax: in perfect markets (no tax, no transaction costs, rational investors who can borrow on the same terms as firms), two firms identical except for leverage must have the same value. Investors use arbitrage — selling the overvalued firm\'s shares and recreating the same leverage personally — until values equalise (home-made leverage).',
            'Ke of a levered firm rises with leverage: Ke = Ko + (Ko – Kd) × D/E.',
            'MM with corporate tax: interest saves tax, so VL = Vu + tD for perpetual debt; value rises with debt. Taken literally, this points to near-100% debt — which other costs prevent.'],
          'Arbitrage is buying the same income stream more cheaply elsewhere until the price gap closes.',
          'At 25% tax, ₹20 lakh of perpetual debt adds ₹5 lakh to firm value.'),
        C('c5', T5, [
            'Trade-off theory: firms add debt until the marginal tax benefit equals the marginal expected cost of financial distress (bankruptcy costs) and agency costs. The optimum lies between no debt and all debt.',
            'Pecking order theory: because managers know more than outsiders, firms prefer internal funds first, then debt, and issue equity only as a last resort. An equity issue may be read as a sign that shares are overvalued.'],
          'Trade-off: borrow while it pays; pecking order: use your own pocket first, then a loan, and sell a share of the shop last.',
          'Profitable firms with ample cash often carry little debt — consistent with pecking order.'),
        C('c6', T6, [
            'Choosing sources: owners\' funds carry no fixed charge but cost more and dilute control; debt is cheaper and keeps control but adds fixed charges and covenants.',
            'Factors: financial leverage and its effect on EPS; growth and stability of sales; cost of capital; risk; cash-flow ability to service debt; nature and size of the firm; control; flexibility; requirements of investors; capital market conditions; asset structure; purpose of finance; period of finance; costs of floatation; personal considerations; corporate tax rate; and legal requirements.',
            'Optimal capital structure is the mix that minimises Ko and maximises value; in practice firms aim for an appropriate range that keeps flexibility, conservatism (debt-servicing capacity) and control.'],
          'There is no single right mix — only the one that suits this firm\'s cash flows, risk and owners.',
          'A utility with steady cash flows can carry far more debt than a start-up software firm.'),
        C('c7', T7, [
            'EBIT–EPS analysis compares financing plans by the EPS each gives at different EBIT levels. EPS = (EBIT – I)(1 – t) – PD, divided by number of equity shares.',
            'Indifference point: the EBIT at which two plans give the same EPS. Above it, the plan with more fixed charges gives higher EPS; below it, the plan with fewer fixed charges is better.',
            'Financial break-even: the EBIT at which EPS is zero = interest + preference dividend ÷ (1 – t).',
            'EPS ignores risk; the market price (MPS = EPS × P/E) shows whether the higher EPS from debt is offset by a lower P/E as risk rises.'],
          'The indifference point is where the debt plan stops hurting and starts helping shareholders.',
          'With expected EBIT well above the indifference point and stable sales, debt usually wins on EPS.'),
        C('c8', T8, [
            'Over-capitalisation: capital exceeds what the business can use profitably, so earnings cannot support fair dividends and interest. Causes include raising more than needed, borrowing at rates above what assets earn, paying too much for goodwill or fictitious assets, under-providing depreciation and overestimating earnings. Results: lower dividends, falling share price, window-dressing, possible reorganisation.',
            'Remedies: reduce debt or interest, buy back shares, reduce face value or number of shares, improve earnings.',
            'Under-capitalisation: capital is too low for the earning capacity, often due to under-estimated earnings or large unrecorded asset appreciation. Results: high dividend rates and share prices; it invites competition, wage demands, regulation and possible share-price manipulation. Remedies: issue bonus shares, split shares, raise the face value or capitalise reserves.'],
          'Over-capitalised: too much capital chasing too little profit; under-capitalised: too little capital for big profits.',
          'A firm that paid a huge premium for a brand that later lost value can find itself over-capitalised.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Advising on a ₹50 crore expansion', 'role': 'Finance analyst',
         'situation': 'The board wants a recommendation: equity, debt or a mix.',
         'steps': ['Forecast EBIT range and volatility.', 'Compute EPS and MPS for each plan; find indifference points.', 'Check interest cover and covenants under a downside case.', 'Weigh control, flexibility and market conditions; recommend.'],
         'takeaway': 'Back the EPS case with a downside test; EPS alone hides risk.'},
        {'id': 'j2', 'title': 'Spotting over-capitalisation', 'role': 'Audit senior',
         'situation': 'A client\'s ROCE has fallen below its cost of debt for three years.',
         'steps': ['Compare return on capital with cost of funds.', 'Look for idle assets, excessive goodwill and weak depreciation policy.', 'Discuss remedies: repay debt, buy back shares, reorganise.'],
         'takeaway': 'Returns below the cost of funds for years point to over-capitalisation.'},
    ]

    mcqs = [
        Q('m1', 'Under the Net Income approach, increasing debt in the capital structure:', ['Lowers Ko and raises firm value', 'Leaves value unchanged', 'Raises Ko', 'Has no effect on Ke'], 0,
          'NI assumes Kd and Ke stay constant regardless of leverage. Since debt is cheaper than equity, more debt lowers the weighted cost Ko and raises value; the optimum is the highest possible debt. NOI and MM-without-tax reach the opposite conclusion. In practice: NI ignores rising risk.', 'c2', T2),
        Q('m2', 'Under the NOI approach, which remains constant as leverage rises?', ['Overall cost of capital (Ko)', 'Cost of equity (Ke)', 'Value of equity', 'Earnings per share'], 0,
          'NOI capitalises EBIT at a constant Ko, so firm value is fixed; Ke rises to offset the use of cheaper debt. Equity value falls as debt replaces it. In practice: NOI says capital structure is irrelevant.', 'c3', T3),
        Q('m3', 'EBIT ₹4,00,000; debt ₹10,00,000 at 10%; Ko 10% (NOI, no tax). Ke is:', ['10%', '12%', '15%', '13.33%'], 0,
          'V = 4,00,000 ÷ 0.10 = ₹40,00,000; E = 40,00,000 – 10,00,000 = ₹30,00,000. Ke = (4,00,000 – 1,00,000) ÷ 30,00,000 = 10%. Because Kd equals Ko here, leverage does not raise Ke — a special case. In practice: Ke = Ko + (Ko – Kd)D/E.', 'c3', T3, 'hard', check=10),
        Q('m4', 'MM\'s proposition without tax rests on the process of:', ['Arbitrage', 'Hedging', 'Speculation', 'Underwriting'], 0,
          'If two identical firms differ in value only because of leverage, investors sell the dearer shares and buy the cheaper, using personal borrowing to copy the leverage; this arbitrage equalises values. Hedging and speculation are different activities. In practice: it assumes personal and corporate borrowing are on equal terms.', 'c4', T4),
        Q('m5', 'Unlevered value ₹80 lakh; perpetual debt ₹30 lakh; tax 30%. Under MM with tax, value of the levered firm is:', ['₹89 lakh', '₹80 lakh', '₹110 lakh', '₹71 lakh'], 0,
          'VL = Vu + tD = 80 + 0.30 × 30 = 80 + 9 = ₹89 lakh. The extra ₹9 lakh is the present value of the tax saved on perpetual interest. Without tax the value would stay at ₹80 lakh. In practice: distress costs limit this gain.', 'c4', T4, 'moderate', check=89),
        Q('m6', 'According to the pecking order theory, firms prefer financing in the order:', ['Internal funds, debt, equity', 'Equity, debt, internal funds', 'Debt, equity, internal funds', 'Equity, internal funds, debt'], 0,
          'Information asymmetry makes outside equity the costliest and the most negative signal, so managers use retained earnings first, then debt, and issue shares last. The trade-off theory instead balances tax benefits against distress costs. In practice: profitable firms often borrow little.', 'c5', T5),
        Q('m7', 'The trade-off theory says the optimal debt level is where:', ['Marginal tax benefit of debt equals marginal cost of financial distress', 'Debt is 100%', 'Debt is zero', 'EPS is maximum'], 0,
          'Debt saves tax but raises the expected cost of bankruptcy and agency problems; the optimum balances the two at the margin. Neither extreme is optimal. In practice: firms with volatile earnings choose lower debt.', 'c5', T5),
        Q('m8', 'Two plans: 2,00,000 shares and no debt, or 1,00,000 shares with interest ₹2,00,000. The indifference EBIT is:', ['₹4,00,000', '₹2,00,000', '₹3,00,000', '₹6,00,000'], 0,
          'EBIT ÷ 2,00,000 = (EBIT – 2,00,000) ÷ 1,00,000, so EBIT = 2 × (EBIT – 2,00,000), giving EBIT = ₹4,00,000. Tax cancels from both sides. In practice: above this EBIT the debt plan gives higher EPS.', 'c7', T7, 'hard', check=400000),
        Q('m9', 'Financial break-even point is the EBIT at which:', ['EPS is zero', 'EPS is maximum', 'Sales cover variable costs', 'Interest is zero'], 0,
          'It is the EBIT just sufficient to pay interest and the pre-tax equivalent of preference dividend, leaving nothing for equity. It is a measure of financial, not operating, break-even. In practice: higher fixed charges raise it.', 'c7', T7),
        Q('m10', 'Interest ₹1,20,000, preference dividend ₹60,000, tax 25%. Financial break-even EBIT is:', ['₹2,00,000', '₹1,80,000', '₹1,20,000', '₹1,35,000'], 0,
          'Financial BEP = Interest + PD ÷ (1 – t) = 1,20,000 + 60,000 ÷ 0.75 = 1,20,000 + 80,000 = ₹2,00,000. Preference dividend is grossed up because it is paid from post-tax profit. In practice: forgetting the gross-up understates BEP.', 'c7', T7, 'hard', check=200000),
        Q('m11', 'A sign of over-capitalisation is:', ['Fall in dividend rate and share price', 'Very high dividend rate', 'Market value far above book value', 'Bonus issue'], 0,
          'Over-capitalised firms earn too little on their capital to pay normal dividends and interest, so dividends and share prices fall. High dividends and high market value relative to book point to under-capitalisation. In practice: idle assets and excessive goodwill are common causes.', 'c8', T8),
        Q('m12', 'A remedy for under-capitalisation is:', ['Issue of bonus shares', 'Buy-back of shares', 'Reduction of face value', 'Redemption of debentures'], 0,
          'Under-capitalised firms have too little capital for their earnings; capitalising reserves through bonus shares or splitting shares brings the rate of dividend per share to a normal level. Buy-backs and reductions are remedies for over-capitalisation. In practice: bonus issues also improve liquidity of shares.', 'c8', T8),
        Q('m13', 'Which is NOT one of the three goals balanced in designing capital structure?', ['Maximising sales', 'Keeping control', 'Limiting financial risk', 'Minimising cost of capital'], 0,
          'The study material frames capital structure around control, risk and cost, with value maximisation as the guiding objective. Sales maximisation is an operating goal, not a financing one. In practice: the three goals conflict and must be balanced.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'NI equity value', 1.5, 'computation', 'equity', nums=[eq_ni]),
           S('s2', 'NI value and Ko', 1.5, 'computation', 'ko', nums=[v_ni, ko_ni]),
           S('s3', 'NOI value and equity', 1.5, 'computation', 'noi', nums=[v_noi, eq_noi]),
           S('s4', 'NOI Ke', 1.5, 'computation', 'ke', nums=[ke_noi])],
          ['Compute side by side.'], ['Treating Ke as constant under NOI.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Vu', 1.5, 'computation', 'unlevered|uday', nums=[vu]),
           S('s2', 'Tax shield', 1, 'computation', 'shield|td', nums=[shield]),
           S('s3', 'VL and equity', 1.5, 'computation', 'levered|lata', nums=[vl, el])],
          ['Apply VL = Vu + tD.'], ['Ignoring tax in Vu.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 6, i3['q'], i3['solution'],
          [S('s1', 'Indifference equation', 1.5, 'concept', 'equal|indifference'),
           S('s2', 'Indifference EBIT', 1.5, 'computation', 'ebit', nums=[ind]),
           S('s3', 'Financial BEP', 1, 'computation', 'break-even|break even', nums=[fbep]),
           S('s4', 'EPS under both plans', 2, 'computation', 'eps', nums=[eps_a, eps_b])],
          ['Cancel the tax factor.'], ['Using total funds instead of share counts.'], ['Equation + table.'], pad='table', checks=list(ck3)),
        W('q4', 4, 'Distinguish over-capitalisation from under-capitalisation, giving one cause and one remedy of each.',
          [table(['Point', 'Over-capitalisation', 'Under-capitalisation'], [
              ['Meaning', 'Capital more than the earning capacity justifies', 'Capital less than the earning capacity justifies'],
              ['Sign', 'Low dividend rate, falling share price', 'High dividend rate, share price well above book value'],
              ['Cause', 'Raising more funds than can be used profitably; paying too much for goodwill', 'Under-estimating earnings; unrecorded appreciation of assets'],
              ['Remedy', 'Repay debt, buy back shares, reduce face value', 'Bonus shares, share split, higher face value']])],
          [S('s1', 'Meanings', 1, 'concept', 'earning capacity|earnings'),
           S('s2', 'Signs', 1, 'concept', 'dividend'),
           S('s3', 'Causes', 1, 'concept', 'goodwill|under-estimat|more funds'),
           S('s4', 'Remedies', 1, 'concept', 'bonus|buy back|buy-back')],
          ['Use a comparison table.'], ['Mixing up the remedies.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the indifference point in EBIT–EPS analysis?',
          'It is the level of EBIT at which two financing plans give the same EPS; above it the plan with more fixed charges gives higher EPS.',
          [P('p1', 'Same EPS', 6, 'same eps|equal'), P('p2', 'Above favours leverage', 4, 'above|fixed charge|debt')], 'c7'),
        V('v2', 'State MM\'s conclusion with corporate tax.',
          'With corporate tax, a levered firm is worth more than an unlevered one by the present value of the tax shield, so VL equals Vu plus tD.',
          [P('p1', 'Levered worth more', 5, 'more|higher'), P('p2', 'Tax shield tD', 5, 'shield|td|tax')], 'c4'),
        V('v3', 'How does the NOI approach treat capital structure?',
          'It treats it as irrelevant: the overall cost and value of the firm stay constant, while the cost of equity rises as debt is added.',
          [P('p1', 'Irrelevant', 4, 'irrelevant'), P('p2', 'Ko constant', 3, 'constant'), P('p3', 'Ke rises', 3, 'rises|increases')], 'c3'),
        V('v4', 'Give two signs of over-capitalisation.',
          'A falling rate of dividend and interest cover, and a falling market price of shares, often with window-dressing of accounts.',
          [P('p1', 'Falling dividend', 5, 'dividend'), P('p2', 'Falling share price', 5, 'price')], 'c8'),
        V('v5', 'Why might a firm follow the pecking order?',
          'Because outsiders know less than managers, so issuing equity can signal overvaluation; firms therefore use internal funds first, then debt, and equity last.',
          [P('p1', 'Information asymmetry', 4, 'know less|asymmetr|signal'), P('p2', 'Order internal-debt-equity', 6, 'internal', 'debt')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Pranav Plastics refinancing', 'difficulty': 'moderate',
              'case': 'Pranav Plastics Ltd. has 5,00,000 equity shares, no debt and EBIT of ₹24,00,000. It needs ₹40,00,000: (A) 2,00,000 new shares at ₹20, or (B) 10% debentures. Tax 25%. The P/E would be 12 under A and 10 under B.',
              'mcqs': [
                  M('k1a', 'EPS under Plan A is:', ['₹2.57', '₹3.60', '₹2.40', '₹3.00'], 0,
                    'EPS = 24,00,000 × 0.75 ÷ 7,00,000 = 18,00,000 ÷ 7,00,000 ≈ ₹2.57. There is no interest under Plan A, and the share count rises to 7,00,000. In practice: dilution lowers EPS.', 'core', check=2.57, topic=T7),
                  M('k1b', 'EPS under Plan B is:', ['₹3.00', '₹2.57', '₹3.60', '₹2.40'], 0,
                    'Interest = 10% × 40,00,000 = ₹4,00,000. EPS = (24,00,000 – 4,00,000) × 0.75 ÷ 5,00,000 = 15,00,000 ÷ 5,00,000 = ₹3.00. Leverage lifts EPS because EBIT is well above the indifference level. In practice: check risk too.', 'core', check=3, topic=T7),
                  M('k1c', 'Market price per share under each plan:', ['A ₹30.86; B ₹30.00', 'A ₹30.00; B ₹30.86', 'A ₹25.70; B ₹36.00', 'Both ₹30.00'], 0,
                    'MPS = EPS × P/E: Plan A 2.571 × 12 ≈ ₹30.86; Plan B 3.00 × 10 = ₹30.00. The market\'s lower P/E for the riskier debt plan more than offsets its higher EPS. In practice: MPS, not EPS, measures shareholder wealth.', 'hard', topic=T7),
                  M('k1d', 'On an MPS basis, the better plan is:', ['Plan A', 'Plan B', 'Both equal', 'Cannot say'], 0,
                    'Plan A gives a slightly higher market price (about ₹30.86 against ₹30.00), so it better maximises shareholder wealth despite lower EPS. This shows why EPS alone can mislead. In practice: always test the P/E effect of added risk.', 'moderate', topic=T7),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch05', 1, 'Financing Decisions – Capital Structure',
                ['Explain the meaning and goals of capital structure.',
                 'Apply the NI, Traditional, NOI and MM approaches, and explain trade-off and pecking order theories.',
                 'Identify factors affecting capital structure and the idea of an optimal structure.',
                 'Perform EBIT–EPS–MPS analysis, including indifference point and financial break-even.',
                 'Explain causes, effects and remedies of over- and under-capitalisation.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 55}, 'prereq': ['int-p6-a-ch04-u01'],
                 'exam_tip': 'Practise NI/NOI value tables, MM with tax (VL = Vu + tD), and EBIT–EPS indifference points with MPS; theory questions often ask over- vs under-capitalisation.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['V = EBIT/Ko.', 'NI: debt raises value; NOI: irrelevant; Traditional: optimum exists.', 'MM no tax: arbitrage → VL = Vu; with tax: VL = Vu + tD.',
                             'Trade-off: tax benefit vs distress costs; pecking order: internal → debt → equity.', 'Indifference EBIT equates EPS; financial BEP = I + PD/(1 – t).',
                             'MPS = EPS × P/E decides when risk changes P/E.', 'Over-capitalisation: low returns on too much capital; under-capitalisation: the reverse.'],
                 'remember': ['NOI: Ke = (EBIT – I)/(V – D).', 'Gross up preference dividend for tax in financial BEP.'],
                 'traps': ['Higher EPS is not always higher wealth.', 'Bonus issue cures under-, not over-capitalisation.']},
                [('Value of firm', 'EBIT ÷ Ko'), ('MM with tax', 'VL = Vu + tD'), ('Financial BEP', 'I + PD/(1–t)'), ('MPS', 'EPS × P/E'),
                 ('NOI Ke', '(EBIT – I)/(V – D)')],
                viva, cases,
                topics=['Meaning of Capital Structure', 'Capital Structure Theories', 'Factors Determining Capital Structure', 'Optimal Capital Structure',
                        'EBIT-EPS-MPS Analysis', 'Over-Capitalisation and Under-Capitalisation'])
