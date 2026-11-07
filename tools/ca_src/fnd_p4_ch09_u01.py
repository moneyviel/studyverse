"""CA Foundation · Paper 4 Business Economics · Chapter 9 International Trade · Unit 1 Theories of International Trade.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py.
This module also holds the small helpers (M, Q, S, V, P, ALT) re-used by the other Chapter 9 / Chapter 10 units."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch09-u01'


def M(mid, q, options, answer, explain, concept=None, difficulty='core', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'difficulty': difficulty}
    if topic: d['topic'] = topic
    if concept: d['concept'] = concept
    if check is not None: d['check'] = check
    return d


def S(sid, pt, m, skill):
    return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def Q(qid, marks, difficulty, pad, q, model, scheme, remarks, mistakes, tips, checks=None, given=None):
    d = {'id': qid, 'marks': marks, 'minutes': minutes(marks), 'difficulty': difficulty, 'pad': pad, 'q': q, 'model': model,
         'scheme': scheme, 'remarks': remarks, 'mistakes': mistakes, 'tips': tips}
    if checks: d['checks'] = checks
    if given: d['given'] = given
    return d


def fx(v, nd=2):
    """Plain number for prose: 0.5 -> '0.5', 1.3333 -> '1.33', 4.0 -> '4'."""
    v = round(v, nd)
    return str(int(v)) if v == int(v) else f'{v:.{nd}f}'.rstrip('0').rstrip('.')


def build():
    # ---------------- Illustration 1: absolute advantage ----------------
    c1 = Checks()
    a_tot = c1.add('4+10', 'Alpha: hours to make one unit of each good')
    b_tot = c1.add('8+5', 'Beta: hours to make one unit of each good')
    a_tea = c1.add('14/4', 'Alpha puts all 14 hours into tea')
    b_cl = c1.add('13/5', 'Beta puts all 13 hours into cloth')
    g_tea = c1.add('3.5-2', 'extra tea for the world')
    g_cl = c1.add('2.6-2', 'extra cloth for the world')
    ill1 = {'id': 'i1', 'title': 'Absolute advantage — who makes what?', 'difficulty': 'core', 'minutes': 8,
            'q': 'Labour hours needed for one unit: Alpha — tea 4 hours, cloth 10 hours; Beta — tea 8 hours, cloth 5 hours. Before trade each country makes one unit of each good. (a) Which country has an absolute advantage in which good? (b) If each country moves all its hours into the good of its absolute advantage, how much extra output does the world get?',
            'given': [table(['Good', 'Alpha (hours per unit)', 'Beta (hours per unit)'], [['Tea', 4, 8], ['Cloth', 10, 5]], num=[1, 2])],
            'solution': [table(['Step', 'Working', 'Result'], [
                ['Compare hours for tea', 'Alpha 4 < Beta 8', 'Alpha has the absolute advantage in tea'],
                ['Compare hours for cloth', 'Beta 5 < Alpha 10', 'Beta has the absolute advantage in cloth'],
                ['Hours available (one unit of each)', f'Alpha 4 + 10 = {a_tot}; Beta 8 + 5 = {b_tot}', '—'],
                ['Alpha specialises in tea', f'{a_tot} ÷ 4', f'{fx(a_tea)} units of tea'],
                ['Beta specialises in cloth', f'{b_tot} ÷ 5', f'{fx(b_cl)} units of cloth'],
                ['Gain to the world', f'Tea {fx(a_tea)} − 2; cloth {fx(b_cl)} − 2', f'+{fx(g_tea)} tea and +{fx(g_cl)} cloth'],
            ]), note('Adam Smith\'s rule: each country exports the good it makes with fewer labour hours than the other country. Same labour, more total output — that is the gain from trade.')],
            'checks': c1}

    # ---------------- Illustration 2: comparative advantage, Ricardo ----------------
    c2 = Checks()
    p_w = c2.add('3/6', 'P: cloth given up for 1 wheat')
    q_w = c2.add('9/12', 'Q: cloth given up for 1 wheat')
    p_c = c2.add('6/3', 'P: wheat given up for 1 cloth')
    q_c = c2.add('12/9', 'Q: wheat given up for 1 cloth')
    adv_w = c2.add('9/3', 'P is this many times as productive in wheat')
    adv_c = c2.add('12/6', 'P is this many times as productive in cloth')
    p_cost_import = c2.add('(1/0.6)*3', 'P: hours spent making the wheat it swaps for 1 cloth')
    p_save = c2.add('6-(1/0.6)*3', 'P: hours saved on each cloth imported')
    q_cost_import = c2.add('0.6*12', 'Q: hours spent making the cloth it swaps for 1 wheat')
    q_save = c2.add('9-0.6*12', 'Q: hours saved on each wheat imported')
    ill2 = {'id': 'i2', 'title': 'Comparative advantage when one country is better at everything', 'difficulty': 'moderate', 'minutes': 12,
            'q': 'Hours of labour for one unit: Country P — wheat 3, cloth 6; Country Q — wheat 9, cloth 12. (a) Show that P has an absolute advantage in both goods. (b) Find the opportunity cost of each good in each country and state which good each should export. (c) Within what range must the terms of trade (cloth per unit of wheat) lie? (d) If they trade at 1 wheat = 0.6 cloth, how many labour hours does each country save per unit imported?',
            'given': [table(['Good', 'P (hours per unit)', 'Q (hours per unit)'], [['Wheat', 3, 9], ['Cloth', 6, 12]], num=[1, 2])],
            'solution': [table(['Measure', 'Country P', 'Country Q', 'Lower cost'], [
                ['Hours for 1 wheat', '3', '9', 'P (absolute)'],
                ['Hours for 1 cloth', '6', '12', 'P (absolute)'],
                ['Opportunity cost of 1 wheat (cloth forgone)', f'3 ÷ 6 = {fx(p_w)}', f'9 ÷ 12 = {fx(q_w)}', 'P → P exports wheat'],
                ['Opportunity cost of 1 cloth (wheat forgone)', f'6 ÷ 3 = {fx(p_c)}', f'12 ÷ 9 = {fx(q_c)}', 'Q → Q exports cloth'],
            ], title='Step 1 and 2: absolute and comparative cost'),
                wn('Ricardo\'s ratio test', f'P is {fx(adv_w)} times as productive in wheat (9 ÷ 3) but only {fx(adv_c)} times in cloth (12 ÷ 6). Its advantage is greatest in wheat, so it exports wheat; Q\'s disadvantage is smallest in cloth, so Q exports cloth.'),
                wn('Step 3: terms of trade', f'Both gain only if 1 wheat exchanges for more than P\'s home cost ({fx(p_w)} cloth) and less than Q\'s home cost ({fx(q_w)} cloth). Range: {fx(p_w)} < cloth per wheat < {fx(q_w)}. The rate 0.6 lies inside, so both gain.'),
                table(['Country', 'Home cost of the import', 'Cost through trade at 1 W = 0.6 C', 'Hours saved per unit'], [
                    ['P (imports cloth)', '6 hours', f'1 ÷ 0.6 = {fx(1/0.6)} wheat × 3 = {fx(p_cost_import)} hours', fx(p_save)],
                    ['Q (imports wheat)', '9 hours', f'0.6 cloth × 12 = {fx(q_cost_import)} hours', fx(q_save)],
                ], title='Step 4: gain in labour hours')],
            'checks': c2}

    # ---------------- Illustration 3: Haberler opportunity cost from output data ----------------
    c3 = Checks()
    x_ph = c3.add('400/100', 'X: coffee forgone per phone')
    y_ph = c3.add('120/60', 'Y: coffee forgone per phone')
    x_cf = c3.add('100/400', 'X: phones forgone per kg coffee')
    y_cf = c3.add('60/120', 'Y: phones forgone per kg coffee')
    ill3 = {'id': 'i3', 'title': 'Opportunity cost from production possibilities (Haberler)', 'difficulty': 'moderate', 'minutes': 8,
            'q': 'Using all its resources, Country X can make either 100 phones or 400 kg of coffee; Country Y can make either 60 phones or 120 kg of coffee (constant costs). Which country has the comparative advantage in phones and which in coffee?',
            'solution': [table(['Country', 'Coffee forgone per phone', 'Phones forgone per kg coffee'], [
                ['X', f'400 ÷ 100 = {fx(x_ph)}', f'100 ÷ 400 = {fx(x_cf)}'],
                ['Y', f'120 ÷ 60 = {fx(y_ph)}', f'60 ÷ 120 = {fx(y_cf)}'],
            ]), p(f'Phones: Y gives up only {fx(y_ph)} kg of coffee per phone against {fx(x_ph)} kg in X, so Y has the comparative advantage in phones. Coffee: X gives up only {fx(x_cf)} phone per kg against {fx(y_cf)} in Y, so X has the comparative advantage in coffee.'),
                note('X can make more of both goods (absolute advantage in both), yet Y still has a comparative advantage. Haberler\'s opportunity-cost version needs no labour theory of value — any mix of factors works.')],
            'checks': c3}

    # ---------------- Illustration 4: Heckscher-Ohlin ----------------
    c4 = Checks()
    k_ratio = c4.add('800/200', 'Kestria: capital per worker')
    l_ratio = c4.add('300/600', 'Lumina: capital per worker')
    ill4 = {'id': 'i4', 'title': 'Factor endowments decide exports (Heckscher-Ohlin)', 'difficulty': 'core', 'minutes': 6,
            'q': 'Kestria has 800 units of capital and 200 units of labour. Lumina has 300 units of capital and 600 units of labour. Machine tools are capital-intensive and readymade garments are labour-intensive. Using the Heckscher-Ohlin theory, predict the pattern of trade and the effect on factor prices.',
            'solution': [table(['Country', 'Capital ÷ labour', 'Relatively abundant factor', 'Predicted export'], [
                ['Kestria', f'800 ÷ 200 = {fx(k_ratio)}', 'Capital', 'Machine tools'],
                ['Lumina', f'300 ÷ 600 = {fx(l_ratio)}', 'Labour', 'Readymade garments'],
            ]), p('A country exports the good that uses its abundant (and therefore cheap) factor intensively and imports the good that uses its scarce factor intensively.'),
                p('Factor-price equalisation: as Lumina exports more garments, demand for its labour rises and wages go up; in Kestria the return to capital rises. Free trade pushes wages and returns to capital in the two countries towards each other.')],
            'checks': c4}

    concepts = [
        {'id': 'c1', 'title': 'International trade, its gains and the case against it', 'body': [
            'International trade means buying and selling goods, services and resources across national borders, between residents of different countries. Compared with internal (domestic) trade it is more complex: several currencies, different legal systems, customs procedures, longer distances, language and cultural differences, and limited mobility of labour and capital between countries.',
            'Why countries trade: a bigger market allows specialisation and division of labour; resources move to their most productive use; domestic monopolies face competition; inputs can be sourced cheaply from anywhere; consumers get more variety at lower prices; trade earns the foreign exchange needed to pay for imports; it pushes automation, research and innovation; it widens the market for services such as banking, insurance and logistics; it helps emerging economies climb the global value chain, diversify exports, share know-how and build friendly relations with other nations.',
            'The case against free trade: gains may be unequal between rich and poor nations; weaker countries may be exploited by powerful global corporations; natural resources may be used up fast and the environment harmed; booms and slumps spread quickly from one country to another; heavy dependence on foreign supplies can threaten economic and even political independence, especially during wars; too much export focus can pull investment away from a country\'s real needs; and trade partners may suddenly change policy — bans, high tariffs or embargoes.'],
         'analogy': 'Trade is like a neighbourhood where the baker bakes and the tailor stitches: everyone eats and dresses better than if each did both badly. But if one shop owns the whole street, the others may lose out.',
         'work': 'Export-import businesses, their auditors and lenders keep watching for currency risk, sudden policy changes (a duty hike or an import ban) and dependence on one foreign supplier. Spotting these risks early is part of business advisory and going-concern work.'},
        {'id': 'c2', 'title': 'Mercantilism — trade as a way to pile up gold', 'body': [
            'Mercantilism was the dominant economic idea in Europe from roughly the 16th to the 18th century. It held that a nation\'s wealth and power depended on its stock of gold and silver (precious metals).',
            'So the state should push exports up and keep imports down, aiming for a permanent trade surplus (a favourable balance of trade). Governments controlled industry and trade and put very high tariffs on foreign goods.',
            'Weakness: trade was seen as a zero-sum game — one nation\'s gain was another\'s loss. Later economists showed that both trading partners can gain. Traces of mercantilist thinking still appear whenever a country treats a trade surplus as a goal in itself.'],
         'analogy': 'A shopkeeper who loves selling but refuses to buy anything, counting coins every night — rich in coins, poor in comforts.',
         'work': 'When a government announces export push schemes together with import curbs, analysts call it "neo-mercantilist". Understanding the motive helps a CA forecast which sectors will get protection and which will face higher input costs.'},
        {'id': 'c3', 'title': 'Absolute advantage — Adam Smith', 'body': [
            'Adam Smith argued that trade rests on absolute cost differences. A country has an absolute advantage in a good if it can make it with less labour (fewer resources) than another country.',
            'If Country A is absolutely better at one good and Country B at another, each should specialise in its own good and trade; total world output rises and both gain.',
            'Assumptions: two countries and two goods; no transport cost; cost measured by the labour needed (labour theory of value); labour moves freely within a country but not between countries; trade happens only when each country has an absolutely lower cost in one good.',
            'Limitation: if one country is absolutely better at both goods, the theory predicts no trade at all — yet such trade happens in real life. Ricardo filled this gap.'],
         'analogy': 'A fast cook and a fast typist living together: the cook cooks, the typist types, and both finish earlier.',
         'work': 'Sourcing decisions often begin with a simple absolute-cost comparison — which country makes this component cheapest? A CA preparing a make-or-import analysis starts here before adding duties, freight and currency.'},
        {'id': 'c4', 'title': 'Comparative advantage — David Ricardo (and Haberler)', 'body': [
            'Ricardo showed that what matters is relative (comparative) cost, not absolute cost. Even if one country is more efficient in every good, both countries gain when each specialises in the good where its advantage is greatest (or its disadvantage is smallest) and imports the other.',
            'Test: compare opportunity costs. The country whose opportunity cost of a good is lower has the comparative advantage in it. Terms of trade must lie between the two countries\' home cost ratios for both to gain.',
            'Ricardo built the theory on the labour theory of value (labour as the only factor). Gottfried Haberler later restated it with opportunity cost — the value of the alternative given up — so the theory no longer depends on labour alone.',
            'Comparative advantage makes trade a positive-sum game: total output and living standards rise in both countries. It also applies to services such as software or financial products. A developing country without absolute advantage in anything will still have a comparative advantage in something.'],
         'analogy': 'A senior partner who types faster than her assistant still lets the assistant type — her time is worth more spent on client advice. Her comparative advantage is advice; his is typing.',
         'work': 'The same logic guides outsourcing and shared-service decisions in firms: keep in-house what you are relatively best at, buy the rest. CAs use opportunity-cost reasoning in every make-or-buy and capacity-allocation decision.'},
        {'id': 'c5', 'title': 'Heckscher-Ohlin (factor endowment / modern) theory', 'body': [
            'Swedish economists Eli Heckscher and Bertil Ohlin explained why comparative costs differ: countries are endowed with different amounts of factors (labour, capital, land).',
            'A country exports goods whose production uses its relatively abundant factor intensively and imports goods that use its relatively scarce factor intensively. Capital-rich countries export capital-intensive goods; labour-rich countries export labour-intensive goods.',
            'Factor-price equalisation theorem: free trade tends to equalise factor prices — wages and returns on capital move closer across trading countries.',
            'Compared with Ricardo: the modern theory is a two-factor (extendable) model based on money costs; it explains the cause of comparative advantage (factor endowments and factor prices); it treats international trade as a special case of inter-regional trade; and it is positive (explains the basis of trade) while the classical theory is normative (shows the gains). It cannot explain intra-industry trade — countries exporting and importing similar goods.'],
         'analogy': 'A farm with lots of land grows wheat; a crowded city with many hands stitches shirts. Each sells what its surroundings make cheap.',
         'work': 'Investors and policy makers use factor-endowment reasoning to judge which Indian sectors (labour-intensive textiles, leather, assembly) can compete globally — useful when a CA evaluates a client\'s export project.'},
        {'id': 'c6', 'title': 'New trade theory — scale, variety and network effects', 'body': [
            'New trade theory (NTT) emerged in the late 1970s and 1980s. Paul Krugman (Nobel Prize 2008) noticed that most world trade takes place between countries with similar capital-labour ratios — rich countries trading cars with each other — which Heckscher-Ohlin cannot explain.',
            'NTT adds imperfect competition and increasing returns. Economies of scale: a firm selling to home and foreign markets produces more, so its cost per unit falls. Network effects: a product becomes more valuable as more people use it (the "bandwagon effect") — messaging apps and computer operating systems.',
            'Trade still remains positive-sum; NTT adds extra gains from bigger markets, more competition, more product variety and cheaper, better intermediate and capital inputs. It explains intra-industry trade (a country exporting household refrigerators while importing industrial coolers) and the large trade between developed and big developing economies (such as BRICS) in similar products.',
            'NTT also points out that markets dominated by a few large firms with scale economies can lead to results that are not the best possible for society (sub-optimal), unlike the classical picture of a perfectly efficient world economy.'],
         'analogy': 'One messaging app wins because everyone is on it — the more users, the more useful, the cheaper per user. Size itself becomes an advantage.',
         'work': 'Valuation and equity research on platform and manufacturing companies leans heavily on scale economies and network effects — the same forces NTT uses to explain trade patterns.'},
    ]

    mcqs = [
        M('m1', 'Which feature is NOT a difference between internal trade and international trade?', ['Use of a single common currency and uniform laws in both', 'Several currencies are involved', 'Different legal systems apply', 'Factors of production are less mobile across borders'], 0, "International trade involves several currencies, different legal systems and less mobility of labour and capital across borders. A single common currency with uniform laws describes internal trade, so it is not a difference — it is the exception. 'Factors are less mobile across borders' is tempting to reject, but it is a real distinguishing feature. In practice: an Indian exporter must handle foreign-exchange conversion, FEMA rules and foreign contract law, which a domestic seller never faces.", 'c1', topic='International trade, its gains and the case against it'),
        M('m2', 'Mercantilists believed a nation becomes wealthy and powerful by:', ['Maximising exports and minimising imports to accumulate precious metals', 'Specialising according to comparative cost', 'Free trade with no state control', 'Importing more than it exports'], 0, "Mercantilists (16th–18th century Europe) believed national wealth and power came from piling up gold and silver, so they pushed for maximum exports, minimum imports and a permanent trade surplus, backed by high tariffs. 'Specialising according to comparative cost' is the trap — that is Ricardo's later free-trade idea. In practice: modern calls to treat any trade deficit as a national loss echo mercantilist thinking that economists caution against.", 'c2', topic='Mercantilism — trade as a way to pile up gold'),
        M('m3', 'Under mercantilism, trade was viewed as:', ['A zero-sum game', 'A positive-sum game', 'Irrelevant to national power', 'Beneficial only to importers'], 0, "Mercantilists saw world wealth as fixed, so one nation's gain from trade had to be another's loss — a zero-sum game. 'A positive-sum game' is the trap: that is the classical view from comparative advantage, where both partners can gain. In practice: trade negotiators who argue that every bilateral surplus is a 'win' and every deficit a 'loss' are using a zero-sum mindset that modern economics rejects.", 'c2', topic='Mercantilism — trade as a way to pile up gold'),
        M('m4', 'The theory of absolute advantage was given by:', ['Adam Smith', 'David Ricardo', 'Bertil Ohlin', 'Paul Krugman'], 0, "Adam Smith, in The Wealth of Nations (1776), argued that countries gain by specialising in goods they produce at an absolutely lower cost and trading for the rest. David Ricardo is the trap — he developed comparative advantage, which builds on and improves Smith's idea. In practice: India's large export of IT services, where it is highly efficient, is often explained using Smith-style specialisation in a simplified way.", 'c3', topic='Absolute advantage — Adam Smith'),
        M('m5', 'According to the absolute advantage theory, if one country is more efficient in both goods:', ['No trade will take place', 'Both countries will still trade', 'The efficient country imports both goods', 'Trade depends on factor endowments'], 0, "Smith's theory needs each country to be absolutely better at one good. If one country is more efficient in both, the theory predicts no trade. 'Both countries will still trade' is the tempting answer — that is true, but it comes from Ricardo's comparative advantage, which removed this limitation. In practice: rich countries still import from less efficient poorer countries, showing that comparative, not absolute, advantage drives real trade.", 'c3', topic='Absolute advantage — Adam Smith'),
        M('m6', 'Which is NOT an assumption of Adam Smith\'s absolute advantage theory?', ['Labour moves freely between countries', 'Two countries and two goods', 'No transport costs', 'Costs are measured by labour required'], 0, "Smith assumed labour moves freely within a country but cannot move between countries; trade in goods substitutes for that immobility. The other assumptions — two countries and two goods, no transport costs, and costs measured in labour — are genuine. 'No transport costs' is a tempting pick because it sounds unrealistic, but it is assumed. In practice: visa restrictions limit labour movement, which is why Indian talent is often exported indirectly through IT services.", 'c3', topic='Absolute advantage — Adam Smith'),
        M('m7', 'Comparative advantage means a country can produce a good:', ['At a lower opportunity cost than another country', 'With fewer labour hours than every other country', 'Using only its abundant factor', 'At the highest possible price'], 0, "Comparative advantage means a country can produce a good at a lower opportunity cost — giving up less of other goods — than its trading partner. 'With fewer labour hours than every other country' is the trap: that is absolute advantage. A country can have comparative advantage even if it is less efficient in everything. In practice: India exports textiles and gems partly because their opportunity cost here is lower, not because India is best at everything.", 'c4', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m8', 'Ricardo explained comparative advantage on the basis of:', ['The labour theory of value', 'Opportunity cost', 'Economies of scale', 'Factor endowments'], 0, "Ricardo built comparative cost theory on the labour theory of value — the cost of a good is measured by the labour needed to produce it. 'Opportunity cost' is the trap: Gottfried Haberler later restated the theory in opportunity-cost terms, freeing it from dependence on labour alone. In practice: introductory trade analysis still often starts with labour-hour tables like Ricardo's before moving to more realistic models.", 'c4', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m9', 'Who restated the comparative cost theory in terms of opportunity cost?', ['Gottfried Haberler', 'Eli Heckscher', 'Adam Smith', 'Paul Krugman'], 0, 'Gottfried Haberler restated comparative cost theory using opportunity cost, so it no longer depended on labour being the only factor of production. Eli Heckscher is the trap — he co-founded the factor-endowment theory with Ohlin. Adam Smith gave absolute advantage. In practice: opportunity-cost reasoning is what business consultants and economists use today when advising which products a firm or country should focus on.', 'c4', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m10', 'According to the theory of comparative advantage, trade is:', ['A positive-sum game — the net gain to the participants is positive', 'A zero-sum game', 'Beneficial only to the more efficient country', 'Beneficial only when transport cost is zero'], 0, "Under comparative advantage, each country specialises in what it produces at lower opportunity cost, world output rises, and both can consume more — a positive-sum game. 'A zero-sum game' is the trap: that was the mercantilist view. Gains do not require zero transport costs, only that costs are low enough. In practice: trade agreements, such as India's with the UAE, are justified by these mutual gains.", 'c4', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m11', 'Labour hours per unit — A: cloth 30, grain 60; B: cloth 60, grain 30. Which country should produce grain?', ['Country B', 'Country A', 'Both', 'Neither'], 0, "Grain needs 60 hours in A but only 30 in B, so B has the absolute advantage in grain — and also the comparative advantage, since grain costs B 0.5 cloth against 2 cloth in A. A makes cloth with 30 hours against B's 60. 'Country A' is the trap — A is better at cloth, not grain. In practice: this simple labour-hour comparison mirrors how analysts compare unit production costs across countries.", 'c3', topic='Absolute advantage — Adam Smith'),
        M('m12', 'Labour hours per unit — India: tables 4, mats 2; Bangladesh: tables 10, mats 1. Which statement is correct?', ['All three of the others are true', 'Bangladesh has a comparative advantage in mats', 'India has a comparative advantage in tables', 'Bangladesh has an absolute advantage in mats'], 0, "Opportunity cost of a table: India 4 ÷ 2 = 2 mats; Bangladesh 10 ÷ 1 = 10 mats, so India has the comparative advantage in tables and Bangladesh in mats. Bangladesh needs 1 hour per mat against India's 2, so it also has the absolute advantage in mats. All three statements hold; picking just one is the trap. In practice: trade economists compute such ratios using real cost data.", 'c4', 'hard', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m13', 'Labour hours per unit — X: wheat 10, rice 20; Y: wheat 20, rice 10. They specialise and trade 1 wheat for 1 rice. How many labour hours does X gain per unit of rice imported?', ['10 hours', '20 hours', '30 hours', '0 hours'], 0, 'X specialises in wheat (10 hours) and trades 1 wheat for 1 rice. Producing that rice at home would take 20 hours, so X saves 20 − 10 = 10 labour hours per unit of rice imported. The tempting 20 hours forgets that X spent 10 hours making the wheat it exported; 30 adds the two. In practice: firms make the same make-or-buy comparison when deciding whether to outsource a component.', 'c4', 'moderate', '20-10', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m14', 'Country P needs 3 hours for wheat and 6 for cloth; Q needs 9 hours for wheat and 12 for cloth. The opportunity cost of 1 unit of wheat in Q (in cloth) is:', ['0.75', '0.5', '1.33', '2'], 0, "In Q, 1 wheat takes 9 hours and 1 cloth 12 hours, so producing 1 wheat means giving up 9 ÷ 12 = 0.75 cloth. The tempting 0.5 is P's opportunity cost (3 ÷ 6); 1.33 (12 ÷ 9) and 2 (6 ÷ 3) are the costs of cloth in wheat. In practice: getting the ratio the right way up — cost of the good in terms of the other good — is the most common exam slip.", 'c4', 'moderate', '9/12', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m15', 'With the data of the previous question, mutually beneficial terms of trade (cloth per wheat) must lie between:', ['0.5 and 0.75', '0.75 and 1.33', '1.33 and 2', '0.5 and 2'], 0, "Trade benefits both only if the terms of trade lie between the two domestic opportunity costs: P's 3 ÷ 6 = 0.5 and Q's 9 ÷ 12 = 0.75 cloth per wheat. P gains by getting more than 0.5 cloth, and Q gains by paying less than 0.75. 'Between 0.5 and 2' is the trap, mixing ratios measured in different units. In practice: trade negotiators bargain over where within such a range the actual price settles.", 'c4', 'hard', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m16', 'With all its resources Country X can make 100 phones or 400 kg coffee; Y can make 60 phones or 120 kg coffee. The opportunity cost of one phone in Y is:', ['2 kg coffee', '4 kg coffee', '0.5 phone', '0.25 phone'], 0, "Y can make 60 phones or 120 kg coffee, so one phone costs 120 ÷ 60 = 2 kg coffee. The tempting 4 kg is X's opportunity cost (400 ÷ 100). 0.5 and 0.25 phone are coffee costs in phone terms. Since Y gives up less coffee per phone, Y has the comparative advantage in phones. In practice: production-possibility data like this help economists identify which sectors a country should export.", 'c4', 'moderate', '120/60', topic='Comparative advantage — David Ricardo (and Haberler)'),
        M('m17', 'The Heckscher-Ohlin theory says comparative advantage arises from differences in:', ['Factor endowments', 'Labour productivity alone', 'Consumer tastes', 'Economies of scale'], 0, "The Heckscher-Ohlin (factor-endowment or modern) theory says comparative advantage arises from differences in countries' endowments of factors such as labour, capital and land. 'Labour productivity alone' is the trap — that is the Ricardian explanation. Economies of scale belong to new trade theory. In practice: India's labour abundance helps explain its exports of labour-intensive goods such as garments and leather products.", 'c5', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
        M('m18', 'A labour-abundant country will, according to Heckscher-Ohlin, export:', ['Labour-intensive goods', 'Capital-intensive goods', 'Both kinds equally', 'Nothing — it will only import'], 0, "Under Heckscher-Ohlin, a country exports goods that use its relatively abundant, and therefore cheap, factor intensively. A labour-abundant country exports labour-intensive goods. 'Capital-intensive goods' is the trap — those would be exported by a capital-rich country. In practice: Bangladesh and Vietnam, with abundant labour, have become major garment exporters, consistent with this theory.", 'c5', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
        M('m19', 'The factor-price equalisation theorem states that free trade:', ['Tends to equalise wages and returns on capital across trading countries', 'Equalises the prices of all goods within a country', 'Makes labour fully mobile between countries', 'Raises wages only in the capital-rich country'], 0, "The factor-price equalisation theorem says free trade raises demand for each country's abundant factor and lowers demand for its scarce factor, so wages and returns to capital tend to converge across trading countries. 'Makes labour fully mobile between countries' is the trap — trade in goods substitutes for factor movement. In practice: wage pressure in rich-country manufacturing from low-cost imports is often explained with this theorem.", 'c5', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
        M('m20', 'Which is TRUE of the modern (Heckscher-Ohlin) theory compared with the classical comparative cost theory?', ['It explains the cause of comparative cost differences', 'It is based on the labour theory of value', 'It treats international trade as entirely different from domestic trade', 'It is a one-factor model'], 0, 'The modern Heckscher-Ohlin theory explains why comparative costs differ — because of differences in factor endowments. The classical theory only assumed cost differences. The other options — labour theory of value, treating trade as entirely different from domestic trade, and a one-factor model — describe the classical theory, which is the trap. In practice: economists use factor-endowment analysis to predict export patterns of developing countries.', 'c5', 'moderate', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
        M('m21', 'The classical comparative cost theory is best described as:', ['Normative — it demonstrates the gains from trade', 'Positive — it explains the basis of trade', 'A two-factor model', 'Based on money costs'], 0, "The classical comparative cost theory is normative: it demonstrates the gains from trade and argues that free trade is beneficial. The modern Heckscher-Ohlin theory is positive, explaining the basis of trade. 'Positive — explains the basis of trade' is the trap, swapping the two. It is also a one-factor model based on labour costs, not money costs. In practice: free-trade advocacy relies on the classical theory's demonstration of gains.", 'c5', 'moderate', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
        M('m22', 'Paul Krugman noticed that most world trade takes place between countries that:', ['Have similar capital-labour ratios', 'Have very different factor endowments', 'Use only labour', 'Have no economies of scale'], 0, "Paul Krugman observed that most world trade happens between countries with similar capital–labour ratios — for example, rich countries trading cars with each other. 'Very different factor endowments' is the trap: that is what Heckscher-Ohlin would predict, and the mismatch with reality led to new trade theory. In practice: India's growing two-way trade in auto components with Europe and Japan fits this pattern.", 'c6', topic='New trade theory — scale, variety and network effects'),
        M('m23', 'A country exports household refrigerators and imports industrial coolers. This is:', ['Intra-industry trade', 'Inter-industry trade explained by factor endowments', 'Dumping', 'Mercantilism'], 0, "Exporting household refrigerators while importing industrial coolers is two-way trade in similar products within one industry — intra-industry trade, explained by product variety and economies of scale. 'Inter-industry trade explained by factor endowments' is the trap — that involves exchanging different kinds of goods, like garments for machinery. In practice: India both exports and imports cars and pharmaceuticals, a common feature of intra-industry trade.", 'c6', topic='New trade theory — scale, variety and network effects'),
        M('m24', 'The value of a messaging app to each user rises as more people use it. New trade theory calls this:', ['A network effect', 'A diseconomy of scale', 'Comparative advantage', 'Factor-price equalisation'], 0, "When each user's value rises as more people use a product, it is a network effect (also called a bandwagon effect). 'A diseconomy of scale' is the trap — that is rising average cost as a firm grows, the opposite of increasing benefits. In practice: UPI and messaging apps such as WhatsApp became dominant in India because each new user made the network more valuable for everyone else.", 'c6', topic='New trade theory — scale, variety and network effects'),
        M('m25', 'Which pair of ideas is central to new trade theory?', ['Economies of scale and network effects', 'Labour theory of value and absolute cost', 'Precious metals and trade surplus', 'Factor endowment and factor-price equalisation'], 0, "New trade theory emphasises economies of scale (increasing returns) and network effects, along with imperfect competition, to explain trade between similar countries and first-mover advantages. 'Factor endowment and factor-price equalisation' is the trap — those are Heckscher-Ohlin ideas. Precious metals and surpluses belong to mercantilism. In practice: India's Production Linked Incentive schemes aim to help firms reach global scale in electronics and solar manufacturing.", 'c6', topic='New trade theory — scale, variety and network effects'),
        M('m26', 'Paul Krugman received the Nobel Prize in Economics in:', ['2008', '1998', '2001', '2015'], 0, "Paul Krugman received the Nobel Prize in Economics in 2008 for his analysis of trade patterns and the location of economic activity (economic geography). 1998 is the trap — that year's prize went to Amartya Sen for welfare economics. In practice: Krugman's work on scale and clustering helps explain why industries concentrate in hubs such as Bengaluru for IT or Tiruppur for knitwear.", 'c6', 'core', '2008', topic='New trade theory — scale, variety and network effects'),
        M('m27', 'Which is an argument AGAINST unrestricted trade?', ['Business cycles and crises spread quickly between countries', 'It weakens domestic monopolies', 'It gives consumers more variety', 'It earns foreign exchange for imports'], 0, 'Unrestricted trade links economies so closely that business cycles and financial crises spread quickly from one country to another — an argument against it. Weakening domestic monopolies, more variety for consumers and foreign-exchange earnings are traps: they are benefits of trade. In practice: the 2008 global financial crisis hit Indian exports and capital flows within months, showing how integration transmits shocks.', 'c1', topic='International trade, its gains and the case against it'),
        M('m28', 'Country P: wheat 3 hours, cloth 6 hours; Q: wheat 9 hours, cloth 12 hours. At 1 wheat = 0.6 cloth, how many hours does Q save on each unit of wheat it imports?', ['1.8 hours', '1 hour', '2.7 hours', '3 hours'], 0, "Q imports wheat at 1 wheat = 0.6 cloth. The cloth Q gives up costs 0.6 × 12 = 7.2 hours, while producing wheat at home would take 9 hours, so Q saves 9 − 7.2 = 1.8 hours per unit. The tempting 1 hour is P's saving on each unit of cloth it imports. In practice: such calculations show how gains from trade are shared depending on the agreed exchange rate.", 'c4', 'hard', '9-0.6*12', topic='Comparative advantage — David Ricardo (and Haberler)'),
    ]

    # ---------------- Written (solve and show steps) ----------------
    cq1 = Checks()
    a_tv = cq1.add('20/40', 'Arvia: opportunity cost of 1 TV in shoes')
    b_tv = cq1.add('30/45', 'Borea: opportunity cost of 1 TV in shoes')
    a_sh = cq1.add('40/20', 'Arvia: opportunity cost of 1 pair of shoes in TVs')
    b_sh = cq1.add('45/30', 'Borea: opportunity cost of 1 pair of shoes in TVs')
    q1 = Q('q1', 5, 'moderate', 'table',
           'Labour hours per unit: Arvia — TV 20, shoes (pair) 40; Borea — TV 30, shoes 45. (a) Who has the absolute advantage in each good? (b) Work out the opportunity costs and state the pattern of specialisation. (c) Give the range of terms of trade (shoes per TV) that benefits both.',
           [table(['Measure', 'Arvia', 'Borea', 'Conclusion'], [
               ['Hours per TV', '20', '30', 'Arvia (absolute)'],
               ['Hours per pair of shoes', '40', '45', 'Arvia (absolute)'],
               ['Opportunity cost of 1 TV (shoes)', f'20 ÷ 40 = {fx(a_tv)}', f'30 ÷ 45 = {fx(b_tv)}', 'Arvia lower → exports TVs'],
               ['Opportunity cost of 1 pair of shoes (TVs)', f'40 ÷ 20 = {fx(a_sh)}', f'45 ÷ 30 = {fx(b_sh)}', 'Borea lower → exports shoes'],
           ]), p(f'(c) Both gain if 1 TV exchanges for more than {fx(a_tv)} and fewer than {fx(b_tv)} pairs of shoes.')],
           [S('s1', 'Absolute advantage of Arvia in both goods', 1, 'concept'), S('s2', 'Opportunity cost of TV in both countries', 1, 'computation'),
            S('s3', 'Opportunity cost of shoes in both countries', 1, 'computation'), S('s4', 'Correct specialisation: Arvia TVs, Borea shoes', 1, 'conclusion'), S('s5', 'Terms-of-trade range between home ratios', 1, 'computation')],
           ['Many candidates stop after noting Arvia is better at both goods and wrongly conclude there is no trade.', 'Full marks need both opportunity-cost ratios for both goods.'],
           ['Dividing the wrong way (shoes ÷ TV) and reversing the pattern.', 'Giving a terms-of-trade range outside the two home ratios.'],
           ['Lay out a four-column table: measure, country 1, country 2, conclusion.', 'Always state which country exports which good in one clear line.'], checks=cq1)

    cq2 = Checks()
    m_hours = cq2.add('6+12', 'Meridia hours for one unit of each')
    n_hours = cq2.add('15+10', 'Nortia hours for one unit of each')
    m_cof = cq2.add('18/6', 'Meridia all hours on coffee')
    n_tea = cq2.add('25/10', 'Nortia all hours on tea')
    q2 = Q('q2', 4, 'core', 'table',
           'Meridia needs 6 hours for a unit of coffee and 12 for a unit of tea; Nortia needs 15 hours for coffee and 10 for tea. Before trade each makes one unit of each good. Show the absolute advantages and the gain in world output if each country specialises fully.',
           [table(['Step', 'Working', 'Result'], [
               ['Absolute advantage', 'Coffee: 6 < 15; Tea: 10 < 12', 'Meridia — coffee; Nortia — tea'],
               ['Hours available', f'Meridia 6 + 12 = {m_hours}; Nortia 15 + 10 = {n_hours}', '—'],
               ['After specialisation', f'Meridia {m_hours} ÷ 6; Nortia {n_hours} ÷ 10', f'{fx(m_cof)} coffee; {fx(n_tea)} tea'],
               ['World gain', f'Coffee {fx(m_cof)} − 2; tea {fx(n_tea)} − 2', f'+{fx(m_cof-2)} coffee, +{fx(n_tea-2)} tea'],
           ])],
           [S('s1', 'Identifies absolute advantage in each good', 1, 'concept'), S('s2', 'Total hours available in each country', 1, 'computation'),
            S('s3', 'Output after specialisation', 1, 'computation'), S('s4', 'Gain in world output stated', 1, 'conclusion')],
           ['Good answers keep the total labour fixed and only re-allocate it.'], ['Adding extra labour after specialisation.', 'Comparing outputs instead of hours to find the advantage.'],
           ['Show the hours available first; the rest is division.'], checks=cq2)

    q3 = Q('q3', 4, 'core', 'table', 'Distinguish between the classical comparative cost theory and the modern (Heckscher-Ohlin) theory of trade on any four points.',
           [table(['Basis', 'Comparative cost theory (Ricardo)', 'Modern theory (Heckscher-Ohlin)'], [
               ['Value / cost basis', 'Labour theory of value', 'Money costs — more realistic'],
               ['Factors', 'One factor (labour)', 'Two factors (labour, capital), extendable'],
               ['Cause of comparative advantage', 'Differences in labour productivity; cause not explained', 'Differences in factor endowments and factor prices'],
               ['Nature', 'Normative — shows gains from trade', 'Positive — explains the basis of trade'],
               ['Domestic vs foreign trade', 'International trade treated as distinct', 'A special case of inter-regional trade'],
           ])],
           [S('s1', 'Labour value vs money cost', 1, 'concept'), S('s2', 'One factor vs two factors', 1, 'concept'), S('s3', 'Cause of comparative advantage', 1, 'analysis'), S('s4', 'Normative vs positive (or inter-regional point)', 1, 'concept')],
           ['A clean table with four valid bases scores full marks.'], ['Writing that Heckscher-Ohlin explains intra-industry trade — it does not.'], ['One line per cell; put the basis in the first column.'])

    jobs = [
        {'id': 'j1', 'title': 'Make in India or import? An opportunity-cost view', 'role': 'CA in industry (plant controller of an electronics assembler)',
         'situation': 'Your plant can make either control boards or wiring harnesses on the same line. Management wants to make both because "we are better than the overseas supplier at both".',
         'steps': ['Measure line-hours per unit for each product and compare with landed import prices.', 'Work out the opportunity cost: how many harnesses are given up for each board made.', 'Allocate scarce line-hours to the product with the larger relative advantage; import the other if the landed price is below your opportunity cost.', 'Present the profit difference to management with a sensitivity for duty and exchange rate.'],
         'takeaway': 'Being better at everything does not mean you should make everything — scarce capacity should go where the relative advantage is largest.',
         'think': 'Line-hours: board 2, harness 1. A harness can be imported for a price equal to the contribution from 0.4 board. Should you import harnesses?',
         'answer': 'Making one harness costs 1 line-hour = 0.5 board forgone. Buying it costs only 0.4 board, which is less than the 0.5 board given up, so importing harnesses and using the line for boards is better.'},
        {'id': 'j2', 'title': 'Reading a sector\'s export potential', 'role': 'Research analyst at a broking firm',
         'situation': 'You are asked whether an Indian footwear company can keep growing exports to Europe.',
         'steps': ['Check factor intensity: footwear is labour-intensive — India\'s abundant factor (Heckscher-Ohlin).', 'Check scale: large plants lower unit cost (new trade theory).', 'Check the case against trade: dependence on one market, sudden standards or tariff changes.', 'Conclude with risks and a view on margins.'],
         'takeaway': 'Trade theories give a quick, structured first view of whether a sector\'s export story is sustainable.'},
    ]

    viva = [
        V('v1', 'State the theory of comparative advantage.',
          'David Ricardo said that a country should specialise in and export the good in which it has a comparative advantage, that is a lower opportunity cost or a smaller relative disadvantage, and import the other good. Even if one country has an absolute advantage in both goods, both countries still gain from trade.',
          [P('p1', 'Given by David Ricardo', 2, 'ricardo'),
           P('p2', 'Specialise in / export the good with lower opportunity cost (greater relative advantage, smaller disadvantage)', 4,
             'specialis|export|produc|concentrat', 'lower opportunity cost|lowest opportunity cost|less opportunity cost|comparative advantage|relative advantage|smaller disadvantage|smaller relative disadvantage|least disadvantage|lower relative cost|comparative cost|greatest advantage|relative cost', min=2),
           P('p3', 'Trade benefits both even if one country is better at both goods (absolute advantage in both)', 4,
             ALT('{a} both', 'better both', 'more efficient both', 'efficient everything', 'better everything', 'superior both', 'both good', a=('absolute advantage', 'absolutely better', 'advantage')),
             'both gain|both benefit|benefit both|benefits both|gains both|benefit to both|both countries gain|both countries benefit|still gain|still benefit|mutual|both better off|gain from trade|benefit from trade|both countries better|both profit')], 'c4'),
        V('v2', 'What did Adam Smith say about the basis of international trade?',
          'Adam Smith said trade is based on absolute advantage. A country should specialise in the good it can produce with less labour than the other country and exchange it for the good the other country makes more cheaply, so both gain. If one country is not better at any good, his theory predicts no trade.',
          [P('p1', 'Basis is absolute cost advantage', 4, 'absolute advantage|absolute cost|absolutely lower|absolutely cheaper|absolute'),
           P('p2', 'Specialise in the good made with less labour / fewer resources and exchange it', 4, 'specialis|export|produc|exchang', 'less labour|fewer labour|less resource|fewer resource|lower cost|cheaper|fewer hours|less hours|less input|more efficient|more output', min=2),
           P('p3', 'No trade if a country has no absolute advantage in anything', 2, 'no trade|not trade|trade will not|no exchange|no gain|trade not happen|won t trade|would not trade|not happen')], 'c3'),
        V('v3', 'Explain the Heckscher-Ohlin theory of trade.',
          'The Heckscher-Ohlin theory, also called the factor endowment theory, says comparative advantage comes from differences in factor endowments. A country exports goods that use its relatively abundant factor intensively and imports goods that use its scarce factor intensively. So a capital-rich country exports capital-intensive goods and a labour-rich country exports labour-intensive goods, and trade tends to equalise factor prices.',
          [P('p1', 'Comparative advantage is due to differences in factor endowments', 4, 'factor endowment|endowment|factor abundance|resource endowment|factor supply|endowed'),
           P('p2', 'Export goods using the abundant factor intensively; import those using the scarce factor', 4,
             'export|sell abroad|specialis', 'abundant|plentiful|plenty|cheap factor|lot of|rich in|capital rich|labour rich|labour abundant|capital abundant|abundance', min=2),
           P('p3', 'Trade tends to equalise factor prices (wages, returns to capital)', 2, 'factor price equal|equalis factor price|factor price converg|wages equal|wages converg|factor price come closer|factor prices become equal|equalise wage|factor price')], 'c5'),
        V('v4', 'What was the mercantilist view of international trade?',
          'Mercantilists, who dominated Europe from the sixteenth to the eighteenth century, believed national wealth meant holding gold and silver. So a country should maximise exports and minimise imports, using high tariffs and state control, to keep a trade surplus. They saw trade as a zero-sum game.',
          [P('p1', 'Wealth = stock of gold and silver / precious metals', 3, 'gold|silver|precious metal|bullion|treasure'),
           P('p2', 'Maximise exports, minimise imports (trade surplus)', 4, ALT('{m} export', 'export more', 'more export', 'encourag export', 'promot export', 'boost export', 'export encourag', 'exports should be encouraged', m=('maximis', 'increas', 'raise', 'more')),
             ALT('{n} import', 'import less', 'fewer import', 'discourag import', 'restrict import', 'curb import', 'cut import', 'reduc import', 'limit import', 'import restrict', 'import discourag', 'import curb', 'import limit', n=('minimis', 'decreas', 'less', 'low'))),
           P('p3', 'High tariffs / state control; trade seen as zero-sum', 3, 'tariff|state control|government control|zero sum|one nation gain|protection|duty|duties', min=1)], 'c2'),
        V('v5', 'How does the new trade theory explain trade between similar countries?',
          'New trade theory, linked with Paul Krugman, says much trade is between countries with similar factor endowments. It is driven by economies of scale, where cost per unit falls as a firm sells in more markets, and by network effects, where a product becomes more valuable as more people use it. This explains intra-industry trade in similar products.',
          [P('p1', 'Linked with Paul Krugman', 2, 'krugman'),
           P('p2', 'Economies of scale — unit cost falls with larger output / bigger market', 3, 'economies of scale|scale economies|large scale|increasing return|cost per unit fall|unit cost fall|cost per unit go down|average cost fall|scale'),
           P('p3', 'Network effects — value rises as more people use the product', 3, 'network effect|bandwagon|network|more people use|more user|more users'),
           P('p4', 'Explains intra-industry trade / trade in similar products between similar countries', 2, 'intra industry|intra-industry|similar product|similar good|same product|same kind|similar countries|two way trade|same industry')], 'c6'),
    ]

    # ---------------- Case study ----------------
    cc = Checks()
    t_s = cc.add('8/4', 'Sundar: opportunity cost of 1 tonne steel in garment lots')
    t_v = cc.add('12/3', 'Vellora: opportunity cost of 1 tonne steel in garment lots')
    case = {'id': 'k1', 'title': 'Sundar and Vellora negotiate a trade deal', 'difficulty': 'hard',
            'case': ('Two countries are planning a bilateral deal. In Sundar a worker-day produces 4 tonnes of steel or 8 lots of garments. In Vellora a worker-day produces 3 tonnes of steel or 12 lots of garments. '
                     'Sundar has relatively more capital per worker; Vellora has relatively more labour. A minister in Sundar argues that "we should only export and never import, so that our reserves keep rising".'),
            'mcqs': [
                M('k1a', 'What is the opportunity cost of one tonne of steel in Vellora (in lots of garments)?', ['4', '2', '0.25', '0.5'], 0, "In Vellora, one worker-day produces 3 tonnes of steel or 12 lots of garments, so one tonne of steel costs 12 ÷ 3 = 4 lots of garments. The tempting 2 is Sundar's opportunity cost (8 ÷ 4); 0.25 is the cost of a garment lot in tonnes of steel in Vellora. In practice: trade negotiators begin with such opportunity costs to decide which sectors each country should concentrate on.", 'c4', 'moderate', '12/3', topic='Comparative advantage — David Ricardo (and Haberler)'),
                M('k1b', 'Which pattern of specialisation benefits both countries?', ['Sundar exports steel; Vellora exports garments', 'Sundar exports garments; Vellora exports steel', 'Sundar exports both', 'No trade — Sundar is better at steel only'], 0, "Steel costs 2 lots of garments in Sundar but 4 in Vellora, so Sundar has the comparative advantage in steel. A garment lot costs 0.25 tonne of steel in Vellora and 0.5 tonne in Sundar, so Vellora has it in garments. 'No trade — Sundar is better at steel only' is the trap, applying absolute advantage. In practice: such specialisation is the economic basis of bilateral trade deals.", 'c4', 'hard', topic='Comparative advantage — David Ricardo (and Haberler)'),
                M('k1c', 'The factor data (Sundar capital-rich, Vellora labour-rich) supports this pattern under which theory?', ['Heckscher-Ohlin', 'Mercantilism', 'Absolute advantage only', 'Network effects'], 0, "Capital-rich Sundar exports capital-intensive steel, and labour-rich Vellora exports labour-intensive garments — exactly the Heckscher-Ohlin prediction that countries export goods using their abundant factor intensively. 'Absolute advantage only' is the trap, since the question links trade to factor endowments, not just efficiency. In practice: India's exports of labour-intensive garments and imports of capital goods fit this pattern.", 'c5', 'moderate', topic='Heckscher-Ohlin (factor endowment / modern) theory'),
                M('k1d', 'The minister\'s view reflects which school of thought?', ['Mercantilism', 'New trade theory', 'Comparative advantage', 'Factor-price equalisation'], 0, "The minister wants to export only and never import so that reserves keep rising — the mercantilist goal of accumulating precious metals or reserves through a permanent surplus. 'Comparative advantage' is the trap: that theory says imports are as beneficial as exports. In practice: excessive reserve hoarding has an opportunity cost, since those resources could have bought imports that raise living standards or investment.", 'c2', 'core', topic='Mercantilism — trade as a way to pile up gold'),
                M('k1e', 'Which terms of trade (lots of garments per tonne of steel) would benefit both countries?', ['3', '1.5', '5', '2'], 0, "Both countries gain only if the terms of trade lie strictly between their opportunity costs of steel: Sundar's 2 and Vellora's 4 lots of garments per tonne. Only 3 lies inside that range. At exactly 2 Sundar gains nothing; 1.5 hurts Sundar; 5 hurts Vellora. In practice: in real negotiations, the final terms within this range depend on bargaining power and demand in each country.", 'c4', 'hard', '3', topic='Comparative advantage — David Ricardo (and Haberler)'),
            ]}

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch09', 'n': 1, 'title': 'Theories of International Trade',
        'outcomes': ['Explain what international trade is, how it differs from internal trade, and weigh the arguments for and against freer trade.',
                     'Describe the mercantilist view and Adam Smith\'s absolute advantage theory with its assumptions.',
                     'Apply Ricardo\'s comparative advantage (and Haberler\'s opportunity-cost version) to numerical data, including the terms-of-trade range and gains in labour hours.',
                     'Explain the Heckscher-Ohlin theory, factor-price equalisation and the new trade theory (economies of scale, network effects, intra-industry trade).'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 50}, 'prereq': [],
                 'exam_tip': 'Expect 2–4 MCQs: one or two numericals on absolute/comparative advantage (compute opportunity costs both ways) and theory-matching questions (who said what). Watch the "NOT" in the stem.'},
        'concepts': concepts, 'illustrations': [ill1, ill2, ill3, ill4], 'jobs': jobs, 'mcqs': mcqs, 'questions': [q1, q2, q3],
        'revision': {'summary': ['International trade = exchange across borders; more complex than internal trade (currencies, laws, factor immobility).',
                                 'Gains: specialisation, efficiency, competition, variety, foreign exchange, innovation. Risks: unequal gains, exploitation, resource depletion, contagion, dependence, policy risk.',
                                 'Mercantilism: maximise exports, minimise imports, accumulate gold; zero-sum view.',
                                 'Smith: absolute advantage; no trade if a country is not absolutely better at anything.',
                                 'Ricardo: comparative advantage (labour theory of value); Haberler: opportunity cost. Terms of trade lie between home cost ratios.',
                                 'Heckscher-Ohlin: factor endowments; export goods using the abundant factor; factor-price equalisation.',
                                 'New trade theory (Krugman, Nobel 2008): economies of scale, network effects, intra-industry trade between similar countries.'],
                     'remember': ['Opportunity cost of A = hours for A ÷ hours for B (or output of B ÷ output of A).', 'Lower opportunity cost = comparative advantage.', 'Classical = normative, labour-based, one factor; modern = positive, money cost, two factors.'],
                     'traps': ['A country better at both goods still gains from trade (Ricardo) — Smith\'s theory would say no trade.', 'Do not confuse "fewer hours" (absolute) with "lower opportunity cost" (comparative).', 'Heckscher-Ohlin cannot explain intra-industry trade; NTT can.']},
        'quickref': [{'k': 'Opportunity cost (hours data)', 'v': 'OC of good X = labour hours for X ÷ labour hours for Y'},
                     {'k': 'Opportunity cost (output data)', 'v': 'OC of X = max output of Y ÷ max output of X'},
                     {'k': 'Terms-of-trade range', 'v': 'Between the two countries\' home cost ratios'},
                     {'k': 'Gain in hours', 'v': 'Home hours for the import − hours spent making the export given for it'},
                     {'k': 'Mercantilism', 'v': '16th–18th c. Europe; export surplus; precious metals; zero-sum'},
                     {'k': 'Smith / Ricardo / Haberler', 'v': 'Absolute cost / comparative cost (labour) / opportunity cost'},
                     {'k': 'Heckscher-Ohlin', 'v': 'Factor endowments; factor-price equalisation'},
                     {'k': 'New trade theory', 'v': 'Krugman (Nobel 2008); economies of scale; network (bandwagon) effects'}],
        'viva': viva, 'cases': [case],
    }
