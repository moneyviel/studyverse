"""CA Final · Paper 1 Financial Reporting · Chapter 7 Unit 2 Ind AS 21 The Effects of Changes in Foreign Exchange Rates.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch07-u02'
T1 = 'Functional and presentation currency'
T2 = 'Reporting foreign currency transactions'
T3 = 'Translating a foreign operation'
T4 = 'Net investment, disposal and exchangeability'


def build():
    ck = Checks()
    init = ck.add('50000*82/100000', 'Payable at transaction date (₹ lakh)')
    ye = ck.add('50000*84/100000', 'Payable at year end (₹ lakh)')
    loss = ck.add('50000*(84-82)/100000', 'Exchange loss at year end (₹ lakh)')
    gain = ck.add('50000*(84-83.5)/100000', 'Exchange gain on settlement (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'An imported machine on credit', 'difficulty': 'core', 'minutes': 7,
          'q': 'Arya Ltd. (functional currency INR) buys a machine for USD 50,000 on 1 February when USD 1 = ₹82, payable on 30 April. At 31 March, USD 1 = ₹84; on 30 April it pays at ₹83.5. Record the machine, the payable, and the exchange differences.',
          'solution': [table(['Date', 'Working', '₹ lakh'], [
              ['1 Feb — machine and payable', '50,000 × 82', inr(init)],
              ['31 Mar — payable retranslated', '50,000 × 84', inr(ye)],
              ['Exchange loss in profit or loss', '50,000 × 2', inr(loss)],
              ['Machine (non-monetary at historical cost)', 'Stays at 41.00', inr(init)],
              ['30 Apr — exchange gain on payment', '50,000 × 0.5', inr(gain)]], title='Monetary vs non-monetary')],
          'checks': list(ck)}

    ck2 = Checks()
    a = ck2.add('1000*85', 'Assets translated at closing rate (₹ thousand)')
    l = ck2.add('400*85', 'Liabilities translated at closing rate (₹ thousand)')
    p = ck2.add('200*83', 'Profit translated at average rate (₹ thousand)')
    ctr = ck2.add('1000*85-400*85-(400*80+200*83)', 'Exchange difference to OCI (₹ thousand)')
    i2 = {'id': 'i2', 'title': 'Translating a US subsidiary', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'A US subsidiary (functional currency USD) was set up with net assets of USD 400 thousand when USD 1 = ₹80. This year it earned profit of USD 200 thousand (average rate ₹83). At year end, assets are USD 1,000 thousand and liabilities USD 400 thousand; closing rate ₹85. Translate and compute the exchange difference.',
          'solution': [table(['Item', 'Working', '₹ thousand'], [
              ['Assets', '1,000 × 85', inr(a)],
              ['Liabilities', '400 × 85', inr(l)],
              ['Opening net assets', '400 × 80', inr(32000)],
              ['Profit', '200 × 83', inr(p)],
              ['Exchange difference (OCI, foreign currency translation reserve)', '51,000 − (32,000 + 16,600)', inr(ctr)]], title='Translation')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'An entity\'s functional currency is the one used in the main economic setting where it does business. Primary indicators: the currency that mainly influences sales prices, and the currency of the country whose competitive forces and regulations mainly set prices; and the currency that chiefly drives what it pays for staff, materials and other inputs.',
            'Secondary indicators: currency in which financing is raised and operating receipts are retained. For a foreign operation, consider autonomy from the parent, proportion of transactions with the parent, direct cash-flow effects on the parent, and self-sufficiency in servicing debts.',
            'Presentation currency is the currency in which statements are presented and may be any currency. Functional currency changes only when underlying conditions change, applied prospectively.'],
          'Functional currency is where the entity lives economically; presentation currency is just the display.',
          'An Indian company selling and buying in rupees has INR as functional currency, even if it reports in USD.'),
        C('c2', T2, [
            'A foreign currency transaction is first recorded in the functional currency at the spot rate on the transaction date (an average rate may be used if rates do not fluctuate significantly).',
            'At each reporting date: monetary items (cash, receivables, payables, loans) are retranslated at the closing rate; non-monetary items at historical cost stay at the transaction-date rate; non-monetary items at fair value use the rate when fair value was measured.',
            'Exchange differences on monetary items go to profit or loss. For non-monetary items, the exchange component follows the gain or loss: OCI if the gain goes to OCI (e.g. revaluation), otherwise profit or loss. Advance consideration (prepayments) uses the rate on the date of the advance, which sets the transaction date.'],
          'Monetary items move with the rate; non-monetary items stay frozen unless revalued.',
          'An advance paid to a foreign supplier fixes the rate for the related asset.'),
        C('c3', T3, [
            'Results and position of an entity whose functional currency is not hyperinflationary are translated into a different presentation currency as follows: assets and liabilities at the closing rate on each balance sheet date; income and expenses at transaction-date rates (average rates as a practical proxy).',
            'Resulting exchange differences are recognised in OCI and accumulated in a separate component of equity; the share attributable to non-controlling interests is allocated to them.',
            'Goodwill and fair value adjustments on acquiring a foreign operation are treated as its assets and liabilities, translated at the closing rate. Intra-group monetary balances still produce exchange differences in consolidated profit or loss, as they represent real exposure.'],
          'Closing rate for the balance sheet, average for profit — the gap goes to OCI.',
          'A strengthening dollar increases the rupee value of a US subsidiary\'s net assets.'),
        C('c4', T4, [
            'A balance owed to or by a foreign operation, whose settlement is neither planned nor likely in the foreseeable future, forms part of the net investment. Its exchange differences go to profit or loss in separate statements, but to OCI in consolidated statements.',
            'On disposal of a foreign operation, the cumulative exchange differences in OCI are reclassified to profit or loss. On partial disposal of a subsidiary without loss of control, a proportionate share is reattributed to non-controlling interests, not recycled.',
            'Lack of exchangeability: when a currency cannot be exchanged into another currency at the measurement date, the entity estimates the spot rate that would have applied to an orderly transaction between market participants under prevailing conditions, and discloses the effects and risks.'],
          'OCI amounts wait until the foreign operation is sold.',
          'A long-term loan to a subsidiary with no repayment plan is part of the net investment.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Consolidating a foreign subsidiary', 'role': 'Group accountant',
             'situation': 'A Singapore subsidiary reports in SGD; the group presents in INR.',
             'steps': ['Confirm the subsidiary\'s functional currency.', 'Translate assets and liabilities at closing, P&L at average rates.', 'Post the difference to the translation reserve.', 'Treat intra-group loans with no repayment plan as net investment.'],
             'takeaway': 'Rate choice depends on the line item; the plug goes to OCI.'}]

    mcqs = [
        Q('m1', 'Monetary items in foreign currency are reported at the reporting date using:', ['The closing rate', 'The historical rate', 'The average rate', 'The forward rate'], 0,
          'They are retranslated each period. In practice: loans and payables.', 'c2', T2),
        Q('m2', 'Exchange differences on translating a foreign operation are recognised in:', ['OCI', 'Profit or loss', 'Revenue', 'Retained earnings directly'], 0,
          'Accumulated in equity until disposal. In practice: foreign currency translation reserve.', 'c3', T3),
        Q('m3', 'A primary indicator of functional currency is the currency that:', ['Mainly influences sales prices', 'Is used to raise finance', 'Is used to present statements', 'The parent uses'], 0,
          'Financing is secondary. In practice: assess sales and costs first.', 'c1', T1),
        Q('m4', 'A non-monetary asset measured at historical cost is translated at:', ['The rate at the date of the transaction', 'The closing rate', 'The average rate', 'The forward rate'], 0,
          'It is not retranslated. In practice: PPE and inventory at cost.', 'c2', T2),
        Q('m5', 'On disposal of a foreign operation, cumulative translation differences are:', ['Reclassified to profit or loss', 'Left in equity', 'Transferred to retained earnings', 'Written off to OCI'], 0,
          'They are recycled. In practice: part of the gain on disposal.', 'c4', T4),
        Q('m6', 'Goodwill on acquiring a foreign operation is translated at:', ['The closing rate', 'The historical rate', 'The average rate', 'Not translated'], 0,
          'It is treated as an asset of the foreign operation. In practice: creates translation differences.', 'c3', T3),
        Q('m7', 'A payment in advance to a foreign supplier is:', ['A non-monetary item; it sets the rate for the related asset', 'Monetary and retranslated', 'Translated at closing rate', 'Expensed'], 0,
          'Appendix B guidance. In practice: no exchange difference on the advance.', 'c2', T2),
        Q('m8', 'If a currency lacks exchangeability, the entity:', ['Estimates the spot rate for an orderly transaction', 'Uses last year\'s rate', 'Stops translating', 'Uses the forward rate'], 0,
          'The 2025 amendment requires an estimate with disclosure. In practice: use observable rates if suitable.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Initial', 1, 'computation', 'initial|transaction', nums=[init]), S('s2', 'Year end loss', 2, 'computation', 'loss', nums=[loss]), S('s3', 'Settlement gain', 1, 'computation', 'gain', nums=[gain]), S('s4', 'Machine unchanged', 1, 'concept', 'historical|non-monetary')],
          ['Separate monetary items.'], ['Retranslating the machine.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Closing rate items', 2, 'computation', 'closing', nums=[a, l]), S('s2', 'Profit at average', 2, 'computation', 'average', nums=[p]), S('s3', 'Difference', 2, 'computation', 'oci|reserve', nums=[ctr])],
          ['Show the reserve.'], ['Using closing rate for profit.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is functional currency?', 'The currency of the main economic environment where the entity operates, mainly the one driving its prices and costs.',
          [P('p1', 'Economic environment', 5, 'economic environment'), P('p2', 'Prices and costs', 5, 'price|cost')], 'c1'),
        V('v2', 'How are monetary and non-monetary items treated at year end?', 'Monetary items use the closing rate; non-monetary items at cost keep the transaction-date rate, and those at fair value use the valuation-date rate.',
          [P('p1', 'Closing rate for monetary', 5, 'closing'), P('p2', 'Historical for non-monetary', 5, 'transaction-date|historical')], 'c2'),
        V('v3', 'What rates are used to translate a foreign operation?', 'Closing rate for assets and liabilities and transaction or average rates for income and expenses, with differences to OCI.',
          [P('p1', 'Closing and average', 6, 'closing|average'), P('p2', 'OCI', 4, 'oci')], 'c3'),
        V('v4', 'What is a net investment in a foreign operation?', 'The parent\'s share of its net assets, including long-term monetary balances whose settlement is neither planned nor likely in the foreseeable future.',
          [P('p1', 'Share of net assets', 5, 'net assets'), P('p2', 'Long-term balances', 5, 'settlement|foreseeable')], 'c4'),
        V('v5', 'What happens to the translation reserve on disposal?', 'It is reclassified from equity to profit or loss as part of the gain or loss on disposal.',
          [P('p1', 'Reclassified', 6, 'reclassif'), P('p2', 'Profit or loss', 4, 'profit or loss')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Ganga Exports Ltd.', 'difficulty': 'moderate',
              'case': 'Ganga Exports Ltd. (INR functional currency) sells goods for EUR 20,000 on 1 March (EUR 1 = ₹90). At 31 March EUR 1 = ₹92. It also has a long-term EUR loan to its German subsidiary with no repayment plan, and holds an equity investment in a French company measured at fair value through OCI.',
              'mcqs': [
                  M('k1a', 'Exchange gain on the receivable at 31 March (₹):', ['40,000', '20,000', '18,40,000', 'Nil'], 0,
                    '20,000 × (92 − 90) = 40,000. In practice: to profit or loss.', 'core', check=40000, topic=T2),
                  M('k1b', 'Revenue recognised for the sale (₹ lakh):', ['18', '18.4', '20', '9'], 0,
                    '20,000 × 90 = ₹18 lakh at the transaction date. In practice: revenue is not retranslated.', 'core', check=18, topic=T2),
                  M('k1c', 'In consolidated statements, exchange differences on the loan to the subsidiary go to:', ['OCI', 'Profit or loss', 'Revenue', 'Goodwill'], 0,
                    'It is part of the net investment. In practice: P&L in separate statements.', 'moderate', topic=T4),
                  M('k1d', 'The exchange component of the fair value change on the French equity investment goes to:', ['OCI, with the fair value change', 'Profit or loss', 'Retained earnings directly', 'Capital reserve'], 0,
                    'It follows the gain. In practice: never recycled for FVOCI equity.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch07', 2, 'Ind AS 21 "The Effects of Changes in Foreign Exchange Rates"',
                ['Determine functional and presentation currency.',
                 'Record and report foreign currency transactions.',
                 'Translate the statements of a foreign operation.',
                 'Apply net investment, disposal and exchangeability rules.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch07-u01'],
                 'exam_tip': 'Label every item monetary or non-monetary before choosing a rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Functional currency: primary economic environment.',
                             'Transactions at spot rate; monetary items at closing rate.',
                             'Monetary differences → profit or loss.',
                             'Foreign operation: closing for B/S, average for P&L, difference to OCI.',
                             'Disposal: recycle translation reserve.'],
                 'remember': ['Advances fix the transaction date rate.'],
                 'traps': ['Retranslating non-monetary items at cost.']},
                [('Monetary', 'Closing rate'), ('Non-monetary at cost', 'Historical rate'), ('Translation difference', 'OCI'), ('Disposal', 'Recycle')],
                viva, cases)
