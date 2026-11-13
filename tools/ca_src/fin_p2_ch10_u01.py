"""CA Final · Paper 2 Advanced Financial Management · Chapter 10 Foreign Exchange Exposure and Risk Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch10-u01'
T1 = 'Forex market, quotations and cross rates'
T2 = 'Exchange rate theories: IRP, PPP and IFE'
T3 = 'Types of foreign exchange exposure'
T4 = 'Hedging tools and the fate of forward contracts'
T5 = 'Derivative products and exposure strategies'


def build():
    ck = Checks()
    fwd = ck.add('round(84*(1+0.07/2)/(1+0.04/2),4)', '6-month forward rate by IRP (₹/USD)')
    prem = ck.add('round((84*(1+0.07/2)/(1+0.04/2)-84)/84*12/6*100,2)', 'Annualised forward premium (%)')
    bid = ck.add('round(84.00*1.0800,4)', 'EUR/INR bid (₹)')
    ask = ck.add('round(84.10*1.0810,4)', 'EUR/INR ask (₹)')
    i1 = {'id': 'i1', 'title': 'Forward rate and cross rates', 'difficulty': 'moderate', 'minutes': 9,
          'q': '(a) Spot USD/INR is ₹84.00. Six-month interest rates are 7% p.a. in India and 4% p.a. in the US. Compute the 6-month forward rate by interest rate parity and the annualised forward premium on USD. (b) USD/INR is 84.00/84.10 and EUR/USD is 1.0800/1.0810. Compute the EUR/INR two-way quote.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Forward rate', '84 × 1.035 ÷ 1.02', '₹' + inr(fwd)],
              ['Annualised premium', '(F − S) ÷ S × 12/6', inr(prem) + '%'],
              ['EUR/INR bid', '84.00 × 1.0800', '₹' + inr(bid)],
              ['EUR/INR ask', '84.10 × 1.0810', '₹' + inr(ask)]], title='IRP and cross rates')],
          'checks': list(ck)}

    ck2 = Checks()
    fw = ck2.add('100000*84.80', 'Cost under forward cover (₹)')
    mm = ck2.add('round(100000/1.01*84*1.02,2)', 'Cost under money market hedge (₹)')
    diff = ck2.add('round(100000/1.01*84*1.02-100000*84.80,2)', 'Saving by forward cover (₹)')
    i2 = {'id': 'i2', 'title': 'Forward cover vs money market hedge', 'difficulty': 'hard', 'minutes': 10,
          'q': 'An importer must pay USD 1,00,000 in 3 months. Spot ₹84.00/USD; 3-month forward ₹84.80. USD deposit rate 4% p.a.; INR borrowing rate 8% p.a. Compare the rupee cost of a forward with a money market hedge.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Forward cost', '1,00,000 × 84.80', inr(fw)],
              ['USD to deposit now', '1,00,000 ÷ 1.01 = 99,009.90', '—'],
              ['Borrow INR now and buy USD', '99,009.90 × 84', '83,16,831.68'],
              ['Repay INR loan in 3 months', '× 1.02', inr(mm)],
              ['Forward cheaper by', 'Difference', inr(diff)]], title='Money market hedge')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'The forex market is a global over-the-counter market linking banks, corporates, central banks and dealers via systems like SWIFT for secure messaging. Banks hold nostro (our account with you), vostro (your account with us) and loro (their account with you) accounts, and manage both exchange (currency) positions and cash (fund) positions.',
            'Quotes: direct (home currency per unit of foreign, e.g. ₹84/USD) or indirect (foreign per unit of home); American and European terms. Bid is the dealer\'s buying rate, ask its selling rate; spread = ask − bid. Cross rates are derived through a common currency: buy at the bank\'s bid, sell at its ask.',
            'Forward rates are quoted as points added (premium) or subtracted (discount) from spot; broken-period rates are interpolated. Merchant rates for customers (TT, bill buying/selling) build in margins.'],
          'Read every quote from the bank\'s side: it buys low and sells high.',
          'If USD/INR is 84.00/84.10, a customer buying USD pays ₹84.10.'),
        C('c2', T2, [
            'Interest rate parity (IRP): forward ÷ spot = (1 + home interest) ÷ (1 + foreign interest) for the period. The higher-interest currency trades at a forward discount. Deviations allow covered interest arbitrage.',
            'Purchasing power parity (PPP): absolute — the same goods cost the same everywhere; relative — expected change in spot rate reflects the inflation differential: S₁ = S₀ × (1 + home inflation) ÷ (1 + foreign inflation).',
            'International Fisher effect (IFE): expected change in spot rate reflects nominal interest differentials. IRP holds well (arbitrage); PPP and IFE hold more loosely and over longer periods. Forecasting uses these parities plus technical and fundamental analysis.'],
          'Interest and inflation gaps explain where currencies should move.',
          'With Indian rates 7% and US 4%, the dollar trades at a forward premium of about 3% a year.'),
        C('c3', T3, [
            'Transaction exposure: risk that rate changes alter the home value of contracted foreign currency receipts or payments (imports, exports, loans) before settlement.',
            'Translation (accounting) exposure: effect of rate changes on consolidated statements when foreign subsidiaries\' accounts are translated; it affects reported figures, not necessarily cash.',
            'Economic (operating) exposure: effect of rate changes on future cash flows and competitive position — e.g. a rising rupee hurting exporters\' long-term margins even without current contracts. It is harder to hedge and needs operational responses (sourcing, pricing, location).'],
          'Transaction hits cash now, translation hits reports, economic hits the future business.',
          'An exporter facing cheaper foreign rivals has economic exposure.'),
        C('c4', T4, [
            'Internal techniques: invoicing in home currency, leading and lagging, netting, matching receipts and payments, and asset-liability management. External techniques: forwards, money market hedges, futures, options and swaps.',
            'Money market hedge: for a payable, deposit the PV of the foreign amount now (borrowing home currency to buy it); for a receivable, borrow the PV in foreign currency and convert now. Compare with forward cost.',
            'Fate of forward contracts: delivery (on due date, early or late), cancellation (on due date, early or late) or extension. Under FEDAI rules, cancellation is at the opposite TT rate (TT selling for a purchase contract cancelled, etc.), with the exchange difference and any swap cost or interest settled with the customer; overdue contracts not cancelled are automatically cancelled after a set period, losses recovered and gains not passed on. Non-deliverable forwards settle only the difference; rollovers extend deliverable contracts.'],
          'Hedge with internal tools first, then markets — and know how forward contracts end.',
          'An importer cancelling a forward early settles the difference at the opposite rate.'),
        C('c5', T5, [
            'Currency futures and options trade on exchanges; options give one-way protection (call for importers, put for exporters) for a premium. Currency swaps exchange principal and interest in different currencies; interest rate swaps convert fixed to floating flows.',
            'Structured bank products include forward importer/exporter contracts with knock-out levels, FX call and put options, and floating-to-fixed IRS on foreign loans; their pay-offs must be understood at different spot outcomes.',
            'Exposure management strategies range from low risk–low reward (hedge everything), low risk–reasonable reward (selective hedging), high risk–low reward (selectively not hedging) to high risk–high reward (actively trading exposures). Policy should fit the board\'s risk appetite.'],
          'Pick tools that match the exposure and the board\'s appetite.',
          'An exporter buys a USD put to protect against a falling dollar while keeping upside.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Treasury policy for an exporter', 'role': 'Forex treasury manager',
             'situation': 'Monthly USD receipts of ₹50 crore equivalent; imports of USD inputs.',
             'steps': ['Net receipts and payments.', 'Forecast using parities and market views.', 'Hedge with forwards and options as per policy ratio.', 'Track cancellations, rollovers and P&L.'],
             'takeaway': 'Net first, then hedge the remainder with a written policy.'}]

    mcqs = [
        Q('m1', 'A direct quote in India is expressed as:', ['Rupees per unit of foreign currency', 'Foreign currency per rupee', 'Euro per dollar', 'Gold per rupee'], 0,
          'Home currency price of foreign. In practice: ₹84/USD.', 'c1', T1),
        Q('m2', 'Under IRP, the higher-interest currency trades at a:', ['Forward discount', 'Forward premium', 'Fixed rate', 'Par'], 0,
          'Interest gain offset by currency loss. In practice: covered arbitrage.', 'c2', T2),
        Q('m3', 'Relative PPP links exchange rate changes to:', ['Inflation differentials', 'Interest differentials only', 'GDP growth', 'Tax rates'], 0,
          'Price levels drive currency values. In practice: long run.', 'c2', T2),
        Q('m4', 'Exposure from translating a foreign subsidiary\'s accounts is:', ['Translation exposure', 'Transaction exposure', 'Economic exposure', 'Credit exposure'], 0,
          'Affects reported figures. In practice: Ind AS 21.', 'c3', T3),
        Q('m5', 'An importer can hedge with a money market hedge by:', ['Borrowing home currency, buying foreign currency now and depositing it', 'Borrowing foreign currency', 'Selling forward', 'Buying a put'], 0,
          'Lock rate today. In practice: compare with forward.', 'c4', T4),
        Q('m6', 'Leading and lagging is a:', ['Internal hedging technique', 'Futures contract', 'Swap', 'Option'], 0,
          'Timing of payments. In practice: within groups.', 'c4', T4),
        Q('m7', 'An exporter seeking downside protection with upside retained should buy a:', ['Put option on the foreign currency', 'Call option', 'Forward purchase', 'Swap'], 0,
          'Right to sell at strike. In practice: premium cost.', 'c5', T5),
        Q('m8', 'A nostro account is:', ['Our account maintained with a bank abroad', 'Their account with us', 'A government account', 'A futures margin account'], 0,
          'Held in foreign currency. In practice: vostro is the reverse.', 'c1', T1),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Forward', 2, 'computation', 'forward', nums=[fwd]), S('s2', 'Premium', 2, 'computation', 'premium', nums=[prem]), S('s3', 'Cross rates', 3, 'computation', 'bid|ask', nums=[bid, ask])],
          ['Use period rates.'], ['Mixing bid and ask in cross rates.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'Forward', 2, 'computation', 'forward', nums=[fw]), S('s2', 'Money market', 3, 'computation', 'money market|repay', nums=[mm]), S('s3', 'Decision', 2, 'computation', 'cheaper', nums=[diff])],
          ['Use quarterly rates.'], ['Using annual rates for 3 months.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State interest rate parity.', 'The forward rate divided by the spot rate equals one plus the home interest rate divided by one plus the foreign interest rate for the same period.',
          [P('p1', 'Forward and spot', 5, 'forward'), P('p2', 'Interest rates', 5, 'interest')], 'c2'),
        V('v2', 'Distinguish transaction and economic exposure.', 'Transaction exposure affects contracted cash flows already agreed; economic exposure affects future cash flows and competitiveness.',
          [P('p1', 'Contracted flows', 5, 'contract'), P('p2', 'Future competitiveness', 5, 'competitive')], 'c3'),
        V('v3', 'Name three internal hedging techniques.', 'Invoicing in home currency, leading and lagging, and netting or matching.',
          [P('p1', 'Invoicing and leading', 5, 'invoic|leading'), P('p2', 'Netting or matching', 5, 'netting|matching')], 'c4'),
        V('v4', 'What are the possible fates of a forward contract?', 'Delivery, cancellation or extension — each on the due date, early or late.',
          [P('p1', 'Delivery and cancellation', 5, 'delivery|cancellation'), P('p2', 'Extension', 5, 'extension')], 'c4'),
        V('v5', 'What is a currency swap?', 'An exchange of principal and interest payments in one currency for those in another currency.',
          [P('p1', 'Principal and interest', 5, 'principal'), P('p2', 'Two currencies', 5, 'another currency')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Textiles', 'difficulty': 'moderate',
              'case': 'Saffron Textiles will receive USD 2,00,000 in 6 months. Spot USD/INR is ₹84.00; 6-month forward ₹85.00. A 6-month USD put at strike ₹84.50 costs ₹0.60 per USD. Indian inflation is expected at 5% and US inflation at 2.5% for the year.',
              'mcqs': [
                  M('k1a', 'Rupee receipt under forward cover (₹ lakh):', ['170', '168', '169', '171'], 0,
                    '2,00,000 × 85. In practice: locks the rate.', 'core', check=170, topic=T4),
                  M('k1b', 'Minimum net receipt with the put (₹ lakh):', ['167.8', '169', '170', '168'], 0,
                    '2,00,000 × (84.50 − 0.60). In practice: upside kept.', 'moderate', check=167.8, topic=T5),
                  M('k1c', 'Spot in one year expected by relative PPP (₹, two decimals):', ['86.05', '84', '88.2', '81.95'], 0,
                    '84 × 1.05 ÷ 1.025. In practice: long-run guide.', 'moderate', check=86.05, topic=T2),
                  M('k1d', 'If the spot at maturity is ₹86, the better choice in hindsight was:', ['The put (receive 86 − 0.60 = 85.40)', 'The forward', 'Equal', 'Neither'], 0,
                    'Put lapses; sell at spot. In practice: options keep upside.', 'moderate', topic=T5),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch10', 1, 'Foreign Exchange Exposure and Risk Management',
                ['Read forex quotations, spreads, cross rates and forward points.',
                 'Apply IRP, PPP and IFE.',
                 'Identify transaction, translation and economic exposure.',
                 'Hedge with forwards and money market hedges and handle forward contract fates.',
                 'Use futures, options, swaps and structured products within an exposure strategy.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fin-p2-ch09-u01'],
                 'exam_tip': 'Convert annual rates to the period before applying IRP or money market hedges.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Direct vs indirect; bid-ask; cross rates.',
                             'IRP: F/S = (1+ih)/(1+if).',
                             'PPP and IFE for forecasting.',
                             'Transaction, translation, economic exposure.',
                             'Forward, MMH, futures, options, swaps; FEDAI cancellation rules.'],
                 'remember': ['Importers fear rupee depreciation; exporters fear appreciation.'],
                 'traps': ['Using annual rates for a 3-month money market hedge.']},
                [('IRP', 'F/S = (1+ih)/(1+if)'), ('PPP', 'S₁ = S₀(1+πh)/(1+πf)'), ('Importer option', 'Call'), ('Exporter option', 'Put')],
                viva, cases)
