"""CA Final · Paper 2 Advanced Financial Management · Chapter 13 Business Valuation.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch13-u01'
T1 = 'Valuation approaches: asset, income and cash flow'
T2 = 'Cost of equity and beta for unlisted companies'
T3 = 'Relative valuation and chop-shop'
T4 = 'Value-based measures: EVA, MVA and SVA'
T5 = 'Special situations: distress, start-ups, digital platforms and ESG'


def build():
    ck = Checks()
    ba = ck.add('round(1.5/(1+(1-0.25)*0.5),4)', 'Asset (unlevered) beta')
    be = ck.add('round(1.5/(1+(1-0.25)*0.5)*(1+(1-0.25)*0.3),4)', 'Relevered equity beta')
    ke = ck.add('round(7+1.5/(1+(1-0.25)*0.5)*(1+(1-0.25)*0.3)*6,2)', 'Cost of equity (%)')
    i1 = {'id': 'i1', 'title': 'Beta for an unlisted firm', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A listed comparable has equity beta 1.5 and debt-to-equity 0.5. The unlisted target will have debt-to-equity 0.3. Tax rate 25%; risk-free rate 7%; market risk premium 6%. Assuming debt beta is zero, compute the target\'s cost of equity.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Unlever comparable', '1.5 ÷ [1 + 0.75 × 0.5]', inr(ba)],
              ['Relever for target', '1.0909 × [1 + 0.75 × 0.3]', inr(be)],
              ['Cost of equity', '7% + 1.3364 × 6%', inr(ke) + '%']], title='βa = βe ÷ [1 + (1 − t)D/E]')],
          'checks': list(ck)}

    ck2 = Checks()
    nopat = ck2.add('200*(1-0.25)', 'NOPAT (₹ crore)')
    eva = ck2.add('200*(1-0.25)-1000*0.12', 'EVA (₹ crore)')
    tv = ck2.add('round(80*(1+0.05)/(0.12-0.05),2)', 'Terminal value at end of year 5 (₹ crore)')
    i2 = {'id': 'i2', 'title': 'EVA and terminal value', 'difficulty': 'moderate', 'minutes': 8,
          'q': '(a) Jade Ltd. has EBIT of ₹200 crore, tax rate 25%, capital employed ₹1,000 crore and WACC 12%. Compute EVA. (b) Its free cash flow to firm in year 5 is ₹80 crore, growing at 5% thereafter. Compute the terminal value at the end of year 5.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['NOPAT', '200 × (1 − 0.25)', inr(nopat)],
              ['Capital charge', '1,000 × 12%', inr(120)],
              ['EVA', '150 − 120', inr(eva)],
              ['Terminal value', '80 × 1.05 ÷ (0.12 − 0.05)', inr(tv)]], title='EVA and Gordon terminal value')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Business valuation estimates the economic worth of a business for transactions, fund-raising, regulation, litigation or reporting. Key tools: present value, IRR, return on investment, and terminal value (often via the Gordon growth formula TV = CF × (1 + g) ÷ (k − g), or an exit multiple).',
            'Asset-based approach: net asset value (book or adjusted), net realisable value (liquidation) and replacement value — suits holding companies, asset-heavy or loss-making firms.',
            'Income approach: P/E or earnings yield multipliers and capitalisation of maintainable earnings. Cash-flow approach: discount FCFF at WACC (deduct debt for equity value) or FCFE at Ke, with explicit forecasts and a terminal value.'],
          'Assets show what it owns, earnings what it makes, cash flows what it is worth.',
          'A property-holding company is often valued on adjusted net assets.'),
        C('c2', T2, [
            'Cost of equity: CAPM (Rf + β × MRP), or arbitrage pricing with several factors.',
            'Unlisted companies lack market betas: take comparables\' equity betas, unlever them to asset beta βa = βe ÷ [1 + (1 − t)D/E] (debt beta zero), average, and relever at the target\'s capital structure βe = βa × [1 + (1 − t)D/E]. Adjust for size, liquidity and company-specific risk premiums.',
            'Discount rates must match cash flows and currency.'],
          'Borrow the risk from listed peers, then adjust for your own debt.',
          'Lower target leverage gives a lower relevered beta.'),
        C('c3', T3, [
            'Relative valuation values a business by comparison: P/E, price-to-book, EV/EBITDA, EV/sales, and sector-specific multiples (per subscriber, per tonne). Steps: choose comparables, compute multiples, adjust for differences in growth, risk and size, and apply to the target.',
            'Contemporary approaches include sum-of-the-parts valuation.',
            'The chop-shop method values a diversified company as if broken up: value each segment using industry multiples of pure-play firms, sum them, and compare with market value to detect a conglomerate discount.'],
          'Value it like its peers — piece by piece if necessary.',
          'A conglomerate trading below the sum of its parts may be a break-up target.'),
        C('c4', T4, [
            'Economic value added (EVA) = NOPAT − (capital employed × WACC): profit after charging for all capital. Positive EVA means value creation; it can drive incentives.',
            'Market value added (MVA) = market value of the firm (or equity) − capital invested by providers; it reflects the market\'s view of present value of future EVAs.',
            'Shareholder value analysis (SVA) uses value drivers — sales growth, operating margin, tax rate, investment in fixed and working capital, planning period and cost of capital — to compute shareholder value from free cash flows.'],
          'Profit is not value until it beats the cost of capital.',
          'NOPAT of 150 on capital of 1,000 at 12% WACC gives EVA of 30.'),
        C('c5', T5, [
            'Fair value is a market-participant, arm\'s-length price; going-concern value assumes continued operations, while non-going concern (liquidation) value assumes break-up. Distressed companies may be valued with modified DCF (probability-weighted scenarios), DCF plus distress value, APV, or relative valuation with distress-adjusted multiples.',
            'Start-ups lack history and profits; value drivers include team, market size, traction and IP. Methods: Berkus, cost-to-duplicate, comparable transactions, scorecard, First Chicago (weighted scenarios) and venture capital method (post-money value = exit value ÷ (1 + target return)^n; pre-money = post-money − investment).',
            'Digital platforms are valued on users, engagement, network effects and unit economics using income, market and cost approaches. ESG factors affect valuation through cash flows (costs, revenues, regulation) and discount rates (risk perception).'],
          'Unusual businesses need adapted methods and judgement.',
          'A VC targeting 40% return values a start-up by discounting its expected exit value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Valuing a private company stake', 'role': 'Registered valuer associate',
             'situation': 'A family-owned manufacturer is selling a 26% stake.',
             'steps': ['Select approaches suitable to the business.', 'Build beta from listed peers.', 'Run DCF and relative valuation.', 'Reconcile values and apply discounts for lack of control/marketability.'],
             'takeaway': 'Triangulate between methods and explain adjustments.'}]

    mcqs = [
        Q('m1', 'Unlevered (asset) beta equals:', ['βe ÷ [1 + (1 − t)D/E]', 'βe × D/E', 'βe + D/E', 'βe × (1 − t)'], 0,
          'Removes financial risk. In practice: relever for target.', 'c2', T2),
        Q('m2', 'EVA equals:', ['NOPAT − capital employed × WACC', 'Net profit − dividend', 'EBIT − interest', 'Sales − costs'], 0,
          'Residual income. In practice: value creation measure.', 'c4', T4),
        Q('m3', 'MVA equals:', ['Market value − capital invested', 'Book value − debt', 'EVA × WACC', 'Sales × margin'], 0,
          'Market view of future EVAs. In practice: listed firms.', 'c4', T4),
        Q('m4', 'The chop-shop method values a firm:', ['As the sum of its segments valued at pure-play multiples', 'On book value', 'On dividends', 'On cost'], 0,
          'Break-up value. In practice: conglomerate discount.', 'c3', T3),
        Q('m5', 'Net realisable value suits:', ['Liquidation scenarios', 'High-growth start-ups', 'Banks only', 'Digital platforms'], 0,
          'Break-up values. In practice: non-going concern.', 'c1', T1),
        Q('m6', 'In the venture capital method, post-money value equals:', ['Exit value ÷ (1 + target return)^n', 'Investment × 2', 'Book value', 'Sales × 1'], 0,
          'Discount exit value. In practice: pre-money = post − investment.', 'c5', T5),
        Q('m7', 'The Gordon terminal value formula is:', ['CF × (1 + g) ÷ (k − g)', 'CF ÷ g', 'CF × k', 'CF × (k − g)'], 0,
          'Perpetual growth. In practice: g below economy growth.', 'c1', T1),
        Q('m8', 'ESG factors affect valuation through:', ['Cash flows and discount rates', 'Only accounting policies', 'Nothing', 'Only tax'], 0,
          'Both channels. In practice: transition risks.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Unlever', 2, 'computation', 'unlever|asset beta', nums=[ba]), S('s2', 'Relever', 2, 'computation', 'relever', nums=[be]), S('s3', 'Ke', 2, 'computation', 'cost of equity', nums=[ke])],
          ['Use after-tax D/E.'], ['Ignoring tax in unlevering.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'NOPAT', 1.5, 'computation', 'nopat', nums=[nopat]), S('s2', 'EVA', 2, 'computation', 'eva', nums=[eva]), S('s3', 'TV', 2.5, 'computation', 'terminal', nums=[tv])],
          ['Use next-year cash flow for TV.'], ['Using year-5 flow without growth.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the three broad valuation approaches.', 'Asset-based, income-based (earnings) and cash-flow based (DCF) approaches.',
          [P('p1', 'Asset and income', 5, 'asset|income'), P('p2', 'Cash flow', 5, 'cash')], 'c1'),
        V('v2', 'How do you estimate beta for an unlisted company?', 'Unlever comparable listed companies\' betas to asset betas, average them and relever at the target\'s debt-equity ratio.',
          [P('p1', 'Unlever comparables', 5, 'unlever'), P('p2', 'Relever', 5, 'relever')], 'c2'),
        V('v3', 'What is relative valuation?', 'Valuing a business by applying multiples such as P/E or EV/EBITDA from comparable companies or transactions.',
          [P('p1', 'Multiples', 5, 'multiple'), P('p2', 'Comparables', 5, 'compar')], 'c3'),
        V('v4', 'What does a positive EVA indicate?', 'The business earns more than the cost of all the capital employed, so it creates value.',
          [P('p1', 'Above cost of capital', 5, 'cost'), P('p2', 'Creates value', 5, 'creates value')], 'c4'),
        V('v5', 'Why are traditional methods hard to apply to start-ups?', 'They have little history, negative profits and uncertain cash flows, so value depends on qualitative drivers and scenarios.',
          [P('p1', 'Little history', 5, 'history'), P('p2', 'Uncertain flows', 5, 'uncertain')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'BrightPath EdTech', 'difficulty': 'moderate',
              'case': 'A VC plans to invest ₹20 crore in BrightPath EdTech, expecting an exit value of ₹300 crore in 5 years and a target return of 50% a year. A diversified parent of BrightPath has two divisions: education (EBITDA ₹40 crore; peer EV/EBITDA 12) and printing (EBITDA ₹30 crore; peer 6). The parent\'s EV is ₹580 crore.',
              'mcqs': [
                  M('k1a', 'Post-money value of BrightPath (₹ crore, nearest whole):', ['40', '300', '20', '60'], 0,
                    '300 ÷ 1.5^5 = 300 ÷ 7.59 = 39.5. In practice: target return is high.', 'moderate', check=40, topic=T5),
                  M('k1b', 'Pre-money value (₹ crore, nearest whole):', ['20', '40', '60', '0'], 0,
                    '39.5 − 20 ≈ 20. In practice: negotiation basis.', 'moderate', check=20, topic=T5),
                  M('k1c', 'Chop-shop value of the parent (₹ crore):', ['660', '580', '480', '840'], 0,
                    '40 × 12 + 30 × 6. In practice: compare with EV.', 'core', check=660, topic=T3),
                  M('k1d', 'The parent trades at a conglomerate discount of (₹ crore):', ['80', '0', '160', '20'], 0,
                    '660 − 580. In practice: break-up may unlock value.', 'core', check=80, topic=T3),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch13', 1, 'Business Valuation',
                ['Apply asset, income and cash-flow valuation approaches.',
                 'Estimate cost of equity and beta for unlisted firms.',
                 'Use relative valuation and the chop-shop method.',
                 'Compute EVA, MVA and SVA.',
                 'Value distressed firms, start-ups and digital platforms and consider ESG.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 45}, 'prereq': ['fin-p2-ch12-u01'],
                 'exam_tip': 'State the approach, justify it for the business, and show unlever-relever steps clearly.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['NAV, earnings multiples, DCF with terminal value.',
                             'βa = βe ÷ [1 + (1 − t)D/E].',
                             'Relative valuation; chop-shop for conglomerates.',
                             'EVA = NOPAT − WACC × capital; MVA = MV − capital.',
                             'VC method, First Chicago for start-ups.'],
                 'remember': ['TV uses next year\'s cash flow.'],
                 'traps': ['Relevering without the tax adjustment.']},
                [('Unlever', 'βe ÷ [1 + (1−t)D/E]'), ('EVA', 'NOPAT − WACC × CE'), ('TV', 'CF(1+g)/(k−g)'), ('VC post-money', 'Exit ÷ (1+r)^n')],
                viva, cases)
