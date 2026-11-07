"""CA Foundation · Paper 4 Business Economics · Chapter 2 · Unit 2 Theory of Consumer Behaviour.
Original explanations, examples and questions (ICAI structure and scope only). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch02-u02'


def Q(mid, q, opts, ans, ex, c, d='core', check=None, topic=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if topic: x['topic'] = topic
    if check: x['check'] = check
    return x


def build():
    # ---------- i1 TU and MU ----------
    c1 = Checks()
    tu = [0, 12, 22, 30, 35, 37, 37, 34]
    mu = [None] + [c1.add(f'{tu[i]}-{tu[i-1]}', f'MU of unit {i}') for i in range(1, len(tu))]
    tu_rows = [[i, tu[i], '—' if i == 0 else mu[i]] for i in range(len(tu))]

    # ---------- i2 consumer surplus from a schedule ----------
    c2 = Checks()
    worth = [45, 38, 32, 27, 23, 20, 16]; price = 20
    bought = [w for w in worth if w >= price]
    cs_each = [c2.add(f'{w}-{price}', f'surplus on unit {i+1}') for i, w in enumerate(bought)]
    tot_worth = c2.add('+'.join(map(str, bought)), 'total utility (worth) of units bought')
    paid = c2.add(f'{len(bought)}*{price}', 'amount actually paid')
    cs_tot = c2.add(f'{tot_worth}-{paid}', 'total consumer surplus')

    # ---------- i3 consumer surplus from a linear demand curve ----------
    c3 = Checks()
    q_at40 = c3.add('(100-40)/2', 'Q at P = 40 for P = 100 − 2Q')
    cs40 = c3.add('0.5*30*(100-40)', 'consumer surplus at P = 40')
    q_at30 = c3.add('(100-30)/2', 'Q at P = 30')
    cs30 = c3.add('0.5*35*(100-30)', 'consumer surplus at P = 30')
    cs_gain = c3.add('1225-900', 'gain in consumer surplus from the price fall')

    # ---------- i4 MRS ----------
    c4 = Checks()
    combos = [('A', 1, 20), ('B', 2, 14), ('C', 3, 10), ('D', 4, 7), ('E', 5, 5)]
    mrs = [None] + [c4.add(f'{combos[i-1][2]}-{combos[i][2]}', f'MRS between {combos[i-1][0]} and {combos[i][0]} (Y given up per extra X)') for i in range(1, len(combos))]

    # ---------- i5 budget line and equilibrium ----------
    c5 = Checks()
    M, Px, Py = 1200, 40, 30
    x_max = c5.add('1200/40', 'max X'); y_max = c5.add('1200/30', 'max Y')
    slope = c5.add('round(40/30,2)', 'price ratio Px/Py')
    # equilibrium bundle on budget line where MRS = 4/3: choose X=15, Y=20  (40*15 + 30*20 = 1200)
    spend = c5.add('40*15+30*20', 'spending on bundle X = 15, Y = 20')
    x_new = c5.add('1200/30', 'max X when Px falls to ₹30')

    # ---------- questions ----------
    cq1 = Checks()
    q1_mu = [cq1.add(f'{a}-{b}', 'q1 MU') for a, b in [(20, 0), (36, 20), (48, 36), (54, 48), (54, 54), (50, 54)]]
    cq2 = Checks()
    q2_q = cq2.add('(150-50)/5', 'q2 Q at P = 50 for P = 150 − 5Q')
    q2_cs = cq2.add('0.5*20*(150-50)', 'q2 consumer surplus')
    q2_paid = cq2.add('50*20', 'q2 amount paid')
    q2_tu = cq2.add('1000+1000', 'q2 total willingness to pay (area under demand curve)')
    cq3 = Checks()
    q3_x = cq3.add('2400/60', 'q3 max X'); q3_y = cq3.add('2400/40', 'q3 max Y'); q3_r = cq3.add('60/40', 'q3 Px/Py')
    q3_chk = cq3.add('60*24+40*30', 'q3 cost of bundle (24, 30)')

    # ---------- case ----------
    k = Checks()
    k_worth = [120, 100, 85, 70, 60, 50]
    k_p = 60
    k_n = k.add('5', 'number of shows watched (worth ≥ price)')
    k_cs = k.add('(120-60)+(100-60)+(85-60)+(70-60)+(60-60)', 'case consumer surplus')
    k_cs2 = k.add('(120-50)+(100-50)+(85-50)+(70-50)+(60-50)+(50-50)', 'case CS at ₹50')
    k_x = k.add('3000/300', 'case max movies'); k_y = k.add('3000/150', 'case max snacks')

    concepts = [
        {'id': 'c1', 'title': 'Nature of human wants',
         'body': ['A want is a desire to own or use goods and services that give satisfaction. Wants arise from physical needs, psychological drives and social pressures. Because resources are limited, we choose between urgent and less urgent wants.',
                  'Characteristics: wants are unlimited in number, though each single want can be satisfied (satiable); they differ in intensity; they compete with one another for limited means; some are complementary (a car also needs fuel); a want can be met in alternative ways; wants are subjective and relative, varying with time, place and person; some recur, others do not; wants can turn into habits and customs; and they are shaped by income, taste, fashion, advertising and social norms.',
                  'Utility is the want-satisfying power of a commodity. It is a psychological, subjective idea: it is not the same as usefulness and carries no moral judgement — a cigarette has utility to a smoker. Total utility (TU) is the sum of the marginal utilities of all units consumed (TU = ΣMU). Marginal utility (MU) is the extra utility from one more unit: MU = TUn − TUn−1 = ΔTU/ΔN.'],
         'analogy': 'Wants are like a queue at a ticket counter that never ends; utility is how happy each person is when served.',
         'work': 'Consumer research for product launches, which CAs in strategy and FP&A roles rely on, starts from what want the product satisfies and how intense it is.'},
        {'id': 'c2', 'title': 'Classification of wants: necessaries, comforts, luxuries',
         'body': ['Necessaries are essential for living, in three kinds: necessaries for life (existence) — the minimum food, clothing and shelter needed to stay alive; necessaries for efficiency — nourishing food, adequate clothing, clean water, a decent home, education and recreation that keep a person energetic and productive; conventional necessaries — things we feel compelled to have because of habit or social custom (gifts at festivals, a particular dress at weddings), though they are needed neither for existence nor for efficiency.',
                  'Comforts make life comfortable and satisfying — tasty food, a good house, clothes for different occasions, labour-saving appliances. They are less urgent than necessaries. Luxuries are superfluous and expensive — designer clothing, vintage cars, lavish furniture, items of vanity.',
                  'The classification is not rigid: what is a luxury for one person or era may be a comfort or necessity for another. Mobile phones and refrigerators moved from luxury to necessity within a generation.'],
         'analogy': 'Necessaries are the foundation of a house, comforts are the furniture, luxuries are the chandelier.',
         'work': 'GST rate slabs broadly follow this logic — essentials at nil or low rates, luxury and "sin" goods at the highest rate plus cess — which CAs apply when classifying goods for clients.'},
        {'id': 'c3', 'title': 'Relationship between TU and MU',
         'body': ['TU = ΣMU and MU = TUn − TUn−1. At the first unit, TU = MU.',
                  'While TU rises at a diminishing rate, MU falls but stays positive. When TU is at its maximum (and constant), MU = 0 — the point of satiety. When TU starts to fall, MU becomes negative (disutility).',
                  'On a graph, the TU curve rises, flattens at its peak and then falls; the MU curve slopes downward, cuts the X-axis exactly where TU is maximum and goes below it afterwards.'],
         'analogy': 'TU is the height of a hill you are climbing; MU is how steep the next step is. At the summit the next step is flat (MU = 0); beyond it you go downhill (negative MU).',
         'work': 'The same marginal-vs-total logic is used throughout CA work: marginal cost and total cost, marginal revenue and total revenue, incremental return on extra investment.'},
        {'id': 'c4', 'title': 'Law of diminishing marginal utility',
         'body': ['Other things remaining the same, as a consumer takes more and more units of a commodity, the extra satisfaction from each successive unit eventually falls. This is the law of diminishing marginal utility, the basis of Marshall\'s cardinal utility analysis (utility measured in numbers called utils, or in money the consumer is willing to pay).',
                  'Reason: each particular want is satiable — as it gets satisfied, the urge for more weakens. Also, goods are imperfect substitutes for each other, so one good cannot satisfy every want.',
                  'Assumptions / limitations: (1) units consumed must be identical in size, quality and taste, and the consumer\'s habits and tastes must not change; (2) units must be of a standard, reasonable size — giving a very thirsty person water by the spoon may first show increasing MU; (3) consumption must be continuous, with no long time gap; (4) the law may not hold for money, gold or collections, where more may increase the desire (the miser, the stamp collector); (5) the MU of a good can be affected by the presence or absence of related goods (substitutes and complements).'],
         'analogy': 'The first glass of cold water on a hot day is heaven; the fifth is a chore.',
         'work': 'Bundle pricing and "second unit at half price" offers exist because the consumer values the second unit less — firms price to the falling marginal utility.'},
        {'id': 'c5', 'title': 'Consumer surplus (Marshall)',
         'body': ['Consumer surplus is the excess of what a consumer is willing to pay for a good over what he actually pays. Consumer surplus = total amount one is willing to pay − amount actually paid (= TU in money terms − price × quantity).',
                  'It rests on diminishing marginal utility. The consumer buys units until MU (in money) equals price. Every earlier unit is worth more than the price paid, so it yields a surplus; the marginal (last) unit yields none.',
                  'On a graph, consumer surplus is the area below the demand (MU) curve and above the price line, up to the quantity bought — a triangle for a straight-line demand curve. A rise in price shrinks consumer surplus; a fall in price enlarges it. Total market consumer surplus is the sum of individual surpluses.',
                  'Applications: helps firms in pricing (price discrimination tries to capture consumer surplus); helps government judge the welfare effect of taxes and subsidies and decide which projects (bridges, roads) to build; explains "value-for-money" comparisons between countries; and is used in cost–benefit analysis.',
                  'Limitations: utility cannot be measured precisely in cardinal numbers; the MU of money is assumed constant, which is unrealistic; it is hard to measure for necessities (willingness to pay may be almost infinite) and for prestige goods; and it ignores the effect of substitutes and complements on willingness to pay.'],
         'analogy': 'If you were ready to pay ₹500 for a concert ticket and got it for ₹300, the ₹200 "you saved in your mind" is your consumer surplus.',
         'work': 'Dynamic pricing in airlines and cab aggregators is designed to capture part of consumer surplus — CAs reviewing revenue management policies see this concept in action.'},
        {'id': 'c6', 'title': 'Indifference curve approach: assumptions and the curve',
         'body': ['The indifference curve (IC) approach, developed by Hicks and Allen, replaces the cardinal measurement of utility with an ordinal ranking: the consumer only needs to say whether he prefers one bundle to another or is indifferent between them.',
                  'Assumptions: the consumer is rational and seeks maximum satisfaction; utility is ordinal (ranked, not measured); preferences are consistent and transitive (if A is preferred to B and B to C, then A is preferred to C); more of a good is preferred to less (non-satiety); and there is a diminishing marginal rate of substitution.',
                  'An indifference schedule lists combinations of two goods that give the same satisfaction. Plotting it gives an indifference curve — the locus of all combinations among which the consumer is indifferent. A set of ICs is an indifference map; a higher (further right) curve shows a higher level of satisfaction.',
                  'MRSxy — the marginal rate at which X is substituted for Y — is the amount of Y the consumer is willing to give up for one more unit of X while staying on the same IC; it is the (absolute) slope of the IC: MRSxy = −ΔY/ΔX. As the consumer gets more X and less Y, he is willing to give up less and less Y for each extra X — diminishing MRS.'],
         'analogy': 'An indifference curve is a contour line on a map of happiness: every point on it is the same "height" of satisfaction.',
         'work': 'Product-mix and bundle design (data vs talk-time in mobile plans, speed vs price in courier services) uses trade-off thinking identical to MRS.'},
        {'id': 'c7', 'title': 'Properties of indifference curves',
         'body': ['(1) They slope downward from left to right — to keep satisfaction constant, more of X must mean less of Y. (2) They are convex to the origin — because MRSxy diminishes. (3) Two ICs never intersect — if they did, the point of intersection would give two different levels of satisfaction at once, which contradicts transitivity and "more is better". (4) A higher IC represents a higher level of satisfaction. (5) An IC does not touch either axis — the consumer is assumed to want some of both goods (an IC touching an axis would mean wanting only one good).',
                  'Special cases: perfect substitutes give straight-line ICs (constant MRS); perfect complements (left shoe and right shoe) give L-shaped ICs.'],
         'analogy': 'Contour lines of different heights on a map never cross — two heights at one point is impossible. ICs follow the same rule.',
         'work': 'In valuation and pricing studies, consistency checks (no "crossing" preferences) are applied to survey data before relying on it — the same logic as non-intersecting ICs.'},
        {'id': 'c8', 'title': 'Budget line and consumer equilibrium',
         'body': ['The budget line (price line) shows all combinations of two goods the consumer can buy by spending his whole income at given prices: Px·X + Py·Y = M. It meets the X-axis at M/Px and the Y-axis at M/Py, and its slope (absolute) is Px/Py. Points inside are affordable but leave money unspent; points outside are unaffordable.',
                  'Changes: a rise in income shifts the line outward parallel (a fall, inward); a change in the price of one good rotates (swivels) the line around the intercept of the other good — a fall in Px moves the X-intercept outward.',
                  'Consumer equilibrium: assumptions — a given indifference map, a fixed money income spent wholly on X and Y, given prices, homogeneous and divisible goods, and rational behaviour. The consumer reaches the highest IC his budget allows, which happens where the budget line is tangent to an IC. At that point the slope of the IC equals the slope of the budget line: MRSxy = Px/Py. The second condition is that the IC is convex to the origin at that point (MRS diminishing).'],
         'analogy': 'The budget line is a fence; the ICs are hills of happiness. You climb to the highest hill you can touch from inside the fence — where the fence just kisses a hill.',
         'work': 'Personal financial planning by CAs is a budget-line exercise: the client\'s income fixes the frontier, and advice aims at the best mix of spending and saving within it.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'TU and MU schedule', 'difficulty': 'core', 'minutes': 5,
         'q': 'Rahul\'s total utility from glasses of juice is given. Compute marginal utility and identify (a) the point of satiety, (b) where disutility begins, (c) the stage where TU rises at a diminishing rate.',
         'given': [table(['Glasses', 'TU (utils)'], [[i, tu[i]] for i in range(len(tu))])],
         'solution': [table(['Glasses', 'TU (utils)', 'MU = TUn − TUn−1'], tu_rows, title='TU and MU'),
                      p(f'(a) TU is maximum ({max(tu)} utils) at the 5th and 6th glasses; MU of the 6th glass is {mu[6]} — the point of satiety. (b) The 7th glass has MU = {mu[7]}: disutility. (c) From the 1st to the 5th glass TU rises while MU falls from {mu[1]} to {mu[5]} — rising at a diminishing rate.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Consumer surplus from a schedule', 'difficulty': 'core', 'minutes': 6,
         'q': f'Meena is willing to pay ₹45, 38, 32, 27, 23, 20 and 16 for the 1st to 7th unit of a snack. The market price is ₹{price}. How many units does she buy, and what is her consumer surplus?',
         'solution': [table(['Unit', 'Willing to pay (₹)', 'Price (₹)', 'Surplus (₹)'], [[i + 1, w, price, s_] for i, (w, s_) in enumerate(zip(bought, cs_each))] + [['Total', tot_worth, paid, cs_tot]], num=[1, 2, 3], total=True, title='Consumer surplus'),
                      p(f'She buys {len(bought)} units — up to the unit whose worth equals the price (₹20). The 7th unit (worth ₹16) is not bought. Consumer surplus = {R(tot_worth)} − {R(paid)} = {R(cs_tot)}. The last unit bought gives zero surplus.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Consumer surplus from a demand curve, and the effect of a price fall', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'The market demand curve is P = 100 − 2Q. Find consumer surplus at a price of ₹40 and at ₹30, and the gain from the price fall.',
         'solution': [p(f'At P = 40: Q = (100 − 40) ÷ 2 = {q_at40}. Consumer surplus = ½ × base × height = ½ × {q_at40} × (100 − 40) = {R(cs40)}.'),
                      p(f'At P = 30: Q = (100 − 30) ÷ 2 = {q_at30}. Consumer surplus = ½ × {q_at30} × 70 = {R(cs30)}.'),
                      p(f'Gain = {R(cs30)} − {R(cs40)} = {R(cs_gain)}. A lower price enlarges the triangle below the demand curve and above the price line.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Diminishing marginal rate of substitution', 'difficulty': 'core', 'minutes': 5,
         'q': 'Combinations of apples (X) and bananas (Y) on one indifference curve are given. Compute MRSxy and comment.',
         'given': [table(['Combination', 'Apples (X)', 'Bananas (Y)'], [[c_[0], c_[1], c_[2]] for c_ in combos])],
         'solution': [table(['Combination', 'X', 'Y', 'MRSxy (Y given up for 1 more X)'], [[c_[0], c_[1], c_[2], '—' if i == 0 else mrs[i]] for i, c_ in enumerate(combos)], title='MRS'),
                      p(f'MRS falls from {mrs[1]} to {mrs[-1]}: as Neha has more apples and fewer bananas, she gives up fewer bananas for each extra apple. This diminishing MRS makes the IC convex to the origin.')],
         'checks': c4},
        {'id': 'i5', 'title': 'Budget line and consumer equilibrium', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'A consumer has ₹{inr(M)} to spend on X (₹{Px} each) and Y (₹{Py} each). (a) Write the budget equation and find the intercepts and slope. (b) At the bundle X = 15, Y = 20 her IC is tangent to the budget line. Verify it is affordable and state the equilibrium condition. (c) What happens if Px falls to ₹30?',
         'solution': [p(f'(a) 40X + 30Y = 1,200. X-intercept = 1,200 ÷ 40 = {x_max}; Y-intercept = 1,200 ÷ 30 = {y_max}. Slope (absolute) = Px/Py = 40/30 ≈ {slope}.'),
                      p(f'(b) Cost of (15, 20) = 40 × 15 + 30 × 20 = {R(spend)} — exactly the income, so it lies on the budget line. Since the IC is tangent there, MRSxy = Px/Py ≈ {slope}: she gives up about 1.33 Y for one more X, the same rate as the market. This is the equilibrium (highest attainable IC).'),
                      p(f'(c) The line swivels outward around the Y-intercept ({y_max}); the new X-intercept is 1,200 ÷ 30 = {x_new}. She can reach a higher IC.')],
         'checks': c5},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Designing a "buy 2, get the 3rd at half price" offer', 'role': 'CA in industry — commercial finance at an FMCG company',
         'situation': 'Marketing proposes a multi-buy offer on a beverage. You are asked whether it makes economic sense.',
         'steps': ['Recognise diminishing marginal utility: the 3rd bottle is worth less to the buyer than the 1st, so full price would not sell it.', 'A lower price on the extra unit matches the lower MU and induces extra purchases.', 'Check the margin: the half-price 3rd unit must still cover its variable cost.', 'Watch cannibalisation: some buyers would have bought three anyway, so you give away part of the margin.'],
         'takeaway': 'Multi-buy discounts are pricing to the falling marginal utility of extra units.'},
        {'id': 'j2', 'title': 'Toll pricing for a new bridge', 'role': 'CA in a public infrastructure consultancy',
         'situation': 'A state government asks for a recommendation on the toll for a new bridge expected to carry 20,000 vehicles a day.',
         'steps': ['Estimate the demand curve: how many vehicles at each toll.', 'Consumer surplus measures the benefit users get beyond the toll they pay — part of the social benefit of the bridge.', 'A very high toll collects revenue but destroys consumer surplus and diverts traffic; a lower toll raises welfare.', 'Present revenue, consumer surplus and total benefit at different tolls.'],
         'takeaway': 'Public projects are judged on consumer surplus, not only on revenue.'},
        {'id': 'j3', 'title': 'Explaining a household budget to a client', 'role': 'CA in personal financial planning',
         'situation': 'A young client earning ₹80,000 a month wants to spend more on travel and also save for a house.',
         'steps': ['Draw the budget line: travel vs savings within ₹80,000.', 'A rise in income shifts the line out; higher rent rotates it inward.', 'The best plan is where the client\'s trade-off (MRS) between travel and saving equals the "price" trade-off.'],
         'takeaway': 'Indifference-curve thinking helps clients see trade-offs clearly.'},
    ]

    mcqs = [
        Q('m1', 'In economics, utility means:', ['Want-satisfying power of a commodity', 'Usefulness of a commodity', 'Moral value of a commodity', 'Price of a commodity'], 0, 'In economics, utility is the want-satisfying power of a commodity — the satisfaction a person expects from it, whether or not it is useful or moral. "Usefulness" is the trap: a cigarette gives utility to a smoker though it is harmful, so utility is ethically neutral and psychological. In practice: market researchers measure what customers enjoy and will pay for, not what experts think is good for them.', 'c1', topic='Nature of Human Wants'),
        Q('m2', 'Which is a characteristic of human wants?', ['Wants are unlimited, but a particular want is satiable', 'Wants are limited in number', 'Each want can never be satisfied', 'Wants never change over time'], 0, 'Human wants are unlimited in number — when one is met, another appears — but any single want can be satisfied at a given time. "Each want can never be satisfied" is the trap; a thirsty person stops wanting water after a few glasses. In practice: once a family buys a refrigerator, it starts wanting an air-conditioner next, which keeps consumer-durable companies launching new products.', 'c1', topic='Nature of Human Wants'),
        Q('m3', 'Goods required because of social customs and habits, not for existence or efficiency, are:', ['Conventional necessaries', 'Necessaries for life', 'Necessaries for efficiency', 'Luxuries'], 0, 'Conventional necessaries are goods people feel compelled to buy because of social customs or habits, not because life or efficiency depends on them. "Luxuries" is the trap — luxuries are bought for pleasure or status, while conventional necessaries feel compulsory because of tradition. In practice: spending on gifts and new clothes during Diwali or weddings is treated as unavoidable by many Indian families, even on tight budgets.', 'c2', topic='Classification of Wants'),
        Q('m4', 'Nourishing food, clean water and education are examples of:', ['Necessaries for efficiency', 'Necessaries for existence', 'Luxuries', 'Conventional necessaries'], 0, 'Necessaries for efficiency are goods that raise a person\'s energy and productivity — nourishing food, clean water, education — beyond bare survival. "Necessaries for existence" is the trap; those are the bare minimum to stay alive, like basic food and shelter. In practice: employers who provide canteen meals and training programmes are investing in necessaries for efficiency, because better-fed, better-trained workers produce more.', 'c2', topic='Classification of Wants'),
        Q('m5', 'The classification of goods into necessaries, comforts and luxuries is:', ['Relative — it changes with person, place and time', 'Fixed for all times', 'Same for all persons', 'Based only on price'], 0, 'Whether a good is a necessary, comfort or luxury is relative: it depends on the person, the place and the time. "Fixed for all times" is the trap — a mobile phone was a luxury in India in the 1990s and is a necessity today. In practice: statistics bodies revise the consumption basket used for the Consumer Price Index from time to time because what households treat as essential keeps changing.', 'c2', topic='Classification of Wants'),
        Q('m6', 'When total utility is maximum, marginal utility is:', ['Zero', 'Maximum', 'Negative', 'Equal to total utility'], 0, 'Total utility rises as long as marginal utility is positive and peaks where marginal utility falls to zero — the point of satiety. "Maximum" is the trap; marginal utility is usually highest at the first unit, when total utility is still low. In practice: at an unlimited buffet, a diner stops eating at the point where one more plate adds nothing; that is maximum total utility with zero marginal utility.', 'c3', topic='Relationship between TU & MU'),
        Q('m7', 'When marginal utility is negative, total utility:', ['Falls', 'Rises', 'Is maximum', 'Is constant'], 0, 'Marginal utility is the change in total utility from one more unit; if it is negative, each extra unit reduces total satisfaction, so total utility falls. "Is maximum" is the trap — total utility is maximum where marginal utility is zero, just before it turns negative. In practice: forcing a fourth sweet on a full guest at a wedding actually lowers their total satisfaction.', 'c3', topic='Relationship between TU & MU'),
        Q('m8', 'TU from 1, 2 and 3 units is 12, 22 and 30 utils. MU of the 3rd unit is:', ['8', '10', '30', '22'], 0, 'Marginal utility of the 3rd unit = TU of 3 units − TU of 2 units = 30 − 22 = 8 utils. 10 is the trap — it is the MU of the 2nd unit (22 − 12), not the 3rd; 30 is total utility, not marginal. In practice: subscription services study how much extra value a customer gets from each additional feature to decide which features to bundle.', 'c3', 'core', '30-22', topic='Relationship between TU & MU'),
        Q('m9', 'At the first unit consumed:', ['TU = MU', 'TU > MU', 'MU = 0', 'TU = 0'], 0, 'For the first unit, total utility consists of that unit alone, so TU = MU. "TU > MU" is the trap — that holds from the second unit onwards, when earlier units add to the total. In practice: the very first cup of tea in the morning gives all of the day\'s tea satisfaction so far, which is why cafés price the first cup and charge less for refills.', 'c3', topic='Relationship between TU & MU'),
        Q('m10', 'The law of diminishing marginal utility does NOT apply when:', ['There is a long time gap between consumption of units', 'Units are identical', 'Consumption is continuous', 'Tastes are constant'], 0, 'The law assumes consumption is continuous; if there is a long time gap between units, the want revives and marginal utility need not fall. "Units are identical" is the trap — identical units are another assumption of the law, so it does apply then. In practice: a person who enjoys a movie and watches the next one a month later gets nearly full satisfaction again, which is why cinemas do not discount repeat monthly visits.', 'c4', topic='Law of Diminishing Marginal Utility'),
        Q('m11', 'The law of diminishing marginal utility is generally said not to apply to:', ['Money and collections such as rare stamps', 'Food', 'Water', 'Clothing'], 0, 'The law is generally said not to apply to money and to collections such as rare stamps or coins: having more can increase the desire for still more. "Food" is the trap — food is the classic case where each extra unit gives less satisfaction. In practice: wealthy investors keep accumulating, and coin collectors pay heavily at auctions to complete a set, showing desire rising with possession.', 'c4', 'moderate', topic='Law of Diminishing Marginal Utility'),
        Q('m12', 'The cardinal utility approach is associated with:', ['Alfred Marshall', 'Hicks and Allen', 'Adam Smith', 'Karl Marx'], 0, 'The cardinal utility approach, which treats utility as measurable in numbers (utils) or money, is associated with Alfred Marshall. "Hicks and Allen" is the trap — they developed the ordinal indifference-curve approach, where utility is only ranked. In practice: when surveys ask "how much would you pay for this feature?", they are using a Marshallian, money-measured view of utility.', 'c4', topic='Law of Diminishing Marginal Utility'),
        Q('m13', 'Consumer surplus is the difference between:', ['What a consumer is willing to pay and what he actually pays', 'Price and cost', 'TU and MU', 'Income and expenditure'], 0, 'Consumer surplus is the gap between the most a buyer would be ready to pay for a good and the price he actually pays. "Price and cost" is the trap — that difference is the seller\'s profit margin, a producer-side idea. In practice: when you would have paid ₹500 for a concert ticket but buy it for ₹300, you enjoy ₹200 of consumer surplus — the reason buyers love "early-bird" prices.', 'c5', topic='Consumer Surplus'),
        Q('m14', 'The concept of consumer surplus was propounded by:', ['Alfred Marshall', 'J. R. Hicks', 'Adam Smith', 'Paul Samuelson'], 0, 'The concept of consumer surplus was developed by Alfred Marshall, using his cardinal utility approach with money as the measure of utility. J. R. Hicks is the trap — he later reformulated the idea using indifference curves, but did not originate it. In practice: governments use consumer-surplus estimates in cost-benefit analysis of projects such as metro rail, counting the value of time saved by commuters.', 'c5', topic='Consumer Surplus'),
        Q('m15', f'A consumer values successive units at ₹45, 38, 32, 27, 23, 20 and 16; price is ₹20. Consumer surplus is:', [R(cs_tot), R(185), R(120), R(61)], 0, 'The consumer buys while worth ≥ price, so 6 units (the 7th is worth only ₹16). Surplus = (45−20) + (38−20) + (32−20) + (27−20) + (23−20) + (20−20) = 25 + 18 + 12 + 7 + 3 + 0 = ₹65. ₹185 is the trap — it is total worth, before subtracting the ₹120 paid; ₹61 wrongly buys the 7th unit. In practice: pricing teams estimate such willingness-to-pay ladders to design bulk discounts.', 'c5', 'moderate', '(45-20)+(38-20)+(32-20)+(27-20)+(23-20)+(20-20)', topic='Consumer Surplus'),
        Q('m16', 'For the demand curve P = 100 − 2Q, consumer surplus at P = ₹40 is:', [R(cs40), R(1800), R(1200), R(450)], 0, 'At P = 40: 40 = 100 − 2Q, so Q = 30. Consumer surplus is the triangle below the demand curve and above price: ½ × 30 × (100 − 40) = ½ × 30 × 60 = ₹900. ₹1,800 is the trap — it forgets the ½; ₹1,200 is the amount actually paid (40 × 30). In practice: regulators estimate such triangles to measure consumer gains from tariff cuts, for example in telecom.', 'c5', 'hard', '0.5*30*(100-40)', topic='Consumer Surplus'),
        Q('m17', 'A fall in the price of a good, other things constant, will:', ['Increase consumer surplus', 'Reduce consumer surplus', 'Not affect consumer surplus', 'Make consumer surplus negative'], 0, 'When price falls, buyers already purchasing pay less for each unit and also buy extra units worth more than the new price, so consumer surplus rises — the triangle above price gets bigger. "Reduce consumer surplus" is the trap; that happens when price rises. In practice: cuts in GST rates on items like televisions are defended partly on the ground that they increase consumers\' welfare.', 'c5', topic='Consumer Surplus'),
        Q('m18', 'A limitation of consumer surplus is that it assumes:', ['Constant marginal utility of money', 'Diminishing marginal utility of goods', 'Rational consumers', 'Given prices'], 0, 'Marshall\'s measure assumes the marginal utility of money stays constant as the consumer spends; in reality, each rupee is worth more to you as your money runs low. "Rational consumers" is the trap — rationality is a general assumption of most demand theory, not the special weakness of consumer surplus. In practice: a ₹100 saving matters far more to a daily-wage worker than to a high earner, which this measure overlooks.', 'c5', 'moderate', topic='Consumer Surplus'),
        Q('m19', 'The indifference curve approach treats utility as:', ['Ordinal — it can be ranked', 'Cardinal — it can be measured in numbers', 'Constant', 'Irrelevant'], 0, 'The indifference curve approach of Hicks and Allen treats utility as ordinal: the consumer only needs to rank bundles — preferred, less preferred or indifferent — not measure satisfaction in numbers. "Cardinal" is the trap; that is Marshall\'s utility approach. In practice: customer surveys that ask people to rank three phone plans, rather than score them in utils, rely on ordinal preferences.', 'c6', topic='Indifference Curve Analysis'),
        Q('m20', 'MRSxy refers to:', ['Units of Y given up for one more unit of X, keeping satisfaction constant', 'Units of X given up for one more Y at higher satisfaction', 'Ratio of TU of X and Y', 'Price of X divided by income'], 0, 'MRSxy is the number of units of Y a consumer is willing to give up to get one more unit of X while staying on the same indifference curve, so satisfaction is unchanged. The option that says "at higher satisfaction" is the trap — moving to a higher satisfaction level would mean a different, higher curve. In practice: a commuter deciding how much shopping time to give up for an extra hour of sleep is weighing such a trade-off.', 'c6', topic='Indifference Curve Analysis'),
        Q('m21', 'Combinations on an IC: (1 X, 20 Y), (2 X, 14 Y), (3 X, 10 Y). MRSxy between the 2nd and 3rd combination is:', ['4', '6', '10', '0.25'], 0, 'Moving from (2 X, 14 Y) to (3 X, 10 Y), the consumer gives up 14 − 10 = 4 units of Y for one more X, so MRSxy = 4. 6 is the trap — it is the MRS between the 1st and 2nd combinations (20 − 14). The falling MRS shows diminishing marginal rate of substitution. In practice: the more data a mobile user already has, the less talk-time they will sacrifice for extra data.', 'c6', 'core', '14-10', topic='Indifference Curve Analysis'),
        Q('m22', 'Indifference curves are convex to the origin because of:', ['Diminishing marginal rate of substitution', 'Increasing marginal utility', 'Constant prices', 'Rising income'], 0, 'Indifference curves are convex to the origin because of the diminishing marginal rate of substitution: the more X a consumer has, the fewer units of Y he will give up for an extra X. "Increasing marginal utility" is the trap — that would contradict the basic tendency of utility to diminish. In practice: a person with plenty of rice but little dal will give up a lot of rice for a bit more dal.', 'c7', topic='Indifference Curve Analysis'),
        Q('m23', 'Two indifference curves cannot intersect because:', ['The intersection point would show two levels of satisfaction at once', 'They are parallel', 'Prices are fixed', 'Income is fixed'], 0, 'If two indifference curves crossed, the common point would lie on both curves, implying equal satisfaction with combinations that the two curves show as different — a logical contradiction of consistency and transitivity. "They are parallel" is the trap; indifference curves need not be parallel, they simply cannot meet. In practice: consistent customer rankings are what make preference surveys usable for product design.', 'c7', topic='Indifference Curve Analysis'),
        Q('m24', 'Indifference curves for perfect complements are:', ['L-shaped', 'Straight lines', 'Concave to the origin', 'Vertical'], 0, 'Perfect complements are used in fixed proportions — a left shoe with a right shoe — so extra units of one alone add no satisfaction, giving L-shaped indifference curves. "Straight lines" is the trap; straight-line curves represent perfect substitutes. In practice: car makers plan tyre purchases in fixed sets of five per car, because extra tyres without cars add nothing.', 'c7', 'moderate', topic='Indifference Curve Analysis'),
        Q('m25', 'With income ₹1,200, Px = ₹40 and Py = ₹30, the maximum quantity of Y that can be bought is:', ['40', '30', '70', '1200'], 0, "If all ₹1,200 is spent on Y, the maximum quantity = income ÷ Py = 1,200 ÷ 30 = 40 units — the budget line's Y-intercept. 30 is the trap: it is the maximum quantity of X (1,200 ÷ 40). In practice: a household with a fixed monthly grocery budget can quickly work out the most of any one item it could afford.", 'c8', 'core', '1200/30', topic='Indifference Curve Analysis'),
        Q('m26', 'A rise in consumer\'s income, prices unchanged, causes the budget line to:', ['Shift outward parallel to itself', 'Rotate around the Y-intercept', 'Become steeper', 'Shift inward'], 0, 'A rise in income with prices unchanged raises both intercepts in the same proportion, so the budget line shifts outward parallel to itself — the slope Px/Py is unchanged. "Rotate around the Y-intercept" is the trap; that happens when only the price of X changes. In practice: a salary hike lets a family buy more of everything at the same relative prices, widening its choices.', 'c8', topic='Indifference Curve Analysis'),
        Q('m27', 'A fall in the price of X only causes the budget line to:', ['Swivel outward around the Y-intercept', 'Shift outward parallel', 'Shift inward parallel', 'Remain unchanged'], 0, 'If only the price of X falls, more X can be bought with the same income, so the X-intercept moves out while the Y-intercept stays put — the line swivels outward around the Y-intercept. "Shift outward parallel" is the trap; a parallel shift needs a change in income, not in one price. In practice: a discount on mobile data alone expands a user\'s options without changing how much talk-time they could buy.', 'c8', 'moderate', topic='Indifference Curve Analysis'),
        Q('m28', 'At consumer equilibrium in the indifference curve approach:', ['MRSxy = Px/Py', 'MRSxy = Py/Px', 'MUx = 0', 'TU is minimum'], 0, 'The consumer is in equilibrium where the budget line is tangent to the highest attainable indifference curve; there the slopes are equal, so MRSxy = Px/Py. "MRSxy = Py/Px" is the trap — it inverts the price ratio. In practice: a rational shopper keeps adjusting the mix of two goods until the rate at which she would trade them equals the rate at which the market lets her trade them.', 'c8', topic='Indifference Curve Analysis'),
        Q('m29', 'The slope of the budget line equals:', ['The ratio of the prices of the two goods (Px/Py)', 'MRS always', 'Income divided by price', 'Total utility'], 0, 'The slope of the budget line (ignoring sign) equals the price ratio Px/Py — the rate at which the market lets the consumer exchange Y for X. "MRS always" is the trap; MRS is the slope of the indifference curve, and it equals the price ratio only at the equilibrium point. In practice: when one product becomes relatively costlier, the budget line becomes steeper, showing the new market trade-off.', 'c8', 'moderate', topic='Indifference Curve Analysis'),
        Q('m30', 'In the consumer surplus schedule, the consumer stops buying where:', ['Marginal utility (in money) equals price', 'Total utility is zero', 'Marginal utility is maximum', 'Price is zero'], 0, 'A rational consumer keeps buying as long as the marginal utility of a unit, in money terms, is at least its price, and stops where marginal utility equals price. "Total utility is zero" is the trap — total utility is still large at that point; it is marginal utility that has fallen to the price. In practice: a shopper stops adding mangoes to the basket once another kilo feels worth no more than its price.', 'c5', topic='Consumer Surplus'),
    ]

    questions = [
        {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'TU from 1 to 6 units of a commodity is 20, 36, 48, 54, 54 and 50 utils. Compute MU, identify the point of satiety and explain the relationship between TU and MU.',
         'model': [table(['Units', 'TU', 'MU'], [[i + 1, t, m_] for i, (t, m_) in enumerate(zip([20, 36, 48, 54, 54, 50], q1_mu))]),
                   p('Point of satiety: 5th unit (TU maximum at 54, MU = 0). TU rises at a diminishing rate while MU falls but is positive (units 1–4); TU is maximum when MU = 0; TU falls when MU is negative (6th unit, MU = −4).')],
         'scheme': [{'id': 's1', 'pt': 'MU column correct', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Point of satiety identified', 'm': 1, 'skill': 'analysis'}, {'id': 's3', 'pt': 'TU–MU relationship stated', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Show MU for the first unit as equal to TU.'], 'mistakes': ['Calling the 4th unit the point of satiety because TU first reaches 54 there — MU of the 4th unit is still 6.'], 'tips': ['Mark the point where MU = 0 clearly.'], 'checks': cq1},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'The demand curve for a museum visit is P = 150 − 5Q (P in ₹, Q visits per year). The ticket price is ₹50. Compute (a) visits, (b) amount spent, (c) total willingness to pay, and (d) consumer surplus. Show steps.',
         'model': [p(f'(a) 50 = 150 − 5Q → Q = {q2_q} visits.'), p(f'(b) Amount spent = 50 × 20 = {R(q2_paid)}.'),
                   p(f'(c) Total willingness to pay = area under the demand curve up to Q = 20 = rectangle (50 × 20 = ₹1,000) + triangle (½ × 20 × 100 = ₹1,000) = {R(q2_tu)}.'),
                   p(f'(d) Consumer surplus = {R(q2_tu)} − {R(q2_paid)} = {R(q2_cs)} (the triangle above the price line).')],
         'scheme': [{'id': 's1', 'pt': 'Quantity from the demand equation', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Amount spent', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Total willingness to pay (area under curve)', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Consumer surplus', 'm': 1.5, 'skill': 'computation'}],
         'remarks': ['Drawing the triangle in rough work avoids sign errors.'], 'mistakes': ['Forgetting the ½ in the triangle area.'], 'tips': ['CS = ½ × Q × (maximum price − market price) for a straight-line demand curve.'], 'checks': cq2},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Ravi has ₹2,400 to spend on X (₹60) and Y (₹40). (a) Find the intercepts and slope of his budget line. (b) Is the bundle (24 X, 30 Y) affordable? (c) At his chosen bundle on the budget line, his MRSxy is 2. Is he in equilibrium? If not, which way should he move?',
         'model': [p(f'(a) X-intercept = 2,400 ÷ 60 = {q3_x}; Y-intercept = 2,400 ÷ 40 = {q3_y}; slope = Px/Py = {q3_r}.'),
                   p(f'(b) Cost = 60 × 24 + 40 × 30 = {R(q3_chk)} > ₹2,400 — not affordable (it lies outside the budget line). (A bundle costing exactly ₹2,400, such as 24 X and 24 Y, would lie on the line.)'),
                   p(f'(c) Equilibrium needs MRSxy = Px/Py = {q3_r}. Here MRS = 2 > 1.5: he values one X at 2 Y, while the market charges only 1.5 Y. He gains by buying more X and less Y; as he does so, MRS diminishes until it equals 1.5.')],
         'scheme': [{'id': 's1', 'pt': 'Intercepts and slope', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Affordability test', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Equilibrium condition MRS = Px/Py', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Correct direction of adjustment with reason', 'm': 1.5, 'skill': 'analysis'}],
         'remarks': ['Direction of adjustment is where most students lose marks.'], 'mistakes': ['Comparing MRS with Py/Px instead of Px/Py.'], 'tips': ['If MRSxy > Px/Py, buy more X; if less, buy more Y.'], 'checks': cq3},
    ]

    viva = [
        V('v1', 'State the law of diminishing marginal utility.',
          'Other things remaining the same, when a person goes on consuming extra units of a good, the marginal utility diminishes with each successive unit. Each extra unit adds less satisfaction than the one before.',
          [P('p1', 'As more units are consumed', 3, 'more and more|more unit|successive unit|additional unit|each extra|every extra|extra unit|more of a|increase consumption|consume more|consumes more|more of the'),
           P('p2', 'Marginal utility diminishes / falls', 5, ALT('{m} {d}', m=['marginal utility', 'mu', 'extra utility', 'additional utility', 'utility from each', 'satisfaction from each', 'extra satisfaction', 'additional satisfaction'], d=['diminish', 'fall', 'decreas', 'declin', 'go down', 'goes down', 'reduc', 'less'])),
           P('p3', 'Other things remaining the same', 2, 'other things|ceteris paribus|constant|same|given')], 'c4'),
        V('v2', 'What is the relationship between total utility and marginal utility?',
          'Total utility is the sum of marginal utilities. While total utility increases at a diminishing rate, marginal utility falls but stays positive. Marginal utility is zero when total utility is maximum, and marginal utility is negative when total utility falls.',
          [P('p1', 'TU is the sum of MUs', 2, 'sum|total of|add|summation'),
           P('p2', 'TU maximum when MU is zero', 4, ALT('{t} {mx} {m} {z}', '{m} {z} {t} {mx}', t=['total utility', 'tu'], mx=['maximum', 'max', 'highest', 'peak'], m=['marginal utility', 'mu', ''], z=['zero', '0', 'nil'])),
           P('p3', 'TU falls when MU is negative', 4, ALT('{t} {f} {m} negative', '{m} negative {t} {f}', 'negative {m} {t} {f}', t=['total utility', 'tu'], f=['fall', 'decreas', 'declin', 'go down', 'goes down', 'reduc'], m=['marginal utility', 'mu', '']))], 'c3'),
        V('v3', 'What is consumer surplus, and how is it measured?',
          'Consumer surplus is the excess of what a consumer is willing to pay for a good over what he actually pays. It is measured as total willingness to pay minus the amount actually paid; on a graph it is the triangle-shaped area lying under the demand curve but over the price line. The concept was given by Marshall.',
          [P('p1', 'Willing to pay minus actually paid', 6, ALT('{w} {mi} {a}', w=['willing', 'ready to pay', 'prepared to pay', 'willingness'], mi=['minus', 'less', 'over', 'exceed', 'more than', 'difference', 'above'], a=['actual', 'paid', 'pays', 'price']) + '|difference between what he is willing|difference between willingness|excess of what|excess of price he is willing'),
           P('p2', 'Area below demand curve and above price line', 2, 'area|triangle|below demand|under demand|above price', min=1),
           P('p3', 'Given by Marshall', 2, 'marshall')], 'c5'),
        V('v4', 'State any four properties of indifference curves.',
          'Indifference curves slope downward from left to right, they are convex to the origin because of diminishing marginal rate of substitution, two indifference curves never intersect, a curve lying higher means more satisfaction, and they do not touch either axis.',
          [P('p1', 'Slope downward', 2, 'slope downward|downward slop|negative slope|negatively slop|slope down|fall from left|downward sloping|slopes down'),
           P('p2', 'Convex to the origin', 3, 'convex'),
           P('p3', 'Never intersect', 3, 'never intersect|not intersect|cannot intersect|can t intersect|do not cut|never cut|cannot cut|never cross|not cross|cannot cross|don t intersect|do not intersect|never touch each other'),
           P('p4', 'Higher IC = higher satisfaction; do not touch axes', 2, 'higher indifference curve higher|higher curve higher|higher ic higher|higher satisfaction|more satisfaction|not touch|never touch either axis|do not touch|does not touch', min=1)], 'c7'),
        V('v5', 'What is the condition of consumer equilibrium in the indifference curve approach?',
          'The consumer is in equilibrium where the budget line is tangent to the highest attainable indifference curve. At that point the marginal rate of substitution of X for Y equals the price ratio Px by Py, and the indifference curve is convex to the origin.',
          [P('p1', 'Budget line tangent to the highest attainable IC', 4, 'tangent|touch|tangency', 'highest|budget line|price line', min=2),
           P('p2', 'MRSxy = Px/Py', 4, ALT('{m} {e} {p}', m=['mrs', 'marginal rate of substitution', 'mrsxy', 'mrs xy', 'mrs of x for y'], e=['equal', 'equals', 'same as', 'is', '='], p=['px py', 'px by py', 'price ratio', 'ratio of price', 'ratio of the price', 'px over py', 'price of x by price of y', 'price of x divided by price of y', 'price of x over price of y', 'px divided by py']) + '|price ratio equal mrs|px by py equal mrs|px py equal mrs'),
           P('p3', 'IC convex at the point (second-order condition)', 2, 'convex|diminishing mrs|mrs diminish|mrs falling|mrs declin')], 'c8'),
        V('v6', 'Does the law of diminishing marginal utility apply to money and collections like rare stamps?',
          'Generally no. The law may not apply to money, gold or collections such as rare stamps, because having more of them can increase the desire for still more, as with a miser or a collector.',
          [P('p1', 'Generally no — may not apply', 5, 'no|not apply|does not apply|may not apply|doesn t apply|exception|not hold|does not hold', min=1),
           P('p2', 'More of them increases the desire (miser / collector)', 5, 'increas desire|more desire|desire for more|desire increas|want more|greed|miser|never satisfied|never enough|craving|keener|increases the urge|hunger for more', min=1)], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Isha\'s entertainment budget', 'difficulty': 'moderate',
              'case': ('Isha loves watching films in theatres. In a month she is willing to pay ₹120 for the first show, ₹100 for the second, ₹85 for the third, ₹70 for the fourth, ₹60 for the fifth and ₹50 for the sixth. A multiplex charges ₹60 a ticket. '
                       'Separately, she sets aside ₹3,000 a month for movies (₹300 a show at a premium hall) and snacks (₹150 a combo), and she chooses a bundle where her indifference curve touches this budget line.'),
              'mcqs': [
                  Q('k1a', 'At ₹60 a ticket, how many shows does Isha watch?', ['5', '4', '6', '3'], 0, 'Isha watches a show as long as her willingness to pay is at least ₹60: ₹120, ₹100, ₹85, ₹70 and ₹60 qualify, giving 5 shows. 6 is the trap — the sixth show is worth only ₹50 to her, below the ₹60 price. In practice: multiplexes run weekday discounts precisely to capture viewers like Isha whose value for an extra show is below the regular price.', 'c5', 'core', '5', topic='Consumer Surplus'),
                  Q('k1b', 'Her consumer surplus at ₹60 a ticket is:', [R(k_cs), R(435), R(125), R(165)], 0, 'Consumer surplus = (120 − 60) + (100 − 60) + (85 − 60) + (70 − 60) + (60 − 60) = 60 + 40 + 25 + 10 + 0 = ₹135. ₹435 is the trap — it is her total willingness to pay for five shows, before subtracting the ₹300 actually paid; ₹125 wrongly adds the sixth show, which has a surplus of −10. In practice: subscription pricing tries to capture part of this surplus through monthly passes.', 'c5', 'moderate', '(120-60)+(100-60)+(85-60)+(70-60)+(60-60)', topic='Consumer Surplus'),
                  Q('k1c', 'If the ticket price falls to ₹50, her consumer surplus becomes:', [R(k_cs2), R(k_cs), R(175), R(235)], 0, "At ₹50 she watches six shows: (120 − 50) + (100 − 50) + (85 − 50) + (70 − 50) + (60 − 50) + (50 − 50) = 70 + 50 + 35 + 20 + 10 + 0 = ₹185. ₹135 is the trap — it is the surplus at the old ₹60 price; the lower price raises surplus both on existing shows and through an extra show. In practice: ticket price cuts are judged partly by how much they increase viewers' welfare.", 'c5', 'hard', '(120-50)+(100-50)+(85-50)+(70-50)+(60-50)+(50-50)', topic='Consumer Surplus'),
                  Q('k1d', 'On her premium-hall budget line, the maximum number of shows (no snacks) is:', [str(k_x), str(k_y), '15', '30'], 0, 'If her whole ₹3,000 goes on premium shows at ₹300 each, the maximum is 3,000 ÷ 300 = 10 shows — one intercept of her budget line. 20 is the trap: it is the maximum number of snack combos (3,000 ÷ 150). In practice: drawing up a monthly entertainment budget means first knowing the extremes — all on one item or all on the other — before choosing a mix.', 'c8', 'core', '3000/300', topic='Indifference Curve Analysis'),
                  Q('k1e', 'At her chosen bundle, her MRS of shows for snacks equals:', ['2', '0.5', '10', '20'], 0, "At the tangency point, MRS of shows for snacks equals the price ratio: P(show) ÷ P(snack) = 300 ÷ 150 = 2, so she would give up 2 snack combos for one more show. 0.5 is the trap — it divides the snack price by the show price, inverting the ratio. In practice: a consumer instinctively stops trading snacks for shows once her personal trade-off matches the market's price ratio.", 'c8', 'moderate', '300/150', topic='Indifference Curve Analysis'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch02', 'n': 2, 'title': 'Theory of Consumer Behaviour',
        'outcomes': ['Explain the nature and classification of human wants and the meaning of utility.', 'Relate total and marginal utility and apply the law of diminishing marginal utility with its limitations.',
                     'Measure consumer surplus from a schedule and from a demand curve, and state its uses and limitations.', 'Explain indifference curves, MRS, their properties, the budget line and consumer equilibrium.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 50}, 'prereq': ['fnd-p4-ch02-u01'],
                 'exam_tip': 'Expect MCQs on TU–MU relationships, consumer surplus calculations, IC properties and the equilibrium condition MRSxy = Px/Py. Read whether the question gives MU or TU.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Wants: unlimited, satiable individually, competitive, complementary, relative; utility = want-satisfying power (not usefulness, no ethics).', 'Classification: necessaries (life, efficiency, conventional), comforts, luxuries — relative.',
                                 'TU = ΣMU; MU = TUn − TUn−1; TU max ⇔ MU = 0; TU falls ⇔ MU < 0.', 'LDMU: assumptions — identical units, standard size, continuity, constant tastes; exceptions — money, collections, related goods.',
                                 'Consumer surplus = willing to pay − actually paid; area under demand curve above price; Marshall.', 'IC: ordinal utility, MRS diminishing; properties — downward slope, convex, non-intersecting, higher = better, not touching axes.',
                                 'Budget line Px·X + Py·Y = M; equilibrium where IC tangent to budget line: MRSxy = Px/Py.'],
                     'remember': ['Consumer buys till MU (₹) = price.', 'Income change → parallel shift; one price change → rotation.', 'Perfect substitutes: straight-line ICs; perfect complements: L-shaped.'],
                     'traps': ['The point of satiety is where MU = 0, not where TU first reaches its highest number if MU is still positive.', 'Slope of budget line = Px/Py (not Py/Px).', 'Utility ≠ usefulness.']},
        'quickref': [{'k': 'MU', 'v': 'TUn − TUn−1'}, {'k': 'Consumer surplus', 'v': 'ΣWTP − P × Q; linear demand: ½ × Q × (Pmax − P)'}, {'k': 'MRSxy', 'v': '−ΔY/ΔX (slope of IC)'},
                     {'k': 'Budget line', 'v': 'Px·X + Py·Y = M; intercepts M/Px, M/Py'}, {'k': 'Equilibrium', 'v': 'MRSxy = Px/Py, IC convex'}],
        'viva': viva, 'cases': cases,
    }
