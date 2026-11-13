"""CA Final · Paper 2 Advanced Financial Management · Chapter 11 International Financial Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch11-u01'
T1 = 'International capital budgeting'
T2 = 'International sources of finance'
T3 = 'International financial centres, GIFT City and sovereign funds'
T4 = 'International working capital management'


def build():
    ck = Checks()
    usd = ck.add('round(400/1.1+500/1.1**2+600/1.1**3-1000,2)', 'Project NPV (USD thousand)')
    inr_npv = ck.add('round((400/1.1+500/1.1**2+600/1.1**3-1000)*84,2)', 'Project NPV in rupees (₹ thousand)')
    s1 = ck.add('round(84*1.06/1.02,2)', 'Expected spot rate in year 1 by PPP (₹)')
    i1 = {'id': 'i1', 'title': 'Evaluating a US project', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'An Indian company considers a US project costing USD 1,000 thousand now, generating USD 400, 500 and 600 thousand in years 1–3. The USD required return is 10%. Spot is ₹84/USD; Indian inflation 6% and US inflation 2%. Compute the NPV in USD and in rupees (home-currency equivalent at spot), and the expected year-1 spot rate.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['PV of inflows', '400/1.1 + 500/1.21 + 600/1.331', '1,227.65'],
              ['NPV in USD', '1,227.65 − 1,000', inr(usd) + ' thousand'],
              ['NPV in rupees', '227.65 × 84', '₹' + inr(inr_npv) + ' thousand'],
              ['Year-1 spot by PPP', '84 × 1.06 ÷ 1.02', '₹' + inr(s1)]], title='Foreign currency approach')],
          'checks': list(ck)}

    ck2 = Checks()
    gross = ck2.add('50+30+40', 'Gross intra-group payments (USD thousand)')
    net = ck2.add('abs(-50+40)+abs(50-30)+abs(30-40)', 'Sum of absolute net positions (USD thousand)')
    flows = ck2.add('(abs(-50+40)+abs(50-30)+abs(30-40))/2', 'Payments needed after netting (USD thousand)')
    i2 = {'id': 'i2', 'title': 'Multilateral netting', 'difficulty': 'core', 'minutes': 6,
          'q': 'Within a group, A owes B USD 50 thousand, B owes C USD 30 thousand and C owes A USD 40 thousand. Show the net positions and the payments needed after netting.',
          'solution': [table(['Entity', 'Working', 'Net (USD thousand)'], [
              ['A', '−50 + 40', '−10 (pays)'], ['B', '+50 − 30', '+20 (receives)'], ['C', '+30 − 40', '−10 (pays)'],
              ['Gross payments before netting', '50 + 30 + 40', inr(gross)],
              ['Payments after netting', 'A and C pay 10 each to B', inr(flows)]], title='Netting centre')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Foreign projects are more complex: cash flows differ between the project and the parent (remittance restrictions, taxes, transfer prices, royalties and fees), exchange rates fluctuate, inflation rates differ, political and country risks exist, and subsidised financing may be available.',
            'Approaches: (1) discount foreign currency flows at a foreign-currency rate, then convert the NPV at spot; or (2) convert flows at forecast exchange rates (via PPP or IRP) and discount at the home rate — the results agree if parity holds. The parent\'s perspective (remittable cash flows) decides the investment.',
            'Adjusted present value suits foreign projects: base NPV plus PV of financing side effects such as subsidised loans and tax shields. Scenarios include a foreign firm investing in India, and an Indian firm investing abroad with funds raised in the same or a different country.'],
          'Value what the parent can actually bring home.',
          'A project with blocked profits is worth less to the parent than to the subsidiary.'),
        C('c2', T2, [
            'Foreign currency convertible bonds (FCCBs) are bonds issued abroad in foreign currency, convertible into equity of the issuer; low coupons but currency and redemption risk if not converted.',
            'Depository receipts: ADRs are issued in the US and traded on US exchanges; GDRs are issued in multiple markets, often listed in Luxembourg or London. A depository bank abroad issues receipts against shares held by a custodian in India.',
            'Other sources: external commercial borrowings, euro-convertible bonds, euro bonds and foreign bonds (e.g. Yankee, Samurai, masala bonds — rupee-denominated bonds issued abroad), syndicated loans and export credit.'],
          'Global markets offer cheaper or larger funds — with currency and regulatory strings.',
          'A masala bond lets an Indian company borrow abroad without taking currency risk.'),
        C('c3', T3, [
            'An international financial centre (IFC) serves non-residents and residents in foreign currency transactions — banking, capital markets, insurance, asset management — with competitive regulation and tax.',
            'GIFT City in Gujarat houses India\'s International Financial Services Centre, regulated by the IFSCA, offering tax benefits, international exchanges, banking units and fund management, aiming to bring offshore financial business onshore.',
            'Sovereign wealth funds are state-owned investment funds (from commodity revenues, trade surpluses or reserves) that invest globally in equities, bonds, infrastructure and private assets; they provide long-term capital but raise governance and strategic concerns.'],
          'IFCs and sovereign funds shape global capital flows.',
          'An Indian firm can list bonds on an exchange in GIFT IFSC.'),
        C('c4', T4, [
            'Multinational cash management aims to minimise idle cash, currency and tax costs: accelerating inflows, managing blocked funds (via royalties, fees, transfer pricing, parallel loans), leading and lagging, netting of intra-group payments, and centralised investment of surplus cash.',
            'Transfer pricing can shift profits to lower-tax jurisdictions, but is constrained by arm\'s-length rules and tax authorities.',
            'International inventory management weighs stockpiling against currency changes and supply disruptions; receivables management covers credit terms, currency of invoicing, factoring and forfaiting.'],
          'Centralise, net and time payments to save cost.',
          'Netting cut three payments totalling 120 to two payments totalling 20.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Overseas expansion appraisal', 'role': 'International finance analyst',
             'situation': 'The company plans a plant in Vietnam funded by a subsidised loan.',
             'steps': ['Forecast project and remittable cash flows.', 'Forecast exchange rates using parity.', 'Compute APV including loan subsidy.', 'Add political risk adjustments and funding options.'],
             'takeaway': 'Parent perspective plus APV gives a fair picture of foreign projects.'}]

    mcqs = [
        Q('m1', 'Foreign projects should be evaluated from the viewpoint of:', ['The parent\'s remittable cash flows', 'The host government only', 'Local banks', 'Customers'], 0,
          'Only cash reaching the parent creates value for its shareholders. In practice: consider restrictions.', 'c1', T1),
        Q('m2', 'ADRs are issued and traded in:', ['The United States', 'India', 'Luxembourg only', 'Japan only'], 0,
          'US depository receipts. In practice: GDRs elsewhere.', 'c2', T2),
        Q('m3', 'Masala bonds are:', ['Rupee-denominated bonds issued abroad', 'Dollar bonds in India', 'Gold bonds', 'Equity shares'], 0,
          'Currency risk with investors. In practice: London listings.', 'c2', T2),
        Q('m4', 'GIFT City IFSC is regulated by:', ['IFSCA', 'SEBI only', 'RBI only', 'IRDAI only'], 0,
          'Unified regulator. In practice: offshore business onshore.', 'c3', T3),
        Q('m5', 'Multilateral netting reduces:', ['Number and value of intra-group payments', 'Sales', 'Taxes always', 'Inventory'], 0,
          'Lower transfer costs. In practice: netting centre.', 'c4', T4),
        Q('m6', 'Blocked funds can be partly released through:', ['Royalties, fees and transfer pricing', 'Higher dividends only', 'Ignoring rules', 'Selling shares'], 0,
          'Alternative channels. In practice: within law.', 'c4', T4),
        Q('m7', 'FCCBs are:', ['Foreign currency bonds convertible into equity', 'Domestic rupee bonds', 'Preference shares', 'Commercial paper'], 0,
          'Low coupons. In practice: redemption risk if not converted.', 'c2', T2),
        Q('m8', 'Sovereign wealth funds are:', ['State-owned investment funds', 'Private hedge funds', 'Mutual funds', 'Pension funds of companies'], 0,
          'Long-term global investors. In practice: governance concerns.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'USD NPV', 2.5, 'computation', 'usd|npv', nums=[usd]), S('s2', 'Rupee NPV', 2, 'computation', 'rupee', nums=[inr_npv]), S('s3', 'PPP', 1.5, 'computation', 'ppp|spot', nums=[s1])],
          ['State approach.'], ['Discounting USD flows at the INR rate.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Net positions', 2, 'computation', 'net', nums=[gross]), S('s2', 'Payments', 2, 'computation', 'after netting', nums=[flows])],
          ['Show each entity.'], ['Paying gross.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Why may project and parent cash flows differ?', 'Because of remittance restrictions, taxes, transfer pricing, royalties and fees, and exchange rate effects.',
          [P('p1', 'Remittance and tax', 5, 'remittance|tax'), P('p2', 'Exchange rates', 5, 'exchange')], 'c1'),
        V('v2', 'Distinguish ADRs and GDRs.', 'ADRs are issued and traded in the US; GDRs are issued in several markets and usually listed in Europe.',
          [P('p1', 'US', 5, 'us'), P('p2', 'Several markets', 5, 'several|europe')], 'c2'),
        V('v3', 'What is GIFT City IFSC?', 'India\'s international financial services centre in Gujarat, regulated by IFSCA, for offshore financial business.',
          [P('p1', 'IFSC in Gujarat', 5, 'gujarat|ifsc'), P('p2', 'IFSCA', 5, 'ifsca')], 'c3'),
        V('v4', 'What is multilateral netting?', 'Offsetting intra-group receivables and payables so that only net amounts are transferred.',
          [P('p1', 'Offsetting', 5, 'offset'), P('p2', 'Net amounts', 5, 'net amount')], 'c4'),
        V('v5', 'How can APV help foreign projects?', 'It values the base project separately and adds financing benefits such as subsidised loans and tax shields.',
          [P('p1', 'Base project', 5, 'base'), P('p2', 'Financing benefits', 5, 'subsid|tax shield')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Indus Pharma Global', 'difficulty': 'moderate',
              'case': 'Indus Pharma\'s German subsidiary can remit only 50% of profits each year; the rest is blocked. Profits are EUR 10 million a year. Spot is ₹90/EUR. Indus is considering a GDR issue in Luxembourg and an FCCB with a 1% coupon.',
              'mcqs': [
                  M('k1a', 'Annual remittable profit (EUR million):', ['5', '10', '2.5', 'Nil'], 0,
                    '50% of 10. In practice: parent cash flow.', 'core', check=5, topic=T1),
                  M('k1b', 'Rupee value of remittance at spot (₹ crore):', ['45', '90', '22.5', '9'], 0,
                    '5 million × 90 = ₹45 crore. In practice: forecast future rates.', 'core', check=45, topic=T1),
                  M('k1c', 'A GDR issue gives Indus:', ['Equity funding from foreign investors', 'A loan', 'A rupee bond', 'Commercial paper'], 0,
                    'Receipts represent shares. In practice: listed abroad.', 'core', topic=T2),
                  M('k1d', 'A key risk of the FCCB is:', ['Repaying principal in foreign currency if not converted', 'High coupon', 'No conversion option', 'Domestic listing only'], 0,
                    'Currency and redemption risk. In practice: falling share prices deter conversion.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch11', 1, 'International Financial Management',
                ['Evaluate foreign projects from the parent\'s perspective.',
                 'Describe international sources of finance.',
                 'Explain IFCs, GIFT City and sovereign funds.',
                 'Apply international working capital techniques.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': ['fin-p2-ch10-u01'],
                 'exam_tip': 'Discount foreign flows at a foreign rate or home flows at a home rate — never mix.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Parent perspective; remittable flows.',
                             'Two consistent NPV approaches; APV for subsidies.',
                             'FCCB, ADR, GDR, ECB, masala bonds.',
                             'GIFT IFSC regulated by IFSCA.',
                             'Netting, leading/lagging, transfer pricing.'],
                 'remember': ['Blocked funds reduce value to parent.'],
                 'traps': ['Mixing currencies and discount rates.']},
                [('ADR', 'US'), ('GDR', 'Global/Europe'), ('Masala bond', 'Rupee bond abroad'), ('Netting', 'Pay net only')],
                viva, cases)
