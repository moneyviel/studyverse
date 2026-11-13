"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 7 Unit 3 — AS 11 The Effects of Changes in Foreign Exchange Rates.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch07-u03'
T1 = 'Key terms: monetary items, rates and exchange differences'
T2 = 'Recording transactions and reporting at the balance sheet date'
T3 = 'Exchange differences, including long-term monetary items'
T4 = 'Integral and non-integral foreign operations'
T5 = 'Forward exchange contracts and disclosure'


def build():
    ck = Checks()
    init = ck.add('20000*83', 'Purchase recorded on 1 February (₹)')
    ye = ck.add('20000*84', 'Creditor restated at 31 March (₹)')
    l1 = ck.add('1680000-1660000', 'Exchange loss in 2026-27 (₹)')
    pay = ck.add('20000*84.5', 'Amount paid on 30 April (₹)')
    l2 = ck.add('1690000-1680000', 'Exchange loss in 2027-28 (₹)')
    i1 = {'id': 'i1', 'title': 'An import spanning the year end', 'difficulty': 'core', 'minutes': 7,
          'q': 'Rhea Ltd. imported goods for US$20,000 on 1 February 2027 (₹83/$), still unsold on 31 March 2027 (closing rate ₹84/$), and paid the supplier on 30 April 2027 (₹84.5/$). Show the amounts.',
          'solution': [table(['Date', 'Item', 'Working', '₹'], [
              ['1 Feb', 'Purchase and creditor', '20,000 × 83', inr(init)],
              ['31 Mar', 'Creditor (monetary) at closing rate', '20,000 × 84', inr(ye)],
              ['31 Mar', 'Exchange loss for 2026-27', '', inr(l1)],
              ['31 Mar', 'Inventory (non-monetary, at cost)', 'Stays at historical rate', inr(init)],
              ['30 Apr', 'Payment', '20,000 × 84.5', inr(pay)],
              ['30 Apr', 'Exchange loss for 2027-28', '', inr(l2)]], title='AS 11 — monetary vs non-monetary')],
          'checks': list(ck)}

    ck2 = Checks()
    prem = ck2.add('50000*(83-82)', 'Premium on the forward contract (₹)')
    am = ck2.add('50000*3/4', 'Premium amortised to 31 March (3 of 4 months) (₹)')
    gain = ck2.add('50000*(82.6-82)', 'Exchange gain on the contract from spot movement (₹)')
    i2 = {'id': 'i2', 'title': 'Hedging with a forward contract', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'On 1 January 2027 Vyom Ltd. had a US$50,000 payable and took a 4-month forward contract to buy US$50,000 at ₹83 when spot was ₹82. Spot on 31 March 2027 is ₹82.6. The contract is a hedge, not for trading. Compute the premium, the amount charged in 2026-27 and the exchange difference on the contract.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Premium', '50,000 × (83 − 82)', inr(prem)],
              ['Premium charged in 2026-27', '50,000 × 3/4', inr(am)],
              ['Exchange gain on contract', '50,000 × (82.6 − 82)', inr(gain)],
              ['Exchange loss on the payable', 'Same spot movement', inr(gain)]], title='Forward contract (hedge)'),
              note('For a hedge, the premium or discount is spread over the life of the contract, and exchange differences on the contract go to profit and loss in the period the rate changes — offsetting those on the payable.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Reporting currency is the currency in which the financial statements are presented; foreign currency is any other.',
            'Monetary items are cash itself, plus claims and debts that will be settled in a fixed or calculable number of currency units — cash, receivables, payables, loans. Non-monetary items are all others — inventory, fixed assets, prepaid expenses, equity investments.',
            'Exchange rate is the ratio for exchanging two currencies; the closing rate is the rate at the balance sheet date. An exchange difference arises when the same number of foreign currency units is reported at different rates.'],
          'Monetary items carry fixed amounts of money, so their rupee value moves with the exchange rate.',
          'A dollar loan is monetary; a machine bought for dollars is not.'),
        C('c2', T2, [
            'A foreign currency transaction is first recorded in the reporting currency at the exchange rate on the transaction date. An average rate for a week or month may be used if rates do not change much.',
            'At each balance sheet date: monetary items are reported at the closing rate (or a rate that better reflects the amount realisable, where the closing rate is unrealistic); non-monetary items at historical cost are reported at the rate on the transaction date; non-monetary items at fair value use the rate when the fair value was determined.',
            'Carrying amounts of non-monetary items are also governed by other standards — for example inventory at lower of cost and NRV, where NRV is translated at the closing rate.'],
          'Restate money items at the year-end rate; leave cost-based non-money items alone.',
          'Dollar receivables are restated every year end; imported inventory keeps its original rupee cost.'),
        C('c3', T3, [
            'Exchange differences on settling monetary items, or on reporting them at rates different from those initially used, are recognised as income or expense in the period they arise (except as below).',
            'Long-term foreign currency monetary items (term of 12 months or more at origination): under paragraphs 46/46A, an enterprise may opt to add exchange differences relating to acquisition of a depreciable capital asset to the asset\'s cost, depreciating them over its balance life; other such differences may be parked in an FCMITD account (translation difference on such long-term items) and written off over the balance period of the item. The option, once exercised, is irrevocable and must be disclosed.',
            'Exchange differences on a monetary item that is, in substance, a net investment in a non-integral foreign operation go to a foreign currency translation reserve until disposal.'],
          'Normally, exchange gains and losses hit this year\'s profit and loss.',
          'A rupee fall that raises a short-term dollar payable by ₹2 lakh is charged to profit at once.'),
        C('c4', T4, [
            'An integral foreign operation carries on business as an extension of the reporting enterprise — for example a foreign sales office selling goods sent from India and remitting proceeds. Its statements are translated as if its transactions were the reporting enterprise\'s own.',
            'A non-integral foreign operation operates with substantial independence, earns and spends in its local currency and raises finance locally. Its assets and liabilities (monetary and non-monetary) are translated at the closing rate; income and expenses at transaction-date rates (average rates allowed); resulting differences go to a foreign currency translation reserve until the net investment is disposed of, when they are recognised in profit and loss.',
            'Indicators of non-integral status include: independent activities, local sales and costs, local financing and few transactions with the reporting enterprise. A change in classification is applied from the date of change.'],
          'An extension abroad is translated like home business; an independent foreign business is translated at closing rates with differences parked in reserves.',
          'A wholly independent subsidiary in Dubai, buying and selling locally, is non-integral.'),
        C('c5', T5, [
            'Forward exchange contracts not for trading or speculation: the premium or discount fixed at the start is spread as expense or income across the contract period; exchange differences on the contract are recognised in profit and loss in the period of the rate change. Profit or loss on cancellation or renewal is income or expense of that period.',
            'Contracts for trading or speculation: at each balance sheet date the gain or loss is the difference between the contract rate and the forward rate available for the remaining maturity; the premium or discount is not recognised separately.',
            'Disclose exchange differences in profit and loss, the amount in the translation reserve with its movement, reasons for using a different reporting currency, and any change in classification of a significant foreign operation.'],
          'Hedges spread their premium; speculative contracts are marked to the forward rate.',
          'A forward premium of ₹1 per dollar on a 4-month hedge is charged over 4 months.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end foreign currency restatement', 'role': 'Accounts executive',
             'situation': 'An exporter has dollar receivables, a 3-year dollar loan for machinery, imported stock and two forward contracts.',
             'steps': ['Classify each item as monetary or non-monetary.', 'Restate monetary items at the closing rate.', 'Check the paragraph 46/46A choice for the loan.', 'Amortise forward premiums for hedges.'],
             'takeaway': 'The monetary / non-monetary split drives everything.'}]

    mcqs = [
        Q('m1', 'Which is a monetary item?', ['Trade payable in US dollars', 'Inventory bought in US dollars', 'Machinery imported', 'Advance paid for a machine'], 0,
          'Monetary items are money or rights and obligations to receive or pay fixed or determinable amounts of money. A dollar payable qualifies; inventory, machinery and advances for goods are non-monetary. In practice: list items by nature.', 'c1', T1),
        Q('m2', 'At the balance sheet date, foreign currency monetary items are reported at:', ['The closing rate', 'The transaction date rate', 'The average rate of the year', 'The forward rate'], 0,
          'Monetary items are restated at the closing rate (or a more realistic realisable rate in rare cases), and the resulting difference goes to profit and loss. Non-monetary items at cost keep their historical rates. In practice: get the year-end rate.', 'c2', T2),
        Q('m3', 'A machine imported for US$10,000 at ₹80 is shown at the year end (rate ₹83) at:', ['₹8,00,000', '₹8,30,000', '₹8,15,000', '₹30,000'], 0,
          'The machine is a non-monetary item carried at historical cost, so it stays at the rate on the transaction date: 10,000 × ₹80 = ₹8,00,000, before depreciation. In practice: only the related loan is restated.', 'c2', T2, 'moderate', check=800000),
        Q('m4', 'A US$5,000 receivable recorded at ₹82 is restated at a closing rate of ₹83.5. Exchange gain:', ['₹7,500', '₹4,10,000', '₹4,17,500', '₹1,500'], 0,
          'Gain = 5,000 × (83.5 − 82) = ₹7,500, recognised in profit and loss because receivables are monetary. On settlement any further difference is also taken to profit and loss. In practice: restate every year end.', 'c3', T3, 'moderate', check=7500),
        Q('m5', 'Under paragraph 46A, exchange differences on a long-term foreign currency loan used to buy a depreciable asset may be:', ['Added to the cost of the asset and depreciated over its balance life', 'Credited to capital reserve', 'Ignored', 'Charged only on repayment'], 0,
          'The paragraph 46A option lets such differences be adjusted in the cost of the depreciable asset and depreciated over its remaining life; other long-term items use the FCMITD account. The option is irrevocable and disclosed. In practice: check the choice made.', 'c3', T3),
        Q('m6', 'For a non-integral foreign operation, assets and liabilities are translated at:', ['The closing rate', 'Historical rates', 'Average rate', 'Opening rate'], 0,
          'All assets and liabilities of a non-integral operation, monetary or not, are translated at the closing rate; income and expenses at transaction (or average) rates; differences go to a translation reserve. In practice: recycle on disposal.', 'c4', T4),
        Q('m7', 'Exchange differences on translating a non-integral foreign operation are:', ['Accumulated in a foreign currency translation reserve until disposal', 'Charged to profit and loss each year', 'Added to goodwill', 'Ignored'], 0,
          'They are taken to a foreign currency translation reserve and recognised in profit and loss only when the net investment is disposed of. This avoids volatility from rates that do not affect cash flows directly. In practice: track the reserve.', 'c4', T4),
        Q('m8', 'A foreign branch that sells goods sent by the head office and remits the proceeds is:', ['An integral foreign operation', 'A non-integral foreign operation', 'Not a foreign operation', 'A joint venture'], 0,
          'Such a branch operates as an extension of the reporting enterprise, so it is integral, and its items are translated as if the head office had transacted them. In practice: non-monetary items keep historical rates.', 'c4', T4),
        Q('m9', 'The premium on a forward contract taken as a hedge is:', ['Amortised over the life of the contract', 'Recognised fully at inception', 'Ignored', 'Recognised at maturity'], 0,
          'For contracts not taken for trading or speculation, AS 11 spreads the premium or discount over the contract life as expense or income. Spot-rate differences on the contract are recognised as rates change. In practice: prorate by months.', 'c5', T5),
        Q('m10', 'For a forward contract taken for speculation, the gain or loss at the year end is based on:', ['The forward rate available for the remaining maturity versus the contract rate', 'The spot rate versus the contract rate', 'The premium amortised', 'Nil until maturity'], 0,
          'Speculative contracts are measured by comparing the contract rate with the forward rate for the remaining maturity at the balance sheet date; premium or discount is not recognised separately. In practice: obtain forward quotes.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Initial recording', 1, 'computation', '83', nums=[init]),
           S('s2', 'Year-end restatement and loss', 2, 'computation', 'closing', nums=[ye, l1]),
           S('s3', 'Inventory not restated; settlement loss', 2, 'computation', 'non-monetary', nums=[l2])],
          ['Separate monetary and non-monetary.'], ['Restating inventory.'], ['Date-wise table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Premium', 1.5, 'computation', 'premium', nums=[prem]),
           S('s2', 'Amortisation', 1.5, 'computation', 'amortis|3/4', nums=[am]),
           S('s3', 'Spot difference', 2, 'computation', 'gain', nums=[gain])],
          ['Spread the premium.'], ['Charging the full premium at once.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are monetary items?', 'Cash, and claims or debts settled in a fixed or calculable number of currency units — such as cash, receivables, payables and loans.',
          [P('p1', 'Fixed amounts of money', 6, 'fixed|determinable'), P('p2', 'Examples', 4, 'receivable|payable|loan|cash')], 'c1'),
        V('v2', 'How are non-monetary items at historical cost reported at the year end?', 'Using the exchange rate on the date of the transaction.',
          [P('p1', 'Transaction date rate', 6, 'transaction'), P('p2', 'Rate', 4, 'rate')], 'c2'),
        V('v3', 'Distinguish integral and non-integral foreign operations.', 'An integral operation works as an extension of the reporting enterprise; a non-integral one operates with substantial independence in its own currency.',
          [P('p1', 'Extension', 5, 'extension'), P('p2', 'Independence', 5, 'independen')], 'c4'),
        V('v4', 'Where do translation differences of a non-integral operation go?', 'To a foreign currency translation reserve, recognised in profit and loss when the net investment is disposed of.',
          [P('p1', 'Translation reserve', 6, 'reserve'), P('p2', 'On disposal', 4, 'dispos')], 'c4'),
        V('v5', 'How is the premium on a hedge forward contract treated?', 'It is amortised as expense over the life of the contract.',
          [P('p1', 'Amortised', 6, 'amortis'), P('p2', 'Life of contract', 4, 'life')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Saanvi Exports Ltd.', 'difficulty': 'moderate',
              'case': 'Saanvi Exports Ltd. sold goods for US$40,000 on 15 March 2027 at ₹83; the closing rate on 31 March 2027 is ₹84; the customer paid on 20 April at ₹83.7. It also has a 5-year US$1,00,000 loan used to buy machinery and has opted for paragraph 46A.',
              'mcqs': [
                  M('k1a', 'Exchange gain recognised in 2026-27 on the receivable:', ['₹40,000', '₹28,000', '₹12,000', 'Nil'], 0,
                    'The receivable is restated from ₹83 to ₹84: 40,000 × ₹1 = ₹40,000 gain in 2026-27. Monetary items are restated at the closing rate. In practice: record in other income.', 'core', check=40000, topic=T3),
                  M('k1b', 'Exchange difference on settlement in 2027-28:', ['Loss of ₹12,000', 'Gain of ₹28,000', 'Loss of ₹40,000', 'Nil'], 0,
                    'Collected at ₹83.7 against ₹84 carried: 40,000 × 0.3 = ₹12,000 loss in 2027-28. Each year carries its own exchange difference. In practice: settle and recognise.', 'moderate', topic=T3),
                  M('k1c', 'With paragraph 46A chosen, the exchange loss on the machinery loan is:', ['Added to the machinery cost and depreciated over its remaining life', 'Charged to profit and loss immediately', 'Credited to capital reserve', 'Deferred until repayment'], 0,
                    'The 46A option allows exchange differences on long-term loans for depreciable assets to adjust the asset cost and be depreciated over its balance life. In practice: disclose the option.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch07', 3, 'Accounting Standard 11 The Effects of Changes in Foreign Exchange Rates',
                ['Classify monetary and non-monetary items and apply the correct rates.',
                 'Recognise exchange differences, including the long-term item options.',
                 'Translate integral and non-integral foreign operations.',
                 'Account for forward exchange contracts.'],
                {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['int-p1-ch07-u02'],
                 'exam_tip': 'Start every question with a monetary / non-monetary list; then pick the rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Initial: transaction-date rate (average allowed).', 'Year end: monetary at closing; non-monetary at historical (or FV-date) rate.',
                             'Differences to P&L; 46/46A option for long-term items.', 'Integral: as own transactions; non-integral: closing rate + translation reserve.',
                             'Hedge forwards: amortise premium; speculative: forward-rate mark.'],
                 'remember': ['Inventory and machinery are non-monetary.'],
                 'traps': ['Do not restate non-monetary items at the closing rate.']},
                [('Monetary items', 'Closing rate'), ('Non-monetary (cost)', 'Historical rate'), ('Non-integral', 'Translation reserve')],
                viva, cases)
