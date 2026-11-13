"""CA Final · Paper 2 Advanced Financial Management · Chapter 8 Mutual Funds.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch08-u01'
T1 = 'What mutual funds are and how they work'
T2 = 'Classification and types of schemes'
T3 = 'NAV, loads, expense ratio, side pocketing and tracking error'
T4 = 'Evaluating funds and the role of managers'


def build():
    ck = Checks()
    nav = ck.add('(520-20)/25', 'NAV per unit (₹)')
    ret = ck.add('round((20-18+1)/18*100,2)', 'Annual return to investor (%)')
    red = ck.add('20*(1-0.01)', 'Redemption price after 1% exit load (₹)')
    i1 = {'id': 'i1', 'title': 'NAV and holding-period return', 'difficulty': 'core', 'minutes': 7,
          'q': 'Growth Plus Fund holds securities worth ₹520 crore at market value and has liabilities (including accrued expenses) of ₹20 crore; 25 crore units are outstanding. NAV a year ago was ₹18 and a dividend of ₹1 per unit was paid during the year. Compute NAV, the investor\'s return, and the redemption price with a 1% exit load.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['NAV', '(520 − 20) ÷ 25', '₹' + inr(nav)],
              ['Return', '(20 − 18 + 1) ÷ 18', inr(ret) + '%'],
              ['Redemption price', '20 × (1 − 1%)', '₹' + inr(red)]], title='NAV and return')],
          'checks': list(ck)}

    ck2 = Checks()
    te = ck2.add('round(((0.15**2+0.15**2+0.25**2+0.25**2)/3)**0.5,3)', 'Tracking error (%)')
    i2 = {'id': 'i2', 'title': 'Tracking error of an index fund', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Over four quarters, an index fund\'s returns minus its benchmark\'s returns were +0.2%, −0.1%, +0.3% and −0.2%. Compute the tracking error (standard deviation of differences, using n − 1). What does a high tracking error indicate?',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Mean difference', '(0.2 − 0.1 + 0.3 − 0.2) ÷ 4', '0.05%'],
              ['Deviations', '0.15, −0.15, 0.25, −0.25', '—'],
              ['Variance', '(0.0225 + 0.0225 + 0.0625 + 0.0625) ÷ 3', '0.0567'],
              ['Tracking error', '√0.0567', inr(te) + '%'],
              ['Meaning', 'High value = fund deviates from index', 'Poor replication or costs']], title='Tracking error')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A mutual fund pools money from many investors and invests it in securities according to a stated objective, managed by an asset management company (AMC) under a trust structure regulated by SEBI. Investors hold units whose value moves with the fund\'s net asset value.',
            'Benefits: professional management, diversification, liquidity, low cost of entry, transparency, regulation and convenience (SIPs, switches). Drawbacks: costs and fees, no control over holdings, possible underperformance, over-diversification and tax or exit-load frictions.',
            'Individuals, HUFs, companies, trusts, NRIs and institutions can invest. Direct plans (bought without distributors) carry lower expense ratios than regular plans.'],
          'Pool the money, hire a professional, share the results.',
          'A ₹500 monthly SIP gives a small investor a diversified portfolio.'),
        C('c2', T2, [
            'By structure: open-ended (continuous buying and redemption), close-ended (fixed maturity, listed) and interval funds. By portfolio: equity, debt (gilt, liquid, income, money market), hybrid/balanced and special funds (index, sector, thematic, international, fund of funds).',
            'Types of schemes: diversified equity, ELSS (tax-saving with lock-in), sector and thematic funds, arbitrage funds (exploit cash-futures price differences), hedge funds, cash funds, exchange-traded funds (trade on exchanges like shares, track an index or commodity such as gold), and fixed maturity plans (closed-ended debt with set tenure).',
            'By ownership: public sector, private sector and foreign-sponsored AMCs.'],
          'Match the scheme to the goal and horizon.',
          'An ETF tracking Nifty trades on the exchange throughout the day.'),
        C('c3', T3, [
            'Net asset value (NAV) per unit = (market value of investments + other assets − liabilities including accrued expenses) ÷ units outstanding. Holding-period return = (closing NAV − opening NAV + distributions) ÷ opening NAV.',
            'Entry loads are not charged in India (abolished by SEBI); exit loads may apply on early redemption. Trail commission is paid to distributors over time. The expense ratio (annual expenses ÷ average net assets) reduces returns and is capped by SEBI.',
            'Side pocketing segregates a stressed or downgraded debt security into a separate portfolio, protecting other investors and allowing recovery to be shared fairly. Tracking error is the standard deviation of the difference between fund and benchmark returns — the key quality measure for index funds and ETFs.'],
          'NAV is net assets per unit; costs and tracking error eat into it.',
          'A downgraded bond moved into a side pocket stops it dragging down main NAV.'),
        C('c4', T4, [
            'Quantitative evaluation: absolute and relative returns versus benchmark and peers, risk-adjusted measures (Sharpe, Treynor, Jensen\'s alpha), expense ratio, tracking error, portfolio turnover and fund size.',
            'Qualitative evaluation: fund house reputation, manager track record and stability, investment process, portfolio quality and concentration, and service.',
            'Actively managed funds aim to beat a benchmark through selection and timing; passively managed funds aim to replicate an index at low cost. FPIs (earlier FIIs) influence market liquidity and flows and can invest via mutual funds and directly.'],
          'Judge a fund on risk-adjusted returns, costs and the people behind it.',
          'A passive fund wins if its costs and tracking error stay very low.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Fund selection for a client', 'role': 'Investment adviser',
             'situation': 'A client wants a long-term equity fund and a short-term parking option.',
             'steps': ['Match objective and horizon to scheme type.', 'Compare risk-adjusted returns and expense ratios.', 'Check tracking error for index options.', 'Recommend direct plans where suitable.'],
             'takeaway': 'Costs and consistency often matter more than last year\'s winner.'}]

    mcqs = [
        Q('m1', 'NAV per unit equals:', ['(Assets − liabilities) ÷ units outstanding', 'Assets ÷ units', 'Profit ÷ units', 'Face value'], 0,
          'Market value basis. In practice: daily NAV.', 'c3', T3),
        Q('m2', 'Entry loads on mutual fund purchases in India are:', ['Not charged', 'Up to 2.25%', 'Mandatory', 'Only on ELSS'], 0,
          'SEBI abolished them. In practice: exit loads may apply.', 'c3', T3),
        Q('m3', 'Tracking error measures:', ['Variability of the difference between fund and index returns', 'Total return', 'Expense ratio', 'NAV growth'], 0,
          'Key for passive funds. In practice: lower is better.', 'c3', T3),
        Q('m4', 'Side pocketing is used to:', ['Segregate stressed securities from the main portfolio', 'Increase returns', 'Avoid tax', 'Merge funds'], 0,
          'Protects investors fairly. In practice: debt funds.', 'c3', T3),
        Q('m5', 'An ELSS scheme offers:', ['Tax benefits with a lock-in period', 'Guaranteed returns', 'No equity exposure', 'Daily redemption'], 0,
          'Equity-linked saving. In practice: three-year lock-in.', 'c2', T2),
        Q('m6', 'Exchange-traded funds:', ['Trade on stock exchanges like shares', 'Can only be bought from AMC', 'Are close-ended debt funds', 'Have no NAV'], 0,
          'Intra-day trading. In practice: low costs.', 'c2', T2),
        Q('m7', 'Direct plans have lower:', ['Expense ratios', 'NAV always', 'Risk', 'Returns'], 0,
          'No distributor commission. In practice: higher NAV over time.', 'c1', T1),
        Q('m8', 'Jensen\'s alpha for a fund measures:', ['Return above CAPM-predicted return', 'Total risk', 'Expense ratio', 'Tracking error'], 0,
          'Manager value added. In practice: quantitative evaluation.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'NAV', 2, 'computation', 'nav', nums=[nav]), S('s2', 'Return', 2, 'computation', 'return', nums=[ret]), S('s3', 'Redemption', 1, 'computation', 'redemption', nums=[red])],
          ['Include dividend.'], ['Ignoring liabilities.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Computation', 3, 'computation', 'tracking', nums=[te]), S('s2', 'Meaning', 1, 'concept', 'deviat|replication')],
          ['State n − 1.'], ['Averaging differences only.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a mutual fund?', 'A trust that pools investors\' money and invests it in securities per a stated objective, managed by an AMC and regulated by SEBI.',
          [P('p1', 'Pools money', 5, 'pool'), P('p2', 'AMC and SEBI', 5, 'amc|sebi')], 'c1'),
        V('v2', 'Distinguish open-ended and close-ended funds.', 'Open-ended funds issue and redeem units continuously; close-ended funds have a fixed maturity and are traded on exchanges.',
          [P('p1', 'Continuous', 5, 'continuous'), P('p2', 'Fixed maturity', 5, 'fixed maturity')], 'c2'),
        V('v3', 'What is the expense ratio?', 'Annual operating expenses of the scheme as a percentage of its average net assets.',
          [P('p1', 'Expenses', 5, 'expense'), P('p2', 'Average net assets', 5, 'net assets')], 'c3'),
        V('v4', 'What is side pocketing?', 'Moving a stressed or downgraded security into a separate portfolio so other investors are protected and recoveries go to holders on that date.',
          [P('p1', 'Separate portfolio', 5, 'separate'), P('p2', 'Stressed security', 5, 'stressed|downgrad')], 'c3'),
        V('v5', 'Name qualitative factors in fund evaluation.', 'Fund house reputation, manager track record, investment process and portfolio quality.',
          [P('p1', 'Manager and fund house', 5, 'manager|fund house'), P('p2', 'Process and quality', 5, 'process|quality')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Shree Balanced Fund', 'difficulty': 'core',
              'case': 'Shree Balanced Fund had opening NAV ₹50 and closing NAV ₹54, after paying a dividend of ₹2. Its expense ratio is 1.8% (regular plan) and 0.9% (direct plan). A bond in its portfolio worth 3% of NAV was downgraded to default.',
              'mcqs': [
                  M('k1a', 'Investor return for the year (%):', ['12', '8', '4', '16'], 0,
                    '(54 − 50 + 2) ÷ 50. In practice: holding-period return.', 'core', check=12, topic=T3),
                  M('k1b', 'Annual cost saving from the direct plan on ₹10 lakh (₹):', ['9,000', '18,000', '900', '90,000'], 0,
                    '0.9% × 10,00,000. In practice: compounding increases benefit.', 'core', check=9000, topic=T3),
                  M('k1c', 'The defaulted bond may be:', ['Side-pocketed', 'Ignored', 'Valued at par', 'Sold to the AMC'], 0,
                    'Segregated portfolio. In practice: SEBI framework.', 'core', topic=T3),
                  M('k1d', 'The fund is classified as:', ['Hybrid (balanced)', 'Pure equity', 'Liquid', 'ETF'], 0,
                    'Mixes equity and debt. In practice: moderate risk.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch08', 1, 'Mutual Funds',
                ['Explain mutual funds, their benefits and drawbacks.',
                 'Classify funds and describe scheme types.',
                 'Compute NAV and returns; explain loads, expense ratio, side pocketing and tracking error.',
                 'Evaluate funds and the role of managers and FPIs.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p2-ch07-u01'],
                 'exam_tip': 'Mutual fund sums usually test NAV, returns with distributions, and loads.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Trust + AMC + SEBI regulation.',
                             'Open, close-ended, interval; equity, debt, hybrid.',
                             'NAV = net assets ÷ units.',
                             'No entry load; exit loads possible; expense ratio capped.',
                             'Evaluate with Sharpe, Treynor, alpha, tracking error.'],
                 'remember': ['Return includes distributions.'],
                 'traps': ['Adding entry load in Indian NAV questions.']},
                [('NAV', '(Assets − liabilities) ÷ units'), ('Return', '(ΔNAV + D) ÷ NAV₀'), ('Tracking error', 'σ of differences'), ('Side pocket', 'Segregate stressed debt')],
                viva, cases)
