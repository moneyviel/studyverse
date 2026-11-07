"""CA Foundation · Paper 4 Business Economics · Chapter 6 Business Cycles (single unit).
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch06-u01'


def Q(i, q, o, a, e, c, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if topic: m['topic'] = topic
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
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
        Q('m1', 'Business cycles refer to:', ['Alternate expansion and contraction of overall economic activity', 'Seasonal changes in farm output only', 'Long-term growth of the economy', 'Changes in the price of one commodity'], 0, "A business cycle is the alternating rise and fall of aggregate economic activity — national output, income and employment taken together. The trap is 'long-term growth': that is the smooth trend line, and the cycle is the wave around it. Seasonal farm swings or one commodity's price are too narrow. In practice: when GDP growth slows for several quarters, bank credit officers and CAs ask whether a client's falling sales reflect the economy-wide cycle or a company-specific problem.", 'c1', topic='Introduction'),
        Q('m2', 'Business cycles are:', ['Recurrent but not periodic', 'Periodic and of equal length', 'Non-recurrent', 'Confined to one sector'], 0, "Cycles are recurrent because booms and slumps keep coming back, but they are not periodic: there is no fixed interval, and each cycle differs in length and depth. The tempting trap is 'periodic and of equal length' — that would make turning points easy to forecast, which they are not. In practice: no Indian economist can say exactly when the next slowdown will hit, so treasury teams plan with scenarios rather than a fixed timetable.", 'c1', topic='Introduction'),
        Q('m3', 'The correct sequence of phases of a business cycle is:', ['Expansion → Peak → Contraction → Trough', 'Peak → Expansion → Trough → Contraction', 'Trough → Peak → Expansion → Contraction', 'Contraction → Expansion → Trough → Peak'], 0, "Activity first expands, reaches a peak, contracts, and bottoms out at a trough, after which recovery begins and a fresh expansion follows. Sequences starting with the peak or trough and jumping to the wrong next phase break this logic — for example, a contraction cannot be followed directly by a peak. In practice: fund managers and FP&A teams label each quarter's data by phase so that budgets for hiring, inventory and capex match where the economy is heading.", 'c2', topic='Phases of Business Cycle'),
        Q('m4', 'During the expansion phase, unemployment is mainly:', ['Frictional or structural', 'Involuntary and widespread', 'Cyclical and rising', 'Disguised in industry'], 0, "In expansion, output and hiring rise until resources are close to fully employed, so involuntary unemployment almost disappears; only frictional (people between jobs) and structural (skill or location mismatch) unemployment remain. 'Cyclical and rising' unemployment is the trap — that belongs to contraction, not expansion. In practice: during boom years, Indian IT and manufacturing firms report attrition and hiring difficulty rather than idle workers, which is why wage costs climb.", 'c2', 'moderate', topic='Phases of Business Cycle'),
        Q('m5', 'Shortage of inputs, rapidly rising input and output prices, and stagnating actual demand are typical of the:', ['Peak', 'Trough', 'Depression', 'Recovery'], 0, "At the peak, the economy is at the top of the wave: inputs are scarce and costly, output prices and living costs climb fast, and actual demand stops growing even though capacity is stretched. 'Recovery' is tempting because prices also rise then, but in recovery they rise gradually from a low base with spare capacity. In practice: when steel and cement prices spike while dealer offtake flattens, analysts at Indian brokerages warn that the cycle may be topping out.", 'c2', topic='Phases of Business Cycle'),
        Q('m6', 'During contraction, the initial mismatch between demand and supply arises because:', ['Producers keep producing at old levels without recognising the fall in demand', 'Government stops all spending', 'Supply falls faster than demand', 'Prices rise sharply'], 0, "As the downswing starts, demand begins falling in some sectors, but producers do not notice at once and continue producing at earlier levels, so supply runs ahead of demand and stocks pile up. Only then do firms cancel orders and investment. 'Supply falls faster than demand' reverses the actual mismatch. In practice: an auditor seeing finished-goods inventory days jump at an automobile company checks whether production has outrun a slowing market.", 'c2', 'moderate', topic='Phases of Business Cycle'),
        Q('m7', 'A typical feature of depression is:', ['Low interest rates but falling demand for credit', 'Rising interest rates and booming credit', 'Full employment', 'Rising prices of capital goods'], 0, "In depression, interest rates fall, yet borrowing does not pick up, because businesses have lost confidence and do not want to invest; banks may also be cautious. 'Rising interest rates and booming credit' describes an overheated boom, the opposite situation. In practice: even when RBI cuts the repo rate in a slump, Indian banks often report weak non-food credit growth because companies postpone capex until demand returns.", 'c2', 'moderate', topic='Phases of Business Cycle'),
        Q('m8', 'The lowest point of a business cycle is called the:', ['Trough', 'Peak', 'Boom', 'Plateau'], 0, "The trough is the bottom of the cycle — the point where activity stops falling and the turn towards recovery begins, marking the end of pessimism. The trap is 'peak', which is the opposite turning point at the top; 'boom' is a phase, not a point, and 'plateau' is not a cycle term. In practice: equity analysts try to spot the trough early because share prices of cyclical companies usually rise before the economy visibly recovers.", 'c2', topic='Phases of Business Cycle'),
        Q('m9', 'Recovery from a trough is first felt in the:', ['Labour market, as workers accept lower wages', 'Stock market only', 'Government budget', 'Foreign exchange market'], 0, 'Per the study material, the turnaround first shows in the labour market: widespread unemployment makes workers accept wages below earlier rates, producers expect lower costs, confidence revives and investment restarts. The stock market is the tempting trap — it often moves early, but the material identifies labour as where reversal is first felt. In practice: HR heads and CAs in industry notice easier hiring at lower pay just before management approves expansion plans.', 'c2', 'moderate', topic='Phases of Business Cycle'),
        Q('m10', 'Which of the following is a leading indicator?', ['New orders for plant and equipment', 'Unemployment rate', 'Labour cost per unit of output', 'Industrial production'], 0, 'New orders for plant and equipment are placed before factories actually produce and install machines, so they move ahead of real output and help forecast turning points. Industrial production is the tempting trap: it is coincident because it is current output itself. Unemployment and unit labour cost are lagging. In practice: analysts tracking capital-goods companies such as L&T watch order inflows each quarter as an early signal of the investment cycle.', 'c3', topic='Phases of Business Cycle'),
        Q('m11', 'Which of the following is a lagging indicator?', ['Unemployment rate', 'Building permits', 'Stock prices', 'Consumer confidence index'], 0, 'Firms hire or lay off workers only after they see output change, so the unemployment rate moves after the cycle turns and confirms the trend. Building permits, stock prices and consumer confidence are the traps — all three move ahead of output and are leading indicators. In practice: when PLFS data show unemployment rising, the slowdown has usually already been visible in orders and sales for some months.', 'c3', topic='Phases of Business Cycle'),
        Q('m12', 'GDP and industrial production are examples of:', ['Coincident indicators', 'Leading indicators', 'Lagging indicators', 'Structural indicators'], 0, "GDP and industrial production measure output itself, so they move at the same time as the cycle and describe its current state — coincident (concurrent) indicators. Calling them leading is the trap: they cannot forecast the cycle because they are the cycle. In practice: India's quarterly GDP release and the monthly Index of Industrial Production are read by economists to confirm which phase the economy is in right now.", 'c3', topic='Phases of Business Cycle'),
        Q('m13', 'Indicators that confirm a trend after it has already occurred are:', ['Lagging indicators', 'Leading indicators', 'Coincident indicators', 'Diffusion indicators'], 0, 'Lagging indicators change only after output has already changed, so they confirm a trend rather than predict it — unemployment and the consumer price index are examples. Leading indicators are the trap: they signal before the change. Coincident indicators move together with the cycle. In practice: a CA preparing a board note might use leading data to flag a likely slowdown and lagging data later to confirm it for impairment assumptions.', 'c3', topic='Phases of Business Cycle'),
        Q('m14', 'Real GDP rose from ₹250 lakh crore to ₹262 lakh crore in a year. The growth rate is:', ['4.8%', '12%', '4.58%', '5.2%'], 0, "Growth rate = (new − old) ÷ old × 100 = (262 − 250) ÷ 250 × 100 = 12 ÷ 250 × 100 = 4.8%. The tempting 4.58% comes from dividing by the later value, 262; 12% mistakes the absolute rise (₹12 lakh crore) for a percentage. In practice: when the NSO announces real GDP growth, it is computed exactly this way on the previous year's real GDP, and analysts recompute it to check press figures.", 'c1', 'core', '(262-250)/250*100', topic='Introduction'),
        Q('m15', 'A real GDP index falls from 125 at the peak to 110 at the trough. The percentage decline is:', ['12%', '15%', '13.64%', '8.8%'], 0, 'Percentage decline = (peak − trough) ÷ peak × 100 = (125 − 110) ÷ 125 × 100 = 15 ÷ 125 × 100 = 12%. The tempting 13.64% uses the trough (110) as the base; 15% confuses the 15-point fall with a percentage. Always divide by the starting value. In practice: economists measuring the depth of the 2020 Covid contraction expressed the fall relative to the pre-crisis peak level of output.', 'c2', 'moderate', '(125-110)/125*100', topic='Phases of Business Cycle'),
        Q('m16', 'According to Keynes, the Great Depression was caused mainly by:', ['A fall in aggregate expenditure', 'A banking crisis and low money supply', 'Rapid population growth', 'War'], 0, "Keynes explained the Great Depression as a collapse in aggregate expenditure (effective demand): spending fell, so output, income and jobs fell. The tempting trap is 'banking crisis and low money supply' — that is the monetarist explanation, not Keynes's. In practice: Indian fiscal stimulus packages during slowdowns, such as higher public capex, rest on the Keynesian idea that boosting demand lifts output and employment.", 'c4', topic='Phases of Business Cycle'),
        Q('m17', 'The dot-com bubble burst during:', ['1999–2001', '1929–33', '2007–09', '1973–75'], 0, 'The dot-com (IT) bubble inflated in the late 1990s on cheap capital and over-optimism about internet firms, and burst over 1999–2001, when many companies closed or were acquired. 1929–33 is the Great Depression and 2007–09 is the global financial crisis — tempting because they are also famous crashes. In practice: valuation analysts still cite the dot-com bust when cautioning against pricing loss-making start-ups purely on growth.', 'c4', topic='Phases of Business Cycle'),
        Q('m18', 'The global financial crisis of 2008–09 originated in:', ['The US housing and financial markets (sub-prime lending)', 'Indian stock markets', 'European agriculture', 'Oil-exporting countries'], 0, 'The 2008–09 crisis began in the US: cheap credit and sub-prime housing loans fuelled a property bubble that burst in 2007, and bank losses spread worldwide. Indian stock markets are a tempting distractor because they fell sharply too, but they were affected by, not the source of, the crisis. In practice: the crisis is why Indian auditors and banks now scrutinise loan quality and expected-credit-loss provisions much more closely.', 'c4', topic='Phases of Business Cycle'),
        Q('m19', 'Which sectors are disproportionately affected by business cycles?', ['Capital goods and durable consumer goods', 'Agriculture', 'Essential food items', 'Public administration'], 0, 'Capital goods and durable consumer goods are hit hardest because their purchase can be postponed: in a slump firms delay machinery and households delay cars or refrigerators, so demand swings sharply. Agriculture is the tempting trap — it is less prone to cyclical swings than industry, and food demand is steady. In practice: in Indian slowdowns, auto and capital-goods sales fall far more than FMCG staples, which analysts reflect in sector forecasts.', 'c5', topic='Features of Business Cycles'),
        Q('m20', 'Business cycles are international in character because:', ['They spread from one country to others through trade relations', 'All countries follow the same policies', 'They are caused only by weather', 'Every country has the same population'], 0, "Cycles are contagious across borders: a fall in income in one country reduces its imports, cutting exports, output and jobs in its trading partners, and financial links spread shocks further. 'All countries follow the same policies' is wrong — policies differ widely, yet cycles still spread. In practice: a US or European slowdown quickly hits Indian IT services and textile exporters, so CAs in those firms watch global indicators closely.", 'c5', topic='Features of Business Cycles'),
        Q('m21', 'Business cycles generally originate in:', ['Free-market economies', 'Fully planned economies', 'Barter economies only', 'Closed tribal economies'], 0, 'Business cycles mainly arise in free-market (capitalist) economies, where millions of decentralised spending, saving and investment decisions can fall out of step and cause booms and slumps. Fully planned economies are the tempting trap: central planning suppresses market-driven swings, although it creates other problems. In practice: as India liberalised after 1991, its economy became more exposed to market-driven and global cycles.', 'c5', topic='Features of Business Cycles'),
        Q('m22', 'According to Hawtrey, the trade cycle is:', ['A purely monetary phenomenon', 'Caused by innovations', 'Caused by waves of optimism and pessimism', 'Caused by sunspots'], 0, "Hawtrey held that the trade cycle is purely a monetary phenomenon: unplanned expansion of money and credit pushes up demand and activity, and contraction of money and credit triggers a downturn. Innovations (Schumpeter) and optimism–pessimism waves (Pigou) are the traps — other economists' theories. In practice: RBI watches money and credit growth because excessive credit expansion can overheat the economy and a sharp squeeze can slow it.", 'c6', topic='Causes of Business Cycles'),
        Q('m23', 'The view that business fluctuations result from waves of optimism and pessimism among businessmen is associated with:', ['Pigou', 'Hawtrey', 'Schumpeter', 'Kaldor'], 0, "Pigou's psychological theory says business cycles are driven by waves of optimism and pessimism among businessmen: optimism leads to over-investment and a boom, while pessimism leads to cut-backs and a slump. Hawtrey is the tempting trap, but his theory is monetary. In practice: business-confidence surveys such as RBI's Industrial Outlook Survey are watched because mood shifts often precede changes in investment.", 'c6', topic='Causes of Business Cycles'),
        Q('m24', 'Schumpeter explained trade cycles in terms of:', ['Innovations', 'Money supply', 'Weather cycles', 'Population growth'], 0, 'Schumpeter linked cycles to innovations that appear from time to time — new products, methods or markets trigger bursts of investment and expansion, followed by slowdown once the innovation is absorbed. Money supply is the trap (that is Hawtrey). In practice: the mobile-telecom and digital-payments waves in India drove large investment cycles, the kind of innovation-led boom Schumpeter described.', 'c6', topic='Causes of Business Cycles'),
        Q('m25', 'The cobweb theory, under which present prices influence future production, was put forward (as per the study material) by:', ['Nicholas Kaldor', 'J. M. Keynes', 'R. G. Hawtrey', 'A. C. Pigou'], 0, "The study material credits Nicholas Kaldor with the cobweb theory: today's prices decide how much producers plan to supply next period, so price swings now become output and employment swings later. Keynes is tempting as the best-known name, but his theory is about effective demand. In practice: Indian onion and tomato farmers plant more after a price spike, the next harvest gluts the market, and prices crash — a classic cobweb pattern.", 'c6', 'moderate', topic='Causes of Business Cycles'),
        Q('m26', 'Which is considered the most volatile component of aggregate demand?', ['Investment spending', 'Consumption of necessities', 'Government salaries', 'Net factor income'], 0, "Investment is the most volatile part of aggregate demand because it depends on uncertain profit expectations, interest rates and new technology, so it can surge or collapse quickly. Consumption of necessities is the trap — it is steady because people must eat and pay rent in any phase. In practice: India's quarterly GDP data typically show gross fixed capital formation swinging far more than private consumption across the cycle.", 'c6', topic='Causes of Business Cycles'),
        Q('m27', 'Which of the following is an EXTERNAL cause of business cycles?', ['Technology shocks', 'Fluctuations in investment', 'Money supply changes', 'Psychological factors'], 0, 'External (exogenous) causes come from outside the economic system — wars, post-war reconstruction, technology shocks, natural factors and population growth. A technology shock fits this list. Fluctuations in investment, money supply and psychological factors are tempting because they sound like shocks, but they arise within the economy and are internal causes. In practice: the arrival of smartphones and cheap data was a technology shock that drove a telecom investment boom in India.', 'c7', topic='Causes of Business Cycles'),
        Q('m28', 'A severe drought in an agrarian economy can lead to an industrial recession because:', ['Farmers\' incomes and demand for industrial goods fall while food prices rise', 'Industrial wages rise', 'Exports rise', 'Interest rates rise automatically'], 0, "A drought cuts farm output and farmers' incomes, so rural demand for industrial goods falls; it also raises food prices, leaving all households less to spend on manufactured goods — industry then slows. 'Industrial wages rise' is the trap: nothing in a drought pushes industrial wages up. In practice: when the IMD forecasts a weak monsoon, two-wheeler, tractor and FMCG companies cut rural sales targets and analysts downgrade them.", 'c7', 'moderate', topic='Causes of Business Cycles'),
        Q('m29', 'If population grows faster than the economy, according to the study material:', ['Savings, investment and effective demand fall, slowing the economy', 'Savings rise sharply', 'A boom follows automatically', 'Prices of all goods fall'], 0, "Per the study material, if population grows faster than the economy, savings fall; lower savings mean lower investment, and that reduces income, employment and effective demand, slowing activity. 'Savings rise sharply' reverses the mechanism — more mouths to feed on the same income cut saving. In practice: policy discussions on India's demographic dividend stress that population growth helps only if jobs and output grow faster.", 'c7', topic='Causes of Business Cycles'),
        Q('m30', 'Firms whose sales and profits rise and fall sharply with the pace of economic growth are known as:', ['Cyclical businesses', 'Defensive businesses', 'Monopolies', 'Public utilities'], 0, "Cyclical businesses are those whose sales and profits rise steeply in expansions and fall sharply in slumps — house-building, restaurants, fashion retail, advertising and tour operators. 'Defensive businesses' is the trap: defensives, like food staples and utilities, keep steady sales whatever the phase. In practice: equity analysts and lenders assign higher risk to cyclical borrowers and demand stronger cash buffers in their loan covenants.", 'c8', topic='Relevance of Business Cycles in Business Decision Making'),
        Q('m31', 'Which business is likely to suffer the sharpest fall in demand during a slump?', ['An overseas tour operator', 'A seller of basic food grains', 'A pharmacy selling essential medicines', 'A low-cost grocery chain'], 0, 'Overseas holidays are postponable, income-sensitive luxuries, so a tour operator sees demand collapse when incomes and confidence fall. Food grains, essential medicines and low-cost groceries are necessities or value options, so their demand holds up — some value retailers even gain in slumps. In practice: during downturns, Indian travel companies cut capacity and costs quickly, while discount grocery chains often report rising footfall.', 'c8', 'moderate', topic='Relevance of Business Cycles in Business Decision Making'),
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
            M('k1a', 'The percentage change in real GDP from the first to the second quarter is:', ['-6.25%', '-6.67%', '-0.6%', '6.25%'], 0, 'Percentage change = (9.0 − 9.6) ÷ 9.6 × 100 = −0.6 ÷ 9.6 × 100 = −6.25%. The tempting −6.67% divides by the later figure, 9.0; −0.6% confuses the absolute fall in ₹ lakh crore with a percentage; +6.25% gets the direction wrong. In practice: an FP&A analyst at an appliance maker would compute quarter-on-quarter GDP changes like this before revising sales forecasts for dealers.', 'moderate', 'round((9.0-9.6)/9.6*100,2)', topic='Introduction'),
            M('k1b', 'Which of the signals mentioned are leading indicators?', ['Stock index, dealer orders and building permits', 'Real GDP only', 'Unemployment only', 'Real GDP and unemployment'], 0, "The stock index, dealer orders and building permits all change before real output does, so they are leading indicators that warn of a downturn. Real GDP is the trap: it is coincident, describing the current state. Unemployment, which has only just started to rise, is lagging. In practice: Prakash Appliances' finance team should act on these early warnings instead of waiting for official GDP data to confirm the slowdown.", 'core', topic='Phases of Business Cycle'),
            M('k1c', 'The economy is most likely in which phase?', ['Contraction', 'Expansion', 'Peak with rising output', 'Recovery'], 0, "Real GDP fell from 9.6 to 9.0 (−6.25%) and then to 8.7 (−3.33%), while leading indicators are down and unemployment is starting to rise — the signs of contraction. 'Recovery' is tempting since the second fall is smaller, but output is still falling, not rising. In practice: a consumer-durables CFO reading these signals would plan for weaker demand over the next few quarters.", 'moderate', topic='Phases of Business Cycle'),
            M('k1d', 'Which cause of the cycle described in the case is an internal (endogenous) cause?', ['Tight monetary policy', 'A drought', 'A war abroad', 'A technology shock'], 0, 'Macroeconomic policy, including tight monetary policy with high interest rates, is an internal (endogenous) cause because it arises within the economic system. Droughts, wars abroad and technology shocks are external causes that come from outside the economic system. In practice: when RBI raises the repo rate to fight inflation, durable-goods sales on EMI slow, so appliance makers feel the policy-driven slowdown directly.', 'moderate', topic='Causes of Business Cycles'),
            M('k1e', 'The most sensible policy for Prakash Appliances now is to:', ['Reduce production plans and inventory, and defer non-essential capex', 'Build large inventories for an expected boom', 'Hire aggressively', 'Raise prices sharply'], 0, "In a contraction, durable-goods demand falls sharply, so the prudent course is to cut production plans and inventory and defer non-essential capex to conserve cash. 'Build large inventories for an expected boom' is the trap — nothing in the case signals a boom, and excess stock locks up working capital. In practice: CAs in FP&A at durable-goods firms tighten working-capital limits and stagger capex when leading indicators turn down.", 'core', topic='Relevance of Business Cycles in Business Decision Making'),
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

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        'extra_ok': True,
        's1': _N(6, 4.91, 1.08, -3.02, -0.92, 2.96),
        's2': _K('peak 4|year 4 peak|peak year 4|4 peak|peak 562|562 peak|peak in year 4', 'trough 6|year 6 trough|trough year 6|6 trough|trough 540|540 trough|trough in year 6'),
        's3': _K('expansion|boom', 'contraction|recession|downturn|depression', 'recovery|revival'),
        's4': _K('shortage', 'input price|cost|price ris|price rise|inflation|cost of living|rising price', 'stagnat|full employment|capacity|output price|demand', min=2),
    },
    'q2': {
        's1': _K('stock price leading|stock leading|leading stock|stock market leading|share price leading|stock prices are leading', 'future|expect|anticipat|before|ahead|advance|early'),
        's2': _K('unemployment lagging|lagging unemployment|unemployment rate lagging|unemployment is lagging', 'follow|after|later|delay|behind|respond'),
        's3': _K('retail sales coincident|retail coincident|coincident retail|sales coincident|retail sales are coincident', 'current|same time|simultaneous|along|together|move with|concurrent'),
        's4': _K('building permit leading|permits leading|leading building|permit leading|building leading|permits are leading', 'before|precede|prior|ahead|future|construction|advance'),
    },
    'q3': {
        's1': _K('internal|endogenous', 'within|inside', 'effective demand|investment|government spending|money supply|psycholog|polic'),
        's2': _K('external|exogenous', 'outside', 'war|technolog|natural|drought|flood|population'),
        's3': _K('monetary hawtrey|hawtrey monetary', 'psycholog pigou|pigou psycholog|optimism pessimism pigou|pessimism pigou', 'innovation schumpeter|schumpeter innovation', 'kaldor', 'effective demand keynes|keynes effective|demand keynes|keynes demand', min=4),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
