"""CA Foundation · Paper 4 Business Economics · Chapter 1 · Unit 2 Basic Problems of an Economy & Role of Price Mechanism.
Original explanations, examples and questions (ICAI structure and scope only)."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch01-u02'


def Q(mid, q, opts, ans, ex, c, d='core', check=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if check: x['check'] = check
    return x


def build():
    # ---- i1: how to produce — choice of technique by relative factor prices ----
    c1 = Checks()
    # 1,000 metres of cloth: Technique A (handloom) 40 workers + 2 machines; B (power loom) 10 workers + 6 machines
    a_cost1 = c1.add('40*500+2*3000', 'Technique A cost when wage ₹500, machine ₹3,000 a day')
    b_cost1 = c1.add('10*500+6*3000', 'Technique B cost when wage ₹500, machine ₹3,000 a day')
    a_cost2 = c1.add('40*900+2*3000', 'Technique A cost when wage rises to ₹900')
    b_cost2 = c1.add('10*900+6*3000', 'Technique B cost when wage rises to ₹900')

    # ---- i2: price mechanism signals what to produce ----
    c2 = Checks()
    cost_u = 400
    p_car0, p_car1 = 450, 520
    prof_car0 = c2.add('(450-400)*1000', 'profit on gadget X at old price')
    prof_car1 = c2.add('(520-400)*1000', 'profit on gadget X at new price')
    p_cl0, p_cl1 = 450, 410
    prof_cl0 = c2.add('(450-400)*1000', 'profit on gadget Y at old price')
    prof_cl1 = c2.add('(410-400)*1000', 'profit on gadget Y at new price')

    # ---- case: Rivertown chooses its system ----
    k = Checks()
    k_cons = k.add('100-30', 'percentage of output consumed now when 30% is saved and invested')

    concepts = [
        {'id': 'c1', 'title': 'The central economic problem and its four parts',
         'body': ['Every country — rich or poor, capitalist or socialist — has limited resources (natural resources, capital goods, consumer goods, money, time) with many alternative uses. Coal can run a factory, generate electricity or cook food; money can be spent in a thousand ways. If resources were unlimited, or if each had only one use, there would be no economic problem. The scarcity of resources relative to wants is called the central economic problem.',
                  'It splits into four basic problems: (1) What to produce, and how much of each? — more guns or more butter, more machines (capital goods) or more mobile phones (consumer goods), how many hospitals, schools, tonnes of wheat. (2) How to produce? — labour-intensive or capital-intensive techniques (handloom, power loom or automatic loom); the choice depends on the availability and relative prices of labour and capital, and society gains by using techniques that make best use of what it has. (3) For whom to produce? — how the output (the "national cake") is shared among people, i.e. distribution. (4) What provision for economic growth? — how much current consumption to give up for saving and investment so that productive capacity rises; with no provision, living standards stagnate and may later fall.',
                  'An economic system is the total set of arrangements and institutions through which a society produces and distributes goods and services — the mechanism that gives effect to its economic choices. Economies are grouped as capitalist, socialist and mixed according to ownership, mode of production and distribution, and the role of government.'],
         'blocks': [table(['Basic problem', 'Question in plain words', 'Example'], [
             ['What to produce', 'Which goods, and how many of each?', 'More metro lines or more highways?'],
             ['How to produce', 'With which technique?', 'Manual harvesting or combine harvesters?'],
             ['For whom to produce', 'Who gets how much?', 'Share of output going to wage-earners vs owners'],
             ['Provision for growth', 'How much to save and invest for the future?', 'Spend the budget on subsidies now, or on power plants for later?']], title='Four basic problems')],
         'analogy': 'A family with one salary must decide what to buy, whether to cook at home or order in, how to share treats among children, and how much to save for the future — the four problems at home.',
         'work': 'Government budgets, which CAs analyse every February, are a public answer to these four questions: what the state will produce, how, for whom and how much it will invest for growth.'},
        {'id': 'c2', 'title': 'Capitalist economy — features',
         'body': ['In a capitalist (free market, laissez-faire) economy, factories, land, mines and other productive resources belong to private persons, who decide how to use them in order to earn profit. Private property is its foundation and the profit motive its driving force; the decisions of consumers and firms run the economy and, ideally, the government plays only a limited role. The USA, UK, Hong Kong and South Korea are often cited, though none is a pure form.',
                  'Features: (1) Right to private property — land, factories, mines can be privately owned, used as the owner likes and passed on by inheritance, subject to restrictions for public good. (2) Freedom of enterprise — anyone may start any business. (3) Freedom of economic choice — in consumption, work, production and exchange. (4) Profit motive — guides all activity. (5) Consumer sovereignty — the consumer is "king": buyers\' spending decides what is produced and in what quantities. (6) Competition — the most important feature; it brings out efficiency. (7) Absence of government interference — no central plan; self-interest and the price mechanism run the economy automatically.'],
         'analogy': 'A capitalist economy is like a giant online marketplace with no central manager: sellers list what they think buyers want, prices rise for hot items and fall for unpopular ones, and production follows the money.',
         'work': 'When CAs evaluate a start-up\'s business plan, they rely on capitalist features: freedom to enter, consumers\' preferences shown through prices, and competition from rivals.'},
        {'id': 'c3', 'title': 'How the price mechanism solves the central problems',
         'body': ['A capitalist economy has no planning authority, yet there is no chaos. The impersonal forces of demand and supply — the price mechanism (market mechanism) — coordinate millions of decisions.',
                  'What to produce: if consumers want more of a good, its price rises; with costs unchanged, profit rises and producers make more of it. If demand for a good falls, its price and profit fall and less is produced. Consumers "vote" with their spending. How to produce: each producer uses the technique that minimises cost — labour-intensive where labour is relatively cheap, capital-intensive where labour is relatively dear. Relative factor prices decide. For whom to produce: goods go to those with purchasing power, which depends on income — earnings from work, the prices of the factors one owns, and property owned. Consumption, saving and investment (growth): households consume and save, guided by income and the interest rate; entrepreneurs invest according to the expected rate of return on capital. Interest and the return on capital are the "prices" of capital.'],
         'analogy': 'Prices are traffic signals: a rising price is a green light telling producers "make more here"; a falling price is a red light saying "move your resources elsewhere".',
         'work': 'Market research and pricing teams read these signals daily — a sustained price rise in a segment is a cue for capacity expansion, which CAs then evaluate through project appraisal.'},
        {'id': 'c4', 'title': 'Capitalism — merits and demerits',
         'body': ['Merits: self-regulating through the price mechanism, with no cost of collecting information or running a planning machinery; private property and profit give strong incentives and efficiency; growth tends to be faster as investors choose only viable projects; resources go to their most productive uses; costs are minimised; consumers get variety and quality at reasonable prices and higher living standards; innovation and technological progress are rewarded; fundamental rights such as freedom and private property are preserved; enterprise and risk-taking are encouraged and the inefficient are penalised; it usually works within democracy.',
                  'Demerits: large inequality of income and wealth, dividing society into "haves" and "have-nots" and causing unrest; property rights placed above human rights; unequal opportunities; welfare ignored because the aim is profit; demand pattern reflects the purchasing power of the rich, not the real needs of society; exploitation of labour, strikes and job insecurity; consumer sovereignty often a myth; resources diverted to luxuries rather than wage goods; too few merit goods (education, health) and too many harmful but profitable goods; instability — overproduction, depression, unemployment; waste on advertising and sales promotion; growth of monopolies; excessive materialism and environmental damage.'],
         'analogy': 'Capitalism is a high-speed engine with weak brakes: it moves fast, but without regulation it can crash into inequality and instability.',
         'work': 'Competition law, labour codes and environmental rules — areas where CAs advise on compliance — exist precisely to correct the demerits of an unregulated market.'},
        {'id': 'c5', 'title': 'Socialist economy — features, merits and demerits',
         'body': ['The idea of socialism was set out by Karl Marx and Friedrich Engels in "The Communist Manifesto" (1848). The material means of production (factories, mines, capital) are owned by the community, represented by the State, and everyone shares the fruits on the basis of equal rights. It is also called a command economy or centrally planned economy, because a central planning authority allocates resources and market forces play little role. The central problems are solved through planning, aimed at maximum social welfare. The former USSR (1917–1990) is the classic example; China, Vietnam, Cuba and North Korea are also cited, though no country today is purely socialist.',
                  'Features: (1) Collective ownership of the means of production (small farms, workshops and trading firms may remain private); profit and self-interest are not the driving forces. (2) Economic planning by a central planning authority, which decides what, how much and how to produce. (3) Limited consumer choice — freedom from hunger is guaranteed but the range of goods is restricted; the right to work is guaranteed but choice of occupation is restricted. (4) Relatively equal distribution of income — little scope to accumulate private capital, and education and other facilities are shared more equally. (5) Minimum role of the price mechanism — prices are "administered prices" fixed by the planners; market prices play only a secondary role, such as clearing accumulated stocks. (6) Absence of competition — the State is the sole entrepreneur.',
                  'Merits: equitable distribution and equal opportunity (economic and social justice); rapid, balanced development through coordinated planning; better use of resources and no waste on advertising; minimal unemployment and stability without business cycles; a co-operative outlook instead of class war; right to work and a minimum living standard; protection of workers and consumers from exploitation; comprehensive social security.',
                  'Demerits: bureaucracy, delays, red tape, corruption and favouritism; loss of individual freedom; no right to private property; weak incentives to work hard; administered prices give no sound basis for cost calculation, so efficient allocation becomes impossible; state monopolies can become uncontrollable; limited consumer choice; no reward for personal efficiency; the extreme form is impractical.'],
         'analogy': 'A socialist economy is a school canteen run by the principal: everyone gets a fair, affordable meal, but the menu is fixed and the cook has little reason to improve the food.',
         'work': 'Price controls and administered prices still exist in parts of mixed economies (for example, some essential drugs). Cost accountants and CAs are often asked to certify costs used to fix such prices — exactly the "basis for cost calculation" that socialism lacked.'},
        {'id': 'c6', 'title': 'Mixed economy — features, merits and demerits',
         'body': ['A mixed economy relies on both markets and government to allocate resources; in fact every real-world economy is mixed to some degree. It tries to combine the best features of capitalism (private enterprise, profit motive, efficiency) and socialism (planning, welfare, equity) while avoiding the worst of each. The State runs important and strategic industries, allows private enterprise a positive role, and regulates the private sector so that it serves national welfare. India is a well-known example.',
                  'Feature — co-existence of private and public sectors, giving three sectors: (a) private sector — owned and managed by individuals and groups, driven by profit, but regulated by government policy; (b) public sector — set up by the State mainly for public welfare, not primarily for profit; (c) combined (joint) sector — government and private enterprise join hands to produce goods and services.',
                  'Merits: economic freedom and private property give incentives; price mechanism and competition push the private sector to efficiency; consumer sovereignty and choice; incentives for innovation, enterprise and risk-taking; benefits of planning and rapid development on plan priorities; greater equality and freedom from exploitation through state participation; harms of cut-throat competition checked by laws on environment and labour.',
                  'Demerits: a mixed economy is not always a "golden path". There may be excessive state control that cuts incentives and private growth, poor plan implementation, high taxes, inefficiency, corruption, waste, delays and poor public-sector performance; it is hard to keep the right balance between the two sectors; and without strong government initiative the private sector may grow out of proportion, so the economy drifts towards capitalism with its drawbacks.'],
         'analogy': 'A mixed economy is a road with both private cars and public buses, plus traffic police: freedom to drive, public transport for all, and rules to stop accidents.',
         'work': 'CAs in India work across all three sectors — auditing private companies, public sector undertakings (often via C&AG-appointed audits) and joint-venture companies — a daily reminder of the mixed economy.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'How to produce: relative factor prices decide the technique', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'A firm can produce 1,000 metres of cloth a day by Technique A (handloom: 40 workers + 2 machines) or Technique B (power loom: 10 workers + 6 machines). Machine cost is ₹3,000 per machine per day. (a) Which technique will a profit-seeking firm choose if the daily wage is ₹500? (b) What if the wage rises to ₹900? (c) Which basic problem does this illustrate, and how does a capitalist economy solve it?',
         'solution': [table(['Technique', 'Cost at wage ₹500 (₹)', 'Cost at wage ₹900 (₹)'], [['A — labour-intensive (40 L + 2 K)', a_cost1, a_cost2], ['B — capital-intensive (10 L + 6 K)', b_cost1, b_cost2]], title='Daily cost of 1,000 metres'),
                      p(f'(a) At ₹500, A costs {R(a_cost1)} and B costs {R(b_cost1)}. A is cheaper, so the firm chooses the labour-intensive technique.'),
                      p(f'(b) At ₹900, A costs {R(a_cost2)} and B costs {R(b_cost2)}. Now B is cheaper, so the firm switches to the capital-intensive technique.'),
                      p('(c) This is the problem of "how to produce". In a capitalist economy, relative factor prices (the wage compared with the cost of capital) guide each firm to the least-cost technique, without any planner.')],
         'checks': c1},
        {'id': 'i2', 'title': 'What to produce: prices and profits as signals', 'difficulty': 'core', 'minutes': 6,
         'q': f'Two gadgets X and Y each cost {R(cost_u)} a unit to make and sell for {R(450)}; a firm sells 1,000 units of each. Consumers\' tastes shift: the price of X rises to {R(p_car1)} and that of Y falls to {R(p_cl1)}. Compute the profit on each before and after, and explain how the market decides "what to produce".',
         'solution': [table(['Gadget', 'Profit before (₹)', 'Profit after (₹)'], [['X (demand up)', prof_car0, prof_car1], ['Y (demand down)', prof_cl0, prof_cl1]], title='Profit on 1,000 units'),
                      p(f'Profit on X rises from {R(prof_car0)} to {R(prof_car1)}; on Y it falls from {R(prof_cl0)} to {R(prof_cl1)}. Producers move resources from Y to X, so more X and less Y are produced — exactly what consumers asked for through their spending. This is consumer sovereignty working through the price mechanism.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Identify the economic system', 'difficulty': 'core', 'minutes': 5,
         'q': 'Identify the economic system indicated by each feature: (1) administered prices; (2) consumer sovereignty and laissez-faire; (3) public, private and joint sectors side by side; (4) central planning authority decides what to produce; (5) right to private property and freedom of enterprise with no planning; (6) state runs strategic industries and regulates private firms.',
         'solution': [table(['Feature', 'System'], [['(1) Administered prices', 'Socialist'], ['(2) Consumer sovereignty, laissez-faire', 'Capitalist'], ['(3) Three sectors side by side', 'Mixed'], ['(4) Central planning authority', 'Socialist'], ['(5) Private property, free enterprise, no plan', 'Capitalist'], ['(6) State in strategic industries + regulated private sector', 'Mixed']])]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Choosing between automation and manual packing', 'role': 'CA in industry — plant controller',
         'situation': 'Minimum wages in the state have gone up by 30%. Operations wants to buy automatic packing machines.',
         'steps': ['Recognise the "how to produce" question: compare a labour-intensive and a capital-intensive technique.', 'Cost both methods per 1,000 units at the new wage, including machine depreciation, interest and maintenance.', 'Consider non-cost factors: flexibility, quality, social impact on workers, government incentives.', 'Recommend the least-cost technique, with a plan to redeploy workers.'],
         'takeaway': 'Relative factor prices change the best technique — the price mechanism at work inside a firm.',
         'think': 'If the government gave a large subsidy on machinery, how would the decision change?', 'answer': 'The subsidy lowers the price of capital relative to labour, making the capital-intensive technique more attractive.'},
        {'id': 'j2', 'title': 'Advising a PSU on pricing', 'role': 'CA in a consultancy assignment for a public sector undertaking',
         'situation': 'A state-owned fertiliser company sells at a government-fixed price below cost; the government reimburses the gap.',
         'steps': ['Identify the administered price — a socialist tool used within India\'s mixed economy.', 'Compute the actual cost per tonne and the subsidy claim carefully, since there is no market price to guide efficiency.', 'Suggest cost-reduction measures, because without competition the incentive to cut costs is weak.'],
         'takeaway': 'Where prices are administered, cost data replaces the market as the guide — making accurate cost certification vital.'},
        {'id': 'j3', 'title': 'Joint-sector project appraisal', 'role': 'Articled assistant in a project finance team',
         'situation': 'A state development corporation and a private company plan a joint venture for an industrial park.',
         'steps': ['Note this is the combined (joint) sector of a mixed economy.', 'Map the objectives: the private partner seeks profit; the state partner seeks jobs and regional development.', 'Build the financial model so that both objectives are visible — returns for the private partner, employment for the state.'],
         'takeaway': 'Joint-sector projects must balance profit and public welfare — the essence of a mixed economy.'},
    ]

    mcqs = [
        Q('m1', 'The central economic problem is the problem of:', ['Scarcity of resources relative to wants', 'Shortage of money only', 'Excess of resources', 'Over-population only'], 0, 'Scarcity relative to wants underlies every economic system.', 'c1'),
        Q('m2', 'Which of the following is NOT one of the basic economic problems?', ['How to fix the exchange rate of the rupee', 'What to produce', 'How to produce', 'For whom to produce'], 0, 'The four problems are what, how, for whom and provision for growth.', 'c1'),
        Q('m3', 'Choice between labour-intensive and capital-intensive techniques relates to:', ['How to produce', 'What to produce', 'For whom to produce', 'Provision for growth'], 0, 'Technique of production = how to produce.', 'c1'),
        Q('m4', 'The decision on how the national output is shared among people relates to:', ['For whom to produce', 'What to produce', 'How to produce', 'Economic growth'], 0, 'Distribution of the "national cake" = for whom.', 'c1'),
        Q('m5', 'Deciding between more capital goods and more consumer goods is mainly a question of:', ['What to produce (and provision for growth)', 'How to produce only', 'For whom to produce', 'Distribution of income'], 0, 'Which goods to produce, with capital goods also building future capacity.', 'c1', 'moderate'),
        Q('m6', 'If a society uses all its resources for current consumption, then:', ['Its productive capacity will not grow and living standards may later fall', 'Growth will be fastest', 'Unemployment will vanish', 'Prices will fall'], 0, 'Growth needs saving and investment — sacrifice of present consumption.', 'c1'),
        Q('m7', 'An economic system is best described as:', ['The total arrangements through which a society produces and distributes goods and services', 'A government department', 'A stock exchange', 'A bank'], 0, 'It is the set of institutions that gives effect to economic choices.', 'c1'),
        Q('m8', 'Laissez-faire economy is another name for:', ['Capitalist economy', 'Socialist economy', 'Mixed economy', 'Command economy'], 0, 'Laissez-faire = leave it alone; free market.', 'c2'),
        Q('m9', 'The driving force of a capitalist economy is:', ['Profit motive', 'Social welfare', 'Central planning', 'Administered prices'], 0, 'Private property is the mainstay and profit motive the driving force.', 'c2'),
        Q('m10', 'Consumer sovereignty means:', ['Consumers ultimately decide what is produced and in what quantities', 'Government decides consumption', 'Producers decide what consumers buy', 'Consumers fix prices by law'], 0, 'Buyers\' spending directs the allocation of resources.', 'c2'),
        Q('m11', 'The most important feature of a capitalist economy is often said to be:', ['Competition', 'Central planning', 'Collective ownership', 'Administered prices'], 0, 'Competition brings efficiency in the use of resources.', 'c2'),
        Q('m12', 'In a capitalist economy, the central problems are solved by:', ['The price mechanism', 'A central planning authority', 'Administered prices', 'Rationing'], 0, 'Impersonal forces of demand and supply coordinate decisions.', 'c3'),
        Q('m13', 'In a capitalist economy, if labour becomes relatively cheap, producers will tend to use:', ['Labour-intensive techniques', 'Capital-intensive techniques', 'No technique', 'Only imported machines'], 0, 'Firms pick the least-cost technique using relative factor prices.', 'c3'),
        Q('m14', 'In a capitalist economy, goods are produced mainly for:', ['Those who have purchasing power', 'Those who need them most', 'Government employees', 'Everybody equally'], 0, 'For whom depends on income and property, i.e. buying capacity.', 'c3'),
        Q('m15', 'In a free market, the rate of interest and the rate of return on capital act as:', ['Prices of capital that guide saving and investment', 'Taxes', 'Administered prices', 'Subsidies'], 0, 'They are market prices for capital and decide growth provision.', 'c3', 'moderate'),
        Q('m16', 'Which is a merit of capitalism?', ['Incentives for innovation and technological progress', 'Equal distribution of income', 'No business cycles', 'No advertising expense'], 0, 'Profit rewards innovators; the others are socialist claims.', 'c4'),
        Q('m17', 'Which is a demerit of capitalism?', ['Too few merit goods like education and health care', 'Bureaucracy and red tape', 'No right to private property', 'Administered prices'], 0, 'Profit-led production neglects merit goods.', 'c4'),
        Q('m18', 'Under capitalism, the pattern of demand may not reflect the real needs of society because of:', ['Income inequality', 'Central planning', 'Absence of private property', 'Fixed prices'], 0, 'The rich have more "votes" in the market.', 'c4', 'moderate'),
        Q('m19', 'The concept of socialism was propounded by:', ['Karl Marx and Friedrich Engels', 'Adam Smith', 'Alfred Marshall', 'J. M. Keynes'], 0, 'The Communist Manifesto, 1848.', 'c5'),
        Q('m20', 'A socialist economy is also known as a:', ['Command or centrally planned economy', 'Free market economy', 'Laissez-faire economy', 'Mixed economy'], 0, 'Resources move on commands of the planning authority.', 'c5'),
        Q('m21', 'Prices fixed by the central planning authority in a socialist economy are called:', ['Administered prices', 'Market prices', 'Equilibrium prices', 'Shadow prices'], 0, 'They are set on socio-economic objectives, not by market forces.', 'c5'),
        Q('m22', 'In a socialist economy, the price mechanism:', ['Exists but has only a secondary role', 'Is the main allocator of resources', 'Does not exist at all', 'Fixes wages freely'], 0, 'For example, it may help dispose of accumulated stocks; allocation follows the plan.', 'c5', 'moderate'),
        Q('m23', 'Which of the following is a demerit of socialism?', ['No proper basis for cost calculation because prices are administered', 'Vast inequality of income', 'Waste on advertisement', 'Frequent business cycles'], 0, 'Without market prices, efficient allocation is very difficult.', 'c5'),
        Q('m24', 'Which economy is known for the co-existence of public and private sectors?', ['Mixed economy', 'Capitalist economy', 'Socialist economy', 'Barter economy'], 0, 'Co-existence of sectors is the first feature of a mixed economy.', 'c6'),
        Q('m25', 'A sector in which government and private enterprises join hands is called the:', ['Combined (joint) sector', 'Public sector', 'Private sector', 'Co-operative sector'], 0, 'Joint ventures between the state and private firms form the combined sector.', 'c6'),
        Q('m26', 'Public sector industries in a mixed economy are set up mainly for:', ['Welfare of the community', 'Maximum private profit', 'Advertising', 'Speculation'], 0, 'They are not primarily profit-oriented.', 'c6'),
        Q('m27', 'Which is a possible demerit of a mixed economy?', ['Difficulty in keeping a proper balance between public and private sectors', 'Total absence of private property', 'No government role', 'No planning at all'], 0, 'Balance is hard; excess control or a dominant private sector can follow.', 'c6'),
        Q('m28', '"Every economy in the real world is mixed to some degree." This is because:', ['All economies use both markets and government in allocation', 'All economies are purely socialist', 'No economy has markets', 'Governments never intervene'], 0, 'Real economies combine market allocation with government action.', 'c6', 'moderate'),
        Q('m29', 'At a wage of ₹900, Technique A (40 workers + 2 machines at ₹3,000) costs:', [R(a_cost2), R(b_cost2), R(a_cost1), R(36000)], 0, f'40 × 900 + 2 × 3,000 = {R(a_cost2)}. ₹36,000 forgets the machine cost.', 'c3', 'moderate', '40*900+2*3000'),
        Q('m30', 'In the same example, at a wage of ₹900 the firm will choose:', ['Technique B, costing ' + R(b_cost2), 'Technique A, costing ' + R(a_cost2), 'Technique A, costing ' + R(a_cost1), 'Either, as costs are equal'], 0, f'B costs 10 × 900 + 6 × 3,000 = {R(b_cost2)}, which is lower than A\'s {R(a_cost2)}.', 'c3', 'hard'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'A shoe maker can make 500 pairs a day by Method P (60 workers + 4 machines) or Method Q (20 workers + 12 machines). Machine cost is ₹2,500 per machine per day. Find the least-cost method when the wage is (a) ₹400 and (b) ₹700 a day. Which basic economic problem does this solve, and by what mechanism in a market economy?',
         'model': [table(['Method', 'Cost at ₹400 (₹)', 'Cost at ₹700 (₹)'], [['P (60 L + 4 K)', 60 * 400 + 4 * 2500, 60 * 700 + 4 * 2500], ['Q (20 L + 12 K)', 20 * 400 + 12 * 2500, 20 * 700 + 12 * 2500]]),
                   p('(a) At ₹400: P = ₹34,000, Q = ₹38,000 → choose P (labour-intensive). (b) At ₹700: P = ₹52,000, Q = ₹44,000 → choose Q (capital-intensive).'),
                   p('This is the "how to produce" problem; in a market economy it is solved by the price mechanism — relative factor prices lead firms to the least-cost technique.')],
         'scheme': [{'id': 's1', 'pt': 'Costs at ₹400 for both methods', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Costs at ₹700 for both methods', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Correct choice in each case', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Names "how to produce" and price mechanism / relative factor prices', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Good answers show both costs side by side before choosing.'], 'mistakes': ['Comparing only labour cost and ignoring machine cost.'], 'tips': ['Put both wages in one table — the switch in technique stands out.'],
         'checks': [{'expr': '60*400+4*2500', 'value': 34000, 'label': 'P at ₹400'}, {'expr': '20*400+12*2500', 'value': 38000, 'label': 'Q at ₹400'}, {'expr': '60*700+4*2500', 'value': 52000, 'label': 'P at ₹700'}, {'expr': '20*700+12*2500', 'value': 44000, 'label': 'Q at ₹700'}]},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'table',
         'q': 'Compare capitalist, socialist and mixed economies on: (i) ownership of means of production, (ii) mechanism that solves the central problems, (iii) motive, (iv) role of the government, (v) consumer choice, (vi) distribution of income.',
         'model': [table(['Basis', 'Capitalist', 'Socialist', 'Mixed'], [
             ['(i) Ownership', 'Private', 'Collective / State', 'Both private and public (and joint)'],
             ['(ii) Mechanism', 'Price mechanism', 'Central planning', 'Price mechanism + planning'],
             ['(iii) Motive', 'Profit', 'Social welfare', 'Profit in private sector, welfare in public sector'],
             ['(iv) Government role', 'Minimal', 'Complete', 'Regulates and participates'],
             ['(v) Consumer choice', 'Wide — consumer sovereignty', 'Limited by the plan', 'Wide, with some regulation'],
             ['(vi) Income distribution', 'Highly unequal', 'Relatively equal', 'Less unequal than capitalism']])],
         'scheme': [{'id': f's{i+1}', 'pt': f'Basis ({r}) correct for all three systems', 'm': 1, 'skill': 'concept'} for i, r in enumerate(['i', 'ii', 'iii', 'iv', 'v', 'vi'])],
         'remarks': ['A tabular answer is fastest and scores best.'], 'mistakes': ['Saying the price mechanism is totally absent in socialism — it exists with a secondary role.'], 'tips': ['Keep the same order of bases you were given.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Explain with a numerical example how the price mechanism decides "what to produce" in a capitalist economy.',
         'model': [p(f'Suppose goods X and Y each cost {R(400)} and sell at {R(450)}, giving a profit of {R(50)} a unit. Consumers start preferring X: its price rises to {R(520)} (profit {R(120)} a unit), while Y\'s price falls to {R(410)} (profit {R(10)} a unit).'),
                   p('Higher profit attracts producers to X and lower profit pushes them out of Y. So more X and less Y is produced — the pattern consumers asked for through their spending. No planner is needed; prices act as signals. This is consumer sovereignty working through the price mechanism.')],
         'scheme': [{'id': 's1', 'pt': 'Sets up a numerical example with costs and prices', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Shows profit change following price change', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Explains movement of resources towards the more profitable good', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Links to consumer sovereignty / price mechanism', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Examiners want the chain: demand → price → profit → output.'], 'mistakes': ['Saying the government decides what to produce in capitalism.'], 'tips': ['Write the chain with arrows before the example.']},
    ]

    viva = [
        V('v1', 'What are the basic problems of an economy?',
          'Because resources are scarce, every economy faces four basic problems: what to produce and how to produce; then for whom to produce, that is, how output is distributed; and finally what provision to make for economic growth.',
          [P('p1', 'What to produce', 2, 'what produce|what goods|which goods|what to make'), P('p2', 'How to produce', 3, 'how produce|technique|method of production|how to make'),
           P('p3', 'For whom to produce', 3, 'what produce produce|how produce produce|produce produce how|produce produce what|distribut|sharing|share output|share of output|share the output'), P('p4', 'Provision for economic growth', 2, 'growth|future|saving|invest')], 'c1'),
        V('v2', 'How does a capitalist economy solve its central problems?',
          'A capitalist economy has no planning authority; it solves its central problems through the price mechanism, that is, the free play of demand and supply. Consumers\' demand decides what is produced, producers choose the least-cost technique using relative factor prices, goods go to those with purchasing power, and interest rates and returns on capital guide saving and investment.',
          [P('p1', 'Through the price mechanism / market forces of demand and supply', 5, 'price mechanism|market mechanism|demand and supply|supply and demand|market forces|forces of demand|price system'),
           P('p2', 'No central planning authority', 1, 'no plan|no central|without plan|not plan|no government|without government', min=1),
           P('p3', 'At least two of: consumer demand decides what; least-cost technique/relative factor prices decides how; purchasing power decides for whom', 4, 'consumer|demand decid|profit', 'least cost|cheap|relative factor|factor price|cost minim|lowest cost', 'purchasing power|buying capacity|income|afford|can pay', min=2)], 'c3'),
        V('v3', 'What is consumer sovereignty?',
          'Consumer sovereignty means the consumer is king: through their purchases, buyers ultimately decide which goods and services are produced and in what quantities, and producers must follow their preferences. It is a feature of a capitalist economy.',
          [P('p1', 'Consumer is king / consumers decide what is produced', 5, 'consumer king|consumer is king|consumers decide|consumer decide|buyers decide|consumers determine|consumer determin|buyer determin'),
           P('p2', 'Through their purchases / spending; producers follow preferences', 3, 'purchas|spending|spend|buy|preference|demand', min=1),
           P('p3', 'Feature of capitalism / free market', 2, 'capitalis|free market|market economy|laissez')], 'c2'),
        V('v4', 'What are administered prices?',
          'Administered prices are prices fixed by the central planning authority in a socialist economy on the basis of socio-economic objectives, not by the market forces of demand and supply.',
          [P('p1', 'Fixed by the central planning authority / government', 4, 'planning authority|government|state|planner|authorit'),
           P('p2', 'Not determined by market forces of demand and supply', 3, 'not market|not by market|not by demand|not determined by demand|no market|instead of market|rather than market|not by the market|not demand and supply'),
           P('p3', 'Used in a socialist economy, based on socio-economic goals', 3, 'socialis|command|centrally planned|planned economy|social objective|socio economic', min=1)], 'c5'),
        V('v5', 'What are the three sectors in a mixed economy?',
          'A mixed economy has three sectors: the private sector, run by individuals for profit but regulated by government; the public sector, set up by the state for public welfare; and the combined or joint sector, where government and private enterprise work together.',
          [P('p1', 'Private sector — profit, regulated', 3, 'private'), P('p2', 'Public sector — welfare', 3, 'public|state owned|government sector'),
           P('p3', 'Combined / joint sector', 4, 'joint|combined|together|partnership|both government and private|government and private')], 'c6'),
        V('v6', 'Is the price mechanism completely absent in a socialist economy?',
          'No, it is not completely absent. The price mechanism exists in a socialist economy but plays only a secondary role, for example to dispose of accumulated stocks. Resources are allocated according to the central plan, and prices are mostly administered prices.',
          [P('p1', 'No — it is not completely absent; it exists', 4, 'no|not complete|not absent|not totally|exists|does exist|present', min=1),
           P('p2', 'Only a secondary / minor role', 4, 'secondary|minor|limited role|small role|minimum role|minimal|little role'),
           P('p3', 'Allocation is by the central plan / administered prices', 2, 'plan|administered', min=1)], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Rivertown chooses its economic system', 'difficulty': 'moderate',
              'case': ('Rivertown is a newly independent island state. Its council is split. One group wants every factory and farm to be owned by the state, with a planning board deciding output and fixing prices. A second group wants no government role at all, with private owners free to produce whatever earns the most profit. '
                       'A third group proposes that the state should run the port and power plant, private firms should run shops and factories under labour and pollution laws, and the state and a private shipping firm should jointly build a dry dock. The council also decides that 30% of national output should be saved and invested every year.'),
              'mcqs': [
                  Q('k1a', 'The first group\'s proposal describes a:', ['Socialist (command) economy', 'Capitalist economy', 'Mixed economy', 'Laissez-faire economy'], 0, 'State ownership, central planning and fixed prices are socialist features.', 'c5', 'core'),
                  Q('k1b', 'Under the second group\'s proposal, what to produce would be decided mainly by:', ['Consumers through the price mechanism', 'The planning board', 'Administered prices', 'The council by vote'], 0, 'In a free market, consumer demand and prices decide output.', 'c3', 'core'),
                  Q('k1c', 'The dry dock built jointly by the state and a private shipping firm belongs to the:', ['Combined (joint) sector', 'Public sector', 'Private sector', 'Co-operative sector'], 0, 'Government and private enterprise joining hands = combined sector.', 'c6', 'core'),
                  Q('k1d', 'If 30% of output is saved and invested, what percentage of output is left for current consumption?', [f'{k_cons}%', '30%', '130%', '100%'], 0, '100 − 30 = 70% is left for current consumption. Deciding how much to save and invest is the basic problem of provision for economic growth.', 'c1', 'moderate', '100-30'),
                  Q('k1e', 'Labour and pollution laws for private firms are meant to correct which demerit of capitalism?', ['Exploitation of labour and environmental damage', 'Bureaucracy and red tape', 'Lack of private property', 'Absence of competition'], 0, 'Regulation checks the harms of unregulated profit-seeking.', 'c4', 'core'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch01', 'n': 2, 'title': 'Basic Problems of an Economy & Role of Price Mechanism',
        'outcomes': ['State the central economic problem and its four basic problems with examples.', 'Explain the features of capitalist, socialist and mixed economies.', 'Explain how the price mechanism solves what, how and for whom to produce in a capitalist economy.', 'Evaluate the merits and demerits of each system.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['fnd-p4-ch01-u01'],
                 'exam_tip': 'MCQs test the matching of features to systems (administered prices → socialism; consumer sovereignty → capitalism; joint sector → mixed). Learn three or four merits and demerits of each.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Central problem = scarcity; four basic problems: what, how, for whom, provision for growth.', 'Capitalism: private property, profit motive, freedom of enterprise and choice, consumer sovereignty, competition, no government interference — solved by the price mechanism.',
                                 'Socialism (Marx & Engels, 1848): collective ownership, central planning, limited consumer choice, relative equality, administered prices, no competition.', 'Mixed: co-existence of private, public and combined sectors; markets plus government.'],
                     'remember': ['Price mechanism: demand → price → profit → output.', 'How to produce: decided by relative factor prices.', 'For whom: decided by purchasing power (income + property).', 'USSR 1917–1990 = classic socialist example.'],
                     'traps': ['The price mechanism is not absent in socialism; it has a secondary role.', 'Consumer sovereignty is a capitalist feature, but its reality is often called a "myth" in the demerits.', 'Mixed economy is not always a golden path — it has its own demerits.']},
        'quickref': [{'k': '4 basic problems', 'v': 'What, how, for whom, provision for growth'}, {'k': 'Capitalism', 'v': 'Price mechanism; profit motive; consumer sovereignty'}, {'k': 'Socialism', 'v': 'Central planning; administered prices; collective ownership'},
                     {'k': 'Mixed', 'v': 'Private + public + joint sectors'}, {'k': 'How to produce', 'v': 'Least-cost technique at current factor prices'}],
        'viva': viva, 'cases': cases,
    }
