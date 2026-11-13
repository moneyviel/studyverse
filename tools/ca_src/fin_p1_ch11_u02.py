"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 2 Classification and Measurement of Financial Assets and Financial Liabilities.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u02'
T1 = 'Classifying financial assets: business model and SPPI'
T2 = 'Measuring financial assets: amortised cost, FVOCI, FVTPL'
T3 = 'Financial liabilities and reclassification'
T4 = 'Impairment: expected credit loss model'


def build():
    ck = Checks()
    cost = ck.add('6000*2.5771+100000*0.7938', 'Initial carrying amount at 8% (₹)')
    int1 = ck.add('(6000*2.5771+100000*0.7938)*0.08', 'Interest income year 1 (₹)')
    cl1 = ck.add('(6000*2.5771+100000*0.7938)*1.08-6000', 'Amortised cost at end of year 1 (₹)')
    i1 = {'id': 'i1', 'title': 'A bond at amortised cost', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Kestrel Ltd. buys a 3-year bond with face value ₹1,00,000 and a 6% annual coupon, priced to yield 8% (3-year annuity factor 2.5771; discount factor year 3: 0.7938). It holds such bonds to collect contractual cash flows. Compute the initial amount, year-1 interest income and closing amortised cost.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Classification', 'Hold-to-collect model + SPPI → amortised cost', '—'],
              ['Initial measurement', '6,000 × 2.5771 + 1,00,000 × 0.7938', inr(cost)],
              ['Interest income at EIR', '94,842.6 × 8%', inr(int1)],
              ['Coupon received', '1,00,000 × 6%', inr(6000)],
              ['Closing amortised cost', '94,842.6 + 7,587.41 − 6,000', inr(cl1)]], title='Effective interest method')],
          'checks': list(ck)}

    ck2 = Checks()
    s1 = ck2.add('1000000*0.02*0.4', 'Stage 1: 12-month ECL (₹)')
    s2 = ck2.add('1000000*0.15*0.4', 'Stage 2: lifetime ECL (₹)')
    i2 = {'id': 'i2', 'title': 'Expected credit losses', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Kestrel Ltd. lends ₹10 lakh. At year 1, credit risk has not increased significantly: 12-month probability of default 2%, loss given default 40%. At year 2, credit risk has increased significantly: lifetime probability of default 15%, loss given default 40%. Compute the loss allowance at each date (ignore discounting).',
          'solution': [table(['Date', 'Stage and working', '₹'], [
              ['Year 1', 'Stage 1: 10,00,000 × 2% × 40%', inr(s1)],
              ['Year 2', 'Stage 2: 10,00,000 × 15% × 40%', inr(s2)],
              ['Interest', 'Stage 1 and 2: on gross amount; Stage 3: on net amount', '—']], title='ECL stages')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Financial assets are classified on two tests: the entity\'s business model for managing them, and whether the contract pays nothing but principal plus interest on the amount still owed (the SPPI test).',
            'Business models: hold to collect contractual cash flows; hold to collect and sell; and others (trading, managing on fair value). Sales are not prohibited in hold to collect, but frequent or significant sales need explaining. Interest under SPPI means consideration for time value, credit risk, other basic lending risks and costs, and a profit margin; leverage or equity-linked returns fail.',
            'Result: debt assets passing SPPI in hold-to-collect go to amortised cost; in hold-to-collect-and-sell, to FVOCI; all others, to FVTPL. Equity investments are FVTPL, but an irrevocable election at initial recognition allows FVOCI for equity not held for trading. A fair value option can designate assets at FVTPL to remove an accounting mismatch.'],
          'Two questions — how is it managed, and what cash flows does it pay — decide the bucket.',
          'A convertible bond held as an investment fails SPPI and is at FVTPL.'),
        C('c2', T2, [
            'All financial assets are initially measured at fair value plus transaction costs (except FVTPL, where costs are expensed). Trade receivables without a significant financing component are measured at transaction price.',
            'Amortised cost uses the effective interest rate (EIR) — the rate that exactly discounts estimated future cash flows to the gross carrying amount. Debt at FVOCI: interest (EIR), impairment and exchange differences go to profit or loss; other fair value changes go to OCI and are recycled on derecognition.',
            'Equity at FVOCI: fair value changes in OCI are never recycled; dividends go to profit or loss. FVTPL: all changes in profit or loss. Day-one gains or losses are recognised only if fair value is based on observable market data; otherwise deferred.'],
          'Amortised cost tracks the EIR; FVOCI debt recycles; FVOCI equity never does.',
          'A bond bought at a discount accretes up to face value.'),
        C('c3', T3, [
            'Financial liabilities are measured at amortised cost, except: FVTPL liabilities (held for trading, derivatives, or designated); liabilities from transfers not qualifying for derecognition; financial guarantee contracts; commitments to lend below market; and contingent consideration of an acquirer.',
            'For liabilities designated at FVTPL, the change in fair value due to own credit risk goes to OCI (unless this creates a mismatch), with the rest in profit or loss.',
            'Reclassification of financial assets happens only when the business model changes (expected to be very infrequent), applied prospectively from the reclassification date — the first day of the next reporting period. Financial liabilities are never reclassified.'],
          'Liabilities are usually at amortised cost; assets move only with business models.',
          'A bank exiting a lending business may reclassify the loans.'),
        C('c4', T4, [
            'Ind AS 109 uses a forward-looking expected credit loss (ECL) model for amortised cost assets, debt at FVOCI, lease receivables, contract assets, loan commitments and financial guarantees.',
            'General approach: Stage 1 — 12-month ECL; Stage 2 (significant increase in credit risk since initial recognition) — lifetime ECL; Stage 3 (credit-impaired) — lifetime ECL with interest on net carrying amount. A rebuttable presumption treats more than 30 days past due as a significant increase, and 90 days as default.',
            'Simplified approach: trade receivables and contract assets (without significant financing) always use lifetime ECL, often via a provision matrix based on historical loss rates adjusted for forward-looking information. Purchased or originated credit-impaired assets use a credit-adjusted EIR.'],
          'Provide for losses you expect, not only those that have happened.',
          'A provision matrix applies ageing-bucket loss rates to receivables.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Classifying a treasury portfolio', 'role': 'Treasury accountant',
             'situation': 'A company holds bonds, mutual funds, equity stakes and receivables.',
             'steps': ['Document business models per portfolio.', 'Run SPPI tests on each instrument.', 'Elect FVOCI for strategic equity if desired.', 'Build ECL staging and provision matrix.'],
             'takeaway': 'Classification is decided at inception; impairment is reassessed each period.'}]

    mcqs = [
        Q('m1', 'A debt instrument passing SPPI held to collect contractual cash flows is measured at:', ['Amortised cost', 'FVTPL', 'FVOCI', 'Cost'], 0,
          'Both tests point to amortised cost. In practice: use EIR.', 'c1', T1),
        Q('m2', 'Fair value gains on equity designated at FVOCI are:', ['Never recycled to profit or loss', 'Recycled on sale', 'Recognised in profit or loss', 'Ignored'], 0,
          'Only dividends go to profit or loss. In practice: transfer within equity on sale.', 'c2', T2),
        Q('m3', 'Transaction costs on FVTPL assets are:', ['Expensed', 'Capitalised', 'Deferred', 'Amortised'], 0,
          'They are not added to the asset. In practice: brokerage on trading shares.', 'c2', T2),
        Q('m4', 'Financial liabilities can be reclassified:', ['Never', 'When the business model changes', 'Annually', 'With auditor approval'], 0,
          'Only assets reclassify. In practice: rare event.', 'c3', T3),
        Q('m5', 'Stage 2 under the ECL model requires recognising:', ['Lifetime expected credit losses', '12-month losses', 'Incurred losses only', 'Nothing'], 0,
          'After significant increase in credit risk. In practice: interest on gross amount.', 'c4', T4),
        Q('m6', 'Trade receivables without a significant financing component use:', ['Lifetime ECL under the simplified approach', '12-month ECL', 'No impairment', 'Incurred loss'], 0,
          'Simplified approach is mandatory for these. In practice: provision matrix.', 'c4', T4),
        Q('m7', 'Own credit risk changes on liabilities designated at FVTPL go to:', ['OCI, unless this creates a mismatch', 'Profit or loss', 'Equity directly', 'Revenue'], 0,
          'Avoids counter-intuitive gains. In practice: not recycled.', 'c3', T3),
        Q('m8', 'An investment in a mutual fund whose returns depend on market prices is usually:', ['At FVTPL, failing SPPI', 'At amortised cost', 'At FVOCI without election', 'At cost'], 0,
          'Units are not simple lending. In practice: often held at fair value.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Classification', 1, 'concept', 'amortised cost'), S('s2', 'Initial', 1.5, 'computation', 'initial', nums=[cost]), S('s3', 'Interest', 1.5, 'computation', 'interest', nums=[int1]), S('s4', 'Closing', 2, 'computation', 'closing', nums=[cl1])],
          ['Use EIR, not coupon.'], ['Recognising coupon as income.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Stage 1', 2.5, 'computation', 'stage 1|12-month', nums=[s1]), S('s2', 'Stage 2', 2.5, 'computation', 'stage 2|lifetime', nums=[s2])],
          ['State the trigger.'], ['Using lifetime ECL in Stage 1.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What two tests classify financial assets?', 'The business model for managing the assets and the contractual cash flow characteristics, known as the SPPI test.',
          [P('p1', 'Business model', 5, 'business model'), P('p2', 'SPPI', 5, 'sppi')], 'c1'),
        V('v2', 'What is the effective interest rate?', 'The rate that exactly discounts expected future cash payments or receipts over the instrument\'s life to its gross carrying amount.',
          [P('p1', 'Discounts future cash flows', 5, 'discount'), P('p2', 'Gross carrying amount', 5, 'carrying amount')], 'c2'),
        V('v3', 'How is debt at FVOCI accounted for?', 'Interest, impairment and exchange differences go to profit or loss; other fair value changes go to OCI and are recycled on derecognition.',
          [P('p1', 'Interest in P&L', 5, 'interest'), P('p2', 'OCI recycled', 5, 'recycl')], 'c2'),
        V('v4', 'When can financial assets be reclassified?', 'Only when the business model for managing them changes, prospectively from the next reporting period\'s first day.',
          [P('p1', 'Business model change', 6, 'business model'), P('p2', 'Prospective', 4, 'prospective')], 'c3'),
        V('v5', 'Describe the three ECL stages.', 'Stage 1 needs 12-month ECL; Stage 2, after a significant rise in credit risk, needs lifetime ECL; Stage 3, credit-impaired, needs lifetime ECL with interest on the net amount.',
          [P('p1', '12-month vs lifetime', 6, '12-month|lifetime'), P('p2', 'Credit-impaired', 4, 'impaired')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Harbor Finance Ltd.', 'difficulty': 'moderate',
              'case': 'Harbor Finance Ltd. holds: government bonds managed to collect interest and sell when liquidity is needed; shares of a supplier held long-term (elected FVOCI); trade receivables of ₹50 lakh with an expected lifetime loss rate of 3%; and a loan 45 days past due with no evidence to rebut the presumption.',
              'mcqs': [
                  M('k1a', 'The government bonds are measured at:', ['FVOCI', 'Amortised cost', 'FVTPL', 'Cost'], 0,
                    'Hold to collect and sell + SPPI. In practice: recycle on sale.', 'core', topic=T1),
                  M('k1b', 'On selling the supplier shares, the accumulated OCI gain is:', ['Transferred within equity, not recycled', 'Recycled to profit or loss', 'Reversed', 'Taxed separately'], 0,
                    'FVOCI equity never recycles. In practice: transfer to retained earnings.', 'moderate', topic=T2),
                  M('k1c', 'Loss allowance on trade receivables (₹ lakh):', ['1.5', '0.5', '3', '15'], 0,
                    '50 × 3% lifetime. In practice: simplified approach.', 'core', check=1.5, topic=T4),
                  M('k1d', 'The loan 45 days past due is in:', ['Stage 2 — lifetime ECL', 'Stage 1', 'Stage 3', 'Written off'], 0,
                    'The 30-day presumption indicates significant increase. In practice: rebuttable with evidence.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 2, 'Classification and Measurement of Financial Assets and Financial Liabilities',
                ['Classify financial assets using the business model and SPPI tests.',
                 'Measure assets at amortised cost, FVOCI and FVTPL.',
                 'Measure financial liabilities and apply reclassification rules.',
                 'Apply the expected credit loss model.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 40}, 'prereq': ['fin-p1-ch11-u01'],
                 'exam_tip': 'For each asset state the business model, the SPPI result and the category — then measure.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Business model + SPPI decide category.',
                             'Amortised cost via EIR.',
                             'FVOCI debt recycles; FVOCI equity does not.',
                             'Liabilities mostly at amortised cost; never reclassified.',
                             'ECL: 12-month, lifetime, credit-impaired.'],
                 'remember': ['Trade receivables: simplified approach.'],
                 'traps': ['Recognising coupon instead of EIR interest.']},
                [('Hold to collect', 'Amortised cost'), ('Collect and sell', 'FVOCI'), ('Others', 'FVTPL'), ('ECL Stage 2', 'Lifetime')],
                viva, cases)
