"""CA Foundation · Paper 4 Business Economics · Chapter 9 International Trade · Unit 4 Exchange Rate and Its Economic Effects.
Original explanations, numbers and questions; every figure computed in code."""
from lib import *
from ca_viva import P, V, ALT
from fnd_p4_ch09_u01 import M, S, Q, fx

UID = 'fnd-p4-ch09-u04'
LOC = ('local', 'domestic', 'home currency', 'rupee', 'rs', 'indian currency', 'own currency')
FOR = ('foreign', 'dollar', 'other currency', 'overseas currency')
HI = ('higher', 'more', 'above', 'exceed', 'exceeds', 'greater', 'over')
LO = ('lower', 'less', 'below', 'under', 'cheaper', 'smaller')


def build():
    # ---------- Illustration 1: quotes and cross rates ----------
    c1 = Checks()
    ind = c1.add('1/83.2*1000', 'indirect quote: US dollars per ₹1,000 (i.e. $0.01202 per rupee)')
    eur_inr = c1.add('84*1.1', 'cross rate: rupees per euro')
    gbp_inr = c1.add('round(84/0.79, 2)', 'cross rate: rupees per pound (via dollar)')
    ill1 = {'id': 'i1', 'title': 'Direct quote, indirect quote and cross rate', 'difficulty': 'core', 'minutes': 8,
            'q': '(a) A bank in Mumbai quotes $1 = ₹83.20. Is this a direct or an indirect quote for an Indian resident? Convert it to the other form. (b) If $1 = ₹84 and €1 = $1.10, find the rupee–euro cross rate. (c) If $1 = ₹84 and $1 = £0.79, find the rupee–pound cross rate.',
            'solution': [table(['Part', 'Working', 'Answer'], [
                ['(a) Type of quote', 'Rupees (local) per one dollar (foreign)', 'Direct quote (foreign currency is the base, rupee the counter currency)'],
                ['(a) Indirect quote', '1 ÷ 83.20', f'₹1 = $0.01202 (≈ ${fx(ind)} per ₹1,000)'],
                ['(b) ₹ per €', '₹84 per $ × $1.10 per €', f'€1 = ₹{fx(eur_inr)}'],
                ['(c) ₹ per £', '₹84 per $ ÷ £0.79 per $', f'£1 = ₹{fx(gbp_inr)}'],
            ]), note('A cross rate is a rate between two currencies worked out through their rates against a third (usually the US dollar, the "vehicle currency"). Indirect quote = reciprocal of the direct quote.')],
            'checks': c1}

    # ---------- Illustration 2: appreciation / depreciation percentages ----------
    c2 = Checks()
    usd_app = c2.add('(84-80)/80*100', 'dollar appreciation %')
    inr_dep = c2.add('round((80/84-1)*100, 2)', 'rupee depreciation % (negative = fall)')
    inr_app = c2.add('round((84/81-1)*100, 2)', 'rupee appreciation when ₹84 → ₹81')
    ill2 = {'id': 'i2', 'title': 'How much did each currency move?', 'difficulty': 'moderate', 'minutes': 8,
            'q': 'In January $1 = ₹80; in June $1 = ₹84. (a) Which currency appreciated and which depreciated? (b) By what percentage did the dollar appreciate and the rupee depreciate? (c) In October the rate moves to $1 = ₹81. What happened to the rupee, and by how much?',
            'solution': [table(['Measure', 'Working', 'Result'], [
                ['More rupees needed per dollar', '₹80 → ₹84', 'Rupee depreciated; dollar appreciated'],
                ['Dollar in rupees', '(84 − 80) ÷ 80 × 100', f'+{fx(usd_app)}%'],
                ['Rupee in dollars', '$1/84 vs $1/80 → (80 ÷ 84 − 1) × 100', f'{fx(inr_dep)}%'],
                ['October: ₹84 → ₹81', '(84 ÷ 81 − 1) × 100', f'Rupee appreciated by {fx(inr_app)}%'],
            ]), note('The two percentages are not equal: when one currency rises by 5%, the other falls by less than 5%. Always measure a currency\'s change in terms of the OTHER currency per unit of it.')],
            'checks': c2}

    # ---------- Illustration 3: real exchange rate ----------
    c3 = Checks()
    e_fd = c3.add('1/80*100', 'nominal rate: US cents per rupee ($0.0125)')
    rer_good = c3.add('(1/80)*50/2.5', 'real exchange rate, single good (rice) = 0.25')
    rer_idx = c3.add('round(84*110/125, 2)', 'real exchange rate with price indices (US view)')
    ill3 = {'id': 'i3', 'title': 'Real exchange rate: what can your money actually buy?', 'difficulty': 'hard', 'minutes': 10,
            'q': '(a) Rice costs ₹50 a kg in India and $2.50 a kg in the USA; $1 = ₹80. Using RER = nominal rate × domestic price ÷ foreign price (nominal rate in units of foreign currency per unit of domestic currency), find India\'s real exchange rate for rice and interpret it. (b) From the USA\'s point of view the nominal rate is ₹84 per dollar, the US price index is 110 and India\'s is 125. Find the US real exchange rate.',
            'solution': [table(['Step', 'Working', 'Result'], [
                ['(a) Nominal rate (foreign per domestic)', '$1 ÷ ₹80', f'$0.0125 per ₹ ({fx(e_fd)} US cents)'],
                ['(a) RER', '0.0125 × 50 ÷ 2.50', f'{fx(rer_good)}'],
                ['(a) Meaning', 'Indian rice in dollars = 50 ÷ 80 = $0.625 vs $2.50 in the USA', f'1 kg of Indian rice exchanges for {fx(rer_good)} kg of US rice — Indian rice is relatively cheap'],
                ['(b) US RER with indices', '84 × 110 ÷ 125', f'{fx(rer_idx)}'],
            ]), p('Trade flows respond to the real exchange rate, not the nominal one. A rise in the real exchange rate (or in the REER — the nominal effective rate against a weighted basket, adjusted for prices) makes a country\'s exports dearer and imports cheaper: a loss of competitiveness.')],
            'checks': c3}

    # ---------- Illustration 4: winners and losers from depreciation ----------
    c4 = Checks()
    exp0 = c4.add('50000*80', 'export receipts at ₹80'); exp1 = c4.add('50000*84', 'export receipts at ₹84')
    imp0 = c4.add('30000*80', 'import bill at ₹80'); imp1 = c4.add('30000*84', 'import bill at ₹84')
    ecb0 = c4.add('1000000*80', 'ECB principal at ₹80'); ecb1 = c4.add('1000000*84', 'ECB principal at ₹84'); ecb_l = c4.add('1000000*84-1000000*80', 'extra rupees to repay the ECB')
    fb0 = c4.add('10*80', 'goods a foreigner buys with $10 at ₹80'); fb1 = c4.add('10*84', 'goods a foreigner buys with $10 at ₹84')
    ill4 = {'id': 'i4', 'title': 'Depreciation: exporter, importer, ECB borrower and foreign buyer', 'difficulty': 'moderate', 'minutes': 10,
            'q': 'The rupee depreciates from ₹80 to ₹84 per dollar. Show the effect on (a) an exporter with receivables of $50,000, (b) an importer with payables of $30,000, (c) a company with an unhedged external commercial borrowing (ECB) of $10,00,000, (d) a foreign tourist spending $10 in India.',
            'solution': [table(['Party', 'At ₹80 (₹)', 'At ₹84 (₹)', 'Effect'], [
                ['(a) Exporter — $50,000 received', inr(exp0), inr(exp1), f'Gains {R(exp1 - exp0)}'],
                ['(b) Importer — $30,000 paid', inr(imp0), inr(imp1), f'Pays {R(imp1 - imp0)} more'],
                ['(c) ECB — $10,00,000 repayable', inr(ecb0), inr(ecb1), f'Debt burden up {R(ecb_l)}'],
                ['(d) Tourist — $10 spent', inr(fb0), inr(fb1), f'Buys {R(fb1 - fb0)} more of Indian goods'],
            ]), p('Depreciation makes exports cheaper for foreigners and imports dearer at home, helps exporters and import-competing firms, and hurts importers and unhedged foreign-currency borrowers. It can also push up consumer prices (imported goods, costlier inputs).')],
            'checks': c4}

    # ---------- Illustration 5: forward premium ----------
    c5 = Checks()
    prem = c5.add('round((83.83-83)/83*100, 2)', 'forward premium %')
    ann = c5.add('round((83.83-83)/83*12/3*100, 2)', 'annualised premium %')
    disc = c5.add('round((82.5-83)/83*100, 2)', 'forward discount %')
    ill5 = {'id': 'i5', 'title': 'Spot, forward, premium and discount', 'difficulty': 'moderate', 'minutes': 6,
            'q': 'Spot: $1 = ₹83.00. (a) The 3-month forward rate is ₹83.83. Is the dollar at a premium or discount, and by what percentage (also annualised)? (b) What if the 3-month forward rate were ₹82.50?',
            'solution': [table(['Case', 'Working', 'Result'], [
                ['(a) Forward ₹83.83 > spot ₹83.00', '(83.83 − 83) ÷ 83 × 100', f'Forward premium of {fx(prem)}% (≈ {fx(ann)}% a year)'],
                ['(b) Forward ₹82.50 < spot ₹83.00', '(82.50 − 83) ÷ 83 × 100', f'Forward discount of {fx(-disc)}%'],
            ]), note('Spot deals settle in about two days; forward deals fix today the rate for delivery on a future date. Forward rate above spot = premium; below spot = discount.')],
            'checks': c5}

    concepts = [
        {'id': 'c1', 'title': 'The exchange rate and foreign currency transactions', 'body': [
            'Households, firms and governments buy foreign goods, services and assets, invest, lend and borrow across borders. Each such deal needs one currency to be exchanged for another, and the exchange rate is the price of one currency in terms of another.',
            'A foreign currency transaction is one that is denominated in, or must be settled in, a foreign currency — buying or selling goods or services priced in foreign currency; borrowing or lending in foreign currency; becoming party to an unperformed forward exchange contract; or otherwise acquiring or disposing of assets, or incurring or settling liabilities, in foreign currency.',
            'Direct quote (European quotation): units of local currency for one unit of foreign currency — e.g. ₹83 per US$. Here the foreign currency acts as the base and the rupee (local currency) as the counter. Indirect quote (American quotation): units of foreign currency per unit of local currency — e.g. about $0.012 per rupee. One is the reciprocal of the other.',
            'Cross rate: the rate between two currencies derived from each one\'s rate against a third currency (e.g. ₹ per € from ₹ per $ and $ per €).'],
         'analogy': 'A direct quote is like a price tag in rupees on a dollar ("one dollar costs ₹83"); an indirect quote is how many dollars one rupee can buy.',
         'work': 'Every import, export, foreign loan and forward contract in a client\'s books is a foreign currency transaction that must be recorded and restated at the right rate — core work in accounting and audit.'},
        {'id': 'c2', 'title': 'Exchange rate regimes: floating, managed float, fixed', 'body': [
            'An exchange rate regime is the way a country manages its currency against others. At one end is a free float (flexible rate) set purely by market demand and supply with no central-bank intervention; in between is a managed float; at the other end a fixed (pegged) rate set by the government against another currency, a basket, or gold.',
            'Free float — advantages: self-regulating, acts as a buffer against external shocks (a rise in foreign demand is partly absorbed by a higher exchange rate); the central bank can run an independent monetary policy; the exchange rate can be used as a policy tool; no need for large reserves. Disadvantage: unpredictability — volatile rates add risk and a risk premium to cross-border deals.',
            'Managed float: the rate floats, but the central bank buys or sells its own currency (and makes announcements) from time to time to prevent sudden large swings; the impact is usually small but can shift expectations.',
            'Fixed rate — advantages: removes exchange risk and conversion uncertainty, boosting trade and investment; curbs speculation if the peg is credible; disciplines the monetary authority, so inflation tends to be lower; can add credibility to monetary policy. Disadvantage: the central bank must always stand ready to intervene and hold adequate reserves, and policy flexibility is lost. A soft peg lets the market largely set the rate; a hard peg fixes an unchanging value.',
            'In short: fixed = stability and credibility but no flexibility; floating = flexibility but less stability.'],
         'analogy': 'A free float is a kite in the wind; a managed float is a kite whose string the central bank tugs now and then; a fixed rate is a kite tied to a pole.',
         'work': 'Treasury teams of companies decide how much exposure to hedge depending on how volatile the currency regime is. Under a managed float like India\'s, CAs still assume rates will move and plan hedges accordingly.'},
        {'id': 'c3', 'title': 'Nominal vs real exchange rate; REER', 'body': [
            'The nominal exchange rate is the rate at which one currency trades for another. A country has many nominal rates (one per currency); an exchange rate index averages them into one measure.',
            'The real exchange rate is the rate at which the goods and services of one country trade for those of another — how many units of a foreign good one unit of the same domestic good can buy. It, not the nominal rate, drives trade flows and is a key determinant of net exports.',
            'Formula (as in the study material): Real exchange rate = Nominal exchange rate × Domestic price ÷ Foreign price; for the whole economy use price indices: Nominal rate × Domestic price index ÷ Foreign price index. (The nominal rate here is expressed as units of foreign currency per unit of domestic currency.)',
            'REER (real effective exchange rate): take the nominal effective rate — the currency\'s value against a weighted basket of partner currencies — and divide it by a price deflator or cost index. A rise in REER means exports become dearer and imports cheaper — a loss of trade competitiveness.'],
         'analogy': 'The nominal rate tells you how many dollars your rupees fetch; the real rate tells you how many burgers in New York your plate of biryani in Delhi is worth.',
         'work': 'Economists and treasury analysts track the REER to judge whether the rupee is over- or under-valued — an input into export pricing and hedging policy.'},
        {'id': 'c4', 'title': 'The foreign exchange market', 'body': [
            'The forex market is the worldwide network of banks, brokers and institutions that exchange currencies. It is over-the-counter — not a physical place but an electronically linked network with very narrow spreads. Because of arbitrage (risk-free profit from price differences between places), the rate for a currency tends to be the same in all centres at a given moment.',
            'Participants: commercial banks executing orders for exporters, importers, investment institutions, insurance and pension funds, hedgers and private investors, and trading on their own account; brokerage houses. Banks and brokers that quote their own prices are "market makers" (active players); passive players trade at those quotes — for trade payments, foreign investment, opening branches or joint ventures abroad, tourism, speculation and hedging.',
            'Spot market: current transactions with immediate delivery — settlement usually in about two days; the rate is the spot rate. Forward and futures markets: contracts today for delivery on a future date at the forward rate. A party who agrees to sell euros for dollars forward has "sold euros forward" and "bought dollars forward".',
            'Forward premium: forward rate above the spot rate; forward discount: forward rate below the spot rate. Futures do the same job as forwards but differ in settlement and delivery details.',
            'Most transactions, even between two non-US parties, go through the US dollar — the "vehicle currency".'],
         'analogy': 'The spot market is buying fruit at today\'s price and taking it home now; a forward is booking the same fruit today at a fixed price for delivery next month.',
         'work': 'Booking forward contracts to lock in the rupee value of export receivables or import payables is a routine treasury task; CAs account for them and assess hedge effectiveness.'},
        {'id': 'c5', 'title': 'Determination of the nominal exchange rate', 'body': [
            'Under a float, the external value of the currency is set by the demand for and supply of foreign exchange — demand for foreign exchange slopes down, supply slopes up, and the rate settles where the two curves cross.',
            'Demand for foreign currency (say dollars in India) arises to: pay for imports of goods and services; make unilateral transfers abroad (gifts, grants, donations); pay investment income abroad; buy foreign financial assets; open foreign bank accounts; acquire real capital abroad; and speculate or hedge.',
            'Supply of foreign currency comes from: foreigners buying our exports; unilateral transfers and remittances into the country; investment income received; inflows of FDI and portfolio investment; deposits placed here; and speculation.',
            'Changes: if demand for dollars rises (curve shifts right) with supply unchanged, the rupee price of the dollar rises — the rupee depreciates. If the supply of dollars rises (curve shifts right), the rupee price of the dollar falls — the rupee appreciates.'],
         'analogy': 'The dollar is a commodity in the Indian market: more buyers (importers) push its price up; more sellers (exporters, remitters, foreign investors) push it down.',
         'work': 'Forecasting the rupee for budgets means watching what drives dollar demand and supply — oil imports, FPI flows, remittances, export earnings.'},
        {'id': 'c6', 'title': 'Appreciation and depreciation; devaluation and revaluation', 'body': [
            'Appreciation: a currency\'s value rises against another currency or a basket; depreciation: it falls. When one currency depreciates against another, the other must appreciate against it.',
            'Home-currency depreciation (= foreign-currency appreciation): the home-currency price of the foreign currency rises (₹80 → ₹84 per $). Home-currency appreciation (= foreign-currency depreciation): the home-currency price of the foreign currency falls.',
            'Devaluation: a deliberate, official downward reset of the par value of a currency by the monetary authority under a fixed or nearly fixed regime. Revaluation: an official upward reset. Depreciation and appreciation, by contrast, are moves produced by demand and supply in the market when the rate floats — no policy decision is involved.'],
         'analogy': 'Depreciation is the tide going out on its own; devaluation is the authorities opening the sluice gates.',
         'work': 'Whether a move is market-driven or an official reset matters for disclosure of significant post-balance-sheet events and for revising foreign-currency budgets.'},
        {'id': 'c7', 'title': 'Effects of exchange rate changes on the economy', 'body': [
            'Depreciation of the home currency: exports become cheaper for foreigners and imports dearer at home; spending switches to domestic goods; demand for exports and import substitutes rises — an expansionary effect on output, provided the economy can supply more. Export-heavy and labour-intensive sectors gain jobs and wages.',
            'Costs of depreciation: higher consumer prices in the short run (imported goods, costlier imported inputs — cost-push inflation), so the central bank has little room to cut rates; possible strain on the current account if import payments rise faster than export earnings; higher burden for firms with unhedged ECBs and for governments with foreign-currency debt (India\'s share of public debt in foreign currency is small); harder forecasting and more hedging cost; nervous foreign investors — FDI and FPI inflows may shrink.',
            'Appreciation: exports dearer and imports cheaper → exports fall, imports rise, aggregate demand and growth may weaken; in a recession it deepens the slump, in a boom it cools inflation; cheaper imports lower costs and inflation and raise living standards; firms are pushed to innovate and cut costs; the current account may worsen (depending on price elasticities of exports and imports); loss of competitiveness is small if the appreciation reflects strong fundamentals.',
            'Example in the material: in late 2022 India and Russia agreed to settle trade in national currencies, and India permitted rupee settlement of international trade.'],
         'analogy': 'A weaker rupee is a discount sale for foreign buyers of Indian goods, and a price hike for Indians buying anything foreign.',
         'work': 'CAs model currency sensitivity for clients — how much margin moves with each rupee change — and advise on natural hedges and forward cover, especially for unhedged foreign borrowings.'},
    ]

    mcqs = [
        M('m1', 'A direct quote for an Indian resident is:', ['₹83.20 per US dollar', '$0.012 per rupee', '€0.92 per dollar', '¥150 per dollar'], 0, "A direct quote states how many units of local currency buy one unit of foreign currency; for an Indian resident, ₹83.20 per US dollar is direct. '$0.012 per rupee' is the trap — that is an indirect quote, with the rupee as the base. Euro and yen quotes against the dollar do not involve the rupee at all. In practice: RBI's reference rate and bank board rates in India are published as direct quotes, such as ₹ per USD.", 'c1', 'core', '83.2', topic='The Exchange Rate'),
        M('m2', 'In a direct quotation:', ['Foreign currency is the base; domestic currency is the counter', 'The domestic currency is the base currency', 'Both currencies are base currencies', 'Only a cross rate is quoted'], 0, "A direct quote fixes one unit of foreign currency as the base and expresses its price in domestic currency, the counter, whose amount varies. 'The domestic currency is the base' is the trap — that describes an indirect quote. In practice: an Indian importer reading 'USD/INR 83.20' understands it as ₹83.20 needed per dollar, the base currency being the dollar.", 'c1', topic='The Exchange Rate'),
        M('m3', 'If $1 = ₹80, the indirect quote for an Indian resident is $___ per rupee:', ['0.0125', '80', '0.125', '1.25'], 0, 'The indirect quote is the reciprocal of the direct quote: 1 ÷ 80 = $0.0125 per rupee. The tempting 80 is the direct quote itself; 0.125 and 1.25 misplace the decimal point. In practice: foreign buyers of Indian goods sometimes think in indirect terms — how many dollars one rupee costs — so treasury staff must convert between the two quickly.', 'c1', 'moderate', '1/80', topic='The Exchange Rate'),
        M('m4', 'If $1 = ₹84 and €1 = $1.05, the rupee–euro cross rate (₹ per €) is:', ['88.2', '80', '84', '79.05'], 0, '₹ per € = (₹ per $) × ($ per €) = 84 × 1.05 = ₹88.20 per euro. The tempting 80 divides 84 by 1.05 instead of multiplying; 84 ignores the euro–dollar rate. Check: since a euro is worth more than a dollar, it must cost more than ₹84. In practice: Indian banks derive rupee–euro and rupee–yen rates through the dollar in exactly this way.', 'c1', 'moderate', '84*1.05', topic='The Exchange Rate'),
        M('m5', 'A rate between two currencies derived from their rates against a third currency is a:', ['Cross rate', 'Spot rate', 'Forward rate', 'Real exchange rate'], 0, "A cross rate is the exchange rate between two currencies derived from each one's rate against a third currency, usually the US dollar. 'Spot rate' is the trap: it refers to the timing of settlement, not how the rate is derived. In practice: the rupee–dirham rate an Indian exporter to the UAE receives is typically derived as a cross rate through the dollar.", 'c1', topic='The Exchange Rate'),
        M('m6', 'Under a free-floating exchange rate regime:', ['The rate is determined by market demand and supply without central-bank intervention', 'The government fixes the rate against gold', 'The central bank frequently buys and sells to hold a band', 'The rate never changes'], 0, "Under a free float, the exchange rate is set by market demand and supply of currencies, with no central-bank intervention to target a level. 'The central bank frequently buys and sells to hold a band' is the trap — that describes a managed float or a peg. In practice: few countries float completely freely; India follows a managed float, where RBI intervenes only to curb excessive volatility.", 'c2', topic='The Exchange Rate Regimes'),
        M('m7', 'The greatest advantage of a floating exchange rate is that it:', ['Allows the central bank to pursue an independent monetary policy', 'Eliminates exchange rate risk', 'Requires large foreign exchange reserves', 'Prevents all speculation'], 0, "With a floating rate, the central bank does not have to use interest rates or reserves to defend a fixed parity, so it can run an independent monetary policy aimed at domestic goals like inflation. 'Eliminates exchange rate risk' is the trap — that is an advantage of a fixed rate, not a floating one. In practice: RBI's flexible inflation targeting depends on not having to defend a fixed rupee rate.", 'c2', topic='The Exchange Rate Regimes'),
        M('m8', 'The main disadvantage of a flexible exchange rate is:', ['Volatility and uncertainty in international transactions', 'Need for huge reserves', 'Loss of monetary independence', 'It cannot absorb external shocks'], 0, "Flexible exchange rates can swing sharply, creating uncertainty for exporters, importers and investors, who must bear or hedge currency risk. 'Need for huge reserves' is the trap: that is a drawback of fixed rates, which must be defended. In practice: Indian exporters and importers use forward contracts and options to protect margins from rupee volatility.", 'c2', topic='The Exchange Rate Regimes'),
        M('m9', 'Which is an advantage of a fixed exchange rate?', ['It imposes discipline on the monetary authority, tending to lower inflation', 'It lets the central bank ignore reserves', 'It gives maximum policy flexibility', 'It allows the exchange rate to be used freely as a policy tool'], 0, "A fixed exchange rate disciplines the monetary authority: it cannot print money freely without threatening the peg, so inflation tends to stay lower. 'It gives maximum policy flexibility' is the trap — a fixed rate does the opposite, limiting monetary independence and requiring reserves. In practice: the UAE dirham's peg to the US dollar ties UAE monetary policy closely to the US Federal Reserve's decisions.", 'c2', topic='The Exchange Rate Regimes'),
        M('m10', 'Government or central-bank buying and selling of its own currency within a floating system is called:', ['A managed float', 'A hard peg', 'Devaluation', 'A free float'], 0, "In a managed float, the exchange rate is broadly market-determined, but the central bank buys or sells currencies to prevent sudden large swings. 'A hard peg' is the trap — it fixes the rate rigidly. Devaluation is an official cut in a fixed parity. In practice: RBI sells dollars when the rupee falls sharply and buys dollars when inflows push it up too fast, which is how India's managed float works.", 'c2', topic='The Exchange Rate Regimes'),
        M('m11', 'Trade flows are affected mainly by:', ['Real exchange rates', 'Nominal exchange rates alone', 'Cross rates', 'Forward rates'], 0, "Trade decisions depend on what a currency can actually buy, so real exchange rates — nominal rates adjusted for relative prices — matter most for exports and imports. 'Nominal exchange rates alone' is the trap: if Indian prices rise faster than foreign prices, a stable nominal rupee still makes exports dearer. In practice: exporters' associations track the real effective exchange rate to judge their competitiveness.", 'c3', topic='Nominal Versus Real Exchange Rates'),
        M('m12', 'Real exchange rate equals (nominal rate expressed as foreign currency per unit of domestic currency):', ['Nominal rate × domestic price index ÷ foreign price index', 'Nominal rate × foreign price index ÷ domestic price index', 'Domestic price ÷ foreign price only', 'Nominal rate ÷ domestic price'], 0, "With the nominal rate expressed as foreign currency per unit of domestic currency, real exchange rate = nominal rate × domestic price index ÷ foreign price index. The trap swaps the price indices, which would apply if the nominal rate were quoted the other way round. In practice: RBI publishes REER indices built on this logic, using price indices and trade weights for India's major partners.", 'c3', topic='Nominal Versus Real Exchange Rates'),
        M('m13', 'A shirt costs ₹1,200 in India and $24 in the USA; $1 = ₹80. India\'s real exchange rate for shirts (nominal rate in $ per ₹) is:', ['0.625', '1.6', '15', '50'], 0, 'Nominal rate in $ per ₹ = 1 ÷ 80. Real rate = (1 ÷ 80) × 1,200 ÷ 24 = 15 ÷ 24 = 0.625, so one Indian shirt trades for 0.625 US shirts — Indian shirts are relatively cheap. The tempting 1.6 is the reciprocal; 15 is the dollar price of the Indian shirt; 50 is the ratio of prices ignoring the exchange rate. In practice: analysts compare such price-adjusted rates to assess export competitiveness.', 'c3', 'hard', '(1/80)*1200/24', topic='Nominal Versus Real Exchange Rates'),
        M('m14', 'An increase in a country\'s REER indicates:', ['A loss of trade competitiveness', 'A gain in competitiveness', 'Cheaper exports', 'Dearer imports'], 0, "A rise in the real effective exchange rate means the home currency has become stronger in real terms against trading partners, so exports become dearer and imports cheaper — a loss of trade competitiveness. 'A gain in competitiveness' is the trap, which reverses the meaning. In practice: RBI watches the REER for rupee overvaluation, which can hurt exporters such as textile and engineering firms.", 'c3', topic='Nominal Versus Real Exchange Rates'),
        M('m15', 'Banks and brokers that quote their own buying and selling prices in the forex market are called:', ['Market makers', 'Passive players', 'Hedgers', 'Arbitrageurs'], 0, "Market makers — large banks and dealers — continuously quote their own buying (bid) and selling (ask) prices, standing ready to trade and earning the spread. 'Passive players' is the trap: they trade at the quotes market makers set. In practice: when an Indian corporate treasurer calls a bank's dealing room for a dollar rate, the bank is acting as a market maker.", 'c4', topic='The Foreign Exchange Market'),
        M('m16', 'Spot foreign exchange transactions are generally settled in about:', ['Two days', 'Two months', 'One year', 'The same minute'], 0, "Spot foreign-exchange transactions are generally settled within about two business days of the trade. 'Two months' is the trap — that would be a forward contract, settled on a specified future date. In practice: when an Indian importer books a spot deal to pay a supplier, the rupees are debited and dollars credited about two working days later.", 'c4', topic='The Foreign Exchange Market'),
        M('m17', 'When the forward rate is higher than the spot rate, the currency is at a:', ['Forward premium', 'Forward discount', 'Par', 'Cross rate'], 0, "When the forward rate for a currency is higher than its spot rate, that currency is at a forward premium — it costs more to buy for future delivery. 'Forward discount' is the trap: that applies when the forward rate is lower than spot. In practice: the US dollar usually trades at a forward premium against the rupee because Indian interest rates are higher than US rates.", 'c4', topic='The Foreign Exchange Market'),
        M('m18', 'Spot $1 = ₹82; 6-month forward $1 = ₹83.23. The forward premium on the dollar (not annualised) is:', ['1.5%', '3%', '1.23%', '0.5%'], 0, 'Forward premium = (forward − spot) ÷ spot × 100 = (83.23 − 82) ÷ 82 × 100 = 1.23 ÷ 82 × 100 = 1.5% for six months. The tempting 3% is the annualised figure; 1.23% confuses the rupee difference with a percentage. In practice: exporters compare this premium with interest-rate differences when deciding whether to sell their dollar receivables forward.', 'c4', 'moderate', '(83.23-82)/82*100', topic='The Foreign Exchange Market'),
        M('m19', 'The US dollar is often called a "vehicle currency" because:', ['Most forex deals pass through it even when neither party is American', 'It is always fixed', 'It is used only for car imports', 'It is the cheapest currency'], 0, "The US dollar is a vehicle currency because most foreign-exchange deals are routed through it, even when neither party is American — for example, rupee-to-peso trades often pass through the dollar. 'It is always fixed' is the trap: the dollar floats. In practice: most of India's trade invoicing is in US dollars, even for trade with non-US partners.", 'c4', topic='The Foreign Exchange Market'),
        M('m20', 'Making riskless profit from price differences of the same currency in different markets is:', ['Arbitrage', 'Hedging', 'Speculation', 'Dumping'], 0, "Arbitrage is buying a currency where it is cheaper and simultaneously selling it where it is dearer to lock in a riskless profit; it keeps rates consistent across centres. 'Speculation' is the trap — speculation takes risk by betting on future movements. Hedging reduces existing risk. In practice: arbitrage between onshore Indian and offshore NDF markets helps keep rupee rates aligned.", 'c4', topic='The Foreign Exchange Market'),
        M('m21', 'Which ought to cause Country X\'s currency to appreciate against the dollar?', ['A rise in remittances from its workers abroad', 'Increased imports by its consumers', 'Repayment of its foreign debts', 'The US deciding not to import from X'], 0, "Higher remittances from workers abroad bring more dollars into Country X; they are converted into home currency, increasing the supply of dollars, so the home currency appreciates. 'Increased imports by its consumers' is the trap — imports raise demand for dollars and weaken the home currency. In practice: India, the world's largest remittance recipient, gets significant support for the rupee from inflows from the Gulf and the US.", 'c5', 'moderate', topic='Changes in Exchange Rates'),
        M('m22', 'Indian consumers develop a taste for US goods and buy more. Other things equal:', ['The demand curve for dollars shifts right and the rupee depreciates', 'The demand curve for dollars shifts right and the rupee appreciates', 'The supply of dollars shrinks and import prices fall', 'The demand curve for dollars shifts left'], 0, "Buying more US goods means Indian importers need more dollars, so the demand curve for dollars shifts right; the rupee price of a dollar rises, meaning the rupee depreciates. 'Shifts right and the rupee appreciates' is the trap — more demand for dollars makes them dearer, not cheaper. In practice: surges in India's oil or gold imports often coincide with rupee weakness.", 'c5', 'moderate', topic='Changes in Exchange Rates'),
        M('m23', 'A large FDI inflow into India, other things equal, will:', ['Increase the supply of dollars and appreciate the rupee', 'Increase demand for dollars and depreciate the rupee', 'Leave the rupee unchanged under a float', 'Shift the demand curve for dollars left only'], 0, "Foreign investors bringing FDI into India sell dollars to buy rupees, increasing the supply of dollars in the forex market, so the rupee appreciates. 'Increase demand for dollars and depreciate the rupee' is the trap, reversing the direction. In practice: large FDI or FPI inflows push the rupee up, and RBI often buys dollars to prevent excessive appreciation and build reserves.", 'c5', topic='Changes in Exchange Rates'),
        M('m24', 'The rupee moves from ₹75 to ₹78 per dollar. The dollar has appreciated by:', ['4%', '3.85%', '3%', '2.5%'], 0, "The dollar's appreciation is measured in rupees: (78 − 75) ÷ 75 × 100 = 3 ÷ 75 × 100 = 4%. The tempting 3.85% is the rupee's depreciation measured in dollar terms; 3% confuses the ₹3 change with a percentage. In practice: business news reports the rupee moving from ₹75 to ₹78 as a 4% rise in the dollar, which exporters translate into higher rupee receipts.", 'c6', 'moderate', '(78-75)/75*100', topic='Changes in Exchange Rates'),
        M('m25', 'The rupee moves from ₹75 to ₹78 per dollar. The rupee has depreciated (in dollar terms) by approximately:', ['3.85%', '4%', '3%', '4.17%'], 0, "In dollar terms, one rupee fell from 1/75 to 1/78 dollars: change = (1/78 − 1/75) ÷ (1/75) = 75/78 − 1 ≈ −3.85%. The tempting 4% is the dollar's appreciation measured in rupees — the two percentages differ because the base differs. In practice: CFOs must be clear which currency is the base when reporting currency movements to boards and investors.", 'c6', 'hard', 'round((1-75/78)*100, 2)', topic='Changes in Exchange Rates'),
        M('m26', 'A deliberate official reduction in the par value of a currency under a fixed regime is:', ['Devaluation', 'Depreciation', 'Appreciation', 'Revaluation'], 0, "Devaluation is a deliberate, official reduction in a currency's par value under a fixed exchange rate regime. 'Depreciation' is the trap: depreciation is a market-driven fall under a floating regime. In practice: India devalued the rupee officially in 1966 and in July 1991; today's rupee moves are depreciation or appreciation under a managed float.", 'c6', topic='Devaluation (Revaluation) vs Depreciation (Appreciation)'),
        M('m27', 'Revaluation refers to:', ['An official increase in the fixed par value of a currency', 'A market-driven rise in a currency', 'A fall in the real exchange rate', 'A forward premium'], 0, "Revaluation is an official increase in the fixed par value of a currency under a fixed regime. 'A market-driven rise in a currency' is the trap — that is appreciation under a float. In practice: China revalued the yuan against the dollar in 2005 by official decision, a classic revaluation cited in trade discussions.", 'c6', topic='Devaluation (Revaluation) vs Depreciation (Appreciation)'),
        M('m28', 'Depreciation of the home currency is likely to:', ['Make exports cheaper and imports dearer', 'Make imports cheaper', 'Reduce the burden of foreign-currency loans', 'Lower domestic consumer prices'], 0, "When the home currency depreciates, foreign buyers need less of their currency to buy home goods, so exports become cheaper abroad, while imports cost more in home currency. 'Make imports cheaper' is the trap — that follows appreciation. Depreciation also raises the burden of foreign-currency loans. In practice: a weaker rupee helps Indian IT and textile exporters but raises costs for oil and electronics importers.", 'c7', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m29', 'An exporter has receivables of $40,000. The rupee depreciates from ₹82 to ₹85 per dollar. The exporter\'s gain is:', ['₹1,20,000', '₹3,40,000', '₹32,80,000', '₹34,00,000'], 0, "The exporter receives $40,000. Gain = 40,000 × (85 − 82) = 40,000 × 3 = ₹1,20,000. The tempting ₹34,00,000 and ₹32,80,000 are the full rupee values at ₹85 and ₹82, not the gain. In practice: Indian exporters' CAs record such foreign-exchange gains on restatement of receivables under Ind AS 21 or AS 11.", 'c7', 'moderate', '40000*(85-82)', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m30', 'A firm has an unhedged ECB of $5,00,000. If the rupee depreciates from ₹80 to ₹83, its repayment burden rises by:', ['₹15,00,000', '₹4,00,00,000', '₹4,15,00,000', '₹1,50,000'], 0, "The firm owes $5,00,000. Extra repayment burden = 5,00,000 × (83 − 80) = 5,00,000 × 3 = ₹15,00,000. Traps: ₹4,00,00,000 and ₹4,15,00,000 are the total rupee liabilities at ₹80 and ₹83; ₹1,50,000 misplaces a zero. In practice: RBI's ECB rules require hedging for certain categories of borrowers, and auditors flag large unhedged ECBs as a risk.", 'c7', 'moderate', '500000*3', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m31', 'Which is NOT a likely effect of currency appreciation?', ['A rise in exports', 'Cheaper imports', 'Lower inflation', 'Pressure on firms to cut costs and innovate'], 0, "Appreciation makes a country's goods dearer for foreign buyers, so exports tend to fall, not rise. Cheaper imports, lower inflation and pressure on firms to cut costs and innovate are genuine effects. 'Lower inflation' is tempting to reject, but cheaper imported goods and inputs do reduce price pressure. In practice: when the rupee strengthens, Indian exporters often lobby for support while importers enjoy lower costs.", 'c7', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m32', 'Appreciation during a recession is likely to:', ['Further reduce aggregate demand and raise unemployment', 'Cure the recession', 'Increase exports', 'Raise inflation'], 0, "Appreciation makes exports dearer and imports cheaper, reducing net exports and aggregate demand. In a recession, when demand is already weak, this deepens the slump and raises unemployment. 'Cure the recession' is the trap — appreciation is helpful in a boom, where it cools inflation, not in a recession. In practice: export-oriented economies resist currency appreciation during slowdowns.", 'c7', 'moderate', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m33', 'Depreciation may add to inflation mainly because:', ['Imported goods and inputs become costlier', 'Exports become cheaper', 'Foreign investors buy more', 'Interest rates must fall'], 0, "Depreciation raises the home-currency prices of imported goods directly and also increases costs for firms using imported inputs such as crude oil and components, creating cost-push inflation. 'Exports become cheaper' is the trap: that is true, but it is not the main reason for inflation. In practice: RBI factors in rupee depreciation when forecasting inflation, because India imports most of its crude oil.", 'c7', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
        M('m34', 'A foreign tourist converts $20 when $1 = ₹82 and again after the rupee moves to ₹86. How many more rupees does she get?', ['₹80', '₹1,640', '₹1,720', '₹4'], 0, 'Extra rupees = 20 × (86 − 82) = 20 × 4 = ₹80. Traps: ₹1,640 and ₹1,720 are the total rupees at ₹82 and ₹86; ₹4 is the per-dollar change only. In practice: a weaker rupee makes India cheaper for foreign tourists, which is one way depreciation supports the tourism and hospitality sector.', 'c7', 'core', '20*(86-82)', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
    ]

    cq1 = Checks()
    a1 = cq1.add('(86-80)/80*100', 'dollar appreciation %')
    a2 = cq1.add('round((80/86-1)*100, 2)', 'rupee depreciation %')
    a3 = cq1.add('25000*86-25000*80', 'importer: extra rupees on $25,000')
    a4 = cq1.add('60000*86-60000*80', 'exporter: extra rupees on $60,000')
    q1 = Q('q1', 5, 'moderate', 'table', 'The rupee moves from ₹80 to ₹86 per dollar. (a) Which currency appreciated? Compute the dollar\'s appreciation and the rupee\'s depreciation in percentage terms. (b) Compute the effect on an importer paying $25,000 and an exporter receiving $60,000.',
           [table(['Item', 'Working', 'Result'], [['Dollar appreciation', '(86 − 80) ÷ 80 × 100', f'{fx(a1)}%'], ['Rupee depreciation', '(80 ÷ 86 − 1) × 100', f'{fx(a2)}%'],
                                                  ['Importer — extra cost', '25,000 × (86 − 80)', R(a3)], ['Exporter — extra receipts', '60,000 × (86 − 80)', R(a4)]])],
           [S('s1', 'Identifies dollar appreciation / rupee depreciation', 1, 'concept'), S('s2', 'Dollar appreciation %', 1, 'computation'), S('s3', 'Rupee depreciation % on the correct base', 1, 'computation'),
            S('s4', 'Importer effect', 1, 'computation'), S('s5', 'Exporter effect', 1, 'computation')],
           ['Most lose a mark by stating the rupee also fell 7.5%.'], ['Using the same percentage for both currencies.', 'Saying the importer gains.'], ['Measure each currency\'s change in the other currency per unit of it.'], checks=cq1)

    cq2 = Checks()
    r1 = cq2.add('(1/80)*400/8*1000', 'RER for the good (India view) × 1,000 — RER = 0.625')
    r2 = cq2.add('(1/80)*130/120*10000', 'RER with indices (India view) × 10,000 — RER ≈ 0.0135')
    q2 = Q('q2', 4, 'hard', 'table', 'A cricket ball costs ₹400 in India and $8 in the USA; $1 = ₹80. (a) Compute India\'s real exchange rate for the ball (nominal rate in $ per ₹) and interpret it. (b) If India\'s price index rises to 130 while the foreign index is 120 and the nominal rate stays at $1 = ₹80, compute the real exchange rate and say whether India\'s competitiveness improved or worsened compared with equal price levels.',
           [table(['Step', 'Working', 'Result'], [['(a) RER', '(1/80) × 400 ÷ 8', '0.625'], ['(a) Meaning', 'Indian ball in $ = 400 ÷ 80 = $5 vs $8 abroad', '1 Indian ball = 0.625 foreign balls — Indian goods relatively cheap'],
                                                  ['(b) RER with indices', '(1/80) × 130 ÷ 120 = 0.0125 × 1.0833', '≈ 0.0135'], ['(b) Comparison', 'Equal indices would give 0.0125; now higher (by about 8.3%)', 'Real appreciation → competitiveness worsened']])],
           [S('s1', 'Correct formula and nominal rate form', 1, 'concept'), S('s2', 'RER for the good', 1, 'computation'), S('s3', 'RER with price indices', 1, 'computation'), S('s4', 'Interpretation of competitiveness', 1, 'conclusion')],
           ['Candidates often flip the nominal rate (using 80 instead of 1/80) with this formula.'], ['Ignoring the price levels.', 'Saying higher domestic prices improve competitiveness.'], ['State the unit of the nominal rate before using it.'], checks=cq2)

    q3 = Q('q3', 4, 'core', 'table', 'Distinguish between devaluation and depreciation of a currency.',
           [table(['Basis', 'Devaluation', 'Depreciation'], [
               ['Cause', 'Deliberate official decision of the government / central bank', 'Demand and supply in the market'],
               ['Regime', 'Fixed or nearly fixed (pegged) exchange rate', 'Floating exchange rate'],
               ['Nature', 'A discrete reset of the par value to a new fixed level', 'Gradual, continuous movement'],
               ['Opposite', 'Revaluation', 'Appreciation'],
           ])],
           [S('s1', 'Cause: policy vs market', 1, 'concept'), S('s2', 'Regime: fixed vs floating', 1, 'concept'), S('s3', 'Nature of change', 1, 'analysis'), S('s4', 'Opposites named', 1, 'concept')],
           ['A four-row table earns full marks.'], ['Using the two terms interchangeably.'], ['Remember: DEValuation = DEcision; dePRECIATION = PRICE forces.'])

    jobs = [
        {'id': 'j1', 'title': 'Hedging an import payable', 'role': 'CA in industry (treasury, pharma importer)',
         'situation': 'You must pay $2,00,000 for raw material in three months. Spot is ₹83.00; the 3-month forward is ₹83.50. Management fears the rupee may fall to ₹85.',
         'steps': ['Quantify the exposure: each ₹1 move changes the payment by ₹2,00,000.', 'Compare: forward cover fixes the cost at 2,00,000 × 83.50; unhedged it could be 2,00,000 × 85.', 'Book the forward if the policy is to remove uncertainty; record it as a derivative in the books.', 'Report the hedged cost to the costing team for pricing.'],
         'takeaway': 'Forward cover converts an uncertain rupee cost into a known one; the forward premium is the price of certainty.',
         'think': 'What is the saving from the forward if the rupee does fall to ₹85?', 'answer': '2,00,000 × (85 − 83.50) = ₹3,00,000 saved compared with staying unhedged.',
         'checks': Checks([{'expr': '200000*(85-83.5)', 'value': 300000, 'label': 'saving from forward cover'}])},
        {'id': 'j2', 'title': 'Currency risk in a lending appraisal', 'role': 'CA in a bank\'s credit team',
         'situation': 'A borrower has a large unhedged foreign-currency loan and sells only in India.',
         'steps': ['Compute the rupee cost of the loan at current and stressed exchange rates.', 'Check debt-service coverage under depreciation scenarios.', 'Insist on a hedging policy or a natural hedge (export receipts).', 'Flag the risk in the credit note.'],
         'takeaway': 'Depreciation silently raises the debt burden of unhedged foreign borrowers — a key credit risk.'},
    ]

    dq = ALT('direct {l} per {f}', 'direct quot {l} per {f}', 'direct {l} 1 {f}', 'direct quot {l} 1 {f}', 'direct quot unit {l} 1 {f}', 'direct quot number {l} 1 {f}', 'direct quot {l} for 1 {f}', 'direct {l} for every {f}', 'direct quot price {f} {l}', 'direct quot {l} need buy 1 {f}', 'direct quot how many {l} 1 {f}', 'direct quot many {l} 1 {f}', l=LOC, f=FOR)
    iq = ALT('indirect {f} per {l}', 'indirect quot {f} per {l}', 'indirect {f} 1 {l}', 'indirect quot {f} 1 {l}', 'indirect quot unit {f} 1 {l}', 'indirect quot number {f} 1 {l}', 'indirect quot {f} for 1 {l}', 'indirect quot how many {f} 1 {l}', 'indirect quot many {f} 1 {l}', f=FOR, l=LOC)
    viva = [
        V('v1', 'Explain a direct quote and an indirect quote with an example.',
          'A direct quote is the number of units of local currency for one unit of foreign currency, for example 83 rupees per dollar for an Indian. An indirect quote is the number of units of foreign currency per one unit of local currency, for example about 0.012 dollars per rupee. One is the reciprocal of the other.',
          [P('p1', 'Direct quote = units of local currency per one unit of foreign currency', 4, dq),
           P('p2', 'Indirect quote = units of foreign currency per unit of local currency', 4, iq + '|reciprocal|inverse|1 divid|one divid|divide 1|divid 1|opposite way'),
           P('p3', 'An example (e.g. ₹83 per $ / $0.012 per ₹)', 2, '83|84|80|0.012|example|instance|rupe per dollar|dollar per rupe|euro|pound|yen')], 'c1'),
        V('v2', 'What does it mean when the rupee depreciates against the dollar, and who gains and who loses?',
          'Rupee depreciation means more rupees are needed to buy one dollar, for example the rate moving from 80 to 84 rupees per dollar, so the rupee loses value and the dollar appreciates. Exporters gain because their dollar earnings convert into more rupees, while importers lose because they pay more rupees for the same imports.',
          [P('p1', 'More rupees needed per dollar — rupee loses value', 4, 'more rupe|rupee lose value|rupee less valuabl|rupee weaken|rupee fall|rupee declin|value of rupee fall|value of rupee declin|value of rupee go down|rupee value fall|rupee becom weak|rupee becomes weaker|lose value|loses value|less valuabl|weaker rupee|80 to 84|80 84'),
           P('p2', 'The dollar simultaneously appreciates', 2, 'dollar apprecia|dollar strengthen|dollar gain|dollar rise|dollar becom strong|stronger dollar|dollar more valuabl|appreciat'),
           P('p3', 'Exporters gain; importers lose', 4, 'exporter gain|exporter benefit|exporters are better|exporter better|export cheaper|exports become cheaper|exporter get more|exporter earn more|exporter receiv more|good for exporter|exporter happy|exporter profit|benefit exporter|help exporter|favour exporter',
             'importer lose|importer pay more|importer suffer|import costl|import dearer|import expensive|imports become costlier|importer worse|bad for importer|hurt importer|importer hurt|importers are worse|import more expensive|importer hit')], 'c6'),
        V('v3', 'What is a floating exchange rate regime, and what are its main advantage and disadvantage?',
          'Under a floating exchange rate regime the exchange rate is determined by market demand and supply of foreign exchange, without the central bank intervening. Its main advantage is that the central bank can follow an independent monetary policy and does not need large reserves. Its main disadvantage is volatility, which creates uncertainty and risk in international transactions.',
          [P('p1', 'Rate set by market demand and supply, no central-bank intervention', 4, 'demand and supply|supply and demand|market force|market determin|market decid|determined by the market|set by the market|by market|market', 'no intervent|without intervent|not intervene|doesn t intervene|no central bank|without central bank|no government|without government|free|freely|not fix|not set by government|not controlled|no control', min=1),
           P('p2', 'Advantage: independent monetary policy / no need for big reserves / shock absorber', 3, 'independent monetary|monetary independ|own monetary|monetary policy|no need reserv|not need reserv|less reserv|no reserv|without reserv|shock absorb|buffer|self correct|self regulat|policy tool|flexib'),
           P('p3', 'Disadvantage: volatility, uncertainty, risk', 3, 'volatil|uncertain|unpredictab|risk|fluctuat|instabil|unstable')], 'c2'),
        V('v4', 'How is devaluation different from depreciation?',
          'Devaluation is a deliberate official reduction in the value of a currency by the government or central bank under a fixed or pegged exchange rate. Depreciation is a fall in the value of a currency caused by the market, that is by demand and supply, when the exchange rate floats. The opposites are revaluation and appreciation.',
          [P('p1', 'Devaluation: deliberate, official, by government/central bank under a fixed regime', 4,
             ALT('{d} {x}', '{d} reduc value {x}', '{d} lower value {x}', '{d} cut value {x}', '{d} fall value {x}', '{d} reduc {x}', '{d} mean {x}', '{d} done {x}', '{d} happen {x}', '{d} occur {x}', '{d} when {x}', '{d} decid {x}', d=('devalu',), x=('deliberat', 'official', 'government', 'central bank', 'policy', 'authorit', 'announc', 'decision', 'decid', 'fix', 'peg', 'intention', 'purpos', 'rbi', 'reserve bank', 'state'))
             + '|' + ALT('{x} devalu', '{x} reduc devalu', x=('official', 'deliberat', 'government', 'central bank', 'policy'))),
           P('p2', 'Depreciation: caused by market demand and supply when the rate floats', 4,
             ALT('{d} {x}', '{d} fall value {x}', '{d} decreas value {x}', '{d} declin value {x}', '{d} drop value {x}', '{d} fall {x}', '{d} mean {x}', '{d} due {x}', '{d} happen {x}', '{d} occur {x}', '{d} result {x}', '{d} caus {x}', '{d} when {x}', '{d} driven {x}', '{d} because {x}', d=('depreci',), x=('market', 'demand', 'supply', 'float', 'flexib', 'automatic', 'natural', 'own'))
             + '|' + ALT('{x} depreci', x=('market driven', 'market force', 'market caus', 'demand supply', 'supply demand'))),
           P('p3', 'Opposites: revaluation and appreciation', 2, 'revalu|apprecia|opposite')], 'c6'),
        V('v5', 'What are the effects of a depreciation of the domestic currency on the economy?',
          'Depreciation makes exports cheaper for foreigners and imports dearer at home, so exports and import-competing output rise and the effect is expansionary. But it can raise inflation through costlier imports and inputs, increases the burden of unhedged foreign borrowings and foreign debt, and may make foreign investors cautious.',
          [P('p1', 'Exports cheaper / rise; imports dearer / fall', 4, 'export cheaper|exports become cheaper|exports rise|export increas|more export|boost export|increas export|raise export|exports grow|export competit|exports more competitive|exports go up|helps export|exporters gain',
             'reduc import|cut import|fewer imports|less import|lower import|discourag import|imports decline|import dearer|import costl|import expensive|imports become costlier|imports fall|import declin|fewer import|import reduc|imports more expensive|imports go down|importers lose|import price ris|import price go up|import cost more'),
           P('p2', 'Expansionary — output and employment rise', 2, 'expansion|output ris|output increas|growth|employment|jobs|aggregate demand|economic activ|gdp'),
           P('p3', 'Inflation from costlier imports/inputs', 2, 'inflation|price ris|prices rise|cost push|price go up|prices go up|price level|costlier input|dearer input'),
           P('p4', 'Higher burden of unhedged foreign borrowings / debt; investor caution', 2, 'ecb|external commercial|foreign loan|foreign debt|foreign borrow|debt burden|repay|borrow|investor|capital outflow|fdi|fpi|hedg')], 'c7'),
        V('v6', 'What is the real exchange rate and why does it matter more than the nominal rate for trade?',
          'The real exchange rate is the rate at which the goods and services of one country can be exchanged for those of another. It equals the nominal exchange rate multiplied by the ratio of domestic to foreign prices. It matters more for trade because buyers care about what the currency can actually buy, so the real rate determines net exports and competitiveness.',
          [P('p1', 'Rate at which goods of one country trade for goods of another', 4, 'good|goods and servic|product|basket|purchas power|what it can buy|what money can buy|real term|in terms of goods', 'another country|other country|foreign|abroad|two countr|countries|one country', min=2),
           P('p2', 'Nominal rate × domestic price ÷ foreign price (price indices)', 4, 'nominal', 'price|price index|price level|inflation|prices', min=2),
           P('p3', 'It determines net exports / competitiveness', 2, 'net export|competitiv|trade flow|exports and imports|export|trade balance|what buyers care|buyer care|purchas power')], 'c3'),
        V('v7', 'Explain spot and forward transactions in the foreign exchange market, and forward premium and discount.',
          'A spot transaction is for immediate delivery of currency, usually settled in about two days at the spot rate. A forward transaction is a contract made today to buy or sell a currency on a specified future date at an agreed forward rate. If the forward rate is higher than the spot rate the currency is at a forward premium, and if the forward rate is lower than the spot rate it is at a forward discount.',
          [P('p1', 'Spot = immediate delivery, settled in about two days', 2, 'spot', 'immediate|now|today|current|two day|2 day|right away|at once|prompt', min=2),
           P('p2', 'Forward = contract now for delivery on a future date at an agreed rate', 2, 'forward', 'future|later|specified date|fixed date|agreed rate|lock|in advance|next month|three month|months', min=2),
           P('p3', 'Forward premium: forward rate above spot', 3, ALT('{p} forward {h} spot', '{p} when forward {h} spot', '{p} if forward {h} spot', 'forward {h} spot {p}', 'forward rate {h} spot rate {p}', '{p} forward rate {h} spot', p=('premium',), h=HI)),
           P('p4', 'Forward discount: forward rate below spot', 3, ALT('{d} forward {l} spot', '{d} when forward {l} spot', '{d} if forward {l} spot', 'forward {l} spot {d}', 'forward rate {l} spot rate {d}', '{d} forward rate {l} spot', 'forward {l} {d}', d=('discount',), l=LO))], 'c4'),
    ]

    case = {'id': 'k1', 'title': 'Kaveri Textiles faces a weaker rupee', 'difficulty': 'hard',
            'case': ('Kaveri Textiles exports garments worth $3,00,000 a quarter and imports dyes worth $1,20,000 a quarter. It also has an unhedged ECB of $10,00,000. Over the quarter the rupee moves from ₹82 to ₹86 per dollar, mainly because Indian oil imports surged. '
                     'The finance head notes that India\'s REER has risen over the past year even though the nominal rupee has weakened, because Indian inflation was higher than in partner countries.'),
            'mcqs': [
                M('k1a', 'What is the net quarterly gain on trade flows (exports less imports) from the rupee move?', ['₹7,20,000', '₹12,00,000', '₹4,80,000', '₹16,80,000'], 0, 'Export gain = 3,00,000 × (86 − 82) = ₹12,00,000; import cost increase = 1,20,000 × 4 = ₹4,80,000; net gain = 12,00,000 − 4,80,000 = ₹7,20,000. Traps: ₹12,00,000 ignores the dearer imports; ₹4,80,000 is only the import cost; ₹16,80,000 adds both. In practice: firms with both exports and imports have a natural hedge, so only the net exposure matters.', 'c7', 'hard', '(300000-120000)*(86-82)', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
                M('k1b', 'By how much does the rupee value of the ECB rise?', ['₹40,00,000', '₹4,00,000', '₹8,60,00,000', '₹8,20,00,000'], 0, "Rise in the rupee value of the loan = 10,00,000 × (86 − 82) = ₹40,00,000. Traps: ₹8,60,00,000 and ₹8,20,00,000 are the full liabilities at ₹86 and ₹82; ₹4,00,000 misplaces a zero. This loss of ₹40 lakh more than wipes out the quarterly trade gain of ₹7.2 lakh. In practice: Kaveri's finance head should consider hedging the ECB with forwards or swaps.", 'c7', 'moderate', '1000000*(86-82)', topic='Impacts of Exchange Rate Fluctuations on Domestic Economy'),
                M('k1c', 'Surging oil imports weakened the rupee because they:', ['Raised the demand for dollars, shifting the demand curve to the right', 'Raised the supply of dollars', 'Shifted the demand for dollars to the left', 'Forced an official devaluation'], 0, "Oil importers must buy dollars to pay for crude, so a surge in oil imports raises the demand for dollars, shifting the demand curve right and raising the rupee price of the dollar — the rupee weakens. 'Raised the supply of dollars' is the trap, reversing the effect. In practice: oil marketing companies' dollar purchases are a major source of daily dollar demand in India's forex market.", 'c5', 'moderate', topic='Changes in Exchange Rates'),
                M('k1d', 'The rupee\'s fall here is best described as:', ['Depreciation', 'Devaluation', 'Revaluation', 'Appreciation'], 0, "The rupee fell because of market forces — higher demand for dollars from oil importers — under India's managed float, so this is depreciation. 'Devaluation' is the trap: devaluation is an official cut in a fixed par value, which India does not operate today. In practice: news reports describe the rupee 'depreciating' or 'hitting a record low', not being devalued.", 'c6', 'core', topic='Devaluation (Revaluation) vs Depreciation (Appreciation)'),
                M('k1e', 'A rising REER despite a weaker nominal rupee means Kaveri\'s competitiveness has:', ['Worsened, because higher Indian inflation outweighed the nominal fall', 'Improved, because the nominal rupee fell', 'Not changed', 'Improved, because REER ignores prices'], 0, "The REER adjusts the nominal rate for relative prices. Even though the nominal rupee weakened, India's higher inflation raised its real exchange rate, so Indian goods became relatively dearer and Kaveri's competitiveness worsened. 'Improved, because the nominal rupee fell' is the trap — it ignores inflation differences. In practice: exporters' bodies cite rising REER as evidence that the rupee is overvalued in real terms.", 'c3', 'hard', topic='Nominal Versus Real Exchange Rates'),
            ]}

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch09', 'n': 4, 'title': 'Exchange Rate and Its Economic Effects',
        'outcomes': ['Explain the exchange rate, foreign currency transactions, direct and indirect quotes and cross rates, with calculations.',
                     'Compare floating, managed-float and fixed exchange rate regimes, and distinguish nominal, real and real effective exchange rates.',
                     'Describe the foreign exchange market (participants, spot and forward deals, premium and discount, arbitrage, vehicle currency) and how demand and supply set the nominal rate.',
                     'Compute appreciation and depreciation, distinguish devaluation and revaluation, and analyse the effects of currency movements on trade, inflation, debt and investment.'],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['fnd-p4-ch09-u01'],
                 'exam_tip': 'Numericals on quotes, cross rates and % appreciation/depreciation are quick marks — but measure each currency on the right base. Demand-supply shift questions ("which event appreciates the rupee?") are asked often.'},
        'concepts': concepts, 'illustrations': [ill1, ill2, ill3, ill4, ill5], 'jobs': jobs, 'mcqs': mcqs, 'questions': [q1, q2, q3],
        'revision': {'summary': ['Exchange rate = price of one currency in another. Direct quote: ₹ per $; indirect: $ per ₹ (reciprocal). Cross rate via a third currency.',
                                 'Regimes: free float (market; independent monetary policy; volatile) → managed float (occasional intervention) → fixed/peg (stable, disciplined; needs reserves, no flexibility). Soft vs hard peg.',
                                 'Real exchange rate = nominal (foreign per domestic) × domestic price ÷ foreign price; REER ↑ = loss of competitiveness.',
                                 'Forex market: OTC network, market makers vs passive players, arbitrage, spot (≈2 days) vs forward/futures; premium (forward > spot) vs discount; dollar = vehicle currency.',
                                 'Demand for $ (imports, transfers out, investment abroad) vs supply of $ (exports, remittances, FDI/FPI inflows). Demand ↑ → rupee depreciates; supply ↑ → rupee appreciates.',
                                 'Devaluation/revaluation = official, fixed regime; depreciation/appreciation = market, floating regime.',
                                 'Depreciation: exports ↑, imports ↓, expansionary, but inflation, ECB/foreign-debt burden, investor caution. Appreciation: the reverse; cools inflation; may widen current account deficit.'],
                     'remember': ['% change of currency A = change in (B per A) ÷ old (B per A).', 'Forward premium % = (forward − spot) ÷ spot × 100.', 'Exporters gain and importers lose from home-currency depreciation.'],
                     'traps': ['Dollar up 5% does not mean rupee down 5%.', 'Remittances and FDI inflows appreciate the rupee; imports and debt repayment depreciate it.', 'Depreciation ≠ devaluation.', 'Real, not nominal, rates drive trade.']},
        'quickref': [{'k': 'Direct quote', 'v': 'Local currency per 1 unit of foreign (₹83/$); foreign = base'}, {'k': 'Indirect quote', 'v': 'Foreign per 1 unit of local ($0.012/₹) = 1 ÷ direct'},
                     {'k': 'Cross rate', 'v': '₹/€ = ₹/$ × $/€'}, {'k': 'Real exchange rate', 'v': 'Nominal × domestic price (index) ÷ foreign price (index)'},
                     {'k': 'REER', 'v': 'NEER ÷ price deflator; rise = competitiveness lost'}, {'k': 'Forward premium/discount', 'v': '(F − S) ÷ S × 100; + premium, − discount'},
                     {'k': 'Rupee depreciates when', 'v': 'Demand for $ ↑ (imports, outflows) or supply of $ ↓'}, {'k': 'Devaluation vs depreciation', 'v': 'Official (fixed) vs market (floating)'}],
        'viva': viva, 'cases': [case],
    }

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        's1': _K('dollar appreciat|dollar strengthen|dollar gain|dollar rise|dollar costlier', 'rupee depreciat|rupee weaken|rupee fall|rupee cheaper|rupee lost', 'appreciat 7.5|7.5 appreciat|dollar 7.5|depreciat 6.98|6.98 depreciat|rupee 6.98|7.5 percent'),
        's2': _N(7.5),
        's3': _K('-6.98|6.98'),
        's4': _N(150000),
        's5': _N(360000),
    },
    'q2': {
        's1': _K('0.0125|e x p p|e p p|1 80 400|1 80 x 400|nominal p p'),
        's2': _K('0.625'),
        's3': _K('0.0135|0.01354|0.0125 1.0833|1.0833|1.083'),
        's4': _K('real appreciation|appreciat|rer rose|rer higher|rer increas|less competitive|lost competitiveness|competitiveness deteriorat|competitiveness fell|competitiveness declin|competitiveness reduc|dearer|costlier'),
    },
    'q3': {
        'extra_ok': True,
        's1': _K('deliberate|official|government|central bank|policy', 'market|demand and supply|supply demand|market forces'),
        's2': _K('fixed|pegged', 'floating|flexible'),
        's3': _K('discrete|one time|sudden|reset|par value|step', 'gradual|continuous|day to day'),
        's4': _K('revaluation', 'appreciation'),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
