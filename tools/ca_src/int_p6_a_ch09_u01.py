"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 1 Introduction to Working Capital Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u01'
T1 = 'Meaning and kinds of working capital'
T2 = 'Operating (working capital) cycle'
T3 = 'Estimating working capital requirement'
T4 = 'Working capital policies and financing approaches'


def build():
    ck = Checks()
    oc = ck.add('45+15+30+60-40', 'Net operating cycle (days)')
    i1 = {'id': 'i1', 'title': 'How long is money locked up?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Raw materials are held for 45 days, production takes 15 days, finished goods are held 30 days, customers pay in 60 days and suppliers are paid in 40 days. Compute the gross and net operating cycle.',
          'solution': [table(['Component', 'Days'], [
              ['Raw material holding', '45'], ['Work-in-progress', '15'], ['Finished goods', '30'], ['Receivables', '60'],
              ['Gross operating cycle', '150'], ['Less: payables deferral', '(40)'], ['Net operating cycle', inr(oc)]], title='Operating cycle')],
          'checks': list(ck)}

    ck2 = Checks()
    rm = ck2.add('36000*50/12', 'Raw material stock (1 month)')
    wip = ck2.add('36000/12*0.5*(50+25)', 'WIP (½ month; material full, conversion 50%)')
    fg = ck2.add('36000/12*100', 'Finished goods (1 month at cost)')
    dr = ck2.add('36000/12*2*100', 'Debtors (2 months at cost)')
    cr = ck2.add('36000*50/12', 'Creditors (1 month of materials)')
    wg = ck2.add('36000*20/12*0.5', 'Wages outstanding (½ month)')
    nwc = ck2.add('150000+112500+300000+600000+50000-150000-30000', 'Net working capital')
    i2 = {'id': 'i2', 'title': 'Estimating working capital', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Annual production and sales 36,000 units evenly. Cost per unit: materials ₹50, wages ₹20, overheads ₹30; price ₹130. Raw material held 1 month; WIP ½ month (materials 100%, conversion 50%); finished goods 1 month; debtors 2 months (take at cost); cash ₹50,000; creditors 1 month of materials; wages paid ½ month in arrears. Estimate net working capital (overheads paid as incurred).',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Raw materials', '36,000 × 50 ÷ 12', inr(rm)],
              ['WIP', '1,500 units × (50 + 50% of 50)', inr(wip)],
              ['Finished goods', '3,000 units × ₹100', inr(fg)],
              ['Debtors at cost', '6,000 units × ₹100', inr(dr)],
              ['Cash', '', inr(50000)],
              ['Less: creditors', '1 month of materials', '(' + inr(cr) + ')'],
              ['Less: wages outstanding', '½ month of ₹7,20,000', '(' + inr(wg) + ')'],
              ['Net working capital', '', inr(nwc)]], title='Working capital estimate'),
              note('Taking debtors at cost excludes profit, since profit does not need to be financed.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Gross working capital is investment in current assets; net working capital is current assets minus current liabilities. Current assets are expected to be realised within the operating cycle or twelve months.',
            'Permanent (fixed) working capital is the minimum level always needed; temporary (fluctuating) working capital varies with seasons and activity.',
            'Both excess (idle funds, lower return) and shortage (missed opportunities, inability to pay, loss of credit) of working capital are harmful; the goal is a balance of liquidity and profitability.'],
          'Working capital is the oil in the business engine — too little and it seizes, too much and it is wasted.',
          'A woollens maker needs far more working capital before winter than in summer.'),
        C('c2', T2, [
            'Operating cycle = raw material conversion period + WIP conversion period + finished goods conversion period + receivables collection period − payables deferral period.',
            'Each period = average balance ÷ daily relevant figure: raw materials on consumption; WIP and finished goods on cost of production or sales; receivables on credit sales; payables on credit purchases.',
            'Number of cycles a year = 365 (or 360) ÷ operating cycle days; working capital requirement ≈ total operating costs ÷ number of cycles (plus minimum cash).'],
          'The shorter the cycle, the less money stays locked in operations.',
          'Cutting the debtor period from 60 to 45 days shortens the cycle by 15 days.'),
        C('c3', T3, [
            'Estimation methods: percentage of sales, regression, and the operating cycle (component) method used in exams: estimate each current asset and liability from its holding period.',
            'Raw materials at material cost; WIP at material plus a proportion of conversion cost; finished goods at cost of production; debtors at cost (cash cost approach) or at sales value; cash as given; less creditors and outstanding expenses.',
            'A safety margin may be added for contingencies. Depreciation is excluded from cash-cost-based estimates.'],
          'Estimate each piece of money tied up, then subtract what suppliers and others fund for you.',
          'A ₹10 lakh monthly material bill with 1 month of stock needs ₹10 lakh tied in raw materials.'),
        C('c4', T4, [
            'Policies: conservative (high current assets, more liquidity, lower return); aggressive (low current assets, higher return, more risk); moderate in between.',
            'Financing approaches: matching (hedging) — permanent needs from long-term funds, temporary needs from short-term funds; conservative — long-term funds also cover part of temporary needs; aggressive — short-term funds finance part of permanent needs.',
            'Choice depends on business nature, seasonality, credit policy, production cycle, growth and access to finance.'],
          'Match the life of the money to the life of the need.',
          'Financing a permanent stock buffer with a 3-month loan risks refinancing trouble.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Working capital loan proposal', 'role': 'Finance analyst trainee',
             'situation': 'A client applies for a cash credit limit.',
             'steps': ['Estimate the operating cycle.', 'Estimate each current asset and liability.', 'Compute net working capital need.', 'Decide the mix of bank and own funds.'],
             'takeaway': 'Banks finance a part; the margin comes from the owner\'s long-term funds.'}]

    mcqs = [
        Q('m1', 'Net working capital is:', ['Current assets minus current liabilities', 'Total current assets', 'Fixed assets minus long-term debt', 'Cash plus bank'], 0,
          'Net working capital is the excess of current assets over current liabilities. In practice: gross WC is total current assets.', 'c1', T1),
        Q('m2', 'Minimum level of current assets always required is:', ['Permanent working capital', 'Temporary working capital', 'Gross working capital', 'Negative working capital'], 0,
          'Permanent working capital persists at all activity levels. In practice: finance it long-term.', 'c1', T1),
        Q('m3', 'RM 30 days, WIP 10, FG 20, debtors 45, creditors 35. Net operating cycle:', ['70 days', '105 days', '140 days', '35 days'], 0,
          '30 + 10 + 20 + 45 − 35 = 70 days. In practice: monitor each component.', 'c2', T2, check=70),
        Q('m4', 'Receivables collection period is based on:', ['Average receivables ÷ daily credit sales', 'Average stock ÷ daily sales', 'Creditors ÷ daily purchases', 'Cash ÷ daily expenses'], 0,
          'Receivables relate to credit sales. In practice: use credit sales where given.', 'c2', T2),
        Q('m5', 'Under the matching approach, temporary working capital is financed by:', ['Short-term funds', 'Equity only', 'Long-term debt only', 'Retained earnings only'], 0,
          'Short-term needs are matched with short-term finance. In practice: permanent needs use long-term funds.', 'c4', T4),
        Q('m6', 'An aggressive working capital policy means:', ['Low current assets and more short-term financing', 'High current assets', 'All needs from equity', 'No credit sales'], 0,
          'It seeks higher returns with more risk. In practice: suitable only with stable cash flows.', 'c4', T4),
        Q('m7', 'Under the cash cost approach, debtors are valued at:', ['Cost of sales excluding profit (and depreciation)', 'Selling price', 'Material cost', 'Market value'], 0,
          'Only funds actually invested need financing. In practice: state the approach used.', 'c3', T3),
        Q('m8', 'Excess working capital leads to:', ['Idle funds and lower return', 'Inability to pay creditors', 'Stock-outs', 'Loss of credit standing'], 0,
          'Funds tied up beyond need reduce profitability. Shortage causes the other problems. In practice: find the balance.', 'c1', T1),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Gross cycle', 1, 'computation', 'gross', nums=[150]), S('s2', 'Net cycle', 2, 'computation', 'net', nums=[oc])],
          ['List each component.'], ['Adding creditors instead of subtracting.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'Inventories', 3, 'computation', 'materials|WIP|finished', nums=[rm, wip, fg]), S('s2', 'Debtors and cash', 2, 'computation', 'debtors', nums=[dr]),
           S('s3', 'Current liabilities', 2, 'computation', 'creditors|wages', nums=[cr, wg]), S('s4', 'Net WC', 1, 'computation', 'net', nums=[nwc])],
          ['Show units and rates.'], ['Valuing WIP at full cost.'], ['Statement.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Distinguish gross and net working capital.', 'Gross working capital is total current assets; net working capital is current assets less current liabilities.',
          [P('p1', 'Total current assets', 5, 'total current assets'), P('p2', 'Less current liabilities', 5, 'less current liabilities')], 'c1'),
        V('v2', 'What is the operating cycle?', 'The time from investing cash in raw materials until cash is collected from customers, less the credit period from suppliers.',
          [P('p1', 'Cash to cash', 5, 'cash'), P('p2', 'Less payables', 5, 'supplier|payable|credit')], 'c2'),
        V('v3', 'How is WIP valued in a working capital estimate?', 'At full material cost plus the proportion of labour and overhead completed, for the holding period.',
          [P('p1', 'Material full', 5, 'material'), P('p2', 'Partial conversion', 5, 'proportion|conversion|labour')], 'c3'),
        V('v4', 'What is the matching approach?', 'Financing permanent working capital with long-term funds and temporary working capital with short-term funds.',
          [P('p1', 'Permanent long-term', 5, 'permanent'), P('p2', 'Temporary short-term', 5, 'temporary')], 'c4'),
        V('v5', 'Name two factors affecting working capital needs.', 'Nature of business and length of the production cycle, along with seasonality and credit policy.',
          [P('p1', 'Business or cycle', 5, 'business|cycle'), P('p2', 'Season or credit', 5, 'season|credit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Monsoon Umbrellas', 'difficulty': 'moderate',
              'case': 'Monsoon Umbrellas has annual cost of sales ₹73 lakh, average stock of ₹12 lakh, average debtors ₹15 lakh (credit sales ₹91.25 lakh) and average creditors ₹8 lakh (credit purchases ₹48.67 lakh). Use 365 days. Demand peaks from June to September.',
              'mcqs': [
                  M('k1a', 'Inventory holding period:', ['60 days', '45 days', '72 days', '30 days'], 0,
                    '12 ÷ (73 ÷ 365) = 12 ÷ 0.2 = 60 days. In practice: seasonal peaks raise this before monsoon.', 'moderate', check=60, topic=T2),
                  M('k1b', 'Receivables period:', ['60 days', '75 days', '45 days', '90 days'], 0,
                    '15 ÷ (91.25 ÷ 365) = 15 ÷ 0.25 = 60 days. In practice: tighten credit after season.', 'moderate', check=60, topic=T2),
                  M('k1c', 'Payables period (approx.):', ['60 days', '30 days', '90 days', '45 days'], 0,
                    '8 ÷ (48.67 ÷ 365) ≈ 60 days. In practice: negotiate seasonal credit.', 'moderate', check=60, topic=T2),
                  M('k1d', 'Pre-season stock build-up is best financed by:', ['Short-term borrowing', 'Long-term debt', 'Equity', 'Sale of fixed assets'], 0,
                    'It is temporary working capital, matched with short-term funds. In practice: repay after the season.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 1, 'Introduction to Working Capital Management',
                ['Explain kinds of working capital and the cost of excess or shortage.',
                 'Compute the operating cycle.',
                 'Estimate working capital requirements.',
                 'Compare working capital policies and financing approaches.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 50}, 'prereq': ['int-p6-a-ch08-u01'],
                 'exam_tip': 'In estimation questions, write the valuation basis of each item (material, cost, sales) before computing.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Gross WC = CA; net WC = CA − CL; permanent vs temporary.',
                             'Operating cycle = RM + WIP + FG + debtors − creditors periods.',
                             'Estimate each current asset and liability; debtors at cost under cash cost approach.',
                             'Policies: conservative, moderate, aggressive; matching approach for financing.'],
                 'remember': ['Depreciation excluded under cash cost approach.'],
                 'traps': ['WIP is not valued at full cost.']},
                [('Operating cycle', 'R + W + F + D − C'), ('Net WC', 'CA − CL'), ('Matching', 'Permanent → long-term')],
                viva, cases)
