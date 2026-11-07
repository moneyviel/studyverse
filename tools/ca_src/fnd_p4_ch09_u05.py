"""CA Foundation · Paper 4 Business Economics · Chapter 9 International Trade · Unit 5 International Capital Movements.
Original explanations, numbers and questions. India FDI figures are those stated in the ICAI study material (year given)."""
from lib import *
from ca_viva import P, V, ALT
from fnd_p4_ch09_u01 import M, S, Q, fx

UID = 'fnd-p4-ch09-u05'
ANCH = ('firm', 'company', 'investor', 'business', 'set', 'sets', 'setting', 'establish', 'open', 'invest', 'invests', 'investment', 'fdi', 'when', 'mean', 'one', 'start', 'buy', 'acquir', 'abroad', 'foreign')


def linked(heads, targets):
    """Phrase alternatives that tie a term (e.g. 'horizontal') to its meaning words, allowing up to two linking words."""
    return ALT('{h} {x}', '{h} {a} {x}', '{h} {a} {b} {x}', h=heads, a=ANCH, b=ANCH, x=targets)


def build():
    # ---------- Illustration 1: FDI or FPI? the 10% line ----------
    c1 = Checks()
    s_a = c1.add('1800000/12000000*100', 'Alpine stake %')
    s_b = c1.add('720000/12000000*100', 'Bayside stake %')
    s_c = c1.add('(720000+600000)/12000000*100', 'Bayside stake after second purchase %')
    ill1 = {'id': 'i1', 'title': 'FDI or FPI? Applying the 10% threshold', 'difficulty': 'core', 'minutes': 7,
            'q': 'Rangoli Ltd, an Indian listed company, has 1,20,00,000 equity shares. Alpine GmbH (Germany) buys 18,00,000 shares and nominates two directors. Bayside Fund (Singapore) buys 7,20,000 shares purely for returns. Later Bayside buys another 6,00,000 shares. Classify each holding under the IMF/OECD convention that India follows.',
            'solution': [table(['Investor', 'Working', 'Stake', 'Classification'], [
                ['Alpine GmbH', '18,00,000 ÷ 1,20,00,000 × 100', f'{fx(s_a)}%', 'FDI — at least 10% and a lasting interest with influence on management'],
                ['Bayside Fund (first purchase)', '7,20,000 ÷ 1,20,00,000 × 100', f'{fx(s_b)}%', 'FPI — below 10%, held only as a financial investment'],
                ['Bayside Fund (after second purchase)', '13,20,000 ÷ 1,20,00,000 × 100', f'{fx(s_c)}%', 'Crosses 10% → treated as FDI under the convention'],
            ]), note('The 10% line is a convention for classifying flows: at or above 10% of ordinary shares or voting power by a non-resident = FDI; below 10% = portfolio investment.')],
            'checks': c1}

    # ---------- Illustration 2: components of FDI ----------
    c2 = Checks()
    tot = c2.add('640+185+95', 'total FDI (US$ million)')
    ill2 = {'id': 'i2', 'title': 'The three components of FDI', 'difficulty': 'core', 'minutes': 5,
            'q': 'A US parent\'s Indian subsidiary reports for the year (US$ million): fresh equity received from the parent 640; profits retained in India instead of being paid as dividends 185; loan received from the parent 95; dividend paid to the parent 60. Compute the FDI for the year.',
            'solution': [table(['Component', 'US$ million'], [['Equity capital', 640], ['Reinvested earnings', 185], ['Other direct capital — intra-company loan', 95], ['Total FDI', tot]], num=[1], total=True),
                         p('Dividends actually paid (60) are investment income flowing out; they are not part of FDI. Only the earnings that stay in the enterprise count, as reinvested earnings.')],
            'checks': c2}

    # ---------- Illustration 3: FDI and the balance of payments ----------
    c3 = Checks()
    y1 = c3.add('500-140-0', 'year 1 net forex: inflow less imported inputs')
    y2 = c3.add('0-140-75', 'year 2 net forex: imported inputs and profit repatriation')
    y3 = c3.add('0-140-75+260', 'year 2 net forex if exports of 260 begin')
    ill3 = {'id': 'i3', 'title': 'Does FDI always help the balance of payments?', 'difficulty': 'moderate', 'minutes': 8,
            'q': 'A foreign carmaker brings US$500 million into India in Year 1 to build a plant. From Year 1 it imports components worth US$140 million a year. From Year 2 it repatriates profits of US$75 million a year. (a) Find the net foreign-exchange effect in Year 1 and Year 2. (b) What if, from Year 2, the plant also exports cars worth US$260 million a year?',
            'solution': [table(['Year', 'Working (US$ million)', 'Net effect'], [
                ['Year 1', '+500 inflow − 140 imported components', f'+{fx(y1)}'],
                ['Year 2 (no exports)', '−140 imports − 75 profits repatriated', f'{fx(y2)}'],
                ['Year 2 (with exports)', '−140 − 75 + 260 exports', f'+{fx(y3)}'],
            ]), p('FDI first brings foreign exchange and supports the rupee, but later imports of inputs and repatriation of profits drain foreign exchange and may weaken the currency — unless the project earns export revenue. This is why host countries sometimes impose export obligations or ceilings on repatriation.')],
            'checks': c3}

    # ---------- Illustration 4: India's FDI figures as given in the study material ----------
    c4 = Checks()
    prev = c4.add('round(81973/1.10)', 'implied previous-year FDI inflow (US$ million), from a 10% rise')
    ma_prev = c4.add('round(27/1.83, 2)', 'implied earlier cross-border M&A (US$ billion), from an 83% rise')
    ill4 = {'id': 'i4', 'title': 'Reading India\'s FDI data from the study material', 'difficulty': 'moderate', 'minutes': 6,
            'q': 'The study material states that India\'s total FDI inflows in 2020-21 were US$81,973 million, 10% higher than the previous financial year, and that cross-border M&A rose 83% to US$27 billion. Work out the approximate base figures these growth rates imply.',
            'solution': [table(['Item', 'Working', 'Implied base'], [
                ['FDI inflows, previous year (2019-20)', '81,973 ÷ 1.10', f'≈ US${inr(prev)} million'],
                ['Cross-border M&A before the 83% rise', '27 ÷ 1.83', f'≈ US${fx(ma_prev)} billion'],
            ]), note('Base = new value ÷ (1 + growth rate). The implied bases are approximations derived from the rounded growth rates; for the exam, remember the figures the material states directly: US$81,973 million (2020-21), +10%; India 8th largest FDI recipient in 2020 (up from 9th in 2019) per the World Investment Report 2022.')],
            'checks': c4}

    concepts = [
        {'id': 'c1', 'title': 'Types of foreign capital', 'body': [
            'Foreign capital is any inflow of capital from abroad; foreign investment is only one part of it. Components: (1) Foreign aid — bilateral (government to government), multilateral (pooled through bodies like the World Bank), tied (use restricted) or untied, and grants (voluntary transfers). (2) Borrowings — inter-government loans, loans from international institutions (World Bank, IMF, ADB), soft loans (e.g. from IDA), external commercial borrowings, and trade credit. (3) Deposits from non-resident Indians. (4) Investment — foreign portfolio investment (FPI) in shares, bonds and other securities, and foreign direct investment (FDI) in enterprises.',
            'This unit concentrates on foreign investment — FDI and FPI.'],
         'analogy': 'Foreign capital is like money coming into a household: gifts (aid), loans (borrowings), relatives\' savings parked with you (NRI deposits), and partners buying a share of the family business (investment).',
         'work': 'Each type is reported differently in the balance of payments and attracts different regulation (ECB rules, FDI policy, FPI limits). CAs advising Indian companies on fund-raising choose among them.'},
        {'id': 'c2', 'title': 'Foreign direct investment (FDI)', 'body': [
            'IMF balance-of-payments definition: investment reflecting a lasting interest and control by a resident of one economy in an enterprise resident in another economy, involving a long-term relationship. Under the IMF/OECD convention (also used by India), a non-resident who acquires 10% or more of an enterprise\'s ordinary shares or voting power is treated as a direct investor.',
            'FDI includes the first transaction and all later transactions between the investor and the enterprise and its affiliates. It has three components: equity capital, reinvested earnings, and other direct capital (intra-company loans between parent and affiliate).',
            'Direct investors may be individuals, companies, groups, governments or their agencies, estates, trusts or other bodies. FDI is real investment — factories, land, inventories — with foreign ownership of production facilities and influence over management in proportion to equity.',
            'Kinds: horizontal (the same business abroad as at home — e.g. a US mobile-service firm providing the same service in India); vertical (a related but different activity that supplements the main business — e.g. a carmaker acquiring a parts or raw-material supplier abroad); conglomerate (an unrelated business, often through a joint venture with a local firm because the investor lacks experience). Two-way FDI: reciprocal investment between countries, each strong in different industries.'],
         'analogy': 'FDI is moving into the neighbourhood and opening your own shop; portfolio investment is buying a few shares of the local shop and watching the price.',
         'work': 'Whether an investment is FDI decides which rules apply — sectoral caps, automatic vs government route, pricing and reporting to RBI. CAs certify valuation and reporting for such transactions.'},
        {'id': 'c3', 'title': 'Foreign portfolio investment (FPI) and the FDI–FPI contrast', 'body': [
            'FPI is a flow of financial capital, not real capital: purchase of shares, bonds and other securities, or bank deposits, by foreigners — without ownership control or management. Its effect falls mainly on the balance of payments and exchange rates rather than on production.',
            'Portfolio investors want a good return, safety and capital appreciation; they have no intention of voting power or managing the company. By international standards, a total stake below 10% is portfolio investment.',
            'FPI is usually short-term, judged security by security, and highly mobile — so it is speculative and can leave quickly when confidence falls, sometimes triggering a financial crisis in the host country.',
            'Contrast: FDI creates physical assets, is long-term and hard to withdraw, is not speculative, often brings technology, directly affects employment and wages, and carries an enduring interest in management. FPI is only in financial assets, short-term, easy to withdraw, speculative, brings no technology, has no direct employment effect and no management interest.'],
         'analogy': 'FDI is planting a tree; FPI is buying fruit from the market — easy to stop buying tomorrow.',
         'work': 'Equity analysts watch FPI flows because sudden FPI selling moves share prices and the rupee; CAs managing listed companies track FPI holding limits.'},
        {'id': 'c4', 'title': 'Why firms invest abroad (reasons and host-country determinants)', 'body': [
            'The main motive is a higher expected return than at home, often because the firm has special assets — superior management, technology, patents or brands — that let it beat local firms.',
            'Other reasons: growing interdependence of economies; internationalisation of production by multinationals; economies of scale; licensing not practical given fast technological change; need to keep control of know-how and patents and to ensure consistent quality; buying a promising foreign firm to remove future competition; risk diversification; common language or nearness saving time and transport cost; capturing large, fast-growing markets; "getting behind the tariff wall" where imports face bans, high duties or NTBs; lower environmental standards; political stability, openness and incentives such as special economic zones; securing raw materials (vertical integration — e.g. petroleum); low wages where labour is abundant; tax differences (a low tax alone cannot fix a weak investment climate); defensive investment to protect competitive position; high GDP, income and growth; good social amenities and quality of life.',
            'Host-country determinants are often grouped as economic (market-seeking — size, income, growth; resource-seeking — raw materials, labour, skills, technology; efficiency-seeking — costs adjusted for productivity, regional integration), the policy framework (stability, entry rules, treatment of foreign affiliates, trade and tax policy, privatisation) and business facilitation (investment promotion, incentives, low "hassle costs", after-investment services).',
            'Discouraging factors: poor infrastructure, high inflation, BoP deficits, low skills, rigid labour markets, bureaucracy and corruption, unfriendly tax regime, legal delays and weak contract enforcement, land acquisition problems, small markets, political instability, unclear property rights, exchange rate volatility, NTBs, strict regulation, language barriers, industrial disputes, insecurity, visa problems for foreign staff, double taxation and an unfriendly attitude to foreign investors.'],
         'analogy': 'A company invests abroad for the same reasons a restaurant opens a branch in another city: more customers, cheaper rent, avoiding the city\'s entry tax on outside food, and keeping its secret recipe in its own kitchen.',
         'work': 'Feasibility reports for inbound and outbound projects list these drivers; a CA quantifies them — market size, cost savings, tax, incentives — into the project\'s cash flows.'},
        {'id': 'c5', 'title': 'Modes of FDI', 'body': [
            'Opening a subsidiary or associate company abroad; injecting equity into an overseas company; acquiring a controlling interest in an existing foreign company; mergers and acquisitions (M&A); joint ventures with a foreign company.',
            'Greenfield investment: a parent sets up a brand-new affiliate abroad and starts production from scratch.',
            'Brownfield investment: uses existing facilities — by merging with, acquiring or leasing them — instead of building new ones. The material notes that India allows 100% FDI under the automatic route in brownfield airport projects.'],
         'analogy': 'Greenfield: buying an empty plot and building a house. Brownfield: buying or renting a house that already stands and renovating it.',
         'work': 'Greenfield vs brownfield changes the valuation, due diligence and accounting (business combination vs asset purchase) a CA performs.'},
        {'id': 'c6', 'title': 'Benefits of FDI for the host country', 'body': [
            'Competition: domestic firms must cut costs, improve quality and innovate; consumers get more variety at lower prices; the power of domestic monopolies weakens.',
            'Capital and growth: investment beyond what domestic savings can fund; more capital per worker raises output (GDP). For developing countries FDI brings capital, technology, management, marketing skills and trained personnel, with spill-overs to local firms.',
            'Employment: direct jobs in new plants and indirect jobs through backward and forward linkages and ancillary units, with multiplier effects on income; higher wages for skilled work and more low-end service jobs.',
            'External sector: access to foreign markets and global marketing networks boosts exports and earns foreign exchange; FDI is non-debt finance, considered better for the balance of payments than external borrowing.',
            'Others: new tax revenue (if taxes are effective); economies of scale lowering prices; competition among governments for FDI pushing useful legal and policy reforms; better work culture and productivity; people-to-people ties that strengthen bilateral relations.'],
         'analogy': 'A good tenant in a building pays rent, hires the neighbours\' kids, sets a higher standard everyone copies, and brings friends from outside.',
         'work': 'Government incentive applications and impact assessments of FDI projects quantify these benefits — jobs, exports, tax — often with CA certification.'},
        {'id': 'c7', 'title': 'Problems with FDI, safeguards, and FDI in India', 'body': [
            'Critics see foreign capital as profit-driven and indifferent to development needs. Problems: capital-intensive methods unsuitable for labour-abundant countries; regional and income inequality as FDI goes to well-endowed regions; governments relaxing efforts to raise domestic savings, and tax revenue lost to tax holidays; crowding-out when foreign firms borrow locally and push up interest rates; BoP and exchange-rate instability from imported inputs and profit repatriation; only routine jobs left in the host country; production distorted towards elite and non-essential goods; aggressive advertising and anti-competitive practices; deep-pocketed firms driving out local firms and acting as monopolies, and wage escalation hurting domestic competitiveness; off-shoring hurting jobs in the home country; exploitation of weak labour and environmental standards and of natural resources; national-security concerns; worse commodity terms of trade when export volumes push down export prices; a dual economy; and loss of policy control and sovereignty, including corruption and undue influence.',
            'No general verdict is possible — each case must be judged on its merits. Safeguards used by countries: domestic-content rules, sectors reserved for local firms, minimum local employment, ceilings on profit repatriation, local sourcing, and export obligations.',
            'FDI in India (as per the study material): a key driver of growth and a significant non-debt resource. Total FDI inflows reached a record US$81,973 million in 2020-21, 10% higher than the previous year; the World Investment Report 2022 ranked India 8th among major FDI recipients in 2020 (9th in 2019). IT, telecom and automobiles were major recipients in FY22; cross-border M&A rose 83% to US$27 billion. FDI has been liberalised through higher sectoral caps, more activities under the automatic route and easier conditions.',
            'Overseas direct investment by Indian companies (outbound FDI): consumption and investment drive about 70% of India\'s economic activity; a resilient economy lets Indian firms invest abroad, bringing back knowledge spill-overs — a mutual benefit. The summary notes outward FDI of US$1.86 billion in June 2016.'],
         'analogy': 'FDI is a powerful medicine: the dose and the patient\'s condition decide whether it heals or harms.',
         'work': 'CAs help clients navigate India\'s FDI policy (caps, routes, reporting) and overseas investment rules for Indian companies setting up subsidiaries abroad.'},
    ]

    mcqs = [
        M('m1', 'Which of the following is NOT a component of foreign capital?', ['Domestic savings of households', 'Foreign aid', 'External commercial borrowings', 'NRI deposits'], 0, 'Domestic savings are domestic capital.', 'c1'),
        M('m2', 'Aid given on condition that it is spent on specified goods or projects is:', ['Tied aid', 'Untied aid', 'A grant without conditions', 'Portfolio investment'], 0, 'Untied aid carries no such stipulation.', 'c1'),
        M('m3', 'Under the IMF/OECD convention, a non-resident\'s investment is FDI if it acquires at least ___ of ordinary shares or voting power.', ['10%', '26%', '51%', '5%'], 0, 'India follows the same 10% convention.', 'c2', 'core', '10'),
        M('m4', 'A foreign company buys 9,00,000 of the 60,00,000 shares of an Indian company and appoints a director. Its stake (which decides FDI vs FPI) is:', ['15%', '9%', '6.67%', '1.5%'], 0, '9,00,000 ÷ 60,00,000 × 100 = 15% — at least 10%, so it is FDI.', 'c2', 'moderate', '900000/6000000*100'),
        M('m5', 'Which is NOT a component of FDI?', ['Dividends paid to the foreign parent', 'Equity capital', 'Reinvested earnings', 'Intra-company loans'], 0, 'Dividends paid out are investment income, not FDI.', 'c2'),
        M('m6', 'An affiliate receives equity of US$400 million, retains earnings of US$90 million and receives a parent loan of US$60 million; it pays dividends of US$50 million. FDI for the year (US$ million) is:', ['550', '500', '600', '490'], 0, '400 + 90 + 60 = 550. Dividends paid are excluded.', 'c2', 'hard', '400+90+60'),
        M('m7', 'A US mobile-service provider sets up the same service in India. This is:', ['Horizontal FDI', 'Vertical FDI', 'Conglomerate FDI', 'Portfolio investment'], 0, 'Same business abroad as at home.', 'c2'),
        M('m8', 'A carmaker acquires an overseas company that supplies its steel and components. This is:', ['Vertical FDI', 'Horizontal FDI', 'Conglomerate FDI', 'Two-way FDI'], 0, 'A related activity that supplements the main business.', 'c2'),
        M('m9', 'An investor puts money abroad into a business unrelated to its home business, usually through a joint venture. This is:', ['Conglomerate FDI', 'Horizontal FDI', 'Vertical FDI', 'FPI'], 0, 'Joint venture because it lacks experience in that industry.', 'c2'),
        M('m10', 'Reciprocal investment between countries, each advanced in different industries, is called:', ['Two-way direct foreign investment', 'Brownfield investment', 'Portfolio investment', 'Tied aid'], 0, 'E.g. one country strong in computers, another in automobiles.', 'c2'),
        M('m11', 'Foreign portfolio investment is the flow of:', ['Financial capital without control over the enterprise', 'Real capital with management control', 'Aid from multilateral institutions', 'Intra-company loans'], 0, 'FPI does not involve ownership control or management.', 'c3'),
        M('m12', 'Which is TRUE of FPI compared with FDI?', ['It is easy to withdraw and speculative', 'It brings technology transfer', 'It has a direct impact on employment', 'It involves an enduring interest in management'], 0, 'The other three describe FDI.', 'c3'),
        M('m13', 'The chief motive for capital to move across borders is:', ['Expectation of a higher rate of return than at home', 'Charity', 'Exchange rate stability', 'Higher taxes abroad'], 0, 'Profit motive, often based on firm-specific assets.', 'c4'),
        M('m14', 'Investing in a country to avoid its high import duties and non-tariff barriers is called:', ['Getting behind the tariff wall', 'Dumping', 'Off-shoring', 'Crowding out'], 0, 'Producing inside the market avoids the import barriers.', 'c4'),
        M('m15', 'A firm acquires a foreign mine to secure uninterrupted supply of a raw material at low cost. This is mainly a form of:', ['Vertical integration', 'Horizontal integration', 'Portfolio diversification', 'Conglomerate diversification'], 0, 'Control of strategic inputs = vertical integration.', 'c4'),
        M('m16', 'Which factor DISCOURAGES FDI inflows into a host country?', ['Exchange rate volatility', 'Large and growing market', 'Political stability', 'Special economic zones'], 0, 'Volatility raises risk; the others attract FDI.', 'c4'),
        M('m17', 'Setting up a brand-new production facility abroad is:', ['Greenfield investment', 'Brownfield investment', 'Portfolio investment', 'A merger'], 0, 'Brownfield uses existing facilities.', 'c5'),
        M('m18', 'Acquiring or leasing an existing plant abroad instead of building a new one is:', ['Brownfield investment', 'Greenfield investment', 'FPI', 'Two-way FDI'], 0, 'E.g. India allows 100% FDI via the automatic route in brownfield airport projects.', 'c5'),
        M('m19', 'Which is NOT a mode of FDI?', ['Buying 2% of a foreign company\'s listed shares purely for dividends', 'Opening a subsidiary abroad', 'A joint venture with a foreign firm', 'Acquiring a controlling interest in a foreign company'], 0, 'A 2% purely financial stake is portfolio investment.', 'c5'),
        M('m20', 'Which is a benefit of FDI to the host country?', ['Weakening the market power of domestic monopolies', 'Crowding out domestic investment', 'Regional disparity', 'Profit repatriation'], 0, 'The other three are problems.', 'c6'),
        M('m21', 'FDI is considered better for the balance of payments than external borrowing mainly because it:', ['Is non-debt finance with no fixed repayment', 'Is always short-term', 'Never repatriates profits', 'Is speculative'], 0, 'No fixed interest and principal repayment obligations.', 'c6'),
        M('m22', 'Jobs created in supplier and distributor firms because of a new foreign plant are due to:', ['Backward and forward linkages', 'Crowding out', 'Off-shoring', 'Tied aid'], 0, 'Indirect employment through linkages.', 'c6'),
        M('m23', 'When foreign firms borrow heavily in the host country\'s capital market, raising interest rates and reducing domestic investment, this is:', ['Crowding-out', 'Spill-over', 'Two-way FDI', 'Trade deflection'], 0, 'A potential problem of FDI.', 'c7'),
        M('m24', 'FDI may worsen the host country\'s commodity terms of trade when:', ['Export-oriented FDI raises export volumes enough to push down export prices', 'Imports become cheaper', 'The host is a very small exporter', 'FDI goes only into services for the home market'], 0, 'Terms of trade = export prices ÷ import prices.', 'c7', 'hard'),
        M('m25', 'Which is a safeguard used by host countries to improve the benefit–cost ratio of FDI?', ['Ceiling on repatriation of profits', 'Unlimited tax holidays', 'Abolishing local-content rules', 'Allowing only capital-intensive projects'], 0, 'Others listed in the material: domestic content, reserved sectors, local employment, export obligations.', 'c7'),
        M('m26', 'As per the study material, India\'s total FDI inflows in 2020-21 were (US$ million):', ['81,973', '58,770', '27,000', '1,860'], 0, 'A record, 10% higher than the previous year.', 'c7', 'core', '81973'),
        M('m27', 'According to the World Investment Report 2022 (as quoted in the material), India\'s rank among major FDI recipients in 2020 was:', ['8th', '9th', '7th', '1st'], 0, 'Up from 9th in 2019.', 'c7', 'moderate'),
        M('m28', 'FDI inflows of US$81,973 million represent a 10% rise over the previous year. The implied previous-year inflow (US$ million) is approximately:', ['74,521', '73,776', '90,170', '81,963'], 0, '81,973 ÷ 1.10 ≈ 74,521. Subtracting 10% of 81,973 (= 73,776) is the common mistake.', 'c7', 'hard', 'round(81973/1.1)'),
        M('m29', 'Cross-border M&A in India, as noted in the material, rose by 83% to (US$ billion):', ['27', '83', '81.97', '1.86'], 0, 'Driven by technology and health-sector deals.', 'c7', 'core', '27'),
        M('m30', 'According to the material, consumption and investment account for about ___ of India\'s economic activity.', ['70%', '50%', '30%', '90%'], 0, 'India is mainly a domestic-demand-driven economy.', 'c7', 'core', '70'),
    ]

    cq1 = Checks()
    k1 = cq1.add('2400000/20000000*100', 'Kestrel stake %')
    k2 = cq1.add('1500000/20000000*100', 'Lumen stake %')
    k3 = cq1.add('520+110+70', 'Kestrel FDI components total')
    q1 = Q('q1', 5, 'moderate', 'table', 'Vistara Foods Ltd has 2,00,00,000 equity shares. Kestrel Inc. (USA) acquires 24,00,000 shares and a board seat; Lumen Capital (UK) buys 15,00,000 shares as a trading investment. During the year Kestrel also retains US$110 million of profits in its own Indian subsidiary, injects US$520 million equity into it and lends it US$70 million. (a) Classify the two investments in Vistara. (b) Compute Kestrel\'s FDI into its subsidiary for the year.',
           [table(['Item', 'Working', 'Result'], [['Kestrel in Vistara', '24,00,000 ÷ 2,00,00,000 × 100', f'{fx(k1)}% → FDI'], ['Lumen in Vistara', '15,00,000 ÷ 2,00,00,000 × 100', f'{fx(k2)}% → FPI'],
                                                  ['FDI into subsidiary', 'Equity 520 + reinvested earnings 110 + intra-company loan 70', f'US${fx(k3)} million']])],
           [S('s1', 'Stake of Kestrel', 1, 'computation'), S('s2', 'Stake of Lumen', 1, 'computation'), S('s3', 'Correct use of 10% convention', 1, 'application'), S('s4', 'Three components identified', 1, 'concept'), S('s5', 'Total FDI', 1, 'computation')],
           ['Many forget that reinvested earnings count as FDI.'], ['Classifying by intention alone, ignoring the 10% line.', 'Adding dividends to FDI.'], ['Show the percentage before the label.'], checks=cq1)

    cq2 = Checks()
    n1 = cq2.add('800-210', 'year 1 net forex')
    n2 = cq2.add('-210-120', 'year 2 net forex without exports')
    n3 = cq2.add('-210-120+400', 'year 2 net forex with exports')
    q2 = Q('q2', 4, 'moderate', 'table', 'A foreign electronics firm invests US$800 million in India in Year 1 and imports parts worth US$210 million every year. From Year 2 it repatriates profits of US$120 million a year. Compute the net foreign-exchange effect in Year 1 and Year 2, and in Year 2 if it starts exporting US$400 million a year. Comment.',
           [table(['Year', 'Working (US$ million)', 'Net'], [['Year 1', '800 − 210', f'+{fx(n1)}'], ['Year 2', '−210 − 120', fx(n2)], ['Year 2 with exports', '−210 − 120 + 400', f'+{fx(n3)}']]),
            p('FDI helps the BoP at entry, but imported inputs and repatriation later drain foreign exchange unless the project exports. Hence export obligations and repatriation ceilings.')],
           [S('s1', 'Year 1 net', 1, 'computation'), S('s2', 'Year 2 net without exports', 1, 'computation'), S('s3', 'Year 2 net with exports', 1, 'computation'), S('s4', 'Comment on BoP instability', 1, 'conclusion')],
           ['Good answers end with the policy point (export obligation / repatriation ceiling).'], ['Treating repatriated profit as an inflow.'], ['Use + and − signs consistently.'], checks=cq2)

    q3 = Q('q3', 4, 'core', 'table', 'Distinguish between FDI and FPI on any four points.',
           [table(['Basis', 'FDI', 'FPI'], [
               ['Nature of assets', 'Creation of physical assets', 'Financial assets only'],
               ['Time horizon / withdrawal', 'Long term; hard to withdraw', 'Short term; easy to withdraw'],
               ['Speculation', 'Not inclined to be speculative', 'Speculative'],
               ['Technology', 'Often brings technology transfer', 'No technology transfer'],
               ['Management', 'Enduring interest and influence (≥ 10%)', 'No management interest (< 10%)'],
               ['Employment', 'Direct impact on jobs and wages', 'No direct impact'],
           ])],
           [S('s1', 'Assets created', 1, 'concept'), S('s2', 'Time horizon / ease of withdrawal', 1, 'concept'), S('s3', 'Control / 10% threshold', 1, 'concept'), S('s4', 'Any one more valid point', 1, 'analysis')],
           ['A table with four clear rows earns full marks.'], ['Saying FPI involves management control.'], ['Put the 10% threshold in the management row.'])

    jobs = [
        {'id': 'j1', 'title': 'Is this investment FDI or FPI?', 'role': 'CA advising an Indian unlisted company raising funds',
         'situation': 'A foreign investor wants 12% of your client\'s equity with one board seat; another wants 6% with no rights.',
         'steps': ['Apply the 10% convention: 12% with a board seat is FDI; 6% held as a financial investment is portfolio in nature.', 'Check the sector\'s FDI cap and whether it falls under the automatic or government route.', 'Ensure valuation and pricing guidelines are met and file the required reports on time.', 'Explain to the board the long-term nature of FDI investors versus the mobility of portfolio money.'],
         'takeaway': 'Classification drives the compliance path; get it right before the money arrives.'},
        {'id': 'j2', 'title': 'Greenfield or brownfield?', 'role': 'CA in industry (strategy team of a foreign food company entering India)',
         'situation': 'The board must choose between building a new plant (greenfield) and acquiring an existing Indian plant (brownfield).',
         'steps': ['Greenfield: full control and latest technology, but long gestation, land and approval risks.', 'Brownfield: quick start, existing workforce and licences, but legacy liabilities need due diligence.', 'Compare NPVs with realistic timelines and tax/incentive differences.', 'Recommend with a risk matrix.'],
         'takeaway': 'Mode of FDI changes timing, risk and accounting — model both before deciding.',
         'think': 'Greenfield costs US$60 million and starts earning in 3 years; brownfield costs US$75 million and earns from Year 1. Which is cheaper upfront?', 'answer': 'Greenfield is cheaper upfront by US$15 million, but brownfield earns two years earlier — the decision needs discounted cash flows, not just the price.',
         'checks': Checks([{'expr': '75-60', 'value': 15, 'label': 'upfront cost difference (US$ million)'}])},
    ]

    viva = [
        V('v1', 'What is foreign direct investment?',
          'Foreign direct investment is investment by a resident of one country in an enterprise in another country with a lasting interest and control or significant influence over its management. By convention the investor holds ten percent or more of the ordinary shares or the votes. It consists of equity capital, reinvested earnings and intra-company loans, and usually creates real assets such as factories.',
          [P('p1', 'Lasting interest with control / influence over management in an enterprise abroad', 4, 'lasting|long term|long-term|control|manag|influenc|ownership|say in'),
           P('p2', 'At least 10% of ordinary shares or voting power', 3, '10 percent|10 %|10|ten'),
           P('p3', 'Components: equity, reinvested earnings, intra-company loans / real assets', 3, 'equity|reinvest|retained earn|intra company|intra-company|inter company|loan from parent|factor|plant|real asset|physical asset')], 'c2'),
        V('v2', 'What is foreign portfolio investment?',
          'Foreign portfolio investment is the purchase of shares, bonds and other securities by foreigners purely as a financial investment, without any control over or interest in managing the company. The stake is below ten percent. It is usually short term, easy to withdraw and speculative, so it can leave the country quickly.',
          [P('p1', 'Investment in financial assets / securities (shares, bonds)', 3, 'share|bond|securit|stock|financial asset|financial capital|equity market|deposit'),
           P('p2', 'No control or management interest; stake below 10%', 4, 'no control|not control|without control|no management|not manag|no say|no interest in manag|passive|below 10|less than 10|under 10|below ten|less than ten|no voting|only return|purely financial|just for return'),
           P('p3', 'Short term, easy to withdraw, speculative / volatile', 3, 'short term|short-term|easy to withdraw|easily withdrawn|withdraw|speculat|volatil|hot money|leave quickly|move quickly|exit quickly|footloose|mobile')], 'c3'),
        V('v3', 'Explain horizontal, vertical and conglomerate FDI.',
          'Horizontal FDI is when a firm sets up the same business abroad that it runs at home, like a mobile operator offering the same service in another country. Vertical FDI is when it invests in a related activity that supplies or supports its main business, such as a carmaker buying a parts supplier abroad. Conglomerate FDI is investment in an unrelated business, often through a joint venture.',
          [P('p1', 'Horizontal = same business abroad', 3, linked(('horizontal',), ('same', 'similar', 'identical', 'same type', 'like'))),
           P('p2', 'Vertical = related activity that supplies / supports the main business', 4, linked(('vertical',), ('supplier', 'supply', 'supplies', 'related', 'support', 'supplement', 'raw material', 'parts', 'component', 'input', 'upstream', 'downstream', 'value chain', 'complement', 'different'))),
           P('p3', 'Conglomerate = unrelated business (often a JV)', 3, linked(('conglomerate',), ('unrelated', 'different', 'not related', 'no relation', 'diversif', 'new line', 'other business', 'joint venture')))], 'c2'),
        V('v4', 'Why do firms make foreign direct investment?',
          'Firms invest abroad mainly to earn a higher return than at home, using their special assets like technology, patents or management skills. They also want to capture large growing markets, get behind tariff walls, secure raw materials, use cheaper labour, reap economies of scale, diversify risk and take advantage of tax incentives and stable policies.',
          [P('p1', 'Higher return / profit than at home', 4, 'higher return|more return|better return|profit|higher rate of return|earn more|return'),
           P('p2', 'Market access — large growing markets, behind tariff walls', 2, 'market|tariff wall|behind tariff|avoid tariff|avoid dut|import barrier|trade barrier'),
           P('p3', 'Cost / resources — cheap labour, raw materials, economies of scale', 2, 'labour|labor|wage|raw material|resource|economies of scale|scale|cost'),
           P('p4', 'Risk diversification, incentives, stability, control of know-how', 2, 'diversif|risk|tax|incentiv|stable|stability|patent|technolog|know how|knowhow|special economic zone|sez|control')], 'c4'),
        V('v5', 'What are the main benefits of FDI to a host country?',
          'FDI brings additional capital beyond domestic savings, along with technology, management and marketing skills. It creates direct and indirect employment through linkages, increases competition so consumers get better products at lower prices, improves access to export markets and foreign exchange, and as non-debt finance it is better for the balance of payments than borrowing.',
          [P('p1', 'Capital beyond domestic savings; technology and skills', 3, 'capital|fund|savings|investment|technolog|know how|skill|management'),
           P('p2', 'Employment — direct and indirect (linkages)', 3, 'employment|jobs|job|linkage|ancillar|work'),
           P('p3', 'Competition — better, cheaper products; curbs monopolies', 2, 'competit|cheaper|lower price|quality|variety|monopol|efficien'),
           P('p4', 'Exports, foreign exchange, non-debt BoP support', 2, 'export|foreign exchange|forex|balance of payment|bop|non debt|non-debt|tax revenue|revenue')], 'c6'),
        V('v6', 'What problems can FDI create for a developing host country?',
          'FDI may use capital-intensive methods that create few jobs, widen regional and income inequality, crowd out domestic firms by borrowing locally, strain the balance of payments through imported inputs and profit repatriation, exploit natural resources and weak standards, create monopolies and a dual economy, and reduce the host government\'s control over policy.',
          [P('p1', 'Capital-intensive methods, few jobs; inequality', 3, 'capital intensive|capital-intensive|few jobs|less employment|fewer jobs|inequal|disparit|unemploy'),
           P('p2', 'Crowding out; monopoly; local firms driven out', 2, 'crowd|monopol|drive out|domestic firms|local firms|competition|market power'),
           P('p3', 'BoP strain — imported inputs, profit repatriation', 3, 'repatriat|profit outflow|imported input|balance of payment|bop|exchange rate|outflow|currency'),
           P('p4', 'Resource exploitation, environment, sovereignty / policy control', 2, 'exploit|environment|natural resource|sovereign|policy control|influenc|dual economy|security|pollut|corrupt')], 'c7'),
        V('v7', 'Distinguish between greenfield and brownfield investment.',
          'Greenfield investment means a parent company builds a completely new facility abroad and starts production from scratch. Brownfield investment uses existing facilities by merging with, acquiring or leasing them instead of building new ones; for example India allows full FDI through the automatic route in brownfield airport projects.',
          [P('p1', 'Greenfield = brand-new facility built from scratch', 5, linked(('greenfield', 'green field'), ('new', 'fresh', 'scratch', 'build', 'built', 'construct', 'empty', 'own plant', 'start from'))),
           P('p2', 'Brownfield = existing facility acquired, merged or leased', 5, linked(('brownfield', 'brown field'), ('exist', 'already', 'acquir', 'merg', 'lease', 'buy', 'purchas', 'take over', 'old', 'running')))], 'c5'),
    ]

    case = {'id': 'k1', 'title': 'Two foreign investors and a new plant', 'difficulty': 'hard',
            'case': ('Nimbus Corp, a Japanese carmaker, buys 30,00,000 of the 1,50,00,000 shares of Sahyadri Motors Ltd and nominates two directors; it also acquires an Indian firm that makes seats and dashboards for Sahyadri. '
                     'Orchid Fund (Mauritius) buys 9,00,000 Sahyadri shares, and sells them within four months when the market falls. Nimbus\'s own new Indian plant is built on an empty plot; it imports electronics worth US$90 million a year and, from Year 2, repatriates profits of US$40 million a year.'),
            'mcqs': [
                M('k5a', 'Nimbus\'s percentage stake in Sahyadri is:', ['20%', '6%', '30%', '2%'], 0, '30,00,000 ÷ 1,50,00,000 × 100 = 20% — at least 10% and with board influence, so FDI.', 'c2', 'moderate', '3000000/15000000*100'),
                M('k5b', 'Orchid\'s holding and behaviour illustrate:', ['FPI — a 6% stake, short-term and quickly withdrawn', 'FDI — long-term control', 'Conglomerate FDI', 'Greenfield investment'], 0, '9,00,000 ÷ 1,50,00,000 = 6% (< 10%), sold quickly when confidence fell.', 'c3', 'moderate'),
                M('k5c', 'Nimbus acquiring the seat-and-dashboard maker is an example of:', ['Vertical FDI', 'Horizontal FDI', 'Conglomerate FDI', 'Portfolio investment'], 0, 'A supplier of parts to its main business.', 'c2', 'core'),
                M('k5d', 'Nimbus\'s new plant on an empty plot is a:', ['Greenfield investment', 'Brownfield investment', 'Merger', 'Two-way investment'], 0, 'Built from scratch.', 'c5', 'core'),
                M('k5e', 'From Year 2, the plant\'s annual drain on foreign exchange (imports plus repatriation, no exports) is (US$ million):', ['130', '50', '90', '40'], 0, '90 + 40 = 130 — the BoP-instability problem of FDI.', 'c7', 'moderate', '90+40'),
            ]}

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch09', 'n': 5, 'title': 'International Capital Movements',
        'outcomes': ['Identify the types of foreign capital — aid, borrowings, NRI deposits and investment.',
                     'Define FDI (10% convention, components, horizontal/vertical/conglomerate) and FPI, and distinguish them.',
                     'Explain the reasons for FDI, host-country determinants and discouraging factors, and the modes of FDI including greenfield and brownfield.',
                     'Evaluate the benefits and problems of FDI for host countries and recall the FDI-in-India figures given in the study material.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 45}, 'prereq': ['fnd-p4-ch09-u04'],
                 'exam_tip': 'The FDI vs FPI table, the 10% threshold, the three components of FDI and horizontal/vertical/conglomerate examples are standard MCQs. Learn the India figures exactly as the material states them, with the year.'},
        'concepts': concepts, 'illustrations': [ill1, ill2, ill3, ill4], 'jobs': jobs, 'mcqs': mcqs, 'questions': [q1, q2, q3],
        'revision': {'summary': ['Foreign capital = aid (bilateral, multilateral, tied/untied, grants) + borrowings (govt, IMF/World Bank/ADB, soft loans, ECB, trade credit) + NRI deposits + investment (FPI, FDI).',
                                 'FDI: lasting interest and control; ≥ 10% of ordinary shares/voting power (IMF/OECD, India); components = equity + reinvested earnings + intra-company loans.',
                                 'Horizontal (same business) · vertical (supplier/related) · conglomerate (unrelated, often JV) · two-way FDI.',
                                 'FPI: financial assets, < 10%, no control, short-term, easy to withdraw, speculative.',
                                 'Reasons: higher return, special assets, markets, tariff walls, resources, cheap labour, scale, risk diversification, incentives.',
                                 'Modes: subsidiary, equity injection, controlling interest, M&A, JV, greenfield (new), brownfield (existing).',
                                 'Benefits: capital, technology, jobs, competition, exports, non-debt BoP support. Problems: capital-intensive, inequality, crowding-out, BoP strain, monopoly, exploitation, sovereignty.',
                                 'India (material): FDI US$81,973 million in 2020-21 (+10%); WIR 2022 ranked India 8th in 2020 (9th in 2019); cross-border M&A +83% to US$27 billion.'],
                     'remember': ['Stake % = shares acquired ÷ total shares × 100; ≥ 10% → FDI.', 'Dividends paid are NOT FDI; reinvested earnings ARE.', 'Base = new value ÷ (1 + growth).'],
                     'traps': ['FPI does not bring technology or management.', 'Vertical ≠ horizontal: supplier vs same business.', 'FDI can strain the BoP later through repatriation and imports.']},
        'quickref': [{'k': 'FDI threshold', 'v': '≥ 10% of ordinary shares / voting power by a non-resident'}, {'k': 'FDI components', 'v': 'Equity capital + reinvested earnings + intra-company loans'},
                     {'k': 'Horizontal / vertical / conglomerate', 'v': 'Same business / related supplier / unrelated'}, {'k': 'FPI', 'v': '< 10%, financial assets, no control, short-term, speculative'},
                     {'k': 'Greenfield vs brownfield', 'v': 'New facility from scratch vs existing facility acquired/leased'}, {'k': 'India FDI 2020-21 (material)', 'v': 'US$81,973 million, +10%'},
                     {'k': 'WIR 2022 (material)', 'v': 'India 8th largest FDI recipient in 2020 (9th in 2019)'}],
        'viva': viva, 'cases': [case],
    }
