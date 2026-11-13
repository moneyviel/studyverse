"""CA Final · Paper 6 · Integrated Business Solutions · Chapter 2 (Case Study Digest Volume-II themes).
Original multidisciplinary case material modelled on the ICAI IBS format; all names, businesses and figures are invented and machine-checked."""
from fkit import *

UID = 'fin-p6-ch02-u01'
T1 = 'Portfolio and value chain analysis'
T2 = 'Strategic cost management'
T3 = 'Acquisitions and risk management'
T4 = 'Governance, reporting and related parties'


def build():
    ck = Checks()
    tc = ck.add('120*(1-0.25)', 'Target cost: target price less 25% margin (₹ per pack)')
    gap = ck.add('98-120*(1-0.25)', 'Cost gap: current cost less target cost (₹ per pack)')
    sav = ck.add('(98-120*(1-0.25))*2500000', 'Annual saving needed on 25 lakh packs (₹)')
    i1 = {'id': 'i1', 'title': 'Target costing for a new snack line', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Hearthstone Foods Ltd. plans a millet snack. Market research fixes the price at ₹120 per pack, and the company wants a 25% margin on price. The current engineered cost is ₹98 per pack and volume is 25 lakh packs a year. Compute the target cost, cost gap and the annual saving needed, and suggest how to close the gap.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Target cost', '₹120 × 75%', f'₹{inr(tc)}'],
              ['Cost gap', '₹98 − target cost', f'₹{inr(gap)}'],
              ['Annual saving needed', 'Gap × 25,00,000 packs', f'₹{inr(sav)}']], title='Target costing'),
              p('Close the gap through value engineering (lighter packaging, fewer SKUs), supplier collaboration on millet sourcing, and process redesign; launch only when the gap is closed or the price strategy changes.')],
          'checks': list(ck)}

    c2 = Checks()
    sw = c2.add('120/400', 'Swap ratio on market prices: target price ÷ acquirer price')
    ns = c2.add('5000000*120/400', 'New Hearthstone shares issued for 50 lakh target shares')
    eps = c2.add('(600000000+90000000)/(20000000+5000000*120/400)', 'Post-merger EPS: combined earnings ÷ total shares (₹)')
    i2 = {'id': 'i2', 'title': 'Share exchange for Rasoi Spices', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Hearthstone (2 crore shares, earnings ₹60 crore, price ₹400) acquires Rasoi Spices (50 lakh shares, earnings ₹9 crore, price ₹120) through a share swap based on market prices. Compute the swap ratio, shares issued and post-merger EPS assuming no synergy. Compare with Hearthstone\'s pre-merger EPS.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Swap ratio', '120 ÷ 400', f'{sw:g} Hearthstone share per Rasoi share'],
              ['Shares issued', '50,00,000 × 0.3', f'{inr(ns)}'],
              ['Post-merger EPS', '(₹60 crore + ₹9 crore) ÷ 2.15 crore shares', f'₹{eps:,.2f}'],
              ['Pre-merger EPS', '₹60 crore ÷ 2 crore', '₹30.00']], title='Merger arithmetic'),
              p('EPS rises from ₹30 to about ₹32.09 even without synergy, because Rasoi is bought at a P/E of 6.67 (₹120 ÷ ₹18 EPS) against Hearthstone\'s own 13.33. EPS accretion alone does not prove value creation; the board should still test strategic fit, synergies and integration risk.')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'The BCG matrix places businesses by market growth and relative market share: stars (high growth, high share), cash cows (low growth, high share), question marks (high growth, low share) and dogs (low growth, low share). Cash from cows funds stars and selected question marks.',
            'Porter\'s value chain splits a firm into primary activities (inbound logistics, operations, outbound logistics, marketing and sales, service) and support activities (infrastructure, HR, technology, procurement). Advantage comes from performing activities at lower cost or in a way that creates differentiation.',
            'Combining the two shows where to invest and which activities to strengthen, outsource or integrate.'],
          'Know where cash comes from and where value is made.',
          'A mature biscuit brand with leading share is a cash cow.'),
        C('c2', T2, [
            'Target costing starts from the market price, deducts the required margin and treats the result as the maximum allowable cost; the gap to current cost is closed through value engineering before launch.',
            'Life-cycle costing tracks costs from design to withdrawal; activity-based costing traces overheads to products by drivers, exposing loss-making SKUs; Kaizen supports continuous small improvements after launch.',
            'Pricing strategies — penetration, skimming, premium — must align with the competitive strategy (cost leadership or differentiation).'],
          'Price first, cost to fit.',
          'A ₹8 per pack gap on 25 lakh packs means ₹2 crore of savings to find.'),
        C('c3', T3, [
            'Acquisitions are tested on strategic fit, valuation and post-merger effects. Swap ratios may use EPS, market price, book value or intrinsic value; paying a higher P/E than the acquirer\'s dilutes EPS unless synergies add earnings.',
            'Due diligence covers financial, tax, legal and operational areas; integration risk often decides success.',
            'Risk management uses forwards, futures, options and swaps to hedge currency, commodity and interest exposures; the hedge decision compares the locked-in cost with the expected unhedged cost and the company\'s risk appetite.'],
          'Deals must create value after integration.',
          'Booking a forward at ₹84.20 for an import payable removes the risk of the rupee weakening.'),
        C('c4', T4, [
            'Section 188 of the Companies Act covers contracts with related parties (sale or purchase of goods, leasing, services, agency, appointment to office). They need board approval, and shareholders\' approval by ordinary resolution where prescribed limits are crossed; interested members cannot vote. Transactions in the ordinary course of business at arm\'s length are outside these approvals.',
            'Ind AS 24 requires disclosure of related party relationships and transactions; Ind AS 115 treats trade discounts, rebates and price concessions as variable consideration, estimated and constrained, reducing revenue.',
            'Auditors assess related party risks (SA 550) and may report significant matters as key audit matters for listed entities (SA 701).'],
          'Related party deals need approvals, disclosure and audit focus.',
          'Buying packaging from a director\'s firm above market price needs scrutiny.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Acquisition screening memo', 'role': 'Corporate strategy analyst',
             'situation': 'The board wants a view on acquiring a regional spice brand.',
             'steps': ['Assess strategic fit and BCG position.', 'Compute swap ratio and EPS effect.', 'List synergies and risks.', 'Note approvals and disclosures.'],
             'takeaway': 'EPS dilution is acceptable only with credible synergies.'}]

    mcqs = [
        Q('m1', 'A business with low market growth and high relative share is a:', ['Cash cow', 'Star', 'Question mark', 'Dog'], 0,
          'BCG. In practice: funds growth.', 'c1', T1),
        Q('m2', 'Procurement in Porter\'s value chain is a:', ['Support activity', 'Primary activity', 'Outbound activity', 'Service activity'], 0,
          'Support. In practice: sourcing.', 'c1', T1),
        Q('m3', 'Target cost equals:', ['Target price minus required margin', 'Current cost plus margin', 'Market price plus margin', 'Standard cost'], 0,
          'Market-driven. In practice: value engineering.', 'c2', T2),
        Q('m4', 'Activity-based costing assigns overheads using:', ['Cost drivers', 'Direct labour hours only', 'Sales value', 'Equal shares'], 0,
          'ABC. In practice: SKU profitability.', 'c2', T2),
        Q('m5', 'Paying a higher P/E for the target than the acquirer\'s own P/E, without synergy, tends to:', ['Dilute acquirer EPS', 'Increase acquirer EPS', 'Leave EPS unchanged', 'Eliminate goodwill'], 0,
          'Merger arithmetic. In practice: synergies needed.', 'c3', T3),
        Q('m6', 'A forward contract for an import payable protects against:', ['Rupee depreciation', 'Rupee appreciation gains', 'Credit risk of supplier', 'Inflation'], 0,
          'Locks the rate. In practice: forgoes upside.', 'c3', T3),
        Q('m7', 'Related party transactions in the ordinary course at arm\'s length under section 188:', ['Need no board or shareholder approval under the section', 'Always need special resolution', 'Need Central Government approval', 'Are prohibited'], 0,
          'Third proviso. In practice: document arm\'s length.', 'c4', T4),
        Q('m8', 'Volume rebates to distributors are treated under Ind AS 115 as:', ['Variable consideration reducing revenue', 'Selling expense', 'Other income', 'Finance cost'], 0,
          'Estimate and constrain. In practice: accrue rebates.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Target cost and gap', 3, 'computation', 'target cost', nums=[tc, gap]), S('s2', 'Annual saving', 1, 'computation', 'saving', nums=[sav]), S('s3', 'Ways to close', 2, 'analysis', 'value engineering')],
          ['Practical suggestions.'], ['Using margin on cost.'], ['Table and advice.'], pad='table', checks=list(ck)),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'Swap ratio', 2, 'computation', 'swap', nums=[sw]), S('s2', 'Shares issued', 2, 'computation', 'shares', nums=[ns]), S('s3', 'EPS and comment', 4, 'analysis', 'synergy', nums=[eps])],
          ['Compare EPS and P/E.'], ['Assuming every share swap dilutes EPS.'], ['Table and comment.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'How should cash cows be managed?', 'Hold position efficiently and use their surplus cash to fund stars and selected question marks.',
          [P('p1', 'Surplus cash', 5, 'surplus cash'), P('p2', 'Stars', 5, 'stars')], 'c1'),
        V('v2', 'What is value engineering?', 'Redesigning a product or process to cut cost while keeping the functions customers value.',
          [P('p1', 'Cut cost', 5, 'cut cost'), P('p2', 'Functions', 5, 'functions')], 'c2'),
        V('v3', 'What does due diligence cover in an acquisition?', 'Financial, tax, legal and operational review of the target to find risks and validate value.',
          [P('p1', 'Legal', 5, 'legal'), P('p2', 'Financial', 5, 'financial')], 'c3'),
        V('v4', 'Can an interested shareholder vote on a related party resolution?', 'A related party member must abstain from voting on that resolution under section 188.',
          [P('p1', 'Abstain', 5, 'abstain'), P('p2', 'Related party', 5, 'related party')], 'c4'),
        V('v5', 'Which standard governs audit of related parties?', 'SA 550 requires the auditor to identify and assess related party risks.',
          [P('p1', 'SA 550', 5, '550'), P('p2', 'Identify', 5, 'identify')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Hearthstone Foods — integrated case', 'difficulty': 'moderate',
              'case': 'Hearthstone Foods Ltd. sells biscuits (market leader, category growth 3%), ready meals (growth 18%, share 4%) and frozen desserts (growth 2%, share 3%). It imports oat flakes worth US$5 lakh payable in 3 months; the 3-month forward rate is ₹84.20 and treasury expects spot of ₹84.80. It buys cartons from Pack Prime LLP, where the managing director\'s brother is a partner, at prices 12% above market.',
              'mcqs': [
                  M('k1a', 'Ready meals in the BCG matrix are a:', ['Question mark', 'Star', 'Cash cow', 'Dog'], 0,
                    'High growth, low share. In practice: invest or exit.', 'moderate', topic=T1),
                  M('k1b', 'Expected saving from booking the forward (₹ lakh):', ['3', '6', '1.5', '0'], 0,
                    '(84.80 − 84.20) × 5 lakh. In practice: hedge.', 'moderate', check=3, topic=T3),
                  M('k1c', 'The carton purchases from Pack Prime are:', ['Related party transactions needing section 188 approvals', 'Exempt as ordinary course at arm\'s length', 'Outside the Act', 'Prohibited'], 0,
                    'Above market, so not arm\'s length. In practice: board approval.', 'moderate', topic=T4),
                  M('k1d', 'Frozen desserts fall in which quadrant?', ['Dog', 'Star', 'Question mark', 'Cash cow'], 0,
                    'Low growth, low share. In practice: harvest or divest.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p6', 'fin-p6-ch02', 1, 'IBS Case Study Digest Volume-II',
                ['Use portfolio and value chain analysis on a case.',
                 'Apply strategic cost management tools.',
                 'Evaluate acquisitions and hedging choices.',
                 'Apply related party, revenue and audit requirements.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 40}, 'prereq': ['fin-p6-ch01-u01'],
                 'exam_tip': 'In merger questions, always comment on EPS effect and synergies, not just the ratio.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['BCG: stars, cash cows, question marks, dogs.', 'Value chain: primary and support activities.', 'Target cost = price − margin.',
                             'Swap ratio and EPS dilution; synergies decide.', 'Section 188 approvals; Ind AS 115 variable consideration; SA 550.'],
                 'remember': ['Arm\'s length ordinary-course deals are outside section 188 approvals.'],
                 'traps': ['Treating above-market supplies from a relative as arm\'s length.']},
                [('Portfolio', 'BCG'), ('Activities', 'Value chain'), ('Cost', 'Target costing'), ('M&A', 'Swap ratio'), ('Governance', 'Section 188')],
                viva, cases)
