"""CA Foundation · Paper 4 Business Economics · Chapter 6 Business Cycles (single unit).
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch06-u01'


def Q(i, q, o, a, e, c, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if check: m['check'] = check
    return m


def build():
    # ---------- Illustration 1: identify phases from a real GDP series ----------
    c1 = Checks()
    gdp = [100, 104, 108, 111, 112, 110, 106, 103, 102, 104, 108, 113]
    rows1 = [['Year 1', '100', '—', '—']]
    for i in range(1, len(gdp)):
        g = c1.add(f'round(({gdp[i]}-{gdp[i-1]})/{gdp[i-1]}*100,2)', f'growth in year {i+1}')
        if i == 4: ph = 'Peak (highest point; growth almost nil)'
        elif i == 8: ph = 'Trough (lowest point)'
        elif i < 4: ph = 'Expansion'
        elif i < 8: ph = 'Contraction'
        else: ph = 'Recovery / expansion'
        rows1.append([f'Year {i+1}', str(gdp[i]), str(g), ph])
    t1 = table(['Year', 'Real GDP index', 'Growth over previous year (%)', 'Phase'], rows1, num=[1, 2], title='Real GDP of Udaypur State (index, Year 1 = 100)')
    fall = c1.add('round((102-112)/112*100,2)', 'peak-to-trough fall %')
    rise = c1.add('round((113-102)/102*100,2)', 'trough-to-latest rise %')

    # ---------- Illustration 3: deviation from trend ----------
    c3 = Checks()
    trend = [200, 210, 220, 230, 240, 250]
    actual = [198, 216, 233, 236, 228, 241]
    rows3 = []
    for i, (t, a) in enumerate(zip(trend, actual)):
        dv = c3.add(f'{a}-{t}', f'deviation year {i+1}')
        pc = c3.add(f'round(({a}-{t})/{t}*100,2)', f'deviation % year {i+1}')
        rows3.append([f'Year {i+1}', str(t), str(a), str(dv), str(pc)])
    t3 = table(['Year', 'Trend GDP (₹ ’000 crore)', 'Actual GDP', 'Actual − trend', 'Deviation (% of trend)'], rows3, num=[1, 2, 3, 4], title='Actual output around its trend')

    # ---------- written questions ----------
    w1 = Checks()
    w1g = [w1.add(f'round(({b}-{a})/{a}*100,2)', f'growth {i+2}') for i, (a, b) in enumerate(zip([500, 530, 556, 562, 545], [530, 556, 562, 545, 540]))]
    w1g6 = w1.add('round((556-540)/540*100,2)', 'growth year 7')

    # ---------- case ----------
    k = Checks()
    kg1 = k.add('round((9.0-9.6)/9.6*100,2)', 'case: % change in GDP quarter 2')
    kg2 = k.add('round((8.7-9.0)/9.0*100,2)', 'case: % change in GDP quarter 3')

    concepts = [
        {'id': 'c1', 'title': 'Meaning of business cycles', 'body': [
            'Business cycles (trade cycles) are the rhythmic ups and downs in overall economic activity that an economy goes through over time — periods of prosperity (rising output, prices and employment) alternating with periods of downturn (falling output and prices, rising unemployment). They show up in aggregate measures such as GNP, employment and income.',
            'They are recurrent — they happen again and again — but not periodic: they do not come at regular intervals and are not of the same length. Some last several years; others are over in two or three years.',
            'Economists draw a smooth trend line showing steady growth without cycles; actual output moves above and below this trend.'],
         'analogy': 'Waves on a rising tide: the tide (trend growth) keeps coming in, but the water level at any moment bobs above and below it in waves of uneven size.',
         'work': 'Auditors and analysts always ask "where are we in the cycle?" before judging whether a client\'s sales drop is company-specific or economy-wide.'},
        {'id': 'c2', 'title': 'Phases of a business cycle', 'body': [
            'Expansion (boom, upswing): output, employment, aggregate demand, consumer and investment spending, sales, profits, stock prices and bank credit all rise. It continues until resources are fully employed; involuntary unemployment is nearly zero and only frictional or structural unemployment remains. Prices and costs rise faster; living standards are high. Growth eventually slows.',
            'Peak (prosperity): the top of the cycle. Inputs become scarce and costly, output prices rise fast, cost of living rises and fixed-income earners are squeezed. Consumers cut back on houses and durables; actual demand stagnates. Growth pauses briefly before reversing.',
            'Contraction (downswing, recession): demand stops rising and starts falling in some sectors, but producers, not reading the change at once, keep producing — so supply exceeds demand. Firms then cancel investment plans and orders for equipment, materials and labour; the chain reaction spreads to capital-goods and raw-material producers. Input prices and incomes fall; consumers postpone purchases expecting lower prices; profits, investment, bank credit and stock prices fall and unemployment rises even as wages fall.',
            'Trough and depression: depression is a severe recession — growth turns negative, income and spending fall rapidly, prices are at their lowest, factories close, unemployment is widespread, interest rates fall but demand for credit falls too because confidence is low; banks may face crises; capital and durable-goods industries have large excess capacity; bankruptcies multiply. The lowest point is the trough (the Great Depression of 1929–33 is the classic case).',
            'Recovery: the trough marks the end of pessimism. Workers accept lower wages, producers expect lower costs, confidence returns, investment and stocks are rebuilt, banks expand credit, new technology needs new machines; employment, income and demand pick up and prices rise gradually — the economy moves into expansion again.',
            'No two cycles are alike: they vary in length and intensity and follow no fixed timetable; turning points are very hard to predict.'],
         'analogy': 'A roller-coaster ride: the climb (expansion), the top (peak), the plunge (contraction), the bottom (trough), and the slow climb out (recovery) — except that each ride has a different length and height.',
         'work': 'A CA preparing cash-flow forecasts for a bank loan builds "base", "slowdown" and "recovery" cases that mirror these phases.'},
        {'id': 'c3', 'title': 'Economic indicators: leading, lagging, coincident', 'body': [
            'Leading indicators change before real output changes, so they are used to forecast turning points: stock prices, new orders for consumer goods and for plant and equipment, building permits for houses, the share of companies reporting slower deliveries, consumer-confidence indices and the growth of money supply. They are useful but not always accurate — a stock-market fall may or may not be followed by a recession.',
            'Lagging indicators change only after output has changed, so they confirm a trend: the unemployment rate, labour cost per unit of output, the consumer price index and commercial lending activity (corporate profits and interest rates are also often listed).',
            'Coincident (concurrent) indicators move at the same time as the cycle and describe its current state: GDP, industrial production, personal income, retail sales and inflation.'],
         'blocks': [table(['Type', 'Timing', 'Examples', 'Use'], [
             ['Leading', 'Change before output', 'Stock prices, new orders, building permits, consumer confidence, money growth', 'Forecast turning points'],
             ['Coincident', 'Change with output', 'GDP, industrial production, personal income, retail sales', 'Describe the current phase'],
             ['Lagging', 'Change after output', 'Unemployment, labour cost per unit, CPI, commercial lending', 'Confirm a trend'],
         ], title='Three kinds of indicators')],
         'analogy': 'Leading indicators are the clouds gathering; coincident indicators are the rain; lagging indicators are the puddles left behind.',
         'work': 'Treasury and planning teams track purchasing-manager surveys and new-order data (leading) to decide on inventory and hiring well before GDP data (coincident) are released.'},
        {'id': 'c4', 'title': 'Business cycles in history', 'body': [
            'Great Depression (1930s): the longest, deepest and most widespread depression of the 20th century; it began in the USA and spread worldwide; world GDP fell by roughly 15% between 1929 and 1932. Keynes blamed a collapse in aggregate expenditure; monetarists blamed banking failures and a shrinking money supply; others pointed to deflation, over-indebtedness, low profits and pessimism. Recovery from 1933 was helped by money-supply growth, gold inflows and, later, war-time government spending.',
            'Dot-com (IT) bubble, about 1997–2000: low interest rates and venture capital poured money into new internet companies; over-optimism pushed their share prices up (adding ".com" to a name could lift its stock price); many gave services away free and spent lavishly in a "growth over profits" mindset. The bubble burst in 1999–2001; about half the dot-coms closed or were taken over, stock markets crashed and economies slowed.',
            'Global financial crisis (2008–09): after the 2000 bust the US Federal Reserve cut interest rates; cheap credit and new financial instruments led banks to lend for housing even to sub-prime borrowers; house prices rose, more houses were built, and when oversupply pushed prices down from 2006 the housing bubble burst (second half of 2007). Defaults caused heavy bank losses that spread through the US and world economy.'],
         'analogy': 'Each bubble is a balloon blown up with cheap credit and optimism; the bigger it gets, the louder the bang.',
         'work': 'The 2008 crisis is why auditors today look hard at credit quality, collateral values and expected-credit-loss models when the cycle is near a peak.'},
        {'id': 'c5', 'title': 'Features of business cycles', 'body': [
            '(a) They occur periodically but without the same regularity; their duration and intensity vary. (b) They have distinct phases — expansion, peak, contraction, trough — which are seldom smooth or of definite length. (c) They generally originate in free-market economies and are pervasive: a disturbance in one sector spreads to the others.',
            '(d) All sectors are affected, but capital-goods and durable consumer-goods industries are hit disproportionately, and industry is more prone to cyclical swings than agriculture. (e) They are complex, with no uniform features or single cause, so they are hard to predict accurately. (f) Their effects are felt at the same time on almost all economic variables — output, employment, investment, consumption, interest, trade and prices.',
            '(g) They are contagious and international: they start in one country and spread to others through trade (the 1930s depression in the USA and Britain affected almost all capitalist countries). (h) They have serious consequences for the well-being of society.'],
         'analogy': 'A cold in a crowded office: it starts at one desk, spreads to all, and hits some people (capital goods) much harder than others (agriculture).',
         'work': 'Sector analysts use beta-like "cyclicality" scores: a capital-goods client\'s order book will swing far more than a food company\'s sales.'},
        {'id': 'c6', 'title': 'Internal (endogenous) causes', 'body': [
            'Fluctuations in effective demand (Keynes): higher aggregate demand leads firms to produce more, raising output, income and jobs (and, if it outruns supply, inflation); low demand cuts output and employment — investors flee to safe assets like bonds and gold, job losses cut spending further, and a downward spiral follows until prices fall low enough for buying to resume. Changes in net exports also shift aggregate demand.',
            'Fluctuations in investment: investment is the most volatile part of aggregate demand because it depends on profit expectations, new inventions and the interest rate; rising investment shifts aggregate demand right and causes expansion, falling investment the opposite.',
            'Variations in government spending, especially during and after wars, destabilise the economy. Macroeconomic policies: expansionary fiscal or monetary policy (higher spending, tax cuts, lower interest rates — sometimes for political reasons) creates booms; anti-inflationary measures (spending cuts, higher taxes and interest rates) can slow the economy, sometimes into recession.',
            'Money supply (Hawtrey): the trade cycle is a purely monetary phenomenon; unplanned expansion of money and credit raises demand and activity (and eventually inflation); contraction of money supply starts a recession.',
            'Psychological factors (Pigou): waves of optimism and pessimism among businessmen drive investment and hence the cycle.',
            'Innovations (Schumpeter): cycles result from innovations that occur from time to time. Cobweb theory (Nicholas Kaldor): today\'s prices largely decide future production, so price fluctuations now cause output and employment fluctuations later.'],
         'analogy': 'Internal causes are like the engine and the driver\'s mood inside the car — demand, investment, credit and confidence.',
         'work': 'When RBI changes the repo rate, CAs in corporate treasury reassess borrowing costs and capex timing — monetary policy as a cause of cycles in action.'},
        {'id': 'c7', 'title': 'External (exogenous) causes', 'body': [
            'Wars: resources are diverted to producing weapons, so output of other capital and consumer goods falls, reducing income, profits and employment — a downturn may follow. Post-war reconstruction: rebuilding houses, roads and bridges lifts effective demand, output, employment and income.',
            'Technology shocks: new products and processes need large investment, which expands employment, income and profits — e.g. the mobile-phone boom in telecom.',
            'Natural factors: droughts and floods reduce farm output, cut farmers\' incomes and their demand for industrial goods, and raise food prices, leaving less to spend on industrial goods — this can cause an industrial recession, especially in agrarian economies.',
            'Population growth: if population grows faster than the economy, savings fall, so investment, income, employment and effective demand fall, slowing activity.',
            'Because economies are linked by trade, fluctuations spread across countries; changes in tax laws, trade rules, government spending, shifting production abroad and shifts in consumer tastes can also disrupt economies. Many cycles combine internal and external causes — e.g. the 2001 recession followed a mania in technology stocks and the 2007–09 recession followed speculation in US housing.'],
         'analogy': 'External causes are the road and the weather — wars, monsoons, inventions — that jolt the car from outside.',
         'work': 'A poor monsoon forecast prompts FMCG and two-wheeler companies to cut rural sales targets — a CA in industry builds this into the budget.'},
        {'id': 'c8', 'title': 'Relevance of business cycles in business decision making', 'body': [
            'Business cycles affect demand for a firm\'s products and hence its profits and survival. Knowing the phase helps in framing policies: prosperity opens up investment, employment and production opportunities; a downturn calls for caution.',
            'Managers must expand or rationalise production and adjust inputs — especially labour — to the phase; decisions on expansion or down-sizing, entry of a new business and the timing of a new product launch all depend on the phase. Surviving slow phases needs planned policies on product, price and promotion.',
            'Cyclical businesses — fashion retail, electrical goods, house-building, restaurants, advertising, overseas tour operators, construction and infrastructure — boom in expansions and suffer sharp drops in slumps. Some businesses actually gain in a downturn when customers see their products as good value or cheaper substitutes.',
            'Forecasts and entrepreneurs\' hunches are never fully reliable, but understanding the phase and using forecasts carefully helps firms anticipate and respond to changes before or soon after they happen.'],
         'analogy': 'A farmer reads the season before sowing; a business reads the cycle before expanding.',
         'work': 'Going-concern assessments, impairment tests and covenant reviews all depend on assumptions about the coming phase of the cycle — a CA must justify those assumptions.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Reading phases from real GDP data', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'The real GDP index of Udaypur State (Year 1 = 100) over 12 years is: 100, 104, 108, 111, 112, 110, 106, 103, 102, 104, 108, 113. Compute annual growth rates, identify the peak and trough, and label the phases. Also compute the percentage fall from peak to trough and the rise from trough to Year 12.',
         'solution': [t1, p(f'Peak in Year 5 (index 112), trough in Year 9 (index 102). Peak-to-trough fall = (102 − 112)/112 × 100 = {fall}%. Trough-to-Year 12 rise = (113 − 102)/102 × 100 = {rise}%, so by Year 12 output is above the old peak — the economy is in expansion again.'),
                      note('Growth slowed before the peak (3.85% → 2.78% → 0.9%) — a typical sign that expansion is losing steam.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Classifying indicators', 'difficulty': 'core', 'minutes': 6,
         'q': 'Classify each as a leading, coincident or lagging indicator and say what it is used for: (a) new orders for machinery; (b) industrial production index; (c) unemployment rate; (d) building permits for houses; (e) retail sales; (f) labour cost per unit of output; (g) stock-market index; (h) personal income.',
         'solution': [table(['Indicator', 'Type', 'Why'], [
             ['(a) New orders for machinery', 'Leading', 'Orders are placed before production rises'],
             ['(b) Industrial production', 'Coincident', 'Is itself part of current output'],
             ['(c) Unemployment rate', 'Lagging', 'Firms hire/fire only after output has changed'],
             ['(d) Building permits', 'Leading', 'Construction follows permits'],
             ['(e) Retail sales', 'Coincident', 'Move with current spending'],
             ['(f) Labour cost per unit of output', 'Lagging', 'Wages adjust after the cycle turns'],
             ['(g) Stock-market index', 'Leading', 'Prices reflect expected future profits'],
             ['(h) Personal income', 'Coincident', 'Moves with current output and employment'],
         ])]},
        {'id': 'i3', 'title': 'Output above and below trend', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Trend GDP grows by ₹10 thousand crore a year from 200. Actual GDP for six years is 198, 216, 233, 236, 228 and 241. Compute the deviation from trend in value and as a percentage, and say in which year the economy was furthest above and furthest below trend.',
         'solution': [t3, p('Furthest above trend: Year 3 (+5.91%) — near the peak of a boom. Furthest below trend: Year 5 (−5%) — a contraction. Year 6 shows recovery towards the trend.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Matching business decisions to the phase', 'difficulty': 'core', 'minutes': 6,
         'q': 'A consumer-durables company asks how its policies should change across the cycle. Prepare a short decision matrix.',
         'solution': [table(['Phase', 'Production & inventory', 'Labour', 'Investment & finance', 'Marketing'], [
             ['Expansion', 'Raise output; build stocks ahead of demand', 'Hire; add shifts', 'Expand capacity; borrow while credit is cheap', 'Launch new products'],
             ['Peak', 'Watch for slowing orders; avoid over-stocking', 'Use overtime/contract staff rather than permanent hires', 'Delay marginal projects; lock in long-term funding', 'Protect margins; costs rising'],
             ['Contraction', 'Cut output; clear inventory', 'Freeze hiring; rationalise', 'Conserve cash; defer capex; renegotiate debt', 'Value packs; promotions'],
             ['Trough / recovery', 'Rebuild stocks gradually as orders return', 'Rehire selectively', 'Restart deferred projects; buy assets cheaply', 'Re-launch; gain share'],
         ], title='Decision matrix across the cycle')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Leading indicators turn down', 'role': 'CA in industry — FP&A head at an auto-components maker',
         'situation': 'Monthly data show falling new orders from vehicle makers, a weaker purchasing-managers survey and a sliding stock market, though current sales are still strong.',
         'steps': ['Recognise that new orders and stock prices are leading indicators — they often turn before output.', 'Re-forecast the next two quarters with a slowdown case.', 'Recommend cutting raw-material purchase commitments, using contract labour for peak needs and deferring non-essential capex.', 'Watch coincident data (production, sales) to confirm; lagging data (unemployment, unit labour cost) will confirm later.'],
         'takeaway': 'Act on leading indicators with flexible, reversible steps; confirm with coincident data.', 'think': 'Why not wait until GDP data confirm the slowdown?', 'answer': 'GDP is a coincident indicator released with a lag; by the time it confirms, inventories and commitments would already be excessive.'},
        {'id': 'j2', 'title': 'Going-concern review in a recession', 'role': 'Statutory auditor of a real-estate developer',
         'situation': 'Housing sales have fallen sharply for three quarters, interest rates are high and the developer has large loan repayments due next year.',
         'steps': ['Identify the business as highly cyclical (house-building).', 'Stress-test cash flows for a longer contraction: lower bookings, slower collections, cost overruns.', 'Review covenant compliance, refinancing plans and lender support.', 'Assess whether a material uncertainty about going concern exists and whether disclosures are adequate.'],
         'takeaway': 'Cyclical businesses need cycle-aware audit judgements on going concern, impairment and inventory.'},
    ]

    mcqs = [
        Q('m1', 'Business cycles refer to:', ['Alternate expansion and contraction of overall economic activity', 'Seasonal changes in farm output only', 'Long-term growth of the economy', 'Changes in the price of one commodity'], 0, 'They are fluctuations in aggregate activity — output, employment, income.', 'c1'),
        Q('m2', 'Business cycles are:', ['Recurrent but not periodic', 'Periodic and of equal length', 'Non-recurrent', 'Confined to one sector'], 0, 'They recur, but at irregular intervals and with varying length.', 'c1'),
        Q('m3', 'The correct sequence of phases of a business cycle is:', ['Expansion → Peak → Contraction → Trough', 'Peak → Expansion → Trough → Contraction', 'Trough → Peak → Expansion → Contraction', 'Contraction → Expansion → Trough → Peak'], 0, 'After the trough comes recovery and a new expansion.', 'c2'),
        Q('m4', 'During the expansion phase, unemployment is mainly:', ['Frictional or structural', 'Involuntary and widespread', 'Cyclical and rising', 'Disguised in industry'], 0, 'Involuntary unemployment is close to zero near full employment.', 'c2', 'moderate'),
        Q('m5', 'Shortage of inputs, rapidly rising input and output prices, and stagnating actual demand are typical of the:', ['Peak', 'Trough', 'Depression', 'Recovery'], 0, 'At the peak growth stops before reversing.', 'c2'),
        Q('m6', 'During contraction, the initial mismatch between demand and supply arises because:', ['Producers keep producing at old levels without recognising the fall in demand', 'Government stops all spending', 'Supply falls faster than demand', 'Prices rise sharply'], 0, 'Supply then exceeds demand, and firms cut orders and investment.', 'c2', 'moderate'),
        Q('m7', 'A typical feature of depression is:', ['Low interest rates but falling demand for credit', 'Rising interest rates and booming credit', 'Full employment', 'Rising prices of capital goods'], 0, 'Confidence is so low that even cheap credit is not taken up.', 'c2', 'moderate'),
        Q('m8', 'The lowest point of a business cycle is called the:', ['Trough', 'Peak', 'Boom', 'Plateau'], 0, 'The trough marks the end of pessimism.', 'c2'),
        Q('m9', 'Recovery from a trough is first felt in the:', ['Labour market, as workers accept lower wages', 'Stock market only', 'Government budget', 'Foreign exchange market'], 0, 'Lower wages make producers expect lower costs and better conditions.', 'c2', 'moderate'),
        Q('m10', 'Which of the following is a leading indicator?', ['New orders for plant and equipment', 'Unemployment rate', 'Labour cost per unit of output', 'Industrial production'], 0, 'Orders change before production does.', 'c3'),
        Q('m11', 'Which of the following is a lagging indicator?', ['Unemployment rate', 'Building permits', 'Stock prices', 'Consumer confidence index'], 0, 'Employment adjusts only after output has changed.', 'c3'),
        Q('m12', 'GDP and industrial production are examples of:', ['Coincident indicators', 'Leading indicators', 'Lagging indicators', 'Structural indicators'], 0, 'They describe the current state of the cycle.', 'c3'),
        Q('m13', 'Indicators that confirm a trend after it has already occurred are:', ['Lagging indicators', 'Leading indicators', 'Coincident indicators', 'Diffusion indicators'], 0, 'Lagging indicators reflect past performance.', 'c3'),
        Q('m14', 'Real GDP rose from ₹250 lakh crore to ₹262 lakh crore in a year. The growth rate is:', ['4.8%', '12%', '4.58%', '5.2%'], 0, '(262 − 250)/250 × 100 = 4.8%. 4.58% divides by 262 instead of 250.', 'c1', 'core', '(262-250)/250*100'),
        Q('m15', 'A real GDP index falls from 125 at the peak to 110 at the trough. The percentage decline is:', ['12%', '15%', '13.64%', '8.8%'], 0, '(125 − 110)/125 × 100 = 12%. 13.64% uses the trough as the base.', 'c2', 'moderate', '(125-110)/125*100'),
        Q('m16', 'According to Keynes, the Great Depression was caused mainly by:', ['A fall in aggregate expenditure', 'A banking crisis and low money supply', 'Rapid population growth', 'War'], 0, 'Monetarists blamed banking failures and money supply; Keynes blamed deficient aggregate demand.', 'c4'),
        Q('m17', 'The dot-com bubble burst during:', ['1999–2001', '1929–33', '2007–09', '1973–75'], 0, 'Many internet companies ran out of capital and closed or were acquired.', 'c4'),
        Q('m18', 'The global financial crisis of 2008–09 originated in:', ['The US housing and financial markets (sub-prime lending)', 'Indian stock markets', 'European agriculture', 'Oil-exporting countries'], 0, 'Cheap credit and sub-prime lending fed a housing bubble that burst in 2007.', 'c4'),
        Q('m19', 'Which sectors are disproportionately affected by business cycles?', ['Capital goods and durable consumer goods', 'Agriculture', 'Essential food items', 'Public administration'], 0, 'Purchases of these can be postponed, so demand swings widely.', 'c5'),
        Q('m20', 'Business cycles are international in character because:', ['They spread from one country to others through trade relations', 'All countries follow the same policies', 'They are caused only by weather', 'Every country has the same population'], 0, 'Contagion travels through trade and finance.', 'c5'),
        Q('m21', 'Business cycles generally originate in:', ['Free-market economies', 'Fully planned economies', 'Barter economies only', 'Closed tribal economies'], 0, 'Market economies with decentralised decisions are prone to cycles.', 'c5'),
        Q('m22', 'According to Hawtrey, the trade cycle is:', ['A purely monetary phenomenon', 'Caused by innovations', 'Caused by waves of optimism and pessimism', 'Caused by sunspots'], 0, 'Unplanned changes in money and credit cause fluctuations.', 'c6'),
        Q('m23', 'The view that business fluctuations result from waves of optimism and pessimism among businessmen is associated with:', ['Pigou', 'Hawtrey', 'Schumpeter', 'Kaldor'], 0, 'Pigou\'s psychological theory.', 'c6'),
        Q('m24', 'Schumpeter explained trade cycles in terms of:', ['Innovations', 'Money supply', 'Weather cycles', 'Population growth'], 0, 'Innovations appearing from time to time drive cycles.', 'c6'),
        Q('m25', 'The cobweb theory, under which present prices influence future production, was put forward (as per the study material) by:', ['Nicholas Kaldor', 'J. M. Keynes', 'R. G. Hawtrey', 'A. C. Pigou'], 0, 'Price fluctuations now lead to output fluctuations later.', 'c6', 'moderate'),
        Q('m26', 'Which is considered the most volatile component of aggregate demand?', ['Investment spending', 'Consumption of necessities', 'Government salaries', 'Net factor income'], 0, 'Investment depends on uncertain profit expectations and interest rates.', 'c6'),
        Q('m27', 'Which of the following is an EXTERNAL cause of business cycles?', ['Technology shocks', 'Fluctuations in investment', 'Money supply changes', 'Psychological factors'], 0, 'External causes: wars, post-war reconstruction, technology shocks, natural factors, population growth.', 'c7'),
        Q('m28', 'A severe drought in an agrarian economy can lead to an industrial recession because:', ['Farmers\' incomes and demand for industrial goods fall while food prices rise', 'Industrial wages rise', 'Exports rise', 'Interest rates rise automatically'], 0, 'Lower farm income and higher food prices reduce spending on industrial goods.', 'c7', 'moderate'),
        Q('m29', 'If population grows faster than the economy, according to the study material:', ['Savings, investment and effective demand fall, slowing the economy', 'Savings rise sharply', 'A boom follows automatically', 'Prices of all goods fall'], 0, 'Lower savings → lower investment → lower income and demand.', 'c7'),
        Q('m30', 'Firms whose sales and profits rise and fall sharply with the pace of economic growth are known as:', ['Cyclical businesses', 'Defensive businesses', 'Monopolies', 'Public utilities'], 0, 'E.g. house-builders, restaurants, fashion retail, tour operators.', 'c8'),
        Q('m31', 'Which business is likely to suffer the sharpest fall in demand during a slump?', ['An overseas tour operator', 'A seller of basic food grains', 'A pharmacy selling essential medicines', 'A low-cost grocery chain'], 0, 'Foreign holidays are postponable luxuries; essentials and value retailers are less affected.', 'c8', 'moderate'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Real GDP of a country (₹ ’000 crore) for seven years is 500, 530, 556, 562, 545, 540, 556. (a) Compute annual growth rates. (b) Identify the peak and the trough. (c) Name the phase in each year and state two features you would expect at the peak.',
         'model': [table(['Year', 'GDP', 'Growth %', 'Phase'], [['1', '500', '—', 'Expansion'], ['2', '530', str(w1g[0]), 'Expansion'], ['3', '556', str(w1g[1]), 'Expansion (slowing)'], ['4', '562', str(w1g[2]), 'Peak'], ['5', '545', str(w1g[3]), 'Contraction'], ['6', '540', str(w1g[4]), 'Trough'], ['7', '556', str(w1g6), 'Recovery']]),
                   p('Peak in Year 4 (GDP 562); trough in Year 6 (GDP 540). Features at the peak: input shortages and rising input prices; rapidly rising output prices and cost of living; stagnating actual demand for houses and durables.')],
         'scheme': [{'id': 's1', 'pt': 'Growth rates computed', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Peak and trough identified', 'm': 1, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Phases labelled', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': 'Two peak features', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Growth must be computed on the previous year\'s value, not the first year\'s.'], 'mistakes': ['Calling the year of slowest positive growth the trough.', 'Using the later year as the base.'], 'tips': ['Peak = highest level; trough = lowest level — look at levels, not just growth rates.'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Classify the following as leading, coincident or lagging indicators, giving a reason for each: stock prices; unemployment rate; retail sales; building permits.',
         'model': [table(['Indicator', 'Type', 'Reason'], [['Stock prices', 'Leading', 'Reflect expected future profits; move before output'], ['Unemployment rate', 'Lagging', 'Hiring and firing follow changes in output'], ['Retail sales', 'Coincident', 'Move with current spending and output'], ['Building permits', 'Leading', 'Permits come before construction activity']])],
         'scheme': [{'id': 's1', 'pt': 'Stock prices — leading with reason', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Unemployment — lagging with reason', 'm': 1, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Retail sales — coincident with reason', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Building permits — leading with reason', 'm': 1, 'skill': 'concept'}],
         'remarks': ['A classification without a reason earns half credit.'], 'mistakes': ['Treating unemployment as a leading indicator.'], 'tips': ['Ask: does it move before, with, or after output?']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Distinguish between internal and external causes of business cycles. Match each of the following theories with its proponent: monetary theory; psychological theory; innovation theory; cobweb theory; effective-demand theory.',
         'model': [p('Internal (endogenous) causes arise within the economic system: fluctuations in effective demand, in investment and in government spending, macroeconomic policies, money supply and psychological factors. External (exogenous) causes come from outside the economic system: wars, post-war reconstruction, technology shocks, natural factors such as droughts and floods, and population growth.'),
                   table(['Theory', 'Proponent'], [['Monetary (trade cycle purely monetary)', 'Hawtrey'], ['Psychological (optimism/pessimism)', 'Pigou'], ['Innovation', 'Schumpeter'], ['Cobweb (present prices drive future output)', 'Nicholas Kaldor (as per the study material)'], ['Fluctuations in effective demand', 'Keynes']])],
         'scheme': [{'id': 's1', 'pt': 'Meaning of internal causes with examples', 'm': 1.5, 'skill': 'concept'}, {'id': 's2', 'pt': 'Meaning of external causes with examples', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Five correct matches (0.4 each)', 'm': 2, 'skill': 'application'}],
         'remarks': ['Examples carry the marks — list at least three of each.'], 'mistakes': ['Placing money supply among external causes.', 'Attributing the psychological theory to Hawtrey.'], 'tips': ['Two-column table: internal vs external.']},
    ]

    viva = [
        V('v1', 'What are business cycles?',
          'Business cycles are the recurring ups and downs in the overall level of economic activity — alternate periods of expansion and contraction in output, income and employment. They are recurrent but not periodic, because they do not occur at regular intervals and differ in length and intensity.',
          [P('p1', 'Fluctuations (expansion and contraction) in aggregate economic activity', 4, 'fluctuat|ups and downs|up and down|rise and fall|expansion and contraction|boom and bust|alternate|swings', 'economic activity|output|income|employment|gdp|aggregate', min=2),
           P('p2', 'Recurrent', 3, 'recurr|repeat|again and again|occur again|keep coming back'),
           P('p3', 'Not periodic — irregular length and intensity', 3, 'not periodic|not regular|irregular|not at regular|not same length|different length|differ in length|vary in length|varying length|not of same length|not fixed|unequal')], 'c1'),
        V('v2', 'Name the four phases of a business cycle and describe each briefly.',
          'The four phases are expansion, peak, contraction and trough. In expansion, output, employment, demand, profits and prices rise. The peak is the highest point, where inputs are scarce, prices rise fast and demand stops growing. In contraction or recession, investment, output, employment and prices fall. The trough is the lowest point, reached after a depression, from which recovery begins.',
          [P('p1', 'Expansion — rising output, employment, demand', 2, 'expansion|boom|upswing', 'rise|rising|increase|grow|higher', min=2),
           P('p2', 'Peak — highest point', 3, 'peak|prosperity|top', 'highest|top|maximum|upper turning|stops growing|stagnat', min=2),
           P('p3', 'Contraction / recession — falling activity', 2, 'contraction|recession|downswing|downturn', 'fall|falling|decline|decrease|drop|lower', min=2),
           P('p4', 'Trough — lowest point; recovery starts', 3, 'trough|depression|bottom', 'lowest|bottom|minimum|recovery|revive|lower turning', min=2)], 'c2'),
        V('v3', 'Explain leading, lagging and coincident indicators with examples.',
          'Leading indicators change before real output changes, so they help forecast turning points — for example stock prices, new orders and building permits. Lagging indicators change after output has changed and confirm a trend — for example the unemployment rate and labour cost per unit of output. Coincident indicators move at the same time as the cycle and show its current state — for example GDP, industrial production and retail sales.',
          [P('p1', 'Leading — change before output (stock prices, new orders, building permits)', 4, 'leading', 'before|ahead|in advance|precede|forecast|predict', 'stock|share price|new order|building permit|consumer confidence|money supply|money growth', min=2),
           P('p2', 'Lagging — change after output (unemployment, unit labour cost)', 3, 'lagging', 'after|later|follow|confirm', 'unemployment|labour cost|consumer price|cpi|lending', min=2),
           P('p3', 'Coincident — move with the cycle (GDP, industrial production)', 3, 'coincident|concurrent', 'same time|simultaneous|along with|current|together|move with', 'gdp|industrial production|retail sales|personal income|output', min=2)], 'c3'),
        V('v4', 'What are the main internal causes of business cycles?',
          'Internal causes arise within the economy. They include fluctuations in effective demand, as Keynes said; fluctuations in investment, which is the most volatile part of demand; variations in government spending; macroeconomic policies such as changes in taxes, spending and interest rates; changes in money supply, which Hawtrey saw as the cause; and psychological factors, the waves of optimism and pessimism stressed by Pigou.',
          [P('p1', 'Effective demand (Keynes)', 2, 'effective demand|aggregate demand|keynes'),
           P('p2', 'Investment fluctuations', 2, 'investment'),
           P('p3', 'Government spending / macroeconomic policies', 2, 'government spending|government expenditure|fiscal|monetary policy|macroeconomic polic|tax|interest rate'),
           P('p4', 'Money supply (Hawtrey)', 2, 'money supply|money and credit|credit|hawtrey|monetary'),
           P('p5', 'Psychological factors — optimism/pessimism (Pigou)', 2, 'psycholog|optimism|pessimism|pigou|confidence|expectation')], 'c6'),
        V('v5', 'What are the external causes of business cycles?',
          'External causes come from outside the economic system. They are wars, which divert resources to weapons and cut other production; post-war reconstruction, which raises demand; technology shocks that require big new investment; natural factors like droughts and floods that hit farm output and incomes; and population growth faster than economic growth, which reduces savings and investment.',
          [P('p1', 'War / post-war reconstruction', 3, 'war|reconstruction'),
           P('p2', 'Technology shocks', 2, 'technolog|innovation|invention'),
           P('p3', 'Natural factors — drought, flood, weather', 3, 'natural|drought|flood|weather|monsoon|rain'),
           P('p4', 'Population growth', 2, 'population')], 'c7'),
        V('v6', 'Why should a business understand the business cycle?',
          'The phase of the cycle affects demand for a firm\'s products and so its profits. Knowing the phase helps managers decide on expansion or down-sizing, how much to produce and how many workers to employ, when to enter a market or launch a new product, and how to plan prices and promotion. Cyclical businesses such as construction, restaurants and tour operators are hit hardest in a slump, so they need this most.',
          [P('p1', 'Cycle affects demand and profits', 3, 'demand|sales', 'profit|revenue|survival|success', min=2),
           P('p2', 'Decisions on expansion/down-sizing, production and labour', 3, 'expansion|expand|down siz|downsiz|production|output|labour|workers|hiring|capacity'),
           P('p3', 'Timing of entry / new product launch; pricing and promotion', 2, 'launch|new product|entry|enter|timing|price|promotion|marketing'),
           P('p4', 'Cyclical businesses hit hardest', 2, 'cyclical|construction|restaurant|tour|house build|real estate|durable|fashion|advertis')], 'c8'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Reading the signals at Prakash Appliances', 'difficulty': 'moderate',
        'case': ('Prakash Appliances makes air-conditioners and refrigerators. Over the last three quarters the national stock index has fallen 18%, new orders from dealers are down, and building permits for new homes have declined. '
                 'Real GDP (₹ lakh crore) for the last three quarters was 9.6, 9.0 and 8.7. Unemployment has only just started to rise. Interest rates are high after a period of tight monetary policy.'),
        'mcqs': [
            M('k1a', 'The percentage change in real GDP from the first to the second quarter is:', ['-6.25%', '-6.67%', '-0.6%', '6.25%'], 0, f'(9.0 − 9.6)/9.6 × 100 = {kg1}%. -6.67% uses 9.0 as the base.', 'moderate', 'round((9.0-9.6)/9.6*100,2)'),
            M('k1b', 'Which of the signals mentioned are leading indicators?', ['Stock index, dealer orders and building permits', 'Real GDP only', 'Unemployment only', 'Real GDP and unemployment'], 0, 'They move before output; GDP is coincident and unemployment lagging.', 'core'),
            M('k1c', 'The economy is most likely in which phase?', ['Contraction', 'Expansion', 'Peak with rising output', 'Recovery'], 0, f'Real GDP is falling ({kg1}% and then {kg2}%), and leading indicators are down.', 'moderate'),
            M('k1d', 'Which cause of the cycle described in the case is an internal (endogenous) cause?', ['Tight monetary policy', 'A drought', 'A war abroad', 'A technology shock'], 0, 'Macroeconomic (monetary) policy is internal; droughts, wars and technology shocks are external.', 'moderate'),
            M('k1e', 'The most sensible policy for Prakash Appliances now is to:', ['Reduce production plans and inventory, and defer non-essential capex', 'Build large inventories for an expected boom', 'Hire aggressively', 'Raise prices sharply'], 0, 'Durable-goods makers are hit hard in contractions; conserving cash and avoiding excess stock is prudent.', 'core'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch06', 'n': 1, 'title': 'Business Cycles',
        'outcomes': ['Explain the meaning of business cycles and describe the phases — expansion, peak, contraction, trough/depression and recovery.', 'Distinguish leading, lagging and coincident indicators and use simple data to identify phases.',
                     'State the features of business cycles and explain their internal and external causes, including the theories of Keynes, Hawtrey, Pigou, Schumpeter and Kaldor.', 'Explain why business cycles matter for business decisions and which businesses are most cyclical.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['fnd-p4-ch05-u02'],
                 'exam_tip': 'Mostly conceptual MCQs: sequence of phases, features of each phase, indicator types with examples, and theory–economist matching (Hawtrey = money, Pigou = psychology, Schumpeter = innovation, Kaldor = cobweb, Keynes = effective demand).'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Business cycles: recurrent but irregular fluctuations in aggregate economic activity around a trend.', 'Phases: expansion → peak → contraction → trough (depression) → recovery.',
                        'Leading (stock prices, new orders, building permits) → forecast; coincident (GDP, industrial production, retail sales) → current state; lagging (unemployment, unit labour cost) → confirm.',
                        'Features: irregular, distinct phases, originate in free markets, pervasive, hit capital and durable goods most, complex, affect all variables, international, harmful to welfare.',
                        'Internal causes: effective demand, investment, government spending, macro policies, money supply, psychology (plus innovations, cobweb).', 'External causes: war, post-war reconstruction, technology shocks, natural factors, population growth.',
                        'Relevance: plan production, labour, capex, entry and launches by phase; cyclical businesses most exposed.'],
            'remember': ['Hawtrey — money; Pigou — psychology; Schumpeter — innovation; Kaldor — cobweb; Keynes — effective demand.', 'Great Depression 1929–33; dot-com burst 1999–2001; global financial crisis 2008–09 (US sub-prime housing).', 'Depression: low interest rates yet weak credit demand.'],
            'traps': ['Recurrent ≠ periodic.', 'Industry is more cycle-prone than agriculture.', 'Unemployment is a lagging, not leading, indicator.', 'Money supply and macro policy are internal causes; technology shocks are external.']},
        'quickref': [{'k': 'Phases', 'v': 'Expansion → Peak → Contraction → Trough/Depression → Recovery'}, {'k': 'Growth rate', 'v': '(This period − previous) ÷ previous × 100'},
                     {'k': 'Leading indicators', 'v': 'Stock prices, new orders, building permits, consumer confidence, money growth'}, {'k': 'Coincident indicators', 'v': 'GDP, industrial production, personal income, retail sales'},
                     {'k': 'Lagging indicators', 'v': 'Unemployment, labour cost per unit of output, CPI, commercial lending'}, {'k': 'Theories', 'v': 'Hawtrey (monetary), Pigou (psychological), Schumpeter (innovation), Kaldor (cobweb), Keynes (effective demand)'}],
        'viva': viva, 'cases': cases,
    }
