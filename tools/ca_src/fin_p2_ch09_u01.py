"""CA Final · Paper 2 Advanced Financial Management · Chapter 9 Derivatives Analysis and Valuation.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch09-u01'
T1 = 'Forwards and futures: features and pricing'
T2 = 'Options: types and pay-offs'
T3 = 'Option valuation: binomial, risk-neutral and Black-Scholes'
T4 = 'Greeks and exotic options'
T5 = 'Credit, commodity and real options'


def build():
    ck = Checks()
    fut = ck.add('round(220*2.718281828459045**(0.08*3/12),2)', 'Fair futures price (₹)')
    p = ck.add('(1.05-0.9)/(1.2-0.9)', 'Risk-neutral probability of up move')
    call = ck.add('round((1.05-0.9)/(1.2-0.9)*15/1.05,2)', 'One-period call value (₹)')
    put = ck.add('round((1.05-0.9)/(1.2-0.9)*15/1.05-100+105/1.05,2)', 'Put value by parity (₹)')
    i1 = {'id': 'i1', 'title': 'Futures and a one-step binomial', 'difficulty': 'moderate', 'minutes': 10,
          'q': '(a) A share trades at ₹220; the continuously compounded risk-free rate is 8% a year; no dividends. Price a 3-month future. (b) Another share is at ₹100 and can go to ₹120 or ₹90 in one period; the risk-free rate per period is 5%. Value a European call with strike ₹105 and the matching put.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Futures price', '220 × e^(0.08 × 0.25)', '₹' + inr(fut)],
              ['Risk-neutral p', '(1.05 − 0.90) ÷ (1.20 − 0.90)', inr(p)],
              ['Call pay-offs', 'Up: 15; down: 0', '—'],
              ['Call value', '0.5 × 15 ÷ 1.05', '₹' + inr(call)],
              ['Put by parity', 'C − S + K ÷ 1.05 = 7.14 − 100 + 100', '₹' + inr(put)]], title='Cost of carry and binomial')],
          'checks': list(ck)}

    ck2 = Checks()
    bs = ck2.add('round(100*0.7257-100*2.718281828459045**(-0.1)*0.6554,2)', 'Black-Scholes call value (₹)')
    i2 = {'id': 'i2', 'title': 'Black-Scholes call', 'difficulty': 'hard', 'minutes': 10,
          'q': 'S = ₹100, K = ₹100, time 1 year, continuously compounded risk-free rate 10%, volatility 20%. Given d₁ = 0.60 and d₂ = 0.40, N(0.60) = 0.7257 and N(0.40) = 0.6554, compute the call value. Show how d₁ is derived.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['d₁', '[ln(100/100) + (0.10 + 0.02) × 1] ÷ (0.20 × 1)', '0.60'],
              ['d₂', 'd₁ − 0.20', '0.40'],
              ['PV of strike', '100 × e^(−0.10)', '90.48'],
              ['Call value', '100 × 0.7257 − 90.48 × 0.6554', '₹' + inr(bs)]], title='C = S·N(d₁) − K·e^(−rt)·N(d₂)')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A derivative\'s value comes from an underlying asset. Forwards are private, customised agreements to buy or sell later at a fixed price, with counterparty risk and settlement at maturity. Futures are standardised, exchange-traded, cleared through a clearing house, margined and marked to market daily.',
            'Cost-of-carry pricing: F = S × e^(rt) with continuous compounding (or S(1 + r)^t discretely); deduct the present value of dividends or add storage costs as relevant. If the market futures price is above fair value, sell futures and buy spot (cash-and-carry arbitrage); if below, the reverse.',
            'Index futures let investors hedge or take market views cheaply; hedging a portfolio needs number of contracts = portfolio value × beta ÷ value of one futures contract.'],
          'Futures price = spot carried forward at the financing cost.',
          'A ₹220 share with 8% carry for 3 months has a futures price near ₹224.44.'),
        C('c2', T2, [
            'An option gives the buyer the right, not obligation, to buy (call) or sell (put) at a strike price; the writer receives a premium and bears the obligation. European options exercise only at expiry; American options at any time up to expiry.',
            'Pay-offs at expiry: long call = max(S − K, 0) − premium; short call is the mirror; long put = max(K − S, 0) − premium; short put is the mirror. Options can be in, at or out of the money.',
            'Compared with futures, options limit the buyer\'s loss to the premium while keeping upside, at the cost of paying that premium.'],
          'Buyers pay for rights; writers are paid to take obligations.',
          'A call with strike ₹105 is worthless at expiry if the share ends at ₹90.'),
        C('c3', T3, [
            'Binomial model: the share moves up or down each period; build a riskless hedge or use risk-neutral probability p = (1 + r − d) ÷ (u − d), value = expected pay-off under p discounted at the risk-free rate. Multi-period trees work backwards.',
            'Black-Scholes (European, non-dividend): C = S·N(d₁) − K·e^(−rt)·N(d₂), with d₁ = [ln(S/K) + (r + σ²/2)t] ÷ (σ√t) and d₂ = d₁ − σ√t. Assumptions: lognormal prices, constant volatility and rate, no transaction costs, continuous trading.',
            'Put-call parity: C + K·e^(−rt) = P + S (or with discrete discounting). Deviations create arbitrage.'],
          'Value options as if investors were risk-neutral, then discount at the risk-free rate.',
          'With equal up and down probabilities, the call worth ₹15 in the up state is worth ₹7.14 today.'),
        C('c4', T4, [
            'Factors raising call value: higher share price, lower strike, longer time, higher volatility, higher interest rates, lower dividends (puts mostly reverse).',
            'Greeks: delta (change in option price per ₹1 change in share price; hedge ratio), gamma (change in delta), theta (time decay), rho (sensitivity to interest rate) and vega (sensitivity to volatility).',
            'Exotic options have non-standard features: Asian (average price), barrier (knock-in/out), binary (fixed payout), lookback (best price over life), basket and compound options.'],
          'Greeks tell traders how options react to each driver.',
          'A delta of 0.6 means the call gains about 60 paise when the share rises ₹1.'),
        C('c5', T5, [
            'Credit derivatives transfer credit risk: credit default swaps (protection buyer pays a spread; seller pays on a credit event, settled physically or in cash) and collateralised debt obligations (pools of debt sliced into tranches — risky when underlying quality is poor).',
            'Commodity derivatives hedge prices of metals, energy and agricultural goods; weather and electricity derivatives hedge volume and price risks linked to temperature, rainfall or power demand. Past derivative mishaps show the dangers of leverage, poor controls and model risk.',
            'Real options are flexibility in real projects — options to expand, abandon, delay or switch — valued with option models; they can make a project worth more than its static NPV.'],
          'Derivatives can move credit, commodity and even project flexibility risk.',
          'An option to abandon a mine if prices crash has real value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Hedging a portfolio with derivatives', 'role': 'Derivatives dealer',
             'situation': 'A fund worries about a market fall over the next month.',
             'steps': ['Compute futures contracts needed using beta.', 'Compare with buying index puts.', 'Check fair value and arbitrage gaps.', 'Monitor Greeks and margins daily.'],
             'takeaway': 'Futures lock in, options insure.'}]

    mcqs = [
        Q('m1', 'Futures differ from forwards in being:', ['Standardised and exchange-traded with daily margining', 'Customised', 'Settled only at maturity', 'Free of margins'], 0,
          'Clearing house reduces counterparty risk. In practice: mark to market.', 'c1', T1),
        Q('m2', 'Under cost of carry with continuous compounding, F equals:', ['S × e^(rt)', 'S ÷ e^(rt)', 'S × r', 'S − rt'], 0,
          'Financing cost added. In practice: deduct dividends.', 'c1', T1),
        Q('m3', 'The maximum loss to a call buyer is:', ['The premium paid', 'Unlimited', 'Strike price', 'Nil'], 0,
          'Right, not obligation. In practice: writer faces large loss.', 'c2', T2),
        Q('m4', 'Risk-neutral probability of an up move equals:', ['(1 + r − d) ÷ (u − d)', '(u − d) ÷ (1 + r)', 'r ÷ u', '0.5 always'], 0,
          'Binomial model. In practice: discount at risk-free.', 'c3', T3),
        Q('m5', 'Put-call parity states:', ['C + PV(K) = P + S', 'C = P', 'C − P = K', 'C + S = P + K'], 0,
          'Arbitrage relation. In practice: European options.', 'c3', T3),
        Q('m6', 'Theta measures:', ['Time decay of an option', 'Sensitivity to volatility', 'Change in delta', 'Interest sensitivity'], 0,
          'Options lose value with time. In practice: writers benefit.', 'c4', T4),
        Q('m7', 'Higher volatility generally makes a call option:', ['More valuable', 'Less valuable', 'Unchanged', 'Worthless'], 0,
          'Greater upside chance. In practice: vega positive.', 'c4', T4),
        Q('m8', 'A credit default swap protection seller:', ['Receives a spread and pays on a credit event', 'Pays a spread', 'Owns the bond', 'Issues the bond'], 0,
          'Insurance-like. In practice: settlement physical or cash.', 'c5', T5),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Futures', 2, 'computation', 'futures', nums=[fut]), S('s2', 'Probability', 2, 'computation', 'risk-neutral|probability', nums=[p]), S('s3', 'Call', 2, 'computation', 'call', nums=[call]), S('s4', 'Put', 2, 'computation', 'put|parity', nums=[put])],
          ['Use discrete rate for binomial.'], ['Discounting at expected return.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'd₁ and d₂', 2, 'concept', 'd1|d₁|ln'), S('s2', 'PV of strike', 2, 'computation', 'pv|strike', nums=[]), S('s3', 'Call', 2, 'computation', 'call', nums=[bs])],
          ['Show formula.'], ['Not discounting strike.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is marking to market?', 'Daily settlement of gains and losses on futures positions through the margin account based on closing prices.',
          [P('p1', 'Daily settlement', 5, 'daily'), P('p2', 'Margin account', 5, 'margin')], 'c1'),
        V('v2', 'Distinguish European and American options.', 'European options can be exercised only at expiry; American options at any time up to expiry.',
          [P('p1', 'Only at expiry', 5, 'only at expiry'), P('p2', 'Any time', 5, 'any time')], 'c2'),
        V('v3', 'State the Black-Scholes call formula.', 'Call value equals share price times N of d1 minus the discounted strike times N of d2.',
          [P('p1', 'N of d1', 5, 'd1'), P('p2', 'Discounted strike', 5, 'discounted strike')], 'c3'),
        V('v4', 'What is delta?', 'The change in option value for a one-unit change in the underlying price, used as the hedge ratio.',
          [P('p1', 'Change per unit', 5, 'change'), P('p2', 'Hedge ratio', 5, 'hedge')], 'c4'),
        V('v5', 'Give three types of real options.', 'Options to expand, to abandon and to delay or wait.',
          [P('p1', 'Expand and abandon', 5, 'expand|abandon'), P('p2', 'Delay', 5, 'delay|wait')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Nova Capital desk', 'difficulty': 'moderate',
              'case': 'Nova Capital holds a ₹10 crore equity portfolio with beta 1.2. Nifty futures trade at 25,000 with a lot size of 75. It also writes a call with strike ₹500 on a share now at ₹480, receiving ₹15 premium. At expiry the share is ₹530.',
              'mcqs': [
                  M('k1a', 'Value of one Nifty futures contract (₹ lakh):', ['18.75', '25', '1.875', '7.5'], 0,
                    '25,000 × 75 = ₹18.75 lakh. In practice: lot size changes over time.', 'core', check=18.75, topic=T1),
                  M('k1b', 'Contracts to sell to hedge fully (nearest whole):', ['64', '53', '75', '40'], 0,
                    '10 crore × 1.2 ÷ 18.75 lakh = 64. In practice: beta-adjusted hedge.', 'moderate', check=64, topic=T1),
                  M('k1c', 'Net result for the call writer per share (₹):', ['-15', '15', '-30', '0'], 0,
                    'Pays 30 (530 − 500), keeps 15 premium. In practice: unlimited upside risk.', 'moderate', check=-15, topic=T2),
                  M('k1d', 'The call writer\'s break-even share price (₹):', ['515', '500', '485', '530'], 0,
                    'Strike + premium. In practice: above it, losses.', 'core', check=515, topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch09', 1, 'Derivatives Analysis and Valuation',
                ['Price forwards and futures and use them to hedge.',
                 'Analyse option types and pay-offs.',
                 'Value options using binomial, risk-neutral and Black-Scholes methods.',
                 'Interpret Greeks and exotic options.',
                 'Explain credit, commodity and real options.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fin-p2-ch08-u01'],
                 'exam_tip': 'Always state whether rates are continuous or discrete before pricing.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['F = S·e^(rt) less PV dividends.',
                             'Hedge contracts = value × β ÷ contract value.',
                             'Binomial: p = (1 + r − d) ÷ (u − d).',
                             'Black-Scholes: C = S·N(d₁) − K·e^(−rt)·N(d₂).',
                             'Greeks: delta, gamma, theta, rho, vega.'],
                 'remember': ['Put-call parity links calls and puts.'],
                 'traps': ['Discounting option pay-offs at the expected return.']},
                [('Futures', 'S·e^(rt)'), ('Binomial p', '(1+r−d)/(u−d)'), ('Parity', 'C + PV(K) = P + S'), ('Delta', 'Hedge ratio')],
                viva, cases)
