"""CA Final · Paper 2 Advanced Financial Management · Chapter 4 Security Analysis.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch04-u01'
T1 = 'Fundamental analysis: economy, industry, company'
T2 = 'Technical analysis: theories and charts'
T3 = 'Moving averages and market indicators'
T4 = 'Efficient market hypothesis'


def build():
    ck = Checks()
    p0 = ck.add('10*0.4/(0.14-0.09)', 'Intrinsic value per share (₹)')
    pe = ck.add('10*0.4/(0.14-0.09)/10', 'Justified P/E on next year earnings')
    i1 = {'id': 'i1', 'title': 'Intrinsic value and P/E', 'difficulty': 'core', 'minutes': 7,
          'q': 'Expected EPS of Cobalt Ltd. next year is ₹10; it pays out 40% as dividends; required return 14%; long-term growth 9%. The share trades at ₹95. Compute intrinsic value and justified P/E, and give the analyst\'s call.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Next dividend', '10 × 40%', '₹4'],
              ['Intrinsic value', '4 ÷ (0.14 − 0.09)', '₹' + inr(p0)],
              ['Justified P/E', '80 ÷ 10', inr(pe)],
              ['Market price', '₹95 > ₹80', 'Overvalued — sell or avoid']], title='P₀ = payout × E₁ ÷ (k − g)')],
          'checks': list(ck)}

    ck2 = Checks()
    ama = ck2.add('(52+54+53+55+56)/5', '5-day arithmetic moving average (₹)')
    ema = ck2.add('0.2*56+0.8*53', 'Exponential moving average for day 5 (₹)')
    i2 = {'id': 'i2', 'title': 'Moving averages', 'difficulty': 'core', 'minutes': 6,
          'q': 'Closing prices of a share over five days: ₹52, 54, 53, 55, 56. Compute the 5-day arithmetic moving average. If the EMA up to day 4 was ₹53 and the smoothing factor is 0.2, compute the day-5 EMA. Interpret if the price is above both averages.',
          'solution': [table(['Measure', 'Working', '₹'], [
              ['5-day AMA', '(52 + 54 + 53 + 55 + 56) ÷ 5', inr(ama)],
              ['Day-5 EMA', '0.2 × 56 + 0.8 × 53', inr(ema)],
              ['Interpretation', 'Price above rising averages', 'Bullish short-term signal']], title='Moving averages')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Fundamental analysis estimates a share\'s intrinsic value from economic, industry and company factors, and compares it with market price: buy if undervalued, sell if overvalued. The dividend growth model links value to the P/E: P₀ = payout × E₁ ÷ (k − g).',
            'Economic analysis studies GDP growth, inflation, interest rates, fiscal and monetary policy, exchange rates, savings and investment, and uses tools such as anchoring, econometric models and leading indicators. Industry analysis looks at the life cycle (pioneer, expansion, stagnation, decline), demand-supply, competition (Porter\'s forces), regulation and cost structure.',
            'Company analysis examines financial statements and ratios, earnings quality, management, competitive position, capital structure and growth prospects, and forecasts earnings and dividends.'],
          'Top-down: economy → industry → company → value.',
          'A strong company in a declining industry may still disappoint.'),
        C('c2', T2, [
            'Technical analysis studies past prices and volumes to predict future movements. It assumes market value is set by supply and demand, prices move in trends that persist, trend changes are caused by shifts in supply and demand, and patterns tend to repeat.',
            'Theories: Dow Theory — primary (long), secondary (intermediate) and daily movements, with trends confirmed by averages; Elliott Wave Theory — markets move in five-wave advances and three-wave corrections; Random Walk Theory — price changes are independent, challenging technical analysis.',
            'Charts: line, bar, candlestick and point-and-figure charts; patterns like head and shoulders, double tops and bottoms, triangles; support (where buying stops falls) and resistance (where selling stops rises).'],
          'Technicians read the crowd\'s behaviour in price and volume.',
          'A break above a resistance level on high volume is read as bullish.'),
        C('c3', T3, [
            'Moving averages smooth price data to show trends. Arithmetic moving average gives equal weight to the last n prices; exponential moving average gives more weight to recent prices: EMA today = α × price + (1 − α) × previous EMA.',
            'Signals: a price rising through a flattening or rising average is a buy signal; falling through a flattening or falling average is a sell signal. Long (200-day), intermediate (60-day) and short (10-day) averages identify different trends.',
            'Market indicators: breadth (advances vs declines), volume, short interest, and confidence indices help judge market strength. Technical analysis can be self-fulfilling but is subjective and often late.'],
          'Averages smooth noise so trends show.',
          'A short average crossing above a long average is a common buy signal.'),
        C('c4', T4, [
            'The efficient market hypothesis (EMH) says prices fully reflect available information, so investors cannot consistently earn abnormal returns. It does not mean prices are always right, that no one ever beats the market, or that analysis is useless — competition among analysts is what makes markets efficient.',
            'Weak form: prices reflect all past price and volume data (technical analysis cannot beat the market) — tested by serial correlation, runs and filter tests. Semi-strong form: prices reflect all public information (fundamental analysis of public data cannot beat it) — tested by event studies. Strong form: prices reflect all information including private — tested by insider and fund manager performance.',
            'Challenges: market anomalies (calendar effects, size effects, momentum), behavioural biases, bubbles and information asymmetry. Equity research uses tools like DCF, relative valuation, ratio screens and data analytics.'],
          'The more efficient the market, the harder it is to beat.',
          'Prices jumping instantly on an earnings announcement support semi-strong efficiency.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Initiating coverage on a stock', 'role': 'Equity research analyst',
             'situation': 'You must issue a buy/hold/sell call on a mid-cap cement company.',
             'steps': ['Assess economic outlook and infrastructure spending.', 'Analyse the cement industry cycle and capacity.', 'Forecast company earnings and value the share.', 'Cross-check timing with technical indicators.'],
             'takeaway': 'Fundamentals give the value; technicals help with timing.'}]

    mcqs = [
        Q('m1', 'Fundamental analysis follows the order:', ['Economy, industry, company', 'Company, industry, economy', 'Charts, volume, price', 'Industry only'], 0,
          'Top-down approach. In practice: concentric circles.', 'c1', T1),
        Q('m2', 'Elliott Wave Theory suggests markets advance in:', ['Five waves and correct in three', 'Two waves', 'Random steps', 'Ten waves'], 0,
          'Wave counting. In practice: subjective labelling.', 'c2', T2),
        Q('m3', 'The weak form of EMH implies:', ['Technical analysis cannot earn abnormal returns', 'Insiders cannot profit', 'Fundamental analysis cannot work', 'Prices are random always'], 0,
          'Past prices are reflected. In practice: tested by runs tests.', 'c4', T4),
        Q('m4', 'An exponential moving average gives:', ['More weight to recent prices', 'Equal weights', 'More weight to old prices', 'No weights'], 0,
          'Reacts faster to change. In practice: smoothing factor.', 'c3', T3),
        Q('m5', 'Event studies test:', ['Semi-strong form efficiency', 'Weak form', 'Strong form', 'Dow theory'], 0,
          'Reaction to public announcements. In practice: abnormal returns around events.', 'c4', T4),
        Q('m6', 'Support level is where:', ['Falling prices tend to stop due to buying', 'Rising prices stop', 'Volume is zero', 'Earnings peak'], 0,
          'Demand absorbs supply. In practice: resistance is the opposite.', 'c2', T2),
        Q('m7', 'If the market price exceeds intrinsic value, a fundamental analyst recommends:', ['Selling', 'Buying', 'Holding forever', 'Short-term trading only'], 0,
          'Overvalued. In practice: target price below market.', 'c1', T1),
        Q('m8', 'Insider trading profits are evidence against:', ['Strong form efficiency', 'Weak form', 'Dow theory', 'Random walk'], 0,
          'Private information has value. In practice: regulators ban it.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Dividend', 1, 'computation', 'dividend', nums=[4]), S('s2', 'Value', 2, 'computation', 'intrinsic', nums=[p0]), S('s3', 'P/E and call', 2, 'computation', 'p/e|overvalued', nums=[pe])],
          ['Give the call.'], ['Using EPS instead of dividend.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'AMA', 1.5, 'computation', 'ama', nums=[ama]), S('s2', 'EMA', 1.5, 'computation', 'ema', nums=[ema]), S('s3', 'Signal', 1, 'concept', 'bullish|buy')],
          ['Interpret.'], ['Weighting EMA wrongly.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is fundamental analysis?', 'Estimating a security\'s intrinsic value from economic, industry and company factors and comparing it with its market price.',
          [P('p1', 'Intrinsic value', 5, 'intrinsic'), P('p2', 'Economy, industry, company', 5, 'economic|industry|company')], 'c1'),
        V('v2', 'State the assumptions of technical analysis.', 'Prices are set by supply and demand, move in persistent trends, change with shifts in supply and demand, and patterns repeat.',
          [P('p1', 'Supply and demand', 5, 'supply'), P('p2', 'Trends and patterns', 5, 'trend|pattern')], 'c2'),
        V('v3', 'Explain the three forms of market efficiency.', 'Weak form reflects past prices, semi-strong reflects all public information, and strong form reflects all information including private.',
          [P('p1', 'Weak and semi-strong', 5, 'weak|semi-strong'), P('p2', 'Strong form', 5, 'strong')], 'c4'),
        V('v4', 'What is the Dow Theory?', 'Markets have primary, secondary and daily movements; the primary trend is confirmed when industrial and transport averages move together.',
          [P('p1', 'Primary and secondary', 5, 'primary|secondary'), P('p2', 'Confirmation', 5, 'confirm')], 'c2'),
        V('v5', 'How does an EMA differ from an AMA?', 'An EMA weights recent prices more heavily, while an AMA weights all prices equally.',
          [P('p1', 'Recent weight', 5, 'recent'), P('p2', 'Equal weights', 5, 'equal')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Cement Ltd.', 'difficulty': 'moderate',
              'case': 'Delta Cement Ltd. has expected EPS of ₹20, payout 50%, required return 12% and growth 7%. Its share trades at ₹180 and has just broken above a resistance level of ₹175 on high volume. A study finds Delta\'s price adjusts within minutes of public earnings announcements.',
              'mcqs': [
                  M('k1a', 'Intrinsic value (₹):', ['200', '180', '400', '143'], 0,
                    '10 ÷ (0.12 − 0.07). In practice: compare with ₹180.', 'core', check=200, topic=T1),
                  M('k1b', 'Justified P/E:', ['10', '9', '20', '5'], 0,
                    '200 ÷ 20. In practice: market P/E is 9.', 'core', check=10, topic=T1),
                  M('k1c', 'The resistance breakout on high volume is read as:', ['Bullish', 'Bearish', 'Neutral', 'A reversal down'], 0,
                    'Buyers overcame sellers. In practice: old resistance may become support.', 'core', topic=T2),
                  M('k1d', 'Rapid price adjustment to earnings news supports:', ['Semi-strong form efficiency', 'Strong form only', 'Weak form failure', 'Elliott waves'], 0,
                    'Public information is quickly reflected. In practice: event study evidence.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch04', 1, 'Security Analysis',
                ['Apply fundamental analysis from economy to company.',
                 'Explain technical analysis theories and chart patterns.',
                 'Compute and interpret moving averages and market indicators.',
                 'Explain and test the efficient market hypothesis.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['fin-p2-ch03-u01'],
                 'exam_tip': 'Theory questions favour EMH forms and Dow/Elliott theories; sums favour intrinsic value and moving averages.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Fundamental: economy → industry → company → value.',
                             'P₀ = payout × E₁ ÷ (k − g).',
                             'Technical: trends, patterns, support and resistance.',
                             'AMA equal weights; EMA recent weights.',
                             'EMH: weak, semi-strong, strong.'],
                 'remember': ['Efficiency comes from competing analysts.'],
                 'traps': ['Using EPS instead of dividend in the growth model.']},
                [('Weak form', 'Past prices'), ('Semi-strong', 'Public info'), ('Strong', 'All info'), ('EMA', 'αP + (1−α)EMA₋₁')],
                viva, cases)
