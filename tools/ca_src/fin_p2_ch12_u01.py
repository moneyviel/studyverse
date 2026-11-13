"""CA Final · Paper 2 Advanced Financial Management · Chapter 12 Interest Rate Risk Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch12-u01'
T1 = 'Benchmark rates and the end of LIBOR'
T2 = 'Types and measurement of interest rate risk'
T3 = 'Traditional hedges: ALM and FRAs'
T4 = 'Modern hedges: futures, options, swaps and swaptions'


def build():
    ck = Checks()
    gap = ck.add('500-650', 'Repricing gap (₹ crore)')
    nii = ck.add('(500-650)*0.01', 'Change in net interest income for a 1% rise (₹ crore)')
    fra = ck.add('round(100000000*(0.09-0.08)*0.5/(1+0.09*0.5),0)', 'FRA settlement received by the buyer (₹)')
    i1 = {'id': 'i1', 'title': 'Gap exposure and an FRA', 'difficulty': 'moderate', 'minutes': 9,
          'q': '(a) A bank has rate-sensitive assets of ₹500 crore and rate-sensitive liabilities of ₹650 crore repricing within a year. Compute the gap and the effect on net interest income of a 1% rise in rates. (b) A company buys a 3×9 FRA at 8% on ₹10 crore. At settlement, the 6-month reference rate is 9%. Compute the settlement amount (paid at the start of the period).',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Gap', '500 − 650', '₹' + inr(gap) + ' crore (negative)'],
              ['NII effect', '−150 × 1%', '₹' + inr(nii) + ' crore'],
              ['FRA interest difference', '10 crore × 1% × 6/12', '₹5,00,000'],
              ['Discounted settlement', '5,00,000 ÷ (1 + 0.09 × 6/12)', '₹' + inr(fra) + ' to the buyer']], title='Gap and FRA')],
          'checks': list(ck)}

    ck2 = Checks()
    gain = ck2.add('(9.5-8)-(1.0-0.5)', 'Total gain from the swap (%)')
    i2 = {'id': 'i2', 'title': 'Comparative-advantage swap', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Company A can borrow fixed at 8% or floating at MIBOR + 0.5%. Company B can borrow fixed at 9.5% or floating at MIBOR + 1.0%. A wants floating, B wants fixed. Compute the total gain from a swap and each party\'s net cost if the gain is shared equally (no intermediary).',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Fixed differential', '9.5 − 8.0', '1.5%'],
              ['Floating differential', '1.0 − 0.5', '0.5%'],
              ['Total gain', '1.5 − 0.5', inr(gain) + '%'],
              ['A\'s net cost', 'MIBOR + 0.5 − 0.5', 'MIBOR'],
              ['B\'s net cost', '9.5 − 0.5', '9.0% fixed'],
              ['Structure', 'A borrows fixed at 8%, B floating; A pays B MIBOR, B pays A 8%', 'Achieves both']], title='Interest rate swap')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Benchmark (reference) rates are the base for pricing loans, bonds and derivatives; borrowers pay a spread in basis points over them.',
            'LIBOR was discontinued after manipulation scandals; since 2022 markets use alternative reference rates based on actual overnight transactions and close to risk-free: SOFR (US, secured), SONIA (UK), €STR (euro area), TONA (Japan), SARON (Switzerland).',
            'In India, benchmarks include MIBOR (FBIL overnight), T-bill rates, and the repo-linked external benchmark used by banks for loans.'],
          'Floating rates are benchmark plus spread — and the benchmarks have changed.',
          'A US dollar loan now references SOFR, not LIBOR.'),
        C('c2', T2, [
            'Interest rate risk arises from mismatches in rate-sensitive assets and liabilities. Types: gap (repricing) risk, basis risk (different benchmarks move differently), embedded option risk (prepayments, calls), yield curve risk (shape changes), price risk (value changes) and reinvestment risk.',
            'Gap = rate-sensitive assets − rate-sensitive liabilities in a time bucket. A positive gap gains when rates rise; a negative gap loses. Change in net interest income ≈ gap × change in rate.',
            'Measurement tools: maturity gap analysis, duration (and duration gap), simulation and value-at-risk.'],
          'Know whether you are asset- or liability-sensitive.',
          'A bank funding long fixed loans with short deposits loses when rates rise.'),
        C('c3', T3, [
            'Asset-liability management (ALM) aligns maturities and repricing of assets and liabilities, setting gap limits and using internal pricing.',
            'A forward rate agreement (FRA) fixes an interest rate for a future period on a notional amount; only the difference is settled. An A×B FRA starts in A months and ends in B months. Settlement = notional × (reference − FRA rate) × period ÷ (1 + reference × period), paid at the start.',
            'FRA buyers (borrowers) are protected against rate rises; sellers (lenders) against falls.'],
          'An FRA locks a future borrowing or lending rate without moving principal.',
          'A 3×9 FRA covers a 6-month period starting in 3 months.'),
        C('c4', T4, [
            'Interest rate futures are exchange-traded contracts on interest rates or bond prices; prices fall when rates rise, so borrowers hedge by selling futures.',
            'Interest rate options: caps (protect borrowers against rates above a strike), floors (protect lenders against rates below a strike), and collars (buy a cap and sell a floor to cut premium).',
            'Interest rate swaps exchange fixed and floating payments on a notional principal; comparative-advantage swaps create gains equal to the difference between fixed-rate and floating-rate spreads of the two parties. Swaptions are options to enter into a swap at agreed terms.'],
          'Futures and swaps lock; options insure; collars cap cost.',
          'A borrower with a cap at 9% pays no more than 9% plus the premium.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Managing a bank\'s rate risk', 'role': 'ALM desk analyst',
             'situation': 'The bank has a large negative one-year gap and expects rate hikes.',
             'steps': ['Prepare the maturity gap report.', 'Estimate NII sensitivity.', 'Use FRAs or swaps to reduce the gap.', 'Report against board limits.'],
             'takeaway': 'Measure the gap first, then choose the hedge.'}]

    mcqs = [
        Q('m1', 'LIBOR has been replaced in the US mainly by:', ['SOFR', 'MIBOR', 'SONIA', 'TONA'], 0,
          'Secured overnight financing rate. In practice: SONIA for sterling.', 'c1', T1),
        Q('m2', 'A negative gap means rising rates will:', ['Reduce net interest income', 'Increase net interest income', 'Have no effect', 'Increase assets'], 0,
          'Liabilities reprice faster. In practice: hedge with FRAs.', 'c2', T2),
        Q('m3', 'Basis risk arises when:', ['Different benchmark rates move differently', 'Rates are fixed', 'There is no debt', 'Futures expire'], 0,
          'Imperfect correlation. In practice: MIBOR vs T-bill.', 'c2', T2),
        Q('m4', 'A borrower protects against rising rates by:', ['Buying an FRA', 'Selling an FRA', 'Buying a floor', 'Buying futures'], 0,
          'FRA buyer gains if rates rise. In practice: settlement discounted.', 'c3', T3),
        Q('m5', 'A cap protects:', ['Borrowers against rates above a strike', 'Lenders against falling rates', 'Equity investors', 'Exporters'], 0,
          'Like a call on rates. In practice: premium paid.', 'c4', T4),
        Q('m6', 'A collar involves:', ['Buying a cap and selling a floor', 'Buying two caps', 'Selling a cap only', 'Buying a swap'], 0,
          'Lower premium. In practice: limits both ways.', 'c4', T4),
        Q('m7', 'A swaption is:', ['An option to enter into a swap', 'A futures contract', 'A loan', 'A bond'], 0,
          'Right, not obligation. In practice: for uncertain needs.', 'c4', T4),
        Q('m8', 'The total gain in a comparative-advantage swap equals:', ['Difference in fixed spreads minus difference in floating spreads', 'Sum of all rates', 'Fixed rate only', 'Notional × rate'], 0,
          'Quality spread differential. In practice: shared by parties.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Gap', 2, 'computation', 'gap', nums=[gap, nii]), S('s2', 'FRA', 4, 'computation', 'fra|settlement', nums=[fra])],
          ['Discount the FRA payment.'], ['Ignoring the discounting.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Differentials', 2, 'concept', 'differential'), S('s2', 'Gain', 2, 'computation', 'gain', nums=[gain]), S('s3', 'Net costs', 3, 'concept', 'net cost|mibor')],
          ['Show structure.'], ['Splitting wrongly.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Why were alternative reference rates introduced?', 'Because LIBOR relied on bank judgement and was manipulated; ARRs are based on actual overnight transactions.',
          [P('p1', 'LIBOR manipulation', 5, 'manipulat'), P('p2', 'Actual transactions', 5, 'transaction')], 'c1'),
        V('v2', 'What is gap analysis?', 'Comparing rate-sensitive assets and liabilities in time buckets to see how rate changes affect net interest income.',
          [P('p1', 'Rate-sensitive items', 5, 'rate-sensitive'), P('p2', 'Net interest income', 5, 'net interest')], 'c2'),
        V('v3', 'How does an FRA work?', 'It fixes a rate for a future period on a notional amount, and only the discounted interest difference is settled.',
          [P('p1', 'Future period rate', 5, 'future'), P('p2', 'Difference settled', 5, 'difference')], 'c3'),
        V('v4', 'Distinguish caps and floors.', 'A cap protects borrowers against rates rising above a strike; a floor protects lenders against rates falling below a strike.',
          [P('p1', 'Cap for borrowers', 5, 'borrower'), P('p2', 'Floor for lenders', 5, 'lender')], 'c4'),
        V('v5', 'Name four types of interest rate risk.', 'Gap risk, basis risk, embedded option risk and yield curve risk, along with price and reinvestment risk.',
          [P('p1', 'Gap and basis', 5, 'gap|basis'), P('p2', 'Option or yield curve', 5, 'option|yield curve')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Metro Infra borrowing', 'difficulty': 'moderate',
              'case': 'Metro Infra has a ₹200 crore floating loan at MIBOR + 1.5%, resetting annually. It enters a swap paying fixed 7% and receiving MIBOR. It also considers a cap at 8% on MIBOR costing 0.4% a year.',
              'mcqs': [
                  M('k1a', 'Net cost after the swap (%):', ['8.5', '7', '1.5', '9'], 0,
                    'Pays 7 fixed + 1.5 spread; MIBOR cancels. In practice: fixed cost.', 'core', check=8.5, topic=T4),
                  M('k1b', 'With the cap instead and MIBOR at 9%, effective cost (%):', ['9.9', '10.5', '9.5', '8.4'], 0,
                    'MIBOR capped at 8 + 1.5 spread + 0.4 premium. In practice: capped cost.', 'moderate', check=9.9, topic=T4),
                  M('k1c', 'With the cap and MIBOR at 6%, effective cost (%):', ['7.9', '9.9', '7.5', '6'], 0,
                    '6 + 1.5 + 0.4; cap not exercised. In practice: keeps benefit of falling rates.', 'moderate', check=7.9, topic=T4),
                  M('k1d', 'The swap removes mainly:', ['Interest rate (repricing) risk on the loan', 'Credit risk of Metro', 'Currency risk', 'Liquidity risk'], 0,
                    'Floating becomes fixed. In practice: counterparty risk remains.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch12', 1, 'Interest Rate Risk Management',
                ['Explain benchmark rates and the LIBOR transition.',
                 'Identify and measure types of interest rate risk.',
                 'Hedge with ALM and forward rate agreements.',
                 'Hedge with futures, caps, floors, collars, swaps and swaptions.'],
                {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['fin-p2-ch11-u01'],
                 'exam_tip': 'In swap sums, compute the quality spread differential first, then design the flows.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['ARRs replaced LIBOR: SOFR, SONIA, €STR, TONA.',
                             'Gap = RSA − RSL; ΔNII ≈ gap × Δr.',
                             'FRA settlement discounted to start of period.',
                             'Cap, floor, collar.',
                             'Swap gain = fixed spread diff − floating spread diff.'],
                 'remember': ['Borrowers buy FRAs and caps.'],
                 'traps': ['Forgetting to discount FRA settlements.']},
                [('FRA buyer', 'Borrower'), ('Cap', 'Borrower protection'), ('Floor', 'Lender protection'), ('Swap gain', 'QSD')],
                viva, cases)
