"""CA Final · Paper 1 Financial Reporting · Chapter 4 Unit 3 Ind AS 113 Fair Value Measurement.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch04-u03'
T1 = 'Definition of fair value and market participants'
T2 = 'Principal and most advantageous market; costs'
T3 = 'Non-financial assets: highest and best use'
T4 = 'Valuation techniques and the fair value hierarchy'


def build():
    ck = Checks()
    na = ck.add('48-4-3', 'Net amount receivable in Market A')
    nb = ck.add('46-1-3', 'Net amount receivable in Market B')
    fvb = ck.add('46-3', 'Fair value if B is the most advantageous market')
    fva = ck.add('48-3', 'Fair value if A is the principal market')
    i1 = {'id': 'i1', 'title': 'Which market sets the price?', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A commodity can be sold in Market A at ₹48 (transaction cost ₹4, transport cost ₹3) or Market B at ₹46 (transaction cost ₹1, transport cost ₹3). (a) There is no principal market. (b) Market A is the principal market. Determine fair value in each case.',
          'solution': [table(['Step', 'Market A ₹', 'Market B ₹'], [
              ['Price', '48', '46'],
              ['Less transaction cost', '(4)', '(1)'],
              ['Less transport cost', '(3)', '(3)'],
              ['Net amount received', inr(na), inr(nb)]], title='Identifying the most advantageous market'),
              table(['Case', 'Fair value', 'Reason'], [
                  ['(a) No principal market', '₹' + inr(fvb), 'B gives the higher net amount; fair value is B\'s price less transport only'],
                  ['(b) A is the principal market', '₹' + inr(fva), 'Principal market price less transport; transaction costs are not deducted']], title='Fair value')],
          'checks': list(ck)}

    ck2 = Checks()
    alt = ck2.add('90-12', 'Value as residential land net of conversion costs (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Land used as a factory', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'An entity acquires land in a business combination; it is used as a factory site worth ₹60 crore in that use. Nearby land has been rezoned for housing and the plot could be sold for residential development for ₹90 crore after demolition and rezoning costs of ₹12 crore. Development is physically possible, legally permissible and financially feasible. What is the fair value?',
          'solution': [table(['Use', 'Value ₹ crore'], [
              ['Current use (factory)', inr(60)],
              ['Residential use, net of conversion costs', inr(alt)]], title='Highest and best use'),
              p('Fair value is ₹' + inr(alt) + ' crore — the highest and best use from a market participant\'s view — even though the entity intends to keep running the factory.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Fair value means the amount that market participants would pay you for an asset, or that you would pay them to take over a liability, in a normal (orderly) deal on the measurement date — an exit price, market-based rather than entity-specific.',
            'The measurement reflects characteristics of the asset or liability (condition, location, restrictions that would transfer to a buyer) and the unit of account set by other standards. An orderly transaction assumes usual marketing activities, not a forced sale.',
            'Market participants are independent, knowledgeable, able and willing buyers and sellers; fair value uses the assumptions they would use in pricing, assuming they act in their economic best interest.',
            'Ind AS 113 explains how to measure fair value when another standard requires or permits it; it does not decide when fair value is used. Some measurements (e.g. share-based payments, leases, value in use, net realisable value) are outside its scope.'],
          'Fair value asks what the market would pay to buy it from you today — not what it is worth to you.',
          'A restriction on selling shares that would pass to a buyer reduces fair value; one personal to the holder does not.'),
        C('c2', T2, [
            'Fair value is measured assuming the transaction takes place in the principal market (where the asset trades most often and in the largest quantities) or, in its absence, the most advantageous market (maximising the amount received after transaction and transport costs).',
            'The price in that market is not adjusted for transaction costs (they belong to the transaction, not the asset), but is adjusted for transport costs if location is a characteristic of the asset.',
            'Transaction costs are used only to identify the most advantageous market. The entity must have access to the market at the measurement date, though it need not be able to sell on that date.'],
          'Choose the market first, then use its price less only the cost of getting the asset there.',
          'Fresh produce valued at the city wholesale market price less transport from the farm.'),
        C('c3', T3, [
            'For non-financial assets, fair value looks at how a market participant could earn the most from the asset — either through its own highest and best use or through a sale to a buyer who would use it that way.',
            'Highest and best use must be physically possible, legally permissible and financially feasible. It is determined from market participants\' perspective, even if the entity intends a different use; current use is presumed highest and best unless market factors suggest otherwise.',
            'The valuation premise may be stand-alone or in combination with other assets and liabilities.'],
          'Value a non-financial asset as the market would best use it, not as the owner happens to use it.',
          'A building used as a warehouse in a prime retail zone may be valued as shop space.'),
        C('c4', T4, [
            'Valuation techniques: market approach (prices and information from market transactions in identical or comparable items), cost approach (current replacement cost adjusted for obsolescence), and income approach (discounting future cash flows or earnings, e.g. present value or option pricing). Techniques maximise relevant observable inputs and minimise unobservable inputs.',
            'Fair value hierarchy: Level 1 — quoted prices in active markets for identical items at the measurement date; Level 2 — inputs other than Level 1 that are observable directly or indirectly (quoted prices for similar items, interest rates, yield curves); Level 3 — unobservable inputs based on the best available information, including the entity\'s own data adjusted to market participants\' assumptions. The level is set by the lowest level input significant to the whole measurement.',
            'Liabilities and own equity instruments are measured assuming transfer to a market participant, reflecting non-performance risk (including own credit). When fair value at initial recognition differs from transaction price, the difference is recognised in profit or loss only if supported by Level 1 or Level 2 evidence; otherwise it is deferred. Disclosures are more extensive for Level 3 measurements.'],
          'The more a value relies on observable market data, the higher its place in the hierarchy.',
          'An unlisted equity valued on a discounted cash flow model with internal forecasts is Level 3.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Review of a valuation report', 'role': 'Audit senior',
             'situation': 'A client measures investment property and unlisted shares at fair value using an external valuer.',
             'steps': ['Check the market and highest-and-best-use assumptions.', 'Identify the valuation technique and inputs.', 'Assign hierarchy levels based on significant inputs.', 'Check Level 3 sensitivity disclosures.'],
             'takeaway': 'Fair value audits focus on inputs and their observability, not just the final number.'}]

    mcqs = [
        Q('m1', 'Fair value under Ind AS 113 is:', ['An exit price', 'An entry price', 'Value in use', 'Historical cost'], 0,
          'It is the price received to sell or paid to transfer. In practice: entity-specific values are excluded.', 'c1', T1),
        Q('m2', 'When measuring fair value, transaction costs are:', ['Not deducted from the price, but used to identify the most advantageous market', 'Always deducted', 'Added to the price', 'Ignored completely'], 0,
          'They are characteristics of the transaction, not the asset. In practice: transport costs are deducted if location matters.', 'c2', T2),
        Q('m3', 'The principal market is the market with:', ['The largest trading volume and activity for that asset', 'The highest price', 'The lowest transaction cost', 'The entity\'s home location'], 0,
          'If a principal market exists, it is used even if another offers a better price. In practice: presumed to be the usual market.', 'c2', T2),
        Q('m4', 'Highest and best use must be:', ['Physically possible, legally permissible and financially feasible', 'The entity\'s current use', 'The use giving the highest accounting profit', 'Approved by management'], 0,
          'All three tests apply from a market participant\'s view. In practice: current use is presumed unless evidence suggests otherwise.', 'c3', T3),
        Q('m5', 'Quoted prices for similar assets in active markets are:', ['Level 2 inputs', 'Level 1 inputs', 'Level 3 inputs', 'Not inputs'], 0,
          'Level 1 needs identical items; similar items are Level 2. In practice: adjustments may move it to Level 3.', 'c4', T4),
        Q('m6', 'A measurement\'s hierarchy level is determined by:', ['The lowest level input significant to the entire measurement', 'The highest level input used', 'Management\'s choice', 'The valuer\'s qualification'], 0,
          'One significant unobservable input makes the measurement Level 3. In practice: assess significance carefully.', 'c4', T4),
        Q('m7', 'The cost approach measures:', ['The current replacement cost adjusted for obsolescence', 'Discounted future cash flows', 'Recent transaction prices', 'Historical cost less depreciation'], 0,
          'It reflects what it would cost to replace the service capacity. In practice: used for specialised assets.', 'c4', T4),
        Q('m8', 'Fair value of a liability reflects:', ['Non-performance risk, including the entity\'s own credit risk', 'Only the contractual amount', 'Only the risk-free rate', 'The amount the entity intends to pay'], 0,
          'Liabilities are measured as if transferred to a market participant. In practice: own credit affects value.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Net amounts', 2, 'computation', 'net', nums=[na, nb]), S('s2', 'Most advantageous case', 2, 'computation', 'advantageous', nums=[fvb]), S('s3', 'Principal market case', 2, 'computation', 'principal', nums=[fva])],
          ['Separate market choice from measurement.'], ['Deducting transaction costs from fair value.'], ['Two tables.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Three tests', 2, 'concept', 'physically|legally|financially'), S('s2', 'Fair value', 2, 'computation', 'highest', nums=[alt])],
          ['Use the market participant view.'], ['Using management\'s intended use.'], ['Table and paragraph.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Why is fair value called a market-based measure?', 'Because it uses the assumptions market participants would use in pricing, not the entity\'s own intentions or value in use.',
          [P('p1', 'Market participants', 6, 'participant'), P('p2', 'Not entity-specific', 4, 'own|intention|value in use')], 'c1'),
        V('v2', 'How are transport costs treated?', 'If location is a characteristic of the asset, the price in the principal or most advantageous market is adjusted for the cost of transporting it there.',
          [P('p1', 'Location', 5, 'location'), P('p2', 'Price adjusted', 5, 'adjust')], 'c2'),
        V('v3', 'What is highest and best use?', 'The use of a non-financial asset by market participants that maximises its value, being physically possible, legally permissible and financially feasible.',
          [P('p1', 'Maximises value', 5, 'maximis'), P('p2', 'Three tests', 5, 'legally|physically|financially')], 'c3'),
        V('v4', 'Name the three valuation approaches.', 'The market approach, the cost approach and the income approach.',
          [P('p1', 'Market and cost', 5, 'market|cost'), P('p2', 'Income', 5, 'income')], 'c4'),
        V('v5', 'What are Level 3 inputs?', 'Unobservable inputs reflecting the best available information, including the entity\'s own data adjusted to what market participants would assume.',
          [P('p1', 'Unobservable', 6, 'unobservable'), P('p2', 'Own data adjusted', 4, 'own data|adjusted')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Horizon Investments Ltd.', 'difficulty': 'moderate',
              'case': 'Horizon Investments Ltd. holds: (i) shares of a company listed on NSE, actively traded; (ii) corporate bonds valued using yields of similar bonds; (iii) shares of an unlisted start-up valued by a DCF model using management\'s forecasts; (iv) a building used as its office in an area where hotels pay much higher prices for similar buildings.',
              'mcqs': [
                  M('k1a', 'Item (i) is measured using:', ['Level 1 inputs', 'Level 2 inputs', 'Level 3 inputs', 'Cost'], 0,
                    'Quoted price for identical shares in an active market. In practice: price × quantity, no blockage discount.', 'core', topic=T4),
                  M('k1b', 'Item (ii) is:', ['Level 2', 'Level 1', 'Level 3', 'Outside Ind AS 113'], 0,
                    'Observable yields on similar instruments are Level 2 inputs. In practice: check comparability.', 'core', topic=T4),
                  M('k1c', 'Item (iii) is:', ['Level 3', 'Level 2', 'Level 1', 'Not a fair value'], 0,
                    'Management forecasts are unobservable inputs significant to the value. In practice: extensive disclosures.', 'core', topic=T4),
                  M('k1d', 'Item (iv) should be valued considering:', ['Highest and best use, possibly as a hotel if feasible', 'Only its office use', 'Its historical cost', 'Management\'s intention only'], 0,
                    'Market participant view decides the use if physically, legally and financially feasible. In practice: disclose if use differs.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch04', 3, 'Ind AS 113 "Fair Value Measurement"',
                ['Explain the exit-price definition of fair value.',
                 'Identify the principal or most advantageous market and treat costs.',
                 'Apply highest and best use for non-financial assets.',
                 'Choose valuation techniques and classify measurements in the hierarchy.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p1-ch04-u02'],
                 'exam_tip': 'In market questions, compute net amounts only to pick the market; then price less transport only.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Exit price; orderly transaction; market participants.',
                             'Principal market, else most advantageous.',
                             'Transaction costs not deducted; transport costs deducted if location matters.',
                             'HBU: physically possible, legally permissible, financially feasible.',
                             'Market, cost, income approaches; Levels 1/2/3.'],
                 'remember': ['Lowest significant input sets the level.'],
                 'traps': ['Intended use does not override highest and best use.']},
                [('Fair value', 'Exit price'), ('Level 1', 'Quoted, identical, active'), ('Level 3', 'Unobservable'), ('HBU', 'Possible, permissible, feasible')],
                viva, cases)
