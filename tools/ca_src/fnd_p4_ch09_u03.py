"""CA Foundation · Paper 4 Business Economics · Chapter 9 International Trade · Unit 3 Trade Negotiations.
Original explanations and questions; figures about the WTO are those given in the ICAI study material for this attempt."""
from lib import *
from ca_viva import P, V, ALT
from fnd_p4_ch09_u01 import M, S, Q, fx

UID = 'fnd-p4-ch09-u03'


def build():
    # ---------- Illustration 1: ladder of integration ----------
    ladder = table(['Stage', 'Tariffs among members', 'Policy towards outsiders', 'Factor movement', 'Common currency', 'Example (from the material)'], [
        ['Unilateral preference', 'One side cuts duties for the other (one-way)', 'Unchanged', 'No', 'No', 'Generalized System of Preferences'],
        ['Bilateral agreement', 'Rules of trade between two countries / blocs', 'Unchanged', 'No', 'No', 'EU–South Africa FTA; ASEAN–India FTA'],
        ['Regional preferential trade agreement', 'Reduced (not removed), reciprocal, members only', 'Own tariffs', 'No', 'No', 'GSTP among developing countries'],
        ['Trading bloc', 'Free trade among members', 'May share a common external tariff', 'No', 'No', 'Arab League; EFTA'],
        ['Free trade area', 'All tariffs and quotas removed', 'Each keeps its OWN external tariff', 'No', 'No', 'ASEAN–India FTA (in force 1 August 2005)'],
        ['Customs union', 'All tariffs removed', 'COMMON external tariff', 'No', 'No', 'EU (27 members); GCC; MERCOSUR'],
        ['Common market', 'All tariffs removed', 'Common external tariff', 'Free movement of labour and capital; laws harmonised', 'No', 'EU'],
        ['Economic and monetary union', 'All tariffs removed', 'Common external tariff', 'Free', 'Yes — single currency, converging macro policies', 'Euro area of the EU'],
    ], title='Types of trade agreement — from shallow to deep integration')
    ill1 = {'id': 'i1', 'title': 'Placing agreements on the integration ladder', 'difficulty': 'core', 'minutes': 8,
            'q': 'Arrange the following from the least to the most integrated and state the feature that takes each step further: free trade area, economic and monetary union, preferential trade agreement, customs union, common market.',
            'solution': [ladder, p('Order: preferential trade agreement → free trade area → customs union → common market → economic and monetary union. Each step adds: tariffs reduced → tariffs removed → common external tariff → free factor movement and harmonised rules → single currency with policy convergence.')]}

    # ---------- Illustration 2: MFN in numbers ----------
    c2 = Checks()
    before_c = c2.add('500000*12/100', 'duty on C before at MFN 12%')
    after_c = c2.add('500000*8/100', 'duty on C after the cut is extended to all')
    saving = c2.add('500000*12/100-500000*8/100', 'saving for C\'s exporter')
    ill2 = {'id': 'i2', 'title': 'Most-favoured-nation treatment with numbers', 'difficulty': 'moderate', 'minutes': 7,
            'q': 'Country A (a WTO member) charges 12% on imported bicycles from all WTO members. After talks with Country B it wants to charge B only 8%. A and B are NOT in a free trade area or customs union. What must A do, and how does this affect a ₹5,00,000 consignment from Country C, another WTO member?',
            'solution': [legal('MFN (Article I of GATT): a favour granted to one WTO member — such as a lower duty — must be extended immediately to all other WTO members for like products. Exceptions exist for FTAs/customs unions, special access for developing countries, and measures against unfair trade.',
                               'A wants to lower its bicycle duty for B from 12% to 8%. A and B have no FTA or customs union; C is also a WTO member.',
                               f'No exception applies, so the 8% rate must be given to C too. Duty on C\'s consignment: before 12% × 5,00,000 = {R(before_c)}; after 8% × 5,00,000 = {R(after_c)}.',
                               f'A must apply 8% to all WTO members. C\'s exporter saves {R(saving)} per such consignment — every tariff cut becomes multilateral.')],
            'checks': c2}

    # ---------- Illustration 3: FTA vs customs union — trade deflection ----------
    c3 = Checks()
    via_x = c3.add('1000*5/100', 'duty if entered through X (5%)')
    via_y = c3.add('1000*20/100', 'duty if entered through Y (20%)')
    gap = c3.add('1000*20/100-1000*5/100', 'incentive to route through X')
    cu = c3.add('1000*12/100', 'duty under a common external tariff of 12%')
    ill3 = {'id': 'i3', 'title': 'Why an FTA needs rules of origin but a customs union does not', 'difficulty': 'moderate', 'minutes': 8,
            'q': 'X and Y form a free trade area. On imports of a ₹1,000 gadget from an outside country, X charges 5% and Y charges 20%. (a) What duty is paid if the gadget enters Y directly, and if it enters through X and then moves duty-free to Y? (b) What changes if X and Y form a customs union with a common external tariff of 12%?',
            'solution': [table(['Route', 'Working', 'Duty (₹)'], [
                ['FTA — directly into Y', '1,000 × 20%', via_y],
                ['FTA — into X, then duty-free to Y', '1,000 × 5%', via_x],
                ['Incentive to deflect trade through X', f'{inr(via_y)} − {inr(via_x)}', gap],
                ['Customs union — entry through either member', '1,000 × 12%', cu],
            ]), p('In an FTA each member keeps its own external tariff, so importers would route goods through the low-duty member (trade deflection). Rules of origin stop this: only goods originating in the FTA get duty-free movement. In a customs union the same tariff applies wherever the goods enter, so there is no incentive to deflect.')],
            'checks': c3}

    # ---------- Illustration 4: national treatment ----------
    c4 = Checks()
    imp_tax = c4.add('200*18/100', 'internal tax on imported soap at 18%')
    loc_tax = c4.add('200*12/100', 'internal tax on local soap at 12%')
    ill4 = {'id': 'i4', 'title': 'National treatment: border duty vs internal tax', 'difficulty': 'moderate', 'minutes': 6,
            'q': 'Country M charges 10% customs duty on imported soap. Inside the country it also levies a sales tax of 18% on imported soap but 12% on locally made soap of the same kind. A ₹200 bar is sold in each case. Does either measure violate national treatment?',
            'solution': [legal('National treatment (GATT Article 3, GATS Article 17, TRIPS Article 3): once foreign goods have entered the market, they must be treated no less favourably than like domestic goods. It applies only after entry, so a customs duty at the border is not a violation.',
                               f'Customs duty 10% at the border; internal tax {R(imp_tax)} on an imported bar against {R(loc_tax)} on a local bar.',
                               'The customs duty is charged at entry — allowed (subject to bound rates). The sales tax discriminates after entry: the imported bar bears ₹12 more tax than a like local bar.',
                               'The 10% customs duty is permitted; the higher internal tax on imported soap violates national treatment.')],
            'checks': c4}

    timeline = table(['Year / period', 'Event'], [
        ['1948–1994', 'GATT provides the rules for most world trade (about 47 years); eight rounds of talks under GATT'],
        ['September 1986', 'Uruguay Round launched at Punta del Este, Uruguay (planned to end December 1990)'],
        ['December 1993', 'Uruguay Round completed — the eighth and largest round; 123 countries took part'],
        ['15 April 1994', 'Agreement signed by most countries'],
        ['1995', 'WTO comes into being — one institution covering GATT as modified by the Uruguay Round, plus services and IP'],
        ['November 2001', 'Doha Round (Doha Development Agenda) launched at the 4th Ministerial Conference, Doha, Qatar — ninth round since the Second World War'],
    ], title='GATT to WTO — key dates')

    concepts = [
        {'id': 'c1', 'title': 'Trade negotiations and regional trade agreements (RTAs)', 'body': [
            'Trade negotiations are bargaining processes between governments with competing aims — one side seeks market access through lower tariffs, the other seeks protection for its industries. Lobbies, pressure groups and NGOs also influence the outcome. The material notes that India was part of 19 concluded agreements and negotiating over two dozen more; and that 2020 saw Brexit and the USMCA (successor to NAFTA), amid the US–China trade war and the pandemic.',
            'An RTA is a treaty between two or more governments setting trade rules for all signatories, formed to reduce barriers among members. Members need not be in the same geographical region. The material counts 339 RTAs in force on 1 February 2021.',
            'Types, from shallow to deep: unilateral (one-way incentives, e.g. GSP), bilateral (two countries or blocs), regional preferential trade agreements (reciprocal, reduced barriers for members), then a trading bloc, a free trade area, a customs union, a common market and finally an economic and monetary union.'],
         'blocks': [ladder],
         'analogy': 'Integration is like a friendship deepening: a one-way favour, then mutual discounts, then free entry to each other\'s homes, then a shared front door, then a joint bank account.',
         'work': 'Each new agreement changes duty rates, rules of origin and compliance paperwork. CAs advising importers and exporters map which agreement gives the best duty and what documentation it needs.'},
        {'id': 'c2', 'title': 'Free trade area, customs union, common market, monetary union', 'body': [
            'Free trade area (FTA): members remove all tariffs and quotas on trade among themselves but each keeps its own, independent tariff on imports from outside. Example: the ASEAN–India FTA (ten ASEAN states and India), in force from 1 August 2005.',
            'Customs union: free trade among members PLUS a common external tariff on non-members — so the same duty applies wherever goods enter the union. Because outsiders face a higher duty than members, it technically departs from MFN. Examples: the EU (27 members, one customs territory), GCC, MERCOSUR.',
            'Common market: a customs union plus free movement of factors of production (labour, capital) and some harmonisation of commercial and financial laws.',
            'Economic and monetary union: a common market with a single currency, which requires strong convergence of macroeconomic policies — e.g. the European Union countries using a single currency.'],
         'analogy': 'FTA: neighbours stop charging each other entry fees but each keeps its own gate rules for strangers. Customs union: they build one common gate with one fee.',
         'work': 'Rules-of-origin compliance exists because of FTAs; customs unions avoid it. Knowing which a partner group is tells a CA how much origin documentation a client needs.'},
        {'id': 'c3', 'title': 'GATT and why it lost relevance', 'body': [
            'The General Agreement on Tariffs and Trade covers international trade in goods. Within the WTO, the Council for Trade in Goods (Goods Council), made up of all members, oversees it through 10 committees (agriculture, market access, subsidies, anti-dumping and others), together with a working party on state-trading enterprises and the committee for the IT Agreement.',
            'GATT provided the rules for most world trade from 1948 to 1994 and held eight rounds that cut tariffs substantially.',
            'Why it lost relevance by the 1980s: unsuited to a complex, globalising world; investment had grown hugely; services and intellectual property were outside it; merchandise trade had outgrown it; its ambiguities could be exploited; agricultural liberalisation had failed; its institutions and dispute settlement were weak; and it was not a treaty, so it bound nations only to the extent it did not clash with domestic law.'],
         'analogy': 'GATT was a gentlemen\'s club rulebook written for goods; by the 1980s the members were also trading services and ideas, and the club had no proper referee.',
         'work': 'Many tariff concessions an importer relies on today trace back to GATT rounds; knowing the history helps interpret bound rates in the tariff schedule.'},
        {'id': 'c4', 'title': 'The Uruguay Round and the birth of the WTO', 'body': [
            'Launched at Punta del Este, Uruguay in September 1986 and due to finish by December 1990, the Round stalled — especially over agriculture — and was completed only in December 1993 after seven years. It was the eighth, the most ambitious and the largest round, with 123 participating countries.',
            'Fifteen negotiating groups covered tariffs, non-tariff barriers, tropical and natural-resource products, textiles and clothing, agriculture, safeguards against import surges, subsidies and countervailing duties, trade-related intellectual property, trade-related investment, services, and the GATT system itself (dispute settlement, implementation of Tokyo Round codes, especially anti-dumping).',
            'The agreement was signed by most countries on 15 April 1994. It created the World Trade Organization, a single institutional framework encompassing GATT as modified by the Round — the biggest reform of the world trading system since the Second World War.'],
         'blocks': [timeline],
         'analogy': 'The Uruguay Round turned a loose club rulebook into a full constitution with a court — the WTO.',
         'work': 'TRIPS, GATS, SPS and TBT — all born in this Round — shape patent costs, service exports and product compliance for Indian businesses today.'},
        {'id': 'c5', 'title': 'The WTO: objectives, functions and structure', 'body': [
            'The WTO is the only global organisation dealing with the rules of trade between nations. Its principal aim is to help trade flow smoothly, freely, fairly and predictably.',
            'Six key objectives: set and enforce rules for international trade; provide a forum for negotiating and monitoring further liberalisation; resolve trade disputes; make decision-making more transparent; cooperate with other international economic institutions; and help developing countries benefit fully. The preamble speaks of raising living standards, full employment, growing real income and effective demand, and expanding production of and trade in goods and services.',
            'Functions: forum for negotiations, administering agreements, reviewing national trade policies, technical assistance and training for developing countries, cooperation with other organisations.',
            'Structure (three tiers): the Ministerial Conference — the top body, meeting at least once every two years; the General Council — meets several times a year in Geneva and also sits in two other capacities — as the body that settles disputes (DSB) and the body that reviews trade policies (TPRB); then the Goods, Services and TRIPS Councils reporting to it. A Secretariat in Geneva, headed by a Director-General, supports the work.',
            'Membership (as given in the material): 164 members in all — 117 of them developing countries or separate customs territories; together about 95% of world trade; around 24 others negotiating to join. (Real-world note: Comoros and Timor-Leste joined in 2024, taking membership to 166; for the exam, quote the material\'s figure of 164 unless 166 is the only matching option.) Over three-quarters of members are developing or transition economies.'],
         'analogy': 'Ministerial Conference = the parliament that meets every two years; General Council = the cabinet that meets often; specialised councils = ministries; Secretariat = civil service.',
         'work': 'When India disputes another country\'s duties (or is challenged), the case goes to the Dispute Settlement Body. Industry bodies — with CA support on data — feed into these cases.'},
        {'id': 'c6', 'title': 'Guiding principles of the WTO', 'body': [
            'Trade without discrimination — (1) Most-favoured-nation: a favour to one member (e.g. a lower duty) must go to all members. It is Article I of GATT, Article 2 of GATS and Article 4 of TRIPS. Exceptions under strict conditions: FTAs/customs unions, special market access for developing countries, barriers against unfairly traded goods, limited cases in services. (2) National treatment: imported and local goods, services and IP must be treated equally once the import has entered the market (GATT Article 3, GATS Article 17, TRIPS Article 3); a customs duty at the border is therefore not a violation.',
            'Freer trade gradually through negotiation — "progressive liberalisation", with longer periods for developing countries.',
            'Predictability through binding and transparency — bound tariffs are ceilings; changing them needs negotiation and possibly compensation. The Uruguay Round raised the share of trade under bindings; in agriculture 100% of products now have bound tariffs. Quotas are discouraged; rules must be published and notified; the Trade Policy Review Mechanism keeps watch.',
            'Promoting fair competition — the WTO is better described as a system of rules for open, fair and undistorted competition than as a pure "free trade" body: tariffs and, in limited cases, other protection are allowed; rules on dumping and subsidies define unfair trade.',
            'Encouraging development and economic reform — flexibility, transition periods and special assistance for developing and least-developed countries, including duty-free and quota-free access for almost all products from LDCs in developed markets.'],
         'analogy': 'MFN: "If I give one friend a discount, every friend gets it." National treatment: "Once you are inside my shop, you are treated like family."',
         'work': 'Before a client lobbies for a duty hike, a CA checks the bound rate — the government cannot go above it without compensating partners.'},
        {'id': 'c7', 'title': 'WTO agreements and the Doha Round', 'body': [
            'Main agreements: Agriculture (market access, domestic support, export subsidies); SPS; Textiles and Clothing (replaced the Multi-Fibre Arrangement in force since 1974, integrating textiles into GATT over 10 years); TBT; TRIMs (no local-content or trade-balancing requirements inconsistent with national treatment and the ban on quantitative restrictions); Anti-Dumping; Customs Valuation; Pre-shipment Inspection; Rules of Origin; Import Licensing; Subsidies & Countervailing Measures (SCM); Safeguards; GATS (services: MFN, transparency, sector commitments); TRIPS (MFN and national treatment for copyright, trademarks, geographical indications, designs, patents, IC layouts, undisclosed information, with enforcement); Dispute Settlement Understanding; Trade Policy Review Mechanism; and plurilateral agreements (civil aircraft, government procurement) signed by only some members.',
            'The Doha Round (Doha Development Agenda): the ninth round since the Second World War, launched at the WTO\'s 4th Ministerial Conference in Doha, Qatar in November 2001. It covers about 20 areas — agriculture, services, non-agricultural market access (NAMA), trade facilitation, environment, geographical indications and other IP issues. Agriculture was the most controversial topic, and progress has been slow.',
            'Issues and criticism: slow multilateral talks, uncertainty from the spread of RTAs, limited liberalisation, and developing-country concerns — protectionism and limited market access in developed countries, implementation difficulties, a north–south divide, very high tariffs and tariff escalation on their products, erosion of preferences.',
            'The material also notes WTO monitoring of G20 economies (2022): export restrictions on food, feed and fertiliser added to price volatility, and the Director-General urged G20 members to keep markets open and predictable.'],
         'analogy': 'The WTO agreements are chapters of one rulebook; the Doha Round is the long-running attempt to write the next edition.',
         'work': 'TRIPS shapes patent and licensing costs for pharma clients; GATS commitments shape whether Indian CA firms can serve clients abroad; customs valuation rules decide the assessable value on which duty is paid.'},
    ]

    mcqs = [
        M('m1', 'Regional trade agreements are formed mainly to:', ['Reduce trade barriers among member countries', 'Raise tariffs on all imports', 'Replace the WTO', 'Fix exchange rates'], 0, 'RTAs reduce barriers among members, who need not share a region.', 'c1'),
        M('m2', 'As per the study material, the number of RTAs in force as of 1 February 2021 was:', ['339', '164', '123', '117'], 0, '339 RTAs; 164 is WTO membership; 123 countries in the Uruguay Round; 117 developing members.', 'c1', 'core', '339'),
        M('m3', 'An importing country offering one-way trade incentives to help an exporting developing country (e.g. GSP) is a:', ['Unilateral trade agreement', 'Bilateral agreement', 'Customs union', 'Common market'], 0, 'GSP is unilateral and non-reciprocal.', 'c1'),
        M('m4', 'Members remove tariffs among themselves but each keeps its own tariff on outsiders. This is a:', ['Free trade area', 'Customs union', 'Common market', 'Economic union'], 0, 'A common external tariff would make it a customs union.', 'c2'),
        M('m5', 'The feature that distinguishes a customs union from a free trade area is:', ['A common external tariff', 'Free movement of labour', 'A single currency', 'Removal of internal tariffs'], 0, 'Both remove internal tariffs; only a customs union adds a common external tariff.', 'c2'),
        M('m6', 'Free movement of labour and capital, along with a common external tariff, is a feature of a:', ['Common market', 'Free trade area', 'Preferential trade agreement', 'Unilateral agreement'], 0, 'Common market = customs union + factor mobility.', 'c2'),
        M('m7', 'Members sharing a common currency and converging macroeconomic policies form a(n):', ['Economic and monetary union', 'Customs union', 'Trading bloc', 'Free trade area'], 0, 'The final stage of integration.', 'c2'),
        M('m8', 'Which is an example of a free trade area given in the material?', ['ASEAN–India FTA', 'MERCOSUR', 'The EU as a customs union', 'GSP'], 0, 'MERCOSUR and the EU are customs unions; GSP is unilateral.', 'c2'),
        M('m9', 'A customs union is said to technically violate MFN because:', ['Members charge outsiders a higher duty than each other', 'Members charge each other higher duties', 'It has no external tariff', 'It uses a single currency'], 0, 'Members get zero duty; non-members pay the common external tariff.', 'c2', 'moderate'),
        M('m10', 'In a free trade area, X charges 6% and Y charges 18% on a ₹2,000 good from outside. How much duty can an importer avoid by entering through X instead of Y (if there are no rules of origin)?', ['₹240', '₹120', '₹360', '₹480'], 0, 'Y: 18% × 2,000 = 360; X: 6% × 2,000 = 120; difference ₹240 — trade deflection, prevented by rules of origin.', 'c2', 'hard', '2000*18/100-2000*6/100'),
        M('m11', 'GATT covered international trade in:', ['Goods', 'Services', 'Intellectual property', 'Capital flows'], 0, 'Services (GATS) and IP (TRIPS) came with the WTO.', 'c3'),
        M('m12', 'Which is NOT a reason why GATT lost relevance?', ['It covered services and intellectual property comprehensively', 'It was not a treaty', 'Agricultural liberalisation failed', 'Its dispute settlement system was weak'], 0, 'GATT did NOT cover services and IP — that was a weakness.', 'c3', 'moderate'),
        M('m13', 'GATT provided the rules for most of world trade for about:', ['47 years', '25 years', '60 years', '10 years'], 0, 'From 1948 to 1994.', 'c3', 'core', '47'),
        M('m14', 'The Uruguay Round was launched in:', ['September 1986', 'November 2001', 'April 1994', 'December 1993'], 0, 'Launched at Punta del Este in September 1986; completed December 1993; signed 15 April 1994.', 'c4'),
        M('m15', 'How many countries participated in the Uruguay Round?', ['123', '164', '117', '95'], 0, '123 countries — the largest round.', 'c4', 'core', '123'),
        M('m16', 'The Uruguay Round was the ___ round of multilateral trade negotiations under GATT.', ['Eighth', 'Ninth', 'Seventh', 'First'], 0, 'The eighth and last GATT round; Doha is the ninth since the Second World War.', 'c4'),
        M('m17', 'The most controversial issue that delayed the Uruguay Round was:', ['Agriculture', 'Textiles', 'Information technology', 'Civil aircraft'], 0, 'Heated controversies over agriculture.', 'c4'),
        M('m18', 'Which is NOT one of the six key objectives of the WTO?', ['Fixing exchange rates of member countries', 'Resolving trade disputes', 'Providing a forum for negotiating further liberalisation', 'Helping developing countries benefit from trade'], 0, 'Exchange rates are not a WTO objective.', 'c5'),
        M('m19', 'The highest decision-making body of the WTO is the:', ['Ministerial Conference', 'General Council', 'Goods Council', 'Secretariat'], 0, 'It meets at least once every two years.', 'c5'),
        M('m20', 'The WTO Ministerial Conference meets at least once every:', ['Two years', 'Year', 'Five years', 'Month'], 0, 'The General Council meets several times a year in between.', 'c5', 'core'),
        M('m21', 'The WTO General Council also meets as the:', ['Dispute Settlement Body and Trade Policy Review Body', 'Ministerial Conference', 'Secretariat', 'TRIPS Council only'], 0, 'One body, three hats.', 'c5'),
        M('m22', 'As per the study material, the WTO has ___ members, accounting for about 95% of world trade.', ['164', '117', '123', '339'], 0, '164 members in total as per the material; 117 of them are developing countries or separate customs territories. (Membership became 166 in 2024 with Comoros and Timor-Leste.)', 'c5', 'core', '164'),
        M('m23', 'The WTO Secretariat is located in:', ['Geneva', 'New York', 'Washington DC', 'Doha'], 0, 'Headed by a Director-General.', 'c5'),
        M('m24', 'Under the MFN principle:', ['A favour granted to one WTO member must be extended to all members', 'Imported goods must be taxed like domestic goods after entry', 'Developed countries must give duty-free access to all', 'Members may never form free trade areas'], 0, 'The second option describes national treatment.', 'c6'),
        M('m25', 'MFN appears as Article I of:', ['GATT', 'GATS', 'TRIPS', 'TRIMs'], 0, 'GATT Article I; in GATS it is Article 2, in TRIPS Article 4.', 'c6', 'moderate'),
        M('m26', 'Charging customs duty on an import, while no equivalent tax is charged on a like local product:', ['Does not violate national treatment, as it applies only after entry', 'Violates national treatment', 'Violates MFN', 'Is banned by the WTO'], 0, 'National treatment applies once goods have entered the market.', 'c6', 'moderate'),
        M('m27', 'Country A charges 10% MFN duty on a product and, outside any FTA, cuts it to 7% for Country B. On a ₹3,00,000 consignment from Country C (a WTO member), A must now charge:', ['₹21,000', '₹30,000', '₹9,000', '₹0'], 0, 'MFN: the 7% must be extended to all members — 7% × 3,00,000 = ₹21,000.', 'c6', 'hard', '300000*7/100'),
        M('m28', 'Which WTO principle is served by "binding" tariffs?', ['Predictability', 'National treatment', 'Unilateral preference', 'Monetary union'], 0, 'Bindings are ceilings that give traders certainty.', 'c6'),
        M('m29', 'The share of agricultural products with bound tariffs after the Uruguay Round is:', ['100%', '50%', '75%', '95%'], 0, 'All agricultural products now have bound tariffs.', 'c6', 'moderate', '100'),
        M('m30', 'The WTO is best described as:', ['A system of rules for open, fair and undistorted competition', 'A pure free-trade institution that bans all tariffs', 'A body that fixes world prices', 'A development bank'], 0, 'Tariffs and limited protection are allowed.', 'c6'),
        M('m31', 'The Agreement on Textiles and Clothing replaced the:', ['Multi-Fibre Arrangement', 'GSP', 'Agreement on Agriculture', 'TRIPS'], 0, 'The MFA had been in force since 1974; ATC integrated textiles into GATT over 10 years.', 'c7'),
        M('m32', 'Local content and trade-balancing requirements on foreign investors are disciplined by:', ['TRIMs', 'TRIPS', 'GATS', 'SPS'], 0, 'Trade-Related Investment Measures.', 'c7'),
        M('m33', 'An agreement signed by only some WTO members, such as on government procurement, is called:', ['Plurilateral', 'Multilateral', 'Unilateral', 'Bilateral'], 0, 'Multilateral agreements bind all members.', 'c7'),
        M('m34', 'The Doha Round was launched at the WTO\'s:', ['Fourth Ministerial Conference in November 2001', 'First Ministerial Conference in 1995', 'Uruguay meeting in 1986', 'General Council in 1994'], 0, 'Doha, Qatar — the ninth round since the Second World War.', 'c7'),
        M('m35', 'The most controversial topic in the Doha agenda was:', ['Agriculture', 'Trade facilitation', 'Geographical indications', 'Environment'], 0, 'As in the Uruguay Round.', 'c7'),
    ]

    cq1 = Checks()
    d_a = cq1.add('800000*15/100', 'duty at 15% (direct entry via Q)')
    d_b = cq1.add('800000*4/100', 'duty at 4% (entry via P)')
    d_g = cq1.add('800000*15/100-800000*4/100', 'deflection gain')
    d_c = cq1.add('800000*10/100', 'common external tariff 10%')
    q1 = Q('q1', 5, 'moderate', 'table', 'P and Q form a free trade area. On a component from outside worth ₹8,00,000, P charges 4% and Q charges 15%. (a) Compute the duty on direct entry into Q and on entry through P. (b) Explain the problem this creates and how it is controlled. (c) Compute the duty if P and Q convert to a customs union with a 10% common external tariff.',
           [table(['Route', 'Working', 'Duty (₹)'], [['Direct into Q', '8,00,000 × 15%', d_a], ['Through P, then duty-free to Q', '8,00,000 × 4%', d_b], ['Duty avoided by deflection', f'{inr(d_a)} − {inr(d_b)}', d_g], ['Customs union, any entry point', '8,00,000 × 10%', d_c]]),
            p('(b) Trade deflection: goods for Q are routed through low-duty P. Rules of origin allow duty-free movement only to goods originating in the FTA. (c) Under a common external tariff the entry point does not matter.')],
           [S('s1', 'Duty via each FTA route', 1, 'computation'), S('s2', 'Duty avoided by deflection', 1, 'computation'), S('s3', 'Explains trade deflection', 1, 'concept'), S('s4', 'Rules of origin as the control', 1, 'application'), S('s5', 'Customs union duty and reason', 1, 'conclusion')],
           ['Many confuse which arrangement needs rules of origin.'], ['Saying a customs union has no external tariff.', 'Forgetting that goods move duty-free inside the FTA.'], ['Show each route as a separate row.'], checks=cq1)

    q2 = Q('q2', 4, 'core', 'table', 'Distinguish between the MFN principle and the national treatment principle of the WTO.',
           [table(['Basis', 'Most-favoured-nation', 'National treatment'], [
               ['Meaning', 'No discrimination between trading partners — a favour to one goes to all members', 'No discrimination between imported and local products once imports have entered'],
               ['Comparison made', 'Foreign vs foreign', 'Foreign vs domestic'],
               ['When it applies', 'At the border and beyond (e.g. customs duty rates)', 'Only after the goods, services or IP have entered the market'],
               ['Where found', 'GATT Art. I, GATS Art. 2, TRIPS Art. 4', 'GATT Art. 3, GATS Art. 17, TRIPS Art. 3'],
               ['Exceptions', 'FTAs / customs unions, special access for developing countries, measures against unfair trade', 'Border customs duties are not a breach'],
           ])],
           [S('s1', 'Meaning of MFN', 1, 'concept'), S('s2', 'Meaning of national treatment', 1, 'concept'), S('s3', 'Timing / comparison made', 1, 'analysis'), S('s4', 'Articles or exceptions', 1, 'application')],
           ['The best answers state "foreign vs foreign" and "foreign vs local" clearly.'], ['Writing that charging customs duty violates national treatment.'], ['A table with 4–5 bases is quickest.'])

    q3 = Q('q3', 4, 'core', 'text', 'Describe the three-tier decision-making structure of the WTO.',
           [ul(['Top tier — Ministerial Conference: highest authority; can decide on any matter under any multilateral agreement; meets at least once every two years.',
                'Second tier — General Council: meets several times a year in Geneva; doubles up as the Dispute Settlement Body and as the Trade Policy Review Body.',
                'Third tier — Councils for Trade in Goods, Trade in Services and TRIPS: report to the General Council and oversee their agreements, assisted by committees and working groups.',
                'Support — the Secretariat in Geneva headed by the Director-General.'])],
           [S('s1', 'Ministerial Conference and its periodicity', 1, 'concept'), S('s2', 'General Council and its two other roles', 1, 'concept'), S('s3', 'Three councils under the General Council', 1, 'concept'), S('s4', 'Secretariat / Director-General', 1, 'presentation')],
           ['Many omit that the General Council doubles as the DSB and TPRB.'], ['Placing the Secretariat as a decision-making tier.'], ['Use a numbered list from top to bottom.'])

    jobs = [
        {'id': 'j1', 'title': 'Choosing the cheapest legal route under trade agreements', 'role': 'CA in industry (supply-chain finance, auto-components maker)',
         'situation': 'You source an alloy from Thailand. Duty options: MFN rate, or the ASEAN–India FTA rate if the supplier provides a valid certificate of origin.',
         'steps': ['Confirm the product meets the FTA\'s origin criteria (value addition / change in tariff classification).', 'Compare landed cost under MFN and FTA rates.', 'Keep origin documents for the period required for customs verification.', 'Do not route non-originating goods through an FTA partner — that is exactly what rules of origin prevent.'],
         'takeaway': 'FTAs reward compliance: duty savings depend on proving origin.',
         'think': 'Why would the same alloy from China not get the ASEAN–India rate even if shipped via Thailand?', 'answer': 'Because it does not originate in an FTA member; merely passing through Thailand does not confer origin, so the MFN rate applies.'},
        {'id': 'j2', 'title': 'Explaining a WTO dispute to a board', 'role': 'CA advising an exporters\' association',
         'situation': 'A trading partner has raised duty on your members\' product above its bound rate.',
         'steps': ['Check the partner\'s bound rate in its WTO schedule.', 'Raising an applied rate above the bound rate breaches its commitment unless it negotiated and compensated partners.', 'Brief the government (which alone can bring a WTO case) with trade-loss data.', 'Meanwhile, explore FTA markets with lower duties.'],
         'takeaway': 'Binding gives exporters legal certainty; the Dispute Settlement Body enforces it.'},
    ]

    viva = [
        V('v1', 'Explain the most-favoured-nation principle of the WTO.',
          'Under the most-favoured-nation principle a WTO member cannot discriminate between its trading partners. If it grants one member a special favour, such as a lower customs duty, it must give the same treatment to all other members. Exceptions are allowed for free trade areas and customs unions, special access for developing countries and action against unfair trade.',
          [P('p1', 'No discrimination between trading partners', 3, 'not discriminat|no discriminat|without discriminat|cannot discriminat|equal|equally|same treatment|non discriminat|treat all|not favour one'),
           P('p2', 'A favour (e.g. lower duty) to one member must be extended to all members', 5, 'lower duty|lower tariff|favour|concession|special treatment|privilege|benefit|reduce tariff|tariff cut|cut duty|cuts duty|lowers duty|lowers tariff|lower rate|cuts a tariff|cuts tariff',
             'all member|all other member|every member|all countries|all trading partner|everyone|every other|all wto|all others|rest of member|every country|other members|everybody'),
           P('p3', 'Exceptions: FTAs/customs unions, developing countries, unfair trade', 2, 'exception|free trade area|free trade agreement|customs union|fta|developing|unfair|except')], 'c6'),
        V('v2', 'What is the national treatment principle?',
          'National treatment means that imported goods, services and intellectual property must be treated no less favourably than local ones once they have entered the market. It applies only after entry, so charging customs duty at the border is not a violation.',
          [P('p1', 'Imported and local goods (services, IP) treated equally', 5, 'import|foreign', 'local|domestic|home|national|indigenous', 'equal|same|no less favour|not less favour|alike|without discriminat|not discriminat|no discriminat|similar|on par|at par|like local|like domestic', min=3),
           P('p2', 'Applies only after the import has entered the market', 3, 'after entry|after enter|once enter|after the goods enter|enter the market|entered|inside the market|after import|after clearance|once inside|after crossing|once in the market|crossed the border|after it enters'),
           P('p3', 'So a border customs duty is not a violation', 2, 'customs duty not|duty is not a violation|not a violation|not violat|does not violat|doesn t violat|allowed|permitted|is fine|okay|ok|not breach|border duty|customs duty allowed')], 'c6'),
        V('v3', 'What is a customs union?',
          'A customs union is a group of countries that remove all tariffs on trade among themselves and adopt a common external tariff on imports from non-members, so the same duty applies wherever goods enter. The European Union is an example.',
          [P('p1', 'Members remove tariffs on trade among themselves', 4, 'remov|elimin|abolish|no tariff|zero tariff|free trade|duty free|tariff free|scrap|without tariff', 'among themselves|between themselves|among member|between member|internal|each other|within|inside|member countries', min=2),
           P('p2', 'Common external tariff on non-members', 5, 'common external|common tariff|same tariff|same external|uniform tariff|single external|one external|uniform external|same duty|common duty|single tariff|joint tariff|same rate'),
           P('p3', 'Example: EU / GCC / MERCOSUR', 1, 'european union|eu|gcc|gulf cooperation|mercosur|example')], 'c2'),
        V('v4', 'Why did GATT lose its relevance and give way to the WTO?',
          'GATT covered only trade in goods, so services, intellectual property and investment were outside it. It was not a treaty, its dispute settlement and institutions were weak, its ambiguities were exploited and agricultural liberalisation had failed. So the Uruguay Round created the WTO as a stronger, permanent organisation.',
          [P('p1', 'Did not cover services, intellectual property or investment', 4, 'servic|intellectual property|ip|investment|trips|patent', min=1),
           P('p2', 'Not a treaty / weak institutions and dispute settlement / ambiguities exploited / agriculture failed', 4, 'not a treaty|no treaty|not binding|weak|inadequ|dispute|ambigu|loophole|agricultur|obsolete|outdated|not enforceable'),
           P('p3', 'Uruguay Round created the WTO as a stronger body', 2, 'uruguay|wto|world trade organi|stronger|permanent|formal organi|new organi')], 'c3'),
        V('v5', 'Describe the decision-making structure of the WTO.',
          'The WTO has a three-tier structure. At the top is the Ministerial Conference, which meets at least once every two years. Next is the General Council in Geneva, which also sits as the Dispute Settlement Body and the Trade Policy Review Body. Below it are the Goods, Services and TRIPS Councils. A Secretariat headed by the Director-General supports them.',
          [P('p1', 'Ministerial Conference at the top, meets at least every two years', 4, 'ministerial', 'two year|2 year|every second year|biennial|top|highest|apex|supreme', min=1),
           P('p2', 'General Council — also Dispute Settlement Body and Trade Policy Review Body', 3, 'general council', 'dispute|trade policy review|review body|several times|geneva', min=1),
           P('p3', 'Goods, Services and TRIPS Councils below', 2, 'goods council|council for trade in goods|services council|trips council|intellectual property council|goods services|three council|specialis council'),
           P('p4', 'Secretariat headed by the Director-General', 1, 'secretariat|director general|director-general')], 'c5'),
        V('v6', 'What is the Doha Round?',
          'The Doha Round, formally the Doha Development Agenda, is the ninth round of multilateral trade talks since the Second World War. It began in November 2001 at the fourth WTO Ministerial Conference, held in Doha, Qatar, and covers about twenty areas such as agriculture, services, non-agricultural market access and trade facilitation. Agriculture has been the most controversial issue.',
          [P('p1', 'Doha Development Agenda — ninth round', 2, 'development agenda|ninth|9th|nine'),
           P('p2', 'Launched November 2001 at the 4th Ministerial Conference in Doha, Qatar', 4, '2001|fourth ministerial|4th ministerial|four ministerial|qatar', min=1),
           P('p3', 'Areas: agriculture, services, NAMA, trade facilitation…', 2, 'servic|nama|non agricultur|market access|trade facilitat|environment|geographical|intellectual|twenty|20 area', min=1),
           P('p4', 'Agriculture most controversial', 2, 'agricultur|farm')], 'c7'),
    ]

    case = {'id': 'k1', 'title': 'Three neighbours plan a trade pact', 'difficulty': 'hard',
            'case': ('Aurelia, Brenna and Corvia are WTO members. They plan to remove all duties on trade among themselves. Aurelia wants each country to keep its own duties on outsiders (Aurelia 5%, Brenna 12%, Corvia 20% on electronics). Brenna proposes a single 12% duty on outsiders and, later, free movement of workers and capital. '
                     'Separately, Corvia wants to give Dravia (a WTO member outside the pact) a special 8% duty on electronics while all others pay 20%. Corvia also taxes imported electronics at 15% inside the country, against 10% on local electronics.'),
            'mcqs': [
                M('k3a', 'Aurelia\'s proposal describes a:', ['Free trade area', 'Customs union', 'Common market', 'Monetary union'], 0, 'Own external tariffs = FTA.', 'c2', 'moderate'),
                M('k3b', 'Brenna\'s full proposal (single external duty, then free factor movement) leads ultimately to a:', ['Common market', 'Free trade area', 'Preferential trade agreement', 'Unilateral agreement'], 0, 'Common external tariff → customs union; + factor mobility → common market.', 'c2', 'hard'),
                M('k3c', 'Under Aurelia\'s plan, how much duty is avoided on ₹50,000 of outside electronics entering through Aurelia instead of Corvia, if there were no rules of origin?', ['₹7,500', '₹2,500', '₹10,000', '₹6,000'], 0, 'Corvia 20% = 10,000; Aurelia 5% = 2,500; difference ₹7,500.', 'c2', 'hard', '50000*20/100-50000*5/100'),
                M('k3d', 'Corvia\'s special 8% rate for Dravia alone would violate:', ['The MFN principle', 'National treatment', 'Tariff binding', 'No principle'], 0, 'Dravia is outside any FTA with Corvia, so the favour must go to all WTO members.', 'c6', 'moderate'),
                M('k3e', 'Corvia\'s 15% internal tax on imported vs 10% on local electronics violates:', ['National treatment', 'MFN', 'Rules of origin', 'Nothing, as it is an internal tax'], 0, 'Discrimination after entry breaches national treatment.', 'c6', 'moderate'),
            ]}

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch09', 'n': 3, 'title': 'Trade Negotiations',
        'outcomes': ['Classify regional trade agreements from unilateral preferences to economic and monetary union and explain why FTAs need rules of origin.',
                     'Explain why GATT lost relevance and how the Uruguay Round created the WTO.',
                     'Describe the WTO\'s objectives, functions, three-tier structure, membership and guiding principles (MFN, national treatment, binding, fair competition, development).',
                     'Outline the main WTO agreements and the Doha Round, and the concerns of developing countries.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 45}, 'prereq': ['fnd-p4-ch09-u02'],
                 'exam_tip': 'Facts and principles: 164 members (117 developing), Ministerial Conference every two years, Uruguay Round 1986–1993 (123 countries), Doha November 2001 (9th round, 4th Ministerial). FTA vs customs union, MFN vs national treatment are favourites.'},
        'concepts': concepts, 'illustrations': [ill1, ill2, ill3, ill4], 'jobs': jobs, 'mcqs': mcqs, 'questions': [q1, q2, q3],
        'revision': {'summary': ['RTAs reduce barriers among members (not necessarily neighbours); 339 in force as of 1 February 2021.',
                                 'Ladder: unilateral → bilateral → regional PTA → trading bloc → FTA (own external tariffs) → customs union (common external tariff) → common market (+ factor mobility) → economic & monetary union (+ single currency).',
                                 'GATT (goods; 1948–1994; eight rounds) lost relevance: no services/IP/investment, not a treaty, weak dispute settlement, failed farm liberalisation.',
                                 'Uruguay Round: September 1986 Punta del Este → December 1993; 123 countries; signed 15 April 1994; created the WTO.',
                                 'WTO: Geneva Secretariat under a Director-General; Ministerial Conference (≥ once in 2 years) → General Council (also DSB, TPRB) → Goods, Services, TRIPS Councils; 164 members, 117 developing; ~95% of world trade.',
                                 'Principles: MFN, national treatment, progressive liberalisation, binding & transparency, fair competition, development.',
                                 'Doha Development Agenda: November 2001, 4th Ministerial Conference, ninth round; agriculture most controversial.'],
                     'remember': ['MFN = GATT Art. I / GATS Art. 2 / TRIPS Art. 4.', 'National treatment = GATT Art. 3 / GATS Art. 17 / TRIPS Art. 3.', 'ATC replaced the Multi-Fibre Arrangement (1974) with a 10-year phase-out.'],
                     'traps': ['A customs duty at the border does not violate national treatment.', 'FTA needs rules of origin; customs union does not.', 'Plurilateral ≠ multilateral: only some members sign.', 'GATT did not cover services or IP.']},
        'quickref': [{'k': 'FTA', 'v': 'Internal tariffs removed; own external tariffs'}, {'k': 'Customs union', 'v': 'FTA + common external tariff (EU, GCC, MERCOSUR)'},
                     {'k': 'Common market', 'v': 'Customs union + free movement of labour & capital'}, {'k': 'Economic & monetary union', 'v': 'Common market + single currency'},
                     {'k': 'Uruguay Round', 'v': '1986 (Punta del Este) – 1993; 123 countries; WTO born'}, {'k': 'WTO tiers', 'v': 'Ministerial Conference → General Council → Goods/Services/TRIPS Councils'},
                     {'k': 'WTO members', 'v': '164 (117 developing / separate customs territories), ~95% of world trade'}, {'k': 'Doha Round', 'v': 'November 2001, 4th Ministerial, Qatar; 9th round'},
                     {'k': 'MFN vs NT', 'v': 'Foreign vs foreign / foreign vs local after entry'}],
        'viva': viva, 'cases': [case],
    }
