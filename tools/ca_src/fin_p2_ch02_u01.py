"""CA Final · Paper 2 Advanced Financial Management · Chapter 2 Risk Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch02-u01'
T1 = 'Types of business risk'
T2 = 'Viewing financial risk from different angles'
T3 = 'Value at Risk'
T4 = 'Identifying and managing specific financial risks'


def build():
    ck = Checks()
    vol = ck.add('500*0.015', 'One standard deviation of daily value (₹ lakh)')
    v1 = ck.add('500*0.015*2.33', '1-day VaR at 99% (₹ lakh)')
    v5 = ck.add('round(500*0.015*2.33*5**0.5,2)', '5-day VaR at 99% (₹ lakh)')
    v95 = ck.add('500*0.015*1.65', '1-day VaR at 95% (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'VaR on an equity position', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A treasury desk holds shares worth ₹500 lakh with a daily return standard deviation of 1.5%. Assuming normal returns, compute 1-day VaR at 99% (z = 2.33) and at 95% (z = 1.65), and 5-day VaR at 99%.',
          'solution': [table(['Measure', 'Working', '₹ lakh'], [
              ['Daily volatility in rupees', '500 × 1.5%', inr(vol)],
              ['1-day VaR, 99%', '7.5 × 2.33', inr(v1)],
              ['1-day VaR, 95%', '7.5 × 1.65', inr(v95)],
              ['5-day VaR, 99%', '17.475 × √5', inr(v5)]], title='VaR = z × σ × value × √t')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Matching risks to remedies', 'difficulty': 'core', 'minutes': 6,
          'q': 'Hira Exports faces: (a) a large customer in a country that has frozen currency remittances; (b) a key distributor showing signs of insolvency; (c) floating-rate borrowings when rates are rising; (d) USD receivables when the rupee may strengthen. Name each risk and one way to manage it.',
          'solution': [table(['Item', 'Risk', 'Management'], [
              ['(a)', 'Political (country) risk', 'Political risk insurance, local partners, limit exposure'],
              ['(b)', 'Counterparty risk', 'Credit limits, guarantees, diversify distributors'],
              ['(c)', 'Interest rate risk', 'Swap to fixed, caps, mix of fixed and floating debt'],
              ['(d)', 'Currency risk', 'Forwards, options, natural hedging via USD costs']], title='Risk identification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Strategic risk arises from wrong business decisions or failure to adapt to change — competition, technology shifts, changing customer needs.',
            'Compliance risk is the risk of breaching laws and regulations; operational risk comes from failed internal processes, people, systems or external events (fraud, system breakdowns, disasters).',
            'Financial risk arises from the way a business is financed and from its exposure to financial markets — including counterparty, political, interest rate and currency risks.'],
          'Businesses face strategic, compliance, operational and financial risks — finance focuses on the last but cannot ignore the others.',
          'A bank failing to upgrade digital services faces strategic risk.'),
        C('c2', T2, [
            'Shareholders see high gearing as risky because debt holders rank ahead of them in winding up; lenders also worry about high existing debt raising default risk.',
            'From the company\'s view, borrowing too much, or lending to parties who default, can push it into insolvency.',
            'From the government\'s view, failures of large banks or institutions, wilful defaults and sovereign debt crises can spread distrust and threaten the whole financial system.'],
          'The same debt looks different to owners, managers and regulators.',
          'A major bank collapse can trigger a wider credit freeze.'),
        C('c3', T3, [
            'Value at Risk (VaR) estimates the maximum loss on a position over a stated time horizon at a given confidence level, under normal market conditions. It answers: how bad can it get, and how much could we lose?',
            'Inputs: time period, confidence level (commonly 95% or 99%), and volatility (standard deviation). VaR = z-score × standard deviation of value; for longer horizons, multiply one-day VaR by the square root of the number of days (assuming independent returns).',
            'Uses: measuring maximum likely loss on portfolios, setting dealer limits, benchmarking trading performance, guiding trading strategy and asset-liability management. Limitations: assumes normal distribution and does not tell the size of losses beyond the VaR level.'],
          'VaR puts one number on downside risk at a chosen confidence level.',
          'A 1-day 99% VaR of ₹17 lakh means losses should exceed that only one day in a hundred.'),
        C('c4', T4, [
            'Counterparty risk — a party fails to perform. Warning signs: failure to obtain resources, regulatory restrictions, insolvency. Management: due diligence, exposure limits, avoid concentration, regular review, guarantees and insurance.',
            'Political risk — host government actions such as currency conversion restrictions, expropriation, price controls or insistence on local ownership. Management: assess country risk rankings and macro conditions, local partners, political risk insurance, structuring investments to reduce exposure.',
            'Interest rate risk — changes in rates affect costs, income and values; managed with matching, swaps, caps, floors and FRAs. Currency risk — exchange rate changes affect cash flows and values; managed with forwards, futures, options, swaps and natural hedging.'],
          'Name the risk first; the toolkit follows.',
          'A forward contract locks the rupee value of export receipts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Treasury risk dashboard', 'role': 'Risk analyst',
             'situation': 'The treasury holds equities, forex exposures and floating loans.',
             'steps': ['Classify exposures by risk type.', 'Compute daily VaR for market positions.', 'Set limits per dealer and portfolio.', 'Recommend hedges for breaches.'],
             'takeaway': 'Measure, limit and hedge — in that order.'}]

    mcqs = [
        Q('m1', 'VaR estimates:', ['Maximum likely loss over a period at a confidence level', 'Average profit', 'Minimum gain', 'Total portfolio value'], 0,
          'Under normal conditions. In practice: one-day or ten-day horizons.', 'c3', T3),
        Q('m2', 'To convert 1-day VaR to 10-day VaR, multiply by:', ['The square root of 10', '10', '1/10', '2.33'], 0,
          'Assumes independent daily returns. In practice: regulatory 10-day measures.', 'c3', T3),
        Q('m3', 'Expropriation of assets by a host government is:', ['Political risk', 'Counterparty risk', 'Interest rate risk', 'Operational risk'], 0,
          'Country-specific action. In practice: political risk insurance.', 'c4', T4),
        Q('m4', 'Failed internal systems causing losses represent:', ['Operational risk', 'Strategic risk', 'Currency risk', 'Political risk'], 0,
          'Process, people, system failures. In practice: controls.', 'c1', T1),
        Q('m5', 'Shareholders view high gearing as risky because:', ['Debt holders rank ahead of them in winding up', 'Debt is cheaper', 'Interest is tax-free', 'Dividends rise'], 0,
          'Residual claimants. In practice: equity beta rises with gearing.', 'c2', T2),
        Q('m6', 'A tool to manage counterparty risk is:', ['Setting exposure limits and taking guarantees', 'Buying more from one supplier', 'Ignoring credit ratings', 'Removing contracts'], 0,
          'Limits and security. In practice: diversify.', 'c4', T4),
        Q('m7', 'A limitation of VaR is that it:', ['Does not show the size of losses beyond the VaR level', 'Is never used', 'Ignores time', 'Has no confidence level'], 0,
          'Tail losses can be much larger. In practice: use stress tests.', 'c3', T3),
        Q('m8', 'An interest rate swap from floating to fixed manages:', ['Interest rate risk', 'Political risk', 'Strategic risk', 'Compliance risk'], 0,
          'Locks the cost of debt. In practice: when rates are expected to rise.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Volatility', 1, 'computation', 'volatility', nums=[vol]), S('s2', '1-day VaR', 2, 'computation', '1-day', nums=[v1, v95]), S('s3', '5-day VaR', 2, 'computation', '5-day', nums=[v5])],
          ['Show z-scores.'], ['Multiplying by 5 instead of √5.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Risk names', 2, 'concept', 'political|counterparty|interest|currency'), S('s2', 'Remedies', 2, 'concept', 'insurance|swap|forward|limit')],
          ['One remedy each.'], ['Confusing political and counterparty risk.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What two questions does VaR answer?', 'What is the worst likely case under normal conditions, and how much could be lost over the period at the chosen confidence level.',
          [P('p1', 'Worst case', 5, 'worst'), P('p2', 'Amount of loss', 5, 'lost|loss')], 'c3'),
        V('v2', 'List the components of a VaR calculation.', 'A time period, a confidence level, and the volatility or loss expressed in amount or percentage.',
          [P('p1', 'Time period', 5, 'time'), P('p2', 'Confidence level', 5, 'confidence')], 'c3'),
        V('v3', 'Name four types of business risk.', 'Strategic, compliance, operational and financial risk.',
          [P('p1', 'Strategic and compliance', 5, 'strategic|compliance'), P('p2', 'Operational and financial', 5, 'operational|financial')], 'c1'),
        V('v4', 'How can political risk be assessed?', 'By looking at published country risk rankings and evaluating the host country\'s macro-economic conditions.',
          [P('p1', 'Country rankings', 5, 'ranking'), P('p2', 'Macro conditions', 5, 'macro')], 'c4'),
        V('v5', 'How does the government view financial risk?', 'As the danger that failures of banks or institutions, wilful defaults or sovereign debt crises spread distrust across the system.',
          [P('p1', 'Institutional failure', 5, 'failure|bank'), P('p2', 'Systemic distrust', 5, 'distrust|system')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Unity Bank treasury', 'difficulty': 'moderate',
              'case': 'Unity Bank holds a bond portfolio of ₹1,000 crore with a daily standard deviation of 0.4%. Its limit for 1-day 99% VaR is ₹10 crore. It also has large loans to one business group and branches in a country that recently imposed capital controls.',
              'mcqs': [
                  M('k1a', '1-day 99% VaR (₹ crore, z = 2.33):', ['9.32', '4', '23.3', '0.93'], 0,
                    '1,000 × 0.4% × 2.33. In practice: compare to limit.', 'core', check=9.32, topic=T3),
                  M('k1b', 'Is the VaR limit breached?', ['No, 9.32 is within 10', 'Yes', 'Cannot tell', 'Only on weekends'], 0,
                    'Within limit. In practice: monitor daily.', 'core', topic=T3),
                  M('k1c', 'Large loans to one business group create:', ['Concentrated counterparty risk', 'Political risk', 'Currency risk only', 'No risk'], 0,
                    'Single-group exposure. In practice: large exposure limits.', 'core', topic=T4),
                  M('k1d', 'Capital controls in the host country are an example of:', ['Political risk', 'Operational risk', 'Interest rate risk', 'Strategic risk'], 0,
                    'Restriction on currency conversion. In practice: country limits.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch02', 1, 'Risk Management',
                ['Identify the types of risk faced by a business.',
                 'Evaluate financial risk from different stakeholders\' viewpoints.',
                 'Compute and interpret Value at Risk.',
                 'Identify and manage counterparty, political, interest rate and currency risks.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 20}, 'prereq': ['fin-p2-ch01-u01'],
                 'exam_tip': 'In VaR sums, state the z-score used and scale by the square root of days.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Risks: strategic, compliance, operational, financial.',
                             'Financial risk viewed by stakeholders, company, government.',
                             'VaR = z × σ × value; × √t for horizon.',
                             'z: 1.65 (95%), 2.33 (99%).',
                             'Counterparty, political, interest, currency: identify and hedge.'],
                 'remember': ['VaR ignores tail size.'],
                 'traps': ['Scaling VaR linearly with days.']},
                [('VaR 99%', 'z = 2.33'), ('VaR 95%', 'z = 1.65'), ('Horizon', '× √t'), ('Political risk', 'Host government action')],
                viva, cases)
