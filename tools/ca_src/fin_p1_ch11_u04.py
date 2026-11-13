"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 4 Derivatives and Embedded Derivatives.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u04'
T1 = 'What makes a contract a derivative'
T2 = 'Accounting for standalone derivatives'
T3 = 'Embedded derivatives: when to separate'
T4 = 'Common derivative instruments'


def build():
    ck = Checks()
    fv = ck.add('1000000*(84.5-83)/100000', 'Fair value of forward at year end (₹ lakh)')
    st = ck.add('1000000*(82-83)/100000', 'Cumulative result at settlement (₹ lakh)')
    mv = ck.add('1000000*(82-83)/100000-1000000*(84.5-83)/100000', 'Loss in the second period (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A currency forward', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Orbit Ltd. enters into a forward on 1 February to buy USD 10 lakh at ₹83 on 31 May; no premium is paid. It is not designated as a hedge. At 31 March, the forward rate for 31 May is ₹84.5. On 31 May, the spot rate is ₹82. Ignore discounting. Show amounts in profit or loss.',
          'solution': [table(['Date', 'Working', '₹ lakh'], [
              ['1 Feb', 'Fair value nil at inception', inr(0)],
              ['31 Mar — derivative asset, gain in P&L', '10,00,000 × (84.5 − 83)', inr(fv)],
              ['31 May — cumulative position', '10,00,000 × (82 − 83)', inr(st)],
              ['Loss recognised in second period', '−10 − 15', inr(mv)]], title='Derivative at FVTPL')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Separate the embedded derivative?', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Assess separation for Orbit Ltd. (holder or issuer as stated): (a) Orbit issues a bond whose interest is linked to the Nifty index; (b) Orbit issues a loan with an interest rate cap above market rate at issue; (c) Orbit holds a bond whose principal is linked to gold prices; (d) Orbit leases a warehouse with rent indexed to local inflation; (e) Orbit sells goods to a German customer priced in USD (neither party\'s functional currency, and USD is not commonly used in that market).',
          'solution': [table(['Item', 'Separate?', 'Reason'], [
              ['(a) Issued equity-index bond', 'Yes', 'Equity-linked return not closely related to a debt host'],
              ['(b) Cap above market', 'No', 'Out-of-the-money cap at issue is closely related'],
              ['(c) Held gold-linked bond', 'No — whole asset at FVTPL', 'Financial asset hosts are not split; fails SPPI'],
              ['(d) Inflation-indexed rent', 'No', 'Local, non-leveraged inflation index is closely related'],
              ['(e) USD-priced sale contract', 'Yes', 'Currency not functional for either party nor commonly used']], title='Embedded derivatives')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'A derivative has three features: its value changes with an underlying variable (interest rate, price, exchange rate, index, credit rating, or a non-financial variable not specific to a party); it needs no initial net investment, or one smaller than for similar contracts; and it is settled at a future date.',
            'Examples: forwards, futures, swaps, options (purchased or written). An option premium is a small initial investment relative to buying the underlying, so options are still derivatives.',
            'Contracts to buy or sell non-financial items are derivatives only if net-settleable and not held for own use.'],
          'Underlying, little upfront money, settlement later — all three make a derivative.',
          'An interest rate swap with nil initial value is a derivative.'),
        C('c2', T2, [
            'Derivatives are financial assets or liabilities at fair value through profit or loss, unless designated as effective hedging instruments.',
            'They are recognised when the entity becomes party to the contract — even if fair value is nil at inception. A forward contract is recognised at nil and gains or losses arise as rates move.',
            'Fair value reflects market inputs (forward rates, volatility, credit risk). Changes in fair value go to profit or loss each period, producing volatility unless hedge accounting is applied.'],
          'Every derivative is on the balance sheet at fair value.',
          'A forward with favourable rates becomes an asset.'),
        C('c3', T3, [
            'An embedded derivative sits inside a larger (hybrid) contract and makes some cash flows vary like a standalone derivative. A derivative attached to a contract but separately transferable is a separate instrument.',
            'If the host is a financial asset within Ind AS 109, the whole hybrid is classified as a unit (usually failing SPPI → FVTPL). For other hosts, the embedded derivative is separated when: its economic characteristics and risks are not closely related to the host; a separate instrument with the same terms would be a derivative; and the hybrid is not measured at FVTPL.',
            'Closely related examples: inflation-indexed lease payments, caps and floors out of the money at inception, foreign currency in a functional or commonly used currency. Not closely related: equity- or commodity-indexed interest, leveraged features, calls in equity hosts.'],
          'Split only what behaves differently from the host contract.',
          'A loan whose interest follows a stock index hides an equity derivative.'),
        C('c4', T4, [
            'Forward contract: customised agreement to buy or sell at a fixed future price. Futures: standardised exchange-traded forwards with daily margining.',
            'Options: right without obligation to buy (call) or sell (put); the writer receives a premium and bears the obligation. Swaps: exchange of cash flow streams (interest rate swap: fixed for floating; currency swap: principal and interest in different currencies).',
            'Separated embedded derivatives are measured at fair value; the host is accounted for under the relevant standard. If the derivative cannot be measured separately, the whole contract is designated at FVTPL.'],
          'Know the instrument to know its underlying.',
          'A company paying fixed and receiving floating has swapped its interest exposure.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Derivative register', 'role': 'Risk analyst',
             'situation': 'Treasury signed forwards and swaps; procurement signed foreign-currency supply contracts.',
             'steps': ['List all derivatives and fair value them.', 'Scan commercial contracts for embedded features.', 'Test closely-related criteria.', 'Book changes in profit or loss unless hedging.'],
             'takeaway': 'Embedded derivatives often hide in ordinary contracts.'}]

    mcqs = [
        Q('m1', 'Which is not a feature of a derivative?', ['Large initial net investment', 'Value linked to an underlying', 'Future settlement', 'Little or no initial investment'], 0,
          'A large initial investment points away from a derivative. In practice: compare to buying the underlying.', 'c1', T1),
        Q('m2', 'Derivatives not designated as hedges are measured at:', ['Fair value through profit or loss', 'Amortised cost', 'Cost', 'FVOCI'], 0,
          'Changes hit profit or loss. In practice: hedge accounting can reduce volatility.', 'c2', T2),
        Q('m3', 'A forward contract with nil fair value at inception is:', ['Recognised at nil', 'Not recognised', 'Recognised at notional', 'Disclosed only'], 0,
          'It is still a contract the entity is party to. In practice: value moves later.', 'c2', T2),
        Q('m4', 'A hybrid contract with a financial asset host in Ind AS 109 scope is:', ['Classified as a whole', 'Always split', 'Measured at cost', 'Excluded'], 0,
          'No bifurcation for asset hosts. In practice: often FVTPL.', 'c3', T3),
        Q('m5', 'Inflation-indexed lease rentals based on the local economy are:', ['Closely related — not separated', 'Separated', 'Derivatives at FVTPL', 'Equity'], 0,
          'Non-leveraged local inflation is closely related. In practice: no split.', 'c3', T3),
        Q('m6', 'Interest linked to an equity index in a debt host issued by the entity is:', ['Not closely related — separate', 'Closely related', 'Ignored', 'Equity'], 0,
          'Equity risk differs from debt risk. In practice: fair value the embedded derivative.', 'c3', T3),
        Q('m7', 'The writer of an option:', ['Receives a premium and bears an obligation', 'Pays a premium', 'Has a right only', 'Has no exposure'], 0,
          'Writers take on obligations. In practice: written options are liabilities.', 'c4', T4),
        Q('m8', 'An interest rate swap typically exchanges:', ['Fixed for floating interest flows', 'Principal in two currencies only', 'Shares for cash', 'Goods for cash'], 0,
          'Currency swaps exchange currencies. In practice: used to hedge loans.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Inception', 1, 'concept', 'nil|inception'), S('s2', 'Year end', 2.5, 'computation', 'gain|asset', nums=[fv]), S('s3', 'Settlement', 2.5, 'computation', 'loss|settle', nums=[mv])],
          ['Track cumulative value.'], ['Not recognising at inception.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Separate items', 3, 'concept', 'separate|not closely'), S('s2', 'Closely related', 2, 'concept', 'closely related'), S('s3', 'Asset host', 2, 'concept', 'asset|fvtpl')],
          ['Reason each.'], ['Splitting a held asset.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'State the three characteristics of a derivative.', 'Its value changes with an underlying, it requires little or no initial net investment, and it is settled at a future date.',
          [P('p1', 'Underlying', 4, 'underlying'), P('p2', 'Small investment and future settlement', 6, 'investment|future')], 'c1'),
        V('v2', 'How are standalone derivatives measured?', 'At fair value through profit or loss unless designated as effective hedging instruments.',
          [P('p1', 'Fair value', 6, 'fair value'), P('p2', 'Hedging exception', 4, 'hedg')], 'c2'),
        V('v3', 'When is an embedded derivative separated?', 'When its risks differ from those of the host (failing the closely related test), would meet the derivative definition alone, and the hybrid is outside FVTPL — and the host is a non-asset contract.',
          [P('p1', 'Risks differ from host', 5, 'risks differ'), P('p2', 'Hybrid outside FVTPL', 5, 'fvtpl')], 'c3'),
        V('v4', 'Why are financial asset hosts not split?', 'Because Ind AS 109 classifies the whole hybrid asset using the SPPI and business model tests.',
          [P('p1', 'Whole hybrid', 5, 'whole'), P('p2', 'SPPI', 5, 'sppi')], 'c3'),
        V('v5', 'Distinguish forwards and futures.', 'Forwards are customised private contracts; futures are standardised, exchange-traded and margined daily.',
          [P('p1', 'Customised', 5, 'customised'), P('p2', 'Standardised exchange-traded', 5, 'standardised|exchange')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Vector Metals Ltd.', 'difficulty': 'moderate',
              'case': 'Vector Metals Ltd. buys a 2-year call option on 1,000 shares of another company for a premium of ₹50,000. It also has a supply contract to buy coal priced in rupees, settled by physical delivery for its plant, and borrows under a loan whose interest is 2 × MIBOR − 4% (leveraged).',
              'mcqs': [
                  M('k1a', 'The call option is:', ['A derivative at FVTPL', 'An equity investment at cost', 'Outside scope', 'A prepayment'], 0,
                    'Small premium relative to the shares; value follows share price. In practice: remeasure each period.', 'core', topic=T1),
                  M('k1b', 'The coal supply contract is:', ['Outside Ind AS 109 under own use', 'A derivative', 'A financial liability', 'A hedge'], 0,
                    'Physically settled for usage needs. In practice: no fair valuing.', 'core', topic=T1),
                  M('k1c', 'The leveraged interest feature in the loan is:', ['Not closely related — separated', 'Closely related', 'Equity', 'Ignored'], 0,
                    'Leverage can double rate exposure. In practice: fair value separately.', 'hard', topic=T3),
                  M('k1d', 'Initial carrying amount of the option (₹):', ['50,000', 'Nil', '5,00,000', '1,000'], 0,
                    'The premium paid equals initial fair value. In practice: transaction costs expensed.', 'core', check=50000, topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 4, 'Derivatives and Embedded Derivatives',
                ['Identify derivatives using the three characteristics.',
                 'Account for standalone derivatives at fair value.',
                 'Decide when embedded derivatives must be separated.',
                 'Recognise common derivative instruments.'],
                {'difficulty': 'hard', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch11-u03'],
                 'exam_tip': 'For embedded derivatives, first ask whether the host is a financial asset — if yes, do not split.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Derivative: underlying, small investment, future settlement.',
                             'At FVTPL unless hedge.',
                             'Recognised even at nil fair value.',
                             'Asset hosts: classify whole hybrid.',
                             'Other hosts: separate if not closely related.'],
                 'remember': ['Options are derivatives despite premiums.'],
                 'traps': ['Splitting embedded features from financial asset hosts.']},
                [('Features', 'Underlying + small investment + future'), ('Measure', 'FVTPL'), ('Asset host', 'Whole hybrid'), ('Other host', 'Closely related test')],
                viva, cases)
